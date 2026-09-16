# Section Manifest — Magnussen Home (mh, org_id=184)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (9 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true (NOTE: inventory 256 days stale) | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | SKIP | HAS_CLICKY = false | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, PEER_GROUP_LEVEL = tier3 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| Cache File | Section(s) | Status |
|-----------|------------|--------|
| Q-01_step1_results.md | §2 Sales | Executed |
| Q-01_step2_results.md | §2 Sales | Executed |
| Q-02 (derived) | §2 Sales | Stage 2 derivation from Q-01 |
| Q-03 (derived) | §2 Sales | Stage 2 derivation from Q-01 |
| Q-04_results.md | §2 Sales | Executed |
| Q-05_results.md | §8 Platform | Executed |
| Q-06_results.md | §2 Sales | Executed |
| Q-07_results.md | §4 Product, §8 Platform | Executed |
| Q-08_results.md | §8 Platform | Executed |
| Q-09_results.md | §8 Platform | Executed |
| Q-10_results.md | §8 Platform | Executed (mobile_sites empty — BigQuery org_summary used) |
| Q-11_results.md | §8 Platform | Executed |
| Q-12_results.md | §3 Customers | Executed |
| Q-13_results.md | §5 Commerce | Executed |
| Q-14_results.md | §3 Customers | Executed |
| Q-16 | §5 Commerce | SKIPPED — HAS_PORTAL_ORDERS = false |
| Q-17_results.md | §3 Customers | Executed |
| Q-18_results.md | §5 Commerce | Executed (Part A only — Part B skipped, no portal_orders) |
| Q-20_results.md | §5 Commerce | Executed |
| Q-21_results.md | §5 Commerce | Executed |
| Q-22_results.md | §8 Platform | Executed |
| Q-37_results.md | §4 Product | Executed (inventory 256 days stale — caveat required) |
| Q-38a | §4 Product | SKIPPED — portal_order_items = 0 |
| Q-39_results.md | §4 Product | Executed |
| Q-40_results.md | §3 Customers | Executed |
| Q-41_results.md | §3 Customers | Executed |
| Q-42_results.md | §4 Product | Executed |
| Q-43_results.md | §2 Sales | Executed (JSON path for territory_codes) |
| Q-45 | §5 Commerce | SKIPPED — HAS_PORTAL_ORDERS = false |
| Q-46_results.md | §8 Platform | Executed |
| Q-47_results.md | §8 Platform | Executed |
| Q-50_results.md | §8 Platform | Executed |
| Q-CI-01_results.md | §7 Peer | Executed |
| Q-CI-02_results.md | §7 Peer | Executed |
| Q-CI-03_results.md | §7 Peer | Executed |
| Q-CI-05_results.md | §7 Peer | Executed |
| Q-CL-01 through Q-CL-05 | §6 Portal | SKIPPED — HAS_CLICKY = false |
| peer_benchmark_extract.md | §7 Peer | Extracted |
| showroom_scan_results.md | §2 Sales | Executed — 0 exclusions |

## Skipped Queries Summary

| Query | Reason |
|-------|--------|
| Q-16 | HAS_PORTAL_ORDERS = false |
| Q-18 Part B | HAS_PORTAL_ORDERS = false |
| Q-38a | portal_order_items_count = 0 |
| Q-45 | HAS_PORTAL_ORDERS = false (no ERP denominator) |
| Q-CL-01 through Q-CL-05 | HAS_CLICKY = false |
| Q-CI-04 | Requires 2+ monthly snapshots — only 2 exist but target May 2026 |
| Q-15 | Excluded from external scope (enrollment) |
| Q-44 | Excluded from external scope (enrollment) |
| Q-49 | HAS_PORTAL_ORDERS = false (no buyer attribution) |
