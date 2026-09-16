# Validation: §8 Platform & Feature Utilization

| Check | Status | Evidence |
|-------|--------|----------|
| **A. Subsection Completeness** | | |
| Subsection: Catalog Health | PASS | `<div class="subsection-title">Catalog Health</div>` found |
| Subsection: Feature Usage Intensity | PASS | `<div class="subsection-title">Feature Usage Intensity</div>` found |
| Subsection: Data Health Report | PASS | `<div class="subsection-title">Data Health Report</div>` found |
| Subsection: Data Pipeline Health | PASS | `<div class="subsection-title">Data Pipeline Health</div>` found |
| Subsection: Platform Configuration Alerts | PASS | `<div class="subsection-title">Platform Configuration Alerts</div>` found — configuration issues detected, subsection correctly rendered |
| Subsection: Smart Stack Performance | PASS | `<div class="subsection-title">Smart Stack Performance</div>` found — gate met: 8 smart stacks > 0 |
| section-contents middot list | PASS | Lists all 6 subsections: "Catalog Health · Feature Usage Intensity · Data Health Report · Data Pipeline Health · Platform Configuration Alerts · Smart Stack Performance" |
| **B. Fragment Contract Compliance** | | |
| B1: Opens with correct `<details>` tag | PASS | `<details class="section-collapse" id="platform">` on line 1 — matches locked ID |
| B2: Closes with `</details>` on final line | PASS | `</details>` on line 226, nothing after |
| B3: No `<html>`, `<head>`, `<body>`, `<style>` | PASS | Zero matches |
| B4: No HTML comments | PASS | Zero `<!-- -->` matches |
| B5: `section-sub` present, data-dense | PASS | "25 active features · 12 stale entities · 8 smart stacks · import pipeline active" — 4 key stats |
| B6: `expand-hint` span present | PASS | `<span class="expand-hint">▾ Click to expand</span>` found |
| B7: Inner `<section class="section">` wrapper | PASS | `<section class="section" style="margin-bottom:0;border-top:none;...">` found |
| **C. Subsection Structure** | | |
| C1: Every subsection has subsection-title as first child | PASS | All 6 subsections open with `<div class="subsection-title">` |
| C2: Every subsection ends with what-this-means | PASS | All 6 subsections close with `<div class="what-this-means">` |
| **D. Forbidden Phrases** | | |
| D1: "health score" / "health scores" | PASS | Zero matches |
| D2: "portal orders" / "portal ordering" as buyer label | PASS | Zero matches — `portal_orders` entity labeled as "All-Channel Orders" per section guide |
| D3: "net-new customers" | PASS | Zero matches |
| D4: "ERP" | PASS | Zero matches |
| D5: "Mixpanel" | PASS | Zero matches |
| D6: "Clicky" | PASS | Zero matches |
| D7: "Platform-Embedded" | PASS | Zero matches |
| D8: "Commerce-Active" | PASS | Zero matches |
| D9: "Catalog-Focused" | PASS | Zero matches |
| D10: VM codes / query IDs | PASS | Zero matches |
| D11: Table names, column names, org IDs, dataset paths | PASS | Zero matches |
| D12: "bounce_rate" | PASS | Zero matches |
| D13: Code literals (e.g., `order_source = 'ipad'`) | PASS | Zero matches |
| D14: "benchmark_confidence" | PASS | Zero matches |
| D15: "peer_group_level" | PASS | Zero matches |
| D16: "peer_group_n" | PASS | Zero matches |
| D17: Literal `[HYPOTHETICAL]` | PASS | Zero matches |
| D18: Literal `[ESTIMATED]` | PASS | Zero matches |
| **E. Hard Rules** | | |
| E1: Hard Rule 7 — time qualifiers | PASS | Metrics use "current snapshot," "all-time cumulative," "trailing 6 months (October 2025–March 2026)," "3 days ago," "240 days ago," "160 days ago." Semantic accuracy note: cannot mechanically confirm window accuracy. |
| E2: Hard Rule 8a — no literal `[HYPOTHETICAL]` | PASS | Zero matches in fragment |
| E3: Hard Rule 8b — projections use hedging | PASS | "could increase the value of these curated collections" uses "could." "Refreshing...would ensure" uses conditional framing. No quantitative forward-looking projections. |
| E4: Hard Rule 9a — no literal `[ESTIMATED]` | PASS | Zero matches in fragment |
| E5: Hard Rule 9b — extrapolations use hedging | PASS | N/A — no extrapolations identified |
| E6: Hard Rule 2 — VM-27/28/29/36/48 not surfaced | PASS | Zero matches |
| E7: Hard Rule 4 — portal_orders not framed as buyer activity | PASS | N/A — "portal orders" term absent; entity labeled "All-Channel Orders" |
| E8: VM-38b not surfaced | PASS | Zero matches |
| **F. Section-Specific Rendering** | | |
| F1: Freshness labels — 3-label system only | PASS | Only Fresh, Monitor, Stale used. Badge classes: `.badge.ok` (Fresh), `.badge.warn` (Monitor), `.badge.danger` (Stale). No 5-label system. |
| F2: portal_orders entity labeled "All-Channel Orders" | PASS | Line 101: "All-Channel Orders (35 days)" — correct per guide |
| F3: Stale entities in collapsed `<details>` | PASS | `<details>` at line 102 wraps all 12 stale entities; summary line: "12 stale entities — all last updated August 20, 2025" |
| F4: Configuration alerts table — 4 columns | PASS | Columns: Feature, Status, Issue, Action (line 173) |
| F5: section-sub has 3–4 key stats | PASS | 4 stats: "25 active features · 12 stale entities · 8 smart stacks · import pipeline active" |
| F6: No CPQ / Online Ordering listed as gap | PASS | Zero matches — only surfaces features the client has access to |
| F7: Smart Stack gate met | PASS | 8 smart stacks > 0 — subsection correctly included |
| **G. Table Display Limits** | | |
| G1: No table exceeds 15 visible rows | PASS | Largest visible table: Feature Usage at 5 rows. Stale entity table (12 rows) inside collapsed `<details>`. |
| G2: Tables >5 visible rows without collapsed overflow | PASS | All visible tables ≤5 rows; Feature Usage (5 → 5 in overflow), Data Pipeline (5 → 2 in overflow). Stale entity table inside parent collapse. |
| **H. Progressive Disclosure** | | |
| H1: Data Pipeline Health `[COLLAPSE]` wrapped in inner `<details>` | PASS | Inner `<details>` at line 130 |
| H2: Platform Configuration Alerts `[COLLAPSE]` wrapped in inner `<details>` | PASS | Inner `<details>` at line 166 |
| H3: Smart Stack Performance `[COLLAPSE]` wrapped in inner `<details>` | PASS | Inner `<details>` at line 202 |
| **I. Highlight File** | | |
| I1: File exists | PASS | `cache/section_08_highlights.md` found |
| I2: 2–4 highlight candidates | PASS | 4 candidates present |
| I3: Each has bold headline, context, section link | PASS | All 4 have **bold headline**, context sentence, `[→ §platform]` |
| I4: 0–1 priority action with urgency | PASS | 1 priority action candidate, urgency = MEDIUM |
| I5: Priority action projection carries `[HYPOTHETICAL]` tag | PASS | Tag present in cache file — correct for internal pipeline marker |

**VERDICT: PASS**
