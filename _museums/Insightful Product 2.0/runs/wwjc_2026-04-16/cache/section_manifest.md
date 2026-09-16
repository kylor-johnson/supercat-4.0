# Section Manifest — Wildwood/Chelsea House (wwjc)
- **Run date**: 2026-04-16
- **Report mode**: Mode 1: Standard Intelligence Report

## Section Status

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (22 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true AND HAS_SALES_DATA = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | SKIP | HAS_CLICKY = false | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier1 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

### §2 Sales Team Performance
- `Q-01_step1_results.md` — Mixpanel behavioral data (74 users)
- `Q-01_step2_results.md` — Rep iPad order leaderboard (41 reps)
- `Q-04_results.md` — Non-selling user classification (74 users)
- `Q-05_results.md` — Seat utilization
- `Q-06_results.md` — Rep engagement trajectory (55 entries)
- `Q-43_results.md` — Territory coverage & dormancy (40 territories)
- `showroom_scan_results.md` — Operational account exclusions (1 confirmed)

### §3 Customer & Buyer Intelligence
- `Q-12_results.md` — Customer activation & ERP penetration
- `Q-13_results.md` — Customer concentration risk (top 15)
- `Q-14_results.md` — Reorder frequency & velocity (top 20)
- `Q-17_results.md` — Dormant eCat customer identification (25 lapsed + 20 at-risk)
- `Q-40_results.md` — Regional sales distribution (top 20 states)
- `Q-41_results.md` — First-time eCat orderers (32 month×channel rows + 42 reps)

### §4 Product & Inventory Intelligence
- `Q-07_results.md` — Catalog completeness (1 visibility group)
- `Q-37_results.md` — OOS top sellers (20 items)
- `Q-38a_results.md` — Product velocity trend (large — 6mo × items)
- `Q-39_results.md` — Line analysis by category (43 categories) + collection (25 collections)
- `Q-42_results.md` — New item performance (1 row — sparse data)

### §5 Commerce Analytics
- `Q-18_results.md` — eCat order trend Part A (13 months) + Part B ERP context (13 months)
- `Q-20_results.md` — AOV by channel (4 dimensions)
- `Q-21_results.md` — Order type & workflow (3 types)
- `Q-16_results.md` — ERP total business visibility (13 months)
- `Q-45_results.md` — eCat capture rate vs. total business

### §6 Portal Engagement — SKIPPED
- No cache files (HAS_CLICKY = false)

### §7 Peer Benchmarking
- `peer_benchmark_extract.md` — Pre-extracted peer data from benchmark CSV
- `Q-CI-03_results.md` — Feature adoption benchmarking + segment benchmarks monthly
- `Q-CI-05_results.md` — Top-performer patterns (anonymized)

### §8 Platform & Feature Utilization
- `Q-08_results.md` — Data freshness (22 entity types)
- `Q-09_results.md` — Import pipeline health (7 months + 10 recent imports)
- `Q-10_results.md` — Feature enablement gap analysis
- `Q-11_results.md` — Configuration completeness (14 stale entities)
- `Q-22_results.md` — Feature usage depth (org-level)
