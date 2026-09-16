# Health V3 run metadata — 2026-03-31

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-04-14_canonical.csv" --score-date 2026-03-31 --cache --cache-dir "cache/historical/2026-03-31" --weights equal --output-dir "runs/historical"`
- MAL: `inputs/master_account_list_2026-04-14_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
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
