# Run Metadata — 2026-03-31 (Historical Backfill)

| Field | Value |
|-------|-------|
| Score date | 2026-03-31 |
| Operator version | V3.2.13 (CHANGELOG; doc-only since V3.2.12 — scoring math unchanged) |
| Run type | Historical backfill (cache mode) |
| Canonical SHA | 83d9942185d16d63072483709a89e05a133f71b72021c2bdc4c08974d285dc6c |
| Row count (canonical) | 104 |
| Row count (formatted) | 104 |
| Run timestamp | 2026-05-13T23:17:59Z |

## Score distribution

| Band | Count |
|------|-------|
| Thriving | 59 |
| Healthy | 32 |
| Watch | 10 |
| At Risk | 2 |
| Critical | 1 |

(Operator emits 5 bands; spec template listed 4. "At Risk" is the operator's label, not "At-Risk".)

## Known limitations

- Adoption — feature flags reflect current config, not historical.
- Catalog completeness — reflects today's catalog state, not Mar 2026.
- Support Fire — only conversations created ≤ 2026-03-31 still open today are captured. For this run `bq_helpscout_fires.csv` returned 0 rows (header-only), so no support-fire flags were applied for any org on 2026-03-31.
- MAL — uses 2026-04-14 MAL.

## Determinism

Run 1 SHA = Run 2 SHA: YES

- Run 1 SHA: `83d9942185d16d63072483709a89e05a133f71b72021c2bdc4c08974d285dc6c`
- Run 2 SHA: `83d9942185d16d63072483709a89e05a133f71b72021c2bdc4c08974d285dc6c`

## Operator's own counters (from stdout)

- MAL orgs loaded: 104
- Postgres: org_cfg=248, eng=248, catalog=233, imports=751
- BigQuery: mixpanel_sharing_orgs=109, helpscout_fire_domains=0
- Scored: 104, skipped: 0
- Ghost accounts: 0
- Behavioral floor applied: 9
- Support fire flags: 0
- Bundle/config mismatches: 3
