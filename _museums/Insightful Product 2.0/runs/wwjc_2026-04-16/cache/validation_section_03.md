# Validation: §3 Customer & Buyer Intelligence

| Check | Status | Evidence |
|-------|--------|----------|
| **A. Subsection Completeness** | | |
| Subsection 1: Customer Activation & Network Health | PASS | `<div class="subsection-title">` found (line 13) |
| Subsection 2: Dormant High-Value Accounts | PASS | `<div class="subsection-title">` found (line 56) |
| Subsection 3: Reorder Velocity & Early Warning | PASS | `<div class="subsection-title">` found (line 151) |
| Subsection 4: New eCat Buyer Acquisition | PASS | `<div class="subsection-title">` found (line 246) |
| Subsection 5: Geographic Distribution | PASS | `<div class="subsection-title">` found (line 363) |
| section-contents middot list | PASS | All 5 subsection names listed, middot-separated (line 6) |
| **B. Fragment Contract** | | |
| Opens with correct `<details>` | PASS | `<details class="section-collapse" id="customers">` (line 1); id matches §3=customers |
| Closes with `</details>` | PASS | `</details>` on final line (459); nothing after |
| No `<html>/<head>/<body>/<style>` | PASS | grep zero matches |
| No HTML comments | PASS | grep for `<!--` zero matches |
| section-sub is data-dense | PASS | "2,393 active buyers trailing 12 months (17.4% of 13,776 accounts) · $695K dormant at-risk GMV across 20 accounts · 1,048 first-time eCat buyers acquired LTM" |
| expand-hint present | PASS | `<span class="expand-hint">` found (line 8) |
| Inner `<section class="section">` wrapper | PASS | Found (line 10) |
| **C. Subsection Structure** | | |
| subsection-title is first child (all 5) | PASS | Each `<div class="subsection">` opens with `<div class="subsection-title">` |
| what-this-means closes each subsection (all 5) | PASS | Found at lines 50, 145, 240, 357, 453 |
| **D. Forbidden Phrases** | | |
| "health score" / "health scores" | PASS | zero matches |
| "portal orders" / "portal ordering" as buyer activity | PASS | zero matches |
| "net-new customers" | PASS | zero matches |
| "ERP" in client-facing text | PASS | zero matches |
| "Mixpanel" | PASS | zero matches |
| "Clicky" | PASS | zero matches |
| "Platform-Embedded" / "Commerce-Active" / "Catalog-Focused" | PASS | zero matches |
| Internal identifiers (VM codes, query IDs, table/column names, org IDs, dataset paths) | PASS | zero matches |
| "bounce_rate" | PASS | zero matches |
| `order_source` code literals | PASS | zero matches |
| "benchmark_confidence" / "peer_group_level" / "peer_group_n" | PASS | zero matches |
| **D. Hard-Rule Compliance** | | |
| HR-7: Every metric has time qualifier | PASS | Metric labels include "(12 Months)", "(6 Months)", "(3 Months)", "12+ months"; section-sub uses "trailing 12 months" and "LTM"; table headers include "(trailing 12 months)" |
| HR-8: Projections tagged [HYPOTHETICAL] | PASS | "$435K in at-risk annual volume [HYPOTHETICAL]" (line 146) — only projection in fragment is tagged |
| HR-9: Extrapolations tagged [ESTIMATED] | PASS | No extrapolated/annualized figures present; all GMV figures are exact LTM — no tag needed per section guide |
| HR-2: VM-27/28/29/36/48 not surfaced | PASS | No VM-code content or references |
| VM-38b not surfaced | PASS | No VM-38b content |
| HR-4: portal_orders not framed as buyer self-service | PASS | No portal_orders references in fragment |
| **E. Section-Specific Rendering** | | |
| ERP label prohibition — metric-note slots | PASS | Uses "All account records in your system", "% of your full account base" — no "ERP" leakage |
| ERP label prohibition — inline prose | PASS | Uses "Of your 13,776 total accounts", "accounts that ever ordered" — no "ERP" phrasing |
| Q-41 column rule: eCat Online column present (HAS_CART = true) | PASS | Both iPad and eCat Online columns rendered in metrics grid and quarterly table |
| Subsection order matches guide | PASS | Activation → Dormant → Reorder → Acquisition → Geographic (matches guide order 1–5) |
| **F. Highlight File** | | |
| File exists | PASS | `cache/section_03_highlights.md` present |
| 2–4 highlight candidates | PASS | 4 candidates |
| Each has bold headline + context + section link | PASS | All 4 follow format: **bold headline** — context sentence. [→ §customers] |
| Priority action candidate format | PASS | 1 candidate with HIGH urgency, quantified impact, [HYPOTHETICAL] tag, section link |

**VERDICT: PASS**
