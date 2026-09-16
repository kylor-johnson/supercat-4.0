# Gate Flags — Wildwood/Chelsea House (wwjc, org_id=8)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | false | org_summary.has_clicky_portal = false; clicky_prefix = null |
| HAS_CART | true | recurring_services includes "eCat Online - B2B Cart"; server_order_count = 4,965 LTM |
| HAS_PORTAL_ORDERS | true | portal_order_count = 111,160 total; LTM portal_orders = 14,843 |
| HAS_INVENTORY | true | inventory_count = 3,961 |
| HAS_SALES_DATA | true | sales_data_count = 98,337 |
| HAS_SALES_SECTION | true | 22 qualifying reps (≥10 iPad orders LTM); threshold = 5 |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv present (3 days old) |
| BENCHMARK_ELIGIBLE | true | From peer benchmark CSV |
| BENCHMARK_CONFIDENCE | high | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 8 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Lighting / Full | Source for plain-language cohort framing |
| CLICKY_PREFIX | N/A | HAS_CLICKY = false |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | PASS | erp_gmv ($17,846,497.76) > ecat_gmv ($8,959,747.67) |
| VM45_GATE_2 | PASS | ecat_gmv ($8,959,747.67) >= 0.05 × erp_gmv ($892,324.89) |
| VM45_RENDER | true | Both gates pass — render capture rate subsection |
| QUALIFYING_REP_COUNT | 22 | Number of reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 74 users |
| SHOWROOM_EXCLUSIONS | 1 | See showroom_scan_results.md for names + evidence |

## Org Identity

- **Client name**: Wildwood/Chelsea House
- **Shortname**: wwjc
- **Org ID**: 8
- **Bundle**: Full (iPad + Online Catalog + B2B Cart + Sales Portal)
- **Bundle label for report**: iPad + Online Catalog + B2B Cart + Sales Portal
- **Vertical**: Lighting
- **Segment**: Platform-Embedded (internal only)
- **ARR**: $40,220
- **Feature depth**: 5

## Validation Log

- portal_orders: present with 111,160 total rows; LTM = 14,843; HAS_PORTAL_ORDERS confirmed true
- Showroom scan: 1 confirmed exclusion — "Atlanta Showroom" (25 orders, $28,110.50 GMV); keyword match on "Showroom" in rep_first_name + city-based rep_last_name pattern
- VM-45: Both gates pass — ecat_gmv_capture_pct = 50.2%; posture = "Primary transaction system"
- order_origin: All portal_orders show order_origin blank (no ECAT/market tagging) — note for §5 assembly
- Territory format: JSON-array (e.g., `["104 Madeline Cole"]`) — JSON path used for Q-43
- Q-42 (New Item Performance): Only 1 new_item flagged across entire catalog — minimal signal
