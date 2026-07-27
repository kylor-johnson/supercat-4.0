# Fine Art Handcrafted Lighting — Sales Portal Working Session

**Date:** July 23, 2026  
**Org:** Fine Art Handcrafted Lighting (`fal`)  
**Primary contact:** Leonardo Faria (eCommerce & Data Support Manager)  
**Prepared by:** SuperCat Solutions

---

## Purpose of this session

Align on where Sales Portal stands today, clear the remaining file-import blockers, and agree who should see what once the data is live.

**Reference docs (source of truth):**

- [Sales Portal File Specifications](https://supercatsolutions.com/knowledgebase/sales-portal-file-specifications)
- [Sales Information Access](https://supercatsolutions.com/knowledgebase/publish-portal-dashboard) (dashboard / who sees what)
- Sample files:
  - [order_data-sample.csv](https://supercatsolutions.com/assets/images/screenshots/order_data-sample.csv)
  - Invoice sample: `invoice_data-sample.csv` (same KB article)

---

## Current status (live as of July 23, 2026)

| Area | Status | Detail |
|---|---|---|
| eCat iPad catalog | Live | ~6,540 active products; ~6,850 customers |
| Active iPad users (30 days) | Strong | ~36 users logged in |
| SFTP / Power Automate to `/data` | Connected | Files are transmitting |
| `order_data.csv` import | **Blocked** | Failed July 21 and July 23 (see §3) |
| Portal orders loaded | **0** | Nothing landed after failed imports |
| Portal invoice headers loaded | **0** | Full `invoice_data.csv` not successfully loaded |
| Invoice line / tracking fragments | Partial | ~1,470 line rows and ~1,400 tracking rows exist without matching invoice headers — not usable for Portal sales until a complete `invoice_data.csv` loads |
| Sales Portal site / dashboard | Not enabled yet | Portal access and dashboard will be turned on after clean order + invoice imports |

**Bottom line:** Automation of the upload is working. The files themselves still need a few format fixes before Sales Portal can show correct order and invoice data.

---

## 1. What Sales Portal needs (vs eCat iPad)

Sales Portal is the web reporting layer for **ERP order and invoice history**. It is separate from iPad quote / order writing.

| File | Exact name (case-sensitive) | What it powers |
|---|---|---|
| Orders | `order_data.csv` | Open / booked orders, backlog, order list |
| Invoices | `invoice_data.csv` | Invoice list and **sales totals** |
| Tracking (optional) | `invoice_tracking_data.csv` | Shipment tracking links |

Upload location: FTP/SFTP **`/data`** folder (same folder as eCat catalog files).

**Important distinctions for Fine Art:**

| Data | Where it lives | Use it as… |
|---|---|---|
| Invoiced ERP history | Sales Portal (`invoice_data.csv`) | **Sales / revenue** |
| Open ERP orders | Sales Portal (`order_data.csv`) | Backlog / open orders |
| eCat Quotes / Proformas on iPad | eCat iPad | Pipeline / activity — **not** Portal sales |

Fine Art writes a high volume of Quotes and Proformas in eCat. Those are valuable for pipeline visibility on the iPad; they should not be treated as Sales Portal sales totals.

---

## 2. File format rules (must match the KB)

Per the [Sales Portal File Specifications](https://supercatsolutions.com/knowledgebase/sales-portal-file-specifications):

1. **Exact filenames** — `order_data.csv` and `invoice_data.csv` (not `tbl_order_data.csv`, etc.).
2. **Header + lines in one file** — First row of each order/invoice carries header fields + first line item; following rows are additional line items (header columns may be blank or repeated).
3. **Grouped / sorted** — All lines for the same `OrderNumber` (or `InvoiceNumber`) must be contiguous. The importer rejects files when the same order number reappears after a different order has started.
4. **Only known columns** — Extra columns (e.g. ERP-only fields) should be removed; unknown field names generate warnings and can complicate troubleshooting.
5. **Required fields** — See the KB tables. For a successful first load, prioritize:

**`order_data.csv` (required):**  
`LastModifiedAt`, `OrderNumber`, `Complete`, `OrderDate`, `Status`, `OrderOrigin`, `CustomerPONumber`, `CustomerBillToNumber`, `CustomerBillToName`, `TotalAmount`, plus line fields `ItemNumber`, `Description`, `QuantityOrdered`, `QuantityInvoiced`, `UnitPrice`

**`invoice_data.csv` (required):**  
`LastModifiedAt`, `InvoiceNumber`, `InvoiceDate`, `CustomerPONumber`, `CustomerBillToNumber`, `CustomerBillToName`, `NetAmount`, plus line fields `LineNumber`, `ItemNumber`, `Description`, `QuantityOrdered`, `QuantityInvoiced`, `UnitPrice`

6. **`CustomerBillToNumber` must match `customers.csv`** — Territory filtering and customer grouping depend on this match.
7. **Currency** — Fine Art is configured for USD (`Sales portal currency code`).

Use the official samples as the structural template:

- [order_data-sample.csv](https://supercatsolutions.com/assets/images/screenshots/order_data-sample.csv)
- `invoice_data-sample.csv` from the same KB article

---

## 3. Fixes needed on the current Fine Art `order_data.csv`

These are the issues from File Import Status on **July 21** and **July 23**:

| # | Issue | What to do |
|---|---|---|
| 1 | Unknown column `FISCAL_MONTH` | Remove this column from the export |
| 2 | Missing `OrderDate` on many rows | Populate `OrderDate` on every order header row (required) |
| 3 | File not sorted by `OrderNumber` | Sort so all lines for each order are together (e.g. orders 323927 and 323943 were split) |
| 4 | Filename | Confirm Power Automate writes `order_data.csv` (no `tbl_` prefix) |

**Suggested live check:** Re-export a corrected `order_data.csv`, upload to `/data`, then confirm a clean (or warning-only) result in Admin → Tools → Admin Reports → **File Import Status**.

---

## 4. Invoice file — next priority after orders

Sales Portal sales numbers and dashboard charts are driven primarily by **invoice line data** from a complete `invoice_data.csv`.

Current Fine Art state:

- Invoice **headers:** 0  
- Invoice **line rows** present without headers: ~1,470 (~946 invoice numbers)  
- Tracking rows: ~1,400  

That means shipment tracking fragments may have landed, but Portal **cannot** present correct invoice lists or sales totals until a full, correctly sorted `invoice_data.csv` imports cleanly (header + lines together, same rules as the sample).

**Discuss today:**

1. Is a full Aftean `invoice_data.csv` ready (header + lines)?
2. Confirm credit memos use **negative** `NetAmount` / `QuantityInvoiced` where applicable (per KB).
3. Prefer tracking via header `TrackingNumber` + `TrackingCarrier`, or keep `invoice_tracking_data.csv` — see [Shipment Tracking setup](https://supercatsolutions.com/knowledgebase/shipment-tracking-setup).

---

## 5. Who sees what (Sales Information Access)

Per [Sales Information Access](https://supercatsolutions.com/knowledgebase/publish-portal-dashboard):

Two user-group settings control Portal visibility. **Keep them aligned.**

| Setting | Options | Typical use |
|---|---|---|
| **Customer list access** | All / Associated / None | Which customers appear in lists, orders, invoices |
| **Customer sales total access** | Company totals / Associated only | Which sales totals appear on lists and dashboard |

Fine Art’s current eCat groups map cleanly:

| User group | Customer list access (today) | Recommended Portal approach |
|---|---|---|
| **Sales Management** | All customers | All customers + company sales totals; **Enable portal dashboard** |
| **Sales Representatives** | Associated (territory-matched) | Associated customers + associated sales totals; dashboard optional |

**Dashboard note:** “Enable portal dashboard” is **off by default** for security. Management should have it on if they want territory/company summary charts and rankings. Reps often keep it off or associated-only depending on policy.

**Admin users** always see company-wide sales. Limit true Admin accounts to one or two trusted people; use restricted Admin for day-to-day tools when needed.

**Decide in this session:**

1. Who gets Sales Portal login first (management only vs management + reps)?  
2. Confirm Sales Management: All + company totals + dashboard ON.  
3. Confirm Sales Representatives: Associated + associated totals (dashboard Y/N).

---

## 6. What Sales Portal will / will not cover

| Need | Solution |
|---|---|
| Submitted ERP orders & invoices across the team | **Sales Portal** |
| Shipment tracking on invoices | **Sales Portal** (tracking fields or `invoice_tracking_data.csv`) |
| Unsubmitted iPad quotes / drafts across territories | **eCat iPad** → Territory → All Orders & Quotes (shared orders) — not Portal |
| “Latest version only” of revised eCat quotes | Not available as a built-in Portal filter today; revisions remain separate records |

---

## 7. Timing expectations after a clean upload

From the KB:

- Order/invoice **detail lists** update when file processing finishes.
- **Dashboard and customer report totals** wait on the warehouse job (runs ~:20 past the hour; ~30–40 minutes). Allow up to ~1 hour 40 minutes after upload before dashboard numbers refresh.

Optional later: upload `sales_data_sentinel.csv` after order + invoice files to auto-build iPad offline `sales_data.csv` (see KB “Automatic summary sales data file generation”).

---

## 8. Action checklist

### Fine Art

- [ ] Remove `FISCAL_MONTH` (and any other non-spec columns) from `order_data.csv`
- [ ] Populate `OrderDate` on every order
- [ ] Sort `order_data.csv` by `OrderNumber` (all lines for an order contiguous)
- [ ] Confirm Power Automate filenames: `order_data.csv`, `invoice_data.csv`, `invoice_tracking_data.csv`
- [ ] Produce / re-upload a full `invoice_data.csv` matching the [KB + sample](https://supercatsolutions.com/knowledgebase/sales-portal-file-specifications)
- [ ] Confirm `CustomerBillToNumber` values match eCat `customers.csv` bill-to codes
- [ ] Confirm who should receive Portal access and dashboard rights

### SuperCat

- [ ] Watch File Import Status for a clean `order_data.csv` and `invoice_data.csv`
- [ ] Enable Sales Portal access for agreed user groups
- [ ] Enable portal dashboard for Sales Management (and others if requested)
- [ ] Walk a first login: order list, invoice list, customer sales, dashboard
- [ ] Confirm eCat catalog automation can use the same `/data` folder (`customers.csv`, `products.csv`, exact names)

---

## 9. Agenda for today’s call

1. Review File Import Status and the three `order_data.csv` fixes  
2. Confirm corrected re-upload plan (orders first, then invoices)  
3. Agree Portal access + dashboard settings for Management vs Reps  
4. Confirm sales definition: **invoiced ERP data** in Portal vs eCat Quotes/Proformas on iPad  
5. Answer automation of eCat catalog files to `/data`  
6. Set a short follow-up once the first clean import lands

---

*Questions before or after the session: support@supercatsolutions.com · 919.234.7778*
