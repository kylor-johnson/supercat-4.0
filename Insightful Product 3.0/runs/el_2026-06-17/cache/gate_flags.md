# Gate Flags — Eurofase Inc. (el, org_id=152)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=765, portal_order_gmv=$4.1M |
| HAS_INVENTORY | True | inventory_count=2122 |
| HAS_SALES_DATA | True | sales_data_count=18706 |
| HAS_SALES_SECTION | True | qualifying_reps=5 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Commerce-Active |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | el_eol_portal |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$4.1M > ecat_gmv=$1.6M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 5 | 5 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 164 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 214, Mixpanel total submit_order (Q-01): 354 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=86.6%, ambiguous_rate=17.6%, showroom_event_share=90.1% |
| USER_GROUP_JOIN_RATE | 87% | 142 of 164 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 90% | showroom+admin share of matched events: 90.1% |
| ADMIN_REPS_IN_LEADERBOARD | True | 50 admin/showroom users in leaderboard: Anthony Interlandi, Matthew Chu, Richard Caputi, Sara Romano, Val Khe |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=74 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=361 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=235 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Eurofase Inc.
- **Shortname**: el
- **Org ID**: 152
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- (none)