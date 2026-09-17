# EXECUTION PLAN — Insightful 4.0 remediation

> Evidence base: [`AUDIT_FINDINGS.md`](AUDIT_FINDINGS.md). Read it first.
> Task IDs here are referenced by every worker brief in `handoffs/exec/`.

---

## Operating facts that shape this plan

| Fact | Consequence |
|---|---|
| A full run is **~1.0s**, offline from `pipeline/cache/`; the 11-org cohort is **~10s** | Every gate is "re-run the cohort and diff." Verification is free. Workers need **no credentials**. |
| Output is **byte-reproducible** across venvs, dependency versions, and filesystems | The golden set works; it was only stale. |
| `run.sh` defaults `--date` to **today**, then calls `populate_cache` (needs VPN + Postgres) | **Always pin `--date`.** `tools/cohort.conf` holds the pinned map. |
| Working tree is `~/repos/supercat-4.0` (commit `9855c11`). The iCloud copy is a **trap** | Never edit the iCloud tree. |

---

## The division-of-labor rule

**Reviewer session** — surgical changes where the exact line and rationale are
already established, writing worker briefs, and reviewing/stamping. Handing these
to a fresh session means re-deriving the audit to change six lines.

**Worker session** — tasks needing their own long context (1,600-line file reads,
end-to-end query ports), broad multi-file refactors, or mechanical bulk work.
These burn context the reviewer needs.

**Owner (Kylor) decides, nobody else** — client-facing voice, what counts as
material to a CEO, every threshold constant, and the repo's final shape.

> **iCloud hazard:** this tree is local, but `_museums/` and client assets still
> live in iCloud. Run workers **serially** on this tree. For genuine parallelism,
> clone to a second local path and rebase back — never run two sessions against
> one tree.

---

## The stamp protocol

1. **Reviewer writes the brief** → `handoffs/exec/<TASK-ID>_brief.md`: problem,
   evidence, files in scope, files **out** of scope, Definition of Done, exact
   verification commands.
2. **Owner opens a fresh session** with the one-line prompt in the brief.
3. **Worker produces three things**: branch `exec/<TASK-ID>`, the change, and
   `handoffs/exec/<TASK-ID>_evidence.md` containing — files changed, every
   verification command **with real pasted output**, the per-org cohort delta,
   the golden-core checksum delta **with one line of justification per changed
   org**, and a self-assessment against each DoD line.
4. **Reviewer verifies by running, not by reading claims**:
   ```bash
   git diff main...exec/<TASK-ID>
   ./tools/cohort_diff.sh                      # reviewer's own re-run
   .venv-renderer/bin/python -m pytest tests/ -q
   ./regression.sh --verify
   ```
5. **Verdict**: **STAMP** (merge + append `handoffs/exec/STAMPS.md`) /
   **REWORK** (numbered feedback, same branch) / **REJECT** (brief rewritten).

**A worker may never**: re-stamp the golden set, edit `config/golden_set.json`,
change LIVE SQL bodies, or touch files outside its brief's scope list. Those are
reviewer-only, at a phase boundary, with owner confirmation.

---

## Phases

> **Status 2026-09-17:** Phases 0–2 complete and merged to `main` (`701a635`).
> Cohort **10 SHIP / 1 REDIRECT / 0 fail** (was 8/1/2). Tests 48 → 150.
> `make check` is green. **Next: Phase 3 (W2, characterization tests).**

| # | Phase | Owner | Sessions | Gate |
|---|---|---|---|---|
| ~~**0**~~ | ~~Safety net, baseline, audit record~~ | reviewer | — | **G0 ✅** |
| ~~**1**~~ | ~~P0 shipping defects~~ | reviewer + W1 | — | **G1 ✅** 11 of 12 closed; P0-6 blocked on VPN |
| ~~**2**~~ | ~~Re-freeze golden 4→11~~ | reviewer | — | **G2 ✅** v12, `PASS (11/11)`, `make check` green |
| **3** | Characterization tests on the renderer | **W2** | 1 | G3 — coverage |
| **4** | **Tier-1 insight restoration** | reviewer | 0 | **G4 — owner reads Sarreid + HFG** |
| **5** | De-Sarreid the constants | **W3** | 1 | G5 — owner approves every constant |
| **6** | Per-row rep identity | **W4** | 1 | G6 — HFG names reps |
| **7** | Materiality floors + eCat gate split | **W5** | 1 | G7 |
| **8** | Voice gates: claims not tokens | **W6** | 1 | G8 |
| **9** | BACKLOG query restoration (4 clusters) | **W7–W10** | 4 | G9a–d |
| **10** | Thin-data contract + Conversation Patterns | **W11** | 1 | G10 — Dainolite is the test |
| **11** | Clean-repo extraction, data split, CI | **W12** | 1 | G11 — **owner** verifies no client data |
| **12** | Doctrine reconciliation | reviewer | 0 | G12 |

**Strictly serial:** 0 → 1 → 2 → 4 → 5.
**Parallelizable after Phase 2** (second clone only): Phase 3; each of W7–W10; Phase 11 scaffolding.

> **If you only do Phases 0–4 you get most of the value.** Everything after is
> amplification of a fix that either landed at G4 or did not.

---

## Phase 1 — P0 shipping defects

Bugs, not design debates. Close **before** the golden freeze or the defects get
enshrined. Definitions in `AUDIT_FINDINGS.md` §4.

**Reviewer takes** P0-1 … P0-6, P0-9, P0-11 (surgical; exact lines known).
Each ships with a unit test and its own commit; cohort diff after every one.

**W1 takes** P0-7, P0-8, P0-10 — these need investigation, not a patch:
- **P0-7** — is single-door project concentration detectable generically
  (`dealer_count == 1 AND revenue > 2% of LTM` → a new signal), or does it need a
  profile field? A $2.5M custom project is 6% of HFG's year and goes unnamed.
- **P0-8** — SKU description truncation that survives all 11 catalogs.
- **P0-10** — make the deterministic fallback satisfy §Q hedging at `PARTIAL`.
  This is the v9 safety story; it is currently **untested and broken** at PARTIAL.

**G1** — owner reads regenerated **Sarreid, Hubbardton Forge, Dainolite, and
Kalco** and confirms the defects are gone and nothing new appeared. Copy defects
need a human; tests are not the gate here.

---

## Phase 2 — Re-freeze the golden set

Only now. `./regression.sh --update`, then the reviewer reviews **every** checksum
delta line-by-line against Phase-1 evidence and writes the justification into
`golden_set.json`'s `stamp_verification`.

**2.1 — Expand the freeze 4 → 11 orgs.** Current freeze (`sarreid, cci, da, clc`)
cannot detect Sarreid overfit, because it contains only orgs that behave like
Sarreid. Add `hfg, kal, ali, sca` — the set README calls *"the anti-Sarreid set
Track 4 will re-include after owner sign-off"* — plus `bsc` (**the only coverage
of the correct-refusal path**), `bmc`, `bri`.

**A golden set is a change detector, not a quality certificate.** Freezing HFG in
its current state is not certifying it; it installs a tripwire so Phases 4–7
produce a loud, readable delta on exactly the broken orgs. Phase 1 fixes the
*bugs* first, so what freezes as defective is *design debt* only.

**2.2 — Add a per-org `known_defects` array** to `golden_set.json` so the manifest
**documents** debt instead of blessing it. Phases 4–7 tick items off it.

**2.3 — `make check`** = `pytest && ./regression.sh --verify && ./tools/cohort_diff.sh`.
Every worker brief requires green `make check` before evidence is written.

**G2** — `GOLDEN SET: PASS (11/11)`. From here, red means red.
*"Expected-red is accepted"* is never written in the changelog again.

---

## Phase 4 — Tier-1 insight restoration  ← the phase that answers the question

| ID | Change | Location |
|---|---|---|
| **T1-1** | **Call `signal_summary_set()`** — implemented, correct, zero callers | `run_report.py:254`, `:365` |
| **T1-2** | **Re-key `talking_points` by `bill_to_number`** instead of nulling on reorder | `run_report.py:293` |
| **T1-3** | **Emit hero-card structure as data**, not a matched English string | `section_01_hero.md.j2` → `sections.py:393` |
| **T1-4** | **Decline floor on the call list** — a growing account may never rank onto "do this week" | `gather.outreach_sort_key:84` |
| **T1-5** | **Cross-bundle consistency check** — one named quantity, one value per report | new check in `smoke_check.py` |

T1-1 and T1-4 **will** move the golden core — expected and correct; reviewer
re-stamps with per-org justification.

**G4 — the most important gate in this plan.** Owner reads before/after Sarreid
and before/after HFG. The question is not "did tests pass" but: **does HFG now
open on something a CEO did not know, and does Sarreid read like the July
PREVIEW again?** If no, stop and diagnose — do not proceed to Phase 5.

---

## Phases 5–12 — summary

- **5 — Constants.** Convert `signals.py:140-155` to `max(absolute_floor,
  pct_of_ltm × inv_ltm_net)` or percentile-of-base. W3 **proposes** a calibration
  table across all 11 orgs at three candidate values; **owner picks the numbers.**
- **6 — Per-row identity.** Row-level name decision; org tier survives only as an
  honesty stamp in methodology (*"45 of 58 reps resolve to names"*), never a
  global mute. Largely retires `config/tier_overrides.json`.
- **7 — Materiality + eCat.** Size-scaled floors on every section/card/play.
  Suppress the eCat **ratio** when `feed_completeness ∈ {STALE,
  PROVABLY-INCOMPLETE}`; allow the **subject** everywhere.
- **8 — Voice gates.** `_RE_CAUSAL` fires only on an **unsourced** cause.
  §P drops `cohort`, `motion`, `feed`, and the eCat section restriction.
  **Deliverable:** a mapping table from every rule in `communication_guideline.md`
  to either a mechanical check or an explicit "human-judgment only" marker.
- **9 — BACKLOG queries** (SQL lifted verbatim, never re-authored; each must pass
  *through* the Spine's gates, not around them; `WHAT_ACTUALLY_RUNS.md` updated in
  the same commit). **Only phase needing live DB + VPN.**
  - **W7** `Q-53` ($12.8M), `Q-51` ($33.5M), `Q-52`
  - **W8** `Q-68` ($2.79M), `Q-ORG-DECAY` (cadence-ratio — the signature 3.0 insight)
  - **W9** `Q-61`, `Q-59`
  - **W10** `Q-20`/`Q-21`, and surface `Q-08` (**already LIVE, just has no section**)
- **10 — Thin data.** Replace the two-variable `_derive_data_mass_tier` with 3.0's
  ten-factor score. Render everything, disclose limits, add the forward line.
  Restore "Patterns That Warrant a Conversation" (questions, not statements).
  **G10: Dainolite is the test case** — 1,115 words today vs 3.0's 7,382.
- **11 — Clean repo.** Fresh `supercat/insightful` under the company org (not
  history surgery on 8,008 files). Product files only; client data to a private
  sibling repo behind an env-var path; one synthetic `example_co` fixture as the
  CI golden and public demo; GitHub Action on `make check`.
  **G11: owner personally runs** `git log -p | grep -iE 'sarreid|hubbardton|currey|kalco|dainolite'`
  against the new repo and confirms it returns nothing.
- **12 — Doctrine.** Re-derive `WHAT_ACTUALLY_RUNS.md` **from the code** (its
  precedence authority comes from being derived; the moment it drifts the whole
  chain is decorative). Reconcile `CANON.md`, `signal_catalog_v4.md`, §P lists.
  **G12:** a fresh session reads `CANON.md` only and correctly predicts pipeline
  behavior on HFG.

---

## Harness reference

```bash
./tools/cohort_run.sh _baseline   # capture baseline   (~10s, offline)
./tools/cohort_diff.sh            # re-run + diff vs baseline — THE gate command
.venv-renderer/bin/python -m pytest tests/ -q
./regression.sh --verify
```

`tools/cohort.conf` pins org→date. `_baseline/` and `_current/` are gitignored
(client text); regenerate in ~10s.
