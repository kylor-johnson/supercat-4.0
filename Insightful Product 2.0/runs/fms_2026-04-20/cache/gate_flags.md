# Gate Flags — Visual Comfort - Studio /Fans (fms, org_id=108)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary.has_clicky_portal = true; clicky_prefix = fms_ecat_online; table confirmed in clicky_analytics. Note: portal traffic is near-zero (1 visitor/day sporadically) |
| HAS_CART | false | recurring_services = "eCat (iPad) Service" only; no B2B Cart; 0 server-source orders confirmed |
| HAS_PORTAL_ORDERS | false | portal_order_count = 0 (Postgres confirmed); override from org_summary |
| HAS_INVENTORY | true | 8,765 inventory rows |
| HAS_SALES_DATA | true | 204,415 sales_data rows |
| HAS_SALES_SECTION | true | 23 qualifying reps with ≥10 iPad orders LTM |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv (6 days old, within 90-day threshold) |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in CSV |
| BENCHMARK_CONFIDENCE | high | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 18 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Lighting / iPad-only | Source for plain-language cohort framing |
| CLICKY_PREFIX | fms_ecat_online | Confirmed via table listing |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | N/A | HAS_PORTAL_ORDERS = false; no denominator available |
| VM45_GATE_2 | N/A | HAS_PORTAL_ORDERS = false; no denominator available |
| VM45_RENDER | false | HAS_PORTAL_ORDERS = false — Q-45 skipped entirely |
| QUALIFYING_REP_COUNT | 23 | Reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 146 rows |
| SHOWROOM_EXCLUSIONS | 5 | Visual Comfort1 (9 orders, $49,180 GMV), Visual Comfort2 (1 order, $2,914), Visual Comfort4 (1 order, $2,754), Visual Comfort5 (1 order, $14,693), Visual Comfort6 (2 orders, $2,266). All numbered corporate accounts — exclude from rep leaderboard. See showroom_scan_results.md. |

## Org Identity

- **Client name**: Visual Comfort - Studio /Fans
- **Shortname**: fms
- **Org ID**: 108
- **Bundle**: iPad-only
- **Bundle label for report**: eCat iPad App
- **Vertical**: Lighting
- **Segment (internal only)**: Platform-Embedded
- **ARR**: $12,271.50
- **Feature depth**: 6

## Minimum Commerce Gate

- **LTM eCat orders**: 1,255
- **LTM ERP orders**: 0
- **All-time eCat orders**: 16,957
- **Last eCat order**: 2026-04-20 (today)
- **LTM eCat GMV**: $3,723,403.16

## Validation Log

- portal_orders: portal_order_count = 0 in Postgres. org_summary does not flag has_portal. HAS_PORTAL_ORDERS = false. Q-16, Q-18 Part B, Q-45, Q-49 skipped.
- portal_order_items: count = 0. Q-38a skipped.
- Showroom scan: 5 "Visual Comfort[N]" numbered accounts identified via Q-01 Step 2 / Q-06 cross-reference. Keyword scan (Pass 1) returned 0 results. Brand-name scan (Pass 2) returned 0 results. These accounts were detected via rep name pattern in order results. All confirmed as corporate/operational accounts (numbered naming convention, no individual person names). Total excluded GMV: $71,806.92 across 14 orders.
- VM-45: Skipped — no portal_orders denominator.
- Q-42 (New Items): No products flagged new_item = true. Data-gated for this org.
- Q-43 (Territory): Territory codes are JSON-array format (e.g., '["271947"]'). Used JSON path. Territory names table (territories) has no matching entries for this org — territory_name = NULL for all codes. Territory gap analysis still valid using numeric codes.
- Clicky: has_clicky_portal = true but portal traffic is near-zero. Max 1 unique visitor per day, scattered across a few days per month. Clicky data will be cached but §6 Portal Engagement section may be thin.
