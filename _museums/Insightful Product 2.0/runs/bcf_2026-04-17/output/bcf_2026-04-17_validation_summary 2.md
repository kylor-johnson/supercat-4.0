# Validation Summary — Braxton Culler (bcf_2026-04-17)
- **Generated**: April 17, 2026
- **Report file**: `bcf_2026-04-17_intelligence_report.html`
- **File size**: 147,229 bytes (2,394 lines)

## Presentation ✅

| Check | Result |
|-------|--------|
| Warm palette: `--accent: #C47A4A`, `--bg: #FAFAF8`, `--text: #2C2925` | ✅ Pass |
| Google Fonts: DM Sans + IBM Plex Mono | ✅ Pass |
| Header: `.h-brand` + `.h-customer` + `.h-type` + `.h-meta` + `.h-accent` | ✅ Pass |
| Exec Summary: `<ul class="highlights">` FIRST — no `<p class="prose">` before it | ✅ Pass |
| Priority Actions: `.priorities` > `.priority` cards | ✅ Pass (2 containers) |
| §2–§8 use `<details class="section-collapse">` | ✅ Pass (6 instances) |
| TOC: `<nav class="toc-strip" id="tocStrip">` | ✅ Pass |

## Structure ✅

| Check | Result |
|-------|--------|
| All 6 INCLUDE sections present (§2, §3, §4, §5, §7, §8) | ✅ Pass — all section IDs confirmed |
| §6 Portal Engagement absent (HAS_CLICKY = false) | ✅ Pass — no `id="portal"` found |
| TOC links match rendered sections | ✅ Pass — 8 links (exec summary, sales, customers, product, commerce, peer, platform, appendix) |
| No remaining `{{PARAM}}` placeholders | ✅ Pass — 0 matches |
| `openAndScroll` function present | ✅ Pass — 2 occurrences (definition + usage) |

## Forbidden Content ✅

| Check | Result |
|-------|--------|
| Zero `<!--` HTML comment nodes | ✅ Pass — 0 matches |
| No "ERP" in body prose | ✅ Pass — 0 matches |
| No "Mixpanel" in HTML | ✅ Pass — 0 matches |
| No "Clicky" in HTML | ✅ Pass — 0 matches |
| No "health score" in HTML | ✅ Pass — 0 matches |
| No `[HYPOTHETICAL]` or `[ESTIMATED]` literal tags | ✅ Pass — 0 matches |
| No internal identifiers or segment labels | ✅ Pass — 0 matches for `benchmark_confidence`, `peer_group_level`, `peer_group_n`, `Platform-Embedded`, `Commerce-Active`, `Catalog-Focused` |
| No `order_source` code literals | ✅ Pass — 0 matches |

## Appendix ✅

| Check | Result |
|-------|--------|
| Attribution rows only — no methodology, gating, or internal identifiers | ✅ Pass |
| No report mode, run parameters, or platform bundle metadata | ✅ Pass |
| No gating explanations, partial-sync blocks, standing caveats | ✅ Pass |
| Plain language only | ✅ Pass |

## Appendix Rows Included (8)

1. **eCat Orders** — always included
2. **Total Business (All Channels)** — HAS_PORTAL_ORDERS = true
3. **Customer Data** — always included
4. **Inventory Data** — HAS_INVENTORY = true
5. **Historical Sales Data** — HAS_SALES_DATA = true
6. **Rep Engagement Data** — MIXPANEL_USER_DATA_PRESENT = true
7. **Peer Benchmark Data** — HAS_PEER_DATA = true (with medium-confidence directional framing)
8. **Platform Configuration** — always included

## Highlight Selection (§1 Executive Summary)

| # | Headline | Source Section |
|---|----------|---------------|
| 1 | $6.6M eCat GMV across 2,608 orders | §5 Commerce |
| 2 | Presentation tool adoption is the team's biggest coaching lever | §2 Sales |
| 3 | 20 top-selling products are currently out of stock | §4 Product |
| 4 | $185K in dormant account value ready for re-engagement | §3 Customers |
| 5 | Top quartile in value delivery among Furniture peers | §7 Peer |
| 6 | 6 data entities stale since August 2025 | §8 Platform |

Coverage: All 6 rendered sections represented. Mix: 2 positive findings, 4 action-oriented.

## Priority Actions (4)

| # | Urgency | Action | Source |
|---|---------|--------|--------|
| 1 | **High** | Coach high-volume reps on presentation and discovery tools | §2 Sales |
| 2 | **High** | Re-engage top 5 dormant accounts ($185K historical value) | §3 Customers |
| 3 | **Medium** | Prioritize restocking out-of-stock top sellers ($4.8M demand) | §4 Product |
| 4 | **Medium** | Re-import kit items and matrix options (configuration alignment) | §8 Platform |

Layout: 2 High-urgency visible, 2 Medium-urgency in collapsed `<details>`.

## QC Result

**All checks passed. Zero failures. Report is ready for delivery.**
