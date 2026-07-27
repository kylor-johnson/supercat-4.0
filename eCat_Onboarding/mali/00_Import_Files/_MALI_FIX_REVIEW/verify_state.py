#!/usr/bin/env python3
"""Independent re-verification of Magic Lite (mali) products.csv state vs 7/23 baseline."""
import csv, sys, os
from collections import defaultdict, Counter

WORK = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/products.csv"
BASE = "/Users/kylorjohnson/Downloads/products.csv.20260723-2122.csv"

def load(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    return rows

def norm(s):
    return (s or "").strip()

def first_img(s):
    s = norm(s)
    if not s:
        return ""
    return s.split(",")[0].strip()

def related_set(s):
    s = norm(s)
    if not s:
        return []
    return [x.strip() for x in s.split(",") if x.strip()]

def analyze(rows, label):
    skus = [norm(r["BaseItemCode"]) for r in rows]
    sku_set = set(skus)
    dup_skus = [k for k,v in Counter(skus).items() if v > 1]
    visible = [r for r in rows if norm(r.get("Hideable","")).upper() != "Y"]
    hidden  = [r for r in rows if norm(r.get("Hideable","")).upper() == "Y"]

    # reachability: any SKU referenced in ANY product's RelatedItems
    referenced = set()
    for r in rows:
        for ref in related_set(r.get("RelatedItems","")):
            referenced.add(ref)

    orphan_hidden = [r for r in hidden if norm(r["BaseItemCode"]) not in referenced]

    print(f"=== {label} ===")
    print(f"  Total SKUs        : {len(rows)}")
    print(f"  Unique SKUs       : {len(sku_set)}")
    print(f"  Duplicate SKUs    : {len(dup_skus)} {dup_skus if dup_skus else ''}")
    print(f"  Visible (N)       : {len(visible)}")
    print(f"  Hidden (Y)        : {len(hidden)}")
    print(f"  Orphaned-hidden   : {len(orphan_hidden)}")
    return {
        "rows": rows, "sku_set": sku_set, "visible": visible, "hidden": hidden,
        "orphan_hidden": orphan_hidden, "referenced": referenced,
        "by_sku": {norm(r["BaseItemCode"]): r for r in rows},
    }

def main():
    w = load(WORK); b = load(BASE)
    W = analyze(w, "WORKING products.csv")
    print()
    B = analyze(b, "BASELINE 7/23-2122")
    print()

    print("=== SKU SET DIFF (working vs baseline) ===")
    lost = B["sku_set"] - W["sku_set"]
    added = W["sku_set"] - B["sku_set"]
    print(f"  Lost (in baseline, not working): {len(lost)} {sorted(lost) if lost else ''}")
    print(f"  Added (in working, not baseline): {len(added)} {sorted(added) if added else ''}")
    print()

    # RelatedItems integrity on working
    print("=== WORKING RelatedItems INTEGRITY ===")
    bad_refs = defaultdict(list)
    too_long = []
    for r in W["rows"]:
        sku = norm(r["BaseItemCode"])
        ri = norm(r.get("RelatedItems",""))
        if len(ri) > 255:
            too_long.append((sku, len(ri)))
        for ref in related_set(ri):
            if ref not in W["sku_set"]:
                bad_refs[sku].append(ref)
    print(f"  RelatedItems >255 chars: {len(too_long)} {too_long if too_long else ''}")
    print(f"  RelatedItems dangling refs: {sum(len(v) for v in bad_refs.values())} across {len(bad_refs)} SKUs")
    for sku, refs in list(bad_refs.items())[:40]:
        print(f"     {sku} -> {refs}")
    print()

    # Shared primary images among VISIBLE products
    print("=== SHARED PRIMARY (hero) IMAGES AMONG VISIBLE PRODUCTS ===")
    vis_img = defaultdict(list)
    for r in W["visible"]:
        img = first_img(r.get("ImageFileName",""))
        if img:
            vis_img[img.lower()].append(norm(r["BaseItemCode"]))
    shared = {img: skus for img, skus in vis_img.items() if len(skus) > 1}
    total_prod_in_shared = sum(len(v) for v in shared.values())
    print(f"  Shared hero images among visible: {len(shared)} clusters covering {total_prod_in_shared} products")
    for img, skus in sorted(shared.items(), key=lambda kv:-len(kv[1])):
        print(f"     [{len(skus)}] {img}: {', '.join(sorted(skus))}")
    print()

    # Visible with NO image
    vis_noimg = [norm(r["BaseItemCode"]) for r in W["visible"] if not first_img(r.get("ImageFileName",""))]
    print(f"=== VISIBLE PRODUCTS WITH NO HERO IMAGE: {len(vis_noimg)} ===")
    if vis_noimg:
        print("   " + ", ".join(sorted(vis_noimg)))
    print()

    # Orphan-hidden split: share image with a visible product vs not
    print("=== ORPHAN-HIDDEN SPLIT ===")
    vis_img_keys = set(vis_img.keys())
    orphan_share_visible = []
    orphan_no_visible = []
    for r in W["orphan_hidden"]:
        img = first_img(r.get("ImageFileName","")).lower()
        sku = norm(r["BaseItemCode"])
        if img and img in vis_img_keys:
            orphan_share_visible.append((sku, img, vis_img[img]))
        else:
            orphan_no_visible.append((sku, img))
    print(f"  Orphan-hidden sharing image w/ a VISIBLE product: {len(orphan_share_visible)}")
    print(f"  Orphan-hidden with NO visible image-sibling      : {len(orphan_no_visible)}")

if __name__ == "__main__":
    main()
