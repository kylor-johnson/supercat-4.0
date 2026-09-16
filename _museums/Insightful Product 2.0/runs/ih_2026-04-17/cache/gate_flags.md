# Gate Flags — Interlude Home (ih, org_id=164)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary.has_clicky_portal = true; clicky_prefix = interlude_home_ih_eol_portal |
| HAS_CART | false | No "eCat Online - B2B Cart" in recurring_services; 0 server orders LTM |
| HAS_PORTAL_ORDERS | true | 7,123 LTM portal_orders; portal_order_count = 7,147 all-time |
| HAS_INVENTORY | true | 1,082 inventory rows |
| HAS_SALES_DATA | true | 8,801 sales_data rows |
| HAS_SALES_SECTION | true | 28 qualifying reps with ≥10 iPad orders LTM |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv present (3 days old); BQ segment_peer_comparison has data |
| BENCHMARK_ELIGIBLE | true | benchmark_eligible = True in peer CSV |
| BENCHMARK_CONFIDENCE | low | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier2 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 32 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Furniture | Source for plain-language cohort framing |
| CLICKY_PREFIX | interlude_home_ih_eol_portal | Confirmed via BQ table listing |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | PASS | erp_gmv ($17,003,445.78) > ecat_gmv ($11,514,096.89) — ERP sync is superset |
| VM45_GATE_2 | PASS | ecat_gmv ($11,514,096.89) >= 5% of erp_gmv ($850,172.29) — capture rate is interpretable |
| VM45_RENDER | true | Both gates pass — render capture rate subsection |
| QUALIFYING_REP_COUNT | 28 | Reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 51 rows |
| SHOWROOM_EXCLUSIONS | 3 | See showroom_scan_results.md for names + evidence |

## Org Identity

- **Client name**: Interlude Home
- **Shortname**: ih
- **Org ID**: 164
- **Bundle**: iPad+Catalog+Portal
- **Bundle label for report**: eCat iPad + Online Product Catalog + Sales Intelligence Portal
- **Vertical**: Furniture
- **Segment (internal)**: Platform-Embedded
- **ARR**: $25,555
- **Feature depth**: 6
- **Recurring services**: eCat (iPad) - Add'l Seats; eCat (iPad) - CC Service; eCat (iPad) Service; eCat Online - Catalog; eCat Online - Closed Site; eCat Online - Portal; eCat Online service

## Validation Log

- portal_orders: LTM count = 7,123, all-time = 7,147. HAS_PORTAL_ORDERS = true. order_origin = all zeros for 'ECAT' — ERP does not tag eCat-originated orders, but Q-45 still valid via total comparison.
- Showroom scan: 3 accounts flagged — MIASR2 Miami Showroom (confirmed, $1,046,847 GMV), NYSR New York ($969,641 GMV, city in last name), NYSR2 New York ($611,177 GMV, city in last name). See showroom_scan_results.md.
- VM-45: Both gates pass. eCat GMV capture = 67.7% of ERP total. Posture: Primary transaction system.
- Q-38a: Returned 0 rows for 6-month window — ecat_item_number may not be populated in portal_order_items for this org. Q-38a skipped.
- Q-42: 24 collections with new_item = true but all show $0 ERP sales. sales_data may not join correctly to new items or new items have not yet been invoiced.
