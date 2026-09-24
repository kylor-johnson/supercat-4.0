# GAPS — Skyard Furniture Co Ltd. (Pebl) · `pebl` · org 275

Companion to `JOURNEY_pebl.md`. Everything here is what I *could not* establish, what would
establish it, and where the sources disagree. Snapshot 2026-08-25.

---

## 1. Ticket de-duplication — 8 ticket IDs are 4 conversations

Collapsing on subject with `Re:` / `Fwd:` / `FW:` / `回复:` stripped:

| Real conversation | Ticket IDs | Messages | Note |
|---|---|---|---|
| "Summary of our meeting" | #13857 (B), #13859 (B) | 2 | Two tier-B captures of the same chain; #13859 quotes #13857 in full |
| "Assistance with eCAT System – Getting You Up to Speed" | #13879 (A) | ~66 | The spine of the project, 2026-01-24 → 2026-07-08 |
| "EBL / eCat Check-In — Post-SPOGA + Next Steps" | #14637 (A), #14656 (B) | 9 + 2 | #14656 is a byte-identical double-capture of two #14637 messages |
| "Pebl eCat — you're in great shape; introducing Kyla…" | #14800 (A), #14801 (A), #14815 (B) | 4 + 6 + 3 | Same conversation captured three times: client mailbox, `onboarding@`, `support@` |

**So: volume is not evidence of engagement here.** 8 tickets → 4 conversations, and one of
those four (#13879) carries the entire onboarding. Anyone counting tickets to infer effort or
friction on this account will over-count by 2×.

### Tier B tickets — what I kept and what I discarded

| Ticket | Verdict | Why |
|---|---|---|
| **#13857** (2026-01-19, `kjael@`) | **Kept — essential** | Its quoted body is the only surviving copy of Jon Vanderberg's 2025-12-11 project plan (the "March 2nd, Full Go-Live" / CIFF timeline) and of Mandy's 2026-01-14 opening request. Nothing else in the corpus contains either. |
| **#13859** (2026-01-20, `kylor@`) | **Kept — relevant** | Kylor's first substantive reply, establishing that options/option-groups/images were the known gap before he took the account. |
| **#14656** (2 msgs, 2026-06-18T04:59:38 and 13:10:25) | **Discarded for new information** | Both messages are verbatim duplicates of #14637 messages at the identical timestamps. Zero unique content. Retained only as evidence that HelpScout double-captures the `onboarding@` mailbox. |
| **#14815** (3 msgs, 2026-07-20/21) | **Discarded for new information, with one exception** | Duplicates of #14801 at 16:24:17, 01:12:51 and 13:48:34, differing only in plaintext rendering and the HelpScout satisfaction footer. **One incremental fact used:** #14815 alone carries Kyla's full signature block — *"Kyla Bosch / Onboarding & Implementation Manager / support@supercatsolutions.com / +1-919-234-7778"* — which lets me confirm her surname and title. Everything else discarded. |

No tier C tickets exist. `ica.com.tr` and `sezondekor.com` were excluded from tier A by the
corpus generator on the assumption they are "Turkish suppliers." **That assumption is wrong** —
both are Pebl distributors with their own eCat user groups and iPad logins (see §4). No harm
done to this analysis because neither ever filed a ticket, but the tiering rule would misclassify
them on any future run.

---

## 2. What I could not determine

Ordered by how much it matters.

### 2.1 Was eCat used at CIFF Guangzhou (March 2026)? — `undetermined`, leaning strongly no
The 2025-12-10 plan aimed at "March 18th CIFF Guangzhou Fair" and "March 2nd, Full Go-Live."
March 2026 in the DB: **2 logins, 0 orders, 0 rep accounts, 2 fatal + 2 warning Products
imports, no images, no options.** Corpus for the whole of March: two short Kylor check-ins and
Mandy's 2026-03-31 file. So eCat almost certainly was not used there; whether Pebl *attended*
is unknowable from these sources.
**Would settle it:** any email in the 2026-03-01 → 2026-03-25 window; a Fathom call; or a
CIFF-named Smart Stack (only "SPOGA 2026", created 2026-06-05, exists).

### 2.2 Why were ten user accounts destroyed on 2026-07-28 → 07-30? — `undetermined`
`audit_log_entries` records the acts and the actor (org_user 152538, Mandy) to the second, and
nothing about intent. The three distributor groups created in the same window (ICA 07-22, ETC
07-30, Sezon Dekor 08-10) and the domestic-China accounts (07-22, 07-24, 08-05) argue
*deliberate pivot* rather than error. But that is inference.
**Would settle it:** one email to Mandy. This is the highest-value open question on the account
and nobody at SuperCat has asked it.

### 2.3 Can the nine users in "Pebl sales oversea" currently see any customer? — `undetermined`, leaning no
`user_types.customer_synching = 'o'` (associated-only) for that group, and all 171 customers
carry `territory_codes = '[]'`. That combination should yield an empty customer list on the
iPad. I did not verify the runtime rule and did not read the sync code.
**Would settle it:** an iPad sync test on `sales15@` or `tomdewulf@`, or reading the
customer-sync selection logic in `supercat_server`.

### 2.4 When was the price level `project` deleted? — `undetermined`
Twelve orders totalling $264,130.00 (2026-05-13 → 2026-06-12) reference `price_level = 'project'`.
No such row exists in `price_levels` today. `price_levels` has no soft-delete column and no
audit trail, and `audit_log_entries` does not record price-level changes.
**Would settle it:** nothing available in Postgres. Would need Rails logs or a DB backup.

### 2.5 What are the 26 August `order submission` audit events that produced 1 order? — `undetermined`
`audit_log_entries` holds 26 `order submission` events for surviving org_users in Aug 2026
(12 of them by `eltecul@hotmail.com` / ETC on 2026-08-05 and 08-06, plus 11 by Mandy), while
`orders` holds exactly **one** submitted August row. The August event payloads repeat identical
`extended_price` values (5740, 6880, 7360) across four sessions — the same three-line order
submitted over and over, consistent with a new distributor being trained or a template being
tested. Whether they failed server-side validation, were hard-deleted, or were never persisted
by design, I cannot tell. `orders.num_failures = 0` on every surviving row, and no
`is_marked_deleted = true` rows exist.
**Would settle it:** Rails request logs for 2026-08-05/06, or the submission-handling code path.

### 2.6 Which emails belong to Annie Xie and Gavin Lai? — `undetermined`
Both appear in `login_events` with full names (`anniexie`, 15 logins; `gavinlai`, 27 logins)
and both accounts are destroyed. Two candidate `users` rows survive with no org attachment:
`sales10@peblfurniture.com` and `sales16@peblfurniture.com`, both created 2026-06-25. I will
not guess which is which.
**Would settle it:** the `rep_lookup_table.csv` attached to Mandy's 2026-07-01 email (not in
the corpus), or `login_events.user_id` joined to `users` — which I did attempt; the join
resolves for surviving accounts only.

### 2.7 Who is "harson"? — `undetermined`
Three logins, 2026-07-28/29, group `Pebl sales domestic`, account destroyed within days. Two
candidate orphan `users` rows created 2026-07-22: `doc@peblfurniture.com` and
`sales01.cn@peblfurniture.com`.

### 2.8 Why was the item-code scheme replaced around 2026-06-06? — `undetermined`
`products` shows 372 numeric-code rows (`302010072`) last touched 2026-06-06 and 126
dashed-code rows (`1-ORBIT-01-003`) first touched the same day. A complete primary-key
migration, sixteen days before SPOGA. The corpus is silent — Kylor's 2026-06-03 email is still
discussing numeric codes and even *assigns four new numeric codes* (`303010223`, `303010224`,
`303010225`, `304010200`), none of which survive.
**Would settle it:** the `products.csv` attached to Mandy's 2026-06-03 or 06-04 emails, or the
Yixing ERP's item master.

### 2.9 Are "Tbs" and "Montenegro " real trade accounts? — `undetermined`
Tom De Wulf's four orders: two to "Tbs" ($12,378) and one to "Montenegro " ($54,206 — the
third-largest single order on the account, with a trailing space in the name). Both are
locally-created buyers with no matching `customers` row and no buyer email. "Montenegro" is a
country, not a company. I counted both as *plausible third-party* in the JOURNEY, which may
overstate that bucket by up to $66,584.
**Would settle it:** Pebl's own ERP/order book.

### 2.10 Did Jon ever run the rep training? — `undetermined`, leaning no
Promised by Kyla on 2026-07-20: *"Separately, Jon will be reaching out to schedule a hands-on
session with your sales team."* No later corpus message, no Fathom call after 2025-12-10, and
by the time such a session could plausibly have happened (late July / August) nine of the reps
it would have trained no longer had accounts.
**Would settle it:** Jon's calendar, or Fathom for 2026-07-21 → 2026-08-25.

### 2.11 Was the Yixing ERP integration ever scoped past the Discovery Call? — `undetermined`, leaning no
The whole second half of the 2025-12-10 call is about ERP→eCat automation and orders→ERP
export. `organizations.export_type` is empty, `stdjson_export_url` is `NULL`, all 91 orders
have `is_exported = false` and `to_export = false`, and the ERP's name and URL — which Jon
asked for twice — appear nowhere. Mandy did ask for something adjacent on 2026-06-26
(*"I am wondering if I could from where to download all the photos which I uploaded to ecat?
We need the photos for our another warehousing system"*), which suggests Pebl built its own
downstream systems instead.
**Would settle it:** any email between Jon/Brent and Pebl about the ERP after 2025-12-11.

### 2.12 Is 0 inventory rows a decision or an oversight? — `undetermined`, leaning "decided by silence"
Offered exactly once, on 2026-06-17: *"Inventory (optional) — if you'd like reps to see stock
levels on iPad, we'd need an inventory file. This can come later if it's not a priority."*
Never answered in the corpus. `inventories` = 0 rows and **no Inventory import exists anywhere
in the org's 480-event import history**. Nothing was ever blocked by it. But a manufacturer
whose reps sell at fairs off lead times may well want it.
**Would settle it:** one line of email.

### 2.13 What did SuperCat actually build in August 2025, and who asked for it? — partially undetermined
`import_events` and `login_events` establish *what* (84 collection-level products, all priced
$0.00, three image batches, two taxonomy imports, four options imports, all by Brent Sanders,
2025-08-01 → 2025-09-06) and *when*. Nothing establishes *why*, whether it was a pre-sales
demo or a first delivery attempt, or what the client saw. The corpus starts 2025-12-10.

### 2.14 What Mandy actually broke and fixed between 2026-05-11 and 2026-05-12 — partially undetermined
She wrote *"Please ignore all my previous emails. I have fixed most of the problems"* on
2026-05-12T12:00:18, listing three fixes. May 2026 holds 39 Images imports, 12 clean + 3 error
Options imports, 6 clean + 1 error Option Groups imports and 39 warning-tier Products imports —
far too many events to map onto the narrative. Which upload caused the Admin Console
"internal error has occurred" is not recoverable from block-level tiers.

---

## 3. Contradictions between sources

### 3.1 `RAWSTATE_pebl.json` says 13 users; `org_users` has 17 rows
RAWSTATE excludes four SuperCat-internal accounts (`brent@`, `chuck+u@`,
`chuck+superadmin@`, `kjael@`) but **retains** `kylor22johnson@gmail.com`, which it labels
"SuperCat-side test account, not a client user." The filter is inconsistent with itself.
Neither number is the client headcount: **the client has 13 org_user rows today, of which
12 are real client people** (`kylor22johnson` being the thirteenth).
Consequence for anyone scoring "user count": three defensible answers exist (17 / 13 / 12).

### 3.2 Image coverage does not reconcile — three answers
RAWSTATE: `products_with_images: 690` of 713, i.e. 23 without. My queries on the same
snapshot: `image_exists = false` → **16**; `images_json` empty/null → **9**. The `images` text
column is empty on all 713 rows and is evidently vestigial. I cannot reproduce 23 by any
definition I tried. **Flagged rather than resolved** — the DB is not automatically right
either, and RAWSTATE may be using a join against imported image files that I did not replicate.
The 16 named products lacking `image_exists` are listed in the JOURNEY's supporting queries
(Coral, Deck Slim, Harbour Vertical, Riva, Flow, Bloom CT, Dos, Faro ×2, Leaf, Tube Dining,
XX, Basix cushion, Bloom Neo armrest).

### 3.3 The $999,930.60 headline is true and misleading — the sharpest contradiction
RAWSTATE reports `total_value: "999930.60"` and correctly warns *"do not assume self-test."*
Both halves of that warning need qualifying:
- It is **not** a self-test pattern in the technical sense — 88 of 91 orders are legitimate
  locally-created-customer orders, exactly the behaviour Kylor described on 2026-07-08.
- But **58.2% of the value ($582,004.60 across 51 orders) sits against internal or literal
  test buyer names** — "Pebl" (25 orders, $394,600), "Test" (11, $115,009), "Skyard" (10,
  $17,757), "Test_02", "Joe", "dsbs", "Pebl(Rita)" — and a further 3.7% ($36,646 across 17
  orders, all Rita Luo on 2026-06-21) sits against **product-set names used as buyers**
  ("Wave Set", "Riposo Teak Set", "Newport Set"…), i.e. the order screen used as a
  bundle-pricing calculator.
- And decisively: **`customer_po_num` is empty on all 91 orders**, `ship_date` is set on 6,
  `is_exported` and `to_export` are `false` on all 91, `sum(num_failures) = 0`, and the org has
  no export configured at all.

**Conclusion: `orders.total` on this org measures quotation and configuration activity, not
commercial activity.** The defensible commercial figure is at most **$381,280 across 23
orders**, and the figure backed by a real customer record is **$35,304 across 3 orders**.
Citing $999,930.60 as revenue, pipeline or GMV would overstate by roughly 2.6× to 28×
depending on the definition. This is the one number on this account most likely to be
repeated wrongly.

### 3.4 `distinct_ordering_users: 8` vs `distinct_rep_emails: 13` — both true, neither useful alone
RAWSTATE reports both. The gap is explained by the purge: five of the thirteen ordering
`rep_email` values (`sales06@`, `sales11@`, `sales05@`, `sales08@`, `sales03@`) belong to
destroyed accounts whose `org_user_id` no longer resolves. **The true count of humans who ever
wrote an order is 13, or 12 excluding `kylor22johnson@gmail.com`.** A framework that reads
`distinct_ordering_users: 8` as adoption will under-count by a third and will silently drop
the highest-value rep on the account (Marly Mai, $251,592).

### 3.5 Import tier counts differ slightly from mine
RAWSTATE counts *blocks* (a single `import_events` row can carry more than one file block); my
parse takes the first block per row. Divergences: 2026-05 Products warning 42 (RAWSTATE) vs 39
(mine); 2026-06 Products error 20 vs 17, warning 48 vs 45; and 2025-08, where RAWSTATE records
Options as `clean: 4` while my parse of those rows sees `:error` tokens and no Option Groups
blocks at all. **RAWSTATE's block-level method is the better one and I deferred to it for all
tier claims**, using `import_events` only for dates and message content. The 2025-08 Options
disagreement is unresolved and worth a second look if tier accuracy matters.

### 3.6 Kylor's product counts drift against the DB
2026-06-17: *"687 active products"*. 2026-07-17: *"713 products live with images (~97%
coverage)"*. Today: 713 active, of which 690 (RAWSTATE) or 697 (`image_exists`) have images.
The 713 figure has been stable since 2026-07-17 despite Products imports on 2026-07-30,
08-05, 08-06 and 08-07 — either a coincidence or the 2026-07-17 number was quoted from a
later reading. Not resolvable; `products` is mutable and has no per-row creation timestamp.

### 3.7 The customer-assignment claim of 2026-07-01 cannot be verified and is now false
[HS #13879, 2026-07-01T23:51:26, kylor@] *"171 customers are imported, each assigned to the
correct rep via territory codes per your list."* Today all 171 `customers` rows were created
**2026-07-30 07:48** with `territory_codes = '[]'`. Because each customer import hard-deletes
and reloads the table, **no evidence of the 2026-07-01 state survives** — the statement was
presumably true when written and is definitely false now. `customers` cannot be reconstructed
for a past date, as RAWSTATE itself warns.

### 3.8 Mandy's own diagnosis of the image failure is incomplete, and entered the record as fact
[HS #13879, 2026-04-28T07:08:59] *"I tried to use the VPN and all the photos are displayed
now."* The DB shows the option-swatch files were **also** stored with doubled extensions
(`sf090.jpg.jpg`, `latte_ro6.jpg.jpg`) until they re-imported correctly at **2026-04-28
04:18:33**, three hours before she wrote. Two independent causes; only the network one was
named, and it is the one the corpus preserves. Anyone reading the corpus alone will conclude
this was purely a Great Firewall problem. It was not.

### 3.9 Kylor's 2026-06-30 price-level list vs `price_levels`
He offered the client *"fob , ahp , project , tmm , suggested retail price , zebra sales price
in dach"*. Of those six, only `fob` (created 2026-04-01) and `suggested retail price` (created
2026-06-15) exist today; `ahp`, `project`, `tmm` and `zebra sales price in dach` have been
deleted with no recorded date. `zebra sales price in dach` — together with `login_events`
recording Rita Luo's group as **`ZEBRA GROUP`** on 2026-06-17 — is direct evidence the org was
cloned from another client's template, which also explains the `TN1` / `COL20` / `COL3` /
`CAT1` codes Kylor had to renumber on 2026-04-02.

### 3.10 Manifest bookkeeping
The manifest reports "94 HelpScout threads" and 4 tier A + 4 tier B tickets; the chronological
record renders ~101 message entries under 8 ticket IDs; the handoff brief says "8 tickets, 94
threads". "Threads" and "messages" are being used interchangeably somewhere upstream. Cosmetic,
but it means "94 threads" should not be read as 94 conversations — the real number is **4**.

---

## 4. Corpus holes — where the database shows work and the corpus shows nothing

This is the defining feature of this client. The corpus covers **4 conversations and 1 call
across 13 months**. The database covers 480 import events, 776 login events, 91 orders and a
full audit trail. Named by stretch, worst first:

### H1 · 2026-07-22 → 2026-08-25 — the entire post-handoff period. **Five weeks. Zero messages.**
Last corpus message: 2026-07-21T13:48:34. In the silence since:
- 10 user accounts destroyed (2026-07-28 → 07-30)
- all 171 customers re-imported with territory codes wiped (2026-07-30 07:48)
- three distributor user groups created (ICA 07-22, ETC 07-30, Albania-Sezon Dekor 08-10)
- two domestic-China accounts created (`jojo` 07-24, `info.cn` 08-05); one (`harson`) created and destroyed
- two **fatal** Products imports on 2026-08-05, self-recovered the same day
- 52 clean Images imports
- two new iPad report formats on 2026-08-13, one named "Furniture China 2026 Shanghai - Internal Reference"
- **eight new price levels on 2026-08-19**
- 85 logins by 10 users; one order
Nobody at SuperCat has any written knowledge of any of this. **If there is one thing to fix
about how this account is monitored, it is this.**

### H2 · 2025-07-24 → 2025-12-09 — the org's first four and a half months. **Zero messages.**
Org created, `Pebl sales oversea` user group created (same day), Brent Sanders builds an
84-product zero-priced catalogue with images and taxonomies (2025-08-01 → 09-06), Trista Qiu
becomes the first client user (2025-08-08) and logs in monthly through the autumn, Brent
returns 2025-10-31 and 11-04, `chuck+*` accounts appear 2025-11-12, `kylor22johnson` 2025-11-21,
`kjael@` 2026-01-07. The corpus opens on 2025-12-10 with a call that treats the project as
just starting. **Whatever was agreed to justify the July 2025 provisioning is not in evidence.**

### H3 · 2026-06-06 — the item-code migration. **Not one word.**
372 numeric-code products retired and the dashed-code generation begun on a single day,
sixteen days before the fair the whole project was aimed at. Kylor's emails on 2026-06-03 and
06-04 are still assigning numeric codes. The scheme change is visible only in
`products.item_number` and `last_modified_at`.

### H4 · 2026-06-19 → 2026-06-26 — SPOGA itself. **The best week on the account has no narrative.**
26 orders on 06-21, 5 on 06-22, 3 on 06-24, **17 on 06-25 worth $316,232**, 8 on 06-30; six
rep accounts created *during* the fair on 06-25; 373 logins across 16 users in the month. The
only corpus content in the window is Kylor's internal *"@kylaB can you help her out here and
reference me OOO , sorry been unplugged"* (2026-06-23), Kyla's internal reply, and one
retrospective line on 06-26: *"the feedback of our ecat system from Spoga is quite good !"*
**The onboarding owner was on honeymoon during his client's go-live event.** That is not a
criticism — it is why the record is empty.

### H5 · Every real buyer is missing from the corpus.
No corpus message anywhere names a customer Pebl actually quoted. Esun International
($251,592, Marly, 2026-06-25), "Montenegro" ($54,206, Tom), Gescova Outdoor Furniture
($28,920, Mandy — the first order ever written against an imported customer), Everything Under
The Sun ($18,000, Wisteria), Ocean Import & Export in Qatar ($9,800, Wisteria), and the
Maldives resort project ($6,384, Priscilla, 2026-08-13). All of it lives in `orders` alone.

### H6 · All three distributors are absent.
ICA (Turkey), ETC and Albania-Sezon Dekor have their own user groups, 16 logins between them,
2 persisted orders and 12 order-submission attempts, and **have never filed a HelpScout
ticket**. The corpus generator additionally mis-tiered `ica.com.tr` and `sezondekor.com` as
"Turkish suppliers — excluded from A."

### H7 · Every attachment and every screenshot is gone.
The substantive data exchange in this project happened in attachments, and the corpus preserves
only the covering text. Missing payloads include: the original Haven & Wave Excel; every
generation of `products.csv`, `options.csv`, `option_groups.csv`; `peblproducts.csv`,
`products2pebl.csv`, `optionspebl.csv`, `option_groupspebl.csv`; the `ecat-options mapping`
workbook; `rep_lookup_table.csv`; the first `customers.csv`; the logo files (`.png` and the
unusable `.eps`); the Wave collection Product File PDF; and the 2026 Terms & Conditions PDF.
Six WeTransfer links (`we.tl/t-xhdxo6qbQt`, `t-QOxLYhYhs2geyvq0`, `t-kMw6C15wVeCvnEPj`,
`t-8QeWwrnPnvAqXhf1`, `t-8BHmeogSqPJEFUvx`) are long expired. At least **14 messages** say
"attached is the screenshot / screen recording" — and several of the "the catalog is wrong"
claims rest entirely on visual evidence I cannot see, including the iPad display Mandy used to
specify her field layout (2026-01-29), the broken Wave-sofa fabric swatch (2026-05-09), and
the option-mapping recordings of 2026-05-25 and 2026-06-02.

### H8 · No call after 2025-12-10 — nine months run entirely by email.
One call in thirteen months, across a 12–13 hour time difference, deliberately. Kylor,
2026-02-05: *"Since I know scheduling calls can be challenging with the time difference, I've
tried to make this email as comprehensive as possible so you can work through everything at
your own pace."* Kyla, 2026-07-20: *"no need to schedule anything live if you don't need a live
call!"* Mandy declined training on 2026-07-21. **Consequence for this reconstruction: there is
no verbal record of any decision after the Discovery Call.** Every inference about intent comes
from written text or from database state.

### H9 · Internal SuperCat coordination is essentially unrecorded.
Four tier-B tickets, two of which are pure duplicates. There is no internal thread about the
August 2025 build, the missed CIFF date, the SPOGA outcome, the decision to hand off, or the
post-handoff changes. The only internal exchange in the corpus is two lines between Kylor and
Kyla on 2026-06-23.

### H10 · 2026-02-05 → 2026-03-31 — the CIFF window.
Three short check-in emails from Kylor (2026-02-16, 2026-03-10) and one holiday notice from
Mandy (2026-02-17). Meanwhile: Mandy's account is created, she logs in three times, two fatal
and two warning Products imports run in March, and the March 2nd go-live and March 18th fair
both pass. **Neither party ever writes the words CIFF or Guangzhou again after 2025-12-11.**

### H11 · 2026-07-02 → 2026-07-08 and 2026-07-08 → 2026-07-17.
Two multi-day corpus gaps during the busiest configuration period on the account:
`audit_log_entries` records 19 `OrgUser updated`, 12 `user group updated`, 11 `OrgUser
destroyd` and 5 `OrgUser created` events in July, plus four Customers imports (2 clean,
2 error) — against six corpus messages for the whole month.

---

## 5. Things I deliberately did not claim

- **I did not call the 88 unmatched orders "self-tests."** They are locally-created-customer
  orders, a documented behaviour. Whether an individual one is a test is a separate judgement,
  made per buyer name and stated as such.
- **I did not call the 2026-07-28→30 purge churn risk.** The simultaneous creation of
  distributor and domestic groups argues the opposite. I recorded it as an undocumented
  regression against the delivered configuration, which is what the evidence supports.
- **I did not date the deletion of any price level, user account territory, or product
  generation** beyond what `created_at` / `last_modified_at` / `audit_log_entries` will bear.
- **I did not attribute the August audit-only order submissions to any cause.**
- **I did not treat `orders.total` as revenue anywhere**, and flagged the one figure most
  likely to be misread.
