# Gate Flags — Geo Contemporary (gcl, org_id=231)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | False | portal_order_count=0, portal_order_gmv=$0 |
| HAS_INVENTORY | False | inventory_count=0 |
| HAS_SALES_DATA | False | sales_data_count=0 |
| HAS_SALES_SECTION | False | mode=none order_reps=2 engagement_reps=4 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Commerce-Active |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | N/A |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | SKIP |  |
| VM45_GATE_2 | SKIP |  |
| VM45_RENDER | False |  |
| QUALIFYING_REP_COUNT | 2 | 2 |
| ENGAGEMENT_REP_COUNT | 4 | engagement_reps=4 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | none | none |
| MIXPANEL_USER_DATA_PRESENT | False | Q-01 Step 1 not executed |
| SHOWROOM_EXCLUSIONS | 0 |  |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 248, Mixpanel submit_order (Q-22): 393 |
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
| INVENTORY_FRESH | False | inventories last_updated 313d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 14d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=15 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | — | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | PARTIAL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | PARTIAL | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | PARTIAL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Geo Contemporary
- **Shortname**: gcl
- **Org ID**: 231
- **Bundle**: 7
- **Bundle label for report**: 7

## Validation Log

- portal_orders LTM count=0, gmv=0.0 — HAS_PORTAL_ORDERS overridden to false