#!/usr/bin/env python3
"""Download PNG source images, convert to JPG, and stage them for FTP.

Why: CdnImageSync (supercat_server/app/services/cdn_image_sync.rb) only downloads
an image when the derived filename ends in .jpg/.jpeg AND the URL returns
image/jpeg. CopperSmith's source images for ~71 SKUs exist only as PNG, so they
can never CDN-sync. The sync script now rewrites every .png source link to a plain
"{basename}.jpg" filename; this script produces those JPG files from the original
Catsy PNGs and stages them into the FTP upload folders:

    products.csv ImageFileName plain refs -> images_upload/
    options.csv  ImageName     plain refs -> option_images_upload/

Run AFTER sync_from_june_source.py. Idempotent (re-converts in place).
"""
from __future__ import annotations

import csv
import tempfile
import urllib.request
from pathlib import Path

from PIL import Image

from sync_from_june_source import (
    OPTION_IMAGE_OVERRIDES,
    PRODUCT_IMAGE_OVERRIDES,
    cdn_needs_local_copy,
)

BASE = Path(__file__).parent
JUNE = Path.home() / "Downloads/CS_Master_Product_List_June_2026_UPDATE"
MASTER = JUNE / "Master Sheet E+G-Table 1.csv"
WEIYAN = JUNE / "Weiyan LED-Table 1.csv"
ACCESSORIES = JUNE / "Accessories-Table 1.csv"
PARTS_SRC = JUNE / "Parts-Table 1.csv"
CORR = Path.home() / "Downloads/eCat Image Corrections.csv"

PRODUCTS = BASE / "products.csv"
OPTIONS = BASE / "options.csv"
IMAGES_DIR = BASE / "images_upload"
OPT_DIR = BASE / "option_images_upload"
MANIFEST = BASE / "image_conversion_manifest.csv"


def collect_source_urls() -> dict[str, str]:
    """Map clean target jpg filename -> original source URL across every sync input.

    Covers both CDN-incompatible classes (same rule as the sync's to_csv_ref):
    .png sources AND .jpg sources whose Catsy filename has parens/space/%/+.
    """
    out: dict[str, str] = {}

    def add(url: str) -> None:
        u = (url or "").strip()
        target = cdn_needs_local_copy(u)
        if target:
            out[target] = u

    with CORR.open(encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) >= 2:
                add(row[1])

    with ACCESSORIES.open(newline="", encoding="utf-8-sig") as f:
        next(f)
        for row in csv.DictReader(f):
            add(row.get("Accessory Image Link", ""))

    for path in (MASTER, WEIYAN):
        with path.open(newline="", encoding="utf-8-sig") as f:
            r = csv.reader(f)
            next(r)
            next(r)
            for row in r:
                for cell in row:
                    add(cell)

    with PARTS_SRC.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if len(row) > 9:
                add(row[9])

    # Manual override maps may point at recovered assets (e.g. TE20E.png) that
    # don't appear in the standard source columns.
    for url in list(PRODUCT_IMAGE_OVERRIDES.values()) + list(OPTION_IMAGE_OVERRIDES.values()):
        add(url)

    return out


def needed_filenames(csv_path: Path, field: str) -> set[str]:
    """Plain-filename (non-URL, non-blank) image references in a CSV column."""
    out: set[str] = set()
    with csv_path.open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            for part in (row.get(field) or "").split(","):
                v = part.strip()
                if v and not v.startswith("http"):
                    out.add(v)
    return out


def download_convert(url: str, dest: Path) -> None:
    """Download any source image and write a clean JPEG with NO metadata.

    Re-encoding through Pillow strips EXIF/XMP, which is what causes eCat's
    thumbnail step (ImageMagick `-regard-warnings`) to fail on a corrupt XMP
    profile. The output is a plain baseline JPEG, sRGB, no embedded profiles.
    """
    tmp = Path(tempfile.mkstemp()[1])
    try:
        urllib.request.urlretrieve(url, tmp)
        with Image.open(tmp) as im:
            im = im.convert("RGB")
            im.save(dest, "JPEG", quality=90)
    finally:
        tmp.unlink(missing_ok=True)


def prune_unreferenced(target_dir: Path, referenced: set[str]) -> list[str]:
    """Delete staged JPGs not referenced by any current CSV plain filename
    (e.g. swatches now served via a clean CDN URL). Keeps the FTP folder pristine."""
    removed = []
    for f in sorted(target_dir.glob("*.jpg")):
        if f.name not in referenced:
            f.unlink()
            removed.append(f.name)
    return removed


def referenced_plain_filenames(csv_path: Path, field: str) -> set[str]:
    return needed_filenames(csv_path, field)


def strip_metadata_inplace(target_dir: Path) -> int:
    """Re-save every staged JPG with no EXIF/XMP (belt-and-suspenders for any
    pre-existing staged file not regenerated this run)."""
    n = 0
    for f in sorted(target_dir.glob("*.jpg")):
        try:
            with Image.open(f) as im:
                rgb = im.convert("RGB")
            rgb.save(f, "JPEG", quality=90)
            n += 1
        except Exception:  # noqa: BLE001
            pass
    return n


def stage(
    needed: set[str],
    target_dir: Path,
    source_map: dict[str, str],
    label: str,
    manifest_rows: list,
    missing: list,
) -> None:
    target_dir.mkdir(exist_ok=True)
    for fn in sorted(needed):
        if not fn.lower().endswith((".jpg", ".jpeg")):
            continue
        url = source_map.get(fn)
        if not url:
            # No PNG source (e.g. mount-meta wall-mount.jpg, or already-correct .jpg).
            missing.append((label, fn))
            continue
        dest = target_dir / fn
        try:
            download_convert(url, dest)
            manifest_rows.append((label, fn, url, "ok", dest.stat().st_size))
        except Exception as exc:  # noqa: BLE001
            manifest_rows.append((label, fn, url, f"ERROR {exc}", 0))
            missing.append((label, fn))


def main() -> None:
    source_map = collect_source_urls()
    prod_needed = needed_filenames(PRODUCTS, "ImageFileName")
    opt_needed = needed_filenames(OPTIONS, "ImageName")

    manifest: list = []
    missing: list = []
    stage(prod_needed, IMAGES_DIR, source_map, "product", manifest, missing)
    stage(opt_needed, OPT_DIR, source_map, "option", manifest, missing)

    pruned = prune_unreferenced(IMAGES_DIR, prod_needed) + prune_unreferenced(OPT_DIR, opt_needed)
    if pruned:
        print(f"Pruned {len(pruned)} unreferenced staged JPG(s).")

    stripped = strip_metadata_inplace(IMAGES_DIR) + strip_metadata_inplace(OPT_DIR)
    print(f"Metadata-stripped {stripped} staged JPG(s) (no EXIF/XMP).")

    with MANIFEST.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["type", "filename", "source_url", "status", "bytes"])
        w.writerows(manifest)

    ok = [m for m in manifest if m[3] == "ok"]
    print(
        f"Staged {len(ok)} JPGs "
        f"({sum(1 for m in ok if m[0] == 'product')} product -> images_upload/, "
        f"{sum(1 for m in ok if m[0] == 'option')} option -> option_images_upload/)"
    )
    print(f"Manifest: {MANIFEST.name}")
    errs = [m for m in manifest if m[3] != "ok"]
    if errs:
        print(f"\n{len(errs)} conversion error(s):")
        for m in errs:
            print(f"  [{m[0]}] {m[1]} <- {m[2]}: {m[3]}")
    if missing:
        no_src = [(lbl, fn) for lbl, fn in missing if (lbl, fn, ) not in {(e[0], e[1]) for e in errs}]
        if no_src:
            print(
                f"\nNo PNG source for {len(no_src)} referenced filename(s) "
                f"(skipped — mount-meta or pre-staged, verify these exist on FTP):"
            )
            for lbl, fn in no_src:
                print(f"  [{lbl}] {fn}")


if __name__ == "__main__":
    main()
