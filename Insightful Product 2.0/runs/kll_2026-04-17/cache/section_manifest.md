# Section Manifest — Kuzco Lighting Inc. (kll, org_id=166)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Section Inclusion

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | SKIP | HAS_SALES_SECTION = false (4 qualifying reps, need 5) | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true (no sales_data; inventory-only) | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | INCLUDE | HAS_CLICKY = true (prefix: kuzco_kll_eol) | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier1 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping

### §2 Sales Team Performance — SKIP
- Q-01 (Rep Behavioral Scorecard): SKIPPED — HAS_SALES_SECTION = false
- Q-02 (Selling Archetype): SKIPPED — Stage 2 derivation, depends on Q-01
- Q-03 (Funnel Gap Analysis): SKIPPED — Stage 2 derivation, depends on Q-01
- Q-06 (Rep Engagement Trajectory): SKIPPED — HAS_SALES_SECTION = false
- Q-43 (Territory Coverage): SKIPPED — HAS_SALES_SECTION = false

### §3 Customer & Buyer Intelligence — INCLUDE
- Q-12 (Customer Activation): `Q-12_results.md` ✓
- Q-13 (Customer Concentration): `Q-13_results.md` ✓
- Q-14 (Reorder Velocity): `Q-14_results.md` ✓
- Q-17 (Dormant Customers): `Q-17_results.md` ✓
- Q-41 (First-Time eCat Orderers): `Q-41_results.md` ✓
- Q-40 (Regional Distribution): `Q-40_results.md` ✓

### §4 Product & Inventory Intelligence — INCLUDE (partial)
- Q-07 (Catalog Completeness): `Q-07_results.md` ✓
- Q-37 (OOS Top Sellers): SKIPPED — HAS_SALES_DATA = false
- Q-38a (Product Velocity): SKIPPED — ecat_item_number not populated in portal_order_items
- Q-39 (Line Analysis): SKIPPED — HAS_SALES_DATA = false
- Q-42 (New Item Performance): SKIPPED — HAS_SALES_DATA = false

### §5 Commerce Analytics — INCLUDE
- Q-18 Part A (eCat Order Trend): `Q-18_results.md` ✓
- Q-18 Part B (ERP Total Context): `Q-18_results.md` ✓
- Q-16 (ERP Total Business): `Q-16_results.md` ✓
- Q-20 (AOV Analysis): `Q-20_results.md` ✓
- Q-21 (Order Type/Workflow): `Q-21_results.md` ✓
- Q-45 (Capture Rate): SKIPPED — VM45_GATE_2 FAIL (eCat = 1.3% of ERP)
- Q-19 (Channel Mix): Derived from Q-18 Part A — HAS_CART = true

### §6 Portal Engagement — INCLUDE
- Q-CL-01 (Portal Traffic): `Q-CL-01_results.md` ✓
- Q-CL-03 (Geographic Demand): `Q-CL-03_results.md` ✓
- Q-CL-05 (Traffic Sources): `Q-CL-05_results.md` ✓

### §7 Peer Benchmarking — INCLUDE
- Q-CI-02 (Peer Comparison): `Q-CI-02_results.md` ✓
- Q-CI-03 (Feature Adoption): `Q-CI-03_results.md` ✓
- Q-CI-05 (Top Performers): `Q-CI-05_results.md` ✓
- Peer benchmark extract: `peer_benchmark_extract.md` ✓

### §8 Platform & Feature Utilization — INCLUDE
- Q-08 (Data Freshness): `Q-08_results.md` ✓
- Q-09 (Import Health): `Q-09_results.md` ✓
- Q-10 (Feature Enablement): `Q-10_results.md` ✓
- Q-11 (Configuration Completeness): `Q-11_results.md` ✓
- Q-22 (Feature Usage Depth): `Q-22_results.md` ✓

### Not Run (pending/internal)
- Q-38b: pending_engineering (no invoice_date on sales_data)
- Q-15, Q-44: Excluded from external scope (enrollment)
- Q-CI-04: Requires 2+ monthly snapshots (target: May 2026)
- VM-27, VM-28, VM-29: Internal only
