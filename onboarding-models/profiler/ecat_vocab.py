"""eCat field vocabulary for source profiling.

Header names are sourced from preflight/limits_generated.py (generated from
supercat_server, SHA d4a0e7d408fba6917ac5e685cd21e54c5ecd801d) wherever that file
carries them, and from the ecat-core-files / ecat-customers-build skills for fields
that carry no length limit and therefore do not appear in LIMITS.

Do not transcribe lengths here. This module answers "is this header an eCat field
name", not "how long may it be" — limits_generated.py owns lengths.
"""

import re

# --- normalisation ---------------------------------------------------------

def norm(h):
    """Normalise a header for comparison: lowercase, strip all non-alphanumerics."""
    return re.sub(r'[^a-z0-9]', '', str(h).strip().lower())


# --- per-file vocabularies -------------------------------------------------
# 'key'         : the field that anchors the file
# 'distinctive' : fields that appear in this file and (mostly) not the others.
#                 Scoring uses these; shared fields like baseitemcode cannot
#                 discriminate products from inventory from stories.
# 'all'         : every recognised header for the file, for pre-mapped detection.

PRODUCTS = {
    'key': 'baseitemcode',
    'distinctive': {
        'longdesc', 'shortdesc', 'mediumdesc', 'imagefilename', 'dimensions',
        'materials', 'features', 'packedvolume', 'packquantity', 'minimumquantity',
        'tradenamecode', 'collectioncodes', 'categorycodes', 'collectioncode',
        'categorycode', 'newitem', 'netprice', 'promotionprice', 'hideable',
        'relateditems', 'discountpricelevelcode', 'upcvalue', 'upctype',
        'keywords', 'shipweight', 'producttype', 'suitegroup',
    },
}

CUSTOMERS = {
    'key': 'billtocode',
    'distinctive': {
        'billtocode', 'billtoname', 'billtoshortname', 'billtoaddress1',
        'billtoaddress2', 'billtoaddress3', 'billtocity', 'billtostate',
        'billtopostcode', 'billtocountry', 'defaultpricecode', 'territorycodes',
        'shiptocode', 'shiptoaddress1', 'shiptoaddress2', 'shiptoaddress3',
        'shiptocity', 'shiptostate', 'shiptopostcode', 'shiptocountry',
        'shiptoemail', 'shiptophone', 'shiptoterritorycodes', 'buyeremail',
        'buyerfirstname', 'buyerlastname', 'buyerphone', 'buyerfax',
        'carrier', 'terms', 'shipinstructions', 'distributioncenter',
        'distributionsource',
    },
}

INVENTORY = {
    'key': 'baseitemcode',
    'distinctive': {
        'qtyavailable', 'qtyonhand', 'qtyreserved', 'qtyintransit',
        'qtyonbackorder', 'qtyonporder', 'qtyoverseas', 'qtyinshowroom',
        'nextreceiptdate', 'nextreceiptqty',
    },
}

STORIES = {
    'key': 'baseitemcode',
    'distinctive': {'productstory'},
}

OPTIONS = {
    'key': 'code',
    'distinctive': {'optioncode', 'optionname', 'swatchfilename'},
}

OPTION_GROUPS = {
    'key': 'code',
    'distinctive': {'options', 'optiongroupcode'},
}

TARGETS = {
    'products.csv': PRODUCTS,
    'customers.csv': CUSTOMERS,
    'inventory.csv': INVENTORY,
    'stories.csv': STORIES,
    'options.csv': OPTIONS,
    'option_groups.csv': OPTION_GROUPS,
}

# Required headers, verbatim from limits_generated.REQUIRED_HEADERS.
REQUIRED_HEADERS = {
    'products.csv': ['baseitemcode'],
    'inventory.csv': ['baseitemcode'],
    'options.csv': ['code', 'name'],
    'option_groups.csv': ['code', 'name', 'options'],
    'customers.csv': [
        'billtoaddress1', 'billtocity', 'billtocode', 'billtoname',
        'billtopostcode', 'billtostate', 'defaultpricecode',
    ],
    'stories.csv': ['baseitemcode', 'productstory'],
}

# Patterned headers that are eCat fields but cannot be listed literally.
PATTERNED = [
    (re.compile(r'^price[a-z0-9]+$'), 'products.csv', 'Price_<code> price level'),
    (re.compile(r'^option(?:[1-9]|1[0-9]|20)$'), 'inventory.csv', 'Option1-20'),
    (re.compile(r'^optionset[0-9]+(?:required|matrixed)?$'), 'products.csv', 'OptionSet#'),
    (re.compile(r'^[a-z0-9]+qty(?:onhand|available|reserved|intransit)$'),
     'inventory.csv', 'per-division qty'),
]

ALL_ECAT = set()
for _t in TARGETS.values():
    ALL_ECAT |= _t['distinctive']
    ALL_ECAT.add(_t['key'])
ALL_ECAT |= {'baseitemcode', 'code', 'name', 'options', 'productstory'}


def patterned_match(h):
    """Return (target, label) if h matches a patterned eCat field, else None."""
    for rx, target, label in PATTERNED:
        if rx.match(h):
            return target, label
    return None


def is_ecat_header(h):
    return h in ALL_ECAT or patterned_match(h) is not None


# --- semantic fallback -----------------------------------------------------
# For raw ERP exports whose headers are not eCat names at all. These are weaker
# evidence and MUST be reported as such: they suggest a shape, they do not
# identify a target.

SEMANTIC = {
    'products.csv': [
        r'\bitem\b', r'\bsku\b', r'\bpart\s*(no|num|#)', r'\bmodel\b',
        r'\bdescription\b', r'\bprice\b', r'\bupc\b', r'\bweight\b',
        r'\bdimension', r'\bfinish\b', r'\bcolor\b', r'\bcategory\b',
        r'\bcollection\b', r'\bbrand\b', r'\bimage\b', r'\bcost\b',
    ],
    'customers.csv': [
        r'\bcustomer\b', r'\baccount\b', r'\bbill\s*to\b', r'\bship\s*to\b',
        r'\baddress\b', r'\bcity\b', r'\bstate\b', r'\bprovince\b',
        r'\bzip\b', r'\bpostal\b', r'\bterritory\b', r'\bsales\s*(rep|person)\b',
        r'\bphone\b', r'\bemail\b', r'\bterms\b',
    ],
    'inventory.csv': [
        r'\bqty\b', r'\bquantity\b', r'\bon\s*hand\b', r'\bavailable\b',
        r'\bstock\b', r'\bwarehouse\b', r'\bbackorder\b', r'\beta\b',
        r'\breceipt\b', r'\binventory\b',
    ],
}


def semantic_scores(raw_headers):
    """Keyword-family hits per target. Weak evidence; label it as such upstream."""
    joined = [str(h).strip().lower() for h in raw_headers]
    out = {}
    for target, pats in SEMANTIC.items():
        hits = set()
        for p in pats:
            for h in joined:
                if re.search(p, h):
                    hits.add(p)
                    break
        out[target] = len(hits)
    return out


# --- key semantics ---------------------------------------------------------
# Uniqueness is the WRONG test for a key once the target is known. customers.csv
# is bill-to rows plus ship-to continuation rows, so BillToCode is legitimately
# repeated: 842 rows over 421 distinct codes is the expected shape, not a broken
# key. Ask "does this match the key semantics of the eCat file it claims to be",
# not "is this column unique".

KEY_SEMANTICS = {
    'products.csv': {
        'col': 'baseitemcode', 'unique': True,
        'shape': 'one row per product; BaseItemCode unique',
    },
    'customers.csv': {
        'col': 'billtocode', 'unique': False,
        'shape': 'bill-to row plus one row per ship-to; BillToCode REPEATS by design',
    },
    'inventory.csv': {
        'col': 'baseitemcode', 'unique': None,   # unique unless Option1-20 in use
        'shape': 'one row per SKU, or one row per option combination if Option1-20 '
                 'are populated',
    },
    'stories.csv': {
        'col': 'baseitemcode', 'unique': True,
        'shape': 'one story per product; BaseItemCode unique',
    },
    'options.csv': {'col': 'code', 'unique': True, 'shape': 'one row per option code'},
    'option_groups.csv': {'col': 'code', 'unique': True,
                          'shape': 'one row per group code'},
}


def key_expectation(target, headers_norm):
    """Return (key_column_norm, expect_unique, prose) for a detected target."""
    spec = KEY_SEMANTICS.get(target)
    if not spec:
        return None, None, None
    unique = spec['unique']
    if target == 'inventory.csv':
        opts = [h for h in headers_norm if re.fullmatch(r'option(?:[1-9]|1[0-9]|20)', h)]
        unique = not opts
    return spec['col'], unique, spec['shape']
