# Health V3 — Start Here

**`Health V3/` is the single source of truth for SuperCat customer health.** One
folder. Health V2 is frozen in `_museums/`; the former `Health V3 Backfill/`
clone was merged in here on 2026-09-16 and no longer exists.

## Current state

| | |
|---|---|
| Version | **3.4.1** (2026-09-21) |
| Weights | **equal — 25 / 25 / 25 / 25** (`--weights equal`, the default) |
| Live canonical | `runs/2026-05-13/client_health_scores_2026-05-13.csv` |
| SHA-256 | `6a2f1d9fc6c86ae58a6888386f83b0a9122ecc98cb5ae6f2195e89a8d4dd1bff` |
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

Carried forward deliberately so they don't get lost. Items 1–3 came out of the
2026-09-21 end-to-end test run and **all three can move scores** — resolve them
before promoting `runs/_staged/2026-09-21/`.

1. **New-org gate is inert (NaT bug), and must be fixed together with
   ghost-over-gate precedence.** `NaT is not None` is `True`, so the zero-login
   branch of the gate is dead code and no org is ever excluded for having no
   logins. Fixing it alone would drop `aa` ($42,480, zero logins ever) from the
   scorecard, which is the wrong outcome — a paying account with no logins is a
   ghost, not a new org. See README §"New-Org Exclusion".
2. **Ops scores 100 when no import feed has ever run**, and `clean_ops_dark`
   then narrates it as "data infrastructure is healthy… the infrastructure isn't
   the problem". Absence of measurement reported as positive evidence, in the very
   sub-shape meant to rule infrastructure out. Seen on `ol` and `hvl`; all four
   ghosts share the shape. Either ops should be `None` when there is no import
   signal, or the narrative must say "not measured".
3. **§5.1 conflates never-activated with went-dark.** The ghost condition is ARR +
   zero 90-day logins, blind to lifetime history: `aa` (0 logins ever) and `bmc`
   (6,751 logins ever, org since 2011, just stopped) get the same flag, score and
   band but need opposite CS plays. A `ghost_subtype` off `active_users_365d`
   would separate them.
4. **Cache population has no automation and no credentials on disk.** All ~215 KB
   round-trips through an agent as text; `pg_domain_map.csv` alone is ~5,000 rows.
   The 2026-09-21 run produced three silent transcription errors, all caught only
   by the new README rule 8 checksum. A populate script would remove the whole
   risk class.
5. **agent-factory mirror is stale.** `agents/ceo_system/onboarding_reality/health_v3/`
   still has V3.3.0 weights hardcoded (25/20/35/20) and its `FACTORY.md` calls
   that "CS-authoritative". The Wednesday Windmill `fetch_early_life` job runs
   it. This repo's operator is now a clean superset — both have
   `--include-new-orgs`; only this one has `--weights` — so the merge is
   one-directional (copy here → there). **Until ported, that job scores with the
   rejected weights.**
6. **September MAL not yet used.** `inputs/master_account_list_2026-09-16_canonical.csv`
   (114 orgs, $1.97M ARR) is built and validated but no canonical has been run
   against it — that needs a fresh cache populate. The 2026-05-13 canonical
   correctly still uses the April MAL.
7. **BigQuery contradicts.** `insightful_product.at_risk_accounts` flags 79
   accounts (63 with zero ARR) and `segment_classifier` returns 86/35/48 against
   the stamped 56/28/20. Since T3 sells account health scoring, two disagreeing
   sources is a real exposure. `05_strategic_direction.md`'s "always-current
   health scores" claim needs correcting too.
8. **`subscriptions.custom_price` is mixed-unit.** `mah` and `kii` are stored at
   exactly 12× their monthly rate. Worth a ticket; it's a billing-data bug
   independent of health, and it's why MRR in the Sept MAL is carried forward
   from HubSpot rather than read from Postgres.
9. **README §9 is not closed.** The look-back ran on 11 outcome labels; the gate
   is 30. `outcomes.csv` should grow as churn and downgrades land.
10. **No `save_plays.md`.** Triggers emit a CS action per row, but the full
   save-play runbook (README §10) has not shipped.
11. **Stale iCloud fork.** `iCloud/SuperCat 4.0/Health V3/` still exists with none
   of the V3.4.0 work. Per `TRAP.md` this repo is the working tree; that copy
   will mislead anyone who opens it.
