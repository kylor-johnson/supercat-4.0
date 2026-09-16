# Gate Flags — Fine Art Handcrafted Lighting (fal, org_id=241)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | false | org_summary.has_clicky_portal = false |
| HAS_CART | false | recurring_services = "eCat (iPad) - Add'l Seats;eCat (iPad) Service" — no B2B Cart; 0 server orders in LTM |
| HAS_PORTAL_ORDERS | false | portal_order_count LTM = 0; portal_orders entity exists but no LTM rows |
| HAS_INVENTORY | false | inventories row count = 0 |
| HAS_SALES_DATA | false | sales_data row count = 0 |
| HAS_SALES_SECTION | true | 27 qualifying reps (≥10 iPad orders LTM) — threshold = 5 |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv contains fal row; run_date = 2026-04-14 (6 days old) |
| BENCHMARK_ELIGIBLE | True | benchmark_eligible = True in peer CSV |
| BENCHMARK_CONFIDENCE | high | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 18 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Lighting / iPad-only | Source for plain-language cohort framing |
| CLICKY_PREFIX | N/A | HAS_CLICKY = false |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | N/A | HAS_PORTAL_ORDERS = false — VM-45 precondition not met |
| VM45_GATE_2 | N/A | HAS_PORTAL_ORDERS = false — VM-45 precondition not met |
| VM45_RENDER | false | HAS_PORTAL_ORDERS = false — no ERP denominator available |
| QUALIFYING_REP_COUNT | 27 | Reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 59 rows |
| SHOWROOM_EXCLUSIONS | 0 | Pass 1 (keyword scan): 0 matches. Pass 2 (brand-name "Fine Art"): 0 matches. See showroom_scan_results.md |

## Org Identity

- **Client name**: Fine Art Handcrafted Lighting
- **Shortname**: fal
- **Org ID**: 241
- **Bundle**: iPad-only
- **Bundle label for report**: eCat iPad App
- **Vertical**: Lighting
- **Segment**: Platform-Embedded (internal only — never in delivered output)
- **ARR**: $16,975
- **Feature depth**: 6
- **Recurring services**: eCat (iPad) - Add'l Seats; eCat (iPad) Service

## Validation Log

- portal_orders: Entity exists but LTM count = 0 — HAS_PORTAL_ORDERS overridden to false. Q-16 and VM-45 skipped.
- Showroom scan: Both passes returned 0 matches. No exclusions applied. Note: "Dunn Lighting" appears as a rep name in Q-01 Step 2 (15 orders, $283,675 GMV). Name resembles a company but no corroborating evidence of showroom/operational pattern — classified as ambiguous, flagged for CSM review.
- VM-45: Skipped — HAS_PORTAL_ORDERS = false (no ERP denominator).
- mobile_sites: No row found for org_id = 241. Q-10 returned empty. Feature flags derived from org_summary instead.
- Seat utilization: 18 active org_users, 42 logged in 90d, 27 ordering 90d. Logged-in count exceeds active org_users — likely includes users accessing via non-org_user paths.
