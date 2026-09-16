# Gate Flags — Hubbardton Forge (hfg, org_id=165)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=22112, portal_order_gmv=$42.2M |
| HAS_INVENTORY | False | inventory_count=0 |
| HAS_SALES_DATA | True | sales_data_count=44983 |
| HAS_SALES_SECTION | True | qualifying_reps=17 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | hubbardton_forge_hfg_eol_portal |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$42.2M > ecat_gmv=$16.8M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 17 | 17 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 137 rows |
| SHOWROOM_EXCLUSIONS | 1 | 1 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 1873, Mixpanel total submit_order (Q-01): 3123 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=86.1%, ambiguous_rate=88.1%, showroom_event_share=3.5% |
| USER_GROUP_JOIN_RATE | 86% | 118 of 137 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 3% | showroom+admin share of matched events: 3.5% |
| ADMIN_REPS_IN_LEADERBOARD | True | 2 admin/showroom users in leaderboard: Shannon Rose, Retha Boles |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=47 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=2589 |
| INVENTORY_FRESH | False | inventories last_updated 300d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=57 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Hubbardton Forge
- **Shortname**: hfg
- **Org ID**: 165
- **Bundle**: 7
- **Bundle label for report**: 7

## Validation Log

- (none)