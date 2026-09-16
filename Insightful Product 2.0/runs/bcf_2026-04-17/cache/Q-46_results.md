# Q-46 · eCat Selling Workflow Maturity

| Field | Value |
|---|---|
| **Query** | Q-46 |
| **Org** | Braxton Culler (bcf, org_id=171) |
| **Period** | Last 90 days (Postgres) / All-time cumulative (Mixpanel) |
| **Run Date** | 2026-04-17 |
| **Exclusions** | orders: is_marked_deleted = false OR IS NULL; is_submitted = true |

## Postgres Side — eCat Submit Count (Numerator)

| metric | value |
|---|---|
| submitted_ecat_orders_90d | 779 |

## Mixpanel Side — Behavioral Signal Count (Denominator)

| metric | value |
|---|---|
| customer_targeting_events | 11,617 |
| product_discovery_events | 39,793 |
| presentation_events | 1,266 |

## Band Classification

Submit rate context: 779 submitted orders in 90 days against all-time Mixpanel behavioral signals. Mixpanel aggregates are cumulative (not 90-day windowed), so direct ratio is not apples-to-apples. Stage 2 will compute the appropriate band classification using comparable time windows where available.
