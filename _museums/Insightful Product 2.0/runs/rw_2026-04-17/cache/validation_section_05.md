# Validation: §5 Commerce Analytics

| Check | Status | Evidence |
|-------|--------|----------|
| A: Subsection 1 — eCat Order Trend (Part A only) | PASS | `<div class="subsection-title">eCat Order Trend — Trailing 12 Months</div>` present (line 13); Part B correctly absent (HAS_PORTAL_ORDERS=false) |
| A: Subsection 2 — AOV by Order Segment | PASS | `<div class="subsection-title">AOV by Order Segment — Trailing 12 Months</div>` present (line 70) |
| A: Subsection 3 — eCat Ordering Channel Breakdown | PASS | Correctly absent; gate requires HAS_CART=true; HAS_CART=false |
| A: Subsection 4 — Top Buyers & Concentration | PASS | `<div class="subsection-title">Top Buyers &amp; Concentration — Trailing 12 Months</div>` present (line 104) |
| A: Subsection 5 — Order Type & Workflow | PASS | `<div class="subsection-title">Order Type &amp; Workflow — Trailing 12 Months</div>` present (line 143) |
| A: Subsection 6 — ERP Total Business Context | PASS | Correctly absent; gate requires HAS_PORTAL_ORDERS=true; HAS_PORTAL_ORDERS=false |
| A: Subsection 7 — eCat Capture Rate | PASS | Correctly absent; VM45_RENDER=false and HAS_PORTAL_ORDERS=false |
| A: section-contents middot list | WARN | Lists "eCat Order Trend · AOV by Order Segment · Top Buyers & Concentration · Order Type & Workflow" — all 4 rendered subsections present. However, subsection-titles in fragment include "— Trailing 12 Months" suffix which is not reflected in section-contents. Consistent across all 4 subsections; not a structural failure |
| B1: Opens with correct `<details>` | PASS | Line 1: `<details class="section-collapse" id="commerce">` — correct ID |
| B2: Closes with `</details>` | PASS | Line 163: `</details>` — nothing after |
| B3: No `<html>/<head>/<body>/<style>` tags | PASS | Grep confirms zero matches |
| B4: No HTML comments | PASS | Grep confirms zero `<!-- -->` matches |
| B5: `section-sub` present with data-dense stat line | PASS | Line 5: "7,691 eCat orders · $9.5M GMV trailing 12 months · $1,236 avg order value · 100% rep-submitted" |
| B6: `expand-hint` span present | PASS | Line 8: `<span class="expand-hint">&#9662; Click to expand</span>` |
| B7: Inner `<section class="section">` wrapper present | PASS | Line 10: `<section class="section" style="margin-bottom:0;border-top:none;border-radius:0 0 var(--r) var(--r);">` |
| C1: Every subsection has `subsection-title` as first child | PASS | All 4 subsections open with `<div class="subsection-title">` immediately after `<div class="subsection">` |
| C2: Every subsection ends with `what-this-means` | PASS | All 4 subsections end with `<div class="what-this-means">` (lines 64, 98, 137, 157) |
| D1: Forbidden — "health score/scores" | PASS | Zero matches |
| D2: Forbidden — "portal orders/ordering" | PASS | Zero matches |
| D3: Forbidden — "net-new customers" | PASS | Zero matches |
| D4: Forbidden — "ERP" | PASS | Zero matches; no mention of ERP, total business, or portal_orders (correct per HAS_PORTAL_ORDERS=false rule) |
| D5: Forbidden — "Mixpanel" | PASS | Zero matches |
| D6: Forbidden — "Clicky" | PASS | Zero matches |
| D7: Forbidden — "Platform-Embedded" | PASS | Zero matches |
| D8: Forbidden — "Commerce-Active" | PASS | Zero matches |
| D9: Forbidden — "Catalog-Focused" | PASS | Zero matches |
| D10: Forbidden — VM codes / query IDs | PASS | Zero matches |
| D11: Forbidden — table names, column names, org IDs, dataset paths | PASS | Zero matches |
| D12: Forbidden — "bounce_rate" | PASS | Zero matches |
| D13: Forbidden — code literals | PASS | Zero matches for `order_source` |
| D14: Forbidden — "benchmark_confidence" | PASS | Zero matches |
| D15: Forbidden — "peer_group_level" | PASS | Zero matches |
| D16: Forbidden — "peer_group_n" | PASS | Zero matches |
| E1: Hard Rule 7 — time qualifiers on metrics | PASS | All metrics carry "LTM," "trailing 12 months," or specific month references (e.g., "Oct 2025"). Subsection titles include "— Trailing 12 Months." Semantic accuracy not mechanically confirmable |
| E2: Hard Rule 8 — projections tagged [HYPOTHETICAL] | PASS | No quantified projections in fragment body. Qualitative statements like "could meaningfully lift" (line 99) are general observations, not tagged projections. No numerical hypotheticals present |
| E3: Hard Rule 9 — extrapolations tagged [ESTIMATED] | PASS | No extrapolations present; N/A |
| E4: Hard Rule 2 — VM-27/28/29/36/48 not surfaced | PASS | Zero matches |
| E5: Hard Rule 4 — portal_orders not framed as buyer activity | PASS | Term absent from fragment; N/A. No mention of "total business," "portal_orders," or ERP (correct per HAS_PORTAL_ORDERS=false) |
| E6: VM-38b not surfaced | PASS | Zero matches |
| F1: VM-45 capture rate absent (VM45_RENDER=false) | PASS | No capture rate subsection rendered |
| F2: Cart-dependent subsections absent (HAS_CART=false) | PASS | No eCat Ordering Channel Breakdown subsection; no channel attribution statement (not required when HAS_CART=false) |
| F3: ERP/portal_orders subsections absent (HAS_PORTAL_ORDERS=false) | PASS | Subsections 6 and 7 absent; Q-18 Part B absent; no ERP/total-business/portal_orders mentions |
| F4: Top Buyers table — correct 4 columns | PASS | Customer / Orders / GMV / % of eCat GMV (line 108) |
| F5: Top 10 buyers — 5 visible + 5 in `<details>` | PASS | 5 visible rows (lines 111–115); 5 in collapsed details (lines 125–129). Total = 10 |
| F6: Concentration callout (top-5 > 25%) | PASS | Top-5 share = 22.4% (below 25%); no concentration callout required. Buyer Profile Contrast insight callout present instead — appropriate |
| G: Table display — max 15 rows per table | PASS | Largest table: 8 rows (eCat Order Trend overflow). All under 15 |
| G: Table display — >5 visible rows without `<details>` overflow | PASS | All visible tables ≤5 rows; overflow in `<details>` where applicable |
| H: Progressive disclosure | PASS | No [COLLAPSE]-tagged subsections in §5 guide; N/A |
| I: Highlight file exists | PASS | `cache/section_05_highlights.md` present |
| I: Highlight count 2–4 | PASS | 4 highlight candidates |
| I: Highlight format | PASS | Each has **bold headline**, context sentence, section link `[→ §commerce]` |
| I: Priority action candidate | PASS | 1 priority action with urgency "MEDIUM" and [HYPOTHETICAL] tag |

**VERDICT: PASS**

**Notes:**
- WARN on section-contents: Subsection-titles include "— Trailing 12 Months" suffix but section-contents omits this suffix for all 4 subsections. The section-contents names match the guide headings. This is a systematic pattern across all subsections, not a structural failure.
