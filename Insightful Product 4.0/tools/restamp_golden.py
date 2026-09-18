#!/usr/bin/env python3
"""Re-stamp config/golden_set.json from the artifacts currently in outputs/.

This exists because `regression.sh --update` only ever PRINTED the new
checksums for a human to paste, while its own usage text claimed it wrote
the manifest. A re-stamp that silently keeps the old hashes is worse than
no re-stamp: `--verify` then fails on exactly the orgs you meant to bless,
or — if you paste selectively — passes against a manifest nobody re-derived.

Re-stamping is a deliberate act. Read the cohort diff first
(./tools/cohort_diff.sh --full), confirm every changed line is one you
intended, and only then run this.

Usage:
  tools/restamp_golden.py --note "why these hashes moved"   # writes
  tools/restamp_golden.py --dry-run                         # shows only
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "config" / "golden_set.json"
PY_BIN = ROOT / ".venv-renderer" / "bin" / "python"
ARTIFACT_KEYS = ("ship_html", "preview_html", "gatestop_md", "redirect_md")


def core_digest(path: pathlib.Path) -> tuple[str, int]:
    """sha256 + byte count of the deterministic core (prose slots removed)."""
    proc = subprocess.run(
        [str(PY_BIN), "-m", "pipeline.extract_deterministic_core", str(path)],
        capture_output=True,
        cwd=ROOT,
    )
    if proc.returncode != 0:
        raise SystemExit(
            f"extract_deterministic_core failed for {path.name}:\n"
            + proc.stderr.decode(errors="replace")
        )
    return hashlib.sha256(proc.stdout).hexdigest(), len(proc.stdout)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--note", default="", help="recorded as stamp_verification")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text())
    changed: list[tuple[str, str, str]] = []
    missing: list[str] = []

    for row in manifest["orgs"]:
        name = next((row[k] for k in ARTIFACT_KEYS if row.get(k)), None)
        if not name:
            missing.append(f"{row['org']}: no artifact key in manifest row")
            continue
        path = ROOT / "outputs" / name
        if not path.exists():
            missing.append(f"{row['org']}: {name} not in outputs/")
            continue
        sha, nbytes = core_digest(path)
        if row.get("deterministic_core_sha256") != sha:
            changed.append((row["org"], str(row.get("deterministic_core_sha256"))[:12], sha[:12]))
            row["deterministic_core_sha256"] = sha
            row["deterministic_core_bytes"] = nbytes

    if missing:
        # A partial re-stamp is how a manifest drifts out of step with the
        # cohort, so refuse rather than bless a subset.
        print("REFUSING to re-stamp — artifacts missing. Run ./tools/cohort_run.sh first:")
        for line in missing:
            print("  " + line)
        return 2

    for org, old, new in changed:
        print(f"  {org:<8} {old} -> {new}")
    print(f"\n{len(changed)} of {len(manifest['orgs'])} rows move.")

    if args.dry_run:
        print("--dry-run: config/golden_set.json left untouched.")
        return 0
    if not changed:
        print("Nothing to write.")
        return 0

    manifest["supersedes"] = manifest["version"]
    manifest["version"] = int(manifest["version"]) + 1
    manifest["stamped"] = _dt.date.today().isoformat()
    if args.note:
        manifest["stamp_verification"] = args.note
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {MANIFEST.relative_to(ROOT)} at version {manifest['version']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
