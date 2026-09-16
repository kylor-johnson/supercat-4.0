# Q-49 — Buyer-Level Repeat Purchase (portal_orders, LTM)
- **Query**: Q-49 | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres `portal_orders` | **Run date**: 2026-06-12
- **Gate**: buyer attribution confirmed — 141,409 portal_orders all carry buyer_name + customer_bill_to_number.
- **Framing**: `portal_orders` = ERP-synced total business across all channels (NOT eCat-specific).

| new_buyers_in_period | returned_within_period | returned_within_90d | returned_within_180d | repeat_rate_90d |
|---|---|---|---|---|
| 2,056 | 1,419 | 1,129 | 1,317 | 54.9% |

**Note**: Of 2,056 buyers placing a first (LTM) ERP order, 54.9% reordered within 90 days and 64% within 180 days — strong all-channel repeat behavior. This is total business (all channels), not eCat self-service.
