# Q-46 — Workflow Maturity

- **Org:** Sarreid · org_id = 1
- **Period:** 90-day window (Postgres) / all-time (Mixpanel)
- **Row count:** 5 metrics
- **Run date:** 2026-04-17
- **Exclusions:** None

---

## Postgres Side

| metric | value |
|--------|-------|
| submitted_ecat_orders_90d | 120 |

## Mixpanel Side

| metric | event_count |
|--------|------------|
| customer_targeting_events | 15,295 |
| product_discovery_events | 35,849 |
| presentation_events | 2,167 |

## Submit Rate Calculation

| metric | value |
|--------|-------|
| submitted_orders (90d) | 120 |
| presentation_events (denominator for VM-46) | 2,167 |
| submit_rate | 5.5% |
| band | Minimal submit-through (< 10%) |

> Submit rate computed as 120 / 2,167 = ~5.5%. Per VM-46 band definitions, this falls in the "Minimal submit-through" band (< 10%).
