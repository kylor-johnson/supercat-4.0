#!/usr/bin/env python3
"""Rank VISIBLE parent heroes by how likely their Related-Items strip looks off on the iPad,
so a human can eyeball the highest-risk strips first."""
import csv, re, os
from collections import OrderedDict
REV=os.path.dirname(os.path.abspath(__file__))
WORK="/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/products.csv"
DATE="2026-07-24"
def n(s): return (s or "").strip()
def fi(s): s=n(s); return s.split(",")[0].strip() if s else ""
def basen(img): return re.sub(r"\.(jpg|jpeg|png|gif|webp)$","",img,flags=re.I).upper().replace("/","-")
def rel(s): s=n(s); return [x.strip() for x in s.split(",") if x.strip()] if s else []
def fam(sku):
    p=sku.upper().replace("/","-").split("-"); return "-".join(p[:2]) if len(p)>1 else p[0]

rows=list(csv.DictReader(open(WORK,encoding="utf-8-sig")))
by={n(r["BaseItemCode"]):r for r in rows}
def norm(x): return x.upper().replace("/","-")
# owner of an image basename (name-match)
owner={}
for r in rows:
    sku=n(r["BaseItemCode"])
    if basen(fi(r["ImageFileName"]))==norm(sku): owner[norm(sku)]=sku

visible=[r for r in rows if n(r["Hideable"]).upper()!="Y"]
# the confirmed fixed families (heroes) — their own strip is trustworthy after fixes
FIXED_HEROES={"LTSPRO-9-WH","LTSPRO-SW-09-WH","DL-FR-5CCT-4-WH","RGL-FR-5CCT-4-WH","LEDLB-5CCT-10",
              "GDL-4-14W-38-CCT-WH","MLDR-120-24","DD-2460-S-WH","DD-24100-S-WH","ACC-TM-BLK","NFLX-RGB-CHANNEL",
              "LV-SPIR-1CH-LV","LV-DL-EX-10-L","LV-DL-EX-30-L"}

out=[]
for r in visible:
    sku=n(r["BaseItemCode"]); kids=rel(r["RelatedItems"])
    if not kids: continue
    blanks=[]; crossprod=[]; ownnamed=[]
    for k in kids:
        kr=by.get(k)
        if not kr: continue
        kimg=fi(kr["ImageFileName"]); kb=basen(kimg)
        if not kimg:
            blanks.append(k)
        elif kb==norm(k):
            ownnamed.append(k)
        else:
            src=owner.get(kb,"?")
            # child borrows an image owned by a product of a DIFFERENT family stem
            if src=="?" or fam(src)!=fam(k):
                # but same-family borrow (size/finish sibling) is fine; only count if the
                # borrowed source is a truly different product line (different first token)
                if src=="?" or src.split("-")[0]!=k.split("-")[0]:
                    crossprod.append(f"{k}->{kb}")
    score=len(blanks)*3 + len(crossprod)*2 + (0 if sku in FIXED_HEROES else 0)
    if score==0: 
        continue
    out.append(OrderedDict(parent_hero=sku, ShortDesc=n(r["ShortDesc"]),
        n_related=len(kids), blanks=";".join(blanks), n_blank=len(blanks),
        cross_product_thumbs=";".join(crossprod), n_cross=len(crossprod), risk=score))

out.sort(key=lambda d:(-d["risk"], d["parent_hero"]))
with open(os.path.join(REV,f"IPAD_SPOTCHECK_PRIORITY_{DATE}.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)

print(f"Parent heroes whose related strip has a blank or a different-product thumbnail: {len(out)}\n")
print(f"{'#':>2}  {'PARENT HERO':22} {'blk':>3} {'xpr':>3}  detail")
for i,d in enumerate(out,1):
    detail = (f"BLANK: {d['blanks']}" if d['blanks'] else "") + \
             ((" | " if d['blanks'] and d['cross_product_thumbs'] else "") + (f"XPROD: {d['cross_product_thumbs']}" if d['cross_product_thumbs'] else ""))
    print(f"{i:>2}  {d['parent_hero']:22} {d['n_blank']:>3} {d['n_cross']:>3}  {detail}")
