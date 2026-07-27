#!/usr/bin/env python3
"""Validate CS_OptionMapping_Rebuild CSVs against June 2026 source of truth."""

import csv
import sys
from pathlib import Path

from sync_from_june_source import (
    OPTION_IMAGE_OVERRIDES,
    PRODUCT_IMAGE_OVERRIDES,
    convert_image_field,
    to_csv_ref,
)

BASE = Path(__file__).parent
JUNE = Path.home() / "Downloads/CS_Master_Product_List_June_2026_UPDATE"
MASTER = JUNE / "Master Sheet E+G-Table 1.csv"
WEIYAN = JUNE / "Weiyan LED-Table 1.csv"
ACC_PATH = JUNE / "Accessories-Table 1.csv"
PARTS_PATH = JUNE / "Parts-Table 1.csv"
CORR_PATH = Path.home() / "Downloads/eCat Image Corrections.csv"

FINISH_CODES = {"BLK", "BRZ", "GRAY", "CLEAR", "COPPER"}


def clean(val: str) -> str:
    v = (val or "").strip()
    return "" if v in ("----", "#", "$") else v


def http_url(val: str) -> str:
    v = clean(val)
    return v if v.startswith("http") else ""


def load_accessories() -> dict[str, str]:
    acc = {}
    with ACC_PATH.open(newline="", encoding="utf-8-sig") as f:
        next(f)
        for row in csv.DictReader(f):
            sku = (row.get("Accessory SKU") or "").strip()
            if sku:
                acc[sku] = (row.get("Accessory Image Link") or "").strip()
    return acc


def load_corrections() -> dict[str, str]:
    corr = {}
    with CORR_PATH.open(encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) >= 2 and row[0].strip() and row[0].strip() not in (
                "Lantern + Product SKUs",
                "Accessory SKUs",
            ):
                corr[row[0].strip()] = clean(row[1])
    return corr


def load_master_field(field: str) -> dict[str, str]:
    """Full (untruncated) value of a master/weiyan column keyed by SKU."""
    out = {}
    for path in (MASTER, WEIYAN):
        with path.open(encoding="utf-8-sig") as f:
            r = csv.reader(f)
            next(r)
            headers = next(r)
            if field not in headers:
                continue
            idx = headers.index(field)
            for row in r:
                if row and row[0].strip():
                    out[row[0].strip()] = row[idx].strip() if idx < len(row) else ""
    return out


def expected_image(sku: str, acc: dict, corr: dict) -> str | None:
    if sku in corr:
        return corr[sku]
    if sku in acc:
        return acc[sku]
    return None


def main() -> int:
    errors: list[str] = []
    advisories: list[str] = []
    acc = load_accessories()
    corr = load_corrections()
    master_short = load_master_field("Short Description")
    master_retailer = load_master_field("Retailer Product Name")
    MAX_DESC = 255

    for path in ("products.csv", "options.csv", "option_groups.csv", "stories.csv"):
        if "CSHI" in (BASE / path).read_text(encoding="utf-8"):
            errors.append(f"{path} still contains CSHI")

    prods = list(csv.DictReader((BASE / "products.csv").open(encoding="utf-8")))
    opts = {r["Code"]: r for r in csv.DictReader((BASE / "options.csv").open(encoding="utf-8"))}
    groups = list(csv.DictReader((BASE / "option_groups.csv").open(encoding="utf-8")))

    # --- Image deliverability (PNG can't CDN-sync; plain filenames must be FTP-staged) ---
    # eCat-only mount-meta swatches live on the server from a prior pass, not staged here.
    MOUNT_META = {"wall-mount.jpg", "ceiling-mount.jpg", "post-mount.jpg"}
    images_dir = BASE / "images_upload"
    opt_dir = BASE / "option_images_upload"

    def check_image_refs(value: str, where: str, staged_dir: Path) -> None:
        for part in (value or "").split(","):
            ref = part.strip()
            if not ref:
                continue
            if ref.lower().split("?")[0].endswith(".png"):
                errors.append(f"{where}: PNG cannot CDN-sync -> {ref}")
            elif ref.startswith("http"):
                continue  # https .jpg URL: CDN path (already HEAD-validated separately)
            elif ref in MOUNT_META:
                advisories.append(f"{where}: mount-meta {ref} not staged locally (must exist on FTP)")
            elif not (staged_dir / ref).exists():
                errors.append(f"{where}: plain filename {ref} has no staged file in {staged_dir.name}/")

    for row in prods:
        check_image_refs(row.get("ImageFileName"), f"product {row['BaseItemCode']}", images_dir)
    for code, row in opts.items():
        check_image_refs(row.get("ImageName"), f"option {code}", opt_dir)

    master_skus = set()
    with MASTER.open(encoding="utf-8-sig") as f:
        r = csv.reader(f)
        next(r)
        next(r)
        for row in r:
            if row and row[0].strip():
                master_skus.add(row[0].strip())
    weiyan_skus = set()
    with WEIYAN.open(encoding="utf-8-sig") as f:
        r = csv.reader(f)
        next(r)
        next(r)
        for row in r:
            if row and row[0].strip():
                weiyan_skus.add(row[0].strip())
    prod_skus = {r["BaseItemCode"] for r in prods}

    if master_skus - prod_skus:
        errors.append(f"missing master SKUs in products: {len(master_skus - prod_skus)}")
    if weiyan_skus - prod_skus:
        errors.append(f"missing weiyan SKUs in products: {len(weiyan_skus - prod_skus)}")

    for row in prods:
        sku = row["BaseItemCode"]
        # ShortDesc must equal the FULL source Short Description (capped at 255),
        # not a 15-char fragment.
        if sku in master_short and master_short[sku]:
            exp = master_short[sku][:MAX_DESC]
            got = row.get("ShortDesc") or ""
            if got != exp:
                errors.append(f"ShortDesc {sku}: expected {exp!r}, got {got!r}")
        # LongDesc must equal the FULL Retailer Product Name (capped at 255).
        if sku in master_retailer and master_retailer[sku]:
            expL = master_retailer[sku][:MAX_DESC]
            gotL = row.get("LongDesc") or ""
            if gotL != expL:
                errors.append(f"LongDesc {sku}: expected {expL!r}, got {gotL!r}")

        if row.get("CollectionCodes") == "Accessories":
            raw = PRODUCT_IMAGE_OVERRIDES.get(sku, expected_image(sku, acc, corr))
            if raw is None:
                continue
            exp = convert_image_field(raw)  # mirror sync: .png source -> plain .jpg
            got = (row.get("ImageFileName") or "").strip()
            if not exp and got:
                errors.append(f"blank-violation product {sku}")
            elif exp and got != exp:
                errors.append(f"product {sku} image mismatch (exp {exp!r} got {got!r})")

    for code in FINISH_CODES:
        if code not in opts:
            continue
        img = (opts[code].get("ImageName") or "").strip()
        if "_750px" in img:
            errors.append(f"finish {code} still uses _750px alias")
        raw = OPTION_IMAGE_OVERRIDES.get(code, expected_image(code, acc, corr))
        exp = to_csv_ref(raw) if raw is not None else None
        if exp and img != exp:
            errors.append(f"finish {code}: expected {exp!r}, got {img[:50]}")

    for code, row in opts.items():
        if code not in acc and code not in corr and code not in OPTION_IMAGE_OVERRIDES:
            continue
        raw = OPTION_IMAGE_OVERRIDES.get(code, expected_image(code, acc, corr))
        if raw is None:
            continue
        exp = to_csv_ref(raw)
        got = (row.get("ImageName") or "").strip()
        if not exp and got:
            errors.append(f"blank-violation option {code}")
        elif exp and got != exp:
            errors.append(f"option {code} image mismatch (exp {exp!r} got {got!r})")

    for sku, raw in corr.items():
        if sku in prod_skus:
            exp = convert_image_field(PRODUCT_IMAGE_OVERRIDES.get(sku, raw))
            img = (next(r for r in prods if r["BaseItemCode"] == sku).get("ImageFileName") or "").strip()
            if img != exp:
                errors.append(f"corrections product {sku} not applied (exp {exp!r} got {img!r})")
        elif sku in opts:
            exp = to_csv_ref(OPTION_IMAGE_OVERRIDES.get(sku, raw))
            img = (opts[sku].get("ImageName") or "").strip()
            if img != exp:
                errors.append(f"corrections option {sku} not applied (exp {exp!r} got {img!r})")

    opt_codes = set(opts)
    for g in groups:
        for code in (g.get("Options") or "").split(","):
            code = code.strip()
            if code and code not in opt_codes:
                errors.append(f"option_groups {g['Code']}: unknown option {code}")

    jordan_checks = {
        "VNG50FH": "",
        "VNG": corr.get("VNG", acc.get("VNG", "")),
        "GH1-GPF": corr.get("GH1-GPF", ""),
        "GH2-GPF": corr.get("GH2-GPF", ""),
        "CHSI": acc.get("CHSI", corr.get("CHSI", "")),
    }
    for sku, exp_raw in jordan_checks.items():
        row = next((r for r in prods if r["BaseItemCode"] == sku), None)
        if not row:
            errors.append(f"missing Jordan check SKU {sku}")
            continue
        exp = convert_image_field(PRODUCT_IMAGE_OVERRIDES.get(sku, exp_raw))
        got = (row.get("ImageFileName") or "").strip()
        if got != exp:
            errors.append(f"Jordan product {sku}: expected {exp!r}, got {got!r}")

    for code in ("BMPM", "CHB", "CSP8", "FT", "PFA"):
        if (opts.get(code, {}).get("ImageName") or "").strip():
            errors.append(f"parent option {code} should be blank")

    # Sweep EVERY option for stale _750px local aliases (not just the finish set).
    # BRASS has no Catsy source URL in any source file -> advisory, not a hard fail.
    for code, row in opts.items():
        img = (row.get("ImageName") or "").strip()
        if "_750px" in img:
            if code in acc or code in corr:
                errors.append(f"option {code} still uses _750px alias: {img}")
            else:
                advisories.append(
                    f"option {code} swatch is stale local alias {img} with no Catsy "
                    f"source — needs Jordan to supply a URL or be blanked"
                )

    if advisories:
        print("ADVISORIES (non-blocking):")
        for a in advisories:
            print(f"  ! {a}")

    if errors:
        print("VALIDATION FAILED:")
        for e in errors[:40]:
            print(f"  - {e}")
        if len(errors) > 40:
            print(f"  … and {len(errors) - 40} more")
        return 1

    n_prod_staged = len(list((BASE / "images_upload").glob("*.jpg")))
    n_opt_staged = len(list((BASE / "option_images_upload").glob("*.jpg")))
    print("VALIDATION PASSED")
    print(f"  - {len(master_skus)} master + {len(weiyan_skus)} weiyan SKUs in products.csv")
    print(f"  - ShortDesc matches FULL source Short Description; LongDesc matches FULL Retailer Product Name")
    print(f"  - No .png in any image field; every plain filename has a staged JPG")
    print(f"    ({n_prod_staged} in images_upload/, {n_opt_staged} in option_images_upload/ for FTP)")
    print(f"  - Zero blank-source violations on synced SKUs")
    print(f"  - All corrections applied; no CSHI; option groups resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
