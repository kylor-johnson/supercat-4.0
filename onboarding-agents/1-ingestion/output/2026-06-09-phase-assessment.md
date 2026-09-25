# June 9, 2026 — Onboarding Phase Assessment

## Where everyone is

| Client | Phase (of 7) | Working on | Days in onboarding | Integration | One thing to resolve |
|---|---|---|---|---|---|
| Lib and Co. (libco) | 3 — Building the catalog | Catalog ready | 78 | Us (Managed) | Customer file is being rejected — the price codes in it don't match the price lists set up in the app. |
| Skyard / Pebl (pebl) | 3 — Building the catalog | Catalog ready | ~320 (active since late Jan) | — | No real customers loaded yet — the only orders so far are the team's own test orders. |
| The Coppersmith (tcs) | 3 — Building the catalog | Catalog ready | 50 | Them (Certified) | No customers loaded yet — the catalog is built but there's no one to sell to in the app. |
| Dorell Fabrics (drf) | 4 — Catalog ready | Reps using the iPad | 55 | — | Reps haven't been set up or invited yet — the catalog and customers are ready for them. |

## Standup agenda

### 🔴 Resolve this week
- **Lib and Co. — fix the customer import.** Every customer row is being rejected because the file's price codes (`cad-wsp`, `us-wsp`) don't match the price lists actually set up in the app (`cad`, `imapcad`, `imapusd`, `netprice`). Until this is reconciled, Lib and Co. will keep showing zero customers.
- **The Coppersmith — load customers.** The catalog is built (271 products, 94% with photos) but no customers are in the app yet.
- **Skyard / Pebl — load real customers.** The catalog is built and reps are already poking at it, but the only orders so far are test orders billed to "Pebl" itself.

### ⚠️ Discuss / decide
- **The Coppersmith — is the client flagging a real data problem, or just reviewing the first pass?** Their team sent detailed notes on the initial import in the last week. It reads as a normal first-pass review, but it tripped our "client may be seeing wrong data" alarm — worth a quick gut-check. (See their section.)
- **Lib and Co. — we own their integration but aren't tracking it anywhere.** The deal includes a Managed Integration (Business Central); we should record where that build stands.
- **Dorell Fabrics — confirm the second company domain.** We picked up both `dorellfabrics.com` and `loomcraft.com` from their team's email addresses. Meetings confirm Loomcraft is the parent ("Loomcraft Textiles, DBA Dorrell Fabrics"), so this looks legitimate — just confirm.

### ✅ On track (nothing to resolve)
- **Dorell Fabrics** is the furthest along: catalog built, 389 customers loaded and every one matched to a price list, and an admin has already run a real customer order through the app. Next step is simply setting up and inviting reps. (They run a single net price by design — confirmed — and have no product options by design.)

---

## libco (Lib and Co.)

**Phase 3 of 7 — Building the catalog** · working on **Catalog ready** · eCat iPad
**In onboarding 78 days** · Talking regularly — a call last week and email through yesterday

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kicked off in May; kickoff and onboarding calls on the books. |
| 2 · First import | 🟢 | 907 products loaded. |
| 3 · Building the catalog | 🟢 | Products, inventory, and stories all loaded; 88% of products have a photo; four price lists set up. |
| 4 · Catalog ready | 🟡 | Catalog is built, but no customers are loaded — the customer file keeps getting rejected. |
| 5 · Reps using the iPad | ⚪ | Two rep groups (US and Canadian) were created but nobody's been added to them yet. |
| 6 · Admin trained | ⚪ | No handoff to our support team yet. |
| 7 · Live | ⚪ | Not live. |
| Integration | 🟡 | We own a Managed Business Central integration for them, but it isn't being tracked anywhere on our side yet. |

### Next step
Reconcile the customer file's price codes with the price lists in the app so the customer import stops failing, then re-import customers.

### Things to flag (4)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 4 | Customer import failing on price codes | Database (import log 2026-05-28) | Every customer row errored: "Default price code 'cad-wsp' must be a valid price level code" / "'us-wsp' must be a valid price level code". The app's actual price codes are `cad`, `imapcad`, `imapusd`, `netprice`. |
| 4 | No customers loaded yet (`PHASE_4_VACUOUS_NO_CUSTOMERS`) | Database | 0 customers in the app — a direct result of the rejected import above. |
| 5 | Rep groups created but empty (`USER_TYPES_EMPTY`) | Database | "Lib & Co — US Reps" and "Lib & Co — Canadian Reps" both have zero members. |
| Integration | We own the integration but aren't tracking it (`INTEGRATION_OWNER_UNCLEAR`) | HubSpot deal "Lib & Co - TIER 2" | Deal includes "Managed Integration Build" + "Managed Integration Hosting" — ours to run — but no status is recorded for the build. |

### Recent activity
- **Meetings:** 9 in the last 90 days — last was "SuperCat + Lib & Co: Integration Chat" on June 4.
- **Support:** 1 email thread (8 messages), none still open — last reply June 8.
- **Imports:** Products, inventory, and stories all loaded in the last week; the customer file was attempted and rejected.

### Bottom line
Lib and Co. is in good shape on product data but stuck on customers — their customer file uses price codes that don't exist in the app, so every row bounces. Fix that mapping and the customer count should jump from zero. They've bought a managed Business Central integration that we own and should start tracking.

---

## pebl (Skyard / Pebl)

**Phase 3 of 7 — Building the catalog** · working on **Catalog ready** · eCat iPad
**In onboarding ~320 days since the account was created (project active since late January 2026)** · Very active over support email; no calls captured in the last 90 days

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Long-running, heavily engaged over support email. |
| 2 · First import | 🟢 | 376 products loaded. |
| 3 · Building the catalog | 🟢 | Products and options loaded; 76% of products have a photo; two price lists set up. |
| 4 · Catalog ready | 🟡 | Catalog is built, but no customers are loaded yet. |
| 5 · Reps using the iPad | 🟡 | Five reps are in the app and one logged in June 4 — but they're all in the default group, not a real rep group. |
| 6 · Admin trained | ⚪ | Order-confirmation email is set, but no handoff to our support team yet. |
| 7 · Live | ⚪ | Not live. |

### Next step
Load a real customer list so reps have accounts to sell to, and move the reps out of the default group into a proper rep group.

### Things to flag (4)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 4 | No customers loaded yet (`PHASE_4_VACUOUS_NO_CUSTOMERS`) | Database | 0 customers in the app. |
| 5 | Only test orders so far (`SELF_TEST_ONLY_ORDERS`) | Database | All 9 submitted orders are billed to "Pebl" itself, entered by an admin account — none are real customer orders. |
| 5 | Reps are in the default group (`REPS_IN_DEFAULT_GROUP`) | Database | Five non-admin reps (incl. one who logged in June 4) sit in the default group, so no real rep group exists yet. |
| 3 | Same warning on every product import (`RECURRING_WARNINGS_NO_ERROR`) | Database | 78 product imports carry the same "Custom field 'Certification' is missing" warning (also Color, PackingSize, etc.). Decide: register these custom fields, drop them from the file, or accept the warning. |

### Recent activity
- **Meetings:** 0 in the last 90 days (no recorded calls).
- **Support:** 1 very active email thread (50 messages, 29 from the client), none still open — last reply June 8.
- **Imports:** Products and options loaded repeatedly over the last week, all with the recurring custom-field warnings.

### Bottom line
Pebl is product-complete and reps are already test-driving the app, but there are no real customers and no real orders yet — just the team billing test orders to themselves. The next moves are loading a customer list, putting reps into a real group, and cleaning up the recurring custom-field warnings. Worth noting we've had no calls with them in 90 days — all the back-and-forth is over support email.

---

## tcs (The Coppersmith)

**Phase 3 of 7 — Building the catalog** · working on **Catalog ready** · eCat iPad
**In onboarding 50 days** · Talking regularly — heavy email back-and-forth, last reply June 5

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kicked off April 21; bi-weekly check-ins running. |
| 2 · First import | 🟢 | 271 products loaded. |
| 3 · Building the catalog | 🟢 | Products, options, and stories loaded; 94% of products have a photo; two price lists set up. |
| 4 · Catalog ready | 🟡 | Catalog is built, but no customers are loaded yet. |
| 5 · Reps using the iPad | ⚪ | No reps set up yet. |
| 6 · Admin trained | ⚪ | No handoff to our support team yet. |
| 7 · Live | ⚪ | Not live. |

_Integration: The Coppersmith is building their own integration (a "Certified Pipeline" — Catsy PIM feeding the app); we certify it rather than run it._

### Next step
Load a customer list so the built catalog has accounts to sell to, and continue working through the client's first-pass import review notes.

### Things to flag (2)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 4 | No customers loaded yet (`PHASE_4_VACUOUS_NO_CUSTOMERS`) | Database | 0 customers in the app; the customer file was discussed as part of the integration, not yet imported. |
| 3 | Possible data-mismatch alarm — likely just a first-pass review (`IMPORT_VS_HELPSCOUT_DRIFT`) | Help Scout #14520 (June 2 & 5) | Client's detailed notes tripped the alarm, e.g. "Can you clarify where you are seeing product SKUs with no Dealer Net?" — but a follow-up the same week reads: "Nothing that changes the shape of what you built." Reads as collaborative review of the first import, not a complaint that we shipped wrong data. Standup gut-check. |

### Recent activity
- **Meetings:** 6 in the last 90 days — last was "SuperCat / Coppersmith: Technical Q&A" on May 14.
- **Support:** 4 email threads (35 messages, 11 from the client), none still open — last reply June 5.
- **Imports:** Products, options, and stories loaded in early June (warning-only on two custom fields).

### Bottom line
The Coppersmith's catalog is built and image-rich, and the client is engaged and detail-oriented — their recent notes are a thorough review of the first import, not a sign something's broken. The gap is customers: none are loaded yet. They're handling their own integration (we just certify it), so there's nothing for us to build there.

---

## drf (Dorell Fabrics)

**Phase 4 of 7 — Catalog ready** · working on **Reps using the iPad** · eCat iPad
**In onboarding 55 days** · Quiet on calls and email the last few weeks, but imports are still running (products re-uploaded June 9)

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kicked off in April; path-forward and implementation calls done. |
| 2 · First import | 🟢 | 1,676 products loaded. |
| 3 · Building the catalog | 🟢 | 73% of products have a photo; runs a single net price (confirmed as intentional). |
| 4 · Catalog ready | 🟢 | 389 customers loaded and every one is matched to a price list; an admin has run a real customer order through the app. |
| 5 · Reps using the iPad | ⚪ | No reps set up or invited yet. |
| 6 · Admin trained | ⚪ | No handoff to our support team yet. |
| 7 · Live | ⚪ | Not live. |

### Next step
Set up rep accounts and send invitations so reps can start using the iPad — the catalog and customers are ready for them.

### Things to flag (2)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 3 | No product options — by design (`OPTIONS_INTENTIONALLY_EMPTY`) | Database | Zero options and zero option groups; this is the expected per-SKU fabric model, not a gap. |
| 1 | Second company domain to confirm (`MULTI_DOMAIN_FALLBACK_UNVERIFIED`) | Database + meeting (April 15) | Their team's emails span `dorellfabrics.com` and `loomcraft.com`. A meeting confirms: "the eCat will use 'Dorrell Fabrics' for branding, while invoices will use the legal entity 'Loomcraft Textiles, DBA Dorrell Fabrics'" — so Loomcraft is the parent. Just confirm. |

### Recent activity
- **Meetings:** 6 in the last 90 days — last was "SuperCat / Dorell: Implementation Check-In" on May 18.
- **Support:** 2 email threads (9 messages), none still open — last reply May 5.
- **Imports:** Products re-uploaded as recently as June 9; customers loaded (warning-only) back in late April.

### Bottom line
Dorell Fabrics is the furthest along of the group — catalog built, all 389 customers matched to a price list, and a real customer order already run through the app by an admin. The single open item is reps: none are set up yet. Their single-net-price setup and lack of product options are both intentional, so neither is a problem.

---

_Framework v3.3 · run 2026-06-09 · all metrics pulled from live Postgres, BigQuery (Fathom/Help Scout), and HubSpot at run time._

**Override / resolution notes**
- **drf:** single net price confirmed intentional (`overrides.yml § net_price_only_confirmed`), so the one-price-level question is settled and not re-raised.
- **drf:** `client_domains[]` resolved via the admin-email fallback to `dorellfabrics.com` + `loomcraft.com`; Loomcraft confirmed as the parent legal entity in a meeting, pending a one-time human confirmation.
- **pebl:** `client_domains[]` resolved from the order-confirmation email (`peblfurniture.com`). A rep also appears on `skyard-outdoor.com` (Pebl's legal name is "Skyard furniture Co Ltd.") — see framework feedback.
- **Integration ownership** read from HubSpot deal line items: libco = Managed (us, "Lib & Co - TIER 2"); tcs = Certified Pipeline (them, "The Coppersmith - TIER 3"); drf and pebl = no integration line item (self-serve, suppressed).

**Framework feedback (for the maintainer)**
1. **`VALUES`/`LATERAL` is rejected by the Postgres tool.** The per-file-type import-events query in `RUN_PROMPT.md § Step 1` uses `CROSS JOIN LATERAL (VALUES …)`, which the `execute_sql` MCP refuses to validate. I reproduced the same block-level "most-recent per file type" result with a `UNION ALL` of six `DISTINCT ON (shortname)` selects. Recommend swapping the primitive in `RUN_PROMPT.md` to the `DISTINCT ON` form (or noting the limitation), or future runs will hit the same wall.
2. **`client_domains[]` resolution rule is internally contradictory.** The header says "first non-empty wins" and "concatenate non-empty results" in the same line. For pebl this matters: the order-email gives `peblfurniture.com` only, but a real rep and the company's legal name live on `skyard-outdoor.com`, and pebl has no Fathom under either domain. If "first wins" is the intent, pebl's engagement scan silently misses any `skyard-outdoor.com` activity. Recommend picking one rule explicitly and, for pebl specifically, deciding whether `skyard-outdoor.com` should be a second client domain.
3. **The override tables don't exist.** `onboarding_assessment.client_domain_overrides`, `integration_workstream`, and `client_self_names` are absent from BigQuery (only `fathom_recent_meetings`, `helpscout_tickets`, and an unused `onboarding_clients` exist). The framework already treats them as optional, which is correct — but as written, `INTEGRATION_OWNER_UNCLEAR` will fire on every Managed client forever (libco today) until that table exists somewhere writable. Consider folding integration status into `overrides.yml` (the one config that does exist) so it can actually be cleared.
4. **The biggest real problem this week isn't a named flag.** Lib and Co.'s customer import failing on price-code mismatch is the single most actionable item in the cohort, but it surfaces only as the generic `PHASE_4_VACUOUS_NO_CUSTOMERS` (customers = 0). The root cause — an Error-tier customer import whose `DefaultPriceCode` values don't match any price level — has no dedicated flag. A `CUSTOMER_IMPORT_PRICE_CODE_MISMATCH` flag (Error-tier customer block + the offending codes) would catch this directly instead of relying on the reader to dig into the import log. The same gap would hide any Error-tier customer import behind a bare "0 customers."
5. **`IMPORT_VS_HELPSCOUT_DRIFT` still false-positives on first-pass review.** Even after the v3.2 regex tightening, tcs's collaborative import-review notes ("missing a Dealer Net", "where you are seeing product SKUs with no Dealer Net") trip it, while the client explicitly says "Nothing that changes the shape of what you built." The flag fires against a warning-only (treated as "clean") products import. Consider excluding cases where the most-recent product import is warning-only AND the client thread also contains review/collaboration language, or down-rank to informational when the same thread contains reassurance language.
