#!/usr/bin/env python3
"""Post-fix validation for CopperSmith image corrections."""

import csv
import sys
from pathlib import Path

BASE = Path(__file__).parent
ACC_PATH = Path.home() / "Downloads/CS_Master_Product_List_June_2026_UPDATE/Accessories-Table 1.csv"
CORR_PATH = Path.home() / "Downloads/eCat Image Corrections.csv"

ECAT_META = {"WALL", "CEIL", "POST", "COPPER", "BRASS"}

PRODUCT_IMAGE_FIXES = {
    "VNG": "https://s3.us-west-2.amazonaws.com/catsy.962/VNG.png",
    "VNG50FH": "",
    "GH1-GPF": "https://s3.us-west-2.amazonaws.com/catsy.962/GH1-GPF.png",
    "GH2-GPF": "https://s3.us-west-2.amazonaws.com/catsy.962/GH2-GPF.png",
    "HSI1": "https://s3.us-west-2.amazonaws.com/catsy.962/HSI1.png",
    "HSI2": "https://s3.us-west-2.amazonaws.com/catsy.962/HSI2.png",
    "BMHCHM": "https://s3.us-west-2.amazonaws.com/catsy.962/BMDSM.jpg",
    "SP36": "https://s3.us-west-2.amazonaws.com/catsy.962/_lg/4076156550/SP.jpg",
    "WY36": "https://s3.us-west-2.amazonaws.com/catsy.962/WY36.png",
    "VR25E": "https://s3.us-west-2.amazonaws.com/catsy.962/VR25E.png",
    "VR25G": "https://s3.us-west-2.amazonaws.com/catsy.962/VR25G.png",
    "LL-TUBE6A": "https://s3.us-west-2.amazonaws.com/catsy.962/LL-TUBE6A.png",
    "LL-TUBE8A": "https://s3.us-west-2.amazonaws.com/catsy.962/LL-TUBE8A.png",
    "GLC": "https://s3.us-west-2.amazonaws.com/catsy.962/GLC.png",
    "GN14": "https://s3.us-west-2.amazonaws.com/catsy.962/GN14.png",
    "GN17": "https://s3.us-west-2.amazonaws.com/catsy.962/GN17.png",
    "GTTL": "https://s3.us-west-2.amazonaws.com/catsy.962/GTTL.jpg",
    "PM36": "https://s3.us-west-2.amazonaws.com/catsy.962/PM36.png",
    "SA14": "https://s3.us-west-2.amazonaws.com/catsy.962/SA14.png",
    "SA17": "https://s3.us-west-2.amazonaws.com/catsy.962/SA17.png",
    "CHSI": "https://s3.us-west-2.amazonaws.com/catsy.962/_lg/4076156518/CHSI.jpg",
}

OPTION_IMAGE_FIXES = {
    "HSI1": "https://s3.us-west-2.amazonaws.com/catsy.962/HSI1.png",
    "HSI2": "https://s3.us-west-2.amazonaws.com/catsy.962/HSI2.png",
    "HSCM": "https://s3.us-west-2.amazonaws.com/catsy.962/HSCM.png",
    "WY": "https://s3.us-west-2.amazonaws.com/catsy.962/WY.png",
    "PF1": "https://s3.us-west-2.amazonaws.com/catsy.962/PF.png",
    "PF2": "https://s3.us-west-2.amazonaws.com/catsy.962/PF.png",
    "PF3": "https://s3.us-west-2.amazonaws.com/catsy.962/PF.png",
    "PF4": "https://s3.us-west-2.amazonaws.com/catsy.962/PF.png",
    "PF5": "https://s3.us-west-2.amazonaws.com/catsy.962/PF.png",
    "PF6": "https://s3.us-west-2.amazonaws.com/catsy.962/PF.png",
    "PF7": "https://s3.us-west-2.amazonaws.com/catsy.962/PF.png",
    "CHSI": "https://s3.us-west-2.amazonaws.com/catsy.962/_lg/4076156518/CHSI.jpg",
}

OPTION_CLEAR = {"BMPM", "CHB", "CSP8", "FT", "PFA"}


def load_accessories() -> dict[str, str]:
    acc = {}
    with ACC_PATH.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f.readlines()[1:]):
            sku = (row.get("Accessory SKU") or "").strip()
            if sku:
                acc[sku] = (row.get("Accessory Image Link") or "").strip()
    return acc


def load_corrections() -> dict[str, str]:
    corr = {}
    with CORR_PATH.open() as f:
        for row in csv.reader(f):
            if len(row) >= 2 and row[0].strip() and row[0].strip() not in (
                "Lantern + Product SKUs",
                "Accessory SKUs",
            ):
                corr[row[0].strip()] = row[1].strip()
    return corr


def expected_image(sku: str, acc: dict, corr: dict) -> str | None:
    if sku in corr:
        return corr[sku]
    if sku in acc:
        return acc[sku]
    return None


def main() -> int:
    errors: list[str] = []
    acc = load_accessories()
    corr = load_corrections()

    for path in ("products.csv", "options.csv", "option_groups.csv", "stories.csv"):
        text = (BASE / path).read_text(encoding="utf-8")
        if "CSHI" in text:
            errors.append(f"{path} still contains CSHI")

    prods = list(csv.DictReader((BASE / "products.csv").open(encoding="utf-8")))
    opts = {r["Code"]: r for r in csv.DictReader((BASE / "options.csv").open(encoding="utf-8"))}
    groups = list(csv.DictReader((BASE / "option_groups.csv").open(encoding="utf-8")))

    for sku, exp in PRODUCT_IMAGE_FIXES.items():
        row = next((r for r in prods if r["BaseItemCode"] == sku), None)
        if not row:
            errors.append(f"products.csv missing expected SKU {sku}")
            continue
        got = (row.get("ImageFileName") or "").strip()
        if got != exp:
            errors.append(f"products.csv {sku}: expected {exp!r}, got {got!r}")

    for code, exp in OPTION_IMAGE_FIXES.items():
        if code not in opts:
            errors.append(f"options.csv missing code {code}")
            continue
        got = (opts[code].get("ImageName") or "").strip()
        if got != exp:
            errors.append(f"options.csv {code}: expected {exp!r}, got {got!r}")

    for code in OPTION_CLEAR:
        if code not in opts:
            errors.append(f"options.csv missing code {code}")
        elif (opts[code].get("ImageName") or "").strip():
            errors.append(f"options.csv {code}: ImageName should be blank")

    for code in OPTION_CLEAR | ECAT_META:
        if code in acc and not acc[code] and code in opts and (opts[code].get("ImageName") or "").strip():
            if code not in ECAT_META:
                errors.append(f"blank-violation option {code}")

    for row in prods:
        sku = row["BaseItemCode"]
        if row.get("CollectionCodes") != "Accessories":
            continue
        exp = expected_image(sku, acc, corr)
        if exp is None:
            continue
        got = (row.get("ImageFileName") or "").strip()
        if not exp and got:
            errors.append(f"blank-violation product {sku}: has image {got[:50]}")
        elif exp and got != exp:
            errors.append(f"product {sku}: expected {exp[:50]}, got {got[:50]}")

    opt_codes = set(opts)
    for g in groups:
        for code in (g.get("Options") or "").split(","):
            code = code.strip()
            if code and code not in opt_codes:
                errors.append(f"option_groups {g['Code']}: unknown option {code}")

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("VALIDATION PASSED")
    print(f"  - No CSHI references in import files")
    print(f"  - {len(PRODUCT_IMAGE_FIXES)} product image targets verified")
    print(f"  - {len(OPTION_IMAGE_FIXES)} option image targets verified")
    print(f"  - {len(OPTION_CLEAR)} parent-option clears verified")
    print(f"  - Zero blank-source violations on accessory products")
    print(f"  - All option group codes resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
