#!/usr/bin/env python3
"""One-shot Lib & Co output updates (Jun 15):
  1. customers.csv — price codes, row filters, strip extra columns
  2. inventory.csv — full rebuild from Silvio Jun 3 xlsx feed
  3. products.csv — drop sold-out discontinued SKUs (smart list sync later)
  4. stories.csv — drop story rows for removed product SKUs
"""
from __future__ import annotations

import csv
import re
from datetime import date, datetime
from pathlib import Path

import openpyxl

OUT = Path(__file__).parent / "output"
JUN3_XLSX = Path("/Users/kylorjohnson/Downloads/Discontonued Inventory - 06.03.2026 (1).xlsx")

REMOVE8 = {
    "C00042", "C00074", "C00078", "C00082", "C00145", "C00151", "C00152", "C00478",
}
PRICE_MAP = {"cad-wsp": "cad", "us-wsp": "netprice"}
DROP_EXTRA_COLS = {"BillTo_BCPriceGroup", "BillTo_BCSalesperson"}

MONTHS = {m: f"{i:02d}" for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June",
     "July", "August", "September", "October", "November", "December"], start=1)}

DATE_RE = re.compile(
    r"^(January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+(\d{1,2})(?:st|nd|rd|th)?,?\s*(\d{4})$",
    re.IGNORECASE,
)
DISCONTINUED_NRD = {"discontinued", "discontinued once sold-out"}
BLANK_NRD = {"tbd", "restock date", ""}
TODAY = date(2026, 6, 15)


def parse_nrd(raw: str) -> tuple[str, str]:
    v = (raw or "").strip()
    low = v.lower()
    if low in BLANK_NRD:
        return "", "blank"
    if low in DISCONTINUED_NRD or "discontinued" in low:
        return "", "discontinued"
    m = DATE_RE.match(v)
    if not m:
        return "", "unparseable"
    month = m.group(1).capitalize()
    day = int(m.group(2))
    year = int(m.group(3))
    d = date(year, int(MONTHS[month]), day)
    if d < TODAY:
        return "", "past"
    return d.strftime("%Y-%m-%d"), "date"


def load_jun3_inventory() -> dict[str, tuple[int, str, str]]:
    wb = openpyxl.load_workbook(JUN3_XLSX, read_only=True, data_only=True)
    ws = wb["Inventory Feed"]
    all_rows = list(ws.iter_rows(values_only=True))
    hdr_i = next(i for i, r in enumerate(all_rows) if r and str(r[0]).strip() == "Item No.")
    out: dict[str, tuple[int, str, str]] = {}
    for r in all_rows[hdr_i + 1 :]:
        if not r or r[0] is None:
            continue
        sku = str(r[0]).strip()
        name = str(r[1]).strip() if r[1] else ""
        try:
            qty = int(float(r[2])) if r[2] not in (None, "") else 0
        except (TypeError, ValueError):
            qty = 0
        nrd_raw = str(r[3]).strip() if len(r) > 3 and r[3] is not None else ""
        out[sku] = (qty, nrd_raw, name)
    return out


def sold_out_disc_skus(jun3: dict[str, tuple[int, str, str]]) -> set[str]:
    smart_path = OUT / "smart_list_discontinued_25off.csv"
    with open(smart_path, newline="", encoding="utf-8") as f:
        smart = {r["BaseItemCode"] for r in csv.DictReader(f)}
    instock_disc = {
        sku for sku, (qty, nrd_raw, _) in jun3.items()
        if qty > 0 and "discontinued" in nrd_raw.lower()
    }
    return smart - instock_disc


def fix_customers() -> dict:
    path = OUT / "customers.csv"
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = rows[0].keys() if rows else []

    kept, dropped8, dropped_pending, price_fixed = [], 0, 0, 0
    for r in rows:
        code = r["BillToCode"].strip()
        tier = (r.get("BillTo_BCPriceGroup") or "").strip().upper()
        if code in REMOVE8:
            dropped8 += 1
            continue
        if tier == "PENDING":
            dropped_pending += 1
            continue
        pc = r["DefaultPriceCode"].strip()
        if pc in PRICE_MAP:
            r["DefaultPriceCode"] = PRICE_MAP[pc]
            price_fixed += 1
        for col in DROP_EXTRA_COLS:
            r.pop(col, None)
        kept.append(r)

    out_fields = [c for c in fieldnames if c not in DROP_EXTRA_COLS]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=out_fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(kept)

    return {
        "rows_in": len(rows),
        "rows_out": len(kept),
        "dropped_remove8": dropped8,
        "dropped_pending": dropped_pending,
        "price_codes_fixed": price_fixed,
    }


def fix_products(drop_skus: set[str]) -> dict:
    path = OUT / "products.csv"
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        kept = [r for r in reader if r["BaseItemCode"] not in drop_skus]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(kept)
    return {"rows_in": len(kept) + len(drop_skus), "rows_out": len(kept), "dropped": sorted(drop_skus)}


def fix_stories(drop_skus: set[str]) -> dict:
    path = OUT / "stories.csv"
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    kept = [r for r in rows if r["BaseItemCode"] not in drop_skus]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(kept)
    return {"rows_in": len(rows), "rows_out": len(kept), "dropped": len(rows) - len(kept)}


def rebuild_inventory(product_keys: set[str], jun3: dict[str, tuple[int, str, str]]) -> dict:
    metrics = {
        "rows_in": len(jun3),
        "rows_out": 0,
        "nrd_date": 0,
        "nrd_blank": 0,
        "nrd_discontinued": 0,
        "nrd_past_blanked": 0,
        "nrd_unparseable": 0,
        "unmatched": 0,
    }
    out_rows: list[list[str]] = []
    unmatched: list[list[str]] = []
    discontinued: list[list[str]] = []

    for sku in sorted(jun3.keys()):
        qty, nrd_raw, name = jun3[sku]
        nrd_clean, kind = parse_nrd(nrd_raw)
        if kind == "date":
            metrics["nrd_date"] += 1
        elif kind == "discontinued":
            metrics["nrd_discontinued"] += 1
            discontinued.append([sku, name, str(qty), nrd_raw])
        elif kind == "past":
            metrics["nrd_past_blanked"] += 1
        elif kind == "unparseable" and nrd_raw:
            metrics["nrd_unparseable"] += 1
        else:
            metrics["nrd_blank"] += 1
        out_rows.append([sku, str(qty), nrd_clean])
        if sku not in product_keys:
            unmatched.append([sku, name, str(qty)])

    inv_path = OUT / "inventory.csv"
    with open(inv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["BaseItemCode", "QtyAvailable", "NextReceiptDate"])
        w.writerows(out_rows)

    um_path = OUT / "unmatched_inventory.csv"
    with open(um_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["BaseItemCode", "ProductName_from_inventory_feed", "QtyAvailable"])
        w.writerows(unmatched)

    disc_path = OUT / "discontinued_skus.csv"
    with open(disc_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["BaseItemCode", "ProductName", "QtyAvailable", "RestockDate_raw"])
        w.writerows(discontinued)

    metrics["rows_out"] = len(out_rows)
    metrics["unmatched"] = len(unmatched)
    return metrics


def main() -> None:
    jun3 = load_jun3_inventory()
    drop_skus = sold_out_disc_skus(jun3)

    cust = fix_customers()
    prod = fix_products(drop_skus)
    product_keys = set()
    with open(OUT / "products.csv", newline="", encoding="utf-8") as f:
        product_keys = {r["BaseItemCode"] for r in csv.DictReader(f)}
    stories = fix_stories(drop_skus)
    inv = rebuild_inventory(product_keys, jun3)

    report = OUT / "jun15_apply_report.txt"
    lines = [
        "Lib & Co — Jun 15 apply report",
        "=" * 50,
        "",
        "CUSTOMERS",
        *(f"  {k}: {v}" for k, v in cust.items()),
        "",
        "PRODUCTS (sold-out discontinued removed)",
        f"  rows_in: {prod['rows_in']}",
        f"  rows_out: {prod['rows_out']}",
        f"  dropped_count: {len(prod['dropped'])}",
        "",
        "STORIES (orphans removed)",
        *(f"  {k}: {v}" for k, v in stories.items()),
        "",
        "INVENTORY (Jun 3 xlsx rebuild)",
        *(f"  {k}: {v}" for k, v in inv.items()),
        "",
        "Dropped product SKUs:",
        ", ".join(prod["dropped"]),
    ]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
