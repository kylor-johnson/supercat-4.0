# Validation Summary — Linon/Powell Furniture (lpf)
**Run date:** 2026-04-20
**Report mode:** Mode 1: Standard Intelligence Report
**Profile:** deep_intelligence

## Pre-Flight QC

### Presentation
- [x] Warm palette: `--accent: #C47A4A`, `--bg: #FAFAF8`, `--text: #2C2925`
- [x] Google Fonts loads both DM Sans and IBM Plex Mono
- [x] Header uses `.h-brand` + `.h-customer` + `.h-type` + `.h-meta` + `.h-accent`
- [x] Exec Summary opens with `<ul class="highlights"><li>` as first content
- [x] Priority Actions use `.priorities` > `.priority` cards
- [x] §2–§8 use `<details class="section-collapse">`
- [x] TOC is `<nav class="toc-strip" id="tocStrip">`

### Structure
- [x] §6 and §8 rendered as separate sections
- [x] Summary layer written last
- [x] TOC links only to sections actually rendered (9 links)
- [x] Portal Engagement present (HAS_CLICKY = true)
- [x] Peer Benchmarking included (HAS_PEER_DATA = true, BENCHMARK_ELIGIBLE = true)
- [x] All INCLUDE sections from manifest present (§2–§8)
- [x] Zero remaining `{{PARAM}}` placeholders

### Forbidden Content
- [x] Zero HTML comment nodes (`<!--`)
- [x] "ERP" not in report body
- [x] "Mixpanel" not in delivered HTML
- [x] "Clicky" not in delivered HTML
- [x] No internal table/dataset names
- [x] No `order_source` code literals
- [x] No "health score" / "health scores"
- [x] No `benchmark_confidence`, `peer_group_level`, `peer_group_n` labels
- [x] `operational_health_score` row titled "Data & Operational Health"
- [x] No `[HYPOTHETICAL]` or `[ESTIMATED]` tags in HTML
- [x] No segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused)

### Appendix Contract
- [x] Attribution rows only — 9 data source rows
- [x] No omitted-sections table, methodology, or calculation docs
- [x] No report mode, run parameters, or platform bundle metadata
- [x] No gating explanations, partial-sync blocks, or standing caveats
- [x] Plain language only — no internal identifiers

## Output
- **HTML file:** `output/lpf_2026-04-20_intelligence_report.html`
- **File size:** 97 KB
- **Sections built:** §1 (Exec Summary), §2–§8, §9 (Appendix)
- **Sections skipped:** None (all INCLUDE)
- **Highlights selected:** 6 from §2, §3, §4, §5, §7, §8
- **Priority actions:** 4 (2 High visible, 1 High + 1 Medium collapsed)
