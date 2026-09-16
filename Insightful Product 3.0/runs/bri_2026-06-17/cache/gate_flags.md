# Gate Flags — Bulbrite (bri, org_id=222)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | True | recurring_services contains B2B Cart: True |
| HAS_PORTAL_ORDERS | True | portal_order_count=117632, portal_order_gmv=$19.0M |
| HAS_INVENTORY | True | inventory_count=895 |
| HAS_SALES_DATA | True | sales_data_count=45296 |
| HAS_SALES_SECTION | True | qualifying_reps=5 (threshold: >=5) |
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
| VM45_GATE_1 | PASS | erp_gmv=$19.0M > ecat_gmv=$3.5M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 5 | 5 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 107 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 3137, Mixpanel total submit_order (Q-01): 435 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=97.2%, ambiguous_rate=1.0%, showroom_event_share=2.0% |
| USER_GROUP_JOIN_RATE | 97% | 104 of 107 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 2% | showroom+admin share of matched events: 2.0% |
| ADMIN_REPS_IN_LEADERBOARD | False | 0 admin/showroom users in leaderboard |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False | days_since_last_erp_order=9999 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=1309 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=179 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | STRONG | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | STRONG | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Bulbrite
- **Shortname**: bri
- **Org ID**: 222
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- (none)