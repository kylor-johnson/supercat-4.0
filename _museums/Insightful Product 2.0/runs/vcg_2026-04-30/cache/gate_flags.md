# Gate Flags — Visual Comfort Signature (vcg, org_id=141)
- **Run date**: 2026-04-30
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | false | org_summary.has_clicky_portal = false |
| HAS_CART | false | No "eCat Online - B2B Cart" in recurring_services; server_order_count = 0 LTM |
| HAS_PORTAL_ORDERS | false | portal_order_count LTM = 0 (portal_orders entity exists but LTM count = 0) |
| HAS_INVENTORY | true | inventory_count = 13,090 |
| HAS_SALES_DATA | true | sales_data_count = 193,205 |
| HAS_SALES_SECTION | true | 15 qualifying reps with ≥10 iPad orders LTM |
| HAS_PEER_DATA | true | CSV 2026-04-14 (16 days old, not stale) |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in peer_benchmark_2026-04-14.csv |
| BENCHMARK_CONFIDENCE | high | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 18 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Lighting / iPad-only | Source for plain-language cohort framing |
| CLICKY_PREFIX | N/A | HAS_CLICKY = false |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | N/A | HAS_PORTAL_ORDERS = false — Q-45 not applicable |
| VM45_GATE_2 | N/A | HAS_PORTAL_ORDERS = false — Q-45 not applicable |
| VM45_RENDER | false | HAS_PORTAL_ORDERS = false — no denominator available |
| QUALIFYING_REP_COUNT | 15 | 15 reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 81+ rows |
| SHOWROOM_EXCLUSIONS | 3 | Visual Comfort1 ($36,218.80), Visual Comfort2 ($7,955.45), Visual Comfort6 ($9,964.20) — see showroom_scan_results.md |
| MIXPANEL_ORDER_TRACKING_GAP | false | Postgres LTM iPad orders: 754, Mixpanel total submit_order: 265 |
| USER_GROUP_SPLIT_AVAILABLE | false | Pending join-rate computation — Q-01 Step 1 output large; user group mapping produced |
| USER_GROUP_JOIN_RATE | — | Requires cross-reference of Q-01 Step 1 usernames against Postgres user mapping |
| USER_GROUP_SHOWROOM_EVENT_SHARE | — | Requires cross-reference computation |

## Org Identity

- **Client name**: Visual Comfort Signature
- **Shortname**: vcg
- **Org ID**: 141
- **Bundle**: iPad-only (per peer benchmark classification)
- **Bundle label for report**: eCat iPad App
- **Vertical**: Lighting
- **Segment (internal only)**: Commerce-Active
- **Recurring services**: eCat (iPad) Service; eCat (iPad) - Add'l Seats; eCat Online service

## Validation Log

- portal_orders: portal_orders entity exists but LTM count = 0 — HAS_PORTAL_ORDERS overridden to false. Q-16, Q-18 Part B, and Q-45 skipped.
- Showroom scan: Pass 1 (keyword scan) returned 0 matches. Pass 2 (brand-name scan) returned 0 matches. Pass 1b (non-person entity scan) flagged 3 accounts: Visual Comfort1, Visual Comfort2, Visual Comfort6 — numbered corporate accounts matching {{BRAND_NAME}}[0-9]+ pattern. All confirmed operational via user_group_mapping (Sales Staff group, not individual person names). Excluded from rep leaderboard.
- VM-45: Skipped — HAS_PORTAL_ORDERS = false, no ERP denominator available.
- Q-10 (mobile_sites): mobile_sites table returned 0 rows for org_id=141. Feature enablement derived from org_summary recurring_services instead.
- territories table: 0 rows. Q-43 territory code-to-name lookup not available; territory codes present on customers in JSON format. Territory gap analysis uses codes only.
- Rep name normalization: "Simar  James" → "Simar James" (double space collapsed). "Bryon   Woerner" → "Bryon Woerner" (triple space collapsed). "LESLIE HORRY" → "Leslie Horry" (case normalized).
