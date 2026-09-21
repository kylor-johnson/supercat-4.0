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

Seven snapshots exist, all scored under **V3.4.0 equal weights** and the pinned
interpreter (see `ENVIRONMENT.md`):

| Score date | Location |
|---|---|
| 2025-11-30 → 2026-04-30 | `runs/historical/{date}/` |
| 2026-05-13 | `runs/2026-05-13/` (the live canonical, `6a2f1d9f…`) |

The six historical months were regenerated on 2026-09-16 when the default
weighting reverted to equal, so the whole series is internally consistent. Each
carries its original limitations note plus its V3.4.0 SHA.

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

## Step 1 — Populate the historical cache

Use the Postgres and BigQuery MCP servers (VPN required). Read each loader
function in `health_operator_v3.py` verbatim for its SQL — do not paraphrase —
then apply the date substitution below to **every** trailing-window filter, and
write the 10 CSVs to `cache/historical/{score_date}/`.

**The historical cutoff substitution rule:**

| Live form | Historical form |
|---|---|
| `NOW() - INTERVAL '90 days'` | `'{score_date}'::date - INTERVAL '90 days'` |
| `NOW()` | `'{score_date}'::date` |
| `CURRENT_DATE - INTERVAL '90 days'` | `'{score_date}'::date - INTERVAL '90 days'` |
| BigQuery `CURRENT_DATE()` | `DATE('{score_date}')` |

Missing one of these silently scores a *current* window under a historical
label — the single most damaging error in this workflow. The file list, column
requirements, and format rules are in README §"How to populate the cache".

## Step 2 — Run the operator

```bash
cd "Health V3"
.venv/bin/python3 health_operator_v3.py \
  --mal "inputs/master_account_list_2026-04-14_canonical.csv" \
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

1. `.venv/bin/python3 check_consistency.py` — 8/8. It evaluates the latest
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
