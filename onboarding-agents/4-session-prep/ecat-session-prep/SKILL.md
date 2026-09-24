---
name: ecat-session-prep
description: Build the ten-minute brief a human reads before a working session with an eCat client — what has moved since the last conversation, what we committed to and whether it happened, what they asked that is still unanswered, and what is newly worth showing on screen. Use before any scheduled client call, working session, admin training, or go-live review, and whenever asked "what do I need to know before I talk to <client>". NOT a status report, NOT a findings dump — for live-state audits use ecat-postgres-audit, for a single inbound ticket use ecat-support-triage.
---

# eCat Session Prep

A brief a human reads in the ten minutes before a working session. Kylor's words:
**"what's been done, what to discuss, what to show."**

**Not a status report. Not a harness dump.** 187 findings is useless before a 30-minute
call. If a section has nothing in it, the section says "nothing" and takes one line.

**Read-only throughout.** No Postgres writes, no HelpScout writes, nothing sent anywhere.
v1 produces a document a human reads.

---

## The one idea

**A session-prep brief is a DIFF SINCE THE LAST CONVERSATION, not a snapshot.**

Everything after the last conversation is new: imports that ran, images that landed,
users who logged in, tickets that opened and closed, orders that went through. That delta
is the whole value. A brief that re-states what the client already knows gets read once
and never again.

So the first thing this skill does is **fix the anchor date**, and the anchor is the
hardest part — see § 2. Everything downstream is windowed on it.

---

## What this skill is allowed to do that no other eCat skill is

Every other tool in this programme is forbidden from interpreting. **This one must
interpret — that is its job.** But it separates the two, visibly, on every line:

| kind | how it appears |
|---|---|
| what was said | `> "..."` blockquote, **with a date and a named source** |
| what was recorded | a count or a timestamp, **with the table it came from** |
| what I conclude from either | prefixed **`Conclusion:`** — never a quote, never a count |

The programme's most expensive error was stating a consequence as if it were a
measurement, and it reached a client (`OPEN_ITEMS § F1`: Legrand was told inventory
could not be displayed; the NULLs were real, the consequence was invented). Three of the
six recorded errors are that same shape. The label is the whole defence.

**Also binding here:**

- **Cite the harness, never re-derive it.** If `onboarding-agents/1-ingestion/acceptance/` or an
  `ecat-config-check` run has a finding, name it and link it. Do not re-run the SQL and
  do not form a second opinion. If neither has run, say the section is unchecked — do not
  fill the gap with your own analysis.
- **A harness finding must be confirmed against live state before it reaches a client**
  (`OPEN_ITEMS § G2`). A brief is read *to* a client. Anything from the harness that has
  not been confirmed in state is marked `unconfirmed` or left out.
- **A lookup that returns nothing is not an answer.** Three instances in this codebase,
  each initially read as a real negative. See § 6.

---

## 1. Inputs, and which are required

| source | required? | reaches | gives |
|---|---|---|---|
| **Calendar** — the operator's calendar, or the meeting stated in the prompt | **REQUIRED to know a session exists** | this Mac / Google Calendar, once wired | source 0: a session is scheduled or happened, with attendees and time |
| **BigQuery** — `onboarding_assessment.fathom_recent_meetings`, `Fathom.call-transcripts`, `onboarding_assessment.helpscout_tickets` | **REQUIRED for the conversation record** | anywhere (service-account key) | §§ 1–3 when the mail and recording exist |
| **Postgres** — `supercat-postgres-vpn` MCP | **OPTIONAL** | VPN only | what actually moved in the org: the numbers in § 1 and most of § 4 |
| harness / `ecat-config-check` output | optional | wherever it was run | findings to cite, never to re-derive |

**Calendar is not optional for "was there a call."** Fathom is a transcript source, not a
meeting source. HelpScout is the eCat support mailbox, not Kylor's inbox. Client Teams
meetings routinely exclude the Fathom bot, and some working correspondence never hits
HelpScout. Empty Fathom or a thin HelpScout thread is **not** evidence that no session
happened.

Until Google Calendar is wired, the meeting line in the prompt **is** the calendar:
date, time, attendees, and "Fathom cannot join / mail may be off HelpScout" when true.
Do not wait for a recording to build the brief. Header must say what was missing.

Do **not** ingest the operator's whole Gmail. If mail off HelpScout is needed later,
scope it to a label or to `org_domains` senders — never the inbox.

**Postgres is optional and degrades loudly.** This skill is the first built to deploy on
eve, and eve cannot reach Postgres — `mcp-postgres-tools.tools.supercatsolutions.com` is
split-horizon DNS, NXDOMAIN on public resolvers. No credential fixes it. Making Postgres
a hard dependency is exactly what would block deployment.

**Both halves verified off-VPN 2026-09-09**, tunnel actually down, not simulated:

- **The BigQuery service-account key authenticates with no VPN.** It is self-contained —
  `type: service_account`, `token_uri: https://oauth2.googleapis.com/token`, private key
  inline — so auth is a local JWT signature plus a POST to a public Google endpoint.
  Traced: both the token exchange and the API call left over the physical interface, never
  the tunnel. Assumed portable since 2026-08-18; now measured.
- **Postgres fails fast and uninformatively.** The MCP returns exactly
  `mcp-remote: fetch failed` — no hostname, no reason, no hint that a VPN is involved.
  **Recognise that string.** It does not mean a transient network blip and it must not be
  retried; it means this run is Postgres-less. It does not hang, so there is no wedged
  session to clear.

Without Postgres the brief still builds from the conversation record, and it opens with:

```
> **Postgres unavailable.** <host> does not resolve on a public resolver and the host is
> unreachable; the MCP returns `mcp-remote: fetch failed`. This brief is built from the
> conversation record only. Not included: import activity, catalogue and customer counts,
> image coverage, logins, orders, inventory freshness. § 1 is almost entirely lost and
> § 4 cannot be confirmed current. § 3 is unaffected.
```

**Say § 3 only.** An earlier version of this block claimed "sections 2 and 3 are
unaffected" and that is wrong twice over: § 2 is exactly where `not verified` lands, and
§ 4 degrades badly and went unmentioned. Measured section by section, off-VPN:

| § | keeps | loses |
|---|---|---|
| 1 Since we last spoke | "no message in N days", plus `lineitem` activity | every count, every import, every login |
| 2 We said we would | **what they owe us, nearly intact** | most of what we owe them |
| 3 They said / asked | **everything — byte-identical** | nothing |
| 4 Worth showing | the list of candidates | any confirmation they carry data |

**The rule that follows from this:** the degraded brief keeps its value in proportion to
how much of the client's state lives in the conversation rather than the database. A
client waiting on files and answers degrades gracefully. A client in active technical
validation — beta testing, imports landing, adoption being measured — degrades badly, and
the brief should say so in the header rather than pretend otherwise.

Never silently drop a section. Never let a missing source read as a zero.

---

## 2. Fix the anchor — and do not trust Fathom alone

**Fathom's coverage is incomplete, and this is the failure mode most likely to ruin the
brief.** Verified 2026-09-04 on both test clients:

| client | last Fathom call | a session that actually happened after it | evidence |
|---|---|---|---|
| `leg` | 2026-08-07 | **2026-08-28** | Trey, 08-27: *"Looking forward to seeing your magic tomorrow"*; Tracy, 08-28: *"I can't make the call"* |
| `mer` | 2026-08-13 | **2026-08-27** | Kylor's recap, 08-31: *"Good session Thursday"*; the invite was confirmed in-thread on 08-24 |

Neither call is in Fathom at all — not under another title, not with empty domains
(checked the whole fleet window). Anchoring on Fathom would have produced a brief
re-stating three or four weeks of work the client had already been walked through, which
is precisely the "read once and never again" failure.

**So the anchor is `max(` of FOUR sources, not three:**

0. **Calendar (or the meeting stated in the prompt).** This is source 0. A Teams/Zoom
   event with the client's attendee domains is a session whether or not Fathom or
   HelpScout saw it. Match attendees against `org_domains` (and the prompt). Never
   conclude "no session" from empty Fathom.
1. **Last deduped Fathom call.**
2. **Last session-shaped email** — a thread from `@supercatsolutions.com` whose body opens
   with a recap frame: `good session`, `thanks for the time today`, `recap`, `here's where
   we landed`, `what we locked in`, `good progress today`, `good to meet you all today`.
   These are Kylor's own post-call notes and the highest-signal artifact in the corpus
   (see § 4). Match on the first ~400 characters; recap language appears at the top or not
   at all. HelpScout only. Mail that stayed in the operator's inbox is invisible here
   until a recap is forwarded to the eCat mailbox or a scoped Gmail label exists.
3. **Last forward-looking session reference** — anyone, either side, pointing at a session
   about to happen: `prior to tomorrow's call`, `looking forward to seeing you tomorrow`,
   `ahead of our meeting`, `our meeting on <day>`, `we will walk through it together
   tomorrow`, `I can't make the call`, `just sent an updated meeting invite`.

**Source 3 is not optional, and `leg` is why.** Neither of `leg`'s last two sessions
produced a recap — the 09-03 "Final review" is a sign-off, not a recap — so sources 1 and
2 both stop at **2026-08-07**. A brief anchored there re-states a month of work the client
has already been walked through, which is the exact failure this skill exists to avoid.
Adding source 3 recovers all three real sessions across both test clients (`leg` 08-28,
`leg` 09-04, `mer` 08-27) with **zero false positives** in the window. Verified twice: on
2026-09-04 with Postgres and again 2026-09-09 with the VPN down.

**A scheduled session is not a held session.** Source 3 proves a session was *arranged*,
never that it happened. With Postgres, corroborate from login or import activity clustered
on the day. Without it you cannot, so **label the anchor `inferred, not confirmed`** in
the header and say what it rests on:

```
Last conversation: 2026-09-04 — settings walkthrough (inferred, not confirmed)
```

If Fathom missed a session, say so in the header — it tells the reader the transcript
quotes in § 2 are from an *older* call than the one they actually last had. Client
Teams tenants that refuse the Fathom bot are the common case, not an exception:

```
> **Fathom has no recording of the 2026-08-28 session.** Anchor taken from Kylor's
> recap email of 2026-08-31. Commitments below are read from that email, not a transcript.
```

---

## 3. Resolve the client — domains, not titles

**Domain matching is primary, title regex secondary.** Title search found fewer calls for
every client tested and zero for `pebl`, whose only call is titled "Discovery Call".

With Postgres, resolve domains at runtime rather than from a hardcoded map:

```sql
-- org identity + every domain that touches it
SELECT o.id, o.shortname, o.name, o.created_at,
       o.properties->>'status'  AS status,
       o.order_email_recipient, o.company_email
FROM organizations o WHERE o.shortname = '<sn>';

SELECT lower(split_part(u.email,'@',2)) AS domain,
       count(*) AS users, count(*) FILTER (WHERE ou.is_admin) AS admins
FROM org_users ou JOIN users u ON u.id = ou.user_id
WHERE ou.organization_id = (SELECT id FROM organizations WHERE shortname = '<sn>')
GROUP BY 1 ORDER BY users DESC;
```

**Union the order-email domain with the user domains — they differ.** `leg`'s
`order_email_recipient` is `legrand.cs@legrand.us` while all six client users are on
`legrand.com`, and Fathom only ever carries `legrand.com`. Taking either alone loses
calls or loses tickets.

**Exclude staff by the derived rule, and by nothing else** (`OPEN_ITEMS § A27`, resolved
2026-09-05):

```sql
staff = users.billable IS FALSE  OR  email ILIKE '%@supercatsolutions.com'
```

Both halves earn their place. `billable` catches the **24** staff on personal or
contractor domains a filter misses — including `kylor22johnson@gmail.com`, `is_admin`,
member of 110 orgs. The domain half catches the **39** staff seats marked billable: test
and demo accounts provisioned inside client orgs (`chuck+911@`, `kyla+rep@`, `brent+demo2@`).
Fleet-wide that is **96 staff against 70,008 client-side**. *Residual, named:* a staff
member on a personal domain holding a billable seat is invisible to both signals.

**Do not drop free-mail or personal domains.** They are load-bearing client identities
(`§ A28`). eCat's client side includes multi-line rep agencies and multi-brand dealers who
legitimately hold accounts at many manufacturers — `lightingvision@comcast.net` has
accounts at **16 orgs** and is a real user; `christieslightinggallery@gmail.com` 10+.
**2,982 client accounts sit in 5+ orgs and none are staff.** An earlier version of this
line dropped free-mail as "staff and personal logins" and would have lost every one of them.

For the same reason, **org count is not a staff signal** and **a sender's email domain does
not identify a client org** — a message from `riccisales.com` could concern any of eleven
manufacturers. Scope the corpus by the org named in the thread, not by the sender's domain
alone.

Without Postgres none of this is available: `billable` is a Postgres column. Use the
registry below, and treat any personal-domain address appearing in the client's own threads
as a client identity unless it is `@supercatsolutions.com`.

**This is the deployment blocker, not the degradation.** Runtime domain resolution is a
Postgres read, so off-VPN the skill falls back to the static registry below — which covers
six clients. **RESOLVED 2026-09-09 — `onboarding_assessment.org_domains` now exists in BigQuery (6 rows) and `resolve_client` reads it, so a seventh client is one INSERT and no code change. The static registry below is retained as the offline fallback only.** Before this ships to
eve, push an org → domain map to BigQuery (one small table: shortname, org name, domains,
mention token). Everything else about the degraded path is a graceful loss of detail; this
one is a hard stop.

Without Postgres, fall back to this registry (verified 2026-08-18 / 2026-09-04, re-checked
off-VPN 2026-09-09):

| sn | name | domains | mention token |
|---|---|---|---|
| `leg` | Legrand US | `legrand.com`, `legrand.us` | `legrand\|adorne` — **not** `radiant`, a common word that drags in unrelated lighting threads |
| `mer` | 111Mercer | `tempaper.com`, `111mercer.com` | `tempaper\|111 ?mercer` — brand ≠ org name |
| `drf` | Dorell Fabrics | `dorellfabrics.com`, `loomcraft.com` | `dorell\|loomcraft` |
| `mali` | Magic Lite / NSL | `magiclite.com`, `nslusa.com` (+ partner `endeavoursolutions.com`) | `magic ?lite\|nslusa\|nsl\b` |
| `pebl` | Skyard Furniture (Pebl) | `peblfurniture.com`, `skyard-outdoor.com` | `pebl\|skyard` |
| `tcd` | Terracotta Designs | `terracottalighting.com` | `terracotta` |

Two orgs are named "legrand": live is `leg` id 273; `lna` id 93 is an inactive 2015 org.

---

## 4. The conversation record

### 4a. Calls — dedupe or read the same call four times

The same call is recorded by several Fathom users under different `recording_id`s.
**Dedupe on `(meeting_title, meeting_start)`.** Raw → unique: `mer` 14→5, `drf` 17→11,
`mali` 30→18, `leg` 7→5. One `mer` call was captured by five recorders.

**Summaries and transcripts join on `Recording Share URL`, NEVER `ID`.** The ID columns
match on 0 of 933 rows — a join on ID yields zero transcripts and looks like missing data.

```sql
WITH flat AS (
  SELECT meeting_title, meeting_start, duration_minutes, recording_url,
         invitee_names, invitee_emails_raw, summary
  FROM `supercat-data-pipeline.onboarding_assessment.fathom_recent_meetings`
  WHERE EXISTS (SELECT 1 FROM UNNEST(external_domains) d WHERE TRIM(d) IN UNNEST(<domains>))
     OR REGEXP_CONTAINS(LOWER(meeting_title), r'<token>')
), dedup AS (
  SELECT meeting_title, meeting_start,
    MAX(duration_minutes) AS duration_minutes,
    ARRAY_AGG(recording_url IGNORE NULLS ORDER BY recording_url)[SAFE_OFFSET(0)] AS url,
    ARRAY_AGG(invitee_names  IGNORE NULLS ORDER BY LENGTH(invitee_names)  DESC)[SAFE_OFFSET(0)] AS names,
    ARRAY_AGG(summary        IGNORE NULLS ORDER BY LENGTH(summary)        DESC)[SAFE_OFFSET(0)] AS summary,
    COUNT(*) AS recorders
  FROM flat GROUP BY 1,2
)
SELECT d.*, c.`Transcript Plaintext` AS transcript
FROM dedup d
LEFT JOIN `supercat-data-pipeline.Fathom.call-transcripts` c
       ON c.`Recording Share URL` = d.url          -- NOT ID
ORDER BY d.meeting_start DESC;
```

A call with no transcript falls back to its Fathom AI summary. **Say so.** A summary is an
interpretation; weight it below a transcript and never quote it as if someone said it.

### 4b. HelpScout — two levels of duplication, not one

**Level 1, documented: tickets duplicate.** 21 of 31 `tcd` tickets were captures of 9
conversations. Collapse on subject minus `Re:` / `Fwd:` / `FW:`.

**Level 2, found 2026-09-04 and not previously recorded: threads duplicate inside the
collapsed group.** `leg`'s "Settings tour" collapses to 2 conversations / 10 threads but
holds **5 unique messages** — each captured twice, sometimes with timestamps **one second
apart** (13:37:17 and 13:37:18). Truncating to the second does not catch it. Dedupe on
`(thread_author_email, LEFT(normalised_body, 200))` and keep the earliest.

Without level 2, § 3 lists the same open question twice and the brief looks careless.

```sql
WITH raw AS (
  SELECT ticket_number, conversation_id, ticket_subject, ticket_status, thread_type,
         thread_created_at, thread_author_email, thread_body,
         TRIM(REGEXP_REPLACE(LOWER(IFNULL(ticket_subject,'(none)')),
                             r'^(re|fwd|fw)\s*:\s*','')) AS subj_key,
         LEFT(REGEXP_REPLACE(thread_body, r'\s+',' '), 200) AS body_key
  FROM `supercat-data-pipeline.onboarding_assessment.helpscout_tickets`
  WHERE (primary_customer_domain IN UNNEST(<domains>)
      OR REGEXP_CONTAINS(LOWER(CONCAT(IFNULL(ticket_subject,''),' ',
                                      IFNULL(thread_body,''))), r'<token>'))
    AND thread_body IS NOT NULL AND TRIM(thread_body) <> ''
    AND thread_type <> 'note'                      -- internal, never client-visible
), uniq AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY subj_key, thread_author_email, body_key
                               ORDER BY thread_created_at) AS rn
  FROM raw
)
SELECT * FROM uniq WHERE rn = 1 ORDER BY thread_created_at;
```

**`thread_created_by_type` is not who spoke.** Fleet-wide, **802 of 16,390 threads typed
`customer` were authored by `@supercatsolutions.com`** — 4.9% misattributed, and it hits
both test clients (Kylor's own `mer` recap of 2026-08-31 is typed `customer`). Decide who
spoke from **`thread_author_email`'s domain**, always.

`thread_type = 'note'` is an internal HelpScout note. It never reached the client. Exclude
it from §§ 2–3; if you cite one at all, label it internal.

**`thread_type = 'lineitem'` is not a message at all** — it is a status change (assigned,
closed, reopened, moved). Measured 2026-09-09: **7,947 rows, 100% of them with an empty
body**, the only type where that is true. The `thread_body <> ''` filter already drops
them, but by accident rather than by design, so exclude the type explicitly and know what
you are excluding.

**Off-VPN, `lineitem` is worth reading back in as the only activity signal BigQuery has.**
When Postgres is gone there is no import log and no login table, so "somebody touched this
conversation on 09-04 at 21:25" is genuinely the best available evidence that anything
happened at all. Report it as what it is — *a status change, no content* — never as
correspondence. On this run it was the sole recorded activity for `leg` in a five-day
window, and it is what let § 1 say something truthful rather than nothing.

**`ticket_status` will not tell you what is open.** Every `leg` conversation reads
`closed`, including questions answered thirty minutes ago and questions never answered —
Kylor closes as he goes. Openness is a property of the *last unique thread*: if the last
message in a collapsed conversation is from a client domain and reads as a question or a
request, it is open. Judge it; do not filter on status.

---

## 5. The Postgres delta — and the columns that will lie to you

Only **append-only** tables give a true delta. eCat imports **hard-delete and reload**, so
on reloaded tables a `created_at` is the timestamp of the last import, not of creation.

| want to say | source | verdict |
|---|---|---|
| an import ran | `import_events.created_at` | ✅ append-only, true delta |
| an iPad login happened | `login_events.created_at` | ✅ append-only. **iPad only** — carries `ipad_release`, `ios_version` |
| an eOL login happened | `org_users.last_ecat_online_login_at` | ⚠ last-value, not an event. The **sibling** of `last_ipad_login_at`; measuring one misreports any org with eOL |
| an order was submitted | `orders.submit_date` | ✅ the business event. Its sibling `orders.created_at` is the row — they differ by up to **4,751 days** |
| a user was invited / accepted | `organization_invitations.created_at` / `.redeemed_at` | ✅ |
| an image landed | `product_images.created_at` | ✅ spread over a year on `leg`, so not reloaded. Sibling: `product_images.updated_at` ≠ `product_image_updated_at` |
| **products were added** | — | ❌ **`products` has no `created_at`.** `last_modified_at` = last content change, `timestamp` = last touched by any pass. On `leg`, all 1,020 rows carry `timestamp` = 2026-09-03. Neither is a creation date |
| **customers were added** | — | ❌ **`customers.created_at` is the last reload.** All 1,133 `leg` customers were created inside an **11-second window** on 2026-08-28. "1,133 new customers since we last spoke" would be flatly false |

So the honest catalogue line is **"a Products import ran clean on <date>; the catalogue
now holds N active products"** — two facts, one append-only and one current-state — never
"N products were added." `import_events` carries no row counts; do not invent them.

**Four sibling pairs in this schema look like one answer and are not:**
`qty_available` / `qty_on_hand` · `last_ipad_login_at` / `last_ecat_online_login_at` ·
`submit_date` / `created_at` · `images` / `images_json`. Before using any column as *the*
answer, look for its sibling.

### The delta statements

Run read-only through the `supercat-postgres-vpn` MCP. Substitute `<sn>` and the anchor.

```sql
-- D1  what imported, and did it run clean
WITH org AS (SELECT id FROM organizations WHERE shortname = '<sn>'),
blocks AS (
  SELECT e.created_at,
         (regexp_match(chunk, '^([A-Za-z][A-Za-z ]*)'))[1] AS block_type,
         CASE WHEN chunk ILIKE '%:fatal%'   THEN 'fatal'
              WHEN chunk ILIKE '%:error%'   THEN 'error'
              WHEN chunk ILIKE '%:warning%' THEN 'warning'
              ELSE 'clean' END AS tier
  FROM import_events e, org,
       regexp_split_to_table(e.data, E'\n- - ') AS chunk
  WHERE e.organization_id = org.id
    AND e.created_at >= TIMESTAMP '<anchor>'
    AND chunk NOT LIKE '---%')
SELECT block_type, tier, count(*) AS runs, min(created_at) AS first, max(created_at) AS last
FROM blocks WHERE block_type IS NOT NULL GROUP BY 1,2 ORDER BY last DESC;
```

Do **not** filter out `Images` / `Option Images` here. `rawstate.py` excludes them because
they are 47% of all events and drown the rest — but an Images import is a *Worth Showing*
item, and its **absence** is the finding on `mer`.

```sql
-- D2  everything else, driven from organizations so a zero renders as a zero
WITH a AS (SELECT id, shortname, TIMESTAMP '<anchor>' AS since
           FROM organizations WHERE shortname = '<sn>')
SELECT a.shortname, a.since,
 (SELECT count(*) FROM products p WHERE p.organization_id=a.id AND NOT p.deleted)                        AS active_products,
 (SELECT count(*) FROM products p WHERE p.organization_id=a.id AND NOT p.deleted AND p.image_exists)     AS products_with_images,
 (SELECT count(*) FROM product_images i WHERE i.organization_id=a.id)                                    AS image_rows,
 (SELECT count(*) FROM product_images i WHERE i.organization_id=a.id AND i.created_at>=a.since)          AS image_rows_new,
 (SELECT count(*) FROM customers c WHERE c.organization_id=a.id)                                         AS customers,
 (SELECT count(*) FROM org_users ou WHERE ou.organization_id=a.id)                                       AS org_users,
 (SELECT count(*) FROM org_users ou WHERE ou.organization_id=a.id AND ou.created_at>=a.since)            AS org_users_new,
 (SELECT count(*) FROM organization_invitations v WHERE v.organization_id=a.id AND v.created_at>=a.since)  AS invites_sent,
 (SELECT count(*) FROM organization_invitations v WHERE v.organization_id=a.id AND v.redeemed_at>=a.since) AS invites_redeemed,
 (SELECT count(*) FROM login_events l WHERE l.organization_id=a.id AND l.created_at>=a.since)            AS ipad_logins,
 (SELECT count(DISTINCT l.user_id) FROM login_events l WHERE l.organization_id=a.id AND l.created_at>=a.since) AS ipad_users,
 (SELECT count(*) FROM org_users ou WHERE ou.organization_id=a.id AND ou.last_ecat_online_login_at>=a.since)   AS eol_logins_latest,
 (SELECT count(*) FROM orders r WHERE r.organization_id=a.id AND r.submit_date>=a.since)                 AS orders_submitted,
 (SELECT count(*) FROM inventories i WHERE i.organization_id=a.id)                                       AS inventory_rows,
 (SELECT max(i.updated_at) FROM inventories i WHERE i.organization_id=a.id)                              AS inventory_last
FROM a;
```

`a` is driven from `organizations`, so an org with no images returns an explicit `0` and
not a missing row. Written the other way round — `FROM product_images … GROUP BY org` —
`mer` **vanishes from the result set entirely** and reads as "not checked". That is § 6,
reproduced live while building this skill.

```sql
-- D3  orders are usually tests during onboarding; show who they are for
SELECT r.order_number, r.submit_date, r.total, r.bill_to_company_name,
       EXISTS (SELECT 1 FROM customers c
               WHERE c.organization_id = r.organization_id
                 AND lower(btrim(c.name)) = lower(btrim(r.bill_to_company_name))) AS matches_real_customer
FROM orders r
WHERE r.organization_id = (SELECT id FROM organizations WHERE shortname = '<sn>')
  AND COALESCE(r.is_submitted,false)
ORDER BY r.submit_date DESC;
```

`is_submitted` is **nullable**; a bare `WHERE is_submitted` silently drops rows. And the
only submitted order at each test client is named `Test Kylor` / `Test` — **"your first
order came through" would be false.** Show `bill_to_company_name`, and where
`matches_real_customer` is false call it a test order.

`customers.company_name` does not exist. The column is `customers.name`.

### Staff accounts sit inside the client's user and login counts

`org_users` and `login_events` carry SuperCat people alongside the client's. Counting
"users who logged in" without removing them overstates adoption, and **a domain filter on
`supercatsolutions.com` alone does not catch them** — Kylor's admin account on both test
orgs is `kylor22johnson@gmail.com`. **Use the § 3 staff rule** (`billable IS FALSE OR
@supercatsolutions.com`), not a domain guess, and never a free-mail filter — that would
drop real reps along with him. Proportional damage from getting this wrong is worst on
small onboarding orgs: `leg` −29% of provisioned users, `mer` −25% (`§ A27`).

Verified 2026-09-04: `mer` shows 2 distinct iPad users since the anchor, but one is Jon
Vanderberg. The client figure is **1**. `leg` shows 8; the client figure is **7**.

`login_events` carries `username`, `first_name`, `last_name` and `user_group_name`, so
name the people rather than printing a count. A brief with four names in it is more useful
than one that says "8 users" and it makes the staff row obvious on sight.

### The two login sources disagree, and one is broader than the other

`org_users.last_ipad_login_at` and `max(login_events.created_at)` agree to within
milliseconds on 7 of `leg`'s 11 logged-in users — and differ by up to **20 hours** on the
other four, always with `org_users` **later**. **Conclusion:** `login_events` records a
subset of what touches `last_ipad_login_at`; the column is "last time the device talked to
us", the table is "a login was recorded".

So: quote a **specific login time** from `login_events` only, and answer **"has this person
ever opened the app"** by requiring `last_ipad_login_at` *and* `last_ecat_online_login_at`
*and* `login_events` all to be empty. That three-way test is what found `mer`'s Jen and
Jeffrey and `leg`'s Bryan — three people who had been told their logins were live and had
never used them, which is a § 2 row in every case.

### An empty delta is a finding, and must be rendered

D1 returns **no rows** when nothing imported. That is not "not checked" — it is the answer,
and on `mer` it is the most important line in the brief. Render it as
**"No import of any kind has run since <anchor>."** Never let the section disappear.

---

## 6. A lookup that returns nothing is not an answer

Three instances in this codebase, each initially read as a real negative:

- `rawstate.py` carried `libco: 279`. libco is **288**. Every libco statement returned
  zero rows and read as "libco has no products", not as a lookup failure.
- `territory_codes`' empty value is the literal string `'[]'`, not `''` or NULL. A query
  reported "every customer has a territory" when none did.
- Building this skill: an image query grouped from `product_images` dropped `mer` from
  the result set entirely rather than returning `0`.

**Before printing any zero or any "nothing found", prove the lookup resolved.** Resolve
the org by shortname and check the identity row came back; drive counts from
`organizations`; and when a section is genuinely empty write **"no X since <date>"** with
the date, never a bare `0` and never silence.

The same rule on the BigQuery side: if the domain set resolves to nothing, or the Fathom
query returns zero calls for a client that demonstrably has calls, the brief says the
lookup failed. It does not say the client has been quiet.

---

## 7. The output

Four sections, in this order, in one markdown document. Header first.

````markdown
# Session prep — <Client> (`<sn>`)
**For:** <session, date/time if known>  ·  **Prepared:** <ts>
**Last conversation:** <date> — <call title | recap email subject>
**Window:** <anchor> → now (<N> days)
**Sources:** BigQuery ✅ · Postgres <✅ | ❌ + reason> · harness <run <date> | not run>

<warnings: Fathom gap, missing Postgres, failed lookups — one blockquote each, or omit>

## 1. Since we last spoke
## 2. We said we would
## 3. They said / asked
## 4. Worth showing
````

### § 1 — Since we last spoke

The delta. Dates, counts, what moved — one line each, newest first. A count with no date
is not a delta. Anything that did **not** move but was expected to belongs in § 2, not
here. Cap at ~8 lines; below that threshold nothing is worth a line.

```
- **2026-09-03** — Inventory feed loaded; quantities now showing on iPad (`import_events`, clean)
- **2026-08-28** — Customers import ran clean; org now holds 1,133 customers
- **08-07 → 09-04** — 8 distinct users logged in from an iPad, 92 sessions (`login_events`)
- No images have landed since 2026-08-06 (`product_images`)
```

### § 2 — We said we would

**The highest-value section and the one nothing else produces.** Commitments made on the
last call, with whether they happened.

**Source order: the recap email first, the transcript second.** After every session Kylor
sends a structured recap — `WHAT WE LOCKED IN` / `WHAT I STILL NEED` / `WHAT I'M DOING` /
`HOW WE GET TO GO-LIVE`. It is an explicit commitment list written by the person who made
the commitments, it survives when Fathom missed the call, and it beats transcript parsing
on both precision and cost. Use the transcript for commitments the recap omitted, and for
anything the *client* committed to in their own words.

### The bound — state it in the brief, every time

**§ 2 only knows commitments that were written down.** A commitment made out loud and
never recapped is invisible to this section, and no amount of database access recovers it.
Both test clients have unrecorded, unrecapped sessions (§ 2 of this skill), so this is the
normal case, not the edge case.

The section therefore carries a one-line bound, always, immediately under the heading:

```
Scope: commitments written down in the <date> recap and the thread since. A commitment
made verbally on the <date> call and never recapped does not appear here.
```

Without that line the section reads as complete when it is not, which is worse than a
short section. It is also the honest answer to "is that everything?" — no, it is
everything that was written down.

### Two owners. Theirs goes first.

**"What am I waiting on from you" is half of what a reader needs in the first thirty
seconds** — often the more actionable half, because it is what the call has to unblock.
Give it its own heading and put it **above** what we owe, regardless of which list is
longer.

It also degrades better: an unsent file and an unanswered question leave no email, so
"they owe us" is answerable from the conversation record alone and survives the loss of
Postgres almost intact. "Did we deliver" mostly does not.

```markdown
### What they owe us
| # | Commitment | Bucket | Evidence |
|---|---|---|---|
| 1 | Send product images | **not done** | 0 rows in `product_images`; no Images import since anchor |
| 2 | Send the customer list | **not done** | `customers` = 0 — and see § 3, they asked a blocking question first |

### What we owe them
| # | Commitment | Bucket | Evidence |
|---|---|---|---|
| 3 | Reload the corrected product file | **done** | Products import clean 08-27; 102 active |
| 4 | Load the five logos | **NOT VERIFIABLE** | no database fact exists — confirm on screen |
```

### Three buckets, and the third is where the risk sits

Every row lands in exactly one:

| bucket | means | rule |
|---|---|---|
| **verified done** | a measurement shows it happened | name the measurement |
| **verified not done** | a measurement shows it did not | name the measurement |
| **NOT VERIFIABLE** | **no source can answer this, in any mode** | name *why* no source can |

`partly` is a legitimate refinement of the first two — give the fraction. It is not a
fourth bucket.

**NOT VERIFIABLE is not a failure state and must never be hidden.** It is the commitments
with no database fact behind them: *"I'll send the pricing template"*, an FTP upload, a
logo slot, a Library link's contents, a decision someone promised to make, anything that
happened in email or on a screen rather than in a table. Left out, they vanish and the
brief silently under-reports what is outstanding. Given an unearned `done` or `not done`,
the brief states a consequence as a measurement — `§ F1`, the error that reached a client.

So they get their own visible bucket and, when there are more than one or two, their own
short block:

```
NOT VERIFIABLE — no source confirms these either way. Check on screen before claiming them:
  • five logos loaded, incl. the email banner
  • Design Studio links corrected for Enlightening Sales and Fletcher
```

**One more status, and it is not a bucket:** `not verified` means *Postgres was
unavailable* — the fact is verifiable in principle, just not from here. It is a property
of this run, not of the commitment. **Never collapse it into `done`, `not done`, or
`NOT VERIFIABLE`** — the first two are false, and the third is a permanent claim about a
temporary condition.

Then, separately and labelled:

```
Conclusion: images are the only thing between here and a demo-able catalogue.
```

That sentence is a judgement. It gets the prefix. The rows above it do not.

### § 3 — They said / asked

Open questions **from them**, from calls and HelpScout, still unanswered — quoted, dated,
attributed. Not paraphrased: the point is the reader recognises their own client's words.

A question is open when the last unique thread in the collapsed conversation is from a
client domain and reads as a question or a request. Ignore `ticket_status` (§ 4b). Check
whether a later thread from us answers it; if one does, drop it.

```markdown
> **Trey Wilson**, 2026-09-04 — *"Jason @ Dunn Brands does not see Legrand in his list
> of brands. Brad & Sam do though. What do you recommend?"*
> Answered 16:38 the same day — Legrand added to `sales@dunnbrands.com`. **Closed.**
```

Include a question the client asked on the *call* and that nothing since has answered —
that is the one most likely to be forgotten, and only the transcript holds it.

If none: **"Nothing open from them since <date>."** One line.

### § 4 — Worth showing

What is **newly demonstrable** — images now live, a filter chip that now works, products
imported, an order that went through end to end, a rep who synced for the first time.
Newly: it was not showable at the last conversation and is now.

Each item names the screen and the reason it is new.

```
- **The iPad catalogue with inventory** — quantities render for the first time; the feed
  loaded 09-03 after the column mismatch was fixed. Trey pushed on this directly.
- **Order submission end to end** — one order submitted 09-03 (`Test Kylor`, $281.13).
  Internal test, not a client order.
```

**Do not promise a screen you have not confirmed carries data.** "Images now live" needs
`products_with_images > 0`, not an Images import that ran. This is `F1` in the shape it
would take here: the import event is the measurement, what the rep sees is the
consequence, and they are separate claims.

If a harness or config-check finding is relevant, name it and link it — `A7`, `G1`,
`SCORECARD § 12 R1`. The brief is not a second opinion.

---

## 8. Before you hand it over

- [ ] Every quote carries a **date** and a **named source**
- [ ] Every count names the **table** it came from
- [ ] Every judgement is prefixed **`Conclusion:`**
- [ ] No consequence stated as a measurement (`§ F1`)
- [ ] Any partition **sums to its total** (`§ F7` — leg's inventory breakdown did not, by 23)
- [ ] No harness finding present that live state has not confirmed (`§ G2`)
- [ ] Every zero traced to a lookup that demonstrably resolved (§ 6)
- [ ] Postgres unavailability, Fathom gaps and failed lookups **stated in the header**
- [ ] § 2 carries its **scope bound** — written-down commitments only
- [ ] § 2 leads with **what they owe us**
- [ ] Every § 2 row in exactly one bucket, and **NOT VERIFIABLE rows are visible**, not dropped
- [ ] No `not verified` row collapsed into `done`, `not done`, or `NOT VERIFIABLE`
- [ ] Staff excluded by `billable IS FALSE OR @supercatsolutions.com` — **no free-mail filter** (`§ A28`)
- [ ] Reads in under ten minutes. If it does not, § 1 is too long — cut it, not § 2

**The test is whether Kylor would open this instead of scrolling his own notes.** Iterate
on that answer, not on completeness.
