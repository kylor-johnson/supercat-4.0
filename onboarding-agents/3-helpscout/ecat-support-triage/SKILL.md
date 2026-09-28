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
               supercat_server on GitHub (shallow clone, cite commit + file:line), never
               from memory. iPad behaviour is read from sarreid_ios, newest release/*
               branch matched to the rep's orders.app_version. Check the KB for an
               article; "none exists" is a finding. Before asking the client "which
               user / which surface", check eOL logins in audit_log_entries and
               orders.app_version for the client's domain in the hour before the email.
5. DIAGNOSE  → route to the domain skill, confirm root cause against ground truth
6. REPLY     → draft the response with ecat-client-email (draft only — never auto-send)
7. LOG       → append a dated line to that same client folder's HANDOFF.md
```

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
| Customers or ship-tos missing after an upload | omitted from a **clean** file → hard-delete on omission; if that `customers.csv` logged any `Error`, the deletes were skipped and the error row does not prove the named account is gone | `ecat-ground-truth` → `ecat-customers-build`, and prove identity per the section below |
| Inventory/options wiped after a partial file | **HARD-delete on omission** | `ecat-ground-truth` → `ecat-core-files` / `ecat-options-and-mapping` |
| Expected deletes didn't happen | an `Error` row blocked deletes | `ecat-import-ops` |
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
- **eOL shows old taxonomy or old names.** The left nav is cached for a week
  (`app/models/eol_left_nav_dataflow.rb:366-367`); rule that out before the data.
- **An order won't post to the ERP.** Read `orders.local_customer_code` (set from the
  iPad, `app/services/orders/build.rb:29`) and ask for the exact error text; a reused
  local customer code is a common ERP-side rejection.

## Prove identity before causal claims (hard)

The record the client **named** and the record an **error log** named are different
until you prove they are the same code/name in the **file that actually imported**.

This is the miss that sends a confident wrong email (cci ANTMAR vs line-24999 `'o'`):

1. Look up the named record in Postgres (name **and** code).
2. Look up the error record separately (that run's line, or `Customer # =` from an
   older event). Historical line numbers and customer numbers **drift**.
3. If the codes do not match, they are two problems. Say so. One `Error` row skips
   **that** row; other rows still load (`ecat-ground-truth`).
4. A client who regenerates the CSV and jumps to line N is on a different file.
   Match by `BillToCode` / `BaseItemCode`, never by line number in a new export.
5. Neighbors are evidence: if `0008616` and `0008618` imported and `0008617` did
   not, `0008617` was omitted or that specific row failed. It is not "the file's
   one error at line 24999."

Do not write "that error is exactly why X is missing" unless step 1 and step 2
return the same record.

## Reply posture

Draft with `ecat-client-email` (warm, declarative, point-by-point, **"Best, Kylor"**).
Carry its discipline:
- Don't claim something is fixed/uploaded until it actually is.
- State UI limits honestly rather than overpromising.
- Give the exact next action and who owns it (FTP folder, Admin path, "sync on Wi-Fi").
- Keep internal context (health scores, support history, CDN) out of client copy.

Drafts only. This skill never sends; you paste/approve.

Before presenting the draft: re-read it for broken/truncated sentences. If the
draft says a config or file change is already done, **re-query that field now**.
If it is still the old value, do not claim it is done — tell Kylor the Admin/FTP
step and keep the email in "I will / I have not yet" form.

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
