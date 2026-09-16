# Section Manifest — Kindel Karges Furniture (kkc, org_id=99)
- **Run date**: 2026-04-23
- **Report mode**: Mode 3: Platform Reactivation Report
- **Report type label**: Partnership Overview
- **Report badge**: Partnership Overview · Platform Configuration as of 2026-04-23

## Section Inclusion (Mode 3 Assembly)

| § | Section | Status | Gate | Notes |
|---|---------|--------|------|-------|
| 1 | Overview | INCLUDE | Always (written last) | Replaces Executive Summary for Mode 3 |
| 2 | Historical Commerce Context | INCLUDE | Mode 3 required | Lightweight all-time context |
| 3 | Platform Status | INCLUDE | Always | Platform config, catalog health, data freshness — staleness emphasis |
| 4 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = True | Add caveat: peer benchmarks reflect current platform use, not lapsed period |
| 5 | Appendix | INCLUDE | Always | Data sources, staleness disclosures, last-active date |

## Excluded Sections (Mode 3 — no LTM commerce data)

| § | Section | Reason |
|---|---------|--------|
| 2 | Sales Team Performance | Mode 3 — no LTM orders; HAS_SALES_SECTION = false |
| 3 | Customer & Buyer Intelligence | Mode 3 — no LTM data |
| 4 | Product & Inventory Intelligence | Mode 3 — HAS_INVENTORY = false; inventory Stale >180 days |
| 5 | Commerce Analytics | Mode 3 — no LTM data |
| 6 | Portal Engagement | Mode 3 — HAS_CLICKY = false; also excluded per Mode 3 rules |

## Query-to-Section Mapping

### Section: Overview (§1 — Mode 3)
- Reads: gate_flags.md, historical_commerce_context.md, all other section drafts

### Section: Historical Commerce Context (§2 — Mode 3)
- Reads: historical_commerce_context.md

### Section: Platform Status (§3 — Mode 3)
- Reads: Q-07_results.md, Q-08_results.md, Q-09_results.md, Q-10_results.md, Q-11_results.md, Q-22_results.md, gate_flags.md

### Section: Peer Benchmarking (§4 — Mode 3)
- Reads: peer_benchmark_extract.md, Q-CI-03_results.md, Q-CI-05_results.md, gate_flags.md

### Section: Appendix (§5 — Mode 3)
- Reads: gate_flags.md, Q-08_results.md

## Skipped Queries (Mode 3 — not applicable)

| Query | Reason |
|-------|--------|
| Q-01 (Steps 1 & 2) | HAS_SALES_SECTION = false — no LTM iPad orders |
| Q-02 | Derived from Q-01 — Q-01 not run |
| Q-03 | Derived from Q-01 — Q-01 not run |
| Q-04 | HAS_SALES_SECTION = false |
| Q-05 | Mode 3 — excluded section |
| Q-06 | HAS_SALES_SECTION = false |
| Q-12 | Mode 3 — Customer section excluded |
| Q-13 | Mode 3 — Commerce section excluded |
| Q-14 | Mode 3 — Customer section excluded |
| Q-16 | HAS_PORTAL_ORDERS = false |
| Q-17 | Mode 3 — Customer section excluded |
| Q-18 | Mode 3 — Commerce section excluded |
| Q-19 | HAS_CART = false |
| Q-20 | Mode 3 — Commerce section excluded |
| Q-21 | Mode 3 — Commerce section excluded |
| Q-37 | HAS_INVENTORY = false |
| Q-38a | portal_order_items = 0 |
| Q-39 | Mode 3 — Product section excluded |
| Q-40 | Mode 3 — Customer section excluded |
| Q-41 | Mode 3 — Customer section excluded |
| Q-42 | Mode 3 — Product section excluded |
| Q-43 | HAS_SALES_SECTION = false |
| Q-45 | HAS_PORTAL_ORDERS = false |
| Q-46 | Mode 3 — excluded section |
| Q-47 | Mode 3 — excluded section |
| Q-49 | HAS_PORTAL_ORDERS = false |
| Q-50 | Mode 3 — excluded section |
| Q-CL-01 through Q-CL-05 | HAS_CLICKY = false |
| Q-CI-04 | Requires 2+ monthly snapshots (2 available but growth trajectory is Mode 1 only) |

## Cache File Inventory

| File | Status |
|------|--------|
| gate_flags.md | Written |
| section_manifest.md | Written |
| historical_commerce_context.md | Written |
| Q-07_results.md | Written |
| Q-08_results.md | Written |
| Q-09_results.md | Written |
| Q-10_results.md | Written |
| Q-11_results.md | Written |
| Q-22_results.md | Written |
| peer_benchmark_extract.md | Written |
| Q-CI-03_results.md | Written |
| Q-CI-05_results.md | Written |
| **Total cache files** | **12** |
