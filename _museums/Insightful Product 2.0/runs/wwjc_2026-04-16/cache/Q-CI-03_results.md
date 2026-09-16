# Q-CI-03: Feature Adoption Benchmarking
- **Query ID**: Q-CI-03 (VM-24)
- **Org**: Wildwood/Chelsea House (wwjc, org_id=8)
- **Period**: Current snapshot + trailing 2 benchmark months
- **Row count**: 1 (org summary) + 2 (segment benchmarks monthly)
- **Run date**: 2026-04-16
- **Source**: BigQuery insightful_product.org_summary + segment_benchmarks_monthly

## Org Feature Profile

| Field | Value |
|-------|-------|
| org_shortname | wwjc |
| org_name | Wildwood/Chelsea House |
| segment | Platform-Embedded |
| feature_depth | 5 |
| has_clicky_portal | false |
| arr | $40,220 |

## Segment Benchmarks Monthly (Platform-Embedded)

### 2026-04 (Latest)

| Metric | P10 | P25 | Median | P75 | P90 |
|--------|-----|-----|--------|-----|-----|
| Submit Order | 543 | 935 | 2,748 | 5,196 | 7,092 |
| Total Logins | — | 4,681 | 6,458 | 8,730 | — |
| Search Products | — | 18,101 | 33,085 | 44,759 | — |
| MRR | — | $0 | $1,685 | $2,030 | — |
| ARR | — | $0 | $16,980 | $25,555 | — |

| Feature Adoption | Pct of Segment |
|-----------------|---------------|
| Kit Items | 27.7% |
| Portal Orders | 66.0% |
| Sales Portal | 66.0% |
| Library | 100.0% |
| PDF Catalog | 100.0% |
| CPQ | 40.4% |

Org count in segment: 47

### 2026-03

| Metric | P10 | P25 | Median | P75 | P90 |
|--------|-----|-----|--------|-----|-----|
| Submit Order | 565 | 1,205 | 2,986 | 6,109 | 7,760 |
| Total Logins | — | 4,640 | 6,368 | 8,568 | — |
| Search Products | — | 25,709 | 35,609 | 52,644 | — |
| MRR | — | $0 | $1,685 | $2,030 | — |
| ARR | — | $0 | $16,980 | $25,760 | — |

| Feature Adoption | Pct of Segment |
|-----------------|---------------|
| Kit Items | 24.2% |
| Portal Orders | 66.7% |
| Sales Portal | 66.7% |
| Library | 100.0% |
| PDF Catalog | 100.0% |
| CPQ | 36.4% |

Org count in segment: 33

### wwjc Position vs. Segment

| Metric | wwjc Value | Segment Median (Apr 2026) | Position |
|--------|-----------|--------------------------|----------|
| Submit Order (Mixpanel) | 1,758 | 2,748 | Below median |
| Total Logins (Mixpanel) | 9,557 | 6,458 | Above P75 |
| Search Products (Mixpanel) | 32,798 | 33,085 | Near median |
| ARR | $40,220 | $16,980 | Above P75 |
| Feature Depth | 5 | — | — |
