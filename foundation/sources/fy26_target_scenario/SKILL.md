---
name: fy26-target-scenario
description: >-
  FY26 annual target scenario model for SuperCat — quarterly goal metrics,
  monthly MRR waterfall, migration schedule analysis, growth levers, and
  sensitivity analysis. Use when the user asks about FY26 targets, revenue
  projections, migration scheduling scenarios, quarterly goals, implied ARR,
  subscription revenue forecasts, or the target scenario artifact on ceosystem.io.
---

# FY26 Target Scenario

## Purpose

Quantified FY26 financial plan for SuperCat, anchored to pricing migration of the 104-account install base, new logo acquisition (5/quarter), and organic expansion. Produces quarterly goal metrics, a 12-month MRR waterfall, revenue decomposition, growth levers, and sensitivity analysis.

**Current version: v3** (April 15, 2026). Q1 2026 locked to scorecard actuals; Q2-Q4 forecast from normalized Q1 run-rate ($161,481/mo). The HTML artifact includes an **interactive Migration Schedule Explorer** for Q2-Q4 cohort timing scenarios.

## Key Files

| File | What It Is |
|------|-----------|
| [data/fy26_target_scenario_calc.py](data/fy26_target_scenario_calc.py) | v3 Python computation engine. Q1 actuals locked, Q2-Q4 forecast. Source of truth for all numbers. |
| [data/fy26_target_scenario__v3.md](data/fy26_target_scenario__v3.md) | v3 markdown output — team/investor-facing. Q1 actuals + Q2-Q4 forecast. Anchor: all accounts Q3/Sep. |
| [data/fy26_target_scenario__v2.md](data/fy26_target_scenario__v2.md) | v2 markdown — superseded. Fully projected from derived platform MRR base. |
| [data/fy26_target_scenario__v1.md](data/fy26_target_scenario__v1.md) | v1 markdown — internal, with 30% threshold assessment. |
| [reports/fy26-target-scenario.html](reports/fy26-target-scenario.html) | v3 HTML artifact deployed to ceosystem.io/projects/fy26-target-scenario. Includes interactive explorer. |
| [reference/migration_cohort_data.md](reference/migration_cohort_data.md) | 6-cohort breakdown: accounts, deltas, churn rates, current/new MRR. Extracted from v5 migration revenue model. |

## How the Model Works (v3)

The v3 calc engine uses a **hybrid actuals + forecast** architecture:

### Q1 2026: Locked to Scorecard Actuals
- Jan: $163,771, Feb: $168,207, Mar: $152,464 (total: $484,442)
- March dip (NRR 90.64%) = seasonal user-fee reduction, not structural
- 1 new logo booked ($8,988 ARR), 4 logos churned (outside migration scope)
- End-of-Q1: 109 accounts

### Q2-Q4 2026: Forecast from Normalized Q1 Average
Starting MRR: $161,481 (Q1 trailing 3-month average — absorbs March trough and Jan-Feb peak)

Monthly waterfall components:
1. **Migration delta** — all 104 accounts in September. Gross +$30,379/mo, churn -$11,748/mo, net +$18,631/mo
2. **New logos** — 5/quarter at $1,125/mo MRR ($13.5K ACV)
3. **Tier upgrades** — 2x T1->T2 + 0.5x T2->T3 per quarter ($572/mo)
4. **Organic user expansion** — 2%/quarter on user-revenue portion (~22% of MRR)
5. **Background churn** — 0.53%/quarter (from 97.9% annual retention)
6. **Migration churn** — 4 accounts, $11,748/mo (additional to Q1 background churn)

### Key Metric Definitions

- **Subscription Revenue**: Q1 = scorecard actuals; Q2-Q4 = forecast. Recognized P&L revenue.
- **Implied ARR**: trailing 6-month average sub rev MRR x 12. Q1 uses scorecard value ($1,897,612).
- **ACV (derived)**: end-of-quarter ARR / active accounts.
- **Pricing MRR Growth**: incremental net migration delta produced *that quarter*.

## v3 Anchor Numbers

| Metric | FY26 Base | vs FY25 |
|---|---|---|
| Subscription Revenue | $2,120,139 | +15.2% |
| Implied ARR (6mo) | $2,273,726 | +23.4% |
| New Booked ARR | $273,300 | +13.9% |
| Year-End MRR | $201,663 | +24.5% |
| Year-End Accounts | 120 | +13.2% |
| Year-End ACV | $20,166 | +14.0% |

With churn suppression + floor pricing: Implied ARR reaches $2,414K (+31.1%).

## v3 vs v2 Changes

| What Changed | v2 | v3 | Why |
|---|---|---|---|
| Q1 data | Projected from $148,598 base | Scorecard actuals ($484,442) | 3 months of real data exist |
| Q2 starting point | Derived $153,390 | Normalized $161,481 | Q1 avg absorbs seasonal variance |
| Booked ARR | $352,416 (all projected) | $273,300 (Q1 actual + Q2-Q4 target) | Q1 booked only $8,988 |
| Starting accounts | 104 | 109 (Q1 end) | Reflects actual customer count |
| Explorer Q1 | Interactive | Locked to actuals | Q1 is done |

## Interactive Explorer (HTML)

The HTML artifact embeds a JS `runModel()` function that mirrors the Python calc. Q1 is locked to actuals. Six risk cohorts can each be assigned to Q2-Q4 (Q1 is disabled). The engine forecasts from the normalized Q1 MRR, runs the Q2-Q4 waterfall, and renders a comparison table with delta rows vs the anchor schedule.

Four presets:
- **Anchor** — all cohorts Q3/Sep (committed plan, 60-day notice July 1)
- **Accelerated** — safe cohorts Q2, risky Q3
- **Phased** — safe Q2, moderate Q3, significant Q4
- **Conservative** — risky cohorts deferred to Q4

## Relationship to Other Skills

- **monetization_refresh_2026**: Parent pricing program. The v5 migration revenue model provides cohort deltas, churn rates, and account-level data.
- **ceo_system**: HTML artifact deployed via ceosystem.io, follows SuperCat design system.
- **insightful_product**: ACV stress-testing used historical ARPU data.
- **fy26_goals_framework**: Chief-of-staff framework references v1 target scenario numbers; may need refresh to align with v3.

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2026-04-01 | Initial model — fully projected from derived platform MRR base |
| v2 | 2026-04-01 | Team/investor-facing reframe; derived ACV; interactive migration explorer |
| **v3** | **2026-04-15** | **Q1 locked to scorecard actuals; normalized Q2 start; recalibrated booked ARR and pipeline** |

## Running the Calc

```bash
cd skills/fy26_target_scenario/data
python3 fy26_target_scenario_calc.py
```

Output: Q1 actuals, normalized Q2 baseline, monthly waterfall, quarterly goal metrics, FY26 annual totals, growth levers, and v3-vs-v2 comparison.
