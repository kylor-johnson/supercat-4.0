#!/usr/bin/env python3
"""Measure what spike/ecat-web actually built, and map it onto Phase 3 units.

Produces scripts/spike.json. Two consumers:
  - Phase 3 `spike_status` (the field approved in Phase 0 sec 2.1)
  - Phase 6 calibration backtest

Method: `git diff --numstat` between the merge-base and origin/spike/ecat-web
gives added lines per file. Files are mapped to iPad units by an explicit,
inspectable path->unit table below. Unmapped files are reported, not silently
dropped.
"""
import collections
import json
import os
import subprocess

SPIKE = "/tmp/ecat-audit/server-ecatweb"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sh(cmd, cwd=SPIKE):
    return subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True,
                          text=True).stdout


BASE = sh("git merge-base origin/master origin/spike/ecat-web").strip()
HEAD = sh("git rev-parse origin/spike/ecat-web").strip()
numstat = sh(f"git diff --numstat {BASE} origin/spike/ecat-web")

from spike_map import MAP, CATEGORY  # noqa: E402

per_unit = collections.defaultdict(lambda: {"files": 0, "added": 0,
                                            "paths": []})
per_cat = collections.defaultdict(lambda: {"files": 0, "added": 0})
unmapped = []
total_added = 0

for line in numstat.strip().splitlines():
    parts = line.split("\t")
    if len(parts) != 3:
        continue
    add, _dele, path = parts
    add = 0 if add == "-" else int(add)
    total_added += add

    cat = next((c for sub, c in CATEGORY if sub in path), None)
    if cat:
        per_cat[cat]["files"] += 1
        per_cat[cat]["added"] += add
        if cat == "TESTS":
            # tests still attribute to a unit, for acceptance_determinism
            u = next((u for sub, u in MAP if sub in path), None)
            if u:
                per_unit[u].setdefault("test_files", 0)
                per_unit[u]["test_files"] = per_unit[u].get("test_files", 0) + 1
                per_unit[u]["test_added"] = per_unit[u].get("test_added", 0) + add
        continue

    unit = next((u for sub, u in MAP if sub in path), None)
    if unit is None:
        unmapped.append((path, add))
        continue
    per_unit[unit]["files"] += 1
    per_unit[unit]["added"] += add
    per_unit[unit]["paths"].append(path)

# --- design-doc titles: these are the SPECIFIED evidence -------------------
design_docs = sorted(
    p for p in sh(f"git diff --name-only {BASE} origin/spike/ecat-web").split()
    if p.startswith("docs/design") or p.startswith("docs/superpowers"))

out = {
    "method": ("git diff --numstat merge-base..origin/spike/ecat-web in "
               "/tmp/ecat-audit/server-ecatweb; path->unit map is the explicit "
               "MAP table in this script and is auditable file by file"),
    "merge_base": BASE,
    "spike_head": HEAD,
    "commits_ahead": int(sh("git rev-list --count origin/master.."
                            "origin/spike/ecat-web").strip() or 0),
    "total_lines_added": total_added,
    "per_unit": {k: v for k, v in sorted(per_unit.items(),
                                         key=lambda x: -x[1]["added"])},
    "per_category": dict(per_cat),
    "unmapped_files": unmapped,
    "design_doc_files": design_docs,
    "design_doc_count": len(design_docs),
}

with open(os.path.join(ROOT, "scripts", "spike.json"), "w") as f:
    json.dump(out, f, indent=1)

print(f"merge_base={BASE[:9]} head={HEAD[:9]} "
      f"commits={out['commits_ahead']} total_added={total_added}")
print(f"\n{'unit':30s} {'files':>6s} {'added':>7s} {'tests':>6s}")
for u, v in out["per_unit"].items():
    print(f"{u:30s} {v['files']:6d} {v['added']:7d} "
          f"{v.get('test_files', 0):6d}")
print(f"\n{'category':30s} {'files':>6s} {'added':>7s}")
for c, v in sorted(per_cat.items(), key=lambda x: -x[1]["added"]):
    print(f"{c:30s} {v['files']:6d} {v['added']:7d}")
print(f"\nunmapped: {len(unmapped)} files, "
      f"{sum(a for _, a in unmapped)} lines added")
for p, a in sorted(unmapped, key=lambda x: -x[1]):
    print(f"   {a:6d}  {p}")
