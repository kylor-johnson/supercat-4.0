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

---

## Historical-run provenance (carried forward from the original run)

These runs are **approximate**, per `HISTORICAL_RUN_GUIDE.md`. Regenerated
2026-09-16 under V3.4.0 (equal weights) and the pinned interpreter; the
limitations below are unchanged and still apply.

## Known limitations
- Adoption — feature flags reflect current config, not historical.
- Catalog completeness — reflects today's catalog state, not Mar 2026.
- Support Fire — only conversations created ≤ 2026-03-31 still open today are captured. For this run `bq_helpscout_fires.csv` returned 0 rows (header-only), so no support-fire flags were applied for any org on 2026-03-31.
- MAL — uses 2026-04-14 MAL.

## Determinism

- SHA-256 (V3.4.0, equal weights): `c2e1ee644480cb8f667b6b30c075c592904a2d4036cd5eb692f9a5dc349feebb`
- Regenerated 2026-09-16 under Python 3.9.6 / pandas 2.3.3 / numpy 2.0.2.
- Drift vs the original stored run was +/-0.1 on a handful of composites
  with **zero band changes** — see `ENVIRONMENT.md`.

