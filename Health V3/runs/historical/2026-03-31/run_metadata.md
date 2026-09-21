# Health V3 run metadata — 2026-03-31

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-04-14_canonical.csv" --score-date 2026-03-31 --cache --cache-dir "cache/historical/2026-03-31" --weights equal --output-dir "runs/historical"`
- MAL: `inputs/master_account_list_2026-04-14_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
- New-org window: excluded (90-day gate)
- Output CSV: `runs/historical/2026-03-31/client_health_scores_2026-03-31.csv`
- Rows scored: 104
- Rows skipped (new-org exclusion or not in Postgres): 0

## Distribution

Health band counts: {'Thriving': 59, 'Healthy': 32, 'Watch': 10, 'At Risk': 2, 'Critical': 1}
Scoring status counts: {'complete': 104}
Ghost accounts: 0
Behavioral floor applied: 9
Support fire flags: 0
Bundle/config mismatches: 3

### V3.5.0 rescore (2026-09-21)

Schema change: `ghost_subtype` and `ops_measurement` added (28 → 30 columns), so
every SHA in the series moved. No composite score and no band changed anywhere in
this month; the only value edits are `operational_health_narrative` for orgs with
no import feed, which now disclose that import health and freshness are unmeasured.

- V3.5.0 SHA: `b688f7da038f4c9b621d331f3e783ec56e543b830aceed4edee09fad11368c42`
- Interpreter unchanged (Python 3.9.6 / pandas 2.3.3 / numpy 2.0.2)

