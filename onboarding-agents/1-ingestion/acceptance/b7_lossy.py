#!/usr/bin/env python3
"""B7 - lossy regeneration gate. BUILD_SPEC §3.2, stage `pre_upload`.

Three questions sit in front of an upload, and until now only two were asked:

    A1  is this the right ORG?              (a1_fingerprint.py)
    B6  is this file DIFFERENT from the     (ecatlib.diff_against_previous,
        one that produced live state?        driven by mapping/preupload_check.py)
    B7  is this file POORER than the        <- this module
        live rows it will replace?

B6 only fires when a previous file exists. A26 is the case where one does not:

    `mali`'s customers.csv regenerated from the available export carries
    BillToAddress1 on 749 of 3,517 rows (21.3%). Live holds it on 3,418 of
    3,418 (100%). customers.csv HARD-DELETES and reloads, so importing that
    file blanks ~2,669 live addresses. The file parses, the import reads
    clean, and the deletes fire precisely BECAUSE it is clean.

## The hazard is column blanking, not row deletion

That is why this generalises past mali. A1 counts KEYS, so it only ever sees
rows appearing and disappearing; a file with every key present and half its
columns empty passes A1 at 100%. All eight eCat file types can be blanked this
way. Delete semantics change the SEVERITY (a hard-delete leaves nothing to
reverse) and feed recurrence changes the DURATION, but every type is exposed.

## Two stages, because density alone has a known blind spot

  Stage 1  DENSITY - per-column fill rate in the file vs live, same org.
           Catches the mali shape: a column the file has largely dropped.

  Stage 2  VALUE SPOT-CHECK - sample N keys present on both sides and compare
           values where BOTH are filled. Density cannot see mali's 1,428
           postcodes where both sides carry a value and the values DISAGREE:
           the fill rate is identical and the data is still wrong. A 50-row
           sample joined on the business key finds a 42% disagreement rate
           with near-certainty and needs no full join and no row alignment.

## Coverage - BUILD_SPEC §3.4

Every run reports `evaluated N of M columns`. A file column with no live
counterpart is NOT CHECKED and is named; it is never counted as a pass. A
column live holds on zero rows is NOT CHECKED too - there is nothing there to
lose - and it is also named, because a silent skip and a real negative are
indistinguishable unless the check says which it was.

There is deliberately NO prevalence floor. §3.4 instance 4 is a validator that
dropped `ShipWeight` for sitting at 41%. Low-prevalence columns are evaluated
and reported with their absolute row counts alongside the percentage.

## Read-only

Emits SQL; it does not connect. Run the emitted statements through the
supercat-postgres-vpn MCP and feed the rows back with --from-results. Same
pattern and same reason as a1_fingerprint.py: no Postgres credentials here.
"""

import argparse
import csv
import io
import json
import os
import random
import re
import sys

SHORTNAME_RE = re.compile(r'^[a-z0-9_-]{1,32}$')

# ---------------------------------------------------------------------------
# file column -> live column.
#
# `kind` decides what "filled" MEANS, and it is not cosmetic:
#   text   - non-empty after btrim
#   num    - NOT NULL. A qty of 0 is a real value; treating it as empty would
#            report a stocked-then-zeroed feed as a blanking event.
#   jsonish- non-empty AND not the literal empty-collection string. The
#            `territory_codes` empty value is '[]', not '' (SESSION_HANDOFF,
#            and the query that once reported "every customer has a territory"
#            when none did).
#   pair   - filled if EITHER sibling carries a value. products.images is empty
#            on all 915 libco rows while images_json holds the data.
# ---------------------------------------------------------------------------
#   taxo   - the live column stores an internal taxonomy CODE while the FILE
#            carries the taxonomy NAME. products.trade_name_code holds `TN2`;
#            products.csv holds `adorne`. Compared raw they disagree on 100%
#            of rows -- on a file byte-identical to the one that produced the
#            live state. Resolved through taxonomies(organization_id, code,
#            type) instead. Spelled `column@Type`.
TEXT, NUM, JSONISH, PAIR, TAXO = 'text', 'num', 'jsonish', 'pair', 'taxo'

# The importer AUTO-CREATES taxonomy from whatever string the file carries, and
# what it stores is a generated code with the file's string as the NAME. So the
# file and the column are two different vocabularies for the same fact, and a
# gate that compares them directly reports a defect on a correct file. That is
# worse than a missed finding: a check that cries wolf on every run is a check
# nobody reads. Verified live 2026-09-09 on org leg -- item ADSM703HW2 carries
# trade_name_code `TN2`, and taxonomies holds (code TN2, name `adorne`,
# type TradeName), which is exactly what the file says.
TAXONOMY_TYPES = {'trade_name_code': 'TradeName',
                  'collection_code': 'Collection',
                  'category_code': 'Category'}

CUSTOMERS_BILLTO = {
    'BillToName':         ('name', TEXT),
    'BillToAddress1':     ('billing_address1', TEXT),
    'BillToAddress2':     ('billing_address2', TEXT),
    'BillToAddress3':     ('billing_address3', TEXT),
    'BillToCity':         ('billing_city', TEXT),
    'BillToState':        ('billing_state', TEXT),
    'BillToPostCode':     ('billing_post_code', TEXT),
    'BillToCountry':      ('billing_country', TEXT),
    'BuyerFirstName':     ('buyer_first_name', TEXT),
    'BuyerLastName':      ('buyer_last_name', TEXT),
    'BuyerEmail':         ('buyer_email', TEXT),
    'BuyerPhone':         ('buyer_phone', TEXT),
    'BuyerFax':           ('buyer_fax', TEXT),
    'Terms':              ('terms', TEXT),
    'DefaultPriceCode':   ('default_price_code', TEXT),
    'DistributionSource': ('distribution_source', TEXT),
    'TerritoryCodes':     ('territory_codes', JSONISH),
    'TradeNameCodes':     ('trade_name_codes', JSONISH),
}

CUSTOMERS_SHIPTO = {
    'ShipToCode':       ('code', TEXT),
    'ShipToName':       ('ship_to_name', TEXT),
    'ShipToAddress1':   ('address1', TEXT),
    'ShipToAddress2':   ('address2', TEXT),
    'ShipToAddress3':   ('address3', TEXT),
    'ShipToCity':       ('city', TEXT),
    'ShipToState':      ('state', TEXT),
    'ShipToPostCode':   ('post_code', TEXT),
    'ShipToCountry':    ('country', TEXT),
    'ShipToPhone':      ('phone', TEXT),
    'ShipToEmail':      ('email', TEXT),
    'Carrier':          ('carrier', TEXT),
    'ShipInstructions': ('ship_instructions', TEXT),
}

PRODUCTS = {
    'ShortDesc':           ('short_description', TEXT),
    'ItemName':            ('short_description', TEXT),
    'LongDesc':            ('long_description', TEXT),
    'PlistDesc':           ('plist_description', TEXT),
    'MaterialsDesc':       ('materials_description', TEXT),
    'Features':            ('features', TEXT),
    'CategoryCode':        ('category_code', TEXT),
    'CollectionCode':      ('collection_code', TEXT),
    'TradeNameCode':       ('trade_name_code@TradeName', TAXO),
    'ProductStory':        ('story', TEXT),
    'Story':               ('story', TEXT),
    'NetPrice':            ('net_price', NUM),
    'PromotionalPrice':    ('promotional_price', NUM),
    'MinimumOrder':        ('minimum_order', NUM),
    'UnitsPerCarton':      ('units_per_carton', NUM),
    'ShipWeight':          ('shipping_weight', NUM),
    'ProductVolume':       ('product_volume', NUM),
    'ProductDimensionsIn': ('product_dimensions_in', TEXT),
    'ProductDimensionsCm': ('product_dimensions_cm', TEXT),
    'UPCValue':            ('upc_value', TEXT),
    'UPCType':             ('upc_type', TEXT),
    'ProductType':         ('product_type', TEXT),
    'SuiteGroup':          ('suite_group', TEXT),
    'ImageFileName':       ('images|images_json', PAIR),
}

INVENTORY = {
    'QtyAvailable':             ('qty_available', NUM),
    'QtyOnHand':                ('qty_on_hand', NUM),
    'QtyOnOrder':               ('qty_on_p_order', NUM),
    'QtyInTransit':             ('qty_in_transit', NUM),
    'QtyOnBackorder':           ('qty_on_backorder', NUM),
    'QtyReserved':              ('qty_reserved', NUM),
    'QtyInShowroom':            ('qty_in_showroom', NUM),
    'QtyOverseas':              ('qty_overseas', NUM),
    'NextScheduledReceiptDate': ('next_scheduled_receipt_date', NUM),
    'NextScheduledReceiptQty':  ('next_scheduled_receipt_qty', NUM),
}

OPTIONS = {
    'Name':            ('name', TEXT),
    'Description':     ('description', TEXT),
    'CategoryCode':    ('category_code', TEXT),
    'ImageFileName':   ('image_name', TEXT),
    'SortValue':       ('sort_value', NUM),
    'PriceAddend':     ('price_addend', NUM),
    'PriceFactor':     ('price_factor', NUM),
    'OptionFormCodes': ('option_form_codes', TEXT),
}

OPTION_GROUPS = {
    'Name':        ('name', TEXT),
    'Options':     ('options', TEXT),
    'PriceAddend': ('price_addend', NUM),
    'PriceFactor': ('price_factor', NUM),
}

STORIES = {
    'ProductStory': ('story', TEXT),
    'Story':        ('story', TEXT),
}

# file type -> (key column, live table, live key column, live-row filter, colmap,
#               omitted-record semantics)
MATRIX_OPTIONS = {
    'OptionItemCode': ('option_item_code', TEXT),
    'NetPrice':       ('net_price', NUM),
    'ImageName':      ('image_name', TEXT),
    'OptionGroup1':   ('option_group1', TEXT),
    'OptionGroup2':   ('option_group2', TEXT),
    'OptionGroup3':   ('option_group3', TEXT),
    'OptionGroup4':   ('option_group4', TEXT),
    'OptionGroup5':   ('option_group5', TEXT),
}

CONTRACT_PRICES = {
    'ItemNumber':         ('item_number', TEXT),
    'ContractPrice':      ('contract_price', NUM),
    'DistributionCenter': ('distribution_center', TEXT),
    'QuantityBreaks':     ('quantity_breaks', TEXT),
}

SPECS = {
    'customers.csv':     ('BillToCode', 'customers', 'code', 'TRUE',
                          CUSTOMERS_BILLTO, 'HARD-DELETE'),
    'products.csv':      ('BaseItemCode', 'products', 'item_number',
                          'NOT COALESCE(deleted,false)', PRODUCTS, 'SOFT-DELETE'),
    'inventory.csv':     ('BaseItemCode', 'inventories', 'base_item_code', 'TRUE',
                          INVENTORY, 'HARD-DELETE'),
    'options.csv':       ('Code', 'options', 'code', 'TRUE', OPTIONS, 'HARD-DELETE'),
    'option_groups.csv': ('Code', 'option_groups', 'code', 'TRUE', OPTION_GROUPS,
                          'HARD-DELETE'),
    'stories.csv':       ('BaseItemCode', 'products', 'item_number',
                          'NOT COALESCE(deleted,false)', STORIES, 'sets story=null'),
    # Added 2026-09-09. The proposal said ALL EIGHT types, because the hazard is
    # COLUMN BLANKING and blanking is unaffected by delete semantics. These
    # three were missing, so a lossy file of any of them passed B7 by not being
    # recognised at all - which is the §3.4 pattern: a check that had nothing to
    # measure reporting a pass.
    'matrix_options.csv': ('ItemNumber', 'matrix_options', 'item_number', 'TRUE',
                           MATRIX_OPTIONS, 'HARD-DELETE'),
    'contract_prices.csv': ('BillToCode', 'contract_prices', 'bill_to_code', 'TRUE',
                            CONTRACT_PRICES, 'HARD-DELETE'),
    # products_1.csv is a SUPPLEMENT: it updates by BaseItemCode and deletes
    # nothing, so row loss is impossible. Column blanking is not - a supplement
    # that carries a column empty still overwrites it - hence WARN, not BLOCKING.
    'products_1.csv':    ('BaseItemCode', 'products', 'item_number',
                          'NOT COALESCE(deleted,false)', PRODUCTS,
                          'no delete; updates by key'),
}

EMPTY_COLLECTIONS = ("'[]'", "'{}'", "'null'")


def sql_literal(s):
    return "'" + str(s).replace("'", "''") + "'"


# Every live column is compared AS TEXT, and the `::text` is not decoration.
# `products.images` is `text` but `products.images_json` is `json`, so
# `COALESCE(images_json,'')` is not a wrong answer -- it is
# `invalid input syntax for type json`, and it aborts the whole stage-1
# statement. That means B7's per-column density had never once run against a
# real org carrying an ImageFileName column: the check most concerned with
# blanked images could not measure images.
#
# Found 2026-09-09 by running the emitted SQL through the MCP instead of
# reading it. It survived review because the expression LOOKS symmetric, and
# because JSONISH -- the other kind that COALESCEs a collection -- happens to
# sit on `text` columns (`territory_codes`, `trade_name_codes`,
# `collection_codes`, `category_codes` are all `text`, verified live). One
# kind was right by luck and its neighbour was broken.
#
# So the cast is applied for every kind rather than for the one that failed.
# `col::text` is a no-op on text and correct on json, jsonb, numeric and
# timestamps, and it removes the class of bug rather than this instance.

def _t(col):
    return '%s::text' % col


def filled_expr(col, kind):
    """The SQL predicate for "this live cell carries a value"."""
    if kind == NUM:
        return '%s IS NOT NULL' % col
    if kind == JSONISH:
        return ("btrim(COALESCE(%s,'')) <> '' AND btrim(COALESCE(%s,'')) NOT IN (%s)"
                % (_t(col), _t(col), ', '.join(EMPTY_COLLECTIONS)))
    if kind == PAIR:
        a, b = col.split('|')
        return ("(btrim(COALESCE(%s,'')) <> '' AND btrim(COALESCE(%s,'')) NOT IN (%s)) "
                "OR (btrim(COALESCE(%s,'')) <> '' AND btrim(COALESCE(%s,'')) NOT IN (%s))"
                % (_t(a), _t(a), ', '.join(EMPTY_COLLECTIONS),
                   _t(b), _t(b), ', '.join(EMPTY_COLLECTIONS)))
    if kind == TAXO:
        # DENSITY only asks "does this cell carry a value", and a code is a
        # value. Resolution is a stage-2 concern, so density stays on the raw
        # column -- a product with an unresolvable code is still populated.
        return "btrim(COALESCE(%s,'')) <> ''" % _t(col.split('@')[0])
    return "btrim(COALESCE(%s,'')) <> ''" % _t(col)


def value_expr(col, kind):
    if kind == PAIR:
        a, b = col.split('|')
        return ("COALESCE(NULLIF(btrim(COALESCE(%s,'')),''), btrim(COALESCE(%s,'')))"
                % (_t(a), _t(b)))
    if kind == TAXO:
        # Resolve the stored code to the NAME the file carries. Qualified with
        # `t.` because stage 2 aliases the product table `t` and an
        # unqualified organization_id inside this subquery would bind to
        # taxonomies instead -- which would silently compare every product
        # against every org's taxonomy and return whatever came first.
        # Falls back to the raw code when nothing resolves, so an orphaned
        # code shows up as a disagreement rather than as a blank.
        column, taxo_type = col.split('@')
        return ("COALESCE((SELECT btrim(tx.name) FROM taxonomies tx "
                "WHERE tx.organization_id = t.organization_id "
                "AND tx.code = t.%s AND tx.type = '%s' LIMIT 1), "
                "btrim(COALESCE(t.%s::text,'')))"
                % (column, taxo_type, column))
    return "btrim(COALESCE(%s::text,''))" % col


def detect_file_type(path, headers):
    base = os.path.basename(path).lower()
    by_name = next((k for k in SPECS if k in base), None)
    hset = {h.strip().lower() for h in headers}
    by_header = None
    if 'billtocode' in hset:
        by_header = 'customers.csv'
    elif 'baseitemcode' in hset:
        if 'productstory' in hset or 'story' in hset:
            by_header = 'stories.csv'
        elif any(h.startswith('qty') for h in hset):
            by_header = 'inventory.csv'
        else:
            by_header = 'products.csv'
    elif 'code' in hset:
        by_header = 'option_groups.csv' if 'options' in hset else 'options.csv'
    note = None
    if by_name and by_header and by_name != by_header:
        note = ('filename says %s but headers say %s - trusting the headers'
                % (by_name, by_header))
        return by_header, note
    return (by_name or by_header), note


def read_file(path):
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
        raise SystemExit('%s is empty' % path)
    headers = [h.strip() for h in rows[0]]
    body = [r for r in rows[1:] if any(c.strip() for c in r)]
    return headers, body


def file_density(headers, body):
    fill = {}
    for i, h in enumerate(headers):
        fill[h] = sum(1 for r in body if i < len(r) and str(r[i]).strip())
    return fill


def resolve_columns(ftype, headers):
    """Split the file's headers into evaluated and NOT CHECKED. §3.4."""
    keycol, table, livekey, live, colmap, _ = SPECS[ftype]
    shipto = CUSTOMERS_SHIPTO if ftype == 'customers.csv' else {}
    mapped, unmapped = [], []
    for h in headers:
        if h == keycol:
            continue
        if h in colmap:
            mapped.append((h, colmap[h][0], colmap[h][1], table))
        elif h in shipto:
            mapped.append((h, shipto[h][0], shipto[h][1], 'shipping_locations'))
        else:
            unmapped.append(h)
    return mapped, unmapped


def emit_sql(path, ftype, headers, body, shortname, sample_n):
    if not SHORTNAME_RE.match(shortname):
        raise SystemExit('unsafe shortname: %r' % shortname)
    keycol, table, livekey, live, _, _ = SPECS[ftype]
    mapped, unmapped = resolve_columns(ftype, headers)
    kidx = next((i for i, h in enumerate(headers) if h.lower() == keycol.lower()), None)
    if kidx is None:
        raise SystemExit('%s has no %s column' % (path, keycol))

    stmts = []

    # -- stage 1: live per-column density, over the org's live rows -----------
    for tbl in sorted({m[3] for m in mapped}):
        cols = [m for m in mapped if m[3] == tbl]
        sel = ',\n  '.join(
            'count(*) FILTER (WHERE %s) AS %s' % (filled_expr(c[1], c[2]), _alias(c[0]))
            for c in cols)
        if tbl == 'shipping_locations':
            frm = ("""FROM shipping_locations s
JOIN customers c ON c.id = s.customer_id
WHERE c.organization_id = (SELECT id FROM organizations WHERE shortname = {sn})"""
                   .format(sn=sql_literal(shortname)))
            sel = sel.replace('FILTER (WHERE ', 'FILTER (WHERE ')
            total = 'count(*) AS live_rows'
        else:
            frm = ("""FROM {t}
WHERE organization_id = (SELECT id FROM organizations WHERE shortname = {sn})
  AND {live}""".format(t=tbl, sn=sql_literal(shortname), live=live))
            total = 'count(*) AS live_rows'
        stmts.append('-- B7 stage 1: live density, %s\nSELECT %s,\n  %s\n%s'
                     % (tbl, total, sel, frm))

    # -- stage 2: value spot-check on a sample of shared keys ----------------
    keys = [r[kidx].strip() for r in body if kidx < len(r) and r[kidx].strip()]
    uniq = sorted(set(keys))
    rng = random.Random(1729)          # fixed seed: the sample is reproducible
    sample = sorted(rng.sample(uniq, min(sample_n, len(uniq))))
    if sample and any(m[3] == table for m in mapped):
        cols = [m for m in mapped if m[3] == table]
        sel = ',\n  '.join('%s AS %s' % (value_expr(c[1], c[2]), _alias(c[0]))
                           for c in cols)
        vals = ',\n    '.join('(%s)' % sql_literal(k) for k in sample)
        stmts.append("""-- B7 stage 2: value spot-check, {n} sampled keys
WITH sample(k) AS (VALUES
    {vals}
)
SELECT t.{livekey} AS __key,
  {sel}
FROM {t} t
JOIN sample s ON upper(t.{livekey}) = upper(s.k)
WHERE t.organization_id = (SELECT id FROM organizations WHERE shortname = {sn})
  AND {live}""".format(n=len(sample), vals=vals, livekey=livekey, sel=sel,
                       t=table, sn=sql_literal(shortname), live=live))

    meta = {
        'file': path, 'file_type': ftype, 'key_column': keycol,
        'file_rows': len(body), 'distinct_keys': len(uniq),
        'target_org': shortname, 'live_table': table,
        'omitted_records': SPECS[ftype][5],
        'evaluated_columns': [m[0] for m in mapped],
        'not_checked_columns': unmapped,
        'sample_keys': sample,
        'column_kinds': {m[0]: m[2] for m in mapped},
        'file_density': {h: file_density(headers, body)[h] for h in headers},
    }
    return meta, stmts


def _alias(header):
    return 'c_' + re.sub(r'[^a-z0-9]+', '_', header.lower()).strip('_')


def norm(v, kind=TEXT):
    """Normalise a value for comparison.

    JSONISH columns are stored as a JSON array (`territory_codes` is `["32"]`)
    while the file carries the bare member (`32`). Comparing the raw strings
    reports 100% disagreement on data that agrees perfectly - found by B7's own
    first run against mali, which is exactly the "a lookup that returns nothing
    is not an answer" shape: a formatting mismatch masquerading as a finding.
    """
    s = str(v or '').strip()
    if kind in (JSONISH, PAIR) and s.startswith('[') and s.endswith(']'):
        try:
            parsed = json.loads(s)
        except (ValueError, TypeError):
            parsed = None
        if isinstance(parsed, list):
            # A list of SCALARS is territory_codes (`["32"]` against `32`).
            # A list of OBJECTS is products.images_json, whose members are
            # {"file_name": ..., "last_modified_at": ...} while the file
            # carries a bare comma-separated filename list. Both are the same
            # fact in two encodings, and both were reporting 100%
            # disagreement -- the scalar case was fixed against mali in
            # August and the object case was not, in the same function, for
            # the neighbouring column kind. `last_modified_at` is server
            # state that no file can carry, so only `file_name` is compared.
            parts = []
            for x in parsed:
                if isinstance(x, dict):
                    parts.append(str(x.get('file_name')
                                     or x.get('name') or ''))
                else:
                    parts.append(str(x))
            s = ','.join(p for p in parts if p)
    # The file's own list is comma-separated and may carry a trailing comma
    # (`A.jpg,A_2.jpg,`), which is not a difference in content.
    if kind == PAIR:
        s = ','.join(p for p in (q.strip() for q in s.split(',')) if p)
    return re.sub(r'\s+', ' ', s).strip().casefold()


def report(meta, results, drop_points, disagree_pct):
    """results = {"density": {table: {...}}, "spotcheck": [rows]}"""
    out, blocking, warn, notchecked = [], [], [], []
    frows = meta['file_rows']
    fdens = meta['file_density']
    density = results.get('density') or {}

    # flatten the density rows the operator fed back
    live = {}
    live_rows = {}
    for tbl, row in density.items():
        r = row[0] if isinstance(row, list) else row
        live_rows[tbl] = r.get('live_rows')
        for k, v in r.items():
            if k != 'live_rows':
                live[k] = (v, tbl)

    out.append('%-24s %10s %10s %10s' % ('column', 'file', 'live', 'change'))
    out.append('-' * 58)
    evaluated = 0
    for h in meta['evaluated_columns']:
        a = _alias(h)
        if a not in live:
            notchecked.append('%s - live density was not returned' % h)
            continue
        lv, tbl = live[a]
        lrows = live_rows.get(tbl) or 0
        if lrows == 0:
            notchecked.append('%s - the org holds 0 live rows in %s, nothing to lose'
                              % (h, tbl))
            continue
        if (lv or 0) == 0:
            notchecked.append('%s - live holds this on 0 of %d rows, nothing to lose'
                              % (h, lrows))
            continue
        evaluated += 1
        fpct = 100.0 * fdens.get(h, 0) / frows if frows else 0.0
        lpct = 100.0 * lv / lrows
        delta = fpct - lpct
        out.append('%-24s %5d %4.0f%% %5d %4.0f%% %+9.1f pt'
                   % (h[:24], fdens.get(h, 0), fpct, lv, lpct, delta))
        if delta <= -drop_points:
            would = max(0, int(round(lv * (1 - fpct / 100.0))))
            # SEVERITY SPLITS ON DELETE SEMANTICS, the same split A1 prints.
            # Fixed 2026-09-09: every density finding used to be BLOCKING
            # regardless of file type, so `products.csv` - which SOFT-deletes,
            # leaving `deleted=true` to reverse - was reported at the same
            # weight as `customers.csv`, which hard-deletes and leaves nothing.
            # Blanking is unrecoverable either way; ROW loss is not, and that is
            # what the tier is about.
            omitted = SPECS[meta['file_type']][5]
            hard = omitted.startswith('HARD')
            msg = ('%s: the file carries it on %.1f%% of rows, live holds it on '
                   '%.1f%%. Importing this file would blank roughly %d live '
                   'value(s). [%s]' % (h, fpct, lpct, would, omitted))
            (blocking if hard else warn).append(msg)

    # stage 2
    spot = results.get('spotcheck') or []
    spotlines, compared_any = [], False
    if spot:
        bykey = {}
        for r in spot:
            bykey[norm(r.get('__key'))] = r
        headers, body = read_file(meta['file'])
        kidx = next(i for i, h in enumerate(headers)
                    if h.lower() == meta['key_column'].lower())
        fileby = {}
        for r in body:
            if kidx < len(r) and r[kidx].strip():
                fileby[norm(r[kidx])] = dict(zip(headers, r))
        kinds = meta.get('column_kinds', {})
        for h in meta['evaluated_columns']:
            a = _alias(h)
            kind = kinds.get(h, TEXT)
            both = diff = 0
            ex = []
            for k, lrow in bykey.items():
                if a not in lrow or k not in fileby:
                    continue
                fv, lvv = norm(fileby[k].get(h), kind), norm(lrow.get(a), kind)
                if fv and lvv:
                    both += 1
                    if fv != lvv:
                        diff += 1
                        if len(ex) < 3:
                            ex.append('%s: file=%r live=%r'
                                      % (k, (fileby[k].get(h) or '')[:28],
                                         (lrow.get(a) or '')[:28]))
            if both:
                compared_any = True
                pct = 100.0 * diff / both
                spotlines.append('  %-24s %3d of %3d disagree (%.0f%%)%s'
                                 % (h[:24], diff, both, pct,
                                    '' if not ex else '\n        ' + '\n        '.join(ex)))
                if pct >= disagree_pct:
                    warn.append(
                        '%s: %d of %d sampled rows carry a value on BOTH sides and '
                        'they DISAGREE (%.0f%%). Density cannot see this. Confirm '
                        'which side is right before uploading.' % (h, diff, both, pct))
    return out, blocking, warn, notchecked, spotlines, evaluated, compared_any




# --- DATABASE_URL path (added 2026-09-09) -----------------------------------
# Before this, B7 offered --emit-sql and --from-results only, so running it
# meant a human carrying rows between two commands. That is workable at a desk
# and impossible on a cron: the gate could not run in the same container that
# produced the file it was meant to gate. `collector.py:197-217` had had a
# working DATABASE_URL path since August; the four modules that actually gate
# an upload had none, so a read-only replica credential on its own would still
# have left the gate unrunnable.
#
# It runs the SAME statements --emit-sql prints and assembles the SAME dict
# --from-results loads, so the two paths cannot drift into disagreeing about
# what was measured. Read-only is enforced per statement in dbexec.

def _session():
    import os as _os
    import sys as _sys
    _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    import dbexec
    return dbexec, dbexec.ReadOnlySession()

def _results_from_db(meta, stmts):
    """Run B7's stage-1 and stage-2 statements into the --from-results shape.

    Stage 1 is one statement per live table and is keyed BY that table, because
    `report()` flattens `density` per table to recover `live_rows`. The table
    name is read back out of the statement's own comment, which is the same
    string an operator reads when keying the rows by hand.
    """
    dbexec, sess = _session()
    res = {'meta': meta, 'density': {}, 'spotcheck': []}
    with sess:
        for st in stmts:
            m = re.match(r'--\s*B7 stage 1: live density,\s*(\S+)', st)
            if m:
                res['density'][m.group(1)] = sess.rows(st)
            elif re.match(r'--\s*B7 stage 2:', st):
                res['spotcheck'] = sess.rows(st)
            else:
                raise RuntimeError('unrecognised B7 statement: %s'
                                   % st.splitlines()[0][:80])
    return res



def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('file')
    ap.add_argument('--org', required=True, help='target org shortname')
    ap.add_argument('--emit-sql', action='store_true')
    ap.add_argument('--from-results',
                    help='JSON {"meta": {...}, "density": {...}, "spotcheck": [...]}')
    ap.add_argument('--use-db', action='store_true',
                    help='run the statements directly against DATABASE_URL, '
                         'read-only. For a container; needs psycopg2.')
    ap.add_argument('--sample', type=int, default=50,
                    help='rows for the stage-2 value spot-check (default 50)')
    ap.add_argument('--drop-points', type=float, default=10.0,
                    help='BLOCKING when fill drops this many points (default 10)')
    ap.add_argument('--disagree-pct', type=float, default=20.0,
                    help='WARN when this %% of sampled shared values differ (default 20)')
    args = ap.parse_args()

    headers, body = read_file(args.file)
    ftype, note = detect_file_type(args.file, headers)
    if not ftype:
        raise SystemExit('cannot tell what eCat file this is: %s' % args.file)

    if args.emit_sql:
        meta, stmts = emit_sql(args.file, ftype, headers, body, args.org, args.sample)
        if note:
            meta['note'] = note
        print(json.dumps(meta, indent=2))
        print('\n-- run through supercat-postgres-vpn, read-only --')
        for s in stmts:
            print('\n' + s + ';')
        return 0

    if args.use_db:
        meta, stmts = emit_sql(args.file, ftype, headers, body, args.org,
                               args.sample)
        if note:
            meta['note'] = note
        try:
            res = _results_from_db(meta, stmts)
        except Exception as exc:                              # noqa: BLE001
            print('B7 NOT CHECKED - %s' % exc)
            return 2
    elif args.from_results:
        with open(args.from_results) as fh:
            res = json.load(fh)
    else:
        ap.error('need --emit-sql, --from-results or --use-db')
    meta = res['meta']

    print('=' * 70)
    print('B7 LOSSY REGENERATION GATE')
    print('=' * 70)
    print('file      : %s' % meta['file'])
    print('type      : %s (keyed by %s, %d rows)'
          % (meta['file_type'], meta['key_column'], meta['file_rows']))
    print('target org: %s   omitted records: %s'
          % (meta['target_org'], meta['omitted_records']))
    if meta.get('note'):
        print('NOTE      : %s' % meta['note'])
    print('-' * 70)
    out, blocking, warn, notchecked, spotlines, evaluated, compared_any = report(
        meta, res, args.drop_points, args.disagree_pct)
    print('\n-- stage 1: column fill density, file vs live ' + '-' * 22)
    for l in out:
        print(l)

    print('\n-- stage 2: value spot-check on %d sampled keys %s'
          % (len(meta.get('sample_keys') or []), '-' * 18))
    if not spotlines:
        print('  NOT CHECKED - no sampled key matched live on any comparable column.')
    else:
        for l in spotlines:
            print(l)

    # §3.4 coverage, always, before any verdict
    total = len(meta['evaluated_columns']) + len(meta['not_checked_columns'])
    print('\n-- coverage (BUILD_SPEC §3.4) ' + '-' * 38)
    print('  evaluated %d of %d file columns for density' % (evaluated, total))
    print('  value spot-check: %s'
          % ('ran' if compared_any else 'NOT CHECKED - nothing comparable'))
    for n in notchecked:
        print('  NOT CHECKED  %s' % n)
    for h in meta['not_checked_columns']:
        print('  NOT CHECKED  %s - no live counterpart is mapped for this column' % h)

    print('\n' + '-' * 70)
    for b in blocking:
        print('BLOCKING [pre_upload] : %s' % b)
    for w in warn:
        print('WARN     [pre_upload] : %s' % w)
    print('\nstage    : pre_upload - nothing here has been applied to the org yet.')
    print('repair   : carry the live values forward into the file and DECLARE them')
    print('           as carried, or get an export that includes the missing fields.')
    if evaluated == 0:
        print('\nVERDICT: NOT CHECKED - no column could be compared. This is not a pass.')
        return 2
    if blocking:
        print('\nVERDICT: DO NOT UPLOAD')
        return 1
    if warn:
        print('\nVERDICT: PROCEED ONLY AFTER CONFIRMING THE ABOVE')
        return 0
    print('\nVERDICT: PASS - the file is not poorer than the rows it replaces')
    return 0


if __name__ == '__main__':
    sys.exit(main())
