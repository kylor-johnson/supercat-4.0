# Gate Flags — Universal Furniture (ufi, org_id=18)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary.has_clicky_portal = true; ufi_eol_daily_metrics confirmed in clicky_analytics |
| HAS_CART | false | No "B2B Cart" in recurring_services; enable_online_ordering = false; 0 server orders LTM |
| HAS_PORTAL_ORDERS | true | portal_order_count (LTM) = 60,434; portal_orders GMV = $135.9M |
| HAS_INVENTORY | true | inventory_count = 2,201 |
| HAS_SALES_DATA | true | sales_data_count = 102,570 |
| HAS_SALES_SECTION | true | 20 reps with ≥10 iPad orders LTM (≥5 required) |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv; benchmark_eligible = True |
| BENCHMARK_ELIGIBLE | True | peer_benchmark_2026-04-14.csv |
| BENCHMARK_CONFIDENCE | low | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier2 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 32 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Furniture | Source for plain-language cohort framing |
| CLICKY_PREFIX | ufi_eol | org_summary.clicky_prefix confirmed; ufi_eol_daily_metrics exists |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | PASS | erp_gmv ($135,911,715) > ecat_gmv ($13,278,253) |
| VM45_GATE_2 | PASS | ecat_gmv ($13,278,253) >= 0.05 × erp_gmv ($6,795,586) |
| VM45_RENDER | true | Both gates pass — render capture rate subsection |
| QUALIFYING_REP_COUNT | 20 | Number of reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 101 rows |
| SHOWROOM_EXCLUSIONS | 0 | See showroom_scan_results.md — no operational accounts identified |

## Org Identity

- **Client name**: Universal Furniture
- **Shortname**: ufi
- **Org ID**: 18
- **Bundle**: iPad+Catalog+Portal
- **Bundle label for report**: eCat iPad + Online Catalog + Sales Portal
- **Vertical**: Furniture
- **Segment (internal)**: Platform-Embedded
- **ARR**: $25,435
- **Feature depth**: 5

## Validation Log

- portal_orders: LTM count = 60,434; all-time count = 114,417. HAS_PORTAL_ORDERS confirmed true. order_origin = 'ECAT' is NOT populated for this org (all ecat_originated_orders = 0 in Q-16) — ERP sync does not tag eCat origin.
- Showroom scan: Pass 1 (keyword) and Pass 2 (brand-name "Universal") both returned 0 matches. No operational/showroom accounts to exclude.
- VM-45: Both gates pass. ecat_gmv_capture_pct = 9.8%. ecat_posture = "Enablement-heavy; eCat captures little of total volume".
- Q-38a: SKIPPED — portal_order_items has 251,995 rows but ecat_item_number is NULL for all rows. Data gap: ecat_item_number not populated for this org.
- Q-42: SKIPPED — no products with new_item = true for this org.
- Q-CI-04: SKIPPED — requires 2+ monthly peer benchmark snapshots (2 exist but first available May 2026 for trending).
- Import warnings: Products import shows recurring :warning for unknown price fields (Price_BBD, Price_BBW, etc.) and missing custom fields (Wood_Finish, Nail_Trim, etc.) — cosmetic import config issue, not data loss.
- Catalog completeness: 0% completeness_pct for visible products (2,201 visible, 0 hidden) because net_price = NULL for all 2,201 products. Images are 100% present. Price data appears to be managed outside the standard net_price field (likely via price levels or custom pricing).
