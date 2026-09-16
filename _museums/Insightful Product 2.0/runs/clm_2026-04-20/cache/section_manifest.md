# Section Manifest — Crystorama (clm, org_id=64)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (5 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | INCLUDE | HAS_CLICKY = true | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier1 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

| Cache File | Section(s) | Status |
|-----------|-----------|--------|
| Q-01_step1_results.md | §2 Sales Team | Executed |
| Q-01_step2_results.md | §2 Sales Team | Executed |
| Q-02 (derived from Q-01) | §2 Sales Team | Derived in Stage 2 |
| Q-03 (derived from Q-01) | §2 Sales Team | Derived in Stage 2 |
| Q-04 (derived from Q-01) | §8 Platform | Derived in Stage 2 |
| Q-05_results.md | §8 Platform | Executed |
| Q-06_results.md | §2 Sales Team | Executed |
| Q-07_results.md | §4 Product | Executed |
| Q-08_results.md | §8 Platform | Executed |
| Q-09_results.md | §8 Platform | Executed |
| Q-10_results.md | §8 Platform | Executed |
| Q-11_results.md | §8 Platform | Executed |
| Q-12_results.md | §3 Customer | Executed |
| Q-13_results.md | §3 Customer | Executed |
| Q-14_results.md | §3 Customer | Executed |
| Q-15 | — | Excluded (enrollment out of scope) |
| Q-16_results.md | §5 Commerce | Executed |
| Q-17_results.md | §3 Customer | Executed |
| Q-18_results.md | §5 Commerce | Executed (Parts A + B) |
| Q-19 (derived from Q-18) | §5 Commerce | Skipped (HAS_CART = false, 0 server orders) |
| Q-20_results.md | §5 Commerce | Executed |
| Q-21_results.md | §5 Commerce | Executed |
| Q-22_results.md | §8 Platform | Executed |
| Q-37_results.md | §4 Product | Executed |
| Q-38a | §4 Product | Not executed (portal_order_items gate not checked) |
| Q-39_results.md | §4 Product | Executed (category + collection) |
| Q-40_results.md | §5 Commerce | Executed |
| Q-41_results.md | §3 Customer | Executed (by month + by rep) |
| Q-42_results.md | §4 Product | Executed (summary) |
| Q-43_results.md | §2 Sales Team | Executed (territory mapping) |
| Q-44 | — | Excluded (enrollment out of scope) |
| Q-45 | §5 Commerce | Skipped (VM45_RENDER = false, Gate 2 failed) |
| Q-46_results.md | §5 Commerce, §8 Platform | Executed (Postgres + Mixpanel) |
| Q-47_results.md | §8 Platform | Executed (stack inventory) |
| Q-49_results.md | §3 Customer | Executed (portal + eCat repeat purchase) |
| Q-50_results.md | §8 Platform | Executed (document inventory + Mixpanel) |
| Q-CL-01_results.md | §6 Portal | Executed |
| Q-CL-03_results.md | §6 Portal | Executed |
| Q-CL-05_results.md | §6 Portal | Executed |
| Q-CI-03_results.md | §7 Peer | Executed |
| Q-CI-05_results.md | §7 Peer | Executed |
| gate_flags.md | All sections | Written |
| showroom_scan_results.md | §2 Sales Team | Written |
| peer_benchmark_extract.md | §7 Peer | Written |

## Skipped Queries (with reasons)

| Query | Reason |
|-------|--------|
| Q-15 | Enrollment excluded from external report scope |
| Q-19 | HAS_CART = false; 0 server-source eCat orders |
| Q-44 | Enrollment excluded from external report scope |
| Q-45 | VM45_RENDER = false (Gate 2 failed: eCat GMV < 5% of ERP total) |
| Q-CL-02 | Content performance requires page-level Clicky data not in aggregate tables |
| Q-CL-04 | Visitor organization identification requires ISP-level Clicky data not in aggregate tables |
