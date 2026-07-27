#!/usr/bin/env python3
"""
Lib & Co. eCat core-file rebuild.

Inputs (in ~/Downloads):
  - Lib_Co_Spec_Master_eCat_Mapped - Lib_Co_Spec_Master_eCat_Mapped.csv (1).csv   (canonical source)
  - LIB_Co_Upload_Fixed_Prices - LIB_Co_Upload_Fixed_Prices.csv (1).csv           (AE's price-ready POC products file)
  - Lib & Co Inventory with eCat Headers - Inventory Feed (1).csv                 (raw inventory feed)

Outputs (in ./output):
  - products.csv              (LongDesc backfilled, 9 parts SKUs added, fields cleaned)
  - stories.csv               (real Productstory built from spec master Feature 1-5 concat)
  - inventory.csv             (secondary header dropped, "Not needed" column dropped)
  - unmatched_inventory.csv   (inventory rows with no matching product, for Silvio spot-check)
  - rebuild_report.txt        (human-readable summary)

Why this script exists:
  AE's POC mapped product NAMES into stories.Productstory, leaving LongDesc empty on all 897 rows.
  Catalog/Details/Order views would show no product names. This rebuild fixes that AND replaces
  the stories file with real romance copy (the spec master's Feature 1-5 narrative content).
"""
from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Iterable

DOWNLOADS = Path("/Users/kylorjohnson/Downloads")
OUTDIR = Path(__file__).parent / "output"
OUTDIR.mkdir(parents=True, exist_ok=True)

SPEC_PATH = DOWNLOADS / "Lib_Co_Spec_Master_eCat_Mapped - Lib_Co_Spec_Master_eCat_Mapped.csv.csv"
POC_PRODUCTS_PATH = DOWNLOADS / "LIB_Co_Upload_Fixed_Prices - LIB_Co_Upload_Fixed_Prices.csv.csv"
INVENTORY_PATH = DOWNLOADS / "Lib & Co Inventory with eCat Headers - Inventory Feed.csv"
# Optional: Jon's pre-mapped customers file. If missing, customer rebuild is skipped
# and the previous output/customers.csv is preserved.
CUSTOMERS_PATH = DOWNLOADS / "LIB_Customers_eCat_Mapped - LIB_Customers_eCat_Mapped.csv.csv"
# Rep List file lives alongside the script (it's xlsx-disguised-as-csv).
REP_LIST_PATH = Path(__file__).parent / "Rep List.csv"

# Email corrections for the rep list (typos / multi-email fields).
REP_EMAIL_OVERRIDES = {
    # Source had "steve@riccislaes.com; accounting@riccisales.com" - first has a typo,
    # second is the AR mailbox not the rep. Use corrected primary.
    "SR": "steve@riccisales.com",
}
# Country code -> eCat user group (US/MX bundled because MX rep is USD-currency).
REP_USER_GROUP_BY_COUNTRY = {
    "US": "Lib & Co - US Reps",
    "MX": "Lib & Co - US Reps",
    "PR": "Lib & Co - US Reps",
    "CA": "Lib & Co - Canadian Reps",
}
DEFAULT_USER_TYPE = "rep"

# Placeholder strategy for required-but-blank customer fields.
# Pattern documented in kickoff call: "any of these can be kind of bypassed with
# just placeholder data, if you don't want to use any of it" (Kyler to Silvio, May 22).
PLACEHOLDER_ADDRESS = "TBD"
PLACEHOLDER_CITY = "TBD"
PLACEHOLDER_POSTCODE = "00000"
PLACEHOLDER_TERRITORY = "TBD"
PLACEHOLDER_STATE_BY_COUNTRY = {
    "CA": "ON",  # default to Ontario (HQ province)
    "US": "XX",
    "PR": "PR",
    "MX": "XX",
}
DEFAULT_PLACEHOLDER_STATE = "XX"
DEFAULT_PLACEHOLDER_COUNTRY = "US"

# Country -> price-level routing. Only USD WSP / CAD WSP are real price levels
# in eCat. The IMAP comparison price displays alongside via Company Settings
# (configured separately in Admin, not on the customer row).
COUNTRY_TO_PRICE_CODE = {
    "CA": "cad-wsp",
    "US": "us-wsp",
    "PR": "us-wsp",  # US territory, gets USD pricing
    "MX": "us-wsp",  # default to USD until Silvio confirms
}
DEFAULT_PRICE_CODE = "us-wsp"

LONGDESC_MAX = 50

# Per May 28 call with Silvio: 25% off Canadian and US prices across the board for
# discontinued sell-through. Applied to all 4 price columns so it works for any
# customer currency / price-level routing.
DISCOUNT_RATE = 0.25
PROMO_CATEGORY_TAG = "Discontinued - 25% Off"

# Hard-drop SKUs (already sold / not real inventory). Per Silvio on May 28:
# "even the one that has one isn't really real, it's sitting at my desk right now,
# it's already sold" - referring to 10131-06.
FORCE_DROP_SKUS = {"10131-06"}

# Manual product additions. Each entry: clone an existing product row, override
# variant-specific fields. Per Silvio May 28: only 10193-02 (Adelfia Matte Black,
# 111 units in inventory but missing from product file) needs adding from the
# unmatched_inventory list. The other 6 unmatched SKUs are part of the discontinued
# set and have zero stock or are already-sold (10131-06).
FORCE_ADD_PRODUCTS = [
    {
        "sku": "10193-02",
        "clone_from": "10193-030",
        "overrides": {
            "LongDesc": "Adelfia, 1 Light LED Pendant, Matte Black",
            "UPCValue": "",      # not in spec master; flag for Silvio
            "FinishCode": "Matte Black",
            "ImageFileName": "10193-02.jpg,10193-02-1.jpg,10193-02-2.jpg",
            "NewItem": "N",
            "Video": "",         # not known for this variant; flag for Silvio
        },
    },
]

BELLISSIMA_TUBES_SILVER = ["12069-01", "12070-01", "12071-01"]
BELLISSIMA_TUBES_BLACK = ["12069-02", "12070-02", "12071-02"]
ALCAMO_RODS = ["12298", "12299", "12300"]
PARTS_TO_ADD = BELLISSIMA_TUBES_SILVER + BELLISSIMA_TUBES_BLACK + ALCAMO_RODS

BELLISSIMA_PARENTS_SILVER = ["12064-01", "12065-01", "12066-01", "12067-01", "12068-01", "12176-01", "12177-01"]
BELLISSIMA_PARENTS_BLACK = ["12064-02", "12065-02", "12066-02", "12067-02", "12068-02", "12176-02", "12177-02"]
ALCAMO_PARENTS = ["12414-02", "12415-02", "12416-02", "12284-02", "12285-02"]

INTRO_DATE_FIXES = {
    "Janaury 2024": "January 2024",
    "2025": "January 2025",
    "Catalogue 2026": "January 2026",
    "January 204": "January 2024",
    "January 225": "January 2025",
}

MONTHS = {m: f"{i:02d}" for i, m in enumerate(
    ["January","February","March","April","May","June",
     "July","August","September","October","November","December"], start=1)}

DISCONTINUED_NRD_VALUES = {"discontinued once sold-out", "discontinued"}
BLANK_NRD_VALUES = {"tbd", "restock date", ""}

# Spec-master column positions (verified by inspection of header + secondary-header rows).
SPEC_COL = {
    "BaseItemCode": 0,
    "LongDesc": 1,           # "Description"
    "UPCValue": 2,           # "UPC Number"
    "Collection": 3,         # "Collection name"
    "Category": 4,           # "Category - Product Category"
    "Subcategory": 5,        # "Sub Product Category"
    "Feature1": 6, "Feature2": 7, "Feature3": 8, "Feature4": 9, "Feature5": 10,
    "Dimensions": 11,
    "MaxHeight": 12,
    "MinHeight": 13,
    "ChainLength": 14,
    "WireLength": 15,
    "ExtensionRods": 16,
    "BackplateDimension": 17,
    "CanopyDimension": 18,
    "FinishCode": 19,        # "Finish"
    "ShadeMaterial": 20,
    "ShadeColor": 21,
    "NumberOfShades": 22,
    "ShadeDimension": 23,
    "ShipLBS": 24,           # "Product Weight" (string like "70 lbs.")
    "Disclaimer": 25,
    "BulbType": 26,
    "NbrBulbs": 27,
    "TotalWattage": 28,
    "BulbWattage": 29,
    "TotalLumen": 30,
    "Kelvin": 31,
    "CRI": 32,
    "Dimmable": 33,
    "Voltage": 34,           # "Input Voltage"
    "Certifications": 35,
    "IPRating": 36,
    "Rating": 37,            # "Mounting Location Rating"
    "ADA": 38,
    "LEDHours": 39,
    "BulbShape": 40,
    "BulbSocket": 41,
    "BulbIncluded": 42,
    "SlopeCeilingCompatible": 43,
    "IntroDate": 44,         # "Catalogue"
    "Direction": 45,
    "MotionSensor": 46,
    "Materials": 47,         # "Product Material"
    "ImageFileName": 50,     # "concatenate"
    "Price_cad": 51,         # "WSP-CAD"
    "Price_imapcad": 52,     # "IMAP-CAD"
    "netprice": 53,          # "WSP-USD"
    "Price_imapusd": 54,     # "IMAP-USD"
}


# ---------- IO ----------

def read_csv(path: Path) -> tuple[list[str], list[list[str]]]:
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [r for r in reader if r]
    return header, rows


# Output-header normalization for products.csv. The POC source header is mostly
# consistent PascalCase already; these are the two true outliers. Applied ONLY at
# write time so internal column lookups (idx["netprice"], idx["NbrBulbs"], ...) keep
# using the POC source names. The eCat importer downcases headers, so these renames
# do not change standard-field matching; NumberOfBulbs is a CUSTOM field and must be
# registered in Admin under that exact name.
PRODUCTS_HEADER_RENAME = {
    "netprice": "NetPrice",      # US WSP -> standard net_price field
    "NbrBulbs": "NumberOfBulbs",  # match the spelled-out NumberOfShades
}

# Columns dropped from the output entirely. ShipLBS (text, e.g. "2.54 lbs.") is
# redundant with the numeric standard ShipWeight, which is still derived from the
# spec's ShipLBS value via strip_weight(). Internal logic keeps using the POC name.
PRODUCTS_DROP_COLUMNS = {"ShipLBS"}


def finalize_product_output(header: list[str], rows: list[list[str]]) -> tuple[list[str], list[list[str]]]:
    """Apply output-only header renames and column drops, positionally, so the
    internal idx[...] lookups elsewhere can keep using the original POC names."""
    keep = [i for i, h in enumerate(header) if h not in PRODUCTS_DROP_COLUMNS]
    new_header = [PRODUCTS_HEADER_RENAME.get(header[i], header[i]) for i in keep]
    new_rows = [[r[i] for i in keep] for r in rows]
    return new_header, new_rows


def write_csv(path: Path, header: Iterable[str], rows: Iterable[Iterable[str]]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


# ---------- Cleaning helpers ----------

_WHITESPACE_RE = re.compile(r"[\r\n]+")
_NUMERIC_CLEAN_RE = re.compile(r"[^0-9.\-]")


def clean_text(v: str) -> str:
    if v is None:
        return ""
    # KB explicitly bans LF/CR in product file data; collapse them defensively.
    v = _WHITESPACE_RE.sub(" ", str(v))
    return v.strip()


def truncate_longdesc(v: str) -> str:
    return clean_text(v)[:LONGDESC_MAX]


def normalize_intro_date(v: str) -> str:
    v = clean_text(v)
    return INTRO_DATE_FIXES.get(v, v)


def normalize_bool_y_n(v: str) -> str:
    v = clean_text(v)
    if v.lower() == "yes":
        return "Yes"
    if v.lower() == "no":
        return "No"
    return v


def strip_money(v: str) -> str:
    """Convert '$4,058.00' -> '4058.00'. Preserves blanks."""
    v = clean_text(v)
    if not v:
        return ""
    cleaned = _NUMERIC_CLEAN_RE.sub("", v)
    if not cleaned:
        return ""
    try:
        f = float(cleaned)
    except ValueError:
        return cleaned
    # Match the POC convention: integer dollars are stored without trailing .00.
    return str(int(f)) if f.is_integer() else f"{f:.2f}"


def strip_weight(v: str) -> str:
    """'70 lbs.' -> '70'. Preserves blanks."""
    v = clean_text(v)
    if not v:
        return ""
    m = re.search(r"(\d+(?:\.\d+)?)", v)
    return m.group(1) if m else ""


_DATE_RE = re.compile(
    r"^(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s*(\d{4})$",
    re.IGNORECASE,
)

_VARIANT_ROOT_RE = re.compile(r"^(.+)-(\d+)$")
RELATED_ITEMS_MAX = 255


def _variant_root(sku: str) -> str | None:
    m = _VARIANT_ROOT_RE.match(sku)
    return m.group(1) if m else None


def _parse_related_items(val: str) -> list[str]:
    return [x.strip() for x in (val or "").split(",") if x.strip()]


def _join_related_items(codes: list[str]) -> str:
    seen: set[str] = set()
    out: list[str] = []
    for code in codes:
        if code not in seen:
            seen.add(code)
            out.append(code)
    return ",".join(out)


def backfill_variant_sibling_related_items(
    rows: list[list[str]], bic_i: int, rel_i: int, metrics: dict
) -> None:
    """Link finish/size variants that share a SKU root (e.g. 10162-017-01/02/07)."""
    by_root: dict[str, list[int]] = {}
    for i, row in enumerate(rows):
        root = _variant_root(row[bic_i])
        if root:
            by_root.setdefault(root, []).append(i)

    metrics["related_items_sibling_groups"] = 0
    metrics["related_items_sibling_filled"] = 0
    metrics["related_items_sibling_merged"] = 0

    for _root, indices in by_root.items():
        if len(indices) < 2:
            continue
        metrics["related_items_sibling_groups"] += 1
        siblings = sorted({rows[i][bic_i] for i in indices})
        for i in indices:
            existing = _parse_related_items(rows[i][rel_i])
            if not existing:
                new_val = _join_related_items(siblings)
                if len(new_val) <= RELATED_ITEMS_MAX:
                    rows[i][rel_i] = new_val
                    metrics["related_items_sibling_filled"] += 1
            else:
                merged = list(existing)
                for sku in siblings:
                    if sku not in merged:
                        merged.append(sku)
                new_val = _join_related_items(merged)
                if len(new_val) <= RELATED_ITEMS_MAX and new_val != rows[i][rel_i]:
                    rows[i][rel_i] = new_val
                    metrics["related_items_sibling_merged"] += 1


def parse_next_receipt_date(v: str) -> tuple[str, str]:
    """Returns (yyyymmdd_or_empty, classification).

    classification ∈ {"date", "blank", "discontinued", "tbd", "unparseable"}.
    """
    v = clean_text(v)
    low = v.lower()
    if low in BLANK_NRD_VALUES:
        return "", ("tbd" if low == "tbd" else "blank")
    if low in DISCONTINUED_NRD_VALUES:
        return "", "discontinued"
    m = _DATE_RE.match(v)
    if not m:
        return "", "unparseable"
    month_name, day, year = m.group(1).capitalize(), int(m.group(2)), int(m.group(3))
    return f"{year:04d}{MONTHS[month_name]}{day:02d}", "date"


def join_features(spec_row: dict[str, str]) -> str:
    parts = []
    for k in ("Feature1", "Feature2", "Feature3", "Feature4", "Feature5"):
        v = clean_text(spec_row.get(k, ""))
        if v:
            v = v.rstrip(". ")
            parts.append(v + ".")
    return " ".join(parts)


# ---------- Spec master parsing ----------

def load_spec_master(path: Path) -> dict[str, dict[str, str]]:
    _hdr, rows = read_csv(path)
    rows = [r for r in rows if r and r[0] != "Item#"]
    spec: dict[str, dict[str, str]] = {}
    for r in rows:
        bic = r[0].strip()
        if not bic:
            continue
        spec[bic] = {name: (r[idx].strip() if idx < len(r) else "") for name, idx in SPEC_COL.items()}
    return spec


# ---------- Products rebuild ----------

def build_products(poc_path: Path, spec: dict[str, dict[str, str]]) -> tuple[list[str], list[list[str]], dict]:
    hdr, rows = read_csv(poc_path)
    idx = {name: i for i, name in enumerate(hdr)}

    ld_i = idx["LongDesc"]
    cat_i = idx["CategoryCodes"]
    intro_i = idx["IntroDate"]
    bulb_i = idx["BulbIncluded"]
    rel_i = idx["RelatedItems"]
    new_i = idx["NewItem"]

    metrics = {
        "rows_in": len(rows),
        "longdesc_backfilled": 0,
        "longdesc_no_match": 0,
        "introdate_normalized": 0,
        "bulb_normalized": 0,
        "parts_added": 0,
        "related_items_added_on_parents": 0,
    }

    # Pass 1: backfill + clean existing rows.
    for r in rows:
        bic = r[0]
        spec_row = spec.get(bic)

        if not clean_text(r[ld_i]):
            spec_ld = (spec_row or {}).get("LongDesc", "")
            if spec_ld:
                r[ld_i] = truncate_longdesc(spec_ld)
                metrics["longdesc_backfilled"] += 1
            else:
                metrics["longdesc_no_match"] += 1

        new_intro = normalize_intro_date(r[intro_i])
        if new_intro != r[intro_i]:
            metrics["introdate_normalized"] += 1
        r[intro_i] = new_intro

        new_bulb = normalize_bool_y_n(r[bulb_i])
        if new_bulb != r[bulb_i]:
            metrics["bulb_normalized"] += 1
        r[bulb_i] = new_bulb

    # Pass 2: add the 9 missing parts.
    existing_keys = {r[0] for r in rows}
    parts_missing_from_spec = []

    PRODUCTS_FROM_SPEC = [
        "UPCValue", "Subcategory",
        "Feature1", "Feature2", "Feature3", "Feature4", "Feature5",
        "Dimensions", "MaxHeight", "MinHeight", "ChainLength", "WireLength",
        "ExtensionRods", "BackplateDimension", "CanopyDimension", "FinishCode",
        "ShadeMaterial", "ShadeColor", "NumberOfShades", "ShadeDimension",
        "Disclaimer", "BulbType", "NbrBulbs", "TotalWattage", "BulbWattage",
        "TotalLumen", "Kelvin", "CRI", "Dimmable", "Voltage", "Certifications",
        "IPRating", "Rating", "ADA", "LEDHours", "BulbShape", "BulbSocket",
        "BulbIncluded", "SlopeCeilingCompatible", "Direction", "MotionSensor",
        "Materials", "ImageFileName",
    ]
    PRICE_FIELDS = ["Price_cad", "Price_imapcad", "netprice", "Price_imapusd"]

    for sku in PARTS_TO_ADD:
        if sku in existing_keys:
            continue
        s = spec.get(sku)
        if not s:
            parts_missing_from_spec.append(sku)
            continue

        if sku in BELLISSIMA_TUBES_SILVER:
            related = ",".join(BELLISSIMA_PARENTS_SILVER); collection = "BELLISSIMA"
        elif sku in BELLISSIMA_TUBES_BLACK:
            related = ",".join(BELLISSIMA_PARENTS_BLACK); collection = "BELLISSIMA"
        else:
            related = ",".join(ALCAMO_PARENTS); collection = "ALCAMO"

        row = [""] * len(hdr)
        row[idx["BaseItemCode"]] = sku
        row[ld_i] = truncate_longdesc(s["LongDesc"])
        row[idx["CollectionCodes"]] = collection
        row[cat_i] = "Accessory"

        for k in PRODUCTS_FROM_SPEC:
            if k in idx:
                row[idx[k]] = clean_text(s.get(k, ""))

        for k in PRICE_FIELDS:
            if k in idx:
                row[idx[k]] = strip_money(s.get(k, ""))

        if "ShipLBS" in idx:
            row[idx["ShipLBS"]] = clean_text(s.get("ShipLBS", ""))
        if "ShipWeight" in idx:
            row[idx["ShipWeight"]] = strip_weight(s.get("ShipLBS", ""))

        row[idx["TradeNameCode"]] = "Lib & Co"
        for k, default in [("PackedVolume", "1"), ("PackQuantity", "1"), ("MinimumQuantity", "1")]:
            if k in idx:
                row[idx[k]] = default
        row[new_i] = "Y"
        row[rel_i] = related
        row[intro_i] = normalize_intro_date(s.get("IntroDate", ""))
        row[bulb_i] = normalize_bool_y_n(row[bulb_i])

        rows.append(row)
        metrics["parts_added"] += 1

    if parts_missing_from_spec:
        metrics["parts_missing_from_spec"] = parts_missing_from_spec

    # Pass 3: reciprocal RelatedItems on parent fixtures.
    parent_link_map: dict[str, list[str]] = {}
    for p in BELLISSIMA_PARENTS_SILVER:
        parent_link_map[p] = list(BELLISSIMA_TUBES_SILVER)
    for p in BELLISSIMA_PARENTS_BLACK:
        parent_link_map[p] = list(BELLISSIMA_TUBES_BLACK)
    for p in ALCAMO_PARENTS:
        parent_link_map[p] = list(ALCAMO_RODS)

    for r in rows:
        bic = r[0]
        if bic in parent_link_map:
            existing_links = [x.strip() for x in r[rel_i].split(",") if x.strip()]
            for added in parent_link_map[bic]:
                if added not in existing_links:
                    existing_links.append(added)
                    metrics["related_items_added_on_parents"] += 1
            r[rel_i] = ",".join(existing_links)

    # Pass 3b: same fixture family, different finish/size (SORRENTO, Adelfia, etc.).
    backfill_variant_sibling_related_items(rows, idx["BaseItemCode"], rel_i, metrics)

    # Pass 4: universal field scrub - LF/CR cannot appear in product file per KB.
    scrubbed = 0
    for r in rows:
        for i, v in enumerate(r):
            if v and ("\n" in v or "\r" in v):
                r[i] = clean_text(v)
                scrubbed += 1
    metrics["fields_lfcr_scrubbed"] = scrubbed

    metrics["rows_out"] = len(rows)
    return hdr, rows, metrics


# ---------- Force-add products (manual clone + override) ----------

def force_add_products(p_hdr: list[str], p_rows: list[list[str]]) -> dict:
    """Add SKUs that are missing from the product file by cloning an existing
    row and applying overrides. See FORCE_ADD_PRODUCTS for the manifest.
    """
    idx = {name: i for i, name in enumerate(p_hdr)}
    bic_i = idx["BaseItemCode"]
    existing = {r[bic_i] for r in p_rows}

    added: list[str] = []
    skipped: list[tuple[str, str]] = []

    for entry in FORCE_ADD_PRODUCTS:
        sku = entry["sku"]
        clone_from = entry["clone_from"]
        if sku in existing:
            skipped.append((sku, "already in products"))
            continue
        source = next((r for r in p_rows if r[bic_i] == clone_from), None)
        if source is None:
            skipped.append((sku, f"clone source {clone_from} not found"))
            continue
        new_row = list(source)
        new_row[bic_i] = sku
        for field, value in entry["overrides"].items():
            if field in idx:
                new_row[idx[field]] = value
        new_row[idx["LongDesc"]] = truncate_longdesc(new_row[idx["LongDesc"]])
        p_rows.append(new_row)
        added.append(sku)

    return {"added": added, "skipped": skipped}


# ---------- Discontinued promo (25% off + smart-list export) ----------

def apply_discontinued_promo(
    p_hdr: list[str],
    p_rows: list[list[str]],
    discontinued_rows: list[list[str]],
) -> tuple[list[list[str]], list[list[str]], dict]:
    """Apply Silvio's discontinued-sell-through pricing across all 4 price columns.

    Rules (May 28 call):
      - Inventory feed flagged 'Discontinued once sold-out' or 'DISCONTINUED'.
      - SKUs with qty > 0: 25% off on Price_cad, Price_imapcad, netprice, Price_imapusd.
      - SKUs with qty = 0: drop from products entirely (no point in catalog).
      - FORCE_DROP_SKUS (10131-06): drop regardless of qty (sold-per-Silvio).

    Returns:
      - new product rows (with discontinued SKUs discounted, drops removed)
      - smart_list_rows: [BaseItemCode, LongDesc, NewNetPrice_USD, NewPrice_CAD]
        for the "Discontinued - 25% Off" smart list export.
      - metrics dict.
    """
    idx = {name: i for i, name in enumerate(p_hdr)}
    bic_i = idx["BaseItemCode"]
    ld_i = idx["LongDesc"]
    PRICE_FIELDS = ["Price_cad", "Price_imapcad", "netprice", "Price_imapusd"]

    qty_by_sku: dict[str, int] = {}
    for row in discontinued_rows:
        sku = row[0]
        try:
            qty_by_sku[sku] = int(row[2])
        except (ValueError, IndexError, TypeError):
            qty_by_sku[sku] = 0

    drop_zero_stock = {sku for sku, q in qty_by_sku.items() if q == 0}
    drop_set = set(FORCE_DROP_SKUS) | drop_zero_stock

    metrics = {
        "discontinued_in_inventory": len(qty_by_sku),
        "discounted_with_stock": 0,
        "dropped_zero_stock": 0,
        "dropped_force": 0,
        "discontinued_not_in_products": 0,
    }

    new_rows: list[list[str]] = []
    smart_list_rows: list[list[str]] = []
    discounted_skus: list[str] = []

    matched_skus = set()
    for r in p_rows:
        sku = r[bic_i]
        if sku in drop_set:
            matched_skus.add(sku)
            if sku in FORCE_DROP_SKUS:
                metrics["dropped_force"] += 1
            else:
                metrics["dropped_zero_stock"] += 1
            continue

        if sku in qty_by_sku and qty_by_sku[sku] > 0:
            matched_skus.add(sku)
            for field in PRICE_FIELDS:
                if field not in idx:
                    continue
                val = clean_text(r[idx[field]])
                if not val:
                    continue
                try:
                    f = float(val)
                except ValueError:
                    continue
                discounted = f * (1.0 - DISCOUNT_RATE)
                r[idx[field]] = (
                    str(int(discounted)) if discounted.is_integer() else f"{discounted:.2f}"
                )
            smart_list_rows.append([
                sku,
                r[ld_i],
                str(qty_by_sku[sku]),
                clean_text(r[idx["netprice"]]),
                clean_text(r[idx["Price_cad"]]),
                clean_text(r[idx["Price_imapusd"]]),
                clean_text(r[idx["Price_imapcad"]]),
            ])
            discounted_skus.append(sku)
            metrics["discounted_with_stock"] += 1

        new_rows.append(r)

    metrics["discontinued_not_in_products"] = len(
        [s for s in qty_by_sku.keys() if s not in matched_skus]
    )

    smart_list_rows.sort(key=lambda r: r[0])
    metrics["smart_list_skus"] = discounted_skus

    return new_rows, smart_list_rows, metrics


# ---------- Color-variant consistency audit ----------

_SKU_VARIANT_RE = re.compile(r"^(.+)-(\d+)$")


def audit_color_variants(p_hdr: list[str], p_rows: list[list[str]]) -> dict:
    """Backfill fields that should be identical across color variants of the
    same fixture (silver/black/brass, etc.). Triggered by Silvio's May 28 note
    on the Bellissima 3 Light: the matte black variant had 'Metal + Glass' in
    Materials while the silver variant was blank.

    Approach:
      - Group rows by SKU root (everything before the trailing -NN suffix).
      - Skip groups with fewer than 2 variants.
      - For each shared-backfillable field, if some variants have a value and
        others are blank, fill the blanks with the most common value.
      - Color/finish/UPC/image fields are excluded (they legitimately differ).
      - Groups where every variant is blank for a field are reported separately
        so Silvio can decide whether to source from the collection level.
    """
    idx = {name: i for i, name in enumerate(p_hdr)}
    bic_i = idx["BaseItemCode"]

    SHARED_BACKFILLABLE = [
        "CollectionCodes", "CategoryCodes", "Subcategory",
        "Dimensions", "MaxHeight", "MinHeight", "ChainLength", "WireLength",
        "ExtensionRods", "BackplateDimension", "CanopyDimension",
        "ShadeMaterial", "ShadeColor", "NumberOfShades", "ShadeDimension",
        "ShipLBS", "ShipWeight", "BulbType", "NbrBulbs", "TotalWattage",
        "BulbWattage", "TotalLumen", "Kelvin", "CRI", "Dimmable", "Voltage",
        "Certifications", "IPRating", "Rating", "ADA", "LEDHours", "BulbShape",
        "BulbSocket", "BulbIncluded", "SlopeCeilingCompatible", "IntroDate",
        "Direction", "MotionSensor", "Materials", "Disclaimer",
        "TradeNameCode", "PackedVolume", "PackQuantity", "MinimumQuantity",
    ]

    def sku_root(bic: str) -> str | None:
        m = _SKU_VARIANT_RE.match(bic)
        return m.group(1) if m else None

    groups: dict[str, list[int]] = {}
    for i, r in enumerate(p_rows):
        root = sku_root(r[bic_i])
        if root:
            groups.setdefault(root, []).append(i)

    from collections import Counter

    backfills: list[dict[str, str]] = []
    mismatches_flagged: list[dict[str, str]] = []
    all_blank_groups: list[dict[str, str]] = []

    for root, indices in groups.items():
        if len(indices) < 2:
            continue
        for field in SHARED_BACKFILLABLE:
            if field not in idx:
                continue
            col = idx[field]
            values = [(i, clean_text(p_rows[i][col])) for i in indices]
            non_blank = [(i, v) for i, v in values if v]
            blank = [i for i, v in values if not v]

            if not non_blank and len(values) >= 2:
                all_blank_groups.append({"root": root, "field": field, "variants": str(len(values))})
                continue

            if non_blank and blank:
                value_counts = Counter(v for _, v in non_blank)
                mode_value = value_counts.most_common(1)[0][0]
                for bi in blank:
                    p_rows[bi][col] = mode_value
                    backfills.append({
                        "sku": p_rows[bi][bic_i],
                        "root": root,
                        "field": field,
                        "backfilled_with": mode_value,
                    })
                if len(value_counts) > 1:
                    mismatches_flagged.append({
                        "root": root,
                        "field": field,
                        "values": " | ".join(f"{v} ({n})" for v, n in value_counts.most_common()),
                    })

    return {
        "backfills": backfills,
        "mismatches_flagged": mismatches_flagged,
        "all_blank_groups": all_blank_groups,
        "backfills_count": len(backfills),
        "mismatches_count": len(mismatches_flagged),
        "all_blank_count": len(all_blank_groups),
    }


# ---------- Stories rebuild ----------

def _color_variant_key(bic: str) -> str | None:
    """Swap -01 (silver) and -02 (black) sleeve variants. Returns None if not applicable."""
    if bic.endswith("-01"):
        return bic[:-3] + "-02"
    if bic.endswith("-02"):
        return bic[:-3] + "-01"
    return None


def build_stories(spec: dict[str, dict[str, str]], products_keys: set[str]) -> tuple[list[str], list[list[str]], dict]:
    header = ["BaseItemCode", "Productstory"]
    rows: list[list[str]] = []
    metrics = {"with_story": 0, "no_features": 0, "orphan_dropped": 0, "fallback_to_color_variant": 0}

    for bic, s in spec.items():
        if bic not in products_keys:
            metrics["orphan_dropped"] += 1
            continue
        story = join_features(s)
        if not story:
            # Fallback: borrow features from the color-variant SKU (silver <-> black sleeve).
            sibling_key = _color_variant_key(bic)
            sibling = spec.get(sibling_key) if sibling_key else None
            if sibling:
                story = join_features(sibling)
                if story:
                    metrics["fallback_to_color_variant"] += 1
        if not story:
            metrics["no_features"] += 1
            continue
        rows.append([bic, story])
        metrics["with_story"] += 1

    rows.sort(key=lambda r: r[0])
    return header, rows, metrics


# ---------- Inventory rebuild ----------

def build_inventory(
    path: Path, products_keys: set[str]
) -> tuple[list[str], list[list[str]], list[list[str]], list[list[str]], dict]:
    """Returns (header, kept_rows, unmatched_rows, discontinued_rows, metrics).

    NextReceiptDate is parsed into YYYYMMDD (KB requires 8-char date format).
    Free-text values like 'TBD', 'Discontinued once sold-out' are blanked here and surfaced
    via the discontinued_rows export for client follow-up.
    """
    hdr, rows = read_csv(path)
    assert hdr[0] == "BaseItemCode" and hdr[2] == "QtyAvailable", f"unexpected inventory header: {hdr}"

    NOT_NEEDED_I, QA_I, NRD_I = 1, 2, 3
    out_header = ["BaseItemCode", "QtyAvailable", "NextReceiptDate"]
    out_rows: list[list[str]] = []
    unmatched: list[list[str]] = []
    discontinued: list[list[str]] = []
    metrics = {
        "rows_in": len(rows),
        "rows_dropped_secondary_header": 0,
        "rows_unmatched": 0,
        "nrd_parsed_as_date": 0,
        "nrd_blanked_tbd": 0,
        "nrd_blanked_discontinued": 0,
        "nrd_unparseable": 0,
        "rows_out": 0,
    }

    for r in rows:
        bic = r[0].strip()
        qa = (r[QA_I].strip() if QA_I < len(r) else "")
        if not qa.lstrip("-").isdigit():
            metrics["rows_dropped_secondary_header"] += 1
            continue
        nrd_raw = (r[NRD_I].strip() if NRD_I < len(r) else "")
        product_name = (r[NOT_NEEDED_I].strip() if NOT_NEEDED_I < len(r) else "")

        nrd_clean, kind = parse_next_receipt_date(nrd_raw)
        if kind == "date":
            metrics["nrd_parsed_as_date"] += 1
        elif kind == "tbd":
            metrics["nrd_blanked_tbd"] += 1
        elif kind == "discontinued":
            metrics["nrd_blanked_discontinued"] += 1
            discontinued.append([bic, product_name, qa, nrd_raw])
        elif kind == "unparseable":
            metrics["nrd_unparseable"] += 1

        out_rows.append([bic, qa, nrd_clean])
        if bic not in products_keys:
            unmatched.append([bic, product_name, qa])
            metrics["rows_unmatched"] += 1

    metrics["rows_out"] = len(out_rows)
    return out_header, out_rows, unmatched, discontinued, metrics


# ---------- Customers rebuild ----------

def build_customers(path: Path) -> tuple[list[str], list[list[str]], dict]:
    """Build a placeholder-filled customers.csv from Jon's mapped BC export.

    Required-but-blank fields are filled with sentinel placeholders so the file
    will import cleanly. Silvio's BC export already provides the bones (BillToCode,
    BillToName, BillToCountry as 2-letter ISO, TerritoryCodes = salesperson code,
    DefaultPriceCode = BC discount group). We:
      - Map DefaultPriceCode from BC's TIER labels to country-based eCat codes
        (us-wsp / cad-wsp). The original TIER value is preserved in a custom field.
      - Add the eCat-required Bill/Ship address-block placeholders.
      - Sort by BillToCode (KB requirement; required for multi-ship-to grouping).
    """
    hdr, rows = read_csv(path)
    # Drop secondary header row (BC source column labels like "(ADDRESS NEEDED)").
    rows = [r for r in rows if r and r[0].strip() and r[0].strip().lower() != "no."]

    idx = {h: i for i, h in enumerate(hdr)}

    # Append two custom fields to preserve original BC values for traceability.
    out_hdr = list(hdr) + ["BillTo_BCPriceGroup", "BillTo_BCSalesperson"]

    metrics = {
        "rows_in": len(rows),
        "placeholder_state": 0,
        "placeholder_postcode": 0,
        "placeholder_address": 0,
        "placeholder_city": 0,
        "placeholder_country": 0,
        "placeholder_territory": 0,
        "price_code_us_wsp": 0,
        "price_code_cad_wsp": 0,
        "price_code_default_fallback": 0,
        "bc_tier_preserved": 0,
    }

    out_rows: list[list[str]] = []
    for r in rows:
        # Defensive padding to handle short rows.
        r = list(r) + [""] * (len(hdr) - len(r))

        bc_price_group = clean_text(r[idx["DefaultPriceCode"]])
        bc_salesperson = clean_text(r[idx["TerritoryCodes"]])

        country = clean_text(r[idx["BillToCountry"]])
        if not country:
            country = DEFAULT_PLACEHOLDER_COUNTRY
            metrics["placeholder_country"] += 1
        r[idx["BillToCountry"]] = country

        ship_country = clean_text(r[idx["ShipToCountry"]]) or country
        r[idx["ShipToCountry"]] = ship_country

        state_placeholder = PLACEHOLDER_STATE_BY_COUNTRY.get(country, DEFAULT_PLACEHOLDER_STATE)
        ship_state_placeholder = PLACEHOLDER_STATE_BY_COUNTRY.get(ship_country, DEFAULT_PLACEHOLDER_STATE)

        for fld, ph in [
            ("BillToAddress1", PLACEHOLDER_ADDRESS),
            ("ShipToAddress1", PLACEHOLDER_ADDRESS),
            ("BillToCity", PLACEHOLDER_CITY),
            ("ShipToCity", PLACEHOLDER_CITY),
            ("BillToPostCode", PLACEHOLDER_POSTCODE),
            ("ShipToPostCode", PLACEHOLDER_POSTCODE),
        ]:
            if not clean_text(r[idx[fld]]):
                r[idx[fld]] = ph
                if "Address" in fld:
                    metrics["placeholder_address"] += 1
                elif "City" in fld:
                    metrics["placeholder_city"] += 1
                else:
                    metrics["placeholder_postcode"] += 1

        if not clean_text(r[idx["BillToState"]]):
            r[idx["BillToState"]] = state_placeholder
            metrics["placeholder_state"] += 1
        if not clean_text(r[idx["ShipToState"]]):
            r[idx["ShipToState"]] = ship_state_placeholder
            metrics["placeholder_state"] += 1

        if not clean_text(r[idx["TerritoryCodes"]]):
            r[idx["TerritoryCodes"]] = PLACEHOLDER_TERRITORY
            metrics["placeholder_territory"] += 1

        # ShipToName: if blank, mirror BillToName.
        if not clean_text(r[idx["ShipToName"]]):
            r[idx["ShipToName"]] = r[idx["BillToName"]]

        # DefaultPriceCode: route by country, preserve BC tier in custom field.
        price_code = COUNTRY_TO_PRICE_CODE.get(country, DEFAULT_PRICE_CODE)
        r[idx["DefaultPriceCode"]] = price_code
        if price_code == "us-wsp":
            metrics["price_code_us_wsp"] += 1
        elif price_code == "cad-wsp":
            metrics["price_code_cad_wsp"] += 1
        else:
            metrics["price_code_default_fallback"] += 1

        if bc_price_group:
            metrics["bc_tier_preserved"] += 1

        out_rows.append(r + [bc_price_group, bc_salesperson])

    out_rows.sort(key=lambda x: x[idx["BillToCode"]])
    metrics["rows_out"] = len(out_rows)
    return out_hdr, out_rows, metrics


# ---------- User invites rebuild ----------

def _split_name(contact: str) -> tuple[str, str]:
    """'Reed Rosenberg/Scott Rosenberg' -> ('Reed', 'Rosenberg').
    For combined names with '/', take the first person and flag in comments
    via the source rep list. eCat doesn't handle 2 people per user record."""
    contact = clean_text(contact)
    if not contact:
        return "", ""
    primary = contact.split("/")[0].strip()
    parts = primary.split()
    if len(parts) == 0:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])


def build_user_invites(path: Path) -> tuple[list[str], list[list[str]], dict]:
    """Build eCat user-invite CSV from Lib & Co's BC rep list (xlsx file).

    eCat user-import spec: email (required), username, first_name, last_name,
    user_type, territory_codes, customer_number. Lib & Co uses territory-based
    rep visibility (multiple customers per rep), so customer_number is left blank.

    Bundles MX rep with US group because the single MX rep is USD-currency.
    """
    try:
        from openpyxl import load_workbook  # type: ignore
    except ImportError as e:
        raise RuntimeError("openpyxl required to read the rep list xlsx file") from e

    # File is named .csv but is actually xlsx - copy to tmp with right extension first.
    import shutil, tempfile
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        shutil.copyfile(path, tmp.name)
        wb = load_workbook(tmp.name, data_only=True)

    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    hdr = [str(c).strip() if c else "" for c in rows[0]]
    idx = {h: i for i, h in enumerate(hdr)}

    # Strictly the eCat user-import spec columns. Group assignment + phone go
    # into the side reference file (see main() driver).
    out_header = ["email", "username", "first_name", "last_name", "user_type",
                  "territory_codes", "customer_number"]
    ref_header = ["rep_code", "user_group", "first_name", "last_name", "email", "phone", "country"]
    ref_rows: list[list[str]] = []
    out_rows: list[list[str]] = []
    metrics = {
        "rows_in": 0,
        "rows_out": 0,
        "us_group": 0,
        "ca_group": 0,
        "email_corrected": 0,
        "multi_person_collapsed": 0,
        "missing_email": 0,
    }

    for r in rows[1:]:
        if not r or not r[idx["Rep Code"]]:
            continue
        metrics["rows_in"] += 1

        rep_code = clean_text(r[idx["Rep Code"]])
        contact = clean_text(r[idx["Contact"]] or "")
        raw_email = clean_text(r[idx["Email"]] or "")
        country = clean_text(r[idx["Country/Region Code"]] or "")
        phone = clean_text(r[idx["Phone No."]] or "")

        email = REP_EMAIL_OVERRIDES.get(rep_code, raw_email)
        if rep_code in REP_EMAIL_OVERRIDES:
            metrics["email_corrected"] += 1
        elif ";" in email:
            email = email.split(";")[0].strip()
            metrics["email_corrected"] += 1

        if not email:
            metrics["missing_email"] += 1
            continue

        if "/" in contact:
            metrics["multi_person_collapsed"] += 1
        first, last = _split_name(contact)

        group = REP_USER_GROUP_BY_COUNTRY.get(country, "Lib & Co - US Reps")
        if group == "Lib & Co - US Reps":
            metrics["us_group"] += 1
        else:
            metrics["ca_group"] += 1

        out_rows.append([
            email,
            "",                       # username (let eCat default to email prefix)
            first,
            last,
            DEFAULT_USER_TYPE,
            rep_code,                 # territory_codes
            "",                       # customer_number (n/a - using territory model)
        ])
        ref_rows.append([rep_code, group, first, last, email, phone, country])
        metrics["rows_out"] += 1

    # Sort by group then rep code for both outputs.
    pair = list(zip(out_rows, ref_rows))
    pair.sort(key=lambda p: (p[1][1], p[1][0]))
    out_rows = [p[0] for p in pair]
    ref_rows = [p[1] for p in pair]
    return out_header, out_rows, metrics, ref_header, ref_rows


# ---------- Driver ----------

def main() -> None:
    print(f"Reading spec master:    {SPEC_PATH.name}")
    spec = load_spec_master(SPEC_PATH)
    print(f"  spec rows: {len(spec)}")

    print(f"Reading POC products:   {POC_PRODUCTS_PATH.name}")
    p_hdr, p_rows, p_metrics = build_products(POC_PRODUCTS_PATH, spec)

    # Force-add missing SKUs identified during May 28 review (e.g., 10193-02).
    fa_result = force_add_products(p_hdr, p_rows)
    print(f"  force-added: {fa_result['added']}")
    if fa_result["skipped"]:
        print(f"  force-add skipped: {fa_result['skipped']}")

    # Color-variant consistency audit (Silvio's Bellissima Materials note).
    audit_result = audit_color_variants(p_hdr, p_rows)
    print(f"  color-variant backfills: {audit_result['backfills_count']}")
    print(f"  color-variant mismatches flagged: {audit_result['mismatches_count']}")
    print(f"  color-variant all-blank groups (info only): {audit_result['all_blank_count']}")

    # Read inventory next so we can apply the discontinued promo before
    # finalizing products.csv. Inventory matching uses post-force-add keys.
    products_keys_pre_promo = {r[0] for r in p_rows}

    print(f"Reading inventory:      {INVENTORY_PATH.name}")
    i_hdr, i_rows, i_unmatched, i_discontinued, i_metrics = build_inventory(
        INVENTORY_PATH, products_keys_pre_promo
    )

    # Apply 25% off discontinued-sell-through pricing (Silvio May 28 directive).
    p_rows, smart_list_rows, promo_metrics = apply_discontinued_promo(
        p_hdr, p_rows, i_discontinued
    )
    print(f"  promo discounted (qty>0): {promo_metrics['discounted_with_stock']}")
    print(f"  promo dropped zero-stock: {promo_metrics['dropped_zero_stock']}")
    print(f"  promo dropped force list: {promo_metrics['dropped_force']}")

    # Final products write (after force-add, audit, promo).
    out_products = OUTDIR / "products.csv"
    out_p_hdr, out_p_rows = finalize_product_output(p_hdr, p_rows)
    write_csv(out_products, out_p_hdr, out_p_rows)
    print(f"  -> {out_products}")
    for k, v in p_metrics.items():
        print(f"     {k}: {v}")

    # Color-variant audit detail dump (for Silvio spot-check).
    out_audit = OUTDIR / "color_variant_audit.csv"
    with open(out_audit, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["change_type", "sku", "root", "field", "value_or_summary"])
        for b in audit_result["backfills"]:
            w.writerow(["backfilled", b["sku"], b["root"], b["field"], b["backfilled_with"]])
        for m in audit_result["mismatches_flagged"]:
            w.writerow(["mismatch_flagged", "", m["root"], m["field"], m["values"]])
        for g in audit_result["all_blank_groups"]:
            w.writerow(["all_variants_blank", "", g["root"], g["field"], f"{g['variants']} variants"])
    print(f"  -> {out_audit}")

    # Smart-list export for the Discontinued - 25% Off list.
    out_smart = OUTDIR / "smart_list_discontinued_25off.csv"
    write_csv(
        out_smart,
        [
            "BaseItemCode", "LongDesc", "QtyAvailable",
            "NetPrice_USD_25off", "Price_CAD_25off",
            "Price_IMAP_USD_25off", "Price_IMAP_CAD_25off",
        ],
        smart_list_rows,
    )
    print(f"  -> {out_smart} ({len(smart_list_rows)} SKUs)")

    # Comma-separated SKU paste-ready string for the admin Smart List creator.
    out_smart_paste = OUTDIR / "smart_list_discontinued_25off_skus.txt"
    out_smart_paste.write_text(",".join([r[0] for r in smart_list_rows]) + "\n", encoding="utf-8")
    print(f"  -> {out_smart_paste}")

    products_keys = {r[0] for r in p_rows}

    print("Building stories from spec master Feature 1-5...")
    s_hdr, s_rows, s_metrics = build_stories(spec, products_keys)
    out_stories = OUTDIR / "stories.csv"
    write_csv(out_stories, s_hdr, s_rows)
    print(f"  -> {out_stories}")
    for k, v in s_metrics.items():
        print(f"     {k}: {v}")

    out_inventory = OUTDIR / "inventory.csv"
    write_csv(out_inventory, i_hdr, i_rows)
    print(f"  -> {out_inventory}")
    for k, v in i_metrics.items():
        print(f"     {k}: {v}")

    out_unmatched = OUTDIR / "unmatched_inventory.csv"
    write_csv(out_unmatched, ["BaseItemCode", "ProductName_from_inventory_feed", "QtyAvailable"], i_unmatched)
    print(f"  -> {out_unmatched} ({len(i_unmatched)} rows)")

    out_disc = OUTDIR / "discontinued_skus.csv"
    write_csv(
        out_disc,
        ["BaseItemCode", "ProductName_from_inventory_feed", "QtyAvailable", "NextReceiptDate_raw"],
        i_discontinued,
    )
    print(f"  -> {out_disc} ({len(i_discontinued)} rows)")

    if CUSTOMERS_PATH.exists():
        print(f"Reading customers:      {CUSTOMERS_PATH.name}")
        c_hdr, c_rows, c_metrics = build_customers(CUSTOMERS_PATH)
        out_customers = OUTDIR / "customers.csv"
        write_csv(out_customers, c_hdr, c_rows)
        print(f"  -> {out_customers}")
        for k, v in c_metrics.items():
            print(f"     {k}: {v}")
    else:
        print(f"Customers source not found ({CUSTOMERS_PATH.name}); preserving previous output/customers.csv")
        c_metrics = {"skipped": "source file missing - using previous output/customers.csv as-is"}

    print(f"Reading rep list:       {REP_LIST_PATH.name}")
    u_hdr, u_rows, u_metrics, ref_hdr, ref_rows = build_user_invites(REP_LIST_PATH)
    out_users = OUTDIR / "user_invites.csv"
    write_csv(out_users, u_hdr, u_rows)
    print(f"  -> {out_users}")
    out_users_ref = OUTDIR / "user_invites_groups_reference.csv"
    write_csv(out_users_ref, ref_hdr, ref_rows)
    print(f"  -> {out_users_ref}")
    for k, v in u_metrics.items():
        print(f"     {k}: {v}")

    report = OUTDIR / "rebuild_report.txt"
    with open(report, "w", encoding="utf-8") as f:
        f.write("Lib & Co. eCat core-file rebuild report\n")
        f.write("=" * 60 + "\n\n")
        f.write("Inputs:\n")
        f.write(f"  - {SPEC_PATH.name}\n")
        f.write(f"  - {POC_PRODUCTS_PATH.name}\n")
        f.write(f"  - {INVENTORY_PATH.name}\n\n")
        f.write("Products:\n")
        for k, v in p_metrics.items():
            f.write(f"  {k}: {v}\n")
        f.write("\nForce-Added Products (manual clone + override):\n")
        f.write(f"  added: {fa_result['added']}\n")
        f.write(f"  skipped: {fa_result['skipped']}\n")
        f.write("\nColor-Variant Consistency Audit:\n")
        f.write(f"  backfills_applied: {audit_result['backfills_count']}\n")
        f.write(f"  mismatches_flagged: {audit_result['mismatches_count']}\n")
        f.write(f"  all_variants_blank_groups: {audit_result['all_blank_count']}\n")
        f.write(f"  detail: see color_variant_audit.csv\n")
        f.write("\nDiscontinued Promo (25% off):\n")
        for k, v in promo_metrics.items():
            if k == "smart_list_skus":
                f.write(f"  smart_list_skus_count: {len(v)}\n")
            else:
                f.write(f"  {k}: {v}\n")
        f.write(f"  smart_list_csv: smart_list_discontinued_25off.csv\n")
        f.write(f"  smart_list_paste_string: smart_list_discontinued_25off_skus.txt\n")
        f.write("\nStories:\n")
        for k, v in s_metrics.items():
            f.write(f"  {k}: {v}\n")
        f.write("\nInventory:\n")
        for k, v in i_metrics.items():
            f.write(f"  {k}: {v}\n")
        f.write(f"  unmatched_csv: {out_unmatched.name}\n")
        f.write(f"  discontinued_csv: {out_disc.name}\n")
        f.write("\nCustomers:\n")
        for k, v in c_metrics.items():
            f.write(f"  {k}: {v}\n")
        f.write("\nUser Invites:\n")
        for k, v in u_metrics.items():
            f.write(f"  {k}: {v}\n")
    print(f"  -> {report}")


if __name__ == "__main__":
    main()
