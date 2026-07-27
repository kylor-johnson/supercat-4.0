#!/usr/bin/env python3
"""Generate reviewable proposal CSVs for Magic Lite (mali) merchandising fix.
Outputs:
  PROPOSAL_01_DUP_IMAGE_TRIAGE.csv   (57 products in 19 shared-hero clusters)
  PROPOSAL_02_ORPHAN_FIX.csv         (163 orphaned-hidden)
  PROPOSAL_03_RELATEITEMS_PREVIEW.csv (per-parent RelatedItems after adds + length check)
Nothing is written to products.csv here."""
import csv, re
from collections import defaultdict, OrderedDict

WORK = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/products.csv"
OUT  = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/00_Import_Files/_MALI_FIX_REVIEW/"

def load(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))
def n(s): return (s or "").strip()
def fi(s): s=n(s); return s.split(",")[0].strip() if s else ""
def rel(s): s=n(s); return [x.strip() for x in s.split(",") if x.strip()] if s else []

rows = load(WORK)
by = {n(r["BaseItemCode"]): r for r in rows}
SKUS = set(by)
visible=[r for r in rows if n(r["Hideable"]).upper()!="Y"]
hidden =[r for r in rows if n(r["Hideable"]).upper()=="Y"]
referenced=set()
for r in rows:
    for x in rel(r["RelatedItems"]): referenced.add(x)
orphans=[r for r in hidden if n(r["BaseItemCode"]) not in referenced]
orphan_set={n(r["BaseItemCode"]) for r in orphans}

vis_by_img=defaultdict(list)
for r in visible:
    im=fi(r["ImageFileName"]).lower()
    if im: vis_by_img[im].append(n(r["BaseItemCode"]))

# ---- track proposed RelatedItems additions/removals per parent ----
add_to_parent=defaultdict(list)   # parent -> [child,...]
del_from_parent=defaultdict(list) # parent -> [child,...] (remove redundant refs)
def relate(child, parent):
    if parent and parent in SKUS and child not in add_to_parent[parent] and child not in rel(by[parent]["RelatedItems"]):
        add_to_parent[parent].append(child)
# Strip redundant cross-size trim refs off the 6" surface-mount heroes (each size hero now visible carries its own trims)
for base in ["LVLDL-SR","LVLDL-SS"]:
    for sz in ["08","10","12"]:
        for fin in ["BK","BZ","BN"]:
            del_from_parent[f"{base}-06-WW-WH-L"].append(f"{base}-{sz}-TR-{fin}-L")

# ================= DELIVERABLE 1: DUP-IMAGE TRIAGE =================
clusters = [
 ("LTSPRO-9-WH.jpg", ["LTSPRO-9-WH","LTSPRO-12-WH","LTSPRO-18-WH","LTSPRO-24-WH","LTSPRO-32-WH","LTSPRO-40-WH"]),
 ("LTSPRO-SW-09-WH.jpg", ["LTSPRO-SW-09-WH","LTSPRO-SW-12-WH","LTSPRO-SW-18-WH","LTSPRO-SW-24-WH","LTSPRO-SW-32-WH","LTSPRO-SW-40-WH"]),
 ("LTS-II-1-HW-WH.jpg", ["LTS-II-1-HW/WH","LTS-II-2-HW/WH","LTS-II-3-HW/WH","LTS-II-4-HW/WH","LTS-II-5-HW/WH"]),
 ("DL-5CCT-4-WH.jpg", ["DL-5CCT-3-WH","DL-5CCT-4-WH","DL-5CCT-6-WH","DL-5CCT-8-WH","DL-5CCT-10-WH"]),
 ("LV-LB-V3-FR.jpg", ["LV-LB-V3-FR","LV-V1V3-EC","LV-V1V3-EC-WF","LV-V1V3-MC"]),
 ("FL-15-CT.jpg", ["FL-15-CT","FL-30-CT","FL-50-CT"]),
 ("LV-ALP2908.jpg", ["LV-ALP2908","LV-ALP2908-EC","LV-ALP2908-EC-WF"]),
 ("SX-12V-DD-60W.jpg", ["SX-12V-DD-60W","SX-TP-BR","SX-TP-LA"]),
 ("LESHP-40-3000K.jpg", ["LESHP-40-3000K","LTP-001-OD-6FT"]),
 ("NFLX-40-3000K.jpg", ["NFLX-40-3000K","NFLX-RGB-CHANNEL"]),
 ("ES-EXT.jpg", ["ES-EXT","ES-EXT-XX"]),
 ("DL-5CCT-4S-WH.jpg", ["DL-5CCT-4S-WH","DL-5CCT-6S-WH"]),
 ("DL-FR-5CCT-4-WH.jpg", ["DL-FR-5CCT-4-WH","DL-FR-5CCT-6-WH"]),
 ("RGL-FR-5CCT-4-WH.jpg", ["RGL-FR-5CCT-4-WH","RGL-FR-5CCT-6-WH"]),
 ("LV-ALP2208.jpg", ["LV-ALP2208","LV-ALP2208-BK"]),
 ("LV-ALP007.jpg", ["LV-ALP007","LV-ALP007-BK"]),
 ("EPL-SR-WW-WH.jpg", ["EPL-SR-WW-WH","EPL-SS-WW-WH"]),
 ("IG-01-12V-36D-BLK.jpg", ["IG-01-12V-36D-BLK","IG-01-12V-60D-BLK"]),
 ("RGL-4B-9W-SW.jpg", ["RGL-4B-9W-SW","RGL-6B-12W-SW"]),
]

# Per-SKU decisions for the 57. action in {KEEP, HIDE_RELATE, HIDE_RELATE_FIXIMG, KEEP_CROSSRELATE}
dup_dec = {}
def D(sku, action, parent, imgchange, reason, cat, flag=""):
    dup_dec[sku]=dict(action=action,parent=parent,imgchange=imgchange,reason=reason,cat=cat,flag=flag)

# KEEP families (distinct size/wattage share stock photo) -> category (a)
for sku in ["LTSPRO-9-WH","LTSPRO-12-WH","LTSPRO-18-WH","LTSPRO-24-WH","LTSPRO-32-WH","LTSPRO-40-WH"]:
    D(sku,"KEEP","", "", "Distinct SIZE/WATTAGE (9-40in, 3-20W); legit family sharing one stock photo","a-keep")
for sku in ["LTSPRO-SW-09-WH","LTSPRO-SW-12-WH","LTSPRO-SW-18-WH","LTSPRO-SW-24-WH","LTSPRO-SW-32-WH","LTSPRO-SW-40-WH"]:
    D(sku,"KEEP","","", "Distinct SIZE/WATTAGE swivel family; legit shared stock photo","a-keep")
for sku in ["LTS-II-1-HW/WH","LTS-II-2-HW/WH","LTS-II-3-HW/WH","LTS-II-4-HW/WH","LTS-II-5-HW/WH"]:
    D(sku,"KEEP","","", "Distinct SIZE/WATTAGE (9.5-43in, 5-25W); legit shared stock photo","a-keep")
for sku in ["DL-5CCT-3-WH","DL-5CCT-4-WH","DL-5CCT-6-WH","DL-5CCT-8-WH","DL-5CCT-10-WH"]:
    D(sku,"KEEP","","", "Distinct SIZE (3-10in); legit shared stock photo","a-keep")
for sku in ["FL-15-CT","FL-30-CT","FL-50-CT"]:
    D(sku,"KEEP","","", "Distinct WATTAGE (15/30/50W); legit shared stock photo","a-keep")
for sku in ["DL-5CCT-4S-WH","DL-5CCT-6S-WH"]:
    D(sku,"KEEP","","", "Distinct SIZE square downlight (4/6in)","a-keep")
for sku in ["DL-FR-5CCT-4-WH","DL-FR-5CCT-6-WH"]:
    D(sku,"KEEP","","", "Distinct SIZE fire-rated (4/6in)","a-keep")
for sku in ["RGL-FR-5CCT-4-WH","RGL-FR-5CCT-6-WH"]:
    D(sku,"KEEP","","", "Distinct SIZE fire-rated regressed (4/6in)","a-keep")
for sku in ["RGL-4B-9W-SW","RGL-6B-12W-SW"]:
    D(sku,"KEEP","","", "Distinct SIZE/WATTAGE (4in/9W, 6in/12W)","a-keep")

# Accessories riding a hero image -> HIDE + relate (category b)
D("LV-LB-V3-FR","KEEP","","", "Extrusion hero (verified magiclite LV-LB-V3-FR page)","a-keep")
for sku in ["LV-V1V3-EC","LV-V1V3-EC-WF","LV-V1V3-MC"]:
    D(sku,"HIDE_RELATE","LV-LB-V3-FR","", "Accessory (end caps/mounting clips) riding hero photo; verified as accessory on magiclite","b-hide")
D("LV-ALP2908","KEEP","","", "Extrusion hero","a-keep")
for sku in ["LV-ALP2908-EC","LV-ALP2908-EC-WF"]:
    D(sku,"HIDE_RELATE","LV-ALP2908","", "Accessory (end caps) riding hero photo","b-hide")
D("SX-12V-DD-60W","KEEP","","", "Switchex hero (verified magiclite switchex page)","a-keep")
for sku in ["SX-TP-BR","SX-TP-LA"]:
    D(sku,"HIDE_RELATE","SX-12V-DD-60W","", "Trim-plate accessory riding hero photo","b-hide")
# Finish variants (black extrusion) -> HIDE + relate
D("LV-ALP2208","KEEP","","", "Extrusion hero (natural aluminum)","a-keep")
D("LV-ALP2208-BK","HIDE_RELATE","LV-ALP2208","", "Black FINISH variant of same extrusion","b-hide","FINISH-CALL: owner may prefer to keep black visible")
D("LV-ALP007","KEEP","","", "Extrusion hero (natural aluminum)","a-keep")
D("LV-ALP007-BK","HIDE_RELATE","LV-ALP007","", "Black FINISH variant of same extrusion","b-hide","FINISH-CALL: owner may prefer to keep black visible")

# Wrong-image accessories -> HIDE + relate + CLEAR wrong image (category c)
D("LESHP-40-3000K","KEEP","","", "High Power eStrip hero; image correct (verified magiclite estrip page)","a-keep")
D("LTP-001-OD-6FT","HIDE_RELATE_FIXIMG","LES-40-RGB","CLEAR",
  "Power-feed connector accessory wrongly showing eStrip photo; belongs to RGB eStrip (already in LES-40-RGB related)","c-fiximg")
D("NFLX-40-3000K","KEEP","","", "Neon Flex hero; image correct","a-keep")
# NFLX heroes' RelatedItems are all already 244-253 chars (no room). Keep channel VISIBLE with a correct image
# instead of hiding it (verified real aluminum-channel photo downloaded from magiclite + staged as NFLX-RGB-CHANNEL.jpg).
D("NFLX-RGB-CHANNEL","KEEP_FIXIMG","","NFLX-RGB-CHANNEL.jpg",
  "Aluminum mounting-channel wrongly showing neon-flex photo; real channel photo staged. Kept visible (NFLX heroes' RelatedItems already full at 244-253 chars)","c-fiximg",
  "Confirm RGB channel identical to single-colour NFLX-CHANNEL photo; else request client photo")

# Borderline -> KEEP both, cross-relate, flag
D("ES-EXT","KEEP_CROSSRELATE","ES-EXT-XX","", "8ft extrusion; keep. Cross-relate to shorter-length variant","flag-keep","LENGTH variant pair")
D("ES-EXT-XX","KEEP_CROSSRELATE","ES-EXT","", "Shorter-length extrusion; keep visible (distinct length/price)","flag-keep","LENGTH variant pair")
D("EPL-SR-WW-WH","KEEP","","", "Round puck hero (distinct SHAPE)","a-keep")
D("EPL-SS-WW-WH","KEEP","","", "Square puck hero (distinct SHAPE)","a-keep")
D("IG-01-12V-36D-BLK","KEEP_CROSSRELATE","IG-01-12V-60D-BLK","", "Well light 36deg; keep. Beam angle is a real selection","flag-keep","BEAM-ANGLE: keep both, cross-relate")
D("IG-01-12V-60D-BLK","KEEP_CROSSRELATE","IG-01-12V-36D-BLK","", "Well light 60deg; keep. Beam angle is a real selection","flag-keep","BEAM-ANGLE: keep both, cross-relate")

# emit dup triage csv
with open(OUT+"PROPOSAL_01_DUP_IMAGE_TRIAGE.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["cluster_hero_img","BaseItemCode","ShortDesc","cur_Hideable","cur_first_image",
                "PROPOSED_action","PROPOSED_Hideable","relate_to","image_change","reason","category","flag"])
    for himg,cl in clusters:
        for sku in cl:
            r=by.get(sku)
            d=dup_dec.get(sku, dict(action="REVIEW",parent="",imgchange="",reason="",cat="",flag="UNMAPPED"))
            new_hide = "Y" if d["action"].startswith("HIDE") else n(r["Hideable"])
            if d["action"] in ("HIDE_RELATE","HIDE_RELATE_FIXIMG"):
                relate(sku, d["parent"])
            if d["action"]=="KEEP_CROSSRELATE":
                relate(sku, d["parent"])
            w.writerow([himg,sku,n(r["ShortDesc"]),n(r["Hideable"]),fi(r["ImageFileName"]),
                        d["action"],new_hide,d["parent"],d["imgchange"],d["reason"],d["cat"],d["flag"]])

# ================= DELIVERABLE 2: ORPHAN FIX =================
# parent resolver for shared-image orphans
def resolve_parent(sku, img):
    cand=vis_by_img.get(img,[])
    if not cand: return ""
    if len(cand)==1: return cand[0]
    # multi-parent: longest common prefix
    best=""; bl=-1
    for c in cand:
        k=0
        for a,b in zip(sku,c):
            if a==b: k+=1
            else: break
        if k>bl: bl=k; best=c
    return best

# explicit UNHIDE sets (distinct sizes with a size-hero gap)
UNHIDE_SIZE = set()
RELATE_CCT = {}     # child -> parent (CCT/finish variant to relate)
FLAG_CLIENT = {}    # child -> note

# LEDLB task bar: only 10in visible; 12/18/24/36/48 distinct sizes -> UNHIDE
for s in ["LEDLB-5CCT-12","LEDLB-5CCT-18","LEDLB-5CCT-24","LEDLB-5CCT-36","LEDLB-5CCT-48"]:
    UNHIDE_SIZE.add(s)
# GDL gimbal: 4in visible; 3/6 distinct -> UNHIDE
for s in ["GDL-3-8W-38-CCT-WH","GDL-6-18W-38-CCT-WH"]:
    UNHIDE_SIZE.add(s)
# LV-HS-PD20 hard strip: 30-WW visible. sizes 50/100/120 -> unhide WW hero; relate NW + 30-NW
for s in ["LV-HS-PD20-24V-50-WW","LV-HS-PD20-24V-100-WW","LV-HS-PD20-24V-120-WW"]:
    UNHIDE_SIZE.add(s)
RELATE_CCT["LV-HS-PD20-24V-30-NW"]="LV-HS-PD20-24V-30-WW"
RELATE_CCT["LV-HS-PD20-24V-50-NW"]="LV-HS-PD20-24V-50-WW"
RELATE_CCT["LV-HS-PD20-24V-100-NW"]="LV-HS-PD20-24V-100-WW"
RELATE_CCT["LV-HS-PD20-24V-120-NW"]="LV-HS-PD20-24V-120-WW"
# LV-HS-RGB hard strip: 300mm visible; 500/1000 distinct -> UNHIDE
for s in ["LV-HS-RGB-24T2-2","LV-HS-RGB-24T2-3"]:
    UNHIDE_SIZE.add(s)
# LVLDL-SR/SS surface mount: 06-WW visible. unhide 08/10/12 WW; relate NW + 06-NW
for base in ["LVLDL-SR","LVLDL-SS"]:
    for sz in ["08","10","12"]:
        UNHIDE_SIZE.add(f"{base}-{sz}-WW-WH-L")
    RELATE_CCT[f"{base}-06-NW-WH-L"]=f"{base}-06-WW-WH-L"
    for sz in ["08","10","12"]:
        RELATE_CCT[f"{base}-{sz}-NW-WH-L"]=f"{base}-{sz}-WW-WH-L"
# SDL packs: 4-WH-1P visible. 6-WH-1P distinct size -> UNHIDE (flag needs 6in image). packs -> relate
UNHIDE_SIZE.add("SDL-5CCT-6-WH-1P")
for s in ["SDL-5CCT-4-WH-6P","SDL-5CCT-4-WH-12P","SDL-5CCT-4-WH-24P"]:
    RELATE_CCT[s]="SDL-5CCT-4-WH-1P"
for s in ["SDL-5CCT-6-WH-6P","SDL-5CCT-6-WH-12P"]:
    RELATE_CCT[s]="SDL-5CCT-6-WH-1P"
# LT-WIFI-RM accessory remote -> relate to a controller hero (flag which)
RELATE_CCT["LT-WIFI-RM"]="ACC-WIFI"
FLAG_CLIENT["LT-WIFI-RM"]="Verify parent controller for WiFi remote (default ACC-WIFI)"
# ST-ID Standard Tape: 2700K low-power is CCT variant of visible 3000K low-power
RELATE_CCT["ST-ID-27K-LP-20-B0"]="ST-ID-30K-LP-20-B0"
# Switch Star: DISCONTINUED + too many cover/finish variants for one RelatedItems (255 cap) -> flag, do not force-relate
DISCONTINUED_FLAG = {}
for r in orphans:
    s=n(r["BaseItemCode"])
    if s.startswith("LED-SW-"):
        DISCONTINUED_FLAG[s]="Switch Star DISCONTINUED + too many variants for RelatedItems(255); client: drop or keep hidden"
# Disc Light + Mini Disc Marker COLOR families -> FLAG for client (default: relate to visible cool-white hero, keep hidden)
COLOR_FLAG_PARENT = {}
def flag_color(prefix_list, parent, note):
    for r in orphans:
        s=n(r["BaseItemCode"]); img=fi(r["ImageFileName"]).lower()
        if any(s.startswith(p) for p in prefix_list) and s not in UNHIDE_SIZE and s not in RELATE_CCT \
           and img not in vis_by_img:  # items sharing a visible hero image go to Group A relate, not color-flag
            COLOR_FLAG_PARENT[s]=parent; FLAG_CLIENT[s]=note
flag_color(["LEDD-C","LEDD-F"],"LEDD-F-WH","Disc Light color/shape family - client: choose visible heroes per shape/color")
flag_color(["LEDMD-S-"],"LEDMD-S-WH-AL","Mini Disc Scoop color family - client decision (non cool-white)")
flag_color(["LEDMD-"],"LEDMD-WH-AL","Mini Disc Marker color family - client decision (non cool-white)")

# Build orphan rows
orphan_rows=[]
for r in orphans:
    sku=n(r["BaseItemCode"]); img=fi(r["ImageFileName"]).lower()
    shares = img in vis_by_img
    if sku in DISCONTINUED_FLAG:
        orphan_rows.append([sku,n(r["ShortDesc"]),"Y",fi(r["ImageFileName"]),
            "FLAG_CLIENT (leave hidden)","Y","","", "Discontinued line; too many variants for RelatedItems cap","B-flag",
            DISCONTINUED_FLAG[sku]])
    elif sku in UNHIDE_SIZE:
        orphan_rows.append([sku,n(r["ShortDesc"]),"Y",fi(r["ImageFileName"]),
            "UNHIDE","N","","", "Distinct SIZE with no visible size-hero; promote to visible","B-unhide",""])
    elif sku in RELATE_CCT:
        p=RELATE_CCT[sku]; relate(sku,p)
        orphan_rows.append([sku,n(r["ShortDesc"]),"Y",fi(r["ImageFileName"]),
            "RELATE_TO_VISIBLE","Y",p,"", "CCT/pack/accessory variant; relate to same-size hero","B-relate",
            FLAG_CLIENT.get(sku,"")])
    elif sku in COLOR_FLAG_PARENT:
        p=COLOR_FLAG_PARENT[sku]
        orphan_rows.append([sku,n(r["ShortDesc"]),"Y",fi(r["ImageFileName"]),
            "FLAG_CLIENT (default: relate hidden)","Y",p,"", "Color family needs client decision; default relate to cool-white hero","B-flag",
            FLAG_CLIENT.get(sku,"")])
    elif shares:
        parent=resolve_parent(sku,img)
        relate(sku,parent)
        orphan_rows.append([sku,n(r["ShortDesc"]),"Y",fi(r["ImageFileName"]),
            "RELATE_TO_VISIBLE","Y",parent,"", "Shares hero image with visible parent; add to parent RelatedItems so rep can reach it","A-relate",""])
    else:
        orphan_rows.append([sku,n(r["ShortDesc"]),"Y",fi(r["ImageFileName"]),
            "REVIEW","Y","","", "Unmapped orphan - needs manual review","B-review","UNMAPPED"])

with open(OUT+"PROPOSAL_02_ORPHAN_FIX.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["BaseItemCode","ShortDesc","cur_Hideable","cur_first_image",
                "PROPOSED_action","PROPOSED_Hideable","relate_to","image_change","reason","category","flag"])
    for row in orphan_rows: w.writerow(row)

# ================= DELIVERABLE 3: RelatedItems length preview =================
overflow=[]
with open(OUT+"PROPOSAL_03_RELATEITEMS_PREVIEW.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["parent","cur_len","added_count","removed_count","new_len","OVER_255","new_RelatedItems"])
    parents=sorted(set(add_to_parent)|set(del_from_parent))
    for parent in parents:
        children=add_to_parent.get(parent,[])
        removed=del_from_parent.get(parent,[])
        cur=rel(by[parent]["RelatedItems"])
        kept=[c for c in cur if c not in removed]
        new=kept+[c for c in children if c not in kept]
        s=",".join(new)
        over = "YES" if len(s)>255 else ""
        if over: overflow.append(parent)
        w.writerow([parent,len(",".join(cur)),len(children),len(removed),len(s),over,s])

# ================= SUMMARY =================
from collections import Counter
dcat=Counter(d["action"] for d in dup_dec.values())
ocat=Counter(row[5-1] if False else row[9] for row in orphan_rows)  # category col index 9
print("DUP-IMAGE TRIAGE (57):")
for k,v in dcat.items(): print(f"   {k}: {v}")
print("\nORPHAN FIX (163) by category:")
ocount=Counter(row[9] for row in orphan_rows)
for k,v in sorted(ocount.items()): print(f"   {k}: {v}")
print(f"\nTotal RelatedItems parents receiving adds: {len(add_to_parent)}")
print(f"RelatedItems OVER 255 after adds: {len(overflow)} -> {overflow}")
unmapped=[row[0] for row in orphan_rows if row[10]=='UNMAPPED']
print(f"UNMAPPED orphans: {len(unmapped)} {unmapped}")
