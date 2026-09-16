# Q-10: Feature Enablement Gap Analysis — Kindel Furniture (kkc, org_id=99)
- **Maps to**: VM-10
- **Source**: Postgres MCP (`user-supercat-postgres-vpn`) — `mobile_sites`, `smart_stacks`, `shared_resources`, `portal_orders`
- **Run date**: 2026-04-20

## Feature Flag Status

| Feature | Status | Notes |
|---------|--------|-------|
| enable_sales_portal | — | No `mobile_sites` record found for org_id=99 |
| enable_online_catalog | — | No `mobile_sites` record found for org_id=99 |
| enable_online_ordering | — | No `mobile_sites` record found for org_id=99 |

**Note**: The `mobile_sites` table returned no rows for organization_id = 99. Feature flag status cannot be determined from this source. Platform features are confirmed via `recurring_services` in `org_summary`: "eCat (iPad) Service; eCat Online - Closed Site; eCat Online - Portal; eCat Online service". No B2B Cart.

## Feature Usage Counts

| Feature | Count |
|---------|-------|
| kit_item_count | 0 |
| contract_price_count | 0 |
| smart_stack_count | 11 |
| shared_resource_count | 13 (directories only — no document assets) |
| portal_order_count (all-time) | — (data_versions shows portal_orders entity updated 2026-03-13; LTM count = 0) |
