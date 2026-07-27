#!/usr/bin/env python3
"""Post-import verification for tcs (org 291).

Reads expected values from local CSVs (after sync_from_june_source.py) and prints
Postgres queries plus a checklist. Run queries via supercat-postgres-vpn MCP.

Usage:
  python3 verify_post_import.py              # print SQL + expectations
  python3 verify_post_import.py --expect     # CSV expectations only
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from urllib.parse import urlparse

BASE = Path(__file__).parent
PRODUCTS = BASE / "products.csv"
OPTIONS = BASE / "options.csv"

SPOT_PRODUCTS = [
    "VNG",
    "VNG50FH",
    "GH1-GPF",
    "GH2-GPF",
    "HSI1",
    "HSI2",
    "CHSI",
    "LL-TUBE6A",
    "LL-TUBE8A",
    "CSHI",
    "LL-TUBE6",
    "LL-TUBE8",
]

SPOT_OPTIONS = [
    "CHSI",
    "CSHI",
    "HSI1",
    "HSI2",
    "WY",
    "HSCM",
    "PF1",
    "BMPM",
    "CHB",
    "PFA",
    "BLK",
]

GONE_PRODUCTS = {"CSHI", "LL-TUBE6", "LL-TUBE8"}
GONE_OPTIONS = {"CSHI"}


def basename_from_image(value: str) -> str | None:
    v = (value or "").strip()
    if not v:
        return None
    if v.startswith("http"):
        path = urlparse(v).path
        name = path.rsplit("/", 1)[-1]
        return name or None
    return v


def load_product_expectations() -> dict[str, str | None]:
    out: dict[str, str | None] = {}
    with PRODUCTS.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            sku = row["BaseItemCode"].strip()
            if sku in SPOT_PRODUCTS:
                primary = (row.get("ImageFileName") or "").split(",")[0].strip()
                out[sku] = basename_from_image(primary)
    return out


def load_option_expectations() -> dict[str, str | None]:
    out: dict[str, str | None] = {}
    with OPTIONS.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            code = row["Code"].strip()
            if code in SPOT_OPTIONS:
                out[code] = basename_from_image(row.get("ImageName") or "")
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expect", action="store_true", help="Print CSV expectations only")
    args = parser.parse_args()

    prod_exp = load_product_expectations()
    opt_exp = load_option_expectations()

    if args.expect:
        print("=== CSV expectations (local source of truth) ===\n")
        print("Products (images_json primary file_name after CDN):")
        for sku in sorted(prod_exp):
            if sku in GONE_PRODUCTS:
                print(f"  {sku}: (should not exist or deleted=true)")
            else:
                print(f"  {sku}: {prod_exp[sku] or '(blank)'}")
        print("\nOptions (image_name after CDN):")
        for code in sorted(opt_exp):
            if code in GONE_OPTIONS:
                print(f"  {code}: (should not exist)")
            else:
                print(f"  {code}: {opt_exp[code] or '(blank)'}")
        return

    skus = [s for s in SPOT_PRODUCTS if s not in GONE_PRODUCTS] + list(GONE_PRODUCTS)
    opt_codes = list(dict.fromkeys(SPOT_OPTIONS))

    print("=== Post-import verification (tcs / org 291) ===\n")
    print("Local CSV validation (run before FTP):")
    print("  python3 validate_source_truth.py\n")

    print("1. Recent import events:")
    print(
        """
SELECT created_at, left(data, 2000) AS data
FROM import_events
WHERE organization_id = 291
ORDER BY created_at DESC
LIMIT 8;
"""
    )
    print("Expect: clean Options, Option Groups, Products, Stories (no :error).")
    print("Look for Option Image Downloads / Product Image Downloads with new CDN URLs.\n")

    print("2. Product spot-check:")
    print(
        f"""
SELECT item_number,
       images_json->0->>'file_name' AS primary_image,
       short_description,
       deleted
FROM products
WHERE organization_id = 291
  AND item_number = ANY(ARRAY[{", ".join(repr(s) for s in skus)}])
ORDER BY item_number;
"""
    )
    print("Expected primary_image from local CSV:")
    for sku in sorted(prod_exp):
        if sku in GONE_PRODUCTS:
            print(f"  {sku}: row missing or deleted=true")
        else:
            print(f"  {sku}: {prod_exp[sku] or '(blank)'}")

    print("\n3. Option spot-check:")
    print(
        f"""
SELECT code, image_name
FROM options
WHERE organization_id = 291
  AND code = ANY(ARRAY[{", ".join(repr(c) for c in opt_codes)}])
ORDER BY code;
"""
    )
    print("Expected image_name from local CSV:")
    for code in sorted(opt_exp):
        if code in GONE_OPTIONS:
            print(f"  {code}: should not exist")
        else:
            print(f"  {code}: {opt_exp[code] or '(blank)'}")

    print("\n4. Finish swatch CDN example:")
    blk = opt_exp.get("BLK")
    if blk:
        print(f"  BLK → {blk} (was Finishes_BLK_750px.jpg pre-sync)")

    print("\n5. iPad spot-check: VNG50FH blank, VNG single-burner, GH-GPF distinct,")
    print("   HSI1/2 distinct, CHSI replaces CSHI, ShortDesc under SKU on configure.")


if __name__ == "__main__":
    main()
