#!/usr/bin/env python3
"""Generate the catalogue hero-audit deliverables for Magic Lite (mali)."""
import csv, re, os
from collections import OrderedDict
REV=os.path.dirname(os.path.abspath(__file__))
WORK="/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/products.csv"
CATTXT=os.path.join(REV,"catalogue","_alltext.txt")
DATE="2026-07-24"
def n(s): return (s or "").strip()
def fi(s): s=n(s); return s.split(",")[0].strip() if s else ""

rows=list(csv.DictReader(open(WORK,encoding="utf-8-sig")))
visible=[r for r in rows if n(r["Hideable"]).upper()!="Y"]

# page text
pages={}; cur=None; buf=[]
for line in open(CATTXT):
    m=re.match(r"===== IDX (\d+) =====",line)
    if m:
        if cur is not None: pages[cur]="\n".join(buf).upper()
        cur=int(m.group(1)); buf=[]
    else: buf.append(line.rstrip("\n"))
if cur is not None: pages[cur]="\n".join(buf).upper()

def cat_hits(sku):
    su=sku.upper(); h=[i for i,t in pages.items() if su in t]
    if h: return h
    parts=su.split("-")
    for k in range(len(parts)-1,1,-1):
        pref="-".join(parts[:k])
        if len(pref)<3: break
        hh=[i for i,t in pages.items() if pref in t]
        if hh: return hh
    if parts and len(parts[0])>=3:
        hh=[i for i,t in pages.items() if parts[0] in t]
        if hh: return hh
    return []
def printed_pp(idx): return f"{2*idx-3}-{2*idx-2}"

# ---- decisions ----
FIX_FILESWAP={  # sku -> (staged_file, source, correct_desc)
 "LTSPRO-9-WH":("LTSPRO-9-WH.jpg","catalogue p.51","clean white task bar (shared by all LTSPRO-*-WH)"),
 "LTSPRO-SW-09-WH":("LTSPRO-SW-09-WH.jpg","catalogue p.53","clean white swivel bar (shared by all LTSPRO-SW-*)"),
 "DL-FR-5CCT-4-WH":("DL-FR-5CCT-4-WH.jpg","catalogue p.129","red fire-rated downlight (shared by DL-FR-5CCT-4/6)"),
 "RGL-FR-5CCT-4-WH":("RGL-FR-5CCT-4-WH.jpg","catalogue p.131","red regressed downlight (shared by RGL-FR-5CCT-4/6)"),
 "LV-SPIR-1CH-LV":("LV-SPIR-1CH-LV.jpg","catalogue p.167","black PIR motion sensor"),
 "LV-DL-EX-10-L":("LV-DL-EX-10-L.jpg","magiclite.com scrape","interconnection cable 10ft"),
 "LV-DL-EX-30-L":("LV-DL-EX-30-L.jpg","magiclite.com scrape","interconnection cable 30ft"),
 "MLDR-120-24":("MLDR-120-24.jpg","magiclite.com scrape (staged prior)","indoor/outdoor driver photo"),
 "DD-2460-S-WH":("DD-2460-S-WH.jpg","magiclite.com scrape (staged prior)","DimDrive 60W device face"),
 "DD-24100-S-WH":("DD-24100-S-WH.jpg","magiclite.com scrape (staged prior)","DimDrive 100W device face"),
 "ACC-TM-BLK":("ACC-TM-BLK.jpg","magiclite.com scrape (staged prior)","landscape tree mount"),
 "NFLX-RGB-CHANNEL":("NFLX-RGB-CHANNEL.jpg","magiclite.com scrape (staged prior)","RGB aluminum channel"),
}
# products that share a fixed primary file (fixed automatically by the file-swap)
FIXED_VIA_SHARED={
 "LTSPRO-12-WH":"LTSPRO-9-WH.jpg","LTSPRO-18-WH":"LTSPRO-9-WH.jpg","LTSPRO-24-WH":"LTSPRO-9-WH.jpg",
 "LTSPRO-32-WH":"LTSPRO-9-WH.jpg","LTSPRO-40-WH":"LTSPRO-9-WH.jpg",
 "LTSPRO-SW-12-WH":"LTSPRO-SW-09-WH.jpg","LTSPRO-SW-18-WH":"LTSPRO-SW-09-WH.jpg","LTSPRO-SW-24-WH":"LTSPRO-SW-09-WH.jpg",
 "LTSPRO-SW-32-WH":"LTSPRO-SW-09-WH.jpg","LTSPRO-SW-40-WH":"LTSPRO-SW-09-WH.jpg",
 "DL-FR-5CCT-6-WH":"DL-FR-5CCT-4-WH.jpg","RGL-FR-5CCT-6-WH":"RGL-FR-5CCT-4-WH.jpg",
}
FIX_REPOINT={ # already applied to CSV
 "LEDLB-5CCT-12":"LEDLB-5CCT-10.jpg","LEDLB-5CCT-18":"LEDLB-5CCT-10.jpg","LEDLB-5CCT-24":"LEDLB-5CCT-10.jpg",
 "LEDLB-5CCT-36":"LEDLB-5CCT-10.jpg","LEDLB-5CCT-48":"LEDLB-5CCT-10.jpg",
 "GDL-3-8W-38-CCT-WH":"GDL-4-14W-38-CCT-WH.jpg","GDL-6-18W-38-CCT-WH":"GDL-4-14W-38-CCT-WH.jpg",
}
CLIENT_PHOTO={
 "LV-RF103":"Wireless RF Mini RGB Controller — not in catalogue; individual controller photo needed",
 "LT-11S-RF":"RF Touch Control (RGBW) — not in catalogue; individual remote photo needed",
 "LV-ZJFFS-3CH-6INW":"RGB Signal Amplifier (Outdoor) — not in catalogue; individual amp photo needed",
 "LT-490A":"Signal Amplifier (RGB-W) — not in catalogue; individual amp photo needed",
}
VERIFY={ # own-named; product family exists but SKU string not verbatim in catalogue — cannot see live file
 "DR-96-24-TM-5N1D":"Infini Drive 24V 96W — driver; not in catalogue (own-named). Verify hero on iPad.",
 "ES-LS283527K422430":"24V Wall Washer (2700K) — family confirmed catalogue p.45 (ES-LS2835). Own-named; verify hero on iPad.",
 "ES-LS283530-WH244FT":"Wall Washer 4' Enclosed (3000K) — 24V Wall Washer family (catalogue p.45). Own-named; verify hero on iPad.",
 "YH-HRF50CA120S505060":"120V AC RGB eStrip — YH RGB family (catalogue p.31-32). Own-named; verify hero on iPad.",
}

def family(sku):
    p=sku.split("-"); return "-".join(p[:2]) if len(p)>1 else p[0]

audit=[]
for r in visible:
    sku=n(r["BaseItemCode"]); img=fi(r["ImageFileName"]); sd=n(r["ShortDesc"])
    hits=cat_hits(sku); pp=printed_pp(hits[0]) if hits else ""
    own = re.sub(r"\.jpg$","",img,flags=re.I).upper().replace("/","-")==sku.upper().replace("/","-")
    if sku in FIX_FILESWAP:
        f,src,desc=FIX_FILESWAP[sku]
        verdict="FIXED — file-swap (upload)"; fix="upload clean JPG (same filename)"; corr=f"{src}: {desc}"; act=f"UPLOAD {f}"
    elif sku in FIXED_VIA_SHARED:
        verdict="FIXED — via shared primary"; fix="none (shares fixed hero file)"; corr=f"shares {FIXED_VIA_SHARED[sku]}"; act=f"covered by UPLOAD {FIXED_VIA_SHARED[sku]}"
    elif sku in FIX_REPOINT:
        verdict="FIXED — repoint (CSV applied)"; fix="ImageFileName repoint"; corr=f"reuse {FIX_REPOINT[sku]} (verified-clean sibling)"; act="re-import products.csv"
    elif sku in CLIENT_PHOTO:
        verdict="CLIENT PHOTO NEEDED"; fix="await client photo"; corr="not in catalogue"; act="request photo from client"
    elif sku in VERIFY:
        verdict="VERIFY on iPad"; fix="none pending verify"; corr="not in catalogue text"; act="visually confirm hero on iPad"
    else:
        if own and hits:
            verdict="OK — own-named + catalogue-confirmed"; fix="none"; corr=f"catalogue pp.{pp}"; act="none"
        elif (not own) and hits:
            verdict="OK — shared family hero (distinct size)"; fix="none"; corr=f"catalogue pp.{pp}; shares {img}"; act="none"
        elif own and not hits:
            verdict="OK — own-named (no catalogue text hit)"; fix="none"; corr="own photo (website/client)"; act="none"
        else:
            verdict="REVIEW"; fix="none"; corr=""; act="review"
    audit.append(OrderedDict(BaseItemCode=sku,family=family(sku),ShortDesc=sd,current_hero=img,
        own_named=("Y" if own else "N"),catalogue_pp=pp,verdict=verdict,fix_type=fix,
        correct_image_source=corr,action=act))

audit.sort(key=lambda d:(d["verdict"],d["family"],d["BaseItemCode"]))
with open(os.path.join(REV,f"CATALOGUE_HERO_AUDIT_{DATE}.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(audit[0].keys())); w.writeheader(); w.writerows(audit)

# client photo needed csv (visible controllers = high; hidden blank accessories = low)
HIDDEN_BLANK_NOPHOTO={
 "LV-HSDR-36-24-PC":"36W 24V Hard-Strip driver — blank; not pictured as a product in catalogue",
 "LV-HSDR-60-24-PC":"60W 24V Hard-Strip driver — blank; not pictured as a product in catalogue",
 "LMSH-001":"Terminal Block/Junction Box — blank; not pictured as a product in catalogue",
 "LBR-II-KIT":"Brick Star Replacement Kit — blank; code-only in catalogue p.87 (no photo)",
 "BL-CC":"Brick Star Concrete Cap — blank; catalogue p.87 shows a line-drawing only",
 "SL-CC":"Step Star Concrete Cap — blank; catalogue shows a line-drawing only",
 "LTP-001-OD-6FT":"Outdoor Power Feed Connector — blank; RGB eStrip accessory",
}
allrows={n(r["BaseItemCode"]):r for r in rows}
with open(os.path.join(REV,f"CLIENT_PHOTO_NEEDED_{DATE}.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["BaseItemCode","ShortDesc","current_hero","visible","priority","reason"])
    for sku,reason in CLIENT_PHOTO.items():
        r=allrows[sku]; w.writerow([sku,n(r["ShortDesc"]),fi(r["ImageFileName"]),"Y","HIGH (visible tile)",reason])
    for sku,reason in HIDDEN_BLANK_NOPHOTO.items():
        r=allrows[sku]; w.writerow([sku,n(r["ShortDesc"]),fi(r["ImageFileName"]) or "(blank)","N","LOW (hidden related-thumbnail)",reason])

# FTP upload list
upload=sorted(os.listdir(os.path.join(REV,"catA_images")))
upload=[u for u in upload if u.lower().endswith(".jpg")]
with open(os.path.join(REV,f"FTP_UPLOAD_LIST_{DATE}.txt"),"w") as f:
    f.write("# Magic Lite (mali) — FTP /images upload list  ("+DATE+")\n")
    f.write("# Drop these into FTP /images (FLAT root, no subfolders). Source: _MALI_FIX_REVIEW/catA_images/\n")
    f.write("# All sRGB .jpg, exact ImageFileName casing. After upload, re-import products.csv, then verify File Import Status.\n\n")
    for u in upload: f.write(u+"\n")

# summary
from collections import Counter
c=Counter(d["verdict"] for d in audit)
print("=== VERDICT SUMMARY (218 visible) ===")
for k,v in sorted(c.items(),key=lambda kv:-kv[1]): print(f"  {v:3}  {k}")
print("\nFTP upload files:",len(upload))
print("CLIENT_PHOTO_NEEDED:",len(CLIENT_PHOTO))
print("wrote CATALOGUE_HERO_AUDIT / CLIENT_PHOTO_NEEDED / FTP_UPLOAD_LIST")
