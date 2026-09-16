# Gate Flags — Four Seasons Furniture (fsf, org_id=225)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary.has_clicky_portal = true; clicky_analytics tables confirmed |
| HAS_CART | true | recurring_services contains "eCat Online - B2B Cart"; server_order_count = 5,371 LTM |
| HAS_PORTAL_ORDERS | true | portal_order_count LTM = 1,826; portal_orders GMV = $2,912,350.12 |
| HAS_INVENTORY | true | inventory_count = 920 |
| HAS_SALES_DATA | true | sales_data_count = 14,894 |
| HAS_SALES_SECTION | true | 12 qualifying reps with ≥10 iPad orders LTM (threshold: 5) |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv present (3 days old) |
| BENCHMARK_ELIGIBLE | True | benchmark_eligible = True in CSV |
| BENCHMARK_CONFIDENCE | medium | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 6 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Furniture / Full | Source for plain-language cohort framing |
| CLICKY_PREFIX | four_seasons_furniture_fsf_eol_portal | Confirmed via INFORMATION_SCHEMA |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | FAIL | eCat GMV ($12,395,204.95) > ERP GMV ($2,912,350.12) — ERP sync is partial |
| VM45_GATE_2 | N/A | Not evaluated — Gate 1 failed |
| VM45_RENDER | false | Gate 1 failed — capture rate denominator invalid; Q-45 skipped |
| QUALIFYING_REP_COUNT | 12 | Reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 33 rows |
| SHOWROOM_EXCLUSIONS | 0 | No keyword or brand-name matches in showroom scan |

## Org Identity

- **Client name**: Four Seasons Furniture
- **Shortname**: fsf
- **Org ID**: 225
- **Bundle**: Full (iPad + Catalog + Cart + Portal)
- **Bundle label for report**: eCat iPad, Online Catalog, B2B Cart, Sales Portal
- **Segment (internal only)**: Platform-Embedded
- **Vertical**: Furniture
- **ARR**: $22,560
- **Feature depth**: 7

## Validation Log

- portal_orders: LTM count = 1,826; GMV = $2,912,350.12. ERP sync appears partial — eCat GMV ($12.4M) exceeds ERP GMV ($2.9M). HAS_PORTAL_ORDERS = true but VM-45 skipped due to denominator invalidity.
- Showroom scan: Pass 1 (keyword) = 0 matches. Pass 2 (brand name "Four Seasons") = 0 matches. No exclusions applied.
- VM-45: Gate 1 FAIL — eCat GMV ($12,395,204.95) > portal_orders GMV ($2,912,350.12). ERP sync is a subset, not total business. Capture rate not computable.
- Q-43: Territory codes in JSON format (["006"]). JSON path used. No territory names in territories table for this org.
