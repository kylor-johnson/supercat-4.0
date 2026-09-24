# GAPS — Magic Lite | NSL (`mali`, org 285)

Companion to `JOURNEY_mali.md`. Written 2026-08-25 from the same evidence:
both corpus parts in full, `RAWSTATE_mali.json`, and direct read-only SQL.

---

## 1. What I could not determine

| # | Unresolved | Why | What would settle it |
|---|---|---|---|
| 1 | **When the 608 `hideable` flags were set, and in which import.** | `products` has no `updated_at` column and no per-row history. The hero-variant strategy is dated to the 2026-03-19 call by conversation only. | The archived product CSVs on the FTP `/data` backup path, or an S3 copy of the import files. The import log records tiers, not payloads. |
| 2 | **What changed on 2026-08-19 at 18:17:32.** | `organizations` and *both* `mobile_sites` rows for org 285 share that exact `updated_at`. No `audit_log_entries` row. No corpus message falls between 2026-08-17 and 2026-08-24. | A PaperTrail/`versions` table if one exists for these models; failing that, ask Kyla or Kylor directly. |
| 3 | **What, if anything, the two Electra Sales reps were told.** | `ryan@` and `jason@electrasalesltd.ca` were invited 2026-08-10 and both invitations expired unredeemed on 2026-08-17. "Electra Sales" appears **nowhere** in either corpus part. | SuperCat's outbound invitation mail log, or Jen Penton. |
| 4 | **Why the beta rep list changed between May and August.** | Jen P's 2026-05-13 list was Jim Bechkos, Tim Veal (GSL), Alton McKey, Shelley Aldridge, Josh Skula, Josh Nelson, Anna Tardif. The invitations actually issued on 2026-08-10 went to Electra Sales ×2, Dan French (GS Lighting), Mike Krause and Josh Nelson — one name in common. | The email Jen P must have sent between 2026-08-04 and 2026-08-10 with the final names and addresses. It is not in the corpus. |
| 5 | **Whether an empty `price_levels_user_types` set means "all" or "none".** | Admin and z-SuperCat have no rows; the four other groups have explicit rows. Behaviourally admins plainly see every price level — that is the whole subject of the 2026-07-20 → 07-28 confusion — so empty is almost certainly "all". I did not verify against code. | The user-group price authorization logic in `supercat_server`. |
| 6 | **What Endeavour was actually scoped to deliver, and whether the rest was descoped.** | Brittni's 2025-10-15 estimate covered "Product file (excluding images), Customer File, Inventory File, Sales Data File, Invoice & Order Data File" at "30-50 HRS". What exists on 2026-08-25 is one inventory export. Nothing records the other four being dropped. | Endeavour's SOW, or Jen Zorony. |
| 7 | **Who created the single empty cart on 2026-07-15.** | `org_user_id 155369` is the shared `support@supercatsolutions.com` account, used by both Kyla and Kylor. | Session logs. Immaterial — it is SuperCat's either way. |
| 8 | **Whether the "Organization Tearsheet" iPad report is bespoke or a default.** | Created 2026-07-22 18:37:17, never mentioned in the corpus, name looks generic. | Compare `ipad_reports.name` across other orgs. |
| 9 | **Whether any rep-facing training ever happened.** | Promised repeatedly — Kyla, 2026-05-13: "we'll get one of our sales reps, John or Emery, to do the eCat rep-based training because they are the sales experts talking to salesmen." No corpus record of one being held or booked. | Fathom, outside this corpus window; or the SuperCat sales team's calendar. |
| 10 | **Whether the client has yet accepted Phase 4 for either brand.** | I dated catalogue completeness from SuperCat's own claims (2026-07-24 ML / 2026-08-03 NSL). Jen P's last message is a chase, not an acceptance. 16 visible NSL SKUs are still unpriced. | The 2026-08-25+ correspondence, which falls outside this corpus. |

---

## 2. Tier-B and tier-C dispositions

### Part 1 — 51 tier-B tickets, of which I discarded 50

**#13582–#13631 — DISCARDED as narrative evidence, retained as a file manifest.**

All 50 are byte-identical automated notifications from
`noreply@supercatsolutions.com`, subject "New Onboarding File Upload - Magic
Lite", all fired between **2025-12-23 20:04:05 and 20:14:19 UTC** — a ten-minute
window. Each differs only in filename and byte size. I read five in full,
confirmed the boilerplate, and extracted filename + timestamp from all 50
programmatically instead of reading the remaining 45 line by line.

**This is the whole explanation for the ratio the brief flags.** "51 tier-B
vs 5 tier-A" does not describe a project dominated by internal chatter. It
describes *one client action* — a single bulk upload of 36 `.xlsx` spec tables
and 14 `.png` product images — fanned out into 50 HelpScout tickets by a
notification rule. Ticket volume here measures the notification system, not
the relationship.

Retained value: the manifest dates the client's spec-table delivery precisely
and names the files (`5CCT LED Thin Line Down Light - Square.xlsx`,
`SL-ID-30K-LP-XX-A8.png`, and so on). But see §4.3 — even as a manifest it is
incomplete.

**#14211 — KEPT.** 2026-03-26 03:44, kylor@ to "Team", "Magic Lite eCat Update —
Ready for Review". The only genuine internal thread in part 1, and the only
place the figure "694 products across 5 collections (Linear Lighting, Under
Cabinet, Down Lighting, Landscape, Industrial)" appears.

### Part 2 — 6 tier-B tickets

| Ticket | Disposition |
|---|---|
| **#14329** (11 msgs) | **KEPT.** "SuperCat x Magic Lite — Next Steps & Admin Training". A real working thread despite the tier-B label — it carries the SFTP credentials, the rep-file clarifications (missing emails, retired reps, "Josh & Jason Nelson", Priya Singh) and the 47-invitation build. Tier-B only because the capture is on `supercatsolutions.com`. |
| **#15008** (1 msg) | **KEPT.** 2026-08-10 17:02, "Rep Beta Testers". One message, and the *only* corpus trace of the beta launch decision. Without it the 2026-08-10 invitations in the DB have no explanation at all. |
| **#14419, #14509, #14851, #14944** | **KEPT ONLY AS DUPLICATES.** Each is the `support@supercatsolutions.com` mirror of a tier-A thread, with HelpScout satisfaction-rating footers appended. No unique content. Counted in §3 below. |

### Part 2 — the single tier-C ticket, discarded outright

**#15172 — "Re: Additional Orders to Void", 2026-08-06, ben@gabriellawhite.com.**
An unrelated Gabriella White production incident about 18 missing orders, tagged
`l3 - engineering intervention`, `s2 - high`, `type: bug`. It has nothing to do
with Magic Lite.

It was captured because the mention token `nsl\b` matched inside the email
address **`SusanSL@gabriellawhite.com`** — "Susa**nSL**@". That is the only
occurrence of the token in the entire 135-line ticket. A false positive from a
substring in a third party's name.

Worth flagging beyond this run: `nsl\b` will match any address or word ending in
"nsl", and Endeavour's genuine second domain `endeavor4solutions.com` (22
occurrences, real — Brittni's signature alternates between it and
`endeavoursolutions.com`) is *not* the tier-C noise. The noise is the token.

---

## 3. Duplicate captures — the volume figures are inflated ~2×

Collapsing on normalised subject (stripping `Re:`/`RE:`/`Fw:`/`FW:`/`Fwd:`):

**Part 2's 150 messages are, at most, ~95 distinct messages across 10
conversations.** The dominant case:

| Normalised subject | Ticket numbers | Messages |
|---|---|---|
| "SuperCat / Magic Lite: 4/29 Follow-Up" | #14418 (11), #14509 (9), #14727 (36), #14728 (28), #14743 (2), #14944 (1) | **87** |
| "SFTP Permissions" | #14842 (1), #14891 (16), #14944 | 18 |
| "Next Steps & Admin Training" | #14329 | 11 |
| "SuperCat invite - Please activate account…" | #14437 (8), #14456 (3), #14425 (3) | 14 |
| "Magic Lite / SuperCat: 7/28 Follow-Up" | #14849 (4), #14851 (4) | 8 |

**87 of part 2's 150 messages — 58% — are one conversation captured under six
ticket numbers.** #14727 and #14728 are near-perfect mirrors, frequently one
second apart (e.g. both carry Jen Z's 2026-07-02 message at 14:16:06 and
14:16:07). #14425 contains the same message twice at the identical timestamp
2026-04-30T18:03:26.

**Part 1's 116 messages are 6 conversations plus 50 identical notifications.**

**Combined: 266 "threads" collapse to roughly 15 actual conversations.** Any
conclusion drawn from raw ticket counts — engagement, escalation frequency,
support load — will be wrong by roughly a factor of two, and by a factor of ten
for December 2025.

---

## 4. Contradictions between sources

### 4.1 Against `RAWSTATE_mali.json`
Six, set out in full at the end of `JOURNEY_mali.md`. Summarised: there is no
`status` column on `organizations`; `ever_logged_in` silently means *iPad only*,
which inverts the ML-vs-NSL adoption story; the three "NSL Reps" who signed in
are two SuperCat staff and one NSL employee; there is one `orders` row, not
zero; `audit_log_entries` holds 80 rows for this org, not 9; and
`distribution_centers` is 0 despite a written claim that two exist.

### 4.2 SuperCat's statements against the database

| Claim | Date & source | Database |
|---|---|---|
| "We have set up two Distribution Centers in SuperCat: one for Magic Lite (ml ) and one for NSL (nsl )… We have already set this up and tested it on our end" | 2026-05-19, #14418, kyla@ | `distribution_centers` for org 285 = **0**. `inventories` = 703 rows, none with a `distribution_center_id`. The format was reverted to brand-prefixed columns by 2026-07-22. |
| "all 695 products now have a product story populated" | 2026-07-08, #14727, kylor@ | **660** of 725 active products have a story. 65 do not. That day's Product Stories import was error-tier. |
| "Product images - all products now have images with correct product photos as the primary image" | 2026-03-26, #14211, kylor@ | **652** of 725 have an image; 73 do not. "Correct" is separately disproved by the 2026-07-21 punch list. |
| "all 3,418 customers (NSL + ML merged) are live with correct price codes… **No errors.**" | 2026-04-29 00:06, #14329, kylor@ | The 2026-04-28 23:28:44 import carried 1 error (`Buyer phone is too long… Customer # = 21721`) — the exact error Kyla then demonstrated live on the 2026-04-29 training call. The attempt five minutes earlier (23:23:09) carried **1,001 errors + 1 fatal**, all `Default price code 'nsl_dn' must be a valid price level code` — the code is `nsldn`, not `nsl_dn`. Substantially true, literally not. |
| "The file imported cleanly and ML warehouse quantities are showing" | 2026-08-12, #14891, kylor@ | Warning-tier, with rows silently discarded: `Product not found, record ignored., BaseItemCode=ES-120V-27K-XX`, `YH-HRF50CA120S-505060RGB`, `YH-RGB-PC-10` and others. |
| "there were like 180 images in that initial file dump" | 2026-02-02 call, Kylor | `onboarding_file_uploads`: 16 images on 2025-12-23 + 118 on 2026-01-06 = **134**. |

### 4.3 Internal to the record

- **Product count drifts through the whole project and is never reconciled.**
  948 SKUs (2026-01-20 call, Brent: "We've got 948 different SKUs. Does that
  seem right?" — Jen P: "Yes.") → 906 imported and live (2026-03-11) → 694
  (2026-03-26) → 695 (2026-07-08) → 679 in-catalogue / 69 visible (2026-07-28
  call) → 681 rows / 69 visible hero products (2026-07-29) → **725 active, 117
  visible, 962 total rows including 237 soft-deleted** in the database today.
  No message in either corpus part explains a single one of these movements.
- **Default price level, stated two ways two weeks apart.** 2026-04-29: "ML Reps
  default to ML **Net** (with DealerNet accessible but not default)". 2026-05-12:
  "ML Reps default to ML **DN** (both with their respective List price accessible
  but not default)". Then 2026-07-22, Jen Z: "It should really be when they log
  in, they should see their pricing" — the setting was still being argued about
  in late July.
- **"Business Central" vs Dynamics GP.** The brief describes Endeavour as "the
  Business Central integrator". Every reference in 266 messages and 18 calls is
  to **Dynamics GP**, on-premises, SQL Server — Jen Z, 2026-01-20: "Yeah, that's
  Microsoft Dynamics"; Brittni, 2026-04-09: "GP is housed in a SQL Server
  on-prem". No Business Central anywhere.
- **The `.co` domains were not typos, and captured nothing.** `nslusa.co` and
  `magiclite.co` appear **zero times** in either corpus part. They exist only in
  the database, as the login addresses of the two service accounts SuperCat
  created for the eCat Online public sites: `lights@magiclite.co` (2026-07-09)
  and `nslsales@nslusa.co` (2026-07-15). Non-deliverable addresses used as
  usernames. The corpus filter's `.co` clause could not have matched anything
  and did not.

---

## 5. Corpus holes — the database shows activity, the corpus shows nothing

Ordered by date. Every one is verifiable against `import_events`,
`onboarding_file_uploads`, `organization_invitations` or `audit_log_entries`.

1. **2025-11-27 — the client's first delivery.** 3 files to the onboarding portal
   (2 spreadsheets, 1 PDF), six days after kickoff. No notification ticket, no
   email. Brent's first acknowledgement is 2025-12-04.
2. **2025-12-22, 21:54–23:54 — the entire first product import.** Twelve
   attempts in two hours: 2 fatal, 1,003 errors on the first, ending with two
   error-free imports at 22:45 and 23:54. **Not one word of this exists in the
   corpus.** The next client-facing message is Brent on 2026-01-07 asking to
   book a catalogue review. This is Phase 2 in its entirety, invisible.
3. **2025-12-23 — 17 uploads with no notification.** 67 files hit the portal that
   day; only 50 notification tickets exist. The manifest is 25% short.
4. **2026-01-06 — 119 uploads, 118 of them images, and zero tickets.** This is
   Jen's "I've uploaded a LOT of images, with product codes in the names." The
   notification stream stopped after 2025-12-23 and no one noticed. The corpus
   preserves the *small* upload burst in exhaustive 50-ticket detail and loses
   the *large* one completely.
5. **2026-03-12 → 2026-03-19 — an entire options build, unmentioned.** 12
   `Options`, 8 `Option Groups`, 18 `Matrix Options` and 1 `Option Images`
   import, several fatal. It is never raised in any email or on any call. Worse,
   the 2026-03-19 call *rejected* the approach — Brent: "our recommendation is
   not to go with the optioning just for the sake of like having what feels like
   a more complete set of data" — yet imports ran both before and after that
   decision. Residue in the DB today: 2 options, 2 option groups.
6. **2026-04-09, 17:18:01 and 17:18:06 — two `OrgUser destroyd` events fired
   during a live call** with Brittni and both Jens. Both on SuperCat's own
   `support` account. Unmentioned on the call and everywhere else.
7. **2026-05-19 → 2026-07-07 — 49 days with no import of any kind.** The corpus
   contains three messages in that span. This is the project's dead zone;
   neither source explains it, and it is the single largest unexplained gap in
   the record.
8. **2026-07-09, 21:55:54 → 22:28:13 — `hide_products_marked_hideable` set true,
   then back to false** on the Magic Lite eCat Online site. A 32-minute
   experiment with the hero-variant display, recorded only in
   `audit_log_entries`.
9. **2026-08-10 19:54:22 and 2026-08-17 17:57:56 — the beta launch.** Five
   invitations issued, three redeemed, two expired. **The most important
   adoption event in the project's history, and the corpus contains only Kylor's
   17:02 email *offering* to send them.** Nothing confirms they went; nothing
   names the recipients; nothing notes that Dan French took his up two minutes
   later and logged into eCat Online 17 minutes after that; nothing notes that
   both Electra Sales invites died. It is not in `audit_log_entries` either —
   self-enrolment through an invitation link writes no audit row, so the org's
   audit trail simply stops on 2026-08-03.
10. **2026-08-19 18:17:32 — `organizations` and both `mobile_sites` rows
    updated.** No audit entry, no corpus message in the surrounding week. See
    §1.2.
11. **2026-08-25 19:41:21 — a 102-error product import,** `Invalid CategoryCodes
    code: '["LIGHT"]'` — JSON array syntax leaked into the CSV — re-run clean at
    19:54:21. Four hours after the `RAWSTATE` snapshot (18:10) and on the day
    this was written. The corpus window closes at 12:52 the same day.
12. **`sales_data.csv` was never imported. Ever.** `import_events` has ten
    distinct file types for this org and Sales Data is not among them. Yet it was
    an action item on 2026-05-18 ("yes, that's handled through the
    `sales_data.csv` import"), got a full column specification and a `:PARAMS`
    example on 2026-05-19, was assigned to Brittni with the ETA "Before beta
    launch", and was chased again on 2026-07-09. Beta launched on 2026-08-10
    without it. Nobody has closed the item or acknowledged that it lapsed —
    which means Customer Favorites and the Sales Portal dashboards, both sold in
    the October 2025 demo, do not function.

---

## 6. One thing that is in the corpus and probably should not be

The live SFTP password for org `mali` appears in plaintext twice: in the
2026-04-15 action-items email (#14329, alongside the host and username) and
again inside the PowerShell script Brittni pasted on 2026-07-07 (#14743 /
#14727). It is therefore in HelpScout, in this corpus, and in whatever else
consumed these threads. Flagging as a record-handling issue, not a finding
about the onboarding.
