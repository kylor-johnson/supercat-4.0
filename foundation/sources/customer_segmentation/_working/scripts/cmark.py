import csv,re,os,glob
M={
 "TRADE_GATE": r"to the trade|trade only|trade program|trade account|trade portal|trade login|designer program|designer resources|designer trade|trade professional|design professional|apply for.{0,20}trade",
 "DEALER_PORTAL": r"dealer login|dealer portal|dealer resources|retailer login|wholesale login|b2b portal|authorized dealer|dealer center|become a dealer|apply to become a dealer|dealer application",
 "RETAIL_ECOM": r"add to cart|add to bag|add to basket|proceed to checkout|shopping cart",
 "PRICE_VISIBLE": r"\$\s?\d[\d,]*\.\d{2}",
 "WHERE_TO_BUY": r"where to buy|find a dealer|find a retailer|store locator|dealer locator|showroom locator|find a store|find a showroom",
 "REP_NETWORK": r"sales rep|find a rep|rep locator|sales representative|territory manager|rep territory|our reps|representative directory",
 "CONTRACT_SPEC": r"hospitality|contract grade|contract division|contract market|specification|spec sheet|a&d |architects and designers|architect & design",
 "COM_PROGRAM": r"customer'?s own material|customer own material|com program|com/col|\bcom & col\b",
 "CATALOG_DL": r"download catalog|digital catalog|price list|pricelist|tear ?sheet|catalog request|request a catalog",
 "LOGIN_ANY": r"sign in|log ?in|my account|create an account|register",
}
BAD=re.compile(r'just a moment|enable javascript and cookies|attention required|access denied|403 forbidden',re.I)
rows=[r for r in csv.DictReader(open('hp/cands_v.csv')) if r['http'].startswith(('2','3'))]
out=[]
for r in rows:
    p=f"cpages/{r['eid']}__home.html"
    if not os.path.exists(p) or os.path.getsize(p)<1500:
        for k in M: r[k]='UNKNOWN'
        r['obs']='no_page'; out.append(r); continue
    h=open(p,encoding='utf-8',errors='ignore').read()
    t=re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->','',h,flags=re.S|re.I)
    links=' '.join(re.findall(r'href="([^"]+)"',h))
    t=re.sub(r'<[^>]+>',' ',t); t=re.sub(r'&nbsp;?|&amp;',' ',t); t=re.sub(r'\s+',' ',t).lower()
    blob=t+' '+links.lower()
    if BAD.search(h[:4000]) and len(t.split())<200:
        for k in M: r[k]='UNKNOWN'
        r['obs']='blocked'
    else:
        for k,pat in M.items(): r[k]='1' if re.search(pat,blob) else '0'
        r['obs']='auto'
    out.append(r)
w=csv.DictWriter(open('hp/cands_m.csv','w',newline=''),fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
from collections import Counter
print(Counter(r['obs'] for r in out))
auto=[r for r in out if r['obs']=='auto']
for lane in ('L1','L2','L3'):
    g=[r for r in auto if r['lane']==lane]
    print(f"\n{lane} n={len(g)}")
    for k in M: print(f"   {k:15} {sum(1 for r in g if r[k]=='1'):3d}/{len(g)}")
