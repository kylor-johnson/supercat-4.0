#!/usr/bin/env python3
"""Detailed orphan-hidden analysis + family grouping for Magic Lite."""
import csv, re
from collections import defaultdict

WORK = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/products.csv"

def load(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))
def n(s): return (s or "").strip()
def first_img(s):
    s=n(s); return s.split(",")[0].strip() if s else ""
def rel(s):
    s=n(s); return [x.strip() for x in s.split(",") if x.strip()] if s else []

rows = load(WORK)
by = {n(r["BaseItemCode"]): r for r in rows}
visible = [r for r in rows if n(r.get("Hideable","")).upper()!="Y"]
hidden  = [r for r in rows if n(r.get("Hideable","")).upper()=="Y"]
referenced=set()
for r in rows:
    for x in rel(r.get("RelatedItems","")): referenced.add(x)
orphans=[r for r in hidden if n(r["BaseItemCode"]) not in referenced]

# map: visible hero image -> [visible skus]
vis_by_img=defaultdict(list)
for r in visible:
    im=first_img(r.get("ImageFileName","")).lower()
    if im: vis_by_img[im].append(n(r["BaseItemCode"]))

# For each orphan: does its hero image match a visible product?
share=[]; noshare=[]
for r in orphans:
    sku=n(r["BaseItemCode"]); im=first_img(r.get("ImageFileName","")).lower()
    if im and im in vis_by_img:
        share.append((sku, im, vis_by_img[im]))
    else:
        noshare.append((sku, im))

print(f"ORPHANS: {len(orphans)}  share-with-visible: {len(share)}  no-visible-sibling: {len(noshare)}\n")

print("========== GROUP A: orphan shares image with a VISIBLE product (=> add to that parent's RelatedItems) ==========")
# group by the visible parent (first visible sku of that image)
grp=defaultdict(list)
for sku,im,vskus in share:
    parent=sorted(vskus)[0]
    grp[(im,tuple(sorted(vskus)))].append(sku)
for (im,vskus),skus in sorted(grp.items()):
    print(f"\n  IMG {im}  visible-parents={vskus}")
    for s in sorted(skus):
        r=by[s]; print(f"     + {s:24} | {n(r['ShortDesc'])} | {n(r['LongDesc'])[:60]}")

print("\n\n========== GROUP B: orphan with NO visible image-sibling ==========")
# Try to bucket by SKU prefix family
def fam(sku):
    m=re.match(r'^([A-Za-z]+(?:-[A-Za-z0-9]+)?)', sku)
    return m.group(1) if m else sku
fams=defaultdict(list)
for sku,im in noshare:
    fams[fam(sku)].append(sku)
for f in sorted(fams):
    print(f"\n  FAMILY {f}  ({len(fams[f])})")
    for s in sorted(fams[f]):
        r=by[s]; print(f"     - {s:26} | H:{n(r['Hideable'])} | {n(r['ShortDesc'])[:34]:34} | img={first_img(r.get('ImageFileName',''))} | W:{n(r['PowerConsumption_W'])} mm:{n(r['Dimensions_mm'])[:18]}")
