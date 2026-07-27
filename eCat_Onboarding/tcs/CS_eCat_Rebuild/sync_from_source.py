#!/usr/bin/env python3
"""Re-sync option_groups.csv and products.csv OptionSets from client source files.

Source of truth:
  Source Data/option_groups (1).csv
  Source Data/products (4).csv

Also fixes FurnishWeb taxonomy display names and re-applies CDN image URLs.
Preserves RelatedItems, RelatedItems2, Hideable from current products.csv.
"""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent
SRC = BASE.parent / "Source Data"
SRC_GROUPS = SRC / "option_groups (1).csv"
SRC_PRODUCTS = SRC / "products (4).csv"
MASTER = SRC / "Master Sheet E+G-Table 1.csv"
WEIYAN = SRC / "Weiyan LED-Table 1.csv"
ACCESSORIES = SRC / "Accessories-Table 1.csv"
TAX = BASE / "taxonomies.csv"

OPTIONS = BASE / "options.csv"
PRODUCTS = BASE / "products.csv"
OPTION_GROUPS = BASE / "option_groups.csv"
IMAGES_STILL_NEEDED = BASE / "images_still_needed.csv"

ACCESSORY_PRODUCT_CATS = {
    "703001": "Light Bulbs",
    "703002": "Light Bulbs",
    "LL-TUBE6": "Light Bulbs",
    "LL-TUBE8": "Light Bulbs",
    "FB1": "Light Bulbs",
    "FB12V": "Light Bulbs",
    "FBBM1": "Light Bulbs",
    "ADS": "Electric Accessories",
    "CSHI": "Electric Accessories",
    "HSI1": "Electric Accessories",
    "HSI2": "Electric Accessories",
    "TLA": "Electric Accessories",
    "WGS": "Gas Accessories",
    "WGL": "Gas Accessories",
    "GLC": "Gas Accessories",
}

MOUNT_TYPES = ("Wall Mount", "Ceiling Mount", "Post & Pier Mount")
TYPE_PREFIX = {
    "Wall Mount": "WM",
    "Ceiling Mount": "CM",
    "Post & Pier Mount": "PP",
}


def parse_options_field(raw: str) -> list[str]:
    return [c.strip() for c in raw.replace('"', "").split(",") if c.strip()]


def load_groups(path: Path) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            code = row["Code"].strip()
            groups[code] = parse_options_field(row["Options"])
    return groups


def load_option_types(path: Path) -> dict[str, str]:
    types: dict[str, str] = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            types[row["Code"].strip()] = (row.get("Description") or "").strip()
    return types


def split_mount_group(codes: list[str], opt_types: dict[str, str]) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {t: [] for t in MOUNT_TYPES}
    for code in codes:
        t = opt_types.get(code, "")
        if t in buckets:
            buckets[t].append(code)
    return buckets


def mount_suffix(m_code: str) -> str | None:
    if m_code.startswith("M") and m_code[1:].isdigit():
        return m_code[1:]
    return None


def build_derived_groups(
    src_groups: dict[str, list[str]], opt_types: dict[str, str]
) -> dict[str, list[str]]:
    """Build WM/CM/PP splits from source M### groups; pass through W/D/GE."""
    out: dict[str, list[str]] = {}

    # FIN groups: keep rebuild CLEAR fix
    out["FIN001"] = ["COPPER", "BLK", "BRZ", "GRAY", "CLEAR"]
    out["FIN002"] = ["BRASS", "CLEAR"]

    for code, codes in src_groups.items():
        if code.startswith("M") and mount_suffix(code):
            suffix = mount_suffix(code)
            assert suffix is not None
            split = split_mount_group(codes, opt_types)
            for mount_type, prefix in TYPE_PREFIX.items():
                derived = split[mount_type]
                if derived:
                    out[f"{prefix}{suffix}"] = derived
        elif code.startswith(("W", "D", "GE")):
            out[code] = codes

    return out


def sku_ignition(sku: str) -> str:
    if not sku:
        return ""
    if sku.endswith("W") and len(sku) >= 2 and sku[-2].isdigit():
        return "W"
    if sku.endswith("G"):
        return "G"
    if sku.endswith("E"):
        return "E"
    return ""


def map_source_optionsets(
    src_row: dict[str, str],
    groups: dict[str, list[str]],
    ignition: str,
) -> dict[int, str]:
    """Map source products (4) columns to eCat OptionSet1-8."""
    os: dict[int, str] = {i: "" for i in range(1, 9)}
    os[1] = src_row.get("OptionSet1", "").strip()

    m_code = src_row.get("OptionSet2", "").strip()
    d_code = src_row.get("OptionSet3", "").strip()
    ge_code = src_row.get("OptionSet4", "").strip()
    w_code = src_row.get("OptionSet5", "").strip()

    suffix = mount_suffix(m_code) if m_code else None
    if suffix:
        for os_num, prefix in ((2, "WM"), (4, "CM"), (5, "PP")):
            gcode = f"{prefix}{suffix}"
            if gcode in groups:
                os[os_num] = gcode

    if w_code and w_code in groups:
        os[3] = w_code

    if d_code and d_code in groups:
        os[6] = d_code

    if ge_code and ge_code in groups:
        if ignition == "G":
            os[8] = ge_code
        elif ignition in ("E", "W"):
            os[7] = ge_code

    return os


def load_taxonomy_name_maps() -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    tn: dict[str, str] = {}
    col: dict[str, str] = {}
    cat: dict[str, str] = {}
    with open(TAX, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            t = row["Type"].strip()
            code = row["Code"].strip()
            name = row["Name"].strip()
            if t == "TradeName":
                tn[code] = name
            elif t == "Collection":
                col[code] = name
            elif t == "Category":
                cat[code] = name
    return tn, col, cat


def fixture_subtype_to_category_names(subtype: str, cat_map: dict[str, str]) -> str:
    code_str = {
        "Electric Lanterns": "CAT4",
        "Gas Lanterns": "CAT5",
        "Flush Mount, Electric Lanterns": "CAT3,CAT4",
        "Flush Mount, Gas Lanterns": "CAT3,CAT5",
        "RLM Lighting, Pendant Lights": "CAT2",
        "Sconce, RLM Lighting": "CAT1,CAT2",
        "Sconce, Wildlife Friendly": "CAT1,CAT6",
        "Sconce": "CAT1",
        "Flush Mount": "CAT3",
    }.get((subtype or "").strip(), "CAT4")
    names = [cat_map.get(c.strip(), c.strip()) for c in code_str.split(",") if c.strip()]
    return ",".join(names)


def brand_to_trade_name(brand: str, tn_map: dict[str, str]) -> str:
    b = (brand or "").strip()
    if "Biltmore" in b:
        return tn_map.get("TN2", "The CopperSmith Biltmore®")
    return tn_map.get("TN1", "The CopperSmith")


def codes_to_names(code_str: str, mapping: dict[str, str]) -> str:
    parts = [p.strip() for p in (code_str or "").split(",") if p.strip()]
    return ",".join(mapping.get(p, p) for p in parts)


def load_master() -> dict[str, dict]:
    with open(MASTER, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        next(r)
        headers = next(r)
        by_sku: dict[str, dict] = {}
        for row in r:
            if row and row[0].strip():
                d = dict(zip(headers, row + [""] * (len(headers) - len(row))))
                by_sku[row[0].strip()] = d
        return by_sku


def master_lookup(sku: str, by_sku: dict[str, dict]):
    if sku in by_sku:
        return by_sku[sku]
    if sku.endswith("W"):
        for alt in (sku[:-1] + "E", sku[:-1] + "G"):
            if alt in by_sku:
                return by_sku[alt]
    return None


def load_weiyan_images() -> dict[str, str]:
    urls: dict[str, str] = {}
    with open(WEIYAN, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        next(r)
        headers = next(r)
        idx_sku = headers.index("SKU")
        idx_url = headers.index("Main Image File Link")
        for row in r:
            if not row or not row[idx_sku].strip():
                continue
            url = row[idx_url].strip() if idx_url < len(row) else ""
            if url.startswith("http"):
                urls[row[idx_sku].strip()] = url
    return urls


def load_accessory_images() -> dict[str, str]:
    urls: dict[str, str] = {}
    with open(ACCESSORIES, newline="", encoding="utf-8-sig") as f:
        next(f)
        for row in csv.DictReader(f):
            sku = row.get("Accessory SKU", "").strip()
            url = row.get("Accessory Image Link", "").strip()
            if sku and url.startswith("http"):
                urls[sku] = url
    return urls


def apply_taxonomy_and_images(
    products: list[dict],
    src_by_sku: dict[str, dict],
    tn_map: dict[str, str],
    col_map: dict[str, str],
    cat_map: dict[str, str],
    master_by_sku: dict[str, dict],
    weiyan_urls: dict[str, str],
    accessory_urls: dict[str, str],
) -> list[tuple[str, str, str]]:
    """Return list of SKUs still missing images."""
    still_missing: list[tuple[str, str, str]] = []

    for p in products:
        sku = p["BaseItemCode"]

        # Taxonomy: source products already have display names
        if sku in src_by_sku:
            s = src_by_sku[sku]
            p["TradeNameCode"] = s.get("TradeNameCode", "").strip()
            p["CollectionCodes"] = s.get("CollectionCodes", "").strip()
            m = master_by_sku.get(sku)
            if m:
                p["CategoryCodes"] = fixture_subtype_to_category_names(
                    m.get("Fixture Sub-Type (Additional Filtering Options)", ""), cat_map
                )
        elif sku in ACCESSORY_PRODUCT_CATS:
            p["TradeNameCode"] = tn_map.get("TN1", "The CopperSmith")
            p["CollectionCodes"] = col_map.get("COL48", "Accessories")
            p["CategoryCodes"] = ACCESSORY_PRODUCT_CATS[sku]
        elif sku.endswith("W"):
            m = master_lookup(sku, master_by_sku)
            if m:
                p["TradeNameCode"] = brand_to_trade_name(m.get("Brand Name", ""), tn_map)
                p["CollectionCodes"] = m.get("Collection", "").strip()
            p["CategoryCodes"] = cat_map.get("CAT7", "LED Fixtures")
        else:
            m = master_by_sku.get(sku)
            if m:
                p["TradeNameCode"] = brand_to_trade_name(m.get("Brand Name", ""), tn_map)
                p["CollectionCodes"] = m.get("Collection", "").strip()
                p["CategoryCodes"] = fixture_subtype_to_category_names(
                    m.get("Fixture Sub-Type (Additional Filtering Options)", ""), cat_map
                )
            else:
                # Fall back: convert existing codes to names
                p["TradeNameCode"] = codes_to_names(p.get("TradeNameCode", ""), tn_map)
                p["CollectionCodes"] = codes_to_names(p.get("CollectionCodes", ""), col_map)
                p["CategoryCodes"] = codes_to_names(p.get("CategoryCodes", ""), cat_map)

        # Images
        m = master_by_sku.get(sku) or master_lookup(sku, master_by_sku)
        if m and m.get("Main Image File Link", "").strip().startswith("http"):
            p["ImageFileName"] = m["Main Image File Link"].strip()
        elif sku in weiyan_urls:
            p["ImageFileName"] = weiyan_urls[sku]
        elif sku in accessory_urls:
            p["ImageFileName"] = accessory_urls[sku]

        img = (p.get("ImageFileName") or "").strip()
        if not img.startswith("http"):
            name = p.get("LongDesc", sku)[:40]
            cat = ACCESSORY_PRODUCT_CATS.get(sku, "")
            still_missing.append((sku, name, cat or "product"))

    return still_missing


def expected_option_codes(
    src_row: dict[str, str], groups: dict[str, list[str]]
) -> set[str]:
    codes: set[str] = set()
    for key in ("OptionSet1", "OptionSet2", "OptionSet3", "OptionSet4", "OptionSet5"):
        g = src_row.get(key, "").strip()
        if not g:
            continue
        if g.startswith("M") and mount_suffix(g):
            suffix = mount_suffix(g)
            assert suffix is not None
            for prefix in ("WM", "CM", "PP"):
                gc = f"{prefix}{suffix}"
                if gc in groups:
                    codes.update(groups[gc])
        elif g in groups:
            codes.update(groups[g])
    return codes


def actual_option_codes(row: dict[str, str], groups: dict[str, list[str]]) -> set[str]:
    codes: set[str] = set()
    for i in range(1, 9):
        g = row.get(f"OptionSet{i}", "").strip()
        if g and g in groups:
            codes.update(groups[g])
    return codes


def validate(
    products: list[dict],
    src_by_sku: dict[str, dict],
    groups: dict[str, list[str]],
    opt_codes: set[str],
) -> list[str]:
    errors: list[str] = []
    orphans: set[str] = set()
    for gcode, codes in groups.items():
        for c in codes:
            if c not in opt_codes:
                orphans.add(c)
    if orphans:
        errors.append(f"Orphan option codes in groups: {sorted(orphans)[:20]}")

    mismatches = 0
    for sku, srow in src_by_sku.items():
        prow = next((p for p in products if p["BaseItemCode"] == sku), None)
        if not prow:
            errors.append(f"Source SKU missing from products.csv: {sku}")
            continue
        if expected_option_codes(srow, groups) != actual_option_codes(prow, groups):
            mismatches += 1
    if mismatches:
        errors.append(f"Option wiring mismatches vs source: {mismatches}/{len(src_by_sku)}")

    for sku in ("BS61G", "AS41G"):
        prow = next((p for p in products if p["BaseItemCode"] == sku), None)
        if not prow:
            errors.append(f"Spot-check SKU missing: {sku}")
            continue
        codes = actual_option_codes(prow, groups)
        if sku == "BS61G":
            for need in ("GNP4", "GNS4", "BFH3", "SPTS", "WGS"):
                if need not in codes:
                    errors.append(f"BS61G missing expected code {need}")
        if sku == "AS41G":
            for need in ("CMS", "SPTS", "WGS"):
                if need not in codes:
                    errors.append(f"AS41G missing expected code {need}")

    return errors


def write_option_groups(groups: dict[str, list[str]]) -> None:
    rows = []
    for code in sorted(groups.keys()):
        opts = groups[code]
        if not opts:
            continue
        name = code
        if code.startswith("WM"):
            name = f"Wall Mount {code[2:]}"
        elif code.startswith("CM"):
            name = f"Ceiling Mount {code[2:]}"
        elif code.startswith("PP"):
            name = f"Post & Pier Mount {code[2:]}"
        elif code.startswith("W") and code[1:].isdigit():
            name = f"Wall Accessories {code[1:]}"
        elif code.startswith("D") and code[1:].isdigit():
            name = f"Decorative {code[1:]}"
        elif code.startswith("GE"):
            name = f"Gas/Electric {code[2:]}"
        elif code.startswith("FIN"):
            name = f"Finish {code[3:]}"
        rows.append((code, name, ",".join(opts)))

    with open(OPTION_GROUPS, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Code", "Name", "Options", "PriceAddend", "PriceFactor"])
        for code, name, opts in rows:
            w.writerow([code, name, opts, "", ""])


def write_images_still_needed(missing: list[tuple[str, str, str]]) -> None:
    known = {
        "GLC": ("Gas Line Cover", "GAS", "No Catsy URL in Accessories tab"),
        "FBBM1": ("Flame Bulb Battery Module", "BULBS", "No Catsy URL in Accessories tab"),
        "LL-TUBE6": ("LanternLyte 6 Amber Tube Bulb", "BULBS", "No Catsy URL in Accessories tab"),
        "LL-TUBE8": ("LanternLyte 8 Amber Tube Bulb", "BULBS", "No Catsy URL in Accessories tab"),
    }
    rows = []
    seen = set()
    for sku, name, _ in missing:
        if sku not in known:
            continue
        seen.add(sku)
        n, typ, notes = known[sku]
        rows.append((sku, n, typ, notes))
    for sku in known:
        if sku not in seen:
            n, typ, notes = known[sku]
            rows.append((sku, n, typ, notes))

    with open(IMAGES_STILL_NEEDED, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["SKU", "ProductName", "Type", "Notes"])
        w.writerows(rows)


def main() -> None:
    opt_types = load_option_types(OPTIONS)
    opt_codes = set(opt_types.keys())
    src_groups = load_groups(SRC_GROUPS)
    derived_groups = build_derived_groups(src_groups, opt_types)

    with open(SRC_PRODUCTS, newline="", encoding="utf-8-sig") as f:
        src_rows = list(csv.DictReader(f))
    src_by_sku = {r["BaseItemCode"]: r for r in src_rows}

    with open(PRODUCTS, newline="", encoding="utf-8-sig") as f:
        products = list(csv.DictReader(f))
    fieldnames = list(products[0].keys())

    tn_map, col_map, cat_map = load_taxonomy_name_maps()
    master_by_sku = load_master()
    weiyan_urls = load_weiyan_images()
    accessory_urls = load_accessory_images()

    source_skus = set(src_by_sku.keys())
    patched = 0
    for p in products:
        sku = p["BaseItemCode"]
        if sku not in source_skus:
            continue
        ignition = sku_ignition(sku)
        os_map = map_source_optionsets(src_by_sku[sku], derived_groups, ignition)
        for i in range(1, 9):
            p[f"OptionSet{i}"] = os_map[i]
        if ignition == "G":
            p["OptionSet7"] = ""
        elif ignition in ("E", "W"):
            p["OptionSet8"] = ""
        patched += 1

    still_missing = apply_taxonomy_and_images(
        products,
        src_by_sku,
        tn_map,
        col_map,
        cat_map,
        master_by_sku,
        weiyan_urls,
        accessory_urls,
    )

    errors = validate(products, src_by_sku, derived_groups, opt_codes)
    if errors:
        print("VALIDATION ERRORS:")
        for e in errors:
            print(f"  - {e}")
        raise SystemExit(1)

    write_option_groups(derived_groups)

    with open(PRODUCTS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(products)

    write_images_still_needed(still_missing)

    print(f"Written {OPTION_GROUPS} ({len(derived_groups)} groups)")
    print(f"Written {PRODUCTS}")
    print(f"Patched OptionSets for {patched} source SKUs")
    print(f"Validation: 0 errors, {len(src_by_sku)}/{len(src_by_sku)} source SKUs match")
    print(f"Images still needed: {len([s for s, _, _ in still_missing if s in {'GLC','FBBM1','LL-TUBE6','LL-TUBE8'}])} flagged SKUs")


if __name__ == "__main__":
    main()
