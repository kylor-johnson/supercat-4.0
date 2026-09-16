# Gate Flags — Gabby (gh, org_id=55)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False |
| HAS_PORTAL_ORDERS | True | portal_order_count=25284, portal_order_gmv=$41.6M |
| HAS_INVENTORY | True | inventory_count=6857 |
| HAS_SALES_DATA | True | sales_data_count=63154 |
| HAS_SALES_SECTION | True | qualifying_reps=38 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | gabby_gh_eol_portal |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | FAIL | erp_gmv=$41.6M > ecat_gmv=$50.2M: False |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 38 | 38 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 95 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 14474, Mixpanel total submit_order (Q-01): 15645 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=68.4%, ambiguous_rate=1.5%, showroom_event_share=3.0% |
| USER_GROUP_JOIN_RATE | 68% | 65 of 95 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 3% | showroom+admin share of matched events: 3.0% |
| ADMIN_REPS_IN_LEADERBOARD | True | 7 admin/showroom users in leaderboard: Ben Erickson, Jonah Tibbs, Richard Bentley, Beau Taylor, Margaret Murray |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False | days_since_last_erp_order=9999 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=31 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=2683 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=27 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | STRONG | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | STRONG | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Gabby
- **Shortname**: gh
- **Org ID**: 55
- **Bundle**: 8
- **Bundle label for report**: 8

## Validation Log

- VM-45 skipped: Gate1=FAIL, Gate2=PASS