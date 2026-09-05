# FIX / Lane 0 — Diagnosis: Territory & Date-Filter Truth (Bet A)

**Date:** 2026-07-16
**Lane:** 0 (Trust / Fix)
**Bet:** A — Territory & filter truth
**Isolation:** ON — diagnosis + proposed patch only. Nothing applied to `supercat-code`. Implement only on `ISOLATION OFF — GO on SERV-XXXX`.
**Tickets:** SERV-2178, SERV-2196, SERV-2395

> Note on process: the FIX starter runs **one ticket per Agent chat** when isolation lifts. This file is the bundled Bet-A diagnosis produced by PROGRAM; each ticket below is self-contained so it can be handed to its own FIX chat for implementation.

---

## Shared architecture (read once)

- Portal controllers inherit `EcatOnlineController`, which sets `layout 'ecat'` (`app/controllers/ecat_online_controller.rb:16`). **Portal shares the catalog layout + shared filter partials** (`ecat/date_range_global`, `ecat/_feature_stat`, `ecat/filters/*`). Any fix that touches a shared partial is org-wide and touches catalog — prefer controller/query/service-level fixes.
- Territory assignment source of truth: `org_users.territory_codes` (JSONB array), set via `OrgUser#set_territory_codes` (`app/models/org_user.rb:506`).
- The portal does **not** read `org_users.territory_codes` live. It reads a **warehouse** projection built by ETL:
  `org_users.territory_codes` → `rep_to_territory_bridge` (`app/services/warehouse/extracts_and_transforms/rep_to_territory_bridge.rb:23`) → matched to `rep_dimension` by **username** → `territory_keys` CTE (`app/models/warehouse_access.rb:1040`).
- Territory restriction WHERE clause: `territory_code_limit_subquery` (`app/models/warehouse_access.rb:424`) filters on `customer_key IN customer_keys OR ship_to_key IN ship_to_keys` (+ `territory_key` when the `territory_access_via_rep_number` flag is on).
- `PerOrgPortalWarehouseAccess` (`app/models/per_org_portal_warehouse_access.rb`) is a thin wrapper; the logic lives in `WarehouseAccess`.

---

## SERV-2178 — Sales Portal doesn't grant access to all territories

### 1. Root cause (plain language)
Two distinct failure modes, both stemming from the same design fact (**portal reads the warehouse projection, not the live `territory_codes` column**):

- **(a) Empty-territory leakage (primary, confirmed live).** A portal-enabled user with **no** territory assigned has an empty `territory_keys` set. Depending on user-type permission (`UserTypePermissions.may_access_all_customer_sales_totals?`, `warehouse_access.rb:425`), that user either sees **ALL customers** or **NONE** — never "their book." This is exactly the KLL "sunburst showing all customers" incident.
- **(b) Stale/missing warehouse bridge.** `territories_for_orguser` (`warehouse_access.rb:899`) inner-joins `territory_dimension`. A territory that is (i) newly assigned on `org_users.territory_codes` but not yet re-ETL'd into `rep_to_territory_bridge`, or (ii) present on the user but absent from the `territories`/`territory_dimension` master, will silently not appear — the user "loses" assigned territories.

### 2. Repro / org evidence
- **KLL (`kll`, org 166)** — `documentation/KLL_Territory_Sales_Portal_Analysis_Feb_2026.md`:
  - 9 users had Sales Portal **enabled** with **empty** `territory_codes`.
  - `territories` master table had **0 rows** for org 166.
  - Documented effect: "Without territories, these users either see ALL customers or NO customers … root cause of the 'Sunburst showing all customers' issue from Jan 30 training."
- Confirms mode (a) leakage in production and mode (b) empty-master condition.

### 3. Proposed fix + risk (markdown only)
Smallest correct changes, in priority order:

1. **Config remediation (no code):** populate `territories` master + assign `org_users.territory_codes` for portal-enabled reps; re-run warehouse ETL. Fixes the majority of live incidents without touching Rails.
2. **Fail-closed guard (small code):** in the territory limit path (`warehouse_access.rb:424-434`), when a rep-type user resolves to an **empty** `territory_keys`/`customer_keys`/`ship_to_keys` set, return `false` (see NONE) rather than allowing the all-customers branch — never leak the whole org to an unterritoried rep. Gate behind a per-org flag so orgs that intentionally give reps full visibility (via `may_access_all_customer_sales_totals?`) are unaffected.
3. **Optional live-fallback:** in `territories_for_orguser` (`warehouse_access.rb:899`), union in `org_user.territory_codes` that exist in `territory_dimension` but are missing from the bridge, to reduce ETL-lag "lost territory" reports.

**Risk / coupling:** `territory_code_limit_common_table_expression` is shared by customers, orders, invoices, and reports — any change to the CTE is org-wide across all portal surfaces. Fix (2) changes visibility semantics for unterritoried reps; must be flag-gated and verified against `may_access_all_customer_sales_totals?` user types.

### 4. Acceptance criteria
- Given a portal rep assigned territories `[T1, T2]` (with ETL current), when they open Customers/Orders/Invoices, then all customers in T1 ∪ T2 appear and none outside.
- Given a portal-enabled rep with **empty** `territory_codes` and a user type **not** authorized for all-customer totals, then they see **no** customers (fail-closed) and a clear empty-state — never the full org.
- Given a newly assigned territory that exists in the `territories` master, after ETL the territory appears in the filter dropdown and gates rows.
- Verify on `kll` after config remediation; regression-check `sarreid`/`cci` reps see an unchanged book.

---

## SERV-2196 — Does not restrict to ShipToTerritoryCodes

### 1. Root cause (plain language)
Two compounding issues:

- **(a) Dual-path over-grant.** Customer-list access is granted if the customer's **bill-to** `TerritoryCodes` OR **any** ship-to `ShipToTerritoryCodes` matches the rep's territories (`customer_keys` from bill-to bridge + `ship_to_keys` from ship-to bridge; `warehouse_access.rb:1048-1055`, `filter_customers_by_territory_code_limit.rb:43`). For orgs whose territory model is **ship-to based**, a bill-to match pulls in the customer and exposes **all** of its ship-tos, not just the ship-tos in the rep's territory.
- **(b) Ship-to bridge case mismatch (silent failure).** In `territory_to_ship_to_bridge.rb`, the outer loop iterates **downcased** org territory codes (`:25`) but the `shipping_location_ids_by_territory_code` map is keyed by **raw (non-downcased)** `sl.territory_codes` (`:37-39`). If ship-to codes are mixed-case in the DB, bridge rows are **not** produced → the ship-to restriction path is empty → ship-to filtering silently does nothing.

### 2. Repro / org evidence
- Code-confirmed: bill-to bridge is built only from customer `TerritoryCodes` (`territory_to_customer_bridge.rb:25-28`); ship-to bridge from `ShippingLocation.territory_codes` mapped from CSV `ShipToTerritoryCodes` (`shipping_location_importer.rb:33`).
- Case-mismatch is a static code defect (`territory_to_ship_to_bridge.rb:25` vs `:37`); reproduce by seeding a shipping location with a mixed-case `ShipToTerritoryCodes` and confirming no `territory_to_ship_to_bridge` row.
- Test `test/services/warehouse/territory_code_limit_test.rb:29-41` shows ship-to restriction works **when the bridge is correctly populated** — i.e. the defect is in bridge population + dual-path breadth, not the WHERE clause itself.

### 3. Proposed fix + risk (markdown only)
1. **Fix ETL case normalization (small, high-value):** downcase the keys of `shipping_location_ids_by_territory_code` to match `format_territory_key` (`territory_to_ship_to_bridge.rb:37-39`). Restores ship-to restriction for mixed-case orgs.
2. **Per-org "ship-to territory model" flag (small):** when set, build `customer_keys` from the **ship-to** bridge only (skip bill-to bridge in the rep branch of `territory_code_limit_common_table_expression`, `warehouse_access.rb:1048-1051`) so a bill-to match doesn't expose out-of-territory ship-tos.

**Risk / coupling:** removing the bill-to path breaks orgs that intentionally scope reps by bill-to `TerritoryCodes` → must be flag-gated, default preserving current behavior. Case fix is low-risk but re-ETL required to backfill bridges.

### 4. Acceptance criteria
- Given an org on the ship-to territory model and a rep assigned ship-to territory `B`, when they open Customers, then only customers with a ship-to in `B` appear, and for those customers only the `B` ship-tos count toward their totals.
- Given a mixed-case `ShipToTerritoryCodes` value, after ETL a `territory_to_ship_to_bridge` row exists and gates rows (case-insensitive).
- Bill-to-model orgs are unchanged (flag default off).

---

## SERV-2395 — Date filter dropdown does not update summary blocks

### 1. Root cause (plain language)
The summary blocks are architecturally split and most of them are **date-range-independent by design**, so changing the dropdown appears to "do nothing":

- **Customers page** (`app/views/ecat_customers/index.html.erb`): the LY / CY / Backlog blocks load via AJAX to `ly_sales_total` / `cy_sales_total` / `backlog_total` (`ecat_customers_controller.rb:29-48`). These call hardcoded `previous_year_date_range` / `current_year_date_range` / no-date (`app/services/controllers/ecat_customer.rb:113-122`) — they **ignore** `params[:date_range]`. The only date-aware block ("selected range sales") is gated by `show_custom_totals_by_bill_to?` (`ecat_customers_controller.rb:294`), which uses **substring** matching: `params['date_range']['previous_ytd'] || params['date_range']['custom']`. That truthy-matches only `previous_ytd`/`custom`; for `current_ytd`, `previous_year`, `all_available`, `current_mtd`, etc. the date-aware block is **hidden and never updates**.
- **Dashboard** (`app/models/ecat_reporting/reports/dashboard.rb`): `invoice_total` respects `from_date`/`to_date`, but `backlog_total` explicitly ignores the range ("backlog is independent of date range selected", `dashboard.rb:17`).

### 2. Repro / org evidence
- Static code defect at `ecat_customers_controller.rb:294-296` (substring match) + hardcoded ranges at `ecat_customer.rb:113-122`.
- Repro: on Customers, select date range = `current_ytd` (or any non-`custom`/`previous_ytd`) → the selected-range total block does not render/update while CY/LY/Backlog stay fixed. Data span is real and wide, so ranges matter: `cci` invoices 2023-10-20 → 2026-07-15; `sarreid` invoices 2022-01-04 → 2026-07-16.

### 3. Proposed fix + risk (markdown only)
1. **Correct the gate (tiny):** replace substring match with explicit set membership, e.g. `%w[all_available current_ytd previous_ytd previous_year current_mtd previous_month yesterday custom].include?(params[:date_range])` (`ecat_customers_controller.rb:294`), or simply always render one "Selected Range Sales" block.
2. **Add a date-aware totals endpoint (small):** a `date_range_sales_total` action calling `invoice_totals_by_bill_to_for_date_range` with `Eol::DateRanges.date_range(params[:date_range], params[:from_date], params[:to_date])`, wired to the block for **every** selection — rather than repurposing the fixed CY/LY endpoints.
3. **Copy/UX:** keep CY/LY/Backlog labeled as fixed-period anchors; make the date-driven block visually the primary "for selected range" number so the dropdown's effect is obvious. Document that dashboard backlog is intentionally date-independent.

**Risk / coupling:** CY/LY semantics feed export CSV headers and per-row columns in `_list.html.erb`; do not change their meaning, only add the selected-range block. Shared `ecat/_feature_stat` / `ecat/date_range_global` partials are used on orders/invoices/reports — prefer a new action + block over editing shared partials.

### 4. Acceptance criteria
- Given the Customers page on any supported date range, when the user changes the dropdown, then a "Selected Range Sales" block recomputes to that exact range (verified against `invoice_totals_by_bill_to_for_date_range`).
- CY / LY / Backlog remain labeled as fixed-period anchors and are unchanged.
- Dashboard `invoice_total` recomputes on range change; backlog is labeled date-independent.
- Selected-range totals reconcile to `SUM(portal_invoices.net_amount)` for that org + range.

---

## 5. Handoff
- Paste this into `05-ORCHESTRATOR` for Review Cards (done in `ORCHESTRATOR-review-cards.md`).
- Do **not** implement. When ready, open one FIX chat per ticket on `ISOLATION OFF — GO on SERV-2178` (then 2196, then 2395).
- Recommended implementation order: **SERV-2178 (fail-closed leakage)** first — trust gate; then **SERV-2196** (ship-to case fix + model flag); then **SERV-2395** (date-aware block).
