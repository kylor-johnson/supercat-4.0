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
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import intent as intent_mod  # noqa: E402
import severity as sev  # noqa: E402

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

    `net` is stored on `products.net_price`; every other AD-HOC level lives in
    the `prices_json` blob under its own code. A level that resolves to ONE
    distinct value across the whole catalogue is a placeholder, and it only
    matters when customers actually point at it - drf had 389 of 389 customers
    on `net` with every product at $1.00 for 42+ days.

    ## A2 only evaluates ad-hoc levels, and now says so

    `arithmetic` and `quantity` levels store NO key in `prices_json`; their value
    is COMPUTED (`net_price` x `factor`, optionally against
    `target_price_level_id`). Reading `prices_json ->> code` for one of those
    returns NULL on every row, `count(DISTINCT ...)` discards the NULLs, and the
    check saw either 0 or - worse - whatever single stray row happened to carry
    the key.

    That produced a BLOCKING finding on `uhc`: 'wholesale' is arithmetic
    factor=1.0, exactly ONE of 4,433 products carried a stray `wholesale` key at
    307.89, and A2 reported "resolves to ONE distinct value across all 4433 live
    products". The catalogue in fact carries 396 distinct net prices, $0.00 to
    $450.00. Fleet-wide, 46 of A2's 47 findings were this artifact.

    So: non-ad-hoc levels are declared NOT EVALUATED rather than measured wrong.
    Resolving the arithmetic properly means following factor / target chains and
    is a separate job; it is not needed to stop the check lying.

    `products_carrying_value` is selected so the message can use the number of
    products that ACTUALLY carry a price for the level as its denominator. The
    old text said "across all N live products" where N was the whole catalogue
    even when the count came from one row - the same shape as OPEN_ITEMS F7, a
    partition that does not describe what it claims.
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
       -- How many live products actually CARRY a value for this level. This is
       -- the denominator the finding must quote: count(DISTINCT ...) above
       -- silently skips NULLs, so "1 distinct value" can describe one row while
       -- reading as though it described the catalogue.
       CASE WHEN lower(pl.code)='net'
            THEN (SELECT count(net_price) FROM live)
            ELSE (SELECT count(prices_json::jsonb ->> pl.code::text) FROM live)
       END AS products_carrying_value,
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
        carrying = r.get('products_carrying_value')
        pl_type = (r.get('pl_type') or '').strip().lower()
        # Below the share threshold the level is out of scope for a
        # placeholder-pricing finding whatever its type, so nothing is said.
        # Above it, a level A2 CANNOT evaluate has to say so out loud rather
        # than fall through to a number derived from the wrong column.
        if share <= 50:
            continue
        if pl_type and pl_type != 'ad-hoc':
            findings.append(sev.stamp({
                'rule': 'A2.not_evaluated', 'severity': 'INFO',
                'measured_at': measured_at,
                'detail': "NOT EVALUATED - %r is %s level; its value derives from "
                          "net_price and is not stored in prices_json. A2 measures "
                          "stored values. The level carries %d of %d customers "
                          "(%.1f%%), so if placeholder pricing is a live question for "
                          "this org it has to be answered another way."
                          % (r['code'],
                             ('an %s' if pl_type[:1] in 'aeiou' else 'a %s') % pl_type,
                             int(on), int(total), share),
            }, evidence_from=measured_at))
            continue
        if distinct is None:
            continue
        # Denominator is the products that carry a price for THIS level, not the
        # whole catalogue. Fall back to live_products only when the SQL predates
        # this column, and say which one is being quoted either way.
        if carrying is None:
            denom, denom_text = int(live), "%d live products" % int(live)
        else:
            denom = int(carrying)
            denom_text = ("the %d live product(s) carrying a price for it, of %d live"
                          % (int(carrying), int(live)))
        if int(distinct) == 1 and denom > 20:
            findings.append(sev.stamp({
                'rule': 'A2.placeholder_pricing', 'severity': 'BLOCKING',
                'measured_at': measured_at,
                'detail': "price level %r carries %d of %d customers (%.1f%%) and "
                          "resolves to ONE distinct value (%s) across %s. That is a "
                          "placeholder priced catalogue reaching every customer on "
                          "the level."
                          % (r['code'], int(on), int(total), share,
                             r.get('sample_value'), denom_text),
            }, evidence_from=measured_at))
        elif int(distinct) <= 3 and denom > 50:
            findings.append(sev.stamp({
                'rule': 'A2.near_constant_pricing', 'severity': 'WARN',
                'measured_at': measured_at,
                'detail': "price level %r carries %.1f%% of customers and resolves to "
                          "only %d distinct values across %s."
                          % (r['code'], share, int(distinct), denom_text),
            }, evidence_from=measured_at))
    return findings


# --------------------------------------------------------------------- A3

# Measured 2026-09-05 at ufi (421 dangling orders, the largest case in the
# cohort). Written into the finding so the tier carries its evidence.
ORDERS_PRICE_LEVEL_CONSEQUENCE = (
    ' CONSEQUENCE MEASURED, and it is none: the order total is STORED, not '
    'recomputed (421 of 421 dangling ufi orders carry a non-null total, '
    '$3,942,148.45; largest 1924-030314-2, level dc10, $976,925.00, 2014-03-03). '
    '`orders.price_level` has no foreign key - the table has two, org_user_id '
    'and organization_id - so it is a stored string by design. The Sales Portal '
    'order-history path is portal_orders/portal_order_items, a separate '
    'ERP-imported history with NO price_level column, so the Portal report '
    'cannot read this field. Era-controlled, dangling orders are 1.2% '
    'zero-total against a 0.7% control once the two STATUS codes are excluded '
    '(H: 70 of 71 orders zero, $625 total; C: 3 of 3) - the apparent 18.3% was '
    'those two pooled in, a common cause and not an effect. NOT ESTABLISHED: '
    'the Rails order-detail render path, which is not readable from here; note '
    'show_price_level_on_order is false at ufi/clli/cl/pebl and true only at '
    'sp, and what it shows is the stored string.')

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


# BUILD_SPEC §3.1 A3 says "every stored reference resolves" and names two
# incidents that are NOT among the branches below. Declared here rather than
# left implicit, per §3.4: a check that evaluates six of eight classes and
# prints six passes reads as though it covered all eight.
A3_REFERENCE_CLASSES_EVALUATED = 6
A3_REFERENCE_CLASSES_TOTAL = 8
A3_NOT_EVALUATED = [
    ('mobile_sites.price_level_id',
     'an eOL site pointing at a price level that exists in no organisation - '
     'mali held price_level_id 5722 for eight days (OPEN_ITEMS A13, since '
     'fixed). Forward-looking the way customers.default_price_code is: a site '
     'on a dead level breaks the NEXT quote, it does not describe an old one.'),
    ('organization_invitations',
     'a bulk-invite link pointing INTO another org - mali held one into `tcd`. '
     'Nothing validates that an invitation\'s user_type_id or redeemer belongs '
     'to the inviting org.'),
]


def check_a3(rows, measured_at):
    findings = []
    for r in rows:
        n = int(r.get('dangling') or 0)
        if not n:
            continue
        ref = r['reference']
        # RE-TIERED 2026-09-05, on a measurement rather than on aesthetics.
        #
        # `orders.price_level` was BLOCKING because the rule keyed on the COLUMN,
        # not on the consequence. It has repair_channel `none` - a historical
        # order's price-level string is immutable - so BLOCKING told an operator
        # to act when there is no action. Before re-tiering, the consequence was
        # measured (see `ORDERS_PRICE_LEVEL_CONSEQUENCE`):
        #
        #   1. The total is STORED, not recomputed: 421 of 421 dangling ufi
        #      orders carry a non-null `total`, summing $3,942,148.45.
        #   2. `orders` has exactly two foreign keys - org_user_id and
        #      organization_id. `price_level` has NONE; it is a stored string by
        #      design, and the level being retired does not orphan a reference.
        #   3. The Sales Portal order-history path is `portal_orders` /
        #      `portal_order_items`, a separate ERP-imported history (117,156
        #      rows at ufi against 37,817 eCat orders) - and `portal_orders` has
        #      NO price_level column at all. The Portal report cannot read it.
        #   4. Era-controlled: within 2012-08-02..2021-03-25, resolving orders
        #      are 0.7% zero-total and dangling orders 18.3%. That 26x gap is a
        #      COMMON CAUSE, not a consequence - it collapses to `H` (70 of 71
        #      orders zero, $625 total) and `C` (3 of 3), which are status codes
        #      rather than pricing levels. Excluding those two, dangling orders
        #      are 1.2% zero-total against the 0.7% control. No effect.
        #
        # So: INFO for orders.price_level. It stays a real, reportable
        # observation - the codes ARE gone - and it no longer asks for an action
        # that does not exist. customers.default_price_code keeps its tier: that
        # one is forward-looking, and a customer pointing at a missing level
        # breaks pricing on the NEXT order rather than describing an old one.
        if ref.startswith('orders.'):
            level = 'INFO'
        elif ref.startswith('customers.'):
            level = 'BLOCKING'
        else:
            level = 'WARN'
        chan = sev.a3_channel(ref)
        # Evidence dates come from the SQL where the branch has them (orders);
        # elsewhere the dangling reference is a property of current state.
        ev_from = r.get('first_seen') or measured_at
        ev_to = r.get('last_seen') or measured_at
        # evidence_state describes the EVIDENCE, not whether it is repairable.
        # An order from 2019 is closed evidence even though `orders.price_level`
        # has repair_channel `none`; conflating the two made a 2019 order print
        # as `standing`. Demotion then declines separately, on the channel, and
        # says which of the two reasons applied.
        state = 'closed' if r.get('last_seen') else 'standing'
        findings.append(sev.stamp({
            'rule': 'A3.dangling_reference', 'severity': level,
            'measured_at': measured_at,
            'detail': '%s: %d value(s) resolve to nothing (e.g. %r).%s%s'
                      % (ref, n, r.get('example'),
                         ' Image filenames are NOT covered - that is B2, still '
                         'unimplemented.' if ref.startswith('products.related') else '',
                         ORDERS_PRICE_LEVEL_CONSEQUENCE
                         if ref.startswith('orders.') else ''),
        }, evidence_from=ev_from, evidence_to=ev_to,
           repair_channel=chan, evidence_state=state))

    # Coverage always, whether or not anything was found. A silent skip and a
    # real negative are indistinguishable unless the check says which it was.
    findings.append(sev.stamp({
        'rule': 'A3.coverage', 'severity': 'NOT CHECKED',
        'measured_at': measured_at,
        'detail': 'evaluated %d of %d stored-reference classes. NOT evaluated: %s.'
                  % (A3_REFERENCE_CLASSES_EVALUATED, A3_REFERENCE_CLASSES_TOTAL,
                     '; '.join('%s - %s' % (n, why) for n, why in A3_NOT_EVALUATED)),
        'measured': 'the six branches in sql_a3: customers.default_price_code, '
                    'orders.price_level, products.trade_name_code, '
                    'products.collection_code, products.category_code, '
                    'products.related_items',
        'not_established': 'whether the two unevaluated classes resolve. Measured '
                           'directly 2026-09-09 and both are clean fleet-wide - '
                           'mobile_sites 0 of 102 dangling and 0 cross-org, '
                           'organization_invitations 0 of 307 with a wrong-org '
                           'user_type and 0 dangling redeemers - so this is '
                           'undeclared coverage, NOT a missed finding. That can '
                           'change without this check noticing.',
    }, evidence_from=measured_at))
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
        return [sev.stamp({'rule': 'B3.no_customers', 'severity': 'INFO',
                 'measured_at': measured_at,
                 'detail': 'org has no customers; territory filtering is not yet '
                           'applicable.'}, evidence_from=measured_at)]
    if without == 0:
        return []
    share = 100.0 * without / total
    # Severity turns on whether anyone is there to be filtered. Territory codes
    # on an org with no reps provisioned is a sequencing fact, not a defect.
    if without == total and reps > 0:
        level = 'BLOCKING'
        tail = ('Rep<->customer filtering is off org-wide: every one of %d reps sees '
                'every customer.' % reps)
    elif reps == 0:
        level = 'INFO'
        tail = ('No non-admin users exist yet, so nothing is being mis-filtered '
                'today. This becomes blocking the moment reps are provisioned.')
    else:
        level = 'WARN'
        tail = '%d rep(s) provisioned.' % reps
    return [sev.stamp({'rule': 'B3.territory_codes_empty', 'severity': level,
             'measured_at': measured_at,
             'example': specimen,
             'detail': '%d of %d customers (%.1f%%) have empty territory codes '
                       "(stored as the literal '[]')%s. %s%s"
                       % (without, total, share,
                          ', e.g. %r' % specimen if specimen else '',
                          tail,
                          ' (%s excluded as non-rep by the framework definition.)'
                          % excluded if excluded else '')}, evidence_from=measured_at)]


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
        return [sev.stamp({'rule': 'B5.no_inventory', 'severity': 'INFO',
                 'measured_at': measured_at,
                 'detail': 'org has no inventory rows; nothing to reconcile.'},
                 evidence_from=measured_at)]

    state = '%s. %s. inventory custom fields populated on %d rows.' % (
        describe('qty_available', av), describe('qty_on_hand', oh), icust)
    out = []

    # The partition check runs on the numbers this tool is about to print, so a
    # breakdown that does not add up is caught here rather than in a client's
    # recount.
    for nm, d in (('qty_available', av), ('qty_on_hand', oh)):
        if not partition_ok(d):
            out.append(sev.stamp({
                'rule': 'B5.partition_mismatch', 'severity': 'WARN',
                'measured_at': measured_at,
                'detail': '%s breakdown does not sum: %d > 0 + %d zero + %d '
                          'negative != %d non-null. The counts are inconsistent, so '
                          'do not report any of them until this is resolved.'
                          % (nm, d['gt_zero'], d['zero'], d['negative'],
                             d['non_null'])}, evidence_from=measured_at))

    neg_min = r.get('qty_on_hand_min')
    neg_sku = r.get('qty_on_hand_min_sku')
    if oh['negative'] and neg_min is not None and int(neg_min) < 0:
        level = 'WARN' if int(neg_min) <= -1000 else 'INFO'
        out.append(sev.stamp({
            'rule': 'B5.negative_on_hand', 'severity': level,
            'measured_at': measured_at,
            'example': neg_sku,
            'detail': '%d row(s) carry a NEGATIVE qty_on_hand, floor %s on %r. '
                      'Negative on-hand is usually legitimate - oversold or '
                      'backorder carried from the ERP - so this is reported as its '
                      'own state, not folded into "populated". The magnitude is the '
                      'question, not the sign.'
                      % (oh['negative'], neg_min, neg_sku)}, evidence_from=measured_at))
    if not aliases:
        out.append(sev.stamp({
            'rule': 'B5.no_display_field_registered', 'severity': 'WARN',
            'measured_at': measured_at,
            'detail': 'no i.qty_* or ic.* alias is registered, but inventory exists. '
                      '%s MEASUREMENT ONLY: what the iPad renders with no alias '
                      'registered is NOT established here - settle it against the '
                      'sync payload or the rendering code before telling anyone reps '
                      'see nothing.' % state}, evidence_from=measured_at))
        return out

    wants_avail = 'i.qty_available' in aliases
    wants_onhand = 'i.qty_on_hand' in aliases
    if wants_avail and av['non_null'] == 0 and (oh['non_null'] > 0 or icust > 0):
        out.append(sev.stamp({
            'rule': 'B5.config_data_mismatch', 'severity': 'BLOCKING',
            'measured_at': measured_at,
            'detail': 'the registered display alias is qty_available, but no row '
                      'carries a qty_available value. %s' % state}, evidence_from=measured_at))
    if wants_onhand and oh['non_null'] == 0 and (av['non_null'] > 0 or icust > 0):
        out.append(sev.stamp({
            'rule': 'B5.config_data_mismatch', 'severity': 'BLOCKING',
            'measured_at': measured_at,
            'detail': 'the registered display alias is qty_on_hand, but no row '
                      'carries a qty_on_hand value. %s' % state}, evidence_from=measured_at))
    if not out:
        out.append(sev.stamp({'rule': 'B5.agrees', 'severity': 'INFO',
                    'measured_at': measured_at,
                    'detail': 'registered alias(es) [%s] agree with the populated '
                              'columns. %s' % (aliases, state)}, evidence_from=measured_at))
    return out


CHECKS = {
    'a2': (sql_a2, check_a2), 'a3': (sql_a3, check_a3),
    'b3': (sql_b3, check_b3), 'b5': (sql_b5, check_b5),
}




# --- DATABASE_URL path (added 2026-09-09) -----------------------------------
# Before this, state_checks offered --emit-sql and --from-results only, so running it
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

def _statements(org, names):
    """[(results-key, sql)] in emitted order: the header first, then each check.

    The key is what --from-results expects as a dict key, lower-cased, and
    --emit-sql prints it upper-cased in its `===== NAME =====` banner. One
    function so the two paths cannot name the same statement differently -- the
    F6 `_key()` defect (`file:option_groups` never matching `Option Groups`,
    73 windows sitting at WARN while LOOKING evaluated) was exactly this shape.
    """
    out = [('header', sev.sql_header(org_ref(org)))]
    for n in names:
        out.append((n, CHECKS[n][0](org)))
    return out



def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--org', required=True)
    ap.add_argument('--check', choices=sorted(CHECKS) + ['all'], default='all')
    ap.add_argument('--emit-sql', action='store_true')
    ap.add_argument('--from-results', help='JSON {"a2": [...], "a3": [...], ...}')
    ap.add_argument('--use-db', action='store_true',
                    help='run the statements directly against DATABASE_URL, '
                         'read-only. For a container; needs psycopg2.')
    ap.add_argument('--measured-at', help='YYYY-MM-DD of the measurement')
    ap.add_argument('--intent', help='path to config_intent.toml (default: alongside the harness)')
    ap.add_argument('--no-intent', action='store_true',
                    help='run WITHOUT declared intent. Every declaration is ignored and '
                         'the report says so on every line. Never the default: an absent '
                         'declaration file must not look like an org with no declarations.')
    args = ap.parse_args()

    names = sorted(CHECKS) if args.check == 'all' else [args.check]

    if args.emit_sql:
        for key, sql in _statements(args.org, names):
            print('-- ===== %s =====' % key.upper())
            print(sql)
            print(';')
        return 0

    if args.use_db:
        try:
            dbexec, sess = _session()
            res = {}
            with sess:
                for key, sql in _statements(args.org, names):
                    res[key] = sess.rows(sql)
        except Exception as exc:                              # noqa: BLE001
            print('state_checks NOT CHECKED - %s' % exc, file=sys.stderr)
            return 2
    elif args.from_results:
        with open(args.from_results) as fh:
            res = json.load(fh)
    else:
        ap.error('need --emit-sql, --from-results or --use-db')
    measured_at = args.measured_at or datetime.date.today().isoformat()

    # F5: declared intent. Fails CLOSED - if the file cannot be read the run
    # stops, because "no declarations" and "declarations unavailable" are
    # different states and only one of them is safe to report findings from.
    org_intent, intent_unavailable = {}, None
    if args.no_intent:
        intent_unavailable = 'suppressed by --no-intent'
    else:
        try:
            org_intent = intent_mod.for_org(intent_mod.load(args.intent), args.org)
        except intent_mod.IntentError as e:
            print('DECLARED INTENT UNAVAILABLE -- refusing to run.\n  %s\n'
                  '  Re-run with --no-intent to proceed anyway; every finding will be '
                  'marked as measured without declarations.' % e, file=sys.stderr)
            return 2
    suppressed, shown, unconsumed = intent_mod.declarations_for(org_intent)

    # Decision 5: the org-state header, printed FIRST and ALWAYS. A green
    # report is structurally impossible once the org's state is on it.
    header = res.get('header')
    header_state = {}
    if header:
        header_state = dict(header[0] if isinstance(header, list) else header)
    header_state['shortname'] = args.org
    header_state.setdefault('last_import_by_type', res.get('last_import_by_type') or {})
    header_state.setdefault('admin_touched', res.get('admin_touched') or {})
    if header:
        sev.render_header(header_state, sys.stdout)
    else:
        print('=' * 72)
        print('ecat-acceptance — %s' % args.org)
        print('!! ORG-STATE HEADER NOT RUN (no `header` rows supplied). Findings '
              'below are not\n   set against the org\'s state, and demotion has '
              'nothing to key on.')
        print('=' * 72)

    print()
    print('§3 STATE CHECKS -- org %s -- measured %s' % (args.org, measured_at))
    if intent_unavailable:
        print('!! DECLARED INTENT NOT LOADED (%s) -- every finding below is '
              'measured WITHOUT declarations.' % intent_unavailable)
    print('=' * 72)
    allf, alld, allmoves, rc = [], [], [], 0
    if header:
        hf = sev.header_findings(header_state, measured_at)
        hf, hmoves = sev.apply_demotion(hf, header_state)
        allmoves += hmoves
        hf, hdecl = intent_mod.apply(hf, suppressed, measured_at)
        alld += hdecl
        if hf:
            print('\n-- ORG STATE %s' % ('-' * 57))
            for f in hf:
                print('   %-9s %s  [%s · repair %s]'
                      % (f['severity'], f['rule'], f['stage'],
                         f['repair_channel']))
                print('             %s' % f['detail'])
                if f['severity'] == 'BLOCKING':
                    rc = 1
            allf += hf
    for n in names:
        rows = res.get(n)
        if rows is None:
            print('\n%s  NOT RUN (no results supplied)' % n.upper())
            continue
        findings = CHECKS[n][1](rows, measured_at)
        findings, moves = sev.apply_demotion(findings, header_state)
        allmoves += moves
        findings, declared = intent_mod.apply(findings, suppressed, measured_at)
        allf += findings
        alld += declared
        print('\n-- %s %s' % (n.upper(), '-' * 66))
        if not findings and not declared:
            print('   pass - no finding')
        elif not findings:
            print('   pass - no finding (%d DECLARED, see below)' % len(declared))
        for f in findings:
            print('   %-9s %s  [%s · repair %s · evidence %s %s]'
                  % (f['severity'], f['rule'], f.get('stage', '?'),
                     f.get('repair_channel', '?'), f.get('evidence_state', '?'),
                     ('%s..%s' % (f.get('evidence_from'), f.get('evidence_to')))
                     if f.get('evidence_from') != f.get('evidence_to')
                     else str(f.get('evidence_from'))))
            print('             %s' % f['detail'])
            if f.get('demotion') and f['demotion'].startswith('demoted'):
                print('             ^ %s' % f['demotion'])
            if f['severity'] == 'BLOCKING':
                rc = 1
    if not intent_unavailable:
        intent_mod.render(shown, unconsumed, suppressed, alld, args.org, sys.stdout)

    print('\n%s' % ('-' * 72))
    counts = {}
    for f in allf:
        counts[f['severity']] = counts.get(f['severity'], 0) + 1
    print('summary: %s' % (', '.join('%s %d' % kv for kv in sorted(counts.items()))
                           or 'no findings'))
    if alld:
        print('declared: %d finding(s) suppressed by config_intent.toml (%s)'
              % (len(alld), ', '.join(sorted(set(d['rule'] for d in alld)))))
    if allmoves:
        print('demoted:  %d finding(s) moved one level' % len(allmoves))
        for rule, was, now, why in allmoves:
            print('          %s  %s -> %s  (%s)' % (rule, was, now, why))
    print('all findings measured %s; state moves, so a later reading may differ.'
          % measured_at)
    return rc


if __name__ == '__main__':
    sys.exit(main())
