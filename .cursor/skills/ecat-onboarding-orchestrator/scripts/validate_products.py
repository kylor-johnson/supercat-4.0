#!/usr/bin/env python3
"""Validate an eCat products.csv and inventory its taxonomy codes.

Headers are matched case-insensitively because the importer downcases them.
Exits non-zero only on hard FAILs (duplicates, blank required fields, invalid
Hideable, missing columns) so a phase gate can branch on the result. Advisory
WARNINGS (e.g. long BaseItemCode) print but do not fail.

Usage:
    python validate_products.py path/to/products.csv
"""
import argparse
import csv
import sys

REQUIRED = ["BaseItemCode", "TradeNameCode", "CollectionCodes", "CategoryCodes", "LongDesc"]
# Advisory only. The importer accepts longer codes (mali org has live 21-char
# item_numbers; the DB column is unbounded varchar). Keep codes short for image
# filenames / grid display, but a long code is NOT an import failure.
BIC_ADVISORY_LEN = 20


def load_rows(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return [], {}
        lookup = {name.strip().lower(): name for name in reader.fieldnames}
        return list(reader), lookup


def get(row, lookup, field):
    actual = lookup.get(field.lower())
    return (row.get(actual) or "").strip() if actual else ""


def split_codes(value):
    return [c.strip() for c in value.split(",") if c.strip()]


def main():
    ap = argparse.ArgumentParser(description="Validate eCat products.csv")
    ap.add_argument("csv_path", help="path to products.csv")
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
        if hideable and hideable not in ("Y", "N"):
            issues.append(f"row {i} ({bic or '?'}): invalid Hideable '{hideable}' (want Y/N)")
        if hideable == "N":
            visible += 1

        if get(r, lookup, "ImageFileName"):
            with_images += 1

        for c in split_codes(get(r, lookup, "CollectionCodes")):
            collections.add(c)
        for c in split_codes(get(r, lookup, "CategoryCodes")):
            categories.add(c)

    dupes = {b: lines for b, lines in seen.items() if len(lines) > 1}
    for b, lines in dupes.items():
        issues.append(f"DUPLICATE BaseItemCode '{b}' on rows {lines}")

    has_hideable = "hideable" in lookup
    all_codes = collections | categories
    # Spaces in a code are the reliable Auto-Create signal (codes become iPad labels,
    # e.g. "HAVEN ALU."). Length alone is NOT reliable — Standard orgs can ship long
    # single-token codes (mali has "ACCESSORIES", "STRING") and remain Standard.
    auto_create = any(" " in c for c in all_codes)

    print(f"File: {args.csv_path}")
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
