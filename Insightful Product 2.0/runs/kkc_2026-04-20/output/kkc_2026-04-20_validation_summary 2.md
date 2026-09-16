# Validation Summary — Kindel Furniture (kkc) — 2026-04-20

## Report Mode
Mode 3: Platform Reactivation Report

## Pre-Flight QC Results

### Presentation Checks
- [x] Warm palette: `--accent: #C47A4A` ✓
- [x] Google Fonts loads both DM Sans and IBM Plex Mono ✓
- [x] Header uses `.h-brand` + `.h-customer` + `.h-type` + `.h-meta` + `.h-accent` ✓
- [x] Reactivation Summary opens with `<ul class="highlights">` as FIRST content — no prose before it ✓
- [x] Priority Actions use `.priorities` > `.priority` cards ✓
- [x] §2–§4 use `<details class="section-collapse">` ✓
- [x] Each `<summary>` has meaningful `section-sub` and `section-contents` ✓
- [x] TOC is `<nav class="toc-strip" id="tocStrip">` ✓

### Structure Checks
- [x] Reactivation Summary written last from highlight candidates ✓
- [x] TOC links only to sections actually rendered ✓
- [x] Portal Engagement absent (HAS_CLICKY = false) ✓
- [x] Peer Benchmarking included (HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true) ✓
- [x] All INCLUDE sections from manifest present ✓
- [x] No remaining `{{PARAM}}` placeholders ✓

### Forbidden Content Checks
- [x] Zero HTML comment nodes ✓
- [x] "ERP" not in report body ✓
- [x] "Mixpanel" not in delivered HTML ✓
- [x] "Clicky" not in delivered HTML ✓
- [x] "health score" / "health scores" not in delivered HTML ✓
- [x] `benchmark_confidence`, `peer_group_level`, `peer_group_n` not in client-facing HTML ✓
- [x] `[HYPOTHETICAL]` and `[ESTIMATED]` tags not in HTML (cache only) ✓
- [x] Segment labels (Catalog-Focused, Platform-Embedded, Commerce-Active) not in HTML ✓
- [x] `operational_health_score` peer-metric-title = "Data & Operational Health" ✓
- [x] "portal ordering" not in delivered HTML ✓

### Appendix Contract
- [x] Attribution rows only ✓
- [x] No omitted-sections table or methodology ✓
- [x] No report mode, run parameters, or bundle metadata in Appendix ✓
- [x] No gating explanations ✓
- [x] Plain language only ✓

## Section Build Summary
| Section | Status |
|---------|--------|
| §1 Reactivation Summary | BUILT |
| §2 Historical Commerce Context | BUILT |
| §3 Platform Status | BUILT |
| §4 Peer Benchmarking | BUILT |
| Appendix | BUILT |
| §2 Sales Team Performance | SKIPPED (Mode 3 exclusion) |
| §3 Customer & Buyer Intelligence | SKIPPED (Mode 3 exclusion) |
| §4 Product & Inventory Intelligence | SKIPPED (Mode 3 exclusion + inventory Stale >180 days) |
| §5 Commerce Analytics | SKIPPED (Mode 3 exclusion) |
| §6 Portal Engagement | SKIPPED (HAS_CLICKY = false) |

## Output File
- `output/kkc_2026-04-20_intelligence_report.html` — 69,490 bytes
