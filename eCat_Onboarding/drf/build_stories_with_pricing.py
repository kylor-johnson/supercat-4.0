#!/usr/bin/env python3
"""
Build stories.csv for Dorell Fabrics (org: drf) with embedded pricing tables.

Reads:
  - products.csv          → BaseItemCode + all Price_* columns
  - stories.csv.20260703-0215.csv → existing story text

Outputs:
  - stories.csv           → ready-to-import file with story + plain-text pricing

The iPad renders stories via NSAttributedString (plain text, not HTML).
The SuperCat CSV importer pipeline:
  1. dos2unix -c mac converts standalone \r → \n
  2. cleancsv collapses multi-line quoted fields (replaces \n inside quotes with space)
  3. FileReader.each_line reads line-by-line on \n

So \r and \n both get flattened. We use U+2028 (LINE SEPARATOR) instead:
  - dos2unix does NOT touch it (only handles \r and \r\n)
  - cleancsv does NOT touch it (only handles \n within quotes)
  - iOS UITextView/NSAttributedString renders U+2028 as a visual line break

Rules:
  - Products WITH pricing: story text + \r\r + formatted pricing block
  - Products WITHOUT pricing (all 10 levels = 0): story text only
  - Products with no story AND no pricing: omitted entirely
  - Orphan stories (no matching product row): dropped
  - Prices formatted with currency symbols: $ (USD), ¥ (CNY), CA$ (CAD)
  - Zero-valued individual levels within a priced product are omitted
"""

import csv
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

PRODUCTS_FILE = SCRIPT_DIR / "products.csv"
STORIES_FILE = SCRIPT_DIR / "stories.csv.20260703-0215.csv"
OUTPUT_FILE = SCRIPT_DIR / "stories.csv"

LSEP = "\u2028"

PRICE_LEVELS = [
    ("List",    "List",      "$",   ""),
    ("MFR",     "MFR",       "$",   ""),
    ("WHS",     "WHS",       "$",   ""),
    ("FOBList", "FOB List",  "$",   ""),
    ("FOBLow",  "FOB Low",   "$",   ""),
    ("C2CList", "C2C List",  "¥",   ""),
    ("C2CLow",  "C2C Low",   "¥",   ""),
    ("CAList",  "CA List",   "CA$", ""),
    ("CALow",   "CA Low",    "CA$", ""),
    ("Retail",  "Retail",    "$",   ""),
]

def format_price(value: float, prefix: str) -> str:
    return f"{prefix}{value:,.2f}"


def build_pricing_text(prices: dict) -> str:
    """Build plain-text pricing block using U+2028 for line breaks."""
    usd_line = []
    fob_line = []
    c2c_line = []
    ca_line = []

    for code, label, currency_prefix, _ in PRICE_LEVELS:
        val = prices.get(code, 0.0)
        if val <= 0:
            continue
        formatted = format_price(val, currency_prefix)
        entry = f"{label}: {formatted}"

        if code in ("List", "MFR", "WHS", "Retail"):
            usd_line.append(entry)
        elif code in ("FOBList", "FOBLow"):
            fob_line.append(entry)
        elif code in ("C2CList", "C2CLow"):
            c2c_line.append(entry)
        elif code in ("CAList", "CALow"):
            ca_line.append(entry)

    lines = []
    for group in [usd_line, fob_line, c2c_line, ca_line]:
        if group:
            lines.append(" | ".join(group))

    if not lines:
        return ""

    return LSEP.join(lines)


def main():
    # 1. Load existing stories
    existing_stories = {}
    with open(STORIES_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            bic = row["baseitemcode"].strip()
            story = row["productstory"].strip()
            existing_stories[bic] = story

    # 2. Load products + prices
    products = {}
    with open(PRODUCTS_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            bic = row["BaseItemCode"].strip()
            prices = {}
            for code, _, _, _ in PRICE_LEVELS:
                col = f"Price_{code}"
                try:
                    prices[code] = float(row.get(col, 0) or 0)
                except ValueError:
                    prices[code] = 0.0
            products[bic] = prices

    # 3. Build output rows
    output_rows = []
    stats = {
        "story_and_pricing": 0,
        "story_only": 0,
        "pricing_only": 0,
        "orphan_dropped": 0,
        "no_content_skipped": 0,
    }

    all_bics = set(list(products.keys()) + list(existing_stories.keys()))

    for bic in sorted(all_bics):
        has_product = bic in products
        has_story = bic in existing_stories and existing_stories[bic]

        if not has_product:
            stats["orphan_dropped"] += 1
            continue

        prices = products[bic]
        has_pricing = any(v > 0 for v in prices.values())

        if not has_story and not has_pricing:
            stats["no_content_skipped"] += 1
            continue

        story_text = existing_stories.get(bic, "").strip() if has_story else ""
        pricing_block = build_pricing_text(prices) if has_pricing else ""

        if story_text and pricing_block:
            combined = f"{story_text}{LSEP}{LSEP}{pricing_block}"
            stats["story_and_pricing"] += 1
        elif story_text:
            combined = story_text
            stats["story_only"] += 1
        else:
            combined = pricing_block
            stats["pricing_only"] += 1

        output_rows.append((bic, combined))

    # 4. Write output — U+2028 is multi-byte UTF-8 (E2 80 A8), safe in any CSV mode
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["BaseItemCode", "ProductStory"])
        for bic, story in output_rows:
            writer.writerow([bic, story])

    with open(OUTPUT_FILE, "rb") as f:
        csv_bytes = f.read()

    # 5a. Verify byte-level structure
    lsep_bytes = "\u2028".encode("utf-8")  # E2 80 A8
    lsep_count = csv_bytes.count(lsep_bytes)
    lf_count = csv_bytes.count(b"\n")
    cr_count = csv_bytes.count(b"\r")
    print(f"\nByte-level check:")
    print(f"  \\n (CSV row endings): {lf_count}")
    print(f"  U+2028 (in-story line breaks): {lsep_count}")
    print(f"  \\r (should be 0): {cr_count}")

    # 6. Report
    print(f"Output: {OUTPUT_FILE}")
    print(f"Total rows written: {len(output_rows)}")
    print(f"  Story + pricing:  {stats['story_and_pricing']}")
    print(f"  Story only:       {stats['story_only']}")
    print(f"  Pricing only:     {stats['pricing_only']}")
    print(f"  Orphans dropped:  {stats['orphan_dropped']}")
    print(f"  No content skip:  {stats['no_content_skipped']}")

    # 7. List products with no pricing (for email flagging)
    no_pricing_items = []
    for bic in sorted(products.keys()):
        prices = products[bic]
        if all(v == 0 for v in prices.values()):
            no_pricing_items.append(bic)

    print(f"\n--- Products with ALL prices = 0 ({len(no_pricing_items)}) ---")
    for bic in no_pricing_items:
        print(f"  {bic}")


if __name__ == "__main__":
    main()
