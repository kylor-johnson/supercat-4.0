# Q-16 — ERP Total Business Visibility (portal_orders, LTM)
- **Query**: Q-16 | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres `portal_orders` | **Run date**: 2026-06-12
- **Framing**: ERP-synced total business across all channels (NOT buyer self-service). 13 corrupt-date outlier rows (order_date years 9380/9260/9201/9021/8022/7690/6949/6021/2870/2220/2140/2080×2, 1 order each, ~$5.2K total) excluded from the LTM rollup below.

| month | total_erp_orders | unique_accounts | total_erp_gmv | ecat_originated_orders | market_orders |
|---|---|---|---|---|---|
| 2026-06 | 2,442 | 472 | $1,539,072.40 | 0 | 0 |
| 2026-05 | 6,796 | 722 | $3,835,752.08 | 0 | 0 |
| 2026-04 | 6,676 | 774 | $3,820,107.27 | 0 | 0 |
| 2026-03 | 6,817 | 776 | $4,014,035.61 | 0 | 0 |
| 2026-02 | 5,980 | 736 | $3,476,059.04 | 0 | 0 |
| 2026-01 | 5,900 | 655 | $3,130,006.34 | 0 | 0 |
| 2025-12 | 5,649 | 700 | $2,891,252.38 | 0 | 0 |
| 2025-11 | 6,533 | 702 | $3,267,437.74 | 0 | 0 |
| 2025-10 | 6,524 | 758 | $3,401,656.39 | 0 | 0 |
| 2025-09 | 5,830 | 759 | $2,986,384.00 | 0 | 0 |
| 2025-08 | 6,308 | 732 | $3,197,232.18 | 0 | 0 |
| 2025-07 | 5,561 | 741 | $2,888,136.65 | 0 | 0 |
| 2025-06 | 2,954 | 523 | $1,672,861.01 | 0 | 0 |

**LTM totals (valid months)**: 73,970 ERP orders, ≈ $40.12M GMV. With 13 corrupt-date rows = 73,983 rows. `order_origin` is not populated as 'ECAT'/market codes for this org (all 0). Frame only as "orders synced from your ERP / total business across all channels." Strong, consistent monthly volume; partial months at both ends (Jun 2025 / Jun 2026).
