#!/usr/bin/env python3
"""CopperSmith eCat perfection pass — 7-stage rebuild from locked source-of-truth."""
from __future__ import annotations

import csv
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent
SRC = BASE.parent / "Source Data"
MASTER = SRC / "Master Sheet E+G-Table 1.csv"
WEIYAN = SRC / "Weiyan LED-Table 1.csv"
ACCESSORIES = SRC / "Accessories-Table 1.csv"
PARTS_SRC = SRC / "Parts-Table 1.csv"
SRC_PRODUCTS = SRC / "products (4).csv"
SRC_GROUPS = SRC / "option_groups (1).csv"

PRODUCTS = BASE / "products.csv"
STORIES = BASE / "stories.csv"
OPTIONS = BASE / "options.csv"
OPTION_GROUPS = BASE / "option_groups.csv"
TAX = BASE / "taxonomies.csv"

TN1 = "The CopperSmith"
TN2 = "The CopperSmith Biltmore®"
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

CATEGORY_MAP = {
    "Electric Lanterns": "Electric Lanterns",
    "Gas Lanterns": "Gas Lanterns",
    "Flush Mount, Electric Lanterns": "Flush Mount,Electric Lanterns",
    "Flush Mount, Gas Lanterns": "Flush Mount,Gas Lanterns",
    "Sconce, Wildlife Friendly": "Sconces,Wildlife Friendly",
    "Sconce": "Sconces",
    "Sconce, RLM Lighting": "Sconces,RLM Lighting",
    "Electric Lanterns, Outdoor LED Fixture": "LED Fixtures",
    "RLM Lighting, Pendant Lights": "RLM Lighting,Pendant Lights",
}

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

HIDEABLE_ALWAYS = set(ACCESSORY_PRODUCT_CATS) | {"16WST", "16WSTH", "9WST", "9WSTH"}

WST_CORRUPT = re.compile(r"^WST[\s\xa0](\d+)\.00$")
SRG_CORRUPT = re.compile(r"^SRG[\s\xa0](\d+)\.00$")
CORRUPT_RE = re.compile(r"[\s\xa0]\d+\.00$")

KIT_SKUS = [
    "IR14-CPKIT", "IR14-SMKIT", "IR17-CPKIT", "IR17-SMKIT",
    "KL14-CPKIT", "KL14-SMKIT", "KL17-CPKIT", "KL17-SMKIT",
    "KW14-CPKIT", "KW14-SMKIT", "KW17-CPKIT", "KW17-SMKIT",
]


def load_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        return fields, list(reader)


def write_rows(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def backup(paths: list[Path], suffix: str = ".pre_perfection_bak") -> None:
    for p in paths:
        if p.exists():
            dest = p.with_name(p.name + suffix)
            shutil.copy(p, dest)
            print(f"  backup {dest.name}")


def run_validate(label: str, *, required: bool = True) -> None:
    r = subprocess.run(
        [sys.executable, str(BASE / "validate.py"), label],
        cwd=BASE,
        capture_output=True,
        text=True,
    )
    print(r.stdout)
    if r.returncode != 0:
        if r.stderr:
            print(r.stderr)
        if required:
            raise SystemExit(f"validate ({label}) failed")


def fix_sku_code(sku: str) -> str | None:
    m = WST_CORRUPT.match(sku)
    if m:
        return f"{m.group(1)}WST"
    m = SRG_CORRUPT.match(sku)
    if m:
        return f"SRG{m.group(1)}"
    return None


def replace_sku_in_csv_field(value: str, mapping: dict[str, str]) -> str:
    if not value:
        return value
    parts = []
    for code in value.split(","):
        code = code.strip()
        parts.append(mapping.get(code, code))
    return ",".join(parts)


def stage0_backup_and_before() -> None:
    print("\n[0] Backup + before report")
    backup([PRODUCTS, STORIES, OPTIONS, OPTION_GROUPS])
    run_validate("before", required=False)


def stage1_sku_integrity() -> dict[str, str]:
    print("\n[1] SKU integrity")
    fields, rows = load_rows(PRODUCTS)
    mapping: dict[str, str] = {}

    for row in rows:
        old = row["BaseItemCode"].strip()
        new = fix_sku_code(old)
        if new and new != old:
            if new in mapping.values() or any(r["BaseItemCode"].strip() == new for r in rows if r["BaseItemCode"].strip() != old):
                print(f"  WARN: skip rename {old!r} -> {new!r} (target exists)")
                continue
            mapping[old] = new
            row["BaseItemCode"] = new
            row["RelatedItems"] = replace_sku_in_csv_field(row.get("RelatedItems", ""), mapping)
            row["RelatedItems2"] = replace_sku_in_csv_field(row.get("RelatedItems2", ""), mapping)
            row["RelatedItems3"] = replace_sku_in_csv_field(row.get("RelatedItems3", ""), mapping)

    for row in rows:
        for col in ("RelatedItems", "RelatedItems2", "RelatedItems3"):
            row[col] = replace_sku_in_csv_field(row.get(col, ""), mapping)

    write_rows(PRODUCTS, fields, rows)
    print(f"  Renamed {len(mapping)} product SKUs: {mapping}")

    _, srows = load_rows(STORIES)
    sfields = ["BaseItemCode", "ProductStory"]
    for row in srows:
        old = row["BaseItemCode"].strip()
        if old in mapping:
            row["BaseItemCode"] = mapping[old]
    # dedupe stories after rename
    seen: set[str] = set()
    deduped = []
    for row in srows:
        sku = row["BaseItemCode"].strip()
        if sku in seen:
            continue
        seen.add(sku)
        deduped.append(row)
    write_rows(STORIES, sfields, deduped)
    return mapping


def load_master_rows() -> dict[str, dict[str, str]]:
    with open(MASTER, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        next(r)
        headers = next(r)
        out: dict[str, dict[str, str]] = {}
        for row in r:
            if row and row[0].strip():
                out[row[0].strip()] = dict(zip(headers, row + [""] * (len(headers) - len(row))))
        return out


def load_weiyan_rows() -> dict[str, dict[str, str]]:
    with open(WEIYAN, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        next(r)
        headers = next(r)
        out: dict[str, dict[str, str]] = {}
        for row in r:
            if row and row[0].strip():
                out[row[0].strip()] = dict(zip(headers, row + [""] * (len(headers) - len(row))))
        return out


def brand_to_trade_name(brand: str, collection: str) -> str:
    if "Biltmore" in (brand or "") or (collection or "").strip() in TN2_COLLECTIONS:
        return TN2
    return TN1


def fixture_to_category(subtype: str) -> str:
    s = (subtype or "").strip()
    return CATEGORY_MAP.get(s, "Electric Lanterns")


def fmt_dims(h: str, w: str, d: str) -> str:
    parts = []
    if h:
        parts.append(f'{h.replace(chr(34), "")}"H' if '"' not in h else f'{h}H')
    if w:
        parts.append(f'{w.replace(chr(34), "")}"W' if '"' not in w else f'{w}W')
    if d:
        parts.append(f'{d.replace(chr(34), "")}"D' if '"' not in d else f'{d}D')
    if not parts:
        return ""
    # normalize to products style: 18.75"H x 10.5"W x 10.5"D
    norm = []
    for p in parts:
        p = p.replace('""', '"')
        if not p.endswith(('"H', '"W', '"D')):
            if p.endswith("H"):
                p = p[:-1] + '"H'
            elif p.endswith("W"):
                p = p[:-1] + '"W'
            elif p.endswith("D"):
                p = p[:-1] + '"D'
        norm.append(p)
    return " x ".join(norm)


def clean_price(val: str) -> str:
    return (val or "").replace("$", "").replace(",", "").strip()


def apply_master_fields(row: dict[str, str], m: dict[str, str]) -> None:
    long_desc = (m.get("Long Description") or m.get("Retailer Product Name") or "").strip()
    short_desc = (m.get("Short Description") or long_desc[:50]).strip()
    coll = m.get("Collection", "").strip()
    subtype = m.get("Fixture Sub-Type (Additional Filtering Options)", "").strip()

    row["LongDesc"] = long_desc[:50] if len(long_desc) > 50 else long_desc
    row["ShortDesc"] = short_desc[:15]
    row["TradeNameCode"] = brand_to_trade_name(m.get("Brand Name", ""), coll)
    row["CollectionCodes"] = coll
    row["CategoryCodes"] = fixture_to_category(subtype)
    row["materials"] = m.get("Material", "").strip()
    row["dimensions"] = fmt_dims(
        m.get("Height (inches)", ""),
        m.get("Width (inches)", ""),
        m.get("Depth (inches)", ""),
    )
    sw = m.get("Shipping Weight (lbs)", "").strip() or m.get("Weight", "").strip()
    row["shipweight"] = sw
    row["UPCValue"] = (
        m.get("UPC", "").strip()
        or m.get("UPC/GTIN", "").strip()
    )
    if row["UPCValue"] in ("----", "#"):
        row["UPCValue"] = ""
    if m.get("Main Image File Link", "").strip().startswith("http"):
        row["ImageFileName"] = m["Main Image File Link"].strip()
    row["NetPrice"] = clean_price(m.get("Dealer Net ", ""))
    row["Price_MAP"] = clean_price(m.get("MAP/ IMAP", ""))
    row["Price_MSRP"] = clean_price(m.get("MSRP/ List Price", ""))
    row["Genre"] = m.get("Primary Genre/ Style", "").strip()
    row["GasElectricDual"] = m.get("Power Source", "").strip()
    row["SecondaryFinish"] = m.get("Secondary Finish", "").strip()
    row["GlassFeatures"] = m.get("Glass Features", "").strip()
    row["Extension"] = m.get("Extension (inches)", "").strip()
    row["BackplateWidth"] = m.get("Backplate Width  (inches)", "").strip()
    row["BackplateHeight"] = m.get("Backplate Height  (inches)", "").strip()
    row["CanopyWidth"] = m.get("Canopy Width  (inches)", "").strip()
    row["CanopyHeight"] = m.get("Canopy Height", "").strip()
    row["BulbBase"] = m.get("Bulb Base", "").strip()
    row["BulbCount"] = m.get("Bulb Count", "").strip()
    row["WattsPerBulb"] = m.get("Watts Per Bulb", "").strip()
    row["TotalWattage"] = m.get("Total Wattage", "").strip()
    row["Voltage"] = m.get("Voltage", "").strip()
    row["BulbIncluded"] = m.get("Bulb Included", "").strip()
    row["BulbTypeRequired"] = m.get("Bulb Type Required", "").strip()
    row["MarineGrade"] = m.get("Marine Grade", "").strip()
    row["DarkSky"] = m.get("Dark Sky", "").strip()
    row["LocationRating"] = m.get("Location Rating", "").strip()
    row["ADA"] = m.get("ADA", "").strip()
    row["Certifications"] = m.get("Certifications", "").strip()
    row["Title20"] = m.get("Title 20", "").strip()
    row["Title24"] = m.get("Title 24", "").strip()
    row["Prop65"] = m.get("Prop 65", "").strip()
    row["SpecSheet"] = m.get("Spec Sheet URL", "").strip()
    row["MarketingCopy"] = m.get("Marketing Copy", "").strip()
    row["Warranty"] = m.get("Warranty", "").strip()
    row["CountryOfOrigin"] = m.get("Country of Origin", "").strip()


def master_lookup(sku: str, master: dict[str, dict[str, str]]) -> dict[str, str] | None:
    if sku in master:
        return master[sku]
    if sku.endswith("W"):
        for alt in (sku[:-1] + "E", sku[:-1] + "G"):
            if alt in master:
                return master[alt]
    return None


def stage2_lantern_rebuild() -> None:
    print("\n[2] Lantern rebuild from Master + Weiyan")
    master = load_master_rows()
    weiyan = load_weiyan_rows()
    lantern_skus = set(master) | set(weiyan)

    fields, rows = load_rows(PRODUCTS)
    updated = 0
    for row in rows:
        sku = row["BaseItemCode"].strip()
        if sku not in lantern_skus:
            continue
        m = weiyan.get(sku) or master.get(sku) or master_lookup(sku, master)
        if not m:
            continue
        apply_master_fields(row, m)
        if sku.endswith("W"):
            row["CategoryCodes"] = "LED Fixtures"
        updated += 1

    write_rows(PRODUCTS, fields, rows)
    print(f"  Updated {updated} lantern rows")


def stage3_options() -> None:
    print("\n[3] options.csv fixes + option_groups sync")
    fields, rows = load_rows(OPTIONS)
    fixes = {"BMPM": "113", "PMAU": "157"}
    for row in rows:
        code = row["Code"].strip()
        if code in fixes:
            row["PriceAddend"] = fixes[code]

    if not any(r["Code"].strip() == "FT" for r in rows):
        rows.append({
            "Code": "FT",
            "Name": "Fluted Top",
            "SortValue": "",
            "Description": "Decorative",
            "ImageName": "FT.jpg",
            "PriceAddend": "58",
            "PriceFactor": "",
        })
        print("  Added FT parent option")

    write_rows(OPTIONS, fields, rows)

    subprocess.run([sys.executable, str(BASE / "sync_from_source.py")], cwd=BASE, check=True)
    subprocess.run([sys.executable, str(BASE / "merge_weiyan_groups.py")], cwd=BASE, check=True)
    reapply_lantern_source_fields()


def reapply_lantern_source_fields() -> None:
    """Re-apply master/weiyan taxonomy + shipweight after sync_from_source overwrites TN2."""
    master = load_master_rows()
    weiyan = load_weiyan_rows()
    lantern_skus = set(master) | set(weiyan)
    fields, rows = load_rows(PRODUCTS)
    n = 0
    for row in rows:
        sku = row["BaseItemCode"].strip()
        if sku not in lantern_skus:
            continue
        m = weiyan.get(sku) or master.get(sku) or master_lookup(sku, master)
        if not m:
            continue
        coll = m.get("Collection", "").strip()
        subtype = m.get("Fixture Sub-Type (Additional Filtering Options)", "").strip()
        row["TradeNameCode"] = brand_to_trade_name(m.get("Brand Name", ""), coll)
        row["CollectionCodes"] = coll
        row["CategoryCodes"] = "LED Fixtures" if sku.endswith("W") else fixture_to_category(subtype)
        row["Genre"] = m.get("Primary Genre/ Style", "").strip()
        sw = m.get("Shipping Weight (lbs)", "").strip() or m.get("Weight", "").strip()
        if sw:
            row["shipweight"] = sw
        n += 1
    write_rows(PRODUCTS, fields, rows)
    print(f"  Re-applied master taxonomy/shipweight on {n} lanterns")


def load_part_skus() -> set[str]:
    skus: set[str] = set()
    with open(PARTS_SRC, newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if not row or not row[0].strip():
                continue
            sku = row[0].strip()
            if sku in ("Accessory SKU", "Master Accessory Index 2026"):
                continue
            skus.add(sku)
    return skus


def stage4_parts_and_kits() -> None:
    print("\n[4] Parts + kits rebuild")
    part_skus = load_part_skus()
    fields, rows = load_rows(PRODUCTS)

    # Remove corrupt + stale part rows; keep lanterns/accessories/kits
    cleaned = []
    removed = 0
    for row in rows:
        sku = row["BaseItemCode"].strip()
        cat = row.get("CategoryCodes", "")
        if cat == "Parts" or sku in part_skus or CORRUPT_RE.search(sku):
            removed += 1
            continue
        cleaned.append(row)

    write_rows(PRODUCTS, fields, cleaned)
    print(f"  Removed {removed} part/corrupt rows")

    subprocess.run([sys.executable, str(BASE / "build_parts.py")], cwd=BASE, check=True)

    # Fix kits in place
    master = load_master_rows()
    fields, rows = load_rows(PRODUCTS)
    for row in rows:
        sku = row["BaseItemCode"].strip()
        if sku not in KIT_SKUS:
            continue
        m = master.get(sku)
        if not m:
            continue
        row["CategoryCodes"] = "RLM Lighting,Pendant Lights"
        row["Genre"] = m.get("Primary Genre/ Style", "RLM").strip() or "RLM"
        sw = m.get("Shipping Weight (lbs)", "").strip() or m.get("Weight", "").strip()
        if sw:
            row["shipweight"] = sw
        if m.get("Main Image File Link", "").strip().startswith("http"):
            row["ImageFileName"] = m["Main Image File Link"].strip()
        row["OptionSet1"] = "FIN001"
        row["OptionSet1Required"] = "Y"
        row["Hideable"] = "Y"

    write_rows(PRODUCTS, fields, rows)
    print(f"  Fixed {len(KIT_SKUS)} kit rows")


def sku_ignition(sku: str) -> str:
    if sku.endswith("W") and len(sku) >= 2 and sku[-2].isdigit():
        return "W"
    if sku.endswith("G"):
        return "G"
    if sku.endswith("E"):
        return "E"
    return ""


def size_sort_key(sku: str, master_row: dict[str, str] | None) -> float:
    if master_row:
        h = master_row.get("Height (inches)", "").strip()
        if h:
            try:
                return float(h.replace('"', ""))
            except ValueError:
                pass
    m = re.search(r"(\d+)", sku)
    return float(m.group(1)) if m else 9999


def merge_related(existing: str, add: list[str]) -> str:
    seen: list[str] = []
    for code in (existing or "").split(","):
        code = code.strip()
        if code and code not in seen:
            seen.append(code)
    for code in add:
        if code not in seen:
            seen.append(code)
    return ",".join(seen)


def stage5_related_and_hideable() -> None:
    print("\n[5] RelatedItems + Hideable + gas ADS/TLA")
    master = load_master_rows()
    weiyan = load_weiyan_rows()
    lantern_skus = set(master) | set(weiyan)

    fields, products = load_rows(PRODUCTS)
    by_sku = {r["BaseItemCode"].strip(): r for r in products}

    families: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for sku in lantern_skus:
        if sku not in by_sku:
            continue
        m = master.get(sku) or weiyan.get(sku) or master_lookup(sku, master)
        if not m:
            continue
        parent = m.get("Parent SKU", "").strip()
        ign = sku_ignition(sku)
        if parent and ign:
            families[parent][ign].append(sku)

    for p in products:
        sku = p["BaseItemCode"].strip()
        if sku not in lantern_skus:
            continue
        m = master.get(sku) or weiyan.get(sku) or master_lookup(sku, master)
        parent_key = m.get("Parent SKU", "").strip() if m else ""
        ign = sku_ignition(sku)
        old_related = [x.strip() for x in (p.get("RelatedItems") or "").split(",") if x.strip()]
        sibling_set: set[str] = set()
        if parent_key and ign:
            sibling_set = set(families[parent_key][ign])
        accessory_codes = [c for c in old_related if c != sku and c not in sibling_set]

        if parent_key and ign and len(families[parent_key][ign]) > 1:
            siblings = sorted(
                families[parent_key][ign],
                key=lambda s: size_sort_key(s, master.get(s) or weiyan.get(s)),
            )
            p["RelatedItems"] = ",".join(siblings)
        elif parent_key and ign:
            p["RelatedItems"] = sku
        else:
            p["RelatedItems"] = sku if not accessory_codes else ",".join([sku] + accessory_codes)

        if accessory_codes:
            p["RelatedItems2"] = ",".join(accessory_codes)
            p["RelatedItems2TabName"] = "Accessories"
        elif sku.endswith("G") and sku in lantern_skus:
            p["RelatedItems2"] = merge_related(p.get("RelatedItems2", ""), ["ADS", "TLA"])
            p["RelatedItems2TabName"] = "Accessories"
        elif not p.get("RelatedItems2"):
            p["RelatedItems2TabName"] = ""

        if sku.endswith("G") and sku in lantern_skus:
            p["RelatedItems2"] = merge_related(p.get("RelatedItems2", ""), ["ADS", "TLA"])
            p["RelatedItems2TabName"] = "Accessories"

        if ign == "G":
            p["OptionSet7"] = ""
        elif ign in ("E", "W"):
            p["OptionSet8"] = ""

    # Hideable heroes
    for parent, ign_map in families.items():
        for ign, skus in ign_map.items():
            live = [s for s in skus if s in by_sku]
            if len(live) <= 1:
                for s in live:
                    if s not in HIDEABLE_ALWAYS:
                        by_sku[s]["Hideable"] = ""
                continue
            ordered = sorted(live, key=lambda s: size_sort_key(s, master.get(s) or weiyan.get(s)))
            by_sku[ordered[0]]["Hideable"] = ""
            for s in ordered[1:]:
                by_sku[s]["Hideable"] = "Y"

    for sku in ACCESSORY_PRODUCT_CATS:
        if sku in by_sku:
            by_sku[sku]["Hideable"] = "Y"

    for row in products:
        sku = row["BaseItemCode"].strip()
        if row.get("CategoryCodes") == "Parts":
            row["Hideable"] = "Y"
        if sku in KIT_SKUS:
            row["Hideable"] = "Y"
        if sku in ACCESSORY_PRODUCT_CATS:
            row["TradeNameCode"] = TN1
            row["CollectionCodes"] = "Accessories"
            row["CategoryCodes"] = ACCESSORY_PRODUCT_CATS[sku]

    # Accessory images
    with open(ACCESSORIES, newline="", encoding="utf-8-sig") as f:
        next(f)
        for row in csv.DictReader(f):
            acc = row.get("Accessory SKU", "").strip()
            url = row.get("Accessory Image Link", "").strip()
            if acc in by_sku and url.startswith("http"):
                by_sku[acc]["ImageFileName"] = url

    write_rows(PRODUCTS, fields, products)
    print("  RelatedItems, gas ADS/TLA, Hideable applied")


def stage6_stories_sync() -> None:
    print("\n[6] stories.csv 1:1 sync")
    master = load_master_rows()
    weiyan = load_weiyan_rows()
    _, products = load_rows(PRODUCTS)
    prod_skus = [r["BaseItemCode"].strip() for r in products]

    existing: dict[str, str] = {}
    if STORIES.exists():
        _, srows = load_rows(STORIES)
        for row in srows:
            existing[row["BaseItemCode"].strip()] = row.get("ProductStory", "")

    stories_out: list[dict[str, str]] = []
    for sku in prod_skus:
        story = existing.get(sku, "")
        m = weiyan.get(sku) or master.get(sku)
        if m:
            mc = m.get("Marketing Copy", "").strip()
            ld = m.get("Long Description", "").strip()
            if mc:
                story = mc
            elif ld and not story:
                story = ld
        if not story:
            row = next((r for r in products if r["BaseItemCode"].strip() == sku), None)
            if row:
                story = row.get("ShortDesc") or row.get("LongDesc") or sku
        stories_out.append({"BaseItemCode": sku, "ProductStory": story})

    write_rows(STORIES, ["BaseItemCode", "ProductStory"], stories_out)
    print(f"  stories rows: {len(stories_out)} (matches products)")


def main() -> None:
    stage0_backup_and_before()
    stage1_sku_integrity()
    stage2_lantern_rebuild()
    stage3_options()
    stage4_parts_and_kits()
    stage5_related_and_hideable()
    reapply_lantern_source_fields()
    stage6_stories_sync()
    print("\n[6b] Full source field sync (Master + Weiyan + Accessories + Parts)")
    subprocess.run([sys.executable, str(BASE / "sync_all_source_fields.py")], cwd=BASE, check=True)
    subprocess.run([sys.executable, str(BASE / "fix_import_warnings.py")], cwd=BASE, check=True)
    print("\n[7] Final validation")
    run_validate("after")
    print("\nDone. Import order: options.csv → option_groups.csv → products.csv → stories.csv")


if __name__ == "__main__":
    main()
