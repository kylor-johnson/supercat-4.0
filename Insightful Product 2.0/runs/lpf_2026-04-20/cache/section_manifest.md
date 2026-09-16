# Section Manifest — Linon/Powell Furniture (lpf, org_id=139)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (17 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | INCLUDE | HAS_CLICKY = true | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier3 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| Section | Cache Files Read |
|---------|-----------------|
| §2 Sales Team | Q-01_step1_results.md, Q-01_step2_results.md, Q-04_results.md, Q-05_results.md, Q-06_results.md, Q-43_step1_results.md, Q-43_step2_results.md, Q-43_step3_results.md, Q-46_results.md |
| §3 Customers | Q-12_results.md, Q-13_results.md, Q-14_results.md, Q-17_results.md, Q-40_results.md, Q-41_results.md, Q-49_results.md |
| §4 Product | Q-07_results.md, Q-37_results.md, Q-38a_results.md, Q-39_results.md |
| §5 Commerce | Q-18_results.md, Q-16_results.md, Q-20_results.md, Q-21_results.md, Q-45_results.md |
| §6 Portal | Q-CL-01_results.md, Q-CL-03_results.md, Q-CL-05_results.md |
| §7 Peer | Q-CI-03_results.md, Q-CI-05_results.md, peer_benchmark_extract.md |
| §8 Platform | Q-08_results.md, Q-09_results.md, Q-10_results.md, Q-11_results.md, Q-22_results.md, Q-47_results.md, Q-50_results.md |

## Skipped Queries

| Query | Reason |
|-------|--------|
| Q-02 | Stage 2 derivation from Q-01 — not a SQL query |
| Q-03 | Stage 2 derivation from Q-01 — not a SQL query |
| Q-15 | Excluded from external scope (enrollment) |
| Q-19 | Derived from Q-18 Part A — not a separate cache file |
| Q-38b | pending_engineering — no invoice_date on sales_data |
| Q-42 | No products with new_item = true — no data |
| Q-44 | Excluded from external scope (enrollment) |
| Q-CL-02 | Not in conditional query list for Stage 1 |
| Q-CL-04 | Not in conditional query list for Stage 1 |
