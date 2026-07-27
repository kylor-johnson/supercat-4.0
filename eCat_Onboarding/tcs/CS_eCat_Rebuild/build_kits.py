#!/usr/bin/env python3
"""Add 12 RLM conversion kit SKUs and link them on matching wall sconces (Step 3)."""
from __future__ import annotations

import csv
import re
import shutil
from pathlib import Path

BASE = Path(__file__).parent
SRC = BASE.parent / "Source Data"
MASTER = SRC / "Master Sheet E+G-Table 1.csv"
PRODUCTS = BASE / "products.csv"
STORIES = BASE / "stories.csv"

KIT_SKUS = [
    "IR14-CPKIT", "IR14-SMKIT", "IR17-CPKIT", "IR17-SMKIT",
    "KL14-CPKIT", "KL14-SMKIT", "KL17-CPKIT", "KL17-SMKIT",
    "KW14-CPKIT", "KW14-SMKIT", "KW17-CPKIT", "KW17-SMKIT",
]

WALL_BY_FAMILY = {
    "IR14": ["IR14-GN14", "IR14-SA14"],
    "IR17": ["IR17-GN17", "IR17-SA17"],
    "KL14": ["KL14-GN14", "KL14-SA14"],
    "KL17": ["KL17-GN17", "KL17-SA17"],
    "KW14": ["KW14-GN14", "KW14-SA14"],
    "KW17": ["KW17-GN17", "KW17-SA17"],
}

KIT_LABEL = {
    "CPKIT": "Ceiling Pendant Conversion Kit",
    "SMKIT": "Stem Mount Conversion Kit",
}


def load_master() -> dict[str, dict[str, str]]:
    with open(MASTER, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        next(r)
        headers = next(r)
        out: dict[str, dict[str, str]] = {}
        for row in r:
            if row and row[0].strip():
                out[row[0].strip()] = dict(zip(headers, row + [""] * (len(headers) - len(row))))
        return out


def kit_longdesc(sku: str, collection: str) -> str:
    m = re.match(r"^([A-Z]{2})(\d{2})-(CPKIT|SMKIT)$", sku)
    if not m:
        return sku
    family, size, kind = m.groups()
    coll_short = collection.replace(" RLM", "")
    return f'CopperSmith {coll_short} RLM {size}" {KIT_LABEL[kind]}'


def kit_story(sku: str, collection: str, marketing: str) -> str:
    kind = "ceiling pendant" if "CPKIT" in sku else "stem mount"
    coll = collection.replace(" RLM", "")
    base = (
        f"Convert your {coll} RLM wall sconce to a {kind} fixture with this "
        f"handcrafted solid copper conversion kit from CopperSmith."
    )
    if marketing.strip():
        return base + " " + marketing.strip()[:300]
    return base


def dims(h: str, w: str, d: str) -> str:
    parts = []
    if h:
        parts.append(f'{h}"H')
    if w:
        parts.append(f'{w}"W')
    if d:
        parts.append(f'{d}"D')
    return " x ".join(parts) if parts else ""


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


def build() -> None:
    master = load_master()

    with open(PRODUCTS, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    existing = {r["BaseItemCode"].strip() for r in rows}
    kit_rows: list[dict[str, str]] = []
    stories: list[tuple[str, str]] = []

    for sku in KIT_SKUS:
        m = master.get(sku)
        if not m:
            raise SystemExit(f"Missing master row for {sku}")
        coll = m.get("Collection", "").strip()
        kind = "CPKIT" if "CPKIT" in sku else "SMKIT"
        kit_rows.append({
            "BaseItemCode": sku,
            "LongDesc": kit_longdesc(sku, coll),
            "ShortDesc": KIT_LABEL[kind],
            "TradeNameCode": "The CopperSmith",
            "CollectionCodes": coll,
            "CategoryCodes": "RLM Lighting,Pendant Lights",
            "Hideable": "Y",
            "RelatedItems": sku,
            "RelatedItems2TabName": "",
            "RelatedItems2": "",
            "materials": "Copper",
            "dimensions": dims(
                m.get("Height (inches)", ""),
                m.get("Width (inches)", ""),
                m.get("Depth (inches)", ""),
            ),
            "shipweight": m.get("Shipping Weight (lbs)", ""),
            "UPCValue": m.get("UPC", ""),
            "ImageFileName": m.get("Main Image File Link", "").strip(),
            "NetPrice": m.get("Dealer Net ", "").strip(),
            "Price_MAP": m.get("MAP/ IMAP", "").strip(),
            "Price_MSRP": m.get("MSRP/ List Price", "").strip(),
            "OptionSet1": "",
            "OptionSet1Required": "",
            "OptionSet2": "",
            "OptionSet3": "",
            "OptionSet4": "",
            "OptionSet5": "",
            "OptionSet6": "",
            "OptionSet7": "",
            "OptionSet8": "",
            "Genre": "RLM",
            "Subcategory": "",
            "GasElectricDual": "Electric",
            "SecondaryFinish": "",
            "GlassFeatures": "",
            "Extension": "",
            "BackplateWidth": "",
            "BackplateHeight": "",
            "CanopyWidth": "",
            "CanopyHeight": "",
            "BulbBase": "",
            "BulbCount": "",
            "WattsPerBulb": "",
            "TotalWattage": "",
            "Voltage": "",
            "BulbIncluded": "",
            "BulbTypeRequired": "",
            "MarineGrade": "",
            "DarkSky": "",
            "LocationRating": "",
            "ADA": "",
            "Certifications": "",
            "Title20": "",
            "Title24": "",
            "Prop65": m.get("Prop 65", ""),
            "SpecSheet": "",
            "MarketingCopy": "",
            "Warranty": m.get("Warranty", ""),
            "CountryOfOrigin": m.get("Country of Origin", ""),
        })
        stories.append((sku, kit_story(sku, coll, m.get("Marketing Copy", ""))))

    # Link kits on wall sconces via RelatedItems2 / Accessories tab
    family_kits: dict[str, list[str]] = {}
    for sku in KIT_SKUS:
        fam = sku.split("-", 1)[0]
        family_kits.setdefault(fam, []).append(sku)

    wall_updates = 0
    for row in rows:
        sku = row["BaseItemCode"].strip()
        for fam, walls in WALL_BY_FAMILY.items():
            if sku in walls:
                kits = family_kits.get(fam, [])
                row["RelatedItems2TabName"] = "Accessories"
                row["RelatedItems2"] = merge_related(row.get("RelatedItems2", ""), kits)
                wall_updates += 1

    new_skus = [r for r in kit_rows if r["BaseItemCode"] not in existing]
    rows.extend(new_skus)

    shutil.copy(PRODUCTS, PRODUCTS.with_suffix(".csv.pre_kits_bak"))
    with open(PRODUCTS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    # Append stories
    with open(STORIES, newline="", encoding="utf-8-sig") as f:
        sreader = csv.DictReader(f)
        sfields = sreader.fieldnames or ["BaseItemCode", "ProductStory"]
        srows = list(sreader)
    story_existing = {r["BaseItemCode"].strip() for r in srows}
    for sku, story in stories:
        if sku not in story_existing:
            srows.append({"BaseItemCode": sku, "ProductStory": story})

    shutil.copy(STORIES, STORIES.with_suffix(".csv.pre_kits_bak"))
    with open(STORIES, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=sfields)
        w.writeheader()
        w.writerows(srows)

    print(f"Added {len(new_skus)} kit product rows")
    print(f"Updated RelatedItems2 on {wall_updates} RLM wall sconces")
    print(f"Added {len(stories)} kit story rows")


if __name__ == "__main__":
    build()
