# Validation Summary — Kindel Karges Furniture (kkc, org_id=99)
- **Run date**: 2026-04-22
- **Report mode**: Mode 3: Platform Reactivation Report
- **Output file**: kkc_2026-04-22_intelligence_report.html (60KB)

## Pre-Flight QC Results

### Presentation
- [x] Warm palette: `--accent: #C47A4A` — confirmed (2 matches in CSS)
- [x] Google Fonts loads both DM Sans and IBM Plex Mono — confirmed
- [x] Header uses `.h-brand` + `.h-customer` + `.h-type` + `.h-meta` + `.h-accent`
- [x] Reactivation Summary opens with `<ul class="highlights">` as FIRST content — confirmed
- [x] Priority Actions use `.priorities` > `.priority` cards — confirmed (3 cards)
- [x] Platform Status and Peer use `<details class="section-collapse">` — confirmed
- [x] TOC is `<nav class="toc-strip" id="tocStrip">` — confirmed
- [x] `openAndScroll` function included in script — confirmed (2 references)

### Structure
- [x] 5 sections rendered: reactivation-summary, historical-commerce, platform-status, peer, appendix
- [x] Reactivation Summary written last (in methodology; placed first in HTML)
- [x] TOC links only to rendered sections (5 links)
- [x] Peer Benchmarking included (HAS_PEER_DATA = true, tier1, high confidence)
- [x] All INCLUDE sections from manifest present
- [x] No remaining `{{PARAM}}` placeholders — zero hits

### Forbidden Content
- [x] Zero HTML comments (`<!--`) — confirmed
- [x] "ERP" not in report body — confirmed (0 hits)
- [x] "Mixpanel" not in HTML — confirmed (0 hits)
- [x] "Clicky" not in HTML — confirmed (0 hits)
- [x] "health score" not in HTML — confirmed (0 hits)
- [x] `[HYPOTHETICAL]` / `[ESTIMATED]` not in HTML — confirmed (0 hits)
- [x] Internal segment labels not in HTML — confirmed (0 hits)
- [x] `submit_order` / "Order Submission" not in HTML — confirmed (0 hits, MIXPANEL_ORDER_TRACKING_GAP handled)
- [x] "portal orders" / "portal_orders" not in body prose — confirmed (0 hits)
- [x] `operational_health_score` displayed as "Data & Operational Health" — confirmed

### Appendix Contract
- [x] Attribution rows only — 6 data source rows
- [x] No omitted-sections table, methodology, or gating explanations
- [x] No report mode, profile, run parameters, or bundle metadata
- [x] Plain language only — no internal identifiers

## Section Build Status

| § | Section | Status | Highlights | Notes |
|---|---------|--------|------------|-------|
| 1 | Reactivation Summary | Built | 5 highlights | Mode banner + disclosure callout included |
| 2 | Historical Commerce Context | Built | 2 candidates | All-time: 41 orders, $1.08M GMV, iPad only |
| 3 | Platform Status | Built | 4 candidates | 5 subsections: Catalog, Features, Data Health, Pipeline, Config Alerts |
| 4 | Peer Benchmarking | Built | 3 candidates | Hero: Trajectory (Top 30%), 4 metric rows, top performers, feature adoption |
| 5 | Appendix | Built | — | 6 attribution rows |

## Sections Skipped (Mode 3)

| Section | Reason |
|---------|--------|
| Sales Team Performance | No LTM data; HAS_SALES_SECTION = false |
| Customer & Buyer Intelligence | No LTM data |
| Product & Inventory Intelligence | HAS_INVENTORY = false |
| Commerce Analytics | No LTM data |
| Portal Engagement | HAS_CLICKY = false |

## Special Handling Applied

| Flag | Handling |
|------|---------|
| MIXPANEL_ORDER_TRACKING_GAP = true | Removed "Order Submission" from Q-22 feature table. No non-transactional framing. |
| Mode 3 peer caveat | Added: "Peer benchmarks reflect current platform activity among active accounts and may not reflect conditions during this account's last active period." |
| Mode 3 staleness emphasis | Alert callout for 13 stale entities at 257 days. Prerequisite framing for re-activation. |
| Order submission gap guardrail | Top performers framed as "maintaining order flow" not "adopting new behavior" |
