# Section Guide: §4 — Product & Inventory Intelligence
> **v1.0** — validated 2026-04-17 (RENWIL run). Last updated: 2026-04-17.

## Section Identity
- **id**: `product`
- **title**: Product & Inventory Intelligence
- **section number**: 4
- **include when**: `HAS_INVENTORY = true` OR `HAS_SALES_DATA = true`
- **skip when**: Neither `HAS_INVENTORY` nor `HAS_SALES_DATA` is true — omit silently, no note in delivered report

## Query Inputs

Read these cache files:
- `cache/Q-07_results.md` — Catalog completeness
- `cache/Q-37_results.md` — Top sellers currently out of stock
- `cache/Q-38a_results.md` — Product velocity trend
- `cache/Q-39_results.md` — Line analysis by category & collection
- `cache/Q-42_results.md` — New introduction performance
- `cache/gate_flags.md` — for `HAS_SALES_DATA`, `HAS_INVENTORY`, `HAS_CART`, `HAS_PORTAL_ORDERS`

## Subsection Order (do not reorder — render every subsection whose gate is met)

### 1. Top Sellers OOS (Q-37)

**Gate**: `HAS_SALES_DATA = true` AND `HAS_INVENTORY = true` (both required)

Build from `Q-37_results.md`. Surface top-selling products that are currently out of stock.

### 2. New Introduction Performance (Q-42)

**Gate**: `HAS_SALES_DATA = true`

Build from `Q-42_results.md`. Surface performance of newly introduced products.

### 3. Product Velocity Trend (Q-38a)

**Gate**: `portal_order_items` confirmed present (check `gate_flags.md` — `HAS_PORTAL_ORDERS = true` is the proxy)

Build from `Q-38a_results.md`. Exclude fee items, freight charges, and non-product line items from the analysis (Stage 1 filters by matching to `products` table on `ecat_item_number`).

Render as a table with these exact columns:

| Column | Content |
|--------|---------|
| Direction | ▲ accelerating / ▼ declining |
| Item Code | Product item code |
| Category | From products table if available |
| Recent 90d | Order count or unit count for the recent 90-day window |
| Prior 90d | Order count or unit count for the prior 90-day window |
| Velocity Change | Percentage with Accelerating/Declining badge |

Show the top 3–5 accelerating and top 3–5 declining items by absolute velocity change. Follow with a prose note: accelerating items should be flagged for inventory replenishment before stockout; declining items may warrant clearance pricing or repositioning.

**Omission rule**: If after filtering fee items fewer than 3 real products remain with meaningful velocity data, omit this subsection silently.

### 4. Catalog Completeness (Q-07)

**Gate**: Always (all accounts with a product catalog)

Build from `Q-07_results.md`. Render as a table with these exact columns:

| Column | Content |
|--------|---------|
| Visibility | Visible / Hidden |
| Products | Count of products |
| Missing Images | Count missing images |
| Missing Price | Count missing price |
| Complete % | Percentage of products that are complete |

Include a callout if completeness is below 90% or if more than 50 items need assets.

### 5. What's Selling (Q-39)

**Gate**: `HAS_SALES_DATA = true`

Build from `Q-39_results.md`. Render as a **single subsection** titled "What's Selling" — do not split into separate subsections for category and collection.

Inside this one subsection, render two progressive-disclosure tables:

**(a) Category breakdown** with columns:
- Category
- Orders
- GMV
- Customers
- Value/Order

**(b) Collection breakdown** with columns:
- Collection
- Items
- Orders
- GMV

Lead with a callout identifying the dominant collection by GMV share and any categories with zero or near-zero eCat orders despite catalog presence.

## Empty-Section Guard

After evaluating individual subsection gates, if zero subsections qualify for rendering, omit §4 entirely — do not render a section header or collapsible card with no content. The section-level gate (`HAS_INVENTORY = true` OR `HAS_SALES_DATA = true`) is a pre-filter; the final inclusion decision requires at least one subsection to be buildable from query results.

## Section-Specific Rules

- **VM-38b is `pending_engineering`** — do not attempt to run. Do not fabricate product velocity data from `sales_data` without an `invoice_date`.
