# Session result — Sales Portal territory attribution (el / Eurofase)

**Date:** 2026-09-22
**Input:** the 2026-09-22 handoff
**Net effect:** §8 shrank from three unknowns to one. No new findings. No new exposure numbers.
**Nothing below upgrades an evidence label.** New work is `SQL-PROXY` or `CODE-VERIFIED`; nothing is `PROD-OBSERVED` that the handoff did not already record as such.

---

## 1. Multi-currency — RESOLVED. M10 reproduces. `SQL-PROXY`

The prior session looked for a currency column, found only `price_levels.currency_code`,
and concluded M10 was unreproducible. **The derivation is not a currency column.**

`customers.default_price_code` → `price_levels.code` → `price_levels.currency_code`.

el runs 8 price levels, 4 CAD and 4 USD (`dncad/dnusd`, `ecomcad/ecomusd`,
`pdncad/pdnusd`, `straatoncad/straatonusd`).

el, `portal_invoices`, 2026-01-01 → 2026-09-18, 19,829 invoices, **0 unmapped**:

| Currency | Invoices | `sum(net_amount)` |
|---|---:|---:|
| USD | 14,804 | $12,440,158.76 |
| CAD | 5,025 | $7,852,599.41 |
| **Total** | **19,829** | **$20,292,758.17** |

M10's "$12.3M USD + $7.8M CAD summed 1:1" is **confirmed**.

Two notes for whoever re-derives this:

- `total_amount` is NULL on every el invoice. The money column at el is `net_amount`.
  `taxable_amount` and `nontaxable_amount` are present but sum to $0.00.
- `portal_invoices` *does* carry `customer_bill_to_country`; the handoff's "no currency
  column on portal_invoices or customers" note overlooked it. It is a sound second proxy
  but a slightly worse one — US $12,384,695.15 / CA $7,754,638.51, about 0.4% off the
  price-code split, because a handful of accounts bill in one country and price in the
  other currency. Country↔currency agreement at el is 1,942 of 1,946 customers
  (CA→CAD 345/346, US→USD 1,597/1,598). **Use the price code, not the country.**

**Consequence:** EBR-447 is not a Magnussen-only future problem. It is live at el today,
and it governs how §6's number may be stated.

---

## 2. The $749K is not a dollar figure `SQL-PROXY`

§6's sizing reproduces **exactly** — same cohort rule (el, active, `org_users.is_admin=false`
AND `users.is_admin=false`, 2–8 territories, internal `@supercatsolutions.com` account excluded),
same window, rep_number arm, increment floor = book − largest single territory, deduplicated
at invoice grain:

| | §6 | This session |
|---|---:|---:|
| reps affected | 52 | **52** |
| customers | 62 | **62** |
| pairs | 329 | **329** |
| increment floor | $749,073.00 / 675 inv | **$749,073.00 / 675 inv** |
| pool | $4,715,811.74 / 2,927 inv | $4,715,807.99 / 2,928 inv |

Then split the increment by currency:

| | Invoices | Amount | Share |
|---|---:|---:|---:|
| USD | 721 | $360,999.80 | 48.2% |
| CAD | 62 | $388,073.20 | 51.8% |
| **"$749,073.00"** | **675*** | **$749,073.00** | |

\* the currency rows count invoices in each currency's own scope; the dedup'd increment
set is 675 invoices.

**So the number may not be written as "$749K."** It is **$361K USD plus $388K CAD, added
together 1:1 by the Portal.** CAD is the larger half. Same for the pool: USD $1,979,604.85
+ CAD $2,736,203.14.

Minor: org base here is $20,292,758.17 against §6's $20,292,913.57 — **$155.40 apart,
0.0008%**. Recording it so it is not rediscovered later as a mystery. It is not one.

---

## 3. Customer-master arm — sized. It is **zero** at el. `SQL-PROXY`

Not "never sized." **Structurally nil**, and the reason is one line of data:

> Of el's 1,929 customers carrying a territory code on the customer master,
> **1,929 carry exactly one. Zero carry two or more.**

Under customer-master attribution an account therefore can never sit in two of one rep's
territories, so "whole book on the account" and "selected territory" are the same number
by construction. Increment **$0.00**, 0 reps, 0 accounts, 0 pairs.

Bounds on that claim: it is a property of el's customer master **as loaded today**, not of
the code. If el ever imports a customer with two territory codes the exposure appears. It
says nothing about any other org. Note also that el's rep-territory and customer-territory
code sets are different namespaces that only partly overlap (154 rep codes, 92 customer
codes, 61 in common) — worth remembering before anyone joins them elsewhere.

---

## 4. §8 after this session

| Item | Was | Now |
|---|---|---|
| Multi-currency / M10 | unknown, blocks every el figure | **resolved**; figures must be stated per-currency |
| Customer-master arm at el | never sized | **sized: $0** |
| SERV-2447 comment 38300 contradiction | open | **still open** — decision draft in §7 |

---

## 5. Code spot-check `CODE-VERIFIED`

Read `app/models/warehouse_access.rb` from `origin/master` myself via `gh api`
(note: `app/models/`, not `app/services/`). Every §2 line reference checks out:

- `:338 sum_amount_invoiced`, `:373 sum_backlog_total` — do pass the territory filter
- `:424 territory_code_limit_subquery`
- `:443 backlog_totals_by_bill_to` → `territory_codes: []` at **:454**
- `:500 invoice_totals_by_bill_to_for_date_range` → `territory_codes: []` at **:516**

---

## 6. Jira duplicate search

Searched SERV / ECAT / EBR / CSP.

- **Impersonation: no ticket exists.** Confirms §10.1.
- **Ticket #2 is already authorized, not a duplicate.** SERV-2486 comment 38300-series
  (comment 38422, Kylor, 18 Sep) ends: *"Not this ticket: the same figure on each customer
  row — the column AC8 left as 'consider'. That's a new surface, writing it up separately."*
- **One scope collision to settle before filing #2.** SERV-2486's own Scope section lists
  three surfaces, and surface 3 is **Customers — list header totals**
  (`get_customer_totals` / `get_customer_sales_totals`), with a "confirm this reading with
  Brent" note attached. The handoff records PR #2642 as shipping Invoices + Orders only.
  So the Customers *header* is in SERV-2486 and unbuilt; the new ticket is the *per-row*
  figure. They are not independent: the headers are the sum of the per-row numbers, so
  fixing the rows moves the headers. Say so in the ticket rather than letting Brent find it.
- **EBR-447** is "Support currency in sales data (Magnussen)", Triaging, description "TBD",
  one comment (chuck, 2025-08-26): *"Potentially blocking issue for Sales Portal for orgs
  that sell in multiple currencies."* §1–§2 above are the first sizing anyone has put on it.

---

## 7. Drafts for you to paste

All four below are drafts only. Nothing was written to Jira or Confluence, no org setting
was touched, and the artifact was not edited.

### 7A — NEW SERV: scoped rep impersonation

> **Summary:** Sales Portal: let a manager view the Portal as one of their reps (scoped impersonation)
>
> **Type:** FEA
>
> **User story**
>
> As a sales manager or agency principal who holds a subset of the org's reps, I want to
> open the Sales Portal as one of those reps and see exactly what they see — customer list,
> per-row and header sales figures, pricing, smart lists, library — so that I can answer
> "what is my rep actually looking at" without asking them to share a screen, and without
> an admin account, which skips territory logic entirely and shows me something different
> from what any rep sees.
>
> **Why now**
>
> Every territory-attribution escalation in this program has cost multiple sessions because
> the only accounts available to reproduce with were admin accounts. `OrgUser#is_admin?`
> (`org_user.rb:422-426`) is true if **either** `org_users.is_admin` **or** `users.is_admin`
> is set; `UserTypePermissions.may?` (`user_type_permissions.rb:117-125`) then grants every
> permission without reading the user type, and `FilterItemsByTerritoryCodeLimit:10-11`
> returns the relation unfiltered. An admin capture is not rep evidence, and three separate
> retractions in this program came from treating one as though it were. Support and PM
> currently have no way to see a rep's view at all.
>
> **Scope**
>
> - A user with the impersonation permission may act as an org_user drawn from an explicitly
>   assigned subset. Not "any user in the org."
> - The impersonated session must resolve permissions, territory access limits, price
>   levels, smart lists and library exactly as that org_user's own session does — not as a
>   filtered view of the manager's session.
> - Read-only. No order submission, no settings change, no acting on the rep's behalf.
> - The session is visibly banner-marked as impersonating, with one-click exit.
> - Every impersonation start/stop is audit-logged with actor, subject, and timestamp.
>
> **Out of scope**
>
> - Granting impersonation to admins by default.
> - iPad. Sales Portal / eCat Online only.
> - Any change to who a rep can see.
>
> **Acceptance criteria**
>
> 1. Given a manager with an assigned rep subset, when they open the rep picker, then only
>    that subset is listed.
> 2. Given a manager impersonating rep R on a page with a territory filter, when the page
>    renders, then every figure matches what R sees in R's own session, byte for byte.
> 3. Given the manager is impersonating, when any page renders, then a persistent banner
>    names the impersonated rep and offers exit.
> 4. Given the manager is impersonating, when they attempt any write action, then it is
>    refused.
> 5. Given impersonation starts or ends, when it does, then an audit record is written.
> 6. Given a user without the permission, when they hit the impersonation route directly,
>    then they are refused.
>
> **Notes**
>
> SERV-2486 does not deliver this and is not a partial version of it.
> FRD §9 parked this as its own ticket.

### 7B — NEW SERV: Customers per-row sales figures ignore the page's territory filter

> **Summary:** Sales Portal Customers: per-row LY / CY / Backlog figures ignore the selected territory filter
>
> **Type:** Bug (filter consistency)
>
> **What happens**
>
> On the Customers page, the territory filter correctly determines **which customers are
> listed**. It does not reach **the sales figures printed on each row**. Those figures are
> computed with an empty territory list, so each row shows the viewer's whole access-scoped
> book on that account rather than the territory they selected. The LY / CY / Backlog header
> blocks are sums of those row figures and inherit the same behavior.
>
> **Where** (`app/models/warehouse_access.rb`, `origin/master`, read 2026-09-22)
>
> - `invoice_totals_by_bill_to_for_date_range` (`:500`) passes `territory_codes: []` at `:516`
> - `backlog_totals_by_bill_to` (`:443`) passes `territory_codes: []` at `:454`
> - by contrast `sum_amount_invoiced` (`:338`) and `sum_backlog_total` (`:373`) **do** pass
>   `multi_filters[:territory]`, and `portal_get_customers.rb:143` passes it to the customer list
> - `territory_code_limit_subquery` (`~:424`) returns literal `true` for
>   all-customer-sales-totals users, discarding their selection on the legacy CTE paths
> - `app/views/.../customers/index.html.erb` has four header blocks (`:40, :55, :71, :88`);
>   LY / CY / Backlog do not carry the filter, the custom-range block does — so two numbers
>   on the same page answer different questions
>
> **Who sees it**
>
> The size of the gap is set by how wide the viewer's access limit is:
>
> - **Rep** — sees their own book across all their territories instead of the one they
>   picked. Bounded, and it never crosses into another rep's book.
> - **Admin / manager (no access limit)** — sees the **whole account**, including other
>   agencies' activity on it. This is the large one, and it is what the original Eurofase
>   escalation was actually reporting.
>
> Every rep-side test in this program came back clean because the rep-facing gap is the
> small one. Observed at el on 2026-09-22: the same customer list, ANIXTER 23426 Current-YTD
> reading $10,127 to an admin and $4,078 to a two-territory rep.
>
> **This is not a visibility or leakage defect.** No user sees a customer, invoice or order
> they could not already reach. The row set is correct; only the arithmetic on it is scoped
> differently from the page. Frame it as filter consistency.
>
> **Size at el** — 2026-01-01 → 2026-09-18, rep_number arm, active non-admin reps holding
> 2–8 territories, deduplicated at invoice grain: 52 reps, 62 customers, 329 rep/customer
> pairs. Minimum over-report (each rep's book minus their single largest territory)
> **$360,999.80 USD + $388,073.20 CAD**, against an org base of $12,440,158.76 USD +
> $7,852,599.41 CAD — about **3.7% of displayed dollars**.
>
> Stated per currency deliberately: el sells in both and the Portal adds them 1:1 (EBR-447).
> Do not collapse those two figures into one number.
>
> Method caveats: `portal_invoices` is a proxy for the warehouse the Portal actually reads,
> and this is the rep_number arm. The customer-master arm is **$0 at el**, because all 1,929
> el customers carrying a territory carry exactly one.
>
> **Acceptance criteria**
>
> 1. Given a territory filter is applied on Customers, when a row renders, then its LY, CY
>    and Backlog figures cover only the selected territories, for every viewer type.
> 2. Given no territory filter is applied, when the page renders, then behavior is unchanged.
> 3. Given a filter is applied, when the headers render, then each header equals the sum of
>    the rendered rows' corresponding figures.
> 4. Given a filter is applied, when the custom-range block and the LY/CY/Backlog blocks both
>    render, then all four answer the same scope question.
> 5. Given the change ships, when any viewer loads the page, then no customer, invoice or
>    order becomes reachable that was not reachable before.
> 6. Given the export is run under the same filter, when it is produced, then its figures
>    match the on-screen figures.
>
> **Relationship to SERV-2486**
>
> SERV-2486's scope already names Customers list header totals (`get_customer_totals` /
> `get_customer_sales_totals`) as its third surface, and that surface has not shipped —
> PR #2642 covered Invoices and Orders. This ticket is the **per-row** figure, which
> SERV-2486's PO note explicitly split out as a new surface. They meet at the header:
> because the headers are sums of the rows, fixing the rows moves the headers. Decide which
> ticket owns the Customers header before either is built.

### 7C — SERV-2447: the decision, not a dollar figure

The real blocker on 2447 is that comment 38300 asks for two incompatible things:

1. narrowing must resolve **"through the customer and ship-to bridges only"**
2. narrowing **"must use the same account→territory resolution the permission base uses"**

At el the permission base is `rep_number` (`territory_access_via_rep_number`: el, ctest,
shl only — `enabled_features.rb:81-84`). Both cannot hold. Brent cannot build until you pick.

**Recommendation: (2) — follow the permission base.** Three reasons:

- With the flag on, the access limit is `territory_key IN (own territories)`, built from the
  document's rep number (`filter_items_by_territory_code_limit.rb:43`). A bridges-only
  narrowing would not be a subset of that limit, so at el it can narrow to rows the limit
  has already removed — empty or nonsensical results on exactly the org that escalated.
- SERV-2486 has already shipped "Rep total" to el, and it is defined as the rep-number-credited
  figure. If the narrowed list answered the bridge question while the total beside it answered
  the rep-number question, the page would contradict itself.
- The el escalation is a rep-number attribution story end to end. Bridges-only does not address it.

Cost of choosing (2): orgs without the flag keep bridge resolution, so the rule is
"whatever the permission base uses" rather than one global semantic. That is already true
of the access limit, so it adds no new concept.

**Suggested comment text for 2447:**

> Resolving the contradiction in comment 38300. The narrowing filter must use the same
> account→territory resolution as the permission base for that org — rep number where
> `territory_access_via_rep_number` is on (el, ctest, shl), customer and ship-to bridges
> everywhere else. Strike "through the customer and ship-to bridges only." Rationale: with
> the flag on, the access limit is `territory_key IN (own territories)` built from the
> document's rep number, so a bridges-only narrowing is not a subset of the limit and can
> narrow to rows the limit already removed. It would also disagree with the "Rep total"
> figure SERV-2486 just shipped to el on the same pages. Territory semantics as decided
> remain unchanged; this only settles which resolution the narrowing reads.

### 7D — Confluence corrections log (1850867714 and 1851162625)

Do **not** delete either page. M15, M16, M1, M11, the substring-vs-array warning and the
Limits section are real work. Add these rows to the corrections log and rewrite the Short
Version.

| Item | Status | Correction |
|---|---|---|
| M10 — el sums $12.3M USD + $7.8M CAD 1:1 | **Confirmed 2026-09-22** | Reproduced. Derivation is `customers.default_price_code` → `price_levels.currency_code`, not a currency column. USD $12,440,158.76 / CAD $7,852,599.41 / total $20,292,758.17, 0 of 19,829 invoices unmapped. `SQL-PROXY` |
| $208,766.52 and $872,209.44 (Progressive, Ferguson) under a U3046 filter; 3.25x and 69x "as experienced by reps" | **Falsified** | Admin captures. `OrgUser#is_admin?` is true if either `org_users.is_admin` or `users.is_admin` is set; admins take no access limit and no territory filter. Not rep-facing. |
| M8 — whole-account aggregate for every user type | **Falsified** | Reps receive their own access-limited book. Only viewers with no access limit see the whole account. |
| M12 / the dnaulls repro | **Falsified** | dnaulls (org_user 56441, `["U3046"]`, non-admin in both columns) sees the correct figure. Client confirmed working correctly. |
| R1 / R2 — 708 rows, 151 belonging to six other agencies, $258,877.54 foreign | **Falsified** | Admin-only artifact. Promoting it to full weight was the error. |
| "646 active reps" | **Falsified** | el has 92 active non-admin org_users holding 2–8 territories; 52 are affected. |
| $76.6M / $134.3M / $5.47M as defect figures | **Falsified** | Populations of dollars that could be affected, not dollars displayed wrongly. |
| $472,414.81 "unexplained residual" | **Superseded** | The 2026-09-22 capture reconciles to 1.8% ETL lag. Stale, not mysterious. |
| Cross-rep leakage | **Closed** | No leakage path. The three-way OR in `FilterItemsByTerritoryCode:29-34` can only widen within a rep's own book, because the access limit is ANDed ahead of it. Do not reopen. |
| $749,073.00 as a single dollar figure | **Corrected** | It is $360,999.80 USD + $388,073.20 CAD summed 1:1. State per currency. |
| Customer-master attribution arm at el | **Sized** | $0. All 1,929 el customers carrying a territory carry exactly one, so an account cannot span two of a rep's territories. |

**Short Version, rewritten:**

> On the Sales Portal Customers page the territory filter selects which customers are
> listed but does not reach the sales figures printed on each row. Those figures are
> computed with an empty territory list, so each row shows the viewer's whole
> access-scoped book on that account, and the LY / CY / Backlog headers, being sums of
> those rows, inherit it.
>
> How large the gap is depends on the viewer's access limit. A rep sees their own book
> across all their territories rather than the one they selected — bounded, and never
> crossing into another rep's book. A viewer with no access limit — an admin or manager —
> sees the whole account, including other agencies' activity on it. The original Eurofase
> escalation is real, and it is that second case: an admin-facing over-report, about 3x on
> the accounts captured on 2026-09-22. It is not rep-facing, which is why every rep-side
> test came back clean.
>
> No user can see a customer, invoice or order they could not already reach. There is no
> cross-rep leakage. The row set is correct; only the arithmetic on it is scoped
> differently from the page.
>
> Sized at el for 2026-01-01 → 2026-09-18 on the rep_number arm: 52 reps, 62 customers,
> 329 pairs, minimum over-report $360,999.80 USD + $388,073.20 CAD — about 3.7% of
> displayed dollars. Stated in two currencies because el sells in both and the Portal adds
> them 1:1 (EBR-447). The customer-master arm is $0 at el.
>
> Two tickets follow: scoped rep impersonation, and Customers per-row figure scope. Every
> other finding on this page is already built, falsified above, or a characteristic of the
> client's data.

---

## 8. Still owed — the §5 test, which only you can run

It needs a real rep session and the credentials on disk are a single admin account, so a
capture from them would be exactly the failure this program keeps repeating.

As **betaverify**, at el, Customers page, Current YTD: tick **u3046 only** and reload.

- If the rows and the headers are unchanged from the no-filter view (LY $1,650,909.88),
  the defect is confirmed `PROD-OBSERVED` and 7B moves from SQL-sized to production-confirmed.
- Capture the filter chip, all three headers, and ANIXTER 23426 in one frame.
- Note the time; warehouse ETL lag is running 1–2%.

Nothing else in this program is waiting on anything else.
