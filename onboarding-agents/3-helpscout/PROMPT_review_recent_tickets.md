# Prompt: review yesterday's and today's HelpScout tickets through the agent

Paste everything below the line into a **new** Claude Code session opened on `~/repos/supercat-4.0` on the owner's Mac. Change the two dates in the first line if you run it on another day. Written 2026-10-01.

---

WINDOW = 2026-09-30 00:00 UTC → now. TODAY = 2026-10-01.

You are running the HelpScout drafting agent ("agent 3") over the real tickets in WINDOW, to see how its drafts land: for tickets a human already answered, how the draft compares with the reply that went out and with what happened next; for unanswered tickets, what the draft would say. **Drafts only. Nothing is sent, posted or written anywhere outside the gitignored run folder.**

## STOP: rules that override everything below

1. **Read-only everywhere.**
   - Postgres: SELECT only, via `mcp__supercat-postgres-vpn__execute_sql`.
   - BigQuery: SELECT only, via `mcp__bigquery-admin__query`.
   - Jira: read-only (see CLAUDE.md).
   - HelpScout, Gmail, Slack: never write to them.
   - No service-account keys and no scripts that call MCP endpoints. If the classifier blocks something, report it; don't work around it.
2. **Don't touch git.** Another session is working on branch `helpscout-library` in this checkout. Don't switch branches, commit, push, stash or reset in `~/repos/supercat-4.0`, and don't touch `~/repos/agent-factory` at all.
3. **Client data stays local.** Write only under `onboarding-agents/3-helpscout/runs/live_<TODAY>/` (gitignored). Redact any credential you see. A client's Azure client secret from a 2026-06-10 email is known to sit in the data.
4. **Cost and time are budgeted.** Before launching any agent, tell the owner the ticket count, agent count, expected minutes and rough tokens, and wait for his OK. Expect roughly 10–15 minutes and ~0.4–0.6M tokens per ticket for the drafter plus verify. A grader adds ~0.15M per answered ticket. Run at most 3 tickets at a time, with **one orchestrator (you)**. Never two launchers on the same folder; check an agent is really stopped before replacing it. If a usage limit hits, stop and report what finished.
5. Never claim something is verified that you didn't check. Never call a draft "sendable"; the job is to see where the agent is right or wrong.

## Read first

1. `CLAUDE.md`. The memory index `~/.claude/projects/-Users-kylorjohnson/memory/MEMORY.md`, especially:
   - `helpscout_drafts_scope_and_validation.md`
   - `feedback_agent_runs_must_be_short.md`
   - `feedback_handoffs_guard_company_repos.md`
   - `feedback_replay_is_about_agent_not_sending.md`
   - `mcp_postgres_needs_legacy_negotiation.md`
2. The agent: `onboarding-agents/3-helpscout/`:
   - `ecat-correspondence/SKILL.md`: § 0 run order, § 3a scope, § 5 gate, § 6 draft steps including step 6 (verify);
   - `ecat-support-triage/SKILL.md`;
   - `ecat-client-email/SKILL.md` and `CLAIMS_STANDARD.md`;
   - `tools/DRAFTING_BRIEF.md`, `tools/VERIFY_PASS_BRIEF.md`, `tools/lint_client_text.py`, `tools/PACKET.md`;
   - the `tools/replay_*.sql` files, and `tools/packet_assemble.py`.
3. If present on this branch, `onboarding-agents/3-helpscout/library/` (ticket types, response types, good vs bad). Use it as reference; don't edit it.

## Phase 0: preflight (no agents)

- Confirm `/mcp` shows `supercat-postgres-vpn` and `bigquery-admin` connected.
- Record the mirror's freshness: `MAX(thread_created_at)` in `onboarding_assessment.helpscout_tickets`. It lags hours behind HelpScout. Say how many hours, and that tickets newer than that are invisible to this run.

## Phase 1: inventory (no agents; then stop and ask)

1. List every conversation with a client message (author domain not `supercatsolutions.com`) in WINDOW.
2. Dedupe twin captures across the two inboxes, keeping the onboarding copy.
3. Apply the § 3a scope **at the time of the client message**, using `tools/replay_scope_at_t.sql` logic:
   - onboarding inbox 312855: unassigned or assigned to 889305;
   - support inbox 65829: assigned to 889305 only.
4. Run § 3b–3f: drop lineitems and spam, flag automated senders (the daily inventory feeds), and do the acknowledgment pass.
5. Write `runs/live_<TODAY>/INVENTORY.md`, one row per in-scope conversation:
   - ticket and conversation_id, the client message time (T);
   - mailbox and assignee at T;
   - a one-line ask (no quotes needed);
   - **answered?** (a staff reply of 50+ characters after T: yes, with time and author role, or no);
   - classification (needs-reply / acknowledgment / automated / handled-out-of-band);
   - for needs-reply, the likely ticket type from the library if present.

   Add counts at the top, out-of-scope included, per § 4 coverage.
6. **Stop.** Show the owner the inventory, the proposed set (all needs-reply tickets, or the first 6 if there are more), and the cost and time line. Wait for his OK and his selection.

## Phase 2: draft (after OK; at most 3 tickets at a time)

For each selected ticket, in `runs/live_<TODAY>/<ticket>/`:

1. **Build the packet** per `tools/PACKET.md`:
   - threads via `replay_threads.sql` cut at T;
   - `fleet.md` via `replay_fleet_at_t.sql`, every window ending at T;
   - `scope.json`;
   - `meetings.md` (Fathom ≤ T) and `calendar.json` pre-fetched as JSON;
   - `folder.md` with post-T files as a count only;
   - then `python3 onboarding-agents/3-helpscout/tools/packet_assemble.py runs/live_<TODAY>/<ticket> --conv <id> --t <T> --client "<name>"`.

   T is the client message being answered. For unanswered tickets, that's the latest client message. The packet must hold nothing after T; for answered tickets the staff reply must not be in it.
2. **Drafter:** one general-purpose sub-agent: "Follow `onboarding-agents/3-helpscout/tools/DRAFTING_BRIEF.md` for ticket folder `runs/live_<TODAY>/<ticket>/`, output `DRAFT.md`." No hints.
3. **Lint:** `python3 onboarding-agents/3-helpscout/tools/lint_client_text.py runs/live_<TODAY>/<ticket>/DRAFT.md --out runs/live_<TODAY>/<ticket>/LINT_1.md`. A placeholder goes straight back to the drafter.
4. **Verifier:** ONE new sub-agent on the **sonnet** model, on `tools/VERIFY_PASS_BRIEF.md`, the draft, the packet and `LINT_1.md`. It writes `VERIFY_1.md`; append it to `DRAFT.md`.
5. If FAILED: SendMessage the same drafter to revise per the brief's "Verify pass and revision". Then lint again and run one new sonnet verifier (`VERIFY_2.md`). At most two rounds. A draft still failing gets `VERIFY FAILED` in its header.
6. Log per ticket: minutes and tokens, as reported by the agents.

## Phase 3: how they land

- **Answered tickets:** launch ONE grader sub-agent per ticket, after its draft is final.
  - Have it follow `onboarding-agents/3-helpscout/runs/replay/_grader/FACTCHECK_BRIEF.md`: a claim table on the draft's client text, then the sent reply and any later threads in BigQuery as the outcome.
  - It must not read the draft's verify sections before its table is written.
  - Output `GRADE.md`:
    - `Copy errors: <n> (quotes)`
    - `Cause matches outcome: yes / partly / no / no outcome yet`
    - `Action would have worked: yes / partly / no`
    - `Category: right / wrong`
    - `vs sent reply: better / same / worse, one line why`
- **Unanswered tickets:** no grader. List the draft's category, the verify result, and the one or two facts the owner would need to check before using it.

## Output

`runs/live_<TODAY>/SUMMARY.md`:
- mirror freshness and the coverage counts;
- one row per ticket: type, T, answered?, verify result, copy errors, vs sent reply, minutes and tokens;
- the two or three most instructive misses or wins, with the rule each one touches (`CLAIMS_STANDARD.md` row, skill section, or "no rule covers this").

Final message to the owner, under 200 words:
- how many tickets were in scope and how many were drafted;
- of the answered ones, how many drafts had a client-text error, and how they compare with what was sent;
- the unanswered drafts awaiting his read;
- total time and tokens;
- anything blocked.

No rule edits in this session; list candidates only.
