#!/usr/bin/env python3
"""Measure the eCat component registry's coverage of each Phase 3 unit.

The registry (docs/design/ecat-component-registry/, 22 files on
supercat_server origin/master) documents the iPad app. It was NOT found in
Phase 1 because Phase 1 searched the iOS repo only. This script measures its
per-unit coverage MECHANICALLY: the registry names iOS source files, so every
file reference is resolved through the same file->unit map used everywhere
else. No judgement about which doc "covers" which unit.

Output: scripts/registry.json
"""
import collections
import json
import os
import re
import subprocess

SERVER = "/tmp/ecat-audit/server-ecatweb"
REG = "docs/design/ecat-component-registry"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

units = json.load(open(os.path.join(ROOT, "scripts", "units.json")))
file_to_unit = units["file_to_unit"] if "file_to_unit" in units else units


def sh(cmd):
    return subprocess.run(cmd, shell=True, cwd=SERVER, capture_output=True,
                          text=True).stdout


files = [f for f in sh(f"git ls-tree -r --name-only origin/master -- {REG}")
         .split() if f.strip()]

# every basename we know how to attribute
basename_to_unit = {}
for path, unit in file_to_unit.items():
    basename_to_unit[os.path.basename(path)] = unit

# iOS source references inside the registry
REFPAT = re.compile(r'\b([A-Za-z_][A-Za-z0-9_+]*\.(?:h|m|mm|swift))\b')

per_unit_refs = collections.defaultdict(collections.Counter)
per_file_lines = {}
unresolved = collections.Counter()
doc_to_units = {}

for f in files:
    text = sh(f"git show origin/master:{f}")
    per_file_lines[f] = text.count("\n")
    hits = collections.Counter()
    for ref in REFPAT.findall(text):
        u = basename_to_unit.get(ref)
        if u is None:
            unresolved[ref] += 1
            continue
        hits[u] += 1
        per_unit_refs[u][ref] += 1
    doc_to_units[f] = dict(hits.most_common())

total_lines = sum(per_file_lines.values())

summary = {}
for u, refs in per_unit_refs.items():
    summary[u] = {
        "distinct_ios_files_documented": len(refs),
        "total_references": sum(refs.values()),
        "docs_covering_unit": sorted(
            d for d, h in doc_to_units.items() if u in h),
    }

# how much of each unit's own file set is documented
unit_file_counts = collections.Counter(file_to_unit.values())
for u, s in summary.items():
    tot = unit_file_counts.get(u, 0)
    s["unit_total_files"] = tot
    s["pct_files_documented"] = (round(100.0 * s["distinct_ios_files_documented"]
                                       / tot, 1) if tot else None)

out = {
    "method": ("regex scan for iOS source basenames (*.h/*.m/*.mm/*.swift) "
               "across all 22 registry files on supercat_server "
               "origin/master, resolved through the same scripts/units.json "
               "file->unit map used in Phase 1 and Phase 3"),
    "registry_path": f"supercat_server:origin/master:{REG}",
    "registry_files": len(files),
    "registry_total_lines": total_lines,
    "registry_dated": "2026-04-03 (per _overview.yaml and _validation-report.yaml)",
    "per_file_lines": per_file_lines,
    "doc_to_units": doc_to_units,
    "per_unit": dict(sorted(summary.items(),
                            key=lambda x: -x[1]["distinct_ios_files_documented"])),
    "unresolved_reference_sample": dict(unresolved.most_common(25)),
    "unresolved_distinct": len(unresolved),
}
with open(os.path.join(ROOT, "scripts", "registry.json"), "w") as fh:
    json.dump(out, fh, indent=1)

print(f"registry: {len(files)} files, {total_lines} lines, "
      f"dated {out['registry_dated']}")
print(f"\n{'unit':32s} {'docd':>5s} {'tot':>4s} {'pct':>6s} {'refs':>5s}")
for u, s in out["per_unit"].items():
    print(f"{u:32s} {s['distinct_ios_files_documented']:5d} "
          f"{s['unit_total_files']:4d} "
          f"{str(s['pct_files_documented']) + '%':>6s} "
          f"{s['total_references']:5d}")

undoc = sorted(set(unit_file_counts) - set(summary))
print(f"\nunits with ZERO registry references ({len(undoc)}):")
for u in undoc:
    print(f"   {u}  ({unit_file_counts[u]} files)")
print(f"\nunresolved basenames: {len(unresolved)} distinct "
      f"(server-side or renamed files)")
