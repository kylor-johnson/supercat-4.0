#!/usr/bin/env python3
"""Validate an eCat products.csv and inventory its taxonomy codes.

Headers are matched case-insensitively because the importer downcases them.
Exits non-zero only on hard FAILs (duplicates, blank required fields, invalid
Hideable, missing columns, a UTF-8 BOM, a field over a hard length limit) so a phase
gate can branch on the result. Advisory WARNINGS (truncation-tier overflow, long
BaseItemCode, unconfirmed live state) print but do not fail.

Field limits are NOT written down here. They come from `preflight/limits_generated.py`,
which `tools/gen_limits.py` derives from `Product::ATTR_LENGTHS` in supercat_server. Two
tiers, because the importer has two: the six fields in `ATTRS_TO_TRUNCATE` warn and
silently truncate, everything else rejects the row.

This checks the LOCAL file only. Pass the optional live-state lists to turn the
"could not confirm" warnings into real assertions:

    python validate_products.py products.csv \\
        --custom-fields rohscompliant,Color,voltage \\
        --admin-taxonomy ML,LL,LIGHT,SL \\
        --admin-groups MAIN

Usage:
    python validate_products.py path/to/products.csv
"""
import argparse
import sys

from preflight.checks import bom, custom_fields, dupes, enums, refs, taxonomy
from preflight.core import FAIL, WARNING, get, load_rows, split_codes
from preflight.limits import PROVENANCE, check_lengths

CSV_FILE = "products.csv"
REQUIRED = ["BaseItemCode", "TradeNameCode", "CollectionCodes", "CategoryCodes", "LongDesc"]
# Advisory only, and deliberately NOT the importer's limit. The real cap is 40
# (Product::ATTR_LENGTHS[:item_number]) and it IS enforced; mali's live 21-char codes
# pass because 21 < 40, not because the limit is advisory. Keep codes short for image
# filenames and grid display — that is a preference, not a rule.
BIC_ADVISORY_LEN = 20


def _split_arg(value):
    """None means "not supplied"; an empty string means "supplied, and it is empty".

    The difference is load-bearing: `--admin-groups ""` states that Admin has zero groups,
    which is a FAIL because categories live under groups and groups never auto-create.
    Collapsing it to None would turn that into "unverified" and let the import through.
    """
    if value is None:
        return None
    return [v.strip() for v in value.split(",") if v.strip()]


def main():
    ap = argparse.ArgumentParser(description="Validate eCat products.csv")
    ap.add_argument("csv_path", help="path to products.csv")
    ap.add_argument("--custom-fields", default=None,
                    help="comma-separated custom field names registered in Admin")
    ap.add_argument("--admin-taxonomy", default=None,
                    help="comma-separated taxonomy codes that exist in Admin")
    ap.add_argument("--admin-groups", default=None,
                    help="comma-separated group codes that exist in Admin")
    args = ap.parse_args()

    rows, lookup = load_rows(args.csv_path)
    if not rows:
        print("ERROR: no rows / empty header in file")
        return 2

    missing_headers = [f for f in REQUIRED if f.lower() not in lookup]
    issues = []
    warnings = []
    if missing_headers:
        issues.append(f"MISSING REQUIRED COLUMNS: {missing_headers}")

    for finding in bom.run([args.csv_path]):
        issues.append(finding.render())

    seen = {}
    collections, categories = set(), set()
    visible = with_images = 0

    for i, r in enumerate(rows, start=2):  # row 1 is the header
        bic = get(r, lookup, "BaseItemCode")
        if not bic:
            issues.append(f"row {i}: blank BaseItemCode")
        else:
            if len(bic) > BIC_ADVISORY_LEN:
                warnings.append(
                    f"row {i}: BaseItemCode {len(bic)} chars (>{BIC_ADVISORY_LEN} advisory; "
                    f"importer accepts, keep short for image filenames/display): {bic}"
                )
            seen.setdefault(bic, []).append(i)

        for field in REQUIRED:
            if field == "BaseItemCode":
                continue
            if field.lower() in lookup and not get(r, lookup, field):
                issues.append(f"row {i} ({bic or '?'}): blank {field}")

        hideable = get(r, lookup, "Hideable")
        for finding in enums.check_hideable(i, bic, hideable):
            issues.append(finding.render())
        if hideable == "N":
            visible += 1

        if get(r, lookup, "ImageFileName"):
            with_images += 1

        for c in split_codes(get(r, lookup, "CollectionCodes")):
            collections.add(c)
        for c in split_codes(get(r, lookup, "CategoryCodes")):
            categories.add(c)

    dupes_found = {b: lines for b, lines in seen.items() if len(lines) > 1}
    for b, lines in dupes_found.items():
        issues.append(f"DUPLICATE BaseItemCode '{b}' on rows {lines}")

    # UPC is not unique-constrained, so a repeat imports fine but is almost always a
    # source copy-paste error.
    for finding in dupes.run(CSV_FILE, rows, lookup, key_field=None,
                             warn_fields=("UPCValue",)):
        warnings.append(finding.render())

    for finding in check_lengths(CSV_FILE, rows, lookup, label_field="BaseItemCode"):
        (issues if finding.severity == FAIL else warnings).append(finding.render())

    for finding in custom_fields.run(CSV_FILE, lookup, _split_arg(args.custom_fields)):
        (issues if finding.severity == FAIL else warnings).append(finding.render())

    for finding in taxonomy.run(rows, lookup, _split_arg(args.admin_taxonomy),
                                _split_arg(args.admin_groups)):
        (issues if finding.severity == FAIL else warnings).append(finding.render())

    # RelatedItems targets are checked within this file: the importer warns and drops
    # just the dead link, keeping the product, so this is advisory.
    for finding in refs.check_related_items(rows, lookup, set(seen)):
        (issues if finding.severity == FAIL else warnings).append(finding.render())

    has_hideable = "hideable" in lookup
    all_codes = collections | categories
    # Spaces in a code are the reliable Auto-Create signal (codes become iPad labels,
    # e.g. "HAVEN ALU."). Length alone is NOT reliable — Standard orgs can ship long
    # single-token codes (mali has "ACCESSORIES", "STRING") and remain Standard.
    auto_create = any(" " in c for c in all_codes)

    print(f"File: {args.csv_path}")
    print(f"Field limits from {PROVENANCE} (generated, never transcribed)")
    if has_hideable:
        print(f"Rows: {len(rows)} | Visible (Hideable=N): {visible} | With images: {with_images}")
    else:
        print(f"Rows: {len(rows)} | Hideable column ABSENT (all products visible by default) | With images: {with_images}")
    print(f"CollectionCodes ({len(collections)}): {sorted(collections)}")
    print(f"CategoryCodes ({len(categories)}): {sorted(categories)}")
    if auto_create:
        print("-> Codes contain spaces -> Auto-Create taxonomy: strings become the iPad labels and are")
        print("   created on import. Do NOT pre-create; never ship cryptic codes.")
    else:
        print("-> Codes are single tokens -> likely Standard taxonomy: pre-create every code above in")
        print("   Admin before import (groups never auto-create). Confirm the org's method if unsure.")
    print()

    if warnings:
        print(f"WARNINGS ({len(warnings)}) — advisory, do not block import:")
        for msg in warnings:
            print(f"  ? {msg}")
        print()

    if issues:
        print(f"FAIL: {len(issues)} issue(s)")
        for msg in issues:
            print(f"  - {msg}")
        return 1

    if warnings:
        print(f"PASS: no hard issues ({len(warnings)} advisory warning(s) above)")
    else:
        print("PASS: no data-quality issues")
    return 0


if __name__ == "__main__":
    sys.exit(main())
