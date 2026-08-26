import csv
from collections import Counter
rows=[r for r in csv.DictReader(open('features.csv')) if r['collect']=='auto']
SEG={"1. Luxury Specification":"SEG-01","2. Premium Trade Brand":"SEG-02",
     "3. Mid-Market Multi-Channel":"SEG-03","4. Volume Distribution":"SEG-04"}
def arch(r):
    b=lambda k: r[k]=='1'
    if b('TRADE_GATE') and not b('RETAIL_ECOM'):                 return "ARCH-01"
    if b('RETAIL_ECOM') or b('PRICE_VISIBLE'):                   return "ARCH-03"
    if b('WHERE_TO_BUY') or b('REP_NETWORK') or b('DEALER_PORTAL'): return "ARCH-02"
    return "ARCH-04"
NAME={"ARCH-01":"Trade-Gated Access","ARCH-02":"Dealer-Locator Network",
      "ARCH-03":"Open-Price Retail Presence","ARCH-04":"No Public Channel Signal"}
APRIORI={"ARCH-01":"SEG-01","ARCH-02":"SEG-02","ARCH-03":"SEG-03","ARCH-04":"SEG-04"}
for r in rows: r['arch']=arch(r); r['seg']=SEG[r['v4']]
n=len(rows)
maj=Counter(r['seg'] for r in rows).most_common(1)[0]
print(f"Back-test set: n={n} orgs with automated observation")
print(f"Majority-class baseline on this set: {maj[0]} = {maj[1]}/{n} = {maj[1]/n:.1%}")
print(f"Established prior baseline for comparison: 30.0%\n")
print(f"{'ARCH':8} {'name':28} {'n':>4} {'a-priori':>9} {'prec':>7}   {'modal seg':>9} {'prec':>7}  verdict")
tot_ap=0; tot_modal=0
for a in ["ARCH-01","ARCH-02","ARCH-03","ARCH-04"]:
    g=[r for r in rows if r['arch']==a]
    if not g: continue
    ap=APRIORI[a]; hit=sum(1 for r in g if r['seg']==ap); p=hit/len(g)
    md,mdn=Counter(r['seg'] for r in g).most_common(1)[0]; pm=mdn/len(g)
    tot_ap+=hit; tot_modal+=mdn
    v = "BEATS baseline" if p>maj[1]/n else "FAILS baseline"
    print(f"{a:8} {NAME[a]:28} {len(g):4d} {ap:>9} {p:7.1%}   {md:>9} {pm:7.1%}  {v}")
print(f"\nOverall, a-priori mapping : {tot_ap}/{n} = {tot_ap/n:.1%}  vs majority {maj[1]/n:.1%}")
print(f"Overall, modal mapping (fit ON answer key, optimistic ceiling): {tot_modal}/{n} = {tot_modal/n:.1%}")
print("\nArchetype x Segment matrix (rows=archetype, cols=stamped segment):")
cols=["SEG-01","SEG-02","SEG-03","SEG-04"]
print(f"{'':10}"+"".join(f"{c:>8}" for c in cols)+f"{'total':>8}")
for a in ["ARCH-01","ARCH-02","ARCH-03","ARCH-04"]:
    g=[r for r in rows if r['arch']==a]
    print(f"{a:10}"+"".join(f"{sum(1 for r in g if r['seg']==c):8d}" for c in cols)+f"{len(g):8d}")
print(f"{'total':10}"+"".join(f"{sum(1 for r in rows if r['seg']==c):8d}" for c in cols)+f"{n:8d}")
csv.DictWriter(open('backtest_rows.csv','w',newline=''),fieldnames=list(rows[0])).writerows([dict(zip(rows[0],rows[0]))]+rows) if False else None
w=csv.DictWriter(open('backtest_rows.csv','w',newline=''),fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
