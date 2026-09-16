# Gate Flags — RENWIL (rw, org_id=248)
- **Run date**: 2026-04-16
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary.has_clicky_portal = true; table `renwil_rw_eol_daily_metrics` confirmed in clicky_analytics |
| HAS_CART | false | recurring_services includes "eCat Online - B2B Cart" but server order count = 0 LTM; enable_online_ordering = false in mobile_sites |
| HAS_PORTAL_ORDERS | false | portal_order_count = 0 (all-time); LTM portal_orders = 0; data_versions shows portal_orders entity last updated 2026-03-13 but 0 rows |
| HAS_INVENTORY | true | 2,048 inventory rows; inventories last updated 2026-04-16 (Fresh) |
| HAS_SALES_DATA | false | 0 rows in sales_data table |
| HAS_SALES_SECTION | true | 44 qualifying reps with ≥10 iPad orders LTM (threshold: 5) |
| HAS_PEER_DATA | true | Org present in peer_benchmark_2026-04-14.csv; run_date 2 days ago (not stale) |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in peer benchmark CSV |
| BENCHMARK_CONFIDENCE | low | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier2 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 14 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Home & Decor / Housewares / Art Manufacturers | Source for plain-language cohort framing |
| CLICKY_PREFIX | renwil_rw_eol | Confirmed via INFORMATION_SCHEMA.TABLES lookup |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | N/A | HAS_PORTAL_ORDERS = false; no ERP GMV denominator available |
| VM45_GATE_2 | N/A | HAS_PORTAL_ORDERS = false; no ERP GMV denominator available |
| VM45_RENDER | false | Skipped — portal_orders = 0; no denominator for capture rate |
| QUALIFYING_REP_COUNT | 44 | Number of reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 86 rows from user_feature_usage_report |
| SHOWROOM_EXCLUSIONS | 1 | "Test Sales Portal" — 1 order, $313.19 GMV; see showroom_scan_results.md |

## Org Identity

- **Client name**: RENWIL
- **Shortname**: rw
- **Org ID**: 248
- **Bundle**: iPad+Catalog+Portal
- **Bundle label for report**: iPad + Online Catalog + Sales Portal
- **Segment (internal)**: Platform-Embedded
- **ARR**: $28,249.04
- **Feature depth**: 7
- **Created**: 2024-11-07

## Validation Log

- portal_orders: org_summary reports has_portal = true but portal_order_count = 0 (all-time). data_versions shows portal_orders entity last updated 2026-03-13 but table contains 0 rows. HAS_PORTAL_ORDERS overridden to false. Q-16 and VM-45 skipped.
- HAS_CART: recurring_services includes "eCat Online - B2B Cart" but enable_online_ordering = false in mobile_sites and server order count = 0. HAS_CART set to false per SKILL.md rule.
- HAS_SALES_DATA: 0 rows. Q-37, Q-39, Q-42 skipped.
- Showroom scan: Pass 1 found "Test Sales Portal" (1 order, $313.19) — confirmed test account, excluded from rep leaderboard. Pass 2 (brand name "RENWIL") returned 0 results. Note: Mixpanel user "torontoshowroom" (693 submit_order events, 9,387 total events) and customer "TORONTOSHOWROOM" / "Renwil Showroom" ($296,541 GMV, 17 orders) identified as showroom/internal account — flagged for CSM review. Orders from this customer remain in total org GMV.
- VM-45: Not executed — HAS_PORTAL_ORDERS = false, no denominator available.
- Import health: Recent imports show :warning entries (product not found for ~10 item codes) but no :error or :fatal. Pipeline healthy.
- Q-43 territory format: JSON array confirmed (e.g., `["MONTREALSHOWROO"]`). Territories table has 0 name mappings — territory_name is NULL for all codes. Territory codes are rep-name-based (e.g., SHERYLLOWE, ROBTROTTIER).
