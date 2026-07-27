#!/usr/bin/env python3
"""The pre-import gate: one read-only command to run before every FTP upload.

Exit 1 blocks the upload. Exit 2 means a check could not run. Exit 0 with WARNINGs is a
pass. Every check that does not apply to this client prints `SKIP (flag: ...)` — an
unexplained absence is how a deliberate exclusion becomes next quarter's argument.

The gate decides; the agent explains. It never writes to a deliverable.

    python preflight_gate.py --client-dir eCat_Onboarding/mali \\
        --dir eCat_Onboarding/mali/00_Import_Files/Ready_For_Import \\
        --live-state live_mali.json --check-urls --ack-deletes

Live state is passed in, never queried here — a validator asserts against an external
authority (source data, code-derived limits, or the live DB), and keeping the DB out of
this script is what makes it runnable anywhere and honest about what it could not
confirm. `--live-state` takes a JSON document; Phase 2's reconciler generates it.

    {
      "shortname": "mali",
      "queried_at": "2026-07-27T20:00:00Z",
      "price_levels": ["dn", "imap"],
      "custom_fields": {"products": ["Color"], "customers": ["BillTo_Region"]},
      "taxonomy": {"codes": ["ML", "LL", "LIGHT"], "groups": ["MAIN"]},
      "keys": {"products.csv": ["ML-001"], "customers.csv": ["0099"]},
      "counts": {"products.csv": 683, "customers.csv": 3418},
      "uploaded_images": ["ML-001.jpg"]
    }

Anything absent from that document degrades to a WARNING naming what went unconfirmed —
never to a silent pass.
"""
import argparse
import glob
import json
import os
import sys

from preflight import files as family
from preflight.checks import (blanks, bom, custom_fields, dupes, enums, fingerprint,
                              image_urls, images_live, omission, order, refs, taxonomy)
from preflight.core import Report, get, load_rows, skip, warn
from preflight.flags import Profile, parse_profile
from preflight.limits import PROVENANCE, RETIRED_CLAIMS, check_lengths


def _tag(findings, label):
    """Namespace a check's findings by the file they came from."""
    for f in findings or ():
        f.check = f"{label}/{f.check}" if label else f.check
    return findings or []


def _split(value):
    """None means "not supplied"; an empty string means "supplied, and it is empty".

    `--admin-groups ""` asserts that Admin has zero groups — a FAIL, since categories
    live under groups and groups never auto-create. Collapsing it to None would report
    that as merely unverified.
    """
    if value is None:
        return None
    return [v.strip() for v in value.split(",") if v.strip()]


def discover(directory):
    found = []
    for path in sorted(glob.glob(os.path.join(directory, "*.csv"))):
        if family.classify(path):
            found.append(path)
    return found


def load_live_state(path):
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class Gate:
    def __init__(self, args):
        self.args = args
        self.report = Report()
        self.live = load_live_state(args.live_state)
        self.profile = (
            parse_profile(args.profile) if args.profile
            else Profile.undeclared()
        )
        self.paths = list(args.files or [])
        if args.dir:
            self.paths.extend(discover(args.dir))
        self.paths = sorted(set(self.paths))
        self.loaded = {}     # canonical name -> (rows, lookup, path)

    # --- helpers ----------------------------------------------------------------

    def live_keys(self, name):
        keys = (self.live.get("keys") or {}).get(name)
        return list(keys) if keys is not None else None

    def live_count(self, name):
        return (self.live.get("counts") or {}).get(name)

    def registered_fields(self, name):
        mapping = self.live.get("custom_fields") or {}
        key = {"products.csv": "products", "customers.csv": "customers",
               "inventory.csv": "inventory"}.get(name)
        override = _split(self.args.custom_fields) if key == "products" else None
        if override is not None:
            return override
        return mapping.get(key) if key in mapping else None

    def rows_for(self, name):
        entry = self.loaded.get(name)
        return entry if entry else (None, None, None)

    def run_check(self, subsystem, label, check_name, fn):
        """Run fn() unless the client's flags switch this subsystem off."""
        reason = self.profile.skip_reason(subsystem)
        tag = f"{label}/{check_name}" if label else check_name
        self.report.record(tag)
        if reason:
            self.report.add(skip(tag, f"({reason})"))
            return
        self.report.add(_tag(fn(), label))

    # --- the gate ---------------------------------------------------------------

    def run(self):
        args = self.args
        report = self.report

        if not self.paths:
            report.add(warn("gate", "no eCat import files found — nothing to check"))
            return report

        for path in self.paths:
            # Unrecognized files still get the BOM check below; the order check is what
            # reports them as unknown, since that is a question about the upload set.
            name = family.classify(path)
            if name is None:
                continue
            if name in self.loaded:
                report.record("gate")
                report.add(warn(
                    "gate",
                    f"{os.path.basename(path)} and "
                    f"{os.path.basename(self.loaded[name][2])} both resolve to "
                    f"{name} — only the first is checked. Upload exactly one file per "
                    f"family",
                ))
                continue
            self.loaded[name] = (*load_rows(path), path)

        shortname = self.live.get("shortname") or self.profile.shortname
        report.title = (
            f"Pre-import gate — {shortname or 'UNKNOWN ORG'}  "
            f"({len(self.paths)} file(s))"
        )
        report.note(f"Client:  {self.profile.summary()}")
        report.note(f"Limits:  {PROVENANCE} (generated, never transcribed)")
        if self.live:
            report.note(
                f"Live:    {args.live_state} "
                f"(queried {self.live.get('queried_at', 'UNKNOWN — treat as stale')})")
        else:
            report.note("Live:    NONE SUPPLIED — every live-state check degrades to a "
                        "warning. Pass --live-state before a hard-delete upload.")
        for hint, message in self.profile.issues():
            report.record("profile")
            report.add(warn("profile", message))

        # Checks that span the whole upload set.
        self.run_check("core", "", bom.CHECK, lambda: bom.run(self.paths))
        self.run_check("core", "", order.CHECK,
                       lambda: order.run(self.paths, _split(args.order)))

        products_rows, products_lookup, _p = self.rows_for("products.csv")
        product_keys = (
            refs.product_codes(products_rows, products_lookup)
            if products_rows else set()
        )
        group_codes = self._codes_from("option_groups.csv", "Code")
        option_codes = self._codes_from("options.csv", "Code")

        for name in sorted(self.loaded, key=lambda n: family.order_position(n) or 99):
            rows, lookup, path = self.loaded[name]
            info = family.meta(name)
            subsystem = info["subsystem"] if info else "core"
            if not rows:
                report.record(f"{name}/load")
                report.add(warn(f"{name}/load",
                                "no data rows / empty header — is this the right file?"))
                continue
            self.check_file(name, rows, lookup, path, subsystem,
                            product_keys, group_codes, option_codes)

        return report

    def _codes_from(self, name, field):
        rows, lookup, _p = self.rows_for(name)
        if not rows:
            return None
        return {get(r, lookup, field).lower() for r in rows if get(r, lookup, field)}

    def check_file(self, name, rows, lookup, path, subsystem, product_keys,
                   group_codes, option_codes):
        args = self.args
        key_field = family.key_column(name)

        self.run_check(subsystem, name, "lengths",
                       lambda: check_lengths(name, rows, lookup, label_field=key_field))

        if key_field:
            unique = ("UPCValue",) if name == "products.csv" else ()
            self.run_check(
                subsystem, name, dupes.CHECK,
                lambda: dupes.run(
                    name, rows, lookup,
                    key_field=None if name == "customers.csv" else key_field,
                    warn_fields=unique),
            )

        self.run_check(
            subsystem, name, fingerprint.CHECK,
            lambda: fingerprint.run(
                name, rows, lookup, key_field or "BaseItemCode",
                live_keys=self.live_keys(name), live_count=self.live_count(name),
                path=path, client_dir=args.client_dir,
                shortname=self.live.get("shortname") or self.profile.shortname),
        )

        self.run_check(
            subsystem, name, omission.CHECK,
            lambda: omission.run(
                name, rows, lookup, key_field or "BaseItemCode",
                live_keys=self.live_keys(name), live_count=self.live_count(name),
                acknowledged=args.ack_deletes),
        )

        if name in ("products.csv", "customers.csv", "inventory.csv"):
            self.run_check(
                subsystem, name, custom_fields.CHECK,
                lambda: custom_fields.run(name, lookup, self.registered_fields(name)),
            )

        if name == "products.csv":
            self.check_products(rows, lookup, group_codes)
        elif name == "customers.csv":
            self.check_customers(rows, lookup)
        elif name in ("inventory.csv", "stories.csv"):
            self.run_check(
                subsystem, name, refs.CHECK,
                lambda: refs.check_child_file(name, rows, lookup, product_keys),
            )
        elif name == "option_groups.csv":
            self.run_check(
                "options", name, refs.CHECK,
                lambda: refs.check_group_membership(rows, lookup, option_codes),
            )

    def check_products(self, rows, lookup, group_codes):
        args = self.args
        tax = self.live.get("taxonomy") or {}

        self.run_check(
            "core", "products.csv", taxonomy.CHECK,
            lambda: taxonomy.run(
                rows, lookup,
                _split(args.admin_taxonomy) or tax.get("codes"),
                _split(args.admin_groups) if args.admin_groups is not None
                else tax.get("groups")),
        )
        self.run_check(
            "core", "products.csv", "refs",
            lambda: refs.check_related_items(
                rows, lookup, refs.product_codes(rows, lookup)),
        )
        self.run_check(
            "options", "products.csv", "refs-optionsets",
            lambda: refs.check_option_sets(rows, lookup, group_codes),
        )
        self.run_check(
            "images-url", "products.csv", image_urls.CHECK,
            lambda: image_urls.run(
                rows, lookup, check_network=args.check_urls,
                cache_path=args.url_cache),
        )
        self.run_check(
            "images-local", "products.csv", images_live.CHECK,
            lambda: images_live.run(
                rows, lookup, self.live.get("uploaded_images")),
        )
        self.run_check(
            "images", "products.csv", blanks.CHECK,
            lambda: blanks.run(rows, lookup, args.source,
                               source_key_field=args.source_key,
                               source_image_field=args.source_image_field),
        )

    def check_customers(self, rows, lookup):
        levels = _split(self.args.price_levels) or self.live.get("price_levels")
        valid = {c.lower() for c in levels} if levels else None

        def enum_check():
            findings = []
            if valid is None:
                findings.append(warn(
                    enums.CHECK,
                    "no price levels supplied: checked for placeholder/status codes only, "
                    "could not confirm DefaultPriceCode membership. This is the check "
                    "that caught tcd's 100% rejection",
                ))
            prev = None
            for i, row in enumerate(rows, start=2):
                code = get(row, lookup, "BillToCode")
                nm = get(row, lookup, "BillToName")
                is_billto = bool(nm) or (code and code != prev)
                if is_billto:
                    findings.extend(enums.check_required(
                        i, code, row, lookup,
                        ["BillToCode", "BillToName", "BillToAddress1", "BillToCity",
                         "BillToState", "BillToPostCode", "DefaultPriceCode"]))
                    findings.extend(enums.check_price_code(
                        i, code, get(row, lookup, "DefaultPriceCode"), valid))
                elif not (get(row, lookup, "ShipToAddress1")
                          and get(row, lookup, "ShipToCity")):
                    findings.extend(enums.check_required(
                        i, code, row, lookup, ["ShipToAddress1", "ShipToCity"]))
                if code:
                    prev = code
            return findings

        self.run_check("customers", "customers.csv", enums.CHECK, enum_check)


def main():
    ap = argparse.ArgumentParser(
        description="Pre-import gate for the eCat file family (read-only)")
    ap.add_argument("--files", nargs="*", default=None, help="explicit files to check")
    ap.add_argument("--dir", default=None,
                    help="directory to scan for recognized eCat files")
    ap.add_argument("--client-dir", default=None,
                    help="the client's folder; files outside it are a hard FAIL")
    ap.add_argument("--profile", default=None,
                    help="CLIENT_PROFILE.md (defaults to <client-dir>/CLIENT_PROFILE.md)")
    ap.add_argument("--live-state", default=None,
                    help="JSON document of live org state (see module docstring)")
    ap.add_argument("--order", default=None,
                    help="comma-separated planned upload sequence, to verify it")
    ap.add_argument("--price-levels", default=None,
                    help="comma-separated price level codes (overrides --live-state)")
    ap.add_argument("--custom-fields", default=None,
                    help="comma-separated registered product custom fields")
    ap.add_argument("--admin-taxonomy", default=None,
                    help="comma-separated taxonomy codes that exist in Admin")
    ap.add_argument("--admin-groups", default=None,
                    help="comma-separated group codes that exist in Admin")
    ap.add_argument("--source", default=None,
                    help="the client's own file, for the blank-stays-blank check")
    ap.add_argument("--source-key", default=None)
    ap.add_argument("--source-image-field", default=None)
    ap.add_argument("--check-urls", action="store_true",
                    help="HEAD every image URL (network)")
    ap.add_argument("--url-cache", default=None)
    ap.add_argument("--ack-deletes", action="store_true",
                    help="acknowledge the previewed deletions and stop blocking on them")
    ap.add_argument("--claims", action="store_true",
                    help="print the documented limits that are NOT enforced, and why")
    args = ap.parse_args()

    if args.claims:
        print("Documented limits deliberately NOT enforced (traced to code or the DB):\n")
        for claim, why in RETIRED_CLAIMS.items():
            print(f"  {claim}\n    {why}\n")
        return 0

    if args.client_dir and not args.profile:
        candidate = os.path.join(args.client_dir, "CLIENT_PROFILE.md")
        if os.path.exists(candidate):
            args.profile = candidate

    if not args.files and not args.dir:
        ap.error("pass --files and/or --dir")

    report = Gate(args).run()
    print(report.render())
    return report.exit_code


if __name__ == "__main__":
    sys.exit(main())
