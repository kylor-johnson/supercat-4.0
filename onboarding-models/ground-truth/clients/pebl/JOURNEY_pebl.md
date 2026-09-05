# JOURNEY — Skyard Furniture Co Ltd. (Pebl) · `pebl` · org 275

**Built blind** from `CORPUS_pebl.md` (read start to finish, in full) + `RAWSTATE_pebl.json`
+ live read-only SQL against `supercat-postgres-vpn`.
**No forbidden file was opened.** See "Compliance" at the end.
**Snapshot date:** 2026-08-25. DB queries run 2026-08-25.

---

## Narrative

Skyard Furniture Co Ltd. sells outdoor furniture out of Foshan, Guangdong under the brand
Pebl (and a second brand, BLOO, plus a `skyard-outdoor.com` identity). The org was
provisioned 2025-07-24 and SuperCat's own CTO, Brent Sanders, loaded a collection-level
catalogue shell in the first week of August 2025 — 84 rows, every one priced at $0.00. Then
the project went quiet for five months while Pebl implemented a Chinese ERP. Between
2025-09-11 and 2026-03-31 the entire client-side footprint is fourteen logins by two people.

A Discovery Call on 2025-12-10 restarted it. Jon Vanderberg set a plan: ERP data done by
end of 2025, import in January, reps added by end of January, "March 2nd, Full Go-Live" and
CIFF Guangzhou on 18 March. None of that happened. Kylor Johnson picked the account up on
2026-01-24 and started over from a 76-row Haven & Wave spreadsheet. Chinese New Year took
February. CIFF passed unremarked by either side — there is no email anywhere in the corpus
acknowledging the missed date.

The project genuinely began on 2026-03-31, when Mandy Mai — a coordinator who had joined the
conversation only in January and told Jon on the call *"I have no idea, no idea how we should
start for the eCat system"* — sent her own product file, having failed to import it twice.
Kylor found five separate CSV defects, fixed them, and from that point Mandy took the build
over. She fought images for a month (they were being stored with doubled `.jpg.jpg`
extensions while every import logged clean, and separately she could not reach the servers
from China without a VPN), then learned the three-file options model, then the Option Mapping
cascade, and by 2026-06-06 was writing: *"for the option mapping for the new collections, I
have managed them by our side."* Along the way she solved multi-currency herself with ad-hoc
price levels.

The whole build was aimed at one date: SPOGA+GAFA, Cologne, 22–26 June 2026. Her stated
priority, in capitals, was not order entry — it was emailing product information to strangers
at a booth. The blocker turned out to be that iPads had no Mail account configured. Fixed
2026-06-08. Six rep accounts went in on 2026-06-04, six more on 2026-06-25 *during* the fair.
June 2026: 373 logins, 16 users, 10 devices, 83 orders. It worked. *"the feedback of our ecat
system from Spoga is quite good ! Our sales team is very happy about this system."*

Customers were imported 2026-07-01, user groups built, and on 2026-07-17 Kylor handed the
account to Kyla Bosch. Mandy declined formal training in favour of the video library. Then,
between 2026-07-28 and 2026-07-30 — with no ticket, no email, no trace in the corpus — Mandy
destroyed ten user accounts, dissolving most of the export sales team that had just used the
tool at SPOGA, and re-imported all 171 customers with empty territory codes. Since then the
org has been rebuilding around a different market: domestic-China user groups, three
distributor groups with no customer list at all, CNY price levels, and on 2026-08-13 an iPad
report format named "Furniture China 2026 Shanghai - Internal Reference." Eight of the
thirteen price levels now on the account were created on 2026-08-19 and have never been used.

Orders went 83 → 5 → 1. Logins went 373 → 125 → 85. Those two numbers say different things,
and the second one is closer to the truth: this client is not decaying, it is between fairs.

---

## A. Cast

Roles are inferred from behaviour and from how people are addressed; where a role is a guess
it says so. "First/last appearance" spans corpus and DB.

### Client — Skyard Furniture Co Ltd. / Pebl / Skyard Outdoor

| Person | Email | First appearance | Last appearance | Role & notes |
|---|---|---|---|---|
| **Mandy Mai** | `sales04@peblfurniture.com` | 2026-01-14 (email quoted in HS #13857) | 2026-08-24 (iPad login) | The project. Joined as a newcomer in Dec 2025, became sole admin and builder. Account created 2026-02-05, first login 2026-02-06. **173 logins in June 2026 alone**; 27 in Aug 1–24. 25 orders. Group: DefaultUserGroup → Peblers → **Pebl Managers** (2026-07-01). Performed the 2026-07-28→30 account purge. |
| **Trista Qiu** | `sales07@peblfurniture.com` | 2025-08-08 (first client login ever) | 2026-08-10 (login) | Original client contact; on the 2025-12-10 call. Account 2025-08-04. Carried the account solo through the dormancy (logins 2025-09-11, 10-20, 12-10, 2026-01-13). **0 orders.** Deliberately given no customer access from 2026-07-02. |
| **Vincent Lee** | `vincent@peblfurniture.com` | 2025-12-10 (named on call; cc'd on Jon's 2025-12-11 summary) | 2026-08-21 (login) | Owner / decision maker. Account 2026-06-04. Admin. 1 order. Group: Pebl Managers. |
| **Priscilla Huang** | `sales01@skyard-outdoor.com` | 2026-06-11 (first login) | 2026-08-24 (login) | Manager. Account 2026-06-04. 4 orders — including the **only** post-go-live order against a real customer record (Maldives resort, 2026-08-13). Note the `skyard-outdoor.com` domain: not an anomaly, a second corporate identity. |
| **Tom De Wulf** | `tomdewulf@peblfurniture.com` | 2026-06-11 (first login) | 2026-08-21 (login) | Manager, Europe-facing (his one large order is a Montenegro buyer). Account 2026-06-04. 3 orders. Moved DefaultUserGroup → Peblers → Pebl Managers → **Pebl sales oversea** (2026-08-05). |
| **Marly Mai** | `sales06@peblfurniture.com` | 2026-06-15 (account created) | 2026-07-30 (login) | Rep. **10 orders / $251,592 — highest client value of any user**, all on 2026-06-25, all one buyer (Esun International). **Account removed** in the 2026-07-28→30 purge. |
| **Rita Luo** | `sales15@peblfurniture.com` | 2026-06-11 (first login) | 2026-07-15 (login) | Rep, territory code `rita`. Account 2026-06-04. 21 orders, **all on 2026-06-21** — 17 of them with product-set names as the buyer (see §E-B). Account still exists; dormant since 2026-07-15. |
| **Daria Wei** | `sales13@peblfurniture.com` | 2026-06-11 (first login) | 2026-07-01 (login as `dariawei`) | Rep, territory code `daria`. 4 orders 2026-06-21. **Her account record was reassigned** — from 2026-08-07 the same `org_users` row logs in under username `sales01`. Daria herself has not appeared since 2026-07-01. |
| **Wisteria Wong** | `sales11@peblfurniture.com` | 2026-06-25 (account created, during SPOGA) | 2026-07-22 (login) | Rep. 7 orders (Everything Under The Sun ×6, Ocean Import & Export ×1 — Qatar). **Account removed.** |
| **Theresa To** | `sales05@peblfurniture.com` | 2026-06-25 (account created) | 2026-07-17 (login) | Rep. 5 orders, all 2026-06-30. **Account removed.** |
| **Joe Ouyang** | `sales08@peblfurniture.com` | 2026-06-25 (account created) | 2026-06-30 (login) | Rep. 2 orders. **Account removed.** |
| **Dawn Zeng** | `sales03@peblfurniture.com` | 2026-06-25 (account created) | 2026-07-02 (login) | Rep. 1 order. **Account removed.** |
| **Annie Xie** | undetermined (`sales10@` or `sales16@`) | 2026-06-30 (first login) | 2026-07-09 (login) | Rep. 15 logins, **0 orders**. Named in Kylor's 2026-07-01 rep list. **Account removed.** |
| **Gavin Lai** | undetermined (`sales10@` or `sales16@`) | 2026-06-25 (first login) | 2026-07-23 (login) | Rep. **27 logins, 0 orders** — the most engaged non-ordering user. **Account removed.** |
| **Arne Martijn Malfait** | `arne@peblfurniture.com` | 2026-06-17 (account created; 1 login same day) | 2026-06-17 | Never used it. Flagged by Kylor 2026-07-01 as having no territory; Mandy replied *"Arne and Trista, they do not need to see any customer."* **Account removed.** |
| **"jojo"** | `jojo@peblfurniture.com` | 2026-07-24 (account created) | 2026-08-05 (login) | Domestic-China sales. 8 logins. Moved Pebl Managers → Pebl sales domestic on 2026-08-05. |
| **"salescn01"** | `info.cn@peblfurniture.com` | 2026-08-05 (account created) | 2026-08-24 (login) | Domestic-China sales. 11 logins in 3 weeks — currently the third most active user. |
| **"harson"** | undetermined (`doc@` or `sales01.cn@`, both created 2026-07-22) | 2026-07-28 (first login) | 2026-07-29 (login) | Domestic-China sales. 3 logins. **Account removed within days.** |

### Distributors / partners given their own user groups

| Person | Email | Group created | Activity |
|---|---|---|---|
| **Cenk Kirbeyi** | `ckirbeyi@ica.com.tr` | `ICA` — 2026-07-22 | 11 logins 2026-07-23/24; 2 orders ($54,515) with buyer names "Test_02" and "Test". Never filed a ticket. |
| **"arian"** | `eltecul@hotmail.com` | `ETC` — 2026-07-30 | 4 logins 2026-08-05/06; 12 order-submission audit events on 2026-08-05/06, **none of which persisted as an order row**. Never filed a ticket. |
| — | `info@sezondekor.com` | `Albania-Sezon Dekor` — 2026-08-10 | 1 login 2026-08-11; 0 orders. Never filed a ticket. |

All three groups have `customer_synching = 'n'` — **no customer list at all**. That is
deliberate: these are distributors who write against locally-created buyers. It answers the
handoff's question about why a company this size has six user groups.

### SuperCat

| Person | Email | First appearance | Last appearance | Role |
|---|---|---|---|---|
| **Brent Sanders** | `brent@supercatsolutions.com` | 2025-07-24 (account, same day as org) | 2026-02-28 (login) | CTO. Built the entire 2025 catalogue shell himself (logins 2025-08-01 → 08-08, imports 2025-08-01 → 09-06). Praised on the call: *"Brent is so good."* Offered as cover 2026-06-18. |
| **Jon Vanderberg** | `jon@supercatsolutions.com` | 2025-12-10 (Discovery Call) | 2026-07-20 (named by Kyla as rep-training owner) | Sales / exec sponsor. Ran the only call and wrote the only project plan. **No evidence he ever scheduled the rep training.** |
| **Kjael Skaalerud** | `kjael@supercatsolutions.com` | 2026-01-19 (HS #13857) | 2026-06-05 (cc'd by Mandy when escalating) | CEO. Account 2026-01-07, **never logged in**. Redirected the client to `onboarding@`. |
| **Kylor Johnson** | `kylor@supercatsolutions.com` / `onboarding@` | 2026-01-24 (HS #13879) | 2026-07-20 | Onboarding owner 2026-01-24 → 2026-07-17. Out of office 2026-06-18 → 06-23 (wedding). Test account `kylor22johnson@gmail.com` — 6 orders, **excluded from all client adoption counts below**. |
| **Kyla Bosch** | `kyla@` / `support@supercatsolutions.com` | 2026-06-18 (named as cover) | 2026-07-21 | Head of Support; signs as "Onboarding & Implementation Manager". First client-facing message 2026-06-23. Took ownership 2026-07-20. |
| — | `chuck+u@`, `chuck+superadmin@supercatsolutions.com` | 2025-11-12 (accounts) | never | Internal accounts, zero logins. |

**Role changes worth recording:** the default user group was renamed twice — `DefaultUserGroup`
→ `Peblers` (~2026-06-24) → `Pebl sales oversea` (2026-07-22). A 2026-06-17 login event for
Rita Luo records her group as **`ZEBRA GROUP`**, which together with the deleted price level
`zebra sales price in dach` shows this org was provisioned from another client's template and
has been de-templated in stages.

---

## B. Phase transitions

### → Phase 1 complete (Discovery / Kickoff) · 2025-12-10 · confidence: high

**What changed:** A 45-minute Discovery Call put a named owner, a named blocker (ERP
implementation) and a hard deadline (CIFF Guangzhou) on the record for the first time.

**Evidence:**
- [CALL, 2025-12-10T12:45+00:00, Jon Vanderberg (SuperCat) → Mandy Mai / Trista Qiu]
  > "we're almost, well, got, so end of this year, you're going to have your data ready, correct?"
- [CALL, 2025-12-10, Mandy (Pebl furniture)]
  > "Yes.    And we want to use the eCat in March."
  > "Yeah, in CIFF Fair in Guangzhou.    So we need to, yes, in March, before March."
- [HS #13857 quoting jon@supercatsolutions.com, 2025-12-11 01:03:33]
  > "March 2nd, Full Go-Live"
- [DB] `login_events`: `tristaqiu` logged in on 2025-12-10 — the day of the call.
- [DB] `ipad_reports`: "Organization Tearsheet" created 2025-12-10.

**Against:** A defensible earlier date exists. The org was created 2025-07-24T22:56:11, Brent
Sanders' account the same day, and by 2025-08-08 a catalogue was loaded and a client user
(Trista) had logged in — arguably kickoff already happened in August 2025. I date the phase to
2025-12-10 because the August work was a SuperCat-side demo build (84 collection-level rows,
**all priced $0.00**, since fully soft-deleted) with no client plan, no owner and no deadline.
Both dates are in the record; a framework that picks 2025-07-24 or 2025-08-01 is not wrong,
just measuring something else.

---

### Phase 1 → 2 (Initial Import) · 2026-01-24 · confidence: high
*(with a technically-earlier date of 2025-08-01 — see Against)*

**What changed:** A real, priced product file for real Pebl SKUs was mapped and imported.

**Evidence:**
- [HS #13879, 2026-01-24T21:08:51, kylor@supercatsolutions.com]
  > "I've already imported the translated file into your&nbsp;eCat Admin Console so&nbsp;you can see how everything looks."
- [HS #13879, 2026-01-24T21:08:51, kylor@supercatsolutions.com]
  > "Our last import activity was in September 2025, and we paused because we needed to align on how Options should be structured for your products."
- [DB] `products`: 372 rows with numeric ERP item codes (e.g. `302010072`) have
  `last_modified_at` starting **2026-01-24**. All are now soft-deleted.
- [DB] `import_events`: a Products import on 2026-01-24, warning tier.

**Against:** The first Products import on this org is 2025-08-01T16:47:43 (warning tier), and
a second on 2025-09-06. So "has at least the products file been imported?" was literally true
from 2025-08-01. But that generation was 84 collection-level rows — `DEC_DECK_SLIM`,
`SUN_SUNSET_LOUNGE`, `ALB_ALBATROS_ORGANIC` — with `net_price = 0.00` on every single row,
`trade_name_code` values like `TN1` and `collection_code` values like `COL20`. It was a shell,
not a catalogue. **This is a genuine two-answer transition and the framework's answer will
depend entirely on whether "imported" means "the file parsed" or "the catalogue exists."**

---

### Phase 2 → 3 (Progress) · 2026-04-02 · confidence: high

**What changed:** Options, option groups and products were all in, all non-fatal, on the same
day — the three-file model was working for the first time.

**Evidence:**
- [HS #13879, 2026-04-02T00:59:31, kylor@supercatsolutions.com]
  > "Imported options file (19 options: 3 frame colors, 9 material colors, 7 fabrics)Imported option groups file (3 groups organizing the options)Imported products file (44 unique products)All imports successful! ✓"
- [DB] `import_events` 2026-04-02: `Options` at 00:18:09 (clean, empty error list),
  `Option Groups` at 00:22:09 (clean), `Products` at 00:25:09 and 00:30:08 (warning tier —
  missing-custom-field notices only).
- [DB] `organizations.imports_options = true`; `option_type_labels` = `Frame Color` /
  `Material Color` / `Cushion Fabric`, exactly as Kylor described setting them on 2026-04-02.

**Against:** None. This is the cleanest transition in the record. Note it required Kylor to
enable "Imports Options?" and to renumber collection/category codes from the template values
(`COL3`, `COL5`, `CAT1`, `CAT2`) to real ones — i.e. progress was gated on undoing template
provisioning, not on client data.

---

### Phase 3 → 4 (Catalog Completeness) · two dates · confidence: medium

**4a — pilot catalogue buildable: 2026-04-28**

**What changed:** Images displayed on an iPad for the first time. Until this day the
catalogue existed in the console and was blank on the device.

**Evidence:**
- [HS #13879, 2026-04-28T07:08:59, sales04@peblfurniture.com]
  > "Finally I made it !!!!!"
  > "I tried to use the VPN and all the photos are displayed now."
- [DB] `import_events` 2026-04-28 04:18:33, Option Images, `:information` (clean):
  > 'The following images were imported: latte_ro6.jpg, sandb_cer.jpg, graph_cer.jpg, mocha.jpg, grey_cer.jpg, dkgrey_ro6…'
  — the same swatches that had imported on 2026-04-10 as `latte_ro6.jpg.jpg`,
  `sf090.jpg.jpg`, `mocha.jpg.jpg`. See §E-D.

**4b — full line buildable: 2026-06-17**

**Evidence:**
- [HS #14637, 2026-06-17T00:31:18, kylor@supercatsolutions.com]
  > "You now have 687 active products across all your collections, with images loaded and options configured."
- [DB] `products`: 713 active today, 690–704 with images depending on definition; 80 trade
  names, 94 collections, 24 categories; 151 options across 382 option groups.

**Against 4a:** The catalogue was 44–76 products of a multi-thousand-SKU line, and the option
cascade was still wrong (fixed 2026-05-08, re-broken 2026-05-11, re-fixed 2026-05-12).
**Against 4b:** On 2026-06-03 Kylor recorded that 124 new-collection rows had been imported
with placeholder option groups cleared, i.e. *"browse-only"*, and on 2026-06-17 he was still
listing option-group errors and a missing OptionSet2→OptionSet3 mapping. "Buildable" was true;
"complete" was not, and arguably still isn't.

---

### Phase 4 → 5 (Reps Signed In) · 2026-06-11 · confidence: high

**What changed:** Reps other than the admin logged into iPads.

**Evidence:**
- [DB] `org_users`: five client accounts created 2026-06-04 — `vincent@`,
  `sales01@skyard-outdoor.com`, `sales13@`, `sales15@`, `tomdewulf@`.
- [DB] `login_events` June 2026: first logins on **2026-06-11** for `ritaluo`, `tomdewulf`,
  `priscillahuang`, `dariawei`. June totals: **373 logins, 16 distinct users, 10 devices.**
- [HS #14637, 2026-06-17T00:31:18, kylor@supercatsolutions.com]
  > "The team has been actively importing and syncing — I can see Mandy, Marly, Trista, Vincent, and Priscilla all logging in regularly."
- [DB] `login_events`: six more accounts first appear 2026-06-25 — `marlymai` (in Peblers),
  `gavinlai`, `wisteriawong`, and on 2026-06-30 `theresato`, `anniexie`, `Joeouyang`,
  `dawnzeng`. Six rep accounts were **created on 2026-06-25, during SPOGA**.

**Against:** Nothing argues against the fact. What argues against reading it as durable
adoption: of the 14 client users who ever logged in, **nine no longer have accounts**, and
two of the most engaged (Gavin Lai, 27 logins; Annie Xie, 15) never wrote a single order.

---

### Phase 5 → 6 (Admin Training) · split answer · confidence: high on the facts

**Formal admin training: never happened.** Date of the decision: **2026-07-21.**

**Evidence:**
- [HS #14801, 2026-07-20T16:24:17, kyla@supercatsolutions.com]
  > "If you'd like a walkthrough of the admin tools, I'm happy to set up a session. We'd cover platform orientation, user management, and data imports. That said, this is completely optional."
- [HS #14801, 2026-07-21T01:12:54, sales04@peblfurniture.com]
  > "We prefer to check the eCat Video Tutorials first, and we will reach out whenever we need help."
- [DB] `Fathom` corpus manifest: **1 call, 2025-12-10.** No call exists after Discovery. No
  training session was ever recorded.
- Rep training was assigned to Jon — [HS #14801, 2026-07-20T16:24:17, kyla@]
  > "Separately, Jon will be reaching out to schedule a hands-on session with your sales team covering syncing, browsing products, creating presentations, and placing orders."
  No evidence in corpus or DB that it occurred.

**Functional admin competence: achieved ~2026-06-06.** confidence: high.

**Evidence:**
- [HS #13879, 2026-06-05T09:46:36, sales04@peblfurniture.com]
  > "Just want to let you know that I already know how to manage the Library and Smart List."
- [HS #13879, 2026-06-06T10:03:49, sales04@peblfurniture.com]
  > "Just want to let you know, for the option mapping for the new collections, I have managed them by our side."
- [HS #14637, 2026-06-18T13:10:25, sales04@peblfurniture.com]
  > "Important note: Everything regarding to the products / option mappings, I will manage from our side. (For now, everything should be OK )"
- [HS #13879, 2026-07-01T07:17:56, sales04@peblfurniture.com]
  > "I found a way to handle multiple currencies - using Ad-Hoc price levels with pre-calculated prices in the CSV import. I've already tested importing CNY prices and it works perfectly."
- [DB] `price_levels`: `cny_retail`, `pl_type = 'ad-hoc'`, `currency_code = 'CNY'`, **created
  2026-07-01** — the client's self-taught solution, corroborated to the day.
- [DB] `smart_stacks`: "SPOGA 2026" created 2026-06-05, i.e. the same day she said she'd
  learned Smart Lists.
- [DB] `audit_log_entries`: 19 `OrgUser updated`, 12 `user group updated`, 11 `OrgUser
  destroyd` and 5 `OrgUser created` events in July 2026, all attributed to org_user 152538
  (Mandy). She runs user administration unassisted.

**Against:** "with ongoing operations covered" is only partly true. Two operational areas were
raised and never closed: **inventory** (offered 2026-06-17, never answered — `inventories` has
0 rows and no inventory file has ever been imported) and **ERP order export** (the entire
premise of the Discovery Call — `organizations.export_type` is empty and
`stdjson_export_url` is null; no integration was ever built).

---

### Phase 6 → 7 (Go-Live) · 2026-07-17 · confidence: high

**What changed:** Formal handoff from onboarding to support, accepted by the client.

**Evidence:**
- [HS #14800, 2026-07-17T16:37:04, kylor@supercatsolutions.com]
  > "I did a full review of your Pebl account, and it's in really good shape — honestly, one of the smoother rollouts we've seen"
  > "Everything looks good on my end, so I'd like to introduce you to&nbsp;Kyla, our Head of Support&nbsp;(copied here)."
- [HS #13879, 2026-07-08T18:03:57, kylor@supercatsolutions.com] — the pre-handoff readiness call:
  > "Products, images, options, customers, rep assignments, and user groups are all set up and looking clean. You're genuinely ready to go live with your team."
- [HS #14800, 2026-07-18T02:41:45, sales04@peblfurniture.com]
  > "We don't have any new requests at the moment, but we'll be sure to reach out to Kyla when something comes up."
- [HS #14801, 2026-07-20T16:24:17, kyla@supercatsolutions.com]
  > "Kylor did a wonderful job getting you through onboarding, and I'm glad to officially take things from here."
- [DB] Ongoing activity after handoff: 85 logins by 10 users in 2026-08-01→24; last login
  2026-08-24; latest Products import 2026-08-07; latest Images import 2026-08-07; new iPad
  report formats 2026-08-13; new price levels 2026-08-19.

**Against — and this matters.** Two of the five things Kylor listed as "set up and looking
clean" were undone within three weeks, by the client:
- [DB] All 171 `customers` rows were re-created on **2026-07-30 07:48** with
  `territory_codes = '[]'`. The rep↔customer assignment described on 2026-07-01 no longer
  exists. Only two surviving users hold any territory code (`daria`, `rita`), and no customer
  matches either. The user group "Pebl sales oversea" (9 users) has
  `customer_synching = 'o'` (associated only) — **so those nine users currently sync zero
  customers.**
- [DB] `audit_log_entries`: 11 `OrgUser destroyd` events, 2026-07-02 (×1), 2026-07-28,
  2026-07-29, and eight between 2026-07-30 07:40:20 and 07:42:25 — all by org_user 152538.
  Ten client user records are now detached from the org.

Go-live happened. What went live is not what was handed over.

---

## C. Current phase as of 2026-08-25

**Phase 7 (Go-Live) satisfied, and the org is mid-reconfiguration for a different market.**
Confidence: high on activity, medium on what to call it.

**Evidence for "live and active":**
- [DB] `login_events` 2026-08-01→24: **85 logins, 10 distinct users, 7 devices**; most recent
  2026-08-24 by Mandy Mai, Priscilla Huang, `salescn01` and `sales01`.
- [DB] Latest imports: Products 2026-08-07 11:08 (warning), Images 2026-08-07 14:49 (clean),
  Customers 2026-07-30 07:48 (clean). Nothing fatal is outstanding.
- [DB] `products`: 713 active, 330 distinct net prices, no zero/$1.00 placeholders.

**Evidence for "reconfiguring toward Furniture China, Shanghai":**
- [DB] `ipad_reports`: **"Furniture China 2026 Shanghai - Internal Reference"** created
  2026-08-13 04:30, and "pebl quotation" (CSV shape) the same session.
- [HS #13879, 2026-07-01T07:17:56, sales04@peblfurniture.com]
  > "This means for our Shanghai exhibition in September, both our domestic (CNY) and export (USD) sales teams can use eCat side by side - they just switch the Price Level on the iPad."
- [DB] `user_types`: `Pebl sales domestic` created 2026-07-22; `ICA` 2026-07-22; `ETC`
  2026-07-30; `Albania-Sezon Dekor` 2026-08-10.
- [DB] `price_levels`: **8 of 13 created 2026-08-19** — six days before this snapshot.

**Evidence against calling it healthy steady-state:**
- [DB] `orders`: 83 (Jun) → 5 (Jul) → **1 (Aug)**. Last order 2026-08-13.
- [DB] `customers`: 171 rows, every one `default_price_code = 'fob'`, every one
  `territory_codes = '[]'`.
- [DB] `price_levels`: no order has ever used any level other than `fob` and `project`, and
  `project` **no longer exists**.

---

## D. Turning points

**1 · 2025-12-10 — the Discovery Call set a deadline nobody hit, and nobody mentioned again.**
Jon's plan ("March 2nd, Full Go-Live", CIFF Guangzhou 18 March) was overtaken by the ERP
build and Chinese New Year. On 2026-03-10 Kylor wrote *"Hey Mandy, I hope you enjoyed your
time off for the Chinese New Year!"* — eight days before CIFF — with no reference to the fair
at all. **The single most consequential fact about this project's first six months is a missed
date that appears nowhere in the correspondence.**

**2 · 2026-03-31 — Mandy takes the build over.**
> "I tried to import the data by myself twice, but failed. 😞" … "I want to know why and still want to try to do it by myself."
Kylor's reply diagnosed five defects (duplicate `Dimensions` header, bare `"` inch marks,
an empty column, non-standard field names, missing `TradeNameCode`) and pre-configured trade
names, collections, categories and custom fields. Everything after this date is client-driven.

**3 · 2026-04-28 — images finally render, after 18 days of a clean import log and a blank iPad.**
Two independent causes were in play and only one was named: doubled `.jpg.jpg` filenames on
the server (fixed by re-import at 04:18 that morning) and network reachability from Foshan
(*"I tried to use the VPN and all the photos are displayed now"*, 07:08). Until this day
nothing SuperCat had built was visible to the customer.

**4 · 2026-06-08 — the real SPOGA blocker was an empty iPad Mail account.**
Mandy, in capitals, on 2026-06-05:
> "THIS IS THE FIRST PRIORITY WE WANT TO SOLVE BEFORE SPOGA."
> "At this stage, eCat is more important for us to handle new inquiries during fairs, than our exiting clients."
Kylor, 2026-06-08:
> "I checked your Pebl account on our side —&nbsp;nothing is blocking Email Product Information. Your catalog and settings are fine. The issue is almost certainly that the&nbsp;iPad needs an email account configured in Apple Settings&nbsp;before eCat can open a product email."
Resolved 2026-06-09: *"Finally we fixed the problems of emailing function."* **The feature the
client cared about most was not a catalogue feature at all.**

**5 · 2026-07-28 → 2026-07-30 — the silent restructure.**
Ten user accounts destroyed, all 171 customers re-imported with empty territory codes, the
"Peblers" group renamed, and three distributor groups with no customer list created in its
place. Eleven days after SuperCat declared the rollout "one of the smoother rollouts we've
seen." **Not one word of this is in the corpus.** It is visible only in
`audit_log_entries`, `org_users`, `users` and `customers`.

---

## E. The five questions the phase model does not ask

### A. Did this client ever go backwards?

**Yes — three times, and the largest one is invisible to every phase question.**

**A1 · Dormancy, 2025-09-06 → 2026-03-31 (roughly seven months).**
- [DB] `import_events`: one Products import in 2025-09, then **nothing at all until 2026-01-24.**
- [DB] `login_events` by month: 2025-09 = 1, 2025-10 = 2, 2025-11 = 1, 2025-12 = 1,
  2026-01 = 1, 2026-02 = 5, 2026-03 = 2. Fourteen logins in seven months, by three people.
- Trigger: the ERP build. [CALL, 2025-12-10, Mandy] *"Now we are still in the stage of
  inputting the datas into the ERP, and we are doing some adjustment on the ERP system."*
  Compounded by [HS #13879, 2026-02-17T08:44:50, sales04@] *"I am in Chinese New Year holiday
  and will resume to work on February 24."* and by SuperCat-side latency — [HS #13879,
  2026-02-03T18:33:59, kylor@] *"I am so sorry for the delay here - I wasn't cc'd on your
  reply above and just recently got assigned to our formal onboarding inbox."*
- Ended by the client, not by SuperCat: Mandy's unprompted 2026-03-31 file.
- **The CIFF Guangzhou go-live was lost inside this window and neither party acknowledged it.**

**A2 · Self-inflicted regression, 2026-05-11.**
[HS #13879, 2026-05-11T12:24:50, sales04@peblfurniture.com]
> "the options mapping doesn't work any more. Even I can't check this function in the Admin Sole. It tells "an internal error has occurred""
Root cause was a process failure on SuperCat's side — [HS #13879, 2026-05-12T18:58:57, kylor@]
> "I'm sorry for the confusion caused by my delay in sending you the updated files. I should have shared them with you directly rather than having you work from the originals."
Recovered within a day. Notable because the Admin Console page itself threw an error while the
underlying Products import was only warning-tier.

**A3 · The post-go-live restructure, 2026-07-28 → 2026-07-30. The big one.**
- [DB] `audit_log_entries`, event `OrgUser destroyd`, actor org_user 152538 (Mandy):
  2026-07-02, 2026-07-28 01:35:42, 2026-07-29 02:47:51, then eight in 122 seconds between
  2026-07-30 07:40:20 and 07:42:25.
- [DB] `users` ↔ `org_users`: ten client accounts now have zero org rows — `sales03@`
  (Dawn Zeng), `sales05@` (Theresa To), `sales06@` (Marly Mai), `sales08@` (Joe Ouyang),
  `sales10@`, `sales11@` (Wisteria Wong), `sales16@`, `arne@`, `doc@`, `sales01.cn@`.
  Between them these people accounted for **25 orders and $329,255.82** — a third of all
  order value on the account.
- [DB] `customers`: all 171 re-created 2026-07-30 07:48:08–09, `territory_codes = '[]'`.
- Effect: the export sales team that had just used eCat successfully at SPOGA no longer has
  logins, and the customer↔rep model Kylor built on 2026-07-01 no longer exists.
- Almost certainly not churn — it reads as a deliberate pivot from the export team to a
  domestic-China team plus named distributors, timed for the September Shanghai fair. But it
  is a *regression against the delivered configuration*, it happened days after handoff, and
  no one at SuperCat has any record of it.

**Did they nearly churn? No.** Nothing in the record suggests it. The engagement tone runs the
other way throughout — *"You've been incredibly helpful, and it's been a pleasure working with
you"* (2026-07-18), and the account is still being actively built on 2026-08-24.

---

### B. Adoption — separate from go-live

**`kylor22johnson@gmail.com` is excluded from every client figure below** (SuperCat test
account: 6 orders, $25,800, buyer name "Test", all on 2026-06-09, 5 logins).

**Headcount and activity**

| Month | Logins | Distinct users | Devices | Orders (client) | Order value (client) |
|---|---|---|---|---|---|
| 2025-08 | 22 | 2 (Brent, Trista) | 3 | 0 | — |
| 2025-09 → 2026-03 | 13 | 3 | 3 | 0 | — |
| 2026-04 | 45 | 2 | 2 | 0 | — |
| 2026-05 | 115 | 2 | 3 | 2 | $34,010.00 |
| 2026-06 | 373 | **16** | 10 | 77 | $848,304.82 |
| 2026-07 | 125 | **18** | 8 | 5 | $85,431.78 |
| 2026-08 (to 24th) | 85 | 10 | 7 | 1 | $6,384.00 |

**Who actually wrote orders** (12 client users, 85 orders, $974,130.60):

| User | Orders | Value | Window |
|---|---|---|---|
| Mandy Mai | 25 | $409,760.00 | 2026-05-13 → 07-02 |
| Rita Luo | 21 | $46,096.00 | 2026-06-21 only |
| Marly Mai | 10 | $251,592.00 | 2026-06-25 only |
| Wisteria Wong | 7 | $27,800.00 | 2026-06-25 → 06-29 |
| Theresa To | 5 | $50,493.82 | 2026-06-30 only |
| Daria Wei | 4 | $4,459.00 | 2026-06-21 only |
| Priscilla Huang | 4 | $12,180.78 | 2026-06-21 → 08-13 |
| Tom De Wulf | 3 | $66,584.00 | 2026-06-22 → 06-24 |
| Joe Ouyang | 2 | $10,080.00 | 2026-06-30 only |
| Cenk Kirbeyi (ICA) | 2 | $54,515.00 | 2026-07-23 → 07-24 |
| Dawn Zeng | 1 | $36,950.00 | 2026-06-30 only |
| Vincent Lee | 1 | $3,620.00 | 2026-06-12 only |

**Seven of those twelve wrote orders on exactly one day.**

**Who logged in and never ordered:** Trista Qiu (many sessions across a year), Gavin Lai (27
logins), Annie Xie (15), Arne Martijn Malfait (1), `jojo` (8), `salescn01` (11), `harson` (3),
`arian`/ETC (4), `sezondekor` (1).

**What they were doing — and why $999,930.60 is not $999,930.60.**
Only 3 of 91 orders carry a `customer_num`; the other 88 carry a `local_customer_code`, i.e.
a buyer typed into the iPad on the spot. That is not a self-test artefact and not naming
drift — it is the documented behaviour of on-device customers, and Kylor described it on
2026-07-08:
> "Customers a rep creates locally on the iPad stay on that device only — they don't sync back to the server or appear on other iPads."

Classifying all 91 orders by buyer name reconciles exactly to the total:

| Class | Orders | Value | Share |
|---|---|---|---|
| Internal / test buyer names — "Pebl" (25), "Test" (11), "Skyard" (10), "Test_02", "Joe", "dsbs", "Pebl(Rita)" | 51 | **$582,004.60** | 58.2% |
| Product-set names used as the buyer — "Wave Set", "Riposo Teak Set", "Newport Set", "Haven Teak Set", "Tolo Teak Set", "Orbit Set", "Noon Set", "Riposo Alu Set", … (all Rita Luo, all 2026-06-21) | 17 | **$36,646.00** | 3.7% |
| Plausible third-party trade buyers — Esun International ($251,592), Montenegro ($54,206), Gescova Outdoor Furniture ($28,920), Everything Under The Sun ($18,000), Tbs ($12,378), Ocean Import & Export ($9,800), A A Ethere Madivaru ($6,384) | 23 | **$381,280.00** | 38.1% |
| **Total** | **91** | **$999,930.60** | 100% |

Of that last group, only **3 orders / $35,304.00** are against a customer record that actually
exists in the database. Rita Luo's 17 "Set" orders are the clearest tell: she used the order
screen as a **bundle-pricing tool**, not to place orders — 17 orders averaging $2,155 in a
single day, each named after the product set being priced.

**Four order-header facts settle the interpretation.** Across all 91 submitted orders:

| Check | Result |
|---|---|
| `customer_po_num` populated | **0 of 91** |
| `ship_date` populated | 6 of 91 |
| `customer_email_address` populated | 47 of 91 |
| `is_exported` / `to_export` | **false / false on all 91**; `sum(num_failures) = 0` |

Not one order on this account carries a customer PO number, and not one has ever been queued
for or sent to an ERP. Combined with `organizations.export_type = ''` and
`stdjson_export_url = NULL`, that is conclusive: **these 91 records are quotations,
configurations and demonstrations. None of them is a booked purchase order.** The
$999,930.60 in `RAWSTATE_pebl.json` is a true sum of `orders.total` and a misleading measure
of commercial activity; it should never be cited as revenue, pipeline, or GMV.

**So: adoption of eCat as a catalogue and quotation tool is real and continuing. Adoption of
eCat as an order-entry system barely happened.** Which is exactly what the client said it
wanted on 2026-06-05, in capitals.

---

### C. Current trajectory

**Cycling, not decaying — with one real risk.** Confidence: medium-high.

**Improving / active:**
- 85 logins by 10 users in 24 days; most recent 2026-08-24, the day before snapshot.
- 52 clean Images imports in August 2026 — the catalogue is still being enriched.
- Forward-looking build work dated 2026-08-13 (Furniture China Shanghai report format,
  "pebl quotation" CSV) and 2026-08-19 (eight new price levels).
- New user constituencies added after go-live: domestic China (2026-07-22, 07-24, 08-05) and
  three named distributors (2026-07-22, 07-30, 08-10).
- Zero support tickets since 2026-07-21 — and one thing that would have generated a ticket
  four months earlier did not: on **2026-08-05 07:01 and 12:51 the Products import failed
  fatal** with `undefined method 'downcase' for nil:NilClass` — the *identical* header defect
  Kylor diagnosed for her on 2026-03-31 — and she fixed it herself by 13:12 the same day. No
  email, no ticket. That is what real self-sufficiency looks like in the log.

**Decaying:**
- Orders: 83 → 5 → 1. The order-writing behaviour of June has not recurred.
- Distinct users: 16 → 18 → 10. Nine of the fourteen client users who ever logged in no
  longer have accounts.
- The two most-engaged non-ordering reps (Gavin Lai, Annie Xie) were removed.

**The risk, stated plainly:** the account currently has 171 customers with no territory codes,
9 users in a group set to sync *associated customers only*, and 8 brand-new price levels no
customer or order references. If the Shanghai fair is run the way SPOGA was — locally-created
buyers on `fob` — none of that matters. If anyone expects the customer list or the channel
pricing to work on an iPad in September, it will not.

---

### D. Was the catalog ever *wrong* while the imports looked *clean*?

**Yes. Twice, provably, and once for eighteen days.**

**D1 · Double-extension image filenames, 2026-04-01 → 2026-04-28.**
The importer accepted and logged as `:information` (clean) filenames that could never match
the `ImageFileName` values in `products.csv`:

- [DB] `import_events` 2026-04-01 04:03:35, Images, `:information`:
  > 'The following images were imported: Wave_coffee table_42x42cm_teak top_cha_1.jpg.jpg'
- [DB] `import_events` 2026-04-01 06:57:42, Images, `:information`:
  > 'The following images were imported: Wave chaise lounge_left_cha_1.jpg.JPG'
- [DB] `import_events` 2026-04-10 11:48:21, Option Images, `:information`:
  > 'The following images were imported: sf090.jpg.jpg, sf140.jpg.jpg, sandb_cer.jpg.jpg, sj131.jpg.jpg, sf163.jpg.jpg'
- [DB] `import_events` 2026-04-10 12:06:29, Option Images, `:information`:
  > 'The following images were imported: latte_ro6.jpg.jpg, mocha.jpg.jpg, mh1763.jpg.jpg, mh1764.jpg.jpg, dkgrey_ro6…'

Note the embedded spaces too — the very thing the client had been told to eliminate. Every
one of these imports is clean-tier. Meanwhile:

- [HS #13879, 2026-04-10T12:22:03, sales04@peblfurniture.com]
  > "Now I can use the filezilla for upload photos.
  > And it also shows all photos uploaded successfully.
  > But I still cannot see the photo in ipad. I already wait for more than 30mints."
- [HS #13879, 2026-04-22T06:49:09, sales04@peblfurniture.com]
  > "Today I tried several times one the ipad, but the images still not displayed."

Corrected 2026-04-28 04:18:33, when the same swatch set re-imported with single extensions
(`latte_ro6.jpg`, `sandb_cer.jpg`, `graph_cer.jpg`, `mocha.jpg`, `grey_cer.jpg`) — and
Mandy's *"Finally I made it !!!!!"* lands at 07:08:59 the same morning. **She attributed the
fix to a VPN; the DB shows the filenames were also genuinely wrong until that morning.** Both
causes were real, one was diagnosed, and neither was visible in the import tier.
*This is the cleanest example in the whole account of an import tier lying by omission.*

**D2 · A live catalogue with dead configurators, 2026-06-03 → mid-June.**
- [HS #13879, 2026-06-03T17:14:57, kylor@supercatsolutions.com]
  > "Four item numbers were used twice for completely different products (e.g.&nbsp;304010001 &nbsp;was both Haven neo teak sunlounger and Cloud tray-small). eCat requires every&nbsp;BaseItemCode &nbsp;to be unique, so the import stopped."
  and on the 124 new rows:
  > "Placeholder&nbsp;FRAMECOLOR &nbsp;/&nbsp;MATCOLOR &nbsp;/&nbsp;CUSHFABRIC &nbsp;cleared so they import as&nbsp;browse-only&nbsp;until your updated option-mapping spreadsheet is ready"
- [DB] June 2026 shows 45 warning-tier and 17 error-tier Products blocks and **15 error-tier
  Option Groups blocks** — the busiest and messiest month on the account, three weeks before
  the fair. A "products imported: warning" line says nothing about whether a rep could
  configure the product.

**D3 · A third case worth naming, though it is a configuration break rather than an import
lie:** on 2026-05-11 the Option Mappings admin page returned *"an internal error has
occurred"* while the concurrent Products import was warning-tier only.

**Also relevant to D, and not detectable from tiers at all:** the item-code scheme was
replaced wholesale. [DB] `products` shows three generations —
84 rows on prefix codes (`ALB_ALBATROS`) last touched 2025-08-04 → 2025-09-06;
372 rows on numeric ERP codes (`302010072`) 2026-01-24 → 2026-06-06;
839 rows on the current dashed scheme (`1-ORBIT-01-003`, `4-TOLOA-01-002`) from 2026-06-06.
**All 713 active products use the dashed scheme; not one numeric code survives.** A full
primary-key migration happened around 2026-06-06, sixteen days before SPOGA, and is not
mentioned anywhere in the corpus.

---

### E. Is anything priced as a placeholder?

**Not today. Yes in 2025. And the price levels people use are not the price levels that exist.**

**Product prices are real.**
- [DB] `products` (713 active): `min(net_price) = 3.00`, `max = 1579.00`, `avg = 263.35`,
  **330 distinct values**, and **zero** rows at `1.00` or `0.00`. No placeholder pricing.

**But the 2025 generation was entirely placeholder.**
- [DB] All 84 Gen-1 products (`DEC_DECK_SLIM`, `SUN_SUNSET_LOUNGE`, `ALB_ALBATROS_ORGANIC`,
  `BAY_BAY`, …), last modified 2025-08-04 → 2025-09-06, carry `net_price = 0.00`. All are
  soft-deleted. The catalogue that existed for the first five months of this org's life had
  no prices in it at all.

**The price-level mismatch — this is the live finding.**

| Fact | Evidence |
|---|---|
| Only two price levels have ever appeared on an order: `fob` (79 orders, $735,800.60) and `project` (12 orders, $264,130.00) | [DB] `orders` grouped by `price_level` |
| **`project` no longer exists** | [DB] `price_levels` for org 275 contains no `project` row |
| **8 of the 13 current levels were created 2026-08-19** — six days before snapshot | [DB] `price_levels.created_at`: `fob 1.05`, `online shop (1.1)`, `residential channel (2.0)`, `commercial channel (1.3)`, `hospitality channel (1.15)`, `end consumer (2.2)`, `commercial project owner (1.5)`, `hotel project owner (1.15)`, `cny_project` all = 2026-08-19 |
| **None of the 8 new levels has ever been used on an order** | [DB] `orders.price_level` ∈ {`fob`, `project`} only |
| **All 171 customers point at `fob`** — not one at a channel level | [DB] `customers.default_price_code` has exactly one distinct value: `fob` |
| The levels Kylor listed on 2026-06-30 are mostly gone | [HS #13879, 2026-06-30T18:32:08, kylor@]: *"Your options today:&nbsp;fob ,&nbsp;ahp ,&nbsp;project ,&nbsp;tmm ,&nbsp;suggested retail price ,&nbsp;zebra sales price in dach ."* — `ahp`, `project`, `tmm` and `zebra sales price in dach` have all been deleted |
| The org was provisioned from another client's template | `zebra sales price in dach` above, plus [DB] `login_events` 2026-06-17 records Rita Luo's `user_group_name` as **`ZEBRA GROUP`** |
| The CNY work is genuine and dated to the day | [DB] `price_levels`: `cny_retail`, `pl_type = 'ad-hoc'`, `currency_code = 'CNY'`, created **2026-07-01** — the same day Mandy wrote *"I found a way to handle multiple currencies - using Ad-Hoc price levels"* |

**Read:** the 13-level channel-pricing structure is six days old, arithmetic, unused, and
unreferenced by any customer. It looks like preparation for the September Shanghai fair (where
domestic CNY and export USD teams were to work side by side), not a live pricing model. The
handoff's guess that "330 distinct net prices so it is probably fine" is right about products
and wrong about levels: **the pricing risk on this account is not placeholder prices, it is
$264,130 of order history pointing at a price level that has been deleted.**

**Inventory — 0 rows, by design (by omission, strictly).**
- [HS #14637, 2026-06-17T00:31:18, kylor@supercatsolutions.com]
  > "Inventory (optional) — if you'd like reps to see stock levels on iPad, we'd need an inventory file. This can come later if it's not a priority."
- No reply on inventory appears anywhere in the corpus. [DB] `inventories` = 0 rows;
  `import_events` contains **no Inventory import in the org's entire history**. Offered once,
  never pursued, never blocked anything.

---

## Does the real story fit the seven phases?

**No. It fits them well enough to be scored, and badly enough that the score would mislead.**

1. **The shape is event-driven, not linear.** This project has no "steady state" to progress
   toward. It has fairs: CIFF Guangzhou (March 2026, missed), SPOGA Cologne (June 2026, hit),
   Furniture China Shanghai (September 2026, in preparation). Activity is 373 logins in the
   fair month and 13 logins across the preceding seven months. A phase model reads the gap as
   a stall and the spike as go-live; the client reads both as normal.

2. **"Go-Live" and "the client is getting value" are different events here.** Phase 7 fired
   on 2026-07-17. Order volume peaked *four weeks earlier* and has been ~1/month since. The
   value was delivered at SPOGA, before go-live was declared.

3. **The primary use case is not in the model.** The client's stated first priority was
   emailing product information and quotations to strangers at a booth — *"eCat is more
   important for us to handle new inquiries during fairs, than our exiting clients"* — and the
   blocker was an iPad Mail account, not anything eCat controls. Phases 2–4 measure catalogue
   completeness; nothing measures "can a rep email a stranger a spec sheet."

4. **Nothing measures catalogue *regeneration*.** Three catalogue generations, two full
   item-code migrations (2026-01-24 and 2026-06-06), 582 soft-deleted products. Every one of
   those events is invisible to "has the products file been imported."

5. **Nothing measures post-go-live regression.** The single largest event after handoff — ten
   accounts destroyed, all territory codes wiped, the pricing model replaced — moves no phase
   and generated no ticket. A framework run on this account today would report Phase 7,
   healthy, and be describing a configuration that no longer exists.

6. **"Admin Training" has no true/false answer here.** No training session was ever held; the
   admin is nonetheless one of the most capable this account will see, self-diagnosing a fatal
   CSV header error on 2026-08-05 that had needed SuperCat's help in March. Phase 6 is either
   never satisfied or was satisfied without the activity it names.

---

## Compliance (per "Before you finish")

1. **Every transition has a date and evidence, or an explicit split/undetermined.** Phases
   1, 2, 3, 5, 7 are dated with high confidence. Phase 4 is given two dates (4a/4b) because
   "buildable" and "complete" separate by seven weeks. Phase 6 is split: formal training
   **never happened** (decision dated 2026-07-21), functional competence dated ~2026-06-06.
   Items I could not date are recorded as `undetermined` in `GAPS_pebl.md`, not guessed.
2. **Every quote is verbatim**, with source, author and timestamp. HTML entities (`&nbsp;`)
   and typos (`filr`, `Admin Sole`, `30mints`, `Kyler`) are reproduced as they appear in the
   corpus. Nothing is paraphrased inside quote marks.
3. **I read the whole corpus, start to finish — not a skim.** All 4,916 lines. The only
   passages I did not re-read line-by-line are blocks that are verbatim re-quotes of text
   already read earlier in the same thread (Chinese-client mail clients quote the full prior
   message; e.g. lines 2350–2382, 3567–3649, 3847–3958, 4264–4338). I verified by heading
   index that no unique message sits inside those ranges.
4. **Forbidden files: none opened.** I did not read `pebl/CLIENT_PROFILE.md`, `pebl/HANDOFF.md`
   or any other `pebl/*.md` note, `eCat_Onboarding/REGISTRY.yaml`, any
   `onboarding-models/*.md` framework document (`Phase_Anchors`, `Phase_Progression_Framework`,
   `Flags_and_Signals`, `Output_Contract`, `RUN_PROMPT`), `overrides.yml`,
   `ground-truth/SCORECARD.md`, or any other client's `JOURNEY_*.md`, or any `ecat-*` skill
   describing phase meanings. I listed `pebl/_ground_truth/` (filenames only) and read exactly
   two files there: `CORPUS_pebl.md` and `RAWSTATE_pebl.json`. The workspace `CLAUDE.md` was
   auto-loaded into context by the harness before I received the task; it is not on the
   forbidden list and contains no phase definitions.
5. **`kylor22johnson@gmail.com` is excluded from all client adoption counts** and its
   contribution stated separately wherever it would otherwise inflate a figure (6 orders,
   $25,800, all 2026-06-09, buyer name "Test", 5 logins).
6. **Contradictions with `RAWSTATE_pebl.json` are flagged**, not smoothed. Four of them —
   user count, image coverage, order-value interpretation, and August order submissions — are
   itemised in `GAPS_pebl.md` §Contradictions.
