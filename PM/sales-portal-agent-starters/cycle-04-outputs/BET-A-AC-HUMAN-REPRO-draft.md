# Bet A — acceptance criteria, rewritten as reproducible bugs

**DRAFT for Kylor. Nothing here has been posted to Confluence or Jira.**
Written 2026-07-30 in response to Brent's note: *"we just want to see a more human
explanation like 'when I change the filter it doesn't update' with a link to a page
that I can reproduce. Then, when I change the code, I can test that and see it working."*

Every item below is: one plain sentence of what's wrong · a link · what you see now ·
what you should see · where it is in the code. No shorthand, no `[T1,T2]`, no symbols.

---

## Read this first — two things gate the whole list

**1. Admin accounts can't reproduce any of the territory items.** `OrgUser#is_admin?`
is true if *either* `org_users.is_admin` or `users.is_admin` is set, and
`UserTypePermissions.may?` returns true for every permission on an admin without ever
reading the user type. So on an admin login the territory filter is loaded from the
"all customer sales totals" branch, which returns **every territory in the org** —
`warehouse_access.rb:1002-1011`. That is what the withdrawn 2026-07-28 captures were
actually showing. Items 3 through 7 need a **non-admin** login to reproduce.

**2. The portal reads territories from the warehouse, not from the app database.**
For a normal rep the territory list comes from `rep_to_territory_bridge` joined to
`rep_dimension.username` — `warehouse_access.rb:1040-1047`. `org_users.territory_codes`
is the ETL *input*, not what the page queries. If the wwjc warehouse build hasn't run
since territories were assigned, a correct implementation still shows an empty book.
**Run the wwjc build before treating any territory result as a bug.**

Items 1 and 2 need neither of those. Start there.

---

## The URLs

Production host is `supercat.supercatsolutions.com`. wwjc has two portal sites, one per
brand, and the path segments are required even on the vanity domain:

| Brand | Link base |
|---|---|
| Wildwood — use this one, `105:x` territories are Wildwood | `https://supercat.supercatsolutions.com/wwjc/e/wwfc-2` |
| Chelsea House — `40 Daniel Ratchford` lives here | `https://supercat.supercatsolutions.com/wwjc/e/ch-2` |
| Vanity equivalents | `catalog.wildwoodhome.com/wwjc/e/wwfc-2`, `catalog.chelseahouseinc.com/wwjc/e/ch-2` |

Pages: `/invoices` · `/customers` · `/portal` (that's the Dashboard).

### Baselines — all re-derived 2026-07-30

`SUM(portal_invoices.net_amount)` on the bill-to book, 2026-01-01 through today.

| Scope | Invoices | Accounts | Invoiced net |
|---|---|---|---|
| `105:1 Gigi Lane` | 747 | 246 | $812,857.19 |
| `105:2 Katherine McMullan` | 579 | 135 | $531,730.44 |
| `105:3 Weezie Ward` | 104 | 30 | $127,853.05 |
| `105:4 Susan Rutherford` | 49 | 21 | $57,034.28 |
| `105:5 Grace Ingram` | 0 | 0 | $0.00 |
| `105:6 Krissa DeGennaro Newell` | 0 | 0 | $0.00 |
| **`cmallon`'s six, union — her correct default book** | **1,479** | **432** | **$1,529,474.96** |
| `95 BILL MINCHEW` | 1,069 | 350 | $1,324,694.54 |
| `E4` + `E8 JMH - MINCHEW` | 0 | 0 | $0.00 |
| `104 Madeline Cole` | 764 | 228 | $1,113,363.57 |
| `104:1 Bella Scarpa` | 0 | 0 | $0.00 |
| `40 Daniel Ratchford` | 2,302 | 682 | $2,503,022.96 |
| `105:1 Gigi Lane`, June 2026 only | 110 | 75 | $123,585.35 |
| Org-wide — contrast only, never a rep's book | 10,535 | 2,643 | $10,917,581.97 |

**Every figure is identical to the 2026-07-29 derivation — nothing moved overnight.**
Drift is real across weeks (org-wide went $10,478,474.02 on 07-21 → $10,871,602.36 on
07-28 → $10,917,581.97 on 07-29 and 07-30, roughly +0.8%/week as invoices land inside an
already-closed window) but it isn't continuous, so a figure isn't automatically stale a day
later. Re-derive on capture day and compare rather than assuming movement. Closed periods
don't move at all: June 2026 has read $123,585.35 on four separate derivation dates.

Filters are real query params, so links are shareable: `?date_range=current_ytd` and
`&multi-select-filters[]=["territory","<code>"]`. The territory code's exact casing comes
from the warehouse, so rather than guessing it, tick the box in the UI once and copy the
resulting URL — that's your permalink.

---

## 1. On Customers, pick "Previous Month" and the month's sales column vanishes

**This is EBR-91 and you can reproduce it right now, on your own admin login, no fixture
needed.** It's the cleanest item on the list.

**Reproduce — two links, same page, one param different:**

- Broken: `…/wwjc/e/wwfc-2/customers?date_range=previous_month`
- Working: `…/wwjc/e/wwfc-2/customers?date_range=previous_ytd`

**What you see now:** on `previous_month` the per-customer sales column for that period is
blank/absent. On `previous_ytd` the same column renders. Six of the eight ranges in the
dropdown are broken this way — `all_available`, `current_ytd`, `previous_year`,
`current_mtd`, `previous_month`, `yesterday`. Only `previous_ytd` and `custom` work.

**What you should see:** the column renders on all eight ranges, labeled with the range
it covers.

**Where it is:** `ecat_customers_controller.rb:293-295`

```ruby
def show_custom_totals_by_bill_to?
  params['date_range']['previous_ytd'] || params['date_range']['custom']
end
```

`params['date_range']` is a String, so `String#[]` is doing a **substring match**, not a
comparison. It returns truthy only when the selected range's name happens to contain the
text "previous_ytd" or "custom". Nothing else does. The value is then thrown away at
lines 25 and 59 (`@custom_totals_by_bill_to = nil unless show_custom_totals_by_bill_to?`).

**The figure is computed correctly before it's discarded** — line 23 populates
`@custom_sales_total` for any range that resolves to dates. That's why it reaches the CSV
but not the screen: for June 2026 on `105:1 Gigi Lane` the export carries $123,585.35
across 75 accounts, and production SQL for that window returns exactly $123,585.35.
**So this is a display-gating defect, not a math defect. Don't rebuild the math.**

**Done when:** the period column renders on all eight ranges, and on Previous Month with
June 2026 it reads $123,585.35 over 75 accounts.

**Also worth a look while you're in there:** nothing defaults `params[:date_range]` in this
controller, so if the param is absent entirely, line 294 evaluates `nil['previous_ytd']`
and raises. I couldn't test that path without a running app — if it's real, it's the same
hardening as Q18.

---

## 2. The Customers CSV has nine column headers and ten columns of data

**Reproduce:** on `…/wwjc/e/wwfc-2/customers`, apply any filter and export. Count the
fields in the header row, then in any data row.

**What you see now:** header has **9** fields — Bill to Code, Customer, City, State,
Last Year Sales, Current Year Sales, Previous Month Sales, Backlog, Last Order. All
**1,154** data rows in the 2026-06 artifact have **10**. The unlabeled tenth column holds a
customer class: `DN` on 996 rows, `WS` on 158. Any consumer parsing by header position
mis-maps every column after the gap, or silently drops one.

**What you should see:** header field count equals data field count on every row, every
column labeled, and the period column using a fixed header (`Selected Range Sales`) with
the actual range printed in a scope block rather than baked into the column name.

**Done when:** the counts match and the tenth column is labeled with what it carries.

This is the concrete form of the `sarreid` automation risk — a moving column *name* is
annoying, but a header/data mismatch is what actually breaks a positional parser.

---

## 3. A rep picks one territory and the total doesn't narrow

Needs a non-admin login. This is the original A1.1.

**Reproduce:** log in as a rep who holds several territories — `cmallon`, user type
`WW only Reps`, six territories, not authorized for all-customer totals. Go to
`…/wwjc/e/wwfc-2/invoices?date_range=current_ytd`, open the Territories filter, tick only
**105:1 Gigi Lane**.

**What you should see:** every row belongs to a customer in `105:1 Gigi Lane`, and the
header total is that territory alone — **$812,857.19 across 747 invoices** (2026-07-30).

**What would be a bug:** the header still shows her full six-territory book
($1,529,474.96), or the company total ($10,917,581.97), or the rows narrow but the header
doesn't move. Rows and total have to move together.

**Done when:** the header matches the same-day figure for the selected territory within
0.05%, and the row count matches too.

*On the 0.05%: the screen sums `sales_fact.amount_invoiced` and these baselines sum
`portal_invoices.net_amount`. That difference is intended per Q1. Observed gap on wwjc is
0.0013% on the current-year figure. Anything materially past 0.05% is a scope difference,
not rounding.*

---

## 4. A rep who selects nothing should see their own book, not the company's

Original A1.3.

**Reproduce:** same login, `…/wwjc/e/wwfc-2/invoices?date_range=current_ytd`, touch no
filter at all. Then open the Territories dropdown without selecting anything.

**What you should see:** the total is the union of her six assigned territories —
**$1,529,474.96 over 1,479 invoices** — and the dropdown lists **exactly those six**.

**What would be a bug:** the company total, or a dropdown listing every territory in the
org. An unscoped dropdown is itself a failure, because it means the page doesn't believe
the account is restricted.

**One thing to know before you write the test:** `cmallon`'s six territories share no
customers, so her per-territory totals sum to exactly her union total —
$812,857.19 + $531,730.44 + $127,853.05 + $57,034.28 = $1,529,474.96, to the penny. Two of
her six (`105:5 Grace Ingram`, `105:6 Krissa DeGennaro Newell`) have no invoices at all.
**So don't assert "the parts should exceed the whole" against this account** — it would
fail a correct build. Pick a non-empty territory for any two-territory assertion, or the
test passes on an empty set. Overlapping territories do exist on the org and the totals
genuinely aren't additive there; see the last section for the one pair that shows it and
the numbers it should produce.

---

## 5. A rep with no territories assigned must see nothing, not everything

Original A1.4. Two shapes, worth a test each. Fixtures verified 2026-07-30 — non-admin on
both columns, **no** `customer_number`, and on a rep user type:

- NULL: `tomo`, `jkinch`, `highpoint` (all `WW & CH Reps`)
- Empty array `[]`: `jamiegatto`, `fperez`, `moxielighting` · `ehysler`, `gclark1`,
  `jrawlins`, `scooth3` · `atlantashowroom` · `mark`

`rfreeman` and `bulluckfurn` appear in earlier drafts and **are not valid fixtures** —
both carry a `customer_number` (10168 and 2155), which sends them down the
associated-customer branch at `warehouse_access.rb:1012-1037` where the empty territory
column never decides anything. `mark` was missing from those drafts.

**Reproduce:** log in as one of them, open `/invoices` at any range. Repeat on
`/customers`.

**What you should see:** empty list, $0.00, and a message saying so — *"No territories are
assigned to your account — contact your administrator."* A blank page with no explanation
is a partial fail; the copy is in scope.

**What would be a bug:** any populated list or non-zero total. It must never fall back to
the company book.

**What the code suggests, which you should confirm rather than trust:** for a normal rep,
`territory_keys` comes from `rep_to_territory_bridge` and `customer_keys` is derived from
it — `warehouse_access.rb:1040-1056`. An empty bridge yields an empty customer set, which
looks like it already fails closed. The risk is downstream: whether anything treats "empty
customer list" as "no filter to apply." **I have not verified which way it goes, and the
withdrawn captures don't tell us** — they were on an admin, which takes the
all-territories branch at line 1002 instead.

There are three branches in that method, and picking a fixture from the wrong one tests
nothing: all-totals/admin at 1002, associated-customer at 1012, normal rep at 1040. Only
the third makes empty territories the deciding factor.

---

## 6. A territory that genuinely has no sales should show zero, not fall back

Original A1.6, and it's the test that catches the failure mode that made last week's
captures look like a leak.

**Reproduce:** log in as `bscarpa`, who holds `104 Madeline Cole` and `104:1 Bella Scarpa`.
On `/invoices?date_range=current_ytd`, select only **104:1 Bella Scarpa** — that territory
has no invoiced customers. Then select only **104 Madeline Cole**.

**What you should see:** `104:1 Bella Scarpa` → empty list and $0.00. `104 Madeline Cole` →
$1,113,363.57 over 764 invoices.

**What would be a bug:** the empty territory returning her combined book or the company
book — i.e. an empty result being read as "no restriction."

---

## 7. The Dashboard should agree with the Invoices page

Original A1.2. **There is no fixture for this on wwjc.** All 22 wwjc user types have
`view_dashboard: false`, including the one named `Office - All - Dashboard`. Re-verified
2026-07-30: 22 types, 0 with the permission. The Dashboard was reachable in last week's
captures only through the admin short-circuit. So this needs either a new wwjc user type
or a different org — see the open question at the bottom.

**Reproduce (on whichever org is chosen):** open `/invoices?date_range=current_ytd`, select
one territory, note the header total. Without changing anything, open `/portal`.

**What you should see:** the invoiced KPI equals the Invoices total from the same session
(±$1 — the Dashboard rounds to whole dollars, Customers prints cents), and no Top-N panel
lists a customer from an unselected territory.

**What would be a bug:** the KPI showing the rep's full book, or the company book, while
one territory is selected.

---

## 8. Territory should survive a drill-through

Original A1.8. As `cmallon` with `105:1 Gigi Lane` selected, click into an invoice and come
back, then use any summary link that navigates to a filtered list. The selection should
still be applied and the total unchanged. Parameter pass-through only, no UI change.

---

## Two decisions I need from you, Kylor — not answered here

**Non-additivity, and how A1.3 gets worded.** Your instruction was that non-additivity is
correct behavior and gets a footnote, never a "fix." That still holds. What's changed is
that **no rep currently on wwjc can demonstrate it.** Every non-admin multi-territory rep
on the org has a perfectly additive book — customer counts, sum of parts vs union:
`cmallon` 1,971/1,971 · `dself2` 1,971/1,971 · `bminchew` 1,782/1,782 · `bscarpa`
1,075/1,075. Zero overlap in any of them.

Overlap is real at org level, and there is exactly one pair that shows it cleanly:

| | Invoices | Accounts | Invoiced net |
|---|---|---|---|
| `105:1 Gigi Lane` alone | 747 | 246 | $812,857.19 |
| `40 Daniel Ratchford` alone | 2,302 | 682 | $2,503,022.96 |
| Arithmetic sum of the two | 3,049 | 928 | **$3,315,880.15** |
| **Actual union of the two** | **2,302** | **682** | **$2,503,022.96** |

`105:1 Gigi Lane`'s invoiced customers are a **complete subset** of `40 Daniel Ratchford` —
1,153 of its 1,156 customers are in both, and all 246 invoiced ones are. So selecting both
territories should return $2,503,022.96, not $3,315,880.15, and the gap is exactly
`105:1`'s entire book. That's the sharpest possible demonstration: the sum of parts exceeds
the union by 32%.

The catch is that no one holds both. Only `dratchford` holds `40 Daniel Ratchford`, on
`CH only Reps`, and it's his only territory. So this needs a constructed test account
holding `105:1 Gigi Lane` + `40 Daniel Ratchford` — which the non-admin login work has to
create anyway, so it's close to free — or it stays a code-review item with no capture
behind it. Your call. If you want it, the expected numbers above are ready to paste into
the criterion.

**Which org for the Dashboard item.** Granting `view_dashboard` on wwjc means editing a
user type carrying live production users, or standing up a new one. The alternative is
another org — the previous session named `bri`/`alugo` as non-admin with dashboard access
and multiple territories, but **I have not re-verified those accounts myself** and would
before you commit to them.

---

## Still open from before this note

Your four revert decisions from yesterday are unanswered — the agent comment on Brent's
plan page (`1821179905`), and whether to roll back the AC page to v1 and the evidence page
to v6. Worth noting that this rewrite changes the calculus on the AC page: v1 is the
shorthand form Brent is telling you he can't read, and v3 is an agent-authored expansion
you didn't approve. Neither is what he's asking for. This document is.
