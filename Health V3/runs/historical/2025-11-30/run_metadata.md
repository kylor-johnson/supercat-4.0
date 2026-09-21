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

### V3.4.1 correction (2026-09-21)

Rescored under V3.4.1. `prog` ($25,200 ARR, zero logins in the trailing 90 days)
was correctly flagged `ghost_account = true` but banded **At Risk**, because
`GHOST_CAP` is 20 and 20 is the At Risk floor. §5.1 requires Critical. The band
is now assigned directly, so `prog` reads Critical here.

- Prior SHA: `e0931bf5664c89f6d2b84414629e8147f1c1fe5136a52b6b5d44db19132ce029`
- V3.4.1 SHA: `e818042bccf0613b2449dd51d352f3d6a6f3f3639bf06888d4833912e0930a39`
- One cell changed. No composite score moved; no other org affected.

