# Customer Intelligence — Data Gap Analysis

> **Status**: Verified against live production 2026-06-15
> **Method**: Direct queries against Postgres MCP and BigQuery MCP

---

## Summary

| Original Claimed Gap | Verdict | Evidence |
|---|---|---|
| Time-series product data per customer (need `invoice_date` on `sales_data`) | **CLOSED — data exists** | `portal_invoices` (4.6M rows) + `portal_invoice_items` (13.7M rows) with real `invoice_date`. Also `portal_orders` + `portal_order_items` with `order_date`. Two separate dated sources, no engineering needed. |
| Customer-level behavioral data in Mixpanel | **CLOSED — data exists** | `selected_bill_to_code` present on 50.8% of 9.8M Mixpanel events (4.97M events, 126K distinct customers). Events include: product_search (2M), customer_selection (273K), order_submitted (208K), view_document (151K), add_configured_item (125K), pdf_catalog_generated (37K). |
| iPad order line items unparseable | **CLOSED — parseable** | `orders.order_items` is a well-structured JSON array with `item_number`, `quantity`, `item_price`, `extended_price`, `options`, `tags`. Queryable via Postgres `json_array_elements()`. |
| End-customer web portal browsing data | **CONFIRMED — real gap** | Clicky visitor tables have IP/session/geo but zero customer identity. GA is aggregate. No `bill_to_code`, `customer_id`, or business identity field. Would require instrumenting the portal login flow. |
| Customer satisfaction / NPS | **CONFIRMED — real gap** | No survey or satisfaction data anywhere. `rma_requests` return rate is the closest proxy. |
| Customer firmographic enrichment | **CONFIRMED — real gap** | No industry, company size, or years-as-customer beyond what's derivable from order history. Would require external data enrichment. |
| Cross-org customer deduplication | **CONFIRMED — real gap** | A dealer buying from multiple client orgs appears as separate `bill_to_code` values. No unified customer ID. Not needed for single-client briefs. |

---

## Detailed Verification Results

### Gap 1: Time-series product velocity per customer — CLOSED

`portal_invoices` schema confirmed:
- `invoice_date` (date type) — real dates verified (sample: 2022-01-04)
- `customer_bill_to_number` (varchar) — customer attribution
- `invoice_number` (varchar) — join key to line items
- `total_amount`, `freight_amount`, `tax_amount` — financial detail
- 43 columns total

`portal_invoice_items` schema confirmed:
- `item_number` (varchar) — product attribution
- `quantity_invoiced`, `quantity_returned` (numeric) — fulfillment detail
- `unit_price` (numeric) — price per item
- `invoice_number` + `organization_id` — join to invoice header

This means: for any customer, we can compute product-level spend by month/quarter/year using `portal_invoices.invoice_date` + `portal_invoice_items.item_number` + `portal_invoice_items.unit_price * quantity_invoiced`. The VM-38b blocker (`invoice_date` on `sales_data`) is irrelevant for the customer brief.

### Gap 2: Customer-level behavioral data — CLOSED

BigQuery `mixpanel.events` has `selected_bill_to_code` and `selected_ship_to_code` as top-level columns. When a rep selects a customer in the iPad app, all subsequent events carry that customer's code.

Top events with customer attribution:
- `product_search`: 1,987,536 events with bill-to
- `customer_search`: 544,886
- `customer_selection`: 272,784
- `order_submitted`: 207,702
- `view_document`: 150,521
- `view_kit`: 144,731
- `add_configured_item_to_order`: 124,587
- `pdf_catalog_generated`: 36,926

The actor is the rep, but we know which customer context they were in. This enables: "Customer X was worked on 67 times by reps, had 142 product searches, 21 orders submitted, 6 PDF catalogs generated."

### Gap 3: iPad order line items — CLOSED

`orders.order_items` is a text column containing a well-structured JSON array:

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

Queryable via Postgres JSON functions (`json_array_elements`, `json_extract_path_text`). Not normalized but workable without schema changes.

Additional: `cart_items` table exists for in-progress carts (normalized: `item_number`, `quantity`, `options`, `org_user_id`). For ERP-imported orders, `portal_order_items` is fully normalized.

### Gap 4: End-customer web browsing — CONFIRMED (real gap)

Clicky `*_visitors` tables have:
- `ip_address`, `session_id`, `geolocation`, `web_browser`, `referrer_url`, `campaign`, `actions`, `time_total_seconds`
- `organization` field = ISP/network name (e.g., "Icloud Private Relay"), NOT a SuperCat customer
- `custom_data` = empty `{}` in all sampled rows

No `bill_to_code`, `customer_id`, `username`, or any business identity field. Cannot tie portal browsing to a specific dealer/buyer.

To close: instrument the portal login flow to pass customer identity into analytics custom_data, or switch to an analytics tool that captures authenticated user IDs.

**Impact on brief**: Minimal. Transactional data (portal invoices/orders) + rep-mediated Mixpanel events provide comprehensive customer intelligence. The missing piece is "what did the buyer browse on the portal" — valuable but not essential for the first version.

---

## Tables Verified During Gap Analysis

Additional customer-related tables confirmed in Postgres:

| Table | Purpose |
|---|---|
| `customers` | Master customer records |
| `customer_favorites` | Aggregated purchase history per product (4.67M rows) |
| `customer_custom_fields` | Custom field definitions per org |
| `customer_payment_informations` | Payment info |
| `customer_product_totals_by_invoice` | Lifetime product totals from invoices (no date dimension) |
| `customer_product_totals_by_order` | Lifetime product totals from orders (no date dimension) |
| `authenticated_sessions` | Auth tokens only (not useful for intelligence) |
| `login_events` | iPad login audit (rep logins, not customer logins) |

No `buyer%` tables exist. No `%browse%`, `%view%`, `%click%`, `%visit%`, `%page%`, or `%analytics%` tables exist (beyond shipment tracking).
