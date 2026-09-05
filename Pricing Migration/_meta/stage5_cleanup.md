# Stage 5 Cleanup Tracker

> **Purpose**: The running list of Stage 5 CL-NNN items — surfaced, resolved, deferred, or open. Stage 5 spans Phase 0 (snapshot + handoff) through Phase 8 (June cohort batch); each Phase 1+ `_root/` doc landing or per-phase planning-agent intake files a CL-NNN entry here. Stage 5 has its own CL-NNN series independent of legacy items; legacy items continue at `_meta/stage3_cleanup.md` until each is RESOLVED at the source where it lands.
>
> **Cross-reference**: `_meta/stage3_cleanup.md` is the legacy tracker (Stage 2 through Stage 4; CL-001 through CL-031 series); the most recent legacy entries (CL-029 + CL-030 + CL-031) RESOLVED 2026-05-27 via Source-fix Session D. Stage 5 cleanup tracker (this file) starts at CL-032; numbering continues the global CL-NNN series so cross-doc references remain unambiguous.
>
> **Read by**: Planning agent during Stage 5 phase transitions; not read by fresh authoring agents (each Phase's paste-ready prompt carries the relevant CL-NNN context inline). Stage 5 Phase 1 fresh agent reads this file as Phase 1 reading scope item 12-equivalent (per the handoff sibling-doc reading scope addition at `_root/00 §3`).
>
> **Last updated**: 2026-05-27 (CL-033 FILED + RESOLVED — `_root/03.5_artifact_taxonomy.md` landed; Stage 5 Phase 1 second doc CLOSED. Prior: CL-032 FILED + RESOLVED — `_root/01.5_playbook_architecture.md` landed; Stage 5 Phase 1 first doc CLOSED).
>
> **Owner**: CEO (via planning agent).

---

## Format

Each entry follows:

```
### CL-NNN — <one-line summary>

- **Phase**: Stage 5 Phase X
- **Source**: <which `_root/` doc / planning-agent session / operator chat surfaced the item>
- **Fix**: <what was done OR what needs to be done>
- **Locations affected**: <files written, edited, or referenced>
- **Status**: FILED / RESOLVED / DEFERRED / OPEN
- **Resolved**: <date + by whom> (if RESOLVED)
- **Notes** (optional): <gotchas, downstream impacts, audit trail>
```

Entries are listed in CL-NNN order. RESOLVED items stay in the tracker for audit trail; do not delete.

---

## Phase 1 entries (taxonomy docs)

### CL-032 — `_root/01.5_playbook_architecture.md` authored at source (Stage 5 Phase 1 step 1 of 5)

- **Phase**: Stage 5 Phase 1
- **Source**: `_meta/stage5_prompts/STAGE_5_PLANNING_AGENT_HANDOFF.md §6.2` step 1 (operator-stamped 2026-05-27) + operator-stamped Source-fix Session E (operator chat 2026-05-27 — resolves handoff §2.2 5 TBD playbook rows + stamps Section IV billing-cycle cohort architecture + Section V Playbook Anatomy 10-item structure + Section VI Two-Axis composition).
- **Fix**: Authored `_root/01.5_playbook_architecture.md` (648 lines; 8-playbook architecture; §0 timing model / §1 8-playbook overview + canonical 14-column table + capacity-realistic comm architecture mapping + 10-item Playbook Anatomy / §§2–9 per-playbook sections following Playbook Anatomy / §10 cross-references). References `_root/02 §1` (sealed input contract) + `_root/03.5` / `_root/03.6` / `_root/04.5` (Phase 1 siblings — landing next) + `_root/06` (Phase 2 rewrite target) by pointer per `_root/CONTRACTS.md §5` path-reference contract. STARTER markers on §X.6 objection scripts + §X.9 CRM stage checklists per operator-stamped "default-then-correct" authoring mode (refined at Phase 4 template authoring or Phase 2 dispatch rewrite as appropriate).
- **Locations affected**:
  - NEW `_root/01.5_playbook_architecture.md` (648 lines).
  - `_root/00_manifest.md` — §2 row 1.5 inserted between rows 1 and 2; §3 reading-order item 5 inserted between `_root/02` and `_root/03` (subsequent items renumbered 6–12; intro "9 numbered docs" → "10 numbered docs"; per-task variation "all 11" → "all 12" + Stage 5 Phase 1 sibling-doc author reading scope added); §4 topic-index 7 entries appended; row 0 self-row Last-updated 2026-05-27 + Lines 229 → 238 + cell annotation Stage 5 Phase 1 prefix; row 9 self-row line count 775 → 801 (reconciling residual Source-fix Session D manifest sync gap); §2 footer cumulative recount 4,804 → 5,487 + "this 4,804-line corpus" → "this 5,487-line corpus"; Last-updated header bumped with Stage 5 Phase 1 prefix + prior Source-fix Session D paragraph retained.
  - `_root/09_changelog.md` — Last-updated header bumped 2026-05-27 with Stage 5 Phase 1 prefix + prior Phase 0 paragraph retained; new entry appended at end of file (2026-05-27 — Stage 5 Phase 1 — `_root/01.5_playbook_architecture.md` landed (CL-032 RESOLVED)).
  - NEW `_meta/stage5_cleanup.md` (this file; initialized this session as the durable home of the Stage 5 CL-NNN series).
- **Status**: RESOLVED 2026-05-27 by Stage 5 Phase 1 planning agent in this chat. CLOSED.
- **Resolved**: 2026-05-27 by Stage 5 Phase 1 planning agent (operator stamp signal "proceed" + operator answers #1–#5 + operator stamp `Mode switched to Agent. Start _root/01.5. Go.`).
- **Notes**:
  - **`_root/02 §1` untouched** per Stage 5 invariant 5 — sealed input contract preserved; `_root/01.5 §1.2` is a pointer not a restatement.
  - **Path-reference contract honored** per `_root/CONTRACTS.md §5` — Notice Template Family + Companion Materials substance referenced to `_root/03.5` (Phase 1 sibling — not restated); Axis 1 × Axis 2 composition + canonical platform-positioning sentence referenced to `_root/03.6` (Phase 1 sibling — not restated); per-playbook concession matrix detail referenced to `_root/04.5` (Phase 1 sibling — not restated); segment definitions referenced to `_root/02 §1` (sealed input — not restated). The only verbatim cross-doc paste in `_root/01.5` is the §1.1 canonical 14-column playbook table (operator-stamped 2026-05-27 — paste-quoted verbatim from Source-fix Session E + handoff §2.2) which is `_root/01.5`'s legitimate ownership (this doc owns the per-playbook architecture table).
  - **STARTER markers** preserve operator-pending refinement boundary so future drafters do not mistake placeholder content for stamped rules. Markers: `STARTER (operator-pending refinement at Phase 4 template authoring)` for objection scripts (§X.6) and CRM stage checklists (§X.9).
  - **Open items propagated to Phase 1 sibling docs** (not blocking CL-032 itself):
    - `_root/03.5` (CL-033 — RESOLVED 2026-05-27; see CL-033 entry below): Q2a substance budget per notice template + Q2b substance budget per companion material (operator stamp at `_root/03.5` review per chat operator answer #3 "starter ranges accepted as you laid them out … annotate each budget in `_root/03.5` itself as `STARTER (operator-pending refinement at Phase 4 template authoring)`"). RESOLVED via default-then-correct authoring + visible STARTER markers at every length-budget cell in `_root/03.5 §1.X / §2.X / §5`.
    - `_root/03.6` (CL-034 forthcoming): Q3 canonical platform-positioning sentence (operator picks from 2–3 variants surfaced at `_root/03.6` review per chat operator answer #2); Section VI Axis 1 × Axis 2 composition rules + canonical examples (Crystorama / Hudson Valley / WAC) + Two-Tier Production model paste-quoted verbatim from Source-fix Session E (operator chat answer #1).
    - `_root/04.5` (CL-035 forthcoming): 5 open cell items A–F from prior chat turn (Executive vs Narrative concession menu identity intentional? Executive CEO-approval column moot since CEO co-authors? Pre-Engagement CEO-approval column? Tailwind concessions default to none? Annual concessions inherit natural segment? Bounded transition pricing "intermediate rate" definition?). Operator stamps at `_root/04.5` review.
  - **Open items propagated to Phase 2 (`_root/06_playbook_routing.md`)**: cohort/comm-family misalignment formal audit deferred from Phase 1 per operator stamp ("defer formal audit to Phase 2 dispatch rewrite"); no specific files identified by operator at Phase 1 intake. Phase 2 dispatch rewrite agent runs the audit against `_master-account-data-v6.2.csv` routing-logic canonical source per anti-drift invariant 5. `_root/01.5 §8.1` Strategic-named-accounts paragraph carries the named accounts (HVLG, Coleto Brands, Rock House Farm, Watch-band, VD<40 accounts) as awareness with routing canonical per `_root/02 §4` health-override rule.
  - **Open items propagated to Phase 4 (template authoring)**: STARTER objection-script + CRM-stage placeholders at `_root/01.5 §§2–9` items 6 and 9 — Phase 4 per-playbook template sessions pressure-test against real client scenarios and refine.
    - **Open items propagated to Phase 7 (pilot per playbook)**: Stage 4.2 `bri` pending re-run absorbed into Stage 5 Phase 7 pilot per Narrative playbook pilot candidate selection (operator surfaces via Phase 7 paste-ready when Phase 7 lands per handoff §4).

### CL-033 — `_root/03.5_artifact_taxonomy.md` authored at source (Stage 5 Phase 1 step 2 of 5)

- **Phase**: Stage 5 Phase 1
- **Source**: `_meta/stage5_prompts/STAGE_5_PLANNING_AGENT_HANDOFF.md §6.2` step 2 (operator-stamped 2026-05-27) + handoff §2.5 (Notice Template Family + Companion Materials tables — operator-stamped verbatim 2026-05-27) + handoff §2.6 (legal-clock-vs-substance-carrier split rule — operator-stamped verbatim 2026-05-27) + operator-stamped Source-fix Session E (Two-Tier Production capacity-aligned model + production timeline) + operator-stamped length-budget STARTER ranges per this chat operator answer #3 ("starter ranges accepted as you laid them out … annotate each budget in `_root/03.5` itself as `STARTER (operator-pending refinement at Phase 4 template authoring)`").
- **Fix**: Authored `_root/03.5_artifact_taxonomy.md` (430 lines; 6 notice templates + 4 companion materials + legal-clock-vs-substance-carrier split rule + delivery semantics + Two-Tier Production model + substance-budget STARTER summary). Structure: §0 legal-clock-vs-substance-carrier split rule (foundational pairing principle; handoff §2.6 + Source-fix Session E verbatim) / §1 Notice Template Family with §1.1–§1.6 per-template detail (Good News / Standard Migration / Value Migration / Entity Migration Packet / Strategic Migration / Annual Renewal) / §2 Companion Materials with §2.1–§2.4 per-companion detail (Full value artifact / Simplified value summary / CEO exec letter / CEO-initiated call) / §3 Delivery semantics table with 5 sequencing invariants / §4 Two-Tier Production capacity-aligned model + production timeline / §5 Substance budget summary table (10 rows; all STARTER) / §6 Cross-references. References `_root/02 §1` (sealed) + `_root/01.5` (Phase 1 sibling — landed) + `_root/03` / `_root/04` / `_root/05` / `_root/06` (Phase 2 / Phase 3a / Phase 3a-b / Phase 3c rewrite targets) + `_root/07` (data pipeline) + `_root/03.6` / `_root/04.5` (Phase 1 siblings — landing next) by pointer per `_root/CONTRACTS.md §5` path-reference contract. STARTER markers visible inline at every length-budget cell in §1.X / §2.X + a prominent ⚠ STARTER callout at §5 substance-budget summary table opening per operator instruction ("annotate each budget in `_root/03.5` itself as `STARTER (operator-pending refinement at Phase 4 template authoring)` so the placeholder is visible — don't bury it").
- **Locations affected**:
  - NEW `_root/03.5_artifact_taxonomy.md` (430 lines).
  - `_root/00_manifest.md` — §2 row 3.5 inserted between rows 3 and 4 (Lines 430; What it owns one-liner cell with full annotation); row 3 cell appended with "Phase 3a rewrite target" annotation; §3 reading-order item 7 inserted between `_root/03` and `_root/04` (subsequent items renumbered 8–13; intro "10 numbered docs" → "11 numbered docs"; per-task variation "all 12" → "all 13" + Stage 5 Phase 1 sibling-doc author reading scope updated to pin `_root/03.5` as landed and remove from "landing in sequence" list); §4 topic-index 8 entries appended (Artifact taxonomy / Legal-clock split rule / Notice family / Companion family / Delivery semantics with 5 sequencing invariants / Two-Tier Production model / Substance-budget STARTER); row 0 self-row Last-updated annotation extended with Stage 5 Phase 1 step 2 prefix + line count and footer marked TBD pending recount step; Last-updated header bumped with Stage 5 Phase 1 step 2 prefix + prior Stage 5 Phase 1 step 1 paragraph retained.
  - `_root/09_changelog.md` — Last-updated header bumped 2026-05-27 with Stage 5 Phase 1 step 2 prefix + prior Stage 5 Phase 1 step 1 paragraph retained; new entry appended at end of file (2026-05-27 — Stage 5 Phase 1 — `_root/03.5_artifact_taxonomy.md` landed (CL-033 RESOLVED)).
  - `_meta/stage5_cleanup.md` (this file) — Last-updated header bumped; CL-033 entry filed here; CL-032 entry's "Open items propagated" cross-reference updated to mark CL-033 as RESOLVED.
- **Status**: RESOLVED 2026-05-27 by Stage 5 Phase 1 planning agent in this chat. CLOSED.
- **Resolved**: 2026-05-27 by Stage 5 Phase 1 planning agent (operator stamp signal "proceed to _root/03.5_artifact_taxonomy.md (Phase 1 step 2)").
- **Notes**:
  - **`_root/02 §1` untouched** per Stage 5 invariant 5 — sealed input contract preserved; every per-artifact "Applies to" cell is a pointer to `_root/02 §1` line N.
  - **Path-reference contract honored** per `_root/CONTRACTS.md §5` — `_root/03` (tier names + user-rate ladder + "What's Coming in 2026" block) + `_root/04` (voice + framing + close text + audience register + parent-letter voice register + annual-cohort voice rules) + `_root/05` (per-driver `migration_driver` explanation) + `_root/06` (dispatch logic) + `_root/07` (data fields) + `_root/08 §10` (entity-packet program QB-NNN checks) substance referenced by pointer; not restated. Verbatim cross-doc paste = handoff §2.5 Notice Template Family + Companion Materials tables at §1 intro + §2 intro (this doc's legitimate ownership) + handoff §2.6 legal-clock-vs-substance-carrier split rule at §0 (this doc's legitimate ownership).
  - **STARTER markers** visible inline at every length-budget cell in §1.X + §2.X + a prominent ⚠ STARTER callout at §5 substance-budget summary table opening per operator instruction. Markers: `STARTER (operator-pending refinement at Phase 4 template authoring)`. Operator-pending refinement scope explicitly enumerated at §5 footer (notice word-count ranges; Full value artifact upper bound; Simplified value summary parameterized-1-page constraint; Entity packet range; CEO exec letter range).
  - **Operator-stamped length-budget STARTER ranges** (per chat operator answer #3 this session): Good News Notice ~3–5 sentences; Standard Migration Notice ~150–250 words; Value Migration Notice ~150–300 words; Entity Migration Packet ~1,000–2,500 words (~2–4 pages); Strategic Migration Notice ~100–200 words; Annual Renewal Notice inherits natural segment + 1–2 sentence Annual opener; Full value artifact ~800–2,000 words bespoke; Simplified value summary ~1 page / ~500 words; CEO exec letter ~150–300 words (~half page); CEO-initiated call N/A (conversational).
  - **Two-Tier Production capacity-aligned model** (per Source-fix Session E verbatim): Full artifact for Executive ($401–$600 delta) + Pre-Engagement (>$600 delta); Simplified summary for Core (≤$200) + Narrative ($201–$400); Entity packet for all entity children (~27 accounts / ~17 packets); No artifact for Tailwind. Production timeline: Entity packets and simplified summaries complete during readiness sprint before June cohort launch. Full bespoke artifacts for July cohort produced during late June, refined by entity conversation feedback (per `_root/01.5 §0.6` "why entity conversations ARE the pilot").
  - **Open items propagated to Phase 1 sibling docs** (not blocking CL-033 itself):
    - `_root/03.6` (CL-034 forthcoming): Q3 canonical platform-positioning sentence (operator picks from 2–3 variants surfaced at `_root/03.6` review per chat operator answer #2); Section VI Axis 1 × Axis 2 composition rules + canonical examples (Crystorama / Hudson Valley / WAC) paste-quoted verbatim from Source-fix Session E; install-base normalization framing canonicalized for Value Migration Notice (`_root/03.5 §1.3`) per `platform_discount_correction` driver.
    - `_root/04.5` (CL-035 forthcoming): 5 open cell items A–F from prior chat turn (Executive vs Narrative concession menu identity intentional? Executive CEO-approval column moot since CEO co-authors? Pre-Engagement CEO-approval column? Tailwind concessions default to none? Annual concessions inherit natural segment? Bounded transition pricing "intermediate rate" definition?). Operator stamps at `_root/04.5` review.
  - **Open items propagated to Phase 2 (`_root/06_playbook_routing.md`)**: cohort/comm-family misalignment formal audit deferred from Phase 1 per operator stamp (unchanged from CL-032).
  - **Open items propagated to Phase 3a/3b/3c**: this doc's structural pointers (notice form / simplified-companion form / full-companion form) per Stage 5 cut-line §3.2 are the input contract for `_root/03` rewrite (Phase 3a — recut tier and user-rate language against this doc's artifact taxonomy) + `_root/04` rewrite (Phase 3a/3b — audience register + forbidden phrases + close text per playbook + parent-letter voice register + annual-cohort voice rules) + `_root/05` rewrite (Phase 3c — recut each driver into 3 form-cuts).
  - **Open items propagated to Phase 4 (template authoring)**: every length budget at `_root/03.5 §1.X` + §2.X + §5 carries STARTER status; Phase 4 templates pressure-test ranges + operator stamps refined budgets. Specifically: Full value artifact upper bound (~2,000 words); Simplified value summary parameterized-1-page constraint; Entity packet per-entity range; CEO exec letter ~150–300 word range.
  - **Open items propagated to Stage 5 readiness sprint** (per Source-fix Session E production timeline): scheduling of the readiness sprint itself is operator-pending; one specific 24-hour ask carried from `_root/01.5 §9.3` step 1 (Jonathan Charles renewal-date audit). Phase mapping for the readiness sprint surfaces at Phase 4 paste-ready (or earlier if operator clarifies).

---

## Phase 2 entries (dispatch rewrite — pending Phase 2 paste-ready)

*Empty. CL-NNN entries land here as Phase 2 work begins.*

---

## Phase 3 entries (prose rewrites — pending Phase 3a / 3b / 3c paste-readys)

*Empty. CL-NNN entries land here as Phase 3 work begins.*

---

## Phase 4 entries (templates per playbook — pending Phase 4 paste-readys)

*Empty. CL-NNN entries land here as Phase 4 work begins.*

---

## Phase 5 entries (Stage 5 drafter prompts per playbook — pending Phase 5 paste-readys)

*Empty. CL-NNN entries land here as Phase 5 work begins.*

---

## Phase 6 entries (atomic cutover — pending Phase 6 paste-ready)

*Empty. CL-NNN entries land here as Phase 6 work begins.*

---

## Phase 7 entries (pilot per playbook — pending Phase 7 paste-ready)

*Empty. CL-NNN entries land here as Phase 7 work begins. Stage 4.2 `bri` pending re-run absorbed here per CL-032 notes — operator surfaces via Phase 7 paste-ready.*

---

## Phase 8 entries (June cohort batch — pending Phase 8 paste-ready)

*Empty. CL-NNN entries land here as Phase 8 work begins.*

---

## Cross-reference: legacy CL-NNN items at `_meta/stage3_cleanup.md`

The legacy tracker (CL-001 through CL-031) lives at `_meta/stage3_cleanup.md`. Most items are RESOLVED at source per the prior cadence (Stages 2 / 3 / 3.5 / 4 / 4.1 / 4.2). The Stage 5 cleanup tracker (this file) does NOT relitigate legacy items; references to legacy items appear inline in `_root/09_changelog.md` entries or in Stage 5 paste-ready prompts when relevant.

**Selected legacy items with Stage 5 relevance** (audit-trail; not action items here):

- **CL-026 + CL-023 RESOLVED 2026-05-26** — v6.2 driver-stamp baseline at 91.6% clean; absorbed at `_root/05` source via Source-fix Session D 2026-05-27 follow-on. Stage 5 Phase 3c `_root/05` rewrite preserves the 91.6% baseline as input.
- **CL-027 RESOLVED 2026-05-26** — `_root/05 §2.1.2` reduction-direction sub-block addition. Stage 5 Phase 3c URN-driver authoring session inherits this resolution as input.
- **CL-028 RESOLVED 2026-05-26** — `_root/07 §4.5` AND-discipline tightening. `_root/07` stays per Stage 5 cut-line (handoff §3.1); this resolution is preserved.
- **CL-029 + CL-030 + CL-031 RESOLVED 2026-05-27** via Source-fix Session D — `_root/05` conversational-language trims + §4 weaving matrix full rebuild + `_root/00_manifest.md` REPLACING bloat trim. All absorbed pre-Stage-5; clean baseline.

---

*This document is the durable home of the Stage 5 CL-NNN tracker as of 2026-05-27. CL-NNN entries are append-only; RESOLVED items stay in the tracker for audit trail; do not delete or rewrite resolved entries.*
