import re,subprocess,urllib.parse,json,csv,sys,concurrent.futures as cf
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
def get(u):
    return subprocess.run(["curl","-sSL","--compressed","--max-time","30","-A",UA,u],capture_output=True).stdout.decode('utf-8','ignore')
def furl(typ,vals,page):
    f=json.dumps({"Type":typ,"Values":vals},separators=(',',':'))
    return f"https://www.highpointmarket.org/exhibitordirectory?pageindex={page}&filters={urllib.parse.quote(f)}"
ROW=re.compile(r'<h2><a href="/exhibitor/(\d+)">(.*?)</a></h2>',re.S)
def ids(h): return [(m.group(1),re.sub(r'<[^>]+>','',m.group(2)).strip()) for m in ROW.finditer(h)]
def tot(h):
    m=re.search(r'PAGINATION_TOTAL\s*=\s*(\d+)',h); return int(m.group(1)) if m else 1
SETS=[("Options",["Designer Friendly"],"designer_friendly"),
      ("PricePoint",["High"],"price_high"),
      ("PricePoint",["Medium-High"],"price_medhigh"),
      ("PricePoint",["Medium"],"price_medium"),
      ("Categories",["Contract/Hospitality"],"contract_hosp")]
out={}
for typ,vals,tag in SETS:
    h=get(furl(typ,vals,1)); n=tot(h); rows=ids(h)
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for hh in ex.map(lambda p: get(furl(typ,vals,p)), range(2,n+1)): rows+=ids(hh)
    out[tag]={e for e,_ in rows}
    print(f"{tag:16} {n:3d} pages -> {len(out[tag])} exhibitors", flush=True)
json.dump({k:sorted(v) for k,v in out.items()}, open('hp/attrs.json','w'))
