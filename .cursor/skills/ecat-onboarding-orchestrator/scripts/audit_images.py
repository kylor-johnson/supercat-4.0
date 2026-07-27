#!/usr/bin/env python3
"""Audit the images referenced by an eCat products.csv.

Hard failures (exit 1): missing files, corrupt/error-page files (< 500 bytes), more
images than the org's limit, filenames the importer rejects, unfetchable URLs, a primary
image absent from the org's uploaded set, and images invented for SKUs that are blank at
source. Hero-image warnings are heuristic and printed but do not fail the run.

Three delivery classes, and they need different evidence:

1. **Local disk** — the original mode, and the narrowest. Most clients upload straight to
   FTP/Admin and never stage images in the repo (mali had 691 live against 17 staged), so
   a clean local audit proves very little on its own.
2. **The org's uploaded set** (`--live-images`) — the authoritative check. `image_exists`
   tracks only the FIRST filename, and eOL suppresses imageless products from search.
   That is what took Lib & Co's catalog off the portal while the iPad looked fine.
3. **CDN URLs** (`--check-urls`) — `ImageFileName` accepts a full HTTPS URL that eCat
   fetches itself. PNG is silently rejected at `:error` tier, which also suppresses every
   delete in the same import.

Usage:
    python audit_images.py products.csv /path/to/images [--max 6]
    python audit_images.py products.csv /path/to/images --live-images uploaded.txt
    python audit_images.py products.csv /path/to/images --check-urls
    python audit_images.py products.csv /path/to/images --source client_export.csv
"""
import argparse
import os
import sys

from preflight.checks import blanks, bom, image_urls, images_live
from preflight.core import FAIL, SKIP, WARNING, get, is_url, load_rows
from preflight.limits import image_filename_is_valid

MIN_BYTES = 500
HERO_SIZE_RATIO = 4  # image 1 this many times larger than image 2 => likely a scene shot


def read_list(path):
    """One value per line (or comma-separated); blanks and # comments ignored."""
    if not path:
        return None
    with open(path, "r", encoding="utf-8-sig") as f:
        out = []
        for line in f:
            line = line.split("#", 1)[0].strip()
            if line:
                out.extend(v.strip() for v in line.split(",") if v.strip())
        return out


def main():
    ap = argparse.ArgumentParser(description="Audit eCat product images")
    ap.add_argument("csv_path", help="path to products.csv")
    ap.add_argument("image_dir", help="directory holding the image files")
    ap.add_argument("--max", type=int, default=6,
                    help="max images per product (6 default, 12 with the paid flag)")
    ap.add_argument("--live-images", default=None,
                    help="file listing image filenames already uploaded for the org "
                         "(the authoritative check — see product_images)")
    ap.add_argument("--check-urls", action="store_true",
                    help="HEAD every URL in ImageFileName (network); without it, URLs "
                         "are classified by pattern only")
    ap.add_argument("--url-cache", default=None,
                    help="json file caching HEAD results so re-runs are free")
    ap.add_argument("--url-timeout", type=int, default=image_urls.DEFAULT_TIMEOUT)
    ap.add_argument("--source", default=None,
                    help="the client's own file, to prove blank-at-source stayed blank")
    ap.add_argument("--source-key", default=None, help="SKU column in --source")
    ap.add_argument("--source-image-field", default=None,
                    help="image column in --source")
    args = ap.parse_args()

    rows, lookup = load_rows(args.csv_path)
    if not rows:
        print("ERROR: no rows / empty header in file")
        return 2
    if "imagefilename" not in lookup:
        print("ERROR: no ImageFileName column")
        return 2

    failures, warnings, skipped = [], [], []
    products_with_images = 0
    url_refs = 0

    for finding in bom.run([args.csv_path]):
        failures.append(finding.render())

    for r in rows:
        bic = get(r, lookup, "BaseItemCode") or "?"
        raw = get(r, lookup, "ImageFileName")
        if not raw:
            continue
        products_with_images += 1
        names = [n.strip() for n in raw.split(",") if n.strip()]

        if len(names) > args.max:
            failures.append(f"{bic}: {len(names)} images > limit {args.max}")

        # URLs are a different delivery path — they are censused, not looked for on disk.
        local_names = []
        for name in names:
            if is_url(name):
                url_refs += 1
            else:
                local_names.append(name)
                ok, why = image_filename_is_valid(name)
                if not ok:
                    failures.append(f"{bic}: INVALID FILENAME {name} — {why}")

        sizes = []
        for name in local_names:
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
                f"{bic}: hero {local_names[0]} is {sizes[0] // 1024}KB vs next "
                f"{sizes[1] // 1024}KB (>{HERO_SIZE_RATIO}x) — verify it is a product "
                f"cutout, not a scene shot"
            )

    def absorb(findings):
        for f in findings:
            bucket = {FAIL: failures, WARNING: warnings, SKIP: skipped}.get(f.severity)
            if bucket is not None:
                bucket.append(f.render())

    absorb(image_urls.run(rows, lookup, check_network=args.check_urls,
                          timeout=args.url_timeout, cache_path=args.url_cache))
    absorb(images_live.run(rows, lookup, read_list(args.live_images)))
    absorb(blanks.run(rows, lookup, args.source,
                      source_key_field=args.source_key,
                      source_image_field=args.source_image_field))

    print(f"Products with images: {products_with_images} | image limit: {args.max}"
          + (f" | URL-delivered references: {url_refs}" if url_refs else ""))

    if skipped:
        print(f"\nSKIPPED ({len(skipped)}) — not applicable:")
        for s in skipped:
            print(f"  ~ {s}")

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
