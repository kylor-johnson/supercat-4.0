# Q-18 — eCat Order Velocity & Trend — Palecek (pf, org_id=32)
- **Run date**: 2026-04-21
- **Period**: LTM
- **Source**: Postgres orders + portal_orders

## Part A — eCat Orders

| month | total_ecat_orders | ipad_orders | ecat_online_orders | ecat_gmv | ecat_aov |
|-------|------------------|-------------|-------------------|----------|---------|
| 2026-04 | 179 | 179 | 0 | $1,248,167.05 | $6,973.00 |
| 2026-03 | 281 | 281 | 0 | $2,555,504.53 | $9,094.32 |
| 2026-02 | 190 | 190 | 0 | $1,196,110.45 | $6,295.32 |
| 2026-01 | 164 | 164 | 0 | $869,660.84 | $5,302.81 |
| 2025-12 | 205 | 205 | 0 | $1,344,018.95 | $6,556.19 |
| 2025-11 | 192 | 192 | 0 | $1,080,832.36 | $5,629.34 |
| 2025-10 | 224 | 224 | 0 | $1,409,240.15 | $6,291.25 |
| 2025-09 | 298 | 298 | 0 | $1,678,219.46 | $5,631.61 |
| 2025-08 | 244 | 244 | 0 | $1,912,531.18 | $7,838.24 |
| 2025-07 | 220 | 220 | 0 | $1,473,078.53 | $6,695.81 |
| 2025-06 | 260 | 260 | 0 | $1,632,518.08 | $6,278.92 |
| 2025-05 | 336 | 336 | 0 | $2,536,531.31 | $7,549.20 |
| 2025-04 | 97 | 97 | 0 | $781,532.58 | $8,057.04 |

Note: 100% iPad orders — no eCat Online (server) orders. HAS_CART = false confirmed.

## Part B — ERP Total Context (portal_orders)

| month | total_erp_orders | total_erp_gmv |
|-------|-----------------|--------------|
| 2026-04 | 613 | $2,615,781.97 |
| 2026-03 | 716 | $3,625,566.08 |
| 2026-02 | 328 | $1,913,510.97 |
| 2026-01 | 184 | $1,433,785.49 |
| 2025-12 | 93 | $1,289,259.60 |
| 2025-11 | 54 | $372,703.34 |
| 2025-10 | 62 | $245,911.17 |
| 2025-09 | 10 | $132,011.14 |
| 2025-08 | 15 | $232,552.45 |
| 2025-07 | 9 | $30,716.30 |
| 2025-06 | 6 | $139,853.40 |
| 2025-05 | 3 | $12,540.00 |

Note: ERP order volume was very low May–Nov 2025 (3–62/mo), then ramped sharply Jan–Apr 2026 (184–716/mo). This suggests the portal_orders ERP sync was recently activated or expanded. The LTM ERP GMV ($12.0M) is significantly below eCat GMV ($19.7M), confirming partial ERP sync (VM45 Gate 1 FAIL).
