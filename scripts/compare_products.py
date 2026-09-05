import csv

good = {}
with open('/Users/kylorjohnson/Downloads/products.csv.20260227-1924.csv', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        good[row['BaseItemCode']] = row

bad = {}
with open('/Users/kylorjohnson/Downloads/products.csv.20260310-2057.csv', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        bad[row['BaseItemCode']] = row

compare_cols = ['LongDesc', 'ImageFileName', 'Dimensions', 'ShortDesc', 'NetPrice',
                'UPC', 'CRI', 'Certifications', 'ColorTemperature_K', 'Dimmable',
                'InputVoltage', 'Wattage', 'BeamAngle_Deg', 'PackQuantity', 'MinimumQuantity',
                'TradeNameCode', 'CollectionCodes', 'CategoryCodes', 'NewItem',
                'LEDType', 'LifeSpan_Hours', 'LuminousFlux_Lm', 'MountingType',
                'PowerConsumption_W', 'Warranty_Years', 'RelatedItems', 'PackedVolume']

shared_codes = set(good.keys()) & set(bad.keys())
print(f'Shared BaseItemCodes: {len(shared_codes)}')
print()

diffs = {}
for code in shared_codes:
    for col in compare_cols:
        gval = good[code].get(col, '').strip()
        bval = bad[code].get(col, '').strip()
        if gval != bval:
            cleaned = bval.replace('\u00e2\u0080', '"').replace('\u00c2\u00b0', '\u00b0')
            cleaned = cleaned.replace('\xe2\x80\x9c', '"').replace('\xe2\x80\x9d', '"')
            cleaned = cleaned.replace('\u201c', '"').replace('\u201d', '"')
            cleaned = cleaned.replace('\u00e2\u20ac\u2122', "'")
            cleaned = cleaned.replace('\u00e2\u20ac\u201c', '-')
            # Also try simple ascii normalization
            import unicodedata
            if col not in diffs:
                diffs[col] = {'encoding_only': 0, 'real': []}
            # Check if difference is just encoding
            g_ascii = gval.encode('ascii', 'ignore').decode()
            b_ascii = bval.encode('ascii', 'ignore').decode()
            if g_ascii == b_ascii:
                diffs[col]['encoding_only'] += 1
            else:
                diffs[col]['real'].append((code, gval, bval))

print('=== Differences by column ===')
for col in compare_cols:
    if col in diffs:
        enc = diffs[col]['encoding_only']
        real = diffs[col]['real']
        if real:
            print(f'\n{col}: {len(real)} REAL differences, {enc} encoding-only')
            for code, gval, bval in real[:3]:
                print(f'  {code}:')
                print(f'    GOOD: {gval[:100]}')
                print(f'    BAD:  {bval[:100]}')
            if len(real) > 3:
                print(f'  ... and {len(real)-3} more')
        elif enc > 0:
            print(f'{col}: {enc} diffs, ALL encoding-only')
