# Gate Flags — Linon/Powell Furniture (lpf, org_id=139)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary.has_clicky_portal = true; table lpf_ecat_online_daily_metrics confirmed in clicky_analytics |
| HAS_CART | true | enable_online_ordering = true; 1,005 server orders LTM confirmed |
| HAS_PORTAL_ORDERS | true | 74,400 LTM portal_orders; portal_order_count all-time = 191,228 |
| HAS_INVENTORY | true | 3,845 inventory rows |
| HAS_SALES_DATA | true | 21,804 sales_data rows |
| HAS_SALES_SECTION | true | 17 qualifying reps (≥10 iPad orders LTM) |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv present; 6 days old |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in CSV |
| BENCHMARK_CONFIDENCE | low | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier3 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 19 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Full | Source for plain-language cohort framing |
| CLICKY_PREFIX | lpf_ecat_online | Confirmed via clicky_analytics.INFORMATION_SCHEMA |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | PASS | ERP GMV $27,690,068.19 > eCat GMV $3,989,073.19 |
| VM45_GATE_2 | PASS | eCat GMV $3,989,073.19 ≥ 5% × ERP GMV ($1,384,503.41) |
| VM45_RENDER | true | Both gates pass — render capture rate subsection |
| QUALIFYING_REP_COUNT | 17 | Reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 69 rows |
| SHOWROOM_EXCLUSIONS | 0 | No keyword or brand-name matches in showroom scan |

## Org Identity

- **Client name**: Linon/Powell Furniture
- **Shortname**: lpf
- **Org ID**: 139
- **Bundle**: Full
- **Bundle label for report**: iPad + Online Catalog + B2B Cart + Sales Portal
- **Vertical**: Generic B2B Wholesale
- **Segment (internal)**: Platform-Embedded

## Validation Log

- portal_orders: 74,400 LTM; 191,228 all-time. HAS_PORTAL_ORDERS = true (confirmed).
- Showroom scan: Pass 1 (keyword) = 0 matches. Pass 2 (brand-name "Linon") = 0 matches. Pass 2 (brand-name "Powell") = 0 matches. No exclusions.
- VM-45: Gate 1 PASS (ERP $27.7M > eCat $4.0M). Gate 2 PASS (eCat 14.4% of ERP > 5% threshold). VM45_RENDER = true.
- order_origin: All portal_orders.order_origin values = NULL (no ECAT tag). Q-16 ecat_originated_orders = 0. This is an ERP-side attribution gap — eCat orders exist but are not tagged as ECAT origin in the ERP feed.
- Q-42: No products with new_item = true. Skipped.
