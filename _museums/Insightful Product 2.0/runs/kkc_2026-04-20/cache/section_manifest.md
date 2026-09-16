# Section Manifest — Kindel Furniture (kkc) — 2026-04-20
- **Report mode**: Mode 3: Platform Reactivation Report
- **Profile**: deep_intelligence (default)

## Section Inclusion Table

| § | Section | Status | Gate / Reason | Agent File |
|---|---------|--------|---------------|------------|
| 1 | Reactivation Summary | INCLUDE (STAGE 4) | Replaces Executive Summary in Mode 3 | stage4_assembly.md |
| 2 | Historical Commerce Context | INCLUDE | Mode 3 required — all-time eCat context | Mode 3 self-contained |
| 3 | Platform Status | INCLUDE | Mode 3 required — Q-07, Q-08, Q-09, Q-10, Q-11 | section_08_platform.md (adapted for Mode 3) |
| 4 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA = true; BENCHMARK_ELIGIBLE = true; peer_group_level = tier1 | section_07_peer.md |
| 5 | Appendix | INCLUDE (STAGE 4) | Always — attribution only in Mode 3 | stage4_assembly.md |
| — | §2 Sales Team Performance | SKIP | Mode 3 exclusion; also HAS_SALES_SECTION = false (LTM orders = 0) | — |
| — | §3 Customer & Buyer Intelligence | SKIP | Mode 3 exclusion — no LTM data | — |
| — | §4 Product & Inventory Intelligence | SKIP | Mode 3 exclusion; also inventory Stale at 255 days (>180 day threshold) | — |
| — | §5 Commerce Analytics | SKIP | Mode 3 exclusion — no LTM data | — |
| — | §6 Portal Engagement | SKIP | HAS_CLICKY = false | — |

## Query-to-Section Mapping

| Cache File | Used In | Notes |
|------------|---------|-------|
| historical_commerce_context.md | §2 Historical Commerce Context | All-time eCat orders, GMV, last active month, channel breakdown |
| Q-07_results.md | §3 Platform Status | Catalog completeness |
| Q-08_results.md | §3 Platform Status | Data freshness per entity |
| Q-09_results.md | §3 Platform Status | Import pipeline trend + recent errors |
| Q-10_results.md | §3 Platform Status | Feature enablement (partial — no mobile_sites record) |
| Q-11_results.md | §3 Platform Status | Configuration completeness (stale entities) |
| Q-22_results.md | §3 Platform Status | Feature usage depth (all-time Mixpanel) |
| Q-05_results.md | §3 Platform Status | Seat utilization context |
| peer_benchmark_extract.md | §4 Peer Benchmarking | Peer comparison data from 2026-04-14 benchmark run |
| showroom_scan_results.md | Internal only | No exclusions; validation log only |

## Mode 3 Required Disclosures

The following disclosure must appear as a callout inside the Reactivation Summary section (NOT in the Appendix):

> "This report reflects platform configuration and historical activity context. Commerce sections are not included as no eCat ordering activity has been recorded in the trailing 12 months. Last recorded eCat activity: July 2024."

The Appendix must contain only data source attribution rows. No mode explanation, omission rationale, or non-attribution content.
