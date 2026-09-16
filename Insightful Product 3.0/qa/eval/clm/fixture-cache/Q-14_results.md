# Q-14 — Customer Reorder Frequency & Velocity (eCat, LTM)
- **Query**: Q-14 | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres `orders` | **Run date**: 2026-06-12
- **Row count**: 11 (HAVING ≥3 eCat orders LTM) | **Scope**: eCat-channel only

| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
|---|---|---|---|---|---|---|
| 544 | Lightstyle of Orlando | 7 | $19,163.30 | 2025-06-24 | 2026-01-21 | 35.1 |
| 30825 | Austell Lighting | 6 | $4,200.00 | 2025-07-07 | 2026-02-19 | 45.4 |
| 8091 | Beautiful Lights | 6 | $8,679.68 | 2025-11-17 | 2026-05-21 | 37.0 |
| 682 | Richards Lighting | 4 | $14,827.80 | 2026-02-16 | 2026-02-16 | 0.0 |
| 30311 | Mathes of Alabama Electric Supply Co., Inc. | 4 | $7,866.80 | 2026-01-23 | 2026-01-23 | 0.0 |
| 24743 | Enterprise Wholesale & Floorin | 3 | $2,545.45 | 2025-12-12 | 2026-03-30 | 54.1 |
| 992 | Lighting World Decorator | 3 | $12,495.70 | 2025-11-17 | 2026-01-27 | 35.5 |
| 2562 | Wage Lighting & Design | 3 | $20,334.00 | 2026-01-11 | 2026-01-11 | 0.0 |
| 30223 | Poonams by Design, LLC | 3 | $1,623.78 | 2025-07-11 | 2025-10-03 | 42.0 |
| 30980 | Surf Electrical Services | 3 | $11,959.90 | 2026-01-12 | 2026-01-26 | 7.0 |
| 7428 | Royal Lighting | 3 | $5,094.30 | 2025-06-27 | 2026-02-10 | 113.9 |

**Note**: eCat reorder cadence ~35–45 days for steady repeat buyers. Several `0.0` rows = multiple orders on the same day (batch entry). eCat-channel only.
