# Section Manifest — Palecek (pf, org_id=32)
- **Run date**: 2026-04-21
- **Report mode**: Mode 1: Standard Intelligence Report

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (31 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true (qty only) | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | INCLUDE | HAS_CLICKY = true (prefix: palecek_eol_trial) | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = True, tier2 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| Cache File | Section(s) |
|-----------|------------|
| Q-01_step1_results.md | §2 Sales Team |
| Q-01_step2_results.md | §2 Sales Team |
| Q-04_results.md | §2 Sales Team (non-selling roles) |
| Q-05_results.md | §8 Platform |
| Q-06_results.md | §2 Sales Team |
| Q-07_results.md | §4 Product, §8 Platform |
| Q-08_results.md | §8 Platform |
| Q-09_results.md | §8 Platform |
| Q-10_results.md | §8 Platform |
| Q-11_results.md | §8 Platform |
| Q-12_results.md | §3 Customers |
| Q-13_results.md | §5 Commerce |
| Q-14_results.md | §3 Customers |
| Q-16_results.md | §5 Commerce |
| Q-17_results.md | §3 Customers |
| Q-18_partA_results.md | §5 Commerce |
| Q-18_partB_results.md | §5 Commerce |
| Q-20_results.md | §5 Commerce |
| Q-21_results.md | §5 Commerce |
| Q-22_results.md | §8 Platform |
| Q-38a_results.md | §4 Product |
| Q-40_results.md | §3 Customers |
| Q-41_results.md | §3 Customers |
| Q-42_results.md | §4 Product |
| Q-43_step1_results.md | §2 Sales Team |
| Q-43_step2_results.md | §2 Sales Team |
| Q-43_step3_results.md | §2 Sales Team |
| Q-46_results.md | §8 Platform |
| Q-47_results.md | §4 Product |
| Q-49_results.md | §3 Customers |
| Q-50_results.md | §4 Product |
| Q-CL-01_results.md | §6 Portal |
| Q-CL-03_results.md | §6 Portal |
| Q-CI-02_results.md | §7 Peer |
| Q-CI-03_results.md | §7 Peer |
| Q-CI-05_results.md | §7 Peer |
| peer_benchmark_extract.md | §7 Peer |
| showroom_scan_results.md | §2 Sales Team |
| user_group_mapping.md | §8 Platform |
| gate_flags.md | All sections |

## Skipped Queries

| Query | Reason |
|-------|--------|
| Q-02 | Stage 2 derivation from Q-01 (not a SQL query) |
| Q-03 | Stage 2 derivation from Q-01 (not a SQL query) |
| Q-15 | Excluded from external scope (enrollment) |
| Q-19 | HAS_CART = false — no server orders |
| Q-37 | Data-gated: sales_data.amount_invoiced is NULL for all rows (ERP join guard fails) |
| Q-38b | pending_engineering — no invoice_date in sales_data |
| Q-39 | Data-gated: sales_data.amount_invoiced is NULL for all rows |
| Q-44 | Excluded from external scope (enrollment) |
| Q-45 | VM45_GATE_1 FAIL — eCat GMV exceeds ERP GMV |
| Q-CL-02 | Not attempted — page-level Clicky data not in scope for Stage 1 |
| Q-CL-04 | Not attempted — organization identification table not confirmed |
| Q-CL-05 | Alternative schema (title/value) — traffic_sources table uses non-standard column names; query attempted but column 'source' not found. Needs schema adaptation. |
| Q-CI-04 | Requires 2+ monthly snapshots — only 2 available (March and April 2026). Minimally eligible but data is very recent. |
