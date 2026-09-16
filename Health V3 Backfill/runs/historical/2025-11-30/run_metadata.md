# Run Metadata — 2025-11-30 (Historical Backfill)

| Field | Value |
|-------|-------|
| Score date | 2025-11-30 |
| Operator version | V3.2.12 |
| Run type | Historical backfill (cache mode) |
| Canonical SHA | `3267e4578c8c85c0047e7ded2a73b825d6834ea948e23644023c8dd985a89e4a` (SHA-1 = SHA-2) |
| Row count (canonical) | 103 |
| Row count (formatted) | 103 |
| Run timestamp | 2026-05-13T23:11:01Z |
| Orgs in MAL | 104 |
| Orgs scored | 103 |
| Orgs skipped | 1 (`gblx` — onboarding_window) |

## Score distribution

The V3.2.12 operator emits four bands: `Thriving / Healthy / Watch / At Risk`. There is no `Critical` band in this operator version (no orgs would qualify for one in this dataset either).

| Band | Count |
|------|-------|
| Thriving | 52 |
| Healthy | 36 |
| Watch | 12 |
| At Risk | 3 |

## Operator-reported flags

| Flag | Count |
|------|------:|
| Scoring status `complete` | 103 |
| Ghost accounts | 1 |
| Behavioral floor applied | 10 |
| Support fire flags | 0 |
| Bundle/config mismatches | 3 |

## Known limitations

- **Adoption** — feature flags reflect current config, not historical (`pg_org_config.csv` was not date-filtered).
- **Catalog completeness** — reflects today's catalog state (`pg_catalog.csv` has no `as_of` filter on `products`), not Nov 2025.
- **Smart Stacks** — `pg_smart_stacks.csv` has no date filter; counts reflect current state, not Nov 2025.
- **Support Fire** — only conversations created on or before 2025-11-30 that are *still* `active`/`pending` today are captured. Fires that have been resolved since 2025-11-30 do not appear, so this dimension structurally underreports for historical runs. (Helpscout query returned 0 rows, as expected per methodology note.)
- **MAL** — uses 2026-04-14 master account list; orgs added after 4/14/2026 or removed before that date will be misclassified relative to their actual 2025-11-30 status.

## Determinism

Run 1 SHA = Run 2 SHA: **YES** (`3267e4578c8c85c0047e7ded2a73b825d6834ea948e23644023c8dd985a89e4a`)

Both runs scored the same 103 orgs, skipped the same 1 org (`gblx`), and produced byte-identical canonical CSVs.
