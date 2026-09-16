# Health V3 run metadata — 2026-06-12

- Command: `python health_operator_v3.py --mal "../Health V2/inputs/master_account_list_2026-04-14_canonical.csv" --score-date 2026-06-12 --output-dir "runs/_test_future_date"`
- MAL: `../Health V2/inputs/master_account_list_2026-04-14_canonical.csv`
- Output CSV: `runs/_test_future_date/2026-06-12/client_health_scores_2026-06-12.csv`
- Rows scored: 104
- Rows skipped (new-org exclusion or not in Postgres): 0

## Distribution

Health band counts: {'Healthy': 44, 'Thriving': 36, 'Watch': 21, 'At Risk': 2, 'Critical': 1}
Scoring status counts: {'complete': 104}
Ghost accounts: 0
Behavioral floor applied: 7
Support fire flags: 9
Bundle/config mismatches: 3
