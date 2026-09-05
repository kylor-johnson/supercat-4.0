# Sales Portal system specification

**Status:** Canonical working specification  
**Version:** 1.0  
**Date:** 2026-08-04  
**Product owner:** Kylor Johnson  
**Engineering reader:** Brent Sanders  
**Applies to:** eCat Online Sales Portal only  
**Does not apply to:** eCat iPad order-taking behavior, generic eCat Online catalog behavior, Insightful reports, or Admin Console behavior unless explicitly named

## 1. Purpose

This document gives product, engineering, support, and future agents one shared understanding of the Sales Portal before they inspect Jira, propose a bet, change a ticket, or interpret production behavior.

The Sales Portal has grown incrementally. Its behavior is spread across old design documents, client-facing calculation documentation, Rails code, warehouse ETL, settings, Jira history, and production data. Those sources sometimes conflict. This specification records:

- the product and customer mental model;
- the current implementation where verified;
- production evidence where available;
- decisions that remain open;
- the verification protocol required before engineering work.

This is not permission to change Jira, Confluence, production data, users, settings, or code.

## 2. Authority and evidence rules

No single historical source is automatically correct.

### 2.1 Authority order

Use this order when determining current truth:

1. **Explicit current product decision** approved by Kylor.
2. **Valid production behavior** observed with the correct user role and fixture.
3. **Current deployed code**, when the deployed revision is known.
4. **Current repository source**, clearly labeled if it differs from production.
5. **Canonical product documentation**, interpreted as intended behavior rather than proof of implementation.
6. **Read-only production SQL**, interpreted as a baseline rather than proof of UI behavior.
7. **Jira and Confluence**, which may be stale or contradictory.
8. **Local PM history**, which is evidence of prior reasoning, not current authority.

### 2.2 Evidence labels

Every material claim must carry one of these labels:

| Label | Meaning |
|---|---|
| `PROD-REPRO` | Valid user reproduced a defect in production |
| `PROD-PASS` | Valid user completed the named acceptance route successfully |
| `SQL-BASELINE` | Read-only SQL establishes expected records or amounts |
| `CODE-IMPLICATION` | Behavior follows directly from current inspected source |
| `CODE-RISK` | Source suggests a problem, but data/configuration or deployed behavior is unverified |
| `DOC-INTENT` | Product documentation describes intended behavior |
| `STALE` | Claim was once used but is no longer current |
| `INVALID` | Evidence used the wrong role, fixture, data, or product surface |
| `OPEN-DECISION` | Product meaning has not been settled |
| `PROCESS` | Finding concerns planning or evidence control, not product behavior |

Do not call a ticket a production bug based only on `CODE-RISK`, SQL, an admin account, or old documentation.

## 3. What the Sales Portal is

The Sales Portal is the historical-sales and account-review layer inside eCat Online.

Its users are primarily:

- sales representatives reviewing their customer/territory book;
- sales managers reviewing company or territory performance;
- customer-service representatives researching customer, order, and invoice history;
- customer users reviewing their own account history;
- internal/admin users when support or company-wide access is required.

The Sales Portal is not a generic BI builder. Users work in recognizable business objects:

- customer accounts;
- ship-to locations;
- orders;
- invoices;
- territories;
- selected reporting periods.

SuperCat clients are B2B furniture, lighting, and home-décor manufacturers and wholesalers. Their customers are typically stocking dealers, interior designers, contract buyers, distributors, marketplaces, and other trade accounts—not end consumers.

The Sales Portal is also not necessarily a complete view of a manufacturer's whole business unless the client supplies complete ERP history. Orders may also arrive through EDI, phone, marketplaces, customer service, or other channels.

## 4. Product surfaces

### 4.1 Customers

Customers is account-first.

Users use it to:

- locate an account;
- review account sales and backlog;
- compare standing current/prior-year values;
- inspect another selected period;
- export the same customer result for work in Excel or another operational workflow.

Search, sorting, and filters primarily determine which customers are in the result set. The totals at the top summarize the complete matching result set across all pages, not just the visible page.

Changing the date range changes the sales values shown. It does not normally remove customers merely because they had no sales in that period.

### 4.2 Customer detail

Customer detail provides:

- open-order and recent-invoice snapshots;
- links to more orders and invoices for that customer;
- purchased products;
- registered customer users where applicable.

Customer identity and access must survive links into Orders and Invoices.

### 4.3 Orders

Orders is order-first.

Filtering determines which orders appear:

- order date;
- customer;
- territory;
- status;
- complete/open state;
- search terms such as order number, PO, customer, or item.

The displayed order total comes from imported order data. Related invoice amounts may use imported invoice data. Warehouse-based aggregate calculations can differ from displayed imported totals.

### 4.4 Invoices

Invoices is invoice-first.

Filtering determines which invoices appear:

- invoice date;
- customer;
- territory;
- order/customer/item search.

The invoice row amount comes from imported invoice `NetAmount`. The total at the top is currently line-derived through warehouse sales facts. Freight, surcharges, discounts, missing lines, and other data differences can make those values differ.

Do not promise that row amounts will always sum exactly to the header without first deciding the amount contract.

### 4.5 Dashboard

Dashboard is a summary surface, not a promise that every panel uses one measure.

Verified/current measures include:

- invoiced KPI and invoice graph: line-derived invoiced amount;
- Top Customers and Top Products: ordered amount;
- Top Territories: invoiced amount;
- backlog: order and invoice line-derived calculation.

Top Customers and Top Products therefore do not necessarily reconcile to the invoice KPI. That can be intentional.

Current unresolved Dashboard areas:

- Top Customer membership under a selected territory;
- Top Product scope under a selected territory;
- drill-through parameter persistence;
- Top Territory attribution when invoice `RepNumber` access is enabled;
- direct access to Dashboard sub-actions when the Dashboard-specific gate is off.

## 5. Source data and warehouse flow

### 5.1 Primary imports

| File | Role in Sales Portal |
|---|---|
| `customers.csv` | Customer/bill-to identity, ship-tos, territory assignments, customer names and addresses |
| `order_data.csv` | Historical/imported orders, lines, dates, quantities, prices, status, customer identity, optional rep number |
| `invoice_data.csv` | Historical/imported invoices, lines, dates, quantities, prices, net amount, customer identity, optional rep number |
| `products.csv` | Product descriptions and taxonomy used by product/tradename/collection panels |

These import files are not the same as orders created in eCat/iPad.

### 5.2 Important identity fields

- `CustomerBillToNumber` must align to the customer code.
- `CustomerShipToNumber` identifies the applicable shipping location.
- `OrderNumber` links orders and invoices where supplied.
- `ItemNumber`/`eCatItemNumber` connects sales facts to products.
- `RepNumber` is an optional invoice/order-level access path, not the default meaning of customer territory.

### 5.3 Warehouse delay

Territory-limited and customer-user access uses warehouse projections.

Changes to:

- user territories;
- customer territories;
- ship-to territories;
- imported orders/invoices;

do not necessarily appear immediately. Historical documentation cites one to three hours depending on process and period. Acceptance must record the relevant warehouse timestamp rather than assume a live setting has propagated.

Users with company-wide sales access can bypass territory restriction immediately because the query restriction is removed.

## 6. Amount and calculation contracts

### 6.1 Two classes of amounts

The Sales Portal intentionally contains:

1. **Individual imported values**
   - order `TotalAmount`;
   - invoice `NetAmount`;
   - other header values supplied by the client.

2. **Warehouse-calculated totals**
   - line quantity multiplied by unit price;
   - invoice, order, backlog, customer, and Dashboard aggregates.

These can differ. A difference is not automatically a defect.

### 6.2 Backlog

For orders not excluded by configured statuses:

| Data condition | Backlog quantity |
|---|---|
| Order present, invoice present | `QuantityOrdered - QuantityInvoiced` |
| Order absent, invoice present | `0` |
| Order present, invoice absent | `QuantityOrdered` |

Backlog value is quantity multiplied by the applicable unit price.

The client must supply enough historical order data for historical order reporting. If only open orders are supplied, past order totals and comparisons will be incomplete.

### 6.3 Current unresolved amount decisions

Do not change these without a dedicated product decision:

- whether Invoice header total should use imported `NetAmount` or line-derived invoiced amount;
- how freight, surcharges, and credits should be explained;
- whether Customers production totals currently and intentionally use the documented warehouse line calculation everywhere;
- whether Dashboard panels require clearer measure labels.

## 7. Sales Portal access model

Access to customer records for order taking and access to sales totals are related but not identical.

### 7.1 Company-wide user

A user can see company-wide Sales Portal data when:

- their user group grants all-customer sales totals; or
- admin behavior grants unrestricted permission.

Admins bypass most `UserTypePermissions` checks. Admin sessions are invalid evidence for restricted-rep acceptance.

### 7.2 Customer user

A user with a valid customer number sees orders and invoices belonging to that customer account.

### 7.3 Territory-limited user

A non-admin user without all-customer totals:

- sees no Sales Portal customer/order/invoice data if no territories are assigned;
- sees customer and sales data connected to their assigned bill-to and ship-to territories;
- may also see records tied through invoice/order `RepNumber` only when the managed feature is enabled.

### 7.4 Bill-to and ship-to behavior

Documented product intent:

1. User territory matches customer/bill-to territory:
   - user has access to the customer and everything associated with that customer.

2. User territory matches a ship-to but not the bill-to:
   - user has access to the customer so they can reach that ship-to;
   - sales access should follow the applicable ship-to path.

3. Neither bill-to nor ship-to matches:
   - user has no access to that customer.

This conflicts with a later Bet A comment saying territory merely selects customer accounts and every row shows the account's full sales. That later statement is not canonical. Preserve current production behavior until Kylor explicitly resolves the conflict.

### 7.5 `RepNumber`

`RepNumber` is a separate access mechanism.

- It can directly associate an order/invoice with a territory when the feature is enabled.
- It must not silently redefine normal customer/ship-to territory.
- Comma-separated rep numbers are not reliably represented by the current scalar warehouse model.
- EBR-180/SERV-2178 covers that separate, large implementation class.

### 7.6 Current authorization risks

Current `origin/master` source still suggests:

- Dashboard sub-actions may not enforce the stricter Dashboard-specific gate;
- Invoice show may resolve within the organization without checking the user's territory book;
- invoice email uses a global invoice id lookup;
- Customer detail may allow any non-customer user with a blank customer number.

These are `CODE-IMPLICATION`/`CODE-RISK` until production is tested with a legitimate non-admin session.

## 8. Territory warehouse model

The warehouse represents many-to-many territory relationships through:

- territory dimension;
- rep-to-territory bridge;
- territory-to-customer bridge;
- territory-to-ship-to bridge.

The permission book is resolved before user-selected narrowing on current Orders/Invoices service paths. A selected territory should intersect the permitted book, not widen it.

### Known risks

- shipping-location territory codes are downcased for enumeration but raw-cased in one bridge map;
- blank ship-to keys can collapse to the customer key;
- old raw SQL and newer service-object predicates can differ;
- territory changes wait for ETL;
- direct invoice/order `RepNumber` access and master-data territory have different semantics.

Each needs its own evidence and, if necessary, its own repair. They are not one “territory resolver” bet.

## 9. Customer-page behavior contract

### 9.1 Search

- Search is case-insensitive.
- Search acts on customer/account identity.
- Search terms separated by commas are treated as separate required terms in the historical design.
- A recognized US state code receives special treatment.
- Search changes which customer accounts appear.
- Top totals summarize sales for all matching customers, not only the visible page.
- Per-customer account sales are not recomputed merely because of free-text search.

Historical search behavior contains old TODOs. Do not expand search behavior inside an unrelated reporting fix.

### 9.2 Date ranges

Standing columns:

- Current YTD/current-year sales;
- Previous Year/last-year sales;
- backlog.

Historical design says Current YTD and Previous Year are already represented by standing columns. Other selected ranges add a selected-period value at the top and per customer.

Current reproduced defect:

- Previous Month is correctly calculated/exported but hidden on the page.
- Previous YTD renders the selected-period value.
- the accidental Ruby substring test permits only `previous_ytd` and `custom`.

Fix the display rule without adding duplicate standing columns or changing the revenue definition.

### 9.3 Territory

Territory is not merely a UI filter. It is an access and business-book constraint.

The selected territory must not expose data outside the user's permitted book. Row calculations must preserve the documented bill-to/ship-to semantics until a product decision supersedes them.

### 9.4 Sorting

- Sorting must not change result-set membership.
- Customer sort is alphabetic.
- Sales-value sorts are numeric and normally descending.
- NULL values should behave as zero where historically specified.

## 10. Orders and Invoices behavior contract

### 10.1 Date filtering

- Orders filter on order date.
- Invoices filter on invoice date.
- Current YTD is the normal default.

### 10.2 Territory filtering

- Bill-to match includes the applicable customer book.
- Ship-to match includes records associated with matching ship-tos.
- Optional rep-number access is separate and feature-gated.

### 10.3 Search

Search narrows the order/invoice records by fields such as:

- order/invoice number;
- PO number;
- customer name/number;
- item number.

### 10.4 Linked context

Links between pages must preserve the reason the user arrived:

- Customer → More Orders/Invoices preserves the customer number.
- Order → Invoices preserves the order number.
- Dashboard → Orders/Invoices should preserve the applicable period and user-selected filters where the destination supports them.

Do not demand parameter propagation merely because it sounds consistent. Confirm the source page's intended behavior and whether the destination can represent that filter.

## 11. Dashboard behavior contract

### 11.1 Visibility

Dashboard visibility for non-customer users requires:

- the Sales Portal/customer surface to be available;
- the organization/feature Dashboard gate;
- user type `enable_portal_dashboard`;
- user type `display_sales_portal_totals`.

Admin Console `view_dashboard` is not the Sales Portal Dashboard gate.

### 11.2 Period behavior

Dashboard panels do not all have one universal period/comparison behavior.

Historical behavior includes:

- Current YTD graph can show current-year and prior-year context;
- Current Month compares with the same prior-year month;
- Previous Month compares with the prior-year equivalent;
- Yesterday can suppress the graph;
- Custom displays the requested range without an automatic comparison.

Where historical documentation says TBD, source and production must be inspected before writing acceptance criteria.

### 11.3 Drill-through

Current source shows inconsistent parameter propagation:

- some invoice KPI links pass report parameters;
- graph, backlog, and Top-N/customer/product destinations can omit selected territory filters.

Only fix the links that fail a user workflow. Do not rewrite passing links or the territory resolver.

## 12. CSV export contract

The basic customer export contract is:

> Export the same customer result and selected-period sales as the Customers page, in a valid CSV.

Required:

- same customer result set as the page;
- same selected period;
- valid tabular CSV;
- one heading for every field;
- one field for every heading;
- existing cue-character field labeled `Price Level Cue`;
- human-readable period heading such as `Previous Month Sales`, unless a named integration requires a stable machine field.

Not part of the current Customers bug:

- scope/preamble block;
- totals row;
- generic `Selected Range Sales` header;
- new ranges;
- revenue changes;
- broad CY/LY relabeling.

A scope block before the CSV header can break normal CSV consumers. Do not add one without a named client workflow and compatibility decision.

## 13. Canonical fixtures

### 13.1 `wwjc/betaverify`

Purpose: legitimate restricted-rep Sales Portal testing.

- non-admin on both admin columns;
- blank customer number;
- user type `z'-Bet A Verify` (id 2864);
- Dashboard enabled;
- portal totals enabled;
- all-customer totals off;
- six separate territories:
  - `105:1 Gigi Lane`
  - `105:2 Katherine McMullan`
  - `105:3 Weezie Ward`
  - `105:4 Susan Rutherford`
  - `105:5 Grace Ingram`
  - `105:6 Krissa DeGennaro Newell`

Always record the warehouse timestamp before interpreting territory behavior.

### 13.2 Stable closed baseline

`wwjc`, territory `105:1 Gigi Lane`, 2026-06-01 through 2026-06-30:

- 110 invoices;
- 75 accounts;
- `$123,585.35`.

Use this for closed-period acceptance. Current YTD is not a stable baseline.

### 13.3 Authorization out-of-book control

Current control selected on 2026-08-04:

- customer `14378` — MEG BRAFF DESIGNS;
- territories `D6 LORNE GARDNER`, `30440 Interim Rep House Account`;
- invoice `INV65157`;
- portal invoice id `4667912895`;
- invoice date 2026-08-04;
- amount `$100.00`.

This record is outside `betaverify`'s six-territory book.

## 14. Mandatory verification matrix

Before a territory or access ticket is ready for implementation:

| Case | Required result |
|---|---|
| Non-admin, one selected assigned territory | Correct rows and total |
| Multiple assigned territories, none selected | Union of permitted territories |
| Explicit selection by all-totals user | Selected territory honored where product supports narrowing |
| NULL territory assignment | Fail closed |
| Empty territory array | Fail closed |
| Customer user | Own customer only |
| Bill-to territory match | Documented customer-book behavior |
| Ship-to-only territory match | Applicable ship-to behavior |
| Mixed-case territory code | Case-insensitive intended match |
| Blank/collapsed ship-to key | No accidental bridge match |
| Dashboard KPI | Correct measure and selected book |
| Dashboard Top Customers | Membership belongs to selected book |
| Dashboard Top Products | Uses territory-scoped order facts |
| Drill-through | Intended customer/order/period/filter context preserved |
| Direct invoice/customer URL | Out-of-book record denied |
| Dashboard sub-action with gate off | No metric content |

No stubbed permission check qualifies as acceptance.

## 15. Code map

### Access and permissions

- `app/models/org_user.rb`
- `app/models/user_type_permissions.rb`
- `app/helpers/ecat_permissions_helper.rb`
- `app/controllers/ecat_dashboard_controller.rb`
- `app/controllers/ecat_invoices_controller.rb`
- `app/controllers/ecat_customers_controller.rb`

### Warehouse territory scope

- `app/services/warehouse/filter_items_by_territory_code_limit.rb`
- `app/services/warehouse/filter_items_by_territory_code.rb`
- `app/services/warehouse/get_invoices_for_invoices_page.rb`
- `app/services/warehouse/get_orders_for_orders_page.rb`
- `app/models/warehouse_access.rb`

### Territory ETL

- `app/services/warehouse/extracts_and_transforms.rb`
- `app/services/warehouse/extracts_and_transforms/rep_to_territory_bridge.rb`
- `app/services/warehouse/extracts_and_transforms/territory_to_ship_to_bridge.rb`
- `app/services/warehouse/extracts_and_transforms/format.rb`
- `app/services/warehouse/extracts_and_transforms/sales_portal_invoice_dimension.rb`
- `app/services/warehouse/extracts_and_transforms/sales_portal_sales_fact.rb`

### Customers and export

- `app/controllers/ecat_customers_controller.rb`
- `app/services/controllers/ecat_customer.rb`
- `app/views/ecat_customers/index.html.erb`
- `test/services/controllers/ecat_customer_test.rb`

### Dashboard and invoice measures

- `app/models/ecat_reporting/reports/dashboard.rb`
- `app/models/ecat_reporting/invoices/invoice.rb`
- `app/services/warehouse/get_sales_facts_for_invoices_by_territory.rb`
- `app/views/ecat_dashboard/`

## 16. Known open decisions

These are not authorized engineering work until decided:

1. Does ship-to-only access constrain row-level sales to matching ship-tos everywhere?
2. What compatibility rule should replace SERV-2196's current bill-to/ship-to over-grant?
3. Should invoice header totals use imported net amount or line-derived amount?
4. Do Dashboard panels need clearer labels for ordered versus invoiced measures?
5. Which Dashboard drill-throughs should preserve selected territory and period?
6. Does any client automation require a stable customer-export period column?
7. Is multi-valued invoice/order `RepNumber` worth the XL schema/import/ETL work?
8. Which affected organization should reproduce the ship-to casing defect?

## 17. Current verified findings

As of 2026-08-04:

- `PROD-PASS`: Invoice Gigi Lane/June total matched SQL within display rounding.
- `PROD-PASS`: Dashboard Current-YTD invoiced KPI matched Invoices for Gigi Lane.
- `PROD-REPRO`: Customers Previous Month omitted the selected-period card and column.
- `PROD-PASS`: Customers Previous YTD showed the selected-period card and column.
- `PROD-REPRO`: Customers CSV has fewer headings than row values.
- `CODE-IMPLICATION`: Dashboard destination links inconsistently propagate selected filters.
- `CODE-RISK`: direct invoice/customer routes and Dashboard sub-actions may expose out-of-book data.
- `CODE-RISK`: ship-to casing and collapsed blank ship-to keys can affect territory matching.

## 18. Agent operating protocol

Before reviewing or changing Sales Portal work, an agent must:

1. Read this specification.
2. Read the current dated decision file in this folder.
3. Read the latest dated handoff prompt in this folder.
4. Identify the exact product surface.
5. Identify the user role and fixture.
6. Determine whether production and repository revisions match.
7. Label every material claim.
8. Reproduce before rewriting a ticket.
9. Use a closed period for stable acceptance.
10. Keep Jira and Confluence read-only unless Kylor gives explicit per-conversation authorization.
11. Draft one coordinated correction set instead of adding layered comments.
12. Do not group tickets because their symptoms share words such as “filter,” “total,” or “territory.”

## 19. Source documents

### Product documentation

- [Sales Portal Behavior Design draft](https://supercatsolutions.atlassian.net/wiki/pages/resumedraft.action?draftId=1193246721)
- [Sales Portal Calculations](https://supercatsolutions.atlassian.net/wiki/spaces/SCKB/pages/1193246721/Sales+Portal+Calculations)
- [Accessing Sales Portal Data](https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/994279438/Accessing+Sales+Portal+Data)
- [Sales Territories](https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/336363531/Sales+Territories)
- [eCat Online Sales Portal](https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/142737411/eCat+Online+Sales+Portal)
- `Insightful Product 4.0/knowledge/industry_context.md`

### Current reset authority

- `PM/sales-portal-agent-starters/cycle-04-outputs/REVIEW-sales-portal-backlog-reset-2026-08-04.md`
- `PM/sales-portal-agent-starters/cycle-04-outputs/POV-sales-portal-what-next-2026-08-04.md`

### Rails repository

- `/Users/kylorjohnson/supercat-code/supercat_server`
- inspected local revision: `d4a0e7d40`
- inspected `origin/master` during the reset: `0856f2d1a`

The deployed production revision remains to be recorded during the authorization probe.
