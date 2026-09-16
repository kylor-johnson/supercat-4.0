# Section Manifest — Visual Comfort - Studio /Fans (fms, org_id=108)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report
- **Profile**: deep_intelligence (default)

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (23 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | INCLUDE | HAS_CLICKY = true (note: near-zero traffic — section will be thin) | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier1 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

### §2 Sales Team Performance
| Cache File | Query | Description |
|-----------|-------|-------------|
| Q-01_step1_results.md | Q-01 Step 1 | Rep behavioral scorecard (BigQuery Mixpanel) |
| Q-01_step2_results.md | Q-01 Step 2 | Rep order outcomes (Postgres) |
| Q-04_results.md | Q-04 | Non-selling user role classification (BigQuery Mixpanel) — derived from Q-01 Step 1 |
| Q-05_results.md | Q-05 | Seat utilization |
| Q-06_results.md | Q-06 | Rep engagement trajectory |
| Q-43_step1_results.md | Q-43 Step 1 | Territory coverage (customer-side) |
| Q-43_step2_results.md | Q-43 Step 2 | eCat order activity by customer |
| Q-43_step3_results.md | Q-43 Step 3 | Territory gap summary |
| Q-46_results.md | Q-46 | eCat selling workflow maturity |
| showroom_scan_results.md | — | Showroom/operational account exclusions |

### §3 Customer & Buyer Intelligence
| Cache File | Query | Description |
|-----------|-------|-------------|
| Q-12_results.md | Q-12 | Customer activation & ERP penetration |
| Q-13_results.md | Q-13 | Customer concentration risk |
| Q-14_results.md | Q-14 | Customer reorder frequency |
| Q-17_results.md | Q-17 | Dormant eCat customer identification |
| Q-40_results.md | Q-40 | Regional sales distribution |
| Q-41_results.md | Q-41 | First-time eCat orderers |

### §4 Product & Inventory Intelligence
| Cache File | Query | Description |
|-----------|-------|-------------|
| Q-07_results.md | Q-07 | Catalog completeness |
| Q-37_results.md | Q-37 | Inventory × Sales (OOS top sellers) |
| Q-39_results.md | Q-39 | Line analysis by category & collection |
| Q-47_results.md | Q-47 | Smart stack effectiveness |
| Q-50_results.md | Q-50 | Library/document engagement |

### §5 Commerce Analytics
| Cache File | Query | Description |
|-----------|-------|-------------|
| Q-18_results.md | Q-18 Part A | eCat order velocity & trend |
| Q-20_results.md | Q-20 | eCat AOV analysis |
| Q-21_results.md | Q-21 | eCat order type & workflow |

### §6 Portal Engagement
| Cache File | Query | Description |
|-----------|-------|-------------|
| Q-CL-01_results.md | Q-CL-01 | Portal traffic health (near-zero data) |

### §7 Peer Benchmarking
| Cache File | Query | Description |
|-----------|-------|-------------|
| Q-CI-01_results.md | Q-CI-01 | Org summary lookup |
| Q-CI-02_results.md | Q-CI-02 | Peer comparison |
| Q-CI-03_results.md | Q-CI-03 | Feature adoption benchmarking |
| Q-CI-05_results.md | Q-CI-05 | Top-performer patterns |
| peer_benchmark_extract.md | — | Peer benchmark CSV extract |

### §8 Platform & Feature Utilization
| Cache File | Query | Description |
|-----------|-------|-------------|
| Q-08_results.md | Q-08 | Data freshness |
| Q-09_results.md | Q-09 | Import health |
| Q-10_results.md | Q-10 | Feature enablement |
| Q-11_results.md | Q-11 | Configuration completeness |
| Q-22_results.md | Q-22 | Feature usage depth |

## Skipped Queries

| Query | Reason |
|-------|--------|
| Q-02 | Stage 2 derivation from Q-01 — not a SQL query |
| Q-03 | Stage 2 derivation from Q-01 — not a SQL query |
| Q-15 | Internal only — enrollment excluded from external scope |
| Q-16 | HAS_PORTAL_ORDERS = false |
| Q-18 Part B | HAS_PORTAL_ORDERS = false |
| Q-19 | HAS_CART = false — no server-source orders |
| Q-38a | portal_order_items_count = 0 |
| Q-38b | pending_engineering — no invoice_date in sales_data |
| Q-42 | No products with new_item = true |
| Q-44 | Internal only — enrollment excluded from external scope |
| Q-45 | HAS_PORTAL_ORDERS = false — no denominator |
| Q-49 | HAS_PORTAL_ORDERS = false — no buyer attribution |
| Q-CL-02 | Near-zero traffic data — insufficient for page-level analysis |
| Q-CL-03 | Near-zero traffic data — insufficient for geographic analysis |
| Q-CL-04 | Near-zero traffic data — insufficient for org identification |
| Q-CL-05 | Near-zero traffic data — insufficient for source analysis |
| Q-CI-04 | 2 monthly snapshots available but growth trajectory requires different-period comparison |
