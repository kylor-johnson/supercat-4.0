# Gate Flags — Visual Comfort - Studio /Fans (fms, org_id=108)
- **Run date**: 2026-04-30
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary.has_clicky_portal = true; table fms_ecat_online_daily_metrics confirmed in clicky_analytics |
| HAS_CART | false | recurring_services = "eCat (iPad) Service" — no B2B Cart; server_order_count = 0 |
| HAS_PORTAL_ORDERS | false | portal_order_count = 0 (Postgres); overrides org_summary |
| HAS_INVENTORY | true | inventories row count = 8,764 |
| HAS_SALES_DATA | true | sales_data row count = 204,415 |
| HAS_SALES_SECTION | true | 23 qualifying reps with ≥10 iPad orders LTM (threshold: 5) |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv present; run_date 2026-04-14 (16 days old) |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in CSV |
| BENCHMARK_CONFIDENCE | high | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 18 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Lighting / iPad-only | Source for plain-language cohort framing |
| CLICKY_PREFIX | fms_ecat_online | Confirmed via INFORMATION_SCHEMA |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | N/A | HAS_PORTAL_ORDERS = false — Q-45 skipped entirely |
| VM45_GATE_2 | N/A | HAS_PORTAL_ORDERS = false — Q-45 skipped entirely |
| VM45_RENDER | false | portal_orders = 0; no denominator available |
| QUALIFYING_REP_COUNT | 23 | 23 reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned rows from user_feature_usage_report |
| SHOWROOM_EXCLUSIONS | 5 | Visual Comfort1 (9 orders, $49,180), Visual Comfort2 (1, $2,914), Visual Comfort4 (1, $2,754), Visual Comfort5 (1, $14,693), Visual Comfort6 (2, $2,266) |
| MIXPANEL_ORDER_TRACKING_GAP | false | Postgres LTM orders: 1,226; Mixpanel all-time submit_order: 2,035 |
| USER_GROUP_SPLIT_AVAILABLE | false | All 3 conditions fail: join_rate 87.1% < 90%, ambiguous_rate 10.2% ≠ 0, showroom_event_share 7.1% < 10% |
| USER_GROUP_JOIN_RATE | 87.1% | 128 of 147 Mixpanel users matched to Postgres user group |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 7.1% | Showroom+admin share: 13,879 of 195,819 matched events |

## Org Identity

- **Client name**: Visual Comfort - Studio /Fans
- **Shortname**: fms
- **Org ID**: 108
- **Bundle**: iPad-only
- **Bundle label for report**: eCat iPad App
- **Vertical**: Lighting
- **Segment (internal only)**: Platform-Embedded

## Instance Summary

- Active products: 10,430
- Total ERP customers: 5,299
- Active users (org_users, not disabled): 156
- eCat orders LTM: 1,226
- eCat GMV LTM: $3,659,968.31
- Portal orders: 0
- Portal order items: 0
- Sales data rows: 204,415
- Inventory rows: 8,764
- Smart Stacks: 30
- Shared resources: 140
- Import events: 13,106
- Login events: 26,740

## Validation Log

- portal_orders: org_summary reports has_portal=false, Postgres confirms portal_order_count=0. HAS_PORTAL_ORDERS overridden to false. Q-16, Q-18 Part B, Q-45 skipped.
- Showroom scan: Pass 1 (keyword) returned 0 matches. Pass 1b identified 5 Visual Comfort[N] numbered corporate accounts. Pass 2 (brand name) also captured these. All 5 confirmed operational — numbered corporate accounts matching brand-name pattern. Excluded from rep leaderboard.
- VM-45: Skipped — HAS_PORTAL_ORDERS = false. No denominator available.
- Q-42: No products with new_item = true. Q-42 returned empty results.
- Clicky: has_clicky_portal = true, but actual portal traffic is near-zero (≤2 visitors/day, mostly 0). Portal barely used. Still included in section since gate is binary.
- Rep name normalization applied: "John  Chapman" → "John Chapman", "Simar  James" → "Simar James", "Bryon   Woerner" → "Bryon Woerner" (whitespace collapsed), "LESLIE HORRY" → "Leslie Horry" (case normalized)
