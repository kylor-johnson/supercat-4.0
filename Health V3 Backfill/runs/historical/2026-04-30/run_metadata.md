# Run Metadata — 2026-04-30 (Historical Backfill)

| Field | Value |
|-------|-------|
| Score date | 2026-04-30 |
| Operator version | V3.2.12 |
| Run type | Historical backfill (cache mode) |
| Canonical SHA | 6e2a00722dd2494534fc77736177f4af2436e4ab334c82dd92a58afe1803707c |
| Row count (canonical) | 104 |
| Row count (formatted) | 104 |
| Run timestamp | 2026-05-13T22:39:15Z |

## Score distribution

| Band | Count |
|------|-------|
| Thriving | 59 |
| Healthy | 28 |
| Watch | 15 |
| At Risk | 1 |
| Critical | 1 |

## Known limitations (apply to all historical runs)

- **Adoption** — feature flags reflect current config, not historical. Orgs that changed features since Apr 2026 may have understated/overstated adoption scores.
- **Catalog completeness** — reflects today's catalog state. Not historical. Treat ops scores as approximate for catalog-heavy orgs.
- **Support Fire** — only open conversations visible. Conversations opened before 2026-04-30 and since closed do not appear; conversations opened after 2026-04-30 are excluded by the createdAt <= cutoff filter.
- **MAL** — uses the 2026-04-14 MAL. Orgs added or removed after that date are affected accordingly.

## Determinism

Run 1 SHA = Run 2 SHA: YES
