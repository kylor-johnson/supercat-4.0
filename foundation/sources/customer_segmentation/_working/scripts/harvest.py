import re,subprocess,urllib.parse,json,csv,sys,os,concurrent.futures as cf
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
def get(url):
    r=subprocess.run(["curl","-sSL","--compressed","--max-time","30","-A",UA,url],capture_output=True)
    return r.stdout.decode('utf-8','ignore')
def furl(cat,page):
    f=json.dumps({"Type":"Categories","Values":[cat]},separators=(',',':'))
    return f"https://www.highpointmarket.org/exhibitordirectory?pageindex={page}&filters={urllib.parse.quote(f)}"
ROW=re.compile(r'exhibitor-block\s+([A-Za-z0-9_\- ]*)".*?<h2><a href="/exhibitor/(\d+)">(.*?)</a></h2>(.*?)(?=exhibitor-block|<div class="pagination)',re.S)
def parse(html,cat):
    out=[]
    for m in ROW.finditer(html):
        nbhd,eid,name,tail=m.groups()
        txt=re.sub(r'<[^>]+>',' ',tail); txt=re.sub(r'&amp;','&',txt); txt=re.sub(r'\s+',' ',txt).strip()
        name=re.sub(r'<[^>]+>','',name); name=re.sub(r'&amp;','&',name).strip()
        out.append(dict(cat=cat,eid=eid,name=name,neighborhood=nbhd.strip(),loc=txt[:160]))
    return out
def total(html):
    m=re.search(r'PAGINATION_TOTAL\s*=\s*(\d+)',html)
    return int(m.group(1)) if m else 1
CATS=sys.argv[1:]
allrows=[]
for cat in CATS:
    h=get(furl(cat,1)); n=total(h)
    print(f"{cat}: {n} pages", flush=True)
    rows=parse(h,cat)
    pages=list(range(2,n+1))
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for hh in ex.map(lambda p: get(furl(cat,p)), pages):
            rows+=parse(hh,cat)
    print(f"   -> {len(rows)} rows", flush=True)
    allrows+=rows
w=csv.DictWriter(open('hp/frame.csv','a',newline=''),fieldnames=["cat","eid","name","neighborhood","loc"])
if os.path.getsize('hp/frame.csv') if os.path.exists('hp/frame.csv') else 0: pass
else: w.writeheader()
w.writerows(allrows)
print("TOTAL rows appended:",len(allrows))
