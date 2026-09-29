# Replay packet: how to build one, and what it must not contain

A packet is everything the agent may see for one ticket at one cut time `T`. It is
built from four sources with four cuts, and the agent drafts from the packet only.
The sent reply is never in it. Used for replay grading (HARDENING_PLAN.md) and for
live runs (where `T` is now).

## Inputs

`conversation_id`, `T` (UTC timestamp of the client message being answered),
`client_domains` (the client's domains, from `org_domains` or the thread).

## 1. Threads, cut at T (BigQuery)

Query through the `bigquery-admin` MCP tool only. Do not load a service-account key into a script or client library. If a result is too big to handle, page it (LIMIT/OFFSET, or one conversation at a time).

`replay_threads.sql` with `@conv`, `@t`, `@domains`. It returns, for the ticket and
for every other conversation whose client-side author is on the client's domains in
the 30 days before `T`:

- `customer` / `message` / `forwardchild` / `forwardparent` / `phone` threads with
  `thread_created_at <= T`;
- `note` threads only where `thread_created_at <= T` (notes after `T` usually
  contain the resolution; they are the leak);
- no `lineitem`;
- `thread_attachment_count`, `mailbox_id`, `assignee_id`;
- duplicate captures across inboxes collapsed on `(author, LEFT(body,200))`.

## 1b. Fleet at T (BigQuery + Postgres)

`replay_fleet_at_t.sql`: other clients' ticket subjects in T−2h → T, admin/app sessions in 15-minute buckets for T−3h → T, sessions / iPad sign-ins / eOL logins hourly for T−24h → T, and import fatals by org for T−24h → T. Every window ends at T. Save as `fleet.md` (no build date inside it; the assembler refuses any timestamp after T). The drafter has no BigQuery, so without this block a fleet incident can't be seen (measured: a draft blamed a browser during a fleet session collapse).

## 1c. Scope at T (BigQuery)

`replay_scope_at_t.sql` gives the assignee and inbox as they were at T; the view's `assignee_id` / `mailbox_id` are today's. Save the reading as `scope.json`: `{"mailbox_at_t", "assignee_at_t", "basis"}`, and put the build date in `basis`.

## 2. Meetings, cut at T

- Fathom: `search_meetings` on the client name, `recorded_by = anyone`,
  `created_after = T - 14d`; keep only recordings whose date `<= T`. Summary only;
  transcript when a commitment goes into copy.
- Google Calendar: `list_events` for `[T - 7d, T]`; keep events with an attendee on
  the client's domains. For each event, run Fathom `list_meetings` for that date and
  match on invitee emails or the client's domain, **not the title**. Only an event with
  no such match is flagged `unrecorded-meeting`; a matched recording goes into
  meetings.md. Measured: a title-only match flagged a recorded call as unrecorded, and
  the draft asked the owner for notes that were already on record.

Calendar must be pre-fetched as JSON (`{"window": [T-7d, T], "events": [...]}`); 35 of the first 50 packets said "not pre-fetched" and left the cut to the drafter. The assembler now prints a BUILD WARNING when it is not JSON.

## 3. Client folder

`~/repos/ecat-onboarding-workspace/02_Implementation/<Client>/` as it is now. List only
files whose mtime is at or before T; files that postdate T appear as a **count only**
("4 files modified after T, withheld"), never by name, since names carry later dates and
topics. Put the check date in `scope.json` `basis`, not in `folder.md`: the assembler
refuses any date after T in `folder.md`.

## 4. Live state (Postgres, read-only)

Whatever `ecat-support-triage` GROUND needs for the diagnosis, with `updated_at` on
every row read. **Snapshot:** the builder saves every row it read into `state.md` with the query, so a re-run reads the same state and not today's. Rows with `updated_at > T` are shown but marked `changed-after-T`;
the grader treats claims that depend on them as "method graded, value not graded".
For tickets older than ~60 days, skip value grading entirely.

## 5. Code and KB

Not cut: `supercat_server` on GitHub at the current SHA, and the KB. Product
behaviour rarely changes within the replay window; the SHA is cited so the grader
can check when it matters.

## Assembly

Packets assembled before commit 66607f1 (2026-09-28) trimmed every thread, this ticket's own included, at the first `From:` / `On … wrote:` line, which cut forwarded complaints. Rebuild any such packet before reusing it; grep an old packet for `[quoted history trimmed]` under the `← THIS TICKET` heading or a `FW:` subject.

The Meetings, Calendar and Live-state sections are supplied as files and are not checked by the script; the builder asserts their cut by hand (dates ≤ T) and must be a session that has not read the sent reply.

`packet_assemble.py <dir> [--out PACKET_rebuilt.md]` reads `threads.json`, `fleet.md`, `scope.json`, `meetings.md`, `calendar.json`,
`state.md` from `<dir>` and writes `PACKET.md` with the sections above in order, the
cut time in the header, and a `LEAK CHECK` block listing anything found after `T`
and excluded. The agent is given `PACKET.md` and nothing else from HelpScout.

## Leak check, before grading

- No thread in the packet has `thread_created_at > T`.
- No note in the packet has `thread_created_at > T`.
- No Fathom recording in the packet is dated after `T`.
- The grader, not the agent, holds the sent reply.
