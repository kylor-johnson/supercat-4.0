# Stage 2 — Root-Doc Authoring Prompts

> **Drafted**: 2026-05-22 by planning agent
> **Purpose**: Author the `_root/` doc set by delegating each doc to a fresh agent — independent of any prior planning-context bias.
> **Audience**: The operator (CEO) who pastes these prompts into fresh Cursor agent sessions.

---

## What this folder is

Each `wave_X_Y__<doc_name>.md` file in this folder is a **paste-ready prompt** for a fresh Cursor agent session. Each prompt produces exactly ONE `_root/` doc.

These prompts exist because:
1. The `_root/` doc set is the highest-leverage drift-control layer in the entire migration communications system.
2. The planning agent that designed the system carries context that — if used to author the rule docs — would unconsciously bias toward the planning prose, would skip mentally-resolved ambiguities, and would weave duplications into seemingly-clean documents.
3. A fresh agent operates from scratch, reads ONLY what the prompt directs, and surfaces gaps that the planning agent would have papered over.

This is intentional production-grade discipline. The cost is six fresh sessions; the benefit is a `_root/` set built with the same kind of independent oversight that the agent contract requires for every future draft.

---

## Wave sequence

| Wave | Doc | Independence | Run order |
|---|---|---|---|
| 1.1 | `_root/CONTRACTS.md` | Independent | Run first (or in parallel with 1.2, 1.3). Establishes the operator/agent contracts that all subsequent prompts reference. |
| 1.2 | `_root/01_why_we_are_migrating.md` | Independent | Parallel with 1.1, 1.3. |
| 1.3 | `_root/04_communication_posture.md` | Independent | Parallel with 1.1, 1.2. **Highest-leverage** — the voice doc that every template, prompt, and draft will reference. |
| 2.1 | `_root/02_who_is_being_migrated.md` | Independent | Parallel with 2.2, 2.3. Best run after Wave 1 is reviewed (so the new agent can reference completed `_root/CONTRACTS.md` and `_root/01`). |
| 2.2 | `_root/03_what_we_sell.md` | Independent | Parallel with 2.1, 2.3. |
| 2.3 | `_root/07_data_pipeline.md` | Independent | Parallel with 2.1, 2.2. |
| 3.1 | `_root/05_driver_taxonomy.md` | **Depends on Wave 1.3** (`_root/04` authored 2026-05-22) + Wave 2.2 (`_root/03`) + Wave 2.3 (`_root/07`) | Prompt drafted 2026-05-22 — `wave_3_1__05_driver_taxonomy.md`. **Parallelizable with 3.2.** |
| 3.2 | `_root/06_format_routing.md` | **Depends on Wave 2.1** (`_root/02` authored 2026-05-22) + Wave 1.3 (`_root/04`) + Wave 2.3 (`_root/07`) | Prompt drafted 2026-05-22 — `wave_3_2__06_format_routing.md`. **Parallelizable with 3.1.** |
| 4.1 | `_root/08_quality_bar.md` | **Depends on all of `_root/01`–`_root/07`** | Prompt drafted 2026-05-22 (post Wave-3 operator-stamping pass) — `wave_4_1__08_quality_bar.md`. The QA checklist indexes all rules; authored last so it can cleanly cite every rule. |
| 5 | `_root/00_manifest.md` | Depends on all | **Authored by the planning agent**, not a fresh agent. Manifests are pure indexes — there is no extraction or reconciliation work, only enumeration of already-written docs. |

**Total**: 9 fresh-agent sessions + 1 planning-agent session = the full `_root/` set.

---

## Why prompts are drafted in waves rather than all at once

Wave 1 + Wave 2 (the 6 prompts in this folder) can be drafted up-front because they have no `_root/` dependencies. Each one reads from the archive, the reference docs, and the CSVs — never from another in-progress `_root/` doc.

Wave 3 (prompts for `_root/05` and `_root/06`) and Wave 4 (prompt for `_root/08`) WILL reference completed Wave 1 / Wave 2 docs. The planning agent could draft those prompts now with vague pointers ("read `_root/04`"), but the prompt quality is materially better when the planning agent can reference completed structure ("read `_root/04` §4.6 platform-base-grown sentence"). Drafting those prompts after the upstream docs exist takes ~30 minutes per prompt and produces meaningfully tighter instructions.

This is the same discipline being baked into the system: don't pre-author against unknown shape; let the upstream output inform the downstream spec.

---

## The review protocol (mandatory between waves)

For every Wave 1 / Wave 2 prompt the operator paste-runs:

1. **Operator pastes the prompt into a fresh Cursor agent session.**
2. **Fresh agent reads required files, authors the doc, posts a Conformance Block in chat.**
3. **Operator pastes the Conformance Block AND the agent's final chat message back to the planning agent in this thread.**
4. **Planning agent reviews:**
   - Did the agent echo all required files with last-updated dates?
   - Did the agent flag any conflicts or gaps?
   - Does the authored doc respect its "owns / does not own" boundary?
   - Did the agent restate rules from other docs anywhere?
   - Are verbatim blocks preserved character-for-character (where specified)?
5. **Planning agent either approves (→ proceed to next wave) or requests revision (→ operator returns to the fresh agent with the planning agent's feedback).**
6. **Approved doc triggers a `_root/09_changelog.md` entry** authored by the planning agent.

The operator does NOT run the next prompt until the prior prompt's output has been approved.

---

## Why each prompt is so long

Each prompt averages 250–500 lines. This length is intentional. The cost of a long prompt is one paste; the cost of a short prompt that fails to specify a constraint is an authored doc that quietly violates a rule the system depends on. Prompt length is the operator's leverage over the fresh agent — every constraint stated in the prompt is a constraint enforced in the output.

Common elements of every prompt:
- **Step 1**: Required reading (with absolute file paths and section names)
- **Step 2**: What to author (section-by-section spec)
- **Step 3**: What NOT to author (drift-prevention)
- **Step 4**: Voice and format constraints
- **Step 5**: Output (replace stub + post Conformance Block in chat)
- **Step 6**: If something is missing (stop and ask, never improvise)

The Conformance Block is the operator's single audit artifact. It enumerates what the agent read, what it produced, what it skipped, and what it flagged.

---

## Anti-archive override (explicit per-prompt authorization)

Some prompts (Wave 1.3, Wave 2.1, Wave 2.2, Wave 2.3, Wave 3.1, Wave 3.2) explicitly authorize the fresh agent to read specific files inside `_archive/`. This is a **per-prompt override** of the general anti-archive rule established in `_root/CONTRACTS.md` §4.

The override is legitimate because:
- The prompt names the specific archive files to read (no scope creep)
- The reading purpose is **extraction** (pulling a specific piece of content forward into the `_root/` set), not consultation
- After Wave 2 completes, the extracted content lives in the `_root/` docs, and the archive is once again strictly OFF-LIMITS to all subsequent agents

This is the **only** legitimate pattern for reading the archive. Any other archive read is a violation of the agent contract.

---

## What happens after Stage 2

Once all `_root/` docs are authored, reviewed, and approved:
- **Stage 3**: The planning agent rebuilds the 4 active format folders (`format-a-notices/`, `format-b-notices/`, `ceo-letter-notices/`, `good-news-notices/`) with new templates that reference (never restate) rules from `_root/`.
- **Stage 4**: New per-format fresh-agent prompts are authored that point at the new templates + `_root/`.
- **Stage 5**: First per-account drafts are produced from the new system. The first 1–2 drafts per format are reviewed especially carefully — they are the proof that the system actually produces drift-free output.

The 9 prompts in this folder are the foundation for everything downstream. They warrant the care they're being given.
