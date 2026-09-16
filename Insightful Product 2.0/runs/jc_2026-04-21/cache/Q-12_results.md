# Q-12: Customer Activation & ERP Penetration
- **Org**: Jonathan Charles Fine Furniture Ltd. (jc, org_id=65)
- **Period**: Various windows (all-time, 12mo, 6mo, 3mo)
- **Run date**: 2026-04-21
- **Rows returned**: 1

| Metric | Value |
|--------|-------|
| total_erp_customers | 34 |
| total_ever_ordered_via_ecat | 19 |
| active_12mo | 9 |
| active_6mo | 9 |
| active_3mo | 0 |

## Derived Metrics

| Metric | Value | Formula |
|--------|-------|---------|
| lapsed_ecat | 10 | total_ever_ordered (19) - active_12mo (9) |
| never_activated | 15 | total_erp_customers (34) - total_ever_ordered (19) |
| ecat_retention_rate | 47.4% | active_12mo (9) / total_ever_ordered (19) |

**Note**: active_3mo = 0 indicates no eCat orders have been placed in the last 3 months (Jan–Apr 2026). All 9 active-12mo customers ordered between Apr–Dec 2025. This is consistent with the Q-18 monthly trend showing zero eCat orders after December 2025.
