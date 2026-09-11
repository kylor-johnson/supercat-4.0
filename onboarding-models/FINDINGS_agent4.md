# Findings — agent 4 (correspondence) + the B7 lossy-regeneration gate

Written 2026-09-05. **Nothing in `ground-truth/` was edited.** These are the
items that belong in `SESSION_HANDOFF.md`, `OPEN_ITEMS.md` and `BUILD_SPEC.md`,
for whoever owns those files.

## A. Shipped

- `~/.claude/skills/ecat-correspondence/SKILL.md` — agent 4, 564 lines.
- `acceptance/b7_lossy.py` — the lossy-regeneration gate, 561 lines, read-only,
  emits SQL / `--from-results` like `a1_fingerprint.py`.
- `mapping/preupload_check.py` — B7 wired in between B6 and A1.
- `ecatlib/carryforward.py` — `diff_key_for()` added, `diff_against_previous()`
  given a `key_missing` guard (see D2, a live defect).

## B. The day-one question: HelpScout write access

**There is none, under any identity.** `api.helpscout.net/v2/conversations`
returns **401** — reachable, unauthenticated. No HelpScout credential exists in
`~/.supercat/`, the login keychain, the environment, or the workspace. BigQuery
receives HelpScout through a **Hevo ETL** whose credential is Hevo's, read-only
to us, and not borrowable as a write path.

Confirmed further after the first pass: the only HelpScout code on this machine
is `agent-factory/platform/lib/helpscout_snapshot.py`, 86 lines, **zero network
calls** — it computes freshness over a static JSON export. Across every repo
there is **not one reference to `api.helpscout.net`**; all HelpScout URLs in
code are `secure.helpscout.net/conversation/<id>` UI deep-links. There is no
API client and no credential.

**Useful consequence:** that deep-link pattern is the substitute for a write
path. `conversation_id` is on the BigQuery view, so every drafted ticket can
carry a one-click link to its thread. Verified against an independent source
(ticket 15176 → `3426077090`). Use `conversation_id`, **not** `ticket_number` —
they differ (14673 → `3364971115`).

Two grant types, not interchangeable, and the ask must name one:

| grant | replies appear as |
|---|---|
| OAuth2 `client_credentials` (an app) | a bot identity |
| OAuth2 `authorization_code` as Kylor | **Kylor** — the only one worth having |

## C. The finding that reshaped agent 4: the mirror is a nightly batch

`helpscout.conversation_threads` last written **2026-09-04 22:37 UTC**. At
18:54 UTC on 09-05 the table held **zero** threads for that day, while every
prior weekday carries 20–65. Average lag from a client message to visibility is
**6.4h**, worst case ~24h.

Median first staff reply is **226 minutes**. So:

> **57% of client messages (1,579 of 2,769 since 2026-03-01) already have a
> human reply before the batch exposes them to the agent.**

**This is an argument against auto-send that is independent of the gate**, and
it is stronger than the correctness argument: an agent on this data path is
structurally late, and no gate tuning changes it. It also bounds anything else
built on this table.

## D. Defects found

**D1 — `thread_type = 'lineitem'` must be excluded, and only `note` is
documented.** 982 of 982 lineitem threads carry an **empty body**; they are
HelpScout system events and they all carry the staff domain. Excluding only
`note` leaves them in, where they read as a staff reply and **mask genuinely
unanswered tickets**. `ecat-session-prep` § 4b excludes `note` only.

**D2 — B6 was silently inert on four of six file types.** `preupload_check.py`
called `diff_against_previous()` without a key, taking the `BaseItemCode`
default. On a `customers.csv` every row collapses onto the key `''`, which is
then dropped, and B6 returned `dropped=0 added=0 changed={}` — printing
**"none — output is identical to the previous build"** for the mali pair, where
the correct key (`BillToCode`) shows **3,412 changed `DefaultPriceCode`, 3,072
changed `BillToAddress1`, 105 dropped customers**.

This is **BUILD_SPEC §3.4 instance #7**, and it sat in the pre-upload gate
itself — the check whose entire job is catching regeneration blanking could not
see the file type the mali incident is about. Fixed: `diff_key_for()` picks the
key per file type, and a missing key now returns `key_missing` and reports
**NOT CHECKED** instead of zeros.

**D3 — `primary_customer_domain` is not the client.** Ticket 15244 carries
`primary_customer_domain = supercatsolutions.com` while the client is
`jhessler@finearthl.com`; 15249 the same with the client on `legrand.com`. A
second, undocumented way domain-based attribution fails. Derive the client from
the threads.

**D4 — `thread_created_by_type` is worse in the recent window than the
fleet figure suggests.** Fleet-wide 4.9%; over the last quarter **248 of 1,811
threads typed `customer` (13.7%)** were authored from `@supercatsolutions.com`.

## E. A28 measured on the ticket corpus

Of the **38** real client domains in the two-week window:

| domains | orgs each | |
|---|---|---|
| 21 | exactly 1 | confident |
| 14 | 2–12 | ambiguous — `gabriellawhite.com` **12 orgs / 480 users** |
| 3 | 103–165 | undeterminable — `gmail.com` reaches **165 orgs / 15,203 users** |

A28's own example domains (`riccisales`, `decorlightingsales`,
`pacificliteforcesales`) do not appear in this window, but **the phenomenon
does**, through `gabriellawhite.com`, `urbanlightsdenver.com`,
`lightingreps.net` and the free-mail domains.

**New, and it removes about half the ambiguity cheaply:** several apparent
multi-org domains are **test/staging twins** — `alfrescohome.com` → `{ah,
ahtest}`, `goldenlighting.com` → `{gl, gl_staging}`, `dorellfabrics.com` →
`{demo2, drf}`, `interludehome.com` → `{ih, ihw, ihw_staging}`. Collapsing a
`demo`/`test`/`staging`-suffixed sibling onto its parent is safe and worth
doing before declaring a ticket ambiguous.

**Action for agent 3:** `ecat-session-prep` SKILL.md § 3 drops free-mail
domains as "staff and personal logins". A28 says that is wrong —
`lightingvision@comcast.net` holds accounts at 16 orgs. **Not changed here**;
it is agent 3's file and the fix is one paragraph.

## F. The gate, measured

Two weeks, 27 structurally-open conversations:

```
16  acknowledgments ("Thanks", "Ok, got it")     59%
 3  automated (Lib&Co daily feed)
 1  spam, unflagged by HelpScout
 4  handled out-of-band, provable ONLY from internal notes
 1  ambiguous
 5  genuinely need a reply                       18.5%
```

**Send-safe fraction: well under 20%.** Of the 5 genuine tickets, none is
send-safe. Corroborated across **490 staff first-replies** since 2026-05-01
(median 537 characters): **291 (59.4%)** carry a commitment, apology,
escalation, or money reference, so **at most 40.6%** are even candidates, and
that is a loose upper bound.

> **So agent 4 is a drafting assistant, not an autoresponder** — built and
> described that way, per the recommendation. v1 never sends, in any category.

**The single most valuable behaviour is suppression**, not drafting: 22 of 27
removed. And **reading internal notes is what makes it work** — 4 of the 10
surviving candidates were already resolved and only a note says so (*"Called.
Advised to update the app."*, *"Brent responded in another thread."*). Notes
stay excluded from client-visible reasoning and must still be read.

**Best catch:** ticket **14673, Hubbardton Forge**. We wrote "next week or two"
on 07-06; the client chased on 09-03. **59 days, no client-facing contact**,
`ticket_status` = `active` throughout.

## G. B7 validated against A26

Against `ML + NSL CUSTOMERS COMBINED 2.0.csv` → `mali`:

- **Stage 1 (density)** flags `BillToAddress1` −78.7 pt, `BillToCountry`
  −88.0 pt, City/State/PostCode −13 to −15 pt. Fires at any threshold from 10
  points up, as predicted.
- **Stage 2 (50-row value spot-check)** estimated the postcode disagreement at
  **50%** against A26's row-matched **42%** — the sample works. It also found
  what A26 did not: **`BillToCity` disagrees on 45%** and **`BillToState` on
  26%**. The export does not merely lack addresses, it describes **different
  branches** (`10038`: file `NACOGDOCHES`, live `LUFKIN`). And it caught A26's
  "BillToAddress1 holds contact names" automatically (`16304`: file
  `BILL HALEY`, live `15 COMMERCE DRIVE`).

**NEW AND MORE SERIOUS THAN THE ADDRESSES — `DefaultPriceCode`.** Both sides
are 100% dense, so **stage 1 sees nothing**; only the spot-check catches it:

| | |
|---|---|
| live `mali` | `nsldn` 3,003 · `mldn` 415 |
| the export | `nsllist` 3,096 · `mllist` 421 |

`nsldn` = "NSL DN" (dealer net), `nsllist` = "NSL List". **The export would
move every one of mali's 3,418 customers from dealer-net onto list pricing.**
That is a client-visible repricing of the entire customer base, invisible to
density, invisible to A1, and not recorded in A26. It is the strongest possible
argument for the spot-check having been added.

Negative control: the carried-forward `Ready_For_Import/customers.csv` returns
**PASS** on density, matching live exactly.

B7's own first run also surfaced a defect in itself — it compared
`territory_codes` raw (`["32"]`) against the file's bare `32` and reported
100% disagreement on data that agrees perfectly. Fixed with JSON-aware
normalisation; recorded because it is the §3.4 shape again.

## H. Not done

- `BUILD_SPEC` §3.2 should gain **B7**, and §3.4 its **seventh instance** (D2).
- B7 maps standard columns only. **`products.ecat_custom_field_1..180` are not
  mapped**; they report NOT CHECKED. Wiring B7 to the `custom_fields` registry
  that `b1_fields.py` already reads is the obvious next step.
- The **email ingestion path** (client files arriving as attachments into
  `active_storage_blobs`) was in agent 4's stated scope and is **not built**.
  It is a genuinely separate ingestion surface from HelpScout and needs its own
  pass.
- Agent 4 has been acceptance-tested but **never run in anger**. The fortnight
  comparison in SKILL.md § 9 is the next real test.
