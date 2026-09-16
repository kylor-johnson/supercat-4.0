# Q-46 — eCat Selling Workflow Maturity
- **Query**: Q-46 | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres `orders` (numerator) + BigQuery Mixpanel `org_feature_usage_report` (denominator signals) | **Run date**: 2026-06-12

## Numerator (Postgres) — submitted eCat orders, last 90 days
| submitted_ecat_orders_90d |
|---|
| 20 |

## Denominator (Mixpanel, all-time org behavioral signals)
| customer_targeting_events | product_discovery_events | presentation_events |
|---|---|---|
| 10,312 | 20,421 | 1,121 |

**Band classification**: Mixpanel `submit_order` is effectively untracked for this org (org-wide = 2), so a Mixpanel-based submit-through % is not interpretable. Using Postgres as authoritative: the platform is used heavily as a **selling/presentation layer** (high customer-targeting + product-discovery + library usage) with order submission largely captured outside eCat. Frame as "enablement-heavy / selling-layer," never "low platform value." Treat band as **Non-submit-through / Enablement-heavy** given the Mixpanel order-tracking gap.
