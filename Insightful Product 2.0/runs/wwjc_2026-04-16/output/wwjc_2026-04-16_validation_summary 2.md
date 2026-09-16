# Validation Summary — Wildwood/Chelsea House (wwjc)
- **Run date**: 2026-04-16
- **Report mode**: Mode 1: Standard Intelligence Report
- **Report profile**: deep_intelligence
- **Stage**: 4 (Assembly)

## Executive Summary Selections

### Highlights (6 selected)
1. **eCat captures half of all-channel business** — 50.2% GMV capture, $9.0M of $17.8M trailing 12 months. Source: §5 Commerce Analytics.
2. **$695K in trailing-12-month GMV at risk from dormant accounts** — 20 accounts, 90+ days silent. Source: §3 Customer & Buyer Intelligence.
3. **One rep drives a third of all iPad orders** — Daniel Ratchford: 33% orders, 27% GMV ($836K). Source: §2 Sales Team Performance.
4. **20 top-selling products currently out of stock** — $1.0M+ combined all-time sales at zero availability. Source: §4 Product & Inventory Intelligence.
5. **12 supporting data entities stale since August 2025** — 239-day configuration drift. Source: §8 Platform & Feature Utilization.
6. **Five of seven peer benchmarks at or above median** — Value Delivery, Engagement, Catalog Completeness top-quartile. Source: §7 Peer Benchmarking.

### Priority Actions (4 selected: 3 HIGH + 1 MEDIUM)
1. **HIGH**: Reactivate 2,208 dormant house-account customers — +$226K est. annual GMV [HYPOTHETICAL]. Source: §2.
2. **HIGH**: Outreach to top 5 dormant high-value accounts — up to $435K recoverable [HYPOTHETICAL]. Source: §3.
3. **HIGH**: Re-import product options, categories, and groups — resolves 239-day drift [HYPOTHETICAL]. Source: §8.
4. **MEDIUM** (collapsed): Close feature depth gap from 5 to 8 — correlated with 8–40× throughput [HYPOTHETICAL]. Source: §7.

## Appendix Rows Written: 8

| # | Row Label | Source |
|---|-----------|--------|
| 1 | eCat Orders | orders |
| 2 | Total Business (All Channels) | portal_orders |
| 3 | Customer Data | customers |
| 4 | Inventory Data | inventories |
| 5 | Historical Sales Data | sales_data |
| 6 | Rep Engagement Data | Mixpanel (not named in output) |
| 7 | Peer Benchmark Data | peer_benchmark_2026-04-14.csv |
| 8 | Platform Configuration | org_summary |

## Pre-Flight QC Results

### Presentation
- [x] Warm palette: `--accent: #C47A4A`, `--bg: #FAFAF8`, `--text: #2C2925` — confirmed, not blue
- [x] Google Fonts loads both `DM Sans` and `IBM Plex Mono` — confirmed on line 9
- [x] Header uses `.h-brand` + `.h-customer` + `.h-type` + `.h-meta` + `.h-accent` — confirmed
- [x] Exec Summary opens with `<ul class="highlights"><li>` as FIRST content — confirmed (line 330, directly after `<h2>` on line 329), no `<p class="prose">` before it
- [x] Priority Actions use `.priorities` > `.priority` cards — confirmed, not `<div class="callout info"><ol>`
- [x] §2–§8 use `<details class="section-collapse">` — confirmed (6 instances for §2, §3, §4, §5, §7, §8)
- [x] Each `<summary>` has meaningful `section-sub` and `section-contents` — confirmed in all 6 fragments
- [x] TOC is `<nav class="toc-strip" id="tocStrip">` — confirmed on line 317

### Structure
- [x] §6 and §8 rendered as separate sections — §6 SKIP (HAS_CLICKY = false), §8 present as standalone section
- [x] Summary layer written last — Executive Summary composed after all fragments were read
- [x] TOC links only to sections actually rendered — 8 links: executive-summary, sales, customers, product, commerce, peer, platform, appendix
- [x] Portal Engagement absent (HAS_CLICKY = false) — no `#portal` link in TOC, no §6 fragment
- [x] Peer Benchmarking included (HAS_PEER_DATA = true) — §7 present
- [x] All INCLUDE sections from manifest present — §2, §3, §4, §5, §7, §8 all confirmed
- [x] No remaining `{{PARAM}}` placeholders — grep returned zero matches

### Forbidden Content
- [x] Zero `<!--` HTML comment nodes — grep returned zero matches
- [x] "ERP" not in report body — grep returned zero matches
- [x] "Mixpanel" not in delivered HTML — grep returned zero matches
- [x] "Clicky" not in delivered HTML — grep returned zero matches
- [x] Internal Clicky table names / dataset paths not in HTML — N/A (HAS_CLICKY = false)
- [x] `order_source = 'ipad'` code literals not in client-facing prose — grep returned zero matches
- [x] "health score" / "health scores" not anywhere — grep returned zero matches
- [x] `benchmark_confidence`, `peer_group_level`, `peer_group_n` not in client-facing HTML — grep returned zero matches
- [x] `operational_health_score` row uses `peer-metric-title` = "Data & Operational Health" — confirmed on line 2069
- [x] Segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) not in HTML — grep returned zero matches

### Appendix Contract
- [x] Attribution rows only — 8 data source rows, nothing else
- [x] No report mode, report profile, run parameters, or platform bundle metadata
- [x] No gating explanations, partial-sync blocks, standing caveats, [ESTIMATED] explanation rows
- [x] Plain language only — no internal table names, column names, org IDs, VM codes, query IDs, dataset paths
- [x] No operator/debug language

## Assembly Notes

- **CSS augmentation**: The §7 fragment uses `class="quartile-pill"` but the template CSS defines `.peer-quartile-pill`. Added `.quartile-pill` + `.q1`–`.q4` rules (identical styling) at the end of the `<style>` block to ensure peer benchmark pills render correctly. This is a known mismatch between the shared_rules quick reference (which lists `.quartile-pill`) and the template CSS (which prefixes with `peer-`).
- **Section 6 (Portal Engagement)**: Correctly omitted — HAS_CLICKY = false. No placeholder, no mention.
- **All fragments pasted verbatim**: No modifications to validated §2–§8 HTML content.
- **Peer cohort framing**: Uses "Lighting manufacturers on the same platform bundle" throughout (derived from PEER_GROUP_ID_EFFECTIVE = "Lighting / Full") — no raw segment labels or internal identifiers.
