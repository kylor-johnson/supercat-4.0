# Handoff: take the HelpScout drafting agent into agent-factory and Windmill

For a Cursor agent. Read the whole file before touching anything. Written 2026-09-30.

## The goal

Make the HelpScout drafting agent ("agent 3": `ecat-correspondence` + `ecat-support-triage` + `ecat-client-email`) ready to **test and deploy as a factory agent in `~/repos/agent-factory`, running on Windmill**, drafts only. "Ready" means:

1. It lives in agent-factory under the factory's own rules (`AGENTS.md`, `README.md`, `standards/topologies/`, `standards/evals/`), not as Claude Code skills.
2. It runs end to end in Windmill against real data: HelpScout, Postgres, code, KB, Fathom and Jira, all read-only.
3. It has a golden set and a Windmill-run eval that measures what matters: false or unsupported sentences in the client text.
4. It can do a dry run on the owner's real queue (§ 3a scope) that writes drafts somewhere the owner reads, and sends nothing.

It is **not** ready to auto-send, and nothing here changes that (§ 8 of the skill is a lock).

## Where things are now

**Source of truth for the agent's behaviour:** `~/repos/supercat-4.0`, branch `main` @ `4b47460` (8 commits ahead of `origin/main`, **not pushed**; ask the owner before pushing).

- `onboarding-agents/3-helpscout/ecat-correspondence/SKILL.md`: the loop, scope rule (§ 3a), gate (§ 5) and draft steps (§ 6, including the verify pass, step 6). `reference/BACKGROUND.md` holds the measurements.
- `onboarding-agents/3-helpscout/ecat-support-triage/SKILL.md`: diagnosis, GROUND sources and code-backed symptom checks.
- `onboarding-agents/3-helpscout/ecat-client-email/SKILL.md` + `CLAIMS_STANDARD.md`: voice, and what a sentence may claim. The claims standard is the most important file.
- `onboarding-agents/3-helpscout/tools/`:
  - `VERIFY_PASS_BRIEF.md`: the verifier's instructions;
  - `lint_client_text.py`: a free mechanical pre-check;
  - `DRAFTING_BRIEF.md`: replay drafting rules;
  - `PACKET.md`, `replay_threads.sql`, `replay_scope_at_t.sql`, `replay_fleet_at_t.sql`, `packet_assemble.py`: the replay harness.
- `CLAUDE.md` and `.cursor/rules/*.mdc`: import ground truth. These are in sync; keep them that way.
- The domain skills the agent routes to live in `.cursor/skills/ecat-*`, with copies in `~/.claude/skills/ecat-*`; the copies are not symlinks.

**The test record** is gitignored and lives on this Mac only: `onboarding-agents/3-helpscout/runs/replay/`. Read, in this order:

1. `_grader/FIX_PLAN.md`: the plan and its status log.
2. `_grader/REDRAFT_CHECK_RESULT.md`: the latest measured result.
3. `_grader/CHEAP_VERIFY_RESULT.md`: the cheaper verify loop's first test.
4. `_grader/GRADES_B7.md` / `GRADES_B8.md` / `DEFECTS_B7.md` / `DEFECTS_B8.md`: the error patterns.

Batches 7 and 8 are held-out replays with outcome grading.

**Already in agent-factory:**
- `docs/helpscout_warehouse.md` (the CEO System's HelpScout data notes);
- `platform/lib/helpscout_snapshot.py`;
- no correspondence agent.

**A prior port exists elsewhere:** `~/ecat-eve`, a Vercel eve project, deployed at ecat-agents.vercel.app. Its correspondence cron is deliberately disabled (memory `project_ecat_eve.md`), and it predates every fix above. Decide with the owner whether to retire it. Don't run both.

## What the evidence says (so you don't over-promise)

- Before the fixes, about 45% of drafts carried a false or unsupported sentence in the client text, even when the diagnosis was right. The errors are claims that go further than their evidence: scope, cause, counts, past-tense actions, concessions, paraphrased labels, and premises repeated from earlier messages.
- **The claims standard fixes the known shapes:** 0 of 13 re-drafts repeated their earlier error.
- **A separate verifier pass is needed**, and the two-verifier, three-round version was too slow and expensive: about 1M tokens and 30–45 minutes per draft. It has been replaced by lint, then one sonnet verifier, at most two rounds. First test (`CHEAP_VERIFY_RESULT.md`): it caught 6 of 6 known errors on 5 drafts, including 3 the old loop passed as CLEAN, at about 100–150k tokens and 1.5–4 minutes per pass. Its precision (5–10 flags per draft) and the full loop with revision are not measured yet.
- **Still getting through:** a premise carried from an earlier message and stated as fact ("the customer data from the files we've imported" when every row was rejected).
- **The live-run bar is not met.** It needs at most 1 of 20 held-out drafts with a client-text error, 0 wrong SEND-SAFE, every ESCALATE caught, and a human blind check. The owner has never done that human check himself; earlier "owner sheets" were filled by Claude sessions.

## Blockers to resolve first (each one is a real gap, verified 2026-09-30)

1. **HelpScout data source mismatch.** The agent reads BigQuery `onboarding_assessment.helpscout_tickets` (Hevo), which has `assignee_id`. Assignment history comes from lineitems in `helpscout.conversation_threads` (see `replay_scope_at_t.sql`). Windmill's `bigquery_query` defaults to `WELD_RAW`, and `agent-factory/docs/helpscout_warehouse.md` says `assignee_id` is **always NULL** there. The scope rule (§ 3a) depends on the assignee. Decide which source the Windmill agent reads, and prove scope works on it.
2. **Postgres from Windmill.** Every draft depends on live read-only Postgres (the org's state, `import_events`, `audit_log_entries`, `login_events`). In Claude Code that's the `supercat-postgres-vpn` MCP behind the VPN. Find or provision a read-only Postgres path for Windmill; check `docs/DATA_SOURCE_REFERENCE.md` and `platform/`. No credential in a script, and SELECT only.
3. **Code reads.** The agent cites supercat_server and sarreid_ios file:line. Windmill needs clones (supercat_server master; sarreid_ios's newest `release/*` branch, full history), or a read path like `code_index`. Cite the SHA in every claim.
4. **Fathom, Google Calendar, Jira (read-only), KB fetch.** The consolidation step needs them. Map each to a Windmill resource or mark the step degraded, loudly, in every draft header.
5. **Sub-agents.** The pipeline assumes a drafter plus a separate verifier with a fresh context, on a different model (sonnet). In Windmill that's two separate model calls with separate prompts and no shared context. Keep them separate; the verifier must not see the drafter's reasoning.
6. **Execution constraint.** agent-factory runs tests, gates and deploys in Windmill, **never GitHub Actions** (`docs/WINDMILL_ONLY.md`).
7. **A live client secret sits in HelpScout and BigQuery:** an Azure client secret that a client pasted into an email on 2026-06-10 15:35 UTC. Packets must redact it, and the owner or client should rotate it.

## Steps

1. **Read** agent-factory's `AGENTS.md`, `README.md`, `standards/adr/001-craft-placement-and-compile.md`, `standards/topologies/` and `standards/evals/gold_sets.md`. Pick the topology with the owner (likely `operator_skill` or a human-approve scheduled job) and add the agent to the § 3 table.
2. **Port the agent:** `agents/helpscout_correspondence/`.
   - Put the three skills' rules, `CLAIMS_STANDARD.md` and `VERIFY_PASS_BRIEF.md` in the prompts, compiled per ADR 001. `CLAUDE.md`'s import ground truth becomes doctrine.
   - `lint_client_text.py` becomes a deterministic step.
   - Keep the order: GROUND → VERIFY table → draft → lint → verifier → at most one revision → verifier → category.
   - Each draft carries its VERIFY table, Owner actions, Also found and the verifier table.
3. **Resolve blockers 1–4**, with a smoke test each: one real ticket's scope, one Postgres read, one code citation, one Fathom lookup.
4. **Golden set.** Build `golden_set.json` from the graded replay tickets. Use each ticket's known client-text errors and its outcome card (from `GRADES_B7/B8`, `REDRAFT_CHECK_RESULT.md`, and the `OWNER_BLIND.md` sheets). The eval scores:
   - false or unsupported sentences in the client text;
   - verifier recall on known errors;
   - category;
   - whether the reply still answers the ask.

   Run it in Windmill with `standards/evals/run_golden_set.py`. The sentence text of the tickets that taught a rule must not appear in the prompts (the leak rule in `DRAFTING_BRIEF.md`).
5. **Cost and time budget per draft**, enforced and logged in Langfuse: target at most about 10 minutes and a stated token ceiling. Alert when a draft breaks the budget. The owner's hard constraint: no run may exhaust his usage, and long multi-agent runs need his OK first.
6. **Dry run on the real queue**, drafts only:
   - § 3a scope: onboarding inbox (unassigned plus the owner's), support inbox (the owner's only).
   - Drafts go to a private place the owner reads; nothing to HelpScout.
   - Check the scope list by hand once with the owner.
7. **Batch 9, the live-run gate:** 20 held-out tickets first messaged on or after 2026-09-29, graded on outcome by a separate grader, plus the owner's own 4-ticket blind check. The handoffs are `runs/replay/HANDOFF_B9_BUILDER.md` (already on the lint + one-sonnet-verifier loop) and `_grader/HANDOFF_B9_GRADER.md`. Start with 5 tickets and measure verifier precision before running the rest.

## Rules that stay

- Read-only everywhere: Postgres SELECT, BigQuery SELECT, Jira read-only, no sends, no HelpScout writes.
- Drafts only; no auto-send without the fortnight comparison and the owner's explicit yes (§ 8).
- Every behaviour claim cites code (SHA, file:line), a dated Postgres row, or a KB URL.
- People by role in committed files. No client names or ticket numbers in prompts or skills.
- Before any multi-agent or long run, state the agent count, time and cost, and get the owner's OK. Default to 5 tickets, not 20.
