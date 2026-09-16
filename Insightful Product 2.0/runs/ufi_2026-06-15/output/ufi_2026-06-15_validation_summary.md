# Validation Summary — Universal Furniture (ufi)
**Report Date**: June 15, 2026
**Run**: ufi_2026-06-15

## Presentation Checks

| Check | Result |
|---|---|
| Warm palette (`--accent: #C47A4A`, `--bg: #FAFAF8`, `--text: #2C2925`) | PASS |
| Google Fonts loads DM Sans + IBM Plex Mono | PASS |
| Header uses `.h-brand` + `.h-customer` + `.h-type` + `.h-meta` + `.h-accent` | PASS |
| Exec Summary opens with `<ul class="highlights"><li>` — no `<p>` before it | PASS |
| Priority Actions use `.priorities` > `.priority` cards | PASS |
| §2–§8 use `<details class="section-collapse">` | PASS (23 occurrences across CSS + 7 sections) |
| Each `<summary>` has `section-sub` and `section-contents` | PASS |
| TOC is `<nav class="toc-strip" id="tocStrip">` | PASS |

## Structure Checks

| Check | Result |
|---|---|
| §6 and §8 rendered as separate sections | PASS |
| Summary layer written last | PASS |
| TOC links match rendered sections | PASS (exec-summary, sales, customers, product, commerce, portal, peer, platform, appendix) |
| Portal Engagement present (HAS_CLICKY = true) | PASS |
| Peer Benchmarking included | PASS |
| All INCLUDE sections present (§2–§8) | PASS |
| No remaining `{{PARAM}}` placeholders | PASS |

## Forbidden Content Checks

| Check | Result |
|---|---|
| Zero `<!--` HTML comment nodes | PASS |
| "ERP" not in body | PASS |
| "Mixpanel" not in HTML | PASS |
| "Clicky" not in HTML | PASS |
| Internal dataset paths not in HTML | PASS |
| `order_source` code literals not in prose | PASS |
| "health score" not in HTML | PASS |
| `benchmark_confidence` / `peer_group_level` / `peer_group_n` not in HTML | PASS |
| `[HYPOTHETICAL]` / `[ESTIMATED]` tags not in HTML | PASS |

## Appendix Contract Checks

| Check | Result |
|---|---|
| Attribution rows only | PASS |
| No report mode / run parameters / bundle metadata | PASS |
| No gating explanations / partial-sync blocks / standing caveats | PASS |
| Plain language only — no internal identifiers | PASS |
| No operator/debug language | PASS |
| Data Completeness row present (sections below FULL exist) | PASS |

## Section Build Summary

| Section | Status | Subsections | Notes |
|---|---|---|---|
| §1 Executive Summary | BUILT | 6 highlights, 4 priority actions (2 collapsed) | — |
| §2 Sales Team | BUILT | Rep Activity Ladder, Rep Engagement Trajectory | Data confidence: PARTIAL |
| §3 Customer & Buyer Intelligence | BUILT | Activation, Dormant, Geographic, Reorder, New Buyers | — |
| §4 Product & Inventory | BUILT | Catalog Completeness | Data confidence: STRONG |
| §5 Commerce Analytics | BUILT | Order Trend, AOV, Top Buyers, Order Type, Capture Rate | — |
| §6 Portal Engagement | BUILT | Traffic Health, Monthly Trend | Skipped: Geographic Demand, Top Pages, Traffic Source (missing Clicky data) |
| §7 Peer Benchmarking | BUILT | Peer Group, Standout, Breakdown, Feature Adoption | Skipped: What Top Performers Do, Growth Trajectory |
| §8 Platform & Feature | BUILT | Catalog Health, Feature Usage, Data Health, Pipeline, Config Alerts, Smart Stacks | — |
| §9 Appendix | BUILT | 9 attribution rows | — |

## Known Data Gaps

1. **BigQuery Q-CL-03** (Geographic Demand Map) — 404 Dataset not found. §6 Geographic subsection skipped.
2. **BigQuery Q-CL-05** (Traffic Source Intelligence) — Column `source` not recognized. §6 Traffic Source subsection skipped.
3. **MIXPANEL_USER_DATA_PRESENT gate flag** — Set to `False` but Q-01_step1 cache contains 103 rows. Bug in `data_gather.py` gate computation; §2 built conservatively based on the `False` flag.
4. **Peer benchmark CSV** (`peer_benchmark_extract.md`) — Not generated. §7 used raw Q-CI-02/Q-CI-03-bench data; composite score metrics unavailable.

## Verdict

**PASS** — All QC checks passed. Report delivered with known data gaps documented above.
