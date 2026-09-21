# Health V3 run metadata — 2025-11-30

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-04-14_canonical.csv" --score-date 2025-11-30 --cache --cache-dir "cache/historical/2025-11-30" --weights equal --output-dir "runs/historical"`
- MAL: `inputs/master_account_list_2026-04-14_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
- New-org window: excluded (90-day gate)
- Output CSV: `runs/historical/2025-11-30/client_health_scores_2025-11-30.csv`
- Rows scored: 103
- Rows skipped (new-org exclusion or not in Postgres): 1

## Distribution

Health band counts: {'Thriving': 52, 'Healthy': 36, 'Watch': 12, 'At Risk': 2, 'Critical': 1}
Scoring status counts: {'complete': 103}
Ghost accounts: 1
Behavioral floor applied: 10
Support fire flags: 0
Bundle/config mismatches: 3

### V3.5.1 rescore (2026-09-21)

SHA: `4d55f899dd6fdd334b0c9eb5b409c27f4e635dbd67f97f48e52d29ac408dfc68`. `ops_measurement` now requires both import health *and* freshness
(it previously ignored freshness), and `ghost_subtype` labels were renamed. No
composite score and no band changed.

