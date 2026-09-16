# Gate Flags — Braxton Culler (bcf, org_id=171)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | false | org_summary.has_clicky_portal = false |
| HAS_CART | true | 1,293 server-submitted orders (order_origin = 'server') LTM |
| HAS_PORTAL_ORDERS | true | 1,612 portal_orders LTM |
| HAS_INVENTORY | true | 1,099 inventory rows for org 171 |
| HAS_SALES_DATA | true | 16,075 sales_data rows for org 171 |
| HAS_SALES_SECTION | true | 20 qualifying reps (≥10 iPad orders LTM) — threshold ≥5 met |
| HAS_PEER_DATA | true | bcf present in peer_benchmark_2026-04-14.csv |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in peer CSV |
| BENCHMARK_CONFIDENCE | medium | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 6 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Furniture / Full | Source for plain-language cohort framing |
| CLICKY_PREFIX | N/A | HAS_CLICKY = false |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | FAIL | ecat_gmv $6,586,775.71 > erp_gmv $2,135,092.84 — ERP sync is partial |
| VM45_GATE_2 | N/A | Gate 1 failed — Gate 2 not evaluated |
| VM45_RENDER | false | Gate 1 failed — render capture rate subsection skipped |
| QUALIFYING_REP_COUNT | 20 | 20 reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 71 rows |
| SHOWROOM_EXCLUSIONS | 0 | No showroom accounts detected in Pass 1 or Pass 2 |

## Org Identity

- **Client name**: Braxton Culler
- **Shortname**: bcf
- **Org ID**: 171
- **Bundle**: Full
- **Bundle label for report**: Full Suite
- **Segment**: Platform-Embedded (internal only)
- **Feature depth**: 7
- **Recurring services**: eCat Online - B2B Cart, eCat Online - Portal

## Validation Log

- portal_orders: 1,612 LTM portal orders confirmed via `SELECT COUNT(*) FROM portal_orders WHERE organization_id = 171 AND created_at >= NOW() - INTERVAL '12 months'`
- Showroom scan: Pass 1 (keyword) and Pass 2 (brand name "Braxton Culler") both returned 0 showroom accounts
- VM-45: Gate 1 FAIL — ecat_gmv ($6,586,775.71) exceeds erp_gmv ($2,135,092.84), indicating partial ERP sync; capture rate would be >100% and is nonsensical
