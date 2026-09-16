# Validation Summary — Fine Art Handcrafted Lighting (fal)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report
- **Profile**: deep_intelligence

## Pre-Flight QC Results

### Presentation
- [x] Warm palette: `--accent: #C47A4A`, `--bg: #FAFAF8`, `--text: #2C2925`
- [x] Google Fonts loads both DM Sans and IBM Plex Mono
- [x] Header uses `.h-brand` + `.h-customer` + `.h-type` + `.h-meta` + `.h-accent`
- [x] Exec Summary opens with `<ul class="highlights"><li>` as FIRST content — no prose before it
- [x] Priority Actions use `.priorities` > `.priority` cards
- [x] §2–§8 use `<details class="section-collapse">`
- [x] Each `<summary>` has meaningful `section-sub` and `section-contents`
- [x] TOC is `<nav class="toc-strip" id="tocStrip">`

### Structure
- [x] Summary layer written last
- [x] TOC links only to sections actually rendered (7 links: Exec Summary, Sales, Customer, Commerce, Peer, Platform, Appendix)
- [x] Portal Engagement absent (HAS_CLICKY = false)
- [x] Peer Benchmarking included (peer data available, benchmark_eligible = true)
- [x] All INCLUDE sections from manifest present
- [x] No remaining `{{PARAM}}` placeholders — zero `{{` in output

### Forbidden Content
- [x] Zero `<!--` HTML comment nodes
- [x] "ERP" not in report body — 0 matches
- [x] "Mixpanel" not in delivered HTML — 0 matches
- [x] "Clicky" not in delivered HTML — 0 matches
- [x] "health score" / "health scores" not anywhere — 0 matches
- [x] `benchmark_confidence`, `peer_group_level`, `peer_group_n` not in HTML — 0 matches
- [x] `[HYPOTHETICAL]` / `[ESTIMATED]` not in HTML — 0 matches
- [x] Segment labels not in HTML — 0 matches
- [x] `operational_health_score` row uses title "Data & Operational Health"

### Appendix Contract
- [x] Attribution rows only — 5 data source rows
- [x] No report mode, run parameters, or bundle metadata
- [x] No gating explanations or methodology
- [x] Plain language only — no internal identifiers

## Section Build Status

| § | Section | Status | Subsections |
|---|---------|--------|-------------|
| 1 | Executive Summary | BUILT | 6 highlights, 4 priority actions (2 high, 2 medium collapsed) |
| 2 | Sales Team Performance | BUILT | 6/6 subsections: Rep Ladder, Behavioral Scorecard, Archetypes, Coaching (4 cards), Engagement Trajectory [COLLAPSE], Territory Coverage [COLLAPSE] |
| 3 | Customer & Buyer Intelligence | BUILT | 5/5 subsections: Activation, Dormant (25 accounts), Geographic [COLLAPSE], Reorder Velocity, New Buyers [COLLAPSE] |
| 4 | Product & Inventory | SKIP | HAS_INVENTORY = false AND HAS_SALES_DATA = false |
| 5 | Commerce Analytics | BUILT | 4/7 subsections: eCat Trend, AOV, Top Buyers, Order Type. 3 skipped (channel breakdown, ERP context, capture rate — all gated off) |
| 6 | Portal Engagement | SKIP | HAS_CLICKY = false |
| 7 | Peer Benchmarking | BUILT | 4/5 subsections: Peer Comparison (hero: Adoption 100), Benchmark Breakdown (4 metrics), Top Performers [COLLAPSE], Feature Adoption [COLLAPSE]. Growth Trajectory skipped (not available until May 2026) |
| 8 | Platform & Feature | BUILT | 6/6 subsections: Catalog Health, Feature Usage, Data Health, Pipeline Health [COLLAPSE], Config Alerts [COLLAPSE], Smart Stacks [COLLAPSE] |
| 9 | Appendix | BUILT | 5 attribution rows |

## Highlight Selection

6 highlights selected from 15 candidates across 5 sections:
1. GMV momentum up 42% [→ §commerce]
2. One rep drives 42% of iPad revenue [→ §sales]
3. $3.2M at risk from decelerating reorderers [→ §customers]
4. Perfect adoption score leads peer group [→ §peer]
5. 11 data entities stale since August 2025 [→ §platform]
6. 80.3% retention among activated accounts [→ §customers]

## Priority Actions

4 priority actions selected:
1. **HIGH**: Re-engage decelerating high-frequency accounts ($3.2M at risk) [→ §customers]
2. **HIGH**: Refresh stale data entities (matrix options, placement reports, favorites) [→ §platform]
3. **MEDIUM** [collapsed]: Investigate Jim Coyle's disengagement ($3.1M annual risk) [→ §sales]
4. **MEDIUM** [collapsed]: Coaching for mid-tier reps with funnel gaps [→ §sales]

## Output

- **File**: `output/fal_2026-04-20_intelligence_report.html`
- **Size**: 113 KB
- **Status**: Ready for browser review
