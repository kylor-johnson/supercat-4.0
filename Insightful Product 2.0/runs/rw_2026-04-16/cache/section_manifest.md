# Section Manifest — RENWIL (rw, 2026-04-16)

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (44 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true (no sales_data — limited to catalog + inventory only) | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | INCLUDE | HAS_CLICKY = true (prefix: renwil_rw_eol) | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier2 (not tier4) | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| Section | Cache Files |
|---------|-------------|
| §2 Sales Team | Q-01_step1_results.md, Q-01_step2_results.md, Q-04_results.md, Q-05_results.md, Q-06_results.md, Q-43_step1_results.md, Q-43_step3_results.md, showroom_scan_results.md |
| §3 Customers | Q-12_results.md, Q-13_results.md, Q-14_results.md, Q-17_results.md, Q-40_results.md, Q-41_results.md |
| §4 Product | Q-07_results.md |
| §5 Commerce | Q-18_results.md, Q-20_results.md, Q-21_results.md |
| §6 Portal | Q-CL-01_results.md, Q-CL-03_results.md, Q-CL-05_results.md |
| §7 Peer | Q-CI-05_results.md, peer_benchmark_extract.md |
| §8 Platform | Q-08_results.md, Q-09_results.md, Q-10_results.md, Q-11_results.md, Q-22_results.md |

## Skipped Queries (gates not met)

| Query | Reason |
|-------|--------|
| Q-16 | HAS_PORTAL_ORDERS = false |
| Q-18 Part B | HAS_PORTAL_ORDERS = false |
| Q-45 | HAS_PORTAL_ORDERS = false — no denominator |
| Q-37 | HAS_SALES_DATA = false |
| Q-38a | portal_order_items = 0 |
| Q-39 | HAS_SALES_DATA = false |
| Q-42 | HAS_SALES_DATA = false |
| Q-19 | HAS_CART = false (0 server orders) |
| Q-49 | HAS_PORTAL_ORDERS = false |
