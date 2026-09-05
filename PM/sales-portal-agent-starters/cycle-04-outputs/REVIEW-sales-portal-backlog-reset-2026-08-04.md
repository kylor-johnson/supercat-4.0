# Sales Portal backlog reset — independent review

**Date:** 2026-08-04  
**Decision owner:** Kylor Johnson  
**Engineering reader:** Brent Sanders  
**Evidence cut:** Live Jira and Confluence read-only review, Rails source review, read-only production SQL, and the 2026-08-04 `wwjc` production walkthrough

## 1. Executive verdict

The original Bet A should be retired as an engineering bet.

Its central thesis was wrong: EBR-40/SERV-2447, EBR-212/SERV-2448, and EBR-91/SERV-2449 do not currently form one demonstrated production defect or one shared implementation package. They were grouped because the symptoms all sounded like “filter truth.” Production evidence now separates them:

- **SERV-2449 is a demonstrated production defect, but its current “Done when” is not an acceptable product specification.** The Customers page hides a period value that the export already calculates, and the CSV has more values than headings. The ticket then invents a scope block, totals row, generic header, fallback behavior, and broader relabeling without a named customer need. The smallest high-confidence package is the display repair plus CSV structural repair—not the invented export redesign.
- **SERV-2447 passed its primary production route.** A legitimate non-admin rep fixture selected `105:1 Gigi Lane` for June 2026 and the displayed invoice total matched the stable SQL baseline: `$123,585` versus `$123,585.35`. The screenshot does not prove the expected 110-invoice count.
- **SERV-2448 passed its primary KPI route.** The same fixture and territory produced `$836,263` on both Invoices and Dashboard for Current YTD. Top-N membership remains unverified; source confirms that Dashboard destination links omit the selected territory filter, with user-visible production impact still to reproduce.
- The live result means **SERV-2447 and SERV-2448 are not presently demonstrated headline bugs**. They may contain edge-case defects or justify regression tests, but the current Jira descriptions overstate the case for behavior changes and a shared refactor.
- **Dashboard territory filtering already has a completed engineering predecessor, SERV-1092.** The current production pass is consistent with that history. SERV-2448 must be treated as possible regression hardening or an edge-case follow-up, not a clean-sheet implementation.
- The ship-to casing defect, fail-closed access behavior, and invoice `rep_number` identity are real or plausible concerns, but they are separate problems with different fixtures, data semantics, and change risk. They do not rescue the original Bet A grouping.
- **The code audit found a more important access-control cluster outside Bet A.** In the checked-out revision, Dashboard sub-actions do not enforce the Dashboard-specific gate; invoice show/email and customer detail routes do not consistently resolve records through territory-authorized relations. These are code-demonstrated risks that need an immediate non-admin direct-URL probe. A reproduced cross-territory record exposure should outrank SERV-2449.
- **Invoice rows and the displayed Invoice Total use different amount sources.** Rows expose invoice-header `net_amount`; the total sums line-derived `amount_invoiced`. Scope can be correct while dollars still diverge. This is a separate reporting-contract decision, not proof that the June acceptance result was wrong.

Bet A therefore **failed as a shaped engineering portfolio, partially succeeded as an investigation, found one smaller valid fix, and exposed separate access-model work**. Its useful output was the legitimate fixture, the closed-period baseline, the product boundary between master-assigned territory and invoice rep number, the CSV diagnosis, and the discovery that admin evidence had invalidated earlier conclusions.

### Immediate decisions

1. **Build now:** a narrowed SERV-2449 package: selected-period display gate, CSV heading/value parity, `Price Level Cue`, and focused tests.
2. **Urgent validate-first gate:** use `betaverify` to request an unassigned invoice/customer directly and call Dashboard sub-endpoints while the Dashboard gate is false. If unauthorized data is returned, ship a focused authorization hotfix before SERV-2449.
3. **Validate first:** SERV-2447 and SERV-2448 edge cases. Write failing tests or reproduce a failing route before changing behavior. Do not fund the proposed broad unification merely because two paths exist.
4. **Split:** customer/ship-to access semantics, ship-to casing, collapsed NULL ship-to keys, empty-assignment fail-closed behavior, invoice-rep identity, and invoice amount semantics into separate decisions.
5. **Decision required:** EBR-180/SERV-2178 is active, assigned work with an XL implementation warning. Kylor and Brent must explicitly continue, narrow, or pause it; this review does not silently park it. EBR-772/776 and unrelated Intelligence/LLM work remain outside this reset.
6. **Verify or reclassify after the correction pass:** confirm EBR-7 against its actual discount acceptance criteria; resolve EBR-474 versus EBR-601 as duplicate product demand; reclassify EBR-40/212 and SERV-2447/2448 as “primary route passes; residual gaps only.”

## 2. What Bet A was supposed to be

Bet A attempted to make one promise across Invoices, Dashboard, Customers, and export:

> A selected date range and territory should produce the same book of business, rows, totals, metrics, and exported data everywhere.

The product tickets were:

| Product | Engineering | Intended promise |
|---|---|---|
| EBR-40 | SERV-2447 | Invoice rows and displayed total honor selected territory |
| EBR-212 | SERV-2448 | Dashboard metrics and Top-N honor selected territory |
| EBR-91 | SERV-2449 | Customers shows selected-period sales and exports a structurally trustworthy CSV |

They were grouped because all three touched filtering and reconciliation. That was a useful user-level principle, but it was not evidence of one root cause. The Customers defect is date-range presentation/export code. Invoice and Dashboard territory scope run through warehouse access and bridge data. A shared acceptance principle is not the same as a shared engineering implementation.

## 3. What actually happened

### What previous work got wrong

- It treated admin screenshots as rep evidence. `OrgUser#is_admin?` is true when either the organization-user admin column or the global user admin column is true; permission checks then short-circuit. Those captures could not test territory restrictions.
- It inferred a current production failure from code risk and a stale `kal` example before obtaining a valid fixture.
- It initially treated direct `invoice_dimension.territory_key` matching as territory filtering even though that key comes from invoice `rep_number`. That violated the later product boundary that territory is assigned on customer/ship-to master data.
- It connected the ship-to casing defect to `wwjc`, even though `wwjc` ship-tos carry no territory assignments and therefore cannot exercise that defect.
- It confused Admin Console `view_dashboard` with the Sales Portal Dashboard gate.
- It called `PriceLevel.cue_character` “customer class.” That was factually wrong.
- It used drifting Current-YTD figures as if they were durable acceptance baselines.
- It layered Jira comments and Confluence corrections instead of replacing stale claims, leaving readers to reconstruct truth from chronology.
- It changed Sprint fields during review without first agreeing on board behavior, causing Brent to interpret disappearance from the board as deletion.

### Legitimate learning

- The admin short-circuit was verified rather than assumed.
- `betaverify` was corrected into a valid non-admin, blank-customer-number, six-territory fixture.
- The portal warehouse completed after the corrected assignments, and all six territories appeared in the filter.
- June 2026 was established as a stable period for `105:1 Gigi Lane`: 110 invoices, 75 accounts, `$123,585.35`.
- Direct rep-number matching was correctly removed from master-assignment territory semantics. On `wwjc`, it would add 29 invoices and `$43,093.69` outside the assigned-customer book while adding nothing for Gigi Lane.
- The Customers substring defect and CSV structure defect were isolated to concrete code.
- The ship-to casing mismatch was identified as a separate cross-org ETL defect rather than a `wwjc` blocker.

### Net value

The process cost confidence and time, but it did create reusable evidence discipline: a valid role fixture, an acceptance baseline, a clear product boundary, a reproducible Customers defect, and a list of access-model questions that should now be handled separately.

## 4. Bet A ticket-by-ticket disposition

| Ticket | Live state | Evidence verdict | Recommended disposition |
|---|---|---|---|
| [EBR-40](https://supercatsolutions.atlassian.net/browse/EBR-40) | Approved; no Sprint; unassigned | Product rule is valid, but the summary still says the filter “isn't working” while the valid primary route passed | Rewrite as verified product invariant and edge-validation decision; close if no failing edge case is found |
| [SERV-2447](https://supercatsolutions.atlassian.net/browse/SERV-2447) | To Do; no Sprint; unassigned | Primary June route passes; row count, empty assignment, multiple territory union, ship-to-assigned org, and case behavior not fully verified | Validate first; convert to focused regression/edge work only if a test fails; do not execute current broad refactor |
| [EBR-212](https://supercatsolutions.atlassian.net/browse/EBR-212) | Approved; no Sprint; unassigned | Primary Dashboard KPI route passes; Top-N is unverified; drill-through filter propagation is absent in source; SERV-1092 already Done | Reframe as residual Dashboard propagation/validation, not an unimplemented headline feature |
| [SERV-2448](https://supercatsolutions.atlassian.net/browse/SERV-2448) | To Do; no Sprint; unassigned | KPI reconciles with Invoices; destination links omit the selected filter; Top-N membership remains unverified | Reproduce the link behavior, fix propagation narrowly, and add regression coverage; do not refactor the resolver |
| [EBR-91](https://supercatsolutions.atlassian.net/browse/EBR-91) | Approved; no Sprint; unassigned | Demonstrated defect, but the current product scope mixes bug fixes with export enhancements | Keep; split required correction from optional export improvements |
| [SERV-2449](https://supercatsolutions.atlassian.net/browse/SERV-2449) | To Do; no Sprint; unassigned | Demonstrated UI and CSV defects; current acceptance invents unsupported export/product behavior | Replace the ticket wording, then build the narrowed package unless the authorization probe confirms exposure |

### Product model recovered from the newly accessible documentation

The earlier Bet A work was written as if the goal were to make an abstract reporting system mathematically uniform. That is not the Sales Portal product.

- The Sales Portal is the manufacturer's historical-sales workspace for **customers, sales reps, sales managers, and CSRs**, not an internal analytics-engineering console. Its records come from the manufacturer's ERP/accounting exports and its users work in customer accounts, orders, invoices, and territory books.
- On **Customers**, the primary object is the customer account. Search, sort, and filters decide which accounts appear. The totals at the top summarize the complete matching account set across all pages. Changing the date range changes the sales value shown; it does not remove customers merely because they had no sales in that period.
- Territory is the exceptional filter because it controls who may see sales. Bill-to and ship-to assignments define the rep's book. The warehouse refresh delay is part of the operating model and must be acknowledged during setup and support.
- Export is documented as the **same customer result in CSV form**. That supports making the page and export agree. It does not support inserting a non-tabular scope block or adding a totals row without a named customer workflow.
- The product intentionally distinguishes warehouse-calculated totals from individual imported amounts. Freight and surcharges can make them differ. “Make every number identical” is therefore not a valid acceptance principle.
- These clients are B2B furniture, lighting, and décor manufacturers/wholesalers. Their “customers” are dealer accounts, designers, contract buyers, distributors, and marketplaces—not consumers. A rep or sales manager picking Previous Month is trying to review account performance in their book, not configure a generic report schema.

Sources: the newly accessible [Sales Portal Behavior Design draft](https://supercatsolutions.atlassian.net/wiki/pages/resumedraft.action?draftId=1193246721), [Sales Portal Calculations](https://supercatsolutions.atlassian.net/wiki/spaces/SCKB/pages/1193246721/Sales+Portal+Calculations), [Accessing Sales Portal Data](https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/994279438/Accessing+Sales+Portal+Data), [Sales Territories](https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/336363531/Sales+Territories), [eCat Online Sales Portal](https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/142737411/eCat+Online+Sales+Portal), and `Insightful Product 4.0/knowledge/industry_context.md`.

### Why the current SERV-2449 “Done when” is wrong

| Current requirement | Product verdict |
|---|---|
| Every date range gets a selected-range column | Wrong. The behavior design says Current YTD and Previous Year are already represented by the standing sales columns; adding a duplicate column is noise. Other selected ranges should add the appropriate period value. |
| Total equals selected-range sales across all filtered customers | Directionally valid, but badly phrased. A sales manager expects the top number to summarize every account matching the current customer search/filter, not just the visible page. Preserve the documented bill-to/ship-to territory rules. |
| Export uses the same selected period | Valid and directly tied to the complaint. |
| Stable `Selected Range Sales` plus a scope block | Unsupported and risky. The current export uses a useful period-specific heading such as `Previous Month Sales`; a scope preamble can break normal CSV consumers. No named customer requested this redesign. |
| Export totals row | New feature, not bug repair. The original export contract is the same customer rows in CSV form. Validate with a real user before adding it. |
| Equal header/data field counts and every field labeled | Valid structural repair. Label the existing cue value `Price Level Cue`. |
| Unknown `date_range` falls back | Sensible defensive engineering, but not a customer-facing acceptance criterion and not evidence for enlarging this ticket. |
| Relabel calendar-year columns | Unnecessary for the reproduced defect. Preserve established CY/LY behavior unless a customer usability test demonstrates confusion. |

### Customer-aware replacement wording for EBR-91 / SERV-2449

**Problem**

Sales reps and sales managers use Customers to review account sales for their territory and export the same account list to Excel. When they choose a period such as Previous Month, the export includes that period's sales but the page does not show it. The CSV also contains an unlabeled price-level cue value.

**Done when**

1. On Customers, choosing Previous Month, Current Month, Previous YTD, Yesterday, Custom, or another range not already represented by the standing CY/LY columns shows that period's sales at the top and beside each customer.
2. The top period total covers every customer matching the current customer search and territory filter, not only the visible page.
3. Territory behavior stays consistent with the documented Sales Portal access model: bill-to access includes the customer account; ship-to-only access includes the applicable ship-to sales. Do not silently replace this with a new account-level rule.
4. Exporting produces the same customer set and selected-period sales as the page.
5. Keep the existing human-readable period heading, such as `Previous Month Sales`, unless a named client integration requires a stable machine header.
6. Every CSV row has the same number of fields as the header, and the existing cue-character field is labeled `Price Level Cue`.
7. Current YTD and Previous Year continue using the existing standing columns; do not add duplicate selected-period columns or change the revenue calculation in this fix.

**Not part of this bug fix**

- CSV scope/preamble block
- CSV totals row
- Generic `Selected Range Sales` header
- New date-range choices
- Revenue-definition changes
- Broad CY/LY relabeling

## 5. Production reproduction matrix

| Route | Fixture and period | Expected | Observed | Classification |
|---|---|---|---|---|
| Invoice territory total | `wwjc` / `betaverify` / Gigi Lane / June 2026 | `$123,585.35` | UI `$123,585` | **Passing production verification** |
| Invoice row count | Same | 110 invoices | Not visible/proven in supplied screenshot | **Unverified** |
| Dashboard KPI | `wwjc` / `betaverify` / Gigi Lane / Current YTD | Match Invoices | Both `$836,263` | **Passing production verification** |
| Dashboard Top Customers | Same | Every row belongs to selected customer/location book | Panel rendered; membership not checked | **Unverified** |
| Dashboard Top Products | Same | Product values derive only from selected book | Panel rendered; row scope not checked | **Unverified** |
| Dashboard drill-through | Same | Selected territory persists into target | Rails links omit `multi-select-filters` on Invoice, Order, Backlog, Top Customer, Top Tradename, and Top Collection destinations | **Code-confirmed propagation gap; production impact pending** |
| Customers Previous Month | Valid production login | Selected-period card and column appear | Both absent | **Live production defect** |
| Customers Previous YTD | Valid production login | Selected-period card and column appear | Both present | **Passing comparison that exposes gate bug** |
| Customers CSV structure | Source plus production export evidence | One heading per value | More values than headings | **Live/code-confirmed defect** |
| Empty territory assignment | Non-admin, no customer, no all-totals | Empty book, never org-wide | Not reproduced with `betaverify` | **Code/access risk; unverified** |
| Ship-to uppercase territory | Affected org with ship-to territory assignments | Bridge resolves case-insensitively | Code mismatch found; no current end-user route captured in this review | **Separate code/data defect** |

Current-YTD numbers are observations tied to capture time, not acceptance constants. June 2026 is the durable `wwjc` comparison period.

## 6. Remaining Bet A verification gaps

Before any SERV-2447 or SERV-2448 behavior change:

1. Capture invoice row count for Gigi Lane/June and reconcile the 110-invoice baseline.
2. Test one assigned territory and the union of multiple assigned territories.
3. Test `NULL`, empty string/array, and no territory assignment with no all-totals permission. Confirm fail-closed behavior.
4. Test an explicit selection for an all-totals user and confirm it narrows.
5. Use an organization whose ship-tos actually carry territory assignments; `wwjc` cannot validate ship-to behavior.
6. Test case differences in customer and ship-to territory codes.
7. Inspect each Top Customer against the selected master-assignment book.
8. Reconcile Top Product values to territory-scoped **orders/order lines**; the widgets use ordered amount/quantity, not invoice lines.
9. Reproduce the code-confirmed drill-through propagation gap and decide whether every destination should preserve `multi-select-filters`.
10. Check list rows, header totals, CSV/export, and detail routes separately; a matching KPI does not prove them all.

### Code and data verification ledger

| Claim | Verified source | Finding |
|---|---|---|
| Either admin column bypasses rep permissions | `app/models/org_user.rb:383-386`; `app/models/user_type_permissions.rb:117-123` | `OrgUser#is_admin?` returns true for the org-user flag or global `users.is_admin`; `may?` then returns true except for one limited-management permission |
| Sales Portal Dashboard gate | `app/helpers/ecat_permissions_helper.rb:54-59`; `app/controllers/ecat_dashboard_controller.rb:9-12` | The route uses `should_display_portal_dashboard?`, requiring customer visibility, the portal/org feature gate, user-type `enable_portal_dashboard`, and `display_sales_portal_totals`; Admin Console `view_dashboard` is not this gate |
| Dashboard sub-action authorization | `app/controllers/ecat_dashboard_controller.rb:9-72` at checked-out `d4a0e7d40` | Only `index` invokes the Dashboard-specific gate; KPI, graph, and Top-N actions do not. Commit `15aad6c52` on `origin/master` adds a general Sales Portal gate, not the stricter Dashboard gate. Validate deployed production before assigning implementation |
| Invoice/customer direct-record authorization | `app/controllers/ecat_invoices_controller.rb:32-35,54-66`; `app/controllers/ecat_customers_controller.rb:297-307` | Invoice show scopes by org but not the rep's warehouse book; email uses global `PortalInvoice.find(id)`; a rep without an associated customer is allowed to open any customer code. Direct-URL production validation is urgent |
| Permitted book | `app/services/warehouse/filter_items_by_territory_code_limit.rb:9-46` | All-totals users receive the entity unchanged; customer users are limited by customer; reps resolve through `RepDimension` → `RepToTerritoryBridge` → territory filter |
| Selected territory | `app/services/warehouse/get_invoices_for_invoices_page.rb:118-128`; `app/services/warehouse/filter_items_by_territory_code.rb:17-40` | Selection uses customer and ship-to bridges; direct `territory_key` is added only when `territory_access_via_rep_number` is enabled |
| Legacy all-totals short-circuit | `app/models/warehouse_access.rb:424-429` | `territory_code_limit_subquery` returns literal `true` for all-totals users. This is a code risk on legacy callers, not proof that the current Invoice or Dashboard route fails |
| Empty rep bridge behavior | `filter_items_by_territory_code_limit.rb:28-46`; `filter_items_by_territory_code.rb:17-40` | The relation-based path appears to filter against an empty territory subquery rather than intentionally widen. `territories.nil?` widens, but the rep path passes a relation. A production/test assertion is still required before calling fail-closed behavior proven |
| Collapsed NULL ship-to key | `app/services/warehouse/extracts_and_transforms/format.rb:19-23`; `filter_items_by_territory_code.rb:29-39` | A blank ship-to makes `ship_to_key == customer_key`; the OR predicate does not exclude collapsed keys. A ship-to bridge can therefore match a fact with no actual ship-to. Commit `5e87df1b4` attempted a guard, but it is absent from checked-out HEAD and current `origin/master` service code |
| Ship-to casing mismatch | `app/services/warehouse/extracts_and_transforms.rb:11-42`; `.../territory_to_ship_to_bridge.rb:19-40` | Enumerated territory codes are downcased, while the shipping-location map stores raw `sl.territory_codes` keys and is queried with the downcased code |
| Customers selected-period gate | `app/controllers/ecat_customers_controller.rb:293-295` | `params['date_range']['previous_ytd'] || params['date_range']['custom']` is Ruby string indexing, not equality/membership. It happens to be truthy only when those substrings occur |
| CSV structural defect and cue semantics | `app/services/controllers/ecat_customer.rb:15-42,129-134`; `test/services/controllers/ecat_customer_test.rb:12-90` | Headers contain 8/9 values while rows contain 9/10; the extra value is looked up from `PriceLevel.code → cue_character` using `customer.default_price_code`. Existing tests encode the mismatch instead of rejecting it |
| CY/LY semantics | `app/services/controllers/ecat_customer.rb:113-126`; `app/models/warehouse_access.rb:1181-1189` | CY and LY are calendar-based report ranges; selected-period totals are a separate calculation |
| Dashboard drill-through | `app/views/ecat_dashboard/_graph.html.erb:109-129`; `_index_content.html.erb:11-15`; `_top_customers.html.erb:23-41`; `_top_tradenames.html.erb:23-47`; `_top_collections.html.erb:27-50` | Destination links omit the selected `multi-select-filters`. This is a code-confirmed propagation gap; the exact user-visible result still needs a production walkthrough |
| Dashboard measure contract | `app/models/ecat_reporting/reports/dashboard.rb:21-33,46-76,107-118` | Invoice KPI and Top Territory use invoiced amount; Top Customer and Top Product use ordered amount. This may be intentional, but “same number everywhere” is not the current product contract |
| Top Territory attribution | `app/services/warehouse/get_sales_facts_for_invoices_by_territory.rb:46-56,78-82` | Records admitted through invoice `rep_number` are grouped through customer territory bridges, so Top Territories can omit or misattribute rep-number-only access. Keep this with the EBR-180 path, not master-assignment Bet A |
| Invoice row/total amount contract | `app/models/ecat_reporting/invoices/invoice.rb:43-61,210-225` | Rows expose invoice-dimension header `net_amount`; Invoice Total sums line-derived `amount_invoiced`. Both share scope, but amounts can differ when header and lines differ |
| `betaverify` | Read-only production SQL and 2026-08-04 walkthrough | Non-admin on both columns, blank customer number, dedicated type, six separate territories; warehouse refresh followed the corrected assignment |
| Closed-period baseline | Read-only production SQL | Gigi Lane, June 2026: 110 invoices, 75 accounts, `$123,585.35`; use this instead of drifting YTD |

## 7. Live Sales Portal Jira inventory

This inventory includes tickets with a direct Sales Portal reporting, territory, totals, or export relationship found in the live Jira search and local program corpus. Broad keyword matches that were actually iPad/Admin work—such as SERV-2453 through SERV-2455 and SERV-2457/2458—were inspected and excluded.

| Product | Engineering | Live state | Evidence / relationship | Recommendation |
|---|---|---|---|---|
| EBR-7 | SERV-747 | EBR Triaging; SERV Done | Line-item discount import/display/calculation request; implementation history exists, but this review did not rerun the full acceptance criteria | Verify before closure |
| EBR-40 | SERV-2447 | Approved / To Do | Explicit link; primary route passes | Validate edges, then close or narrow |
| EBR-87 | none confirmed | Triaging | Product request remains data/client-specific; no live Jira link to SERV-2214 | Validate client and data readiness; shape only if still wanted |
| EBR-91 | SERV-2449 | Approved / To Do | Explicit link; demonstrated production defect | Build narrowed fix now |
| EBR-180 | SERV-2178 | EBR Triaging; SERV In Progress, assigned to Brent | Explicit product boundary; comma-separated invoice/order rep numbers require schema/import/ETL many-to-many work; EBR also has active CSP-52 context | Explicit continue/narrow/pause decision; do not bury inside Bet A |
| EBR-212 | SERV-1092 (Done); SERV-2448 (To Do) | Approved / mixed | SERV-1092 is completed predecessor; SERV-2448 is residual/possible duplicate-regression package | Preserve history; validate residual gaps |
| EBR-474 | none confirmed | Triaging | Duplicate/overlapping Savoy invoice-status product demand with EBR-601; no confirmed SERV implementation link | Product owner chooses canonical record |
| EBR-601 | none confirmed | Waiting for Client | Duplicate/overlapping Savoy invoice-status product demand with EBR-474; awaiting client evidence | Keep waiting or consolidate; do not invent an implementation link |
| EBR-772 / EBR-776 | none in this reset | Submitted/parked in program docs | LLM/agentic layer, downstream of trusted computation | Park; outside Sales Portal backlog reset |
| none located | SERV-2196 | To Do | Live Savoy over-access report: ship-to territory can grant invoice visibility despite bill-to semantics | Product decision and prevalence audit before fix |
| none located | SERV-2214 | To Do | Dashboard calculation work located in the broader search, but not linked to EBR-87 | Inspect and shape independently; no inferred EBR pairing |
| none located | SERV-2431 | Ready to Accept | `invoice_data.csv` rejects missing optional `OrderNumber`; concrete importer/schema contradiction | Run acceptance; close if optional-field import now passes |
| none located | SERV-2111 | Done | Historical missing-invoice warehouse reconciliation | Precedent only; not an open Bet A dependency |
| none located | SERV-2179 | Done | Ship-to territory dropdown work; comments confirm warehouse timing affects observations | Preserve as regression/history context |
| none located | SERV-2199 | Done | Direct-URL permission enforcement precedent | Reuse its authorization pattern when validating current detail routes |
| none located | SERV-2224 | Done | Open-order Dashboard totals | Historical implementation; verify before filing a duplicate |
| none located | SERV-2251 | Done | Complete-order visibility | Historical implementation; verify before filing a duplicate |
| none located | SERV-2001 | Historical/archived | Reported lag traced to warehouse ETL timing | Working-as-designed precedent, not an active filter defect |
| none located | SERV-2138 | Archived/weak evidence | Investigation ended without a stable reproduction or cause | Do not cite as fixed or as proof of a current defect |

### Explicit exclusions

- SERV-2453: matrix-options sequence overflow—system import issue, not Sales Portal.
- SERV-2454: broad database key migration—not Sales Portal.
- SERV-2455: sandbox settings clone—not Sales Portal.
- SERV-2457 and SERV-2458: iPad/Admin order export data repairs—not Sales Portal imported-order reporting.
- SERV-2397: iPad kit-options bug, not Savoy Sales Portal invoice status.
- SERV-2213: iPad presentation/layout request, not Sales Portal order totals.
- SERV-2217: order quantity/pack-size work and already Done, not Sales Portal currency.
- Generic Dashboard redesign, Insightful, eCat Online, and iPad work are outside this portfolio unless a concrete Sales Portal path is shown.

## 8. EBR↔SERV relationship and orphan map

### Explicit pairs

- EBR-40 ↔ SERV-2447
- EBR-91 ↔ SERV-2449
- EBR-180 ↔ SERV-2178
- EBR-212 ↔ SERV-1092, with SERV-2448 as a later Bet A follow-up

### Product orphans

- EBR-87, EBR-474, and EBR-601 have no confirmed engineering link in this review.
- EBR-772/776 intentionally have no implementation in this portfolio.
- Any product request for ship-to casing normalization was not located as a clean EBR/SERV pair. Do not hide it inside EBR-40.

### Engineering orphans

- SERV-2196 has a concrete production access report but no clear EBR product decision about bill-to versus ship-to precedence, compatibility, or rollout.
- SERV-2214 is relevant Dashboard calculation work but has no confirmed product pairing in the reviewed relationship set.
- The direct-record/Dashboard authorization risks found in source have no confirmed current Jira owner. Search SERV-2199 history before creating a new engineering record.
- SERV-2431 is implementation-first and awaiting acceptance without a located EBR product parent.

### Relationship quality

| Relationship | Quality |
|---|---|
| EBR-91 ↔ SERV-2449 | Strong and reproduced, although scope should be narrowed |
| EBR-40 ↔ SERV-2447 | Strong explicit link; defect premise now false on primary route |
| EBR-212 ↔ SERV-2448 | Explicit but historically incomplete because SERV-1092 is the completed predecessor |
| EBR-180 ↔ SERV-2178 | Strong but intentionally separate and XL |
| EBR-474 ↔ EBR-601 | Strong product-level duplicate/overlap; no engineering relationship established |
| SERV-2196 without EBR | Unsafe to implement before product semantics and prevalence are decided |

## 9. Root-cause and theme clustering

### Cluster A — Customers selected-period presentation and CSV contract

- **Tickets:** EBR-91 / SERV-2449
- **Foundation:** Customers controller/view date-range gating and CSV row/header construction
- **Why together:** same surface, same request parameters, same focused tests
- **Does not include:** territory bridges, Dashboard, rep-number identity
- **Evidence:** directly reproduced in production and source

### Cluster B — Territory regression and Dashboard propagation

- **Tickets:** EBR-40/SERV-2447 and residual EBR-212/SERV-2448
- **Foundation:** warehouse permission book, selected-territory narrowing, Dashboard query propagation
- **Why together:** one fixture can verify shared invariants; code already shows drill-through links drop the selected filter, but that does not justify rewriting the underlying territory resolver
- **Does not include:** invoice `rep_number`, ship-to ETL normalization, Customers period display
- **Evidence:** primary routes pass; drill-through propagation gap is code-confirmed; other edge routes remain unknown

### Cluster C — Customer/ship-to access semantics

- **Tickets:** SERV-2196 plus a missing product decision
- **Foundation:** customer and shipping-location bridges and invoice visibility
- **Why separate:** this is an authorization/precedence decision with backward-compatibility risk, not a filter UI bug
- **Evidence:** concrete Savoy production report in Jira; prevalence and dependency behavior not yet audited

### Cluster D — Ship-to territory normalization

- **Tickets:** new dedicated product/engineering pair required
- **Foundation:** ETL normalization in `all_territory_codes_for_organization` and `TerritoryToShipToBridge`
- **Why separate:** a case-normalization defect can cause false negatives across affected orgs, but `wwjc` cannot reproduce it
- **Evidence:** code/data discovery; affected-org user reproduction still needed

### Cluster E — Invoice/order rep-number identity

- **Tickets:** EBR-180 / SERV-2178
- **Foundation:** import schema, portal order/invoice models, warehouse schema, ETL many-to-many mapping
- **Why separate:** explicitly different product meaning and XL implementation
- **Evidence:** comma-separated values unsupported; engineering already identified schema-wide impact

### Cluster F — Reporting trust outside Bet A

- **Tickets:** EBR-474/601; EBR-7/SERV-747; EBR-87; orphan SERV-2214
- **Foundation:** status semantics, established revenue math, territory-master completeness
- **Why not one bet:** these have different root causes. They belong in the same portfolio review, not the same code package.

### Cluster G — Direct-route authorization

- **Tickets:** no confirmed new pair; SERV-2199 is completed precedent
- **Foundation:** controller authorization callbacks and warehouse-authorized record lookup
- **Why separate:** this is access containment, not report-filter correctness
- **Evidence:** checked-out source permits Dashboard sub-action and record-detail paths without the expected specific gate/scope; deployment and production behavior require a direct-URL probe

### Cluster H — Reporting amount contracts

- **Tickets:** product decision required
- **Foundation:** invoice header `net_amount`, line-derived `amount_invoiced`, and Dashboard ordered-versus-invoiced measures
- **Why separate:** identical filter scope does not require every metric to use the same business measure
- **Evidence:** deterministic source difference; no demonstrated June mismatch

## 10. Duplicate, stale, invalid, and already-fixed list

### Duplicate

- EBR-474 and EBR-601 describe the same Savoy invoice-status problem. Keep one canonical product ticket; no engineering implementation link was confirmed.
- SERV-2448 overlaps completed SERV-1092. It is not necessarily a literal duplicate, but its residual scope must be stated before engineering begins.

### Stale

- Current-YTD figures around `$777k`, `$808k`, `$830k`, and `$836k` were valid at different capture times. None is a permanent baseline.
- Confluence pages that say no Bet A production AC has executed are stale after the `betaverify` walkthrough.
- The claim that the `wwjc` build must wait for ship-to casing is stale and wrong.
- The claim that `betaverify` is malformed or unavailable is stale.

### Invalid

- Admin captures as evidence of rep restrictions.
- `view_dashboard` as the Sales Portal Dashboard gate.
- “Customer class” as the unlabeled CSV field.
- Ship-to casing as the cause of the `wwjc` result or the old `kal/0016` claim.
- Direct invoice-rep matching as the definition of customer/location territory.

### Already fixed or implemented

- SERV-1092 is Done for Dashboard territory filtering.
- SERV-747 is Done for discount-related work associated with EBR-7, but EBR-7's complete import/display/calculation acceptance still needs verification.

## 11. Recommended disposition for every relevant ticket

| Ticket | Disposition |
|---|---|
| EBR-7 | Rerun its line-item discount import/display/calculation acceptance; close only if all pass |
| SERV-747 | Leave Done |
| EBR-40 | Replace bug assertion with passed primary route plus named edge gaps; close if edge tests pass |
| SERV-2447 | Validate first; no broad behavior refactor without a failing test |
| EBR-87 | Validate client demand and data readiness; no implementation pairing is established |
| SERV-2214 | Inspect independently as orphan Dashboard calculation work; do not infer an EBR-87 pairing |
| EBR-91 | Keep and narrow to required correctness |
| SERV-2449 | Build now as the first package |
| EBR-180 | Product owner must reconcile Triaging state and CSP-52 context with active engineering |
| SERV-2178 | Brent/Kylor decide continue, narrow, or pause in light of the documented XL scope; currently In Progress |
| EBR-212 | Reframe as residual acceptance after SERV-1092 |
| SERV-1092 | Leave Done; cite as predecessor |
| SERV-2448 | Narrow to the code-confirmed drill-through propagation gap plus Top-N/regression validation; do not retain the broad resolver premise |
| EBR-474 | Resolve as duplicate/overlap with EBR-601; likely non-canonical, subject to product-owner review |
| EBR-601 | Preserve Waiting for Client unless evidence arrives; choose as canonical only through an explicit product decision |
| SERV-2196 | Validate prevalence and decide precedence/compatibility before build |
| SERV-2214 | Inspect as an engineering orphan and either link to the correct product decision or close/reshape |
| SERV-2431 | Complete acceptance for optional `OrderNumber`; close if the import now passes |
| SERV-2111 / 2179 / 2199 / 2224 / 2251 | Leave Done; use as regression and duplicate-check history |
| SERV-2001 | Leave historical/working-as-designed unless fresh ETL-lag evidence appears |
| SERV-2138 | Leave archived; do not cite its inconclusive investigation as proof |
| EBR-772/776 | Park outside this program lane |
| Ship-to casing discovery | Create a dedicated pair only after reproducing on an affected org |
| Direct-route authorization discovery | Validate immediately against deployed production; link to SERV-2199 history or create a dedicated pair manually if reproduced |
| Invoice/Dashboard amount contract | Product decision first; no calculation change until user-visible variance and intended semantics are established |

## 12. Proposed replacement bet portfolio

### Bet 0 — Portal authorization containment

- **User problem:** a logged-in rep may be able to address Dashboard data or individual invoice/customer records outside the intended territory book.
- **Business value:** prevents cross-territory or cross-organization data exposure.
- **Included:** direct-URL validation; a new or correctly linked product/engineering record after checking SERV-2199 history.
- **Foundation:** controller gates, current-organization scoping, warehouse-authorized detail relations.
- **Evidence:** code-demonstrated missing specific checks at checked-out `d4a0e7d40`; `origin/master` has a newer general portal gate but not the full Dashboard/detail authorization.
- **Uncertainty:** deployed revision and whether upstream routing/other callbacks block the demonstrated path.
- **Fixture:** non-admin `betaverify`, a known unassigned `wwjc` invoice/customer, and a user type with Dashboard gate false.
- **Acceptance:** direct identifiers and Dashboard sub-actions return deny/not-found without leaking record content; email lookup is org- and territory-scoped.
- **Sequence/size/confidence:** immediate probe; small/medium repair; high code confidence, production impact unconfirmed.
- **Recommendation:** **Validate immediately; build before Bet 1 if reproduced.**

### Bet 1 — Customers period and export correctness

- **User problem:** Customers hides selected-period sales for valid ranges and exports unlabeled data.
- **Business value:** Restores trust in a visible reporting/export surface with low change risk.
- **Included:** EBR-91; narrowed SERV-2449.
- **Foundation:** Customers date-range predicate, view/table/card rendering, CSV headings and values.
- **Evidence:** Production reproduction plus direct source diagnosis.
- **Uncertainty:** The older behavior design's bill-to/ship-to row rules conflict with the later Bet A PO comment that territory only selects accounts. Resolve that conflict before changing row-level territory math. Also confirm whether any customer automation depends on the existing range-specific CSV headings.
- **Fixture:** A non-admin sales rep or manager with a real territory book and data in Previous Month plus one other non-standing range; `wwjc/betaverify` is suitable for behavior, while the original CLM requester should be used for workflow validation if available.
- **Acceptance:** ranges not already represented by the standing CY/LY columns show the selected period on the page; the top total covers the complete matching customer set; export carries the same customers and period; header/data counts match; cue character is labeled `Price Level Cue`.
- **Sequence/size/confidence:** First; small; high.
- **Recommendation:** **Rewrite, then build.** Remove the scope block, totals row, generic header, and other unrequested redesign from the bug.

### Bet 2 — Territory regression hardening

- **User problem:** We lack trustworthy proof for edge behavior even though the primary routes pass.
- **Business value:** Prevents access leakage/false negatives without funding speculative refactoring.
- **Included:** residual SERV-2447 and SERV-2448.
- **Foundation:** test fixtures around warehouse permission book, selection narrowing, Dashboard propagation.
- **Evidence:** Happy-path totals pass; drill-through filter propagation is missing in source; other edge cases remain open.
- **Uncertainty:** Production impact of dropped drill-through filters and whether any underlying resolver defect remains.
- **Fixture:** `betaverify` plus one empty-assignment user and one ship-to-assigned affected org.
- **Acceptance:** matrix in section 6, including rows/totals, order-based Top-N, and preserved drill-through filters.
- **Sequence/size/confidence:** Second; small if tests only, medium if a defect is found; medium.
- **Recommendation:** **Validate first.** Merge only at the test/acceptance level; split any behavior fixes by root cause.

### Bet 3 — Customer/location access semantics

- **User problem:** A ship-to assignment may grant access to invoices contrary to expected bill-to semantics.
- **Business value:** Correct authorization while avoiding surprise loss of access for existing customers.
- **Included:** SERV-2196 and a new product decision.
- **Foundation:** customer and ship-to bridge membership and invoice visibility.
- **Evidence:** Concrete Savoy report.
- **Uncertainty:** Prevalence, clients relying on current behavior, exact precedence.
- **Fixture:** `shl` customer 70461 / invoice INV1446401 or a safe equivalent.
- **Acceptance:** explicit bill-to/ship-to matrix with compatibility rollout.
- **Sequence/size/confidence:** After prevalence audit; medium; medium.
- **Recommendation:** **Validate first, then split rollout from semantics.**

### Bet 4 — Ship-to bridge normalization

- **User problem:** Case differences can silently omit ship-to territory bridge rows.
- **Business value:** Removes false negatives for affected orgs.
- **Included:** new dedicated tickets; not EBR-40.
- **Foundation:** ETL normalization and bridge tests.
- **Evidence:** Source/data discovery; `wwjc` excluded.
- **Uncertainty:** User-visible impact per affected org.
- **Fixture:** one org with uppercase ship-to territories and known invoices.
- **Acceptance:** normalized bridge membership and before/after invoice visibility without widening unrelated access.
- **Sequence/size/confidence:** After reproduction; small/medium; medium-high code confidence, lower product-impact confidence.
- **Recommendation:** **Validate first, then build separately.**

### Bet 5 — Multi-rep invoice/order identity

- **User problem:** comma-separated invoice/order rep numbers cannot grant access to every intended rep.
- **Business value:** Supports a specific advanced access model.
- **Included:** EBR-180/SERV-2178 only. SERV-2180 is archived master-assignment/bridge history and is not the comma-separated invoice `RepNumber` implementation.
- **Foundation:** database schema, import, ETL, and warehouse many-to-many identity.
- **Evidence:** unsupported input shape is confirmed; size is XL.
- **Uncertainty:** breadth of customer demand and cheaper upstream alternatives.
- **Fixture:** Savoy or another committed client with multi-rep records.
- **Acceptance:** import, storage, ETL, access, and deduplicated totals across multiple rep numbers.
- **Sequence/size/confidence:** Later; large/XL; medium.
- **Recommendation:** **Park until explicitly funded.**

### Bet 6 — Invoice and Dashboard measure contract

- **User problem:** users can reasonably assume a row amount, page total, and similarly named Dashboard ranking use the same measure when source says they do not.
- **Business value:** prevents false reconciliation promises and support disputes.
- **Included:** product decision and focused tests; no automatic calculation change.
- **Foundation:** invoice header `net_amount`, line-derived sales facts, Dashboard `amount_ordered`/`amount_invoiced`.
- **Evidence:** deterministic source differences.
- **Uncertainty:** which differences are intentional and whether real clients show material variance.
- **Fixture:** invoices with discounts, freight, credits, and header/line differences.
- **Acceptance:** labels define each measure; rows and totals either reconcile or explicitly disclose different contracts.
- **Sequence/size/confidence:** validate after urgent correctness work; small decision, potentially medium implementation; high.
- **Recommendation:** **Validate first; do not merge into territory work.**

## 13. Recommended first engineering package

First run the same-day authorization probe in Bet 0. If a non-admin can retrieve unassigned data, the focused authorization hotfix becomes the first engineering package.

If the probe does not reproduce exposure, start with a deliberately narrower SERV-2449:

1. Replace the accidental substring condition with the documented Customers-page policy: Current YTD and Previous Year use their standing columns; other selected periods render an additional period value.
2. Prove Previous Month first because it is the reproduced customer-visible failure; cover the remaining non-standing ranges as regression cases.
3. Keep the page customer-first: date changes values, not which accounts appear.
4. Keep export aligned to the same customer set and selected period, preserving the existing range-specific heading unless a named integration requires otherwise.
5. Add the missing CSV heading as `Price Level Cue` and assert every row has the header's field count.
6. Preserve current calculation sources and established CY/LY behavior.

Do **not** include a totals row, scope block, generic `Selected Range Sales` header, broad relabeling, revenue rewrite, or territory refactor in this bug. Those ideas were not grounded in the reported customer workflow.

## 14. Work to park or close

- Make an explicit continue/narrow/pause decision on active EBR-180/SERV-2178; do not silently park or continue an XL path.
- Park EBR-772/776 and all LLM/Intelligence work until computational reporting is trusted.
- Verify EBR-7's complete discount behavior before closure.
- Resolve EBR-474 versus EBR-601 at the product level; no SERV implementation was confirmed.
- Close or reclassify EBR-40/SERV-2447 and EBR-212/SERV-2448 if the edge matrix passes.
- Do not fund a shared territory resolver solely because duplicate code exists.
- Do not fund `wwjc` ship-to casing work; that fixture cannot exercise the defect.

## 15. Jira and Confluence contradiction audit

### Live Jira

- **EBR-40 summary/status:** still presents a current broken Invoice filter and remains Approved, while the valid primary route passes.
- **SERV-2447 description:** still says no user-visible failure has been reproduced and proposes unification; it now needs the stronger update that the primary non-admin route passed.
- **SERV-2447 comment 38270:** confidently interprets direct territory-key matching and the stale `kal` route; later evidence/product decisions supersede it.
- **Comment 38275:** incorrectly links ship-to casing to the working diagnosis and endorses behavior work before valid reproduction.
- **Comment 38279:** accurately retracts a headline reproduction but is based on an admin/all-totals shape and should not be used as rep acceptance.
- **Comment 38287:** reasserts the current problem and embeds stale YTD values plus the irrelevant `wwjc` ship-to diagnosis.
- **Comment 38290:** correctly explains the either-admin-column problem, but its fixture recommendation changed later.
- **Comment 38300:** correctly fixes Dashboard gating, direct rep-number scope, ship-to applicability, and stable-period use. Its original statement that all three SERV Sprint fields were cleared was false when posted because SERV-2449 remained in June. Live Jira now shows all three with no Sprint, so the operational state has since caught up.
- **SERV-2448:** “looks correct” language is directionally honest but must now record the valid KPI pass and exact remaining gaps.
- **SERV-2449:** any “customer class” wording is wrong; the field is `PriceLevel.cue_character` and should be called `Price Level Cue`. Its current “Done when” is overdesigned and conflicts with the recovered Sales Portal behavior.

### Confluence

- **1819836417 — Filter Truth AC:** treats the three tickets as one Bet A and says acceptance has not executed. Update to split SERV-2449 from territory validation and record the two primary passes.
- **1819869185 — Eng Handoff/code map:** the broad implementation premise is stale. Remove direct rep-number narrowing from customer/location territory and do not present casing as a `wwjc` dependency.
- **1819901953 — Verification & Evidence:** admin captures and old Current-YTD values must be labeled historical/invalid or removed from the current-evidence section. Add the June pass and Dashboard KPI pass.
- **1820262402 — Eng Implementation Plan:** do not instruct engineering to implement the original unified package. Replace with SERV-2449 first and edge validation before territory changes.
- **Footer comment 1820655618:** the partial correction remains internally contradictory if it still says the build is blocked on casing while also acknowledging `wwjc` is unaffected. Replace the whole correction, not another nested comment.
- **Sales Portal Behavior Design / Sales Portal Calculations:** these older product documents contain the missing mental model. Customers is account-first; Current YTD and Previous Year are standing columns; export mirrors the HTML result; totals are warehouse line calculations while individual imported amounts can differ. The Bet A pages must not silently override those rules.
- **Revenue contradiction:** EBR-91 comments call `SUM(portal_invoices.net_amount)` the “spine,” while [Sales Portal Calculations](https://supercatsolutions.atlassian.net/wiki/spaces/SCKB/pages/1193246721/Sales+Portal+Calculations) says Customer sales totals use warehouse `QuantityInvoiced × UnitPrice`. Preserve current production math until this is deliberately reconciled; a coincidental matching baseline is not a product decision.
- **Territory contradiction:** [Sales Territories](https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/336363531/Sales+Territories) says bill-to access includes everything for that customer while ship-to-only access includes the applicable ship-to path. SERV-2449 comment 38277 instead says territory only selects the account set and every row shows the account's full sales. Re-open that decision before changing row totals.
- **Export inventions:** the scope block, totals row, and generic stable header came from the Bet A question/answer loop, not the client complaint or established export contract.

## 16. Exact correction queue for Kylor to apply manually

Apply one coordinated pass; do not add a new layer of commentary before descriptions/pages are corrected.

1. **EBR-40:** change summary/lead to “Invoice territory filter — primary route verified; edge cases pending.” Record Gigi Lane/June pass and the unverified 110-row count. Remove any assertion of a current headline failure.
2. **SERV-2447:** replace the opening problem and implementation instruction. State: primary non-admin route passes; no behavior change is authorized until an edge test fails. Retain the product boundary excluding invoice `rep_number`.
3. **EBR-212:** cite SERV-1092 as the completed predecessor. State that 2026-08-04 KPI reconciliation passed, Top-N membership is unverified, and destination links omit the selected filter.
4. **SERV-2448:** narrow to production reproduction and repair of drill-through filter propagation plus Top-N/regression validation. Remove any implication that the primary KPI currently fails.
5. **EBR-91/SERV-2449:** replace the entire acceptance block with the customer-aware wording in section 4. Replace “customer class” with `Price Level Cue`; remove the scope block, totals row, generic header, duplicate selected columns for Current YTD/Previous Year, broad relabeling, and unknown-range fallback from customer-facing acceptance.
6. **Sprint statement:** if comment 38300 remains, clarify that the “all three cleared” statement became true only after SERV-2449 was later cleared. Close the stale June 2026 Sprint through normal human board administration.
7. **Confluence 1819836417:** replace unified Bet A status with three ticket dispositions and the current reproduction matrix.
8. **Confluence 1819869185:** remove the shared-refactor mandate, direct rep-number matching, and `wwjc` casing dependency.
9. **Confluence 1819901953:** make the latest valid non-admin evidence the first section; label admin captures invalid; freeze June baseline and timestamp Current-YTD observations.
10. **Confluence 1820262402:** replace build plan with SERV-2449 first, territory edge validation second.
11. **Footer 1820655618:** replace the contradictory comment in one human-approved correction; do not append another correction chain.
12. **EBR-7:** rerun line-item discount import, display, and calculation acceptance before deciding closure.
13. **EBR-474/601:** choose one canonical product record after reviewing the waiting-client evidence; do not attach SERV-2397.
14. **SERV-2196:** create/attach a product decision before implementation.
15. **Ship-to casing:** create a dedicated issue only after an affected-org production reproduction is attached.
16. **Authorization:** inspect SERV-2199's completed scope, then test Dashboard sub-actions, invoice show/email, and customer detail with a non-admin outside the target book. Draft a dedicated correction/issue only if the deployed route reproduces.
17. **SERV-2431:** assign human acceptance for the optional `OrderNumber` import case.
18. **Amount contract:** do not promise “same number everywhere.” Decide and document header net, line invoiced, and ordered-ranking semantics before creating work.
19. **Authority documents:** add the four recovered product pages to the review source list and require future ticket changes to identify whether they preserve or intentionally supersede each documented behavior.

## 17. Process postmortem

### Why invalid evidence survived

The review began with ticket shaping and explanation-writing before proving that the test user could exercise the authorization path. Because screenshots looked plausible, fixture validity was treated as a detail instead of a gate.

### Why admin behavior was not tested first

The process lacked a role matrix. Nobody first wrote down the two admin columns, customer-number shape, territory assignments, permission flags, and warehouse timestamp. The correct test order was available from code but was not made mandatory.

### Why sources diverged

Local Markdown, Jira descriptions, Jira comments, Confluence bodies, and Slack drafts were all allowed to function as truth. Corrections landed in whichever surface was convenient. Readers then had to understand chronology to know which sentence won.

### Why layered comments failed

Comments are append-only history, not a durable specification. Each new comment fixed only part of the previous claim and sometimes introduced another error. The result was technically rich but operationally unusable.

### Why Sprint changes confused Brent

Sprint membership was changed as “hygiene” while Brent was using the board as his work view. The process did not distinguish deleting work from removing a board field, nor did it verify all three records before announcing completion.

### Why external AI edits became hard to control

The AI was optimizing for completion across multiple systems instead of a single approved change set. Each partial correction created another external artifact attributable to Kylor.

### Why changing fixtures invalidated drafts

User types, admin status, and territories changed while explanations and acceptance text were already being written. Evidence was not bound to a fixture snapshot and warehouse timestamp.

### Why inference was overstated

Code smells, SQL baselines, stale reproduction, and live behavior were not labeled as different evidence classes. A plausible code path was described as the user-visible cause before it failed a production test.

### Lightweight operating process

1. **One source of truth:** one PM review file named in every Jira/Confluence correction until the ticket is ready for engineering.
2. **Evidence labels:** `PROD-REPRO`, `PROD-PASS`, `SQL-BASELINE`, `CODE-RISK`, `UNTESTED`, `STALE`, `PROCESS`.
3. **Fixture gate:** record org, username, both admin columns, customer number, user type, flags, territory array, and warehouse timestamp before capture.
4. **Reproduce before rewrite:** no bug-description rewrite or implementation plan until the primary route is run with a valid role.
5. **Stable baseline:** use a closed period for acceptance; timestamp Current-YTD observations.
6. **Product before engineering:** EBR decides semantics and scope; SERV describes implementation only after that decision.
7. **Human approval:** Kylor reviews one proposed Jira/Confluence change set; the agent does not post it.
8. **One correction pass:** replace stale descriptions/page bodies, then add at most one concise historical note.
9. **Board-change protocol:** announce intended Sprint/status changes and verify every issue before telling Brent they are complete.
10. **Pre-send checklist:** fixture valid, screenshot readable, counts/totals independently checked, stale numbers removed, links tested, Sprint state verified, no product term invented.

## 18. Plain-English CTO briefing

Bet A should not go to engineering as written. We finally tested its two territory claims with a real non-admin rep account. The Invoice total matched the June database baseline, and the Dashboard total matched Invoices. That means the main SERV-2447 and SERV-2448 failures were not reproduced. Source does show a smaller Dashboard defect candidate: drill-through links drop the selected territory filter. Reproduce and fix that narrowly; separately test empty assignments, ship-to territories, and Top-N panels. None of this supports the original broad resolver refactor.

One small defect is real: Customers hides selected-period sales for ranges such as Previous Month because of a bad string check, and its CSV writes an unlabeled price-level cue value. The existing ticket is not ready, however: it adds a scope block, totals row, generic header, duplicate period columns, and relabeling that were never grounded in a customer workflow. Rewrite it around how reps and managers actually use the customer list, then fix the display and malformed CSV. Before it starts, run a short direct-URL authorization probe; confirmed exposure would outrank the reporting fix.

The review also found separate access work: a Savoy bill-to/ship-to authorization question, a case-normalization bug in ship-to territory ETL, and an XL multi-rep-number design. They should be separate decisions, not folded into Bet A.

The process failure was evidence control. We used admin accounts, changed fixtures midstream, and spread corrections across Jira, Confluence, and comments. Going forward, one review file, one frozen fixture, closed-period baselines, explicit evidence labels, and one human-approved correction pass should prevent a repeat.

## 19. Short Slack message to Brent

> I reset Bet A against the valid non-admin production test. SERV-2447’s June Invoice route passed (`$123,585` UI vs `$123,585.35` SQL) and SERV-2448’s Dashboard KPI matched Invoices (`$836,263` each). Source shows a focused drill-through gap, not evidence for the broad resolver refactor. I also rechecked SERV-2449 against the actual Sales Portal product docs: the display bug and malformed CSV are real, but the current acceptance invents a scope block, totals row, generic header, and other changes customers did not ask for. It needs a rewrite before engineering—show the selected period where the page design calls for it, export the same customer list/period, and label `Price Level Cue`. One direct-URL authorization probe comes first; confirmed out-of-book access would take priority.
