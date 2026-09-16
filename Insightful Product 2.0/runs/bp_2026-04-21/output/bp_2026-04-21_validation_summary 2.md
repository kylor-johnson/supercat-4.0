# Validation Summary — Buster & Punch (bp) Intelligence Report
- **Run date**: 2026-04-21
- **Output file**: `output/bp_2026-04-21_intelligence_report.html`
- **File size**: 95 KB (1,449 lines)

## Presentation Checks
- [x] Warm palette: `--accent: #C47A4A`, `--bg: #FAFAF8`, `--text: #2C2925`
- [x] Google Fonts loads both DM Sans and IBM Plex Mono
- [x] Header uses `.h-brand` + `.h-customer` + `.h-type` + `.h-meta` + `.h-accent`
- [x] Exec Summary opens with `<ul class="highlights"><li>` as FIRST content — no `<p class="prose">` before it
- [x] Priority Actions use `.priorities` > `.priority` cards
- [x] §3–§8 use `<details class="section-collapse">`
- [x] Each `<summary>` has meaningful `section-sub` and `section-contents`
- [x] TOC is `<nav class="toc-strip" id="tocStrip">`

## Structure Checks
- [x] §2 (Sales Team) correctly SKIPPED — HAS_SALES_SECTION = false
- [x] §6 (Portal Engagement) correctly SKIPPED — HAS_CLICKY = false
- [x] Summary layer written last
- [x] TOC links only to sections actually rendered (7 links)
- [x] Peer Benchmarking included — HAS_PEER_DATA = true
- [x] All INCLUDE sections present: §3, §4, §5, §7, §8
- [x] No remaining `{{PARAM}}` placeholders

## Forbidden Content Checks
- [x] Zero `<!--` HTML comment nodes
- [x] "ERP" not in report body
- [x] "Mixpanel" not in delivered HTML
- [x] "Clicky" not in delivered HTML
- [x] "health score" / "health scores" not anywhere
- [x] No segment labels (Commerce-Active, Platform-Embedded, Catalog-Focused)
- [x] No `[HYPOTHETICAL]` or `[ESTIMATED]` tags
- [x] No `benchmark_confidence`, `peer_group_level`, `peer_group_n` exposed
- [x] `peer_group_n` (52) not exposed as literal count

## Appendix Contract
- [x] Attribution rows only — 6 data source rows
- [x] No omitted-sections table, methodology, or calculation docs
- [x] No report mode, report profile, run parameters, or platform bundle metadata
- [x] Plain language only — no internal identifiers

## Section Build Summary
| Section | Status | Subsections |
|---------|--------|-------------|
| §1 Executive Summary | Built (Stage 4) | 6 highlights, 4 priority actions (2 High, 2 Medium) |
| §2 Sales Team Performance | SKIPPED | HAS_SALES_SECTION = false (0 qualifying reps) |
| §3 Customer & Buyer Intelligence | Built | 5 subsections (2 collapsed) |
| §4 Product & Inventory Intelligence | Built | 1 subsection (Catalog Completeness only) |
| §5 Commerce Analytics | Built | 4 subsections |
| §6 Portal Engagement | SKIPPED | HAS_CLICKY = false |
| §7 Peer Benchmarking | Built | 5 subsections (2 collapsed) |
| §8 Platform & Feature Utilization | Built | 6 subsections (3 collapsed) |
| §9 Appendix | Built | 6 attribution rows |

## Highlight Selection
6 highlights selected from candidate pool:
1. §3: 0.2% eCat activation rate (16 of 7,084 accounts)
2. §4: 45.2% catalog completeness — 1,226 missing pricing
3. §5: 51.5% buyer concentration on single account
4. §7: Order volume in bottom quartile vs. peers
5. §5: Q1 2026 positive momentum ($24,304)
6. §8: 11 data entities frozen since Aug 2025

## Priority Actions
| # | Urgency | Action | Section |
|---|---------|--------|---------|
| 1 | High | Re-engage 5 lapsed one-order buyers (~$12K recovery) | §3 |
| 2 | High | Address 1,226 products missing price data (→ 90%+ completeness) | §4 |
| 3 | Medium | Expand active buyer base to reduce concentration | §5 |
| 4 | Medium | Restore secondary data import pipeline (11 entities) | §8 |
