# Q-12: Customer Activation & ERP Penetration — Buster & Punch (bp, org_id=250)
- **Query**: Q-12 (VM-12)
- **Period**: Rolling 12/6/3 months + all-time
- **Run date**: 2026-04-21
- **Rows returned**: 1

| metric | value |
|--------|-------|
| total_erp_customers | 7,084 |
| total_ever_ordered_via_ecat | 16 |
| active_12mo | 7 |
| active_6mo | 2 |
| active_3mo | 2 |

## Derived Metrics

| metric | value |
|--------|-------|
| lapsed_ecat | 9 (16 all-time − 7 active LTM) |
| never_activated | 7,068 (7,084 ERP − 16 ever ordered) |
| ecat_retention_rate | 43.8% (7 active / 16 ever ordered) |
| 6mo_retention_rate | 12.5% (2 / 16) |
| 3mo_retention_rate | 12.5% (2 / 16) |
