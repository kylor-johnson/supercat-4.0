# Q-01 Step 2 — Rep Order Outcomes (Postgres orders, LTM iPad)
- **Query**: Q-01 Step 2 | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres `orders`
- **Period**: trailing 12 months (created_at > NOW() − 12 months), order_source = 'ipad', submitted, not deleted
- **Run date**: 2026-06-12 | **Row count**: 30 reps
- Name normalization applied (collapsed double-spaces). No case-dup or mangled-name merges required.
- `HighPoint Showroom` = confirmed operational exclusion (see showroom_scan_results.md) — keep out of rep leaderboard/archetype. `Dunn Lighting` = ambiguous, retained.

| rep_name | total_orders | total_gmv | avg_order_value | unique_customers |
|---|---|---|---|---|
| Jeff Nicholson | 20 | $73,197.30 | $3,659.87 | 20 |
| Chas Lassoff | 11 | $58,374.20 | $5,306.75 | 7 |
| Steve Linder | 6 | $56,623.00 | $9,437.17 | 5 |
| Katy McCully | 38 | $56,371.23 | $1,483.45 | 16 |
| Brad Dobson | 4 | $49,831.00 | $12,457.75 | 4 |
| Vince Hall | 9 | $34,469.90 | $3,829.99 | 9 |
| Megan Trosclair | 5 | $28,131.80 | $5,626.36 | 5 |
| Matt Sullivan | 11 | $24,583.50 | $2,234.86 | 9 |
| Mike Hemsarth | 5 | $22,615.90 | $4,523.18 | 2 |
| Zachary Rapp | 11 | $22,434.30 | $2,039.48 | 5 |
| Shelly Orban | 6 | $19,845.00 | $3,307.50 | 5 |
| Cindy Vackar | 2 | $16,792.40 | $8,396.20 | 2 |
| Jeff Izower | 3 | $12,495.70 | $4,165.23 | 1 |
| Forrest Denbow | 2 | $10,988.00 | $5,494.00 | 1 |
| HighPoint Showroom | 2 | $8,084.00 | $4,042.00 | 1 |
| Collin Framburg | 2 | $7,338.00 | $3,669.00 | 1 |
| Nick Brown | 2 | $6,875.50 | $3,437.75 | 2 |
| Brad Krieger | 2 | $6,347.60 | $3,173.80 | 2 |
| Kevin Taylor | 2 | $6,155.00 | $3,077.50 | 2 |
| Kelly York | 2 | $6,021.40 | $3,010.70 | 2 |
| Pauline Theos | 1 | $4,573.00 | $4,573.00 | 1 |
| Amy Matteson | 5 | $4,205.78 | $841.16 | 2 |
| Cindy Rogers | 6 | $3,939.00 | $656.50 | 5 |
| Kristen Cavanagh | 1 | $3,361.95 | $3,361.95 | 1 |
| Rob Hailpern | 1 | $2,813.30 | $2,813.30 | 1 |
| Sebastian Castrillon | 1 | $2,649.60 | $2,649.60 | 1 |
| Gary Ellis | 1 | $1,320.00 | $1,320.00 | 1 |
| Steve Jones | 3 | $1,199.00 | $399.67 | 2 |
| Amit Sharma | 1 | $1,148.00 | $1,148.00 | 1 |
| Dunn Lighting | 1 | $316.00 | $316.00 | 1 |

**Totals (all rows)**: 166 LTM iPad orders, $553,100.36 GMV. Qualifying reps (≥10 orders): Katy McCully (38), Jeff Nicholson (20), Chas Lassoff (11), Matt Sullivan (11), Zachary Rapp (11) → HAS_SALES_SECTION = true.
