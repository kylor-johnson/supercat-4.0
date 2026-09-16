# Section Manifest — Jamie Young Company (jyc, org_id=76)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (35 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | INCLUDE | HAS_CLICKY = true | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

### §2 Sales Team Performance
- Q-01_step1_results.md (Mixpanel behavioral data — 92 users)
- Q-01_step2_results.md (Postgres rep orders — 56 reps, showroom exclusion applied)
- Q-04_results.md (Non-selling user classification — derived from Q-01 Step 1)
- Q-05_results.md (Seat utilization)
- Q-06_results.md (Rep engagement trajectory)
- Q-43_results.md (Territory coverage & dormancy)
- showroom_scan_results.md (Operational account exclusion evidence)
- Q-02 / Q-03: Stage 2 derivations — NOT cached (derived from Q-01 at assembly time)

### §3 Customer & Buyer Intelligence
- Q-12_results.md (Customer activation & ERP penetration)
- Q-13_results.md (Customer concentration risk)
- Q-14_results.md (Reorder frequency & velocity)
- Q-17_results.md (Dormant eCat customer identification)
- Q-40_results.md (Regional sales distribution)
- Q-41_results.md (First-time eCat orderers)

### §4 Product & Inventory Intelligence
- Q-07_results.md (Catalog completeness)
- Q-37_results.md (Inventory × Sales — OOS top sellers)
- Q-38a_results.md (Product velocity trend via portal_order_items)
- Q-39_results.md (Line analysis by category & collection)
- Q-42_results.md (New item performance)

### §5 Commerce Analytics
- Q-16_results.md (ERP total business visibility)
- Q-18_results.md (eCat order velocity & trend — Parts A + B)
- Q-20_results.md (AOV analysis)
- Q-21_results.md (Order type & workflow)
- Q-45: SKIPPED — VM45_GATE_1 FAIL (eCat GMV exceeds ERP GMV; partial sync)

### §6 Portal Engagement
- Q-CL-01_results.md (Portal traffic health)
- Q-CL-03_results.md (Geographic demand map)
- Q-CL-05_results.md (Traffic source intelligence)

### §7 Peer Benchmarking
- Q-CI-01_results.md (Org summary lookup)
- Q-CI-02_results.md (Peer comparison)
- Q-CI-03_results.md (Feature adoption benchmarking + segment benchmarks monthly)
- Q-CI-05_results.md (Top performers by segment)
- peer_benchmark_extract.md (Pre-extracted peer metrics)

### §8 Platform & Feature Utilization
- Q-08_results.md (Data freshness monitor)
- Q-09_results.md (Import health & sync reliability)
- Q-10_results.md (Feature enablement gap analysis)
- Q-11_results.md (Configuration completeness)
- Q-22_results.md (Feature usage depth)
- Q-46_results.md (eCat selling workflow maturity)
- Q-47_results.md (Smart stack effectiveness)
- Q-50_results.md (Library / document engagement)

## Skipped Queries

| Query | Reason |
|-------|--------|
| Q-02 | Stage 2 derivation from Q-01 — not a SQL query |
| Q-03 | Stage 2 derivation from Q-01 — not a SQL query |
| Q-15 | Excluded from external scope (enrollment) |
| Q-19 | Derived from Q-18 Part A at assembly time |
| Q-38b | pending_engineering — no invoice_date in sales_data |
| Q-44 | Excluded from external scope (enrollment) |
| Q-45 | VM45_GATE_1 FAIL — eCat GMV exceeds ERP GMV |
| Q-CI-04 | Pending — requires 2+ monthly snapshots (first available May 2026) |
| Q-CL-02 | Not in Stage 1 execution plan |
| Q-CL-04 | Not in Stage 1 execution plan |
