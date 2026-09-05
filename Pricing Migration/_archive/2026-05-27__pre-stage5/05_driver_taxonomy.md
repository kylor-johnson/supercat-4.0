# 05 — Driver Taxonomy

> **What this doc owns**: The 11 `migration_driver` values that appear in v6.2 (8 increase-side + 3 decrease-side), with the canonical "Why the Number Is Changing" prose for each — preserved verbatim from the four archived brief templates (Format A, Format B, CEO Letter, Good News). The per-driver pricing-table row template that the brief renders directly under the prose. The conditional sub-blocks each driver carries (`[IF trailing avg users ≤ new included base…]`, `[IF secondary driver = …]`, etc.). The secondary-driver weaving matrix for the 9 primary-secondary combinations v6.2 actually exhibits (post-CL-026 / CL-023 / CL-027 joint resolution 2026-05-26). The pointers from each driver block to the voice rules in `_root/04` (billing-basis footnote, platform-base-grown sentence, IUR fork close, early-adopter tenure paragraph, platform-base conditional inside URN). The `already_migrated` anomaly flag.
>
> **What this doc DOES NOT own**: Voice rules governing HOW the driver block reads (`_root/04` — especially §4.5, §4.6, §4.7, §4.9, §4.10, §4.14). The tier-feature paragraph that follows the driver block ("What You're Getting at $X") (`_root/03 §1`). Segment definitions and ownership boundaries (`_root/02`). Which format a driver routes to — delta thresholds, CEO involvement gates (`_root/06`). The v6.2 data fields each driver dispatches on (`_root/07 §2`). The per-draft quality-bar check that confirms the right block was selected (`_root/08`).
>
> **Last updated**: 2026-05-27 (**CL-029 + CL-030 RESOLVED at source via Source-fix Session D 2026-05-27** — operator-stamped Stage 4 prep Session C audit-pass trims applied. CL-029: F1 + F2 conversational debug language trim at §2.4.1 line 349 + §2.4.7 line 429 (cut `bcf` parenthetical from 9-account TBI+IUR enumeration; cut "Wait — `bcf` was re-stamped..." sentence; cross-refs preserved via §2.4.7 → §4 weaving matrix row 5 pointer). CL-030: F9+F10+F16 §4 weaving matrix full rebuild from `csv.DictReader` ground truth (9→23 rows; aggregate 83→107 reconciles to §1.1 driver-inventory totals 38+10+13+6+9+2+17+1+8+2+1=107) + §2.4.7 line 424 stale "21 occurrences" cross-reference fix → cites §4 matrix row directly. No v6.2 CSV re-stamps (rule-layer-only). Matrix rebuild closes a CL-027 propagation gap (`bcf` double-counting in TBI cohort) + 4 stale-number drifts (rows 1+2+6+7+8+9) + 14 missing-row drifts (PDC enumerated + IUR+ADR + ABTS + SA + MC + UCV + RA + others). Two AFTER-prose-template reconciliations during rebuild (CSV-canonical): URN+IUR row count "26 (25 R + 1 E)" → "20 (19 R + 1 E)" matching footer aggregate; `pre_discount_correction` typo → canonical `platform_discount_correction`. Prior 2026-05-26 entry: **CL-027 RESOLVED at source via Option A operator stamp 2026-05-26** — Stage 4.2 `sca` (Shadow Catchers) production-proof drafter subagent hard-stop closeout per `_root/CONTRACTS.md §2`: drafter surfaced source-layer gap at §2.1.2 Format B URN canonical block (single expansion-baked `[IF excess users remain after new included base]` sub-block produced direction-inverted prose for URN-primary + IUR-secondary reduction-direction accounts — 25 of 26 URN+IUR-secondary v6.2 accounts; legacy 25 → new 10 T1 / 25 → 15 T2). CL-027 source-fix: added parallel `[IF excess users remain AND secondary driver = included_user_reduction (base shrinking)]` sub-block to §2.1.2 mirroring the pre-existing §2.1.3 CEO Letter pattern ("Your included base is also adjusting from the legacy [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED]" — direction-neutral "adjusting" prose); tightened existing §2.1.2 marker to specify EXPANSION-direction (matching §2.1.3 line 120 pattern); §2.1.7 routing rewritten to enumerate the 26-account URN+IUR-secondary cohort (25 reduction + 1 expansion = `bcf`); §2.4.1 primary-vs-secondary semantic stamp extended to cover §2.1.2 / §2.1.3 alongside §2.3.2 / §2.3.3 (URN-side closeout of the CL-026 / CL-023 / CL-027 sequence); §2.4.7 cross-reference paragraph extended to enumerate URN-primary cohort + cross-reference §2.1.2 reduction-aware sub-block; §4 weaving matrix row 5 (`user_rate_normalization, included_user_reduction`) re-tallied 7 → 26 with named enumeration; §4 footer cumulative-occurrences aggregation updated 7-row → 9-row × occurrences = 83 total v6.2-exhibited combination occurrences. Planning-agent self-corrections logged: (1) sca paste-ready pre-flight observation 2 was wrong (claimed §2.1.7 sub-block describes "legacy-allotment-reducing-to-new-tier-standard" — actual §2.1.7 pre-CL-027 routed URN+IUR-secondary to §2.1.2's expansion-only sub-block; conflated IUR-primary §2.4.x reduction-orientation with URN+IUR-secondary §2.1.7 routing); (2) CL-026 / CL-023 joint resolution 2026-05-26 had a scope-gap (TBI-side only; URN-side §2.1.x / §2.1.7 never inspected; §4 matrix URN+IUR-secondary count "7" was stale). Drafter caught both via CL-024 paste-verification discipline + direct source-read against `_root/05`. Prior 2026-05-26 entry: Stage 4.2 `bri` production-proof hard-stop closeout — CL-026 + CL-023 jointly RESOLVED at source via Option A operator stamp 2026-05-26: §2.4.1 primary-vs-secondary semantic scope paragraph appended [IUR-as-secondary semantic widened to "any included-base move (expansion OR reduction)"; IUR count 11→10 after `bri` re-stamp]; §2.4.7 cross-reference paragraph appended [9-account expansion cluster enumerated]; §2.3.2 CL-012-RESOLVED explainer extended with CL-023/CL-026 joint-resolution annotation; §2.3.7 fully rewritten — TBI secondary-driver integration documents 9-account expansion cluster + sccon's compound secondary stamp + audit-trail of CL-023→CL-026 joint resolution; §4 secondary-driver weaving matrix expanded from 7→9 combinations (adds TBI+IUR 9-occ + TBI+MOR-IUR 1-occ rows; corrects MOR+URN 2→1 after sccon re-code). v6.2 row 65 (`bri`) re-stamped `migration_driver` IUR→TBI + `secondary_drivers` blank→`included_user_reduction`; row 101 (`bcf`) re-stamped `migration_driver` ABTS→URN + `secondary_drivers` blank→`included_user_reduction`; 7 of 8 CL-023 rows (`ihw`/`ali`/`vic`/`ih`/`fc`/`ta`/`sbmh`) `secondary_drivers` re-coded URN→IUR; `sccon` (8th CL-023 row) `secondary_drivers` re-coded preserving MOR annotation per entity-child judgment. Prior 2026-05-26 entry: Stage 4.1 lpf production proof closeout — §2.1.5 After-row canonicality paragraph appended (CL-025 RESOLVED). Prior 2026-05-26 entry: CL-012 + CL-016 source fixes applied during Stage 3.2 review pass — §2.3.2 + §2.3.3 secondary-driver marker amended from URN to IUR per operator stamp; §2.3.7 integration note revised + CL-023 filed for v6.2 re-evaluation of TBI+URN rows; §2.6.2 + §2.6.3 canonical MOR blocks extended with `[IF secondary driver = included_user_reduction]` templated sub-block per operator stamp; §2.6.6 billing-basis footnote bullet updated to reflect the new sub-block; §2.6.7 entries revised. Prior 2026-05-26 entry: CL-013 cleanup at §2.5.4.)
> **Owner**: CEO
> **Primary sources**: archived `_handoff-prompt.md` §Driver Framing + §Format Routing Rules; archived Format A / Format B / CEO Letter / Good News brief templates (per-driver `**DRIVER:` blocks); archived per-account exemplars (kal, kii, ih, da, pf); `_master-account-data-v6.2.csv` (driver counts inlined in Wave 3.1 prompt §2)
> **Supersedes**: per-driver narrative content previously scattered across the four archived brief templates. After this doc lands, Stage 3 templates reference `_root/05` by section number, not by inline restatement.

---

## Section 1 — Driver inventory and the primary-vs-secondary rule

### §1.1 The 11 driver values in v6.2

The system carries **11 distinct `migration_driver` values across 109 accounts** in `_master-account-data-v6.2.csv` (count: deduped, 2026-05-22). The values group as 8 increase-side, 3 decrease-side, plus one status-marker leak (`already_migrated` — see §1.4).

**Increase-side drivers** (96 of 107 pending accounts — `delta_mrr > 0`):

| `migration_driver` | Pending accounts | Notes |
|---|---:|---|
| `user_rate_normalization` | 38 | Most common driver. Per-user rate locked at signing; moving to graduated standard ladder. (Post-CL-026 / CL-023 joint resolution 2026-05-26: `bcf` re-stamped ABTS→URN as the 38th URN-primary row.) |
| `platform_discount_correction` | 17 | Signing-time discount being retired across all accounts. Triggers `_root/04 §4.14` lede substitution. |
| `tier_base_increase` | 13 | Platform base moved from old book rate to current tier standard. Tier unchanged, only the rate. (Post-CL-026 / CL-023 joint resolution 2026-05-26: `bri` re-stamped IUR→TBI as the 13th TBI-primary row.) |
| `included_user_reduction` | 10 | Legacy expanded user allotment normalizing to current tier standard. Triggers IUR fork in `_root/04 §4.5`, billing-basis footnote `_root/04 §4.9`. (Post-CL-026 / CL-023 joint resolution 2026-05-26: count 11→10 after `bri` re-stamping out per primary-vs-secondary semantic clarification at §2.4.1.) |
| `at_book_tier_shift` | 9 | Account already at book rate; minor adjustment. Near-zero delta typical. (Post-CL-026 / CL-023 joint resolution 2026-05-26: count 10→9 after `bcf` re-stamping out per §2.5.1 not-at-book signature mismatch; `kii` retained per `_root/05 §2.5.6` documented down-move special case.) |
| `multi_org_retirement` | 6 | Multi-organization pricing program being retired; each entity moves to individual standard. |
| `annual_discount_retirement` | 2 | Annual commitment discount being retired; standard monthly rate going forward. |
| `special_arrangement` | 1 | Custom arrangement to standard. Delta-dependent CEO involvement. |

**Decrease-side drivers** (11 of 107 pending accounts — `delta_mrr < 0` — distributed across 6 Tailwind + 3 Annual + 2 Strategic segments):

| `migration_driver` | Pending accounts | Notes |
|---|---:|---|
| `module_compression` | 8 | Separate module charges consolidating to a single tier subscription — lower combined rate. Account distribution: Tailwind segment (ml, gc, dccl, pf — 4 accounts), Annual segment (mali, mah — 2 accounts), Strategic segment (ap, mfc — 2 accounts). Named in `_handoff-prompt.md` §Driver Framing and `_root/04 §5`. The 4 Strategic / Annual MC accounts are NOT in Tailwind because the entity / health / annual overlays (per `_root/02 §3`–§5 + `_root/06 §2`) supersede the Tailwind segment label — MC is the underlying mechanic, segment routing is the operational overlay. |
| `user_count_variance` | 2 (rw, jyc — both Tailwind) | Current billed users above 6-month trailing average; user count being aligned to trailing actuals. **NOT** in `_handoff-prompt.md` §Driver Framing — see §3.5 flag. |
| `rate_architecture` | 1 (mlg — Minka Lighting Group, Annual segment) | Per-user rate set at legacy structure; recalculated rate produces a lower invoice. **NOT** in `_handoff-prompt.md` §Driver Framing — see §3.5 flag. Account is in Annual segment but has negative delta (−$38/mo). |

Reconciliation: 96 increase-side + 11 decrease-side = 107 pending. Plus 2 already_migrated (`tcs`, `drf`) = 109 total v6.2 rows. Cross-references `_root/02 §1` (Tailwind segment = 6 accounts; the 5 non-Tailwind decrease accounts route to their override-driven segment) and `_root/02 §8` (109 / 107 / 2 reconciliation). The 6 Tailwind decreases comprise the 4 Tailwind MC accounts (ml, gc, dccl, pf) + 2 UCV accounts (rw, jyc). The 3 Annual decreases comprise 2 MC accounts (mali, mah) + 1 RA account (mlg). The 2 Strategic decreases are both MC accounts (ap, mfc).

### §1.2 Primary driver is authoritative — v6.2 wins on conflict

Per archived `_handoff-prompt.md` §Driver Framing: **always use `migration_driver` from `_master-account-data-v6.2.csv`. If v6.2 CSV and the HTML revenue model (`_reference/migration_revenue_model_2026-05-14.html`, abbreviated key `d`) disagree on the driver, v6.2 wins.** This is consistent with the source-of-truth hierarchy in `_root/07 §1`.

The drafter does not infer the driver from the pricing-breakdown fields. The v6.2 `migration_driver` value selects the §2 or §3 block; the drafter copies the block prose verbatim and substitutes `[BRACKETED_TOKENS]` from v6.2 + Postgres data per `_root/07 §2`.

### §1.3 Secondary drivers are woven into the primary block — never a separate section

The `secondary_drivers` field in v6.2 is a pipe-separated list of 1–2 additional driver names. Per archived `_handoff-prompt.md` §Driver Framing and `_root/04 §5`: **`secondary_drivers` add as supporting context within the primary driver block — never as a separate section.**

The 9 primary-secondary combinations v6.2 actually exhibits (and how each integrates) live in §4 (post-CL-026 / CL-023 / CL-027 joint resolution 2026-05-26 — the count was 7 pre-CL-026; CL-026 / CL-023 added the 2 TBI-primary combinations; CL-027 re-tallied URN+IUR-secondary occurrences 7 → 26 without adding a new combination row). Stage 4 drafters: pick the primary block from §2 or §3, then consult §4 for the secondary integration sub-paragraph (if any). Do not author a "Secondary Drivers" heading in the brief.

### §1.4 The `already_migrated` anomaly

Two rows in v6.2 carry `migration_driver = 'already_migrated'`: `tcs` (CopperSmith, T3 Annual) and `drf` (Dorell Fabrics, T1). Both rows also carry `migration_status = 'already_migrated'`.

This is a **status-marker leak into the driver field**, not a real driver. Per `_root/07 §3`, the v6.2 loader's call-site filter skips rows whose `migration_status = 'already_migrated'`, so these accounts never reach a brief drafter. Per `_root/02 §8`, they are excluded from the 107-pending count.

`_root/05` does not author a driver block for `already_migrated`. The anomaly is documented here so a future agent who sees the value in the CSV does not invent prose for it.

---

## Section 2 — Increase-side drivers

The 8 increase-side driver subsections below are ordered by v6.2 pending-account count, descending. Each subsection follows the same skeleton: definition, Format B canonical block (verbatim), CEO Letter canonical block (verbatim), Format A canonical block (verbatim or "not carried — forward to Format B"), pricing-table row template, conditional context paragraphs, secondary-driver integration.

The driver-prose blocks below are **rendered as Markdown blockquotes**. The conditional markers `[IF ...:]` and `[REQUIRED when ...]` are part of the template's drafter-facing scaffolding and are preserved exactly as the templates render them.

---

### §2.1 — `user_rate_normalization` (38 pending accounts — most common; post-CL-026 / CL-023 joint resolution 2026-05-26)

#### §2.1.1 Definition

The per-user rate was locked at signing and has not been updated to the current standard ladder. Going forward, every account moves to the graduated user-rate ladder (`_root/03 §2 Block A` — 1–10 / 11–25 / 26–50 / 51+ at $25/$22/$20/$18). The v6.2 field signature: `current_user_rate ≠ standard_ladder_rate_for_band` (typically a flat $15 or $20 below the ladder's first band of $25). 38 of 107 pending accounts (the most common single driver; count was 37 pre-CL-026 / CL-023 joint resolution 2026-05-26 — `bcf` re-stamped ABTS→URN added the 38th row). Often co-occurs with `included_user_reduction` as secondary (see §4 row 5 — **26 accounts have URN primary + IUR secondary post-CL-026 / CL-023 / CL-027 joint resolution 2026-05-26**: 25 REDUCTION-direction (`sca` + 24 others; legacy `provided=25 > new included=10` T1 dominant + 25→15 T2) + 1 EXPANSION-direction (`bcf` row 101 — re-stamped from ABTS-primary; legacy `provided=25 < new included=40` T3 outlier). The §2.1.2 Format B canonical block carries TWO direction-specific sub-blocks post-CL-027 (line 98 expansion-direction "expanding from" prose; line 101 reduction-direction "adjusting from the legacy ... to the current [TIER] standard" prose); see §2.1.7 for full enumeration + §4 weaving matrix row 5 for routing.

#### §2.1.2 Format B canonical block (verbatim)

> Your additional-user rate has been **$[LEGACY_USER_RATE]/user** since your account was set up in [YEAR]. That rate reflects the pricing in place at signing — it hasn't been updated to the current standard. Going forward, every account moves to the same graduated user structure.
>
> [REQUIRED when Before platform base ≠ After platform base — always include:]
> Your platform base is also moving from $[LEGACY_BASE] to $[NEW_BASE] — this is the current [TIER] standard.
>
> The new user pricing follows a graduated curve applied consistently across all accounts:
>
> | Additional users above included base | Rate |
> |---|---|
> | 1–10 excess users | $25/user |
> | 11–25 excess users | $22/user |
> | 26–50 excess users | $20/user |
> | 51+ excess users | $18/user |
>
> [IF trailing avg users ≤ new included base — user charge goes to $0:]
> Your included user base is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]. With [TRAILING_AVG] average users, all of your users are now covered within the included base — your user charge goes to $0/month.
>
> [IF excess users remain AND new included base > legacy included base (base expanding):]
> Your included user base is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED] — absorbing [N] users who no longer generate a charge. The remaining [NEW_EXCESS] excess users are billed at the graduated rate: [EXCESS_MATH_BREAKDOWN] = $[NEW_USER_CHARGE]/month.
>
> [IF excess users remain AND secondary driver = included_user_reduction (base shrinking from legacy to current tier standard):]
> Your included base is also adjusting from the legacy [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED]. With [TRAILING_AVG] average users, [NEW_EXCESS] are now above the [NEW_INCLUDED]-user included base, billed at the graduated rate: [EXCESS_MATH_BREAKDOWN] = $[NEW_USER_CHARGE]/month.

(CL-027 RESOLVED 2026-05-26 at source per operator stamp — added the third sub-block above to mirror the §2.1.3 CEO Letter pattern. The original §2.1.2 carried a single `[IF excess users remain after new included base]` marker with expansion-baked prose ("expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]") that produced direction-inverted copy for URN-primary + IUR-secondary reduction-direction accounts (25 of 26 URN+IUR-secondary v6.2 accounts: legacy 25 → new 10 for T1, 25 → 15 for T2). Surfaced by the Stage 4.2 `sca` (Shadow Catchers) production-proof drafter subagent hard-stop 2026-05-26 per `_root/CONTRACTS.md §2`. The CL-026 / CL-023 joint-resolution Option A semantic clarification at §2.4.1 was scoped to TBI-side §2.3.2 / §2.3.3 only; URN-side §2.1.2 / §2.1.3 were never re-scoped — CL-027 closes that scope-gap. The marker name `included_user_reduction` is preserved (no rename) per the same Option A operator stamp; the direction-specific sub-block prose carries the resolution. **Mutual-exclusivity rule (inherited from §2.1.3 CL-012 RESOLVED pattern; CL-027 codifies it for §2.1.2)**: the two `[IF excess users remain ...]` sub-blocks at lines 98 and 101 are mutually exclusive — the parenthetical conditions "(base expanding)" and "(base shrinking from legacy to current tier standard)" function as operational gates, not cosmetic clarifications. Drafter reads them as: line 98 fires iff `new_included_base > legacy_included_base` (direction-pure expansion gate; secondary-driver value not checked); line 101 fires iff `new_included_base < legacy_included_base AND secondary_driver = included_user_reduction` (compound gate; both conditions required). For accounts where `new_included = legacy_included` (no included-base move), neither sub-block fires — only the zero-excess sub-block at line 95 or no sub-block at all (URN-without-IUR no-base-move case). For `bcf` (Braxton Culler — the v6.2 outlier: URN-primary + IUR-secondary + 25 → 40 EXPANSION direction): line 98 fires; line 101 does NOT fire despite `secondary_driver = IUR` because `40 < 25` is FALSE (parenthetical gate). For sca + 24 other reduction-direction URN+IUR-secondary accounts: line 101 fires; line 98 does NOT fire because `10 > 25` is FALSE. See `_meta/stage3_cleanup.md` CL-027 RESOLVED entry.)

#### §2.1.3 CEO Letter canonical block (verbatim)

> Your additional-user rate has been **$[LEGACY_USER_RATE]/user** since your account was set up in [YEAR]. That rate was locked in at signing and hasn't been updated to the current rate card. We're standardizing all accounts to the same graduated structure as part of this refresh.
>
> [IF platform base also changes alongside the user rate (Before platform base ≠ After platform base) — add this sentence:]
> Your platform base is also standardizing from $[LEGACY_BASE] to the current [TIER] rate of $[NEW_BASE] — this reflects the move from legacy module pricing to the current bundled tier structure.
>
> The new user pricing follows a graduated curve applied consistently across all accounts:
>
> | Additional users above included base | Rate |
> |---|---|
> | 1–10 excess users | $25/user |
> | 11–25 excess users | $22/user |
> | 26–50 excess users | $20/user |
> | 51+ excess users | $18/user |
>
> [IF trailing avg users ≤ new included base — user charge goes to $0:]
> Your included user base is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]. With [TRAILING_AVG] average users, all of your users are now covered within the included base — your user charge goes to $0/month.
>
> [IF excess users remain AND new included base > legacy included base (base expanding):]
> Your included user base is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED] — absorbing [N] users who no longer generate a charge. The remaining [NEW_EXCESS] excess users are billed at the graduated rate: [EXCESS_MATH_BREAKDOWN] = $[NEW_USER_CHARGE]/month.
>
> [IF excess users remain AND secondary driver = included_user_reduction (base shrinking from legacy to current tier standard):]
> Your included base is also adjusting from the legacy [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED]. With [TRAILING_AVG] average users, [NEW_EXCESS] are now above the [NEW_INCLUDED]-user included base, billed at the graduated rate: [EXCESS_MATH_BREAKDOWN] = $[NEW_USER_CHARGE]/month.

#### §2.1.4 Format A canonical block (verbatim)

> Your additional-user rate has been **$[LEGACY_USER_RATE]/user** since your account was set up in [YEAR]. That rate reflects the pricing in place at signing — it hasn't been updated to the current standard. Going forward, every account moves to the same graduated user structure.
>
> The new user pricing follows a graduated curve applied consistently across all accounts:
>
> | Additional users above included base | Rate |
> |---|---|
> | 1–10 excess users | $25/user |
> | 11–25 excess users | $22/user |
> | 26–50 excess users | $20/user |
> | 51+ excess users | $18/user |
>
> Here's how that plays out for your account:
>
> [Pricing-table row template — see §2.1.5]
>
> [Optional: If the included-base expansion absorbs users: "The new included base absorbs [N] of your current additional users — those users no longer generate a charge. The net effect on your user charges is [+/–$X/month]."]

(Format A's URN block omits the conditional sub-blocks Format B and CEO Letter carry — Format A's mechanical scope is delta ≤ 10% / ≤ $80, so the simpler near-flat framing is intentional. The "Optional" follow-up sentence is the Format A equivalent of the conditional excess-users paragraph in the longer formats.)

#### §2.1.5 Pricing-table row template

The "Why the Number Is Changing" prose is followed directly by this table (identical across Format A, Format B, and CEO Letter for URN):

```
| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] | $[NEW_BASE] ([TIER]) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS] users at $[LEGACY_RATE] = **$[LEGACY_USER_CHARGE]/month** | [NEW_EXCESS] users at graduated rate = **$[NEW_USER_CHARGE]/month** |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |
```

Followed (Format B and CEO Letter only) by the billing-basis footnote — verbatim per `_root/04 §4.9`.

**After-row canonicality (operator-stamped 2026-05-26, Stage 4.1 `lpf` production proof finding)**: the `[NEW_EXCESS]` value in the row template above = v6.2 `excess_users` (modeled-canonical per `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix B). The `[NEW_USER_CHARGE]` value = v6.2 `user_charge` (computed by v6.2 at the graduated-rate ladder in `_root/03 §2 Block A` against `modeled_users − included_users`). Where v6.2 `modeled_users` ≠ billing-implied enabled count (per `_root/07 §4.5` reconciliation flag), the gap is resolved via INTERNAL ops cleanup pre-`[EFFECTIVE_DATE]`; the brief's After-row math stands as v6.2 stamps it. Drafters do NOT recompute `[NEW_EXCESS]` from billing-derived enabled count; that path violates Appendix B canonicality and is reserved for v6.2 re-stamps (operator action only). The `[LEGACY_EXCESS]` and `[LEGACY_USER_CHARGE]` values in the Before column DO derive from current billing math (the customer's actual today-invoice values) — the modeled-canonical discipline applies only to After-row.

#### §2.1.6 Conditional context paragraphs

For URN, the following paragraphs may follow the table — text is owned by `_root/04`, not restated here:

- **Billing-basis footnote** (italicized, immediately after the table, before the next `---` separator) — required for every URN brief. Verbatim sentence in `_root/04 §4.9`.
- **Platform-base-grown sentence** (when `new_tier_base > current_platform_mrr`) — required regardless of which driver is primary. Verbatim sentence in `_root/04 §4.6`. Cohort-year token populated from v6.2 `cohort_year`.
- **Platform-base conditional inside the URN block** (when Before platform base ≠ After platform base) — required. Format B variant in `_root/04 §4.10`; CEO Letter variant in `_root/04 §4.10`. The Format B and CEO Letter blocks above already carry the bracketed `[REQUIRED when Before platform base ≠ After platform base...]` / `[IF platform base also changes...]` markers — those bracketed conditional sentences are the §4.10 verbatim text.
- **Early-adopter tenure paragraph** (when `cohort_year ≤ 2015`) — required. Format B and CEO Letter variants in `_root/04 §4.7`. This paragraph lands in or after the lede, not inside the URN block itself; the URN block is unchanged for early-adopter cohorts.
- **IUR-variant close** (when secondary = `included_user_reduction`) — required. Replaces the default "only thing changing" close. Verbatim sentence in `_root/04 §4.5` IUR variant.

#### §2.1.7 Secondary-driver integration

URN appears as primary with the following secondaries in v6.2:

- **`included_user_reduction` secondary (26 occurrences in v6.2 post-CL-026 / CL-023 / CL-027 joint resolution 2026-05-26; was stale at "7" pre-CL-027 — the re-tally is the joint resolution's URN-side closeout).** The 26 accounts split into 2 direction-shape sub-cohorts per the §2.4.1 primary-vs-secondary semantic scope:
  - **25 REDUCTION-direction** (legacy `provided > new included`; T1 25→10 dominant pattern + T2 25→15): `sca` (Shadow Catchers — Stage 4.2 production-proof catalyst for CL-027 source-fix), `wac` / `sbl` / `fms` / `tla` / `mli` / `vcg` (6 with compound `multi_org_retirement, included_user_reduction` secondary), `all` / `kl` / `da` / `eglo` / `prog` / `cst` (HOLD-Annual) / `afx` / `dals` / `uhc` / `rf` / `big` / `heb` / `gsa` / `vl` / `cfg` / `mh` / `ah` / `etl` (18 with `included_user_reduction` solo secondary).
  - **1 EXPANSION-direction** (legacy `provided < new included`; 25→40 T3 pattern): `bcf` (Braxton Culler, row 101 — re-stamped 2026-05-26 from ABTS primary to URN primary + IUR secondary per CL-026 / CL-023 joint resolution).
  - **Format B routing (post-CL-027)**: REDUCTION accounts use the `[IF excess users remain AND secondary driver = included_user_reduction (base shrinking from legacy to current tier standard)]` sub-block above (the "Your included base is also adjusting from the legacy [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED]" paragraph — direction-neutral "adjusting" prose); EXPANSION accounts (bcf) use the `[IF excess users remain AND new included base > legacy included base (base expanding)]` sub-block above (the "expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED] — absorbing [N] users" paragraph). The two sub-blocks are mutually exclusive (exactly one fires per account based on direction).
  - **CEO Letter routing** (unchanged; CL-027 closed the §2.1.2 Format B gap to match the pre-existing §2.1.3 CEO Letter pattern): same two-sub-block dispatch — `bcf` uses the §2.1.3 expansion sub-block (line 120 above); any URN+IUR-secondary REDUCTION account routing to CEO Letter ($400 < delta_mrr < $600) uses the §2.1.3 reduction sub-block (line 123 above). No v6.2 URN+IUR-secondary REDUCTION account currently routes CEO Letter — all 25 land in Format B per delta_mrr; `cst` is HOLD-Annual pending health score + renewal date.
  - **Format A**: no secondary-IUR sub-block in template; the operator-judgment "Optional" follow-up sentence stands in (unchanged).
  - Apply IUR-variant close per `_root/04 §4.5` for all 26 (close fork is shape-agnostic — not direction-specific). Apply billing-basis footnote per `_root/04 §4.9` for all 26 (URN-primary fires §4.9 unconditionally; one paste covers both URN-primary and IUR-secondary per §4.9 source text covering excess-user billing universally).

(URN does not co-occur with any other secondary in v6.2 — no `multi_org_retirement | user_rate_normalization`, `annual_discount_retirement | user_rate_normalization`, etc. as primary URN. The reverse direction — URN as secondary under other primaries — is handled in those primary drivers' §X.7.)

---

### §2.2 — `platform_discount_correction` (17 pending accounts)

#### §2.2.1 Definition

A signing-time discount on the platform base is being retired. Legacy account-level discounts are being retired across all accounts; everyone is moving to the same standard tier pricing. The v6.2 field signature: `current_platform_mrr < new_tier_base` for the same tier, with the historical discount documented in `discount_drivers`. 17 of 107 pending accounts. Triggers the lede-sentence substitution per `_root/04 §4.14`.

#### §2.2.2 Format B canonical block (verbatim)

> Your current pricing reflects a discount applied at signing in [YEAR]. As part of this change, legacy account-level discounts are being retired across all accounts. Everyone is moving to the same standard tier pricing. Your new monthly rate is the [TIER] standard rate for your account profile.
>
> [IF no user structure change:]
> The change is entirely on the platform side — your user count and user structure are unchanged.

#### §2.2.3 CEO Letter canonical block (verbatim)

> Your current pricing reflects a discount applied at signing in [YEAR]. As part of this refresh, legacy account-level discounts are being retired across all accounts. Everyone is moving to the same standard tier pricing. Your new monthly rate is the [TIER] standard rate for your account profile.
>
> [IF no user structure change:]
> The change is entirely on the platform side — your user count and user structure are unchanged.

(Difference between Format B and CEO Letter: "as part of this **change**" vs. "as part of this **refresh**." Both are preserved verbatim from the respective archived templates.)

#### §2.2.4 Format A canonical block (verbatim)

The Format A template carries this driver under the name **`discount_correction`** (without the `platform_` prefix). The block prose is:

> Your current pricing reflects a [N%] discount applied at signing in [YEAR]. Going forward, account-level discounts are being retired — every account moves to the same standard tier pricing. Your new monthly rate is the standard rate for your usage profile.

**Naming flag:** v6.2 uses `platform_discount_correction`; Format A template uses `discount_correction`; the archived `_handoff-prompt.md` §Driver Framing uses `platform_discount_correction`. Format A's name is a stale variant. Stage 3 cleanup of the Format A template should update the driver name to `platform_discount_correction` so the template field-matches v6.2. The block prose itself stands as the Format A canonical version. (Surfaced in §6 as an open question for the operator.)

#### §2.2.5 Pricing-table row template

```
| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] ([YEAR] discounted rate) | $[NEW_BASE] ([TIER] standard) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS_DESCRIPTION] | [NEW_EXCESS_DESCRIPTION] |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |
```

Format A's row 1 is phrased slightly differently — `$[LEGACY_BASE] ([N]% below book)` vs. `$[NEW_BASE] (standard)` — preserving the percentage callout. Format A version:

```
| | Before | After |
|---|---|---|
| Platform rate | $[LEGACY_BASE] ([N]% below book) | $[NEW_BASE] (standard) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS] at $[LEGACY_RATE]/user | [NEW_EXCESS] at graduated rate |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |
```

#### §2.2.6 Conditional context paragraphs

For PDC, the following paragraphs may follow the table — text is owned by `_root/04`:

- **Lede-sentence substitution** (`_root/04 §4.14`) — required. Replaces the default "rate at signing" sentence in the lede framing block. Verbatim sentence in `_root/04 §4.14`. Applied in Format A, Format B, and CEO Letter — uniform across formats.
- **Platform-base-grown sentence** (when `new_tier_base > current_platform_mrr`) — required. PDC by definition has `new_tier_base > current_platform_mrr` (the discount is being retired). Verbatim sentence in `_root/04 §4.6`.
- **Early-adopter tenure paragraph** (when `cohort_year ≤ 2015`) — required. Variants in `_root/04 §4.7`.
- **Billing-basis footnote** — **NOT** required for PDC. Per `_root/04 §4.9`, the footnote applies only to URN and IUR blocks; PDC does not turn on enabled-account billing as a primary lever.
- **Default close** (`_root/04 §4.5` default form) — applies unless secondary = `included_user_reduction`.

#### §2.2.7 Secondary-driver integration

PDC does not appear with a secondary driver in v6.2 (the 17 PDC primary rows all have `secondary_drivers` blank). No integration sub-block to author. If a future v6.2 row introduces a PDC primary + secondary combination, the integration is undocumented; flag per `_root/CONTRACTS.md §2`.

---

### §2.3 — `tier_base_increase` (13 pending accounts; post-CL-026 / CL-023 joint resolution 2026-05-26)

#### §2.3.1 Definition

The platform base moved from the old book rate to the current tier standard. The tier itself is unchanged — only the base rate. The v6.2 field signature: `current_platform_mrr < tier_base` for the matching tier, with `current_user_rate` typically already at the standard ladder (the "typically" qualifier accommodates the 8-account CL-023 + bri cohort where `current_user_rate < $25` but the included-base expansion is the integrated mechanic per §2.3.7). 13 of 107 pending accounts (count was 12 pre-CL-026 / CL-023 joint resolution 2026-05-26 — `bri` re-stamped IUR→TBI added the 13th row). Often co-occurs with `included_user_reduction` as secondary (9 accounts have TBI primary + IUR-as-secondary expansion-shape per §4 + §2.3.7 post-resolution; the legacy expanded OR contracted user allotment moves alongside the base move).

#### §2.3.2 Format B canonical block (verbatim)

> When your account was set up in [YEAR], the [TIER] platform was priced at **$[LEGACY_BASE]/month** — the book rate at that time. The current standard rate for this tier is **$[NEW_BASE]/month**. Your invoice is moving to the current standard — your tier isn't changing, only the rate.
>
> [IF secondary driver = included_user_reduction — add this paragraph:]
> Additionally, the included user base for this tier is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED].
>
> [IF trailing avg users ≤ new included base — user charge goes to $0:]
> With your team averaging [TRAILING_AVG] users, everyone is now within the included base — your current user charge of $[LEGACY_USER_CHARGE]/month goes to $0.
>
> [IF excess users remain after new included base:]
> The remaining [NEW_EXCESS] users above the new included base are billed at the graduated rate: [EXCESS_MATH_BREAKDOWN] = $[NEW_USER_CHARGE]/month.

(CL-012 RESOLVED 2026-05-26 at source per operator stamp — the secondary-driver marker was amended from `[IF secondary driver = user_rate_normalization AND included base expands]` to `[IF secondary driver = included_user_reduction]` to match the integrated paragraph's behavior (included-base move). The prior URN-secondary phrasing was a template-prose phrasing inheritance from the archived Format B template; the integration behavior was always IUR-style. See `_root/09_changelog.md` "Stage 3.2 review pass" entry for the source-fix rationale and the follow-on CL-023 filed for v6.2 `secondary_drivers` re-evaluation on TBI rows historically coded with URN secondary. **CL-023 + CL-026 RESOLVED 2026-05-26 jointly via Option A primary-vs-secondary semantic clarification at §2.4.1 + v6.2 re-codes of the 9-account expansion cluster — see `_meta/stage3_cleanup.md` CL-023 / CL-026 RESOLVED entries**. The marker name `included_user_reduction` is preserved (no rename) because the §2.3.2 sub-block prose already accommodates expansion semantics ("expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]"); the marker semantic for secondary use is wider than the §2.4.1 primary definition per CL-026 operator stamp 2026-05-26.)

#### §2.3.3 CEO Letter canonical block (verbatim)

> When your account was set up in [YEAR], the [TIER] platform was priced at **$[LEGACY_BASE]/month** — the book rate at that time. The current standard rate for this tier is **$[NEW_BASE]/month**. Your invoice is moving to the current standard — your tier isn't changing, only the rate.
>
> [IF secondary driver = included_user_reduction — add this paragraph:]
> Additionally, the included user base for this tier is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED].
>
> [IF trailing avg users ≤ new included base — user charge goes to $0:]
> With your team averaging [TRAILING_AVG] users, everyone is now within the included base — your current user charge of $[LEGACY_USER_CHARGE]/month goes to $0.
>
> [IF excess users remain after new included base:]
> The remaining [NEW_EXCESS] users above the new included base are billed at the graduated rate: [EXCESS_MATH_BREAKDOWN] = $[NEW_USER_CHARGE]/month.

(The Format B and CEO Letter `tier_base_increase` blocks are identical character-for-character. CL-012 source fix applied to §2.3.3 in lockstep with §2.3.2 per operator stamp 2026-05-26.)

#### §2.3.4 Format A canonical block

**Format A does not carry a `tier_base_increase` block.** Format A's mechanical scope is delta ≤ 10% / ≤ $80; in practice TBI accounts produce deltas large enough that they route to Format B or CEO Letter and Format A never carries this driver in production.

If a TBI account ever routes to Format A (e.g. a low-delta TBI account at the boundary), the drafter falls back to the Format B block above and trims to Format A's near-flat register per `_root/04 §4.13` and the Format A near-flat tone discipline.

#### §2.3.5 Pricing-table row template

```
| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] ([YEAR] rate) | $[NEW_BASE] ([TIER] standard) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS_DESCRIPTION] | [NEW_EXCESS_DESCRIPTION] |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |
```

#### §2.3.6 Conditional context paragraphs

For TBI, the following paragraphs may follow the table — text is owned by `_root/04`:

- **Platform-base-grown sentence** (when `new_tier_base > current_platform_mrr`) — required. TBI by definition has the base moving up. Verbatim sentence in `_root/04 §4.6`.
- **Early-adopter tenure paragraph** (when `cohort_year ≤ 2015`) — required. Variants in `_root/04 §4.7`.
- **Billing-basis footnote** — **NOT** required for TBI. Applies only to URN and IUR per `_root/04 §4.9`.
- **IUR-variant close** (when secondary = `included_user_reduction`) — required. Verbatim sentence in `_root/04 §4.5` IUR variant.
- **Default close** — applies when no secondary IUR. Verbatim sentence in `_root/04 §4.5` default form.

#### §2.3.7 Secondary-driver integration

TBI appears with the following secondaries in v6.2 (post-CL-026 / CL-023 joint resolution 2026-05-26):

- **`included_user_reduction` secondary (9 occurrences after operator-stamped joint resolution 2026-05-26).** Apply the `[IF secondary driver = included_user_reduction]` sub-block above (the "Additionally, the included user base for this tier is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]" paragraph). The 9 accounts: `bri` (Bulbrite, row 65 — re-stamped from IUR primary 2026-05-26), `bcf` (Braxton Culler, row 101 — re-stamped from ABTS primary 2026-05-26; URN-primary mechanic with included-base expansion side-effect — see §2.4.7 cross-reference for the expansion-case secondary-semantic stamp), `ihw` / `ali` / `vic` / `ih` / `fc` / `ta` / `sbmh` (7 of 8 CL-023 cluster — `secondary_drivers` re-coded `user_rate_normalization` → `included_user_reduction` 2026-05-26 per operator-stamped Option A semantic clarification), `sccon` (Summer Classics Contract, child entity in Summer Classics packet — `secondary_drivers` re-coded `multi_org_retirement, user_rate_normalization` → `multi_org_retirement, included_user_reduction` 2026-05-26 preserving MOR annotation per operator judgment given sccon's entity-child role). All 9 instantiate the 25→40 included-base expansion shape; the sub-block fires for all 9 under the amended marker per CL-012 + the §2.4.1 primary-vs-secondary semantic clarification per CL-026.
- **`multi_org_retirement, included_user_reduction` secondary (1 occurrence; `sccon` only).** Same as above; MOR annotation is preserved per entity-child documentation discipline but does NOT fire any TBI sub-block of its own per `_root/05 §2.6.7` (TBI primary + MOR-secondary is not a templated combination). The `included_user_reduction` portion of the compound secondary stamp fires the §2.3.2 sub-block; the `multi_org_retirement` portion is annotation-only at TBI-primary scope.

Apply IUR-variant close per `_root/04 §4.5` (IUR-as-secondary fork applies — close fork is shape-agnostic, not direction-specific) and billing-basis footnote per `_root/04 §4.9`.

**Pre-resolution context (preserved for audit trail)**: The exemplar `ih__interlude-home` (TBI primary) was historically coded with `secondary_drivers = user_rate_normalization` under the old `[IF secondary driver = user_rate_normalization AND included base expands]` marker (pre-CL-012). After CL-012 amended the marker to `[IF secondary driver = included_user_reduction]`, `ih`'s URN-secondary coding stopped firing the sub-block, prompting CL-023 to file v6.2 maintenance question whether to (a) re-code to IUR-secondary OR (b) handle via per-account narrative integration. CL-026 (Stage 4.2 `bri` production-proof hard-stop 2026-05-26) ran the full-cohort driver-stamp audit + surfaced that `bri` was a 9th member of the same expansion-shape cohort (with the additional twist that `bri` was mis-stamped IUR primary — same expansion shape but with `current_user_rate=$25` already on ladder, so URN-secondary signature did not apply). Operator-stamped CL-023 + CL-026 joint resolution 2026-05-26 = Option A semantic clarification + (a) path re-code (URN → IUR secondary for the 8 CL-023 rows) + bri re-stamped IUR primary → TBI primary + IUR secondary + bcf re-stamped ABTS primary → URN primary + IUR secondary. The §2.3.2 sub-block fires for all 9 under the amended + clarified marker. CL-023 + CL-026 both RESOLVED 2026-05-26 at this §2.3.7 source (+ §2.4.1 primary-vs-secondary clarification + §4 secondary-driver weaving matrix expansion-cluster row).

If v6.2 introduces a TBI primary + URN secondary row going forward (no IUR), the §2.3.2 sub-block does NOT fire; the drafter integrates the URN secondary via per-account narrative per `_root/05 §4` Format B note (the kii exemplar pattern).

---

### §2.4 — `included_user_reduction` (11 pending accounts)

#### §2.4.1 Definition

The legacy expanded user allotment is being normalized to the current tier standard. The included-user count moves from the historical larger value (e.g. 25 on a T1) to the current tier standard (e.g. 10 for T1, 15 for T2, 40 for T3). The v6.2 field signature: `current_provided_users > included_users` for the new tier. **The field signature above applies to PRIMARY `included_user_reduction` stamps only — i.e., genuine reductions where the legacy expanded allotment normalizes downward to current tier standard.** 10 of 107 pending accounts (post-CL-026 / CL-023 joint resolution 2026-05-26 — `bri` row 65 re-stamped from IUR primary to TBI primary + IUR secondary; remaining 10 IUR-primary rows all satisfy the signature). Triggers the IUR fork in `_root/04 §4.5` close and the billing-basis footnote per `_root/04 §4.9`.

**Primary-vs-secondary semantic scope (CL-026 operator-stamped 2026-05-26; URN-side closeout per CL-027 operator-stamped 2026-05-26)**: When `included_user_reduction` appears as a SECONDARY stamp (in `secondary_drivers`), the marker semantic is wider than the primary definition: it means *any included-base move (expansion OR reduction)*. The semantic covers TWO v6.2 sub-cohorts:

- **TBI-primary + IUR-secondary (9 accounts; expansion-shape 25→40)** — `bri` (row 65, re-stamped from IUR primary 2026-05-26) + 8 CL-023 cluster (`ihw`/`sccon`/`ali`/`vic`/`ih`/`fc`/`ta`/`sbmh`). Integrated at §2.3.2 / §2.3.3 sub-block ("Additionally, the included user base for this tier is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]" — expansion-baked prose accommodates the 25→40 shape directly). See §2.3.7 for full enumeration + §4 weaving matrix row 3.
- **URN-primary + IUR-secondary (26 accounts; 25 REDUCTION-shape 25→10 + 1 EXPANSION-shape 25→40 = `bcf`)** — added per CL-027 RESOLVED 2026-05-26. Integrated at §2.1.2 / §2.1.3 via TWO direction-specific sub-blocks (post-CL-027 source-fix at §2.1.2): REDUCTION uses "Your included base is also adjusting from the legacy [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED]" (direction-neutral "adjusting" prose); EXPANSION (bcf) uses "expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED] — absorbing [N] users" (the existing expansion-baked sub-block, unchanged). See §2.1.7 for full enumeration + §4 weaving matrix row 5.

The marker name `included_user_reduction` semantically lags the marker behavior for the secondary case across both cohorts, but resolution is via this primary-vs-secondary clarification rather than a marker rename (Option A operator-stamped 2026-05-26 at CL-026 / CL-023 / CL-027 joint resolution sequence; Options B / C / D rescinded; lowest-cost path validated by the §2.3.2 sub-block prose already accommodating expansion semantics + the §2.1.2 / §2.1.3 sub-block pair now accommodating both directions post-CL-027). See `_meta/stage3_cleanup.md` CL-026 + CL-023 + CL-027 RESOLVED entries.

#### §2.4.2 Format B canonical block (verbatim)

> Your account was set up with **[LEGACY_INCLUDED] included users** in [YEAR] — more than the [NEW_INCLUDED] users standard for the [TIER] tier. That expanded allotment was part of your original arrangement. As part of this change, the included base is moving to the current [TIER] standard.
>
> The new user pricing follows a graduated curve applied consistently across all accounts:
>
> | Additional users above included base | Rate |
> |---|---|
> | 1–10 excess users | $25/user |
> | 11–25 excess users | $22/user |
> | 26–50 excess users | $20/user |
> | 51+ excess users | $18/user |
>
> [IF secondary driver = user_rate_normalization — add:]
> Your per-user rate is also moving from **$[LEGACY_USER_RATE]/user** to the current graduated standard.
>
> With [TRAILING_AVG] average users, [NEW_EXCESS] users are now above the [NEW_INCLUDED]-user included base, billed at the graduated rate: [EXCESS_MATH_BREAKDOWN] = $[NEW_USER_CHARGE]/month.

#### §2.4.3 CEO Letter canonical block (verbatim)

> Your account was set up with **[LEGACY_INCLUDED] included users** in [YEAR] — more than the [NEW_INCLUDED] users standard for the [TIER] tier. That expanded allotment was part of your original arrangement. As part of this refresh, the included base is moving to the current [TIER] standard.
>
> The new user pricing follows a graduated curve applied consistently across all accounts:
>
> | Additional users above included base | Rate |
> |---|---|
> | 1–10 excess users | $25/user |
> | 11–25 excess users | $22/user |
> | 26–50 excess users | $20/user |
> | 51+ excess users | $18/user |
>
> [IF secondary driver = user_rate_normalization — add:]
> Your per-user rate is also moving from **$[LEGACY_USER_RATE]/user** to the current graduated standard.
>
> With [TRAILING_AVG] average users, [NEW_EXCESS] users are now above the [NEW_INCLUDED]-user included base, billed at the graduated rate: [EXCESS_MATH_BREAKDOWN] = $[NEW_USER_CHARGE]/month.

(Difference between Format B and CEO Letter: "as part of this **change**" vs. "as part of this **refresh**." Both are preserved verbatim.)

#### §2.4.4 Format A canonical block

**Format A does not carry an `included_user_reduction` block.** Format A's mechanical scope is delta ≤ 10% / ≤ $80; standalone IUR primary cases produce deltas that route to Format B or CEO Letter.

If an IUR account ever routes to Format A (the kii exemplar — Kennedy International — is the canonical example: primary `at_book_tier_shift` with the included-user-reduction included-base move integrated as Format A's "Included user change rule" guidance from the Format A template), the drafter follows the Format A "Included user change rule" guidance block (preserved verbatim in the Format A template, not re-rendered here). The Format B IUR block above stands as the canonical IUR prose for any near-flat case Format A is asked to carry.

#### §2.4.5 Pricing-table row template

```
| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] | $[NEW_BASE] ([TIER]) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS] users at $[LEGACY_RATE] = **$[LEGACY_USER_CHARGE]/month** | [NEW_EXCESS] users at graduated rate = **$[NEW_USER_CHARGE]/month** |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |
```

Followed (Format B and CEO Letter) by the billing-basis footnote — verbatim per `_root/04 §4.9`.

#### §2.4.6 Conditional context paragraphs

For IUR, the following paragraphs may follow the table — text is owned by `_root/04`:

- **Billing-basis footnote** (italicized, immediately after the table) — required for every IUR brief. Verbatim sentence in `_root/04 §4.9`.
- **Platform-base-grown sentence** (when `new_tier_base > current_platform_mrr`) — required. Verbatim sentence in `_root/04 §4.6`.
- **IUR-variant close** — **required** for every IUR primary brief (per `_root/04 §2.13` non-negotiable). Replaces the default "only thing changing" close. Verbatim sentence in `_root/04 §4.5` IUR variant.
- **Early-adopter tenure paragraph** (when `cohort_year ≤ 2015`) — required. Variants in `_root/04 §4.7`.

#### §2.4.7 Secondary-driver integration

IUR appears as primary with the following secondaries in v6.2:

- **Standalone IUR primary, no secondary (9 occurrences post-CL-026 / CL-023 / CL-027 joint resolution 2026-05-26 — was 10 pre-CL-027 sweep; was 11 pre-CL-026/CL-023 before `bri` re-stamping; see §4 weaving matrix row 5).** Apply the canonical block as-is.
- **`user_rate_normalization` secondary.** Apply the `[IF secondary driver = user_rate_normalization]` sub-block above (the "Your per-user rate is also moving..." paragraph).

**Cross-reference — IUR appears as SECONDARY under other primaries (CL-026 + CL-027 operator-stamped 2026-05-26)**: The secondary semantic per §2.4.1 covers TWO v6.2 cohorts totaling 35 accounts (9 under TBI primary + 26 under URN primary; integrated at the respective §X.7 sections + §4 weaving matrix):

- **TBI primary + IUR secondary (9 accounts; 25→40 expansion shape)** — operator-stamped 2026-05-26 via CL-026 / CL-023 joint resolution: `bri` (Bulbrite, row 65 — re-stamped from IUR primary 2026-05-26), 8 CL-023 cluster (`ihw` / `ali` / `vic` / `ih` / `fc` / `ta` / `sbmh` + `sccon` — secondary_drivers re-coded URN → IUR 2026-05-26; `sccon` preserves MOR annotation per entity-child judgment). Integrated at §2.3.2 / §2.3.3 sub-block ("Additionally, the included user base for this tier is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]"); the §2.3.2 expansion-baked prose accommodates the 25→40 shape directly.
- **URN primary + IUR secondary (26 accounts; 25 REDUCTION-shape 25→10 + 1 EXPANSION-shape 25→40 = `bcf`)** — operator-stamped 2026-05-26 via CL-027 RESOLVED (URN-side closeout of the CL-026 / CL-023 sequence; surfaced by Stage 4.2 `sca` production-proof drafter hard-stop). The 25 reduction accounts: `sca` (Shadow Catchers — Stage 4.2 production-proof catalyst), `wac` / `sbl` / `fms` / `tla` / `mli` / `vcg` (6 with compound `multi_org_retirement, included_user_reduction` secondary), `all` / `kl` / `da` / `eglo` / `prog` / `cst` (HOLD-Annual) / `afx` / `dals` / `uhc` / `rf` / `big` / `heb` / `gsa` / `vl` / `cfg` / `mh` / `ah` / `etl`. The 1 expansion account: `bcf` (Braxton Culler — re-stamped from ABTS primary). Integrated at §2.1.2 / §2.1.3 via the two direction-specific sub-blocks (post-CL-027 source-fix at §2.1.2 mirrors the pre-existing §2.1.3 pattern): REDUCTION uses "Your included base is also adjusting from the legacy [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED]"; EXPANSION (bcf) uses the existing "expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED] — absorbing [N] users" sub-block.

Apply IUR-variant close per `_root/04 §4.5` for all 35 (IUR-as-secondary fork applies — close fork is shape-agnostic, not direction-specific). Apply billing-basis footnote per `_root/04 §4.9` for all 35. See §4 secondary-driver weaving matrix rows 3 + 5 for the canonical post-resolution combinations tally.

(Pre-CL-027 historical note: §2.1.7 previously cited "7 accounts" for URN+IUR-secondary — that count was stale across the v6.2 lifecycle and was never re-tallied during the CL-026 / CL-023 work because that effort scoped to TBI-side only. CL-027 closes the URN-side scope-gap. The reverse direction — IUR primary + URN secondary — remains as authored in §2.4.2's "[IF secondary driver = user_rate_normalization]" sub-block above for the standalone IUR-primary case; no v6.2 row instantiates this combination currently.)

---

### §2.5 — `at_book_tier_shift` (9 pending accounts; post-CL-026 / CL-023 joint resolution 2026-05-26)

#### §2.5.1 Definition

The account is already at the book rate for its tier; this is a minor adjustment as the book rate moves to the current standard. Near-zero delta is typical. The v6.2 field signature: `current_platform_mrr ≈ historical_book_rate_for_tier`, with `new_tier_base = current_tier_standard`. The "`≈ historical_book_rate_for_tier`" condition accommodates §2.5.6's ABTS-down special case (kii pattern; `current_platform_mrr` above current `tier_base` because legacy was OLD higher book). 9 of 107 pending accounts (count was 10 pre-CL-026 / CL-023 joint resolution 2026-05-26 — `bcf` re-stamped ABTS→URN after audit revealed `current_platform_mrr=$1,880` vs `tier_base=$2,295` = 18.1% gap fails the "at book" condition; `kii` retained per §2.5.6 documented down-move special case).

#### §2.5.2 Format B canonical block (verbatim)

> When your account was set up in [YEAR], the [TIER] tier was priced at **$[LEGACY_BASE]/month**. The current book rate for [TIER] is **$[NEW_BASE]/month**. Your invoice is moving to the current book rate — your tier is not changing, only the rate.

#### §2.5.3 CEO Letter canonical block (verbatim)

> When your account was set up in [YEAR], the [TIER] tier was priced at **$[LEGACY_BASE]/month**. The current book rate for [TIER] is **$[NEW_BASE]/month**. Your invoice is moving to the current book rate — your tier is not changing, only the rate.

(Format B and CEO Letter `at_book_tier_shift` blocks are identical character-for-character.)

#### §2.5.4 Format A canonical block (verbatim)

> When your account was set up in [YEAR], the [TIER] tier was priced at **$[LEGACY_BASE]/month**. The current standard for [TIER] is **$[NEW_BASE]/month**. [INSERT _root/04 §4.6 platform-base-grown sentence verbatim — applies when `new_tier_base > current_platform_mrr`; OMITTED when `new_tier_base < current_platform_mrr` (kii exemplar pattern, per §2.5.6 special case below).] Your tier is not changing, and neither is what your team has access to.

(Format A's ABTS block previously inlined `_root/04 §4.6`'s platform-base-grown sentence verbatim — the prior pattern violated the path-reference contract because the same sentence appeared in TWO places (§4.6 as canonical and inline here). CL-013 cleanup, applied 2026-05-26 at this `_root/05 §2.5.4` source per operator stamp 2026-05-26, replaces the inline with a pointer to `_root/04 §4.6`. The §4.6 sentence still applies for Format A ABTS briefs whenever `new_tier_base > current_platform_mrr`; the only change is that the canonical source is now §4.6 alone, and the drafter pastes the §4.6 sentence into the §2.5.4 placeholder at draft time. Format A's pattern now matches Format B and CEO Letter — all three formats reference §4.6 by pointer per §2.5.6.)

#### §2.5.5 Pricing-table row template

```
| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] ([YEAR] book rate) | $[NEW_BASE] (current [TIER] book rate) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS_DESCRIPTION] | [NEW_EXCESS_DESCRIPTION] |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |
```

Format A's row 1 second column is phrased `$[NEW_BASE] ([TIER] current book rate)` (small ordering difference). Both forms are canonical for their respective formats.

#### §2.5.6 Conditional context paragraphs

For ABTS, the following paragraphs may follow the table — text is owned by `_root/04`:

- **Platform-base-grown sentence** (when `new_tier_base > current_platform_mrr`) — required for Format A, Format B, and CEO Letter. All three formats reference `_root/04 §4.6` for the verbatim sentence. Format A's §2.5.4 block carries an inline pointer-placeholder for §4.6 (per CL-013 cleanup applied 2026-05-26 — see §2.5.4 explainer); Format B and CEO Letter apply the §4.6 sentence as a follow-on paragraph after the pricing table.
- **Early-adopter tenure paragraph** (when `cohort_year ≤ 2015`) — required. Variants in `_root/04 §4.7`. ABTS often co-occurs with early-adopter cohorts since these accounts were on book when book was lower.
- **Billing-basis footnote** — **NOT** required for ABTS. Per `_root/04 §4.9`, applies only to URN and IUR.
- **Default close** — applies. Verbatim sentence in `_root/04 §4.5` default form.

**Special case — base moves DOWN under ABTS** (the kii exemplar — Kennedy International — moves from $1,387 → $1,295, a base decrease, with a small user-count-driven net positive delta of +$8/mo). When `new_tier_base < current_platform_mrr`, the platform-base-grown sentence does NOT apply (the base is shrinking, not growing). The §2.5.4 placeholder for the `_root/04 §4.6` sentence is OMITTED in this case — the kii exemplar omits the platform-base-grown sentence entirely. This is operator-judgment territory: the §4.6 rule fires only when the base moves up. If the base moves down, the brief proceeds without the platform-base-grown sentence and the included-user-reduction integration (if any) carries the explanation.

#### §2.5.7 Secondary-driver integration

ABTS does not appear with a secondary driver explicitly named in v6.2's deduped secondary-combinations tally. However, the kii exemplar (Format A, ABTS primary) integrates an IUR-style included-base move (25 → 15 included users) inline in the prose: "The included-user base for this tier also standardizes to 15 users going forward. Your team averages 19 users — 4 are above the new included base and billed at the graduated rate." This is per-account narrative integration, not a templated sub-block. If v6.2 introduces explicit ABTS primary + IUR secondary or ABTS primary + URN secondary rows, the integration is undocumented in the canonical templates; flag per `_root/CONTRACTS.md §2`. For Stage 4 drafters: the kii exemplar's prose pattern stands as a per-account precedent, not a canonical rule.

---

### §2.6 — `multi_org_retirement` (6 pending accounts)

#### §2.6.1 Definition

The multi-organization pricing program is being retired. Each entity in the multi-org program moves to individual standard tier pricing. The v6.2 field signature: account has historical multi-org program affiliation (typically documented in `discount_drivers` and `parent_entity`). 6 of 107 pending accounts. Frequently produces large deltas when the multi-org rate was significantly below the individual standard.

#### §2.6.2 Format B canonical block (verbatim)

> [ACCOUNT_NAME] has been part of SuperCat's multi-organization pricing program — a structure that applied cross-entity benefits across [PARENT_ORG] and its related accounts. That program is being retired as part of this change. Each entity moves to individual standard [TIER] pricing.
>
> [IF secondary driver = included_user_reduction — add this paragraph:]
> Your included base also moves from [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED].

(CL-016 RESOLVED 2026-05-26 at source per operator stamp — the `[IF secondary driver = included_user_reduction]` templated sub-block was added to honor the 2026-05-22 operator stamp directing extension of Format B + CEO Letter MOR blocks with explicit IUR-secondary templated coverage. Pre-fix, the integration was per-account narrative per §2.6.7; post-fix, the sub-block fires automatically for the 6 v6.2 `multi_org_retirement | included_user_reduction` accounts. The MOR + URN secondary integration (2 v6.2 accounts) remains per-account narrative per the same operator stamp — only the IUR-secondary sub-block was elevated to templated coverage. See `_root/09_changelog.md` "Stage 3.2 review pass" entry for the source-fix rationale.)

#### §2.6.3 CEO Letter canonical block (verbatim)

> [ACCOUNT_NAME] has been part of SuperCat's multi-organization pricing program — a structure that applied cross-entity benefits across [PARENT_ORG] and its related accounts. That program is being retired as part of this refresh. Each entity moves to individual standard [TIER] pricing.
>
> [IF secondary driver = included_user_reduction — add this paragraph:]
> Your included base also moves from [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED].

(Difference between Format B and CEO Letter primary: "as part of this **change**" (Format B) vs. "as part of this **refresh**" (CEO Letter). Both verbatim. The IUR-secondary sub-paragraph is identical across both formats. CL-016 source fix applied to §2.6.3 in lockstep with §2.6.2 per operator stamp 2026-05-26.)

#### §2.6.4 Format A canonical block (verbatim)

> [ACCOUNT_NAME] has been part of SuperCat's multi-organization pricing program — a structure that applied cross-entity pricing benefits across [PARENT_ORG] and its related accounts. That program is being retired. Going forward, each entity moves to individual standard [TIER] pricing.
>
> Your pricing moves from the multi-org program rate to the standard [TIER] rate for your account's user count and configuration. Every [PARENT_ORG] entity is making the same move.

(Format A's MOR block adds a second paragraph — "Your pricing moves from the multi-org program rate..." — that Format B and CEO Letter omit. Format A carries this driver in production despite MOR typically producing larger deltas; the second paragraph is an entity-coordination acknowledgment that lands the structural fairness point. Preserved verbatim.)

#### §2.6.5 Pricing-table row template

```
| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] (multi-org program) | $[NEW_BASE] ([TIER] standard) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS_DESCRIPTION] | [NEW_EXCESS_DESCRIPTION] |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |
```

Format A's row 1 second column phrasing — `$[LEGACY_BASE] (multi-org program rate)` — is a near-identical variant. Format B and CEO Letter use `(multi-org program)`; Format A uses `(multi-org program rate)`. Either form is canonical for its template.

#### §2.6.6 Conditional context paragraphs

For MOR, the following paragraphs may follow the table — text is owned by `_root/04`:

- **Platform-base-grown sentence** (when `new_tier_base > current_platform_mrr`) — required. Verbatim sentence in `_root/04 §4.6`.
- **Early-adopter tenure paragraph** (when `cohort_year ≤ 2015`) — required. Variants in `_root/04 §4.7`.
- **Billing-basis footnote** — NOT required for MOR-primary standalone or MOR + URN-secondary (MOR's primary block does not produce excess-users lines on its own per `_root/04 §4.9`). REQUIRED for MOR + IUR-secondary when the IUR-secondary sub-block's included-base move produces excess users in the new pricing table — apply the verbatim sentence per `_root/04 §4.9` immediately after the pricing table. Drafter judgment per the actual user-count math.
- **IUR-variant close** (when secondary = `included_user_reduction`) — required. Verbatim sentence in `_root/04 §4.5` IUR variant.
- **Entity-coordination context** — MOR by definition involves a `parent_entity` per `_root/02 §3` (the entity overlay rule). The brief is part of an entity packet; per-brand pricing detail lives in this brief and the packet's framing letter handles the entity-level relationship. `_root/05` does not own the entity-packet structure.

#### §2.6.7 Secondary-driver integration

MOR appears as primary with the following secondaries in v6.2:

- **`included_user_reduction` secondary (6 occurrences in the v6.2 secondary-combinations tally — `multi_org_retirement | included_user_reduction`).** Apply the `[IF secondary driver = included_user_reduction]` templated sub-block in §2.6.2 (Format B) or §2.6.3 (CEO Letter) — the integrated paragraph "Your included base also moves from [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED]" lands immediately after the MOR primary block. Apply IUR-variant close per `_root/04 §4.5` (IUR is secondary, fork applies) and billing-basis footnote per `_root/04 §4.9`. [CL-016 RESOLVED 2026-05-26 at the §2.6.2 + §2.6.3 source per operator stamp — see `_root/09_changelog.md` "Stage 3.2 review pass" entry.]
- **`user_rate_normalization` secondary (2 occurrences — `multi_org_retirement | user_rate_normalization`).** No templated sub-block (per CL-016 operator stamp 2026-05-22: only IUR-secondary was elevated to templated coverage; URN-secondary remains narrative integration given the lower volume). The drafter integrates the URN move into the per-account narrative within the MOR block (e.g. "Your per-user rate is also moving from $[LEGACY_USER_RATE]/user to the current graduated standard"). Apply billing-basis footnote per `_root/04 §4.9` if URN integration produces a user-charge change. The 2 v6.2 accounts in this combination follow the kii / da exemplar narrative-integration pattern documented in §4.
- **`multi_org_retirement` standalone (1 occurrence in the secondary-combinations tally — `multi_org_retirement` alone, secondary blank).** Apply the canonical block as-is (the `[IF secondary driver = included_user_reduction]` sub-block does not fire; default close applies per `_root/04 §4.5`).

---

### §2.7 — `annual_discount_retirement` (2 pending accounts)

#### §2.7.1 Definition

The annual commitment discount is being retired. Accounts billed at an annual prepay discount move to the standard monthly tier rate. Annual prepay remains available — only the rate changes. The v6.2 field signature: `deal_type = 'Annual'` AND `current_mrr < new_tier_base` (the discount being retired is on the rate, not the billing cadence). 2 of 107 pending accounts.

#### §2.7.2 Format B canonical block (verbatim)

> Your account has been billed at an annual commitment rate since [YEAR] — a discount applied at signing for annual prepayment. As part of this change, annual-commitment discounts are being retired across all accounts. Your new rate is the [TIER] standard monthly rate.
>
> Annual prepay remains available if you prefer that billing structure — terms are the same, only the base rate is changing. If you'd like to continue annual billing, we'll document that as part of this transition.

#### §2.7.3 CEO Letter canonical block (verbatim)

> Your account has been billed at an annual commitment rate since [YEAR] — a discount applied at signing for annual prepayment. As part of this refresh, annual-commitment discounts are being retired across all accounts. Your new rate is the [TIER] standard monthly rate.
>
> Annual prepay remains available if you prefer that billing structure — terms are the same, only the base rate is changing. If you'd like to continue annual billing, we'll document that as part of this transition.

(Difference: "as part of this **change**" (Format B) vs. "as part of this **refresh**" (CEO Letter). Both verbatim.)

(Note on "transition": the second paragraph in both blocks contains the word "transition" ("we'll document that as part of this transition"). Per `_root/04 §3` row on the "transition" replacement, this usage is permitted in the narrow administrative context of `annual_discount_retirement` blocks — the existing template usage stands until edited. The word does not refer to the customer's side of the move; it refers to administering the documentation of the billing change.)

#### §2.7.4 Format A canonical block

**Format A does not carry an `annual_discount_retirement` block.** Format A's mechanical scope is delta ≤ 10% / ≤ $80; ADR accounts produce deltas large enough that they route to Format B or CEO Letter. The Annual segment also routes by renewal calendar per `_root/02 §5`, decoupling timing from cohort.

If a near-flat ADR case ever arises, the drafter falls back to the Format B block above and trims to Format A's near-flat register.

#### §2.7.5 Pricing-table row template

```
| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] ([YEAR] annual rate) | $[NEW_BASE] ([TIER] standard) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS_DESCRIPTION] | [NEW_EXCESS_DESCRIPTION] |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |
```

#### §2.7.6 Conditional context paragraphs

For ADR, the following paragraphs may follow the table — text is owned by `_root/04`:

- **Platform-base-grown sentence** (when `new_tier_base > current_platform_mrr`) — required. Verbatim sentence in `_root/04 §4.6`.
- **Early-adopter tenure paragraph** (when `cohort_year ≤ 2015`) — required. Variants in `_root/04 §4.7`.
- **Billing-basis footnote** — **NOT** required for ADR. Per `_root/04 §4.9`, applies only to URN and IUR.
- **Default close** — applies (no IUR fork unless secondary = IUR).
- **Annual-cohort timing notice** — `_root/02 §5` annual overlay applies. The brief itself is unchanged; timing routes off renewal calendar, not cohort calendar. `_root/06` owns the routing detail.

#### §2.7.7 Secondary-driver integration

ADR appears as primary with the following secondaries in v6.2:

- **`annual_discount_retirement` standalone (1 occurrence in the secondary-combinations tally — `annual_discount_retirement` alone, secondary blank).** Apply the canonical block as-is.

(The other ADR primary row's secondary configuration is not enumerated in the deduped tally — likely also blank. ADR co-occurring with IUR or URN secondaries is not currently observed in v6.2.)

---

### §2.8 — `special_arrangement` (1 pending account)

#### §2.8.1 Definition

A custom pricing arrangement set outside the standard structure is being moved to standard tier rates. Direct, no-euphemism framing. The v6.2 field signature: account history documented in `discount_drivers` and `angies_notes` indicating a one-off arrangement (custom rate, executive-approved discount, partner program). 1 of 107 pending accounts. Delta-dependent CEO involvement: per `_handoff-prompt.md` §Driver Framing, delta > 30% triggers CEO involvement; per the Format B / CEO Letter operator-note blockquote, "for `special_arrangement` accounts with delta >30%, confirm the account history with Finance before outreach. The CEO must be prepared to answer 'what was the arrangement and why is it changing?'"

#### §2.8.2 Format B canonical block (verbatim)

> Your current pricing reflects a custom arrangement from [YEAR] — a rate set outside SuperCat's standard structure. In 2026, every account is moving to one clear pricing structure. The new rate is the [TIER] standard for your tier and user count.

#### §2.8.3 CEO Letter canonical block (verbatim)

> Your current pricing reflects a custom arrangement from [YEAR] — a rate set outside SuperCat's standard commercial structure. As we bring all accounts onto the same pricing structure in 2026, custom arrangements are moving to standard tier rates. This is not a judgment about your account — it's a structural decision: one rate card, applied consistently. The new price is what every account at your tier and user count pays.

(The CEO Letter SA block is materially longer and more direct than Format B's — it adds the explicit "this is not a judgment about your account" reframe and the "one rate card, applied consistently" closing line. The divergence is intentional: SA in CEO Letter context is a peer-to-peer conversation about a custom arrangement, and the longer framing earns the move. Preserved verbatim.)

#### §2.8.4 Format A canonical block (verbatim)

> Your current pricing reflects a custom arrangement from [YEAR] — a rate set outside the standard structure at the time. In 2026, every account moves to the same tier structure, including those on custom arrangements.
>
> The new pricing is the standard [TIER] rate for your account's user count and configuration.

(Format A's SA block is shorter than CEO Letter's and roughly the same length as Format B's, with slightly different phrasing. Format A handles low-delta SA cases where the longer CEO Letter framing would be disproportionate.)

#### §2.8.5 Pricing-table row template

```
| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] (custom arrangement) | $[NEW_BASE] ([TIER] standard) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS_DESCRIPTION] | [NEW_EXCESS_DESCRIPTION] |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |
```

Format A's row 1 phrasing — `$[LEGACY_BASE] (custom arrangement, [YEAR])` — adds the year inline.

#### §2.8.6 Conditional context paragraphs

For SA, the following paragraphs may follow the table — text is owned by `_root/04`:

- **Operator note** (Format B and CEO Letter) — verbatim from the templates: "For `special_arrangement` accounts with delta >30%, confirm the account history with Finance before outreach. The CEO must be prepared to answer 'what was the arrangement and why is it changing?'" This is internal-only; removed before send.
- **Platform-base-grown sentence** (when `new_tier_base > current_platform_mrr`) — required. Verbatim sentence in `_root/04 §4.6`.
- **Early-adopter tenure paragraph** (when `cohort_year ≤ 2015`) — required. Variants in `_root/04 §4.7`.
- **High-delta lede rule** (when `delta_pct > 30%`) — required. Verbatim sentences in `_root/04 §4.4`. SA accounts often clear this threshold; CEO involvement is the mechanical consequence.
- **Default close** — applies.
- **Billing-basis footnote** — **NOT** required for SA.

#### §2.8.7 Secondary-driver integration

SA does not appear with a secondary driver in v6.2 (the 1 SA primary row has `secondary_drivers` blank). No integration sub-block to author.

---

## Section 3 — Decrease-side drivers

The 3 decrease-side drivers route to the Good News Notice format per `_handoff-prompt.md` §Format Routing Rules and `_root/06` (next wave). The Good News template's voice posture is "math, not a favor" — per `_root/04 §3` row on "gift / reward for loyalty," the decrease is stated as the mechanic that produces it, never as a gift, reward, or thank-you.

### §3.1 — `module_compression` (8 pending accounts across 3 segments)

#### §3.1.1 Definition

Separate module charges (e.g. iPad App + Catalog + Sales Intelligence as standalone line items under legacy module pricing) consolidate into a single tier subscription at a lower combined rate. The v6.2 field signature: account historically billed for multiple module SKUs whose combined rate exceeds the new tier's standard base. **8 of 107 pending accounts**, distributed across three segments per `_root/02 §1`:

| Segment | Accounts | Notes |
|---|---|---|
| Tailwind | `ml`, `gc`, `dccl`, `pf` (4) | Net-negative delta, no segment-override applies, route to Good-News Notice per §3.1.2 mechanic block. |
| Annual | `mali`, `mah` (2) | Annual overlay (`_root/02 §5`) supersedes Tailwind segment label; routing timing is renewal-driven; format substance is still Good News if Δ < 0 (which both are). |
| Strategic | `ap`, `mfc` (2) | Health override (`_root/02 §4`) supersedes Tailwind segment label; both accounts are Watch-band. Routing per `_root/06 §4.2` — Good-News-eligible accounts that are Watch/At Risk/Critical do NOT receive a Good News brief; routed through CSM for health check-in first, then per-account operator decision via routing-CSV `post_hold_action`. |

Named in `_handoff-prompt.md` §Driver Framing and forward-referenced in `_root/04 §5`. The mechanic block (§3.1.2) and Format A variant (§3.1.3) are canonical for the underlying driver; the eventual format / send disposition is governed by `_root/06` overrides for the 4 Annual + Strategic accounts.

#### §3.1.2 Mechanic block (Good News canonical, verbatim)

> As part of SuperCat's 2026 pricing restructure, the platform now moves to a unified tier model. For [ACCOUNT_NAME], this means the separate module charges that made up your current invoice are consolidating into a single [T1/T2/T3] tier subscription — at a lower combined rate.

#### §3.1.3 Format A canonical block (verbatim — for near-flat module-compression cases)

The Format A template also carries a `module_compression` block:

> SuperCat's legacy pricing structured your account as separate module line items. Those modules are now part of a single unified tier. For [ACCOUNT_NAME], the consolidation means **your monthly price is decreasing from $[CURRENT_MRR] to $[NEW_MRR]** — the unified tier includes everything you were paying for separately, at a lower combined rate.

(Format A carries `module_compression` because some module-compression accounts produce small absolute decreases that still route to Format A's near-flat handling rather than Good News. The Format A block carries the dollar change inline; the Good News block leads with the dollar change in the brief's first sentence and the mechanic paragraph references it. Both are canonical for their format.)

#### §3.1.4 Pricing-table row template (Good News)

```
| | Before | After |
|---|---|---|
| [MODULE_1 — e.g., iPad App] | $[M1_PRICE] | — |
| [MODULE_2 — e.g., Catalog] | $[M2_PRICE] | — |
| [MODULE_3 — if applicable] | $[M3_PRICE] | — |
| **[TIER_LABEL] subscription** | — | **$[NEW_MRR]** |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |
```

Format A's table for `module_compression`:

```
| | Before (modules) | After (tier) |
|---|---|---|
| [MODULE_1] | $[M1_PRICE] | — |
| [MODULE_2] | $[M2_PRICE] | — |
| [MODULE_3] | $[M3_PRICE] | — |
| **[TIER_NAME] base** | — | **$[NEW_BASE]** |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |
```

(Same data, slight column-header phrasing variance: Good News says "Before / After"; Format A says "Before (modules) / After (tier)". Both are canonical.)

#### §3.1.5 Voice posture note

Per `_root/04 §3` row on "gift / reward for loyalty" prohibition: a Good News notice states the mechanic plainly. The consolidation produces a lower combined rate; do not frame as a favor. Per the Good News template's "Critical voice rules": lead with the dollar amount and effective date in the first sentence; do not bury the decrease after a paragraph of context; do not include percentage unless asked; the percentage is available in the summary table.

The Good News close is owned by `_root/04 §4.12` (Good News close: "Questions about what's changing or how the new rate was calculated — reach out directly."). Good News notices do not include a meeting offer, a call commitment, or a follow-up trigger.

---

### §3.2 — `user_count_variance` (2 pending accounts: rw, jyc)

#### §3.2.1 Definition

The current invoice is based on a billed-user count higher than the 6-month trailing average of active users. As part of the 2026 pricing refresh, user counts across all accounts are aligned to trailing-average actuals. The recalculated user charge produces a lower invoice. The v6.2 field signature: `current_user_mrr / current_user_rate > trailing_avg_users − included_users` (i.e. billed-excess > actual-excess). 2 of 6 Tailwind accounts.

**Flag**: `user_count_variance` is **NOT** in `_handoff-prompt.md` §Driver Framing. The Good News template carries the canonical mechanic block (below); the handoff stamp is missing. Surfaced in §6 as an open question for the operator. The Good News template prose stands as the canonical version until ratified.

#### §3.2.2 Mechanic block (Good News canonical, verbatim)

> Your current invoice is based on [CURRENT_BILLED_USERS] users. Your 6-month trailing average is [TRAILING_AVG_USERS] active users. As part of this refresh, user counts across all accounts are being aligned to trailing-average actuals. Your new invoice reflects [TRAILING_AVG_USERS] users at the current rate structure.

#### §3.2.3 Pricing-table row template (Good News)

```
| | Before | After |
|---|---|---|
| Platform base ([TIER]) | $[BASE] | $[BASE] |
| Included users | [INCLUDED] | [INCLUDED] |
| Billable users | [OLD_EXCESS] users at $[OLD_RATE] = **$[OLD_USER_CHARGE]** | [NEW_EXCESS] users at graduated rate = **$[NEW_USER_CHARGE]** |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |
```

#### §3.2.4 Voice posture note

Same as §3.1.5: per `_root/04 §3`, state the mechanic, not a favor. Per the Good News template, the user_count_variance mechanic block is required to land with the table (the Good News template comments "Tables are optional for module_compression; required for user_count_variance" — the table is the proof for the recalibration).

---

### §3.3 — `rate_architecture` (1 pending account: mlg — Minka Lighting Group)

#### §3.3.1 Definition

The per-user rate was set at a legacy rate structure that, recalculated against the current graduated ladder, produces a lower invoice. The v6.2 field signature: `current_user_rate × current_excess > graduated_ladder_charge_for_same_excess`. 1 of 7 decrease accounts (mlg is in the Annual segment but carries a negative delta of −$38/mo). The only decrease-side account that is not in the Tailwind segment.

**Flag**: `rate_architecture` is **NOT** in `_handoff-prompt.md` §Driver Framing. The Good News template carries the canonical mechanic block (below); the handoff stamp is missing. Surfaced in §6 as an open question for the operator. The Good News template prose stands as canonical.

#### §3.3.2 Mechanic block (Good News canonical, verbatim)

> Your current user rate was set at **$[LEGACY_RATE]/user** under the rate structure in place at signing. As part of the 2026 refresh, all accounts move to the same graduated rate card. For [ACCOUNT_NAME], the recalculated rate produces a lower invoice.

#### §3.3.3 Pricing-table row template (Good News)

```
| | Before | After |
|---|---|---|
| Platform base ([TIER]) | $[BASE] | $[BASE] |
| Included users | [INCLUDED] | [INCLUDED] |
| Billable users | [OLD_EXCESS] users at $[OLD_RATE]/user = **$[OLD_USER_CHARGE]** | [NEW_EXCESS] users at graduated rate = **$[NEW_USER_CHARGE]** |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |
```

#### §3.3.4 Voice posture note

Same as §3.1.5: per `_root/04 §3`, state the mechanic. The graduated rate card produces a lower invoice for this account's specific configuration; the brief explains the recalculation, not a discount or thank-you.

---

## Section 4 — Secondary-driver weaving matrix

The matrix below enumerates **all** primary-secondary combinations v6.2 actually exhibits (post-CL-026 / CL-023 / CL-027 joint resolution 2026-05-26 + CL-030 RESOLVED 2026-05-27 full-matrix rebuild from `csv.DictReader` ground truth). It is the operational artifact Stage 4 drafters consult after picking the primary block from §2 or §3.

| Primary | Secondary | Occurrences in v6.2 | What changes about the primary block |
|---|---|---:|---|
| `user_rate_normalization` | (none) | 11 | Apply §2.1 canonical block as-is. Apply default close per `_root/04 §4.5` and billing-basis footnote per `_root/04 §4.9`. The 11 accounts: `cci` / `clc` / `clli` / `el` / `eli` / `hfg` / `kal` / `lpf` / `sarreid` / `shl` / `ufi`. |
| `user_rate_normalization` | `included_user_reduction` | 20 (19 REDUCTION + 1 EXPANSION = `bcf`) | §2.1 primary block + one of two direction-specific sub-paragraphs per the post-CL-027 §2.1.2 / §2.1.3 sub-block pair: REDUCTION accounts use the `[IF excess users remain AND secondary driver = included_user_reduction (base shrinking from legacy to current tier standard)]` "Your included base is also adjusting from the legacy [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED]" sub-block; EXPANSION (`bcf`) uses the `[IF excess users remain AND new included base > legacy included base (base expanding)]` "expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED] — absorbing [N] users" sub-block. Mutually exclusive (exactly one fires per account). Apply IUR-variant close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9`. The 20 accounts: `afx` / `ah` / `all` / `bcf` (expansion) / `big` / `cfg` / `cst` (HOLD) / `da` / `dals` / `eglo` / `etl` / `gsa` / `heb` / `kl` / `mh` / `prog` / `rf` / `sca` / `uhc` / `vl`. See §2.1.7 for the broader 26-account URN+IUR-bearing cohort (this row + the URN+MOR+IUR row below). |
| `user_rate_normalization` | `multi_org_retirement, included_user_reduction` | 6 | `wac` / `sbl` / `fms` / `tla` / `mli` / `vcg` (URN-primary; MOR + IUR compound secondary; all 6 REDUCTION direction). §2.1 primary block + the REDUCTION sub-block per §2.1.2 / §2.1.3; MOR portion is annotation-only at URN-primary scope (no MOR-secondary sub-block under URN primary per §2.1.7). Apply IUR-variant close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9`. |
| `user_rate_normalization` | `multi_org_retirement` | 1 | `sc`. §2.1 primary block + MOR portion annotation-only at URN-primary scope (no MOR-secondary sub-block under URN primary). Apply default close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9`. |
| `included_user_reduction` | (none) | 9 | Apply §2.4 canonical block as-is. Apply IUR-variant close per `_root/04 §4.5` and billing-basis footnote per `_root/04 §4.9`. The 9 accounts: `am` / `bp` / `clm` / `df` / `fal` / `gblx` / `hf` / `ihm` / `mlc`. (Post-CL-026 / CL-023 joint resolution 2026-05-26: count 10→9 after `bri` re-stamping out to TBI primary.) |
| `included_user_reduction` | `annual_discount_retirement` | 1 | `arl`. §2.4 primary block + per-account narrative integration of the ADR move (no canonical IUR+ADR sub-block; see §6 flag). Apply IUR-variant close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9`. |
| `tier_base_increase` | (none) | 4 | Apply §2.3 canonical block as-is. Apply default close per `_root/04 §4.5` and billing-basis footnote per `_root/04 §4.9`. The 4 accounts: `fsf` / `gl` / `ol` / `ril`. |
| `tier_base_increase` | `included_user_reduction` | 8 | `bri` + 7 CL-023 cluster (`ihw` / `ali` / `vic` / `ih` / `fc` / `ta` / `sbmh`). §2.3 primary block + the `[IF secondary driver = included_user_reduction]` sub-block "Additionally, the included user base for this tier is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]" (25→40 EXPANSION shape per CL-026 / CL-023 Option A primary-vs-secondary semantic clarification). Apply IUR-variant close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9`. (Post-CL-027 + CL-030: `bcf` removed from this cohort — re-stamped TBI→URN per CL-027; canonical home is URN+IUR row above.) |
| `tier_base_increase` | `multi_org_retirement, included_user_reduction` | 1 | `sccon` (Summer Classics Contract). §2.3 primary block + IUR sub-block (fires from IUR portion of compound secondary stamp); MOR portion is annotation-only at TBI-primary scope (no MOR-secondary sub-block under TBI primary per §2.3.7). Apply IUR-variant close + billing-basis footnote. |
| `multi_org_retirement` | `user_rate_normalization` | 4 | `asi` / `cf` / `gh` / `hh` (CL-030 RESOLVED 2026-05-27 corrected count 1→4 from `csv.DictReader` ground truth; pre-rebuild matrix incorrectly listed only `scw` here, but `scw` is PDC-primary per v6.2 — canonical home is the PDC+MOR+URN row below). §2.6 primary block + per-account narrative integration of the URN move (no canonical MOR + URN sub-block; see §6 flag). Apply default close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9` if URN integration produces a user-charge change. |
| `multi_org_retirement` | `user_rate_normalization, included_user_reduction` | 2 | `eglo_can` / `vce`. §2.6 primary block + per-account narrative integration of the compound URN+IUR moves. Apply IUR-variant close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9`. |
| `at_book_tier_shift` | (none) | 9 | Apply §2.5 canonical block as-is. Apply default close per `_root/04 §4.5`. The 9 accounts: `abol` / `kii` (§2.5.6 down-move special case) / `krb` / `lss` / `mpc` / `pebl` / `soi` / `swc` / `tcd`. (Post-CL-026 / CL-023 joint resolution 2026-05-26: count 10→9 after `bcf` re-stamping out to URN primary.) |
| `annual_discount_retirement` | `user_rate_normalization` | 1 | `jc`. §2.7 primary block + per-account narrative integration of URN move. Apply default close per `_root/04 §4.5`. |
| `annual_discount_retirement` | (none) | 1 | `luc`. Apply §2.7 canonical block as-is. Apply default close per `_root/04 §4.5`. |
| `platform_discount_correction` | `user_rate_normalization` | 5 | `jcusa` / `kkc` / `kll` / `st` / `wwjc`. §2.2 primary block + per-account narrative integration of URN move (no canonical PDC + URN sub-block; see §6 flag). Apply default close per `_root/04 §4.5`. |
| `platform_discount_correction` | `included_user_reduction` | 2 | `gcl` / `wag`. §2.2 primary block + per-account narrative integration of IUR move (no canonical PDC + IUR sub-block; see §6 flag). Apply IUR-variant close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9`. |
| `platform_discount_correction` | `user_rate_normalization, included_user_reduction` | 5 | `hvl` / `pw` / `rac` / `ssi` / `tl`. §2.2 primary block + per-account narrative integration of compound URN+IUR. Apply IUR-variant close per `_root/04 §4.5`. Apply billing-basis footnote per `_root/04 §4.9`. |
| `platform_discount_correction` | (none) | 4 | `bsc` / `cl` / `sp` / `tam`. Apply §2.2 canonical block as-is. Apply default close per `_root/04 §4.5`. |
| `platform_discount_correction` | `multi_org_retirement, user_rate_normalization` | 1 | `scw`. §2.2 primary block + per-account narrative integration of compound MOR+URN. Apply default close per `_root/04 §4.5`. |
| `special_arrangement` | (none) | 1 | `yw`. Apply §2.8 canonical block as-is. Apply default close per `_root/04 §4.5`. |
| `module_compression` | (none) | 8 | `ap` / `dccl` / `gc` / `mah` / `mali` / `mfc` / `ml` / `pf`. Apply §3.1 canonical block as-is. Apply Good News close per `_root/04 §4.12`. |
| `user_count_variance` | (none) | 2 | `jyc` / `rw`. Apply §3.2 canonical block as-is. Apply Good News close per `_root/04 §4.12`. |
| `rate_architecture` | (none) | 1 | `mlg`. Apply §3.3 canonical block as-is. Apply Good News close per `_root/04 §4.12`. |

**Total combinations enumerated: 23** (post-CL-030 RESOLVED 2026-05-27 full-matrix rebuild from `csv.DictReader` ground truth). **Aggregate v6.2-exhibited primary-secondary occurrences across the 23 rows**: 11+20+6+1+9+1+4+8+1+4+2+9+1+1+5+2+5+4+1+1+8+2+1 = **107** (reconciles to §1.1 driver-inventory totals: URN 38 + IUR 10 + TBI 13 + MOR 6 + ABTS 9 + ADR 2 + PDC 17 + SA 1 + MC 8 + UCV 2 + RA 1 = 107 ✓).

**Constraint reminder**: do not enumerate hypothetical combinations. If a future v6.2 update introduces a new combination beyond the 23 enumerated above, the integration is undocumented; flag per `_root/CONTRACTS.md §2` and ask the operator before drafting.

**Format A note**: Format A's mechanical scope (delta ≤ 10% / ≤ $80) means the matrix above applies primarily to Format B and CEO Letter. Format A integrates secondaries via the per-account narrative pattern shown in the kii exemplar (`at_book_tier_shift` primary + IUR-style included-base move integrated inline).

---

## Section 5 — Driver-segment correlation (informational)

The table below notes which drivers tend to cluster in which segments. **This is informational only.** Per `_root/02` and the archived `_handoff-prompt.md`, segment is determined by Δ + entity overlay + health overrides + annual overlay; the driver is independent of segment routing. **Do not route on this table.**

| Segment | Common primary drivers (informational) | Notes |
|---|---|---|
| Tailwind (Δ ≤ $0) | `module_compression`, `user_count_variance`, `rate_architecture` | All decrease-side. **Decrease-side accounts spill across three segments** per `_root/02 §1` + the §3 overrides: 6 Tailwind (4 MC: ml/gc/dccl/pf + 2 UCV: rw/jyc), 3 Annual (2 MC: mali/mah + 1 RA: mlg), 2 Strategic (2 MC: ap/mfc — both Watch-band). The mechanic block per driver applies regardless of segment; routing is governed by `_root/06 §4.2`/`§4.3` overrides. |
| Core ($0 < Δ ≤ $200) | `at_book_tier_shift`, `user_rate_normalization`, `tier_base_increase` | Healthy, low-delta increase-side. Format A and Format B routing typical. |
| Narrative ($201 ≤ Δ ≤ $400) | `user_rate_normalization`, `tier_base_increase`, `platform_discount_correction` | Healthy, mid-delta increase-side. Format B routing typical. |
| Executive ($401 ≤ Δ ≤ $600) | `user_rate_normalization` (often + IUR secondary), `included_user_reduction`, `platform_discount_correction` | Co-authored with CEO. CEO Letter routing typical. |
| Pre-Engagement (Δ > $600) | `user_rate_normalization` (often + IUR secondary), `included_user_reduction`, `multi_org_retirement` | CEO-initiated call before notice. 7 of 8 Pre-Engagement accounts have URN as primary — useful calibration signal for the drafter. |
| Entity (parent_entity overlay) | `multi_org_retirement` (when retiring a multi-org program), plus mixed drivers per child | Entity packet covers all child accounts; per-child driver may vary. |
| Strategic (health override) | Mixed — driver is independent of health override | CEO-led conversation precedes notice; voice posture changes per `_root/04 §4.13`. |
| Annual (deal_type = Annual) | `annual_discount_retirement` (when a discount is being retired), plus mixed drivers per renewal calendar | Renewal-driven timing per `_root/02 §5`. |

The clustering is a side-effect of the underlying account-level facts (high deltas tend to fall on accounts with locked-at-signing user rates, multi-org program members produce large structural moves, etc.), not a routing rule. Drafters: pick the driver from v6.2 `migration_driver` and the format from `_root/06`. This table is calibration context only.

---

## Section 6 — What this doc does NOT own

The following live in other root docs. References should point there, not duplicate the rules here:

- **Voice rules governing HOW the driver block reads** → `_root/04` (especially §4.5 IUR fork close, §4.6 platform-base-grown sentence, §4.7 early-adopter tenure paragraph, §4.9 billing-basis footnote, §4.10 platform-base conditional inside URN block, §4.14 discount-correction posture).
- **The tier-feature paragraph that follows the driver block ("What You're Getting at $X")** → `_root/03 §1` (the verbatim T1/T2/T3 blocks).
- **The user-rate ladder that appears in URN, IUR, TBI, and ABTS driver blocks** → `_root/03 §2 Block A` (the canonical 1–10 / 11–25 / 26–50 / 51+ table at $25/$22/$20/$18). The rendering of the ladder inside the driver-prose blockquote in §2.1.2, §2.1.3, §2.1.4, §2.4.2, §2.4.3 is verbatim from the templates; the canonical source is `_root/03 §2 Block A`.
- **Segment definitions and ownership boundaries** → `_root/02` (the 8 segments, the $200 / $400 / $600 ownership thresholds, entity overlay, health overrides, annual overlay, cohort assignment).
- **Which format a driver routes to** (delta thresholds, CEO involvement gates, entity-packet structure) → `_root/06` (next wave; not yet authored).
- **The v6.2 data fields each driver dispatches on** → `_root/07 §2` (the column-by-column field guide; `migration_driver`, `secondary_drivers`, `current_user_rate`, `current_platform_mrr`, `tier_base`, `current_provided_users`, `included_users`, `trailing_avg_users`, `cohort_year`, `delta_mrr`, `delta_pct`).
- **The quality-bar check** that confirms the right driver block was selected and the right conditional sub-blocks fired → `_root/08` (Wave 4; not yet authored).

---

*Cross-references: `_root/00_manifest.md` (required-reading map); `_root/CONTRACTS.md §5` (path-reference contract — this doc references `_root/04` voice rules rather than restating them); `_root/09_changelog.md` (log entries for every edit to this doc).*



