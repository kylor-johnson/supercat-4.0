# §7 Peer Benchmarking — Highlights
- **Client**: Kuzco Lighting Inc. (kll, org_id=166)
- **Peer group**: Lighting / Full (tier1, n=8, high confidence)
- **Client-facing cohort label**: "Lighting manufacturers on the same platform bundle"
- **Caveat**: None (high confidence)

## Hero Stat
- **Metric**: adoption_score → "Adoption"
- **Org value**: 100 | **Peer median**: 90 | **Delta**: +10 | **Quartile**: Q4
- **Percentile display**: Top 5% (raw: 1.000 → Top 0% → rounded to Top 5%)
- **Rationale**: Strongest positive outlier — Q4, top of peer group, compelling positive story about full platform capability usage. orders_per_user was considered first (HAS_CART=true) but was on-par with peers (Q3, delta=0) — not a strong story.

## Metric Row Summary (7 rows, excluding hero + health_score)

| Metric | Org | Median | Delta | Quartile | Marker % | Direction |
|--------|-----|--------|-------|----------|----------|-----------|
| Value Delivery | 60 | 65 | -5 | Q3 | 43% | above |
| Engagement | 30 | 30 | 0 | Q3 | 0% | above |
| Data & Operational Health | 50 | 75 | -25 | Q1 | 0% | below |
| Trajectory | 100 | 90 | +10 | Q4 | 100% | above |
| Orders (90-Day) | 128 | 298 | -170 | Q2 | 5% | on-par |
| Orders per User | 0.14 | 0.14 | 0 | Q3 | 63% | above |
| Catalog Completeness | 0% | 99% | -99pp | Q1 | 0% | below |

## Key Narratives
- **Strengths**: Adoption (Q4, Top 5%), Trajectory (Q4, Top 5%), ordering efficiency on par with peers
- **Gaps**: Data & Operational Health (Q1, 25 points below median — widest gap), Catalog Completeness (Q1, pricing field unpopulated — image coverage at 97%)
- **Middle**: Value Delivery and Engagement at or near median, total order volume below median but per-user efficiency in line

## Feature Adoption (Q-CI-03)
- Active: Product Library (100%), PDF Catalog (94%), Sales Portal (50%)
- Not Active: Order History Import (50% of peers), Kit & Bundle Configuration (8% of peers)

## Top Performer Patterns (Q-CI-05, anonymized)
1. Concentrated order sessions — more orders than login sessions
2. Full feature activation drives 3-5x login activity
3. Leading accounts submit 3,000-8,000 orders per quarter
4. Broadest feature sets drive highest combined login + order volumes

## Suppressed
- health_score (internal only — not surfaced)
- login_intensity (not in metric whitelist)
- primary_value_metric (not in metric whitelist)
- Segment label "Commerce-Active" (internal only)
- benchmark_confidence / peer_group_level / peer_group_n labels (internal only)
