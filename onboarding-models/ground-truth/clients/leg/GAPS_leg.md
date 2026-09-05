# GAPS — Legrand US (`leg`, org id 273)

Companion to `JOURNEY_leg.md`. Built 2026-08-27 from `CORPUS_leg.md`, `RAWSTATE_leg.json`, `supercat-postgres-vpn`, and BigQuery (`hubspot`, `helpscout`, `Fathom`, `quickbooks`).

**Forbidden files:** none opened. No `.md` under `eCat_Onboarding/leg/`, nothing under `SuperCat_Simple_Final/02_Implementation/Legrand/`, no `REGISTRY.yaml`, no `onboarding-models/` framework document, no `SCORECARD.md`, no other client's `JOURNEY_*.md`, no `ecat-*` skill. I also stayed out of the BigQuery datasets `onboarding_assessment` and `scorecard`, which appear to hold the framework being graded.

**Corpus reading:** read start to finish, all 2,051 lines. Nothing skimmed. Specifically read in full: all five call transcripts (2025-11-07 ~40 min, 2025-12-12 ~54 min, 2026-01-12 ~23 min, 2026-07-14 ~43 min, 2026-08-07 ~22 min) and all 28 HelpScout message blocks across 9 threads, including Tracy's 2026-08-18 library specification in its entirety and the boilerplate French/English confidentiality footers.

**Org identity:** kept separate throughout. Org 273 = `leg` = "Legrand US", created 2025-06-10, status `onboarding`. Org 93 = `lna` = "legrand", created 2015-06-25, status `inactive`, 101 products, 3 orders. Every query in the journey was filtered on `organization_id = 273` or `id IN (273, 93)` with the results labelled. Org 93 was touched only to confirm separation and to check for cross-contamination.

---

## 1. What I could not determine, and what would settle it

### 1.1 The identity of the third destroyed account (2026-06-18)

Three `OrgUser destroyd` events fired at 2026-06-18 19:13:42, :47 and :53. Two are recoverable from `login_events`: **Chuck Wiebe** (`chuck+u@supercatsolutions.com`, 5 logins 2025-06-13 → 2025-06-19) and **Steve Thrasher** (`steve@supercatsolutions.com`, 35 logins over 4 days). The third never logged in, so it leaves no trace anywhere.

**Why it can't be resolved:** the audit payload is `{"id":144053,"organization":"leg"}` on all three rows — `144053` is Jon Vanderberg, the *actor*, not the destroyed row. `parent_id` is also 144053. The event records who did it, not what was done. The `org_users` row is gone and `users` rows are org-agnostic.

**What would settle it:** a Rails-side log or DB backup from before 2026-06-18, or `org_users` id-sequence forensics if ids were dense (they are not — 144051, 144053, 144117 with a gap at 144052 and 144054–144116, most of which belong to other orgs).

**Is it important?** Low. It was almost certainly a fourth SuperCat internal account from the demo build. It matters only as a demonstration that `OrgUser destroyd` is not self-describing.

### 1.2 The mechanism that soft-deleted 381 products on 2026-07-13

381 `products` rows carry `deleted = true` and `last_modified_at` 2026-07-13 23:15:14. **There is no Products import event on 2026-07-13** — only 13 clean Images imports, the last at 23:15:14.315 (44 ms later), whose entire body is `'The following images were imported: RWP263BK.jpg'`. An image import does not delete products.

Nor does the timestamp fit the next Products import (2026-07-14 15:14:37, warning tier), which under the omitted-record rule *would* have soft-deleted omitted rows — but those rows would then carry `last_modified_at` 2026-07-14, and no row in this org does.

**Related unreconciled arithmetic:** 1,538 total product rows = 1,020 active + 137 deleted (2025-06-18) + 381 deleted (2026-07-13). That leaves 1,020 active immediately after 2026-07-13, yet Kylor told the client on 2026-07-14 > "It's 908 products." 908 is also exactly today's `products_with_story` count, so the July-14 cohort is real and identifiable — but the two numbers cannot both be the active count on the same day.

**What would settle it:** the Rails importer's own job log for 2026-07-13, or a `delayed_jobs`/`delayed_job_reports` row for that window (both tables exist; I did not find leg-scoped rows, and they are pruned). Failing that, the FTP transfer log.

**Effect is certain even though the mechanism is not:** the web-scraped demo catalog was retired on/around 2026-07-13 and replaced with Legrand's own data.

### 1.3 When Trey Wilson was promoted to admin

`audit_log_entries` 2026-06-19 10:58:37 records his creation with `"is_admin":false`. He is `is_admin = true` today. The only `OrgUser updated` rows for 157198 are 2026-06-19 11:01:14 (payload `{"id":157198,"organization":"leg","is_admin":false,"disabled":null}`) and 2026-08-17 19:17:11 (payload `{"id":157198,"organization":"leg","territory_codes":[]}`).

The payloads appear to record *prior* values, not new ones — which is how the user-group rename history reconstructs cleanly. On that reading the promotion happened at 2026-06-19 11:01:14. On the opposite reading it happened at some unlogged later point.

**What would settle it:** confirmation of whether `audit_log_entries.data` stores pre- or post-change state. That is a two-minute look at the audit concern in `supercat_server` — which I did not do, because it is source code rather than client evidence and was not in scope for this pass.

**Consequence:** Trey is counted as an admin in every current-state figure, which is why `RAWSTATE` shows 5 admin / 5 non-admin. For most of the onboarding he was a non-admin user.

### 1.4 Whether the eCat Online storefront is actually reachable

`mobile_sites` row 141 exists for org 273 (created 2025-06-13 12:42:16, `url_key` = `'1'`) with `enable_online_catalog = true`, `allows_unauthenticated_users = true`, `self_service_enrollment_enabled = true`, `hide_products_marked_hideable = false`, `display_quantity_available = true`.

I did not test whether that resolves to a live public URL, and I make no claim that it does. Routing, DNS, a reverse-proxy allowlist or the absence of a `custom_cname` (it is NULL) could all make it inert.

**What would settle it:** an HTTP request to the eOL host for `url_key` 1, or the eOL routing config. Also: `analytics` / `google_analytics_ecat_online` in BigQuery would show whether anyone has ever loaded it.

**Why it matters:** on 2026-01-12 Brent asked > "I think you guys are just looking at eCat, not eCat Online.    Is that correct?" and Justin answered > "Correct." — while telling his own cybersecurity reviewer the asset was > "Not publicly, but, yes, our servers are on the Internet." If the row is live, an unauthenticated storefront exposing all 1,020 products (including the 710 hidden variants and 3 visible $0.00 SKUs) sits outside the scope that Legrand governance signed off. If it is inert, this is dead demo residue. I could not tell which.

### 1.5 Whether Kylor's 2026-08-18 and 2026-08-27 messages were ever sent

Both carry HelpScout `state: draft` in `helpscout.conversation_threads`:
- 2026-08-18 16:05:56 — > "Team,Quick follow-up to yesterday's note. The rest of the import work finished today…"
- 2026-08-27 16:27:28 — > "100% - I'm just doing some final validation before I push the new import…"

Every other thread in the set is `state: published`. Circumstantially the 08-18 note may not have landed: Tracy's 17:57:45 reply that day does not reference it, and Trey's 18:22:08 question > "I am not super clear on the inventory issue.    Can you elaborate on this and the pricing issue (s)?" is answered *in* that note. But `state` on a `type: message` thread may mean something other than "unsent" in this export, and the corpus generator treated the 08-18 draft as a normal message.

**What would settle it:** the HelpScout UI for conversations 15151, or the `email_event` table cross-referenced to Trey's address.

**Why it matters:** it changes the read on the nine-day stall. If the notes went out, the client has been told about the inventory and pricing blockers and is waiting. If they did not, the client's last substantive information is from 2026-08-17 and Trey's 2026-08-27 question is unanswered.

### 1.6 "Sonia"

[HS #14840, 2026-07-24T22:52:28, kylor@supercatsolutions.com] > "Admin access — I just sent Sonia an eCat invite so she can get on the iPad and start testing"

**Sonia does not exist in org 273.** Not in `org_users` (10 rows, all accounted for), not in `organization_invitations` (4 rows, all Greg/Justin, none created between 2026-07-08 and 2026-07-30), not in `audit_log_entries`, and not in `users` for any `%legrand%` email. A global `users` search on `first_name ILIKE 'sonia%'` returns 27 people, none at Legrand and none in org 273. A global `organization_invitations` search for 2026-07-23 → 2026-07-26 returns one row, for org 83 (`cfg`), a different person.

**Three readings, none testable from here:** (a) the invite was never actually sent; (b) it was sent to the wrong org; (c) "Sonia" is a mis-transcription of a name Kylor got wrong, and no such Legrand employee exists. Note that no Legrand participant ever queries it, in any later message or call.

**What would settle it:** Kylor's sent mail, or the eCat admin invite log for 2026-07-24.

### 1.7 Everything about the first year of client relationship

The `hubspot.deal` record shows an Electrical Distributor deal created **2025-05-07** (id 38692696705, Discovery, $23,700 → $181,200 → $158,700, Closed lost 2025-07-16, later edited to $15,000) and a Showroom deal created 2025-06-20. Kjael said on 2025-12-12 > "Yeah, I've talked to you guys a few times in the last six months" and Jon said > "I've worked with your brand before.    I've known you guys for quite a while."

**None of that relationship is documented in any source I can read.** See §4.

### 1.8 What the 22 agency user groups are supposed to see

Each of the 22 groups has `collections_auth = 'a'`, `custom_fields_auth = 'a'`, `price_levels_auth = 'a'`, `shared_resources_auth = 'a'`, `ipad_reports_auth = 'a'`, `custom_field_filters = '[]'`, `territory_url = NULL`, `base_price_level_id = NULL`, `default_price_level_id = NULL`, and an all-NULL `ipad_custom_views`. They are unconfigured shells with one library link attached each.

Whether that is intentional (inherit everything from the org, differ only by Design Studio URL and eventually territory) or unfinished cannot be determined from the record. Kylor's 2026-08-06 description — > "22 agency-specific user groups are set up, each with their own Library linkto the personalized design studio URL for that agency. Each rep logs in andsees only their URL, no one else's." — is **correct on the point it makes**: I verified each of the 22 `shared_resources` rows (ids 38027–38048) has exactly one row in `shared_resources_user_types`, matching its own group. But no group has a price level, a territory, or a rep.

**What would settle it:** the agency→territory mapping Kylor asked Legrand for on 2026-08-07 and has not received.

### 1.9 Whether the `®` removal was deliberate

`long_description LIKE '%®%'` returns **0 of 1,020**, and `long_description ~ '[^\x20-\x7E®]'` also returns 0 — so the junk character was cleaned and the trademark mark went with it. Kylor committed to > "I'll clean that up and keep the ®" and Trey said > "I would leave the R just because it's there on purpose." The demo data had it (the deleted 2025-12-12 test order recorded `"radiant® Two Gang Screwless Wall Plate, Nickel"`).

I cannot tell whether the ® was stripped deliberately (because brand now lives in `trade_name`, which reads `adorne` / `radiant` cleanly) or lost as collateral damage in the character cleanup. Nobody has raised it since 2026-07-15.

**What would settle it:** the source `products.csv` Kylor built, or asking him.

### 1.10 Whether anything happened on the 2026-07-24 working session beyond what Kylor wrote

[HS #14840, 2026-07-24T22:52:28, kylor@supercatsolutions.com] > "I didn't realize until afterward that my AI recorder didn't join the call. If we covered anything that isn't captured below, please flag it and I'll add it to the list."

Confirmed independently: `Fathom.ai-summaries` has no row for 2026-07-24. This was the session where taxonomy structure, agency personalisation and alternate hero images were discussed — three of the largest design decisions in the project — and the only record is Kylor's own recap. Nobody flagged an omission, which is weak confirmation at best.

---

## 2. Tier-B tickets: what I used and what I discarded

Four tier-B threads (internal SuperCat threads mentioning the client). **I judged all four relevant and discarded none.** Reasoning per thread:

| Ticket | Date range | Judgment | Why |
|---|---|---|---|
| **#14821** "Re: Adorne + Radiant Inventory" (2 msgs) | 2026-07-21 | **Load-bearing.** Cited in the journey. | Brent's message stands up the inbound feed address (`leg@inbound.supercatsolutions.com`) — the direct cause of every 06:01 import from 2026-08-05 onward. Trey's reply is the *only* place in the entire corpus that says the feed is two files, one per brand: > "there will be one file for adorne and one radiant." Without that line, finding G (the two files overwriting each other) is not attributable. Tier B only because Brent's address is the customer of record on the thread. |
| **#14961** "Re: Quick Check-In" (1 msg, 9,394 chars) | 2026-08-06 | **Load-bearing.** Cited extensively. | Tier B only because Kylor is both sender and primary customer on the row. It contains the hero-variant strategy (> "310 hero products visible, 710 variant productsaccessible but not front-and-center"), the 22 agency groups, the personal-SharePoint flag, and the three customer-file questions. It also nests Alexandra's > "We are in, thank you!" (2026-08-06 12:19) and Trey's > "I added the Agency Customer address folder which contains all customer’saddresses by sales agency." — the only evidence of the agency address hand-off. |
| **#14974** "Recap for today" (1 msg) | 2026-08-07 | **Load-bearing.** Cited for the phase-6 finding. | The only place the full sequencing is stated: > "Next week: … then your go / no-go on beta." / > "Following week: beta testers, internal super users first." / > "After beta: admin training with our support lead". Also the DN-as-default decision and the logo specs. |
| **#15151** "Re: Quick Update" (8 msgs) | 2026-08-17 → 2026-08-27 | **The most important thread in the corpus.** | Contains the library rebuild, the DealerNet finding, the inventory finding, the Wiremold/P&S scope question, Tracy's full IA spec, Trey's DN answer, and Trey's 2026-08-27 beta request. Everything in §C of the journey rests on it. |

**Tier C:** the manifest reports 0 tier-C tickets. Confirmed independently — a `helpscout.conversation_threads` search on `body LIKE '%legrand%' OR '%adorne%'` returns threads whose customers are only `@legrand.com` and `@supercatsolutions.com` addresses. No third party discusses this client.

**What I did discard:** nothing at thread level. At message level I ignored the repeated French/English confidentiality footers, the signature blocks (except where the department line changes — see §3.3), and roughly four minutes of the 2025-11-07 call about showroom drywall, TV frames and lighting history, and the closing minutes of the 2026-07-14 call about Kylor's recent marriage. The 2025-11-07 small talk is not entirely noise — Trey's account of building data files for Lights of America and Ferguson (> "I just built Lights Americas from scratch.    They sent me a template and I just started from scratch") is why Kylor could say on 2026-07-14 > "you guys have one of the more clean data files that I've seen". I kept that.

---

## 3. Contradictions between sources

### 3.1 Import log vs. inventory table — "record ignored" records that were not ignored

Every 06:01 adorne import logs exactly ten warnings of the form > `'Line 39: Product not found, record ignored., BaseItemCode=ADPD453LM2'`. All ten of those `base_item_code` values are present in `inventories` today with quantities (`ARUSBM4` = 1,407; `ARPTR151GW2WP` = 158; `ARTR152W4WP` = 159; …), and none of the ten matches any `products` row in org 273 — not even a soft-deleted one.

The message says the record was ignored. The table says it was inserted. One of the two is wrong. Either way the observable outcome is 10 orphan inventory rows.

### 3.2 Client was told six price levels; five exist

[HS #14783, 2026-07-14T23:12:59, kylor@supercatsolutions.com] > "On pricing; six levels are live: US Net, US Retail/MSRP, US iMAP, Canada Net, Canada iMAP, Canada MSRP."

`price_levels` for org 273 = 5 (`retail`, `imap`, `canet`, `caimap`, `camsrp`), all created 2026-07-13 22:20:31 → 22:22:23. "US Net" is `products.net_price`, not a price level. Self-corrected 2026-08-17 (> "What's loaded is US Retail (MSRP), US iMAP, Canada Net, Canada iMAP and Canada MSRP") — but the client was told six for 34 days, and the count difference is exactly the level that later became the DealerNet problem.

### 3.3 Two email domains and two department names for the same person

Trey Wilson's HelpScout header address is `trey.wilson@legrand.com`; his own signature block reads `Trey.Wilson@legrand.com <trey.wilson@legrand.us>` on 2026-07-08 and `trey.wilson@legrand.us` from 2026-07-15 onward. His department line reads `ELECTRICAL WIRING SYSTEMS` through 2026-08-18 18:32:04 and `ELECTRICAL INFRASTRUCTURE` on 2026-08-21 13:06:31 and 2026-08-27 16:07:06. `org_users`/`users` hold only `@legrand.com`.

Not a data problem — an organisational rename mid-project, worth knowing because it postdates every document in the library.

### 3.4 Tracy's last-login timestamp differs between two DB sources

`org_users.last_ipad_login_at` for 157530 = 2026-08-20 14:26:01. Her latest `login_events` row = 2026-08-19 15:17:47. A ~23-hour discrepancy. Likely `last_ipad_login_at` is also touched by a sync that does not write a login event, but I did not verify that. Nobody else in the org shows the mismatch — Alexandra's and Trey's agree to the microsecond.

### 3.5 Client statements vs. current configuration, still open

| Stated | Where | DB today |
|---|---|---|
| "keep the ®" | Kylor, 2026-07-14 23:12 | 0 of 1,020 `long_description` contain `®` |
| "All 36 categories are now assigned to their correct groups: Dimmers, Switches & Outlets, Sensors & Timers, Plates/Boxes/Blanks, and Smart Technology" | Kylor, 2026-07-23 22:50 | 14 categories exist; **13 sit under `Group` `GRP2` "Default Group"**, 4 under `SWT` "Switches & Outlets". `DIM`, `ST`, `GRP1`, `WPB` have no categories. The browse hierarchy was rebuilt 2026-08-17/18 as TradeName → Collection → Category, so the Group layer may simply be unused — but the 2026-07-23 statement no longer describes the org. |
| "DN as the default price shown first" | Kylor, 2026-08-07 18:02 | No DealerNet level exists; 981 customers default to `imap`, 152 to `caimap` |
| "we list all the Product Types in Collections under adorne and radiant" | Tracy, 2026-08-18 18:28, agreed by Trey 18:32 | `product_type` is NULL (526) or `''` (494) on all 1,020 products |
| "Enable Finish and # of Gangs as active iPad filters" | Kylor, 2026-07-23 22:50 | `Finish` = 1,001 of 1,020 populated (fine). **`numberofgangs` = 0 populated.** |
| "Territory codes are set for all six of you" | Kylor, 2026-08-17 22:58 | True — and all six hold the **identical** 24 codes, covering all 1,133 customers. No per-person scoping exists. |
| "each with their own Library link … Each rep logs in and sees only their URL" | Kylor, 2026-08-06 22:41 | **Verified correct.** All 22 links are scoped 1:1 via `shared_resources_user_types`. (I initially suspected `shared_resources_auth = 'a'` broke this; the join table governs and it does not.) |

### 3.6 A message in HelpScout that the corpus does not contain

`helpscout.conversation_threads` holds a 29th Legrand-related thread — 2026-08-27 16:27:28, `state: draft`, from `kylor@supercatsolutions.com`, quoted in §C and §E-F of the journey. The corpus was generated 2026-08-27 18:22:59, nearly two hours later, and its last entry is Trey's 16:07:06 message. The corpus does include the 2026-08-18 16:05:56 draft, so drafts are not categorically excluded.

Either the corpus builder's HelpScout snapshot predates 18:22, or drafts are captured inconsistently. Minor for this client, potentially systematic for the framework.

(Separately: my BigQuery filter on `body LIKE '%legrand%'` caught 28 of the 29 threads. The one it missed is Brent's 2026-07-21 19:16:38 message, whose body mentions neither "legrand" nor "adorne" — only the inbound address `leg@inbound.supercatsolutions.com`. It is in the corpus. Noting it because the same filter shape is presumably what built the corpus, and it is one character-class away from dropping a load-bearing message.)

### 3.7 Duplicate-ticket check: negative

Collapsed on subject with `Re:` / `RE:` / `Fwd:` / `FW:` stripped, the 28 message blocks reduce to **9 distinct conversations**, one per ticket number — no conversation is captured twice under different numbers. `helpscout.conversations` confirms the thread counts per number (14747: 1 + 1 note, 14752: 3, 14783: 3, 14821: 2, 14833: 5, 14840: 3, 14961: 1, 14974: 1, 15151: 8).

The volume-inflation risk here is different and worth naming: **content duplication inside threads**. Trey's 2026-07-24 13:26:09 reply reproduces Kylor's entire 2026-07-23 22:50:27 progress update verbatim with inline answers (4,996 chars, mostly quoted text). #14961's single message nests four earlier emails. #14833 and #14840 both cover the 2026-07-24 working session. A naive character count over-weights 2026-07-23/24 by roughly 2×. My reading is de-duplicated: I treated Trey's quoted block as answers only.

Fathom has the mirror-image issue and the corpus handled it correctly: `Fathom.ai-summaries` holds **7** rows for this client because 2025-11-07 and 2025-12-12 are each stored twice (ids 69516524/69516526 and 76418264/76418265 — "2 recordings merged" in the corpus header). Five real calls. No hidden sixth call exists.

---

## 4. Corpus holes — where the DB shows activity and the corpus shows nothing

This is the critical section for this client. **Roughly the first thirteen months of this org's life have no readable narrative record at all.** Named by stretch:

### Hole 1 · 2025-05-07 → 2025-11-06 (183 days): the entire pre-sales relationship and the whole demo build

**DB and BigQuery show:**
- `hubspot.deal` 38692696705 "Legrand - Electrical Distributor eCat" created 2025-05-07 22:24:50, moved Discovery → Demo → Discovery → Demo → Discovery between 2025-05-13 17:19 and 2025-05-16 17:38, amount swinging $23,700 → $181,200 → $188,700 → $158,700, **Closed lost 2025-07-16 13:43:36**.
- Org 273 created 2025-06-10 19:05:20. Three SuperCat accounts created 2025-06-10/12.
- **69 import events between 2025-06-12 19:27:53 and 2025-06-19 14:00:23** — Products ×14 error / ×2 warning, Images ×34 warning + ×3 clean + ×3 error, Product Stories ×3 warning + ×2 clean, Options, Option Groups, Customers ×3 error + ×1 clean.
- 178 iPad logins in June 2025 across 5 users, 9 distinct days. `swt` alone: 35 logins over 4 days.
- 6 `ipad_reports`, 5 `notices`, 7 `shared_resources`, 16 `custom_fields`, 29 `options`, 11 `option_groups`, 1 `mobile_sites` row — all created in this window.
- 137 products soft-deleted 2025-06-18.
- `hubspot.deal` 39221664105 "Legrand - Showroom TIER 1" created 2025-06-20 15:47, Discovery 2025-06-23 18:52:55, Demo → Assist → Propose in 7 seconds at 19:46:15–22, $31,200.
- One Products import 2025-09-06 12:30:20 with 964 warnings.

**Corpus shows:** nothing. Not one line. HelpScout's earliest Legrand thread is 2026-07-08 and Fathom's earliest call is 2025-11-07.

**Not a retention artefact.** `helpscout.conversations` goes back to 2020-01-29 and holds 5,639 conversations; there are simply no Legrand rows before 2026-07-08. Pre-onboarding communication ran through Jon's direct mailbox, outside HelpScout — proven by the fact that his 2026-06-22 credentials email survives only as quoted text *inside* HS #14747, and is not itself a HelpScout thread.

**Also blind here:** `audit_log_entries` retains only from **2025-08-27** (global min). Every configuration action in the June 2025 demo build is unrecoverable. The `IpadReport updated` payloads of 2025-12-12 preserve prior `updated_at` values of `2025-06-16T23:16:44`, `2025-06-16T23:23:00` and `2025-06-19T12:44:48`, which is the only surviving trace that those reports were edited in June 2025.

**What would fill it:** Jon's mailbox for 2025-05 → 2025-11, and Fathom recordings from before 2025-11-07 (Kjael: > "I've talked to you guys a few times in the last six months", 2025-12-12 — those calls are not in Fathom).

### Hole 2 · 2025-09-07 → 2025-11-06 (60 days) and 2025-11-08 → 2025-12-11 (33 days): the sale in motion

**BigQuery shows** `closedate` revisions on 2025-10-13 18:17:49 (→ 2025-12-31), 2025-11-10 20:59:59 (→ 2025-11-21) and 2025-11-24 20:56:27 (→ 2025-12-12), plus the amount cut from $31,200 to $25,200 at 2025-11-07 15:52:29 and the stage move to **Commit** at 15:52:39. `login_events` shows `jonv` in the org in September, October and November (2 logins each month).

**Corpus shows** only the 2025-11-07 call. The three close-date revisions and the Commit move have no narrative behind them beyond that one conversation, and the two months either side are empty.

### Hole 3 · 2025-12-13 → 2026-01-11 (29 days) and 2026-01-13 → 2026-07-07 (176 days): the governance wait

**The single largest documentary hole in the live period.** 176 days with one data point.

**DB and BigQuery show:**
- `closedate` revised 2025-12-15, 2025-12-16, 2025-12-30, 2026-01-22, 2026-02-24, 2026-03-20 (twice, 19 ms apart), 2026-04-14, 2026-06-02 — **eight revisions with no accompanying record of any kind**.
- Amount cut $25,200 → **$24,108** on 2026-04-28 17:18:33. Nobody explains why.
- `login_events`: 2026-02 = 1, 2026-03 = 1, 2026-04 = 0, 2026-05 = 2 — all `jonv`, keeping the demo warm.
- Deal **Closed won 2026-06-11 13:59:44**. Invoice `WDQN3KNL-0001` raised 2026-06-15 for $24,670, balance 0.
- `Organization updated {"id":273,"stats_enabled":true}` at 2026-07-01 19:18:54, by a SuperCat user who is neither Jon nor Kylor.

**Corpus shows:** the 2026-01-12 security review, and then silence until 2026-07-08. The single most commercially important event in this client's history — contract signature — has **no** entry in the corpus at all. It is knowable only from HubSpot and QuickBooks.

**What would fill it:** the executed agreement and its date, the legal-review thread Justin described (> "Yeah, know Greg and I will be working with legal on the contract"), the third-party cybersecurity questionnaire Clinton said he would send, and whatever communication accompanied the April price reduction.

### Hole 4 · 2026-06-12 → 2026-07-07 (26 days): the restart itself

**This is the most consequential hole, because the events are fully reconstructable from the DB and completely absent from the narrative.**

**DB shows** (all in `JOURNEY_leg.md` §F): the 2026-06-18 customers import, three account destroys, the user-group rewrite and rename, the 2026-06-19 test-order deletion, three client accounts created, Tracy's account destroyed and recreated 2026-06-22, first client logins 2026-06-22/23, 7 library items added 2026-06-22.

**Corpus shows** one artefact: Jon's 2026-06-22 credentials email, surviving only because Trey quoted it back on 2026-07-08 —
> "From: Jon Vanderberg <jon@supercatsolutions.com>Sent: Monday, June 22, 2026 12:12 PMTo: Trey Wilson …Subject: eCat loginHello Trey, Alex and Tracy,I look forward to seeing you in person this week and working together.I wanted to confirm that you received the email invitation to log in toeCat for review."

Note > "I look forward to seeing you in person this week" — there was an **in-person meeting in the week of 2026-06-22** with no record anywhere. Not in Fathom, not in HelpScout, not in HubSpot engagements.

**Nobody wrote down that this project restarted.** There is no kickoff note, no internal handoff, no statement of the reset. Trey's first HelpScout message, sixteen days later, is a client wondering what is happening: > "I wanted to check in and see when your team will have the content organizedin the app."

### Hole 5 · 2026-07-25 → 2026-08-05 (12 days) and 2026-08-08 → 2026-08-16 (9 days): mid-project working weeks

**DB shows** no imports 2026-07-25 → 2026-08-04, then the automated feed starting 2026-08-05 06:00:41; `login_events` show Trey, Alexandra and Tracy active throughout; 22 user groups and 22 library links created 2026-08-06 18:40–18:41; four clean Products imports on 2026-08-06 (19:15, 20:10, 21:41, 22:01); an Images **error** at 2026-08-06 17:54:36 (`CorruptImageProfile` on two files, plus non-sRGB warnings on `3894.jpg` and `AFGF152TRW-P.jpg`).

**Corpus shows** for 2026-07-25 → 2026-08-05: two scheduling emails (Tracy 2026-07-29, Kylor 2026-07-30) and nothing else. A Monday 2026-08-03 call was proposed (> "Does Monday at 3 pm ET work?") and there is **no record of whether it happened** — no Fathom row, no follow-up email. For 2026-08-08 → 2026-08-16: nothing at all, across a week in which the client logged in six times.

The 2026-08-06 Images error is never mentioned to anyone. It is the only `:error`-tier import in the entire 2026 project.

### Hole 6 · 2026-08-19 → 2026-08-27 (9 days): the stall

**DB shows** zero configuration writes; the feed running daily; `abriggs` logging in 2026-08-19, and again 2026-08-27 14:31:33.

**Corpus shows** two client messages (Trey 2026-08-21, Trey 2026-08-27) and no SuperCat response. The only SuperCat text in the window is the 2026-08-27 16:27:28 draft, **which is not in the corpus**.

**What would fill it:** Kylor's calendar and sent mail for 2026-08-19 → 2026-08-27. As it stands, the record cannot distinguish "was pulled onto another account" from "was working locally on the import he mentions in the draft" from "dropped it".

---

## 5. Things I checked that came back clean

Recording these so a reader does not re-run them.

- **No `:fatal` import token ever**, in any of 145 `import_events` rows for org 273 across 14 months.
- **No cross-org contamination, either direction.** No product, customer, taxonomy, library, user-group or option row in org 273 references org 93 or any other org, and none in org 93 references org 273. `XEVPED%` products exist only in org 273 (11 rows) — the `xevped2_3.jpg` string in the 2025-09-06 import warning is Legrand's own EV-charging line, not another client's data. The sole crossover in the estate is `steve@supercatsolutions.com` holding memberships in both `leg` and `lna`.
- **No dangling price codes.** All 1,133 `customers.default_price_code` values (`imap` ×981, `caimap` ×152) resolve to existing org-273 price levels. `customers_no_territory` = 0.
- **No dangling taxonomy parents.** Every non-null `taxonomies.taxonomy_id` in org 273 resolves to a row in org 273.
- **No orphan agency library links.** All 22 rows in `shared_resources_user_types` for the 2026-08-06 batch point at existing groups, 1:1.
- **The 5 empty library buttons are real and unchanged.** Directory ids 38130, 38137, 38141, 38143, 38146 have zero children; `shared_resources` max `updated_at` = 2026-08-18 15:39:59.
- **`orders` is genuinely empty** — `count(*) = 0`, so the nullable-`is_submitted` trap does not bite here. (One order existed 2025-12-12 → 2026-06-19; see journey §E-F.)
- **No `enrollment_applicants`, `portal_orders`, `portal_invoices`, `sales_data`, `smart_stacks`, `matrix_options`, `contract_prices`, `option_images`, `option_mappings`, `distribution_centers`, `territories`, `org_documents`, `onboarding_questionnaires`, `onboarding_file_uploads`, or `subscriptions`** rows for org 273.
- **Fathom is complete for this client**: 5 deduped calls, all transcribed, none missing. The 2026-07-24 session genuinely was not recorded.
- **HelpScout has no pre-2026-07-08 Legrand data**, and that is not retention (dataset starts 2020-01-29).
- **1,018 of 1,020 products have images**; the 2 without (`HMKITBK`, `1597TRBK`) are both `hideable = true`, so neither appears in the visible browse grid. The image gap is real but not rep-facing.
- **No `.jpg.jpg` double-extension problem** and no evidence of the wrong-image-on-right-product pattern seen on other clients: `image_exists` is computed and true on 1,018 rows, and the only image-tier defects in 14 months are colourspace warnings and two `CorruptImageProfile` errors on 2026-08-06.

---

## 6. One-line summary of residual risk

The highest-value fact in this client is not in the corpus, is not in `RAWSTATE`, and required three separate sources to establish: **the onboarding is seven weeks old, not fourteen months, because the first thirteen months are a pre-sales demo (org 273, June 2025) plus a procurement wait that ended when HubSpot deal 39221664105 closed won on 2026-06-11 and QuickBooks invoice `WDQN3KNL-0001` was paid.** Any assessment built only on `import_history` will read a 285-day regression that never happened, and will miss the nine-day stall that is the actual problem.
