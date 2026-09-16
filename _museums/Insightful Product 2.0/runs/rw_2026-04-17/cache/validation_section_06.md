# Validation: §6 Portal Engagement

| Check | Status | Evidence |
|-------|--------|----------|
| **A. Subsection Completeness** | | |
| Subsection: Traffic Health | PASS | `<div class="subsection-title">Traffic Health</div>` found |
| Subsection: Monthly Traffic Trend | PASS | `<div class="subsection-title">Monthly Traffic Trend</div>` found |
| Subsection: Geographic Demand | PASS | `<div class="subsection-title">Geographic Demand</div>` found |
| Subsection: Traffic Sources (conditional) | PASS | Absent from fragment — guide allows silent omission when Q-CL-05 shows 100% direct traffic. Validator does not read Q files; structural omission is consistent with the conditional rule. |
| section-contents middot list | PASS | Lists 3 rendered subsections: "Traffic Health · Monthly Traffic Trend · Geographic Demand" — Traffic Sources correctly excluded |
| **B. Fragment Contract Compliance** | | |
| B1: Opens with correct `<details>` tag | PASS | `<details class="section-collapse" id="portal">` on line 1 |
| B2: Closes with `</details>` on final line | PASS | `</details>` on line 118, nothing after |
| B3: No `<html>`, `<head>`, `<body>`, `<style>` | PASS | Zero matches |
| B4: No HTML comments | PASS | Zero `<!-- -->` matches |
| B5: `section-sub` present, data-dense | PASS | "1.4 avg daily visitors trailing 6 months · 227 monthly pageviews · Canada 45%, U.S. 54% of traffic" |
| B6: `expand-hint` span present | PASS | `<span class="expand-hint">▾ Click to expand</span>` found |
| B7: Inner `<section class="section">` wrapper | PASS | `<section class="section" style="margin-bottom:0;border-top:none;...">` found |
| **C. Subsection Structure** | | |
| C1: Every subsection has subsection-title as first child | PASS | All 3 subsections open with `<div class="subsection-title">` |
| C2: Every subsection ends with what-this-means | PASS | All 3 subsections close with `<div class="what-this-means">` |
| **D. Forbidden Phrases** | | |
| D1: "health score" / "health scores" | PASS | Zero matches |
| D2: "portal orders" / "portal ordering" as buyer label | PASS | Zero matches |
| D3: "net-new customers" | PASS | Zero matches |
| D4: "ERP" | PASS | Zero matches |
| D5: "Mixpanel" | PASS | Zero matches |
| D6: "Clicky" | PASS | Zero matches — portal traffic data referenced generically |
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
| E1: Hard Rule 7 — time qualifiers | PASS | All metrics include qualifiers: "Trailing 6 months (Oct 2025 – Mar 2026)," "April 2026 month-to-date," monthly labels in trend table. Semantic accuracy note: cannot mechanically confirm window accuracy. |
| E2: Hard Rule 8a — no literal `[HYPOTHETICAL]` | PASS | Zero matches in fragment |
| E3: Hard Rule 8b — projections use hedging | PASS | "Your portal averages roughly 1 visitor per day" — "roughly." Forward-looking framing uses cautious language ("Monitoring whether mid-2026 traffic stabilizes will help establish a reliable baseline"). No quantitative projections found. |
| E4: Hard Rule 9a — no literal `[ESTIMATED]` | PASS | Zero matches in fragment |
| E5: Hard Rule 9b — extrapolations use hedging | PASS | N/A — no extrapolations identified |
| E6: Hard Rule 2 — VM-27/28/29/36/48 not surfaced | PASS | Zero matches; traffic trend is descriptive with no churn-signal framing (VM-36 compliant) |
| E7: Hard Rule 4 — portal_orders not framed as buyer activity | PASS | N/A — term absent from fragment |
| E8: VM-38b not surfaced | PASS | Zero matches |
| **F. Section-Specific Rendering** | | |
| F1: VM-36 prohibition — no churn-signal framing | PASS | Traffic trend is purely descriptive; no framing of decline as churn signal |
| F2: Clicky naming — never appears | PASS | Verified in D6 — zero "Clicky" matches |
| F3: One what-this-means per subsection max | PASS | Each of 3 subsections has exactly one what-this-means block |
| F4: Traffic Sources conditional omission | PASS | Subsection absent; consistent with 100% direct traffic rule. Data condition not verified (validator scope). |
| **G. Table Display Limits** | | |
| G1: No table exceeds 15 visible rows | PASS | Largest visible table: Monthly Traffic Trend at 7 rows |
| G2: Tables >5 visible rows without collapsed overflow | WARN | Monthly Traffic Trend table has 7 visible rows (Oct 2025 – Apr 2026 MTD) without collapsed `<details>` overflow. Shared_rules default: >5 visible rows should use overflow. However, this is a 7-month trend where truncation may harm readability. |
| **H. Progressive Disclosure** | | |
| H1: Geographic Demand `[COLLAPSE]` wrapped in inner `<details>` | PASS | Inner `<details>` at line 73 wraps Geographic Demand subsection |
| H2: Traffic Sources `[COLLAPSE]` (omitted) | PASS | Subsection omitted per conditional rule — no progressive disclosure check needed |
| **I. Highlight File** | | |
| I1: File exists | PASS | `cache/section_06_highlights.md` found |
| I2: 2–4 highlight candidates | PASS | 3 candidates present |
| I3: Each has bold headline, context, section link | PASS | All 3 have **bold headline**, context sentence, `[→ §portal]` |
| I4: 0–1 priority action with urgency | PASS | 1 priority action candidate, urgency = MEDIUM |
| I5: Priority action projection carries `[HYPOTHETICAL]` tag | PASS | Tag present in cache file — correct for internal pipeline marker |

**VERDICT: PASS**
