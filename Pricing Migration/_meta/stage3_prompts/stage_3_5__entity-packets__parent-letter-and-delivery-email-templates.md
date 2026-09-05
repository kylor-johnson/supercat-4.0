# Stage 3.5 — Authoring Prompt for `entity-packets/_parent-letter-template.md` + `_parent-letter-delivery-email-template.md`

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-26 by planning agent immediately post Stage 3.4 closeout per pattern-inheritance-compounds discipline. Inherits Stage 3.1 + Stage 3.2 + Stage 3.3 + Stage 3.4 pattern conventions + strict-placeholder precedent + "pricing" subject convention + path-reference contract. **Operator stamps applied 2026-05-26 before paste** (Stage 3.5 scope-decision pass + Stage 3.5 prep pass):
>   - `_master-entity-data-v6.2.csv` Master Entity tab promoted as canonical entity-level scope source (dual-canonical v6.2 architecture with `_master-account-data-v6.2.csv` per `_root/06 §1.6`).
>   - `_root/04 §4.15` Parent-letter voice register authored at source (6 sub-sections; voice fork by `delivery_owner` with CEO-delivered + Kylor-delivered Head of Customer Success variants; multi-brand portfolio acknowledgment; cross-brand consolidation lens; per-brand mechanics restraint; default-only pricing posture; routing pointer to per-child notices).
>   - Cross-format CSM-role note at `_root/04 §4.15.1` — SuperCat's CSM support role does NOT handle migration conversations; "CSM-sent" role-marker filled by Kylor in HoCS role across all 5 Stage 3 templates.
>   - `_root/06 §1.6` rewritten with canonical 14-entity scope (13 rollup + 1 standalone_multi_org); Ferguson Enterprises mixed-direction one-off exception documented; Stage 3.5 template scope = 13 entities (12 increase-side rollup + 1 standalone_multi_org Maxim).
>   - Default-only pricing posture per `_root/04 §4.15.5` — `consolidated_delta` / `consolidation_saving` INTERNAL-ONLY.
>   - `one_template_two_voices` packet structure: single template with `[VOICE FORK: CEO_DELIVERED | KYLOR_DELIVERED]` selector.
>   - 48-hour two-stage sequencing per `_root/04 §4.15.6` (parent letter Day 0; per-child notices Day 1–Day 2).
>   - **STRICT + paste-verification manifest-echo language** per CL-024 — fresh agent must paste-quote operator-stamped rule text in conformance block (NOT just cite section numbers).
> **Output target**: TWO new files under a NEW folder at `Pricing Migration/entity-packets/`:
>   - `entity-packets/_parent-letter-template.md` (the structural skeleton for every Stage 4 per-entity parent letter — voice fork by `delivery_owner`; default-only pricing posture; multi-brand portfolio acknowledgment; cross-brand consolidation lens; per-brand mechanics restraint; closes with routing pointer to per-child notices)
>   - `entity-packets/_parent-letter-delivery-email-template.md` (the cover email that wraps every parent letter at delivery; CEO-sent OR Kylor-sent per `delivery_owner` fork)
> **Estimated authored length**: parent-letter template 350–450 lines (entity-packet carries 6 sub-section voice rules via path-reference, member-brand enumeration table, default-pricing summary, cross-brand consolidation lens block, per-brand narrative threading list, no per-brand mechanics, no per-brand pricing tables, voice-fork selector renders); delivery email template 150–200 lines (CEO-delivered + Kylor-delivered subject + body forks; routing block subset per CL-022 inference).
> **Dependency**: Stage 5 complete (`_root/00`–`_root/09` all authored and operator-stamped); `_root/04 §4.15` operator-stamped 2026-05-26 at source (Stage 3.5 prep); `_root/06 §1.6` rewritten 2026-05-26 at source (Stage 3.5 prep); `_master-entity-data-v6.2.csv` imported 2026-05-26 as canonical entity-level scope source (Stage 3.5 prep). Independent of Stage 3.1 / 3.2 / 3.3 / 3.4. **Pattern inheritance from all four prior Stage 3.X waves**: consult Format A + Format B + CEO Letter + Good News approved template sets for structural-convention reference only. Do NOT lift per-account driver content, per-child pricing tables, or per-child close text — those are per-child territory per `_root/04 §4.15.4`.

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. That is **load-bearing** for this prompt. `entity-packets/_parent-letter-template.md` is the structural skeleton every Stage 4 per-entity drafting agent fills in to produce a parent letter for a multi-brand entity (rollup) or standalone multi-org entity. The parent letter is sent BEFORE per-child notices in a two-stage sequence (parent letter Day 0; per-child notices Day 1–Day 2 within 48 hours of parent letter — per `_root/04 §4.15.6` operator-stamped 2026-05-26).

The companion `_parent-letter-delivery-email-template.md` is the cover email that wraps the completed parent letter at delivery time. Like the parent letter, the delivery email has TWO voice forks determined by the Master Entity tab `delivery_owner` column:

- **CEO-delivered fork** (4 entities; `delivery_owner = CEO`): CEO-to-CEO peer-to-peer voice; CEO signs.
- **Kylor-delivered fork** (10 entities; `delivery_owner = Kylor` — 9 rollup + 1 standalone_multi_org Maxim; Ferguson Enterprises is Kylor-delivered but excluded from Stage 3.5 template scope per `_root/06 §1.6` mixed-direction exception): SuperCat Head of Customer Success direct-relationship voice; Kylor signs ("Kylor Johnson, Head of Customer Success" per operator stamp 2026-05-26).

Your job is to **author two new template files that reference `_root/` rules by §-number and never restate them.** This is the single most important discipline of this entire task. Every voice rule, every forbidden phrase, every voice-fork variant, every routing condition, every quality check lives in exactly one `_root/` doc. The templates carry only:

- **Drafter-facing structural scaffolding** — the operator-notes blockquote header, the routing block format (with entity-level fields per `_root/07 §7` inferred subset — see Step 4 + CL-022), the section headings, the bracketed placeholders the drafter fills in from data, the member-brand enumeration table, the cross-brand consolidation lens block, the per-brand narrative threading list, the `[VOICE FORK: ...]` selector.
- **Lookup instructions** — pointers like `[INSERT _root/04 §4.15.1 CEO-delivered voice fork — verbatim]`. The drafter at draft time copies the verbatim block from the owning `_root/` doc into the parent letter; the template does not carry the prose.
- **Conditional flow logic** — `[IF delivery_owner = CEO: use §4.15.1 CEO-delivered fork | IF delivery_owner = Kylor: use §4.15.1 Kylor-delivered fork]`. The conditions reference Master Entity tab columns by name (per `_root/07 §2`); the resulting block is a pointer to `_root/04 §4.15.X`, not inline prose.

If you find yourself about to paste verbatim prose from `_root/03`, `_root/04` (including ANY part of `§4.15.1`–`§4.15.6`), `_root/05`, or `_root/06` into the template, **stop**. That is exactly the drift the path-reference contract (`_root/CONTRACTS.md §5`) was written to prevent. The strict-placeholder precedent operator-stamped 2026-05-26 (Stage 3.1 review pass) applies in full to all six `_root/04 §4.15` sub-sections.

You will not invent new rules. You will not loosen, summarize, or "improve" any existing rule. You will not extend the template's scope beyond what `_root/06 §1.6` defines the entity-packet program to be (13 entities in Stage 3.5 template scope per operator stamp 2026-05-26; 14 total per Master Entity tab with Ferguson Enterprises excluded as mixed-direction one-off per operator stamp `defer` 2026-05-26).

You will not author per-child notices in this task. Per-child notices use the Stage 3.1–3.4 standalone-format templates (Format A / Format B / CEO Letter / Good News), each child routed to its natural format per `_root/06 §2`–§3. Your scope is ONLY the parent-letter artifact.

---

## Step 1: Required reading (in this exact order) — STRICT MANIFEST-ECHO CONTRACT

**Reading file mtimes is NOT the manifest echo.** The manifest echo requires reading the `_root/00_manifest.md §2` table AND reading every `_root/` doc's header block AND echoing each doc's title + Last-updated date from the header in your first chat response. **A pre-existing artifact in the workspace (e.g. a template authored in a prior session, a sibling format's approved templates) is NOT a substitute for re-reading the canonical rule layer.** If you cannot produce the canonical manifest echo, your session is not ready to author; STOP and flag per `_root/CONTRACTS.md §2`.

**This is CL-024 strengthening** (operator-stamped 2026-05-26 in response to a Stage 3.4 fresh-agent manifest-echo skip). Stage 3.5 is the heaviest fresh-agent task in the program — no archived template precedent; thinner rule-layer support than 3.1–3.4 in some surfaces; more new architectural pieces than any prior Stage 3.X wave. Drift here is the most expensive.

**Additionally — paste-verification requirement (CL-024)**: in your conformance block, you must paste-quote the FULL TEXT of the following operator-stamped rule passages, verbatim from the `_root/` docs (not paraphrased, not summarized, not just cited):

1. `_root/04 §4.15.1` — the CEO-delivered fork bullet-list AND the Kylor-delivered fork bullet-list AND the cross-format CSM-role note paragraph.
2. `_root/04 §4.15.5` — the default-pricing posture rationale paragraph AND the terminology constraint paragraph.
3. `_root/04 §4.15.6` — the CEO-delivered close blockquote AND the Kylor-delivered close blockquote AND the 48-hour timing paragraph.
4. `_root/06 §1.6` — the 14-entity enumeration block AND the Ferguson Enterprises exception paragraph AND the Stage 3.5 template scope paragraph.

If you cannot paste-quote any of these passages because the rule text is not present at the cited location, STOP and flag per QB-125 propagation-failure rule. Do NOT proceed to authoring.

### Folder orientation (mandatory — echo in conformance block per `_root/00_manifest.md §6`)

1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/00_manifest.md` — the index. **The §2 manifest table is the authoritative list of every `_root/` doc; you echo it in your first chat response per the manifest-echo contract in §1 step 6. ALL ENTRIES, NOT A SUBSET.**
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md`
5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/09_changelog.md` — read every entry. **Particularly important for Stage 3.5**:
    - Wave 2 Q4 (CL-005 — "What's Coming in 2026" in ALL formats including entity-packet parent letter; ADDITIVE in the parent letter via `_root/03 §3` pointer where appropriate to entity-level framing — flag in conformance block if scope unclear).
    - Wave 1 (peer-dollars universal-strip + competitor-pricing broadening — apply to parent letter).
    - Stage 3.4 review pass + closeout lede normalization 2026-05-26 (CL-024 filed; lede normalized "invoice"→"pricing" — extends to parent-letter lede pattern; cross-format consistency).
    - **Stage 3.5 prep 2026-05-26** (this entry — read in FULL; documents the dual-canonical v6.2 architecture, `_root/04 §4.15` authoring, `_root/06 §1.6` rewrite, CL-014 resolution, CL-015 location update, Ferguson Enterprises exception, and Stage 3.5 template scope).

### The rule layer — read in FULL

6. `_root/01_why_we_are_migrating.md` — strategic register. Entity packets carry the multi-brand consolidation framing (`_root/04 §4.15.3`) — the strategic register applies at the portfolio level, not the per-brand level.
7. `_root/02_who_is_being_migrated.md` — **For entity packets**: §3 entity overlay (entity-children fold into entity packets — no standalone briefs for the children of the 13 in-scope entities); §4 health overrides (Watch-band carve-out still applies at the child level for Good News routing); §5 annual overlay (mixed-segment entities — `has_annual = TRUE` triggers the §4.15.3 deal-type heterogeneity acknowledgment; timing follows ≥90-day window for Annual children; substance stays per-child format).
8. `_root/03_what_we_sell.md` — **For entity packets**: Section 3 "What's Coming in 2026" verbatim block is per-child territory (each child notice carries the §3 verbatim block per Wave 2 Q4 CL-005); the parent letter does NOT carry tier verbatim blocks or "What You're Getting at $X" prose (per `_root/04 §4.15.4` per-brand mechanics restraint — tier feature lists are per-child territory).
9. `_root/04_communication_posture.md` — **For entity packets**:
    - §1 voice posture (peer-to-peer or vendor-to-principal — never service-rep-to-buyer; applies to both fork variants).
    - §2 non-negotiables (apply at entity level; lede stat guardrail per §4.2 applies — relationship sentence comes BEFORE the entity-level delta per §4.15.2).
    - §3 forbidden-phrase rows (apply at entity level — no peer dollars; no competitor pricing; no expansion language; no gift/reward/apology).
    - **§4.15 (the central rule package for this template)** — read all 6 sub-sections in FULL. Paste-verify in conformance block per CL-024:
        - §4.15.1 — Voice fork by `delivery_owner` (CEO-delivered + Kylor-delivered HoCS variants; cross-format CSM-role note).
        - §4.15.2 — Multi-brand portfolio acknowledgment (opening framing).
        - §4.15.3 — Cross-brand consolidation lens (program framing block).
        - §4.15.4 — Per-brand mechanics restraint (parent-letter exclusions).
        - §4.15.5 — Default-pricing posture (default_only; terminology constraint).
        - §4.15.6 — Routing pointer to per-child notices (closing transition; 48-hour timing).
10. `_root/05_driver_taxonomy.md` — **Read for orientation only**. Per-driver mechanics live in per-child notices per `_root/04 §4.15.4`. The parent letter does NOT carry driver mechanic blocks. Read §3 (decrease-side drivers) only to confirm Ferguson Enterprises decrease-side child (`ml`) routes to Good News per the exception note in §1.6; the entity-packet template does NOT cover this case.
11. `_root/06_format_routing.md` — **§1.6 is the central rule for this template** (rewritten 2026-05-26; read in FULL; paste-verify in conformance block per CL-024). Also read §1 (4 brief formats + 2 routing patterns); §2 routing-decision flow (entity overlay at step 3); §3 delta-tier dispatch (decrease-side row); §4.1 entity-overlay sub-section (updated 2026-05-26 with Master Entity `notice_cohort` distribution + §4.15 voice cross-reference); §4.2 health-override + HOLD-row tally annotation.
12. `_root/07_data_pipeline.md` — §2 field meanings (use Master Entity tab columns: `entity_name`, `entity_type`, `brands`, `mixed_tiers`, `multi_org_pct`, `legacy_discount_value`, `current_entity_mrr`, `default_mrr`, `default_delta`, `default_delta_pct`, `default_risk`, `consolidated_mrr`, `consolidated_delta`, `consolidated_delta_pct`, `consolidated_risk`, `consolidation_saving`, `consolidation_saving_pct`, `platform_tier`, `platform_charge`, `brand_charges`, `user_charges`, `weighted_health_score`, `billing_entities`, `paying_entities`, `has_annual`, `member_accounts`, `member_ord_ids`, `delivery_owner`, `notice_cohort`, `mixed_segment`, `entity_messaging_headline`); §6 file-naming (Stage 4 production: `entity-packets/<entity-slug>/<entity-slug>__parent-letter.md`); §7 per-format routing-block matrix — **entity-packet row does NOT yet exist** per CL-022 inference pattern; infer slim subset from Stage 3.1 / 3.2 / 3.3 / 3.4 precedent (Step 4 below; flag in conformance block).
13. `_root/08_quality_bar.md` — entity-packet-applicable QB-NNN checks only if your task requires QA awareness; cite IDs in checklist sections, do not restate check text.

### Canonical scope source files (NEW for Stage 3.5 — read both)

14. `_master-entity-data-v6.2.csv` (15 lines; CANONICAL entity-level scope source per `_root/06 §1.6` operator-stamped 2026-05-26) — read the header row + every data row. The 14 entities are: 13 rollup (`entity_type = rollup`) + 1 standalone_multi_org (`entity_type = standalone_multi_org`). The 13 Stage 3.5 template-scope entities are: Abaline, Coleto Brands, Creative Home Furniture, Gabriella White, Godinger Group, HVLG, Interlude Home, Jonathan Charles, Rock House Farm, Thesis, Visual Comfort & Co., WAC Group (12 increase-side rollup) + Maxim group Lighting (1 standalone_multi_org). Ferguson Enterprises is EXCLUDED per operator stamp `defer` 2026-05-26 on `mixed_direction_handling` (mixed-direction one-off; handled ad-hoc at Stage 4).
15. `_master-account-data-v6.2.csv` (346 lines; canonical account-level scope source for the Stage 3.1–3.4 standalone-format templates) — read for per-child data reference. The Master Entity tab's `member_ord_ids` column joins to this file's `ord_id` column. Per-child notices at Stage 4 production drafting draw from this file; the entity-packet parent letter draws from `_master-entity-data-v6.2.csv` and does NOT reproduce per-child data.

### Cleanup-tracker items the new template must address

16. `_meta/stage3_cleanup.md` — read in full; apply specifically to entity packets:
    - **CL-001** — confirm absent in parent letter (no "no account-specific adjustments" sentence; the parent letter is portfolio-level framing — there are no per-account adjustments to defensively name); reference `_root/04 §3` row.
    - **CL-003** — confirm absent (no peer dollar ranges at entity level; reference `_root/04 §3` row).
    - **CL-004** — confirm absent (no equivalent-platforms sentence; reference `_root/04 §3` row).
    - **CL-005** — flag in conformance block: "What's Coming in 2026" is per-child territory per `_root/04 §4.15.4` — the parent letter does NOT carry the roadmap verbatim block. Each child notice carries it independently per Wave 2 Q4. If the operator wants the parent letter to carry the roadmap section, flag for source-fix to `_root/04 §4.15` (operator stamp required).
    - **CL-014** — RESOLVED 2026-05-26 at Stage 3.5 prep (this template authoring is the resolution implementation; reference `_meta/stage3_cleanup.md` CL-014 entry for audit-trail).
    - **CL-022** — delivery email routing-block subset inferred per Stage 3.1 / 3.2 / 3.3 / 3.4 precedent + entity-packet-specific fields (see Step 4 Section 2; flag in conformance block).
    - **CL-024** — STRENGTHENED in Step 1 above (manifest-echo + paste-verification of operator-stamped rule text). This is the resolution implementation for CL-024.
    - **Other CL items**: CL-002, CL-006–CL-013, CL-015–CL-021, CL-023 — out of scope for entity packets; document as such in conformance block.

### Archive references (NO archived entity-packet template exists per CL-014 + `_root/06 §1.6`)

17. There is no archived entity-packet template to consult. Stage 3.5 is the first authoring of this artifact. The structural conventions you inherit come from the four approved Stage 3.X template sets (item 18 below) — pattern reference only, not lift-and-paste.

### Pattern reference from Stage 3.1 + 3.2 + 3.3 + 3.4 (required — all operator-approved 2026-05-26)

18. Read all eight approved template files in FULL:
    - `format-a-notices/_brief-template.md` + `_delivery-email-template.md`
    - `format-b-notices/_brief-template.md` + `_delivery-email-template.md`
    - `ceo-letter-notices/_brief-template.md` + `_delivery-email-template.md`
    - `good-news-notices/_brief-template.md` + `_delivery-email-template.md`

    **Match these 14 cross-format conventions exactly** (deviating produces operator review flags):
    1. Operator-notes blockquote header style (Section 1 in all four formats).
    2. Internal routing-note structure per `_root/07 §7` (Section 2 in all four formats — entity-packet inference subset per CL-022; Step 4 Section 2).
    3. Section-header convention: `> **Section N — ...**` blockquote at each section start (every Section header in every approved template).
    4. `>` blockquote convention for drafter-facing content (operator notes, routing block, voice calibration notes).
    5. QA-checklist `>` blockquote convention citing QB-NNN by number only (Section 4 in all four formats).
    6. Cross-references footer mapping every `_root/XX §N.M` the template touches.
    7. Strict-placeholder precedent operator-stamped 2026-05-26 (Stage 3.1 review pass — applies to ALL `_root/`-owned prose including short bracketed-token sentences; the parent letter's six `_root/04 §4.15.X` references are placeholders, NOT inlines).
    8. Section presence pattern (Section 0 file header / Section 1 operator notes / Section 2 routing / Section 3 brief or letter skeleton / Section 4 checklist / Section 5 voice calibration [delivery email only] / footer).
    9. Subject-line "pricing" convention — extends to parent-letter delivery email subject per operator stamp 2026-05-26 (Stage 3.4 closeout — lede normalization extends to all cross-format customer-facing pricing prose).
    10. `[ALL_CAPS_WITH_UNDERSCORES]` placeholder convention.
    11. Driver dispatch / voice fork table format (Format A/B/CEO Letter/Good News: driver dispatch by `migration_driver` value. **Entity-packet**: voice fork dispatch by `delivery_owner` value — adapt the table pattern to the voice-fork case).
    12. Pre-send checklist citation pattern (QB-NNN by number only; do not restate check text).
    13. Operator-notes blocks pattern (Do not send if / After sending blocks from archived templates where applicable).
    14. Lede-pattern convention: "Your monthly pricing is [changing/decreasing/increasing] from $X to $Y" — extends to entity-packet parent letter lede with portfolio-level framing per `_root/04 §4.15.2` ("Across [N] brands under [ENTITY_NAME], your monthly pricing is changing by $[DEFAULT_DELTA]/month — effective [EFFECTIVE_DATE]").

    **What you may legitimately deviate on** — only entity-packet-specific scope per Step 2: voice fork by `delivery_owner` (single template, two voice variants) replaces per-account driver dispatch; multi-brand portfolio acknowledgment replaces per-account opening; cross-brand consolidation lens replaces per-driver "Why the Number Is Changing" block; per-brand mechanics restraint replaces per-account driver blocks; default-only pricing posture replaces per-account pricing tables; routing pointer to per-child notices replaces per-account close commitment (or COMPLEMENTS it in CEO-delivered fork); 48-hour two-stage sequencing operator-stamped at `_root/04 §4.15.6`.

### Do NOT read

- Per-account exemplars (`format-*-notices/*__*/*__*.md` files at Stage 4 production scope) — these are stale or not yet authored under the new templates; out of scope for template authoring.
- Other format archives beyond the 8 approved templates in item 18.
- `_meta/stage2_prompts/**` and other `_meta/stage3_prompts/**` files beyond this prompt.
- `_reference/**` or `~/Downloads/**`.
- `_archive/**` entity-packet artifacts (none exist; the entity-packet template is new).

---

## Step 2: Authoritative entity-packet scope (use as fact — do not re-derive)

**Mechanical scope** (per `_root/06 §1.6` operator-stamped 2026-05-26):

- The entity-packet template targets the **13 unambiguously Stage-3.5-scope entities** per the Master Entity tab (`_master-entity-data-v6.2.csv`):

| # | entity_name | entity_type | brands | member_ord_ids | delivery_owner | notice_cohort | default_delta |
|---|---|---|---|---|---|---|---|
| 1 | Abaline | rollup | 2 | `asi \| mpc` | Kylor | June | +$410 |
| 2 | Coleto Brands | rollup | 2 | `prog \| kl` | Kylor | June | +$924 |
| 3 | Creative Home Furniture | rollup | 2 | `ta \| tam` | Kylor | June | +$715 |
| 4 | Gabriella White | rollup | 4 | `sc \| gh \| scw \| sccon` | **CEO** | June | +$1,862 |
| 5 | Godinger Group | rollup | 4 | `gsa \| rac \| ssi \| pw` | Kylor | June | +$1,856 |
| 6 | HVLG | rollup | 3 | `hvl \| tl \| cl` | Kylor | Post-Migration | +$2,435 |
| 7 | Interlude Home | rollup | 2 | `ih \| ihw` | Kylor | June | +$965 |
| 8 | Jonathan Charles | rollup | 2 | `jc \| jcusa` | **CEO** | June | +$1,368 |
| 9 | Rock House Farm | rollup | 2 | `cf \| hh` | **CEO** | Post-Migration | +$193 |
| 10 | Thesis | rollup | 2 | `eglo \| eglo_can` | **CEO** | June | +$764 |
| 11 | Visual Comfort & Co. | rollup | 4 | `fms \| vcg \| tla \| vce` | Kylor | June | +$1,316 |
| 12 | WAC Group | rollup | 2 | `wac \| sbl` | Kylor | June | +$1,417 |
| 13 | Maxim group Lighting | **standalone_multi_org** | 1 | `mli` | Kylor | June | +$312 |

- **Ferguson Enterprises** (rollup; 2 brands `mlg | ml`; net `default_delta = -$109/mo` mixed-direction) is **EXCLUDED** per operator stamp `defer` 2026-05-26 on `mixed_direction_handling`. `mlg` routes to its natural increase-side format per §2–§3 dispatch (likely Format B given Δ tier); `ml` routes to Good News per §3 row 1. A coordinated parent-letter wrapper for Ferguson is authored ad-hoc at Stage 4 if the operator judges it necessary. The entity-packet template does NOT cover Ferguson Enterprises.
- **Watch-band carve-out** (per `_root/06 §4.2`): applies at the CHILD level for per-child notices. The entity-packet parent letter is sent first regardless of any child's health band; per-child Watch / At-Risk / Critical handling is per-child territory.
- **Annual overlay** (per `_root/02 §5` + `_root/06 §4.3`): mixed-segment entities (`has_annual = TRUE` in Master Entity tab) acknowledge deal-type heterogeneity in the parent letter per `_root/04 §4.15.3`; per-child Annual notice timing follows ≥90-day renewal window per `_root/02 §5`. The entity-packet two-stage sequencing operates parallel to the Annual overlay — parent letter sends Day 0; Annual children's per-child notices follow within 48 hours BUT effective timing is renewal-based.

**Voice fork** (per `_root/04 §4.15.1` — paste-verify in conformance block):

- **CEO-delivered fork** (4 entities: Gabriella White, Jonathan Charles, Rock House Farm, Thesis) — CEO-to-CEO peer-to-peer voice; CEO signs; specific calendar date call commitment per §4.15.6 CEO-delivered close.
- **Kylor-delivered fork** (9 rollup entities + Maxim standalone_multi_org = 10 entities; Ferguson Enterprises is Kylor-delivered but EXCLUDED from Stage 3.5 template scope per `_root/06 §1.6` mixed-direction exception) — SuperCat Head of Customer Success direct-relationship voice; Kylor signs ("Kylor Johnson, Head of Customer Success" per operator stamp 2026-05-26); self-continuity close per §4.15.6 Kylor-delivered close (no specific calendar date; 48-hour follow-up commitment).

**Voice posture** (per `_root/04 §1` + `§4.15`):

- "Peer-to-peer or vendor-to-principal — never service-rep-to-buyer and never marketing-to-prospect." Both fork variants apply this posture.
- Lead with relationship-historicity sentence; delta in sentence 2 or later per §4.2 lede stat guardrail. **No** entity-level lede that opens with the dollar number.
- No apology for prior pricing. No expansion language. No peer dollars. No competitor pricing. All universal §2 + §3 prohibitions apply at the entity level.

**Pricing posture** (per `_root/04 §4.15.5` — paste-verify in conformance block):

- **default_only**: parent letter presents `default_mrr` / `default_delta` / `default_delta_pct` from the Master Entity tab. `consolidated_delta` / `consolidation_saving` / `consolidation_saving_pct` are **INTERNAL-ONLY** for CSM/CEO post-send conversation.
- No "consolidation savings opt-in" CTA in parent letter. No pointer sentence to the consolidated scenario. No soft mention.
- **Terminology constraint** (operator-stamped 2026-05-26): when `migration_driver = multi_org_retirement` (legacy multi-org discount retiring across a child brand), the parent letter MAY name the discount retirement in per-brand threading (§4.15.3) — that "consolidation" is the migration mechanic. The new consolidation_saving column is a different sense of "consolidation" (sales motion) — internal-only.

**Two-stage sequencing** (per `_root/04 §4.15.6` — paste-verify in conformance block):

- Day 0: parent letter sends.
- Day 1–Day 2: per-child notices send within 48 hours of parent letter. Per-child notices use the Stage 3.1–3.4 standalone-format templates (per-child format determined by §2–§3 dispatch on the child's individual Δ tier).
- The 48-hour window is operator-stamped 2026-05-26 as canonical Stage 3.5 timing.

**Routing block** (per `_root/07 §7` inferred subset per CL-022; entity-packet row does NOT yet exist in §7):

- General fields through `Comm_action` (substitute entity-level fields: `entity_name`, `entity_type`, `member_ord_ids`, `default_mrr / default_delta`).
- `CEO awareness required before send: YES` (CEO authors CEO-delivered fork; CEO reviews + approves Kylor-delivered fork per `_root/06 §1.6` operator-stamped 2026-05-26).
- `delivery_owner: [CEO | Kylor]` — required (Master Entity tab column; drives voice fork).
- `notice_cohort: [June | Post-Migration]` — required (Master Entity tab column; drives timing).
- `member_accounts: [PIPE_SEPARATED_BRAND_NAMES]` — required (Master Entity tab `member_accounts` column).
- `member_ord_ids: [PIPE_SEPARATED_ORD_IDS]` — required (Master Entity tab `member_ord_ids` column).
- `has_annual: [TRUE | FALSE]` — required (drives §4.15.3 deal-type heterogeneity acknowledgment).
- `mixed_tiers: [YES | No]` — required (drives §4.15.3 tier heterogeneity acknowledgment).
- `mixed_segment: [LABEL or empty]` — required (drives §4.15.3 segment heterogeneity acknowledgment).
- `multi_org_pct + legacy_discount_value`: required (internal context for terminology constraint per §4.15.5 — distinguishing legacy multi_org_retirement migration mechanic from new consolidation_saving).
- `consolidated_delta + consolidation_saving + consolidation_saving_pct`: **INTERNAL-ONLY** routing-block fields (NOT in customer copy per §4.15.5).
- `weighted_health_score`: internal context; per-child health-band drives per-child Watch-band carve-out (not parent-letter routing).
- Per-child notice format per child (e.g. `hvl → Format B`; `tl → Format A`; `cl → CEO Letter`): required for Stage 4 production drafting cross-reference; one row per child.
- `Parent-letter send date (Day 0): [DATE]` + `Per-child notices send window (Day 1–Day 2): [DATE_RANGE]`: required for 48-hour sequencing.
- **OMIT** Postgres live-data line — entity-packet template draws from Master Entity tab + per-child rows in Master Account tab; not a single per-account Postgres query.
- Conditional rows per standard `_root/07 §7` convention (support fire across any child; entity-level CSM assignment if relevant).

**Authorship** (per `_root/04 §4.15.1` cross-format CSM-role note — paste-verify in conformance block):

- CEO-delivered fork: SuperCat CEO sends + signs.
- Kylor-delivered fork: Kylor sends + signs; "Kylor Johnson, Head of Customer Success" signature line per operator stamp 2026-05-26.
- **SuperCat's CSM support role does NOT handle migration conversations**. The "CSM-sent" role-marker in `_root/06 §1` + `_root/02 §2` (and in the existing Format A / Format B / Good News approved templates) is filled by Kylor in HoCS role in practice across all 5 Stage 3 templates for the migration program. This cross-format note is codified at `_root/04 §4.15.1`.

**Operator-stamped subject + signature conventions (2026-05-26)**:

- Parent-letter title (Section 3a): `# [ENTITY_NAME]: Your Pricing Is Changing` (mirrors Format A / B / CEO Letter title convention; "Changing" because entity-level direction is increase for 12 of 13 in-scope entities; Maxim standalone_multi_org is also increase — all 13 in-scope entities are increase-side per Step 2 mechanical scope).
- Delivery email subject: `[ENTITY_NAME]: your SuperCat pricing is changing — effective [EFFECTIVE_DATE]` (mirrors Stage 3.1 / 3.2 / 3.3 "pricing is changing" form).
- Signature:
  - CEO-delivered fork: `[CEO_NAME], CEO, SuperCat` (or similar — CEO's title at SuperCat).
  - Kylor-delivered fork: `Kylor Johnson, Head of Customer Success, SuperCat` (operator-stamped 2026-05-26).

---

## Step 3: What you are authoring — file 1 of 2: `entity-packets/_parent-letter-template.md`

Author the parent-letter template as the following sections, in this order. **Every section either contains pure scaffolding OR a §-pointer. NO rule prose is inlined — including ALL six `_root/04 §4.15` sub-sections.**

### Section 0 — File header

```
# Entity-Packet Parent Letter — Template
*Two-stage entity-packet program (Day 0 parent letter; Day 1–2 per-child notices) per `_root/06 §1.6` | Voice fork by `delivery_owner` per `_root/04 §4.15.1` | Default-only pricing posture per `_root/04 §4.15.5`*
```

### Section 1 — Operator notes (drafter-facing, removed before sending)

A `>` blockquote block naming:

- When to use (cite `_root/06 §1.6` — 13 entity-packet template-scope entities; reference Master Entity tab `_master-entity-data-v6.2.csv` as canonical scope source).
- Who sends (CEO for 4 entities; Kylor in HoCS role for 9 rollup + 1 standalone_multi_org = 10 entities; cite `_root/04 §4.15.1` voice fork + cross-format CSM-role note; cite `_root/06 §1.6` `delivery_owner` column).
- Voice fork rendering instructions (`[VOICE FORK: CEO_DELIVERED | KYLOR_DELIVERED]` selector — drafter renders ONE fork per parent letter based on Master Entity tab `delivery_owner` value; the template carries both fork variants in `[IF delivery_owner = CEO: ... | IF delivery_owner = Kylor: ...]` conditional structure per Step 3 sections below).
- What this template is NOT for: Ferguson Enterprises mixed-direction one-off (excluded per operator stamp 2026-05-26 — see `_root/06 §1.6` exception note); standalone-account routing (Format A / B / CEO Letter / Good News — separate templates); per-child notices (per-child templates are Stage 3.1–3.4, NOT this template).
- Cleanup-tracker history:
  - CL-001 / CL-003 / CL-004 — confirmed absent at entity-level + referenced (cite `_root/04 §3` rows).
  - CL-005 — FLAGGED: roadmap section is per-child territory per `_root/04 §4.15.4`; parent letter does NOT carry the "What's Coming in 2026" verbatim block. If operator wants it in parent letter, source-fix to `_root/04 §4.15` required.
  - CL-014 — RESOLVED at Stage 3.5 prep 2026-05-26 (this template authoring is the resolution implementation).
  - CL-022 — delivery email routing-block subset inferred (Section 2 + Step 4 Section 2; flag in conformance block).
  - CL-024 — STRENGTHENED in Step 1 of this prompt (manifest-echo + paste-verification of operator-stamped rule text; this template authoring is the resolution implementation).
- Length target: 250–350 words (cite Format A / B / CEO Letter / Good News operator-notes lengths as pattern reference; entity-packet operator notes are denser because of voice-fork rendering + dual-canonical v6.2 architecture).
- **Two-stage sequencing block** (operator-stamped 2026-05-26 per `_root/04 §4.15.6`): Day 0 parent letter sends; Day 1–Day 2 per-child notices send within 48 hours. The drafter coordinates the 48-hour window with CS-team scheduling at Stage 4 production drafting time.
- **Do not send if** block: any of the 13 in-scope entities lacks Master Entity tab data (`member_ord_ids` empty, `default_delta` empty, `delivery_owner` empty, `entity_messaging_headline` empty); per-child notices not yet drafted (parent letter MUST send first; per-child notices follow within 48 hours per `_root/04 §4.15.6`); CEO not yet aware of CEO-delivered fork content (per `_root/06 §1.6` `CEO awareness required before send: YES`).
- **After sending** block: log Day 0 send date; coordinate Day 1–Day 2 per-child notice send window; track per-child notice send confirmations against the 48-hour window; if any child notice slips past 48 hours, flag to operator (the 48-hour sequencing is operator-stamped per `_root/04 §4.15.6`; revising requires `_root/CONTRACTS.md §3` rule-change protocol).

### Section 2 — Internal routing block (drafter-facing, removed before sending)

A `>` blockquote with the entity-packet routing block fields per Step 2 routing-block specification. **Inferred subset per CL-022 — flag in conformance block pending `_root/07 §7` Wave 6 batch authoring the canonical entity-packet row.**

Structure:

- `Brief type: entity_packet_parent_letter | Program: CEO-Led Entity Pre-Engagement → Coordinated Notices (per _root/06 §1.6)`
- `Entity name: [ENTITY_NAME] | Entity type: [rollup | standalone_multi_org] | Brands count: [N]`
- `Member accounts: [PIPE_SEPARATED_BRAND_NAMES]`
- `Member ord_ids: [PIPE_SEPARATED_ORD_IDS]`
- `Delivery owner: [CEO | Kylor]` — drives voice fork per `_root/04 §4.15.1`
- `Notice cohort: [June | Post-Migration]` — drives timing per `_root/02 §5` + `_root/06 §1.6`
- `has_annual: [TRUE | FALSE]` — drives §4.15.3 deal-type heterogeneity acknowledgment
- `mixed_tiers: [YES | No]` — drives §4.15.3 tier heterogeneity acknowledgment
- `mixed_segment: [LABEL | empty]` — drives §4.15.3 segment heterogeneity acknowledgment
- `multi_org_pct: [N%] | legacy_discount_value: $[N]` — internal context for terminology constraint per §4.15.5
- `current_entity_mrr: $[CURRENT_ENTITY_MRR] | default_mrr: $[DEFAULT_MRR] | default_delta: $[DEFAULT_DELTA] | default_delta_pct: [N]% | default_risk: [LABEL]`
- `consolidated_mrr: $[CONSOLIDATED_MRR] | consolidated_delta: $[CONSOLIDATED_DELTA] | consolidation_saving: $[N] | consolidation_saving_pct: [N]%` — **INTERNAL-ONLY** per `_root/04 §4.15.5`; NOT in customer copy
- `weighted_health_score: [N] | weighted health band: [LABEL]` — internal context
- `Per-child format dispatch table` — required list of each child's routed format (per `_root/06 §2`–§3 dispatch on child's individual Δ tier), e.g.:

  | child ord_id | child name | child Δ tier | routed format | Stage 4 per-child template |
  |---|---|---|---|---|
  | `[ORD_ID]` | `[BRAND_NAME]` | `[$X / N%]` | `[Format A | Format B | CEO Letter | Good News]` | `[format-X-notices/_brief-template.md]` |
  
- `Parent-letter send date (Day 0): [DATE]`
- `Per-child notices send window (Day 1–Day 2): [DATE] – [DATE]`
- `CEO awareness required before send: YES` (always for entity packets per `_root/06 §1.6` operator stamp 2026-05-26)
- `Expansion eligible: [YES | NO]` — Master Entity tab signal (cite if Master Entity tab carries it; flag in conformance block if not present)
- **OMIT** Postgres live-data line per Step 2 routing-block specification

Conditional rows per standard `_root/07 §7` convention (support fire across any child; entity-level CSM assignment; tenure acknowledgment at entity level if applicable).

### Section 3 — Parent-letter content skeleton

#### 3a. Subject / parent-letter title (per Step 2 operator stamp 2026-05-26)

`# [ENTITY_NAME]: Your Pricing Is Changing` + `*Effective [EFFECTIVE_DATE]*`

#### 3b. Opening greeting (voice-fork conditional)

```
[IF delivery_owner = CEO:]
Dear [RECIPIENT_FIRST_NAME],

[IF delivery_owner = Kylor:]
Hi [RECIPIENT_FIRST_NAME],
```

The greeting is drafter-generated per voice fork. CEO-delivered uses formal `Dear`; Kylor-delivered uses direct-relationship `Hi` (matching the HoCS direct-relationship register per `_root/04 §4.15.1`).

#### 3c. Multi-brand portfolio acknowledgment (opening framing per `_root/04 §4.15.2`)

`[INSERT _root/04 §4.15.2 multi-brand portfolio acknowledgment rule — RENDER as drafter-generated prose following the §4.15.2 required-content list:]`

- Every member brand named (use `member_accounts` column from Master Entity tab — pipe-separated; render as natural-language list).
- Total entity impact in a single dollar number after relationship sentence (per §4.2 lede stat guardrail).
- Relationship-historicity construction (use `cohort_year` from earliest member brand if cross-referenced from Master Account tab; entity-level cohort_year if available).

Pattern (drafter-generated; do NOT lift verbatim — §4.15.2 specifies REQUIRED CONTENT, not exact wording):

`We've worked with the [ENTITY_NAME] portfolio since [YEAR] — [MEMBER_BRAND_LIST_NATURAL_LANGUAGE]. As part of standardizing pricing across our install base in 2026, your monthly pricing across these [N] brands is changing by $[DEFAULT_DELTA]/month — effective [EFFECTIVE_DATE].`

#### 3d. Cross-brand consolidation lens (program framing block per `_root/04 §4.15.3`)

`[INSERT _root/04 §4.15.3 cross-brand consolidation lens rule — RENDER as drafter-generated prose following the §4.15.3 required-content list:]`

- Structural reason for coordinated communication (one paragraph).
- Deal-type heterogeneity acknowledgment IF `has_annual = TRUE` OR `mixed_segment` is populated (conditional paragraph).
- Tier heterogeneity acknowledgment IF `mixed_tiers = YES` (conditional paragraph).
- Per-brand narrative threading via `entity_messaging_headline` column (compact list — one sentence per brand naming the brand + the headline snippet from Master Entity tab).

`[IF has_annual = TRUE OR mixed_segment populated: INSERT_DEAL_TYPE_HETEROGENEITY_PARAGRAPH per §4.15.3 required content]`

`[IF mixed_tiers = YES: INSERT_TIER_HETEROGENEITY_PARAGRAPH per §4.15.3 required content]`

`[INSERT_PER_BRAND_NARRATIVE_THREADING_LIST — one sentence per member brand drawing from Master Entity tab `entity_messaging_headline` column; format as compact bulleted list with brand name + headline snippet]`

#### 3e. Per-brand mechanics restraint (NOT a section; this is a CONSTRAINT — per `_root/04 §4.15.4`)

The parent letter does NOT carry per-brand mechanics. Per-brand drivers, "Why the Number Is Changing" prose, tier feature lists, pricing tables, value-anchor sections, and per-brand call commitments are ALL per-child territory per `_root/04 §4.15.4`. The template does NOT carry any of these blocks in any section.

If you find yourself authoring per-brand mechanic blocks in this template, STOP — that is `_root/04 §4.15.4` drift territory. Per-brand mechanics live in per-child notices, not in the parent letter.

#### 3f. Default-pricing summary block (per `_root/04 §4.15.5`)

`[INSERT _root/04 §4.15.5 default-pricing posture rule — RENDER as the default-only entity-level pricing summary; consolidated_delta / consolidation_saving NOT in customer copy:]`

A 4-row entity-level summary table (NOT a per-brand pricing table — that's per-child territory):

| | Current | New (effective [EFFECTIVE_DATE]) |
|---|---|---|
| **Monthly entity total** | $[CURRENT_ENTITY_MRR] | **$[DEFAULT_MRR]** |
| **Annual entity total** | $[CURRENT_ENTITY_MRR × 12] | **$[DEFAULT_MRR × 12]** |
| **Change** | — | +$[DEFAULT_DELTA]/month (+[DEFAULT_DELTA_PCT]%) |
| **Effective date** | — | [EFFECTIVE_DATE] |

**Do NOT** add a consolidated-scenario row, a consolidation-savings row, or any reference to the `consolidated_delta` / `consolidation_saving` columns. Those are INTERNAL-ONLY per `_root/04 §4.15.5`.

#### 3g. Closing transition (routing pointer to per-child notices per `_root/04 §4.15.6` — voice-fork conditional)

```
[IF delivery_owner = CEO:]
[INSERT _root/04 §4.15.6 CEO-delivered close — verbatim blockquote]

[IF delivery_owner = Kylor:]
[INSERT _root/04 §4.15.6 Kylor-delivered close — verbatim blockquote]
```

Per `_root/04 §4.15.6`:

- CEO-delivered close carries specific calendar date within 5 business days of send per `_root/04 §4.12` CEO Letter close convention (3-location date parity contract applies — date in parent-letter close MUST match parent-letter routing block AND parent-letter delivery email routing block per operator stamp 2026-05-26 Stage 3.3 review pass).
- Kylor-delivered close uses self-continuity "from me" + 48-hour soft commitment + reply-directly-to-this-email accessibility.

#### 3h. Signature (voice-fork conditional)

```
[IF delivery_owner = CEO:]
[CEO_NAME], CEO, SuperCat

[IF delivery_owner = Kylor:]
Kylor Johnson, Head of Customer Success, SuperCat
```

Signature per Step 2 operator stamp 2026-05-26 (`Kylor Johnson - Head of Customer Success`).

### Section 4 — Pre-send drafter checklist

`>` blockquote pointing to `_root/08`. Cite 10–14 entity-packet-applicable QB-NNN checks by number only — e.g. QB-002 (path-reference contract), QB-046 (data-pipeline source-of-truth — Master Entity tab + Master Account tab joined via `member_ord_ids` ↔ `ord_id`), QB-059 (no "no account-specific adjustments"), QB-085 (no peer dollars), QB-086 (close convention — CEO-delivered fork carries specific calendar date; Kylor-delivered fork does NOT), QB-119 (path-reference contract verification), QB-125 (propagation failure if `_root/04 §4.15` rule text absent at read time). Do NOT restate check text.

Entity-packet-specific QB additions to flag in conformance block (since `_root/08` does NOT yet enumerate entity-packet-applicable QB-NNN values — entity-packet-specific QB checks are inferred):

- Voice-fork rendering check: parent letter uses exactly ONE fork (CEO-delivered OR Kylor-delivered), not both, per `delivery_owner` value.
- Per-brand-mechanics-restraint check: parent letter does NOT carry per-brand driver blocks, tier feature lists, pricing tables, value-anchor sections, or per-brand call commitments (`_root/04 §4.15.4`).
- Default-only pricing posture check: parent letter does NOT mention `consolidated_delta` / `consolidation_saving` / consolidation savings opportunity (`_root/04 §4.15.5`).
- 48-hour two-stage sequencing check: per-child notice send window planned within 48 hours of parent-letter send date (`_root/04 §4.15.6`).
- Member-brand enumeration check: every member brand named in Section 3c per Master Entity tab `member_accounts` column (`_root/04 §4.15.2`).
- Cross-format CSM-role note check: Kylor-delivered fork signature uses "Head of Customer Success" title, NOT "CSM" generic role (`_root/04 §4.15.1`).

Cross-references footer mapping every `_root/XX §N.M` the template touches (expected: `_root/00 §5`, `_root/02 §3` + §5, `_root/03 §3`, `_root/04 §1` + §2 + §3 + §4.2 + §4.15 [all 6 sub-sections], `_root/05 §3` [orientation only], `_root/06 §1.6` + §3 + §4.1, `_root/07 §2` + §6 + §7, `_root/08`, `_root/CONTRACTS.md §2` + §3 + §5).

---

## Step 4: What you are authoring — file 2 of 2: `entity-packets/_parent-letter-delivery-email-template.md`

Uniform parent-letter + delivery-email pattern (operator-stamped 2026-05-26 per Stage 3.5 prep — same packet_structure as Stage 3.4 Good News). Voice fork by `delivery_owner` per `_root/04 §4.15.1`.

### Section 0 — File header

```
# Entity-Packet Parent Letter — Delivery Email Template
*CEO-sent OR Kylor-sent (HoCS) per `delivery_owner` voice fork per `_root/04 §4.15.1` | Wraps the parent letter; voice fork mirrors parent-letter fork*
```

### Section 1 — Operator notes

A `>` blockquote covering:

- When to use (cite `_root/06 §1.6` — wraps every entity-packet parent letter at delivery time; voice fork mirrors parent-letter fork; do NOT use this email template independent of the parent-letter artifact).
- Who sends (CEO for 4 entities; Kylor in HoCS role for 10 entities; cite `_root/04 §4.15.1`).
- Length: 4–6 sentences (entity-packet delivery emails are denser than per-account because they introduce the multi-brand parent letter + signal the 48-hour per-child notice cadence).
- What is NEVER in this email (cite `_root/04 §3` rows — gift/reward framing, apology, expansion language, percentage in lede, health-band names, peer dollars, competitor pricing; `_root/04 §4.15.4` — no per-brand mechanics, no per-child pricing detail, no per-child call commitments; `_root/04 §4.15.5` — no consolidated-savings opportunity).
- Attach parent letter PDF per `_root/07 §6`.
- 48-hour per-child notice signal: the email body MUST include the routing pointer to per-child notices per `_root/04 §4.15.6` — the recipient must know per-brand notices are coming within 48 hours.

### Section 2 — Internal routing block

Slim subset inferred per CL-022 (Stage 3.1 / 3.2 / 3.3 / 3.4 precedent + parent-letter Section 2 + entity-packet-specific fields). Include: Brief type, Entity / Type / Brands count, Member accounts, Member ord_ids, Delivery owner, Notice cohort, Current entity MRR / New MRR / Delta(positive), Effective date, Parent-letter send date (Day 0), Per-child notices send window (Day 1–Day 2), Attachment (parent letter PDF), CEO awareness: YES (always). Flag in conformance block that the subset is inferred pending `_root/07 §7` Wave 6 batch authoring the canonical entity-packet row.

### Section 3 — Email body skeleton

- **Subject** (per Step 2 operator stamp 2026-05-26): `[ENTITY_NAME]: your SuperCat pricing is changing — effective [EFFECTIVE_DATE]`

- **Greeting** (voice-fork conditional):
  ```
  [IF delivery_owner = CEO:]
  Dear [RECIPIENT_FIRST_NAME],

  [IF delivery_owner = Kylor:]
  Hi [RECIPIENT_FIRST_NAME],
  ```

- **Sentence 1 (drafter-generated, mirror parent-letter Section 3c)**: relationship-historicity + entity-level delta lede.

  Pattern: `We've worked with the [ENTITY_NAME] portfolio since [YEAR] — across [N] brands. Your monthly pricing across these brands is changing by $[DEFAULT_DELTA]/month — effective [EFFECTIVE_DATE]; the attached letter walks through the portfolio-level framing.`

- **Sentence 2 (drafter-generated)**: cross-brand consolidation lens summary; signals per-brand notices are coming.

  Pattern: `Rather than send [N] independent notices that might miss the cross-brand picture, we've consolidated the portfolio-level framing in this letter; each brand's specific pricing will follow in a separate note within 48 hours.`

- **Sentence 3 (voice-fork conditional, routing pointer per `_root/04 §4.15.6`)**:

  ```
  [IF delivery_owner = CEO:]
  [INSERT _root/04 §4.15.6 CEO-delivered close — verbatim quoted in email body; specific calendar date carries through 3-location date parity contract]

  [IF delivery_owner = Kylor:]
  [INSERT _root/04 §4.15.6 Kylor-delivered close — verbatim quoted in email body; self-continuity "from me" + 48-hour soft commitment]
  ```

- **Signature** (voice-fork conditional):
  ```
  [IF delivery_owner = CEO:]
  [CEO_NAME], CEO, SuperCat

  [IF delivery_owner = Kylor:]
  Kylor Johnson, Head of Customer Success, SuperCat
  ```

### Section 4 — Pre-send checklist

Cite QB-NNN by number only; include parent-letter PDF attach check + Day 0 send-date log check (cited to `_root/07 §6` + operator-notes "After sending" block in Section 1).

### Section 5 — Voice calibration notes

Point to `_root/04 §4.15.1` voice fork (CEO-delivered + Kylor-delivered HoCS variants); `_root/04 §4.15.5` default-only pricing posture (NOT a sales motion; do NOT mention consolidation savings); `_root/04 §4.15.6` routing pointer (recipient MUST know per-brand notices are coming within 48 hours). Calibration boundary: the delivery email is the wrapper; the parent letter does the heavy lifting; the email does NOT carry per-brand detail or per-brand call commitments (those are per-child territory per `_root/04 §4.15.4`).

---

## Step 5: Anti-drift discipline

- **Path-reference contract is absolute** — strict-placeholder precedent operator-stamped 2026-05-26 applies to ALL `_root/`-owned prose including the six `_root/04 §4.15` sub-sections. Any prose owned by `_root/04` (including §4.15.1 voice fork variants, §4.15.5 default-pricing posture, §4.15.6 close variants) is a `[INSERT _root/04 §N.M ...]` placeholder, never inline.
- **Voice-fork rendering**: the template carries BOTH fork variants as `[IF delivery_owner = CEO: ... | IF delivery_owner = Kylor: ...]` conditional blocks. The drafter at Stage 4 production drafting RENDERS ONE fork per parent letter based on Master Entity tab `delivery_owner` value. The template MUST NOT pick a fork; the template carries both.
- **ONLY inlined content** in the template: drafter-facing scaffolding; section headings; table layouts; bracketed data placeholders; bridge/scaffolding sentences with no owning rule (the lede sentence pattern in Section 3c is drafter-generated per §4.15.2 required content, NOT a verbatim rule quote — flag in conformance block); the optional attachment-pointer sentence in delivery email Sentence 2 (template scaffolding per Stage 3.4 precedent — flag in conformance block).
- **CL-001 / CL-003 / CL-004**: confirm absent at entity-level; reference `_root/04 §3` rows in operator-notes.
- **CL-005**: FLAGGED — roadmap section is per-child territory per `_root/04 §4.15.4`; parent letter does NOT carry the "What's Coming in 2026" verbatim block. Each child notice carries it independently per Wave 2 Q4. If operator wants it in parent letter, source-fix to `_root/04 §4.15` required (operator stamp).
- **CL-014**: RESOLVED at Stage 3.5 prep 2026-05-26 (this template authoring is the resolution implementation).
- **CL-022**: infer delivery email + parent-letter routing block subset per Stage 3.1 / 3.2 / 3.3 / 3.4 precedent + entity-packet-specific fields; flag in conformance block pending `_root/07 §7` Wave 6 batch.
- **CL-024**: STRENGTHENED in Step 1 of this prompt (manifest-echo + paste-verification). Conformance block MUST paste-quote the four operator-stamped rule passages enumerated in Step 1.
- **NOT entity-packet-applicable**: CL-002, CL-006–CL-013, CL-015–CL-021, CL-023 — document as out of scope in conformance block.
- **Do NOT carry** archived per-account exemplar patterns — entity-packet is a NEW build with no archived precedent; pattern reference from Stage 3.1–3.4 approved templates is structural-convention reference only.
- **Do NOT** invent rules for the voice-fork variants beyond what `_root/04 §4.15.1` codifies. If you find a fork-specific need that §4.15.1 does NOT cover, flag for operator stamp.
- **Asking is cheap. Inventing is the drift vector.**

---

## Step 6: Voice and format constraints

- Declarative register; `>` blockquotes for drafter-facing blocks.
- `#` file title; `##` customer-facing sections; `###` inside drafter blocks.
- `[ALL_CAPS_WITH_UNDERSCORES]` placeholder convention.
- `[IF condition: ...]` and `[IF condition: ... | ELSE: ...]` for conditional flow.
- `[VOICE FORK: CEO_DELIVERED | KYLOR_DELIVERED]` for the central voice-fork selector (operator-notes Section 1 mention the selector pattern once; Section 3 + Section 4 use `[IF delivery_owner = ...]` conditionals throughout).
- No emoji. No "Importantly" / "Critically".
- Pipe-separated lists in routing block (e.g. `member_accounts: [BRAND_A | BRAND_B | BRAND_C]`) match Master Entity tab CSV column delimiter convention.

---

## Step 7: Output

Create the new folder + both files:

- `Pricing Migration/entity-packets/_parent-letter-template.md`
- `Pricing Migration/entity-packets/_parent-letter-delivery-email-template.md`

Then produce this conformance block in chat (NOT in the files) per `_root/00_manifest.md §5`:

```
─── Conformance Block ─────────────────────────────────────────
Session task: Stage 3.5 — author entity-packets/_parent-letter-template.md + _parent-letter-delivery-email-template.md
Output target:
- Pricing Migration/entity-packets/_parent-letter-template.md (NEW file, NEW folder)
- Pricing Migration/entity-packets/_parent-letter-delivery-email-template.md (NEW file)

Manifest echo (per _root/00_manifest.md §1 step 6 + §6 — paste-quote ALL ENTRIES from §2 with title + Last-updated header date — NOT mtime, the doc's own "Last updated" header):
- 00 Root Doc Manifest — <Last-updated header date>
- C  Operator + Agent Contracts — <Last-updated header date>
- 01 Why We Are Migrating — <Last-updated header date>
- 02 Who Is Being Migrated — <Last-updated header date>
- 03 What We Sell — <Last-updated header date>
- 04 Communication Posture — <Last-updated header date>
- 05 Driver Taxonomy — <Last-updated header date>
- 06 Format Routing — <Last-updated header date>
- 07 Data Pipeline — <Last-updated header date>
- 08 Quality Bar — <Last-updated header date>
- 09 Changelog — <Last-updated header date>

CL-024 paste-verification (per Step 1 — paste-quote the FULL TEXT of each operator-stamped rule passage; if any passage cannot be located, STOP and flag QB-125):
1. `_root/04 §4.15.1` CEO-delivered fork bullet-list:
   <paste-quote verbatim>
   `_root/04 §4.15.1` Kylor-delivered fork bullet-list:
   <paste-quote verbatim>
   `_root/04 §4.15.1` cross-format CSM-role note paragraph:
   <paste-quote verbatim>
2. `_root/04 §4.15.5` default-pricing posture rationale paragraph:
   <paste-quote verbatim>
   `_root/04 §4.15.5` terminology constraint paragraph:
   <paste-quote verbatim>
3. `_root/04 §4.15.6` CEO-delivered close blockquote:
   <paste-quote verbatim>
   `_root/04 §4.15.6` Kylor-delivered close blockquote:
   <paste-quote verbatim>
   `_root/04 §4.15.6` 48-hour timing paragraph:
   <paste-quote verbatim>
4. `_root/06 §1.6` 14-entity enumeration block:
   <paste-quote verbatim>
   `_root/06 §1.6` Ferguson Enterprises exception paragraph:
   <paste-quote verbatim>
   `_root/06 §1.6` Stage 3.5 template scope paragraph:
   <paste-quote verbatim>

Files read (with last-updated header date / mtime — DISTINGUISH between the two; mtime alone is insufficient per CL-024):
- <enumerate every file path from Step 1; include header "Last updated" date for _root/ docs + mtime for archive / artifact files>

Pattern-reference read (Step 1 item 18) — all 8 Stage 3.1–3.4 approved templates:
- <enumerate; note 14 conventions consulted>

Canonical scope source reads (Step 1 items 14–15):
- _master-entity-data-v6.2.csv — <line count + header row + 14-entity row enumeration confirmed>
- _master-account-data-v6.2.csv — <line count + reference for child-brand join confirmed>

Files NOT read:
- <per Step 1 "Do NOT read" + per-account exemplars + non-approved per-account templates>

Parent-letter template sections authored: <count + names 3a–3h>
Delivery email template sections authored: <count + names>

Voice-fork rendering (per `_root/04 §4.15.1`):
- CEO-delivered fork present in template as [IF delivery_owner = CEO: ...] conditional: <yes/no per parent-letter section + per delivery-email section>
- Kylor-delivered fork present in template as [IF delivery_owner = Kylor: ...] conditional: <yes/no per parent-letter section + per delivery-email section>
- Cross-format CSM-role note referenced in operator-notes Section 1: <yes/no>

Entities in scope (per `_root/06 §1.6` + Step 2):
- 12 increase-side rollup: Abaline / Coleto Brands / Creative Home Furniture / Gabriella White / Godinger Group / HVLG / Interlude Home / Jonathan Charles / Rock House Farm / Thesis / Visual Comfort & Co. / WAC Group
- 1 standalone_multi_org: Maxim group Lighting
- Excluded one-off: Ferguson Enterprises (mixed-direction per operator stamp 2026-05-26)

CL items addressed:
- CL-001 / CL-003 / CL-004: confirmed absent at entity-level + referenced `_root/04 §3` rows in operator-notes
- CL-005: FLAGGED — roadmap is per-child territory per `_root/04 §4.15.4`; parent letter does NOT carry roadmap block; operator decision needed if scope changes
- CL-014: RESOLVED at Stage 3.5 prep 2026-05-26 (this authoring is the implementation)
- CL-022: delivery email + parent-letter routing subset INFERRED per Stage 3.1–3.4 precedent + entity-packet-specific fields; flagged pending `_root/07 §7` Wave 6 batch
- CL-024: STRENGTHENED in Step 1 (manifest-echo + paste-verification); paste-quotes provided above

Path-reference contract verification:
- Inlined rule prose count (should be 0): <count>
- §-pointer count by owning doc: <counts; expected: _root/04 §4.15.1 ≥ 2 [voice fork conditional in parent letter + delivery email], §4.15.2 = 1, §4.15.3 = 1, §4.15.4 = 0 [constraint, not insert], §4.15.5 = 1, §4.15.6 ≥ 2 [parent letter + delivery email closes]; _root/06 §1.6 ≥ 1; _root/03 §3 = 0 [per-child territory per §4.15.4]>
- Bracketed placeholder count: <count>

Entity-packet-specific verification:
- `_root/04 §4.15.1` voice fork referenced in BOTH parent letter Section 3 + delivery email Section 3 (CEO-delivered + Kylor-delivered conditionals present): <yes/no>
- `_root/04 §4.15.2` portfolio acknowledgment referenced in parent letter Section 3c: <yes/no>
- `_root/04 §4.15.3` cross-brand consolidation lens referenced in parent letter Section 3d (with conditional acknowledgments for has_annual / mixed_segment / mixed_tiers): <yes/no>
- `_root/04 §4.15.4` per-brand mechanics restraint enforced (zero per-brand driver blocks; zero per-brand pricing tables; zero per-brand call commitments): <yes/no>
- `_root/04 §4.15.5` default-only pricing posture enforced (zero consolidated_delta / consolidation_saving references in customer copy; routing block contains them as INTERNAL-ONLY): <yes/no>
- `_root/04 §4.15.6` routing pointer + 48-hour timing referenced in parent letter Section 3g + delivery email Section 3 Sentence 3: <yes/no>
- Member-brand enumeration present in parent letter Section 3c (every member brand named per `member_accounts` column): <yes/no>
- 4-row entity-level summary table in parent letter Section 3f (NOT 6-row per-account format; NOT per-child pricing tables): <yes/no>
- Voice fork signature variants in BOTH templates (CEO + Kylor "Head of Customer Success" — NOT generic CSM): <yes/no>
- Subject-line convention extended to entity packet ("pricing is changing — effective [DATE]"): <yes/no>

Routing-block field list cross-check (per Step 2 routing-block specification + CL-022 inference):
- <confirm entity-packet routing block fields present in parent letter Section 2 + delivery email Section 2; flag divergences from Stage 3.1–3.4 inference pattern>

Two-stage sequencing verification (per `_root/04 §4.15.6`):
- Day 0 parent-letter send date placeholder in routing block: <yes/no>
- Day 1–Day 2 per-child notices send window placeholder in routing block: <yes/no>
- 48-hour window referenced in operator notes + parent letter close + delivery email Sentence 2 + Sentence 3: <yes/no>

Cross-format CSM-role note verification (per `_root/04 §4.15.1`):
- Kylor-delivered fork signature uses "Head of Customer Success" title (NOT generic "CSM"): <yes/no>
- Operator notes Section 1 references the cross-format CSM-role note explicitly: <yes/no>

Per-brand mechanics restraint verification (per `_root/04 §4.15.4`):
- Zero per-brand driver blocks in template: <yes/no>
- Zero per-brand "Why the Number Is Changing" prose in template: <yes/no>
- Zero per-brand tier feature lists in template: <yes/no>
- Zero per-brand pricing tables in template (entity-level 4-row summary only; per-child tables are per-child territory): <yes/no>
- Zero per-brand value-anchor sections in template: <yes/no>
- Zero per-brand call commitments in template (parent letter has ONE close commitment, not N): <yes/no>

Gaps surfaced: <list or none — particular attention to entity-packet-specific fields that may need source-fix at `_root/07 §7` Wave 6 batch>
Conflicts resolved: <list or none>
Open questions for operator: <list or none — particularly: should Sentence 2 of delivery email be operator-stamped scaffolding or promoted to `_root/04 §4.15`? should CL-005 roadmap pointer be added to parent letter as source-fix to `_root/04 §4.15`? are there member-brand enumeration edge cases (e.g. 4-brand entities like Gabriella White / Godinger / Visual Comfort) that the natural-language rendering needs to handle specifically?>
─────────────────────────────────────────────────────────────
```

Then **STOP**. Do not edit `_root/`, other format folders, `_meta/stage3_cleanup.md`, or any artifact outside the two new template files in `entity-packets/`.

---

## Step 8: If something is missing or contradictory

- Missing `_root/04 §4.15` (any sub-section) at read time → STOP; flag — source fix was applied 2026-05-26 Stage 3.5 prep; if absent, propagation failure per QB-125. Do NOT proceed to authoring (CL-024 manifest-echo + paste-verification will fail).
- Missing `_root/06 §1.6` rewrite at read time → STOP; flag — source fix was applied 2026-05-26 Stage 3.5 prep; if §1.6 still claims "5 accounts" instead of the 14-entity canonical scope, propagation failure per QB-125.
- Missing `_master-entity-data-v6.2.csv` at the workspace root of `Pricing Migration/` → STOP; flag — file was imported 2026-05-26 Stage 3.5 prep; if absent, dual-canonical v6.2 architecture is incomplete.
- A 14th in-scope entity in v6.2 not in the 13 enumerated in Step 2 → STOP; flag — Ferguson Enterprises is the only documented one-off; any other un-enumerated entity is either new data or a v6.2 update; operator must resolve.
- Conflict between `_root/06 §1.6` enumeration and Master Entity tab `entity_name` column → `_master-entity-data-v6.2.csv` Master Entity tab is canonical scope source per operator stamp 2026-05-26 (`_root/06 §1.6` documents the program; the entity file documents the entities).
- `_root/07 §7` entity-packet routing block row not yet authored → infer subset per Step 4 Section 2; flag in conformance block pending Wave 6 batch.
- Voice-fork variant fields ambiguous (e.g. CEO-delivered close calendar date vs Kylor-delivered close 48-hour timing) → cite `_root/04 §4.15.6` explicitly; do NOT improvise.
- Member-brand natural-language rendering edge case (e.g. 4-brand entity rendering becomes awkward) → flag as open question for operator; do NOT improvise a different convention.

**Asking is cheap. Inventing is the drift vector.**
