# Health V3 run metadata — 2026-01-31

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-04-14_canonical.csv" --score-date 2026-01-31 --cache --cache-dir "cache/historical/2026-01-31" --weights equal --output-dir "runs/historical"`
- MAL: `inputs/master_account_list_2026-04-14_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
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

---

## Historical-run provenance (carried forward from the original run)

These runs are **approximate**, per `HISTORICAL_RUN_GUIDE.md`. Regenerated
2026-09-16 under V3.4.0 (equal weights) and the pinned interpreter; the
limitations below are unchanged and still apply.

## Known limitations
- **Adoption** — feature flags reflect current config, not historical (cache file `pg_org_config.csv` has no date filter).
- **Catalog completeness** — reflects today's catalog state, not Jan 2026 (cache file `pg_catalog.csv` has no date filter).
- **Support Fire** — only conversations created ≤ 2026-01-31 still open today are captured; for this run `bq_helpscout_fires.csv` returned 0 rows, so support fire flags = 0.
- **MAL** — uses 2026-04-14 MAL, not a Jan 2026 MAL snapshot.

## Determinism

- SHA-256 (V3.4.0, equal weights): `649c0275e38aff2be78fbccfbfa2d000305a3707070fa7cd2ddfe1061687f56d`
- Regenerated 2026-09-16 under Python 3.9.6 / pandas 2.3.3 / numpy 2.0.2.
- Drift vs the original stored run was +/-0.1 on a handful of composites
  with **zero band changes** — see `ENVIRONMENT.md`.

