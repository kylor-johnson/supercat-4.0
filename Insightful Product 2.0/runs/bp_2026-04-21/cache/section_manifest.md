# Section Manifest — Buster & Punch (bp, org_id=250)
- **Run date**: 2026-04-21
- **Report mode**: Mode 1: Standard Intelligence Report

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | SKIP | HAS_SALES_SECTION = false (0 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true (3,417 rows). Note: HAS_SALES_DATA = false — product velocity, line analysis, and OOS queries skipped | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | SKIP | HAS_CLICKY = false | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

### §2 Sales Team Performance (SKIP)
| Query | Status | Reason |
|-------|--------|--------|
| Q-01 | SKIPPED | HAS_SALES_SECTION = false |
| Q-02 | SKIPPED | Derived from Q-01 (not run) |
| Q-03 | SKIPPED | Derived from Q-01 (not run) |
| Q-06 | SKIPPED | HAS_SALES_SECTION = false |
| Q-43 | SKIPPED | HAS_SALES_SECTION = false |

### §3 Customer & Buyer Intelligence (INCLUDE)
| Query | Status | Cache File |
|-------|--------|------------|
| Q-12 | RAN | Q-12_results.md |
| Q-13 | RAN | Q-13_results.md |
| Q-14 | RAN | Q-14_results.md (0 rows — no customers with ≥3 LTM orders) |
| Q-17 | RAN | Q-17_results.md |
| Q-40 | RAN | Q-40_results.md |
| Q-41 | RAN | Q-41_results.md |

### §4 Product & Inventory Intelligence (INCLUDE — partial)
| Query | Status | Cache File |
|-------|--------|------------|
| Q-07 | RAN | Q-07_results.md |
| Q-37 | SKIPPED | HAS_SALES_DATA = false |
| Q-38a | SKIPPED | portal_order_items = 0 |
| Q-39 | SKIPPED | HAS_SALES_DATA = false |
| Q-42 | SKIPPED | HAS_SALES_DATA = false |

### §5 Commerce Analytics (INCLUDE)
| Query | Status | Cache File |
|-------|--------|------------|
| Q-18 Part A | RAN | Q-18_results.md |
| Q-18 Part B | SKIPPED | HAS_PORTAL_ORDERS = false |
| Q-20 | RAN | Q-20_results.md |
| Q-21 | RAN | Q-21_results.md |
| Q-16 | SKIPPED | HAS_PORTAL_ORDERS = false |
| Q-45 | SKIPPED | HAS_PORTAL_ORDERS = false (VM45_RENDER = false) |

### §6 Portal Engagement (SKIP)
| Query | Status | Reason |
|-------|--------|--------|
| Q-CL-01 | SKIPPED | HAS_CLICKY = false |
| Q-CL-03 | SKIPPED | HAS_CLICKY = false |
| Q-CL-05 | SKIPPED | HAS_CLICKY = false |

### §7 Peer Benchmarking (INCLUDE)
| Query | Status | Cache File |
|-------|--------|------------|
| Q-CI-01 | RAN | Q-CI-01_results.md |
| Q-CI-02 | RAN | Q-CI-02_results.md |
| Q-CI-03 | RAN | Q-CI-03_results.md |
| Q-CI-05 | RAN | Q-CI-05_results.md |

### §8 Platform & Feature Utilization (INCLUDE)
| Query | Status | Cache File |
|-------|--------|------------|
| Q-08 | RAN | Q-08_results.md |
| Q-09 | RAN | Q-09_results.md |
| Q-10 | RAN | Q-10_results.md |
| Q-11 | RAN | Q-11_results.md |
| Q-22 | RAN | Q-22_results.md |
| Q-05 | RAN | Q-05_results.md |
