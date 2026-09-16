# Validation: §5 Commerce Analytics

| Check | Status | Evidence |
|-------|--------|----------|
| Subsection count | PASS | 4 subsections rendered; matches expected (4 of 7 with gates met) |
| Subsection 1: eCat Order Trend | PASS | subsection-title found at line 13 |
| Subsection 2: Top Buyers & Concentration | PASS | subsection-title found at line 72 |
| Subsection 3: AOV by Order Segment | PASS | subsection-title found at line 105 |
| Subsection 4: Order Type & Workflow | PASS | subsection-title found at line 141 |
| Skipped: eCat Ordering Channel Breakdown | PASS | not present (HAS_CART=false) |
| Skipped: ERP Total Business Context | PASS | not present (HAS_PORTAL_ORDERS=false) |
| Skipped: eCat Capture Rate | PASS | not present (HAS_PORTAL_ORDERS=false, VM45_RENDER=false) |
| section-contents accuracy | PASS | lists exactly 4 rendered names: "eCat Order Trend · Top Buyers & Concentration · AOV by Order Segment · Order Type & Workflow" |
| Fragment contract: id | PASS | `id="commerce"` correct |
| Fragment contract: open/close | PASS | opens `<details class="section-collapse" id="commerce">` at line 1; closes `</details>` at line 170; nothing before or after |
| Fragment contract: banned tags | PASS | no `<html>`, `<head>`, `<body>`, `<style>` tags |
| Fragment contract: no HTML comments | PASS | zero `<!-- -->` matches |
| Fragment contract: section-sub | PASS | data-dense stat line: "7,684 eCat orders · $9.5M GMV · $1,236 AOV · trailing 12 months" |
| Fragment contract: expand-hint | PASS | `<span class="expand-hint">&#9662; Click to expand</span>` present |
| Fragment contract: inner section wrapper | PASS | `<section class="section" style="margin-bottom:0;border-top:none;border-radius:0 0 var(--r) var(--r);">` present |
| Structure: subsection-title as first child | PASS | confirmed for all 4 subsections |
| Structure: what-this-means closes | PASS | found at lines 66, 99, 135, 164 — one per subsection |
| Forbidden: "health score" / "health scores" | PASS | zero matches |
| Forbidden: "portal orders" / "portal ordering" | PASS | zero matches |
| Forbidden: "net-new customers" | PASS | zero matches |
| Forbidden: "ERP" | PASS | zero matches |
| Forbidden: "total business" | PASS | zero matches |
| Forbidden: "all-channel" | PASS | zero matches |
| Forbidden: "capture rate" | PASS | zero matches |
| Forbidden: "channel breakdown" | PASS | zero matches |
| Forbidden: "Mixpanel" | PASS | zero matches |
| Forbidden: "Clicky" | PASS | zero matches |
| Forbidden: segment labels | PASS | zero matches for Platform-Embedded, Commerce-Active, Catalog-Focused |
| Forbidden: internal identifiers | PASS | no VM codes, query IDs, table names, column names, org IDs, dataset paths |
| Forbidden: "bounce_rate" | PASS | zero matches |
| Forbidden: code literals | PASS | no `order_source = 'ipad'` or similar |
| Forbidden: "benchmark_confidence" / "peer_group_level" / "peer_group_n" | PASS | zero matches |
| Hard Rule 7: time qualifiers | PASS | all metrics carry qualifiers ("trailing 12 months," specific months, "MTD") |
| Hard Rule 8: projections tagged [HYPOTHETICAL] | PASS | no quantified projections in fragment; no tag required |
| Hard Rule 9: extrapolations tagged [ESTIMATED] | PASS | no extrapolations in fragment; no tag required |
| Rendering: eCat Order Trend Part A only | PASS | shows eCat-originated order trend; no Part B all-channel context |
| Rendering: no channel attribution statement | PASS | two-source attribution statement absent (HAS_CART=false); factual single-channel observation is appropriate |
| Rendering: Top Buyers table columns | PASS | exactly 4 columns: Customer, Orders, GMV, % of eCat GMV |
| Rendering: concentration callout logic | PASS | top-5 at 22.5% — below 25% threshold; no concentration callout rendered (correct) |
| Highlight file: exists | PASS | cache/section_05_highlights.md present |
| Highlight file: candidate count | PASS | 4 highlight candidates (within 2–4 range) |
| Highlight file: format | PASS | each candidate has **bold headline**, context sentence with data, section link [→ §commerce] |
| Highlight file: priority action | PASS | 1 candidate, MEDIUM urgency, includes [HYPOTHETICAL] tag |

**VERDICT: PASS**
