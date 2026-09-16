# Health V3 Backfill — Historical Run Guide

**This folder is an isolated clone of `Health V3/` for historical backfill work only.**

The production folder (`Health V3/`) must never be touched during this work. The production canonical SHA is `b48e3a5f7354ee8d769b764e24ca6195a2424ec5f1416891da9877d6011efcb8`. If you ever need to verify production is intact, run:

    shasum -a 256 "../Health V3/runs/2026-05-13/client_health_scores_2026-05-13.csv"

It must always return `b48e3a5f…`. If it doesn't, stop everything.

---

## Purpose

Produce approximate historical scorecards for Nov 2025 – Apr 2026 to enable:

1. Month-over-month trigger detection (V3.3) from day one of the June 2026 run
2. A directional look-back study on dimension weighting (§9 of README.md)

All outputs from this work live under `runs/historical/` and `cache/historical/` in **this folder only**. Nothing here gets written back to the production `Health V3/` folder except the final historical canonical CSVs, which are copied (not moved) after analysis.

---

## Known limitations of historical runs

These runs are approximate. Document these limitations in every `run_metadata.md` produced here:

| Dimension | Limitation |
|-----------|------------|
| Engagement | Accurate — login_events are timestamped, trailing windows are correctly anchored |
| Adoption | Approximately accurate — feature flags (`mobile_sites`) reflect current config, not historical. An org that disabled a feature since November will show it as currently disabled, potentially understating their historical adoption. |
| Value Delivery | Accurate — orders and portal_orders are timestamped |
| Ops Health (imports) | Accurate — import_events are timestamped |
| Ops Health (catalog) | **Not historical** — catalog completeness reflects today's catalog, not the historical state. Treat ops scores as approximate for catalog-heavy orgs. |
| Support Fire | Approximately accurate — queries only open conversations; conversations opened before the window and still open appear; conversations that were open then but closed since do not. |
| MAL | **Current MAL only** — orgs that churned and were removed from the MAL won't appear in historical runs. New orgs added to the MAL after the historical date will appear (but are likely gated by new-org exclusion if their first login is after the score date). |

---

## Directory structure

```
Health V3 Backfill/
├── cache/
│   ├── 2026-05-13/          ← Copy of production cache (reference only — do not modify)
│   └── historical/
│       ├── 2025-11-30/      ← 10 cache CSVs for November 2025 run
│       ├── 2025-12-31/      ← etc.
│       ├── 2026-01-31/
│       ├── 2026-02-28/
│       ├── 2026-03-31/
│       └── 2026-04-30/
├── runs/
│   ├── 2026-05-13/          ← Copy of production run (reference only — do not modify)
│   └── historical/
│       ├── 2025-11-30/      ← canonical + formatted CSV + run_metadata.md
│       └── ...
```

---

## How to populate a historical cache

For each historical score date, use the Cursor MCP tools (`user-supercat-postgres-vpn`, `user-bigquery-vpn`) to query the data with historical date bounds. Run these queries via MCP and save results as CSVs to `cache/historical/{date}/`.

**The historical cutoff date substitution rule:**

In every query, replace trailing-window anchors with explicit date bounds:
- `NOW() - INTERVAL '90 days'` → `'{score_date}'::date - INTERVAL '90 days'`
- `NOW()` → `'{score_date}'::date`
- `CURRENT_DATE - INTERVAL '90 days'` → `'{score_date}'::date - INTERVAL '90 days'`
- BigQuery `CURRENT_DATE()` → `DATE('{score_date}')`

The 10 cache files required and their source queries are in `health_operator_v3.py`. Read each loader function verbatim for the SQL. Apply the date substitution above to every trailing-window filter.

**Score dates to target (last day of each month):**

| Score date | Cache directory |
|------------|----------------|
| 2025-11-30 | cache/historical/2025-11-30/ |
| 2025-12-31 | cache/historical/2025-12-31/ |
| 2026-01-31 | cache/historical/2026-01-31/ |
| 2026-02-28 | cache/historical/2026-02-28/ |
| 2026-03-31 | cache/historical/2026-03-31/ |
| 2026-04-30 | cache/historical/2026-04-30/ |

---

## How to run the operator for a historical date

Once the cache for a date is populated (all 10 files present):

    cd "Health V3 Backfill"

    .venv/bin/python3 health_operator_v3.py \
      --mal "../Health V2/inputs/master_account_list_2026-04-14_canonical.csv" \
      --score-date {score_date} \
      --cache --cache-dir "cache/historical/{score_date}" \
      --output-dir "runs/historical/{score_date}"

Run it twice and SHA both outputs — they must be byte-identical (determinism check).

Each `runs/historical/{date}/` directory should contain:
- `client_health_scores_{date}.csv`
- `client_health_scores_{date}_formatted.csv`
- `run_metadata.md` — record the SHA, row count, distribution, and the limitations note above

---

## What to do when all 6 historical runs are complete

1. Verify the production canonical is still untouched: `shasum -a 256 "../Health V3/runs/2026-05-13/client_health_scores_2026-05-13.csv"` must return `b48e3a5f…`
2. Copy (do not move) the 6 historical canonical CSVs to `../Health V3/runs/historical/{date}/` in the production folder — these become the reference data for V3.3 trigger detection
3. Run the look-back validation study (see below)
4. Report findings back to the orchestrator before any production operator changes

---

## Look-back validation study (dimension weighting)

Once all 6 historical runs exist, if you have labeled churn/retention outcomes for Nov 2025–Apr 2026:

1. For each labeled org, record: `org_shortname`, `outcome` (churned / retained / expanded), `outcome_date`
2. Join to the historical canonical closest to 90 days before the outcome date
3. Compute correlation of each dimension score with the binary churn outcome, stratified by bundle (iPad-only, Catalog, Cart/Full) — see README §9 for the full protocol
4. Report: does any weighting scheme improve AUC by ≥ 0.05 vs 25/25/25/25, AND does it hold across ≥ 2 bundle strata?
5. Treat result as directional only (§9) — cannot trigger a production weight change without the full prospective validation

---

## Hard constraints

- **Never write to `../Health V3/`** during historical work. Every output goes to this clone.
- **Never modify** `cache/2026-05-13/` or `runs/2026-05-13/` in this clone — those are the production reference copies.
- **Document limitations** in every `run_metadata.md` — these are approximate runs, not canonical.
- If anything behaves unexpectedly, stop and report to the orchestrator before continuing.
