#!/usr/bin/env python3
"""Phase 6: run the Phase 1 and Phase 3 substrate against the two named spikes.

CONTAMINATION DISCLOSURE, recorded in code so it cannot be dropped from the
writeup: docs/iphone-adaptation-plan.md on spike/iphone-compatibility contains
an "Effort Estimates" section and per-phase day ranges in its section headers.
Those headers were visible while locating the countable inventory. No figure
from them is read into this script or the Phase 6 document. See
06_CALIBRATION.md for what this does and does not compromise.

Output: scripts/calibration.json
"""
import collections
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, "scripts")

units = json.load(open(os.path.join(HERE, "units.json")))["file_to_unit"]
base = {os.path.basename(p): u for p, u in units.items()}

# The server spike's files are Ruby/ERB/CSS, not iOS basenames, so the
# basename map cannot resolve them. Reuse the explicit, auditable path->unit
# table already defined and used in p3_spike.py rather than duplicating it.
from spike_map import MAP as SERVER_MAP  # noqa: E402


def resolve(path, repo_key):
    if repo_key == "ecat-web":
        return next((u for sub, u in SERVER_MAP if sub in path), None)
    return base.get(os.path.basename(path))

SPIKES = {
    "ecat-web": dict(repo="/tmp/ecat-audit/server-ecatweb",
                     ref="origin/spike/ecat-web",
                     against="origin/master"),
    "iphone-compatibility": dict(repo="/tmp/ecat-audit/ios-master",
                                 ref="origin/spike/iphone-compatibility",
                                 against="origin/master"),
}


def sh(cmd, cwd):
    return subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True,
                          text=True).stdout


out = {"contamination_disclosure": (
    "docs/iphone-adaptation-plan.md contains an 'Effort Estimates' section and "
    "day ranges in phase headers. Headers were seen; no value was used. The "
    "measured substrate below is derived from git and scc only.")}

for name, cfg in SPIKES.items():
    repo, ref, against = cfg["repo"], cfg["ref"], cfg["against"]
    mb = sh(f"git merge-base {against} {ref}", repo).strip()
    numstat = sh(f"git diff --numstat {mb} {ref}", repo)

    per_unit = collections.defaultdict(lambda: {"files": 0, "added": 0,
                                                "deleted": 0})
    docs = {"files": 0, "added": 0}
    binary, unmapped = [], []
    tot_a = tot_d = 0
    for line in numstat.strip().splitlines():
        p = line.split("\t")
        if len(p) != 3:
            continue
        a, d, path = p
        if a == "-":
            binary.append(path)
            continue
        a, d = int(a), int(d)
        tot_a += a
        tot_d += d
        if path.startswith("docs/") or path.startswith("doc/"):
            docs["files"] += 1
            docs["added"] += a
            continue
        u = resolve(path, name)
        if u is None:
            unmapped.append((path, a, d))
            continue
        per_unit[u]["files"] += 1
        per_unit[u]["added"] += a
        per_unit[u]["deleted"] += d

    out[name] = {
        "repo": os.path.basename(repo),
        "ref": ref,
        "merge_base": mb,
        "commits_ahead": int(sh(f"git rev-list --count {against}..{ref}",
                                repo).strip() or 0),
        "files_changed": len(numstat.strip().splitlines()),
        "lines_added": tot_a,
        "lines_deleted": tot_d,
        "documentation": docs,
        "binary_files": binary,
        "units_touched": len(per_unit),
        "per_unit": {k: v for k, v in sorted(per_unit.items(),
                                             key=lambda x: -x[1]["added"])},
        "unmapped": sorted(unmapped, key=lambda x: -x[1]),
    }

with open(os.path.join(HERE, "calibration.json"), "w") as fh:
    json.dump(out, fh, indent=1)

for name in SPIKES:
    s = out[name]
    print(f"\n{'=' * 68}\n{name}  ({s['repo']} {s['ref']})")
    print(f"  merge_base={s['merge_base'][:9]} commits={s['commits_ahead']} "
          f"files={s['files_changed']}")
    print(f"  lines +{s['lines_added']} -{s['lines_deleted']}   "
          f"docs: {s['documentation']['files']} files / "
          f"+{s['documentation']['added']}   "
          f"binary: {len(s['binary_files'])}")
    print(f"  units touched: {s['units_touched']}")
    print(f"\n  {'unit':32s} {'files':>6s} {'+':>7s} {'-':>7s}")
    for u, v in s["per_unit"].items():
        print(f"  {u:32s} {v['files']:6d} {v['added']:7d} {v['deleted']:7d}")
    if s["unmapped"]:
        print(f"\n  unmapped ({len(s['unmapped'])} files):")
        for p, a, d in s["unmapped"][:12]:
            print(f"     +{a:<6} -{d:<6} {p}")
