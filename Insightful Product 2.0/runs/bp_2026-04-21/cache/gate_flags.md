# Gate Flags — Buster & Punch (bp, org_id=250)
- **Run date**: 2026-04-21
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | false | org_summary.has_clicky_portal = false; clicky_prefix = null |
| HAS_CART | false | enable_online_ordering = true BUT server_order_count = 0 — Cart configured but never activated |
| HAS_PORTAL_ORDERS | false | portal_order_count = 0 (all-time); LTM erp_orders = 0 |
| HAS_INVENTORY | true | inventory_count = 3,417 |
| HAS_SALES_DATA | false | sales_data_count = 0 |
| HAS_SALES_SECTION | false | 0 qualifying reps with ≥10 iPad orders LTM (only 9 total iPad orders LTM across all reps) |
| HAS_PEER_DATA | true | segment_peer_comparison row exists; segment_benchmarks_monthly available |
| BENCHMARK_ELIGIBLE | true | Present in segment_peer_comparison with peer_standing = "Needs Attention" |
| BENCHMARK_CONFIDENCE | standard | Internal only — peers_in_segment = 52 |
| PEER_GROUP_LEVEL | segment | Internal only — grouped by segment = "Commerce-Active" |
| PEER_GROUP_N | 52 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Commerce-Active | Source for plain-language cohort framing |
| CLICKY_PREFIX | N/A | HAS_CLICKY = false |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | N/A | HAS_PORTAL_ORDERS = false — Q-45 skipped entirely |
| VM45_GATE_2 | N/A | HAS_PORTAL_ORDERS = false — Q-45 skipped entirely |
| VM45_RENDER | false | No portal_orders denominator available |
| QUALIFYING_REP_COUNT | 0 | 0 reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | N/A | Q-01 not run (HAS_SALES_SECTION = false) |
| SHOWROOM_EXCLUSIONS | 0 | Showroom scan not run (HAS_SALES_SECTION = false) |
| MIXPANEL_ORDER_TRACKING_GAP | N/A | Q-01 not run (HAS_SALES_SECTION = false) |
| USER_GROUP_SPLIT_AVAILABLE | false | Q-01 not run — user group mapping skipped |
| USER_GROUP_JOIN_RATE | N/A | Skipped |
| USER_GROUP_SHOWROOM_EVENT_SHARE | N/A | Skipped |

## Org Identity

- **Client name**: Buster & Punch
- **Shortname**: bp
- **Org ID**: 250
- **Bundle**: iPad+Catalog+Cart (Cart configured but never activated — 0 server orders)
- **Bundle label for report**: eCat iPad + Online Product Catalog + Online Ordering (inactive)
- **Segment (internal only)**: Commerce-Active
- **Feature depth**: 3
- **ARR**: Not available (null in org_summary)

## Instance Summary

| Metric | Value |
|--------|-------|
| Active products | 2,297 |
| Total ERP customers | 7,084 |
| Active users | 81 |
| eCat orders (LTM) | 9 |
| eCat GMV (LTM) | $36,332.78 |
| All-time eCat orders | 19 |
| Last eCat order | 2026-04-13 |
| Portal orders (all-time) | 0 |
| Portal order items | 0 |
| Sales data rows | 0 |
| Inventory rows | 3,417 |
| Smart stacks | 6 |
| Shared resources | 16 |
| Import events | 1,196 |
| Login events | 3,730 |

## Validation Log

- portal_orders: portal_order_count = 0 all-time. HAS_PORTAL_ORDERS = false. Q-16 and VM-45 skipped.
- Showroom scan: Not run (HAS_SALES_SECTION = false). Note: Q-41 rep-by-rep data shows "Dunn Lighting" as a first-time buyer acquirer — flagged as potential non-person entity for awareness.
- VM-45: Skipped — no portal_orders denominator.
- Q-14: Returned 0 rows — no customers with ≥3 eCat orders in LTM (only 9 total orders across 7 customers).
- Import health: Consistent daily imports running. Inventory imports show recurring warnings (product not found for ~10+ items). Customer imports show recurring :error entries (validation failures — missing shipping address fields).
- Sales section: Only 9 iPad orders LTM across all reps; no rep reaches the ≥10 order threshold. §2 Sales Team Performance will be skipped.
- B2B Cart: enable_online_ordering = true in mobile_sites, but 0 all-time server orders. HAS_CART = false.
