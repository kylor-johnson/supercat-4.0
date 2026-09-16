# §4 Product & Inventory Intelligence — Highlights
- **Client:** Magnussen Home (mh, org_id=184)
- **Run date:** 2026-04-20
- **Subsections rendered:** 4 of 5 (Q-38a skipped — HAS_PORTAL_ORDERS = false)

## Subsection Summary

### 4.1 Top Sellers Out of Stock (Q-37)
- **CRITICAL CAVEAT:** Inventory is 256 days stale (last updated 2025-08-07) and covers only 22 items. All findings are directional only.
- 20 top-selling products show zero available inventory (zero on hand, zero on backorder, no receipt dates)
- Combined cumulative all-channel invoiced sales: $9.8M
- Collection 5614CB dominates: 7 of 20 OOS items, $4.2M cumulative revenue
- 8 of 20 items are dining seating (side chairs, host chairs, arm chairs) sold in 2-carton packs
- Top item: B5614-22 Double Drawer Dresser at $1,032,621 cumulative

### 4.2 New Introduction Performance (Q-42)
- 1,076 items flagged as new across 68 collections
- Only 6 items (collection 6330) have confirmed sell-through: $48,836, 94 units
- 1,070 new items (99.4%) with zero all-channel invoiced sales
- Largest zero-sales collections: P444 (56 items), P433 (49), P437 (45)
- May reflect pre-market staging rather than failed launches

### 4.3 Catalog Completeness (Q-07)
- Visible: 6,202 products, 96.7% complete
- Hidden: 1,439 products, 99.9% complete
- 205 visible products missing images; zero missing prices
- Above 90% benchmark — callout triggered for 205 items > 50 threshold

### 4.4 What's Selling (Q-39)
- 44 categories, 25 collections (top by cumulative all-channel sales)
- Dominant collection: 5614CB at $7.8M from 43 items ($182,115/item)
- Top category: D6069 at $8.5M from 135 items
- Most efficient category: E0119 at $108,189/item (30 products)
- Most efficient small collections: 5013 ($269K/item, 5 products), 5333 ($201K/item, 7 products)
- Long-tail categories (Y5059, A0000, Y0000) under $6K cumulative — minimal business impact

## Key Decisions
- Q-38a (Product Velocity Trend) **skipped** — HAS_PORTAL_ORDERS = false, no portal_order_items data
- VM-38b is pending_engineering — not attempted
- Inventory staleness caveat rendered as top-level alert in OOS subsection, plus "(stale data)" in stat line
- All sales figures framed as "cumulative all-channel invoiced sales" — no invoice_date available for period-specific reporting
- "ERP" terminology avoided throughout; used "all-channel invoiced sales" and "your business system"
- Inventory coverage note included: only 22 items out of 7,641 in catalog
