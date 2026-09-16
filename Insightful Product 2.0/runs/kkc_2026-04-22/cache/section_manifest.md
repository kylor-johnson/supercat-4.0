# Section Manifest — Kindel Karges Furniture (kkc, org_id=99)
- **Run date**: 2026-04-22
- **Report mode**: Mode 3: Platform Reactivation Report

## Section Inclusion

| § | Section | Status | Gate | Notes |
|---|---------|--------|------|-------|
| 1 | Reactivation Summary | STAGE 2/3 | Always (written last) | Replaces Executive Summary in Mode 3 |
| 2 | Historical Commerce Context | INCLUDE | Mode 3 always | All-time eCat context (41 orders, $1.08M GMV, last active July 2024) |
| 3 | Platform Status | INCLUDE | Always | Catalog health, data freshness, feature enablement — with staleness emphasis |
| 4 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true, tier1 | Caveat: "Peer benchmarks reflect current platform use, not the lapsed period." |
| 5 | Appendix | STAGE 2/3 | Always | Data sources, staleness disclosures, last-active date |

## Sections Excluded (Mode 3)

| § | Section | Reason |
|---|---------|--------|
| 2 | Sales Team Performance | No LTM order data; HAS_SALES_SECTION = false |
| 3 | Customer & Buyer Intelligence | No LTM data |
| 4 | Product & Inventory Intelligence | HAS_INVENTORY = false; no LTM data |
| 5 | Commerce Analytics | No LTM data |
| 6 | Portal Engagement | HAS_CLICKY = false |

## Query-to-Section Mapping

| Cache File | Section Consumer | Status |
|------------|-----------------|--------|
| gate_flags.md | All sections | Written |
| historical_commerce_context.md | §2 Historical Commerce Context | Written |
| Q-05_results.md | §3 Platform Status | Written |
| Q-07_results.md | §3 Platform Status | Written |
| Q-08_results.md | §3 Platform Status | Written |
| Q-09_results.md | §3 Platform Status | Written |
| Q-10_results.md | §3 Platform Status | Written |
| Q-11_results.md | §3 Platform Status | Written |
| Q-22_results.md | §3 Platform Status | Written |
| peer_benchmark_extract.md | §4 Peer Benchmarking | Written |
| Q-CI-03_results.md | §4 Peer Benchmarking | Written |
| Q-CI-05_results.md | §4 Peer Benchmarking | Written |
| showroom_scan_results.md | Validation reference | Written |
| section_manifest.md | All stages | This file |

## Queries Skipped (Mode 3 / Gate = false)

| Query ID | Reason |
|----------|--------|
| Q-01 | HAS_SALES_SECTION = false (no LTM orders) |
| Q-02 | Derived from Q-01 (not run) |
| Q-03 | Derived from Q-01 (not run) |
| Q-04 | HAS_SALES_SECTION = false |
| Q-06 | HAS_SALES_SECTION = false |
| Q-12 | Mode 3 — no LTM customer intelligence |
| Q-13 | Mode 3 — no LTM commerce |
| Q-14 | Mode 3 — no LTM commerce |
| Q-16 | HAS_PORTAL_ORDERS = false |
| Q-17 | Mode 3 — no LTM commerce |
| Q-18 | Mode 3 — no LTM commerce |
| Q-19 | HAS_CART = false |
| Q-20 | Mode 3 — no LTM commerce |
| Q-21 | Mode 3 — no LTM commerce |
| Q-37 | HAS_INVENTORY = false |
| Q-38a | Mode 3 — no LTM commerce |
| Q-39 | Mode 3 — no LTM commerce |
| Q-40 | Mode 3 — no LTM commerce |
| Q-41 | Mode 3 — no LTM commerce |
| Q-42 | Mode 3 — no LTM commerce |
| Q-43 | HAS_SALES_SECTION = false |
| Q-45 | HAS_PORTAL_ORDERS = false |
| Q-46 | Mode 3 — no LTM commerce |
| Q-47 | Mode 3 — not applicable |
| Q-49 | HAS_PORTAL_ORDERS = false |
| Q-50 | Mode 3 — not applicable |
| Q-CL-01–05 | HAS_CLICKY = false |
| Q-CI-04 | Requires 2+ monthly snapshots for trending |
