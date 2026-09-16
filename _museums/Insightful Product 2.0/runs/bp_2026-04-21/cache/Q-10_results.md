# Q-10: Feature Enablement Gap Analysis — Buster & Punch (bp, org_id=250)
- **Query**: Q-10 (VM-10)
- **Period**: Current snapshot
- **Run date**: 2026-04-21
- **Rows returned**: 1

| field | value |
|-------|-------|
| enable_sales_portal | false |
| enable_online_catalog | true |
| enable_online_ordering | true |
| kit_item_count | 0 |
| contract_price_count | 0 |
| enrollment_count | 12 |
| smart_stack_count | 6 |
| shared_resource_count | 16 |
| portal_order_count | 0 |

**Notes**:
- Online Catalog is enabled
- Online Ordering (B2B Cart) is enabled but has 0 server orders ever — feature is configured but never activated
- Sales Portal (internal BI) is not enabled
- No kit items or contract prices configured
- 6 Smart Stacks created (all published)
- 16 shared resources (all directory-type)
- 12 enrollment applicants exist
