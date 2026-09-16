# Section Guide: §1 — Executive Summary
> **v1.0** — validated 2026-04-17 (RENWIL run). Last updated: 2026-04-17.

## Section Identity
- **id**: `executive-summary`
- **title**: Executive Summary
- **section number**: 1
- **structure**: `<section id="executive-summary">` — NOT `<details class="section-collapse">`
- **built by**: Stage 4 assembler (not a Stage 2 section agent)

## Rendering Rules

The Executive Summary is built by the Stage 4 assembler AFTER all section fragments are complete. It is NOT a section agent deliverable.

### Highlights
- `<ul class="highlights">` as the FIRST element after the section heading — NO prose before it
- 5–6 `<li>` items selected from `cache/section_NN_highlights.md` candidates
- Each: bold headline, one sentence of context, cross-link `<a href="#section-id">→ Section Name</a>`
- At least one positive finding; at least one recommended action

### Priority Actions
- `.priorities` > `.priority` cards, 2–4 items, highest urgency first
- Badge text: "High" / "Medium" / "Low" (matching `.priority-badge.high` / `.medium` / `.low`)
- Each card includes section cross-link in title
- Impact projections use hedging language ("potential," "could," "estimated") — literal `[HYPOTHETICAL]` tags must NOT appear in the HTML (see shared_rules.md Hard Rule 8)
- Wrap lower-priority actions in a collapsed `<details>` block

### Forbidden in Executive Summary
- Any `<p class="prose">` before the highlights list
- Narrative paragraphs or orientation sentences above the numbered list
- Generic "action box" or `<div class="callout info"><ol>` replacing Priority Actions
