# Health V3 run metadata — 2025-12-31

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-04-14_canonical.csv" --score-date 2025-12-31 --cache --cache-dir "cache/historical/2025-12-31" --weights equal --output-dir "runs/historical"`
- MAL: `inputs/master_account_list_2026-04-14_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
- New-org window: excluded (90-day gate)
- Output CSV: `runs/historical/2025-12-31/client_health_scores_2025-12-31.csv`
- Rows scored: 102
- Rows skipped (new-org exclusion or not in Postgres): 2

## Distribution

Health band counts: {'Thriving': 53, 'Healthy': 33, 'Watch': 14, 'At Risk': 2}
Scoring status counts: {'complete': 102}
Ghost accounts: 0
Behavioral floor applied: 8
Support fire flags: 0
Bundle/config mismatches: 3

### V3.5.1 rescore (2026-09-21)

SHA: `2f25ff38566ba770c452ecbe527a9ab69d5d494cc6274131685f7a6308d7d209`. `ops_measurement` now requires both import health *and* freshness
(it previously ignored freshness), and `ghost_subtype` labels were renamed. No
composite score and no band changed.

