# Section Manifest — Wildwood/Chelsea House (wwjc) — 2026-04-17

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (22 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | SKIP | HAS_CLICKY = false | — |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier1 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| Section | Cache Files Read |
|---------|-----------------|
| §2 Sales Team | Q-01_step1_results.md, Q-01_step2_results.md, Q-05_results.md, Q-06_results.md, Q-43_results.md, showroom_scan_results.md |
| §3 Customers | Q-12_results.md, Q-13_results.md, Q-14_results.md, Q-17_results.md, Q-40_results.md, Q-41_results.md |
| §4 Product | Q-07_results.md, Q-37_results.md, Q-38a_results.md, Q-39_results.md, Q-42_results.md |
| §5 Commerce | Q-18_results.md, Q-16_results.md, Q-20_results.md, Q-21_results.md, Q-45_results.md |
| §6 Portal | SKIP — HAS_CLICKY = false |
| §7 Peer | Q-CI-03_results.md, Q-CI-05_results.md, peer_benchmark_extract.md |
| §8 Platform | Q-08_results.md, Q-09_results.md, Q-10_results.md, Q-11_results.md, Q-22_results.md, Q-46_results.md |
