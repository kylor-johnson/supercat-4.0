# Q-10 — Feature Enablement Gap Analysis
- **Query**: Q-10 | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres `mobile_sites` + counts | **Run date**: 2026-06-12
- **Row count**: 1

| field | value |
|---|---|
| enable_sales_portal | true |
| enable_online_catalog | true |
| enable_online_ordering | false |
| kit_item_count | 0 |
| contract_price_count | 0 |
| smart_stack_count | 21 |
| shared_resource_count | 36 |
| portal_order_count | 141,409 |

**Note**: `enable_online_ordering = false` confirms HAS_CART = false (no B2B Cart). Sales Portal + Online Catalog active. CPQ/kits not in use (expansion opportunity, not a gap). 21 SmartStacks, 36 shared resources active.
