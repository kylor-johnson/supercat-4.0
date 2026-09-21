# Health V3 — Start Here

**`Health V3/` is the single source of truth for SuperCat customer health.** One
folder. Health V2 is frozen in `_museums/`; the former `Health V3 Backfill/`
clone was merged in here on 2026-09-16 and no longer exists.

## Current state

| | |
|---|---|
| Version | **3.6.0** (2026-09-21) |
| Weights | **equal — 25 / 25 / 25 / 25** (`--weights equal`, the default) |
| Live canonical | `runs/2026-09-21/client_health_scores_2026-09-21.csv` |
| SHA-256 | `2850025eb9de25926e4c633e3d0aed8f39a4010d874cc6e2935b4e176069896e` |
| Population | 114 orgs, $1.97M ARR, score date 2026-09-21 |
| Distribution | 52 Thriving · 40 Healthy · 14 Watch · 4 At Risk · **4 Critical** (4 ghosts, $83,520 ARR) |
| Series | 8 snapshots, 2025-11-30 → 2026-09-21, all equal-weighted. Priors in `runs/historical/`. |

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
  --mal "inputs/master_account_list_2026-09-16_canonical.csv" \
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

Every finding from both verification passes is closed, and the September run is
promoted (CHANGELOG 3.6.0). What remains:

1. **`catalog_only` ops still enters the composite at full weight.**
   `ops_measurement` makes it detectable, not corrected. Nothing is mis-scored
   today — every `catalog_only` org is ghost- or floor-capped — but a
   `catalog_only` org with healthy engagement and no override would carry an
   unearned ops 100. Candidate fix: cap `catalog_only` ops at ~75–79 rather than
   blanking. Own version bump plus a delta study.
2. **Cache population has no automation and no credentials on disk.** ~215 KB
   round-trips through an agent as text, and it produced the only silent corruption
   this program has seen — three transcription errors in `pg_domain_map.csv`, caught
   only by checksum. **Highest-value remaining engineering task.**
3. **Commit before rescore.** Two uncommitted-work losses are on record: the V3.3.x
   doc layer plus `trigger_engine_v1.py` (CHANGELOG 3.4.0), and the V3.4.0 staged
   run `6dc304ea…` (CHANGELOG 3.5.1). Same root cause both times.
4. **agent-factory mirror is stale and falling further behind.**
   `agents/ceo_system/onboarding_reality/health_v3/` still hardcodes V3.3.0 weights
   and now lacks both new columns and every fix from V3.4.1 → V3.6.0. The Wednesday
   Windmill `fetch_early_life` job runs it. This repo's operator is a clean
   superset, so the merge is one-directional (copy here → there).
5. **Four ghosts need CS contact.** `aa` $42,480 has never logged in against six
   months of billing — confirm go-live before treating it as churn. `bmc` $21,720
   was live since 2011 and is dark 291 days. Neither was visible before this run.
6. **Lifetime login counts.** One unwindowed `COUNT(*)` in `load_pg_engagement`
   would make `dark_12m_plus` exact rather than windowed. Take it whenever the cache
   contract next changes.
7. **BigQuery contradicts.** `insightful_product.at_risk_accounts` flags 79 accounts
   (63 with zero ARR); `segment_classifier` returns 86/35/48 against the stamped
   56/28/20. T3 sells account health scoring, so two disagreeing sources is real
   exposure. `05_strategic_direction.md`'s "always-current health scores" claim needs
   correcting.
8. **`subscriptions.custom_price` is mixed-unit** (`mah`, `kii` at 12× monthly).
9. **README §9 is not closed** — 11 outcome labels against a 30-outcome gate. The
   four new ghosts and any churn among them should land in `outcomes.csv`.
10. **No `save_plays.md`.**
11. **Stale iCloud fork** — `iCloud/SuperCat 4.0/Health V3/` has none of this work.
