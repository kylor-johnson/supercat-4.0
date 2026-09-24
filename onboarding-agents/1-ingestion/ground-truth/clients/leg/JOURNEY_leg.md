# JOURNEY — Legrand US (`leg`, org id 273)

**Built:** 2026-08-27 · **Sources:** `CORPUS_leg.md`, `RAWSTATE_leg.json`, `supercat-postgres-vpn` (read-only SQL), `bigquery-admin` (hubspot, helpscout, Fathom, quickbooks).
**Forbidden files:** none opened. I did not read any `.md` under `eCat_Onboarding/leg/`, anything under `SuperCat_Simple_Final/02_Implementation/Legrand/`, `REGISTRY.yaml`, any `onboarding-models/` framework document, `SCORECARD.md`, any other client's `JOURNEY_*.md`, or any `ecat-*` skill. I also avoided the BigQuery datasets `onboarding_assessment` and `scorecard` on the same reasoning.
**Identity:** every DB fact below is org **273** / `leg` / "Legrand US" (created 2025-06-10). Org **93** / `lna` / "legrand" (created 2015-06-25, inactive, 101 products, 3 orders) is a different company record and was queried only to confirm separation. The one point of contact between them: SuperCat staff account `steve@supercatsolutions.com` holds memberships in both. No products, users, customers, library items or taxonomy rows cross between them.

---

## Narrative

Legrand US is not a fourteen-month onboarding. It is a **two-month onboarding wearing a fourteen-month costume**, and almost everything odd about this org comes from that.

In June 2025, before any contract existed, Jon Vanderberg stood up org 273 and — with Kjael Skaalerud, Brent Sanders, Chuck Wiebe and Steve Thrasher — built a complete speculative demo from a public web scrape of legrand.us. Nine days of work: 69 import events, 137 products retired and re-imported, options, option groups, stories, images, a customer file, six iPad report formats, five notices written in the voice of a Legrand sales manager at Dallas market. No Legrand employee had an account. Kjael said so out loud six months later: *"we pulled this together via kind of public web scrape of your website long ago when we were first pulling in, putting together a demo for the broader team."*

Then the sale took a year. The showroom deal was created 2025-06-23 and its close date slipped **eleven times** — 2025-07-31 → 2025-08-11 → 2025-10-01 → 2025-12-31 → 2025-11-21 → 2025-12-12 → 2025-12-19 → 2025-12-31 → 2026-01-30 → 2026-02-27 → 2026-03-31 → 2026-04-30 → 2026-05-31 → 2026-06-30. On 2025-11-07 Trey Wilson asked to start manually rather than wait for an automated feed, and in the same breath said *"I don't want you to do anything else until that's a done deal."* On 2026-01-12 Justin Baillargeon told his own cybersecurity reviewer *"we haven't signed the contract or anything yet"* and named the real blocker: a Central-marketing governance approval sitting with David Morris. That is the 285-day import gap. Nothing broke. Nothing went backwards. A pre-sales asset sat untouched while a French multinational's procurement process ran.

The deal closed won **2026-06-11 13:59:44 UTC** at $24,108; Legrand North America was invoiced $24,670 on 2026-06-15 and the balance is zero. Seven days after signature, on 2026-06-18, Jon dismantled the demo: he deleted the December test order, destroyed three internal SuperCat accounts, and renamed the user group off `DefaultUserGroup`. The next morning he created the first three Legrand accounts. The real project starts there.

Kylor Johnson took it over 2026-07-08, threw away the scraped catalog on 2026-07-13 (381 SKUs retired, five price levels and nineteen custom fields built the same night), and ran the kickoff on 2026-07-14. Six weeks of genuinely fast work followed: 908 real products becoming 1,020; images from 613 files uploaded in a morning; a hero-variant strategy that hides 710 colour variants behind 310 visible heroes; a library that went 7 → 24 → 88 → 108 → 129 items across 24 buttons; 22 per-agency user groups each with its own Design Studio link, correctly scoped one-to-one; a customer file of 1,133 accounts; territory codes for all six internal users; and a daily inventory feed by email that has run every morning since 2026-08-05.

And then, on **2026-08-18 15:58**, all configuration work stopped. Nothing in this org has been changed since — not a product, not a library item, not a price level, not a user group. In the nine days after that, Tracy Miller sent a 100-line library re-organisation spec, Trey answered the one question blocking pricing, and Trey asked for a CEU file swap. None of it has been actioned. On 2026-08-27 Trey wrote: *"Prior to tomorrow's call, I wanted to make sure we can let our sales agents that we selected to begin testing the app by the end of next week."* Kylor's reply is still sitting in HelpScout as an unsent draft.

Meanwhile the parts that *look* finished are not. The daily inventory feed sends quantity-on-hand, and the iPad displays quantity-available — so availability is blank on all 439 rows. Two brand files (adorne and radiant) arrive as separate emails, each import full-replaces the whole inventory table, and only one of the two lands on 17 of the last 23 days — this morning it was adorne, so **there is currently zero radiant inventory in the app**. The agreed default price level, DealerNet, does not exist. Three visible SKUs carry $0.00. Thirteen custom fields are registered, sent to the iPad and wired as filters with zero values behind them. Five notices from June 2025 still push to every user, including *"Thanks team for the awesome first day at Dallas market."*

No rep has ever seen this app. All ten accounts are Legrand employees or SuperCat staff. Twenty-two agency user groups are empty. Zero orders, ever, in the live table — though one existed for six months and was deleted.

---

## A. Cast

### SuperCat Solutions

| Person | Email / account | Role | First appearance | Last appearance | Notes / role changes |
|---|---|---|---|---|---|
| **Jon Vanderberg** | `jon@supercatsolutions.com` · `jonv` · org_user **144053**, admin | Director of Sales; owner of the account pre-sale; built the demo; provisioned the first client users | org_user 2025-06-10 19:54:40; first iPad login 2025-06-10 20:22:20 | last iPad login 2026-07-15 14:27:22; last login_event 2026-06-18 17:43 (`DefaultUserGroup`) → 2026-07-14 18:31 (`Lighting Showrooms`) | 159 logins over 22 days. Ran the 2025-11-07 and 2025-12-12 calls. Performed the 2026-06-18/19 reset (3 account destroys, order deletion, user-group rename, 3 client accounts created). Handed off 2026-07-08 with the note *"Kylor,They are ready to go."* Named again 2026-08-07 and 2026-08-27 as the intended rep trainer. **Role: seller → implementer → provisioner → trainer-in-waiting.** |
| **Kjael Skaalerud** | `kjael@supercatsolutions.com` · `kjael` · org_user **144117**, admin | CEO | org_user 2025-06-12 17:23:59; first login 2025-06-13 01:40:00 | last login 2025-06-19 13:54:59; last spoken appearance 2025-12-12 call | 8 logins, 3 days. Disclosed the web scrape on the 2025-12-12 call. Rendered "Cale"/"Hale"/"Carol" by the transcriber. Absent from the entire 2026 onboarding. |
| **Brent Sanders** | `brent@supercatsolutions.com` · `brentsanders` · org_user **144051**, admin | CTO | org_user 2025-06-10 19:06:19; first login 2025-06-17 18:10:07 | last login 2025-09-16 14:54:04; last written appearance HS #14821, 2026-07-21 19:16:38 | Fielded integration and security questions (2025-12-12, 2026-01-12). Stood up the inbound feed address `leg@inbound.supercatsolutions.com` on 2026-07-21. Created the `mobile_sites` row on 2025-06-13. |
| **Kylor Johnson** | `kylor@supercatsolutions.com` (mail) / `kylor22johnson@gmail.com` (login) · `Kylor_Johnson` · org_user **157982**, admin | Head of Customer Success; onboarding lead | org_user 2026-07-08 22:50:18; first email HS #14752, 2026-07-08 16:50:41; first login 2026-07-13 18:57:59 | last login 2026-08-07 16:09:50; last published message 2026-08-18 16:05:56; last draft 2026-08-27 16:27:28 | 18 logins, 5 days. Sole SuperCat actor from 2026-07-08 onward. Set `ui_preference: modern` 2026-07-14 18:55. Performed every 2026-07/08 configuration change in the audit log. |
| **Chuck Wiebe** | `chuck+u@supercatsolutions.com` · `chuck-user` | SuperCat internal test/support account | first login **2025-06-13 15:14:51** | last login **2025-06-19 14:19:58** | 5 logins, 3 days. **Appears nowhere in the corpus.** Org membership destroyed 2026-06-18. Recoverable only from `login_events`. |
| **Steve Thrasher** | `steve@supercatsolutions.com` · `swt` | SuperCat internal | first login **2025-06-13 15:44:09** | last login **2025-06-19 13:55:48** | **35 logins over 4 days — the heaviest single user in this org's history.** Appears nowhere in the corpus. Org membership destroyed 2026-06-18. Also a member of org 93 (`lna`) — the only account touching both Legrand orgs. |
| **"Emery"** | — | named alongside Jon as a candidate rep trainer | 2026-08-27 16:27 (HelpScout draft, not in corpus) | same | No account in org 273. |

### Legrand, North & Central America

| Person | Email / account | Role | First appearance | Last appearance | Notes / role changes |
|---|---|---|---|---|---|
| **Trey Wilson** | `trey.wilson@legrand.com` · `Treyw` · org_user **157198** | Senior Director of Showroom Sales — project owner and budget holder | call 2025-11-07 15:00; org_user 2026-06-19 10:58:37; first login 2026-06-22 18:02:26 | last login 2026-08-21 14:59:02; last message 2026-08-27 16:07:06 | 48 logins over 28 distinct days — the most active client user. **Created as `is_admin: false` (audit 2026-06-19 10:58:37), now `is_admin: true` — promoted at an undetermined date.** Signature block changes from "ELECTRICAL WIRING SYSTEMS" to "ELECTRICAL INFRASTRUCTURE" between 2026-08-18 and 2026-08-21 — a reorg, not a role change. Uses `trey.wilson@legrand.us` in his signature and `@legrand.com` in the header. |
| **Alexandra Briggs** | `Alexandra.Briggs@Legrand.com` · `abriggs` · org_user **157197** | Eastern Regional Manager, Showroom Sales | org_user **2026-06-19 10:54:32 — the first Legrand account ever created in this org**; first login 2026-06-23 15:30:24 | **last login 2026-08-27 14:31:33 — the most recent human activity in org 273** | 25 logins, 11 days. Created with `territory_codes: ["ERSM"]`, which matched no customer; corrected 2026-08-17. Drove the collection-first navigation requirement on the 2026-07-14 call. |
| **Tracy Miller** | `tracy.miller-01@legrand.com` · `millert` · org_user **157530** (originally **157199**) | Western Regional Manager, Showroom Sales | org_user 157199 created 2026-06-19 11:00:46; **destroyed 2026-06-22 17:17:38; recreated as 157530 at 17:19:22** (1m 44s later); first login 2026-06-23 15:03:24 | last login_event 2026-08-19 15:17:47 (`org_users.last_ipad_login_at` says 2026-08-20 14:26:01); last message 2026-08-18 18:28:48 | 12 logins, 9 days. Created with `territory_codes: ["SRCM"]`. **Author of the library information architecture** — the spec Kylor rebuilt against on 2026-08-17, and the 100-line follow-up list of 2026-08-18 that is still unactioned. Previously used eCat as a rep for other brands (per Trey, 2026-07-14). |
| **Kyle Smith** | `kyle.smith@legrand.com` · `k_smith` · org_user **158112** | Marketing | mentioned 2025-11-07; on 2025-12-12 call; org_user 2026-07-13 16:25:45; first login 2026-07-14 19:04:29 | last login 2026-08-07 16:09:07; last message HS #14783, 2026-07-15 19:42:17 | 5 logins, 4 days. Owns brand assets and logo delivery. The logo request of 2026-08-07 is still open. |
| **Justin Baillargeon** | `justin.baillargeon@legrand.com` · `JBaillargeon` · org_user **158893** | IT / business owner of record for Legrand governance | 2025-12-12 call | invitation redeemed 2026-08-07 17:35:57 | Named himself business owner, asset owner and project manager on the 2026-01-12 security review. Invited 2026-07-30 16:16:23 (expired unredeemed 2026-08-06), re-invited 2026-08-07 16:26:27, redeemed the same day. **Has never logged into the iPad.** |
| **Greg Kozniewski** | `greg.kozniewski@legrand.com` · `gkozni1a` · org_user **159033** | eCommerce / digital — pushed for the automated feed | mentioned 2025-11-07; on 2025-12-12 call | invitation redeemed 2026-08-12 20:49:00 | Invited 2026-07-30 16:16:22 (expired), re-invited 2026-08-07 16:26:27, redeemed 5 days later. **Has never logged into the iPad.** His personal SharePoint account is the target of library item 33218 "radiant® Video", still live and still behind a Microsoft login. |
| **Angela Coffman** | `angela.coffman@legrand.com` | VP/GM Marketing for the division; budget approver | 2025-12-12 call | 2025-12-12 call | The approval Trey needed. No account. |
| **Clinton Gatling** | `clinton.gatling@legrand.com` | IT / cybersecurity — ran the ASQ and LISP review | 2026-01-12 call | 2026-01-12 call | Stated Legrand has 26 showroom agencies. No account. |
| **Jaclyn Aulich** | `jaclyn.aulich@legrand.com` | Product data quality / MDM–PCM–STIBO | 2025-12-12 call | 2025-12-12 call | Raised the data-exposure risk of reusing the DDS feed. No account. |
| **Ryan Painter** | (no email captured) | Owner of the partner API and the existing daily Adorne/Radiant inventory feed | 2025-12-12 call | 2025-12-12 call | The 1 a.m. CST feed he described is the one now arriving at 06:01 UTC. No account. |
| **Daniel Dreissen** | `daniel.dreissen@legrand.com` | Argued for flat file first | 2025-12-12 call | 2025-12-12 call | No account. |
| **Richard Pugnier** | `richard.pugnier@legrand.com` | Marketing | 2025-12-12 call | 2025-12-12 call | No account. |
| **Karmen Muller** | `karmen.muller@legrand.com` | Product data | 2025-12-12 (invitee, silent) | same | No account. |
| **Jeffrey Beyel, Sean Welch, Lisa Frank** | `jeffrey.beyel@`, `sean.welch@`, `lisa.frank@legrand.com` | — | 2025-12-12 (invitees, silent) | same | No accounts. |
| **David Morris** | — | Central marketing governance approver | named 2026-01-12 | named 2026-01-12 | Never speaks or writes. The 285-day gap ends when this approval clears. |
| **"Sonia"** | — | claimed invitee | Kylor, 2026-07-24 22:52 | same | *"I just sent Sonia an eCat invite so she can get on the iPad and start testing"* — **no Sonia exists in `org_users`, `users` (any Legrand domain), or `organization_invitations` for org 273, and no invitation of any kind was created between 2026-07-08 and 2026-07-30.** Either the invite was never sent or it went to another org. Contradiction, unresolved. |

**Not in the cast:** any outside rep agency. 22 agency user groups exist (`Eastern Illuminations` … `Alberta LTD.`), created 2026-08-06 18:40:52–18:41:06 in a 14-second scripted burst. All 22 contain zero users. Clinton put the real agency count at 26.

---

## B. Phase transitions

> **Read this first.** This client crosses phases 1–4 **twice**, thirteen months apart, for two entirely different reasons. The 2025 pass was a SuperCat-internal pre-sales demo with no client participation; the 2026 pass is the onboarding. I give both, labelled. Everything from "Phase 1 (real)" onward is the onboarding.

### Phase 0 → Phase 1 (pre-sales demo) · 2025-06-10 · confidence: high

**What changed:** SuperCat created org 273 and began building a speculative Legrand catalog from a web scrape, with no contract and no Legrand participant.

**Evidence:**
- [DB] `organizations.created_at` = 2025-06-10 19:05:20 (org 273, `leg`, "Legrand US"). `user_types` id 2641 created 2025-06-10 19:05:20 as `DefaultUserGroup`.
- [DB] `org_users`: Brent Sanders 2025-06-10 19:06:19; Jon Vanderberg 2025-06-10 19:54:40; Kjael Skaalerud 2025-06-12 17:23:59. First iPad login `jonv` 2025-06-10 20:22:20. No Legrand-domain account exists until 2026-06-19.
- [Fathom, 2025-12-12T19:30, Kjael Skaalerud (SuperCat)] > "So we pulled this together via kind of public web scrape of your website long ago when we were first pulling in, putting together a demo for the broader team.    So just assume that this is like our best attempt at it without access to your data."
- [Fathom, 2026-07-14T19:00, Kylor Johnson (SuperCat)] > "I know, I looked at it first, because I think John just like scraped your guys' website at first, and so I looked at it at first, I was like, I don't think so, and so made a bunch of updates."
- [BigQuery hubspot.deal] Showroom deal 39221664105 was not created until 2025-06-20 15:47 and did not enter Discovery until 2025-06-23 18:52 — **after** the demo build had finished.

**Against:** The org record is indistinguishable from a real onboarding kickoff on structure alone. Anyone reading only `import_history` would date the project start here.

---

### Phase 1 → Phase 2 (pre-sales demo) · 2025-06-12 · confidence: high

**What changed:** First products file imported into org 273.

**Evidence:**
- [DB] `import_events` id 1601883, 2025-06-12 19:27:53, Products, **error** tier (9,289 bytes). Warnings on unknown fields `Keywords`, `custom_CountryOfOrigin`, `custom_Prop65`, `custom_ROHSCompliant`, `custom_ProductLifeCycleStatus`, `custom_Warranty`, `custom_Hazmat`. First non-error Products import 2025-06-13 (warning tier).

**Against:** None on the fact. But this satisfies "has the products file been imported" for a catalog Legrand had never seen and had not paid for.

---

### Phase 2 → Phase 3 (pre-sales demo) · 2025-06-13 · confidence: high

**What changed:** Five core file types were in within 24 hours; the demo became a browsable catalog.

**Evidence:**
- [DB] 2025-06-13: Products, Images (34 events), Product Stories, Options, Option Groups. `import_events` 1602339 (Options + Products, error), 1602406 (Option Groups + Options + Products, warning), 1602429 (same three, error).
- [DB] `options` 29 rows and `option_groups` 11 rows, all `created_at` 2025-06-16 16:54:16–17, `updated_at` identical. Codes `10FT,AT,BK,BR,BS,CP,G,GG,GR,GRY,LA,M,MB,MG,MO,MS,MW,NI,NK,OB,PW,SN,SV1,SV2,TF,TM,W,WH,WHW` / `10FTBKNI,BKGRYLA,…,SV1SV2`.
- [DB] `import_events` 1605635, 2025-06-19 14:00:23, Customers, clean (`--- - - Customers - []`).
- [DB] 6 `ipad_reports` created 2025-06-11 → 2025-06-19; 5 `notices` created 2025-06-19 13:22 → 14:26; 7 `shared_resources` created 2025-06-11/12.

**Against:** None.

---

### Phase 3 → Phase 4 (pre-sales demo) · `undetermined`

**What changed:** Ambiguous. By configuration the June 2025 demo was iPad-buildable — products, images, stories, options, customers, five notices, six report formats, a `mobile_sites` row. By substance it was fiction: the data was scraped, the customer file was invented, and the notices were written in the voice of a Legrand employee at a market that SuperCat was not attending (`"Thanks team for the awesome first day at Dallas market."`).

**Why undetermined:** I cannot date a "catalog completeness" transition for a catalog whose completeness was never the point, and there is no client statement in June 2025 to test it against — `audit_log_entries` retains only from 2025-08-27, HelpScout holds nothing before 2026-07-08, and Fathom holds nothing before 2025-11-07. I will not guess.

---

### Phase 4 → freeze · 2025-09-06 · confidence: high

**What changed:** One last demo refresh, then nothing for 285 days.

**Evidence:**
- [DB] `import_events` id 1645894, 2025-09-06 12:30:20, Products, warning tier, 2,213,669 bytes, **964 warnings**, opening with > `'Error running cleancsv: 2025/09/06 12:29:51 parse error on line 2, column 18: bare " in non-quoted-field'` and > `'Line 2: Illegal quoting, probably in the following text: , " ..OR..  Dual-Sided" …'`
- [DB] Next import of any kind: 2026-06-18 17:55:09. Gap = **285 days**.
- [DB] `login_events` for org 273 by month: 2025-07 = 2, 2025-08 = 1, 2025-09 = 2, 2025-10 = 2, 2025-11 = 2, 2025-12 = 21, 2026-01 = 0, 2026-02 = 1, 2026-03 = 1, 2026-04 = 0, 2026-05 = 2. Every one of those is `jonv`.

**Against:** The 2025-12-12 spike (21 logins, plus 12 `IpadReport updated` and 2 `user group updated` audit rows between 16:54 and 19:24, plus a submitted test order at 19:24:06) shows the demo was actively re-dressed during the freeze. The org was dormant, not abandoned.

---

### Phase 1 (real) — Kickoff · 2026-07-08 · confidence: high

**What changed:** Commercial close, then a named onboarding lead, an intro, and a scheduled kickoff. This is the first moment the project is an onboarding.

**Evidence:**
- [BigQuery hubspot.deal_property_history] deal 39221664105 "Legrand - Showroom TIER 1": `dealstage` → `53599608` ("Closed won") at **2026-06-11 13:59:44 UTC**; `closedate` set to 2026-06-11 13:59:42 in the same transaction; final `amount` 24,108 (set 2026-04-28).
- [BigQuery quickbooks.invoice] doc `WDQN3KNL-0001`, customer "Legrand North America, LLC", `txn_date` 2026-06-15, `total_amt` **24,670**, `balance` **0**.
- [HS #14747, 2026-07-08T13:52:23, trey.wilson@legrand.com (customer)] > "I wanted to check in and see when your team will have the content organizedin the app.  Should we start auditing the way things are arranged, orshould we wait until everything is in the app?"
- [HS #14747, 2026-07-08T13:52:23, jon@supercatsolutions.com (note)] > "Kylor,They are ready to go.https://drive.google.com/drive/folders/1IdX879Hyi1qOLuMUOI5ZQAUuBiCso6M6?usp=sharing"
- [HS #14752, 2026-07-08T16:50:41, kylor@supercatsolutions.com] > "I wanted to reach out and personally introduce myself as I will be your primary point of contact during the onboarding process." … > "It would be great if we could find some time early next week for an official Onboarding Kick-Off call"
- [DB] `org_users` 157982 (Kylor) created 2026-07-08 22:50:18.
- [Fathom] Kickoff call held 2026-07-14T19:00, host Kylor Johnson, 43 min, attendees Trey Wilson, Alexandra Briggs, Kyle Smith. > "I'm Kylor Johnson.    I'll be managing your guys' onboarding."

**Against:** An earlier date is defensible. On **2026-06-18/19** Jon reset the org and created the first three Legrand accounts, and by 2026-06-22 he had sent login credentials — real client provisioning, three weeks before Kylor's intro. I treat 2026-06-18/19 as the *project restart* (see §F) and 2026-07-08 as the kickoff, because the restart had no kickoff conversation, no agenda and no client-facing process orientation — Trey's 2026-07-08 email is a client who has been given a login and left to wonder what happens next.

---

### Phase 1 → Phase 2 (real) · 2026-07-14 · confidence: high

**What changed:** Legrand's own product data replaced the scraped catalog and was imported.

**Evidence:**
- [DB] `products`: 381 rows carry `deleted = true` with `last_modified_at` 2026-07-13 23:15:14 — the scraped demo SKUs being retired. (137 more were retired 2025-06-18.)
- [DB] `import_events` id 1889813, 2026-07-14 15:14:37, Products, warning tier, 46 warnings, all of form `'Line 1: Field name carton1_h is unknown.'` and `'Line 1: Custom field ''rohscompliant'' is missing.'` Followed by Product Stories clean (15:26:17) and Inventory warning (15:30:14).
- [DB] `price_levels`: all five created 2026-07-13 22:20:31 → 22:22:23 (`retail`, `imap`, `canet`, `caimap`, `camsrp`). Three new `custom_fields` created 2026-07-13 22:26.
- [Fathom, 2026-07-14T19:00, Kylor Johnson (SuperCat)] > "So this is the current product file that we have.    It's 908 products.    That is from your source file."
- [DB] `products_with_story` = 908 today, against 1,020 active — the July-14 cohort is still identifiable.

**Against:** The 381 deletions are timestamped 2026-07-13 23:15:14 but there is **no Products import event on 2026-07-13** — only 13 clean Images imports, the last at 23:15:14.315. The mechanism that retired them is undetermined; the effect is not.

---

### Phase 2 → Phase 3 (real) · 2026-07-14 · confidence: high

**What changed:** Three core files landed inside 16 minutes, none fatal.

**Evidence:**
- [DB] 2026-07-14: Products warning 15:14:37 → Product Stories **clean** 15:26:17 → Inventory warning 15:30:14 (24,103 bytes, 247 `Product not found, record ignored`, highest flagged line 1195). Repeated at 18:02 / 18:41 / 18:47. Images clean 18:27:24.
- [DB] No `:fatal` token appears in any of the 145 `import_events` rows for org 273, ever.
- [Fathom, 2026-07-14T19:00, Kylor Johnson (SuperCat)] > "And so what I did is I imported a product, an initial product file.    John had a customer file already in there." … > "And then I did an inventory and a Stories import."
- [DB] Customers completed the set later: `import_events` 1922062, 2026-08-07 16:02:29, Customers, clean; 1,133 `customers` rows all created 2026-08-07 16:02:15–16:02:29, plus 1,133 `shipping_locations`.

**Against:** None. The most recent import of every core type is non-fatal: Products clean 2026-08-18, Product Stories clean 2026-07-14, Customers clean 2026-08-07, Images clean 2026-07-24, Inventory warning 2026-08-27.

---

### Phase 3 → Phase 4 (real) · 2026-08-18 · confidence: medium

**What changed:** The catalog became genuinely buildable as a live iPad — structured browse, priced, imaged, populated with customers and a 129-item library.

**Evidence:**
- [DB] `products`: 1,020 active, all `last_modified_at` between 2026-08-18 15:58:17 and 15:58:32 (the last Products import, clean). 1,018 have `image_exists`. 310 visible / 710 `hideable`. 382 distinct net prices.
- [DB] `taxonomies`: 2 TradeName (`adorne`, `radiant`), 6 Collection (`Devices`/`Plates`/`Other` under each brand), 14 Category — all created 2026-08-17, all updated 2026-08-18. Every `taxonomy_id` parent resolves inside org 273. Labels are human-readable, not codes.
- [DB] `shared_resources`: 153 rows = 24 top-level directories (all created 2026-08-17) + 129 content items. Loaded 7 (2025-06) / 7 (2026-06-22) / 7 (2026-07-14) / 59 (2026-07-23) / 8 (2026-07-24) / 22 (2026-08-06) / 27 (2026-08-17) / 16 (2026-08-18).
- [DB] `user_types` 2641 carries `territory_url` = `https://legrand.login.go.akamai-access.com/#/login`, label `MyLegrand` — the in-app portal jump Trey asked for on 2025-12-12 (> "he'll show you here in a second on how easily it is to get into my Legrand or Service Center").
- [DB] All six Legrand `org_users` carry the same 24 territory codes; those 24 codes cover all 1,133 customers; `customers_no_territory` = 0.
- [HS #15151, 2026-08-18T16:05:56, kylor@supercatsolutions.com] > "The remaining documents are loaded: 129 items across your 24 buttons." … > "The product import completed, so Devices / Plates / Other is showing on the iPad now with your product types underneath."

**Against — substantial, which is why this is `medium` and not `high`:**
- [DB] `inventories`: **`qty_available` is NULL on all 439 rows.** The iPad displays availability. Flagged by Kylor 2026-08-17 and unfixed for 10 days.
- [DB] All 439 `inventories` rows have `created_at` 2026-08-27 06:01:10–11 — each import full-replaces the table. Today's surviving file was the adorne one; `1597*` = 0, `2097*` = 0, `R*` = 0. **Zero radiant inventory in the app right now.**
- [DB] `price_levels` contains no DealerNet. All 1,133 customers default to `imap`/`caimap`. The agreed default was DN.
- [DB] 6 active products at `net_price = 0.00`; **3 of them are visible** (`hideable = false`): `1597TRUSBAA`, `1597TRUSBCCI`, `AWP6GBL1`.
- [DB] 13 `custom_fields` are registered with `send_to_ipad = true` and hold **zero values across all 1,020 products**: `rohscompliant`, `prop65`, `switchtype`, `numberofswitches`, `workswith`, `bulbcompatibility`, `mountingtype`, `numberofgangs`, `voltage`, `wattage`, `wiresize`, `warranty`, `Color`. Nine are configured as active iPad filters. `user_types` 2641 `ipad_custom_views.order_preview` still renders `c.Color`, `c.voltage`, `c.wattage`.
- [DB] 5 of the 24 library directories have zero children (ids 38130, 38137, 38141, 38143, 38146).
- [DB] `shared_resources` 38039 (Dretzka & Associates) → `https://collectionsconfigurator.legrand.us/partner/Rep`; 38048 (Alberta LTD.) → `https://collectionsconfigurator.legrand.us/partner/`.
- [DB] `product_type` is NULL or `''` on all 1,020 products, though Tracy and Trey specified a Product Types layer on 2026-08-18.

---

### Phase 4 → Phase 5 (Reps Signed In) · **satisfied mechanically 2026-06-23; not reached in substance** · confidence: high

**What changed mechanically:** Non-admin users began logging into the iPad and remain active.

**Evidence for:**
- [DB] `login_events`, first non-admin logins: `millert` 2026-06-23 15:03:24, `abriggs` 2026-06-23 15:30:24, `k_smith` 2026-07-14 19:04:29.
- [DB] `RAWSTATE` framing holds: 5 non-admin users, 3 with `last_ipad_login_at`, 3 active in the last 30 days (`abriggs` 2026-08-27, `millert` 2026-08-20, plus `k_smith` 2026-08-07).

**Against — decisive:**
- [DB] All 10 `org_users` are `@legrand.com`, `@supercatsolutions.com`, or Kylor's gmail login. **Not one rep-agency account exists.**
- [DB] 22 of 23 `user_types` are empty. The 22 agency groups were created 2026-08-06 18:40:52–18:41:06 and have held zero users for 21 days.
- [DB] The three "reps" signed in are the Eastern Regional Manager, the Western Regional Manager, and a marketing lead — Legrand employees running acceptance testing.
- [HS #15151, 2026-08-27T16:07:06, trey.wilson@legrand.com (customer)] > "Prior to tomorrow's call, I wanted to make sure we can let our sales agents that we selected to begin testing the app by the end of next week." — as of today the client is asking permission to *begin* agency testing.
- [Fathom, 2026-08-07T16:00, Kyle Smith (Legrand)] > "do we have any super users in yet to give us feedback or no?    Because I think we talked about that last time." Answer: no.

**Reading:** a phase test keyed on "non-admin `org_users` with iPad logins" scores this client as rep-adopted. Zero reps have opened the app.

---

### Phase 5 → Phase 6 (Admin Training) · **not reached** · confidence: high

**Evidence:**
- [Fathom, 2026-08-07T16:00, Kylor Johnson (SuperCat)] > "then usually do like a kind of formal like admin training with our head of support for you guys just to, you be able to just know like, hey, a rep is having trouble logging in, just like some quick troubleshooting stuff."
- [HS #14974, 2026-08-07T18:02:42, kylor@supercatsolutions.com] > "Next week: tie up library reorg, taxonomy updates, customer/agency mapping, and inventory, then your go / no-go on beta." / > "Following week: beta testers, internal super users first." / > "After beta: admin training with our support lead (login troubleshooting, basic Admin tasks), plus optional full rep training with John if you want that for the wider team."
- [HS #15151, 2026-08-27T16:07:06, trey.wilson@legrand.com (customer)] > "Regarding the rest of the agents, we should designate 2 training times that you and your team to host. Could we select a Friday morning and an afternoon time later in September?"
- [BigQuery helpscout, 2026-08-27T16:27:28, kylor@supercatsolutions.com, **state `draft`, not in corpus**] > "As for the training, I'm coordinating internal calendars right now, as we typically have our sales team (Jon or Emery) run point on those. I'll send you availability shortly.   Additionally, we'd love to also schedule an admin training with your internal team"
- [DB] No training-related artefact exists: `smart_stacks` = 0, `onboarding_questionnaires` = 0, `onboarding_file_uploads` = 0, `org_documents` = 0.

**Against:** none. Both sides describe training as September work.

---

### Phase 6 → Phase 7 (Go-Live) · **not reached** · confidence: high

**Evidence:**
- [DB] `organizations.properties->>'status'` = `onboarding` — the only org in the system with that value.
- [DB] `orders` = 0 rows. `order_email_recipient` = `''` while `require_online_order_submission` = true — a submitted order today would have no delivery target.
- [DB] `subscriptions` for org 273 = 0 rows.
- [Fathom, 2026-01-12T19:00, Justin Baillargeon (Legrand)] > "we're not going to be using it for orders, so we're just using it really for our, to represent our digital product catalog" — orders are deliberately out of scope, so zero orders is not a go-live signal either way.
- No support handoff appears in any source.

**Against:** none.

---

## C. Current phase as of 2026-08-27

**Phase 4 — Catalog Completeness, held. Phase 5 attempted but not started. The build has been frozen for nine days.**

**Evidence:**

- [DB] Last write to any configuration table in org 273: `products.last_modified_at` = 2026-08-18 15:58:32; `taxonomies` 2026-08-18 15:58:25; `shared_resources` 2026-08-18 15:39:59; `user_types` 2026-08-17 19:15:37; `customers` 2026-08-07 16:02:29; `price_levels` 2026-07-13 22:22:23; `ipad_reports` 2025-12-12 18:55:27. **Nothing has changed in nine days.** (`organizations.updated_at` = 2026-08-19 18:17:31 is a platform-wide batch — org 93 was stamped 2026-08-19 18:17:26, five seconds earlier.)
- [DB] The only activity since: the daily inventory feed (`import_events` 06:01 every day through 2026-08-27) and rep logins (`abriggs` 2026-08-27 14:31:33).
- [HS #15151, 2026-08-27T16:07:06, trey.wilson@legrand.com (customer)] > "I want to make sure you are confident the changes will be ready for them to test. … Our sales agent are ready to get going with us and eCat which is great."

**The next real blockers, in order of what actually stops the beta:**

1. **Inventory reads blank, and half of it is missing.** `qty_available` is NULL on all 439 rows; the field the app displays has never been populated. Worse, adorne and radiant arrive as two separate emailed files, each import hard-deletes and reloads the whole table, and only one of the two lands on most days — 6 days both, 11 days radiant only, 6 days adorne only, over 2026-08-05 → 08-27. This morning it was adorne, so radiant inventory is currently absent entirely. Owner: Legrand customer support (Trey, HS #14833, 2026-07-24: > "Made the request, need to hear back from customer support.").
2. **DealerNet does not exist.** Trey unblocked it on 2026-08-18 18:22:08 — > "For Dealer Net, the Column H in the US adorne price is labeled as DN. That is the customer cost, and we would prefer IMAP and DN show." — and no price level has been created since. All 1,133 customers still default to iMAP. Owner: SuperCat.
3. **Nine days of client instructions unactioned.** Tracy's 2026-08-18 17:57:45 library spec (~40 discrete moves/removals), her 2026-08-18 18:28:48 Collections structure, and Trey's 2026-08-21 13:06:31 CEU swap. Verified unactioned: `shared_resources` max `updated_at` = 2026-08-18 15:39:59; "Art of Residential Lighting" (id 37932), "Wireless Charger Sell Sheet" (37901), "POGs SS3329R2" (37903), "adorne Planogram with Pricing (US)" (37904) and "(Canada)" (37905), "Standard to Smart Sell Sheet" (37943), "radiant AFCI Receptacles Cut Sheet" (37889), "radiant IS PASS LED Dimmer" (33208) and "radiant Hospitality EWS RAD BR" (33209) are all still present; "Contemporary Residential Lighting Controls" is absent. Owner: SuperCat.
4. **No agency user can be created.** 22 empty user groups, no agency→territory mapping (all six internal users hold all 24 codes), and two Design Studio URLs still broken. The beta Trey wants "by the end of next week" has no accounts to run on. Owner: split — Legrand owes the territory mapping (asked 2026-08-07, HS #14974), SuperCat owes the accounts.
5. **Unanswered scope question with structural consequences.** [HS #15151, 2026-08-17T22:58:17, kylor@supercatsolutions.com] > "Wiremold and Pass &amp; Seymour run through the whole library, but there are no Wiremold or P&amp;S products in the catalog. All 1,020 are adorne and radiant. Are those coming? That would change the structure more than a rename." Asked twice, never answered.

---

## D. Turning points

**1 · 2025-06-10 → 2025-06-19 — the demo that became the record.** SuperCat built a full org from a web scrape before a deal existed. Everything that makes this client look like a 14-month grind — the 2025-06-12 first import, the 285-day gap, the 6 iPad reports, the 5 notices, the 29 orphan options — is an artefact of this decision. It also worked: it is what Jon showed Trey in November and the whole Legrand team in December.

**2 · 2025-11-07 — Trey chooses manual and freezes the work.** He asks to bypass the automated-feed dependency (> "Could we get this thing kicked off on a more manual, like me handing you stuff, manual for me, instead of it being this automatic feed?") and in the same call closes the door (> "And I don't want you to do anything else until that's a done deal.", > "knowing that the check's going to get cut in 26, not now."). HubSpot moves the deal to Commit at 15:52:39, 52 minutes after the call began, and cuts the amount from $31,200 to $25,200. The decision that unblocked the eventual build also guaranteed seven more months of silence.

**3 · 2026-01-12 — the real blocker is named, and it is not technical.** In a security review that finds nothing (> "to be honest with you, just going through it, I don't see any issues"), Justin says > "we haven't signed the contract or anything yet" and > "we're still going through and getting the approval from David Morris and Central on this because we have to, like, hey, go through a governance process with them on a new tool or application we adopt." Eleven close-date slips in HubSpot are this, repeated.

**4 · 2026-06-11 → 2026-06-19 — the project actually starts, and the demo is destroyed.** Deal closed won 2026-06-11 13:59:44; invoiced 2026-06-15 for $24,670, paid. On 2026-06-18 Jon imports a customer file (17:55:09), destroys three internal SuperCat accounts (19:13:42, :47, :53), rewrites the user group (19:15:16) and renames it off `DefaultUserGroup` (19:18:56). On 2026-06-19 he deletes the December test order (10:50:12 — order `144053-121225-20`) and creates Alexandra (10:54:32), Trey (10:58:37) and Tracy (11:00:46). **None of this appears in the corpus.** It is recoverable only from `audit_log_entries` and `login_events`.

**5 · 2026-08-18 15:58 — the build stops mid-sentence.** The last products import completes the Devices/Plates/Other structure. Kylor's follow-up that afternoon sits in HelpScout as `state: draft`. Within four hours Tracy sends the most detailed client specification of the entire project and Trey answers the one question blocking pricing. Nine days later nothing has been touched, and Trey is asking whether agency testing can start next week. Whatever the cause, this is the moment the project's momentum and the client's momentum came apart.

---

## E. The seven extra questions

### A. Did this client ever go backwards?

**No — but the record is built to look as though it did, and there is one genuine partial regression.**

The 285-day gap and the 79-day gap before it are not decay. They are the sales cycle sitting on top of a pre-sales asset. The `import_history` clock starts 2025-06-12 because SuperCat chose to build speculatively, not because Legrand started and stalled. Reconstructed gaps (`import_events`, distinct dates): 2025-06-19 → 2025-09-06 = **79 days**; 2025-09-06 → 2026-06-18 = **285 days**; 2026-06-18 → 2026-07-13 = 25 days; 2026-07-24 → 2026-08-05 = 12 days; 2026-07-14 → 2026-07-23 = 9 days.

Three things did move backwards, all deliberate and all inside the 2026 project:

1. **The catalog was torn down.** 381 products soft-deleted 2026-07-13 23:15:14, on top of 137 from 2025-06-18. 1,538 product rows exist for a 1,020-product catalog. The scraped catalog Trey and Alexandra had been browsing since 2026-06-22 was replaced under them.
2. **Tracy's identity was destroyed and rebuilt.** `org_user` 157199 created 2026-06-19 11:00:46, destroyed 2026-06-22 17:17:38, recreated as 157530 at 17:19:22.
3. **The user group was renamed twice, and its meaning inverted.** `DefaultUserGroup` (2025-06-10 → 2026-06-18) → `Lighting Showrooms` (2026-06-18 → 2026-08-17) → `Admin / Internal Legrand` (2026-08-17 →). Corroborated independently by `login_events.user_group_name`: last `DefaultUserGroup` login `jonv` 2026-06-18 17:43:43; first `Lighting Showrooms` login `jonv` 2026-06-19 10:49:28; first `Admin / Internal Legrand` login `Treyw` 2026-08-18 12:40:13. The third rename is an admission: the group that was supposed to hold showroom reps was reclassified as internal-only once the 22 agency groups were built.

The genuine regression is **the last nine days**. Client instruction volume went up sharply on 2026-08-18 and SuperCat output went to zero on the same day.

**Did anyone treat the gap as a problem at the time?** No. It was never framed as a problem because it was never framed as an onboarding. The only person in the org during those nine and a half months was Jon, and his December activity was demo preparation. There is no message anywhere expressing concern about elapsed time.

### B. Adoption — separate from go-live

**Six people have ever used this org as a client. All six are Legrand employees. Zero reps.**

| User | Logins | Distinct days | First | Last | Devices |
|---|---|---|---|---|---|
| Trey Wilson (`Treyw`) | 48 | 28 | 2026-06-22 18:02:26 | 2026-08-21 14:59:02 | 1 |
| Alexandra Briggs (`abriggs`) | 25 | 11 | 2026-06-23 15:30:24 | 2026-08-27 14:31:33 | 2 |
| Tracy Miller (`millert`) | 12 | 9 | 2026-06-23 15:03:24 | 2026-08-19 15:17:47 | 2 |
| Kyle Smith (`k_smith`) | 5 | 4 | 2026-07-14 19:04:29 | 2026-08-07 16:09:07 | 1 |
| Justin Baillargeon | **0** | 0 | account 2026-08-07 17:35:57 | — | — |
| Greg Kozniewski | **0** | 0 | account 2026-08-12 20:49:00 | — | — |

SuperCat staff, for contrast: `jonv` 169 logins over 27 days; `Kylor_Johnson` 18 over 5; `swt` 35 over 4 (June 2025 only); `kjael` 8; `brentsanders` 9; `chuck-user` 5.

Everyone is on iPad — `last_ecat_online_login_at` is NULL for all 10 `org_users`, and `eol_login` = 0 for the one populated user type. All four active Legrand users are on `iPad15,7` running build `20260808`, i.e. they are on current software and syncing.

Trey is a real user, not a checkbox: 28 distinct days over two months, on a single device. Alexandra logged in this morning. But nobody is *selling* with it — `orders` = 0, `smart_stacks` = 0, `user_stacks` unused, no `placement_reports`, no `sales_data`. This is acceptance testing, and it is genuine.

### C. Current trajectory

**Client engagement: improving. SuperCat delivery: stalled since 2026-08-18. Net: at risk, on a deadline the client has now set.**

Improving, on evidence: client login-days by month — 2026-06: 4, 2026-07: 9, 2026-08: 14. `login_events` totals 2026-06: 27 / 2026-07: 51 / 2026-08: 44 (August with four days left). Trey's user-group history shows him following the platform through two renames. Tracy escalated from feedback to authoring the information architecture. Two new stakeholders redeemed invitations in August. The client's last three messages are all forward-leaning, and Trey's 2026-08-27 note is the opposite of disengagement — > "Our sales agent are ready to get going with us and eCat which is great."

Stalled, on evidence: zero configuration writes in nine days across every table checked. Kylor's last iPad login was 2026-08-07; his last *published* message 2026-08-17 22:58:17 (the 2026-08-18 16:05:56 note carries HelpScout `state: draft`); his 2026-08-27 reply is also a draft. Three named client requests are outstanding with no partial progress.

The daily inventory feed is the only thing still moving on its own: it ran at 2026-08-27 06:01:11–12 this morning, warning tier, as it has every day since 2026-08-05. **It is running, not working** — see G.

### D. Was the catalog ever *wrong* while the imports looked *clean*?

**Yes, in four distinct ways, and one of them is the clearest case in this dataset of the import tier actively hiding a defect.**

**1 · The importer warned thirteen times, then stopped warning while nothing was fixed.** `import_events` 1902247 (2026-07-23 21:41:29, Products, warning) carries exactly 13 warnings: > `'Line 1: Custom field ''rohscompliant'' is missing.'`, then `'Color'`, `'voltage'`, `'wattage'`, `'switchtype'`, `'workswith'`, `'wiresize'`, `'mountingtype'`, `'prop65'`, `'warranty'`, `'numberofswitches'`, `'bulbcompatibility'`, `'numberofgangs'`. Sixty-one minutes later, `import_events` 1902318 (2026-07-23 22:42:30) records `--- - - Products - []` — **clean**. Every Products import since (2026-07-24 ×2, 2026-08-06 ×4, 2026-08-17 ×2, 2026-08-18) is clean. Today, all 13 fields are still empty on all 1,020 products, all 13 still carry `send_to_ipad = true`, and nine are still wired as active iPad filters (`use_as_filter` = `multi` or `binary`). The tier went from warning to clean without a single value being added. Kylor had already asked and never got an answer — [HS #14783, 2026-07-14T23:12:59] > "do you have structured spec data re: voltage, wattage, mounting type, number of gangs, wire size, that kind of thing, or are we launching without those fields? The source file had them empty." He then announced two of those very filters as done: [HS #14833, 2026-07-23T22:50:27] > "Enable Finish and # of Gangs as active iPad filters (quick Admin Console toggle,doing that now)". `# of Gangs` has zero values. **A rep tapping it gets an empty filter.**

**2 · Somebody described something wrong on the iPad, and the import log for that day was clean.** On the 2026-07-14 kickoff Trey said: > "This is not your fault by any means, but see like on the very top line, it says Radiant.    And it has like a wing ding." Kylor committed to > "there's a junk character showing up before "adorne" and "radiant" in a lot of the product descriptions; I'll clean that up and keep the ®" and Trey specifically asked > "I would leave the R just because it's there on purpose." The junk character is gone. **So is the ®: `long_description LIKE '%®%'` returns 0 of 1,020, and `long_description ~ '[^\x20-\x7E®]'` returns 0.** Descriptions now read `One-Gang Screwless Wall Plate, Pale Blue` — no brand word, no trademark mark. The demo data had it: the deleted 2025-12-12 test order recorded `"item_description" : "radiant® Two Gang Screwless Wall Plate, Nickel"`. Every products import since 2026-07-23 22:42 has been clean tier. A brand team Trey described as > "they're, they're particular about brand, that we are particular about brand standards" has lost its trademark notice on 1,020 items, and no import will ever flag it.

**3 · Five stale notices from the demo still push to every active user.** `notices` 171–174 created 2025-06-19 13:22–14:26, `notices` 208 created 2025-12-12 17:08:29, and `audit_log_entries` 2026-06-18 19:18:56 confirms `"notices":[171,172,173,174,208]` bound to user group 2641 — the group all 10 users sit in. Contents include > "Attention Dallas market attendees!  Order origin will default to “Dallas market” June 18-20.  To ensure order reporting accuracy, do not override this unless writing orders/quotes not related to market.", > "Thanks team for the awesome first day at Dallas market.  Great job on the setup and getting customers into the showroom.  Day two!  Let’s knock it out of park!", and > "We call these Notices. You can send them to your reps and segment them by User Groups." Notices are not imported, so no import tier could ever surface this. Trey, Alexandra, Tracy and Kyle have been syncing against fabricated internal messages dated fourteen months ago.

**4 · Inventory: 31 consecutive warning-tier imports where the displayed field is empty.** See G. The tier is honest here — it says warning every day — but it warns about the *wrong thing* (247 unmatched rows) and is silent about the thing that actually breaks the screen (`QtyAvailable` absent from the file).

### E. Placeholder or dangling references?

**Checked both directions. No cross-org contamination. Seven classes of dangling or placeholder reference inside org 273.**

*Placeholders:*
1. **6 products at `net_price = 0.00`** — `AWP6GBL1`, `1597TRUSBAA`, `1597TRUSBCCI`, `1597TRUSBCCLA`, `1597TRWRUSBCCW`, `R26USBPD65WCC6`. Not the $1.00 pattern; $0.00, which renders as a price. **Three are visible** (`hideable = false`): `1597TRUSBAA`, `1597TRUSBCCI`, `AWP6GBL1`. Open since 2026-07-14, escalated 2026-07-24 (> "AWP6GBL1 , 1597TRUSBAA , 1597TRUSBCCI , 1597TRUSBCCLA , 1597TRWRUSBCCW , R26USBPD65WCC6  — drop, hold at $0, or send prices?"), never answered.
2. **`organizations.order_footer_text`** on org 273 reads > "This order is subject to our standard terms and conditions. All custom upholstery sales are final.  Please call immediately to report shipment damage. … * 50% Deposit required on all orders. * In Stock Orders must be picked up within 48 hours * 3% Holding charge per month on all orders held over 30 days." Legrand sells wiring devices. This is boilerplate cloned from a furniture org and never cleared.
3. **`order_email_recipient` = `''`** while `require_online_order_submission = true`. Any order submitted today goes nowhere.

*Dangling references:*
4. **10 inventory rows point at BaseItemCodes with no product row at all** in org 273 (not even a deleted one): `ADPD453LM2`, `ADTP700MMTUM2`, `ADTP700MMTUW2`, `ARPTR151GM2WP`, `ARPTR151GW2WP`, `ARTR152M4WP`, `ARTR152W4WP`, `ARUSBM4` (qty 1,407), `ASPD1532M4WP`, `ASPD1532W4WP`. These are the *same ten codes* the importer logged as > `'Line 39: Product not found, record ignored., BaseItemCode=ADPD453LM2'` — the log says the records were ignored; they are in the table with quantities. Log and state disagree.
5. **Two agency Design Studio links resolve to placeholders**: `shared_resources` 38048 (Alberta LTD.) → `https://collectionsconfigurator.legrand.us/partner/` (empty path); 38039 (Dretzka & Associates) → `https://collectionsconfigurator.legrand.us/partner/Rep`. Plus data-quality damage in the others: `partner/Englightening%20Sales` (misspelled), `partner/FLERCHER%20LIGHTING%20` (should be Fletcher, trailing space), `partner/Light%20SOCAL` against label "Light So Cal", trailing spaces on `BLJ group ` and `Dunn Brands `.
6. **A library item pointing into a named employee's personal OneDrive.** `shared_resources` 33218 "radiant® Video", created 2025-06-12 14:16:05, `value` = `https://grpleg-my.sharepoint.com/personal/greg_kozniewski_legrand_com/_layouts/1…`. Flagged 2026-08-06 (> "This one is pointing to a personal SharePoint URL, so anyone opening ithits a Microsoft login prompt") and still live 21 days later. If Greg leaves, it dies.
7. **29 options and 11 option_groups, fully orphaned.** All created 2025-06-16 16:54, `updated_at` identical, never touched in 14 months. **Zero active products reference them**: `options` is `--- :custom: false` on all 1,020 rows; `option_images` = 0, `option_mappings` = 0, `matrix_options` = 0. Kylor was right on 2026-07-14 — > "And then options is not, it doesn't seem like it's applicable to your products at first glance." They are demo residue.
8. **A `mobile_sites` row that contradicts the security review.** Row 141, created 2025-06-13 12:42:16 by `org_user` 144051 (Brent), with `enable_online_catalog = true`, `allows_unauthenticated_users = true`, `self_service_enrollment_enabled = true`, `hide_products_marked_hideable = false`, `display_quantity_available = true`, `default_user_type_id = 2641`. On 2026-01-12 Brent asked > "I think you guys are just looking at eCat, not eCat Online.    Is that correct?" and Justin answered > "Correct." — while telling his cybersecurity reviewer the asset was > "Not publicly, but, yes, our servers are on the Internet." I have not tested whether this storefront is reachable and make no claim that it is; the row's flags are what they are, and they were signed off as out of scope. Note also `enable_rep_enrollment = true` and `enable_delegated_enrollment = true` on the org.

*Cross-org check, both directions:* no product, customer, taxonomy, library, user group or option row in org 273 references org 93 or any other org, and none in org 93 references org 273. `XEVPED%` products exist only in org 273 (11 rows) — the `xevped2_3.jpg` string in the 2025-09-06 import warning is Legrand's own EV-charging pedestal line, not another client's data. Every `taxonomies.taxonomy_id` parent resolves inside org 273. Every `customers.default_price_code` resolves to an existing org-273 price level. The only genuine crossover in the entire estate is SuperCat's `steve@supercatsolutions.com` holding memberships in both `leg` and `lna`.

### F. `audit_log_entries` and `organization_invitations`

**`audit_log_entries` is where this client's real restart is recorded, and none of it is in the corpus.** Matched on `data::text ILIKE '%"organization":"leg"%'`: 16 rows, 2026-06-18 → 2026-08-17.

| When (UTC) | Event | What it shows |
|---|---|---|
| 2026-06-18 19:13:42 / :47 / :53 | `OrgUser destroyd` ×3 | Three org memberships removed in 11 seconds, actor `org_user` 144053 (Jon). Two are identifiable only from `login_events`: **Chuck Wiebe** and **Steve Thrasher**. The third never logged in and cannot be identified — the audit payload is `{"id":144053,"organization":"leg"}`, i.e. it records the *actor*, not the deleted row. |
| 2026-06-18 19:15:16 | `user group updated` | `trade_names_auth` c, `surcharge_types_auth` a, `notices:[171,172,173,174,208]` |
| 2026-06-18 19:18:56 | `user group updated` | prior `name` = `DefaultUserGroup` — the rename off the demo default |
| 2026-06-19 10:50:12 | `order deletion` | `{"order_number"=>"144053-121225-20", "order_org_user_id"=>144053, "order_org_user_username"=>"jonv"}` |
| 2026-06-19 10:54:32 | `OrgUser created` | 157197, `user_type` "Lighting Showrooms", `is_admin` false, `territory_codes ["ERSM"]` → Alexandra |
| 2026-06-19 10:58:37 | `OrgUser created` | 157198, `is_admin` false, `territory_codes []` → Trey (**created as non-admin; is admin today**) |
| 2026-06-19 11:00:46 | `OrgUser created` | 157199, `territory_codes ["SRCM"]` → Tracy, first attempt |
| 2026-06-19 11:01:14 | `OrgUser updated` | 157198 |
| 2026-06-22 17:17:38 | `OrgUser destroyd` | 157199 removed |
| 2026-06-22 17:19:22 | `OrgUser created` | 157530 → Tracy, recreated 1m 44s later |
| 2026-07-13 16:25:45 | `OrgUser created` | 158112 → Kyle Smith |
| 2026-08-17 19:16:26 → 19:17:11 | `OrgUser updated` ×6 | 158893, 157197, 159033, 157530, 158112, 157198 — actor `org_user` 157982 (Kylor), 8–10 s apart. This is > "Territory codes are set for all six of you as well. Alex, that's why your customer list looked empty. The code on your account didn't match any customer." (2026-08-17 22:58:17), and the payloads confirm the old values `["ERSM"]` and `[]`. |

Also in the audit log, outside the `"organization":"leg"` key (found via `parent_type='OrgUser'` on leg org_user ids, and `Organization updated` where `data LIKE '{"id":273,%'`): **a whole day of demo preparation on 2025-12-12** — `user group updated` 16:54:05; nine `IpadReport updated` between 17:14:19 and 18:55:27 (re-pointing report fields at `c.Color`, `c.Finish`, `c.countryoforigin`, `c.rohscompliant`, `c.Catalog`, `c.brochure*`, `c.CutSheet`); `Organization updated` 19:13:28 rewriting `ipad_custom_views`; and at **19:24:06 an `order submission`** — one item, `RWP262NICC6`, > `"item_description" : "radiant® Two Gang Screwless Wall Plate, Nickel"`, qty 1, price 100. The 2025-12-12 call started at 19:30. Jon dressed the demo and wrote a test order six minutes before walking into a sixteen-person meeting.

**`organization_invitations` is a genuinely separate third source.** 4 rows for org 273:

| id | Email | Created | Expires | Redeemed | Redeemed by |
|---|---|---|---|---|---|
| 237 | greg.kozniewski@legrand.com | 2026-07-30 16:16:22 | 2026-08-06 16:16:22 | **never** | — |
| 238 | justin.baillargeon@legrand.com | 2026-07-30 16:16:23 | 2026-08-06 16:16:23 | **never** | — |
| 244 | justin.baillargeon@legrand.com | 2026-08-07 16:26:27 | 2026-08-14 | 2026-08-07 17:35:57 | user 80928 |
| 245 | greg.kozniewski@legrand.com | 2026-08-07 16:26:27 | 2026-08-14 | 2026-08-12 20:49:00 | user 81009 |

This corroborates the 2026-08-07 call exactly — [Fathom, 2026-08-07T16:00, Kylor Johnson] > "Oh, so I sent Justin and Greg one, and they both expired yesterday, but I can send them out again." The expiry was 2026-08-06 16:16, i.e. "yesterday". And the handoff's warning is confirmed: **`org_users` 158893 and 159033 have no `OrgUser created` audit row** — self-enrolment writes nothing to the audit log. Without this table, Justin and Greg appear from nowhere.

The three June-2026 accounts (Trey, Alexandra, Tracy) are *not* in this table — Jon created them directly, which is why they have audit rows and no invitations. **Neither source alone gives the full user history; you need `login_events` as well to see Chuck Wiebe and Steve Thrasher, who appear in none of the other three.**

And the counter-check: Kylor's claim > "I just sent Sonia an eCat invite so she can get on the iPad and start testing" (2026-07-24 22:52:28) is contradicted by all three sources — no invitation exists between 2026-07-08 and 2026-07-30, no audit row, no `users` row on any Legrand domain named Sonia.

### G. What is the recurring feed actually doing?

**It is delivering half the inventory, with the displayed field empty, and dropping 247 rows a day. Someone read it once, ten days ago, and reported the wrong number.**

**It is not one feed, it is two files.** Every import splits cleanly into two signatures:

| Signature | Size | `Product not found` | Highest flagged line | Content |
|---|---|---|---|---|
| adorne | 997–1,002 B | **10** | 151–344 | `ADPD453LM2`, `ADTP700MMTUM2`, `ARPTR151GM2WP`, `ARUSBM4`, `ASPD1532M4WP` … |
| radiant / Pass & Seymour | 23,106–23,119 B | **237** | 756 | `1597`, `1597BK`, `1597BKCCD12`, `1597NTLTRBKCCD4`, `1597RED`, `2097*`, `885*` … |

Trey said it would be this way — [HS #14821, 2026-07-21T19:40:47, trey.wilson@legrand.com] > "It is sent daily at 1:00 AM CST, and there will be one file for adorne and one radiant. There will be products that should not be included in the eCat app due to them serving healthcare and similar applications."

**Finding 1 — the feed started 2026-08-05, not 2026-07-14.** `RAWSTATE` says *"Inventory has imported 31 times between 2026-07-14 and 2026-08-27, at ~06:01 daily"*. The 31 count is right; the framing is not. The two 2026-07-14 imports (15:30:14 and 18:47:13, 24,103 bytes, 247 unmatched, highest flagged line 1195) are Kylor's manual load of a single combined static file — > "And then I used inventory feeds for just kind of like an initial look and feel of what inventory looks like." The automated 06:01 feed begins **2026-08-05 06:00:41** and has run 29 times since. There is a 22-day inventory gap between them, which no gap analysis surfaces because both endpoints are inventory imports.

**Finding 2 — only one of the two files arrives on 17 of 23 days.** Both files: 2026-08-05, 08-07, 08-08, 08-14, 08-21, 08-23 (6 days). radiant only: 08-09, 08-10, 08-11, 08-12, 08-13, 08-15, 08-16, 08-17, 08-19, 08-22, 08-25 (11 days). adorne only: 08-06, 08-18, 08-20, 08-24, 08-26, **08-27** (6 days).

**Finding 3 — and each import wipes the whole table, so the missing brand is simply gone.** All 439 `inventories` rows carry `created_at` **2026-08-27 06:01:10–11**: the import hard-deletes and reloads. Today's surviving file was adorne, so right now: `base_item_code LIKE '1597%'` = **0**, `LIKE '2097%'` = **0**, `LIKE 'R%'` = **0**; 380 of 439 codes begin `A`. **A rep opening any radiant product today sees no inventory record at all.** On the 11 radiant-only days the same thing happens to adorne. On the 6 both-days, the second import overwrites the first. There has never been a moment when both brands' inventory were in the app together.

**Finding 4 — the field the app displays has never had a value.** `qty_available` is NULL on 439 of 439 rows; `qty_on_hand` is populated on all 439 (397 positive, **20 negative**, 22 zero). Only 429 of 439 rows match an active product, and only 429 of 1,020 active products (42%) have an inventory row at all.

**Is anyone reading the warnings? Once.** [HS #15151, 2026-08-17T22:58:17, kylor@supercatsolutions.com] > "Inventory. The daily feed is running fine, but it sends quantity on hand rather than quantity available, and availability is the field the app displays, so it reads blank until that column is added. Worth holding off on judging that one. Two other things from the feed: 237 SKUs in it aren't in the catalog (161 are case-pack variants, but 76 are plain SKUs like 1597, 2097 and 885), and 31 items show negative on-hand."

That is a careful, accurate read of **one of the two files** — the 237 figure is the radiant file alone. The adorne file's 10 unmatched rows are unaccounted for; the true daily drop when both land is **247**. The "31 items show negative on-hand" figure likewise comes from the radiant file; today's adorne file yields 20. And neither Kylor nor anyone else noticed that the two files overwrite each other, or that only one arrives most days.

Trey's response tells you how much of this reached the client: [HS #15151, 2026-08-18T18:22:08, trey.wilson@legrand.com] > "I am not super clear on the inventory issue.    Can you elaborate on this and the pricing issue (s)?" He was answered in the 2026-08-18 16:05:56 note, which carries HelpScout `state: draft`. Ten days on, `qty_available` is still NULL.

**Rows silently dropped per day:** 247 when both files land, 237 on radiant-only days, 10 on adorne-only days. Since the automated feed began: 6×247 + 11×237 + 6×10 = **4,149 ignored rows across 29 imports**, every one recorded as warning tier and never escalated after 2026-08-17.

---

## F. The 285-day gap, answered specifically

**What stopped:** nothing that had started. There was no onboarding to stop. What went dormant on 2025-09-06 was a **pre-sales demo asset**, built by SuperCat between 2025-06-10 and 2025-06-19 from a public web scrape of legrand.us, with no contract and no Legrand participant. The last act before dormancy was a re-import of that same scraped file at 2025-09-06 12:30:20 — 2,213,669 bytes, 964 warnings, opening with > `'Error running cleancsv: 2025/09/06 12:29:51 parse error on line 2, column 18: bare " in non-quoted-field'`. Nobody fixed it because nobody was waiting on it.

**Why it lasted 285 days:** Legrand procurement and governance. HubSpot deal 39221664105 records **eleven `closedate` revisions** between 2025-07-01 and 2026-06-02. The reason is on the record twice. Trey, 2025-11-07: > "And I don't want you to do anything else until that's a done deal." and > "knowing that the check's going to get cut in 26, not now." Justin, 2026-01-12: > "we haven't signed the contract or anything yet" and > "we're still going through and getting the approval from David Morris and Central on this because we have to, like, hey, go through a governance process with them on a new tool or application we adopt.    So right now, it's still going through the process with him." Clinton's own review found nothing to object to (> "to be honest with you, just going through it, I don't see any issues") — the blocker was never technical or security-related. It was a Central marketing sign-off.

The gap was not idle at SuperCat's end either. On **2025-12-12**, the day of the sixteen-person live demo, Jon logged in 21 times, edited nine iPad report formats between 17:14:19 and 18:55:27, rewrote the org's `ipad_custom_views` at 19:13:28, and submitted a test order at 19:24:06 — six minutes before the call started. Selling continued; building did not.

**What restarted it, precisely:**

| When (UTC) | Event | Source |
|---|---|---|
| 2026-06-11 13:59:44 | Deal → **Closed won**, $24,108 | `hubspot.deal_property_history` |
| 2026-06-15 | Invoice `WDQN3KNL-0001`, $24,670, balance 0 | `quickbooks.invoice` |
| 2026-06-18 17:43:43 | `jonv` last login under `DefaultUserGroup` | `login_events` |
| 2026-06-18 17:55:09 | **Customers import, clean — the 285-day gap ends** | `import_events` 1856381 |
| 2026-06-18 19:13:42/47/53 | 3 `OrgUser destroyd` (Chuck Wiebe, Steve Thrasher, +1 unidentified) | `audit_log_entries` |
| 2026-06-18 19:15:16 / 19:18:56 | User group rewritten, then renamed off `DefaultUserGroup` | `audit_log_entries` |
| 2026-06-19 10:49:28 | `jonv` first login under `Lighting Showrooms` | `login_events` |
| 2026-06-19 10:50:12 | December test order `144053-121225-20` deleted | `audit_log_entries` |
| 2026-06-19 10:54:32 / 10:58:37 / 11:00:46 | Alexandra, Trey, Tracy accounts created | `audit_log_entries`, `org_users` |
| 2026-06-22 ~12:12 ET | Jon emails logins: > "Trey: TreywAlex: abriggsTracy: millert" | quoted inside HS #14747 |
| 2026-06-22 18:02:26 | Trey's first iPad login | `login_events` |

**Who restarted it:** Jon Vanderberg, on his own, seven days after signature. Kylor did not appear for another twenty days.

**Is the project that resumed in June 2026 the same project that stopped in September 2025?**

**No. It shares an org id and almost nothing else.** Between them SuperCat deleted or replaced: the catalog (381 of the scraped SKUs retired 2026-07-13, on top of 137 in 2025; 1,020 of the 1,538 product rows are Legrand's own data, imported from 2026-07-14), the customer file (all 1,133 rows created 2026-08-07 16:02, replacing whatever Jon loaded on 2026-06-18), the pricing (all five `price_levels` created 2026-07-13 22:20–22:22 — none existed before), the user population (3 of 3 pre-2026 internal accounts destroyed; 7 new accounts created), the user group's name and meaning (twice), the taxonomy (all 22 `Collection`/`Category` rows created 2026-08-17), the library structure (all 24 directories created 2026-08-17), the browse hierarchy, and the test order.

Four things did survive the transition, and each one is a live defect today:
1. **7 library items from 2025-06-11/12**, re-parented into the new structure — including `shared_resources` 33218 pointing at Greg Kozniewski's personal SharePoint, and 33208/33209 which Tracy asked to have removed on 2026-08-18.
2. **All 5 notices**, still bound to the only populated user group, still telling four active users about Dallas market June 2025.
3. **All 6 iPad report formats**, created 2025-06-11 → 2025-06-19 and last edited 2025-12-12. This corrects the handoff's framing: the library is recent, the report formats are fourteen months old and are pre-sales artefacts, not evidence of recent substantial build.
4. **29 options, 11 option_groups, 16 of 19 custom fields, and the `mobile_sites` row** — created June 2025, never used, never cleared.

The honest description: **a fourteen-month org record containing a nine-day pre-sales demo, a nine-and-a-half-month procurement wait, and a seven-week onboarding that is now nine days stalled with a client-set deadline of 2026-09-11.**

---

## Where the seven-phase model does not fit

1. **There is no slot for pre-sales build.** Phases 1–4 are satisfied by June 2025 evidence — org created, products imported, five file types in, a buildable catalog — for a project that did not exist. Any model reading `organizations.created_at` and `import_history` will date this client's onboarding at 14 months and score its gap as decay. The correct reading is 7 weeks and no decay at all. **This is the single largest scoring risk in this client.**
2. **Phase 5 ("Are reps actually logging into the iPad?") returns a false positive.** The framework's own rep definition (`is_admin` false, `user_type <> 'DefaultUserGroup'`, not `@supercatsolutions.com`, not disabled) matches 5 users, 3 with logins, 3 active in 30 days — a clean pass. Every one is a Legrand employee doing acceptance testing. Zero rep-agency accounts exist and 22 agency user groups are empty. A model that distinguished internal from external would need the email domain of the *rep organisation*, which is unknowable here because there isn't one yet.
3. **Phase 4 ("buildable as a live iPad") cannot see whether the build is correct.** By every structural count this catalog passes. It also has NULL availability on 100% of inventory rows, one of two brands' inventory missing on any given day, no DealerNet level despite DealerNet being the agreed default, 3 visible $0.00 SKUs, 13 empty iPad filter fields, 5 empty library buttons, 2 dead agency URLs, and 5 notices from a market fourteen months ago. Buildable and shippable are different questions.
4. **The phases assume monotonic progress; this client's most informative event is a stall inside a phase.** Nothing regressed a phase on 2026-08-18. Yet that date — zero configuration writes for nine days while client instruction volume spiked — is the most decision-relevant fact about this account, and no phase transition can express it.
5. **"Progress" (>1 core file, no fatal on the most recent of each) is trivially satisfied and stays satisfied.** There has never been a `:fatal` token in 145 import events across 14 months. The test cannot fail here, so it carries no information.
6. **Import tiers measure the wrong surface.** The 2026-07-23 21:41 import warned thirteen times that thirteen iPad-visible filter fields had no column; sixty-one minutes later the same catalog imported clean, and it has imported clean nine times since with all thirteen fields still empty. Tier improved; the catalog did not change.
7. **Go-live is defined partly by order activity, which this client has contractually excluded.** Justin, 2026-01-12: > "we're not going to be using it for orders". `orders` = 0 is a design decision, not a signal. Any readiness measure leaning on order flow will read this account as pre-live forever, even after a successful launch.

---

## Contradictions with `RAWSTATE_leg.json`

The DB is not automatically right, and neither is the capture. Five discrepancies, in descending importance:

1. **`recurring_feed` framing.** `RAWSTATE`: *"Inventory has imported 31 times between 2026-07-14 and 2026-08-27, at ~06:01 daily and sometimes twice a day."* The count is correct; the description is not. The two 2026-07-14 imports were manual (15:30 and 18:47) and the automated 06:01 feed began 2026-08-05, leaving a 22-day inventory gap in between. "Sometimes twice a day" is not jitter — it is two different brand files, one of which is absent on 17 of 23 days, and each import full-replaces the table.
2. **`order_rows_total: 0` / `submitted_orders: 0`.** True at capture. But `audit_log_entries` records an `order submission` at 2025-12-12 19:24:06 (order `144053-121225-20`, item `RWP262NICC6`, qty 1, price 100) and an `order deletion` of that same order at 2026-06-19 10:50:12. An order existed in this org for 189 days. "Zero orders after 14 months" is true of the table and false of the history.
3. **`largest_gaps` first entry: 78 days.** Computed from `import_events` distinct dates, 2025-06-19 → 2025-09-06 is **79 days**. Minor, but the 285 and 25 figures reconcile exactly, so this one is an off-by-one.
4. **`populated_user_types` name.** `RAWSTATE` reports the single populated group as "Admin / Internal Legrand", correct as of 2026-08-17 19:15:37. For the first two months of the actual onboarding it was called `Lighting Showrooms`, and before 2026-06-18 `DefaultUserGroup`. Any historical read keyed on the current name will mis-file the June–August 2026 period. Corroborated by `login_events.user_group_name`, which stores the name at login time.
5. **`counts.price_levels: 5`** is correct and directly contradicts Kylor's own statement to the client of 2026-07-14 — > "On pricing; six levels are live: US Net, US Retail/MSRP, US iMAP, Canada Net, Canada iMAP, Canada MSRP." Six only if you count `products.net_price` as a level. He corrected himself on 2026-08-17. Recording it because the client was told six.

One more, not a contradiction but a correction of the handoff's own framing: *"153 Library items and 6 iPad report formats — the richest configuration in the whole test set. Something substantial was built here recently."* The 153 library items are recent (146 of them created 2026-06-22 → 2026-08-18). **The 6 iPad report formats are not** — all created 2025-06-11 → 2025-06-19, last edited 2025-12-12, i.e. pre-sales demo artefacts.
