# Health Data — Source Pointer

Do not copy health score CSVs into this folder. Always reference from source paths below.

## Current Run (May 2026)

**Path:** `SuperCat 4.0/Health V3/runs/2026-05-13/client_health_scores_2026-05-13.csv`
**Version:** V3.3.0
**Orgs scored:** 104
**Score date:** 2026-05-13
**Weights:** Engagement 25% / Adoption 20% / Value Delivery 35% / Ops 20%

**Key columns used in routing:**
- `org_shortname` — org identifier
- `bundle` — current product bundle (iPad-only, Full, iPad+Catalog+Portal, etc.)
- `arr` — implied ARR
- `health_band` — Thriving / Healthy / Watch / At Risk / Critical
- `composite_score` — 0–100
- `behavioral_floor_applied` — True/False (flags floor-muted accounts)
- `value_delivery_score` — leading commercial stress signal
- `engagement_score`

## Backfill (Nov 2025 – Apr 2026)

**Path:** `SuperCat 4.0/Health V3 Backfill/runs/historical/[YYYY-MM-DD]/client_health_scores_[YYYY-MM-DD].csv`

**Available snapshots:**
- `2025-11-30`
- `2025-12-31`
- `2026-01-31`
- `2026-02-28`
- `2026-03-31`
- `2026-04-30`

**Used for:** Determining which accounts are consistently Healthy/Thriving (Wave 1 qualification) vs. chronically weak (Wave 3).

## Next Run

Health V3 runs monthly. Next score date: ~June 13, 2026. Re-run routing table against updated scores before beginning Wave 1 outreach at scale.
