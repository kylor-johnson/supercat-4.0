# Section Manifest — Jonathan Charles Fine Furniture Ltd. (jc, org_id=65)
- **Run date**: 2026-04-21
- **Report mode**: Mode 1: Standard Intelligence Report

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | SKIP | HAS_SALES_SECTION = false (1 qualifying rep, need 5) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | SKIP | HAS_CLICKY = false | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier2 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

### §3 Customer & Buyer Intelligence
| Cache File | Query | Description |
|-----------|-------|-------------|
| Q-12_results.md | Q-12 | Customer activation & ERP penetration |
| Q-13_results.md | Q-13 | Customer concentration risk |
| Q-14_results.md | Q-14 | Customer reorder frequency & velocity |
| Q-17_results.md | Q-17 | Dormant eCat customer identification |
| Q-41_results.md | Q-41 | First-time eCat orderers by channel & rep |
| Q-40_results.md | Q-40 | Regional sales distribution |

### §4 Product & Inventory Intelligence
| Cache File | Query | Description |
|-----------|-------|-------------|
| Q-07_results.md | Q-07 | Catalog completeness score |
| Q-37_results.md | Q-37 | Inventory × Sales intelligence (OOS top sellers) |
| Q-38a_results.md | Q-38a | Product velocity trend (portal_order_items) |
| Q-39_results.md | Q-39 | Line analysis by category & collection |
| Q-42_results.md | Q-42 | New item performance |

### §5 Commerce Analytics
| Cache File | Query | Description |
|-----------|-------|-------------|
| Q-18_results.md | Q-18 | eCat order velocity & trend (Part A + Part B) |
| Q-20_results.md | Q-20 | eCat AOV analysis |
| Q-21_results.md | Q-21 | eCat order type & workflow analysis |
| Q-16_results.md | Q-16 | ERP total business visibility |
| Q-45_results.md | Q-45 | eCat capture rate vs total business |

### §7 Peer Benchmarking
| Cache File | Query | Description |
|-----------|-------|-------------|
| peer_benchmark_extract.md | CSV extract | Peer benchmark data for jc |
| Q-CI-03_results.md | Q-CI-03 | Feature adoption benchmarking |
| Q-CI-05_results.md | Q-CI-05 | Top performer patterns (anonymized) |

### §8 Platform & Feature Utilization
| Cache File | Query | Description |
|-----------|-------|-------------|
| Q-08_results.md | Q-08 | Data freshness monitor |
| Q-09_results.md | Q-09 | Import health & sync reliability |
| Q-10_results.md | Q-10 | Feature enablement gap analysis |
| Q-11_results.md | Q-11 | Configuration completeness |
| Q-22_results.md | Q-22 | Feature usage depth |

## Skipped Queries

| Query | Reason | Section |
|-------|--------|---------|
| Q-01, Q-02, Q-03, Q-04, Q-05, Q-06, Q-43 | HAS_SALES_SECTION = false | §2 Sales Team |
| Q-19 | HAS_CART = false (no server orders) | §5 Commerce (channel mix) |
| Q-CL-01 through Q-CL-05 | HAS_CLICKY = false | §6 Portal Engagement |
| Q-15, Q-44 | Excluded from external scope (enrollment) | N/A |
| Q-CI-04 | Pending — requires 2+ monthly snapshots (target May 2026) | §7 Peer (growth trajectory) |
| Q-38b | pending_engineering — no invoice_date in sales_data | §4 Product |
