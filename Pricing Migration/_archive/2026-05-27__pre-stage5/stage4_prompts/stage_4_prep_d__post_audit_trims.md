# Stage 4 prep — Source-fix Session D: Apply operator-stamped audit trims (post-Stage-4-prep-C self-audit pass)

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-27 by Stage 4 planning agent (post-Stage-4-prep-C self-audit pass; operator-stamped all 7 audit decisions per planning-agent recommendations 2026-05-27).
> **Output target**: APPLY the 5 operator-stamped trims (F1 + F2 + F4+F5 + F9+F10+F16 matrix rebuild) to canonical sources + file CL-029 + CL-030 + CL-031 at `_meta/stage3_cleanup.md` + write `_root/09_changelog.md` entry + refresh manifest §2 row 5 line count + manifest §2 footer cumulative recount + manifest Last-updated header. DEFERRED per operator stamp: F6 (Stage 4.3 launch); F14 (drafter judgment retained); F15 (Stage 5 finalization).
> **Estimated authored length**: ~80–120 line conformance block + 5 surgical source-file edits (no new files authored this session). Light-touch by design — the audit-pass already did the verification work; Session D is mechanical application + propagation discipline.
> **Dependency**: Stage 4 prep Session C (self-audit pass) CLOSED 2026-05-27. Operator stamps recorded at planning-agent recommendation tier (see Step 2 below for the 7 stamped decisions verbatim). CL-024 strict + paste-verification discipline operator-stamped 2026-05-26 — **applies to this session in full** (5 catches within Stage 4 to date — Stage 3.5 Thesis + Stage 4.2 bri + Stage 4.2 sca v1 + Stage 4.2 sca v2 audit→CL-028 + Stage 4 prep C audit pass).

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. That is **load-bearing** for this prompt. You are running Source-fix Session D per `_root/CONTRACTS.md §3` rule-change protocol applied to the operator-stamped audit decisions from Stage 4 prep Session C (the self-audit pass).

Your job is **mechanical application + propagation discipline**, NOT re-verification of the audit findings (those are operator-stamped; do not re-debate). You execute 5 surgical source-file edits with verbatim BEFORE → AFTER prose per the audit-pass spec, then sweep propagation per `_root/CONTRACTS.md §3` step 5.

**You will not invent new rules.** Every edit is either subtractive (cut conversational language; cut bloat) or replacing (point to authoritative source; rebuild stale table from ground truth). **Cleanups are SUBTRACTIVE or REPLACING, never ADDITIVE** per Appendix B.6.3 guardrail 3.

**You WILL re-verify the BEFORE prose at source before applying the AFTER prose** per CL-024 paste-verification protocol. If the BEFORE prose at source does not match the spec below (verbatim), STOP and flag per `_root/CONTRACTS.md §2` — do NOT silently reconcile.

---

## Step 1: Required reading (in this exact order) — STRICT MANIFEST-ECHO + PASTE-VERIFICATION CONTRACT

**Reading file mtimes is NOT the manifest echo.** The manifest echo requires reading `_root/00_manifest.md §2` table AND reading every `_root/` doc's header block AND echoing each doc's title + Last-updated date from the header in your first chat response.

If you cannot produce the canonical manifest echo, your session is not ready to execute; STOP and flag per `_root/CONTRACTS.md §2`.

**Additionally — paste-verification requirement (CL-024)**: in your conformance block, you must paste-quote the FULL TEXT of the following operator-stamped source passages, verbatim from the source files:

1. `_root/05 §2.4.1` line 349 verbatim (BEFORE prose for F1).
2. `_root/05 §2.4.7` line 429 verbatim (BEFORE prose for F2).
3. `_root/05 §4` Section 4 weaving matrix (lines 790–806) verbatim (BEFORE prose for F9+F10+F16).
4. `_root/05 §2.4.7` line 424 verbatim (BEFORE prose for F9+F10+F16 propagation — "21 occurrences" inline count).
5. `_root/00_manifest.md` Last-updated header (line 7) verbatim — first 200 chars + last 200 chars (BEFORE prose anchor for F5; full ~10,200-char header would burst chat).

If you cannot paste-quote any of these passages because the source text is not present at the cited location, STOP and flag per QB-125 propagation-failure rule. Do NOT proceed to application.

### Folder orientation (mandatory — echo in conformance block per `_root/00_manifest.md §6`)

1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/00_manifest.md` — read in FULL (this session edits row 0 self-row + row 5 + row 7 + row 9 cell annotations + Last-updated header + §2 footer cumulative recount).
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md` — §3 rule-change protocol is the discipline this session follows.
5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/09_changelog.md` — read every 2026-05-26 entry + read CL-027 + CL-028 RESOLVED entries (your CL-029 + CL-030 + CL-031 entries will land here following the same pattern).

### The rule layer — read in FULL for the docs you will edit

6. `_root/05_driver_taxonomy.md` — read in FULL (this session edits §2.4.1 line 349 + §2.4.7 line 429 + §2.4.7 line 424 + §4 weaving matrix lines 790–806).

### The rule layer — read for orientation (you will NOT edit these but the audit-pass discipline depends on understanding the full rule layer)

7. `_root/01_why_we_are_migrating.md` (188L)
8. `_root/02_who_is_being_migrated.md` (244L)
9. `_root/03_what_we_sell.md` (173L)
10. `_root/04_communication_posture.md` (568L) — particularly §3 (forbidden phrases) + §4.2 (lede stat guardrail; F15 deferral context) + §4.11 (How This Compares; F14 deferral context)
11. `_root/06_format_mapping.md` (319L)
12. `_root/07_data_pipeline.md` (477L) — particularly §4.5 (post-CL-028 AND-discipline)
13. `_root/08_qa_checklist.md` (960L)

### Source materials for the audit-pass closeout

14. `_meta/stage4_prompts/stage_4_prep_c__self_audit_pass.md` (321L) — **explicit per-prompt authorization to read this file**. The audit-pass prompt this Session D implements against.
15. `_meta/stage3_cleanup.md` — **explicit per-prompt authorization to read this file**. Read the CL-027 + CL-028 entries (pattern templates for the CL-029 + CL-030 + CL-031 entries you'll author).
16. `_master-account-data-v6.2.csv` — **explicit per-prompt authorization to read** (Appendix B canonical data). REQUIRED for F9+F10+F16 matrix rebuild verification (you re-derive the 23-row ground truth via `csv.DictReader` per Appendix B.5.1 discipline; expected counts supplied in Step 3 Fix 3 below).

### Files NOT to read (per AGENTS.md hard rules; explicit re-statement for this session)

- `_archive/**` — anti-archive rule per `_root/CONTRACTS.md §4`.
- `Migration-Health Artifacts/**` — out of scope.
- `_reference/**` — out of scope.
- `_meta/stage2_prompts/**` + `_meta/stage3_prompts/**` — out of scope.
- `_meta/stage4_prompts/_paste-ready/**` — out of scope for this session (F6 paste-ready trim is DEFERRED to Stage 4.3 launch per operator stamp).
- `format-*-notices/*.md` per-account artifacts — out of scope (Session D edits rule layer + manifest; no per-account artifact touches).

---

## Step 2: Operator-stamped audit decisions (verbatim from Stage 4 prep Session C closeout 2026-05-27)

The operator stamped "stamp all per recommendations" on 2026-05-27 against the planning-agent recommendation table from the Stage 4 prep Session C self-audit pass. The 7 decisions are:

| # | Finding | Operator stamp | Action this session |
|---|---|---|---|
| F1 | `_root/05 §2.4.1` line 349 conversational debug language + stale enumeration | **APPLY NOW** (`f1_apply`) | Apply per Step 3 Fix 1 below |
| F2 | `_root/05 §2.4.7` line 429 conversational debug language ("Wait —") | **APPLY NOW** (`f2_apply`) | Apply per Step 3 Fix 2 below |
| F4 + F5 | `_root/00_manifest.md` cell annotations + Last-updated header bloat | **APPLY NOW — FULL** (`f4f5_apply_now`) | Apply per Step 3 Fix 4 + Fix 5 below |
| F6 | `_meta/stage4_prompts/_paste-ready/stage_4_2__*.md` paste-ready bloat | **DEFER to Stage 4.3 cohort launch** (`f6_defer_stage43`) | NO action this session; log deferral in CL-029 changelog entry |
| F9 + F10 + F16 | `_root/05 §4` weaving matrix stale numbers + contradictions + missing rows | **OPTION A — Full 23-row rebuild totaling 107** (`matrix_full_rebuild`) | Apply per Step 3 Fix 3 below |
| F14 | `_root/04 §4.11` "How This Compares" default-omit codification | **Keep drafter judgment + QB-071 pointer** (`f14_drafter_judgment`) | NO action this session; log decision in CL-029 changelog entry |
| F15 | `_root/04 §4.2` lede 4th-stat health-component variant | **DEFER to Stage 5 finalization** (`f15_defer_stage5`) | NO action this session; log deferral in CL-029 changelog entry |

**Hierarchical fix-priority sequencing per Appendix B.6.3 guardrail 4** (contradictions > stale numbers > conversational debug language > bloat):

1. **F9+F10+F16 matrix rebuild** (HIGHEST — contradictions + stale numbers) → apply first.
2. **F1 + F2 conversational debug language** → apply second (same `_root/05` doc; bundle with matrix rebuild as one Source-fix Session D-1 = `_root/05` consolidated edit pass).
3. **F4 + F5 manifest bloat** → apply third (single Source-fix Session D-2 = `_root/00_manifest.md` consolidated prune pass).

---

## Step 3: The 5 source-fixes to apply (per-fix spec with BEFORE → AFTER prose)

### Fix 1: F1 — `_root/05 §2.4.1` line 349 trim

**Source location**: `_root/05_driver_taxonomy.md` line 349.

**Verify BEFORE prose at source** (paste-quote in conformance block per CL-024):

> - **TBI-primary + IUR-secondary (9 accounts; expansion-shape 25→40)** — `bri` (row 65, re-stamped from IUR primary 2026-05-26) + `bcf` (row 101, re-stamped from ABTS primary 2026-05-26 — note: `bcf` was re-stamped TBI→URN in the next iteration of joint resolution; see CL-027 RESOLVED entry — `bcf` lives in the URN+IUR cohort below) + 8 CL-023 cluster (`ihw`/`sccon`/`ali`/`vic`/`ih`/`fc`/`ta`/`sbmh`). Integrated at §2.3.2 / §2.3.3 sub-block ("Additionally, the included user base for this tier is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]" — expansion-baked prose accommodates the 25→40 shape directly). See §2.3.7 for full enumeration + §4 weaving matrix row 3.

**Apply AFTER prose** (subtractive cleanup — cut `bcf` + cut "— note: ..." parenthetical; restore heading-vs-list parity to 9 accounts):

> - **TBI-primary + IUR-secondary (9 accounts; expansion-shape 25→40)** — `bri` (row 65, re-stamped from IUR primary 2026-05-26) + 8 CL-023 cluster (`ihw`/`sccon`/`ali`/`vic`/`ih`/`fc`/`ta`/`sbmh`). Integrated at §2.3.2 / §2.3.3 sub-block ("Additionally, the included user base for this tier is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]" — expansion-baked prose accommodates the 25→40 shape directly). See §2.3.7 for full enumeration + §4 weaving matrix row 3.

**Rationale** (do NOT re-debate; this is operator-stamped): conversational debug language from CL-027 in-session iteration. Cross-reference to bcf's URN-primary status is already canonical at §2.1.7 + §2.4.7 line 430 + §4 weaving matrix row 5 — no information loss. Heading "(9 accounts)" mismatched list of 10 names pre-trim; restored to 9 names post-trim.

**Line-change**: −1 line (cut the "+ `bcf` (row 101, ...)" sub-phrase + parenthetical; single line collapses).

---

### Fix 2: F2 — `_root/05 §2.4.7` line 429 trim

**Source location**: `_root/05_driver_taxonomy.md` line 429.

**Verify BEFORE prose at source** (paste-quote in conformance block per CL-024):

> - **TBI primary + IUR secondary (9 accounts; 25→40 expansion shape)** — operator-stamped 2026-05-26 via CL-026 / CL-023 joint resolution: `bri` (Bulbrite, row 65 — re-stamped from IUR primary 2026-05-26), 8 CL-023 cluster (`ihw` / `ali` / `vic` / `ih` / `fc` / `ta` / `sbmh` + `sccon` — secondary_drivers re-coded URN → IUR 2026-05-26; `sccon` preserves MOR annotation per entity-child judgment). Wait — `bcf` was re-stamped to URN-primary in the same joint resolution iteration; not in this TBI cohort. (Per CL-027 RESOLVED, see the §2.1.7 enumeration for the URN-primary cohort below.) Integrated at §2.3.2 / §2.3.3 sub-block ("Additionally, the included user base for this tier is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]"); the §2.3.2 expansion-baked prose accommodates the 25→40 shape directly.

**Apply AFTER prose** (subtractive cleanup — cut "Wait —" sentence + parenthetical; cross-ref already canonical at §2.1.7):

> - **TBI primary + IUR secondary (9 accounts; 25→40 expansion shape)** — operator-stamped 2026-05-26 via CL-026 / CL-023 joint resolution: `bri` (Bulbrite, row 65 — re-stamped from IUR primary 2026-05-26), 8 CL-023 cluster (`ihw` / `ali` / `vic` / `ih` / `fc` / `ta` / `sbmh` + `sccon` — secondary_drivers re-coded URN → IUR 2026-05-26; `sccon` preserves MOR annotation per entity-child judgment). Integrated at §2.3.2 / §2.3.3 sub-block ("Additionally, the included user base for this tier is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]"); the §2.3.2 expansion-baked prose accommodates the 25→40 shape directly.

**Rationale**: "Wait —" is conversational debug-language artifact from CL-027 in-session iteration; bcf URN-primary status is canonical at §2.1.7 + §4 weaving matrix row 5. Cross-ref preserved via the §2.4.7 → §4 weaving matrix pointer at line 432.

**Line-change**: −1 line (cut the "Wait — `bcf` was re-stamped..." sentence + parenthetical; line collapses).

---

### Fix 3: F9+F10+F16 — `_root/05 §4` weaving matrix rebuild + §2.4.7 line 424 inline count fix

**HIGHEST PRIORITY per Appendix B.6.3 guardrail 4** (contradictions + stale numbers).

#### Fix 3a: `_root/05 §4` weaving matrix rebuild (lines 790–806)

**Verify BEFORE prose at source** (paste-quote the full Section 4 matrix in conformance block per CL-024 — lines 790 through 806 verbatim).

**Verify ground truth via `csv.DictReader` on `_master-account-data-v6.2.csv`** per Appendix B.5.1 discipline. Expected counts (planning-agent pre-derived; you re-verify):

| Primary | Secondary | Count | Named accounts |
|---|---|---:|---|
| URN | (none) | 11 | (re-derive from CSV: rows where `migration_driver=user_rate_normalization` AND `secondary_drivers` is blank) |
| URN | IUR | 20 | (re-derive: 25 URN+IUR-secondary minus 6 URN+MOR+IUR compound minus 1 URN+MOR = ... cross-check via CSV) |
| URN | MOR+IUR | 6 | `wac` / `sbl` / `fms` / `tla` / `mli` / `vcg` (re-verify) |
| URN | MOR | 1 | (re-derive from CSV) |
| IUR | (none) | 9 | (re-derive from CSV; post-CL-026 bri re-stamp) |
| IUR | ADR | 1 | (re-derive from CSV) |
| TBI | (none) | 4 | (re-derive from CSV) |
| TBI | IUR | 8 | `bri` + 7 CL-023 cluster excluding `sccon` (re-verify; note `sccon` belongs in TBI+MOR+IUR per compound stamp) |
| TBI | MOR+IUR | 1 | `sccon` (re-verify) |
| MOR | URN | 4 | `scw` + 3 others (re-derive from CSV) |
| MOR | URN+IUR | 2 | (re-derive from CSV) |
| ABTS | (none) | 9 | (re-derive from CSV; post-CL-026 bcf re-stamp out) |
| ADR | URN | 1 | (re-derive from CSV) |
| ADR | (none) | 1 | (re-derive from CSV) |
| PDC | URN | 5 | (re-derive from CSV) |
| PDC | IUR | 2 | (re-derive from CSV) |
| PDC | URN+IUR | 5 | (re-derive from CSV) |
| PDC | (none) | 4 | (re-derive from CSV) |
| PDC | MOR+URN | 1 | (re-derive from CSV) |
| SA | (none) | 1 | (re-derive from CSV) |
| MC | (none) | 8 | (re-derive from CSV) |
| UCV | (none) | 2 | (re-derive from CSV) |
| RA | (none) | 1 | (re-derive from CSV) |

**Aggregate ground truth**: 11+20+6+1+9+1+4+8+1+4+2+9+1+1+5+2+5+4+1+1+8+2+1 = **107** (reconciles to §1.1 driver-inventory totals: URN 38 + IUR 10 + TBI 13 + MOR 6 + ABTS 9 + ADR 2 + PDC 17 + SA 1 + MC 8 + UCV 2 + RA 1 = 107 ✓).

**Apply AFTER prose** — replace lines 790–806 with the 23-row rebuilt matrix. Use the structure below as the template; **populate "Named accounts" cells from your `csv.DictReader` re-derivation, NOT from the planning-agent pre-derivation above** (CL-024 paste-verification discipline applies — you are the canonical author of the named enumeration):

> ## Section 4 — Secondary-driver weaving matrix
>
> The matrix below enumerates **all** primary-secondary combinations v6.2 actually exhibits (post-CL-026 / CL-023 / CL-027 joint resolution 2026-05-26 + CL-030 RESOLVED 2026-05-27 full-matrix rebuild from `csv.DictReader` ground truth). It is the operational artifact Stage 4 drafters consult after picking the primary block from §2 or §3.
>
> | Primary | Secondary | Occurrences in v6.2 | What changes about the primary block |
> |---|---|---:|---|
> | `user_rate_normalization` | (none) | 11 | Apply §2.1 canonical block as-is. Apply default close per `_root/04 §4.5` and billing-basis footnote per `_root/04 §4.9`. |
> | `user_rate_normalization` | `included_user_reduction` | 26 (25 REDUCTION + 1 EXPANSION = `bcf`) | §2.1 primary block + one of two direction-specific sub-paragraphs per the post-CL-027 §2.1.2 / §2.1.3 sub-block pair: REDUCTION accounts use the `[IF excess users remain AND secondary driver = included_user_reduction (base shrinking from legacy to current tier standard)]` "Your included base is also adjusting from the legacy [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED]" sub-block; EXPANSION (`bcf`) uses the `[IF excess users remain AND new included base > legacy included base (base expanding)]` "expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED] — absorbing [N] users" sub-block. Mutually exclusive (exactly one fires per account). Apply IUR-variant close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9`. See §2.1.7 for named enumeration. |
> | `user_rate_normalization` | `multi_org_retirement, included_user_reduction` | 6 | `wac` / `sbl` / `fms` / `tla` / `mli` / `vcg` (URN-primary; MOR + IUR compound secondary). §2.1 primary block + the REDUCTION sub-block (per §2.1.2 / §2.1.3 post-CL-027); MOR portion is annotation-only at URN-primary scope (no MOR-secondary sub-block under URN primary per §2.1.7). Apply IUR-variant close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9`. |
> | `user_rate_normalization` | `multi_org_retirement` | 1 | Re-derive named account from CSV. §2.1 primary block + MOR portion annotation-only at URN-primary scope (no MOR-secondary sub-block under URN primary). Apply default close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9`. |
> | `included_user_reduction` | (none) | 9 | Apply §2.4 canonical block as-is. Apply IUR-variant close per `_root/04 §4.5` and billing-basis footnote per `_root/04 §4.9`. (Post-CL-026 / CL-023 joint resolution 2026-05-26: count 10→9 after `bri` re-stamping out to TBI primary.) |
> | `included_user_reduction` | `annual_discount_retirement` | 1 | Re-derive named account from CSV. §2.4 primary block + per-account narrative integration of the ADR move (no canonical IUR+ADR sub-block; see §6 flag). Apply IUR-variant close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9`. |
> | `tier_base_increase` | (none) | 4 | Apply §2.3 canonical block as-is. Apply default close per `_root/04 §4.5` and billing-basis footnote per `_root/04 §4.9`. |
> | `tier_base_increase` | `included_user_reduction` | 8 | `bri` + 7 CL-023 cluster (`ihw` / `ali` / `vic` / `ih` / `fc` / `ta` / `sbmh`). §2.3 primary block + the `[IF secondary driver = included_user_reduction]` sub-block "Additionally, the included user base for this tier is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]" (25→40 EXPANSION shape per CL-026 / CL-023 Option A primary-vs-secondary semantic clarification). Apply IUR-variant close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9`. (Post-CL-027 + CL-030: `bcf` removed from this cohort — re-stamped TBI→URN per CL-027; canonical home is URN row above.) |
> | `tier_base_increase` | `multi_org_retirement, included_user_reduction` | 1 | `sccon` (Summer Classics Contract). §2.3 primary block + IUR sub-block (fires from IUR portion of compound secondary stamp); MOR portion is annotation-only at TBI-primary scope. Apply IUR-variant close + billing-basis footnote. |
> | `multi_org_retirement` | `user_rate_normalization` | 4 | Re-derive named accounts from CSV (includes `scw` per CL-026 / CL-023 joint resolution; CL-030 RESOLVED 2026-05-27 corrected count 1→4). §2.6 primary block + per-account narrative integration of the URN move (no canonical MOR + URN sub-block; see §6 flag). Apply default close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9` if URN integration produces user-charge change. |
> | `multi_org_retirement` | `user_rate_normalization, included_user_reduction` | 2 | Re-derive named accounts from CSV. §2.6 primary block + per-account narrative integration of the compound URN+IUR moves. Apply IUR-variant close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9`. |
> | `at_book_tier_shift` | (none) | 9 | Apply §2.5 canonical block as-is. Apply default close per `_root/04 §4.5`. (CL-027 reduction `bcf` re-stamped out 2026-05-26 → URN-primary; remaining 9 are book-canonical ABTS accounts.) |
> | `annual_discount_retirement` | `user_rate_normalization` | 1 | Re-derive named account from CSV. §2.7 primary block + per-account narrative integration of URN move. Apply default close per `_root/04 §4.5`. |
> | `annual_discount_retirement` | (none) | 1 | Apply §2.7 canonical block as-is. Apply default close per `_root/04 §4.5`. |
> | `pre_discount_correction` | `user_rate_normalization` | 5 | Re-derive named accounts from CSV. Per-account narrative integration (no canonical PDC sub-block matrix; see §6 flag). Apply default close per `_root/04 §4.5`. |
> | `pre_discount_correction` | `included_user_reduction` | 2 | Re-derive named accounts from CSV. Per-account narrative integration of IUR move. Apply IUR-variant close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9`. |
> | `pre_discount_correction` | `user_rate_normalization, included_user_reduction` | 5 | Re-derive named accounts from CSV. Per-account narrative integration of compound URN+IUR. Apply IUR-variant close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9`. |
> | `pre_discount_correction` | (none) | 4 | Per-account narrative integration of the discount-correction move. Apply default close per `_root/04 §4.5`. |
> | `pre_discount_correction` | `multi_org_retirement, user_rate_normalization` | 1 | Re-derive named account from CSV. Per-account narrative integration of compound MOR+URN. Apply default close per `_root/04 §4.5`. |
> | `seat_acquisition` | (none) | 1 | Re-derive named account from CSV. Apply §2.X canonical block (re-derive driver section §N from §1.1) as-is. Apply default close per `_root/04 §4.5`. |
> | `mid_cycle_change` | (none) | 8 | Re-derive named accounts from CSV. Apply §2.X canonical block (re-derive driver section §N from §1.1) as-is. Apply default close per `_root/04 §4.5`. |
> | `unspecified_contract_variance` | (none) | 2 | Re-derive named accounts from CSV. Apply §2.X canonical block (re-derive driver section §N from §1.1) as-is. Apply default close per `_root/04 §4.5`. |
> | `re_aligned` | (none) | 1 | Re-derive named account from CSV. Apply §2.X canonical block (re-derive driver section §N from §1.1) as-is. Apply default close per `_root/04 §4.5`. |
>
> **Total combinations enumerated: 23** (post-CL-030 RESOLVED 2026-05-27 full-matrix rebuild from `csv.DictReader` ground truth). **Aggregate v6.2-exhibited primary-secondary occurrences across the 23 rows**: 11+26+6+1+9+1+4+8+1+4+2+9+1+1+5+2+5+4+1+1+8+2+1 = **107** (reconciles to §1.1 driver-inventory totals: URN 38 + IUR 10 + TBI 13 + MOR 6 + ABTS 9 + ADR 2 + PDC 17 + SA 1 + MC 8 + UCV 2 + RA 1 = 107 ✓).
>
> **Constraint reminder**: do not enumerate hypothetical combinations. If a future v6.2 update introduces a new combination beyond the 23 enumerated above, the integration is undocumented; flag per `_root/CONTRACTS.md §2` and ask the operator before drafting.
>
> **Format A note**: Format A's mechanical scope (delta ≤ 10% / ≤ $80) means the matrix above applies primarily to Format B and CEO Letter. Format A integrates secondaries via the per-account narrative pattern shown in the kii exemplar (`at_book_tier_shift` primary + IUR-style included-base move integrated inline).

**Line-change**: +~14 lines (matrix grows 9→23 rows; aggregate footer rewritten). Acceptable per operator stamp on Option A full rebuild.

#### Fix 3b: `_root/05 §2.4.7` line 424 inline "21 occurrences" stale count fix

**Source location**: `_root/05_driver_taxonomy.md` line 424.

**Verify BEFORE prose at source** (paste-quote in conformance block per CL-024):

> - **Standalone IUR primary, no secondary (21 occurrences in the v6.2 secondary-combinations tally — the most common secondaries pattern, here referring to IUR being secondary under another primary; standalone IUR primary with no secondary is also represented in the 10 IUR primary rows when secondary is blank — post-CL-026 / CL-023 joint resolution 2026-05-26 the count is 10, was 11 pre-resolution before `bri` re-stamping).** Apply the canonical block as-is.

**Apply AFTER prose** (subtractive — the "21 occurrences" inline cross-reference is stale post-CL-027; clarify that the canonical IUR-primary count is 9 with secondary=(none) per the rebuilt §4 matrix row 5):

> - **Standalone IUR primary, no secondary (9 occurrences post-CL-026 / CL-023 / CL-027 joint resolution 2026-05-26 — was 10 pre-CL-027 sweep; was 11 pre-CL-026/CL-023 before `bri` re-stamping; see §4 weaving matrix row 5).** Apply the canonical block as-is.

**Rationale**: "21 occurrences" was an obsolete cross-reference to a pre-CL-027 IUR-as-secondary tally that didn't reconcile to the §4 matrix (was conflating "IUR-as-secondary across all primaries" with "IUR-primary-no-secondary"). Post-CL-030 matrix rebuild, IUR-as-secondary across all primaries = 44 (8 TBI+IUR + 26 URN+IUR + 6 URN+MOR+IUR + 2 PDC+IUR + 5 PDC+URN+IUR — wait, re-verify against rebuilt matrix). Net: cite canonical §4 matrix row directly; do NOT replicate inline counts.

**Line-change**: 0 lines (single-line replacement).

---

### Fix 4: F4 — `_root/00_manifest.md` cell annotations REPLACING

**Source location**: `_root/00_manifest.md` §2 manifest table cells for row 0 (self-row) + row 5 (`_root/05`) + row 7 (`_root/07`) + row 9 (`_root/09`).

**Verify BEFORE prose at source** (the 4 cell annotations are MASSIVE — paste-quote first 100 chars + last 100 chars of each cell in conformance block, NOT the full ~3,000+ word cells which would burst chat). Anchor each excerpt with line number + cell column.

**Apply AFTER prose** (REPLACING per Appendix B.6.3 guardrail 3 example — relocate cumulative narrative to `_root/09_changelog.md` canonical home; keep §2 cells as one-line summaries with `→ see _root/09 <date> entries chain` pointer):

For **row 0 self-row** (the manifest's own row in §2): replace the multi-paragraph cell with:

> `_root/00_manifest.md` — 229 lines — 2026-05-27 (Source-fix Session D 2026-05-27 applied operator-stamped Stage 4 prep Session C audit trims; cell annotations + Last-updated header pruned per CL-031 RESOLVED REPLACING discipline; → see `_root/09_changelog.md` 2026-05-22 through 2026-05-27 entries chain for full history).

For **row 5** (`_root/05_driver_taxonomy.md`): replace the multi-paragraph cell with:

> `_root/05_driver_taxonomy.md` — [NEW_LINE_COUNT post-Fixes 1+2+3] lines — 2026-05-27 (Source-fix Session D 2026-05-27 applied audit trims F1 + F2 conversational debug language + F9+F10+F16 §4 weaving matrix full rebuild from `csv.DictReader` ground truth + §2.4.7 line 424 inline count fix; → see `_root/09_changelog.md` 2026-05-27 entry for full diff).

For **row 7** (`_root/07_data_pipeline.md`): replace the multi-paragraph cell with:

> `_root/07_data_pipeline.md` — 477 lines — 2026-05-26 (CL-028 RESOLVED §4.5 reconciliation-flag AND-discipline tightening; → see `_root/09_changelog.md` 2026-05-26 entries chain for full history).

For **row 9** (`_root/09_changelog.md`): replace the multi-paragraph cell with:

> `_root/09_changelog.md` — [NEW_LINE_COUNT post-Session-D entry] lines — 2026-05-27 (Source-fix Session D 2026-05-27 closeout entry absorbed; → see this doc's entries chain for full history).

**Line-change**: ~−2,800 lines across the 4 cells (cumulative narrative footprint exits manifest; canonical content already exists at `_root/09` so no information loss).

---

### Fix 5: F5 — `_root/00_manifest.md` Last-updated header pruning

**Source location**: `_root/00_manifest.md` line 7 (the `> **Last updated**: ...` paragraph in the header blockquote).

**Verify BEFORE prose at source** (paste-quote first 200 chars + last 200 chars in conformance block; full ~10,200-char single-line paragraph would burst chat).

**Apply AFTER prose** (REPLACING per Appendix B.6.3 guardrail 3 example — prune to latest 2–3 changes + pointer to `_root/09` for prior history):

> **Last updated**: 2026-05-27 (**Source-fix Session D 2026-05-27 — operator-stamped Stage 4 prep Session C audit trims applied**: F1 + F2 conversational debug language trim at `_root/05 §2.4.1` + `_root/05 §2.4.7` (−2 lines); F9+F10+F16 `_root/05 §4` weaving matrix full rebuild from `csv.DictReader` ground truth (9→23 rows; aggregate 83→107 reconciles to §1.1) + §2.4.7 line 424 inline count fix; F4 + F5 manifest §2 cell annotations + Last-updated header REPLACING bloat trim (~−5,300 lines via pointer-replacement to `_root/09`). F6 paste-ready trim DEFERRED to Stage 4.3 cohort launch; F14 §3m default-omit DEFERRED to Stage 5 finalization (drafter judgment retained); F15 lede 4th-stat health-component variant DEFERRED to Stage 5 finalization. Fifth CL-024 paste-verification carry-forward within Stage 4 (Stage 3.5 Thesis + Stage 4.2 bri + Stage 4.2 sca v1 + Stage 4.2 sca v2 audit→CL-028 + Stage 4 prep C audit pass). row 0 self-row 229 → [NEW_COUNT]; row 5 `_root/05` 850 → [NEW_COUNT]; row 9 `_root/09` 727 → [NEW_COUNT]; §2 footer cumulative recount 4,742 → [NEW_FOOTER]. → see `_root/09_changelog.md` 2026-05-22 through 2026-05-27 entries chain for prior changes.)

**Line-change**: ~−2,500 lines (single mega-paragraph collapses to ~3-paragraph latest-change summary).

---

## Step 4: Propagation sweep per `_root/CONTRACTS.md §3` step 5

After applying Fixes 1 + 2 + 3 + 4 + 5, sweep propagation in this exact order:

1. **`wc -l` ground-truth refresh** for `_root/05_driver_taxonomy.md` post-Fixes 1+2+3 (expected: 850 − 2 + ~13 = ~861 lines; re-verify).
2. **`wc -l` ground-truth refresh** for `_root/00_manifest.md` post-Fixes 4+5 (expected: ~229 − ~5,300 across cell + header collapse; re-verify — note: the manifest's own `.md` line count won't drop by ~5,300 since most of the bloat is in single mega-paragraph cells; actual line-count drop is closer to the markdown-paragraph count differential).
3. **`wc -l` ground-truth refresh** for `_root/09_changelog.md` post-Session-D entry (expected: 727 + ~40 = ~767 lines; re-verify).
4. **Manifest §2 row 5 line-count cell refresh**: 850 → new count from step 1.
5. **Manifest §2 row 9 line-count cell refresh**: 727 → new count from step 3.
6. **Manifest §2 footer cumulative recount**: sum of all 11 row line-count cells; update the footer "Sum of §2 rows: N" line.
7. **Manifest row 0 self-row line-count refresh** if any new topic-index rows added (none expected this session — Session D is in-place edits, no new §4 topic-index rows).
8. **`_root/09_changelog.md` entry authoring** — file a single Session D entry under 2026-05-27 with the format below:

```
**2026-05-27 — Source-fix Session D applied (Stage 4 prep Session C audit-pass operator-stamped trims; 5 fixes across `_root/05` + `_root/00_manifest.md`)**

CL-029 RESOLVED at `_root/05 §2.4.1` line 349 + `_root/05 §2.4.7` line 429 — F1 + F2 conversational debug language trim per Stage 4 prep Session C audit-pass operator stamps `f1_apply` + `f2_apply` 2026-05-27. Subtractive cleanup: cut `bcf` from §2.4.1 9-account enumeration (heading-vs-list parity restored to 9; bcf canonical home is URN-primary per CL-027 + §2.1.7 + §4 row 5); cut "Wait — `bcf` was re-stamped..." sentence from §2.4.7 (cross-ref preserved via §2.4.7 → §4 weaving matrix pointer at line 432). Line-change: `_root/05` 850 → 848 (−2). No v6.2 re-stamps. No paste-ready refreshes (per-account artifacts do not reference these lines).

CL-030 RESOLVED at `_root/05 §4` weaving matrix + `_root/05 §2.4.7` line 424 — F9 + F10 + F16 stale numbers + contradictions + missing rows + arithmetic-doesn't-reconcile per Stage 4 prep Session C audit-pass operator stamp `matrix_full_rebuild` 2026-05-27. REPLACING cleanup: rebuilt §4 matrix from `csv.DictReader` ground truth (9→23 rows; aggregate 83→107 reconciles to §1.1 driver-inventory totals); fixed §2.4.7 line 424 stale "21 occurrences" cross-reference to cite §4 matrix row directly. Line-change: `_root/05` 848 → [NEW_COUNT] (+~14). No v6.2 re-stamps (rule-layer-only matrix-rebuild; the underlying CSV is canonical and unchanged). No paste-ready refreshes (drafters route off v6.2 + §1.1; §4 matrix is operational reference not routing gate). The matrix rebuild closes a CL-027 propagation gap (bcf TBI-cohort double-counting) + 4 stale-number drifts (rows 1+2+6+7+8+9) + 14 missing-row drifts (PDC enumerated + IUR+ADR + ABTS + SA + MC + UCV + RA + others).

CL-031 RESOLVED at `_root/00_manifest.md` row 0 + row 5 + row 7 + row 9 cell annotations + Last-updated header — F4 + F5 cumulative-narrative bloat per Stage 4 prep Session C audit-pass operator stamp `f4f5_apply_now` 2026-05-27. REPLACING cleanup per Appendix B.6.3 guardrail 3 example: relocated ~3,000+ word cumulative narrative per cell + ~1,500-word Last-updated header narrative to `_root/09_changelog.md` (canonical narrative-history home); kept §2 cells + header as one-line summaries with `→ see _root/09 <date> entries chain` pointer. Line-change: manifest ~−5,300 character-density reduction; markdown-line count drop ~−[NEW_COUNT verified by wc -l]. No information loss (cumulative content exists verbatim at `_root/09`). Manifest §2 footer cumulative recount 4,742 → [NEW_FOOTER]. row 0 self-row 229 → [NEW_COUNT]; row 5 `_root/05` line-count refresh 850 → [NEW_COUNT post-CL-029+CL-030]; row 7 `_root/07` unchanged at 477; row 9 `_root/09` 727 → [NEW_COUNT post-Session-D entry].

**Deferrals logged (Stage 4 prep Session C operator stamps; no source action this session)**:

- F6 paste-ready bloat (`_meta/stage4_prompts/_paste-ready/stage_4_2__*.md`) — operator stamp `f6_defer_stage43`: trim deferred to Stage 4.3 cohort launch (natural template-refresh boundary; preserves Stage 4.2 cci + sca + bri-pending audit-trail context mid-cohort).
- F14 `_root/04 §4.11` §3m default-omit codification — operator stamp `f14_drafter_judgment`: 3-of-3 URN-primary §3m omissions kept as drafter judgment with QB-071 pointer; reassess at 5+ consecutive or Stage 5 finalization.
- F15 `_root/04 §4.2` lede 4th-stat health-component variant — operator stamp `f15_defer_stage5`: translation discipline (health-data → operational signal phrasing) deferred to Stage 5 finalization bulk-production gate; aligns with F14 codification timing.

**CL-024 paste-verification status**: 5th catch within Stage 4 (Stage 3.5 Thesis + Stage 4.2 bri + Stage 4.2 sca v1 + Stage 4.2 sca v2 audit→CL-028 + Stage 4 prep C audit pass). Discipline operationally robust; 0 paste-drift detected in Session D execution.

**v6.2 driver-stamp baseline**: unchanged at 91.6% clean (98/8/1) — Session D was rule-layer-only (no v6.2 re-stamps).

**Hierarchical fix-priority distribution closed this session**:
- Contradictions: 1 cluster (F9+F10+F16 matrix rebuild — bcf double-counting contradiction with CL-027 + §1.1) ✓
- Stale numbers: 1 cluster (F9+F10+F16 matrix counts + §2.4.7 line 424) ✓
- Conversational debug language: 2 (F1 §2.4.1 + F2 §2.4.7) ✓
- Bloat: 2 (F4 manifest cells + F5 manifest header) ✓
```

9. **`_meta/stage3_cleanup.md` CL-029 + CL-030 + CL-031 RESOLVED entries** — file three RESOLVED entries mirroring the CL-028 RESOLVED pattern at lines 315–325. Each carries: Source / Fix applied / Operator stamp / Status. Use the CL-029 + CL-030 + CL-031 framing from the `_root/09` entry above as the body.

10. **Conformance block** — produce per Step 5 below.

---

## Step 5: Conformance block (paste-into-final-response template)

Use the canonical format from `_root/00_manifest.md §5` with these Session-D-specific additions:

```
─── Conformance Block (Stage 4 prep Source-fix Session D — Apply operator-stamped audit trims) ─────────
Session task: Apply 5 operator-stamped trims from Stage 4 prep Session C self-audit pass per `_root/CONTRACTS.md §3` rule-change protocol. CL-029 + CL-030 + CL-031 RESOLVED. F6 + F14 + F15 deferrals logged.
Output target: 5 source-file edits (3 to `_root/05` + 2 to `_root/00_manifest.md`) + CL-029 + CL-030 + CL-031 entries at `_meta/stage3_cleanup.md` + Session D entry at `_root/09_changelog.md` + manifest §2 row 5 + row 9 line-count refreshes + manifest §2 footer cumulative recount.

Manifest echo (per `_root/00_manifest.md §1 step 6 + §6` — paste-quote ALL 11 ENTRIES from §2 with title + Last-updated header date verified at source per CL-024):
[paste-quote 11 entries verbatim]

Files read (with last-updated date / mtime):
[list every file from Step 1 with last-updated date or mtime]

Files edited:
- `_root/05_driver_taxonomy.md` (F1 + F2 + F3a + F3b): 850 → [NEW_COUNT] lines
- `_root/00_manifest.md` (F4 + F5 + row 5 + row 9 + footer recount): 229 → [NEW_COUNT] lines
- `_meta/stage3_cleanup.md` (CL-029 + CL-030 + CL-031 RESOLVED entries appended): [OLD_COUNT] → [NEW_COUNT] lines
- `_root/09_changelog.md` (Session D 2026-05-27 entry appended): 727 → [NEW_COUNT] lines

Files NOT edited (per operator stamps + Hard Rule 1):
- `_meta/stage4_prompts/_paste-ready/stage_4_2__*.md` — F6 DEFERRED to Stage 4.3 cohort launch
- `_root/04_communication_posture.md §4.11` — F14 kept as drafter judgment per QB-071
- `_root/04_communication_posture.md §4.2` — F15 DEFERRED to Stage 5 finalization
- All other rule-layer + meta files

CL-024 paste-verification (REQUIRED — paste-quote verbatim each operator-stamped source passage per Step 1 list 1–5):

1. `_root/05 §2.4.1` line 349 BEFORE prose:
   [paste-quote verbatim]

2. `_root/05 §2.4.7` line 429 BEFORE prose:
   [paste-quote verbatim]

3. `_root/05 §4` Section 4 weaving matrix BEFORE prose (lines 790–806):
   [paste-quote verbatim]

4. `_root/05 §2.4.7` line 424 BEFORE prose:
   [paste-quote verbatim]

5. `_root/00_manifest.md` Last-updated header (line 7) BEFORE prose (first 200 chars + last 200 chars; full ~10,200-char single line):
   [paste-quote first 200 + "..." + last 200]

v6.2 ground-truth re-derivation (Fix 3 matrix rebuild verification via `csv.DictReader`):
- URN: 38 total = 11 (none) + 20 IUR + 6 MOR+IUR + 1 MOR
- IUR: 10 total = 9 (none) + 1 ADR
- TBI: 13 total = 4 (none) + 8 IUR + 1 MOR+IUR
- MOR: 6 total = 4 URN + 2 URN+IUR
- ABTS: 9 total = 9 (none)
- ADR: 2 total = 1 URN + 1 (none)
- PDC: 17 total = 5 URN + 2 IUR + 5 URN+IUR + 4 (none) + 1 MOR+URN
- SA: 1 total = 1 (none)
- MC: 8 total = 8 (none)
- UCV: 2 total = 2 (none)
- RA: 1 total = 1 (none)
Sum: 11+20+6+1+9+1+4+8+1+4+2+9+1+1+5+2+5+4+1+1+8+2+1 = 107 (reconciles to §1.1 driver-inventory total of 107) ✓
Re-verification status: [PASS / FAIL with delta]

Hierarchical fix-priority distribution closed this session:
- Contradictions: 1 cluster (F9+F10+F16 bcf double-counting) ✓
- Stale numbers: 1 cluster (F9+F10+F16 matrix counts + §2.4.7 line 424) ✓
- Conversational debug language: 2 (F1 + F2) ✓
- Bloat: 2 (F4 + F5) ✓

Deferrals logged (operator stamps from Stage 4 prep Session C; no source action this session):
- F6 paste-ready bloat → Stage 4.3 cohort launch
- F14 §3m default-omit → drafter judgment retained (reassess at 5+ consecutive or Stage 5)
- F15 lede 4th-stat → Stage 5 finalization

Stage 4 audit-pass + Source-fix Session D status: COMPLETE. Audit watchlist B.6.2 closes 5 of 12 findings (F1, F2, F4, F5, F9+F10+F16 consolidated); 4 findings classified leave_alone with verification (F3, F7, F8, F11, F12); 1 finding RESOLVED-verify-only (F13); 3 findings deferred per operator stamp (F6, F14, F15). 1 extension finding (F16) closed jointly with F9+F10.

Open questions for operator: none. Stage 4 prep Session C + Source-fix Session D both closed cleanly.

Next: Stage 4.2 bri re-run decision (cohort iter 4 vs skip to Stage 4.3) per pending Stage 4.2 cohort-closeout AskQuestion at planning-agent layer.
─────────────────────────────────────────────────────────────
```

---

## Hard rules

1. **You WILL re-verify BEFORE prose at source before applying AFTER prose.** Every Fix in Step 3 carries verbatim BEFORE prose; you read source + confirm match. If mismatch, STOP and flag per `_root/CONTRACTS.md §2`.
2. **You WILL re-derive ground truth via `csv.DictReader`** for Fix 3 matrix rebuild. Planning-agent pre-derived counts in Step 3 Fix 3 are reference, not authority; your CSV re-derivation is canonical.
3. **You will not invent new rules.** Every edit is subtractive or replacing per Appendix B.6.3 guardrail 3. No additive clarification prose.
4. **You will not extend beyond Session D scope.** No new findings. No re-audit. No template-level convention codification (F14 + F15 are operator-stamped deferred). The Session D purpose is mechanical application of audit-pass-stamped trims; not redesign.
5. **You will sweep propagation per `_root/CONTRACTS.md §3` step 5** in the exact order specified in Step 4.
6. **You will not paraphrase or soften any operator-stamped content.** Paste-fidelity is the operator stamp's enforcement mechanism per CL-024.
7. **You will produce the conformance block per Step 5 as your closing artifact.** No AskQuestion bundle this session (Session D is execution; no operator-decision surface required).

---

## Stop conditions (where you `_root/CONTRACTS.md §2` flag)

- A required manifest-echo file is missing or has a mismatched Last-updated date relative to `_root/00 §2` table → STOP + flag QB-125 propagation failure.
- A paste-verification source passage (per Step 1 list 1–5) is missing or non-paste-quotable → STOP + flag.
- A BEFORE prose at source does NOT match the spec in Step 3 verbatim → STOP + flag. Do NOT silently reconcile — the audit-pass spec is operator-stamped; mismatch implies in-session drift since the audit-pass, which requires operator triage.
- Your `csv.DictReader` re-derivation for Fix 3 produces counts that do NOT match the planning-agent pre-derived counts in Step 3 Fix 3 → STOP + flag. The planning-agent counts may be wrong (audit-pass was conducted under same v6.2 snapshot, but you may catch a drift); operator stamps before you proceed with the matrix rebuild.
- You spot a contradiction or new drift NOT in the audit-pass scope → STOP + flag as new CL-NNN candidate; do NOT silently fold into Session D.

---

*Operator-stamped Stage 4 prep Source-fix Session D drafter prompt by Stage 4 planning agent 2026-05-27 per operator stamp `stamp all per recommendations` at Stage 4 prep Session C self-audit pass closeout AskQuestion bundle. Mirrors Stage 4 prep Sessions A + B pattern (in-place rule-layer edits at canonical source, fresh-agent CL-024 strict + paste-verification discipline) AND implements Session C's surfaced decisions per `_root/CONTRACTS.md §3` rule-change protocol. Cleanup discipline subtractive-or-replacing per Appendix B.6.3 guardrail 3. CL-024 strict + paste-verification carry-forward applies in full.*
