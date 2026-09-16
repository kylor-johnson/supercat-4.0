# Q-10: Feature Enablement Gap Analysis — Kindel Karges Furniture (kkc, org_id=99)
- **Query ID**: Q-10
- **VM**: VM-10
- **Run date**: 2026-04-23
- **Period**: Current snapshot
- **Rows returned**: 0 (mobile_sites table has no row for org_id=99)

## Feature Flags (from org_summary as fallback)

| Feature | Status | Source |
|---------|--------|--------|
| eCat iPad App | Active | recurring_services |
| eCat Online - Closed Site | Active | recurring_services |
| eCat Online - Portal | Active | recurring_services |
| eCat Online service | Active | recurring_services |
| B2B Cart (Online Ordering) | Not present | recurring_services |
| CPQ / Configurable Items | Active (20 configured item events in Mixpanel) | org_summary.order_configured_item |

## Data Presence Summary (from instance summary query)

| Entity | Count |
|--------|-------|
| Active products | 766 |
| Total ERP customers | 368 |
| Active users | 14 |
| Smart Stacks | 11 |
| Shared Resources (Library) | 104 |
| Kit items | 0 |
| Contract prices | 0 |
| Portal orders | 0 |
| Portal order items | 0 |
| Sales data rows | 21 |
| Inventory rows | 0 |
| Import events | 1,202 |
| Login events | 1,485 |

**Note**: mobile_sites table returned no rows for this org. Feature flags derived from org_summary.recurring_services and Mixpanel event counts instead.
