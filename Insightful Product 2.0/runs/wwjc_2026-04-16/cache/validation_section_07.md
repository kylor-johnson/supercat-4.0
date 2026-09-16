# Validation: §7 Peer Benchmarking

| Check | Status | Evidence |
|-------|--------|----------|
| **A: Subsection Completeness** | | |
| Subsection 1: Your Peer Group | PASS | `<div class="subsection-title">Your Peer Group</div>` found; combines Peer Group Header + Hero Stat |
| Subsection 2: Benchmark Breakdown | PASS | `<div class="subsection-title">Benchmark Breakdown</div>` found |
| Subsection 3: What Top Performers Do | PASS | `<div class="subsection-title">What Top Performers Do</div>` found |
| Subsection 4: Feature Adoption | PASS | `<div class="subsection-title">Feature Adoption</div>` found |
| Subsection 6: Growth Trajectory omitted | PASS | Correctly omitted — guide says "Skip until May 2026" |
| section-contents matches rendered subsections | PASS | `Your Peer Group · Benchmark Breakdown · What Top Performers Do · Feature Adoption` — all 4 match |
| **B: Fragment Contract** | | |
| Opens with `<details class="section-collapse" id="peer">` | PASS | Line 1 — correct id per §7=peer |
| Closes with `</details>`, nothing after | PASS | Line 168 — clean close, no trailing content |
| No `<html>`, `<head>`, `<body>`, `<style>` tags | PASS | Grep: zero matches |
| No HTML comments `<!-- -->` | PASS | Grep: zero matches |
| `section-sub` is data-dense stat line | PASS | "1,797 orders/90d (9× peer median) · value delivery leads cohort at 85 · per-user ordering 36% below median" |
| `expand-hint` span present | PASS | `<span class="expand-hint">&#9662; Click to expand</span>` found |
| Inner `<section class="section" ...>` wrapper | PASS | Line 10 — present with correct style attributes |
| **C: Subsection Structure** | | |
| Your Peer Group: subsection-title as first child | PASS | First child is `<div class="subsection-title">` |
| Your Peer Group: ends with what-this-means | PASS | `<div class="what-this-means">` closes subsection |
| Benchmark Breakdown: subsection-title as first child | PASS | First child is `<div class="subsection-title">` |
| Benchmark Breakdown: ends with what-this-means | PASS | `<div class="what-this-means">` closes subsection |
| What Top Performers Do: subsection-title as first child | PASS | First child is `<div class="subsection-title">` |
| What Top Performers Do: ends with what-this-means | PASS | `<div class="what-this-means">` closes subsection |
| Feature Adoption: subsection-title as first child | PASS | First child is `<div class="subsection-title">` |
| Feature Adoption: ends with what-this-means | PASS | `<div class="what-this-means">` closes subsection |
| **D: Forbidden Phrases & Hard Rules** | | |
| Forbidden: "health score" / "health scores" | PASS | Grep: zero matches (case-insensitive) |
| Forbidden: "portal orders" / "portal ordering" as buyer activity | PASS | Zero matches |
| Forbidden: "net-new customers" | PASS | Zero matches |
| Forbidden: "ERP" | PASS | Zero matches |
| Forbidden: "Mixpanel" | PASS | Zero matches |
| Forbidden: "Clicky" | PASS | Zero matches |
| Forbidden: segment labels | PASS | Zero matches for Platform-Embedded, Commerce-Active, Catalog-Focused |
| Forbidden: internal identifiers (VM codes, query IDs, table names, org IDs) | PASS | Zero matches |
| Forbidden: "bounce_rate" | PASS | Zero matches |
| Forbidden: code literals (`order_source = 'ipad'` etc.) | PASS | Zero matches |
| Forbidden: "benchmark_confidence" / "peer_group_level" / "peer_group_n" | PASS | Zero matches |
| Hard Rule 7: every metric has time qualifier | PASS | All metric sentences include "last 90 days", "trailing 12 months", "(90 Days)", or "(90-Day)" |
| Hard Rule 8: projections tagged [HYPOTHETICAL] | PASS | No projections in fragment |
| Hard Rule 9: extrapolations tagged [ESTIMATED] | PASS | No extrapolations in fragment |
| Hard Rule 2: VM-27/28/29/36/48 not surfaced | PASS | Zero matches |
| VM-38b not surfaced | PASS | Zero matches |
| Hard Rule 4: portal_orders not framed as buyer self-service | PASS | No portal_orders mention |
| Hard Rule 5: segment labels not in §7 | PASS | Plain-language framing used throughout |
| Hard Rule 11: internal signals not exposed as labels | PASS | No benchmark_confidence, peer_group_level, or peer_group_n labels |
| **E: Section-Specific Rendering** | | |
| `operational_health_score` row title = "Data & Operational Health" | PASS | Line 76: `Data &amp; Operational Health` — correct |
| `operational_health_score` sentence uses approved framing | PASS | "Catalog freshness and import reliability at 100" — no "health score" vocabulary |
| No confidence labels, tier labels, or raw peer_group_n counts | PASS | Plain-language framing only; no "tier", "confidence", or literal peer count |
| Segment label rule: plain-language cohort framing | PASS | "Lighting manufacturers on the same platform bundle" used consistently — correct Tier 1 framing for Lighting / Full |
| Feature adoption table has exactly 3 columns | PASS | Feature / Capability, Your Status, Peer Adoption Rate — 3 columns |
| Hero stat uses metric from priority list | PASS | `orders_per_user` selected; HAS_CART=true per gate_flags |
| Hero stat not `health_score` | PASS | Hero is orders_per_user |
| Hero stat percentile badge class correct for quartile | **FAIL** | Line 20: `<span class="peer-hero-pctile on-par">Bottom 25%</span>` — "Bottom 25%" = Q1. Per §7 guide: Q1 requires class `.below`, not `.on-par` (`.on-par` is for Q2 only) |
| Top performers rendered as primary content (not collapsed) | PASS | No `<details>` wrapper around top-performer subsection |
| Top performers prose: no "health score" vocabulary | PASS | Zero matches in subsection |
| Metric whitelist compliance | PASS | All 7 breakdown rows use whitelisted metrics; hero (orders_per_user) correctly excluded from breakdown |
| Growth Trajectory subsection correctly omitted | PASS | Guide says "Skip until May 2026" — not rendered |
| peer_group_n not exposed as literal count | PASS | No raw count (e.g., "8 accounts") in delivered text |
| **F: Highlight File** | | |
| File exists | PASS | `cache/section_07_highlights.md` found |
| Contains 2–4 highlight candidates | PASS | 4 candidates present |
| Each highlight: bold headline + context + section link | PASS | All 4 have **bold headline**, context sentence with data, `[→ §peer]` link |
| Priority action candidate format | PASS | 1 candidate with MEDIUM urgency, action statement, [HYPOTHETICAL] tag, section link |

**VERDICT: FAIL**

## Failed Checks

1. **Hero stat percentile badge class** (Check E)
   - **Location**: Line 20 of `fragments/section_07.html`
   - **Found**: `<span class="peer-hero-pctile on-par">Bottom 25%</span>`
   - **Expected**: `<span class="peer-hero-pctile below">Bottom 25%</span>`
   - **Rule**: section_07_peer.md §2 — "Apply class `.above` for Q3/Q4, `.below` for Q1, `.on-par` for Q2." The text "Bottom 25%" indicates Q1 (Bottom Quartile), which requires `.below`, not `.on-par`.
