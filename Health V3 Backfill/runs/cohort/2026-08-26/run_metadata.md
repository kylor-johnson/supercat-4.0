# Health V3 run metadata — 2026-08-26

- Command: `python health_operator_v3.py --mal "inputs/cohort_mal_2026-08-26.csv" --score-date 2026-08-26 --cache --cache-dir "cache/cohort/2026-08-26" --output-dir "runs/cohort"`
- MAL: `inputs/cohort_mal_2026-08-26.csv`
- Output CSV: `runs/cohort/2026-08-26/client_health_scores_2026-08-26.csv`
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

## Cohort run — provenance and limitations

**This is an isolated cohort run, not a canonical scorecard.** It scores six orgs that are
absent from the canonical MAL (`master_account_list_2026-04-14_canonical.csv`, 104 orgs,
cohort_year 2011–2025). None of these six appear in the canonical 104, so this run does not
overlap or conflict with the production canonical.

- Canonical SHA-256: `381e690c4798e373829496734aa95b369eb8293b8b2fceb576ebc9ed22c1faec`
- Determinism: two consecutive passes over the same cache produced byte-identical output.
- Cohort defined by the user on 2026-08-26: `cst`, `mali`, `tcd`, `libco`, `drf`, `pebl`.

### Cohort MAL construction

The MAL at `inputs/cohort_mal_2026-08-26.csv` was purpose-built for this run, since none of
the six orgs are in the canonical MAL.

| Field | Source |
|-------|--------|
| `ord_id` | Postgres `organizations.shortname` |
| `company` | HubSpot deal company name (Postgres `organizations.name` differs for `pebl`: legal entity "Skyard Furniture Co Ltd." vs. trading name "Pebl Furniture") |
| `stack` | Derived from live Postgres config (`mobile_sites.enable_online_catalog / enable_online_ordering / enable_sales_portal`), not from a contracted-bundle record |
| `mrr` / `arr` | HubSpot closed-won deal `properties_hs_mrr` / `properties_hs_arr` |
| `cohort_year` | Year of HubSpot closed-won `closedate` |

**Limitation — bundle is inferred, not contracted.** The canonical MAL carries a curated
`stack` value per account. No such record exists for these six, so bundle was derived from
current feature flags. Bundle affects only the inflated-denominator adjustment
(`INFLATED_DENOM_BUNDLES`) and the `bundle_config_mismatch` flag; because bundle was derived
*from* config, `bundle_config_mismatch` is structurally False for all six and carries no
signal in this run.

**Limitation — ARR is deal-stated, not invoiced.** ARR comes from the HubSpot deal record,
not from QuickBooks invoiced revenue. ARR feeds only the §5.1 ghost-account override
(ARR ≥ $5,000 with zero 90-day logins); no org here has zero logins, so no ghost override
fired and the ARR figures did not affect any score.

### Cache provenance

`cache/cohort/2026-08-26/` — all 10 files, populated via MCP on 2026-08-26 using the loader
SQL in `health_operator_v3.py` verbatim, with `NOW()`-anchored trailing windows left intact
(this is a present-day run, so no historical date substitution was applied).

**Scope note:** the per-org Postgres files are filtered to the six cohort orgs
(`organization_id IN (275, 282, 285, 287, 288, 290)`) rather than pulled org-wide. The
operator reads these by indexed lookup per MAL org, so the filtering cannot change any score.
`pg_domain_map.csv` was ranked globally across all orgs *before* filtering to the six, which
preserves the winner-per-domain semantics of the live query.
`bq_helpscout_fires.csv` is unfiltered (all 3 open fire-flagged domains). None of them map to
a cohort org, so all six show `support_fire = False`.

**Limitation — populate window.** Cache files were written over roughly a 10-minute window
while the source systems were live; `cst` login counts moved by 1–2 between probes. The cache
is immutable once written, so the run is deterministic against it, but the six orgs are not
all frozen at the same instant.

### Data-quality flags carried in the output

- `pebl` and `drf` show `denominator_quality = stale`: `active_users_90d` exceeds
  `enabled_users` (22 of 13, 8 of 7). Users who logged in during the window have since been
  disabled or moved. Read the "% of reps active" phrasing in those two narratives with that
  in mind — the login counts themselves are sound.
- `tcd` contributes no rows to `pg_domain_map.csv` (no non-generic domain with ≥2 users), so
  it could not be matched to a support conversation even if one existed.
- Ops-health catalog completeness reflects the catalog as of the populate time, which is
  correct for a present-day run (unlike the historical backfills in `runs/historical/`).

### 90-day new-org gate

All six cleared it — days since first login: `pebl` 390, `tcd` 303, `mali` 246, `cst` 246,
`libco` 154, `drf` 121. Zero orgs skipped. No operator patch or provisional-scoring bypass
was needed, and `health_operator_v3.py` was not modified.

### Environment note

The `.venv` in this folder was broken before this run (it pointed at a Homebrew
`python@3.14` that no longer exists on this machine; the production `Health V3/.venv` is
broken the same way). It was rebuilt against `/usr/bin/python3` with
`--system-site-packages` (pandas 2.3.3, numpy 2.0.2). The old one is preserved at
`.venv_broken_python314/`. Production `Health V3/` was not touched.

### Engine-version caveat — read before using these composites

This run used **this clone's** operator (V3.2.x, unweighted mean of the four dimensions).
Production's operator was updated on 2026-06-08 to **V3.3.0**, which weights the dimensions
ENG 0.25 / ADO 0.20 / VAL 0.35 / OPS 0.20 ("validated against 7-month backfill" per the code
comment). The clone was never updated to match.

A parallel run of the same cache and MAL through the production V3.3.0 engine is at
`runs/cohort_v330/2026-08-26/`. Dimension scores are identical; composites differ by −3.3 to
+1.6 and **no org changes band**. Use the `cohort_v330` output when comparing these six against
the current production canonical.
