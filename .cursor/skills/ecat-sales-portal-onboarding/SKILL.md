---
name: ecat-sales-portal-onboarding
description: >
  Onboard a net-new SuperCat Sales Portal for a client — the historical-sales / account-review
  layer inside eCat Online (NOT the iPad, NOT eCat Online's buyer catalog). Use when building or
  troubleshooting Sales Portal import files (order_data.csv, invoice_data.csv, customers.csv,
  products.csv, territories.csv), setting up Portal access/territories, mapping ERP order/invoice
  history, or diagnosing missing/wrong portal orders/invoices/totals during a build. For reactive
  triage of a live portal issue ("is this a production bug?"), start with ecat-support-triage; for
  evidence rules, fixtures, and the Rails code map, use
  PM/Sales Portal Docs/00-SALES-PORTAL-SYSTEM-SPEC.md.
---
# Sales Portal Onboarding (net-new build)
The Sales Portal is the historical-sales and account-review layer inside eCat Online: reps,
managers, CS, and customer users review customer accounts, orders, invoices, territories, and
reporting periods. It is **not** the iPad app and **not** the eOL buyer catalog. It is only as
complete as the ERP history the client supplies — orders may also arrive via EDI, phone, or
marketplaces, so a portal is not necessarily a full picture of the client's business.

For any live-state question about the org (is Sales Portal provisioned, what actually imported,
which users have portal access), consult supercat-data-routing first, then ecat-postgres-audit.
Provisioning and import state are Postgres; portal/eOL usage and adoption are BigQuery
(google_analytics_ecat_online). Never supercat-cs-tools — it's retired.

> Authoritative reference for anything beyond this build workflow — access edge cases, amount
> contracts, acceptance, fixtures, code map, open decisions — is
> `PM/Sales Portal Docs/00-SALES-PORTAL-SYSTEM-SPEC.md`. This skill is the build playbook; the
> spec wins on conflict and should be updated when the spec is wrong.
>
> KB anchors: [Sales Portal File Specifications](https://supercatsolutions.com/knowledgebase/sales-portal-file-specifications),
> [Sales Information Access](https://supercatsolutions.com/knowledgebase/publish-portal-dashboard),
> [Sales Territories](https://supercatsolutions.com/knowledgebase/sales-territories) (territory file),
> [Shipment Tracking setup](https://supercatsolutions.com/knowledgebase/shipment-tracking-setup).
## 1. File inventory
### Core Portal data (must load for a working Portal)
| File | Role | Notes |
|---|---|---|
| `customers.csv` | Bill-to/ship-to identity + **territory assignments** | **Same file as iPad.** `BillToCode` must match `CustomerBillToNumber` in order/invoice files. **Hard-deletes ALL customers on reimport** — coordinate with iPad go-live. |
| `products.csv` | Product descriptions + taxonomy for product/trade-name/collection panels | **Same file as iPad.** `ItemNumber` or `eCatItemNumber` on sales lines should resolve to `BaseItemCode`. |
| `order_data.csv` | ERP order history — lines, dates, qty, prices, status, customer identity, optional rep | Hierarchical: header + line items in one file. Powers backlog and order lists. |
| `invoice_data.csv` | ERP invoice history — lines, dates, qty, prices, **NetAmount**, customer identity, optional rep | Hierarchical. **Portal sales totals and dashboard invoiced KPIs are driven primarily by invoice line data.** |
These import files are **not** the same as orders created in eCat/iPad — different data path,
different meaning. Do not conflate Sales Portal `order_data.csv` with iPad quote/proforma activity.
### Access setup (required for territory-limited reps — not optional in most builds)
| File | Role | Notes |
|---|---|---|
| `territories.csv` | Territory code → display name lookup | Columns: `Code`, `Name`. **Hard-deletes all territories on reimport.** Codes must align with `TerritoryCodes` on customer bill-to/ship-to rows in `customers.csv` and with user territory assignments in Admin. |
### Optional / adjacent (declare per client in onboarding notes)
| File | Role | Portal? |
|---|---|---|
| `invoice_tracking_data.csv` | Shipment tracking links (`InvoiceNumber`, `Carrier`, `Number`) | Optional Portal enhancement. Hard-deletes all tracking rows on reimport. Import **after** `invoice_data.csv`. Alternative: header `TrackingNumber` + `TrackingCarrier` on invoice rows. |
| `order_header_data.csv` + `order_item_data.csv` | Split-file alternative to combined `order_data.csv` | Same data, different packaging. |
| `invoice_header_data.csv` + `invoice_item_data.csv` | Split-file alternative to combined `invoice_data.csv` | Same data, different packaging. |
| `sales_data_sentinel.csv` | Triggers auto-generation of `sales_data.csv` | **iPad offline summary — NOT Portal sales.** Upload ~1 hour after order+invoice files; warehouse must have processed first. |
| `sales_quotas.csv` | Territory/rep budget targets | Rare (effectively one-org today). Budget chart only where populated. |
| `customer_payment_information.csv` | Stored payment methods for eOL credit-card feature | Not Portal reporting. |
**Do not use for Portal sales totals:** iPad `sales_data.csv`, iPad-submitted orders, eCat quotes/proformas.
## 2. Identity fields that MUST align (most common build failure)
- `CustomerBillToNumber` ↔ `BillToCode` in `customers.csv`.
- `CustomerShipToNumber` ↔ ship-to code on the matching customer row (when ship-to territory access matters).
- `TerritoryCodes` on customer rows ↔ codes in `territories.csv` ↔ territories assigned to users in Admin.
- `OrderNumber` links orders to invoices — supply wherever possible.
- `ItemNumber` / `eCatItemNumber` ↔ `BaseItemCode` in `products.csv` (use `eCatItemNumber` when ERP item codes differ from catalog codes).
- `RepNumber` is an **optional** order/invoice-level access path — NOT the default meaning of customer territory. Only relevant when the managed rep-number feature is enabled (see §5).
If sales facts don't tie to customers or products, check these keys first.
## 3. Import mechanics
### Where files go
- FTP/SFTP **`/data`** (processed files deleted on success), **or**
- Admin Console → **Tools → Import Data**
Portal file types appear in Import Data only when the org has eCat Online Portal enabled.
### Recommended import order
customers.csv (bill-to codes must exist before portal facts reference them) order_data.csv invoice_data.csv invoice_tracking_data.csv (optional; after invoices) territories.csv (after portal data; before validating territory access) sales_data_sentinel.csv (optional; ~1 hr after order+invoice for iPad sales_data only)

`products.csv` follows normal iPad import order (typically before or alongside customers depending on org state).
### Hierarchical file shape
First row of each order/invoice carries header fields **and** the first line item. Continuation rows carry line fields only (header columns blank or repeated — importer uses the first header row seen).
### Format rules (code- and KB-verified)
| Rule | Detail |
|---|---|
| **Exact filenames** | Case-sensitive: `order_data.csv`, `invoice_data.csv` — not `Order_Data.csv`, not `tbl_order_data.csv`. |
| **CSV only** | Importer pipeline expects `.csv`. Convert `.xls`/`.xlsx` before upload — no auto-conversion. |
| **Sort contiguously** | All lines for the same `OrderNumber` (or `InvoiceNumber`) must be grouped. Non-contiguous re-appearance of the same key is a **fatal** import error. |
| **Date-only dates** | `OrderDate`, `InvoiceDate`, etc. must be date-only (`4-16-2026`). Datetime strings like `4-16-2026 12:00:00 AM` are rejected. |
| **`LastModifiedAt`** | Unix epoch integer (typically ms since 1970-01-01 UTC) on the **first row of each order/invoice only** — omit on continuation line rows. Required by KB for incremental import behavior. |
| **No stray columns** | Remove ERP-only columns (e.g. `FISCAL_MONTH`). Allowed custom prefixes: `header_`, `footer_`, `item_`. |
| **Credit memos** | Negative `NetAmount` and negative `QuantityInvoiced` on invoice lines. |
### Required fields for a first successful load (KB minimum)
**`order_data.csv` header:** `LastModifiedAt`, `OrderNumber`, `Complete`, `OrderDate`, `Status`, `OrderOrigin`, `CustomerPONumber`, `CustomerBillToNumber`, `CustomerBillToName`, `TotalAmount`
**`order_data.csv` lines:** `ItemNumber`, `Description`, `QuantityOrdered`, `QuantityInvoiced`, `UnitPrice`
**`invoice_data.csv` header:** `LastModifiedAt`, `InvoiceNumber`, `InvoiceDate`, `CustomerPONumber`, `CustomerBillToNumber`, `CustomerBillToName`, `NetAmount`
**`invoice_data.csv` lines:** `LineNumber`, `ItemNumber`, `Description`, `QuantityOrdered`, `QuantityInvoiced`, `UnitPrice`
Importer severity tiers: missing `OrderNumber`/`OrderDate`/`InvoiceNumber`/`InvoiceDate` → fatal; missing `CustomerBillToNumber`, `TotalAmount`/`NetAmount`, line qty/price fields → warning (imports but Portal incomplete).
### Verify every import
Admin → Tools → Admin Reports → **File Import Status**. Blue timestamp = problems with line numbers.
| Tier | Effect |
|---|---|
| **Fatal** | Whole file rejected |
| **Error** | Good rows import; bad rows skipped |
| **Warning** | Imports including warning rows |
Samples: [order_data-sample.csv](https://supercatsolutions.com/assets/images/screenshots/order_data-sample.csv), invoice sample on same KB page.

To confirm what actually loaded without opening Admin, see §10.
## 4. How much history the client must supply
- For historical order reporting to be meaningful, the client must supply enough historical order data. **If only open orders are supplied, past-order totals and comparisons will be incomplete** — set expectations up front.
- **Invoiced sales / dashboard charts** need a complete `invoice_data.csv` (headers + lines together). Tracking-only fragments without invoice headers do not produce usable Portal sales.
- Backlog is derived, not imported (for orders not excluded by configured status):
  | Data condition | Backlog quantity |
  |---|---|
  | Order present, invoice present | `QuantityOrdered − QuantityInvoiced` |
  | Order absent, invoice present | `0` |
  | Order present, invoice absent | `QuantityOrdered` |
  Backlog value = quantity × applicable unit price. Missing order history distorts backlog.
## 5. Access model — set this up deliberately
Access to customer records (for order-taking) and access to sales totals are related but not identical.
### Admin setup checklist (before user validation)
1. Org has **eCat Online Portal** enabled.
2. Company Settings → **Sales portal currency code** matches exported amounts (e.g. `USD`).
3. `customers.csv` loaded with correct `TerritoryCodes` on bill-to and ship-to rows.
4. `territories.csv` loaded.
5. User types / groups configured per [Sales Information Access](https://supercatsolutions.com/knowledgebase/publish-portal-dashboard):
   - **Customer list access:** All / Associated / None
   - **Customer sales total access:** Company totals / Associated only
   - **Enable portal dashboard** (off by default — turn on for management if they need summary charts)
   - **`display_sales_portal_totals`** must be on for Portal sales to show
6. Assign territories to each rep user in Admin.
7. Keep **true Admin accounts** to one or two people — admins bypass territory checks and are invalid proof that restricted reps are set up correctly.
### Three user shapes
- **Company-wide user** — sees all Sales Portal data via user-group all-customer sales totals or admin. **Admin sessions are not valid proof of restricted-rep setup** — always verify with a real non-admin.
- **Customer user** — valid customer number; sees only that account's orders/invoices.
- **Territory-limited user** — non-admin without all-customer totals: sees **nothing** if no territories assigned; otherwise sees customers/sales tied to assigned bill-to and ship-to territories; may also see records via order/invoice `RepNumber` only if that feature is enabled.
Bill-to / ship-to intent (preserve current production behavior; do not "fix" without Kylor):
1. User territory matches customer/bill-to territory → access to the customer and everything on it.
2. User territory matches a ship-to but not the bill-to → access to the customer to reach that ship-to; sales access follows the ship-to path.
3. Neither matches → no access to that customer.
## 6. Warehouse delay — bake into go-live expectations
Territory-limited and customer-user access runs through **warehouse projections**, not live settings.
| What updates | When |
|---|---|
| Order/invoice **detail lists** | After file import processing completes |
| **Dashboard + customer report totals** | After hourly warehouse job (~:20 past the hour; ~30–40 min runtime). Allow up to **~1 hour 40 minutes** after upload. |
When validating a new portal, record the relevant warehouse timestamp; do not assume a setting you just changed has propagated. Company-wide users bypass territory restriction in queries and see changes faster for access scope — but dashboard totals still wait on warehouse for aggregates.
## 7. Amounts: expect two classes, and that they can differ
The portal intentionally holds:
1. **Imported header values** — order `TotalAmount` (row display), invoice `NetAmount` (row display; **the client-facing invoiced total**, negative for credit memos).
2. **Warehouse-calculated totals** — line qty × unit price and aggregates (CY sales, dashboard invoiced KPI, most customer totals).
**These can differ, and a difference is not automatically a defect.** Do not raise a "totals are wrong" bug during onboarding without checking which class you're comparing. Several amount questions (invoice header total source, freight/surcharge/credit handling) are open product decisions — see spec §6.3.
Also: Dashboard Top Customers / Top Products use **ordered** amounts; invoiced KPI uses **invoiced** amounts — panels may not reconcile by design.
## 8. Build gotchas (from real builds + verified importer behavior)
- **iPad quotes/proformas ≠ Portal sales** — high quote volume in eCat is pipeline on iPad, not invoiced ERP history in Portal.
- **Invoice file without headers** — line/tracking fragments without matching invoice headers produce no usable Portal sales until a full hierarchical `invoice_data.csv` loads cleanly.
- **Customer reimport during Portal build** — `customers.csv` hard-deletes all customers; schedule carefully if iPad is already live.
- **ERP export sort** — sort by `OrderNumber` / `InvoiceNumber` before export; ERPs that log revisions as scattered rows will fail the contiguous-block rule.
- **Ship-to population** — some clients export bill-to only; ship-to-only territory access needs ship-to codes on order/invoice rows and customer file.
- **`OrderOrigin` often blank** — channel filtering shows "Unknown" unless the client populates it; not a Portal bug.
## 9. What Portal will / will not cover (set client expectations)
| Need | Where |
|---|---|
| ERP orders, invoices, sales totals, backlog | **Sales Portal** |
| Shipment tracking | Portal invoice fields or `invoice_tracking_data.csv` |
| Unsubmitted iPad quotes across territories | **eCat iPad** → shared orders/quotes — not Portal |
| Offline rep sales summary on iPad | `sales_data.csv` (manual or via `sales_data_sentinel.csv`) — not Portal |
## 10. Read-only MCP HTTP API (fast first look)

A read-only JSON API in `supercat_server` complements `supercat-postgres-vpn` — same underlying
data, quicker for a first pass. **The org shortname sits between `/api/v1/` and `mcp`**
(`config/routes.rb:652,654,710-762`): `/api/v1/<shortname>/mcp/...`.

| Endpoint | Use |
|---|---|
| `GET /api/v1/<shortname>/mcp/organizations/data/import_events.json` | Whether `Order_Data.csv` / `Invoice_Data.csv` actually loaded — same source as Admin → File Import Status. |
| `GET /api/v1/<shortname>/mcp/organizations/data/orders.json` | Loaded order rows. |
| `GET /api/v1/<shortname>/mcp/organizations/data/summary.json` | Data summary / counts. |
| `GET /api/v1/<shortname>/mcp/organizations/data/customers.json` | Loaded customer rows. |
| `GET /api/v1/<shortname>/mcp/organizations/territories.json` | Territory codes/names. |
| `GET /api/v1/<shortname>/mcp/organizations/customers/hierarchy.json` | Bill-to / ship-to hierarchy. |
| `GET /api/v1/<shortname>/mcp/organizations/health.json` (also `health_csv`) | Six-category onboarding scorecard. |

**Auth (verified in code) — admin-only.** `verify_mcp_access` requires `is_admin?` on the user
or org-user and returns `403` otherwise (`api/v1/mcp/base_controller.rb:12,18-30`).
`AdminController#authenticate` tries three methods in order (`admin_controller.rb:6-14`):

1. **Existing session cookie** — why a browser-logged-in request may succeed with no headers.
2. **`X-CLIENT-ID` + `X-API-KEY` headers** — the shortname in the URL must match the
   client-id's org or auth is discarded (`admin_controller.rb:53-65`).
3. **HTTP Basic** — the practical choice for curl (`admin_controller.rb:21-25`).

Two hard requirements: **HTTPS only** (`prepend_before_action :require_https`) and the
**`.json` extension is mandatory** — `api_call?` only treats plist/json/csv as API requests
(`admin_controller.rb:16-19`), so without it you get redirected to the login page and see HTML
instead of an auth challenge.

```bash
curl -s "https://<host>/api/v1/<shortname>/mcp/organizations/data/import_events.json" \
  -u 'USER:PASS'
```

This is a faster first look, **not** a replacement for `supercat-postgres-vpn` on deeper questions.
## When to hand off to reactive triage
If the question is "is this a production bug," involves evidence rules (`PROD-REPRO`/`CODE-RISK`/etc.), canonical fixtures (`wwjc/betaverify`), the acceptance verification matrix, or the Rails code map — that's `ecat-support-triage` for the triage loop (identify the org, ground live state, diagnose, draft a reply, never auto-send — and Jira stays read-only), grounded in `PM/Sales Portal Docs/00-SALES-PORTAL-SYSTEM-SPEC.md` for evidence rules, fixtures, and the Rails code map. This skill stops at building and standing up a new portal.
