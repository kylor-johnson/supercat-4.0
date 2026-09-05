# Stage 3 — Format-Template Rebuild Prompts

> **Drafted**: 2026-05-26 by planning agent
> **Purpose**: Rebuild the 5 active format folders (`format-a-notices/`, `format-b-notices/`, `ceo-letter-notices/`, `good-news-notices/`, `entity-packets/`) with new templates that reference (never restate) rules from `_root/`.
> **Audience**: The operator (CEO) who pastes these prompts into fresh Cursor agent sessions.

---

## What this folder is

Each `stage_3_X__<format>__<artifacts>.md` file in this folder is a **paste-ready prompt** for a fresh Cursor agent session. Each prompt produces 1–2 template files for ONE format folder. The output is the structural skeleton drafters fill in at Stage 4 to produce per-account briefs.

These prompts exist because:

1. The pre-refactor templates inlined verbatim driver prose, voice-rule sentences, tier blocks, and forbidden-phrase replacements. Every inlined element is a drift vector — when a `_root/` rule changes, the template silently goes stale.
2. The Stage 1–5 work that authored `_root/00`–`_root/09` consolidated every rule into exactly one owning doc per the path-reference contract (`_root/CONTRACTS.md §5`). Stage 3 rebuilds the templates so every rule reference in every template is a §-pointer, never an inlined sentence.
3. A fresh agent — loaded with only `_root/` + the cleanup tracker + the archived templates — produces a template that mechanically respects the path-reference contract. The planning agent that designed `_root/` carries enough context that it would unconsciously paste in convenient verbatim text. The fresh agent will not.

---

## Wave sequence

| Sub-wave | Output | Independence | Run order |
|---|---|---|---|
| 3.1 | `format-a-notices/_brief-template.md` + `_delivery-email-template.md` | Independent of 3.2/3.3/3.4. Best run first — Format A is the simplest format (CS-led, passive close, 6 drivers) and the resulting pattern informs 3.2/3.3/3.4 review. | Prompt drafted 2026-05-26 — `stage_3_1__format-a__brief-and-delivery-templates.md`. **APPROVED 2026-05-26** with operator-stamped strict-placeholder revision (Section 3c effective-date sentence + Section 3l-continued graduated-rate string converted from inline to `[INSERT _root/XX §N.M ...]` placeholders). 5 new CL items filed (CL-018 through CL-022). See `_root/09_changelog.md` "Stage 3.1 review pass" entry. |
| 3.2 | `format-b-notices/_brief-template.md` + `_delivery-email-template.md` | Independent of 3.1/3.3/3.4. Parallelizable. | Prompt drafted 2026-05-26 in parallel with Stage 3.1 execution — `stage_3_2__format-b__brief-and-delivery-templates.md`. Delta-pass applied 2026-05-26 after Stage 3.1 approval (pattern-inheritance cross-references; strict-placeholder precedent; "unique to Format B" claim corrected; CL-022 reference). **APPROVED 2026-05-26** as authored — path-reference contract verified end-to-end (0 inlined rule prose); all 7 applicable CL items addressed; 9 Stage 3.1 conventions matched exactly. Three operator stamps applied in same review pass: (a) CL-012 source fix at `_root/05 §2.3.2 + §2.3.3` (URN→IUR marker amendment); (b) CL-016 source fix at `_root/05 §2.6.2 + §2.6.3` (templated `[IF secondary driver = included_user_reduction]` sub-block addition); (c) subject-line normalized to "your SuperCat pricing is changing" across all 4 format folders (Stage 3.1 Format A delivery email edited in lockstep). CL-023 filed (`_meta/stage3_cleanup.md`) for v6.2 TBI+URN secondary re-evaluation. See `_root/09_changelog.md` "Stage 3.2 review pass" entry. |
| 3.3 | `ceo-letter-notices/_brief-template.md` + `_delivery-email-template.md` | Independent of 3.1/3.2/3.4. Parallelizable. | Prompt drafted 2026-05-26 in parallel with Stage 3.2 (post Stage 3.1 approval) — `stage_3_3__ceo-letter__brief-and-delivery-templates.md`. Delta-pass applied 2026-05-26 after Stage 3.2 approval. **APPROVED 2026-05-26** as authored — path-reference contract verified end-to-end (0 inlined rule prose); all 7 applicable CL items addressed (CL-001 / CL-003 / CL-004 / CL-005 / CL-012 / CL-016 / CL-022); CL-012 + CL-016 source-fix verification confirmed by drafter (paste-as-written); 12 pattern-inheritance conventions matched from Stage 3.1 + 3.2; 8 legitimate CEO-Letter-specific extensions accepted (integrated lede with `_root/04 §4.4` CEO Letter variant; `_root/04 §4.13` CEO Letter sub-paragraph with call-commitment-moves-to-sentence-2; `_root/04 §4.7` first-person variant; `## I'll Call You` close heading; routing-block CEO-required fields; QB-086 specific-calendar-date constraint; QB-114 audit-only CEO call execution; delivery email Section 5 voice-calibration boundaries). **3-location date parity contract operator-stamped via template-level QB-086 + QB-NNN cross-check** (the specific calendar date carried in `_root/04 §4.12` close MUST match across the brief's Section 3o, the brief's Section 2 routing block, and the delivery email's Section 2 routing block — drift is a hard send blocker). **No new CL items filed** — first Stage 3.X wave to land without source amendments, CL filings, or template revisions. See `_root/09_changelog.md` "Stage 3.3 review pass" entry. |
| 3.4 | `good-news-notices/_brief-template.md` + `_delivery-email-template.md` | Independent of 3.1/3.2/3.3. Parallelizable. | Prompt authored 2026-05-26 by incoming planning agent in parallel with Stage 3.3 review approval — `stage_3_4__good-news__brief-and-delivery-templates.md` (391 lines). Inherits all 12 Stage 3.1/3.2/3.3 pattern conventions + strict-placeholder precedent + "pricing" subject convention (extended to "pricing is decreasing" for Good News positive framing per operator stamp). Two source fixes applied at `_root/04 §3.1` (Good News consolidated 2026 framing sentence) + `_root/04 §4.5` (Good News operations-unchanged variant) per operator stamps on five handoff-time open questions — see `_root/09_changelog.md` "Stage 3.4 prep" entry. **APPROVED 2026-05-26** as-authored — path-reference contract verified end-to-end (0 inlined rule prose); all 5 applicable CL items addressed (CL-001 / CL-003 / CL-004 / CL-005 / CL-022); 12 pattern-inheritance conventions matched from Stage 3.1 + 3.2 + 3.3; all Good-News-specific structural deviations accepted (NO formal-notice line per `_root/04 §4.12` Good News exception; 4-row mini summary table; CSM signature; `Expansion eligible` + `Watch health flag` Good-News-specific routing fields; Postgres line omitted per `_root/07 §7` footnote; brief title "Your Pricing Is Decreasing"; email subject "pricing is decreasing — effective [EFFECTIVE_DATE]"). Brief (240 lines) authored 2026-05-26 13:39 by prior session; delivery email (164 lines) authored 2026-05-26 13:51 by fresh-agent session that posted the conformance block (two-session authorship documented in changelog). **No new source amendments** — second Stage 3.X wave to land clean at the rule layer (Stage 3.3 was the first). **One protocol observation filed as CL-024**: fresh agent skipped manifest-echo + did not re-read `_root/00`–`_root/09` (relied on brief's pointer fidelity instead of verifying at source); planning agent verified pointers at source by re-reading `_root/04` directly; templates approved on substance; Stage 3.5 prompt strengthens manifest-echo language per CL-024. See `_root/09_changelog.md` "Stage 3.4 review pass" entry. |
| 3.5 | `entity-packets/_parent-letter-template.md` (303 lines) + `entity-packets/_parent-letter-delivery-email-template.md` (243 lines) | **NEW build** — heaviest of the five Stage 3 waves; no archived template precedent. Stage 3.5 prep landed extensive rule-layer scaffolding 2026-05-26: dual-canonical v6.2 architecture (`_master-entity-data-v6.2.csv` joins `_master-account-data-v6.2.csv` as canonical entity-level scope source — 14 entities total per Master Entity tab); `_root/04 §4.15` Parent-letter voice register authored at source (6 sub-sections: voice fork by `delivery_owner` with CEO-delivered + Kylor-delivered HoCS variants; multi-brand portfolio acknowledgment; cross-brand consolidation lens; per-brand mechanics restraint; default-only pricing posture; routing pointer to per-child notices); cross-format CSM-role note codified — SuperCat's CSM support role does NOT handle migration conversations, "CSM-sent" role-marker filled by Kylor in HoCS role across all 5 Stage 3 templates; `_root/06 §1.6` rewritten with canonical 14-entity scope (13 rollup + 1 standalone_multi_org; Ferguson Enterprises mixed-direction one-off exception documented; Stage 3.5 template scope = 13 entities [excludes Ferguson]); CL-014 RESOLVED at Stage 3.5 prep. Prompt drafted 2026-05-26 — `stage_3_5__entity-packets__parent-letter-and-delivery-email-templates.md` 655 lines. **APPROVED 2026-05-26** at Stage 3.5 review pass — templates approved as-authored with one source-fix amendment: Thesis `delivery_owner` reconciled rule-layer → CSV ground truth (Thesis moved from Kylor row to CEO row in `_root/04 §4.15.1` + `_root/06 §1.6` + Stage 3.5 prompt Step 2 table + both new templates' Section 1 entity-count references; CSV is canonical per `_root/06 §1.6` operator stamp). Post-fix canonical counts: 4 CEO-delivered + 10 Kylor-delivered (9 rollup + 1 standalone_multi_org Maxim); Stage 3.5 template scope 13 entities (Ferguson excluded). Path-reference contract verified end-to-end (0 inlined rule prose; every `_root/XX §N.M` reference is an `[INSERT ...]` pointer or section citation); voice-fork conditional rendering correct in both templates; cross-format CSM-role note enforced (HoCS title, not generic CSM); 48-hour two-stage sequencing referenced throughout; 3-location date parity contract enforced for CEO-delivered fork; per-brand mechanics restraint enforced (Section 3e CONSTRAINT block); default-only pricing posture enforced (consolidated_* INTERNAL-ONLY); 8 EP-NNN entity-packet-specific blockers in parent-letter Section 4 + 9 EP-NNN in delivery email Section 4 (inferred pending `_root/08` Wave 6 batch). **CL-024 RESOLVED 2026-05-26 at Stage 3.5 review pass** — the fresh agent's strict + paste-verification protocol produced its design value: surfaced the Thesis discrepancy that pointer-only reading would have missed (rule layer drifted from data; paste-verification protocol forced the verbatim source-reading that exposed the drift). Five items deferred to Stage 4 / Wave 6 (sentence-2 promotion; CL-005 roadmap promotion; 4-brand member-enumeration example; `_root/07 §7` entity-packet row; `_root/08` entity-packet QB additions). See `_root/09_changelog.md` "Stage 3.5 review pass" entry. |

**Total**: 5 fresh-agent sessions = the full Stage 3 template rebuild.

---

## Why prompts are drafted in waves rather than all at once

Each prompt depends on the same upstream (`_root/00`–`_root/09` + `_meta/stage3_cleanup.md`), so structurally the 5 prompts could be drafted up-front. Two reasons not to:

1. **Pattern inheritance.** Stage 3.1's output establishes the path-reference conventions (how the dispatch table references `_root/05`; how the conditional-flow markers reference `_root/04`; how the routing block references `_root/07 §7`). Stage 3.2/3.3/3.4 prompts are materially tighter when they can cite "match the pattern in `format-a-notices/_brief-template.md` §3f" rather than re-specifying the convention from scratch.
2. **Cleanup-tracker evolution.** Each Stage 3.X fresh-agent session may surface new `CL-NNN` items via the gaps list in its conformance block. Those items inform the next prompt's "address these cleanups" section. Pre-drafting all 5 prompts forfeits that learning.

This is the same discipline baked into Stage 2: don't pre-author against unknown shape; let the upstream output inform the downstream spec.

---

## The review protocol (mandatory between sub-waves)

For every Stage 3.X prompt the operator paste-runs:

1. **Operator pastes the prompt into a fresh Cursor agent session.**
2. **Fresh agent reads required files, authors the template files, posts a Conformance Block in chat per `_root/00_manifest.md §5`.**
3. **Operator pastes the Conformance Block AND the agent's final chat message back to the planning agent in the planning thread.**
4. **Planning agent reviews:**
   - Did the agent echo all required files with last-updated dates per `_root/00_manifest.md §6`?
   - Did the agent flag any conflicts, gaps, or new `CL-NNN` items?
   - Is the path-reference contract respected? (Verbatim rule-prose count should be 0.)
   - Does every required CL item have a corresponding template element?
   - Does the routing block match `_root/07 §7` exactly?
   - Does the driver dispatch table match `_root/05` exactly?
5. **Planning agent either approves (→ draft next sub-wave prompt) or requests revision (→ operator returns to the fresh agent with planning agent's feedback).**
6. **Approved templates trigger a `_root/09_changelog.md` Wave 6 (Stage 3) entry** authored by the planning agent. New cleanup items from gaps lists are filed in `_meta/stage3_cleanup.md`.

The operator does NOT run the next sub-wave prompt until the prior sub-wave's output has been approved and the next prompt has been drafted by the planning agent.

---

## What each prompt produces (and what it does NOT produce)

| Each Stage 3.X prompt produces | Each Stage 3.X prompt does NOT produce |
|---|---|
| 2 new template files (1 brief template + 1 delivery email template) | Per-account briefs (Stage 4 territory) |
| Path-reference scaffolding to existing `_root/` rules | New rules (rules are owned by `_root/`; any new rule needs `_root/CONTRACTS.md §3` rule-change protocol) |
| Conditional-flow markers that drafters apply at draft time | Pre-filled placeholders for any specific account |
| Driver dispatch tables citing `_root/05 §N.M` per `migration_driver` | Verbatim driver prose (driver prose stays in `_root/05`) |
| Routing-block scaffolding matching `_root/07 §7` per format | Verbatim "What You're Getting at $X" tier blocks (stay in `_root/03 §2`) |
| QA-checklist `>` blockquotes citing QB-NNN | Verbatim QB-NNN check text (checks stay in `_root/08`) |
| Cleanup-item resolution notes naming CL-NNN | Updates to `_meta/stage3_cleanup.md` (the planning agent files new items based on gaps surfaced) |

The brief template is the structural skeleton — placeholders + section headings + §-pointers + dispatch tables. The drafter at Stage 4 fills the placeholders from v6.2 + Postgres data and fetches the verbatim `_root/` blocks named by the §-pointers. The template carries the LOOKUP; the prose stays in its owning doc.

---

## Why each prompt is long

Each Stage 3 prompt averages 350–500 lines. This length is intentional. The cost of a long prompt is one paste; the cost of a short prompt that fails to specify a path-reference convention is a template that silently inlines a `_root/` sentence, which silently drifts the next time the rule is edited. Prompt length is the operator's leverage over the fresh agent — every constraint stated in the prompt is a constraint enforced in the output.

Common elements of every Stage 3 prompt:

- **Step 1**: Required reading (all 10 `_root/` docs + cleanup tracker + 3–4 specific archive references with explicit per-prompt anti-archive override authorization).
- **Step 2**: Authoritative format scope (driver coverage in/out, voice-rule applicability, routing scope) — stated as fact, not re-derived.
- **Step 3**: Brief template section spec (every section either contains pure scaffolding OR a §-pointer; NO rule prose is inlined).
- **Step 4**: Delivery email template section spec.
- **Step 5**: Anti-drift discipline (the path-reference contract is absolute; specific CL items called out by ID).
- **Step 6**: Voice and format constraints for the template's own scaffolding text.
- **Step 7**: Output (create files + post Conformance Block).
- **Step 8**: If something is missing or contradictory (flag in conformance block, never invent).

The Conformance Block is the operator's single audit artifact. It enumerates files read, sections authored, drivers covered, CL items addressed, path-reference verification counts, scaffolding content carried, gaps surfaced, conflicts resolved, and open questions.

---

## Anti-archive override (explicit per-prompt authorization)

Every Stage 3 prompt explicitly authorizes the fresh agent to read specific files inside `_archive/2026-05-22__pre-refactor/<format-folder>/` plus the relevant `Migration-Health Artifacts/02_briefs/templates/` files. This is a **per-prompt override** of the general anti-archive rule established in `_root/CONTRACTS.md §4`.

The override is legitimate because:

- The prompt names the specific archive files to read (no scope creep).
- The reading purpose is **structural extraction** (operator-notes header style, routing-block field layout, section ordering, conditional-flow markers) — NOT inline-prose extraction. Inline prose from archived templates is exactly the drift the rebuild eliminates; lifting it would defeat the purpose.
- The exemplar briefs (kal v2, etc.) are read for calibration of what a completed brief looks like — NOT as template sources.

After Stage 3.X is reviewed and approved, the new template is the canonical scaffolding; the archived template is once again strictly OFF-LIMITS to all Stage 4 drafters.

This is the **only** legitimate pattern for reading the archive during Stage 3. Any other archive read is a violation of the agent contract.

---

## What happens after Stage 3

Once all 5 format folders are rebuilt and approved:

- **Stage 4**: New per-format fresh-agent drafting prompts (one per format folder) are authored. Each prompt directs a Stage-4 drafter to (a) consult the rebuilt template, (b) pull v6.2 + Postgres data for ONE account, (c) fetch named verbatim blocks from `_root/03`/`_root/04`/`_root/05`, and (d) produce a per-account brief + delivery email + conformance block. These replace the archived `_fresh-agent-prompt.md` files in each format folder.
- **Stage 5**: First per-account drafts are produced from the new system. The first 1–2 drafts per format are reviewed especially carefully — they are the proof that the rebuilt template + the rule layer produce drift-free output.
- **Stage 6+**: Cohort execution (June, July, deferred) per the schedule in `_reference/2026-05-20__execution_plan_v3.3.md` §IV.

The 5 prompts in this folder are the bridge from the rule layer (`_root/`) to production drafting (Stage 4+). They warrant the care they're being given.
