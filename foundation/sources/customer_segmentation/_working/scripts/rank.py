import csv,re,os
rows=[r for r in csv.DictReader(open('hp/cands_m.csv')) if r['obs']=='auto']
def b(r,k): return r[k]=='1'
def score(r):
    L=r['lane']; s=0; why=[]
    if L=='L1':
        if b(r,'TRADE_GATE'): s+=3; why.append('+trade/designer gate')
        if not b(r,'PRICE_VISIBLE') and not b(r,'RETAIL_ECOM'): s+=2; why.append('+no public price/cart')
        else: s-=3; why.append('-PUBLIC PRICE/CART')
        if b(r,'CONTRACT_SPEC'): s+=1; why.append('+contract/spec')
        if b(r,'COM_PROGRAM'): s+=1; why.append('+COM')
        if b(r,'WHERE_TO_BUY'): s-=1; why.append('-consumer locator')
    if L=='L2':
        if b(r,'DEALER_PORTAL'): s+=3; why.append('+dealer portal/recruit')
        if b(r,'WHERE_TO_BUY'): s+=1; why.append('+dealer locator')
        if not b(r,'PRICE_VISIBLE') and not b(r,'RETAIL_ECOM'): s+=2; why.append('+no public price/cart')
        else: s-=2; why.append('-PUBLIC PRICE/CART')
        if b(r,'TRADE_GATE'): s-=1; why.append('-designer-gated (lane1?)')
    if L=='L3':
        if b(r,'WHERE_TO_BUY'): s+=3; why.append('+consumer where-to-buy')
        if b(r,'TRADE_GATE'): s-=4; why.append('-TRADE GATED (excl)')
        if b(r,'COM_PROGRAM'): s-=3; why.append('-COM PROGRAM (excl)')
        if b(r,'CATALOG_DL'): s+=1; why.append('+catalog/price list')
        if b(r,'DEALER_PORTAL'): s+=1; why.append('+dealer portal')
    r['score']=s; r['why']='; '.join(why)
    return s
for r in rows: score(r)
def nav(eid,n=22):
    p=f"cpages/{eid}__home.html"
    if not os.path.exists(p): return ''
    h=open(p,encoding='utf-8',errors='ignore').read()
    a=[]
    for m in re.finditer(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',h,re.S|re.I):
        t=re.sub(r'<[^>]+>','',m.group(2)); t=re.sub(r'\s+',' ',t).strip()
        if t and 2<len(t)<28 and t not in a: a.append(t)
    return ' | '.join(a[:n])
for lane,label in (('L1','LANE 1  Luxury Spec x Furniture'),('L2','LANE 2  Premium Trade x Furniture'),('L3','LANE 3  Mid-Market x Lighting')):
    g=sorted([r for r in rows if r['lane']==lane],key=lambda x:-x['score'])[:14]
    print(f"\n{'='*100}\n{label}\n{'='*100}")
    for r in g:
        print(f"\n[{r['score']:+d}] {r['name']}  <{r['guess']}>  eid={r['eid']}")
        print(f"      HPMKT: {r['loc'][:100]}")
        print(f"      {r['why']}")
        print(f"      NAV: {nav(r['eid'])[:250]}")
w=csv.DictWriter(open('hp/ranked.csv','w',newline=''),fieldnames=list(rows[0])); w.writeheader(); w.writerows(sorted(rows,key=lambda x:(x['lane'],-x['score'])))
