# Gate Flags — Wildwood/Chelsea House (wwjc, org_id=78)
- **Run date**: 2026-06-16
- **Report mode**: Mode 2: Platform Activation Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | org_summary has_clicky_portal = false |
| HAS_CART | False | recurring_services includes B2B Cart but server_order_count = 0 |
| HAS_PORTAL_ORDERS | False | portal_order LTM count = 0 |
| HAS_INVENTORY | True | inventory_count = 1,559 |
| HAS_SALES_DATA | False | sales_data_count = 0 |
| HAS_SALES_SECTION | False | 0 qualifying reps (0 all-time eCat orders) |
| HAS_PEER_DATA | False |  |
| BENCHMARK_ELIGIBLE | False |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | N/A |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | SKIP | No eCat orders |
| VM45_GATE_2 | SKIP | No eCat orders |
| VM45_RENDER | False |  |
| QUALIFYING_REP_COUNT | 0 |  |
| MIXPANEL_USER_DATA_PRESENT | False |  |
| SHOWROOM_EXCLUSIONS | 0 |  |
| MIXPANEL_ORDER_TRACKING_GAP | False |  |
| USER_GROUP_SPLIT_AVAILABLE | False |  |
| USER_GROUP_JOIN_RATE | N/A |  |
| USER_GROUP_SHOWROOM_EVENT_SHARE | N/A |  |
| ADMIN_REPS_IN_LEADERBOARD | False |  |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False |  |
| PORTAL_REP_DATA_PRESENT | False |  |
| PORTAL_CUSTOMER_DATA_PRESENT | False |  |
| INVENTORY_FRESH | False | inventories last_updated 2026-02-23 (112 days) |
| SALES_DATA_FRESH | False |  |
| CUSTOMER_DATA_FRESH | False | customers last_updated 2026-02-23 (112 days) |
| HAS_COMMITMENT_DATA | False |  |
| HAS_NEW_ITEMS | False |  |
| HAS_BUYER_DATA | False |  |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | — | Section skipped (Mode 2) |
| SECTION_CONFIDENCE_3 | — | Section skipped (Mode 2) |
| SECTION_CONFIDENCE_4 | — | Section skipped (Mode 2) |
| SECTION_CONFIDENCE_5 | — | Section skipped (Mode 2) |

## Org Identity

- **Client name**: Wildwood/Chelsea House
- **Shortname**: wwjc
- **Org ID**: 78
- **Bundle**: eCat (iPad) Service, eCat Online - B2B Cart, eCat Online - Catalog, eCat Online - Portal
- **Bundle label for report**: Full · iPad + eCat Online

## Validation Log

- Mode 2 determined: 0 all-time eCat orders, 0 LTM ERP orders
- portal_orders entity exists (last_updated 2026-03-13) but LTM eCat order count = 0; Mode 2 applies
- Q-22 shows 2,046 submit_order events in Mixpanel but 0 persisted orders in Postgres orders table
