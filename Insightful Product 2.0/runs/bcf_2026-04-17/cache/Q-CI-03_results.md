# Q-CI-03 — Feature Adoption + Segment Benchmarks

- **Query ID**: Q-CI-03
- **Org**: Braxton Culler (`bcf`, org_id: 171)
- **Segment**: Platform-Embedded
- **Source**: `insightful_product.org_summary` + `insightful_product.segment_benchmarks_monthly`
- **Period**: Current + trailing 2 months
- **Row count**: 1 (org) + 2 (benchmarks)
- **Run date**: 2026-04-17
- **Exclusions**: None
- **Note**: `arr_band` column does not exist in org_summary; excluded from query

## Part A — Feature Adoption (bcf)

| org_shortname | org_name | segment | feature_depth | has_clicky_portal | arr |
|---|---|---|---|---|---|
| bcf | Braxton Culler | Platform-Embedded | 7 | false | $26,620 |

## Part B — Segment Benchmarks (Platform-Embedded, Last 2 Months)

| benchmark_month | org_count | submit_order_p10 | submit_order_p25 | submit_order_median | submit_order_p75 | submit_order_p90 | total_logins_p25 | total_logins_median | total_logins_p75 | search_products_p25 | search_products_median | search_products_p75 | mrr_p25 | mrr_median | mrr_p75 | arr_p25 | arr_median | arr_p75 | feature_kit_items_pct | feature_portal_orders_pct | feature_sales_portal_pct | feature_library_pct | feature_pdf_catalog_pct | feature_cpq_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-04 | 47 | 543 | 935 | 2,748 | 5,196 | 7,092 | 4,681 | 6,458 | 8,730 | 18,101 | 33,085 | 44,759 | $0 | $1,685 | $2,030 | $0 | $16,980 | $25,555 | 27.7% | 66.0% | 66.0% | 100.0% | 100.0% | 40.4% |
| 2026-03 | 33 | 565 | 1,205 | 2,986 | 6,109 | 7,760 | 4,640 | 6,368 | 8,568 | 25,709 | 35,609 | 52,644 | $0 | $1,685 | $2,030 | $0 | $16,980 | $25,760 | 24.2% | 66.7% | 66.7% | 100.0% | 100.0% | 36.4% |
