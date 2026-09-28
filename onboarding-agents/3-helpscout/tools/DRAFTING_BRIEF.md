# Replay drafting brief (blind)

You are drafting ONE blind replay of a SuperCat HelpScout ticket. A human reply was already sent and will be compared with yours later. You must never see it.

Inputs you are given: a ticket folder `runs/replay/<TICKET>/` and an output file name (DRAFT.md or DRAFT_v2.md). Read `PACKET.md` in that folder. It is everything that existed at the cut time T in its header. If it is long, read the ticket marked "← THIS TICKET" in full and skim the rest.

## Hard rules (breaking any invalidates the test)

- No BigQuery and no HelpScout data source (no `mcp__bigquery-admin` tools at all). Do not read any other folder under `runs/`, anything under `runs/2026-09-25/`, `runs/replay/_grader/`, or any file in your folder other than PACKET.md and the ones you write.
- Fathom and Google Calendar: only meetings/events dated on or before T. Jira: read-only; cite issues created on or before T; do not rely on status changes or comments after T.
- Nothing is sent or written anywhere except your output file. Postgres: read-only SELECTs via `mcp__supercat-postgres-vpn__execute_sql` (load with ToolSearch `select:mcp__supercat-postgres-vpn__execute_sql`). Postgres is live NOW, not at T: show `updated_at` on rows you rely on and mark values that could have changed after T.
- Code, cite commit + file:line; behaviour claims come from code or a KB article, never memory:
  - server: `/private/tmp/claude-501/-Users-kylorjohnson/c4cb84e8-ab42-401b-8bc9-f7d6a333f3c3/scratchpad/scs_repo` (supercat_server @183d8e1)
  - iPad, current: `.../scratchpad/ios_3.1` (sarreid_ios `release/2026.3.1` @f2e9877, build 20260909)
  - iPad, August builds: `.../scratchpad/ios_2.10` (sarreid_ios `release/2026.2.10` @4ca0696, plist 20260818; approximate for 20260822)
  Match the iPad branch to the rep's `orders.app_version` at T.
- KB: https://supercatsolutions.com/knowledgebase (WebFetch). If no article exists, say "none exists".

## Read first

`/Users/kylorjohnson/repos/supercat-4.0/CLAUDE.md`; then in `/Users/kylorjohnson/repos/supercat-4.0/onboarding-agents/3-helpscout/`: `ecat-correspondence/SKILL.md` (§ 4-0, § 6, § 7 with step 0, the VERIFY table and the two copy rules), `ecat-support-triage/SKILL.md`, `ecat-client-email/SKILL.md`. Route to domain skills under `~/.claude/skills/ecat-*` as triage directs. Client folders: `~/repos/ecat-onboarding-workspace/02_Implementation/` (files modified after T unavailable). Org registry: `organizations` (column `shortname`); some domains span several orgs, attribute from the thread.

## Task

Draft the reply to the last client message on the ticket at T. Consolidate per client, diagnose, ground in live state (values, not just events), verify behaviour in code, and draft in Kylor's voice.

## Output file sections, exactly

1. Header: ticket, client + org shortname/id (or unattributed), cut time, category (SEND-SAFE / DRAFT-AND-PING / ESCALATE) and the § 6 clause, scope line (inbox + assignee).
2. `## VERIFY` table: thread / live state / code (server) / code (iPad) / KB / meetings / Jira, each cited or NOT CHECKED. Then a `Conclusion:` line.
3. `## What the client said`: key quote, dated and attributed.
4. `## Draft`: the reply in a fenced code block.
5. `## Owner actions before this goes`: numbered exact steps.
6. `## Also found`.

Final message back: category, a two-sentence diagnosis, the three most important citations. Under 150 words.
