# Health V3 run metadata — 2026-01-31

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-04-14_canonical.csv" --score-date 2026-01-31 --cache --cache-dir "cache/historical/2026-01-31" --weights equal --output-dir "runs/historical"`
- MAL: `inputs/master_account_list_2026-04-14_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
- New-org window: excluded (90-day gate)
- Output CSV: `runs/historical/2026-01-31/client_health_scores_2026-01-31.csv`
- Rows scored: 103
- Rows skipped (new-org exclusion or not in Postgres): 1

## Distribution

Health band counts: {'Thriving': 57, 'Healthy': 35, 'Watch': 8, 'At Risk': 3}
Scoring status counts: {'complete': 103}
Ghost accounts: 0
Behavioral floor applied: 6
Support fire flags: 0
Bundle/config mismatches: 3

### V3.5.0 rescore (2026-09-21)

Schema change: `ghost_subtype` and `ops_measurement` added (28 → 30 columns), so
every SHA in the series moved. No composite score and no band changed anywhere in
this month; the only value edits are `operational_health_narrative` for orgs with
no import feed, which now disclose that import health and freshness are unmeasured.

- V3.5.0 SHA: `1c1a173ae31efee0b868eb36de1a67d00283cf97239d27892dbd5bf5b9988cbc`
- Interpreter unchanged (Python 3.9.6 / pandas 2.3.3 / numpy 2.0.2)

