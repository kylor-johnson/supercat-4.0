# Section Manifest — Kaleen Rugs & Broadloom (krb, org_id=244)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report
- **Profile**: deep_intelligence (default)

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | **SKIP** | HAS_SALES_SECTION = false (0 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true (note: inventory is Stale — 255 days) | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | **SKIP** | HAS_CLICKY = false | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier1 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

### §2 Sales Team Performance — SKIP
| Query | Status | Reason |
|-------|--------|--------|
| Q-01 Step 1 | RAN (derived gate only) | Mixpanel user data check — 8 rows cached |
| Q-01 Step 2 | SKIPPED | HAS_SALES_SECTION = false |
| Q-02 | N/A | Stage 2 derivation from Q-01 — not a SQL query |
| Q-03 | N/A | Stage 2 derivation from Q-01 — not a SQL query |
| Q-06 | SKIPPED | HAS_SALES_SECTION = false |
| Q-43 | SKIPPED | HAS_SALES_SECTION = false |

### §3 Customer & Buyer Intelligence — INCLUDE
| Query | Status | Cache File | Rows |
|-------|--------|-----------|------|
| Q-12 | RAN | Q-12_results.md | 1 |
| Q-13 | RAN | Q-13_results.md | 0 |
| Q-14 | RAN | Q-14_results.md | 0 |
| Q-17 | RAN | Q-17_results.md | 0 |
| Q-41 | RAN | Q-41_results.md | 1+1 |
| Q-40 | RAN | Q-40_results.md | 0 |

### §4 Product & Inventory Intelligence — INCLUDE
| Query | Status | Reason |
|-------|--------|--------|
| Q-07 | RAN | Q-07_results.md — 1 row |
| Q-37 | SKIPPED | HAS_SALES_DATA = false |
| Q-38a | SKIPPED | portal_order_items_count = 0 |
| Q-39 | SKIPPED | HAS_SALES_DATA = false |
| Q-42 | SKIPPED | HAS_SALES_DATA = false |

### §5 Commerce Analytics — INCLUDE
| Query | Status | Cache File | Rows |
|-------|--------|-----------|------|
| Q-18 Part A | RAN | Q-18_step1_results.md | 1 |
| Q-18 Part B | SKIPPED | HAS_PORTAL_ORDERS = false |
| Q-20 | RAN | Q-20_results.md | 4 |
| Q-21 | RAN | Q-21_results.md | 1 |
| Q-45 | SKIPPED | HAS_PORTAL_ORDERS = false |
| Q-16 | SKIPPED | HAS_PORTAL_ORDERS = false |

### §6 Portal Engagement — SKIP
| Query | Status | Reason |
|-------|--------|--------|
| Q-CL-01 | SKIPPED | HAS_CLICKY = false |
| Q-CL-03 | SKIPPED | HAS_CLICKY = false |
| Q-CL-05 | SKIPPED | HAS_CLICKY = false |

### §7 Peer Benchmarking — INCLUDE
| Query | Status | Cache File | Rows |
|-------|--------|-----------|------|
| Q-CI-02 | RAN | Q-CI-02_results.md | 1 |
| Q-CI-03 | RAN | Q-CI-03_results.md | 1+2 |
| Q-CI-05 | RAN | Q-CI-05_results.md | 10 |
| Peer CSV | EXTRACTED | peer_benchmark_extract.md | 1 |

### §8 Platform & Feature Utilization — INCLUDE
| Query | Status | Cache File | Rows |
|-------|--------|-----------|------|
| Q-05 | RAN | Q-05_results.md | 1 |
| Q-08 | RAN | Q-08_results.md | 22 |
| Q-09 | RAN | Q-09_results.md | 1+10 |
| Q-10 | RAN | Q-10_results.md | 0 (no mobile_sites row) |
| Q-11 | RAN | Q-11_results.md | 22 |
| Q-22 | RAN | Q-22_results.md | 1 |

## Skipped Queries Summary

| Query | Gate | Reason |
|-------|------|--------|
| Q-01 Step 2 | HAS_SALES_SECTION = false | 0 qualifying reps |
| Q-06 | HAS_SALES_SECTION = false | 0 qualifying reps |
| Q-43 | HAS_SALES_SECTION = false | 0 qualifying reps |
| Q-16 | HAS_PORTAL_ORDERS = false | 0 LTM portal_orders |
| Q-18 Part B | HAS_PORTAL_ORDERS = false | 0 LTM portal_orders |
| Q-45 | HAS_PORTAL_ORDERS = false | No denominator |
| Q-37 | HAS_SALES_DATA = false | 0 sales_data rows |
| Q-38a | portal_order_items = 0 | No line item data |
| Q-39 | HAS_SALES_DATA = false | 0 sales_data rows |
| Q-42 | HAS_SALES_DATA = false | 0 sales_data rows |
| Q-CL-01 | HAS_CLICKY = false | No Clicky analytics |
| Q-CL-03 | HAS_CLICKY = false | No Clicky analytics |
| Q-CL-05 | HAS_CLICKY = false | No Clicky analytics |
