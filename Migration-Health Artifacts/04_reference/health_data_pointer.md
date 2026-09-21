# Health Data — Source Pointer

Do not copy health score CSVs into this folder. Always reference from the source
paths below.

## Current Run (May 2026)

**Path:** `SuperCat 4.0/Health V3/runs/2026-05-13/client_health_scores_2026-05-13.csv`
**Version:** V3.4.0
**SHA-256:** `6a2f1d9fc6c86ae58a6888386f83b0a9122ecc98cb5ae6f2195e89a8d4dd1bff`
**Orgs scored:** 104
**Score date:** 2026-05-13
**Weights:** Engagement 25% / Adoption 25% / Value Delivery 25% / Ops 25% (equal)

> **Weighting changed on 2026-09-16.** V3.3.0 had briefly weighted the composite
> 25/20/35/20; V3.4.0 reverted to equal after the §9 look-back rejected it. **The
> routing table in this folder already matches V3.4.0 (99 of 102 comparable
> scores)** — it was built from unweighted scores all along, so V3.4.0 corrected
> a mislabel rather than invalidating any routing. No re-routing is implied.
> See `Health V3/CHANGELOG.md` 3.4.0.

**Key columns used in routing:**
- `org_shortname` — org identifier
- `bundle` — current product bundle (iPad-only, Full, iPad+Catalog+Portal, etc.)
- `arr` — implied ARR
- `health_band` — Thriving / Healthy / Watch / At Risk / Critical
- `composite_score` — 0–100
- `behavioral_floor_applied` — True/False (flags floor-muted accounts)
- `engagement_score` — **the leading indicator.** Best forward separation of the
  four dimensions (AUC 0.620 on 6 functional deaths at 4–10 months' lead).
- `value_delivery_score` — read as **context, not stress.** It ranked 3rd of 4
  as a leading indicator (AUC 0.573) and is substantially a segment proxy:
  Catalog-Focused accounts are 54% of the base and are *defined* by ordering
  outside SuperCat, so low VD is often their normal shape rather than distress.
  `abol` (healthy, 169 logins/90d) and `hmjc` (churned) both score zero VD —
  only Engagement separates them. Do not route on VD alone.

## Backfill (Nov 2025 – Apr 2026)

**Path:** `SuperCat 4.0/Health V3/runs/historical/[YYYY-MM-DD]/client_health_scores_[YYYY-MM-DD].csv`

(The former `Health V3 Backfill/` clone was merged into `Health V3/` on
2026-09-16 and no longer exists.)

**Available snapshots:** `2025-11-30`, `2025-12-31`, `2026-01-31`, `2026-02-28`,
`2026-03-31`, `2026-04-30` — all regenerated under V3.4.0 equal weights, so the
series is consistent with the current run above.

**Used for:** determining which accounts are consistently Healthy/Thriving
(Wave 1 qualification) vs. chronically weak (Wave 3).

**Caveat:** historical adoption flags and catalog completeness reflect
present-day config, not the score date. Fit for trend, not for a client-facing
number — see `Health V3/HISTORICAL_RUN_GUIDE.md`.

## Month-over-month triggers

`SuperCat 4.0/Health V3/trigger_reports/trigger_report_{date}.csv` — band
transitions, score drops, chronic distress, oscillation and long-running support
fires across the whole series, each with a CS action and the dimension that drove
it. Usually the faster read than diffing two canonicals by hand.

## Next Run

Health V3 runs **monthly**. Re-run the routing table against the new canonical
before any further wave outreach at scale; check `Health V3/CHANGELOG.md` for the
latest score date and SHA rather than assuming the May run is current.
