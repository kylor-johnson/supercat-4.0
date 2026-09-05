"""
Lookalike Model v2 — Validated against Postgres source data
Uses Postgres for products/customers/orders/users (source of truth)
Uses CSV for MRR/stack/config (billing data, unaffected by order errors)
Runs for ALL 86 parent entities using relative threshold (2x closest)
"""

import csv
import math
import json
import sys
from collections import defaultdict

# ── Postgres-validated data (pulled 2026-03-24 via MCP) ──────────────────
# Format: shortname -> {product_count, customer_count, order_count, user_count, created_year}
# Orders filtered: is_submitted=true, total < $10M (excludes data entry errors)

POSTGRES_DATA = {
    'asi': {'products': 9658, 'customers': 1663, 'orders': 76471, 'users': 292, 'year': 2011},
    'mpc': {'products': 4927, 'customers': 1745, 'orders': 72693, 'users': 249, 'year': 2015},
    'gsa': {'products': 5844, 'customers': 2043, 'orders': 4657, 'users': 53, 'year': 2011},
    'pw': {'products': 1262, 'customers': 108, 'orders': 461, 'users': 50, 'year': 2012},
    'rac': {'products': 694, 'customers': 552, 'orders': 6352, 'users': 52, 'year': 2011},
    'ssi': {'products': 300, 'customers': 417, 'orders': 567, 'users': 51, 'year': 2011},
    'tla': {'products': 30119, 'customers': 4418, 'orders': 2582, 'users': 210, 'year': 2017},
    'fms': {'products': 12011, 'customers': 5299, 'orders': 16909, 'users': 221, 'year': 2016},
    'vcg': {'products': 38574, 'customers': 5170, 'orders': 9479, 'users': 177, 'year': 2019},
    'big': {'products': 2896, 'customers': 301, 'orders': 126, 'users': 105, 'year': 2018},
    'hmjc': {'products': 3723, 'customers': 1689, 'orders': 2, 'users': 158, 'year': 2018},
    'kkc': {'products': 761, 'customers': 368, 'orders': 41, 'users': 88, 'year': 2015},
    'ih': {'products': 4589, 'customers': 19797, 'orders': 12767, 'users': 58, 'year': 2021},
    'ihw': {'products': 3905, 'customers': 6041, 'orders': 12833, 'users': 64, 'year': 2016},
    'kl': {'products': 5598, 'customers': 3011, 'orders': 852, 'users': 128, 'year': 2012},
    'prog': {'products': 4252, 'customers': 12422, 'orders': 73, 'users': 109, 'year': 2025},
    'ta': {'products': 27285, 'customers': 7130, 'orders': 8371, 'users': 515, 'year': 2016},
    'tam': {'products': 26153, 'customers': 178, 'orders': 230, 'users': 33, 'year': 2025},
    'jcusa': {'products': 16406, 'customers': 4809, 'orders': 2170, 'users': 2555, 'year': 2018},
    'jc': {'products': 26329, 'customers': 34, 'orders': 126, 'users': 59, 'year': 2013},
    'wac': {'products': 29305, 'customers': 9478, 'orders': 4583, 'users': 170, 'year': 2023},
    'sbl': {'products': 4371, 'customers': 1287, 'orders': 394, 'users': 142, 'year': 2023},
    'cf': {'products': 7691, 'customers': 3337, 'orders': 0, 'users': 117, 'year': 2011},
    'hh': {'products': 1723, 'customers': 1570, 'orders': 0, 'users': 86, 'year': 2014},
    'hvl': {'products': 5917, 'customers': 2289, 'orders': 849, 'users': 189, 'year': 2014},
    'tl': {'products': 2285, 'customers': 2272, 'orders': 547, 'users': 221, 'year': 2014},
    'wwjc': {'products': 4910, 'customers': 13699, 'orders': 41340, 'users': 20151, 'year': 2011},
    'clm': {'products': 2389, 'customers': 4675, 'orders': 1798, 'users': 761, 'year': 2013},
    'sbmh': {'products': 887, 'customers': 6441, 'orders': 29773, 'users': 3370, 'year': 2011},
    'rw': {'products': 2124, 'customers': 4881, 'orders': 7693, 'users': 102, 'year': 2024},
    'ril': {'products': 1672, 'customers': 4314, 'orders': 1451, 'users': 256, 'year': 2024},
    'bcf': {'products': 4875, 'customers': 1990, 'orders': 5866, 'users': 1375, 'year': 2022},
    'fsf': {'products': 4945, 'customers': 754, 'orders': 9002, 'users': 715, 'year': 2023},
    'jyc': {'products': 1155, 'customers': 9294, 'orders': 79795, 'users': 15789, 'year': 2014},
    'bri': {'products': 1105, 'customers': 3200, 'orders': 5064, 'users': 1286, 'year': 2023},
    'kal': {'products': 2593, 'customers': 2202, 'orders': 1327, 'users': 1638, 'year': 2019},
    'kll': {'products': 6271, 'customers': 2767, 'orders': 882, 'users': 901, 'year': 2022},
    'lpf': {'products': 6198, 'customers': 1925, 'orders': 11250, 'users': 2445, 'year': 2019},
    'gl': {'products': 3288, 'customers': 2340, 'orders': 460, 'users': 561, 'year': 2023},
    'fc': {'products': 5343, 'customers': 3578, 'orders': 30191, 'users': 9141, 'year': 2017},
    'vic': {'products': 1350, 'customers': 1491, 'orders': 281, 'users': 328, 'year': 2022},
    'eli': {'products': 10894, 'customers': 5712, 'orders': 21046, 'users': 1476, 'year': 2013},
    'cci': {'products': 6055, 'customers': 38550, 'orders': 12738, 'users': 105, 'year': 2021},
    'hfg': {'products': 1172, 'customers': 8886, 'orders': 8396, 'users': 201, 'year': 2022},
    'el': {'products': 11087, 'customers': 2006, 'orders': 1221, 'users': 329, 'year': 2020},
    'clli': {'products': 3512, 'customers': 5149, 'orders': 1320, 'users': 1685, 'year': 2019},
    'clc': {'products': 2017, 'customers': 3212, 'orders': 262, 'users': 1049, 'year': 2012},
    'shl': {'products': 4851, 'customers': 1318, 'orders': 6586, 'users': 2075, 'year': 2012},
    'dccl': {'products': 2686, 'customers': 354, 'orders': 441, 'users': 28, 'year': 2024},
    'ali': {'products': 1674, 'customers': 2348, 'orders': 129, 'users': 245, 'year': 2018},
    'cfg': {'products': 680, 'customers': 2529, 'orders': 6524, 'users': 1474, 'year': 2015},
    'ah': {'products': 3569, 'customers': 3715, 'orders': 9249, 'users': 1812, 'year': 2018},
    'gc': {'products': 6217, 'customers': 1501, 'orders': 3281, 'users': 327, 'year': 2023},
    'kii': {'products': 36451, 'customers': 3615, 'orders': 32073, 'users': 108, 'year': 2015},
    'mah': {'products': 3328, 'customers': 875, 'orders': 5303, 'users': 362, 'year': 2019},
    'ap': {'products': 1051, 'customers': 4752, 'orders': 1629, 'users': 1224, 'year': 2012},
    'sarreid': {'products': 6565, 'customers': 4682, 'orders': 13268, 'users': 142, 'year': 2010},
    'gblx': {'products': 699, 'customers': 1140, 'orders': 0, 'users': 59, 'year': 2025},
    'pf': {'products': 1921, 'customers': 17274, 'orders': 40744, 'users': 195, 'year': 2012},
    'ml': {'products': 3540, 'customers': 0, 'orders': 111, 'users': 136, 'year': 2020},
    'tel': {'products': 2253, 'customers': 287, 'orders': 14, 'users': 28, 'year': 2015},
    'mfc': {'products': 9687, 'customers': 94, 'orders': 51, 'users': 573, 'year': 2012},
    'ol': {'products': 846, 'customers': 13364, 'orders': 58, 'users': 26, 'year': 2025},
    'bp': {'products': 2633, 'customers': 6928, 'orders': 16, 'users': 96, 'year': 2024},
    'ufi': {'products': 2852, 'customers': 14401, 'orders': 36816, 'users': 128, 'year': 2011},
    'am': {'products': 611, 'customers': 92, 'orders': 107, 'users': 28, 'year': 2024},
    'hf': {'products': 3936, 'customers': 13185, 'orders': 341, 'users': 71, 'year': 2024},
    'gcl': {'products': 141, 'customers': 157, 'orders': 382, 'users': 41, 'year': 2024},
    'fal': {'products': 8041, 'customers': 6806, 'orders': 3067, 'users': 63, 'year': 2024},
    'mh': {'products': 12375, 'customers': 1508, 'orders': 1874, 'users': 104, 'year': 2023},
    'mlg': {'products': 4288, 'customers': 8453, 'orders': 160, 'users': 109, 'year': 2025},
    'wag': {'products': 52665, 'customers': 24053, 'orders': 3582, 'users': 104, 'year': 2025},
    'all': {'products': 720, 'customers': 669, 'orders': 92, 'users': 74, 'year': 2023},
    'mlc': {'products': 2411, 'customers': 1211, 'orders': 350, 'users': 65, 'year': 2023},
    'vl': {'products': 1487, 'customers': 1827, 'orders': 718, 'users': 103, 'year': 2019},
    'eglo': {'products': 2223, 'customers': 1304, 'orders': 270, 'users': 62, 'year': 2022},
    'df': {'products': 1496, 'customers': 778, 'orders': 26, 'users': 49, 'year': 2024},
    'da': {'products': 2612, 'customers': 1982, 'orders': 20708, 'users': 50, 'year': 2013},
    'rf': {'products': 1909, 'customers': 4751, 'orders': 1259, 'users': 63, 'year': 2021},
    'afx': {'products': 2832, 'customers': 3480, 'orders': 72, 'users': 75, 'year': 2023},
    'heb': {'products': 47968, 'customers': 1787, 'orders': 16231, 'users': 112, 'year': 2012},
    'uhc': {'products': 4979, 'customers': 6617, 'orders': 18314, 'users': 25, 'year': 2021},
    'soi': {'products': 1246, 'customers': 0, 'orders': 0, 'users': 13, 'year': 2024},
    'abol': {'products': 1140, 'customers': 605, 'orders': 0, 'users': 30, 'year': 2024},
    'dals': {'products': 1150, 'customers': 630, 'orders': 55, 'users': 65, 'year': 2023},
    'sca': {'products': 4865, 'customers': 2782, 'orders': 2918, 'users': 44, 'year': 2015},
    'lss': {'products': 566, 'customers': 49, 'orders': 59, 'users': 29, 'year': 2023},
    'swc': {'products': 1581, 'customers': 0, 'orders': 5, 'users': 37, 'year': 2013},
    'etl': {'products': 6252, 'customers': 595, 'orders': 5336, 'users': 26, 'year': 2019},
    'krb': {'products': 5829, 'customers': 2208, 'orders': 2, 'users': 39, 'year': 2024},
    'ihm': {'products': 261, 'customers': 121, 'orders': 18, 'users': 56, 'year': 2024},
    'mli': {'products': 11853, 'customers': 9248, 'orders': 196, 'users': 95, 'year': 2019},
    'eglo_can': {'products': 2133, 'customers': 777, 'orders': 146, 'users': 28, 'year': 2024},
    'arl': {'products': 246, 'customers': 33, 'orders': 198, 'users': 71, 'year': 2025},
    'vce': {'products': 16908, 'customers': 1681, 'orders': 116, 'users': 39, 'year': 2022},
    'luc': {'products': 714, 'customers': 877, 'orders': 4, 'users': 29, 'year': 2025},
    'st': {'products': 18713, 'customers': 787, 'orders': 429, 'users': 26, 'year': 2015},
    'bsc': {'products': 2040, 'customers': 8314, 'orders': 8598, 'users': 29, 'year': 2011},
    'sp': {'products': 12046, 'customers': 0, 'orders': 1710, 'users': 20, 'year': 2018},
    'yw': {'products': 4247, 'customers': 231, 'orders': 156, 'users': 35, 'year': 2024},
    'sc': {'products': 27410, 'customers': 91340, 'orders': 325049, 'users': 158, 'year': 2014},
    'gh': {'products': 8098, 'customers': 11840, 'orders': 170466, 'users': 7888, 'year': 2013},
    'scw': {'products': 8679, 'customers': 8311, 'orders': 114421, 'users': 4459, 'year': 2015},
    'sccon': {'products': 13437, 'customers': 5257, 'orders': 63217, 'users': 1163, 'year': 2015},
    'gg': {'products': 7774, 'customers': 2043, 'orders': 14390, 'users': 54, 'year': 2013},
}

# ── CSV entity to Postgres shortname mapping ─────────────────────────────
# For rollups: maps to list of child shortnames to aggregate
# For standalones: maps to single shortname

ENTITY_TO_SHORTNAMES = {
    'Gabriella White': ['sc', 'gh', 'scw', 'sccon'],
    'Godinger Silver Art Co.': ['gsa', 'pw', 'rac', 'ssi'],
    'Generation Brands': ['tla', 'fms', 'vcg'],
    'Interlude Home': ['ih', 'ihw'],
    'Abaline': ['asi', 'mpc'],
    'Coleto Brands': ['kl', 'prog'],
    'WAC': ['wac', 'sbl'],
    'Century Furniture': ['cf', 'hh'],
    'HVLG': ['hvl', 'tl'],
    'Jonathan Charles': ['jcusa', 'jc'],
    'Wildwood/Chelsea House': ['wwjc'],
    'Crystorama': ['clm'],
    'Somerset Bay and Modern History': ['sbmh'],
    'RENWIL': ['rw'],
    'Ratana International Ltd.': ['ril'],
    'Braxton Culler': ['bcf'],
    'Four Seasons Furniture': ['fsf'],
    'Jamie Young Company': ['jyc'],
    'Bulbrite': ['bri'],
    'Kalco Lighting / Allegri Crystal': ['kal'],
    'Kuzco Lighting Inc.': ['kll'],
    'Linon/Powell Furniture': ['lpf'],
    'Golden Lighting': ['gl'],
    'Furniture Classics': ['fc'],
    'Vaxcel International Corporation': ['vic'],
    'Elegant Furniture & Lighting': ['eli'],
    'Currey & Company': ['cci'],
    'Hubbardton Forge': ['hfg'],
    'Eurofase Inc.': ['el'],
    'Litex Industries': ['clli'],
    'Capital Lighting Fixture Co.': ['clc'],
    'Savoy House Lighting': ['shl'],
    'Donald Choi Canada': ['dccl'],
    'Access Lighting': ['ali'],
    'Charleston Forge': ['cfg'],
    'Alfresco Home': ['ah'],
    'Groupe Courchesne': ['gc'],
    'Kennedy International, Inc.': ['kii'],
    'Moda at Home Enterprises Ltd': ['mah'],
    'Alden Home': ['ap'],
    'Sarreid, Ltd.': ['sarreid'],
    'Globalux': ['gblx'],
    'Palecek': ['pf'],
    'Millennium Lighting': ['ml'],
    'Tomlinson Companies': ['tel'],
    'Morgan Fabrics Corporation': ['mfc'],
    'Oly Studio': ['ol'],
    'Buster & Punch': ['bp'],
    'Universal Furniture': ['ufi'],
    'Alfonso Marina': ['am'],
    'Hooker Furnishings': ['hf'],
    'Geo Contemporary': ['gcl'],
    'Fine Art Handcrafted Lighting': ['fal'],
    'Magnussen Home': ['mh'],
    'Minka Lighting Group': ['mlg'],
    'Wendover Art Group': ['wag'],
    'Accord Lighting': ['all'],
    'Matteo Lighting': ['mlc'],
    'Ciana Varaluz LLC': ['vl'],
    'Eglo USA Inc.': ['eglo'],
    "Designer's Fountain": ['df'],
    'Dainolite Ltd.': ['da'],
    'Rowe Furniture': ['rf'],
    'AFX, Inc.': ['afx'],
    'Home Essentials & Beyond': ['heb'],
    'Uniware Housewares Corp.': ['uhc'],
    'Silver One': ['soi'],
    "America's Backyards": ['abol'],
    'DALS Lighting': ['dals'],
    'Shadow Catchers': ['sca'],
    'Lifestyle Solutions': ['lss'],
    'Sauder Woodworking': ['swc'],
    'ELICO LTD.': ['etl'],
    'Kaleen Rugs & Broadloom': ['krb'],
    'International Home Miami': ['ihm'],
    'Maxim Lighting International': ['mli'],
    'EGLO Canada': ['eglo_can'],
    'Arabela Lighting': ['arl'],
    'Visual Comfort Europe': ['vce'],
    'Lucas McKearn': ['luc'],
    'Sixtrees Limited': ['st'],
    'Butler Specialty Company': ['bsc'],
    'Sabine Pools, Spas, & Furnitur': ['sp'],
    'Yutzy Woodworking': ['yw'],
    'Theodore\u00ac\u00a8\u201a\u00c4\u2020Alexander': ['ta', 'tam'],
    'Baker\u00ac\u00a8\u201a\u00c4\u2020Interiors Group': ['big', 'hmjc', 'kkc'],
}

def aggregate_postgres(shortnames):
    """Sum Postgres metrics across child orgs."""
    total = {'products': 0, 'customers': 0, 'orders': 0, 'users': 0, 'year': 2025}
    earliest_year = 2030
    for sn in shortnames:
        d = POSTGRES_DATA.get(sn, {})
        total['products'] += d.get('products', 0)
        total['customers'] += d.get('customers', 0)
        total['orders'] += d.get('orders', 0)
        total['users'] += d.get('users', 0)
        yr = d.get('year', 2025)
        if yr < earliest_year:
            earliest_year = yr
    total['year'] = earliest_year
    return total


# ── Same config as v1 ────────────────────────────────────────────────────

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


def parse_number(val):
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
    entities = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        next(reader)
        headers = [h.strip() for h in next(reader)]
        for row_vals in reader:
            row = dict(zip(headers, row_vals))
            name = row.get('entity_name', '').strip()
            if not name:
                continue

            mrr = parse_number(row.get('mrr', ''))
            stack = row.get('stack', '').strip()
            has_catalog = parse_bool(row.get('has_catalog', ''))
            has_cart = parse_bool(row.get('has_cart', ''))
            has_portal = parse_bool(row.get('has_portal', ''))
            has_cpq = parse_bool(row.get('has_cpq', ''))
            has_closed = parse_bool(row.get('has_closed_site', ''))

            segment = SEGMENT_MAP.get(name, 'UNKNOWN')

            shortnames = ENTITY_TO_SHORTNAMES.get(name, [])
            if shortnames:
                pg = aggregate_postgres(shortnames)
            else:
                pg = {'products': 0, 'customers': 0, 'orders': 0, 'users': 0, 'year': 2025}

            entity = {
                'name': name,
                'entity_type': row.get('entity_type', '').strip(),
                'segment': segment,
                'raw': {
                    'mrr': mrr,
                    'total_products': pg['products'],
                    'total_customers': pg['customers'],
                    'orders': pg['orders'],
                    'billable_users': pg['users'],
                    'stack': stack,
                    'cohort_year': pg['year'],
                    'has_catalog': has_catalog,
                    'has_cart': has_cart,
                    'has_portal': has_portal,
                    'has_cpq': has_cpq,
                    'has_closed_site': has_closed,
                },
                'features': {
                    'log_mrr': safe_log(mrr),
                    'log_products': safe_log(pg['products']),
                    'log_customers': safe_log(pg['customers']),
                    'log_orders': safe_log(pg['orders']),
                    'log_users': safe_log(pg['users']),
                    'stack_ordinal': STACK_ORDINAL.get(stack, 1),
                    'feature_surface': sum([has_catalog, has_cart, has_portal, has_cpq, has_closed]),
                    'tenure_years': 2026 - pg['year'],
                },
            }
            entities.append(entity)
    return entities


def compute_segment_stats(entities):
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
    seg = entity['segment']
    normalized = {}
    for feat in WEIGHTS:
        mean = stats[seg][feat]['mean']
        std = stats[seg][feat]['std']
        normalized[feat] = (entity['features'][feat] - mean) / std
    return normalized


def weighted_distance(norm_a, norm_b):
    dist_sq = 0.0
    contributions = {}
    for feat, weight in WEIGHTS.items():
        diff = norm_a[feat] - norm_b[feat]
        contrib = weight * (diff ** 2)
        dist_sq += contrib
        contributions[feat] = math.sqrt(contrib)
    return math.sqrt(dist_sq), contributions


def compute_all_distances(target, candidates, stats):
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


def method_relative(ranked, multiplier=2.0):
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


FEAT_LABELS = {
    'log_mrr': 'Revenue',
    'log_products': 'Catalog size',
    'log_customers': 'Customer base',
    'stack_ordinal': 'Platform stack',
    'log_orders': 'Order volume',
    'log_users': 'Org size',
    'feature_surface': 'Feature surface',
    'tenure_years': 'Tenure',
}

def top_match_reasons(contributions, n=3):
    sorted_contribs = sorted(contributions.items(), key=lambda x: x[1])
    return [FEAT_LABELS.get(c[0], c[0]) for c in sorted_contribs[:n]]


def main():
    csv_path = '/Users/kylorjohnson/Downloads/Copy of  Pricing Refresh Master Data V2 - v2 Master Entity.csv'
    entities = load_entities(csv_path)
    print(f"Loaded {len(entities)} entities\n")

    stats, segment_groups = compute_segment_stats(entities)

    print("=" * 90)
    print("SEGMENT SUMMARY")
    print("=" * 90)
    for seg in sorted(segment_groups.keys()):
        print(f"  {seg}: {len(segment_groups[seg])} entities")

    # Run for ALL entities
    all_results = {}
    for entity in entities:
        seg = entity['segment']
        candidates = segment_groups.get(seg, [])
        if len(candidates) < 2:
            continue
        ranked = compute_all_distances(entity, candidates, stats)
        peers = method_relative(ranked, multiplier=2.0)
        all_results[entity['name']] = {
            'entity': entity,
            'peers': peers,
            'ranked': ranked,
        }

    # Print results grouped by segment
    for seg in ['Lighting', 'Furniture', 'Home & Decor / Housewares / Art Manufacturers', 'Generic B2B Wholesale']:
        seg_entities = [e for e in entities if e['segment'] == seg]
        if not seg_entities:
            continue

        print(f"\n{'=' * 90}")
        print(f"SEGMENT: {seg} ({len(seg_entities)} entities)")
        print(f"{'=' * 90}")

        for entity in sorted(seg_entities, key=lambda x: x['name']):
            name = entity['name']
            result = all_results.get(name)
            if not result:
                continue
            r = entity['raw']
            peers = result['peers']

            print(f"\n{'─' * 90}")
            print(f"  {name}")
            print(f"  MRR: ${r['mrr']:,.0f}  |  Products: {r['total_products']:,}  |  Customers: {r['total_customers']:,}  |  Orders: {r['orders']:,}  |  Users: {r['billable_users']:,}  |  Stack: {r['stack']}  |  Cohort: {r['cohort_year']}")
            print(f"  PEERS ({len(peers)}):")
            for i, p in enumerate(peers, 1):
                pr = p['raw']
                reasons = ', '.join(top_match_reasons(p['contributions']))
                print(f"    {i:2d}. {p['name']:<42s} dist={p['distance']:.3f}  MRR=${pr['mrr']:,.0f}  Prod={pr['total_products']:,}  Cust={pr['total_customers']:,}  Ord={pr['orders']:,}  Stack={pr['stack']}")
                print(f"        Closest on: {reasons}")

    # Summary: data discrepancies found
    print(f"\n{'=' * 90}")
    print("DATA VALIDATION: OUTLIER ORDERS FOUND IN POSTGRES")
    print("=" * 90)
    outliers = [
        ('shl', 'Savoy House Lighting', 1, '$464,039,001.80'),
        ('bmc', 'Bassett Mirror', 7, '$116,292,506.00'),
        ('fms', 'Visual Comfort - Studio/Fans', 5, '$285,469,343.82'),
        ('mhc', "Moe's Home Collection", 9, '$737,291,094.00'),
        ('khl', 'Kenroy Home', 1, '$14,506,467.00'),
    ]
    for sn, name, count, max_val in outliers:
        print(f"  {sn:<10s} {name:<35s} {count} outlier orders (max: {max_val})")
    print(f"\n  These outliers were EXCLUDED from order counts (threshold: orders.total < $10M)")
    print(f"  All product/customer/user counts sourced from Postgres (not CSV)")


if __name__ == '__main__':
    main()
