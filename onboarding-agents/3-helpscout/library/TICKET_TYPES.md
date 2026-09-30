# Ticket types: what clients write in about

The drafter classifies a ticket into one of these types **before** diagnosing. The type
fixes which facts get checked first, which domain skill it routes to, which response
type fits (`RESPONSE_TYPES.md`) and the usual gate category (`ecat-correspondence` § 5).
The type never overrides the gate: any ESCALATE trigger wins, and scope (§ 3a) is applied first.

De-identified: patterns, shapes and role names only. Raw rows are in the gitignored
`runs/library_sources.md`.

## How the taxonomy was derived (and how far to trust the numbers)

- **Data:** BigQuery `onboarding_assessment.helpscout_tickets`, conversations created in the
  last 150 days (2026-05-03 to 2026-09-29) with at least one non-staff message, spam excluded:
  678 conversations, 647 after removing cross-inbox duplicate captures.
- **Tags did not make a usable taxonomy.** All 139 onboarding-inbox conversations are untagged, 87
  support-inbox ones are untagged, and the `bug` tag (154) holds logins, duplicate-order notices
  and app-update replies together. Types below are grouped by **what the client needs**.
- **Method:** all 226 untagged first messages and a sample from each tag were read to name the
  types. Counts come from an ordered keyword rule over subject and first message, not from hand
  labels. I read 80 assigned rows and 63 (79%) were the right type. **Treat each share as
  approximate, about plus or minus 4 points.** 8.8% did not match any type.
- **Sample bias:** the 150 days include one event cluster (the August app-update and
  duplicate-order notices) that inflates type 2. Outside such a cluster expect type 2 near zero.
- **Reproduce or improve it:** hand-label a random 100 before relying on any single share.

## Summary

| # | type | n | share | inbox mix (onboarding / support) | usual gate | response type |
|---|---|---|---|---|---|---|
| 1 | Automated, notification or spam | 69 | 10.7% | 58 / 11 | no reply | acknowledgment (no reply) |
| 2 | Reply to our app-update or duplicate-order notice | 74 | 11.4% | 0 / 74 | DRAFT-AND-PING (ESCALATE if the notice was wrong) | direct answer, or correction of our earlier reply |
| 3 | Import or file error, or a file question | 47 | 7.3% | 9 / 38 | SEND-SAFE only for documented rules | diagnosis plus next action |
| 4 | Order or quote will not submit, export or reach the ERP | 75 | 11.6% | 4 / 71 | DRAFT-AND-PING | answer with a check first |
| 5 | Billing, contract, cancellation, seats | ~4 to 10 | ~1% | 2 / 2 | ESCALATE | owner action plus a holding line |
| 6 | Images and assets | ~19 to 25 | ~3 to 4% | 3 / 16 | SEND-SAFE for documented paths | direct answer, or answer with a check |
| 7 | Login, access or account change | 77 | 11.9% | 9 / 68 | DRAFT-AND-PING | diagnosis plus next action |
| 8 | User groups, territories, rep visibility | 33 | 5.1% | 4 / 29 | DRAFT-AND-PING | answer with a check first |
| 9 | Prices, promos, discounts, freight | 28 | 4.3% | 7 / 21 | DRAFT-AND-PING | answer with a check first |
| 10 | Items, inventory, options or search not as expected | 54 | 8.3% | 8 / 46 | DRAFT-AND-PING | diagnosis plus next action |
| 11 | Sales Portal or reporting numbers | 37 | 5.7% | 5 / 32 | DRAFT-AND-PING | answer with a check first |
| 12 | Scheduling, check-in or chase | 46 | 7.1% | 19 / 27 | DRAFT-AND-PING (chase on something owed: ESCALATE) | scheduling, or chase |
| 13 | How-to or training question | ~14 | ~2% | 2 / 12 | SEND-SAFE when documented | direct answer |
| 14 | Feature request or "can eCat do X" | ~7 | ~1% | 2 / 5 | DRAFT-AND-PING | direct answer (no delivery implication) |
| 15 | Onboarding build thread (files, corrections, next steps) | 6 | 0.9% | 6 / 0 | DRAFT-AND-PING | recap note |
| 16 | Outage or "everything is down" | not counted | inside 7 and the unclassified | | ESCALATE if ours | fleet check first |
| ? | Unclassified | 57 | 8.8% | 0 / 57 | | classify by hand, then add a type if 3 or more share a shape |

Types 13 and 14 split the keyword bucket "how-to / feature ask" (n=21, 3.2%); the split counts are
estimated from the tag mix (`training` 82 and `feature request` 11 in the support inbox), not measured.
Type 6 and 5 are also small in keyword counts and larger in tags (`image asset` 23, `sales and finance` 8);
the ranges give both.

Type 16 and the credential hazard (below) are handling types, not volume types.

## Hazard: credentials in the ticket text

Seen at least twice in 150 days: a plaintext password in a client email and a set of OAuth
credentials in another (plus one Azure client secret, earlier). **Never quote it, never store it
in a draft, VERIFY table or library file.** The draft says "a credential is in this thread" as an
owner action (rotate, and tell the client not to send secrets by email) and refers to it by
position, not value. Applies to every type.

---

## 1. Automated, notification or spam (10.7%)

- **Signals:** subject like "Inventory Feed - <date>", daily report senders on a client domain, voicemail
  or shared-file notifications, ticket-system relays, unrelated marketing or foreign-language event requests.
  Local parts `info, notify, noreply, support` (correspondence § 3e).
- **Check first:** whether a client actually rang or wrote (a voicemail notification can hide a
  real ask: one carried "I can't process an order for a new customer"). A daily feed is an
  automated sender, not a person.
- **Route:** none. `ecat-correspondence` § 3e-3f.
- **Gate:** no reply, counted and listed one line each. The exception is a notification that hides a real ask: then re-classify.

## 2. Reply to our app-update or duplicate-order notice (11.4%)

- **Signals:** subject is our own notice ("update required: version ...", "Action Required: duplicate orders to
  void", "Order Cleanup Notice"); body is "done", "I updated", "she is no longer with us, remove her", "did
  this update correctly?", or "an order is missing after the cleanup".
- **Facts to check first:** the fleet signal and the org's own `orders.app_version` for the sender's
  logins; whether the sender's iPad reports the notice's build; the cleanup list against the org's
  `orders` (status, `export_errors`). Sign-in versus sync events differ (a sync check is not a sign-in;
  iPad sign-in rows carry a NULL organization_id).
- **Route:** `ecat-ipad-app`, `ecat-support-triage` (fleet check, order export bullets).
- **Gate:** most are acknowledgments ("Done, thanks"): no reply. A missing-order or wrong-build
  question is DRAFT-AND-PING; if our notice was wrong, ESCALATE and correct it by name.

## 3. Import or file error, or a file question (7.3%)

- **Signals:** "Import error", "fatal error occurred", "Error Report", "Item not found: ... File: ...
  Line no", matrix or option files, UPC in scientific notation, price-level code with a space, "can it be
  automated", SFTP or PowerShell moves.
- **Facts to check first:** `import_events` for that org and file (fatal vs error vs warning; the org's
  `enable_new_product_importer`), which file actually ran (line numbers drift across exports; match by
  `BillToCode` / `BaseItemCode`), scheduled drops of the same file, whether the named record is the record
  the error row names (triage "Prove identity").
- **Route:** `ecat-core-files`, `ecat-customers-build`, `ecat-options-and-mapping`, `ecat-images-ftp`; import
  rules in `ecat-ground-truth`.
- **Gate:** SEND-SAFE only for a documented rule (a length limit, an import order, a header name). Any
  claim about what an Error row did to omitted records is read from the org's flag first: DRAFT-AND-PING.

## 4. Order or quote will not submit, export or reach the ERP (11.6%)

- **Signals:** "orders not processing", "did not come into SAP", "hundreds of old POs by email",
  "order error, try again later", "Missing Quote", "QR code needed to recover", "Batch Order Export endpoint not
  returning", "promo code edit didn't work", "warehouse custom field required".
- **Facts to check first:** `orders` row (exists or not; `export_errors`, `local_customer_code`, status, order
  source and `app_version`); the audit "order submission" row exists only after the permission check passes, so
  its absence does not prove the server was never contacted; ERP error text (ask for it, do not name a cause);
  `mark_orders_sent` and `Order updated` events; fleet check for a cluster.
- **Route:** `ecat-support-triage` order bullets, `ecat-ipad-app` (order submission), `ecat-online` for server orders.
- **Gate:** DRAFT-AND-PING. ESCALATE for a repeat of a defect we reported fixed, or a chase.

## 5. Billing, contract, cancellation, seats (about 1%)

- **Signals:** "official notice of contract termination", "did something change on billing invoices?", "how
  are user seats counted under our 25-user plan", "who signs the contract", an invoice-legitimacy question.
- **Facts to check first:** who owns billing; the seat definition in the org's plan (the source for it is not
  established in this library: find it before quoting a number); never state a balance from a mirror
  without the billing owner.
- **Route:** `supercat-data-routing` (billing source); no domain skill. `truth-discipline` (billed is not collected).
- **Gate:** ESCALATE always. Draft is an owner-action note plus at most a one-line holding reply. Do not disclose
  another org's billing state.

## 6. Images and assets (about 3 to 4%)

- **Signals:** "images not loading", "option images not showing on iPad", "how do I update the icon", "catalog tile
  size", "hide photo on an export", lifestyle imagery, missing-images report says present.
- **Facts to check first:** FTP folder (`/images` flat, `/option_images`), filename match to `ImageFileName`,
  `.jpg` lowercase, count limit (6 or 12 with the paid flag), processing time (30 to 45 min), the org's
  `product_synch_requires_photo`, whether the item shows in eOL but not the iPad (device sync).
- **Route:** `ecat-images-ftp`.
- **Gate:** SEND-SAFE when the path is documented and the state was read; else DRAFT-AND-PING.

## 7. Login, access or account change (11.9%)

- **Signals:** "unable to log in", "email me a login link", "change the email/username", "merge old with new",
  "customer disabled from the portal", "blocked ... Cloudflare ID", new associate gets a sync error, "how do I
  get to the admin panel", "portal access for a customer".
- **Facts to check first:** look up the person in `users` across all orgs by email, domain and name; existing
  global login (add it to the org, do not invite a second one); the login's user group and Customer Number;
  which surface (Admin Console, eOL, Sales Portal, iPad) and its URL shape (triage login table);
  `login_events` by `user_id` for sign-ins; fleet check before blaming a browser.
- **Route:** `ecat-go-live`, `ecat-online`, `ecat-support-triage` (URL table).
- **Gate:** DRAFT-AND-PING. Password reset requests: never draft a credential in text; the classifier may block
  launching a drafter on a password-reset ticket (skip those).

## 8. User groups, territories, rep visibility (5.1%)

- **Signals:** "reps can see all customers in the US and Canada", "territory code 200 shows nothing in the
  Portal", "user removal errors", "brand not in his list", "combine rep agency accounts", "beta reps".
- **Facts to check first:** the group's authorisations (trade names, collections), `TerritoryCodes` on customers
  (needed for filtering, not import-fatal), whether the addressee's group has the capability (each group, not the
  main one: a claim true for one group has been false for the sibling group), `access_all_customer_sales_totals`
  for Portal lists.
- **Route:** `ecat-go-live`, `ecat-ipad-app` (territory filtering), `ecat-sales-portal-onboarding`.
- **Gate:** DRAFT-AND-PING.

## 9. Prices, promos, discounts, freight (4.3%)

- **Signals:** "price not showing", "history pricing on the web portal", "promo rounding for Canada", "Stocking - No
  Promo zeroed the line", "order discount on custom products", "freight not prepopulated", "modify price button
  missing".
- **Facts to check first:** **the price level the complaining login renders**, read from the group's
  `default_price_level_id`, else the linked customer's `DefaultPriceCode`, else the group's first authorised level,
  and whether the product has a price at it (`products.prices_json`); `promo_factor`; the site's `price_level_id`
  and My Account choice on eOL. Name the level for that login before reassuring about another.
- **Route:** `ecat-pricing-levels`, `ecat-online`.
- **Gate:** DRAFT-AND-PING.

## 10. Items, inventory, options or search not as expected (8.3%)

- **Signals:** "stock display wrong", "fewer items than expected", "item missing", "inventory not showing on the
  iPad", "search returns tables for a chair", "slow search", "collection name search", "SmartList missing", "option
  group changes".
- **Facts to check first:** a count, not a sync theory. Count active products that should match, then subtract each
  gate with its own count: `deleted`, Hideable (a different switch per surface), trade-name and collection
  authorisation, the group's custom-field filters, and on the iPad `product_synch_requires_photo`. A clean
  inventory import is not correct data: read the quantities a rep sees (non-null `qty_available`, custom columns).
  Option groups: `options.csv` nulls group membership, so `option_groups.csv` is always re-sent after it.
- **Route:** `ecat-ipad-app`, `ecat-options-and-mapping`, `ecat-smartlists`, `ecat-core-files`, `ecat-postgres-audit`.
- **Gate:** DRAFT-AND-PING.

## 11. Sales Portal or reporting numbers (5.7%)

- **Signals:** "2025 sales total is wrong on the customer page", "YTD filter", "invoice status still 'I'", "quota
  or budget graph", "portal shows no customer or sales data", "visibility of unsubmitted orders".
- **Facts to check first:** whether the figure is blank everywhere (a feed/mapping question) before proposing a
  display change; list versus detail source (warehouse snapshot `warehouse_timestamp` versus live portal tables);
  re-upload semantics (a portal upload deletes and reloads unless delta imports are on); Portal access per user
  group; open-orders-only scope; what the widgets are set to.
- **Route:** `ecat-sales-portal-onboarding`, `ecat-postgres-audit`.
- **Gate:** DRAFT-AND-PING.

## 12. Scheduling, check-in or chase (7.1%)

- **Signals:** "can we set something up for Thursday", "do we need another meeting", "where are we with launch", "any
  movement?", "I don't see your invite".
- **Facts to check first:** calendar events with the client in the last 7 days and Fathom recordings by invitee or
  domain (not by title); what we already owe them in earlier threads; today's date and the client's time zone.
- **Route:** `ecat-session-prep` for the meeting, `ecat-client-email` for the reply.
- **Gate:** DRAFT-AND-PING (a date). A chase on something we already owe: ESCALATE.

## 13. How-to or training question (about 2%)

- **Signals:** "where do I upload the exception pricing file", "can the report be filtered to last year's YTD",
  "how are Smart Picks calculated", "what size is the catalog image".
- **Facts to check first:** the KB article (URL or "none exists"), the screen the person actually uses
  (Admin modern versus classic: quote that sidebar), the build.
- **Route:** the domain skill for the topic; `ecat-client-email`.
- **Gate:** SEND-SAFE when the answer is documented and cited to code or KB.

## 14. Feature request or "can eCat do X" (about 1%)

- **Signals:** "can search ignore accents", "stop-sell at zero inventory", "add a reference number to the order
  email", "customer history should not disappear on add to order".
- **Facts to check first:** whether it already exists (a no-code Admin route), whether Jira already tracks it
  (read-only), whether a documented workaround exists.
- **Route:** `ecat-support-triage`, Jira read-only.
- **Gate:** DRAFT-AND-PING. Wording says "logged", never "once it's in" or any delivery implication.

## 15. Onboarding build thread (0.9%)

- **Signals:** client mid-build sends corrected master files, image corrections, customer or pricing files, open-item
  answers; subjects like "Check-In and Next Steps", "Corrected files", "Open Items".
- **Facts to check first:** everything in correspondence § 6 step 0 (consolidate every conversation with that client
  for 30 days, meetings for 14, calendar for 7, the client folder, attachments, and every claim in our earlier replies).
- **Route:** `ecat-onboarding-orchestrator`, then the file skill that applies.
- **Gate:** DRAFT-AND-PING. Default form is one recap note in a new thread, with the threads to close named.

## 16. Outage or "everything is down"

- **Signals:** "servers down?", "site is down, internal error", "unable to load the console", knowledge base 404s.
- **Facts to check first:** the fleet signal for the hour around the message (login and session counts, `import_events`
  fatals by org, other clients' tickets in the same hour). A fleet-wide dip or a cluster is ours; the copy says so.
- **Route:** `ecat-support-triage` fleet-check bullet.
- **Gate:** ESCALATE when ours; otherwise DRAFT-AND-PING.
