> **COMPLETED — archived 2026-09-16.** The V3.2.x patch loop this drove is
> finished. SHAs and version numbers quoted below are historical. For a
> present-day operator change, follow `RUN_PROMPT.md` and CHANGELOG 3.4.0.

---

# Health V3 — Operator Patch Prompt

> **What this is:** A reusable, SHA-gated prompt for applying a *single-purpose* code patch to `health_operator_v3.py`. Use this any time the operator needs a focused fix (comment cleanup, dead-code removal, narrow logic change, etc.) where the canonical SHA contract must be enforced.
>
> The whole point of this prompt is the **two-pass byte-identical SHA gate** — a patch can only ship if either (a) the canonical CSV SHA is unchanged from the prior version, or (b) the SHA change is intentional and fully documented. A fresh agent reading this prompt cannot rationalize a silent SHA shift; either the gate clears or the patch stops.

---

**When to use:**

- Any change to `health_operator_v3.py` outside of a routine canonical refresh.
- Any change a separate agent should validate independently of the agent that proposed it.
- *Not* for monthly canonical runs — use `RUN_PROMPT.md` for those.
- *Not* for narrative or dashboard work that doesn't touch the operator — use `DASHBOARD_POLISH_PROMPT.md`.

**Prerequisites:**

- Working `Health V3/.venv/` with `pandas` installed.
- The most recent canonical cache directory exists: `Health V3/cache/{prior-score-date}/` (currently `cache/2026-05-13/`).
- The prior canonical CSV and its SHA-256 are recorded in `CHANGELOG.md`.
- The MAL referenced in the prior canonical's `run_metadata.md` is still readable (currently `inputs/master_account_list_2026-04-14_canonical.csv`).

**Rough runtime:** 5–10 min per patch (edit + two cache-mode runs + SHA compare + version bump + CHANGELOG entry).

**Hard rules:**

- **One patch per invocation.** Do not bundle. The SHA gate is most useful when it can bisect a single change.
- **Do not modify anything outside the specified location.** If the patch description says "function X lines N–M," only touch those lines.
- **Do not modify the cache.** Use the existing `cache/{prior-score-date}/` directory unchanged.
- **Do not skip the two-pass verification.** Even for a patch that "obviously won't change anything." That's exactly when silent SHA shifts hide.
- **If anything fails or is ambiguous, stop and report.** Do not invent a workaround.

---

## The prompt

Everything below the line is the prompt body. Copy from the line break to the end of the *current* `## Pending patches` block (one block per invocation). Do not copy multiple patch blocks in the same agent run.

---

You are applying a single, focused patch to `Health V3/health_operator_v3.py`. Read the entire prompt before touching anything. Do not apply more than one patch in this run.

## Authoritative docs

Before doing anything, read:

1. `Health V3/README.md` §6.6 Determinism and Reproducibility — the contract you are protecting.
2. `Health V3/CHANGELOG.md` top entry — the prior canonical's SHA, distribution, and floor cohort.
3. The specific lines named in the patch block below — to confirm the current code matches what the patch description claims.

## Step 1 — Capture the baseline SHA

The current canonical SHA (V3.2.12, score date 2026-05-13) is:

```
b48e3a5f7354ee8d769b764e24ca6195a2424ec5f1416891da9877d6011efcb8
```

Verify this matches `Health V3/runs/2026-05-13/client_health_scores_2026-05-13.csv` before proceeding:

```bash
shasum -a 256 "Health V3/runs/2026-05-13/client_health_scores_2026-05-13.csv"
```

If the live file does not match the baseline SHA, **stop and report.** Something has drifted independently of this patch and must be resolved first.

## Step 2 — Apply the patch

Apply *only* the change described in the patch block at the bottom of this prompt. Do not refactor adjacent code, do not "clean up while you're in there," do not adjust formatting outside the touched lines.

## Step 3 — Two-pass cache-mode verification

Run the operator twice with identical arguments against the existing cache. Use a scratch output directory so the canonical run output is not overwritten.

```bash
cd "Health V3"

.venv/bin/python3 health_operator_v3.py \
  --mal "inputs/master_account_list_2026-04-14_canonical.csv" \
  --score-date 2026-05-13 \
  --cache --cache-dir "cache/2026-05-13" \
  --output-dir "/tmp/health_v3_patch_run_a"

.venv/bin/python3 health_operator_v3.py \
  --mal "inputs/master_account_list_2026-04-14_canonical.csv" \
  --score-date 2026-05-13 \
  --cache --cache-dir "cache/2026-05-13" \
  --output-dir "/tmp/health_v3_patch_run_b"

shasum -a 256 \
  "/tmp/health_v3_patch_run_a/2026-05-13/client_health_scores_2026-05-13.csv" \
  "/tmp/health_v3_patch_run_b/2026-05-13/client_health_scores_2026-05-13.csv"
```

## Step 4 — Branch on the SHA result

Exactly one of three branches applies. Do not try to push through if you are unsure which.

### Branch A — both runs match each other AND equal `b48e3a5f…`

The patch is SHA-neutral. This is the expected outcome for comment-only, dead-code, metadata-template, and narrative-wording-with-no-output-change patches.

Proceed to Step 5 and write a "scoring math and canonical SHA unchanged" CHANGELOG entry. Bump the patch version (e.g., V3.2.12 → V3.2.13).

### Branch B — both runs match each other but differ from `b48e3a5f…`

The patch changed the canonical output deterministically. This is acceptable *only* if the patch description explicitly anticipated it (each patch block flags whether an SHA change is expected/possible).

Required before proceeding:

1. Diff the two CSVs against the prior canonical and identify exactly which orgs and which columns changed.
2. Confirm the change set is consistent with the patch description (e.g., a `build_domain_map` tiebreaker should only shift orgs whose domains had ties).
3. Recompute the distribution table from the new CSV. Note any band shifts.
4. Write a full canonical-refresh CHANGELOG entry following the V3.2.2 exemplar (distribution table with delta, band changes with drivers, composite shifts ≥ 5pts with drivers).

If the change set does *not* match the patch description, **stop and report.** A silent expansion of scope is a bug.

### Branch C — the two runs differ from each other

Determinism has broken. **Stop immediately.** Do not bump versions, do not write a CHANGELOG entry, do not move artifacts. The patch has introduced non-determinism (most likely: dict iteration order, set iteration order, or a wall-clock dependency). Report:

1. The two SHAs.
2. A column-by-column diff of the rows that differ between the two runs.
3. Your hypothesis for the source of non-determinism.

## Step 5 — Document and ship (only if Branch A or B cleared)

1. Bump `README.md` "Version" line to the new patch version.
2. Bump `METHODOLOGY.md` "Version" and "Last Updated" lines.
3. Add a new entry at the top of `CHANGELOG.md` with the appropriate level of detail (terse for Branch A, full canonical-refresh shape for Branch B).
4. If Branch B: move `runs/{score-date}/` → `_archive/runs/v{prior-version}_{score-date}/` and re-run the operator with `--output-dir "runs/{score-date}"` to produce the new canonical in place. Update the dashboard footer: locate the footer SHA line with `grep -n "SHA-256:" dashboards/health_dashboard_*.html`, then replace the old truncated SHA with the new one (first 8 hex chars + `…`) and update the version label to the new version.
5. Remove the patch block you just executed from this prompt file (`OPERATOR_PATCH_PROMPT.md`) — it has shipped and should not be re-run.
6. Run `.venv/bin/python3 check_consistency.py` from `Health V3/` after all doc edits. Exit code must be 0 (one informational [NOTE] from Invariant 5 is acceptable if the patch was SHA-neutral and the dashboard wasn't regenerated). If any check fails, halt — the patch is not yet consistent.

Do not skip step 5. A shipped patch block left in the queue is a re-run hazard.

## Hard constraints (restated)

- One patch per run. No bundling.
- Do not touch anything outside the lines named in the patch block.
- The two-pass SHA check is required, not advisory.
- If the patch fails any branch's expectations, stop and report. Do not "fix forward."

---

## Pending patches

Each patch block below is a self-contained work unit. Copy the prompt body above plus *one* patch block when handing this to a fresh agent.

When a patch ships, remove its block from this file (Step 5.5).

---

## Deferred patches — do not apply yet

These are real fixes the audit identified, but they should not be applied as standalone patches because they would either change the cache schema or be redundant with imminent work. They are listed here so they are not lost.

(No patches currently deferred.)
