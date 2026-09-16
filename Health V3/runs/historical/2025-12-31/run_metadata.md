# Run Metadata — 2025-12-31 (Historical Backfill)

| Field | Value |
|-------|-------|
| Score date | 2025-12-31 |
| Operator version | V3.2.12 |
| Run type | Historical backfill (cache mode) |
| Canonical SHA | `8e4c69b5377322829d8ef89eb6e1d7a6297f17f0b8758afa435c02f783bd7e94` |
| Formatted SHA | `ba037d01f560863d2aa0d541462c7d327a25a8e67d92fc9c367d8b666e991c11` |
| Row count (canonical) | 102 |
| Row count (formatted) | 102 |
| Rows skipped (new-org / not in Postgres) | 2 |
| Run timestamp (UTC) | 2026-05-13T23:10:19Z |
| MAL input | `../Health V2/inputs/master_account_list_2026-04-14_canonical.csv` |
| Cache directory | `cache/historical/2025-12-31` |

## Score distribution

> Note: the operator emits five bands (`Thriving`, `Healthy`, `Watch`, `At Risk`, `Critical`). The orchestrator template listed only four — the table below uses the operator's actual band labels so the totals reconcile to 102.

| Band | Count |
|------|------:|
| Thriving | 53 |
| Healthy | 33 |
| Watch | 14 |
| At Risk | 2 |
| Critical | 0 |
| **Total** | **102** |

## Operational flags

| Flag | Count |
|------|------:|
| Ghost accounts | 0 |
| Behavioral floor applied | 8 |
| Support fire flags | 0 |
| Bundle / config mismatches | 3 |
| Scoring status = `complete` | 102 |

## Known limitations

- **Adoption** — feature flags reflect current org config, not the historical state on 2025-12-31.
- **Catalog completeness** — reflects today's catalog state, not Dec 2025.
- **Support Fire** — only Help Scout conversations created on or before 2025-12-31 that remain open today are captured (yields 0 domains for this score date).
- **MAL** — uses the 2026-04-14 canonical MAL (no historical MAL snapshot is available).

## Determinism

Run 1 SHA = Run 2 SHA: **YES**

- Run 1 canonical SHA: `8e4c69b5377322829d8ef89eb6e1d7a6297f17f0b8758afa435c02f783bd7e94`
- Run 2 canonical SHA: `8e4c69b5377322829d8ef89eb6e1d7a6297f17f0b8758afa435c02f783bd7e94`
- Run 1 formatted SHA: `ba037d01f560863d2aa0d541462c7d327a25a8e67d92fc9c367d8b666e991c11`
- Run 2 formatted SHA: `ba037d01f560863d2aa0d541462c7d327a25a8e67d92fc9c367d8b666e991c11`

## Files in this run

- `client_health_scores_2025-12-31.csv` — canonical output (102 rows × 28 cols)
- `client_health_scores_2025-12-31_formatted.csv` — formatted output (102 rows × 20 cols)
- `skipped_new_orgs.csv` — new-org / not-in-Postgres exclusions (2 rows)
- `run_metadata.md` — this file
