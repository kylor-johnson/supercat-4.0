"""
Spec-derived Postgres queries for the onboarding Phase Progression collector.

Every query here is (a) traceable to a clause in Phase_Anchors.md and (b) verified
against the live information_schema on 2026-08-18. Where the spec named a column
that does not exist, the correction is noted inline and recorded in
RECONCILIATION.md — do not "fix" one without the other.

Two classes of metric, and the distinction is load-bearing:

  POINT_IN_TIME  derived from append-only rows (import_events, orders, logins).
                 Honest under --as-of: filtered by `created_at <= as_of`.

  CURRENT_STATE  derived from mutable tables (products, customers, price_levels,
                 user_types). CANNOT be reconstructed for a past date. Under
                 --as-of these are still today's values and are tagged as such,
                 so a backtest can never silently score them as historical.

A metric that cannot be captured emits NOT_CAPTURED with a reason, never a zero.
Same discipline as preflight_gate.py: an unexplained absence is how a real gap
turns into a silent pass.
"""

POINT_IN_TIME = "point_in_time"
CURRENT_STATE = "current_state"

# Personal-email providers — never treated as a client domain, regardless of source.
# Phase_Anchors.md § Resolving client_domains[]
PERSONAL_EMAIL_DOMAINS = (
    "gmail.com", "yahoo.com", "outlook.com", "icloud.com", "hotmail.com",
    "me.com", "aol.com", "fuse.net", "proton.me", "protonmail.com",
)

# Every block type that actually occurs as a top-level key in import_events.
# Enumerated from live data 2026-08-18 across drf/mali/pebl/tcd/leg:
#   Images 612, Products 429, Option Groups 77, Options 67, Option Images 62,
#   Inventory 55, Product Stories 49, Customers 44, Matrix Options 30,
#   Taxonomies 6
# Phase_Anchors.md names only six of these. "Option Images", "Matrix Options"
# and "Taxonomies" are undocumented — see RECONCILIATION.md.
OBSERVED_FILE_TYPES = (
    "Products", "Customers", "Options", "Option Groups", "Inventory",
    "Product Stories", "Images", "Option Images", "Matrix Options", "Taxonomies",
)

# Back-compat alias for the spec's narrower vocabulary.
CORE_FILE_TYPES = (
    "Products", "Customers", "Options", "Option Groups",
    "Inventory", "Product Stories",
)

# Image-import events dominate recent history (612 of 1,431 events in the
# sample above). Any "last N rows" window hides core-file events behind them —
# which is exactly why IMPORT_EVENTS is unwindowed.
NOISE_FILE_TYPES = ("Images", "Option Images")

# Core files that count toward the Phase 3 ">=2 of" clause.
# "Option Groups" and "Images" deliberately excluded — Phase_Anchors.md § Phase 3
# names exactly these five.
PHASE3_CORE_FILES = (
    "Products", "Customers", "Options", "Inventory", "Product Stories",
)


# ---------------------------------------------------------------- cohort


COHORT = """
SELECT id, shortname, name, created_at,
       properties->>'status' AS status,
       order_email_recipient,
       COALESCE(send_order_email_on_submit,false) AS send_order_email_on_submit
       -- import_active dropped (D6): true for 0 of 257 orgs
FROM organizations
WHERE properties->>'status' = 'onboarding'
  AND name NOT ILIKE '%%demo%%'
  AND name NOT ILIKE '%%template%%'
  AND name NOT ILIKE '%%test%%'
  AND COALESCE(properties->>'status','') NOT IN ('demo','test')
ORDER BY created_at DESC
"""

# Explicit-org form, for backtesting clients that have since left the cohort
# (drf/libco/pebl are now 'active', tcs is 'fully_suspended').
ORGS_BY_SHORTNAME = """
SELECT id, shortname, name, created_at,
       properties->>'status' AS status,
       order_email_recipient,
       COALESCE(send_order_email_on_submit,false) AS send_order_email_on_submit
       -- import_active dropped (D6): true for 0 of 257 orgs
FROM organizations
WHERE shortname = ANY(%(shortnames)s)
ORDER BY shortname
"""


# ------------------------------------------------- client_domains[] resolution
# Resolution order (Phase_Anchors.md): overrides.yml -> order_email_recipient
# -> [HubSpot: DROPPED, see RECONCILIATION.md] -> admin email fallback.
# First non-empty SOURCE wins outright; do not merge across sources.

ADMIN_EMAIL_DOMAINS = """
SELECT lower(split_part(u.email,'@',2)) AS domain, count(*) AS n
FROM org_users ou
JOIN users u ON u.id = ou.user_id
WHERE ou.organization_id = %(org_id)s
  AND NOT COALESCE(ou.disabled, false)
  AND u.email IS NOT NULL
  AND u.email NOT LIKE '%%@supercatsolutions.com'
GROUP BY 1
ORDER BY n DESC
"""


# ------------------------------------------------------------ import events
# Phase 2 + Phase 3. Append-only, so fully honest under --as-of.
# NOT windowed by row count: image-import events dominate recent history for
# image-heavy orgs and would hide core-file events (Phase_Anchors.md § Phase 3).

IMPORT_EVENTS = """
SELECT id, created_at, data
FROM import_events
WHERE organization_id = %(org_id)s
  AND created_at <= %(as_of)s
ORDER BY created_at DESC
"""


# ------------------------------------------------------------ catalog state

# D7 (SCORECARD.md): `visible_products` measures `hideable` only. When the org has
# product_synch_requires_photo ON, an imageless product does NOT reach the iPad even
# though it counts as visible. tcd: 397 visible / 396 with images -> 1 product silently
# absent. `ipad_visible_products` is the figure a rep would actually see.
CATALOG_COUNTS = """
SELECT
  count(*) FILTER (WHERE NOT deleted)                                   AS active_products,
  count(*) FILTER (WHERE NOT deleted AND image_exists)                  AS products_with_images,
  count(*) FILTER (WHERE NOT deleted AND NOT COALESCE(hideable,false))  AS visible_products,
  count(*) FILTER (
    WHERE NOT deleted AND NOT COALESCE(hideable,false)
      AND (image_exists OR NOT (SELECT COALESCE(product_synch_requires_photo,false)
                                FROM organizations WHERE id = %(org_id)s))
  )                                                                     AS ipad_visible_products,
  count(*)                                                              AS rows_total
FROM products
WHERE organization_id = %(org_id)s
"""

PRICE_LEVELS = """
SELECT code, name, pl_type, factor, COALESCE(hidden,false) AS hidden
FROM price_levels
WHERE organization_id = %(org_id)s
ORDER BY position NULLS LAST, code
"""

CUSTOMER_COUNTS = """
SELECT
  count(*) AS total_customers,
  count(*) FILTER (
    WHERE c.default_price_code IS NULL OR btrim(c.default_price_code) = ''
  ) AS blank_default_price_code,
  count(*) FILTER (
    WHERE c.default_price_code IS NOT NULL
      AND btrim(c.default_price_code) <> ''
      AND NOT EXISTS (
        SELECT 1 FROM price_levels pl
        WHERE pl.organization_id = c.organization_id
          AND lower(btrim(pl.code)) = lower(btrim(c.default_price_code))
      )
  ) AS unresolved_default_price_code,
  -- D11: territory_codes stores an EMPTY ARRAY as the literal string '[]', not ''.
  -- A `btrim(...) = ''` test silently returns 0 and reports "all customers have
  -- territories" when none do. Verified 2026-08-25: pebl 171/171 and libco 6/267
  -- were being missed. Caught by the pebl blind read, not by this code.
  count(*) FILTER (
    WHERE c.territory_codes IS NULL OR btrim(c.territory_codes) IN ('', '[]', '{}')
  ) AS customers_without_territory
FROM customers c
WHERE c.organization_id = %(org_id)s
"""

OPTION_COUNTS = """
SELECT
  (SELECT count(*) FROM options       WHERE organization_id = %(org_id)s) AS options_count,
  (SELECT count(*) FROM option_groups WHERE organization_id = %(org_id)s) AS option_groups_count
"""

INVENTORY_COUNTS = """
SELECT count(*) AS inventory_rows, max(updated_at) AS inventory_last_updated
FROM inventories
WHERE organization_id = %(org_id)s
"""

# Smart-SKU builder lives in org properties JSONB, NOT set by import.
# ecat-postgres-audit skill, § Options / smart SKU builder.
ORG_FEATURE_FLAGS = """
SELECT
  (properties ->> 'configured_item_number_builder') IS NOT NULL AS has_sku_builder,
  properties ->> 'status'                                       AS status,
  COALESCE(imports_options, false)                              AS imports_options,
  COALESCE(enable_rep_activity, false)                          AS enable_rep_activity,
  COALESCE(product_synch_requires_photo, false)                 AS product_synch_requires_photo
  -- NOTE (D6): `import_active` is deliberately NOT collected. It is true for 0 of 257
  -- organizations -- dead field, and reporting it invites a false inference.
FROM organizations
WHERE id = %(org_id)s
"""


# ------------------------------------------------------------------- reps
# Phase 5. The contamination-free rep definition, verbatim from Phase_Anchors.md.
# is_admin is read from org_users (per-org role), NOT users.is_admin (global).
# last_ipad_login_at is a mutable column: the boolean "ever logged in" is
# effectively point-in-time, but "active in last 30d" is CURRENT_STATE — under
# --as-of it reflects today. Tagged accordingly in the snapshot.

REPS = """
SELECT
  u.email,
  lower(split_part(u.email,'@',2)) AS domain,
  ut.name                          AS user_type,
  ou.last_ipad_login_at,
  ou.last_ecat_online_login_at
FROM org_users ou
JOIN users u       ON u.id  = ou.user_id
LEFT JOIN user_types ut ON ut.id = ou.user_type_id
WHERE ou.organization_id = %(org_id)s
  AND NOT COALESCE(ou.is_admin, false)
  AND COALESCE(ut.name, '') <> 'DefaultUserGroup'
  AND u.email NOT LIKE '%%@supercatsolutions.com'
  AND NOT COALESCE(ou.disabled, false)
"""

USER_TYPE_COUNTS = """
SELECT
  count(*)                                        AS user_types_total,
  count(*) FILTER (WHERE name <> 'DefaultUserGroup') AS user_types_beyond_default
FROM user_types
WHERE organization_id = %(org_id)s
"""

IPAD_REPORT_COUNT = """
SELECT count(*) AS ipad_reports
FROM ipad_reports
WHERE organization_id = %(org_id)s
"""


# ----------------------------------------------------------------- orders
# Phase 7 clause 3 — the allowlist model.
#
# SPEC BUG CORRECTED: Phase_Anchors.md says `customers.company_name`.
# That column does not exist. Verified live 2026-08-18: the customer name
# column is `customers.name`. Using the spec verbatim would have thrown
# UndefinedColumn on every Phase 7 evaluation.
#
# Requires a POSITIVE match to a real customers row — a mere mismatch against
# organizations.name fails unsafe when brand <> legal name (the PEBL precedent:
# brand "Pebl" vs legal "Skyard Furniture Co Ltd.").

# D15 (SCORECARD.md): `is_submitted` is NULLABLE. A bare `FILTER (WHERE o.is_submitted)`
# silently drops NULL rows, so an org with order rows can report zero. mali's only
# order row has is_submitted NULL -- an empty server-side cart. Always report the raw
# row count alongside the submitted count.
ORDERS_MATCHED_TO_CUSTOMERS = """
SELECT
  count(*)                                                    AS order_rows_total,
  count(*) FILTER (WHERE o.is_submitted IS NULL)              AS order_rows_unsubmitted_null,
  count(*) FILTER (WHERE COALESCE(o.is_submitted,false))      AS submitted_orders_total,
  count(*) FILTER (
    WHERE o.is_submitted
      AND o.submit_date >= %(as_of)s - INTERVAL '90 days'
  )                                                            AS submitted_orders_90d,
  count(*) FILTER (
    WHERE o.is_submitted
      AND o.submit_date >= %(as_of)s - INTERVAL '90 days'
      AND EXISTS (
        SELECT 1 FROM customers c
        WHERE c.organization_id = o.organization_id
          AND lower(btrim(c.name)) = lower(btrim(o.bill_to_company_name))
      )
  )                                                            AS customer_matched_orders_90d
FROM orders o
WHERE o.organization_id = %(org_id)s
  AND o.created_at <= %(as_of)s
"""

# Surfaces SELF_TEST_SUSPECTED_NOT_CUSTOMER (Flags_and_Signals.md § F):
# submitted orders whose bill-to matches no customer row.
UNMATCHED_ORDER_NAMES = """
SELECT DISTINCT btrim(o.bill_to_company_name) AS bill_to, count(*) AS n
FROM orders o
WHERE o.organization_id = %(org_id)s
  AND o.is_submitted
  AND o.created_at <= %(as_of)s
  AND o.bill_to_company_name IS NOT NULL
  AND NOT EXISTS (
    SELECT 1 FROM customers c
    WHERE c.organization_id = o.organization_id
      AND lower(btrim(c.name)) = lower(btrim(o.bill_to_company_name))
  )
GROUP BY 1
ORDER BY n DESC
LIMIT 25
"""


# Registry of every query, with its temporal honesty class.
# The collector iterates this — adding a query here is the only place to add one.
QUERY_REGISTRY = (
    # (key,                        sql,                          temporal,      many?)
    ("import_events",              IMPORT_EVENTS,                POINT_IN_TIME, True),
    ("catalog_counts",             CATALOG_COUNTS,               CURRENT_STATE, False),
    ("price_levels",               PRICE_LEVELS,                 CURRENT_STATE, True),
    ("customer_counts",            CUSTOMER_COUNTS,              CURRENT_STATE, False),
    ("option_counts",              OPTION_COUNTS,                CURRENT_STATE, False),
    ("inventory_counts",           INVENTORY_COUNTS,             CURRENT_STATE, False),
    ("org_feature_flags",          ORG_FEATURE_FLAGS,            CURRENT_STATE, False),
    ("reps",                       REPS,                         CURRENT_STATE, True),
    ("user_type_counts",           USER_TYPE_COUNTS,             CURRENT_STATE, False),
    ("ipad_report_count",          IPAD_REPORT_COUNT,            CURRENT_STATE, False),
    ("orders_matched",             ORDERS_MATCHED_TO_CUSTOMERS,  POINT_IN_TIME, False),
    ("unmatched_order_names",      UNMATCHED_ORDER_NAMES,        POINT_IN_TIME, True),
    ("admin_email_domains",        ADMIN_EMAIL_DOMAINS,          CURRENT_STATE, True),
)
