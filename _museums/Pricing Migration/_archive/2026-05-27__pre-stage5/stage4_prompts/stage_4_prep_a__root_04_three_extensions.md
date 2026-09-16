# Stage 4 Prep — Source-fix Session A: Three `_root/04` extensions (audience register + SaaS-renewal forbidden-phrase rows + Annual-overlay voice rules)

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-26 by Stage 4 planning agent per operator stamps on Stage 4 prep candidates Q1 (CL-015: fix-now) + Q3 (audience register: fix-root-04-1) + Q4 (SaaS-renewal forbids: fix-now). Bundled into one fresh-agent session because all three are `_root/04` extensions — one fresh agent reading `_root/04` in full to make three additive edits is efficient and preserves drift-detection independence per-edit.
> **Output target**: in-place edits to `Pricing Migration/_root/04_communication_posture.md`. THREE additions:
>   - **Extension 1** — `_root/04 §1` (Audience and posture): add an audience-register table distinguishing this program's reader (CFO / owner / principal of a furniture / lighting / decor wholesaler) from SaaS-renewal drift audiences (procurement, IT buyer, "platform admin").
>   - **Extension 2** — `_root/04 §3` (Forbidden phrases): add 8 SaaS-renewal vocabulary rows to the forbidden-phrase table.
>   - **Extension 3** — `_root/04 §4.16` (NEW sub-section): Annual-overlay voice rules per CL-015 (notice references the renewal date rather than a migration effective date per exec plan v3.3 §III). `§4.15` was reclaimed by Parent-letter voice register in Stage 3.5 prep; `§4.16` is the next available slot. If you judge `§5` extension reads better than `§4.16`, surface in the conformance block — operator decides at review pass.
> **Estimated authored length**: ~110–150 net new lines across the three extensions (Extension 1: ~25 lines table + framing; Extension 2: 8 rows × ~3 lines = ~24 lines; Extension 3: ~40–60 lines for §4.16). `_root/04` grows ~495 → ~620 lines.
> **Dependency**: Stage 5 complete (`_root/00`–`_root/09` all operator-stamped). All 5 Stage 3.X template waves APPROVED (Format A + B + CEO Letter + Good News + entity packets). Stage 3.5 closeout manifest-hygiene sweep applied 2026-05-26 (manifest is self-consistent). CL-024 strict + paste-verification discipline operator-stamped 2026-05-26 — **applies to this session in full**.

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. That is **load-bearing** for this prompt. You are authoring three additive extensions to `_root/04_communication_posture.md` (the highest-rule-density doc in the system) at the canonical source. Your output is NEW RULE PROSE that every Stage 4 per-account drafter will fetch by `_root/04 §N.M` pointer.

This is **source-fix work**, not template authoring. The path-reference contract (`_root/CONTRACTS.md §5`) governs your authoring: you author the rule prose at its canonical home, and downstream artifacts (Stage 3 templates, Stage 4 per-account briefs, Appendix A of the handoff doc) reference your prose by `_root/04 §N.M` pointer. You do NOT restate any other `_root/` doc's rules inside your new prose — cross-references are pointers, never inlines, per the strict-placeholder precedent operator-stamped 2026-05-26.

**You will not invent new rules.** The operator has pre-stamped what each extension contains:
- Extension 1's audience-register table is operator-stamped in `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix A.2 (operator stamp footer at A.12 end).
- Extension 2's SaaS-renewal forbidden-phrase vocabulary is operator-stamped in the same handoff doc Appendix A.6.
- Extension 3's Annual-overlay voice consequence is documented in `_meta/stage3_cleanup.md` CL-015 entry (operator-decisions cross-reference exec plan v3.3 §III).

Your job is to translate the operator-stamped content into canonical `_root/04` sub-section form (matching `_root/04`'s existing voice + structure + cross-reference style) and produce the in-place edit.

**You will not paraphrase, soften, or "improve" any operator-stamped content** in the source materials. If you find yourself wanting to reword Appendix A.2's audience table or Appendix A.6's forbidden-phrase list, **stop**. Paste-fidelity is the operator stamp's enforcement mechanism (per the CL-024 strict + paste-verification discipline operator-stamped 2026-05-26).

**You will not extend beyond the three named extensions.** No edits to §2 (non-negotiables), no edits to §4.1–§4.15 (existing voice rules), no edits to §5 (driver-voice orientation), no edits to §6 (what this doc does NOT own). The header `Last updated` line and the §3 table itself receive in-place edits per the extension specs below; nothing else in `_root/04` is touched.

---

## Step 1: Required reading (in this exact order) — STRICT MANIFEST-ECHO + PASTE-VERIFICATION CONTRACT

**Reading file mtimes is NOT the manifest echo.** The manifest echo requires reading the `_root/00_manifest.md §2` table AND reading every `_root/` doc's header block AND echoing each doc's title + Last-updated date from the header in your first chat response. **A pre-existing artifact in the workspace (e.g. a prior session's source-fix output, a Stage 3 template, an Appendix A of the handoff doc you read in passing) is NOT a substitute for re-reading the canonical rule layer.**

If you cannot produce the canonical manifest echo, your session is not ready to author; STOP and flag per `_root/CONTRACTS.md §2`.

**This is the CL-024 strict + paste-verification protocol** (operator-stamped 2026-05-26 at Stage 3.5 review pass — applies forward to every fresh-agent session in the program). Source-fix sessions are the heaviest-leverage fresh-agent work: authoring at canonical source. Drift here propagates to every Stage 4 per-account brief.

**Additionally — paste-verification requirement (CL-024)**: in your conformance block, you must paste-quote the FULL TEXT of the following operator-stamped source passages, verbatim from the source files (not paraphrased, not summarized, not just cited):

1. `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix **A.2** — the entire 4-row audience-register table (Dimension / This program / SaaS-renewal drift to forbid) PLUS the one-line operator-stamped framing sentence ("Write for a principal who runs a wholesale business, not a software buyer renewing a SaaS seat.")
2. `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix **A.6** — the bulleted "Forbidden framings (cite `_root/04 §3` table in prompts)" list (7+ items) PLUS the formal-notice-line paragraph PLUS the Good News exception paragraph.
3. `_meta/stage3_cleanup.md` **CL-015 entry** — the entire entry (Source / Fix / Locations to fix) verbatim.
4. `_reference/2026-05-20__execution_plan_v3.3.md` **§III paragraph(s)** discussing Annual-overlay voice (the notice references the renewal date rather than a migration effective date) — paste-quote the relevant paragraph(s) verbatim. If §III does not contain explicit Annual-overlay voice prose, paste-quote the closest paragraph that documents the renewal-date framing and flag in your conformance block.

If you cannot paste-quote any of these passages because the source text is not present at the cited location, STOP and flag per QB-125 propagation-failure rule. Do NOT proceed to authoring.

### Folder orientation (mandatory — echo in conformance block per `_root/00_manifest.md §6`)

1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/00_manifest.md` — the index. **The §2 manifest table is the authoritative list of every `_root/` doc; you echo it in your first chat response per the manifest-echo contract in §1 step 6. ALL ENTRIES, NOT A SUBSET.**
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md`
5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/09_changelog.md` — read every entry. **Particularly important for this session**:
    - Wave 1 (`_root/04` initial authoring 2026-05-22) — the existing §1 / §2 / §3 / §4 structural conventions you must match.
    - Stage 3 reviews 3.1 / 3.2 / 3.3 / 3.4 / 3.5 — operator stamps that affect downstream propagation (your extensions will trigger downstream re-runs only of `_root/08` QB-NNN dependencies; no Stage 3 template re-runs because the templates reference §1 / §3 / §4.X by pointer and pointers are stable).
    - Stage 3.5 prep entry — `_root/04 §4.15` was authored as Parent-letter voice register (6 sub-sections); this is why CL-015 needs `§4.16` or `§5` extension (§4.15 is no longer available).
    - Stage 3.5 review pass + closeout manifest-hygiene sweep — the most recent edits to `_root/04` + `_root/00_manifest.md`; this session's header `Last updated` bump appends to the existing 2026-05-26 annotations.

### The rule layer — read in FULL

6. `_root/01_why_we_are_migrating.md` — strategic register; the 5 structural problems + 4 operating principles. Your Extension 1 (audience-register) cross-references this for the relationship-before-price principle.
7. `_root/02_who_is_being_migrated.md` — segments, $200/$400/$600 ownership boundaries, **§5 Annual overlay** (your Extension 3 cross-references §5 for Annual overlay scope; the timing consequence lives at `_root/06 §4.3` and your Extension 3 cross-references both).
8. `_root/03_what_we_sell.md` — tier blocks; not directly cross-referenced by your extensions but read for full rule-layer context.
9. `_root/04_communication_posture.md` — **the doc you are editing.** Read every subsection in FULL. **For this session specifically**:
    - **§1 Audience and posture** — your Extension 1 inserts at the end of §1 (after the existing "Internal-vs.-client boundary" paragraph). The existing §1 contains: (a) Audience paragraph, (b) Voice posture paragraph, (c) Internal-vs.-client boundary paragraph. Your extension adds a fourth element: an audience-register table contrasting this program's audience with SaaS-renewal-drift audiences.
    - **§2 Non-negotiables** — read but DO NOT EDIT. Your extensions do not change any non-negotiable.
    - **§3 Forbidden phrases table** — your Extension 2 inserts 8 new rows into the existing 27-row table. Read all 27 existing rows in full to understand the row format (Do not write | Replacement | Why) and to confirm none of your 8 new SaaS-renewal rows duplicate an existing row.
    - **§3.1 Good News consolidated 2026 framing sentence** — read but DO NOT EDIT.
    - **§4.1 through §4.15.6** — read all in FULL. Your Extension 3 authors §4.16 NEW after §4.15.6; you do not edit any §4.1–§4.15 prose.
    - **§5 Driver-voice orientation** — read in full. Your Extension 3 alternative (if you judge §5 extension reads better than §4.16 standalone — see Step 5) would extend §5. Default: author §4.16 new sub-section.
    - **§6 What this doc does NOT own** — read but DO NOT EDIT.
10. `_root/05_driver_taxonomy.md` — read for orientation only; your extensions do not edit `_root/05` nor cross-reference it directly.
11. `_root/06_format_routing.md` — **§4.3 Annual overlay** is the canonical timing rule (90-day notice window; Renewal-Based cohort). Your Extension 3 cross-references §4.3 as the timing companion to your new §4.16 voice rule.
12. `_root/07_data_pipeline.md` — read for orientation; §2's `has_annual` column is the data signal that fires your Extension 3 voice rule at draft time.
13. `_root/08_quality_bar.md` — read for orientation; your Extension 3 (§4.16 Annual voice) and Extension 2 (§3 SaaS-renewal forbids) will trigger new QB-NNN check additions in a separate `_root/08` source-fix session (Source-fix Session B / Wave 6 batch — not this session). You do not edit `_root/08`; just be aware downstream QB additions will follow.

### Source materials for the three extensions (REQUIRED — paste-verify in conformance block per CL-024)

14. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` — **explicit per-prompt authorization to read this file** (the normal AGENTS.md hard rule against browsing `_meta/` is overridden for this Stage 4 prep session, scoped to this specific file). Read sections:
    - **§1 What this program is (in 200 words)** — establishes the canonical CFO/owner/principal audience claim that your Extension 1 codifies at `_root/04 §1`.
    - **§4 Architectural concepts you are inheriting from Stage 3** — particularly concept #1 (Path-reference contract) and concept #2 (Strict-placeholder precedent); both govern your authoring discipline.
    - **Appendix A.2 — Lock audience and relationship register** — the 4-row audience-register table is your Extension 1 source; paste-verify verbatim in conformance block.
    - **Appendix A.6 — Migration mechanics vocabulary, not SaaS vocabulary** — the bulleted SaaS-renewal forbids list is your Extension 2 source; paste-verify verbatim in conformance block.
    - Appendix A footer ("Appendix A is operator-stamped 2026-05-26 ... Revising any of A.1–A.12 requires the rule-change protocol per `_root/CONTRACTS.md §3`") — confirm operator-stamp authority.
15. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_meta/stage3_cleanup.md` — **explicit per-prompt authorization to read this file** (Stage 3 cleanup tracker; normally consulted by planning agent only). Read in full but apply specifically:
    - **CL-015 entry** — your Extension 3 source. Paste-verify the entire entry verbatim in conformance block. The entry references `_root/06 §4.3` (timing) and exec plan v3.3 §III (voice consequence).
    - Other CL items: read for context; do not act on them. CL-001 / CL-003 / CL-004 / CL-005 / CL-018–CL-021 are exemplar-regen items (Stage 4 production scope). CL-022 / Stage 3.5-deferred items #4 + #5 are scope for Source-fix Session B (a separate fresh-agent session — not this session).
16. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_reference/2026-05-20__execution_plan_v3.3.md` — **explicit per-prompt authorization to read this file**, scoped to **§III only** (the Annual-overlay voice consequence reference). The normal AGENTS.md rule against browsing `_reference/` is overridden for this specific section read. Paste-verify the relevant paragraph(s) verbatim in conformance block. If §III does not contain explicit Annual-overlay voice prose at the cited location, search for "renewal-based," "renewal cohort," or "Annual overlay" anywhere in the document and paste-verify the closest matching passage; flag the discrepancy in your conformance block.

### Pattern reference from Stage 3.4 prep + Stage 3.5 prep (required — both operator-approved 2026-05-26)

17. `_root/09_changelog.md` entries:
    - **"2026-05-26 — Stage 3.4 prep"** — pattern for adding NEW sub-sections to `_root/04` (`§3.1` Good News framing sentence + `§4.5` Good News operations-unchanged variant; planning-agent-applied edits after fresh-agent surfacing). Your Extension 1 (§1 audience table) and Extension 2 (§3 SaaS-renewal rows) follow this in-section-extension pattern.
    - **"2026-05-26 — Stage 3.5 prep"** — pattern for adding a NEW sub-section block (§4.15 Parent-letter voice register; 6 sub-sections totaling ~110 lines). Your Extension 3 (§4.16 Annual-overlay voice) follows this new-sub-section pattern at smaller scale (~40–60 lines).

### Do NOT read

- Any other `_meta/` file beyond items 14 + 15 above (no other stage4_prompts files including Source-fix Session B prep prompt if drafted; no stage3_prompts files; no stage2_prompts files; no other cleanup trackers).
- Any other `_reference/` file beyond item 16's §III scope (no full read of exec plan v3.3; no HTML revenue model).
- Any `_archive/` file — anti-archive per `_root/CONTRACTS.md §4`; no explicit-extraction exception opened for this session because all source materials live in `_root/` + `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` + `_meta/stage3_cleanup.md` + `_reference/...v3.3.md §III`.
- Any Stage 3 template file (format-a-notices/, format-b-notices/, ceo-letter-notices/, good-news-notices/, entity-packets/) — these are downstream artifacts that reference `_root/04` by pointer; they don't inform your authoring and reading them risks confusing scope.
- Per-account exemplars (none should exist in the workspace at Stage 4 prep time; if any do, do NOT read them).
- `~/Downloads/**` or anything outside `Pricing Migration/`.

---

## Step 2: Authoritative scope (three extensions; use as fact — do not re-derive, do not extend)

You author exactly THREE extensions to `_root/04`. Each extension is operator-stamped per the source materials in Step 1. Do not propose a fourth extension; do not skip an extension; do not merge extensions.

### Extension 1 — `_root/04 §1` audience-register table

**What**: an audience-register table contrasting this program's reader (CFO / owner / principal of a furniture / lighting / decor wholesaler) with SaaS-renewal-drift audiences (procurement, IT buyer, "platform admin"). Source: PLANNING_AGENT_HANDOFF.md Appendix A.2 verbatim table + the one-line operator-stamped framing sentence.

**Where**: at the end of `_root/04 §1` (after the existing "Internal-vs.-client boundary" paragraph; before the `---` separator that begins §2). The existing §1 contains three paragraphs (Audience / Voice posture / Internal-vs.-client boundary); your extension adds a fourth element as `### §1.1 — Audience register` (or equivalent; you choose the sub-section heading style that matches `_root/04`'s existing convention).

**Why now**: Stage 4 per-account drafters will inherit the audience-register table by `_root/04 §1` pointer per Appendix A.5 path-reference contract. Without the rule-layer codification, Appendix A.2 is the only canonical source — and Appendix A is a planning-agent-handoff artifact, not a rule doc; 5 separate `stage_4_X` prompts each baking in the table verbatim is a drift vector (any single prompt diverging produces inconsistency). Codifying at `_root/04 §1` gives every Stage 4 drafter prompt a single pointer.

### Extension 2 — `_root/04 §3` SaaS-renewal forbidden-phrase rows

**What**: 8 new rows added to the existing 27-row §3 forbidden-phrase table. Source: PLANNING_AGENT_HANDOFF.md Appendix A.6 bulleted forbidden-framings list. The 8 rows (Do not write | Replacement | Why) cover:

1. "Renewal" framing (e.g. "As your renewal approaches…")
2. "Auto-renew" framing
3. "Subscription renewal" framing
4. "At renewal we're adjusting…" framing
5. "Rate card alignment" without tenure / driver context (note: a row exists for "rate card" alone at the existing §3 table line ~58 — your new row is distinct, addressing the "rate card alignment" full phrase)
6. "As part of this refresh" → "going forward" (note: a row exists for this at the existing §3 table line ~59 — DO NOT duplicate; if your row would duplicate, skip and note in conformance block)
7. "We're adjusting your pricing" (note: this is non-negotiable §2.2 already; the existing §3 table may not have a row — verify and add if absent, skip if present)
8. Generic SaaS terms: "platform admin," "platform admin login," "platform admin role" (per Appendix A.2 audience-register row 1 "platform admin" forbid)

**Verification step before authoring Extension 2**: read the entire existing 27-row §3 table and confirm which Appendix A.6 forbids already have rows. The §3 table currently includes rows for "rate card" (single phrase), "as part of this refresh," "We're adjusting your pricing" (possibly via non-negotiable §2.2 cross-reference), and a few others. Your 8 new rows are the Appendix A.6 forbids NOT already covered. Net new row count may be 5–8 depending on which already exist; document each skip-because-duplicate decision in your conformance block.

**Where**: appended to the existing §3 table (in row-order convention — alphabetical or thematic per `_root/04`'s existing row-order convention; if no clear convention, append at the end of the table before the `### §3.1 — Good News consolidated 2026 framing sentence` heading).

**Why now**: same path-reference contract argument as Extension 1. Appendix A.6 enumerates SaaS-renewal forbids as design constraints for every `stage_4_X` drafter prompt; codifying at `_root/04 §3` gives drafters a single canonical source. Without codification, the appendix's bulleted list risks divergence from any `stage_4_X` prompt that re-bakes it.

### Extension 3 — `_root/04 §4.16` (or `§5` extension; default `§4.16`) Annual-overlay voice rules

**What**: NEW sub-section authoring the voice rule for Annual-cohort accounts (`has_annual = TRUE` per v6.2 + `_root/07 §2`). Source: `_meta/stage3_cleanup.md` CL-015 entry + `_reference/2026-05-20__execution_plan_v3.3.md` §III.

**Substance** (per CL-015 + exec plan v3.3 §III):

- Annual-cohort accounts receive notice referencing the **renewal date**, not a migration effective date. The notice frames the pricing change as effective at the next renewal (per the 90-day window in `_root/06 §4.3`), not at a flat migration effective date that applies uniformly to non-Annual accounts.
- The lede dollar + effective date pattern (non-negotiable `_root/04 §2.1` "Lead with the dollar amount and effective date") shifts at draft time: the effective date is the renewal date, not a migration effective date. The drafter pulls the renewal date from v6.2 (or from the routing CSV's `nuances` column if v6.2 is missing) and renders the lede sentence accordingly.
- The consolidated 2026 framing sentence (`_root/04 §3` row "SuperCat is standardizing its pricing…" → universal sentence; Good News exception at §3.1) applies as-is for Annual accounts — the framing of "moving every account to one clear pricing structure" is timing-independent. Only the per-account effective-date sentence shifts to renewal-date framing.
- Cross-references: `_root/06 §4.3` (Annual overlay timing — 90-day notice window; Renewal-Based cohort); `_root/02 §5` (Annual overlay scope — which accounts are Annual); `_root/07 §2` (`has_annual` data field); `_root/04 §2.1` (non-negotiable lede pattern — Annual voice rule supplements rather than replaces).

**Where** (default): NEW sub-section `### Section 4.16 — Annual-cohort voice rules` (matching `_root/04 §4.15` Parent-letter voice register naming convention). Inserted between `### §4.15.6 — Routing pointer to per-child notices (closing transition)` (line ~459 in current `_root/04`) and `## Section 5 — Driver-voice orientation` (line ~477 in current `_root/04`). Use `## Section 4.16` if `_root/04`'s convention is `## Section N` headings (verify against §4.15 which uses `### §4.15.1`–`§4.15.6` sub-section headings under a `## Section 4` ancestor — adopt the existing pattern; you may use `## Section 4.16` standalone heading OR `### §4.16` under an implicit `## Section 4` ancestor; choose the structure that reads cleanest in `_root/04`'s established style and explain choice in conformance block).

**Where** (alternative): if you judge `§5` (Driver-voice orientation) extension reads better — i.e. the Annual-overlay voice consequence is "timing voice" rather than a standalone voice register, and a one-paragraph extension to §5 captures it cleanly — author at `§5 extension` instead of `§4.16` standalone. Surface the choice in conformance block; operator decides at review pass.

**Length target**: ~40–60 lines for §4.16 (matches the per-sub-section length of §4.15.1–§4.15.6 at ~15–20 lines each). If §5 extension chosen, ~10–20 lines.

**Why now**: Stage 4 will draft Annual accounts (the `has_annual = TRUE` slice of v6.2 — meaningful volume across multiple formats). Missing voice-rule home means drafters improvise per-account or surface as a CL during production. Authoring §4.16 (or §5 extension) at Stage 4 prep keeps the path-reference contract clean before any per-account drafting begins.

---

## Step 3: Extension 1 detailed spec — `_root/04 §1` audience-register table

### Source content (paste-verify verbatim from Appendix A.2)

The 4-row audience-register table from `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix A.2:

| Dimension | This program | SaaS-renewal drift to forbid |
|---|---|---|
| Reader | CFO / owner / principal of a furniture / lighting / decor wholesaler | Procurement, IT buyer, "platform admin" |
| Relationship | Vendor-to-principal or CEO-to-CEO (CEO Letter) | Service-rep-to-buyer, CSM check-in |
| Register | Declarative, empathetic on impact, firm on architecture | Cheerful renewal, "excited to partner," soft upsell |
| What they're evaluating | A specific invoice change with a mechanical explanation | Subscription tier change or contract term sheet |

Plus the one-line operator-stamped framing sentence:

> Write for a principal who runs a wholesale business, not a software buyer renewing a SaaS seat.

### Authoring spec

- **Sub-section heading**: `### Section 1.1 — Audience register` (or equivalent — match `_root/04`'s existing sub-section heading style; the existing §1 doesn't currently use `§1.1` sub-sections so you may author the table as a labeled block under §1 without a sub-section heading, OR introduce `### §1.1` as the new sub-section. Surface your choice + rationale in conformance block.)
- **Framing paragraph (drafter-authored; short)**: 1–2 sentences introducing the table. Cite `_root/01 §1` relationship-before-price principle as the strategic anchor; cite the existing §1 Audience paragraph as the canonical audience definition the table elaborates.
- **The table verbatim from Appendix A.2** (paste; do not paraphrase any cell text).
- **Closing one-line sentence**: paste the operator-stamped framing sentence verbatim from Appendix A.2 ("Write for a principal who runs a wholesale business, not a software buyer renewing a SaaS seat.").
- **Cross-references** (italicized closing line of the new sub-section): pointer to `_root/04 §3` (SaaS-renewal forbids — your Extension 2 codifies these); pointer to `_root/04 §4` (named voice rules that operate inside this audience register); pointer to `_root/01 §1` (relationship-before-price principle).

### Anti-drift discipline (Extension 1 specific)

- **Do NOT paraphrase any cell text** in the table. Paste-fidelity per CL-024 strict + paste-verification.
- **Do NOT extend the table beyond 4 rows**. The 4 rows are operator-stamped at Appendix A.2; adding a 5th row is rule invention.
- **Do NOT add explanatory prose for individual rows** — the table is the codification; per-row commentary clutters and dilutes.
- **Do NOT edit the existing §1 Audience, Voice posture, or Internal-vs.-client boundary paragraphs** — your extension is purely additive at the end of §1.
- **Cross-reference forbidden phrases by `_root/04 §3` pointer; do NOT inline any forbidden-phrase examples** — those live in §3 (extended by your Extension 2).

---

## Step 4: Extension 2 detailed spec — `_root/04 §3` SaaS-renewal forbidden-phrase rows

### Source content (paste-verify verbatim from Appendix A.6)

The bulleted SaaS-renewal forbids list from `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix A.6:

- "Renewal," "auto-renew," "subscription renewal," "at renewal we're adjusting…"
- "Rate card alignment" without tenure / driver context
- "As part of this refresh" → use "going forward"
- Leading with percentage (`_root/04 §2.1`)
- "We're adjusting your pricing"
- Gift / reward / favor on decreases
- Expansion / Format C in migration notice
- Competitor or peer dollar ranges (CL-003 / CL-004)
- CL-001 forbidden sentence ("no account-specific adjustments")

### Authoring spec

For each Appendix A.6 forbid NOT already in the existing 27-row §3 table (verification step below), add a row to the §3 table in the format:

| Do not write | Replacement | Why |
|---|---|---|
| `<the forbidden phrase as quoted in Appendix A.6>` | `<replacement direction; cite a §-pointer to existing rule if relevant>` | `<one-sentence rationale tying to audience register §1.1 + SaaS-renewal-drift framing>` |

### Verification step (BEFORE authoring — required)

Read the entire existing §3 table (lines ~49–76 in current `_root/04`; ~27 rows) and produce a coverage map:

| Appendix A.6 forbid | Already in §3? (YES/NO + existing row reference) | Action |
|---|---|---|
| "Renewal" / "auto-renew" / "subscription renewal" / "at renewal we're adjusting…" | (verify) | ADD if absent |
| "Rate card alignment" without tenure / driver context | (verify — note "rate card" alone has a row at ~line 58) | ADD distinct row for "alignment" framing |
| "As part of this refresh" → "going forward" | YES at line ~59 | SKIP — already covered |
| Leading with percentage | YES — covered by non-negotiable §2.1 + an existing §3 row at line ~65 | SKIP — already covered |
| "We're adjusting your pricing" | (verify — non-negotiable §2.2 prohibits; check if §3 has explicit row) | ADD if absent from §3 (non-negotiable status is separate from §3-table membership) |
| Gift / reward / favor on decreases | YES at line ~67 (in Good News context) | SKIP — already covered |
| Expansion / Format C in migration notice | YES via non-negotiable §2.6 + an existing §3 row at line ~73 | SKIP — already covered |
| Competitor / peer dollar ranges | YES at line ~57 (competitor) + line ~74 (peer dollars) | SKIP — already covered |
| CL-001 forbidden sentence | YES at line ~62 | SKIP — already covered |

Net new rows expected: **5–8** (the exact count depends on your verification — surface the coverage map in your conformance block).

Additionally, add row(s) for the Appendix A.2 audience-drift forbids that are NOT in Appendix A.6 but are clearly forbids in the program's vocabulary per the audience-register table:

| Audience-register forbid (from Appendix A.2 row 1 SaaS-renewal column) | Add to §3? |
|---|---|
| "platform admin" / "platform admin login" / "platform admin role" | ADD — SaaS-vocabulary that signals wrong audience |
| "procurement" framing (e.g. "your procurement team," "procurement contact") | ADD — wrong-audience framing per Appendix A.2 row 1 |
| "IT buyer" framing | ADD — wrong-audience framing per Appendix A.2 row 1 |

These 3 audience-drift rows are operator-stamped via Appendix A.2 (audience-register codification implies their forbids); add them as part of Extension 2.

### Authoring discipline

- **Row format**: match the existing §3 table format exactly (3 columns: Do not write | Replacement | Why).
- **"Why" column**: each new row's rationale ties to either (a) audience-register §1.1 (wrong-audience signals) or (b) SaaS-renewal-drift framing (vocabulary that pulls the brief out of book-normalization register and into SaaS-renewal register). Be specific; cite §1.1 or the SaaS-renewal-drift framing explicitly.
- **Replacement column**: where Appendix A.6 specifies a replacement (e.g. "As part of this refresh" → "going forward"), use it; where it doesn't, direct to "Cut entirely; cite `_root/04 §1.1` audience register" or similar — match the existing §3 table's replacement conventions (some rows direct to specific replacements, others say "Cut entirely" or "Strip entirely").
- **Row order**: append after the existing row 27 (the "transition" row at ~line 76) before the `### §3.1 — Good News consolidated 2026 framing sentence` heading. If the existing table has a thematic ordering (audience / structural / numerical / format-specific / decrease-side), insert in the thematic location; if alphabetical or no clear order, append.
- **Do NOT edit any existing row** — pure additive.

---

## Step 5: Extension 3 detailed spec — `_root/04 §4.16` (or §5 extension) Annual-overlay voice rules

### Source content (paste-verify verbatim from CL-015 + exec plan v3.3 §III)

From `_meta/stage3_cleanup.md` CL-015 entry (operator-stamped via cleanup-tracker lifecycle 2026-05-22 + location update 2026-05-26):

> **CL-015 — Annual overlay voice rules need a home in `_root/04`**
> - **Source**: `_root/06 §4.3` (GAP-2) + Wave 3.2 review 2026-05-22.
> - **Fix**: `_root/06 §4.3` documents the Annual overlay's timing consequence (90-day notice window, Renewal-Based cohort). The voice consequence — per exec plan v3.3 §III, the notice references the renewal date rather than a migration effective date — is not yet owned by any `_root/04` subsection. Stage 3 cleanup (or earlier, when first Annual brief is drafted): add `_root/04 §4.16` Annual renewal-date voice rule (or extend `_root/04 §5` driver-voice orientation paragraph), then update `_root/06 §4.3` to point to the new rule.
> - **Locations to fix**: `_root/04` (new §4.16 or §5 extension — §4.15 originally proposed for this CL was occupied by Stage 3.5 prep 2026-05-26 with the Parent-letter voice register; CL-015 location updated 2026-05-26 to §4.16 or §5 extension).

From `_reference/2026-05-20__execution_plan_v3.3.md` §III: paste-verify the relevant paragraph(s) verbatim. Surface in conformance block. The §III content should document the Renewal-Based cohort's voice consequence (notice references renewal date rather than migration effective date); if §III does not explicitly carry this prose, paste-quote the closest available exec-plan paragraph and flag.

### Authoring spec (default — `§4.16` standalone sub-section)

Sub-section structure (matching `_root/04 §4.15` Parent-letter voice register style):

**`### Section 4.16 — Annual-cohort voice rules`** (or `## Section 4.16` standalone heading — choose per `_root/04` existing convention; surface choice in conformance block)

**Sub-section content** (~40–60 lines):

1. **What this sub-section owns** (1 paragraph): voice consequence for Annual-cohort accounts; renewal-date framing vs migration-effective-date framing; lede shift; consolidated framing sentence stability.

2. **§4.16.1 — Scope** (~5–8 lines): cite `_root/02 §5` (Annual overlay scope — which accounts are Annual); cite `_root/07 §2` (`has_annual` data field — `TRUE` fires this voice rule); cite `_root/06 §4.3` (timing companion — 90-day notice window, Renewal-Based cohort). Affects all 4 increase-side formats (Format A, Format B, CEO Letter, Good News) AND the entity-packet parent letter where any member-brand is Annual.

3. **§4.16.2 — Lede effective-date shift** (~10–15 lines):
    - Non-negotiable `_root/04 §2.1` ("Lead with the dollar amount and effective date") supplements with Annual variant: effective date is the renewal date, not a flat migration effective date.
    - The verbatim lede sentence pattern: "Your monthly pricing is changing from $X to $Y effective at your renewal on [RENEWAL_DATE]" (or per-format equivalent — cross-reference the per-format lede patterns at `_root/04 §4.1` tenure-aware variants, `§4.2` lede stat guardrail, `§4.13` health-band overrides).
    - Drafter pulls `renewal_date` from v6.2 (column to be added; flag for v6.2 maintainer if column missing — fallback to routing CSV `nuances` per `_root/07 §5`).
    - Operations-unchanged sentence (`_root/04 §4.5`) and consolidated 2026 framing sentence (`_root/04 §3` universal row; Good News exception at `§3.1`) apply as-is for Annual accounts — only the per-account effective-date sentence shifts.

4. **§4.16.3 — Close + formal-notice line** (~8–12 lines):
    - Format-specific close text (`_root/04 §4.12`) applies as-is for Annual accounts; the close commitment (passive Format A / active Format B / specific date CEO Letter / Good News no-ask) does not shift.
    - Formal-notice line per `_root/04 §4.12` references the renewal date as the effective date (substitute `[EFFECTIVE_DATE]` = `[RENEWAL_DATE]` for Annual accounts).
    - CEO Letter 3-location date parity contract (operator-stamped at Stage 3.3 review pass 2026-05-26 via template-level QB-086 + QB-NNN cross-check) applies as-is for Annual CEO Letter accounts; the specific calendar date in the close + brief routing block + delivery email routing block can be either the call commitment date OR the renewal date OR both (operator stamps at per-account draft time; drafter surfaces both options).

5. **§4.16.4 — Drafter judgment + surfacing** (~5–8 lines):
    - If `renewal_date` is missing or ambiguous, drafter surfaces to operator before drafting (do NOT default to migration effective date).
    - If `has_annual = TRUE` but the routing CSV indicates the account is in a non-Renewal-Based cohort (e.g. operator override), drafter surfaces the routing-cohort mismatch to operator.
    - Annual + entity-packet interaction: if an entity has both Annual and non-Annual member-brands, the parent letter's `§4.15.3` deal-type heterogeneity acknowledgment fires; the parent letter is sent at parent timing (Day 0 per `§4.15.6` 48-hour sequencing), and per-child Annual notices follow their renewal-date timing per this §4.16 (which may extend beyond the 48-hour window for Annual children — flag operator at per-brief draft time).

6. **Closing cross-references** (italicized line at end): `_root/06 §4.3` (Annual timing); `_root/02 §5` (Annual scope); `_root/07 §2` (`has_annual` field); `_root/04 §2.1` (non-negotiable lede); `_root/04 §4.5` (operations-unchanged); `_root/04 §3` + `§3.1` (consolidated 2026 framing); `_root/04 §4.12` (format-specific close + formal-notice line); `_root/04 §4.15.3` (entity-packet deal-type heterogeneity).

### Alternative — `§5` extension (only if you judge this reads cleaner)

If you judge the §4.16 standalone sub-section over-engineers a voice consequence that fits better as a one-paragraph extension to `_root/04 §5` Driver-voice orientation, author the extension as:

- A new paragraph (or sub-paragraph) at the end of `_root/04 §5` titled `### §5.1 — Annual-cohort voice` (or equivalent).
- ~10–20 lines covering the same substantive content as §4.16.1–§4.16.4 above, but compressed to fit §5's "voice orientation" register.
- Cross-references unchanged.

**Decision criterion**: §4.16 standalone (default) if the Annual-overlay voice consequence warrants its own sub-section (multiple sub-rules; lede shift + close handling + drafter judgment); §5 extension if a single paragraph captures the substantive content.

Surface your choice + rationale in conformance block; operator decides at review pass and may direct revision.

### Anti-drift discipline (Extension 3 specific)

- **Do NOT inline `_root/06 §4.3` timing rules** — cross-reference by pointer. The 90-day window lives at `_root/06 §4.3`, not at your new §4.16.
- **Do NOT restate `_root/02 §5` Annual overlay scope** — cross-reference by pointer.
- **Do NOT inline `_root/04 §4.5` operations-unchanged sentence** — cross-reference by pointer.
- **Do NOT inline `_root/04 §4.12` close text or formal-notice line** — cross-reference by pointer.
- **Do NOT propose changes to non-negotiable §2.1** — your §4.16 supplements §2.1; it does not amend.
- **If the `renewal_date` v6.2 column is missing** (verify against `_master-account-data-v6.2.csv` header — column count = 53 per `_root/07 §2`), flag in conformance block as a downstream v6.2-maintainer task; do NOT add the column yourself (v6.2 is the data layer, not the rule layer).

---

## Step 6: Anti-drift discipline (cross-cutting; applies to all three extensions)

This session authors NEW rule prose at canonical source. The path-reference contract governs your authoring as much as it governs Stage 3 template authoring:

- **You do NOT restate any other `_root/` doc's rules inside your new prose.** Cross-references are `_root/XX §N.M` pointers, never inlines. (Strict-placeholder precedent operator-stamped 2026-05-26 Stage 3.1 review pass; applies to rule-prose-authoring sessions as well as template-build sessions.)
- **You do NOT edit existing `_root/04` prose** beyond the explicit insertion points named in Steps 3 / 4 / 5. No reworking of §1's existing paragraphs; no row deletions or edits in §3 (only appends); no edits to §4.1–§4.15 prose; no edits to §5 / §6 / footer (except the §5 extension if you choose that path for Extension 3).
- **You do NOT propose changes to non-negotiables (§2)** — your extensions supplement non-negotiables, never amend them.
- **You do NOT touch any other `_root/` doc.** Downstream propagation (manifest bumps, changelog entry, `_root/06 §4.3` cross-reference update to point to your new §4.16, etc.) is the planning agent's review-pass responsibility, NOT yours.
- **You do NOT touch any Stage 3 template, Stage 4 prompt, or per-account artifact.** Stage 3 templates reference `_root/04` by pointer; your edits at `_root/04 §1` / `§3` / `§4.16` are picked up automatically via pointer resolution at draft time. No template edits required.
- **Header `Last updated` bump is required**: append a new annotation to the existing `_root/04` header `Last updated` line (currently "2026-05-26 (Stage 3.5 prep — §4.15 Parent-letter voice register added: ...) ...") with a Stage-4-prep-Source-fix-Session-A annotation summarizing the three extensions. Format: "Stage 4 prep Source-fix Session A 2026-05-26 (Extension 1: `§1.1` audience register table per Appendix A.2; Extension 2: 5–8 SaaS-renewal forbidden-phrase rows added to `§3` per Appendix A.6 + audience-register implications; Extension 3: `§4.16` Annual-cohort voice rules per CL-015 + exec plan v3.3 §III)" — adjust counts to your actual coverage.
- **No header `Owner` change**: `_root/04` is CEO-owned; your authoring is operator-stamped via Appendix A footer + CL-015 lifecycle.
- **Path-reference contract self-check before writing**: every cross-reference to another `_root/` rule in your new prose is a `_root/XX §N.M` pointer (not "see Section X" without a path; not "as documented elsewhere"; not paraphrased reproduction).

---

## Step 7: Output + Conformance Block

### Output target

- **File written**: `Pricing Migration/_root/04_communication_posture.md` (in-place edit; no new files).
- **Files NOT written**: NO new files; NO edits to any other `_root/` doc; NO edits to `_meta/`, `_archive/`, `_reference/`, format folders, or `entity-packets/`.

### Conformance block (per `_root/00_manifest.md §5` with Source-fix-Session-A-specific additions)

```
─── Source-fix Session A Conformance ─────────────────────────
Session task: Author three additive extensions to `_root/04_communication_posture.md` per Stage 4 prep operator stamps Q1 (CL-015 fix-now) + Q3 (audience register fix-root-04-1) + Q4 (SaaS-renewal forbids fix-now). One fresh-agent session; one doc edited in three places.
Output target: `Pricing Migration/_root/04_communication_posture.md` (in-place edit)

Manifest echo (per `_root/00_manifest.md §1 step 6` + `§6` — paste-quote ALL entries from §2 with title + Last-updated header date):
- 00 Root Doc Manifest — <date>
- C  Operator + Agent Contracts — <date>
- 01 Why We Are Migrating — <date>
- 02 Who Is Being Migrated — <date>
- 03 What We Sell — <date>
- 04 Communication Posture — <date>  ← the doc you are editing; report pre-edit Last-updated
- 05 Driver Taxonomy — <date>
- 06 Format Routing — <date>
- 07 Data Pipeline — <date>
- 08 Quality Bar — <date>
- 09 Changelog — <date>

Files read (with last-updated date / mtime):
- <enumerate every file from Step 1 reading list>

Files NOT read (per Step 1 "Do NOT read"):
- <enumerate>

CL-024 paste-verification (REQUIRED — paste-quote verbatim from source):
1. Appendix A.2 audience-register table + framing sentence:
<paste full table + sentence here, verbatim>
2. Appendix A.6 forbidden-framings list + formal-notice paragraph + Good News exception:
<paste full list + paragraphs here, verbatim>
3. `_meta/stage3_cleanup.md` CL-015 entry (full):
<paste entire CL-015 entry here, verbatim>
4. `_reference/2026-05-20__execution_plan_v3.3.md` §III Annual-overlay voice paragraph(s):
<paste relevant paragraph(s) here, verbatim; flag if §III prose is not explicit>

Extensions authored (per Step 2):
- Extension 1 — `_root/04 §1.1` (or equivalent): <line range; sub-section heading style chosen; 4-row table + framing sentence verbatim from Appendix A.2; cross-references added>
- Extension 2 — `_root/04 §3` row appends: <net new row count after coverage-map verification; coverage-map table per Step 4 verification step>
- Extension 3 — `_root/04 §4.16` (or `§5` extension): <line range; choice rationale; sub-section count if §4.16; total line count>

Coverage map for Extension 2 (per Step 4 verification step):
| Appendix A.6 forbid | Already in §3? (YES/NO + existing row line reference) | Action |
|---|---|---|
| <fill in> | <fill in> | <fill in> |

Path-reference contract verification (REQUIRED — count + enumerate):
- Inlined `_root/` rule prose in new extensions: COUNT = 0 (target). Each cross-reference to another `_root/` rule in your new prose is a `_root/XX §N.M` pointer, not an inline restatement.
- Cross-reference pointers added: <enumerate every `_root/XX §N.M` pointer in your three extensions>

Header `Last updated` annotation appended to `_root/04`:
<paste your new annotation here>

QB-NNN checks newly triggered (downstream — NOT this session's responsibility but flag for Source-fix Session B / planning-agent review pass):
- Extension 1 (§1.1 audience register): no new QB-NNN required (existing QB checks for audience-register-implicit forbids already exist).
- Extension 2 (§3 SaaS-renewal forbidden-phrase rows): new QB-NNN checks needed in `_root/08` for each new row (analog to existing per-forbid QB-NNN checks); flag for `_root/08` Source-fix Session B (Wave 6 batch).
- Extension 3 (§4.16 Annual-overlay voice): new QB-NNN checks needed in `_root/08` for renewal-date framing; flag for Source-fix Session B (Wave 6 batch) OR a separate `_root/08` Annual-voice QB session at planning-agent discretion.

Cross-doc propagation candidates (planning-agent review-pass scope; NOT your responsibility):
- `_root/06 §4.3` Annual overlay row — should cross-reference your new `_root/04 §4.16` (currently doesn't, per CL-015 entry "then update `_root/06 §4.3` to point to the new rule").
- `_root/00_manifest.md §4` topic-index — should add row for "Annual-cohort voice rules" pointing to `_root/04 §4.16` (currently the row was reclassified to "landing TBD per Stage 4 prep" at Stage 3.5 closeout manifest-hygiene sweep).
- `_root/00_manifest.md §2 row 4` — `_root/04` line count bump + Last-updated annotation appended.
- `_root/00_manifest.md §2 footer` cumulative recount.
- `_root/09_changelog.md` new entry documenting this session.

Gaps surfaced:
- <enumerate any gaps; e.g. exec plan v3.3 §III does not contain explicit Annual-voice prose at the expected location; renewal_date column missing from v6.2 header>
- <or: "none">

Conflicts between sources:
- <enumerate any conflicts; e.g. CL-015 cleanup-tracker note says §4.16 OR §5 extension — judgment surfaced in Extension 3 spec; etc.>
- <or: "none">

Open questions for operator:
- <enumerate; particularly: §4.16 vs §5 extension choice rationale; any Coverage-map ambiguities for Extension 2 (rows that partially overlap an existing §3 row)>
- <or: "none">
─────────────────────────────────────────────────────────────
```

---

## Step 8: If something is missing, contradictory, or unclear

**Flag in your conformance block; do NOT invent.**

Common scenarios:

- **Manifest dates disagree with file headers**: this is a §3-propagation failure per `_root/CONTRACTS.md §3`. Stop and flag (QB-125). Do not silently proceed.
- **Appendix A.2 or A.6 source text not present at cited location**: paste-verification per CL-024 fails. Stop and flag.
- **CL-015 entry not present or location-update note not present in `_meta/stage3_cleanup.md`**: paste-verification per CL-024 fails. Stop and flag.
- **Exec plan v3.3 §III does not contain explicit Annual-voice prose**: search for closest matching passage; paste-verify whatever is found; flag the partial match in conformance block; surface to operator for direction (operator may direct §III re-read with different scope OR may stamp Extension 3 authoring without exec-plan paste-quote based on CL-015 entry alone).
- **`renewal_date` column missing from v6.2 header**: your Extension 3 references `[RENEWAL_DATE]` placeholder which presumes v6.2 carries the column. Flag missing column; surface to operator + v6.2 maintainer. Do NOT add the column to v6.2 yourself (v6.2 is data layer, not rule layer).
- **`_root/04 §3` table row order convention unclear**: append at end of existing 27 rows (before `### §3.1` heading) and surface row-order question in conformance block; operator may direct re-ordering at review pass.
- **§4.16 vs §5 extension judgment call genuinely 50/50**: default to §4.16 standalone (matches §4.15 Parent-letter precedent); surface rationale in conformance block.

**Do NOT improvise around any of the above.** Stop, surface, await operator direction.

---

**End of Source-fix Session A prep prompt.** Paste-run this in a fresh Cursor agent chat. Fresh agent will produce the three `_root/04` extensions in-place + conformance block. Planning agent reviews + applies the `_root/CONTRACTS.md §3` propagation sweep (changelog entry + manifest bumps + topic-index update + `_root/06 §4.3` cross-reference update) at landing.
