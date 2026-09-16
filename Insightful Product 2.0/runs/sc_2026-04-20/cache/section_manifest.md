# Section Manifest — Gabriella White (sc, org_id=69)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (91 qualifying reps) | section_02_sales_team.md |
| 3 | Customer &amp; Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product &amp; Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | INCLUDE | HAS_CLICKY = true (prefix: sc_retail_sc) | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true | section_07_peer.md |
| 8 | Platform &amp; Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| Cache File | Query | Section(s) |
|------------|-------|------------|
| Q-01_step1_results.md | Q-01 Step 1 (Mixpanel behavioral) | §2 Sales |
| Q-01_step2_results.md | Q-01 Step 2 (Postgres orders) | §2 Sales |
| Q-04_results.md | Q-04 (Non-selling user roles) | §2 Sales |
| Q-05_results.md | Q-05 (Seat utilization) | §2 Sales, §8 Platform |
| Q-06_results.md | Q-06 (Rep engagement trajectory) | §2 Sales |
| Q-07_results.md | Q-07 (Catalog completeness) | §4 Product, §8 Platform |
| Q-08_results.md | Q-08 (Data freshness) | §8 Platform |
| Q-09_results.md | Q-09 (Import health) | §8 Platform |
| Q-10_results.md | Q-10 (Feature enablement) | §8 Platform |
| Q-11_results.md | Q-11 (Configuration completeness) | §8 Platform |
| Q-12_results.md | Q-12 (Customer activation) | §3 Customers |
| Q-13_results.md | Q-13 (Customer concentration) | §5 Commerce |
| Q-14_results.md | Q-14 (Reorder velocity) | §3 Customers |
| Q-16_results.md | Q-16 (ERP total business) | §5 Commerce |
| Q-17_results.md | Q-17 (Dormant buyers) | §3 Customers |
| Q-18_partA_results.md | Q-18 Part A (eCat order trend) | §5 Commerce |
| Q-18_partB_results.md | Q-18 Part B (ERP total context) | §5 Commerce |
| Q-20_results.md | Q-20 (AOV analysis) | §5 Commerce |
| Q-21_results.md | Q-21 (Order type &amp; workflow) | §5 Commerce |
| Q-22_results.md | Q-22 (Feature usage depth) | §8 Platform |
| Q-37_results.md | Q-37 (OOS top sellers) | §4 Product |
| Q-38a_results.md | Q-38a (Product velocity) — PENDING | §4 Product |
| Q-39_category_results.md | Q-39 (Line analysis - category) | §4 Product |
| Q-39_collection_results.md | Q-39 (Line analysis - collection) | §4 Product |
| Q-40_results.md | Q-40 (Regional distribution) | §3 Customers |
| Q-41_channel_results.md | Q-41 (First-time buyers - by channel) | §3 Customers |
| Q-41_rep_results.md | Q-41 (First-time buyers - by rep) | §3 Customers |
| Q-42_results.md | Q-42 (New item performance) | §4 Product |
| Q-43_step1_results.md | Q-43 Step 1 (Territory customer base) | §2 Sales |
| Q-43_step3_results.md | Q-43 Step 3 (Territory gap) | §2 Sales |
| Q-46_results.md | Q-46 (Workflow maturity) | §8 Platform |
| Q-47_results.md | Q-47 (Smart stack effectiveness) | §8 Platform |
| Q-50_results.md | Q-50 (Library/document inventory) | §8 Platform |
| Q-CL-01_results.md | Q-CL-01 (Portal traffic) | §6 Portal |
| Q-CL-03_results.md | Q-CL-03 (Geographic demand) | §6 Portal |
| Q-CL-05_results.md | Q-CL-05 (Traffic sources) | §6 Portal |
| Q-CI-02_results.md | Q-CI-02 (Peer comparison) | §7 Peer |
| Q-CI-03_results.md | Q-CI-03 (Feature benchmarking) | §7 Peer |
| Q-CI-04_results.md | Q-CI-04 (Segment benchmarks monthly) | §7 Peer |
| peer_benchmark_extract.md | Peer benchmark CSV extract | §7 Peer |

## Skipped Queries

| Query | Reason |
|-------|--------|
| Q-02 | Stage 2 derivation from Q-01 — not a SQL query |
| Q-03 | Stage 2 derivation from Q-01 — not a SQL query |
| Q-15 | Excluded from external scope (enrollment) |
| Q-19 | HAS_CART = false; no server orders |
| Q-44 | Excluded from external scope (enrollment) |
| Q-45 | VM45_GATE_1 FAIL — eCat GMV exceeds ERP GMV; denominator invalid |
| Q-38b | pending_engineering — no invoice_date in sales_data |
| Q-49 | Buyer attribution check needed — deferred |
| Q-CI-05/06 | Top performers — need segment confirmation |
