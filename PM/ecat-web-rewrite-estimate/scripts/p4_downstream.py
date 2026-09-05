#!/usr/bin/env python3
"""Phase 4 support: roll up downstream LOC / tenant counts per invention item.

Every number printed here is a sum over Phase 3 ledger rows, so the invention
register cites measured downstream exposure rather than asserted exposure.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

rows = json.load(open(os.path.join(ROOT, "03_UNIT_LEDGER.json")))["rows"]
A = {r["unit_id"]: r for r in rows if r["scenario"] == "A"}
B = {r["unit_id"]: r for r in rows if r["scenario"] == "B"}


def rollup(names, tag):
    loc = sum(A[n]["loc_total"] for n in names)
    logic = sum(A[n]["loc_logic"] for n in names)
    tn = [A[n]["tenants_touched"] for n in names]
    nums = [t for t in tn if isinstance(t, int)]
    unk = len(tn) - len(nums)
    print(f"\n--- {tag}")
    print(f"  units={len(names)} loc_total={loc} loc_logic={logic} "
          f"max_tenants={max(nums) if nums else 'n/a'} unknown_tenants={unk}")
    for n in sorted(names, key=lambda x: -A[x]["loc_total"]):
        r = A[n]
        print(f"    {n:34s} {r['loc_total']:6d} LOC  logic={r['loc_logic']:5d}  "
              f"tenants={r['tenants_touched']}  A={r['port_class']:25s} "
              f"B={B[n]['port_class']}")
    return dict(units=len(names), loc_total=loc, loc_logic=logic)


# --- hazard -> units carrying it -----------------------------------------
haz_units = {}
for n, r in A.items():
    for h in r["port_hazards"]:
        hid, equiv = h.split(":", 1)
        haz_units.setdefault((hid, equiv), []).append(n)

print("=" * 72)
print("HAZARD DOWNSTREAM (REQUIRES_PRODUCT_DECISION hazards only)")
print("=" * 72)
haz_roll = {}
for (hid, equiv), names in sorted(haz_units.items()):
    if equiv != "REQUIRES_PRODUCT_DECISION":
        continue
    haz_roll[hid] = rollup(names, f"hazard {hid}")

# --- invention / RPD / unknown units ------------------------------------
print("\n" + "=" * 72)
print("PORT-CLASS GROUPS")
print("=" * 72)
inv_a = [n for n, r in A.items() if r["port_class"] == "INVENTION"]
inv_b = [n for n, r in B.items() if r["port_class"] == "INVENTION"]
rpd = [n for n, r in A.items() if r["port_class"] == "REQUIRES_PRODUCT_DECISION"]
unk = [n for n, r in A.items() if r["port_class"] == "UNKNOWN"]
rollup(inv_a, "INVENTION under Scenario A")
rollup(inv_b, "INVENTION under Scenario B")
rollup(rpd, "REQUIRES_PRODUCT_DECISION (keep/kill precedes port class)")
rollup(unk, "UNKNOWN port class")

# --- fidelity bar UNDECIDED ---------------------------------------------
und = [n for n, r in A.items() if r["fidelity_bar"] == "UNDECIDED"]
rollup(und, "fidelity_bar UNDECIDED")

# --- units differing between scenarios ----------------------------------
diff = [n for n in A if A[n]["port_class"] != B[n]["port_class"]]
rollup(diff, "port_class differs between scenarios (the fork's blast radius)")

# --- CONTESTED specification --------------------------------------------
con = [n for n, r in A.items() if r["behavior_specification"] == "CONTESTED"]
rollup(con, "behavior_specification CONTESTED")

# --- tenants_touched UNKNOWN --------------------------------------------
tu = [n for n, r in A.items() if not isinstance(r["tenants_touched"], int)]
rollup(tu, "tenants_touched UNKNOWN (unmeasured reach)")
