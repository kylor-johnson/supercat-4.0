# Q-12: Customer Activation & ERP Penetration
- **Query ID**: Q-12 (VM-12)
- **Org**: Wildwood/Chelsea House (wwjc, org_id=8)
- **Period**: All-time + trailing 12/6/3 months
- **Row count**: 1
- **Run date**: 2026-04-16
- **Exclusions**: None

| Metric | Value |
|--------|-------|
| total_erp_customers | 13,776 |
| total_ever_ordered_via_ecat | 9,434 |
| active_12mo | 2,393 |
| active_6mo | 1,572 |
| active_3mo | 950 |

## Derived Metrics

| Metric | Value |
|--------|-------|
| lapsed_ecat (ever ordered - active_12mo) | 7,041 |
| never_activated (ERP total - ever ordered) | 4,342 |
| ecat_retention_rate (active_12mo / ever ordered) | 25.4% |
