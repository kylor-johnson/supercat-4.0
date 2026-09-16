# Gate Flags — Kuzco Lighting Inc. (kll, org_id=166)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary.has_clicky_portal = true; confirmed table `kuzco_kll_eol_daily_metrics` exists |
| HAS_CART | true | recurring_services contains "eCat Online - B2B Cart" + 139 server orders LTM confirmed |
| HAS_PORTAL_ORDERS | true | 91,777 LTM portal_orders; 119,805 all-time |
| HAS_INVENTORY | true | 4,786 inventory rows |
| HAS_SALES_DATA | false | 0 sales_data rows |
| HAS_SALES_SECTION | false | 4 qualifying reps (≥10 iPad orders LTM); threshold is 5 |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv present (3 days old); org row confirmed |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in peer CSV |
| BENCHMARK_CONFIDENCE | high | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 8 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Lighting / Full | Source for plain-language cohort framing |
| CLICKY_PREFIX | kuzco_kll_eol | Confirmed via INFORMATION_SCHEMA |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | PASS | erp_gmv ($70,652,229.06) > ecat_gmv ($887,099.91) |
| VM45_GATE_2 | FAIL | ecat_gmv ($887,099.91) < 5% of erp_gmv ($3,532,611.45); eCat = 1.3% of ERP — not interpretable |
| VM45_RENDER | false | Gate 2 failed — skip capture rate subsection |
| QUALIFYING_REP_COUNT | 4 | Reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | org_feature_usage_report returned 1 row for kll (117 total users, 78,129 total events) |
| SHOWROOM_EXCLUSIONS | 1 | "Kuzco Showroom" — see showroom_scan_results.md |
| Q38A_DATA_GATED | true | portal_order_items has 217,360 rows but ecat_item_number = NULL for all; no item-level join possible |

## Org Identity

- **Client name**: Kuzco Lighting Inc.
- **Shortname**: kll
- **Org ID**: 166
- **Bundle**: Full (iPad + Catalog + Cart + Portal)
- **Bundle label for report**: iPad App, Online Catalog, B2B Cart, and Sales Portal
- **Vertical**: Lighting
- **Segment (internal)**: Commerce-Active
- **ARR**: $40,620
- **Feature depth**: 7
- **Created**: 2022-02-28

## Instance Summary

| Metric | Value |
|--------|-------|
| Active products | 6,268 |
| Total ERP customers | 2,765 |
| Active users | 789 |
| eCat orders (LTM) | 268 |
| eCat GMV (LTM) | $887,099.91 |
| Portal orders (all-time) | 119,805 |
| Portal order items | 217,360 |
| Smart Stacks | 20 |
| Shared resources | 69 |
| Import events | 3,748 |
| Login events | 11,837 |

## Validation Log

- **portal_orders**: LTM count = 91,777; entity is active; HAS_PORTAL_ORDERS = true confirmed. order_origin = 'ECAT' returns 0 across all months — ERP sync does not tag eCat-originated orders.
- **Showroom scan**: 1 confirmed showroom account ("Kuzco Showroom") — 11 orders, $112,926 GMV. Keyword "Showroom" in rep_last_name + brand name "Kuzco" in rep_first_name = confirmed operational account. Exclude from rep leaderboard only.
- **VM-45**: Gate 2 FAIL — eCat GMV ($887K) is 1.3% of ERP GMV ($70.7M). Capture rate not interpretable at this ratio. Skip Q-45.
- **Q-38a**: portal_order_items present (217,360 rows) but ecat_item_number is NULL for all rows — no item-level matching possible. Q-38a data-gated.
- **Q-07 note**: Catalog shows 0% completeness due to 6,268/6,268 products with missing net_price. Only 184/6,268 have missing images. Likely org does not use net_price field (price managed externally or at order level). Section builder should note price field is unpopulated rather than interpreting as incomplete catalog.
- **Q-09 import errors**: Recent customer imports (2026-04-08) show validation errors for customer INC-K0001250 (address too long). Portal order/invoice imports show EOF warnings. No :fatal errors observed.
