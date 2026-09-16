# Section Manifest — Fine Art Handcrafted Lighting (fal)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (27 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | SKIP | HAS_INVENTORY = false AND HAS_SALES_DATA = false | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | SKIP | HAS_CLICKY = false | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier1 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| Cache File | Section(s) | Status |
|-----------|-----------|--------|
| Q-01_step1_results.md | §2 Sales | Executed — 59 rows |
| Q-01_step2_results.md | §2 Sales | Executed — 42 rows |
| Q-02 (derived) | §2 Sales | Stage 2 derivation from Q-01 — no cache file |
| Q-03 (derived) | §2 Sales | Stage 2 derivation from Q-01 — no cache file |
| Q-05_results.md | §8 Platform | Executed — 1 row |
| Q-06_results.md | §2 Sales | Executed — 50 rows |
| Q-07_results.md | §4 Product, §8 Platform | Executed — 2 rows |
| Q-08_results.md | §8 Platform | Executed — 22 rows |
| Q-09_results.md | §8 Platform | Executed — 6 months + 10 recent imports |
| Q-10_results.md | §8 Platform | Executed — 0 rows (mobile_sites empty; flags from org_summary) |
| Q-11_results.md | §8 Platform | Executed — 13 rows |
| Q-12_results.md | §3 Customers | Executed — 1 row |
| Q-13_results.md | §5 Commerce | Executed — 15 rows |
| Q-14_results.md | §3 Customers | Executed — 20 rows |
| Q-16 | §5 Commerce | SKIPPED — HAS_PORTAL_ORDERS = false |
| Q-17_results.md | §3 Customers | Executed — 25 lapsed + 20 at-risk |
| Q-18_results.md | §5 Commerce | Executed — 13 months (Part A only; Part B skipped — no portal_orders) |
| Q-19 | §5 Commerce | SKIPPED — HAS_CART = false (derived from Q-18) |
| Q-20_results.md | §5 Commerce | Executed — 4 rows |
| Q-21_results.md | §5 Commerce | Executed — 5 rows |
| Q-22_results.md | §8 Platform | Executed — 1 row |
| Q-37 | §4 Product | SKIPPED — HAS_INVENTORY = false, HAS_SALES_DATA = false |
| Q-38a | §4 Product | SKIPPED — portal_order_items_count = 0 |
| Q-39 | §4 Product | SKIPPED — HAS_SALES_DATA = false |
| Q-40_results.md | §3 Customers | Executed — 20 rows |
| Q-41_results.md | §3 Customers | Executed — 16 months + 44 reps |
| Q-42 | §4 Product | SKIPPED — HAS_SALES_DATA = false |
| Q-43_results.md | §2 Sales | Executed — 38 territories (3 steps) |
| Q-45 | §5 Commerce | SKIPPED — HAS_PORTAL_ORDERS = false |
| Q-CL-01..05 | §6 Portal | SKIPPED — HAS_CLICKY = false |
| Q-CI-01_results.md | §7 Peer | Executed — org summary data |
| Q-CI-02_results.md | §7 Peer | Executed — peer comparison row |
| Q-CI-03_results.md | §7 Peer | Executed — segment benchmarks (2 months) |
| Q-CI-05_results.md | §7 Peer | Executed — top 10 performers |
| peer_benchmark_extract.md | §7 Peer | Extracted from CSV |
| showroom_scan_results.md | §2 Sales | 0 confirmed exclusions |
