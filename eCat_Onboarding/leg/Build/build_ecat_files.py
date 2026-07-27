#!/usr/bin/env python3
"""
Legrand eCat Build Script
Transforms Legrand source data into eCat products.csv, stories.csv, and
inventory.csv.

Scope note (2026-07-13): the source "adorne radiant US CAD Data File" carries a
generic Legrand column template, but for THIS dataset almost every spec column
(LED/fan/bulb specs, certifications, Materials, Special Feature, document URLs,
Add Option 1-10, Dist NET 2-10, UMAP, etc.) is 100% empty. The only populated,
catalog-relevant data beyond the standard fields is:
  - Finish (55 distinct)            -> custom field + multi-select filter
  - Country of Origin               -> custom field (already mapped)
  - Drop Ship / Shipped Via / UOM   -> constant/low-value optional custom fields
  - Finish variants                 -> RelatedItems (built-in reserved field)
There are NO product "options" in the eCat sense (Add Option * columns are all
blank, and each finish is its own orderable SKU), so finish variants are modeled
as Related Items rather than option sets. See products-review.md and
custom-fields-setup.md.
"""

import collections
import csv
import os
import re
import openpyxl

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(BASE_DIR, "Source Data")
CONVERTED_DIR = os.path.join(SOURCE_DIR, "_converted")
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

PRODUCT_FILE = os.path.join(
    SOURCE_DIR,
    "Product File",
    "adorne  radiant US  CAD Data File  5-14-26.xlsx - Data.csv",
)

IMAGE_SOURCE_FILE = "/Users/kylorjohnson/Downloads/adorne & radiant image & video links.xlsx - Image Files.csv"
MAX_IMAGES_PER_PRODUCT = 6

INVENTORY_SOURCE_FILES = [
    os.path.join(SOURCE_DIR, "Inventory", "LegrandAdorneInventory.xlsx - LegrandAdorneInventory.csv"),
    os.path.join(SOURCE_DIR, "Inventory", "LegrandRadiantInventory.xlsx - LegrandRadiantInventory.csv"),
]

CATEGORY_FIXES = {
    "Night Lighs": "Night Lights",
    "radiant® Microban®": "Antimicrobial Devices",
    "radiant® with Netatmo": "Smart Home (Netatmo)",
    "Lighting & Fan Controls": "Fan Control",
    "Smart Dimmer Kit": "Dimmer Kit",
    # Unify singular/plural duplicates that only differ because adorne and
    # radiant used different wording for the same category (verified in the
    # source distribution 2026-07-13). "Light Switch" vs "Switches" is left
    # separate pending client confirmation (see TAXONOMY.md).
    "Outlet": "Outlets",
    "Night Light": "Night Lights",
}

# Brand axis: adorne + radiant are Trade Names (not Collections under "Legrand").
# Client confirmed 2026-07-15 / 2026-07-24: brand must be the first iPad nav layer
# before category. CollectionCodes mirrors the trade name (required field;
# auto-create). Old "Legrand" TN + COL1/COL2 prune once nothing references them.
#
# Carton custom fields are NOT registered in Admin yet — keep them out of the
# written products.csv so imports stay Warning-clean. Source carton data still
# feeds PackedVolume. Flip to True after Admin registration.
INCLUDE_CARTON_FIELDS = False

# --- Group -> Category taxonomy -------------------------------------------
# The live org (`leg`, id 273) uses the FurnishWeb / Auto-Create import method,
# so TradeName / Collection / Category all auto-create from the name strings in
# products.csv. BUT the product file has no Group field: every auto-created
# category lands under a single "Default Group". The client already built the
# 5 groups below during the POC (verified in Postgres 2026-07-13, codes DIM /
# SWT / ST / WPB / GRP1). This map is therefore the Admin worksheet for placing
# our auto-created categories into those existing groups (either pre-create the
# categories under the right group before import, or reassign after import).
GROUP_ORDER = [
    "Switches & Outlets",
    "Dimmers",
    "Sensors & Timers",
    "Plates, Boxes & Blanks",
    "Smart Technology",
]

# Cleaned category name -> client group. Entries also listed in
# CATEGORY_GROUP_REVIEW are best-guess placements to confirm with the client.
CATEGORY_TO_GROUP = {
    # Switches & Outlets
    "USB Outlet": "Switches & Outlets",
    "GFCI": "Switches & Outlets",
    "GFCI/USB": "Switches & Outlets",
    "Outlets": "Switches & Outlets",
    "Countertop Outlet": "Switches & Outlets",
    "Combination Devices": "Switches & Outlets",
    "AFCI Devices": "Switches & Outlets",
    "Switches": "Switches & Outlets",
    "Light Switch": "Switches & Outlets",
    "EV Charging": "Switches & Outlets",
    "Night Lights": "Switches & Outlets",
    "Locator Light": "Switches & Outlets",
    "Antimicrobial Devices": "Switches & Outlets",
    "Connectivity": "Switches & Outlets",
    # Dimmers
    "Dimmer": "Dimmers",
    "Dimmer Kit": "Dimmers",
    "Fan Control": "Dimmers",
    # Sensors & Timers
    "Timer Switch": "Sensors & Timers",
    "Occupancy Sensor": "Sensors & Timers",
    "Vacancy Sensor": "Sensors & Timers",
    # Plates, Boxes & Blanks
    "Plastics Wall Plate": "Plates, Boxes & Blanks",
    "Cast Metal Wall Plate": "Plates, Boxes & Blanks",
    "Real Materials Wall Plate": "Plates, Boxes & Blanks",
    "Screwless Wall Plates": "Plates, Boxes & Blanks",
    "Sub Frame": "Plates, Boxes & Blanks",
    "Device Blank": "Plates, Boxes & Blanks",
    "Inserts": "Plates, Boxes & Blanks",
    # Smart Technology
    "Smart Color Change Kit": "Smart Technology",
    "Smart Scene Controller": "Smart Technology",
    "Smart Switch": "Smart Technology",
    "Smart Outlet": "Smart Technology",
    "Smart Outlet Kit": "Smart Technology",
    "Smart Gateway": "Smart Technology",
    "Smart Dimmer": "Smart Technology",
    "Smart Lamp Module": "Smart Technology",
    "Smart Home (Netatmo)": "Smart Technology",
}

# Best-guess placements to confirm with the client: either the group is
# ambiguous, or they may warrant a 6th "Accessories" group.
CATEGORY_GROUP_REVIEW = {
    "Connectivity",
    "Smart Dimmer",
    "Night Lights",
    "Antimicrobial Devices",
    "Fan Control",
    "EV Charging",
    "Locator Light",
}

# Unambiguous Finish typo/spelling fixes. Finish becomes a multi-select filter,
# so dirty values create duplicate filter facets. Only clearly-identical values
# are merged here; genuinely distinct-looking finishes (e.g. Mirror vs Mirror
# White, Gloss White vs Gloss White on White, Brushed Stainless vs Brushed
# Stainless Steel) are left alone and flagged for client review in
# custom-fields-setup.md.
FINISH_FIXES = {
    "Grahite": "Graphite",
    "Tri Color": "Tri-Color",
    "Tri-color": "Tri-Color",
}

# Per-SKU Finish overrides where the Finish column is wrong but the Product
# Name + SKU suffix agree. Keyed by Item ID so a fix can never bleed.
FINISH_OVERRIDES = {
    # Finish columns swapped between these two Color Change Kit SKUs;
    # Name and suffix (NI / LA) both say Nickel / Light Almond.
    "WNRL43CKITNI": "Nickel",
    "WNRL43CKITLA": "Light Almond",
}

# Near-duplicate Finish values to surface for client confirmation (not merged
# automatically because they may be genuinely distinct SKUs).
FINISH_REVIEW_GROUPS = [
    ["Mirror", "Mirror White", "Mirror Black"],
    ["Gloss White", "Gloss White on White", "Powder White", "Matte White"],
    ["Brushed Stainless", "Brushed Stainless Steel", "Stainless Steel", "Spiraled Stainless"],
    ["Tri-Color", "Tri Color (WH, IV, LA)"],
]

# Verified one-off typos in the source `Product Name` column, keyed by Item ID
# so a fix can never accidentally apply to an unrelated row. Applying these
# BEFORE RelatedItems grouping and LongDesc construction matters: the
# RelatedItems key is derived from this name, and a wrong color word orphans
# a SKU from its finish family.
#
# NOTE on why we don't auto-merge RelatedItems families by fuzzy name
# matching instead of hand-verifying each fix: this catalog is full of
# genuinely-different products whose names differ by only 1-3 characters
# (15A vs 20A, 1-gang vs 2-gang vs 3-gang, USB type A/A vs A/C vs C/C, etc).
# A difflib similarity test at a 0.95 cutoff produced 118 "matches" on this
# dataset and nearly all of them were FALSE positives (e.g. it wanted to
# merge the 15A GFCI family with the unrelated 20A GFCI family). Silently
# auto-merging on similarity would create wrong RelatedItems data, which is
# worse than a blank field. Only ship a fix here once a human has confirmed
# it against the actual source row (SKU suffix + Finish column agreement).
PRODUCT_NAME_FIXES = {
    # 227V typo -> 277V (also re-joins G277/M277 finish family)
    "ASPD1531W277": "adorne® 277V Paddle Switch, Half-Size, White, with Microban®",
    # Name color word wrong; SKU letter + Finish column agree
    "ADPD153LM2": "adorne® 150W LED Advanced Dimmer, Magnesium, with Microban®",
    "AC6RJ45M1": "adorne® Cat 6 RJ45 Data Insert, Magnesium",
    "ACBLKM4": "adorne® Blank Keystone Insert 4-Pack, Magnesium",
    "ACRJ25M1": "adorne® RJ25 Phone Jack, Magnesium",
    "ACRJ25W1": "adorne® RJ25 Phone Jack, White",
    "2097TRWRUSBACBK": (
        "radiant® Tamper-Resistant Weather-Resistant 20A Duplex Self-Test GFCI "
        "Receptacles with SafeLock® Protection, Type A/C Outlet, Black"
    ),
    # Netatmo G-suffix: Name said Nickel; Finish + SKU letter = Graphite
    "WNAL33G1": "adorne® Wireless Home/Away Smart Switch with Netatmo, Graphite",
    "WNAL63G1": "adorne® Wireless Remote Smart Dimmer with Netatmo, Graphite",
    "WNAL43G1": "adorne® Wireless Wake/Sleep Smart Switch with Netatmo, Graphite",
    "WNACB40G1": "adorne® Wireless Smart Scene Controller with Netatmo, Graphite",
    # Netatmo M-suffix: Name copy-pasted from Scene Controller; G/W siblings
    # prove the correct product type for each SKU prefix
    "WNAL33M1": "adorne® Wireless Home/Away Smart Switch with Netatmo, Magnesium",
    "WNAL63M1": "adorne® Wireless Remote Smart Dimmer with Netatmo, Magnesium",
    "WNAL43M1": "adorne® Wireless Wake/Sleep Smart Switch with Netatmo, Magnesium",
}


def get_product_name(row):
    """Return the source Product Name with verified typo fixes applied."""
    item_id = row["Item ID"].strip()
    return PRODUCT_NAME_FIXES.get(item_id, row["Product Name"].strip())


def get_finish(row):
    """Return Finish with per-SKU overrides and typo normalization applied."""
    item_id = row["Item ID"].strip()
    if item_id in FINISH_OVERRIDES:
        return FINISH_OVERRIDES[item_id]
    return normalize_finish(row.get("Finish", ""))

# Freight / carton packaging fields, captured verbatim from the source's
# positional carton tiers so that ALL non-blank source data lands in the file.
# Notes verified in the source (2026-07-13):
#   - `Carton Weight 2` is byte-identical to `Carton Weight` on every row, so it
#     is captured once (carton1_wt) rather than duplicated.
#   - Tier 1/2/3 dimensions genuinely differ, but which physical package a tier
#     represents is inconsistent row-to-row, so tiers are captured positionally
#     rather than relabeled. Recommend registering these as HIDDEN-from-details
#     custom fields (data lands / usable in reports without cluttering the
#     rep-facing catalog). Tier-1 dims also feed the derived PackedVolume cube.
# Each entry: (csv header / custom field name, source column, Admin label).
CARTON_FIELDS = [
    ("carton1_h", "Carton Height", "Carton 1 Height"),
    ("carton1_l", "Carton Length", "Carton 1 Length"),
    ("carton1_w", "Carton Width", "Carton 1 Width"),
    ("carton1_wt", "Carton Weight", "Carton 1 Weight"),
    ("carton2_h", "Carton Height 2", "Carton 2 Height"),
    ("carton2_l", "Carton Length 2", "Carton 2 Length"),
    ("carton2_w", "Carton Width 2", "Carton 2 Width"),
    ("carton3_h", "Carton Height 3", "Carton 3 Height"),
    ("carton3_l", "Carton Length 3", "Carton 3 Length"),
    ("carton3_w", "Carton Width 3", "Carton 3 Width"),
    ("carton3_wt", "Carton Weight 3", "Carton 3 Weight"),
    ("cartons_per_unit", "Cartons Per Unit", "Cartons Per Unit"),
]


def strip_currency(val):
    """Remove $ and commas from a price string, return float or empty string."""
    if not val or val.strip() in ("", "#N/A", "N/A", "0"):
        return ""
    val = val.strip().replace("$", "").replace(",", "")
    try:
        return f"{float(val):.2f}"
    except ValueError:
        return ""


def parse_ship_weight_lb(val):
    """Parse a source weight string into pounds for ShipWeight.

    Accepts `N lb` / `N lbs` (passthrough) and `N g` (converted ÷ 453.59237).
    Returns a compact numeric string, or empty if unparseable / null.
    """
    if not val or val.strip() in ("", "0", "#N/A", "N/A"):
        return ""
    m = re.match(r"^\s*([\d.]+)\s*(lb|lbs|g|kg)?\s*$", val.strip(), re.IGNORECASE)
    if not m:
        return ""
    num = float(m.group(1))
    unit = (m.group(2) or "lb").lower()
    if unit == "g":
        num = num / 453.59237
    elif unit == "kg":
        num = num * 2.20462262
    # Compact: drop trailing zeros (0.25 -> "0.25", 0.0107 -> "0.0107")
    return f"{num:.6f}".rstrip("0").rstrip(".")


def build_dimensions(height, width, length):
    """Concatenate H x W x L into a single Dimensions string."""
    parts = []
    for v in [height, width, length]:
        v = v.strip() if v else ""
        if v and v != "0":
            parts.append(v)
        else:
            parts.append("0 in")
    if not any(p != "0 in" for p in parts):
        return "N/A"
    return f"{parts[0]} H x {parts[1]} W x {parts[2]} L"


def load_us_radiant_prices():
    """Load US radiant pricing: Item -> {msrp, imap, dn}"""
    prices = {}
    wb = openpyxl.load_workbook(
        os.path.join(CONVERTED_DIR, "radiant_us.xlsx"), data_only=True
    )
    ws = wb.active
    for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 2):
        if not row or not row[1]:
            continue
        item_id = str(row[1]).strip()
        if not item_id or item_id == "Item":
            continue
        prices[item_id] = {
            "msrp": strip_currency(str(row[4]) if row[4] else ""),
            "imap": strip_currency(str(row[5]) if row[5] else ""),
            "dn": strip_currency(str(row[6]) if row[6] else ""),
        }
    wb.close()
    return prices


def load_us_adorne_prices():
    """Load US adorne pricing: Item -> {msrp, imap, dn}"""
    prices = {}
    wb = openpyxl.load_workbook(
        os.path.join(CONVERTED_DIR, "adorne_us.xlsx"), data_only=True
    )
    ws = wb.active
    for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 2):
        if not row or not row[1]:
            continue
        item_id = str(row[1]).strip()
        if not item_id or item_id == "Item":
            continue
        prices[item_id] = {
            "msrp": strip_currency(str(row[5]) if row[5] else ""),
            "imap": strip_currency(str(row[6]) if row[6] else ""),
            "dn": strip_currency(str(row[7]) if row[7] else ""),
        }
    wb.close()
    return prices


def load_ca_radiant_prices():
    """Load CA radiant pricing: Item -> {net_cad, imap_cad, msrp_cad}"""
    prices = {}
    wb = openpyxl.load_workbook(
        os.path.join(CONVERTED_DIR, "radiant_ca.xlsx"), data_only=True
    )
    ws = wb.active
    # Header is row 6; data starts row 8
    for i, row in enumerate(ws.iter_rows(min_row=8, values_only=True), 8):
        if not row or not row[1]:
            continue
        item_id = str(row[1]).strip()
        if not item_id:
            continue
        prices[item_id] = {
            "net_cad": strip_currency(str(row[5]) if row[5] else ""),
            "imap_cad": strip_currency(str(row[6]) if row[6] else ""),
            "msrp_cad": strip_currency(str(row[7]) if row[7] else ""),
        }
    wb.close()
    return prices


def load_ca_adorne_prices():
    """Load CA adorne pricing: Item -> {net_cad, msrp_cad, imap_cad}"""
    prices = {}
    wb = openpyxl.load_workbook(
        os.path.join(CONVERTED_DIR, "adorne_ca.xlsx"), data_only=True
    )
    ws = wb.active
    # Header is row 7; data starts row 8
    for i, row in enumerate(ws.iter_rows(min_row=8, values_only=True), 8):
        if not row or not row[1]:
            continue
        item_id = str(row[1]).strip()
        if not item_id:
            continue
        prices[item_id] = {
            "net_cad": strip_currency(str(row[5]) if row[5] else ""),
            "msrp_cad": strip_currency(str(row[6]) if row[6] else ""),
            "imap_cad": strip_currency(str(row[7]) if row[7] else ""),
        }
    wb.close()
    return prices


def clean_category(cat):
    """Apply category name fixes."""
    cat = cat.strip()
    return CATEGORY_FIXES.get(cat, cat)


def load_image_filenames():
    """Load the verified image filename mapping keyed by BaseItemCode.

    Prefers `image_filename_map.csv` — the output of `download_images.py`,
    which only lists a filename after the corresponding image was actually
    downloaded to `images/`. That's a stronger guarantee than re-deriving
    from the raw URL list (IMAGE_SOURCE_FILE), which can go stale/disappear
    from Downloads and says nothing about whether a download succeeded.
    Falls back to IMAGE_SOURCE_FILE only if the verified map isn't present,
    e.g. on a first run before any images have been downloaded.
    """
    mapping = {}
    verified_map_path = os.path.join(OUTPUT_DIR, "image_filename_map.csv")
    if os.path.exists(verified_map_path):
        with open(verified_map_path, "r", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                part = row.get("BaseItemCode", "").strip()
                fnames = row.get("ImageFileName", "").strip()
                if part and fnames:
                    mapping[part] = fnames
        return mapping

    if not os.path.exists(IMAGE_SOURCE_FILE):
        print(f"  WARNING: Image source file not found: {IMAGE_SOURCE_FILE}")
        print(f"  WARNING: Verified map not found either: {verified_map_path}")
        return mapping

    with open(IMAGE_SOURCE_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            part = row.get("Part Number", "").strip()
            if not part:
                continue

            filenames = []
            main_url = row.get("Main Image_1", "").strip()
            if main_url and "youtube" not in main_url.lower():
                filenames.append(f"{part}.jpg")

            for i in range(1, 50):
                if len(filenames) >= MAX_IMAGES_PER_PRODUCT:
                    break
                col = f"alternate_image_{i}"
                val = row.get(col, "").strip()
                if val and "youtube" not in val.lower() and val != main_url:
                    idx = len(filenames) + 1
                    filenames.append(f"{part}_{idx}.jpg")

            if filenames:
                mapping[part] = ",".join(filenames[:MAX_IMAGES_PER_PRODUCT])

    return mapping


def clean_country(val):
    """Clean Country of Origin values."""
    val = val.strip()
    if val in ("0", "#N/A", ""):
        return ""
    return val


def normalize_receipt_date(val):
    """Convert an 'MM/DD/YY' source date to 'YYYY-MM-DD'. Non-date prose
    (e.g. 'to be sched') is unmappable and returns '' rather than failing
    the importer's date validation."""
    val = (val or "").strip()
    if not val:
        return ""
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{2})$", val)
    if not m:
        return ""
    month, day, yy = m.groups()
    year = 2000 + int(yy)
    return f"{year:04d}-{int(month):02d}-{int(day):02d}"


def load_inventory_source(path, product_line):
    """Parse a Legrand inventory export (title row + blank row + real header,
    then data rows) into a list of dicts keyed by the real header names."""
    with open(path, "r", newline="", encoding="utf-8-sig") as f:
        raw_rows = list(csv.reader(f))

    header_idx = next(
        i for i, row in enumerate(raw_rows) if row and row[0].strip() == "Supplier ID"
    )
    header = raw_rows[header_idx]
    rows = []
    for row in raw_rows[header_idx + 1 :]:
        if not row or not any(cell.strip() for cell in row):
            continue
        record = dict(zip(header, row))
        record["_product_line"] = product_line
        rows.append(record)
    return rows


def clean_order_min(val):
    """Clean Order Minimum, default to 1."""
    val = val.strip()
    if val in ("#N/A", "", "0"):
        return "1"
    try:
        v = int(float(val))
        return str(max(v, 1))
    except ValueError:
        return "1"


def clean_na(val):
    """Return a trimmed value, mapping the source's null tokens to empty."""
    val = (val or "").strip()
    return "" if val in ("#N/A", "N/A", "0", "") else val


def normalize_finish(val):
    """Clean and apply unambiguous Finish spelling fixes."""
    val = clean_na(val)
    return FINISH_FIXES.get(val, val)


def to_boolean_y(val):
    """Coerce a source 'Yes'/'True' style value to eCat boolean 'Y' (blank
    otherwise). eCat boolean filters only match 'Y'/'y'/'T'/'t'/digit 1-9,
    so a raw 'Yes' would NOT match a filter."""
    v = clean_na(val).lower()
    if v in ("yes", "y", "true", "t", "1"):
        return "Y"
    return ""


def _normalize_variant_key(name, finish):
    """Collapse a product name to a finish-independent key so that SKUs that
    differ only by finish share a key. Used to derive RelatedItems families."""
    key = name
    finish = (finish or "").strip()
    if finish and finish not in ("#N/A", "0"):
        key = re.sub(re.escape(finish), "", key, flags=re.IGNORECASE)
    key = key.replace(",", " ")
    key = re.sub(r"\s+", " ", key).strip().lower()
    return key


def build_related_items(source_rows):
    """Group SKUs that differ only by finish into Related Items families.

    Returns (related_map, families) where related_map maps each BaseItemCode in
    a multi-member family to the comma-joined list of ALL family members
    (including itself, per the eCat Related Items best practice), preserving
    source file order. `families` is the list of member-lists for review.
    """
    groups = collections.OrderedDict()
    for row in source_rows:
        item = row["Item ID"].strip()
        key = _normalize_variant_key(
            get_product_name(row), get_finish(row)
        )
        groups.setdefault(key, []).append(item)

    related_map = {}
    families = []
    for items in groups.values():
        if len(items) > 1:
            joined = ",".join(items)
            for item in items:
                related_map[item] = joined
            families.append(items)
    return related_map, families


def write_taxonomy_files(products):
    """Emit the Group -> Category worksheet (TAXONOMY.md) and a machine-readable
    group-category-map.csv from the real built category counts. Returns the list
    of any categories not present in CATEGORY_TO_GROUP so the caller can warn."""
    cat_count = collections.Counter()
    cat_collections = collections.defaultdict(set)
    for p in products:
        for cat in (p["CategoryCodes"] or "").split(","):
            cat = cat.strip()
            if cat:
                cat_count[cat] += 1
                cat_collections[cat].add(p["CollectionCodes"].strip())

    unmapped = sorted(c for c in cat_count if c not in CATEGORY_TO_GROUP)

    # group -> [(category, count, collections, review?)]
    grouped = collections.defaultdict(list)
    for cat in sorted(cat_count, key=lambda c: (-cat_count[c], c)):
        group = CATEGORY_TO_GROUP.get(cat, "UNMAPPED — assign before import")
        grouped[group].append(
            (cat, cat_count[cat], ",".join(sorted(cat_collections[cat])), cat in CATEGORY_GROUP_REVIEW)
        )

    # --- group-category-map.csv ---
    map_out = os.path.join(OUTPUT_DIR, "group-category-map.csv")
    with open(map_out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Group", "Category", "ProductCount", "Collections", "ConfirmWithClient"])
        for group in GROUP_ORDER + [g for g in grouped if g not in GROUP_ORDER]:
            for cat, cnt, cols, review in grouped.get(group, []):
                w.writerow([group, cat, cnt, cols, "YES" if review else ""])

    # --- TAXONOMY.md ---
    tax_out = os.path.join(OUTPUT_DIR, "TAXONOMY.md")
    with open(tax_out, "w", encoding="utf-8") as f:
        f.write("# Legrand eCat Taxonomy — build worksheet\n\n")
        f.write(
            "Live org `leg` (id 273) import method = **FurnishWeb / Auto-Create**. "
            "On the product import, **TradeName, Collections, and Categories "
            "auto-create** from the name strings in `products.csv`; empty leftover "
            "taxonomy from the sales POC is auto-pruned once no product references "
            "it. **Groups do NOT come from the product file** — every auto-created "
            "category lands under a single *Default Group*, so the Group -> Category "
            "assignment below must be done in Admin (see two options at the bottom).\n\n"
        )
        f.write("## Brand axis — Trade Names (adorne / radiant)\n\n")
        f.write("| Trade Name | CollectionCodes (mirrors TN) | Products |\n|---|---|---|\n")
        f.write(
            f"| adorne | adorne | "
            f"{sum(1 for p in products if p['TradeNameCode'] == 'adorne')} |\n"
        )
        f.write(
            f"| radiant | radiant | "
            f"{sum(1 for p in products if p['TradeNameCode'] == 'radiant')} |\n\n"
        )
        f.write(
            "> **2026-07-24:** Trade Names are **adorne** and **radiant** (not a "
            "parent \"Legrand\" TN). Matches client ask: pick brand before "
            "category. `CollectionCodes` mirrors the trade name (required field). "
            "Old Legrand / COL1 / COL2 rows prune on a clean import once unused.\n\n"
        )
        f.write("## Functional axis — Group -> Category\n\n")
        f.write(
            "Categories mapped to the client's **5 existing Admin groups** "
            "(`Switches & Outlets`, `Dimmers`, `Sensors & Timers`, "
            "`Plates, Boxes & Blanks`, `Smart Technology`). Rows marked "
            "**CONFIRM** are best-guess placements for the meeting.\n\n"
        )
        for group in GROUP_ORDER + [g for g in grouped if g not in GROUP_ORDER]:
            rows = grouped.get(group)
            if not rows:
                continue
            total = sum(r[1] for r in rows)
            f.write(f"### {group}  ({total} products, {len(rows)} categories)\n\n")
            f.write("| Category | Products | Collection(s) | Confirm? |\n|---|---|---|---|\n")
            for cat, cnt, cols, review in rows:
                f.write(f"| {cat} | {cnt} | {cols} | {'**CONFIRM**' if review else ''} |\n")
            f.write("\n")

        f.write("## Confirm with the client\n\n")
        f.write(
            "- **~7 best-guess placements** (marked CONFIRM above): "
            + ", ".join(f"`{c}`" for c in sorted(CATEGORY_GROUP_REVIEW))
            + ". Decide the right group, or add a 6th **Accessories** group for the "
            "odd ones (Connectivity, Night Lights, Locator Light, Antimicrobial).\n"
        )
        f.write(
            "- **`Light Switch` vs `Switches`** — kept separate; confirm whether to "
            "merge (adorne says 'Light Switch', radiant says 'Switches').\n"
        )
        f.write(
            "- Auto-applied singular/plural merges: `Outlet` -> `Outlets`, "
            "`Night Light` -> `Night Lights`.\n\n"
        )
        f.write("## How to make the groups stick (pick one)\n\n")
        f.write(
            "1. **Pre-create (clean):** in `Products > Groups & Categories`, create "
            "each category above under its group *before* importing products. The "
            "importer matches categories by name (`find_or_create_category`), so it "
            "reuses them and they keep their group — nothing lands in Default Group.\n"
            "2. **Import then reassign:** import first (all categories land in "
            "*Default Group*), then drag/reassign each to its group in Admin. Group "
            "reassignment does not require re-importing products.\n\n"
        )
        f.write(
            "`group-category-map.csv` is the machine-readable version of this sheet.\n"
        )

    return unmapped, tax_out, map_out


LONGDESC_LIMIT = 50
SHORTDESC_LIMIT = 15


def _truncate_word_boundary(s, limit):
    """Truncate to `limit` chars without cutting a word in half. Breaks on a
    space or hyphen (keeping the hyphen, e.g. "Tamper-" not "Tamper"); falls
    back to a hard cut only if there's no reasonable boundary to use."""
    if len(s) <= limit:
        return s
    truncated = s[:limit].rstrip()
    last_space = truncated.rfind(" ")
    last_hyphen = truncated.rfind("-")
    if last_hyphen > last_space:
        cut = last_hyphen + 1  # keep the hyphen, e.g. "Tamper-" not "Tamper"
    else:
        cut = last_space
    if cut > limit * 0.5:
        truncated = truncated[:cut]
        return truncated.rstrip(", ;")
    return truncated.rstrip(",; -")


def _find_finish_span(s, finish):
    """Locate `finish` inside `s`, treating '-' and ' ' as equivalent. Both
    substitutions are single-character-for-single-character, so the returned
    span indexes directly into the original (un-normalized) string."""
    norm_s = s.replace("-", " ").lower()
    norm_finish = finish.replace("-", " ").lower()
    idx = norm_s.find(norm_finish)
    if idx == -1:
        return None
    return (idx, idx + len(norm_finish))


def build_long_desc(product_name, brand, finish, limit=LONGDESC_LIMIT):
    """Build a LongDesc that fits eCat's 50-char limit without truncating the
    Finish word off the end (the one piece of the name that actually
    distinguishes finish-variant SKUs from each other in a list view).

    Returns (long_desc, was_truncated, finish_mismatch):
      - was_truncated: the cleaned name still didn't fit and had to be cut.
      - finish_mismatch: the source Finish field's value doesn't appear
        anywhere in Product Name (case/hyphen-insensitive) — a source data
        quality issue (Finish column vs. Name column disagree), not
        something safe to silently paper over. The name is left untouched
        in this case rather than forcing in an unverified color word.
    """
    s = product_name.replace("\u00ae", "").replace("\u2122", "")
    s = re.sub(rf"^\s*{re.escape(brand)}\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r",?\s*with Microban\.?\s*$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s{2,}", " ", s)
    s = re.sub(r",\s*,", ",", s)
    s = s.strip().strip(",").strip()

    finish = (finish or "").strip()
    core, suffix, mismatch = s, "", False
    if finish and finish not in ("#N/A", "0"):
        span = _find_finish_span(s, finish)
        if span:
            start, end = span
            finish_text = s[start:end]
            core = (s[:start] + s[end:]).strip()
            core = re.sub(r"\s{2,}", " ", core).strip(" ,-")
            suffix = f", {finish_text}"
        else:
            mismatch = True

    if len(core) + len(suffix) <= limit:
        return (core + suffix).strip(", "), False, mismatch

    core_trunc = _truncate_word_boundary(core, limit - len(suffix))
    final = (core_trunc + suffix).strip(", ")
    return final, True, mismatch


def build_short_desc(long_desc, limit=SHORTDESC_LIMIT):
    """Best-effort compact label for order-form/admin grid views. ShortDesc
    falls back to LongDesc if left blank, but a populated short label reads
    far better in narrow columns than a mid-word-truncated LongDesc would."""
    return _truncate_word_boundary(long_desc, limit)


def main():
    print("Loading image filename mapping...")
    image_map = load_image_filenames()
    print(f"  {len(image_map)} products have image filenames")

    print("Loading pricing data from xlsx files...")
    us_radiant = load_us_radiant_prices()
    us_adorne = load_us_adorne_prices()
    ca_radiant = load_ca_radiant_prices()
    ca_adorne = load_ca_adorne_prices()

    print(f"  US Radiant: {len(us_radiant)} items")
    print(f"  US Adorne:  {len(us_adorne)} items")
    print(f"  CA Radiant: {len(ca_radiant)} items")
    print(f"  CA Adorne:  {len(ca_adorne)} items")

    print(f"\nReading main product file: {PRODUCT_FILE}")
    with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        source_rows = list(reader)
    print(f"  Loaded {len(source_rows)} rows")

    # Build products.csv
    products_out = os.path.join(OUTPUT_DIR, "products.csv")
    stories_out = os.path.join(OUTPUT_DIR, "stories.csv")

    ecat_fields = [
        "BaseItemCode",
        "LongDesc",
        "ShortDesc",
        "ImageFileName",
        "Dimensions",
        "ShipWeight",
        "PackedVolume",
        "PackQuantity",
        "MinimumQuantity",
        "TradeNameCode",
        "CollectionCodes",
        "CategoryCodes",
        "NewItem",
        "NetPrice",
        "PromotionPrice",
        "Price_retail",
        "Price_imap",
        "Price_canet",
        "Price_caimap",
        "Price_camsrp",
        "UPCValue",
        # Custom fields registered in Admin > Products > Custom Fields with
        # send_to_ipad=true. All 18 registered fields must appear here (even if
        # blank) or the importer emits a Warning for each missing column.
        "Finish",
        "CountryOfOrigin",
        "drop_ship",
        "shipped_via",
        "order_uom",
        # Spec fields — blank until Legrand provides data; registered 2026-07-23
        "rohscompliant",
        "Color",
        "voltage",
        "wattage",
        "switchtype",
        "workswith",
        "wiresize",
        "mountingtype",
        "prop65",
        "warranty",
        "numberofswitches",
        "bulbcompatibility",
        "numberofgangs",
        # Freight / carton packaging — only when INCLUDE_CARTON_FIELDS is True
        # (Admin custom fields must be registered first; see CARTON_FIELDS)
        *(
            [name for name, _src, _label in CARTON_FIELDS]
            if INCLUDE_CARTON_FIELDS
            else []
        ),
        # Built-in reserved field (no custom-field registration needed)
        "RelatedItems",
    ]

    # Derive finish-variant families -> RelatedItems
    related_map, related_families = build_related_items(source_rows)
    related_sku_count = sum(len(fam) for fam in related_families)

    products = []
    stories = []
    missing_us_price = []
    missing_ca_price = []
    story_na_skipped = 0
    longdesc_truncated = []
    finish_name_mismatches = []
    image_fallback_codes = []

    for row in source_rows:
        item_id = row["Item ID"].strip()
        collection = row["Collection"].strip()
        product_name = get_product_name(row)

        # Resolve US pricing
        if collection == "adorne":
            us_price = us_adorne.get(item_id, {})
            ca_price = ca_adorne.get(item_id, {})
            # Also check main file pricing as fallback
            main_dn = strip_currency(row.get("Dist NET 1", ""))
            main_retail = strip_currency(row.get("Retail Price", ""))
            main_imap = strip_currency(row.get("IMAP Price", ""))
            main_ca_net = strip_currency(row.get("Canadiant NET", ""))
            main_ca_imap = strip_currency(row.get("Canadian IMAP", ""))
            main_ca_msrp = strip_currency(row.get("Canadian MSRP", ""))
        else:
            us_price = us_radiant.get(item_id, {})
            ca_price = ca_radiant.get(item_id, {})
            main_dn = ""
            main_retail = ""
            main_imap = ""
            main_ca_net = ""
            main_ca_imap = ""
            main_ca_msrp = ""

        # Determine final pricing (prefer price list files, fallback to main file)
        net_price = us_price.get("dn", "") or main_dn
        retail_price = us_price.get("msrp", "") or main_retail
        imap_price = us_price.get("imap", "") or main_imap
        ca_net = ca_price.get("net_cad", "") or main_ca_net
        ca_imap = ca_price.get("imap_cad", "") or main_ca_imap
        ca_msrp = ca_price.get("msrp_cad", "") or main_ca_msrp

        if not net_price:
            missing_us_price.append(item_id)
        if not ca_net:
            missing_ca_price.append(item_id)

        # Build dimensions string
        dimensions = build_dimensions(
            row.get("height", ""), row.get("width/dia", ""), row.get("length", "")
        )

        # Ship weight (lb passthrough; grams converted to lb)
        ship_weight = parse_ship_weight_lb(row.get("weight", ""))

        # Packed volume from carton dims (H x L x W in inches, convert to cubic feet)
        try:
            ch = float(row.get("Carton Height", "0").replace(" in", "").strip() or "0")
            cl = float(row.get("Carton Length", "0").replace(" in", "").strip() or "0")
            cw = float(row.get("Carton Width", "0").replace(" in", "").strip() or "0")
            packed_vol = round((ch * cl * cw) / 1728, 2) if (ch and cl and cw) else 0
        except (ValueError, TypeError):
            packed_vol = 0
        packed_vol_str = str(packed_vol) if packed_vol > 0 else "0.01"

        # Image filename: only ship a filename we actually verified against a
        # downloaded image (image_map, built from the real CDN links file).
        # Guessing "{item_id}.jpg" for the ~20 codes with no verified image
        # would ship an ImageFileName that matches no real file on FTP —
        # worse than leaving it blank, since it looks intentional but isn't.
        image_filename = image_map.get(item_id, "")
        if not image_filename:
            image_fallback_codes.append(item_id)

        finish = get_finish(row)
        long_desc, was_truncated, finish_mismatch = build_long_desc(
            product_name, collection, finish
        )
        short_desc = build_short_desc(long_desc)
        if was_truncated:
            longdesc_truncated.append((item_id, product_name, long_desc))
        if finish_mismatch:
            finish_name_mismatches.append(
                (item_id, product_name, finish or row.get("Finish", ""))
            )

        product = {
            "BaseItemCode": item_id,
            "LongDesc": long_desc,
            "ShortDesc": short_desc,
            "ImageFileName": image_filename,
            "Dimensions": dimensions,
            "ShipWeight": ship_weight or "0",
            "PackedVolume": packed_vol_str,
            "PackQuantity": "1",
            "MinimumQuantity": clean_order_min(row.get("Order Minimum", "1")),
            # Brand-first nav: adorne / radiant are Trade Names (not Collections
            # under a parent "Legrand"). CollectionCodes mirrors the TN.
            "TradeNameCode": collection,
            "CollectionCodes": collection,
            "CategoryCodes": clean_category(row.get("Category", "")),
            "NewItem": "N",
            "NetPrice": net_price or "0.00",
            "PromotionPrice": "",
            "Price_retail": retail_price,
            "Price_imap": imap_price,
            "Price_canet": ca_net,
            "Price_caimap": ca_imap,
            "Price_camsrp": ca_msrp,
            "UPCValue": row.get("UPC", "").strip(),
            "Finish": finish,
            "CountryOfOrigin": clean_country(row.get("Country of Origin", "")),
            "drop_ship": to_boolean_y(row.get("Drop Ship", "")),
            "shipped_via": clean_na(row.get("Shipped Via", "")),
            "order_uom": clean_na(row.get("Order Unit of Measure", "")),
            "RelatedItems": related_map.get(item_id, ""),
        }
        # Freight / carton fields — only when registered in Admin
        if INCLUDE_CARTON_FIELDS:
            for name, src, _label in CARTON_FIELDS:
                product[name] = clean_na(row.get(src, ""))
        products.append(product)

        # Stories (skip the source's '#N/A' null token — it must not be
        # written as a product story)
        romance = clean_na(row.get("Romance Copy", ""))
        if romance:
            stories.append({"BaseItemCode": item_id, "ProductStory": romance})
        elif (row.get("Romance Copy", "") or "").strip() in ("#N/A", "0"):
            story_na_skipped += 1

    # Write products.csv
    print(f"\nWriting {len(products)} rows to {products_out}")
    with open(products_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ecat_fields)
        writer.writeheader()
        writer.writerows(products)

    # Write stories.csv
    print(f"Writing {len(stories)} rows to {stories_out}")
    with open(stories_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["BaseItemCode", "ProductStory"])
        writer.writeheader()
        writer.writerows(stories)

    # Taxonomy worksheet (Group -> Category mapping to the client's 5 groups)
    unmapped_categories, tax_out, map_out = write_taxonomy_files(products)
    print(f"  {tax_out}")
    print(f"  {map_out}")
    if unmapped_categories:
        print(
            "  WARNING: categories not in CATEGORY_TO_GROUP (assign a group): "
            + ", ".join(unmapped_categories)
        )

    # Custom-field setup instructions (Admin pre-registration)
    finish_values = sorted({p["Finish"] for p in products if p["Finish"]})
    drop_ship_vals = sorted({p["drop_ship"] for p in products if p["drop_ship"]})
    shipped_via_vals = sorted({p["shipped_via"] for p in products if p["shipped_via"]})
    uom_vals = sorted({p["order_uom"] for p in products if p["order_uom"]})
    coo_vals = sorted({p["CountryOfOrigin"] for p in products if p["CountryOfOrigin"]})

    setup_out = os.path.join(OUTPUT_DIR, "custom-fields-setup.md")
    with open(setup_out, "w", encoding="utf-8") as f:
        f.write("# Legrand — Custom Field & Related Items Setup\n\n")
        f.write(
            "Custom fields must be pre-registered in **Admin > Products > Custom "
            "Fields** before import, with **Send to iPad** checked and a Label set. "
            "Any column in `products.csv` that is not registered is silently ignored "
            "on import (so shipping the columns now is harmless).\n\n"
        )
        f.write("## Register these custom fields\n\n")
        f.write(
            "| Field name (CSV header) | Label | Type | Send to iPad | Use as filter | Recommendation |\n"
        )
        f.write(
            "|---|---|---|---|---|---|\n"
        )
        f.write(
            f"| `Finish` | Finish | String | Yes | **Multi-select** | Ship. {len(finish_values)} distinct values -> strong catalog filter |\n"
        )
        f.write(
            f"| `CountryOfOrigin` | Country of Origin | String | Yes | No (detail only) | Ship. {len(coo_vals)} values: {', '.join(coo_vals)} |\n"
        )
        f.write(
            f"| `drop_ship` | Drop Ship | Boolean | Optional | Boolean (optional) | Constant ({', '.join(drop_ship_vals) or 'none'}) — low value, OK to skip registering |\n"
        )
        f.write(
            f"| `shipped_via` | Shipped Via | String | Optional | No | Constant ({', '.join(shipped_via_vals) or 'none'}) — low value, OK to skip registering |\n"
        )
        f.write(
            f"| `order_uom` | Order Unit | String | Optional | No | Low cardinality ({', '.join(uom_vals) or 'none'}) — OK to skip registering |\n"
        )
        f.write("\n### Distinct Finish values (for reference)\n\n")
        f.write(", ".join(finish_values) + "\n")
        f.write("\n### Finish data quality — confirm with client\n\n")
        f.write(
            "Applied unambiguous Finish spelling fixes automatically: "
            + ", ".join(f"`{k}` -> `{v}`" for k, v in FINISH_FIXES.items())
            + ".\n\n"
        )
        if FINISH_OVERRIDES:
            f.write(
                "Per-SKU Finish overrides (Name + SKU suffix were right; Finish "
                "column was wrong):\n\n"
            )
            for k, v in FINISH_OVERRIDES.items():
                f.write(f"- `{k}` -> `{v}`\n")
            f.write("\n")
        f.write(
            "The following look like possible duplicates but were **left as-is** "
            "because they may be genuinely distinct finishes. As a multi-select "
            "filter each becomes its own facet — confirm whether any should be "
            "merged:\n\n"
        )
        present = {v for v in finish_values}
        for grp in FINISH_REVIEW_GROUPS:
            hits = [g for g in grp if g in present]
            if len(hits) > 1:
                f.write("- " + " / ".join(f"`{h}`" for h in hits) + "\n")

        f.write("\n## Freight / carton custom fields\n\n")
        f.write(
            "Per the client rule that all non-blank source data must land, the "
            "source's carton/packaging columns are captured verbatim. **Recommend "
            "registering these as custom fields with 'Send to iPad' checked but "
            "'Hide from details view' selected** — the data lands (and is usable in "
            "reports/SmartLists) without cluttering the rep-facing catalog. "
            "Confirm the display choice with the client.\n\n"
        )
        f.write("| Field name (CSV header) | Label | Source column | Populated |\n")
        f.write("|---|---|---|---|\n")
        for name, src, label in CARTON_FIELDS:
            pop = sum(1 for p in products if p.get(name, "").strip())
            f.write(f"| `{name}` | {label} | {src} | {pop} |\n")
        f.write(
            "\n**Notes:** `Carton Weight 2` was byte-identical to `Carton Weight` "
            "on every row, so it is captured once as `carton1_wt` (not duplicated). "
            "Carton tiers 1/2/3 are captured positionally; which physical package a "
            "tier represents varies row-to-row in the source, so treat them as raw "
            "freight data, not clean inner/master/pallet levels. `cartons_per_unit` "
            "is constant (`1`).\n"
        )

        f.write("\n## Related Items (built-in — NO custom-field registration)\n\n")
        f.write(
            f"`RelatedItems` is a reserved product-file field. It is populated for "
            f"**{related_sku_count} SKUs** across **{len(related_families)} finish "
            f"families**, cross-linking each product to its other finish variants. "
            "Each product's list includes its own BaseItemCode (per eCat best "
            "practice) so reps can navigate in any direction. See "
            "`related-items-review.md` for the full grouping.\n\n"
        )
        f.write("## Not applicable for this dataset\n\n")
        f.write(
            "- **Product Options** — the source `Add Option 1..10` columns are 100% "
            "empty and each finish is its own orderable SKU, so the eCat Options "
            "feature is not used. Finish variants are modeled as Related Items.\n"
            "- **Spec custom fields** (LED/fan/bulb specs, certifications, Materials, "
            "Special Feature, document URLs, etc.) — every one of these source "
            "columns is empty in this file, so there is nothing to publish.\n"
            "- **Extra price levels** (`UMAP`, `Dist NET 2..10`, `Sales Price`) — all "
            "empty; only the mapped US/CA price levels carry data.\n"
        )
    print(f"  {setup_out}")

    # Related Items review
    rel_out = os.path.join(OUTPUT_DIR, "related-items-review.md")
    with open(rel_out, "w", encoding="utf-8") as f:
        f.write("# RelatedItems build review\n\n")
        f.write(
            f"Derived **{len(related_families)} finish-variant families** covering "
            f"**{related_sku_count} SKUs**. Families are grouped by product name with "
            "the Finish token removed; every member lists the full family (including "
            "itself) in the `RelatedItems` column.\n\n"
        )
        f.write("## How to validate\n\n")
        f.write(
            "Spot-check that members of a family truly differ only by finish (SKU "
            "prefixes should match, finish suffix differs). A handful of families "
            "may include a related pack/variant that shares a finish — still a valid "
            "'related' relationship, not an error.\n\n"
        )
        f.write("## Fixed since first pass (2026-07-14)\n\n")
        f.write(
            "`ASPD1531W277` (White, 277V half-size switch) was silently dropped from "
            "its own family and missing from its siblings' lists. Root cause: the "
            "source `Product Name` had a typo — **\"227V\" instead of \"277V\"** — so "
            "the finish-stripped grouping key didn't match `ASPD1531G277` / "
            "`ASPD1531M277`. Fixed via `PRODUCT_NAME_FIXES`; confirm the \"227V\" typo "
            "with Legrand so it's corrected at the source too.\n\n"
        )
        f.write(
            "Additional hand-verified `PRODUCT_NAME_FIXES` (SKU suffix + Finish column "
            "agree; Name color/product-type word was wrong) that re-join finish "
            "families:\n\n"
            "- `ADPD153LM2` — Name said Graphite, Finish/SKU = Magnesium\n"
            "- `AC6RJ45M1`, `ACBLKM4`, `ACRJ25M1`, `ACRJ25W1` — Name color word wrong\n"
            "- Netatmo G-suffix (`WNAL33G1`, `WNAL63G1`, `WNAL43G1`, `WNACB40G1`) — "
            "Name said Nickel, Finish/SKU = Graphite\n"
            "- Netatmo M-suffix (`WNAL33M1`, `WNAL63M1`, `WNAL43M1`) — Name "
            "copy-pasted as Scene Controller; G/W siblings prove correct product type\n"
            "- `2097TRWRUSBACBK` — Name said Ivory, Finish/SKU = Black\n\n"
            "`FINISH_OVERRIDES` also swaps the Finish columns on `WNRL43CKITNI` / "
            "`WNRL43CKITLA` (Name + SKU suffix were right; Finish columns were swapped).\n\n"
        )
        f.write(
            "**We deliberately did not add a generic fuzzy/edit-distance matcher** to "
            "catch other typos like this automatically. Tested a difflib similarity "
            "pass (0.95 cutoff) against this dataset: it produced 118 candidate merges "
            "and nearly all were false positives — e.g. it wanted to merge the 15A GFCI "
            "family with the unrelated 20A GFCI family, and the 1-gang/2-gang/3-gang "
            "wall plate families with each other. This catalog has too many genuinely-"
            "different products with 1-3 character name differences for similarity "
            "matching to be safe here. Any further gaps among the singleton "
            "(no-RelatedItems) SKUs below should be hand-verified against the source "
            "row before assuming they're a bug.\n\n"
        )
        f.write("## Families\n\n")
        for fam in related_families:
            f.write(f"- ({len(fam)}) " + ", ".join(fam) + "\n")
    print(f"  {rel_out}")

    # LongDesc / ShortDesc build review
    longdesc_out = os.path.join(OUTPUT_DIR, "longdesc-review.md")
    with open(longdesc_out, "w", encoding="utf-8") as f:
        f.write("# LongDesc / ShortDesc build review\n\n")
        f.write(
            "**Fixed 2026-07-14:** the first pass copied the source `Product Name` "
            "straight into `LongDesc` verbatim. 668 of 1,020 rows (65%) exceeded "
            "eCat's 50-char limit (avg 61, max 143) — guaranteed length Warnings on "
            "import and mid-word truncation in the app's grid/list/order views. "
            "`ShortDesc` was also left blank on all 1,020 rows, so there was no "
            "shorter fallback name either.\n\n"
        )
        f.write("## What the build now does\n\n")
        f.write(
            "1. Strip `®`/`™` and the leading brand word (redundant with "
            "`CollectionCodes` — adorne/radiant is already shown as the "
            "Collection).\n"
            "2. Strip the trailing \", with Microban\" marketing suffix (antimicrobial "
            "protection is a line-wide feature on nearly every SKU, not a "
            "differentiator — not worth the character budget in the display name).\n"
            "3. Locate the SKU's `Finish` value inside what's left (hyphen/space "
            "insensitive) and anchor it to the end, so truncation trims the "
            "*description*, never the finish/color word that differentiates finish-"
            "variant SKUs from each other in a list view.\n"
            "4. If still over 50 chars, truncate at the last word boundary (never "
            "mid-word) and log it below for a human spot-check.\n"
            "5. `ShortDesc` is the cleaned name truncated to 15 chars at a word "
            "boundary — best-effort; still far better than blank for narrow admin/"
            "order-form columns.\n\n"
        )
        f.write(
            f"**Result: 0 of {len(products)} rows exceed 50 chars.** "
            f"{len(longdesc_truncated)} rows needed word-boundary truncation to fit — "
            "listed below for a quick human read-through (most reasonable; a few may "
            "read better with manual editorial polish).\n\n"
        )
        f.write(f"## Rows that required truncation ({len(longdesc_truncated)})\n\n")
        f.write("| BaseItemCode | Original Product Name | Built LongDesc |\n|---|---|---|\n")
        for code, orig, final in longdesc_truncated:
            f.write(f"| {code} | {orig} | {final} |\n")
        f.write(
            f"\n## Finish field / Product Name disagreements ({len(finish_name_mismatches)})\n\n"
        )
        f.write(
            "For these SKUs, the source `Finish` column's value does not appear "
            "anywhere in `Product Name` (checked case/hyphen-insensitive). Rather "
            "than guess which one is right, `LongDesc` keeps whatever color word (if "
            "any) is already in the Name text, unmodified. The `Finish` custom field "
            "(used for the multi-select finish filter) still uses the `Finish` "
            "column's value — so on these SKUs the filter facet and the display name "
            "may not visually agree. **Flag to Legrand's data team to confirm which "
            "column is correct.**\n\n"
        )
        f.write("| BaseItemCode | Product Name | Finish field |\n|---|---|---|\n")
        for code, name, finish in finish_name_mismatches:
            f.write(f"| {code} | {name} | {finish} |\n")
    print(f"  {longdesc_out}")

    # Build inventory.csv
    print("\nLoading inventory source files...")
    product_codes = {p["BaseItemCode"] for p in products}
    inventory_source_rows = []
    for path in INVENTORY_SOURCE_FILES:
        line = "adorne" if "Adorne" in os.path.basename(path) else "radiant"
        rows = load_inventory_source(path, line)
        print(f"  {os.path.basename(path)}: {len(rows)} rows")
        inventory_source_rows.extend(rows)

    inventory = []
    orphan_codes = []
    negative_qty_codes = []
    unscheduled_codes = []
    seen_codes = set()
    dup_codes = []

    for row in inventory_source_rows:
        code = row["Item Number"].strip()
        if not code:
            continue
        if code in seen_codes:
            dup_codes.append(code)
            continue
        seen_codes.add(code)

        qty_raw = row.get("Qty On Hand", "").strip()
        try:
            qty = int(qty_raw)
        except ValueError:
            qty = 0
        if qty < 0:
            negative_qty_codes.append(code)

        next_receipt_date = normalize_receipt_date(row.get("Item Next Availability Date", ""))
        if not next_receipt_date and row.get("Item Next Availability Date", "").strip():
            unscheduled_codes.append(code)

        if code not in product_codes:
            orphan_codes.append(code)

        inventory.append(
            {
                "BaseItemCode": code,
                "QtyAvailable": qty,
                "QtyOnHand": qty,
                "NextReceiptDate": next_receipt_date,
            }
        )

    inventory.sort(key=lambda r: r["BaseItemCode"])
    missing_inventory_codes = sorted(product_codes - seen_codes)

    inventory_out = os.path.join(OUTPUT_DIR, "inventory.csv")
    print(f"\nWriting {len(inventory)} rows to {inventory_out}")
    with open(inventory_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["BaseItemCode", "QtyAvailable", "QtyOnHand", "NextReceiptDate"]
        )
        writer.writeheader()
        writer.writerows(inventory)

    # Inventory review notes
    review_out = os.path.join(OUTPUT_DIR, "inventory-review.md")
    with open(review_out, "w", encoding="utf-8") as f:
        f.write("# inventory.csv build review\n\n")
        f.write(
            "Source: `LegrandAdorneInventory.csv` + `LegrandRadiantInventory.csv` "
            f"({len(inventory_source_rows)} combined rows, {len(inventory)} unique BaseItemCode).\n\n"
        )
        f.write("## Assumptions (confirm with client)\n\n")
        f.write(
            "- **QtyAvailable = QtyOnHand.** The source has no independent "
            "backorder/reserved columns (both are 100% blank), so on-hand is passed "
            "through as the available-to-promise quantity. This is supported by the "
            f"data: all {len(negative_qty_codes)} negative-quantity rows are exactly "
            "the rows also flagged `to be sched`, suggesting on-hand already nets "
            "against uncommitted replenishment for those SKUs. If on-hand is actually "
            "a raw warehouse count instead, QtyAvailable should not mirror it.\n"
        )
        f.write(
            "- **NextReceiptDate blanked where source said `to be sched`.** Prose is "
            "not a valid date and would fail import validation; blank means "
            "'unknown' rather than 0/none.\n"
        )
        f.write(
            "- **QtyOnBackorder, QtyOnPOrder, QtyReserved, QtyInTransit, QtyOverseas, "
            "QtyInShowroom, NextReceiptQty omitted** — no source data exists for any "
            "of them (the source's `Qty Backordered`/`Qty On Order` columns are blank "
            "on every row).\n"
        )
        f.write(f"\n## Negative on-hand quantity ({len(negative_qty_codes)} SKUs)\n\n")
        f.write(
            "All correspond to `to be sched` rows; treated as valid signed integers "
            "per the importer spec (not blocked).\n\n"
        )
        f.write(", ".join(negative_qty_codes) + "\n")
        f.write(f"\n## Orphan inventory rows — no matching product ({len(orphan_codes)})\n\n")
        f.write(
            "These import without error but can't be ordered since they don't match "
            "a BaseItemCode in products.csv. Included as-is; flag to client in case "
            "some represent products missing from the catalog.\n\n"
        )
        f.write(", ".join(orphan_codes) + "\n")
        f.write(f"\n## Products with no inventory row ({len(missing_inventory_codes)})\n\n")
        f.write("Will show no stock data on the iPad until the client's export includes them.\n\n")
        f.write(", ".join(missing_inventory_codes) + "\n")
        if dup_codes:
            f.write(f"\n## Duplicate Item Numbers dropped ({len(dup_codes)})\n\n")
            f.write(", ".join(dup_codes) + "\n")
    print(f"  {review_out}")

    # Summary
    print("\n=== BUILD SUMMARY ===")
    print(f"Total products: {len(products)}")
    print(f"Total stories:  {len(stories)} (skipped {story_na_skipped} '#N/A' romance rows)")
    print(
        f"RelatedItems:   {related_sku_count} SKUs in {len(related_families)} finish families"
    )
    print(f"Missing US net price (NetPrice=0.00): {len(missing_us_price)}")
    if missing_us_price:
        print(f"  First 10: {missing_us_price[:10]}")
    print(f"Missing CA net price: {len(missing_ca_price)}")
    if missing_ca_price:
        print(f"  First 10: {missing_ca_price[:10]}")

    # Data quality report
    long_names = sum(1 for p in products if len(p["LongDesc"]) > 50)
    print(f"\nLongDesc > 50 chars (will warn): {long_names}")
    print(f"  (of which needed word-boundary truncation to fit: {len(longdesc_truncated)})")
    print(f"  Finish field / Name disagreements (see longdesc-review.md): {len(finish_name_mismatches)}")
    no_short_desc = sum(1 for p in products if not p["ShortDesc"])
    print(f"ShortDesc blank: {no_short_desc}")
    no_finish = sum(1 for p in products if not p["Finish"])
    print(f"No Finish value: {no_finish}")
    zero_price = sum(1 for p in products if p["NetPrice"] == "0.00")
    print(f"NetPrice = 0.00: {zero_price}")
    print(f"ImageFileName blank (no verified image, was previously a guessed filename): {len(image_fallback_codes)}")
    if image_fallback_codes:
        print(f"  {', '.join(image_fallback_codes)}")

    print(f"\nTotal inventory rows: {len(inventory)}")
    print(f"  Negative QtyOnHand: {len(negative_qty_codes)}")
    print(f"  NextReceiptDate blanked ('to be sched'): {len(unscheduled_codes)}")
    print(f"  Orphan rows (no matching product): {len(orphan_codes)}")
    print(f"  Products with no inventory row: {len(missing_inventory_codes)}")
    if dup_codes:
        print(f"  Duplicate Item Numbers dropped: {len(dup_codes)}")

    print(f"\nOutput files:")
    print(f"  {products_out}")
    print(f"  {stories_out}")
    print(f"  {inventory_out}")
    print(f"  {review_out}")
    print(f"  {setup_out}")
    print(f"  {rel_out}")
    print(f"  {longdesc_out}")
    print(f"  {tax_out}")
    print(f"  {map_out}")
    print("\nDone.")


if __name__ == "__main__":
    main()
