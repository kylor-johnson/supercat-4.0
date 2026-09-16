# Section Manifest — RENWIL (rw, org_id=248)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report
- **Profile**: deep_intelligence (default)

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (44 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true (2,048 items); HAS_SALES_DATA = false | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | INCLUDE | HAS_CLICKY = true (prefix: renwil_rw_eol) | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier2 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| Section | Cache Files Read |
|---------|-----------------|
| §1 Executive Summary | All section outputs (written last by stage4_assembly.md) |
| §2 Sales Team | Q-01_step1_results.md, Q-01_step2_results.md, Q-06_results.md, Q-43_results.md, showroom_scan_results.md, gate_flags.md (+ query_library.md for Q-02/Q-03 derivation rules) |
| §3 Customers | Q-12_results.md, Q-14_results.md, Q-17_results.md, Q-40_results.md, Q-41_results.md, gate_flags.md |
| §4 Product & Inventory | Q-07_results.md, gate_flags.md (HAS_SALES_DATA = false: Q-37, Q-39, Q-42 skipped; portal_order_items = 0: Q-38a skipped) |
| §5 Commerce | Q-13_results.md, Q-18_results.md, Q-20_results.md, Q-21_results.md, gate_flags.md (HAS_PORTAL_ORDERS = false: Q-16, Q-18B, Q-45 skipped) |
| §6 Portal | Q-CL-01_results.md, Q-CL-03_results.md, Q-CL-05_results.md, gate_flags.md |
| §7 Peer Benchmarking | peer_benchmark_extract.md, Q-CI-03_results.md, Q-CI-05_results.md, gate_flags.md |
| §8 Platform & Feature | Q-07_results.md, Q-08_results.md, Q-09_results.md, Q-10_results.md, Q-11_results.md, Q-22_results.md, gate_flags.md |
| §9 Appendix | gate_flags.md (data source attribution rows only) |

## Conditional Queries Skipped

| Query | Reason |
|-------|--------|
| Q-16 | HAS_PORTAL_ORDERS = false |
| Q-18 Part B | HAS_PORTAL_ORDERS = false |
| Q-45 | HAS_PORTAL_ORDERS = false (no ERP denominator) |
| Q-37 | HAS_SALES_DATA = false |
| Q-38a | portal_order_items_count = 0 |
| Q-39 | HAS_SALES_DATA = false |
| Q-42 | HAS_SALES_DATA = false |
| Q-CI-04 | Requires 2+ monthly snapshots — target May 2026 |
| Q-38b | pending_engineering — no invoice_date in sales_data |
