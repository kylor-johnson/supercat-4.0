# Validation: §5 Commerce Analytics

| Check | Status | Evidence |
|-------|--------|----------|
| **A. Subsection Completeness** | | |
| Subsection 1: eCat Order Trend | PASS | `<div class="subsection-title">eCat Order Trend</div>` found; Part B (all-channel context) rendered per HAS_PORTAL_ORDERS = true |
| Subsection 2: eCat Ordering Channel Breakdown | PASS | `<div class="subsection-title">eCat Ordering Channel Breakdown</div>` found; gate HAS_CART = true met |
| Subsection 3: Top Buyers & Concentration | PASS | `<div class="subsection-title">Top Buyers &amp; Concentration</div>` found |
| Subsection 4: AOV by Order Segment | PASS | `<div class="subsection-title">AOV by Order Segment</div>` found |
| Subsection 5: Order Type & Workflow | PASS | `<div class="subsection-title">Order Type &amp; Workflow</div>` found |
| Subsection 6: Total Business Context | PASS | `<div class="subsection-title">Total Business Context</div>` found; gate HAS_PORTAL_ORDERS = true met; "ERP" correctly omitted from client-facing title per forbidden phrase rule |
| Subsection 7: eCat Capture Rate | PASS | `<div class="subsection-title">eCat Capture Rate</div>` found; gates HAS_PORTAL_ORDERS = true AND VM45_RENDER = true both met |
| section-contents list | PASS | Lists all 7 rendered subsections separated by ` · `: "eCat Order Trend · eCat Ordering Channel Breakdown · Top Buyers & Concentration · AOV by Order Segment · Order Type & Workflow · Total Business Context · eCat Capture Rate" |
| **B. Fragment Contract** | | |
| Opens with correct `<details>` | PASS | `<details class="section-collapse" id="commerce">` — correct id per locked map §5=commerce |
| Closes with `</details>` | PASS | Final line is `</details>`, nothing after |
| No `<html>/<head>/<body>/<style>` | PASS | Zero matches |
| No HTML comments | PASS | Zero `<!-- -->` matches |
| section-sub is data-dense | PASS | "$9.0M eCat GMV across 6,232 orders trailing 12 months · 50.2% GMV capture of $17.8M all-channel business · AOV $1,437 · eCat Online: 79.7% of volume" — data-dense stat line |
| expand-hint present | PASS | `<span class="expand-hint">&#9662; Click to expand</span>` found |
| Inner `<section>` wrapper | PASS | `<section class="section" style="margin-bottom:0;border-top:none;border-radius:0 0 var(--r) var(--r);">` present |
| **C. Subsection Structure** | | |
| subsection-title as first child (all 7) | PASS | Every `<div class="subsection">` has `<div class="subsection-title">` as immediate first child |
| what-this-means closes (all 7) | PASS | All 7 subsections end with `<div class="what-this-means">` containing actionable close |
| **D. Forbidden Phrases & Hard Rules** | | |
| Forbidden: "health score" / "health scores" | PASS | Zero matches |
| Forbidden: "portal orders" / "portal ordering" as entity | PASS | Zero matches — all-channel framing used instead |
| Forbidden: "net-new customers" | PASS | Zero matches |
| Forbidden: "ERP" | PASS | Zero matches — "your business system", "all-channel" used |
| Forbidden: "Mixpanel" | PASS | Zero matches |
| Forbidden: "Clicky" | PASS | Zero matches |
| Forbidden: segment labels | PASS | No "Platform-Embedded", "Commerce-Active", or "Catalog-Focused" |
| Forbidden: internal identifiers (VM codes, query IDs, table/column names, org IDs) | PASS | Zero matches |
| Forbidden: "bounce_rate" | PASS | Zero matches |
| Forbidden: code literals (`order_source = 'ipad'` etc.) | PASS | Zero matches |
| Forbidden: "benchmark_confidence" / "peer_group_level" / "peer_group_n" | PASS | Zero matches |
| Hard Rule 7: time qualifiers on every metric | PASS | All metrics include "trailing 12 months", quarter labels (Q1 2026, Q4 2025), or "full months" qualifier |
| Hard Rule 8: projections tagged [HYPOTHETICAL] | PASS | No projections in fragment — N/A |
| Hard Rule 9: extrapolations tagged [ESTIMATED] | PASS | No extrapolations in fragment — N/A |
| Hard Rule 2: VM-27/28/29/36/48 not surfaced | PASS | Zero matches |
| VM-38b not surfaced | PASS | Zero matches |
| Hard Rule 4: portal_orders not framed as buyer activity | PASS | All portal_orders data presented as "all-channel" business context; no "portal ordering" or buyer-activity framing |
| **E. Section-Specific Rendering** | | |
| eCat Order Trend Part B (all-channel context) | PASS | Table includes All-Channel GMV and eCat Share columns; HAS_PORTAL_ORDERS = true gate met |
| Channel Breakdown: iPad vs eCat Online split | PASS | Metrics grid shows both channels with order count, GMV, and percentage breakdowns |
| Top Buyers: 4-column table (Customer / Orders / GMV / % of eCat GMV) | PASS | Exact columns present in correct order |
| Top Buyers: concentration callout gate | PASS | Top-5 = 10.6% < 25% threshold — callout correctly omitted |
| Channel attribution statement (HAS_CART = true) | PASS | Exact statement found: "All eCat orders originate from one of two sources: iPad (rep-submitted) or eCat Online (buyer self-service)." |
| VM-45 capture rate: VM45_RENDER = true → subsection rendered | PASS | eCat Capture Rate subsection present with valid denominator context ($9.0M of $17.8M) |
| HAS_PORTAL_ORDERS gated subsections (1B, 6, 7) all rendered | PASS | All three gated subsections present |
| **F. Highlight File** | | |
| cache/section_05_highlights.md exists | PASS | File found |
| 2–4 highlight candidates | PASS | 4 candidates present |
| Each highlight: bold headline + context + section link | PASS | All 4 have **bold headline**, context sentence with data, `[→ §commerce]` link |
| Priority action candidate format | PASS | 1 candidate with MEDIUM urgency, quantified impact, [HYPOTHETICAL] tag, section link |

**VERDICT: PASS**
