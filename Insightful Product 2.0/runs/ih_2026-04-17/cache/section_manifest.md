# Section Manifest — Interlude Home (ih, org_id=164)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report
- **Profile**: deep_intelligence (default)

## Section Inclusion Status

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (28 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | INCLUDE | HAS_CLICKY = true | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, PEER_GROUP_LEVEL = tier2 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| Cache File | Section(s) |
|-----------|-----------|
| Q-01_step1_results.md | §2 Sales Team |
| Q-01_step2_results.md | §2 Sales Team |
| Q-04_results.md | §2 Sales Team (non-selling classification) |
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
| Q-18_results.md | §5 Commerce |
| Q-20_results.md | §5 Commerce |
| Q-21_results.md | §5 Commerce |
| Q-22_results.md | §8 Platform |
| Q-37_results.md | §4 Product |
| Q-39_results.md | §4 Product |
| Q-40_results.md | §3 Customers |
| Q-41_results.md | §3 Customers |
| Q-43_results.md | §2 Sales Team |
| Q-45_results.md | §5 Commerce |
| Q-46_results.md | §8 Platform |
| Q-47_results.md | §8 Platform |
| Q-49_results.md | §3 Customers |
| Q-50_results.md | §8 Platform |
| Q-CL-01_results.md | §6 Portal |
| Q-CL-03_results.md | §6 Portal |
| Q-CL-05_results.md | §6 Portal |
| Q-CI-02_results.md | §7 Peer |
| Q-CI-03_results.md | §7 Peer |
| Q-CI-05_results.md | §7 Peer |
| peer_benchmark_extract.md | §7 Peer |
| showroom_scan_results.md | §2 Sales Team (exclusions) |
| gate_flags.md | All sections (gating reference) |

## Skipped Queries

| Query | Reason |
|-------|--------|
| Q-02 | Stage 2 derivation from Q-01 (not SQL) |
| Q-03 | Stage 2 derivation from Q-01 (not SQL) |
| Q-15 | Internal only — enrollment excluded from external scope |
| Q-19 | HAS_CART = false — no eCat Online/server orders |
| Q-38a | Returned 0 rows — ecat_item_number not populated in portal_order_items for this org |
| Q-38b | pending_engineering — no invoice_date in sales_data |
| Q-42 | Executed but all new items show $0 ERP sales — included in cache but may not be surfaced |
| Q-44 | Internal only — enrollment excluded from external scope |
| Q-CI-04 | Growth trajectory requires 2+ monthly snapshots — only 2 available (borderline), target: May 2026 |
| Q-CL-02 | Not in required conditional query set |
| Q-CL-04 | Not in required conditional query set |
