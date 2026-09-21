# Health V3 — Start Here

**`Health V3/` is the single source of truth for SuperCat customer health.** One
folder. Health V2 is frozen in `_museums/`; the former `Health V3 Backfill/`
clone was merged in here on 2026-09-16 and no longer exists.

## Current state

| | |
|---|---|
| Version | **3.6.1** (2026-09-21) |
| Weights | **equal — 25 / 25 / 25 / 25** (`--weights equal`, the default) |
| Live canonical | `runs/2026-09-21/client_health_scores_2026-09-21.csv` |
| SHA-256 | `2850025eb9de25926e4c633e3d0aed8f39a4010d874cc6e2935b4e176069896e` |
| Population | 114 orgs, $1.97M ARR, score date 2026-09-21 |
| Distribution | 52 Thriving · 40 Healthy · 14 Watch · 4 At Risk · **4 Critical** (4 ghosts, $83,520 ARR) |
| Series | **11 snapshots**, 2025-11-30 → 2026-09-21, all equal-weighted. Priors in `runs/historical/`. Gap: 2026-09-01 rejected, see open item 1. |

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

1. **2026-09-01 needs a re-run.** Scored during the Jun–Sep backfill and
   **rejected** for using the wrong window anchor — quarantined at
   `_archive/rejected/2026-09-01_wrong_anchor/`, which documents the proof and lists
   the five cache files reusable on re-run. Until it lands, the series has an
   8-week gap between 2026-08-01 and 2026-09-21.
2. **The `NOW()` / `CURRENT_DATE` anchor disagreement.** `NOW()` loaders window
   `[(D+1)−N, D+1)`; `CURRENT_DATE` loaders window `[D−N, D)`. Every snapshot
   reproduces this one-day inconsistency faithfully. It is a real model defect, not
   a transcription error — reconcile deliberately, never mid-backfill, and expect to
   rescore the whole series when you do.
3. **Cache population has no automation.** ~215 KB round-trips through an agent as
   text and it produced this programme's only silent corruption. Two cheap
   mitigations are now proven and should be written into the guide: **copy the five
   anchor-independent files forward and re-prove them by server-side checksum**
   (removes the transcription channel entirely, including the 4,979-row
   `pg_domain_map.csv`), and parse harness-written result files directly rather than
   re-typing large results.
4. **`login_events` is on a rolling purge.** `min(first_login_at)` is now
   2025-03-21; caches populated five days earlier reach back to 2024-11-13. No
   current snapshot is affected, but **`first_login_at` is not comparable across
   snapshots populated at different times**, and a backfill reaching further back
   will silently lose window coverage.
5. **`catalog_only` ops still enters the composite at full weight.**
   `ops_measurement` makes it detectable, not corrected. Nothing is mis-scored today
   — every `catalog_only` org is ghost- or floor-capped. Candidate fix: cap
   `catalog_only` ops at ~75–79 rather than blanking. Own version bump plus a delta
   study.
6. **Commit before rescore.** Three uncommitted-work losses are now on record: the
   V3.3.x doc layer plus `trigger_engine_v1.py` (3.4.0), the V3.4.0 staged run
   `6dc304ea…` (3.5.1), and the rejected 2026-09-01 numbers (3.6.1, preserved only
   because it was quarantined deliberately).
7. **agent-factory mirror is stale and falling further behind.**
   `agents/ceo_system/onboarding_reality/health_v3/` still hardcodes V3.3.0 weights
   and lacks every fix from V3.4.1 → V3.6.1. The Wednesday Windmill
   `fetch_early_life` job runs it. This repo's operator is a clean superset, so the
   merge is one-directional (copy here → there).
8. **Four ghosts need CS contact, and they have been dark since at least June.**
   `aa` $42,480 has never logged in against six months of billing — confirm go-live
   before treating it as churn. `bmc` $21,720 was live since 2011 and is dark 291
   days. None were visible before the September MAL refresh.
9. **`support_fire` is populate-time-sensitive to within hours.** It reads only
   currently-open conversations, so it is 0 across all three backfill months and 1 in
   the canonical. Never read a trend off it.
10. **BigQuery contradicts.** `insightful_product.at_risk_accounts` flags 79 accounts
    (63 with zero ARR); `segment_classifier` returns 86/35/48 against the stamped
    56/28/20. T3 sells account health scoring, so two disagreeing sources is real
    exposure.
11. **`subscriptions.custom_price` is mixed-unit** (`mah`, `kii` at 12× monthly).
12. **README §9 is not closed** — 11 outcome labels against a 30-outcome gate.
13. **No `save_plays.md`.**
14. **Stale iCloud fork** — `iCloud/SuperCat 4.0/Health V3/` has none of this work.
