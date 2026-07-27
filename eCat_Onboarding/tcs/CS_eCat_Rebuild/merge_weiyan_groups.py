#!/usr/bin/env python3
"""Merge option_groups_audit_fix.csv into option_groups.csv and fill gaps.

Appends non-colliding rows from audit_fix (WA/DEC/ELE/WM Weiyan groups).
Builds WA052-WA062 and DEC050-DEC052 from Weiyan TSW codes + existing W/D groups.
Does NOT overwrite existing main groups (202 CM/WM/etc collisions are skipped).

Run after sync_from_source.py if that script dropped Weiyan groups again.
"""
from __future__ import annotations

import csv
import re
import shutil
from pathlib import Path

BASE = Path(__file__).parent
MAIN = BASE / "option_groups.csv"
FIX = BASE / "option_groups_audit_fix.csv"
WEIYAN = BASE.parent / "Source Data" / "Weiyan LED-Table 1.csv"
PRODUCTS = BASE / "products.csv"
FIELDNAMES = ["Code", "Name", "Options", "PriceAddend", "PriceFactor"]

MISSING_WA = {
    "WA052": "MV25W",
    "WA053": "MV30W",
    "WA054": "OA20W",
    "WA055": "OA25W",
    "WA056": "OA33W",
    "WA057": "PH20W",
    "WA058": "PH22W",
    "WA059": "PH29W",
    "WA060": "SO20W",
    "WA061": "SO22W",
    "WA062": "SO26W",
}
MISSING_DEC = {
    "DEC050": "D028",
    "DEC051": "D029",
    "DEC052": "D030",
}
TRAVELER_NO_WA = ("TR19W", "TR25W", "TR31W")


def load_rows(path: Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def tsw_lookup(main_rows: list[dict[str, str]]) -> dict[str, str]:
    """Map TSW code -> richest W-group Options string from source-sync groups."""
    out: dict[str, tuple[int, str]] = {}
    for row in main_rows:
        code = row["Code"].strip()
        if not code.startswith("W"):
            continue
        opts = row["Options"]
        m = re.match(r"^TSW(\d+)", opts.replace('"', ""))
        if not m:
            continue
        tsw = f"TSW{m.group(1)}"
        if tsw not in out or len(opts) > out[tsw][0]:
            out[tsw] = (len(opts), opts)
    return {k: v[1] for k, v in out.items()}


def weiyan_tsw_by_sku() -> dict[str, str]:
    with open(WEIYAN, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    fill, hdr, data = rows[0], rows[1], rows[2:]
    sku_idx = hdr.index("SKU")
    wa_idx = next(i for i, label in enumerate(fill) if "WALL ACCESSORIES" in label.upper())
    out: dict[str, str] = {}
    for row in data:
        sku = row[sku_idx].strip()
        if wa_idx < len(row):
            val = row[wa_idx].strip()
            if val and val != "----":
                out[sku] = val
    return out


def merge() -> int:
    main_rows = load_rows(MAIN)
    merged = {r["Code"].strip(): r for r in main_rows}
    appended = 0

    for row in load_rows(FIX):
        code = row["Code"].strip()
        if code not in merged:
            merged[code] = {k: row.get(k, "") for k in FIELDNAMES}
            appended += 1

    tsw_map = tsw_lookup(main_rows)
    sku_tsw = weiyan_tsw_by_sku()
    extra = 0

    for wa_code, sku in MISSING_WA.items():
        if wa_code in merged:
            continue
        tsw = sku_tsw.get(sku)
        opts = tsw_map.get(tsw or "")
        if not opts:
            print(f"WARN: cannot build {wa_code} ({sku}, tsw={tsw})")
            continue
        merged[wa_code] = {
            "Code": wa_code,
            "Name": f"Wall Accessories {wa_code[2:]}",
            "Options": opts,
            "PriceAddend": "",
            "PriceFactor": "",
        }
        extra += 1

    for dec_code, src in MISSING_DEC.items():
        if dec_code in merged:
            continue
        src_row = merged.get(src)
        if not src_row:
            print(f"WARN: cannot build {dec_code} (missing {src})")
            continue
        merged[dec_code] = {
            "Code": dec_code,
            "Name": f"Decorative {dec_code[3:]}",
            "Options": src_row["Options"],
            "PriceAddend": "",
            "PriceFactor": "",
        }
        extra += 1

    main_order = [r["Code"].strip() for r in main_rows]
    ordered = [merged[c] for c in main_order]
    for code in sorted(merged):
        if code not in main_order:
            ordered.append(merged[code])

    shutil.copy(MAIN, MAIN.with_suffix(".csv.pre_merge_bak"))
    with open(MAIN, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        w.writerows(ordered)

    print(f"Merged {len(ordered)} groups (+{appended} from audit_fix, +{extra} built)")
    return len(ordered)


def fix_traveler_products() -> int:
    with open(PRODUCTS, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)
    fixed = 0
    for row in rows:
        if row["BaseItemCode"] in TRAVELER_NO_WA and (row.get("OptionSet3") or "").startswith("WA06"):
            row["OptionSet3"] = ""
            fixed += 1
    if fixed:
        shutil.copy(PRODUCTS, PRODUCTS.with_suffix(".csv.pre_tr_fix_bak"))
        with open(PRODUCTS, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
    return fixed


if __name__ == "__main__":
    merge()
    n = fix_traveler_products()
    if n:
        print(f"Cleared bogus OptionSet3 on {n} Traveler SKUs")
