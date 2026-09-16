# Section Manifest — Sarreid, Ltd. (sarreid, org_id=1)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report
- **Profile**: deep_intelligence (default)

## Section Inclusion Status

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true (14 qualifying reps) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true, HAS_SALES_DATA = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | INCLUDE | HAS_CLICKY = true (prefix: sarreid_eol_portal) | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier2 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

### §2 Sales Team Performance
| Cache File | Query | Description |
|-----------|-------|-------------|
| Q-01_step1_results.md | Q-01 Step 1 | Rep behavioral data (BigQuery Mixpanel) |
| Q-01_step2_results.md | Q-01 Step 2 | Rep order outcomes (Postgres) |
| Q-04_results.md | Q-04 | Non-selling user classification |
| Q-05_results.md | Q-05 | Seat utilization |
| Q-06_results.md | Q-06 | Rep engagement trajectory |
| Q-43_results.md | Q-43 | Territory coverage & dormancy |
| showroom_scan_results.md | Derived | Showroom/operational exclusions |

Notes:
- Q-02 (archetypes) and Q-03 (funnel gaps) are Stage 2 derivations from Q-01 — no cache files produced
- Showroom exclusion: "Sarreid Showroom" excluded from rep leaderboard (1 account, $14,192.45)

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
| Q-37_results.md | Q-37 | Inventory × sales (OOS top sellers) |
| Q-38a_results.md | Q-38a | Product velocity trend (DATA GAP: ecat_item_number empty) |
| Q-39_results.md | Q-39 | Line analysis by category & collection |
| Q-42_results.md | Q-42 | New item performance |

Notes:
- Q-38a returned aggregate monthly data but no product-level detail (ecat_item_number empty for this org)
- Q-38b is pending_engineering (no invoice_date in sales_data)

### §5 Commerce Analytics
| Cache File | Query | Description |
|-----------|-------|-------------|
| Q-18_results.md | Q-18 | eCat order velocity & trend (Parts A + B) |
| Q-20_results.md | Q-20 | eCat AOV analysis |
| Q-21_results.md | Q-21 | eCat order type & workflow |
| Q-16_results.md | Q-16 | ERP total business visibility |
| Q-45_results.md | Q-45 | eCat capture rate vs. total business |
| Q-46_results.md | Q-46 | eCat selling workflow maturity |

Notes:
- Q-19 (channel mix evolution) SKIPPED — HAS_CART = false (0 server orders)
- Q-49 (buyer-level repeat purchase) NOT RUN — would need explicit gate check; portal_orders buyer attribution present but not required for standard run

### §6 Portal Engagement
| Cache File | Query | Description |
|-----------|-------|-------------|
| Q-CL-01_results.md | Q-CL-01 | Portal traffic health |
| Q-CL-03_results.md | Q-CL-03 | Geographic demand map |
| Q-CL-04_results.md | Q-CL-04 | Visitor organization identification |
| Q-CL-05_results.md | Q-CL-05 | Traffic source intelligence |

Notes:
- Q-CL-02 (portal content performance / pages) NOT RUN — not in standard §2.2 conditional list
- Clicky schema: alternative (title/value) variant confirmed
- bounce_rate excluded per permanent exclusion policy

### §7 Peer Benchmarking
| Cache File | Query | Description |
|-----------|-------|-------------|
| peer_benchmark_extract.md | Peer CSV | Pre-extracted benchmark data |
| Q-CI-03_results.md | Q-CI-03 | Feature adoption benchmarking |
| Q-CI-05_results.md | Q-CI-05 | Top-performer patterns |

Notes:
- Q-CI-01 data captured in gate_flags.md (org_summary)
- Q-CI-02 data captured from segment_peer_comparison (in gate_flags.md)
- Q-CI-04 (growth trajectory) SKIPPED — requires 2+ monthly snapshots; only 2 available (Mar + Apr 2026), first available May 2026 for time-series

### §8 Platform & Feature Utilization
| Cache File | Query | Description |
|-----------|-------|-------------|
| Q-08_results.md | Q-08 | Data freshness monitor |
| Q-09_results.md | Q-09 | Import health & sync reliability |
| Q-10_results.md | Q-10 | Feature enablement gap analysis |
| Q-11_results.md | Q-11 | Configuration completeness |
| Q-22_results.md | Q-22 | Feature usage depth |
| Q-47_results.md | Q-47 | Smart stack effectiveness |
| Q-50_results.md | Q-50 | Library/document engagement |

## Queries Skipped

| Query | Reason |
|-------|--------|
| Q-02 | Stage 2 derivation (not a SQL query) |
| Q-03 | Stage 2 derivation (not a SQL query) |
| Q-15 | Excluded from external scope (enrollment) |
| Q-19 | HAS_CART = false (0 server orders) |
| Q-38b | pending_engineering (no invoice_date in sales_data) |
| Q-44 | Excluded from external scope (enrollment) |
| Q-CI-04 | Pending — requires 2+ monthly snapshots (target: May 2026) |
| Q-HS-* | Internal only (HelpScout) |
| Q-27 | Internal only (health score — superseded by Health V2) |
