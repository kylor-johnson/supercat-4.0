# Validation Summary — Jamie Young Company (jyc)
- **Run date**: 2026-04-17
- **Report mode**: Mode 1: Standard Intelligence Report
- **Output file**: `jyc_2026-04-17_intelligence_report.html` (156K, 2,662 lines)

## Pre-Flight QC Results

### Presentation
- [x] Warm palette: `--accent: #C47A4A`, `--bg: #FAFAF8`, `--text: #2C2925`
- [x] Google Fonts: DM Sans + IBM Plex Mono
- [x] Header: `.h-brand` + `.h-customer` + `.h-type` + `.h-meta` + `.h-accent`
- [x] Exec Summary: `<ul class="highlights">` FIRST — no `<p class="prose">` before it
- [x] Priority Actions: `.priorities` > `.priority` cards (2 visible + 1 collapsed)
- [x] §2–§8: `<details class="section-collapse">` with correct IDs
- [x] TOC: `<nav class="toc-strip" id="tocStrip">`

### Structure
- [x] All 7 INCLUDE sections present (§2 sales, §3 customers, §4 product, §5 commerce, §6 portal, §7 peer, §8 platform)
- [x] TOC links match rendered sections (9 links: exec summary + 7 sections + appendix)
- [x] No remaining `{{PARAM}}` placeholders
- [x] `openAndScroll` function present in script
- [x] Executive Summary written last (from highlight candidates)

### Forbidden Content
- [x] Zero `<!--` HTML comments
- [x] No "ERP" in report body
- [x] No "Mixpanel" in delivered HTML
- [x] No "Clicky" in delivered HTML
- [x] No "health score" / "health scores"
- [x] No segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused)
- [x] No `[HYPOTHETICAL]` or `[ESTIMATED]` literal tags
- [x] No `benchmark_confidence`, `peer_group_level`, `peer_group_n`
- [x] No internal identifiers, VM codes, query IDs, table names, column names, org IDs
- [x] No "portal ordering" as buyer activity
- [x] No "net-new customers"
- [x] No "bounce_rate"

### Appendix Contract
- [x] Attribution rows only (9 data sources)
- [x] No report mode, report profile, run parameters
- [x] No gating explanations, methodology, or calculation docs
- [x] No internal table names, column names, VM codes, or org IDs
- [x] Plain language only

## Section Build Summary

| § | Section | Status | Fragment Size | Subsections |
|---|---------|--------|---------------|-------------|
| 1 | Executive Summary | BUILT (Stage 4) | inline | 6 highlights + 3 priority actions |
| 2 | Sales Team Performance | BUILT | 22K | Rep Leaderboard, Behavioral Scorecard, Selling Patterns, Coaching, Seat Utilization, Territory Coverage |
| 3 | Customer & Buyer Intelligence | BUILT | 27K | Activation, Concentration, Reorder, Dormant, Regional, First-Time |
| 4 | Product & Inventory Intelligence | BUILT | 20K | Catalog Completeness, OOS, Velocity, Line Analysis, New Items |
| 5 | Commerce Analytics | BUILT | 20K | Total Business, Velocity, AOV, Order Type |
| 6 | Portal Engagement | BUILT | 9.2K | Traffic Health, Geographic, Traffic Sources |
| 7 | Peer Benchmarking | BUILT | 7.6K | Hero Stat, Metric Comparison, Feature Adoption, Top Performer Patterns |
| 8 | Platform & Feature Utilization | BUILT | 18K | Data Freshness, Import Health, Feature Gap, Config, Usage Depth, Workflow, Smart Stacks, Library |
| 9 | Appendix | BUILT (Stage 4) | inline | 9 attribution rows |

## Highlight Selection

| # | Source | Headline |
|---|--------|----------|
| 1 | §5 Commerce | $8.0M platform GMV across 8,295 eCat orders LTM |
| 2 | §7 Peer | Top performer in order activity — 139% above peer median |
| 3 | §3 Customers | eCat Online drives 68% of new buyer acquisition |
| 4 | §4 Product | 20 top-selling items currently out of stock ($1.09M) |
| 5 | §2 Sales | Charlee Lowery's 88% order decline in trailing 90 days |
| 6 | §8 Platform | 12 of 22 data entities 240+ days stale |

## Priority Actions

| # | Urgency | Action | Impact |
|---|---------|--------|--------|
| 1 | HIGH | Check-in with Charlee Lowery | ~$100K+ quarterly run rate |
| 2 | HIGH | Prioritize OOS top seller allocation | $272K total business |
| 3 | MEDIUM | Re-engage 3,654 lapsed accounts | ~365 potential reactivations |
