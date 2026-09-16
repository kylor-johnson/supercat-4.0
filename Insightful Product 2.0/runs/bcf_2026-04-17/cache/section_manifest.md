# Section Manifest — Braxton Culler (bcf, org_id=171)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (20 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | SKIP | HAS_CLICKY = false | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier1 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| Cache File | Section(s) | Status |
|------------|-----------|--------|
| Q-01_step1_results.md | §2, §8 | EXECUTED — 71 rows (Mixpanel behavioral data) |
| Q-01_step2_results.md | §2 | EXECUTED — 38 reps (Postgres rep orders) |
| Q-04_results.md | §8 | EXECUTED — non-selling user classification from Mixpanel |
| Q-05_results.md | §8 | EXECUTED — seat utilization |
| Q-06_results.md | §2 | EXECUTED — rep engagement trajectory |
| Q-07_results.md | §4, §8 | EXECUTED — catalog completeness |
| Q-08_results.md | §8 | EXECUTED — data freshness |
| Q-09_results.md | §8 | EXECUTED — import health |
| Q-10_results.md | §8 | EXECUTED — feature enablement |
| Q-11_results.md | §8 | EXECUTED — configuration completeness |
| Q-12_results.md | §3 | EXECUTED — customer activation |
| Q-13_results.md | §3 | EXECUTED — customer concentration |
| Q-14_results.md | §3 | EXECUTED — reorder velocity |
| Q-16_results.md | §5 | EXECUTED — ERP total business visibility |
| Q-17_results.md | §3 | EXECUTED — dormant customers |
| Q-18_results.md | §5 | EXECUTED — eCat order trend |
| Q-20_results.md | §5 | EXECUTED — AOV analysis |
| Q-21_results.md | §5 | EXECUTED — order type & workflow |
| Q-22_results.md | §8 | EXECUTED — feature usage depth (BigQuery) |
| Q-37_results.md | §4 | EXECUTED — OOS top sellers |
| Q-38a_results.md | §4 | EXECUTED — product velocity |
| Q-39_results.md | §4 | EXECUTED — line analysis by category & collection |
| Q-40_results.md | §2 | EXECUTED — regional sales distribution |
| Q-41_results.md | §3 | EXECUTED — first-time eCat orderers by channel |
| Q-42_results.md | §4 | EXECUTED — new item performance |
| Q-43_results.md | §2 | EXECUTED — territory coverage & dormancy |
| Q-46_results.md | §5 | EXECUTED — eCat selling workflow maturity |
| Q-47_results.md | §4, §8 | EXECUTED — smart stack effectiveness |
| Q-49_results.md | §3 | EXECUTED — buyer-level repeat purchase |
| Q-50_results.md | §8 | EXECUTED — library/document engagement effectiveness |
| Q-CI-01_results.md | §7 | EXECUTED — org summary (BigQuery) |
| Q-CI-02_results.md | §7 | EXECUTED — segment peer comparison (BigQuery) |
| Q-CI-03_results.md | §7 | EXECUTED — feature adoption benchmarking (BigQuery) |
| Q-CI-05_results.md | §7 | EXECUTED — top performers & best practices (BigQuery) |
| peer_benchmark_extract.md | §7 | EXECUTED — peer benchmark CSV extract |
| showroom_scan_results.md | §5 | EXECUTED — 0 exclusions |

## Skipped Queries

| Query | Reason |
|-------|--------|
| Q-02 | NOT a SQL query — Stage 2 derivation from Q-01 data |
| Q-03 | NOT a SQL query — Stage 2 derivation from Q-01 data |
| Q-CL-* (all Clicky queries) | HAS_CLICKY = false — entire Portal Engagement section skipped |
| Q-45 | VM45_RENDER = false — capture rate data not meaningful |
