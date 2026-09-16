# Gate Flags — Ratana International Ltd. (ril, org_id=245)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | True | recurring_services contains B2B Cart: True |
| HAS_PORTAL_ORDERS | True | portal_order_count=1738, portal_order_gmv=$17.2M |
| HAS_INVENTORY | True | inventory_count=1514 |
| HAS_SALES_DATA | True | sales_data_count=24377 |
| HAS_SALES_SECTION | True | qualifying_reps=13 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | ratana_ril |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | FAIL | erp_gmv=$17.2M > ecat_gmv=$17.6M: False |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 13 | 13 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 71 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 1256, Mixpanel total submit_order (Q-01): 1973 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=77.5%, ambiguous_rate=76.4%, showroom_event_share=11.9% |
| USER_GROUP_JOIN_RATE | 77% | 55 of 71 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 12% | showroom+admin share of matched events: 11.9% |
| ADMIN_REPS_IN_LEADERBOARD | True | 1 admin/showroom users in leaderboard: Winnie Ng |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=43 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=612 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | False | new_item_count=0 |
| HAS_BUYER_DATA | True | distinct_buyers_6mo=447 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Ratana International Ltd.
- **Shortname**: ril
- **Org ID**: 245
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- VM-45 skipped: Gate1=FAIL, Gate2=PASS