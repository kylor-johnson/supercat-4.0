# Section Manifest — Universal Furniture (ufi, org_id=18)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Section Inclusion Status

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (20 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | INCLUDE | HAS_CLICKY = true (prefix: ufi_eol) | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier2 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| § | Section | Cache Files Read |
|---|---------|-----------------|
| 1 | Executive Summary | All section outputs (Stage 4 synthesis) |
| 2 | Sales Team Performance | Q-01_step1_results.md, Q-01_step2_results.md, Q-06_results.md, Q-43_results.md, showroom_scan_results.md |
| 3 | Customer & Buyer Intelligence | Q-12_results.md, Q-13_results.md, Q-14_results.md, Q-17_results.md, Q-41_results.md, Q-40_results.md |
| 4 | Product & Inventory Intelligence | Q-07_results.md, Q-37_results.md, Q-39_results.md |
| 5 | Commerce Analytics | Q-18_results.md, Q-20_results.md, Q-21_results.md, Q-16_results.md, Q-45_results.md |
| 6 | Portal Engagement | Q-CL-01_results.md, Q-CL-03_results.md, Q-CL-05_results.md |
| 7 | Peer Benchmarking | peer_benchmark_extract.md, Q-CI-03_results.md, Q-CI-05_results.md |
| 8 | Platform & Feature Utilization | Q-08_results.md, Q-09_results.md, Q-10_results.md, Q-11_results.md, Q-22_results.md |
| 9 | Appendix | gate_flags.md (data sources and staleness context) |

## Queries Skipped (with reason)

| Query | Reason | Section Affected |
|-------|--------|-----------------|
| Q-02 | Stage 2 derivation — not SQL, applied by §2 builder from Q-01 data | §2 |
| Q-03 | Stage 2 derivation — not SQL, applied by §2 builder from Q-01 data | §2 |
| Q-38a | Data-gated — ecat_item_number is NULL for all 251,995 portal_order_items rows | §4 |
| Q-38b | pending_engineering — no invoice_date on sales_data | §4 |
| Q-42 | Data-gated — no products with new_item = true for this org | §4 |
| Q-CI-04 | Pending — requires 2+ monthly snapshots for trending (target: May 2026) | §7 |

## Notes

- All eCat orders are iPad-only (0 server orders). HAS_CART = false — no eCat Online channel mix to display.
- Q-16 order_origin tagging not populated for this org — ecat_originated_orders = 0 across all months. ERP total business context is available by volume and GMV only.
- Q-07 catalog completeness shows 0% because net_price is NULL for all products. Images are 100% present. Pricing is managed via price levels or custom fields, not the standard net_price column.
- Q-37 top OOS items are predominantly "Special Order" products which may intentionally carry zero stock.
