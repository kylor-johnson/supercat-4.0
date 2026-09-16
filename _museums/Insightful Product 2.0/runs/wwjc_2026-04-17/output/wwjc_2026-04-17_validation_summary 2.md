# Validation Summary — Wildwood/Chelsea House (wwjc) — 2026-04-17

## Presentation Checks

| Check | Result |
|-------|--------|
| Warm palette: `--accent: #C47A4A`, `--bg: #FAFAF8`, `--text: #2C2925` | PASS |
| Google Fonts loads both DM Sans and IBM Plex Mono | PASS |
| Header uses `.h-brand` + `.h-customer` + `.h-type` + `.h-meta` + `.h-accent` | PASS |
| Exec Summary opens with `<ul class="highlights"><li>` as FIRST content | PASS |
| Priority Actions use `.priorities` > `.priority` cards | PASS |
| §2–§8 use `<details class="section-collapse">` | PASS (22 occurrences in CSS + 6 section instances) |
| Each `<summary>` has meaningful `section-sub` and `section-contents` | PASS |
| TOC is `<nav class="toc-strip" id="tocStrip">` | PASS |

## Structure Checks

| Check | Result |
|-------|--------|
| §6 and §8 rendered as separate sections | PASS (§6 SKIP, §8 rendered) |
| Summary layer (§1) written last | PASS |
| TOC links only to sections actually rendered | PASS (8 links: exec-summary, sales, customers, product, commerce, peer, platform, appendix) |
| Portal Engagement absent (HAS_CLICKY = false) | PASS — no `id="portal"` in output |
| Peer Benchmarking included (HAS_PEER_DATA = true) | PASS — `id="peer"` present |
| All INCLUDE sections from manifest present | PASS — §2 (sales), §3 (customers), §4 (product), §5 (commerce), §7 (peer), §8 (platform) all present |
| No remaining `{{PARAM}}` placeholders | PASS |

## Forbidden Content Checks

| Check | Result |
|-------|--------|
| Zero `<!--` HTML comment nodes | PASS |
| "ERP" not in report body | PASS |
| "Mixpanel" not in delivered HTML | PASS |
| "Clicky" not in delivered HTML | PASS |
| Internal Clicky table names / dataset paths not in HTML | PASS |
| `order_source = 'ipad'` code literals not in prose | PASS |
| "health score" / "health scores" not anywhere | PASS |
| `benchmark_confidence`, `peer_group_level`, `peer_group_n` not in client-facing HTML | PASS |
| `operational_health_score` row uses `peer-metric-title` = "Data & Operational Health" | PASS |
| No `[HYPOTHETICAL]` or `[ESTIMATED]` literal tags | PASS |
| No segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) | PASS |
| No `bounce_rate` | PASS |
| No `<div class="callout info"><ol>` pattern | PASS |
| No blue accent (`--accent: #2563EB`) | PASS |

## Appendix Contract Checks

| Check | Result |
|-------|--------|
| Attribution rows only | PASS (8 rows: eCat Orders, Total Business, Customer Data, Inventory Data, Historical Sales Data, Rep Engagement Data, Peer Benchmark Data, Platform Configuration) |
| No omitted-sections table, methodology, calculation docs | PASS |
| No report mode, report profile, run parameters, or platform bundle metadata | PASS |
| No gating explanations, partial-sync blocks, standing caveats, [ESTIMATED] explanation rows | PASS |
| Plain language only — no internal identifiers | PASS |
| No operator/debug language | PASS |

## Section Build Status

| § | Section | Status |
|---|---------|--------|
| 1 | Executive Summary | BUILT (Stage 4) |
| 2 | Sales Team Performance | INCLUDED (fragment verbatim) |
| 3 | Customer & Buyer Intelligence | INCLUDED (fragment verbatim) |
| 4 | Product & Inventory Intelligence | INCLUDED (fragment verbatim) |
| 5 | Commerce Analytics | INCLUDED (fragment verbatim) |
| 6 | Portal Engagement | SKIPPED (HAS_CLICKY = false) |
| 7 | Peer Benchmarking | INCLUDED (fragment verbatim) |
| 8 | Platform & Feature Utilization | INCLUDED (fragment verbatim) |
| 9 | Appendix | BUILT (Stage 4) |

## Executive Summary Content

- **Highlights**: 6 items (from §5 Commerce, §3 Customers, §7 Peer, §2 Sales, §4 Product, §5 Commerce)
- **Priority Actions**: 4 total
  - 2 visible (both HIGH: lapsed account re-engagement, OOS restock)
  - 2 collapsed in `<details>` (1 HIGH: presentation coaching; 1 MEDIUM: stale data re-import)
- Sources: §2 Sales, §3 Customers, §4 Product, §5 Commerce, §7 Peer, §8 Platform

## Output File

- **Path**: `runs/wwjc_2026-04-17/output/wwjc_2026-04-17_intelligence_report.html`
- **File size**: 143,669 bytes (~140 KB)
- **All QC checks**: PASS (0 failures)
