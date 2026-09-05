import csv
import re

filepath = '/Users/kylorjohnson/Downloads/products_clean_20260310.csv'

with open(filepath, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    rows = list(reader)

print(f'Total rows: {len(rows)}')
print(f'Columns: {len(headers)}')
print()

issues = []

REQUIRED_FIELDS = [
    'BaseItemCode', 'LongDesc', 'ImageFileName', 'Dimensions',
    'PackedVolume', 'PackQuantity', 'MinimumQuantity',
    'TradeNameCode', 'CollectionCodes', 'CategoryCodes',
    'NewItem', 'NetPrice'
]

SPEC_FIELDS = {
    'BaseItemCode':    {'type': 'S', 'maxlen': 20},
    'LongDesc':        {'type': 'S', 'maxlen': 50},
    'MediumDesc':      {'type': 'S', 'maxlen': 25},
    'ShortDesc':       {'type': 'S', 'maxlen': 15},
    'Materials':       {'type': 'S', 'maxlen': 50},
    'Features':        {'type': 'S', 'maxlen': 50},
    'ImageFileName':   {'type': 'S', 'maxlen': 255},
    'Dimensions':      {'type': 'S', 'maxlen': 50},
    'ShipWeight':      {'type': 'F', 'maxlen': 8},
    'PackedVolume':    {'type': 'F', 'maxlen': 8},
    'PackQuantity':    {'type': 'I', 'maxlen': 5},
    'MinimumQuantity': {'type': 'I', 'maxlen': 5},
    'TradeNameCode':   {'type': 'S', 'maxlen': 5},
    'CollectionCodes': {'type': 'S', 'maxlen': 5},
    'CategoryCodes':   {'type': 'S', 'maxlen': 5},
    'NewItem':         {'type': 'B', 'maxlen': 1},
    'NetPrice':        {'type': 'M', 'maxlen': 8},
    'PromotionPrice':  {'type': 'M', 'maxlen': 8},
    'ProductType':     {'type': 'S', 'maxlen': 5},
    'RelatedItems':    {'type': 'S', 'maxlen': 255},
}

# 1. Check required fields present in headers
print('=== HEADER VALIDATION ===')
for field in REQUIRED_FIELDS:
    if field not in headers:
        print(f'  MISSING REQUIRED COLUMN: {field}')
        issues.append(f'Missing required column: {field}')
    else:
        print(f'  OK: {field}')

if 'PromotionPrice' not in headers:
    print(f'  NOTE: PromotionPrice not in file (spec says required, but may be optional in practice)')
print()

# 2. Identify standard vs custom fields
standard = [h for h in headers if h in SPEC_FIELDS or h.startswith('price_') or h.startswith('Price_') or h.startswith('OptionSet') or h.startswith('StartsAt')]
custom = [h for h in headers if h not in SPEC_FIELDS and not h.startswith('price_') and not h.startswith('Price_') and not h.startswith('OptionSet') and not h.startswith('StartsAt')]
print(f'=== FIELD CLASSIFICATION ===')
print(f'  Standard spec fields: {", ".join(standard)}')
print(f'  Custom fields: {", ".join(custom)}')
print()

# 3. Row-level validation
print('=== ROW VALIDATION ===')

empty_required = {f: 0 for f in REQUIRED_FIELDS}
longdesc_over50 = 0
shortdesc_over15 = 0
baseitemcode_invalid = 0
producttype_invalid = 0
netprice_invalid = 0
packqty_invalid = 0
minqty_invalid = 0
newitem_invalid = 0
image_over6 = 0
baseitemcode_over20 = 0
duplicate_codes = {}
tradename_over5 = 0

for i, row in enumerate(rows, start=2):
    code = row.get('BaseItemCode', '').strip()

    # Track duplicates
    if code in duplicate_codes:
        duplicate_codes[code].append(i)
    else:
        duplicate_codes[code] = [i]

    # Required field empty checks
    for f in REQUIRED_FIELDS:
        if not row.get(f, '').strip():
            empty_required[f] += 1

    # BaseItemCode: max 20, only numbers/text/dash/underscore
    if code and len(code) > 20:
        baseitemcode_over20 += 1
    if code and not re.match(r'^[A-Za-z0-9\-_/\.]+$', code):
        baseitemcode_invalid += 1

    # LongDesc max 50
    ld = row.get('LongDesc', '').strip()
    if len(ld) > 50:
        longdesc_over50 += 1

    # ShortDesc max 15
    sd = row.get('ShortDesc', '').strip()
    if sd and len(sd) > 15:
        shortdesc_over15 += 1

    # ProductType: must be 'suite', 'product', or empty
    pt = row.get('ProductType', '').strip().lower()
    if pt and pt not in ('suite', 'product'):
        producttype_invalid += 1

    # NetPrice: should be numeric
    np_val = row.get('NetPrice', '').strip()
    if np_val:
        try:
            float(np_val)
        except ValueError:
            netprice_invalid += 1

    # PackQuantity: integer > 0
    pq = row.get('PackQuantity', '').strip()
    if pq:
        try:
            if int(pq) < 1:
                packqty_invalid += 1
        except ValueError:
            packqty_invalid += 1

    # MinimumQuantity: integer > 0
    mq = row.get('MinimumQuantity', '').strip()
    if mq:
        try:
            if int(mq) < 1:
                minqty_invalid += 1
        except ValueError:
            minqty_invalid += 1

    # NewItem: boolean
    ni = row.get('NewItem', '').strip().upper()
    if ni and ni not in ('T', 'F', 'Y', 'N', '1', '0', 'TRUE', 'FALSE', 'YES', 'NO', ''):
        newitem_invalid += 1

    # ImageFileName: max 6 images
    img = row.get('ImageFileName', '').strip()
    if img:
        img_count = len([x for x in img.split(',') if x.strip()])
        if img_count > 6:
            image_over6 += 1

    # TradeNameCode max 5
    tn = row.get('TradeNameCode', '').strip()
    if tn and len(tn) > 5:
        tradename_over5 += 1

# Print results
for f in REQUIRED_FIELDS:
    if empty_required[f] > 0:
        severity = 'ERROR' if f != 'NetPrice' else 'WARNING'
        print(f'  {severity}: {f} empty in {empty_required[f]} rows')

if longdesc_over50 > 0:
    print(f'  WARNING: LongDesc exceeds 50 chars in {longdesc_over50} rows (will generate warning, not error)')
if shortdesc_over15 > 0:
    print(f'  WARNING: ShortDesc exceeds 15 chars in {shortdesc_over15} rows')
if baseitemcode_over20 > 0:
    print(f'  ERROR: BaseItemCode exceeds 20 chars in {baseitemcode_over20} rows')
if baseitemcode_invalid > 0:
    print(f'  WARNING: BaseItemCode has unusual chars in {baseitemcode_invalid} rows')
if producttype_invalid > 0:
    print(f'  ERROR: ProductType not suite/product/empty in {producttype_invalid} rows')
if netprice_invalid > 0:
    print(f'  ERROR: NetPrice not numeric in {netprice_invalid} rows')
if packqty_invalid > 0:
    print(f'  ERROR: PackQuantity not valid integer > 0 in {packqty_invalid} rows')
if minqty_invalid > 0:
    print(f'  ERROR: MinimumQuantity not valid integer > 0 in {minqty_invalid} rows')
if newitem_invalid > 0:
    print(f'  ERROR: NewItem not valid boolean in {newitem_invalid} rows')
if image_over6 > 0:
    print(f'  WARNING: ImageFileName has > 6 images in {image_over6} rows')
if tradename_over5 > 0:
    print(f'  WARNING: TradeNameCode exceeds 5 chars in {tradename_over5} rows')

dupes = {k: v for k, v in duplicate_codes.items() if len(v) > 1}
if dupes:
    print(f'  WARNING: {len(dupes)} duplicate BaseItemCodes found:')
    for code, lines in sorted(dupes.items()):
        print(f'    {code}: lines {lines}')
else:
    print(f'  OK: No duplicate BaseItemCodes')

# Check if all zero-issue
all_clear = (
    all(v == 0 for v in empty_required.values()) and
    producttype_invalid == 0 and netprice_invalid == 0 and
    packqty_invalid == 0 and minqty_invalid == 0 and
    newitem_invalid == 0 and baseitemcode_over20 == 0 and
    not dupes
)

print()
if all_clear:
    print('RESULT: File passes all critical import validations.')
else:
    print('RESULT: Issues found - review above.')

print()
print('=== PRICE LEVEL COLUMNS ===')
price_cols = [h for h in headers if h.lower().startswith('price_')]
for pc in price_cols:
    populated = sum(1 for r in rows if r.get(pc, '').strip())
    print(f'  {pc}: {populated}/{len(rows)} rows populated')
