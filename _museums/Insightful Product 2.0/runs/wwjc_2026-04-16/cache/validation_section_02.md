# Validation: §2 Sales Team Performance

| Check | Status | Evidence |
|-------|--------|----------|
| **A. Subsection Completeness** | | |
| Subsection 1: Rep Activity Ladder | PASS | `<div class="subsection-title">Rep Activity Ladder</div>` found (line 13) |
| Subsection 2: Behavioral Scorecard Spotlight | PASS | `<div class="subsection-title">Behavioral Scorecard Spotlight</div>` found (line 104); gate MIXPANEL_USER_DATA_PRESENT = true met |
| Subsection 3: Selling Archetypes | PASS | `<div class="subsection-title">Selling Archetypes</div>` found (line 138); gate MIXPANEL_USER_DATA_PRESENT = true met; QUALIFYING_REP_COUNT = 22 > 3 |
| Subsection 4: Coaching Opportunities | PASS | `<div class="subsection-title">Coaching Opportunities</div>` found (line 175); gate MIXPANEL_USER_DATA_PRESENT = true met |
| Subsection 5: Rep Engagement Trajectory | PASS | `<div class="subsection-title">Rep Engagement Trajectory</div>` found (line 244) |
| Subsection 6: Territory Coverage | PASS | `<div class="subsection-title">Territory Coverage</div>` found (line 292); territory data present in fragment |
| section-contents matches rendered subsections | PASS | "Rep Activity Ladder · Behavioral Scorecard Spotlight · Selling Archetypes · Coaching Opportunities · Rep Engagement Trajectory · Territory Coverage" — all 6 names present, middot-separated |
| **B. Fragment Contract** | | |
| Opens with `<details class="section-collapse" id="sales">` | PASS | Line 1; id="sales" matches §2 locked ID |
| Closes with `</details>`, nothing after | PASS | Line 381; no trailing content |
| No `<html>`, `<head>`, `<body>`, `<style>` | PASS | grep: zero matches |
| No HTML comments | PASS | grep for `<!--`: zero matches |
| section-sub is data-dense | PASS | "21 qualifying reps · 1 showroom excluded · $3.13M iPad GMV trailing 12 months · top rep drives 27% of volume" — specific stats, not generic |
| expand-hint span present | PASS | `<span class="expand-hint">&#9662; Click to expand</span>` found (line 8) |
| Inner `<section class="section">` wrapper | PASS | `<section class="section" style="margin-bottom:0;border-top:none;border-radius:0 0 var(--r) var(--r);">` found (line 10) |
| **C. Subsection Structure** | | |
| subsection-title is first child of every subsection | PASS | Verified for all 6 subsections (lines 12–13, 103–104, 137–138, 174–175, 243–244, 291–292) |
| what-this-means closes every subsection | PASS | `<div class="what-this-means">` found at end of all 6 subsections (lines 98, 132, 169, 238, 286, 375) |
| **D. Forbidden Phrases** | | |
| "health score" / "health scores" | PASS | zero matches |
| "portal orders" / "portal ordering" as buyer activity | PASS | zero matches (term absent entirely) |
| "net-new customers" | PASS | zero matches |
| "ERP" | PASS | zero matches |
| "Mixpanel" | PASS | zero matches; uses "Platform engagement data" instead (line 105) |
| "Clicky" | PASS | zero matches |
| "Platform-Embedded" / "Commerce-Active" / "Catalog-Focused" | PASS | zero matches |
| Internal identifiers (VM codes, query IDs, table names, column names, org IDs) | PASS | zero matches |
| "bounce_rate" | PASS | zero matches |
| `order_source = 'ipad'` / code literals | PASS | zero matches |
| "benchmark_confidence" / "peer_group_level" / "peer_group_n" | PASS | zero matches |
| **D. Hard-Rule Compliance** | | |
| HR7: Every metric includes time qualifier | PASS | "trailing 12 months" established in section-sub (line 5) and subsection prose (lines 14, 293); "trailing 180 days" / "current 90-day" / "prior 90-day" in trajectory (lines 245, 254); all metrics contextualized |
| HR8: Every projection tagged [HYPOTHETICAL] | PASS | 6 [HYPOTHETICAL] tags found — 5 coaching-impact values (lines 186, 198, 210, 222, 234) + 1 what-this-means rollup (line 239); no untagged quantified projections |
| HR9: Every extrapolation tagged [ESTIMATED] | PASS | no extrapolations present |
| HR2: VM-27/28/29/36/48 not surfaced | PASS | no VM codes in fragment |
| VM-38b not surfaced | PASS | no VM codes in fragment |
| HR4: portal_orders never framed as buyer self-service | PASS | term absent entirely |
| **E. Section-Specific Rendering** | | |
| Coaching Opportunities uses `.coaching-card` elements | PASS | 5 coaching-card elements (Whit Barnes, Mark Horne, Pam Cain, Ryan McWilliams, Janice Roetman); each uses coaching-header / coaching-name / coaching-body / coaching-action / coaching-impact classes |
| Selling Archetypes has 4-column table (Archetype / Rep(s) / Signature / Implication) | PASS | Table at line 141–142 with exact column headers: Archetype, Rep(s), Signature, Implication |
| Selling Archetypes includes archetype-as-coaching-tool callout | PASS | `.callout.insight` at line 165 with title "Archetypes Are Coaching Tools, Not Performance Labels" |
| Showroom exclusion reflected in section-sub | PASS | "1 showroom excluded" in section-sub; showroom account details in prose (line 14: "Atlanta Showroom — 25 orders, $28,111 GMV") |
| Coaching cards include gap location, quantified upside, recommended action | PASS | All 5 cards contain all 3 elements |
| Only archetypes with qualifying reps rendered | PASS | 3 archetypes rendered (Curated Discovery Seller: 8 reps, Volume Relationship Seller: 18 reps, Deep-Account Specialist: 9 reps) — all populated |
| Rep Activity Ladder built from qualifying reps (≥10 orders) | PASS | 21 reps in main table, 19 below threshold in collapsible `<details>` — matches 21 qualifying after 1 showroom exclusion |
| **F. Highlight File** | | |
| cache/section_02_highlights.md exists | PASS | file present |
| Contains 2–4 highlight candidates | PASS | 4 candidates (numbered 1–4) |
| Each has bold headline, context sentence, section link | PASS | All 4: **bold headline** — context with data — [→ §sales] |
| Priority action candidate format | PASS | 1 candidate with HIGH urgency, quantified impact [HYPOTHETICAL], section link |

**VERDICT: PASS**
