# Gate Flags — Ciana Varaluz LLC (vl, org_id=147)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=2019, portal_order_gmv=$1.4M |
| HAS_INVENTORY | True | inventory_count=775 |
| HAS_SALES_DATA | True | sales_data_count=10634 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=3 engagement_reps=38 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Commerce-Active |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | varaluz_vl_eol |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$1.4M > ecat_gmv=$1.3M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 3 | 3 |
| ENGAGEMENT_REP_COUNT | 38 | engagement_reps=38 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 95 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 116, Mixpanel total submit_order (Q-01): 160 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=84.2%, ambiguous_rate=0.0%, showroom_event_share=100.0% |
| USER_GROUP_JOIN_RATE | 84% | 80 of 95 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 100% | showroom+admin share of matched events: 100.0% |
| ADMIN_REPS_IN_LEADERBOARD | True | 27 admin/showroom users in leaderboard: Angela Smith, CS3 Varaluz, CS4 Varaluz, CS5 Varaluz, CS6 Varaluz |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=36 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=640 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=283 |
| HAS_BUYER_DATA | True | distinct_buyers_6mo=480 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Ciana Varaluz LLC
- **Shortname**: vl
- **Org ID**: 147
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- (none)