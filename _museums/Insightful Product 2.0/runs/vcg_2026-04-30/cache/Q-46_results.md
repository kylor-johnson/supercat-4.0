# Q-46: Workflow Maturity — Visual Comfort Signature (vcg, org_id=141)
- **Period**: 90 days
- **Source**: Postgres MCP + BigQuery Mixpanel
- **Run date**: 2026-04-30

## Postgres: eCat Order Submissions (90 days)
- **Submitted eCat orders**: 59

## BigQuery Mixpanel: Behavioral Events (90 days)

| Event Category | Event Count |
|---------------|-------------|
| customer_targeting_events | 22,184 |
| product_discovery_events | 50,071 |
| presentation_events | 1,370 |

## Submit Rate
- Not directly computed. Denominator is total behavioral events (not individual submit-order-tracking). Submit rate would require session-level funnel analysis mapping product_discovery → presentation → order submission, which is not available from aggregate event counts alone.
