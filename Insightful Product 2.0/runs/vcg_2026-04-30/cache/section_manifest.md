# Section Manifest — Visual Comfort Signature (vcg, org_id=141)
- **Run date**: 2026-04-30
- **Report mode**: Mode 1: Standard Intelligence Report
- **Profile**: deep_intelligence (default)

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (15 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | SKIP | HAS_CLICKY = false | — |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier1 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| Cache File | Query | Section(s) |
|-----------|-------|-----------|
| Q-01_step1_results.md | Q-01 Step 1 (Mixpanel behavioral) | §2 Sales |
| Q-01_step2_results.md | Q-01 Step 2 (Postgres iPad orders by rep) | §2 Sales |
| Q-04_results.md | Q-04 (Non-selling user classification) | §2 Sales |
| Q-05_results.md | Q-05 (Seat utilization) | §2 Sales, §8 Platform |
| Q-06_results.md | Q-06 (Rep engagement trajectory) | §2 Sales |
| Q-07_results.md | Q-07 (Catalog completeness) | §4 Product, §8 Platform |
| Q-08_results.md | Q-08 (Data freshness) | §8 Platform |
| Q-09_results.md | Q-09 (Import health) | §8 Platform |
| Q-10_results.md | Q-10 (Feature enablement) | §8 Platform |
| Q-11_results.md | Q-11 (Configuration completeness) | §8 Platform |
| Q-12_results.md | Q-12 (Customer activation) | §3 Customers |
| Q-13_results.md | Q-13 (Customer concentration) | §5 Commerce |
| Q-14_results.md | Q-14 (Reorder frequency) | §3 Customers |
| Q-17_results.md | Q-17 (Dormant customers) | §3 Customers |
| Q-18_results.md | Q-18 Part A (eCat order trend) | §5 Commerce |
| Q-20_results.md | Q-20 (AOV analysis) | §5 Commerce |
| Q-21_results.md | Q-21 (Order type & workflow) | §5 Commerce |
| Q-22_results.md | Q-22 (Feature usage depth) | §8 Platform |
| Q-37_results.md | Q-37 (OOS top sellers) | §4 Product |
| Q-39_results.md | Q-39 (Line analysis) | §4 Product |
| Q-40_results.md | Q-40 (Regional distribution) | §3 Customers |
| Q-41_results.md | Q-41 (First-time eCat orderers) | §3 Customers |
| Q-42_results.md | Q-42 (New item performance) | §4 Product |
| Q-43_results.md | Q-43 (Territory coverage) | §2 Sales |
| Q-46_results.md | Q-46 (Workflow maturity) | §8 Platform |
| Q-47_results.md | Q-47 (Smart stack effectiveness) | §8 Platform |
| Q-50_results.md | Q-50 (Library engagement) | §8 Platform |
| Q-CI-01_results.md | Q-CI-01 (Org summary) | §7 Peer |
| Q-CI-03_results.md | Q-CI-03 (Feature adoption benchmark) | §7 Peer |
| Q-CI-05_results.md | Q-CI-05 (Top performers) | §7 Peer |
| peer_benchmark_extract.md | Peer benchmark CSV extract | §7 Peer |
| showroom_scan_results.md | Showroom/operational account scan | §2 Sales |

## Skipped Queries

| Query | Reason |
|-------|--------|
| Q-02 | Stage 2 derivation (from Q-01 data) — not a SQL query |
| Q-03 | Stage 2 derivation (from Q-01 data) — not a SQL query |
| Q-15 | Excluded from external scope (enrollment) |
| Q-16 | HAS_PORTAL_ORDERS = false |
| Q-18 Part B | HAS_PORTAL_ORDERS = false |
| Q-19 | HAS_CART = false (derived from Q-18 Part A) |
| Q-38a | portal_order_items_count = 0 |
| Q-38b | pending_engineering (no invoice_date on sales_data) |
| Q-44 | Excluded from external scope (enrollment) |
| Q-45 | HAS_PORTAL_ORDERS = false |
| Q-49 | HAS_PORTAL_ORDERS = false |
| Q-CL-01 through Q-CL-05 | HAS_CLICKY = false |
| Q-CI-04 | Pending — requires 2+ monthly peer benchmark snapshots (only 2 exist, but May 2026 target) |
