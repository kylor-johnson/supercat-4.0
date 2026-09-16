# Gate Flags — RENWIL (rw, org_id=248)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary.has_clicky_portal = true; table `renwil_rw_eol_daily_metrics` confirmed in clicky_analytics |
| HAS_CART | false | recurring_services includes "eCat Online - B2B Cart" but server_order_count = 0 LTM; enable_online_ordering = false in mobile_sites |
| HAS_PORTAL_ORDERS | false | portal_order_count = 0 LTM (data_versions shows portal_orders last updated 2026-03-13, 35 days ago; override to false) |
| HAS_INVENTORY | true | inventory_count = 2,048; last updated 2026-04-17 (0 days, Fresh) |
| HAS_SALES_DATA | false | sales_data_count = 0 |
| HAS_SALES_SECTION | true | 44 qualifying reps with ≥10 iPad orders LTM (threshold = 5) |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv contains rw row; run date 2026-04-14 (3 days old, within 90-day freshness window) |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in peer benchmark CSV |
| BENCHMARK_CONFIDENCE | low | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier2 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 14 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Home & Decor / Housewares / Art Manufacturers | Source for plain-language cohort framing |
| CLICKY_PREFIX | renwil_rw_eol | Confirmed via INFORMATION_SCHEMA.TABLES listing |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | N/A | HAS_PORTAL_ORDERS = false — no ERP denominator available; Q-45 skipped |
| VM45_GATE_2 | N/A | HAS_PORTAL_ORDERS = false — no ERP denominator available; Q-45 skipped |
| VM45_RENDER | false | HAS_PORTAL_ORDERS = false — capture rate subsection skipped |
| QUALIFYING_REP_COUNT | 44 | 44 reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 86 rows from mixpanel.user_feature_usage_report |
| SHOWROOM_EXCLUSIONS | 1 | "Test Sales Portal" — 1 order, $313.19; see showroom_scan_results.md |

## Org Identity

- **Client name**: RENWIL
- **Shortname**: rw
- **Org ID**: 248
- **Bundle**: iPad+Catalog+Portal
- **Bundle label for report**: iPad + Online Catalog + Sales Portal
- **ARR**: $28,249
- **Segment (internal only)**: Platform-Embedded
- **Feature depth**: 7
- **Vertical**: Home & Decor / Housewares / Art Manufacturers
- **Org created**: 2024-11-07

## Validation Log

- portal_orders: data_versions shows portal_orders last updated 2026-03-13 (35 days). LTM portal_order_count = 0. HAS_PORTAL_ORDERS overridden to false. Q-16, Q-18 Part B, and VM-45 skipped.
- HAS_CART: recurring_services includes "eCat Online - B2B Cart" but mobile_sites.enable_online_ordering = false AND server_order_count = 0 LTM. B2B Cart listed but never activated. HAS_CART = false.
- Showroom scan: Pass 1 found "Test Sales Portal" (1 order, $313.19). Keyword match: "Test" in rep_first_name. Classification: confirmed test account — excluded from rep leaderboard. Pass 2 (brand name "RENWIL"): no matches.
- VM-45: Skipped — HAS_PORTAL_ORDERS = false. No ERP denominator available.
- sales_data: count = 0. Q-37, Q-39, Q-42 skipped. §4 Product & Inventory limited to catalog completeness and inventory metadata.
- portal_order_items: count = 0. Q-38a skipped.
- Q-CI-04: Skipped — requires 2+ monthly peer benchmark snapshots (first available May 2026). Current snapshots: March 2026 + April 2026 available in segment_benchmarks_monthly but growth trajectory not yet meaningful.
- Clicky traffic: Very low volume — avg <2 unique visitors/day across 6 months. Portal engagement section will be data-limited.
- Territory data: territory_codes format is JSON-array (e.g., ["SHERYLLOWE"]). Territories table has no rows matching (territory_name = NULL for all codes). Territory codes are rep-name-based, not geographic.
