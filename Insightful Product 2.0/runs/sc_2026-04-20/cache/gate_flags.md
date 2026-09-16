# Gate Flags — Gabriella White (sc, org_id=69)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary.has_clicky_portal = true; clicky_prefix confirmed |
| HAS_CART | false | No "eCat Online - B2B Cart" in recurring_services; server_order_count = 0 LTM |
| HAS_PORTAL_ORDERS | true | portal_order_count LTM = 16,266; portal_order_items = 356,533 |
| HAS_INVENTORY | true | inventory_count = 15,630 |
| HAS_SALES_DATA | true | sales_data_count = 111,305 |
| HAS_SALES_SECTION | true | 91 qualifying reps with ≥10 iPad orders LTM |
| HAS_PEER_DATA | true | Present in segment_peer_comparison; benchmark CSV 2026-04-14 |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in CSV |
| BENCHMARK_CONFIDENCE | low | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier3 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 13 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | iPad+Catalog+Portal | Source for plain-language cohort framing |
| CLICKY_PREFIX | sc_retail_sc | Confirmed table sc_retail_sc_daily_metrics exists |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | FAIL | eCat GMV ($142.7M) > ERP GMV ($33.8M) — ERP sync is partial |
| VM45_GATE_2 | PASS | eCat GMV ($142.7M) >= 5% of ERP GMV ($1.69M threshold) |
| VM45_RENDER | false | Gate 1 fails — ERP sync is partial; capture rate denominator invalid |
| QUALIFYING_REP_COUNT | 91 | 91 reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 207 rows |
| SHOWROOM_EXCLUSIONS | 0 | No keyword or brand-name matches in showroom scan |

## Org Identity

- **Client name**: Gabriella White
- **Shortname**: sc
- **Org ID**: 69
- **Bundle**: iPad+Catalog+Portal
- **Bundle label for report**: eCat iPad App with Online Catalog and Sales Intelligence Dashboard
- **Segment (internal only)**: Platform-Embedded
- **ARR**: $30,904
- **Feature depth**: 8
- **Recurring services**: eCat (iPad) - Add'l Seats; eCat (iPad) Service; eCat Online - Catalog; eCat Online - Closed Site; eCat Online - Portal; eCat Online service

## Validation Log

- portal_orders: LTM count = 16,266; ERP GMV = $33.8M vs eCat GMV = $142.7M. eCat GMV exceeds ERP GMV — ERP sync is partial. VM-45 denominator gate fails (Gate 1). Q-45 skipped.
- Showroom scan: Pass 1 (keyword) = 0 matches. Pass 2 (brand "Gabriella") = 0 matches. SHOWROOM_EXCLUSIONS = 0.
- VM-45: Gate 1 FAIL — eCat GMV ($142,727,837.65) exceeds portal_orders GMV ($33,791,133.68). ERP sync appears partial. Capture rate not computed.
- Territory data: JSON-array format confirmed (e.g., ["302"]). 17 territories found. Territory names not populated in territories table.
- Q-19 (Channel Mix): SKIP — HAS_CART = false, server_order_count = 0.
- Q-42 (New Items): 3 collections with new_item flag; modest ERP sales ($62.8K top collection).
- Clicky portal: Very low traffic — avg 4 unique visitors/day. Portal is a closed site (eCat Online - Closed Site).
