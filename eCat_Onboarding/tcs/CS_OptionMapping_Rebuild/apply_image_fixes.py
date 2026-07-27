#!/usr/bin/env python3
"""One-time surgical image fixes per IMAGE_FIX plan. Run once, then validate."""

import csv
from pathlib import Path

BASE = Path(__file__).parent

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
    "GLC": "https://s3.us-west-2.amazonaws.com/catsy.962/GLC.png",
    "GN14": "https://s3.us-west-2.amazonaws.com/catsy.962/GN14.png",
    "GN17": "https://s3.us-west-2.amazonaws.com/catsy.962/GN17.png",
    "GTTL": "https://s3.us-west-2.amazonaws.com/catsy.962/GTTL.jpg",
    "PM36": "https://s3.us-west-2.amazonaws.com/catsy.962/PM36.png",
    "SA14": "https://s3.us-west-2.amazonaws.com/catsy.962/SA14.png",
    "SA17": "https://s3.us-west-2.amazonaws.com/catsy.962/SA17.png",
}

PRODUCT_DESC_FIXES = {
    "HSI1": ("Hammered Shade", "Frosted Hurricane Shade"),
    "HSI2": ("Hammered Shade", "Sanded Hurricane Shade"),
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

SKU_RENAMES = {
    "LL-TUBE6": ("LL-TUBE6A", "https://s3.us-west-2.amazonaws.com/catsy.962/LL-TUBE6A.png"),
    "LL-TUBE8": ("LL-TUBE8A", "https://s3.us-west-2.amazonaws.com/catsy.962/LL-TUBE8A.png"),
}

changes: list[str] = []


def log_change(file: str, sku: str, field: str, before: str, after: str) -> None:
    changes.append(f"| {file} | `{sku}` | {field} | `{before or '(blank)'}` | `{after or '(blank)'}` |")


def load_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def fix_options() -> None:
    path = BASE / "options.csv"
    fields, rows = load_csv(path)
    for row in rows:
        code = row["Code"]
        if code in OPTION_CLEAR:
            before = row.get("ImageName", "")
            row["ImageName"] = ""
            log_change("options.csv", code, "ImageName", before, "")
        if code == "CSHI":
            before_code = code
            before_img = row.get("ImageName", "")
            row["Code"] = "CHSI"
            row["ImageName"] = OPTION_IMAGE_FIXES["CHSI"]
            log_change("options.csv", before_code, "Code", before_code, "CHSI")
            log_change("options.csv", "CHSI", "ImageName", before_img, row["ImageName"])
        elif code in OPTION_IMAGE_FIXES:
            before = row.get("ImageName", "")
            row["ImageName"] = OPTION_IMAGE_FIXES[code]
            log_change("options.csv", code, "ImageName", before, row["ImageName"])
    write_csv(path, fields, rows)


def fix_option_groups() -> None:
    path = BASE / "option_groups.csv"
    fields, rows = load_csv(path)
    for row in rows:
        opts = row.get("Options", "")
        if "CSHI" in opts:
            before = opts
            row["Options"] = opts.replace("CSHI", "CHSI")
            log_change("option_groups.csv", row["Code"], "Options", before[:80], row["Options"][:80])
    write_csv(path, fields, rows)


def fix_products() -> None:
    path = BASE / "products.csv"
    fields, rows = load_csv(path)
    for row in rows:
        sku = row["BaseItemCode"]

        for col in ("RelatedItems2", "RelatedItems", "RelatedItems3"):
            val = row.get(col, "")
            if "CSHI" in val:
                before = val
                row[col] = val.replace("CSHI", "CHSI")
                log_change("products.csv", sku, col, before[:60], row[col][:60])

        if sku == "CSHI":
            before = sku
            row["BaseItemCode"] = "CHSI"
            if row.get("RelatedItems") == "CSHI":
                row["RelatedItems"] = "CHSI"
            log_change("products.csv", before, "BaseItemCode", before, "CHSI")
            sku = "CHSI"

        if sku in SKU_RENAMES:
            new_sku, img = SKU_RENAMES[sku]
            before = sku
            row["BaseItemCode"] = new_sku
            if row.get("RelatedItems") == before:
                row["RelatedItems"] = new_sku
            log_change("products.csv", before, "BaseItemCode", before, new_sku)
            before_img = row.get("ImageFileName", "")
            row["ImageFileName"] = img
            log_change("products.csv", new_sku, "ImageFileName", before_img, img)
            sku = new_sku

        if sku in PRODUCT_IMAGE_FIXES:
            before = row.get("ImageFileName", "")
            row["ImageFileName"] = PRODUCT_IMAGE_FIXES[sku]
            log_change("products.csv", sku, "ImageFileName", before[:70], row["ImageFileName"] or "(blank)")

        if sku in PRODUCT_DESC_FIXES:
            old_ld, new_ld = PRODUCT_DESC_FIXES[sku]
            if row.get("LongDesc") == old_ld:
                before = row["LongDesc"]
                row["LongDesc"] = new_ld
                row["ShortDesc"] = new_ld
                log_change("products.csv", sku, "LongDesc", before, new_ld)

    write_csv(path, fields, rows)


def fix_stories() -> None:
    path = BASE / "stories.csv"
    fields, rows = load_csv(path)
    for row in rows:
        sku = row["BaseItemCode"]
        if sku == "CSHI":
            before = sku
            row["BaseItemCode"] = "CHSI"
            log_change("stories.csv", before, "BaseItemCode", before, "CHSI")
        elif sku in SKU_RENAMES:
            new_sku, _ = SKU_RENAMES[sku]
            before = sku
            row["BaseItemCode"] = new_sku
            log_change("stories.csv", before, "BaseItemCode", before, new_sku)
    write_csv(path, fields, rows)


def write_audit() -> None:
    lines = [
        "# CopperSmith Image Fix Audit",
        "",
        "Applied per client feedback (Jordan) + eCat Image Corrections spreadsheet.",
        "",
        "| File | SKU | Field | Before | After |",
        "|------|-----|-------|--------|-------|",
        *changes,
        "",
        f"**Total changes logged:** {len(changes)}",
    ]
    (BASE / "IMAGE_FIX_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    fix_options()
    fix_option_groups()
    fix_products()
    fix_stories()
    write_audit()
    print(f"Applied {len(changes)} logged changes.")
    print(f"Audit written to {BASE / 'IMAGE_FIX_AUDIT.md'}")


if __name__ == "__main__":
    main()
