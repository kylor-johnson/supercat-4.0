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

### V3.5.1 rescore (2026-09-21)

SHA: `c490040ccaafd909c99a204a030be1de356a7645a459a3019397e6a756f98350`. `ops_measurement` now requires both import health *and* freshness
(it previously ignored freshness), and `ghost_subtype` labels were renamed. No
composite score and no band changed.

