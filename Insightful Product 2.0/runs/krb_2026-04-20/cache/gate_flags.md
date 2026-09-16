# Gate Flags — Kaleen Rugs & Broadloom (krb, org_id=244)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | false | org_summary.has_clicky_portal = false |
| HAS_CART | false | recurring_services = "eCat (iPad) Service" — no B2B Cart; iPad-only bundle |
| HAS_PORTAL_ORDERS | false | portal_order_count = 0 (LTM); portal_orders entity updated 2026-03-13 but contains 0 LTM rows |
| HAS_INVENTORY | true | inventory_count = 2,509 rows; however inventory data is Stale (255 days since last update) |
| HAS_SALES_DATA | false | sales_data_count = 0 |
| HAS_SALES_SECTION | false | 0 qualifying reps with ≥10 iPad orders LTM (only 1 LTM eCat order total) |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv present (6 days old, within 90-day window) |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in peer CSV |
| BENCHMARK_CONFIDENCE | high | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 9 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Home & Decor / Housewares / Art Manufacturers / iPad-only | Source for plain-language cohort framing |
| CLICKY_PREFIX | N/A | HAS_CLICKY = false |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | N/A | HAS_PORTAL_ORDERS = false — VM-45 precondition not met |
| VM45_GATE_2 | N/A | HAS_PORTAL_ORDERS = false — VM-45 precondition not met |
| VM45_RENDER | false | HAS_PORTAL_ORDERS = false — skip capture rate subsection |
| QUALIFYING_REP_COUNT | 0 | No reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 8 rows |
| SHOWROOM_EXCLUSIONS | 0 | Pass 1 (keyword scan): 0 matches; Pass 2 (brand-name "kaleen"): 0 matches |

## Org Identity

- **Client name**: Kaleen Rugs & Broadloom
- **Shortname**: krb
- **Org ID**: 244
- **Bundle**: iPad-only
- **Bundle label for report**: eCat iPad App
- **Vertical**: Home & Decor / Housewares / Art Manufacturers
- **Segment (internal)**: Catalog-Focused
- **ARR**: $2,900
- **Feature depth**: 2

## Instance Summary (diagnostic)

| Metric | Value |
|--------|-------|
| Active products | 1,493 |
| Total ERP customers | 2,208 |
| Active org_users | 5 |
| eCat orders (12mo) | 1 |
| eCat GMV (12mo) | $381.00 |
| All-time eCat orders | 2 |
| Last eCat order | 2025-08-20 |
| Portal orders | 0 |
| Portal order items | 0 |
| Sales data rows | 0 |
| Inventory rows | 2,509 |
| Smart Stacks | 1 |
| Shared resources | 57 |
| Import events | 345 |
| Login events | 341 |

## Validation Log

- **portal_orders**: portal_orders entity exists (last updated 2026-03-13) but LTM count = 0 — HAS_PORTAL_ORDERS overridden to false. Q-16 and VM-45 skipped.
- **Showroom scan**: Pass 1 keyword scan returned 0 results. Pass 2 brand-name scan ("kaleen") returned 0 results. No showroom exclusions.
- **VM-45**: Precondition not met (HAS_PORTAL_ORDERS = false). Both gates N/A. VM45_RENDER = false.
- **Commerce volume note**: Only 1 LTM eCat order ($381) and 2 all-time. This is an extremely thin commerce org. Many customer/commerce queries return empty results due to insufficient order volume. Q-12 shows active_12mo = 0 distinct customers (the single LTM order has no customer_num that maps to an active customer in the 12mo window).
- **Inventory staleness**: Inventory data is 255 days stale (last updated 2025-08-07). While HAS_INVENTORY = true (2,509 rows), the data is Stale by freshness standards.
- **Import errors**: Most recent imports (2025-12-03) contained errors: invalid trade name codes on product import (code "HAB") and missing parent code on taxonomy import (code "HNB").
- **Q-10 (Feature Enablement)**: No mobile_sites row exists for org 244 — feature enablement flags cannot be derived from this table.
