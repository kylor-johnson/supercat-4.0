# Planning-Agent Handoff — SuperCat Pricing Migration (Stage 4 transition)

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-26 by outgoing Stage 3 planning agent, in anticipation of Stage 3.5 closeout.
> **Review-pass amendment 2026-05-26**: Stage 3.5 review pass completed by outgoing Stage 3 planning agent — `entity-packets/_parent-letter-template.md` (303 lines) + `entity-packets/_parent-letter-delivery-email-template.md` (243 lines) APPROVED as-authored with one source-fix amendment (Thesis `delivery_owner` reconciled rule-layer → CSV ground truth across `_root/04 §4.15.1` + `_root/06 §1.6` + Stage 3.5 prompt + both new templates; CSV is canonical per `_root/06 §1.6` operator stamp; post-fix canonical counts 4 CEO-delivered + 10 Kylor-delivered). CL-024 RESOLVED 2026-05-26. Stage 3 is complete; this handoff is now production-ready for paste. Sections updated: §2 reading-list line counts; §3 state-snapshot table; §3 CL-NNN status table; §3 Stage 4 prep candidates (item #6 added — CSV-vs-rule-layer reconciliation discipline lesson from Stage 3.5 review pass).
>
> **Manifest-hygiene sweep amendment 2026-05-26** (post review-pass): outgoing Stage 3 planning agent applied a Stage 3.5 closeout manifest-hygiene sweep to `_root/00_manifest.md` surfaced during peer review of this very handoff document. Five edits: (a) §2 footer cumulative line count refreshed **3,558 → 4,185** (sum of §2 row line-counts — the footer had drifted across Stage 3.2–3.5 row-count bumps without recount); (b) §4 topic-index Annual-overlay-voice row owning-section pointer reclassified `§4.15 (CL-015)` → "landing TBD per Stage 4 prep" (CL-015 deferred; `§4.15` was reclaimed by the Parent-letter voice register in Stage 3.5 prep); (c) §4 topic-index Entity-packet-template row repointed from `_meta/stage3_cleanup.md` to the delivered templates at `Pricing Migration/entity-packets/` (CL-014 **RESOLVED 2026-05-26**); (d) §4 topic-index — 2 new rows added (Parent-letter voice register → `_root/04 §4.15`; Entity-packet routing → `_root/06 §1.6`); (e) §7 closing-reminder paragraph annotated with current statuses for CL-014 / CL-015 / CL-016. Side-effects: row 0 self-row 222 → 224 lines; row 9 (`_root/09_changelog.md`) 404 → 436 lines (absorbing the new changelog entry that documents this sweep). Incoming Stage 4 planning agent will read the post-sweep manifest in §1 and see correct topic-index rows + correct cumulative count in their manifest-echo conformance block. Sections of this handoff doc that name specific `_root/00` or `_root/09` line counts: none — the handoff is line-count-free for the rule-layer docs and references them only by path, so no further amendments to this doc are required.
>
> **Amendment 5 — Stage 4.2 mid-cohort finish-line takeover (2026-05-26)** (Stage 4 planning agent intra-stage refresh #2 — you are the **incoming Stage 4.2-finish + 4.3 + 4.4 + 4.5 planning agent**; the prior Stage 4.2 planning agent stewarded Stage 4.2 partway through its cohort and is handing off mid-flight). **Read this amendment first; it supersedes the §9 first-action sequence and adds §3.5 state-snapshot delta + Appendix B.6 drift watchlist below.**
>
> **What landed since Amendment 4** (2026-05-26 Stage 4.1 closeout): three Stage 4.2 production-proof iterations + two source-fix joint resolutions + one paste-ready v2 refresh. Specifically:
>
> 1. **Stage 4.2 cohort iter 1 — `cci` (Currey & Company)** APPROVED 2026-05-26 as Format B standard variant. Production proof CLOSED + ledger row filed + clean closeout (no source-fix; no rule changes). Artifacts: `format-b-notices/cci__currey-and-company__brief.md` (133) + `__delivery-email.md` (47).
> 2. **Stage 4.2 prompt authored** at `_meta/stage4_prompts/stage_4_2__format-b__per-account-drafter.md` (697 lines) + production-proven via `cci` 2026-05-26 closeout. **APPROVED** + carry-forward into all subsequent Format B paste-readys.
> 3. **Stage 4.2 cohort iter 2 — `bri` (Bulbrite)** drafter subagent HARD-STOPPED at Step 5 2026-05-26 per `_root/CONTRACTS.md §2`: v6.2 `migration_driver = included_user_reduction` contradicted IUR field signature (bri has `provided=25 < included=40` expansion-case; IUR's primary definition per `_root/05 §2.4.1` is a reduction). Planning agent ran full-cohort v6.2 driver-stamp-vs-field-signature audit via `csv.DictReader` (Appendix B.5.1 discipline) → 96 pass / 8 flag / 3 fail = 89.7% clean baseline; surfaced 3 hard failures (bri + bcf + kii) + 8 flags mapping to CL-023's filed scope (TBI primary + URN secondary 25→40 cluster). **CL-026 FILED + jointly RESOLVED with CL-023 2026-05-26** at `_root/05` source + v6.2 CSV re-stamps (10 rows: bri IUR→TBI + bcf ABTS→URN + 7 of 8 CL-023 cluster URN-secondary→IUR-secondary + sccon compound-secondary URN→IUR preserving MOR). Operator decisions: Decision 1 = stamp-both + Decision 2 = Option A (primary-vs-secondary semantic clarification at `_root/05 §2.4.1`; lowest-cost path; `_root/05 §2.3.2` sub-block prose already accommodates expansion semantics) + Next-action = apply-source-fix-only-no-bri (bri re-paste-run **deferred**; planning agent recommended next candidate from 18-row clean cohort). Post-resolution audit re-run = 98 pass / 8 flag / 1 fail = 91.6% clean (+1.9 pts; remaining 1 FAIL is kii `_root/05 §2.5.6` documented special case; 8 flags persist as informational-only post-Option-A semantic). v6.2 pre-snapshot preserved at `_archive/2026-05-26__pre-cl-026/_master-account-data-v6.2__pre-cl-026-snapshot.csv`.
> 4. **Stage 4.2 cohort iter 3 — `sca` (Shadow Catchers) v1** drafter subagent HARD-STOPPED at Step 5 2026-05-26 per `_root/CONTRACTS.md §2`: `_root/05 §2.1.2` Format B URN canonical block carried a single expansion-baked `[IF excess users remain after new included base]` sub-block that produced direction-inverted prose for URN-primary + IUR-secondary REDUCTION-direction accounts (sca's data: legacy `provided=25 → new included=10`; substituting tokens produced "expanding from 25 to 10 — absorbing [N] users" — direction-inverted and customer-incoherent). Planning agent verified v6.2 enumeration via `csv.DictReader`: **26 URN+IUR-secondary accounts** in v6.2 (25 REDUCTION + 1 EXPANSION = `bcf`); §4 matrix's "7-account" count was stale by 19 occurrences; CL-026 / CL-023 joint resolution had been TBI-side-only (URN-side §2.1.x / §2.1.7 never inspected). **CL-027 FILED + RESOLVED 2026-05-26** at `_root/05 §2.1.2` source via operator-stamped Option 2 (proper source-fix): added parallel `[IF excess users remain AND secondary driver = included_user_reduction (base shrinking from legacy to current tier standard)]` sub-block to §2.1.2 mirroring the pre-existing §2.1.3 reduction-direction sub-block (direction-neutral "adjusting" prose; locate by marker text, not line number); tightened existing §2.1.2 marker to specify EXPANSION-direction; §2.1.7 routing rewritten to dispatch URN+IUR-secondary by direction-shape; §2.4.1 Option A semantic extended to URN-side §2.1.2 / §2.1.3 (closes CL-026 / CL-023's TBI-side-only scope-gap); §2.4.7 cross-reference extended; §4 matrix row 5 count re-tallied 7 → 26 with named enumeration + mutual-exclusivity rule codified; §1.1 URN definition + §1.3 + doc header line 3 hygiene-propagation updates ("7 combinations" → "9 combinations"). No v6.2 CSV re-stamps required (rule-layer-only fix). Two planning-agent self-corrections logged: (a) v1 sca paste-ready pre-flight observation 2 was WRONG (claimed §2.1.7 sub-block describes "legacy-allotment-reducing-to-new-tier-standard"; actual §2.1.7 pre-CL-027 routed URN+IUR-secondary to §2.1.2's EXPANSION-only sub-block — drafter caught via CL-024 paste-verification + direct source-read); (b) CL-026 / CL-023 joint resolution 2026-05-26 had a TBI-side-only scope-gap. **CL-024 paste-verification protocol validated again — third Stage 4 catch** (Stage 3.5 Thesis + Stage 4.2 bri + Stage 4.2 sca v1).
> 5. **`_meta/stage4_prompts/_paste-ready/stage_4_2__sca.md` v2** refreshed 2026-05-26 (882 → 886 lines) — corrected pre-flight observation 3 + data observations 1 + 2 + `csv.DictReader` attestation + `secondary_drivers` CSV-row description; added v2 stamp documenting v1 hard-stop + CL-027 source-fix + planning-agent self-corrections + v1→v2 transparency note. **v2 paste-ready is in-flight via a parallel Cursor agent at the time of this handoff** (operator is applying the CL-027 file diffs to that agent's context now; the agent will then produce sca v2 brief + delivery email + conformance block).
>
> **What's open at handoff time**:
>
> - **Stage 4.2 cohort iter 3 v2** (sca) — drafter subagent in-flight via parallel Cursor agent; conformance block pending. **Your first action when posted: planning-agent audit pass + AskQuestion for operator stamp.**
> - **Stage 4.2 cohort iter 2** (bri) — deferred per operator-stamped `apply_source_fix_only_no_bri` 2026-05-26. Now technically unblocked at the rule layer (CL-026 + CL-023 + CL-027 source-fixes all landed; bri's TBI-primary + IUR-secondary stamp fires `_root/05 §2.3.2` cleanly with the expansion-direction "Additionally, the included user base for this tier is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]" sub-block). **Decision point after sca cohort iter 3 closes**: re-run bri (cohort iter 4 — clean re-paste-run; quick win to lock in the post-CL-026 TBI+IUR-secondary expansion pattern as a production proof) OR proceed to Stage 4.3 (CEO Letter prompt authoring + first CEO Letter production proof). Surface via `AskQuestion` after cohort iter 3 closes.
> - **Stages 4.3 / 4.4 / 4.5** drafter prompts — all PENDING. Pattern-inherit from `stage_4_2__format-b__per-account-drafter.md` (697 lines) which itself pattern-inherits from `stage_4_1__format-a__per-account-drafter.md` (657 lines). Per-format adjustments documented at each format's Stage 3 template + each format's `_root/05 §N` driver block.
> - **Production proof gate** — pending; activates once all 5 `stage_4_X` prompts have 1 APPROVED production proof each (current state: 4.1 lpf APPROVED + 4.2 cci APPROVED + 4.2 sca in-flight; 4.3 / 4.4 / 4.5 not yet started).
>
> **Operator's elite-and-no-drift directive 2026-05-26**: the operator surfaced explicit drift concern at the handoff trigger point ("this is becoming a very complex operation all of a sudden"). Your **second action** after closing sca cohort iter 3 is a **self-audit pass on the work landed during Amendment 5's catalyst session** (CL-026 + CL-023 + CL-027 joint-resolution sequence + sca v2 paste-ready refresh) for drift / contradictions / overlapping instructions / unnecessary language. **Appendix B.6 below pre-populates 12 drift findings** the prior planning agent already spotted but did not act on. **You verify each + extend the list with any new findings + surface to operator via `AskQuestion`** with `definitely_fix` / `consider_fix` / `leave_alone` triage. Operator stamps; you apply approved fixes.
>
> **What does NOT change at this amendment**: Appendix A (12 design constraints) + Appendix B (CSV canonical) + Appendix B.4 (CL-025 reconciliation discipline) + Appendix B.5.1 (csv.DictReader pre-flight) + Appendix B.5.2 (Appendix-B canonicality check) all remain operator-stamped + carry-forward. The 8 architectural concepts in §4 unchanged. The §7 operator-interaction protocol + §10 closing reminder unchanged. The §6 review protocol unchanged. **Your job is to extend the precedent, not rewrite it.** Source-of-truth pointers: `_root/09_changelog.md` 2026-05-26 entries (Stage 4.2 cci closeout + Stage 4.2 bri hard-stop + CL-026 + CL-023 joint resolution + CL-027 RESOLVED at `_root/05 §2.1.2`) + `_meta/stage3_cleanup.md` CL-026 + CL-027 RESOLVED entries.
>
> **Prior amendment retained verbatim below** for handoff continuity ↓
>
> **Stage 4.1 closeout amendment 2026-05-26** (Stage 4 planning agent intra-stage refresh — the incoming agent reading this is the Stage 4.2–4.5 planning agent; Stage 4.1 was closed by the Stage 4.1 planning agent — same role, different context). What landed since the original handoff: (a) **Stage 4 prep Source-fix Sessions A + B closed** — `_root/04 §1.1` audience register + `_root/04 §3` 6 SaaS-renewal forbidden-phrase rows + `_root/04 §4.16` Annual-cohort voice rules (CL-015 **RESOLVED 2026-05-26**); `_root/07 §7.5` delivery-email routing-block subset matrix (CL-022 **RESOLVED 2026-05-26**); `_root/08 §10` 12 entity-packet QB-NNN blockers QB-127–QB-138 (Stage 3.5 deferred item #5 **RESOLVED 2026-05-26**); 5 Stage 3 delivery-email templates Section 2 strip-and-replace + Format A `Comm_action:` add + `Support fire cleared:` matrix row add. (b) **`_meta/stage4_prompts/README.md` authored** (183 lines; review protocol + paste-ready pattern + 8-step skeleton mirror) + **`_meta/stage4_account_ledger.md` authored** (153 lines; per-account ledger + per-format row groups + cohort organization + entity-packet orchestration playbook). (c) **Stage 4.1 prompt authored + closed** — `_meta/stage4_prompts/stage_4_1__format-a__per-account-drafter.md` (638 lines) + production proof `lpf` (Linon/Powell Furniture) paste-runned via `_meta/stage4_prompts/_paste-ready/stage_4_1__lpf.md` (735 lines) → APPROVED 2026-05-26 as Format A 60-Day Notice (`format-a-notices/lpf__linon-powell-furniture__brief.md` + `__delivery-email.md`). Ledger lpf row filed APPROVED 2026-05-26. (d) **CL-025 RESOLVED 2026-05-26** (v6.2 reconciliation discipline — operator Option (1) stamp): v6.2 modeled-canonical wins per Appendix B; reconciliation flag → INTERNAL ops cleanup pre-effective-date; client copy NEVER mentions "unused users"; source-fix at `_root/07 §4.5` + `_root/05 §2.1.5` + `_root/04 §4.9`; `_meta/v6_2_reconciliation_log.md` NEW file (100 lines; 37 flagged rows pre-populated from cohort sweep — 35% of pending cohort); `enabled_users` column added to `_master-account-data-v6.2.csv` at position 15 (populated from billing math); **Appendix B.4 added below** codifying the discipline at planning-agent layer. (e) **Appendix B.5 added below** codifying two operational lessons from Stage 4.1: routing-CSV header-position parse discipline (planning-agent pre-flight enforcement) + Appendix-B-canonicality-check before pivot recommendations (planning-agent audit discipline). (f) **§2 reading list amended below** with Stage 4.1 closeout precedents (9 new files); **§3 state snapshot table amended below** (Stage 4 prep candidates marked CLOSED + Stage 4.1 verification rows added + CL-015/CL-022/CL-025 marked RESOLVED); **§5 Phase 4-prep table** marks Stage 4.1 ✅; **§9 first-action sequence rewritten** for Stage 4.2 takeover (Stage 4.1 work is closed; new agent picks up at Stage 4.2 Format B prompt authoring). Source-of-truth pointers: `_root/09_changelog.md` 2026-05-26 entries (Stage 4 prep Sources A + B closeout + Stage 4.1 lpf production proof closeout) + `_meta/stage3_cleanup.md` CL-015 / CL-022 / CL-025 RESOLVED entries.
> **Workspace root**: `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/`

---

## You are taking over as the Stage 4 planning agent for the SuperCat Pricing Migration program

The Stage 3 planning agent (outgoing) stewarded the program through all 5 Stage 3 template waves (3.1 Format A → 3.5 entity packets). All 5 template sets are operator-approved at the rule layer and present in the workspace. Stage 4 is **per-account production drafting** — you author 5 format-specific drafter prompts (one per format), then shepherd ~85 per-account drafting sessions through review + operator approval.

**You are not a fresh drafter agent.** You are the planning agent — the operator's reviewer, drafter-prompt author, changelog author, manifest custodian, CL-tracker maintainer, AND the per-account routing pre-flight runner. Fresh drafter agents are spawned by the operator pasting `stage_4_X` prompts you author + an `ord_id` parameter; their per-account outputs (one brief + one delivery email per account) come back to you for review. You execute closeout edits (changelog, manifest, per-account ledger). **You never write client copy directly** — drafting is what fresh agents are for; the architecture is designed around their fresh-context independence as the drift-detection mechanism.

**Stage 4 is structurally different from Stage 3 in three load-bearing ways**:

1. **The path-reference inversion** (architectural concept #8 in §4 below). Stage 3 templates carry `[INSERT _root/XX §N.M ...]` pointers; Stage 4 production artifacts carry the actual rule prose, fetched verbatim from the owning `_root/` doc, with bracketed tokens substituted from v6.2 + Postgres. Strict-placeholder precedent does NOT relax at Stage 4 — paste character-for-character; paraphrase is automatic fail.
2. **The session shape is `ord_id`-scoped.** One account in, two files out, conformance block, STOP. Batch drift = automatic fail. The 4 archived per-account prompts batched 3 accounts; this is forbidden in Stage 4.
3. **The job naming has to be locked at every layer** to prevent SaaS-renewal-vocabulary drift. Stage 4 drafters are **per-account pricing migration notice drafters for SuperCat's 2026 book normalization** — explicitly NOT SaaS renewal writers, CRM sequence authors, contract negotiators, or template builders. Every `stage_4_X` drafter prompt you author must lock the job naming at its top (see Appendix A §1).

**Output is read by the operator (CEO) AND used as paste material for fresh agents you spawn.** Be direct, declarative, no marketing language. Present audit results in tables. Use the `AskQuestion` tool for operator decisions rather than listing options in chat text. Cite specific line numbers and `_root/XX §N.M` references. Never improvise — flag and escalate per `_root/CONTRACTS.md §2`.

---

## §1. What this program is (in 200 words)

SuperCat is migrating 107 customers to a new pricing structure in 2026 — a **book normalization**, not a SaaS renewal. Notices go out in three cohorts (June / July / Deferred) plus per-entity Post-Migration timing for 2 rollup entities. Five communication formats exist (Format A 60-Day Notice; Format B Notice + Meeting; CEO Letter + Call Commitment; Good News for decreases; entity-packet parent letter for multi-brand parents). Each format has a brief template and a delivery email template, both operator-approved at Stage 3. The dual-canonical v6.2 architecture splits the data: `_master-account-data-v6.2.csv` (346 lines) is canonical for standalone-account scope; `_master-entity-data-v6.2.csv` (15 lines) is canonical for entity-packet scope.

The pre-2026-05-22 templates inlined verbatim rule prose; the 2026-05-22 refactor consolidated every rule into exactly one owning `_root/` doc per the **path-reference contract** (`_root/CONTRACTS.md §5`: no rule restated outside its owning doc). Stage 3 rebuilt all 5 templates as pointer artifacts. Stage 4 is **per-account production drafting** under those rebuilt templates — fresh drafter agents fetch verbatim rule blocks via the pointers, substitute placeholders from v6.2 + Postgres, and produce one brief + one delivery email per account.

The recipient is a **CFO / owner / principal of a furniture / lighting / decor wholesaler** — not a procurement officer, IT buyer, or platform admin. The architecture is operator-stamped strict on path-reference contract, strict on per-account session scope, strict on routing-as-hard-gate.

---

## §2. Required reading (read in this exact order; echo every file's last-updated date in your first response)

This is the manifest-echo contract per `_root/00_manifest.md §6` plus the program-specific context you inherit. **Do not skip files. Do not skim.** The cost of one extra read is five seconds; the cost of a missed precedent is unrecoverable drift.

### Folder orientation (the contract layer — every agent reads these first)

1. `Pricing Migration/AGENTS.md`
2. `Pricing Migration/00_README.md`
3. `Pricing Migration/_root/00_manifest.md` — **the index.** §2 is the manifest table (echo every row's title + last-updated date in your first response). §5 is the canonical conformance-block format. §6 is the manifest-echo contract.
4. `Pricing Migration/_root/CONTRACTS.md` — the operator contract, agent contract, rule-change protocol (`§3`), anti-archive rule with explicit-extraction exception (`§4`), path-reference contract (`§5`).

### The rule layer (the 10 numbered docs every per-account brief + delivery email references)

5. `_root/01_why_we_are_migrating.md` — strategic register; relationship-before-price principle.
6. `_root/02_who_is_being_migrated.md` — 8 segments, $200/$400/$600 ownership boundaries, entity overlay, health overrides (incl. Critical-band per-account exception), annual overlay, cohort assignment, errata, 109/107/2 reconciliation.
7. `_root/03_what_we_sell.md` — T1/T2/T3 verbatim tier blocks, user-rate ladder, "What's Coming in 2026" roadmap (CL-005 — in all 4 brief formats + per-child notices under entity packets), implementation-fee table, INTERNAL peer ranges (NEVER in client copy per CL-003), INTERNAL unpublished SKUs.
8. `_root/04_communication_posture.md` — **the highest-rule-density doc.** §1 voice posture (peer-to-peer or vendor-to-principal — never service-rep-to-buyer; never marketing-to-prospect). §2 14 non-negotiables. §3 27-row forbidden-phrase table (the canonical anti-SaaS-vocabulary list — point drafters here, do NOT re-list ad hoc). **§3.1** Good News consolidated 2026 framing variant (operator-stamped 2026-05-26). **§4.1–§4.14** named voice rules including format-specific close text in §4.12. **§4.15 (six sub-sections)** Parent-letter voice register for entity-packet program (operator-stamped 2026-05-26 at Stage 3.5 prep; voice fork by `delivery_owner` CEO vs Kylor HoCS; cross-format CSM-role note — "CSM-sent" role-marker filled by Kylor in HoCS role across all 5 templates for the migration program). §5 driver-voice orientation.
9. `_root/05_driver_taxonomy.md` — 11 `migration_driver` values (8 increase-side + 3 decrease-side + 1 status-marker). Section 2 = increase-side (each driver has §N.1 def + §N.2 Format B canonical + §N.3 CEO Letter canonical + §N.4 Format A canonical + §N.5 pricing-table row + §N.6 conditional context + §N.7 secondary). Section 3 = decrease-side (Good News canonical — 3 drivers). Section 4 secondary-driver weaving matrix. Section 5 driver-segment correlation (informational only). **Stage 3.2 source fixes applied 2026-05-26 at §2.3.2 + §2.3.3 + §2.6.2 + §2.6.3 + §2.6.6 + §2.6.7**.
10. `_root/06_format_routing.md` — 4 brief formats + 2 routing patterns (CEO Pre-Call → Format B; CEO-Led Entity Pre-Engagement → Coordinated Notices). **6-step routing-decision flow** (status filter → decrease → entity → annual → health → delta-tier) — **this is the hard gate every per-account session runs BEFORE any prose is drafted**. Delta-tier dispatch table with operator-stamped Δ_pct vs Δ_mrr precedence. 3 overrides (entity / health / annual). **§1.6** entity-packet program canonical scope (rewritten 2026-05-26 at Stage 3.5 prep — 14 entities total per Master Entity tab; 13 in Stage 3.5 template scope; Ferguson Enterprises mixed-direction one-off excluded). `comm_action` vocabulary + 4 CSV companion columns. 5 routing-CSV errata.
11. `_root/07_data_pipeline.md` — source-of-truth hierarchy (v6.2 CSV → Postgres → routing CSV → HTML model); 53-column v6.2 field guide + Master Entity tab columns (added 2026-05-26 Stage 3.5 prep — see `_root/09` Stage 3.5 prep entry); canonical loader with `ghost_account = TRUE` + `migration_status = 'already_migrated'` filter; **3 verbatim Postgres MCP queries** (for lede stats only); derived metrics (`cost_per_order` / `annual_subscription` / `delta_per_order`); §5 9-row fallback table for Postgres unavailability (`composite_narrative` fallback for live stats); §6 file-naming convention (`<format>-notices/[ord_id]__[company-slug]__brief.md` etc.); **§7 per-format routing-block field-list matrix** (canonical for Format A / B / CEO Letter / Good News; entity-packet row inferred per CL-022 — flag for Stage 4 prep).
12. `_root/08_quality_bar.md` — 126 QB-NNN checks (113 blockers + 5 warnings + 8 audit-only). Cite check IDs by number in `stage_4_X` Section 4 checklists; review per-account proof drafts against these IDs.
13. `_root/09_changelog.md` — **read every entry.** Most load-bearing doc for understanding what's been operator-stamped, deferred, resolved. Particularly important Stage 4 context: Wave 1 + Wave 2 + Wave 3 operator-stamping pass (foundational rule layer); **all 5 Stage 3.X review-pass entries 2026-05-26** (the format-specific deviations + structural conventions); **Stage 3.5 prep 2026-05-26** (dual-canonical v6.2 architecture; `_root/04 §4.15` authored; `_root/06 §1.6` rewritten; CL-014 closed; CL-015 location updated; cross-format CSM-role note); **Stage 3.5 review pass 2026-05-26** (templates APPROVED with Thesis source-fix amendment; CL-024 RESOLVED; five items deferred to Stage 4 / Wave 6 — sentence-2 promotion / CL-005 roadmap promotion / 4-brand member-enumeration example / `_root/07 §7` entity-packet row / `_root/08` entity-packet QB additions).

### The dual-canonical v6.2 data files (Stage 4's authoritative scope sources — read both header rows + sample data)

14. `_master-account-data-v6.2.csv` — canonical for standalone-account scope (Stage 4.1–4.4 drafter prompts). 346 lines (1 header + 345 account rows). Per-row drafter input.
15. `_master-entity-data-v6.2.csv` — canonical for entity-packet scope (Stage 4.5 drafter prompt + orchestration). 15 lines (1 blank + 1 header + 13 rollup + 1 standalone_multi_org entity rows). Master Entity tab joins to Master Account tab via `member_ord_ids` ↔ `ord_id`.

### The cleanup tracker (the in-flight CL-NNN list)

16. `_meta/stage3_cleanup.md` — every `CL-NNN` item filed across the program. **Items relevant to your Stage 4 work** (full status verification in §3 below): CL-001/003/004/005 (exemplar-regen items; Stage 4 production is where they're resolved per-account); CL-007 (Foundation/03 D-004b ladder bands — operator decides Stage 4 prep or deferred); CL-011 (Format A driver rename — confirm absorbed into Stage 3.1 template); CL-015 (Annual overlay voice rules — Stage 4 prep candidate; should be source-fixed to `_root/04 §4.16` or §5 extension BEFORE Stage 4.4 Annual children draft); CL-017 (Critical-band per-account judgment — operator-stamped 2026-05-22; applies per-account); CL-018–021 (Format A v2 exemplar issues — Stage 4 production replaces these archived exemplars); CL-022 (delivery-email routing-block field-list batch — Wave 6; Stage 4 prep candidate); CL-023 (v6.2 `secondary_drivers` re-evaluation — Stage 4 surfaces; per-account operator decision); CL-024 (Stage 3.5 prompt manifest-echo strengthening — should RESOLVE at Stage 3.5 review pass; verify); CL-000 (routing-CSV errata not baked into source CSV — Stage 4 production references `_root/06 §2 + §7` errata mirror).

### Stage 3 process docs (the wave-sequence + review-protocol layer)

17. `_meta/stage3_prompts/README.md` — Stage 3 wave sequence (3.1 ✓ / 3.2 ✓ / 3.3 ✓ / 3.4 ✓ / 3.5 ✓ — verify final row before starting). Pattern-inheritance discipline you inherit.
18. `_meta/stage3_prompts/PLANNING_AGENT_HANDOFF.md` — the Stage 3 planning-agent handoff (409 lines). Read for handoff-doc structural inheritance + operator-interaction protocol patterns + Stage 3 architectural-concept formulations.
19. `_meta/stage3_prompts/stage_3_3__ceo-letter__brief-and-delivery-templates.md` — **the gold-standard reference for Stage 4 drafter-prompt structure.** This prompt has the cleanest 8-step skeleton. Adapt its structure for every `stage_4_X` you author.
20. `_meta/stage3_prompts/stage_3_5__entity-packets__parent-letter-and-delivery-email-templates.md` — the Stage 3.5 prompt (655 lines). Reference for paste-verification language (CL-024 strict + paste-verification framing) and for voice-fork conditional rendering (`[IF delivery_owner = CEO: ... | IF delivery_owner = Kylor: ...]`).

### The 5 approved Stage 3 template sets (10 files — the source of every Stage 4 production artifact)

21. `format-a-notices/_brief-template.md` (330 lines) + `_delivery-email-template.md` (129 lines) — Stage 3.1 output (APPROVED 2026-05-26).
22. `format-b-notices/_brief-template.md` (354 lines) + `_delivery-email-template.md` (159 lines) — Stage 3.2 output (APPROVED 2026-05-26).
23. `ceo-letter-notices/_brief-template.md` (366 lines) + `_delivery-email-template.md` (164 lines) — Stage 3.3 output (APPROVED 2026-05-26).
24. `good-news-notices/_brief-template.md` (240 lines) + `_delivery-email-template.md` (164 lines) — Stage 3.4 output (APPROVED 2026-05-26).
25. `entity-packets/_parent-letter-template.md` (303 lines) + `_parent-letter-delivery-email-template.md` (243 lines) — Stage 3.5 output (APPROVED 2026-05-26 with Thesis source-fix amendment; templates carry voice-fork conditional rendering `[IF delivery_owner = CEO: ... | IF delivery_owner = Kylor: ...]`; default-only pricing posture enforced; 48-hour two-stage sequencing referenced throughout; per-brand mechanics restraint enforced; 3-location date parity contract enforced for CEO-delivered fork; cross-format CSM-role note carried through to both files; 8 + 9 EP-NNN entity-packet-specific blockers in Section 4 superseded by `_root/08 §10` QB-127–QB-138 per Stage 4 prep Source-fix Session B 2026-05-26).

### Stage 4.1 closeout precedents (the pattern you inherit for Stages 4.2–4.5; read every file)

These 9 files are the precedent set for Stages 4.2–4.5. The Stage 4.1 planning agent closed Stage 4.1 with this output; you pattern-inherit. Read every file in full.

26. `_meta/stage4_prompts/README.md` — Stage 4 wave sequence + review protocol + paste-ready pattern + canonical 8-step skeleton. Mirrors `_meta/stage3_prompts/README.md` structure. **The review protocol (between every per-account session) is the same one you run for Stages 4.2–4.5.** Particularly: Step 4 reconciliation-discipline check (CL-025 RESOLVED 2026-05-26 — see Appendix B.4 below).
27. `_meta/stage4_prompts/stage_4_prep_a__root_04_three_extensions.md` — Source-fix Session A prep prompt (audience register + 6 SaaS-renewal forbids + Annual-cohort voice rules; landed 2026-05-26; CL-015 RESOLVED). Pattern reference for Stage 4-class source-fix prep prompts (operator-paste-runs into fresh agent; fresh agent applies edits to `_root/`).
28. `_meta/stage4_prompts/stage_4_prep_b__wave_6_batch.md` — Source-fix Session B prep prompt (`_root/07 §7.5` delivery-email routing-block matrix + `_root/08 §10` 12 entity-packet QB-NNN blockers; landed 2026-05-26; CL-022 + Stage 3.5 deferred item #5 RESOLVED). Same pattern as item 27.
29. `_meta/stage4_prompts/stage_4_1__format-a__per-account-drafter.md` (657 lines) — **the gold-standard per-account drafter prompt.** You pattern-inherit from this for Stages 4.2 (Format B), 4.3 (CEO Letter), 4.4 (Good News), 4.5 (entity-packet parent letter). 8-step canonical skeleton per Appendix A.11. Appendix A.1–A.12 embedded verbatim in Step 1. Step 4 includes the After-row math discipline (CL-025; reconciliation flag handling; tracker cross-reference). Per-format adjustments for 4.2/4.3/4.4/4.5 are documented in each format's Stage 3 template + each format's `_root/05 §N` driver block.
30. `_meta/stage4_prompts/_paste-ready/stage_4_1__lpf.md` (734 lines) — **the gold-standard paste-ready artifact.** You author one per Stage 4.X production proof. Structure: 8-step skeleton with `[ORD_ID] = lpf` substitutions inline + planning-agent annotation block (routing pre-flight trace + CSV-canonical reconciliation table + data observations). The canonical prompt at item 29 stays untouched (carries `[ORD_ID]` placeholder); per-account paste-ready files substitute the placeholder.
31. `format-a-notices/lpf__linon-powell-furniture__brief.md` (137 lines) — the Stage 4.1 lpf brief APPROVED 2026-05-26. Your Stage 4.2/4.3/4.4/4.5 production proof outputs match this artifact in structural form (per the format's `_brief-template.md`).
32. `format-a-notices/lpf__linon-powell-furniture__delivery-email.md` (44 lines) — the Stage 4.1 lpf delivery email APPROVED 2026-05-26. Same role as item 31 for delivery email scope.
33. `_meta/stage4_account_ledger.md` (153 lines) — per-account ledger; one row per operator-stamped per-account session. Stage 4.1 lpf row filed APPROVED 2026-05-26 under Format A section. **You append rows during Stages 4.2–4.5 closeouts.** Schema + per-format groups + cohort organization + entity-packet orchestration playbook documented in-file.
34. `_meta/v6_2_reconciliation_log.md` (100 lines) — per-account ops cleanup tracker. 37 flagged rows pre-populated from 2026-05-26 cohort sweep (35% of 107 pending; 14 routing-flip rows at top as highest urgency). **You verify every Stage 4.X production proof candidate against this tracker** (per Stage 4.1 closeout discipline — every flagged account already has a row; new accounts post-2026-05-26 you append rows for if newly-flagged). Read methodology section + pattern reference in-file.

### Stage 4.1 closeout source-fix files (read for context on what changed in the rule layer + v6.2 CSV)

35. `_master-account-data-v6.2.csv` — `enabled_users` column added 2026-05-26 at position 15 (Stage 4.1 closeout; populated from billing math `current_provided_users + ROUND(current_user_mrr ÷ current_user_rate)`). This is the column drafters reference for reconciliation flag computation per `_root/07 §4.5`. Read row 1 header line to confirm column position.
36. The 3 source-fixed `_root/` sections (all 2026-05-26; CL-025 RESOLVED at planning-agent layer): `_root/07 §4.5` Resolution discipline paragraph (v6.2 modeled wins; flag → INTERNAL ops cleanup; cohort sweep result cited); `_root/05 §2.1.5` After-row canonicality paragraph (`[NEW_EXCESS]` / `[NEW_USER_CHARGE]` = v6.2 modeled-canonical; drafters do not recompute from billing); `_root/04 §4.9` drafter-facing operational note (customer-facing footnote unchanged; internal note clarifies ops cleanup IS the hedge; never edit footnote to hedge). Read each in-place when you reach the corresponding `_root/` doc in items 8 / 9 / 11 above.

### Stage 4.2 cohort iter precedents — Amendment 5 (the pattern you inherit for cohort iter 3 closeout + Stages 4.3–4.5; read every file)

These files are the precedent set for Stage 4.2 cohort iters 1–3 + Stages 4.3–4.5. Pattern-inherit. Read every file in full.

37. `_meta/stage4_prompts/stage_4_2__format-b__per-account-drafter.md` (697 lines) — **the Format B per-account drafter prompt** APPROVED via `cci` production proof. Pattern reference for Stages 4.3 / 4.4 / 4.5 drafter prompts.
38. `_meta/stage4_prompts/_paste-ready/stage_4_2__cci.md` (841 lines) — Stage 4.2 cohort iter 1 paste-ready (cci APPROVED 2026-05-26). Pattern reference for clean paste-ready closeout.
39. `_meta/stage4_prompts/_paste-ready/stage_4_2__bri.md` (~830 lines) — Stage 4.2 cohort iter 2 paste-ready (bri DEFERRED 2026-05-26 post-CL-026 / CL-023 source-fix). Pattern reference for hard-stop-and-source-fix paste-ready. **Read for the hard-stop conformance block + CL-026 / CL-023 trace evidence.**
40. `_meta/stage4_prompts/_paste-ready/stage_4_2__sca.md` v2 (886 lines) — Stage 4.2 cohort iter 3 paste-ready v2 (post-CL-027 source-fix refresh). Pattern reference for v1 → v2 paste-ready refresh + planning-agent self-correction transparency. **Read for the v2 stamp block + corrected pre-flight observations + drafter-survives-CL-024-paste-verification-catch evidence.**
41. `format-b-notices/cci__currey-and-company__brief.md` (~133 lines) + `__delivery-email.md` (~47 lines) — Stage 4.2 cci production proof APPROVED 2026-05-26. Your Stage 4.2 sca / Stage 4.3 / 4.4 / 4.5 production-proof outputs match this artifact in structural form (per the format's `_brief-template.md`).
42. `_archive/2026-05-26__pre-cl-026/_master-account-data-v6.2__pre-cl-026-snapshot.csv` (346 lines) + `v6_2_driver_signature_audit.py` (audit script) — pre-CL-026 baseline preservation. Read for the re-stamp-discipline pattern (`csv.DictReader` pre-snapshot + post-stamp audit re-run + baseline comparison). Re-use this pattern if you re-stamp v6.2 in any future session.
43. `_root/09_changelog.md` Amendment-5 catalyst session entries — Stage 4.2 cci closeout entry + Stage 4.2 bri hard-stop entry + CL-026 + CL-023 jointly RESOLVED entry + CL-027 RESOLVED entry. Read every Amendment-5 entry (4 entries dated 2026-05-26 with Amendment-5 context).
44. `_meta/stage3_cleanup.md` CL-026 + CL-027 RESOLVED entries — the canonical CL-NNN closure documentation. Read for the resolution-prose pattern + post-resolution scope/impact enumeration.

### Do NOT read

- `_archive/**` per-account exemplars — CL-001 / CL-003 / CL-004 / CL-005 / CL-018–021 explicitly flag these as drift sources for Stage 4. The anti-archive rule (`_root/CONTRACTS.md §4`) applies absolutely; reading these risks pattern-inheritance from forbidden patterns.
- `Migration-Health Artifacts/` templates — strategic reference materials abstracted into `_root/`. Reading them is scope creep.
- `_reference/2026-05-20__execution_plan_v3.3.md` or `_reference/migration_revenue_model_2026-05-14.html` — strategic source material; abstracted into `_root/01`–`_root/07`. Reading is scope creep.
- `_meta/stage2_prompts/**` — pre-refactor template-build prompts. Out of scope.
- Per-account exemplars under `format-*-notices/<account>/` if any remain (kal/kii/lss v2 specifically — CL-018–021 explicitly flag).
- `~/Downloads/**` or anything outside `Pricing Migration/` and `Migration-Health Artifacts/` per AGENTS.md hard rules.

---

## §3. Where the program is right now (state snapshot — verify EVERY ROW from disk before starting; do not trust memory)

The outgoing planning agent verified the snapshot below at 2026-05-26 pre-Stage-3.5-review. **You must re-verify every row by reading the disk** (use `wc -l` ground truth; read header "Last updated" dates; do not infer from memory).

### State snapshot — verify from disk

| Item | Expected state (verify) | Source-of-truth |
|---|---|---|
| `_root/00`–`_root/09` + `_root/CONTRACTS.md` | All 11 docs present; 2026-05-26 or later in "Last updated" headers | `grep -n "Last updated" _root/*.md _root/CONTRACTS.md` |
| Manifest §2 line counts match `wc -l` | All 10 _root/ docs reconcile | `wc -l _root/*.md` vs `_root/00_manifest.md §2` |
| Stage 3.1 Format A APPROVED | `format-a-notices/_brief-template.md` (330 lines) + `_delivery-email-template.md` (130 lines; +1 from CL-022 Source-fix Session B `Comm_action:` line add) | `wc -l format-a-notices/*.md` + `_meta/stage3_prompts/README.md` Wave 3.1 row |
| Stage 3.2 Format B APPROVED | `format-b-notices/_brief-template.md` (354 lines) + `_delivery-email-template.md` (157 lines; –2 from CL-022 strip-and-replace) | `wc -l format-b-notices/*.md` + README Wave 3.2 row |
| Stage 3.3 CEO Letter APPROVED | `ceo-letter-notices/_brief-template.md` (366 lines) + `_delivery-email-template.md` (162 lines; –2 from CL-022 strip-and-replace) | `wc -l ceo-letter-notices/*.md` + README Wave 3.3 row |
| Stage 3.4 Good News APPROVED (incl. closeout amendment) | `good-news-notices/_brief-template.md` (240 lines) + `_delivery-email-template.md` (162 lines; –2 from CL-022 strip-and-replace); lede normalization "invoice"→"pricing" applied 2026-05-26 | `wc -l good-news-notices/*.md` + README Wave 3.4 row + `_root/09 §"Closeout amendment 2026-05-26"` entry |
| **Stage 3.5 entity packets APPROVED** | `entity-packets/_parent-letter-template.md` (303 lines) + `_parent-letter-delivery-email-template.md` (241 lines; –2 from CL-022 strip-and-replace); README Wave 3.5 status = APPROVED 2026-05-26 | `wc -l entity-packets/*.md` + README Wave 3.5 row + `_root/09` Stage 3.5 review-pass entry |
| `_root/04 §4.15` (6 sub-sections) at source | `_root/04_communication_posture.md` 495+ lines; §4.15.1–§4.15.6 present | `grep -n "^#### §4\.15\." _root/04_communication_posture.md` (expect 6 matches) |
| `_root/06 §1.6` rewritten with 14-entity scope | `_root/06_format_routing.md` 319+ lines; §1.6 names "14 entities" + "Ferguson Enterprises" | `grep -n "14 entities\|Ferguson Enterprises" _root/06_format_routing.md` |
| Dual-canonical v6.2 files present | `_master-account-data-v6.2.csv` (346 lines) + `_master-entity-data-v6.2.csv` (15 lines) | `wc -l _master-*.csv` |
| **`_master-account-data-v6.2.csv` `enabled_users` column at position 15** (Stage 4.1 closeout 2026-05-26) | Row 1 header: column 15 = `enabled_users` (after `active_users`, before `current_stack`) | `head -1 _master-account-data-v6.2.csv \| awk -F, '{print $15}'` should print `active_users`; `{print $16}` should print `enabled_users` (CSV has leading empty column 1; counted-without-leading-empty position is 15) |
| **`_meta/stage4_prompts/` populated** (Stage 4 prep + Stage 4.1 closeout) | 6 files present: PLANNING_AGENT_HANDOFF.md (this doc, 745+ lines post-Stage-4.1-amendment) + README.md (183) + stage_4_prep_a__root_04_three_extensions.md (446) + stage_4_prep_b__wave_6_batch.md (429) + stage_4_1__format-a__per-account-drafter.md (657) + _paste-ready/stage_4_1__lpf.md (734); 4.2/4.3/4.4/4.5 drafter prompts PENDING (your job) | `ls _meta/stage4_prompts/ _meta/stage4_prompts/_paste-ready/` |
| **`_meta/stage4_account_ledger.md` populated** (Stage 4.1 closeout 2026-05-26) | 153 lines; lpf row APPROVED 2026-05-26 under Format A section | `wc -l _meta/stage4_account_ledger.md` + `grep "lpf" _meta/stage4_account_ledger.md` (expect 1 match in Format A section) |
| **`_meta/v6_2_reconciliation_log.md` created** (Stage 4.1 closeout 2026-05-26) | 100 lines; 37 flagged rows pre-populated from cohort sweep (35% of 107 pending) | `wc -l _meta/v6_2_reconciliation_log.md` + `grep -c "^\| " _meta/v6_2_reconciliation_log.md` (expect ~37 table rows) |
| **Stage 4.1 lpf production proof APPROVED** (Stage 4.1 closeout 2026-05-26) | `format-a-notices/lpf__linon-powell-furniture__brief.md` (137 lines) + `__delivery-email.md` (44 lines) present | `wc -l format-a-notices/lpf__*.md` |
| **Appendix B.4 + B.5 present in this doc** | Appendix B.4 (CL-025 reconciliation discipline) + Appendix B.5 (Stage 4.1 lpf operational lessons) appended below | `grep -n "^## Appendix B\." _meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` (expect B.4 + B.5 matches) |

**If ANY row fails verification, STOP and flag immediately.** Do not improvise around the gap. The outgoing planning agent's snapshot may be stale, or Stage 3.5 closeout may have partially executed, or the file system may be in a partial-sync state (iCloud).

### CL-NNN status — verify each from `_meta/stage3_cleanup.md`

| CL | Expected status | Stage 4 relevance |
|---|---|---|
| CL-001 / CL-003 / CL-004 | OPEN (universal forbid stamped; Stage 4 production verifies) | Each `stage_4_X` prompt enforces via `_root/04 §3` pointer |
| CL-005 | OPEN (additive roadmap section in all formats) | Each per-account brief includes `_root/03 §3` roadmap pointer; entity-packet parent letter EXCLUDES per `_root/04 §4.15.4` (per-child territory) |
| CL-007 | OPEN (Foundation/03 D-004b ladder bands stamp) | Stage 4 prep candidate — operator decides if source-fix to `_root/03` before Stage 4.1 |
| CL-011 | OPEN OR RESOLVED — verify Format A template references `platform_discount_correction` not `discount_correction` | Verify in `format-a-notices/_brief-template.md` driver dispatch table |
| CL-014 | RESOLVED 2026-05-26 (Stage 3.5 prep) | Entity-packet template architecture closed |
| CL-015 | **RESOLVED 2026-05-26 (Stage 4 prep Source-fix Session A)** — `_root/04 §4.16` Annual-cohort voice rules landed (4 sub-sub-sections: Scope / Lede effective-date shift / Close + formal-notice line / Drafter judgment + surfacing); `_root/06 §4.3` voice-consequence bullet updated on landing. Outstanding `renewal_date` v6.2 column gap operator-stamped defer-to-first-annual (`_master-account-data-v6.2.csv` does NOT currently carry the column; surface at first Annual proof per Cohort E pre-requisite annotation in ledger). | Stage 4.4 Good News + any Annual-overlay account references §4.16 by pointer. Cohort E rows blocked until `renewal_date` source decision operator-stamped at first Annual proof. |
| CL-017 | OPEN (per-account operator judgment for Critical band) | Applies during Stage 4 routing pre-flight for Critical-band accounts |
| CL-018–021 | OPEN (Format A v2 exemplar drift) | Each Stage 4 Format A production draft replaces the corresponding v2 exemplar; CL closes per-account on operator stamp |
| CL-022 | **RESOLVED 2026-05-26 (Stage 4 prep Source-fix Session B)** — `_root/07 §7.5` delivery-email routing-block subset matrix landed (22-field × 5-format + 7-row conditionals + per-format omissions narrative + closing Rule paragraph; covers all 5 formats); planning agent on landing stripped CL-022 note blockquotes from all 5 delivery-email templates + replaced with single canonical pointer line per operator-stamped strip-and-replace decision; Format A `Comm_action:` line added + §7.5 `Support fire cleared:` matrix row added per operator-stamped resolve-both decision. | Stage 4.2–4.5 delivery-email Section 2 routing blocks reference `_root/07 §7.5` by pointer. |
| CL-023 | OPEN (v6.2 maintenance — TBI primary rows with URN secondary re-evaluated against IUR marker) | Per-account surface during Stage 4 production for affected ord_ids; operator-stamps per-account whether to override v6.2 coding |
| CL-024 | **RESOLVED 2026-05-26 (Stage 3.5 review pass)** — Stage 3.5 fresh-agent session passed strict + paste-verification protocol; surfaced the Thesis `delivery_owner` discrepancy via the protocol (validating the CL-024 strengthening design — paste-verification forced verbatim source-reading which exposed rule-layer/CSV drift that pointer-only reading would have missed) | Strict + paste-verification language carries forward into every `stage_4_X` prompt per Appendix A.10 design constraint; Stage 4 inherits the discipline by reference |
| CL-025 | **RESOLVED 2026-05-26 (Stage 4.1 lpf production proof closeout — planning-agent layer)** — v6.2 reconciliation discipline operator-stamped Option (1): v6.2 modeled wins per Appendix B; reconciliation flag → INTERNAL ops cleanup pre-effective-date; client copy NEVER mentions "unused users"; source-fix at `_root/07 §4.5` + `_root/05 §2.1.5` + `_root/04 §4.9`; `_meta/v6_2_reconciliation_log.md` tracker created (37 flagged rows from cohort sweep); `enabled_users` column added to v6.2 at position 15. **Appendix B.4 codifies the discipline at planning-agent layer.** | Every Stage 4.X session applies the Step 4 reconciliation-discipline check per the Stage 4.1 prompt's Step 4 pattern + `_meta/stage4_prompts/README.md` review-protocol Step 4. Tracker is the per-account ops cleanup workstream. |
| CL-000 | OPEN (deferred — routing-CSV errata mirror in `_root/06 §2 + §7` is authoritative) | Stage 4 production uses the mirror; does not re-introduce errata to the source CSV |

### Stage 4 prep candidates — ALL 6 CLOSED at Stage 4 prep + Stage 4.1 closeout (do NOT re-surface)

**Stage 4.2–4.5 agent: this section is historical context only. All 6 candidates were operator-stamped + applied during Stage 4 prep (Source-fix Sessions A + B, 2026-05-26) + Stage 4.1 closeout (CL-025 source-fix, 2026-05-26). Do NOT re-surface these via `AskQuestion` — the rule layer is stable for Stages 4.2–4.5.**

1. **CL-015 (Annual overlay voice rules)** — **RESOLVED 2026-05-26** at `_root/04 §4.16` (Stage 4 prep Source-fix Session A; 4 sub-sub-sections; `_root/06 §4.3` voice-consequence bullet updated on landing). Outstanding `renewal_date` v6.2 column gap operator-stamped defer-to-first-annual.
2. **CL-022 (delivery-email routing-block field-list)** — **RESOLVED 2026-05-26** at `_root/07 §7.5` (Stage 4 prep Source-fix Session B; 22-field × 5-format matrix + 7-row conditionals + per-format omissions narrative; all 5 delivery-email templates' Section 2 strip-and-replaced on landing; Format A `Comm_action:` added; §7.5 `Support fire cleared:` row added).
3. **`_root/04 §1.1` audience register** — **RESOLVED 2026-05-26** at `_root/04 §1.1` (Stage 4 prep Source-fix Session A; 4-row table contrasting program audience [CFO/owner/principal of furniture/lighting/decor wholesaler] with SaaS-renewal-drift audiences [procurement, IT buyer, "platform admin"]; the framing previously lived in Appendix A §2 of this handoff; now source-fixed + referenced by pointer).
4. **`_root/04 §3` 6 SaaS-renewal forbidden-phrase rows** — **RESOLVED 2026-05-26** at `_root/04 §3` (Stage 4 prep Source-fix Session A; 26 → 32 rows; reconciles pre-existing manifest-vs-table off-by-one; SaaS-renewal-vocabulary entries [renewal, auto-renew, at renewal we're adjusting, rate card alignment, refresh, subscription renewal] now propagate to all 5 Stage 3 templates + all `stage_4_X` prompts via existing `_root/04 §3` pointers).
5. **`_root/08` entity-packet-specific QB-NNN additions** — **RESOLVED 2026-05-26** at `_root/08 §10` (Stage 4 prep Source-fix Session B; 12 entity-packet program QB-NNN blockers QB-127 through QB-138; planning agent on landing converted EP-* identifier bullets in both entity-packet templates' Section 4 to QB-NNN pointers; Stage 3.5 deferred item #5 RESOLVED).
6. **CSV-vs-rule-layer reconciliation discipline** — **RESOLVED 2026-05-26** (Stage 3.5 review-pass lesson; operator-stamped at Stage 4 prep). The CSV is canonical for entity-level + account-level scope per `_root/06 §1.6` + `_root/07` Master Account/Entity tab stamps; rule-layer enumerations reconcile to CSV. Codified in **Appendix B** of this handoff (CSV canonical principle). Forward propagation: every `stage_4_X` Step 3 routing verification re-derives `delivery_owner` / `migration_driver` / `notice_cohort` / `health_band` from the CSV row at draft time per Appendix A.4 routing-as-hard-gate stamp.

### Stage 4.1 closeout addition (NEW since original handoff — operationalizes during Stage 4.2–4.5)

7. **CL-025 (v6.2 reconciliation discipline)** — **RESOLVED 2026-05-26** at planning-agent layer (Stage 4.1 lpf production proof closeout). Operator-stamped Discipline (1): v6.2 modeled wins per Appendix B; reconciliation flag → INTERNAL SuperCat ops cleanup pre-effective-date; client copy NEVER mentions "unused users." Source-fix landed at `_root/07 §4.5` (Resolution discipline paragraph) + `_root/05 §2.1.5` (After-row canonicality paragraph) + `_root/04 §4.9` (drafter-facing operational note); operational artifacts created: `_meta/v6_2_reconciliation_log.md` tracker (37 flagged rows pre-populated from cohort sweep) + `_master-account-data-v6.2.csv` `enabled_users` column at position 15. **Codified in Appendix B.4 of this handoff.** Forward propagation to Stages 4.2–4.5: every per-account session applies Step 4 reconciliation-discipline check (per Stage 4.1 prompt's Step 4 pattern + `_meta/stage4_prompts/README.md` review-protocol Step 4 audit); planning agent verifies flagged accounts have a tracker row + records `drafter_session_id` cross-reference in tracker `notes` column.

**The rule layer is stable for Stages 4.2–4.5.** Your job is `stage_4_2` → `stage_4_3` → `stage_4_4` → `stage_4_5` drafter-prompt authoring + production proofs + ledger rows. No further Stage 4 prep candidates are anticipated; if you surface one mid-session, treat as a new CL-NNN entry per `_meta/stage3_cleanup.md` filing convention + `_root/CONTRACTS.md §3` rule-change protocol.

### Stage 3.5 deferred items (documented for forward visibility; not Stage 4 prep blockers)

Five items were deferred at Stage 3.5 review pass per the planning agent's recommendation + operator stamp; track for Stage 4 production / Wave 6 surface:

1. **Sentence 2 of entity-packet delivery email Paragraph 2** (cross-brand consolidation lens summary + 48-hour signal) — currently template scaffolding (drafter-generated structural form); deferred from promotion to `_root/04 §4.15.6` delivery-email-specific 48-hour signal sub-section. Consistent with Stage 3.1–3.4 precedent of accepting template scaffolding for cross-format structural-form sentences. Surface at Stage 4.5 production if recurring drafter-judgment variance produces inconsistency.
2. **CL-005 roadmap promotion to entity-packet parent letter** — `_root/03 §3` "What's Coming in 2026" verbatim block is per-child territory per `_root/04 §4.15.4` (already operator-stamped at Stage 3.5 prep). Revisit only if Stage 4.5 production surfaces operator concern that the parent letter feels under-developed without portfolio-level roadmap.
3. **`_root/04 §4.15.2` member-brand enumeration example sub-section for 4-brand entities** (Gabriella White, Godinger Group, Visual Comfort & Co.) — currently drafter-generated at Stage 4.5 production. Promote to `_root/04 §4.15.2` example sub-section only if recurring drafter-judgment variance across the 3 four-brand entities produces inconsistent rendering at Stage 4.5 production.
4. **`_root/07 §7` entity-packet routing-block row enumeration** — Wave 6 batch scope; see prep candidate #2 above (CL-022).
5. **`_root/08` entity-packet-applicable QB-NNN values enumeration** — Wave 6 batch scope; see prep candidate #5 above.

**Stage 4 prep is the analog of Stage 3.5 prep**: any source-fix surfaced here should be operator-stamped BEFORE the corresponding `stage_4_X` prompt is authored, so the prompt can reference the source-fixed rule by pointer (not by restated content in the prompt body).

---

## §3.5. Mid-cohort state snapshot delta (2026-05-26 end-of-session-N; verify EVERY ROW from disk)

**This section is the Amendment-5-delta layer on top of §3.** Where §3 row says one thing and §3.5 row says another, §3.5 wins (§3 was authored at Stage 4.1 closeout — pre-Stage-4.2-cohort-iter). Verify all line counts + Last-updated dates via `wc -l` + `grep -n "Last updated" _root/*.md` BEFORE producing the §8 confirmation block.

### Rule-layer line counts (post-CL-027)

| Doc | Pre-Amd-5 (Stage 4.1 close) | Post-Amd-5 (end-of-session-N) | Δ | Driver |
|---|---|---|---|---|
| `_root/00_manifest.md` | 224 | 229 | +5 | CL-026/023/027 manifest refreshes |
| `_root/CONTRACTS.md` | 109 | 109 | 0 | — |
| `_root/01_why_we_are_migrating.md` | 81 | 81 | 0 | — |
| `_root/02_who_is_being_migrated.md` | 178 | 178 | 0 | — |
| `_root/03_what_we_sell.md` | 244 | 244 | 0 | — |
| `_root/04_communication_posture.md` | 568 | 568 | 0 | — |
| `_root/05_driver_taxonomy.md` | **819** | **850** | **+31** | CL-026/CL-023 (§2.3.2/§2.4.1/§2.4.7 + 7→8 combinations) + CL-027 (§2.1.2 reduction sub-block + §2.1.7 rewrite + §2.4.1/§2.4.7 URN extension + §4 row 5 re-tally + 8→9 combinations + §1.1 URN count update + §1.3 hygiene) |
| `_root/06_format_routing.md` | 319 | 319 | 0 | — |
| `_root/07_data_pipeline.md` | 475 | 475 | 0 | — |
| `_root/08_quality_bar.md` | 960 | 960 | 0 | — |
| `_root/09_changelog.md` | **620** | **697** | **+77** | CL-026 + CL-023 joint RESOLVED entry + CL-027 RESOLVED entry |
| **Cumulative footer** | **4,597** | **4,710** | **+113** | Verify via `wc -l _root/*.md _root/CONTRACTS.md` and `_root/00_manifest.md §2` cumulative line |

### Meta / data line counts

| File | Post-Amd-5 | Driver |
|---|---|---|
| `_meta/stage3_cleanup.md` | 332 (CL-026 + CL-027 RESOLVED entries) | Stage 4.2 cohort iter 2 + iter 3 |
| `_meta/stage4_account_ledger.md` | 154 (cci row APPROVED + lpf row APPROVED; sca row PENDING audit) | Stage 4.2 iter 1 closeout |
| `_meta/v6_2_reconciliation_log.md` | 100 (37 flagged rows + bri driver-annotation update from IUR→TBI) | Stage 4.2 iter 2 source-fix propagation |
| `_meta/stage4_prompts/stage_4_2__format-b__per-account-drafter.md` | 697 (Stage 4.2 canonical drafter — APPROVED via cci) | Stage 4.2 prompt authoring |
| `_meta/stage4_prompts/_paste-ready/stage_4_2__cci.md` | 841 (cci closeout artifact) | iter 1 |
| `_meta/stage4_prompts/_paste-ready/stage_4_2__bri.md` | ~830 (bri hard-stop artifact; v2 not yet refreshed) | iter 2 — refresh pending bri re-decision |
| `_meta/stage4_prompts/_paste-ready/stage_4_2__sca.md` | **886 (v2 post-CL-027 refresh)** | iter 3 — drafter subagent in-flight |
| `_master-account-data-v6.2.csv` | 346 (10 rows re-stamped 2026-05-26 per CL-026/CL-023; `enabled_users` column at position 15 from Amendment 4) | Stage 4.2 iter 2 source-fix |
| `_archive/2026-05-26__pre-cl-026/_master-account-data-v6.2__pre-cl-026-snapshot.csv` | 346 (pre-stamp baseline) | CL-026 audit-trail preservation |

### v6.2 driver-stamp-vs-field-signature audit baseline (post-CL-026 + CL-023 + CL-027)

- Pre-CL-026 baseline: 96 pass / 8 flag / 3 fail = **89.7% clean** (Stage 4.2 iter 2 audit 2026-05-26)
- Post-CL-026 + CL-023 + CL-027 baseline: 98 pass / 8 flag / 1 fail = **91.6% clean** (+1.9 pts)
- Remaining 1 FAIL: `kii` (kraftware-international) — documented as `_root/05 §2.5.6` special case (ABTS-primary cap-band-rebase); not a stamping error
- Remaining 8 flags: informational-only post-Option-A semantic (TBI-primary or URN-primary + IUR-secondary cases; expected by the §2.4.1 + §2.4.7 semantic extension — IUR-as-secondary now valid for BOTH expansion + reduction direction-cases per CL-026 + CL-027)
- **Audit-rerun discipline**: if you re-stamp v6.2 in any future session, re-run `_archive/2026-05-26__pre-cl-026/v6_2_driver_signature_audit.py` (or equivalent `csv.DictReader`-driven enumeration) + log the new pass/flag/fail counts in `_meta/stage3_cleanup.md` + `_root/09`. Pre-snapshot the CSV before any re-stamp (mirror the `_archive/2026-05-26__pre-cl-026/` pattern).

### Stage 4.2 cohort status (per `_meta/stage4_account_ledger.md`)

| Iter | ord_id | Status | Date | Notes |
|---|---|---|---|---|
| 1 | `cci` (Currey & Company) | **APPROVED** | 2026-05-26 | Format B standard variant; clean closeout; no source-fix |
| 2 | `bri` (Bulbrite) | **DEFERRED** | 2026-05-26 | Hard-stopped at v1 → CL-026 + CL-023 jointly RESOLVED → operator-stamped `apply_source_fix_only_no_bri` (bri re-paste-run deferred; technically unblocked post-CL-027) |
| 3 | `sca` (Shadow Catchers) v2 | **IN-FLIGHT** | 2026-05-26 | Hard-stopped at v1 → CL-027 RESOLVED at `_root/05 §2.1.2` → v2 paste-ready refreshed → drafter subagent running in parallel Cursor agent |
| 4+ | TBD | PENDING | — | Remaining Format B accounts in the 107 pending pool — exact count not pre-computed; verify cohort sizing via `_meta/stage4_account_ledger.md` cohort tally + `csv.DictReader` enumeration of `comm_action ∈ {notice-and-meeting, 60-day-notice with delta_mrr > $300 routing to Format B}` before authoring next Format B paste-ready |

### CL-NNN status delta (re-confirm from `_meta/stage3_cleanup.md`)

**Resolved during Amendment-5 catalyst session**:

| CL | Status post-Amd-5 | Resolution |
|---|---|---|
| **CL-023** | **RESOLVED 2026-05-26** (jointly with CL-026) | v6.2 secondary_drivers re-evaluation for TBI-primary + URN-secondary 25→40 cluster → operator-stamped Option A semantic at `_root/05 §2.4.1` (IUR-as-secondary covers both expansion + reduction direction-cases; §2.3.2 sub-block prose already accommodates expansion); 8 rows re-stamped URN-secondary → IUR-secondary (7 standalone + 1 sccon compound preserving MOR) |
| **CL-026** | **RESOLVED 2026-05-26** (jointly with CL-023) | bri + bcf v6.2 driver-stamp mis-alignments → bri re-stamped IUR-primary → TBI-primary (with IUR-secondary appended); bcf re-stamped ABTS-primary → URN-primary (with IUR-secondary appended); 10 total v6.2 rows re-stamped; pre-snapshot preserved at `_archive/2026-05-26__pre-cl-026/`; audit baseline 89.7% → 91.6% clean |
| **CL-027** | **RESOLVED 2026-05-26** | `_root/05 §2.1.2` Format B URN canonical sub-block scope-gap (reduction-direction missing) → operator-stamped Option 2 source-fix; added parallel `[IF excess users remain AND secondary driver = included_user_reduction (base shrinking from legacy to current tier standard)]` sub-block mirroring §2.1.3 reduction-direction sub-block (locate by marker text, not line number); §2.1.7 routing rewritten; §2.4.1 Option A semantic extended to URN-side; §4 matrix row 5 count 7 → 26 with named enumeration + mutual-exclusivity codified; rule-layer-only fix (no v6.2 re-stamps) |

**Still open** (carry-forward from §3 CL-NNN table — no change at Amendment 5):

- CL-001 / CL-003 / CL-004 / CL-005: OPEN (universal forbids; Stage 4 production verifies per-account)
- CL-007: OPEN (Foundation/03 D-004b ladder bands)
- CL-011: verify Format A template references `platform_discount_correction` (re-verify during Stage 4.4 or 4.5 prompt authoring)
- CL-017: OPEN (per-account operator judgment for Critical band)
- CL-018–021: OPEN (Format A v2 exemplar drift)
- CL-000: OPEN (routing-CSV errata not baked into source CSV)

### In-flight work + first-action sequencing

**At the moment you receive this handoff**:

1. **Parallel Cursor agent is running `sca` v2** (`_meta/stage4_prompts/_paste-ready/stage_4_2__sca.md` v2, 886 lines). The operator is applying the CL-027 file diffs (the 6 surgical `_root/05` edits + `_meta/stage3_cleanup.md` CL-027 entry + `_root/09_changelog.md` CL-027 entry + `_root/00_manifest.md` refresh + v2 paste-ready stamp + planning-agent self-corrections) to the parallel agent's context BEFORE that agent runs the drafter task. When that drafter finishes, it produces `format-b-notices/sca__shadow-catchers__brief.md` + `__delivery-email.md` + a conformance block.
2. **The operator will paste that conformance block + file paths back to YOU** (this new agent) for review. **Your §9 first action is to run the planning-agent audit pass on those artifacts per §6 review protocol + Appendix B.5.1 + Appendix B.5.2.** See §9 rewrite below.

**If you receive the handoff BEFORE the parallel agent finishes sca v2**: produce the §8 confirmation block, then STOP and wait. Do NOT start authoring Stage 4.3 / 4.4 / 4.5 prompts in parallel — the audit-then-decide cadence ordering (sca v2 close → self-audit → bri-decision → next-format) is operator-stamped at Amendment 5 to prevent compounding drift.

**If you receive the handoff AFTER the parallel agent finishes sca v2** (operator pasted conformance block + file paths in the same message as this handoff): produce the §8 confirmation block, then proceed directly to §9 Action 1 (sca audit).

---

## §4. The architectural concepts you must internalize before authoring any `stage_4_X` prompt

These are the 8 load-bearing concepts that shape every Stage 4 drafter prompt + every per-account review pass. **Concepts 1–7 inherited from Stage 3 (verbatim formulation in `_meta/stage3_prompts/PLANNING_AGENT_HANDOFF.md §4`; do not restate here — fetch from there).** Concept 8 is new for Stage 4.

### 4.1–4.7. Concepts inherited from Stage 3 (`_meta/stage3_prompts/PLANNING_AGENT_HANDOFF.md §4.1–§4.7`)

- Path-reference contract (`_root/CONTRACTS.md §5`)
- Strict-placeholder precedent (operator-stamped 2026-05-26)
- Manifest-echo contract (`_root/00_manifest.md §6`)
- Conformance-block format (`_root/00_manifest.md §5`)
- Pattern inheritance compounds (operator-stamped 2026-05-26)
- Source-fix-at-source > template-level carve-out
- Cross-template structural rules stamp at the template level

Recite each in one sentence in your handoff-confirmation block (§8 below).

### 4.8. Path-reference inversion at production scope (NEW for Stage 4)

At **template scope** (Stage 3), the file carries `[INSERT _root/XX §N.M ...]` pointers and the rule prose lives in the `_root/` doc. At **production scope** (Stage 4), the file carries the actual rule prose — fetched verbatim from the owning `_root/` doc per the template's pointer, with `[BRACKETED_TOKENS]` substituted from v6.2 + Postgres per `_root/07 §2 + §4`. **The strict-placeholder precedent does NOT relax at Stage 4**: the agent pastes character-for-character (not paraphrased, not summarized, not "improved"). Paraphrase of owned rule prose at production scope = automatic fail in review.

The drafter's allowable creativity is narrow and pre-enumerated in Appendix A §5 of this handoff (the "Allowed drafter-generated prose (narrow)" list). Anything outside that narrow list is fetch-and-paste.

The path-reference inversion is the architectural mirror of the path-reference contract. They are the same discipline applied at two different artifact scopes. If you find yourself relaxing strict-placeholder at Stage 4 because "it's the production artifact now, not the template" — STOP. The discipline is identical at both scopes; only the artifact form changes.

---

## §5. Wave sequence — Stage 4 has two phases

Stage 4 is NOT a single linear wave. It is two phases with different rhythms.

### Phase 4-prep: author 5 drafter prompts (you produce these — 1 per format)

| Wave | File you author | Scope | Status |
|---|---|---|---|
| 4.1 | `_meta/stage4_prompts/stage_4_1__format-a__per-account-drafter.md` | Format A 60-Day Notice — single-account drafter prompt | **✅ APPROVED 2026-05-26 (638 lines)** — Stage 4.1 planning agent authored + closed; production proof `lpf` (Linon/Powell Furniture) APPROVED 2026-05-26 as Format A; ledger row filed APPROVED. **Pattern reference for 4.2/4.3/4.4/4.5.** |
| 4.2 | `_meta/stage4_prompts/stage_4_2__format-b__per-account-drafter.md` | Format B Notice + Meeting — single-account drafter prompt | **PENDING — START HERE** |
| 4.3 | `_meta/stage4_prompts/stage_4_3__ceo-letter__per-account-drafter.md` | CEO Letter + Call Commitment — single-account drafter prompt (3-location date parity verification) | PENDING |
| 4.4 | `_meta/stage4_prompts/stage_4_4__good-news__per-account-drafter.md` | Good News Notice — single-account decrease-side drafter prompt | PENDING |
| 4.5 | `_meta/stage4_prompts/stage_4_5__entity-packets__parent-letter-per-account-drafter.md` + orchestration playbook in `_meta/stage4_account_ledger.md` §Entity-packet orchestration playbook | Entity-packet parent letter — single-entity drafter prompt; orchestration playbook for per-child notice sequencing (1 parent + N children with 48-hour Day 0 → Day 1–2 sequencing) already operator-stamped in ledger §Entity-packet orchestration playbook at Stage 4.1 closeout | PENDING — sub-structure operator-stamped Q8 2026-05-26 (one drafter prompt + orchestration playbook in ledger; NOT multiple sub-prompts) |

**Target length per `stage_4_X`**: 400–650 lines (Stage 4.1 = 638 lines reference). Mirrors Stage 3.3 / Stage 3.5 prompt scale + adds Appendix A.1–A.12 verbatim in Step 1 + 8-step canonical skeleton per Appendix A.11.

**Wave order**: 4.2 → 4.3 → 4.4 → 4.5 (Stage 4.1 already complete). Pattern inheritance compounds — Stage 4.2 inherits from 4.1; 4.3 inherits from 4.1 + 4.2; 4.4 inherits from 4.1 + 4.2 + 4.3; 4.5 inherits from 4.1 + 4.2 + 4.3 + 4.4. **Operator may stamp a different order at your handoff confirmation** if there's a cohort-scheduling reason (e.g. Annual cohort renewal-date cluster makes 4.4 Good News more urgent). Default = sequential 4.2 → 4.3 → 4.4 → 4.5.

**Stage 4.5 sub-structure operator-stamped 2026-05-26** (Q8 at Stage 4 prep): ONE drafter prompt for parent-letter artifact + orchestration playbook (already filed in `_meta/stage4_account_ledger.md` §Entity-packet orchestration playbook at Stage 4.1 closeout) for per-child notice dispatch through format-routed `stage_4_X` per-format prompts. NOT multiple sub-prompts (4.5a / 4.5b / 4.5c). Re-confirm in your handoff confirmation block.

### Phase 4-production: per-account drafting loop (you orchestrate; fresh agents execute)

After all 5 `stage_4_X` prompts are operator-approved, the per-account production loop begins. Per-account session shape:

1. **Planning-agent routing pre-flight (you)**: for each `ord_id` in scope, run the 6-step routing flow per `_root/06 §2` against the v6.2 row (`_master-account-data-v6.2.csv`). Determine the format (Format A / B / CEO Letter / Good News / entity-packet child-of-entity).
2. **Format dispatch (you)**: select the appropriate `stage_4_X` drafter prompt (4.1 / 4.2 / 4.3 / 4.4 / 4.5).
3. **Hand to fresh drafter (operator)**: operator pastes the `stage_4_X` prompt + the `ord_id` parameter into a fresh Cursor agent chat. The fresh agent has no prior context; the prompt + `ord_id` is the entire session.
4. **Fresh drafter produces 2 files (drafter)**: `<format>-notices/[ord_id]__[company-slug]__brief.md` + `<format>-notices/[ord_id]__[company-slug]__delivery-email.md` per `_root/07 §6` file-naming. Returns conformance block in chat.
5. **Planning-agent review (you)**: operator pastes the conformance block + the two files' paths back. You run the per-account audit (§6 below).
6. **Operator stamp (operator)**: via your `AskQuestion`. Either approve as-drafted, approve with operator-stamped revisions (you apply), OR request fresh-agent revision (operator re-pastes prompt + ord_id + revision notes to drafter).
7. **Per-account ledger update (you)**: append to `_meta/stage4_account_ledger.md` (you create this file at Stage 4 prep — see §9 below). One row per account. Per-account changelog entry NOT required for `_root/09` unless the per-account proof surfaces a structural issue (rule-layer or template-layer).

Each per-account session is `ord_id`-scoped. **One account in. Two files out. Conformance block. STOP. Batch drift = automatic fail.**

### Production proof gate (the validation step before bulk production)

Between Phase 4-prep and full Phase 4-production: a **production proof gate** runs 1 account per format (5 total proof accounts) through the full per-account loop. The 5 proofs validate that each `stage_4_X` prompt produces a clean per-account artifact end-to-end. Only after all 5 proofs are operator-stamped APPROVED does Phase 4-production scale to the remaining ~80 accounts.

**Do not call this "Stage 5"** — the historical "Stage 5" in `_root/09_changelog.md` is the meta-stage that authored `_root/00_manifest.md` (already completed). The production proof gate is its own labeled gate, not a renumbered stage. Suggested label: **"Stage 4 proof gate"** or **"Stage 4.6 production proof"**. Operator-stamped at the planning agent's discretion when surfacing the gate at the appropriate point.

---

## §6. Review protocol (per-account)

The per-account audit pattern is materially different from Stage 3 template review. Stage 3 reviewed 2 template files at a time (1 brief + 1 email — pattern + structure). Stage 4 reviews per-account artifacts — same 2 files but with substituted prose + math reconciliation against v6.2.

### Step 1: Read both delivered files in full

The fresh drafter produces 2 files. Read both via the Read tool. Note line counts.

### Step 2: Per-account audit table

| Audit | What you're checking | Source-of-truth | QB-NNN |
|---|---|---|---|
| Path-reference contract | Count inlined rule prose paraphrases in customer-copy sections; should be 0 | Customer-facing sections of each file; compare each `[INSERT _root/XX §N.M ...]` block against the `_root/` source character-for-character | QB-119 |
| Strict-placeholder precedent | Every owned rule prose is pasted character-for-character (no paraphrase, no abbreviation) | The 4 `_root/` source blocks the template's pointers reference for this format | QB-119 |
| Math reconciliation | Before / After / Delta MRR + Annual totals match the v6.2 row exactly | The `ord_id`'s row in `_master-account-data-v6.2.csv` | QB-104 + QB-105 |
| Postgres-stat fetch | Lede stat is from a Postgres MCP query OR uses the `_root/07 §5` `composite_narrative` fallback verbatim — never invented | Postgres MCP query result OR `_root/07 §5` fallback table | QB-046 + fallback rules |
| Driver-block paste fidelity | Driver block matches `_root/05 §N.M` character-for-character (the per-format canonical block; no paraphrase, no abbreviation) | `_root/05 §N.M` for the routed format | QB-119 |
| Routing-block field list | Matches `_root/07 §7` per-format row exactly | `_root/07 §7` row for the routed format | QB-039 + per-format QB |
| Routing 6-step trace | Each step's evaluation result recorded in conformance block; the format selected matches the trace's terminal result | Per-account routing trace in conformance block + `_root/06 §2` 6-step flow | QB-038 + QB-039 |
| Format-folder placement | File written to the correct folder for the routed format | `_root/07 §6` file-naming + folder-mapping table | QB-101 |
| Close-correctness | Close text matches format-specific `_root/04 §4.12` variant verbatim (formal-notice line present for Format A / B / CEO Letter; ABSENT for Good News; 3-location date parity for CEO Letter) | `_root/04 §4.12` variants | QB-086 |
| Forbidden-phrase check | Zero hits against `_root/04 §3` forbidden-phrase table | `_root/04 §3` 27-row table | QB-064 + QB-085 |
| Internal-routing scrub | Routing block removed before send (template metadata; not client-facing) | Confirm "Section 2" routing block is bracketed for stripping; not inlined in send output | QB-101 |
| Audience register | Customer copy reads as vendor-to-principal OR peer-to-peer; no SaaS-renewal vocabulary; no health-band names; no peer-range dollars | `_root/04 §1` voice posture + §3 forbidden-phrase table + Appendix A §2 (audience register) of THIS handoff | QB-046 + QB-085 |

### Step 3: Surface operator decisions via `AskQuestion`

Typical per-account decision points:

- **Approve / revise / re-draft** — bundle audit results into a single decision question with 3 options.
- **CL-017 Critical-band per-account judgment** — for Critical-band accounts, operator decides per-account whether to draft or defer.
- **CL-023 v6.2 secondary_drivers override** — if the account has TBI primary + URN secondary, operator stamps per-account whether to apply the IUR re-evaluation.
- **Source-fix surfaced by per-account review** — if a structural issue with an underlying `_root/` rule surfaces (analogous to CL-013 / CL-012 / CL-016 / Stage 3.4 lede normalization at Stage 3 review), apply source-fix-at-source per architectural concept #6.

### Step 4: Execute closeout edits

Per-account closeout is LIGHTER than Stage 3 review-pass closeout (no template-level changelog entry required for routine per-account proofs). Standard edits:

| Edit | File | What to change |
|---|---|---|
| Apply per-account revisions (if any) | The two per-account files | Per the operator-stamped revisions |
| Append to per-account ledger | `_meta/stage4_account_ledger.md` | New row: ord_id / company-slug / format / drafter session ID / brief path / email path / review date / operator stamp date / notes |
| Apply source fix (if surfaced) | The relevant `_root/` doc | Per the operator-stamped resolution; full propagation sweep per `_root/CONTRACTS.md §3`; append `_root/09_changelog.md` entry for the source-fix |
| Update CL tracker (if applicable) | `_meta/stage3_cleanup.md` | Mark CL-018/019/020/021 RESOLVED per-account as Format A v2 exemplars are replaced; close CL-017 per-account as Critical-band judgments are stamped; close CL-023 per-account as IUR re-evaluations are stamped |

### Per-account failure protocol

If a per-account proof draft fails review:

- **1st failure on an account**: planning agent files a feedback note via `AskQuestion`, operator stamps revision direction, drafter retries the same `stage_4_X` prompt with revision notes appended.
- **2nd failure on the same account**: planning agent surfaces to operator as potential template-level issue OR per-account anomaly (e.g. v6.2 data quality issue; missing Postgres data; ambiguous routing). Operator stamps next-step direction.
- **3rd failure on the same account**: STOP. Root-cause review — either the `stage_4_X` drafter prompt has a structural gap, OR the underlying `_root/` rule has ambiguity, OR the v6.2 row has bad data. No further drafter retries until root-cause is operator-stamped resolved.

The failure protocol prevents loops on edge-case accounts. Track failure counts in the per-account ledger.

### Cross-format consistency watchdog

During Phase 4-production, watch for cross-format inconsistencies that surface in real per-account proofs (analogous to Stage 3.3 review pass surfacing the 3-location date parity contract). Examples to watch for:

- Per-account briefs from different formats diverging on a sentence pattern that is supposed to be cross-format consistent (e.g. lede sentence pattern; effective-date format).
- Drafters from different per-account sessions interpreting the same `_root/` rule differently.
- Routing pre-flight producing inconsistent format selection between similar accounts (suggests rule ambiguity).

When a cross-format consistency issue surfaces, propose a template-level stamp per architectural concept #7 (`_meta/stage3_prompts/PLANNING_AGENT_HANDOFF.md §4.7`). Cross-template structural rules at template level, not at rule layer.

---

## §7. Operator interaction protocol

| Situation | What to do |
|---|---|
| Operator pastes a draft `stage_4_X` prompt for review | Read in full; verify against Appendix A constraints; present audit table; `AskQuestion` for approval |
| Operator pastes a fresh drafter's conformance block + file paths | Run §6 per-account audit; present audit results in markdown table; `AskQuestion` for operator stamp |
| Operator pastes a fresh drafter's final chat message | Same as above; chat message often contains gap-list items + open questions that the drafter surfaced for operator decision |
| Operator says "go" or "continue" | Continue previously-paused work; operator is signaling proceed |
| Operator says "draft <X> in parallel" | Begin <X> immediately, alongside any pending review work |
| Operator surfaces a new structural concern | Flag in next changelog entry if material; propose CL-NNN filing if appropriate; do not improvise without operator stamp |
| Source-of-truth ambiguity | Stop and ask via `AskQuestion`; never pick interpretation silently per `_root/CONTRACTS.md §2` |
| Per-account proof review surfaces a `_root/` rule gap | Apply source-fix-at-source per concept #6; full propagation sweep per `_root/CONTRACTS.md §3`; log changelog entry; bump manifest |
| You finish a per-account review with no immediate next task | Volunteer next pending account from the ledger; do not idle |
| You finish all Phase 4-prep waves | Volunteer the production proof gate (1 account per format, 5 total proofs); do not start bulk production without operator stamp on the gate |

**Tone**: direct, declarative, no marketing language. Markdown tables for structured outputs. Use code-reference backticks for file paths, `_root/` paths, and section references. Use the `AskQuestion` tool for operator decisions, NOT chat-text option lists. Never use emojis.

**Forbidden moves** (Stage 4 planning agent specifically — these extend the Stage 3 handoff §9 forbidden moves list):

- Drafting client copy directly (you NEVER write the actual brief or delivery email — only `stage_4_X` prompts and review/closeout artifacts).
- Authoring a `stage_4_X` prompt that batches >1 account per session. One ord_id in, two files out. Period.
- Authoring a `stage_4_X` prompt that doesn't enforce manifest-echo + paste-verification per CL-024 carry-forward.
- Authoring a `stage_4_X` prompt that doesn't lock the job naming per Appendix A §1 ("per-account pricing migration notice drafter for SuperCat's 2026 book normalization — explicitly NOT SaaS renewal writer / CRM sequence author / contract negotiator / template builder").
- Selecting "closest format" for an account that doesn't cleanly route to any of the 5 formats. Escalate per `_root/CONTRACTS.md §2` instead.
- Approving a per-account proof draft with `>0` inlined rule prose paraphrases.
- Skipping the 6-step routing pre-flight for any account before handing to a drafter. The routing pre-flight is a planning-agent responsibility, not a drafter responsibility.
- Reading `_archive/` per-account exemplars (kal/kii/lss v2 specifically — CL-018–021 flag these as drift sources; reading them risks pattern-inheritance from forbidden patterns).
- Marking a doc edited without bumping its `_root/00_manifest.md §2` row + the manifest's own footer "Last updated".
- Skipping the production proof gate before scaling to bulk production.
- Inferring routing from `comm_action` alone — `comm_action` is the OUTPUT of routing, not the input. Always re-derive from the 6-step flow per `_root/06 §2`.

---

## §8. Your handoff-confirmation output (produce this in your first response before doing any other work)

Before authoring any `stage_4_X` prompt or running any per-account session, produce this confirmation block in chat so the operator can verify you have proper context. Use the canonical conformance-block format per `_root/00_manifest.md §5` with the Stage-4-specific additions below.

**Stage 4.2 takeover note (2026-05-26 amendment)**: this confirmation block was originally designed for the Stage 4 transition (Stage 3 → Stage 4) handoff. For your Stage 4.2 takeover (Stage 4.1 → Stages 4.2–4.5), the Stage 4 prep candidates section is re-confirmation only (all 6 CLOSED per §3 amendment) + the wave-order request defaults to 4.2 → 4.5 (Stage 4.1 already complete) + the additions below for Appendix B / B.4 / B.5 recitation. The block is otherwise unchanged.

**Amendment 5 takeover note (2026-05-26 amendment to amendment)**: for the Stage-4.2-finish + 4.3 + 4.4 + 4.5 planning agent (you), the §3 state-snapshot rows reflect Stage 4.1 closeout baseline (PRE-Amendment-5). Use **§3.5 (mid-cohort state snapshot delta)** as the authoritative line-count + status baseline for the confirmation block's state-snapshot rows. Add recitation lines for Appendix B.6 (drift watchlist) + CL-026 / CL-023 / CL-027 RESOLVED. **Use the augmented confirmation block below** (added 2026-05-26 at Amendment 5):

```
Amendment-5 augmentation rows (append to the §8 base confirmation block below; do not replace):

State snapshot verification — Amendment 5 mid-cohort delta (verify from disk; §3.5 is authoritative; §3 is pre-Amendment-5 baseline):
- _root/05_driver_taxonomy.md line count = 850 (post-CL-026 + CL-023 + CL-027): <YES/NO + wc -l output>
- _root/09_changelog.md line count = 697 (post-CL-026 + CL-023 + CL-027 entries): <YES/NO + wc -l output>
- _root/00_manifest.md line count = 229 + cumulative footer = 4,710 (sum of §2 rows): <YES/NO + wc -l + sum>
- _meta/stage3_cleanup.md = 332 lines (CL-026 + CL-027 RESOLVED entries): <YES/NO + wc -l>
- _master-account-data-v6.2.csv post-CL-026 + CL-023 re-stamp baseline 91.6% (98 pass / 8 flag / 1 fail): <YES/NO + audit re-run output>
- _archive/2026-05-26__pre-cl-026/_master-account-data-v6.2__pre-cl-026-snapshot.csv present (audit-trail preservation): <YES/NO + file presence>
- _meta/stage4_account_ledger.md cci row APPROVED 2026-05-26 + lpf row APPROVED 2026-05-26 + sca row pending: <YES/NO + ledger rows>
- _meta/stage4_prompts/_paste-ready/stage_4_2__cci.md (841 lines) + stage_4_2__bri.md (~830 lines DEFERRED) + stage_4_2__sca.md (886 lines v2 IN-FLIGHT): <YES/NO + wc -l>
- format-b-notices/cci__currey-and-company__brief.md + __delivery-email.md present APPROVED 2026-05-26: <YES/NO + wc -l>

CL-NNN status verification — Amendment 5 delta (re-confirm from _meta/stage3_cleanup.md):
- CL-023: RESOLVED 2026-05-26 (jointly with CL-026; Option A semantic at _root/05 §2.4.1 covers TBI+IUR-secondary expansion-direction)
- CL-026: RESOLVED 2026-05-26 (jointly with CL-023; 10 v6.2 rows re-stamped; pre-snapshot preserved)
- CL-027: RESOLVED 2026-05-26 (_root/05 §2.1.2 reduction-direction sub-block + §2.1.7 routing rewrite + §2.4.1 Option A extended to URN-side; rule-layer-only fix)

Appendix B.6 recited (Stage 4.2 lessons + drift watchlist):
- B.6.1 Lessons 1–3 (drafter hard-stops are audit surfaces; joint-resolution scope-gaps; planning-agent self-correction transparency): <your one-sentence-each statement>
- B.6.2 drift watchlist (12 pre-populated findings; you verify + extend): <recite count + acknowledge starting set + extend-as-needed posture>
- B.6.3 audit-discipline guardrails (time-box + verify-before-classify + don't introduce new drift + hierarchical priority + operator-stamps-trim): <one-sentence statement>

In-flight work acknowledgment:
- sca v2 paste-ready (886 lines) is in-flight via parallel Cursor agent at handoff time: <YES, will await operator-pasted conformance block before proceeding | NO if already received>
- bri re-paste-run DEFERRED post-CL-027 (technically unblocked at rule layer): <ACKNOWLEDGED, will surface re-run/skip decision via AskQuestion after sca cohort iter 3 closes + Action 3 self-audit completes>

Action sequence acknowledgment (per §9 Amendment-5 rewrite):
- Action 1 (sca audit) → Action 2 (cohort iter 3 closeout: ledger + changelog + manifest) → Action 3 (self-audit per Appendix B.6) → Action 4 (bri re-run decision) → Action 5–7 (4.3 / 4.4 / 4.5 prompt authoring + production proofs) → Action 8 (production proof gate) → Action 9 (Stage 4 closeout): <ACKNOWLEDGED>

Self-correction-transparency posture acknowledgment (Appendix B.6.1 Lesson 3):
- When refreshing any paste-ready post-source-fix, planning-agent observations that were wrong in the prior version are documented transparently in a self-correction stamp block: <ACKNOWLEDGED>
```

```
─── Planning-Agent Handoff Confirmation (Stage 4) ───────────
Session task: Resume planning-agent role for SuperCat Pricing Migration program at Stage 4 transition; manage Phase 4-prep (5 stage_4_X drafter prompts) + Phase 4-production (per-account loop) + production proof gate.

Manifest echo (per _root/00_manifest.md §1 step 6 + §6 — paste-quote ALL ENTRIES from §2 with title + Last-updated header date):
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

Files read for handoff bootstrap (with last-updated date / mtime):
- <enumerate every file path from §2 of this handoff>

Files NOT read (per §2 "Do NOT read"):
- <enumerate>

State snapshot verification (re-confirm §3 state snapshot from disk — wc -l ground truth + header dates, NOT memory):
- 10 _root/ docs + CONTRACTS.md present with 2026-05-26+ Last-updated headers: <YES/NO + any divergences>
- Manifest §2 line counts reconcile with `wc -l`: <YES/NO + any divergences>
- Stage 3.1 Format A APPROVED (format-a-notices/_brief-template.md + _delivery-email-template.md present at 330 + 130 lines): <YES/NO + actual counts>
- Stage 3.2 Format B APPROVED (format-b-notices/* at 354 + 157): <YES/NO + actual counts>
- Stage 3.3 CEO Letter APPROVED (ceo-letter-notices/* at 366 + 162): <YES/NO + actual counts>
- Stage 3.4 Good News APPROVED + lede normalization (good-news-notices/* at 240 + 162; "monthly pricing is decreasing" in lede; "monthly invoice" only in drafter-facing blockquotes): <YES/NO + actual counts>
- Stage 3.5 entity packets APPROVED (entity-packets/_parent-letter-template.md at 303 lines + _parent-letter-delivery-email-template.md at 241 lines; README Wave 3.5 status APPROVED 2026-05-26 with Thesis source-fix amendment): <YES/NO + actual counts + README status>
- _root/04 §4.15 (6 sub-sections) at source: <YES/NO — paste-quote one sub-section's opening line>
- _root/06 §1.6 rewritten with 14-entity scope + Ferguson exception: <YES/NO — paste-quote the 14-entity claim sentence>
- Dual-canonical v6.2 files present (_master-account-data-v6.2.csv 346 lines + _master-entity-data-v6.2.csv 15 lines): <YES/NO + actual counts>
- _meta/stage4_prompts/ exists with only this handoff at handoff time: <YES/NO + folder listing>

CL-NNN status verification (re-confirm from _meta/stage3_cleanup.md):
- CL-001 / CL-003 / CL-004 / CL-005: <OPEN — universal forbids stamped; Stage 4 production enforces>
- CL-007: <status + Stage 4 prep candidate decision>
- CL-011: <verified absorbed into Stage 3.1 template? YES/NO>
- CL-014: <RESOLVED 2026-05-26 — verify entry in cleanup tracker>
- CL-015: <OPEN — STAGE 4 PREP CANDIDATE for §4.16 or §5 extension>
- CL-017: <OPEN — per-account operator judgment for Critical band>
- CL-018–021: <OPEN — Stage 4 production replaces v2 exemplars per-account>
- CL-022: <OPEN — STAGE 4 PREP CANDIDATE for _root/07 §7 Wave 6 batch>
- CL-023: <OPEN — per-account surface during Stage 4 production>
- CL-024: <RESOLVED 2026-05-26 at Stage 3.5 review pass — verify entry in _root/09 + _meta/stage3_cleanup.md>
- CL-000: <OPEN — deferred; mirror in _root/06 §2 + §7 is authoritative>

Architectural concepts internalized (recite each in one sentence to prove understanding):
1. Path-reference contract: <your one-sentence statement>
2. Strict-placeholder precedent: <your one-sentence statement>
3. Manifest-echo contract: <your one-sentence statement>
4. Conformance-block format: <your one-sentence statement>
5. Pattern inheritance compounds: <your one-sentence statement>
6. Source-fix-at-source > template-level carve-out: <your one-sentence statement>
7. Cross-template structural rules stamp at the template level: <your one-sentence statement>
8. **Path-reference inversion at production scope (NEW for Stage 4)**: <your one-sentence statement>

Operational disciplines recited (Appendices B / B.4 / B.5; planning-agent procedural — recite each in one sentence):
- **Appendix B (CSV canonical)**: <your one-sentence statement — should mention "v6.2 CSVs are canonical for their respective scopes; rule-layer enumerations reconcile to CSV, not the reverse">
- **Appendix B.4 (CL-025 reconciliation discipline)**: <your one-sentence statement — should mention "v6.2 modeled wins for After-row math; reconciliation flag → INTERNAL ops cleanup pre-effective-date; client copy NEVER mentions unused users">
- **Appendix B.5.1 (routing-CSV header-position parse)**: <your one-sentence statement — should mention "every paste-ready annotation parses routing CSV via csv.DictReader; never visual column inspection; one-line attestation required">
- **Appendix B.5.2 (Appendix-B-canonicality-check before pivot)**: <your one-sentence statement — should mention "every audit-surfaced pivot proposal includes an explicit Appendix B canonicality check; v6.2-stamped values are source-fix path not per-account re-route path">

Appendix A constraints recited (A.1–A.12 verbatim citation — paste-quote A.1 + A.3 + A.4 + A.10 + A.11 from this handoff to prove paste-verification):
- A.1 (job naming lock): <paste-quote the full constraint>
- A.3 (single-account scope): <paste-quote>
- A.4 (routing-as-hard-gate): <paste-quote>
- A.10 (CL-024 strict + paste-verification carries forward): <paste-quote>
- A.11 (canonical 8-step skeleton): <paste-quote>

Stage 4 specifics recited (prove understanding):
- Per-account session pattern: <your one-sentence statement — should mention "one ord_id in, two files out, conformance block, STOP">
- Routing pre-flight responsibility (who runs it; at what step): <your one-sentence statement — should name "planning agent runs the 6-step routing per _root/06 §2 against the v6.2 row BEFORE handing the ord_id + stage_4_X prompt to the fresh drafter">
- Job naming lock: <your one-sentence statement — should mention "per-account pricing migration notice drafter for SuperCat's 2026 book normalization; not SaaS renewal / CRM / contract negotiator / template builder">
- Phase 4-prep vs Phase 4-production distinction: <your one-sentence statement>
- Production proof gate: <your one-sentence statement>

Stage 4 prep candidates re-confirmation (all 6 CLOSED at Stage 4 prep + Stage 4.1 closeout — verify each from `_meta/stage3_cleanup.md` + `_root/09_changelog.md` 2026-05-26 entries):
1. CL-015 (Annual overlay voice rules → `_root/04 §4.16`): <CLOSED 2026-05-26 — verify §4.16 present in `_root/04` via grep>
2. CL-022 (delivery-email routing-block field-list → `_root/07 §7.5`): <CLOSED 2026-05-26 — verify §7.5 present in `_root/07` via grep>
3. `_root/04 §1.1` audience register: <CLOSED 2026-05-26 — verify §1.1 present in `_root/04` via grep>
4. `_root/04 §3` SaaS-renewal forbidden-phrase rows: <CLOSED 2026-05-26 — verify `_root/04 §3` table has 32 rows via wc-count>
5. `_root/08 §10` entity-packet QB-NNN additions (QB-127–QB-138): <CLOSED 2026-05-26 — verify §10 present in `_root/08` via grep + QB-127 / QB-138 IDs present>
6. CSV-vs-rule-layer reconciliation discipline: <CLOSED 2026-05-26 — operator-stamped as baseline design constraint; codified at Appendix B above; verify Stage 4.1 prompt Step 3 explicitly re-derives delivery_owner / migration_driver / notice_cohort / health_band from CSV row>
7. **CL-025 (v6.2 reconciliation discipline — Stage 4.1 closeout addition)**: <CLOSED 2026-05-26 — verify _root/07 §4.5 Resolution discipline paragraph present + _root/05 §2.1.5 After-row canonicality paragraph present + _root/04 §4.9 drafter-facing operational note present + _meta/v6_2_reconciliation_log.md file exists + _master-account-data-v6.2.csv enabled_users column at position 15 via head-1>

Stage 3.5 deferred items recited (forward visibility; surface as Stage 4.5 production / future Wave fires):
1. Entity-packet delivery email Paragraph 2 Sentence 2 promotion to `_root/04 §4.15.6`: <DEFER unless Stage 4.5 production surfaces drafter-judgment variance>
2. CL-005 roadmap promotion to entity-packet parent letter: <DEFER per Stage 3.5 prep operator stamp on per-brand mechanics restraint>
3. `_root/04 §4.15.2` 4-brand member-enumeration example sub-section: <DEFER pending Stage 4.5 production variance observation>
4. `_root/07 §7` entity-packet routing-block row: <STATUS — verify whether §7.5 covers this OR if separate §7 row enumeration still pending; if pending, treat as Stage 4.5 production / Wave fire>
5. `_root/08` entity-packet-applicable QB-NNN values: <CLOSED at Stage 4 prep Source-fix Session B — `_root/08 §10` QB-127–QB-138 covers this>
6. **`renewal_date` v6.2 column gap (Stage 4 prep Source-fix Session A audit)**: surface at first Annual proof per Cohort E pre-requisite annotation in `_meta/stage4_account_ledger.md`; 3 options (add column to v6.2 / permanent fallback in routing CSV `nuances` / per-account exemplar); blocks all Cohort E rows.

Wave-order operator-stamp request (Stage 4.2–4.5 — Stage 4.1 already complete):
- Default order: 4.2 → 4.3 → 4.4 → 4.5 (pattern inheritance compounds; Stage 4.1 = Format A is the reference pattern). <Recommend default OR propose alternative with rationale — e.g. if Annual cohort renewal-date cluster makes Stage 4.4 Good News more urgent for Cohort E unblocking, propose 4.4 first>
- Stage 4.5 sub-structure (operator-stamped 2026-05-26 at Stage 4 prep Q8): ONE drafter prompt for parent-letter artifact + orchestration playbook in `_meta/stage4_account_ledger.md` §Entity-packet orchestration playbook for per-child notice dispatch through format-routed prompts; NOT multiple sub-prompts. <Re-confirm understanding>

Open questions for operator before authoring stage_4_1:
- <enumerate any ambiguities you cannot resolve from this handoff + the rule layer; if none, write "none">

Ready to proceed: <YES — will surface Stage 4 prep candidates via AskQuestion next response, then await operator stamps before authoring stage_4_1 | NO — need operator clarification on the open questions above first>
─────────────────────────────────────────────────────────────
```

**STOP after producing this confirmation block.** Do not begin `stage_4_1` authoring or any per-account work until the operator confirms the handoff is clean (operator either pastes approval / paste-back to the outgoing planning agent for review, OR stamps the open-question resolutions, OR stamps the Stage 4 prep candidates per the list above). The handoff confirmation is a load-bearing artifact — it gates the rest of your work.

If you cannot produce one or more sections of the confirmation block (e.g. a file the §2 reading list names is missing or unreadable; a state-snapshot row fails verification; a CL status is ambiguous), STOP and flag immediately — do not improvise around the gap. The outgoing planning agent's state snapshot may have been stale (Stage 3.5 closeout state ambiguous), or the file system may be in a partial-sync state (iCloud), or a prior closeout may have partially executed. The operator decides next steps.

---

## §9. Your first action sequence (after operator approves handoff confirmation) — Amendment-5 rewrite for mid-cohort takeover

**This section was rewritten 2026-05-26 at Amendment 5 for the Stage-4.2-finish + 4.3 + 4.4 + 4.5 planning agent (you).** The pre-Amendment-5 sequence (Stage 4.2 prompt authoring + Stage 4.2 first paste-ready) is preserved in `_root/09_changelog.md` for historical reference; both are now DONE (`stage_4_2__format-b__per-account-drafter.md` 697 lines APPROVED; `cci` paste-ready APPROVED; `bri` paste-ready hard-stopped DEFERRED; `sca` v2 paste-ready in-flight at handoff).

In this order:

### Action 0 — Handoff confirmation (always first)

**Produce the §8 handoff-confirmation block** with state-snapshot verified from disk (use the §3.5 mid-cohort delta as the authoritative baseline; §3's pre-Amendment-5 numbers are stale). Manifest echo + Appendix A + B + B.4 + B.5 recited. **STOP and await operator stamp.** No further work until operator stamps the confirmation clean.

If you receive `sca` conformance block + file paths in the same message as the handoff, you may bundle the §8 confirmation block + Action 1 audit-table preview in a single response (mark them as distinct sections). The operator may stamp both in one round.

### Action 1 — `sca` cohort iter 3 v2 audit + closeout

**When the parallel Cursor agent posts `sca` v2 conformance block + file paths** (`format-b-notices/sca__shadow-catchers__brief.md` + `__delivery-email.md`), run the per-account audit per `§6 review protocol` + Appendix B.5.1 (`csv.DictReader` attestation re-verify) + Appendix B.5.2 (Appendix-B canonicality check). Specifically:

1. **Paste-verification audit (CL-024 carry-forward)**: every owned rule prose paste-quoted in the conformance block must reconcile character-for-character with its `_root/XX §N.M` source (especially the post-CL-027 `_root/05 §2.1.2` reduction-direction sub-block + the `_root/05 §2.1.7` post-CL-027 routing-shape paragraph).
2. **`csv.DictReader` re-derivation** (Appendix B.5.1): re-parse `_master-account-data-v6.2.csv` data row 83 (`sca`) + `migration_comm_tiers_2026-05-19.csv` row for sca's slug; reconcile every routing-relevant field (delivery_owner / migration_driver / secondary_drivers / notice_cohort / health_band / delta_mrr / delta_pct / comm_action / nuances / flags). The drafter's pre-flight attestation must match yours.
3. **After-row math reconciliation** (CL-025; Appendix B.4): `[NEW_EXCESS]` + `[NEW_USER_CHARGE]` + `[NEW_MRR]` pulled directly from v6.2 stamped columns (NOT recomputed). Reconciliation flag computation per `_root/07 §4.5` thresholds. If sca is in `_meta/v6_2_reconciliation_log.md`, record `drafter_session_id` in the tracker's `notes` column.
4. **Routing 6-step trace** (`_root/06 §2`): each step's evaluation result + terminal format selected (Format B notice-and-meeting). Verify the trace matches sca's v6.2 row exactly.
5. **Driver-block paste fidelity**: brief's URN+IUR-secondary driver block must paste verbatim from `_root/05 §2.1.2` (URN canonical) + the post-CL-027 reduction-direction sub-block (locate by marker text: `[IF excess users remain AND secondary driver = included_user_reduction (base shrinking from legacy to current tier standard)]`; not by line number — line numbers drift). Delivery email Section 2 must paste verbatim from `_root/07 §7.5` Format B column.
6. **Format-specific blockers** (QB-NNN by ID): minimum coverage = QB-038 (routing trace) + QB-039 (routing block field-list) + QB-046 (lede stat fetch) + QB-064 (Good News favor framing — N/A here) + QB-085 (peer-dollar) + QB-086 (close-correctness — Format B passive close, not active CEO Letter date) + QB-101 (internal-routing scrub) + QB-104 + QB-105 (math reconciliation) + QB-119 (paste fidelity).
7. **High-delta math sanity check (QB-078 + QB-106)**: sca is a high-delta candidate (URN expansion+reduction interaction); verify delta_mrr / delta_pct against billing math; flag if math reads off-pattern.

**Surface audit results via `AskQuestion`** with one bundled decision: `approve_as_drafted` / `approve_with_planning_agent_revisions` (list the revisions inline) / `escalate_to_drafter_revision` / `escalate_as_source_fix` (if a new CL-NNN candidate surfaces).

**If `approve_as_drafted` or `approve_with_planning_agent_revisions`**: proceed to Action 2 (cohort iter 3 closeout). If `escalate_to_drafter_revision`: refresh sca paste-ready to v3 (or higher) with operator-stamped revision notes; loop. If `escalate_as_source_fix`: file CL-028 (or next available CL-NNN) + propose resolution options via `AskQuestion`; do NOT close cohort iter 3 until source-fix lands.

### Action 2 — Cohort iter 3 closeout (file all root + meta updates)

Per operator's explicit Amendment-5 directive: **"ensure it updates all of the files (root, readme, etc) once stamped 4_2 worked"**:

| Edit | File | What to change |
|---|---|---|
| sca ledger row | `_meta/stage4_account_ledger.md` | Append under Format B section: `ord_id=sca / company=Shadow Catchers / format=Format B / drafter_session=<parallel agent ID> / brief=format-b-notices/sca__shadow-catchers__brief.md / email=format-b-notices/sca__shadow-catchers__delivery-email.md / review_date=YYYY-MM-DD / operator_stamp=YYYY-MM-DD APPROVED / notes=URN+IUR-secondary reduction-direction; post-CL-027 §2.1.2 sub-block production proof` |
| sca closeout changelog entry | `_root/09_changelog.md` | Append under 2026-05-26 entries: production proof closeout (analog to lpf closeout 2026-05-26 + cci closeout 2026-05-26). Cite paste-ready v2 + planning-agent audit results + operator stamp. Update `Last updated` header. |
| Manifest refresh | `_root/00_manifest.md` | Update `Last updated` header + row 9 line count (697 → new line count) + footer cumulative recount via `wc -l _root/*.md _root/CONTRACTS.md` + sum. Verify arithmetic. |
| README touch (if Wave 3.5 row needs status) | `_meta/stage4_prompts/README.md` | If the README carries Stage 4.2 status row, update it. (Verify file structure first; do NOT invent rows.) |
| Pricing Migration root README (if applicable) | `Pricing Migration/00_README.md` | Per Stage 4.1 closeout precedent — verify whether the program-level README carries Stage 4 progress section; if so, refresh. Otherwise skip. |

**Verification**: after edits land, run `wc -l _root/*.md _root/CONTRACTS.md` + reconcile against `_root/00_manifest.md §2` rows + `_root/00_manifest.md §2` footer. Manifest-hygiene = source of truth. If arithmetic mismatches, fix manifest before stamping `cohort iter 3 CLOSED`.

### Action 3 — Self-audit of recent work (operator's elite-and-no-drift directive)

Per operator's Amendment-5 directive: **"have it self audit what we've done to spot any fixes that also need to be corrected (ie drift, overlapping instructions, contradictions in instructions, unnecessary language, etc) without being lazy and still elite."**

**The 12 pre-populated drift findings live at Appendix B.6 below.** Read them first. For each finding:

1. **Verify** the finding by reading the cited source file + lines.
2. **Classify** as `definitely_fix` (clear drift / contradiction; cost of leaving = downstream rework) / `consider_fix` (style / hygiene; arguable) / `leave_alone` (planning-agent over-flagged; spec is fine as-is).
3. **Extend** the list with any new findings YOU spot during verification. The 12 are a starting set, not exhaustive.

**Surface the full extended list via `AskQuestion`** with one bundled decision per finding (3 options each: definitely_fix / consider_fix / leave_alone). Operator stamps; you apply approved fixes via source-fix-at-source protocol (`_root/CONTRACTS.md §3`); changelog entry per fix batch.

**Time-box this audit to ONE session** (do not loop indefinitely on drift). If you spot more than ~15 findings during verification, that's a signal that a separate hygiene-pass session is warranted — surface to operator: continue this session OR defer to dedicated hygiene pass.

### Action 4 — `bri` re-paste-run decision (post cohort iter 3 closeout + audit)

`bri` cohort iter 2 was DEFERRED 2026-05-26 per operator-stamped `apply_source_fix_only_no_bri`. The CL-026 + CL-023 + CL-027 source-fixes have all landed since; bri is now technically clean to draft as a TBI-primary + IUR-secondary expansion-shape Format B brief routing through the post-CL-026 `_root/05 §2.3.2` sub-block. **Surface decision via `AskQuestion`**:

- Option A — **Re-run `bri` as cohort iter 4** (refresh `_paste-ready/stage_4_2__bri.md` to v2 documenting CL-026 + CL-023 + CL-027 source-fix sequence; paste-run; audit; close). Quick win to lock in the post-CL-026 TBI+IUR-secondary expansion pattern as a production proof.
- Option B — **Skip `bri` for now; proceed to Stage 4.3** (CEO Letter prompt authoring + first CEO Letter production proof). `bri` enters the bulk-production cohort post-proof-gate.
- Option C — **Defer to operator's discretion at Stage 4.6 bulk-production-gate decision** (no proof needed for `bri` specifically; pattern coverage already exists via cci's URN-primary + sca's URN+IUR-secondary).

Operator stamps; proceed.

### Action 5 — Stage 4.3 (CEO Letter) prompt authoring + production proof

Pattern-inherit from `stage_4_2__format-b__per-account-drafter.md` (697 lines; APPROVED). Target: 400–650 lines + Appendix A.1–A.12 verbatim Step 1 + 8-step canonical skeleton per A.11.

**Per-format adjustments for CEO Letter** (vs Format B):

- Step 3 routing dispatch: CEO Letter 6-step trace per `_root/06 §2` (`status filter → decrease → entity → annual → health → delta tier`); CEO Letter routes at delta-tier ≥ `[CEO_TIER_THRESHOLD]` per `_root/06 §3.4` OR `_root/06 §1.5` CEO-Pre-Call → Format B variant (verify variant in candidate's v6.2 row before routing).
- Step 5 brief assembly: references `ceo-letter-notices/_brief-template.md` (366 lines) + `_root/05 §N.3` CEO Letter canonical block (vs §N.2 Format B). **CL-024 strict + paste-verification protocol is especially load-bearing here** — CEO Letter brief has 3-location date parity contract operator-stamped at Stage 3.3 review pass (brief close + brief routing block + delivery-email routing block); paste-verification must surface any date drift.
- Step 6 delivery email: references `ceo-letter-notices/_delivery-email-template.md` (162 lines) + Section 2 routing block per `_root/07 §7.5` CEO Letter column. **CEO Letter delivery email is CEO-from-CEO voice register** per `_root/04 §1.1` + `§4.15.1` CEO-delivered fork — verify drafter prompt locks the voice in Step 1.

**Production proof candidate selection** via `AskQuestion`: filter v6.2 for `comm_action ∈ {ceo-letter, ceo-pre-call-then-format-b}`; URN OR TBI primary (cleanest precedent); NO reconciliation flag; non-Annual; Tailwind or Core segment; surface 2–3 candidates with 6-step routing trace per candidate; operator picks.

Pattern-inherit `_paste-ready/stage_4_2__cci.md` (841 lines) structure for the paste-ready file. CL-026 / CL-023 / CL-027 lessons documented in pre-flight observations (mutual exclusivity at §2.1.2 / §2.1.3 + URN+IUR-secondary direction-shape routing per CL-027 = same lessons apply to CEO Letter side via `§2.1.3`).

### Action 6 — Stage 4.4 (Good News) prompt authoring + production proof

Pattern-inherit from Stage 4.3 (which inherits from 4.2 which inherits from 4.1). Target: 400–650 lines. Same 8-step skeleton + Appendix A.1–A.12 verbatim.

**Per-format adjustments for Good News** (vs CEO Letter / Format B / Format A):

- Decrease-side driver block — references `_root/05 §3` (3 decrease drivers: `module_compression`, `unrealized_committed_value`, `regional_adjustment`) NOT `_root/05 §2` (increase-side). Per `_root/05 §3.1`–`§3.3`.
- NO formal-notice line per `_root/04 §4.12` "immediately after each close, except Good News" — operator-stamped Stage 3.1 review pass.
- Operator-led close per `good-news-notices/_brief-template.md` Section 6 + `_root/04 §4.12` Good News variant.
- 2026 consolidated-framing variant per `_root/04 §3.1` operator-stamped Stage 3.4 closeout amendment 2026-05-26 (5 forbidden-framing rows specifically for Good News).
- Annual-cohort `renewal_date` v6.2 column gap per CL-015 ledger annotation: if production proof candidate is Annual-cohort, surface column gap to operator BEFORE drafter paste-run (3 options per Stage 4.1 closeout note in §3 CL-NNN table).

**Production proof candidate selection** via `AskQuestion`: filter v6.2 for `comm_action = good-news`; module_compression OR unrealized_committed_value primary (cleanest precedent); non-Annual preferred (defer Annual until renewal_date gap is operator-stamped resolved); surface 2–3 candidates; operator picks.

### Action 7 — Stage 4.5 (entity-packet parent letter) prompt authoring + production proof

**Stage 4.5 sub-structure operator-stamped Q8 2026-05-26** (Stage 4 prep): ONE drafter prompt for parent-letter artifact + orchestration playbook already filed in `_meta/stage4_account_ledger.md §Entity-packet orchestration playbook` for per-child notice dispatch (per-child notices route through Stage 4.1 / 4.2 / 4.3 / 4.4 per-format prompts). NOT multiple sub-prompts.

Pattern-inherit from Stage 4.4 → 4.3 → 4.2 → 4.1. Target: 450–700 lines (entity-packet has more conditional complexity — voice-fork by `delivery_owner` CEO vs Kylor + 48-hour Day-0 → Day-1-2 sequencing).

**Per-format adjustments for entity packets** (vs all standalone formats):

- Scope = ONE entity (`entity_ord_id` parameter, not `ord_id`); references `_master-entity-data-v6.2.csv` (15 lines) as canonical data source (NOT `_master-account-data-v6.2.csv`).
- Voice fork by `delivery_owner` per `_root/04 §4.15.1` (CEO-delivered + Kylor-delivered HoCS variants); voice-fork inversion = automatic fail.
- Default-only pricing posture per `_root/04 §4.15.5` (per-brand mechanics restraint).
- 48-hour Day-0 (parent letter) → Day-1-2 (per-child notices) sequencing per `_root/04 §4.15.6`.
- Cross-format CSM-role note ("CSM-sent" role-marker filled by Kylor in HoCS role across all 5 templates) per Stage 3.5 prep operator stamp.
- 12 entity-packet QB-NNN blockers per `_root/08 §10` (QB-127 through QB-138) added at Stage 4 prep Source-fix Session B 2026-05-26.

**Production proof candidate selection** via `AskQuestion`: filter `_master-entity-data-v6.2.csv` for `migration_status = pending` AND `parent_entity = TRUE`; surface 2–3 entities; operator picks. (Note: the orchestration playbook in `_meta/stage4_account_ledger.md` documents the per-entity playbook — read it before authoring the prompt.)

### Action 8 — Production proof gate (post all 5 format proofs APPROVED)

After Stages 4.1 + 4.2 + 4.3 + 4.4 + 4.5 each have ≥1 APPROVED production proof: surface bulk-production-gate decision via `AskQuestion`:

- Option A — Proceed with bulk production (remaining ~80 accounts paste-run under format-routed prompts; per-account ledger rows logged; per-account changelog entries only if a structural issue surfaces).
- Option B — Run additional proofs per format first (e.g. Format B 2nd proof to cover the TBI-primary + IUR-secondary expansion-direction pattern — bri or one of the 8 CL-023 cluster accounts).
- Option C — Stage the bulk production by cohort (June / July / Deferred per `_root/02 §5`).

Operator stamps; proceed.

### Action 9 — Stage 4 closeout

After bulk production complete + all per-account artifacts in their format folders + ledger fully populated: optionally author `_meta/stage4_prompts/STAGE_4_PLANNING_HANDOFF_TO_STAGE_5.md` if Stage 5 (post-migration / phase 6 cohort execution per `_root/02 §5`) requires a planning-agent handoff. Otherwise, Stage 4 closes at production proof gate + bulk production + ledger fully populated.

---

**Do not start any work in this sequence until the operator approves your §8 handoff confirmation block.** Stage 4 prep candidates are ALL CLOSED — do NOT re-surface them via `AskQuestion`. The Amendment-5 catalyst session resolutions (CL-026 / CL-023 / CL-027) are CLOSED at source — do NOT re-open them via `AskQuestion` unless the self-audit in Action 3 surfaces a verifiable contradiction (which is the entire point of Action 3 — but the bar is "verifiable contradiction in the source," not "I would have written this differently").

---

## §10. Closing reminder

The architecture you are inheriting is operator-stamped strict on path-reference contract, strict on strict-placeholder precedent, strict on manifest-echo contract, strict on conformance-block format, strict on source-fix-at-source. Five Stage 3.X waves landed without drift because every fresh agent and every planning agent before you operated under these constraints absolutely.

You are the steward of those constraints through all of Stage 4 — Phase 4-prep (5 drafter prompts) + Phase 4-production (per-account loop) + production proof gate + any source-fixes that surface along the way. The path-reference inversion (concept #8) is the only new architectural constraint at Stage 4; the rest are inheritance from Stage 3.

**The operator (CEO) is the only stamping authority.** When in doubt, ask via `AskQuestion`. When a `_root/` rule is ambiguous, flag and escalate per `_root/CONTRACTS.md §2`. When a closeout produces an unexpected manifest-date mismatch, flag (QB-125). When a per-account proof conformance block surfaces a gap you cannot resolve from the `stage_4_X` prompt's deviation allowance, flag.

**Asking is cheap. Inventing is the drift vector.** The forbidden-moves list in §7 enumerates the most common drift entry points at Stage 4 — re-read them whenever you're uncertain whether an action is in-scope.

**Welcome to Stage 4.** Produce the handoff confirmation block now and await operator review before proceeding.

---

---

# Appendix A — Stage 4 drafter-prompt design constraints (preserve verbatim in every `stage_4_X` you author)

These 12 constraints govern every `stage_4_X` drafter prompt. Embed them in the prompt's Step 1 or Step 2 verbatim — **NOT paraphrased**. They are the strict-placeholder precedent applied at drafter-prompt scope. Operator-stamped 2026-05-26 (Stage 4 prep pass — operator design constraints baked into the planning-agent handoff so the fresh Stage 4 planning agent does not need a separate addendum).

If you find yourself paraphrasing these constraints in a `stage_4_X` prompt, STOP. Reference them by pointer to this Appendix A, or paste them character-for-character.

---

### A.1. Name the job correctly (opening line of every `stage_4_X` prompt)

Stage 4 drafters are **per-account pricing migration notice drafters** for SuperCat's 2026 book normalization — one brief + one delivery email wrapper for **one** wholesaler principal per session.

**Explicitly NOT**: SaaS renewal / auto-renew / subscription uplift writers; CRM sequence or campaign authors; contract negotiators or procurement responders; template builders (that was Stage 3).

Archived `_fresh-agent-prompt.md` files used "pricing migration communications specialist" and batched 3 accounts — **keep the domain, drop the batching**, anchor to `_root/` + rebuilt Stage 3 templates.

---

### A.2. Lock audience and relationship register (`_root/04 §1`)

Every `stage_4_X` drafter prompt restates the audience-register table:

| Dimension | This program | SaaS-renewal drift to forbid |
|---|---|---|
| Reader | CFO / owner / principal of a furniture / lighting / decor wholesaler | Procurement, IT buyer, "platform admin" |
| Relationship | Vendor-to-principal or CEO-to-CEO (CEO Letter) | Service-rep-to-buyer, CSM check-in |
| Register | Declarative, empathetic on impact, firm on architecture | Cheerful renewal, "excited to partner," soft upsell |
| What they're evaluating | A specific invoice change with a mechanical explanation | Subscription tier change or contract term sheet |

One line in each prompt: *"Write for a principal who runs a wholesale business, not a software buyer renewing a SaaS seat."*

---

### A.3. Lock artifact type — two files, one account, one format

Stage 4 output is always:

- `[ord_id]__[company-slug]__brief.md` — substantive notice (attached PDF in send workflow)
- `[ord_id]__[company-slug]__delivery-email.md` — short wrapper

Per `_root/07 §6` and `_root/01 §5`:

- One account per agent session (production proof gate runs)
- Artifacts over meetings for Tailwind / Core (Format A / B / Good News); meetings reserved for Format B active offer and CEO paths — **not** discovery / QBR language
- Brief = the case; email = the envelope

Forbid in every drafter prompt: "3-email nurture sequence," "renewal reminder cadence," "customer success outreach."

---

### A.4. Routing = hard gate before any prose (`_root/06 §2`)

Every drafter must re-derive format from the **6-step flow**, not memory or `comm_action` alone:

`status filter → decrease → entity → annual → health → delta tier`

Critical stops to encode:

- `parent_entity` child → no standalone brief; entity packet (Stage 4.5 parent letter + per-child notices in their natural formats per `_root/06 §1.6`)
- HOLD → read `post_hold_action`; no draft unless it resolves to sendable format
- Watch / At Risk / Critical → Good News preempted per `_root/06 §4.2`; most routes defer to CEO/CSM first
- CEO Pre-Call → Format B → call happened first; Format B brief + CEO-awareness YES
- Wrong format folder → escalate per `_root/CONTRACTS.md §2`; never "closest format"

Prevents the generic "price increase email" mistake regardless of touch tier.

Routing pre-flight is a **planning-agent responsibility**, not a drafter responsibility. The planning agent runs the 6-step flow against the v6.2 row BEFORE handing the `ord_id` + `stage_4_X` prompt to the drafter. The drafter receives the format pre-determined; the drafter's first verification step is to re-confirm the routing trace in the conformance block.

---

### A.5. Path-reference contract — enforce harder than Stage 3

Stage 3 templates have `[INSERT _root/XX §N.M …]`. Stage 4 is where agents paraphrase.

Require per template section:

1. Open the named `_root/` section
2. Paste character-for-character (drivers `_root/05 §N.M`, closes `_root/04 §4.12`, tiers `_root/03 §1`, etc.)
3. Substitute only `[BRACKETED_TOKENS]` from v6.2 + Postgres per `_root/07 §2 + §4`
4. Zero paraphrase of owned rule prose — including short sentences (strict-placeholder precedent operator-stamped 2026-05-26 Stage 3.1 review pass)

**Allowed drafter-generated prose (narrow)**:

- Relationship lede (Format A / B / CEO Letter) per `_root/04 §4.1 + §4.2` — the relationship-historicity opening that names tenure and cohort
- Good News decrease lede (one sentence, dollar-first; pattern per `good-news-notices/_brief-template.md` Section 3b)
- Minor per-account calibration in delivery-email Sentence 1a — still within format register
- Entity-packet parent letter portfolio acknowledgment (one paragraph per `_root/04 §4.15.2` required-content list; drafter-generated per the §4.15.2 rule — required content specified, exact wording not)

Everything else = fetch-and-paste.

---

### A.6. Migration mechanics vocabulary, not SaaS vocabulary

Point drafters at `migration_driver` from v6.2 + format-specific block in `_root/05` — not "your subscription is increasing."

Explanation = why the number changed under the new architecture (URN / TBI / IUR / MOR / PDC / module compression / etc.).

Forbidden framings (cite `_root/04 §3` table in prompts — do NOT re-list ad hoc):

- "Renewal," "auto-renew," "subscription renewal," "at renewal we're adjusting…"
- "Rate card alignment" without tenure / driver context
- "As part of this refresh" → use "going forward"
- Leading with percentage (`_root/04 §2.1`)
- "We're adjusting your pricing"
- Gift / reward / favor on decreases
- Expansion / Format C in migration notice
- Competitor or peer dollar ranges (CL-003 / CL-004)
- CL-001 forbidden sentence ("no account-specific adjustments")

**Formal-notice line**: paste-only verbatim from `_root/04 §4.12` ("pricing modification under your SuperCat licensing agreement") — not custom contract language.

**Good News**: NO formal-notice line per `_root/04 §4.12` "immediately after each close, except Good News" — do not flatten across formats.

---

### A.7. Data pipeline — kill pre-refactor habits

Stage 4 uses `_root/07` only:

| Source | Role |
|---|---|
| v6.2 CSV (account + entity files) | Authoritative numbers, driver, health, routing |
| Postgres MCP | Live lede stats only |
| Routing CSV (mirror in `_root/06 §2 + §7`) | `comm_action`, `post_hold_action`, HOLD resolution |
| HTML model | Cross-check only; v6.2 wins on conflict |

Hard rules:

- Never read `_archive/` per-account exemplars or old templates (kal / kii / lss v2 — CL-018–021 flag these as drift sources)
- Never read `Migration-Health Artifacts/` templates
- Never invent stats; Postgres fail → `composite_narrative` fallback per `_root/07 §5`
- Lede stat guardrail: output metrics only; never provisioned-vs-active ratios per `_root/04 §4.2`

---

### A.8. Format-specific registers — do not collapse to one "renewal email"

One `stage_4_X` prompt per format folder. Include a "what makes this format different" block:

| Format | Close register | Stage 4 production must enforce |
|---|---|---|
| Format A | Passive "conversation welcome" | No meeting push |
| Format B | Active meeting offer | Migration meeting, not discovery call |
| CEO Letter | Specific calendar date; CEO calls personally | 3-location date parity (brief close, brief routing block, delivery-email routing block) per Stage 3.3 operator stamp 2026-05-26 |
| Good News | No-ask operator-led close | No formal-notice line; "math, not a favor" |
| CEO Pre-Call → Format B | Format B + prior-call acknowledgment | CEO awareness YES; call happened before send |
| Entity packet (parent letter) | Voice fork by `delivery_owner` per `_root/04 §4.15.1` (CEO-delivered + Kylor-delivered HoCS variants) | Default-only pricing posture; 48-hour Day 0 → Day 1–2 sequencing; per-child mechanics restraint |

CEO Letter closes in Format B = hard fail in review. Formal-notice line on Good News = hard fail. Voice-fork inversion at entity packet (CEO-delivered fork rendered for Kylor-delivered entity or vice versa) = hard fail.

---

### A.9. Internal vs client-facing

Per `_root/04 §2.5` and `§2.14`:

- Routing block stays in draft for operator review; **removed before send**
- Health bands, dimension scores, `support_fire`, CEO-awareness flags, billing-entity routing → routing block only (NEVER in client copy)
- "Log in CRM" / cohort tags → NEVER in client copy
- `consolidated_delta` / `consolidation_saving` / `consolidation_saving_pct` (entity packets) → INTERNAL-ONLY per `_root/04 §4.15.5`

---

### A.10. Conformance block = drift audit

End every `stage_4_X` drafter prompt with `_root/00_manifest.md §5` plus per-account additions:

- Manifest echo (files read with last-updated dates)
- QB-NNN results for every applicable check in `_root/08` — by ID, not "looks good"
- Explicit: 0 inlined rule prose paraphrases, 0 archive reads
- Math reconciliation: Before / After / Delta totals vs the v6.2 row (QB-104 + QB-105)
- Format-specific blockers by ID (e.g. QB-086 close-correctness; QB-064 Good News favor framing; QB-085 peer-dollar check; QB-101 internal-routing scrub)
- Routing 6-step trace: each step's evaluation result + terminal format selected
- Postgres-stat fetch: query used + result OR fallback used (per `_root/07 §5`)
- CL-024 strict + paste-verification carry-forward: every owned rule prose paste-quoted verbatim in the conformance block (proves the drafter fetched-and-pasted, not paraphrased)

Review Stage 4 per-account proofs like Stage 3 templates: path-reference clean, format-faithful, no SaaS vocabulary in "helpful examples."

---

### A.11. Prompt structure — mirror Stage 3.3 eight steps

Adapt `_meta/stage3_prompts/stage_3_3__ceo-letter__brief-and-delivery-templates.md` (the gold-standard Stage 3 prompt; 8-step skeleton):

1. Role + single-account scope (`ord_id` parameter; one in / two out / STOP)
2. Required reading (manifest order + format-specific Stage 3 template + format-applicable CL items)
3. Routing verification (`_root/06 §2` 6-step flow re-confirmation against the v6.2 row before drafting)
4. Data load (v6.2 row + Postgres MCP query for lede stat + routing-CSV mirror entry per `_root/06 §2 + §7`)
5. Brief assembly (section-by-section: which `[INSERT _root/XX §N.M]` fires, which conditionals; paste verbatim, substitute bracketed tokens only)
6. Delivery email assembly (wrapper only; mirror brief routing block as subset)
7. Anti-drift discipline (forbidden-phrases pointer to `_root/04 §3`; anti-archive; no exemplars; strict-placeholder precedent)
8. Output + conformance block (per `_root/00_manifest.md §5` + per-account additions per A.10 above)

One prompt per format (+ entity-packet variant after Stage 4.5 sub-structure decision). NOT one mega-prompt.

Target length: 400–550 lines per `stage_4_X`.

---

### A.12. "Do not write like this" contrast pairs (2–3 per drafter prompt)

**Wrong (SaaS renewal)**:

> "As your renewal approaches, we're updating your subscription to reflect current list pricing…"

**Right (migration notice)**:

Relationship-first lede → dollar + effective date → driver block from `_root/05` (verbatim paste) → operations-unchanged sentence (verbatim paste from `_root/04 §4.5`) → roadmap (verbatim paste from `_root/03 §3`) → format-specific close (verbatim paste from `_root/04 §4.12`) → formal-notice line (verbatim paste from `_root/04 §4.12`; except Good News which omits per the §4.12 exception).

**Wrong (CRM)**:

> "Your account health is Strong (VD: 81) and we'd love to schedule a QBR…"

**Right**:

Internal routing block only (Section 2 of the brief; removed before send); client lede uses tenure + eCat-order counts, never health vocabulary.

**Wrong (template builder)**:

> `[INSERT _root/05 §2.1.3 — user_rate_normalization CEO Letter canonical block]`

**Right (production drafter)**:

Verbatim paste of the actual `_root/05 §2.1.3` block content, with `[CURRENT_RATE]` / `[NEW_RATE]` / `[LADDER_BAND]` / `[ANNUAL_DELTA]` tokens substituted from v6.2 + Postgres. The `[INSERT ...]` pointer lives in the Stage 3 template, NOT in the Stage 4 production artifact.

---

**Appendix A is operator-stamped 2026-05-26 (Stage 4 prep — design constraints baked into planning-agent handoff). Revising any of A.1–A.12 requires the rule-change protocol per `_root/CONTRACTS.md §3`.**

---

# Appendix B — Stage 3.5 review-pass lesson: CSV is canonical; rule layer reconciles to CSV

**Operator-stamped 2026-05-26 (Stage 3.5 review pass).**

The Stage 3.5 review pass produced one substantive source-fix amendment: Thesis's `delivery_owner` was classified `Kylor` in the rule layer (`_root/04 §4.15.1` Kylor-delivered fork list + `_root/06 §1.6` enumeration + Stage 3.5 prompt Step 2 table + both new templates' Section 1 entity-count references) while `_master-entity-data-v6.2.csv` row 13 carries `delivery_owner = CEO`. The discrepancy was caught by the Stage 3.5 fresh agent's CL-024 strict + paste-verification protocol — the fresh agent paste-quoted the rule layer verbatim at source, which surfaced the rule-layer drift from CSV ground truth that pointer-only reading would have missed.

**Operator stamp 2026-05-26**: the v6.2 CSVs (`_master-account-data-v6.2.csv` + `_master-entity-data-v6.2.csv`) are canonical for their respective scopes per the dual-canonical architecture stamped at Stage 3.5 prep. **Any rule-layer enumeration claim that disagrees with the CSV reconciles to the CSV**, not the reverse. The rule layer documents the architecture and the routing; the CSV documents the data; rule-layer enumerations of CSV-derived facts must match the CSV.

**Forward propagation to Stage 4**:

1. **Every `stage_4_X` Step 3 (routing verification) explicitly re-derives `delivery_owner` / `migration_driver` / `notice_cohort` / `health_band` from the CSV row at draft time.** Not from any rule-layer enumeration (which may have drifted). The drafter cites the CSV column + row + value in the conformance block; the planning agent re-verifies at review time against the same CSV row.
2. **Routing pre-flight (planning-agent responsibility) reads the CSV row directly** for every routing-relevant field. The 6-step routing flow per `_root/06 §2` operates on CSV values, not on rule-layer narrative.
3. **Cross-format consistency watchdog (§6 of this handoff) extends to rule-layer enumeration drift surfaces.** If multiple per-account proofs disagree with the rule layer on a routing-relevant field, the rule layer is the suspect (per the operator stamp above), not the CSV.
4. **The CL-024 strict + paste-verification discipline propagates to every `stage_4_X` prompt** per Appendix A.10 design constraint. The discipline's design value (catching rule-layer drift that pointer-only reading misses) was validated in Stage 3.5 review pass; preserving the discipline at Stage 4 prevents the same drift from recurring in production drafting.

**What this is NOT**: this is not a 9th architectural concept (the original 8 in `§4` cover the discipline at the architecture level; this Appendix B captures the concrete operational application). This is also not a separate CL item — it operationalizes via the existing CL-024 discipline + the per-account routing-verification step that's already in every `stage_4_X` prompt's Step 3 per Appendix A.4.

**Appendix B is operator-stamped 2026-05-26 (Stage 3.5 review-pass lesson — baked into planning-agent handoff as the canonical articulation of the CSV-canonical operator stamp). Revising the canonical-source claim requires the rule-change protocol per `_root/CONTRACTS.md §3`.**

---

## Appendix B.4 — Stage 4.1 lpf production proof lesson: After-row math is v6.2 modeled-canonical; reconciliation gap → INTERNAL ops cleanup pre-effective-date

**Operator-stamped 2026-05-26 (Stage 4.1 lpf production proof closeout — operator Option (1) discipline stamp; CL-025 RESOLVED at planning-agent layer).**

The Stage 4.1 lpf production proof surfaced a load-bearing architectural question that was not anticipated at Stage 4 prep: when v6.2's `modeled_users` (the canonical input for After-row pricing-table math per `_root/05 §2.1.5`) diverges from the billing-implied enabled count (derived from current invoice math: `current_provided_users + ROUND(current_user_mrr ÷ current_user_rate)`), which canonical value drives the customer-facing After-row?

Cohort-wide sweep run 2026-05-26 (`/tmp/v6_2_reconciliation_sweep.py`) revealed this is a SYSTEMIC v6.2 modeling characteristic, not an lpf edge case:

- **37 of 107 pending accounts (35%)** have material reconciliation gaps per `_root/07 §4.5` thresholds (`|gap_users| > 3 AND |gap_dollars| > $60`)
- **33 of 107 (31%)** would route to a different format (Format A ↔ Format B ↔ CEO Letter, or Good News → increase format) under enabled-canonical After-row math
- **2 accounts (rw, jyc)** would flip from Good News to increase format — the trust-destroying direction
- **6 ABTS accounts (abol, krb, lss, swc, soi, mpc)** cluster: all flip Format A → CEO Letter under enabled-canonical
- **lpf** is a Pattern 1 case (billed=51 > modeled=44; gap=+7 users / +$140) — would flip Format A → Format B under enabled-canonical

**Operator stamp 2026-05-26 — Discipline (1) wins**: v6.2 modeled-canonical wins per existing Appendix B (canonical-data principle); the brief's After-row math = v6.2 `excess_users` × graduated rate per `_root/05 §2.1.5`; reconciliation gap is closed via INTERNAL SuperCat ops cleanup pre-`[EFFECTIVE_DATE]` (disable phantom enabled accounts for Pattern 1 rows; verify operational reality for Pattern 2 rows); brief math stands as v6.2 stamps it; **client copy NEVER mentions "unused users," "phantom accounts," or any user-cleanup language** per `_root/04 §3` audience-discipline. The `_root/04 §4.9` footnote ("billing is based on enabled accounts; user figures above reflect your current enabled count") is made operationally accurate by `[EFFECTIVE_DATE]` because by that date enabled = v6.2 modeled (via ops cleanup).

**Forward propagation to every Stage 4 per-account session**:

1. **Every `stage_4_X` Step 4 (data load / math reconciliation) populates After-row math directly from v6.2 stamped values** — `[NEW_EXCESS]` = v6.2 `excess_users`; `[NEW_USER_CHARGE]` = v6.2 `user_charge`; `[NEW_MRR]` = v6.2 `new_total_mrr`. The drafter does NOT recompute these from billing math, trailing-avg, or `enabled_users`. Recomputing violates Appendix B canonicality + is reserved for v6.2 re-stamps (operator action only per `_root/CONTRACTS.md §3`).
2. **Every `stage_4_X` Step 4 computes the reconciliation flag** per `_root/07 §4.5`: derive `implied_billed_excess = ROUND(current_user_mrr ÷ current_user_rate)`; derive `narrative_excess = trailing_avg_users − current_provided_users`; if `|gap| > 3 OR gap × current_user_rate > $60`, the brief's routing block carries the `⚠️ USER BILLING RECONCILIATION NEEDED` line per `_root/07 §7`. The flag is internal-routing-block content (removed before send); the customer-facing brief math is unaffected.
3. **Planning-agent pre-flight + per-account audit verifies the flagged account has a row in `_meta/v6_2_reconciliation_log.md`** — if pre-existing (from the 2026-05-26 cohort sweep), the planning agent records `drafter_session_id` cross-reference in the tracker row's `notes` column; if newly-flagged (post-sweep account), the planning agent appends a new row at session approval time with `ops_status = pending`.
4. **CSM/Ops team owns the per-account ops cleanup workstream**: for each flagged row in `_meta/v6_2_reconciliation_log.md`, the `ops_owner` (typically `delivery_owner` from v6.2) verifies the gap with the customer's SuperCat admin (or via Postgres login activity), disables phantom enabled accounts (Pattern 1) or updates v6.2 modeled (Pattern 2), updates `ops_status` accordingly. Pre-bulk-production gate verifies all flagged rows have `ops_status ∈ {in-progress, cleared, re-modeled, escalated}` (not `pending`).
5. **`_master-account-data-v6.2.csv` `enabled_users` column at position 15** (added 2026-05-26 at Stage 4.1 lpf closeout; populated from billing math for the 2026-05-26 v6.2 snapshot; ERP-source population path documented for future v6.2 regenerations) — drafters use this column to surface the reconciliation flag without re-deriving billing math themselves; planning-agent pre-flight uses it for routing-trace evidence.
6. **For accounts where ops cleanup cannot complete by `[EFFECTIVE_DATE]`** — operator escalates per `_root/CONTRACTS.md §2`; may re-stamp v6.2 `modeled_users` to the operationally-correct value; the account then re-routes per `_root/06` 6-step flow under the updated v6.2 values; brief re-versions as `__v2` per `_root/07 §6`.

**What this Appendix B.4 is NOT**: not a new architectural concept (the original 8 in `§4` cover the architecture; Appendix B.4 is operational application). Not a separate CL item — it codifies the CL-025 discipline stamp (already RESOLVED 2026-05-26 at planning-agent layer per source-fix landing). Not a re-version of Appendix B — it extends Appendix B's canonical-data principle to the specific case of v6.2 modeled_users vs billing-implied enabled count.

**Appendix B.4 is operator-stamped 2026-05-26 (Stage 4.1 lpf production proof closeout — Discipline (1) stamp baked into planning-agent handoff as the canonical articulation of After-row reconciliation discipline). Revising the discipline requires the rule-change protocol per `_root/CONTRACTS.md §3` + a fresh cohort sweep against any v6.2 re-stamp.**

---

## Appendix B.5 — Stage 4.1 lpf production proof operational lessons (planning-agent discipline)

**Operator-stamped 2026-05-26 (Stage 4.1 lpf production proof closeout).** Two procedural lessons surfaced during the Stage 4.1 lpf audit propagate to every Stage 4.X session.

### B.5.1 — Routing-CSV column parse discipline (planning-agent pre-flight enforcement)

Every `_paste-ready/stage_4_X__<ord_id>.md` planning-agent annotation block parses `migration_comm_tiers_2026-05-19.csv` via `csv.DictReader` (or equivalent header-position mapping by row 1 column names). **Never** by visual column inspection.

The Stage 4.1 lpf paste-ready had `flags` and `nuances` columns reversed under visual inspection (annotation reported `flags = blank` + `nuances = "INSIGHTS-LAYER"`; CSV ground truth was `flags = "INSIGHTS-LAYER"` + `nuances = ""`). The fresh agent's audit caught it via `csv.DictReader` re-derivation per Step 3 / Step 4 of the per-account drafter prompt. Routing-flow outcome was unchanged (Format A either way), but the planning-agent pre-flight had passed a structurally incorrect column attribution into the paste-ready file. The fresh agent acted as the audit catch — but the discipline is for the planning agent to never need that catch.

**Forward rule**: every paste-ready annotation block carries a one-line `parsed via csv.DictReader on row N at YYYY-MM-DD HH:MM` attestation. The attestation is mechanically verifiable (operator or peer planning agent can re-run `csv.DictReader` against the cited row and reconcile). Planning-agent pre-flight is the prevention; fresh-agent audit per Step 3/4 is the catch. Both layers stay in place.

### B.5.2 — Appendix-B-canonicality-check before recommending a pivot (planning-agent audit discipline)

When a per-account audit surfaces what looks like a math integrity gap, the planning agent MUST first verify whether the disputed value is v6.2-stamped (Appendix B canonical) BEFORE recommending a routing or math pivot to the operator.

The Stage 4.1 lpf audit briefly stamped Path (b) Format-B re-route after the fresh agent's conformance block surfaced a billing-implied `[NEW_MRR]` of $2,567 (vs the brief's $2,395). The Path (b) stamp assumed `[NEW_MRR]` was drafter-computed and therefore mutable per-account; the actual v6.2 `new_total_mrr` was $2,395 modeled-canonical, which made the proposed re-route an Appendix-B violation (Appendix B prohibits per-account override of v6.2-stamped values). The Path (b) stamp was rolled back; the actual resolution was source-layer (Discipline 1 stamp at `_root/07 §4.5` + `_root/05 §2.1.5` + `_root/04 §4.9`; codified at Appendix B.4 above), not per-account.

**Forward rule**: every Stage 4.X audit that proposes a routing or math pivot includes an explicit "Appendix B canonicality check" line in the surfacing — `did v6.2 stamp the disputed value? yes → source-fix path (rule-layer; CL-NNN entry per CONTRACTS §3); no → per-account re-route path (data-layer; per-account ledger note)`. Per-account pivots are reserved for true per-account drift (e.g. an `ord_id` whose v6.2 row carries a flag value that contradicts the routing CSV mirror for that same row). Rule-layer ambiguity surfaces as a CL-class item; never as a per-account pivot.

### What Appendix B.5 is NOT

Not new architectural concepts (the original 8 in `§4` cover the architecture). Not new CL items (both lessons operator-stamped 2026-05-26 at Stage 4.1 closeout; no CL-NNN filed because no source-fix is required — the discipline is planning-agent procedural). Not an override to Appendix A or Appendix B — operationalizes existing constraints (Appendix A.4 routing-as-hard-gate + Appendix B CSV canonical + CL-024 strict + paste-verification) at the planning-agent pre-flight + audit layers.

**Appendix B.5 is operator-stamped 2026-05-26 (Stage 4.1 lpf production proof closeout — planning-agent procedural discipline). Revising requires the rule-change protocol per `_root/CONTRACTS.md §3`.**

---

## Appendix B.6 — Stage 4.2 lessons + drift watchlist (Amendment 5)

**Operator-stamped 2026-05-26 (Amendment 5 — Stage 4.2 mid-cohort handoff to finish-line planning agent).** Three lessons + twelve drift findings carry forward from the Amendment-5 catalyst session (CL-026 + CL-023 + CL-027 joint-resolution sequence + sca v2 paste-ready refresh).

### B.6.1 — Lessons from Stage 4.2 hard-stops + joint resolutions

**Lesson 1 — Drafter hard-stops are load-bearing audit surfaces, not failures**

Three Stage 4 drafter hard-stops to date: Stage 3.5 Thesis (rule-layer/CSV `delivery_owner` drift) + Stage 4.2 bri (v6.2 `migration_driver` IUR vs field signature expansion) + Stage 4.2 sca v1 (`_root/05 §2.1.2` URN canonical sub-block reduction-direction gap). Each hard-stop was a fresh-agent invocation of `_root/CONTRACTS.md §2` that surfaced source-layer drift the planning agent had not pre-spotted. **Pattern**: the CL-024 paste-verification protocol is the catch mechanism; fresh agents reading rule-layer prose verbatim surface drift that pointer-only pre-flight misses. Planning agent's job at hard-stop = (a) verify drafter's findings via direct source-read + `csv.DictReader` re-derivation; (b) enumerate scope of the gap across the full cohort (not just the surfacing account); (c) propose resolution options via `AskQuestion`; (d) apply operator-stamped source-fix + propagate; (e) refresh affected paste-readys + document self-corrections transparently. Hard-stop velocity is rising (1 → 2 → 3 in Stage 3.5 → 4.2 iter 2 → 4.2 iter 3) because pattern-inheritance compounds: each new iter inherits more compound complexity (URN+IUR-secondary direction-shape was inert during Stage 4.1 Format A and Stage 4.2 cci because cci's URN is standalone with no IUR-secondary). **Expect Stage 4.3 / 4.4 / 4.5 to surface additional hard-stops**; budget time accordingly. The architecture is working as designed.

**Lesson 2 — Joint resolutions can have scope-gaps**

CL-026 + CL-023 jointly RESOLVED 2026-05-26 (Stage 4.2 iter 2 hard-stop on `bri`) at `_root/05 §2.4.1` semantic clarification — but the resolution was TBI-side-only scope. The URN-side analog (URN-primary + IUR-secondary with reduction-direction at `_root/05 §2.1.2`) was not inspected at the time of CL-026 / CL-023 stamp + landing. CL-027 (Stage 4.2 iter 3 hard-stop on `sca`) surfaced the URN-side analog gap two iterations later. **Forward rule**: when a CL-NNN resolution touches a semantic that crosses driver-axes (TBI / URN / MOR / ABTS / IUR / PDC / ADR), enumerate the symmetric cases across ALL driver-axes BEFORE stamping the resolution — even if only one axis has a known failing case. Cost of asking "is this gap present in the URN-side / MOR-side / ABTS-side too?" at resolution time is 5 minutes of `csv.DictReader` enumeration; cost of missing it is one new hard-stop + one new CL-NNN entry + one new paste-ready refresh + one new audit cycle.

**Lesson 3 — Planning-agent self-corrections must be transparent**

The Stage 4.2 sca v1 paste-ready carried a wrong pre-flight observation 2 (claimed `_root/05 §2.1.7` sub-block "describes legacy-allotment-reducing-to-new-tier-standard"; actual pre-CL-027 §2.1.7 routed URN+IUR-secondary to §2.1.2's EXPANSION-only sub-block, which contradicts the observation). The drafter caught it via CL-024 paste-verification + direct source-read. The sca v2 refresh **documented the v1 planning-agent error transparently** in the v2 stamp block + corrected pre-flight observations 2 + 3. **Forward rule**: when refreshing a paste-ready post-source-fix, document any planning-agent observations that were wrong in v1 with a "Planning-agent self-correction" stamp block; cite the wrong observation + the corrected observation + the source-of-truth that proves the correction. Transparency keeps the next planning agent (you) from inheriting silent drift.

### B.6.2 — Drift watchlist (12 pre-populated findings; verify + extend + surface via AskQuestion per §9 Action 3)

**Methodology**: each finding cites (a) the source file + line range where the suspected drift lives, (b) the suspected drift type (contradiction / overlap / unnecessary language / staleness / convention-inconsistency), (c) the prior planning agent's tentative classification. You verify by reading the source + cross-checking against authoritative sources (Appendix B canonicality + manifest line counts + audit-baseline files), then extend with any new findings YOU spot, then surface the full list via `AskQuestion`.

| # | Source location | Type | Prior agent's note | Verify by |
|---|---|---|---|---|
| 1 | `_root/05_driver_taxonomy.md §2.4.1` (post-CL-027 edit) — paragraph enumerating "TBI primary + IUR-secondary (9 accounts)" | Conversational debug language | Includes parenthetical "Wait — `bcf` was re-stamped TBI→URN in the next iteration of joint resolution; not in this TBI cohort." This reads as inline debugging not crisp source rule. TBI+IUR cohort = `bri + 8 CL-023 cluster` = 9 accounts (no `bcf`). The "Wait —" parenthetical should be cut + enumeration cleaned. | Read `_root/05 §2.4.1` post-CL-027 edit + verify cohort enumeration against `_master-account-data-v6.2.csv` post-stamp |
| 2 | `_root/05_driver_taxonomy.md §2.4.7` (post-CL-027 edit) — cross-reference paragraph | Conversational debug language | Same "Wait —" debug-language artifact as Finding 1 (parallel paragraph). Same cleanup needed. | Read `_root/05 §2.4.7` post-CL-027 edit |
| 3 | `_meta/stage3_cleanup.md` CL-027 RESOLVED entry | Conversational debug language | Similar "Wait — `bcf` was re-stamped" inline-debug language; planning-agent state-of-mind leak into tracker. Should be cut + rewritten as source-rule prose. | Read CL-027 entry in `_meta/stage3_cleanup.md` |
| 4 | `_root/00_manifest.md` row 5 + row 9 cell annotations | Bloat (cell annotations defeat manifest's "one-line summary" purpose) | Each cell now carries 3,000+ words of cumulative annotation (every CL-NNN that touched the doc). The §2 manifest table is supposed to be a one-line-per-row index. Consider: (a) move detailed annotations to `_root/09_changelog.md` (canonical narrative-history location); (b) keep §2 cells as one-line summaries with `→ see _root/09 YYYY-MM-DD entry` pointers. | Read `_root/00 §2` row 5 + row 9; compare cell length to original Stage 2 convention |
| 5 | `_root/00_manifest.md` `Last updated` header | Bloat (header ~1,500+ words) | Each Stage 4.X edit appended a paragraph to the header. Header is supposed to be a one-paragraph summary of the latest change. Convention drift across Stages 3.X + 4.X has produced a chronological narrative. Consider pruning to latest 2–3 changes only; older paragraphs migrate to `_root/09` (canonical narrative-history location). | Read `_root/00` `Last updated` header (top of file); compare to Stage 2 convention |
| 6 | `_meta/stage4_prompts/_paste-ready/stage_4_2__*.md` files (3 paste-readys to date: lpf 735 + cci 841 + sca 886) | Bloat (paste-readys now bigger than the drafter prompt itself at 697) | Paste-readys were originally thin wrappers (substitute `[ORD_ID]`, add 1-page annotation block). Now they're 800+ lines each due to compounding pre-flight observations + audit lessons + v1→v2 stamps. Consider: (a) does the paste-ready need to carry all the compound history? (b) can older lessons collapse into an `_meta/stage4_prompts/_paste-ready/_lessons-learned.md` reference doc + the paste-ready cites by pointer? | Read sca v2 paste-ready + cci paste-ready; compare structure to lpf paste-ready Stage 4.1 closeout baseline |
| 7 | `_meta/stage3_cleanup.md` CL-001 / CL-003 / CL-004 / CL-005 | Staleness | These were filed early in Stage 2 + listed as "Stage-4 exemplar-regen items." Stage 4 production is replacing the v2 exemplars one-by-one. Verify status: are these still active CLs or should they be marked RESOLVED-per-account-as-Stage-4-production-replaces-them? | Read each CL entry + cross-reference with Stage 4 ledger to count how many v2 exemplars have been replaced |
| 8 | `_root/05_driver_taxonomy.md §2.1.2` mutual-exclusivity rule (codified at CL-027) | Convention inconsistency | CL-027 codified an EXPLICIT mutual-exclusivity rule for §2.1.2's two parenthetical-as-gate sub-blocks ("an account fires at most one of {expansion-direction, reduction-direction}"). §2.1.3 (CEO Letter URN canonical) has the SAME convention but IMPLICIT (per CL-012 RESOLVED 2026-05-26). Should §2.1.3 get the same explicit codification? Should other markers across §2.X (TBI / MOR / ABTS / etc.) be audited for parenthetical-as-gate convention + explicit codification? | Read §2.1.2 + §2.1.3 + §2.3.2 + §2.6.2 (each Format B canonical block) + look for parenthetical-as-gate patterns |
| 9 | `_root/05_driver_taxonomy.md §4` weaving matrix — "IUR (none)" row count "21" | Staleness | IUR-primary count post-CL-026 is 10 (bri re-stamped IUR→TBI; was 11 pre-stamp). But §4 matrix's "IUR (none)" row shows "21" — that's not matching IUR-primary count at all. Either (a) "21" represents a different concept (informational annotation) that should be re-labeled or (b) it's a pre-Stage-4 stale number that needs updating. **Investigate**: enumerate v6.2's IUR-primary accounts via `csv.DictReader`; reconcile to §4 row count. | Read §4 matrix + count IUR-primary in `_master-account-data-v6.2.csv` |
| 10 | `_root/05_driver_taxonomy.md §4` weaving matrix aggregate occurrence | Arithmetic-doesn't-reconcile concern | Post-CL-027 footer states "Aggregate v6.2-exhibited primary-secondary occurrences: 83" but v6.2 has 107 pending accounts. The 24-account gap must reconcile somewhere — likely accounts with primary-only-no-secondary (PDC, ABTS-no-secondary, etc.) that are enumerated in their respective `(none)` rows. Verify the 83 + 24 = 107 arithmetic reconciles + matches the v6.2 row count. | Sum §4 row counts + reconcile to 107 pending pool; if gap, identify which categories aren't enumerated |
| 11 | `_meta/v6_2_reconciliation_log.md` — verify no CL-027-related updates needed | Verification (not yet a drift finding) | CL-027 was rule-layer-only (no v6.2 re-stamps). The reconciliation tracker should be unaffected. Verify: read the tracker post-CL-027 + confirm bri's driver-annotation update (IUR → TBI) from CL-026 landed but no new flagged rows from CL-027. | Read `_meta/v6_2_reconciliation_log.md` + cross-check the 37 flagged rows |
| 12 | `_master-account-data-v6.2.csv` audit baseline 91.6% post-CL-026 + CL-023 + CL-027 | Verification (not yet a drift finding) | CL-027 was rule-layer-only; should not have changed the audit baseline. Confirm baseline still 91.6% (98 pass / 8 flag / 1 fail). Cite `_archive/2026-05-26__pre-cl-026/v6_2_driver_signature_audit.py` (or equivalent) re-run output. | Re-run audit script against post-CL-027 v6.2 + reconcile to expected baseline |

### B.6.3 — Audit-discipline guardrails

**For Action 3 (self-audit pass)**:

1. **Time-box** to ONE session. The audit is calibration, not a complete-the-program exercise. If you spot >15 findings during verification, surface to operator: continue this session OR defer to dedicated hygiene-pass session.
2. **Verify before classifying**. A finding only counts if you've read the source + cross-checked the suspected drift. "I think this might be drifty" without source-citation is not actionable.
3. **Don't introduce new drift via the audit itself**. The audit's purpose is to clean up; if your proposed cleanup adds 200 lines of clarification, the cure is worse than the disease. Cleanups should be SUBTRACTIVE (trim language) or REPLACING (point to authoritative source instead of restating), not ADDITIVE.
4. **Hierarchical fix-priority**: contradictions in source rule prose > stale counts/numbers > conversational debug language > bloat. Fix contradictions first; numbers second; conversational artifacts third; bloat last (bloat is style, not correctness).
5. **Operator-stamps the trim, not you**. Surface findings via `AskQuestion` with per-finding triage; do NOT silently edit. Trim discipline is the operator's stamp.

### B.6.4 — What Appendix B.6 is NOT

Not new architectural concepts (the original 8 in `§4` cover the architecture). Not new operator-stamped disciplines (Appendix A + B + B.4 + B.5 are the canonical disciplines). Not a license for unbounded refactoring (the operator's drift concern is about over-complication, not about ground-up redesign — Action 3 is calibration not redesign). The 12 drift findings are a starting set; they are not exhaustive nor are they all guaranteed to be real (Finding 9 + Finding 10 + Finding 11 + Finding 12 are flagged as "verify, may or may not be drift"). The other 8 (Findings 1–8) are higher-confidence; the prior planning agent saw them but did not act on them within the Amendment-5 catalyst session.

**Appendix B.6 is operator-stamped 2026-05-26 (Amendment 5 — Stage 4.2 mid-cohort handoff to finish-line planning agent). Revising requires the rule-change protocol per `_root/CONTRACTS.md §3`. The drift watchlist (B.6.2) is open-ended; you are expected to extend it, not just verify the 12 starting items.**
