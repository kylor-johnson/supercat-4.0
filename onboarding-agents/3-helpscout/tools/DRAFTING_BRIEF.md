# Replay drafting brief (blind)

You are drafting ONE blind replay of a SuperCat HelpScout ticket. A human reply was already sent and will be compared with yours later. You must never see it.

Inputs you are given: a ticket folder `runs/replay/<TICKET>/` and an output file name (DRAFT.md or DRAFT_v2.md). Read `PACKET.md` in that folder. It is everything that existed at the cut time T in its header. Its section 1b (fleet at T) is the only view you get of other clients; if it says NOT BUILT, say so before blaming one client's browser, device or file. If it is long, read the ticket marked "← THIS TICKET" in full and skim the rest.

## Hard rules (breaking any invalidates the test)

- No BigQuery and no HelpScout data source (no `mcp__bigquery-admin` tools at all). Do not read any other folder under `runs/`, anything under `runs/2026-09-25/`, `runs/replay/_grader/`, or any file in your folder other than PACKET.md and the ones you write.
- Fathom and Google Calendar: only meetings/events dated on or before T. Jira: read-only. Every JQL you run carries `AND created <= "<T as yyyy-MM-dd HH:mm>"`, with T converted to Eastern time (JQL dates are read in America/New_York for this account, checked 2026-09-29: an issue created 16:22 UTC matches `created >= "12:22"`; UTC minus 4 in summer, minus 5 from November to March); when unsure, bound a day earlier; never open an issue by key without checking its created date first, and never read one created after T. Do not rely on status changes or comments after T. If you open a post-T issue by mistake, say so in the Jira row; the grader will not score whatever it touched.
- Nothing is sent or written anywhere except your output file. Postgres: read-only SELECTs via `mcp__supercat-postgres-vpn__execute_sql` (load with ToolSearch `select:mcp__supercat-postgres-vpn__execute_sql`). Postgres is live NOW, not at T: show `updated_at` on rows you rely on and mark values that could have changed after T.
- Code, cite commit + file:line; behaviour claims come from code or a KB article, never memory:
  - server: `~/repos/_replay_src/scs` (supercat_server @183d8e1, full history for `git log`)
  - iPad, current: `~/repos/_replay_src/ios_3.1` (sarreid_ios `release/2026.3.1` @f2e9877, build 20260909)
  - iPad, August builds: `~/repos/_replay_src/ios_2.10` (sarreid_ios `release/2026.2.10` @4ca0696, plist 20260818; approximate for 20260822)
  Match the iPad branch to the rep's `orders.app_version` at T.
- Code is not cut at T, so cut it yourself: before citing a file, `git log -1 --before=<T> -- <path>`; if the file changed after T, read it at that commit (`git show <sha>:<path>`) and say so. Both iPad clones have full history (unshallowed 2026-09-29), so the same applies to iPad code; a release branch HEAD dated after T is not evidence of what shipped at T.
- A Postgres value with `updated_at` after T, or from a table that reloads daily (customers, inventory, options), cannot prove the state at T. Label it "changed after T" in VERIFY and don't put it in the copy as fact; use events that are dated (orders, import_events, audit_log_entries, login_events) for state at T.
- KB: https://supercatsolutions.com/knowledgebase (WebFetch). If no article exists, say "none exists".

## Read first

`/Users/kylorjohnson/repos/supercat-4.0/CLAUDE.md`; then in `/Users/kylorjohnson/repos/supercat-4.0/onboarding-agents/3-helpscout/`: `ecat-correspondence/SKILL.md` (§ 4-0, § 6, § 7 with step 0, the VERIFY table and the two copy rules), `ecat-support-triage/SKILL.md`, `ecat-client-email/SKILL.md` and `ecat-client-email/CLAIMS_STANDARD.md` (read it before writing the client text; it is what the verifiers check). Route to domain skills under `~/.claude/skills/ecat-*` as triage directs. Client folders: `~/repos/ecat-onboarding-workspace/02_Implementation/` (files modified after T unavailable). Org registry: `organizations` (column `shortname`); some domains span several orgs, attribute from the thread.

## How this brief and the skills fit

The brief overrides `ecat-correspondence` in the three places its § 0 lists (draft whatever the scope, reply in-thread, these sources and cuts). Everything else in the skills binds, including the gate: an out-of-scope ticket gets a category marked "if in scope".

## Task

Draft the reply to the last client message on the ticket at T. Consolidate per client, diagnose, ground in live state (values, not just events), verify behaviour in code, and draft in Kylor's voice, signed "Kylor" whoever the ticket is assigned to.

## Output file sections, exactly

1. Header: ticket, client + org shortname/id (or unattributed), cut time, category (SEND-SAFE / DRAFT-AND-PING / ESCALATE) and the § 6 clause, scope line (inbox + assignee).
2. `## VERIFY` table: thread / live state / code (server) / code (iPad) / KB / meetings / Jira, each cited or NOT CHECKED. Then a `Conclusion:` line.
3. `## What the client said`: key quote, dated and attributed.
4. `## Draft`: the reply in a fenced code block.
5. `## Owner actions before this goes`: numbered exact steps.
6. `## Also found`.

Final message back: category, a two-sentence diagnosis, the three most important citations. Under 150 words.

## Verify pass and revision (replay)

The session that launched you runs `ecat-correspondence` § 6 step 6 for you: after you finish, **two separate** verifier agents run `tools/VERIFY_PASS_BRIEF.md` on your file, each appending its own `## Verify pass <round><a|b>`. A row either one flags counts. If the round is FAILED, you get the file back with one instruction: revise. Then:

- fix each flagged row (false, unsupported, NOT CHECKED, withheld, unneeded ask) with evidence, delete the sentence, or turn it into an owner action. Unverifiable-at-T rows are caveats, not failures; leave them unless you can prove them from dated evidence. **Fix the sentence, not the answer:** keep the verified cause or fix in the copy with corrected wording; a reply cut down to a holding note fails as `withheld`. Don't ask the client for anything the packet or a query already holds. Don't argue with a row in the copy; if you think a verifier is wrong, say why in one line under the table, with the evidence;
- re-read Owner actions and Also found against the final copy and update or drop anything that no longer matches it;
- rewrite `## Draft` in place and add `## Revision <n>` listing each row and what you did;
- the launcher runs the next round with two new verifiers, at most three rounds. A draft still FAILED after the third gets `VERIFY FAILED` in its header.

You never run the verify pass on your own draft.

## Rule for whoever edits the skills

Skill examples describe the pattern, never the replay ticket number. A skill that names a test ticket leaks the answer into that ticket's next replay (found 2026-09-28: three regression drafts cited skill lines about their own tickets).
