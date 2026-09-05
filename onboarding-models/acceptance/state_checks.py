#!/usr/bin/env python3
"""A2, A3, B3, B5 — the post-import state checks. BUILD_SPEC §3.

Four criteria, all answerable from the live org, all read-only. Emits SQL for
the supercat-postgres-vpn MCP; never connects.

    A2  no placeholder pricing reaching production
    A3  every stored reference resolves
    B3  territory codes present where rep<->customer filtering is expected
    B5  the inventory field the org DISPLAYS must be the one populated

## Severity discipline

Three harness findings in a row were right about the fact and wrong about the
severity, and the cost of that is specific: an operator stops reading the
output. So every threshold below is chosen to fire on the incident that
motivated it and stay quiet otherwise, and anything that is merely unusual is
reported as INFO with its number rather than as a defect.

    BLOCKING  a client-visible defect, evidenced
    WARN      real, but its severity depends on intent only the client knows
    INFO      measured, notable, not a defect

## Dated measurements

Every finding carries `measured_at`. leg's custom-field registry changed between
2026-08-27 and 2026-09-04, and both readings were accurate for their moment;
without a date one of them just looks wrong. State moves — say when you looked.
"""

import argparse
import datetime
import json
import re
import sys

SHORTNAME_RE = re.compile(r'^[a-z0-9_-]{1,32}$')


def lit(s):
    return "'" + str(s).replace("'", "''") + "'"


def org_ref(shortname):
    if not SHORTNAME_RE.match(shortname or ''):
        raise SystemExit('unsafe shortname: %r' % shortname)
    return "(SELECT id FROM organizations WHERE shortname = %s)" % lit(shortname)


# --------------------------------------------------------------------- A2

def sql_a2(sn):
    """Price levels by customer share, with how many distinct values each
    resolves to across the live catalogue.

    `net` is stored on `products.net_price`; every other level lives in the
    `prices_json` blob under its own code. A level that resolves to ONE distinct
    value across the whole catalogue is a placeholder, and it only matters when
    customers actually point at it - drf had 389 of 389 customers on `net` with
    every product at $1.00 for 42+ days.
    """
    o = org_ref(sn)
    return """
WITH live AS (
  -- prices_json is TEXT here, not jsonb; the cast is required and the
  -- NULLIF guards rows that have never been priced.
  SELECT net_price, NULLIF(btrim(COALESCE(prices_json,'')), '') AS prices_json
  FROM products
  WHERE organization_id = {o} AND NOT COALESCE(deleted,false)
),
tot AS (SELECT count(*)::numeric AS n FROM customers WHERE organization_id = {o})
SELECT pl.code, pl.name, pl.pl_type,
       (SELECT count(*) FROM customers c
         WHERE c.organization_id = {o}
           AND lower(btrim(c.default_price_code)) = lower(pl.code)) AS customers_on_level,
       (SELECT n FROM tot) AS customers_total,
       (SELECT count(*) FROM live) AS live_products,
       CASE WHEN lower(pl.code)='net'
            THEN (SELECT count(DISTINCT net_price) FROM live)
            ELSE (SELECT count(DISTINCT prices_json::jsonb ->> pl.code::text) FROM live)
       END AS distinct_values,
       CASE WHEN lower(pl.code)='net'
            THEN (SELECT min(net_price)::text FROM live)
            ELSE (SELECT min(prices_json::jsonb ->> pl.code::text) FROM live)
       END AS sample_value
FROM price_levels pl
WHERE pl.organization_id = {o}
ORDER BY customers_on_level DESC, pl.code
""".format(o=o).strip()


def check_a2(rows, measured_at):
    findings = []
    for r in rows:
        total = float(r.get('customers_total') or 0)
        on = float(r.get('customers_on_level') or 0)
        if not total:
            continue
        share = 100.0 * on / total
        distinct = r.get('distinct_values')
        live = r.get('live_products') or 0
        if share <= 50 or distinct is None:
            continue
        if int(distinct) == 1 and int(live) > 20:
            findings.append({
                'rule': 'A2.placeholder_pricing', 'severity': 'BLOCKING',
                'measured_at': measured_at,
                'detail': "price level %r carries %d of %d customers (%.1f%%) and "
                          "resolves to ONE distinct value (%s) across all %d live "
                          "products. That is a placeholder priced catalogue reaching "
                          "every customer on the level."
                          % (r['code'], int(on), int(total), share,
                             r.get('sample_value'), int(live)),
            })
        elif int(distinct) <= 3 and int(live) > 50:
            findings.append({
                'rule': 'A2.near_constant_pricing', 'severity': 'WARN',
                'measured_at': measured_at,
                'detail': "price level %r carries %.1f%% of customers and resolves to "
                          "only %d distinct values across %d live products."
                          % (r['code'], share, int(distinct), int(live)),
            })
    return findings


# --------------------------------------------------------------------- A3

def sql_a3(sn):
    """Every stored reference resolves.

    Each branch is a stored id or code that something else is expected to
    resolve. Nothing in the app checks these, and a level can be deleted out
    from under historical orders silently - pebl has 12 orders worth $264,130
    pointing at a price level that no longer exists.
    """
    o = org_ref(sn)
    return """
SELECT 'customers.default_price_code' AS reference, count(*) AS dangling,
       min(c.default_price_code) AS example
FROM customers c
WHERE c.organization_id = {o}
  AND btrim(COALESCE(c.default_price_code,'')) <> ''
  AND NOT EXISTS (SELECT 1 FROM price_levels pl
                  WHERE pl.organization_id = {o}
                    AND lower(pl.code) = lower(btrim(c.default_price_code)))
UNION ALL
SELECT 'orders.price_level', count(*), min(o2.price_level)
FROM orders o2
WHERE o2.organization_id = {o}
  AND btrim(COALESCE(o2.price_level,'')) <> ''
  AND NOT EXISTS (SELECT 1 FROM price_levels pl
                  WHERE pl.organization_id = {o}
                    AND lower(pl.code) = lower(btrim(o2.price_level)))
UNION ALL
SELECT 'products.trade_name_code', count(*), min(p.trade_name_code)
FROM products p
WHERE p.organization_id = {o} AND NOT COALESCE(p.deleted,false)
  AND btrim(COALESCE(p.trade_name_code,'')) <> ''
  AND NOT EXISTS (SELECT 1 FROM taxonomies t
                  WHERE t.organization_id = {o}
                    AND lower(t.code) = lower(btrim(p.trade_name_code)))
UNION ALL
SELECT 'products.collection_code', count(*), min(p.collection_code)
FROM products p
WHERE p.organization_id = {o} AND NOT COALESCE(p.deleted,false)
  AND btrim(COALESCE(p.collection_code,'')) <> ''
  AND NOT EXISTS (SELECT 1 FROM taxonomies t
                  WHERE t.organization_id = {o}
                    AND lower(t.code) = lower(btrim(p.collection_code)))
UNION ALL
SELECT 'products.category_code', count(*), min(p.category_code)
FROM products p
WHERE p.organization_id = {o} AND NOT COALESCE(p.deleted,false)
  AND btrim(COALESCE(p.category_code,'')) <> ''
  AND NOT EXISTS (SELECT 1 FROM taxonomies t
                  WHERE t.organization_id = {o}
                    AND lower(t.code) = lower(btrim(p.category_code)))
UNION ALL
-- RelatedItems is stored as a JSON ARRAY STRING ('["A","B"]'), not the comma
-- list the CSV carries. Splitting on ',' leaves the brackets and quotes
-- attached and every element then fails to resolve: the first version of this
-- branch reported 29,161 dangling references at drf, all of them artifacts of
-- the split. The example value gave it away - it came back as '"ADELINA-UV-ASH"'
-- WITH the quotes. Parse the array; fall back to a comma split only if the
-- value is not JSON.
SELECT 'products.related_items', count(*), min(x.code)
FROM products p,
     LATERAL (
       SELECT CASE
         WHEN btrim(COALESCE(p.related_items,'')) LIKE '[%'
           THEN (SELECT array_agg(v) FROM jsonb_array_elements_text(
                   btrim(p.related_items)::jsonb) AS v)
         ELSE string_to_array(COALESCE(p.related_items,''), ',')
       END AS codes
     ) arr,
     LATERAL unnest(COALESCE(arr.codes, ARRAY[]::text[])) AS x(code)
WHERE p.organization_id = {o} AND NOT COALESCE(p.deleted,false)
  AND btrim(x.code) <> ''
  AND NOT EXISTS (SELECT 1 FROM products q
                  WHERE q.organization_id = {o} AND NOT COALESCE(q.deleted,false)
                    AND upper(q.item_number) = upper(btrim(x.code)))
""".format(o=o).strip()


def check_a3(rows, measured_at):
    findings = []
    for r in rows:
        n = int(r.get('dangling') or 0)
        if not n:
            continue
        ref = r['reference']
        sev = 'BLOCKING' if ref.startswith(('customers.', 'orders.')) else 'WARN'
        findings.append({
            'rule': 'A3.dangling_reference', 'severity': sev,
            'measured_at': measured_at,
            'detail': '%s: %d value(s) resolve to nothing (e.g. %r).%s'
                      % (ref, n, r.get('example'),
                         ' Image filenames are NOT covered - that is B2, still '
                         'unimplemented.' if ref.startswith('products.related') else ''),
        })
    return findings


# --------------------------------------------------------------------- B3

def sql_b3(sn):
    """Territory codes. The empty value is the literal string '[]', not '' and
    not NULL - a naive test returns 0 and reports that every customer has a
    territory when none does. That bug was in the audit tooling itself."""
    o = org_ref(sn)
    return """
SELECT count(*) AS customers,
       count(*) FILTER (WHERE btrim(COALESCE(territory_codes,'')) IN ('', '[]'))
         AS without_territory,
       count(*) FILTER (WHERE btrim(COALESCE(territory_codes,'')) NOT IN ('', '[]'))
         AS with_territory,
       -- The rep definition is the framework's, verbatim from
       -- Phase_Anchors.md via collector/queries.py REPS. Counting only
       -- "not is_admin" reported 10 reps at pebl where the framework counts 9:
       -- chuck+u@supercatsolutions.com is SuperCat staff. Two parts of the
       -- system must not disagree about the word "rep".
       (SELECT count(*)
          FROM org_users ou
          JOIN users u2 ON u2.id = ou.user_id
          LEFT JOIN user_types ut ON ut.id = ou.user_type_id
         WHERE ou.organization_id = {o}
           AND NOT COALESCE(ou.is_admin, false)
           AND COALESCE(ut.name, '') <> 'DefaultUserGroup'
           AND u2.email NOT LIKE '%@supercatsolutions.com'
           AND NOT COALESCE(ou.disabled, false)) AS reps,
       (SELECT string_agg(DISTINCT u3.email, ', ')
          FROM org_users ou2 JOIN users u3 ON u3.id = ou2.user_id
          LEFT JOIN user_types ut2 ON ut2.id = ou2.user_type_id
         WHERE ou2.organization_id = {o}
           AND NOT COALESCE(ou2.is_admin, false)
           AND (u3.email LIKE '%@supercatsolutions.com'
                OR COALESCE(ut2.name,'') = 'DefaultUserGroup'
                OR COALESCE(ou2.disabled,false))) AS excluded_non_reps,
       (SELECT min(c2.code) FROM customers c2 WHERE c2.organization_id = {o}
          AND btrim(COALESCE(c2.territory_codes,'')) IN ('', '[]')) AS example_customer
FROM customers WHERE organization_id = {o}
""".format(o=o).strip()


def check_b3(rows, measured_at):
    r = rows[0] if isinstance(rows, list) else rows
    total = int(r.get('customers') or 0)
    without = int(r.get('without_territory') or 0)
    reps = int(r.get('reps') if r.get('reps') is not None
               else r.get('non_admin_users') or 0)
    excluded = (r.get('excluded_non_reps') or '').strip()
    specimen = r.get('example_customer')
    if not total:
        return [{'rule': 'B3.no_customers', 'severity': 'INFO',
                 'measured_at': measured_at,
                 'detail': 'org has no customers; territory filtering is not yet '
                           'applicable.'}]
    if without == 0:
        return []
    share = 100.0 * without / total
    # Severity turns on whether anyone is there to be filtered. Territory codes
    # on an org with no reps provisioned is a sequencing fact, not a defect.
    if without == total and reps > 0:
        sev = 'BLOCKING'
        tail = ('Rep<->customer filtering is off org-wide: every one of %d reps sees '
                'every customer.' % reps)
    elif reps == 0:
        sev = 'INFO'
        tail = ('No non-admin users exist yet, so nothing is being mis-filtered '
                'today. This becomes blocking the moment reps are provisioned.')
    else:
        sev = 'WARN'
        tail = '%d rep(s) provisioned.' % reps
    return [{'rule': 'B3.territory_codes_empty', 'severity': sev,
             'measured_at': measured_at,
             'example': specimen,
             'detail': '%d of %d customers (%.1f%%) have empty territory codes '
                       "(stored as the literal '[]')%s. %s%s"
                       % (without, total, share,
                          ', e.g. %r' % specimen if specimen else '',
                          tail,
                          ' (%s excluded as non-rep by the framework definition.)'
                          % excluded if excluded else '')}]


# --------------------------------------------------------------------- B5

def sql_b5(sn):
    """Config-vs-data agreement for inventory display.

    The config is `custom_fields.alias`, NOT `organizations.inventory_management`
    (which is empty for 10 of 11 orgs checked and does not discriminate). An
    alias of `i.qty_on_hand` means the org surfaces on-hand; `ic.<Div>_Qty*`
    means a per-division inventory custom field.

    B5 is config-vs-data agreement, NOT a fixed field. Assuming qty_available
    was the display field is what produced SCORECARD §12 R1.
    """
    o = org_ref(sn)
    return """
SELECT
  (SELECT string_agg(cf.alias || CASE WHEN cf.send_to_ipad THEN '' ELSE ' (not sent)' END,
                     ', ' ORDER BY cf.position)
     FROM custom_fields cf
    WHERE cf.organization_id = {o} AND (cf.alias LIKE 'i.qty%' OR cf.alias LIKE 'ic.%'))
    AS registered_qty_aliases,
  (SELECT count(*) FROM inventories i WHERE i.organization_id = {o}) AS inventory_rows,
  -- "no stock value" and "stock value of zero" are different states a rep
  -- experiences differently, and a non-zero count silently folds in negatives.
  -- leg: 755 rows, 755 non-null, 704 > 0, 28 = 0, 23 NEGATIVE. A single
  -- "populated 727" figure described none of those.
  (SELECT count(i.qty_available) FROM inventories i WHERE i.organization_id = {o})
    AS qty_available_non_null,
  (SELECT count(*) FROM inventories i WHERE i.organization_id = {o}
     AND i.qty_available > 0) AS qty_available_gt_zero,
  (SELECT count(*) FROM inventories i WHERE i.organization_id = {o}
     AND i.qty_available = 0) AS qty_available_zero,
  (SELECT count(*) FROM inventories i WHERE i.organization_id = {o}
     AND i.qty_available < 0) AS qty_available_negative,
  (SELECT count(i.qty_on_hand) FROM inventories i WHERE i.organization_id = {o})
    AS qty_on_hand_non_null,
  (SELECT count(*) FROM inventories i WHERE i.organization_id = {o}
     AND i.qty_on_hand > 0) AS qty_on_hand_gt_zero,
  (SELECT count(*) FROM inventories i WHERE i.organization_id = {o}
     AND i.qty_on_hand = 0) AS qty_on_hand_zero,
  (SELECT count(*) FROM inventories i WHERE i.organization_id = {o}
     AND i.qty_on_hand < 0) AS qty_on_hand_negative,
  -- Specimen for the negative state. Negative on-hand is usually legitimate
  -- (oversold / backorder carried from the ERP), but the magnitude is the
  -- question: leg's floor is -12,643 on RWP26LA.
  (SELECT min(i.qty_on_hand) FROM inventories i WHERE i.organization_id = {o})
    AS qty_on_hand_min,
  (SELECT i.base_item_code FROM inventories i WHERE i.organization_id = {o}
    ORDER BY i.qty_on_hand ASC NULLS LAST LIMIT 1) AS qty_on_hand_min_sku,
  (SELECT count(*) FROM inventories i WHERE i.organization_id = {o}
     AND i.custom_fields IS NOT NULL AND i.custom_fields::text <> '{{}}')
    AS inventory_custom_fields_populated
""".format(o=o).strip()


def check_b5(rows, measured_at):
    r = rows[0] if isinstance(rows, list) else rows
    aliases = (r.get('registered_qty_aliases') or '').strip()
    rows_n = int(r.get('inventory_rows') or 0)
    icust = int(r.get('inventory_custom_fields_populated') or 0)

    def st(col):
        d = {
            'non_null': int(r.get('%s_non_null' % col) or 0),
            'gt_zero': int(r.get('%s_gt_zero' % col) or 0),
            'negative': int(r.get('%s_negative' % col) or 0),
        }
        # Measured, NOT derived. Deriving zero as the remainder makes the
        # partition check below unable to ever fail.
        d['zero'] = int(r.get('%s_zero' % col) or 0)
        return d
    av, oh = st('qty_available'), st('qty_on_hand')

    def partition_ok(d):
        """Partitions must sum to the total. This is the cheapest specimen there
        is, and it catches the class of error where a breakdown is published
        that does not add up - '755 non-null, 704 > 0, 28 zero' omits 23
        negatives and 704+28 != 755. Enforced, not documented."""
        return d['gt_zero'] + d['zero'] + d['negative'] == d['non_null']

    def describe(name, d):
        """Name each state separately. 'No stock value' and 'a stock value of
        zero' read differently to a rep, and lumping them into one 'populated'
        figure describes neither."""
        return ('%s: %d of %d rows carry a value (%d > 0, %d exactly 0, %d '
                'negative); %d are NULL'
                % (name, d['non_null'], rows_n, d['gt_zero'], d['zero'],
                   d['negative'], rows_n - d['non_null']))

    if rows_n == 0:
        return [{'rule': 'B5.no_inventory', 'severity': 'INFO',
                 'measured_at': measured_at,
                 'detail': 'org has no inventory rows; nothing to reconcile.'}]

    state = '%s. %s. inventory custom fields populated on %d rows.' % (
        describe('qty_available', av), describe('qty_on_hand', oh), icust)
    out = []

    # The partition check runs on the numbers this tool is about to print, so a
    # breakdown that does not add up is caught here rather than in a client's
    # recount.
    for nm, d in (('qty_available', av), ('qty_on_hand', oh)):
        if not partition_ok(d):
            out.append({
                'rule': 'B5.partition_mismatch', 'severity': 'WARN',
                'measured_at': measured_at,
                'detail': '%s breakdown does not sum: %d > 0 + %d zero + %d '
                          'negative != %d non-null. The counts are inconsistent, so '
                          'do not report any of them until this is resolved.'
                          % (nm, d['gt_zero'], d['zero'], d['negative'],
                             d['non_null'])})

    neg_min = r.get('qty_on_hand_min')
    neg_sku = r.get('qty_on_hand_min_sku')
    if oh['negative'] and neg_min is not None and int(neg_min) < 0:
        sev = 'WARN' if int(neg_min) <= -1000 else 'INFO'
        out.append({
            'rule': 'B5.negative_on_hand', 'severity': sev,
            'measured_at': measured_at,
            'example': neg_sku,
            'detail': '%d row(s) carry a NEGATIVE qty_on_hand, floor %s on %r. '
                      'Negative on-hand is usually legitimate - oversold or '
                      'backorder carried from the ERP - so this is reported as its '
                      'own state, not folded into "populated". The magnitude is the '
                      'question, not the sign.'
                      % (oh['negative'], neg_min, neg_sku)})
    if not aliases:
        out.append({
            'rule': 'B5.no_display_field_registered', 'severity': 'WARN',
            'measured_at': measured_at,
            'detail': 'no i.qty_* or ic.* alias is registered, but inventory exists. '
                      '%s MEASUREMENT ONLY: what the iPad renders with no alias '
                      'registered is NOT established here - settle it against the '
                      'sync payload or the rendering code before telling anyone reps '
                      'see nothing.' % state})
        return out

    wants_avail = 'i.qty_available' in aliases
    wants_onhand = 'i.qty_on_hand' in aliases
    if wants_avail and av['non_null'] == 0 and (oh['non_null'] > 0 or icust > 0):
        out.append({
            'rule': 'B5.config_data_mismatch', 'severity': 'BLOCKING',
            'measured_at': measured_at,
            'detail': 'the registered display alias is qty_available, but no row '
                      'carries a qty_available value. %s' % state})
    if wants_onhand and oh['non_null'] == 0 and (av['non_null'] > 0 or icust > 0):
        out.append({
            'rule': 'B5.config_data_mismatch', 'severity': 'BLOCKING',
            'measured_at': measured_at,
            'detail': 'the registered display alias is qty_on_hand, but no row '
                      'carries a qty_on_hand value. %s' % state})
    if not out:
        out.append({'rule': 'B5.agrees', 'severity': 'INFO',
                    'measured_at': measured_at,
                    'detail': 'registered alias(es) [%s] agree with the populated '
                              'columns. %s' % (aliases, state)})
    return out


CHECKS = {
    'a2': (sql_a2, check_a2), 'a3': (sql_a3, check_a3),
    'b3': (sql_b3, check_b3), 'b5': (sql_b5, check_b5),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--org', required=True)
    ap.add_argument('--check', choices=sorted(CHECKS) + ['all'], default='all')
    ap.add_argument('--emit-sql', action='store_true')
    ap.add_argument('--from-results', help='JSON {"a2": [...], "a3": [...], ...}')
    ap.add_argument('--measured-at', help='YYYY-MM-DD of the measurement')
    args = ap.parse_args()

    names = sorted(CHECKS) if args.check == 'all' else [args.check]

    if args.emit_sql:
        for n in names:
            print('-- ===== %s =====' % n.upper())
            print(CHECKS[n][0](args.org))
            print(';')
        return 0

    if not args.from_results:
        ap.error('need --emit-sql or --from-results')
    measured_at = args.measured_at or datetime.date.today().isoformat()
    with open(args.from_results) as fh:
        res = json.load(fh)

    print('=' * 72)
    print('§3 STATE CHECKS -- org %s -- measured %s' % (args.org, measured_at))
    print('=' * 72)
    allf, rc = [], 0
    for n in names:
        rows = res.get(n)
        if rows is None:
            print('\n%s  NOT RUN (no results supplied)' % n.upper())
            continue
        findings = CHECKS[n][1](rows, measured_at)
        allf += findings
        print('\n-- %s %s' % (n.upper(), '-' * 66))
        if not findings:
            print('   pass - no finding')
        for f in findings:
            print('   %-9s %s' % (f['severity'], f['rule']))
            print('             %s' % f['detail'])
            if f['severity'] == 'BLOCKING':
                rc = 1
    print('\n%s' % ('-' * 72))
    counts = {}
    for f in allf:
        counts[f['severity']] = counts.get(f['severity'], 0) + 1
    print('summary: %s' % (', '.join('%s %d' % kv for kv in sorted(counts.items()))
                           or 'no findings'))
    print('all findings measured %s; state moves, so a later reading may differ.'
          % measured_at)
    return rc


if __name__ == '__main__':
    sys.exit(main())
