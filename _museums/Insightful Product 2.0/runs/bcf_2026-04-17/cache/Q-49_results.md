# Q-49 — Buyer Repeat Purchase (Portal)

- **Org:** Braxton Culler (bcf, org_id=171)
- **Period:** Last 12 months
- **Run date:** 2026-04-17

## Gate Check (1 row)

| total_portal_orders | orders_with_buyer_name | orders_with_bill_to |
|---|---|---|
| 1,614 | 1,614 | 1,614 |

Gate passed — all 1,614 portal orders have buyer_name and customer_bill_to_number populated.

## Repeat Purchase Cohort (1 row)

| new_buyers_in_period | returned_within_period | returned_within_90d | returned_within_180d | repeat_rate_90d |
|---|---|---|---|---|
| 303 | 151 | 134 | 149 | 44.2% |
