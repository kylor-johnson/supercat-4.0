# Validation: §7 Peer Benchmarking

| Check | Status | Evidence |
|-------|--------|----------|
| **A. Subsection Completeness** | | |
| Subsection: Peer Group Overview | PASS | `<div class="subsection-title">Peer Group Overview</div>` found (maps to guide's "Peer Group Header") |
| Subsection: Benchmark Overview | PASS | `<div class="subsection-title">Benchmark Overview</div>` found (maps to guide's Hero Stat + Narrative Metric Rows) |
| Subsection: What Top Performers Do | PASS | `<div class="subsection-title">What Top Performers Do</div>` found |
| Subsection: Feature Adoption | PASS | `<div class="subsection-title">Feature Adoption</div>` found |
| Subsection: Growth Trajectory (skipped) | PASS | Correctly absent — guide says skip until May 2026 (requires 2+ monthly snapshots) |
| section-contents middot list | PASS | Lists 4 rendered subsections: "Peer Group Overview · Benchmark Overview · What Top Performers Do · Feature Adoption" |
| **B. Fragment Contract Compliance** | | |
| B1: Opens with correct `<details>` tag | FAIL | Fragment opens with `id="peer-benchmarking"` but shared_rules.md locked ID is `peer` and section guide specifies `id: peer`. The fragment ID does not match the locked contract specification. |
| B2: Closes with `</details>` on final line | PASS | `</details>` on line 147; trailing blank line is whitespace only |
| B3: No `<html>`, `<head>`, `<body>`, `<style>` | PASS | Zero matches |
| B4: No HTML comments | PASS | Zero `<!-- -->` matches |
| B5: `section-sub` present, data-dense | PASS | "Top quartile across all 6 benchmarked metrics vs. Home & Decor peer group (trailing 12 months)" |
| B6: `expand-hint` span present | PASS | `<span class="expand-hint">▾ Click to expand</span>` found |
| B7: Inner `<section class="section">` wrapper | PASS | `<section class="section" style="margin-bottom:0;border-top:none;...">` found |
| **C. Subsection Structure** | | |
| C1: Every subsection has subsection-title as first child | PASS | All 4 subsections open with `<div class="subsection-title">` |
| C2: Every subsection ends with what-this-means | PASS | All 4 subsections close with `<div class="what-this-means">` |
| **D. Forbidden Phrases** | | |
| D1: "health score" / "health scores" | PASS | Zero matches — operational_health_score row uses "Data & Operational Health" title and "Catalog freshness and import health at 100" sentence phrasing |
| D2: "portal orders" / "portal ordering" as buyer label | PASS | Zero matches |
| D3: "net-new customers" | PASS | Zero matches |
| D4: "ERP" | PASS | Zero matches |
| D5: "Mixpanel" | PASS | Zero matches |
| D6: "Clicky" | PASS | Zero matches |
| D7: "Platform-Embedded" | PASS | Zero matches — peer group uses plain-language "Home & Decor, Housewares, and Art manufacturers" |
| D8: "Commerce-Active" | PASS | Zero matches |
| D9: "Catalog-Focused" | PASS | Zero matches |
| D10: VM codes / query IDs | PASS | Zero matches |
| D11: Table names, column names, org IDs, dataset paths | PASS | Zero matches — internal key `operational_health_score` not exposed |
| D12: "bounce_rate" | PASS | Zero matches |
| D13: Code literals (e.g., `order_source = 'ipad'`) | PASS | Zero matches |
| D14: "benchmark_confidence" | PASS | Zero matches |
| D15: "peer_group_level" | PASS | Zero matches |
| D16: "peer_group_n" | PASS | Zero matches — no raw peer count exposed |
| D17: Literal `[HYPOTHETICAL]` | PASS | Zero matches |
| D18: Literal `[ESTIMATED]` | PASS | Zero matches |
| **E. Hard Rules** | | |
| E1: Hard Rule 7 — time qualifiers | PASS | All metrics include "trailing 12 months" or "trailing 12-month period." Semantic accuracy note: cannot mechanically confirm window accuracy. |
| E2: Hard Rule 8a — no literal `[HYPOTHETICAL]` | PASS | Zero matches in fragment |
| E3: Hard Rule 8b — projections use hedging | PASS | "could streamline complex product ordering" uses "could." "Closing the gap...are the most direct paths" is descriptive recommendation, not quantitative projection. |
| E4: Hard Rule 9a — no literal `[ESTIMATED]` | PASS | Zero matches in fragment |
| E5: Hard Rule 9b — extrapolations use hedging | PASS | N/A — no extrapolations identified |
| E6: Hard Rule 2 — VM-27/28/29/36/48 not surfaced | PASS | Zero matches |
| E7: Hard Rule 4 — portal_orders not framed as buyer activity | PASS | N/A — term absent from fragment |
| E8: VM-38b not surfaced | PASS | Zero matches |
| **F. Section-Specific Rendering** | | |
| F1: `operational_health_score` row title = "Data & Operational Health" | PASS | `<div class="peer-metric-title">Data &amp; Operational Health</div>` — exact match |
| F2: No "health score" in operational_health_score row | PASS | Sentence: "Catalog freshness and import health at 100 out of 100" — approved framing, zero "health score" |
| F3: No confidence labels, tier labels, or raw peer_group_n | PASS | No confidence/tier/count labels exposed; peer group described as "other Home & Decor, Housewares, and Art manufacturers" |
| F4: Feature adoption table has exactly 3 columns | PASS | Columns: "Feature / Capability," "Your Status," "Peer Adoption Rate" |
| F5: Health score not benchmarked | PASS | `health_score` metric not rendered in breakdown |
| F6: Segment labels absent | PASS | Plain-language framing: "Home & Decor, Housewares, and Art manufacturers across a range of platform configurations" |
| F7: BENCHMARK_CONFIDENCE = low — directional framing | PASS | "use them as directional context for the trailing 12-month assessment period" — no confidence label exposed |
| F8: Hero stat uses whitelisted metric | PASS | Hero is Adoption (score 89, Q4). Top applicable per priority list debatable — Engagement also Q4 but 10-point lead vs Adoption's 29.5-point lead. Structural validation: hero metric is on whitelist. |
| F9: All narrative rows use whitelisted metrics | PASS | Value Delivery, Engagement, Data & Operational Health, Trajectory, Catalog Completeness — all on whitelist. orders_90d/orders_per_user correctly omitted (HAS_CART=false). |
| F10: Range bars present on each narrative row | PASS | All 5 narrative rows contain `.peer-range-bar` + `.peer-range-marker above` |
| F11: Quartile pills on each narrative row | PASS | All 5 rows have `.peer-quartile-pill q4` with "Top Quartile" label |
| F12: Top performer patterns 3–5 behavioral items | PASS | 4 patterns using `.top-performer-row` / `.top-performer-icon` / `.top-performer-text` |
| F13: No "health score" in top performer patterns | PASS | Zero matches — patterns describe feature activation, login consistency, scale, workflow efficiency |
| F14: Growth Trajectory correctly absent | PASS | Not rendered — guide: skip until May 2026 |
| F15: One what-this-means per subsection | PASS | Each of 4 subsections has exactly one |
| **G. Table Display Limits** | | |
| G1: No table exceeds 15 visible rows | PASS | Largest table: Feature Adoption at 5 rows |
| G2: Tables >5 visible rows without collapsed overflow | PASS | No table exceeds 5 visible rows |
| **H. Progressive Disclosure** | | |
| H1: What Top Performers Do `[COLLAPSE]` wrapped in inner `<details>` | PASS | Inner `<details>` at line 72 |
| H2: Feature Adoption `[COLLAPSE]` wrapped in inner `<details>` | PASS | Inner `<details>` at line 100 |
| **I. Highlight File** | | |
| I1: File exists | PASS | `cache/section_07_highlights.md` found |
| I2: 2–4 highlight candidates | PASS | 4 candidates present |
| I3: Each has bold headline, context, section link | PASS | All 4 have **bold headline**, context sentence, `[→ §peer-benchmarking]` (note: link target matches fragment ID) |
| I4: 0–1 priority action with urgency | PASS | 1 priority action candidate, urgency = LOW |
| I5: Priority action projection carries `[HYPOTHETICAL]` tag | PASS | Tag present in cache file — correct for internal pipeline marker |

**VERDICT: FAIL**

B1 failure: Fragment uses `id="peer-benchmarking"` but the shared_rules.md locked section ID for §7 is `peer` (and section_07_peer.md guide specifies `id: peer`). This will break anchor links from the Executive Summary and any cross-section references targeting `#peer`. Regeneration should correct the ID to `peer`.
