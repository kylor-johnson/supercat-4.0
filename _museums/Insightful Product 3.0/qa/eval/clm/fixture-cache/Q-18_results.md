# Q-18 — eCat Order Velocity & Trend (with ERP Context)
- **Query**: Q-18 (Parts A + B) | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres | **Run date**: 2026-06-12

## Part A — eCat orders by month (LTM)

| month | total_ecat_orders | ipad_orders | ecat_online_orders | ecat_gmv | ecat_aov |
|---|---|---|---|---|---|
| 2026-05 | 4 | 4 | 0 | $4,449.68 | $1,112.42 |
| 2026-04 | 7 | 7 | 0 | $9,730.05 | $1,390.01 |
| 2026-03 | 13 | 13 | 0 | $30,250.25 | $2,326.94 |
| 2026-02 | 29 | 29 | 0 | $92,103.60 | $3,175.99 |
| 2026-01 | 65 | 65 | 0 | $319,141.20 | $4,909.86 |
| 2025-12 | 5 | 5 | 0 | $6,773.45 | $1,354.69 |
| 2025-11 | 9 | 9 | 0 | $15,256.85 | $1,695.21 |
| 2025-10 | 8 | 8 | 0 | $14,388.57 | $1,798.57 |
| 2025-09 | 2 | 2 | 0 | $2,955.30 | $1,477.65 |
| 2025-08 | 4 | 4 | 0 | $4,989.07 | $1,247.27 |
| 2025-07 | 8 | 8 | 0 | $25,291.34 | $3,161.42 |
| 2025-06 | 12 | 12 | 0 | $27,771.00 | $2,314.25 |

**Note**: 100% iPad (0 server/eCat Online orders → confirms HAS_CART=false). Jan 2026 is the dominant peak (65 orders, $319K) — a market/order-entry surge. LTM eCat total ≈ 166 orders, $553.1K (partial June 2026 has 0 eCat rows in this window).

## Part B — ERP total context by month (LTM)

See Q-16_results.md for the full monthly ERP series. eCat share of total ERP order volume is ~0.2% by count (166 eCat / 73,970 ERP) — consistent with VM-45 Gate 2 FAIL (eCat = 1.38% of ERP GMV). eCat is an enablement/selling layer, not the primary capture channel.
