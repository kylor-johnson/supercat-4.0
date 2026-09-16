# Gate Flags — Sarreid, Ltd. (sarreid, org_id=1)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary.has_clicky_portal = true; CLICKY_PREFIX confirmed |
| HAS_CART | false | server_order_count = 0; enable_online_ordering = false; no "B2B Cart" in recurring_services |
| HAS_PORTAL_ORDERS | true | LTM portal_order_count = 10,348 |
| HAS_INVENTORY | true | inventory_count = 5,774 |
| HAS_SALES_DATA | true | sales_data_count = 43,734 |
| HAS_SALES_SECTION | true | 14 qualifying reps with ≥10 iPad orders LTM (threshold: 5) |
| HAS_PEER_DATA | true | Found in segment_peer_comparison and peer_benchmark_2026-04-14.csv |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in peer CSV |
| BENCHMARK_CONFIDENCE | low | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier2 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 32 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Furniture | Source for plain-language cohort framing |
| CLICKY_PREFIX | sarreid_eol_portal | Confirmed via INFORMATION_SCHEMA; alternative schema (title/value) |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | PASS | erp_gmv ($14,474,076.20) > ecat_gmv ($2,748,268.90) |
| VM45_GATE_2 | PASS | ecat_gmv ($2,748,268.90) >= 0.05 × erp_gmv ($723,703.81) |
| VM45_RENDER | true | Both gates pass — render capture rate subsection |
| QUALIFYING_REP_COUNT | 14 | 14 reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 93 rows (Q-04 also returned 93 rows) |
| SHOWROOM_EXCLUSIONS | 1 | "Sarreid Showroom" — 3 orders, $14,192.45 GMV. See showroom_scan_results.md |

## Org Identity

- **Client name**: Sarreid, Ltd.
- **Shortname**: sarreid
- **Org ID**: 1
- **Bundle**: iPad+Catalog+Portal
- **Bundle label for report**: eCat iPad + Online Product Catalog + Sales Intelligence Dashboard
- **Vertical**: Furniture
- **Segment (internal)**: Platform-Embedded
- **ARR**: $22,696
- **Feature depth**: 8

## Validation Log

- portal_orders: LTM count = 10,348; HAS_PORTAL_ORDERS = true. order_origin = 'ECAT' returns 0 for all months — ERP does not tag eCat-originated orders via order_origin field for this org.
- Showroom scan: 1 confirmed exclusion — "Sarreid Showroom" (3 orders, $14,192.45 GMV). Keyword match on "Showroom" in rep_first_name. Brand-name scan also matched same account. Classification: confirmed operational/showroom — exclude from rep leaderboard.
- VM-45: Both gates pass. Capture rate = 19.0% GMV ($2.75M / $14.47M). Posture: "Partial capture; eCat is growing."
- Q-38a: portal_order_items present (61,220 rows) but ecat_item_number is empty for all rows in this org — product-level velocity data not available via this path. Noted in manifest.
- Clicky schema: Alternative schema (title/value) confirmed for regions and traffic_sources tables.
