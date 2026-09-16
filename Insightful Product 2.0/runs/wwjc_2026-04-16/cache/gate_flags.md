# Gate Flags — Wildwood/Chelsea House (wwjc, org_id=8)
- **Run date**: 2026-04-16
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | false | org_summary.has_clicky_portal = false; no Clicky tables for wwjc |
| HAS_CART | true | recurring_services contains "eCat Online - B2B Cart" + 4,969 server orders LTM confirmed |
| HAS_PORTAL_ORDERS | true | 14,838 LTM portal_orders confirmed |
| HAS_INVENTORY | true | 3,963 inventory rows |
| HAS_SALES_DATA | true | 98,285 sales_data rows |
| HAS_SALES_SECTION | true | 22 qualifying reps with ≥10 iPad orders LTM |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv contains wwjc row; run date 2 days ago (not stale) |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in peer benchmark CSV |
| BENCHMARK_CONFIDENCE | high | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 8 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Lighting / Full | Source for plain-language cohort framing |
| CLICKY_PREFIX | N/A | HAS_CLICKY = false |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | PASS | ERP GMV ($17,842,870.22) > eCat GMV ($8,956,694.28) — denominator valid |
| VM45_GATE_2 | PASS | eCat GMV ($8,956,694.28) >= 5% of ERP GMV ($892,143.51) — capture rate interpretable |
| VM45_RENDER | true | Both gates pass — render capture rate subsection |
| QUALIFYING_REP_COUNT | 22 | 22 reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 74 users |
| SHOWROOM_EXCLUSIONS | 1 | See showroom_scan_results.md — "Atlanta Showroom" confirmed operational |

## Org Identity

- **Client name**: Wildwood/Chelsea House
- **Shortname**: wwjc
- **Org ID**: 8
- **Bundle**: Full (iPad + Catalog + Cart + Portal)
- **Bundle label for report**: eCat iPad + Online Catalog + B2B Cart + Sales Portal
- **Segment (internal)**: Platform-Embedded
- **ARR**: $40,220
- **Feature depth**: 5

## Validation Log

- portal_orders: 14,838 LTM orders confirmed; org_summary has_portal not checked (column absent) but portal_orders data confirmed directly. HAS_PORTAL_ORDERS = true.
- Showroom scan: Pass 1 found "Atlanta Showroom" (25 orders, $28,110.50 GMV). Pass 2 (brand name "Wildwood") returned no results. Atlanta Showroom confirmed operational — name contains "Showroom", shared-location account pattern.
- VM-45: Both gates pass. eCat GMV capture rate = 50.2%. Posture = "Primary transaction system."
- Q-42 (New Item Performance): Only 1 new_item = true product found with ERP sales ($95.20). Minimal new item data — section agent should note sparse data.
- Import health: Most recent inventory import (2026-04-17) has ~200+ warnings for "Product not found, record ignored" — item codes in inventory file not matching products table. No :error or :fatal entries. Warnings only, pipeline healthy.
- Q-16 ERP total business: order_origin = 'ECAT' returns 0 for all months — this org does not populate order_origin field. Channel attribution within portal_orders not available.
