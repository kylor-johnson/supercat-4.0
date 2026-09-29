---
name: ecat-correspondence
description: Watch the eCat support inbox and turn it into drafted replies — decide what actually needs an answer, diagnose it, draft in Kylor's voice, and decide whether the draft is safe to send or needs a human. Use to work the inbox, triage a backlog of tickets, or ask "what is waiting on me". NOT for a single pasted ticket (use ecat-support-triage) and NOT for pre-call prep (use ecat-session-prep). Drafts only — this skill never sends.
---

# eCat Correspondence

The owner's words: **"replies when 100% sure, pings me otherwise."**

This skill is the **loop and the gate** around two shipped skills. It does not
diagnose and it does not write prose:

| job | owner |
|---|---|
| diagnose a ticket, route it, ground it in live state | **`ecat-support-triage`** |
| write the reply in the owner's voice, and the copy-truth checklist | **`ecat-client-email`** |
| decide *which* tickets need a reply at all, and whether a draft may be sent | **this skill** |

If you find yourself writing diagnosis logic or voice rules, stop — you are
rebuilding a skill that already works.

**Read-only throughout. v1 NEVER SENDS** (§ 8, a lock, not a preference).
Measurements behind these rules are in `reference/BACKGROUND.md`; read it when a
rule's reason matters, not on every run.

---

## 0. Run order and precedence (read first)

1. **Scope** (§ 3a) decides whether a ticket is drafted at all.
2. **Clean, dedupe, derive openness, acknowledgment pass** (§ 3b–3f).
3. **Attribute** each candidate (§ 4).
4. **Per client: consolidate** (§ 6 step 0). Then per ticket: triage GROUND →
   VERIFY → draft → owner actions → category (§ 5) → also found.
5. **Output** (§ 7) and **checklist** (§ 9).

When rules meet:

- **Scope beats the gate.** An out-of-scope ticket is classified and counted, never
  drafted, and never carries a category.
- **Category precedence: ESCALATE > DRAFT-AND-PING > SEND-SAFE.** Any ESCALATE
  trigger wins. SEND-SAFE only when every clause holds. Unsure → DRAFT-AND-PING.
- **Replay mode** (a blind packet with a cut time T, run under
  `tools/DRAFTING_BRIEF.md`) overrides this skill in three places only: the ticket
  is drafted whatever its scope, and the header states the scope plus "category if
  in scope"; the reply answers the last client message in-thread (no recap note);
  data sources and cut rules are the brief's. Everything else here binds.

---

## 1. The one idea

**The inbox does not tell you what is open, and the obvious signals all lie.**

- **`ticket_status` will not tell you what is open.** Staff close as they go; a
  closed ticket can be unanswered and an active one can be done.
- **`thread_created_by_type` is not who spoke.** Staff threads are often typed
  `customer` (13.7% of `customer` threads last quarter were staff-authored).
- **A sender's domain does not identify a client org** (§ 4). This is the one most
  likely to produce a confident wrong answer.

So openness is **derived from structure**, and structure only produces
*candidates*. § 3 is the method.

---

## 2. Inputs and the clock

| source | required? | gives |
|---|---|---|
| **BigQuery** `onboarding_assessment.helpscout_tickets`, through the `bigquery-admin` MCP tool only (never a service-account key in a script) | **REQUIRED** | the conversation record, incl. `assignee_id`, `thread_attachment_count` |
| **Postgres** `supercat-postgres-vpn` MCP (SELECT only) | optional, degrades loudly | org attribution, live state to ground a diagnosis |
| harness / `ecat-config-check` output | optional | findings to cite, never to re-derive |

- **The mirror lags.** Measured 2026-09-05 it was a daily batch with a 6.4 h average
  lag, and 57% of client messages already had a human reply before the agent could
  see them. State the mirror's age (latest `thread_created_at`) in hours in every
  run's header.
- **There is no HelpScout write access** under any identity. v1 writes drafts to a
  file, and **every drafted ticket carries its deep link**
  `https://secure.helpscout.net/conversation/<conversation_id>` (`conversation_id`,
  not `ticket_number`; they differ).
- **Without Postgres, nothing is SEND-SAFE.** Open the run, and every affected draft,
  with:

```
> **Postgres unavailable** (<reason>). Drafted from the conversation record
> only. NOT grounded: org attribution, live counts, import history, image
> coverage, user and login state. Every factual claim below that would need
> live state is marked `unverified` and the draft is NOT send-safe regardless
> of its category.
```

---

## 3. What needs a reply

### 3a. Scope by inbox and assignee, before anything else

The owner's rule, verbatim (2026-09-25):

> "i should get all open tickets in the onboarding inbox that are unassigned and
> assigned to me and ONLY support inbox ones that i am assigned to."

| inbox | `mailbox_id` | in scope when |
|---|---|---|
| SuperCat Onboarding | 312855 | `assignee_id` IS NULL or = 889305 (owner) |
| SuperCat Support | 65829 | `assignee_id` = 889305 only |

Names are in `helpscout.users` (support lead = 846447). **Dedupe duplicate captures
across inboxes first (§ 3c), then apply the rule to the group:** an email captured in
both inboxes is in scope through the onboarding copy. Out-of-scope candidates are
classified and counted, not drafted. When this runs for the support lead, swap the id.
Measured: the first run drafted eight tickets and four belonged to someone else.

### 3b. Clean the stream, and `note` is not the only exclusion

```
thread_type          keep?   why
-------------------  ------  ------------------------------------------------
customer, message    YES     real messages (but decide the author by domain)
note                 NO      internal, never reached the client (still READ, § 3d)
lineitem             NO      all empty HelpScout system events carrying the staff
                             domain; left in, they read as a staff reply and mask
                             unanswered tickets
phone                FLAG    voicemail notifications
forwardchild/parent  keep    rare, real
```

Then drop `ticket_status = 'spam'`: useless for openness, reliable for spam (not
complete; one marketing blast was never flagged).

### 3c. Dedupe at both levels

- **Tickets:** collapse on subject minus `Re:`/`Fwd:`/`FW:`, repeated (`Re: Re:`
  occurs live).
- **Threads inside the group:** the same message is captured twice, sometimes one
  second apart, so truncating to the second does not catch it. **Dedupe on
  `(thread_author_email, LEFT(normalised_body, 200))`, keep the earliest**, then
  collapse conversations on the normalised subject.

### 3d. Derive openness from structure, then read what structure hides

1. Take the **last thread whose author email domain is NOT
   `supercatsolutions.com`** and that is not an automated sender (§ 3e).
2. Ask whether **any staff-authored, non-note, non-lineitem thread follows it.**
3. If none does, the conversation is a **candidate**.

Decide who spoke from **`thread_author_email`'s domain, always**, never
`thread_created_by_type` and never `primary_customer_domain`.

- **A note after the last client thread is not a reply, but it IS evidence.** "Please
  call me" followed by a note "Called. Advised to update the app." is handled by phone.
  Surface those as **`possibly handled out-of-band`**, not open.
- **Attachments are deliverables, and they are not in the mirror.** A client thread
  with `thread_attachment_count > 0` is flagged `has-attachment`. If the answer
  depends on the file, the header says so and the owner action is "download it from
  HelpScout into the client folder". Measured: a client's user report sat on a closed
  ticket for two weeks because another sentence in the same email had been answered.
- **An unseen screenshot is answered for every surface that shows the thing.** When the
  question points at an attachment you can't open ("see attached", "this field"), list
  each place that field or message appears (Admin Console, Sales Portal, iPad, eCat
  Online), answer for each in a line, and ask which one they were on. Measured: a draft
  guessed Admin for a field shown on the Sales Portal customer list and left the real
  follow-up ("can we hide it there?") for a second round. **When the unseen thing is an
  error message**, don't name a "most likely" cause or a fix in the copy; say what the
  live read shows, ask for the exact text, and keep candidate causes in the draft file.
  Measured: a draft's "most likely" cause and its fix would have hit the same ERP
  rejection again.
- **A forward carries the complaint below its From: line.** On a `FW:` thread, or a
  short internal note like "see below", read the forwarded message in full and quote
  the original sender, not the forwarder.

### 3e. Automated senders

Flag on the local-part set `info, notify, noreply, no-reply, donotreply, support,
mailer-daemon, postmaster`, **for review, never silently dropped**. A
`notify@ringcentral.com` voicemail means a client rang. A daily inventory feed arrives
from `info@` on a **client domain**, so a domain-keyed filter misses it.

### 3f. The acknowledgment pass (mandatory, and a judgement)

Most candidates are courtesies (59% in the acceptance window). Read the last client
message and ask: *does this ask for anything?* Classify `needs-reply` /
`acknowledgment` / `automated` / `handled-out-of-band`, and **report the counts**:
*"27 candidates, 16 acknowledgments and 4 handled out-of-band suppressed, 5 need
you."* "Thanks, will that work for the October file?" is not an acknowledgment.

---

## 4. Attribution: a sender's domain does not identify an org

Rep agencies and multi-brand dealers hold accounts at many manufacturers (2,982
accounts sit in 5+ orgs, none staff). One domain can reach 12 orgs; free-mail reaches
over 100.

- **Never infer the org from the sender domain alone.** Disambiguate from the org or
  brand named in the thread, product codes cited, the mailbox, or the conversation's
  own history. If none resolve it, **refuse to guess**: `org: unattributed` (still
  worth drafting, not worth grounding).
- **Free-mail and personal domains are client identities, not noise.** Do not drop
  them. (`ecat-session-prep` § 3 drops free-mail as "staff and personal logins"; that
  rule is wrong per A28 and needs narrowing to the staff rule below.)
- **Test/staging twins collapse:** a `demo`/`test`/`staging`-suffixed sibling org is
  the same client.
- **`primary_customer_domain` is not the client either** (it has read
  `supercatsolutions.com` on client tickets). Derive the client from the threads.

**The staff rule** (A28): `staff = users.billable IS FALSE OR email ILIKE
'%@supercatsolutions.com'`. Only the second half is portable; without Postgres you
miss the ~24 staff on personal or contractor domains, so say so. Do **not** use
org-count as a staff signal.

**State coverage, both denominators, never a silent zero (BUILD_SPEC §3.4):**

```
classified   N of M conversations   (M - N could not be classified: <why>)
attributed   N of M conversations   (K ambiguous, J unattributed)
```

---

## 5. The gate

**"100% sure" cannot be a feeling. It is a stated property of the ticket.** The
ticket must satisfy *every* clause of its category; precedence is in § 0.

### SEND-SAFE
The answer is **deterministic and documented**, and needs either no client-specific
state or state that is unambiguous and was actually read:

- an FTP path, a field length limit, an import order, a documented KB procedure, a
  stated UI limit, a URL shape from `ecat-support-triage`'s login table
- **and** the ticket is in scope (§ 3a)
- **and** the org is confidently attributed (§ 4)
- **and** Postgres was available if any state is claimed
- **and** every behaviour claim in the copy is cited to code or a KB article
- **and** the reply contains no commitment, no date, no price, no apology

### DRAFT-AND-PING
Anything requiring judgement, a commitment, a date, a price, an apology, a
scheduling decision, a claim about *when* something will happen, or an answer that
depends on an attachment the run could not open. **The default.**

### ESCALATE
Anything where the answer is "we got it wrong" (including a wrong claim in our own
earlier reply, corrected by name, § 6 step 0), or that touches billing, contract,
cancellation, or a person's competence. Also: a client chasing an item we already owe
them, and any repeat of a previously-reported defect.

> Shapes: "Cancellation of Service" (ESCALATE) · "We're seeing this issue again with
> the new build" (ESCALATE, a regression we shipped a fix for) · "Any movement on your
> end?" after a promised follow-up (ESCALATE, a chase) · "Can we set something up for
> Thursday afternoon?" (DRAFT-AND-PING, a date) · how a documented behaviour works
> (SEND-SAFE candidate, once confirmed in code).

Measured: at most 40% of real replies are even candidates, and the hand-classified
send-safe rate is 10–20%. **This is a drafting assistant, not an autoresponder.** A
gate tuned optimistically would be a worse v1.

---

## 6. Building each draft

**Step 0, consolidate per client before drafting.** Three of the first run's four
in-scope drafts were stale or wrong because the context lived in other threads,
calls and attachments. For each client with a needs-reply thread, gather:

- every conversation with that client in the last 30 days, **any status** (answered
  ones carry open asks too);
- every Fathom meeting with the client's domain in the last 14 days (summary;
  transcript when a commitment goes into copy);
- every Google Calendar event with an attendee on the client's domain in the last 7
  days. **When an event exists and Fathom has no matching recording, the header says
  "You met them on <date> at <time>; this run cannot see that meeting; give me three
  lines before this goes", the copy carries an `[ITEMS]` block, and the category stays
  DRAFT-AND-PING.** Measured: an unrecorded launch training with 120+ attendees
  happened after a draft to that client had been marked SEND-SAFE;
- the client folder under `02_Implementation/`;
- any `has-attachment` thread (§ 3d);
- **every factual claim in our earlier replies on those threads**, checked against
  live state and code; a wrong one is corrected by name in this reply (ESCALATE);
- any dated decision on the thing the client calls wrong
  (`onboarding-agents/1-ingestion/config_intent.toml`, the client folder, earlier
  threads, meetings); if one exists, the reply restates what was agreed and what
  changing it takes.

Then decide the form: a reply in-thread, or **one recap note in a new thread** listing
done / in progress / what the client owes / which threads to close. Onboarding
clients mid-build default to the recap. Name the threads to close.

For every `needs-reply` conversation, in order:

1. **Attribute the org** (§ 4), or mark `unattributed`.
2. **Diagnose with `ecat-support-triage`.** It classifies, routes to the domain
   skill, and grounds (its GROUND step says where code and iPad source come from and
   what to check before asking the client anything). Do not duplicate it.
3. **VERIFY, and show it.** Every draft carries this table. Each row is cited or reads
   `NOT CHECKED`; a blank row fails § 9.

   | evidence | what counts |
   |---|---|
   | thread | the quotes, dated and attributed; last client and last staff timestamps from `helpscout_tickets` |
   | live state | every noun in the copy that is a state (a flag, a count, a price, a login, a phone number), read from Postgres with table and `updated_at`; checks below |
   | code (server) | behaviour cited to supercat_server, commit SHA and `file:line` (source per triage GROUND) |
   | code (iPad) | on-device behaviour cited to sarreid_ios, branch matched to the rep's `orders.app_version` |
   | KB | the article URL, or "none exists" (a KB backlog item) |
   | meetings | Fathom recording id or calendar event id, or "none" |
   | Jira | keys read (read-only), or "none" |

   **Live-state checks** (each one measured on a miss):
   - **Meeting commitments are checked here before they are written as done.**
     Measured: four of nine commitments from one onboarding call were not in the DB.
   - **A clean import is not correct data.** For "did the file land / is it working",
     read the values a rep will see after the import (share of
     `inventories.qty_available` non-null, the custom-field columns populated), not
     only the import event. Measured: a clean inventory import delivered zero
     quantities reps could see, because the file carried only prefixed custom columns.
   - **When those values can't be read** (the table was reloaded after the client's
     message), the copy asks the client to confirm the columns that drive them. It
     never says "no action needed".
   - **An empty figure is a data question first.** When a value the client asks about
     is blank (a total, a freight or tax line, a quantity, a URL), count how many of
     the org's rows have it blank before proposing any display change. Blank
     everywhere means the feed or file mapping, and that goes in the copy ahead of any
     label or disclaimer workaround. Measured: a draft offered a disclaimer for missing
     freight and tax that were NULL on every invoice loaded since June.
   - **Nested settings.** A Rails `property` / `flags` value lives in JSON (e.g.
     `mobile_sites.properties->'flags'->'<name>'`); read the model's getter for the
     storage path before querying, or a set flag reads as unset.
   - **Views fall back.** A user group's Quick View / order-preview view whose lines
     are all blank inherits the org's (`user_type.rb:415-432`,
     `ipad_custom_views_for_rendering`, supercat_server 183d8e1); judge what a group
     sees from the rendered view, not the group column.

   - **"Looks resolved" needs a before and an after.** Evidence that something works
     now (an order with a discount, a login that succeeded) shows it is fixed only if
     the same evidence was absent before the client's report. Measured: a draft called
     a permission issue resolved from orders carrying line discounts, and one of those
     orders predated the report by 90 minutes.
   - **"Never" and "none" need the whole search.** A claim that something did not
     happen ("no import event names that customer", "no order on that build") names
     the query, and covers older message formats and every table that could hold it;
     otherwise write "not found in <query>". Measured: a draft told the owner to doubt
     a true line in our own earlier reply because its search missed 154 events in an
     older message format.

   **Code checks:**
   - **A flag cited as a blocker lists where it is checked.** Grep the flag's call
     sites (Admin nav, eOL view, API/sync, iPad) and say which surfaces it gates.
     Measured: a feature flag presented as required for a form gated only the Admin
     menu and the eOL view.
   - **Recent changes:** `git log` the files on the code path for the 30 days before
     the client's message; a merged fix is often the answer.
   - **Pages:** a claim about what a page shows needs a logged-in fetch of that page,
     or is labelled "code path only, no populated row rendered".

4. **Draft with `ecat-client-email`.** Its voice rules and pre-send checklist bind
   (plain text, no em-dashes, no slop, honest about limits, exact next action and
   owner, no past-tense action that hasn't happened, names from `users`, **"Best,
   Kylor"**).
5. **Owner actions.** The numbered steps the owner performs before the copy is true,
   per `ecat-client-email` § Owner actions.
6. **Categorise** (§ 5) and record *which clause* decided it.
7. **Record what it WOULD have sent** under the gate, whatever the category (the
   fortnight experiment, § 8).
8. **"Also found."** Anything true the live read surfaced that the reply does not
   need goes in a separate list at the end of the draft file, never into another
   revision of the email.

**Copy rules** (from replays):

- **Every path, then a recommendation.** For a setup question (a domain, an option,
  an access model), list every route the code allows before recommending one.
  Measured: a draft offered "register a new domain" and missed a subdomain of a domain
  the client already owned. When two paths exist and one changes the client's data or
  what their users see, offer both and ask; do not pick for them.
- **Something to try before something to send.** When a permission or setting is
  proven correct and the symptom is on one device, lead with the cheap client action
  (full sync, update the app) and ask for evidence only if it persists. On eOL, when
  the code, config and data behind the symptom are unchanged, the cheap action is hard
  refresh, then an incognito window, then clearing cookies for the site.

**Separate what was said from what you concluded** (as `ecat-session-prep` does):

| kind | how it appears |
|---|---|
| what the client said | `> "..."` blockquote, dated and attributed |
| what was measured | a count or timestamp, **with the table it came from** |
| what you concluded | prefixed **`Conclusion:`** |

The programme's most expensive error was a consequence stated as a measurement, and it
reached a client (`OPEN_ITEMS §F1`). The gate is where that recurs.

---

## 7. Output

One markdown document, plus one file per draft. Header first.

````markdown
# Inbox run — <date>
**Mirror:** HelpScout via BigQuery, latest thread <ts> (**<N>h old**)
**Sources:** BigQuery ✅ · Postgres <✅ | ❌ + reason>
**Window:** <from> → <to>

Coverage
  classified   27 of 27 conversations
  attributed   21 confident · 5 ambiguous · 1 unattributed
  out of scope 12 (counted, not drafted)
  suppressed   16 acknowledgments · 3 automated · 1 spam
  needs reply  10

> ⚠ 6 of these 10 already had a human reply before this run could see them.

## Needs you (10)
| # | client | org | subject | last client | category | why | open |
|---|---|---|---|---|---|---|---|
| 1 | <contact> | `<org>` | <subject> | 09-04 21:39 | DRAFT-AND-PING | product defect, no documented answer | [#<ticket>](https://secure.helpscout.net/conversation/<conversation_id>) |

## Suppressed (20) — one line each, so the judgement is auditable
- `acknowledgment` <contact>, "Thank you for changing it for me!" (09-02)
- `automated` <client> inventory feed, daily, 09-01…09-04 (4 conversations)

## Drafts
### 1. <contact> (`<org>`) — DRAFT-AND-PING
**Thread:** https://secure.helpscout.net/conversation/<conversation_id> (#<ticket>)
**Category clause:** <the § 5 clause that decided it>
**Grounded:** ✅ Postgres — <what was read>
**Would have sent under the gate:** NO
> "<the client's words>" — <contact>, <date>
```
<the draft, ready to paste>
```
````

Cap the ping list at what a person will actually read. If more than ~12 need a reply,
rank by age of the oldest unanswered client message and say what was held back.

---

## 8. This skill does not send. Ever.

**v1 never auto-sends, in any category, including SEND-SAFE.** It drafts, notifies,
and records what it *would* have sent. Two independent reasons: the clock (§ 2: most
client messages already have a human reply before this agent can see them), and the
cost asymmetry (an unsent draft costs nothing; a wrong sent reply costs a client's
trust).

**How auto-send would ever be justified:** run for a fortnight, then compare the
SEND-SAFE calls against what the owner actually sent. No false positives across 20+
SEND-SAFE calls is evidence; fewer than ~20 is not enough either way, so say so.

> **A future session must not quietly turn this on.** Enabling send requires (a) a
> HelpScout write credential that does not exist today (§ 2), (b) the fortnight
> comparison above, and (c) the owner saying so explicitly. Absent all three, this
> skill drafts.

---

## 9. Before you hand it over

- [ ] Mirror age stated in the header, in hours
- [ ] Scope rule (§ 3a) applied after cross-inbox dedupe; out-of-scope counted, not drafted, no category
- [ ] `lineitem` and `note` excluded from "did we reply"; notes still **read** for out-of-band resolution
- [ ] Deduped at both levels — threads, then conversations
- [ ] Openness derived from **author domain**, never `ticket_status`, `thread_created_by_type`, or `primary_customer_domain`
- [ ] Acknowledgment pass run; suppressed items listed one line each
- [ ] No org attributed from a sender domain alone; free-mail not dropped
- [ ] Coverage stated with both denominators; nothing unclassified reported as a pass
- [ ] Per-client consolidation done (§ 6 step 0); recap-vs-reply decided; threads to close named
- [ ] Calendar checked for unrecorded meetings; `[ITEMS]` block where one exists
- [ ] `has-attachment` threads flagged; file-dependent answers say so; unseen screenshots answered per surface
- [ ] VERIFY table on every draft, no blank rows
- [ ] Every quote dated and attributed; every count names its table; every judgement prefixed `Conclusion:`; no consequence stated as a measurement (`§F1`)
- [ ] `ecat-client-email` pre-send checklist run on every draft; Owner actions present
- [ ] Postgres unavailable → nothing marked SEND-SAFE
- [ ] Every drafted ticket carries its `conversation_id` deep link
- [ ] Nothing sent. Drafts only.

**The test is whether every fact in the draft is true and the draft needs no edit.**
Iterate on that, not on how many tickets were covered.
