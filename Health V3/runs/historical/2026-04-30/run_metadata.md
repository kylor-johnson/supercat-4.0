# Health V3 run metadata — 2026-04-30

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-04-14_canonical.csv" --score-date 2026-04-30 --cache --cache-dir "cache/historical/2026-04-30" --weights equal --output-dir "runs/historical"`
- MAL: `inputs/master_account_list_2026-04-14_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
- Output CSV: `runs/historical/2026-04-30/client_health_scores_2026-04-30.csv`
- Rows scored: 104
- Rows skipped (new-org exclusion or not in Postgres): 0

## Distribution

Health band counts: {'Thriving': 59, 'Healthy': 28, 'Watch': 15, 'Critical': 1, 'At Risk': 1}
Scoring status counts: {'complete': 104}
Ghost accounts: 0
Behavioral floor applied: 10
Support fire flags: 1
Bundle/config mismatches: 3

---

## Historical-run provenance (carried forward from the original run)

These runs are **approximate**, per `HISTORICAL_RUN_GUIDE.md`. Regenerated
2026-09-16 under V3.4.0 (equal weights) and the pinned interpreter; the
limitations below are unchanged and still apply.

## Known limitations (apply to all historical runs)
- **Adoption** — feature flags reflect current config, not historical. Orgs that changed features since Apr 2026 may have understated/overstated adoption scores.
- **Catalog completeness** — reflects today's catalog state. Not historical. Treat ops scores as approximate for catalog-heavy orgs.
- **Support Fire** — only open conversations visible. Conversations opened before 2026-04-30 and since closed do not appear; conversations opened after 2026-04-30 are excluded by the createdAt <= cutoff filter.
- **MAL** — uses the 2026-04-14 MAL. Orgs added or removed after that date are affected accordingly.

## Determinism

- SHA-256 (V3.4.0, equal weights): `f23d12aa6d79193198812a5275218ccf4fba7938be02d5bfa726ee077b617179`
- Regenerated 2026-09-16 under Python 3.9.6 / pandas 2.3.3 / numpy 2.0.2.
- Drift vs the original stored run was +/-0.1 on a handful of composites
  with **zero band changes** — see `ENVIRONMENT.md`.

