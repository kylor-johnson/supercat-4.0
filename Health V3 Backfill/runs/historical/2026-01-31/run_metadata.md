# Run Metadata — 2026-01-31 (Historical Backfill)

| Field | Value |
|-------|-------|
| Score date | 2026-01-31 |
| Operator version | V3.2.12 |
| Run type | Historical backfill (cache mode) |
| Canonical SHA | `b5cf97d6f6051e16eb7ab0edba6bfb7b3430445c8b8ede3f5b275579211c7b22` (SHA-1 = SHA-2) |
| Row count (canonical) | 103 |
| Row count (formatted) | 103 |
| Run timestamp | 2026-05-13 23:11:45 UTC |

## Score distribution

Operator emits five bands (`Thriving`, `Healthy`, `Watch`, `At Risk`, `Critical`). Counts from the canonical CSV:

| Band | Count |
|------|-------|
| Thriving | 57 |
| Healthy | 35 |
| Watch | 8 |
| At Risk | 3 |
| Critical | 0 |

Additional operator stats: `complete` scoring status = 103; ghost accounts = 0; behavioral floor applied = 6; support fire flags = 0; bundle/config mismatches = 3; rows skipped (new-org exclusion or not in Postgres) = 1.

## Known limitations

- **Adoption** — feature flags reflect current config, not historical (cache file `pg_org_config.csv` has no date filter).
- **Catalog completeness** — reflects today's catalog state, not Jan 2026 (cache file `pg_catalog.csv` has no date filter).
- **Support Fire** — only conversations created ≤ 2026-01-31 still open today are captured; for this run `bq_helpscout_fires.csv` returned 0 rows, so support fire flags = 0.
- **MAL** — uses 2026-04-14 MAL, not a Jan 2026 MAL snapshot.

## Determinism

Run 1 SHA = Run 2 SHA: **YES** (`b5cf97d6f6051e16eb7ab0edba6bfb7b3430445c8b8ede3f5b275579211c7b22`)

## Command

```
.venv/bin/python3 health_operator_v3.py \
  --mal "../Health V2/inputs/master_account_list_2026-04-14_canonical.csv" \
  --score-date 2026-01-31 \
  --cache \
  --cache-dir "cache/historical/2026-01-31" \
  --output-dir "runs/historical/2026-01-31"
```
