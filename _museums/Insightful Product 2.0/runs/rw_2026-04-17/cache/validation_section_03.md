# Validation: §3 Customer & Buyer Intelligence

| Check | Status | Evidence |
|-------|--------|----------|
| **A. Subsection Completeness** | | |
| Subsection: Customer Activation & Network Health | PASS | `<div class="subsection-title">Customer Activation &amp; Network Health</div>` found |
| Subsection: Dormant High-Value Accounts | PASS | `<div class="subsection-title">Dormant High-Value Accounts</div>` found |
| Subsection: Geographic Distribution | PASS | `<div class="subsection-title">Geographic Distribution</div>` found |
| Subsection: Reorder Velocity & Early Warning | PASS | `<div class="subsection-title">Reorder Velocity &amp; Early Warning</div>` found |
| Subsection: New eCat Buyer Acquisition | PASS | `<div class="subsection-title">New eCat Buyer Acquisition</div>` found |
| section-contents middot list | PASS | Lists all 5 subsections, middot-separated |
| **B. Fragment Contract Compliance** | | |
| B1: Opens with correct `<details>` tag | PASS | `<details class="section-collapse" id="customers">` on line 1 |
| B2: Closes with `</details>` on final line | PASS | `</details>` on line 621, nothing after |
| B3: No `<html>`, `<head>`, `<body>`, `<style>` | PASS | Zero matches |
| B4: No HTML comments | PASS | Zero `<!-- -->` matches |
| B5: `section-sub` present, data-dense | PASS | "1,071 active buyers (trailing 12 months) · 94.4% retention rate · 64 lapsed accounts · 3,756 never activated" |
| B6: `expand-hint` span present | PASS | `<span class="expand-hint">▾ Click to expand</span>` found |
| B7: Inner `<section class="section">` wrapper | PASS | `<section class="section" style="margin-bottom:0;border-top:none;...">` found |
| **C. Subsection Structure** | | |
| C1: Every subsection has subsection-title as first child | PASS | All 5 subsections open with `<div class="subsection-title">` |
| C2: Every subsection ends with what-this-means | PASS | All 5 subsections close with `<div class="what-this-means">` |
| **D. Forbidden Phrases** | | |
| D1: "health score" / "health scores" | PASS | Zero matches |
| D2: "portal orders" / "portal ordering" as buyer label | PASS | Zero matches |
| D3: "net-new customers" | PASS | Zero matches |
| D4: "ERP" | PASS | Zero matches — uses "account records in your system," "your full account base," "total accounts" |
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
| E1: Hard Rule 7 — time qualifiers | PASS | All metrics include time qualifiers: "Trailing 12 Months," "Trailing 6 Months," "Trailing 3 Months," "All-Time," "Trailing 15 Months," "Mar 2026." Semantic accuracy note: cannot mechanically confirm window accuracy. |
| E2: Hard Rule 8a — no literal `[HYPOTHETICAL]` | PASS | Zero matches in fragment |
| E3: Hard Rule 8b — projections use hedging | PASS | "Converting even 10% of this base would add roughly 376 active buyers" — uses "roughly." No other projection statements found. |
| E4: Hard Rule 9a — no literal `[ESTIMATED]` | PASS | Zero matches in fragment |
| E5: Hard Rule 9b — extrapolations use hedging | PASS | N/A — no extrapolations identified in this section |
| E6: Hard Rule 2 — VM-27/28/29/36/48 not surfaced | PASS | Zero matches |
| E7: Hard Rule 4 — portal_orders not framed as buyer activity | PASS | N/A — term absent from fragment |
| E8: VM-38b not surfaced | PASS | Zero matches |
| **F. Section-Specific Rendering** | | |
| F1: ERP label prohibition — metric-note slots | PASS | All metric-note text uses "account records in your system," "your full account base," "total accounts" — zero "ERP" mentions |
| F2: ERP label prohibition — prose | PASS | Prose uses "total account records," "your full account base" — zero "ERP" mentions |
| F3: Dormant table — top 5 visible, rest collapsed | PASS | 5 rows visible in primary table; 15 more in collapsed `<details>` |
| F4: New eCat Buyer Acquisition — iPad column only (HAS_CART=false) | PASS | Monthly table headers: "Month" + "New eCat Buyers (iPad)" — no eCat Online column |
| F5: Reorder velocity — top 5 + flagged decelerators only | PASS | 5 rows in table; prose states no deceleration flags |
| **G. Table Display Limits** | | |
| G1: No table exceeds 15 visible rows | PASS | All visible tables ≤5 rows; overflow tables ≤15 rows |
| G2: Tables >5 visible rows without collapsed overflow | PASS | All visible portions are ≤5 rows; overflows wrapped in `<details>` |
| **H. Progressive Disclosure** | | |
| H1: Geographic Distribution `[COLLAPSE]` wrapped in inner `<details>` | PASS | Inner `<details>` at line 238 wraps entire Geographic Distribution subsection |
| H2: New eCat Buyer Acquisition `[COLLAPSE]` wrapped in inner `<details>` | PASS | Inner `<details>` at line 425 wraps entire New eCat Buyer Acquisition subsection |
| **I. Highlight File** | | |
| I1: File exists | PASS | `cache/section_03_highlights.md` found |
| I2: 2–4 highlight candidates | PASS | 4 candidates present |
| I3: Each has bold headline, context, section link | PASS | All 4 have **bold headline**, context sentence, `[→ §customers]` |
| I4: 0–1 priority action with urgency | PASS | 1 priority action candidate, urgency = HIGH |
| I5: Priority action projection carries `[HYPOTHETICAL]` tag | PASS | Tag present in cache file — correct for internal pipeline marker |
| **§3 Re-validation Focus** | | |
| Dormant overflow table ≤15 rows (previously 20) | PASS | Overflow table contains exactly 15 rows (Berry's Furniture through Ramsower's Furniture) — fixed from prior 20-row defect |
| "Converting even 10%..." uses hedging, no literal `[HYPOTHETICAL]` | PASS | Sentence uses "roughly" (correct hedging); zero literal `[HYPOTHETICAL]` tags — prior false-positive resolved under updated rules |

**VERDICT: PASS**
