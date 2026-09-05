# Sales Portal foundation exit gate and Brent queue

**Date:** 2026-08-04  
**Decision:** Unified Bet A is retired. Finish the bounded foundation lane below, then move to Bets B–F.  
**Safety:** Jira and Confluence are read-only; all ticket bodies, notes, and transitions below are drafts for Kylor.

## 1. Final exit gate

The foundation lane is complete when:

1. the net-new direct-record authorization package is shipped and its denial/passing controls pass;
2. EBR-91/SERV-2449 is shipped with the narrow Customers contract below;
3. SERV-2196 ships the selected hybrid territory model, including the collapsed-blank-ship-to-key prerequisite and staged migration for ambiguous existing data;
4. SERV-2431 is accepted or returned with one named failure;
5. EBR-40/SERV-2447 and EBR-212/SERV-2448 are closed with the passing-route notes below;
6. EBR-7 is accepted or explicitly declined; EBR-474 is deduplicated into waiting EBR-601; EBR-180/SERV-2178 is explicitly paused unless funded.

No other unresolved ticket blocks Bets B–F unless it later meets the same foundation test: reproduced or strongly code-confirmed access/correctness defect, broad impact, bounded implementation, and clear acceptance.

## 2. Brent's ordered engineering queue

1. **Net-new SERV — contain direct-record Sales Portal authorization** (M, high confidence).
2. **SERV-2449 — Customers selected-period display and malformed CSV** (S, high confidence), after Package 1 ships.
3. **SERV-2196 — hybrid bill-to/ship-to authorization plus collapsed-key repair**, after Package 2 and an affected-client migration review.

SERV-2447 and SERV-2448 are closure items, not open-ended regression projects. Create a new focused issue only when a named edge case reproduces.

## 3. Paste-ready net-new authorization ticket

**Title:** Sales Portal: contain cross-territory direct-record access

### Problem and evidence

`PROD-REPRO` on 2026-08-04: legitimate restricted non-admin `wwjc/betaverify` received HTTP 200 and protected content for out-of-book Invoice `INV65157`, GET email-invoice id `4667912895`, and Customer `14378`. No email was sent. `SQL-BASELINE`: the customer is outside the user's six-territory book.

### Implement

1. Resolve Invoice detail, GET/POST email-invoice, and Customer detail through both current organization and the signed-in user's authorized customer/territory book.
2. Authorize before rendering or enqueueing mail; GET never sends.
3. Deny same-org out-of-book and cross-org identifiers.
4. Enforce the complete Sales Portal Dashboard gate on every data action, including invoice total, Top Customers, and Top Products.
5. Fail closed for restricted non-admin users with NULL, blank, or empty assignments.
6. Preserve customer-user, in-book rep, company-wide, and admin access.

### Acceptance

- `betaverify` cannot retrieve the three out-of-book controls; an in-book invoice, email page, and customer still open.
- Cross-org ids/numbers never resolve.
- A Dashboard-disabled non-admin receives no metric content; an authorized user still does.
- Unauthorized POST cannot enqueue mail; delivery count is unchanged after GET.
- Tests cover customer user, one/many/NULL/empty territories, company-wide, and admin without stubbing the permission decision.

Likely paths: `ecat_invoices_controller.rb`, `ecat_customers_controller.rb`, `ecat_dashboard_controller.rb`, permission helpers/models, `warehouse_access.rb`, and controller/request tests. Reuse the existing authorized book; do not refactor the shared resolver.

**Exclude:** SERV-2449, ship-to casing, SERV-2196 semantics, multi-value `RepNumber`, and amount/calculation changes.

## 4. Final replacement body for SERV-2449

**Title:** Fix Customers selected-period display and malformed CSV

**Problem/evidence:** `PROD-REPRO`: Previous Month is calculated/exported but its total and per-customer values are hidden. `PROD-PASS`: Previous YTD displays both. Three 2026-08-04 exports independently confirm malformed CSV: each has 1,965 rows, nine headings, and ten fields on every row; the unlabeled values are `DN`, `EP`, or `WS`. The two Current Month exports are byte-identical; Previous YTD changes the heading to `Previous YTD Sales` and changes 408 selected-period values. `CODE-IMPLICATION`: the extra value is `PriceLevel.cue_character`.

### Implement and accept

1. Non-standing selected periods display their total and per-customer values.
2. Current YTD and Previous Year are not duplicated.
3. The top total covers the complete matching customer set after current search and territory filters, not only the page.
4. Page and CSV customer sets and selected-period values agree.
5. Preserve human-readable headings such as `Previous Month Sales`.
6. CSV header and every row have equal field counts.
7. Label the existing cue field `Price Level Cue`.
8. Preserve calculation sources and bill-to/ship-to behavior.

Tests: Previous Month fail-to-pass; Previous YTD remains passing; no standing-column duplicates; complete filtered-set total; UI/CSV set and value parity; CSV field parity and label.

**Exclude:** scope/preamble block, totals row, generic `Selected Range Sales`, new ranges, broad relabeling, revenue changes, shared resolver work, or SERV-2196 semantics.

## 5. SERV-2196 selected product rule and engineering scope

### What is established

- The Jira fixture is stale and partly wrong. The valid production fixture is `shl` customer `72170` FERGUSON, bill-to territory `900`, Invoice `INV1446401`, and restricted `905`-only user `adams`.
- `CODE-IMPLICATION` on current `origin/master`: Portal list/report authorization is `bill-to customer_key OR ship_to_key`; ship-to-only territory can admit an invoice and can surface the whole customer account.
- In `shl`, all 3,703 shipping locations and all 450,558 portal invoices have NULL ship-to identifiers. `format_customer_key(...).compact` therefore collapses `ship_to_key` onto `customer_key`, causing a ship-to territory to grant the whole bill-to account.
- Existing Confluence product documentation says the intended model is bill-to full-account access plus exact ship-to access when the bill-to is outside the rep's territory. The multi-rep pattern is not a Savoy-specific exception.
- Direct-record containment is independent: those controllers currently bypass the warehouse book. Package 1 should enforce the current book; SERV-2196 changes what that book means.

### Selected rule — Option A

1. **Bill-to territory grants the full customer account and all its transactions.**
2. **Ship-to-only territory grants the customer shell needed for navigation, but only transactions addressed to that exact ship-to.**
3. When bill-to and ship-to territories differ, bill-to users retain full-account access; ship-to-only users receive only the exact-location transaction.
4. A NULL or blank ship-to identifier cannot prove an exact-location match and must never collapse into the bill-to key.
5. Customer totals include only facts authorized by those rules.
6. New clients use this strict model by default. Existing ambiguous blank-key data receives a staged audit and migration; any temporary compatibility path must be explicitly owned and retired, not preserved as a permanent authorization bypass.

### Compatibility and prevalence

`SQL-BASELINE` on 2026-08-04:

- 47 organizations have ship-to territory assignments;
- 33 have at least one ship-to territory absent from the same customer's bill-to territories;
- 7 have invoices matching populated ship-to-only paths, covering approximately 824,090 invoices;
- 324 customer accounts across 8 organizations are split across multiple ship-to-only territories and multiple restricted reps;
- those accounts contain 8,507 ship-to locations, and 238 have at least two matching reps who logged in during the last year;
- in 6 invoice-exposed organizations, 494 active restricted Sales Portal users hold relevant ship-to-only territories and 138 logged in during the last year;
- five organizations contain NULL-coded ship-tos with territories; `shl` actively over-grants 24 customers, `sarreid` has latent exposure, and `gl`, `dpl`, and `ebc` currently have no divergent bill-to/ship-to grant.

This does not prove that every matching rep viewed every affected account. It does prove that multi-location, multi-rep customer ownership is a real and actively configured product pattern. Bill-to-exclusive Option B would contradict documented behavior and remove legitimate ship-to access. Roll out Option A per organization, beginning with the five blank-key organizations and the seven populated ship-to invoice organizations.

### Reproducible read-only prevalence query plan

```sql
WITH ship_to_tc AS (
  SELECT c.organization_id, c.code bill_to, sl.code ship_to, lower(trim(j.value)) territory
  FROM shipping_locations sl JOIN customers c ON c.id = sl.customer_id
  CROSS JOIN LATERAL json_array_elements_text(
    coalesce(nullif(sl.territory_codes_json,''),'[]')::json) j
), bill_to_tc AS (
  SELECT c.organization_id, c.code bill_to, lower(trim(j.value)) territory
  FROM customers c CROSS JOIN LATERAL json_array_elements_text(
    coalesce(nullif(c.territory_codes_json,''),'[]')::json) j
), ship_to_only AS (
  SELECT DISTINCT s.* FROM ship_to_tc s WHERE NOT EXISTS (
    SELECT 1 FROM bill_to_tc b WHERE b.organization_id=s.organization_id
      AND b.bill_to=s.bill_to AND b.territory=s.territory)
)
SELECT (SELECT count(DISTINCT organization_id) FROM ship_to_tc) orgs_with_ship_to_territories,
       count(DISTINCT s.organization_id) orgs_with_ship_to_only_assignments,
       count(DISTINCT pi.organization_id) orgs_with_invoices,
       count(DISTINCT (pi.organization_id,pi.invoice_number)) invoices
FROM ship_to_only s LEFT JOIN portal_invoices pi
  ON pi.organization_id=s.organization_id
 AND pi.customer_bill_to_number=s.bill_to
 AND pi.customer_ship_to_number=s.ship_to;
```

### Engineering ticket

**Title:** Sales Portal: enforce bill-to/ship-to scope and prevent blank ship-to key collapse

Implement Option A in `FilterItemsByTerritoryCode`, mirror it in legacy `WarehouseAccess` predicates, and align Customers, totals, exports, Orders, Invoices, and direct-record authorization. Repair key construction so NULL/blank ship-to identifiers cannot equal the bill-to key. Audit and rebuild affected warehouse data. Use a temporary migration control only if an affected-client review proves one is required.

Acceptance: bill-to full-account fixture; populated exact ship-to-only fixture; divergent ship-to denial; NULL and blank ship-to fail-closed fixtures; one/many territories; customer-shell navigation; Invoice, Order, Customers, totals, export, and direct-record parity; warehouse rebuild validation; no widened access. Exclude direct-record controller implementation, casing, `RepNumber`, and amount changes.

## 6. Bet A and acceptance/closure lane

Use these concise manual resolution actions:

- **EBR-40 / SERV-2447:** close. `PROD-PASS`: restricted `betaverify`, Gigi Lane, June 2026 displayed `$123,585` vs `$123,585.35` SQL. Broad defect not reproduced. File a new issue only for a named failing edge.
- **EBR-212 / SERV-2448:** close. `PROD-PASS`: restricted Gigi Lane Current YTD displayed `$836,263` on Dashboard and Invoices. File a new issue only for a reproduced Top-N or drill-through route.
- **SERV-2431:** accept/close after one authorized staging or safe-org import with missing/blank `OrderNumber`; local import, required-field, and authenticated detail controls already passed.
- **EBR-7 / SERV-747:** SERV-747 stays Done. Accept EBR-7 only after controlled discount import, optional display/email, and Order/Invoice/Backlog/warehouse rollups pass; otherwise explicitly decline the remainder.
- **EBR-474 / EBR-601:** close EBR-474 as the older duplicate; preserve EBR-601 as canonical Waiting for Client.
- **EBR-180 / SERV-2178:** explicitly pause unless named demand, no upstream normalization, and funding justify the XL import/schema/ETL work.

## 7. Compact classification of the prior 57 candidates

This preserves the exact 57-ticket inventory; classification is about the foundation gate, not Jira status.

| Classification | Count | Tickets |
|---|---:|---|
| FOUNDATION-BUILD | 3 | EBR-91, SERV-2449, SERV-2196 |
| ACCEPT/CLOSE | 6 | EBR-7, EBR-40, SERV-2447, EBR-212, SERV-2448, EBR-474 |
| PAUSE/WAITING | 3 | EBR-601, EBR-606, SERV-2178 |
| FUTURE-BET | 43 | EBR-87, EBR-655; EBR-174, EBR-197, EBR-198, EBR-213, SERV-1912, SERV-1916, EBR-278, EBR-279, EBR-322, EBR-687, EBR-792, EBR-793; EBR-325, EBR-422, EBR-471, EBR-629, EBR-699, SERV-2169, SERV-2185, SERV-2382, SERV-2388; EBR-38, EBR-146, EBR-216, EBR-340, EBR-447, EBR-704, EBR-756, SERV-741, SERV-820, SERV-2403, SERV-2430; EBR-300, EBR-745, EBR-770, EBR-772, EBR-775, EBR-776, SERV-2113, SERV-2337, SERV-2425 |
| NOT-SALES-PORTAL | 1 | SERV-2395 — live body is explicitly iPad Reports > Customer Dashboard |
| INSUFFICIENT-EVIDENCE | 1 | SERV-2214 — old `scw` staging report; no current reproduction or validated current path |
| **Total** | **57** | |

Supplemental records outside that prior count: SERV-2431 = ACCEPT/CLOSE; EBR-180 = PAUSE/WAITING; SERV-747 = completed acceptance predecessor.

Notes on named non-blockers: EBR-606 is a waiting, client-specific drop-ship request that may be moot. EBR-655 is an eOL order-email enhancement. EBR-87 remains parked absent universal correctness impact. SERV-2214 does not enter the queue without current reproduction and correct product classification.

## 8. Exact Bets B–F blocker and non-blocker lists

### Blocks exit until the stated outcome

- **Net-new authorization SERV:** shipped and accepted.
- **EBR-91 / SERV-2449:** narrowed package shipped and accepted.
- **SERV-2196:** selected Option A package, collapsed-key repair, migration audit, and warehouse rebuild ship and pass.
- **SERV-2431:** accepted or returned with one named failure.
- **EBR-40 / SERV-2447; EBR-212 / SERV-2448:** closed with passing-route notes.
- **EBR-7:** accepted or explicitly declined.
- **EBR-474 / EBR-601:** duplicate/waiting disposition recorded.
- **EBR-180 / SERV-2178:** pause or funded continuation recorded.

The last five bullets are disposition gates, not reasons to add Brent engineering.

### Does not block Bets B–F

EBR-87, EBR-606, EBR-655, SERV-2214, SERV-2395, and every FUTURE-BET ticket in section 7. EBR-601 may remain Waiting for Client and EBR-180/SERV-2178 may remain paused after the dispositions are explicit.

## 9. Briefing for Brent

Unified Bet A is retired. The primary Invoice and Dashboard territory routes passed, so close EBR-40/SERV-2447 and EBR-212/SERV-2448. Do not turn them into a shared resolver or indefinite investigation.

Package 1 is the reproduced authorization containment: `betaverify` received protected out-of-book Invoice, GET email-invoice, and Customer content. Apply organization plus authorized-book checks to direct records, enforce Dashboard action gates, and prove denial and legitimate controls.

Package 2 is the narrow SERV-2449 correction: show non-standing selected-period values, avoid duplicate standing columns, make the full filtered total and CSV agree, repair field parity, and label `Price Level Cue`. Do not redesign the export or calculations.

Package 3 is SERV-2196. Option A is selected because it matches longstanding product documentation and live multi-rep customer configurations: bill-to grants the whole account, while ship-to-only grants the customer shell and exact-location transactions. The package must also prevent NULL/blank ship-to keys from collapsing into bill-to access, audit affected organizations, rebuild warehouse data, and validate both populated and blank-key fixtures.

After those packages and the small acceptance/closure dispositions complete, the foundation lane is closed. The other unresolved tickets are enhancements, client waits, non-Sales-Portal work, or unsupported reports; move to Bets B–F.

## 10. Short Slack message

> Brent — final Sales Portal foundation queue: (1) ship reproduced direct-record authorization containment, (2) ship narrowed SERV-2449, then (3) implement selected SERV-2196 Option A: bill-to grants the full account; ship-to-only grants the customer shell and exact-location transactions; NULL/blank ship-to keys must not collapse into bill-to access. This is not Savoy-specific: 324 multi-rep accounts span 8,507 ship-tos, with 238 accounts tied to at least two recently active reps. Audit affected blank-key orgs and rebuild the warehouse as part of Package 3. Close the 2447/2448 pairs, complete the acceptance/disposition lane, then move to Bets B–F.
