# Q-13 — Customer Concentration Risk (eCat GMV, LTM)
- **Query**: Q-13 | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres `orders` | **Run date**: 2026-06-12
- **Row count**: top 15 | **Scope**: eCat-channel GMV only (not total business)

| customer_num | bill_to_company_name | orders | gmv | pct_of_ecat_gmv |
|---|---|---|---|---|
| 12677 | Cregger Company, LLC | 2 | $22,820.00 | 4.1 |
| 2599 | Wiseway Supply | 2 | $20,689.80 | 3.8 |
| 2562 | Wage Lighting & Design | 3 | $20,334.00 | 3.7 |
| 368 | Graham's Lighting | 1 | $19,460.00 | 3.5 |
| 544 | Lightstyle of Orlando | 7 | $19,163.30 | 3.5 |
| 5311 | Home Lighting of Frazer | 1 | $16,602.00 | 3.0 |
| 682 | Richards Lighting | 4 | $14,827.80 | 2.7 |
| 537 | Lighting, Inc | 1 | $14,278.00 | 2.6 |
| 992 | Lighting World Decorator | 3 | $12,495.70 | 2.3 |
| 30784 | Hughes Supply Hajoca | 1 | $12,179.00 | 2.2 |
| 30980 | Surf Electrical Services | 3 | $11,959.90 | 2.2 |
| 13073 | Anthology Lighting | 2 | $10,988.00 | 2.0 |
| 11546 | Schaedler Yesco Distribution | 2 | $10,656.00 | 1.9 |
| 25620 | Greer Lighting Center | 1 | $9,944.00 | 1.8 |
| 11452 | Christies Lighting Gallery,LLC | 1 | $9,467.00 | 1.7 |

**Note**: Top 15 eCat buyers ≈ 43.0% of LTM eCat GMV — low concentration (no single buyer >5%). eCat-channel only; not total-business concentration.
