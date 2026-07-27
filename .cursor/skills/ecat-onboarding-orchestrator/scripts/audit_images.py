#!/usr/bin/env python3
"""Audit the images referenced by an eCat products.csv against files on disk.

Hard failures (exit 1): missing files, corrupt/error-page files (< 500 bytes),
more images than the org's limit. Hero-image warnings are heuristic and printed
but do not fail the run on their own.

Usage:
    python audit_images.py products.csv /path/to/images [--max 6]
"""
import argparse
import csv
import os
import sys

MIN_BYTES = 500
HERO_SIZE_RATIO = 4  # image 1 this many times larger than image 2 => likely a scene shot


def load_rows(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return [], {}
        lookup = {name.strip().lower(): name for name in reader.fieldnames}
        return list(reader), lookup


def get(row, lookup, field):
    actual = lookup.get(field.lower())
    return (row.get(actual) or "").strip() if actual else ""


def main():
    ap = argparse.ArgumentParser(description="Audit eCat product images")
    ap.add_argument("csv_path", help="path to products.csv")
    ap.add_argument("image_dir", help="directory holding the image files")
    ap.add_argument("--max", type=int, default=6,
                    help="max images per product (6 default, 12 with the paid flag)")
    args = ap.parse_args()

    rows, lookup = load_rows(args.csv_path)
    if not rows:
        print("ERROR: no rows / empty header in file")
        return 2
    if "imagefilename" not in lookup:
        print("ERROR: no ImageFileName column")
        return 2

    failures, warnings = [], []
    products_with_images = 0

    for r in rows:
        bic = get(r, lookup, "BaseItemCode") or "?"
        raw = get(r, lookup, "ImageFileName")
        if not raw:
            continue
        products_with_images += 1
        names = [n.strip() for n in raw.split(",") if n.strip()]

        if len(names) > args.max:
            failures.append(f"{bic}: {len(names)} images > limit {args.max}")

        sizes = []
        for name in names:
            path = os.path.join(args.image_dir, name)
            if not os.path.exists(path):
                failures.append(f"{bic}: MISSING {name}")
                sizes.append(None)
                continue
            size = os.path.getsize(path)
            sizes.append(size)
            if size < MIN_BYTES:
                failures.append(f"{bic}: CORRUPT/error-page ({size}B) {name}")

        if len(sizes) >= 2 and sizes[0] and sizes[1] and sizes[0] > sizes[1] * HERO_SIZE_RATIO:
            warnings.append(
                f"{bic}: hero {names[0]} is {sizes[0] // 1024}KB vs next {sizes[1] // 1024}KB "
                f"(>{HERO_SIZE_RATIO}x) — verify it is a product cutout, not a scene shot"
            )

    print(f"Products with images: {products_with_images} | image limit: {args.max}")
    if warnings:
        print(f"\nHERO WARNINGS ({len(warnings)}) — review manually, not auto-failing:")
        for w in warnings:
            print(f"  ? {w}")

    if failures:
        print(f"\nFAIL: {len(failures)} hard issue(s)")
        for fmsg in failures:
            print(f"  - {fmsg}")
        return 1

    print("\nPASS: all referenced images exist, are non-trivial, and within the limit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
