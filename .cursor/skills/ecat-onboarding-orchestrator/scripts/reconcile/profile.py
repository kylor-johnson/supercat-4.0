#!/usr/bin/env python3
"""Reconcile CLIENT_PROFILE.md factual fields against live Postgres and output diffs.

Two modes:

  DEFAULT (diff)
    Reads the `## Live state (reconciled)` block from CLIENT_PROFILE.md,
    queries the live DB, and shows what has drifted. Fields older than
    --stale-days (default 7) are flagged STALE.

  --emit-live-state
    Outputs the JSON document that `preflight_gate.py --live-state` expects.
    Pipe it to a file and pass that file to the gate:

        python scripts/reconcile/profile.py --shortname mali --emit-live-state \\
            > live_mali.json
        python scripts/preflight_gate.py \\
            --dir eCat_Onboarding/mali/00_Import_Files/Ready_For_Import \\
            --live-state live_mali.json --ack-deletes

Connection: set DATABASE_URL env var.
    export DATABASE_URL="postgresql://user:pass@host:5432/supercat_production"

Examples:
    # Show drift since last reconcile
    python scripts/reconcile/profile.py --shortname mali \\
        --client-dir eCat_Onboarding/mali

    # Update the profile's Live state block in place
    python scripts/reconcile/profile.py --shortname mali \\
        --client-dir eCat_Onboarding/mali --update

    # Generate live-state JSON for the gate
    python scripts/reconcile/profile.py --shortname mali --emit-live-state \\
        > live_mali.json

Rule from IMPLEMENTATION_PLAN.md §2.3:
    "Counts must never be typed into prose. They are query results with a timestamp,
    or they do not appear."

This script is the only thing that writes factual counts into CLIENT_PROFILE.md.
"""

import argparse
import dataclasses
import datetime
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# LiveState — the factual fields we track
# ---------------------------------------------------------------------------

_STALE_DAYS_DEFAULT = 7


@dataclasses.dataclass
class LiveState:
    """Factual counts queried from the live DB. None = not yet queried."""
    products_active:      Optional[int]       = None
    products_with_images: Optional[int]       = None
    customers:            Optional[int]       = None
    inventory_rows:       Optional[int]       = None
    orphan_inventory:     Optional[int]       = None
    price_level_codes:    Optional[List[str]] = None
    options:              Optional[int]       = None
    option_groups:        Optional[int]       = None
    lifecycle:            Optional[str]       = None
    queried_at:           Optional[str]       = None  # ISO-8601 UTC

    @classmethod
    def from_dict(cls, d: Dict) -> "LiveState":
        codes = d.get("price_level_codes")
        if isinstance(codes, str):
            codes = [c.strip() for c in codes.split(",") if c.strip()]
        return cls(
            products_active=      _int_or_none(d.get("products_active")),
            products_with_images= _int_or_none(d.get("products_with_images")),
            customers=            _int_or_none(d.get("customers")),
            inventory_rows=       _int_or_none(d.get("inventory_rows")),
            orphan_inventory=     _int_or_none(d.get("orphan_inventory")),
            price_level_codes=    codes,
            options=              _int_or_none(d.get("options")),
            option_groups=        _int_or_none(d.get("option_groups")),
            lifecycle=            d.get("lifecycle"),
            queried_at=           d.get("queried_at"),
        )

    def to_dict(self) -> Dict:
        d = dataclasses.asdict(self)
        if d.get("price_level_codes") is not None:
            d["price_level_codes"] = sorted(d["price_level_codes"])
        return {k: v for k, v in d.items() if v is not None}

    def is_stale(self, stale_days: int = _STALE_DAYS_DEFAULT) -> bool:
        if not self.queried_at:
            return True
        try:
            ts = datetime.datetime.fromisoformat(
                self.queried_at.replace("Z", "+00:00")
            )
            age = datetime.datetime.now(datetime.timezone.utc) - ts
            return age.days >= stale_days
        except Exception:
            return True

    def age_str(self) -> str:
        if not self.queried_at:
            return "never"
        try:
            ts = datetime.datetime.fromisoformat(
                self.queried_at.replace("Z", "+00:00")
            )
            age = datetime.datetime.now(datetime.timezone.utc) - ts
            if age.days == 0:
                hours = age.seconds // 3600
                return f"{hours}h ago" if hours else "< 1h ago"
            return f"{age.days}d ago"
        except Exception:
            return self.queried_at


def _int_or_none(v) -> Optional[int]:
    if v is None:
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# CLIENT_PROFILE.md — block read/write
# ---------------------------------------------------------------------------

_BLOCK_START = "<!-- reconcile:start"
_BLOCK_END = "<!-- reconcile:end -->"
_SECTION_HEADER = "## Live state (reconciled)"


def read_profile_block(path: str) -> Tuple[Optional[LiveState], Optional[str]]:
    """Parse the ``## Live state (reconciled)`` block from CLIENT_PROFILE.md.

    Returns (LiveState, queried_at) if a block was found, (None, None) otherwise.
    """
    try:
        text = open(path, "r", encoding="utf-8").read()
    except OSError:
        return None, None

    match = re.search(
        r"<!-- reconcile:start\s*(\{.*?\})\s*-->",
        text,
        re.S,
    )
    if not match:
        return None, None
    try:
        data = json.loads(match.group(1))
        state = LiveState.from_dict(data)
        return state, state.queried_at
    except Exception:
        return None, None


def _make_block(state: LiveState) -> str:
    """Render the reconcile block to embed in CLIENT_PROFILE.md."""
    d = state.to_dict()
    json_payload = json.dumps(d, sort_keys=True)

    lines = [
        _SECTION_HEADER,
        "",
        f"<!-- reconcile:start {json_payload} -->",
        "",
        "| Field | DB live | Queried |",
        "|---|---|---|",
    ]
    date_str = (state.queried_at or "")[:10]

    def row(label, value):
        return f"| {label} | {value} | {date_str} |"

    if state.products_active is not None:
        lines.append(row("Products (active)", f"**{state.products_active:,}**"))
    if state.products_with_images is not None and state.products_active:
        pct = state.products_with_images / state.products_active * 100
        lines.append(row(
            "With images",
            f"**{state.products_with_images:,}** ({pct:.0f}%)"
        ))
    if state.customers is not None:
        lines.append(row("Customers", f"**{state.customers:,}**"))
    if state.inventory_rows is not None:
        lines.append(row("Inventory rows", f"**{state.inventory_rows:,}**"))
    if state.orphan_inventory is not None:
        flag = " ⚠" if state.orphan_inventory > 0 else ""
        lines.append(row("Orphan inventory", f"**{state.orphan_inventory:,}**{flag}"))
    if state.price_level_codes is not None:
        codes = ", ".join(f"`{c}`" for c in sorted(state.price_level_codes))
        lines.append(row("Price levels", codes or "_none_"))
    if state.options is not None:
        lines.append(row("Options", f"**{state.options:,}**"))
    if state.option_groups is not None:
        lines.append(row("Option groups", f"**{state.option_groups:,}**"))
    if state.lifecycle is not None:
        lines.append(row("Lifecycle", f"`{state.lifecycle}`"))

    lines.append("")
    lines.append(_BLOCK_END)
    return "\n".join(lines)


def write_profile_block(path: str, state: LiveState) -> bool:
    """Write or replace the ``## Live state (reconciled)`` block in CLIENT_PROFILE.md.

    Returns True if the file was changed, False if it did not exist.
    """
    try:
        text = open(path, "r", encoding="utf-8").read()
    except OSError:
        return False

    block = _make_block(state)

    # If a reconciled section already exists, replace it wholesale.
    pattern = re.compile(
        r"^## Live state \(reconciled\).*?<!-- reconcile:end -->",
        re.M | re.S,
    )
    if pattern.search(text):
        new_text = pattern.sub(block, text)
    else:
        # Append before the first ## heading after ## Import history, or at end.
        anchor = re.search(r"^## Import history", text, re.M)
        if anchor:
            insert_at = anchor.start()
            new_text = text[:insert_at] + block + "\n\n" + text[insert_at:]
        else:
            new_text = text.rstrip("\n") + "\n\n" + block + "\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)
    return True


# ---------------------------------------------------------------------------
# Diff
# ---------------------------------------------------------------------------

_DRIFT = "DRIFT"
_FRESH = "✓"
_NEW = "NEW"
_STALE = "STALE"
_NARRATIVE = "~"   # field exists in profile as narrative text, not a count


def _fmt(v) -> str:
    if v is None:
        return "—"
    if isinstance(v, list):
        return ",".join(sorted(str(x) for x in v)) or "none"
    if isinstance(v, int):
        return f"{v:,}"
    return str(v)


def diff_report(
    db: LiveState,
    profile: Optional[LiveState],
    shortname: str,
    stale_days: int = _STALE_DAYS_DEFAULT,
    warnings: Optional[List[str]] = None,
) -> Tuple[str, int]:
    """Produce a human-readable diff report and count of drift fields.

    Returns (report_text, drift_count).
    drift_count > 0 means the profile needs --update.
    """
    lines = []
    lines.append(f"Reconcile: {shortname}  (queried {db.queried_at or 'now'})")
    lines.append("")

    if profile is None:
        profile_label = "not reconciled"
    elif profile.is_stale(stale_days):
        profile_label = f"last reconciled {profile.age_str()} — STALE (>{stale_days}d)"
    else:
        profile_label = f"last reconciled {profile.age_str()}"

    header = (
        f"  {'Field':<24}  {'DB live':<16}  {profile_label:<36}  Status"
    )
    lines.append(header)
    lines.append("  " + "-" * 24 + "  " + "-" * 16 + "  " + "-" * 36 + "  " + "-" * 8)

    drift = 0

    def row(label, db_val, profile_val, is_narrative=False):
        nonlocal drift
        db_s = _fmt(db_val)
        pr_s = _fmt(profile_val)

        if db_val is None:
            status = "?"
        elif profile_val is None:
            status = _NEW
            drift += 1
        elif is_narrative:
            status = _NARRATIVE
        elif db_s == pr_s:
            status = _STALE if (profile and profile.is_stale(stale_days)) else _FRESH
        else:
            status = f"{_DRIFT} ← was {pr_s}"
            drift += 1

        lines.append(f"  {label:<24}  {db_s:<16}  {pr_s:<36}  {status}")

    row("products (active)",  db.products_active,      profile and profile.products_active)
    row("with images",        db.products_with_images, profile and profile.products_with_images)
    row("customers",          db.customers,            profile and profile.customers)
    row("inventory rows",     db.inventory_rows,       profile and profile.inventory_rows)
    row("orphan inventory",   db.orphan_inventory,     profile and profile.orphan_inventory)
    row("price levels",       db.price_level_codes,    profile and profile.price_level_codes)
    row("options",            db.options,              profile and profile.options)
    row("option groups",      db.option_groups,        profile and profile.option_groups)
    row("lifecycle",          db.lifecycle,            profile and profile.lifecycle,
        is_narrative=True)

    lines.append("")

    if warnings:
        lines.append(f"  Queries with issues ({len(warnings)}):")
        for w in warnings:
            lines.append(f"    ! {w}")
        lines.append("")

    if drift > 0:
        lines.append(
            f"DRIFT: {drift} field(s) differ. "
            f"Run with --update to write back to CLIENT_PROFILE.md."
        )
    else:
        age = profile.age_str() if profile else "never"
        stale_note = (
            f" STALE (last {age}, >{stale_days}d — re-run to refresh)"
            if (profile and profile.is_stale(stale_days)) else ""
        )
        lines.append(f"MATCH: profile is current.{stale_note}")

    lines.append(
        "Run with --emit-live-state to output JSON for "
        "preflight_gate.py --live-state."
    )

    return "\n".join(lines), drift


# ---------------------------------------------------------------------------
# Resolve org from shortname or CLIENT_PROFILE.md
# ---------------------------------------------------------------------------

def _resolve_shortname(args) -> str:
    if args.shortname:
        return args.shortname
    if args.client_dir:
        profile_path = os.path.join(args.client_dir, "CLIENT_PROFILE.md")
        try:
            text = open(profile_path, "r", encoding="utf-8").read()
            m = re.search(r"\*\*Org shortname:\*\*\s*`?(\w+)`?", text)
            if m:
                return m.group(1)
        except OSError:
            pass
    return ""


def _profile_path(args) -> Optional[str]:
    if args.profile:
        return args.profile
    if args.client_dir:
        p = os.path.join(args.client_dir, "CLIENT_PROFILE.md")
        if os.path.exists(p):
            return p
    return None


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--shortname", default=None,
                    help="eCat org shortname (e.g. mali, leg, libco)")
    ap.add_argument("--client-dir", default=None,
                    help="client folder, e.g. eCat_Onboarding/mali "
                         "(also used to locate CLIENT_PROFILE.md)")
    ap.add_argument("--profile", default=None,
                    help="explicit path to CLIENT_PROFILE.md")
    ap.add_argument("--emit-live-state", action="store_true",
                    help="output the preflight_gate.py --live-state JSON to stdout")
    ap.add_argument("--update", action="store_true",
                    help="write reconciled values back to CLIENT_PROFILE.md")
    ap.add_argument("--stale-days", type=int, default=_STALE_DAYS_DEFAULT,
                    help=f"flag profile fields as STALE after this many days "
                         f"(default {_STALE_DAYS_DEFAULT})")
    ap.add_argument("--db-url", default=None,
                    help="Postgres URL (overrides DATABASE_URL env var)")
    ap.add_argument("--out", default=None,
                    help="write output to this file instead of stdout")
    args = ap.parse_args()

    shortname = _resolve_shortname(args)
    if not shortname:
        ap.error(
            "Pass --shortname SHORTNAME or --client-dir pointing at a folder that "
            "contains a CLIENT_PROFILE.md with '**Org shortname:**'."
        )

    # Connect and query.
    try:
        from reconcile.queries import (
            Executor, ORG_BY_SHORTNAME,
            build_live_state, query_full_counts, connect,
        )
    except ImportError:
        # Allow running as: python scripts/reconcile/profile.py
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
        from reconcile.queries import (
            Executor, ORG_BY_SHORTNAME,
            build_live_state, query_full_counts, connect,
        )

    try:
        conn = connect(args.db_url)
    except (EnvironmentError, ImportError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    exc_runner = Executor(conn)

    # Resolve org_id.
    org = exc_runner.one(ORG_BY_SHORTNAME, {"shortname": shortname})
    if not org:
        print(
            f"ERROR: org '{shortname}' not found in the database. "
            f"Check the shortname and your DATABASE_URL.",
            file=sys.stderr,
        )
        return 2

    org_id = org["id"]

    # --emit-live-state mode: assemble the gate JSON and exit.
    if args.emit_live_state:
        try:
            live = build_live_state(exc_runner, shortname)
        except Exception as exc:
            print(f"ERROR building live state: {exc}", file=sys.stderr)
            return 2

        output = json.dumps(live, indent=2, sort_keys=True)

        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Wrote live-state JSON to {args.out}", file=sys.stderr)
        else:
            print(output)

        if live.get("_warnings"):
            print("", file=sys.stderr)
            print("Warnings (some queries degraded):", file=sys.stderr)
            for w in live["_warnings"]:
                print(f"  ! {w}", file=sys.stderr)

        return 0

    # Default mode: diff.
    profile_path = _profile_path(args)
    profile_state, _ = read_profile_block(profile_path) if profile_path else (None, None)

    db_counts = query_full_counts(exc_runner, org_id)
    db_state = LiveState.from_dict({
        **db_counts,
        "queried_at": datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
    })

    report, drift = diff_report(
        db_state,
        profile_state,
        shortname,
        stale_days=args.stale_days,
    )

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report + "\n")
        print(f"Wrote diff to {args.out}", file=sys.stderr)
    else:
        print(report)

    if args.update:
        if not profile_path:
            print(
                "WARNING: --update passed but no CLIENT_PROFILE.md found. "
                "Pass --client-dir or --profile.",
                file=sys.stderr,
            )
        else:
            ok = write_profile_block(profile_path, db_state)
            if ok:
                print(
                    f"\nUpdated: {profile_path}",
                    file=sys.stderr,
                )
            else:
                print(
                    f"WARNING: could not write to {profile_path}",
                    file=sys.stderr,
                )

    return 1 if drift > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
