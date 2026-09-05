# HANDOFF — pre-send verification of Bet A claims

**Date:** 2026-08-04
**Owner:** Kylor Johnson (PO)
**Mode:** verify only — read-only against Jira, Confluence, Postgres, and the Rails source
**Requested outcome:** confirm or refute every claim listed below, then return **SEND** or **DO NOT SEND** with a numbered list of corrections.

---

## Why this handoff exists

A prior session rewrote six Bet A Jira tickets, posted a four-point correction comment
on SERV-2447, and drafted two Slack messages for Brent Sanders (CTO). Most of that work
is **already applied and already visible to Brent** — he has read at least one ticket and
has asked to step through it live.

One reply message is drafted but **not yet sent**. Before Kylor sends it, every factual
claim needs an independent skeptical check. Several claims are load-bearing in a way that
makes a mistake expensive:

- They are stated to the CTO as verified fact.
- Some are **already published** in Jira comment `38300`, so an error there is already public.
- A wrong claim about Brent's own user account will be disproved by Brent in about ten seconds.

**Do not rubber-stamp.** The previous session already corrected one significant factual
error of its own (`view_dashboard` versus `enable_portal_dashboard`), which is direct
evidence that this material can be got wrong. Assume more errors exist and go find them.

---

## Non-negotiable safety rules

- **Jira is read-only.** No `editJiraIssue`, `addCommentToJiraIssue`, `transitionJiraIssue`,
  `createJiraIssue`, `createIssueLink`, or `addWorklogToJiraIssue`. Draft all corrections
  as text for Kylor to apply himself.
- **Confluence is read-only.** Do not create or update pages or comments.
- **Postgres is read-only.** `SELECT` only. No DDL, no writes, no `ANALYZE`-style side effects.
- Do not edit or delete local files other than creating your own output file.
- Do not expand scope into new design, new tickets, or code implementation.
- Do not read the frozen legacy Insightful folders.

---

## Ticket map

| Product | Engineering | Subject |
|---|---|---|
| [EBR-40](https://supercatsolutions.atlassian.net/browse/EBR-40) | [SERV-2447](https://supercatsolutions.atlassian.net/browse/SERV-2447) | Invoice list territory filter |
| [EBR-212](https://supercatsolutions.atlassian.net/browse/EBR-212) | [SERV-2448](https://supercatsolutions.atlassian.net/browse/SERV-2448) | Dashboard territory filter |
| [EBR-91](https://supercatsolutions.atlassian.net/browse/EBR-91) | [SERV-2449](https://supercatsolutions.atlassian.net/browse/SERV-2449) | Customers date-range sales and CSV export |

Confluence pages in play:

- `1820262402` — Bet A Eng Implementation Plan (SERV-2447 / 2448 / 2449)
- `1819836417` — Bet A Filter Truth AC
- `1819869185` — Bet A Eng Handoff / code map
- `1819901953` — Bet A Verification & Evidence (wwjc)

---

## Current live state as read on 2026-08-04, ~11:00 MT

Re-read all of this yourself; it may have moved since.

| Ticket | Status | Sprint | Description state |
|---|---|---|---|
| EBR-40 | Approved | — | Rewritten, has Product decision + Revenue decision + Acceptance |
| EBR-212 | Approved | — | Rewritten, has Acceptance |
| EBR-91 | Approved | — | Rewritten, has Acceptance |
| SERV-2447 | To Do | cleared | Rewritten, has Territory semantics + Acceptance |
| SERV-2448 | To Do | cleared | Rewritten, has Verification setup + Acceptance |
| SERV-2449 | To Do | **still June 2026 (id 651)** | Rewritten but **damaged** — see D1 |

Comments present: SERV-2447 has `38270, 38275, 38279, 38287, 38290, 38300`.
SERV-2448 has `38271, 38276, 38280, 38288`.

Comment **`38300`** on SERV-2447 (created 2026-08-03 18:25 ET) is the four-point
correction. It is live and Brent can see it. Its full text is in the ticket; read it
directly rather than trusting any summary of it.

---

## Known open defects — confirm these, then confirm nothing else is wrong

These four were found but **not yet fixed**. Verify each is real, then verify the proposed
fix is correct and complete.

**D1 — SERV-2449 description has a duplicated tail.**
The description renders `Diagnosis pointers` and `Out of scope` **twice each**: once in the
correct position, then the original pair again at the very bottom. Proposed fix: delete
everything after the first `Out of scope` block.

**D2 — SERV-2449 screenshot captions are wrapped in backticks.**
Both captions render as grey inline code instead of prose. Proposed fix: remove the
backticks from `Previous Month — the selected-range sales column is missing` and
`Previous YTD — the selected-range sales column is present`.

**D3 — SERV-2449 Sprint field is still June 2026, and comment 38300 already claims otherwise.**
The last line of `38300` states "I've also cleared the Sprint field on all three SERV
tickets." That is currently false for SERV-2449. This is also the reason Brent thinks two
tickets were deleted: 2447 and 2448 dropped off the June board when their sprint was
cleared, leaving 2449 as the only one visible. Proposed fix: clear SERV-2449's Sprint,
which makes the published comment true and needs no comment edit. **Confirm that clearing
it does not orphan the ticket from a board Brent relies on.**

**D4 — EBR-40 "Done when" contains a contradictory leftover bullet.**
Two bullets sit side by side:

> - A user with no territories and no all-customer-sales-totals permission sees no customer data, never company-wide data.
> - A user with no territories sees no customer data, never company-wide data.

The second is the old unqualified version and contradicts both the first bullet and the
all-customer-totals carve-out stated in SERV-2447. Proposed fix: delete the second bullet.
Also `**Done** when` has the bold markers misplaced; it should be `**Done when**`.

---

## Tier 1 — claims about Brent's account. Highest risk. Verify first.

These go directly into the message to Brent and describe *his* screen. If any is wrong he
will know immediately.

**T1.1 — Brent's wwjc account configuration.**

Claim: `brentsanders` on org `wwjc` is `org_users.is_admin = true`, `users.is_admin = true`,
user type id **1378 "ATL Sales Reps"**, with `display_sales_portal_totals = 'false'`,
`enable_portal_dashboard = 'false'`, `access_all_customer_sales_totals = 'false'`, and
`territory_codes` NULL.

Check:

```sql
SELECT u.username, ou.is_admin AS ou_admin, u.is_admin AS u_admin,
       ut.id AS ut_id, ut.name AS user_type,
       ((ut.properties::jsonb)->'flags')->>'display_sales_portal_totals' AS totals_flag,
       ((ut.properties::jsonb)->'flags')->>'enable_portal_dashboard'     AS dash_flag,
       (ut.permissions::jsonb)->>'access_all_customer_sales_totals'      AS all_totals,
       ou.territory_codes
FROM org_users ou
JOIN users u ON u.id = ou.user_id
JOIN organizations o ON o.id = ou.organization_id
LEFT JOIN user_types ut ON ut.id = ou.user_type_id
WHERE o.shortname = 'wwjc'
  AND u.username IN ('Kylor_Johnson','brentsanders','cmallon');
```

Also confirm `Kylor_Johnson` is on user type **2864 `z'-Bet A Verify`** with
`display_sales_portal_totals = 'true'`, and note that he is `org_users.is_admin = false`
but `users.is_admin = true`.

**T1.2 — the totals flag hides the entire stat-card band.**

Claim: `app/views/ecat_customers/index.html.erb` line 36 opens
`<% if @current_org_user.user_type.display_sales_portal_totals %>`, the block closes at
line 101, and all four stat cards — LY Sales Total, CY Sales Total, the selected-range
Sales Total, Backlog Total — are inside it. Therefore Brent sees **none** of them.

Check the file directly. Confirm the line numbers and that the selected-range card
(gated on `@custom_totals_by_bill_to.present?`, around line 68) is nested inside the
outer flag block.

**T1.3 — admin status does not override the totals flag.**

Claim: line 36 is a **direct attribute read** on the user type, not a call through
`UserTypePermissions.may?`, so the admin short-circuit in `may?` does not apply and
Brent's admin rights do not make the cards appear.

Check: read `app/models/user_type_permissions.rb` around `self.may?` (~line 117) and
confirm the admin short-circuit lives there and only there. Then confirm nothing between
the view and `UserType#display_sales_portal_totals` routes through `may?`. Look at
`UserType::FLAGS` (~line 539) and `get_flag`. **If the flag defaults to `true` when
absent, confirm that wwjc type 1378 has it explicitly set to false rather than merely
missing** — the SQL above returns the raw JSON value, so distinguish `'false'` from `NULL`.

**T1.4 — the per-row column IS visible to Brent.**

Claim: `render 'list'` sits at `index.html.erb` line 103, **outside** the flag block, and
`_list.html.erb` gates the selected-range column only on `@custom_totals_by_bill_to.present?`
at lines 13 and 37. So Brent can still see the column appear on `previous_ytd` and vanish
on `previous_month`, even with the totals flag off.

Also verify the claim that `@custom_totals_by_bill_to` is populated independently of the
totals flag — trace where the controller sets it and confirm no permission gate.

**T1.5 — the column header text.**

Claim: the header is `"#{@dataflow[:date_range_filter_label]} Sales"`, from
`ecat_customers_controller.rb` line 386 (`custom_range: { label: ... }`), so on
`previous_ytd` it reads **"Previous YTD Sales"** and sits between "CY Sales" and "Backlog".

Confirm the exact rendered string, and confirm the ordering against `_list.html.erb`
lines 11–16.

**T1.6 — the proposed remedy is safe.**

Claim: moving `brentsanders` on wwjc to user type **2864 `z'-Bet A Verify`** makes his view
match Kylor's captures, and flipping `display_sales_portal_totals` on type **1378** instead
would be wrong because 1378 is a live type with real showroom users.

Check: how many non-deleted org_users are on type 1378, and who. Confirm 2864's full flag
and permission set so that moving Brent onto it does not grant or remove something
unintended. **Flag any side effect** — for example whether 2864's customer syncing or
price-level visibility differs from 1378 in a way that changes what Brent sees on other pages.

---

## Tier 2 — claims already published in Jira comment 38300

These are public. If any is wrong, Brent has already read a false number and Kylor owes a
correction comment. Re-derive each from Postgres rather than trusting the comment.

**T2.1** — `z'-Bet A Verify` (type 2864) on wwjc has `enable_portal_dashboard` on,
`display_sales_portal_totals` on, `access_all_customer_sales_totals` off, customer syncing
All; and the **org-level** `enable_portal_dashboard` flag on wwjc is on.

**T2.2** — The Sales Portal dashboard gate is `should_display_portal_dashboard?` in
`app/helpers/ecat_permissions_helper.rb` lines 54–59, reading the `enable_portal_dashboard`
flag from `user_types.properties`, and is **not** the Admin Console `view_dashboard`
permission. Confirm the earlier "all 22 wwjc user types have `view_dashboard: false`" claim
is indeed irrelevant to the portal dashboard. Then check whether the superseded version of
that claim still sits uncorrected in comment `38276` or `38288` on SERV-2448, or on
Confluence page `1819901953`.

**T2.3** — `invoice_dimension.territory_key` is built as
`format_territory_key(org_id, portal_invoice.rep_number)`. Verify at
`app/services/warehouse/extracts_and_transforms/sales_portal_invoice_dimension.rb` ~line 34.
This is the basis for ruling invoice `territory_key` matching out of scope as EBR-180 work.

**T2.4** — Enabling the invoice territory match on wwjc would newly surface
**29 invoices / $43,093.69** YTD, and would be a **no-op** for `105:1 Gigi Lane` because
**51 of 72** distinct wwjc `rep_number` values are comma-joined composites such as
`40 DANIEL RATCHFORD,105:1 Gigi Lane` that can never equal a territory key. Re-derive both
numbers and state the exact date window used, since YTD drifts.

**T2.5 — the ship-to casing defect.** Claim: `all_territory_codes_for_organization`
downcases territory codes while `TerritoryToShipToBridge` keys on raw codes
(`shipping_location_id_map[territory_code]`, ~line 25), affecting roughly **150,000**
ship-to records across 15+ orgs — cci 75,114, ta 39,610, clli 11,545, kii 10,123, el 3,956,
gl 2,349. Verify the code path in
`app/services/warehouse/extracts_and_transforms.rb` (~lines 24, 32, 41) and
`.../territory_to_ship_to_bridge.rb`, then re-derive the per-org counts.

**T2.6 — wwjc and kal are unaffected by T2.5.** Claim: wwjc has **0 of 14,020** ship-tos
carrying a territory code, and kal's **3,709** are all lowercase or numeric, so the casing
defect cannot explain the original kal / 0016 false negative and will not move a wwjc
baseline. **This is the single most consequential claim in the set** — it is the reason
Bet A is not blocked on the casing fix, and the reason two statements in Confluence comment
`1820655618` are being called wrong. Verify it carefully and independently.

**T2.7 — baselines and drift.** Claim: `105:1 Gigi Lane` current YTD is now
**762 invoices / $830,845.72** against the ~710 / $777k written on the ticket; cmallon's
union of six territories is **1,508 / $1,555,691.19** against ~1,404 / $1.46M; and June 2026
for `105:1 Gigi Lane` has read **110 invoices / 75 accounts / $123,585.35** on five separate
derivation dates. Re-derive all three. State your derivation date. If the "five separate
derivation dates" claim cannot be substantiated from an artifact, say so — it is an
evidentiary claim, not a measurement.

**T2.8 — sprint state.** Claim: June 2026 (id 651) is still the only open sprint on board 3
and is still marked `active` despite an end date of 2026-06-26.

---

## Tier 3 — supporting claims

**T3.1** — `cmallon` on wwjc is non-admin on **both** columns, carries six territories
`105:1` through `105:6`, and has all-customer totals off. SERV-2447 names this account as
the valid fixture. The territory list specifically was **not** re-verified in the last
session — check it.

**T3.2** — `OrgUser#is_admin?` (~line 383 of `app/models/org_user.rb`) returns true if
**either** `org_users.is_admin` or `users.is_admin` is set, which is what invalidated the
2026-07-28 captures.

**T3.3** — The substring gate: `ecat_customers_controller.rb` ~line 294,
`params['date_range']['previous_ytd'] || params['date_range']['custom']`, is a Ruby
`String#[]` substring test. Confirm which of the ranges in `Eol::DateRanges::DATE_RANGES`
pass and which fail, and confirm the ticket's claim about how many are affected.

**T3.4** — `ecat_customer.rb` ~lines 113–122: calendar-year values ignore
`params[:date_range]`.

**T3.5** — The CSV structural defect: 9 header fields against 10 data fields, with the
unlabeled tenth carrying customer class values such as `DN` and `WS`. Confirm from the
export code, not from an old note.

**T3.6** — `:territory_access_via_rep_number` is enabled for `el` and **not** for `wwjc`
(`config/initializers/enabled_features.rb` ~line 75). Note that the local checkout may
differ from production configuration — say which you verified.

**T3.7** — SERV-2449's two embedded images actually correspond to their captions: the first
showing `previous_month` with the column absent, the second showing `previous_ytd` with the
column present. This was **never visually confirmed**; the images are referenced by blob
URL. Verify or explicitly report as unverifiable.

---

## Confluence comment 1820655618 — proposed correction, needs review

Footer comment on page `1820262402`, authored by Kylor 2026-07-29, opening
"PO answers to the section 6 open items — 2026-07-29."

Direct link:
`https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/1820262402/Bet+A+Eng+Implementation+Plan+SERV-2447+2448+2449?focusedCommentId=1820655618`

Two statements in it are claimed to be wrong, both downstream of **T2.6**:

1. Item 6 says territory baselines will move upward after the ship-to fix and will be
   re-baselined. If wwjc is unaffected, nothing moves.
2. The closing paragraph says the casing find "explains the original false negative" and
   that the wwjc warehouse build should run *after* the ship-to fix. If wwjc and kal are
   unaffected, neither holds — and item 1 of that same comment already attributes the false
   negative to the admin artifact instead.

Verify T2.6 first. Only if it holds, confirm the proposed replacement wording is accurate
and does not overcorrect — the casing defect **is** real and does deserve its own ticket.
Note also that comment `38300` already tells Brent to ignore the sequencing note, so check
whether editing the Confluence comment is even necessary or whether it now just creates a
second version of the record.

---

## The two Brent-facing messages — review both

Both are drafted and **unsent**. Their exact text is in the prior session transcript at
`~/.cursor/projects/Users-kylorjohnson-Library-Mobile-Documents-com-apple-CloudDocs-SuperCat-4-0/agent-transcripts/1c962a83-bbd5-4271-abe1-7756e1e8eb22/1c962a83-bbd5-4271-abe1-7756e1e8eb22.jsonl`.
Search that file for `Nothing got deleted` and for `GREENLIGHT`. Read a small window around
each match; do not read the file linearly, it is large.

**Message A — the immediate reply.** Answers Brent's "did the other two tickets get
deleted?" and "I'm not seeing 1:1 what you are." Depends entirely on Tier 1. Check it for:

- any claim Tier 1 does not support;
- whether it correctly says all three tickets exist and why two vanished from the board;
- whether the sentence about admin rights not overriding the flag is precisely stated;
- tone — it should read as a peer explaining a finding, not as a briefing document.

**Message B — the full handoff message.** Longer, intended for after all fixes land.
Check every factual assertion against Tiers 1–3, and check that it does not claim SERV-2447
or SERV-2448 has a live user-visible reproduction. Both are honest verification routes only;
the only ticket with a real before/after is SERV-2449.

Flag anything in either message that is stated more confidently than the evidence supports.

---

## Sequencing question to answer

The last session told Kylor to hold Message B until SERV-2447 and SERV-2448 were "finished."
Both descriptions now appear fully rewritten and their sprints cleared, and the correction
comment is posted. Determine what, if anything, is actually still outstanding on those two,
and give Kylor a plain answer on whether he can send now or what specifically blocks him.

---

## Deliverable

Write your findings to
`PM/sales-portal-agent-starters/cycle-04-outputs/REVIEW-bet-a-pre-send-2026-08-04.md`
and summarize in chat. Include:

1. **SEND** or **DO NOT SEND**, stated in the first line.
2. A table of every claim above with **CONFIRMED / REFUTED / UNVERIFIABLE**, the evidence
   you used, and your derivation date for anything numeric.
3. A numbered list of required corrections, each naming the exact ticket, comment, page, or
   message and the exact replacement text. No advice of the form "consider revising."
4. Any **new** problem you found that is not on this list. Previous passes missed things;
   assume this one will too, and look specifically at what has not been checked rather than
   re-checking what has.
5. Whether the read-only Postgres and code evidence is sufficient to support the tickets
   going to engineering, or whether a production walkthrough on a corrected fixture is
   required first.

If you find that a claim is wrong in a way that changes the product decision rather than
just a number, stop and say so prominently rather than burying it in the table.
