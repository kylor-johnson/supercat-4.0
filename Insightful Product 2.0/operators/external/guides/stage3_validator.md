# Stage 3: Fragment Validation
> **v1.0** — validated 2026-04-17 (RENWIL run). Last updated: 2026-04-17.

## 1. Read Chain

1. Read `shared_rules.md`
2. Read the assigned `section_NN_*.md` guide for this section
3. Read `fragments/section_NN.html`
4. Read `cache/gate_flags.md` for conditional subsection gates
5. Do NOT read query cache files — validators check structure, not data accuracy

## 2. Validation Checks

### A. Subsection Completeness
- For every subsection in the section guide whose gate is met (per `gate_flags.md`): confirm a `<div class="subsection">` with matching `<div class="subsection-title">` exists
- Confirm `section-contents` in `<summary>` lists all rendered subsections by name, separated by ` · `

### B. Fragment Contract Compliance
- Fragment opens with `<details class="section-collapse" id="{{CORRECT_ID}}">` and closes with `</details>` — nothing before or after
- No `<html>`, `<head>`, `<body>`, or `<style>` tags
- No HTML comments (`<!-- -->`)
- `section-sub` is present and is a data-dense stat line, not a generic description
- `expand-hint` span is present
- Inner `<section class="section" ...>` wrapper is present

### C. Subsection Structure
- Every `<div class="subsection">` has `<div class="subsection-title">` as first child
- Every subsection ends with `<div class="what-this-means">` (exception: §2.4 Coaching Opportunities — omits what-this-means per shared_rules.md Section D)

### D. Forbidden Phrases & Hard-Rule Compliance
Scan the full fragment for every phrase in shared_rules.md Section C. Each phrase is a separate check row.

Also verify these per-section rules from shared_rules.md Section B and the v2 operator Pre-Flight:
- Every metric includes a time qualifier (Hard Rule 7)
- Hard Rule 8 (projections): Two sub-checks:
  - (a) **Fragment**: The literal string `[HYPOTHETICAL]` must NOT appear anywhere in the HTML fragment. If found, **FAIL** — it is a rendering defect.
  - (b) **Fragment**: Projections (forward-looking estimates, "what if" scenarios, potential impact statements) use hedging language ("potential," "estimated," "projected," "roughly," "could," "up to"). Spot-check at least 3 projection statements if present.
- Hard Rule 9 (extrapolations): Same two sub-checks as Hard Rule 8, but for `[ESTIMATED]`.
- VM-27, VM-28, VM-29, VM-36, VM-48 content not surfaced (Hard Rule 2)
- VM-38b not surfaced (pending_engineering)
- `portal_orders` is never framed as buyer self-service activity (Hard Rule 4)

### E. Section-Specific Rendering Checks
Read the assigned section guide and verify each explicit rendering requirement. The validator extracts checks dynamically from whatever guide it receives — it does not hardcode them. Examples for illustration:
- §2: Coaching Opportunities uses `.coaching-card` elements, not bare prose
- §2: Every `.coaching-impact` element uses hedging language (e.g., "potential") and does NOT contain the literal string `[HYPOTHETICAL]`
- §2: Selling Archetypes has a 4-column table (Archetype / Reps / Signature / Implication)
- §5: VM-45 capture rate subsection present only if `VM45_RENDER = true` in gate_flags
- §7: `operational_health_score` row uses `peer-metric-title` = "Data & Operational Health"
- §7: No confidence labels, tier labels, or raw `peer_group_n` counts — plain-language framing only
- §7: Feature adoption table has exactly 3 columns
- §8: Freshness labels are only Fresh / Monitor / Stale — no 5-label system

### E2. Table Display Limit Checks
- If any table in the fragment has more than 15 visible rows: **FAIL**. The section guide or shared_rules.md Section H caps displayed rows at 15.
- If any table has more than 5 visible rows without a collapsed `<details>` overflow element nearby: **WARN**. Default visible is 5; overflow should be wrapped in progressive disclosure.

### E3. Progressive Disclosure Compliance
- For each subsection tagged `[COLLAPSE]` in the section guide: verify the fragment wraps that subsection's content in an inner `<details>` element (inside the outer `<details class="section-collapse">`). The inner `<details>` should contain a `<summary>` with the subsection title and collapse/expand affordance. If a `[COLLAPSE]`-tagged subsection is rendered without an inner `<details>`: **FAIL**.

### F. Highlight File Check
- Confirm `cache/section_NN_highlights.md` exists and contains 2–4 highlight candidates
- Each highlight has: **bold headline**, context sentence, section link
- If a priority action candidate contains a projection, it should carry the `[HYPOTHETICAL]` tag (this is correct for internal cache files — the tag belongs here, not in HTML fragments)

## 3. Output Format

Write to `cache/validation_section_NN.md`:

```markdown
# Validation: §N Section Title

| Check | Status | Evidence |
|-------|--------|----------|
| Subsection 1: Name | PASS | subsection-title found |
| Rendering: specific check | PASS | element/pattern found |
| Forbidden: "phrase" | PASS | zero matches |
| Fragment contract | PASS | correct id, opens/closes correctly |
| what-this-means closes | PASS | found for all N subsections |
| Highlight file | PASS | 3 candidates, format correct |

**VERDICT: PASS**
```

VERDICT: **PASS** if all checks pass. **FAIL** if any check fails. **WARN** items do not trigger FAIL but are reported for human review.

**Note on Hard Rule 7 (time qualifiers):** Presence of a time qualifier is machine-checkable; semantic accuracy (e.g., "trailing 12 months" applied to a metric that actually covers a different window) requires human review. Mark as PASS if a qualifier is present, and add a note if the qualifier's accuracy cannot be mechanically confirmed.

## 4. Aggregation Step

After all per-section validators complete, a follow-up agent:
1. Reads all `cache/validation_section_NN.md` files
2. Concatenates into `cache/validation_checklist.md` using the aggregated format from ARCHITECTURE.md §8 — summary table at top, then per-section detail below
3. No synthesis, no interpretation — mechanical concatenation with a summary table
4. If any section has FAIL verdict, add a "Re-dispatch Required" block listing the failures

## 5. Re-dispatch Instructions

If a section FAILs:
1. **Full regeneration, not targeted edit.** The section agent receives:
   - `shared_rules.md` + `section_NN_*.md` (the full section guide)
   - Relevant `cache/Q-*_results.md` files
   - A failure note stating what was missing or wrong
   - The agent does NOT receive its previous fragment — it regenerates from scratch
2. **Max 2 re-dispatches per section.** After 2 failures, flag for human review — the issue is likely a guide deficiency or data gap, not an agent execution failure.
3. **Re-validate after each regeneration.** The same validator runs again on the new fragment.
