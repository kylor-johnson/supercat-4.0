# Output Contract

This file defines what the agent emits — the phase-assignment algorithm, the per-client output structure, the cohort-level output, the deliberate non-goals, and the run-mechanics summary. See `Phase_Anchors.md` for the phase definitions and `Flags_and_Signals.md` for the flag taxonomy that gets surfaced inside the output.

## Phase assignment algorithm

For each client:

1. Evaluate phases 1 → 7 in order.
2. **Anchor phase** = the highest phase N such that **every** phase ≤ N has its `Done when` clause passing — i.e. the last *fully-Done* phase, evaluated contiguously. A failed lower phase blocks every higher phase, even when a higher phase's own `Done when` would pass in isolation. (This is what prevents a price-unconfirmed org from skipping a failed Phase 3 into Phase 4; it also matches the "last fully-Done" language below.)
3. **Current phase** = `Anchor phase + 1`, capped at 7. (If anchor = 7, client is Live and exits.)
4. **Open workstreams** = any phase ≤ Anchor whose health metrics show incomplete or degraded items (not gating, but called out in narrative). Out-of-order signals (e.g. Phase 6 qual fired while Phase 5 not yet done) are noted in the narrative — the algorithm itself generates this as automatic text and no longer requires a `PHASE_SKIP_OBSERVED` flag.
5. **Ambiguity flags** = the contradiction patterns enumerated in `Flags_and_Signals.md § Ambiguity flags (the standup agenda)`.
6. **Integration workstream** is computed independently per `Phase_Anchors.md § Integration Workstream (parallel)` and reported alongside Anchor/Current. It does NOT participate in phase advancement.

Phases are NOT strictly sequential in completion. A client can have Phase 6 qualitative anchor fired (Kyla intro email) while Phase 5 reps haven't logged in yet. In that case the Anchor is still Phase 4 (last fully-Done), Current = Phase 5, but Phase 6 qual signal is surfaced in the narrative as an out-of-order observation. The linear-ladder fiction is what the v2 framework apologized for — we just bake the non-linearity into the output.

## Per-client output structure

Write this for a sales/ops reader who has never read this framework. Plain English, substance over jargon (see `## Voice & readability (every run)` below — it is binding). Reproduce these sections per client, sorted by Anchor phase ascending.

```
## {SHORTNAME} ({Company Name})

**Phase {N} of 7 — {Phase Name}** · working on **{Phase N+1 Name}** · {product, e.g. eCat iPad}
**In onboarding {days} days** · {plain engagement, e.g. "Talking regularly (mostly email)" / "Quiet for 2+ weeks"}

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 / 🟡 / ⚪ | {one plain sentence} |
| 2 · First import | 🟢 / 🟡 / ⚪ | {one plain sentence} |
| 3 · Building the catalog | 🟢 / 🟡 / ⚪ | {one plain sentence} |
| 4 · Catalog ready | 🟢 / 🟡 / ⚪ | {one plain sentence} |
| 5 · Reps using the iPad | 🟢 / 🟡 / ⚪ | {one plain sentence} |
| 6 · Admin trained | 🟢 / 🟡 / ⚪ | {one plain sentence} |
| 7 · Live | 🟢 / ⚪ | {one plain sentence} |
| Integration | 🟢 / 🟡 / ⚪ | {ONLY shown when SuperCat owns the integration — see "Integration: when to show it" below} |

Status key: 🟢 done · 🟡 in progress / partial · ⚪ not started. (These map to the internal ✅/🟡/⚪ phase states; render as colored dots.)

### Next step
{One plain sentence — the single most important thing that has to happen next, in language a sales manager can act on. If a flag is blocking, the next step is to resolve that flag.}

### Things to flag ({count})

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| {step} | {plain-English issue title} | {Fathom date / Help Scout #N / database} | "{verbatim quote}" or {plain metric} |

(Omit this whole section when there are no flags. The Issue is a plain-English title ONLY — do NOT print the internal flag code here, not even in parentheses. If we need the code for cross-referencing, it lives in the appendix flag-reference map, not in this table.)

### Recent activity
- **Meetings:** {N in last 90 days} — last was "{title}" on {date}
- **Support:** {N email threads, M still open} — last reply {date}
- **Imports:** {plain tally, e.g. "Products and customers loaded in the last month"}

### Bottom line
{2–3 plain sentences a manager could read aloud at standup. No internal vocabulary.}
```

### Integration: when to show it

The Integration row/section is driven by what the client actually bought, read from the HubSpot deal line items (`Phase_Anchors.md § Integration Workstream (parallel)` is the authoritative source). Three cases:

- **SuperCat owns it (a "Managed Integration" line item is on the deal):** show the Integration row and a short Integration block. This is our build to track.
- **Client owns it (a "Certified Pipeline" line item is on the deal):** mention it in one informational line ("Client is building their own integration; we certify it") — do NOT show it as an open SuperCat workstream and do NOT raise an ownership flag.
- **No integration line item (self-serve FTP / none):** omit the Integration row and the Integration block entirely. There is nothing for us to track, so it must not appear on the standup.

## Cohort-level output (top of file)

The top of the file is the at-a-glance standup view. Keep it in plain language — no run metadata, no framework internals (those go in the appendix; see `## Appendix: run metadata & framework feedback` below).

```
# {Month D, YYYY} — Onboarding Phase Assessment

## Where everyone is

| Client | Phase (of 7) | Working on | Days in onboarding | Integration | One thing to resolve |
|---|---|---|---|---|---|
{One row per client. "Phase (of 7)" = Anchor as "N — Name". "Integration" column = "Us (Managed)" / "Them (Certified)" / "—" (none), per the HubSpot deal line items. "One thing to resolve" = the single most important plain-English item.}

## Standup agenda

**Each client appears under exactly one bucket — its single most urgent state.** Pick the highest-severity bucket the client qualifies for (Resolve > Discuss > On track) and list it there only. Do not repeat a client across buckets. An informational/by-design note is not a reason to also list an otherwise-on-track client under Discuss — fold that note into its "On track" line instead.

### 🔴 Resolve this week
{Things blocking a client from moving to the next phase. Plain titles, one line each, name the client.}

### ⚠️ Discuss / decide
{Judgment calls — thresholds, who owns a piece of work, an integration question on a client we own. Only list a client here if it has a genuine open judgment call; a confirmed by-design note alone does NOT belong here.}

### ✅ On track (nothing to resolve)
{Clients with no blocking issues. By-design or informational notes (e.g. "single net price — confirmed", "no product options — by design") do NOT keep a client out of this bucket; only blocking/actionable issues do — append the note to the client's line here rather than listing it under Discuss. A drift/data-mismatch flag stays actionable even when the run judges it a likely false alarm — put it under "Discuss / decide," not here. See `Flags_and_Signals.md § Actionable vs informational`.}
```

## Voice & readability (every run)

The deliverable is read at a sales/ops standup, not by the people who wrote this framework. Every run must follow these rules. They exist because a fresh LLM re-writes the prose each week and will default to internal jargon unless constrained.

**Write for someone who has never read this framework.** If a sentence only makes sense to someone who knows the anchor algorithm, rewrite it.

**Banned words in the client-facing body** (use them only in the appendix, if at all): `anchor`, `Current` (as a phase noun), `Done-when`, `clause`, `vacuous`, `fallback`, `regex`, `primitive`, `disjunctive`, `out-of-order`, `step-4`, `tier` (when you mean error-severity), `DPC`. Translate them:
- "Anchor / Current phase" → "Phase N of 7 — working on {next}".
- "Phase 4 Done-when fails on customers=0 (vacuous-pass blocked)" → "Catalog's built, but no customers are loaded yet — that's the one thing left."
- "DPC resolves 389/389" → "every customer is matched to a price list."
- "single price level, SINGLE_PRICE_LEVEL_UNCONFIRMED" → "they use one net price (confirmed as intentional)".

**Expand every acronym on first use** in a client's section: DefaultPriceCode, not DPC; "false alarm," not FP; "database lock," not PG deadlock.

**Never print an internal flag code in the client-facing body — not even in parentheses.** Every flag gets a plain-English title (e.g. "No customers loaded yet", "Customer import failing on price codes"). The internal codes (`PHASE_4_VACUOUS_NO_CUSTOMERS`, etc.) are constants for *us* — they belong only in the appendix flag-reference map, never in the cohort table, the per-client tables, or the prose.

**One sentence per evidence cell.** If it needs two clauses joined by "→", split or simplify.

**Numbers carry their meaning.** Not "70.4% (1,180/1,676)" alone — "70% of products have a photo (1,180 of 1,676)".

**Verbatim quotes stay verbatim** (`Flags_and_Signals.md § Hard rules`). Plain-language rewriting applies to *our* narration, never to a quoted customer/Fathom line.

> **`_html` field escaping:** Use actual UTF-8 characters for all typographic marks — `'` (curly apostrophe), `"` `"` (curly quotes), `—` (em dash), `→` (arrow), etc. Do NOT use HTML entity names like `&rsquo;` or `&mdash;`. The only escaping needed is literal `&` → `&amp;` when the ampersand is part of prose (e.g., "Lib & Co" → `Lib &amp; Co`). HTML tags in `_html` fields (`<code>`, `<span>`, `<blockquote>`) are trusted and inserted verbatim.

## What this framework deliberately does NOT do

- Does not predict go-live dates. Anchor + Current tells you where, not when.
- Does not score "health" of post-live clients. Phase 7 is terminal.
- Does not auto-resolve ambiguity flags. That's the standup's job.
- Does not assume linear progression. Out-of-order signals are surfaced, not smoothed.
- Does not predict integration completion. The integration workstream may finish before, during, or after phase progression.

## Run mechanics

- `RUN_PROMPT.md` orchestrates: auto-cohort detection → phase assignment per client → integration workstream lookup → ambiguity flag emission → output assembly.
- Output: `output/{YYYY-MM-DD}-phase-assessment.md`. The dated markdown is the deliverable.
- Phase 7 clients are dropped from the next run's cohort. Operations / health surveillance picks them up downstream.

## Appendix: run metadata & framework feedback

Provenance, plumbing status, and framework feedback are useful to us but are noise on a standup. Keep them OUT of the top of the file and OUT of the per-client sections. Put them in a single appendix at the very bottom, under a clear `---` divider:

- **Run metadata (one small italic line):** framework version, run date, and that metrics came from live tool calls. Nothing more.
- **Resolution/override notes:** which clients have a confirmed override applied (e.g. "DRF: single net price confirmed intentional"), and which integration ownership came from HubSpot deal line items.
- **Framework feedback:** clauses the run found ambiguous, under-specified, or contradicted by data. This is feedback to the framework maintainer, not part of the client read. (Previously this lived in a top-of-file "Run notes" block — it moves here.)
- **Flag-reference map (only if any flags fired this run):** a small two-column table mapping each plain-English issue title used above to its internal flag code, e.g. `No customers loaded yet → PHASE_4_VACUOUS_NO_CUSTOMERS`. This is the ONLY place a flag code may appear. It lets us cross-reference `Flags_and_Signals.md` without polluting the standup body.

A standup reader should be able to stop at the last client's "Bottom line" and have everything they need; the appendix is for the maintainer.
