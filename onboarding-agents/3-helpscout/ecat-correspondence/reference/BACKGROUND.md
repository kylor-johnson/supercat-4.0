# ecat-correspondence — background and measurements

Read on demand. `SKILL.md` holds the rules; this file holds the measurements that
justify them, so a later session can re-run and compare instead of re-deriving.
Client names and ticket numbers are removed (committed files describe the pattern,
never the case).

## The clock (measured 2026-09-05; re-measure before relying on it)

The HelpScout mirror in BigQuery was a once-daily batch, not a feed:

| | |
|---|---|
| `helpscout.conversation_threads` last written | 2026-09-04 22:37 UTC |
| threads dated 2026-09-05 at 18:54 UTC | 0, while every weekday in the prior three weeks carried 20–65 |
| average lag from a client message to the batch exposing it | 6.4 hours |
| worst case | ~24 hours |

How fast a human already answers (523 conversations since 2026-06-01): median first
staff reply 226 minutes; 237 of 411 answered within 4 h; 322 of 411 within 24 h.

Consequence: 57% of client messages (1,579 of 2,769 since 2026-03-01) already had a
human reply before the batch made them visible. On this data path the agent is a
drafting assistant working a backlog, not an autoresponder. Answering a live ticket
needs the HelpScout API as a read path.

## HelpScout write access: none, under any identity (checked 2026-09-05)

- `https://api.helpscout.net/v2/conversations` → HTTP 401. Reachable; no credential.
- No HelpScout credential on the machine: not in `~/.supercat/mcp-credentials.json`
  (Admin Console only), the keychain, the environment or the workspace.
- BigQuery gets HelpScout through a Hevo ETL holding its own read-only connection.
  It is not a write path.

If a write path is ever wanted, the grant decides the identity:

| grant | replies appear as | good for |
|---|---|---|
| OAuth2 client_credentials (an app) | the app, a bot identity | machine notes, tagging |
| OAuth2 authorization_code as the owner | the owner | a real draft in his mailbox |

Only the second produces a draft reply. It needs a registered HelpScout app and one
user authorisation. Ask for it explicitly.

`conversation_id` differs from `ticket_number`; the deep link uses `conversation_id`
(verified against an independent source, 2026-09-05).

## The candidate set is mostly thank-yous (2026-08-21 → 09-04)

```
27  structurally open (last client-domain message, no staff reply after)
16  acknowledgments, needing nothing          59%
 3  automated (daily inventory feed)
 1  spam, unflagged by HelpScout
 4  handled out-of-band, provable only from internal notes
 1  ambiguous (client answering our question, closed minutes later)
 5  genuinely needing a reply                 18.5%
```

Out-of-band notes, verbatim shapes: "Called. Advised to update the app." · "This issue
is resolved and [engineer] responded in another thread." · "Chatted with [contact]
this monday and she said we must not worry about [user]." Acknowledgments: "Thanks" ·
"Thank you for changing it for me!" · "ok so all reps updated thanks" · "Thank you for
the confirmation, this ticket can be resolved."

Automated senders over three months: `info@` 48 threads (a client's daily inventory
feed, on a client domain), `notify@ringcentral.com` 14 (voicemail), `support@` 2 (both
spam).

Coverage in that window: classified 27 of 27; attributed 21 confident, 5 ambiguous,
1 unattributed (free-mail).

## Attribution measurements (A28)

2,982 accounts sit in 5+ orgs and none are staff. Against 38 client domains in the
window: 21 map to exactly one org; 14 to 2–12 orgs (one rep-agency domain holds 12
orgs / 480 users); 3 free-mail domains to 103–165 orgs (`gmail.com`: 165 orgs, 15,203
users). One personal comcast address holds accounts at 16 orgs. Staff rule tested on
96 staff vs 70,008 client-side users; ~24 staff sit on personal or contractor
domains. `primary_customer_domain` read `supercatsolutions.com` on two tickets whose
clients were on client domains.

`thread_created_by_type` is not who spoke: fleet-wide 802 of 16,390 `customer`
threads were authored from `@supercatsolutions.com` (4.9%); last quarter 248 of 1,811
(13.7%).

## How much is send-safe (measured)

Of the 5 genuinely-open tickets in the window, none was send-safe; across the
10-candidate set, 1, arguably 2 (documented product behaviour).

Of 490 staff first-replies since 2026-05-01 (median 537 characters):

| marker in the reply actually sent | count | share |
|---|---|---|
| a forward commitment ("I'll…", "we'll…", "by Friday") | 261 | 53% |
| an apology | 60 | 12% |
| an escalation to engineering | 44 | 9% |
| money, invoice, billing or contract | 46 | 9% |
| any of the above | 291 | 59.4% |

So at most 40.6% of real replies are candidates; the hand-classified rate is 10–20%.

## The acceptance run's worked ESCALATE

A client had been told "we'll reach out to schedule a call… in the next week or two";
59 days later they wrote "I just wanted to follow up… Any movement on your end?"
`ticket_status` read `active`; the last staff reply was two months old. ESCALATE,
because the honest answer is "we said two weeks and it has been two months" and the
agent cannot know the engineering status (the note handed scoping to an engineer and
nothing since says what happened). The draft owns the miss, states only what is
provable, and leaves the status sentence for the owner.

Known false-negative risks: the acknowledgment pass is a judgement ("Thank you. We're
looking into this." is an acknowledgment; "Thanks, will that work for the October
file?" is not), and a ticket handled by phone with no note looks dropped. That is the
right direction to fail in.
