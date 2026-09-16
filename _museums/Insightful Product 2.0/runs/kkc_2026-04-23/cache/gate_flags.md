# Gate Flags — Kindel Karges Furniture (kkc, org_id=99)
- **Run date**: 2026-04-23
- **Report mode**: Mode 3: Platform Reactivation Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | false | org_summary.has_clicky_portal = false |
| HAS_CART | false | No "eCat Online - B2B Cart" in recurring_services; all-time order_source = ipad only (0 server orders) |
| HAS_PORTAL_ORDERS | false | portal_orders count = 0 (all-time); no ERP-synced orders present |
| HAS_INVENTORY | false | inventories row count = 0 |
| HAS_SALES_DATA | true | sales_data row count = 21 (very small dataset) |
| HAS_SALES_SECTION | false | Mode 3 — no LTM iPad orders; 0 qualifying reps |
| HAS_PEER_DATA | true | kkc present in peer_benchmark_2026-04-14.csv (9 days old, not stale) |
| BENCHMARK_ELIGIBLE | True | benchmark_eligible = True in CSV |
| BENCHMARK_CONFIDENCE | high | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 16 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Furniture / iPad-only | Source for plain-language cohort framing |
| CLICKY_PREFIX | N/A | HAS_CLICKY = false |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | N/A | No portal_orders — VM-45 not applicable |
| VM45_GATE_2 | N/A | No portal_orders — VM-45 not applicable |
| VM45_RENDER | false | No portal_orders present; capture rate cannot be computed |
| QUALIFYING_REP_COUNT | 0 | No LTM iPad orders — Mode 3 (lapsed account) |
| MIXPANEL_USER_DATA_PRESENT | false | Q-01 not run (HAS_SALES_SECTION = false) |
| SHOWROOM_EXCLUSIONS | 0 | Q-01 not run; showroom scan not applicable |
| MIXPANEL_ORDER_TRACKING_GAP | true | Postgres all-time orders: 41, Q-22 submit_order: 0 |
| USER_GROUP_SPLIT_AVAILABLE | false | HAS_SALES_SECTION = false; Q-01 skipped — user group split not computed |
| USER_GROUP_JOIN_RATE | N/A | Q-01 not available |
| USER_GROUP_SHOWROOM_EVENT_SHARE | N/A | Q-01 not available |

## Org Identity

- **Client name**: Kindel Karges Furniture
- **Shortname**: kkc
- **Org ID**: 99
- **Bundle**: iPad-only (per peer benchmark classification)
- **Bundle label for report**: iPad + Online Catalog + Sales Portal
- **Vertical**: Furniture
- **Recurring services**: eCat (iPad) Service; eCat Online - Closed Site; eCat Online - Portal; eCat Online service
- **ARR**: $11,380
- **Segment (internal only)**: Catalog-Focused
- **Created**: 2015-11-03

## Mode 3 Context

- **All-time eCat orders**: 41
- **All-time eCat GMV**: $1,075,190.25
- **Last eCat order date**: 2024-07-02
- **Last active month**: July 2024
- **All-time order channel**: 100% iPad (41 iPad orders, 0 server orders)
- **Months since last activity**: ~9 months

## Validation Log

- portal_orders: 0 rows all-time — HAS_PORTAL_ORDERS set to false. Q-16 and VM-45 skipped.
- mobile_sites: No row returned for org_id=99 — Q-10 feature enablement data unavailable from mobile_sites. Feature flags derived from org_summary.recurring_services instead.
- Showroom scan: Not applicable — Q-01 not run (Mode 3, HAS_SALES_SECTION = false).
- VM-45: Not applicable — no portal_orders present.
- MIXPANEL_ORDER_TRACKING_GAP: TRUE — Postgres records 41 all-time eCat orders but Q-22 shows submit_order = 0. Mixpanel is not tracking iPad order submissions for this org.
- Inventory: data_versions shows inventories entity last updated 2025-08-07 (258 days ago, Stale) but inventories table has 0 rows. Inventory data was imported historically but is now empty.
