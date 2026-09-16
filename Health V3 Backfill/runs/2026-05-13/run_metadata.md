# Health V3 run metadata — 2026-05-13

- Command: `python health_operator_v3.py --mal "../Health V2/inputs/master_account_list_2026-04-14_canonical.csv" --score-date 2026-05-13 --cache --cache-dir "cache/2026-05-13" --output-dir "runs/2026-05-13"`
- MAL: `../Health V2/inputs/master_account_list_2026-04-14_canonical.csv`
- Output CSV: `runs/2026-05-13/client_health_scores_2026-05-13.csv`
- Rows scored: 104
- Rows skipped (new-org exclusion or not in Postgres): 0

## Distribution

Health band counts: {'Thriving': 57, 'Healthy': 31, 'Watch': 14, 'Critical': 1, 'At Risk': 1}
Scoring status counts: {'complete': 104}
Ghost accounts: 0
Behavioral floor applied: 7
Support fire flags: 9
Bundle/config mismatches: 3
