#!/usr/bin/env python3
"""Apply Magic Lite (mali) merchandising proposals to products.csv.
Usage:
  python3 apply_changes.py            # DRY RUN: simulate + validate, write nothing
  python3 apply_changes.py --write    # backup + write products.csv + changelog
Reads decisions from PROPOSAL_01_DUP_IMAGE_TRIAGE.csv and PROPOSAL_02_ORPHAN_FIX.csv
plus the trim-rebalance rule (encoded here to match build_proposals.py)."""
import csv, sys, os, shutil, datetime
from collections import defaultdict

WORK = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/products.csv"
BASE = "/Users/kylorjohnson/Downloads/products.csv.20260723-2122.csv"
REV  = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/00_Import_Files/_MALI_FIX_REVIEW/"
WRITE = "--write" in sys.argv

def n(s): return (s or "").strip()
def rel(s): s=n(s); return [x.strip() for x in s.split(",") if x.strip()] if s else []

with open(WORK, encoding="utf-8-sig", newline="") as f:
    rd=csv.DictReader(f); FIELDS=rd.fieldnames; rows=list(rd)
by={n(r["BaseItemCode"]):r for r in rows}
baseline_skus={n(r["BaseItemCode"]) for r in csv.DictReader(open(BASE,encoding="utf-8-sig"))}

def load_prop(fn):
    return list(csv.DictReader(open(REV+fn,encoding="utf-8-sig")))
dup=load_prop("PROPOSAL_01_DUP_IMAGE_TRIAGE.csv")
orp=load_prop("PROPOSAL_02_ORPHAN_FIX.csv")

changelog=[]  # (sku, field, old, new, reason)
add_to_parent=defaultdict(list)
del_from_parent=defaultdict(list)
for base in ["LVLDL-SR","LVLDL-SS"]:
    for sz in ["08","10","12"]:
        for fin in ["BK","BZ","BN"]:
            del_from_parent[f"{base}-06-WW-WH-L"].append(f"{base}-{sz}-TR-{fin}-L")

def set_field(sku, field, val, reason):
    r=by[sku]; old=n(r[field])
    if old!=n(val):
        r[field]=val; changelog.append((sku,field,old,n(val),reason))

def queue_relate(child,parent):
    if parent and parent in by:
        cur=rel(by[parent]["RelatedItems"])
        if child not in cur and child not in add_to_parent[parent]:
            add_to_parent[parent].append(child)

# ---- apply dup triage ----
for d in dup:
    sku=n(d["BaseItemCode"]); act=n(d["PROPOSED_action"])
    if sku not in by: print("MISSING",sku); continue
    if act in ("HIDE_RELATE","HIDE_RELATE_FIXIMG"):
        set_field(sku,"Hideable","Y","dup-triage: accessory/finish hidden")
        queue_relate(sku,n(d["relate_to"]))
        if n(d["image_change"]).upper()=="CLEAR":
            set_field(sku,"ImageFileName","","dup-triage: clear wrong shared image")
    elif act=="KEEP_FIXIMG":
        ic=n(d["image_change"])
        if ic and ic.upper()!="CLEAR":
            set_field(sku,"ImageFileName",ic,"dup-triage: fix wrong image to real product photo")
    elif act=="KEEP_CROSSRELATE":
        queue_relate(sku,n(d["relate_to"]))

# ---- apply orphan fix ----
for o in orp:
    sku=n(o["BaseItemCode"]); act=n(o["PROPOSED_action"])
    if sku not in by: print("MISSING",sku); continue
    if act=="UNHIDE":
        set_field(sku,"Hideable","N","orphan-fix: distinct size promoted to visible")
    elif act=="RELATE_TO_VISIBLE":
        queue_relate(sku,n(o["relate_to"]))
    # FLAG_CLIENT* and REVIEW: no change

# ---- apply RelatedItems removals then additions ----
for parent,dels in del_from_parent.items():
    if parent in by:
        cur=rel(by[parent]["RelatedItems"]); kept=[c for c in cur if c not in dels]
        if kept!=cur:
            set_field(parent,"RelatedItems",",".join(kept),"rebalance: drop redundant cross-size trim refs")
for parent,adds in add_to_parent.items():
    cur=rel(by[parent]["RelatedItems"]); new=cur+[c for c in adds if c not in cur]
    if new!=cur:
        set_field(parent,"RelatedItems",",".join(new),"relate children to hero")

# ================= VALIDATION =================
errors=[]
skus=[n(r["BaseItemCode"]) for r in rows]
cur_set=set(skus)
if cur_set!=baseline_skus:
    lost=baseline_skus-cur_set; added=cur_set-baseline_skus
    errors.append(f"SKU set changed! lost={sorted(lost)} added={sorted(added)}")
from collections import Counter
dups=[k for k,v in Counter(skus).items() if v>1]
if dups: errors.append(f"Duplicate BaseItemCodes: {dups}")
for r in rows:
    sku=n(r["BaseItemCode"]); ri=n(r["RelatedItems"])
    if len(ri)>255: errors.append(f"{sku}: RelatedItems {len(ri)}>255")
    for ref in rel(ri):
        if ref not in cur_set: errors.append(f"{sku}: dangling RelatedItems ref {ref}")

visible=sum(1 for r in rows if n(r["Hideable"]).upper()!="Y")
hidden=len(rows)-visible
referenced=set()
for r in rows:
    for x in rel(r["RelatedItems"]): referenced.add(x)
orphans=sum(1 for r in rows if n(r["Hideable"]).upper()=="Y" and n(r["BaseItemCode"]) not in referenced)

print(f"--- {'WRITE' if WRITE else 'DRY-RUN'} SIMULATION RESULT ---")
print(f"Total SKUs : {len(rows)} (baseline {len(baseline_skus)})")
print(f"Visible    : {visible}   Hidden: {hidden}")
print(f"Orphaned-hidden (remaining): {orphans}")
print(f"Changelog line items: {len(changelog)}")
print(f"VALIDATION ERRORS: {len(errors)}")
for e in errors[:50]: print("   !!",e)

if WRITE and not errors:
    ts=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bak=WORK.replace("products.csv",f"products.csv.bak_mergefix_{ts}")
    shutil.copy2(WORK,bak); print("Backup:",bak)
    with open(WORK,"w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    with open(REV+f"FIX_CHANGELOG_MERGE_{ts}.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(["BaseItemCode","field","old","new","reason"])
        for c in changelog: w.writerow(c)
    print(f"WROTE {WORK}")
    print(f"WROTE changelog FIX_CHANGELOG_MERGE_{ts}.csv ({len(changelog)} rows)")
elif WRITE and errors:
    print("REFUSING TO WRITE due to validation errors.")
