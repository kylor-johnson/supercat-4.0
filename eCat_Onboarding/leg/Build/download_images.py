#!/usr/bin/env python3
"""
Download Legrand product images from distributor CDN for eCat FTP /images.

Usage:
    python3 download_images.py [--only-skus-file PATH] [--max-per-product N]
                               [--out-dir DIR] [--dry-run] [--limit N]

Default source: Legrand root xlsx Image Files sheet.
Writes verified files as {PartNumber}.jpg / {PartNumber}_2.jpg …
and merges BaseItemCode → ImageFileName into image_filename_map.csv.
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    import openpyxl
except ImportError:
    openpyxl = None

try:
    from PIL import Image
except ImportError:
    Image = None

SCRIPT_DIR = Path(__file__).parent
DEFAULT_XLSX = SCRIPT_DIR.parent / "adorne & radiant image & video links.xlsx"
FALLBACK_XLSX = SCRIPT_DIR.parent / "adorne  radiant US  CAD Data File  5-14-26.xlsx"
MAP_PATH = SCRIPT_DIR / "image_filename_map.csv"
MAX_IMAGES_PER_PRODUCT = 6
WORKERS = 12


def parse_args():
    p = argparse.ArgumentParser(description="Download Legrand images for eCat")
    p.add_argument("--xlsx", type=Path, default=None, help="Image links xlsx")
    p.add_argument("--only-skus-file", type=Path, default=None,
                   help="Newline-separated BaseItemCodes to download")
    p.add_argument("--max-per-product", type=int, default=MAX_IMAGES_PER_PRODUCT)
    p.add_argument("--out-dir", type=Path, default=SCRIPT_DIR / "images_missing_batch")
    p.add_argument("--limit", type=int, default=0, help="Max products (0=all)")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--workers", type=int, default=WORKERS)
    return p.parse_args()


def load_sheet_rows(xlsx: Path) -> list[dict]:
    if openpyxl is None:
        raise RuntimeError("openpyxl required: pip install openpyxl")
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    if "Image Files" not in wb.sheetnames:
        raise RuntimeError(f"No 'Image Files' sheet in {xlsx}")
    ws = wb["Image Files"]
    it = ws.iter_rows(values_only=True)
    header = [str(h).strip() if h is not None else "" for h in next(it)]
    rows = []
    for raw in it:
        row = {
            header[i]: ("" if raw[i] is None else str(raw[i]).strip())
            for i in range(len(header))
        }
        if row.get("Part Number"):
            rows.append(row)
    wb.close()
    return rows


def get_image_urls(row: dict, max_per_product: int) -> list[str]:
    urls: list[str] = []
    main = row.get("Main Image_1", "").strip()
    if main and "youtube" not in main.lower() and main.startswith("http"):
        urls.append(main)
    for i in range(1, 50):
        if len(urls) >= max_per_product:
            break
        val = row.get(f"alternate_image_{i}", "").strip()
        if val and val.startswith("http") and "youtube" not in val.lower() and val != main:
            urls.append(val)
    return urls[:max_per_product]


def filename_for(part: str, index: int) -> str:
    return f"{part}.jpg" if index == 1 else f"{part}_{index}.jpg"


def to_jpg_bytes(raw: bytes) -> bytes:
    """Normalize any raster to sRGB JPEG bytes. Falls back to raw if Pillow missing."""
    if Image is None:
        return raw
    try:
        im = Image.open(io.BytesIO(raw))
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1] if im.mode == "RGBA" else None)
            im = bg
        elif im.mode != "RGB":
            im = im.convert("RGB")
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=90, optimize=True)
        return buf.getvalue()
    except Exception:
        return raw


def download_one(url: str, dest: Path, dry_run: bool) -> tuple[str, bool, str]:
    if dry_run:
        return dest.name, True, "dry-run"
    if dest.exists() and dest.stat().st_size > 500:
        return dest.name, True, "exists"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SuperCat-LegrandImagePull/1.0"})
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read()
        if len(raw) < 500:
            return dest.name, False, f"too-small ({len(raw)} bytes)"
        data = to_jpg_bytes(raw)
        dest.write_bytes(data)
        if dest.stat().st_size < 500:
            dest.unlink(missing_ok=True)
            return dest.name, False, "wrote-too-small"
        return dest.name, True, "ok"
    except Exception as e:
        return dest.name, False, str(e)


def merge_map(updates: dict[str, str]) -> None:
    existing: dict[str, str] = {}
    if MAP_PATH.exists():
        with MAP_PATH.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                code = (row.get("BaseItemCode") or "").strip()
                fn = (row.get("ImageFileName") or "").strip()
                if code and fn:
                    existing[code] = fn
    existing.update(updates)
    with MAP_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["BaseItemCode", "ImageFileName"])
        for code in sorted(existing):
            w.writerow([code, existing[code]])


def main() -> int:
    args = parse_args()
    xlsx = args.xlsx
    if xlsx is None:
        xlsx = DEFAULT_XLSX if DEFAULT_XLSX.exists() else FALLBACK_XLSX
    if not xlsx.exists():
        print(f"ERROR: xlsx not found: {xlsx}", file=sys.stderr)
        return 1

    only: set[str] | None = None
    if args.only_skus_file:
        only = {
            line.strip()
            for line in args.only_skus_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        }

    rows = load_sheet_rows(xlsx)
    if only is not None:
        rows = [r for r in rows if r["Part Number"].strip() in only]

    rows = sorted(rows, key=lambda r: r["Part Number"])
    if args.limit:
        rows = rows[: args.limit]

    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Source: {xlsx}")
    print(f"Products to process: {len(rows)}")
    print(f"Max images/product: {args.max_per_product}")
    print(f"Output: {out_dir}")
    if only is not None:
        missing_from_sheet = sorted(only - {r['Part Number'].strip() for r in rows})
        print(f"SKUs in only-list but not on Image Files sheet: {len(missing_from_sheet)}")
    if args.dry_run:
        print("*** DRY RUN ***")

    jobs: list[tuple[str, str, Path]] = []  # part, url, dest
    filename_map: dict[str, str] = {}
    for row in rows:
        part = row["Part Number"].strip()
        urls = get_image_urls(row, args.max_per_product)
        if not urls:
            continue
        names = []
        for i, url in enumerate(urls, start=1):
            fname = filename_for(part, i)
            names.append(fname)
            jobs.append((part, url, out_dir / fname))
        filename_map[part] = ",".join(names)

    print(f"Image files to fetch/check: {len(jobs)}")

    ok = err = skipped = 0
    errors: list[str] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = {
            pool.submit(download_one, url, dest, args.dry_run): (part, dest.name)
            for part, url, dest in jobs
        }
        done = 0
        for fut in as_completed(futs):
            done += 1
            name, success, reason = fut.result()
            if success and reason == "exists":
                skipped += 1
            elif success:
                ok += 1
            else:
                err += 1
                errors.append(f"{name}: {reason}")
            if done % 50 == 0 or done == len(futs):
                print(f"  progress {done}/{len(futs)} ok={ok} skip={skipped} err={err}")

    if not args.dry_run and filename_map:
        # only keep map entries where primary file exists
        verified = {}
        for part, fnames in filename_map.items():
            present = []
            for fn in fnames.split(","):
                p = out_dir / fn
                if p.exists() and p.stat().st_size > 500:
                    present.append(fn)
            if present:
                verified[part] = ",".join(present)
        merge_map(verified)
        filename_map = verified

    gap_path = SCRIPT_DIR / "missing_still_no_image.txt"
    if only is not None:
        still = sorted(only - set(filename_map))
        gap_path.write_text("\n".join(still) + ("\n" if still else ""))
        print(f"Still no image ({len(still)}): {gap_path.name}")

    print("\n=== SUMMARY ===")
    print(f"Products with files: {len(filename_map)}")
    print(f"Downloaded/wrote: {ok}")
    print(f"Already present: {skipped}")
    print(f"Errors: {err}")
    if errors[:10]:
        print("Sample errors:")
        for e in errors[:10]:
            print(f"  {e}")
    print(f"Map: {MAP_PATH}")
    print(f"Staging folder: {out_dir}")
    print("\nNext:")
    print("  1. python3 build_ecat_files.py")
    print(f"  2. FTP upload {out_dir.name}/ → /images (≤500/batch)")
    print("  3. Import products.csv → /data")
    return 0 if err == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
