# Bet A — ticket rewrites for Brent, 2026-07-30

**Paste-ready. Nothing has been written to Jira — Jira is read-only through my
integration, so every edit below is yours to make by hand.**

Brent's ask, from Slack this morning: *"a more human explanation like 'when I change the
filter it doesn't update' with a link to a page that I can reproduce. Then, when I change
the code, I can test that and see it working."* Then: *"do you want me to just edit the
current tickets with updated language, examples, etc" → **Yes**.*

So this is an amendment, not a rewrite. **Keep each ticket's existing header block** —
Program, Program key, AC, Eng SoT, Verify, Out of scope. Replace only from
`### Problem (current)` down to the end of the acceptance list, and leave `### Out of scope`
as it is. Where a ticket states a fact we now know is wrong, that's called out under
"Corrections" before the paste block.

Order below is deliberate: **SERV-2449 first, because it's the only one Brent can start on
today** — no non-admin login, no warehouse build, no fixture decision.

---

## The link format, confirmed

EBR-40's preserved original request already carries the exact query-string shape, so this
isn't guesswork:

```
…/invoices?utf8=%E2%9C%93&date_range=custom&from_date=2021-02-17&to_date=2021-02-17&multi-select-filters%5B%5D=%5B%22territory%22%2C%220016%22%5D
```

Decoded, that's `multi-select-filters[]=["territory","0016"]`. Same shape works on
`/invoices`, `/customers` and `/portal`.

**wwjc link bases** — two portal sites, one per brand, and the path segments are required
even on the vanity domains:

| Brand | Base |
|---|---|
| Wildwood (the `105:x` territories live here) | `https://supercat.supercatsolutions.com/wwjc/e/wwfc-2` |
| Chelsea House (`40 Daniel Ratchford`) | `https://supercat.supercatsolutions.com/wwjc/e/ch-2` |

**Date range values:** `all_available`, `current_ytd`, `previous_ytd`, `previous_year`,
`current_mtd`, `previous_month`, `yesterday`, `custom` (with `from_date` / `to_date`).

**One caveat on territory casing.** The filter value comes from the warehouse
(`territory_dimension.territory_code`), and the ETL downcases it, so the links below use
lowercase — `105:1 gigi lane`. The app database stores it uppercase. If a link returns
nothing, tick the box in the UI once and copy the URL rather than hand-editing the case.

---

# 1. SERV-2449 — Customers (EBR-91)

### Corrections to what's on the ticket now

- **Nothing is wrong with the diagnosis pointers.** `ecat_customers_controller.rb ~294 —
  substring gate on previous_ytd/custom` is exactly right. Keep it.
- **Reframe the second pointer.** `ecat_customer.rb ~113–122 — hardcoded CY/LY ranges
  ignore params[:date_range]` reads like a bug to fix. Per Q4 that behavior is **intended**
  and the fix is an honest relabel, not a range change. Worth making explicit or Brent will
  "fix" something you decided to keep.
- The ticket's A2.1–A2.4 numbering stays as-is. The repro sections below slot underneath it.

### Replace `### Problem (current)` and `### Acceptance` with this

```markdown
### Problem (current) — in plain terms

Pick "Previous Month" on the Customers page and the per-customer sales column for that
period disappears. Pick "Previous YTD" and it comes back. The number is being calculated
correctly either way — it's in the CSV export — the screen just refuses to render it for
six of the eight date ranges.

### How to reproduce — two links, same page, one param different

No special login needed. Works on a staff/admin account. No warehouse build required.

- Column MISSING: https://supercat.supercatsolutions.com/wwjc/e/wwfc-2/customers?date_range=previous_month
- Column PRESENT: https://supercat.supercatsolutions.com/wwjc/e/wwfc-2/customers?date_range=previous_ytd

Broken on: all_available, current_ytd, previous_year, current_mtd, previous_month,
yesterday. Works on: previous_ytd, custom. **The default range is one of the broken ones**,
so a rep who never touches the picker never sees a period figure at all.

### The same June window, two ways — this proves it's display, not math

While today is in July, "Previous Month" resolves to June 2026. So do these two links,
which cover an identical window and disagree about whether the column exists:

- Renders: …/customers?utf8=%E2%9C%93&date_range=custom&from_date=2026-06-01&to_date=2026-06-30
- Blank:   …/customers?date_range=previous_month

Add the territory filter to either and the figure to look for is $123,585.35 across 75
accounts:

…/customers?utf8=%E2%9C%93&date_range=custom&from_date=2026-06-01&to_date=2026-06-30&multi-select-filters%5B%5D=%5B%22territory%22%2C%22105%3A1%20gigi%20lane%22%5D

(After 2026-07-31, previous_month stops meaning June — use the custom form to pin it.)

### Why it happens

ecat_customers_controller.rb:293-295

    def show_custom_totals_by_bill_to?
      params['date_range']['previous_ytd'] || params['date_range']['custom']
    end

params['date_range'] is a String, so String#[] is doing a substring match, not a
comparison. It's truthy only when the selected range's name literally contains the text
"previous_ytd" or "custom". Nothing else does. The result is then discarded at lines 25
and 59: @custom_totals_by_bill_to = nil unless show_custom_totals_by_bill_to?

Line 23 has already computed the figure correctly for any range that resolves to dates.
That's why June's $123,585.35 reaches the export but never the screen.

Also: nothing in this controller defaults params[:date_range], so if the param is absent
entirely, line 294 evaluates nil['previous_ytd'] and raises. Unverified — no running app
on this side — but if real it's the same hardening as Q18.

### Second defect on the same ticket: the export is structurally malformed

Export any Customers CSV and count fields. On the 2026-06 artifact the header row has
**9** fields — Bill to Code, Customer, City, State, Last Year Sales, Current Year Sales,
Previous Month Sales, Backlog, Last Order — while all **1,154** data rows have **10**. The
unlabeled tenth column carries a customer class: DN on 996 rows, WS on 158.

Any consumer parsing by header position mis-maps every column after the gap or silently
drops one. This is the concrete form of the sarreid automation risk: a moving column *name*
is annoying, a header/data mismatch breaks the parse outright.

### Acceptance

* A2.1 — Any standard `date_range` shows a selected-range invoiced total via `Eol::DateRanges`
* A2.2 — Export CSV sales column for that same range; SUM = on-screen selected-range total (± rounding)
* A2.3 — Spine = `SUM(portal_invoices.net_amount)`
* A2.4 — Fix is period/scope alignment, not a second revenue definition
* A2.5 — Header field count equals data field count on every row; every column labeled

### Done when

1. The period column renders on all eight ranges, labeled with the range it covers.
2. On June 2026 + `105:1 gigi lane` it reads $123,585.35 across 75 accounts, with cents.
3. Export header field count equals data row field count, and the tenth column is labeled.
4. CY/LY blocks are relabeled as fixed calendar anchors — label only, ranges do not move (Q4).

### Reconciliation already verified — this is a regression guard, not a fix target

Column sums from the 2026-06 export, each tied to SQL on 2026-07-29 and re-confirmed
2026-07-30:

| Export column | Rows | Sum | Ties to |
|---|---|---|---|
| Last Year Sales | 315 | $1,300,171.90 | LY block, exact |
| Current Year Sales | 245 | $808,094.79 | CY block, exact |
| Previous Month Sales | 75 | $123,585.35 | nothing on screen — SQL agrees exactly |
| Backlog | 510 | $245,657.50 | Backlog block, exact |

The math is right. Don't rebuild it.
```

---

# 2. SERV-2447 — Invoices (EBR-40)

### Corrections to what's on the ticket now

- **The evidence figures are stale.** "~1,404 / $1.46M → ~710 / $777k" was 2026-07-21.
  Re-derived 2026-07-30: `cmallon`'s assigned book is **1,479 / $1,529,474.96** and
  `105:1 Gigi Lane` is **747 / $812,857.19**.
- **The diagnosis line number has drifted.** The ticket says `warehouse_access.rb ~424–434`.
  The code is now `territory_code_limit_common_table_expression`, **lines 999–1059**. Cite
  the method name so it survives the next refactor.
- **"empty keys + all-totals leak" needs splitting.** There are **three** branches in that
  method, not two. All-totals (lines 1002–1011) returns every territory in the org — that's
  the branch every admin takes, and it's what the withdrawn 2026-07-28 captures were
  actually showing. Associated-customer (1012–1037) derives territory from the linked
  customer's bridge rows. Normal rep (1040–1056) reads `rep_to_territory_bridge` by
  username, and that's the only branch where empty territories are the deciding factor.
  Verified: these are not the same bug, and the middle branch is why two of the fail-closed
  fixtures named in earlier drafts are invalid.
- **The Kalco original request is stale but should stay.** Ferguson bill-to `0010023` is
  assigned to `0999`, no 2021-02-17 Ferguson invoice remains, and that account's ship-tos
  aren't `0016`. Keep the links as provenance; add a note not to test against them.

### Replace `### Problem (current)`, `### Acceptance` and `### Evidence` with this

```markdown
### Problem (current) — in plain terms

A rep who covers six territories picks one of them on the Invoices page. The rows should
narrow to that territory and the invoiced total in the header should narrow with them.
Today they don't reliably move together — and a rep who selects nothing at all can be
shown a book wider than the territories they're assigned.

### Read this before you try to reproduce it — two things will fool you

**1. You cannot reproduce this on an admin login.** OrgUser#is_admin? is true if EITHER
org_users.is_admin OR users.is_admin is set, and UserTypePermissions.may? short-circuits to
true for an admin without ever reading the user type. An admin therefore takes the
all-customer-totals branch at warehouse_access.rb:1002-1011, which loads EVERY territory in
the org into territory_keys. That is exactly why the 2026-07-28 captures showed an unscoped
dropdown and org-wide totals — your is_admin hypothesis was right, and those captures have
been withdrawn.

**2. The portal does not read org_users.territory_codes.** For a normal rep, territories
come from rep_to_territory_bridge joined to rep_dimension.username
(warehouse_access.rb:1040-1047). The app-DB column is the ETL input, not the query source.
If the wwjc warehouse build hasn't run since territories were assigned, a correct
implementation still shows an empty book. Run the build before calling any result a bug.

### How to reproduce

Log in as a rep who holds several territories and is NOT admin on either column:
`cmallon` (Colin Mallon), user type `WW only Reps`, six territories, all-customer-totals
false. Then:

https://supercat.supercatsolutions.com/wwjc/e/wwfc-2/invoices?utf8=%E2%9C%93&date_range=current_ytd&multi-select-filters%5B%5D=%5B%22territory%22%2C%22105%3A1%20gigi%20lane%22%5D

**What should happen:** every row belongs to a customer in `105:1 Gigi Lane`, and the header
total reads that territory alone — $812,857.19 across 747 invoices.

**What would be the bug:** the header still shows her full six-territory book
($1,529,474.96), or the company book ($10,917,581.97), or the rows narrow while the header
doesn't. Rows and total have to move together.

Then remove the filter entirely and reload:

https://supercat.supercatsolutions.com/wwjc/e/wwfc-2/invoices?date_range=current_ytd

**What should happen:** the total is the union of her six assigned territories —
$1,529,474.96 over 1,479 invoices — and the Territories dropdown offers exactly those six.
A dropdown listing every territory in the org is itself a failure of this criterion: it
means the page doesn't believe the account is restricted.

### Fail-closed: a rep with no territories must see nothing, not everything

Two different values reach the same guard, so this is two tests. Fixtures below are
non-admin on both columns, have NO customer_number, and sit on a rep user type — all three
conditions matter, see the note underneath. Verified 2026-07-30.

- `territory_codes` is NULL — 3 accounts, all `WW & CH Reps`: `tomo`, `jkinch`, `highpoint`
- `territory_codes` is an empty array `[]` — 9 accounts: `jamiegatto`, `fperez`,
  `moxielighting` (`WW only Reps`) · `ehysler`, `gclark1`, `jrawlins`, `scooth3`
  (`WW & CH Reps`) · `atlantashowroom` (`ATL Sales Reps`) · `mark` (`CH only Reps`)

Log in as one, open /invoices at any range, repeat on /customers. Expected: empty list,
$0.00, and the message "No territories are assigned to your account — contact your
administrator." A blank page with no explanation is a partial fail — the copy is in scope.
It must never fall back to the company book.

**Why customer_number matters, and why two accounts are NOT valid fixtures here.** There
are three branches in territory_code_limit_common_table_expression, not two. If an org user
has an associated customer (warehouse_access.rb:1012-1037), territory access is derived from
THAT customer's bridge rows and the empty territory_codes column is never the deciding
factor. So an account with a customer_number cannot exercise the fail-closed path at all.

Two accounts named in earlier drafts fail this test and have been dropped: `rfreeman`
(territory_codes NULL but customer_number 10168) and `bulluckfurn` (empty array but
customer_number 2155). `mark` was missing from those drafts and has been added.

This also means the population is much larger than a dozen accounts. On wwjc, 2,702
non-admin accounts have NULL territories with no customer_number and 180 have an empty
array — but most sit on customer-facing user types. The 12 above are the ones on true rep
user types, which is what makes them the right fixtures. Separately, 17,895 non-admin
accounts have no territories AND a customer_number: those are customer logins taking the
associated-customer branch, and they are not in scope for this criterion.

Reading warehouse_access.rb:1040-1056, an empty bridge yields an empty customer set, which
looks like it already fails closed. The open question is downstream: whether anything
treats "empty customer list" as "no filter to apply." Not verified either way — the
withdrawn captures can't tell us, because they were on an admin.

### A territory with a genuinely empty book must show zero, not fall back

Log in as `bscarpa`, who holds `104 Madeline Cole` and `104:1 Bella Scarpa`. Select only
`104:1 Bella Scarpa` — it has no invoiced customers at all. Expected: empty list, $0.00.
Then select only `104 Madeline Cole`: $1,113,363.57 over 764 invoices.

This is the test that catches "an empty result set is treated as no restriction," which is
the failure mode that made the withdrawn captures look like a data leak.

### Before you write the two-territory test — this fixture is additive

`cmallon`'s six territories share no customers, so her per-territory totals sum to exactly
her union total: $812,857.19 + $531,730.44 + $127,853.05 + $57,034.28 = $1,529,474.96, to
the penny. Two of her six (`105:5 Grace Ingram`, `105:6 Krissa DeGennaro Newell`) have zero
invoices, as do both of `bminchew`'s JMH territories and `104:1 Bella Scarpa`.

So do NOT assert "the parts should exceed the whole" against this account — it would fail a
correct build. And pick a non-empty territory for the two-territory assertion, or the test
passes on an empty set.

Overlap is real on the org, but only one pair shows it, and no current rep holds both:
`105:1 Gigi Lane` is a complete subset of `40 Daniel Ratchford` (1,153 of 1,156 customers
in both; all 246 invoiced ones). Selecting both should return $2,503,022.96, not the
arithmetic sum of $3,315,880.15.

### Acceptance

* A1.1 — Rep with several territories selects one → only that territory's rows, and the header total equals that scope
* A1.3 — Nothing selected → union of assigned territories only, never the whole org, unless the user type carries all-customer totals
* A1.4 — `territory_codes` NULL, no all-totals → fail-closed empty book with the message, never the full org
* A1.5 — Same as A1.4 with `territory_codes` = `[]`
* A1.6 — A territory with a zero book returns $0.00 and does not fall back
* A1.8 — Territory selection survives a drill-through and back (parameter pass-through, no UI change — Q16)

### Baselines — re-derived 2026-07-30

`SUM(portal_invoices.net_amount)`, bill-to book, 2026-01-01 through today.

| Scope | Invoices | Accounts | Invoiced net |
|---|---|---|---|
| `105:1 Gigi Lane` | 747 | 246 | $812,857.19 |
| `105:2 Katherine McMullan` | 579 | 135 | $531,730.44 |
| `105:3 Weezie Ward` | 104 | 30 | $127,853.05 |
| `105:4 Susan Rutherford` | 49 | 21 | $57,034.28 |
| `105:5` / `105:6` | 0 | 0 | $0.00 |
| **`cmallon` union of six — her correct book** | **1,479** | **432** | **$1,529,474.96** |
| `95 BILL MINCHEW` | 1,069 | 350 | $1,324,694.54 |
| `104 Madeline Cole` | 764 | 228 | $1,113,363.57 |
| `40 Daniel Ratchford` | 2,302 | 682 | $2,503,022.96 |
| Org-wide — contrast only, never a rep's book | 10,535 | 2,643 | $10,917,581.97 |

**Tolerance: within 0.05% of a same-day baseline.** The screen sums
sales_fact.amount_invoiced while these sum portal_invoices.net_amount; per Q1 that gap is
intended. Observed on wwjc: 0.0013% on the current-year figure. Materially past 0.05% is a
scope difference, not rounding.

**On drift:** org-wide read $10,478,474.02 on 07-21, $10,871,602.36 on 07-28, and
$10,917,581.97 on both 07-29 and 07-30 — roughly +0.8%/week as invoices land inside
already-closed windows, but not continuously. Re-derive on capture day and compare rather
than assuming movement. Closed periods don't move: June 2026 has read $123,585.35 on four
separate derivation dates.

### Note on the original request below

The Kalco links are preserved as provenance but are no longer a live repro: Ferguson
bill-to 0010023 is assigned to 0999, no 2021-02-17 Ferguson invoice remains, and that
account's ship-tos aren't 0016. Use the wwjc links above.
```

---

# 3. SERV-2448 — Dashboard (EBR-212)

### Corrections to what's on the ticket now

- **`Verify: wwjc — Office/SuperCat or dash-enabled multi-terr rep` is not achievable.**
  All 22 wwjc user types have `view_dashboard: false` — including `Office - All - Dashboard`
  despite the name, and including `z'-Bet A Verify`. Confirmed 2026-07-29 and again
  2026-07-30. The Dashboard was reachable in the withdrawn captures only through the admin
  short-circuit. **There is no dash-enabled rep on wwjc to verify against.**
- This is a blocker on the ticket, not a detail. It needs a decision before the ticket can
  be verified, though not before it can be coded.

### Replace `### Problem (current)` and `### Acceptance` with this

```markdown
### Problem (current) — in plain terms

Select one territory on Invoices, note the invoiced total, then open the Dashboard without
changing anything. The Dashboard's invoiced KPI and its Top-N panels should be showing the
same territory's book. Today they can show the rep's full book or the org's.

### BLOCKER — there is no fixture for this on wwjc

All 22 wwjc user types have view_dashboard: false, including the one named
"Office - All - Dashboard" and including z'-Bet A Verify. Verified 2026-07-30. So no
rep-shaped account on this org can open the Dashboard at all, and the withdrawn 07-28
captures only reached it via the admin short-circuit in UserTypePermissions.may?.

Two ways out, and this needs a PO decision before verification (not before coding):

1. Stand up a NEW wwjc user type — a copy of `WW only Reps` plus view_dashboard — and put
   the new non-admin test user on it. Keeps everything on one org and one set of baselines.
   Do NOT add view_dashboard to `WW only Reps` itself: it carries 19 live users.
   `WW & CH Reps` carries 36.
2. Verify on an org that already has genuine non-admin dashboard reps. Candidates named in
   an earlier pass — bri / Primary_External_Sales_Reps, jcusa / Sales Reps, shl / Sales Reps
   SH/Mer/L1 — but these have NOT been re-verified and shl is a match-mode org
   (territory_access_via_rep_number is on), so it can't be the only capture.

### How to reproduce, once a fixture exists

On the chosen org, as a non-admin rep with multiple territories and all-customer-totals
false:

1. Open /invoices with one territory selected and Current YTD, and note the header total:
   …/invoices?utf8=%E2%9C%93&date_range=current_ytd&multi-select-filters%5B%5D=%5B%22territory%22%2C%22<code>%22%5D
2. Without changing the range or the selection, open /portal — that's the Dashboard route.

**What should happen:** the invoiced KPI equals the Invoices header total from the same
session, and no Top-N panel lists a customer from an unselected territory.

**What would be the bug:** the KPI showing the rep's full book, or the org book, while one
territory is selected.

Allow ±$1 on the comparison: Dashboard and Invoices round to whole dollars while Customers
prints cents. Otherwise the 0.05% tolerance from SERV-2447 applies.

The same two traps from SERV-2447 apply here — an admin login can't reproduce it, and the
warehouse build has to have run.

### Acceptance

* A1.2 — With one territory selected, the dashboard invoiced KPI and Top-N panels use that territory's scope, not the rep's full book and not org-wide
* Ships with EBR-40 / AC-A1 — do not score UI polish
```

---

# 4. The three EBR mirrors

EBR-40, EBR-212 and EBR-91 are the program-side tickets; each already points at its SERV
implementation ticket. Two options, your call:

**Lighter (recommended):** leave the EBR descriptions alone and add one line under
`### Problem (current)` on each:

```markdown
**2026-07-30:** repro steps, links and same-day baselines are on [SERV-XXXX] — that is the
executable copy. Figures in the Evidence block below are superseded.
```

That avoids maintaining the same text in two places, which is how the stale $1.46M figure
survived on both EBR-40 and SERV-2447 in the first place.

**Heavier:** paste the same repro blocks into the EBR descriptions too. Only worth it if
someone works from EBR rather than SERV.

**One correction that belongs on EBR-40 either way:** its Evidence block carries the same
stale 2026-07-21 figures (~1,404 / $1.46M → ~710 / $777k). Current: 1,479 / $1,529,474.96
→ 747 / $812,857.19.

---

## What's still yours to decide

1. **Non-additivity** — keep it as a criterion using the `105:1 Gigi Lane` + `40 Daniel
   Ratchford` pair (needs a constructed account holding both; expected $2,503,022.96 union
   vs $3,315,880.15 arithmetic sum), or drop it to a code-review item with no capture.
   Your ruling that it gets footnoted rather than "fixed" is unaffected either way.
2. **A1.2 fixture** — new wwjc user type, or another org. If you go with `bri`, those
   accounts need re-verifying first; they're currently an unchecked claim.
3. **The non-admin login ask.** Still the critical path, still eng's to resolve, and no
   territory criterion can be verified without it. Cheapest version: a new non-admin test
   user on wwjc, on the existing `WW only Reps` type, given `cmallon`'s six territories —
   touches no live user and edits no shared user type.
