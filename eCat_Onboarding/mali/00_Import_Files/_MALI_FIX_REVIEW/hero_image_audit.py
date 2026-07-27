#!/usr/bin/env python3
"""Audit every VISIBLE hero: does it show its own SKU-named image, or a borrowed one?"""
import csv, re
from collections import defaultdict

WORK = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/products.csv"
def n(s): return (s or "").strip()
def fi(s): s=n(s); return s.split(",")[0].strip() if s else ""
rows=list(csv.DictReader(open(WORK,encoding="utf-8-sig")))
visible=[r for r in rows if n(r["Hideable"]).upper()!="Y"]

def base(img): return re.sub(r"\.(jpg|jpeg|png|gif|webp)$","",img,flags=re.I)
def norm(x): return base(x).upper().replace("/","-")

own=[]; borrowed=[]; noimg=[]
# map image basename -> which visible SKU "owns" it (name match)
for r in visible:
    sku=n(r["BaseItemCode"]); img=fi(r["ImageFileName"])
    if not img: noimg.append(sku); continue
    if norm(img)==norm(sku):
        own.append(sku)
    else:
        borrowed.append((sku, img, n(r["ShortDesc"])))

print(f"VISIBLE heroes: {len(visible)}")
print(f"  Own SKU-named image (safe): {len(own)}")
print(f"  BORROWED image (audit):     {len(borrowed)}")
print(f"  No image:                   {len(noimg)} {noimg}")
print("\n=== BORROWED-IMAGE VISIBLE HEROES (each shows another SKU's file) ===")
for sku,img,sd in sorted(borrowed):
    print(f"  {sku:24} shows [{img:28}] | {sd}")
