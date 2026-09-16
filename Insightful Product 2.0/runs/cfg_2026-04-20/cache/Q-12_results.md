# Q-12: Customer Activation & ERP Penetration — Charleston Forge (cfg, org_id=83)
- **Run date**: 2026-04-20
- **Row count**: 1

| Metric | Value |
|--------|-------|
| total_erp_customers | 2,541 |
| total_ever_ordered_via_ecat | 921 |
| active_12mo | 200 |
| active_6mo | 110 |
| active_3mo | 51 |

## Derived Metrics
- lapsed_ecat = 921 - 200 = **721** (ordered before but not in 12 months)
- never_activated = 2,541 - 921 = **1,620** (ERP records with no eCat history)
- ecat_retention_rate = 200 / 921 = **21.7%**
