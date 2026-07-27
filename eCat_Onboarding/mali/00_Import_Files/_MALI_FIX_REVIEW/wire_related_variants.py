#!/usr/bin/env python3
"""
Wire the 81 orphaned-hidden Landscape/RGB variants into their VISIBLE parent's
RelatedItems so tapping a hero surfaces the full color/finish range.

Deterministic line rules (each orphan -> exactly one visible hero). Appends to
the hero's existing RelatedItems (dedup, preserves existing order). Hidden flags
are NOT touched. SKU set is invariant.

DRY_RUN=True  -> prints the full diff, writes nothing.
DRY_RUN=False -> backs up products.csv then writes.
"""
import csv, sys, os, datetime

WORK="/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/products.csv"
EXPECT_ROWS=683
DRY_RUN = ("--write" not in sys.argv)

def n(s): return (s or "").strip()
def codes(v): return [n(x) for x in n(v).replace(";",",").split(",") if n(x)]

def hero_for(sku):
    """Return the visible parent SKU for an orphaned variant, or None."""
    # Switch Star -> Prism White hero
    if sku.startswith("LED-SW-"):
        return "LED-SW-P-WH"
    # Disc Light: Concrete Form + Clear + Dome -> Clear-Dome hero; Frosted -> Frosted hero
    if sku.startswith("LEDD-"):
        if sku.startswith("LEDD-F-"):
            return "LEDD-F-WH"
        # LEDD-C-*, LEDD-CF-* (concrete form mount), and any dome
        return "LEDD-C-WH-D"
    # Mini Disc Scoop -> scoop hero ; Mini Disc Marker Round/Square -> round hero
    if sku.startswith("LEDMD-S-"):
        return "LEDMD-S-WH-AL"
    if sku.startswith("LEDMD-"):
        return "LEDMD-WH-AL"
    # RGB flex connectors -> RGB controller hero
    if sku.startswith("NFLX-RGB-"):
        return "NFLX-RGB-CONTROL"
    return None

def main():
    with open(WORK, encoding="utf-8-sig", newline="") as f:
        rd=csv.DictReader(f); FIELDS=rd.fieldnames; rows=list(rd)
    assert len(rows)==EXPECT_ROWS, f"row count {len(rows)} != {EXPECT_ROWS}"
    by={n(r["BaseItemCode"]):r for r in rows}
    def vis(r): return n(r["Hideable"]).upper()!="Y"

    # reachable from visible products (current)
    reachable=set()
    for r in rows:
        if vis(r):
            reachable.add(n(r["BaseItemCode"]))
            for ri in codes(r["RelatedItems"]): reachable.add(ri)
    orphans=[n(r["BaseItemCode"]) for r in rows if not vis(r) and n(r["BaseItemCode"]) not in reachable]

    # build additions per hero
    additions={}   # hero -> ordered list of orphan skus to append
    unresolved=[]
    for o in orphans:
        h=hero_for(o)
        if h is None or h not in by:
            unresolved.append((o,h)); continue
        if not vis(by[h]):
            unresolved.append((o,h+"(hidden!)")); continue
        additions.setdefault(h,[]).append(o)

    # apply (in memory) with dedup + preserve existing order
    total_added=0
    diff=[]
    for h in sorted(additions):
        cur=codes(by[h]["RelatedItems"])
        curset=set(cur)
        new=list(cur)
        added_here=[]
        for o in sorted(additions[h]):
            if o not in curset:
                new.append(o); curset.add(o); added_here.append(o)
        if added_here:
            total_added+=len(added_here)
            diff.append((h, cur, new, added_here))
            by[h]["RelatedItems"]=",".join(new)

    # report
    print(f"orphans={len(orphans)}  heroes touched={len(diff)}  refs added={total_added}  unresolved={len(unresolved)}\n")
    for h,cur,new,added in diff:
        print(f"HERO {h}  ({n(by[h]['ShortDesc'])[:44]})")
        print(f"   existing related ({len(cur)}): {', '.join(cur) if cur else '(none)'}")
        print(f"   + adding ({len(added)}): {', '.join(added)}")
        print()
    if unresolved:
        print("=== UNRESOLVED (NOT wired — need decision) ===")
        for o,h in unresolved: print(f"   {o} -> {h}")
        print()

    # integrity checks
    allsku=set(by)
    dangling=set()
    for r in rows:
        for ri in codes(r["RelatedItems"]):
            if ri not in allsku: dangling.add(ri)
    assert not dangling, f"dangling refs introduced: {sorted(dangling)[:10]}"
    assert len(rows)==EXPECT_ROWS
    print(f"integrity: rows={len(rows)} unique={len(allsku)} dangling={len(dangling)}  OK")

    if DRY_RUN:
        print("\nDRY-RUN — no file written. Re-run with --write to apply.")
        return
    stamp=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bak=WORK+f".bak_relwire_{stamp}.csv"
    with open(WORK,encoding="utf-8-sig") as f: raw=f.read()
    with open(bak,"w",encoding="utf-8") as f: f.write(raw)
    with open(WORK,"w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f, fieldnames=FIELDS); w.writeheader()
        for r in rows: w.writerow(r)
    print(f"\nWROTE {WORK}\nBACKUP {bak}")

if __name__=="__main__":
    main()
