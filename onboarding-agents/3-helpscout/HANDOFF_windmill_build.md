# Handoff: build the HelpScout drafting agent for Windmill

Paste everything below the line into a **new** Claude Code session opened on `~/repos/supercat-4.0` on the owner's Mac (the machine with the VPN, the MCP servers and the gitignored test record). Written 2026-09-30.

---

You are taking over the HelpScout drafting agent ("agent 3"). It drafts replies to eCat support and onboarding tickets and **never sends**. A colleague of the owner defined what the Windmill version needs. Your job is those two deliverables, built safely:

> 1. **Context library / inventory** of ticket types, response types, etc., so it knows what a good vs bad reply looks like depending on the request. Required; can live in GitHub.
> 2. **GitHub code and Windmill scripts.** Required; that's the agent's code you'll develop.

## STOP: rules that override everything below

**Repos:**
- `~/repos/supercat-4.0` is the owner's own repo (`kylor-johnson/supercat-4.0`). You may commit there on a branch.
- `~/repos/agent-factory` is **SuperCat's shared company repo** (`SuperCatSolutionsLLC/agent-factory`), and other people's live agents and docs are in it. On 2026-09-30 an earlier handoff led an agent to write straight onto its `main`, including shared files; it had to be undone. That must not happen again.

1. **Nothing is written in `~/repos/agent-factory` until the owner approves a written plan in this conversation.** Read it read-only (`git -C ~/repos/agent-factory fetch` is fine; don't pull or check out in the owner's checkout). Its local `main` is 103 commits behind `origin/main`, so read `origin/main` (`git show origin/main:<path>`).
2. **After the owner's written yes:**
   - Create a separate worktree on a new branch: `git -C ~/repos/agent-factory worktree add ~/repos/agent-factory-helpscout -b <branch> origin/main`. Name the branch per agent-factory's `AGENTS.md` convention (it says `kjael/<topic>`; confirm the name with the owner first).
   - Never touch the owner's checkout or `main`.
3. **Never push, open a PR, run `wmill sync`/`wmill` deploys, or change Windmill schedules or resources** without a separate, explicit yes for that step.
4. **Don't edit agent-factory's shared files** (`AGENTS.md`, `README.md`, `docs/`, `standards/`, `platform/`, `windmill/f/platform/`, other agents' folders) unless the owner approves that exact edit. The agent is self-contained in its own folder.

**Data and access:**

5. **Client data never goes in git.** Ticket text, client names, contact names and ticket numbers stay in the gitignored `onboarding-agents/3-helpscout/runs/`. Anything committed is de-identified: patterns, shapes, role names.
6. **Read-only everywhere:** Postgres SELECT only via `mcp__supercat-postgres-vpn__execute_sql`; BigQuery SELECT only via `mcp__bigquery-admin__query`; Jira read-only (see CLAUDE.md); no HelpScout writes, no emails, no Slack. Never load a service-account key or call an MCP endpoint from a script. If the classifier blocks something, report it; don't work around it.

**Runs and commits:**

7. **Before any multi-agent or model run,** state the agent count, expected minutes and a rough token cost, and get the owner's OK. Default to 5 tickets, no more than 3–5 agents at once. The owner's usage limit is shared with his other work; a run on 2026-09-29/30 hit it twice.
8. Committed files refer to people by role. Commit messages end with the co-author line from the system prompt.

## Read first (in this order)

1. `CLAUDE.md`, then the memory index `~/.claude/projects/-Users-kylorjohnson/memory/MEMORY.md` and these notes:
   - `feedback_handoffs_guard_company_repos.md`
   - `feedback_agent_runs_must_be_short.md`
   - `helpscout_replay_eval.md`
   - `helpscout_drafts_scope_and_validation.md`
   - `feedback_replay_is_about_agent_not_sending.md`
   - `audit_log_entries_holds_no_config_events.md`
   - `project_ecat_eve.md`
2. The agent as it stands on `main` (all committed and pushed):
   - `onboarding-agents/3-helpscout/ecat-correspondence/SKILL.md`: the loop, scope § 3a, gate § 5, draft steps § 6.
   - `ecat-support-triage/SKILL.md`: diagnosis and code-backed symptom checks.
   - `ecat-client-email/SKILL.md` and **`ecat-client-email/CLAIMS_STANDARD.md`**: what a client sentence may claim. It's the core of "good vs bad".
   - `tools/VERIFY_PASS_BRIEF.md`, `tools/lint_client_text.py`: the verify loop (free lint, then one separate verifier on sonnet, at most two rounds).
   - `tools/PACKET.md` and the `replay_*.sql` files, plus `packet_assemble.py`: the replay harness.
3. `onboarding-agents/3-helpscout/HANDOFF_agent_factory_windmill.md`: the evidence summary and the Windmill blockers (data source, Postgres path, code reads, Fathom, Calendar, Jira, KB, separate model calls, Windmill-only CI).
4. The gitignored test record in `onboarding-agents/3-helpscout/runs/replay/`:
   - `_grader/`: `FIX_PLAN.md`, `REDRAFT_CHECK_RESULT.md`, `CHEAP_VERIFY_RESULT.md`, `GRADES_B7.md`, `GRADES_B8.md`, `DEFECTS_B7.md`, `DEFECTS_B8.md`, `REDRAFT_CHECK_KEY.md`, `DRYRUN_VERIFY_RESULT.md`
   - `b7/`, `b8/`, `_redraft_check/`: drafts, each with a `GRADE.md` and `OWNER_BLIND.md`
5. Read-only in agent-factory (from `origin/main`): `AGENTS.md`, `README.md`, `standards/adr/001-craft-placement-and-compile.md`, `standards/topologies/`, `standards/evals/gold_sets.md`, `docs/WINDMILL_ONLY.md`, `docs/helpscout_warehouse.md`, `docs/DATA_SOURCE_REFERENCE.md`, and one existing agent end to end as the pattern to copy: `agents/insightful_product/` (authored source) with its runtime `windmill/f/agents/insightful_product/` (both verified present on `origin/main` 2026-09-30).

## Where things stand (facts, dated 2026-09-30)

- **Drafts still carry errors.** Held-out batches 7 and 8 had a false or unsupported sentence in the client text in ~45% of drafts, even when the diagnosis was right.
- **The claims standard fixes the known error shapes:** 0 of 13 re-drafts repeated their earlier error.
- **The cheaper verify loop** caught 6 of 6 known errors on 5 drafts at ~100–150k tokens and 1.5–4 min per pass. Its precision (5–10 flags per draft) and the full loop with revision are unmeasured.
- **The live-run bar is not met:** at most 1 of 20 held-out drafts with a client-text error, 0 wrong SEND-SAFE, every ESCALATE caught, and a **human** blind check. The earlier "owner sheets" were filled by Claude sessions, not by the owner.
- **Reported by the reverted port attempt, not yet re-verified by you:**
  - `WELD_RAW.helpscout__conversation` has `assignee_id` on 5,789 of 5,790 rows, with unassigned stored as id 1 (Hevo stores NULL).
  - The CEO onboarding job already uses a hosted read-only Postgres SSE client in Windmill.
  - `code_index` is the Windmill path for code reads.
  - The Fathom warehouse table is stale (latest 2026-02-04).
  - Calendar, Jira and the KB have no read resource for this agent.
- **A client's Azure client secret** sits in a HelpScout email (2026-06-10 15:35 UTC) and in BigQuery. Redact it from anything you build. The owner is handling rotation.

## Deliverable 1: the context library (do this first; it needs no company-repo access)

Build it in **`~/repos/supercat-4.0/onboarding-agents/3-helpscout/library/`**, de-identified, on a branch (`git switch -c helpscout-library`). It moves into agent-factory later, with the code, on the approved branch.

1. **`TICKET_TYPES.md`: the inventory of request types.**
   - Derive the taxonomy from real data: BigQuery `onboarding_assessment.helpscout_tickets` over the last 90–180 days. Use the `tags` column, mailbox, and the client message's text for untagged tickets. `HARDENING_PLAN.md` has a starting tag table.
   - Cluster into roughly 12–20 types by what the client needs, not by tag name. Examples: "import didn't show up", "can't log in / access", "prices or stock not showing", "fewer items than expected", "order won't submit / export", "Sales Portal numbers", "setup question for a new feature", "scheduling / chase", "billing or contract".
   - For each type, record:
     - the count and share;
     - the signals that identify it;
     - the facts the agent must check first (from `ecat-support-triage`'s symptom checks);
     - the domain skill it routes to;
     - the usual gate category.
2. **`RESPONSE_TYPES.md`: what kind of reply each situation calls for.** Types include:
   - direct answer;
   - answer with a check first;
   - diagnosis plus the client's next action;
   - owner action plus a holding line (only when required);
   - recap note for onboarding clients mid-build;
   - correction of our own earlier reply (ESCALATE);
   - chase on something we owe (ESCALATE);
   - scheduling;
   - acknowledgment (no reply).

   For each: when to use it, required parts, forbidden parts, and length.
3. **`GOOD_VS_BAD.md`: paired examples per ticket type**, de-identified:
   - **Good:** the reply that actually resolved it, confirmed by the outcome in later threads (see the outcome cards in `GRADES_B7/B8.md` and `REDRAFT_CHECK_RESULT.md`).
   - **Bad:** the draft errors graded in batches 5–8 and the re-draft check. Each with the violated rule from `CLAIMS_STANDARD.md`.
   - Paraphrase the shape; no client names, contact names, ticket numbers or verbatim client text. Keep the raw source rows (ticket, conversation_id, quote) in a gitignored `runs/library_sources.md` so every example is traceable.
4. **`library/README.md`:** how the drafter and the verifier use the library. Probably: classify the ticket type first, load that type's checks and response type, and let the verifier flag a reply that doesn't match. Add a short `LIBRARY_EVAL.md` plan: which graded tickets become golden-set cases, and what each one asserts.
5. Show the owner the library before starting deliverable 2. Commit on the branch; **push only with his yes.**

## Deliverable 2: GitHub code and Windmill scripts (plan first; build only after approval)

1. **Write `onboarding-agents/3-helpscout/PORT_PLAN.md`** (in supercat-4.0, not agent-factory), covering:
   - the target folder `agents/helpscout_correspondence/` and runtime path `windmill/f/agents/helpscout_correspondence/`;
   - every file you'd create;
   - any shared file you'd need to touch, and why;
   - the topology (operator skill at human-approve is the likely fit; confirm with the owner);
   - how each blocker is resolved: data source and scope, Postgres, code reads, Fathom/Calendar/Jira/KB (degraded and marked in each draft header if no resource);
   - the drafter/verifier as two separate model calls (verifier on sonnet, no shared context);
   - the lint as a deterministic step;
   - per-draft time and token caps logged to Langfuse;
   - where drafts go: private to the owner, never HelpScout;
   - the golden set built from the library and the graded tickets;
   - how it is tested in Windmill only (no GitHub Actions).

   Re-verify each "reported" fact above with a read-only query before relying on it.
2. **Stop and ask the owner to approve the plan.** Name the branch and the worktree path.
3. **After approval,** build in the worktree only. Commit locally, run the golden set locally or in Windmill **only with a yes**, and report. Push, PR and deploy each need their own yes.
4. The first model run is **5 tickets**, with agent count, time and tokens stated first. Batch 9 (the 20-ticket live-run gate, tickets first messaged on or after 2026-09-29) uses `runs/replay/HANDOFF_B9_BUILDER.md` and `_grader/HANDOFF_B9_GRADER.md`, and only after the 5-ticket run looks right.

## When you finish a step

Report in under 150 words:
- what you built (paths);
- what you verified (queries, file:line);
- what you did not do, and why;
- the exact next decision you need from the owner.

Never describe an unverified fact as verified.
