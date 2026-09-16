# Gate Flags — Crystorama (clm, org_id=64)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary has_clicky_portal = true; daily_metrics table confirmed |
| HAS_CART | false | enable_online_ordering = false; 0 server-source orders LTM |
| HAS_PORTAL_ORDERS | true | 72,632 LTM portal_orders |
| HAS_INVENTORY | true | 2,074 inventory rows confirmed |
| HAS_SALES_DATA | true | 68,568 sales_data rows confirmed |
| HAS_SALES_SECTION | true | 5 reps with ≥10 iPad orders LTM |
| HAS_PEER_DATA | true | Peer CSV dated 2026-04-14, not stale |
| BENCHMARK_ELIGIBLE | True | peer_benchmark_2026-04-14.csv |
| BENCHMARK_CONFIDENCE | medium | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 5 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Lighting / iPad+Catalog+Portal | Source for plain-language cohort framing |
| CLICKY_PREFIX | crystorama_clm_ecat_online | Used for BigQuery clicky_analytics table names |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | PASS | portal_orders_gmv ($39.3M) > ecat_gmv ($555K) |
| VM45_GATE_2 | FAIL | ecat_gmv ($555K) < 5% of portal_orders_gmv ($1.96M threshold) |
| VM45_RENDER | false | Gate 2 failed — eCat capture rate not interpretable as activation signal |
| QUALIFYING_REP_COUNT | 5 | Reps with ≥10 iPad orders LTM: Katy McCully (38), Jeff Nicholson (19), Matt Sullivan (11), Chas Lassoff (11), Zachary Rapp (10) |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 99 users |
| SHOWROOM_EXCLUSIONS | 1 | See showroom_scan_results.md for names + evidence |

## Org Identity

- **Client name**: Crystorama
- **Shortname**: clm
- **Org ID**: 64
- **Bundle**: iPad+Catalog+Portal
- **Bundle label for report**: iPad + eCat Online + Sales Portal

## Validation Log

- portal_orders: 138,769 total rows; 72,632 LTM; all have buyer_name and customer_bill_to_number populated
- Showroom scan: 1 confirmed exclusion ("HighPoint Showroom" — $8,084 GMV, 2 orders LTM)
- VM-45: Gate 2 FAIL — eCat GMV ($555K) is 1.4% of ERP total ($39.3M), below 5% threshold. Capture rate subsection skipped.
