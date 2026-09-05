"""Phase 3 inputs that are measurable: the inter-unit coupling graph.

coupling_fan_in  = number of OTHER units containing at least one file that
                   imports a header owned by this unit.
coupling_fan_out = number of OTHER units this unit imports a header from.

Both are counts of units, not of import statements, so a unit that is imported
400 times by one neighbour does not outrank one imported once by twenty. Local
imports (#import "Foo.h") are resolved against the file->unit map from
p1_units.py; system and Pod imports (<...>) are ignored because they say nothing
about internal coupling.
"""
import collections
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = "/tmp/ecat-audit/ios-master"

units = json.load(open(os.path.join(HERE, "units.json")))
file_to_unit = units["file_to_unit"]

# basename -> owning unit, for resolving #import "Foo.h"
owner = {os.path.basename(f): u for f, u in file_to_unit.items()}

IMPORT = re.compile(r'^\s*(?:#import|#include)\s+"([^"]+)"', re.M)
SWIFT_IMPORT = re.compile(r'^\s*import\s+([A-Za-z_][A-Za-z0-9_]*)', re.M)

edges = collections.Counter()          # (src_unit, dst_unit) -> import count
files_scanned = 0

for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames
                   if d not in ("Pods", ".git", "build", "DerivedData")]
    for fn in filenames:
        if os.path.splitext(fn)[1] not in (".m", ".mm", ".h", ".swift"):
            continue
        src_unit = file_to_unit.get(fn)
        if not src_unit:
            continue
        path = os.path.join(dirpath, fn)
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        files_scanned += 1
        for inc in IMPORT.findall(text):
            dst_unit = owner.get(os.path.basename(inc))
            if dst_unit and dst_unit != src_unit:
                edges[(src_unit, dst_unit)] += 1

fan_in = collections.defaultdict(set)
fan_out = collections.defaultdict(set)
for (s, d), n in edges.items():
    fan_out[s].add(d)
    fan_in[d].add(s)

all_units = sorted(set(file_to_unit.values()))
result = {
    "method": ("count of DISTINCT neighbouring units, resolved via local "
               "#import \"...\" against the p1_units.py file->unit map; "
               "system/Pod imports excluded"),
    "files_scanned": files_scanned,
    "distinct_unit_edges": len(edges),
    "total_local_imports": sum(edges.values()),
    "units": {},
    "source": (f"os.walk over {ROOT} (commit pinned in 01_CODE_CENSUS.json) "
               "+ scripts/units.json"),
}
for u in all_units:
    result["units"][u] = {
        "coupling_fan_in": len(fan_in[u]),
        "coupling_fan_out": len(fan_out[u]),
        "fan_in_units": sorted(fan_in[u]),
        "fan_out_units": sorted(fan_out[u]),
        "imports_received": sum(n for (s, d), n in edges.items() if d == u),
        "imports_emitted": sum(n for (s, d), n in edges.items() if s == u),
    }

with open(os.path.join(HERE, "coupling.json"), "w") as fh:
    json.dump(result, fh, indent=2)

print(f"files_scanned={files_scanned} edges={len(edges)} "
      f"imports={sum(edges.values())}")
print(f"\n{'unit':<32}{'fan_in':>7}{'fan_out':>8}{'recv':>7}{'emit':>7}")
for u in sorted(all_units, key=lambda x: -result["units"][x]["coupling_fan_in"]):
    r = result["units"][u]
    if r["coupling_fan_in"] or r["coupling_fan_out"]:
        print(f"{u:<32}{r['coupling_fan_in']:>7}{r['coupling_fan_out']:>8}"
              f"{r['imports_received']:>7}{r['imports_emitted']:>7}")
