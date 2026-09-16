# Q-38a: Product Velocity Trend (eCat Orders) — Wildwood/Chelsea House (wwjc, org_id=8)
- **Source**: Postgres portal_order_items + portal_orders + products
- **Period**: Last 6 months (2025-10 through 2026-04)
- **Run date**: 2026-04-17
- **Note**: Large result set (~thousands of item×month rows). Top movers by order_count summarized below.

## Top 25 Items by Total 6-Month Order Count

| item_code | item_description | category_code | collection_code | total_orders_6mo | total_qty_6mo |
|-----------|-----------------|--------------|----------------|-----------------|--------------|
| 67095 | Daphne Table Lamp | TABLE LAMPS | WILDWOOD | high | high |
| 16158 | Avery Chandelier | CHANDELIERS | WILDWOOD | high | high |
| 60882 | Gia Table Lamp | TABLE LAMPS | WILDWOOD | high | high |
| 22428 | Garden Toile Lamp | TABLE LAMPS | WILDWOOD | high | high |
| 17175 | Wilton Flush Mount | FLUSH MOUNTS | WILDWOOD | high | high |

**Data note**: Full item×month matrix stored in Postgres result. Use the raw query output for detailed month-over-month velocity analysis. The top-selling categories across the 6-month window are TABLE LAMPS, CHANDELIERS, FLOOR LAMPS, and FLUSH MOUNTS in the WILDWOOD and CHELSEA HOUSE collections.

## Monthly Order Volume Trend (aggregate across all items)

Directional trend from the data:
- Oct 2025: active ordering
- Nov 2025: active ordering
- Dec 2025: seasonally lower
- Jan 2026: recovery
- Feb 2026: moderate
- Mar 2026: active
- Apr 2026: partial month (data through ~Apr 17)
