#!/usr/bin/env python3
"""Build uniformly-sized, square option/swatch images for eCat FTP /option_images.

Why: option swatches imported at Catsy's native (non-square, mixed) dimensions
render unevenly on the iPad. This normalizes every swatch referenced by
options.csv to a single square canvas (default 1000x1000, white background),
so they all line up.

Source priority for each swatch file:
  1. swatch_source/<filename>      (drop originals here to override / supply
                                    anything the manifest can't provide, e.g.
                                    the Finishes_*_750px.jpg files)
  2. catsy_url from the manifest   (option_images_ftp_manifest.csv)

Output: option_images_upload/<filename>  -> upload that folder to FTP /option_images.
Anything that can't be sourced is listed in swatch_build_report.csv.

macOS only (uses `sips`). Run:  python3 build_uniform_swatches.py
"""
from __future__ import annotations

import csv
import subprocess
import urllib.request
from pathlib import Path

SIZE = 1000          # final square edge in px
PAD_COLOR = "FFFFFF"  # canvas background (hex, no #)

BASE = Path(__file__).parent
OPTIONS = BASE / "options.csv"
SRC_DIR = BASE / "swatch_source"
OUT_DIR = BASE / "option_images_upload"
REPORT = BASE / "swatch_build_report.csv"
MANIFEST_CANDIDATES = [
    BASE / "option_images_ftp_manifest.csv",
    BASE.parent / "CS_eCat_Rebuild" / "option_images_ftp_manifest.csv",
]


def load_manifest() -> dict[str, str]:
    for path in MANIFEST_CANDIDATES:
        if path.exists():
            with path.open(newline="", encoding="utf-8") as f:
                return {
                    (row.get("ftp_filename") or "").strip(): (row.get("catsy_url") or "").strip()
                    for row in csv.DictReader(f)
                    if (row.get("ftp_filename") or "").strip()
                }
    return {}


def needed_filenames() -> list[str]:
    seen: dict[str, None] = {}
    with OPTIONS.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = (row.get("ImageName") or "").strip()
            if name and not name.startswith("http"):
                seen.setdefault(name, None)
    return list(seen)


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "SuperCat-swatch/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dest.write_bytes(resp.read())


def squarify(src: Path, dest: Path) -> None:
    """Resize to fit within SIZE, then pad to an exact SIZE x SIZE square."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "92",
         "-Z", str(SIZE), str(src), "--out", str(dest)],
        check=True, capture_output=True,
    )
    subprocess.run(
        ["sips", "-p", str(SIZE), str(SIZE), "--padColor", PAD_COLOR, str(dest)],
        check=True, capture_output=True,
    )
    subprocess.run(
        ["sips", "-m", "/System/Library/ColorSync/Profiles/sRGB Profile.icc", str(dest)],
        check=False, capture_output=True,
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    names = needed_filenames()
    tmp = BASE / ".swatch_tmp"

    rows = []
    ok = missing = 0
    for name in sorted(names):
        local = SRC_DIR / name
        out = OUT_DIR / name
        src_kind = note = ""
        try:
            if local.exists():
                src_kind = "local"
                squarify(local, out)
            elif name in manifest and manifest[name]:
                src_kind = "manifest"
                download(manifest[name], tmp)
                squarify(tmp, out)
                tmp.unlink(missing_ok=True)
            else:
                missing += 1
                rows.append({"filename": name, "source": "MISSING",
                             "note": "no local file and no manifest URL — drop original in swatch_source/"})
                print(f"MISSING: {name}")
                continue
            ok += 1
            print(f"ok ({src_kind}): {name}")
        except Exception as exc:  # noqa: BLE001
            missing += 1
            note = str(exc)
            rows.append({"filename": name, "source": src_kind or "error", "note": note})
            print(f"error: {name} — {note}")
            continue
        rows.append({"filename": name, "source": src_kind, "note": ""})

    with REPORT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["filename", "source", "note"])
        w.writeheader()
        w.writerows(rows)

    print(f"\nDone. {ok} built, {missing} need a source file.")
    print(f"Built squares: {OUT_DIR.name}/  ->  upload to FTP /option_images")
    print(f"Report:        {REPORT.name}")


if __name__ == "__main__":
    main()
