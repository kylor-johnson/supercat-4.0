# Section 07 Highlights — Peer Benchmarking
- **Client**: Currey & Company (cci, org_id=161)
- **Run date**: 2026-06-15
- **Period**: Trailing 12 months (2025-06-15 to 2026-06-15)
- **Benchmark data vintage**: 2026-04-14 (most recent peer benchmark run)

## Peer Group

| Field | Value |
|-------|-------|
| Effective group | Lighting / iPad+Catalog+Portal |
| Group level | Tier 1 (vertical + bundle match) |
| Steady-state peers | 5 |
| Benchmark confidence | Medium |
| External framing | Lighting manufacturers on the same platform bundle |

## Key Metrics

| Metric | Org Value | Peer Median | Delta | Quartile | Percentile |
|--------|-----------|-------------|-------|----------|------------|
| Engagement (HERO) | 80 | 40 | +40 | Q4 | Top 5% |
| Value Delivery | 80 | 90 | -10 | Q2 | Bottom 40% |
| Adoption | 89 | 100 | -11 | Q1 | Bottom 20% |
| Data & Operational Health | 64 | 70 | -6 | Q1 | Bottom 20% |
| Trajectory | 60 | 100 | -40 | Q1 | Bottom 5% |
| Catalog Completeness | 88.9% | 95% | -6.1pp | Q1 | Bottom 20% |

## Non-Whitelisted Metrics (not rendered, for cross-reference)

| Metric | Org Value | Peer Median | Quartile | Notes |
|--------|-----------|-------------|----------|-------|
| Login Intensity | 162.6 | 105.0 | Q4 | Confirms engagement strength |
| Primary Value Metric | 883.0 | 492.75 | Q4 | Bundle-specific value measure |
| Health Score | 77.0 | 82.0 | Q2 | Internal only — suppressed |
| Orders 90d | 985.0 | — | — | metric_applicable=False (no cart bundle) |
| Orders per User | 11.1 | — | — | metric_applicable=False (no cart bundle) |

## Feature Adoption vs. Peers

| Feature | CCI Status | Peer Adoption |
|---------|-----------|---------------|
| Digital Library | Active | 100% |
| PDF Catalog | Active | 100% |
| Sales Portal | Active | 67% |
| Portal Order Submission | Active | 67% |
| Kit Items | Configured (not active) | 29% |

## Headline Findings

1. **Engagement dominance**: CCI's rep engagement score (80) is double the peer median (40), ranking at the top of the peer group — the clear standout metric.
2. **Configuration staleness drives below-median scores**: Operational health (64 vs 70), trajectory (60 vs 100), and adoption (89 vs 100) gaps all trace to configuration entities stale since August 2025.
3. **Catalog completeness gap is actionable**: At 88.9% vs peer median 95%, driven by missing images and pricing — June 2026 visible-product completeness has already improved to 95.8%.
4. **Feature adoption strong relative to peers**: 4 of 5 tracked features active, exceeding peer adoption rates on Sales Portal and Portal Orders.
5. **Trajectory is the widest gap**: At 60 vs 100, momentum metrics have flattened despite high absolute engagement — likely reflects plateaued growth rather than decline.

## Positive Signals

- Engagement Q4: Double the peer median, top of peer group
- Login intensity Q4: 162.6 vs median 105 — highest daily usage intensity
- Primary value metric Q4: 883 vs median 492.75
- Feature adoption exceeds peers on Sales Portal (Active vs 67%) and Portal Orders (Active vs 67%)
- Peer group is Tier 1 with vertical + bundle match — comparisons are directly relevant

## Areas to Watch

- Trajectory Q1 (60 vs 100): Momentum has flattened; recent growth rates trail peers
- Operational health Q1 (64 vs 70): Configuration entities stale 299 days
- Catalog completeness Q1 (88.9% vs 95%): Image/pricing gaps on visible products
- Adoption Q1 (89 vs 100): Kit items configured but unused; full feature breadth not realized
- Value delivery Q2 (80 vs 90): Below median but closest to peer parity

## Hero Selection Rationale

1. orders_per_user — skipped (HAS_CART=False, metric_applicable=False)
2. **engagement_score — SELECTED** (Q4, strong outlier: org 80 vs median 40, pctile=1.0)
3. adoption_score — skipped (Q1, not a positive story)
4. catalog_completeness — skipped (Q1)
5. trajectory_score — skipped (Q1)

## Narrative Posture

CCI is a high-engagement account that leads its peer group on daily platform activity but trails on infrastructure and maintenance metrics. The below-median scores are driven by a known configuration maintenance gap (Aug 2025 stale entities) and catalog completeness, not by low utilization. Refreshing configuration data would likely move operational health, adoption, and trajectory scores upward in the next benchmark cycle. The engagement strength provides a strong foundation — reps are already using the platform daily; the platform infrastructure just needs to keep pace.
