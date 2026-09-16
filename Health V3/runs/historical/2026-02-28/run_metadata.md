# Health V3 run metadata — 2026-02-28

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-04-14_canonical.csv" --score-date 2026-02-28 --cache --cache-dir "cache/historical/2026-02-28" --weights equal --output-dir "runs/historical"`
- MAL: `inputs/master_account_list_2026-04-14_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
- Output CSV: `runs/historical/2026-02-28/client_health_scores_2026-02-28.csv`
- Rows scored: 103
- Rows skipped (new-org exclusion or not in Postgres): 1

## Distribution

Health band counts: {'Thriving': 56, 'Healthy': 34, 'Watch': 11, 'At Risk': 2}
Scoring status counts: {'complete': 103}
Ghost accounts: 0
Behavioral floor applied: 8
Support fire flags: 0
Bundle/config mismatches: 3

---

## Historical-run provenance (carried forward from the original run)

These runs are **approximate**, per `HISTORICAL_RUN_GUIDE.md`. Regenerated
2026-09-16 under V3.4.0 (equal weights) and the pinned interpreter; the
limitations below are unchanged and still apply.

## Known limitations
- Adoption — feature flags reflect current config, not historical.
- Catalog completeness — reflects today's catalog state, not Feb 2026.
- Support Fire — only conversations created ≤ 2026-02-28 still open today are captured (zero captured in this run).
- MAL — uses 2026-04-14 MAL.

## Determinism

- SHA-256 (V3.4.0, equal weights): `842c6289de61dff21062ce1f369208b6b2968972a7ec25c94986024c1d4185cd`
- Regenerated 2026-09-16 under Python 3.9.6 / pandas 2.3.3 / numpy 2.0.2.
- Drift vs the original stored run was +/-0.1 on a handful of composites
  with **zero band changes** — see `ENVIRONMENT.md`.

