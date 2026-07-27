#!/usr/bin/env python3
"""Surgical products.csv fixes for CopperSmith Tuesday call — NOT a full regenerate."""
import csv
import re
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent
SRC = BASE.parent / "Source Data"
MASTER = SRC / "Master Sheet E+G-Table 1.csv"
ACCESSORIES = SRC / "Accessories-Table 1.csv"
PRODUCTS = BASE / "products.csv"
TAX = BASE / "taxonomies.csv"

# Accessory BaseItemCodes that are standalone products (also may appear as options)
ACCESSORY_PRODUCT_CATS = {
    "703001": "CAT10", "703002": "CAT10", "LL-TUBE6": "CAT10", "LL-TUBE8": "CAT10",
    "FB1": "CAT10", "FB12V": "CAT10", "FBBM1": "CAT10",
    "ADS": "CAT8", "CSHI": "CAT8", "HSI1": "CAT8", "HSI2": "CAT8", "TLA": "CAT8",
    "WGS": "CAT9", "WGL": "CAT9", "GLC": "CAT9",
}


def load_master():
    with open(MASTER, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        next(r)
        headers = next(r)
        rows = []
        for row in r:
            if row and row[0].strip():
                d = dict(zip(headers, row + [""] * (len(headers) - len(row))))
                rows.append(d)
        return rows


def load_taxonomies():
    coll = {}
    with open(TAX, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row["Type"] == "Collection":
                coll[row["Name"].strip()] = row["Code"]
    return coll


def fixture_subtype_to_categories(subtype: str) -> str:
    s = (subtype or "").strip()
    if not s:
        return "CAT4"
    mapping = {
        "Electric Lanterns": "CAT4",
        "Gas Lanterns": "CAT5",
        "Flush Mount, Electric Lanterns": "CAT3,CAT4",
        "Flush Mount, Gas Lanterns": "CAT3,CAT5",
        "RLM Lighting, Pendant Lights": "CAT2",
        "Sconce, RLM Lighting": "CAT1,CAT2",
        "Sconce, Wildlife Friendly": "CAT1,CAT6",
        "Sconce": "CAT1",
        "Flush Mount": "CAT3",
    }
    return mapping.get(s, "CAT4")


def brand_to_tn(brand: str) -> str:
    b = (brand or "").strip()
    if "Biltmore" in b:
        return "TN2"
    return "TN1"


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


def size_sort_key(sku: str, master_row=None) -> float:
    if master_row:
        h = master_row.get("Height (inches)", "").strip()
        if h:
            try:
                return float(h.replace('"', ""))
            except ValueError:
                pass
    m = re.search(r"(\d+)", sku)
    return float(m.group(1)) if m else 9999


def master_lookup_for_sku(sku: str, by_sku):
    if sku in by_sku:
        return by_sku[sku]
    if sku.endswith("W"):
        for alt in (sku[:-1] + "E", sku[:-1] + "G"):
            if alt in by_sku:
                return by_sku[alt]
    return None


def main():
    master = load_master()
    by_sku = {r["SKU"]: r for r in master}
    coll_map = load_taxonomies()

    # Parent SKU -> list of product SKUs by ignition
    families = defaultdict(lambda: defaultdict(list))
    for r in master:
        parent = r["Parent SKU"].strip()
        sku = r["SKU"].strip()
        ign = sku_ignition(sku)
        if parent and sku and ign:
            families[parent][ign].append(sku)

    # Weiyan W SKUs: infer parent from E/G sibling prefix
    with open(PRODUCTS, newline="", encoding="utf-8-sig") as f:
        products = list(csv.DictReader(f))
    fieldnames = list(products[0].keys())

    for col in ("RelatedItems2", "RelatedItems2TabName"):
        if col not in fieldnames:
            # insert after RelatedItems
            idx = fieldnames.index("RelatedItems") + 1
            fieldnames.insert(idx, col)

    w_skus_added = 0
    for p in products:
        sku = p["BaseItemCode"]
        if not sku.endswith("W") or sku in by_sku:
            continue
        ref = master_lookup_for_sku(sku, by_sku)
        if not ref:
            continue
        parent = ref["Parent SKU"].strip()
        ign = "W"
        if sku not in families[parent][ign]:
            families[parent][ign].append(sku)
            w_skus_added += 1

    print(f"Added {w_skus_added} Weiyan W SKUs to family groupings")

    for p in products:
        sku = p["BaseItemCode"]
        m = by_sku.get(sku) or master_lookup_for_sku(sku, by_sku)

        # --- Taxonomy ---
        if sku in ACCESSORY_PRODUCT_CATS:
            p["TradeNameCode"] = "TN1"
            p["CollectionCodes"] = "COL48"
            p["CategoryCodes"] = ACCESSORY_PRODUCT_CATS[sku]
        elif sku.endswith("W"):
            ref = master_lookup_for_sku(sku, by_sku)
            if ref:
                p["TradeNameCode"] = brand_to_tn(ref.get("Brand Name", ""))
                coll_name = ref.get("Collection", "").strip()
                p["CollectionCodes"] = coll_map.get(coll_name, coll_name)
            p["CategoryCodes"] = "CAT7"
        elif m:
            p["TradeNameCode"] = brand_to_tn(m.get("Brand Name", ""))
            coll_name = m.get("Collection", "").strip()
            p["CollectionCodes"] = coll_map.get(coll_name, coll_name)
            p["CategoryCodes"] = fixture_subtype_to_categories(
                m.get("Fixture Sub-Type (Additional Filtering Options)", "")
            )

        # --- Related Items ---
        old_related = [x.strip() for x in (p.get("RelatedItems") or "").split(",") if x.strip()]

        parent_key = None
        ign = sku_ignition(sku)
        if m:
            parent_key = m.get("Parent SKU", "").strip()
        elif sku.endswith("W"):
            ref = master_lookup_for_sku(sku, by_sku)
            if ref:
                parent_key = ref.get("Parent SKU", "").strip()

        sibling_set = set()
        if parent_key and ign:
            sibling_set = set(families[parent_key][ign])

        accessory_codes = [c for c in old_related if c != sku and c not in sibling_set]

        if parent_key and ign and len(families[parent_key][ign]) > 1:
            siblings = sorted(
                families[parent_key][ign],
                key=lambda s: size_sort_key(s, by_sku.get(s)),
            )
            p["RelatedItems"] = ",".join(siblings)
        elif parent_key and ign:
            p["RelatedItems"] = sku
        else:
            p["RelatedItems"] = sku if not accessory_codes else ",".join([sku] + accessory_codes)

        if accessory_codes:
            p["RelatedItems2"] = ",".join(accessory_codes)
            p["RelatedItems2TabName"] = "Accessories"
        else:
            p["RelatedItems2"] = ""
            p["RelatedItems2TabName"] = ""

        # --- Ignition option sets ---
        ign = sku_ignition(sku)
        if ign == "G":
            p["OptionSet7"] = ""
        elif ign == "E":
            p["OptionSet8"] = ""
        elif ign == "W":
            p["OptionSet7"] = ""
            p["OptionSet8"] = ""

        # --- Images from master ---
        if m and m.get("Main Image File Link", "").strip().startswith("http"):
            p["ImageFileName"] = m["Main Image File Link"].strip()
        elif m and m.get("Main Image File Name", "").strip():
            img = m["Main Image File Name"].strip()
            if not (p.get("ImageFileName") or "").startswith("http"):
                p["ImageFileName"] = img if "." in img else f"{img}.jpg"

    # --- Hideable heroes per parent + ignition ---
    prod_by_sku = {p["BaseItemCode"]: p for p in products}
    for parent, ign_map in families.items():
        for ign, skus in ign_map.items():
            live = [s for s in skus if s in prod_by_sku]
            if len(live) <= 1:
                for s in live:
                    prod_by_sku[s]["Hideable"] = ""
                continue
            ordered = sorted(live, key=lambda s: size_sort_key(s, by_sku.get(s)))
            prod_by_sku[ordered[0]]["Hideable"] = ""
            for s in ordered[1:]:
                prod_by_sku[s]["Hideable"] = "Y"

    # Accessory / single-SKU products: clear hideable
    for sku in ACCESSORY_PRODUCT_CATS:
        if sku in prod_by_sku:
            prod_by_sku[sku]["Hideable"] = ""

    # Accessory image URLs from accessories tab
    with open(ACCESSORIES, newline="", encoding="utf-8-sig") as f:
        next(f)
        for row in csv.DictReader(f):
            acc_sku = row.get("Accessory SKU", "").strip()
            url = row.get("Accessory Image Link", "").strip()
            if acc_sku in prod_by_sku and url.startswith("http"):
                prod_by_sku[acc_sku]["ImageFileName"] = url

    with open(PRODUCTS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(products)

    # Stats
    gas_elec = sum(1 for p in products if p["BaseItemCode"].endswith("G") and p.get("OptionSet7"))
    with_r2 = sum(1 for p in products if p.get("RelatedItems2"))
    tn1 = sum(1 for p in products if p.get("TradeNameCode") == "TN1")
    print(f"Written {PRODUCTS}")
    print(f"Gas SKUs still with OptionSet7: {gas_elec}")
    print(f"Products with RelatedItems2: {with_r2}")
    print(f"TN1 products: {tn1}")


if __name__ == "__main__":
    main()
