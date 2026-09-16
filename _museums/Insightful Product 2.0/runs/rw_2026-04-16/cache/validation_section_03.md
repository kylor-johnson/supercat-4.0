# Validation: §3 Customer & Buyer Intelligence

| Check | Status | Evidence |
|-------|--------|----------|
| Subsection 1: Customer Activation & Network Health | PASS | subsection-title found at line 13 |
| Subsection 2: Dormant High-Value Accounts | PASS | subsection-title found at line 56 |
| Subsection 3: Reorder Velocity & Early Warning | PASS | subsection-title found at line 102 |
| Subsection 4: New eCat Buyer Acquisition | PASS | subsection-title found at line 148 |
| Subsection 5: Geographic Distribution | PASS | subsection-title found at line 218 |
| section-contents lists all 5 subsections | PASS | all 5 names present, middot-separated |
| Fragment contract: correct id | PASS | `id="customers"` on line 1 |
| Fragment contract: opens/closes correctly | PASS | opens `<details>` line 1, closes `</details>` line 264, nothing before/after |
| Fragment contract: no banned tags | PASS | no `<html>`, `<head>`, `<body>`, `<style>` found |
| Fragment contract: no HTML comments | PASS | zero `<!--` matches |
| Fragment contract: section-sub present & data-dense | PASS | stat line with 4 data points (1,069 active, 94.4% retention, 25 lapsed/$550K, ON+QC 48%) |
| Fragment contract: expand-hint | PASS | `<span class="expand-hint">` found at line 8 |
| Fragment contract: inner section wrapper | PASS | `<section class="section" ...>` found at line 10 |
| subsection-title as first child (all 5) | PASS | lines 13, 56, 102, 148, 218 each immediately follow their subsection div |
| what-this-means closes (all 5) | PASS | found at lines 50, 96, 142, 212, 258 |
| Forbidden: "health score" / "health scores" | PASS | zero matches |
| Forbidden: "portal orders" / "portal ordering" | PASS | zero matches |
| Forbidden: "net-new customers" | PASS | zero matches |
| Forbidden: "ERP" | PASS | zero matches — metric-notes use "total account records" and "your full account base" |
| Forbidden: "Mixpanel" | PASS | zero matches |
| Forbidden: "Clicky" | PASS | zero matches |
| Forbidden: "Platform-Embedded" / "Commerce-Active" / "Catalog-Focused" | PASS | zero matches |
| Forbidden: internal identifiers (VM codes, query IDs, table names, org IDs) | PASS | zero matches |
| Forbidden: "bounce_rate" | PASS | zero matches |
| Forbidden: `order_source` code literals | PASS | zero matches |
| Forbidden: "benchmark_confidence" / "peer_group_level" / "peer_group_n" | PASS | zero matches |
| Hard Rule 7: time qualifiers on all metrics | PASS | all 18 metric cards include time qualifiers (trailing 12 mo, trailing 6 mo, all-time, as of April 2026, etc.) |
| Hard Rule 8: projections tagged [HYPOTHETICAL] | PASS | no projections in fragment — not applicable |
| Hard Rule 9: extrapolations tagged [ESTIMATED] | PASS | no extrapolations in fragment — not applicable |
| Hard Rule 2: VM-27/28/29/36/48 not surfaced | PASS | no VM content found |
| Hard Rule 4: portal_orders not framed as buyer activity | PASS | "portal_orders" not referenced |
| Rendering: New eCat Buyer Acquisition — iPad column only (HAS_CART=false) | PASS | table has 2 columns (Month, New Buyers iPad); no eCat Online column present |
| Rendering: ERP label prohibition in metric-notes | PASS | line 18 "total account records", line 23 "your full account base", line 29 "total accounts" — no ERP leakage |
| Rendering: ERP label prohibition in prose | PASS | all prose uses "account base" / "accounts" — no ERP references |
| Highlight file exists | PASS | `cache/section_03_highlights.md` present |
| Highlight file: 2–4 candidates | PASS | 4 highlight candidates |
| Highlight file: format correct | PASS | each has bold headline, context sentence with data, section link `[→ §customers]` |
| Highlight file: priority action candidate | PASS | 1 HIGH-urgency candidate with [HYPOTHETICAL] tag and section link |

**VERDICT: PASS**
