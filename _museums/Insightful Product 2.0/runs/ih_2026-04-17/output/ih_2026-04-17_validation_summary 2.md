# Validation Summary — Interlude Home (ih_2026-04-17)

## Build Status

| Section | Status | Source |
|---------|--------|--------|
| §1 Executive Summary | Built | Assembled from highlight candidates (§2–§8) |
| §2 Sales Team Performance | INCLUDE | `fragments/section_02.html` — verbatim |
| §3 Customer & Buyer Intelligence | INCLUDE | `fragments/section_03.html` — verbatim |
| §4 Product & Inventory Intelligence | INCLUDE | `fragments/section_04.html` — verbatim |
| §5 Commerce Analytics | INCLUDE | `fragments/section_05.html` — verbatim |
| §6 Portal Engagement | INCLUDE | `fragments/section_06.html` — verbatim |
| §7 Peer Benchmarking | INCLUDE | `fragments/section_07.html` — verbatim |
| §8 Platform & Feature Utilization | INCLUDE | `fragments/section_08.html` — verbatim |
| §9 Appendix | Built | 9 attribution rows |

## Highlight Selection

6 highlights selected from candidates across all 7 sections:

1. **eCat captures 67.7% of all-channel GMV** — from §5 Commerce Analytics
2. **Top 5% peer engagement among Furniture manufacturers** — from §7 Peer Benchmarking
3. **$1.1M+ in trailing 12-month GMV at risk** — from §2 Sales Team Performance
4. **87% of your account base has never placed an eCat order** — from §3 Customer Intelligence
5. **20 top-selling products currently out of stock** — from §4 Product Intelligence
6. **10 data entities stale since August 2025** — from §8 Platform

Selection rationale: Ranked by signal strength. Includes 1 positive finding (highlight #1 platform dominance, #2 peer leadership), 3 risk/action signals (#3 rep decline, #4 activation gap, #5 stock-outs), and 1 operational alert (#6 data drift). Covers 6 of 7 content sections; §6 Portal omitted from highlights due to lower signal strength relative to other candidates.

## Priority Actions

3 priority actions selected:

| # | Urgency | Action | Section |
|---|---------|--------|---------|
| 1 | HIGH | Re-engage declining reps (Athre, Mirwaldt) | §2 Sales Team |
| 2 | HIGH | Address out-of-stock top sellers (19 items, no receipt date) | §4 Product |
| 3 | HIGH | Re-import stale configuration data (240-day drift) | §8 Platform |

Priority #3 wrapped in `<details>` for progressive disclosure per assembly rules.

## Appendix Rows

9 attribution rows:

1. eCat Orders
2. Total Business (All Channels)
3. Customer Data
4. Inventory Data
5. Historical Sales Data
6. Rep Engagement Data
7. Portal Traffic Data
8. Peer Benchmark Data
9. Platform Configuration

## Pre-Flight QC

| # | Check | Result |
|---|-------|--------|
| 1 | Warm palette: `--accent: #C47A4A`, `--bg: #FAFAF8`, `--text: #2C2925` | PASS |
| 2 | Google Fonts: DM Sans + IBM Plex Mono | PASS |
| 3 | Header: `.h-brand` + `.h-customer` + `.h-type` + `.h-meta` + `.h-accent` | PASS |
| 4 | Exec Summary: `<ul class="highlights">` as FIRST content — no `<p class="prose">` before it | PASS |
| 5 | Priority Actions: `.priorities` > `.priority` cards | PASS |
| 6 | §2–§8: `<details class="section-collapse">` (7 instances) | PASS |
| 7 | TOC: `<nav class="toc-strip" id="tocStrip">` | PASS |
| 8 | All INCLUDE sections present (§2, §3, §4, §5, §6, §7, §8) | PASS |
| 9 | No remaining `{{PARAM}}` placeholders | PASS |
| 10 | `openAndScroll` function present | PASS |
| 11 | ZERO `<!--` HTML comments | PASS |
| 12 | No "ERP" in body text | PASS |
| 13 | No "Mixpanel" in HTML | PASS |
| 14 | No "Clicky" in HTML | PASS |
| 15 | No "health score" in HTML | PASS |
| 16 | No `[HYPOTHETICAL]` or `[ESTIMATED]` literal tags | PASS |
| 17 | No segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) | PASS |
| 18 | Appendix: attribution rows only — no methodology, gating, or metadata | PASS |

**All 18 checks: PASS**

## File Details

| File | Size | Lines |
|------|------|-------|
| `ih_2026-04-17_intelligence_report.html` | 137,164 bytes (134 KB) | 2,459 |
| `ih_2026-04-17_validation_summary.md` | (this file) | — |
