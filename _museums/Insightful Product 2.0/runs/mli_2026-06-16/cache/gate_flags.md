# Gate Flags — Interlude Furniture (mli, org_id=107)
- **Run date**: 2026-06-16
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False |
| HAS_PORTAL_ORDERS | True | portal_order_count=1382, portal_order_gmv=$7.8M |
| HAS_INVENTORY | True | inventory_count=386 |
| HAS_SALES_DATA | True | sales_data_count=1776 |
| HAS_SALES_SECTION | True | qualifying_reps=22 (threshold: >=5) |
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
| VM45_GATE_1 | FAIL | erp_gmv=$7.8M > ecat_gmv=$10.1M: False |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 22 | 22 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 91 rows |
| SHOWROOM_EXCLUSIONS | 1 | 1 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 1961, Mixpanel total submit_order (Q-01): 102 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=4.4%, ambiguous_rate=0.0%, showroom_event_share=100.0% |
| USER_GROUP_JOIN_RATE | 4% | 4 of 91 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 100% | showroom+admin share of matched events: 100.0% |
| ADMIN_REPS_IN_LEADERBOARD | True | 5 admin/showroom users in leaderboard: David Boggus, Jim Becker, NYSR2 New York, Sean McFadden, Tommy Ivy |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=29 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=586 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | False | new_item_count=0 |
| HAS_BUYER_DATA | True | distinct_buyers_6mo=181 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Interlude Furniture
- **Shortname**: mli
- **Org ID**: 107
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- VM-45 skipped: Gate1=FAIL, Gate2=PASS