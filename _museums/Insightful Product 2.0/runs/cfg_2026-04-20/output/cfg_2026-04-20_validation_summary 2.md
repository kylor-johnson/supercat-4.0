# Validation Summary — Charleston Forge (cfg)
- **Run date**: 2026-04-20
- **Report mode**: Mode 1: Standard Intelligence Report
- **Profile**: deep_intelligence

## Presentation Checks
- [x] Warm palette: --accent: #C47A4A, --bg: #FAFAF8, --text: #2C2925
- [x] Google Fonts loads both DM Sans and IBM Plex Mono
- [x] Header uses .h-brand + .h-customer + .h-type + .h-meta + .h-accent
- [x] Exec Summary opens with `<ul class="highlights"><li>` as FIRST content
- [x] Priority Actions use .priorities > .priority cards
- [x] §2–§8 use `<details class="section-collapse">`
- [x] Each summary has meaningful section-sub and section-contents
- [x] TOC is `<nav class="toc-strip" id="tocStrip">`

## Structure Checks
- [x] §6 and §8 rendered as separate sections
- [x] Summary layer written last
- [x] TOC links only to sections actually rendered (8 links)
- [x] Portal Engagement present (HAS_CLICKY = true)
- [x] Peer Benchmarking included (HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true)
- [x] All INCLUDE sections from manifest present: §2, §3, §5, §6, §7, §8
- [x] §4 correctly omitted (HAS_INVENTORY = false AND HAS_SALES_DATA = false)
- [x] No remaining {{PARAM}} placeholders

## Forbidden Content Checks
- [x] Zero `<!--` HTML comment nodes
- [x] "ERP" not in report body
- [x] "Mixpanel" not in delivered HTML
- [x] "Clicky" not in delivered HTML
- [x] Internal table names / dataset paths / prefix values not in HTML
- [x] `order_source = 'ipad'` code literals not in client-facing prose
- [x] "health score" / "health scores" not anywhere
- [x] `benchmark_confidence`, `peer_group_level`, `peer_group_n` not in client-facing HTML
- [x] `operational_health_score` row uses peer-metric-title = "Data & Operational Health"
- [x] No [HYPOTHETICAL] or [ESTIMATED] tags in HTML
- [x] No Platform-Embedded / Commerce-Active / Catalog-Focused segment labels

## Appendix Contract
- [x] Attribution rows only
- [x] No omitted-sections table, methodology, calculation docs
- [x] No report mode, report profile, run parameters, or platform bundle metadata
- [x] No gating explanations, partial-sync blocks, standing caveats
- [x] Plain language only — no internal identifiers

## Output
- **File**: cfg_2026-04-20_intelligence_report.html
- **Size**: ~89 KB
- **Sections built**: 6 (§2, §3, §5, §6, §7, §8)
- **Sections skipped**: 1 (§4 — Product & Inventory)
- **Highlights selected**: 6
- **Priority actions**: 4 (2 High, 2 Medium)
- **Appendix rows**: 6
