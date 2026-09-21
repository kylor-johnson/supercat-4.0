# Health V3 — Start Here

**`Health V3/` is the single source of truth for SuperCat customer health.** One
folder. Health V2 is frozen in `_museums/`; the former `Health V3 Backfill/`
clone was merged in here on 2026-09-16 and no longer exists.

## Current state

| | |
|---|---|
| Version | **3.5.0** (2026-09-21) |
| Weights | **equal — 25 / 25 / 25 / 25** (`--weights equal`, the default) |
| Live canonical | `runs/2026-05-13/client_health_scores_2026-05-13.csv` |
| SHA-256 | `a5d8cb289f0ae945efc1636453bfd8f4f3ffe316417dde2011d7ab8f5bc5b73d` |
| Population | 104 orgs, score date 2026-05-13 |
| Distribution | 57 Thriving · 31 Healthy · 14 Watch · 1 At Risk · 1 Critical |
| Series | 7 monthly snapshots, 2025-11-30 → 2026-05-13, all equal-weighted |
| Staged | `runs/_staged/2026-09-21/` — 114 orgs on the September MAL, verified, **not promoted** |
| Invariants | `check_consistency.py` — 8 pass / 0 fail |
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

# 3. invariants — must be 8/8 before the run counts
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

The three score-moving findings from the 2026-09-21 test run are **closed in
V3.5.0** — see CHANGELOG. What remains:

1. **The September run is staged, not promoted.** `runs/_staged/2026-09-21/`
   (`9fc4b519…`, 114 orgs) is verified and all three blockers are cleared. Promoting
   it is now a decision, not a dependency — follow the checklist in
   `runs/_staged/README.md`.
2. **Cache population has no automation and no credentials on disk.** All ~215 KB
   round-trips through an agent as text; `pg_domain_map.csv` alone is ~5,000 rows.
   The 2026-09-21 run produced three silent transcription errors, all caught only by
   the README rule-8 checksum. A populate script would remove the whole risk class
   and is the highest-value remaining engineering task.
3. **agent-factory mirror is stale, and further behind than before.**
   `agents/ceo_system/onboarding_reality/health_v3/` still has V3.3.0 weights
   hardcoded and now also lacks both new columns and all three V3.5.0 fixes. Its
   `FACTORY.md` calls V3.3.0 "CS-authoritative" and the Wednesday Windmill
   `fetch_early_life` job runs it. This repo's operator is a clean superset, so the
   merge is one-directional (copy here → there).
4. **`ghost_subtype` uses a 12-month proxy for lifetime history.** `pg_engagement`
   carries no lifetime login count, so an org dark longer than a year reads as
   `no_activity_12m` even if it was once active (`pol`: 200 lifetime logins, dark
   432 days). Adding a lifetime column would break the existing cache contract.
5. **BigQuery contradicts.** `insightful_product.at_risk_accounts` flags 79 accounts
   (63 with zero ARR) and `segment_classifier` returns 86/35/48 against the stamped
   56/28/20. T3 sells account health scoring, so two disagreeing sources is a real
   exposure. `05_strategic_direction.md`'s "always-current health scores" claim
   needs correcting too.
6. **`subscriptions.custom_price` is mixed-unit.** `mah` and `kii` are stored at
   exactly 12× their monthly rate — a billing-data bug independent of health, and
   the reason Sept MAL MRR is carried forward from HubSpot rather than read from PG.
7. **README §9 is not closed.** The look-back ran on 11 outcome labels; the gate is
   30. `outcomes.csv` should grow as churn and downgrades land.
8. **No `save_plays.md`.** Triggers emit a CS action per row; the full save-play
   runbook (README §10) has not shipped.
9. **Stale iCloud fork.** `iCloud/SuperCat 4.0/Health V3/` has none of this work.
