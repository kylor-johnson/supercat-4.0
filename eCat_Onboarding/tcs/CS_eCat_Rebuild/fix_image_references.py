#!/usr/bin/env python3
"""Fix CopperSmith image references for eCat CDN + FTP workflows."""
from __future__ import annotations

import csv
import re
import shutil
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path(__file__).parent
PRODUCTS = BASE / "products.csv"
OPTIONS = BASE / "options.csv"
OPTION_FTP_DIR = BASE / "option_images_ftp"
PRODUCT_MANUAL_DIR = BASE / "product_images_manual"
MANIFEST = BASE / "option_images_ftp_manifest.csv"

# Google Drive file IDs for VR25 (not on Catsy CDN)
VR25_DRIVE = {
    "VR25E": "1nj7asY8GYKHQFXiFs4XUzJ_ymWx4_ssJ",
    "VR25G": "16e3Uh0q690NIdjsWU6vPvfBQs2aCUc9s",
}

PLUS_RENAMES = {
    "wide+top.jpg": "wide-top.jpg",
    "wide+bottom.jpg": "wide-bottom.jpg",
}


def url_to_filename(url: str) -> str:
    path = urllib.parse.urlparse(url).path
    name = Path(path).name
    name = urllib.parse.unquote(name)
    return PLUS_RENAMES.get(name, name)


def normalize_existing_filename(name: str) -> str:
    name = (name or "").strip()
    if not name:
        return name
    return PLUS_RENAMES.get(name, name)


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "SuperCat-eCat-fix/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dest.write_bytes(resp.read())


def convert_to_srgb_jpg(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    # macOS sips: flatten PNG/other to JPEG sRGB
    subprocess.run(
        ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "90", str(src), "--out", str(dest)],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["sips", "-m", "/System/Library/ColorSync/Profiles/sRGB Profile.icc", str(dest)],
        check=False,
        capture_output=True,
    )


def fix_options_csv() -> dict[str, str]:
    rows = []
    url_map: dict[str, str] = {}
    with OPTIONS.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            img = (row.get("ImageName") or "").strip()
            if img.startswith("http"):
                url_map[url_to_filename(img)] = img
                row["ImageName"] = url_to_filename(img)
            elif img:
                row["ImageName"] = normalize_existing_filename(img)
            rows.append(row)

    shutil.copy2(OPTIONS, OPTIONS.with_suffix(".csv.bak2"))
    with OPTIONS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return url_map


def fix_products_csv() -> None:
    rows = []
    with PRODUCTS.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            code = row["BaseItemCode"]
            img = (row.get("ImageFileName") or "").strip()
            if code in VR25_DRIVE:
                row["ImageFileName"] = f"{code}.jpg"
            rows.append(row)

    shutil.copy2(PRODUCTS, PRODUCTS.with_suffix(".csv.bak2"))
    with PRODUCTS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_vr25_product_images() -> None:
    PRODUCT_MANUAL_DIR.mkdir(parents=True, exist_ok=True)
    for code, file_id in VR25_DRIVE.items():
        tmp = PRODUCT_MANUAL_DIR / f"{code}_source"
        out = PRODUCT_MANUAL_DIR / f"{code}.jpg"
        gurl = f"https://drive.google.com/uc?export=download&id={file_id}"
        download(gurl, tmp)
        convert_to_srgb_jpg(tmp, out)
        tmp.unlink(missing_ok=True)
        print(f"product manual: {out.name}")


def download_option_images(url_map: dict[str, str]) -> list[dict]:
    OPTION_FTP_DIR.mkdir(parents=True, exist_ok=True)
    manifest_rows = []
    for ftp_name in sorted(url_map):
        src_url = url_map[ftp_name]
        dest = OPTION_FTP_DIR / ftp_name
        status = "ok"
        note = ""
        try:
            download(src_url, dest)
            # normalize + filenames on disk if Catsy serves literal plus
            if "+" in Path(urllib.parse.urlparse(src_url).path).name and ftp_name != Path(urllib.parse.urlparse(src_url).path).name:
                pass
            size = dest.stat().st_size
            if size < 500:
                status = "error"
                note = "file too small — likely not an image"
        except Exception as exc:  # noqa: BLE001
            status = "error"
            note = str(exc)
        manifest_rows.append(
            {
                "ftp_filename": ftp_name,
                "catsy_url": src_url,
                "local_path": str(dest.relative_to(BASE)),
                "status": status,
                "notes": note,
            }
        )
        print(f"option {status}: {ftp_name}")
    return manifest_rows


def write_manifest(rows: list[dict]) -> None:
    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["ftp_filename", "catsy_url", "local_path", "status", "notes"],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    print("Fixing options.csv ImageName values...")
    url_map = fix_options_csv()
    print(f"  {len(url_map)} unique option image filenames")

    print("Fixing products.csv VR25 ImageFileName values...")
    fix_products_csv()

    print("Building VR25 manual product images from Google Drive...")
    build_vr25_product_images()

    print("Downloading option swatches for FTP...")
    manifest = download_option_images(url_map)
    write_manifest(manifest)

    errors = [r for r in manifest if r["status"] != "ok"]
    print(f"Done. {len(manifest)} option files, {len(errors)} errors.")
    print(f"Upload {OPTION_FTP_DIR.name}/ contents to FTP /option_images")
    print(f"Upload {PRODUCT_MANUAL_DIR.name}/ VR25E.jpg VR25G.jpg to FTP /images")


if __name__ == "__main__":
    main()
