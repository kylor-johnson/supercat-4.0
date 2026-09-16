# Health V3 run metadata — 2026-08-26

- Command: `python health_operator_v3.py --mal "inputs/cohort_mal_2026-08-26.csv" --score-date 2026-08-26 --cache --cache-dir "cache/cohort/2026-08-26" --output-dir "runs/cohort_v330"`
- MAL: `inputs/cohort_mal_2026-08-26.csv`
- Output CSV: `runs/cohort_v330/2026-08-26/client_health_scores_2026-08-26.csv`
- Rows scored: 6
- Rows skipped (new-org exclusion or not in Postgres): 0

## Distribution

Health band counts: {'Healthy': 3, 'Thriving': 2, 'At Risk': 1}
Scoring status counts: {'complete': 6}
Ghost accounts: 0
Behavioral floor applied: 1
Support fire flags: 0
Bundle/config mismatches: 0

---

## Cohort run — V3.3.0 weighted engine

Same six orgs, same cache, same MAL as `runs/cohort/2026-08-26/`. The only difference is the
scoring engine: this run used the **production** operator (`../Health V3/health_operator_v3.py`,
V3.3.0, weighted composite ENG 0.25 / ADO 0.20 / VAL 0.35 / OPS 0.20), whereas
`runs/cohort/2026-08-26/` used this clone's operator (V3.2.x, unweighted mean of the four
dimensions).

- SHA-256: `8d878c0b5610601e8e8900b898fc4f44f2fda83bb73d43ea8e9d43550d8d5569`
- Determinism: two consecutive passes byte-identical.
- The production operator was **read only** — invoked by path, all output written here.
  `Health V3/` was not modified (verified by SHA before and after).
- Dimension scores are identical across both engines; only the composite differs.
- **Zero band changes** between the two engines. Composite deltas: `pebl` +1.6, `tcd` 0.0,
  `cst` −0.8, `libco` −1.4, `mali` −2.8, `drf` −3.3.

**Use this run** for any comparison against the current production canonical, which is
V3.3.0-weighted. See the provenance and limitations section in
`runs/cohort/2026-08-26/run_metadata.md` — every note there applies to this run as well.
