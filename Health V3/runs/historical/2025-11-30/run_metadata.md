# Health V3 run metadata — 2025-11-30

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-04-14_canonical.csv" --score-date 2025-11-30 --cache --cache-dir "cache/historical/2025-11-30" --weights equal --output-dir "runs/historical"`
- MAL: `inputs/master_account_list_2026-04-14_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
- New-org window: excluded (90-day gate)
- Output CSV: `runs/historical/2025-11-30/client_health_scores_2025-11-30.csv`
- Rows scored: 103
- Rows skipped (new-org exclusion or not in Postgres): 1

## Distribution

Health band counts: {'Thriving': 52, 'Healthy': 36, 'Watch': 12, 'At Risk': 2, 'Critical': 1}
Scoring status counts: {'complete': 103}
Ghost accounts: 1
Behavioral floor applied: 10
Support fire flags: 0
Bundle/config mismatches: 3

### V3.5.0 rescore (2026-09-21)

Schema change: `ghost_subtype` and `ops_measurement` added (28 → 30 columns), so
every SHA in the series moved. No composite score and no band changed anywhere in
this month; the only value edits are `operational_health_narrative` for orgs with
no import feed, which now disclose that import health and freshness are unmeasured.

- V3.5.0 SHA: `4954b41cde4b10e4a7c7bf877b5c7837d896d8e54f42979c1def89516e5bf70e`
- Interpreter unchanged (Python 3.9.6 / pandas 2.3.3 / numpy 2.0.2)

