# Decision — retire and restart Sales Portal Bet A

**Date:** 2026-08-04  
**Decision owner:** Kylor Johnson  
**Status:** Proposed decision for Kylor/Brent confirmation  
**Supersedes as engineering authority:** the 2026-07-24 unified Bet A GO and the current unified implementation plan  
**External systems:** Jira and Confluence remain unchanged; all corrections are manual

## Decision

Retire Bet A as a shared engineering package.

Do not send SERV-2447, SERV-2448, and SERV-2449 to engineering under their current descriptions or under the original “filter truth” implementation theory.

The three tickets do not represent one demonstrated defect, one root cause, or one justified refactor:

- SERV-2447's primary Invoice territory route passed.
- SERV-2448's primary Dashboard invoiced-KPI route passed.
- SERV-2449 contains two real Customers defects, but its acceptance criteria were expanded into an unsupported export redesign.

Preserve the evidence and ticket history. Retire the contaminated framing.

## Why this decision is necessary

Bet A began with a useful user promise:

> Territory, period, rows, totals, Dashboard, and export should be trustworthy.

It became an invalid engineering package because:

- symptoms that sounded related were assumed to share one implementation;
- admin sessions were treated as restricted-rep evidence;
- a stale `kal` example was promoted before valid reproduction;
- current-YTD values were treated as stable;
- `view_dashboard` was confused with the Sales Portal Dashboard gate;
- customer/ship-to territory was confused with invoice `RepNumber`;
- ship-to casing was incorrectly treated as a `wwjc` dependency;
- code risk was presented as production failure;
- questions and speculative improvements became approved scope without a named customer workflow;
- corrections were layered across Jira and Confluence instead of replacing stale bodies;
- Sprint changes made work disappear from Brent's board without a shared operational explanation.

The result no longer gives engineering a safe answer to “what should I build?”

## What survives the reset

### Verified production evidence

1. `wwjc/betaverify` is a valid restricted-rep fixture.
2. Gigi Lane, June 2026:
   - 110 invoices;
   - 75 accounts;
   - `$123,585.35`.
3. Invoice UI displayed `$123,585`, matching the closed SQL baseline within display rounding.
4. Dashboard and Invoices both displayed `$836,263` for the same Current-YTD Gigi Lane selection.
5. Customers Previous Month omitted the selected-period card and column.
6. Customers Previous YTD displayed the selected-period card and column.
7. The Customers CSV has more row values than headings.
8. The unlabeled value is `PriceLevel.cue_character`, not customer class.

### Valid product boundaries

- Customer and ship-to master assignments define normal territory.
- Invoice/order `RepNumber` is a separate, feature-gated access mechanism.
- `wwjc` does not exercise the ship-to casing defect.
- Current YTD is not a durable acceptance baseline.
- Warehouse refresh timing is part of territory verification.
- Imported header amounts and warehouse line totals can intentionally differ.
- Customers is an account-first workflow, not a generic reporting builder.

### Reusable test assets

- `betaverify`;
- six separate `105:1`–`105:6` territories;
- Gigi Lane June baseline;
- out-of-book authorization control:
  - customer `14378`;
  - invoice `INV65157`;
  - portal invoice id `4667912895`.

## What is retired

The following no longer authorizes engineering:

- one shared territory/filter resolver as Bet A's foundation;
- direct invoice `territory_key` matching as the default territory fix;
- a claim that SERV-2447 or SERV-2448 currently fails its primary route;
- a claim that ship-to casing blocks `wwjc`;
- admin screenshots as restricted-rep acceptance;
- a universal requirement that every date-range choice add a selected-period column;
- CSV scope/preamble block;
- CSV totals row;
- generic `Selected Range Sales` heading;
- broad CY/LY relabeling;
- unknown-date fallback as customer-facing acceptance;
- a new revenue definition;
- the unified 2026-07-24 Bet A GO.

## Ticket dispositions

### EBR-40 / SERV-2447

**Current verdict:** primary route passed; broad bug premise is unproven.

Recommended action:

- retire the current behavior-rewrite instruction;
- preserve the edge-case matrix;
- run focused regression assertions;
- close/reclassify if all pass;
- create a focused repair only for a reproduced failing root cause.

Required matrix:

- June row count and total;
- single selected territory;
- union of assigned territories;
- NULL territories;
- empty territories;
- all-totals user with explicit selection;
- actual ship-to-assigned organization;
- territory casing;
- collapsed blank ship-to key.

### EBR-212 / SERV-2448

**Current verdict:** invoiced KPI passed; residual Dashboard behavior remains.

Retain only:

- Top Customer membership validation;
- Top Product scope against order facts;
- drill-through parameter reproduction;
- focused parameter-propagation tests and repair if reproduced.

Do not rewrite the shared territory resolver.

### EBR-91 / SERV-2449

**Current verdict:** two small production defects exist; current specification is overdesigned.

Replacement problem:

> Sales reps and managers use Customers to review account sales for a selected period and export the same account list. Previous Month sales are calculated and exported but hidden on the page. The CSV also writes a price-level cue value without a matching heading.

Replacement acceptance:

1. Ranges not already represented by the standing Current YTD/Previous Year columns show the selected-period value.
2. The top selected-period total covers all accounts matching the current customer search and territory filter.
3. Export returns the same customer set and selected-period sales as the page.
4. Keep the human-readable period heading, such as `Previous Month Sales`.
5. Every CSV row has the same field count as the header.
6. Label the existing cue-character field `Price Level Cue`.
7. Preserve current revenue calculations and standing CY/LY behavior.
8. Preserve current bill-to/ship-to row math until the documented conflict is decided separately.

Explicitly excluded:

- scope/preamble block;
- totals row;
- generic period heading;
- duplicate Current YTD/Previous Year selected-period columns;
- new range choices;
- revenue changes;
- territory resolver work.

## P0 gate before replacement engineering

Run the authenticated production authorization probe.

### Fixture

- restricted user: `betaverify`;
- out-of-book customer: `14378` — MEG BRAFF DESIGNS;
- out-of-book invoice: `INV65157`;
- portal invoice id: `4667912895`;
- Dashboard-disabled non-admin user: `cmallon` or a confirmed equivalent.

### Routes

1. Record the deployed revision.
2. As `betaverify`, open:
   - `/wwjc/e/wwfc-2/invoices/INV65157`
   - `/wwjc/e/wwfc-2/email_invoice/4667912895` using GET only; do not send email
   - `/wwjc/e/wwfc-2/customers/14378`
3. As a non-admin whose Dashboard gate is off, call:
   - `/wwjc/e/wwfc-2/portal/invoice_total?date_range=current_ytd`
   - `/wwjc/e/wwfc-2/portal/top_customers?date_range=current_ytd`
   - `/wwjc/e/wwfc-2/portal/top_products?date_range=current_ytd`

Pass:

- deny, redirect, or not-found;
- no record or metric content.

Fail:

- any out-of-book customer/invoice content;
- any Dashboard metric while the Dashboard gate is false.

Decision rule:

- any fail → focused authorization containment is the first engineering package;
- all pass → document the deployed protection and proceed to the rewritten Customers package.

## Replacement portfolio

| Sequence | Package | Decision |
|---|---|---|
| P0 | Direct-route authorization probe | Run immediately |
| 1A | Authorization containment | Build first only if P0 fails |
| 1B | Customers selected-period display + CSV structure | Rewrite, then build if P0 passes |
| 2 | Invoice/Dashboard territory regression matrix | Validate; split only failing roots |
| 3 | SERV-2431 acceptance | Run one real import |
| 4 | EBR-7 discount acceptance | Verify before closure |
| 5 | EBR-474/601 dedupe | Keep EBR-601 canonical pending client evidence |
| 6 | EBR-180/SERV-2178 | Pause absent a current named customer and funding |
| Later | SERV-2196 | Product precedence/compatibility decision first |
| Later | Ship-to casing | Reproduce on an affected org before ticketing |
| Later | Amount contract | Separate product decision |

## Other backlog decisions

### EBR-180 / SERV-2178

Pause unless:

- a current named customer is committed to comma-separated `RepNumber`;
- upstream normalization is unavailable;
- Kylor and Brent explicitly accept the XL scope.

The ticket spans import, application schema, warehouse schema, ETL, and deduplication.

### SERV-2431

Ready to Accept. Run one authenticated import with missing/blank `OrderNumber`. Close if import and invoice detail behavior pass.

### EBR-7 / SERV-747

Do not close only because `net_amount` exists. Verify:

- discount import;
- order/invoice display;
- email display;
- order, invoice, backlog, and warehouse rollups.

### EBR-474 / EBR-601

Use EBR-601 as the likely canonical product record pending client evidence. Treat EBR-474 as older duplicate/non-canonical history.

### SERV-2196

Do not implement before deciding:

- bill-to versus ship-to precedence;
- clients relying on current behavior;
- compatibility;
- rollout.

### Ship-to casing

The code defect is real. `wwjc` cannot reproduce it. Select an affected org, capture user-visible impact, then create a separate pair.

## Authority cleanup required

Kylor must apply one coordinated manual correction pass:

1. Rewrite EBR-40/SERV-2447 as primary-route pass plus edge validation.
2. Rewrite EBR-212/SERV-2448 as KPI pass plus Top-N/drill-through residuals.
3. Replace EBR-91/SERV-2449 with the narrowed customer-aware package.
4. Replace or clearly supersede Confluence pages:
   - `1819836417`
   - `1819869185`
   - `1819901953`
   - `1820262402`
5. Update the program spine so it no longer authorizes unified Bet A or doctrine-closes EBR-7.
6. Close the stale June 2026 Sprint through normal human board administration.
7. Issue a fresh scoped GO only after the P0 result and authority replacement.

Do not add another correction-comment layer. Replace stale bodies and leave one concise historical note.

## Future-agent starting point

Future agents must read, in order:

1. `HANDOFF-CLOSE-FOUNDATION-AND-START-BETS-B-F-2026-08-04.md`
2. `PRE-JIRA-VERIFICATION-SALES-PORTAL-2026-08-04.md`
3. `BRENT-ENGINEERING-QUEUE-2026-08-04.md`
4. `00-SALES-PORTAL-SYSTEM-SPEC.md`
5. this decision

They must not begin by browsing Jira and inventing a new grouping.

## Confirmation needed

Kylor and Brent should explicitly confirm:

- unified Bet A is retired;
- P0 runs before replacement engineering;
- current 2447/2448 behavior work is not authorized;
- 2449 must be rewritten before implementation;
- SERV-2178 is paused unless a current business case is named;
- one coordinated authority correction will replace layered comments.
