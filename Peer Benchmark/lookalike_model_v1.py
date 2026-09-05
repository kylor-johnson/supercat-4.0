#!/usr/bin/env python3
"""
Lookalike Model v1 — Supercat Client Peer Matching
Hard filters: Industry Segment + Ordering Tier
Soft features: Weighted Euclidean Distance on z-scored log-transformed features
Similarity score: Gaussian decay — score = 100 * exp(-d^2 / (2 * sigma^2))
"""

import csv
import math
import sys
from collections import defaultdict

CSV_PATH = "/Users/kylorjohnson/Downloads/Copy of  Pricing Refresh Master Data V2 - v2 Master Entity.csv"

# ─── Segment assignments ─────────────────────────────────────────────
# From HubSpot properties_segment (BigQuery) where available,
# manual assignment where entity is not in org_feature_usage_report.
SEGMENT_MAP = {
    # === LIGHTING ===
    "Wildwood/Chelsea House": "Lighting",
    "Crystorama": "Lighting",
    "Jamie Young Company": "Lighting",
    "Bulbrite": "Lighting",
    "Kalco Lighting / Allegri Crystal": "Lighting",
    "Kuzco Lighting Inc.": "Lighting",
    "Golden Lighting": "Lighting",
    "Vaxcel International Corporation": "Lighting",
    "Elegant Furniture & Lighting": "Lighting",
    "Currey & Company": "Lighting",
    "Hubbardton Forge": "Lighting",
    "Eurofase Inc.": "Lighting",
    "Litex Industries": "Lighting",
    "Capital Lighting Fixture Co.": "Lighting",
    "Savoy House Lighting": "Lighting",
    "Access Lighting": "Lighting",
    "Globalux": "Lighting",
    "Millennium Lighting": "Lighting",
    "Buster & Punch": "Lighting",
    "Fine Art Handcrafted Lighting": "Lighting",
    "Minka Lighting Group": "Lighting",
    "Accord Lighting": "Lighting",
    "Matteo Lighting": "Lighting",
    "Ciana Varaluz LLC": "Lighting",
    "Eglo USA Inc.": "Lighting",
    "Designer's Fountain": "Lighting",
    "Dainolite Ltd.": "Lighting",
    "AFX, Inc.": "Lighting",
    "DALS Lighting": "Lighting",
    "Maxim Lighting International": "Lighting",
    "EGLO Canada": "Lighting",
    "Arabela Lighting": "Lighting",
    "Visual Comfort Europe": "Lighting",
    "Lucas McKearn": "Lighting",
    "Geo Contemporary": "Lighting",
    "Kennedy International, Inc.": "Lighting",  # per HubSpot properties_segment

    # === FURNITURE ===
    "Somerset Bay and Modern History": "Furniture",
    "Ratana International Ltd.": "Furniture",
    "Braxton Culler": "Furniture",
    "Four Seasons Furniture": "Furniture",
    "Linon/Powell Furniture": "Furniture",
    "Furniture Classics": "Furniture",
    "Donald Choi Canada": "Furniture",
    "Charleston Forge": "Furniture",
    "Alfresco Home": "Furniture",
    "Alden Home": "Furniture",
    "Sarreid, Ltd.": "Furniture",
    "Palecek": "Furniture",
    "Tomlinson Companies": "Furniture",
    "Oly Studio": "Furniture",
    "Universal Furniture": "Furniture",
    "Alfonso Marina": "Furniture",
    "Hooker Furnishings": "Furniture",
    "Magnussen Home": "Furniture",
    "Rowe Furniture": "Furniture",
    "Home Essentials & Beyond": "Furniture",  # per HubSpot properties_segment
    "America's Backyards": "Furniture",
    "Lifestyle Solutions": "Furniture",
    "Sauder Woodworking": "Furniture",
    "International Home Miami": "Furniture",
    "Butler Specialty Company": "Furniture",
    "Sabine Pools, Spas, & Furnitur": "Furniture",
    "Yutzy Woodworking": "Furniture",

    # === HOME & DECOR ===
    "RENWIL": "Home & Decor",
    "Groupe Courchesne": "Home & Decor",
    "Moda at Home Enterprises Ltd": "Home & Decor",
    "Morgan Fabrics Corporation": "Home & Decor",
    "Wendover Art Group": "Home & Decor",
    "Uniware Housewares Corp.": "Home & Decor",
    "ELICO LTD.": "Home & Decor",
    "Silver One": "Home & Decor",
    "Shadow Catchers": "Home & Decor",
    "Kaleen Rugs & Broadloom": "Home & Decor",
    "Sixtrees Limited": "Home & Decor",
}

GMV_OVERRIDES = {
    "Savoy House Lighting": 3607810,  # CSV had $466M due to a single $464M data-entry error (order #1505482)
}

ORDERS_OVERRIDES = {
    "Maxim Lighting International": 89,
    "Minka Lighting Group": 160,
}

GMV_ORDERS_OVERRIDES = {
    "Maxim Lighting International": 686178,
    "Minka Lighting Group": 1690326,
}

STACK_ORDINAL = {
    "iPad-only": 1,
    "iPad+Catalog": 2,
    "iPad+Catalog+Cart": 3,
    "iPad+Catalog+Portal": 3,
    "Full (Cart+Portal)": 4,
}

ORDERING_FEATURES = [
    "total_products_log", "total_customers_log", "billable_users_log",
    "gmv_log", "mrr_log", "stack_ordinal", "tenure",
]
ORDERING_WEIGHTS = [0.30, 0.15, 0.15, 0.15, 0.10, 0.10, 0.05]

NON_ORDERING_FEATURES = [
    "total_products_log", "total_customers_log", "billable_users_log",
    "mrr_log", "stack_ordinal", "tenure",
]
NON_ORDERING_WEIGHTS = [0.35, 0.20, 0.20, 0.10, 0.10, 0.05]

TARGETS = [
    "Kuzco Lighting Inc.",
    "Maxim Lighting International",
    "Currey & Company",
    "Wildwood/Chelsea House",
    "Sarreid, Ltd.",
]

THRESHOLDS_CASCADE = [60, 50, 40]  # Try tightest first, fall back as needed
MIN_PEERS = 5


def clean_num(val):
    if not val or val.strip() == "":
        return 0.0
    return float(val.replace("$", "").replace(",", ""))


def log1p(x):
    return math.log(1 + max(0, x))


def load_data():
    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header_row = None
        for i, row in enumerate(reader):
            if i == 0:
                continue  # skip blank first row
            if i == 1:
                header_row = [h.strip() for h in row]
                continue
            if len(row) < 5:
                continue
            record = {}
            for j, h in enumerate(header_row):
                record[h] = row[j] if j < len(row) else ""
            if record.get("entity_type", "").strip() != "standalone":
                continue
            rows.append(record)
    return rows


def build_feature_matrix(rows):
    entities = []
    for r in rows:
        name = r["entity_name"].strip()
        segment = SEGMENT_MAP.get(name)
        if not segment:
            print(f"  WARNING: No segment mapping for '{name}' — skipping")
            continue

        mrr = clean_num(r.get("mrr", "0"))
        billable_users = clean_num(r.get("billable_users", "0"))
        total_products = clean_num(r.get("total_products", "0"))
        total_customers = clean_num(r.get("total_customers", "0"))
        orders = clean_num(r.get("orders", "0"))
        if name in ORDERS_OVERRIDES:
            orders = ORDERS_OVERRIDES[name]
        gmv = clean_num(r.get("gmv", "0"))
        if name in GMV_OVERRIDES:
            gmv = GMV_OVERRIDES[name]
        if name in GMV_ORDERS_OVERRIDES:
            gmv = GMV_ORDERS_OVERRIDES[name]
        cohort = clean_num(r.get("cohort_year", "2025"))
        stack = r.get("stack", "iPad-only").strip()

        e = {
            "entity_name": name,
            "segment": segment,
            "ordering_tier": "ordering" if orders > 0 else "non-ordering",
            "total_products": total_products,
            "total_customers": total_customers,
            "billable_users": billable_users,
            "orders": orders,
            "gmv": gmv,
            "mrr": mrr,
            "stack": stack,
            "stack_ordinal": STACK_ORDINAL.get(stack, 1),
            "tenure": max(1, 2026 - int(cohort)),
            "cohort_year": int(cohort),
            "total_products_log": log1p(total_products),
            "total_customers_log": log1p(total_customers),
            "billable_users_log": log1p(billable_users),
            "gmv_log": log1p(gmv),
            "mrr_log": log1p(mrr),
        }
        entities.append(e)
    return entities


def z_score_features(entities, features):
    """Compute mean/std for each feature across entities, return z-scored matrix."""
    n = len(entities)
    k = len(features)
    raw = [[e[f] for f in features] for e in entities]

    means = [0.0] * k
    for j in range(k):
        means[j] = sum(raw[i][j] for i in range(n)) / n

    stds = [0.0] * k
    for j in range(k):
        variance = sum((raw[i][j] - means[j]) ** 2 for i in range(n)) / max(1, n - 1)
        stds[j] = math.sqrt(variance) if variance > 0 else 1.0

    z = []
    for i in range(n):
        z.append([(raw[i][j] - means[j]) / stds[j] for j in range(k)])
    return z


def weighted_euclidean(v1, v2, weights):
    return math.sqrt(sum(w * (a - b) ** 2 for a, b, w in zip(v1, v2, weights)))


def gaussian_similarity(distance, sigma=1.0):
    return 100.0 * math.exp(-(distance ** 2) / (2 * sigma ** 2))


def compute_peers(target_name, entities, min_pool=6, sigma=1.0):
    target = None
    for e in entities:
        if e["entity_name"] == target_name:
            target = e
            break
    if target is None:
        return None

    segment = target["segment"]
    ordering = target["ordering_tier"]

    pool_full = [e for e in entities if e["segment"] == segment and e["entity_name"] != target_name]
    pool = [e for e in pool_full if e["ordering_tier"] == ordering]
    filter_note = ""

    if len(pool) < min_pool:
        filter_note = f"(ordering filter relaxed — only {len(pool)} same-tier candidates, using full segment pool of {len(pool_full)})"
        pool = pool_full

    if not pool:
        return {"target": target_name, "error": "No candidates in segment"}

    if ordering == "ordering":
        features = ORDERING_FEATURES
        weights = ORDERING_WEIGHTS
    else:
        features = NON_ORDERING_FEATURES
        weights = NON_ORDERING_WEIGHTS

    all_ents = pool + [target]
    z = z_score_features(all_ents, features)
    target_z = z[-1]

    results = []
    for i, candidate in enumerate(pool):
        d = weighted_euclidean(z[i], target_z, weights)
        score = gaussian_similarity(d, sigma=sigma)
        results.append({
            "entity_name": candidate["entity_name"],
            "distance": d,
            "similarity": score,
            "total_products": candidate["total_products"],
            "total_customers": candidate["total_customers"],
            "billable_users": candidate["billable_users"],
            "orders": candidate["orders"],
            "gmv": candidate["gmv"],
            "mrr": candidate["mrr"],
            "stack": candidate["stack"],
            "tenure": candidate["tenure"],
        })

    results.sort(key=lambda x: x["similarity"], reverse=True)

    return {
        "target": target_name,
        "segment": segment,
        "ordering_tier": ordering,
        "pool_size": len(pool),
        "filter_note": filter_note,
        "target_stats": {
            "total_products": target["total_products"],
            "total_customers": target["total_customers"],
            "billable_users": target["billable_users"],
            "orders": target["orders"],
            "gmv": target["gmv"],
            "mrr": target["mrr"],
            "stack": target["stack"],
            "tenure": target["tenure"],
        },
        "peers": results,
    }


def fmt_num(n):
    return f"{int(n):,}"


def fmt_dollar(n):
    if n >= 1_000_000:
        return f"${n / 1_000_000:,.1f}M"
    elif n >= 1_000:
        return f"${n / 1_000:,.0f}K"
    else:
        return f"${n:,.0f}"


def adaptive_threshold(result, cascade=THRESHOLDS_CASCADE, min_peers=MIN_PEERS):
    """Try tightest threshold first. Fall back until min_peers is met."""
    for threshold in cascade:
        peers = [p for p in result["peers"] if p["similarity"] >= threshold]
        if len(peers) >= min_peers:
            return threshold, peers
    # If even the loosest threshold doesn't hit min_peers, use it anyway
    loosest = cascade[-1]
    return loosest, [p for p in result["peers"] if p["similarity"] >= loosest]


def print_results(result):
    if result is None or "error" in result:
        print(f"\n  ERROR: {result}")
        return

    s = result["target_stats"]
    threshold_used, peers = adaptive_threshold(result)
    total_above_loosest = len([p for p in result["peers"] if p["similarity"] >= THRESHOLDS_CASCADE[-1]])

    print(f"\n{'━' * 140}")
    print(f"  TARGET: {result['target']}")
    print(f"  Segment: {result['segment']}  |  Ordering: {result['ordering_tier']}  |  Candidate Pool: {result['pool_size']} entities  {result['filter_note']}")
    print(f"  Profile: {fmt_num(s['total_products'])} products  |  {fmt_num(s['total_customers'])} customers  |  "
          f"{fmt_num(s['billable_users'])} users  |  {fmt_num(s['orders'])} orders  |  "
          f"{fmt_dollar(s['gmv'])} GMV  |  {fmt_dollar(s['mrr'])} MRR  |  {s['stack']}  |  {s['tenure']}yr")
    print(f"{'━' * 140}")

    # Show cascade decision
    cascade_detail = []
    for t in THRESHOLDS_CASCADE:
        count = len([p for p in result["peers"] if p["similarity"] >= t])
        marker = " ◄── SELECTED" if t == threshold_used else ""
        cascade_detail.append(f"≥{t}: {count} peers{marker}")
    print(f"  Adaptive threshold: {' → '.join(cascade_detail)}  (min_peers={MIN_PEERS})")

    if not peers:
        print(f"  No peers matched at any threshold.\n")
        return

    print(f"\n  ┌─ Final Peer Group: {len(peers)} peers at threshold ≥{threshold_used}")
    hdr = f"  │ {'#':<4} {'Entity':<38} {'Score':>5}  {'Products':>10}  {'Customers':>10}  {'Users':>7}  {'Orders':>7}  {'GMV':>10}  {'MRR':>8}  {'Stack':<22}  {'Tenure':>6}"
    sep = f"  │ {'─'*4} {'─'*38} {'─'*5}  {'─'*10}  {'─'*10}  {'─'*7}  {'─'*7}  {'─'*10}  {'─'*8}  {'─'*22}  {'─'*6}"
    print(hdr)
    print(sep)

    for i, p in enumerate(peers, 1):
        print(f"  │ {i:<4} {p['entity_name']:<38} {p['similarity']:>5.1f}  {fmt_num(p['total_products']):>10}  "
              f"{fmt_num(p['total_customers']):>10}  {fmt_num(p['billable_users']):>7}  {fmt_num(p['orders']):>7}  "
              f"{fmt_dollar(p['gmv']):>10}  {fmt_dollar(p['mrr']):>8}  {p['stack']:<22}  {p['tenure']:>4}yr")

    print(f"  └{'─' * 139}")

    # Benchmark averages
    avg_products = sum(p["total_products"] for p in peers) / len(peers)
    avg_customers = sum(p["total_customers"] for p in peers) / len(peers)
    avg_users = sum(p["billable_users"] for p in peers) / len(peers)
    avg_orders = sum(p["orders"] for p in peers) / len(peers)
    avg_gmv = sum(p["gmv"] for p in peers) / len(peers)
    avg_mrr = sum(p["mrr"] for p in peers) / len(peers)

    print(f"\n  ┌─ Benchmark Averages (peer group mean)")
    print(f"  │  Products: {fmt_num(avg_products)}  |  Customers: {fmt_num(avg_customers)}  |  Users: {fmt_num(avg_users)}  |  "
          f"Orders: {fmt_num(avg_orders)}  |  GMV: {fmt_dollar(avg_gmv)}  |  MRR: {fmt_dollar(avg_mrr)}")
    print(f"  │")
    print(f"  │  vs. Target:")
    diff_products = ((s['total_products'] / avg_products) - 1) * 100 if avg_products > 0 else 0
    diff_customers = ((s['total_customers'] / avg_customers) - 1) * 100 if avg_customers > 0 else 0
    diff_users = ((s['billable_users'] / avg_users) - 1) * 100 if avg_users > 0 else 0
    diff_orders = ((s['orders'] / avg_orders) - 1) * 100 if avg_orders > 0 else 0
    diff_gmv = ((s['gmv'] / avg_gmv) - 1) * 100 if avg_gmv > 0 else 0

    def fmt_diff(val):
        sign = "+" if val >= 0 else ""
        return f"{sign}{val:.0f}%"

    print(f"  │  Products: {fmt_diff(diff_products)}  |  Customers: {fmt_diff(diff_customers)}  |  Users: {fmt_diff(diff_users)}  |  "
          f"Orders: {fmt_diff(diff_orders)}  |  GMV: {fmt_diff(diff_gmv)}")
    print(f"  └{'─' * 139}")


def main():
    print("\n  Loading data...")
    rows = load_data()
    print(f"  Loaded {len(rows)} standalone entities from CSV")

    entities = build_feature_matrix(rows)
    print(f"  Built feature matrix for {len(entities)} entities")

    seg_counts = defaultdict(int)
    for e in entities:
        seg_counts[e["segment"]] += 1
    print(f"  Segment distribution: {dict(seg_counts)}")

    ord_counts = defaultdict(int)
    for e in entities:
        ord_counts[f"{e['segment']}|{e['ordering_tier']}"] += 1
    print(f"  Segment × Ordering pools:")
    for k in sorted(ord_counts):
        print(f"    {k}: {ord_counts[k]}")

    print(f"\n{'═' * 140}")
    print(f"  LOOKALIKE MODEL v1 — PEER MATCHING RESULTS (Adaptive Threshold)")
    print(f"  Scoring: Gaussian decay with σ=1.0  |  Features: 7 (ordering) / 6 (non-ordering)")
    print(f"  Hard filters: Segment must-match + Ordering tier must-match (relaxed if pool < 6)")
    print(f"  Adaptive threshold: try ≥60 first → fall back to ≥50 → ≥40 if fewer than {MIN_PEERS} peers")
    print(f"{'═' * 140}")

    for target in TARGETS:
        result = compute_peers(target, entities, min_pool=6, sigma=1.0)
        print_results(result)

    print(f"\n{'═' * 140}")
    print(f"  COMPLETE")
    print(f"{'═' * 140}\n")


if __name__ == "__main__":
    main()
