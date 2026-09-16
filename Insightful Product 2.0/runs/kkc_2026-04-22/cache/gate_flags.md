# Gate Flags — Kindel Karges Furniture (kkc, org_id=99)
- **Run date**: 2026-04-22
- **Report mode**: Mode 3: Platform Reactivation Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | false | `has_clicky_portal = false` in org_summary; `clicky_prefix = null` |
| HAS_CART | false | recurring_services has no "eCat Online - B2B Cart"; all-time server order count = 0 |
| HAS_PORTAL_ORDERS | false | LTM portal_orders count = 0; overriding regardless of org_summary portal flag |
| HAS_INVENTORY | false | `inventories` row count = 0 for org 99 |
| HAS_SALES_DATA | true | `sales_data` row count = 21 |
| HAS_SALES_SECTION | false | LTM eCat orders = 0; qualifying rep count = 0 (no reps with ≥10 iPad orders LTM) |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv — 8 days old (fresh); benchmark_eligible = True |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible column = True in peer_benchmark_2026-04-14.csv |
| BENCHMARK_CONFIDENCE | high | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 16 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Furniture / iPad-only | Source for plain-language cohort framing in §7 |
| CLICKY_PREFIX | N/A | HAS_CLICKY = false |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | N/A | Mode 3 — HAS_PORTAL_ORDERS = false; Q-45 not applicable |
| VM45_GATE_2 | N/A | Mode 3 — HAS_PORTAL_ORDERS = false; Q-45 not applicable |
| VM45_RENDER | false | HAS_PORTAL_ORDERS = false; capture rate section excluded |
| QUALIFYING_REP_COUNT | 0 | LTM eCat orders = 0; no rep has ≥10 iPad orders in trailing 12 months |
| MIXPANEL_USER_DATA_PRESENT | N/A | Mode 3 — Q-01 not run (no LTM order activity) |
| SHOWROOM_EXCLUSIONS | 0 | LTM orders = 0; showroom scan not applicable for Mode 3 |
| MIXPANEL_ORDER_TRACKING_GAP | true | Postgres all-time orders: 41, Q-22 submit_order: 0 |
| USER_GROUP_SPLIT_AVAILABLE | false | HAS_SALES_SECTION = false; Q-01 not run — skip user group mapping |
| USER_GROUP_JOIN_RATE | N/A | Q-01 not run |
| USER_GROUP_SHOWROOM_EVENT_SHARE | N/A | Q-01 not run |

## Org Identity

- **Client name**: Kindel Karges Furniture
- **Shortname**: kkc
- **Org ID**: 99
- **Bundle**: iPad-only (peer benchmark classification); recurring_services includes eCat (iPad) Service, eCat Online - Closed Site, eCat Online - Portal — no B2B Cart
- **Bundle label for report**: iPad + Catalog + Portal (catalog and portal features are listed in recurring_services; no online ordering / B2B Cart)
- **Industry**: Furniture
- **Segment (internal)**: Catalog-Focused
- **ARR**: $11,380
- **Feature depth**: 4
- **Platform since**: 2015-11-03

## Validation Log

- **portal_orders**: org_summary shows `has_portal = true` via recurring_services, but LTM portal_orders count = 0 in Postgres. HAS_PORTAL_ORDERS overridden to false. Q-16 and VM-45 skipped.
- **Showroom scan**: Not applicable for Mode 3 (LTM orders = 0). No exclusions.
- **VM-45**: Not applicable — Mode 3; LTM eCat and ERP orders both = 0.
- **mobile_sites**: No record found for organization_id = 99 in Postgres mobile_sites table. Q-10 feature flag columns (enable_sales_portal, enable_online_catalog, enable_online_ordering) unavailable; counts still obtained via subquery.
- **Mode determination**: LTM eCat orders = 0, LTM ERP orders = 0, all-time eCat orders = 41 → Mode 3 (Reactivation). Last eCat order: 2024-07-02 (~9.7 months lapsed as of run date).
- **Inventory**: inventories row count = 0. §4 Product & Inventory excluded.
- **sales_data**: 21 rows present but not used in Mode 3 sections.
- **Mixpanel order-tracking gap**: Postgres all-time eCat orders = 41, Q-22 submit_order = 0. MIXPANEL_ORDER_TRACKING_GAP = true. Mixpanel is not tracking iPad order submissions for this org. Platform Status and Peer Benchmarking must apply gap handling rules.
- **Q-05 anomaly**: logged_in_90d (23) exceeds active_org_users (14). This is expected — login_events tracks all user_ids that logged in, including users who may have been disabled after their login.
