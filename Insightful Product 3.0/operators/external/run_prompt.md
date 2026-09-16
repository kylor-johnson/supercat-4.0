# Insightful Product 3.0 — Report Orchestrator

Produces a signal-first intelligence report end-to-end using parallel section
agents. Most steps are now deterministic Python scripts — the LLM only handles
section narrative generation and Signal Summary composition.

**Prerequisites:** Cursor with `user-supercat-postgres-vpn` and
`user-bigquery-admin` MCPs enabled. VPN active.

---

Read the entire prompt before starting.

## Client Parameters

The only required input is the **shortname**. Resolve everything else:

1. Query Postgres via `user-supercat-postgres-vpn`:
   `SELECT id, shortname, name FROM organizations WHERE shortname = '<shortname>' LIMIT 1;`
   If no row is returned, stop and report the error.
2. Set `ORG_ID` and `CLIENT_NAME` from the query result.
3. Set `RUN_DATE` to today (`YYYY-MM-DD`).

**Run directory:** `Insightful Product 3.0/runs/{SHORTNAME}_{RUN_DATE}/`
Create `cache/`, `fragments/`, and `output/` subdirectories.

---

## Step 1 — Data Gathering (Python script)

```bash
cd "Insightful Product 3.0"
source scripts/.venv/bin/activate
python scripts/data_gather.py \
  --shortname {SHORTNAME} \
  --org-id {ORG_ID} \
  --run-date {RUN_DATE}
```

After completion, verify `gate_flags.md` exists. Determine report mode:

| Mode | Condition |
|------|-----------|
| **Mode 1** (Standard) | LTM eCat orders > 0 OR LTM portal orders > 0 |
| **Mode 2** (Activation) | Zero commerce ever |
| **Mode 3** (Reactivation) | All-time commerce > 0 but LTM = 0 |

If Mode 2 or Mode 3, skip to **Mode 2/3 Handling** at the end of this prompt.
If Mode 1, proceed to Step 2.

---

## Step 2 — Signal Detection (Python script)

```bash
python scripts/detect_signals.py \
  --shortname {SHORTNAME} \
  --run-date {RUN_DATE}
```

Produces `cache/signal_rank.md` and `cache/top_accounts.md` deterministically.
No LLM needed — runs in < 5 seconds.

### Checkpoint

Report to chat: total signals fired (P0/P1/P2), top 3 signals by rank.

---

## Step 2.5 — Build Context Bundles (Python script)

```bash
python scripts/build_context.py \
  --shortname {SHORTNAME} \
  --run-date {RUN_DATE}
```

Produces `cache/section_NN_context.md` bundles (< 1 second).

---

## Step 3 — Spawn Section Agents (PARALLEL)

For each qualifying section (not marked skip in `signal_rank.md`), spawn a
**separate subagent** using the section build prompt at
`operators/external/section_build_prompt.md`.

Each section agent receives this task:

```
Run the section build prompt at:
  Insightful Product 3.0/operators/external/section_build_prompt.md

Parameters:
  SHORTNAME: {SHORTNAME}
  RUN_DATE: {RUN_DATE}
  SECTION_NUMBER: {N}
  BUNDLE_PATH: Insightful Product 3.0/runs/{SHORTNAME}_{RUN_DATE}/cache/section_{NN}_context.md
  FRAGMENTS_DIR: Insightful Product 3.0/runs/{SHORTNAME}_{RUN_DATE}/fragments/
  CACHE_DIR: Insightful Product 3.0/runs/{SHORTNAME}_{RUN_DATE}/cache/
```

**Spawn ALL section agents simultaneously.** They are fully independent — each
reads only its own context bundle and writes only its own fragment files.

Typical sections to spawn (skip any marked skip):
- §5 Team Intelligence
- §2 Account Intelligence
- §4 Commerce Patterns
- §3 Product Intelligence
- §6 Platform Context

Wait for all section agents to complete before proceeding.

### Checkpoint

Report to chat: which section agents were spawned, which completed successfully,
fragment file sizes.

---

## Step 4 — Build Signal Summary (LLM — the ONLY narrative step in assembly)

Read:
- `operators/external/guides/section_01_signals.md` (Signal Summary guide)
- All `cache/section_NN_highlights.md` files
- `cache/signal_rank.md`

Build the Signal Summary fragment following the guide exactly. Save to
`fragments/section_01.html`.

**CRITICAL BALANCE CHECK**: Finding #1 MUST be positive. At least 3 of 7
findings must be positive. Risk findings go in slots 5–7 only. At least
1 Priority Action must be a GROWTH action.

---

## Step 5 — Assemble Final Report (Python script)

```bash
python scripts/assemble_report.py \
  --shortname {SHORTNAME} \
  --run-date {RUN_DATE}
```

Concatenates all fragments in fixed order (§1→§5→§2→§4→§3→§6→Appendix),
substitutes placeholders, strips HTML comments. Runs in < 1 second.

---

## Step 6 — Audit (Python script)

```bash
python scripts/audit_report.py \
  --shortname {SHORTNAME} \
  --run-date {RUN_DATE}
```

Structural verification: subsection completeness, forbidden terms, details
balance, what-this-means count. Runs in < 2 seconds.

If FAIL: review the defect list. If missing subsections, re-spawn the affected
section agent(s). If forbidden terms, patch the assembled HTML.

```bash
bash qa/eval/check_static.sh \
  "runs/{SHORTNAME}_{RUN_DATE}/output/{SHORTNAME}_{RUN_DATE}_intelligence_report.html" \
  {RENDERED_SECTION_COUNT}
```

---

## Final Report to Chat

1. Report mode and signal detection summary
2. Sections rendered (in fixed order) with signal counts
3. Top 3 signals surfaced
4. Audit result (PASS / FAIL)
5. Output file path
6. Confirmation: report ready for browser review

---

## Batch Mode

For running multiple clients, use the batch runner to handle all deterministic
work first:

```bash
python scripts/batch_run.py \
  --shortnames cci,kal,shl,mlc,... \
  --parallel 4 \
  --run-date {RUN_DATE}
```

This runs data_gather + detect_signals + build_context for all clients in
parallel. Then spawn a fresh agent per client for Steps 3-6 (section agents +
signal summary + assembly + audit).

---

## Mode 2/3 Handling (Simplified)

Mode 2 (Activation) and Mode 3 (Reactivation) have insufficient commerce data
for signal detection. Skip Steps 2–4 and build directly from mode-specific
templates.

| Mode | Scope |
|------|-------|
| **Mode 2** (Activation) | Platform readiness + peer context only. No commerce sections. |
| **Mode 3** (Reactivation) | Historical commerce context + platform staleness + re-engagement framing. |

For both modes:

1. Complete Step 1 (data gathering) as normal.
2. Read mode-specific structure from `authority/report_architecture.md`.
3. Build the lean section set defined there (no signal detection, no ranked ordering).
4. Assemble and run the audit as in Steps 5–6.
