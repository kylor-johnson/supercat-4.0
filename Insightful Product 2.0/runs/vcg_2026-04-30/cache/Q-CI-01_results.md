# Q-CI-01: Org Summary Lookup — Visual Comfort Signature (vcg, org_id=141)
- **Source**: BigQuery MCP (insightful_product.org_summary)
- **Run date**: 2026-04-30
- **Row count**: 1

## Org Summary

| Field | Value |
|-------|-------|
| org_shortname | vcg |
| org_name | Visual Comfort Signature |
| segment | Commerce-Active |
| health_score | 0.75 |
| recurring_services | eCat (iPad) Service; eCat (iPad) - Add'l Seats; eCat Online service |
| feature_depth | 3 |
| has_clicky_portal | false |
| clicky_prefix | (null) |
| order_configured_item | 0 |
| view_kit | 0 |
| order_kit | 0 |
| access_sales_portal | 229 |
| arr | $11,304 |
| mrr | $1,606.50 |
| mp_submit_order | 265 |
| mp_total_logins | 9,846 |
| mp_total_events | (aggregated from user-level data) |
| mp_total_users | 111 |

## Derived Fields

| Field | Value | Logic |
|-------|-------|-------|
| HAS_CART | false | No "B2B Cart" in recurring_services |
| HAS_CPQ | false | order_configured_item = 0 |
| HAS_KIT | false | view_kit = 0 AND order_kit = 0 |
| BUNDLE | iPad-only | Recurring services include eCat iPad only |
| VERTICAL | Lighting | From peer benchmark CSV |
