#!/usr/bin/env python3
"""B1 - registered custom fields must be populated. BUILD_SPEC §3.2.

    A field registered with `send_to_ipad` and used as a filter, carrying zero
    values, is worse than absent - it ships an empty filter chip.

## Two checks, because the incident is the INVERSE of the criterion

B1 as written is post-import: a field is registered, and no product has a value.

leg's 2026-07-23 incident is the other direction. Thirteen columns
(`rohscompliant`, `Color`, `voltage`, `wattage`, `switchtype`, `workswith`,
`wiresize`, `mountingtype`, `prop65`, `warranty`, `numberofswitches`,
`bulbcompatibility`, `numberofgangs`) were in `products.csv` and **never
registered in Admin**, so the importer warned `Custom field 'X' is missing` and
dropped them. leg has five registered custom fields; not one of them is
`numberofgangs`, and all five are well populated.

Same client-visible outcome - an announced field delivers nothing - but the
opposite mechanism and the opposite fix. So:

    B1a  registered, but no product carries a value      (post-import)
    B1b  in the file, but not registered - silently dropped   (pre-upload)

## The two storage shapes

Custom fields store two ways, and a check that looks at one reports false zeros
for the other:

    db_column_name   'ecat_custom_field_N' - a real column on products
                     (180 such columns exist)
    alias            a POINTER to an existing field, with no storage of its own
                     'i.qty_on_hand' -> inventories.qty_on_hand
                     'ic.ML_QtyOnHand' -> inventories.custom_fields JSONB key
                     'pl.murray' -> a price level
                     'item_number' -> products.item_number

`cl` uses both shapes in the same org. An alias field can never be "empty
because nothing populated it" in the way a db_column field can - it inherits
whatever its target holds - so the two are reported separately rather than
summed.

Read-only: emits SQL, never connects.
"""

import argparse
import csv
import io
import json
import os
import re
import sys

SHORTNAME_RE = re.compile(r'^[a-z0-9_-]{1,32}$')
COL_RE = re.compile(r'^ecat_custom_field_[0-9]{1,3}$')

# Alias prefixes and where they actually point.
ALIAS_TARGETS = [
    ('ic.', 'inventories.custom_fields', 'inventory custom field (JSONB key)'),
    ('i.',  'inventories',               'standard inventory column'),
    ('pl.', 'price_levels',              'price level'),
]


def sql_literal(s):
    return "'" + str(s).replace("'", "''") + "'"


def sql_registered(shortname):
    if not SHORTNAME_RE.match(shortname):
        raise SystemExit('unsafe shortname: %r' % shortname)
    return """
SELECT cf.id, cf.position, cf.field_name, cf.db_column_name, cf.alias, cf.label,
       cf.send_to_ipad, cf.use_as_filter, cf.field_type
FROM custom_fields cf
WHERE cf.organization_id = (SELECT id FROM organizations WHERE shortname = {sn})
ORDER BY cf.position
""".format(sn=sql_literal(shortname)).strip()


def classify(field):
    """Which storage shape, and what to count against."""
    col = (field.get('db_column_name') or '').strip()
    alias = (field.get('alias') or '').strip()
    if col:
        if not COL_RE.match(col):
            return 'unknown', None, 'unrecognised db_column_name %r' % col
        return 'column', col, 'products.%s' % col
    if alias:
        for prefix, target, human in ALIAS_TARGETS:
            if alias.startswith(prefix):
                return 'alias', alias, '%s (%s)' % (target, human)
        return 'alias', alias, 'products.%s (bare alias)' % alias
    return 'unknown', None, 'neither db_column_name nor alias is set'


def sql_population(shortname, fields):
    """One aggregate over products counting non-empty values per column field.

    Only `column` fields are counted here. An alias points at a field that
    something else populates, so "is the alias populated" is a question about
    its target, not about the custom field - counting them together would
    manufacture zeros.
    """
    cols = []
    for f in fields:
        kind, ref, _ = classify(f)
        if kind != 'column':
            continue
        cols.append((f, ref))
    if not cols:
        return None, 'no db_column_name-backed fields registered for this org'
    sel = ',\n  '.join(
        "count(*) FILTER (WHERE NOT COALESCE(deleted,false) "
        "AND btrim(COALESCE(%s,'')) <> '') AS %s" % (ref, ref)
        for _, ref in cols)
    return ("""
SELECT count(*) FILTER (WHERE NOT COALESCE(deleted,false)) AS live_products,
  {sel}
FROM products
WHERE organization_id = (SELECT id FROM organizations WHERE shortname = {sn})
""".format(sel=sel, sn=sql_literal(shortname)).strip()), None


def read_file_columns(path):
    """Return (headers, fill_counts, data_rows).

    B1b needs the FILL RATE, not just the header list. A column that is present
    and populated but unregistered has its data silently discarded on every
    import - that is blocking. A column that is present and EMPTY is 13 warnings
    per import and nothing else, and the fix is to stop emitting it, not to
    register it. Same check, opposite severity, and getting that backwards makes
    the gate cry wolf on a file that is fine.
    """
    with open(path, 'rb') as fh:
        raw = fh.read()
    for enc in ('utf-8-sig', 'utf-8', 'cp1252', 'latin-1'):
        try:
            txt = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise SystemExit('cannot decode %s' % path)
    rows = list(csv.reader(io.StringIO(txt)))
    if not rows:
        return [], {}, 0
    headers = [h.strip() for h in rows[0]]
    body = [r for r in rows[1:] if any(c.strip() for c in r)]
    fill = {}
    for i, h in enumerate(headers):
        fill[h] = sum(1 for r in body if i < len(r) and str(r[i]).strip())
    return headers, fill, len(body)


def read_file_headers(path):
    with open(path, 'rb') as fh:
        raw = fh.read()
    for enc in ('utf-8-sig', 'utf-8', 'cp1252', 'latin-1'):
        try:
            txt = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise SystemExit('cannot decode %s' % path)
    rows = list(csv.reader(io.StringIO(txt)))
    return [h.strip() for h in rows[0]] if rows else []


# Standard eCat product headers - anything here is NOT a custom field, so its
# absence from custom_fields is expected rather than a finding.
STANDARD = {
    'baseitemcode', 'longdesc', 'shortdesc', 'mediumdesc', 'imagefilename',
    'dimensions', 'shipweight', 'packedvolume', 'packquantity', 'minimumquantity',
    'tradenamecode', 'collectioncodes', 'categorycodes', 'collectioncode',
    'categorycode', 'newitem', 'netprice', 'promotionprice', 'promoprice',
    'hideable', 'relateditems', 'discountpricelevelcode', 'upcvalue', 'upctype',
    'materials', 'features', 'producttype', 'suitegroup', 'productstory',
}


def norm(h):
    return re.sub(r'[^a-z0-9]', '', str(h).strip().lower())


def check_b1b(headers, fields, fill=None, rows=0):
    """Unregistered file columns, split by whether they carry data.

    Returns (blocking, informational). The split is the point:

      populated + unregistered -> the values are discarded on every import
      empty     + unregistered -> warnings only; stop emitting the column
    """
    registered = set()
    for f in fields:
        for key in ('field_name', 'label', 'alias'):
            v = (f.get(key) or '').strip()
            if v:
                registered.add(norm(v))
    blocking, info = [], []
    for h in headers:
        n = norm(h)
        if not n or n in STANDARD or n in registered:
            continue
        if re.match(r'^price[a-z0-9]+$', n) or re.match(r'^optionset[0-9]+', n):
            continue
        filled = (fill or {}).get(h)
        entry = {'column': h, 'filled': filled, 'rows': rows}
        if filled is None:
            info.append(entry)          # fill unknown: do not assert severity
        elif filled > 0:
            blocking.append(entry)
        else:
            info.append(entry)
    return blocking, info


def check_b1a(fields, counts):
    """Registered column fields carrying no values."""
    live = counts.get('live_products')
    findings, reported = [], []
    for f in fields:
        kind, ref, where = classify(f)
        label = (f.get('label') or '').strip()
        internal = (f.get('field_name') or f.get('alias') or '').strip()
        name = label or internal or '?'
        if label and internal and label != internal:
            name = '%s (%s)' % (label, internal)
        if kind != 'column':
            reported.append({'field': name, 'shape': kind, 'where': where,
                             'populated': None,
                             'note': 'alias field - inherits its target; not counted '
                                     'as a B1a candidate'})
            continue
        n = counts.get(ref)
        reported.append({'field': name, 'shape': 'column', 'where': where,
                         'populated': n, 'live_products': live,
                         'send_to_ipad': f.get('send_to_ipad'),
                         'use_as_filter': f.get('use_as_filter')})
        if n is None:
            continue
        filterish = bool(f.get('use_as_filter'))
        if n == 0:
            findings.append({
                'severity': 'BLOCKING' if (f.get('send_to_ipad') and filterish)
                            else 'WARN',
                'field': name, 'where': where,
                'detail': 'registered%s%s and populated on 0 of %s live products. '
                          'An empty filter chip is worse than an absent one: it '
                          'returns nothing and looks broken.'
                          % (' with send_to_ipad' if f.get('send_to_ipad') else '',
                             ', used as a %s filter' % f['use_as_filter']
                             if filterish else ''),
            })
        elif live and n / float(live) < 0.05:
            findings.append({
                'severity': 'WARN', 'field': name, 'where': where,
                'detail': 'populated on %d of %s live products (%.1f%%) - too sparse '
                          'to be a useful filter.' % (n, live, 100.0 * n / live),
            })
    return findings, reported


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--org', required=True)
    ap.add_argument('--stage', choices=('registered', 'population'), default='registered')
    ap.add_argument('--fields', help='JSON rows from the registered query')
    ap.add_argument('--counts', help='JSON row from the population query')
    ap.add_argument('--file', help='products.csv to check for B1b')
    ap.add_argument('--emit-sql', action='store_true')
    args = ap.parse_args()

    if args.emit_sql and args.stage == 'registered':
        print(sql_registered(args.org))
        return 0

    if args.emit_sql and args.stage == 'population':
        if not args.fields:
            ap.error('--stage population needs --fields')
        with open(args.fields) as fh:
            fields = json.load(fh)
        sql, err = sql_population(args.org, fields)
        if err:
            print('-- %s' % err)
            return 2
        print(sql)
        return 0

    if not args.fields:
        ap.error('need --fields')
    with open(args.fields) as fh:
        fields = json.load(fh)
    counts = {}
    if args.counts:
        with open(args.counts) as fh:
            c = json.load(fh)
        counts = c[0] if isinstance(c, list) else c

    print('=' * 72)
    print('B1  REGISTERED CUSTOM FIELDS -- org %s' % args.org)
    print('=' * 72)
    shapes = {}
    for f in fields:
        shapes[classify(f)[0]] = shapes.get(classify(f)[0], 0) + 1
    print('%d registered field(s): %s' % (
        len(fields), ', '.join('%s %d' % kv for kv in sorted(shapes.items()))))

    rc = 0
    if counts:
        findings, reported = check_b1a(fields, counts)
        print('\n-- B1a  registered but unpopulated ' + '-' * 36)
        print('   %-34s %-34s %s' % ('field (as the rep sees it)', 'stored at', 'populated'))
        for r in reported:
            pop = ('%s / %s' % (r['populated'], r['live_products'])
                   if r.get('populated') is not None else '(alias - inherits target)')
            print('   %-34s %-34s %s' % (r['field'][:34], r['where'][:34], pop))
        if not findings:
            print('\n   no registered column field is empty or near-empty')
        for f in findings:
            print('\n   %-9s %s' % (f['severity'], f['field']))
            print('             %s' % f['detail'])
            if f['severity'] == 'BLOCKING':
                rc = 1
    else:
        print('\n-- B1a  SKIPPED: no --counts supplied')

    if args.file:
        headers, fill, nrows = read_file_columns(args.file)
        blocking, info = check_b1b(headers, fields, fill, nrows)
        print('\n-- B1b  in the file, not registered ' + '-' * 35)
        print('   %s: %d columns, %d data rows' % (
            os.path.basename(args.file), len(headers), nrows))
        if not blocking and not info:
            print('   every non-standard column is registered')
        if blocking:
            print('\n   BLOCKING - populated but not registered, so these values are')
            print('   DISCARDED on every import:')
            for e in blocking:
                print('     %-28s %d of %d rows populated (%.0f%%)'
                      % (e['column'][:28], e['filled'], e['rows'],
                         100.0 * e['filled'] / max(1, e['rows'])))
            print('   -> register these fields in Admin before the next import.')
            rc = 1
        if info:
            print('\n   INFO - present but EMPTY and not registered. These produce a')
            print('   "Custom field is missing" warning per import and nothing else:')
            for e in info:
                n = ('%d of %d rows' % (e['filled'], e['rows'])
                     if e['filled'] is not None else 'fill unknown')
                print('     %-28s %s' % (e['column'][:28], n))
            print('   -> the fix is to STOP EMITTING these columns from the'
                  ' generator,\n      not to register them. No data is being lost.')
    print()
    return rc


if __name__ == '__main__':
    sys.exit(main())
