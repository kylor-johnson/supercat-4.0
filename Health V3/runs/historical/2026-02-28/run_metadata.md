# Run Metadata — 2026-02-28 (Historical Backfill)

| Field | Value |
|-------|-------|
| Score date | 2026-02-28 |
| Operator version | V3.2.13 (scoring code unchanged from V3.2.12; V3.2.13 was doc-only) |
| Run type | Historical backfill (cache mode) |
| Canonical SHA | bc8a46be8473791576d5f5371487da418a92e3c3e8c93db93e4c4def3d6cfb38 |
| Row count (canonical) | 103 |
| Row count (formatted) | 103 |
| Run timestamp | 2026-05-13T23:15:07Z |

## Score distribution

Operator emits four bands (`Thriving`, `Healthy`, `Watch`, `At Risk`); there is no `Critical` band in V3. Table reflects the canonical `health_band` column.

| Band | Count |
|------|-------|
| Thriving | 56 |
| Healthy | 34 |
| Watch | 11 |
| At Risk | 2 |

Additional canonical-CSV facts (from operator stdout):
- Rows skipped (new-org exclusion or not in Postgres): 1
- Ghost accounts: 0
- Behavioral floor applied: 8
- Support fire flags: 0
- Bundle/config mismatches: 3
- Scoring status: all 103 `complete`

## Known limitations

- Adoption — feature flags reflect current config, not historical.
- Catalog completeness — reflects today's catalog state, not Feb 2026.
- Support Fire — only conversations created ≤ 2026-02-28 still open today are captured (zero captured in this run).
- MAL — uses 2026-04-14 MAL.

## Determinism

Run 1 SHA = Run 2 SHA: YES
- Run 1 SHA: `bc8a46be8473791576d5f5371487da418a92e3c3e8c93db93e4c4def3d6cfb38`
- Run 2 SHA: `bc8a46be8473791576d5f5371487da418a92e3c3e8c93db93e4c4def3d6cfb38`

## Inputs

- MAL: `../Health V2/inputs/master_account_list_2026-04-14_canonical.csv` (104 orgs)
- Cache dir: `cache/historical/2026-02-28/` (10 files, populated 2026-05-13)
  - org_cfg=248, eng=248, catalog=233, imports=719, mixpanel_sharing_orgs=108, helpscout_fire_domains=0

## Command

```
.venv/bin/python3 health_operator_v3.py \
  --mal "../Health V2/inputs/master_account_list_2026-04-14_canonical.csv" \
  --score-date 2026-02-28 \
  --cache \
  --cache-dir "cache/historical/2026-02-28" \
  --output-dir "runs/historical/2026-02-28"
```
