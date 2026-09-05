# Pre-Jira verification — Sales Portal foundation

**Date:** 2026-08-04
**Owner:** Kylor Johnson
**Engineering reader:** Brent Sanders
**Mode:** Read-only. No Jira, Confluence, production data, user, setting, import, email, or code change was made.
**Supersedes as the verification record:** the runtime, fixture, and evidence sections of `EXECUTION-SALES-PORTAL-RESET-NEXT-ACTIONS-2026-08-04.md`
**Preserves:** `00-SALES-PORTAL-SYSTEM-SPEC.md` and `DECISION-BET-A-RESET-2026-08-04.md` as product authority

---

## 1. Executive decision

# READY FOR KYLOR MANUAL JIRA PASS

This status applies only to the **initial controlled Jira correction pass**. The
replacement pack in section 9 is complete and the final narrow pre-fix Customers
observation is recorded: with **Previous YTD** selected, the refreshed Customers
list retained the selected-period card and column.

The prior gate list was too broad. It incorrectly treated the later Invoice and
Dashboard regression matrices, fail-closed acceptance, authorized imports, and
Package 3 migration work as prerequisites to correcting stale Jira authority. They
remain required for the later **foundation exit to Bets B–F**, not for this manual
Jira sitting.

| Status | Initial Jira correction pass | Foundation exit to Bets B–F |
|---|---|---|
| Initial-pass evidence | Complete | Packages 1–3 ship; listed acceptance/disposition work completes |
| Already established | All six Package 1 authorization failures; Package 2 defect/CSV structure; Package 3 Option A decision | Nothing is declared complete merely because the Jira bodies are corrected |
| Not a blocker here | Invoice/Dashboard edge matrix, fail-closed checks, authorized imports, Package 3 migration/rebuild | These remain later acceptance, implementation, or disposition work |

**The initial Jira pass is ready.** Do not reopen a general evidence program
first.

Four findings from this pass change prior conclusions and define the three bounded package shapes:

**Finding A — SERV-2196 is mis-modelled, and the product decision is now settled.** In `shl`, every one of 3,703 shipping locations has a NULL `code`, and all 450,558 `shl` portal invoices have a NULL ship-to number. `Format.format_customer_key` uses `.compact`, so a NULL ship-to code makes `ship_to_key` identical to `customer_key`. Every ship-to territory in that organization therefore grants the **entire** customer account, and invoice `INV1446401` matches through the collapsed key rather than through any genuine ship-to-only path. Kylor selected Option A: bill-to territory grants the full account; ship-to-only territory grants the customer shell and exact-location transactions. The collapsed-blank-ship-to-key repair is accepted as mandatory prerequisite scope. `DOC-INTENT` + `SQL-BASELINE` + `CODE-IMPLICATION`.

**Finding B — the ship-to casing defect has zero current production exposure.** `ShippingLocation#territory_codes` reads `territory_codes_json`, and a `before_validation` callback downcases every write. Across all 488,069 ship-to rows in production, `territory_codes_json` contains **no uppercase character**. The bridge builder and the code enumerator therefore agree today. This closes open decision #8 in the system spec ("which affected organization should reproduce the ship-to casing defect") with the answer: none exists. Confluence page `1819836417` naming `cci`, `ta`, `ih`, `bmc2`, `gb` as verification orgs is `INVALID`. `SQL-BASELINE` + `CODE-IMPLICATION`.

**Finding C — the Customers display gate has two call sites, not one.** `@custom_totals_by_bill_to = nil unless show_custom_totals_by_bill_to?` appears at `ecat_customers_controller.rb:26` in `index` **and** at line 60 in `list`, the action that re-renders the `_list` partial on AJAX sort, page, and filter changes. A repair applied only to `index` would show the selected-period column on arrival and drop it on the user's first interaction — a partial fix that presents as a new intermittent defect and would likely come back as a reopened ticket. Both call sites and a list-refresh assertion are now written into the SERV-2449 body. `CODE-IMPLICATION`.

**Finding D — the supplied exports close the CSV-structure question.** All three exports contain 1,965 customer rows, nine headings, and ten fields on every row. The unlabeled tenth value is `DN`, `EP`, or `WS`, matching the price-level cue path. The two Current Month exports are byte-identical. The Previous YTD export changes the selected-period heading to `Previous YTD Sales` and changes 408 selected-period values while preserving customer order. `PROD-REPRO` + `CODE-IMPLICATION`.

Everything the 2026-08-04 reset asserted about package sequencing survives. Package 1 (authorization containment) is still first and is now confirmed line-by-line against `4ff408492`. Package 2 (narrow SERV-2449) is unchanged in scope and its mechanism is fully isolated to one predicate applied at two call sites. Package 3 is now a selected build rather than an open product decision: Option A plus the collapsed-key repair and affected-client migration.

---

## 2. Runtime ledger

```text
deployed_production_sha:        not disclosed — no longer material, see 2.1
deployed_at:                    not disclosed
reviewed_source_sha:            4ff408492650a2f14e6572f833365c3eaba97c10 (all code claims read from this tree)
origin_master_sha:              4ff408492650a2f14e6572f833365c3eaba97c10
origin_master_commit_date:      2026-08-04 12:52:09 -0400 (Brent Sanders)
origin_master_commit_subject:   "Hotfix: block iPad resubmission of old orders as duplicates (#2596)"
origin_master_fetch_time:       2026-08-04T21:17:59Z
local_head_sha:                 d4a0e7d408fba6917ac5e685cd21e54c5ecd801d (2025-12-09), 680 behind
portal_warehouse_completed_at:  2026-08-04 20:01:25 UTC  (AppSetting warehouse_timestamp = portal_20260804200125)
internal_warehouse_timestamp:   internal_20260804200125
verification_started_at:        2026-08-04T21:17:00Z
verification_completed_at:      2026-08-04T21:40:00Z
database_inspected:             supercatprod (application database), TimeZone GMT
```

### 2.1 Deployed SHA — CLOSED without disclosure

The deployed revision was never disclosed, and it is no longer needed. The question it was standing in for — *do the code claims in this document describe what is actually running?* — was answered directly.

`PROCESS`: Asked 2026-08-04. Brent's reply: "you should be able to find that by going to SuperCat_server on GitHub and checking out the latest hash on master." That answers a different question — master's tip is not necessarily the deployed revision, and the two diverge whenever a merge has not shipped. Rather than press, the gap was measured.

`CODE-IMPLICATION`, verified by diff at 21:54Z against the fetched clone: exactly **2** commits separate the previously inspected `0856f2d1a` from `4ff408492`.

```
4ff408492  2026-08-04 12:52 -0400  Brent Sanders  Hotfix: block iPad resubmission of old orders as duplicates (#2596)
367f73e29  2026-08-04 12:43 -0400  Brent Sanders  Accept windows-1252 SendGrid inbound text/html params. (#2595)
```

Together they touch seven files: `app/controllers/inbound_emails_controller.rb`, `app/services/orders/create.rb`, `app/services/orders/get_submitted_order_uuids.rb`, `docs/INCIDENT_2026-08-04_order_draft_resubmission.md`, and three test files. **No Sales Portal path is touched.** Whether production sits on `4ff408492`, `367f73e29`, or `0856f2d1a`, every reviewed file is byte-identical.

`PROCESS`: Every line reference in this document was independently re-verified against `4ff408492` by content, not by working-tree position. The local working tree is `d4a0e7d40` (2025-12-09) and its files on disk are eight months stale; the source claims were read from the fetched `4ff408492` objects. Confirmed line numbers: `show_custom_totals_by_bill_to?` at 294, `org_user_may_view_customer?` at 304, `@custom_sales_total` at 24, the nil-out at **26 and 60**, `should_display_portal_dashboard?` at helper 54, `index.html.erb` at 68, `_list.html.erb` at 13/37/39/44, and the ten dashboard data actions at 27–71 with the gate appearing only at line 12 inside `index`.

`CODE-IMPLICATION`: one substantive change did land in the reviewed controllers between December and now — `before_action :require_sales_portal_access` was added at the top of `EcatInvoicesController`, `EcatCustomersController`, and `EcatDashboardController`. That is exactly the state this document describes: the routes are reachable by anyone with Sales Portal access and nothing narrower is enforced. The remaining differences in those three files are quote-style churn (`:"multi-select-filters"` → `:'multi-select-filters'`).

`PROCESS`: `origin/master` has **not moved** since the 2026-08-04 reset recorded it. Re-verified by fetch at 21:17:59Z.

`PROCESS`: If the exact deployed revision is wanted for the record, `config/appsignal.yml` reports `ENV['APP_VERSION']` as the production revision, so AppSignal's deploy markers for "SuperCat Backend" carry it. The Capistrano-style layout at `/home/supercat/supercat/current` (`config/unicorn.rb`) is the SSH alternative. Neither is a prerequisite for anything in this document.

### 2.2 Warehouse freshness — PASS

`SQL-BASELINE`: The portal warehouse completed at **20:01:25 UTC**. `betaverify`'s territory assignment was last written at **17:24:21 UTC**. The warehouse is 2h37m newer than the fixture, so territory results are interpretable. The stop condition "warehouse is older than territory assignments" does **not** fire.

The timestamp must be UTC: any timezone west of UTC would place `20:01:25` in the future relative to the 21:20 UTC observation time.

`SQL-BASELINE`: `betaverify`'s last eCat Online login is **2026-08-04 20:25:09 UTC** — 14:25:09 MDT. That independently corroborates the recorded P0 probe at "approximately 14:24 MDT" and confirms it ran after the 20:01:25 warehouse build. The three `PROD-REPRO` captures are therefore bound to the current warehouse state.

### 2.3 Warehouse database is out of reach

`PROCESS`: The available Postgres connection reaches `supercatprod` only. The warehouse database (dimensions, bridges, sales facts) is a separate database and is **not** queryable from here. Every SQL baseline in this document is derived from application tables (`customers`, `shipping_locations`, `portal_invoices`, `org_users`, `user_types`, `organizations`) — which is how the original baselines were derived, and which reproduces them exactly (section 5.1).

---

## 3. Fixture ledger

### 3.1 `wwjc/betaverify` — VALID, all six required facts confirmed

`SQL-BASELINE`, re-derived 2026-08-04 21:20 UTC:

| Required fact | Observed | Result |
|---|---|---|
| `org_users.is_admin = false` | `false` | PASS |
| `users.is_admin = false` | `false` | PASS |
| Blank `customer_number` | `''` (length 0) | PASS |
| User type `z'-Bet A Verify`, id `2864` | id `2864`, name `z'-Bet A Verify` | PASS |
| Sales Portal Dashboard enabled | `enable_portal_dashboard = true` | PASS |
| Portal totals enabled | `display_sales_portal_totals = true` | PASS |
| All-customer totals disabled | `access_all_customer_sales_totals = false` | PASS |
| Six **separate** territory values | 6 discrete JSON array elements, not concatenated | PASS |

```
["105:1 Gigi Lane","105:2 Katherine McMullan","105:3 Weezie Ward",
 "105:4 Susan Rutherford","105:5 Grace Ingram","105:6 Krissa DeGennaro Newell"]
```

Supporting identifiers: `org_users.id = 158770`, `users.id = 80858`, org `wwjc` = organization id 8, not disabled on either record.

No stop condition fires. The fixture is valid for restricted-rep acceptance.

### 3.2 Dashboard-gate-off reproduction — established with controlled `betaverify`

The handoff required this be verified against the real Sales Portal Dashboard gate, not Admin Console `view_dashboard`, and warned against assuming the username from old notes. Both checks were performed.

`CODE-IMPLICATION` — the actual gate, `origin/master` `app/helpers/ecat_permissions_helper.rb:54-59`:

```ruby
def should_display_portal_dashboard?
  @show_customers &&
    (Feature.enabled?(:portal_portal, @current_org, @current_org_user) || @current_org.enable_portal_dashboard) &&
    @current_org_user.user_type.enable_portal_dashboard &&
    @current_org_user.user_type.display_sales_portal_totals
end
```

`SQL-BASELINE` had identified `cmallon`, user type 87 `WW only Reps`, as a clean
Dashboard-gate-off shape:

| Gate component | Value | Effect |
|---|---|---|
| `organizations.properties->flags->enable_portal_dashboard` (wwjc) | **`true`** | gate component satisfied |
| `user_type.enable_portal_dashboard` | **`false`** | **gate fails here** |
| `user_type.display_sales_portal_totals` | `true` | gate component satisfied |
| `user_type.enable_sales_portal` | `true` | passes `require_sales_portal_access`, so the routes are reachable |
| `org_users.is_admin` / `users.is_admin` | `false` / `false` | legitimate non-admin |
| `customer_number` | `''` | not a customer user |
| `access_all_customer_sales_totals` | `false` | territory-limited |
| Territories | the same six `105:1`–`105:6` as `betaverify` | **in-book** |

`PROD-REPRO` supersedes the credential-dependent plan: Kylor temporarily changed
only `wwjc/betaverify` from `z'-Bet A Verify` to `WW only Reps`, started a fresh
authenticated browser session, and called the three routes in section 4.1. Each
returned protected Dashboard content; Kylor then restored `z'-Bet A Verify`.
The six territories remained available. This is the required single-variable
test: the organization gate stayed on, the territory book stayed constant, and
only the user-type Dashboard flag was changed.

`cmallon` remains a valid SQL comparison fixture, but Kylor does not need its
credentials and must not repeat the temporary user-group switch. Admin Console
`view_dashboard` is coincidental and was not used to qualify the reproduction.

`SQL-BASELINE`: Of the 22 user types in `wwjc`, only three have `enable_portal_dashboard = true`: `z'-Bet A Verify` (2864), `z-SuperCat` (92), and `Office - All - Dashboard` (1274). The latter two also carry `access_all_customer_sales_totals = true`, so **`betaverify` is the only restricted-rep Dashboard fixture in the organization.** Every other non-admin `wwjc` user is Dashboard-gate-off.

### 3.3 Out-of-book authorization control — VALID, with one correction

`SQL-BASELINE`, re-derived 2026-08-04:

| Field | Recorded | Observed | Result |
|---|---|---|---|
| Portal invoice id | `4667912895` | `4667912895` | PASS |
| Invoice number | `INV65157` | `INV65157` | PASS |
| Customer bill-to | `14378` | `14378` | PASS |
| Customer name | MEG BRAFF DESIGNS | MEG BRAFF DESIGNS | PASS |
| Invoice date | 2026-08-04 | 2026-08-04 | PASS |
| Net amount | `$100.00` | `100.0` | PASS |
| Ship-to number | — | `000` | recorded |
| Outside `betaverify`'s six-territory book | yes | **yes** | PASS |

**Correction:** the control was recorded as carrying customer territories `D6 LORNE GARDNER` and `30440 Interim Rep House Account`. Those two strings are the invoice's **`rep_number`** value (`"D6 LORNE GARDNER,30440 Interim Rep House Account"`), not the customer's territory assignment. The customer's actual bridge territories are `112 barris group` and `d6 lorne gardner`. Either way the record sits outside `105:1`–`105:6`, so the control holds; the description in the ticket bodies has been corrected accordingly.

Two incidental observations, recorded and deliberately **not** escalated:

- The control invoice carries a comma-separated `rep_number`, the exact shape EBR-180/SERV-2178 describes. `SQL-BASELINE`: `wwjc` has `territory_access_via_rep_number` unset, so this path is inert for this organization and does not affect the control.
- The application table `billing_and_shipping_codes_to_territory_codes_bridge` yields a different (smaller) `wwjc` book than the customer master. `CODE-IMPLICATION`: its population is commented out in `org_importer.rb:796-797` and nothing reads it. It is a dead legacy artifact, not the Sales Portal path, and is **not** a new package.

### 3.4 Fail-closed and edge fixtures — verified, with two rejections

Confluence `1819836417` names fail-closed fixtures. They were re-verified; two must not be used.

| Fixture | Territory shape | Customer number | Verdict |
|---|---|---|---|
| `tomo`, `jkinch`, `highpoint` | NULL | blank | **VALID** for NULL fail-closed |
| `rfreeman` | NULL | **`10168`** | **INVALID** — customer user, takes a different code branch |
| `jamiegatto`, `fperez`, `moxielighting`, `ehysler`, `gclark1`, `jrawlins`, `scooth3`, `atlantashowroom` | `[]` | blank | **VALID** for empty-array fail-closed |
| `bulluckfurn` | `[]` | **`2155`** | **INVALID** — customer user |
| `bscarpa` | `104 Madeline Cole`, `104:1 Bella Scarpa` | blank | VALID — zero-book territory case |
| `bminchew` | 3 territories, 2 with zero book | blank | VALID |
| `dself2` | same six as `cmallon` | blank | VALID — control |

`SQL-BASELINE`: `gclark1`, `jrawlins`, `scooth3`, `rfreeman` have `disabled = NULL` rather than `false`. Confirm each can still sign in before relying on it.

All of the above are `enable_portal_dashboard = false`, so a NULL- or empty-territory user hitting a `/portal/*` data action is a **compound** test: no territories *and* no Dashboard gate. Use `tomo` for that combined case.

### 3.5 `wwjc` cannot test ship-to behavior — confirmed

`SQL-BASELINE`: `wwjc` has 14,018 shipping locations and **0** carry any territory assignment; all 14,018 customers do. The reset's statement stands. Ship-to cases must run elsewhere — see section 6.3.

---

## 4. Six-route authorization matrix

### 4.1 Current status

| # | Route | Fixture | Status | Evidence |
|---|---|---|---|---|
| 1 | `GET /wwjc/e/wwfc-2/invoices/INV65157` | `betaverify` | **FAILED** 2026-08-04 ~14:24 MDT — HTTP 200, returned `INV65157`, MEG BRAFF DESIGNS, `$100.00` | `PROD-REPRO` (settled) |
| 2 | `GET /wwjc/e/wwfc-2/email_invoice/4667912895` | `betaverify` | **FAILED** — HTTP 200, returned `INV65157`. No POST, no send. | `PROD-REPRO` (settled) |
| 3 | `GET /wwjc/e/wwfc-2/customers/14378` | `betaverify` | **FAILED** — HTTP 200, returned `14378` / MEG BRAFF DESIGNS | `PROD-REPRO` (settled) |
| 4 | `GET /wwjc/e/wwfc-2/portal/invoice_total?date_range=current_ytd` | `betaverify` temporarily in `WW only Reps` | **FAILED** — returned a dollar metric | `PROD-REPRO` (controlled, restored) |
| 5 | `GET /wwjc/e/wwfc-2/portal/top_customers?date_range=current_ytd` | `betaverify` temporarily in `WW only Reps` | **FAILED** — returned customer names and amounts | `PROD-REPRO` (controlled, restored) |
| 6 | `GET /wwjc/e/wwfc-2/portal/top_products?date_range=current_ytd` | `betaverify` temporarily in `WW only Reps` | **FAILED** — returned product details and amounts | `PROD-REPRO` (controlled, restored) |

Routes 1–3 are settled and are not required again to justify Package 1. They must be rerun only as post-fix acceptance. The earlier caveat — "unless the deployed SHA predates the reviewed source" — no longer applies: per 2.1, every commit between the candidate revisions leaves the reviewed files byte-identical.

Routes 4–6 are settled production failures. Package 1 acceptance must still cover
all ten Dashboard data actions, but that is post-implementation acceptance—not a
reason to delay the initial Jira correction pass.

### 4.2 Source position on all six, read from `origin/master` `4ff408492`

`CODE-IMPLICATION` — `app/controllers/ecat_invoices_controller.rb`:

```ruby
def show
  @invoice = @current_org.portal_invoices.where(:invoice_number => params[:invoice_number]).first
  raise ActiveRecord::RecordNotFound unless @invoice
  ...
end

def email_invoice
  @invoice = PortalInvoice.find(params[:invoice_id])
  if request.post?
    ...
    MobileMailer.portal_invoice(...).deliver_later
```

- `show` scopes to the organization and the invoice number. It never consults the signed-in user's territory book. This is exactly route 1's observed behavior.
- `email_invoice` uses a **global** `PortalInvoice.find(id)` — not even organization-scoped. Route 2's exposure follows directly, and cross-organization invoice ids will also resolve.
- The POST branch enqueues mail with **no authorization check at any layer**. An unauthorized POST can send another organization's invoice. This is `CODE-IMPLICATION` only — it must **not** be tested by POSTing.

`CODE-IMPLICATION` — `app/controllers/ecat_customers_controller.rb:304-308`:

```ruby
def org_user_may_view_customer?(org_user, bill_to)
  return true if org_user.is_admin?
  return true if org_user.customer_number.blank? # this should restrict to user's territory
  return org_user.customer_number.downcase == bill_to.try(:downcase)
end
```

The comment in shipped source states the defect. `betaverify` has a blank customer number, so it is allowed any bill-to in the organization. This is route 3.

`CODE-IMPLICATION` — `app/controllers/ecat_dashboard_controller.rb`: only `index` calls `should_display_portal_dashboard?`, and only to redirect. **Ten** data actions run behind `require_sales_portal_access` alone:

`backlog_total`, `invoice_total`, `all_graph`, `graph`, `budget_graph`, `top_customers`, `top_products`, `top_tradenames`, `top_collections`, `top_territories`

Routes 4–6 test three of those ten. Package 1 acceptance must cover all ten; the ticket body in section 9.7 names them explicitly.

### 4.3 Recording template — one block per route

```text
route:
organization:                        wwjc
username:
role_shape:                          non-admin territory-limited rep
admin_fields:                        org_users.is_admin=false; users.is_admin=false
customer_number:                     (blank)
user_type:
territories:
warehouse_timestamp:                 portal_20260804200125 (2026-08-04 20:01:25 UTC) — re-read before capture
deployed_sha:                        (from Brent)
requested_at:
http_status:
protected_identifiers_or_metrics_returned:
email_delivery_count_before:
email_delivery_count_after:
evidence_label:
```

Pass = deny, redirect, or not-found with no protected content. Fail = an out-of-book record or a gated Dashboard metric is returned. Routes 4–6 fail if any dollar figure, customer name, or product name renders.

**Do not POST the email form. Do not send email.** The GET/POST route share one path (`config/routes.rb:215`), and the POST branch is unguarded.

---

## 5. Invoice and Dashboard closure matrix

### 5.1 The June baseline reproduces exactly

`SQL-BASELINE`, re-derived 2026-08-04 21:22 UTC — `wwjc`, territory `105:1 Gigi Lane`, 2026-06-01 to 2026-06-30, resolved against customer-master `territory_codes_json`:

| Metric | Recorded | Re-derived | Result |
|---|---|---|---|
| Invoices | 110 | **110** | exact |
| Accounts | 75 | **75** | exact |
| Invoiced net | `$123,585.35` | **`$123,585.35`** | exact |

The territory book contains 1,152 customers. The period is closed and has not drifted.

`PROCESS`: This total is `SUM(portal_invoices.net_amount)` — the **imported header** amount. The Invoices page total is line-derived `amount_invoiced`. The two agree here within display rounding (`$123,585` shown). That agreement is a property of this period, not a product decision. Do not cite the June baseline as evidence for either side of the amount-contract question.

### 5.2 New baselines for the cases that had none

| Case | `SQL-BASELINE` (2026-08-04) |
|---|---|
| One assigned territory — `105:1`, June 2026 | 110 invoices / 75 accounts / `$123,585.35` |
| **Union of all six assigned territories, June 2026** | **224 invoices / 127 accounts / `$221,114.05`** (book = 1,965 customers) |
| Organization-wide contrast, June 2026 — never a rep's book | 1,693 invoices / 824 accounts / `$1,832,799.91` |

The union figure is new. It gives the "multiple assigned territories" case a hard expected value instead of "more than one territory's worth."

### 5.3 EBR-40 / SERV-2447 — what Kylor must run before closing

Fixture `betaverify`. Record the warehouse timestamp immediately before each capture.

- [ ] Gigi Lane, June 2026: the page reports **110** invoice rows. *(The old capture never proved this. It is the one genuinely open item on the primary route.)*
- [ ] Same selection: total within display rounding of **`$123,585.35`**.
- [ ] Every sampled row belongs to a `105:1` customer.
- [ ] No territory selected, June 2026: **224** invoices / **`$221,114.05`** — the union, not the company book.
- [ ] Single-territory selection narrows correctly from that union.
- [ ] NULL assignment fails closed — as `tomo`. Empty list, zero total, never the org book.
- [ ] Empty-array assignment fails closed — as `jamiegatto`.
- [ ] All-totals user makes an explicit selection and is narrowed to it — use a `z-SuperCat` or `Office - All - Dashboard` member.
- [ ] Zero-book territory returns zero and does not fall back — as `bscarpa`, selecting `104:1 Bella Scarpa`.
- [ ] Real ship-to-assigned organization follows documented bill-to/ship-to behavior — **not `wwjc`**; see 6.3 for the candidate list.
- [ ] Mixed-case territory codes — **now closed by evidence, no run required.** See section 8, Finding B.
- [ ] Collapsed blank ship-to key does not create a false bridge match — **now reproduced by data, see section 7.** Treat as evidenced, not as a UI run.

If every runnable case passes, close EBR-40 and SERV-2447 with the note in section 9.1/9.2. If one fails, do not keep SERV-2447 open as a generic project — name the fixture, route, expected result, observed result, and root path, then file a focused issue.

### 5.4 EBR-212 / SERV-2448 — what Kylor must run before closing

- [ ] Dashboard invoiced KPI vs Invoices, same role, period, and territory. Use **June 2026 / `105:1`** and expect `$123,585.35` on both, not Current YTD.
- [ ] Every Top Customer belongs to the selected permitted book.
- [ ] Top Product reconciles to territory-scoped **orders / order lines**, not invoice amount.
- [ ] Drill-through persistence through graph, Orders, Backlog, and Top-N destinations.
- [ ] The already-passing Invoice KPI link still passes `report_params`.
- [ ] Do **not** require ordered panels to equal the invoiced KPI.

`STALE`: The 2026-08-04 `$836,263` Current-YTD agreement is a timestamped observation. It is not a closure baseline and will have drifted. The reset recorded `wwjc` org-wide drift of roughly +0.8% per week.

---

## 6. Customers reproduction and CSV field-count matrix

### 6.1 The display gate — mechanism fully isolated on current `origin/master`

`CODE-IMPLICATION` — `app/controllers/ecat_customers_controller.rb:294-296`:

```ruby
def show_custom_totals_by_bill_to?
  params['date_range']['previous_ytd'] || params['date_range']['custom']
end
```

This is Ruby `String#[]` — substring search, not equality or membership. Applying it to the eight ranges in `Eol::DateRanges::DATE_RANGES`:

| `date_range` | Gate result | Standing column exists? | Verdict |
|---|---|---|---|
| `all_available` | hidden | no | **defect** |
| `current_ytd` | hidden | yes — CY Sales | correct, by accident |
| `previous_ytd` | shown | no | correct |
| `previous_year` | hidden | yes — LY Sales | correct, by accident |
| `current_mtd` | hidden | no | **defect** |
| `previous_month` | hidden | no | **defect — reproduced** |
| `yesterday` | hidden | no | **defect** |
| `custom` | shown | no | correct |

Four ranges are affected, not one. Only `previous_month` carries a `PROD-REPRO`; the other three are `CODE-IMPLICATION`.

The two ranges that behave correctly do so *coincidentally* — they happen to be the two with standing columns. **A naive "always show" fix would introduce exactly the duplicate-standing-column outcome the reset excludes.** The correct fix is an explicit allow-list of non-standing ranges.

One gate controls all three display surfaces, and it is applied at **two** controller call sites:

- `ecat_customers_controller.rb:26` — in `index`: `@custom_totals_by_bill_to = nil unless show_custom_totals_by_bill_to?`
- `ecat_customers_controller.rb:60` — **the identical line in `list`**, the action that re-renders the `_list` partial for AJAX refreshes
- `views/ecat_customers/index.html.erb:68` — the selected-period **total card** is inside `if @custom_totals_by_bill_to.present?`
- `views/ecat_customers/_list.html.erb:13-14, 37-39` — the per-customer **column header and cells** use the same condition

`ecat_customers_controller.rb:24` computes `@custom_sales_total` correctly for every range; line 26 then discards the hash the view checks. That is why a correctly calculated Previous Month total is invisible.

**The second call site is load-bearing for the fix.** `index` serves the first page load; `list` serves every subsequent sort, page, and filter change and renders the same partial. A repair applied only at line 26 would show the selected-period column on arrival and silently drop it the moment the user sorts or filters — a partial fix that presents as a new intermittent bug. Both call sites must move to the same display policy, and the acceptance criteria must exercise a list refresh, not only initial render.

`CODE-IMPLICATION` — the export takes a **different** branch. `Controllers::EcatCustomer::ExportCsv` keys on `context[:custom_totals_by_bill_to].present?`, which is populated unconditionally by `Query#get_customer_totals`. The controller's buggy gate never reaches it. This is the precise mechanism behind "calculated and exported but hidden on the page."

### 6.2 CSV field counts — exact, from `app/services/controllers/ecat_customer.rb:15-42`

| Branch | Header fields | Row fields | Deficit |
|---|---|---|---|
| Selected-period column present | **9** — Bill to Code, Customer, City, State, Last Year Sales, Current Year Sales, `<label> Sales`, Backlog, Last Order | **10** | **1** |
| No selected-period column | **8** — same minus the period column | **9** | **1** |

The unlabeled trailing value is `context[:customer_price_levels][customer.code]`, built by `Query#get_customer_price_levels` as `PriceLevel.where(organization_id:).pluck(:code, :cue_character)` keyed on `customer.default_price_code`.

`CODE-IMPLICATION`: the extra field is **`PriceLevel.cue_character`**. It is not customer class. The label is `Price Level Cue`.

Additional observation for the implementer, not new scope: `_list.html.erb:44` renders the same value on the HTML page as `<td data-label="">` — an empty label. The page and the CSV share the same missing-label omission.

`PROD-REPRO`, supplied exports checked 2026-08-04:

- Previous YTD export: 1,965 rows; 9 headings; every row has 10 fields; trailing values are `DN`, `EP`, `WS`, or one blank.
- Both Current Month exports: the same 1,965 rows and 9→10 mismatch; files are byte-identical.
- Previous YTD uses `Previous YTD Sales`; Current Month uses `Current Month Sales`.
- Customer identity and ordering are unchanged; 408 selected-period values differ between Previous YTD and Current Month.

### 6.3 What Kylor must reproduce before replacing SERV-2449

- [ ] Previous Month: selected-period total card **and** per-customer column absent.
- [x] Previous YTD: both present.
- [x] With Previous YTD selected, a Customer list refresh retained the
  selected-period card and column. `PROD-PASS`, Kylor-supplied screenshot
  2026-08-04: `Screenshot_2026-08-04_at_8.46.13_PM-b78f3da7-c8e2-47db-872c-9f46e61597ea.png`.
- [ ] Same selected range on page and CSV.
- [ ] Complete customer-set membership under current search and territory filters — the top total must cover every matching account, not just the visible page.
- [x] CSV header field count — 9.
- [x] Every CSV row field count — all 1,965 rows contain 10 fields.
- [x] Confirm the extra value is the price-level cue character, matching `PriceLevel.cue_character` — observed values `DN`, `EP`, and `WS`; source path confirms the field.

Current Month was captured twice and the exports are byte-identical. Yesterday remains optional.

---

## 7. SERV-2196 — decision record and compatibility

### 7.1 The recorded fixture does not survive contact with production

Live SERV-2196 description (read-only, unchanged since 2025-10-23, To Do, unassigned, Unprioritized, reported by chuck):

> Customer 70461 is assigned to (BillTo) territory 900. That customer has a ShipToTerritory of 905 (among several). Invoice INV1446401 for that customer should be viewable for territory 900, and not 905. User [dvaccarowholesale] is assigned to territory 905 (not 900). Per territory permissions, user should not be able to see that invoice, but can.

`SQL-BASELINE`, checked 2026-08-04:

| Ticket claim | Production today | Verdict |
|---|---|---|
| Customer `70461` in `shl` | Does not exist. The only `70461` anywhere is in `pf` (Palecek), unrelated. | **INVALID** |
| Invoice `INV1446401` | Exists in `shl`. Bill-to **`72170` FERGUSON**, ship-to **NULL**, rep_number `936`, `$276.80`, dated 2025-08-26. | corrected |
| Bill-to territory `900` | Customer `72170` FERGUSON has `["900"]`. | **confirmed** |
| A ship-to territory `905` | Customer `72170` has 3 ship-tos carrying `905`. | **confirmed** |
| User `dvaccarowholesale` on `905` | Dana Vaccaro now holds **`["912"]`**, not `905`. | **STALE** |

The ticket's customer number is wrong; the customer is `72170`. The named user no longer holds the territory. **The reproduction cannot be re-run as written.**

A currently valid replacement fixture exists:

| Role | Account | Shape |
|---|---|---|
| Restricted `905`-only rep | **`shl/adams`** (Adams Smith) | non-admin both columns, blank customer number, user type `Sales Reps SH/Mer/L1`, `access_all_customer_sales_totals = false`, territories `["905"]` |

Two other `shl` accounts hold `905` and must **not** be used: `dszekely` (org admin) and `wfalk1`/`mikebush` (all-customer totals true).

### 7.2 The mechanism is a collapsed ship-to key, not ship-to precedence

`CODE-IMPLICATION` — `Warehouse::ExtractsAndTransforms::Format`:

```ruby
def format_customer_key(organization_id, customer_code, shipping_location_code = nil)
  ["#{organization_id}-#{customer_code.try(:downcase)}",
   shipping_location_code.try(:downcase),
  ].compact.join("---")
end
```

`.compact` drops `nil`. A shipping location whose `code` is NULL therefore produces a `ship_to_key` **identical** to the customer key. `TerritoryToShipToBridge` writes `[territory_key, customer_key, ship_to_key]` using that same helper, and `SalesPortalInvoiceDimension` builds the invoice's `ship_to_key` from `customer_ship_to_number` the same way. `FilterItemsByTerritoryCode` then matches on `customer_key IN (...) OR ship_to_key IN (...)`.

`SQL-BASELINE` for `shl`:

| Fact | Value |
|---|---|
| Total shipping locations | 3,703 |
| With a NULL `code` | **3,703 — every one** |
| NULL-coded and carrying a territory | 3,699 |
| Portal invoices | 450,558 |
| With a NULL `customer_ship_to_number` | **450,558 — every one** |
| `territory_access_via_rep_number` | not enabled |
| Customer `72170` FERGUSON ship-tos | 534, all NULL-coded, all carrying territories; 14 carry `900`, 3 carry `905` |

Both sides of the predicate collapse onto the customer key. Every ship-to territory in `shl` grants the whole customer account.

**Consequence for the A/B choice.** Option A restricts a ship-to-only rep to "transactions addressed to that exact ship-to." In `shl` there is no such thing — the collapsed key makes every FERGUSON invoice look addressed to every FERGUSON ship-to. **Option A does not fix the reported case unless the collapsed-blank-ship-to-key repair ships first.** Option B ("a populated bill-to territory controls transaction access") resolves it regardless.

This is the single most decision-relevant fact available and it was not in any prior document.

### 7.3 Exposure is different, and smaller, than recorded

The prevalence query in `BRENT-ENGINEERING-QUEUE-2026-08-04.md` joins `portal_invoices.customer_ship_to_number = ship_to`. It therefore **cannot** see the collapsed-key class, because those invoices have NULL ship-to numbers. It structurally misses the reported case.

`SQL-BASELINE` 2026-08-04, both classes:

**Class 1 — populated ship-to codes with genuine ship-to-only territories** (the recorded query, re-run):

| Metric | 2026-08-04 recorded | Re-derived today |
|---|---|---|
| Orgs with ship-to territory assignments | 47 | **47** |
| Orgs with ship-to-only assignments | 33 | **33** |
| Orgs with matching invoices | 7 | **7** |
| Matching invoices | 824,089 | **824,090** (imports are ongoing; treat as approximate) |

The seven: **`cci`** Currey & Company, **`clli`** Craftmade, **`clm`** Crystorama, **`ffdm`** Fine Furniture Design, **`hfg`** Hubbardton Forge, **`ihw`** Interlude Furniture, **`kal`** Kalco Lighting / Allegri Crystal.

Note `clm` is the original EBR-91 Customers requester and `kal` is the organization behind the retired stale Bet A example. Neither fact changes their disposition here.

**Class 2 — collapsed NULL-ship-to-code keys** (new):

| Org | NULL-coded ship-tos with a territory | Customers where the collapsed territory is **not** on the bill-to | Distinct over-granted territories |
|---|---:|---:|---:|
| `sarreid` Sarreid, Ltd. | 4,814 | **4,814** | **1** (territory `1`) |
| `shl` Savoy House Lighting | 3,699 | **24** | 18 |
| `gl` Golden Lighting | 2,350 | 0 | 0 |
| `dpl` Dasch Design | 2,237 | 0 | 0 |
| `ebc` Emerson Bentley | 1,007 | 0 | 0 |

`gl`, `dpl`, and `ebc` collapse keys but their collapsed territories always match the bill-to, so there is **no over-grant**. They are not exposed.

`sarreid`'s 4,814 customers all over-grant a single territory coded `1`. `SQL-BASELINE`: **no active `sarreid` user holds territory `1`.** The exposure is latent, not active. It becomes live the moment anyone is assigned that territory.

`shl`'s real exposure is **24 customers**, not 1,364. The worst by a wide margin is `72170` FERGUSON — bill-to territory `900`, over-granting to **17** other territories: 904, 905, 906, 911, 912, 914, 915, 921, 922, 930, 933, 934, 936, 941, 942, 969, 992. The remaining 23 customers over-grant one to three territories each.

The two classes do **not** overlap. Twelve distinct organizations have some ship-to-derived exposure.

### 7.4 Decision record — completed 2026-08-04

```text
selected_model:                              A — bill-to full account; ship-to-only exact-location access
customer_shell_visibility:                   visible when at least one child ship-to is authorized
invoice_rule_when_bill_to_and_ship_to_differ: bill-to match grants all; otherwise exact nonblank ship-to match only
order_rule_when_bill_to_and_ship_to_differ:  same as invoice
existing_client_default:                     staged strict rollout after blank-key and reliance audit
new_client_default:                          strict Option A
compatibility_flag_owner:                    no permanent legacy mode; any temporary migration control needs an owner and removal date
rollout_cohort:                              shl, sarreid, gl, dpl, ebc first; then the seven populated ship-to invoice organizations
acceptance_owner:                            Kylor
collapsed_key_prerequisite_accepted:         yes
```

Decision basis: Option A matches the longstanding `Sales Territories` and `Accessing Sales Portal Data` product documentation and preserves real multi-location customer ownership. Production contains 324 customer accounts across 8 organizations split among multiple ship-to-only territories and multiple restricted reps, covering 8,507 ship-to locations. Of those accounts, 238 map to at least two reps who logged in during the last year. In 6 organizations with matching invoice data, 494 active restricted Sales Portal users hold relevant territories and 138 logged in during the last year. Option B would remove legitimate ship-to-derived access. Option A is selected with the collapsed-key repair and staged migration.

Before the SERV-2196 engineering GO:

1. Restate the fixture as `shl` / customer `72170` FERGUSON / invoice `INV1446401` / restricted user `adams`.
2. Reproduce it: as `adams`, open `INV1446401` and confirm it renders today.
3. Review the five blank-key organizations and the seven class-1 organizations with a named owner per organization.
4. Decide whether `sarreid`'s latent territory-`1` grant is intended before anyone is assigned it.
5. Name the owner and removal date for any temporary migration control.

---

## 8. Discrepancy ledger

### 8.1 Live Jira, read 2026-08-04

| Record | Live state | Statement | Label |
|---|---|---|---|
| EBR-40 | Approved, unassigned, Medium, updated 2026-08-04 | Summary still reads "Territory filter isn't working for invoice list" while the primary route passed | `STALE` |
| SERV-2447 | To Do, unassigned, Unprioritized | Summary still reads "unify the two territory-scope paths"; the shared resolver is retired | `STALE` |
| EBR-212 | Approved, unassigned, Medium | Presents broad Dashboard filter work despite the KPI pass | `STALE` |
| SERV-2448 | To Do, unassigned, Unprioritized | Summary still reads "should match invoice list scope (Bet A ...)" | `STALE` |
| EBR-91 | Approved, unassigned, Low | Retains the unsupported export redesign | `STALE` |
| SERV-2449 | To Do, unassigned, Unprioritized | Summary frames it as "selected-range total and export must share one period (Bet A / EBR-91)" | `STALE` |
| SERV-2196 | To Do, unassigned, Unprioritized, untouched since 2025-10-23 | Fixture invalid — see 7.1 | `INVALID` |
| SERV-2431 | Ready to Accept, **Olga Gnezdyonova**, Medium | Accurate. Assignee was not recorded in prior PM docs. | `PROCESS` |
| SERV-2178 | In Progress, Brent, last updated 2025-09-05 | Status implies active work; history says paused | `STALE` |
| EBR-180 | Triaging, unassigned, Lowest | Consistent with pause | — |
| EBR-474 | Triaging, **Sarah Moravec**, High | Older duplicate. Assignee not previously recorded. | `PROCESS` |
| EBR-601 | Waiting for Client, High | Canonical | — |
| EBR-7 | Triaging, High | Open pending real acceptance | — |
| SERV-747 | Done | Leave Done | — |

**Sprint.** `SERV-2447`, `SERV-2448`, `SERV-2449`, and `SERV-2196` carry **no** Sprint — the reset's statement is confirmed. But **Sprint "June 2026" (id 651, board 3) is still `state: active`** with an end date of 2026-06-26, five weeks past, and **`SERV-2431` is still in it**. `SERV-2178`'s sprints are all closed. Closing that sprint is normal board administration and should not be done as part of the ticket pass.

### 8.2 Confluence page `1819836417` — re-read live, version 7, edited 2026-08-04T17:56Z

The page was last edited **before** the afternoon walkthrough and probe, so its status line is stale by a few hours.

| Statement on the page | Label | Correction |
|---|---|---|
| "No acceptance criterion has been executed yet." | `STALE` | Invoice June and Dashboard KPI both passed later that day |
| "The remaining verification dependency is the wwjc portal warehouse build." | `STALE` | Completed 2026-08-04 20:01:25 UTC |
| A2.4 requires a **scope header block**, a **totals row**, and the stable header `Selected Range Sales` | `STALE` | All three retired by the reset |
| A2.5 requires CY/LY relabeling | `STALE` | Retired |
| Q11/Q12 record PO approval for the totals row and scope block | `STALE` | Withdrawn |
| §8: "EBR-7: discounts are already reflected in the invoiced spine — **close the ticket, do not rebuild.**" | `STALE` | This is the doctrine closure the reset explicitly forbids |
| §3.4: "all of wwjc's codes are uppercase"; verify the casing fix on `cci`, `ta`, `ih`, `bmc2`, `gb` | **`INVALID`** | See Finding B below |
| §3.4: "0 of 14,019 wwjc ship-tos carries a territory code" | **accurate** | Confirmed: 0 of 14,018 |
| §2 fixture register | mostly accurate | `rfreeman` and `bulluckfurn` are customer users — see 3.4 |
| §3 baselines | accurate for June; Current-YTD rows have drifted | June `$123,585.35` reconfirmed exactly |

**Finding B, stated precisely.** `ShippingLocation#territory_codes` reads `territory_codes_json`, and `before_validation :downcase_territory_codes` downcases every write. Production contains 488,069 ship-to rows with territory data; **`territory_codes_json` contains zero uppercase characters** across all of them. The legacy `territory_codes` text column does retain original casing in 152,295 rows (e.g. `["H"]` in `bts`, whose json is `["h"]`), but that column is only exposed through `territory_codes_yaml`, which `TerritoryToShipToBridge` does not use. The bridge builder and the code enumerator both work in lowercase and therefore agree.

The source-level asymmetry the review identified is real but currently unreachable. It would only bite if the downcasing callback were bypassed — a bulk SQL load, for example. **Ship-to casing stays parked, now on evidence rather than on a missing fixture.** Open decision #8 in the system spec is answered.

### 8.3 Confluence pages `1819869185`, `1819901953`, `1820262402`, footer `1820655618`

`PROCESS`: Not re-read in this pass; only `1819836417` was re-verified live. Their stale statements as recorded in `EXECUTION-SALES-PORTAL-RESET-NEXT-ACTIONS-2026-08-04.md` §2 are carried forward unchanged. Re-read each immediately before replacing it, and check whether the version number has moved since 2026-08-04.

### 8.4 Corrections to the PM record itself

| Prior PM statement | Correction | Label |
|---|---|---|
| Control customer `14378` carries territories `D6 LORNE GARDNER`, `30440 Interim Rep House Account` | Those are the invoice's `rep_number`. Bridge territories are `112 barris group`, `d6 lorne gardner`. Control still valid. | `SQL-BASELINE` |
| SERV-2196 concerns customer `70461` | Customer is `72170` FERGUSON; `70461` does not exist in `shl` | `SQL-BASELINE` |
| A `905`-only user could see the invoice | The named user now holds `912`; use `adams` | `SQL-BASELINE` |
| SERV-2196 is a bill-to/ship-to precedence question | It is a collapsed NULL-ship-to-key match | `CODE-IMPLICATION` |
| Ship-to-only prevalence is 7 orgs / 824,089 invoices | That is one of two classes and misses the reported case | `SQL-BASELINE` |
| Ship-to casing needs an affected org | No organization is affected today | `SQL-BASELINE` |
| The Customers gate affects Previous Month | It affects four ranges: `all_available`, `current_mtd`, `previous_month`, `yesterday` | `CODE-IMPLICATION` |
| The Customers gate is one line in `index` | It is applied at **two** call sites — `index:26` and `list:60`. `list` re-renders the same partial on AJAX sort, page, and filter changes, so a one-site fix regresses on first interaction. | `CODE-IMPLICATION` |
| "Dashboard sub-actions" | Ten named actions, enumerated in 4.2 | `CODE-IMPLICATION` |
| Dashboard routes 4–6 have not been run because `cmallon` credentials are unavailable | Controlled `betaverify` / `WW only Reps` `PROD-REPRO` ran all three routes, returned protected metrics, and restored the original group. | `PROD-REPRO` |

---

## 9. Replacement bodies

Complete bodies. Replace the existing description; do not append a comment. Apply only after Kylor approves the whole pack and the gates in section 1 close.

### 9.1 EBR-40

**Summary:** `Invoice territory filter — primary route verified; edge validation pending`

```markdown
## Sales Portal Invoice territory invariant

Current authority: Sales Portal system specification (2026-08-04), Decision — retire and restart Sales Portal Bet A (2026-08-04), Pre-Jira verification (2026-08-04). Implementation: SERV-2447.

### Product result

`PROD-PASS` 2026-08-04: the legitimate non-admin fixture `wwjc/betaverify` selected `105:1 Gigi Lane` for 2026-06-01 to 2026-06-30. The Invoice UI displayed `$123,585`, matching the SQL baseline within display rounding.

`SQL-BASELINE` re-derived 2026-08-04: 110 invoices, 75 accounts, `$123,585.35`. The book is 1,152 customers.

`SQL-BASELINE` re-derived 2026-08-04: the union of all six assigned territories for the same period is 224 invoices, 127 accounts, `$221,114.05`.

`OPEN-DECISION`: the original capture did not prove the 110-row count.

This request no longer asserts that the Invoice territory filter is broadly broken.

### Product invariant

A non-admin rep sees only the customer and ship-to territory book authorized to that user. A selected territory narrows that book and must never widen it. Invoice and order `RepNumber` access is a separate, feature-gated mechanism.

### Validation required

- 110-row June count and `$123,585.35` total for `105:1 Gigi Lane`
- one assigned territory
- union of six assigned territories = 224 / `$221,114.05`
- NULL territory assignment fails closed (`wwjc/tomo`)
- empty-array territory assignment fails closed (`wwjc/jamiegatto`)
- a genuinely zero-book territory returns zero and does not fall back (`wwjc/bscarpa`, `104:1 Bella Scarpa`)
- explicit selection narrows an all-customer-totals user
- one organization whose ship-tos actually carry territory assignments — `wwjc` has none of 14,018

Ship-to territory casing is **closed without a run**. `SQL-BASELINE` 2026-08-04: `territory_codes_json` contains no uppercase character in any of 488,069 production ship-to rows, and `ShippingLocation` downcases on write. The bridge and the enumerator agree. No organization can currently exercise the defect.

Collapsed blank ship-to keys are **evidenced without a run** and tracked with SERV-2196 rather than here.

### Decision rule

If every runnable case passes, close or reclassify as verified regression coverage. If one fails, create a focused repair naming the fixture, route, expected result, observed result, and root path.

### Out of scope

Shared territory-resolver rewrite; `RepNumber` changes; Customer display or export work; Dashboard redesign; revenue or amount-contract changes.
```

### 9.2 SERV-2447

**Summary:** `Validate Sales Portal Invoice territory edge cases after primary-route pass`

```markdown
## Invoice territory regression validation

Product request: EBR-40. Current authority: Sales Portal system specification (2026-08-04), Decision — retire and restart Sales Portal Bet A (2026-08-04), Pre-Jira verification (2026-08-04).

### Current result

`PROD-PASS` 2026-08-04: restricted `wwjc/betaverify`, `105:1 Gigi Lane`, June 2026 — UI `$123,585` against a `$123,585.35` SQL baseline.

`SQL-BASELINE` 2026-08-04: 110 invoices / 75 accounts / `$123,585.35`; six-territory union 224 / 127 / `$221,114.05`; organization-wide contrast 1,693 / 824 / `$1,832,799.91`.

`OPEN-DECISION`: the UI capture did not prove the 110-row count.

The broad defect premise and the shared-resolver instruction are retired. No Invoice behavior change is authorized until an edge case fails.

### Execute

Add or run focused assertions for:

1. one selected assigned territory
2. union of assigned territories = 224 rows / `$221,114.05` for June 2026
3. Gigi Lane June count = 110, total within documented rounding tolerance
4. NULL territory assignment fails closed
5. empty-array territory assignment fails closed
6. a zero-book territory returns zero without falling back
7. explicit selection narrows an all-customer-totals user
8. an organization whose ship-tos actually carry territory assignments

Record the portal warehouse timestamp for every territory-dependent check. The build in effect for the evidence above is `portal_20260804200125` (2026-08-04 20:01:25 UTC).

Two cases previously listed here are now closed by evidence and require no assertion:

- **Mixed-case territory codes.** `ShippingLocation#territory_codes` reads `territory_codes_json` and downcases on write. `SQL-BASELINE`: zero uppercase characters across 488,069 production ship-to rows.
- **Collapsed blank ship-to keys.** Reproduced in data and moved to SERV-2196, where it is the actual mechanism.

### Done when

Passing cases are covered by regression tests; no permission check is stubbed in a test proving scope; failures are split by root cause; passing behavior is not rewritten. If all cases pass, close or reclassify as regression coverage.

### Out of scope

Shared territory resolver; SERV-2448 Dashboard residuals; SERV-2449 Customers work; SERV-2196 semantics; EBR-180/SERV-2178; revenue recalculation.
```

### 9.3 EBR-212

**Summary:** `Sales Portal Dashboard territory — KPI verified; Top-N and drill-through pending`

```markdown
## Dashboard territory residual validation

Implementation: SERV-2448. Completed predecessor: SERV-1092. Current authority: Sales Portal system specification (2026-08-04), Decision — retire and restart Sales Portal Bet A (2026-08-04), Pre-Jira verification (2026-08-04).

### Current result

`PROD-PASS` 2026-08-04: `wwjc/betaverify` selected `105:1 Gigi Lane` and Current YTD. Invoices and Dashboard each displayed `$836,263`.

`STALE`: that is a timestamped observation, not a baseline. `wwjc` org-wide totals drift roughly +0.8% per week as invoices land inside closed windows. Re-verify closure against the closed June 2026 period instead: `105:1 Gigi Lane`, 110 invoices, `$123,585.35`.

The primary Dashboard invoiced-KPI route is verified and is not a current headline defect.

### Residual product questions

- `OPEN-DECISION`: do all Top Customer members belong to the selected permitted book?
- `OPEN-DECISION`: do Top Product values use only territory-scoped orders and order lines?
- `CODE-IMPLICATION`: several Dashboard destination links omit the selected `multi-select-filters`; user-visible impact still needs reproduction.

### Done when

1. Top Customer membership is validated against the selected permitted book.
2. Top Product values are validated against territory-scoped orders and order lines.
3. Drill-through is reproduced for graph, Orders, Backlog, and Top-N destinations.
4. Only links that fail an intended workflow are repaired.
5. The already-passing Invoice KPI link is unchanged unless a regression test fails.

Passing checks become regression coverage. Any failure becomes a focused repair. No shared territory-resolver rewrite is authorized.

### Out of scope

Dashboard redesign; one universal measure across panels; Customers display or export; ship-to casing; bill-to/ship-to precedence; multi-valued `RepNumber`; amount-contract changes.
```

### 9.4 SERV-2448

**Summary:** `Validate Dashboard Top-N territory scope and drill-through persistence`

```markdown
## Dashboard territory residuals after primary KPI pass

Product request: EBR-212. Completed predecessor: SERV-1092. Current authority: Sales Portal system specification (2026-08-04), Decision — retire and restart Sales Portal Bet A (2026-08-04), Pre-Jira verification (2026-08-04).

### Current result

`PROD-PASS` 2026-08-04: the legitimate non-admin fixture `wwjc/betaverify` selected Gigi Lane, Current YTD. Dashboard and Invoices both displayed `$836,263`.

The primary KPI route passes. This ticket no longer asserts that Dashboard territory scope broadly fails.

### Validate

1. Every Top Customer member belongs to the selected permitted customer and location book.
2. Top Product values reconcile to territory-scoped orders and order lines. These widgets use ordered measures; the Invoice KPI uses an invoiced measure. They are not required to agree.
3. Reproduce selected-filter persistence through graph, Orders, Backlog, Top Customer, Top Product, Tradename, and Collection destinations, where the destination can represent the filter.
4. Confirm the existing Invoice KPI link, which already passes `report_params`, remains correct.

Use the closed June 2026 period with `105:1 Gigi Lane` (110 invoices, `$123,585.35`) rather than Current YTD, which drifts.

### Repair rule

Add regression tests for passing paths. Repair only a reproduced failing link or query. Keep each failure scoped to its root cause. Do not refactor the shared territory resolver merely because Dashboard and Invoice paths differ.

### Related but separate

`CODE-IMPLICATION` on `origin/master` `4ff408492`: ten Dashboard data actions — `backlog_total`, `invoice_total`, `all_graph`, `graph`, `budget_graph`, `top_customers`, `top_products`, `top_tradenames`, `top_collections`, `top_territories` — run behind `require_sales_portal_access` only and do not enforce the Sales Portal Dashboard gate. That belongs to the authorization containment package, **not** to this ticket.

### Out of scope

Primary KPI rewrite; Dashboard redesign; shared resolver work; Customers selected-period or export work; ship-to casing; `RepNumber`; amount-contract changes.
```

### 9.5 EBR-91

**Summary:** `Customers selected-period display and CSV structure correction`

```markdown
## Customers selected-period display and export correctness

Implementation: SERV-2449. Current authority: Sales Portal system specification (2026-08-04), Decision — retire and restart Sales Portal Bet A (2026-08-04), Pre-Jira verification (2026-08-04).

### Problem

Sales reps and sales managers use Customers to review account sales for their territory and export the same account list to Excel. When they choose a period such as Previous Month, the export includes that period's sales but the page does not show it. The CSV also contains an unlabeled price-level cue value.

### Evidence

- `PROD-REPRO`: Previous Month omitted the selected-period card and the per-customer column.
- `PROD-PASS`: Previous YTD displayed both, proving the capability exists.
- `PROD-REPRO`: the Customers CSV contains more row fields than headings.
- `CODE-IMPLICATION`: the unlabeled value is `PriceLevel.cue_character`, resolved from `customer.default_price_code`. It is not customer class.
- `CODE-IMPLICATION`: four of the eight ranges are affected — `all_available`, `current_mtd`, `previous_month`, `yesterday`. `current_ytd` and `previous_year` are hidden **correctly**, because the standing CY and LY columns already represent them.

### Done when

1. Ranges not already represented by the standing Current YTD and Previous Year columns show the selected-period total and per-customer value, and keep showing it after the rep sorts, pages, or changes a filter.
2. Current YTD and Previous Year do not gain duplicate selected-period columns.
3. The top selected-period total covers every account matching the current customer search and territory filter, not only the visible page.
4. Export returns the same customer set and selected-period sales as the page.
5. The human-readable period heading is preserved, such as `Previous Month Sales`.
6. Every CSV row has the same field count as the header.
7. The existing cue-character field is labeled `Price Level Cue`.
8. Current revenue calculations, standing-column behavior, and current bill-to/ship-to row math are preserved.

### Excluded

CSV scope or preamble block; totals row; generic `Selected Range Sales`; duplicate selected-period columns for Current YTD or Previous Year; new date ranges; broad CY/LY relabeling; unknown-range fallback as customer-facing scope; revenue changes; territory-resolver work.
```

### 9.6 SERV-2449

**Summary:** `Fix Customers selected-period display and malformed CSV`

```markdown
## Customers selected-period display and CSV structure

Product request: EBR-91. Current authority: Sales Portal system specification (2026-08-04), Decision — retire and restart Sales Portal Bet A (2026-08-04), Pre-Jira verification (2026-08-04).

### Problem

Sales reps and sales managers use Customers to review account sales for their territory and export the same account list. Previous Month sales are calculated and exported but hidden on the page. The CSV also writes a price-level cue value without a matching heading.

### Evidence — mechanism isolated on `origin/master` `4ff408492`

`CODE-IMPLICATION`: `ecat_customers_controller.rb:294-296`

```ruby
def show_custom_totals_by_bill_to?
  params['date_range']['previous_ytd'] || params['date_range']['custom']
end
```

This is Ruby `String#[]` — substring search, not equality. Against the eight ranges in `Eol::DateRanges::DATE_RANGES`:

| range | gate | standing column | verdict |
|---|---|---|---|
| `all_available` | hidden | no | defect |
| `current_ytd` | hidden | CY Sales | correct by accident |
| `previous_ytd` | shown | no | correct |
| `previous_year` | hidden | LY Sales | correct by accident |
| `current_mtd` | hidden | no | defect |
| `previous_month` | hidden | no | defect, `PROD-REPRO` |
| `yesterday` | hidden | no | defect |
| `custom` | shown | no | correct |

The two correct-by-accident ranges are exactly the two with standing columns. **An "always show" fix would create the duplicate standing columns this ticket excludes.** Use an explicit non-standing allow-list.

One gate controls three surfaces, applied at **two** controller call sites:

- `ecat_customers_controller.rb:26` — in `index`: `@custom_totals_by_bill_to = nil unless show_custom_totals_by_bill_to?`
- `ecat_customers_controller.rb:60` — **the identical line in `list`**, which re-renders the `_list` partial on AJAX sort, page, and filter changes
- `views/ecat_customers/index.html.erb:68` — the selected-period total card
- `views/ecat_customers/_list.html.erb:13-14, 37-39` — the column header and cells

`ecat_customers_controller.rb:24` computes `@custom_sales_total` correctly for every range; line 26 then discards the hash the view checks.

Fixing only line 26 produces a partial repair: the column appears on first load and disappears on the next sort or filter, because that request goes through `list`. Both call sites must apply the same display policy.

`CODE-IMPLICATION`: the export takes a different branch. `Controllers::EcatCustomer::ExportCsv` keys on `context[:custom_totals_by_bill_to].present?`, populated unconditionally by `Query#get_customer_totals`. That is why the value is exported but not displayed.

`CODE-IMPLICATION`: exact CSV field counts in `app/services/controllers/ecat_customer.rb:15-42`:

| branch | header | row | deficit |
|---|---|---|---|
| selected-period column present | 9 | 10 | 1 |
| no selected-period column | 8 | 9 | 1 |

The extra value is `Query#get_customer_price_levels` → `PriceLevel.cue_character` keyed on `customer.default_price_code`.

`_list.html.erb:44` renders the same value on the page as `<td data-label="">` — the page shares the missing label.

### Implement

1. Replace the substring gate with an explicit display policy: standing Current YTD and Previous Year columns are not duplicated; every other supported range renders the selected-period total and per-customer value.
2. Apply that policy at **both** call sites — `index` (line 26) and `list` (line 60). Prefer a single shared decision over two copies of the same expression.
3. Prove Previous Month first; keep Previous YTD as a passing comparison; cover `all_available`, `current_mtd`, and `yesterday` as regression cases.
4. Keep Customers account-first: date selection changes values, not customer membership.
5. Ensure the top total covers the full matching customer set after search and territory filters, not only the visible page.
6. Keep export aligned to the same customer set and period.
7. Preserve the human-readable period header.
8. Add the missing `Price Level Cue` heading and assert every row has the header's field count in both branches.
9. Preserve existing calculation sources, standing columns, and current bill-to/ship-to row math.

### Required tests

Previous Month renders total and per-customer value; Previous YTD remains passing; `all_available`, `current_mtd`, `yesterday` render; Current YTD and Previous Year gain no duplicate column; **the `list` action returns the selected-period column for the same ranges as `index`, so a sort, page, or filter refresh does not drop it**; search and territory filters apply to the complete matching set; UI and CSV customer sets agree; UI and CSV selected-period sums agree; CSV header count equals every row count in both branches; `Price Level Cue` present and aligned.

### Excluded

Scope or preamble block; totals row; generic `Selected Range Sales`; new ranges; broad relabeling; customer-facing unknown-range fallback; revenue-definition changes; shared territory resolver; bill-to/ship-to semantic changes.

### Sequence

Start after the authorization containment package ships.
```

### 9.7 Net-new authorization ticket

**Title:** `Sales Portal: contain cross-territory and cross-organization direct-record access`

```markdown
## Problem and evidence

`PROD-REPRO` 2026-08-04 ~14:24 MDT, authenticated production HTTPS session as the legitimate restricted non-admin `wwjc/betaverify` (non-admin on both admin columns, blank customer number, user type `z'-Bet A Verify` 2864, all-customer totals off, territories `105:1`–`105:6`; portal warehouse `portal_20260804200125` completed 20:01:25 UTC, 2h37m after the territory assignment):

| Route | Result |
|---|---|
| `GET /wwjc/e/wwfc-2/invoices/INV65157` | HTTP 200; returned `INV65157`, MEG BRAFF DESIGNS, `$100.00` |
| `GET /wwjc/e/wwfc-2/email_invoice/4667912895` | HTTP 200; returned `INV65157`. GET only; no submission, no email sent |
| `GET /wwjc/e/wwfc-2/customers/14378` | HTTP 200; returned customer `14378`, MEG BRAFF DESIGNS |

`SQL-BASELINE` 2026-08-04: portal invoice `4667912895` is `INV65157`, customer `14378`, `$100.00`, dated 2026-08-04. The customer's bridge territories are `112 barris group` and `d6 lorne gardner` — outside the user's six-territory book.

`CODE-IMPLICATION` on `origin/master` `4ff408492`:

- `ecat_invoices_controller#show` resolves `@current_org.portal_invoices.where(invoice_number:)` — organization-scoped, never territory-scoped.
- `ecat_invoices_controller#email_invoice` uses a global `PortalInvoice.find(params[:invoice_id])` — not even organization-scoped, so cross-organization ids resolve. Its POST branch calls `MobileMailer.portal_invoice(...).deliver_later` with no authorization check at any layer.
- `ecat_customers_controller#org_user_may_view_customer?` returns `true` for any non-admin with a blank `customer_number`; the shipped source carries the comment `# this should restrict to user's territory`.
- `ecat_dashboard_controller` calls `should_display_portal_dashboard?` only in `index`, and only to redirect. Ten data actions run behind `require_sales_portal_access` alone: `backlog_total`, `invoice_total`, `all_graph`, `graph`, `budget_graph`, `top_customers`, `top_products`, `top_tradenames`, `top_collections`, `top_territories`.

`PROD-REPRO`: Kylor temporarily changed only `betaverify` to the
Dashboard-gate-off `WW only Reps` group, used a fresh authenticated session, and
confirmed that `invoice_total` returned a dollar metric, `top_customers` returned
customer names and amounts, and `top_products` returned product details and
amounts. The original `z'-Bet A Verify` group was restored. No `cmallon`
credentials are needed.

`PROCESS`: the deploy-marker question is closed by diff. The reviewed Portal files are byte-identical across the candidate revisions; source references are verified against `origin/master` `4ff408492`.

## Implement

1. Resolve Invoice detail, GET and POST email-invoice, and Customer detail through both the current organization and the signed-in user's authorized customer and territory book.
2. Authorize before rendering or enqueueing mail. A GET must never send.
3. Deny same-organization out-of-book identifiers and cross-organization identifiers alike.
4. Enforce the complete Sales Portal Dashboard gate on all ten data actions listed above, not only `index`.
5. Fail closed for restricted non-admin users whose territory assignment is NULL, blank, or an empty array.
6. Preserve customer-user, in-book rep, company-wide, and admin access.

Likely paths: `ecat_invoices_controller.rb`, `ecat_customers_controller.rb`, `ecat_dashboard_controller.rb`, `ecat_permissions_helper.rb`, `warehouse_access.rb`, and controller/request tests. Reuse the existing authorized book. SERV-2199 is precedent for the general direct-URL class but did not solve record-level authorization. Do not refactor the shared resolver.

## Acceptance

- `betaverify` cannot retrieve any of the three out-of-book controls; an in-book invoice, email page, and customer still open.
- All ten Dashboard data actions return no metric content for the Dashboard-gate-off
  `WW only Reps` user-type state (non-admin, blank customer number,
  `enable_portal_dashboard = false`, `display_sales_portal_totals = true`,
  `enable_sales_portal = true`). The controlled pre-fix reproduction used
  `betaverify` temporarily in that state and then restored `z'-Bet A Verify`; an
  authorized Dashboard user still receives metrics.
- A user with NULL territories (`wwjc/tomo`) and a user with `[]` territories (`wwjc/jamiegatto`) fail closed on record and Dashboard routes. Do not use `rfreeman` or `bulluckfurn` — both have customer numbers and take the customer-user branch.
- Cross-organization ids and numbers never resolve.
- Unauthorized POST cannot enqueue mail; the delivery count is unchanged after a GET.
- Tests cover customer user, one territory, many territories, NULL, empty array, company-wide, and admin, **without stubbing the permission decision being proved**.

## Exclude

SERV-2449 Customers work; ship-to territory casing; SERV-2196 bill-to/ship-to semantics; collapsed blank ship-to keys; multi-value `RepNumber`; any amount or calculation change.
```

### 9.8 SERV-2196 — selected rule, fixture correction, and engineering scope

Option A is selected. Replace the stale fixture and open-ended A/B framing with the complete block below.

```markdown
## Fixture correction — 2026-08-04

`INVALID`: the reproduction as written cannot be re-run.

- Customer `70461` does not exist in `shl`. The only customer with that code in production is in `pf` (Palecek) and is unrelated.
- The affected customer is **`72170` FERGUSON**, bill-to territory `["900"]`, which matches the territory in the original report.
- Invoice `INV1446401` exists in `shl`: bill-to `72170`, ship-to **NULL**, `rep_number` `936`, `$276.80`, dated 2025-08-26.
- User `dvaccarowholesale` (Dana Vaccaro) now holds `["912"]`, not `905`.

Current valid restricted fixture: **`shl/adams`** (Adams Smith) — non-admin on both columns, blank customer number, user type `Sales Reps SH/Mer/L1`, all-customer totals false, territories `["905"]`. Do not use `dszekely` (org admin) or `wfalk1`/`mikebush` (all-customer totals true).

## Mechanism — 2026-08-04

`CODE-IMPLICATION`: `Warehouse::ExtractsAndTransforms::Format.format_customer_key` builds `[org-customer, ship_to_code].compact.join("---")`. A NULL ship-to code makes `ship_to_key` identical to `customer_key`. `TerritoryToShipToBridge` and `SalesPortalInvoiceDimension` both use that helper, and `FilterItemsByTerritoryCode` matches `customer_key IN (...) OR ship_to_key IN (...)`.

`SQL-BASELINE`: in `shl`, all 3,703 shipping locations have a NULL `code` and all 450,558 portal invoices have a NULL ship-to number. Every ship-to territory therefore grants the entire customer account. Customer `72170` has 534 NULL-coded ship-tos; 14 carry `900` and 3 carry `905`.

**This is a collapsed ship-to key, not a genuine ship-to-only territory grant.** Option A ("ship-to-only sees only transactions addressed to that exact ship-to") does not resolve the reported case until the collapsed-key defect is fixed, because in this organization every invoice is "addressed to" every ship-to. Option B resolves it regardless.

## Product decision — Option A

- Bill-to territory grants the full customer account and all transactions.
- Ship-to-only territory grants the customer shell and transactions for the exact nonblank ship-to.
- NULL or blank ship-to identifiers cannot establish exact-location access and must not collapse into the bill-to key.
- Orders, Invoices, Customers, totals, exports, and direct-record routes must resolve the same authorized book.
- New clients use strict Option A. Existing ambiguous blank-key data receives a staged audit and migration; no permanent over-grant compatibility mode is authorized.

## Exposure — 2026-08-04

Two distinct classes, no overlap, twelve organizations total.

Class 1, populated ship-to codes with ship-to-only territories and matching invoices: 47 organizations have ship-to territory assignments, 33 have ship-to-only assignments, **7** have matching invoices — `cci`, `clli`, `clm`, `ffdm`, `hfg`, `ihw`, `kal` — covering roughly 824,090 invoices. That count moves with ongoing imports.

Class 2, collapsed NULL-ship-to-code keys — this is the class the reported case belongs to, and the class-1 query cannot see it:

| Org | NULL-coded ship-tos with a territory | Customers actually over-granted | Distinct over-granted territories |
|---|---:|---:|---:|
| `sarreid` | 4,814 | 4,814 | 1 (territory `1`) |
| `shl` | 3,699 | **24** | 18 |
| `gl` | 2,350 | 0 | 0 |
| `dpl` | 2,237 | 0 | 0 |
| `ebc` | 1,007 | 0 | 0 |

`gl`, `dpl`, and `ebc` collapse keys but their collapsed territories always match the bill-to, so nothing is over-granted. No active `sarreid` user holds territory `1`, so that exposure is latent. `shl`'s real exposure is 24 customers; the worst is `72170` FERGUSON, whose bill-to territory `900` over-grants to 17 others: 904, 905, 906, 911, 912, 914, 915, 921, 922, 930, 933, 934, 936, 941, 942, 969, 992.

The multi-rep model is active beyond the originating client: 324 accounts across 8 organizations are split among multiple ship-to-only territories and multiple restricted reps, covering 8,507 ship-to locations. Of those accounts, 238 map to at least two reps who logged in during the last year. Six invoice-exposed organizations have 494 active restricted users on relevant territories; 138 logged in during the last year.

## Implement and accept

Repair blank-key construction, rebuild affected warehouse data, and implement Option A consistently in `FilterItemsByTerritoryCode`, legacy `WarehouseAccess`, Customers, totals, export, Orders, Invoices, and Package 1 direct-record checks. Acceptance must cover bill-to full account, exact populated ship-to-only access, divergent ship-to denial, NULL/blank fail-closed, customer-shell navigation, and no widened access. Before GO, name affected-client migration owners and any temporary migration-control removal date.
```

### 9.9 Confluence

Use the four page bodies and the footer-comment replacement already drafted in `EXECUTION-SALES-PORTAL-RESET-NEXT-ACTIONS-2026-08-04.md` §6 and §7, with these additions:

1. In the acceptance-portfolio body (`1819836417`), add: the portal warehouse completed 2026-08-04 20:01:25 UTC; the controlled `betaverify`/`WW only Reps` Dashboard-gate-off reproduction returned metrics on all three tested actions and was restored; ten Dashboard data actions lack the gate; four Customers ranges are affected, not one; the CSV deficit is 9→10 and 8→9.
2. Delete §3.4's ship-to casing paragraph and the `cci`/`ta`/`ih`/`bmc2`/`gb` verification list. Replace with the Finding B statement in section 8.2 of this document.
3. Delete §8's "EBR-7 ... close the ticket, do not rebuild" sentence. Replace with the EBR-7 language in the program-spine replacement.
4. Delete A2.4's scope block and totals row, A2.5's relabeling requirement, and the Q11/Q12 decision rows.
5. Correct the §2 fixture register: `rfreeman` and `bulluckfurn` are customer users and are invalid fail-closed fixtures.
6. Re-read `1819869185`, `1819901953`, `1820262402`, and footer `1820655618` immediately before replacing them; only `1819836417` was re-verified in this pass.

### 9.10 Program spine

Apply the replacement text in `EXECUTION-SALES-PORTAL-RESET-NEXT-ACTIONS-2026-08-04.md` §8, plus:

```markdown
- Ship-to casing — CLOSED without engineering. `SQL-BASELINE` 2026-08-04: `territory_codes_json` contains no uppercase character in any of 488,069 production ship-to rows, and `ShippingLocation` downcases on write. No organization can exercise the defect. Reopen only if a bulk load bypasses the model.
- SERV-2196 — Option A selected: bill-to grants the full account; ship-to-only grants the customer shell and exact nonblank ship-to transactions. The reported case is a collapsed NULL-ship-to-key match, so blank-key repair and warehouse rebuild are mandatory scope. Fixture corrected to `shl` / customer `72170` / invoice `INV1446401` / user `adams`.
```

---

## 10. Manual action order for Kylor

### Initial controlled Jira correction pass

1. Review the complete replacement bodies in section 9. They are coordinated
   replacements, not material to append as comments.
2. Replace **EBR-40/SERV-2447** with their primary-route-pass/closure bodies.
3. Replace **EBR-212/SERV-2448** with their KPI-pass/closure bodies.
4. Replace **EBR-91/SERV-2449** with the narrow Package 2 body.
5. Create **one** net-new Package 1 SERV from section 9.7.
6. Replace **SERV-2196** with the Option A, corrected-fixture, collapsed-key
   body from section 9.8. Do not create a separate Package 3 implementation
   ticket in this sitting.
7. If time permits, re-read the named Confluence authority pages immediately
   before applying their drafted replacements and update the program spine.
8. Verify body, status, board/Sprint, and assignee after every manual action.
9. Issue a fresh GO for **Package 1 only** and assign it to Brent.

Do not create tickets for the passing 2447/2448 primary routes, post Jira
"hygiene" comments, repeat the user-group switch, POST the email form, or reopen
the 57-ticket sweep.

### Later work — not a pre-Jira gate

- Package 1 acceptance: post-fix denial/in-book controls, all ten Dashboard data
  actions, and NULL/empty territory fail-closed behavior.
- Package 2 acceptance: full page/CSV parity and complete filtered-set total.
- Package 3: `shl/adams` reproduction, named migration owners, temporary-control
  expiry if needed, blank-key repair, warehouse rebuild, and staged rollout.
- Separate foundation-exit lane: SERV-2431 and EBR-7 authorized imports;
  EBR-474/601 and EBR-180/SERV-2178 dispositions; post-Package-1 2447/2448
  regression validation.

---

## 11. Briefing for Brent

The initial evidence gate is closed. Previous YTD survived the Customers `list`
refresh, all six Package 1 authorization failures are recorded, the Package 2
display/CSV defect is bounded, and Package 3 Option A is settled. Kylor can now
correct stale Jira authority and issue a GO for Package 1 only. Package 1 is
direct-record authorization containment, Package 2 is the narrow Customers
correction, and Package 3 is the selected Option A territory repair.

Package 1 is confirmed line-by-line against current `origin/master` `4ff408492`.
`Invoice#show` scopes to the organization and never to the user's territory
book. `email_invoice` uses a global `PortalInvoice.find`, so cross-organization
ids resolve, and its POST branch enqueues mail with no authorization check at
all. `Customer#show` returns true for any non-admin with a blank customer
number, and the shipped source says so in a comment. The Dashboard gate is
enforced only in `index`; ten data actions run behind the general Sales Portal
callback alone. All six representative routes are `PROD-REPRO`: the three
Dashboard routes were captured with `betaverify` temporarily in `WW only Reps`,
then the original group was restored. Do not request `cmallon` credentials or
repeat that switch.

Package 2 is smaller and more precise than the ticket suggests. One expression, `params['date_range']['previous_ytd'] || params['date_range']['custom']`, is a Ruby substring search rather than a membership test. It hides the selected-period card and column for four ranges, not one — `all_available`, `current_mtd`, `previous_month`, and `yesterday`. It happens to be correct for `current_ytd` and `previous_year` purely because those two already have standing columns, which means a naive "always show" fix would create exactly the duplicate columns we excluded. One gate controls the card, the column header, and the cells — but it is applied at two call sites, `index` line 26 and `list` line 60, and `list` is what re-renders the partial on every sort, page, and filter change. Fix only `index` and the column will appear on load and vanish on the first interaction, so please treat both as one change. The export takes a different branch entirely, which is why the number is calculated and exported but never displayed. The CSV deficit is exactly one field in both branches — nine headings against ten values, or eight against nine — and the extra value is `PriceLevel.cue_character`.

Package 3 is now decided. Kylor selected the documented hybrid model: bill-to territory grants the full account; ship-to-only grants the customer shell and exact-location transactions. This is not a Savoy-only workflow: production has 324 multi-rep customer accounts across 8,507 ship-tos, and 238 accounts map to at least two recently active reps. The package must also fix the actual Savoy mechanism: all 3,703 `shl` ship-tos and all 450,558 invoices have NULL ship-to identifiers, and `.compact` collapses `ship_to_key` onto `customer_key`, granting the whole account. Repair blank-key construction, rebuild affected warehouse data, and validate the corrected `shl/72170/INV1446401/adams` fixture plus populated exact-ship-to controls.

On the revision question: your GitHub pointer was enough. Master's tip is `4ff408492`, and the only two commits back to the previously reviewed point are your SendGrid windows-1252 fix and the iPad resubmission hotfix, which between them touch inbound emails, order submission, and tests. No Sales Portal path moves, so whatever is actually deployed, the reviewed files are byte-identical and nothing here depends on the deploy marker. One thing that did land since December is `before_action :require_sales_portal_access` on all three portal controllers — which is exactly the state described above, since that callback is broader than the record-level check that's missing.

Two things you can stop worrying about. The ship-to territory casing defect has no current production exposure: `ShippingLocation` downcases territory codes on write and reads the JSON column, and there is not one uppercase character in any of 488,069 production ship-to rows, so the bridge and the enumerator already agree. And the `billing_and_shipping_codes_to_territory_codes_bridge` table that gives a different answer than the customer master is dead — its population is commented out in the importer and nothing reads it.

---

## 12. Slack message

> Brent — the foundation sequence is settled and the initial evidence gate is closed. Package 1 is direct-record authorization containment: all three out-of-book direct-record routes and all three controlled Dashboard-gate-off routes are reproduced failures. Package 2 is the narrow Customers display/CSV fix; the supplied CSVs conclusively reproduce 9 headings versus 10 fields on all 1,965 rows, with unlabeled price cues `DN`/`EP`/`WS`, and Previous YTD survives the AJAX list refresh. Package 3 is selected Option A: bill-to grants the full account; ship-to-only grants the customer shell and exact nonblank ship-to transactions. This is a real multi-rep pattern—324 accounts across 8,507 ship-tos, with 238 accounts tied to at least two recently active reps—not a Savoy one-off. The Savoy mechanism is the collapsed NULL key, so Package 3 must prevent blank `ship_to_key` from equaling `customer_key`, rebuild affected warehouse data, and validate migration cohorts. Kylor is ready for the manual Jira correction sitting and will issue a GO for Package 1 only.
