#!/usr/bin/env python3
"""Populate EXISTING products.csv columns from source — add only Feature1-6 + ProductTags."""
from __future__ import annotations

import csv
import shutil
from pathlib import Path

BASE = Path(__file__).parent
SRC = BASE.parent / "Source Data"
MASTER = SRC / "Master Sheet E+G-Table 1.csv"
WEIYAN = SRC / "Weiyan LED-Table 1.csv"
ACCESSORIES = SRC / "Accessories-Table 1.csv"
PARTS_SRC = SRC / "Parts-Table 1.csv"
PRODUCTS = BASE / "products.csv"
STORIES = BASE / "stories.csv"

MAX_IMAGES = 6

# Only columns that do NOT already exist on the standard template.
NEW_COLUMNS = ["Feature1", "Feature2", "Feature3", "Feature4", "Feature5", "Feature6", "ProductTags"]

IMAGE_URL_KEYS = [
    "Main Image File Link",
    "Product View 1 - RA ",
    "Product View 2 - LA",
    "Detailed Product View 3",
    "Detailed Product View 4",
    "Detailed Product View 5",
    "Detailed Product View 6",
    "Detailed Product View 7",
    "Matte Black Image - BLK",
    "Oil Rubbed Bronze Image -  BRZ",
    "Graphite Image - GRAY",
]


def load_sheet(path: Path) -> dict[str, dict[str, str]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        next(r)
        headers = next(r)
        out: dict[str, dict[str, str]] = {}
        for row in r:
            if row and row[0].strip():
                out[row[0].strip()] = dict(zip(headers, row + [""] * (len(headers) - len(row))))
        return out


def load_accessories() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with open(ACCESSORIES, newline="", encoding="utf-8-sig") as f:
        next(f)
        for row in csv.DictReader(f):
            sku = row.get("Accessory SKU", "").strip()
            if sku:
                out[sku] = row
    return out


def load_parts() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with open(PARTS_SRC, newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if not row or not row[0].strip():
                continue
            sku = row[0].strip()
            if sku in ("Accessory SKU", "Master Accessory Index 2026"):
                continue
            out[sku] = {
                "name": row[2].strip() if len(row) > 2 else sku,
                "gtin": row[3].strip() if len(row) > 3 else "",
                "net": row[5].strip() if len(row) > 5 else "",
                "map": row[6].strip() if len(row) > 6 else "",
                "msrp": row[7].strip() if len(row) > 7 else "",
                "image": row[9].strip() if len(row) > 9 else "",
            }
    return out


def clean(val: str) -> str:
    v = (val or "").strip()
    return "" if v in ("----", "#", "$") else v


def clean_price(val: str) -> str:
    return clean(val).replace("$", "").replace(",", "")


def http_url(val: str) -> str:
    v = clean(val)
    return v if v.startswith("http") else ""


def master_lookup(sku: str, master: dict[str, dict[str, str]]) -> dict[str, str] | None:
    if sku in master:
        return master[sku]
    if sku.endswith("W"):
        for alt in (sku[:-1] + "E", sku[:-1] + "G"):
            if alt in master:
                return master[alt]
    return None


def fmt_dims(m: dict[str, str]) -> str:
    parts = []
    for key, suffix in (("Height (inches)", "H"), ("Width (inches)", "W"), ("Depth (inches)", "D")):
        v = clean(m.get(key, ""))
        if v:
            parts.append(f'{v.replace(chr(34), "")}"{suffix}')
    return " x ".join(parts)


def collect_image_urls(m: dict[str, str]) -> list[str]:
    seen: list[str] = []
    for key in IMAGE_URL_KEYS:
        url = http_url(m.get(key, ""))
        if url and url not in seen:
            seen.append(url)
        if len(seen) >= MAX_IMAGES:
            break
    return seen


def turtle_friendly(m: dict[str, str], row: dict[str, str]) -> str:
    tf = clean(m.get("Turtle Friendly", ""))
    if tf.lower() in ("yes", "y"):
        return "Yes"
    coll = (row.get("CollectionCodes") or "").lower()
    cat = (row.get("CategoryCodes") or "").lower()
    subtype = clean(m.get("Fixture Sub-Type (Additional Filtering Options)", "")).lower()
    if "turtle friendly" in coll or "wildlife friendly" in cat or "wildlife friendly" in subtype:
        return "Yes"
    return ""


def genre_from_source(m: dict[str, str], is_weiyan: bool) -> str:
    if is_weiyan:
        return clean(m.get("Fixture Style", "")) or clean(m.get("Primary Genre/ Style", ""))
    return clean(m.get("Primary Genre/ Style", ""))


def subcategory_from_source(m: dict[str, str], is_weiyan: bool) -> str:
    if is_weiyan:
        return clean(m.get("Fixture Style", ""))
    return clean(m.get("Fixture Type", ""))


def build_story(m: dict[str, str]) -> str:
    parts: list[str] = []
    mc = clean(m.get("Marketing Copy", ""))
    ld = clean(m.get("Long Description", ""))
    if mc:
        parts.append(mc)
    elif ld:
        parts.append(ld)
    bullets = [clean(m.get(f"Feature {i}", "")) for i in range(1, 7)]
    bullets = [b for b in bullets if b]
    if bullets:
        if parts:
            parts.append("")
        parts.extend(f"• {b}" for b in bullets)
    return "\n".join(parts).strip()


def apply_lantern_existing(row: dict[str, str], m: dict[str, str], *, is_weiyan: bool) -> None:
    """Map source into columns that already exist on products.csv — no duplicate fields."""
    retailer = clean(m.get("Retailer Product Name", ""))
    row["LongDesc"] = retailer[:50] if retailer else clean(m.get("Long Description", ""))[:50]
    row["ShortDesc"] = clean(m.get("Short Description", ""))[:15] or row["LongDesc"][:15]

    row["materials"] = clean(m.get("Material", ""))
    row["dimensions"] = fmt_dims(m)
    sw = clean(m.get("Shipping Weight (lbs)", "")) or clean(m.get("Weight", ""))
    if sw:
        row["shipweight"] = sw

    upc = clean(m.get("UPC", "")) or clean(m.get("UPC/GTIN", ""))
    if upc:
        row["UPCValue"] = upc

    urls = collect_image_urls(m)
    if urls:
        row["ImageFileName"] = ",".join(urls)

    row["NetPrice"] = clean_price(m.get("Dealer Net ", "") or m.get("Dealer Net", ""))
    row["Price_MAP"] = clean_price(m.get("MAP/ IMAP", ""))
    row["Price_MSRP"] = clean_price(m.get("MSRP/ List Price", "") or m.get("MSRP", ""))

    row["Genre"] = genre_from_source(m, is_weiyan)
    row["Subcategory"] = subcategory_from_source(m, is_weiyan)
    row["GasElectricDual"] = clean(m.get("Power Source", ""))
    row["SecondaryFinish"] = clean(m.get("Secondary Finish", ""))
    row["GlassFeatures"] = clean(m.get("Glass Features", ""))

    row["Extension"] = clean(m.get("Extension (inches)", ""))
    row["BackplateWidth"] = clean(m.get("Backplate Width  (inches)", ""))
    row["BackplateHeight"] = clean(m.get("Backplate Height  (inches)", ""))
    row["CanopyWidth"] = clean(m.get("Canopy Width  (inches)", ""))
    row["CanopyHeight"] = clean(m.get("Canopy Height", ""))

    row["BulbBase"] = clean(m.get("Bulb Base", ""))
    row["BulbCount"] = clean(m.get("Bulb Count", ""))
    row["WattsPerBulb"] = clean(m.get("Watts Per Bulb", ""))
    row["TotalWattage"] = clean(m.get("Total Wattage", ""))
    row["Voltage"] = clean(m.get("Voltage", "") or m.get("Total Voltage", ""))
    row["BulbIncluded"] = clean(m.get("Bulb Included", ""))
    row["BulbTypeRequired"] = clean(m.get("Bulb Type Required", ""))
    row["MarineGrade"] = clean(m.get("Marine Grade", ""))
    row["DarkSky"] = clean(m.get("Dark Sky", ""))
    row["LocationRating"] = clean(m.get("Location Rating", ""))
    row["ADA"] = clean(m.get("ADA", ""))
    row["Certifications"] = clean(m.get("Certifications", ""))
    row["Title20"] = clean(m.get("Title 20", ""))
    row["Title24"] = clean(m.get("Title 24", ""))
    row["Prop65"] = clean(m.get("Prop 65", ""))

    row["SpecSheet"] = http_url(m.get("Spec Sheet URL", ""))
    inst = clean(m.get("Installation", ""))
    row["Installation"] = inst or row.get("SpecSheet", "")
    row["MarketingCopy"] = clean(m.get("Marketing Copy", ""))
    row["Warranty"] = clean(m.get("Warranty", ""))
    row["CountryOfOrigin"] = clean(m.get("Country of Origin", ""))
    row["TurtleFriendly"] = turtle_friendly(m, row)

    # Only net-new columns (POC polish — not elsewhere on the row)
    for i in range(1, 7):
        row[f"Feature{i}"] = clean(m.get(f"Feature {i}", ""))
    row["ProductTags"] = clean(m.get("Product Tags", ""))


def apply_accessory_existing(row: dict[str, str], acc: dict[str, str]) -> None:
    name = clean(acc.get("Accessory Name", ""))
    if name:
        row["LongDesc"] = name[:50]
        row["ShortDesc"] = name[:15]
    gtin = clean(acc.get("Accessory GTIN", ""))
    if gtin:
        row["UPCValue"] = gtin
    img = http_url(acc.get("Accessory Image Link", ""))
    if img:
        row["ImageFileName"] = img
    app = http_url(acc.get("Accessory Application Link", ""))
    if app:
        row["Installation"] = app
    net = clean_price(acc.get("Accessory Dealer Net", ""))
    if net:
        row["NetPrice"] = net
    pmap = clean_price(acc.get("Accessory MAP", ""))
    if pmap:
        row["Price_MAP"] = pmap
    msrp = clean_price(acc.get("Accessory MSRP", ""))
    if msrp:
        row["Price_MSRP"] = msrp


def apply_part_existing(row: dict[str, str], part: dict[str, str]) -> None:
    name = part.get("name", "")
    if name:
        row["LongDesc"] = name[:50]
        row["ShortDesc"] = name[:15]
    if part.get("gtin"):
        row["UPCValue"] = part["gtin"]
    if part.get("net"):
        row["NetPrice"] = part["net"]
    if part.get("map"):
        row["Price_MAP"] = part["map"]
    if part.get("msrp"):
        row["Price_MSRP"] = part["msrp"]
    img = http_url(part.get("image", ""))
    if img:
        row["ImageFileName"] = img


def write_rows(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def sync() -> None:
    master = load_sheet(MASTER)
    weiyan = load_sheet(WEIYAN)
    accessories = load_accessories()
    parts = load_parts()

    with open(PRODUCTS, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    for col in NEW_COLUMNS:
        if col not in fields:
            fields.append(col)

    n_lantern = n_acc = n_part = 0
    for row in rows:
        sku = row["BaseItemCode"].strip()
        if sku in weiyan:
            apply_lantern_existing(row, weiyan[sku], is_weiyan=True)
            n_lantern += 1
        elif sku in master:
            apply_lantern_existing(row, master[sku], is_weiyan=False)
            n_lantern += 1
        elif sku in accessories:
            apply_accessory_existing(row, accessories[sku])
            n_acc += 1
        elif sku in parts:
            apply_part_existing(row, parts[sku])
            n_part += 1
        elif sku.endswith("W") and (m := master_lookup(sku, master)):
            apply_lantern_existing(row, m, is_weiyan=False)
            n_lantern += 1

    shutil.copy(PRODUCTS, PRODUCTS.with_suffix(".csv.pre_source_sync_bak"))
    write_rows(PRODUCTS, fields, rows)

    story_rows: list[dict[str, str]] = []
    for row in rows:
        sku = row["BaseItemCode"].strip()
        m = weiyan.get(sku) or master.get(sku) or master_lookup(sku, master)
        story = build_story(m) if m else ""
        if not story:
            story = row.get("MarketingCopy") or row.get("LongDesc") or sku
        story_rows.append({"BaseItemCode": sku, "ProductStory": story})

    write_rows(STORIES, ["BaseItemCode", "ProductStory"], story_rows)

    print(f"products.csv: {len(fields)} columns (added only {NEW_COLUMNS})")
    print(f"Lanterns: {n_lantern}, Accessories: {n_acc}, Parts: {n_part}")
    feat = sum(1 for r in rows if (r.get("Feature1") or "").strip())
    print(f"Feature1 filled: {feat}/{len(rows)}")


if __name__ == "__main__":
    sync()
