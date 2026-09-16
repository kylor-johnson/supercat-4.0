# Q-12: Customer Activation & ERP Penetration — Kuzco Lighting Inc. (kll, org_id=166)
- **Period**: Trailing 12 months (activation windows at 12mo, 6mo, 3mo)
- **Run date**: 2026-04-17
- **Rows returned**: 1

| metric | value |
|--------|-------|
| total_erp_customers | 2,765 |
| total_ever_ordered_via_ecat | 417 |
| active_12mo | 181 |
| active_6mo | 125 |
| active_3mo | 60 |

## Derived Metrics

| metric | value |
|--------|-------|
| lapsed_ecat (ordered before, not in 12mo) | 236 |
| never_activated (ERP records, no eCat history) | 2,348 |
| ecat_retention_rate (active_12mo / ever_ordered) | 43.4% |
