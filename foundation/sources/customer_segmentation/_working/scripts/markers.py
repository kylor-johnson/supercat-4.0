import re,os,csv,glob,json
orgs=list(csv.DictReader(open('orgs.csv')))
usable=set(open('usable.txt').read().split())
def text_of(sn):
    parts=[]
    for p in [f"pages/{sn}__home.html"]+sorted(glob.glob(f"pages/{sn}__sub*.html")):
        if not os.path.exists(p): continue
        h=open(p,encoding='utf-8',errors='ignore').read()
        h=re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->','',h,flags=re.S|re.I)
        h=re.sub(r'<[^>]+>',' ',h)
        h=re.sub(r'&nbsp;?|&amp;',' ',h)
        parts.append(h)
    t=re.sub(r'\s+',' ',' '.join(parts)).lower()
    return t
def links_of(sn):
    s=[]
    for p in [f"pages/{sn}__home.html"]:
        if os.path.exists(p):
            s.append(open(p,encoding='utf-8',errors='ignore').read().lower())
    for row in csv.DictReader(open('subpages.csv')):
        if row['org']==sn: s.append((row['url']+' '+row['anchor']).lower())
    return ' '.join(s)

M={
 "TRADE_GATE":      r"to the trade|trade only|trade program|trade account|trade portal|trade login|designer program|designer trade|trade professional",
 "DEALER_PORTAL":   r"dealer login|dealer portal|dealer resources|retailer login|wholesale login|b2b portal|authorized dealer|dealer center|become a dealer",
 "RETAIL_ECOM":     r"add to cart|add to bag|add to basket|proceed to checkout|shopping cart",
 "PRICE_VISIBLE":   r"\$\s?\d[\d,]*\.\d{2}",
 "WHERE_TO_BUY":    r"where to buy|find a dealer|find a retailer|store locator|dealer locator|showroom locator|find a store|find a showroom",
 "REP_NETWORK":     r"sales rep|find a rep|rep locator|sales representative|territory manager|rep territory|our reps|representative directory",
 "REP_RECRUIT":     r"become a rep|rep opportunit|seeking representation|sales rep position|rep inquiries|join our sales",
 "CONTRACT_SPEC":   r"hospitality|contract grade|contract division|contract market|specification|spec sheet|a&d |architects and designers|architect & design",
 "COM_PROGRAM":     r"customer'?s own material|customer own material|com program|com/col|\bcom & col\b",
 "MAP_POLICY":      r"minimum advertised price|\bmap policy\b|map pricing",
 "COLLECTIONS_NAV": r"\bcollections?\b",
 "CATALOG_DL":      r"download catalog|digital catalog|price list|pricelist|tear ?sheet|catalog request|request a catalog",
 "LOGIN_ANY":       r"sign in|log ?in|my account|create an account|register",
 "FOUNDED":         r"(since|established|est\.?|founded in) (1[89]\d\d|20[0-2]\d)",
 "MARKETPLACE":     r"wayfair|houzz|amazon\.com|overstock|perigold",
}
out=[]
for o in orgs:
    sn=o['org']; row=dict(org=sn,company=o['company'],v4=o['v4_segment'],domain=o['domain'])
    if sn not in usable:
        why = "no_domain" if not o['domain'] else ("blocked_or_dead")
        for k in M: row[k]="UNKNOWN"
        row['collect']=why
    else:
        blob=text_of(sn)+" "+links_of(sn)
        for k,pat in M.items(): row[k]="1" if re.search(pat,blob) else "0"
        row['collect']="auto"
    out.append(row)
cols=["org","company","v4","domain","collect"]+list(M)
w=csv.DictWriter(open('features.csv','w',newline=''),fieldnames=cols); w.writeheader(); w.writerows(out)
auto=[r for r in out if r['collect']=='auto']
print(f"observed automatically: {len(auto)} orgs\n")
segs=["1. Luxury Specification","2. Premium Trade Brand","3. Mid-Market Multi-Channel","4. Volume Distribution"]
print(f"{'marker':17}"+"".join(f"{s.split('. ')[1][:13]:>15}" for s in segs)+f"{'ALL':>8}")
for k in M:
    cells=[]
    for s in segs:
        g=[r for r in auto if r['v4']==s]
        cells.append(f"{sum(1 for r in g if r[k]=='1')}/{len(g)}")
    tot=sum(1 for r in auto if r[k]=='1')
    print(f"{k:17}"+"".join(f"{c:>15}" for c in cells)+f"{tot:>8}")
