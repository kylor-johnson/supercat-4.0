# Changelog — Health V3

All notable changes to the Health V3 operator and surrounding artifacts. Newest entries first.






## 3.6.2 — 2026-09-21

**2026-09-01 re-run and folded in. The series is now twelve continuous snapshots with no gap. Canonical unchanged: `2850025eb9de25926e4c633e3d0aed8f39a4010d874cc6e2935b4e176069896e`**

- **2026-09-01 SHA:** `670d8774d097b7dfe6174f36daa402face9545a5719b32f399c3eb26019d8e6b`
- 114 orgs, 0 skipped, bands 53 Thriving / 40 Healthy / 13 Watch / 4 At Risk / 4 Critical
- Two-pass byte-identical. Anchor proven: `max(last_login_at)` = 2026-09-01 23:59:51,
  `min(first_run_at)` = 2026-03-06 (exactly `(D+1) − 180d`), org 1 `logins_90d` = 4789.

`trigger_reports/trigger_report_2026-09-21.csv` regenerated across **12 snapshots —
155 triggers** (13 Immediate / 55 High / 87 Standard). The four-month gap that made
the 3.6.0 report's "month-over-month" deltas misleading is closed.

The run reused the five anchor-independent cache files from the quarantine folder
(verified against their recorded md5s) and re-pulled the five windowed ones with
the corrected anchors, each with a fresh server-side checksum.

### What the anchor error actually cost

Now measurable: **31 of 114 composites changed, mean |Δ| 0.42, max 7.8, and zero
band changes.** Rejecting was right on principle — the offset was real, broad, and
landed on the tightest seam in the series — but no published band or narrative
would have been wrong had it shipped. Recorded in the quarantine README so the true
cost of this class of error is known rather than assumed.

The ghost block was identical across both runs: `today` is `score_date` in either
case and none of the four ghosts had activity near the boundary, so the bug was
confined to the windowed counts.

### Fixed — the verify block passed on the bug it existed to catch

3.6.1 added post-write assertions to `HISTORICAL_RUN_GUIDE.md`. They were
**one-sided** (`max(last_login_at) <= D 23:59:59`), which cannot detect an anchor
that is a day too *early* — the failure mode that actually occurred. The rejected
cache maxed at `2026-08-31 23:59:50` and satisfies that assertion cleanly. Now
two-sided: the value must land **on** `D`, and `min(first_run_at)` is stated as an
exact equality rather than with a `~` that invites an eyeball.

That is the third verification recipe in three releases that did not work as
written — rule 8 twice, now this. Worth noting as a pattern: a check that has never
been run against a known-bad input is not yet a check.

### Fixed — four more defects the re-run surfaced

- **The strongest control was buried as advice.** "Reproduce one already-committed
  month" was the last sentence of the verify block. It is the only check that
  catches a wrong anchor *before* an hour of cache population, and it costs one
  query. Promoted to **Step 0.5**, before Step 1, with the 2026-04-30 org-1 query
  inlined ready to paste and the three wrong answers (6048, 6112) named so the
  failure is self-diagnosing.
- **The upper-bound rule was scoped too broadly.** `WHERE created_at < DATE 'D' +
  INTERVAL '1 day'` sat under the two-anchor table and read as universal, but
  `load_pg_portal_orders` and `load_bq_mp_sharing` anchor at `DATE 'D'` — applying
  it mechanically would widen them by a day and re-create a variant of this bug.
  Now explicitly scoped to the `NOW()` family.
- **`bq_helpscout_fires` was mis-classified as "no date filter".** It filters
  `status IN ('active','pending')` — not an absent filter but one that *cannot be
  back-dated*, so a historical run sees only conversations still open today. Four
  consecutive backfill months produced `support_fire = 0` from a header-only file
  and each agent independently worked out whether they had broken something. The
  guide now states it: this dimension does not backfill, never read a trend off it.
- **The reuse rule existed in two places and they contradicted.** The quarantine
  README said to re-prove a reused file against a fresh server checksum; the re-run
  brief said the opposite. The brief was right — the source drifts, so a re-proof
  fails for legitimate reasons and trains the operator to ignore the check. The rule
  now lives in **Step 1.5**: verify against the recorded md5, record the populate
  window, and for a file that *has* drifted, compare per key bucket and transfer only
  what differs (one agent moved 1 bucket of 32, leaving 4,684 of 4,979 rows
  untouched).
- The snapshot count in the guide is now self-describing — "one per directory under
  `runs/historical/`, plus the live canonical" — after going stale twice.

### Series

| Date | n | Thr | Hea | Wat | Risk | Crit | ghosts |
|---|---|---|---|---|---|---|---|
| 2026-06-01 | 111 | 56 | 33 | 14 | 4 | 4 | 4 |
| 2026-07-01 | 112 | 55 | 35 | 13 | 5 | 4 | 4 |
| 2026-08-01 | 113 | 52 | 39 | 15 | 3 | 4 | 4 |
| **2026-09-01** | 114 | 53 | 40 | 13 | 4 | 4 | 4 |
| 2026-09-21 | 114 | 52 | 40 | 14 | 4 | 4 | 4 |

The four-month-drift conclusion survives the correction intact: mean composite
delta 09-01 → 09-21 is −0.94, median 0.00. The September distribution was already
in place on 09-01, so the large deltas against 2026-05-13 are gradual drift rather
than a final-three-weeks event.

---
## 3.6.1 — 2026-09-21

**Backfill: Jun, Jul and Aug 2026 added. The series is now eleven continuous snapshots. Canonical unchanged: `2850025eb9de25926e4c633e3d0aed8f39a4010d874cc6e2935b4e176069896e`**

The series jumped 2026-05-13 → 2026-09-21, so every "month-over-month" delta in
the 3.6.0 trigger report actually spanned four months. Three backfill months close
that gap. **A fourth, 2026-09-01, was run and rejected** — see below.

| Date | n | Thr | Hea | Wat | Risk | Crit | ghosts | ARR |
|---|---|---|---|---|---|---|---|---|
| 2026-05-13 | 104 | 57 | 31 | 14 | 1 | 1 | 0 | $1,783,181 |
| **2026-06-01** | 111 | 56 | 33 | 14 | 4 | 4 | 4 | $1,911,442 |
| **2026-07-01** | 112 | 55 | 35 | 13 | 5 | 4 | 4 | $1,929,634 |
| **2026-08-01** | 113 | 52 | 39 | 15 | 3 | 4 | 4 | $1,938,622 |
| 2026-09-21 | 114 | 52 | 40 | 14 | 4 | 4 | 4 | $1,973,662 |

All three scored with `--weights equal`, the September MAL, and the pinned
interpreter; each two-pass byte-identical. `check_consistency.py` 9/9.
`trigger_reports/trigger_report_2026-09-21.csv` regenerated across **11 snapshots
— 153 triggers** (was 107 across 8): 14 Immediate / 54 High / 85 Standard.

**The four ghosts were dark the whole time.** `aa`, `bmc`, `blh` and `pol` fire in
every backfill month, so the $83,520 the September run surfaced was not a new
event — it had been invisible since at least June because those orgs were missing
from the April MAL. `days_dark` decreases by exactly the calendar distance in every
month, which independently confirms window anchoring.

### Rejected — 2026-09-01, wrong window anchor

Quarantined at `_archive/rejected/2026-09-01_wrong_anchor/` with its proof and a
list of which cache files are reusable. It used the **literal** reading of the
substitution table below, bounding the window at the *start* of the score date.

The offset is small per-org but broad, and it landed on the one comparison the run
existed to make: 98 of 188 orgs differ on `logins_90d`, **15 on
`active_users_90d`** (which feeds the ratio directly), **101 on `last_login_at`**
(so `days_dark` and potentially `ghost_subtype`), and 3,947 login events on
2026-09-01 itself were excluded. Removing spurious deltas was the entire point of
the backfill, so a one-day-offset snapshot at the tightest seam was not acceptable.

### Documented — the substitution rule, which was wrong and load-bearing

`HISTORICAL_RUN_GUIDE.md` said `NOW()` → `'{score_date}'::date` and specified no
upper bound. **Three of the four agents independently discovered that this does not
reproduce the committed series, and derived the real rule from first principles.**
That is a documentation failure paid for three times over. Now written down:

- **Two anchors, not one.** `NOW()` loaders (`pg_engagement`, `pg_orders`,
  `pg_imports`) anchor at **`DATE 'D' + INTERVAL '1 day'`** — the window includes
  the whole score date. `CURRENT_DATE` loaders (`pg_portal_orders`,
  `bq_mp_sharing`) anchor at `DATE 'D'`. The remaining five have no date filter.
  That one-day disagreement between the two families is a real inconsistency in the
  model, faithfully reproduced by every snapshot; it should be reconciled
  deliberately, never mid-backfill.
- **Proof**, org 1 at the committed 2026-04-30 (`logins_90d = 6028`): the literal
  reading gives 6048, a 91-day window gives 6112, and `anchor = D+1` gives **6028**.
  Re-confirmed on 2026-03-31, 2026-02-28, `pg_imports` run counts, and
  `last_login_at` to the microsecond.
- **An upper bound must be added that the SQL does not contain.**
  `MAX(created_at) AS last_login_at` and `MIN(created_at) AS first_login_at` sit
  *outside* the `FILTER` clauses in `load_pg_engagement`, as do `MAX/MIN` in
  `load_pg_imports`. Substituting only the `FILTER` intervals leaves them
  unwindowed, returning present-day values under a historical label — while
  `logins_90d` still looks correct, so nothing flags it. `first_login_at` drives the
  new-org gate and `last_login_at` drives `days_dark`.
- Verified post-write assertions added, plus an instruction to reproduce one
  committed month exactly before trusting a convention on a new one.

### Fixed — README rule 8 was still incomplete

Rule 8 was added in 3.5.1 after three silent transcription errors. All four
backfill agents found further defects in it:

- **`concat_ws` alone is not enough.** The rule correctly bans `||` (which makes
  NULL-bearing rows vanish), but `concat_ws` *skips* NULL arguments rather than
  emitting an empty field, so `('a', NULL, 'c')` renders `a|c` — indistinguishable
  from a two-column row and never matching the local side. Every column now needs
  `COALESCE(col::text,'')`. All three PG agents hit this and fixed it identically.
- **`ORDER BY line` needs `COLLATE "C"`.** The default collation does not sort the
  same way as Python's byte sort, so the two sides disagree for reasons unrelated to
  the data — which trains the operator to ignore the check.
- **An empty result set has no checksum.** `md5(string_agg(...))` over zero rows is
  `NULL`, so the equality check cannot run. `bq_helpscout_fires.csv` is legitimately
  header-only in most historical months; fall back to row count 0 on both sides and
  separately confirm the source is live, so "no fires open" is distinguishable from
  "broken feed".

### Also observed

- **`login_events` is subject to a rolling purge.** `min(first_login_at)` across all
  258 orgs is now 2025-03-21; caches populated five days earlier show it back to
  2024-11-13. No scoring impact on any current snapshot — every gate-relevant date
  falls inside the retained range — but **`first_login_at` is not comparable across
  snapshots populated at different times**, and a backfill reaching further back will
  silently lose window coverage. Two agents found this independently.
- **`support_fire` is 0 in all three backfill months** because the one open
  fire-tagged conversation in the 09-21 canonical cache closed during the backfill
  window. The signal is populate-time-sensitive to within hours. Five of seven prior
  historical caches are also empty, so this is precedent, not breakage.
- **The re-prove-by-checksum shortcut works.** Rather than re-transcribing the
  4,979-row `pg_domain_map.csv`, agents copied it forward and proved equality against
  a fresh server-side checksum — one did it per first-letter bucket and transferred
  only the single bucket that had drifted. That removes the transcription channel for
  the five anchor-independent files entirely and is worth making standard.
- `ghost_subtype` for `pol` is `lapsed` in Jun/Jul and `dark_12m_plus` in Aug/Sep.
  Correct: its last login (2025-07-16) sits inside the 365-day window until
  2026-07-16. The backfill brief carried the September label backwards without
  recomputing; the operator was right and the brief was wrong.
- `HISTORICAL_RUN_GUIDE.md` stale text corrected — snapshot count, the demoted
  2026-05-13, the April MAL in the worked example, and 8/8 → 9/9.

### Still open

- **2026-09-01 needs a re-run** with the corrected anchor before the series is
  complete. Five cache files are reusable from the quarantine folder.
- The `NOW()` / `CURRENT_DATE` one-day disagreement between loader families.
- Cache population automation — still the largest remaining risk, now with a
  cheap partial mitigation (copy-and-prove-by-checksum) worth writing into the guide.

---
## 3.6.0 — 2026-09-21

**New canonical. The September run is promoted; the standing MAL moves to 114 orgs.**

- **New canonical SHA:** `2850025eb9de25926e4c633e3d0aed8f39a4010d874cc6e2935b4e176069896e`
- **Prior canonical (2026-05-13, V3.5.1):** `a797e95980f7a9dc5fa185dbba51857f9f1bef57074e2a534744376a40207ca8`
- Score date `2026-09-21` · MAL `master_account_list_2026-09-16_canonical.csv` · 114 orgs, $1,973,662 ARR
- `--weights equal`, new-org gate on. Two-pass byte-identical. `check_consistency.py` 9/9.

No engine change. This entry promotes the run that was staged at
`runs/_staged/2026-09-21/` after it cleared two independent verification passes —
a fresh session that had not seen the folder, and a review by the session that ran
the original test. Every finding from both is closed in V3.4.1 / V3.5.0 / V3.5.1.

### Distribution

| Band | 2026-05-13 | 2026-09-21 | Δ |
|---|---|---|---|
| Thriving | 57 | 52 | −5 |
| Healthy | 31 | 40 | +9 |
| Watch | 14 | 14 | 0 |
| At Risk | 1 | 4 | +3 |
| **Critical** | 1 | **4** | **+3** |

Flags: behavioural floor 14 · **ghost 4** · support fire 1 · bundle/config mismatch 0.
`scoring_status = complete` for all 114.

**Read every delta as four months, not one.** The prior snapshot is 2026-05-13 and
the trigger engine treats consecutive snapshots as adjacent regardless of calendar
distance, so the 24 band changes and the ≥15-point moves below span May →
September. They are not a one-month collapse.

Across the 102 orgs common to both snapshots: mean composite −1.22, median −0.75;
57 declined, 39 improved, 6 flat.

### Composite shifts ≥ 15 points, with drivers

| Org | ARR | May → Sep | Δ | Driver |
|---|---|---|---|---|
| `cf` | $7,830 | 40.0 → 75.3 | +35.3 | Value Delivery |
| `kl` | $9,360 | 55.4 → 82.9 | +27.5 | Value Delivery |
| `jc` | $24,029 | 89.6 → 62.4 | **−27.2** | Value Delivery |
| `ol` | $13,380 | 63.8 → 40.0 | **−23.8** | Value Delivery |
| `dccl` | $22,038 | 66.2 → 86.4 | +20.2 | Value Delivery |
| `soi` | $8,700 | 71.7 → 52.9 | −18.8 | Value Delivery |
| `bp` | $15,280 | 60.2 → 78.5 | +18.3 | Adoption |
| `df` | $9,560 | 74.8 → 58.7 | −16.1 | Value Delivery |

Seven of eight are Value-Delivery-driven over a four-month window, which is the
dimension `MAINTENANCE.md` flags as substantially a segment proxy. Treat the
direction as real and the magnitude as partly structural — `jc` and `ol` are the
two worth a CS conversation on the evidence, not the arithmetic.

### Population

**+12** (`aa`, `blh`, `bmc`, `cl`, `cst`, `drf`, `libco`, `mali`, `pebl`, `pol`,
`tcd`, `tcs`) — real paying accounts the April MAL omitted, sourced from live
`subscriptions`. **−2** (`hmjc`, `tel`) — both churned, zero active plans.

**Four of the twelve additions are ghosts**, carrying **$83,520 of at-risk ARR
that nothing was watching**: `aa` $42,480 `never_activated` (no login event in its
entire history against six months of billing), `bmc` $21,720 `lapsed` (dark 291d,
live since 2011), `blh` $10,620 `lapsed` (dark 227d), `pol` $8,700 `dark_12m_plus`
(dark 431d). The first ghost cohort in the program's history, and the single
strongest argument for the MAL refresh.

### Triggers

`trigger_reports/trigger_report_2026-09-21.csv` — 107 triggers across 8 snapshots,
10 Immediate / 34 High / 63 Standard. All five `new_ghost` rows band Critical
(`prog` at 2025-11-30 plus the four September ghosts). Generated after promotion,
so no `--production-csv` override is needed.

### Archive and layout

RUN_PROMPT step 5.3 said to move the prior canonical to `_archive/`. **That would
have broken the series** — `_archive/` is excluded from the trigger engine, so
retiring May there would have left a Nov→Apr + Sep sequence with the May snapshot
invisible to month-over-month detection. The prior canonical is instead demoted
into the historical series, which is what `runs/historical/` is for:

- `runs/2026-05-13/` → `runs/historical/2026-05-13/`
- `cache/2026-05-13/` → `cache/historical/2026-05-13/`
- `trigger_reports/trigger_report_2026-05-13.*` → `trigger_reports/_archive/`
- `dashboards/health_dashboard_2026-05-13.html` → `_archive/dashboards/…_v3.5.1.html`

SHAs verified identical pre- and post-move. **RUN_PROMPT step 5.3 is corrected**
so the next run demotes rather than archives. `runs/historical/` now holds eight
months, Nov 2025 → May 2026.

### Dashboard

`dashboards/health_dashboard_2026-09-21.html` — 114 rows, 30 columns, footer
`2850025e…`, V3.6.0. The May dashboard is archived rather than left beside it, so
`check_consistency.py` Invariant 5 resolves against one live dashboard.

---
## 3.5.1 — 2026-09-21

**Closes everything found by an independent verification pass. Live canonical: `a797e95980f7a9dc5fa185dbba51857f9f1bef57074e2a534744376a40207ca8`**

V3.5.0 was verified by a fresh session that had not seen the folder, and separately
reviewed by the session that ran the original test. Both passes confirmed all five
earlier fixes. Between them they found three real defects — one of them in the
column V3.5.0 added to prevent exactly that class of problem — plus six
documentation errors. All are fixed here. No composite score and no band moved.

### Fixed — `ops_measurement` did not mean what it said

The flag was `"full" if imp_score is not None`, ignoring freshness entirely, while
README §6 and the code's own comment both claimed "all three ops sub-signals
contributed." Three orgs were labelled `full` with `freshness_score = None`:
`cl` (ops 80), `ihm` (ops 100), `tl` (ops 60).

Because `clean_ops_dark` gates on this flag, the suppression V3.5.0 shipped leaked:
`cl` published *"Corbett Lighting's data infrastructure is healthy… The
infrastructure isn't the problem"* at ops 80 with the cadence signal unmeasured and
an ops narrative that disclosed nothing. **The mechanism added to stop the false
infrastructure claim was itself making a smaller version of it.**

Now requires `imp_score is not None and fresh_score is not None`. `catalog_only`
goes 7 → 10 orgs (adds `cl`, `ihm`, `tl`); `cl` drops into the standard
behavioural-floor narrative. Also verified that `pw` at 2026-02-28 keeps
`clean_ops_dark` legitimately — 4 healthy feeds with freshness present.

### Fixed — the staged trigger report contradicted the run it described

`runs/_staged/2026-09-21/trigger_report_2026-09-21.csv` was a V3.4.0-era artifact,
timestamped nine minutes before the scores CSV it described. All five `new_ghost`
rows read `band_now = At Risk` and `ol` still carried the healthy-infrastructure
claim — **both defects V3.4.1 and V3.5.0 closed were still live in the artifact CS
actually works from**, inside the folder proposed for promotion. Regenerated: 107
triggers across all 8 snapshots, ghosts Critical, narrative corrected.

### Fixed — `--history-dir runs/_staged` was a silent no-op

`NON_CANONICAL_SUBTREES` is applied to explicitly-named directories too, so naming
a staged directory contributed nothing and the engine said nothing — it reported 7
snapshots and 78 triggers with the staged month simply absent. That produced a
confidently wrong answer during verification. The engine now warns when a named
`--history-dir` yields zero snapshots and names the remedy; `--history-dir` help
text and `runs/_staged/README.md` both say it is unconditional.

### Renamed — `ghost_subtype` labels misled on three of four ghosts

`lapsed_this_quarter` was attached to orgs dark **291 and 227 days** — nine and
seven months. `no_activity_12m` invited "never activated" for `pol`, which has 200
logins behind it and is a win-back, not a go-live problem. On the only populated
bucket the routing was wrong half the time.

The never-activated discriminator was **already in the cache** as a NULL
`first_login_at`, so this needed no new column and no cache-contract change —
contrary to V3.5.0's note claiming otherwise.

| Old | New | Condition | September |
|---|---|---|---|
| `no_activity_12m` | `never_activated` | `first_login_at` is NULL | `aa` |
| `no_activity_12m` | `dark_12m_plus` | has logged in, `active_users_365d = 0` | `pol` (431d) |
| `lapsed_this_quarter` | `lapsed` | active within 365d, none within 90d | `bmc` (291d), `blh` (227d) |

`ghost_account_note` now carries exact days-dark (`dark 291d`), so urgency comes
from the number rather than the bucket.

### Fixed — a genuinely new account would have been called churn

§5.1 outranking the new-org gate (V3.5.0) is right, but the rule is blind to *why*
there are no logins. An account signed six weeks ago, above the $5k threshold, with
reps not yet invited, matches the ghost condition exactly — and got *"urgent churn
risk that needs an immediate conversation with the client."* That is the false
positive the gate existed to prevent, now unreachable for any account above $5k.
Nothing has that shape today; it fires the first time a T1/T2 account onboards
across a run boundary.

The ghost narrative is now subtype-aware: `never_activated` reads *"Confirm whether
this account has actually gone live before treating it as churn"*, and
`dark_12m_plus` says "in over a year" rather than "in the last 90 days". The
thorough fix — exempting orgs whose earliest `pg_imports.first_run_at` is under 90
days old — is deferred; it changes no current row.

### Fixed — operator crashed when every org was skipped

`KeyError: 'health_band'` on the empty frame. `skipped_new_orgs.csv` is written
first so nothing was lost, and it cannot happen in a real run, but it buried the
cause in a traceback. Now warns and returns cleanly.

### Documentation

- **`ENVIRONMENT.md` — all three rows of the environment-of-record table were
  wrong**, in the file whose purpose is preventing SHA confusion, directly above
  its own note boasting of having just fixed that class of error. It named
  `6a2f1d9f…` as live (that was V3.4.1, and is *also* the archived unweighted
  operator's output on this interpreter — one SHA, two roles), `6dc304ea…` for
  September (two versions stale), and claimed `e34552ab…` was "still reproducible
  here" (V3.5.0 broke that; the actual v330 output is `e98f11a4…`). Rebuilt as a
  six-row table with an explicit status column.
- **New Invariant 9** pins `ENVIRONMENT.md` against the live canonical SHA. That
  table had gone stale twice with nothing to catch it — Invariant 2 only checks the
  top CHANGELOG entry. `check_consistency.py` is now 9 invariants.
- **README rule 8 rewritten — the checksum recipe had a flaw that hid corruption
  in the rows that matter most.** It used `col1 || '|' || col2`, and in Postgres
  `a || NULL` is `NULL` while `string_agg` skips NULLs, so **any row with a single
  NULL column vanishes from the checksum entirely**. 70 of 258 `pg_engagement` rows
  carry a NULL, and `first_login_at`/`last_login_at` are NULL for exactly the
  zero-login orgs — so `aa`, the highest-ARR ghost in the book, was the one row the
  check could not see. Verified live: a three-row table with one NULL checksums two
  rows under `||`, three under `concat_ws`. The rule now mandates `concat_ws`,
  `ORDER BY line` (so a row-position swap is a no-op and a value swap between rows
  is caught — the original `ORDER BY <key>` was ambiguous at exactly that point),
  explicit numeric/timestamp normalization, and recording per-file md5s in
  `run_metadata.md`.
- `README.md` §4 headline said ops is the "average of three sub-signal scores"; the
  code averages only those that could be measured. Corrected, with the
  `catalog_only` case named at the headline rather than 80 lines later.
- `README.md` §4 now states that **`catalog_only` is an asymmetric warning**:
  `catalog_only` + high ops is weak evidence, but `catalog_only` + low ops is fully
  trustworthy (`dals` at ops 20 on a 33% catalog is a blocker either way). A
  consumer that discounts ops wherever the flag is set would discard a real finding.
- `RUN_PROMPT.md` Step 5.5's stale-path sweep grepped `Health\ V3/` while every
  other command runs from inside `Health V3` — it errored and exited 0, silently
  passing having checked nothing.
- `runs/_staged/README.md`: pointed at `run_metadata.md` for the transcription-error
  provenance, which never contained it (only CHANGELOG 3.4.1 does); listed five
  items under "three blockers"; and did not say the `_staged` exclusion is
  unconditional. All corrected, with the working trigger-engine invocation.

### Known, deferred

- **A `catalog_only` org can still carry ops 100 into the composite at full
  weight.** `ops_measurement` makes it detectable, not corrected. Every
  `catalog_only` org today is ghost- or floor-capped, so no composite carries an
  unearned 100; the exposure is a `catalog_only` org with healthy engagement and no
  override, which nothing currently is. Candidate fix is capping `catalog_only` ops
  at the top of Healthy (~75–79) rather than blanking — it moves composites only
  where the number overstates. Needs its own version bump and a delta study.
- **Lifetime login counts.** One unwindowed `COUNT(*)` in `load_pg_engagement`
  would make `dark_12m_plus` exact rather than windowed. Deferred until the cache
  contract changes for another reason.
- **§9 remains ungated** — 11 outcome labels against a 30-outcome threshold.
- **Cache population has no automation**, and is the source of the only silent
  corruption this program has seen.

### Regeneration

| Run | V3.5.0 | V3.5.1 |
|---|---|---|
| 2025-11-30 | `4954b41c…` | `4d55f899…` |
| 2025-12-31 | `f31ee3e2…` | `2f25ff38…` |
| 2026-01-31 | `1c1a173a…` | `c490040c…` |
| 2026-02-28 | `5d4abcf3…` | `fbb84877…` |
| 2026-03-31 | `b688f7da…` | `d2f7b545…` |
| 2026-04-30 | `969ab5c9…` | `5365fc34…` |
| **2026-05-13 (canonical)** | `a5d8cb28…` | **`a797e959…`** |
| 2026-09-21 (staged) | `9fc4b519…` | `2850025e…` |

May distribution unchanged: 57 Thriving · 31 Healthy · 14 Watch · 1 At Risk · 1
Critical. September staged unchanged: 52 · 40 · 14 · 4 At Risk · 4 Critical.
Dashboard regenerated. `check_consistency.py` 9 pass / 0 fail.

---
## 3.5.0 — 2026-09-21

**Closes the three open findings from the end-to-end test run. Schema grows by two columns, so every SHA in the series moves. No composite score and no band changed anywhere.**

- **New canonical SHA:** `a5d8cb289f0ae945efc1636453bfd8f4f3ffe316417dde2011d7ab8f5bc5b73d`
- **Old canonical SHA (V3.4.1):** `6a2f1d9fc6c86ae58a6888386f83b0a9122ecc98cb5ae6f2195e89a8d4dd1bff`
- Canonical CSV 28 → 30 columns; formatted CSV 20 → 22.

### New columns

| Column | Values | Purpose |
|---|---|---|
| `ghost_subtype` | `no_activity_12m` / `lapsed_this_quarter` / null | Splits the two ghost populations §5.1 cannot distinguish |
| `ops_measurement` | `full` / `catalog_only` | Whether all three ops sub-signals contributed |

### Fixed — the new-org gate was inert, and repairing it alone would have been worse

`load_pg_engagement` LEFT JOINs `organizations`, so an org with no logins gets
`first_login_at = NULL` → `NaT`. The gate tested `if first_login is not None`,
and **`NaT is not None` is `True`**, so the `cohort_year` fallback was dead code
in cache mode, the subtraction yielded `nan`, and `nan < 90` is `False`. **No org
had been excluded for having zero logins since V3.0.** Now `pd.notna()`.

Fixing only that would have skipped `aa` — $42,480 ARR, zero logins in its entire
history, current-year cohort — removing the worst account in the portfolio from
the scorecard. So it ships with **§5.1 taking precedence over the gate**: the
ghost condition is now evaluated *before* the gate and a ghost is never skipped as
an onboarding-window org. A paying account with zero logins is never merely new.

- `health_operator_v3.py`: `ghost` computed ahead of the gate and reused by the
  override; `pd.notna(first_login)`; `cohort_year` comparison guarded against NaN.
- `README.md` §"New-Org Exclusion" rewritten — both conditions stated, the bug and
  its five-month reach recorded, and the pairing explained.

### Fixed — ops reported silence as health

With no import feed in the 180-day window, the import-health and freshness
sub-signals are both `None` and the dimension rests on catalog completeness alone.
The per-dimension narrative was honest, but the `clean_ops_dark` composite shape
escalated it to *"data infrastructure is healthy… the infrastructure isn't the
problem"* — about orgs whose feeds have **never run**. Absence of measurement
reported as positive evidence, inside the one sub-shape whose job is to rule
infrastructure out. 7 of 114 orgs have this shape in the September run, and **all
four ghosts are among them**, so it was concentrated in the worst accounts.

The score is deliberately **not** blanked — a poor catalog is a real ops finding
(`dals` sits at ops 20 on the same shape) and blanking would flip those orgs to
`scoring_status = partial` and move their composites. Instead:

- `ops_measurement` records `full` vs `catalog_only`.
- The ops narrative states that import health and freshness are unmeasured and
  that the score reflects catalog completeness only.
- `clean_ops_dark` now additionally requires `ops_measurement == "full"`.
- Observed effect: `ol` and `hvl` drop out of `clean_ops_dark` into the standard
  behavioural-floor narrative. The false infrastructure claim is gone; their
  scores are unchanged.

### Added — `ghost_subtype`, because §5.1 conflated two populations

The condition is ARR + zero 90-day logins, blind to history. In the September run
`aa` (zero logins ever) and `bmc` (live since 2011, thousands of logins behind it,
now at zero) carried the same flag, the same 20.0 and the same band while needing
opposite CS plays.

| Subtype | Condition | September |
|---|---|---|
| `no_activity_12m` | `active_users_365d = 0` | `aa`, `pol` |
| `lapsed_this_quarter` | active within 365d, none within 90d | `bmc`, `blh` |

Routing signal, not severity — both still cap at 20 and band Critical. **Twelve
months is a proxy for lifetime history**, which `pg_engagement` does not carry, so
an org dark longer than a year reads as `no_activity_12m` even if once active
(`pol`, 200 lifetime logins, dark 432 days). Adding lifetime counts would break
the existing cache contract; deferred.

### Regeneration and impact

All seven canonical snapshots and the staged September run were rescored. Only two
kinds of cell changed anywhere: the two new columns, and
`operational_health_narrative` for `catalog_only` orgs.

| Run | V3.4.1 | V3.5.0 |
|---|---|---|
| 2025-11-30 | `e818042b…` | `4954b41c…` |
| 2025-12-31 | `9f4fb466…` | `f31ee3e2…` |
| 2026-01-31 | `649c0275…` | `1c1a173a…` |
| 2026-02-28 | `842c6289…` | `5d4abcf3…` |
| 2026-03-31 | `c2e1ee64…` | `b688f7da…` |
| 2026-04-30 | `f23d12aa…` | `969ab5c9…` |
| **2026-05-13 (canonical)** | `6a2f1d9f…` | **`a5d8cb28…`** |
| 2026-09-21 (staged) | `592c1bdb…` | `9fc4b519…` |

- May distribution unchanged: 57 Thriving · 31 Healthy · 14 Watch · 1 At Risk · 1 Critical.
- September staged: 52 · 40 · 14 · 4 At Risk · 4 Critical. 114 rows, `complete` for all.
- Dashboard regenerated against `a5d8cb28…`; footer reads V3.5.0.
- `--weights v330` no longer reproduces `e34552ab…` — that SHA predates the schema
  change. The v330 *scheme* is still selectable and still produces the V3.3.x
  composites; only the row format differs. Reproducing `e34552ab…` byte-for-byte
  requires a V3.4.x checkout.

### Still open

- **§9 remains ungated** — 11 outcome labels against a 30-outcome threshold.
- **Cache population has no automation.** ~215 KB round-trips through an agent as
  text and produced three silent transcription errors in the September run, caught
  only by the rule-8 checksum. A populate script would remove the risk class.
- **agent-factory mirror** is still on V3.3.0 weights and now also lacks both new
  columns and all three fixes.
- The staged September run is still **staged**, not promoted.

---
## 3.4.1 — 2026-09-21

**Two defects found by the first end-to-end test run. Live canonical unchanged: `6a2f1d9fc6c86ae58a6888386f83b0a9122ecc98cb5ae6f2195e89a8d4dd1bff`**

A full pipeline test was run against the September MAL (`master_account_list_2026-09-16_canonical.csv`,
114 orgs, first use) on a freshly populated `cache/2026-09-21/`. The pipeline ran
end to end without a single code change being needed, the May canonical
reproduced bit-for-bit beforehand, and the new run was byte-identical across two
passes. But it was the **first run in the program's history to produce any ghost
accounts**, and that exposed two defects that had been latent since V3.0.

The staged run is at `runs/_staged/2026-09-21/` — verified, deliberately not
promoted. See that folder's `README.md` for why.

### Fixed — ghosts banded At Risk instead of Critical

§5.1 requires `health_band = "Critical"`. `GHOST_CAP` is 20, and 20 is the *At
Risk* floor in `HEALTH_BANDS`, so `band_for_score(20)` returned `"At Risk"` and
the band was never assigned explicitly. The spec has been unmet since V3.0 and
was invisible because no run had ever produced a ghost.

Impact: the test run reported **`Critical: 0` while carrying four ghosts**,
including `aa` at $42,480 ARR with zero logins in its entire history. Any exec
reading the band distribution got a materially false picture.

- `health_operator_v3.py`: the §5.1 override now assigns `band = "Critical"`
  directly. Chosen over lowering `GHOST_CAP` to 19 — the cap is the documented
  score ceiling and shouldn't be tuned to land on a band boundary.
- `README.md` §5.1 now states that the band is assigned directly, not derived
  from the cap, and why a ghost outranks a low-scoring active account.
- Historical impact: exactly one prior snapshot contained a ghost. `prog`
  ($25,200, zero logins) in `runs/historical/2025-11-30/` moves At Risk →
  Critical. That month was rescored; one cell changed, no composite moved.
  - Prior SHA: `e0931bf5664c89f6d2b84414…`
  - V3.4.1 SHA: `e818042bccf0613b2449dd51…`
- The live 2026-05-13 canonical contains no ghosts, so `6a2f1d9f…` is unchanged.

### Fixed — `new_ghost` could never fire for a single-snapshot org

`detect_triggers` opened with `if len(runs) < 2: continue`, and both state-flag
triggers (`new_ghost`, `fire_duration`) sat inside the month-over-month pair
loop. An org whose *first* appearance is already a ghost therefore produced no
trigger at all.

Impact: all four ghosts in the test run arrived with their org and had exactly
one snapshot, so **none of them appeared anywhere in the trigger report** — the
artifact CS actually works from. The single highest-ARR at-risk account in the
portfolio was absent from its own worklist.

- `trigger_engine_v1.py`: state-flag triggers now evaluate per *snapshot*
  rather than per pair, and no longer require an adjacent prior. A state flag is
  not a delta, so "was this org a ghost at its previous observation" stays
  meaningful across a calendar gap. With no prior observation, the flag being
  set *is* the first firing, and the detail line says "on first appearance in
  the series" rather than "fired" so the two cases are distinguishable.
- Month-over-month delta triggers are untouched and still require adjacency.
- Verified additive: the canonical series goes 77 → 78 triggers, the single
  addition being `prog` at 2025-11-30 — a ghost that had been invisible for ten
  months. On the staged September series, 102 → 107 (+5 `new_ghost`). No existing
  trigger changed type, urgency, driver, detail or action.

### Documentation

- `ENVIRONMENT.md`: the environment-of-record line named `e34552ab… --weights v330`
  as the canonical for this interpreter. Written before the V3.4.0 flip and never
  updated — reproducible here, but not the live canonical, which is the exact
  confusion the file exists to prevent. Replaced with a table covering all three.
- `README.md` §"New-Org Exclusion": documents that the zero-login branch is
  **unreachable**. `load_pg_engagement` LEFT JOINs `organizations`, so an org with
  no logins gets `first_login_at = NaT`, and `NaT is not None` is `True` — the
  `cohort_year` fallback is dead code in cache mode, `nan < 90` is `False`, and no
  org is ever excluded for having zero logins. **Not fixed in isolation**: a
  `pd.isna()` correction would remove `aa` from the scorecard, so it must ship with
  giving the ghost override precedence over the gate. Tracked in `MAINTENANCE.md`.
- `README.md` §"How to populate the cache": rules renumbered 6–9. New rule 6 says
  which converter to use — `scripts/to_csv.py` is the only one that emits
  `sample_tags` in the required list-repr form; `mcp_to_csv.py` joins lists with
  `|` and must not be used for `bq_helpscout_fires.csv`. **New rule 8 requires a
  server-side content checksum.** The test run produced three silent transcription
  errors in `pg_domain_map.csv` (a swapped adjacent pair and two mangled domains);
  all three preserved row count and column names, so the existing read-back check
  could not see them, and all three were caught only by checksum. A corrupted
  domain map degrades `support_data_available` for every org, not just its own row.
- MCP server names corrected throughout — `supercat-postgres-vpn` /
  `bigquery-admin`, and no longer "Cursor with…". Sanity-check row counts refreshed
  against the September cache.
- `runs/_staged/README.md` added, describing the staging convention and the
  promotion checklist.

### Known, unfixed — both can move scores, both need a decision

1. **NaT/`None` new-org gate**, paired with ghost-over-gate precedence, per above.
2. **`operational_health_score = 100` for orgs with no import rows.** Ops is then
   computed from catalog completeness alone. The per-dimension narrative is honest
   ("Catalog 100% complete") but the `clean_ops_dark` composite shape escalates it
   to "data infrastructure is healthy… the infrastructure isn't the problem" — for
   an org whose feeds have *never run*. Absence of measurement is being reported as
   positive evidence, inside the sub-shape whose whole job is to rule infrastructure
   out. Seen on `ol` and `hvl`; **all four ghosts share the shape**, so it is
   concentrated in the accounts that matter most.
3. **§5.1 conflates two populations.** The condition is ARR + zero 90-day logins,
   which is blind to lifetime history. In the test run `aa` (0 logins ever) and
   `bmc` (**6,751** logins ever, an org since 2011 that just stopped) carry the
   same flag, same 20.0, same band — and need opposite CS plays. A `ghost_subtype`
   keyed off `active_users_365d` / lifetime logins would separate
   never-activated from went-dark. Spec gap, not a bug.

### Also observed, not defects

- The September MAL surfaced **$83,520 of at-risk ARR that nothing was watching** —
  all four ghosts are orgs the April MAL omitted.
- `pg_orders.csv` schema drift: `cache/2026-05-13/` carries a third column
  `all_orders_90d` that `load_pg_orders` does not emit and no code reads. The
  reference cache and the source of truth disagree; harmless, zero score impact.
- `dccl` bands Thriving at 6% rep activation (10 of 157), on VD and Adoption both
  at 100. Internally consistent, and a clean live example of the
  Value-Delivery-as-segment-proxy effect `MAINTENANCE.md` warns about.

---

## 3.4.0 — 2026-09-16

**Dimension weights reverted to equal (25/25/25/25). Folders consolidated. Canonical SHA changes.**

- **Old canonical SHA (V3.3.x, weighted 25/20/35/20):** `e34552abe2232c630b088465a067c77a39d598cd6979e912717626598edafce9`
- **New canonical SHA (V3.4.0, equal 25/25/25/25):** `6a2f1d9fc6c86ae58a6888386f83b0a9122ecc98cb5ae6f2195e89a8d4dd1bff`
- Two-pass byte-identical determinism confirmed under the pinned interpreter (Python 3.9.6 / pandas 2.3.3 / numpy 2.0.2).

### First, the V3.3.x arc this entry closes

V3.3.0, V3.3.1 and V3.3.2 shipped without CHANGELOG entries, README updates, or
METHODOLOGY updates. What is recoverable from the code and artifacts:

- **V3.3.0 (2026-06-08)** replaced the equal composite with `ENG 0.25 / ADO 0.20 / VAL 0.35 / OPS 0.20`, justified by a four-line code comment: *"Validated against 7-month backfill. VD has strongest churn-separation signal (38pt gap between declining/stable orgs)."* No validation artifact was ever written. `outcomes.csv` was empty, so the README §9 gating test could not have run.
- **V3.3.1 / V3.3.2** left no trace in code. `FOLDER_AUDIT_PROMPT.md` names V3.3.2 as current and references a `roadmap/` directory that does not exist. Both were doc/tooling-only.
- The V3.3.x documentation layer, `trigger_engine_v1.py`, and `roadmap/` were lost — none had ever been committed to git.

### Why the weights are reverted

The §9 validation finally ran, against real outcomes rather than a proxy.
`outcomes.csv` now carries 11 labels sourced from Postgres `subscriptions` and
`login_events` as of 2026-09-16 — four months past the last snapshot: 2 churned
(`hmjc`, `tel`), 5 downgraded, 4 functionally dark. Both schemes were run across
all seven snapshots and scored against them (`runs/_weighting_study/2026-09-16/`).

| Test | equal | v330 | §9 requirement |
|---|---|---|---|
| Forward AUC (6 deaths, 4–10 mo lead) | 0.933–0.992 | 0.904–0.991 | +0.05 improvement |
| Best v330 margin in any month | — | **+0.008** | **FAIL** |
| Deaths caught, every month | 5 of 6 | 5 of 6 | tie |
| First-flag month, all 6 | identical | identical | tie |
| Worklist precision, all 7 months | **higher in 7/7** | lower in 7/7 | — |
| May worklist | 16 orgs | 21 orgs | — |

v330 matched equal on recall and lead time, missed the AUC bar by 6x, and was
less precise in every month — adding ~5 accounts per month to the CS worklist
while catching nothing extra.

**Mechanism.** Value Delivery scores SuperCat-submitted order volume. Per
`02_who_we_serve.md`, Catalog-Focused is 54% of the base and is *defined* by
"100% iPad orders, no eOL" at a median 24 orders/quarter. Weighting VAL up is
therefore a digital-maturity tax, not a health signal: mean composite delta by
bundle ran `Full` +0.68 versus `iPad+Catalog` −2.37. It also contradicts the
LOCKED "selling instrument vs order consummation" doctrine, which forbids
reading low SuperCat-submitted volume as failed adoption.

The decisive case: `abol` (healthy, 169 logins/90d) and `hmjc` (churned) both
have **zero** SuperCat orders. VAL cannot separate them; Engagement can.

Caveat: 6 functional-death events is below §9's 30-outcome gate, so the AUC
comparison is directional. The precision result rests on 16 orgs verified active
today and does not depend on the event count.

### Operator
- `health_operator_v3.py`: hardcoded weights replaced by `WEIGHT_SCHEMES` + `--weights {equal,v330}`. `DEFAULT_WEIGHTS = "equal"`. `--weights v330` still reproduces `e34552ab…` byte-for-byte, so every V3.3.x canonical stays regenerable.
- `composite()` takes the plain-mean path when all available weights are equal. `sum(s*w)/sum(w)` and `sum(s)/n` round differently at a `.x5` boundary; this keeps `--weights equal` bit-identical to the pre-V3.3.0 operator.

### Distribution (104 orgs, 2026-05-13)

| Band | V3.3.2 | V3.4.0 | Δ |
|---|---|---|---|
| Thriving | 56 | 57 | +1 |
| Healthy | 27 | 31 | +4 |
| Watch | 17 | 14 | −3 |
| At Risk | 3 | 1 | −2 |
| Critical | 1 | 1 | 0 |

10 orgs change band ($105,778 ARR). CS worklist 21 → 16. Dimension scores are
byte-identical across the change — only the composite moves. Behavioral floor
(7), ghost (0) and support fire (9) counts unchanged.

### Trigger engine
- `trigger_engine_v1.py` rebuilt from `TRIGGER_ENGINE_V2_PATCH.md` plus the shipped outputs. Reproduces all 75 shipped triggers with zero field mismatches. `CHRONIC_MIN_MONTHS` and three `Immediate` action strings could not be recovered and are marked RECONSTRUCTED.
- **Fixed: mixed-engine comparison.** The shipped engine built history from the unweighted `runs/historical/` CSVs while taking the latest month from the weighted canonical. Four of eleven 2026-05-13 triggers were artifacts — `swc` and `pw` had *zero* change on all four dimensions. The engine now infers each input's scheme and refuses a mixed series without `--allow-mixed-weights`.
- **Fixed: `fire_duration` was dead**, reporting 0 against 4 qualifying cases (`shl` 26d and 39d, `vcg` 18d, `wwjc` 27d at $40k ARR).
- Non-adjacent snapshot pairs are skipped (`prog` is absent Dec–Feb).
- Canonical series excludes `cohort/`, `cohort_v330/`, `_weighting_study/`, `_engine_baseline_v3.2.13/` and `_archive/`.
- Regenerated on the consistent equal series: 77 triggers (was 75). Shipped report preserved at `trigger_reports/_archive/`.

### Dashboard
- `dashboards/health_dashboard_2026-05-13.html`: the embedded `const DATA` blob matched the **unweighted** v3.2.13 canonical while the footer claimed V3.3.2 / `e34552ab…` — it had been rendering unweighted numbers under a weighted label since June. DATA regenerated from the new canonical; footer now reads V3.4.0 / `6a2f1d9f…`.

### Consolidation
- `Health V3 Backfill/` merged in: README, METHODOLOGY, CHANGELOG, `check_consistency.py`, the run guides, `outcomes.csv`, the 7-month backfill and the Aug cohort runs.
- Canonical MAL copied out of the frozen `_museums/Health V2/inputs/` into `inputs/`.
- `_archive/` lineage rescued from iCloud and un-gitignored. The V3.3.x loss happened because none of it was ever committed.

### MAL
- `inputs/master_account_list_2026-09-16_canonical.csv` — 114 orgs, $1.97M ARR. +12 since April (incl. the six Aug cohort orgs), −2 (`hmjc`, `tel`, both churned). Roster and stack derived first-party from `subscriptions` + `mobile_sites`; stack matches the independently-built Aug cohort MAL 6/6.
- **`subscriptions.custom_price` is a mixed-unit field** — `mah` and `kii` are stored at exactly 12x their monthly rate. MRR is carried forward from the April HubSpot-sourced MAL for 102 of 114; PG fills only the 12 April never covered, with an annual→monthly correction on 3. Per-field provenance in `master_account_list_2026-09-16_provenance.csv`.
- Not yet used for a canonical run — the 2026-05-13 canonical still uses the April MAL, as it must.

### Environment
- `requirements.txt`, `.python-version`, `ENVIRONMENT.md` added; README §6.6 rewritten.
- **The determinism guarantee is interpreter-scoped.** The V3.2.13 canonical `b48e3a5f…` no longer reproduces: the *original* v3.2.x operator against its *own* immutable cache now emits `6a2f1d9f…` under Python 3.9.6 / numpy 2.0.2. Across all six historical months the drift is 17 composite cells at ±0.1 and one narrative digit, with **zero band changes**. Cause is float summation order at a `.x5` rounding boundary; the `.venv` that made those canonicals targeted a `python@3.14` that no longer exists. A SHA quoted without its interpreter is not a reproducibility claim.
- Historical runs regenerated under the pinned interpreter so the whole series is self-consistent.

### Tooling
- `check_consistency.py`: `_latest_run_dir` now matches only `YYYY-MM-DD` directories. Consolidation added `historical/`, `cohort/` and `_weighting_study/` under `runs/`, and a plain name sort was selecting `historical` as the latest run, failing four invariants against a file that never existed.

### Out of scope
- README §9 is **not** yet closed. 11 labels is short of the 30-outcome gate; this entry records a directional result that reverts to the documented default, not a completed prospective validation.
- The BigQuery `insightful_product.at_risk_accounts` view is a second, contradictory at-risk model (79 flagged accounts; `segment_classifier` returns 86/35/48 against the stamped 56/28/20). Not reconciled here.

---

## 3.2.13 — 2026-05-13

**Doc-only. Scoring math and canonical SHA unchanged: `b48e3a5f7354ee8d769b764e24ca6195a2424ec5f1416891da9877d6011efcb8`**

### Documentation
- `README.md` §6 output field list: added `composite_narrative` (between `health_band` and `ghost_account`) and `support_fire_days_open` (between `support_fire_notes` and `support_data_available`). Field list now reflects all 28 canonical columns.
- `README.md` §10 Operational Roadmap: rewritten to separate what has shipped (V3.0 scores, V3.1 interpretive narratives, V3.2.x audit arc, V3.2.12 fire-days column) from what is next (trigger detection → save plays) from what is aspirational (churn pattern recognition, requires 12+ months of history). Removed the prior roadmap table whose "V3.2" row described unshipped churn-pattern work under a version label the audit arc had already used.
- `README.md` line 195: removed stale note claiming interpretive narrative is a "V3.1 target" not produced by the V3.0 operator. Interpretive narratives have shipped since V3.1.
- `FRESH_RUN_GUIDE.md`: corrected canonical column count 27 → 28 and formatted column count 19 → 20 (lines 39, 40, 92, 93). Added `python3 check_consistency.py` step to monthly checklist.
- `OPERATOR_PATCH_PROMPT.md` Step 5.4: replaced hardcoded dashboard filename and line number with a `grep -n "SHA-256:"` instruction so Branch B footer updates remain correct after any dashboard rebuild.

## 3.2.12 — 2026-05-13

**New column: `support_fire_days_open`. Canonical SHA shifts; band assignments unchanged.**

Adds an integer-valued, nullable `support_fire_days_open` column to both the canonical and formatted CSVs. Records days since the most recently opened fire-tagged HelpScout conversation, as of `--score-date`. Null for orgs without an active fire flag. `support_fire` was previously a boolean; the age signal was already computed inside `fires_by_org` via `most_recent_open_at` but discarded — three days vs. forty-seven days is a materially different CS conversation, and this exposes that distinction without changing scoring math.

### Operator
- `health_operator_v3.py` lines 1486–1496: support-fire block now derives `support_fire_days_open = (score_date_dt - fire_ts).days` when a fire is active, where `fire_ts = pd.Timestamp(fire["most_recent_open_at"]).replace(tzinfo=None)`. The `tzinfo=None` normalization makes the math safe across both cache mode (timezone-naive timestamps parsed by `_read_cache_csv` with `parse_dates=["most_recent_open_at"]`) and live BigQuery mode (UTC-aware). Null when `support_fire = False`.
- `health_operator_v3.py` line 1515: new key `"support_fire_days_open"` added to the canonical row-dict, positioned between `support_fire_notes` and `support_data_available`.
- `health_operator_v3.py` line 1555: new entry `"support_fire_days_open"` added to `_fmt_cols`, positioned between `support_fire_notes` and `bundle_config_mismatch`. Formatted CSV grows from 19 to 20 columns.
- No scoring math change. No narrative change. No override behavior change. Purely additive informational column.

### Verification
- **Two-pass byte-identical determinism** confirmed at SHA `b48e3a5f7354ee8d769b764e24ca6195a2424ec5f1416891da9877d6011efcb8` under the patched code (`/tmp/health_v3_patch_run_a` vs `/tmp/health_v3_patch_run_b`, same cache, same `--score-date 2026-05-13`).
- **Diff vs V3.2.11**: only structural change is the new `support_fire_days_open` column at position 22. All 27 prior columns retain byte-identical values across all 104 rows. All other column ordering preserved.
- **Column population check**: 9 of 9 orgs with `support_fire = True` have a non-null integer `support_fire_days_open` (range: 7–39 days). 95 of 95 orgs with `support_fire = False` have null `support_fire_days_open`.
- **Old canonical SHA (V3.2.11):** `63148feb319f4dc434d249ecc47ed90df1adc4c19cf5fc36b9d258bbfcea8ddf`
- **New canonical SHA (V3.2.12):** `b48e3a5f7354ee8d769b764e24ca6195a2424ec5f1416891da9877d6011efcb8`

### Distribution (104 orgs scored — unchanged from V3.2.11)

| Band | V3.2.11 | V3.2.12 | Δ | % |
|---|---|---|---|---|
| Thriving | 57 | 57 | 0 | 54.8% |
| Healthy | 31 | 31 | 0 | 29.8% |
| Watch | 14 | 14 | 0 | 13.5% |
| At Risk | 1 | 1 | 0 | 1.0% |
| Critical | 1 | 1 | 0 | 1.0% |

Behavioral floor: 7 (unchanged). Ghost: 0 (unchanged). Support fire flags: 9 (unchanged). Bundle/config mismatches: 3 (unchanged). Zero per-org band transitions vs V3.2.11.

### Out of scope
- No change to the `support_fire`, `support_fire_notes`, or `support_data_available` semantics. The new column is purely additive.
- The HelpScout SQL and `fires_by_org` aggregation are unchanged — `most_recent_open_at` was already collected; only its consumption changed.
- Narrative engine (`_build_composite_narrative` and per-dimension narrative builders) is unchanged. Fire age is recorded as structured data only; surfacing it in narrative is a future task.

---

## 3.2.11 — 2026-05-13

**New tooling: `check_consistency.py`.**

### Added
- `Health V3/check_consistency.py` — stdlib-only script that verifies eight cross-file invariants identified by the V3.2.x audit arc: version coherence, canonical SHA presence in top CHANGELOG entry, CSV header alignment with operator code, absence of stale column-name references (outside `CHANGELOG.md` and archived paths), dashboard footer SHA agreement with live canonical (with version-lag note), formatted-CSV header alignment with `_fmt_cols`, `--score-date` required-arg enforcement, and floor sub-shape name presence in both operator and README §6.5.

### Documentation
- `README.md` §6.6 gains a "Consistency checking" subsection describing the script and its invariants.

### Verification
- Script run against V3.2.11 state: all 8 checks PASS, exit 0. Invariant 5 prints one `[NOTE]` confirming the dashboard footer (V3.2.8) lags the current system version — expected since V3.2.9 and V3.2.10 were SHA-neutral.
- Deliberate-break tests confirmed for Invariants 1, 2, 4, 7: each correctly returns exit 1 with the failing invariant named in the output.
- Canonical SHA unchanged: `63148feb319f4dc434d249ecc47ed90df1adc4c19cf5fc36b9d258bbfcea8ddf` (script is purely additive, no operator code change).

---

## 3.2.10 — 2026-05-13

**Breaking CLI change. `--score-date` is now required.**

### Operator
- `health_operator_v3.py` line 633: `--score-date` no longer defaults to `date.today().isoformat()` (local time). The operator now refuses to run without `--score-date`. Help text updated to reflect that the argument anchors all scoring math and is required for deterministic output.

### Rationale
- README §6.6 makes determinism a core contract. The prior implicit default silently anchored freshness math to the host's local wall-clock date, contradicting the contract. The default was never intentionally used — every documented invocation in the repo and every archived `run_metadata.md` passes `--score-date` explicitly.

### Verification
- Argparse rejection confirmed: invocations without `--score-date` exit 2 with `error: the following arguments are required: --score-date`.
- Canonical SHA unchanged: `63148feb319f4dc434d249ecc47ed90df1adc4c19cf5fc36b9d258bbfcea8ddf`.
- Two-pass cache-mode verification with `--score-date 2026-05-13`: byte-identical to V3.2.9 baseline.

### Migration note
- Any operator caller that previously omitted `--score-date` will now fail at argparse. None exist in the repo. External callers (none documented) must add the argument.

---

## 3.2.9 — 2026-05-13

**Dead-code and stale-comment cleanup. No scoring math or canonical output change.**

### Operator
- `score_adoption()`: removed third return value `bundle_config_mismatch` (always `False`, discarded by caller, computed independently in `main()` at line 1488).
- `load_pg_orders()`: removed unused `all_orders_90d` SQL output column. Existing `cache/2026-05-13/pg_orders.csv` retains the column; pandas ignores it on load. Next live-PG cache repopulate will produce a 2-column `pg_orders.csv`.
- Stale comment at line ~1540 updated: `# Formatted CSV: ... renamed, ...` → `# Formatted CSV: ... reordered for stakeholder readability` (the rename map was removed in V3.2.8).

### Verification
- Canonical SHA unchanged: `63148feb319f4dc434d249ecc47ed90df1adc4c19cf5fc36b9d258bbfcea8ddf`.
- Two-pass cache-mode verification: byte-identical to V3.2.8 baseline.

---

## 3.2.8 — 2026-05-13

**Schema migration — BREAKING CHANGE for downstream CSV consumers.**

Canonical CSV column renames:
- `health_score` → `composite_score`
- `score_date` → `run_date`
- `support_fire_note` → `support_fire_notes`

The formatted CSV (`*_formatted.csv`) column names are unchanged — it now becomes a pure column-subset-and-reorder of canonical with no rename map. The two-schema design collapses to one.

- **Operator change:** `health_operator_v3.py` `main()` row-dict keys updated; `_fmt_renames` dict removed.
- **Old canonical SHA (V3.2.7):** `e016ed8a5af2e9f64c0f7e7d11217198dae50000df797e79b1e96639aae63c53`
- **New canonical SHA (V3.2.8):** `63148feb319f4dc434d249ecc47ed90df1adc4c19cf5fc36b9d258bbfcea8ddf`
- **Determinism:** two-pass cache-mode verification confirms byte-identical reproducibility under new code.
- **Out of scope:** `outcomes.csv` `prior_health_score` / `prior_health_band` snapshot columns remain (no join semantics affected). Internal Python variable `score_date` retained (CLI arg `--score-date` unchanged).

---

## 3.2.7 — 2026-05-13 (README §6.5 documents V3.2.4 floor sub-shapes)

### Documentation
- `README.md` §6.5 "Composite Narrative" Override paths section now enumerates all four behavioral-floor sub-shapes (critically-low, full-adoption-dark, clean-infrastructure-dark, standard) with the exact thresholds the operator uses. Previously the README described only "standard" and "very low," reflecting the V3.2.3 binary split rather than the V3.2.4 four-way refactor.
- No code change. Canonical SHA unchanged from V3.2.4: `e016ed8a5af2e9f64c0f7e7d11217198dae50000df797e79b1e96639aae63c53`.
- The README table now references operator line numbers (~1414–1463) and explicitly states that any future change to the conditions or narrative framings must update both files together.

---

## 3.2.6 — 2026-05-13 (deterministic tiebreaker in domain map SQL)

### Operator
- `build_domain_map()` SQL now uses `ORDER BY n DESC, org_shortname ASC` inside the `ranked` CTE. Previously, when two orgs shared the same user count for a domain, the `ROW_NUMBER()` assignment was not deterministic — a forward-looking hole in the live extract that did not affect cache-mode runs (which read `pg_domain_map.csv` as-is) but could have produced silently different cache files across repopulation runs.
- Affects live-mode runs and any future cache repopulation. Cache-mode canonical output against `cache/2026-05-13/` is unchanged.
- Canonical SHA: `e016ed8a5af2e9f64c0f7e7d11217198dae50000df797e79b1e96639aae63c53` (unchanged).

---

## 3.2.5 — 2026-05-13 (run_metadata.md fidelity fix)

### Operator metadata
- `run_metadata.md` `Command:` line now records `--cache --cache-dir` when those flags were used. Previously the recorded command silently omitted them, so the metadata trail was not replayable.
- Affects `runs/{date}/run_metadata.md` only. Canonical CSV and SHA are unchanged from V3.2.4.
- Canonical SHA: `e016ed8a5af2e9f64c0f7e7d11217198dae50000df797e79b1e96639aae63c53` (unchanged).

---

## 3.2.4 — 2026-05-13

### Composite narrative rewrite — exec-readable, one field

- Rewrote `_build_composite_narrative()` to produce plain-English narratives
  readable by both CS reps and exec/CEO audiences. No internal jargon
  ("behavioral floor," "capping," "save play," etc.) in any output.
  Shape logic (5 shapes + fallback) is preserved; output language is new.
- Removed `exec_narrative` field (added in V3.2.3). The rewritten
  `composite_narrative` supersedes it — one field now serves both audiences.
- Three specific quality fixes applied:
  1. Floor accounts now differentiated by profile (full-adoption-dark,
     clean-infra-dark, critically-low, standard) instead of identical text.
  2. "Near the boundary" framing restricted to composites 80–84 only.
     Composites 85+ use "mixed profile Thriving" framing.
  3. Value delivery = 0 now named explicitly ("no measurable business
     outcomes") rather than described as "primary liability."
- Formatted CSV returns to 19 columns (exec_narrative removed).
- All score and band columns are byte-identical to V3.2.3.
  New canonical SHA: `e016ed8a5af2e9f64c0f7e7d11217198dae50000df797e79b1e96639aae63c53`

---

## 3.2.3 — 2026-05-13

### New field: exec_narrative

- Added `exec_narrative` column to the **formatted CSV only** (`_formatted.csv`). Plain-English per-org summary (1–2 sentences, no internal jargon) for non-CS audiences. Written by a new `_build_exec_narrative()` function using the same shape-driven approach as `_build_composite_narrative()` but with exec-audience framing.
- `composite_narrative` is unchanged — this is a purely additive column.
- `exec_narrative` is computed in `main()` immediately after `composite_narrative` and stored in the working DataFrame, but excluded from the canonical CSV write via `df.drop(columns=["exec_narrative"]).to_csv(...)`. This keeps the canonical record stable and its SHA unaffected by additive narrative columns.
- Formatted CSV now has 20 columns (`exec_narrative` at position 9, after `composite_narrative`).
- Canonical SHA unchanged: `5d7dc1fdbe70f42f9931665abfbc785b2fa5dc5c988b43123401eadf89e519fc` (verified two-pass).

---

## 3.2.2 — 2026-05-13 (first canonical on fresh data + cache-population workflow documented)

The V3.2.1 canonical was built against `cache/2026-05-11/`. This version supersedes it with the first canonical produced via the architecturally correct workflow: MCP-driven cache population followed by the deterministic cache-mode operator run. **Operator code is unchanged from V3.2.1** — this is a canonical-artifact refresh and a documentation patch, not a code change.

### What changed

- **New canonical artifact:** `runs/2026-05-13/client_health_scores_2026-05-13.csv` — SHA-256 `5d7dc1fdbe70f42f9931665abfbc785b2fa5dc5c988b43123401eadf89e519fc`. Built from `cache/2026-05-13/` (10 CSVs populated via the `user-supercat-postgres-vpn` and `user-bigquery-vpn` MCPs).
- **README — new section "How to populate the cache"** added before the existing "How to run" section. Documents the 10-file MCP-driven workflow (loader-function mapping, named-param substitution, format requirements, post-write verification, sanity checks). Closes the documentation gap that surfaced when the first attempt at the live extract assumed the operator could populate its own cache (it cannot — see §6.6).
- **README version bumped to 3.2.2 and date to 2026-05-13.** Status text updated to remove the "for initial CEO read" qualifier; the system is now production-ready for routine use.
- **V3.2.1 cache-mode baselines archived:**
  - `runs/2026-05-11/` → `_archive/runs/v3.2.1-cache-baseline_2026-05-11/`
  - `cache/2026-05-11/` → `_archive/cache/v3.2.1-cache-baseline_2026-05-11/`

### Score-date anchor

`$SCORE_DATE` was determined via `date -u +%F` and resolved to **2026-05-13** (UTC). This intentionally diverges from the local-time date because the data inside Postgres queries is anchored to PG `NOW()` (UTC); aligning the cache directory name and `--score-date` with the data's actual anchor preserves the determinism contract.

### Distribution (104 orgs scored)

| Band | V3.2.1 (cache 2026-05-11) | V3.2.2 (cache 2026-05-13) | Δ |
|---|---|---|---|
| Thriving | 57 | 57 | 0 |
| Healthy | 32 | 31 | -1 |
| Watch | 13 | 14 | +1 |
| At Risk | 1 | 1 | 0 |
| Critical | 1 | 1 | 0 |

Behavioral floor: 7 (identical cohort: `cf, hh, hmjc, krb, mfc, st, tel`). Ghost: 0. Net band shift: 1 Healthy → 1 Watch.

### Delta vs V3.2.1 baseline

**5 band changes** (3 are sub-2-point boundary brushes; 2 are real value-delivery swings):

| Org | V3.2.1 | V3.2.2 | Composite Δ | Driver |
|---|---|---|---|---|
| `ap` | Healthy | Watch | 60.6 → 59.4 (−1.2) | ops (−4.8), crossed 60 boundary |
| `asi` | Thriving | Healthy | 84.3 → 78.9 (−5.4) | value delivery (−20.0) |
| `eglo_can` | Healthy | Thriving | 78.1 → 89.0 (+10.9) | value (+33.3), engagement (+10) |
| `sca` | Thriving | Healthy | 80.9 → 79.8 (−1.1) | ops (−4.4), crossed 80 boundary |
| `yw` | Healthy | Thriving | 79.0 → 80.7 (+1.7) | ops (+3.6), crossed 80 boundary |

**6 composite shifts > 5 points** (all bands unchanged unless listed above):

| Org | Composite Δ | Driver |
|---|---|---|
| `eglo_can` | +10.9 | value +33.3, engagement +10.0 |
| `mli` | −8.4 | value −33.3 |
| `ssi` | −8.4 | value −33.4 |
| `etl` | +6.9 | ops +27.7 |
| `soi` | +5.9 | ops +23.6 |
| `asi` | −5.4 | value −20.0 |

All shifts concentrated in `value_delivery` and `operational_health` — the two inherently volatile dimensions (a single order or import-feed event crossing a 90-day window can produce a 20–33pt step on small denominators). 98 of 104 orgs (94%) shifted composite by < 5 points.

### Cache deltas vs `cache/2026-05-11/`

| File | 05-11 | 05-13 | Δ |
|---|---|---|---|
| pg_org_config | 248 | 248 | 0 |
| pg_engagement | 248 | 248 | 0 |
| pg_smart_stacks | 181 | 181 | 0 |
| pg_orders | 186 | 186 | 0 |
| pg_portal_orders | 35 | 35 | 0 |
| pg_catalog | 233 | 233 | 0 |
| pg_imports | 759 | 758 | -1 |
| pg_domain_map | 4,848 | 4,850 | +2 |
| bq_mp_sharing | 106 | 107 | +1 |
| bq_helpscout_fires | 10 | 10 | 0 |

All deltas under 1%, well inside the 50% suspicion threshold.

### Validation

- **Two-pass byte-identical determinism** confirmed at SHA `5d7dc1fdbe70f42f9931665abfbc785b2fa5dc5c988b43123401eadf89e519fc`.
- **Independent cold-read review** (separate agent, 9 checks) cleared all checks. Notable verification: `mfc` operational_health jumped 46.7 → 64.8 between the two runs, but the composite remained floor-capped at 40 with band unchanged at Watch. The +18 ops jump is backed by 3 new successful Products import runs in `cache/2026-05-13/pg_imports.csv` (most recent on 2026-05-12, one day before score date) — a real cache-level activity change, not a calculation artifact.
- **All 7 narrative spot-checks preserved expected shape.** The two with shifted wording (`kii`, `mfc`) shifted only because dimension scores ticked, not because the narrative branch changed.

---

## 3.2.1 — 2026-05-12 (post-review polish)

Triaged from a cold-read review of V3.2.0. All findings were minor (no scoring or pipeline blockers). This patch addresses the items that change CSV content or that the CHANGELOG misstated.

### Narrative engine

- **Re-introduced engagement-rate qualifier in Shape 2 (breadth gap).** The first sentence now reads `"<org>'s reps are logging in at a limited rate (engagement <e>)"` when `engagement < 70`, or `"...consistently (engagement <e>)"` when `engagement ≥ 70`. The V3.2.0 simplification had dropped the qualifier entirely, which preserved the semantic intent (no overstatement of activity) but lost the spec'd phrasing for borderline-engagement accounts. Verified across all 10 breadth-gap accounts in the canonical run: 3 correctly receive "at a limited rate" (`gc`, `ihm`, `sp`), 7 correctly receive "consistently" (`bp`, `yw`, `ah`, `soi`, `eli`, `arl`, `gcl`).
- **Docstring fix:** `_build_composite_narrative` docstring now says "Five shape categories" (was "Four"). Stale text from an earlier draft of the V3.2 refactor.

### Documentation

- **Softened the threshold-stripping claim** in V3.2.0's `METHODOLOGY.md` bullet. Was "Stripped of all specific numerical thresholds." Now reflects reality: stripped of fine-grained per-signal thresholds; composite-level thresholds (band cutoffs, dimension weights) retained because they belong in an executive explainer.
- **Corrected the line-count claim** for the simplified narrative engine (`140` → `~165`). The 244 → 167 reduction is real (32% fewer lines, 7 patterns → 5 shapes + fallback); the round number was just imprecise.

### Determinism — verified end to end

- **Two-pass byte-identical reproduction** at `--score-date 2026-05-11` against the existing cache: SHA `d1f03c2f886f875faeb51e66abf124bf91a13c0188b8343b7380393d7f2e221d` reproduced exactly.
- **Future-date dry run** at `--score-date 2026-06-12` against the same cache: also two-pass byte-identical (SHA `bc816777efd436622ae225f8ba923173474553601ba3aa6db7036a6f94ab99db`). Confirmed all expected drifts are anchored to score-date math, not wall-clock:
  - Day counts in `operational_health_narrative` advanced by exactly 32 days (e.g., `dals` Products feed: `73d ago` → `105d ago`).
  - `engagement_score`, `adoption_score`, `value_delivery_score` unchanged across all 104 orgs (zero wall-clock dependence).
  - `operational_health_score` shifted for 91 of 104 orgs (correct behavior — feeds that are 60d fresh today will be 92d stale a month from now).
  - Behavioral floor count unchanged (7 → 7) — floor depends on engagement and value delivery, not freshness.
  - Test artifacts archived to `_archive/determinism_tests/2026-05-12/future_date_06-12/`.

### Canonical run

- V3.2.1 canonical CSV — SHA-256: `d1f03c2f886f875faeb51e66abf124bf91a13c0188b8343b7380393d7f2e221d`. Replaces the V3.2.0 SHA `c85e7a3cce14333a65e6c40482e99af1338e590c8917bedc066d17bec3b2ab20` (only the `composite_narrative` column changed for the 10 breadth-gap orgs; all scores and bands are unchanged). Originally at `runs/2026-05-11/client_health_scores_2026-05-11.csv`; archived under V3.2.2 to `_archive/runs/v3.2.1-cache-baseline_2026-05-11/client_health_scores_2026-05-11.csv`.

### Distribution (unchanged from V3.2.0)

| Band | Count |
|---|---|
| Thriving | 57 |
| Healthy | 32 |
| Watch | 13 |
| At Risk | 1 |
| Critical | 1 |

Ghost: 0. Behavioral floor: 7. Support fire flags: 9. Bundle/config mismatches: 3.

---

## 3.2.0 — 2026-05-12

### Operator behavior

- **Behavioral floor override (§5.2 in `README.md`).** When `engagement < 55` AND `value_delivery < 40`, the composite score is capped at 40 (top of Watch) regardless of how strong adoption or operational health are. Prevents an account where reps have effectively gone dark from scoring Healthy on the strength of clean infrastructure.
- **Deterministic cache-mode runs.** All wall-clock time dependencies in scoring and narrative logic now anchor to `--score-date` rather than `datetime.utcnow()`. Cache-mode runs are now byte-identical regardless of when the operator is invoked. Previously, freshness-based ops sub-signals drifted by 1–6 points per dimension depending on the gap between data extraction and operator execution; that drift is gone. Verified by SHA-256 comparison across multiple runs against the same cache.
  - Specific changes in `health_operator_v3.py`:
    - `score_operational_health` and `_build_ops_narrative` now take an `as_of` parameter (passed `score_date_dt` from `main`) and use it for all freshness math.
    - New-org exclusion in `main` now compares against `score_date_dt`, not `today`.
- **Idempotent output directory.** Re-running with `--output-dir runs/2026-05-11` no longer creates a `runs/2026-05-11/2026-05-11/` nest. The operator now writes to `{output_dir}/{score_date}/` only when `{output_dir}` doesn't already end in the score date.

### Composite narrative engine — simplified

- The composite narrative engine in `_build_composite_narrative()` was rewritten to be score-shape driven rather than pattern-template driven:
  - **Before**: 7 patterns (244 lines), with `Pattern 1` lumping all all-strong accounts into a single narrative regardless of whether the composite was 81 or 98, and a 25-entry `action_map` lookup.
  - **After**: 5 explicit shapes + a mixed-profile fallback (~165 lines). All-strong accounts split into three sub-shapes (clean Thriving, borderline Thriving, all-strong Healthy) that each warrant a different action tone. Fallback uses a 12-entry band-aware action lookup.
- **Differentiated all-strong narratives.** Previously, `ih` (composite 98, all dims 91+) and `gl` (composite 81, engagement 72) received the *identical* "performing at a high level… consistent performance across every pillar" narrative. Now `ih` reads "performing across the board, no CS action required" and `gl` reads "in the Thriving band, but near the boundary — engagement (72) is the relative drag… a check-in would solidify Thriving status before drift sets in."
- **Score-aware override paths.** The behavioral-floor narrative used to be a single template string that produced identical text for every floor-applied account. Now:
  - `tel` (composite 15, engagement 13, value delivery 0) reads "Behavioral floor applied, but the composite (15) is well below the floor cap on its own merits… immediate save-play candidate."
  - `mfc` (composite 40, engagement 50, value delivery 33) reads "Behavioral floor applied — engagement (50) and value delivery (33) are both below threshold… CS should treat this as a near-ghost."
- **Numbers are surfaced in every narrative.** Each shape now embeds the actual dimension scores (e.g., "engagement (67)", "ops (10)") rather than referring to dimensions abstractly. Makes the narrative interpretable without cross-referencing the score columns.

### Narrative content fixes (carried forward from earlier V3.2.x work)

- `asi.ops_narrative` names Portal Invoices as the outlier feed instead of declaring all feeds "running on cadence."
- `sbl.ops_narrative` uses "critical" (not "declining") for the Customers feed.
- `ihm.adoption_narrative` enumerates all three unused features (Smart Stacks, Inventory Management, Sales Data).
- `dals.ops_narrative` includes a day count for the errored Products feed.
- `asi.value_delivery_narrative` says "no portal orders in 90d" rather than "haven't opened it" when Sales Portal engagement is a gap.
- `dals.composite_narrative` includes an explicit critical-ops sentence when ops_score is 10.
- `ihm.composite_narrative` uses "at a limited rate" rather than "consistently" when reps are logging in below threshold.

### Documentation

- **`README.md` is now the single authoritative spec.** Sections updated for V3.2: §5.2 Behavioral Floor Override, §6.5 Composite Narrative (rewritten to describe the simplified engine), §6.6 Determinism and Reproducibility. Stale §11 Cache Regeneration Note removed.
- **`METHODOLOGY.md` is the executive-facing explainer.** Restored from the archive after a brief attempt to merge it into `README.md`. Stripped of fine-grained per-signal thresholds (login bands, ratio bands, freshness bands) — those live in `README.md`. Composite-level thresholds (band cutoffs, dimension weights) are retained because they belong in an executive explainer. The methodology file now explains *what each dimension means and why* without duplicating the per-signal spec.

### Data hygiene

- **`outcomes.csv` created** with the header `org_shortname,outcome_date,outcome_type,prior_health_score,prior_health_band,notes`. Empty for now — will be populated as labeled outcomes (churn / renewal / expansion / save) become available, to support V3.3 weight calibration.

### Cleanup

- **`_archive/` directory** created. Moved into it:
  - Pre-cleanup full backup tarball (`Health_V3_pre_cleanup_2026-05-12.tar.gz`).
  - Transient audit/review docs: `COLD_READ_AUDIT.md`, `NARRATIVE_FIX_REVIEW_2026-05-12.md`, `OPERATOR_AUDIT_2026-05-12.md`, `HANDOFF_TO_RUN_AGENT.md`, `METHODOLOGY.html`.
  - Old `raw_signals_extractor.py` (functionality is folded into the operator).
  - All intermediate `runs/` subfolders (`v3.1`, `v3.1-narratives`, `v3.2-composite-narrative`, `raw_2026-05-11`, `research_2026-05-11`, `test_2026-05-11`, `spot_check_7_clients_2026-05-12_folder`, etc.) and the initial pre-V3.2 `2026-05-11` run.
  - `_preview_narratives_2026-05-12.md` (the 7-org side-by-side used to validate the simplified engine before implementation).
- The canonical V3.2 output had CSV checksum (SHA-256): `c85e7a3cce14333a65e6c40482e99af1338e590c8917bedc066d17bec3b2ab20`. Originally at `runs/2026-05-11/`; superseded by V3.2.1 at the same path on the same day, then archived under V3.2.2 to `_archive/runs/v3.2.1-cache-baseline_2026-05-11/`.

### Distribution (104 orgs scored)

| Band | Count |
|---|---|
| Thriving | 57 |
| Healthy | 32 |
| Watch | 13 |
| At Risk | 1 |
| Critical | 1 |

Ghost accounts: 0. Behavioral floor applied: 7. Support fire flags: 9. Bundle/config mismatches: 3.

---

## 3.1 — 2026-05-11 (earlier same-week iteration, archived)

Initial post-cleanup narrative pass. State is preserved in `_archive/runs/v3.1/` and `_archive/runs/v3.1-narratives/` for reference. Superseded by 3.2.

---

## 3.0 — 2026-05-10 (initial V3 run)

First end-to-end V3 run. Preserved in `_archive/runs/initial_2026-05-11/`. Superseded.
