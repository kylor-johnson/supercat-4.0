# W3 — Phase 5: de-Sarreid the signal constants

> **Open a FRESH Claude Code session in `~/repos/supercat-4.0` with this prompt:**
>
> `Read "Insightful Product 4.0/handoffs/exec/W3_brief.md" and execute it. Work on branch exec/W3. Do not touch anything outside the scope list.`

**Read first:** `AUDIT_FINDINGS.md` §2.1 and §10 · `EXECUTION_PLAN.md` (stamp protocol).

**No VPN, no Postgres, no API key.** Everything runs from `pipeline/cache/` in ~10s.
Pin `--date` on every run; `tools/cohort.conf` holds the org→date map.

```bash
cd "Insightful Product 4.0"
make check          # pytest + golden (11/11) + cohort diff — ALL GREEN today
```

---

## The problem, quantified

`pipeline/signals.py` gates every detector on **absolute dollar constants**
calibrated on Sarreid, a $15.8M client:

```python
DECLINE_PACE_THRESHOLD    = 0.6        # recent < 60% of prior = real decline
DECLINE_MIN_LTM_DOLLARS   = 50_000     # "only fire for material accounts"
CADENCE_CLIFF_GAP_MULTIPLIER = 2.0
GROWTH_POCKET_MIN_YOY_PCT = 20.0
GROWTH_POCKET_MIN_DEALERS = 10
NEW_LINE_MIN_REVENUE      = 100_000
NEW_LINE_MIN_DEALERS      = 5
LIFT_CONC_TOP5_THRESHOLD  = 60.0
REP_OVERPERFORM_MIN_YOY   = 30.0
REP_UNDERPERFORM_MAX_YOY  = -20.0
REP_ATRISK_MIN_DOLLARS    = 20_000
CHANNEL_CONC_THRESHOLD    = 70.0
ECAT_MINORITY_THRESHOLD   = 15.0
LEAKAGE_LOW_THRESHOLD     = 3.0
SECOND_YEAR_RETURN_THRESHOLD = 0.50
```

What `DECLINE_MIN_LTM_DOLLARS = 50_000` actually means across the cohort:

| org | LTM invoiced | $50K as % of LTM |
|---|---|---|
| cci | $70.02M | **0.07%** |
| clc | $58.93M | 0.08% |
| hfg | $41.17M | 0.12% |
| bri | $21.25M | 0.24% |
| **sarreid** | **$15.77M** | **0.32%** ← where it was tuned |
| kal | $8.76M | 0.57% |
| ali | $7.34M | 0.68% |
| bmc | $6.94M | **0.72%** |

**A 10× spread in what counts as "material."** On hfg the watchlist is 10
accounts against a 2,422-dealer base; on a $3M client the same floor would
surface nothing at all. This is the overfit this whole programme exists to undo,
and it is the largest remaining lever.

Not every constant is wrong. **A ratio is already size-neutral** —
`DECLINE_PACE_THRESHOLD` (0.6), `CADENCE_CLIFF_GAP_MULTIPLIER` (2.0),
`GROWTH_POCKET_MIN_YOY_PCT`, the two rep-YoY gates, `CHANNEL_CONC_THRESHOLD`,
`SECOND_YEAR_RETURN_THRESHOLD`. Those may still be mis-tuned, but they are not
*overfit to size*. **The dollar floors and the raw counts are.** Say which
category each constant is in before you touch it.

---

## The job

**Convert size-dependent constants to size-relative ones, and produce the
evidence for choosing the parameters. Do not choose them yourself.**

Recommended shape — keep an absolute floor so a tiny org does not fire on
noise:

```python
threshold = max(ABSOLUTE_FLOOR, PCT_OF_LTM * posture.inv_ltm_net)
```

A percentile of the org's own distribution is also legitimate where a
distribution exists (e.g. account LTM, item unit price — W1 used
`unit_price_ratio` against the catalog median for P0-7 and that pattern worked).
Use whichever fits each signal, and say why.

### The deliverable is a calibration table

For **every** constant you propose changing, sweep **all 11 orgs × at least 3
candidate parameter values** and report, per org per value:

- how many signals of that kind fire
- what the top-ranked one is (so the owner can see whether it is worth saying)
- whether the org's report outcome changes

Then a recommendation with a one-line rationale each. **False positives matter
more than coverage** — a report that surfaces a $1K "risk" is worse than one
that surfaces nothing, and that failure is already on record (hfg shipped four
`$1K at risk` coaching cards).

### Hard constraint

**W3 proposes; the owner decides.** Do not merge a chosen set of numbers. Land
the mechanism (size-relative formulas, wired and tested) with the **current
behaviour preserved by default** — i.e. pick defaults that reproduce today's
firing pattern — and put the candidates in the evidence file for the owner to
choose from. What counts as material to a CEO is a business judgment.

If that is impossible for a given signal (the mechanism cannot be neutral), say
so explicitly and leave that constant alone.

---

## DoD

- Every constant classified: **size-dependent** (convert) or **size-neutral**
  (leave, and say so).
- Each converted constant has a `max(floor, pct × inv_ltm_net)` form or a
  documented percentile equivalent, reading org size from `RunPosture`.
- Calibration table: 11 orgs × ≥3 candidate values × every converted constant,
  in `handoffs/exec/W3_evidence.md`.
- **`make check` green with the defaults you ship** — golden `PASS (11/11)`,
  cohort no-change. A green cohort proves the mechanism is neutral; the owner's
  chosen values will move it deliberately, later, with a re-stamp.
- Unit tests covering: a small org and a large org reaching the same *relative*
  threshold; the absolute floor still binding on a tiny org; and a
  `commerce_confidence = NONE` org (`inv_ltm_net = 0`) not dividing by zero.
- `AUDIT_FINDINGS.md` §2.1 updated to describe the mechanism that now exists.

## Scope

**In:** `pipeline/signals.py`, `pipeline/fact_bundles.py` (only where a play
threshold mirrors a signal one), `tests/**`, `handoffs/exec/W3_evidence.md`,
`AUDIT_FINDINGS.md`.

**Out:** `config/golden_set.json` (reviewer-only), LIVE SQL in `foundation/**` /
`operators/**`, `pipeline/cache/**`, `outputs/*_prose_*.json` (authored client
inputs), `pipeline/templates/**` and `report_render/**` unless a template reads
a constant directly, and anything outside `Insightful Product 4.0/`.

**Do not** enable `validate_slot` on the prose-file path (Phase 8 — it rejects
`$1` from the phrase "for every $1"; `AUDIT_FINDINGS.md` §7).

**Known adjacent item, not yours:** the hero cross-sell carries a temporary
floor of 3 dealers (`_macros.md.j2`, `hero_finding`). Phase 7 replaces it with
the size-scaled version. Leave it.

## Two traps already paid for

1. **`run_report` writes the DRAFT before it fails.** A stale artifact looks
   exactly like a passing run. Delete `outputs/*_DRAFT_*.md` before a
   verification sweep, or read the run's exit code — do not trust the file.
2. **`| first` on an empty sequence RAISES under `StrictUndefined`.**
   Materialise to a list and index it.

## Evidence

`handoffs/exec/W3_evidence.md`: the classification table; the full calibration
sweep; your recommendation per constant with rationale; every verification
command with **real pasted output**; and a self-assessment against each DoD line.
