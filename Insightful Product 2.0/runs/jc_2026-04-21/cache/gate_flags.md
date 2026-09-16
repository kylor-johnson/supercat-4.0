# Gate Flags — Jonathan Charles Fine Furniture Ltd. (jc, org_id=65)
- **Run date**: 2026-04-21
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | false | org_summary.has_clicky_portal = false; clicky_prefix = null |
| HAS_CART | false | recurring_services = "eCat (iPad) - Add'l Seats;eCat (iPad) Service"; enable_online_ordering = false; server_order_count LTM = 0 |
| HAS_PORTAL_ORDERS | true | portal_order_count LTM = 336; LTM ERP GMV = $4,104,226.33 |
| HAS_INVENTORY | true | inventory_count = 6,641 rows |
| HAS_SALES_DATA | true | sales_data_count = 6,166 rows |
| HAS_SALES_SECTION | false | Only 1 qualifying rep with ≥10 iPad orders LTM (threshold: 5) |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv exists; run_date = 2026-04-14 (7 days old, within 90-day window) |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in CSV |
| BENCHMARK_CONFIDENCE | low | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier2 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 32 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Furniture | Source for plain-language cohort framing |
| CLICKY_PREFIX | N/A | HAS_CLICKY = false |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | PASS | portal_orders_gmv ($4,104,226.33) > ecat_gmv ($1,441,609.33) |
| VM45_GATE_2 | PASS | ecat_gmv ($1,441,609.33) >= 0.05 × portal_orders_gmv ($205,211.32) |
| VM45_RENDER | true | Both gates pass — render capture rate subsection |
| QUALIFYING_REP_COUNT | 1 | 1 rep with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | N/A | Q-01 skipped — HAS_SALES_SECTION = false |
| SHOWROOM_EXCLUSIONS | 0 | Showroom scan skipped — HAS_SALES_SECTION = false |
| MIXPANEL_ORDER_TRACKING_GAP | N/A | Q-01 skipped — HAS_SALES_SECTION = false |
| USER_GROUP_SPLIT_AVAILABLE | false | Q-01 skipped — HAS_SALES_SECTION = false |
| USER_GROUP_JOIN_RATE | N/A | Q-01 skipped |
| USER_GROUP_SHOWROOM_EVENT_SHARE | N/A | Q-01 skipped |

## Org Identity

- **Client name**: Jonathan Charles Fine Furniture Ltd.
- **Shortname**: jc
- **Org ID**: 65
- **Bundle**: iPad+Catalog+Portal
- **Bundle label for report**: iPad App with Online Catalog and Sales Intelligence Dashboard
- **Segment (internal only)**: Commerce-Active
- **Vertical**: Furniture
- **ARR**: $9,660

## Validation Log

- **portal_orders**: LTM count = 336, GMV = $4,104,226.33. HAS_PORTAL_ORDERS = true. All ecat_originated_orders = 0 in Q-16 (order_origin not tagged as 'ECAT' in this org's ERP sync).
- **Showroom scan**: Skipped — HAS_SALES_SECTION = false (only 1 qualifying rep). However, Q-41 rep attribution shows "VFR SALES" (5 new buyers) and "VFR MARKETING" (1 new buyer) — these appear to be operational/showroom-type names, not individual reps. Flagged for CSM awareness.
- **VM-45**: Both gates pass. eCat GMV capture rate = 35.1%. Posture = "Meaningful eCat channel; dual-system".
- **Q-13 data quality note**: customer_num "1" / "Test Customer" appears with 1 order / $14,700 GMV (1.2% of eCat total). Section builder should note or exclude.
- **Q-42 note**: All 21 new_item collections show $0.00 ERP sales — new items have zero sell-through in sales_data. This may reflect timing (items flagged as new but sales_data lacks date granularity) or genuine zero sell-through.
- **eCat activity concentration**: All 40 LTM eCat orders occurred in Oct–Dec 2025. Zero eCat orders in Jan–Apr 2026. Active_3mo = 0. This indicates seasonal/market-event-driven ordering (likely furniture market shows) rather than continuous eCat usage.
