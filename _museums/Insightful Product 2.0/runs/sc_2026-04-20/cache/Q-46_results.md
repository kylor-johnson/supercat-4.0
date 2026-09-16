# Q-46 Results — eCat Selling Workflow Maturity
- **Org**: Gabriella White (sc, org_id=69)
- **Period**: 90-day window (Postgres) + all-time (Mixpanel)
- **Run date**: 2026-04-20

## Postgres Side (Numerator)

| Metric | Value |
|--------|-------|
| Submitted eCat orders (90d) | 7,629 |

## BigQuery Mixpanel Side (Denominator — all-time org totals)

| Metric | Value |
|--------|-------|
| Customer targeting events | 400,966 |
| Product discovery events | 369,548 |
| Presentation events | 5,730 |

Note: Denominator is all-time cumulative. Submit rate calculation requires time-windowed Mixpanel data (not available in org_feature_usage_report). All-time submit_order = 40,121. Band classification: > 25% — **Transactional** (eCat is a primary order capture channel).
