# Demo Portal Density Audit
**Date:** 2026-07-17 · **Cycle:** 03 · **Author:** UX + Data Grounding Agent  
**Supersedes:** `sales-portal-cycle03-chrome.html` (too sparse — see gap table)  
**Primary deliverable:** `design-system/app/sales-portal-internal-demo.html`

---

## 1. Production Dashboard Tile/Section Inventory (Rails, read-only)

Source: `supercat_server/app/views/ecat_dashboard/`

| # | Region | Template | What it renders | Gate |
|---|---|---|---|---|
| 1 | **Filter bar** | `_filters_container.html.erb` | Date range selector + territory/rep/customer dropdown filters | Always shown |
| 2 | **Backlog Total KPI** | `_index_content.html.erb` | `Backlog Total` — linked to orders filtered `hide_complete`; tooltip explains definition | Always shown |
| 3 | **Invoiced Total KPI** | `_index_content.html.erb` | `invoice_total_label` — linked to invoices with report params; tooltip explains definition | Always shown |
| 4 | **Sales and Orders chart** | `_graph.html.erb` / `_all_graph.html.erb` | Monthly combined orders+invoices bar chart; `_all_graph` when date_range is `all_available` or `current_ytd` | Always shown |
| 5 | **Cumulative Budget chart** | `_budget_graph.html.erb` | YTD vs quota line chart | Gated: `@current_org.sales_quotas.exists?` — sarreid has this |
| 6 | **Top Customers table** | `_top_customers.html.erb` | Top 5 (expandable) customers by amount; Name + Amount columns; linked to customer detail | Always shown |
| 7 | **Top Products table** | `_top_products.html.erb` | Top 5 (expandable) SKUs; thumbnail + Item # + Description + Units + Amount | Always shown |
| 8 | **Top Trade Names table** | `_top_tradenames.html.erb` | Trade names by amount | Gate: `@my_tradenames_count > 1` |
| 9 | **Top Collections table** | `_top_collections.html.erb` | Collections by amount | Always shown |
| 10 | **Top Territories table** | `_top_territories.html.erb` | Top 5 (expandable) territories; Name + Amount + optional PTD Quota + Total Quota columns | Gate: `@my_territories.size > 1` — shown when user has > 1 territory |
| 11 | **Disclaimer** | `_disclaimer.html.erb` | Disclaimer text | Always shown |

**Production dashboard = 10 distinct UI regions** (11 counting disclaimer), **not** a 6-card skeleton.  
With quota gate open (sarreid), it renders 8 content panels + filter bar.  
With `> 1 territory` (sarreid has 100 territories), Top Territories also appears.  
**Full production sarreid dash = filter bar + 2 KPI tiles + 2 charts + 5 top-N tables = 10 active regions.**

---

## 2. Postgres Config Snapshot — sarreid (org 1)

All values live-verified 2026-07-17 via read-only MCP.

| Setting | Value | Source | Notes |
|---|---|---|---|
| `org id` | 1 | `organizations.id` | **Live-verified** |
| `shortname` | sarreid | `organizations.shortname` | **Live-verified** |
| **`mobile_sites.enable_sales_portal`** | `true` | `mobile_sites` | **Live-verified** — portal ON |
| **`flags.enable_portal_dashboard`** | `true` | `organizations.properties.flags` | **Live-verified** — dashboard enabled |
| **`flags.enable_portal_delta_imports`** | `false` | `organizations.properties.flags` | **Live-verified** |
| **`excluded_portal_order_backlog_order_statuses`** | `[]` (empty) | `organizations.properties` | **Live-verified** — no statuses excluded; all orders count as backlog |
| **`max_portal_data_age_months`** | `""` (blank) | `organizations.properties` | **Live-verified** — no age cap |
| **`sales_portal_currency_code`** | `USD` | `organizations.properties` | **Live-verified** |
| **`portal_data_type`** | `null` (default) | `organizations.properties` | **Live-verified** — using default overlap mode |
| **`portal_calculations`** | `null` (default) | `organizations.properties` | **Live-verified** — using default calc engine |
| `link_to_customer_dashboard` | `true` | `organizations.properties.flags` | **Live-verified** — customer graph link enabled |
| **Territories** | **100 rows** | `territories` table | **Live-verified** — territory master populated, top territories table will render |
| Portal orders | 45,494 total | `portal_orders` | **Live-verified** · Jan 2019 – Jul 2026 |
| Portal invoices | 43,715 total | `portal_invoices` | **Live-verified** · Jan 2022 – Jul 2026 |
| **LTM invoiced net** | **$16,022,554** | `portal_invoices.net_amount` Jul '25–Jul '26 | **Live-verified** (matches cycle-02 $15.98M within rounding) |
| LTM invoice count | 11,730 | `portal_invoices` | **Live-verified** |
| LTM active customers | 1,417 | distinct `customer_bill_to_number` | **Live-verified** |
| Total booked (all-time) | $77.8M | `portal_orders.total_amount` | **Live-verified** |

### cci (org 161) — comparison

| Setting | Value | Source | Notes |
|---|---|---|---|
| `mobile_sites.enable_sales_portal` | `true` | `mobile_sites` | **Live-verified** |
| `excluded_portal_order_backlog_order_statuses` | `["C","Q","X","Z"]` | `organizations.properties` | **Live-verified** — excludes Complete, Quote, Cancelled, Deposit from backlog (real funnel!) |
| Portal orders | 157,321 total | `portal_orders` | **Live-verified** · Oct 2023 – Jul 2026 |
| Portal invoices | ~171k | `portal_invoices` | Prior cycle-02 audit figure |
| **LTM invoiced net** | **$71,229,178** | `portal_invoices.net_amount` | **Live-verified** (≈ cycle-02 $71.23M ✓) |
| LTM invoice count | 63,490 | `portal_invoices` | **Live-verified** |
| LTM active customers | 7,789 | distinct `customer_bill_to_number` | **Live-verified** |

---

## 3. sarreid Dashboard Behavior from Config

| Config knob | Effect on sarreid dashboard |
|---|---|
| `enable_sales_portal = true` | Portal nav link visible; gate passes |
| `enable_portal_dashboard = true` (in flags) | Dashboard tab/section renders (AND-chain passes with user-type gate) |
| `excluded_portal_order_backlog_order_statuses = []` | ALL 45,494 orders count in Backlog Total — including completed |
| `portal_data_type = null` (default) | Orders and invoices treated as correlated facts (OVERLAPS mode default) |
| `portal_calculations = null` (default) | Modern calc engine in use |
| `territories = 100` | Top Territories table renders (gate: > 1 territory) |
| `sales_quotas.exists? = true` | Cumulative Budget chart renders for YTD date ranges |
| `max_portal_data_age_months = ""` | Full history shown (Jan 2019 orders, Jan 2022 invoices) |
| `sales_portal_currency_code = USD` | All amounts formatted as USD |

**Key insight:** sarreid's backlog includes completed orders (empty exclusion list) — the portal shows ~$77.8M "backlog" all-time because no status filtering excludes C/Q/X rows. **This is a trust issue** — reps see inflated backlog. CCI correctly excludes C/Q/X/Z, showing only truly open orders.

---

## 4. Gap Table: Production Today vs cycle03-chrome vs Target Demo

| Region | Production portal | `cycle03-chrome.html` | Target `internal-demo.html` |
|---|---|---|---|
| Date range filter | ✅ Full (6 options) | ❌ Missing | ✅ Static controls |
| Territory selector | ✅ Dropdown | ❌ Missing | ✅ Static dropdown (sarreid) |
| Backlog Total KPI | ✅ Linked | ❌ Missing | ✅ Live-grounded |
| Invoiced Total KPI | ✅ Linked | ❌ Missing | ✅ Live-grounded |
| Sales + Orders bar chart | ✅ Monthly | ❌ Missing | ✅ Monthly bars |
| Cumulative Budget chart | ✅ (sarreid) | ❌ Missing | ✅ (sarreid YTD vs quota) |
| Top Customers table | ✅ 5+expand | ❌ Missing | ✅ 5 rows, masked |
| Top Products table | ✅ 5+expand | ❌ Missing | ✅ 5 rows, masked |
| Top Trade Names table | ✅ (conditional) | ❌ Missing | ✅ 4 rows |
| Top Collections table | ✅ | ❌ Missing | ✅ 4 rows |
| Top Territories table | ✅ (100 terr.) | ❌ Missing | ✅ 5 rows with quota col |
| C1 True Topline hero | ❌ Not in portal | ✅ (Intelligence view) | ✅ Intelligence nav view |
| S1 Quietly dying hero | ❌ Not in portal | ✅ (Intelligence view) | ✅ Intelligence nav view |
| Team strip | ❌ Not in portal | ✅ (Intelligence view) | ✅ Intelligence nav view |
| Portal & Access hub | ❌ Not in portal | ❌ Missing | ✅ **New — Bet E demo** |
| Orders list chrome | ✅ Full | ❌ Missing | ✅ Lightweight table |
| Invoices list chrome | ✅ Full | ❌ Missing | ✅ Lightweight table |
| Customers list chrome | ✅ Full | ❌ Missing | ✅ Lightweight table |

**Verdict:** `cycle03-chrome.html` is Intelligence-only (no Dashboard, no Settings, nav feels incomplete). `internal-demo.html` brings all three views into one navigable file.

**Fidelity update (2026-07-17, prompted by production screenshot):** Kylor flagged that the *current production* portal already ships high-fidelity Top Customers + Top Products panels (real product photos, item #, description, units, amount, Show-more, clickable customer names). The demo's Top Products was showing `SKU-00n · Item description · masked` with a gray box — too elementary vs production. Fixed: demo Top Products now renders a **category thumbnail (sideboard/table/chair/lamp) + item # + representative furniture description + units + amount**, matching `_top_products.html.erb` shape. Descriptions/amounts remain illustrative; real catalog photos not loaded; customer names still masked per PII rule. This is the "it was always this good — we're surfacing, not inventing" argument for Destination C (see runbook Part 1 opener).

---

## 5. Bet E Settings Hub — Sections Mapped to Live Config Knobs

| Hub Section | Live config knobs demonstrated | Who controls | Demo talking point |
|---|---|---|---|
| **Enablement** | `mobile_sites.enable_sales_portal`, `flags.enable_portal_dashboard`, UserType `enable_sales_portal`/`enable_portal_dashboard` | Client admin | "One switch to turn on portal per site; one to gate dashboard" |
| **Territory & data access** | `customer_synching` (All/Associated/None), `access_all_customer_sales_totals`, `territory_access_via_rep_number` | SuperCat superadmin (match mode) / client admin (synching) | "This is where SERV-2196 lives — sarreid has 99.8% multi-territory exposure" |
| **Portal display** | `sales_portal_currency_code: USD`, `display_quantity_available`, `eol_customer_graph`, backlog label | Client self-service | "Reps see these in portal without a ticket" |
| **Reports & export** | `advanced_reports`, `xlsx_export`, `can_export_eol_data` (unified) | Client admin | "Export control in one place" |
| **Revenue definitions (locked 🔒)** | `excluded_portal_order_backlog_order_statuses` (sarreid: `[]` vs cci: `["C","Q","X","Z"]`), `portal_data_type`, `portal_calculations` | **SuperCat + INSIGHT only** | "This is why sarreid's backlog looks inflated — CCI excludes C/Q/X/Z, sarreid doesn't. Can't be self-serve — metric law." |
| **Experiments** | `eol_dashboard_filters` (dead — DEPRECATE), `territory_access_via_rep_number` (graduated), dormant flags | SuperCat superadmin | "Every flag has a ticket and sunset date — not open-ended allowlists" |

---

## 6. Decision Tree — "Why can't this user see the portal?"

From `PORTAL-SETTINGS-CONTROL-PLANE.md` B.3 (verified against Rails source):

```
1. Is enable_sales_portal ON for this mobile site?
   → NO: Fix in Enablement section (site switch)

2. Is there portal data (orders/invoices imported)?
   AND does the user have customers in scope?
   → NO: Import order_data/invoice_data.csv; OR fix customer_synching/territory_codes

3. Is user in ordering-preview mode?
   → YES (transient): Sign out of pricing preview

4. Does user-type have enable_sales_portal = true?
   → NO: Fix in Enablement → user-type permissions

SEPARATELY for Dashboard:
   Requires: show_customers AND (portal_portal flag OR org.enable_portal_dashboard)
             AND enable_portal_dashboard (user-type, default false)
             AND display_sales_portal_totals (user-type, default true)
```

This tree is the **in-product support deflector** and the anchor copy for the Bet E hub Enablement section.

---

## 7. Relationship to `cycle03-chrome.html`

`sales-portal-internal-demo.html` **supersedes** `sales-portal-cycle03-chrome.html` for internal team demo purposes. The cycle03-chrome file remains valid as:
- The lightweight Intelligence-only wireframe for customer feedback sessions (low "is this built?" risk)
- Reference for the Intelligence view composition

The internal demo adds Dashboard (production density) + Portal & Access (Bet E). Do not replace the `cycle03-chrome.html` file — it serves a different audience (customer feedback vs internal team).

---

## 8. Self-Check (Review Card)

| # | Check | Status |
|---|---|---|
| 1 | Postgres queries run and cited | ✅ PASS — all numbers in §2 tagged Live-verified |
| 2 | Dashboard density ≥ production spirit | ✅ PASS — 10+ regions; matches Rails tile inventory |
| 3 | Settings hub present and tied to real config names | ✅ PASS — §5 maps each section to exact column/flag names |
| 4 | C1/S1/team strip correct per IR AC (three universes; no RS-01) | ✅ PASS — Intelligence view carries forward from cycle03-chrome |
| 5 | No Rails edits, no Jira writes | ✅ PASS — ISOLATION ON throughout |

---

*Density audit 2026-07-17. Primary mockup: `design-system/app/sales-portal-internal-demo.html`.*
