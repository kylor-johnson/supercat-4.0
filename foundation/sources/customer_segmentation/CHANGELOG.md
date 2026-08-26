---
id: CHANGELOG
title: Change history — two-layer taxonomy subtree
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
source_lineage: []
depends_on: []
---

# Changelog

## 2026-08-25 — Phase 0 + Phase 1 (draft)

### Added
- `taxonomy/account-segments.md` (**TAX-A**) — Layer A, SEG-01..04 plus SEG-00 abstention.
  Definitions, field-level lineage, measured per-segment distributions, an authored precedence
  rule with its justification, and the rule's real reproduction rate. Marked
  `availability: post-sale-only` in the schema.
- `taxonomy/prospect-archetypes.md` (**TAX-B**) — Layer B, ARCH-01..04 built only from pre-sale
  observable features. Full feature register including what was pruned and why.
- `taxonomy/segment-archetype-mapping.md` (**TAX-MAP**) — measured A↔B matrix and per-archetype
  back-test against the answer key.
- `ASSUMPTIONS.md` — 5 assumptions, 4 data-quality items, 14 findings carried forward.
- `FOUNDATION-CORRECTIONS.md` — proposed corrections to `CEO_SYSTEM_CONTEXT.md` and
  `02_who_we_serve.md`. **Held, not applied**, pending Layer A/B hardening.
- Empty directories for later phases: `personas/`, `analytics/`, `product/`, `prospects/`,
  `field-kit/`.

### Changed
- `README.md` — capped link repair only. The two files it named as living here now point at
  `Customer Segmentation/current/` (the path `build_v4.py` writes); no file was copied in. Dead
  `agent_research/` links marked as not-imported. New taxonomy subtree indexed. `Last updated`
  bumped to 2026-08-25.

### Not changed (deliberate)
- `foundation/CEO_SYSTEM_CONTEXT.md`, `foundation/02_who_we_serve.md` — corrections held.
- Stamped v4.0 narrative, `build_v4.py`, MASTER CSV — read-only.
- Insightful Product 4.0 profiles and `industry_context.md` — the "Brand-Building" alias was not swept.
- Lens 1 (Digital Selling Maturity) and T1/T2/T3 pricing — untouched.
- Postgres — read-only throughout, including the three malformed `company_website` values.
- `Customer Segmentation 2/` — added to ignore list, not deleted.

### Headline results
| Result | Value |
|---|---|
| Layer A authored rule reproduces stamped label | **38.5%** (majority baseline 34.9%; fitted ceiling 50.0%) |
| Layer B overall, a-priori mapping | **33.3%** (majority baseline 34.5% — fails) |
| ARCH-01 Trade-Gated Access → SEG-01 | **65.0%**, n=20 — the only archetype that beats baseline |
| ARCH-01 exclusion of SEG-03 | **0 of 20** — strong disqualifier |
| Layer B collection coverage | 87 of 109 automated; 94 of 109 with manual observation |

### Open
- Phase 4 lane criteria are next, ahead of Phase 2 (HPMKT ~6 weeks out).
- Volume Distribution's 89% predictability did not reproduce (F-04) — unresolved.
- HPMKT footprint and LinkedIn headcount remain uncollected (F-07).
