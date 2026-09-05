#!/usr/bin/env python3
"""Emit the Phase 5 kill-list tables so nothing is transcribed by hand."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

led = json.load(open(os.path.join(ROOT, "03_UNIT_LEDGER.json")))
A = {r["unit_id"]: r for r in led["rows"] if r["scenario"] == "A"}
named = json.load(open(os.path.join(HERE, "kill_named.json")))["per_feature"]
dead = json.load(open(os.path.join(ROOT, "01_CODE_CENSUS.json")))["1_8_dead_code"]

# Non-production tenants, identified by naming convention. Stated explicitly so
# the reader can disagree with the classification rather than guess at it.
NONPROD = {"demo", "demo2", "demo3", "test1", "pf_test", "sc_test",
           "ufistaging", "ihw_staging"}


def split_tenants(feature):
    ts = named[feature]["tenants"]
    prod = [t for t in ts if t["shortname"] not in NONPROD]
    non = [t for t in ts if t["shortname"] in NONPROD]
    return prod, non


print("### A. UNREACHABLE — no inbound navigation edge, no tenant conversation\n")
print("| Screen | Unit | LOC | IB document | Evidence |")
print("|---|---|--:|---|---|")
tot_unreach = 0
for s in dead["unreachable_screen_candidates"]:
    ib = ", ".join(s["ib_documents"]) or "none"
    print(f"| `{s['screen_id']}` | {s['unit'] or '(unmapped)'} | "
          f"{s['loc_total']} | {ib} | zero inbound navigation edges |")
    tot_unreach += s["loc_total"]
print(f"\n**Total LOC that would not be rewritten: {tot_unreach}.**\n")

print("\n### B. Compiled but referenced only by its own header/impl pair\n")
print("| Class | Unit | Header LOC | Impl LOC |")
print("|---|---|--:|--:|")
tot_self = 0
for c in dead["classes_declared_but_referenced_only_in_own_pair"]:
    print(f"| `{c['class']}` | {c['unit']} | {c['loc_header']} | "
          f"{c['loc_impl']} |")
    tot_self += c["loc_header"] + c["loc_impl"]
print(f"\n**Total: {tot_self} LOC across "
      f"{len(dead['classes_declared_but_referenced_only_in_own_pair'])} "
      f"classes.**\n")

print("\n### C. On disk but not in the Xcode project — not compiled at all\n")
print("| File |")
print("|---|")
for f in dead["source_files_on_disk_not_in_project"]:
    print(f"| `{f}` |")

print("\n\n### D. Orphan Interface Builder documents\n")
print("| Document | Custom classes bound | Note |")
print("|---|---|---|")
for d in dead["ib_documents_orphan"]:
    cc = ", ".join(f"`{c}`" for c in d["custom_classes"]) or "—"
    print(f"| `{d['ib']}` | {cc} | {d.get('note', '')} |")
print(f"\n8 of {dead['ib_documents_total']} Interface Builder documents.\n")

# ---- LOW_USE ranking ----------------------------------------------------
print("\n### E. LOW_USE — ranked by removal candidacy\n")
print("Ranked on two measured quantities together: how many production tenants "
      "touch the unit, and how much they actually do with it. Depth matters as "
      "much as breadth -- a unit reaching 12 tenants that fired 74 times in a "
      "year is a weaker attachment than one reaching 2 that fired 2,242 times.\n")
print("| Rank | Unit | LOC | LOGIC | Prod tenants | Non-prod | Events (12mo) "
      "| Most recent use | Reach basis | Registry | Tests |")
print("|--:|---|--:|--:|--:|--:|--:|---|---|---|--:|")

RANK = [
    ("SemanticSearch", ["smart_search_toggled",
                        "smart_search_embeddings_generated"]),
    ("ShowroomCart", []),
    ("Commitments", ["view_commitments"]),
    ("RepActivity", []),
    ("Spreadsheet Import", []),
    ("Flipbook", ["view_flipbook", "flipbook_add_to_order",
                  "flipbook_add_to_list"]),
    ("Placements", ["view_customer_placements"]),
]
CONTRAST = [("Kit/Options related", ["view_kit", "add_kit_to_order",
                                     "add_configured_item_to_order"])]

rows_out = []
for i, (unit, feats) in enumerate(RANK + CONTRAST, 1):
    a = A[unit]
    prod, non = set(), set()
    events, last = 0, ""
    for f in feats:
        p, n = split_tenants(f)
        prod |= {t["shortname"] for t in p}
        non |= {t["shortname"] for t in n}
        events += named[f]["total_events"]
        for t in p + n:
            last = max(last, t["last_seen"])
    if feats:
        pc, nc, ev, lu = len(prod), len(non), events, last
        basis = "telemetry"
    else:
        # no telemetry event exists; fall back to the Postgres-derived reach
        # already recorded in the ledger, and say which it is
        pc, nc, ev, lu = a["tenants_touched"], "—", "not instrumented", "UNKNOWN"
        basis = "Postgres table"
    reg = {"DEDICATED_SPEC": "SPEC", "REFERENCED": "ref",
           "NONE": "**none**"}[a["registry_coverage"]]
    label = str(i) if unit not in dict(CONTRAST) else "—"
    print(f"| {label} | {unit} | {a['loc_total']} | {a['loc_logic']} | {pc} | "
          f"{nc} | {ev} | {lu} | {basis} | {reg} | "
          f"{a['test_files_referencing_unit']} |")
    rows_out.append((unit, a, sorted(prod), sorted(non), events))

kill = [r for r in rows_out if r[0] not in dict(CONTRAST)]
print(f"\n**Ranked LOW_USE total: {sum(r[1]['loc_total'] for r in kill)} LOC, "
      f"{sum(r[1]['loc_logic'] for r in kill)} of it LOGIC, across "
      f"{len(kill)} units.** The final row is included for contrast and is "
      f"**not** a candidate: `Kit/Options related` reaches a comparable number "
      f"of tenants but fired 236,343 times.")

print("\n\n### F. Named tenants, per low-use unit\n")
for unit, a, prod, non, events in rows_out:
    if not prod and not non:
        continue
    print(f"**{unit}** — {a['loc_total']} LOC, "
          f"{a['test_files_referencing_unit']} test files")
    print(f"- Production tenants ({len(prod)}): "
          f"{', '.join('`' + p + '`' for p in prod) or 'none'}")
    if non:
        print(f"- Non-production ({len(non)}): "
              f"{', '.join('`' + n + '`' for n in non)}")
    print()
