# Health V3 run metadata — 2025-11-30

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-04-14_canonical.csv" --score-date 2025-11-30 --cache --cache-dir "cache/historical/2025-11-30" --weights equal --output-dir "runs/historical"`
- MAL: `inputs/master_account_list_2026-04-14_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
- Output CSV: `runs/historical/2025-11-30/client_health_scores_2025-11-30.csv`
- Rows scored: 103
- Rows skipped (new-org exclusion or not in Postgres): 1

## Distribution

Health band counts: {'Thriving': 52, 'Healthy': 36, 'Watch': 12, 'At Risk': 3}
Scoring status counts: {'complete': 103}
Ghost accounts: 1
Behavioral floor applied: 10
Support fire flags: 0
Bundle/config mismatches: 3

---

## Historical-run provenance (carried forward from the original run)

These runs are **approximate**, per `HISTORICAL_RUN_GUIDE.md`. Regenerated
2026-09-16 under V3.4.0 (equal weights) and the pinned interpreter; the
limitations below are unchanged and still apply.

## Known limitations
- **Adoption** — feature flags reflect current config, not historical (`pg_org_config.csv` was not date-filtered).
- **Catalog completeness** — reflects today's catalog state (`pg_catalog.csv` has no `as_of` filter on `products`), not Nov 2025.
- **Smart Stacks** — `pg_smart_stacks.csv` has no date filter; counts reflect current state, not Nov 2025.
- **Support Fire** — only conversations created on or before 2025-11-30 that are *still* `active`/`pending` today are captured. Fires that have been resolved since 2025-11-30 do not appear, so this dimension structurally underreports for historical runs. (Helpscout query returned 0 rows, as expected per methodology note.)
- **MAL** — uses 2026-04-14 master account list; orgs added after 4/14/2026 or removed before that date will be misclassified relative to their actual 2025-11-30 status.

## Determinism

- SHA-256 (V3.4.0, equal weights): `e0931bf5664c89f6d2b84414629e8147f1c1fe5136a52b6b5d44db19132ce029`
- Regenerated 2026-09-16 under Python 3.9.6 / pandas 2.3.3 / numpy 2.0.2.
- Drift vs the original stored run was +/-0.1 on a handful of composites
  with **zero band changes** — see `ENVIRONMENT.md`.

