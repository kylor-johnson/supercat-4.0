# Q-40 — Regional Sales Distribution
- **Query**: Q-40 | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres | **Run date**: 2026-06-12

## By state (eCat orders, LTM) — top 20

| state | customer_count | ecat_order_count | ecat_gmv |
|---|---|---|---|
| LA | 13 | 13 | $56,433.60 |
| PA | 5 | 10 | $56,133.40 |
| AL | 12 | 27 | $45,496.05 |
| FL | 11 | 24 | $39,924.58 |
| SC | 4 | 5 | $39,550.00 |
| TX | 6 | 7 | $36,909.80 |
| GA | 9 | 9 | $36,398.40 |
| ON | 12 | 14 | $32,058.50 |
| NC | 5 | 5 | $28,786.80 |
| TN | 2 | 2 | $24,676.00 |
| NJ | 3 | 6 | $24,376.50 |
| KY | 1 | 2 | $20,689.80 |
| NY | 2 | 4 | $15,857.65 |
| IL | 3 | 4 | $14,213.50 |
| AB | 3 | 4 | $12,664.00 |
| MS | 2 | 2 | $12,396.00 |
| OH | 2 | 2 | $10,812.80 |
| AR | 4 | 4 | $10,101.10 |
| KS | 1 | 1 | $8,812.00 |
| CO | 3 | 6 | $7,019.08 |

**Note**: eCat order activity concentrated in the Southeast (LA, AL, FL, GA, SC) + PA/TX, with notable Canadian activity (ON, AB). Regional × Category cross-tab not separately materialized (sales_data is national; covered by Q-39). eCat-channel only.
