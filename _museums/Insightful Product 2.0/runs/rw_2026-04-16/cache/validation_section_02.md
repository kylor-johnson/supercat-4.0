# Validation: §2 Sales Team Performance

**Client**: RENWIL (rw) · **Run date**: 2026-04-16 · **Validator run**: 2026-04-17

| Check | Status | Evidence |
|-------|--------|----------|
| **A. Subsection Completeness** | | |
| Subsection 1: Rep Activity Ladder | PASS | `subsection-title` at line 13 |
| Subsection 2: Behavioral Scorecard Spotlight | PASS | `subsection-title` at line 137; gate MIXPANEL_USER_DATA_PRESENT = true |
| Subsection 3: Selling Archetypes | PASS | `subsection-title` at line 174; gate MIXPANEL_USER_DATA_PRESENT = true |
| Subsection 4: Coaching Opportunities | PASS | `subsection-title` at line 217; gate MIXPANEL_USER_DATA_PRESENT = true |
| Subsection 5: Rep Engagement Trajectory | PASS | `subsection-title` at line 286 |
| Subsection 6: Territory Coverage | PASS | `subsection-title` at line 333 |
| section-contents lists all 6 | PASS | Line 6: all 6 names present with `&middot;` separators |
| **B. Fragment Contract** | | |
| Opens with `<details class="section-collapse" id="sales">` | PASS | Line 1 |
| Closes with `</details>` — nothing after | PASS | Line 429 — final line of file |
| No `<html>`, `<head>`, `<body>`, `<style>` tags | PASS | Zero matches (grep) |
| No HTML comments (`<!-- -->`) | PASS | Zero matches (grep) |
| `section-sub` is data-dense | PASS | Line 5: "44 qualifying reps · 1 showroom excluded · $9.5M iPad GMV trailing 12 months · top rep drives 13% of volume" |
| `expand-hint` present | PASS | Line 8: `<span class="expand-hint">&#9662; Click to expand</span>` |
| Inner `<section class="section" ...>` wrapper | PASS | Line 10: `<section class="section" style="margin-bottom:0;border-top:none;border-radius:0 0 var(--r) var(--r);">` |
| **C. Subsection Structure** | | |
| Every subsection has `subsection-title` as first child | PASS | 6 subsection divs each immediately followed by subsection-title (lines 12→13, 136→137, 173→174, 216→217, 285→286, 332→333) |
| Every subsection ends with `what-this-means` | PASS | 6 what-this-means divs found (lines 131, 168, 211, 280, 327, 423) — one per subsection |
| **D. Forbidden Phrases & Hard Rules** | | |
| Forbidden: "health score" / "health scores" | PASS | Zero matches |
| Forbidden: "portal orders" / "portal ordering" | PASS | Zero matches |
| Forbidden: "net-new customers" | PASS | Zero matches |
| Forbidden: "ERP" | PASS | Zero matches |
| Forbidden: "Mixpanel" | PASS | Zero matches — uses "platform engagement data" |
| Forbidden: "Clicky" | PASS | Zero matches |
| Forbidden: "Platform-Embedded" / "Commerce-Active" / "Catalog-Focused" | PASS | Zero matches |
| Forbidden: VM codes, query IDs, table names, column names, org IDs | PASS | Zero matches |
| Forbidden: "bounce_rate" | PASS | Zero matches |
| Forbidden: `order_source` code literals | PASS | Zero matches |
| Forbidden: "benchmark_confidence" / "peer_group_level" / "peer_group_n" | PASS | Zero matches |
| HR7: Metrics include time qualifiers | PASS | section-sub and leading prose establish "trailing 12 months"; individual metric cards carry qualifiers (e.g., "≥10 iPad orders, trailing 12 months"); trajectory subsection uses "current 90-day window vs. prior 90-day window" |
| HR8: Projections tagged [HYPOTHETICAL] | PASS | 7 instances found — all coaching-impact values and Territory what-this-means projection carry the tag |
| HR9: Extrapolations tagged [ESTIMATED] | PASS | No extrapolations present; no untagged estimates found |
| HR2: VM-27, VM-28, VM-29, VM-36, VM-48 not surfaced | PASS | Zero matches for any VM code |
| HR4: portal_orders not framed as buyer activity | PASS | portal_orders not referenced in fragment |
| **E. Section-Specific Rendering** | | |
| Coaching Opportunities uses `.coaching-card` elements | PASS | 5 coaching-card divs found (lines 220, 232, 244, 256, 268) — not bare prose |
| Selling Archetypes table has 4 columns | PASS | Line 178: `Archetype / Rep(s) / Signature / Implication` — exact match |
| Showroom exclusion documented | PASS | section-sub (line 5): "1 showroom excluded"; prose (line 14): "One operational account (Test Sales Portal — 1 order, $313 GMV) was excluded" |
| Archetype coaching-tool callout present | PASS | Lines 207–209: callout insight titled "Archetypes Are Coaching Tools, Not Performance Labels" with style-specific coaching guidance |
| **F. Highlight File** | | |
| Highlight file exists | PASS | `cache/section_02_highlights.md` present |
| 2–4 candidates | PASS | 4 candidates |
| Each has bold headline + context + section link | PASS | All 4 follow format: `**bold** — context [→ §sales]` |
| Priority action candidate | PASS | 1 candidate with `**HIGH**` urgency, quantified signal (94% order collapse, $7,117 AOV), and section link |

**VERDICT: PASS**
