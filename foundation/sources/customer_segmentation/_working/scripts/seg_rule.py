import csv, os, sys
from collections import Counter, defaultdict
P=os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv")
rows=list(csv.DictReader(open(P)))
def n(v):
    try: return float(v)
    except: return 0.0
LABEL={"1":"SEG-01","2":"SEG-02","3":"SEG-03","4":"SEG-04"}
def truth(r): return LABEL[r['v4_segment'][0]]

def classify(r):
    aov=n(r['avg_order_value']); oc=n(r['order_count'])
    pc=n(r['price_code_count']); cc=n(r['customer_count'])
    if aov==0 and oc==0: return "SEG-00"          # insufficient data
    if oc>=4000 and aov<2500: return "SEG-04"     # volume distribution
    if oc<1000 and aov<5000:  return "SEG-03"     # mid-market multi-channel
    if aov>=5000:             return "SEG-01"     # luxury specification
    return "SEG-02"                                # premium trade brand

pred=[(r['org'],truth(r),classify(r)) for r in rows]
segs=["SEG-01","SEG-02","SEG-03","SEG-04"]
tot=len(pred); scored=[p for p in pred if p[2]!="SEG-00"]
agree=sum(1 for _,t,c in pred if t==c)
print(f"Roster n={tot}; rule abstains (SEG-00) on {tot-len(scored)}")
print(f"Overall reproduction of stamped label: {agree}/{tot} = {agree/tot:.1%}")
print(f"On scored subset only: {sum(1 for _,t,c in scored if t==c)}/{len(scored)} = {sum(1 for _,t,c in scored if t==c)/len(scored):.1%}")
maj=Counter(t for _,t,_ in pred).most_common(1)[0]
print(f"Majority-class baseline: {maj[0]} {maj[1]}/{tot} = {maj[1]/tot:.1%}\n")
print("Confusion (rows = stamped truth, cols = rule):")
hdr=["SEG-00"]+segs
print(f"{'truth':8}"+"".join(f"{h:>8}" for h in hdr)+f"{'recall':>9}")
for s in segs:
    row=[sum(1 for _,t,c in pred if t==s and c==h) for h in hdr]
    rec=sum(1 for _,t,c in pred if t==s and c==s)/max(1,sum(1 for _,t,_ in pred if t==s))
    print(f"{s:8}"+"".join(f"{v:8d}" for v in row)+f"{rec:9.1%}")
print("\nAbstained (no usable Postgres fields):", " ".join(o for o,_,c in pred if c=="SEG-00"))
