"""Bound the coupling measure's blind spot.

p3_coupling.py resolves `#import "Foo.h"`. Swift has no per-file import of a
sibling type -- within one module, Swift types are visible without any import
statement. So a Swift-only unit necessarily scores fan_in=0/fan_out=0 even when
it is heavily used. Compute Swift LOC share per unit so every zero can be
labelled either MEASURED_ISOLATED (Obj-C, genuinely no edges) or
UNKNOWN_SWIFT_OPAQUE (Swift, measure cannot see it).
"""
import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
loc = json.load(open(os.path.join(HERE, "loc_split.json")))
coupling = json.load(open(os.path.join(HERE, "coupling.json")))

by_unit = collections.defaultdict(lambda: collections.Counter())
for f in loc["files"]:
    by_unit[f["unit"]][f["ext"]] += f["code_lines"]

rows = []
for u, exts in by_unit.items():
    total = sum(exts.values())
    swift = exts.get(".swift", 0)
    c = coupling["units"].get(u, {})
    fi, fo = c.get("coupling_fan_in", 0), c.get("coupling_fan_out", 0)
    swift_pct = round(100.0 * swift / total, 1) if total else 0.0
    if fi == 0 and fo == 0:
        verdict = ("UNKNOWN_SWIFT_OPAQUE" if swift_pct >= 50
                   else "MEASURED_ISOLATED")
    elif swift_pct >= 50:
        verdict = "PARTIAL_SWIFT_OPAQUE"
    else:
        verdict = "MEASURED"
    rows.append({"unit": u, "loc": total, "swift_loc": swift,
                 "swift_pct": swift_pct, "fan_in": fi, "fan_out": fo,
                 "coupling_confidence": verdict})

rows.sort(key=lambda r: -r["loc"])
out = {
    "method": ("Swift LOC share per unit from loc_split.json, joined to "
               "coupling.json. Swift sibling types need no import statement, "
               "so coupling counts are structurally blind to Swift-only units."),
    "units": rows,
    "source": "scripts/loc_split.json + scripts/coupling.json",
}
with open(os.path.join(HERE, "swiftshare.json"), "w") as fh:
    json.dump(out, fh, indent=2)

print(f"{'unit':<32}{'LOC':>7}{'swift%':>8}{'in':>4}{'out':>5}  confidence")
for r in rows:
    print(f"{r['unit']:<32}{r['loc']:>7}{r['swift_pct']:>8}{r['fan_in']:>4}"
          f"{r['fan_out']:>5}  {r['coupling_confidence']}")
