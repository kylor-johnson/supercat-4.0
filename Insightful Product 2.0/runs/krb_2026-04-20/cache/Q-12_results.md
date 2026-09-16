# Q-12: Customer Activation & ERP Penetration
- **Org**: Kaleen Rugs & Broadloom (krb, org_id=244)
- **Period**: All-time + trailing 12/6/3 months
- **Rows returned**: 1
- **Run date**: 2026-04-20

| metric | value |
|--------|-------|
| total_erp_customers | 2,208 |
| total_ever_ordered_via_ecat | 1 |
| active_12mo | 0 |
| active_6mo | 0 |
| active_3mo | 0 |

## Derived Metrics

| metric | value |
|--------|-------|
| lapsed_ecat | 1 (total_ever - active_12mo) |
| never_activated | 2,207 (erp_total - ever_ordered) |
| ecat_retention_rate | 0.0% (active_12mo / total_ever) |

Note: Only 1 customer has ever ordered via eCat. That customer is now lapsed (no orders in 12 months). The single LTM order (August 2025) appears to have a NULL or non-matching customer_num, as it does not register in the distinct customer count for active_12mo. 2,207 of 2,208 ERP customers have never ordered via eCat.
