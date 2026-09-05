import csv
from collections import OrderedDict

INPUT = '/Users/kylorjohnson/Downloads/products_clean_20260310.csv'
OUTPUT = '/Users/kylorjohnson/Downloads/products_deduped_20260310.csv'
REVIEW = '/Users/kylorjohnson/Downloads/products_conflicts_review.txt'

with open(INPUT, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    all_rows = []
    for row in reader:
        all_rows.append(row)

groups = OrderedDict()
for i, row in enumerate(all_rows):
    code = row['BaseItemCode']
    if code not in groups:
        groups[code] = []
    groups[code].append((i, row))

MERGE_FIELDS = {'CollectionCodes', 'CategoryCodes'}
IGNORE_DIFFS = {'CollectionCodes', 'CategoryCodes'}

output_rows = []
conflicts = []

for code, entries in groups.items():
    if len(entries) == 1:
        output_rows.append(entries[0][1])
        continue

    base_row = dict(entries[0][1])
    all_collections = []
    all_categories = []
    has_conflict = False
    conflict_details = []

    for idx, row in entries:
        for cc in row['CollectionCodes'].split(','):
            cc = cc.strip()
            if cc and cc not in all_collections:
                all_collections.append(cc)
        for cat in row['CategoryCodes'].split(','):
            cat = cat.strip()
            if cat and cat not in all_categories:
                all_categories.append(cat)

    for field in headers:
        if field in IGNORE_DIFFS:
            continue
        values = set()
        for idx, row in entries:
            val = row.get(field, '').strip()
            if val:
                values.add(val)
        if len(values) > 1:
            has_conflict = True
            conflict_details.append(field)

    base_row['CollectionCodes'] = ','.join(all_collections)

    # For CategoryCodes, merge but put non-UNCAT codes first
    non_uncat = [c for c in all_categories if c != 'UNCAT']
    uncat = [c for c in all_categories if c == 'UNCAT']
    merged_cats = non_uncat + uncat
    if merged_cats:
        base_row['CategoryCodes'] = ','.join(merged_cats)

    if has_conflict:
        detail_lines = [f'\n=== {code} ({len(entries)} rows) ===']
        detail_lines.append(f'  Conflicting fields: {", ".join(conflict_details)}')
        detail_lines.append(f'  Merged CollectionCodes: {base_row["CollectionCodes"]}')
        detail_lines.append(f'  Merged CategoryCodes: {base_row["CategoryCodes"]}')
        for field in conflict_details:
            detail_lines.append(f'  Field: {field}')
            for idx, row in entries:
                val = row.get(field, '').strip()
                coll = row.get('CollectionCodes', '')
                detail_lines.append(f'    Line {idx+2} (Coll={coll}): {val[:100]}')

        # Use the LAST occurrence as the "winner" (matches importer behavior)
        # but override with the merged collections/categories
        final_row = dict(entries[-1][1])
        final_row['CollectionCodes'] = base_row['CollectionCodes']
        final_row['CategoryCodes'] = base_row['CategoryCodes']
        output_rows.append(final_row)
        conflicts.append('\n'.join(detail_lines))
    else:
        output_rows.append(base_row)

with open(OUTPUT, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(output_rows)

print(f'Input:  {len(all_rows)} rows, {len(groups)} unique BaseItemCodes')
print(f'Output: {len(output_rows)} rows (all unique)')
print(f'Removed: {len(all_rows) - len(output_rows)} duplicate rows')
print()

if conflicts:
    with open(REVIEW, 'w') as f:
        f.write('PRODUCTS WITH DATA CONFLICTS (merged but review recommended)\n')
        f.write('=' * 70 + '\n')
        f.write('These items had duplicate BaseItemCodes with DIFFERENT data in some fields.\n')
        f.write('The LAST occurrence was kept (matches eCat importer behavior).\n')
        f.write('CollectionCodes and CategoryCodes were merged from all occurrences.\n')
        f.write('=' * 70 + '\n')
        f.write('\n'.join(conflicts))
    print(f'Conflicts: {len(conflicts)} items have data differences - see review file')
    print(f'Review file: {REVIEW}')
else:
    print('No data conflicts found - all duplicates were collection-only differences.')
