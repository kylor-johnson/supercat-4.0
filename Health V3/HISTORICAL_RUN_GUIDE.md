# Health V3 — Historical Run Guide

How to score a **past** date. Use this when you need to extend the month-over-month
series backwards, or reconstruct a snapshot that was never run.

For the normal monthly run, use `RUN_PROMPT.md`. For the mechanics of a single
run, `FRESH_RUN_GUIDE.md`. This guide only covers what is *different* about a
historical date.

> **Historical runs are approximate.** They are fit for trend and trigger
> detection, not for a client-facing number. The limitations below are real and
> must be restated in every `run_metadata.md` you produce.

## State of the existing series

The series is **one snapshot per directory under `runs/historical/`, plus the
live canonical** — count the directories rather than trusting a number here; a
hand-maintained count in this file has gone stale twice. All are scored under
equal weights and the pinned interpreter (see `ENVIRONMENT.md`):

| Score date | Location |
|---|---|
| 2025-11-30 → 2026-09-01 | `runs/historical/{date}/` |
| 2026-09-21 | `runs/2026-09-21/` (the live canonical, `2850025e…`) |

Nov 2025 – May 2026 were regenerated as the engine changed, and Jun–Aug 2026 were
backfilled on 2026-09-21, so the whole series is internally consistent under one
weighting scheme and one interpreter. Each `run_metadata.md` carries its
limitations note and its current SHA.

> **2026-09-01 was scored twice.** The first attempt used the wrong window anchor
> and was rejected; it is preserved at
> `_archive/rejected/2026-09-01_wrong_anchor/` as the worked example of the rule
> below, with the proof and the reusable-file list. The corrected run is in the
> series.

**`trigger_engine_v1.py` will refuse a series that mixes weighting schemes.** It
infers each snapshot's scheme from the data and exits rather than emit
month-over-month deltas that reflect an engine change instead of client
behaviour. If you add a snapshot, score it with the same `--weights` as the
rest (default `equal`) or the trigger run will stop.

---

## Known limitations of historical runs

Restate these in every `run_metadata.md` produced from a historical cache:

| Dimension | Limitation |
|-----------|------------|
| Engagement | Accurate — `login_events` are timestamped, trailing windows correctly anchored |
| Adoption | Approximately accurate — feature flags (`mobile_sites`) reflect **current** config, not historical. An org that has since disabled a feature will show it disabled, understating its historical adoption. |
| Value Delivery | Accurate — `orders` and `portal_orders` are timestamped |
| Ops Health (imports) | Accurate — `import_events` are timestamped |
| Ops Health (catalog) | **Not historical** — catalog completeness reflects today's catalog. Treat ops scores as approximate for catalog-heavy orgs. |
| Support Fire | Approximately accurate — the query sees only conversations still open. Ones open then but closed since do not appear. |
| MAL | **Whichever MAL you pass** — orgs that churned and were dropped from it will not appear at all. Orgs added after the score date will appear but are usually caught by the 90-day new-org gate. |

---

## Directory layout

```
Health V3/
├── cache/
│   ├── {YYYY-MM-DD}/          ← current-month canonical caches
│   └── historical/
│       └── {YYYY-MM-DD}/      ← 10 cache CSVs per historical score date
└── runs/
    ├── {YYYY-MM-DD}/          ← current-month canonical output
    └── historical/
        └── {YYYY-MM-DD}/      ← canonical + formatted CSV + run_metadata.md
```

Each `cache/historical/{date}/` is **immutable once populated**, exactly like a
current-month cache (README §6.6). To rescore a date, point at the same cache.

---

## Step 0 — Environment

Same as every other run: `.venv/bin/python3`, built per `ENVIRONMENT.md`. A
historical snapshot scored under a different interpreter will drift by ~0.1 on a
handful of composites, which is enough to manufacture a spurious `score_drop`
against its neighbours.

## Step 0.5 — Prove your anchor against a committed month, before pulling anything

**Do this first. It costs one query and it is the only check that catches a wrong
anchor before you have spent an hour populating a cache.** Every agent who skipped
it paid far more than one query; one had a whole month rejected.

Run this and require an exact match:

```sql
SELECT COUNT(*) FILTER (WHERE created_at >= (DATE '2026-04-30' + INTERVAL '1 day') - INTERVAL '90 days'
                          AND created_at <  DATE '2026-04-30' + INTERVAL '1 day') AS logins_90d
FROM login_events WHERE organization_id = 1;
-- must return exactly 6028, which is what cache/historical/2026-04-30/pg_engagement.csv holds
```

If it returns 6048 you have applied the literal `[D−90, D)` reading; 6112 means a
91-day window. Neither is the series convention. Only proceed on 6028.

Then apply the identical form to *your* score date. The whole org-1 row reproduces
under this anchor — `logins_30d` 2067, `logins_180d` 10283, `active_users_90d` 59,
`active_users_365d` 78, and `last_login_at` to the microsecond — so if you want a
stronger check, reproduce all of them.

---

## Step 1 — Populate the historical cache

Use the Postgres and BigQuery MCP servers (VPN required). Read each loader
function in `health_operator_v3.py` verbatim for its SQL — do not paraphrase —
then apply the date substitution below to **every** trailing-window filter, and
write the 10 CSVs to `cache/historical/{score_date}/`.

**The historical cutoff substitution rule.**

This is the most load-bearing rule in the folder and it was undocumented until
2026-09-21, when three backfill agents independently rediscovered it at real cost.
Get it wrong and the run looks plausible while being silently inconsistent with
every other snapshot.

**Two anchors, not one.** The loaders do not agree with each other, and the series
faithfully reproduces that disagreement. Match the loader, not a single rule:

| Loader | SQL anchor | Historical anchor | Window |
|---|---|---|---|
| `load_pg_engagement` | `NOW()` | **`DATE 'D' + INTERVAL '1 day'`** | `[(D+1)−N, D+1)` |
| `load_pg_orders` | `NOW()` | **`DATE 'D' + INTERVAL '1 day'`** | `[(D+1)−90, D+1)` |
| `load_pg_imports` | `NOW()` | **`DATE 'D' + INTERVAL '1 day'`** | `[(D+1)−N, D+1)` |
| `load_pg_portal_orders` | `CURRENT_DATE` | `DATE 'D'` | `[D−90, D)` |
| `load_bq_mp_sharing` | `CURRENT_DATE()` | `DATE('D')` | `[D−90, D)` |
| `load_pg_org_config`, `load_pg_catalog`, `load_pg_smart_stacks`, `build_domain_map` | *no date filter* | n/a — current state, see limitations | n/a |
| `load_bq_helpscout_fires` | `status IN ('active','pending')` | **cannot be back-dated** | see below |

**`bq_helpscout_fires` does not backfill — expect zero rows.** It is not an
absent date filter, it is a filter on *current* ticket status, so a historical run
sees only conversations still open today. Four consecutive backfill months have
produced `support_fire = 0` from a header-only file, and each agent has had to
work out independently whether they broke something. They did not. Never read a
support-fire trend across historical snapshots.

So a `NOW()` window **includes the whole score date**; a `CURRENT_DATE` window
stops at its start. That one-day difference between the two families is a genuine
inconsistency in the model, not a transcription error — reconcile it deliberately
someday, never mid-backfill.

**Why `D + 1` and not `D`.** Verified against the already-committed 2026-04-30
snapshot, org 1, whose cache holds `logins_90d = 6028`:

| Convention | Result | Reproduces the cache? |
|---|---|---|
| `[D−90, D)` — anchor at the start of the score date | 6048 | no |
| `[D−90, D+1)` — 91 days wide | 6112 | no |
| `[(D+1)−90, D+1)` — **anchor = D+1** | **6028** | **yes** |

Confirmed again across 2026-03-31 and 2026-02-28, on `pg_imports` run counts, and
on `last_login_at` to the microsecond.

**You must also add an upper bound that the SQL does not contain.** In
`load_pg_engagement`, `MAX(created_at) AS last_login_at` and
`MIN(created_at) AS first_login_at` sit **outside** the `FILTER` clauses, as do
`MAX/MIN(created_at)` in `load_pg_imports`. Substituting only the `FILTER`
intervals leaves those completely unwindowed, so they return **present-day**
values under a historical label:

```sql
-- required for the NOW() loaders only, in addition to the FILTER substitutions
WHERE created_at < DATE 'D' + INTERVAL '1 day'
```

**Scope this to the `NOW()` family.** `load_pg_portal_orders` and
`load_bq_mp_sharing` anchor at `DATE 'D'`, so applying the `+ 1 day` bound to them
would widen their window by a day and re-create a variant of the bug this rule
exists to prevent. Neither has an unbounded `MAX/MIN` today, so nothing breaks
right now — but do not apply it mechanically.

Omit it and `logins_90d` still looks perfectly correct, so nothing downstream
flags it — but `first_login_at` drives the 90-day new-org gate and `last_login_at`
drives `days_dark` and `ghost_subtype`. Silent and consequential.

**Verify empirically, and make the assertions two-sided.** A one-sided upper
bound cannot detect an anchor that is a day too *early* — which is the failure
mode that actually happened. The rejected 2026-09-01 run maxed at
`2026-08-31 23:59:50`, and an assertion of `<= D 23:59:59` passes on that
cleanly. Assert the value lands **on** the score date:

```python
# each must fall ON D, not merely at or before it
assert max(pg_engagement.last_login_at).date() == D
assert max(pg_imports.last_run_at).date()      == D
# exact, not approximate — 180 days back from the anchor, which is D+1
assert min(pg_imports.first_run_at).date()     == (D + 1 day) - 180 days
```

(For a score date with genuinely no activity anywhere in the estate the first two
would legitimately fail — check the date against the busiest org rather than the
global max if you ever hit that.)

Missing any of this silently scores a *current* window under a historical
label — the single most damaging error in this workflow. The file list, column
requirements, and format rules are in README §"How to populate the cache".

## Step 1.5 — Reusing cache files on a re-run

The five loaders with no date filter are **anchor-independent**, so on a re-run
(or a second score date populated the same day) they can be copied forward rather
than re-pulled. That removes the transcription channel entirely for the expensive
ones — `pg_domain_map.csv` alone is ~5,000 rows, and is where this programme's only
silent corruption occurred.

**Verify a reused file against its recorded md5, not against a fresh server
checksum.** The source drifts continuously, so a server re-proof on a file
populated hours or days earlier fails for entirely legitimate reasons — and an
operator who sees the check fail for non-reasons learns to ignore it. Record the
populate window the file came from; that window is what makes it comparable to its
sibling months, and it belongs in `run_metadata.md`.

A cheaper middle path when a file *has* drifted: compare server-side checksums
per key bucket (e.g. `LEFT(domain,1)` for the domain map) and transfer only the
buckets that differ. One backfill agent moved a single bucket of 32 that way,
leaving 4,684 of 4,979 rows with zero transcription exposure.

---

## Step 2 — Run the operator

```bash
cd "Health V3"
.venv/bin/python3 health_operator_v3.py \
  --mal "inputs/master_account_list_2026-09-16_canonical.csv" \
  --score-date {score_date} \
  --cache --cache-dir "cache/historical/{score_date}" \
  --output-dir "runs/historical"
```

Run it twice and SHA both outputs — they must be byte-identical.

Pass the MAL that was closest to the score date. Note which one you used in
`run_metadata.md`; it changes the population, not just the metadata.

Each `runs/historical/{date}/` should end up with:

- `client_health_scores_{date}.csv`
- `client_health_scores_{date}_formatted.csv`
- `run_metadata.md` — SHA, row count, distribution, **the limitations table
  above**, the MAL used, and the interpreter

## Step 3 — Fold into the series

1. `.venv/bin/python3 check_consistency.py` — 9/9. It evaluates the latest
   `YYYY-MM-DD` run under `runs/`, so a new historical date should not move it.
2. `.venv/bin/python3 trigger_engine_v1.py` — confirm it reports your new
   snapshot at the same weighting scheme as the rest, then check the
   month-over-month triggers around the date you added.
3. Add a CHANGELOG note if the new snapshot changes any published trend.

---

## Hard constraints

- **Never modify a populated cache.** Immutable once written, per §6.6.
- **Never mix weighting schemes within a series.** The trigger engine enforces
  this; do not reach for `--allow-mixed-weights` to get past it.
- **Restate the limitations** in every `run_metadata.md`. A historical run that
  looks canonical but omits them is worse than no run.
- **Do not present historical scores to a client.** Catalog completeness and
  adoption flags are present-day; trend and triggers only.

---

## History

This folder was previously a separate clone (`Health V3 Backfill/`) created in
June 2026 so backfill work could not touch production. That clone was merged
back in on 2026-09-16 — the guide you are reading now describes the merged
folder, and the "never write to production" rules it used to carry no longer
apply.

The dimension-weighting look-back study that motivated the original backfill is
**complete**. It ran on 2026-09-16 against 11 real outcome labels and rejected
weighting; see `CHANGELOG.md` 3.4.0, `runs/_weighting_study/2026-09-16/`, and
README §9. Do not re-run it as though it were open — §9 remains ungated on the
30-outcome threshold, which is a different question.
