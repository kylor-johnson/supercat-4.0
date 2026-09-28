---
name: ecat-correspondence
description: Watch the eCat support inbox and turn it into drafted replies — decide what actually needs an answer, diagnose it, draft in Kylor's voice, and decide whether the draft is safe to send or needs a human. Use to work the inbox, triage a backlog of tickets, or ask "what is waiting on me". NOT for a single pasted ticket (use ecat-support-triage) and NOT for pre-call prep (use ecat-session-prep). Drafts only — this skill never sends.
---

# eCat Correspondence

Kylor's words: **"replies when 100% sure, pings me otherwise."**

This skill is the **loop and the gate** around two shipped skills. It does not
diagnose and it does not write prose:

| job | owner |
|---|---|
| diagnose a ticket, route it, ground it in live state | **`ecat-support-triage`** |
| write the reply in Kylor's voice | **`ecat-client-email`** |
| decide *which* tickets need a reply at all, and whether a draft may be sent | **this skill** |

If you find yourself writing diagnosis logic or voice rules, stop — you are
rebuilding a skill that already works.

**Read-only throughout. v1 NEVER SENDS.** See § 9, which is a lock, not a
preference.

---

## 1. The one idea

**The inbox does not tell you what is open, and the obvious signals all lie.**

Three of them, each measured, each fatal to the naive implementation:

- **`ticket_status` will not tell you what is open.** Kylor closes as he goes.
  Every `leg` conversation reads `closed`, including one answered thirty
  minutes earlier and one never answered at all.
- **`thread_created_by_type` is not who spoke.** Fleet-wide, 802 of 16,390
  threads typed `customer` were authored from `@supercatsolutions.com` (4.9%);
  in the last quarter it is **248 of 1,811 (13.7%)**. Kylor's own threads are
  typed `customer`.
- **A sender's domain does not identify a client org** (`OPEN_ITEMS A28`). See
  § 5 — this is the one most likely to produce a confident wrong answer.

So openness is **derived from structure**, and even then structure only
produces *candidates*. § 4 is the whole method.

---

## 2. The clock — read this before designing anything around this skill

**The HelpScout mirror in BigQuery is a once-daily batch, not a feed.**

Measured 2026-09-05:

| | |
|---|---|
| `helpscout.conversation_threads` last written | **2026-09-04 22:37 UTC** |
| threads dated 2026-09-05 at 18:54 UTC | **0** — while every weekday in the prior three weeks carries **20–65** |
| average lag from a client message to the batch exposing it | **6.4 hours** |
| worst case | **~24 hours** |

Against that, here is how fast a human already answers (523 conversations
since 2026-06-01):

| | |
|---|---|
| median first staff reply | **226 minutes** |
| answered within 4h | 237 of 411 |
| answered within 24h | 322 of 411 |

Put those together and the consequence is decisive:

> **57% of client messages (1,579 of 2,769 since 2026-03-01) already have a
> human reply before the nightly batch makes them visible to this agent.**

**Therefore this skill is a drafting assistant working a backlog, not an
autoresponder.** An agent on this data path is *structurally* late. That is a
property of the pipeline, not of the model, and no improvement to the gate
changes it. Anything that wanted to answer a live ticket would need the
HelpScout API as a read path (§ 3), not BigQuery.

State the mirror's age in every run's header. A run at 3pm is reasoning about
yesterday evening's inbox.

---

## 3. Inputs, and what write access actually exists

| source | required? | reaches | gives |
|---|---|---|---|
| **BigQuery** `onboarding_assessment.helpscout_tickets` | **REQUIRED** | anywhere (service-account key) | the conversation record |
| **Postgres** `supercat-postgres-vpn` MCP | **OPTIONAL** | VPN only | org attribution, live state to ground a diagnosis |
| harness / `ecat-config-check` output | optional | wherever run | findings to cite, never to re-derive |

### HelpScout write access: NONE, under any identity — checked 2026-09-05

- `https://api.helpscout.net/v2/conversations` → **HTTP 401**. The API is
  reachable; it is authentication that is missing.
- **No HelpScout credential exists on this machine.** Not in
  `~/.supercat/mcp-credentials.json` (Admin Console only), not in the login
  keychain, not in the environment, not in the workspace. The only hits on disk
  are prose mentions in handoff notes.
- BigQuery gets HelpScout through a **Hevo ETL**, which holds its own
  connection to HelpScout. That credential is Hevo's and is read-only to us —
  it is not a write path and cannot be borrowed as one.

**So v1 writes drafts to a file and notifies. That is the design, not a
fallback.**

Because there is no write path, **every drafted ticket must carry its HelpScout
deep link** so the hop from this document to the thread is one click:

```
https://secure.helpscout.net/conversation/<conversation_id>
```

`conversation_id` is a column on the BigQuery view. Verified 2026-09-05 against
an independent source: ticket 15176 → `3426077090`. Use `conversation_id`, NOT
`ticket_number` — the number in the URL is the internal id, and the two differ
(14673 → `3364971115`). If a write path is ever wanted, note that the identity question has
two different answers and they are not interchangeable:

| grant | replies appear as | good for |
|---|---|---|
| OAuth2 **client_credentials** (an app) | the *app*, a bot identity | machine notes, tagging |
| OAuth2 **authorization_code** as Kylor | **Kylor** | a real draft reply in his mailbox |

Only the second produces the thing this skill is for. Getting it means
registering a HelpScout app in the SuperCat account and completing a user
authorization once. **Ask for it explicitly; do not assume the first grant
type will do.**

### Postgres is optional and degrades loudly

Without it the skill still triages and drafts from the conversation record. It
opens with, and repeats at the top of every affected draft:

```
> **Postgres unavailable** (<reason>). Drafted from the conversation record
> only. NOT grounded: org attribution, live counts, import history, image
> coverage, user and login state. Every factual claim below that would need
> live state is marked `unverified` and the draft is NOT send-safe regardless
> of its category.
```

**Without Postgres, nothing is SEND-SAFE.** The gate's whole premise is that
the answer is checkable; if it cannot be checked, it cannot be certain. This is
not caution, it is the definition.

---

## 4. What needs a reply

### 4-0. Scope by inbox and assignee — before anything else (measured 2026-09-25)

The first run drafted eight tickets; four were Kyla's. Kylor's rule, verbatim:

> "i should get all open tickets in the onboarding inbox that are unassigned and
> assigned to me and ONLY support inbox ones that i am assigned to."

| inbox | `mailbox_id` | in scope when |
|---|---|---|
| SuperCat Onboarding | 312855 | `assignee_id` IS NULL or = 889305 (Kylor) |
| SuperCat Support | 65829 | `assignee_id` = 889305 only |

`assignee_id` and `assignee_email` are columns on `helpscout_tickets` as of
2026-09-25 (from `conversations._links.assignee.href`; names in `helpscout.users`,
Kyla = 846447). **Dedupe duplicate captures across inboxes first (§ 4b), then
apply the rule to the group:** a client email captured in both inboxes (#15378
support, #15379 onboarding) is in scope through the onboarding copy. Out-of-scope
candidates are still classified and counted in coverage; they are not drafted.
When this skill runs for Kyla, swap the id.

### 4a. Clean the stream first — and `note` is not the only exclusion

```
thread_type          keep?   why
-------------------  ------  ------------------------------------------------
customer, message    YES     real messages (but see the author-domain rule)
note                 NO      internal, never reached the client
lineitem             NO      982 of 982 are EMPTY — HelpScout system events
                             (assignment, status change). Excluding only
                             `note` leaves these in, and because they all
                             carry the staff domain they read as a STAFF
                             REPLY and mask genuinely unanswered tickets.
phone                FLAG    voicemail notifications from notify@ringcentral
forwardchild/parent  keep    rare, real
```

Then drop `ticket_status = 'spam'`. Status is useless for openness but it is
**reliable for spam**, and that is worth using. It does not catch everything —
one French event-marketing blast in the test window was never flagged.

### 4b. Dedupe at BOTH levels

**Level 1, tickets duplicate.** 21 of 31 `tcd` tickets were captures of 9
conversations. Collapse on subject minus `Re:`/`Fwd:`/`FW:`, repeated —
`Re: Re: Pebl eCat…` occurs live.

**Level 2, threads duplicate inside the collapsed group.** `leg`'s "Settings
tour" is 2 conversations / 10 threads holding **5 unique messages**, captured
twice, sometimes **one second apart** (13:37:17 and 13:37:18). Truncating to
the second does not catch it.

> **Dedupe on `(thread_author_email, LEFT(normalised_body, 200))` and keep the
> earliest.** Then collapse conversations on the normalised subject.

Without level 2 the same open question is listed twice and the run looks
careless.

### 4c. Derive openness from structure

Order the surviving threads by time. Then:

1. Take the **last thread whose author email domain is NOT
   `supercatsolutions.com`** and that is not an automated sender (§ 4d).
2. Ask whether **any staff-authored, non-note, non-lineitem thread follows it.**
3. If none does, the conversation is a **candidate**.

Decide who spoke from **`thread_author_email`'s domain, always** — never
`thread_created_by_type`, and never `primary_customer_domain`, which is wrong
in a way § 5 explains.

**A `note` after the last client thread is not a reply, but it IS evidence.**
Notes are excluded from client-visible reasoning, and must still be *read*:
ticket 15195's last client message is "Please call me", and the resolution is
an internal note reading *"Called. Advised to update the app."* Structurally
open, actually handled, by phone. Surface those as **`possibly handled
out-of-band`** rather than as open.

**Attachments are deliverables, and they are not in the mirror.** The view now
carries `thread_attachment_count`. A client thread with an attachment is flagged
`has-attachment`; if the answer depends on the file (a customer list, an item
list, a cut-sheet list), the draft header says so and the owner action is
"download it from HelpScout into the client folder". Measured 2026-09-25: Jonathan
Charles' user report with emails sat on a closed ticket (#15280) for two weeks
because the CS-admin sentence in the same email had been answered elsewhere and
the run treated the ticket as handled.

### 4d. Automated senders

Measured over three months, only three role local-parts appear at all, and
**none of them ever carried genuine client mail**:

| sender | threads | what it is |
|---|---|---|
| `info@` | 48 | the **Lib&Co daily inventory feed** — a new conversation every single day, never answered, never needing an answer |
| `notify@ringcentral.com` | 14 | voicemail notifications |
| `support@` | 2 | both spam |

Flag on the local-part set `info, notify, noreply, no-reply, donotreply,
support, mailer-daemon, postmaster` — but **flag for review, never silently
drop**. A `notify@ringcentral` voicemail means a client actually rang, which is
a real signal even though the sender is a robot. And note the Lib&Co feed
arrives on a **client domain**: an automation filter keyed on domain would miss
it entirely.

### 4e. The candidate set is dominated by thank-yous, and this is the finding

Structure gets you candidates. It cannot tell a question from a closing
courtesy, and **the courtesies are the majority.**

Two weeks, 2026-08-21 → 09-04, every conversation whose last client-domain
message had no staff reply after it:

```
27  structurally open
16  acknowledgments, needing nothing          59%
 1  unflagged spam
10  candidates surviving the acknowledgment pass
     4  already handled OUT-OF-BAND, provable only from internal notes
     1  ambiguous (client answering our question, closed minutes later)
     5  genuinely needing a reply               18.5% of the 27
```

**Four of the ten were already handled, and only the notes say so** — see
§ 4c. The notes read: *"Called. Advised to update the app."* · *"This issue is
resolved and Brent responded in another thread."* · *"Chatted with Beth this
monday and she said we must not worry about Neil."* · *"my bad… if you're able
to come over the top."* An agent that excludes notes entirely, as the
client-visible rule requires, pings Kylor about all four.

The sixteen are not ambiguous. They read: *"Thanks"* · *"Thank you for changing
it for me!"* · *"ok so all reps updated thanks"* · *"Ok, got it. Thanks for
clarifying!"* · *"Thank you for the confirmation, this ticket can be
resolved."* · *"Internal Will send to the agents. Thanks for knocking
everything out so they can test."*

> **So a second pass is mandatory, and it is a judgement, not a rule.** Read
> the last client message and ask: *does this ask for anything?* Classify it
> `needs-reply` / `acknowledgment` / `automated` / `handled-out-of-band`, and
> **report the counts**. An agent that skips this pass pings Kylor about
> sixteen thank-you notes and gets switched off in a week.

Suppressing the noise is the single most valuable thing this skill does — on
the test window it removes **22 of 27**. Say so in the output: *"27 candidates,
16 acknowledgments and 4 handled out-of-band suppressed, 5 need you."*

---

## 5. Attribution — a sender's domain does not identify an org

`OPEN_ITEMS A28`, and it **directly constrains this skill**. eCat's client-side
population includes multi-line rep agencies and multi-brand dealers who
legitimately hold accounts at many manufacturers. **2,982 accounts sit in 5+
orgs and none of them are staff.**

Measured against the 38 real client domains in the two-week test window:

| domains | orgs each | attribution |
|---|---|---|
| 21 | exactly 1 | **confident** |
| 14 | 2–12 | **ambiguous** — `gabriellawhite.com` is 12 orgs / 480 users; `urbanlightsdenver.com` 9; `lightingreps.net` 5 |
| 3 | 103–165 | **undeterminable from domain** — `gmail.com` reaches 165 orgs and 15,203 users |

**So:**

- **Never infer the org from the sender domain alone.** Disambiguate from the
  org or brand named in the thread, from product codes cited, from the mailbox,
  or from the conversation's own history. If none of those resolve it,
  **refuse to guess** and mark the ticket `org: unattributed` — it is still
  worth drafting, just not worth grounding.
- **Free-mail and personal domains are load-bearing client identities, not
  noise.** `lightingvision@comcast.net` holds accounts at 16 orgs. Do NOT drop
  them. (`ecat-session-prep` § 3 currently drops free-mail as "staff and
  personal logins" — that rule is wrong and A28 says so; it needs narrowing to
  the staff rule below.)
- Several apparent ambiguities are **test/staging twins** and collapse
  cleanly: `alfrescohome.com` → `{ah, ahtest}`, `goldenlighting.com` →
  `{gl, gl_staging}`, `dorellfabrics.com` → `{demo2, drf}`. Treat a
  `demo`/`test`/`staging`-suffixed sibling as the same client.
- **`primary_customer_domain` is not the client either.** Ticket 15244 carries
  `primary_customer_domain = supercatsolutions.com` while the actual client is
  `jhessler@finearthl.com`; 15249 the same, with the client on `legrand.com`.
  Derive the client from the threads.

**The staff rule** (derived and tested, A28) — 96 staff fleet-wide against
70,008 client-side:

```sql
staff = users.billable IS FALSE OR email ILIKE '%@supercatsolutions.com'
```

Only the second half is portable. **Without Postgres you have the domain half
only**, which misses the ~24 staff on personal or contractor domains —
including `kylor22johnson@gmail.com`, an admin on both `leg` and `mer`. Say so
rather than implying the filter was complete. Do **not** use org-count as a
staff signal: it was the obvious signal and A28 refutes it.

### State your coverage — BUILD_SPEC §3.4

Every run reports both denominators, and a zero is never a silent pass:

```
classified   N of M conversations   (M - N could not be classified: <why>)
attributed   N of M conversations   (K ambiguous, J unattributed)
```

A conversation whose org cannot be resolved reports **`unattributed`**, never a
guess and never a default to the largest org on the domain.

---

## 6. The gate

**"100% sure" cannot be a feeling. It has to be a stated property of the
ticket.** Three categories, and the ticket must satisfy *every* clause of one.

### SEND-SAFE
The answer is **deterministic and documented**, and either needs no
client-specific state or needs state that is unambiguous and was actually read.

- an FTP path, a field length limit, an import order, a documented KB procedure,
  a stated UI limit, a URL shape from `ecat-support-triage`'s login table
- **and** the org is confidently attributed (§ 5)
- **and** Postgres was available if any state is claimed
- **and** the reply contains no commitment, no date, no price, no apology

### DRAFT-AND-PING
Anything requiring judgement, a commitment, a date, a price, an apology, a
scheduling decision, or a claim about *when* something will happen. This is the
default. **If you are choosing between categories, it is this one.**

### ESCALATE
Anything where the answer is "we got it wrong", or that touches billing,
contract, cancellation, or a person's competence. Also: a client chasing an
item we already owe them, and any repeat of a previously-reported defect.

> Test-window examples, all real: *"Cancellation of Service"* (`ESCALATE`) ·
> *"We're seeing this issue again with the new build"* (`ESCALATE` — a
> regression we already shipped a fix for) · *"I just wanted to follow up on
> this as it has been a while. Any movement on your end?"* (`ESCALATE` — a
> chase on something we owe) · *"Can we set something up for Thursday
> afternoon the 15th, around 4/4:30pm?"* (`DRAFT-AND-PING` — a date) ·
> *"I thought that any order that was submitted could be reopened and
> edited?"* (`SEND-SAFE` candidate — documented product behaviour).

### What fraction is genuinely send-safe? Measured: well under 20%

Of the 5 genuinely-open tickets in the test window, **none is send-safe**.
Across the wider 10-candidate set, **1, arguably 2** — the "can a submitted
order be reopened" question, which is documented product behaviour.

Corroborated across a far larger sample. Of **490 staff first-replies** since
2026-05-01 (median length 537 characters — these are substantive, not
one-liners):

| marker in the reply Kylor or Kyla actually sent | count | share |
|---|---|---|
| a forward commitment (*"I'll…"*, *"we'll…"*, *"by Friday"*) | 261 | 53% |
| an apology | 60 | 12% |
| an escalation to engineering | 44 | 9% |
| money, invoice, billing or contract | 46 | 9% |
| **any of the above** | **291** | **59.4%** |

So **at most 40.6% of real replies are even candidates** for send-safety, and
that is a loose upper bound — a reply with no commitment language can still
need client-specific state or be wrong. The hand-classified rate is **10–20%**.

> **Design consequence, stated plainly: this is a drafting assistant, not an
> autoresponder.** Four of every five tickets need Kylor. That is still
> valuable — it suppresses the 59% that need nothing and it drafts the rest —
> but it must be built and described as an assistant. A gate tuned
> optimistically would be a worse v1.

---

## 7. Building each draft

**Step 0, consolidate per client before drafting (added 2026-09-25).** Three of
the first run's four in-scope drafts were stale or wrong for one reason: the
context lived in other threads, calls, and attachments. For each client with a
needs-reply thread, gather first:

- every conversation with that client in the last 30 days, **any status** — the
  answered ones carry open asks too;
- every Fathom meeting with the client's domain in the last 14 days (summary;
  transcript when a commitment is going into copy);
- every Google Calendar event with an attendee on the client's domain in the last
  7 days. **When an event exists and Fathom has no matching recording, the draft
  header says "You met them on <date> at <time>; this run cannot see that
  meeting; give me three lines before this goes", the copy carries an
  `[ITEMS]` block, and the category stays DRAFT-AND-PING.** Measured: the
  Legrand launch training, 2026-09-25 10:00 MDT, 120+ attendees, no recording,
  after a draft to them had been marked SEND-SAFE;
- the client folder under `02_Implementation/`;
- any thread flagged `has-attachment` (§ 4c).

Then decide the form: a reply in-thread, or **one recap note in a new thread**
that lists done / in progress / what the client owes / which threads to close.
Onboarding clients mid-build default to the recap. Name the threads to close.

For every `needs-reply` conversation, in order:

1. **Attribute the org** (§ 5), or mark `unattributed`.
2. **Diagnose with `ecat-support-triage`.** It classifies the symptom, routes
   to the right `ecat-*` skill, and grounds in live state. Do not duplicate it.
3. **VERIFY, and show it.** Every draft carries this table; each row is cited
   or reads `NOT CHECKED`; a blank row fails § 10.

   | evidence | what counts |
   |---|---|
   | thread | the quotes, dated and attributed; last client and last staff timestamps from `helpscout_tickets` |
   | live state | every noun in the copy that is a state (a flag, a count, a price, a login, a phone number) read from Postgres with table and timestamp; **every commitment taken from a meeting summary is checked here before it is written as done** (measured: four of nine 111 Mercer call commitments were not in the database). **A clean import is not correct data:** for any "did the file land / is it working" question, read the values a rep will see after the import (e.g. share of `inventories.qty_available` non-null, the custom-field columns populated), not only the import event (measured: an inventory import with a clean log delivered zero quantities reps could see, because the file carried only prefixed custom columns) |
   | code | any claim about how the product behaves cited to source on GitHub, shallow clone, commit SHA and `file:line`; never memory, never the local checkout. **Server:** `SuperCatSolutionsLLC/supercat_server` (master). **iPad:** `SuperCatSolutionsLLC/sarreid_ios` — master lags; clone the newest `release/*` branch (2026-09-28: `release/2026.3.1` = build 20260909; August builds ≈ `release/2026.2.10`, plist 20260818) and match it to the rep's `orders.app_version`. Search, option-set handling, order state and presentation building run on the device; four of ten batch-1 replays needed this |
   | KB | the article URL, or "none exists", which is a KB backlog item |
   | meetings | Fathom recording id or calendar event id, or "none" |

   Names in copy come from `users.first_name` / `last_name`, never from a
   username (measured: `millert` became "Mike"; she is Tracy Miller).
   No Postgres → nothing is send-safe.
4. **Draft with `ecat-client-email`.** Its rules bind: mirror their structure,
   no em-dashes, no AI slop, honest about limits, exact next action and owner,
   **"Best, Kylor"**.
5. **Owner actions.** The numbered steps Kylor performs before the copy is
   true, per `ecat-client-email` § Owner actions. If the copy promises the
   client something, this section says how it gets made.
6. **Categorise** (§ 6) and record *which clause* decided it.
7. **Record what it WOULD have sent** under the gate, whether or not the
   category is SEND-SAFE. That record is the fortnight experiment in § 9.
8. **"Also found."** Anything true that the live read surfaced and the reply
   does not need goes in a separate list at the end of the draft file, never
   into another revision of the email.

Two copy rules from replay batch 1 (2026-09-27):

- **Every path, then a recommendation.** For a setup question (a domain, an
  option, an access model), list every route the code allows before
  recommending one. A draft offered "register a new domain" and missed a
  subdomain of a domain the client already owns, which was the fastest path.
- **Something to try before something to send.** When a permission or setting
  is proven correct and the symptom is on one device, lead with the cheap client
  action (full sync, update the app) and ask for evidence only if it persists.

Carry `ecat-support-triage`'s discipline: check for an existing Jira ticket
before drafting a "logged with engineering" reply, and never claim something is
fixed or uploaded until it is.

**Separate what was said from what you concluded**, exactly as
`ecat-session-prep` does:

| kind | how it appears |
|---|---|
| what the client said | `> "..."` blockquote, dated and attributed |
| what was measured | a count or timestamp, **with the table it came from** |
| what you concluded | prefixed **`Conclusion:`** |

The programme's most expensive error was a consequence stated as a
measurement, and it reached a client (`OPEN_ITEMS §F1`). The gate is exactly
where that recurs.

---

## 8. Output

One markdown document, plus one file per draft. Header first.

````markdown
# Inbox run — <date>
**Mirror:** HelpScout via BigQuery, last loaded <ts> (**<N>h old**)
**Sources:** BigQuery ✅ · Postgres <✅ | ❌ + reason>
**Window:** <from> → <to>

Coverage
  classified   27 of 27 conversations
  attributed   21 confident · 5 ambiguous · 1 unattributed
  suppressed   16 acknowledgments · 3 automated · 1 spam
  needs reply  10

> ⚠ 6 of these 10 already had a human reply before this run could see them.

## Needs you (10)
| # | client | org | subject | last client | category | why | open |
|---|---|---|---|---|---|---|---|
| 1 | Jamie Young | `jyc` | duplicated lines on order emails | 09-04 21:39 | DRAFT-AND-PING | product defect, no documented answer | [#15256](https://secure.helpscout.net/conversation/3441558657) |

## Suppressed (20) — one line each, so the judgement is auditable
- `acknowledgment` Braxton Culler, "Thank you for changing it for me!" (09-02)
- `automated` Lib&Co Inventory Feed, daily, 09-01…09-04 (4 conversations)

## Drafts
### 1. Jamie Young (`jyc`) — DRAFT-AND-PING
**Thread:** https://secure.helpscout.net/conversation/3441558657 (#15256)
**Category clause:** a product defect with no documented answer; needs a
commitment about a fix.
**Grounded:** ✅ Postgres — `jyc` order email template, 3 orders affected
**Would have sent under the gate:** NO
> "Some of our orders are coming in with duplicated first lines…" — Charlee
> Lowery, 09-04
```
<the draft, ready to paste>
```
````

Cap the ping list at what a person will actually read. If more than ~12 need
a reply, rank by age of the oldest unanswered client message and say what was
held back.

---

## 9. This skill does not send. Ever.

**v1 never auto-sends, in any category, including SEND-SAFE.** It always
drafts, always notifies, and always records what it *would* have sent.

The reason is measured, not cautious, and there are two independent ones:

1. **The clock (§ 2).** 57% of client messages already have a human reply
   before this agent can see them. Auto-sending onto a batch that late means
   replying to answered tickets.
2. **The cost asymmetry.** This programme's most expensive error was a
   confident false statement reaching a client. An unsent draft costs nothing;
   a wrong sent reply costs a client's trust and a day of repair.

**How auto-send would ever be justified:** run this for a fortnight, then
compare the SEND-SAFE calls against what Kylor actually sent. If the drafts he
would have sent unedited match the SEND-SAFE set with no false positives, that
is evidence. Fewer than ~20 SEND-SAFE calls in the window is not enough
evidence either way — say so rather than concluding.

> **A future session must not quietly turn this on.** Enabling send requires
> (a) a HelpScout write credential that does not exist today (§ 3), (b) the
> fortnight comparison above, and (c) Kylor saying so explicitly. Absent all
> three, this skill drafts.

---

## 10. Before you hand it over

- [ ] Mirror age stated in the header, in hours
- [ ] `lineitem` and `note` excluded from "did we reply"; notes still **read**
      for out-of-band resolution
- [ ] Deduped at BOTH levels — threads, then conversations
- [ ] Openness derived from **author domain**, never `ticket_status`,
      `thread_created_by_type`, or `primary_customer_domain`
- [ ] Acknowledgment pass run; suppressed items listed one line each
- [ ] No org attributed from a sender domain alone; free-mail not dropped
- [ ] Coverage stated with both denominators; nothing unclassified reported
      as a pass (`BUILD_SPEC §3.4`)
- [ ] Every quote dated and attributed; every count names its table; every
      judgement prefixed `Conclusion:`
- [ ] No consequence stated as a measurement (`§F1`)
- [ ] Postgres unavailable → nothing marked SEND-SAFE
- [ ] Every drafted ticket carries its `conversation_id` deep link
- [ ] Scope rule (§ 4-0) applied after cross-inbox dedupe; out-of-scope
      candidates counted, not drafted
- [ ] Per-client consolidation done (§ 7 step 0); recap-vs-reply decided;
      threads to close named
- [ ] VERIFY table on every draft, no blank rows; names from `users`, not
      usernames; meeting commitments checked against live state
- [ ] Calendar checked for unrecorded meetings; `[ITEMS]` block where one exists
- [ ] Owner actions section on every draft
- [ ] `has-attachment` threads flagged; file-dependent answers say so
- [ ] Nothing sent. Drafts only.

**The test is whether Kylor sends the draft unedited.** Iterate on that answer,
not on how many tickets were covered.

---

## Appendix — the acceptance run, 2026-08-21 → 09-04

Run against the real inbox while building this skill. Every number here is
measured, and the section exists so the next session can re-run it and compare
rather than re-deriving.

```
27  conversations structurally open (last client-domain message, no staff reply after)
16  acknowledgments             suppressed
 3  automated (Lib&Co feed)     suppressed
 1  spam, unflagged by HelpScout suppressed
 4  handled out-of-band         suppressed — visible ONLY in internal notes
 1  ambiguous                   listed, flagged
 5  genuinely need a reply      18.5%
```

Coverage: **classified 27 of 27.** Attribution: 21 of 27 confident, 5
ambiguous (`gabriellawhite.com` at 12 orgs, `interludehome.com` at 3), 1
unattributed (`gmail.com`).

**The catch that justifies the skill:** ticket **14673, Hubbardton Forge**. On
07-06 we wrote *"we'll reach out to schedule a call… in the next week or two."*
On 09-03 Kelly Murphy wrote *"I just wanted to follow up with you on this as it
has been a while. Any movement on your end?"* — **59 days, no client-facing
contact.** `ticket_status` reads `active`, which says nothing; the last staff
reply is two months stale, which says everything. Nothing else in this
programme surfaces that.

It is also a clean worked example of the gate:

> **ESCALATE.** Not because the topic is sensitive, but because the honest
> answer is *"we said two weeks and it has been two months"*, and because the
> agent **cannot know the engineering status** — the note says the scoping was
> handed to `@brentS` and a support Project was opened, and nothing since says
> what happened. A draft that guesses at status would be the exact failure
> mode this programme has paid for twice. The draft owns the miss, states only
> what is provable, and leaves the status sentence for Kylor to complete.

Two false-negative risks worth re-testing on the next run, both of which this
version accepts rather than hides:

- **The acknowledgment pass is a judgement.** *"Thank you Kyla. We're looking
  into this."* is an acknowledgment; *"Thanks — will that work for the
  October file?"* is not. Misreading one drops a real question.
- **The out-of-band rule depends on someone having written a note.** Four
  tickets were resolved silently and only the note proves it. A ticket handled
  by phone with no note is indistinguishable from a dropped one, and this
  skill will surface it as needing a reply. That is the right direction to
  fail in.
