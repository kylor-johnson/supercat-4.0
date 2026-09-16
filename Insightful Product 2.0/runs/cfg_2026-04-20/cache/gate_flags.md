# Gate Flags — Charleston Forge (cfg, org_id=83)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary.has_clicky_portal = true; charleston_forge_eol_daily_metrics table confirmed in clicky_analytics |
| HAS_CART | true | enable_online_ordering = true; 240 server orders confirmed LTM |
| HAS_PORTAL_ORDERS | false | portal_order_count = 0; LTM portal orders = 0 |
| HAS_INVENTORY | false | inventory_count = 0 |
| HAS_SALES_DATA | false | sales_data_count = 0 |
| HAS_SALES_SECTION | true | 10 qualifying reps with ≥10 iPad orders LTM |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv present (6 days old) |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in CSV |
| BENCHMARK_CONFIDENCE | low | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier3 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 8 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | iPad+Catalog+Cart | Source for plain-language cohort framing |
| CLICKY_PREFIX | charleston_forge_eol | Confirmed via INFORMATION_SCHEMA |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | N/A | HAS_PORTAL_ORDERS = false — Q-45 not applicable |
| VM45_GATE_2 | N/A | HAS_PORTAL_ORDERS = false — Q-45 not applicable |
| VM45_RENDER | false | HAS_PORTAL_ORDERS = false — no denominator available |
| QUALIFYING_REP_COUNT | 10 | Reps: Erica Reece (73), Dan Minor (49), Stephen Bowles (37), Danielle Green (18), Ron Adelman (15), John Wells (14), Kelly Gwaltney (11), Joan Harrison (11), Randy Gould (10), Douglas Hall (10) |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 47 rows |
| SHOWROOM_EXCLUSIONS | 0 | No keyword or brand-name matches found |

## Org Identity

- **Client name**: Charleston Forge
- **Shortname**: cfg
- **Org ID**: 83
- **Bundle**: iPad+Catalog+Cart
- **Bundle label for report**: iPad + Online Catalog + B2B Cart

## Validation Log

- portal_orders: portal_orders entity exists (data_versions shows last update 2026-03-13) but portal_order_count = 0 and LTM portal orders = 0 — HAS_PORTAL_ORDERS overridden to false. Q-16 and VM-45 skipped.
- Showroom scan: Pass 1 (keyword) returned 0 matches. Pass 2 (brand name "Charleston") returned 0 matches. No exclusions applied.
- VM-45: Skipped — HAS_PORTAL_ORDERS = false, no ERP denominator available.
- Territory codes: JSON array format detected (e.g., '["Swanson"]'). Used JSON path for Q-43. Territory codes are rep last names (not geographic codes). territories table has no matching rows.
