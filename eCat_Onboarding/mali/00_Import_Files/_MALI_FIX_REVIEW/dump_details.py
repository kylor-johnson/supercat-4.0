#!/usr/bin/env python3
import csv
from collections import defaultdict

WORK = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/products.csv"

def load(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def n(s): return (s or "").strip()
def first_img(s):
    s=n(s); return s.split(",")[0].strip() if s else ""

rows = load(WORK)
by = {n(r["BaseItemCode"]): r for r in rows}

# The 19 shared-hero clusters (from verify_state)
clusters = [
 ["LTSPRO-9-WH","LTSPRO-12-WH","LTSPRO-18-WH","LTSPRO-24-WH","LTSPRO-32-WH","LTSPRO-40-WH"],
 ["LTSPRO-SW-09-WH","LTSPRO-SW-12-WH","LTSPRO-SW-18-WH","LTSPRO-SW-24-WH","LTSPRO-SW-32-WH","LTSPRO-SW-40-WH"],
 ["LTS-II-1-HW/WH","LTS-II-2-HW/WH","LTS-II-3-HW/WH","LTS-II-4-HW/WH","LTS-II-5-HW/WH"],
 ["DL-5CCT-3-WH","DL-5CCT-4-WH","DL-5CCT-6-WH","DL-5CCT-8-WH","DL-5CCT-10-WH"],
 ["LV-LB-V3-FR","LV-V1V3-EC","LV-V1V3-EC-WF","LV-V1V3-MC"],
 ["FL-15-CT","FL-30-CT","FL-50-CT"],
 ["LV-ALP2908","LV-ALP2908-EC","LV-ALP2908-EC-WF"],
 ["SX-12V-DD-60W","SX-TP-BR","SX-TP-LA"],
 ["LESHP-40-3000K","LTP-001-OD-6FT"],
 ["NFLX-40-3000K","NFLX-RGB-CHANNEL"],
 ["ES-EXT","ES-EXT-XX"],
 ["DL-5CCT-4S-WH","DL-5CCT-6S-WH"],
 ["DL-FR-5CCT-4-WH","DL-FR-5CCT-6-WH"],
 ["RGL-FR-5CCT-4-WH","RGL-FR-5CCT-6-WH"],
 ["LV-ALP2208","LV-ALP2208-BK"],
 ["LV-ALP007","LV-ALP007-BK"],
 ["EPL-SR-WW-WH","EPL-SS-WW-WH"],
 ["IG-01-12V-36D-BLK","IG-01-12V-60D-BLK"],
 ["RGL-4B-9W-SW","RGL-6B-12W-SW"],
]

for ci, cl in enumerate(clusters,1):
    hero_img = first_img(by[cl[0]].get("ImageFileName","")) if cl[0] in by else "?"
    print(f"\n########## CLUSTER {ci}  hero_img={hero_img} ##########")
    for sku in cl:
        r = by.get(sku)
        if not r:
            print(f"  !!! MISSING {sku}")
            continue
        print(f"  {sku}")
        print(f"     Short : {n(r['ShortDesc'])}")
        print(f"     Long  : {n(r['LongDesc'])}")
        print(f"     Img   : {n(r['ImageFileName'])}")
        print(f"     Hide  : {n(r['Hideable'])}  W:{n(r['PowerConsumption_W'])}  CCT:{n(r['ColorTemperature_K'])}  Dim(mm):{n(r['Dimensions_mm'])}  Dim(in):{n(r['Dimensions_inches'])}")
        print(f"     Price : mllist={n(r['price_mllist'])} nsllist={n(r['price_nsllist'])}")
        print(f"     Rel   : {n(r['RelatedItems'])}")
