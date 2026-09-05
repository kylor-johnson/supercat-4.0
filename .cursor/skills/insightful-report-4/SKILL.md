---
name: insightful-report-4
description: Run an Insightful Product 4.0 CEO Intelligence Report end-to-end from just a client shortname. Two-pass prose generation (deterministic pipeline + agent-authored prose). This is the DEFAULT Insightful report. Use when the user says "run a report for X", "run insightful for X", "generate the intelligence report for X", "run the 4.0 report for X", or names a client shortname in a report context — unless they explicitly ask for the 2.0 / Customer Intelligence Report.
---

# Insightful Product 4.0 — Report Runner (Agent-Driven Prose)

Run a complete CEO Intelligence Report from **just a client shortname**. No API key
needed — you (the agent) generate the prose slots directly.

## Reading contract (load BEFORE Step 1)

Per `CANON.md` in the project root — read these in order. Do **not** load
`foundation/capability/**` (VM catalog / Money Map) to run a report.

```
PROJECT=…/Insightful Product 4.0
```

0. `$PROJECT/foundation/WHAT_ACTUALLY_RUNS.md` — 24 live queries, 14 signals, two axes
1. `$PROJECT/foundation/provenance_spine.md` — invoiced-net + gates (factory commerce gate = **`Q-ECON-00`**)
2. `$PROJECT/profiles/{org}.md` — who this client is
3. `$PROJECT/knowledge/industry_context.md` — industry-normal = **context, not a finding**
4. `$PROJECT/knowledge/communication_guideline.md` — voice ("no shit" test, anti-cute, failure modes)

When writing slots, apply (3) and (4) as hard constraints — the API path injects them into
the system prompt automatically; **you must apply them yourself** on this agent path.

## What the user gives you

- A **shortname** (e.g. `sarreid`, `cci`, `clc`, `ali`, `da`)
- Optionally: a date (`--date 2026-07-02`). Default: today.

## Architecture

The report has 6 LLM prose slots (A-F). Instead of calling an external LLM API,
**you** generate the prose for each slot, validate it, and write it to a file the
pipeline picks up.

## Setup

```
PROJECT=/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Insightful Product 4.0
PY="$PROJECT/.venv-renderer/bin/python"
```

If the venv is broken or missing, recreate:
```
/opt/homebrew/bin/python3.13 -m venv "$PROJECT/.venv-renderer"
"$PROJECT/.venv-renderer/bin/pip" install -r "$PROJECT/requirements-pipeline.txt" beautifulsoup4 lxml
```

---

## Step 1 — Run the deterministic pipeline pass

```bash
cd "$PROJECT" && ./run.sh {org} --date {date}
```

This produces:
- `outputs/{org}_DRAFT_{date}.md` — the markdown draft (deterministic prose)
- `outputs/{org}_bundles_{date}.json` — the fact bundles for all 6 slots
- `outputs/{DisplayName}_CEO_intelligence_report_{date}.html` — the HTML (with deterministic fallback prose)
- Console output showing `slots: all skipped (no API key)` or `slots: loaded X/6 from ...`

If it says "all skipped", proceed to Step 2. If it says "loaded 6/6", the prose
file already exists and was used — skip to Step 4.

---

## Step 2 — Generate prose for each slot

Read `outputs/{org}_bundles_{date}.json`. It contains `slot_a_bundle` through
`slot_f_bundle`, plus `expected_counts`.

For each slot, generate prose following these rules:

### Absolute constraints (apply to ALL slots)

1. Every dollar you cite must come from the fact bundle (facts OR derived_facts). **No new numbers.**
2. No forbidden vocab: posture, feed(s), pipeline (as verb), house-rep, NRR, cohort, playbook, franchise, flywheel, treadmill.
3. Markdown formatting only.
4. Use derived_facts where present; do NOT recompute ratios or deltas.
5. If a fact is absent or null, skip it — never hallucinate a placeholder number.

### Slot A — hero_framing

**Input:** `slot_a_bundle`
**Output:** A markdown string (2-4 paragraphs). The 60-second executive framing.
Lead with the topline dollar, then the same-dealer spend ratio (from derived_facts),
then 2-3 surprise findings from the signals. End with priority actions by cadence.

### Slot B — talking_points

**Input:** `slot_b_bundle`, expected_counts.talking_points = N
**Output:** A JSON array of exactly N markdown strings (one per account in the outreach list).
Each talking point is what the rep says on the call — 1-2 sentences, direct, specific.
- Accounts with `is_cadence_cliff=true` are GROWING — do NOT use decline language.
- Accounts with `is_real_decline=true` — be direct about the slope.
- Use the `derived_facts.pace_description` and `derived_facts.gap_multiple` for phrasing.

### Slot C — coaching_narratives

**Input:** `slot_c_bundle`, expected_counts.coaching_narratives = N
**Output:** A JSON array of exactly N markdown strings (one per rep coaching card).
Each narrative (2-4 sentences) must:
- Name the top at-risk account and its `derived_facts.decay_dollars` (NOT full LTM)
- Express whether it's a real decline or beat-skip using `derived_facts.beat_skip_label`
- Give one specific action

### Slot D — play_framing

**Input:** `slot_d_bundle`, expected_counts.play_framing = N
**Output:** A JSON array of exactly N markdown strings (one per play).
Each play body (2-5 sentences) should lead with the dollar and the name.
Use `derived_facts.upside_range` for cross-sell plays and flag as DIRECTIONAL.

### Slot E — growth_connective

**Input:** `slot_e_bundle`
**Output:** A JSON object with keys `"layer_1"`, `"layer_2"`, `"layer_3"`, each a markdown string.
1-2 connective sentences per layer that tie numbers into a narrative. Not arithmetic
narration ("$X offset $Y") but synthesis ("the engine is broad-based dealer reorder,
not one account dressed up as a year").

### Slot F — outreach_framing

**Input:** `slot_f_bundle`
**Output:** A single markdown string (2-3 sentences).
Frame the call list. If both real declines AND beat-skips are present, warn the reader
not to conflate the two conversations. Name which rows are which.

### Validation

After generating each slot, verify:
- Every dollar/percent you wrote traces to a value in the bundle's facts or derived_facts
- No forbidden vocabulary
- Correct structure (arrays have exactly N items, object has the right keys)

If a slot fails validation, fix it before including it.

---

## Step 3 — Write the prose file

Write all generated prose to `outputs/{org}_prose_{date}.json`:

```json
{
  "hero_framing": "...",
  "talking_points": ["...", "...", ...],
  "coaching_narratives": ["...", "...", ...],
  "play_framing": ["...", "...", ...],
  "growth_connective": {"layer_1": "...", "layer_2": "...", "layer_3": "..."},
  "outreach_framing": "..."
}
```

---

## Step 4 — Re-run the pipeline (picks up prose)

```bash
cd "$PROJECT" && ./run.sh {org} --date {date}
```

This time it will say: `slots: loaded 6/6 from {org}_prose_{date}.json`

The pipeline injects the prose into the templates with `<!--slot:X-->` markers,
renders HTML, and runs `smoke_check` + `step10_check`.

If SHIP: you're done. Show the user the output path.

If step10_check fails: read the violations, fix the offending slot(s) in the prose
file, and re-run.

---

## Step 5 — Deliver

Tell the user:
- Output: `outputs/{DisplayName}_CEO_intelligence_report_{date}.html`
- Slot status (which slots shipped LLM prose vs deterministic fallback)
- Any validation issues encountered and how they were resolved

---

## Quick reference

| Slot | Key | Type | Template section |
|------|-----|------|-----------------|
| A | hero_framing | string | §1 "The 60-second read" |
| B | talking_points | string[] | §2 call-list table "Talking point" column |
| C | coaching_narratives | string[] | §6 coaching card narratives |
| D | play_framing | string[] | §3 play body prose |
| E | growth_connective | object | §5 layer connective tissue |
| F | outreach_framing | string | §2 call-list header callout |

## Troubleshooting

- **"ERROR: no cache"** — run `python -m pipeline.populate_cache --org {org} --date {date}` first, or use MCP to execute the queries and write CSVs.
- **step10_check fails on forbidden vocab** — the prose likely used a word from the blocklist. Read the violation, fix the prose file, re-run.
- **"FELL BACK" for a slot** — the prose file had that key as `null` or missing. Fill it in.
- **Byte count way off** — check that talking_points array has exactly N items (match expected_counts).
