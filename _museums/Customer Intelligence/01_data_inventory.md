# Customer Intelligence — Data Inventory

> **Status**: Verified against live production databases 2026-06-15
> **Sources verified**: Postgres MCP (`user-supercat-postgres-vpn`), BigQuery (`user-bigquery-admin`)

---

## Postgres — Customer-Level Data Sources

### Primary Tables

| Table | Rows (platform) | Key Customer Column | What It Provides |
|---|---|---|---|
| `customers` | 836K | `code` | Master record: name, billing address, territory, price level, terms, custom fields |
| `orders` | 1.6M+ | `customer_num` | iPad-submitted eCat orders: total, date, rep, channel, order type, line items (JSON) |
| `portal_orders` | 3.6M | `customer_bill_to_number` | ERP-imported all-channel orders: total, date, channel origin, rep, buyer name |
| `portal_order_items` | 11.7M | via `order_number` join | Normalized line items: item, qty ordered/invoiced/backordered, unit price, warehouse |
| `portal_invoices` | 4.6M | `customer_bill_to_number` | Invoice headers: invoice date, total, freight, tax, tracking, ship-via |
| `portal_invoice_items` | 13.7M | via `invoice_number` join | Invoice line items: item, qty invoiced/returned, unit price — **has invoice_date via join** |
| `sales_data` | varies | `bill_to_code` | Pre-aggregated ERP sales: item, qty invoiced, amount invoiced, qty on order |
| `inventories` | varies | `base_item_code` | Current stock: qty available, on hand, on backorder, next receipt date |
| `products` | varies | `item_number` | Catalog: category, collection, trade name, new_item flag, price, description |

### Pre-Aggregated Tables

| Table | Rows | What It Provides |
|---|---|---|
| `customer_product_totals_by_invoice` | 3.7M | Lifetime invoiced total per customer × product (no date dimension) |
| `customer_product_totals_by_order` | 2.8M | Lifetime ordered total per customer × product (no date dimension) |

### Supplementary Tables

| Table | Rows | What It Provides |
|---|---|---|
| `customer_favorites` | 4.7M | Items the customer has purchased repeatedly — purchase history by product |
| `rma_requests` | 10.6K | Returns: customer, item, quantity, reason code |
| `commitment_reports` | 27K+ | Market commitments: customer, items (text), market code |
| `placement_reports` | 27K+ | Showroom placements: customer, items, showroom location |
| `shipping_locations` | varies | Ship-to addresses per customer (1:many via customer_id) |
| `customer_payment_informations` | varies | Stored payment methods |
| `taxonomies` | varies | Category/collection/trade name lookup (join via products) |

### Key Join Paths

```
customers.code ←→ orders.customer_num
customers.code ←→ portal_orders.customer_bill_to_number
customers.code ←→ sales_data.bill_to_code
customers.code ←→ customer_product_totals_by_*.customer_bill_to_number
customers.code ←→ rma_requests.bill_to_code
customers.code ←→ commitment_reports.bill_to_code
customers.code ←→ placement_reports.bill_to_code
customers.code ←→ customer_favorites.bill_to_code
customers.id   ←→ shipping_locations.customer_id

portal_orders.order_number   ←→ portal_order_items.order_number
portal_invoices.invoice_number ←→ portal_invoice_items.invoice_number
portal_order_items.item_number ←→ products.item_number
products.category_code       ←→ taxonomies.code (type='Category')
products.collection_code     ←→ taxonomies.code (type='Collection')

All joins scoped by organization_id.
```

### iPad Order Line Items

`orders.order_items` is a `text` column containing a well-structured JSON array. Each element:

```json
{
  "item_number": "AS41G",
  "item_price": 465.0,
  "quantity": 2,
  "extended_price": 930.0,
  "item_description": "CopperSmith Adam Street 41\" Tall Gas Lantern...",
  "options": [],
  "tags": {},
  "is_promo_price": false,
  "calculated_has_discount": false,
  "line_notes": null
}
```

Parseable via Postgres `json_array_elements()`. Not normalized, but workable.

---

## BigQuery — Customer-Level Data Sources

### Mixpanel Events (customer-attributed)

`selected_bill_to_code` is a top-level column on `mixpanel.events`. Present on **50.8% of 9.8M total events** (4.97M events attributed to 126,753 distinct customers).

| Event | Count with bill-to | Intelligence Value |
|---|---:|---|
| `product_search` | 1,987,536 | What products reps search for in this customer's context |
| `customer_search` | 544,886 | How often this customer is looked up |
| `customer_selection` | 272,784 | How often reps open this customer's profile |
| `order_submitted` | 207,702 | eCat order submissions with total, item count, price level |
| `view_document` | 150,521 | Library/document views while working on this customer |
| `view_kit` | 144,731 | Kit/bundle views in customer context |
| `add_configured_item_to_order` | 124,587 | Configured products built for this customer |
| `add_kit_to_order` | 115,506 | Kit purchases for this customer |
| `view_customer_orders` | 99,000+ | Reps reviewing this customer's order history |
| `pdf_catalog_generated` | 36,926 | Tailored catalogs created for this customer |
| `copy_order` | 17,000+ | Repeat/reorder behavior |
| `view_customer_placements` | 10,000+ | Showroom placement reviews |
| `view_customer_smart_picks` | 7,000+ | Algorithmic recommendations viewed |

Key columns: `selected_bill_to_code`, `selected_ship_to_code`, `current_organization_shortname`, `username` (rep).

**Note**: The *actor* is the rep, not the end-customer. We know which customer context the rep was working in. This is "how much attention does this account get from your team" — not "what does the buyer browse."

---

## Confirmed Data Gaps

| Gap | Status | Impact on Brief |
|---|---|---|
| End-customer web portal browsing | **Confirmed gap** — Clicky/GA have no customer identity | Cannot say "this buyer browsed X products on your portal." Brief doesn't suffer — transactional + rep-engagement data is sufficient. |
| Customer satisfaction / NPS | **Confirmed gap** — no survey data | Cannot include satisfaction score. Return rate from `rma_requests` is the closest proxy. |
| Customer firmographic enrichment | **Confirmed gap** — no industry, company size, years-as-customer beyond order history | Can derive relationship length from first-order date. Size/industry would require external enrichment. |
| Cross-org customer dedup | **Confirmed gap** — a dealer buying from multiple client orgs appears as separate records | Not needed for single-client briefs. Would matter for platform-wide dealer intelligence (future). |

---

## What We Can Derive Per Customer

| Dimension | Derivable? | Source Tables |
|---|---|---|
| What they buy (products, categories, collections) | **Yes** | `portal_order_items` / `portal_invoice_items` + `products` + `taxonomies` |
| When they buy (frequency, seasonality, recency) | **Yes** | `orders.submit_date`, `portal_orders.order_date` |
| How much they spend (LTV, AOV, trend) | **Yes** | `orders.total`, `portal_orders.total_amount`, `portal_invoices.total_amount` |
| How they buy (channel mix) | **Yes** | `orders.order_source`, `portal_orders.order_origin` |
| Who they buy through (rep relationship) | **Yes** | `orders.rep_*`, `portal_orders.rep_name` |
| Where they ship (geography, multi-location) | **Yes** | `customers.billing_*`, `shipping_locations.*` |
| Their inventory status (top items in stock?) | **Yes** | `inventories` joined to their top items |
| Returns / quality issues | **Yes** | `rma_requests` |
| Market commitments vs. actuals | **Yes** | `commitment_reports` + `portal_order_items` |
| Showroom placement status | **Yes** | `placement_reports` + `products.deleted` |
| eCat penetration (eCat share of total business) | **Yes** | `orders` vs. `portal_orders` |
| Rep engagement level | **Yes** | BigQuery `mixpanel.events` by `selected_bill_to_code` |
| Price/discount behavior | **Yes** | `portal_invoice_items.unit_price`, `orders.discount_*` |
| Fulfillment / fill rate | **Yes** | `portal_order_items` (ordered vs. invoiced vs. backordered) |
| Product velocity trends | **Yes** | `portal_invoice_items` + `portal_invoices.invoice_date` |
| Buyer-within-customer (multiple purchasers) | **Yes** | `portal_orders.buyer_name` |
