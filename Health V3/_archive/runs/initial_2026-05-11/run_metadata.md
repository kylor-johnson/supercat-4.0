# Health V3 run metadata — 2026-05-11

- Command: `python health_operator_v3.py --mal "Health V2/inputs/master_account_list_2026-04-14_canonical.csv" --score-date 2026-05-11 --output-dir "Health V3/runs"`
- MAL: `Health V2/inputs/master_account_list_2026-04-14_canonical.csv`
- Output CSV: `Health V3/runs/2026-05-11/client_health_scores_2026-05-11.csv`
- Rows scored: 104
- Rows skipped (new-org exclusion or not in Postgres): 0

## Distribution

Health band counts: {'Thriving': 55, 'Healthy': 36, 'Watch': 11, 'Critical': 1, 'At Risk': 1}
Scoring status counts: {'complete': 104}
Ghost accounts: 0
Support fire flags: 9
Bundle/config mismatches: 3
