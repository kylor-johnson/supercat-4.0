# Planning-Agent Handoff — SuperCat Pricing Migration (Stage 5: Playbook Architecture Refactor)

> **For paste into a fresh Cursor agent chat (Agent mode) as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-27 by Stage 4 chat (outgoing) at operator direction (Phase 0 execution).
> **Workspace root**: `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/`
> **Owner**: CEO
> **Supersedes (operationally, prose-and-mapping layer only)**: `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` and the 4-format architecture it operates over. The Stage 4 handoff remains in place for audit + pattern reference; Stage 5 supersedes its Phase 4-production scope.
> **Scope of this handoff**: Bootstrap Phase 1 ONLY. Phases 2–8 each get their own paste-ready prompts authored by the Stage 5 planning agent (you) at each phase gate as Stage 5 progresses, matching the established Stage 4 `_meta/stage4_prompts/_paste-ready/` pattern. This handoff grows via top-of-file amendment blocks per the Stage 4 amendment precedent — not in-place rewrites.

> **Amendment 1 — 2026-05-27 (Phase 1 intra-stage takeover; steps 1 + 2 → 3 + 4)**: Stage 5 Phase 1 chat A (outgoing) at operator direction closed after authoring `_root/01.5_playbook_architecture.md` (648 lines; CL-032 RESOLVED) and `_root/03.5_artifact_taxonomy.md` (430 lines; CL-033 RESOLVED) with full `_root/CONTRACTS.md §3` 5-step sweeps applied to both landings (`_root/00_manifest.md` 229→247 lines absorbing 2 §2 row inserts + 2 §3 reading-order inserts + 15 §4 topic-index entries + 2 row 0 self-row line-count bumps + row 9 self-row line-count bumps 775→817 reconciling Source-fix Session D manifest sync gap + 2 §2 footer cumulative recounts 4,804→5,487→5,942; `_root/09_changelog.md` 775→817 lines absorbing CL-032 + CL-033 entries; NEW `_meta/stage5_cleanup.md` 144 lines housing Stage 5 CL-NNN series initialized with CL-032 + CL-033 entries). Operator stamped intra-stage takeover 2026-05-27 12:08 UTC-6 per honest context-management self-assessment: Source-fix Session E verbatim content (Section VI Axis 1 × Axis 2 composition; concession menus per playbook) lives in chat A transcript but never paste-quoted by chat A — chat A referenced it only as forward pointers to Phase 1 siblings `_root/03.6` + `_root/04.5` per path-reference contract. Phase 1 chat B (incoming) authors `_root/03.6_platform_narrative.md` (step 3) + `_root/04.5_concessions.md` (step 4) + closes Phase 1. Paste-ready prep prompt for chat B operator paste-run lives at `_meta/stage5_prompts/stage_5_phase_1_handoff_to_steps_3-4.md` (drafted 2026-05-27 by chat A at session close). Same Stage 4.2 intra-stage takeover precedent (chat 4.1 → chat 4.2 at 2026-05-26; `_meta/stage4_prompts/stage_4_session_handoff_to_4_2-4_5.md`). Stage 5 charter (this doc) unchanged below — chat B reads §§1–8 as authored 2026-05-27.

---

## You are the Stage 5 planning agent

The Stage 4 chat (outgoing) closed at 2026-05-27 after the operator (CEO) reviewed the 2026-05-26 Stage 4.2 `cci` (Currey & Company) production artifact and identified that the new artifact is structurally identical to the 2026-05-19 archived pre-refactor artifact. Root cause: `_root/04` and `_root/05` cite the archived templates + per-account exemplars as `Primary sources` in their front matter; the path-reference contract enforces verbatim paste of that prose; output was structurally guaranteed to look like archive.

You are stewarding the rebuild of the prose-and-mapping layer downstream of `_root/02 §1` (where the 8 segments are already correctly stamped). The infrastructure layer (`AGENTS.md`, `_root/00`, `_root/CONTRACTS.md`, `_root/01`, `_root/02`, `_root/07`, `_root/08` skeleton, `_root/09`, data files, reconciliation log, Stage 4 8-step drafter skeleton) stays.

You do not author client copy directly. Fresh authoring agents in Phases 1–5 own the prose decisions per operator stamp at each gate. Your role mirrors Stage 4: planning, prompt authoring, operator-stamping facilitator, changelog + manifest custodian, per-account ledger maintainer. You author paste-ready prompts at each phase boundary that the operator paste-runs into fresh Cursor chats.

---

## §1. Why Stage 5 exists

### §1.1. What the operator observed

The 2026-05-26 Stage 4.2 production artifact at `format-b-notices/cci__currey-and-company__brief.md` (134 lines) is structurally identical to the 2026-05-19 pre-refactor archived artifact at `_archive/2026-05-22__pre-refactor/format-b-notices/cci__currey-company__brief.md` (96 lines). Material differences are limited to: effective date update (July 19 → September 1); lede paraphrase; one additive section ("What's Coming in 2026") per CL-005; routing block format change; sign-off name resolution. The body — driver explanation, pricing table, tier description, "Let's Talk" close, formal-notice line, operations-unchanged sentence, summary table, billing-basis footnote — is character-identical or near-identical between the two.

### §1.2. Why this happened structurally

`_root/04_communication_posture.md` line 9 (front matter) cites as `Primary sources`: archived `_handoff-prompt.md`, archived `_template-test-prompt.md`, archived per-account exemplars (kal, kii, ih, da, pf).

`_root/05_driver_taxonomy.md` line 9 (front matter) cites as `Primary sources`: archived `_handoff-prompt.md`, archived Format A/B/CEO Letter/Good News brief templates, archived per-account exemplars.

The rebuild extracted and codified the archived prose into rule docs. The path-reference contract (`_root/CONTRACTS.md §5`) then enforces verbatim paste of that prose into every new artifact. Stage 4 drafter prompts forbid paraphrase ("Zero paraphrase of owned rule prose — including short sentences"). New artifacts were guaranteed to look like archived artifacts because the archived prose IS the rule layer.

The drift-prevention machinery worked exactly as designed. It just was designed to preserve the wrong thing.

### §1.3. What was supposed to come out instead

Per `_root/02 §1` (operator-stamped 2026-05-22) and operator-stamped inputs §2.2 + §2.5 below: an 8-playbook architecture producing 6 notice templates + 4 companion materials, with substance distributed across notice (legal-clock vehicle) vs companion (substance carrier). Platform-vs-product-menu positioning. Per-playbook concessions framework + cadence + duration + mixed-segment handling + pilot-then-scale model. None of these are currently captured at `_root/`.

---

## §2. Operator-stamped sources of truth (the inputs to Stage 5 authoring)

### §2.1. Already-stamped at `_root/02 §1` (operator 2026-05-22)

The 8 segments + ownership boundaries + cohort assignment are operator-stamped at `_root/02 §1` lines 13–28. **This is the input contract for all Stage 5 authoring. Do NOT edit `_root/02 §1`.** It is referenced by pointer from `_root/01.5_playbook_architecture.md` (Phase 1) and `_root/06_playbook_routing.md` (Phase 2); never restated.

### §2.2. Operator-stamped 2026-05-27: the playbook table

Verbatim from operator chat 2026-05-27. The 3 stamped rows (Core / Narrative / Entity) are canonical Phase 1 inputs. The 5 TBD rows (Executive / Pre-Engagement / Strategic / Tailwind / Annual) are surfaced via `AskQuestion` in your Phase 1 first-action sequence (§6.1).

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

### §2.3. Operator-stamped 2026-05-27: the two concerns

Verbatim from operator chat 2026-05-27:

1. "Objective of the notice / balancing substance contained in the notice vs attached artifact — (rationale) SuperCat has transitioned to platform…standardized pricing across customers"
2. "Articulating the platform vs product menu"

### §2.4. Operator-stamped 2026-05-27: the three deliverables

Verbatim from operator chat 2026-05-27:

1. Establish general communication and posture standards and guidelines
2. Further define communication variants so it's clear what substance is contained where: simplified migration notice vs [full artifact]
3. Translate standards and guidelines into templates

### §2.5. Operator-stamped 2026-05-27: Notice Template Family + Companion Materials

Verbatim from operator chat 2026-05-27. The notice triggers the legal 60-day clock; companion materials carry the substance.

#### Notice Template Family

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

### §2.6. The legal-clock-vs-substance-carrier split rule

Derivable from §2.5 verbatim language. The notice triggers the legal 60-day clock; companion materials carry the substance. This rule governs every artifact-taxonomy decision in `_root/03.5_artifact_taxonomy.md` (authored Phase 1). The rule is the canonical input that resolves the operator's §2.3 concern 1.

---

## §3. The cut-line

### §3.1. STAYS (do not touch unless explicitly directed)

`AGENTS.md`; `_root/00_manifest.md` (table updates lockstep per `_root/CONTRACTS.md §3`); `_root/CONTRACTS.md`; `_root/01_why_we_are_migrating.md`; **`_root/02_who_is_being_migrated.md`** (input contract — sealed); `_root/07_data_pipeline.md`; `_root/08_quality_bar.md` (skeleton; ~12 format-keyed checks rekeyed at Phase 6); `_root/09_changelog.md` (audit trail continues); `_meta/v6_2_reconciliation_log.md`; `_master-account-data-v6.2.csv`; `migration_comm_tiers_2026-05-19.csv`; `_reference/**`; `_root/06 §2` 6-step routing flow (mechanics stay; only terminal dispatch changes in Phase 2); Stage 4 8-step drafter skeleton at `_meta/stage4_prompts/stage_4_1__format-a__per-account-drafter.md` (pattern reference for Phase 5); `entity-packets/` (refined not rebuilt in Phase 4 — closest alignment to Entity Migration Packet per §2.5).

### §3.2. REWRITES (parallel build, operator-stamp, atomic Phase 6 cutover)

| Doc / scope | Phase | What changes |
|---|---|---|
| `_root/03 §1` tier blocks (T1/T2/T3) | 3a | Rewrite for platform-vs-product-menu framing per `_root/03.6` |
| `_root/03 §3` roadmap | 3a | Reframe as platform-investment narrative; may relocate per substance budget in `_root/03.5` |
| `_root/04 §3` consolidated 2026 sentence + forbidden-phrase table | 3a | Replace procedural sentence with platform-positioning sentence; refresh table for playbook vocabulary |
| `_root/04 §4.5` operations-unchanged variants | 3b | Per-playbook substance-budget variants |
| `_root/04 §4.12` close variants | 3b | 8 playbook-specific closes (was 4 format-specific) |
| `_root/05 §2.X` driver prose (8 increase-side drivers) | 3c | Recut into **notice form-cut** + **simplified-companion form-cut** + **full-companion form-cut** per §2.5 / §2.6 split |
| `_root/06_format_routing.md` | 2 | Replaced by `_root/06_playbook_routing.md` (8-playbook dispatch) |
| `_root/08` format-keyed QB checks (~12) | 6 | Rekey playbook-keyed |
| Template folders | 4 | Replace `format-a/b/ceo-letter/good-news-notices/` with `core/narrative/executive/pre-engagement/tailwind/strategic/annual/`; `entity-packets/` refined in place |
| Stage 4 drafter prompts | 5 | Replaced by `_meta/stage5_prompts/stage_5_X__[playbook]__per-account-drafter.md` family |

### §3.3. NEW (additive)

| Doc / artifact | Phase | What it owns |
|---|---|---|
| `_root/01.5_playbook_architecture.md` | 1 | 8 playbooks per §2.2 + `_root/02 §1`; references segment defs by pointer; owns playbook timing, owner, cadence, duration, mixed-segment, pilot/feedback |
| `_root/03.5_artifact_taxonomy.md` | 1 | 6 notices + 4 companions per §2.5; substance budget per artifact; §2.6 legal-clock-vs-substance split rule; delivery semantics |
| `_root/03.6_platform_narrative.md` | 1 | Platform-vs-product-menu source-of-truth sentences; resolves operator concern §2.3 item 2 |
| `_root/04.5_concessions.md` | 1 | Pre-authorized + CEO-required matrix per playbook |
| `_meta/stage5_cleanup.md` | 1 | Stage 5 CL-NNN tracker (Stage 3 tracker continues for legacy items) |
| Playbook-keyed template folders | 4 | `core/`, `narrative/`, `executive/`, `pre-engagement/`, `tailwind/`, `strategic/`, `annual/` |
| `_meta/stage5_prompts/_paste-ready/` | Per-phase | Per-phase paste-ready prompts you author at each phase gate |

---

## §4. The 8-phase sequence

Per-phase detail (Owner / Output / Reading scope / Gate / Drift control / Duration) is documented in the per-phase paste-ready prompts you author at each phase gate. This handoff carries the sequence + summary only. Per-phase paste-readys go to `_meta/stage5_prompts/_paste-ready/stage_5_X__<phase>.md` matching the Stage 4 pattern.

- **Phase 0 — Snapshot + handoff (COMPLETE 2026-05-27)**: snapshot at `_archive/2026-05-27__pre-stage5/`; this handoff. Status: COMPLETE
- **Phase 1 — Taxonomy docs (next)**: fresh Agent A authors 4 new docs (`_root/01.5` + `_root/03.5` + `_root/03.6` + `_root/04.5`) + initializes `_meta/stage5_cleanup.md`. ~1 day. Detailed scope in §6 below
- **Phase 2 — Dispatch rewrite**: fresh Agent B authors `_root/06_playbook_routing.md` (8-playbook dispatch; 6-step flow + 3 overrides + `comm_action` vocabulary preserved). ~half day
- **Phase 3a — Platform anchor prose**: fresh Agent C rewrites `_root/04 §3` + `_root/03 §1` + `_root/03 §3` per Phase 1 platform narrative. ~1 day
- **Phase 3b — Close + ops-unchanged variants**: fresh Agent D rewrites `_root/04 §4.12` (8 playbook closes) + `_root/04 §4.5` (playbook variants). ~half day
- **Phase 3c — Driver block recuts**: **one fresh agent per driver** (8 sessions); recut each `_root/05 §2.X` into 3 form-cuts (notice / simplified-companion / full-companion). Sequenced URN → PDC → TBI → IUR → ABTS → MOR → ADR → SA. ~1 day total
- **Phase 4 — Templates per playbook**: one fresh agent per playbook (F1–F6 sequential; F7–F8 deferred to post-pilot); per-playbook template families (~16 templates total grouped into 6 sessions). ~3 days
- **Phase 5 — Stage 5 drafter prompts per playbook**: G1–G6 sequential; per-playbook prompts pattern-inheriting Stage 4 8-step skeleton. ~3 days
- **Phase 6 — Atomic cutover**: mechanical; archive pre-rebuild artifacts; rename new docs canonical; manifest + changelog sweep; `_root/08` rekey. ~1 hour
- **Phase 7 — Pilot per playbook**: fresh per-account drafter per pilot; sequence Core → Narrative → Entity → Executive → Pre-Engagement; each permitted to STOP per `_root/CONTRACTS.md §2` for source-fix issues (precedent: Stage 4.2 cci/bri/sca → CL-026/CL-027/CL-028). ~half day per pilot
- **Phase 8 — Batch June cohort**: Core (13) + Narrative (15) + Entity (27) = 55 accounts. Operator capacity-limited

**Total time-to-first-correct-output**: 3–4 days tight stamping; 5–7 days async. June cohort send before July 1 achievable on either trajectory.

**Agent assignment principle**: every authoring step runs in a fresh chat against operator-stamped context. Fresh-per-agent is the cross-agent drift control; manifest-echo + path-reference contract + conformance blocks + `_root/CONTRACTS.md §2` stop-and-ask are the per-agent drift controls.

---

## §5. Anti-drift discipline (7 invariants)

Stage 5 invariants operator-stamped 2026-05-27. Any agent violating one has output discarded per `_root/CONTRACTS.md §2`.

1. **No cross-phase chat continuation.** Every authoring step starts fresh against the operator-stamped handoff + the phase's paste-ready prompt. Phase 6 cutover mechanical work is the only exception
2. **No skipping taxonomy docs to go straight to prose.** Without Phase 1 outputs, every Phase 3 prose rewrite is sized to gut. Author the rules before the prose
3. **No multi-driver authoring in one Phase 3c session.** Fresh-per-driver. The cross-driver consistency one agent would unconsciously enforce is the wrong pressure for Stage 5
4. **No parallel pilots before first playbook is frozen.** Pilots will surface source-fix issues (Stage 4.2 precedent). Serialize
5. **Do not touch `_root/02 §1`.** Sealed input contract for Phase 2 dispatch rewrite
6. **No `_archive/**` reads during authoring.** Archived prose IS the drift attractor. The Phase 0 snapshot at `_archive/2026-05-27__pre-stage5/` is rollback-only. `_root/CONTRACTS.md §4` exception applies only to operator-directed extraction by file path
7. **No skipping manifest + changelog updates.** Every edit closes with `_root/CONTRACTS.md §3` 5-step protocol: edit, log, bump dates, update manifest, identify downstream re-runs

---

## §6. Phase 1 detailed scope (the only phase fully specified in this handoff)

### §6.1. Pre-authoring: surface 5 questions to operator via `AskQuestion`

Before authoring `_root/01.5`, surface and wait for operator stamps:

- **Question 1** — Fill the 5 TBD playbook rows (Executive / Pre-Engagement / Strategic / Tailwind / Annual) per §2.2 columns. Serialize one playbook at a time if `AskQuestion` form gets too large
- **Question 2a** — Substance budget per notice template (6 notices in §2.5): target word count + sections allowed per notice
- **Question 2b** — Substance budget per companion material (3 written companions: Full value artifact / Simplified value summary / CEO exec letter): target word count + sections allowed per companion
- **Question 2c** — Confirm delivery semantics per companion verbatim from §2.5 ("Delivered with or ahead of notice" / "Attached to notice" / "Delivered alongside notice" / "CEO initiates before any notice is sent")
- **Question 3** — Platform-vs-product-menu (operator concern §2.3 item 2): canonical positioning sentence (operator stated rationale "SuperCat has transitioned to platform…standardized pricing across customers" — confirm verbatim or amend); tier-narrative structural pattern; roadmap relocation decision (stays in Core/Narrative artifacts? or only Executive/Pre-Engagement full value artifact?)
- **Question 4** — Concessions matrix fill-in for the 5 unfilled playbooks; confirm canonical concession list completeness (existing list: user cleanup, billing date adjustment, annual prepay, 30-day transition credit, multi-brand consolidation)
- **Question 5** — Timing rules confirmation per §2.5: Strategic notice post-CEO-conversation; Pre-Engagement CEO call before notice; Entity packet legal coverage all children simultaneously; Annual ≥90-day pre-renewal (per `_root/02 §5`). Operator confirms operational binding form of each

Wait for operator stamps before authoring. Improvising is invariant 2 violation.

### §6.2. Authoring order (after stamps land)

1. `_root/01.5_playbook_architecture.md` — 8 playbooks per §2.2 (post-stamp) + `_root/02 §1` (by reference; do NOT restate per `_root/CONTRACTS.md §5`). Owns: per-playbook cohort/timing, notice/artifact (by reference to `_root/03.5`), meeting handling, follow-up cadence, framing, artifact composition, pilot/feedback loop, mixed-segment handling, delivery model, concessions (by reference to `_root/04.5`), owner, duration. CL-NNN tracker entry on landing
2. `_root/03.5_artifact_taxonomy.md` — 6 notices + 4 companions per §2.5 verbatim; substance budget per artifact (post-Question-2a/2b stamps); §2.6 legal-clock-vs-substance split rule verbatim; delivery semantics per §2.5 (post-Question-2c confirmation). CL-NNN entry
3. `_root/03.6_platform_narrative.md` — platform positioning sentence (post-Question-3 stamp); tier-narrative structural pattern; roadmap relocation decision. CL-NNN entry. May fold into `_root/03` at Phase 3a if operator prefers — surface decision at landing
4. `_root/04.5_concessions.md` — pre-authorized + CEO-required matrix per playbook (post-Question-4 stamps). CL-NNN entry
5. `_meta/stage5_cleanup.md` initialized — Stage 5 CL-NNN tracker; cross-references `_meta/stage3_cleanup.md` for legacy items

### §6.3. Manifest + changelog sweep per `_root/CONTRACTS.md §3` (after each doc lands)

1. Bump `Last updated` header in the doc
2. Add a row to `_root/00_manifest.md §2` (path, last-updated, lines, what-it-owns one-line)
3. Add a row to `_root/00_manifest.md §3` reading-order list
4. Add an entry to `_root/00_manifest.md §4` topic index
5. Append a Phase 1 entry to `_root/09_changelog.md` per the established format
6. File CL-NNN entry in `_meta/stage5_cleanup.md`

### §6.4. Phase 1 stop condition

All 4 docs land + manifest + changelog + cleanup tracker reflect them + operator stamps full Phase 1 output via `AskQuestion`. Then author `_meta/stage5_prompts/_paste-ready/stage_5_2__dispatch_rewrite.md` (the Phase 2 paste-ready). Surface to operator: ready for Phase 2 in fresh chat. STOP.

---

## §7. First-action sequence (your first response in this chat)

Required reading (read in this order; manifest-echo contract per `_root/00 §6`):

1. `AGENTS.md`
2. `_root/00_manifest.md` (echo §2 every row)
3. `_root/CONTRACTS.md` (§3 / §4 / §5)
4. `_root/01_why_we_are_migrating.md`
5. `_root/02_who_is_being_migrated.md` (especially §1; sealed input contract)
6. `_root/07_data_pipeline.md` (stays; awareness)
7. `_root/08_quality_bar.md` (skeleton; structural awareness)
8. `_root/09_changelog.md` (every entry; particularly Stage 4.2 cohort iters + Stage 4 prep Source-fix Sessions for source-fix discipline you inherit)
9. This handoff
10. `_archive/2026-05-27__pre-stage5/DO_NOT_READ.md` (snapshot manifest awareness; do NOT read other snapshot contents per anti-archive)
11. `_meta/stage4_prompts/README.md` + `_meta/stage4_prompts/stage_4_1__format-a__per-account-drafter.md` (Stage 4 patterns inherited; structural only, NOT for Format A prose)
12. `_meta/stage4_account_ledger.md` (pattern; you continue appending Phase 7/8)

Do NOT read in Phase 1: `_root/03`, `_root/04`, `_root/05`, `_root/06` (rewrite targets — reading biases inheritance); `format-*-notices/**` (rebuild targets); `_archive/**` other than item 10; `_meta/stage2_prompts/`, `_meta/stage3_prompts/` (historical); `_reference/**` (already abstracted); `Migration-Health Artifacts/` (already abstracted).

Your first message in this chat:

1. **Manifest echo**: paste-quote every `_root/00 §2` row with Last-updated date verified at source (not from manifest cell — CL-024 paste-verification discipline)
2. **Required-reading completeness echo**: enumerate items 1–12 with verified Last-updated date
3. **State snapshot verification**: confirm `_archive/2026-05-27__pre-stage5/` exists + DO_NOT_READ.md present; this handoff exists at `_meta/stage5_prompts/STAGE_5_PLANNING_AGENT_HANDOFF.md`; `_root/01.5` / `_root/03.5` / `_root/03.6` / `_root/04.5` / `_meta/stage5_cleanup.md` do NOT yet exist (you author Phase 1); paste-quote `_root/02 §1` lines 13–28 segment table to confirm canonical input
4. **Conformance block** (canonical per `_root/00 §5` + Stage 5 additions): includes session-task line + output target + manifest echo result + reading completeness + state snapshot verification + files-NOT-read list per Phase 1 reading scope + ready-to-surface-Question-1 status
5. **Wait for operator signal.** Do NOT author `_root/01.5` until operator stamps the 5 questions per §6.1. Improvising violates invariant 2

---

## §8. Cross-references

`_root/00_manifest.md`; `_root/CONTRACTS.md §3` (rule-change protocol every Phase 1+ edit follows); `_root/CONTRACTS.md §4` (anti-archive — Phase 0 snapshot sealed); `_root/CONTRACTS.md §5` (path-reference contract — Phase 1 docs reference `_root/02 §1` by pointer); `_root/02_who_is_being_migrated.md §1` (input contract); `_root/09_changelog.md` (audit trail); `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` (Stage 4 handoff pattern inherited); `_meta/stage4_prompts/README.md` (Stage 4 review protocol + paste-ready pattern inherited); `_meta/stage4_prompts/stage_4_1__format-a__per-account-drafter.md` (8-step drafter skeleton — pattern-inherited Phase 5); `_archive/2026-05-27__pre-stage5/DO_NOT_READ.md` (snapshot marker; awareness only).

---

*This handoff is the operator-stamped Stage 5 charter as of 2026-05-27. Amendments follow the Stage 4 handoff amendment pattern: append a dated amendment blockquote at the top of this file; do not edit in place.*
