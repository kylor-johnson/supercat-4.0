# Gate Flags — Hubbardton Forge (hfg, org_id=165)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary.has_clicky_portal = true; Clicky tables confirmed in BigQuery |
| HAS_CART | false | No "eCat Online - B2B Cart" in recurring_services; 0 server orders LTM |
| HAS_PORTAL_ORDERS | true | 22,098 LTM ERP orders; portal_orders table populated |
| HAS_INVENTORY | false | 0 rows in inventories table |
| HAS_SALES_DATA | true | 42,459 rows in sales_data table |
| HAS_SALES_SECTION | true | 17 qualifying reps with ≥10 iPad orders LTM (threshold: 5) |
| HAS_PEER_DATA | true | segment_peer_comparison has row for hfg; segment_benchmarks_monthly has 2 snapshots |
| BENCHMARK_ELIGIBLE | true | Data present in peer comparison table |
| BENCHMARK_CONFIDENCE | high | Internal only — not in delivered HTML. N=47 peers in segment. |
| PEER_GROUP_LEVEL | segment | Internal only — not in delivered HTML |
| PEER_GROUP_N | 47 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Platform-Embedded | Source for plain-language cohort framing |
| CLICKY_PREFIX | hubbardton_forge_hfg_eol_portal | Confirmed via BigQuery INFORMATION_SCHEMA; 23 tables present |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | PASS | ERP GMV ($42,908,534.73) > eCat GMV ($15,616,842.46) |
| VM45_GATE_2 | PASS | eCat GMV ($15.6M) ≥ 5% of ERP GMV ($2.15M threshold) — actual ratio 36.4% |
| VM45_RENDER | true | Both gates pass — render capture rate subsection |
| QUALIFYING_REP_COUNT | 17 | Reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 134 rows |
| SHOWROOM_EXCLUSIONS | 0 | Keyword scan: 0 matches. Brand-name scan ("Hubbardton"): 0 matches. |

## Org Identity

- **Client name**: Hubbardton Forge
- **Shortname**: hfg
- **Org ID**: 165
- **Bundle**: iPad+Catalog+Portal
- **Bundle label for report**: eCat iPad + Online Product Catalog + Sales Intelligence Portal
- **ARR**: $35,540
- **Feature depth**: 7
- **recurring_services**: eCat (iPad) - Add'l Seats; eCat (iPad) Service; eCat Online - Catalog; eCat Online - Closed Site; eCat Online - Portal; eCat Online service

## Validation Log

- portal_orders: 22,098 LTM orders confirmed; HAS_PORTAL_ORDERS = true. order_origin column populated but all values show 0 for ECAT-originated — ERP does not tag eCat origin.
- Showroom scan: Pass 1 (keyword) and Pass 2 (brand name "Hubbardton") both returned 0 matches. No showroom/operational accounts detected.
- VM-45: Both gates pass. eCat GMV capture rate = 36.4%. Posture: "Meaningful eCat channel; dual-system."
- Q-49: Buyer repeat purchase BLOCKED — portal_orders.buyer_name = 0 populated rows. No buyer attribution available.
- Clicky regions schema: Alternative variant (title/value columns, no country column). Used alternative query path for Q-CL-03.
- Clicky traffic sources schema: Alternative variant (title/value columns). Used alternative query path for Q-CL-05.
- Territory codes format: JSON-array (e.g., ["45123"]). Used JSON path for Q-43.
- Import errors: Recurring customer import errors (lines 1724-1727: invalid default price code 't'; line 11760: CSV parse error). Portal Orders and Portal Invoices also show recurring CSV parse warnings. These are non-blocking but should be noted.
