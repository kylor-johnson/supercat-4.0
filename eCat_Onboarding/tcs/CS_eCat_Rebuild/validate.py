#!/usr/bin/env python3
"""CopperSmith eCat rebuild validator — fails on regressions between stages."""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

BASE = Path(__file__).parent
SRC = BASE.parent / "Source Data"
MASTER = SRC / "Master Sheet E+G-Table 1.csv"
WEIYAN = SRC / "Weiyan LED-Table 1.csv"
PARTS = SRC / "Parts-Table 1.csv"
SRC_PRODUCTS = SRC / "products (4).csv"

PRODUCTS = BASE / "products.csv"
STORIES = BASE / "stories.csv"
OPTIONS = BASE / "options.csv"
OPTION_GROUPS = BASE / "option_groups.csv"
CUSTOMERS = BASE / "customers.csv"

CUSTOMER_REQUIRED_HEADERS = {
    "BillToCode",
    "BillToName",
    "BillToAddress1",
    "BillToCity",
    "BillToState",
    "BillToPostCode",
    "DefaultPriceCode",
    "ShipToCity",
}
CUSTOMER_REQUIRED_FIELDS = [
    "BillToCode",
    "BillToName",
    "BillToAddress1",
    "BillToCity",
    "BillToState",
    "BillToPostCode",
    "DefaultPriceCode",
    "ShipToCity",
]
VALID_PRICE_CODES = {"map", "msrp"}
VENDOR_BILL_TO_CODES = {"contact_103", "contact_212", "contact_963"}

TN2 = "The CopperSmith Biltmore®"
TN1 = "The CopperSmith"
TN2_COLLECTIONS = {
    "Biltmore® Antler Hill",
    "Biltmore® Amherst",
    "Biltmore® Aurora",
    "Biltmore® Approach",
    "Biltmore® Arcus",
    "Biltmore® Flush Traveler",
    "Biltmore® Gala",
    "Biltmore® Vestibule",
    "Traveler",
}

CORRUPT_RE = re.compile(r"[\s\xa0]\d+\.00$")
WST_CORRUPT = re.compile(r"^WST[\s\xa0](\d+)\.00$")
SRG_CORRUPT = re.compile(r"^SRG[\s\xa0](\d+)\.00$")

GAS_ACCESSORIES = ("ADS", "TLA")


def load_csv(path: Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_master_shipweight_expectations() -> dict[str, str]:
    """SKU -> expected shipweight when master has Shipping Weight or Weight."""
    out: dict[str, str] = {}
    with open(MASTER, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        next(r)
        headers = next(r)
        sku_i = headers.index("SKU")
        sw_i = headers.index("Shipping Weight (lbs)")
        w_i = headers.index("Weight")
        for row in r:
            if not row or not row[sku_i].strip():
                continue
            sw = row[sw_i].strip() if sw_i < len(row) else ""
            w = row[w_i].strip() if w_i < len(row) else ""
            val = sw or w
            if val:
                out[row[sku_i].strip()] = val
    with open(WEIYAN, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        next(r)
        headers = next(r)
        sku_i = headers.index("SKU")
        sw_i = headers.index("Shipping Weight (lbs)")
        w_i = headers.index("Weight")
        for row in r:
            if not row or not row[sku_i].strip():
                continue
            sw = row[sw_i].strip() if sw_i < len(row) else ""
            w = row[w_i].strip() if w_i < len(row) else ""
            val = sw or w
            if val:
                out[row[sku_i].strip()] = val
    return out


def load_master_skus() -> set[str]:
    return set(load_master_shipweight_expectations().keys()) | _all_master_weiyan_skus()


def _all_master_weiyan_skus() -> set[str]:
    skus: set[str] = set()
    with open(MASTER, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        next(r)
        headers = next(r)
        idx = headers.index("SKU")
        for row in r:
            if row and row[idx].strip():
                skus.add(row[idx].strip())
    with open(WEIYAN, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        next(r)
        headers = next(r)
        idx = headers.index("SKU")
        for row in r:
            if row and row[idx].strip():
                skus.add(row[idx].strip())
    return skus


def load_part_skus() -> set[str]:
    skus: set[str] = set()
    with open(PARTS, newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if not row or not row[0].strip():
                continue
            sku = row[0].strip()
            if sku in ("Accessory SKU", "Master Accessory Index 2026"):
                continue
            skus.add(sku)
    return skus


def sku_ignition(sku: str) -> str:
    if sku.endswith("W") and len(sku) >= 2 and sku[-2].isdigit():
        return "W"
    if sku.endswith("G"):
        return "G"
    if sku.endswith("E"):
        return "E"
    return ""


def is_lantern_sku(sku: str, lantern_skus: set[str]) -> bool:
    return sku in lantern_skus


def validate_customers() -> list[str]:
    errors: list[str] = []
    if not CUSTOMERS.exists():
        errors.append(f"Missing {CUSTOMERS.name}")
        return errors

    customers = load_csv(CUSTOMERS)
    if len(customers) != 721:
        errors.append(f"customers.csv row count: expected 721, got {len(customers)}")

    headers = set(customers[0].keys()) if customers else set()
    missing_headers = CUSTOMER_REQUIRED_HEADERS - headers
    if missing_headers:
        errors.append(f"customers.csv missing headers: {sorted(missing_headers)}")

    codes: list[str] = []
    for i, row in enumerate(customers, start=2):
        for field in CUSTOMER_REQUIRED_FIELDS:
            if not (row.get(field) or "").strip():
                errors.append(f"customers.csv line {i}: blank {field}")
        code = (row.get("DefaultPriceCode") or "").strip().lower()
        if code and code not in VALID_PRICE_CODES:
            errors.append(f"customers.csv line {i}: invalid DefaultPriceCode {code!r}")
        if (row.get("BillToCode") or "").strip() in VENDOR_BILL_TO_CODES:
            errors.append(f"customers.csv line {i}: vendor leaked into output ({row.get('BillToCode')})")
        codes.append((row.get("BillToCode") or "").strip())

    dupes = [c for c, n in Counter(codes).items() if n > 1]
    if dupes:
        errors.append(f"customers.csv duplicate BillToCode: {dupes[:5]}")

    sorted_codes = [c for c in codes if c]
    if sorted_codes != sorted(sorted_codes, key=_customer_sort_key):
        errors.append("customers.csv not sorted by BillToCode")

    return errors


def _customer_sort_key(code: str) -> tuple[int, str]:
    m = re.match(r"contact_(\d+)$", code)
    if m:
        return (0, f"{int(m.group(1)):08d}")
    return (1, code)


def validate(label: str = "final") -> list[str]:
    errors: list[str] = []
    products = load_csv(PRODUCTS)
    stories = load_csv(STORIES)
    options = load_csv(OPTIONS)
    groups = load_csv(OPTION_GROUPS)

    master_skus = _all_master_weiyan_skus()
    weiyan_skus = set()  # included in master_skus
    lantern_skus = master_skus
    part_skus = load_part_skus()
    opt_codes = {r["Code"].strip() for r in options}
    sw_expect = load_master_shipweight_expectations()

    prod_by_sku = {r["BaseItemCode"].strip(): r for r in products}
    skus = list(prod_by_sku.keys())

    # --- SKU integrity ---
    for sku in skus:
        if CORRUPT_RE.search(sku) or WST_CORRUPT.match(sku) or SRG_CORRUPT.match(sku):
            errors.append(f"Corrupt BaseItemCode: {sku!r}")

    dupes = [k for k, v in Counter(skus).items() if v > 1]
    if dupes:
        errors.append(f"Duplicate BaseItemCodes: {dupes[:10]}")

    for need in ("9WST", "16WST"):
        if need not in prod_by_sku:
            errors.append(f"Missing required lantern SKU: {need}")

    for bad in ("WST 16.00", "WST 9.00", "WST\xa016.00", "WST\xa09.00"):
        if bad in prod_by_sku:
            errors.append(f"Corrupt WST SKU still present: {bad!r}")

    # --- Stories 1:1 ---
    story_skus = {r["BaseItemCode"].strip() for r in stories}
    prod_set = set(skus)
    missing_stories = sorted(prod_set - story_skus)[:20]
    orphan_stories = sorted(story_skus - prod_set)[:20]
    if missing_stories:
        errors.append(f"products without stories ({len(prod_set - story_skus)}): {missing_stories}")
    if orphan_stories:
        errors.append(f"stories without products ({len(story_skus - prod_set)}): {orphan_stories}")

    # --- Options prices + FT ---
    for code, price in (("BMPM", "113"), ("PMAU", "157")):
        row = next((r for r in options if r["Code"].strip() == code), None)
        if not row:
            errors.append(f"Missing option code: {code}")
        elif (row.get("PriceAddend") or "").strip() != price:
            errors.append(f"{code} PriceAddend should be {price}, got {row.get('PriceAddend')!r}")
    if "FT" not in opt_codes:
        errors.append("Missing parent option FT (Fluted Top)")

    # --- TN2 Biltmore ---
    for sku in master_skus:
        if sku not in prod_by_sku:
            continue
        row = prod_by_sku[sku]
        with open(MASTER, newline="", encoding="utf-8-sig") as f:
            r = csv.reader(f)
            next(r)
            headers = next(r)
            for mrow in r:
                if mrow and mrow[0].strip() == sku:
                    coll = mrow[headers.index("Collection")].strip()
                    brand = mrow[headers.index("Brand Name")].strip()
                    break
            else:
                continue
        expect_tn2 = "Biltmore" in brand or coll in TN2_COLLECTIONS
        tn = row.get("TradeNameCode", "").strip()
        if expect_tn2 and tn != TN2:
            errors.append(f"{sku}: expected TN2 {TN2!r}, got {tn!r}")
        elif not expect_tn2 and tn == TN2 and coll not in TN2_COLLECTIONS:
            errors.append(f"{sku}: unexpected TN2 for collection {coll!r}")

    # --- Gas ADS/TLA on RelatedItems2 ---
    gas_missing = []
    for sku, row in prod_by_sku.items():
        if not sku.endswith("G") or not is_lantern_sku(sku, lantern_skus):
            continue
        r2 = [x.strip() for x in (row.get("RelatedItems2") or "").split(",") if x.strip()]
        for need in GAS_ACCESSORIES:
            if need not in r2:
                gas_missing.append(sku)
                break
    if gas_missing:
        errors.append(f"Gas lanterns missing ADS/TLA on RelatedItems2 ({len(gas_missing)}): {gas_missing[:8]}")

    # --- Parts SKUs literal ---
    for sku in part_skus:
        if sku in prod_by_sku:
            continue
        if any(sku in k for k in prod_by_sku if SRG_CORRUPT.match(k)):
            continue
        errors.append(f"Part SKU missing from products: {sku}")

    for sku in skus:
        if SRG_CORRUPT.match(sku):
            errors.append(f"Corrupt part SKU in products: {sku!r}")

    # --- RelatedItems3 broken refs ---
    broken_r3 = []
    for sku, row in prod_by_sku.items():
        if not is_lantern_sku(sku, lantern_skus):
            continue
        for ref in (row.get("RelatedItems3") or "").split(","):
            ref = ref.strip()
            if not ref:
                continue
            if ref not in prod_by_sku or CORRUPT_RE.search(ref):
                broken_r3.append((sku, ref))
    if broken_r3:
        errors.append(f"Broken RelatedItems3 refs ({len(broken_r3)}): {broken_r3[:8]}")

    for sku in sorted(lantern_skus):
        if sku not in prod_by_sku:
            errors.append(f"Lantern SKU missing from products: {sku}")

    # --- Lantern shipweight (only when source has data) ---
    blank_sw = []
    for sku, expected in sw_expect.items():
        if sku not in prod_by_sku:
            continue
        actual = (prod_by_sku[sku].get("shipweight") or "").strip()
        if not actual:
            blank_sw.append(sku)
        elif actual != expected:
            errors.append(f"{sku}: shipweight {actual!r} != source {expected!r}")
    if blank_sw:
        errors.append(
            f"Lanterns with blank shipweight but source has weight ({len(blank_sw)}): {blank_sw[:10]}"
        )

    # --- Source richness (lanterns) ---
    feat_blank = []
    tags_blank = []
    for sku in sorted(lantern_skus):
        if sku not in prod_by_sku:
            continue
        row = prod_by_sku[sku]
        if not (row.get("Feature1") or "").strip():
            feat_blank.append(sku)
        if not (row.get("ProductTags") or "").strip():
            tags_blank.append(sku)
    if feat_blank:
        errors.append(f"Lanterns missing Feature1 from source ({len(feat_blank)}): {feat_blank[:8]}")
    if tags_blank:
        errors.append(f"Lanterns missing ProductTags from source ({len(tags_blank)}): {tags_blank[:8]}")
    for sku in prod_by_sku:
        if "-CPKIT" in sku or "-SMKIT" in sku:
            cat = prod_by_sku[sku].get("CategoryCodes", "")
            if cat != "RLM Lighting,Pendant Lights":
                errors.append(f"{sku}: kit CategoryCodes should be RLM Lighting,Pendant Lights, got {cat!r}")

    # --- Option group orphans (sample) ---
    orphans: set[str] = set()
    for row in groups:
        for code in (row.get("Options") or "").replace('"', "").split(","):
            code = code.strip()
            if code and code not in opt_codes:
                orphans.add(code)
    if orphans:
        errors.append(f"Orphan option codes in groups: {sorted(orphans)[:15]}")

    errors.extend(validate_customers())
    customer_count = len(load_csv(CUSTOMERS)) if CUSTOMERS.exists() else 0

    print(f"=== validate ({label}) ===")
    print(
        f"products: {len(products)}  stories: {len(stories)}  options: {len(options)}  "
        f"groups: {len(groups)}  customers: {customer_count}"
    )
    if errors:
        print(f"FAIL — {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
    else:
        print("PASS — 0 errors")
    return errors


def main() -> None:
    label = sys.argv[1] if len(sys.argv) > 1 else "final"
    errors = validate(label)
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
