# Gate Flags — Currey & Company (cci, org_id=161)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | false | org_summary.has_clicky_portal = false; clicky_prefix = null |
| HAS_CART | false | recurring_services does not contain "eCat Online - B2B Cart"; enable_online_ordering = false; 0 server-source orders LTM |
| HAS_PORTAL_ORDERS | true | 56,705 LTM portal_orders; 156,303 all-time |
| HAS_INVENTORY | true | 3,488 inventory rows |
| HAS_SALES_DATA | true | 101,939 sales_data rows |
| HAS_SALES_SECTION | true | 35 qualifying reps (≥10 iPad orders LTM) |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv present (3 days old); org row confirmed |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in CSV |
| BENCHMARK_CONFIDENCE | medium | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 5 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Lighting / iPad+Catalog+Portal | Source for plain-language cohort framing |
| CLICKY_PREFIX | N/A | HAS_CLICKY = false |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | PASS | erp_gmv ($83,767,399.62) > ecat_gmv ($8,280,273.85) — denominator is total business |
| VM45_GATE_2 | PASS | ecat_gmv ($8.28M) = 9.9% of erp_gmv — above 5% threshold |
| VM45_RENDER | true | Both gates pass — render capture rate subsection |
| QUALIFYING_REP_COUNT | 35 | Number of reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 73 rows |
| SHOWROOM_EXCLUSIONS | 3 | See showroom_scan_results.md for names + evidence |

## Org Identity

- **Client name**: Currey & Company
- **Shortname**: cci
- **Org ID**: 161
- **Bundle**: iPad+Catalog+Portal
- **Bundle label for report**: iPad App + Online Product Catalog + Sales Intelligence Dashboard
- **Vertical**: Lighting
- **Segment (internal only)**: Platform-Embedded
- **ARR**: $26,420
- **Feature depth**: 5
- **Active products**: 6,099
- **Total ERP customers**: 38,665
- **Active users**: 72
- **eCat orders LTM**: 3,951
- **eCat GMV LTM**: $8,280,273.85
- **Portal order items available**: true (285,104 rows)

## Validation Log

- portal_orders: LTM count = 56,705; HAS_PORTAL_ORDERS = true. ERP GMV LTM = $83,767,399.62.
- Showroom scan: 3 confirmed showroom accounts (CC Dallas Showroom: 387 orders / $685,647; Atlanta Showroom: 119 orders / $356,944; Highpoint Showroom: 9 orders / $76,281). Total showroom GMV = $1,118,872. All confirmed by keyword "Showroom" in rep name + city/location patterns. Exclude from individual rep leaderboard analysis.
- VM-45: Both gates pass. eCat GMV capture rate = 9.9% of ERP total. Posture: Enablement-heavy.
- Brand-name showroom scan (Currey): 0 additional matches.
- Q-42: New items flagged (354 items) but all show $0 ERP sales — sales_data may not cover new item period. Note for section builder.
- Territory codes format: JSON-array (e.g., '["ROBB"]'). Used JSON path for Q-43.
- All 73 Mixpanel users returned. Q-01 join surface confirmed.
