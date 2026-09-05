"""
Lookalike Model — Benchmark Peer Assignment
Computes similarity between eCat client entities using weighted features
and three threshold approaches for peer selection.
"""

import csv
import math
import json
import sys
from collections import defaultdict

# ── Configuration ──────────────────────────────────────────────────────────

WEIGHTS = {
    'log_mrr': 0.20,
    'log_products': 0.15,
    'log_customers': 0.15,
    'stack_ordinal': 0.15,
    'log_orders': 0.10,
    'log_users': 0.10,
    'feature_surface': 0.10,
    'tenure_years': 0.05,
}

STACK_ORDINAL = {
    'iPad-only': 1,
    'iPad+Catalog': 2,
    'iPad+Catalog+Cart': 3,
    'iPad+Catalog+Portal': 4,
    'Full (Cart+Portal)': 5,
}

# Manual segment assignments for CSV entities
# (mapped from HubSpot segment data on child entities)
SEGMENT_MAP = {
    'Gabriella White': 'Furniture',
    'Godinger Silver Art Co.': 'Home & Decor / Housewares / Art Manufacturers',
    'Generation Brands': 'Lighting',
    'Baker\u00ac\u00a8\u201a\u00c4\u2020Interiors Group': 'Furniture',
    'Interlude Home': 'Furniture',
    'Abaline': 'Generic B2B Wholesale',
    'Coleto Brands': 'Lighting',
    'Theodore\u00ac\u00a8\u201a\u00c4\u2020Alexander': 'Furniture',
    'Jonathan Charles': 'Furniture',
    'WAC': 'Lighting',
    'Century Furniture': 'Furniture',
    'HVLG': 'Lighting',
    'Wildwood/Chelsea House': 'Lighting',
    'Crystorama': 'Lighting',
    'Somerset Bay and Modern History': 'Furniture',
    'RENWIL': 'Home & Decor / Housewares / Art Manufacturers',
    'Ratana International Ltd.': 'Furniture',
    'Braxton Culler': 'Furniture',
    'Four Seasons Furniture': 'Furniture',
    'Jamie Young Company': 'Lighting',
    'Bulbrite': 'Lighting',
    'Kalco Lighting / Allegri Crystal': 'Lighting',
    'Kuzco Lighting Inc.': 'Lighting',
    'Linon/Powell Furniture': 'Furniture',
    'Golden Lighting': 'Lighting',
    'Furniture Classics': 'Furniture',
    'Vaxcel International Corporation': 'Lighting',
    'Elegant Furniture & Lighting': 'Lighting',
    'Currey & Company': 'Lighting',
    'Hubbardton Forge': 'Lighting',
    'Eurofase Inc.': 'Lighting',
    'Litex Industries': 'Lighting',
    'Capital Lighting Fixture Co.': 'Lighting',
    'Savoy House Lighting': 'Lighting',
    'Donald Choi Canada': 'Lighting',
    'Access Lighting': 'Lighting',
    'Charleston Forge': 'Furniture',
    'Alfresco Home': 'Furniture',
    'Groupe Courchesne': 'Home & Decor / Housewares / Art Manufacturers',
    'Kennedy International, Inc.': 'Lighting',
    'Moda at Home Enterprises Ltd': 'Home & Decor / Housewares / Art Manufacturers',
    'Alden Home': 'Furniture',
    'Sarreid, Ltd.': 'Furniture',
    'Globalux': 'Lighting',
    'Palecek': 'Furniture',
    'Millennium Lighting': 'Lighting',
    'Tomlinson Companies': 'Furniture',
    'Morgan Fabrics Corporation': 'Home & Decor / Housewares / Art Manufacturers',
    'Oly Studio': 'Furniture',
    'Buster & Punch': 'Home & Decor / Housewares / Art Manufacturers',
    'Universal Furniture': 'Furniture',
    'Alfonso Marina': 'Furniture',
    'Hooker Furnishings': 'Furniture',
    'Geo Contemporary': 'Lighting',
    'Fine Art Handcrafted Lighting': 'Lighting',
    'Magnussen Home': 'Furniture',
    'Minka Lighting Group': 'Lighting',
    'Wendover Art Group': 'Home & Decor / Housewares / Art Manufacturers',
    'Accord Lighting': 'Lighting',
    'Matteo Lighting': 'Lighting',
    'Ciana Varaluz LLC': 'Lighting',
    'Eglo USA Inc.': 'Lighting',
    "Designer's Fountain": 'Lighting',
    'Dainolite Ltd.': 'Lighting',
    'Rowe Furniture': 'Furniture',
    'AFX, Inc.': 'Lighting',
    'Home Essentials & Beyond': 'Home & Decor / Housewares / Art Manufacturers',
    'Uniware Housewares Corp.': 'Home & Decor / Housewares / Art Manufacturers',
    'Silver One': 'Home & Decor / Housewares / Art Manufacturers',
    "America's Backyards": 'Furniture',
    'DALS Lighting': 'Lighting',
    'Shadow Catchers': 'Home & Decor / Housewares / Art Manufacturers',
    'Lifestyle Solutions': 'Furniture',
    'Sauder Woodworking': 'Furniture',
    'ELICO LTD.': 'Lighting',
    'Kaleen Rugs & Broadloom': 'Home & Decor / Housewares / Art Manufacturers',
    'International Home Miami': 'Furniture',
    'Maxim Lighting International': 'Lighting',
    'EGLO Canada': 'Lighting',
    'Arabela Lighting': 'Lighting',
    'Visual Comfort Europe': 'Lighting',
    'Lucas McKearn': 'Lighting',
    'Sixtrees Limited': 'Home & Decor / Housewares / Art Manufacturers',
    'Butler Specialty Company': 'Furniture',
    'Sabine Pools, Spas, & Furnitur': 'Furniture',
    'Yutzy Woodworking': 'Furniture',
}

TARGET_ENTITIES = [
    'Kuzco Lighting Inc.',
    'Maxim Lighting International',
    'Currey & Company',
    'Wildwood/Chelsea House',
    'Sarreid, Ltd.',
]

# ── Data Parsing ───────────────────────────────────────────────────────────

def parse_number(val):
    """Parse a number from CSV, handling $, commas, empty strings."""
    if not val or val.strip() == '' or val.strip() == '#ERROR!':
        return 0.0
    val = val.replace('$', '').replace(',', '').strip()
    try:
        return float(val)
    except ValueError:
        return 0.0

def parse_bool(val):
    return val.strip().upper() == 'TRUE' if val else False

def safe_log(x):
    return math.log(x + 1)

def load_entities(csv_path):
    """Load and parse entity data from CSV."""
    entities = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        next(reader)  # skip blank row 0
        headers = [h.strip() for h in next(reader)]
        for row_vals in reader:
            row = dict(zip(headers, row_vals))
            name = row.get('entity_name', '').strip()
            if not name:
                continue

            mrr = parse_number(row.get('mrr', ''))
            products = parse_number(row.get('total_products', ''))
            customers = parse_number(row.get('total_customers', ''))
            orders = parse_number(row.get('orders', ''))
            users = parse_number(row.get('billable_users', ''))
            stack = row.get('stack', '').strip()
            cohort = parse_number(row.get('cohort_year', ''))

            has_catalog = parse_bool(row.get('has_catalog', ''))
            has_cart = parse_bool(row.get('has_cart', ''))
            has_portal = parse_bool(row.get('has_portal', ''))
            has_cpq = parse_bool(row.get('has_cpq', ''))
            has_closed = parse_bool(row.get('has_closed_site', ''))

            segment = SEGMENT_MAP.get(name, 'UNKNOWN')

            entity = {
                'name': name,
                'entity_type': row.get('entity_type', '').strip(),
                'segment': segment,
                'raw': {
                    'mrr': mrr,
                    'total_products': products,
                    'total_customers': customers,
                    'orders': orders,
                    'billable_users': users,
                    'stack': stack,
                    'cohort_year': int(cohort) if cohort else 2025,
                    'has_catalog': has_catalog,
                    'has_cart': has_cart,
                    'has_portal': has_portal,
                    'has_cpq': has_cpq,
                    'has_closed_site': has_closed,
                },
                'features': {
                    'log_mrr': safe_log(mrr),
                    'log_products': safe_log(products),
                    'log_customers': safe_log(customers),
                    'log_orders': safe_log(orders),
                    'log_users': safe_log(users),
                    'stack_ordinal': STACK_ORDINAL.get(stack, 1),
                    'feature_surface': sum([has_catalog, has_cart, has_portal, has_cpq, has_closed]),
                    'tenure_years': 2026 - (int(cohort) if cohort else 2025),
                },
            }
            entities.append(entity)
    return entities


# ── Normalization ──────────────────────────────────────────────────────────

def compute_segment_stats(entities):
    """Compute mean and std for each feature within each segment."""
    segment_groups = defaultdict(list)
    for e in entities:
        segment_groups[e['segment']].append(e)

    stats = {}
    for seg, group in segment_groups.items():
        stats[seg] = {}
        for feat in WEIGHTS:
            vals = [e['features'][feat] for e in group]
            mean = sum(vals) / len(vals)
            variance = sum((v - mean) ** 2 for v in vals) / len(vals)
            std = math.sqrt(variance) if variance > 0 else 1.0
            stats[seg][feat] = {'mean': mean, 'std': std}
    return stats, segment_groups

def normalize_features(entity, stats):
    """Z-score normalize an entity's features using segment stats."""
    seg = entity['segment']
    normalized = {}
    for feat in WEIGHTS:
        mean = stats[seg][feat]['mean']
        std = stats[seg][feat]['std']
        normalized[feat] = (entity['features'][feat] - mean) / std
    return normalized


# ── Distance Computation ──────────────────────────────────────────────────

def weighted_distance(norm_a, norm_b):
    """Compute weighted Euclidean distance between two normalized feature vectors."""
    dist_sq = 0.0
    contributions = {}
    for feat, weight in WEIGHTS.items():
        diff = norm_a[feat] - norm_b[feat]
        contrib = weight * (diff ** 2)
        dist_sq += contrib
        contributions[feat] = math.sqrt(contrib)
    return math.sqrt(dist_sq), contributions

def compute_all_distances(target, candidates, stats):
    """Compute distances from target to all candidates."""
    norm_target = normalize_features(target, stats)
    results = []
    for cand in candidates:
        if cand['name'] == target['name']:
            continue
        norm_cand = normalize_features(cand, stats)
        dist, contribs = weighted_distance(norm_target, norm_cand)
        results.append({
            'name': cand['name'],
            'distance': dist,
            'contributions': contribs,
            'raw': cand['raw'],
            'segment': cand['segment'],
        })
    results.sort(key=lambda x: x['distance'])
    return results


# ── Threshold Methods ─────────────────────────────────────────────────────

def method_absolute(ranked, threshold=0.75):
    """Include all peers with distance < threshold, floor of 3."""
    peers = [r for r in ranked if r['distance'] < threshold]
    if len(peers) < 3:
        peers = ranked[:3]
    return peers

def method_relative(ranked, multiplier=2.0):
    """Include all peers within multiplier × closest peer distance, floor of 3."""
    if not ranked:
        return []
    closest = ranked[0]['distance']
    if closest == 0:
        cutoff = 0.5
    else:
        cutoff = closest * multiplier
    peers = [r for r in ranked if r['distance'] <= cutoff]
    if len(peers) < 3:
        peers = ranked[:3]
    return peers

def method_elbow(ranked, gap_ratio=0.50):
    """Include peers up to the first large gap in distances, floor of 3."""
    if len(ranked) <= 3:
        return ranked

    peers = [ranked[0]]
    for i in range(1, len(ranked)):
        prev_dist = ranked[i - 1]['distance']
        curr_dist = ranked[i]['distance']
        if prev_dist > 0:
            gap = (curr_dist - prev_dist) / prev_dist
        else:
            gap = curr_dist
        if gap > gap_ratio and len(peers) >= 3:
            break
        peers.append(ranked[i])
    if len(peers) < 3:
        peers = ranked[:3]
    return peers


# ── Output Formatting ─────────────────────────────────────────────────────

def format_raw_value(key, val):
    if key == 'mrr':
        return f'${val:,.0f}'
    if key in ('total_products', 'total_customers', 'orders'):
        return f'{val:,.0f}'
    if key == 'billable_users':
        return f'{int(val)}'
    if key == 'cohort_year':
        return str(int(val))
    if key == 'stack':
        return val
    return str(val)

def top_contributors(contributions, n=3):
    """Return the top n features driving the distance."""
    feat_labels = {
        'log_mrr': 'Revenue',
        'log_products': 'Catalog size',
        'log_customers': 'Customer base',
        'stack_ordinal': 'Platform stack',
        'log_orders': 'Order volume',
        'log_users': 'Org size',
        'feature_surface': 'Feature surface',
        'tenure_years': 'Tenure',
    }
    sorted_contribs = sorted(contributions.items(), key=lambda x: x[1])
    closest = sorted_contribs[:n]
    return [feat_labels.get(c[0], c[0]) for c in closest]

def print_entity_profile(entity):
    r = entity['raw']
    print(f"  Segment: {entity['segment']}")
    print(f"  MRR: ${r['mrr']:,.0f}  |  Products: {r['total_products']:,.0f}  |  Customers: {r['total_customers']:,.0f}")
    print(f"  Orders: {r['orders']:,.0f}  |  Users: {int(r['billable_users'])}  |  Stack: {r['stack']}")
    print(f"  Features: catalog={r['has_catalog']} cart={r['has_cart']} portal={r['has_portal']} cpq={r['has_cpq']} closed={r['has_closed_site']}")
    print(f"  Cohort: {int(r['cohort_year'])}")

def print_peer_list(peers, target_raw):
    for i, p in enumerate(peers, 1):
        r = p['raw']
        closest_feats = top_contributors(p['contributions'])
        match_str = ', '.join(closest_feats)
        print(f"  {i:2d}. {p['name']:<45s}  dist={p['distance']:.3f}")
        print(f"      MRR: ${r['mrr']:,.0f}  |  Products: {r['total_products']:,.0f}  |  Customers: {r['total_customers']:,.0f}  |  Stack: {r['stack']}")
        print(f"      Most similar on: {match_str}")


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    csv_path = '/Users/kylorjohnson/Downloads/Copy of  Pricing Refresh Master Data V2 - v2 Master Entity.csv'
    entities = load_entities(csv_path)
    print(f"Loaded {len(entities)} entities")

    stats, segment_groups = compute_segment_stats(entities)

    print("\n" + "=" * 80)
    print("SEGMENT SUMMARY")
    print("=" * 80)
    for seg in sorted(segment_groups.keys()):
        print(f"  {seg}: {len(segment_groups[seg])} entities")

    for target_name in TARGET_ENTITIES:
        target = next((e for e in entities if e['name'] == target_name), None)
        if not target:
            print(f"\n*** TARGET NOT FOUND: {target_name} ***")
            continue

        seg = target['segment']
        candidates = segment_groups.get(seg, [])

        ranked = compute_all_distances(target, candidates, stats)

        print("\n" + "=" * 80)
        print(f"TARGET: {target_name}")
        print("=" * 80)
        print_entity_profile({'segment': seg, 'raw': target['raw']})

        print(f"\n  Segment pool: {len(candidates)} entities (including self)")
        print(f"  Distance range: {ranked[0]['distance']:.3f} — {ranked[-1]['distance']:.3f}")

        # Method 1: Absolute threshold
        abs_peers = method_absolute(ranked, threshold=0.75)
        print(f"\n  ─── METHOD 1: ABSOLUTE THRESHOLD (distance < 0.75) ─── [{len(abs_peers)} peers]")
        print_peer_list(abs_peers, target['raw'])

        # Method 2: Relative threshold
        rel_peers = method_relative(ranked, multiplier=2.0)
        print(f"\n  ─── METHOD 2: RELATIVE THRESHOLD (< 2× closest) ─── [{len(rel_peers)} peers]")
        print_peer_list(rel_peers, target['raw'])

        # Method 3: Elbow method
        elb_peers = method_elbow(ranked, gap_ratio=0.50)
        print(f"\n  ─── METHOD 3: ELBOW METHOD (50% gap cutoff) ─── [{len(elb_peers)} peers]")
        print_peer_list(elb_peers, target['raw'])

        # Comparison summary
        abs_names = set(p['name'] for p in abs_peers)
        rel_names = set(p['name'] for p in rel_peers)
        elb_names = set(p['name'] for p in elb_peers)
        all_three = abs_names & rel_names & elb_names
        any_method = abs_names | rel_names | elb_names

        print(f"\n  ─── OVERLAP SUMMARY ───")
        print(f"  In all 3 methods: {len(all_three)} — {', '.join(sorted(all_three)) if all_three else 'none'}")
        print(f"  Total unique across methods: {len(any_method)}")

        # Full ranked list for reference
        print(f"\n  ─── FULL RANKED LIST (all {len(ranked)} in segment) ───")
        for i, r in enumerate(ranked, 1):
            marker = ''
            if r['name'] in all_three:
                marker = ' *** [all 3]'
            elif r['name'] in any_method:
                methods = []
                if r['name'] in abs_names: methods.append('abs')
                if r['name'] in rel_names: methods.append('rel')
                if r['name'] in elb_names: methods.append('elbow')
                marker = f"  [{'+'.join(methods)}]"
            print(f"  {i:2d}. {r['name']:<45s}  dist={r['distance']:.3f}{marker}")

if __name__ == '__main__':
    main()
