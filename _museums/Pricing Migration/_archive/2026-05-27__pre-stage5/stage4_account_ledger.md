# Stage 4 — Per-Account Drafting Ledger

> **What this ledger owns**: the authoritative per-account tracker for Phase 4-production. One row per account that progresses through the `stage_4_X__<format>__per-account-drafter.md` per-account session loop. Maintained by the planning agent at review-pass approval; never written by per-account drafter agents.
>
> **What this ledger DOES NOT own**: the per-account artifacts themselves (those live in `<format>-notices/<ord_id>__<slug>__brief.md` + `<format>-notices/<ord_id>__<slug>__delivery-email.md`); the routing CSV itself (canonical at `Pricing Migration/migration_comm_tiers_2026-05-19.csv`); v6.2 account-level data (canonical at `Pricing Migration/_master-account-data-v6.2.csv` + `_master-entity-data-v6.2.csv`); rule-layer state (canonical at `_root/`); CL-NNN tracker (canonical at `_meta/stage3_cleanup.md`).
>
> **Last updated**: 2026-05-26 (Stage 4.2 sca cohort iter 3 closeout — sca row appended under Format B section APPROVED 2026-05-26 as first production proof of post-CL-027 `_root/05 §2.1.2` line 101 reduction-direction sub-block; CL-028 RESOLVED in-session via `_root/07 §4.5` OR-prose → AND-prose tightening per operator stamp `resolve_now_AND_canonical`; 3-consecutive-omission pattern locked for §3m "How This Compares" on URN-primary Format B accounts — Stage 4 template-level convention candidate to surface at Action 3 self-audit. Prior 2026-05-26 entries: Stage 4.2 cci cohort iter 1 closeout — cci row appended under Format B section APPROVED 2026-05-26 as first Format B production proof (clean closeout; no source-fix; no rule changes; Stage 4.2 Format B drafter prompt + paste-ready operator-stamped + production-proven); Stage 4.1 lpf production proof closeout — lpf row appended under Format A section APPROVED 2026-05-26 under operator-stamped Discipline (1) at CL-025 RESOLVED; created at Stage 4 prep by Stage 4 planning agent.)
> **Owner**: CEO (via planning agent — planning agent writes rows; operator stamps the `operator_stamp_date` column at review-pass approval)
> **Primary sources**: `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` §9 step 3 (schema operator-stamped at handoff drafting 2026-05-26); `_meta/stage4_prompts/README.md` (per-account session review protocol). Per-account row substance derived from the per-account fresh-agent session's conformance block + planning-agent review-pass output.
> **Supersedes**: nothing — this is a new artifact at Stage 4 prep. Stage 3 had no per-account ledger because Stage 3 was template-build (5 sessions total); Stage 4 is per-account production (~128 sessions across ~85 standalone + 13 entity parent letters + ~30 entity-child notices).

---

## Schema (per handoff §9 step 3)

10 columns, populated incrementally across each per-account session's lifecycle:

| Column | Type | Source | Populated when |
|---|---|---|---|
| `ord_id` | string (lowercase, verbatim from v6.2 `ord_id` column) | `_master-account-data-v6.2.csv` (standalone accounts) OR `_master-entity-data-v6.2.csv` Master Entity tab (entity-packet rows; `ord_id` = entity identifier per Master Entity convention) | At row creation (planning agent recommends production proof candidate or operator selects bulk account). |
| `company_slug` | string (lowercase, hyphen-separated, per `_root/07 §6` slug derivation) | `_master-account-data-v6.2.csv` `company` column (standalone) OR `_master-entity-data-v6.2.csv` `brands` column (entity-packet; multi-brand concatenation) | At row creation. |
| `format_routed` | enum: `Format A` / `Format B` / `Format B (CEO Pre-Call)` / `CEO Letter` / `Good News` / `Entity-packet parent letter` | Planning-agent routing pre-flight per `_root/06` 6-step flow against v6.2 + routing CSV joint state per Q9 operator stamp 2026-05-26 | At row creation (routing pre-flight runs BEFORE production proof recommendation per Stage 4 README §The review protocol step). |
| `drafter_session_id` | string (e.g. `2026-06-15-stage_4_1-001` — per planning-agent session-naming convention; first 3 digits sequential per stage_4_X prompt) | Planning-agent-assigned at paste-run time | At paste-run (planning agent assigns ID when operator paste-runs the prompt). |
| `brief_path` | string (relative path from `Pricing Migration/`) | Fresh-agent output per `_root/07 §6` file-naming convention | After fresh-agent session completes (drafter writes file; planning agent records path at review-pass). |
| `email_path` | string (relative path from `Pricing Migration/`) | Fresh-agent output per `_root/07 §6` file-naming convention | After fresh-agent session completes. |
| `routing_trace` | string (~50–150 chars; captures the 6-step flow trace + key derived inputs) | Fresh-agent conformance block's Step 3 routing pre-flight echo; planning agent transcribes condensed version | At review-pass. Format example: `Status PASS → not decrease → not entity → not annual → not health-override → Δ_pct=4.2% Δ_mrr=+$87 → Format A. Cohort: June. Driver: user_rate_normalization.` |
| `review_date` | ISO date `YYYY-MM-DD` | Planning-agent review-pass completion timestamp | At review-pass completion. |
| `operator_stamp_date` | ISO date `YYYY-MM-DD` OR `REVISION-REQUESTED YYYY-MM-DD` | Operator's `AskQuestion` stamp at review-pass surfacing | At operator stamp. If operator directs revision, populate as `REVISION-REQUESTED YYYY-MM-DD` and a follow-up `__v2` row is created at re-run (see Versioning below). |
| `notes` | string (free text; captures per-account observations) | Planning-agent observations at review-pass | At review-pass + updated throughout cohort execution. Examples: `PROOF-ACCOUNT for Format A` / `EP-FERGUSON-EXCLUSION fired during routing pre-flight; routed to escalation per _root/06 §1.6` / `CL-027 filed: v6.2 missing renewal_date column for Annual cohort` / `Cohort scheduled: 2026-06-15 send` / `Send-completed 2026-06-15; QB-115 audit-only pass` |

---

## Versioning (per `_root/07 §6` `__v2` convention)

When an upstream rule changes (`_root/03` / `_root/04` / `_root/05` / `_root/06` / `_root/07` / `_root/08`) AND that rule change propagates into already-drafted per-account briefs per `_root/CONTRACTS.md §3` step 5, affected ledger rows trigger re-runs:

1. Planning agent identifies affected rows by routing-CSV + driver + cohort + format intersection (e.g. a `_root/05 §2.4` driver-block edit affects all rows where `format_routed ∈ {Format A, Format B, CEO Letter}` AND `migration_driver = annual_discount_retirement`).
2. Affected rows get a `__v2` row appended below the original row in the ledger (same `ord_id` + `company_slug` + `format_routed`; new `drafter_session_id` + `brief_path` + `email_path` with `__v2` suffix per `_root/07 §6`).
3. Original row's `notes` column updates with `SUPERSEDED YYYY-MM-DD by __v2 row due to <rule-change description + changelog reference>`.
4. New `__v2` row paste-runs through the same review-pass protocol; gets its own `operator_stamp_date` at approval.

Per `_root/07 §6`: "The unversioned and `__v2` files coexist in the same folder until the unversioned file is retired by the operator." Same applies to ledger rows — both rows persist; the operator stamps retirement decisions separately.

---

## Operator stamp + AskQuestion convention

At each per-account review-pass surfacing, planning agent uses `AskQuestion` with at least one question:

> **Approve `<ord_id>__<slug>__brief.md` + `<ord_id>__<slug>__delivery-email.md` for `format_routed` send?**
> - approve-to-send (stamps `operator_stamp_date` = today; ledger row finalized; cohort scheduling proceeds)
> - revision-requested (stamps `operator_stamp_date` = `REVISION-REQUESTED YYYY-MM-DD`; planning agent + operator co-author revision direction; fresh-agent re-paste-runs OR planning agent's direct edit applied IF the revision is mechanical per Appendix A.5 path-reference contract enforcement vs substantive rule-question)
> - escalate (planning-agent audit surfaced a CL-class item; ledger row blocked pending source-fix per `_root/CONTRACTS.md §3`; CL-NNN filed)

Additional per-account questions may surface (e.g. for CEO Letter accounts: CEO call commitment date selection; for entity-packet accounts: per-child notice dispatch order). All operator stamps land in the row's `notes` column with date attribution.

---

## Cohort organization (Phase 6 scheduling lens)

The ledger does NOT carry a separate `cohort` column (cohort is in `notes` per Phase 6 scheduling decisions). For Phase 6 cohort-execution view, planning agent groups rows by cohort at scheduling time via `notes` column grep:

- **Cohort A — June** (~30–40 accounts per `_reference/2026-05-20__execution_plan_v3.3.md §IV`)
- **Cohort B — July** (~30–40 accounts)
- **Cohort C — Deferred** (~10–15 accounts; status overrides + special arrangements per `_root/02 §5` overlay)
- **Cohort D — Post-Migration** (2 rollup entities per `_root/06 §1.6`; per-entity timing post-parent-letter send)
- **Cohort E — Renewal-Based** (Annual overlay accounts per `_root/06 §4.3` + voice rules per `_root/04 §4.16` operator-stamped 2026-05-26 via Stage 4 prep Source-fix Session A; ~11 pending Annual accounts per `_root/02 §5`; send timed to 90-day pre-renewal window). **Pre-requisite — `renewal_date` v6.2 column gap**: `_master-account-data-v6.2.csv` does NOT currently carry a `renewal_date` column (53 columns; column absent per Source-fix Session A verification 2026-05-26). `_root/04 §4.16.2` fallback path: routing CSV `nuances` column per `_root/07 §5`. `_root/04 §4.16.4` surfacing requirement #1: drafter pauses + surfaces if `renewal_date` is absent OR ambiguous at draft time. Operator-stamped **defer-to-first-annual 2026-05-26** at Stage 4 prep Source-fix Session A audit — when the first Annual proof account routes through `stage_4_X`, planning agent surfaces that account's `renewal_date` source via `AskQuestion` (3 options: add column to v6.2 / permanent fallback in routing CSV `nuances` / per-account exemplar). Until then, no Cohort E rows are paste-run.

Per-row cohort tagging happens at operator stamp time (operator selects cohort assignment as part of the `approve-to-send` stamp; planning agent records in `notes` column as `Cohort: <A/B/C/D/E>; scheduled send YYYY-MM-DD`).

For Phase 6 schedule generation, planning agent runs `grep "Cohort: A"` (etc.) against this ledger + cross-references against `_reference/2026-05-20__execution_plan_v3.3.md §IV` cohort scheduling rules.

---

## Production proof rows (special markers)

Per Stage 4 README §The production proof gate, the FIRST account per `stage_4_X` prompt is a production proof account. Its ledger row is tagged in `notes`:

```
notes: PROOF-ACCOUNT for stage_4_<X>__<format>. <planning-agent recommendation rationale>. <audit result>. <operator stamp + any revision history>.
```

After production proof is operator-stamped, additional Format-X accounts begin paste-runs (per Stage 4 README §The production proof gate step 6). Each subsequent row follows the same schema; the `notes` column carries cohort assignment + any per-account observations.

---

## Ledger rows

> **Format**: one row per per-account session. Rows are added in paste-run order (not alphabetical or cohort order); for cohort view, see §Cohort organization above. Each row's pipe-delimited values match the schema column order.

### Per-format row groups

Rows are organized in this file by `format_routed` for readability; within each format, rows are appended in paste-run-chronological order.

#### Format A — 60-Day Notice (`stage_4_1__format-a__per-account-drafter.md`)

| ord_id | company_slug | format_routed | drafter_session_id | brief_path | email_path | routing_trace | review_date | operator_stamp_date | notes |
|---|---|---|---|---|---|---|---|---|---|
| lpf | linon-powell-furniture | Format A — 60-Day Notice | 2026-05-26 Stage 4.1 paste-ready / lpf fresh agent | `format-a-notices/lpf__linon-powell-furniture__brief.md` | `format-a-notices/lpf__linon-powell-furniture__delivery-email.md` | 6-step `_root/06 §2`: (1) entity_overlay=FALSE → no entity override; (2) hold_condition=blank → not held; (3) delta_mrr=+$65 / delta_pct=+2.8% → 60-Day Notice band per `_root/06 §3` delta-tier dispatch; (4) health_band=Thriving / value_delivery_score=100 → no health override per `_root/06 §4.1`; (5) deal_type=Monthly → no Annual overlay per `_root/06 §4.3`; (6) format=Format A; `comm_action=60-day-notice` mirrors. | 2026-05-26 | 2026-05-26 | PROOF-ACCOUNT for stage_4_1__format-a. Planning-agent recommendation: T3 / Monthly / Thriving / VD=100 / no holds / Tailwind non-ABTS / canonical URN driver / clean v6.2 row. Audit result: brief math integrity verified under operator-stamped Discipline (1) at Stage 4.1 lpf production proof closeout 2026-05-26 (CL-025 RESOLVED per Appendix B.4) — v6.2 modeled-canonical wins per Appendix B; After-row math = v6.2 stamped values; reconciliation flag fired ⚠️ (`_root/07 §4.5` thresholds tripped: implied_billed_excess=26 vs narrative_excess=19; gap=+7 users / +$140/mo; Pattern 1 phantom enabled); brief APPROVED as-drafted Format A; routing-CSV `flags`/`nuances` mapping disagreement against planning-agent pre-flight surfaced + acknowledged-discipline stamp applied (all future `_paste-ready/` annotations parse routing CSV via header-position mapping, never visual inspection). Path (b) re-route to Format B briefly stamped earlier in session then ROLLED BACK after v6.2 canonical authority clarified. **Reconciliation tracker cross-reference**: `_meta/v6_2_reconciliation_log.md` row 1 (lpf | Pattern 1 | gap +7u / +$140 | target pre-2026-09-01 EFFECTIVE_DATE | ops_owner Kylor | ops_status pending; CSM/Ops team verifies 7 phantom enabled accounts + disables pre-effective-date). Operator stamp 2026-05-26: approve-to-send under Discipline (1); Cohort: TBD-pending-scheduling. |

#### Format B — Notice + Meeting (`stage_4_2__format-b__per-account-drafter.md`)

| ord_id | company_slug | format_routed | drafter_session_id | brief_path | email_path | routing_trace | review_date | operator_stamp_date | notes |
|---|---|---|---|---|---|---|---|---|---|
| cci | currey-and-company | Format B — Notice + Meeting Offer | 2026-05-26 Stage 4.2 paste-ready / cci fresh agent | `format-b-notices/cci__currey-and-company__brief.md` | `format-b-notices/cci__currey-and-company__delivery-email.md` | 6-step `_root/06 §2`: (1) status_filter `ghost_account=FALSE` + `migration_status=migration_pending` → PASS; (2) decrease `delta_mrr=+$305` → not decrease; (3) entity_overlay `parent_entity=Currey & Company == company` → standalone in scope; (4) annual `deal_type=Monthly` → no Annual overlay per `_root/06 §4.3`; (5) health `health_band=Thriving` (92.4) + `value_delivery_score=100` → no override per `_root/06 §4.1`; (6) delta-tier dispatch `delta_mrr=+$305` ($80<$305≤$400) AND `delta_pct=+13.9%` (10%<13.9%≤30%); `delta_mrr<$600` → CEO Pre-Call variant does NOT fire; format = **Format B — Notice + Meeting Offer (standard variant)**; `comm_action="Format B — Notice + Meeting Offer"` mirrors; routing-CSV `flags=INSIGHTS-LAYER` (non-blocking annotation per `_root/06 §5.5`). Cohort: June. Driver: user_rate_normalization (no secondary). | 2026-05-26 | 2026-05-26 | PROOF-ACCOUNT for stage_4_2__format-b. Planning-agent recommendation: T3 / Monthly / Thriving / VD=100 / no holds / Narrative segment / canonical URN driver / clean v6.2 row / NOT in `_meta/v6_2_reconciliation_log.md` 37-row flagged set (cci is in the 70 unflagged pool per 2026-05-26 cohort sweep). Audit result: 2 production artifacts conformance-clean — `cci__currey-and-company__brief.md` (133 lines) + `cci__currey-and-company__delivery-email.md` (47 lines); CL-024 paste-verification 16/16 verified verbatim against `_root/` source (independent re-verification per planning-agent audit pass); CL-025 After-row math discipline enforced (v6.2-canonical: `excess_users=8` / `user_charge=$200` / `new_total_mrr=$2,495`; ladder-recomputes 8×$25=$200 ✓; Before-row billing-derived `LEGACY_EXCESS=ROUND(480/20)=24` ✓); reconciliation pre-flight per `_root/07 §4.5` did NOT fire (gap_users=1<3 AND gap_dollars=$20<$60 — both below thresholds; consistent with cci absent from tracker). Postgres-derived metrics re-verified via `csv.DictReader`: `cost_per_order=$7.53` + `delta_per_order=$0.92` + `annual_subscription=$29,940`; §4.8 value-anchor BOTH gates fire (`cost_per_order<$200` ✓ + `delta_per_order<$50` ✓; value-anchor section included). Conditionals fired: §4.6 platform-base-grown follow-on paragraph (new_tier_base $2,295 > current_platform_mrr $1,710); §4.10 URN platform-base conditional Format B form (Before ≠ After); §4.9 billing-basis footnote (URN-primary); §2.1.2 `[IF excess users remain after new included base]` sub-block ($N=15$ users absorbed; 8 excess remain). Conditionals NOT fired: §4.7 early-adopter (cohort 2021 > 2015); §4.4 high-delta annual-dollar (delta_pct 13.9% ≤ 30%); §4.13 health-band override (Thriving + VD=100); §4.14 PDC substitution; §4.5 IUR fork (no IUR primary or secondary); §3m "How This Compares" (drafter judgment OMITTED per lpf precedent + QB-071; operator-stamped omission); §3.16 CEO Pre-Call → Format B variant calibration. In-session correction: QB-053 strip of "(T3)" from running prose at §4.10 sentence (running prose retains tier NAME only; "(T3)" preserved in table cells + Section 3j verbatim block opener per CL-024). 3 minor citation cosmetics in drafter's conformance block (col 46 vs 45 for ghost_account; row 222 vs 73 for v6.2; row 28 vs 27 for routing CSV) — non-blocking; VALUES correct; INDICES off-by-one; operator-stamped non-blocking at closeout. Health-score CSV mirror drift (routing CSV 91.7 vs v6.2 92.4) — surfaced; v6.2 wins per `_root/07 §1` + Appendix B canonicality; 0.7-point spread does not flip band; routing decision unaffected. Operator stamps 2026-05-26: APPROVE lede paragraph (Section 3b drafter-generated) + APPROVE email Sentence 1a (drafter-generated DEFAULT relationship hook 14 words) + APPROVE OMISSION of "How This Compares" (lpf precedent) + APPROVE closeout. `[CONTACT_NAME]` token in delivery email left for CSM send-time substitution (operator confirmation: CSM owns at send, consistent with lpf precedent). Cohort: TBD-pending-scheduling. |
| sca | shadow-catchers | Format B — Notice + Meeting Offer | 2026-05-26 Stage 4.2 paste-ready v2 / sca fresh agent (post-CL-027 source-fix re-paste-run) | `format-b-notices/sca__shadow-catchers__brief.md` | `format-b-notices/sca__shadow-catchers__delivery-email.md` | 6-step `_root/06 §2`: (1) status_filter `ghost_account=FALSE` + `migration_status=migration_pending` → PASS; (2) decrease `delta_mrr=+$224` → not decrease; (3) entity_overlay `parent_entity=Shadow Catchers == company` → standalone in scope; (4) annual `deal_type=Monthly` → no Annual overlay; (5) health `health_band=Thriving` (v6.2 82.4; routing CSV `Healthy` 79.8 — v6.2 wins per Appendix B; 2.6-pt soft drift; no override fires); (6) delta-tier dispatch `delta_mrr=+$224` ($80<$224≤$400 Format B dollar band) AND `delta_pct=+30.9%` (just above 30% pct band threshold by 0.9 pts) → `_root/04 §4.4` high-delta annual-dollar lede rule FIRES INSIDE Format B (lede-voice modification, NOT format-flip; delta_mrr=$224 << $400 CEO Letter dollar floor); format = **Format B — Notice + Meeting Offer (standard variant)**; `comm_action="Format B — Notice + Meeting Offer"` mirrors; routing-CSV `flags=EARLY-ADOPTER-2015 \| EXPANSION-T1_TO_T2`. Cohort: June. Driver: user_rate_normalization. Secondary: included_user_reduction (REDUCTION-direction; legacy 25 > new included 10). | 2026-05-26 | 2026-05-26 | **FIRST PRODUCTION PROOF for CL-027 source-fix** (post-CL-027 `_root/05 §2.1.2` line 101 reduction-direction sub-block exercising). Planning-agent recommendation: T1 / Monthly / Thriving / VD=100 / no holds / Narrative segment / canonical URN-primary + IUR-secondary REDUCTION-shape (the dominant 25 of 26 URN+IUR-secondary v6.2 cohort) / clean v6.2 row / NOT in `_meta/v6_2_reconciliation_log.md` 37-row flagged set. Audit result (planning-agent independent verification 2026-05-26): 2 artifacts conformance-clean — brief (137 lines) + delivery email (47 lines); CL-024 paste-verification 21/21 verified verbatim against `_root/` source including the post-CL-027 §2.1.2 line 101 reduction-direction sub-block (FIRST production exercise — mutual-exclusivity gate operates as designed; line 98 expansion sub-block NOT fired; line 101 reduction sub-block FIRED producing correct "adjusting from the legacy 25 to the current Catalog Essentials standard of 10" prose; pre-CL-027 prose would have produced direction-inverted "expanding from 25 to 10 — absorbing −15 users"). CL-025 After-row math discipline enforced (v6.2-canonical: `excess_users=8` / `user_charge=$200` / `new_total_mrr=$949`; ladder-recomputes 8×$25=$200 ✓; Before-row billing-derived `LEGACY_EXCESS=ROUND($0/$20)=0`). Reconciliation pre-flight per `_root/07 §4.5` did NOT fire (gap_users=+7 tripped AND gap_dollars=$0 NOT tripped per CL-028 AND-discipline tightening 2026-05-26; sca correctly absent from 37-row tracker). Postgres-derived metrics re-verified via `csv.DictReader`: `cost_per_order=$86.27` + `delta_per_order=$20.36` + `annual_subscription=$11,388`; §4.8 value-anchor BOTH gates fire. Conditionals fired: §4.4 high-delta annual-dollar lede rule ($2,688/year in lede + §4.13 sentence); §4.6 platform-base-grown follow-on ($749 > $725); §4.7 early-adopter tenure paragraph (cohort 2015; **first production proof of §4.7 paste**); §4.9 billing-basis footnote (URN-primary + IUR-secondary; one paste covers both per §2.1.7); §4.10 URN platform-base conditional Format B form embedded in §2.1.2 verbatim at line 84; §4.5 IUR-fork variant (secondary = IUR per §2.13 non-negotiable). Conditionals NOT fired: §4.13 health-band override (Thriving + VD=100); §4.14 PDC substitution; §3m "How This Compares" (drafter judgment OMITTED per lpf + cci precedent + QB-071 + §4.11 — **3rd consecutive omission; pattern locked as Format B URN-primary default for Stage 4 template-level convention candidate; surface at Action 3 self-audit pass**). Soft finding (non-blocking): drafter's manifest echo cited `_root/07` and `_root/08` Last-updated = `2026-05-22`; actual header dates + manifest §2 rows = `2026-05-26` (Wave 6 batch from Stage 4 prep Source-fix Session B). Mirrors cci closeout's 3-citation-cosmetic precedent — non-blocking; conformance-block annotation hygiene only. New drift watchlist finding 13 surfaced + RESOLVED IN-SESSION via CL-028 (`_root/07 §4.5` OR-prose → AND-prose tightening per operator stamp `resolve_now_AND_canonical` 2026-05-26). Drafter-generated lede health-data extension (4th-stat health-component variant per Migration-Health Artifacts/) DEFERRED to Stage 4 template-level convention at Action 3 self-audit pass (not retroactive to sca). Operator stamps 2026-05-26: APPROVE as-drafted (Section 3b lede + §4.7 paste + §3m omission) + RESOLVE drift-13 now via CL-028 AND-tightening. `[CONTACT_NAME]` token in delivery email left for CSM send-time substitution per lpf + cci precedent. Cohort: June (1-Jul deadline). |

#### CEO Letter + Call Commitment (`stage_4_3__ceo-letter__per-account-drafter.md`)

| ord_id | company_slug | format_routed | drafter_session_id | brief_path | email_path | routing_trace | review_date | operator_stamp_date | notes |
|---|---|---|---|---|---|---|---|---|---|
| *empty — first row populates at CEO Letter production proof paste-run* | | | | | | | | | |

#### Good News Notice (`stage_4_4__good-news__per-account-drafter.md`)

| ord_id | company_slug | format_routed | drafter_session_id | brief_path | email_path | routing_trace | review_date | operator_stamp_date | notes |
|---|---|---|---|---|---|---|---|---|---|
| *empty — first row populates at Good News production proof paste-run* | | | | | | | | | |

#### Entity-packet parent letter (`stage_4_5__entity-packets__parent-letter-per-account-drafter.md`)

| ord_id (entity) | company_slug (entity brands) | format_routed | drafter_session_id | brief_path | email_path | routing_trace | review_date | operator_stamp_date | notes |
|---|---|---|---|---|---|---|---|---|---|
| *empty — first row populates at Entity-packet production proof paste-run* | | | | | | | | | |

---

## Entity-packet orchestration playbook (Stage 4.5 sub-structure per operator stamp 2026-05-26)

Per Q8 operator stamp 2026-05-26 — Stage 4.5 = ONE drafter prompt for parent-letter artifact + orchestration playbook (this section) for per-child notice dispatch.

For each entity in scope per `_root/06 §1.6` (13 entities; Ferguson excluded per mixed-direction one-off):

1. **Parent letter paste-run**: planning agent recommends entity production proof candidate via `AskQuestion`; operator selects. Operator paste-runs `stage_4_5__entity-packets__parent-letter-per-account-drafter.md` with `[ENTITY_ORD_ID]` substituted. Fresh agent produces parent letter + parent-letter delivery email. Planning agent audits per review protocol; operator stamps; ledger row in Entity-packet section above.
2. **Per-child enumeration**: per `_master-entity-data-v6.2.csv` Master Entity tab `member_accounts` column, planning agent enumerates the entity's child brands (each brand corresponds to one `ord_id` in `_master-account-data-v6.2.csv`).
3. **Per-child format routing**: planning agent runs the 6-step routing flow per `_root/06` against EACH child brand individually (children may route to different formats — e.g. an entity might have 2 children routing to Format A, 1 to Format B, and 1 to Good News). For each child, planning agent recommends format-routed proof OR (if format proof already operator-stamped) direct production paste-run.
4. **Per-child dispatch**: each child paste-runs under the format-routed `stage_4_X` per-format prompt (NOT under stage_4_5; stage_4_5 is parent-letter-only). The child's per-account row populates in the format-routed Section above (Format A / Format B / CEO Letter / Good News), with `notes` column tagged `Entity-packet child of <ENTITY_ORD_ID>; coordinate send within 48-hour window after parent letter per _root/04 §4.15.6`.
5. **48-hour coordination check**: per `_root/04 §4.15.6` operator stamp 2026-05-26, per-child notices send within 48 business hours of parent letter send. Planning agent verifies cohort assignment supports this window AND verifies routing-CSV `nuances` column doesn't override (e.g. a child marked HOLD per routing CSV blocks the 48-hour window — escalate per `_root/CONTRACTS.md §2`).

The orchestration playbook is operator-stamped at Stage 4 prep handoff (per Q8 stamp 2026-05-26). Operationalized at first entity-packet paste-run (after 4.5 prompt authored + parent-letter proof operator-stamped).

---

## Audit-trail integrity rules

1. **No row deletions.** Rows persist forever. If an account is removed from program scope (e.g. customer churned mid-2026), the row's `notes` column updates with `OUT-OF-SCOPE YYYY-MM-DD per <reason>` but the row stays.
2. **No retroactive row edits to `operator_stamp_date`.** Once stamped, the date is the audit record. If revision later requested, see Versioning above (`__v2` row); the original stamp is preserved.
3. **`routing_trace` column is the routing-decision audit artifact.** Any post-hoc routing re-derivation must reconcile against the original `routing_trace`. Discrepancies surface as CL items.
4. **`notes` column may be updated post-stamp** for cohort assignment, send completion, post-send audit signals, CL-related observations. Each update is timestamped within the notes string (`Cohort: A; scheduled send 2026-06-15` → `Cohort: A; scheduled send 2026-06-15; SEND-COMPLETED 2026-06-15; QB-115 audit-only PASS 2026-06-22`).
5. **Planning-agent custodianship is exclusive.** Only the Stage 4 planning agent writes/edits ledger rows. Per-account drafters never touch this file. Operator stamps land via `AskQuestion` and are transcribed by planning agent.

---

*Cross-references: `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` §9 step 3 (schema operator-stamp); `_meta/stage4_prompts/README.md` (per-account session review protocol); `_root/07 §6` (file-naming + versioning convention); `_root/06 §1.6` (entity-packet program scope — 13 entities); `_root/04 §4.15.6` (48-hour parent-letter / per-child coordination); `_root/02 §5` (cohort overlay); `_reference/2026-05-20__execution_plan_v3.3.md §IV` (Phase 6 cohort schedule).*
