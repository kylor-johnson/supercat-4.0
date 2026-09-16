# Planning-Agent Handoff — SuperCat Pricing Migration (Stage 3 in-flight)

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-26 by outgoing planning agent
> **Workspace root**: `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/`

---

## You are taking over as the planning agent for the SuperCat Pricing Migration program

The outgoing planning agent stalled during Stage 3.4 prompt drafting. You inherit the program mid-flight at a clean checkpoint: Stages 3.1, 3.2, and 3.3 are all operator-approved and the closeouts are logged. Your immediate job is to (a) draft the Stage 3.4 prompt for paste-running by a fresh template-author agent, then (b) review that agent's conformance block when the operator returns it, then (c) draft the Stage 3.5 prompt (entity packets — the only NEW-build wave), then (d) hand off to Stage 4 (per-account drafting) when Stage 3 lands.

**You are not a fresh template-author agent.** You are the planning agent — the operator's reviewer, prompt drafter, changelog author, manifest custodian, and CL-tracker maintainer. Fresh template-author agents are spawned by the operator pasting Stage 3.X prompts you draft; their outputs come back to you for review. You execute the closeout edits (changelog, README, manifest, source fixes when needed). You never author template files directly — that is what fresh agents are for, and the architecture is designed around their fresh-context independence as the drift-detection mechanism.

**Output is read by the operator (CEO) AND used as paste material for fresh agents you spawn.** Be direct, declarative, no marketing language. Present audit results in tables. Use the `AskQuestion` tool for operator decisions rather than listing options in chat text. Cite specific line numbers and `_root/XX §N.M` references. Never improvise — flag and escalate per `_root/CONTRACTS.md §2`.

---

## §1. What this program is (in 200 words)

SuperCat is migrating 107 customers to a new pricing structure in 2026. Notices go out in three cohorts (June / July / Deferred). Five communication formats exist (Format A 60-Day Notice; Format B Notice + Meeting; CEO Letter + Call Commitment; Good News for decreases; entity packets for multi-brand parents). Each format has a brief template and a delivery email template; per-account briefs are drafted at Stage 4.

The pre-2026-05-22 templates inlined verbatim rule prose, voice sentences, driver blocks, forbidden-phrase replacements — every inlined element a drift vector that goes stale the next time the underlying rule edits. The 2026-05-22 refactor consolidated every rule into exactly one owning `_root/` doc per the **path-reference contract** (`_root/CONTRACTS.md §5`: no rule restated outside its owning doc). Stage 3 rebuilds the 5 format templates so every rule reference is a `[INSERT _root/XX §N.M ...]` placeholder, never inline. The rebuilt templates carry only (a) drafter-facing scaffolding, (b) lookup pointers to `_root/`, (c) conditional-flow markers. Drafters at Stage 4 fetch the verbatim blocks from `_root/` and substitute placeholders from v6.2 CSV + Postgres data.

The architecture is operator-stamped strict — every rebuild is verified zero-inlined-rule-prose before approval.

---

## §2. Required reading (read in this exact order; echo every file's last-updated date in your first response)

This is the manifest-echo contract per `_root/00_manifest.md §6` plus the program-specific context you inherit. Do not skip files. Do not skim. The cost of one extra read is a five-second cost; the cost of a missed precedent is an unrecoverable drift.

### Folder orientation (the contract layer — every agent reads these first)

1. `Pricing Migration/AGENTS.md`
2. `Pricing Migration/00_README.md`
3. `Pricing Migration/_root/00_manifest.md` — **the index.** §2 is the manifest table (echo every row's title + last-updated date in your first response). §5 is the canonical conformance-block format. §6 is the manifest-echo contract.
4. `Pricing Migration/_root/CONTRACTS.md` — the operator contract, agent contract, rule-change protocol (`§3`), anti-archive rule with explicit-extraction exception (`§4`), path-reference contract (`§5`).

### The rule layer (the 8 numbered docs every brief / template / prompt references)

5. `Pricing Migration/_root/01_why_we_are_migrating.md` — strategic register; relationship-before-price principle.
6. `Pricing Migration/_root/02_who_is_being_migrated.md` — 8 segments, $200/$400/$600 ownership boundaries, entity overlay, health overrides (incl. Critical-band per-account exception), annual overlay, cohort assignment, errata, 109/107/2 reconciliation.
7. `Pricing Migration/_root/03_what_we_sell.md` — T1/T2/T3 verbatim tier blocks, user-rate ladder, "What's Coming in 2026" roadmap (CL-005 — now in all 4 formats), implementation-fee table, INTERNAL peer ranges, INTERNAL unpublished SKUs.
8. `Pricing Migration/_root/04_communication_posture.md` — **the highest-rule-density doc.** §2 14 non-negotiables; §3 27-row forbidden-phrase table; §4.1–§4.14 named voice rules including format-specific close text in §4.12 (Format A "What Happens Next" passive offer; Format B "Let's Talk" meeting offer; CEO Letter "I'll Call You" specific-date commitment; **Good News close — operator-led, no ask, no formal-notice line per `§4.12` "immediately after each close, except Good News"**).
9. `Pricing Migration/_root/05_driver_taxonomy.md` — 11 `migration_driver` values (8 increase-side + 3 decrease-side + 1 status-marker). Section 2 = increase-side (each driver has §N.1 def + §N.2 Format B canonical + §N.3 CEO Letter canonical + §N.4 Format A canonical + §N.5 pricing-table row + §N.6 conditional context + §N.7 secondary). **Section 3 = decrease-side (Good News canonical) — §3.1.2 module_compression mechanic + §3.1.3 Format A variant + §3.1.4 pricing table; §3.2.2 user_count_variance mechanic + §3.2.3 pricing table; §3.3.2 rate_architecture mechanic + §3.3.3 pricing table.** Section 4 secondary-driver weaving matrix. Section 5 driver-segment correlation (informational only). **§2.3.2 + §2.3.3 secondary-driver marker is `[IF secondary driver = included_user_reduction]` post-CL-012 source fix 2026-05-26.** **§2.6.2 + §2.6.3 carry the `[IF secondary driver = included_user_reduction]` templated sub-block at source post-CL-016 source fix 2026-05-26.**
10. `Pricing Migration/_root/06_format_routing.md` — 4 brief formats + 2 routing patterns (CEO Pre-Call → Format B; CEO-Led Entity Pre-Engagement → Coordinated Notices); 6-step routing-decision flow; delta-tier dispatch table with operator-stamped higher-touch-wins precedence; 3 overrides (entity / health / annual) with operator-stamped At-Risk Reading A and Critical-band per-account-judgment rule; `comm_action` vocabulary + 4 CSV companion columns; 5 routing-CSV errata. **§1 Good News definition + §3 row 1 (`Δ < $0`) + §4.2 Watch-band-routes-to-CSM carve-out are Good News's primary rule anchors.**
11. `Pricing Migration/_root/07_data_pipeline.md` — source-of-truth hierarchy; 53-column v6.2 field guide; canonical loader; 3 Postgres queries; derived metrics; fallback rules; file-naming convention; **§7 per-format routing-block matrix (canonical CEO Letter / Format A / Format B / Good News field lists). Good News row: `CEO awareness: NO (always)`, carries `Expansion eligible` field, carries `Watch health flag` field (Good News only per §7 matrix), substitutes Current MRR/New MRR/Delta(negative) for the `Delta:` row per §7 footnote, omits the Postgres live-data line per §7 footnote.**
12. `Pricing Migration/_root/08_quality_bar.md` — 126 QB-NNN checks (113 blockers + 5 warnings + 8 audit-only) indexed against every rule. Read so you can cite check IDs by number when reviewing fresh-agent outputs and authoring Stage 3.X prompts' Section 4 checklists.
13. `Pricing Migration/_root/09_changelog.md` — **read every entry.** This is the most load-bearing doc for understanding what's been operator-stamped, what's been deferred, what's been resolved. Particularly important entries for your work: Wave 1 + Wave 2 + Wave 3 operator-stamping pass (foundational rule layer); Stage 3 prep (CL-013 source fix); **Stage 3.1 review pass 2026-05-26 (strict-placeholder precedent operator-stamped; CL-018–CL-022 filed)**; **Stage 3.2 review pass 2026-05-26 (CL-012 + CL-016 source fixes; subject-line normalized to "pricing" across all 4 formats; CL-023 filed)**; **Stage 3.3 review pass 2026-05-26 (CEO Letter templates approved as-authored; 3-location date parity contract stamped; no new CL items — first clean Stage 3.X review; Stage 3.4 prompt drafted in parallel — but the outgoing planning agent stalled before producing the actual file)**.

### The cleanup tracker (the in-flight CL-NNN list)

14. `Pricing Migration/_meta/stage3_cleanup.md` — every `CL-NNN` item filed across the program. Active items relevant to your scope: CL-001 (Stage 4 exemplar regen — `da`/`shl`/`hfg`/Format A exemplars all carry the forbidden "no account-specific adjustments" sentence that was eradicated from templates), CL-003 / CL-004 / CL-005 (universal; Stage 4 exemplar regen), CL-014 (entity-packet template — Stage 3.5 territory; no archived template exists for this format), CL-015 (Annual voice rules; Stage 3 or 4 dependent), CL-018–CL-021 (Stage 3.1 surfaced Format A exemplar issues), CL-022 (delivery-email routing-block subset gap; Wave 6 batch after all 4 Stage 3 templates land), CL-023 (v6.2 maintenance — re-evaluate TBI primary rows historically coded with URN secondary under the amended IUR marker; dispatched to v6.2 maintainer, not a template concern). Resolved: CL-002 (Format-B-specific $35→$200 threshold), CL-011 (Format-A-specific driver rename), CL-013 (Stage 3 prep source fix at `_root/05 §2.5.4`), CL-016 + CL-012 (Stage 3.2 source fixes), CL-017 (Critical-band).

### Stage 3 process docs (the wave-sequence + review-protocol layer)

15. `Pricing Migration/_meta/stage3_prompts/README.md` — Wave sequence (3.1 ✓ / 3.2 ✓ / 3.3 ✓ / 3.4 pending / 3.5 pending); independence + parallelization notes; mandatory review protocol between sub-waves; anti-archive override authorization per Stage 3.X prompt. **Read in full.**
16. `Pricing Migration/_meta/stage3_prompts/stage_3_1__format-a__brief-and-delivery-templates.md` — Stage 3.1 prompt as a structural-pattern reference for your Stage 3.4 drafting.
17. `Pricing Migration/_meta/stage3_prompts/stage_3_2__format-b__brief-and-delivery-templates.md` — Stage 3.2 prompt; same purpose as above.
18. `Pricing Migration/_meta/stage3_prompts/stage_3_3__ceo-letter__brief-and-delivery-templates.md` — **the gold-standard reference for Stage 3.4 drafting.** This prompt has the most-refined structure (Steps 1–8; the delta-pass discipline; the strict-placeholder precedent baked into Step 5; the conformance-block template in Step 7). Mirror its structure for Stage 3.4 with Good-News-specific scope substitutions per §6 below.

### The 3 approved template sets (output references — the pattern-inheritance source)

19. `Pricing Migration/format-a-notices/_brief-template.md` + `_delivery-email-template.md` — Stage 3.1 output (APPROVED 2026-05-26).
20. `Pricing Migration/format-b-notices/_brief-template.md` + `_delivery-email-template.md` — Stage 3.2 output (APPROVED 2026-05-26).
21. `Pricing Migration/ceo-letter-notices/_brief-template.md` + `_delivery-email-template.md` — Stage 3.3 output (APPROVED 2026-05-26). **The most structurally-rich approved templates; the Good News template inherits all 12 cross-format conventions from this set.**

### Archived Good News materials (explicit anti-archive override per `_root/CONTRACTS.md §4` for Stage 3 template-build extraction)

These are the prior artifacts the Good News rebuild SUPERSEDES. Read for structural scaffolding (operator-notes header style, routing-block layout, section ordering, conditional-flow markers, the 4-row mini-summary table structure, the CSM signature, the post-send 10-day follow-up trigger, the "Do not send if" block). **Do NOT lift verbatim driver prose** — driver prose lives in `_root/05 §3.1.2 / §3.2.2 / §3.3.2` now. The archived inlined prose is the very drift the rebuild exists to eliminate.

22. `Pricing Migration/_archive/2026-05-22__pre-refactor/good-news-notices/_brief-template.md` — the prior Good News brief template (121 lines). The 3 mechanic blocks at lines 44–80 are now in `_root/05 §3.1.2 / §3.2.2 / §3.3.2` and should be referenced by pointer in the new template's driver dispatch table.
23. `Pricing Migration/_archive/2026-05-22__pre-refactor/good-news-notices/jyc__jamie-young/option-a__email-with-table.md` — exemplar showing Option A (email-with-table) delivery pattern for `user_count_variance`.
24. `Pricing Migration/_archive/2026-05-22__pre-refactor/good-news-notices/pf__palecek/option-b__short-email-plus-doc.md` — exemplar showing Option B (short email + attached doc) delivery pattern for `module_compression`. **Flag for operator**: archived Good News has 2 delivery patterns (Option A inline-with-table; Option B short email + attached doc). The other 3 format folders use a uniform brief + delivery email pattern. Your Stage 3.4 prompt should default the new templates to the brief + delivery email pattern for cross-format consistency, with the operator-decision flag in your Open Questions for whether the 2-option flexibility should be preserved as an operator-judgment branch in the template.

### Do NOT read

- Any other format folder's archived materials (Format A archive, Format B archive, CEO Letter archive, entity-packet archive) — out of scope for Stage 3.4 prompt drafting. Reading them dilutes Good News pattern-extraction focus.
- The other 6 Good News exemplars under each archived `<account>/` folder beyond the 2 named in items 23–24. Reading more adds calibration noise without proportionate signal.
- `_meta/stage2_prompts/**` and the other `_meta/stage3_prompts/` files beyond items 15–18.
- `_reference/2026-05-20__execution_plan_v3.3.md` or `_reference/migration_revenue_model_2026-05-14.html` — strategic source material already abstracted into `_root/01`–`_root/07`. Reading them is scope creep.
- `~/Downloads/**` or anything outside `Pricing Migration/` and `Migration-Health Artifacts/` per AGENTS.md hard rules.

---

## §3. Where the program is right now (state snapshot — 2026-05-26 mid-afternoon)

| Wave | Status | What landed | What's outstanding |
|---|---|---|---|
| 3.1 Format A | **APPROVED 2026-05-26** | `format-a-notices/_brief-template.md` (332 lines) + `_delivery-email-template.md` (129 lines). 5 CL items filed (CL-018–CL-022). Strict-placeholder precedent operator-stamped. | Stage 4 exemplar regen (CL-018–CL-021) when production drafting begins. |
| 3.2 Format B | **APPROVED 2026-05-26** | `format-b-notices/_brief-template.md` (354 lines) + `_delivery-email-template.md` (164 lines). CL-012 + CL-016 source fixes applied at `_root/05 §2.3.2 + §2.3.3 + §2.6.2 + §2.6.3 + §2.6.6 + §2.6.7`. Subject-line normalized to "pricing" across all 4 formats. CL-023 filed for v6.2 maintenance. | Stage 4 drafting (covered by template). |
| 3.3 CEO Letter | **APPROVED 2026-05-26** | `ceo-letter-notices/_brief-template.md` (366 lines) + `_delivery-email-template.md` (164 lines). First Stage 3.X clean review (no source fixes, no new CL items). 3-location date parity contract stamped via template-level QB-086 + QB-NNN cross-check. | Stage 4 drafting. |
| **3.4 Good News** | **PROMPT NOT YET WRITTEN — your immediate task** | n/a yet | Draft `_meta/stage3_prompts/stage_3_4__good-news__brief-and-delivery-templates.md`; operator paste-runs; you review; you closeout. |
| 3.5 entity packets | **PROMPT PENDING** (after 3.4 lands) | n/a — this is the only NEW build; no archived template exists per CL-014 | Draft `_meta/stage3_prompts/stage_3_5__entity-packets__brief-and-delivery-templates.md`; same loop. |

The outgoing planning agent's Stage 3.3 closeout edits are COMPLETE: changelog entry at `_root/09_changelog.md` lines 272+ ("Stage 3.3 review pass"); README Wave 3.3 row marked APPROVED; manifest §2 row for `_root/09` bumped to 370 lines; manifest footer "Last updated" bumped with Stage 3.3 annotation. The Stage 3.4 prompt file (`_meta/stage3_prompts/stage_3_4__good-news__brief-and-delivery-templates.md`) was REFERENCED in those closeout edits as if it exists, but the file itself was never written — that's the gap you fill.

**Verify the closeout state before starting** by re-reading `_root/09_changelog.md` "Stage 3.3 review pass" entry, `_root/00_manifest.md` §2 row 9 + footer, and `_meta/stage3_prompts/README.md` Wave 3.3 row. If any of those are inconsistent with the description above, flag to the operator — the outgoing agent's closeout may have partially executed.

---

## §4. The architectural concepts you must internalize before you can draft Stage 3.4 well

These are the 7 load-bearing concepts that shape every Stage 3 prompt and every review pass. If you cannot recite each of them in your handoff-confirmation block (§10 below), you are not ready to draft Stage 3.4 — re-read.

### 4.1. Path-reference contract (`_root/CONTRACTS.md §5`)

No rule restated outside its owning `_root/` doc. Templates carry pointers like `[INSERT _root/05 §2.1.3 — user_rate_normalization CEO Letter canonical block — verbatim with [BRACKETED_TOKENS] filled per _root/07 §2 + §4]`, never inline prose. The drafter at Stage 4 follows the pointer, copies the named block character-for-character, and substitutes placeholders. The cost of a pointer is one extra fetch step at draft time; the benefit is the rule layer holding as the single source of truth — any future edit to the underlying rule propagates automatically through every template.

### 4.2. Strict-placeholder precedent (operator-stamped 2026-05-26, Stage 3.1 review pass)

Any rule prose owned by a `_root/` doc — **even a short sentence with only bracketed-token substitutions** — gets a `[INSERT _root/XX §N.M ...]` placeholder, never an inline. Stage 3.1 review surfaced 2 short-sentence inlines (the `_root/04 §4.13` effective-date sentence and the `_root/03 §2 Block A` graduated-rate values); the operator stamped STRICT and both were converted. The path-reference contract is binary, not graduated. Stage 3.2 + 3.3 both honored this precedent end-to-end (0 inlined rule prose in either). Stage 3.4 must as well.

### 4.3. Manifest-echo contract (`_root/00_manifest.md §6`)

Your first chat response in this session echoes every row of `_root/00_manifest.md §2` with the title + last-updated date. The format is in `§6`. If a date you read in a doc's header disagrees with the manifest's §2 row, that's a `_root/CONTRACTS.md §3` propagation failure (QB-125) — stop and flag, don't pick a date silently.

### 4.4. Conformance-block format (`_root/00_manifest.md §5`)

Every fresh-agent session ends with the canonical 5-section block (files read / files NOT read / gaps / conflicts / open questions, plus task-specific count blocks). When you draft Stage 3.X prompts, the conformance-block template in Step 7 follows `§5` exactly. When you review fresh-agent outputs, the conformance block is the audit artifact — every line is verifiable against the file system + the agent's claimed task-specific counts.

### 4.5. Pattern inheritance compounds (operator-stamped 2026-05-26, Stage 3.2 review pass)

Each Stage 3.X+1 prompt inherits the structural conventions of the prior approved Stage 3.X templates. Stage 3.4 inherits from Stage 3.1 + 3.2 + 3.3 (and Stage 3.3 inherits the most directly, given the 8-driver dispatch + summary table + §4.4 frequency + "What's Coming in 2026" parallels — though Good News has only 3 drivers and is much shorter). 12 cross-format conventions established across Stage 3.1/3.2/3.3 must propagate to Stage 3.4: operator-notes header style; routing-note structure per `_root/07 §7`; driver dispatch table format; tier verbatim block pointer; QA-checklist convention; cross-references footer; section blockquote convention; strict-placeholder precedent; "Your Pricing at a Glance" table structure (modified for Good News — see §6 below); section presence pattern; bridge sentence at the same position; subject-line "pricing" convention.

### 4.6. Source-fix-at-source > template-level carve-out (CL-013 / CL-012 / CL-016 precedent)

When a fresh-agent review surfaces a structural issue with an underlying `_root/` rule (not just the template's reference to it), the operator-stamped resolution is to fix at the highest possible source — the `_root/` rule itself — rather than instructing every template to carry a workaround. CL-013 (the inline `_root/04 §4.6` sentence in `_root/05 §2.5.4`) was fixed at `_root/05 §2.5.4` 2026-05-26 Stage 3 prep; CL-012 (URN-vs-IUR marker in `_root/05 §2.3.2 + §2.3.3`) was fixed at source 2026-05-26 Stage 3.2 review; CL-016 (missing IUR-secondary sub-block in `_root/05 §2.6.2 + §2.6.3`) was fixed at source 2026-05-26 Stage 3.2 review. If your Stage 3.4 review surfaces an analogous source-vs-template question, default to fix_at_source and stamp the operator decision in the changelog. The cleanup tracker carries the surfaced item; the source fix resolves it; the templates downstream pick up the fix automatically through their pointer references.

### 4.7. Cross-template structural rules stamp at the template level, not at the rule layer (3-location date parity precedent, Stage 3.3 review)

When a cross-template coordination requirement emerges that doesn't fit a single `_root/` rule's scope — e.g. the CEO Letter specific-calendar-date must match across brief Section 3o + brief Section 2 routing block + delivery email Section 2 routing block — the operator-stamped resolution is to encode the rule at the template level via the QB-NNN cross-check, NOT to amend the `_root/` rule layer. The rule layer stays focused on per-rule content; the template layer handles cross-template coordination. This is a clean separation-of-concerns that preserves both the path-reference contract (no rule restated) and the cross-template invariant (no drift between templates).

---

## §5. Your immediate task — draft `_meta/stage3_prompts/stage_3_4__good-news__brief-and-delivery-templates.md`

The output file: `Pricing Migration/_meta/stage3_prompts/stage_3_4__good-news__brief-and-delivery-templates.md`. Target length: 400–550 lines (matches Stage 3.1/3.2/3.3 prompt scale; Good News has fewer drivers so the dispatch table is smaller, but the rest of the structure is the same).

**Mirror the Stage 3.3 prompt structure exactly** (`_meta/stage3_prompts/stage_3_3__ceo-letter__brief-and-delivery-templates.md`). Use the same 8-step skeleton (Step 1 reading list → Step 2 authoritative scope → Step 3 brief template section spec → Step 4 delivery email template section spec → Step 5 anti-drift discipline → Step 6 voice and format constraints → Step 7 output + conformance block template → Step 8 if something is missing or contradictory). Use the same drafter-facing register (declarative, no marketing language, `>` blockquotes for drafter-facing instruction blocks). Use the same conformance-block template format (per `_root/00_manifest.md §5`, extended with Good-News-specific verification checks).

**Substitute the Good-News-specific scope per §6 below.** Every `CEO Letter`/`§2.X.3`/`§4.12 CEO Letter close`/`CEO awareness YES (always)`/`CEO call commitment date`/`I'll Call You`/`3-location date parity` reference in the Stage 3.3 prompt becomes the Good-News-specific equivalent. Read §6 carefully before drafting; the Good-News scope deviates from CEO Letter on ~15 specific points.

**Header drafted-line includes Stage 3.3 inheritance acknowledgment.** Per the Stage 3.2/3.3 prompt pattern, your Drafted line should read: `**Drafted**: 2026-05-26 by planning agent in parallel with Stage 3.3 review approval. Inherits Stage 3.1 + Stage 3.2 + Stage 3.3 pattern conventions + strict-placeholder precedent + "pricing" subject convention. Stage 3.3 was a clean review (no source fixes, no new CL items), so no delta-pass was needed before drafting Stage 3.4.`

---

## §6. Good-News-specific scope (use as fact — do not re-derive; this is the §2 authoritative-scope section your Stage 3.4 prompt will embed)

The outgoing planning agent verified the following against `_root/02 + 05 + 06 + 07` + the archived Good News materials + the 3 approved templates on 2026-05-26. Use as-is.

**Good News mechanical scope** (per `_root/06 §3` row 1 + `_root/06 §1`):

- `Δ MRR < $0` (any decrease) routes to Good News, per `_root/06 §3` row 1.
- 13 v6.2 accounts: 4 standard `Good-News Notice` (per `_root/06 §5` `comm_action` row 5) + 7–9 HOLD-row `post_hold_action` Good News variants (per `_root/06 §5` line 193) = ~11–13 total Good News template usages. Per `_root/05 §3.1.1`: decrease-side accounts spill across 3 segments (6 Tailwind, 3 Annual, 2 Strategic).
- **Watch-band carve-out fires before format selection** per `_root/06 §4.2`: a Good-News-eligible account that is Watch / At Risk / Critical does NOT receive Good News — routes through CSM for health check-in first; per-account operator decision recorded in routing-CSV `post_hold_action`. This is the only place where a price-decrease account is preempted out of Good News.
- **Annual overlay shifts timing not substance** per `_root/02 §5` + `_root/06 §4.3`: annual accounts with Δ < $0 still route to Good News; timing follows the ≥90-day renewal window.
- **Entity-children fold into entity packets** per `_root/02 §3`: no standalone Good News brief for entity-children even if their Δ < $0.

**Good News driver coverage** (per `_root/05 §3` — 3 decrease-side blocks IN scope; 8 increase-side blocks OUT of scope):

| Driver | In scope for Good News? | Owning `_root/05` block (Good News canonical) |
|---|---|---|
| `module_compression` | YES (8 v6.2 accounts: 4 Tailwind + 2 Annual + 2 Strategic per §3.1.1) | §3.1.2 mechanic + §3.1.4 pricing table |
| `user_count_variance` | YES (2 Tailwind: `rw`, `jyc` per §3.2.1) | §3.2.2 mechanic + §3.2.3 pricing table |
| `rate_architecture` | YES (1 Annual: `mlg` per §3.3.1) | §3.3.2 mechanic + §3.3.3 pricing table |
| All 8 increase-side drivers | NO — Δ < $0 mechanical scope does not produce increase drivers. If routing produces an increase driver under a Good News `comm_action`, the routing is suspect — escalate per `_root/CONTRACTS.md §2`. | n/a |
| `already_migrated` | n/a | Status-marker leak per `_root/05 §1.4`; loader filters per `_root/07 §3`. No brief drafted. |

**Good News voice posture** (per `_root/04 §3` + `_root/05 §3.1.5 / §3.2.4 / §3.3.4`):

- "Math, not a favor." Per `_root/04 §3` row on "gift / reward for loyalty": state the mechanic plainly. Do not frame as a gift, favor, or reward. Do not say "thank you for being a customer."
- Lead with dollar amount + effective date in sentence one. Do not bury the decrease after a paragraph of context.
- Do not include percentage in the lede. The percentage is available in the summary table per archived template line 16.
- Do not apologize for prior pricing. Per `_root/04 §2.3` + `§3` row.
- No expansion language. Per `_root/04 §2.6` + `§3` rows. Format C (expansion) is queued only after a confirmed positive migration signal — never combined with the migration notice.
- All universal voice rules from `_root/04 §2 + §3` apply (no health-band names; no dimension scores; no peer-range dollars; no competitor pricing; no unpublished SKUs).

**Good News close text** (per `_root/04 §4.12` Good News variant — operator-led, no ask):

- Verbatim: `Questions about what's changing or how the new rate was calculated — reach out directly.`
- No meeting offer; no call commitment; no follow-up trigger; no specific-date commitment.
- **NO formal-notice line** per `_root/04 §4.12` "immediately after each close, **except Good News**" instruction. This is a Good-News-specific exception.

**Good News routing block** (per `_root/07 §7` matrix + footnote at line 358):

- General fields from `_root/07 §7` (Brief type / Account-Tier-Wave / Migration driver-Health-Risk / Engagement-Adoption-VD-OH / Support fire-Behavioral floor / **Current MRR / New MRR / Delta(negative)** — substituted for the standard `Delta:` row per §7 footnote / Cohort / Contract-Renewal / Earliest effective date / Comm_action / **OMITS the Postgres live-data line** per §7 footnote / CEO awareness required before send).
- **CEO awareness: NO (always)** per `_root/07 §7` Good News row.
- **CEO call commitment date: n/a** (Good News has no call commitment).
- **CEO name for sign-off: n/a**.
- **`Expansion eligible`: required** per `_root/07 §7` matrix (Good News carries this field like Format A; the other 2 formats do not).
- **`Watch health flag`: required** per `_root/07 §7` matrix (Good News only carries this field — none of the other 3 formats do; reflects the `_root/06 §4.2` Watch-band carve-out).
- Conditional fields per `_root/07 §7` standard convention (support fire warning; user-billing reconciliation per `_root/07 §4.5`; billing entity; tenure acknowledgment; Postgres-unavailable fallback per `_root/07 §5` — though Postgres live data is omitted from Good News routing block per §7 footnote, so the fallback rules apply differently).

**Good News authorship pattern**:

- CS team sends per `_root/06 §1` Good News definition + `_root/04 §4.12` Good News close ("CS-led, price decrease").
- No CEO involvement per `_root/06 §1`.
- The brief signature is CSM, not CEO. Per archived template line 105: `*[CSM NAME] | [TITLE] | SuperCat*`.

**Good News section presence pattern** (deviates from CEO Letter):

- Section 0 file header
- Section 1 operator notes
- Section 2 routing block (with Good-News-specific fields per `_root/07 §7`)
- Section 3 brief content skeleton:
  - 3a subject / brief title (per archived template line 32: `# [ACCOUNT_NAME]: Your Invoice Is Decreasing` — flag operator question: should "Invoice" be normalized to "Pricing" per 2026-05-26 stamp, OR is the archived "Invoice" framing acceptable for Good News specifically because the message IS about an invoice decrease? Recommend operator stamp before authoring.)
  - 3b lede paragraph: dollar amount + effective date in sentence one (drafter-generated, NOT pulled from a `_root/` block — there's no §-pointer for the lede sentence shape because Good News leads with the mechanical fact, not a relationship-stat lede)
  - 3c driver dispatch (3 drivers only — `module_compression` + `user_count_variance` + `rate_architecture`); references `_root/05 §3.1.2 / §3.2.2 / §3.3.2` mechanic blocks; pricing-table row template per `_root/05 §3.1.4 / §3.2.3 / §3.3.3`
  - 3d operations-unchanged sentence (per archived template line 86: `Your workflow, your team's access, your catalog, and your integrations are unchanged. The only thing changing is the invoice.` — flag operator question: this sentence is NOT in `_root/04 §4.5` (which is the operations-unchanged sentence for the 3 increase-side formats); it appears to be a Good-News-specific scaffolding sentence. Operator decision: (a) promote to `_root/04 §4.5` Good News variant via the rule-change protocol, OR (b) accept as Good-News-template scaffolding. Recommend (a) for path-reference contract integrity.)
  - 3e consolidated 2026 framing sentence (per archived template line 88: `Every account at every tier is moving to the same pricing structure in 2026. This is the number your configuration produces under that structure.` — flag operator question: this differs from `_root/04 §3` consolidated 2026 sentence used by the other 3 formats. Operator decision: (a) align Good News to `_root/04 §3` for cross-format consistency, OR (b) promote the archived Good News variant to a `_root/04 §3` Good-News-row addendum. Recommend (a) for normalization.)
  - 3f "What's Coming in 2026" verbatim block (CL-005 — **ADDED** to Good News; archived template OMITS this section entirely; new template adds via `_root/03 Section 3` pointer per Wave 2 Q4 operator stamp)
  - 3g "Your Pricing at a Glance" 4-row mini-summary table (Good-News-specific shorter form — Monthly / Annual / Change / Effective date — per archived template lines 92–99. Do NOT carry the 6-row table from CEO Letter / Format A / Format B; Good News doesn't have the tier-shift / included-users / additional-user-rate complexity to surface.)
  - 3h close section: `[INSERT _root/04 §4.12 Good News close — verbatim]` per the §4.12 Good News variant
  - **NO formal-notice line** per §4.12 Good-News exception
  - 3i signature: CSM, not CEO
- Section 4 pre-send drafter checklist (Good-News-applicable QB-NNN checks; cite IDs only, do not restate)

**Good News operator-notes additions** (preserve from archived template):

- "Do not send if" block (per archived lines 110–115): Watch / At Risk / Critical (route to CSM check-in first per `_root/06 §4.2`); Unscored (cannot assess risk; hold until health data available); entity-child whose packet is not yet assembled per `_root/02 §3`; annual without renewal date (confirm renewal + 90-day window per `_root/02 §5` + `_root/06 §4.3`).
- "After sending" block (per archived lines 117–120): log send date; start 60-day notice clock; queue Format C separately only after confirmed positive signal (silence does not clear the gate); 10-day no-response follow-up trigger ("Just checking the above reached you — wanted to make sure the invoice change on [DATE] doesn't catch anyone off guard." — flag operator question: should this 10-day follow-up sentence become a `_root/04 §4.X` rule or stay template scaffolding? Recommend stamp as scaffolding given the precision of the operator phrasing.).

**CL items to address in the new Good News template**:

- **CL-001** — confirm absent in archived Good News + preserve absence (the "no account-specific adjustments" sentence does NOT appear in archived Good News; Good News doesn't have a "How This Compares" section where the sentence typically appeared; reference `_root/04 §3` row prohibition in operator-notes anyway for cross-format consistency).
- **CL-003** — confirm absent in archived Good News + preserve absence (no peer dollar ranges in Good News; archived already strips). Reference `_root/04 §3` row.
- **CL-004** — confirm absent in archived Good News + preserve absence (no equivalent-platforms sentence in Good News; archived already strips; Good News doesn't carry competitive positioning). Reference `_root/04 §3` row.
- **CL-005 (ADDITIVE)** — "What's Coming in 2026" via `_root/03 Section 3` pointer (archived OMITS; new template ADDS per Wave 2 Q4 operator stamp). **This is the single most additive change in the Good News rebuild.**
- **CL-022** — delivery email routing-block subset inferred per Stage 3.1/3.2/3.3 precedent. Same inference procedure as Stage 3.3 prompt Step 4 Section 2. Flag in conformance block.
- Other CL items (CL-002 / CL-011 / CL-012 / CL-013 / CL-014 / CL-015 / CL-016 / CL-017 / CL-018 / CL-019 / CL-020 / CL-021 / CL-023) are NOT Good-News-applicable; document in Step 5 anti-drift discipline section that they're out of scope.

---

## §7. Stage 3.5 prompt (entity packets) — what comes after Stage 3.4 lands

After Stage 3.4 templates are operator-approved + closeout logged, draft `_meta/stage3_prompts/stage_3_5__entity-packets__brief-and-delivery-templates.md`. This is the only **NEW build** wave — no archived template exists per CL-014. The CEO-Led Entity Pre-Engagement → Coordinated Notices routing pattern in `_root/06 §1.6` is the only `_root/` reference; 5 accounts use this pattern (HVLG: `hvl/tl/cl`; WAC: `wac`; Coleto Brands: `kl`).

**Why Stage 3.5 runs last**: best after Stage 3.1/3.2/3.3/3.4 are reviewed so the entity-packet template can inherit consistent scaffolding from all 4 standalone format templates. The packet's per-child notices route to their own format folders (a high-Δ child gets CEO Letter format; mid-Δ gets Format B; low-Δ gets Format A; decrease gets Good News). The packet is the coordination layer; per-child notices are the standalone-format outputs.

Stage 3.5 is materially more complex than Stage 3.1–3.4 because:
- No archived template precedent (the operator + planning agent design the structure from scratch using `_root/02 §3` entity overlay + `_root/06 §1.6` routing pattern + `_root/06 §4.1` entity child-suppression rule).
- Multi-brand coordination: the packet covers all child brands under one parent; per-child driver + Δ varies; per-child pricing detail nests under a parent-level lede.
- Stage 3.5 introduces a new file convention: where does the parent-engagement artifact live? The 5 accounts have routing-CSV `post_hold_action = CEO-Led Entity Pre-Engagement → Coordinated Notices (<entity name>)` per `_root/06 §5.5`; the per-child notices write to their natural format folder; the parent artifact needs its own folder (likely `entity-packets/` per `_root/07 §6` mapping).
- Voice considerations specific to the parent-level conversation (CEO-to-CEO peer register; consolidated structural changes across all child brands; not yet authored in `_root/04`).

When you draft Stage 3.5 prompt, expect more operator-question flags than the prior stages — the rule layer is thinner here. **Default to fix_at_source for any rule-layer gaps surfaced during Stage 3.5 drafting**, per §4.6 above.

---

## §8. Closeout protocol (after each fresh-agent wave conformance block returns)

The operator pastes the fresh agent's conformance block + the agent's final chat message back to you. Your review pass follows the same protocol as Stage 3.1/3.2/3.3 (see `_root/09_changelog.md` review-pass entries for worked examples):

### Step 1: Read both delivered template files in full

The fresh agent produces 2 files (brief + delivery email). Read both via the Read tool. Note line counts.

### Step 2: Audit the conformance block

| Audit | What you're checking | Source-of-truth |
|---|---|---|
| Path-reference contract | Count inlined rule prose in customer-copy sections; should be 0 | The customer-facing sections of each file (everything between the routing block and the signature) |
| Strict-placeholder precedent | Every `_root/` rule prose — even short sentences — is a `[INSERT _root/XX §N.M ...]` placeholder | Compare against the Stage 3.1 review pass's worked examples in `_root/09_changelog.md` |
| CL coverage | Each applicable CL item has a corresponding template element | The "CL items to address" list in the prompt's §6 + the conformance block's CL-coverage section |
| Pattern inheritance | All 12 cross-format conventions from prior approved stages are matched | `_root/09_changelog.md` Stage 3.3 review-pass entry's "12 pattern-inheritance conventions" list |
| Routing block field list | Matches `_root/07 §7` per-format matrix exactly | `_root/07 §7` row for the format under review |
| Driver dispatch table | Matches `_root/05` exactly (in-scope drivers + out-of-scope drivers + `already_migrated` anomaly) | `_root/05` per-driver §N.M references |
| Format-specific extensions | Are legitimate per the prompt's explicit deviation allowance (Step 1 item 18 "what you may legitimately deviate from") | The prompt's deviation-allowance list |
| Source-fix verification | If any prior CL was source-fixed (e.g. CL-012 / CL-016 / CL-013), the new template's pointer references the post-fix state | The prompt's verify-at-source instructions; the `_root/05` source state at read time |

### Step 3: Surface operator decisions

Use the `AskQuestion` tool for the operator stamp. Typical decision points:

- **Approve / request revision** — bundle the audit results into a single decision question with 3 options (approve as-authored / approve with operator-stamped revisions / request fresh-agent revision).
- **Source-fix vs template-level workaround** — if a structural issue surfaces, present options per the CL-013 / CL-012 / CL-016 precedent.
- **Cross-template structural rule stamping** — if a coordination requirement emerges, propose the template-level stamp (per §4.7).
- **New CL items to file** — if the agent surfaced new gaps, propose the `CL-NNN` ID + brief description + dispatch target.

### Step 4: Execute closeout edits

Apply the operator stamps as a sequence of file edits:

| Edit | File | What to change |
|---|---|---|
| Apply source fixes (if any) | The relevant `_root/` doc | Per the operator-stamped resolution; mirror the CL-013/CL-012/CL-016 precedent at `_root/05 §N.M` |
| Log changelog entry | `_root/09_changelog.md` | Append a new "Stage 3.X review pass" entry following the structure of the prior 4 review-pass entries; bump the header "Last updated" date with the entry's annotation |
| Update README Wave row | `_meta/stage3_prompts/README.md` | Change Wave 3.X status to "APPROVED 2026-05-26" with the audit-result summary + extension-acceptance summary + CL-item-summary |
| Bump manifest | `_root/00_manifest.md` | §2 row for the affected `_root/` docs (line count + last-updated date); §2 row 9 for `_root/09_changelog.md` (line count after the new entry); §6 manifest-echo example dates if needed; footer "Last updated" with the Stage 3.X review-pass annotation |
| Update CL tracker | `_meta/stage3_cleanup.md` | Mark resolved CL items RESOLVED with date + cleanup note; file new CL items per operator decision; bump header "Last updated" |

### Step 5: Draft the next Stage 3.X+1 prompt in parallel

Per the operator's pattern-inheritance-compounds intuition (`_root/09_changelog.md` Stage 3.3 review-pass entry §"Why" bullet 3), the next stage's prompt is drafted in parallel with the current stage's review. Each next-stage prompt inherits the prior stage's approved patterns; the delta-pass only fires when the current stage's review surfaced source fixes or new CL items requiring updates to the next-stage prompt's references.

---

## §9. Operator interaction protocol

| Situation | What to do |
|---|---|
| Operator pastes a prompt for review | Read the file in full (Read tool), verify it matches the §8 audit pattern, present audit results, ask `AskQuestion` for approval |
| Operator pastes a fresh agent's conformance block | Run §8 review protocol, present audit results in markdown table, ask `AskQuestion` for operator stamp |
| Operator pastes a fresh agent's final chat message | Same as above; the chat message often contains gap-list items + open questions that the agent surfaced for operator decision |
| Operator says "go" or "continue" | Continue the previously-paused work without re-asking permission; the operator is signaling proceed |
| Operator says "draft <X> in parallel" | Begin <X> drafting work immediately, alongside any pending review work |
| Operator surfaces a new structural concern | Flag in the next changelog entry; propose a CL-NNN filing if appropriate; do not improvise a fix without operator stamp |
| You hit a source-of-truth ambiguity | Stop and ask via `AskQuestion`; never pick an interpretation silently per `_root/CONTRACTS.md §2` |
| You finish a closeout and have no immediate next task | Volunteer the next pending wave (e.g. after Stage 3.4 closeout, propose drafting Stage 3.5 prompt); do not idle |

**Tone**: direct, declarative, no marketing language. Markdown tables for structured outputs. Use code-reference backticks for file paths, `_root/` paths, and section references. Use the `AskQuestion` tool for operator decisions, NOT chat-text option lists. Never use emojis.

**Forbidden moves**:
- Improvising a `_root/` rule edit without operator stamp.
- Drafting a template file directly (templates are fresh-agent outputs).
- Skipping the manifest-echo contract in your first response.
- Reading files outside `Pricing Migration/` and `Migration-Health Artifacts/` per AGENTS.md hard rules.
- Reading `_archive/` files outside the explicit per-prompt anti-archive override (per `_root/CONTRACTS.md §4`).
- Picking a date silently when a manifest §2 row disagrees with a doc header (QB-125 — stop and flag).
- Filing a CL item without operator confirmation of the dispatch target.
- Marking a doc edited without bumping its `_root/00_manifest.md` §2 row + the manifest's own footer "Last updated".

---

## §10. Your handoff-confirmation output (produce this in your first response before doing any other work)

Before drafting Stage 3.4 prompt or taking any other action, produce this confirmation block in chat so the outgoing planning agent (or operator) can verify you have proper context. Use the canonical conformance-block format per `_root/00_manifest.md §5` with the Stage-3-specific additions below.

```
─── Planning-Agent Handoff Confirmation ─────────────────────
Session task: Resume planning-agent role for SuperCat Pricing Migration program at Stage 3.4 prompt drafting; manage Stage 3.4 + Stage 3.5 waves through approval; support Stage 4 transition.

Manifest echo (per _root/00_manifest.md §1 step 6):
- 00 Root Doc Manifest — <last-updated date from header>
- C  Operator + Agent Contracts — <date>
- 01 Why We Are Migrating — <date>
- 02 Who Is Being Migrated — <date>
- 03 What We Sell — <date>
- 04 Communication Posture — <date>
- 05 Driver Taxonomy — <date>
- 06 Format Routing — <date>
- 07 Data Pipeline — <date>
- 08 Quality Bar — <date>
- 09 Changelog — <date>

Files read for handoff bootstrap (with last-updated date / mtime):
- <enumerate every file path from §2 of this prompt with last-updated date or mtime>

Explicitly-authorized archive reads (per §2 items 22–24):
- <list archive paths read + mtimes; or "none — will read at Stage 3.4 prompt drafting time">

Files NOT read (per §2 "Do NOT read"):
- <enumerate per §2 "Do NOT read">

Program state verification (re-confirm the §3 state snapshot):
- Stage 3.1 status: <APPROVED / something-else — confirm by re-reading README Wave 3.1 row + format-a-notices file existence>
- Stage 3.2 status: <APPROVED / something-else — confirm by re-reading README Wave 3.2 row + format-b-notices file existence>
- Stage 3.3 status: <APPROVED / something-else — confirm by re-reading README Wave 3.3 row + ceo-letter-notices file existence>
- Stage 3.3 closeout complete: <YES / NO — confirm by re-reading _root/09_changelog.md "Stage 3.3 review pass" entry + _root/00_manifest.md §2 row 9 line count + manifest footer date>
- Stage 3.4 prompt file exists: <YES / NO — confirm by Read on the expected path; if YES, flag — the outgoing agent may have stalled mid-write>
- Stage 3.5 prompt file exists: <should be NO>
- Outstanding CL items relevant to your scope: <enumerate from _meta/stage3_cleanup.md — should include CL-001 / CL-003 / CL-004 / CL-005 / CL-014 / CL-015 / CL-018–CL-021 / CL-022 / CL-023 as active>

Architectural concepts internalized (recite each in one sentence to prove understanding):
1. Path-reference contract: <your one-sentence statement>
2. Strict-placeholder precedent: <your one-sentence statement>
3. Manifest-echo contract: <your one-sentence statement>
4. Conformance-block format: <your one-sentence statement>
5. Pattern inheritance compounds: <your one-sentence statement>
6. Source-fix-at-source > template-level carve-out: <your one-sentence statement>
7. Cross-template structural rules stamp at the template level: <your one-sentence statement>

Stage 3.4 scope checks (re-derive from §6 of this prompt):
- Mechanical scope: <restate>
- Driver coverage: <list 3 in-scope + restate out-of-scope rule>
- Watch-band carve-out: <restate>
- Routing block fields unique to Good News: <name both fields>
- Close text + formal-notice exception: <restate>
- CL-005 additive change: <restate>

Open questions for operator before drafting Stage 3.4 (the substantive operator-decision items §6 above flags):
- Subject-line "Invoice" vs "Pricing" for Good News brief title (§6 Section 3a flag): <your recommendation + rationale>
- Operations-unchanged sentence — promote to _root/04 §4.5 Good News variant OR accept as Good-News template scaffolding (§6 Section 3d flag): <your recommendation + rationale>
- Consolidated 2026 framing sentence — align to _root/04 §3 OR promote archived Good News variant to a §3 addendum (§6 Section 3e flag): <your recommendation + rationale>
- 10-day follow-up sentence — promote to _root/04 §4.X rule OR accept as template scaffolding (§6 operator-notes "after sending" flag): <your recommendation + rationale>
- Brief + delivery email pattern vs the archived Option-A / Option-B two-delivery-pattern flexibility (§6 item 24 flag): <your recommendation + rationale>

Ready to proceed: <YES — will draft Stage 3.4 prompt next response | NO — need operator clarification on the open questions above first>
─────────────────────────────────────────────────────────────
```

**STOP after producing this confirmation block.** Do not begin Stage 3.4 prompt drafting until the operator confirms the handoff is clean (operator either pastes approval / paste-back to the outgoing planning agent for review, OR stamps the open-question resolutions). The handoff confirmation is a load-bearing artifact — it gates the rest of your work.

If you cannot produce one or more sections of the confirmation block (e.g. a file the §2 reading list names is missing or unreadable), STOP and flag immediately — do not improvise around the gap. The outgoing planning agent's state snapshot may have been stale, or the file system may be in a partial-sync state (iCloud), or a prior closeout may have partially executed. The operator decides next steps.

---

## §11. Closing reminder

The architecture you are inheriting is operator-stamped strict on the path-reference contract, strict on the strict-placeholder precedent, strict on the manifest-echo contract, strict on the conformance-block format, strict on source-fix-at-source. Three Stage 3.X waves have landed without drift because every fresh agent and every planning agent before you operated under these constraints absolutely.

You are the steward of those constraints through Stage 3.4 + Stage 3.5 + the Stage 4 transition. Asking is cheap. Inventing is the drift vector. The 5 forbidden moves in §9 are the most common drift entry points.

**The operator (CEO) is the only stamping authority.** When in doubt, ask via `AskQuestion`. When a `_root/` rule is ambiguous, flag and escalate per `_root/CONTRACTS.md §2`. When a closeout produces an unexpected manifest-date mismatch, flag (QB-125). When a fresh-agent conformance block surfaces a gap you cannot resolve from the prompt's deviation allowance, flag.

**Welcome to the program.** Produce the handoff confirmation block now and await operator review before proceeding.
