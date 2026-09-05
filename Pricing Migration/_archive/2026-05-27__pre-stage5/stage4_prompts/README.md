# Stage 4 — Per-Account Production Drafting Prompts

> **Drafted**: 2026-05-26 by Stage 4 planning agent
> **Purpose**: Produce per-account briefs + delivery emails for ~85 accounts under the 5 operator-approved Stage 3 templates (Format A | Format B | CEO Letter | Good News | entity-packet parent letter). Each `stage_4_X__<format>__per-account-drafter.md` prompt drives a fresh Cursor agent session that takes ONE `ord_id` in and produces ONE brief + ONE delivery email out.
> **Audience**: The operator (CEO) who paste-runs these prompts into fresh Cursor agent sessions, one account at a time.

---

## What this folder is

Each `stage_4_X__<format>__per-account-drafter.md` file in this folder is a **paste-ready prompt** for a fresh Cursor agent session. Each prompt produces **2 per-account output files** (one brief in `<format>-notices/` + one delivery email in the same folder) for ONE account, identified by `ord_id` parameter substitution at paste time. The output is operator-stamped and sent to the client per Phase 6 cohort scheduling.

This folder ALSO contains:

- `PLANNING_AGENT_HANDOFF.md` — the canonical onboarding document for any Stage 4 planning agent (this includes you if you take over). Required reading before any Stage 4 work. **Amended 2026-05-26 with 3rd top-of-file amendment block** for the Stage 4.1 → Stages 4.2–4.5 intra-stage takeover; §2 / §3 / §5 / §8 / §9 surgical edits + Appendices B.4 + B.5 added (834 lines).
- `stage_4_session_handoff_to_4_2-4_5.md` — **NEW 2026-05-26** — paste-ready prep prompt for the Stage 4.1 → Stages 4.2–4.5 intra-stage planning-agent handoff (98 lines; thin wrapper for operator paste-run into a fresh Cursor agent). Operator-stamped fresh-agent handoff per direct context-overload observation at Stage 4.1 closeout. The fresh agent receiving this prep prompt reads `PLANNING_AGENT_HANDOFF.md` in full + produces the §8 handoff confirmation block + awaits operator stamp before proceeding per §9 first-action sequence. **Pattern**: future intra-stage handoffs (Stage 4.2 → 4.3, etc.) follow the same convention — outgoing agent appends a new top-of-file amendment block to `PLANNING_AGENT_HANDOFF.md` + authors a `stage_4_session_handoff_to_<next_phase>.md` prep prompt.
- `stage_4_prep_a__root_04_three_extensions.md` — Source-fix Session A prep prompt (3 `_root/04` extensions per Stage 4 prep candidates Q1 + Q3 + Q4). **RESOLVED 2026-05-26** (CL-015 landed at `_root/04 §4.16`; §1.1 audience register added; §3 forbidden-phrase table extended 26 → 32 rows).
- `stage_4_prep_b__wave_6_batch.md` — Source-fix Session B prep prompt (`_root/07 §7.5` per-format delivery-email matrix + `_root/08 §10` entity-packet QB-NNN block per Stage 4 prep candidates Q2 + Q5). **RESOLVED 2026-05-26** (CL-022 landed at `_root/07 §7.5`; `_root/08 §10` QB-127–QB-138 landed; Stage 3.5 deferred item #5 closed).
- `stage_4_1__format-a__per-account-drafter.md` — Stage 4.1 Format A 60-Day Notice per-account drafter prompt (638 lines). **OPERATOR-APPROVED 2026-05-26** (production proof `lpf` APPROVED 2026-05-26; ledger row filed). The gold-standard per-account drafter prompt for Stage 4; pattern reference for Stages 4.2 / 4.3 / 4.4 / 4.5.
- `_paste-ready/` — per-session paste-ready artifacts; operator-stamped paste pattern 2026-05-26 (Stage 4.1 first-proof prep). Each fresh-agent session has a corresponding `_paste-ready/stage_4_X__<ord_id>.md` (or `_paste-ready/stage_4_5__<entity_slug>.md` for entity-packet parent-letter sessions) created by the planning agent immediately before paste. The paste-ready file (a) carries the canonical drafter prompt with `[ORD_ID]` (or `[ENTITY_SLUG]`) substituted by the planning agent + (b) prepends a planning-agent annotation block with the routing pre-flight trace (**parsed via `csv.DictReader` per Appendix B.5.1; never visual column inspection**) + CSV-canonical reconciliation + data observations specific to that account / entity. Operator copies the paste-ready file's content + pastes into a fresh Cursor agent chat as the first message; no operator-side substitution required. The paste-ready file serves as the auditable session artifact (which paste snapshot corresponds to which session). **Stage 4.1 precedent**: `_paste-ready/stage_4_1__lpf.md` (735 lines; APPROVED 2026-05-26).
- `README.md` — this file.

These prompts exist because:

1. **The path-reference inversion is load-bearing at production time.** Stage 3 templates carry `[INSERT _root/XX §N.M ...]` pointers — they are scaffolding. Stage 4 per-account artifacts carry the *actual verbatim rule prose* fetched from the owning `_root/` doc, with bracketed tokens substituted from `_master-account-data-v6.2.csv` + `_master-entity-data-v6.2.csv` + Postgres MCP live data. Paste character-for-character; paraphrase is automatic fail per the strict-placeholder precedent operator-stamped 2026-05-26 at Stage 3.1 review pass (see PLANNING_AGENT_HANDOFF.md §4 architectural concept #8 + Appendix A.5).
2. **The per-account session shape is `ord_id`-scoped.** One account in, two files out, conformance block, STOP. Batch drift = automatic fail. The 4 archived per-account prompts batched 3 accounts each; this is forbidden in Stage 4 per the per-account session shape established at Stage 5 architecture (see PLANNING_AGENT_HANDOFF.md §4 concept #9 + Appendix A.7).
3. **Fresh-agent independence is the drift-detection mechanism.** A fresh drafter agent — loaded with only the prompt + `_root/` + the routed `_root/04` voice rules + the routed `_root/05` driver block + the routed template + the v6.2 row + Postgres data for that one account — produces a per-account artifact that mechanically respects the path-reference contract. The planning agent that designed the rule layer carries enough context that it would unconsciously paste in convenient verbatim text or smooth over driver-block transitions. The fresh agent will not.

---

## Wave sequence (operator-stamped 2026-05-26 — default 4.1 → 4.5)

| Sub-wave | Output (per session) | Independence | Run order |
|---|---|---|---|
| **Stage 4 prep — Source-fix Session A** | In-place edits to `_root/04` (3 extensions: `§1.1` audience register + `§3` SaaS-renewal forbidden-phrase rows + `§4.16` Annual-overlay voice). Single fresh-agent session; one doc edited. | Independent of Source-fix Session B. Required BEFORE stage_4_1 paste-runs (stage_4_1 references the new `§1.1` audience register + `§3` SaaS-renewal forbids; Annual accounts also reference `§4.16`). | Prep prompt authored 2026-05-26 — `stage_4_prep_a__root_04_three_extensions.md` (446 lines). PASTE-PENDING. After fresh-agent output lands, planning agent reviews + applies `_root/CONTRACTS.md §3` propagation sweep (changelog + manifest bumps + `_root/06 §4.3` cross-reference update). |
| **Stage 4 prep — Source-fix Session B (Wave 6 batch)** | In-place edits to `_root/07` (`§7.5` per-format delivery-email matrix) + `_root/08` (NEW `§10` entity-packet QB-NNN block; ~11 new checks at QB-127+). Single fresh-agent session; two docs edited. | Independent of Source-fix Session A. Required BEFORE stage_4_5 paste-runs (stage_4_5 entity-packet drafter references `_root/08 §10` EP-* checks); recommended BEFORE stage_4_1 paste-runs (stage_4_1 delivery email references `_root/07 §7.5`). | Prep prompt authored 2026-05-26 — `stage_4_prep_b__wave_6_batch.md` (429 lines). PASTE-PENDING. After fresh-agent output lands, planning agent reviews + applies propagation sweep (changelog + manifest bumps + entity-packet template Section 4 EP-* → QB-NNN conversion + cross-references at `_root/04 §4.15.N` + `_root/06 §1.6`). |
| **4.1** | `format-a-notices/<ord_id>__<slug>__brief.md` + `format-a-notices/<ord_id>__<slug>__delivery-email.md` (per `_root/07 §6` naming convention) for ONE Format A account. | Independent of 4.2/4.3/4.4/4.5. Best run first per operator stamp 2026-05-26 — Format A is the simplest format (CS-led, passive close, 6 increase-side drivers, no CEO involvement) and the resulting per-account-session pattern informs 4.2/4.3/4.4/4.5 review. **One production proof account** is paste-run + planning-agent-audited + operator-stamped BEFORE any other Format A account runs. | Prompt authored after Sources-fix Sessions A + B land + propagation sweeps complete. Planning agent recommends low-risk Tailwind-T1 Format A non-ABTS production proof candidates via `AskQuestion`; operator selects. |
| **4.2** | `format-b-notices/<ord_id>__<slug>__brief.md` + `format-b-notices/<ord_id>__<slug>__delivery-email.md` for ONE Format B account. | Independent of 4.1/4.3/4.4/4.5. Parallelizable AFTER 4.1 proof account approved. **One production proof account** per format before scaling. | Prompt authored after Stage 4.1 proof account operator-stamped + Stage 4.1 patterns extracted for inheritance into 4.2 prompt. |
| **4.3** | `ceo-letter-notices/<ord_id>__<slug>__brief.md` + `ceo-letter-notices/<ord_id>__<slug>__delivery-email.md` for ONE CEO Letter account. Carries 3-location date parity contract per Stage 3.3 review pass operator stamp 2026-05-26 (specific calendar date in close + brief routing block + delivery email routing block — drift = hard send blocker). | Independent of 4.1/4.2/4.4/4.5. Parallelizable AFTER 4.2 proof account approved. **One production proof account** per format before scaling. | Prompt authored after Stage 4.2 proof account operator-stamped. |
| **4.4** | `good-news-notices/<ord_id>__<slug>__brief.md` + `good-news-notices/<ord_id>__<slug>__delivery-email.md` for ONE decrease-side (Good News) account. Smallest cohort (~13 accounts per `_root/02 §5` Good News slice); CSM signature; no formal-notice line per `_root/04 §4.12` Good News exception. | Independent of 4.1/4.2/4.3/4.5. Parallelizable AFTER 4.3 proof account approved. **One production proof account** per format before scaling. | Prompt authored after Stage 4.3 proof account operator-stamped. |
| **4.5** | `entity-packets/<entity_slug>/<entity_slug>__parent-letter.md` + `entity-packets/<entity_slug>/<entity_slug>__parent-letter-delivery-email.md` for ONE entity (parent letter artifact only; per-child notices dispatched to 4.1/4.2/4.3/4.4 per child's format per the entity-packet orchestration playbook in the per-account ledger). Per Stage 4.5 sub-structure operator stamp 2026-05-26: **one-prompt-plus-playbook** (single drafter prompt for parent-letter artifact; planning-agent ledger orchestrates per-child dispatch). 13 entities in scope per `_root/06 §1.6` (Ferguson excluded via mixed-direction one-off exception). | Independent of 4.1/4.2/4.3/4.4 for parent-letter artifact; per-child notices DEPEND on 4.1/4.2/4.3/4.4 prompts existing (per-child notices are dispatched to the per-format prompt that matches each child's format per the routing flow). Run AFTER 4.4 proof account approved AND all 4.1/4.2/4.3/4.4 prompts authored. **One production proof entity** before scaling to remaining 12 entities. | Prompt authored after Stage 4.4 proof account operator-stamped. |

**Total**: 5 per-format drafter prompts + 1 orchestration playbook (Stage 4.5 child dispatch). Each per-format prompt drives ~17 per-account fresh-agent sessions on average (~85 accounts ÷ 5 formats). Total fresh-agent sessions across Stage 4: ~85 standalone + 13 entity parent letters + ~30 entity-child notices dispatched to per-format prompts = ~128 fresh-agent sessions across Phase 4-production.

---

## The production proof gate (mandatory before scaling each format)

Per operator stamp 2026-05-26 + handoff §9 step 5:

1. After `stage_4_X__<format>__per-account-drafter.md` is authored, planning agent recommends 1–3 low-risk production-proof candidate accounts via `AskQuestion` (criteria: Tailwind T1/T2 with clean v6.2 data; no driver edge cases like `special_arrangement`; no ABTS/Critical-band overrides; no Annual overlay UNTIL Source-fix Session A `§4.16` lands; no entity-packet membership UNTIL Source-fix Session B `§10` lands; for CEO Letter — no ambiguous `delivery_owner`).
2. Operator selects ONE proof `ord_id` and paste-runs `stage_4_X` with that `ord_id` substituted at the top.
3. Fresh agent produces brief + delivery email + conformance block.
4. Planning agent runs full per-account audit (every applicable QB-NNN check; path-reference contract verification; cross-doc parity check for CEO Letter; CSV-canonical re-derivation cross-check per Q6 baseline design constraint).
5. Planning agent surfaces audit results to operator via `AskQuestion`. Operator stamps approve-to-send OR direct revision.
6. ONLY AFTER the production proof is operator-stamped do additional Format-X accounts begin paste-runs.
7. After all 5 stage_4_X prompts have their production proof operator-stamped (5 total proofs), planning agent surfaces bulk-production decision via `AskQuestion` per handoff §9 step 6.

**The production proof gate compounds with the Wave-6 batch protection**: by the time Stage 4.1 proof runs, Sources-fix Sessions A + B have landed → `_root/04 §1.1` audience register, `§3` SaaS-renewal forbids, `§4.16` Annual voice, `_root/07 §7.5` delivery-email matrix, and `_root/08 §10` entity-packet QB checks all exist at canonical source. Drafter has zero ambiguity at any cross-reference; planning agent has zero ambiguity at any audit cross-reference.

---

## Why prompts are drafted in waves rather than all at once

Same discipline as Stage 3 (see `_meta/stage3_prompts/README.md`): pattern-inheritance compounds across waves, and per-account-session learnings inform downstream prompt design.

1. **Pattern inheritance**. Stage 4.1's prompt establishes the per-account session pattern (routing pre-flight ledger; CSV-canonical re-derivation block; pointer-resolve-then-paste-verbatim flow; conformance-block specifics). Stage 4.2/4.3/4.4/4.5 prompts are materially tighter when they cite "match the per-account session pattern in `stage_4_1__format-a__per-account-drafter.md` Step N" rather than re-specifying the convention from scratch.
2. **Cleanup-tracker + ledger evolution**. Each Stage 4.X fresh-agent session may surface new edge cases via its conformance block (e.g. a Format B account where `secondary_drivers` includes `included_user_reduction` AND the v6.2 row is missing IUR threshold data — informs Stage 4.3 CEO Letter prompt's IUR handling section). The ledger row also surfaces patterns (e.g. routing-CSV `nuances` consistently carrying renewal date info that v6.2 doesn't — informs Stage 4.4 Good News prompt's renewal-date handling).
3. **Production proof drives downstream prompt revisions**. The Stage 4.1 proof account's planning-agent audit may surface a prompt-design issue (e.g. CL-024-class drift — fresh agent paraphrased a `_root/04` rule despite strict-placeholder discipline). Catching at proof is much cheaper than catching at bulk-production; the next stage_4_X prompt incorporates the revision.

This is the same discipline baked into Stage 3 and Stage 2: don't pre-author against unknown shape; let the upstream output inform the downstream spec.

---

## The review protocol (mandatory between every per-account session)

For every `stage_4_X` paste-run:

1. **Planning agent prepares the `_paste-ready/stage_4_X__<ord_id>.md` artifact** per the per-session paste pattern operator-stamped 2026-05-26. The artifact carries the canonical drafter prompt with `[ORD_ID]` resolved + a planning-agent annotation block (routing pre-flight trace + CSV-canonical reconciliation + data observations). **Operator pastes the `_paste-ready/` file's content** into a fresh Cursor agent session as the first message; no operator-side substitution.
2. **Fresh agent runs the per-account session**: required reading per Step 1 of the prompt (manifest echo + `_root/` reading list + the routed template + the v6.2 row + Postgres MCP live data); routing pre-flight per Step 3 (re-runs the 6-step flow per `_root/06`; surfaces routing trace); CSV-canonical re-derivation per Step 4 (re-derives `delivery_owner` / `migration_driver` / `notice_cohort` / `health_band` from v6.2 row at draft time); voice-rule + driver-block fetching per Steps 5–6 (pulls verbatim from `_root/04` + `_root/05` + `_root/03` per template pointers); per-account brief + delivery email authoring per Steps 7–8; conformance block per Step 9 with the per-account-session-specific additions (routing trace; CSV-canonical re-derivation evidence; path-reference contract verification count = 0 inlined paraphrases; QB-NNN coverage; CL-024 paste-verification of any operator-stamped passages cited).
3. **Operator pastes the Conformance Block AND the agent's final chat message back to the planning agent** in the planning thread.
4. **Planning agent runs the per-account audit**:
   - Did the agent echo all required files with last-updated dates per `_root/00_manifest.md §6`?
   - Did the agent flag any conflicts, gaps, edge cases, or new CL items?
   - Is the path-reference contract respected at production-time? (Inlined paraphrased rule prose count = 0; every voice-rule sentence + driver block + tier description matches its canonical source character-for-character per CL-024 strict + paste-verification.)
   - Did the routing trace re-derive the format from the 6-step flow (not just lift `comm_action` from the routing CSV)? Per Appendix A.4 operator stamp 2026-05-26.
   - Did the CSV-canonical re-derivation match the routing CSV's `comm_action` mapping + v6.2 derived fields? Any discrepancy surfaces as routing-vs-data drift (CL-class item).
   - Does every applicable QB-NNN check pass? (Drafter's Section 4 checklist should enumerate; planning agent re-runs as audit.)
   - For CEO Letter: 3-location date parity holds (specific calendar date in close + brief routing block + delivery email routing block all identical)?
   - For entity-packet: parent letter / per-child notices coordination per ledger orchestration playbook.
   - **Reconciliation discipline check (CL-025 RESOLVED 2026-05-26 — per Appendix B.4)**: did the agent compute the `_root/07 §4.5` reconciliation flag correctly? If the flag fired, did the agent (a) render the `⚠️ USER BILLING RECONCILIATION NEEDED` line in the brief's routing block per `_root/07 §7`, (b) leave the After-row math UNCHANGED at v6.2 modeled-canonical values (`[NEW_EXCESS]` = v6.2 `excess_users`; `[NEW_MRR]` = v6.2 `new_total_mrr`), and (c) NOT introduce any client-facing language about "unused users" / "phantom accounts" / user-cleanup in the brief or delivery email body? If yes to all three, planning agent verifies the account has a row in `_meta/v6_2_reconciliation_log.md` (pre-populated from 2026-05-26 cohort sweep for 37 flagged accounts; planning agent appends a new row for any newly-flagged account post-sweep) and records the `drafter_session_id` cross-reference in the tracker row's `notes` column. The reconciliation flag is a pre-send ops cleanup trigger, NOT a brief-approval blocker per the operator-stamped Discipline (1) at Stage 4.1 lpf production proof closeout.
5. **Planning agent surfaces audit results to operator via `AskQuestion`**: per-check pass/fail; any flagged drift; specific revision requests if needed. Operator stamps approve-to-send OR direct revision.
6. **Approved per-account artifacts trigger ledger row update** authored by the planning agent in `_meta/stage4_account_ledger.md`: `ord_id | company_slug | format_routed | drafter_session_id | brief_path | email_path | routing_trace | review_date | operator_stamp_date | notes`. The ledger is the cohort-execution authoritative tracker for Phase 6.
7. **Any new CL-class items surfaced** are filed in `_meta/stage3_cleanup.md` (CL-NNN continues from existing sequence — Stage 3 cleanup tracker is the canonical CL home for the program). Source-fix sweeps for new CL items follow the `_root/CONTRACTS.md §3` protocol; planning agent may author follow-up `stage_4_prep_C` (or equivalent) prep prompts for fresh-agent source-fix sessions if CL items warrant rule-layer changes mid-production.

The operator does NOT run additional accounts under a `stage_4_X` format until the current account's output has been operator-stamped and ledger-updated.

---

## What each prompt produces (and what it does NOT produce)

| Each Stage 4.X per-account prompt produces | Each Stage 4.X per-account prompt does NOT produce |
|---|---|
| 1 brief in `<format>-notices/<ord_id>__<slug>__brief.md` per `_root/07 §6` naming convention | New templates (templates are owned by `<format>-notices/_brief-template.md` + `<format>-notices/_delivery-email-template.md`; modifying templates requires Stage 3-class rule-change protocol per `_root/CONTRACTS.md §3`) |
| 1 delivery email in `<format>-notices/<ord_id>__<slug>__delivery-email.md` per `_root/07 §6` | New rules (rules are owned by `_root/`; any new rule needs `_root/CONTRACTS.md §3` rule-change protocol + a Source-fix Session prep prompt for fresh-agent authoring) |
| Verbatim `_root/03`/`_root/04`/`_root/05`/`_root/06` rule prose fetched per template pointers + substituted with v6.2 + Postgres data | Per-account ledger row update (the planning agent files the ledger row at review-pass approval; the per-account drafter does NOT touch the ledger) |
| Conformance block per `_root/00_manifest.md §5` + per-account-session-specific additions | Cross-account batching (one account per session is absolute — see Appendix A.7) |
| Routing trace re-deriving format from 6-step flow per `_root/06` | Format choice from `comm_action` alone (drafter re-derives per Appendix A.4 routing-as-hard-gate stamp) |
| CSV-canonical re-derivation block per Q6 baseline design constraint (re-derives `delivery_owner` / `migration_driver` / `notice_cohort` / `health_band` from v6.2 row at draft time) | Inlined paraphrased rule prose (every rule sentence is pulled verbatim per CL-024 strict + paste-verification) |
| QA-checklist Section 4 with applicable QB-NNN checks cited (drafter's checklist; planning agent re-runs as audit) | Verbatim QB-NNN check text (checks stay in `_root/08`; the brief's Section 4 cites by ID + applies-to scope only) |
| Flag-and-stop on missing data / conflicting sources / unexpected edge cases per `_root/CONTRACTS.md §2` | Improvised handling of edge cases (drafter never invents; flags and stops; operator decides) |

The per-account brief is the substantive artifact. The per-account delivery email is the slim wrapper that delivers the brief. The Stage 4 drafter pulls the canonical Stage 3 template, fetches the named `_root/` verbatim blocks per pointer, substitutes placeholders from v6.2 + Postgres, applies the routing trace + CSV-canonical re-derivation cross-checks, runs the QB-NNN checklist, and produces the brief + email + conformance block. The drafter never improvises rule prose, never paraphrases voice rules, never invents driver blocks, never proposes new QB-NNN checks.

---

## Why each prompt is long

Each Stage 4 per-account drafter prompt averages 400–550 lines (target band; established at Stage 4 prep). This length is intentional. The cost of a long prompt is one paste; the cost of a short prompt that fails to specify a CSV-canonical re-derivation discipline or a path-reference contract enforcement is a per-account artifact that silently paraphrases a `_root/04` voice rule (CL-024-class drift), which propagates through ~17 accounts before audit catches it.

Per Stage 3 precedent: prompt length is the operator's leverage over the fresh agent — every constraint stated in the prompt is a constraint enforced in the output.

Common elements of every Stage 4 per-account prompt (canonical 8-step skeleton per `PLANNING_AGENT_HANDOFF.md` Appendix A.11; mirrors Stage 3.3 gold-standard pattern):

- **Step 1**: Role + design constraints (job-naming lock per Appendix A.1; Appendix A.1–A.12 embedded verbatim — operator-stamped 2026-05-26 design constraints that govern every Stage 4 drafter session).
- **Step 2**: Required reading (every `_root/` doc + the routed format's Stage 3 templates + the v6.2 row for `[ORD_ID]` + cleanup tracker for applicable CL items; manifest-echo per `_root/00_manifest.md §6`).
- **Step 3**: Routing verification (re-derive the 6-step flow per `_root/06 §2` against the v6.2 row + routing CSV; paste-cite CSV column/row/value at each step per Appendix B CSV-canonical operator stamp 2026-05-26; flag any routing-CSV-vs-v6.2-vs-derived disagreement per Appendix A.4 hard-gate stamp).
- **Step 4**: Data load (v6.2 row substitutions + 3 verbatim Postgres MCP queries per `_root/07 §4` + routing CSV `comm_action`/`post_hold_action`/`nuances` + derived metrics per `_root/07 §4.4`; fallback per `_root/07 §5` if Postgres fails).
- **Step 5**: Brief assembly (section-by-section per the routed format's `_brief-template.md`; resolve every `[INSERT _root/XX §N.M ...]` pointer by fetch-and-paste verbatim from owning `_root/` section; substitute `[BRACKETED_TOKENS]` from v6.2 + Postgres only; drafter-generated prose narrowly scoped per Appendix A.5).
- **Step 6**: Delivery email assembly (per the routed format's `_delivery-email-template.md`; Section 2 routing block per `_root/07 §7.5` per-format delivery-email matrix operator-stamped 2026-05-26).
- **Step 7**: Anti-drift discipline + QB-NNN self-audit (CL-024 strict + paste-verification; path-reference contract zero-inlined-prose target; forbidden phrases per `_root/04 §3` 32-row table; every applicable QB-NNN check in `_root/08` cited by ID).
- **Step 8**: Output + Conformance Block (write the 2 files + post conformance block per `_root/00_manifest.md §5` + per-account additions per Appendix A.10: manifest echo, routing trace, CSV-canonical reconciliation, Postgres-stat fetch, CL-024 paste-verification of every owned rule paste, QB-NNN ID-by-ID pass/fail, gaps/conflicts/open-questions for operator).

**Flag-and-stop discipline** (woven through every step per `_root/CONTRACTS.md §2`): if a `_root/` rule is ambiguous, if a v6.2 field is missing without a `_root/07 §5` fallback, if routing produces an unexpected format match, if the QB-NNN self-audit surfaces a hard fail — STOP and surface to operator; never invent. "Asking is cheap. Inventing is the drift vector."

The Conformance Block is the planning agent's single audit artifact. It enumerates files read, routing trace, CSV-canonical re-derivation evidence, voice-rule fetches, driver-block fetches, tier-block fetches, placeholder substitutions, QB-NNN check pass/fail per-check, gaps surfaced, conflicts resolved, open questions.

---

## Per-prompt explicit authorization for v6.2 + Postgres + routing CSV reads

Every Stage 4 per-account drafter prompt explicitly authorizes the fresh agent to read:

- `Pricing Migration/_master-account-data-v6.2.csv` (Standalone Accounts sheet — the canonical 109-row roster per `_root/07 §2`)
- `Pricing Migration/_master-entity-data-v6.2.csv` (Master Entity tab — the canonical 14-entity roster per `_root/06 §1.6`)
- `Pricing Migration/migration_comm_tiers_2026-05-19.csv` (routing CSV — `comm_action` + `post_hold_action` + `flags` + `nuances` per `_root/06 §5 + §7`)
- Postgres MCP `user-supercat-postgres-vpn` server, 3 verbatim queries per `_root/07 §3` (the only Postgres MCP queries permitted for production drafting; canonical query text lives in `_root/07 §3`)

This is a **per-prompt override** of the general AGENTS.md hard rules against arbitrary file reads outside `Pricing Migration/`. The override is legitimate because each prompt names the specific files + the specific Postgres queries by SQL text + the per-account scope (`ord_id = [ORD_ID]` filter).

Any other file read outside this list is a violation of the agent contract. Any Postgres query outside the 3 canonical queries in `_root/07 §3` is a violation. Fresh agents flag and stop on either; never improvise.

---

## What the planning agent does at Stage 4 (your job)

You are the planning agent. You do NOT draft client copy. You author drafter prompts; you run routing pre-flights; you review per-account outputs; you maintain the ledger; you maintain `_root/09_changelog.md` + `_root/00_manifest.md` per `_root/CONTRACTS.md §3` propagation discipline; you surface decisions to the operator via `AskQuestion`.

Specifically, at Stage 4:

1. **Author each `stage_4_X__<format>__per-account-drafter.md`** per the 9-step skeleton above. Apply Appendix A constraints verbatim; apply Q6 CSV-canonical re-derivation discipline at Step 4 of every prompt; apply pattern-inheritance from prior stage_4_X prompts (e.g. stage_4_2 inherits from stage_4_1; stage_4_3 inherits from stage_4_1 + stage_4_2; etc.).
2. **Run routing pre-flight for each per-account session**. Before recommending a production proof account, you (planning agent) re-run the 6-step routing flow against v6.2 + routing CSV joint state per Q9 operator stamp 2026-05-26; you confirm format match, driver match, cohort match. Surface ambiguities to operator before recommending the proof candidate.
3. **Audit each per-account fresh-agent output** per the review protocol above.
4. **Maintain `_meta/stage4_account_ledger.md`**: file new row per approved per-account artifact; update notes/cohort assignments as Phase 6 scheduling decisions land.
5. **File any new CL-NNN items** in `_meta/stage3_cleanup.md` (Stage 3 cleanup tracker is the canonical CL home; Stage 4 doesn't get its own tracker — CL-NNN sequence is global to the program).
6. **Apply `_root/CONTRACTS.md §3` propagation sweeps** for any source-fix authored in fresh-agent sessions you spawn (changelog entry + manifest bumps + cross-doc pointer updates + topic-index updates).
7. **Surface decisions to operator via `AskQuestion`** — production proof candidate recommendations; per-account audit pass/fail stamps; bulk-production decision after all 5 proofs land; cohort scheduling for Phase 6.
8. **Maintain pattern-inheritance discipline** across stage_4_X prompts (each new prompt cites prior prompts; structural conventions compound).

For architectural concepts + forbidden moves + the manifest-echo contract + the strict + paste-verification protocol + the routing-as-hard-gate stamp + the CSV-canonical reconciliation discipline + the audience register + the SaaS-renewal vocabulary forbids: see `PLANNING_AGENT_HANDOFF.md` §4 + §5 + §6 + §7 + Appendix A + Appendix B. The handoff is the canonical onboarding document; this README is the operating manual.

---

## What happens after Stage 4

After all 5 `stage_4_X` prompts are operator-approved with 1 operator-stamped production proof each (per the production proof gate) AND bulk-production is operator-stamped:

- **Phase 4-production**: the remaining ~80 accounts paste-run under their format-routed prompts. Each per-account session follows the review protocol above; each approved artifact gets a ledger row. Cohort assignment (June / July / Deferred / Post-Migration / Renewal-Based) is operator-stamped at ledger-row time per `_root/02 §5` cohort overlay + `_root/06 §4.3` Annual timing.
- **Phase 5 (cohort execution)**: Phase 6 cohort scheduling per `_reference/2026-05-20__execution_plan_v3.3.md §IV`. Briefs + delivery emails are sent according to cohort schedule. Send-time discipline per `_root/04 §2.14` (internal routing-note blockquote removed before send — the single highest-drift event in the program; named at canonical source as non-negotiable §2.14).
- **Post-send audit**: `_root/08` audit-only checks (post-send sweep — QB-NNN checks marked `audit-only` per `_root/08 §8`) fire at planning-agent post-send review. Surface signals to operator; feed into Stage-7-class learnings.

The Stage 4 work in this folder is the bridge from the rule layer + template layer (Stages 1–3) to per-account production output (Stage 4) to cohort-scheduled send (Phase 5). It is the highest-leverage point in the program: every per-account artifact is the final product the client reads. The care given to the prompts in this folder + the rigor of the per-account review protocol is what protects 107 customer relationships across the 2026 book normalization.

---

*Cross-references: `PLANNING_AGENT_HANDOFF.md` (architectural concepts + Appendix A constraints + forbidden moves); `_meta/stage4_account_ledger.md` (per-account ledger); `_meta/stage3_cleanup.md` (CL-NNN tracker — Stage 4 continues the sequence); `_root/CONTRACTS.md §3` (rule-change propagation protocol); `_root/00_manifest.md §5` (canonical conformance-block format); `_meta/stage3_prompts/README.md` (Stage 3 README — pattern this README mirrors).*
