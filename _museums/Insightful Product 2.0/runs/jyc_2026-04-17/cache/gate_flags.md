# Gate Flags — Jamie Young Company (jyc, org_id=76)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary.has_clicky_portal = true; clicky_prefix = jamie_young_jyc_ecat_online; daily_metrics table confirmed |
| HAS_CART | true | recurring_services contains "eCat Online - B2B Cart"; server_order_count = 3,881 LTM |
| HAS_PORTAL_ORDERS | true | portal_order_count = 546 LTM; portal_gmv = $2,636,663.36 LTM |
| HAS_INVENTORY | true | inventory_count = 1,320 rows |
| HAS_SALES_DATA | true | sales_data_count = 40,798 rows |
| HAS_SALES_SECTION | true | 35 qualifying reps with ≥10 iPad orders LTM |
| HAS_PEER_DATA | true | jyc present in segment_peer_comparison; segment = Platform-Embedded; peer_standing = Top Performer |
| BENCHMARK_ELIGIBLE | true | Present in segment_peer_comparison with peer_standing = Top Performer |
| BENCHMARK_CONFIDENCE | high | Internal only — not in delivered HTML. 2 monthly snapshots available (Mar + Apr 2026); n=47 orgs in segment. |
| PEER_GROUP_LEVEL | segment | Internal only — not in delivered HTML |
| PEER_GROUP_N | 47 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Platform-Embedded | Source for plain-language cohort framing |
| CLICKY_PREFIX | jamie_young_jyc_ecat_online | Confirmed via INFORMATION_SCHEMA |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | FAIL | eCat GMV ($8,028,945.96) exceeds ERP GMV ($2,636,663.36) — ERP sync is partial; denominator is not total business |
| VM45_GATE_2 | N/A | Gate 1 failed — Gate 2 not evaluated |
| VM45_RENDER | false | Gate 1 failed — skip Q-45 capture rate subsection |
| QUALIFYING_REP_COUNT | 35 | 35 reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 92 rows from user_feature_usage_report |
| SHOWROOM_EXCLUSIONS | 1 | "Jamie Young  Company" — confirmed operational/brand-name account. See showroom_scan_results.md |

## Org Identity

- **Client name**: Jamie Young Company
- **Shortname**: jyc
- **Org ID**: 76
- **Bundle**: Full (iPad + Catalog + Cart + Portal)
- **Bundle label for report**: Full Platform — iPad App, Online Catalog, B2B Cart, Sales Portal
- **Segment**: Platform-Embedded (internal only)
- **ARR**: $35,725
- **Feature depth**: 6

## Validation Log

- portal_orders: LTM count = 546, GMV = $2,636,663.36. HAS_PORTAL_ORDERS = true. Note: eCat GMV ($8.03M) exceeds ERP GMV ($2.64M) — indicates partial ERP sync. portal_orders does not represent total business for this org.
- Showroom scan: 1 confirmed exclusion — "Jamie Young  Company" (186 iPad orders, $1,017,380.12 GMV). Brand name as rep_first_name with double-space formatting. Excluded from individual rep leaderboard; included in total org eCat GMV.
- VM-45: Skipped — Gate 1 FAIL. eCat GMV exceeds ERP GMV. ERP sync is partial for this org.
- Q-43 territory format: JSON-array format confirmed (e.g., `["A&A", "JA", "AC", "JA"]`). Using JSON path for territory queries.
- Q-42 new_item: 149 new items flagged in catalog. HAS_SALES_DATA = true. Q-42 executed.
