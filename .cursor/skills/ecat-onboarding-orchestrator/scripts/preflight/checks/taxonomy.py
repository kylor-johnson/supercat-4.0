#!/usr/bin/env python3
"""Taxonomy pre-registration — groups never auto-create.

Under the Standard method every `TradeNameCode`, `CollectionCodes` and `CategoryCodes`
value must already exist in Admin. Under Auto-Create the strings become the iPad labels
and are created on import — which is why a cryptic internal code (`COL126`, `TN1`) must
never ship: whatever you put in the column is what the rep reads on the iPad.

**Groups never auto-create under either method.** That produced real fatal errors in
Magic Lite's import log, and it is the one part of the taxonomy a product import cannot
bootstrap for you.

Detection of the method follows the existing validator: a space inside a code is the
reliable Auto-Create signal, because length alone is not (mali ships `ACCESSORIES` and
`STRING` as single tokens and is Standard).
"""
from ..core import fail, get, split_codes, warn

CHECK = "taxonomy"
SUBSYSTEM = "core"

CODE_FIELDS = ("TradeNameCode", "CollectionCodes", "CategoryCodes")


def extract(rows, lookup):
    """field -> sorted set of codes used in the file."""
    out = {}
    for field in CODE_FIELDS:
        if field.lower() not in lookup:
            continue
        codes = set()
        for row in rows:
            codes.update(split_codes(get(row, lookup, field)))
        out[field] = codes
    return out


def infer_method(used):
    all_codes = set().union(*used.values()) if used else set()
    return "auto-create" if any(" " in c for c in all_codes) else "standard"


def run(rows, lookup, admin_codes=None, groups=None):
    """Compare taxonomy codes in the file against what exists in Admin.

    admin_codes: iterable of codes that exist in Admin, or None if not supplied.
    groups:      iterable of group codes that exist in Admin, or None.
    """
    used = extract(rows, lookup)
    method = infer_method(used)
    findings = []

    if admin_codes is None:
        findings.append(warn(
            CHECK,
            f"no --admin-taxonomy list supplied: could not confirm any of the "
            f"{sum(len(v) for v in used.values())} taxonomy codes exist in Admin. "
            f"Method looks like {method.upper()}"
            + ("; under Standard every code below must be pre-created"
               if method == "standard" else
               "; codes become the iPad labels verbatim, so verify they are readable"),
        ))
    else:
        known = {str(c).strip().lower() for c in admin_codes if str(c).strip()}
        for field, codes in used.items():
            for code in sorted(codes):
                if code.lower() in known:
                    continue
                if method == "auto-create" and field != "TradeNameCode":
                    findings.append(warn(
                        CHECK,
                        f"{field} '{code}' is not in Admin — Auto-Create will create it "
                        f"and this exact string becomes the iPad label",
                    ))
                else:
                    findings.append(fail(
                        CHECK,
                        f"{field} '{code}' does not exist in Admin and will not "
                        f"auto-create under the {method.upper()} method — pre-create it "
                        f"before import",
                    ))

    if groups is None:
        findings.append(warn(
            CHECK,
            "no --admin-groups list supplied: group existence unverified. Groups NEVER "
            "auto-create from a product import under either method — a missing group is "
            "a fatal error, and it is the one taxonomy layer the import cannot create",
        ))
    elif not list(groups):
        findings.append(fail(
            CHECK,
            "Admin has zero groups. Categories live under groups and groups never "
            "auto-create, so every category in this file will fail. Create the groups "
            "first",
        ))

    cryptic = sorted(
        c for codes in used.values() for c in codes
        if method == "auto-create" and (c.isdigit() or (
            len(c) <= 6 and any(ch.isdigit() for ch in c) and c.isupper()))
    )
    for code in cryptic:
        findings.append(warn(
            CHECK,
            f"'{code}' looks like an internal code, and under Auto-Create it becomes "
            f"the label a rep reads on the iPad. Ship the human-readable name instead",
        ))

    return findings
