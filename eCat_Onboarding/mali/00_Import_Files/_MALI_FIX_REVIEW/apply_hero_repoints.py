#!/usr/bin/env python3
"""Repoint the own-named WRONG hero sizes to their verified-clean sibling file.
LEDLB-5CCT-12/18/24/36/48 -> LEDLB-5CCT-10.jpg   (10" is the confirmed clean bar)
GDL-3-8W-38-CCT-WH, GDL-6-18W-38-CCT-WH -> GDL-4-14W-38-CCT-WH.jpg (4" confirmed clean gimbal)
Usage: python3 apply_hero_repoints.py [--write]
"""
import csv, sys, os, shutil, datetime
from collections import Counter

WORK="/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/products.csv"
BASE="/Users/kylorjohnson/Downloads/products.csv.20260723-2122.csv"
REV=os.path.dirname(os.path.abspath(__file__))
WRITE="--write" in sys.argv
def n(s): return (s or "").strip()
def rel(s): s=n(s); return [x.strip() for x in s.split(",") if x.strip()] if s else []

REPOINTS={
 "LEDLB-5CCT-12":"LEDLB-5CCT-10.jpg",
 "LEDLB-5CCT-18":"LEDLB-5CCT-10.jpg",
 "LEDLB-5CCT-24":"LEDLB-5CCT-10.jpg",
 "LEDLB-5CCT-36":"LEDLB-5CCT-10.jpg",
 "LEDLB-5CCT-48":"LEDLB-5CCT-10.jpg",
 "GDL-3-8W-38-CCT-WH":"GDL-4-14W-38-CCT-WH.jpg",
 "GDL-6-18W-38-CCT-WH":"GDL-4-14W-38-CCT-WH.jpg",
}
REASON="hero-fix: repoint to verified-clean sibling (catalogue pp.55 task bar / p.117 gimbal)"

with open(WORK,encoding="utf-8-sig",newline="") as f:
    rd=csv.DictReader(f); FIELDS=rd.fieldnames; rows=list(rd)
by={n(r["BaseItemCode"]):r for r in rows}
if os.path.exists(BASE):
    baseline_skus={n(r["BaseItemCode"]) for r in csv.DictReader(open(BASE,encoding="utf-8-sig"))}
    base_note="Downloads 7/23 baseline"
else:
    baseline_skus={n(r["BaseItemCode"]) for r in rows}  # ImageFileName-only edit; SKU set is invariant
    base_note="pre-edit working set (Downloads baseline offloaded)"
EXPECT_ROWS=683

changelog=[]
for sku,newimg in REPOINTS.items():
    if sku not in by: print("!! MISSING",sku); continue
    r=by[sku]; old=n(r["ImageFileName"])
    if old!=newimg:
        r["ImageFileName"]=newimg; changelog.append((sku,"ImageFileName",old,newimg,REASON))

# validation
errors=[]
skus=[n(r["BaseItemCode"]) for r in rows]; cur=set(skus)
if len(rows)!=EXPECT_ROWS: errors.append(f"row count {len(rows)} != {EXPECT_ROWS}")
if cur!=baseline_skus: errors.append("SKU set changed!")
dups=[k for k,v in Counter(skus).items() if v>1]
if dups: errors.append(f"dupes {dups}")
vis=sum(1 for r in rows if n(r["Hideable"]).upper()!="Y")
for r in rows:
    ri=n(r["RelatedItems"])
    if len(ri)>255: errors.append(f"{n(r['BaseItemCode'])} RelatedItems>{255}")
    for x in rel(ri):
        if x not in cur: errors.append(f"{n(r['BaseItemCode'])} dangling {x}")
# every referenced hero image target must exist as a file that's uploadable; just report the target set
print(f"--- {'WRITE' if WRITE else 'DRY-RUN'} --- (baseline: {base_note})")
print(f"rows={len(rows)} visible={vis} hidden={len(rows)-vis}")
print(f"changelog items={len(changelog)}")
for c in changelog: print("   ",c[0],"->",c[3])
print(f"VALIDATION ERRORS: {len(errors)}")
for e in errors[:50]: print("  !!",e)

if WRITE and not errors:
    ts=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bak=WORK.replace("products.csv",f"products.csv.bak_herofix_{ts}")
    shutil.copy2(WORK,bak); print("Backup:",bak)
    with open(WORK,"w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    with open(os.path.join(REV,f"FIX_CHANGELOG_HEROIMG_{ts}.csv"),"w",newline="") as f:
        w=csv.writer(f); w.writerow(["BaseItemCode","field","old","new","reason"]); w.writerows(changelog)
    print("WROTE",WORK); print(f"WROTE FIX_CHANGELOG_HEROIMG_{ts}.csv")
elif WRITE and errors:
    print("REFUSING TO WRITE.")
