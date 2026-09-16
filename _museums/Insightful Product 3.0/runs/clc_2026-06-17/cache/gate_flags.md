# Gate Flags — Capital Lighting Fixture Co. (clc, org_id=40)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=121151, portal_order_gmv=$63.2M |
| HAS_INVENTORY | True | inventory_count=1793 |
| HAS_SALES_DATA | True | sales_data_count=178471 |
| HAS_SALES_SECTION | True | qualifying_reps=7 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | capital_lighting_clc_eol |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$63.2M > ecat_gmv=$1.3M: True |
| VM45_GATE_2 | FAIL | ecat_gmv >= 5% of erp_gmv: False |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 7 | 7 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 94 rows |
| SHOWROOM_EXCLUSIONS | 1 | 1 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 263, Mixpanel total submit_order (Q-01): 883 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=96.8%, ambiguous_rate=4.4%, showroom_event_share=7.5% |
| USER_GROUP_JOIN_RATE | 97% | 91 of 94 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 8% | showroom+admin share of matched events: 7.5% |
| ADMIN_REPS_IN_LEADERBOARD | True | 2 admin/showroom users in leaderboard: Liz Townsend, Tim  Pirkl |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False | days_since_last_erp_order=9999 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=45 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=1272 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=186 |
| HAS_BUYER_DATA | True | distinct_buyers_6mo=1456 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | STRONG | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | STRONG | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Capital Lighting Fixture Co.
- **Shortname**: clc
- **Org ID**: 40
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- VM-45 skipped: Gate1=PASS, Gate2=FAIL