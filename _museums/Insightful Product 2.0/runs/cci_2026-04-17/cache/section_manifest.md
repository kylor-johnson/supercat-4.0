# Section Manifest — Currey & Company (cci, org_id=161)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report
- **Profile**: deep_intelligence (default)

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (35 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | SKIP | HAS_CLICKY = false | — |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier1 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| Section | Cache Files Read |
|---------|-----------------|
| §2 Sales Team | Q-01_step1_results.md, Q-01_step2_results.md, Q-04_results.md, Q-05_results.md, Q-06_results.md, Q-43_step1_results.md, Q-43_step2_results.md, Q-43_step3_results.md, Q-46_results.md, showroom_scan_results.md |
| §3 Customer & Buyer | Q-12_results.md, Q-13_results.md, Q-14_results.md, Q-17_results.md, Q-40_results.md, Q-41_results.md, Q-49_results.md |
| §4 Product & Inventory | Q-07_results.md, Q-37_results.md, Q-38a_results.md, Q-39_results.md, Q-42_results.md |
| §5 Commerce Analytics | Q-18_results.md, Q-16_results.md, Q-20_results.md, Q-21_results.md, Q-45_results.md |
| §6 Portal Engagement | SKIP — HAS_CLICKY = false |
| §7 Peer Benchmarking | Q-CI-01_results.md, Q-CI-02_results.md, Q-CI-03_results.md, Q-CI-05_results.md, peer_benchmark_extract.md |
| §8 Platform & Feature | Q-07_results.md, Q-08_results.md, Q-09_results.md, Q-10_results.md, Q-11_results.md, Q-22_results.md, Q-47_results.md, Q-50_results.md |

## Skipped Queries

| Query | Reason |
|-------|--------|
| Q-02 | Stage 2 derivation (from Q-01 behavioral data) — not a SQL query |
| Q-03 | Stage 2 derivation (from Q-01 behavioral data) — not a SQL query |
| Q-15 | Internal only — excluded from external scope |
| Q-19 | HAS_CART = false — no eCat Online orders exist |
| Q-38b | pending_engineering — no invoice_date in sales_data |
| Q-44 | Internal only — excluded from external scope |
| Q-CL-01 through Q-CL-05 | HAS_CLICKY = false |
| Q-CI-04 | Requires 2+ monthly snapshots — only 2 exist, but growth trajectory not yet reliable |
