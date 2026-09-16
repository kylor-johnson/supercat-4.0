# Section Manifest — Charleston Forge (cfg, org_id=83)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (10 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | SKIP | HAS_INVENTORY = false AND HAS_SALES_DATA = false | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | INCLUDE | HAS_CLICKY = true | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier3 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| Query | Section | Status | Cache File |
|-------|---------|--------|-----------|
| Q-01 Step 1 | §2 Sales | Executed | Q-01_step1_results.md |
| Q-01 Step 2 | §2 Sales | Executed | Q-01_step2_results.md |
| Q-02 | §2 Sales | Stage 2 derivation (no cache file) | — |
| Q-03 | §2 Sales | Stage 2 derivation (no cache file) | — |
| Q-04 | §2 Sales, §8 Platform | Executed | Q-04_results.md |
| Q-05 | §8 Platform | Executed | Q-05_results.md |
| Q-06 | §2 Sales | Executed | Q-06_results.md |
| Q-07 | §4 Product, §8 Platform | Executed | Q-07_results.md |
| Q-08 | §8 Platform | Executed | Q-08_results.md |
| Q-09 | §8 Platform | Executed | Q-09_results.md |
| Q-10 | §8 Platform | Executed | Q-10_results.md |
| Q-11 | §8 Platform | Executed | Q-11_results.md |
| Q-12 | §3 Customers | Executed | Q-12_results.md |
| Q-13 | §5 Commerce | Executed | Q-13_results.md |
| Q-14 | §3 Customers | Executed | Q-14_results.md |
| Q-16 | §5 Commerce | Skipped — HAS_PORTAL_ORDERS = false | — |
| Q-17 | §3 Customers | Executed | Q-17_results.md |
| Q-18 Part A | §5 Commerce | Executed | Q-18_results.md |
| Q-18 Part B | §5 Commerce | Skipped — HAS_PORTAL_ORDERS = false | — |
| Q-20 | §5 Commerce | Executed | Q-20_results.md |
| Q-21 | §5 Commerce | Executed | Q-21_results.md |
| Q-22 | §8 Platform | Executed | Q-22_results.md |
| Q-37 | §4 Product | Skipped — HAS_INVENTORY = false AND HAS_SALES_DATA = false | — |
| Q-38a | §4 Product | Skipped — portal_order_items_count = 0 | — |
| Q-39 | §4 Product | Skipped — HAS_SALES_DATA = false | — |
| Q-40 | §3 Customers | Executed | Q-40_results.md |
| Q-41 | §3 Customers | Executed | Q-41_results.md |
| Q-42 | §4 Product | Skipped — HAS_SALES_DATA = false | — |
| Q-43 | §2 Sales | Executed | Q-43_results.md |
| Q-45 | §5 Commerce | Skipped — HAS_PORTAL_ORDERS = false | — |
| Q-46 | §8 Platform | Executed | Q-46_results.md |
| Q-47 | §8 Platform | Executed | Q-47_results.md |
| Q-50 | §8 Platform | Executed | Q-50_results.md |
| Q-CL-01 | §6 Portal | Executed | Q-CL-01_results.md |
| Q-CL-03 | §6 Portal | Executed | Q-CL-03_results.md |
| Q-CL-05 | §6 Portal | Executed | Q-CL-05_results.md |
| Q-CI-01 | §7 Peer | Executed | Q-CI-01_results.md |
| Q-CI-02 | §7 Peer | Executed | Q-CI-02_results.md |
| Q-CI-03 | §7 Peer | Executed | Q-CI-03_results.md |

## Queries Not Executed (by design)

| Query | Reason |
|-------|--------|
| Q-02 | Stage 2 derivation from Q-01 data (not a SQL query) |
| Q-03 | Stage 2 derivation from Q-01 data (not a SQL query) |
| Q-15 | Excluded from external scope (enrollment) |
| Q-16 | HAS_PORTAL_ORDERS = false |
| Q-18 Part B | HAS_PORTAL_ORDERS = false |
| Q-37 | HAS_INVENTORY = false AND HAS_SALES_DATA = false |
| Q-38a | portal_order_items_count = 0 |
| Q-38b | pending_engineering — no invoice_date on sales_data |
| Q-39 | HAS_SALES_DATA = false |
| Q-42 | HAS_SALES_DATA = false |
| Q-44 | Excluded from external scope (enrollment) |
| Q-45 | HAS_PORTAL_ORDERS = false |
| Q-49 | portal_orders = 0 (no buyer attribution available) |
| Q-CI-04 | Requires 2+ monthly snapshots (only 2 available — marginal) |
| Q-CI-05 | top_performers_by_segment table — deferred |
