# Q-16: ERP Total Business Visibility — Crystorama (clm, org_id=64)
- **Query**: Q-16 (Postgres — portal_orders monthly)
- **Period**: LTM
- **Row count**: 13 (valid months only; junk date rows excluded)
- **Run date**: 2026-04-20
- **Note**: portal_orders contained rows with invalid future dates (years 2080–9380); these are excluded from this cache file as data quality artifacts.

| month | total_erp_orders | unique_accounts | total_erp_gmv | ecat_originated_orders | ecat_originated_gmv | market_orders |
|-------|-----------------|----------------|--------------|----------------------|--------------------|--------------| 
| 2026-04 | 4,040 | 594 | $2,300,435.65 | 0 | $0.00 | 0 |
| 2026-03 | 6,817 | 776 | $4,013,422.51 | 0 | $0.00 | 0 |
| 2026-02 | 5,980 | 736 | $3,475,333.64 | 0 | $0.00 | 0 |
| 2026-01 | 5,900 | 655 | $3,128,088.34 | 0 | $0.00 | 0 |
| 2025-12 | 5,649 | 700 | $2,891,252.38 | 0 | $0.00 | 0 |
| 2025-11 | 6,533 | 702 | $3,267,070.20 | 0 | $0.00 | 0 |
| 2025-10 | 6,524 | 758 | $3,403,165.70 | 0 | $0.00 | 0 |
| 2025-09 | 5,830 | 759 | $2,986,384.00 | 0 | $0.00 | 0 |
| 2025-08 | 6,308 | 732 | $3,197,232.18 | 0 | $0.00 | 0 |
| 2025-07 | 5,561 | 741 | $2,888,136.65 | 0 | $0.00 | 0 |
| 2025-06 | 5,228 | 695 | $2,904,270.31 | 0 | $0.00 | 0 |
| 2025-05 | 5,859 | 711 | $3,210,861.14 | 0 | $0.00 | 0 |
| 2025-04 | 2,390 | 460 | $1,617,872.69 | 0 | $0.00 | 0 |

**Note**: ecat_originated_orders = 0 across all months — order_origin field is not populated with 'ECAT' tag for this org. This does not mean eCat orders are absent; it means the ERP sync does not carry the eCat origin tag.
