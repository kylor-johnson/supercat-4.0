# 06 — Format Routing

> **What this doc owns**: The 4 brief formats + 2 routing patterns (Format A, Format B, CEO Letter, Good-News Notice, plus the CEO Pre-Call → Format B pattern and the CEO-Led Entity Pre-Engagement → Coordinated Notices pattern). The 6-step routing-decision flow (status filter → decrease check → entity overlay → annual overlay → health override → delta-tier dispatch) and the order in which the steps fire. The delta-tier dispatch table (the headline dollar-threshold rule). The three override rules as they affect format selection (entity, health, annual). The `comm_action` vocabulary used in `migration_comm_tiers_2026-05-19.csv` and the mapping of each value to a format. A self-sufficient mirror of the 5 routing-CSV errata pulled from `_root/02 §7` (with a pointer that `_root/02` is the canonical owner). A self-sufficient mirror of the per-format output-folder mapping pulled from `_root/07 §6`.
>
> **What this doc DOES NOT own**: Segment definitions, account counts, the ownership-boundary rationale, the canonical 5-errata list itself → `_root/02`. Voice / tone rules for each format's lede and close (including the verbatim close text and the Watch-band lede override) → `_root/04` (especially §4.12, §4.13). The per-driver "Why the Number Is Changing" prose that goes into the brief body → `_root/05`. The verbatim "What You're Getting at $X" tier blocks and the user-rate ladder → `_root/03`. v6.2 column meanings, the loader, the routing-block field list, the file-naming convention, and the per-format output folders themselves → `_root/07`. The pre-send quality checklist → `_root/08` (Wave 4).
>
> **Last updated**: 2026-05-26 (Stage 3.5 prep — §1.6 rewritten with `_master-entity-data-v6.2.csv` Master Entity tab as canonical scope source; 5-account routing-CSV-snapshot claim replaced with 14-entity canonical program scope [13 rollup + 1 standalone_multi_org]; Ferguson Enterprises mixed-direction one-off exception documented; routing-vs-artifact distinction stamped; parent-letter voice register cross-referenced to `_root/04 §4.15`; default-only pricing posture cross-referenced to `_root/04 §4.15.5`; output-folder structure for `entity-packets/<entity-slug>/` operator-stamped; CL-014 closed at Stage 3.5 prep; §4.1 entity-overlay timing + voice consequences updated for Master Entity tab cohort distribution + §4.15 voice rules; §4.2 HOLD-row tally annotated with routing-CSV-slice clarification. **Stage 3.5 review-pass amendment 2026-05-26**: §1.6 `delivery_owner` enumeration reconciled to CSV ground truth — Thesis moved from Kylor row to CEO row [Master Entity tab row 13: `delivery_owner = CEO`]; counts updated [3→4 CEO-delivered; 10→9 Kylor-delivered rollup; cross-reference summary lines 91 + 101 internally aligned]; CSV is canonical per §1.6 operator stamp 2026-05-26, rule-layer enumeration reconciles to CSV.)
> **Owner**: CEO
> **Primary sources**: `_root/02` (segments + overlays + errata); `_root/07` (`comm_action` column + output folders + routing-block matrix); archived `_handoff-prompt.md` §Format Routing Rules + §Data Corrections (read under explicit Wave 3.2 authorization per `_root/CONTRACTS.md` §4); `migration_comm_tiers_2026-05-19.csv` (header + distinct `comm_action` values); exec plan v3.3 §III + §IV + §V + §VI; archived brief-template front-matter (Format A, Format B, CEO Letter, Good News — operator notes only, NOT body prose).
> **Supersedes**: format-routing rules previously scattered across the archived `_handoff-prompt.md` and the routing CSV's implicit logic. After this doc lands, every Stage 4 drafter consults `_root/06` to determine format, then references `_root/02` for overlay confirmation, then opens `_root/05` for body content.

---

## §1. The 4 brief formats + 2 routing patterns

The migration communications system uses exactly four brief formats plus two routing patterns. The routing patterns reuse existing brief artifacts under different ownership and sequencing: `CEO Pre-Call → Format B` (Δ ≥ $600) uses the Format B brief preceded by a CEO call; `CEO-Led Entity Pre-Engagement → Coordinated Notices` (complex multi-brand entities) uses CEO program design followed by a coordinated child-notice batch whose individual formats depend on each child's Δ tier. No other formats or patterns exist. New formats are not invented by drafters; a missing fit is flagged to the operator per `_root/CONTRACTS.md` §2.

### Format A — 60-Day Notice (CS-led, near-flat)

CS-sent (Kylor) standard 60-day notice for accounts whose Δ MRR is near-flat (≤$80/mo or ≤10%, whichever is more rigorous — see §3). Demonstrates the writer looked at the specific account, names the new rate, confirms operations are unchanged, and closes with a passive "talk if you want to" offer rather than a meeting commitment. Closing language is owned by `_root/04 §4.12` (Format A close — "What Happens Next").

- **Who sends**: CS team (Kylor).
- **Distinctive close**: passive offer ("If you'd like to talk through the rate or anything about this before then — that conversation is welcome").
- **Output folder**: `format-a-notices/` (per `_root/07 §6`).
- **CEO awareness required before send**: No.

### Format B — Notice + Meeting Offer (CS-led, meaningful delta)

CS-sent (Kylor) 60-day notice for accounts whose Δ MRR is meaningful but does not breach the $400 ownership boundary ($81 ≤ Δ ≤ $399). Same structural notice as Format A, but the close includes an active meeting offer — Kylor commits to reach out in the next few days. Closing language is owned by `_root/04 §4.12` (Format B close — "Let's Talk").

- **Who sends**: CS team (Kylor).
- **Distinctive close**: active meeting offer ("I'll reach out in the next few days to walk through this together").
- **Output folder**: `format-b-notices/` (per `_root/07 §6`).
- **CEO awareness required before send**: No (for the Notice + Meeting tier itself).

### CEO Letter + Call Commitment (CEO-authored, $400–$599)

CEO-authored letter that accompanies the formal notice. Triggered by the $400 ownership boundary in `_root/02 §2`. The CEO signs and personalizes; CS executes delivery. The close commits to a specific calendar date for a CEO-initiated call within 5 business days of send. Closing language is owned by `_root/04 §4.12` (CEO Letter close — "I'll Call You"); the verbatim §4.13 Watch-band lede override applies when the health-override is in play but does not preempt the format.

- **Who sends**: CEO authors / signs; CS executes delivery.
- **Distinctive close**: specific call-commitment date within 5 business days of send.
- **Output folder**: `ceo-letter-notices/` (per `_root/07 §6`).
- **CEO awareness required before send**: Yes.

### Good-News Notice (CS-led, price decrease)

Short (200–300 word) email-length notice for any account where Δ MRR < $0 (price flat or decreasing). State the decrease in sentence one; do not frame as a gift, favor, or reward. No CEO involvement. No meeting offer. No expansion ask. Closing language is owned by `_root/04 §4.12` (Good News close — operator-led, no ask).

- **Who sends**: CS team.
- **Distinctive close**: no meeting offer, no call commitment ("Questions about what's changing or how the new rate was calculated — reach out directly").
- **Output folder**: `good-news-notices/` (per `_root/07 §6`).
- **CEO awareness required before send**: No.
- **Override interaction**: a Good-News-eligible account that is Watch / At Risk / Critical does NOT receive Good News — it routes to a CSM health check-in first. See §4.2.

### CEO Pre-Call → Format B (routing pattern, Δ ≥ $600)

Not a separate brief format. The CEO initiates a proactive call BEFORE any notice is sent. After the call lands, a Format B brief is drafted and delivered as the formal 60-day notice. The Format B brief's routing block carries a `CEO awareness required before send: YES` flag and notes the pre-call has occurred. Output writes to `format-b-notices/` with the CEO-awareness flag per `_root/07 §7`.

- **Who sends**: CEO calls first; CS drafts and executes the follow-up Format B notice.
- **Distinctive close**: the same Format B close (§4.12), but the lede references the prior CEO conversation rather than offering a first-touch meeting.
- **Output folder**: `format-b-notices/` (per `_root/07 §6`), with the CEO-awareness flag in the routing block per `_root/07 §7`.
- **CEO awareness required before send**: Yes.

### §1.6 — CEO-Led Entity Pre-Engagement → Coordinated Notices (entity-packet program — rollup + standalone_multi_org entities; rewritten 2026-05-26)

Not a separate brief format. A two-stage pattern for multi-brand entities (rollup) and single-brand entities operating multi-org structures (standalone_multi_org) where one coordinated communication replaces N independent per-brand notices. **Stage 1**: the parent letter sends to the entity's principal/CEO, framing the portfolio-level change. **Stage 2**: per-brand notices follow within 48 hours, each in the child's natural format (Format A / Format B / CEO Letter / Good News — dispatched on the child's individual Δ tier per §2–§3). The two-stage sequencing is mandatory; per-brand notices MUST NOT precede the parent letter.

**Canonical scope source**: `_master-entity-data-v6.2.csv` (the 6.2 Master Entity tab — operator-stamped 2026-05-26 as the canonical entity-level scope source, parallel to `_master-account-data-v6.2.csv` for standalone-account scope). Each row in the Master Entity tab is one entity-packet account. The Master Account tab carries per-child data joined via `member_ord_ids` ↔ `ord_id`.

**Routing vs artifact distinction (operator-stamped 2026-05-26)**: this §1.6 documents the entity-packet PROGRAM (which entities are in scope + the two-stage sequencing). The artifact output for each entity is the parent letter (owned by Stage 3.5 entity-packet template) PLUS per-child notices (each owned by the Stage 3.1–3.4 standalone-format template the child routes to). Stage 3.5 produces ONLY the parent-letter artifact.

**Accounts using this pattern** (per `_master-entity-data-v6.2.csv` 2026-05-26 — 14 entities total):

- **13 rollup entities** (`entity_type = rollup`), covering ~30 child brands:
  - **CEO-delivered (4 entities; `delivery_owner = CEO`)**: Gabriella White (4 brands: `sc | gh | scw | sccon`); Jonathan Charles (2 brands: `jc | jcusa`); Rock House Farm (2 brands: `cf | hh`); Thesis (2 brands: `eglo | eglo_can`).
  - **Kylor-delivered (9 entities; `delivery_owner = Kylor`)**: Abaline (`asi | mpc`); Coleto Brands (`prog | kl`); Creative Home Furniture (`ta | tam`); Ferguson Enterprises (`mlg | ml` — **mixed-direction; see exception note below**); Godinger Group (`gsa | rac | ssi | pw`); HVLG (`hvl | tl | cl`); Interlude Home (`ih | ihw`); Visual Comfort & Co. (`fms | vcg | tla | vce`); WAC Group (`wac | sbl`).
- **1 standalone_multi_org entity** (`entity_type = standalone_multi_org`; Kylor-delivered): Maxim group Lighting (1 brand: `mli`) — single-brand entity using entity structure for multi-org-discount retirement.

**Notice cohort timing** (per Master Entity `notice_cohort` column):

- 12 entities are `notice_cohort = June` (the June cohort).
- 2 entities are `notice_cohort = Post-Migration` (HVLG; Rock House Farm) — route post-cohort timing per `_root/02 §5`.

**Direction** (per Master Entity `default_delta` column):

- 13 entities are entity-level increase (`default_delta > 0`; Stage 3.5 template targets this scope).
- **1 entity is mixed-direction**: Ferguson Enterprises (`mlg` increase + `ml` decrease; net entity `default_delta = -$109/mo`). **Exception (operator-stamped 2026-05-26)**: Ferguson Enterprises is NOT handled by the standard Stage 3.5 entity-packet template. Instead, `mlg` routes to its natural increase-side format (per §2–§3 dispatch on its individual Δ tier); `ml` routes to Good News per §3 row 1. A coordinated parent-letter wrapper for Ferguson Enterprises is authored ad-hoc at Stage 4 production drafting if the operator judges it necessary. The mixed-direction case is too rare (1 of 14 entities) to warrant template-level handling.

**Stage 3.5 template scope (operator-stamped 2026-05-26)**: the Stage 3.5 entity-packet template targets the **12 unambiguously increase-side rollup entities** plus the 1 standalone_multi_org entity (Maxim) — 13 entities total. Ferguson Enterprises is excluded per the exception above.

**Parent-letter voice register**: owned by `_root/04 §4.15` (Parent-letter voice register — entity-packet program). Voice forks by `delivery_owner` per `_root/04 §4.15.1`: CEO-delivered (4 entities) uses CEO-to-CEO peer voice; Kylor-delivered (10 entities — 9 rollup + 1 standalone_multi_org Maxim) uses SuperCat Head of Customer Success direct-relationship voice. The cross-format CSM-role note at `_root/04 §4.15.1` documents that across all 5 Stage 3 templates, the "CSM-sent" role-marker is filled by Kylor (HoCS) in practice — SuperCat's CSM support role does NOT handle migration conversations.

**Parent-letter pricing posture**: default-only per `_root/04 §4.15.5` (operator-stamped 2026-05-26). The Master Entity tab's `consolidated_delta` / `consolidation_saving` / `consolidation_saving_pct` columns are INTERNAL-ONLY for CSM/CEO post-send conversation; the parent letter presents only `default_mrr` / `default_delta` / `default_delta_pct`. Migration delivery is decoupled from consolidation sales motion per the `_root/04 §4.15.5` rationale (1.6–6.2% consolidation savings range across 13 rollup entities — meaningful but modest; mixing migration with sales dilutes both).

**Per-child notice format dispatch**: per-child notices use the child's natural format determined by the §2–§3 routing decision flow applied at the child level (with `migration_status` + `ghost_account` + decrease check + entity-overlay-already-applied + annual + health-override + Δ-tier evaluated against the CHILD's data in `_master-account-data-v6.2.csv`). Per-child notices write to their natural format folder (`format-a-notices/` / `format-b-notices/` / `ceo-letter-notices/` / `good-news-notices/`).

**Two-stage send timing**: parent letter sends first (Day 0). Per-child notices send within 48 hours of the parent letter (Day 1–Day 2). The 48-hour window is operator-stamped 2026-05-26 (`_root/04 §4.15.6`); revising requires the rule-change protocol per `_root/CONTRACTS.md §3`.

**Output folder structure (Stage 3.5)**: the parent-letter template lives at `entity-packets/_parent-letter-template.md` + `entity-packets/_parent-letter-delivery-email-template.md`. At Stage 4 production drafting, each entity's parent-letter artifact lives at `entity-packets/<entity-slug>/<entity-slug>__parent-letter.md` per the Stage 3.5 packet_structure operator stamp 2026-05-26 (parent letter + per-child notices bundle pattern). Per-child notice artifacts at Stage 4 live in their natural format folder, NOT under `entity-packets/<entity-slug>/`. Cross-entity coordination at Stage 4 production drafting is documented via per-entity README files in `entity-packets/<entity-slug>/` linking the parent letter to its child notices.

- **Who sends**: per `delivery_owner` column — CEO (4 entities) or Kylor in HoCS role (10 entities; 9 rollup + 1 standalone_multi_org Maxim).
- **Distinctive close**: parent-letter close per `_root/04 §4.15.6`; per-child notice close per the child's individual Δ tier (Format A / B / CEO Letter / Good News close per §1.1–§1.5 / §3).
- **CEO awareness required before send**: Yes for CEO-delivered entities (CEO authors); Yes for Kylor-delivered entities (CEO reviews + approves parent-letter content before send).
- **CL-014 status**: closed — entity-packet template folder + structure operator-stamped 2026-05-26 (Stage 3.5 prep pass). The `_meta/stage3_cleanup.md` CL-014 entry transitions to "applied at Stage 3.5 prep 2026-05-26" tag.

---

## §2. The routing-decision flow — order of evaluation

The format selection is a strict 6-step evaluation. The order matters: an earlier step that fires preempts every later step. Drafters evaluate in the order below and stop at the first step that produces a routing decision.

1. **Status filter** — skip rows where `migration_status = 'already_migrated'` (no notice needed; already on new pricing) or `ghost_account = TRUE` (placeholder / inactive / test row). This filter is enforced at the loader. Owning doc: `_root/07 §3`.
2. **Decrease check** — if `delta_mrr < 0`, route to Good-News Notice. The health-override interaction in §4.2 may pull a Good-News-eligible account out of the Good News format and into a CSM health check-in. Owning doc: this doc (§3 and §4.2).
3. **Entity overlay** — if `parent_entity` is non-empty AND `parent_entity != company`, the child does NOT receive a standalone brief. The child folds into the entity packet (one coordinated artifact per parent). Format selection at the child level is suppressed. Owning doc: `_root/02 §3`.
4. **Annual overlay** — if `deal_type = 'Annual'`, a 90-day notice window applies (60-day legal minimum + 30-day buffer) and the account is batched into `notice_cohort = 'Renewal-Based'`. The annual overlay changes **timing only**; the format substance still dispatches on the account's natural Δ-tier. Owning doc: `_root/02 §5`.
5. **Health override** — if `value_delivery_score < 40` OR `health_band ∈ {Watch, At Risk, Critical}`, the account routes to the Strategic segment and the notice is deferred until a CEO-led conversation has stabilized the relationship. Format selection at notice time depends on the post-stabilization Δ tier and on operator assessment. The §4.13 Watch-band lede override (owned by `_root/04`) applies to whichever format is eventually drafted. Owning doc: `_root/02 §4`.
6. **Delta-tier dispatch** — if and only if no earlier step has fired, dispatch on Δ MRR per the table in §3 below.

The order is: status → decrease → entity → annual → health → delta-tier. The entity overlay supersedes Δ-tier dispatch. The health override supersedes the entity overlay only insofar as a Strategic-routed child still has its packet drafted at the entity level (per exec plan v3.3 §II, "mixed-segment entities: packet covers ALL children including Strategic-routed ones") — the Strategic conversation is held in parallel with the entity treatment. The annual overlay supersedes timing but not substance.

---

## §3. Delta-tier dispatch — the headline routing rule

For accounts that survive all overrides in §2 (healthy, standalone, monthly), the dollar-threshold table below maps Δ MRR to a format. Source: archived `_handoff-prompt.md` §Format Routing Rules + exec plan v3.3 §IV and §VI.

| Condition (on Δ MRR per month) | Format | Owner | Notes |
|---|---|---|---|
| Δ < $0 (any decrease) | Good-News Notice | CS team | Health-override interaction in §4.2: Watch / At Risk / Critical → CSM health check-in instead. |
| 0 < Δ ≤ $80 OR Δ_pct ≤ 10% | Format A — 60-Day Notice | CS (Kylor) | Near-flat. Δ_mrr threshold supersedes Δ_pct at the high end: an account with Δ_pct ≤ 10% but Δ ≥ $600 still routes to CEO Pre-Call → Format B per the ≥$600 rule. |
| $81 ≤ Δ ≤ $399 | Format B — Notice + Meeting | CS (Kylor) | Includes the active meeting offer in the close (`_root/04 §4.12`). |
| $400 ≤ Δ ≤ $599 | CEO Letter + Call Commitment | CEO + CS | CEO authors / signs; CS executes delivery. Specific call date within 5 business days of send (`_root/04 §4.12`). |
| Δ ≥ $600 | CEO Pre-Call → Format B | CEO + CS | CEO calls FIRST. Format B notice follows the call. Output writes to `format-b-notices/` with a CEO-awareness flag in the routing block per `_root/07 §7`. |

### Δ_pct vs. Δ_mrr precedence (stamped 2026-05-22)

The archived handoff's §Format Routing Rules joins the Format A condition with an `OR` (`delta_pct ≤ 10% OR delta_mrr ≤ $80`) and gives Format B as `delta_mrr $81–$399`. The precedence rule for boundary cases:

> **The higher-touch format wins.** Where Δ_mrr and Δ_pct disagree on which format the account lands in, the format that produces more substantive treatment (more CEO involvement, longer notice, deeper explanation) is the binding routing.

Two boundary applications:

1. **Low Δ_mrr but high Δ_pct.** An account at Δ = $75 / Δ_pct = 12% — Δ_mrr satisfies Format A's ≤$80 half of the OR; Δ_pct fails Format A's ≤10% half. The higher-touch format wins: **routes to Format B**, not Format A.
2. **Low Δ_pct but high Δ_mrr.** An account at Δ = $700 / Δ_pct = 8% — Δ_pct satisfies Format A's ≤10% half of the OR; Δ_mrr crosses the $600 boundary. The higher-touch format wins: **routes to CEO Pre-Call → Format B** per the Δ ≥ $600 row, not Format A.

The rule is operator-stamped 2026-05-22 (see `_root/09_changelog.md` Wave 3 operator-stamping entry). Drafters who encounter a boundary case where the rule produces a counterintuitive routing (e.g. a $79 / 50% account) escalate per `_root/CONTRACTS.md` §2 rather than reinterpret the rule unilaterally.

---

## §4. Overrides — the things that SUPERSEDE delta-tier dispatch

Three overrides preempt the §3 dispatch table. Each has a defined trigger (a v6.2 column condition), a format-selection consequence, a timing consequence, a voice consequence (pointer only — voice rules live in `_root/04`), and an owning doc for the rule itself (which is not this doc — the overrides themselves are owned by `_root/02`).

### §4.1 — Entity overlay

- **Trigger**: `parent_entity` is non-empty AND `parent_entity != company`. v6.2 carries the relationship in the `parent_entity` column; there is no separate boolean flag.
- **Format-selection consequence**: the child does NOT receive a standalone brief. The child folds into the entity packet — one coordinated artifact covering all child brands under the parent. Format selection at the child level is suppressed; the entity packet IS the format.
- **Timing consequence**: entity packets are batched per the Master Entity tab `notice_cohort` column (`_master-entity-data-v6.2.csv`) — 12 of 14 entities are `notice_cohort = June` (the June cohort, sent first — entity conversations serve as the high-fidelity pilot for the July cohort); 2 entities (HVLG; Rock House Farm) are `notice_cohort = Post-Migration` and route per `_root/02 §5` post-cohort timing.
- **Voice consequence**: the packet leads with multi-brand consolidation framing at the entity level, with per-brand pricing detail in the per-child notices that follow. The parent-letter voice register is owned by `_root/04 §4.15` (Parent-letter voice register — entity-packet program; authored 2026-05-26 with voice forks for CEO-delivered vs Kylor-delivered, multi-brand portfolio acknowledgment, cross-brand consolidation lens, per-brand mechanics restraint, default-only pricing posture, and routing pointer to per-child notices). The Stage 3.5 entity-packet template implements these voice rules.
- **Owning doc for the rule**: `_root/02 §3`.
- **Stage 3 dependency**: the entity-packet template architecture is operator-stamped 2026-05-26 (Stage 3.5 prep) — `entity-packets/_parent-letter-template.md` + `entity-packets/_parent-letter-delivery-email-template.md` will be authored at Stage 3.5; per-entity output folder `entity-packets/<entity-slug>/<entity-slug>__parent-letter.md` per Stage 4 production drafting. CL-014 in `_meta/stage3_cleanup.md` transitions to "applied at Stage 3.5 prep 2026-05-26" tag.

### §4.2 — Health override (VD < 40 OR Watch-or-worse)

- **Trigger**: `value_delivery_score < 40` OR `health_band ∈ {Watch, At Risk, Critical}`. Either condition fires the override independently.
- **Format-selection consequence**: the account routes to the Strategic segment regardless of Δ. The notice itself is **deferred** until a CEO-led conversation has stabilized the relationship. Format selection at notice time depends on the post-stabilization Δ tier and on the operator's assessment of the relationship state.
- **Timing consequence**: account moves to `notice_cohort = 'Post-Migration'` per `_root/02 §6`. No overlap with the June or July cohorts.
- **Voice consequence**: the §4.13 Watch-band lede override (`_root/04`) applies to whichever format is eventually drafted — the relationship-stats lede and "What You've Built" section are suppressed and the brief opens with the standalone dollar-change sentence. For the CEO Letter specifically, the call commitment also moves to the second sentence (no transition through activity stats). Detail in `_root/04 §4.13`.
- **Owning doc for the rule**: `_root/02 §4`.

**Format-A-vs-Good-News interaction.** Per the archived Good News brief-template front-matter (operator note: "Watch health flag: [YES/NO] — if Watch or below: DO NOT use this template; escalate to CSM for health check-in first"), a Good-News-eligible account that is Watch / At Risk / Critical does NOT send a Good News Notice. It routes through the CSM for a health check-in before any pricing communication. This is the only place where a price-decrease account is preempted out of Good News; the §4.2 health override is the trigger.

**At-Risk handling — operator-stamped 2026-05-22.** The archived `_handoff-prompt.md` §Format Routing Rules contains the line *"At Risk → do not draft migration notice."* The operationally-binding reading is: **defer the notice in the standard cohort; draft post-stabilization when the override resolves.** The handoff's terse phrasing means "no notice during the migration window," not "no notice ever." This matches `_root/02 §4` ("Strategic segment; CEO-led conversation precedes notice; walk-away thresholds pre-authorized") and is what drafters operate by today.

Operationalization: an At-Risk account moves to `notice_cohort = 'Post-Migration'` per `_root/02 §6`. The notice is held until the CEO conversation has either (a) stabilized the relationship such that a migration notice is appropriate, or (b) produced a walk-away decision that supersedes the notice. There is no scenario where an At-Risk account receives a migration notice in the June or July cohorts.

**Critical-band handling — operator judgment per-account (operator-stamped 2026-05-22).** A Critical-band account (`health_band = 'Critical'`) has no band-level routing rule. Critical handling is operator-decided per-account, and the per-account decision is recorded in the routing CSV's `post_hold_action` column. Observed `post_hold_action` values on Critical-band rows include both:

- `"NOT migration — separate health intervention program"` — the account exits the migration motion entirely into a separate health workflow; no migration notice is ever drafted.
- Standard format values (Format A / Format B / CEO Letter / Good News, with or without `"after CSM check-in"` / `"after CSM touchpoint"` parentheticals) — the account follows Reading A above (defer + draft post-stabilization).

Neither path is presumed for a Critical-band account at routing time. The operator chooses per-account when maintaining the routing CSV, and `post_hold_action` is the authoritative record of that decision. Stage 4 drafters reading a Critical-band row consult `post_hold_action` directly — they do not default to Reading A and do not default to the separate-intervention path.

Operator-stamped 2026-05-22 (see `_root/09_changelog.md` Wave 3 operator-stamping entry). The CSV's `post_hold_action` value is the per-account decision record; future revisions to the rule live here, and `_root/02 §4` carries the cross-reference so the segment-roster math (20 Watch-or-worse → 17 Strategic / 2 Annual / 1 Entity) does not silently assume Critical-band accounts will always be drafted post-stabilization.

### §4.3 — Annual overlay

- **Trigger**: `deal_type = 'Annual'` in v6.2.
- **Format-selection consequence**: format substance still matches the account's natural Δ-tier per §3. The overlay does **not** change which format is selected.
- **Timing consequence**: a contractual ≥90-day notice window applies (60-day legal minimum + 30-day buffer, per exec plan v3.3 §III). The account moves to `notice_cohort = 'Renewal-Based'` per `_root/02 §6`. Notice is sent ≥90 days before the account's renewal date; if a renewal is imminent (<90 days from today), the account is fast-tracked individually per `_root/02 §5`.
- **Voice consequence**: per exec plan v3.3 §III, the notice references the renewal date rather than a migration effective date. Voice detail is owned by `_root/04 §4.16` Annual-cohort voice rules (operator-stamped 2026-05-26 via Stage 4 prep Source-fix Session A; 4 sub-sub-sections: §4.16.1 Scope; §4.16.2 Lede effective-date shift; §4.16.3 Close + formal-notice line; §4.16.4 Drafter judgment + surfacing). CL-015 RESOLVED 2026-05-26 at source.
- **Owning doc for the rule**: `_root/02 §5`.
- **Entity-annual interaction**: per `_root/02 §3`, an annual entity-child is coordinated with the entity packet — the entity overlay still supersedes on segment label and ownership; the annual overlay supersedes on timing.

---

## §5. `comm_action` vocabulary — the routing CSV's column

`migration_comm_tiers_2026-05-19.csv` carries a `comm_action` column whose value is the per-account routing decision the CSV captures. The CSV is the routing data; this doc owns the rules. Where the CSV's per-account value contradicts the rules in §3 or §4, the rules win and the discrepancy is logged against the 5 errata in §6.

Distinct `comm_action` values present in `migration_comm_tiers_2026-05-19.csv` (109 rows total — counts include the 2 `Already Migrated` rows that the loader filters out per §2 step 1):

| `comm_action` value (verbatim from CSV) | Maps to | Row count in CSV | Notes |
|---|---|---:|---|
| `Format A — 60-Day Notice` | Format A (§1) | 15 | Standard near-flat dispatch. |
| `Format B — Notice + Meeting Offer` | Format B (§1) | 19 | Standard $81–$399 dispatch. Note the CSV's value carries the suffix "Offer"; the canonical format name is "Format B — Notice + Meeting" (the trailing word "Offer" is decorative). |
| `CEO Letter + Call Commitment` | CEO Letter (§1) | 9 | $400–$599 dispatch. |
| `CEO Pre-Call → Format B` | CEO Pre-Call → Format B routing pattern (§1) | 9 | Δ ≥ $600 dispatch. |
| `Good-News Notice` | Good News (§1) | 4 | Δ < $0 dispatch. |
| `Already Migrated` | Loader skips (§2 step 1) | 2 | `migration_status = 'already_migrated'`; not a format, a filter value. Per `_root/02 §8`, the two accounts are CopperSmith (`tcs`) and Dorell Fabrics (`drf`). |
| `HOLD` | Entity-gated / Watch-band / Annual / VD-override accounts pending resolution. **Eventual format is read from the CSV's `post_hold_action` column** (see §5.5). | 51 | A `HOLD` row is fully decomposable via the CSV's companion columns: `hold_condition` says why, `post_hold_action` says what next. The override that fired (entity / health / annual / VD) is documented in `hold_condition`; the eventual format is documented in `post_hold_action`. |

**The `HOLD` value is deterministic, not a black box.** A Stage 4 drafter encountering `comm_action = HOLD` on a row reads three additional columns in the same row:

1. **`hold_condition`** — the explicit reason this row is on hold. Examples: *"Entity (Gabriella White) — wait for entity parent conversation"*, *"Health hold — Watch (52.9); discount_correction; CSM check-in before notice"*, *"Unscored — Annual; cannot assess risk without health data; pull renewal date"*.
2. **`post_hold_action`** — the format the row resolves to once the hold lifts. Examples: *"Format B — Notice + Meeting Offer"*, *"CEO Letter + Call Commitment (+$734)"*, *"CEO-Led Entity Pre-Engagement → Coordinated Notices (HVLG program)"*, *"Good-News Notice (after CSM touchpoint)"*, *"NOT migration — separate health intervention program"*.
3. **`flags`** — semicolon-separated tags carrying routing-relevant per-account context (`EARLY-ADOPTER-2014`, `VD-OVERRIDE`, `DISCOUNT-CORRECTION`, `EXPANSION-HOLD`, `ANNUAL`, `INSIGHTS-LAYER`, `EXPANSION-T1_TO_T2`, etc.). See §5.5 for the flag vocabulary.

The decomposition of the 51 HOLD rows per `migration_comm_tiers_2026-05-19.csv` (2026-05-22 snapshot): 39 entity children (parent_entity ≠ company), 17 with health-override-eligible bands (Watch/At-Risk/Critical), 9 with Annual deal_type, 13 with `value_delivery_score < 40`. These overlap (an HVLG child is entity + VD-override + DISCOUNT-CORRECTION-flagged); `hold_condition` is the authoritative per-account explanation.

**`post_hold_action` distribution among the 51 HOLD rows** (rolled up by eventual format):
- Format B variants (incl. "Watch-careful" / "after VD check-in"): 13
- CEO Letter + Call Commitment variants: 11
- Format A (incl. "after CSM check-in"): 6
- Good-News Notice variants (incl. "after CSM touchpoint" / "after renewal-date confirm"): 7
- CEO-Led Entity Pre-Engagement → Coordinated Notices: 5 HOLD rows tagged with this `post_hold_action` in the 2026-05-22 routing-CSV snapshot (3 HVLG, 1 WAC, 1 Coleto — see §1.6). NOTE (2026-05-26): the total entity-packet program scope per `_master-entity-data-v6.2.csv` Master Entity tab is **14 entities** (13 rollup + 1 standalone_multi_org); the additional 9 entities have routing-CSV rows that were non-HOLD or carried other `post_hold_action` labels in the 2026-05-22 snapshot. §1.6 is the canonical scope source; this HOLD-row tally is a routing-CSV slice, not the program scope.
- CEO Pre-Call → Format B variants: 2
- NOT migration — separate health intervention: 1
- (remainder are minor format-variant counts that roll up to the above 6 buckets)

**Row-count reconciliation.** 15 + 19 + 9 + 9 + 4 + 2 + 51 = 109. Matches the 109 unique accounts in v6.2 per `_root/02 §8`. The 107 migration-pending count (per `_root/02 §8`) = 109 − 2 (`Already Migrated`).

---

## §5.5 — Additional routing-CSV columns (`hold_condition`, `post_hold_action`, `flags`, `nuances`)

`migration_comm_tiers_2026-05-19.csv` carries four columns beyond `comm_action` that participate in routing decisions:

### `hold_condition`

A free-text explanation of why a row carries `comm_action = HOLD`. Non-blank for all 51 HOLD rows; blank for all 58 non-HOLD rows. Drafters read this column to understand the specific override that fired (entity overlay with named parent, health hold with named band + score, VD-override with named score, annual hold with renewal-date instruction, or some combination). The column is the human-readable equivalent of running the §2 routing-decision flow against the row's other columns; the explanation often names the specific corrective action required to resolve the hold (e.g. "pull renewal date today," "CSM check-in before notice," "entity disambiguation with `ufi` needed").

### `post_hold_action`

A short structured value naming the format the row resolves to once the hold lifts. Non-blank for all 51 HOLD rows; blank for all 58 non-HOLD rows (those rows ARE their `comm_action`). The value uses the same vocabulary as `comm_action` for the four brief formats, plus three additional routing patterns: `CEO Pre-Call → Format B` (matches `comm_action` of the same name); `CEO-Led Entity Pre-Engagement → Coordinated Notices (<entity name>)` (the §1 6th routing pattern); `NOT migration — separate health intervention program` (the Critical-band carve-out documented in §4.2).

Some `post_hold_action` values carry a parenthetical detail (e.g. `CEO Letter + Call Commitment (+$734)` names the Δ MRR; `Format B — Notice + Meeting Offer (Watch-careful)` names a voice-modulation hint per `_root/04 §4.13`; `Good-News Notice (after CSM touchpoint)` names the prerequisite step). The parenthetical is informational; the canonical format name preceding it is what drives the routing decision.

### `flags`

A semicolon-separated list of routing-relevant per-account tags. Non-blank for accounts that carry one or more of the recognized tags. The flag vocabulary observed in the 2026-05-22 CSV snapshot:

| Flag | Meaning | Routing consequence |
|---|---|---|
| `EARLY-ADOPTER-<YEAR>` | Account signed in `<YEAR>` (typically 2011–2016) | Triggers `_root/04 §4.7` early-adopter tenure paragraph in the lede. |
| `VD-OVERRIDE` | `value_delivery_score < 40` | Triggers the §4.2 health override; account is HOLD; eventually routes per `post_hold_action`. |
| `DISCOUNT-CORRECTION` | `migration_driver = platform_discount_correction` (or a related discount-retirement context) | Triggers `_root/04 §4.14` discount-correction lede substitution; informs the §1 Format/CEO Letter selection by `post_hold_action`. |
| `EXPANSION-T1_TO_T2`, `EXPANSION-T2_TO_T3`, `EXPANSION-HOLD` | Account is a potential expansion / upgrade candidate; or expansion is held pending migration completion | Informational for Stage 4+ (after the migration notice lands and a positive signal is confirmed, Format C — expansion — may be queued). The migration notice itself does not surface expansion language (`_root/04 §2.6`). |
| `ANNUAL` | `deal_type = 'Annual'` | Triggers the §4.3 Annual overlay (90-day notice window, Renewal-Based cohort). |
| `INSIGHTS-LAYER` | Account uses the Sales Intelligence add-on (an unpublished premium per `_root/03 §6`) | Informational; the migration notice does NOT name the unpublished SKU per `_root/03 §6` ("never in proactive comms"). |

Drafters surface flag-driven voice modulation in the brief (early-adopter tenure paragraph, discount-correction lede substitution, etc.) but do not write the flag names themselves into client copy. Flags are operator-facing routing context, not customer-facing.

### `nuances`

A free-text column carrying per-account narrative notes that don't fit the other columns — strategic context for the CEO/CSM conversation, prior commitments, sensitivity flags, etc. Read by the drafter to inform tone but not lifted verbatim into the brief (client copy comes from `_root/04` voice rules + `_root/05` driver prose + `_root/03` tier blocks; per-account nuance shapes the lede stat selection and the §health-band voice modulation, not the body text).

### Authority and update protocol

`hold_condition`, `post_hold_action`, `flags`, and `nuances` are owned by the routing CSV maintainer (currently Kylor). Edits to any of these columns are operator decisions captured in `_root/09_changelog.md` only when the change affects a routing rule in `_root/06` or a segment definition in `_root/02`. Per-account narrative edits to `nuances` or descriptive edits to `hold_condition` do not require a changelog entry; structural changes (e.g. a new flag vocabulary tag, a new `post_hold_action` value, a new HOLD condition pattern) do.

---

## §6. The 5 known routing-CSV errata — cross-reference to `_root/02 §7`

Five known errors in `migration_comm_tiers_2026-05-19.csv` are owned and listed by `_root/02 §7`. They are NOT yet baked into the CSV. Until cleanup item `CL-000` lands them (per `_meta/stage3_cleanup.md` — filed and verified 2026-05-22), every routing decision cross-checks against the corrected list below. **`_root/02 §7` is the canonical source.** The list is mirrored here for self-sufficiency at brief-drafting time only; future edits go to `_root/02 §7`.

| `ord_id` | Account | Routing-CSV value | Corrected value (per `_root/02 §7`) | Reason |
|---|---|---|---|---|
| `rac` | Godinger | `CEO Letter + Call Commitment` | `CEO Pre-Call → Format B` | Δ +$734/mo ≥ $600 ownership boundary. |
| `wac` | WAC Group | `CEO Letter + Call Commitment` | `CEO Pre-Call → Format B` | Δ +$744/mo ≥ $600 ownership boundary. |
| `sbl` | WAC Group | `CEO Letter + Call Commitment` | `CEO Pre-Call → Format B` | Δ +$672/mo ≥ $600 ownership boundary. |
| `big` | Baker-McGuire | (listed in CSV as `ufi`) | `HOLD — VD Override` (entity disambiguation needed) | `value_delivery_score = 33.3` triggers the §4.2 health override; entity disambiguation with Samson Holdings / `ufi` required before send. |
| `kl` | Coleto Brands \| Kichler | `Annual` (in `deal_type`) | `Monthly` | CSV `deal_type` error — only `prog` (Coleto Brands \| Progress Lighting) is Annual in v6.2. |

The corrected value wins over the CSV value at every routing decision. Drafters who encounter one of these five `ord_id`s in the routing CSV use the corrected value above, not the CSV value. Any new erratum discovered downstream goes into `_root/02 §7` first, then this mirror table is updated to match (and the update is logged per `_root/09_changelog.md`).

---

## §7. Output folder mapping — cross-reference to `_root/07 §6`

The per-format output folder is owned by `_root/07 §6`. The four main folders are mirrored here for self-sufficiency:

| Format / routing pattern | Output folder |
|---|---|
| Format A — 60-Day Notice | `Pricing Migration/format-a-notices/` |
| Format B — Notice + Meeting | `Pricing Migration/format-b-notices/` |
| CEO Letter + Call Commitment | `Pricing Migration/ceo-letter-notices/` |
| Good-News Notice | `Pricing Migration/good-news-notices/` |
| CEO Pre-Call → Format B | `Pricing Migration/format-b-notices/` (with `CEO awareness required before send: YES` flag in the routing block per `_root/07 §7`) |

The file-naming pattern, the versioned re-run convention (`__v2`, `__v3`), and the routing-block field list per format are all owned by `_root/07 §6 + §7`. Drafters reference `_root/07` for those; this doc owns only the format → folder mapping above.

---

## §8. What this doc does NOT own

The following live in other root docs. References here should point there, not duplicate the rules:

- Segment definitions, account counts, the $200 / $400 / $600 ownership-boundary rationale, entity overlay rule, health-override triggers, annual overlay, cohort assignment, the 5 errata list itself, and the 109 / 107 / 2 reconciliation → `_root/02`.
- Voice / tone rules for each format's lede and close, including the verbatim close text for all four formats, the formal-notice line, the §4.13 Watch-band lede override, and the §4.14 discount-correction lede substitution → `_root/04` (especially §4.12 and §4.13).
- The "Why the Number Is Changing" per-driver prose that goes into the brief body → `_root/05`.
- The verbatim "What You're Getting at $X" tier blocks, the customer-facing user-rate ladder, the "What's Coming in 2026" roadmap block, and the implementation-fee table → `_root/03`.
- v6.2 column meanings, the canonical loader, the Postgres MCP queries, the fallback rules, the file-naming convention, the per-format output folders themselves, and the canonical routing-block field list → `_root/07`.
- The pre-send quality checklist → `_root/08`. The conformance-block format → `_root/00_manifest.md §5`.

---

*Cross-references: `_root/02 §3` (entity overlay), §4 (health override), §5 (annual overlay), §7 (the 5 errata — canonical source), §8 (109/107/2 reconciliation); `_root/04 §4.12` (close variants by format), §4.13 (health-band lede overrides); `_root/07 §3` (loader filter + ghost / already-migrated skip), §6 (output-folder mapping — canonical source), §7 (routing-block field list per format); exec plan v3.3 §III (60-day notice architecture + Annual handling), §IV (cohort summary), §V (segment-by-segment playbooks), §VI (two-axis artifact composition).*
