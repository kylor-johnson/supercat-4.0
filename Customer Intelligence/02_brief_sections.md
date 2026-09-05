# Customer Intelligence Brief — Section Design

> **Status**: Initial design — illustrative data, real data model
> **Date**: 2026-06-15

---

## Brief Structure (Full Data Version)

Assumes the client has all data sources available: `portal_orders`, `portal_order_items`, `portal_invoices`, `portal_invoice_items`, `sales_data`, `inventories`, `commitment_reports`, `placement_reports`, Mixpanel events with `selected_bill_to_code`.

---

### Section 1: Account at a Glance

The 5-second scan. Key numbers and status.

| Field | Source |
|---|---|
| Total business (LTM, all channels) | `portal_orders` SUM(total_amount) |
| eCat orders (LTM) | `orders` SUM(total) WHERE is_submitted AND customer_num |
| eCat penetration % | Derived: eCat GMV / portal_orders GMV |
| Avg order value | `orders` AVG(total) |
| Days since last order | `portal_orders` MAX(order_date) delta |
| YoY change (total business) | `portal_orders` LTM vs. prior 12mo |
| Price level | `customers.default_price_code` |
| Terms | `customers.terms` |
| Territory | `customers.territory_codes` + `territories.name` |
| Ship-to location count | `shipping_locations` COUNT |

---

### Section 2: Purchase DNA

What they buy — product affinity, category mix, top SKUs.

**2a. Category breakdown** (LTM, all channels)
- Source: `portal_invoice_items` → `products.category_code` → `taxonomies.name`
- Show: category name, revenue, % of spend, units, YoY trend

**2b. Top 10 SKUs by revenue**
- Source: `portal_invoice_items` grouped by `item_number`
- Enriched with: `products.long_description`, `inventories.qty_available` + `qty_on_backorder` + `next_scheduled_receipt_date`
- Inventory alert: flag any top-10 item with qty_available = 0

**2c. Collection mix**
- Source: `portal_invoice_items` → `products.collection_code` → `taxonomies.name`

**2d. New introductions adoption**
- Source: `products` WHERE `new_item = true`, cross-ref with this customer's `portal_invoice_items`
- Compare: count of new intros purchased vs. similar-profile customers average
- Surface: top new intros bought by similar customers that this customer hasn't ordered

---

### Section 3: Buying Rhythm

When they buy — frequency, seasonality, velocity, recency.

**3a. Order frequency metrics**
- Source: `portal_orders` grouped by customer
- Metrics: orders/month, avg days between orders, active months (of 12)
- Comparison: vs. org median, percentile rank

**3b. Seasonality pattern**
- Source: `portal_orders.order_date` aggregated by month, 24-month window
- Visualization: monthly bar chart showing seasonal peaks/troughs
- Insight: identify pre-market and post-market buying windows

**3c. Recency & velocity**
- Last order date
- Order velocity trend (QoQ acceleration/deceleration)
- Predicted next order window (based on avg interval)
- Risk level: Low / Watch / At Risk based on interval decay

---

### Section 4: Money Profile

Spend trajectory, price behavior, discount sensitivity.

**4a. Spend trajectory**
- Source: `portal_orders` or `portal_invoices` grouped by quarter
- Show: quarterly revenue trend with QoQ change %

**4b. Price & discount behavior**
- Source: `portal_invoice_items.unit_price`, `orders.discount_percent`
- Metrics: avg unit price, discount %, promo usage %, freight-to-revenue ratio
- Comparison: vs. org averages
- Insight: premium buyer vs. price-sensitive buyer classification

---

### Section 5: Channel Mix

How they order — iPad, online, phone, market, EDI.

- Source: `portal_orders.order_origin` (all channels), `orders.order_source` (eCat breakdown)
- Show: channel, orders, revenue, % of total
- Insight: phone/fax volume = eCat conversion opportunity

---

### Section 6: Rep Engagement Profile

How much attention this account gets from the sales team.

- Source: BigQuery `mixpanel.events` WHERE `selected_bill_to_code = {customer_code}`
- Metrics per event type: customer selections, product searches, configured items, PDF catalogs, document views, orders submitted, order history reviews, SmartPicks used, orders copied
- Engagement score: composite (e.g., sessions with activity / total sessions)
- Comparison: vs. rep's average customer engagement

---

### Section 7: Inventory Alert

Are their favorite items in stock?

- Source: this customer's top items (from `portal_invoice_items`) cross-referenced with `inventories`
- Flag: any top-10 item with `qty_available = 0`
- Include: `next_scheduled_receipt_date` for backordered items
- Suggestion: alternative SKUs in same collection with stock available

---

### Section 8: Cross-Sell Opportunity

What similar customers buy that they don't.

- Source: `portal_invoice_items` grouped by customer cohort (same region via `billing_state`, same spend decile)
- Method: for each category, compare this customer's spend vs. cohort average
- Surface: categories where this customer is below cohort, with $ gap
- Total whitespace estimate: sum of all below-cohort gaps

---

### Section 9: Fulfillment & Returns

Fill rate, backorder rate, return history.

**9a. Fill rate**
- Source: `portal_order_items` (ordered vs. invoiced via `portal_invoice_items`)
- Metrics: line items ordered, invoiced on time, fill rate %, avg backorder days

**9b. Return history**
- Source: `rma_requests` WHERE `bill_to_code = {customer_code}`
- Metrics: returns filed, return $, return rate, top return reasons

---

### Section 10: Market Commitments vs. Actuals

Did they follow through on market commitments?

- Source: `commitment_reports` WHERE `bill_to_code = {customer_code}`, cross-referenced with `portal_order_items`
- Show: per-market committed $ vs. actually ordered $, conversion %
- Breakdown by category: which committed categories converted, which didn't
- Uncommitted items: list with current inventory status

---

### Section 11: Showroom Placements

Current showroom state.

- Source: `placement_reports` WHERE `bill_to_code = {customer_code}`
- Show: location, items placed, last updated
- Flag: stale placements (not updated in 90+ days)
- Flag: placed items that are now discontinued (`products.deleted = true`)

---

### Section 12: Account Health Signal

Composite health assessment.

Derived from multiple signals:
- Spend trajectory direction (accelerating / stable / declining)
- Order frequency stability
- eCat adoption trend
- Reorder velocity (on pace / decaying)
- Product breadth (expanding / contracting)
- Fill rate vs. org average
- Market commitment conversion trend
- Return rate trend

Output: health score (0–100) with signal-level breakdown and pre-meeting priority recommendations.

---

## Conditional Sections

These sections render only when the underlying data is available:

| Section | Condition |
|---|---|
| §5 Channel Mix | `portal_orders.order_origin` populated |
| §6 Rep Engagement | Mixpanel events with `selected_bill_to_code` for this customer |
| §8 Cross-Sell | Sufficient cohort size (10+ similar customers) |
| §10 Market Commitments | `commitment_reports` rows exist for this customer |
| §11 Showroom Placements | `placement_reports` rows exist for this customer |

---

## Minimal Viable Brief (iPad-only client, no ERP sync)

If a client only has `orders` (no `portal_orders`, no `portal_invoice_items`, no `sales_data`):

- §1 Account at a Glance (eCat data only — no total business)
- §2 Purchase DNA (from `orders.order_items` JSON parsing + `products`)
- §3 Buying Rhythm (from `orders.submit_date`)
- §4 Money Profile (from `orders.total`, `orders.discount_*`)
- §6 Rep Engagement (Mixpanel)
- §7 Inventory Alert (if `inventories` present)
- §12 Account Health (subset of signals)

Minimum viable = still useful, just narrower lens (eCat-only, no total-business context).
