# Health V3 — Trigger Engine V2 Patch

> **What this is:** An orchestration prompt for a senior agent patching `trigger_engine_v1.py` to improve CS signal quality. The agent using this file is the central brain — it makes decisions, delegates discrete coding tasks to focused sub-agents, reviews their output, and stitches everything together. It does not implement code itself except for the connective-tissue work (doc updates, CHANGELOG, version bumps).
>
> **How to use it:** Read this file top to bottom. Then read the live files listed in the Read First section. Answer the four open questions. Present your plan to the user. On go-ahead, execute the work breakdown below — spawning sub-agents for the coding tasks, reviewing their output, and doing the documentation work yourself.

---

## Current state

The Health V3 infrastructure is clean. `check_consistency.py` passes 14/14. The trigger engine has `--production-csv`, auto-detection of the latest run, and score-date-keyed output filenames. Those were fixed in a prior session.

The problem is **trigger output quality**. The summary a CS rep opens today contains 112 triggers across 7 months of history with no way to distinguish urgent from noise. The specific failure modes are documented in the Background section below.

**Version at time of writing:** Read `CHANGELOG.md` top entry to confirm the current version before writing the new entry.

**Canonical SHA (unchanged by this patch):** `e34552abe2232c630b088465a067c77a39d598cd6979e912717626598edafce9`

---

## Read first — before doing anything else

| File | What to look for |
|------|-----------------|
| `trigger_engine_v1.py` | Config block, `detect_triggers`, `write_outputs`, `main`, all argparse args — read in full |
| `trigger_reports/trigger_summary_2026-05-13.txt` | The actual output a CS rep receives today |
| `trigger_reports/trigger_report_2026-05-13.csv` | Current column schema |
| `check_consistency.py` | All 14 existing invariants — understand before planning to add a 15th |
| `CHANGELOG.md` | Top entry only — confirm current version number |
| `README.md` §6.6 | The invariant documentation pattern |
| `FRESH_RUN_GUIDE.md` | Step 3b trigger invocation and monthly checklist |
| `RUN_PROMPT.md` | Step 5 — note invariant count and trigger invocation |

After reading, confirm in your plan whether the live files match the descriptions in this document. Call out any discrepancy before proceeding.

---

## Background: why these changes

When a CS rep opens the May trigger summary they see 112 triggers across 7 months with no prioritization guidance. Specific failure modes visible in the live output:

- `vic` fires `band_transition_down` on an 80.0 → 78.9 move (1.1 pt delta — boundary noise, not a regression)
- `prog` fires both `band_transition_down` and `score_drop` for the same April event — two rows, two actions, one conversation
- `tel` fires `chronic_at_risk` AND `band_transition_down` for the same run date — the pattern signal and the point-in-time signal are redundant
- `bp` has alternated Healthy↔Watch across 6 consecutive months — no trigger type exists for this pattern
- The summary says "note which dimension drove this" but never tells you which dimension
- `composite_narrative` — the most readable per-org context in the canonical CSV — is invisible to CS
- Every run dumps the full 7-month backfill — there is no way to ask "what changed this month only"
- `band_transition_up` wins are mixed into the Immediate/High intervention queue

---

## The seven planned changes

### Change 1 — BAND_TRANSITION_MIN_SCORE_DELTA config constant

Add `BAND_TRANSITION_MIN_SCORE_DELTA = 3.0` to the config block alongside `SCORE_DROP_THRESHOLD`. Both `band_transition_down` and `band_transition_up` only fire if the composite score also moved at least this many points. If either score is None, fire anyway — missing data is notable.

Expected result: `vic` (80.0 → 78.9) and `ali` (80.0 → 79.9) are suppressed. `prog` (73.8 → 57.5) still fires.

---

### Change 2 — Deduplication: band_transition_down + score_drop for same org/month

In a deduplication pass at the end of `detect_triggers`: for each `(org_shortname, run_date)` pair, if both `band_transition_down` and `score_drop` exist, drop `score_drop` and append " | Also a score_drop trigger." to the `band_transition_down` detail. Only deduplicate within the same `(org_shortname, run_date)`.

Expected result: `prog` (April 30) appears once.

---

### Change 3 — Pattern-level triggers suppress point-in-time triggers at latest run

If an org fires `chronic_at_risk` or `oscillating_band` (Change 6) for the latest run date, remove `band_transition_down` triggers for that org from the same `run_date`. The pattern signal supersedes the point-in-time transition.

> See **Open Question A** — scope of this suppression (does it extend to `score_drop`?) is an open design decision.

Expected result: `tel` appears as `chronic_at_risk` but not `band_transition_down` for `run_date = 2026-05-13`.

---

### Change 4 — Dimension driver identification

After building `base` in the MoM loop, compute `top_dim_driver` — the dimension name with the largest absolute decline (downward triggers) or largest absolute gain (upward triggers) between `prior` and `curr`. Add to `base`, add to `OUTPUT_COLS`, append to the detail string for `band_transition_down`, `score_drop`, and `band_transition_up`. Example: "Band regressed: Healthy → Watch | Driver: Value Delivery". `chronic_at_risk` gets no driver field — it uses full history, not a single pair.

---

### Change 5 — Pull composite_narrative into trigger rows

Add `composite_narrative = curr.get("composite_narrative", "")` to `base` and to `OUTPUT_COLS`. CSV output only — do not include in the plain-text summary (too long, will wreck the layout).

---

### Change 6 — oscillating_band trigger type

New trigger type detected after the MoM loop. An org is oscillating if its band changed on every consecutive pair for the last 4+ months AND it alternated between exactly two bands. Fire once per org at the latest run date. `prior_date` is the start of the oscillation window.

Add to `CS_ACTIONS` with three urgency levels. Immediate: "Structural instability at high-ARR account — 4+ months alternating bands. CS leadership review required. Do not treat as a routine check-in." High: "Assign a dedicated CS owner. This account has failed to stabilize — current touch cadence is insufficient." Standard: "Escalate from reactive to proactive. Review call history; account is not responding to current intervention."

Add to `TRIGGER_ORDER` at position 1, after `new_ghost`, before `chronic_at_risk`. Update the docstring trigger type list.

Orgs that fire `oscillating_band` should have `band_transition_down` suppressed at the latest run date (Change 3 logic).

> See **Open Questions B and C** for detection window and delta filter interaction decisions.

Expected result: `bp` fires `oscillating_band`. Its `band_transition_down` for the latest run date is suppressed.

---

### Change 7 — --current-only flag and POSITIVE SIGNALS section

**Part A — --current-only flag:** Add `--current-only` boolean flag (default False). When set, limit MoM detection to the most recent run-pair only. `chronic_at_risk` and `oscillating_band` still use full history for detection but only emit if `run_date == latest_date`. Summary header changes to include "(Current Month)".

**Part B — POSITIVE SIGNALS section:** Move all `band_transition_up` triggers out of Immediate/High sections into a new POSITIVE SIGNALS section at the end of the summary. The intervention urgency sections filter to `trigger_type != "band_transition_up"`. Update the stats block at the top to add "Positive signals (band_up): N".

> See **Open Question D** — whether to update the monthly runbook to default to `--current-only`.

---

## Open questions — answer these before presenting your plan

These are genuine design choices. Read the live data, form a view, and state your recommendation with reasoning. The user will confirm or override before implementation begins.

### Open Question A — Does pattern-level suppression extend to score_drop?

Change 3 suppresses `band_transition_down` when an org fires `chronic_at_risk` or `oscillating_band`. But if that same org also fires `score_drop` at the latest run date, that row still appears alongside the pattern-level trigger.

**Decision:** Should `score_drop` also be suppressed for orgs firing a pattern-level trigger at the latest run date? Or does a concurrent point-in-time drop add useful information even when the pattern is already flagged?

---

### Open Question B — oscillating_band window detection

The detection window is "4 or more months, maximum lookback 8 months." If the last 4 months alternate but the 5th month does not, it is ambiguous whether the trigger should fire.

**Decision:** Should the logic find the longest trailing window (up to 8 months) that satisfies the alternating pattern and fire if that window is ≥ 4 months? Or should it require a fixed minimum window from the most recent month backwards? Look at the actual `bp` band history in the data and state which approach produces a cleaner result for the current portfolio.

---

### Open Question C — oscillating_band and the Change 1 delta filter

Change 1 requires a minimum 3.0 pt composite delta for `band_transition_down` to fire. An org could technically oscillate between two bands while each individual transition is below 3.0 pts — those transitions would be filtered by Change 1, but `oscillating_band` would still fire.

**Decision:** Should `oscillating_band` detection count transitions from raw band history (ignoring the 3.0 pt filter) or only count transitions that also meet `BAND_TRANSITION_MIN_SCORE_DELTA`? Check the `bp` data specifically — do the individual `bp` transitions clear 3.0 pts?

---

### Open Question D — Should monthly runbooks default to --current-only?

Change 7 adds `--current-only` but `FRESH_RUN_GUIDE.md` Step 3b and `RUN_PROMPT.md` Step 5 currently show the trigger engine invoked without it. Without updating those docs, the flag exists but will never be used in practice.

**Decision:** Should the runbook docs be updated to include `--current-only` in the standard monthly invocation? If yes, state the exact invocation you would put in each file.

---

## Work breakdown — what you do vs. what sub-agents do

The orchestrator handles decisions and documentation. Coding tasks go to focused sub-agents with minimal context to avoid drift. After each sub-agent run, review its output against the checklist before accepting.

| Task | Who | Why |
|------|-----|-----|
| Answer the four open questions | Orchestrator | Requires reading context and making judgment calls |
| Present plan to user, get go-ahead | Orchestrator | Requires full context |
| Implement Changes 1–7 in `trigger_engine_v1.py` | Sub-agent A | Discrete, bounded, no history needed |
| Add Invariant 15 to `check_consistency.py` | Sub-agent B | Discrete, bounded, no history needed |
| Update `FRESH_RUN_GUIDE.md`, `RUN_PROMPT.md`, `README.md` §6.6 | Orchestrator | Requires knowing the decisions made in open questions |
| Delete orphan trigger files | Orchestrator | One-liner, no context isolation needed |
| Write CHANGELOG entry, bump versions | Orchestrator | Requires knowing all changes made |
| Final `check_consistency.py` run and verification | Orchestrator | Requires interpreting results in full context |

---

## Sub-agent A prompt — trigger_engine_v1.py implementation

Copy this block verbatim to a fresh agent with no prior context. Do not add to it. Replace the `[DECISION: ...]` placeholders with the decisions you finalized on the open questions before sending.

---

```
You are making targeted improvements to one Python file:
Health V3/trigger_engine_v1.py

Read the full file before touching anything. Then implement exactly the seven changes below in order. Do not make any other changes. Do not modify any other file.

CHANGE 1 — Add to the config block alongside SCORE_DROP_THRESHOLD:
BAND_TRANSITION_MIN_SCORE_DELTA = 3.0  # band_transition_down/up only fires if composite also moved >= this pts
In detect_triggers, add abs(score_now - score_prior) >= BAND_TRANSITION_MIN_SCORE_DELTA as an additional condition for both band_transition_down and band_transition_up. If either score is None, fire the trigger anyway.

CHANGE 2 — Event deduplication (same org, same month).
After building the full trigger list in detect_triggers, before returning, add a deduplication pass. For each (org_shortname, run_date) pair: if both band_transition_down and score_drop exist, drop the score_drop entry and append " | Also a score_drop trigger." to the band_transition_down detail string. Only deduplicate within the same (org_shortname, run_date). This is about merging two rows that describe the same event.

CHANGE 3 — Pattern-level suppression (separate logic from Change 2).
In the same deduplication pass, but as a distinct step after Change 2: if an org fires chronic_at_risk or oscillating_band (Change 6) for the latest run date, remove all band_transition_down triggers for that org from the same run_date. [DECISION A: also remove score_drop? YES/NO based on orchestrator decision] This is about a pattern-level signal superseding a point-in-time signal — different concept from Change 2.

CHANGE 4 — In detect_triggers, in the MoM loop after building base, compute top_dim_driver. Iterate over the four dimension keys (engagement_score, adoption_score, value_delivery_score, operational_health_score) paired with labels (Engagement, Adoption, Value Delivery, Ops). Compute delta = now_v - prev_v for each where both are non-None. For band_transition_down and score_drop, top_dim_driver = the label with the most negative delta. For band_transition_up, use the most positive delta. If no deltas are computable, set top_dim_driver = "". Add top_dim_driver to base. Add "top_dim_driver" to OUTPUT_COLS. Append "| Driver: {top_dim_driver}" to the detail string for band_transition_down, score_drop, and band_transition_up. chronic_at_risk gets top_dim_driver = "" — do not append driver to its detail.

CHANGE 5 — In the MoM loop and in the chronic_at_risk block, add composite_narrative = curr.get("composite_narrative", "") to base. Add "composite_narrative" to OUTPUT_COLS at the end. CSV output only — do not reference it anywhere in the plain-text summary write logic.

CHANGE 6 — Add oscillating_band trigger detection after the chronic_at_risk block. An org is oscillating if: [DECISION B: use longest trailing window up to 8 months that satisfies the pattern, minimum 4 months / OR fixed window — fill in orchestrator decision]. The condition is: band changed on every consecutive pair in the window AND exactly two distinct bands appear in that window. Fire once per org at latest_date. prior_date = start of the window. Add oscillating_band to CS_ACTIONS with Immediate / High / Standard copy as specified by the orchestrator. Add oscillating_band to TRIGGER_ORDER at position 1 (after new_ghost, before chronic_at_risk). [DECISION C: count transitions from raw band history or only transitions that meet BAND_TRANSITION_MIN_SCORE_DELTA — fill in orchestrator decision]. Update the module docstring to list oscillating_band in the trigger types list.

CHANGE 7A — Add --current-only boolean flag to argparse (default False, store_true). Pass current_only to detect_triggers. When current_only=True, limit the MoM loop to i == len(runs) - 1 only. chronic_at_risk and oscillating_band still use full history but only emit if run_date == latest_date. When --current-only is active, prepend "(Current Month) " to the report title in write_outputs.

CHANGE 7B — In write_outputs, change the urgency loop to filter out band_transition_up: for label, level in [("IMMEDIATE", "Immediate"), ("HIGH PRIORITY", "High")]: items = [t for t in sorted_t if t["urgency"] == level and t["trigger_type"] != "band_transition_up"]. After the High section, add a POSITIVE SIGNALS section listing all band_transition_up triggers with org, run_date, ARR, band transition, score transition, and top_dim_driver. Add "Positive signals (band_up): N" to the stats block at the top of the summary.

After implementing all seven changes, run the engine against the existing data:
cd "Health V3"
.venv/bin/python3 trigger_engine_v1.py --production-csv runs/2026-05-13/client_health_scores_2026-05-13.csv

Verify and report:
- vic (80.0 → 78.9): appears in band_transition_down? Expected: NO
- prog (April 30): appears how many times? Expected: ONCE
- tel: appears as chronic_at_risk without band_transition_down at run_date 2026-05-13? Expected: YES
- bp: appears as oscillating_band? Expected: YES
- band_transition_up entries: appear in POSITIVE SIGNALS only? Expected: YES
- top_dim_driver column: present in CSV? Expected: YES
- composite_narrative column: present in CSV? Expected: YES

Then run with --current-only and report the trigger count difference vs the full run.

Do not modify any file other than trigger_engine_v1.py. Report what you implemented and the spot-check results.
```

---

## Sub-agent A output review checklist

Before accepting Sub-agent A's output and moving on:

- [ ] vic (80.0 → 78.9) absent from band_transition_down — **[verifies Change 1: delta filter]**
- [ ] prog (April 30) appears exactly once — **[verifies Change 2: event deduplication]**
- [ ] tel appears as chronic_at_risk with no band_transition_down for run_date 2026-05-13 — **[verifies Change 3: pattern suppression]**
- [ ] bp appears as oscillating_band with no band_transition_down at latest run date — **[verifies Change 6: oscillating_band + Change 3 suppression]**
- [ ] band_transition_up entries appear only in POSITIVE SIGNALS section — **[verifies Change 7B]**
- [ ] CSV contains top_dim_driver column — **[verifies Change 4]**
- [ ] CSV contains composite_narrative column — **[verifies Change 5]**
- [ ] --current-only produces a materially shorter trigger list — **[verifies Change 7A]**
- [ ] Output files named trigger_report_2026-05-13.csv and trigger_summary_2026-05-13.txt — **[regression: score-date naming still intact]**
- [ ] No files other than trigger_engine_v1.py were modified — **[scope check]**

If any check fails, send a correction prompt to Sub-agent A with only the specific failing item before proceeding.

---

## Sub-agent B prompt — Invariant 15 in check_consistency.py

Copy this block verbatim to a fresh agent. Send only after Sub-agent A's output has passed the review checklist above.

---

```
You are adding one new invariant to one Python file:
Health V3/check_consistency.py

Read the full file before touching anything. Understand the existing invariant structure — how Result is used, how each invariant function is named and structured, how they are registered in main().

Add the following invariant. Do not add any other changes. Do not modify any other file.

INVARIANT 15 — BAND_TRANSITION_MIN_SCORE_DELTA is defined in trigger_engine_v1.py

Function name: check_band_transition_delta_constant
Name string: "Invariant 15 — BAND_TRANSITION_MIN_SCORE_DELTA is defined in trigger_engine_v1.py"

Implementation: Read trigger_engine_v1.py as text using _read_text(root / "trigger_engine_v1.py"). Check that the string "BAND_TRANSITION_MIN_SCORE_DELTA" appears in the text. If absent, return Result(False, name, detail="BAND_TRANSITION_MIN_SCORE_DELTA is not defined in trigger_engine_v1.py. This constant filters micro-boundary band transitions — without it, every 0.1-pt crossing fires as a trigger."). If present, return Result(True, name).

Important scoping note: do NOT scan README.md for this invariant. The invariant description will appear in README.md §6.6 after documentation is updated, and that self-reference would cause a false positive.

Register the new function in the checks list in main().

After adding it, run:
cd "Health V3"
.venv/bin/python3 check_consistency.py

Expected result: 15/15 PASS, exit 0. Report the full output.

Do not modify any file other than check_consistency.py.
```

---

## Sub-agent B output review checklist

Before accepting Sub-agent B's output:

- [ ] check_consistency.py exits 0 with 15/15 PASS
- [ ] Invariant 15 is in the list, not just passing silently
- [ ] No other invariants were modified
- [ ] No files other than check_consistency.py were modified

---

## Orchestrator documentation tasks

Do these yourself after both sub-agents have passed their review checklists.

**1. Update invariant counts in docs:**
- `README.md` §6.6 — add Invariant 15 to the numbered list with one-line description. Update any "14 invariants" or "14/14" count references.
- `FRESH_RUN_GUIDE.md` monthly checklist — update "14/14 PASS" to "15/15 PASS".
- `RUN_PROMPT.md` Step 5 — update "14 invariants" to "15 invariants".

**2. Update trigger engine invocation in runbooks** (only if Open Question D was answered YES):
- `FRESH_RUN_GUIDE.md` Step 3b — update the invocation command.
- `RUN_PROMPT.md` Step 5 — update the invocation command.

**3. Delete orphan files:**
- `trigger_reports/trigger_report_2026-05-14.csv`
- `trigger_reports/trigger_summary_2026-05-14.txt`

**4. CHANGELOG entry:**
Add a new entry at the top of `CHANGELOG.md`. Tag it as tooling-only, canonical SHA unchanged. Under "Trigger engine quality improvements" document each of the seven changes in one sentence. Under "Tooling" document Invariant 15 and the invariant count updates. Under "Cleanup" document deletion of the two orphan files. Follow the format of the most recent entry.

**5. Version bumps:**
- `README.md` version and date
- `METHODOLOGY.md` version and date

**6. Final consistency check:**
```bash
cd "Health V3"
.venv/bin/python3 check_consistency.py
```
Expected: 15/15 PASS, exit 0. If anything fails, resolve before declaring done.

---

## Hard constraints

- Do not modify `health_operator_v3.py`.
- Do not modify any file in `runs/`, `cache/`, or `_archive/`.
- Do not touch the canonical CSV or its SHA.
- Do not move files between directories.
- Do not implement changes beyond the seven listed.
- Do not collapse `run_metadata.md` and `run_record.md` — both exist intentionally.

---

## Done criteria

The patch is complete when all of the following are true:

- [ ] Sub-agent A review checklist: all items pass
- [ ] Sub-agent B review checklist: all items pass
- [ ] `check_consistency.py` exits 0 with 15/15 PASS
- [ ] All docs say 15 invariants, not 14
- [ ] CHANGELOG has a new entry at the top
- [ ] README.md and METHODOLOGY.md version and date are bumped
- [ ] Orphan files are deleted
- [ ] Monthly runbooks reflect the Open Question D decision
