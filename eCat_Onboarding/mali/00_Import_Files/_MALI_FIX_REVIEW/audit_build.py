#!/usr/bin/env python3
"""Build the full visible-hero audit scaffold for Magic Lite.
Outputs:
  - _audit_visible.csv : every visible SKU, family stem, current hero file, own/borrowed,
                         catalogue page hits (idx list) from text search.
"""
import csv, re, os
from collections import defaultdict, OrderedDict

REV = os.path.dirname(os.path.abspath(__file__))
WORK = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/products.csv"
CATTXT = os.path.join(REV, "catalogue", "_alltext.txt")

def n(s): return (s or "").strip()
def fi(s): s=n(s); return s.split(",")[0].strip() if s else ""

rows=list(csv.DictReader(open(WORK,encoding="utf-8-sig")))
visible=[r for r in rows if n(r["Hideable"]).upper()!="Y"]

# --- load catalogue page text ---
pages={}  # idx -> text (upper)
cur=None; buf=[]
for line in open(CATTXT):
    m=re.match(r"===== IDX (\d+) =====", line)
    if m:
        if cur is not None: pages[cur]="\n".join(buf)
        cur=int(m.group(1)); buf=[]
    else:
        buf.append(line.rstrip("\n"))
if cur is not None: pages[cur]="\n".join(buf)
pages_up={i:t.upper() for i,t in pages.items()}

def stem(sku):
    # family stem: strip trailing size/finish tokens progressively
    return sku

def search_cat(sku):
    """Return list of page idx where sku or its meaningful prefix appears."""
    su=sku.upper()
    hits=[i for i,t in pages_up.items() if su in t]
    if hits: return hits, "exact"
    # try progressively shorter prefixes on hyphen boundaries
    parts=su.split("-")
    for k in range(len(parts)-1,1,-1):
        pref="-".join(parts[:k])
        if len(pref)<3: break
        h=[i for i,t in pages_up.items() if pref in t]
        if h: return h, f"prefix:{pref}"
    # first token
    if parts and len(parts[0])>=3:
        h=[i for i,t in pages_up.items() if parts[0] in t]
        if h: return h, f"tok0:{parts[0]}"
    return [], "none"

def family(sku):
    # crude family key = first two hyphen tokens
    parts=sku.split("-")
    return "-".join(parts[:2]) if len(parts)>1 else parts[0]

out=[]
for r in visible:
    sku=n(r["BaseItemCode"]); img=fi(r["ImageFileName"]); sd=n(r["ShortDesc"])
    imgbase=re.sub(r"\.(jpg|jpeg|png|gif|webp)$","",img,flags=re.I)
    own = imgbase.upper().replace("/","-")==sku.upper().replace("/","-")
    hits,how=search_cat(sku)
    out.append(OrderedDict(
        BaseItemCode=sku, family=family(sku), ShortDesc=sd,
        current_hero=img, own_named=("Y" if own else "N"),
        cat_pages_idx=";".join(str(h) for h in hits[:8]), match_how=how,
    ))

out.sort(key=lambda d:(d["family"], d["BaseItemCode"]))
with open(os.path.join(REV,"_audit_visible.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print("visible:",len(out))
# family summary
fam=defaultdict(list)
for d in out: fam[d["family"]].append(d)
print("families:",len(fam))
nohit=[d["BaseItemCode"] for d in out if d["match_how"]=="none"]
print("no catalogue text hit:",len(nohit))
print(", ".join(nohit))
