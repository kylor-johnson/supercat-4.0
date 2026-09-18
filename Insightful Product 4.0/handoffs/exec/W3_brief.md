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

## Three symptoms the owner saw on screen (added 2026-09-18)

Phase 4's G4 review surfaced three complaints that all trace back to these
constants. **They are the reason this phase matters — treat them as the
acceptance test, not as extras.** Owner's words: *"the numbers don't really
stand out or pop like Sarreid's."*

### S1 — the whole month is a $7–12K play on a $41.2M company

hfg's "Do this month" is one play: *"One dealer already buying the top custom
fixture has never ordered Axis; the estimated upside is $7K–$12K, DIRECTIONAL,
on a single door."* That is 0.02% of the year presented as the month's work.

`fact_bundles.build_plays_from_gather` applies **no materiality floor at all** —
it renders a cross-sell play at `gap_count = 1`. A temporary hero-only floor of
3 dealers sits in `_macros.md.j2` (`hero_finding`, cross_sell branch); **replace
it with the size-scaled version and delete the stopgap.**

A play that cannot clear the floor should not be padded — "no play qualified
this month" is a legitimate, honest output and the template already supports it.

### S2 — four coaching cards reading `$1K at risk`, one of them on a GROWING account

hfg ships five cards; four say **`$1K AT RISK`**. Card 1 is worse than
immaterial — it is wrong in kind:

> *"Rep CANOREP's flagged book is about $22K of near-term risk, and it sits on a
> $602K account that is actually pacing up (about $19K of half-over-half gain).
> Treat it as coverage maintenance."*

A **risk** card about an account that is **growing**. Two defects in one:

- **Materiality** — `REP_ATRISK_MIN_DOLLARS = 20_000` gates the *signal*, but the
  cards render from `bundle.rep_risks` and never consult it. Give the card the
  same size-scaled floor.
- **Consistency** — Phase 4 established ONE definition of "needs attention"
  (`gather.account_needs_a_call`) now driving the call list, the watchlist, the
  hero at-risk card and the footer. **The coaching cards are the fourth surface
  and were missed.** A rep whose flagged accounts are all growing should not
  produce a risk card.

Do the consistency half even if the materiality half needs owner numbers — they
are separable.

### S3 — the hero calls a contracting base "roughly flat"

hfg's hero: *"Your existing accounts are spending **roughly flat** vs. prior
year."* Section 5 of the same report: *"Growing accounts added $9.7M while
shrinking and lapsed ones handed back **$16.5M** … **1,080** prior-year accounts
went dark. **Do not read a flat-looking year as reorder strength.**"*

The hero softens the report's own headline finding. The cause is a constant plus
a measure choice, both in scope here:

- `section_01_hero.md.j2` branches on `same_base_lift_pct < -5` to decide
  "spending less" vs "roughly flat". hfg is **−2%**, so it gets "roughly flat".
- But `nrr_pct` says **$0.84 for every $1 — a 16% contraction in retained
  dollars.** Two measures of one concept, disagreeing by 14 points, and the hero
  leads with the gentler one.

**Decide which measure the hero leads on and at what threshold**, and put both
in the calibration table. If a same-dealer base handing back $16.5M is not
"spending less", the threshold is wrong. Note this is also a T1-5
named-quantity risk: two numbers, one claim.

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
- **S1:** plays carry a size-scaled materiality floor; the hero-only stopgap of 3
  in `_macros.md.j2` is removed; "no play qualified this month" is reachable.
- **S2:** coaching cards honour the same floor **and** the same
  `account_needs_a_call` definition the other four surfaces use — no risk card
  for a rep whose flagged accounts are all growing.
- **S3:** a recommendation on which same-dealer measure the hero leads with and
  at what threshold, with hfg (−2% lift vs $0.84 NRR) in the table.
- The owner can read hfg end to end and not hit an immaterial or
  self-contradictory claim.

## Scope

**In:** `pipeline/signals.py`, `pipeline/fact_bundles.py`, `pipeline/templates/_macros.md.j2` and `section_01_hero.md.j2` (S1/S2/S3 only), `pipeline/availability.py` if a card gate moves, `tests/**`, `handoffs/exec/W3_evidence.md`, `AUDIT_FINDINGS.md`.

**Out:** `config/golden_set.json` (reviewer-only), LIVE SQL in `foundation/**` /
`operators/**`, `pipeline/cache/**`, `outputs/*_prose_*.json` (authored client
inputs), `pipeline/templates/**` and `report_render/**` unless a template reads
a constant directly, and anything outside `Insightful Product 4.0/`.

**Do not** enable `validate_slot` on the prose-file path (Phase 8 — it rejects
`$1` from the phrase "for every $1"; `AUDIT_FINDINGS.md` §7).

**Phase 4 left one rule you must reuse, not re-invent:**
`gather.account_needs_a_call(account)` is the single definition of "this account
has actually slipped". The call list, the watchlist, the hero at-risk card and
the call-list footer all read it. S2 makes the coaching cards the fifth. Do not
add a sixth definition.

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
