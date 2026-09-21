# Health V3 — Start Here

**`Health V3/` is the single source of truth for SuperCat customer health.** One
folder. Health V2 is frozen in `_museums/`; the former `Health V3 Backfill/`
clone was merged in here on 2026-09-16 and no longer exists.

## Current state

| | |
|---|---|
| Version | **3.5.1** (2026-09-21) |
| Weights | **equal — 25 / 25 / 25 / 25** (`--weights equal`, the default) |
| Live canonical | `runs/2026-05-13/client_health_scores_2026-05-13.csv` |
| SHA-256 | `a797e95980f7a9dc5fa185dbba51857f9f1bef57074e2a534744376a40207ca8` |
| Population | 104 orgs, score date 2026-05-13 |
| Distribution | 57 Thriving · 31 Healthy · 14 Watch · 1 At Risk · 1 Critical |
| Series | 7 monthly snapshots, 2025-11-30 → 2026-05-13, all equal-weighted |
| Staged | `runs/_staged/2026-09-21/` — 114 orgs on the September MAL, `2850025e…`, twice-verified, **not promoted** |
| Invariants | `check_consistency.py` — 9 pass / 0 fail |
| Interpreter | Python 3.9.6 · pandas 2.3.3 · numpy 2.0.2 (see `ENVIRONMENT.md`) |

Determinism is **interpreter-scoped**: same cache + same `--score-date` + same
interpreter → byte-identical. A SHA quoted without its interpreter is not a
reproducibility claim. Always run via `.venv/bin/python3`.

## Which file answers what

| Question | File |
|---|---|
| I need to produce this month's canonical | `RUN_PROMPT.md` — the orchestration prompt |
| How does a run actually work, step by step? | `FRESH_RUN_GUIDE.md` |
| What exactly does each dimension measure? | `README.md` — the spec (thresholds, SQL, fields, formulas) |
| Explain the score to an exec | `METHODOLOGY.md` |
| Why did the number change? | `CHANGELOG.md` — newest entry first |
| I need to score a past date | `HISTORICAL_RUN_GUIDE.md` |
| Why isn't the SHA reproducing? | `ENVIRONMENT.md` |
| What changed month over month, and who should CS call? | `trigger_reports/` via `trigger_engine_v1.py` |
| What weighting was chosen, and on what evidence? | `CHANGELOG.md` 3.4.0 + `runs/_weighting_study/2026-09-16/` |

## The monthly sequence

```bash
cd "Health V3"

# 0. once per machine — see ENVIRONMENT.md
/usr/bin/python3 -m venv .venv --system-site-packages
.venv/bin/pip install -r requirements.txt

# 1. populate cache/$DATE/ — 10 CSVs via MCP, README §"How to populate the cache"
#    (VPN required; the operator never pulls live data itself)

# 2. score
.venv/bin/python3 health_operator_v3.py \
  --mal "inputs/master_account_list_{date}_canonical.csv" \
  --score-date $DATE --cache --cache-dir "cache/$DATE" \
  --output-dir "runs/$DATE"

# 3. invariants — must be 9/9 before the run counts
.venv/bin/python3 check_consistency.py

# 4. month-over-month triggers for CS
.venv/bin/python3 trigger_engine_v1.py

# 5. dashboard, then 6. CHANGELOG entry + version bump in README AND METHODOLOGY
```

Full detail and the cold-read review step are in `RUN_PROMPT.md`.

## Rules that are load-bearing

- **A populated cache is immutable.** To rescore a date, point at the same cache.
  For fresher data, populate a new dated directory.
- **Never mix weighting schemes within a series.** `trigger_engine_v1.py` detects
  each snapshot's scheme and refuses. Don't reach for `--allow-mixed-weights`;
  that flag exists to reproduce the historical mistake, not to work around it.
- **`--include-new-orgs` changes the population.** Omit it for the monthly
  canonical; pass it only for onboarding early-life reviews.
- **Historical runs are not client-facing.** Adoption flags and catalog
  completeness are present-day regardless of score date.
- **Value Delivery is not a stress signal on its own.** It is substantially a
  segment proxy — Catalog-Focused accounts (54% of the base) order outside
  SuperCat by design. Engagement is the leading indicator.

## Known open items

Every finding from both verification passes is closed as of V3.5.1. What remains:

1. **The September run is staged, not promoted.** `runs/_staged/2026-09-21/`
   (`2850025e…`, 114 orgs) has cleared two independent verification passes.
   Promoting it swaps a 104-org April snapshot for a 114-org September one, with
   four-month deltas the trigger engine labels month-over-month. Checklist in
   `runs/_staged/README.md`.
2. **`catalog_only` ops still enters the composite at full weight.**
   `ops_measurement` makes it detectable, not corrected. Nothing is currently
   mis-scored — every `catalog_only` org is ghost- or floor-capped — but a
   `catalog_only` org with healthy engagement and no override would carry an
   unearned ops 100. Candidate fix: cap `catalog_only` ops at ~75–79 rather than
   blanking. Own version bump plus a delta study.
3. **Cache population has no automation and no credentials on disk.** ~215 KB
   round-trips through an agent as text. It produced the only silent corruption
   this program has seen — three transcription errors in `pg_domain_map.csv`,
   caught only by checksum. **Highest-value remaining engineering task.**
4. **Commit before rescore.** Two uncommitted-work losses are now on record: the
   V3.3.x doc layer plus `trigger_engine_v1.py` (CHANGELOG 3.4.0), and the V3.4.0
   staged run `6dc304ea…` (CHANGELOG 3.5.1). Same root cause both times. If a run
   is worth a CHANGELOG entry, commit the artifact before rescoring it.
5. **agent-factory mirror is stale and falling further behind.**
   `agents/ceo_system/onboarding_reality/health_v3/` still hardcodes V3.3.0 weights
   and now lacks both new columns and every fix from V3.4.1 / V3.5.0 / V3.5.1. The
   Wednesday Windmill `fetch_early_life` job runs it. This repo's operator is a
   clean superset, so the merge is one-directional (copy here → there).
6. **Lifetime login counts.** One unwindowed `COUNT(*)` in `load_pg_engagement`
   would make `dark_12m_plus` exact rather than windowed. Take it whenever the
   cache contract next changes for another reason.
7. **BigQuery contradicts.** `insightful_product.at_risk_accounts` flags 79
   accounts (63 with zero ARR); `segment_classifier` returns 86/35/48 against the
   stamped 56/28/20. T3 sells account health scoring, so two disagreeing sources
   is real exposure. `05_strategic_direction.md`'s "always-current health scores"
   claim needs correcting.
8. **`subscriptions.custom_price` is mixed-unit** (`mah`, `kii` at 12× monthly).
9. **README §9 is not closed** — 11 outcome labels against a 30-outcome gate.
10. **No `save_plays.md`.**
11. **Stale iCloud fork** — `iCloud/SuperCat 4.0/Health V3/` has none of this work.
