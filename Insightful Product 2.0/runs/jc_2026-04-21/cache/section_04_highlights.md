# §4 Product & Inventory Intelligence — Highlight Candidates
- **Client:** Jonathan Charles Fine Furniture Ltd. (jc, org_id=65)
- **Run date:** 2026-04-21
- **Subsections rendered:** 5 of 5

## Subsection Summary

### 4.1 Top Sellers Currently Out of Stock (Q-37)
- 20 top-selling products at zero available inventory (zero on hand, zero on backorder, no receipt dates)
- Combined cumulative all-channel invoiced sales: $3.5M
- Églomisé & Bronze collection (COL224) dominates: 5 of 20 OOS items, ~$990K cumulative
- Rosenell (COL201) contributes 4 OOS items at $539K combined
- Top item: 494710 Empire Style Sofa with Gold Leaf at $710,111 cumulative
- Inventory caveat applied: current-state snapshot only, no duration data

### 4.2 New Introduction Performance (Q-42)
- 113 items flagged as new across 21 collections
- All 113 items show $0 all-channel invoiced sales and 0 units sold
- Largest launches: COL48 (18 items), COL745 (16 items), COL53 (12 items)
- Zero sales is almost certainly a data-timing artifact — items introduced after last sales_data import
- COL48 and COL817 items appear in recent portal orders, confirming early traction exists outside sales_data

### 4.3 Product Velocity Trend (Q-38a)
- 6-month window: Oct 2025–Mar 2026 via portal_order_items
- November 2025 peak: ~1,181 units, ~80 distinct items, 19 orders (market show effect)
- Top items: Atoll Side Chair (COL817, 24 units), Terra Dining Side Chair (COL745, 24 units)
- Orsman collection (COL48) placed 3 items in top 5
- All eCat orders occurred Oct–Dec 2025; zero in Jan–Apr 2026 — seasonal/market-driven pattern

### 4.4 Catalog Completeness (Q-07)
- Visible: 21,125 products, 85.4% complete
- 1,831 missing images (8.7%), 1,359 missing pricing (6.4%)
- Below 90% benchmark — alert callout rendered
- No hidden products in catalog

### 4.5 What's Selling (Q-39)
- 37 categories, 25 collections (top by cumulative all-channel sales)
- Top category: CAT115 (Lamp Tables) at $2.1M from 399 items
- Highest per-item yield category: CAT30 at $17,184/item (92 products)
- Top collection: COL841 at $1.3M from 152 items
- Most efficient collection: COL201 (Rosenell) at $75,737/item (15 products, $1.1M total)
- COL79 also efficient at $23,825/item from 23 products

## Highlight Candidates

1. **$3.5M in Proven Sellers Sitting at Zero Inventory** — The top 20 out-of-stock products represent $3.5M in cumulative all-channel sales, led by the Empire Style Sofa ($710K) and five Églomisé & Bronze items (~$990K combined). All show zero availability with no replenishment scheduled. [→ §product]
2. **Rosenell Collection: Highest Revenue Efficiency at $75,737/Item** — COL201 delivers $1.1M from just 15 items, nearly 9× the per-item yield of the top collection by total revenue (COL841). Four Rosenell items are also on the OOS list, compounding the missed-revenue risk. [→ §product]
3. **Catalog Completeness at 85.4% — Below 90% Target** — 1,359 products missing pricing and 1,831 missing images leave 14.6% of the 21,125-product visible catalog incomplete. Products without pricing are effectively unbuyable through the digital catalog. [→ §product]
4. **iPad Ordering Concentrated in Market Show Windows** — November 2025 drove 1,181 units and ~80 distinct items via iPad orders, then activity dropped sharply. All eCat-originated orders occurred Oct–Dec 2025 with zero in Jan–Apr 2026, indicating event-driven rather than continuous usage. [→ §product]

## Priority Action Candidate
- **HIGH**: Investigate replenishment for the 5 Églomisé & Bronze (COL224) and 4 Rosenell (COL201) items currently out of stock — these 9 items alone represent $1.5M in cumulative all-channel sales and show zero inventory, zero backorder, and no scheduled receipt dates. Restocking these proven sellers removes the most immediate revenue-at-risk from the OOS list. [→ §product]
