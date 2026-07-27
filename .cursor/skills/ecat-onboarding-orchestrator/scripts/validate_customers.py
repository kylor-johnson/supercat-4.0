#!/usr/bin/env python3
"""Validate an eCat customers.csv before import.

Hard FAILs (exit 1): missing required columns; blank required bill-to fields on a
bill-to row; DefaultPriceCode blank / '0' / known status text; field-length overflow;
a ship-to continuation row missing address or city. Advisory items print as WARNINGS.

The #1 real-world customer-import failure (verified on org `tcd`): DefaultPriceCode = 0
or a status string like PENDING/CLOSED -> every row rejected -> 0 customers imported.
Pass --price-levels (from the live DB / Admin Price Levels) to confirm each code is a
real level.

This checks the LOCAL file only. It does NOT confirm what actually imported — the client
may have run a newer FTP/Admin import. Pair it with the DB recency check via
ecat-postgres-audit (user-supercat-postgres-vpn):

    select created_at, left(data, 4000) as data from import_events
    where organization_id = :org_id and data like '%Customers%'
    order by created_at desc limit 5;
    select count(*) from customers where organization_id = :org_id;

Usage:
    python validate_customers.py customers.csv [--price-levels dn,imap,ns,show50]
"""
import argparse
import csv
import sys

REQUIRED = ["BillToCode", "BillToName", "BillToAddress1", "BillToCity",
            "BillToState", "BillToPostCode", "DefaultPriceCode"]
MAX_LEN = {
    "BillToCode": 15, "BillToName": 60, "BillToAddress1": 60, "BillToCity": 60,
    "BillToState": 60, "BillToPostCode": 20, "DefaultPriceCode": 30,
    "ShipToAddress1": 60, "ShipToCity": 60,
}
# DefaultPriceCode values that are not real price levels (ERP placeholders / statuses).
BAD_PRICE_CODES = {"", "0", "pending", "closed", "inactive", "hold", "n/a", "na", "none"}
PLACEHOLDER = "-"  # eCat convention: ship-to fields = "-" means "same as bill-to"


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

    bill_to_rows = ship_to_rows = 0
    prev_code = None
    bad_price_seen = set()

    for i, r in enumerate(rows, start=2):  # row 1 is the header
        code = get(r, lookup, "BillToCode")
        name = get(r, lookup, "BillToName")
        # A row carrying bill-to identity (name present, or a new BillToCode) is a
        # bill-to row; a repeat BillToCode with no name is a ship-to continuation row.
        is_billto = bool(name) or (code and code != prev_code)

        for field, limit in MAX_LEN.items():
            val = get(r, lookup, field)
            if val and val != PLACEHOLDER and len(val) > limit:
                issues.append(f"row {i} ({code or name or '?'}): {field} {len(val)}>{limit} chars")

        if is_billto:
            bill_to_rows += 1
            for field in REQUIRED:
                if not get(r, lookup, field):
                    issues.append(f"row {i} ({code or '?'}): blank required {field}")
            dpc = get(r, lookup, "DefaultPriceCode")
            if dpc:
                if dpc.lower() in BAD_PRICE_CODES:
                    issues.append(
                        f"row {i} ({code or '?'}): DefaultPriceCode '{dpc}' is a placeholder/"
                        f"status, not a price level -> import will reject the row")
                    bad_price_seen.add(dpc)
                elif valid_levels and dpc.lower() not in valid_levels:
                    issues.append(
                        f"row {i} ({code or '?'}): DefaultPriceCode '{dpc}' not in price levels "
                        f"{sorted(valid_levels)}")
        else:
            ship_to_rows += 1
            if not get(r, lookup, "ShipToAddress1") or not get(r, lookup, "ShipToCity"):
                issues.append(f"row {i} ({code or '?'}): ship-to continuation row missing "
                              f"ShipToAddress1/ShipToCity")

        if code:
            prev_code = code

    if not valid_levels:
        warnings.append("No --price-levels given: checked for placeholder/status codes only, "
                        "could not confirm DefaultPriceCode membership. Pull codes from the DB.")

    print(f"File: {args.csv_path}")
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
