# Sales Portal backlog reset — execution result and POV

**Date:** 2026-08-04  
**Owner:** Kylor Johnson  
**Mode:** read-only Jira, Confluence, production Postgres, and Rails source; no Jira changes made  
**Input:** `REVIEW-sales-portal-backlog-reset-2026-08-04.md`

## Bottom line

Retire Bet A as an engineering package.

The next move is not a shared territory resolver. It is:

1. run one urgent authorization probe;
2. if it passes, build a narrowed Customers display/CSV repair;
3. treat Invoice and Dashboard territory work as regression validation, not a presumed behavior rewrite;
4. explicitly pause the stale XL multi-rep story unless a current customer commitment funds it;
5. finish the small acceptance and dedupe work already sitting in the backlog.

The review's central verdict survived this execution pass. Live Jira and Confluence have not yet been brought into line with it, so engineering could still pick up the wrong package.

## What was run

- Re-read the current descriptions, comments, statuses, assignees, and Sprint fields for the relevant Jira inventory.
- Re-read the four Bet A Confluence pages and implementation-plan footer comment.
- Rechecked the `wwjc` production fixture in Postgres.
- Re-derived the closed June 2026 Gigi Lane baseline.
- Selected current out-of-book `wwjc` records for the authorization probe.
- Compared the checked-out Rails revision with current `origin/master`.
- Rechecked the access, Customers, Dashboard, and export paths in source.

## Facts that changed since the review's evidence cut

### Completed operational corrections

- `betaverify` is now correctly configured:
  - non-admin on both admin columns;
  - blank customer number;
  - user type `z'-Bet A Verify` (2864);
  - Dashboard and portal-total flags on;
  - all-customer totals off;
  - six distinct `105:1`–`105:6` territory array elements.
- SERV-2447, SERV-2448, and SERV-2449 all have no Sprint value. The stale June Sprint claim in comment 38300 is now operationally true.
- Confluence footer comment `1820655618` now correctly calls the unlabeled CSV field `Price Level Cue` and withdraws the false `wwjc` ship-to sequencing dependency.
- The closed acceptance baseline still holds: Gigi Lane, 2026-06-01 through 2026-06-30 = **110 invoices, 75 accounts, $123,585.35**.

### Still stale or wrong

- EBR-40 still says the territory filter “isn't working.”
- SERV-2447 still proposes unifying territory-scope paths even though the valid primary route passed and no failing edge test exists.
- EBR-212 and SERV-2448 still present a broad Dashboard filter package instead of the passed KPI route plus residual Top-N/drill-through work.
- EBR-91 and SERV-2449 still require:
  - a selected-range column for every range;
  - a scope block;
  - totals row;
  - stable `Selected Range Sales` header;
  - unknown-range fallback;
  - broader CY/LY labeling.

  Those are not the smallest customer-grounded repair.
- Confluence pages `1819836417`, `1819869185`, `1819901953`, and `1820262402` still describe Bet A as one authorized package. Two pages still say no acceptance criterion has executed, despite the valid Invoice and Dashboard primary-route passes.
- The active local program spine still says Bet A is a shared EBR-40/212/91 build and says EBR-7 can close “by doctrine.” Both are superseded by the independent review.

## Authorization gate — first action

### Why this is P0

The checked-out source is old (`d4a0e7d40`) and the working tree is 678 commits behind `origin/master`, but current `origin/master` (`0856f2d1a`) does not eliminate the risk:

- A general `require_sales_portal_access` callback has been added.
- Dashboard sub-actions still do not enforce the stricter Dashboard-specific gate used by `index`.
- Invoice `show` still resolves by organization and invoice number, not the user's permitted territory book.
- Invoice email still uses global `PortalInvoice.find(id)`.
- Customer detail still allows any non-customer user with a blank `customer_number`.
- Existing controller tests prove route availability, not out-of-book denial.

SERV-2199 is relevant precedent, but it fixed the general “hidden menu, direct URL still opens Sales Portal” class. It does not prove record-level territory authorization.

Before interpreting a production result, Brent should identify the deployed revision. The source comparison proves the risks remain on current `origin/master`; it does not prove production is running that exact revision.

### Exact production probe

Use an authenticated non-admin session. Do not email anything; GET the email route only.

Out-of-book control selected from current production data:

- Customer: `14378` — MEG BRAFF DESIGNS
- Customer territories: `D6 LORNE GARDNER`, `30440 Interim Rep House Account`
- Invoice: `INV65157`
- Portal invoice id: `4667912895`
- Invoice date/amount: 2026-08-04 / $100.00
- `betaverify` holds only `105:1`–`105:6`, so this record is outside its permitted book.

Run:

1. Record the deployed revision.
2. As `betaverify`, open `/wwjc/e/wwfc-2/invoices/INV65157`.
3. As `betaverify`, GET `/wwjc/e/wwfc-2/email_invoice/4667912895`.
4. As `betaverify`, open `/wwjc/e/wwfc-2/customers/14378`.
5. As a non-admin portal user whose user type has the Dashboard flag off, such as `cmallon`, call:
   - `/wwjc/e/wwfc-2/portal/invoice_total?date_range=current_ytd`
   - `/wwjc/e/wwfc-2/portal/top_customers?date_range=current_ytd`
   - `/wwjc/e/wwfc-2/portal/top_products?date_range=current_ytd`

**Pass:** deny, redirect, or not-found with no record or metric content.  
**Fail:** any out-of-book invoice/customer content or Dashboard metric is returned.

### Decision rule

- **Any fail:** authorization hotfix becomes the first package. Scope it to controller gates and territory-authorized record resolution. Do not fold in Customers period work or territory-resolver refactoring.
- **All pass:** record the deployed protection that blocks the code-demonstrated path, then proceed immediately to the narrowed SERV-2449 package.

This browser-authenticated probe could not be executed through the available read-only database/Jira tooling. It is the only P0 gate still requiring a human session.

## First engineering package if P0 passes

### Narrow EBR-91 / SERV-2449 to required correctness

**Problem**

Sales reps and managers use Customers to review account sales for a selected period and export the same account list. Previous Month sales are calculated and exported but hidden on the page. The CSV also writes a price-level cue value without a matching heading.

**Done when**

1. Ranges not already represented by the standing Current YTD/Previous Year columns show their selected-period total and per-customer value.
2. The top selected-period total covers every account matching the current customer search and territory filter, not only the visible page.
3. Export returns the same customer set and selected-period sales as the page.
4. Keep the existing human-readable period heading, such as `Previous Month Sales`.
5. Every CSV row has the same field count as the header.
6. Label the existing cue-character field `Price Level Cue`.
7. Preserve the existing revenue calculation and Current YTD/Previous Year behavior.
8. Preserve current bill-to/ship-to row math in this package. The conflicting product statements about whether territory selects accounts only or also constrains ship-to sales require a separate explicit decision before any row-math change.

**Exclude**

- scope/preamble block;
- totals row;
- generic `Selected Range Sales` heading;
- duplicate selected-period columns for Current YTD/Previous Year;
- broad CY/LY relabeling;
- new date-range choices;
- revenue-definition changes;
- territory resolver refactor.

**Required tests**

- Previous Month renders; Previous YTD remains a passing comparison.
- Standing Current YTD/Previous Year columns are not duplicated.
- Search and territory filters affect the complete matching customer set.
- UI and export customer sets and selected-period sums agree.
- CSV header count equals every row count, with `Price Level Cue` present.

## Territory work after SERV-2449

### SERV-2447

Do not authorize a shared resolver rewrite.

Add or run focused assertions for:

- June Gigi Lane row count = 110 and total within rounding/tolerance of $123,585.35;
- one selected territory;
- union of multiple assigned territories;
- NULL territories fail closed;
- empty-array territories fail closed;
- explicit selection narrows an all-totals user;
- one actual ship-to-assigned org;
- customer and ship-to territory casing;
- collapsed NULL ship-to key behavior.

If all pass, close or reclassify SERV-2447 as regression coverage. If one fails, split the failing root cause into a focused repair.

### SERV-2448

The primary KPI route passed. Retain only:

- Top Customer membership validation;
- Top Product validation against territory-scoped orders/order lines;
- production reproduction of dropped drill-through filters on graph, Orders, and Top-N/customer destinations;
- focused parameter-propagation tests and fix if reproduced.

The Invoice KPI link already passes `report_params`, including `multi-select-filters`; do not rewrite that passing link merely because sibling destinations omit the filter.

Do not refactor the underlying resolver merely because Dashboard and Invoice paths are separate.

## Explicit backlog decisions

### EBR-180 / SERV-2178 — pause

Recommendation: **pause** unless a current named customer is committed to the comma-separated RepNumber model and an upstream normalization alternative is unavailable.

Evidence:

- EBR-180 is Triaging and unassigned.
- SERV-2178 is still In Progress and assigned to Brent, but its last activity is 2025.
- Engineering sized it XL and explicitly paused pending business-case confirmation.
- The implementation spans import, application schema, warehouse schema, ETL, and many-to-many deduplication.

The current Jira state suggests active work when the comment history says paused. Resolve that contradiction manually.

### SERV-2431 — accept after one real import

The ticket is Ready to Accept and local import/UI checks passed. Run one authenticated staging or safe production import with missing/blank `OrderNumber`. If it imports and the invoice detail opens without a broken order link, accept and close. Do not leave it in the stale active June Sprint.

### EBR-7 / SERV-747 — verify, do not doctrine-close

SERV-747 is Done, but EBR-7's actual criteria include import, optional display, email display, and rollup behavior for line-item discounts. `net_amount` alone does not prove those criteria.

Run a compact acceptance:

1. import UnitPriceDiscount and/or ExtendedPriceDiscount;
2. verify order/invoice and email display behavior;
3. verify Order, Invoice, Backlog, and warehouse rollups use discounted amounts.

Close EBR-7 only if those pass or explicitly decline the remaining product request.

### EBR-474 / EBR-601 — make EBR-601 canonical

Both describe Savoy invoice status import/filtering and NetSuite population. EBR-601 is the newer record and is already Waiting for Client; EBR-474 carries the declined 2023 estimate and older history.

Recommendation: preserve EBR-601 as canonical pending client evidence and mark EBR-474 duplicate/non-canonical through normal human Jira administration.

### SERV-2196 — product decision before code

Keep separate. Define bill-to versus ship-to precedence, prevalence, compatibility, and rollout before implementation.

### Ship-to casing — reproduce before ticketing

The code defect is real, but `wwjc` cannot exercise it. Use an affected org with ship-to territory assignments, capture a before/after, then create a dedicated pair. Do not put it back into EBR-40.

## Authority cleanup

Do one coordinated replacement pass, not another comment layer:

1. Rewrite EBR-40/SERV-2447 as “primary route passed; edge validation only.”
2. Rewrite EBR-212/SERV-2448 as “KPI passed; Top-N and drill-through residuals.”
3. Replace EBR-91/SERV-2449 acceptance with the narrowed package above.
4. Replace or clearly supersede the four old Bet A Confluence bodies.
5. Update `00-PROGRAM-SPINE.md` so it no longer authorizes one shared Bet A implementation or doctrine-closes EBR-7.
6. Name this POV and the independent review as the PM authority until Jira/Confluence descriptions are corrected.
7. After the P0 result and correction pass, Kylor must issue a fresh scoped GO for either the authorization hotfix or narrowed SERV-2449. The 2026-07-24 unified Bet A GO must not authorize the replacement portfolio.

Jira remains read-only for agents. Kylor must apply or explicitly authorize each external change.

## Recommended sequence

| Order | Work | Gate | Outcome |
|---|---|---|---|
| 0 | Direct-route authorization probe | Authenticated non-admin browser session | Hotfix first if any exposure |
| 1 | Authority rewrite | Kylor-approved Jira/Confluence replacement pass | Engineering receives current scope |
| 2 | Fresh scoped GO | P0 outcome and authority rewrite complete | Authorizes only the selected first package |
| 3 | Narrow SERV-2449 | P0 passes or authorization hotfix ships | Small customer-visible correctness fix |
| 4 | SERV-2447/2448 edge matrix | Failing test or production reproduction required for behavior changes | Close/reclassify passes; split failures |
| 5 | SERV-2431 acceptance | One real missing-OrderNumber import | Close ready work |
| 6 | EBR-7 acceptance | Discount fixture | Close or state remaining gap |
| 7 | EBR-474/601 dedupe | Product-owner confirmation | EBR-601 canonical |
| 8 | SERV-2178 decision | Named customer and funding | Default pause |
| Later | SERV-2196, ship-to casing, amount contract | Separate product evidence | Independent bets |

## POV

The product should stop treating “filter truth” as one architecture program. The valid organizing principle is a user promise, not a shared implementation.

The immediate portfolio is:

- one access-containment gate;
- one small, proven Customers correctness fix;
- one regression-hardening pass on territory behavior;
- several explicit product decisions that should not consume engineering until evidence or customer commitment exists.

That sequence reduces both kinds of risk exposed by this review: shipping a speculative refactor for bugs that did not reproduce, and allowing a code-demonstrated authorization gap to sit behind lower-severity reporting work.

