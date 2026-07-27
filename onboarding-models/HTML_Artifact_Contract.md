# HTML Artifact Contract

How the weekly Onboarding Phase Assessment becomes a rendered HTML report.

The pipeline is **emit-JSON**: the run emits one structured JSON file, and a deterministic Python generator fills `phase-assessment.template.html` from it. The JSON — not the markdown — is the source of truth for rendering.

This is a **presentation contract only**. It does not change what the run computes — `Output_Contract.md` remains the single source of truth for *content*. This file governs the *last step*: data → HTML. It deliberately lives outside the four canonical framework files so they stay untouched.

## Files

| File | Role | Regenerated weekly? |
|---|---|---|
| `phase-assessment.template.html` | The layout shell + one tokenized fragment per repeatable region. | No — edit only to change layout. |
| `phase-assessment.css` | All page-local styling, shared by the template and every artifact. | No. |
| `phase-assessment.schema.json` | JSON Schema (draft-07) for the report data — field names, types, required, enums. | No. |
| `render_phase_assessment.py` | The generator: JSON + template → finished HTML. Fills regions, escapes text, rewrites asset paths, strips markers. | No. |
| `EXAMPLE-2026-06-09-phase-assessment.html` | Frozen, fully-populated reference (the 2026-06-09 cohort). Inline CSS so it stays a portable snapshot; doubles as the generator's golden file. | No — dated record. |
| `EXAMPLE-2026-06-09-phase-assessment.json` | The golden fixture — the exact JSON that renders the EXAMPLE html. Committed test asset (NOT under `output/`) so `--check` works on a fresh clone. | No — dated record. |
| `output/{date}-phase-assessment.md` | The week's content (the human-readable deliverable from the run). | Yes — every run. |
| `output/{date}-phase-assessment.json` | The week's content as structured data — the generator's input. | Yes — every run. |
| `output/{date}-phase-assessment.html` | The week's rendered artifact. | Yes — every run. |

## How to render (generator — primary path)

The run agent **emits the JSON** (per `phase-assessment.schema.json`), then runs the generator:

```bash
# from onboarding-models/
python3 render_phase_assessment.py output/{date}-phase-assessment.json
# → writes output/{date}-phase-assessment.html
```

The generator handles everything mechanical: cloning `@repeat` regions, keeping/dropping `@optional` regions, substituting tokens, **HTML-escaping plain-text fields**, rewriting relative asset paths for the output folder's depth, stripping all marker/instruction comments, and refusing to write if any `{{TOKEN}}` is left unresolved or more than one `urgent` agenda item is set. So the agent's only job is to emit correct, schema-valid data.

Regression check (any time the template, CSS, or generator changes):

```bash
python3 render_phase_assessment.py EXAMPLE-2026-06-09-phase-assessment.json \
  --check EXAMPLE-2026-06-09-phase-assessment.html   # prints MATCH
```

This compares the generated `<main>` body (comments + cosmetic whitespace normalized) against the frozen example. It must print `MATCH`.

### Authoring the data: escaping & `_html` fields

- **Plain-text fields** (names, titles, sentences, sources, etc.) are authored with **raw** characters — write `Lib & Co`, `Q&A`, `<3`. The generator escapes them. Do **not** pre-escape these.
- **Fields whose name ends in `_html`** (`detail_html`, `said_html`, appendix `overrides[]`/`feedback[]`) are **trusted inline HTML**, inserted verbatim. This is where verbatim quotes live — wrap them in `<blockquote class="oa-quote">` — and where `<span class="oa-code">`/`<code>` markup goes. Inside these, escape `&`→`&amp;` yourself, and keep quotes verbatim.

## Fallback: filling the template by hand (LLM-as-templater)

Only if the generator can't be run. Copy `phase-assessment.template.html` to the output target, fix relative paths for depth (`../design-system/…` → `../../design-system/…` and `./phase-assessment.css` → `../phase-assessment.css` when writing into `output/`), then fill every `{{TOKEN}}`, clone every `@repeat` region per item, resolve every `@optional` region, escape text values yourself, and remove all marker/instruction comments. `@repeat NAME … @end NAME` = clone per item; `@optional NAME … @end NAME` = keep or delete the whole block. Validate against the acceptance checklist below.

## Global rules (non-negotiable — from the design-system brief)

- **Logo is always the vector** `#i-mark`, colored gold. Never type "SuperCat" as text.
- **Status dots are never crimson.** `done → oa-dot-done` (muted green) · `in progress → oa-dot-progress` (clay) · `not started → oa-dot-todo` (hollow grey).
- **Crimson appears at most once** on the page: the `.oa-urgent` highlight on the single most urgent "Resolve this week" item, or not at all. Never on headings or body prose.
- **Verbatim quotes stay verbatim**, rendered as `<blockquote class="oa-quote">`. Never paraphrase a quote.
- **Sort clients by phase ascending** in both the cohort table and the per-client cards.
- **Don't invent colors or restyle primitives.** Use the classes as given.
- **Escaping is the generator's job for text fields** (author them raw); only `_html` fields are your responsibility. `&` is common in company names ("Lib & Co") — leave it raw in text fields.
- **No HTML comments in the final output.** The final HTML output must not contain `<!-- ... -->` comment blocks. Strip all HTML comments from the template during rendering. Instructional comments in the template are for the generator's reference only and must not appear in the delivered artifact.

## The fixed vocabulary

- **The 7 steps, always this order/labels:** 1 Kickoff · 2 First import · 3 Building the catalog · 4 Catalog ready · 5 Reps using the iPad · 6 Admin trained · 7 Live.
- **Status values:** `done` · `in progress` · `not started`. Step 7 is only `done` or `not started`.
- **Integration:** exactly one of `Us (Managed)` · `Them (Certified)` · `—` (none).
- **Standup agenda:** exactly three buckets, fixed order: Resolve this week · Discuss / decide · On track.

## Token & region reference

`phase-assessment.schema.json` is the authoritative field list; this section maps schema fields to template tokens and notes the few rules the generator applies. Tokens marked *(text)* are auto-escaped; tokens marked *(html)* are inserted verbatim.

### Report level — `report` object
| Token | Value |
|---|---|
| `{{REPORT_TITLE}}` | `"{Month D, YYYY} — Onboarding Phase Assessment"` (matches the md's H1). |
| `{{SOURCE_MD}}` | Path of the source markdown, e.g. `output/2026-06-09-phase-assessment.md`. |
| `{{RUN_METADATA}}` | The one italic appendix line: framework version · run date · "metrics from live tool calls". |

### Cohort table — `@repeat cohort-row` (one per client)
| Token | Value |
|---|---|
| `{{SHORT}}` | Lowercase shortname (also the `#client-{SHORT}` anchor target). |
| `{{CLIENT_NAME}}` | Display name, e.g. `Lib and Co.` |
| `{{PHASE_N}}` | Anchor phase number (1–7). |
| `{{PHASE_NAME}}` | Anchor phase name from the vocabulary. |
| `{{WORKING_ON}}` | Next phase name (`Phase N+1`), or `Live` if anchor = 7. |
| `{{DAYS}}` | Days in onboarding (integer, or a short string like `~320`). |
| `{{INTEGRATION_LABEL}}` | `Us (Managed)` · `Them (Certified)` · or for none use `<span class="kdt-empty">—</span>`. |
| `{{ONE_THING}}` | The single most important plain-English item. |

### Standup agenda — `agenda` object (`resolve` / `discuss` / `on_track`)
Three independent `@repeat` regions: `agenda-resolve`, `agenda-discuss`, `agenda-ontrack`. Each item: `lead` *(text)* + `detail_html` *(html)*.
- Each `<li>` renders `<b>{{LEAD}}</b> {{DETAIL_HTML}}`. **`lead` carries its own terminal punctuation** — e.g. `"Lib and Co. — fix the customer import."` (resolve/discuss) or just `"Dorell Fabrics"` (on-track, where `detail_html` continues the sentence).
- **Empty bucket:** emit an empty array; the generator renders `None this week`.
- **The one crimson item (optional):** set `"urgent": true` on the single most urgent resolve item. The generator renders the `.oa-urgent` chip + rule. At most one `urgent` across the whole report (the generator enforces this).

### Per-client card — `clients[]` (generator renders in array order; sort phase-ascending before emitting)
Header tokens: `{{SHORT}}`, `{{CLIENT_NAME}}` *(text)*, `{{PHASE_N}}`, `{{PHASE_NAME}}` *(text)*, `{{NEXT_PHASE_NAME}}` *(text)*, `{{PRODUCT}}` *(text)*, `{{DAYS}}` *(text)*, `{{DAYS_QUALIFIER}}` *(text, optional)* — a non-bold qualifier shown right after "In onboarding {days} days" and before the " · " separator (used for irregular cases like "~320 days since the account was created (…)"); default empty — and `{{ENGAGEMENT}}` *(text)*, the short note after the separator.

**7-step rail** — `{{STATE_1}}…{{STATE_7}}`, each one of:
- `is-done` — step status is done (green node)
- `is-progress` — step status is in progress (clay node)
- `is-todo` — step status is not started (hollow node)
- add `is-current` to the **"working on" step** (phase N+1) regardless of its status, e.g. `is-todo is-current` or `is-progress is-current` (gold ring).

The rail mirrors the "Where they are" statuses exactly — there is no "% ready" number; phase position is the only progress metric.

**Stepper state mapping:**
- Phases ≤ anchor phase: `is-done`
- The "working on" phase (anchor + 1): `is-progress is-current`
- Phases > working-on phase: `is-todo`

The `is-current` class controls which step receives the visual highlight (gold ring). It always goes on the working-on phase, never on the anchor.

**Where they are** — `@repeat where-row`, EXACTLY 7 rows, fixed `{{STEP_NO}}`/`{{STEP_LABEL}}` in order:
- `{{STATUS_DOT}}` = `oa-dot-done | oa-dot-progress | oa-dot-todo`
- `{{STATUS_WORD}}` = `Done | In progress | Not started`
- `{{WHAT_WE_SEE}}` = one plain sentence.

**Integration row (8th row)** — `@optional integration-row`:
- **Keep** only when integration = `Us (Managed)`. Fill `{{INTEG_DOT}}` / `{{INTEG_WORD}}` from the build's `status`, and `{{INTEG_WHAT_WE_SEE}}`.
- The `status` enum has no "untracked" value: a Managed build we own but aren't tracking uses `in_progress` (clay) — the "untracked" meaning is carried by the `INTEGRATION_OWNER_UNCLEAR` flag that fires alongside it, plus the row's `what_we_see` text.
- **Delete** for `Them (Certified)` and for none.

**Integration note** — `@optional integration-note`:
- **Keep** only when integration = `Them (Certified)`; `{{INTEGRATION_NOTE}}` = one informational sentence ("building their own integration; we certify it").
- **Delete** for `Us (Managed)` and for none.

(So: Managed shows the row, no note. Certified shows the note, no row. None shows neither.)

**Next step** — `{{NEXT_STEP}}`, one plain sentence. The card's most important line.

**Things to flag** — `@optional flags-section` (driven by the client's `flags[]`):
- **Omitted entirely** when `flags` is empty/absent. Otherwise `{{FLAG_COUNT}}` is filled with the count and `@repeat flag-row` renders once per flag:
  - `step` *(text)* = step number (`"1"`–`"7"`), a composite span like `"3/4"`, or `Integration`.
  - `issue` *(text)* = plain-English title. `code` *(text|null)* renders as a trailing `(CODE)` suffix; **use null/omit when there's no code** — never use a raw code as the title. **Also use `null` for confirmed/by-design/suppressed informational rows**, and for any flag whose code name would contradict its confirmed state (e.g. a confirmed single-net-price row must not render `…_UNCONFIRMED`). The plain title + `said_html` carry the "not a problem" meaning.
  - `source` *(text)* = where it's from (Fathom date / Help Scout #N / Database).
  - `said_html` *(html)* = EITHER a plain metric (text, but in an `_html` field so escape `&` yourself) OR a verbatim quote as `<blockquote class="oa-quote">“…”</blockquote>`. May mix a quote followed by a plain `<span>` sentence (see the example file).

**Post-flags note** — `@optional client-note`, field `note_html` *(html, optional)*:
- The md's free paragraph after the flags table — a read/caveat ("likely routine but worth confirming") or an out-of-order observation. Rendered muted between the flags table and Recent activity. Omit when absent.
- **Use this slot** for such commentary rather than burying it in a flag's `said_html` or padding `bottom_line`.

**Recent activity** — `{{MEETINGS}}`, `{{SUPPORT}}`, `{{IMPORTS}}` (one short line each).

**Bottom line** — `{{BOTTOM_LINE}}`, 2–3 plain sentences.

### Appendix
- `{{RUN_METADATA}}` — see report level.
- `@repeat override-note` — one `<li>` per override/resolution note (`{{OVERRIDE_NOTE_HTML}}`).
- `@repeat feedback-item` — one `<li>` per framework-feedback item (`{{FEEDBACK_HTML}}`).
- Wrap internal identifiers / codes / table names in `<code>` for readability.

## Acceptance checklist

Most of this is enforced by the generator; it matters mainly when authoring the JSON (or filling by hand).

**Data the agent must get right** (the generator can't infer these):
- [ ] Clients sorted phase-ascending; cohort and cards match 1:1 with the md.
- [ ] Every client has exactly 7 steps (`no` 1–7); step 7 is `done` or `not_started` only.
- [ ] `integration.mode` matches the client's case (`managed` → row · `certified` → note · `none` → neither), with the mode's required fields present.
- [ ] At most one agenda item has `urgent: true`.
- [ ] All quotes are verbatim, inside `<blockquote class="oa-quote">`, in an `_html` field.
- [ ] `&` is raw in text fields and `&amp;` inside `_html` fields (no double-escaping).

**Enforced automatically by the generator:**
- No `{{…}}` tokens / no `@repeat`/`@optional`/`@end` comments survive; text fields escaped; asset paths rewritten for depth; `flags: []` omits the flags block; empty agenda buckets render "None this week".

**Final smoke test:** `--check` against `EXAMPLE-2026-06-09-phase-assessment.html` still prints `MATCH`, and the new artifact opens with styling intact.

## Run wiring (emit-JSON)

What the weekly run agent does, end to end:

1. Compute the cohort as today (`Output_Contract.md` governs *what* the numbers/flags are).
2. **Emit `output/{date}-phase-assessment.json`** conforming to `phase-assessment.schema.json`. The markdown deliverable (`output/{date}-phase-assessment.md`) stays as the human-readable record; the JSON is the same content shaped for rendering.
3. Run `python3 render_phase_assessment.py output/{date}-phase-assessment.json` to produce the HTML.
4. (Recommended) run the `--check` smoke test above after any template/CSS/generator change.

Notes for the handoff agent wiring `RUN_PROMPT.md`:
- The JSON is the contract surface — point the run at `phase-assessment.schema.json` and the `_html`-vs-text escaping rule above. The agent should never edit the template, CSS, or generator.
- The generator is dependency-free (Python 3 stdlib only). `--check` is the regression guard; keep the golden pair together in `onboarding-models/` (`EXAMPLE-2026-06-09-phase-assessment.html` + `EXAMPLE-2026-06-09-phase-assessment.json`) — they are committed test assets, deliberately NOT under the gitignored `output/`.
