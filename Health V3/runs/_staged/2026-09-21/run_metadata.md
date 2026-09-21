# Health V3 run metadata — 2026-09-21

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-09-16_canonical.csv" --score-date 2026-09-21 --cache --cache-dir "cache/2026-09-21" --weights equal --output-dir "runs"`
- MAL: `inputs/master_account_list_2026-09-16_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
- New-org window: excluded (90-day gate)
- Output CSV: `runs/2026-09-21/client_health_scores_2026-09-21.csv`
- Rows scored: 114
- Rows skipped (new-org exclusion or not in Postgres): 0

## Distribution

Health band counts: {'Thriving': 52, 'Healthy': 40, 'Watch': 14, 'Critical': 4, 'At Risk': 4}
Scoring status counts: {'complete': 114}
Ghost accounts: 4
Behavioral floor applied: 14
Support fire flags: 1
Bundle/config mismatches: 0
