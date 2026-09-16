# Q-12: Customer Activation & ERP Penetration — Crystorama (clm, org_id=64)
- **Query**: Q-12 (Postgres)
- **Period**: Various windows
- **Row count**: 1
- **Run date**: 2026-04-20

| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
|----|----|----|----|----|
| 4,723 | 608 | 113 | 93 | 50 |

## Derived Metrics

- **Lapsed eCat**: 608 − 113 = 495 buyers who have ordered before but not in 12 months
- **Never activated**: 4,723 − 608 = 4,115 ERP records with no eCat history
- **eCat retention rate**: 113 / 608 = 18.6%
