# Validation: §4 Product & Inventory Intelligence

| Check | Status | Evidence |
|-------|--------|----------|
| A: Subsection 1 — Top Sellers OOS | PASS | Correctly absent; gate requires HAS_SALES_DATA=true AND HAS_INVENTORY=true; HAS_SALES_DATA=false |
| A: Subsection 2 — New Introduction Performance | PASS | Correctly absent; gate requires HAS_SALES_DATA=true; HAS_SALES_DATA=false |
| A: Subsection 3 — Product Velocity Trend | PASS | Correctly absent; gate requires HAS_PORTAL_ORDERS=true; HAS_PORTAL_ORDERS=false |
| A: Subsection 4 — Catalog Completeness | PASS | `<div class="subsection-title">Catalog Completeness</div>` present (line 12); gate is "Always" |
| A: Subsection 5 — What's Selling | PASS | Correctly absent; gate requires HAS_SALES_DATA=true; HAS_SALES_DATA=false |
| A: section-contents middot list | PASS | Lists "Catalog Completeness" — the only rendered subsection (line 6) |
| B1: Opens with correct `<details>` | PASS | Line 1: `<details class="section-collapse" id="product">` — correct ID |
| B2: Closes with `</details>` | PASS | Line 43: `</details>` — nothing after |
| B3: No `<html>/<head>/<body>/<style>` tags | PASS | Grep confirms zero matches |
| B4: No HTML comments | PASS | Grep confirms zero `<!-- -->` matches |
| B5: `section-sub` present with data-dense stat line | PASS | Line 5: "1,812 visible products · 99.9% catalog completeness · 1 missing image" |
| B6: `expand-hint` span present | PASS | Line 8: `<span class="expand-hint">&#9662; Click to expand</span>` |
| B7: Inner `<section class="section">` wrapper present | PASS | Line 10: `<section class="section" style="margin-bottom:0;border-top:none;border-radius:0 0 var(--r) var(--r);">` |
| C1: Every subsection has `subsection-title` as first child | PASS | Catalog Completeness subsection opens with `<div class="subsection-title">` (line 12) |
| C2: Every subsection ends with `what-this-means` | PASS | Catalog Completeness ends with `<div class="what-this-means">` (line 38) |
| D1: Forbidden — "health score/scores" | PASS | Zero matches |
| D2: Forbidden — "portal orders/ordering" | PASS | Zero matches |
| D3: Forbidden — "net-new customers" | PASS | Zero matches |
| D4: Forbidden — "ERP" | PASS | Zero matches |
| D5: Forbidden — "Mixpanel" | PASS | Zero matches |
| D6: Forbidden — "Clicky" | PASS | Zero matches |
| D7: Forbidden — "Platform-Embedded" | PASS | Zero matches |
| D8: Forbidden — "Commerce-Active" | PASS | Zero matches |
| D9: Forbidden — "Catalog-Focused" | PASS | Zero matches |
| D10: Forbidden — VM codes / query IDs | PASS | Zero matches |
| D11: Forbidden — table names, column names, org IDs, dataset paths | PASS | Zero matches |
| D12: Forbidden — "bounce_rate" | PASS | Zero matches |
| D13: Forbidden — code literals | PASS | Zero matches |
| D14: Forbidden — "benchmark_confidence" | PASS | Zero matches |
| D15: Forbidden — "peer_group_level" | PASS | Zero matches |
| D16: Forbidden — "peer_group_n" | PASS | Zero matches |
| E1: Hard Rule 7 — time qualifiers on metrics | PASS | Prose qualifies as "Current snapshot ... as of April 2026" (line 13); callout repeats "as of April 2026" (line 36). Catalog completeness is a point-in-time snapshot; qualifier is present |
| E2: Hard Rule 8 — projections tagged [HYPOTHETICAL] | PASS | No projections present. "Resolving that single gap would bring the catalog to 100%" is direct arithmetic (1/1,812), not a statistical projection |
| E3: Hard Rule 9 — extrapolations tagged [ESTIMATED] | PASS | No extrapolations present; N/A |
| E4: Hard Rule 2 — VM-27/28/29/36/48 not surfaced | PASS | Zero matches |
| E5: Hard Rule 4 — portal_orders not framed as buyer activity | PASS | Term absent; N/A |
| E6: VM-38b not surfaced | PASS | Correctly absent; pending_engineering per section guide |
| F1: Catalog Completeness table — correct 5 columns | PASS | Visibility / Products / Missing Images / Missing Price / Complete % (lines 17–21) |
| F2: Subsections 1–3 and 5 absent (gated out) | PASS | Only Catalog Completeness rendered; HAS_SALES_DATA=false and HAS_PORTAL_ORDERS=false correctly gate out subsections 1, 2, 3, 5 |
| F3: VM-38b not attempted | PASS | No product velocity subsection rendered; section guide rule respected |
| G: Table display — max 15 rows per table | PASS | Catalog completeness table has 1 row |
| G: Table display — >5 visible rows without `<details>` | PASS | Only table has 1 row |
| H: Progressive disclosure | PASS | No [COLLAPSE]-tagged subsections rendered; N/A |
| I: Highlight file exists | PASS | `cache/section_04_highlights.md` present |
| I: Highlight count 2–4 | PASS | 2 highlight candidates |
| I: Highlight format | PASS | Each has **bold headline**, context sentence, section link `[→ §product]` |
| I: Priority action candidate | PASS | 1 priority action with urgency "LOW" |

**VERDICT: PASS**
