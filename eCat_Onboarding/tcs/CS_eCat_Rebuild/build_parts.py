#!/usr/bin/env python3
"""Add 234 replacement-part SKUs and link via RelatedItems3 / Parts tab (Step 4)."""
from __future__ import annotations

import csv
import re
import shutil
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent
SRC = BASE.parent / "Source Data"
PARTS_SRC = SRC / "Parts-Table 1.csv"
PRODUCTS = BASE / "products.csv"
STORIES = BASE / "stories.csv"

GLASS_PREFIXES = ("SRG", "HRG", "RG")
ACCESSORY_SKUS = {
    "WGS", "WGL", "GLC", "FB1", "FB12V", "FBBM1", "ADS", "CSHI", "HSI1", "HSI2",
    "TLA", "703001", "703002", "LL-TUBE6", "LL-TUBE8",
    "16WST", "16WSTH", "9WST", "9WSTH",
}


def part_match_keys(sku: str) -> set[str]:
    rest = sku
    for prefix in GLASS_PREFIXES:
        if rest.startswith(prefix):
            rest = rest[len(prefix) :]
            break
    keys: set[str] = set()
    if "/" in rest:
        for seg in rest.split("/"):
            seg = re.sub(r"[A-Z]$", "", seg)
            m = re.match(r"^([A-Z]{2,4})(\d{2,3})", seg)
            if m:
                keys.add(f"{m.group(1)}{m.group(2)}")
        return keys
    m = re.match(r"^D([A-Z]{2,4})(\d{2,3})", rest)
    if m:
        keys.add(f"{m.group(1)}{m.group(2)}")
        return keys
    m = re.match(r"^([A-Z]{2,4})(\d{2,3})([BT])?$", rest)
    if m:
        keys.add(f"{m.group(1)}{m.group(2)}")
        return keys
    m = re.match(r"^(\d{2,3})$", rest)
    if m:
        keys.add(f"size_{m.group(1)}")
    return keys


def lantern_match_keys(sku: str) -> set[str]:
    keys: set[str] = set()
    m = re.match(r"^([A-Z]{2,4})(\d{2,3})([EGW])?$", sku)
    if m:
        keys.add(f"{m.group(1)}{m.group(2)}")
        keys.add(f"size_{m.group(2)}")
    m = re.match(r"^([A-Z]{2})(\d{2})-", sku)
    if m:
        keys.add(f"{m.group(1)}{m.group(2)}")
        keys.add(f"size_{m.group(2)}")
    return keys


def is_lantern(sku: str) -> bool:
    if sku in ACCESSORY_SKUS:
        return False
    if sku.endswith("KIT") or "-CPKIT" in sku or "-SMKIT" in sku:
        return False
    return bool(lantern_match_keys(sku))


def load_parts() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with open(PARTS_SRC, newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if not row or not row[0].strip():
                continue
            sku = row[0].strip()
            if sku in ("Accessory SKU", "Master Accessory Index 2026"):
                continue
            rows.append({
                "sku": sku,
                "name": row[2].strip() if len(row) > 2 else sku,
                "gtin": row[3].strip() if len(row) > 3 else "",
                "net": row[5].strip() if len(row) > 5 else "",
                "map": row[6].strip() if len(row) > 6 else "",
                "msrp": row[7].strip() if len(row) > 7 else "",
                "image": row[9].strip() if len(row) > 9 else "",
            })
    return rows


def merge_related(existing: str, add: list[str]) -> str:
    seen: list[str] = []
    for code in (existing or "").split(","):
        code = code.strip()
        if code and code not in seen:
            seen.append(code)
    for code in sorted(add):
        if code not in seen:
            seen.append(code)
    return ",".join(seen)


def ensure_fields(fields: list[str]) -> list[str]:
    for col in ("RelatedItems3TabName", "RelatedItems3"):
        if col not in fields:
            insert_at = fields.index("RelatedItems2") + 1 if "RelatedItems2" in fields else len(fields)
            fields.insert(insert_at + (1 if col == "RelatedItems3" else 0), col)
    return fields


def build() -> None:
    parts = load_parts()

    with open(PRODUCTS, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = ensure_fields(list(reader.fieldnames or []))
        rows = list(reader)

    lanterns = [r["BaseItemCode"].strip() for r in rows if is_lantern(r["BaseItemCode"].strip())]
    lantern_set = set(lanterns)

    part_to_lanterns: dict[str, list[str]] = defaultdict(list)
    for part in parts:
        pkeys = part_match_keys(part["sku"])
        if not pkeys:
            continue
        for lan in lanterns:
            if pkeys & lantern_match_keys(lan):
                part_to_lanterns[part["sku"]].append(lan)

    lantern_to_parts: dict[str, list[str]] = defaultdict(list)
    for part_sku, lans in part_to_lanterns.items():
        for lan in lans:
            lantern_to_parts[lan].append(part_sku)

    existing = {r["BaseItemCode"].strip() for r in rows}
    new_part_rows: list[dict[str, str]] = []
    stories: list[tuple[str, str]] = []

    template = {k: "" for k in fields}
    for part in parts:
        sku = part["sku"]
        row = dict(template)
        row.update({
            "BaseItemCode": sku,
            "LongDesc": part["name"][:50],
            "ShortDesc": part["name"][:15],
            "TradeNameCode": "The CopperSmith",
            "CollectionCodes": "Accessories",
            "CategoryCodes": "Parts",
            "Hideable": "Y",
            "RelatedItems": sku,
            "materials": "",
            "dimensions": "",
            "UPCValue": part["gtin"] if part.get("gtin") and part["gtin"] not in ("----",) else "",
            "ImageFileName": part.get("image", "") if (part.get("image") or "").startswith("http") else "",
            "NetPrice": part["net"],
            "Price_MAP": part["map"],
            "Price_MSRP": part["msrp"],
        })
        new_part_rows.append(row)
        stories.append((sku, part["name"]))

    linked = 0
    for row in rows:
        sku = row["BaseItemCode"].strip()
        if sku in lantern_to_parts:
            row["RelatedItems3TabName"] = "Parts"
            row["RelatedItems3"] = merge_related(row.get("RelatedItems3", ""), lantern_to_parts[sku])
            linked += 1

    new_skus = [r for r in new_part_rows if r["BaseItemCode"] not in existing]
    rows.extend(new_skus)

    shutil.copy(PRODUCTS, PRODUCTS.with_suffix(".csv.pre_parts_bak"))
    with open(PRODUCTS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    with open(STORIES, newline="", encoding="utf-8-sig") as f:
        sreader = csv.DictReader(f)
        sfields = sreader.fieldnames or ["BaseItemCode", "ProductStory"]
        srows = list(sreader)
    story_existing = {r["BaseItemCode"].strip() for r in srows}
    added_stories = 0
    for sku, story in stories:
        if sku not in story_existing:
            srows.append({"BaseItemCode": sku, "ProductStory": story})
            added_stories += 1

    shutil.copy(STORIES, STORIES.with_suffix(".csv.pre_parts_bak"))
    with open(STORIES, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=sfields)
        w.writeheader()
        w.writerows(srows)

    unmatched = [p["sku"] for p in parts if not part_to_lanterns[p["sku"]]]
    print(f"Added {len(new_skus)} part product rows")
    print(f"Linked Parts tab on {linked} lantern SKUs")
    print(f"Added {added_stories} part story rows")
    print(f"Parts with no lantern match ({len(unmatched)}): {unmatched}")
    print(f"products.csv total rows: {len(rows)}")


if __name__ == "__main__":
    build()
