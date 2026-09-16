# Gate Flags — Somerset Bay and Modern History (sbmh, org_id=2)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary.has_clicky_portal = true; Clicky tables confirmed in clicky_analytics |
| HAS_CART | true | mobile_sites.enable_online_ordering = true + server_order_count = 1,276 LTM |
| HAS_PORTAL_ORDERS | true | portal_order_count = 5,016 LTM; portal_gmv = $12,464,747.13 LTM |
| HAS_INVENTORY | true | inventory_count = 12,207 rows |
| HAS_SALES_DATA | true | sales_data_count = 16,413 rows |
| HAS_SALES_SECTION | true | 18 qualifying reps (≥10 iPad orders LTM) — threshold is 5 |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv present; run date 6 days ago |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in CSV |
| BENCHMARK_CONFIDENCE | medium | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 6 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Furniture / Full | Source for plain-language cohort framing |
| CLICKY_PREFIX | modern_history_eol | Confirmed via INFORMATION_SCHEMA.TABLES |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | PASS | portal_orders_gmv ($12,464,747.13) > ecat_gmv ($10,945,070.44) |
| VM45_GATE_2 | PASS | ecat_gmv ($10,945,070.44) >= 0.05 × portal_orders_gmv ($623,237.36) |
| VM45_RENDER | true | Both gates pass — render capture rate subsection |
| QUALIFYING_REP_COUNT | 18 | Number of reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 36 rows |
| SHOWROOM_EXCLUSIONS | 0 | No showroom/operational accounts detected (both keyword and brand-name passes returned empty) |

## Org Identity

- **Client name**: Somerset Bay and Modern History
- **Shortname**: sbmh
- **Org ID**: 2
- **Bundle**: Full (iPad + Online Catalog + B2B Cart + Sales Portal)
- **Bundle label for report**: Full Platform (eCat iPad, Online Catalog, B2B Cart, Sales Portal)
- **Vertical**: Furniture
- **Segment (internal only)**: Platform-Embedded

## Validation Log

- portal_orders: LTM count = 5,016; GMV = $12,464,747.13. HAS_PORTAL_ORDERS confirmed true. order_origin field not populated with 'ECAT' — all values = 0 across months.
- Showroom scan: Pass 1 (keyword) = 0 results. Pass 2 (brand-name "Somerset"/"Modern History") = 0 results. No exclusions.
- VM-45: Gate 1 PASS (ERP GMV > eCat GMV). Gate 2 PASS (eCat GMV = 87.8% of ERP). Capture rate = 87.8% — "Primary transaction system" posture.
- Q-38a: portal_order_items count = 36,888 all-time but query returned 0 rows for last 6 months with non-null ecat_item_number. Likely ecat_item_number not populated. Q-38a skipped — note in manifest.
- Q-49: buyer_name not populated (0 of 15,523 orders), but customer_bill_to_number fully populated. Q-49 executed using bill_to attribution.
