#!/usr/bin/env python3
"""Validate an eCat customers.csv before import.

Hard FAILs (exit 1): missing required columns; a UTF-8 BOM; blank required bill-to
fields on a bill-to row; DefaultPriceCode blank / '0' / known status text; a field over
a hard length limit; a duplicate BillToCode across bill-to rows; a ship-to continuation
row missing address or city. Advisory items print as WARNINGS.

The #1 real-world customer-import failure (verified on org `tcd`): DefaultPriceCode = 0
or a status string like PENDING/CLOSED -> every row rejected -> 0 customers imported.
Pass --price-levels (from the live DB / Admin Price Levels) to confirm each code is a
real level.

Field limits come from `Customer::ATTR_LENGTHS` and `ShippingLocation::ATTR_LENGTHS` via
`preflight/limits_generated.py` — never transcribed here. That matters for two fields in
particular: `Terms` is 30, which is the real Pebl rejection (their true trade terms run
62 characters, so it needs a client decision rather than a truncation), and `BillToCode`
is 20, not the 15 the old docs claimed. 15 is real but advisory: the importer logs a
warning above 15 and the model rejects above 20, so both tiers are reported.

This checks the LOCAL file only. It does NOT confirm what actually imported — the client
may have run a newer FTP/Admin import. Pair it with the DB recency check via
ecat-postgres-audit (supercat-postgres-vpn):

    select created_at, left(data, 4000) as data from import_events
    where organization_id = :org_id and data like '%Customers%'
    order by created_at desc limit 5;
    select count(*) from customers where organization_id = :org_id;

Usage:
    python validate_customers.py customers.csv [--price-levels dn,imap,ns,show50]
"""
import argparse
import sys

from preflight.checks import bom, enums
from preflight.core import FAIL, get, load_rows
from preflight.limits import PROVENANCE, check_row_lengths

CSV_FILE = "customers.csv"
REQUIRED = ["BillToCode", "BillToName", "BillToAddress1", "BillToCity",
            "BillToState", "BillToPostCode", "DefaultPriceCode"]
# Kept as a module-level name because callers and tests reference it; the values live in
# preflight/checks/enums.py so the gate and this script cannot drift.
BAD_PRICE_CODES = enums.BAD_PRICE_CODES
PLACEHOLDER = "-"  # eCat convention: ship-to fields = "-" means "same as bill-to"


def main():
    ap = argparse.ArgumentParser(description="Validate eCat customers.csv")
    ap.add_argument("csv_path", help="path to customers.csv")
    ap.add_argument("--price-levels", default="",
                    help="comma-separated valid price level codes from the live DB/Admin")
    args = ap.parse_args()

    valid_levels = {c.strip().lower() for c in args.price_levels.split(",") if c.strip()}

    rows, lookup = load_rows(args.csv_path)
    if not rows:
        print("ERROR: no rows / empty header in file")
        return 2

    issues, warnings = [], []
    missing_headers = [f for f in REQUIRED if f.lower() not in lookup]
    if missing_headers:
        issues.append(f"MISSING REQUIRED COLUMNS: {missing_headers}")
        print(f"File: {args.csv_path}")
        print(f"FAIL: {len(issues)} issue(s)")
        for m in issues:
            print(f"  - {m}")
        return 1

    for finding in bom.run([args.csv_path]):
        issues.append(finding.render())

    bill_to_rows = ship_to_rows = 0
    prev_code = None
    bad_price_seen = set()
    billto_lines = {}

    for i, r in enumerate(rows, start=2):  # row 1 is the header
        code = get(r, lookup, "BillToCode")
        name = get(r, lookup, "BillToName")
        # A row carrying bill-to identity (name present, or a new BillToCode) is a
        # bill-to row; a repeat BillToCode with no name is a ship-to continuation row.
        is_billto = bool(name) or (code and code != prev_code)

        for finding in check_row_lengths(CSV_FILE, r, lookup, i, code or name):
            (issues if finding.severity == FAIL else warnings).append(finding.render())

        if is_billto:
            bill_to_rows += 1
            if code:
                billto_lines.setdefault(code, []).append(i)
            for finding in enums.check_required(i, code, r, lookup, REQUIRED):
                issues.append(finding.render())
            dpc = get(r, lookup, "DefaultPriceCode")
            for finding in enums.check_price_code(i, code, dpc, valid_levels):
                issues.append(finding.render())
                if dpc.lower() in BAD_PRICE_CODES:
                    bad_price_seen.add(dpc)
        else:
            ship_to_rows += 1
            if not get(r, lookup, "ShipToAddress1") or not get(r, lookup, "ShipToCity"):
                issues.append(f"row {i} ({code or '?'}): ship-to continuation row missing "
                              f"ShipToAddress1/ShipToCity")

        if code:
            prev_code = code

    # Ship-to continuation rows legitimately repeat BillToCode, so only bill-to rows
    # count toward the uniqueness constraint (validates_uniqueness_of :code per org).
    for code, lines in sorted(billto_lines.items()):
        if len(lines) > 1:
            issues.append(f"DUPLICATE BillToCode '{code}' on bill-to rows {lines} — "
                          f"unique per org, so the later row(s) are rejected")

    if not valid_levels:
        warnings.append("No --price-levels given: checked for placeholder/status codes only, "
                        "could not confirm DefaultPriceCode membership. Pull codes from the DB.")

    print(f"File: {args.csv_path}")
    print(f"Field limits from {PROVENANCE} (generated, never transcribed)")
    print(f"Rows: {len(rows)} | bill-to: {bill_to_rows} | ship-to continuation: {ship_to_rows}")
    if valid_levels:
        print(f"Validated DefaultPriceCode against: {sorted(valid_levels)}")
    print()

    if warnings:
        print(f"WARNINGS ({len(warnings)}) — advisory, do not block import:")
        for m in warnings:
            print(f"  ? {m}")
        print()

    if issues:
        # Collapse the most common failure to a single loud line if it dominates.
        if bad_price_seen:
            print(f"** DefaultPriceCode blocker: {sorted(bad_price_seen)} — the #1 cause of "
                  f"0 customers imported (see org tcd). **")
        print(f"FAIL: {len(issues)} issue(s)")
        for m in issues:
            print(f"  - {m}")
        return 1

    print("PASS: no hard issues" + (f" ({len(warnings)} advisory)" if warnings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
