# Pre-Flight QC — RENWIL (rw) — 2026-04-17

## Presentation

- [x] Warm palette: `--accent: #C47A4A`, `--bg: #FAFAF8`, `--text: #2C2925` — confirmed (3 matches in CSS)
- [x] Google Fonts loads both `DM Sans` and `IBM Plex Mono` — confirmed (2 matches)
- [x] Header uses `.h-brand` + `.h-customer` + `.h-type` + `.h-meta` + `.h-accent` — confirmed (12 matches across CSS + markup)
- [x] No `<div class="h-title">` — confirmed (0 matches)
- [x] Exec Summary opens with `<ul class="highlights"><li>` as FIRST content — confirmed (1 instance)
- [x] Priority Actions use `.priorities` > `.priority` cards — confirmed (2 instances: visible + collapsed)
- [x] §2–§8 use `<details class="section-collapse">` — confirmed (7 instances)
- [x] TOC is `<nav class="toc-strip" id="tocStrip">` — confirmed (1 instance)

## Structure

- [x] All 7 INCLUDE sections present in output — confirmed (7 section IDs: sales, customers, product, commerce, portal, peer, platform)
- [x] §6 (Portal Engagement) and §8 (Platform & Feature Utilization) rendered as separate sections — confirmed
- [x] TOC links only to sections actually rendered — confirmed (9 links: exec summary, 7 content sections, appendix)
- [x] No remaining `{{PARAM}}` placeholders — confirmed (0 matches)
- [x] Summary layer (Executive Summary) written last — confirmed (assembled after all fragments)
- [x] `openAndScroll` function present in script block — confirmed (2 references)

## Forbidden Content

- [x] Zero `<!--` HTML comment nodes — confirmed (0 matches)
- [x] "ERP" not in report body — confirmed (0 matches)
- [x] "Mixpanel" not in delivered HTML — confirmed (0 matches)
- [x] "Clicky" not in delivered HTML — confirmed (0 matches)
- [x] "health score" / "health scores" not anywhere — confirmed (0 matches, case-insensitive)
- [x] `benchmark_confidence`, `peer_group_level`, `peer_group_n` not in client-facing HTML — confirmed (0 matches)
- [x] Literal `[HYPOTHETICAL]` not in delivered HTML — confirmed (0 matches)
- [x] Literal `[ESTIMATED]` not in delivered HTML — confirmed (0 matches)
- [x] No internal segment labels (`Platform-Embedded`, `Commerce-Active`, `Catalog-Focused`) — confirmed (0 matches)
- [x] No internal identifiers (VM codes, query IDs, table names, org IDs) — confirmed (0 matches)
- [x] No `order_source` code literals or `bounce_rate` — confirmed (0 matches)
- [x] `operational_health_score` row uses `peer-metric-title` = "Data & Operational Health" — confirmed in §7

## Appendix Contract

- [x] Attribution rows only — 7 rows (eCat Orders, Customer Data, Inventory Data, Rep Engagement Data, Portal Traffic Data, Peer Benchmark Data, Platform Configuration)
- [x] No omitted-sections table — confirmed
- [x] No methodology, calculation docs, gating explanations — confirmed
- [x] No report mode, report profile, run parameters — confirmed
- [x] No standing caveats, data-quality disclaimers — confirmed
- [x] Plain language only — no internal table names, column names, org IDs, VM codes, query IDs — confirmed
- [x] `sales_data` excluded (HAS_SALES_DATA=false) — confirmed
- [x] `portal_orders` excluded (HAS_PORTAL_ORDERS=false) — confirmed

## Executive Summary

- **Highlights selected**: 6 (from §5, §3, §7, §2, §3, §8)
- **Priority actions**: 4 (2 High, 2 Medium)
  - HIGH: Coach top 5 GMV reps on presentation tools → §sales
  - HIGH: Re-engage Ticking Stripe and top 5 dormant accounts → §customers
  - MEDIUM: Expand quote workflow adoption → §commerce (collapsed)
  - MEDIUM: Refresh option and category data imports → §platform (collapsed)

## Output

- **HTML report**: `rw_2026-04-17_intelligence_report.html` — 118,410 bytes
- **Validation summary**: `rw_2026-04-17_validation_summary.md` (this file)
- **Failures**: 0
- **Warnings**: 0
