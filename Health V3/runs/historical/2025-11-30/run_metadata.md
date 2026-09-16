# Health V3 run metadata — 2025-11-30

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-04-14_canonical.csv" --score-date 2025-11-30 --cache --cache-dir "cache/historical/2025-11-30" --weights equal --output-dir "runs/historical"`
- MAL: `inputs/master_account_list_2026-04-14_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
- Output CSV: `runs/historical/2025-11-30/client_health_scores_2025-11-30.csv`
- Rows scored: 103
- Rows skipped (new-org exclusion or not in Postgres): 1

## Distribution

Health band counts: {'Thriving': 52, 'Healthy': 36, 'Watch': 12, 'At Risk': 3}
Scoring status counts: {'complete': 103}
Ghost accounts: 1
Behavioral floor applied: 10
Support fire flags: 0
Bundle/config mismatches: 3
