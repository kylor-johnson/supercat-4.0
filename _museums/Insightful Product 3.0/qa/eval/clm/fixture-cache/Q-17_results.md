# Q-17 — Dormant eCat Customer Identification
- **Query**: Q-17 | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres | **Run date**: 2026-06-12
- **Scope**: eCat-channel only

## Recently lapsed (ordered 4–12 months ago, NOT in last 3 months) — top 25

| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
|---|---|---|---|---|---|
| 12677 | Cregger Company, LLC | SC | 2026-01-11 | 2 | $22,820.00 |
| 2599 | Wiseway Supply | KY | 2026-02-05 | 2 | $20,689.80 |
| 2562 | Wage Lighting & Design | PA | 2026-01-11 | 3 | $20,334.00 |
| 368 | Graham's Lighting | TN | 2026-01-12 | 1 | $19,460.00 |
| 544 | Lightstyle of Orlando | FL | 2026-01-21 | 7 | $19,163.30 |
| 5311 | Home Lighting of Frazer | PA | 2026-02-05 | 1 | $16,602.00 |
| 682 | Richards Lighting | AL | 2026-02-16 | 4 | $14,827.80 |
| 537 | Lighting, Inc | TX | 2025-07-24 | 1 | $14,278.00 |
| 992 | Lighting World Decorator | NY | 2026-01-27 | 3 | $12,495.70 |
| 30784 | Hughes Supply Hajoca Corporation | LA | 2026-01-11 | 1 | $12,179.00 |
| 30980 | Surf Electrical Services | NJ | 2026-01-26 | 3 | $11,959.90 |
| 13073 | Anthology Lighting | TX | 2026-01-20 | 2 | $10,988.00 |
| 11546 | Schaedler Yesco Distribution | PA | 2026-01-12 | 2 | $10,656.00 |
| 25620 | Greer Lighting Center | SC | 2026-01-12 | 1 | $9,944.00 |
| 11452 | Christies Lighting Gallery,LLC | NC | 2026-01-11 | 1 | $9,467.00 |
| 876 | Wilson Fans And Lighting | KS | 2026-01-10 | 1 | $8,812.00 |
| 10458 | Winsupply Owensboro KY Co | OH | 2026-01-12 | 1 | $8,780.00 |
| 30324 | Staggs Carpets & Interiors Inc. | MS | 2026-01-22 | 1 | $8,464.00 |
| 24874 | Notoco-Baton Rouge | LA | 2026-02-27 | 1 | $8,232.00 |
| 30470 | Made New Interiors and Decor, LLC | NC | 2026-01-13 | 1 | $8,195.60 |
| 30311 | Mathes of Alabama Electric Supply Co., Inc. | AL | 2026-01-23 | 4 | $7,866.80 |
| 428 | Jacobson Electric Service | IL | 2026-01-12 | 2 | $7,338.00 |
| 31313 | Wilhouse Designs | AL | 2025-10-26 | 1 | $6,355.50 |
| 5113 | Billows Electric Supply Co. | NJ | 2026-02-27 | 2 | $6,214.60 |
| 30618 | Illuminating Design LLC DBA A&J Investments | NJ | 2026-01-19 | 1 | $6,202.00 |

## At-risk high-value (LTM eCat buyers, last order > 90 days ago) — top 20

| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
|---|---|---|---|---|---|
| 12677 | Cregger Company, LLC | SC | $22,820.00 | 2026-01-11 | 152 |
| 2599 | Wiseway Supply | KY | $20,689.80 | 2026-02-05 | 127 |
| 2562 | Wage Lighting & Design | PA | $20,334.00 | 2026-01-11 | 152 |
| 368 | Graham's Lighting | TN | $19,460.00 | 2026-01-12 | 151 |
| 544 | Lightstyle of Orlando | FL | $19,163.30 | 2026-01-21 | 142 |
| 5311 | Home Lighting of Frazer | PA | $16,602.00 | 2026-02-05 | 126 |
| 682 | Richards Lighting | AL | $14,827.80 | 2026-02-16 | 116 |
| 537 | Lighting, Inc | TX | $14,278.00 | 2025-07-24 | 323 |
| 992 | Lighting World Decorator | NY | $12,495.70 | 2026-01-27 | 136 |
| 30784 | Hughes Supply Hajoca Corporation | LA | $12,179.00 | 2026-01-11 | 152 |
| 30980 | Surf Electrical Services | NJ | $11,959.90 | 2026-01-26 | 137 |
| 13073 | Anthology Lighting | TX | $10,988.00 | 2026-01-20 | 143 |
| 11546 | Schaedler Yesco Distribution | PA | $10,656.00 | 2026-01-12 | 151 |
| 25620 | Greer Lighting Center | SC | $9,944.00 | 2026-01-12 | 150 |
| 11452 | Christies Lighting Gallery,LLC | NC | $9,467.00 | 2026-01-11 | 152 |
| 876 | Wilson Fans And Lighting | KS | $8,812.00 | 2026-01-10 | 153 |
| 10458 | Winsupply Owensboro KY Co | OH | $8,780.00 | 2026-01-12 | 151 |
| 30324 | Staggs Carpets & Interiors Inc. | MS | $8,464.00 | 2026-01-22 | 141 |
| 24874 | Notoco-Baton Rouge | LA | $8,232.00 | 2026-02-27 | 105 |
| 30470 | Made New Interiors and Decor, LLC | NC | $8,195.60 | 2026-01-13 | 150 |

**Note**: Most high-value buyers last ordered in Jan–Feb 2026 (the seasonal peak) and are now 100–155 days dormant — consistent with the seasonal order trough, not churn. eCat-channel only; these accounts may still order via other channels.
