# Gate Flags — Magnussen Home (mh, org_id=184)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | false | org_summary.has_clicky_portal = false |
| HAS_CART | false | server_orders = 0; recurring_services = null |
| HAS_PORTAL_ORDERS | false | portal_order_count = 0 (LTM and all-time) |
| HAS_INVENTORY | true | inventory_count = 22 (NOTE: 256 days stale per data_versions) |
| HAS_SALES_DATA | true | sales_data_count = 25,523 |
| HAS_SALES_SECTION | true | 9 qualifying reps with ≥10 iPad orders LTM (threshold: 5) |
| HAS_PEER_DATA | true | benchmark_eligible = True, run_date = 2026-04-14 (6 days old) |
| BENCHMARK_ELIGIBLE | True | From peer_benchmark_2026-04-14.csv |
| BENCHMARK_CONFIDENCE | low | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier3 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 54 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | iPad-only | Source for plain-language cohort framing |
| CLICKY_PREFIX | N/A | HAS_CLICKY = false |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | N/A | HAS_PORTAL_ORDERS = false — Q-45 not applicable |
| VM45_GATE_2 | N/A | HAS_PORTAL_ORDERS = false — Q-45 not applicable |
| VM45_RENDER | false | HAS_PORTAL_ORDERS = false — no ERP denominator available |
| QUALIFYING_REP_COUNT | 9 | Reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 117 rows |
| SHOWROOM_EXCLUSIONS | 0 | No keyword, brand-name, or non-person entity matches found |
| MIXPANEL_ORDER_TRACKING_GAP | false | Postgres LTM iPad orders: 291, Mixpanel total submit_order: 558 (all-time) |

## Org Identity

- **Client name**: Magnussen Home
- **Shortname**: mh
- **Org ID**: 184
- **Bundle**: iPad-only
- **Bundle label for report**: eCat iPad App

## Validation Log

- portal_orders: portal_order_count = 0 (both LTM and all-time). HAS_PORTAL_ORDERS = false. Q-16, Q-18 Part B, and Q-45 skipped.
- Showroom scan: Pass 1 (keyword) = 0 matches. Pass 2 (brand-name "magnussen") = 0 matches. Pass 1b (non-person entity) = 0 flags across 18 rep names. All rep names are plausible person names.
- VM-45: Skipped — no portal_orders data (no ERP denominator).
- Inventory staleness: inventories entity last updated 2025-08-07 (256 days stale). Data exists (22 rows) but is extremely stale. Q-37 results should be caveated — inventory snapshot is 8+ months old.
- Q-10: mobile_sites table returned 0 rows for org_id=184. Feature enablement flags not available from Postgres; BigQuery org_summary used instead.
- Rep name normalization: No whitespace issues, no case-insensitive duplicates, no mangled names detected across 18 rep names in Q-01 Step 2 results.
