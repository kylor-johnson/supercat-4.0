#!/usr/bin/env python3
"""Sync CS_OptionMapping_Rebuild import CSVs from June 2026 master source files.

Enforces Jordan's image rule: source URL exactly, blank source link = blank image.
Updates products.csv fields, options.csv ImageName, and rebuilds stories.csv.
"""
from __future__ import annotations

import csv
import re
import shutil
import urllib.parse
from pathlib import Path

BASE = Path(__file__).parent
JUNE = Path.home() / "Downloads/CS_Master_Product_List_June_2026_UPDATE"
MASTER = JUNE / "Master Sheet E+G-Table 1.csv"
WEIYAN = JUNE / "Weiyan LED-Table 1.csv"
ACCESSORIES = JUNE / "Accessories-Table 1.csv"
PARTS_SRC = JUNE / "Parts-Table 1.csv"
CORR_PATH = Path.home() / "Downloads/eCat Image Corrections.csv"

PRODUCTS = BASE / "products.csv"
OPTIONS = BASE / "options.csv"
STORIES = BASE / "stories.csv"
CHANGELOG = BASE / "SOURCE_SYNC_CHANGELOG.md"

MAX_IMAGES = 6
# eCat long_description / short_description are varchar(255); the importer only
# warns+truncates past 255. The old 50/15 caps were fabricated and produced
# mid-word garbage (e.g. ShortDesc "Handcrafted sol").
MAX_DESC = 255
NEW_COLUMNS = ["Feature1", "Feature2", "Feature3", "Feature4", "Feature5", "Feature6", "ProductTags"]

# Source-data corrections that must survive re-sync (the source files are wrong).
# Accessory NAME overrides keyed by accessory SKU.
ACCESSORY_NAME_OVERRIDES = {
    # Accessories tab mislabels HSI2 as "Frosted Hurricane Shade" (a duplicate of
    # HSI1). It is the Sanded shade per the master sheet (col CP) and llms.txt.
    "HSI2": "Sanded Hurricane Shade",
}

# Working Catsy JPG for the Contemporary Yoke (shared by all COY* rows).
COY_JPG_URL = "https://s3.us-west-2.amazonaws.com/catsy.962/_lg/4076155833/COY.jpg"

# Option ImageName overrides keyed by option Code. Empty string = force blank.
OPTION_IMAGE_OVERRIDES = {
    # "Brass" is not a real finish in the CopperSmith builder — it is the AOB base
    # material (no suffix), and AOB only accepts CLEAR. The eCat BRASS option is the
    # default-finish swatch for the AOB finish group (FIN002 = BRASS,CLEAR), but no
    # brass swatch image exists in any source file. Blank per Jordan's no-source rule.
    "BRASS": "",
    # COY12/COY13 carried a bare "COY.jpg" filename (no CDN trigger). Point them at
    # the same working Catsy JPG the other 12 COY* rows already use.
    "COY12": COY_JPG_URL,
    "COY13": COY_JPG_URL,
    # PFP image is 403 everywhere on Catsy (.jpg AND .png). No working asset exists,
    # so blank pending Jordan supplying one (see Jordan follow-up list).
    "PFPAU": "",
}

# Product ImageFileName overrides keyed by BaseItemCode. Empty string = force blank.
# A .png value here is converted to a plain "{basename}.jpg" + staged by build_jpg_images.py.
PRODUCT_IMAGE_OVERRIDES = {
    # Same dead PFP asset as option PFPAU — 403 on Catsy. Blank pending Jordan.
    "PFP36": "",
    # Master "Main Image File Link" 403s; this top-level Catsy JPG works (CDN path).
    "CS43E": "https://s3.us-west-2.amazonaws.com/catsy.962/CS43E.jpg",
    # Master link 403s; only a PNG exists — recover via convert-to-JPG + FTP.
    "TE20E": "https://s3.us-west-2.amazonaws.com/catsy.962/TE20E.png",
}

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

changes: list[tuple[str, str, str, str, str]] = []


def log(file: str, sku: str, field: str, before: str, after: str) -> None:
    if before != after:
        changes.append((file, sku, field, before, after))


def clean(val: str) -> str:
    v = (val or "").strip()
    return "" if v in ("----", "#", "$") else v


def clean_price(val: str) -> str:
    return clean(val).replace("$", "").replace(",", "")


def http_url(val: str) -> str:
    v = clean(val)
    return v if v.startswith("http") else ""


def _decoded_basename(url: str) -> str:
    base = url.split("?")[0].rstrip("/").rsplit("/", 1)[-1]
    return urllib.parse.unquote(base)


def _is_dirty_filename(name: str) -> bool:
    # eCat Product::VALID_IMAGE_REGEX = /\A[^/()]*\z/ forbids ( ) and /.
    # %, spaces and + additionally break the served image URL. Anything outside
    # [A-Za-z0-9._-] cannot be reliably served from the CDN/S3 path.
    return bool(re.search(r"[^A-Za-z0-9._-]", name))


def clean_image_filename(decoded_basename: str) -> str:
    """A safe ASCII .jpg filename for FTP/staging (no parens/space/%/+ etc.)."""
    stem, dot, _ext = decoded_basename.rpartition(".")
    if not dot:
        stem = decoded_basename
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", stem).strip("._-") or "img"
    return f"{stem}.jpg"


def cdn_needs_local_copy(url: str) -> str | None:
    """If a CDN URL cannot be served by eCat, return the clean plain filename it
    must be converted to and FTP'd under; otherwise None (clean .jpg = CDN path).

    Two failure classes, both verified against CdnImageSync / Product::VALID_IMAGE_REGEX:
      - .png source (wrong extension + non image/jpeg content-type), and
      - any filename with parens/space/%/+ etc. (regex-rejected or URL-breaking),
        e.g. Catsy "ES-63(FGPFPC8P2-10FT).jpg" -> "ES-63_FGPFPC8P2-10FT.jpg".
    """
    v = (url or "").strip()
    if not v.lower().startswith("http"):
        return None
    dec = _decoded_basename(v)
    if dec.lower().endswith(".png") or _is_dirty_filename(dec):
        return clean_image_filename(dec)
    return None


def to_csv_ref(url: str) -> str:
    """Convert one source image link to the value stored in the CSV.

    Clean .jpg/.jpeg https URLs pass through unchanged (eCat CDN-pulls them). Any
    URL eCat can't serve (PNG, or a filename with parens/space/%/+) is rewritten to
    a clean plain "{name}.jpg" filename that build_jpg_images.py converts + FTPs.
    """
    v = clean(url)
    if not v:
        return ""
    if not v.lower().startswith("http"):
        return v
    target = cdn_needs_local_copy(v)
    return target if target else v


def convert_image_field(value: str) -> str:
    """Apply to_csv_ref to every element of a (possibly comma-joined) image field."""
    return ",".join(
        ref for ref in (to_csv_ref(part) for part in (value or "").split(",")) if ref
    )


def load_sheet(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
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
    with ACCESSORIES.open(newline="", encoding="utf-8-sig") as f:
        next(f)
        for row in csv.DictReader(f):
            sku = (row.get("Accessory SKU") or "").strip()
            if sku:
                out[sku] = row
    return out


def load_parts() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with PARTS_SRC.open(newline="", encoding="utf-8-sig") as f:
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


def load_corrections() -> dict[str, str]:
    corr: dict[str, str] = {}
    with CORR_PATH.open(encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) >= 2 and row[0].strip() and row[0].strip() not in (
                "Lantern + Product SKUs",
                "Accessory SKUs",
            ):
                corr[row[0].strip()] = clean(row[1])
    return corr


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
    # ProductStory = Marketing Copy (BU) + Long Description (BT) + Feature bullets.
    # Jordan's BT "Long Description" (collection romance/history) belongs in the
    # detail-page story, NOT in the LongDesc catalog title.
    blocks: list[str] = []
    mc = clean(m.get("Marketing Copy", ""))
    ld = clean(m.get("Long Description", ""))
    if mc:
        blocks.append(mc)
    if ld:
        blocks.append(ld)
    bullets = [clean(m.get(f"Feature {i}", "")) for i in range(1, 7)]
    bullets = [b for b in bullets if b]
    if bullets:
        blocks.append("\n".join(f"• {b}" for b in bullets))
    return "\n\n".join(blocks).strip()


def expected_product_image(
    sku: str,
    master: dict,
    weiyan: dict,
    accessories: dict,
    parts: dict,
    corrections: dict,
) -> str | None:
    if sku in corrections:
        return corrections[sku]
    if sku in accessories:
        return http_url(accessories[sku].get("Accessory Image Link", ""))
    if sku in weiyan:
        urls = collect_image_urls(weiyan[sku])
        return ",".join(urls) if urls else ""
    if sku in master:
        urls = collect_image_urls(master[sku])
        return ",".join(urls) if urls else ""
    m = master_lookup(sku, master)
    if m:
        urls = collect_image_urls(m)
        return ",".join(urls) if urls else ""
    if sku in parts:
        return http_url(parts[sku].get("image", ""))
    return None


def expected_option_image(code: str, accessories: dict, corrections: dict) -> str | None:
    if code in corrections:
        return corrections[code]
    if code in accessories:
        return http_url(accessories[code].get("Accessory Image Link", ""))
    return None


def apply_lantern(row: dict[str, str], m: dict[str, str], *, is_weiyan: bool) -> None:
    sku = row["BaseItemCode"]
    retailer = clean(m.get("Retailer Product Name", ""))
    short_src = clean(m.get("Short Description", ""))
    # LongDesc = full Retailer Product Name (catalog title). ShortDesc = full
    # source "Short Description" (subtitle under SKU). Both capped at eCat's 255.
    new_long = (retailer or short_src or sku)[:MAX_DESC]
    new_short = (short_src or retailer or sku)[:MAX_DESC]
    log("products.csv", sku, "LongDesc", row.get("LongDesc", ""), new_long)
    log("products.csv", sku, "ShortDesc", row.get("ShortDesc", ""), new_short)
    row["LongDesc"] = new_long
    row["ShortDesc"] = new_short

    row["materials"] = clean(m.get("Material", ""))
    row["dimensions"] = fmt_dims(m)
    sw = clean(m.get("Shipping Weight (lbs)", "")) or clean(m.get("Weight", ""))
    if sw:
        row["shipweight"] = sw

    upc = clean(m.get("UPC", "")) or clean(m.get("UPC/GTIN", ""))
    if upc:
        row["UPCValue"] = upc

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

    for i in range(1, 7):
        row[f"Feature{i}"] = clean(m.get(f"Feature {i}", ""))
    row["ProductTags"] = clean(m.get("Product Tags", ""))


def apply_accessory(row: dict[str, str], acc: dict[str, str]) -> None:
    sku = row["BaseItemCode"]
    name = ACCESSORY_NAME_OVERRIDES.get(sku) or clean(acc.get("Accessory Name", ""))
    if name:
        new_long, new_short = name[:MAX_DESC], name[:MAX_DESC]
        log("products.csv", sku, "LongDesc", row.get("LongDesc", ""), new_long)
        log("products.csv", sku, "ShortDesc", row.get("ShortDesc", ""), new_short)
        row["LongDesc"] = new_long
        row["ShortDesc"] = new_short
    gtin = clean(acc.get("Accessory GTIN", ""))
    if gtin:
        row["UPCValue"] = gtin
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


def apply_part(row: dict[str, str], part: dict[str, str]) -> None:
    sku = row["BaseItemCode"]
    name = part.get("name", "")
    if name:
        row["LongDesc"] = name[:MAX_DESC]
        row["ShortDesc"] = name[:MAX_DESC]
    if part.get("gtin"):
        row["UPCValue"] = part["gtin"]
    if part.get("net"):
        row["NetPrice"] = part["net"]
    if part.get("map"):
        row["Price_MAP"] = part["map"]
    if part.get("msrp"):
        row["Price_MSRP"] = part["msrp"]


def write_rows(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def write_changelog() -> None:
    lines = [
        "# Source Sync Change Log",
        "",
        f"Total changes: {len(changes)}",
        "",
        "| File | SKU/Code | Field | Before | After |",
        "|------|----------|-------|--------|-------|",
    ]
    for file, sku, field, before, after in changes[:500]:
        b = (before[:60] + "…") if len(before) > 60 else before
        a = (after[:60] + "…") if len(after) > 60 else after
        lines.append(f"| {file} | `{sku}` | {field} | {b!r} | {a!r} |")
    if len(changes) > 500:
        lines.append(f"\n… and {len(changes) - 500} more rows")
    CHANGELOG.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sync() -> None:
    global changes
    changes = []

    master = load_sheet(MASTER)
    weiyan = load_sheet(WEIYAN)
    accessories = load_accessories()
    parts = load_parts()
    corrections = load_corrections()

    shutil.copy(PRODUCTS, PRODUCTS.with_suffix(".csv.pre_june_sync_bak"))
    shutil.copy(OPTIONS, OPTIONS.with_suffix(".csv.pre_june_sync_bak"))

    with PRODUCTS.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        prod_rows = list(reader)

    for col in NEW_COLUMNS:
        if col not in fields:
            fields.append(col)

    n_lantern = n_acc = n_part = 0
    for row in prod_rows:
        sku = row["BaseItemCode"].strip()
        if sku in weiyan:
            apply_lantern(row, weiyan[sku], is_weiyan=True)
            n_lantern += 1
        elif sku in master:
            apply_lantern(row, master[sku], is_weiyan=False)
            n_lantern += 1
        elif sku in accessories:
            apply_accessory(row, accessories[sku])
            n_acc += 1
        elif sku in parts:
            apply_part(row, parts[sku])
            n_part += 1
        elif sku.endswith("W") and (m := master_lookup(sku, master)):
            apply_lantern(row, m, is_weiyan=False)
            n_lantern += 1

        if sku in PRODUCT_IMAGE_OVERRIDES:
            exp_img = PRODUCT_IMAGE_OVERRIDES[sku]
        else:
            exp_img = expected_product_image(sku, master, weiyan, accessories, parts, corrections)
        if exp_img is not None:
            exp_img = convert_image_field(exp_img)
            before = (row.get("ImageFileName") or "").strip()
            log("products.csv", sku, "ImageFileName", before, exp_img)
            row["ImageFileName"] = exp_img

    write_rows(PRODUCTS, fields, prod_rows)

    with OPTIONS.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        opt_fields = list(reader.fieldnames or [])
        opt_rows = list(reader)

    n_opt_img = 0
    for row in opt_rows:
        code = row["Code"].strip()
        if code in OPTION_IMAGE_OVERRIDES:
            exp = OPTION_IMAGE_OVERRIDES[code]
        else:
            exp = expected_option_image(code, accessories, corrections)
        if exp is not None:
            exp = to_csv_ref(exp)
            before = (row.get("ImageName") or "").strip()
            log("options.csv", code, "ImageName", before, exp)
            row["ImageName"] = exp
            n_opt_img += 1

    write_rows(OPTIONS, opt_fields, opt_rows)

    story_rows: list[dict[str, str]] = []
    for row in prod_rows:
        sku = row["BaseItemCode"].strip()
        m = weiyan.get(sku) or master.get(sku) or master_lookup(sku, master)
        story = build_story(m) if m else ""
        if not story:
            story = row.get("MarketingCopy") or row.get("LongDesc") or sku
        story_rows.append({"BaseItemCode": sku, "ProductStory": story})

    write_rows(STORIES, ["BaseItemCode", "ProductStory"], story_rows)
    write_changelog()

    print(f"products.csv: lanterns={n_lantern}, accessories={n_acc}, parts={n_part}")
    print(f"options.csv: {n_opt_img} ImageName rows synced from source")
    print(f"Total logged changes: {len(changes)}")
    print(f"Changelog: {CHANGELOG.name}")


if __name__ == "__main__":
    sync()
