import csv, re, os, json
SEG_CSV = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv")
raw = json.load(open(os.path.join(os.path.dirname(__file__),"pg_websites.json")))

# malformed values -> (primary, [secondary]) ; logged as data-quality items
MALFORMED = {
 "kal":  ("kalco.com", ["allegricrystal.com"]),
 "sbmh": ("modernhistoryhome.com", ["somersetbayhome.com"]),
 "wac":  ("waclighting.com", ["modernforms.com"]),
}
def norm(u):
    u = (u or "").strip()
    u = re.sub(r'^https?://', '', u, flags=re.I)
    u = re.sub(r'^www\.', '', u, flags=re.I)
    u = u.split('/')[0].split('?')[0].strip().lower()
    return u

seg = {}
for r in csv.DictReader(open(SEG_CSV)):
    seg[r['org'].strip()] = (r['Company'].strip(), r['v4_segment'].strip())

out=[]
dq=[]
for sn, name, site in raw:
    if sn in MALFORMED:
        dom, sec = MALFORMED[sn]
        dq.append((sn, site, dom, ";".join(sec)))
    else:
        dom = norm(site); sec=[]
    company, v4 = seg.get(sn, ("",""))
    out.append(dict(org=sn, name=name, company=company, v4_segment=v4, domain=dom,
                    secondary=";".join(sec)))
w = csv.DictWriter(open(os.path.join(os.path.dirname(__file__),"orgs.csv"),"w",newline=""),
                   fieldnames=["org","name","company","v4_segment","domain","secondary"])
w.writeheader(); w.writerows(out)
print("rows:", len(out))
print("blank domain:", sum(1 for o in out if not o['domain']))
print("distinct domains:", len({o['domain'] for o in out if o['domain']}))
from collections import Counter
print("segments:", Counter(o['v4_segment'] for o in out))
print("\nDATA-QUALITY (malformed company_website, fixed in working copy only):")
for d in dq: print("  ", d)
