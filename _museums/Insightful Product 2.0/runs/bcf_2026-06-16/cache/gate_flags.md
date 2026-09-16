# Gate Flags — Braxton Culler (bcf, org_id=171)
- **Run date**: 2026-06-16
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | True | recurring_services contains B2B Cart: True |
| HAS_PORTAL_ORDERS | True | portal_order_count=1697, portal_order_gmv=$2.5M |
| HAS_INVENTORY | True | inventory_count=1142 |
| HAS_SALES_DATA | True | sales_data_count=15934 |
| HAS_SALES_SECTION | True | qualifying_reps=19 (threshold: >=5) |
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
| VM45_GATE_1 | FAIL | erp_gmv=$2.5M > ecat_gmv=$7.0M: False |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 19 | 19 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 74 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 2712, Mixpanel total submit_order (Q-01): 2128 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=83.8%, ambiguous_rate=4.8%, showroom_event_share=7.4% |
| USER_GROUP_JOIN_RATE | 84% | 62 of 74 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 7% | showroom+admin share of matched events: 7.4% |
| ADMIN_REPS_IN_LEADERBOARD | True | 4 admin/showroom users in leaderboard: Matt Sorensen, Carrie Harris, Tina Hoffman, Tom Hoffman |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False | days_since_last_erp_order=9999 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=28 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=354 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=117 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=3 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | STRONG | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | STRONG | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Braxton Culler
- **Shortname**: bcf
- **Org ID**: 171
- **Bundle**: 7
- **Bundle label for report**: 7

## Validation Log

- VM-45 skipped: Gate1=FAIL, Gate2=PASS