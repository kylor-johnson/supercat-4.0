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

## 2. Meetings, cut at T

- Fathom: `search_meetings` on the client name, `recorded_by = anyone`,
  `created_after = T - 14d`; keep only recordings whose date `<= T`. Summary only;
  transcript when a commitment goes into copy.
- Google Calendar: `list_events` for `[T - 7d, T]`; keep events with an attendee on
  the client's domains. An event with no matching Fathom recording is flagged
  `unrecorded-meeting`.

## 3. Client folder

`~/repos/ecat-onboarding-workspace/02_Implementation/<Client>/` as it is now. The
packet notes which files postdate `T` (by mtime); the agent treats those as
unavailable.

## 4. Live state (Postgres, read-only)

Whatever `ecat-support-triage` GROUND needs for the diagnosis, with `updated_at` on
every row read. Rows with `updated_at > T` are shown but marked `changed-after-T`;
the grader treats claims that depend on them as "method graded, value not graded".
For tickets older than ~60 days, skip value grading entirely.

## 5. Code and KB

Not cut: `supercat_server` on GitHub at the current SHA, and the KB. Product
behaviour rarely changes within the replay window; the SHA is cited so the grader
can check when it matters.

## Assembly

Packets assembled before commit 66607f1 (2026-09-28) trimmed every thread, this ticket's own included, at the first `From:` / `On … wrote:` line, which cut forwarded complaints. Rebuild any such packet before reusing it; grep an old packet for `[quoted history trimmed]` under the `← THIS TICKET` heading or a `FW:` subject.

The Meetings, Calendar and Live-state sections are supplied as files and are not checked by the script; the builder asserts their cut by hand (dates ≤ T) and must be a session that has not read the sent reply.

`packet_assemble.py <dir>` reads `threads.json`, `meetings.md`, `calendar.json`,
`state.md` from `<dir>` and writes `PACKET.md` with the sections above in order, the
cut time in the header, and a `LEAK CHECK` block listing anything found after `T`
and excluded. The agent is given `PACKET.md` and nothing else from HelpScout.

## Leak check, before grading

- No thread in the packet has `thread_created_at > T`.
- No note in the packet has `thread_created_at > T`.
- No Fathom recording in the packet is dated after `T`.
- The grader, not the agent, holds the sent reply.
