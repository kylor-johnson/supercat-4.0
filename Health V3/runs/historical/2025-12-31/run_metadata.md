# Health V3 run metadata — 2025-12-31

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-04-14_canonical.csv" --score-date 2025-12-31 --cache --cache-dir "cache/historical/2025-12-31" --weights equal --output-dir "runs/historical"`
- MAL: `inputs/master_account_list_2026-04-14_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
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

---

## Historical-run provenance (carried forward from the original run)

These runs are **approximate**, per `HISTORICAL_RUN_GUIDE.md`. Regenerated
2026-09-16 under V3.4.0 (equal weights) and the pinned interpreter; the
limitations below are unchanged and still apply.

## Known limitations
- **Adoption** — feature flags reflect current org config, not the historical state on 2025-12-31.
- **Catalog completeness** — reflects today's catalog state, not Dec 2025.
- **Support Fire** — only Help Scout conversations created on or before 2025-12-31 that remain open today are captured (yields 0 domains for this score date).
- **MAL** — uses the 2026-04-14 canonical MAL (no historical MAL snapshot is available).

## Determinism

- SHA-256 (V3.4.0, equal weights): `9f4fb466ef70b0d4cb58f902964b96e759a5e457593042e1559cd74046848bd2`
- Regenerated 2026-09-16 under Python 3.9.6 / pandas 2.3.3 / numpy 2.0.2.
- Drift vs the original stored run was +/-0.1 on a handful of composites
  with **zero band changes** — see `ENVIRONMENT.md`.

