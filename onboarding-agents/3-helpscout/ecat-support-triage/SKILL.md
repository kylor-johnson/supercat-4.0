---
name: ecat-support-triage
description: Triage a one-off eCat support request — a HelpScout ticket or a client email — diagnose it, route to the right ecat-* skill, ground it in live client state, and draft a reply in Kylor's voice. Use for ad-hoc issues outside a net-new build (missing images on iPad, wrong price, "everyone disappeared from my customer list", a mid-project question), or whenever a ticket/email needs a diagnosed answer rather than a full onboarding pass.
---

# eCat Support Triage (reactive mode)

The **reactive** entry point to onboarding work. Where `ecat-onboarding-orchestrator`
walks a net-new client through phases, this handles a single inbound signal — a HelpScout
ticket or a client email — and turns it into a diagnosed fix plus a drafted reply.

Always-on rules apply (`ecat-ground-truth`, `ecat-import-ops`, `ecat-data-model`). The
dangerous delete semantics in `ecat-ground-truth` are the most common root cause here.

## The loop

```
1. INGEST    → take the pasted ticket/email (or pull it from BigQuery HelpScout tables)
2. IDENTIFY  → which client/org? known onboarding client or net-new?
3. CLASSIFY  → map the problem to a domain (table below)
4. GROUND    → read ~/repos/ecat-onboarding-workspace/02_Implementation/<Client Name>/CLIENT_PROFILE.md
               (eCat_Onboarding/ in this repo is pointers only); if unknown or unsure,
               run ecat-postgres-audit by org shortname to get REAL state, not a guess.
               Any claim about how the product BEHAVES (what an importer does with an
               absent column, what a flag gates, what a link looks like) is read from
               source, never from memory (sources below). Check the KB for an
               article; "none exists" is a finding. Before asking the client "which
               user / which surface", check eOL logins in audit_log_entries and
               orders.app_version / login_events for the client's domain in the hour
               before the email.
5. DIAGNOSE  → route to the domain skill, confirm root cause against ground truth
6. REPLY     → draft the response with ecat-client-email (draft only — never auto-send)
7. LOG       → standalone use only: append a dated line to that client folder's
               HANDOFF.md. Under ecat-correspondence or a replay, write nothing
               outside the draft file.
```

**Code sources (GROUND).**

- **Server:** `SuperCatSolutionsLLC/supercat_server` master (a fresh clone or GitHub),
  cite the commit SHA and `file:line`. Never the local `~/supercat-code` checkout.
- **iPad:** `SuperCatSolutionsLLC/sarreid_ios`. Master lags; use the newest `release/*`
  branch (2026-09-28: `release/2026.3.1` = build 20260909; August builds ≈
  `release/2026.2.10`, plist 20260818) and match it to the rep's `orders.app_version`.
  Search, option-set handling, order state, pricing and presentation building run on
  the device; measured, four of the first ten replays turned on iPad code.

Do not answer from assumption. If the fix depends on current state (counts, what
imported, what's visible), GROUND first — step 4 is not optional for state-dependent
questions.

## Ingesting from HelpScout

If the ticket isn't pasted, pull it from the BigQuery HelpScout tables via the
bigquery MCP. Confirm the current table/column names with a `list_tables` /
`get_table_schema` call before querying — the warehouse schema changes and the static
docs can lag. Capture: subject, body, customer email/company, and the thread so far.

## Classify → route

| Symptom in the ticket/email | Likely domain | Route to |
|---|---|---|
| Images missing / wrong hero / won't show on iPad | image pipeline / FTP | `ecat-images-ftp` |
| Price wrong, blank, $0.00, or wrong per customer | pricing / price levels | `ecat-pricing-levels` |
| Customers or ship-tos missing after an upload | `customers.csv` replaces the whole list on any non-fatal import, `Error` rows included (`customer_importer.rb:169-175`): the account was omitted from, or rejected in, the file that ran, and the error row does not prove it is the named account | `ecat-ground-truth` → `ecat-customers-build`, and prove identity per the section below |
| Inventory/options wiped after a partial file | **HARD-delete on omission** | `ecat-ground-truth` → `ecat-core-files` / `ecat-options-and-mapping` |
| Expected product deletes didn't happen, or products vanished after a file with errors | depends on the org's product importer: with `enable_new_product_importer` off (the original importer) an `Error` row blocks the soft-delete; with it on, omitted products are soft-deleted on any non-fatal import (`product_importer.rb:101-112`, `product_importer_lib/helpers.rb:62-66`). Read the flag first | `ecat-import-ops` |
| New/updated product file to load | core files build | `ecat-core-files` |
| Option swatches / cascading filters wrong | options + mapping | `ecat-options-and-mapping` |
| SmartList not appearing / wrong items | smartlists | `ecat-smartlists` |
| Rep can't see catalog / wrong customers / login | users, groups, territories | `ecat-go-live` |
| "Why is the item code showing instead of the name" | known UI limit | answer honestly (see `ecat-client-email`) |
| Anything needing live counts/state to answer | live DB audit | `ecat-postgres-audit` |
| **Sales Portal** issue (ERP-fed reporting, order/invoice history, scorecards, portal login) | Sales Portal (ERP data surface) | `ecat-sales-portal-onboarding` for build/import issues (`Order_Data.csv` / `Invoice_Data.csv`, access, territories); ground with `ecat-postgres-audit`; only a genuine ERP-integration/data-flow bug is engineering (Jira, read-only) |
| **eCat Online (eOL)** issue (web catalog, Cart, buyer login, "My Account" markup pricing) | eCat Online — **NOT the iPad** | `ecat-online`; note `ecat-ground-truth` scope (eOL ≠ iPad); ground with `ecat-postgres-audit`, route engineering bugs to Jira (read-only) |
| Trade name / brand on iPad but missing from the eOL left nav | user-group `trade_names_auth` (new trade names are not auto-added to custom lists) | `ecat-online` |
| **iPad runtime** behavior (won't sync, stale catalog, rep sees wrong things, order-pad behavior) | iPad app runtime | `ecat-ipad-app`; check org status gating sync before chasing the data |
| Selected a "no promo" / excluded price level and the line went **$0.00** | `promo_factor` is `0` (iPad multiplies promo by zero) | `ecat-pricing-levels` |

When in doubt between two domains, GROUND with `ecat-postgres-audit` first — the real
state usually disambiguates.

**Symptom checks verified in code** (supercat_server @183d8e1, sarreid_ios `release/2026.3.1`):

- **Sales Portal re-upload.** A portal `order_data.csv` / `invoice_data.csv` upload
  deletes the org's whole set and reloads it, unless the org has
  `enable_portal_delta_imports` on and the model has a delta column
  (`app/models/importer/import_strategy.rb:54-63`). `LastModifiedAt` is parsed and not
  stored (`portal_order_importer.rb:65`, `portal_invoice_importer.rb:62`); it gates
  nothing. Advice to re-upload says "the complete file".
- **Scheduled drops.** Check `import_events` for a scheduled drop of the same file; the
  next drop replaces a hand upload.
- **List vs detail.** The Orders and Invoices list pages read the warehouse snapshot named
  by `app_settings.warehouse_timestamp` (timestamped `*_dimension_<ts>` tables,
  `app/models/ecat_reporting/query_support/invoices.rb:85-88`); the order and invoice
  detail pages read the live `portal_orders` / `portal_invoices` tables
  (`ecat_orders_controller.rb:60`, `ecat_invoices_controller.rb:35`). An "after you
  upload" line says which, with the warehouse timestamp. The refresh schedule is not in
  the repo; state a time only from the timestamp.
- **Portal access.** A portal access claim names the user group.
  `access_all_customer_sales_totals` returns before the login's customer-number filter on
  the list pages (`app/models/warehouse_access.rb:425-427`). The detail pages check only
  Sales Portal access (`require_sales_portal_access`, `ecat_online_controller.rb:85-90`),
  not customer or territory.
- **Check the fleet before blaming one client's browser, device or file.** For "slow",
  "down", "won't log in", or an import that failed, compare the same signal across
  all orgs for the hour around the message (login/session counts in
  `audit_log_entries` or `login_events`, `import_events` fatals by org) and look for
  other clients' tickets in `helpscout_tickets` in the same hour. A fleet-wide dip or
  a cluster of the same failure is ours, and the copy says so. Measured twice: a
  draft told a client his browser was the cause while fleet logins had fallen ~78%
  and another client had reported the same thing five minutes earlier; a sent reply
  blamed a client's file while 15 orgs hit the same fatal that morning.
- **A test the client ran is evidence only once you know what it tests.** Before the
  draft leans on "I tried it in Incognito / on another iPad / with another login",
  say what that test actually used. An Incognito window on eOL is logged out. On a site
  that allows unauthenticated visitors it browses as the mobile site's own org_user and
  that user group's authorisations, not the client's; on a login-only site it shows the
  login page, and once they sign in it is their own group again
  (`app/controllers/eol_controller.rb:57-67`: `allows_unauthenticated_users` decides).
  Read the site's setting before saying which. Another
  iPad on the same login is the same group and the same data. Another login may be a
  different group. If the test used a different group from the one in the complaint,
  the copy says so and explains what their result does and doesn't show. **Timing
  matters too:** if the two tries were minutes apart, the problem may simply have
  ended in between; check the fleet signal (above) before concluding "browser".
- **"Fewer items than expected" is a count, not a sync question.** When a filter,
  search, collection or list shows fewer products than the client expects, first
  count in Postgres the active products that should match, then subtract each gate
  with its own count: `deleted`; `hideable`, which has a different switch per surface
  (eOL drops Hideable products only when the mobile site has
  `hide_products_marked_hideable` on, `app/services/products/query_for_catalog.rb:57`
  via `ecat_products_controller.rb:328`; the iPad drops them unless the rep turns on
  "Show <hidden-products name>" in the app's Settings, a per-device switch that is off
  by default, `ProductQuery.m:601-603,1387-1389,1484-1486`, `DataStore.m:1365-1372`,
  `SettingsPopoverController.m:274-280`, sarreid_ios f2e9877); the group's
  trade-name / collection authorisation; and the group's custom-field filters
  (`user_types.custom_field_filters`, `app/services/products/get_for_user_type.rb:46-58`),
  which can hide whole value ranges of a field from one group. Only when the gates don't
  account for the gap do stale device data, sync or a cache become the explanation.
  Measured: a filter showed 1 of 25 because 24 were Hideable = Y; two replies blamed
  sync first, and the client refreshed and still saw one.
- **Scoping content to some reps or customers has a rep-side answer too.** Admin can
  scope SmartLists only by user group (`user_type.rb:286-292`). Each covering rep can
  also build a My List on the iPad ("New My List…", `SelectListViewController.m:150`).
  A My List belongs to that rep's login: it is backed up to the server as
  `user_stacks` on the org_user (`org_user.rb:57`, `user_stack.rb`) and restored on
  sync (`Synchronizer.m:364-374`), and other reps don't see it. Offer both.
- **An org-setting change on the iPad is picked up at login, not by sync.** The iPad
  reads org settings (the organization hash, e.g. `allow_double_discounting`) from
  the organizations download, which runs at an online sign-in
  (`LoginViewController.m:654`) and when the catalogs screen opens
  (`MainViewController.m:483-491`), sarreid_ios `release/2026.3.1` @f2e9877; the sync
  never fetches it (`ORGANIZATIONS_URL`, `Synchronizer.m:74`, is unused), and an offline
  sign-in reuses the stored settings. Copy that turns one on says "log out and back in
  while online, or switch catalogs"; a sync alone does not pick it up.
- **eOL shows old taxonomy or old names.** The left nav is cached for a week
  (`app/models/eol_left_nav_dataflow.rb:366-367`); rule that out before the data.
- **Two devices on one login.** Saving a user group sets `full_synch` on every login
  in that group (`app/controllers/user_types_controller.rb:77`), and the first device
  to sync clears it (`app/controllers/api_controller.rb:27-28`), so a second iPad on
  the same login never gets that full re-download. Incremental sync sends an entity,
  price levels included, only when its data version is newer than the device's
  (`app/models/data_version.rb:159-166`). `device_id` is stored once when blank
  (`app/models/org_user.rb:395-396`) and is not the sync key. The cheap fix is Refresh
  Data on the stale device; a reinstall works too because it forces a full download,
  so "the reinstall fixed it" doesn't prove a device-id cause.
- **A missing "order submission" audit row doesn't prove the server was never
  contacted.** `Orders::Create` writes that row only after `user_allowed_to_send_orders?`
  passes (`app/services/orders/create.rb:45-46,74-75`); a permission rejection writes
  none, and an on-device validation never POSTs. Say which of those the evidence
  supports.
- **An order won't post to the ERP.** Read `orders.local_customer_code` (set from the
  iPad, `app/services/orders/build.rb:29`), `orders.export_errors`, and ask for the
  exact ERP error text before naming a cause. A reused local customer code has been
  one ERP-side rejection; don't assume it is the one.

## Prove identity before causal claims (hard)

The record the client **named** and the record an **error log** named are different
until you prove they are the same code/name in the **file that actually imported**.

This is the miss that sends a confident wrong email (a named missing customer blamed on an unrelated error row):

1. Look up the named record in Postgres (name **and** code).
2. Look up the error record separately (that run's line, or `Customer # =` from an
   older event). Historical line numbers and customer numbers **drift**.
3. If the codes do not match, they are two problems. Say so. One `Error` row skips
   **that** row; other rows still load (`ecat-ground-truth`).
4. A client who regenerates the CSV and jumps to line N is on a different file.
   Match by `BillToCode` / `BaseItemCode`, never by line number in a new export.
5. Neighbors are evidence: if the codes on either side of the missing one imported
   and it did not, it was omitted or that specific row failed. It is not "the file's
   one error row." Run this check before offering any theory.

Do not write "that error is exactly why X is missing" unless step 1 and step 2
return the same record.

## Reply posture

Draft with `ecat-client-email` (warm, declarative, point-by-point, **"Best, Kylor"**)
and run its pre-send checklist, which is the one home of the copy-truth rules
(nothing claimed done until it is and has been re-queried, names from `users`, the
surface named, internal context kept out). Drafts only. This skill never sends.

**Before drafting a "logged with engineering" reply:** check for an existing Jira ticket
bucket for this issue first (read-only — see the `jira-read-only` rule). Don't promise a
new ticket if one already tracks it; reference the existing work instead of implying fresh
engineering effort. Never create/transition/comment on Jira — read only, then draft text.

## Login / URL shapes (stop the flip-flopping)

When a login or "which surface is this" question comes in, match against the
**confirmed** pattern before diagnosing:

| Surface | URL / path shape | Confirmed source |
|---|---|---|
| **Admin Console** | Host is **`supercat.supercatsolutions.com`** (a subdomain, NOT bare `supercatsolutions.com`). Login form: `https://supercat.supercatsolutions.com/supercat/sessions/new`. A client org: `https://supercat.supercatsolutions.com/<shortname>` (e.g. `.../sccon`). | Verified ground truth (Kylor) |
| **eCat Online (eOL)** | `https://supercat.supercatsolutions.com/<shortname>/e/<url_key>/products` — buyer **login** is `/login` on the same scope, plus `/my-account`, `/checkout`. `<url_key>` is the Mobile Site's `url_key` (Admin → Mobile Sites); an org can have several. Legacy `/<shortname>/m/<url_key>/` redirects to the eOL home. Orgs may also use a custom CNAME. | Code-verified in `config/routes.rb` |
| **Sales Portal** | `https://supercat.supercatsolutions.com/<shortname>/e/<url_key>/portal` — same eOL scope, gated by the mobile site's `enable_sales_portal` | Code-verified in `config/routes.rb` |

## Existing vs net-new client

- **Existing onboarding client:** read their `CLIENT_PROFILE.md` for taxonomy method,
  pricing model, and snowflake quirks before diagnosing. Log the outcome to `HANDOFF.md`.
- **Net-new / unknown:** if the ticket is really the start of an onboarding, hand off to
  `ecat-onboarding-orchestrator` and bootstrap a client folder instead of one-off patching.

## Capture the lesson

If the root cause is generalizable (not client-specific), note it so it can be promoted
to `eCat_Onboarding/<Client>/LESSONS_LEARNED.md` and, eventually, a test fixture. Repeat
tickets with the same root cause are a signal to harden the build, not just reply faster.
