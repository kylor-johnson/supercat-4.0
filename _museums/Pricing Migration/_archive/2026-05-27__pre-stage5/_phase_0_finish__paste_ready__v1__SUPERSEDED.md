# Phase 0 Finisher — Paste-ready prompt

> **For paste into a fresh Cursor agent chat (Agent mode) as the first message.** Do not modify before pasting.
> **Authored**: 2026-05-27 by Stage 4 chat (outgoing) — Path B fallback after mode-flip blocked the Write tool in the originating chat.
> **Workspace root**: `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/`
> **Scope**: Finish Stage 5 Phase 0 ONLY — author the handoff doc + log the changelog entry + STOP. Do NOT start Phase 1. Do NOT author any rule-doc content. You are a mechanical finisher operating against a fully-specified spec.

---

## You are the Stage 5 Phase 0 finisher

Phase 0 was started by the prior chat at 2026-05-27 and is partially complete on disk:

- ✅ `_archive/2026-05-27__pre-stage5/` snapshot landed (all pre-rebuild files copied per `_root/CONTRACTS.md §4` explicit-extraction discipline)
- ✅ `_archive/2026-05-27__pre-stage5/DO_NOT_READ.md` written
- ✅ `_meta/stage5_prompts/` directory created (this prompt is the only file in it currently, plus you'll add the handoff)
- ❌ `_meta/stage5_prompts/STAGE_5_PLANNING_AGENT_HANDOFF.md` — your job to author
- ❌ `_root/09_changelog.md` Phase 0 entry — your job to append

**Two files to write, then STOP.** Do not begin Phase 1 (that requires a separate fresh chat against the handoff you author). Do not author `_root/01.5`, `_root/03.5`, `_root/03.6`, or `_root/04.5` (those are Phase 1 deliverables). Do not edit `_root/03`, `_root/04`, `_root/05`, or `_root/06` (those are Phase 3+ deliverables).

---

## Required reading (in this order; manifest-echo contract per `_root/00_manifest.md §6`)

Echo every doc's last-updated date in your first response.

1. `AGENTS.md`
2. `_root/00_manifest.md` — §2 manifest table (echo every row), §5 conformance block format, §6 manifest-echo contract
3. `_root/CONTRACTS.md` — particularly §3 rule-change protocol (your changelog entry follows this), §4 anti-archive rule (the snapshot is sealed; do not read snapshot contents), §5 path-reference contract (the handoff doc references `_root/02 §1` by pointer; does NOT restate the segment table)
4. `_root/02_who_is_being_migrated.md` — read §1 segment table (lines 13–28) carefully; this is the operator-stamped input contract Stage 5 consumes. The handoff doc references it; do NOT restate
5. `_root/09_changelog.md` — read the most recent ~5 entries to inherit the changelog entry voice + structure
6. `_archive/2026-05-27__pre-stage5/DO_NOT_READ.md` — read ONLY this file in the snapshot; it has the snapshot manifest you'll reference in the handoff. Per `_root/CONTRACTS.md §4` do NOT read any other file in the snapshot folder
7. `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` — first 40 lines only (front matter + amendment blocks); inherit the handoff-doc structural pattern + voice
8. `_meta/stage4_prompts/README.md` — first 100 lines for the wave-sequence + production-proof-gate pattern you reference in the handoff
9. This prompt — re-read §"Spec for the handoff doc" + §"Spec for the changelog entry" below carefully before authoring

### Do NOT read

- Any file in `_archive/2026-05-27__pre-stage5/` other than `DO_NOT_READ.md` (anti-archive rule)
- Any file in `_archive/2026-05-22__pre-refactor/` or `_archive/2026-05-26__pre-cl-026/` (anti-archive rule)
- `_root/03_what_we_sell.md`, `_root/04_communication_posture.md`, `_root/05_driver_taxonomy.md`, `_root/06_format_routing.md` (rewrite targets in Phase 3 + Phase 2; reading biases your handoff toward inheritance)
- `_root/08_quality_bar.md` (rekey target Phase 6; not needed for handoff authoring)
- `_meta/stage3_cleanup.md` (full content not needed; you reference the file by path in the handoff)
- `_meta/stage4_account_ledger.md` (not needed)
- Per-account briefs/emails (not needed)
- `_reference/**`, `Migration-Health Artifacts/`, `_meta/stage2_prompts/`, `_meta/stage3_prompts/` (out of scope)

---

## Operator-stamped inputs (paste verbatim into the handoff doc; do NOT paraphrase)

These three inputs were operator-stamped via chat 2026-05-27 with the prior Stage 4 chat. The handoff doc captures them VERBATIM as `§2.2`, `§2.3`, and `§2.4`. The operator's stamp is the source of truth; no editorial commentary inside the verbatim blocks.

### Input 1 — The playbook table (handoff §2.2)

The operator shared this table 2026-05-27 as the intended Stage 4 output target. Capture verbatim under handoff §2.2. The Strategic / Tailwind / Annual rows + Executive / Pre-Engagement rows are unfilled by the operator and are flagged TBD — surface to operator via `AskQuestion` in Phase 1 (NOT in Phase 0).

| Playbook | Cohort / Timing | Notice / Artifact | Meeting / Inbound Handling | Follow-Up / Escalation | Framing | Artifact Composition | Pilot / Feedback Loop | Mixed-Segment Handling | Delivery Model | Pre-Authorized Concessions | Concessions Requiring CEO Approval | Owner | Duration |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Core** | June cohort — digital-first, Kylor-owned, sends in June Weeks 2–4 in parallel with Narrative | Standard Migration Notice + simplified value summary — no full bespoke artifact | Kylor available for inbound — no proactive call scheduling | Non-response follow-up: Day 7 for Healthy accounts or Day 10 for Thriving accounts — health-driven escalation sensitivity | Honest framing: lead with dollar amount and effective date, then mechanic. Not percentage. Not relationship preamble. | — | — | — | Kylor-owned | User cleanup, billing date adjustment, annual prepay | — | Kylor | 60–75 days |
| **Narrative** | June cohort — digital-first, Kylor-owned, sends in June Weeks 2–4 in parallel with Core | Simplified value summary + Value Migration Notice — not a full bespoke artifact; delta $201–$400 | No default meeting scheduled — Kylor available for inbound | — | Honest framing for `discount_correction` where delta is greater than $300/month: direct acknowledgment — *"You negotiated a discount at signing. We're retiring all legacy arrangements simultaneously. You are not being singled out."* | Two-axis artifact composition: content driven by `migration_driver` × `health_profile` | — | — | Kylor-owned | User cleanup, 30-day transition credit, annual prepay | Permanent discount, transition credit greater than 30 days, any discount greater than 10% of target | Kylor | 60–90 days |
| **Entity** | June cohort — entity packets sent first, Weeks 1–2; meeting proposed after packet delivery | Entity packet is the notice — entity-level impact framing, underpinned by per-brand account detail | Meeting proposed after packet delivery | — | Lead with multi-brand consolidation lever — 90%-of-natural-tier brand fee positioned as partnership benefit | — | Entity conversations are the pilot — feedback refines artifacts for July cohort, including Executive + Pre-Engagement | Mixed-segment entities, such as Godinger and Samson: packet covers all children, including Strategic-routed ones, maintaining entity consistency | CEO delivers complex entities, such as Gabriella White, Visual Comfort, Godinger, etc.; Kylor delivers simpler entities, such as Abaline, Hearthstone, etc. | Multi-brand consolidation, user cleanup, 30-day transition credit | Entity-level concessions only — no brand-by-brand improvisation without CEO approval | CEO for complex entities + Kylor for simpler entities | — |
| **Executive** | TBD (per `_root/02 §1` line 24: July cohort) | TBD (per `_root/02 §1` line 24: full bespoke artifact + CEO exec letter) | TBD | TBD | TBD | TBD | TBD | TBD | TBD (per `_root/02 §1` line 24: Kylor + CEO co-authored) | TBD | TBD | TBD | TBD |
| **Pre-Engagement** | TBD (per `_root/02 §1` line 25: July cohort) | TBD (per `_root/02 §1` line 25: full bespoke artifact + CEO-initiated call before notice) | TBD | TBD | TBD | TBD | Inherits feedback from Entity pilot (per `_root/02 §1` line 26 stamp) | TBD | TBD (per `_root/02 §1` line 25: CEO + CS) | TBD | TBD | TBD | TBD |
| **Strategic** | TBD (per `_root/02 §1` line 27: Deferred / post-migration) | TBD (per `_root/02 §1` line 27: CEO-led conversation precedes notice; walk-away thresholds pre-authorized) | TBD | TBD | TBD | TBD | TBD | TBD | TBD (per `_root/02 §1` line 27: CEO) | TBD | TBD | TBD | TBD |
| **Tailwind** | TBD (per `_root/02 §1` line 21: Deferred) | TBD (per `_root/02 §1` line 21: Good News Notice is the entire comm) | TBD | TBD | TBD | TBD | TBD | TBD | TBD (per `_root/02 §1` line 21: Kylor / CS) | TBD | TBD | TBD | TBD |
| **Annual** | TBD (per `_root/02 §1` line 28: Renewal-driven; ≥90-day notice) | TBD (per `_root/02 §1` line 28: substance matches natural segment; renewal-timed wrapper) | TBD | TBD | TBD | TBD | TBD | TBD | TBD (per `_root/02 §1` line 28: Kylor + CEO) | TBD | TBD | TBD | TBD |

### Input 2 — Operator concerns (handoff §2.3, verbatim from chat 2026-05-27)

1. "Objective of the notice / balancing substance contained in the notice vs attached artifact — (rationale) SuperCat has transitioned to platform…standardized pricing across customers"
2. "Articulating the platform vs product menu"

Plus 3 deliverables (verbatim from chat, captured under handoff §2.4):

1. Establish general communication and posture standards and guidelines
2. Further define communication variants so it's clear what substance is contained where: simplified migration notice vs [full artifact]
3. Translate standards and guidelines into templates

### Input 3 — Notice Template Family + Companion Materials (handoff §2.5)

The operator shared this two-table block 2026-05-27 as the canonical artifact taxonomy. Capture verbatim under handoff §2.5. This is the most-detailed operator-stamped input and the highest-leverage refinement to the Phase 1 + Phase 3 + Phase 4 scope.

#### Notice Template Family

The **notice** is the formal written document satisfying the 60-day contractual requirement. It is distinct from — and delivered alongside — the value artifact, exec letter, or entity packet. The notice triggers the legal clock; the supporting materials carry the substance.

| Template | Segment | What It Contains | What It Does NOT Contain |
|---|---|---|---|
| Good News Notice | Tailwind (6 accts) | "Your price is decreasing from $X to $Y, effective [DATE]." One sentence of mechanic. What doesn't change. Done. | No upsell. No expansion ask. No relationship preamble. |
| Standard Migration Notice | Core (13 accts, ≤$200 delta) | New tier name + pricing. What's included (features, users). User model. Effective date. Simplified value summary attached. Kylor's contact for questions. | No full bespoke artifact. No percentage framing. No apology. |
| Value Migration Notice | Narrative (15 accts, $201–$400) + Executive (8 accts, $401–$600) + Pre-Engagement (8 accts, >$600) | New tier + pricing. References the value artifact (linked). Install-base normalization framing. Effective date. | The artifact carries the substance — the notice is the formal/legal vehicle. |
| Entity Migration Packet | All entities (~17 packets → 27 child accts) | Entity-level impact summary. Per-brand pricing detail. Consolidated multi-brand option. Entity health profile. Satisfies 60-day notice for all child brands simultaneously. | Not an account-by-account notice. Entity-level framing throughout. |
| Strategic Migration Notice | Strategic (19 accts) | Sent AFTER CEO conversation. References the discussion. Confirms agreed terms or standard pricing. Effective date. | Not a first-touch document. Addressed post-migration. |
| Annual Renewal Notice | Annual (11 accts) | New tier + pricing effective at next renewal date. Renewal-specific framing. Sent ≥90 days before renewal. Matches natural segment substance. | Not tied to monthly migration timing. |

#### Companion materials (separate from the notice)

| Material | Applies To | Relationship to Notice |
|---|---|---|
| Full value artifact (bespoke HTML) | Executive ($401–$600 delta) + Pre-Engagement (>$600 delta) | Delivered with or ahead of notice. The substance layer. |
| Simplified value summary (parameterized 1-page) | Core (≤$200) + Narrative ($201–$400) | Attached to notice. Key data points from v6 table + health. |
| CEO exec letter | Executive ($401–$600 delta) | Delivered alongside notice. CEO co-authored — signals executive awareness and ownership. |
| CEO-initiated call | Pre-Engagement (>$600 delta) | CEO initiates before any notice is sent. Full conversation before formal notice. |

---

## Spec for the handoff doc (`_meta/stage5_prompts/STAGE_5_PLANNING_AGENT_HANDOFF.md`)

The handoff doc is the **operator-stamped charter** for Stage 5. Every fresh agent spawned in Phases 1–5 reads it. Pattern-inherits from `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` for structural form (front matter + numbered sections + Required Reading + First-Action Sequence + Conformance Block); content is Stage-5-specific.

### Required structure (11 sections; ~800–1,000 lines)

**Front matter** — `For paste into a fresh Cursor agent chat as the first message.` + `Drafted: 2026-05-27 by Stage 4 chat (outgoing) at operator direction (Phase 0 execution; Path B finish via fresh agent due to mode-flip in originating chat).` + `Workspace root` + `Owner: CEO` + `Supersedes (operationally, prose-and-mapping layer only): _meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md and the 4-format architecture it operates over.`

**§1 — Why Stage 5 exists** (~120 lines)
- §1.1 What the operator observed (the cci/sca artifact-identical-to-archive observation; CEO review 2026-05-26)
- §1.2 Why this happened structurally (paste-quote the `_root/04` line 9 "Primary sources" front matter showing archive citation; paste-quote `_root/05` line 9 same; explain the path-reference contract + verbatim-paste discipline mechanically guaranteed archive-prose propagation)
- §1.3 What was supposed to come out instead (8 playbooks per `_root/02 §1`; 6 notices + 4 companion materials per operator's Input 3 table; substance distributed across notice vs companion; platform-vs-product-menu positioning; concessions framework; per-playbook cadence; pilot-then-scale model)
- §1.4 The operator's two concerns (verbatim from Input 2)

**§2 — Operator-stamped sources of truth** (~250 lines)
- §2.1 Already-stamped at `_root/02 §1` (operator 2026-05-22) — paste-quote lines 13–28 segment table verbatim; mark as "input contract; do NOT edit in Stage 5"
- §2.2 Playbook table (Input 1 above, verbatim)
- §2.3 Operator concerns (Input 2 above, verbatim)
- §2.4 Operator deliverables (3 items from Input 2 follow-up, verbatim)
- §2.5 Notice Template Family + Companion Materials (Input 3 above, verbatim — both tables)
- §2.6 Synthesis: the legal-clock-vs-substance-carrier rule (one paragraph stating that per Input 3, the notice triggers the legal 60-day clock; companion materials carry the substance; this split governs every artifact-taxonomy decision in `_root/03.5`). Do NOT inject editorial opinion; state the rule as derivable from Input 3 verbatim language

**§3 — The cut-line: stays vs rewrites vs new** (~80 lines, table-heavy)
- §3.1 STAYS (table): `AGENTS.md`, `_root/00`, `_root/CONTRACTS.md`, `_root/01`, `_root/02` (especially §1 segment table — sealed), `_root/07`, `_root/08` skeleton, `_root/09`, `_meta/v6_2_reconciliation_log.md`, v6.2 CSV, routing CSV, `_reference/**`, the 6-step routing flow in `_root/06 §2`, the Stage 4 8-step drafter skeleton, `entity-packets/` (refined not rebuilt — closest alignment to Entity playbook per §2.5 Input 3)
- §3.2 REWRITES (table): `_root/03 §1` tier blocks → Phase 3a per `_root/03.6`; `_root/03 §3` roadmap → Phase 3a per `_root/03.6` (may relocate per substance budget); `_root/04 §3` consolidated 2026 sentence → Phase 3a; `_root/04 §3` forbidden-phrase table → Phase 3a (refresh); `_root/04 §4.5` ops-unchanged variants → Phase 3b (playbook-specific); `_root/04 §4.12` close variants → Phase 3b (8 playbook-specific closes); `_root/05 §2.X` driver prose → Phase 3c (recut into **notice form-cut** + **simplified-companion form-cut** + **full-companion form-cut** per Input 3 notice-vs-companion split; NOT the prior "short/mid/long" framing); `_root/06_format_routing.md` → Phase 2 (replaced by `_root/06_playbook_routing.md` with 8-playbook dispatch); `_root/08` format-keyed QB checks → Phase 6 rekey; template folders → Phase 4 (playbook-keyed); Stage 4 drafter prompts → Phase 5 (Stage 5 family)
- §3.3 NEW (table): `_root/01.5_playbook_architecture.md` (Phase 1; 8 playbooks; pulls segment defs by reference from `_root/02 §1`); `_root/03.5_artifact_taxonomy.md` (Phase 1; the 6-notice + 4-companion taxonomy per §2.5 Input 3; substance budget per artifact; notice-vs-companion legal-clock-vs-substance split rule; delivery semantics per companion: attached / alongside / ahead of / before); `_root/03.6_platform_narrative.md` (Phase 1; platform-vs-product-menu source-of-truth sentences); `_root/04.5_concessions.md` (Phase 1; pre-authorized + CEO-required matrix per playbook; pulls from §2.2 playbook table by reference); `_meta/stage5_cleanup.md` (Phase 1; CL-NNN tracker init); playbook-keyed template folders (Phase 4: `core/`, `narrative/`, `executive/`, `pre-engagement/`, `tailwind/`, `strategic/`, `annual/` — `entity-packets/` stays); `_meta/stage5_prompts/` family (per-phase paste-ready prompts)

**§4 — The 8-phase sequence** (~250 lines)

For EACH phase (0–8), state: Owner, Output, Reading scope, Gate, Drift control, Duration. Use the structure below as the template; expand to full detail per phase.

- **Phase 0 — Snapshot + handoff (COMPLETE 2026-05-27)** — Owner: Stage 4 chat (outgoing) + this fresh-agent finisher. Output: snapshot + DO_NOT_READ + this handoff + changelog entry. Gate: operator stamps handoff. Status: COMPLETE
- **Phase 1 — Taxonomy docs** — Owner: fresh Agent A. Output: 4 new docs + cleanup tracker init. Reading scope: `AGENTS.md` + `_root/00` + `_root/CONTRACTS.md` + `_root/01` + `_root/02` + this handoff + (NOT `_root/03`/`04`/`05`/`06`, NOT `_archive/**`, NOT `format-*-notices/**`). First action: surface 5 questions to operator via `AskQuestion` (see §8.1). Gate: operator stamps each of 4 docs individually. Duration: ~1 day
- **Phase 2 — Dispatch rewrite** — Owner: fresh Agent B. Output: new `_root/06_playbook_routing.md` (8-playbook dispatch; 6-step flow + 3 overrides + `comm_action` vocabulary preserved). Gate: operator stamps. Duration: half day
- **Phase 3a — Platform anchor prose** — Owner: fresh Agent C. Output: `_root/04 §3` + `_root/03 §1` + `_root/03 §3` rewrites per `_root/03.6`. Gate: per-section operator stamp. Duration: 1 day
- **Phase 3b — Close + ops-unchanged variants** — Owner: fresh Agent D. Output: `_root/04 §4.12` 8 playbook closes + `_root/04 §4.5` playbook variants. Gate: per-variant operator stamp. Duration: half day
- **Phase 3c — Driver block recuts** — Owner: fresh Agent E, **one fresh chat per driver** (8 sub-sessions for the 8 increase-side drivers). Output: each `_root/05 §2.X` recut into 3 form-cuts (notice / simplified-companion / full-companion) per §2.5 Input 3. Sequenced URN (38 accts) → PDC (17) → TBI (13) → IUR (10) → ABTS (9) → MOR (6) → ADR (2) → SA (1). Gate: per-driver operator stamp before next driver begins. Duration: ~1 day total. Drift control: force fresh-per-driver per §6 invariant
- **Phase 4 — Templates per playbook** — Owner: one fresh agent per playbook (F1–F6 sequential; F7–F8 deferred to post-pilot). Output: per-playbook template families — Core (Standard Migration Notice + Simplified Value Summary + delivery email); Narrative (Value Migration Notice + Simplified Value Summary + delivery email); Executive (Value Migration Notice + Full Value Artifact + CEO Exec Letter + delivery email); Pre-Engagement (Value Migration Notice + Full Value Artifact + CEO Call Prep Doc + delivery email; CEO call IS pre-notice per §2.5 Input 3); Entity (refine `entity-packets/` per Entity Migration Packet spec); Tailwind (Good News Notice + delivery email). ~16 templates total grouped into 6 per-playbook sessions. Gate: per-playbook operator stamp. Duration: 3 days
- **Phase 5 — Stage 5 drafter prompts per playbook** — Owner: fresh G1–G6 sequential. Output: `_meta/stage5_prompts/stage_5_X__[playbook]__per-account-drafter.md` family; pattern-inherits Stage 4 8-step skeleton; per-playbook bodies in Steps 1/3/5/6/7. Per-playbook prompt authors notice + companion + delivery email in one fresh-agent session per account. Gate: per-playbook operator stamp. Duration: 3 days
- **Phase 6 — Atomic cutover** — Owner: planning agent OR mechanical agent. Mechanics: archive pre-rebuild files to `_archive/<date>__stage5-cutover/`; rename new docs; manifest + changelog sweep; `_root/08` rekey. Gate: operator stamps plan; cutover is atomic. Duration: ~1 hour
- **Phase 7 — Pilot per playbook** — Owner: fresh per-account drafter per pilot. Sequence: Core → Narrative → Entity → Executive → Pre-Engagement (Tailwind/Annual/Strategic defer). Each pilot permitted to STOP per `_root/CONTRACTS.md §2` if source-fix issue surfaces (precedent: Stage 4.2 cci/bri/sca → CL-026/CL-027/CL-028). Gate: per-pilot operator stamp. Duration: half day per pilot
- **Phase 8 — Batch June cohort** — Owner: per-account fresh drafters. Sequence: Core (13) + Narrative (15) + Entity (27) = 55 accounts. Gate: per-account operator review per existing Stage 4 protocol. Duration: operator capacity-limited

State total time-to-first-correct-output: 3–4 days tight stamping, 5–7 days async, June cohort send (before July 1) achievable on either.

**§5 — Agent assignment matrix** (~30 lines, table)

The matrix mapping phases to agent types (fresh per phase except mechanical Phase 6); rationale per row (continuity vs context contamination). Restate the principle: "every authoring step runs in a fresh chat against operator-stamped context."

**§6 — Anti-drift discipline (7 invariants)** (~60 lines)

The 7 rules every Stage 5 agent honors:
1. No cross-phase chat continuation (except Phase 6 mechanical)
2. No skipping taxonomy docs to go straight to prose
3. No multi-driver authoring in one Phase 3c session (force fresh-per-driver)
4. No parallel pilots before first playbook is frozen
5. Do not touch `_root/02 §1` (sealed input contract)
6. No `_archive/**` reads during authoring (Phase 0 snapshot is rollback-only)
7. No skipping manifest table + changelog updates per `_root/CONTRACTS.md §3` 5-step protocol

**§7 — Required reading for Stage 5 planning agent (Agent A — Phase 1)** (~50 lines)

The 16-item reading list:
1. `AGENTS.md`
2. `_root/00_manifest.md`
3. `_root/CONTRACTS.md`
4. `_root/01_why_we_are_migrating.md`
5. `_root/02_who_is_being_migrated.md` (input contract; do NOT edit)
6. `_root/07_data_pipeline.md` (stays through Stage 5; awareness)
7. `_root/08_quality_bar.md` (skeleton stays; structural awareness)
8. `_root/09_changelog.md` (read every entry)
9. `_meta/stage5_prompts/STAGE_5_PLANNING_AGENT_HANDOFF.md` (this handoff)
10. `_archive/2026-05-27__pre-stage5/DO_NOT_READ.md` (snapshot manifest awareness only)
11. `_meta/stage4_prompts/README.md` (pattern reference)
12. `_meta/stage4_prompts/stage_4_1__format-a__per-account-drafter.md` (8-step skeleton pattern; structural only)
13. `_meta/stage4_account_ledger.md` (pattern reference; you continue appending Phase 7/8)
14. `_master-account-data-v6.2.csv` (verify presence; header row only in Phase 1)
15. `_master-entity-data-v6.2.csv` (verify presence)
16. `migration_comm_tiers_2026-05-19.csv` (verify presence)

Plus Do-NOT-Read list during Phase 1: `_root/03`, `_root/04`, `_root/05`, `_root/06`, `format-*-notices/**`, `_archive/**` other than item 10, `_meta/stage2_prompts/`, `_meta/stage3_prompts/`, `_reference/**`, `Migration-Health Artifacts/`

**§8 — Phase 1 detailed scope** (~100 lines)

Authoring order (after operator stamps the 5 questions in §8.1 below):

1. `_root/01.5_playbook_architecture.md` — owns the 8 playbooks. References `_root/02 §1` by pointer; does NOT restate segments. Owns: per-playbook cohort/timing, notice/artifact (by reference to `_root/03.5`), meeting handling, follow-up cadence, framing, artifact composition, pilot/feedback loop, mixed-segment handling, delivery model, concessions (by reference to `_root/04.5`), owner, duration. CL-NNN tracker entry
2. `_root/03.5_artifact_taxonomy.md` — owns the 6 notices + 4 companion materials (§2.5 Input 3 verbatim as the canonical tables); substance budget per artifact (operator-stamped per Question 2a–c); notice-vs-companion legal-clock-vs-substance split rule (§2.6 verbatim); delivery semantics (attached / alongside / ahead of / before). CL-NNN entry
3. `_root/03.6_platform_narrative.md` — owns the platform-vs-product-menu source-of-truth sentences (operator-stamped per Question 3); tier-narrative structural pattern; roadmap relocation decision. CL-NNN entry. Note: may fold into `_root/03` at Phase 3a if operator prefers — surface decision at landing
4. `_root/04.5_concessions.md` — owns the pre-authorized + CEO-required matrix per playbook (operator-stamped per Question 4). CL-NNN entry
5. `_meta/stage5_cleanup.md` initialized

§8.1 — Pre-authoring questions to surface to operator via `AskQuestion`:

- **Question 1** — Fill the 5 TBD playbook rows (Executive, Pre-Engagement, Strategic, Tailwind, Annual) per §2.2 columns. Serialize one playbook at a time if needed
- **Question 2a** — Substance budget per notice template (6 notices in §2.5): target word count + sections allowed per notice
- **Question 2b** — Substance budget per companion material (3 written companions: Full value artifact, Simplified value summary, CEO exec letter): target word count + sections allowed
- **Question 2c** — Confirm delivery semantics per companion verbatim from §2.5 ("Delivered with or ahead of notice" / "Attached to notice" / "Delivered alongside notice" / "CEO initiates before any notice is sent")
- **Question 3** — Platform-vs-product-menu canonical positioning sentence (the operator stated rationale "SuperCat has transitioned to platform…standardized pricing across customers" — confirm verbatim form or amend); tier-narrative structural pattern; roadmap relocation decision (does roadmap stay in Core/Narrative artifacts at all, or only Executive/Pre-Engagement full value artifact?)
- **Question 4** — Concessions matrix for the 5 unfilled playbooks (Executive, Pre-Engagement, Strategic, Tailwind, Annual): pre-authorized + CEO-required per playbook; confirm canonical concession list completeness (existing list: user cleanup, billing date adjustment, annual prepay, 30-day transition credit, multi-brand consolidation)
- **Question 5** — Timing rules confirmation: Strategic notice post-CEO-conversation (per §2.5); Pre-Engagement CEO call before notice (per §2.5); Entity packet legal coverage for all children simultaneously (per §2.5); Annual ≥90-day pre-renewal (per `_root/02 §5`). Operator confirms operational binding form of each

Phase 1 stop condition: 4 docs land + manifest + changelog + cleanup tracker; operator stamps full Phase 1 output; surface to operator: ready for Phase 2 (fresh chat).

**§9 — Phase 2–8 paste-ready prompt skeletons** (~30 lines)

State that you (the Stage 5 planning agent) author per-phase paste-ready prompts at each phase boundary; provide the skeleton structure (role + required reading + operator-stamped inputs + what-to-author + anti-drift cite + conformance block). Pattern inherits from `_meta/stage4_prompts/_paste-ready/stage_4_1__lpf.md`.

**§10 — First-action sequence for Stage 5 planning agent (Agent A — first chat response)** (~80 lines)

The script for Agent A's first message:
1. Manifest echo (paste-quote `_root/00 §2` every row, verified at source per CL-024)
2. Required-reading completeness echo (16 items with verified dates)
3. State snapshot verification (this snapshot folder exists; this handoff exists; Phase 1 docs do NOT yet exist; `_root/02 §1` paste-quote)
4. Conformance block per `_root/00 §5` + Stage 5 additions (template provided)
5. Wait for operator signal before authoring; surface Question 1 first via `AskQuestion`

**§11 — Cross-references**

Path references to: `_root/00_manifest.md`, `_root/CONTRACTS.md §3/§4/§5`, `_root/02_who_is_being_migrated.md §1`, `_root/09_changelog.md`, `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md`, `_meta/stage4_prompts/README.md`, `_meta/stage4_prompts/stage_4_1__format-a__per-account-drafter.md`, `_archive/2026-05-27__pre-stage5/DO_NOT_READ.md`.

---

## Spec for the changelog entry (`_root/09_changelog.md`)

Append a new entry to the bottom of `_root/09_changelog.md`. Format follows the established `_root/09 §Format` block:

```
### 2026-05-27 — Stage 5 Phase 0 — Snapshot + Planning Agent Handoff authored (playbook-architecture refactor initiated)
- **Doc(s) changed**: No `_root/` doc edits this entry (Phase 0 is meta-layer only — snapshot + handoff). Files added: `_archive/2026-05-27__pre-stage5/` snapshot (5 `_root/` doc copies + 5 folder snapshots + 2 cleanup-tracker copies + DO_NOT_READ.md marker); `_meta/stage5_prompts/STAGE_5_PLANNING_AGENT_HANDOFF.md` (the Stage 5 charter); `_meta/stage5_prompts/_phase_0_finish__paste_ready.md` (Path B finisher prompt; this is the paste-ready you ran).
- **What changed**: (a) Operator (CEO) reviewed 2026-05-26 Stage 4.2 `cci` (Currey & Company) production artifact and identified that the new artifact is structurally identical to the 2026-05-19 archived pre-refactor artifact — material differences limited to effective date + lede paraphrase + one additive "What's Coming in 2026" section. Root cause: `_root/04` line 9 + `_root/05` line 9 cite the archived templates + per-account exemplars as Primary sources; path-reference contract enforces verbatim paste of that prose; output was structurally guaranteed to look like archive. (b) Operator stamped 8-playbook architecture as the intended Stage 4 output target — segments already correctly stamped at `_root/02 §1` (operator 2026-05-22); breakdown is at the dispatch + prose layer downstream. (c) Operator shared 3 inputs as canonical Stage 5 sources of truth: the playbook table (8 playbooks × 14 columns; 3 rows filled, 5 TBD); the 2 concerns (substance split + platform-vs-product menu); the Notice Template Family + Companion Materials taxonomy (6 notices + 4 companions; legal-clock-vs-substance split rule). (d) Stage 5 charter authored at `_meta/stage5_prompts/STAGE_5_PLANNING_AGENT_HANDOFF.md` with 8-phase sequence (taxonomy → dispatch → source prose → templates → drafter prompts → cutover → pilot → batch); fresh-per-agent discipline; 7 anti-drift invariants; pilot-then-scale cadence into June cohort.
- **Why**: The 2026-05-22 → 2026-05-26 rebuild reorganized the assembly machinery (manifest-echo, path-reference contract, 138 QB checks, reconciliation discipline) correctly but preserved the wrong prose. The drift-prevention machinery worked exactly as designed; it was designed to preserve the wrong thing. Stage 5 rebuilds the prose-and-mapping layer (`_root/03` + `_root/04` + `_root/05` + `_root/06` + format folders + Stage 4 drafter prompts) against operator-stamped 8-playbook + 6-notice + 4-companion architecture; preserves the infrastructure layer (`AGENTS.md`, `_root/00`, `_root/CONTRACTS.md`, `_root/01`, `_root/02`, `_root/07`, `_root/08` skeleton, `_root/09`, data files, reconciliation log).
- **Affected downstream**: (a) Phase 1 (next phase) authors 4 new docs: `_root/01.5_playbook_architecture.md` + `_root/03.5_artifact_taxonomy.md` + `_root/03.6_platform_narrative.md` + `_root/04.5_concessions.md` + initialize `_meta/stage5_cleanup.md`. (b) Phases 2–8 sequenced per handoff §4. (c) `_archive/2026-05-27__pre-stage5/` snapshot is sealed per `_root/CONTRACTS.md §4` anti-archive rule; no agent reads contents during Stage 5 authoring (rollback-only). (d) Pre-rebuild artifacts (`_root/03`, `_root/04`, `_root/05`, `_root/06`, `format-*-notices/**`, `_meta/stage4_prompts/**`) remain in place through Phase 6 atomic cutover; both old and new versions coexist with SUPERSEDED markers until cutover. (e) No per-account drafts retroactive re-runs required until Phase 7 pilot.
- **Manifest bumped**: no (Phase 0 is meta-layer only — no `_root/` doc edits this entry; Phase 1 docs will be added to `_root/00 §2` manifest table as they land per `_root/CONTRACTS.md §3` 5-step protocol).
```

Then bump `_root/09_changelog.md` front matter `Last updated` field to `2026-05-27 (Stage 5 Phase 0 — Snapshot + Planning Agent Handoff authored; → see Stage 5 Phase 0 entry below)` followed by the prior "Last updated" content (preserve as the chained narrative-history per the established pattern in line 7 of the doc).

---

## Stop condition

After both files are written:

1. Verify `_meta/stage5_prompts/STAGE_5_PLANNING_AGENT_HANDOFF.md` exists + is ~800–1,000 lines + has all 11 sections per the spec
2. Verify `_root/09_changelog.md` has the new Phase 0 entry appended + Last-updated header bumped
3. Produce conformance block (canonical per `_root/00_manifest.md §5`) attesting: manifest echo PASS; required reading PASS; Phase 0 deliverables landed; no Phase 1 content authored (you stopped at Phase 0); no `_archive/**` reads other than DO_NOT_READ.md awareness; ready-for-Phase-1 status confirmed
4. **STOP.** Do not begin Phase 1. Do not author `_root/01.5` / `_root/03.5` / `_root/03.6` / `_root/04.5`. Do not surface Phase 1 questions to operator (Phase 1 fresh agent does that, against the handoff you authored).

The operator will open a fresh Cursor chat next and paste the handoff doc you authored as the first message. That fresh chat is Agent A — the Stage 5 planning agent — and runs Phase 1.

---

*Anti-drift reminders for this Phase 0 finish session:*

- *Do NOT inject your own opinions about playbook prose, platform narrative, concession matrix, or substance budgets. The handoff captures operator-stamped INPUTS verbatim and the 8-phase SEQUENCE per spec — it does NOT make Phase 1 prose decisions.*
- *Do NOT read `_root/03`, `_root/04`, `_root/05`, `_root/06`, or any archived prose. The handoff is structurally derivable from the spec above + the operator-stamped inputs + the few `_root/` reads in the Required Reading list.*
- *Do NOT skip the changelog entry. Per `_root/CONTRACTS.md §3`, every change requires a `_root/09` entry. Phase 0 is a meta-layer change but it gets logged anyway because the snapshot creation + handoff authoring are operator-visible changes downstream agents need to discover.*
- *If anything in this spec is ambiguous, STOP and ask the operator per `_root/CONTRACTS.md §2`. Do NOT improvise.*
