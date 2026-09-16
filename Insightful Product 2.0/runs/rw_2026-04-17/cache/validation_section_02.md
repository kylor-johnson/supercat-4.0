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
