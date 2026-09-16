# Validation Checklist — RENWIL (rw) — 2026-04-17

| § | Section | Verdict | Fails | Warns | Notes |
|---|---------|---------|-------|-------|-------|
| 2 | Sales Team Performance | PASS | 0 | 1 | Run A; HR8 re-checked post-patch (see footnote¹) |
| 3 | Customer & Buyer Intelligence | PASS | 0 | 0 | Re-validated (Run B); both prior defects resolved |
| 4 | Product & Inventory Intelligence | PASS | 0 | 0 | Run A |
| 5 | Commerce Analytics | PASS | 0 | 1 | Run A |
| 6 | Portal Engagement | PASS | 0 | 1 | Run B |
| 7 | Peer Benchmarking | FAIL | 1 | 0 | Run B; section ID mismatch |
| 8 | Platform & Feature Utilization | PASS | 0 | 0 | Run B |

**OVERALL: FAIL**

**¹ §2 Hard Rule 8 post-patch note:** Run A's `validation_section_02.md` contains checks E2 and F2 marked as PASS for "Every `.coaching-impact` contains `[HYPOTHETICAL]`." Under the updated rules (shared_rules.md Hard Rule 8, updated after Run A), the literal `[HYPOTHETICAL]` tag is an **internal pipeline marker** that must NEVER appear in HTML fragments — projections must use hedging language instead. The §2 fragment has since been patched to remove literal `[HYPOTHETICAL]` tags per the updated rules. The Run A PASS verdicts for E2/F2 were correct under the prior rule version but are now stale. The patched fragment is compliant with the current rules.

---

## Re-dispatch Required

**§7 Peer Benchmarking** — 1 FAIL

| Check | Status | Evidence |
|-------|--------|----------|
| B1: Opens with correct `<details>` tag | FAIL | Fragment uses `id="peer-benchmarking"` but `shared_rules.md` locked section ID is `peer` and `section_07_peer.md` specifies `id: peer`. This will break anchor links from the Executive Summary and cross-section references targeting `#peer`. |

**Action**: Re-dispatch §7 section agent with failure note: "Fragment must use `id=\"peer\"` per the locked section IDs in `shared_rules.md` Section E. The current `id=\"peer-benchmarking\"` violates the contract. All other checks pass — regeneration should preserve current content structure while correcting the ID."

---

## Per-Section Validation Detail

---

# Validation: §2 Sales Team Performance

| Check | Status | Evidence |
|-------|--------|----------|
| A: Subsection 1 — Rep Activity Ladder | PASS | `<div class="subsection-title">Rep Activity Ladder</div>` present (line 13) |
| A: Subsection 2 — Behavioral Scorecard | WARN | Guide heading is "Behavioral Scorecard Spotlight"; fragment renders "Behavioral Scorecard" (line 80). Content matches; name omits "Spotlight" |
| A: Subsection 3 — Selling Archetypes | PASS | `<div class="subsection-title">Selling Archetypes</div>` present (line 106) |
| A: Subsection 4 — Coaching Opportunities | PASS | `<div class="subsection-title">Coaching Opportunities</div>` present (line 150) |
| A: Subsection 5 — Rep Engagement Trajectory | PASS | `<div class="subsection-title">Rep Engagement Trajectory</div>` present (line 202) |
| A: Subsection 6 — Territory Coverage | PASS | `<div class="subsection-title">Territory Coverage</div>` present (line 247) |
| A: section-contents middot list | PASS | Lists all 6 rendered subsections separated by `&middot;` (line 6) |
| B1: Opens with correct `<details>` | PASS | Line 1: `<details class="section-collapse" id="sales">` — correct ID |
| B2: Closes with `</details>` | PASS | Line 283: `</details>` — nothing after |
| B3: No `<html>/<head>/<body>/<style>` tags | PASS | Grep confirms zero matches |
| B4: No HTML comments | PASS | Grep confirms zero `<!-- -->` matches |
| B5: `section-sub` present with data-dense stat line | PASS | Line 5: "63 reps · 1 test account excluded · $9.50M iPad GMV · $1,236 AOV trailing 12 months" |
| B6: `expand-hint` span present | PASS | Line 8: `<span class="expand-hint">&#9662; Click to expand</span>` |
| B7: Inner `<section class="section">` wrapper present | PASS | Line 10: `<section class="section" style="margin-bottom:0;border-top:none;border-radius:0 0 var(--r) var(--r);">` |
| C1: Every subsection has `subsection-title` as first child | PASS | All 6 subsections open with `<div class="subsection-title">` immediately after `<div class="subsection">` |
| C2: Every subsection ends with `what-this-means` (except §2.4) | PASS | Subsections 1, 2, 3, 5, 6 end with `<div class="what-this-means">`. Subsection 4 (Coaching Opportunities) correctly omits per shared_rules.md Section D |
| D1: Forbidden — "health score/scores" | PASS | Zero matches |
| D2: Forbidden — "portal orders/ordering" | PASS | Zero matches |
| D3: Forbidden — "net-new customers" | PASS | Zero matches |
| D4: Forbidden — "ERP" | PASS | Zero matches |
| D5: Forbidden — "Mixpanel" | PASS | Zero matches; uses "Platform engagement data" instead |
| D6: Forbidden — "Clicky" | PASS | Zero matches |
| D7: Forbidden — "Platform-Embedded" | PASS | Zero matches |
| D8: Forbidden — "Commerce-Active" | PASS | Zero matches |
| D9: Forbidden — "Catalog-Focused" | PASS | Zero matches |
| D10: Forbidden — VM codes / query IDs | PASS | Zero matches for VM-\d+ or Q-\d+ patterns |
| D11: Forbidden — table names, column names, org IDs, dataset paths | PASS | Zero matches for org_id, internal identifiers |
| D12: Forbidden — "bounce_rate" | PASS | Zero matches |
| D13: Forbidden — code literals (`order_source = 'ipad'`) | PASS | Zero matches for `order_source` |
| D14: Forbidden — "benchmark_confidence" | PASS | Zero matches |
| D15: Forbidden — "peer_group_level" | PASS | Zero matches |
| D16: Forbidden — "peer_group_n" | PASS | Zero matches |
| E1: Hard Rule 7 — time qualifiers on metrics | PASS | All metrics include "trailing 12 months" or "trailing 90 days." Semantic accuracy of time windows not mechanically confirmable |
| E2: Hard Rule 8 — projections tagged [HYPOTHETICAL] | PASS | All 4 coaching-impact elements contain [HYPOTHETICAL] (lines 159, 171, 183, 196) |
| E3: Hard Rule 9 — extrapolations tagged [ESTIMATED] | PASS | No extrapolations present; N/A |
| E4: Hard Rule 2 — VM-27/28/29/36/48 not surfaced | PASS | Zero matches for VM-\d+ pattern |
| E5: Hard Rule 4 — portal_orders not framed as buyer activity | PASS | Term absent from fragment; N/A |
| E6: VM-38b not surfaced | PASS | Zero matches |
| F1: `.coaching-card` elements for Coaching Opportunities | PASS | 4 coaching cards rendered with proper `.coaching-card`/`.coaching-header`/`.coaching-name`/`.coaching-body`/`.coaching-action`/`.coaching-impact` structure (lines 151–198) |
| F2: Every `.coaching-impact` contains [HYPOTHETICAL] | PASS | All 4 coaching-impact elements contain [HYPOTHETICAL] |
| F3: Selling Archetypes table — 4 columns | PASS | `<th>Archetype</th><th>Rep(s)</th><th>Signature</th><th>Implication</th>` (line 110) |
| F4: Archetype insight callout present | PASS | `<div class="callout insight">` with coaching-tools-not-labels explanation (lines 139–142) |
| F5: Coaching subsection omits what-this-means | PASS | Subsection 4 ends at line 199 with no what-this-means block |
| F6: Rep Activity Ladder shows top 10 + overflow in `<details>` | PASS | 10 visible rows (lines 42–52); `<details>` overflow for rows 11–20 (lines 54–73) |
| F7: Rep Engagement Trajectory — top 5 accelerating + bottom 5 declining | PASS | 5 accelerating rows (lines 213–217); 5 declining rows (lines 228–232) |
| F8: Territory Coverage — top 10 territories | PASS | 10 territory rows (lines 257–267); guide specifies "Show top 10" — guide-specific limit takes precedence |
| F9: section-sub references exclusion count | PASS | "1 test account excluded" in section-sub; no methodology disclosed |
| F10: No threshold explanations or pipeline context in prose | PASS | No mention of qualifying threshold (≥10 orders), methodology, or internal pipeline context |
| G: Table display — max 15 rows per table | PASS | Largest visible table: 10 rows (Rep Activity Ladder, Territory Coverage). All under 15 |
| G: Table display — >5 visible rows without `<details>` overflow | PASS | Rep Activity Ladder: 10 visible, guide explicitly says "Show top 10 visible" — guide takes precedence. Territory Coverage: 10 rows inside subsection-level `<details>` [COLLAPSE]; guide says "Show top 10" |
| H: Progressive disclosure — Subsection 5 [COLLAPSE] | PASS | Rep Engagement Trajectory content wrapped in inner `<details>` (line 203) |
| H: Progressive disclosure — Subsection 6 [COLLAPSE] | PASS | Territory Coverage content wrapped in inner `<details>` (line 248) |
| I: Highlight file exists | PASS | `cache/section_02_highlights.md` present |
| I: Highlight count 2–4 | PASS | 4 highlight candidates |
| I: Highlight format | PASS | Each has **bold headline**, context sentence, section link `[→ §sales]` |
| I: Priority action candidate | PASS | 1 priority action with urgency level "HIGH" and [HYPOTHETICAL] tag |

**VERDICT: PASS**

**Notes:**
- WARN on subsection 2 naming: guide says "Behavioral Scorecard Spotlight" but fragment renders "Behavioral Scorecard." Content is correct; name is abbreviated. Not a structural failure.

---

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

---

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

---

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

---

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

---

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

---

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
