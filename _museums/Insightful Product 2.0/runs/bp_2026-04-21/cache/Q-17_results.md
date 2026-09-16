# Q-17: Dormant eCat Customer Identification — Buster & Punch (bp, org_id=250)
- **Query**: Q-17 (VM-17)
- **Period**: Trailing 12 months (lapsed = ordered 4–12mo ago, not in last 3mo)
- **Run date**: 2026-04-21
- **Rows returned**: 5 (recently lapsed) + 5 (at-risk high-value)

## Recently Lapsed (ordered 4–12mo ago, NOT in last 3 months)

| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
|-------------|--------------|---------------|---------------------|----------------------|-------------------|
| 107040 | Moxie Design Studio | CA | 2025-05-14 | 1 | $4,358.75 |
| 126490 | Eric Baker Architects | SC | 2025-04-22 | 1 | $3,609.00 |
| 126364 | Elite Interiors | AZ | 2025-08-15 | 1 | $2,876.78 |
| 53740 | Exquisite Kitchen Design | CO | 2025-07-22 | 1 | $1,134.47 |
| 128028 | Andrika King Design | CA | 2025-05-05 | 1 | $49.50 |

## At-Risk High-Value (ordered in LTM but last order >90 days ago)

| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
|-------------|--------------|---------------|--------------|---------------------|--------------------------|
| 107040 | Moxie Design Studio | CA | $4,358.75 | 2025-05-14 | 341 |
| 126490 | Eric Baker Architects | SC | $3,609.00 | 2025-04-22 | 363 |
| 126364 | Elite Interiors | AZ | $2,876.78 | 2025-08-15 | 248 |
| 53740 | Exquisite Kitchen Design | CO | $1,134.47 | 2025-07-22 | 272 |
| 128028 | Andrika King Design | CA | $49.50 | 2025-05-05 | 350 |

**Notes**:
- 5 of 7 LTM eCat customers are now lapsed (>90 days since last order)
- Only 2 customers remain active (ordered in last 3 months)
- Combined lapsed GMV: $12,028.50
