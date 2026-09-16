# Gate Flags — Palecek  (pf, org_id=32)
- **Run date**: 2026-06-15
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=1878, portal_order_gmv=$11.2M |
| HAS_INVENTORY | True | inventory_count=1490 |
| HAS_SALES_DATA | True | sales_data_count=56405 |
| HAS_SALES_SECTION | True | qualifying_reps=31 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | palecek_eol_trial |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | FAIL | erp_gmv=$11.2M > ecat_gmv=$18.9M: False |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 31 | 31 |
| MIXPANEL_USER_DATA_PRESENT | False | Q-01 Step 1 returned 0 rows |
| SHOWROOM_EXCLUSIONS | 6 | 6 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 2745, Mixpanel total submit_order (Q-01): 4714 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=86.6%, ambiguous_rate=19.0%, showroom_event_share=5.2% |
| USER_GROUP_JOIN_RATE | 87% | 142 of 164 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 5% | showroom+admin share of matched events: 5.2% |
| ADMIN_REPS_IN_LEADERBOARD | True | 4 admin/showroom users in leaderboard: Ingrid Sadler, Kayla Lucero, Patrick Phillips, Pat Sexson |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=3 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=78 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=1142 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | PARTIAL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Palecek 
- **Shortname**: pf
- **Org ID**: 32
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- VM-45 skipped: Gate1=FAIL, Gate2=PASS