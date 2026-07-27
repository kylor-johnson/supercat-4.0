#!/usr/bin/env python3
"""Patch products.csv for import warnings: TurtleFriendly, Installation, UPC gaps."""
from __future__ import annotations

import csv
import re
import shutil
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent
SRC = BASE.parent / "Source Data"
MASTER = SRC / "Master Sheet E+G-Table 1.csv"
WEIYAN = SRC / "Weiyan LED-Table 1.csv"
ACCESSORIES = SRC / "Accessories-Table 1.csv"
PARTS_SRC = SRC / "Parts-Table 1.csv"
PRODUCTS = BASE / "products.csv"

GLASS_PREFIXES = ("SRG", "HRG", "RG")
ACCESSORY_SKUS = {
    "WGS", "WGL", "GLC", "FB1", "FB12V", "FBBM1", "ADS", "CSHI", "HSI1", "HSI2",
    "TLA", "703001", "703002", "LL-TUBE6", "LL-TUBE8",
    "16WST", "16WSTH", "9WST", "9WSTH",
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


def load_weiyan() -> dict[str, dict[str, str]]:
    with open(WEIYAN, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f)
        next(r)
        headers = next(r)
        out: dict[str, dict[str, str]] = {}
        for row in r:
            if row and row[0].strip():
                out[row[0].strip()] = dict(zip(headers, row + [""] * (len(headers) - len(row))))
        return out


def load_accessory_gtin() -> dict[str, str]:
    gtin: dict[str, str] = {}
    with open(ACCESSORIES, newline="", encoding="utf-8-sig") as f:
        next(f)
        for row in csv.DictReader(f):
            sku = row.get("Accessory SKU", "").strip()
            val = row.get("Accessory GTIN", "").strip()
            if sku and val and val != "----":
                gtin[sku] = val
    return gtin


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


def lantern_match_keys(sku: str) -> set[str]:
    keys: set[str] = set()
    m = re.match(r"^([A-Z]{2,4})(\d{2,3})([EGW])?$", sku)
    if m:
        keys.add(f"{m.group(1)}{m.group(2)}")
    return keys


def is_lantern(sku: str) -> bool:
    if sku in ACCESSORY_SKUS:
        return False
    if sku.endswith("KIT") or "-CPKIT" in sku or "-SMKIT" in sku:
        return False
    return bool(lantern_match_keys(sku))


def master_lookup(sku: str, master: dict[str, dict[str, str]]) -> dict[str, str] | None:
    if sku in master:
        return master[sku]
    if sku.endswith("W"):
        for alt in (sku[:-1] + "E", sku[:-1] + "G"):
            if alt in master:
                return master[alt]
    return None


def upc_from_row(m: dict[str, str], weiyan: bool = False) -> str:
    for key in ("UPC/GTIN", "UPC") if weiyan else ("UPC", "UPC/GTIN"):
        val = (m.get(key) or "").strip()
        if val and val not in ("----", "#"):
            return val
    return ""


def turtle_friendly(row: dict[str, str], m: dict[str, str] | None) -> str:
    coll = (row.get("CollectionCodes") or "").lower()
    cat = (row.get("CategoryCodes") or "").lower()
    if "turtle friendly" in coll or "wildlife friendly" in cat:
        return "Yes"
    if m:
        subtype = (m.get("Fixture Sub-Type (Additional Filtering Options)") or "").lower()
        if "wildlife friendly" in subtype:
            return "Yes"
        tf = (m.get("Turtle Friendly") or "").strip().lower()
        if tf in ("yes", "y"):
            return "Yes"
    return ""


def installation_value(m: dict[str, str] | None, row: dict[str, str]) -> str:
    if m:
        inst = (m.get("Installation") or "").strip()
        if inst:
            return inst
        spec = (m.get("Spec Sheet URL") or "").strip()
        if spec.startswith("http"):
            return spec
    return (row.get("SpecSheet") or "").strip()


def build_part_upc_fallback(rows: list[dict[str, str]]) -> dict[str, str]:
    """Use RelatedItems3 lantern links, then family/size key matching."""
    by_sku = {r["BaseItemCode"].strip(): r for r in rows}
    part_upc: dict[str, str] = {}

    # Pass 1: lanterns already list parts in RelatedItems3
    for lan_sku, lan_row in by_sku.items():
        if not is_lantern(lan_sku):
            continue
        upc = (lan_row.get("UPCValue") or "").strip()
        if not upc:
            continue
        for ref in (lan_row.get("RelatedItems3") or "").split(","):
            ref = ref.strip()
            if ref and ref not in part_upc:
                part_upc[ref] = upc

    # Pass 2: family/size keys for unmatched parts
    lanterns = {sku: r for sku, r in by_sku.items() if is_lantern(sku)}
    for part_sku, row in by_sku.items():
        if row.get("CategoryCodes") != "Parts" or part_sku in part_upc:
            continue
        pkeys = part_match_keys(part_sku)
        if not pkeys:
            continue
        for lan_sku, lan_row in lanterns.items():
            if pkeys & lantern_match_keys(lan_sku):
                upc = (lan_row.get("UPCValue") or "").strip()
                if upc:
                    part_upc[part_sku] = upc
                    break
    return part_upc


def main() -> None:
    master = load_master()
    weiyan = load_weiyan()
    acc_gtin = load_accessory_gtin()

    with open(PRODUCTS, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    for col in ("TurtleFriendly", "Installation"):
        if col not in fields:
            fields.append(col)

    part_upc = build_part_upc_fallback(rows)

    tf_set = inst_set = upc_weiyan = upc_acc = upc_part = 0
    for row in rows:
        sku = row["BaseItemCode"].strip()
        m = weiyan.get(sku) or master.get(sku) or master_lookup(sku, master)
        is_w = sku in weiyan

        tf = turtle_friendly(row, m)
        if tf:
            row["TurtleFriendly"] = tf
            tf_set += 1
        else:
            row["TurtleFriendly"] = row.get("TurtleFriendly", "")

        inst = installation_value(m, row)
        if inst:
            row["Installation"] = inst
            inst_set += 1
        else:
            row["Installation"] = row.get("Installation", "")

        if not (row.get("UPCValue") or "").strip():
            if m:
                upc = upc_from_row(m, weiyan=is_w)
                if upc:
                    row["UPCValue"] = upc
                    upc_weiyan += 1
            if not (row.get("UPCValue") or "").strip() and sku in acc_gtin:
                row["UPCValue"] = acc_gtin[sku]
                upc_acc += 1
            if not (row.get("UPCValue") or "").strip() and sku in part_upc:
                row["UPCValue"] = part_upc[sku]
                upc_part += 1

    shutil.copy(PRODUCTS, PRODUCTS.with_suffix(".csv.pre_import_warn_bak"))
    with open(PRODUCTS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    blank = sum(1 for r in rows if not (r.get("UPCValue") or "").strip())
    print(f"TurtleFriendly set: {tf_set}")
    print(f"Installation set: {inst_set}")
    print(f"UPC filled — weiyan/source: {upc_weiyan}, accessories: {upc_acc}, parts (lantern fallback): {upc_part}")
    print(f"Remaining blank UPC: {blank}")
    if blank:
        missing = [r["BaseItemCode"] for r in rows if not (r.get("UPCValue") or "").strip()]
        print(f"  Still missing ({len(missing)}): {missing[:12]}...")


if __name__ == "__main__":
    main()
