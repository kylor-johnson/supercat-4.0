"""Emit the markdown tables for 03_UNIT_LEDGER.md so nothing is transcribed."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "..", "03_UNIT_LEDGER.json")))
rows = d["rows"]
byu = {}
for r in rows:
    byu.setdefault(r["unit_id"], {})[r["scenario"]] = r

order = sorted(byu, key=lambda u: -byu[u]["A"]["loc_total"])

print("### Master ledger\n")
print("| Unit | LOC | UI | LOGIC | GLUE | UNCL | A | B | Blast | Tenants | "
      "Rev | Spec | Accept | Fidelity | in | out | Spike | Reg |")
print("|---|--:|--:|--:|--:|--:|---|---|---|--:|---|---|---|---|--:|--:|---|---|")
for u in order:
    a, b = byu[u]["A"], byu[u]["B"]
    ac = {"MECHANICAL": "MECH", "RESPECIFICATION": "RESPEC",
          "INVENTION": "**INV**", "REQUIRES_PRODUCT_DECISION": "RPD",
          "UNKNOWN": "UNK"}
    sp = {"CODE_ONLY": "CODE_ONLY", "CONTESTED": "**CONTESTED**",
          "SPECIFIED": "SPEC"}
    acc = {"TEST_EXISTS": "TEST", "TESTABLE_NOT_TESTED": "TESTABLE",
           "HUMAN_JUDGMENT_ONLY": "HUMAN"}
    fid = {"OUTCOME_EQUIVALENT": "OUTCOME", "BEHAVIOR_PARITY": "BEHAVIOR",
           "PIXEL_PARITY": "PIXEL", "UNDECIDED": "UNDECIDED"}
    br = {"ISOLATED": "ISO", "MULTI_SURFACE": "MULTI", "SPINE": "**SPINE**",
          "UNKNOWN": "UNK"}
    rev = {"DUAL_RUNNABLE": "DUAL", "FLAGGABLE": "FLAG",
           "CUTOVER_ONLY": "CUTOVER", "UNKNOWN": "UNK"}
    spk = {"PARTIALLY_BUILT": "**PART**", "PATTERN_ESTABLISHED": "pat",
           "NOT_STARTED": "--"}
    rg = {"DEDICATED_SPEC": "**SPEC**", "REFERENCED": "ref", "NONE": "--"}
    print(f"| {u} | {a['loc_total']} | {a['loc_ui']} | {a['loc_logic']} | "
          f"{a['loc_glue']} | {a['loc_unclassified']} | {ac[a['port_class']]} | "
          f"{ac[b['port_class']]} | {br[a['blast_radius']]} | "
          f"{a['tenants_touched']} | {rev[a['reversibility']]} | "
          f"{sp[a['behavior_specification']]} | "
          f"{acc[a['acceptance_determinism']]} | "
          f"{fid[a['fidelity_bar']]} | {a['coupling_fan_in']} | "
          f"{a['coupling_fan_out']} | {spk[a['spike_status']]} | "
          f"{rg[a['registry_coverage']]} |")

t = {k: sum(byu[u]["A"][f"loc_{k}"] for u in byu)
     for k in ("ui", "logic", "glue", "unclassified", "total")}
print(f"| **TOTAL ({len(byu)} units)** | **{t['total']}** | **{t['ui']}** | "
      f"**{t['logic']}** | **{t['glue']}** | **{t['unclassified']}** | | | | "
      f"| | | | | | | | |")

print("\n\n### The two Phase 3 amendments, unit by unit\n")
print("Units whose `behavior_specification` changed once the component "
      "registry was found, and what the spike has already built.\n")
print("| Unit | LOC | First pass | Amended | Unit files named in registry | "
      "Spike lines added | Spike status |")
print("|---|--:|---|---|---|--:|---|")
for u in order:
    a = byu[u]["A"]
    if (a["behavior_specification"] != a["behavior_specification_first_pass"]
            or a["spike_lines_added"]):
        den = a["registry_unit_files_total"]
        cov = (f"{a['registry_ios_files_documented']} of {den} "
               f"({a['registry_pct_unit_files_documented']}%)" if den
               else "0 (no references)")
        print(f"| {u} | {a['loc_total']} | "
              f"{a['behavior_specification_first_pass']} | "
              f"{a['behavior_specification']} | {cov} | "
              f"{a['spike_lines_added']} | {a['spike_status']} |")

print("\n\n### Scenario delta, unit by unit\n")
print("| Unit | LOC | A | B | What changes |")
print("|---|--:|---|---|---|")
for u in order:
    a, b = byu[u]["A"], byu[u]["B"]
    if a["port_class"] != b["port_class"]:
        print(f"| {u} | {a['loc_total']} | {a['port_class']} | "
              f"{b['port_class']} | {a['scenario_delta']} |")

print("\n\n### Units with zero test coverage and majority LOGIC\n")
print("| Unit | LOC | LOGIC | LOGIC % | Tests | Spec | Accept |")
print("|---|--:|--:|--:|--:|---|---|")
risky = [u for u in order
         if byu[u]["A"]["test_files_referencing_unit"] == 0
         and byu[u]["A"]["loc_total"]
         and byu[u]["A"]["loc_logic"] / byu[u]["A"]["loc_total"] >= 0.5]
for u in risky:
    a = byu[u]["A"]
    pctl = round(100 * a["loc_logic"] / a["loc_total"], 1)
    print(f"| {u} | {a['loc_total']} | {a['loc_logic']} | {pctl}% | 0 | "
          f"{a['behavior_specification']} | {a['acceptance_determinism']} |")
print(f"\n{len(risky)} units, "
      f"{sum(byu[u]['A']['loc_logic'] for u in risky)} LOGIC LOC, "
      f"{sum(byu[u]['A']['loc_total'] for u in risky)} total LOC.")

print("\n\n### Hazards carried, by unit\n")
print("| Unit | Hazards |")
print("|---|---|")
for u in order:
    h = byu[u]["A"]["port_hazards"]
    if h:
        print(f"| {u} | {', '.join(h)} |")
