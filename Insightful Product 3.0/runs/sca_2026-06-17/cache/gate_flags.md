# Gate Flags — Shadow Catchers (sca, org_id=90)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | False | portal_order_count=0, portal_order_gmv=$0 |
| HAS_INVENTORY | True | inventory_count=3490 |
| HAS_SALES_DATA | False | sales_data_count=0 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=3 engagement_reps=15 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
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
| QUALIFYING_REP_COUNT | 3 | 3 |
| ENGAGEMENT_REP_COUNT | 15 | engagement_reps=15 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 31 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 412, Mixpanel total submit_order (Q-01): 684 |
| USER_GROUP_SPLIT_AVAILABLE | True | join_rate=96.8%, ambiguous_rate=0.0%, showroom_event_share=70.5% |
| USER_GROUP_JOIN_RATE | 97% | 30 of 31 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 70% | showroom+admin share of matched events: 70.5% |
| ADMIN_REPS_IN_LEADERBOARD | True | 5 admin/showroom users in leaderboard: Mary Davis, Carrie Turelli, Lloyd Chapman, Nate McElwee, Tori  Howard |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False |  |
| PORTAL_REP_DATA_PRESENT | False |  |
| PORTAL_CUSTOMER_DATA_PRESENT | False |  |
| INVENTORY_FRESH | False | inventories last_updated 313d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | False | customers last_updated 264d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=2703 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | LIMITED | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | LIMITED | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | PARTIAL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Shadow Catchers
- **Shortname**: sca
- **Org ID**: 90
- **Bundle**: 4
- **Bundle label for report**: 4

## Validation Log

- portal_orders LTM count=0, gmv=0.0 — HAS_PORTAL_ORDERS overridden to false