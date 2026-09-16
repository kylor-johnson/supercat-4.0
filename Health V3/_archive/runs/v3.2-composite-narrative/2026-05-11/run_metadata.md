# Health V3 run metadata — 2026-05-11

- Command: `python health_operator_v3.py --mal "../Health V2/inputs/master_account_list_2026-04-14_canonical.csv" --score-date 2026-05-11 --output-dir "runs/v3.2-composite-narrative"`
- MAL: `../Health V2/inputs/master_account_list_2026-04-14_canonical.csv`
- Output CSV: `runs/v3.2-composite-narrative/2026-05-11/client_health_scores_2026-05-11.csv`
- Rows scored: 104
- Rows skipped (new-org exclusion or not in Postgres): 0

## Distribution

Health band counts: {'Thriving': 53, 'Healthy': 33, 'Watch': 16, 'Critical': 1, 'At Risk': 1}
Scoring status counts: {'complete': 104}
Ghost accounts: 0
Behavioral floor applied: 7
Support fire flags: 9
Bundle/config mismatches: 3
