# Section Manifest — Visual Comfort - Studio /Fans (fms, org_id=108)
- **Run date**: 2026-04-30
- **Report mode**: Mode 1: Standard Intelligence Report
- **Profile**: deep_intelligence (default)

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (23 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | INCLUDE | HAS_CLICKY = true (note: near-zero traffic) | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier1 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| Query | Status | Cache File | Section(s) |
|-------|--------|-----------|------------|
| Q-01 Step 1 | EXECUTED | Q-01_step1_results.md | §2 Sales |
| Q-01 Step 2 | EXECUTED | Q-01_step2_results.md | §2 Sales |
| Q-02 | STAGE 2 DERIVATION | (no cache file) | §2 Sales |
| Q-03 | STAGE 2 DERIVATION | (no cache file) | §2 Sales |
| Q-04 | NOT RUN | — | §2 Sales (derived from Q-01) |
| Q-05 | EXECUTED | Q-05_results.md | §8 Platform |
| Q-06 | EXECUTED | Q-06_results.md | §2 Sales |
| Q-07 | EXECUTED | Q-07_results.md | §4 Product, §8 Platform |
| Q-08 | EXECUTED | Q-08_results.md | §8 Platform |
| Q-09 | EXECUTED | Q-09_results.md | §8 Platform |
| Q-10 | EXECUTED | Q-10_results.md | §8 Platform |
| Q-11 | EXECUTED | Q-11_results.md | §8 Platform |
| Q-12 | EXECUTED | Q-12_results.md | §3 Customers |
| Q-13 | EXECUTED | Q-13_results.md | §5 Commerce |
| Q-14 | EXECUTED | Q-14_results.md | §3 Customers |
| Q-15 | SKIPPED | — | Internal only (enrollment excluded) |
| Q-16 | SKIPPED | — | HAS_PORTAL_ORDERS = false |
| Q-17 | EXECUTED | Q-17_results.md | §3 Customers |
| Q-18 Part A | EXECUTED | Q-18_results.md | §5 Commerce |
| Q-18 Part B | SKIPPED | — | HAS_PORTAL_ORDERS = false |
| Q-19 | SKIPPED | — | HAS_CART = false (iPad-only) |
| Q-20 | EXECUTED | Q-20_results.md | §5 Commerce |
| Q-21 | EXECUTED | Q-21_results.md | §5 Commerce |
| Q-22 | EXECUTED | Q-22_results.md | §8 Platform |
| Q-37 | EXECUTED | Q-37_results.md | §4 Product |
| Q-38a | SKIPPED | — | portal_order_items = 0 |
| Q-38b | PENDING ENGINEERING | — | No invoice_date in sales_data |
| Q-39 | EXECUTED | Q-39_results.md | §4 Product |
| Q-40 | EXECUTED | Q-40_results.md | §3 Customers |
| Q-41 | EXECUTED | Q-41_results.md | §3 Customers |
| Q-42 | EXECUTED (empty) | Q-42_results.md | §4 Product (no new_item data) |
| Q-43 | EXECUTED | Q-43_results.md | §2 Sales |
| Q-44 | SKIPPED | — | Internal only (enrollment excluded) |
| Q-45 | SKIPPED | — | HAS_PORTAL_ORDERS = false |
| Q-46 | EXECUTED | Q-46_results.md | §5 Commerce |
| Q-47 | EXECUTED | Q-47_results.md | §4 Product |
| Q-49 | SKIPPED | — | portal_orders = 0 (no buyer attribution) |
| Q-50 | EXECUTED | Q-50_results.md | §8 Platform |
| Q-CL-01 | EXECUTED | Q-CL-01_results.md | §6 Portal |
| Q-CL-03 | EXECUTED | Q-CL-03_results.md | §6 Portal |
| Q-CL-05 | EXECUTED | Q-CL-05_results.md | §6 Portal |
| Q-CI-02 | EXECUTED | Q-CI-02_results.md | §7 Peer |
| Q-CI-03 | EXECUTED | Q-CI-03_results.md | §7 Peer |
| Q-CI-05 | NOT EXECUTED | — | Requires segment value; deferred |
