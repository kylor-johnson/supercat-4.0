# Section Manifest — Somerset Bay and Modern History (sbmh)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (18 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | INCLUDE | HAS_CLICKY = true | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier1 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| Cache File | Section(s) | Status |
|-----------|-----------|--------|
| Q-01_step1_results.md | §2 Sales | Executed (36 rows) |
| Q-01_step2_results.md | §2 Sales | Executed (25 rows) |
| Q-02 | §2 Sales | Stage 2 derivation — no cache file |
| Q-03 | §2 Sales | Stage 2 derivation — no cache file |
| Q-04_results.md | §2 Sales, §8 Platform | Executed (36 rows) |
| Q-05_results.md | §8 Platform | Executed |
| Q-06_results.md | §2 Sales | Executed (32 rows) |
| Q-07_results.md | §4 Product, §8 Platform | Executed |
| Q-08_results.md | §8 Platform | Executed (22 entity types) |
| Q-09_results.md | §8 Platform | Executed (7 months + 10 recent imports) |
| Q-10_results.md | §8 Platform | Executed |
| Q-11_results.md | §8 Platform | Executed (13 stale entities) |
| Q-12_results.md | §3 Customers | Executed |
| Q-13_results.md | §5 Commerce | Executed (15 rows) |
| Q-14_results.md | §3 Customers | Executed (20 rows) |
| Q-16_results.md | §5 Commerce | Executed (13 months) |
| Q-17_results.md | §3 Customers | Executed (25 lapsed + 20 at-risk) |
| Q-18_results.md | §5 Commerce | Executed (Part A: 13 months, Part B: 13 months) |
| Q-20_results.md | §5 Commerce | Executed (4 dimensions) |
| Q-21_results.md | §5 Commerce | Executed (3 order types) |
| Q-22_results.md | §8 Platform | Executed (org-level) |
| Q-37_results.md | §4 Product | Executed (20 OOS items) |
| Q-38a | §4 Product | SKIPPED — ecat_item_number not populated in portal_order_items |
| Q-39_results.md | §4 Product | Executed (17 categories, 16 collections) |
| Q-40_results.md | §3 Customers | Executed (20 states + 50 cross-tab rows) |
| Q-41_results.md | §3 Customers | Executed (32 month-channel rows + 25 rep rows) |
| Q-42_results.md | §4 Product | Executed (5 collections with new items) |
| Q-43_results.md | §2 Sales | Executed (25 territories, JSON path) |
| Q-45_results.md | §5 Commerce | Executed (VM45_RENDER = true) |
| Q-46_results.md | §8 Platform | Executed (Postgres + BigQuery) |
| Q-47_results.md | §8 Platform | Executed (4 stacks, 0 stale) |
| Q-49_results.md | §3 Customers | Executed (bill_to attribution) |
| Q-50_results.md | §8 Platform | Executed (7 documents, 7 stale) |
| Q-CL-01_results.md | §6 Portal | Executed (7 months) |
| Q-CL-03_results.md | §6 Portal | Executed (20 regions, alt schema) |
| Q-CL-05_results.md | §6 Portal | Executed (6 sources) |
| Q-CI-01_results.md | §7 Peer | Executed (org summary) |
| Q-CI-02_results.md | §7 Peer | Executed (peer comparison) |
| Q-CI-03_results.md | §7 Peer | Executed (org summary + 2 monthly benchmarks) |
| Q-CI-05_results.md | §7 Peer | Executed (top 10 performers) |
| peer_benchmark_extract.md | §7 Peer | Extracted from CSV |
| showroom_scan_results.md | §2 Sales | No exclusions found |
