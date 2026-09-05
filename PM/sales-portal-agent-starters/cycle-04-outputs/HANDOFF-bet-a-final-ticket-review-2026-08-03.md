# HANDOFF — independent final review of Bet A Jira ticket rewrites

**Date:** 2026-08-03  
**Owner:** Kylor Johnson (PO)  
**Mode:** review only — do not change Jira, Confluence, local files, ticket status, or comments  
**Requested outcome:** tell Kylor whether the revised tickets are ready to send to Brent, and list only concrete required fixes if they are not.

---

## Why this review is needed

Several prior sessions generated long, overlapping comments, AC documents, drafts,
and Confluence changes around Bet A. Kylor has now manually rewritten the six
linked Jira descriptions to make them short and human-readable. He wants an
independent, skeptical final check before telling Brent they are ready.

Do not rubber-stamp the changes. Verify the live ticket descriptions and comments
against the actual request below. Be particularly careful not to confuse a code
diagnosis, SQL expectation, or admin capture with a live user reproduction.

---

## Brent's actual request — the review standard

Brent said:

> "we just want to see a more human explanation like 'when I change the filter it
> doesn't update' with a link to a page that I can reproduce. Then, when I change
> the code, I can test that and see it working and see it working."

He also proposed a short discussion around:

1. **What is territory?** A property of the customer, or of the sale?
2. **Do we correct numbers that are wrong but established?**
3. **How will we know it is fixed, and who says so?**

The current ticket set should give an engineer:

- a plain-English problem statement;
- a usable production route where a current reproduction is genuinely available;
- a short, observable definition of done;
- the product answer to each of Brent's three questions;
- no stale capture presented as proof.

It should not make unverified claims merely to create a neat ticket.

---

## Non-negotiable safety rules

- **Jira is read-only.** Do not use any Jira write tool: no edits, comments,
  transitions, links, or worklogs. Draft feedback in chat only.
- **Confluence is read-only unless Kylor explicitly asks for an edit.**
- Do not delete or modify local files.
- Do not broaden the review into a new design or code implementation.
- Do not treat the legacy Insightful folders as relevant to this work.

---

## Six live tickets to inspect

Read each live description fresh. Also read the recent Brent question comment and
Kylor's substantive answer comments when needed to verify a statement.

| Product ticket | Engineering ticket | Subject |
|---|---|---|
| [EBR-40](https://supercatsolutions.atlassian.net/browse/EBR-40) | [SERV-2447](https://supercatsolutions.atlassian.net/browse/SERV-2447) | Invoice territory filter |
| [EBR-212](https://supercatsolutions.atlassian.net/browse/EBR-212) | [SERV-2448](https://supercatsolutions.atlassian.net/browse/SERV-2448) | Dashboard territory filter |
| [EBR-91](https://supercatsolutions.atlassian.net/browse/EBR-91) | [SERV-2449](https://supercatsolutions.atlassian.net/browse/SERV-2449) | Customers date-range sales and CSV export |

### Current rewrite shape (verify, do not assume)

Kylor has replaced all six Description fields:

- EBR tickets are short product summaries, each pointing to its SERV implementation
  ticket.
- SERV tickets contain the plain-language problem, a verification/reproduction route,
  a short “Done when” list, and narrow diagnosis/out-of-scope notes.
- SERV-2449 has two embedded screenshots intended to show:
  1. `previous_month` — selected-range column missing;
  2. `previous_ytd` — selected-range column present.
- Kylor is adding a separate **Revenue decision** section to EBR-40 immediately
  after **Product decision**. Confirm it exists before review:

  > Keep the existing displayed revenue calculation. This work fixes territory and
  > date-range scope; it does not recalculate established sales figures or change
  > the revenue definition.

The exact current contents matter more than this summary.

---

## Product decisions already made

These are not open engineering decisions. The descriptions should express them
simply, without re-litigating the implementation detail.

### Decision 1 — territory semantics

Territory is a property of the **customer/location master**:

- bill-to assignment, plus ship-to location assignment for organizations using
  that model;
- it selects the customer accounts visible in the result;
- it does **not** assign or slice an invoice from the invoice's rep/territory field.

Invoice-rep matching is out of scope: `EBR-180` / `SERV-2178`.

### Decision 2 — established revenue figures

Keep the current displayed revenue calculation. Bet A corrects territory scope,
date-range alignment, labels, and export structure. It does **not** introduce a
new revenue definition or reopen the EBR-7 discount rebuild.

`SUM(portal_invoices.net_amount)` is a reconciliation baseline, while portal
displayed totals can use `sales_fact.amount_invoiced`. Do not require a false exact
match caused by known proration differences.

### Decision 3 — how “fixed” is accepted

Engineering should provide automated coverage for the stated behavior. Kylor is the
PO acceptance owner unless he names a different owner. A sales-portal user sponsor
has not yet been named; Brent specifically raised the need to engage one.

The review must say whether that is sufficiently explicit in the tickets. Do not
invent a sponsor. Recommend one concise next step if it is missing.

---

## Evidence facts and traps

### SERV-2449 — confirmed live reproduction

This is the clean, immediately reproducible ticket:

- Broken route:
  `https://supercat.supercatsolutions.com/wwjc/e/wwfc-2/customers?date_range=previous_month`
- Working comparison:
  `https://supercat.supercatsolutions.com/wwjc/e/wwfc-2/customers?date_range=previous_ytd`
- The selected-range column is hidden on six standard ranges and appears for
  `previous_ytd` and `custom`.
- The export has a structural defect: 9 headers and 10 data fields; the unlabeled
  tenth field contains customer class values such as `DN` and `WS`.
- Root cause: `ecat_customers_controller.rb` uses a Ruby `String#[]` substring
  check around line 294, so it mistakenly gates display on whether the range name
  contains `previous_ytd` or `custom`.

Review the two embedded screenshots. They need clear captions or adjacent text
that identifies which is the broken view and which is the working comparison.

### SERV-2447 and SERV-2448 — do not overclaim a live reproduction

Their routes are useful verification routes:

- Invoices:
  `https://supercat.supercatsolutions.com/wwjc/e/wwfc-2/invoices?date_range=current_ytd&multi-select-filters%5B%5D=%5B%22territory%22%2C%22105%3A1%20gigi%20lane%22%5D`
- Dashboard:
  `https://supercat.supercatsolutions.com/wwjc/e/wwfc-2/portal`

But a valid production before/after capture for the rep-shaped territory case is
not currently established.

Why:

- `OrgUser#is_admin?` treats either `org_users.is_admin` **or** `users.is_admin`
  as admin. Admin accounts bypass normal territory permission logic.
- Historical captures on `Kylor_Johnson` were admin captures and are invalid for
  territory acceptance criteria.
- As of an August 3 read-only Postgres check, `Kylor_Johnson` had
  `org_users.is_admin = false` but `users.is_admin = true`. The test group was
  `z'-Bet A Verify` and the six territories were assigned, but the global admin
  flag still invalidated the account as a normal-rep test fixture.
- All 22 wwjc user types were previously verified with `view_dashboard = false`;
  a dashboard-enabled non-admin multi-territory fixture has not been independently
  confirmed.

The descriptions must be candid that these are verification routes and that a
valid fixture is still needed. They should not claim the old admin screenshots
prove the bug.

### Operational detail to keep out of Brent-facing prose

The portal reads territory assignments from a warehouse bridge, not directly from
the live `org_users.territory_codes` field. That affects fixture setup, but it is
not the human bug statement. It can remain as a brief diagnosis pointer if needed;
do not make it the headline or a reason to block SERV-2449.

---

## Existing comment history

Brent posted his detailed engineering questions on:

- EBR-40 — program/revenue/PR-shape questions;
- SERV-2447 — territory semantics, rollout, all-totals selection, empty state,
  ETL timing, and verification questions;
- SERV-2448 — dashboard fixture and related dashboard scope questions;
- SERV-2449 — calendar columns, reconciliation, territory semantics, CSV naming,
  totals row, and date-range hardening questions.

Kylor posted detailed answers. Those comments are historical context; do not demand
that all of their code-level detail be copied into the newly short descriptions.
The new descriptions should be the straightforward implementation entry point,
while comments retain the decision record.

There were also duplicate/reposted description comments and invalid admin-capture
comments in this history. Do not delete anything during this review.

---

## Local sources to read

These active files contain the evidence trail and previous drafts:

1. `PM/sales-portal-agent-starters/cycle-04-outputs/HANDOFF-bet-a-ticket-rewrite-2026-08-03.md`
   — original rewrite objective, verified facts, and constraints.
2. `PM/sales-portal-agent-starters/cycle-04-outputs/BET-A-AC-HUMAN-REPRO-draft.md`
   — detailed human repro research; use only to verify facts, not as a model for
   ticket length.
3. `PM/sales-portal-agent-starters/cycle-04-outputs/TICKET-EDITS-bet-a-2026-07-30.md`
   — superseded long paste drafts; structural/evidence reference only.
4. `PM/sales-portal-agent-starters/cycle-04-outputs/JIRA-EDITS-bet-a-2026-07-29.md`
   — untrusted earlier draft; do not treat as authority.
5. Rails source when needed: `~/supercat-code/supercat_server`.

Useful code references:

- `warehouse_access.rb`:
  `territory_code_limit_common_table_expression` around lines 999–1059.
- `ecat_customers_controller.rb` around lines 293–295.
- `ecat_customer.rb` around lines 113–122.

Do not read frozen legacy Insightful folders.

---

## Exact review tasks

1. Read all six current descriptions live from Jira.
2. Read Brent's relevant questions and Kylor's answers only as needed to validate
   the short descriptions.
3. For each ticket, answer:
   - Is the plain-English statement accurate and understandable to an engineer?
   - Does it have a valid direct route, or candidly explain why a valid live
     before-state is not yet available?
   - Is “Done when” observable and appropriately scoped?
   - Does it contradict a verified fact, decision, or current comment?
   - Is the EBR/SERV pairing clear without duplicating a design document?
4. Inspect SERV-2449 attachments/captions. Confirm the images actually correspond
   to the stated broken and working views.
5. Check that the three Brent decisions are explicitly and consistently answered.
6. Return a brief, decisive review:
   - **GREENLIGHT** or **NOT READY**;
   - up to five required edits, each naming the ticket and exact change;
   - a one-paragraph suggested Slack message to Brent.

Do not propose speculative new scope, new tickets, or architecture. Do not write to
any external system.

---

## Desired final state

Kylor should be able to tell Brent:

> “The six linked tickets now state the product choices plainly. Each SERV ticket
> tells you what is wrong, where to look, and what done means. SERV-2449 has a live
> before/after proof. SERV-2447 and SERV-2448 are candid about the remaining
> production-fixture gap rather than using invalid admin evidence. I am the PO
> acceptance owner and will identify a sales-portal sponsor for final validation.”

The reviewer should approve that statement only if the live ticket contents
support it.
