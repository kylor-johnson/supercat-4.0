#!/usr/bin/env python3
"""Audit the HIDDEN products' hero images (they show as Related-Items thumbnails).
Flags cross-family borrows (a hidden SKU whose primary image is owned by a DIFFERENT
product family) — the strongest signal of a wrong/misleading thumbnail."""
import csv, re, os
from collections import defaultdict, OrderedDict, Counter
REV=os.path.dirname(os.path.abspath(__file__))
WORK="/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/products.csv"
CATTXT=os.path.join(REV,"catalogue","_alltext.txt")
def n(s): return (s or "").strip()
def fi(s): s=n(s); return s.split(",")[0].strip() if s else ""
def basen(img): return re.sub(r"\.(jpg|jpeg|png|gif|webp)$","",img,flags=re.I).upper().replace("/","-")
def rel(s): s=n(s); return [x.strip() for x in s.split(",") if x.strip()] if s else []

rows=list(csv.DictReader(open(WORK,encoding="utf-8-sig")))
by={n(r["BaseItemCode"]):r for r in rows}
visible=[r for r in rows if n(r["Hideable"]).upper()!="Y"]
hidden =[r for r in rows if n(r["Hideable"]).upper()=="Y"]
sku_norm={n(r["BaseItemCode"]).upper().replace("/","-"): n(r["BaseItemCode"]) for r in rows}

# who is referenced (reachable) via RelatedItems
referenced=set()
for r in rows:
    for x in rel(r["RelatedItems"]): referenced.add(x)

def fam(sku):
    # family key = strip trailing size/finish; use first 2 hyphen tokens, but keep known stems
    p=sku.upper().replace("/","-").split("-")
    return "-".join(p[:2]) if len(p)>1 else p[0]

# map image-basename -> SKU that name-owns it (visible preferred)
owner={}
for r in rows:
    sku=n(r["BaseItemCode"]); b=basen(fi(r["ImageFileName"]))
    if b==sku.upper().replace("/","-"):
        owner[b]=sku
# also record any visible sku owning
vis_owner={}
for r in visible:
    sku=n(r["BaseItemCode"]); b=basen(fi(r["ImageFileName"]))
    if b==sku.upper().replace("/","-"): vis_owner[b]=sku

out=[]
own_ct=borrow_same=borrow_cross=noimg=0
for r in hidden:
    sku=n(r["BaseItemCode"]); img=fi(r["ImageFileName"]); b=basen(img); sd=n(r["ShortDesc"])
    reach = "Y" if sku in referenced else "N"
    if not img:
        cat="NO_IMAGE"; src=""; noimg+=1
    elif b==sku.upper().replace("/","-"):
        cat="OWN_NAMED"; src=""; own_ct+=1
    else:
        src_sku=owner.get(b) or sku_norm.get(b) or "?"
        if src_sku!="?" and fam(src_sku)==fam(sku):
            cat="BORROW_SAME_FAMILY"; borrow_same+=1
        else:
            cat="BORROW_CROSS_FAMILY"; borrow_cross+=1
        src=f"{b} (owned by {src_sku})"
    out.append(OrderedDict(BaseItemCode=sku,family=fam(sku),ShortDesc=sd,primary_image=img,
        image_kind=cat,image_source=src,reachable=reach))

out.sort(key=lambda d:(d["image_kind"],d["family"],d["BaseItemCode"]))
with open(os.path.join(REV,"_audit_hidden.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)

print(f"HIDDEN: {len(hidden)}")
print(f"  OWN_NAMED            : {own_ct}")
print(f"  BORROW_SAME_FAMILY   : {borrow_same}")
print(f"  BORROW_CROSS_FAMILY  : {borrow_cross}  <-- suspect thumbnails")
print(f"  NO_IMAGE             : {noimg}")
print(f"\n=== BORROW_CROSS_FAMILY (reachable=Y shown first) ===")
cross=[d for d in out if d["image_kind"]=="BORROW_CROSS_FAMILY"]
for d in sorted(cross,key=lambda x:(x["reachable"]!="Y", x["BaseItemCode"])):
    print(f"  [{d['reachable']}] {d['BaseItemCode']:26} {d['ShortDesc'][:34]:34} <- {d['image_source']}")
print(f"\ncross-family total: {len(cross)} (reachable: {sum(1 for d in cross if d['reachable']=='Y')})")
