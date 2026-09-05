# Sales Portal reset — execution and next actions

**Date:** 2026-08-04  
**Owner:** Kylor Johnson  
**Engineering reader:** Brent Sanders  
**Status:** P0 authorization failure reproduced; authorization containment selected as Package 1  
**External changes:** None. Jira, Confluence, production records, users, settings, imports, email, and code were not modified.

Current authority:

1. `PM/Sales Portal Docs/00-SALES-PORTAL-SYSTEM-SPEC.md`
2. `PM/Sales Portal Docs/DECISION-BET-A-RESET-2026-08-04.md`
3. `PM/sales-portal-agent-starters/cycle-04-outputs/REVIEW-sales-portal-backlog-reset-2026-08-04.md`
4. `PM/sales-portal-agent-starters/cycle-04-outputs/POV-sales-portal-what-next-2026-08-04.md`

## 1. Executive result

The unified Bet A remains retired. Current evidence does not support a shared territory-resolver rewrite or a claim that the primary SERV-2447 and SERV-2448 routes are broken.

- `PROD-PASS`: The restricted `wwjc/betaverify` Invoice route for Gigi Lane in June 2026 displayed `$123,585`, matching the stable `$123,585.35` SQL baseline within display rounding.
- `PROD-PASS`: On 2026-08-04, Dashboard and Invoices both displayed `$836,263` for Gigi Lane Current YTD. This is a timestamped observation, not a permanent baseline.
- `PROD-REPRO`: Customers hides the selected-period value for Previous Month while showing it for Previous YTD.
- `PROD-REPRO`: Customers CSV rows contain more fields than the header. The unlabeled value is `PriceLevel.cue_character`, to be labeled `Price Level Cue`.
- `PROD-REPRO`: In an authenticated production HTTPS session as the legitimate non-admin `betaverify`, the out-of-book Invoice route returned `INV65157`, MEG BRAFF DESIGNS, and `$100.00`.
- `PROD-REPRO`: The GET-only email-invoice route returned the out-of-book invoice page for portal invoice id `4667912895`. No email was submitted or sent.
- `PROD-REPRO`: The Customer detail route returned out-of-book customer `14378` — MEG BRAFF DESIGNS.
- `CODE-RISK`: Dashboard data actions still appear to lack the stricter Dashboard gate; the gate-off routes remain to be tested as containment acceptance, but they no longer affect package sequencing.

The first engineering package is now definitive:

1. Authorization containment is Package 1.
2. The narrowed EBR-91/SERV-2449 Customers correction follows after containment ships.
3. SERV-2447/2448 remains regression validation, not a shared resolver implementation.

## 2. Current revision and runtime facts

### Repository

- `PROCESS`: Local checkout: `/Users/kylorjohnson/supercat-code/supercat_server`.
- `PROCESS`: Local `HEAD`: `d4a0e7d408fba6917ac5e685cd21e54c5ecd801d`.
- `PROCESS`: Local commit date: 2025-12-09.
- `PROCESS`: The local branch is 680 commits behind `origin/master`.
- `PROCESS`: The local working tree contains pre-existing modified and untracked files. None were changed or cleaned during this execution.
- `PROCESS`: Fetched `origin/master` on 2026-08-04.
- `PROCESS`: Current `origin/master`: `4ff408492650a2f14e6572f833365c3eaba97c10`.
- `PROCESS`: The prior POV inspected `0856f2d1a`; current remote advanced to `4ff408492`.
- `CODE-IMPLICATION`: No commit between `0856f2d1a` and `4ff408492` touched the reviewed Dashboard, Invoice, Customer, Customer-export, or territory-filter paths. The POV's current-source authorization risks therefore remain applicable to current `origin/master`.

### Production runtime

- `PROCESS`: The exact deployed production revision could not be identified.
- `PROCESS`: An unauthenticated request to the production Dashboard route redirected to login and exposed request/runtime headers, but no commit or release identifier.
- `PROCESS`: GitHub deployment metadata could not be queried because the GitHub CLI is unavailable in this environment.
- `OPEN-DECISION`: Brent or an operator with deployment access must record the deployed SHA before interpreting source as deployed behavior.

### Read-only production data recheck

- `SQL-BASELINE`: `betaverify` remains non-admin on both admin columns, has a blank customer number, user type `z'-Bet A Verify` (2864), and six separate `105:1`–`105:6` territories.
- `SQL-BASELINE`: `cmallon` remains non-admin on both admin columns, has a blank customer number, and holds the same six territories.
- `SQL-BASELINE`: Gigi Lane, 2026-06-01 through 2026-06-30 remains 110 invoices, 75 accounts, `$123,585.35`.
- `SQL-BASELINE`: Control invoice id `4667912895` remains `INV65157`, customer `14378`, dated 2026-08-04, net amount `$100.00`.
- `SQL-BASELINE`: Customer `14378` remains MEG BRAFF DESIGNS and is assigned only to `D6 LORNE GARDNER` and `30440 Interim Rep House Account`, outside `betaverify`'s six-territory book.

### Current external authority

- `STALE`: EBR-40 still says the Invoice territory filter is not working.
- `STALE`: SERV-2447 still directs engineering toward unified territory-scope paths.
- `STALE`: EBR-212 and SERV-2448 still present broad Dashboard filter work despite the primary KPI pass.
- `STALE`: EBR-91 and SERV-2449 still contain unsupported export redesign requirements.
- `STALE`: Confluence pages `1819836417`, `1819869185`, `1819901953`, and `1820262402` still authorize or describe unified Bet A.
- `STALE`: Footer comment `1820655618` correctly retracts some errors but still says Phase 0 and Phase 1 can start and approves now-retired scope such as the CSV scope block, totals row, and stable generic heading.
- `STALE`: `00-PROGRAM-SPINE.md` still authorizes the unified Bet A GO and doctrine-closes EBR-7.

## 3. P0 authorization result

### Result

`PROD-REPRO`: Failed on 2026-08-04 at approximately 14:24 MDT.

Preconditions independently established:

- `SQL-BASELINE`: `betaverify` is non-admin on both admin columns, has a blank customer number, all-customer totals off, and only the six `105:1`–`105:6` territories.
- `SQL-BASELINE`: Customer `14378` is assigned only to `D6 LORNE GARDNER` and `30440 Interim Rep House Account`.
- `SQL-BASELINE`: Portal invoice id `4667912895` is `INV65157`, belongs to customer `14378`, and has net amount `$100.00`.

Authenticated production results:

1. `/wwjc/e/wwfc-2/invoices/INV65157`
   - HTTP 200; no denial or redirect.
   - Response contained `INV65157`, MEG BRAFF DESIGNS, and `$100.00`.
   - `PROD-REPRO`: out-of-book Invoice detail exposed.
2. `/wwjc/e/wwfc-2/email_invoice/4667912895`
   - GET only; HTTP 200; no denial or redirect.
   - Response contained `INV65157`.
   - No form submission or email send was performed.
   - `PROD-REPRO`: out-of-book email-invoice page exposed.
3. `/wwjc/e/wwfc-2/customers/14378`
   - HTTP 200; no denial or redirect.
   - Response contained customer `14378` and MEG BRAFF DESIGNS.
   - `PROD-REPRO`: out-of-book Customer detail exposed.

Any one exposure fails P0. All three record-detail controls failed, so authorization containment is definitively first.

Still open inside Package 1 acceptance:

- record the deployed production SHA and portal warehouse timestamp;
- confirm a Dashboard-disabled non-admin fixture;
- test `/portal/invoice_total`, `/portal/top_customers`, and `/portal/top_products` with that fixture;
- verify in-book controls continue to work after containment.

## 4. First-package decision

### Selected Package 1: authorization containment

**Problem**

A logged-in non-admin can retrieve Sales Portal record or Dashboard content outside the user's authorized book or feature gate.

**Scope**

- enforce the Sales Portal Dashboard-specific gate on every Dashboard data action;
- resolve Invoice show through organization-scoped and territory-authorized relations;
- resolve the GET email-invoice route through organization-scoped and territory-authorized relations;
- resolve Customer detail through the user's customer/territory-authorized relation;
- fail closed for blank, NULL, or empty assignments;
- add denial tests based on legitimate non-admin users;
- use SERV-2199 as precedent without assuming it solved record-level authorization.

**Acceptance**

- all six P0 routes deny out-of-book or gated content;
- an in-book control still opens;
- an authorized Dashboard user still receives Dashboard metrics;
- cross-organization ids do not resolve;
- GETting the email route does not send email;
- no test stubs the permission decision being proved.

**Exclude**

- Customers selected-period display or CSV;
- shared territory-resolver rewrite;
- ship-to casing;
- bill-to/ship-to product semantics;
- `RepNumber`;
- reporting amount changes.

### Package 2 after containment: narrowed EBR-91/SERV-2449

Proceed with the replacement contract in sections 5.5 and 5.6 after the authorization containment package passes and ships.

## 5. Paste-ready Jira replacement bodies

These are complete replacement bodies for Kylor to review and paste manually. No Jira changes were made.

### 5.1 EBR-40

**Suggested summary:** Invoice territory filter — primary route verified; edge cases pending

```markdown
## Sales Portal Invoice territory invariant

Program authority:

- Sales Portal system specification — 2026-08-04
- Decision — retire and restart Sales Portal Bet A — 2026-08-04
- Implementation/validation: SERV-2447

### Product result

`PROD-PASS`: On 2026-08-04, the legitimate non-admin `wwjc/betaverify` fixture selected `105:1 Gigi Lane` for 2026-06-01 through 2026-06-30. The Invoice UI displayed `$123,585`, matching the stable SQL baseline of `$123,585.35` within display rounding.

`SQL-BASELINE`: The closed-period baseline is 110 invoices, 75 accounts, and `$123,585.35`.

`OPEN-DECISION`: The supplied capture did not prove the 110-invoice row count.

The primary route is therefore verified. This request no longer asserts that the Invoice territory filter is broadly broken.

### Product invariant

A non-admin rep sees only the customer/ship-to territory book authorized to that user. A selected territory narrows that permitted book and must not widen it. `RepNumber` access is a separate, feature-gated mechanism.

### Validation required

- one assigned territory;
- union of multiple assigned territories;
- 110-row June Gigi Lane count and `$123,585.35` total;
- NULL territory assignment fails closed;
- empty territory assignment fails closed;
- explicit selection narrows an all-customer-totals user;
- one organization with real ship-to territory assignments;
- customer and ship-to territory case differences;
- collapsed blank ship-to key does not create an accidental match.

### Decision rule

If all cases pass, close or reclassify this request as verified regression coverage. If a case fails, create a focused repair for that reproduced root cause.

### Out of scope

- shared territory-resolver rewrite;
- invoice/order `RepNumber` changes;
- ship-to casing without an affected-org reproduction;
- Customer display/export work;
- Dashboard redesign;
- revenue or amount-contract changes.
```

### 5.2 SERV-2447

**Suggested summary:** Validate Sales Portal Invoice territory edge cases after primary-route pass

```markdown
## Invoice territory regression validation

Product request: EBR-40

Current authority:

- Sales Portal system specification — 2026-08-04
- Decision — retire and restart Sales Portal Bet A — 2026-08-04

### Current result

`PROD-PASS`: The restricted `wwjc/betaverify` Invoice route for `105:1 Gigi Lane`, June 2026 displayed `$123,585`, matching the stable `$123,585.35` SQL baseline within display rounding.

`SQL-BASELINE`: 110 invoices, 75 accounts, `$123,585.35`.

`OPEN-DECISION`: The UI capture did not prove the 110-row count.

The former broad defect premise and shared-resolver implementation instruction are retired. No Invoice behavior change is authorized until an edge case fails.

### Execute

Add or run focused assertions for:

1. one selected assigned territory;
2. union of multiple assigned territories;
3. Gigi Lane June count = 110 and total within documented rounding/tolerance;
4. NULL territory assignment fails closed;
5. empty-array territory assignment fails closed;
6. explicit selection narrows an all-customer-totals user;
7. an organization whose ship-tos actually carry territory assignments;
8. mixed-case customer and ship-to territory codes;
9. collapsed blank ship-to keys do not create false bridge matches.

Record the portal warehouse timestamp for territory-dependent checks.

### Done when

- passing cases are covered by regression tests;
- no permission check is stubbed in the test proving scope;
- all failures are split by root cause;
- passing behavior is not rewritten;
- if all cases pass, this ticket is closed or reclassified as regression coverage.

### Product boundaries

- customer and ship-to master assignments define normal territory;
- invoice/order `RepNumber` is separate and feature-gated;
- current bill-to/ship-to row semantics remain unchanged pending a separate product decision;
- amount semantics remain unchanged.

### Out of scope

- shared territory resolver;
- SERV-2448 Dashboard residuals;
- SERV-2449 Customers work;
- SERV-2196 product semantics;
- ship-to casing ticket creation before reproduction;
- EBR-180/SERV-2178;
- revenue recalculation.
```

### 5.3 EBR-212

**Suggested summary:** Sales Portal Dashboard territory — KPI verified; Top-N and drill-through pending

```markdown
## Dashboard territory residual validation

Implementation: SERV-2448
Completed predecessor: SERV-1092

Current authority:

- Sales Portal system specification — 2026-08-04
- Decision — retire and restart Sales Portal Bet A — 2026-08-04

### Current result

`PROD-PASS`: On 2026-08-04, `wwjc/betaverify` selected `105:1 Gigi Lane` and Current YTD. Invoices and Dashboard each displayed `$836,263`.

This is a timestamped observation, not a permanent baseline. The primary Dashboard invoiced-KPI route is verified and is not a current headline defect.

### Residual product questions

- `OPEN-DECISION`: Do Top Customer members all belong to the selected permitted book?
- `OPEN-DECISION`: Do Top Product values use only territory-scoped orders/order lines?
- `CODE-IMPLICATION`: Several Dashboard destination links omit the selected `multi-select-filters`; user-visible impact still requires reproduction.

### Done when

1. Top Customer membership is validated against the selected permitted customer/location book.
2. Top Product values are validated against territory-scoped orders and order lines.
3. Dashboard drill-through behavior is reproduced for graph, Orders, Backlog, and Top-N/customer destinations.
4. Only links that fail the intended workflow are repaired.
5. The already-passing Invoice KPI link remains unchanged unless a regression test fails.

### Decision rule

Passing checks become regression coverage. Any failure is split into a focused repair. Do not authorize a shared territory-resolver rewrite.

### Out of scope

- Dashboard redesign;
- one universal measure across panels;
- Customers display/export;
- ship-to casing;
- bill-to/ship-to precedence;
- multi-valued `RepNumber`;
- amount-contract changes.
```

### 5.4 SERV-2448

**Suggested summary:** Validate Dashboard Top-N territory scope and drill-through persistence

```markdown
## Dashboard territory residuals after primary KPI pass

Product request: EBR-212
Completed predecessor: SERV-1092

Current authority:

- Sales Portal system specification — 2026-08-04
- Decision — retire and restart Sales Portal Bet A — 2026-08-04

### Current result

`PROD-PASS`: On 2026-08-04, the legitimate non-admin `wwjc/betaverify` fixture selected Gigi Lane Current YTD. Dashboard and Invoices both displayed `$836,263`.

The primary KPI route passes. This ticket no longer asserts that Dashboard territory scope broadly fails.

### Validate

1. Every Top Customer member belongs to the selected permitted customer/location book.
2. Top Product values reconcile to territory-scoped orders/order lines; these widgets use ordered measures, not the Invoice KPI's invoiced measure.
3. Reproduce selected-filter persistence through graph, Orders, Backlog, Top Customer, Top Product, Tradename, and Collection destinations where those destinations support the filter.
4. Confirm the existing Invoice KPI link, which already passes `report_params`, remains correct.

### Repair rule

- Add regression tests for passing paths.
- Repair only a reproduced failing link or query.
- Keep each failure scoped to its root cause.
- Do not refactor the shared territory resolver merely because Dashboard and Invoice paths differ.

### Done when

- Top Customer and Top Product scope is evidenced;
- intended drill-through context persists;
- passing links are not rewritten;
- no Dashboard panel is required to use a different business measure merely to match another panel.

### Out of scope

- primary KPI rewrite;
- Dashboard redesign;
- shared resolver work;
- Customers selected-period/export work;
- ship-to casing;
- `RepNumber`;
- amount-contract changes.
```

### 5.5 EBR-91

**Suggested summary:** Customers selected-period display and CSV structure correction

```markdown
## Customers selected-period display and export correctness

Implementation: SERV-2449

Current authority:

- Sales Portal system specification — 2026-08-04
- Decision — retire and restart Sales Portal Bet A — 2026-08-04

### Problem

Sales reps and sales managers use Customers to review account sales for their territory and export the same account list to Excel. When they choose a period such as Previous Month, the export includes that period's sales but the page does not show it. The CSV also contains an unlabeled price-level cue value.

### Evidence

- `PROD-REPRO`: Previous Month omitted the selected-period card and customer column.
- `PROD-PASS`: Previous YTD displayed both, proving the selected-period capability exists.
- `PROD-REPRO`: Customers CSV contains more row fields than headings.
- `CODE-IMPLICATION`: The unlabeled value is `PriceLevel.cue_character`, not customer class.

### Done when

1. Ranges not already represented by the standing Current YTD/Previous Year columns show the selected-period total and per-customer value.
2. The top selected-period total covers every account matching the current customer search and territory filter, not only the visible page.
3. Export returns the same customer set and selected-period sales as the page.
4. The existing human-readable period heading is preserved, such as `Previous Month Sales`.
5. Every CSV row has the same field count as the header.
6. The existing cue-character field is labeled `Price Level Cue`.
7. Current revenue calculations and standing Current YTD/Previous Year behavior are preserved.
8. Current bill-to/ship-to row math is preserved until the conflicting territory documentation is resolved separately.

### Excluded

- CSV scope/preamble block;
- totals row;
- generic `Selected Range Sales`;
- duplicate selected-period columns for Current YTD/Previous Year;
- new date ranges;
- broad CY/LY relabeling;
- unknown-range fallback as customer-facing scope;
- revenue changes;
- territory-resolver work.
```

### 5.6 SERV-2449

**Suggested summary:** Fix Customers selected-period display and malformed CSV

```markdown
## Customers selected-period display and CSV structure

Product request: EBR-91

Current authority:

- Sales Portal system specification — 2026-08-04
- Decision — retire and restart Sales Portal Bet A — 2026-08-04

### Problem

Sales reps and sales managers use Customers to review account sales for their territory and export the same account list. Previous Month sales are calculated and exported but hidden on the page. The CSV also writes a price-level cue value without a matching heading.

### Evidence

- `PROD-REPRO`: Previous Month omits the selected-period card and column.
- `PROD-PASS`: Previous YTD shows both.
- `CODE-IMPLICATION`: The Customers controller uses an accidental Ruby substring check that admits only `previous_ytd` and `custom`.
- `PROD-REPRO`: CSV rows contain more values than the header.
- `CODE-IMPLICATION`: The extra value is `PriceLevel.cue_character`.

### Implement

1. Replace the accidental substring gate with the documented display policy: standing Current YTD/Previous Year columns are not duplicated; other supported selected periods render the selected-period total and per-customer value.
2. Prove Previous Month first and retain Previous YTD as a passing comparison.
3. Keep Customers account-first: date selection changes values, not customer membership by itself.
4. Ensure the top total covers the full matching customer set after current search and territory filters, not only the visible page.
5. Keep export aligned to the same customer set and period.
6. Preserve the human-readable period header, such as `Previous Month Sales`.
7. Add the missing `Price Level Cue` heading and assert that every row has the header's field count.
8. Preserve existing calculation sources, standing columns, and current bill-to/ship-to row math.

### Required tests

- Previous Month renders its total and per-customer value.
- Previous YTD remains passing.
- Current YTD and Previous Year do not gain duplicate selected-period columns.
- search and territory filters apply to the complete matching account set;
- UI and CSV customer sets agree;
- UI and CSV selected-period sums agree;
- CSV header count equals every row count;
- `Price Level Cue` is present and aligned.

### Excluded

- scope/preamble block;
- totals row;
- generic `Selected Range Sales`;
- new ranges;
- broad relabeling;
- customer-facing unknown-range fallback;
- revenue-definition changes;
- shared territory resolver;
- bill-to/ship-to semantic changes.

### Sequence

Start only after the P0 authorization probe passes or after a reproduced authorization failure has been contained.
```

## 6. Paste-ready Confluence replacement bodies

These are complete page bodies for Kylor to review and paste manually. Page titles may be renamed as suggested. No Confluence changes were made.

### 6.1 Page 1819836417

**Suggested title:** Sales Portal reset — acceptance portfolio

```markdown
# Sales Portal reset — acceptance portfolio

**Status:** Unified Bet A retired  
**Date:** 2026-08-04  
**Owner:** Kylor Johnson

Canonical authority:

1. Sales Portal system specification — 2026-08-04
2. Decision — retire and restart Sales Portal Bet A — 2026-08-04

## Decision

SERV-2447, SERV-2448, and SERV-2449 are not one engineering package and do not authorize a shared territory-resolver rewrite.

## Current evidence

- `PROD-PASS`: Invoice, `wwjc/betaverify`, Gigi Lane, June 2026 displayed `$123,585`; stable SQL baseline is 110 invoices, 75 accounts, `$123,585.35`. The capture did not prove row count.
- `PROD-PASS`: Dashboard and Invoices both displayed `$836,263` for Gigi Lane Current YTD on 2026-08-04.
- `PROD-REPRO`: Customers Previous Month hid the selected-period value.
- `PROD-PASS`: Customers Previous YTD displayed it.
- `PROD-REPRO`: Customers CSV has more values than headings.
- `CODE-IMPLICATION`: The unlabeled field is `PriceLevel.cue_character`; label it `Price Level Cue`.
- `PROD-REPRO`: `betaverify` received HTTP 200 and out-of-book content from Invoice detail, GET email-invoice, and Customer detail.
- `CODE-RISK`: Dashboard sub-actions still require gate-off validation inside the containment package.

## Gate 0 — authorization result

`PROD-REPRO`: Failed. As `betaverify`, all three out-of-book record routes returned HTTP 200 and protected content:

- Invoice `INV65157`;
- GET email-invoice for portal invoice id `4667912895`;
- Customer `14378`.

## Package 1 — authorization containment

Controller gates and organization/territory-authorized record resolution. Include GET-only email-route denial. Exclude reporting work, shared resolver work, ship-to casing, `RepNumber`, and amount changes.

## Package 2 — after containment

Customers selected-period display and CSV structure:

1. Non-standing selected ranges display the selected-period total and per-customer value.
2. Top total covers the complete matching customer set.
3. Export matches the page's customer set and selected period.
4. Keep human-readable period headers.
5. Header and row field counts match.
6. Label `Price Level Cue`.
7. Preserve calculations, standing columns, and bill-to/ship-to row math.

Exclude scope block, totals row, generic header, duplicate standing columns, new ranges, broad relabeling, revenue changes, and territory refactoring.

## Package 2 — territory regression

SERV-2447: validate one/many territories, June count/total, NULL and empty fail-closed, all-totals explicit selection, real ship-to assignment, casing, and blank ship-to key.

SERV-2448: validate Top Customer membership, Top Product scope against orders/order lines, and intended drill-through persistence.

Passing behavior becomes regression coverage. Split only reproduced failures.
```

### 6.2 Page 1819869185

**Suggested title:** Sales Portal reset — engineering handoff

```markdown
# Sales Portal reset — engineering handoff

**Status:** Authorization containment selected; no unified Bet A implementation authorization  
**Date:** 2026-08-04

Current authority:

1. Sales Portal system specification — 2026-08-04
2. Decision — retire and restart Sales Portal Bet A — 2026-08-04

## Runtime note

The old local checkout is `d4a0e7d40`. Current `origin/master` recorded on 2026-08-04 is `4ff408492`. No commits after the previously inspected `0856f2d1a` touched the reviewed Portal paths. The deployed production SHA is still required.

## Gate 0 — direct-route authorization result

`PROD-REPRO`: The legitimate non-admin `betaverify` received HTTP 200 and protected out-of-book content from Invoice `INV65157`, GET email-invoice id `4667912895`, and Customer `14378`.

First package is controller-gate and territory-authorized record containment. Use SERV-2199 as precedent. Do not mix in reporting behavior.

Dashboard gate-off sub-actions remain containment acceptance coverage. The narrowed SERV-2449 package follows after containment ships.

## SERV-2449 code map

- `app/controllers/ecat_customers_controller.rb`: replace accidental substring gating with the non-standing-range display rule.
- `app/services/controllers/ecat_customer.rb`: preserve current calculation sources and align the complete matching customer set between page and export.
- `app/views/ecat_customers/index.html.erb`: render selected-period values only where not duplicated by standing columns.
- CSV construction: add `Price Level Cue`; assert header/row parity; preserve range-specific heading.
- Tests: Previous Month fail-to-pass, Previous YTD regression, standing-column non-duplication, full result-set total, UI/CSV set and sum parity.

Do not add a scope block, totals row, generic period header, broad relabeling, new range, revenue change, or territory resolver.

## SERV-2447 validation map

- permission book and selected narrowing remain separate concerns;
- validate one/many, NULL/empty fail-closed, all-totals explicit selection, real ship-to assignment, casing, and collapsed blank ship-to key;
- use Gigi Lane June: 110 invoices, 75 accounts, `$123,585.35`;
- no behavior rewrite without a failing case.

## SERV-2448 validation map

- primary invoiced KPI route passed;
- validate Top Customer membership;
- validate Top Product against territory-scoped orders/order lines;
- reproduce each destination link before repairing parameter propagation;
- preserve the already-passing Invoice KPI link.

## Separate packages

- SERV-2196: bill-to/ship-to precedence and compatibility decision before code.
- Ship-to casing: affected-org reproduction before ticketing.
- EBR-180/SERV-2178: pause absent a named customer and funding.
- Amount contract: separate product decision.
- EBR-7: full discount acceptance, not doctrine closure.
```

### 6.3 Page 1819901953

**Suggested title:** Sales Portal reset — verification and evidence

```markdown
# Sales Portal reset — verification and evidence

**Date:** 2026-08-04  
**Fixture:** `wwjc/betaverify`

## Evidence rules

Use `PROD-REPRO`, `PROD-PASS`, `SQL-BASELINE`, `CODE-IMPLICATION`, `CODE-RISK`, `DOC-INTENT`, `STALE`, `INVALID`, `OPEN-DECISION`, and `PROCESS`.

Admin sessions are invalid for restricted-rep acceptance. Current-YTD observations must be timestamped. Closed periods are preferred.

## Fixture

`SQL-BASELINE`:

- non-admin on both admin columns;
- blank customer number;
- user type `z'-Bet A Verify` (2864);
- Dashboard and portal totals enabled;
- all-customer totals off;
- six separate territories, `105:1` through `105:6`.

## Stable baseline

`SQL-BASELINE`: Gigi Lane, 2026-06-01 through 2026-06-30:

- 110 invoices;
- 75 accounts;
- `$123,585.35`.

## Valid production results

- `PROD-PASS`: Invoice displayed `$123,585`, within display rounding of the stable baseline. Row count was not proven by the capture.
- `PROD-PASS`: Dashboard and Invoices each displayed `$836,263` for Gigi Lane Current YTD on 2026-08-04.
- `PROD-REPRO`: Customers Previous Month omitted selected-period card and column.
- `PROD-PASS`: Customers Previous YTD displayed both.
- `PROD-REPRO`: Customer CSV has fewer headings than values.
- `PROD-REPRO`: `betaverify` received out-of-book Invoice `INV65157`, GET email-invoice id `4667912895`, and Customer `14378`, each with HTTP 200.

## Invalid or stale evidence

- `INVALID`: Admin captures as restricted-rep evidence.
- `INVALID`: Admin Console `view_dashboard` as the Sales Portal Dashboard gate.
- `INVALID`: Calling the cue field customer class.
- `STALE`: Current-YTD amounts used as permanent baselines.
- `STALE`: Claim that `wwjc` depends on ship-to casing.
- `STALE`: Claim that no acceptance criterion has executed.

## P0 authorization record

Out-of-book control:

- customer `14378` — MEG BRAFF DESIGNS;
- invoice `INV65157`;
- portal invoice id `4667912895`;
- amount `$100.00`;
- outside `betaverify`'s book.

Result: failed. The three record routes returned protected content to `betaverify`. Record the deployed SHA and warehouse timestamp, and complete the three Dashboard gate-off checks as containment acceptance coverage.

## Remaining territory matrix

- June count and total;
- one/multiple assigned territories;
- NULL/empty fail-closed;
- all-totals explicit selection;
- actual ship-to-assigned organization;
- case differences;
- blank/collapsed ship-to key;
- Top Customer membership;
- Top Product order-fact scope;
- drill-through persistence.

No behavior change is authorized unless a case fails.
```

### 6.4 Page 1820262402

**Suggested title:** Sales Portal reset — execution plan

```markdown
# Sales Portal reset — execution plan

**Status:** Unified Bet A plan retired  
**Date:** 2026-08-04

This body replaces the prior shared-resolver implementation plan.

## Sequence

### 0. Authorization probe — failed

`PROD-REPRO`: Invoice detail, GET email-invoice, and Customer detail returned out-of-book content to `betaverify`.

Authorization containment is first. The deployed revision still needs to be recorded. Dashboard gate-off sub-actions remain acceptance coverage.

### 1. Apply coordinated authority replacement

Kylor manually replaces EBR-40, SERV-2447, EBR-212, SERV-2448, EBR-91, SERV-2449, and the four Confluence bodies. Do not add another correction layer.

### 2. Issue a fresh scoped GO

The 2026-07-24 unified Bet A GO is retired. A new GO authorizes only the P0-selected first package.

### 3. Authorization containment

Controller gates and organization/territory-authorized record resolution. Include Invoice show, GET email-invoice, Customer detail, and Dashboard data actions. Add legitimate non-admin denial tests.

Exclude Customers reporting, shared resolver, casing, `RepNumber`, bill-to/ship-to semantics, and amount changes.

### 4. Customers correction, after containment ships

Fix the non-standing selected-period display rule and malformed CSV. Preserve the customer set, human-readable period heading, current calculations, standing columns, and bill-to/ship-to row math.

Exclude scope block, totals row, generic header, duplicate standing columns, broad relabeling, new ranges, revenue changes, and territory refactoring.

### 5. Territory regression

Run SERV-2447/2448 acceptance packs. Add regression coverage for passes. Split only failing roots.

### 6. Ready acceptance

- SERV-2431: one authorized import with missing/blank optional `OrderNumber`.
- EBR-7/SERV-747: full discount import/display/email/rollup acceptance.

### 7. Decision-only backlog

- EBR-601 likely canonical over EBR-474 pending client evidence.
- Pause EBR-180/SERV-2178 absent named demand and funding.
- SERV-2196 needs product semantics and compatibility before code.
- Ship-to casing needs an affected-org reproduction.
- Amount semantics remain separate.
- SERV-2214 remains an orphan pending independent inspection.
```

## 7. Replacement note for footer comment 1820655618

```markdown
Historical correction — 2026-08-04:

The unified Bet A implementation plan above is retired by the current Sales Portal system specification and the decision to reset Bet A. SERV-2447's primary Invoice route passed, SERV-2448's primary Dashboard KPI route passed, and SERV-2449 is narrowed to Customers selected-period display plus CSV field parity and `Price Level Cue`.

The prior authorization for a shared resolver, CSV scope block, totals row, generic `Selected Range Sales` heading, broad relabeling, ship-to casing inside `wwjc`, and doctrine closure of EBR-7 is withdrawn.

The authenticated non-admin direct-route probe failed: `betaverify` received out-of-book Invoice, GET email-invoice, and Customer detail content. Focused authorization containment is first. The narrowed Customers package follows only after containment passes and ships. See the 2026-08-04 Sales Portal reset authority for the complete replacement.
```

## 8. Program-spine replacement text

Apply these replacements manually to `PM/sales-portal-agent-starters/00-PROGRAM-SPINE.md`.

### Replace the title/status and Isolation Mode opening

```markdown
# Sales Analytics (Portal & Reporting) — Program Spine
**Reset:** 2026-08-04  
**Owner:** Kylor  
**Current Sales Portal authority:** `PM/Sales Portal Docs/00-SALES-PORTAL-SYSTEM-SPEC.md` and `PM/Sales Portal Docs/DECISION-BET-A-RESET-2026-08-04.md`

## ISOLATION MODE

### Original Bet A — RETIRED 2026-08-04

The 2026-07-24 unified Bet A GO no longer authorizes engineering. EBR-40/SERV-2447, EBR-212/SERV-2448, and EBR-91/SERV-2449 are separate packages.

Before replacement engineering:

1. record the failed authenticated non-admin direct-route probe;
2. manually replace stale Jira and Confluence authority;
3. issue a fresh scoped GO for authorization containment only.

`PROD-REPRO`: Out-of-book Invoice, GET email-invoice, and Customer detail routes returned protected content to `betaverify`. Focused authorization containment is first. Narrowed Customers selected-period display and CSV structure follows after containment.

Still forbidden without separate evidence and GO:

- shared territory-resolver rewrite;
- bill-to/ship-to semantic change;
- ship-to casing without affected-org reproduction;
- EBR-180/SERV-2178 without named customer demand and funding;
- amount-contract changes;
- Bets C/E/F/LLM expansion.

Jira and Confluence are read-only for agents. Kylor applies the coordinated replacement pack manually.
```

### Replace the Bet A shaped-bet section

```markdown
### Sales Portal reset portfolio (Lane 0)

- **Original Bet A:** retired; not an engineering package.
- **Gate 0:** failed; out-of-book Invoice, email-invoice, and Customer detail reproduced with `betaverify`.
- **Package 1:** controller gates plus organization/territory-authorized record resolution.
- **Package 2:** EBR-91/SERV-2449 selected-period display and CSV structure after containment.
- **Regression package:** EBR-40/SERV-2447 and EBR-212/SERV-2448 edge validation; split only reproduced failures.
- **Verified:** Invoice Gigi Lane June total passed; Dashboard invoiced KPI matched Invoices; Customers Previous Month display and CSV structure defects reproduced.
- **Do not authorize:** shared resolver, scope block, totals row, generic period header, broad relabeling, revenue rewrite, or territory semantic change.
- **Stable acceptance:** Gigi Lane June 2026 = 110 invoices, 75 accounts, `$123,585.35`.
- **Current authority:** Sales Portal system specification and reset decision dated 2026-08-04.
```

### Replace the EBR-7 doctrine statements wherever they appear

```markdown
EBR-7 / SERV-747 — SERV-747 is Done, but EBR-7 is not doctrine-closed. Run one authenticated acceptance covering UnitPriceDiscount and/or ExtendedPriceDiscount import, order/invoice display, email display, and Order/Invoice/Backlog/warehouse rollups. Close only after those criteria pass or the remaining request is explicitly declined.
```

### Replace the Lane 0 Jira notes for the reset tickets

```markdown
- EBR-40 / SERV-2447 — primary Invoice route passed; edge validation only.
- EBR-212 / SERV-2448 — primary Dashboard KPI passed; Top-N and drill-through residuals only.
- EBR-91 / SERV-2449 — narrowed Customers selected-period display and CSV structure; start after authorization containment.
- EBR-7 / SERV-747 — verify full discount acceptance; no doctrine closure.
- EBR-180 / SERV-2178 — default pause absent named customer and funding.
- SERV-2196 — product semantics and compatibility before code.
```

## 9. SERV-2447/2448 territory regression pack

Preconditions:

- record deployed SHA and portal warehouse timestamp;
- use non-admin fixtures;
- preserve identical date range and territory during comparisons;
- use closed June 2026 where the pack names the stable baseline;
- do not change behavior unless a case fails.

### Invoice / SERV-2447

- [ ] `betaverify`, Gigi Lane, June 2026: page reports 110 invoices.
- [ ] Same selection: total is `$123,585.35` within documented display rounding/tolerance.
- [ ] Every sampled row belongs to the authorized Gigi Lane customer/location book.
- [ ] One assigned territory narrows correctly.
- [ ] No selection returns the union of assigned territories, not company-wide data.
- [ ] NULL territory assignment with no all-totals permission returns no data.
- [ ] Empty-array territory assignment with no all-totals permission returns no data.
- [ ] All-totals user making an explicit selection is narrowed to that selection.
- [ ] A real ship-to-assigned organization follows the documented bill-to/ship-to behavior.
- [ ] Customer and ship-to territory case differences do not cause false negatives.
- [ ] A blank ship-to key does not accidentally match a ship-to bridge row.

For each row record fixture, flags, range, selection, expected, observed, count, total, and evidence label.

### Dashboard / SERV-2448

- [ ] Invoice KPI remains scoped to the same selected book.
- [ ] Every Top Customer belongs to the selected permitted book.
- [ ] Top Product values reconcile to selected-book orders/order lines.
- [ ] Graph drill-through preserves intended period and territory.
- [ ] Orders drill-through preserves representable filters.
- [ ] Backlog drill-through preserves representable filters.
- [ ] Top Customer/Product/Tradename/Collection destinations preserve intended filters.
- [ ] Existing Invoice KPI link remains passing.

Top Customer/Product are not required to equal the Invoice KPI because they can use ordered measures while the KPI uses invoiced measures.

Disposition:

- all pass → regression coverage and close/reclassify;
- failure → focused repair for that root cause only.

## 10. SERV-2431 acceptance pack

Do not run without explicit authorization to import into staging or a named safe production organization.

Preconditions:

- choose staging or a safe production org;
- snapshot the current import/file state;
- prepare a minimal valid `invoice_data.csv`;
- include one invoice with `OrderNumber` missing and one with it blank if the importer distinguishes those shapes;
- use date-only date fields, exact filename, no extra columns, and contiguous invoice/order grouping as applicable.

Run:

1. Upload/import the authorized file.
2. Inspect File Import Status and retain the exact result.
3. Confirm both optional-OrderNumber rows imported.
4. Open invoice detail for each.
5. Confirm the page does not render a broken order link.
6. Confirm an invoice with a valid OrderNumber still links correctly.

Pass:

- no fatal or row error caused by missing/blank `OrderNumber`;
- invoice detail opens;
- no broken or fabricated order link;
- valid OrderNumber behavior does not regress.

Fail:

- import rejection or skipped row due to `OrderNumber`;
- detail failure;
- broken order link;
- regression for valid OrderNumber.

## 11. EBR-7/SERV-747 acceptance pack

Do not mark EBR-7 complete from source inspection or the presence of `net_amount`.

Preconditions:

- obtain explicit import authorization;
- use an organization/configuration that supports the discount fields;
- prepare controlled lines for `UnitPriceDiscount`, `ExtendedPriceDiscount`, or both according to supported file headers;
- record undiscounted and expected discounted values.

Run:

1. Import controlled order and invoice lines.
2. Verify stored/imported discount values.
3. Verify Order detail display.
4. Verify Invoice detail display.
5. Verify emailed Order rendering without sending to an unintended recipient.
6. Verify emailed Invoice rendering without sending to an unintended recipient.
7. Verify Order total.
8. Verify Invoice total.
9. Verify Backlog calculation.
10. Verify warehouse/Dashboard rollups use the intended discounted amount.

Record separately:

- unit-discount formula;
- extended-discount formula;
- display-on configuration;
- display-off configuration;
- imported header amounts versus line-derived rollups.

Pass only if the actual EBR-7/SERV-747 import, optional display, email display, and rollup criteria pass. Otherwise state the exact remaining gap or explicitly decline it.

## 12. Decision-only backlog recommendations

### EBR-474 / EBR-601

`PROCESS`: Current Jira still shows EBR-474 Triaging and EBR-601 Waiting for Client. Preserve EBR-601 as the likely canonical request because it is newer and already carries the waiting-client state. Keep EBR-474 as older non-canonical history pending Kylor's confirmation. Do not invent a SERV link.

### EBR-180 / SERV-2178

`PROCESS`: EBR-180 is Triaging and unassigned. SERV-2178 is In Progress, assigned to Brent, but last updated in 2025. Default recommendation: pause unless a current named customer is committed, upstream normalization is unavailable, and Kylor/Brent fund the XL import/schema/ETL/many-to-many scope.

### SERV-2196

`OPEN-DECISION`: Define bill-to versus ship-to precedence, prevalence, clients relying on current behavior, compatibility, and rollout before implementation. Keep it separate from SERV-2447.

### Ship-to casing

`CODE-IMPLICATION`: The case mismatch is real in source. `wwjc` cannot reproduce it. Choose an affected org with ship-to territory assignments, reproduce user-visible impact, and only then prepare a dedicated product/engineering pair.

### Amount contract

`OPEN-DECISION`: Keep imported Invoice header `NetAmount`, line-derived invoiced totals, ordered Dashboard rankings, freight, discounts, surcharges, and credits in a separate product decision. Do not promise one number everywhere.

### SERV-2214

`PROCESS`: Current Jira shows a To Do orphan about imported territories not appearing in eOL report filters. Inspect independently. Do not pair it with EBR-87 or include it in the reset without explicit evidence.

## 13. Exact manual action queue for Kylor

1. Have Brent/operator record the deployed production SHA and portal warehouse timestamp.
2. Treat the reproduced out-of-book Invoice, GET email-invoice, and Customer detail results as a failed P0.
3. Confirm the authorization containment package in section 4 as Package 1.
4. Review the six Jira replacement bodies in section 5.
5. Manually replace EBR-40 and SERV-2447.
6. Manually replace EBR-212 and SERV-2448.
7. Manually replace EBR-91 and SERV-2449.
8. Review and manually replace the four Confluence bodies in section 6.
9. Replace footer comment `1820655618` with the historical correction in section 7 if Confluence permits replacement; otherwise add one concise superseding note and do not continue the chain.
10. Apply the program-spine replacements in section 8.
11. Close the stale June 2026 Sprint through normal human board administration if still open.
12. Issue a fresh scoped GO naming only authorization containment.
13. Assign the selected package to Brent only after authority replacement and fresh GO.
14. Schedule SERV-2447/2448 regression validation after the first package.
15. Authorize and assign one SERV-2431 real-import acceptance.
16. Authorize and assign one EBR-7/SERV-747 discount acceptance.
17. Confirm EBR-601 as canonical or state why EBR-474 should remain canonical.
18. Resolve the stale active state on SERV-2178 by explicit continue/narrow/pause decision.
19. Do not create ship-to casing work until an affected-org reproduction exists.
20. Keep SERV-2196 and the amount contract as separate product decisions.

## 14. Plain-English briefing for Brent

The old Bet A is not ready for engineering because its three tickets do not share one proven defect. We tested the two headline territory claims with a real non-admin rep. The June Invoice total passed the stable baseline, and the Dashboard invoiced KPI matched Invoices. That makes SERV-2447 and SERV-2448 validation work, not permission to rewrite a shared resolver.

One Customers defect is real and small: Previous Month sales are calculated and exported but hidden on the page, and the CSV writes an unlabeled `Price Level Cue` value. The current SERV-2449 description expanded that into a scope block, totals row, generic header, duplicate columns, and relabeling that are not part of the customer problem. The replacement package fixes only the display rule, complete-result total, page/export parity, and CSV structure.

Before that starts, authorization containment must ship. The non-admin production probe failed: `betaverify` received HTTP 200 and protected content for an out-of-book Invoice, GET email-invoice page, and Customer detail. Dashboard gate-off sub-actions still need validation, but the three record exposures already make focused containment the first package.

After the first package, run the Invoice/Dashboard edge matrix. Passing routes become regression tests; each failing route becomes its own repair. Ship-to casing, bill-to/ship-to precedence, multi-value `RepNumber`, and amount semantics remain separate decisions.

## 15. Short Slack message to Brent

> I completed the Sales Portal reset pack. Unified Bet A stays retired: SERV-2447's June Invoice route passed (`$123,585` UI vs `$123,585.35` SQL), and SERV-2448's Dashboard KPI matched Invoices (`$836,263` each on Aug 4). The P0 authorization probe failed: non-admin `betaverify` received HTTP 200 and protected content for an out-of-book Invoice, GET email-invoice page, and Customer detail. Focused authorization containment is Package 1; narrowed Customers display/CSV work follows after it ships. Current `origin/master` is `4ff408492`; we still need the deployed SHA and Dashboard gate-off acceptance. No shared resolver, ship-to casing, `RepNumber`, or reporting amount work belongs in the containment package.
