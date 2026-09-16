# Q-CI-03: Feature Adoption Benchmarking — Buster & Punch (bp, org_id=250)
- **Query**: Q-CI-03 (VM-24)
- **Source**: BigQuery insightful_product.org_summary + segment_benchmarks_monthly
- **Run date**: 2026-04-21

## Org Feature Profile

| field | value |
|-------|-------|
| segment | Commerce-Active |
| feature_depth | 3 |
| has_clicky_portal | false |
| arr | — |
| arr_band | — |

## Segment Benchmarks (Commerce-Active — April 2026)

| metric | p25 | median | p75 | bp_value | bp_position |
|--------|-----|--------|-----|----------|-------------|
| submit_order | 103 | 245 | 290 | 66 | Below p25 |
| total_logins | 1,476 | 2,578 | 5,605 | 2,411 | p25–median |
| search_products | 3,455 | 5,017 | 28,432 | 2,244 | Below p25 |
| mrr | $652.50 | $920 | $1,637.50 | — | N/A |
| arr | $7,902.50 | $10,240 | $22,228.50 | — | N/A |

## Feature Adoption Rates (segment-wide)

| feature | segment_adoption_rate |
|---------|----------------------|
| Library | 100% |
| PDF Catalog | 94.2% |
| Sales Portal | 50.0% |
| Portal Orders (ERP sync) | 50.0% |
| CPQ | 11.5% |
| Kit Items | 7.7% |

## Segment Benchmarks (Commerce-Active — March 2026)

| metric | p25 | median | p75 | org_count |
|--------|-----|--------|-----|-----------|
| submit_order | 82 | 128 | 641 | 15 |
| total_logins | 1,352 | 2,533 | 5,108 | 15 |
| search_products | 2,158 | 5,912 | 30,646 | 15 |

**Notes**:
- 2 monthly snapshots available (March + April 2026)
- April snapshot has 52 orgs (up from 15 in March — first full-segment snapshot)
- bp's submit_order (66) is below p25 (103) in April — bottom quartile for ordering activity
- bp's logins (2,411) are between p25 and median — reasonable engagement
- bp's search_products (2,244) is below p25 (3,455) — lower product discovery than peers
