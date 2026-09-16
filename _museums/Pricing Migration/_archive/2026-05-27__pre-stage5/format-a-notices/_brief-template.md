# Format A — 60-Day Notice — Brief Template
*CS-led | Near-flat delta (≤$80/mo or ≤10%, higher-touch-wins precedence per `_root/06 §3`) | Passive close per `_root/04 §4.12`*

---

> **Operator notes — drafter-facing scaffolding; remove this entire blockquote before sending.**
>
> **When to use this template.** Format A is the CS-led 60-Day Notice for accounts whose Δ MRR is near-flat. The mechanical scope, the routing-decision flow, and the higher-touch-wins precedence rule are all defined in `_root/06 §1` (Format A description), `_root/06 §2` (6-step routing-decision flow), and `_root/06 §3` (delta-tier dispatch + operator-stamped Δ_pct vs Δ_mrr precedence). Do not restate them here; consult `_root/06` when in doubt.
>
> **Who sends.** CS team — Kylor — per `_root/06 §1` (no CEO co-signature; no CEO awareness flag required).
>
> **What this template is NOT for.**
> - Entity-children (`parent_entity` non-empty AND `parent_entity ≠ company`): fold into the entity packet per `_root/02 §3` and `_root/06 §4.1` — do NOT draft a standalone Format A.
> - Δ ≥ $400 (CEO Letter) or Δ ≥ $600 (CEO Pre-Call → Format B): out of scope per `_root/06 §3` dispatch table.
> - Boundary cases ($75 / 12%; $700 / 8%): the higher-touch format wins per the `_root/06 §3` precedence rule. If the routing produces a counterintuitive Format A assignment, escalate per `_root/CONTRACTS.md §2`.
> - Watch / At Risk / Critical (`health_band ∈ {Watch, At Risk, Critical}` OR `value_delivery_score < 40`): the health override fires per `_root/02 §4` + `_root/06 §4.2`; the account is in `notice_cohort = 'Post-Migration'` and the brief is deferred. Critical-band routing is per-account per `post_hold_action` — consult the routing CSV directly per `_root/06 §4.2`.
> - `migration_driver ∈ {tier_base_increase, included_user_reduction, annual_discount_retirement}`: Format A does not carry these driver blocks per `_root/05 §2.3.4`, `§2.4.4`, `§2.7.4`. If the routing produces a Format A assignment with one of those primary drivers, the routing is suspect — escalate per `_root/CONTRACTS.md §2`.
>
> **Cleanup-tracker history embedded in this template.** Items applied as of authoring date: CL-001 (no "no account-specific adjustments" sentence anywhere); CL-003 (no peer dollar ranges in client copy — universal per operator stamp 2026-05-22); CL-004 (no "equivalent platforms" / unnamed-competitor pricing sentence anywhere); CL-005 (mandatory "What's Coming in 2026" block via `_root/03 §3` pointer); CL-011 (`platform_discount_correction` is the canonical driver name); CL-013 (RESOLVED 2026-05-26 at source — no per-template carve-out needed for `at_book_tier_shift`; `_root/05 §2.5.4` carries the §4.6 placeholder cleanly). See `_meta/stage3_cleanup.md` for full item history.
>
> **Drafter's responsibility.** Every `_root/XX §N.M` reference in this template is to a canonical rule doc. At draft time, the drafter (a) opens the referenced section, (b) copies the named verbatim content character-for-character, (c) substitutes any `[BRACKETED_TOKEN]` placeholders from v6.2 + Postgres data per `_root/07 §2` + `§4`. The template carries pointers; it does not carry rule prose. Pre-send: run the `_root/08` Quality Bar against the completed draft (the QB-NNN list under "Section 4 — Pre-send drafter checklist" below names the Format-A-specific blockers; the full 126-check checklist lives in `_root/08`).
>
> **Conformance block.** The drafter ends the session with the canonical conformance block defined in `_root/00_manifest.md §5`.

---

> **Internal routing note** (drafter-facing; remove before sending — matches the canonical field list per `_root/07 §7` for Format A; field names and order match `_root/07 §7` exactly):
>
> Brief type: `value_justification` | Format A — 60-Day Notice
> Account: [ACCOUNT_NAME] | Tier: [T1/T2/T3] | Wave: [WAVE]
> Migration driver: [DRIVER] | Health: [HEALTH_SCORE] — [HEALTH_BAND] | Risk label: [RISK_LABEL]
> Engagement: [E] | Adoption: [A] | Value Delivery: [VD] | Ops Health: [OH]
> Support fire: [YES/NO] | Behavioral floor applied: [YES/NO]
> Delta: [DELTA_PCT] (+$[DELTA_MRR]/month)
> Cohort: [COHORT_YEAR]
> Contract: [MONTHLY/ANNUAL] | Renewal date: [DATE or UNKNOWN]
> Earliest enforceable effective date: [EFFECTIVE_DATE]
> Comm_action: [COMM_ACTION from routing CSV]
> Postgres live data ([YYYY-MM-DD]): active_org_users=[N] | logged_in_90d=[N] | total_logins_90d=[N] | ltm_orders=[N] | ltm_gmv=$[N] | ltm_customers_served=[N]
> CEO awareness required before send: NO
> Expansion eligible: [YES/NO] — [NOTE; per `_root/07 §7` Format A required field]
>
> Conditional rows — include only when the condition holds, per `_root/07 §7` conditional-fields table:
> - `> **⚠️ SUPPORT FIRE: [N] days open. Production-ready. Operator decides send timing.**` — insert immediately after `Support fire:` row when `support_fire = TRUE`.
> - `> ⚠️ CEO PRE-CALL REQUIRED — arrangement was negotiated by [NAME]. Do not send at CSM level before CEO confirms.` — when `migration_driver = special_arrangement` AND `angies_notes` / `discount_drivers` reference a named executive as originator.
> - `> ⚠️ USER BILLING RECONCILIATION NEEDED — billed amount implies [M] excess users ($Y/month) but stated trailing average implies [N] excess users ($X/month). Confirm before sending.` — when `_root/07 §4.5` discrepancy threshold tripped.
> - `> Billing entity: [NAME] — notice routes to billing contact` — when `billing_entity` is non-blank AND ≠ `company`.
> - `> Tenure acknowledgment required: YES — [YEARS] years (cohort [COHORT_YEAR])` — when `cohort_year ≤ 2016` (early adopter).
>
> Routing-block edits: if Postgres data was unavailable for any sub-field, render the fallback per `_root/07 §5` (e.g. `Postgres live data: UNAVAILABLE — fell back to composite_narrative` for §4.1 failure; `ltm_orders = 0 — value anchor omitted` for §4.3 empty). Do not delete the line — render the prescribed fallback per the §5 table.

---

# [ACCOUNT_NAME]: Your Pricing Is Changing

*Prepared for [ACCOUNT_NAME] | [DATE]*

---

> **Section 3b — Lede block (Thriving / Healthy accounts only).**
>
> The drafter writes a 2–3 sentence lede that names the relationship before the number, per `_root/04 §4.1`. This is the ONE section of the brief where the prose is drafter-generated rather than pasted from a `_root/` block — the lede is tuned to the specific account.
>
> **Apply at every Format A lede (Thriving / Healthy only):**
> - Per `_root/04 §4.1`: lead with the relationship (tenure + at least one account-specific stat), deliver the dollar / date second. Tenure-band variants live in §4.1; substitute by `cohort_year` from v6.2.
> - Per `_root/04 §4.2`: use unambiguous platform metrics (tenure, active users, session volume, surfaces in use). Order counts are supporting evidence only; when used, scope explicitly to "orders submitted through SuperCat" or "eCat orders" — never the account's total order volume. No provisioned-vs.-active ratio. No per-order subscription cost in the lede.
> - Per `_root/04 §4.7`: when `cohort_year ≤ 2015`, include the early-adopter tenure paragraph (the Format B variant — `_root/04 §4.7` carries the verbatim text and the named-year framing).
> - Per `_root/04 §4.14`: when `migration_driver = platform_discount_correction`, the lede framing block's "rate at signing" sentence is replaced by the §4.14 verbatim substitution.
>
> **Skip this block entirely if `health_band ∈ {Watch, At Risk, Critical}` OR `value_delivery_score < 40`.** The §4.13 health-band override suppresses the relationship-stats lede and the "What You've Built" section; the brief opens with the standalone dollar-change sentence in Section 3c below. (Note: a Watch / At-Risk / Critical Format A is rare per `_root/02 §4` + `_root/06 §4.2` — the health override typically routes the account to Strategic. The lede-suppression rule is preserved here for the rare edge case where Format A still applies.)
>
> **Postgres data sourcing for lede stats** (per `_root/07 §4`):
> - `total_logins_90d` from `_root/07 §4.2`.
> - `active_org_users` and `logged_in_90d` from `_root/07 §4.2` — load into the routing block; per `_root/04 §4.2`, never expressed as a provisioned-vs.-active ratio in client copy.
> - `ltm_orders` and `ltm_customers_served` from `_root/07 §4.3` — when surfaced, framed as "eCat orders" per `_root/07 §4.3` rendering constraint.
> - Tenure: `cohort_year` from v6.2.
> - "Surfaces in use": derived from drafter judgment + v6.2 `current_stack` + Postgres activity.
> - Fallback when Postgres unavailable: `composite_narrative` from v6.2 per `_root/07 §5`; note the fallback in the routing block.
>
> **[LEDE_PARAGRAPH — 2–3 sentences; relationship first, dollar / date second; follows `_root/04 §4.1` + `§4.2` + (if cohort_year ≤ 2015) `§4.7` + (if migration_driver = platform_discount_correction) `§4.14`.]**

---

> **Section 3b-continued — "What You've Built on SuperCat" sub-section (Thriving / Healthy accounts only).**
>
> A short data-point list that demonstrates the writer looked at this specific account. Per `_root/04 §4.2` lede stat guardrail and `_root/01 §5` ("the artifact is the case") — each sentence is one fact, frame each stat as the client's own output, lead with unambiguous platform metrics. Skip the section entirely if fewer than 2 data points are available; do not estimate.
>
> Suppress this section for Watch / At Risk / Critical / VD<40 accounts (per `_root/04 §4.13` — same rule that suppresses the lede block).

## What You've Built on SuperCat

[PLATFORM_STATS — 3–4 single-fact sentences using confirmed Postgres §4.1 / §4.2 / §4.3 data + v6.2 `cohort_year` only. Same guardrails as the lede paragraph per `_root/04 §4.2` (no provisioned-vs.-active ratio; no per-order subscription cost; eCat-scoped order counts only).]

---

> **Section 3c — Effective-date sentence (always present, for all health bands).**
>
> The standalone dollar-change sentence is owned by `_root/04 §4.13`. For Thriving / Healthy accounts this is the second sentence after the lede paragraph; for Watch / At Risk / Critical / VD<40 accounts (Section 3b skipped) this IS the lede. Per operator-stamped strict-placeholder precedent 2026-05-26 (Stage 3.1 review pass): the sentence is fetched from §4.13, never inlined here, even though it has only 4 bracketed tokens — preserves path-reference contract end-to-end.
>
> [INSERT `_root/04 §4.13` standalone sentence — verbatim, with `[EFFECTIVE_DATE]`, `[CURRENT_MRR]`, `[NEW_MRR]`, `[DELTA]`, `[DELTA_PCT]` substituted from v6.2 per `_root/07 §2`.]

---

> **Section 3d — Consolidated 2026 framing sentence.**
>
> Per `_root/04 §3` row on the consolidated 2026 sentence: replace the legacy "SuperCat is standardizing its pricing..." phrasing with the operator-stamped iteration. Drafter pastes the sentence verbatim from `_root/04 §3` (the table row's "Replacement" column carries the canonical text).
>
> [INSERT `_root/04 §3` consolidated 2026 sentence — verbatim, no substitution.]

---

> **Section 3e — Tenure-aware variant sentence.**
>
> One short sentence after the consolidated 2026 sentence that names the account's signing-year context. Per `_root/04 §4.1` tenure-band variants:
> - `cohort_year ≤ 2015` (10+ year tenure): use the §4.1 long-tenure variant — "Your rate has been unchanged since [YEAR] — this is the first time we've adjusted it." (verbatim per §4.1).
> - `2016 ≤ cohort_year ≤ 2021` (≤5 year tenure typical for Format A's near-flat scope): use the §4.1 standard variant — "Your rate was set in [YEAR] — this is the first time we've updated it." (verbatim per §4.1).
> - `migration_driver = platform_discount_correction`: REPLACE this sentence entirely with the `_root/04 §4.14` discount-correction substitution — "Your rate reflects a discount applied at signing that's being retired as part of this change." (verbatim per §4.14). The tenure-aware variant is NOT used when §4.14 fires.
>
> [INSERT one of: `_root/04 §4.1` tenure-aware variant (selected by `cohort_year`), OR `_root/04 §4.14` substitution (when `migration_driver = platform_discount_correction`). Verbatim; substitute `[YEAR]` from `cohort_year`.]

Below is exactly why your number is changing and what you're getting at the new price.

---

## Why the Number Is Changing

> **Section 3f — Driver dispatch.**
>
> The drafter selects ONE block based on the account's v6.2 `migration_driver` value and pastes the named `_root/05 §N.M` block verbatim into the `[INSERT_DRIVER_BLOCK]` placeholder below. The block prose is owned by `_root/05`; the template carries the dispatch table only.
>
> | v6.2 `migration_driver` | Insert `_root/05` block verbatim from | Notes |
> |---|---|---|
> | `user_rate_normalization` | `_root/05 §2.1.4` | Format A canonical block. Apply `_root/04 §4.9` billing-basis footnote after the pricing table per `_root/05 §2.1.6`. |
> | `platform_discount_correction` | `_root/05 §2.2.4` | Format A canonical (driver renamed from `discount_correction` per CL-011 + Wave 3.1 review). The lede already carries the `_root/04 §4.14` substitution; do not re-state. |
> | `at_book_tier_shift` | `_root/05 §2.5.4` | Format A canonical. The §2.5.4 block carries an `[INSERT _root/04 §4.6 verbatim sentence]` placeholder (per CL-013 cleanup applied 2026-05-26 at source). Drafter pastes §2.5.4, then fetches the `_root/04 §4.6` sentence and substitutes it into the placeholder. OMIT the §4.6 sentence when `new_tier_base < current_platform_mrr` (kii exemplar pattern per `_root/05 §2.5.6` special case). |
> | `multi_org_retirement` | `_root/05 §2.6.4` | Format A canonical (carries the additional "every entity is making the same move" paragraph that Format B / CEO Letter omit). Account is also part of an entity packet per `_root/02 §3` + `_root/05 §2.6.6`. |
> | `special_arrangement` | `_root/05 §2.8.4` | Format A canonical. When `delta_pct > 30%`, apply `_root/04 §4.4` high-delta lede rule per `_root/05 §2.8.6` (rare in Format A given the ≤10% scope but possible at the Δ_mrr ≤ $80 boundary). |
> | `module_compression` (decrease-side near-flat only) | `_root/05 §3.1.3` | Format A near-flat variant for decrease accounts that don't route to Good News. Account-distribution note in `_root/05 §3.1.1`: Tailwind (ml/gc/dccl/pf) routes to Format A's `module_compression` block; Annual (mali/mah) and Strategic (ap/mfc) are governed by overlays in `_root/06 §4.2`/`§4.3`. |
> | `tier_base_increase` | NOT carried in Format A | Forward-reference to `_root/05 §2.3.4`. If routing produces this driver in Format A, the routing is suspect — escalate per `_root/CONTRACTS.md §2`. |
> | `included_user_reduction` | NOT carried in Format A | Forward-reference to `_root/05 §2.4.4`. If routing produces this driver in Format A, escalate per `_root/CONTRACTS.md §2`. |
> | `annual_discount_retirement` | NOT carried in Format A | Forward-reference to `_root/05 §2.7.4`. If routing produces this driver in Format A, escalate per `_root/CONTRACTS.md §2`. |
> | `user_count_variance`, `rate_architecture` | NOT carried in Format A | Good News only per `_root/05 §3.2` / `§3.3`. If routed to Format A, escalate. |
> | `already_migrated` | n/a | Status-marker leak per `_root/05 §1.4`; loader filters per `_root/07 §3`. No brief drafted. |

**Driver: [DRIVER]**

[INSERT_DRIVER_BLOCK — paste the verbatim block from the `_root/05 §N.M` named in the dispatch table above; substitute every bracketed token from v6.2 + Postgres per `_root/07 §2` + `§4`. The block carries its own pricing-table row template per `_root/05 §N.5` — paste that too, immediately after the driver prose; format-A row-phrasing variants are noted inside each `_root/05 §N.5`.]

> **Section 3g — Secondary-driver weaving (conditional).**
>
> [IF v6.2 `secondary_drivers` is non-empty: consult `_root/05 §4` (secondary-driver weaving matrix) and apply the named integration pattern within the driver block above — never as a separate section per `_root/05 §1.3`. If no entry in `_root/05 §4` covers the combination, escalate per `_root/CONTRACTS.md §2`. Note: Format A's mechanical scope means the kii exemplar's per-account narrative pattern (ABTS primary + IUR-style included-base move integrated inline) is the canonical Format A precedent for inline integration — see `_root/05 §2.5.7` and `_root/05 §4` Format A note.]

> **Section 3h — Pricing-table row template (per driver).**
>
> The pricing table immediately follows the driver prose. The row template is owned by the driver's `_root/05 §N.5` block (URN: `§2.1.5`; PDC: `§2.2.5`; ABTS: `§2.5.5`; MOR: `§2.6.5`; SA: `§2.8.5`; MC: `§3.1.4`). Format A's row 1 phrasing carries small variants per driver (e.g. `(custom arrangement, [YEAR])` for SA, `($[N]% below book) / (standard)` for PDC) — those variants live in `_root/05 §N.5` and are applied at paste time.
>
> **Billing-basis footnote** — required only for URN per `_root/04 §4.9` (Format A does not carry IUR primary). Drafter pastes the `_root/04 §4.9` verbatim italicized sentence immediately after the URN pricing table, before the next `---` separator.

[Optional follow-up sentence per `_root/05 §2.1.4` Format A URN block: if the included-base expansion absorbs users or produces a net negative on user charges, the drafter writes one short calibration sentence per the "Optional" placeholder in §2.1.4. The sentence is operator-judgment territory; the §2.1.4 placeholder text gives the canonical shape ("The new included base absorbs [N] of your current additional users...").]

---

## What You're Getting at $[NEW_MRR]/Month

> **Section 3i — Tier verbatim block.**
>
> Drafter pastes the verbatim "What You're Getting at $X" block for the account's `assigned_tier` from `_root/03 Section 1` (T1 / T2 / T3). Substitute `[NEW_INCLUDED]` from v6.2 `included_users` (T1 default 10, T2 default 15; T3's block hard-codes "Up to 40 users" per `_root/03 §1` T3 drafter note — no substitution).
>
> [INSERT `_root/03 Section 1` — [T1 — Catalog Essentials | T2 — Commerce Professional | T3 — Commerce Enterprise] verbatim block — verbatim, with `[NEW_INCLUDED]` substituted from v6.2 `included_users` per `_root/07 §2` for T1 and T2; T3's block carries hard-coded "Up to 40 users" per `_root/03 §1` drafter note.]

---

## What's Coming in 2026

> **Section 3j — Roadmap verbatim block (CL-005: mandatory across all 4 formats per operator decision 2026-05-22).**
>
> Drafter pastes the verbatim "What's Coming in 2026" block from `_root/03 Section 3`. The trailing `*[Operator note — remove before sending: …]*` line inside the §3 block is removed before send per `_root/04 §2.14` (operator-note removal as non-negotiable) and QB-046 in `_root/08`.
>
> [INSERT `_root/03 Section 3` verbatim block — verbatim, no substitution; remove the trailing operator-note line before send.]

---

> **Section 3k — "How This Compares" section (conditional; drafter judgment whether to include).**
>
> [IF the drafter judges that a peer-positioning sentence adds clarity for this account AND `_root/04 §4.11` indicates the section is appropriate: include the section using the `_root/04 §4.11` structure. Otherwise: omit the section entirely.]
>
> **If included, the section follows `_root/04 §4.11` exactly:**
> - **No peer dollar ranges anywhere in client copy** — CL-003 + operator stamp 2026-05-22 universal. Peer dollar values (the T1 / T2 / T3 floor / midpoint / ceiling table in `_root/03 §5`) stay INTERNAL-ONLY; they appear in the operator's prep sheet, not in this brief.
> - **No "equivalent platforms" / unnamed-competitor pricing sentence** — CL-004 + operator stamp 2026-05-22 universal. Strike the sentence the archived Format A template carried for T3 accounts; it is forbidden in every format per `_root/04 §3` row on competitor-pricing references.
> - **No "no account-specific adjustments" sentence** — CL-001 + `_root/04 §3` row. Delete entirely; never write it.
> - **Use the plain-English position vocabulary** from `_root/04 §4.11`: "at the base rate" / "below the midpoint" / "near the midpoint" / "above the midpoint". Compute the position against the tier midpoint using the INTERNAL-ONLY peer-range table in `_root/03 §5` (drafter check only, never quoted to the customer).
> - **Apply `_root/04 §4.3`** when the computed position is "above the midpoint": the mandatory user-count clause naming team size explicitly while confirming the platform base is at the tier standard.
> - **Apply `_root/04 §4.11` canonical client-facing form** — one position sentence + one structural-fairness sentence ("This is the same structure going to every account we work with"). The structural-fairness sentence echoes `_root/04 §2.7` non-negotiable.

## How This Compares

[INSERT — section structure per `_root/04 §4.11` if drafter judgment supports inclusion; otherwise omit the entire `## How This Compares` heading. Position vocabulary per `_root/04 §4.11`; user-count clause per `_root/04 §4.3` when "above the midpoint" applies; structural-fairness sentence per `_root/04 §2.7` / §4.11.]

---

> **Section 3l — "What This Works Out To" value-anchor section (conditional).**
>
> [IF derived metric `cost_per_order < $200` per `_root/04 §4.8` (operator-stamped 2026-05-22): include the value-anchor section using `_root/04 §4.8` structure. Otherwise: omit the section entirely.]
>
> **Drafter computes** `cost_per_order` and `delta_per_order` per `_root/07 §4.4` formulas using `new_total_mrr` from v6.2 and `ltm_orders` from Postgres §4.3. **Inclusion gates per `_root/04 §4.8`**: `ltm_orders > 0` AND `cost_per_order < $200`. Append the second sentence (delta-per-order reframe) iff `delta_per_order < $50`; otherwise omit the second sentence. If `ltm_orders = 0` OR `cost_per_order ≥ $200`, omit the entire section. Operator-judgment borderline cases: log the inclusion decision in the routing block.
>
> **Flag for the planning agent**: the three Format A archived v2 exemplars (`kal`, `kii`, `lss`) omit this section in cases where the inclusion gates would have fired under the current `_root/04 §4.8` threshold (operator-stamped 2026-05-22). The exemplars predate the $200 stamp; under the current rule, kii and lss would include the section. This is evidence the exemplars need regeneration when Stage 4 production drafting begins — surfaced in this template's conformance gaps list, not changed at template build time.

## What This Works Out To

[INSERT — section structure per `_root/04 §4.8` if the inclusion gates fire; otherwise omit the entire `## What This Works Out To` heading. Drafter substitutes `[ltm_orders]`, `[COST_PER_ORDER]`, `[DELTA_PER_ORDER]` from `_root/07 §4.4` derivations.]

---

## Your Pricing at a Glance

> **Section 3l-continued — Pricing-at-a-glance summary table (every Format A brief).**
>
> A short summary table that recaps the dollar change, the tier label, and the included-users move. The table's column / row layout is template scaffolding (drafter-facing structure), not rule prose. Every value the drafter substitutes is sourced from v6.2 + the driver block above per `_root/07 §2`, or from `_root/03 §2 Block A` for the graduated-rate ladder summary string.
>
> The annual rows surface `current_mrr × 12` and `new_total_mrr × 12`. The "Additional user rate" row uses the legacy rate before; the after-column value is fetched from `_root/03 §2 Block A` per the strict-placeholder precedent operator-stamped 2026-05-26 (Stage 3.1 review pass) — the canonical ladder values live in §2 Block A alone, not inline here.

| | Before | After |
|---|---|---|
| **Monthly** | $[CURRENT_MRR] | **$[NEW_MRR]** |
| **Annual** | $[CURRENT_ARR] | **$[NEW_ARR]** |
| **Change** | — | +$[DELTA]/month ([DELTA_PCT]) |
| **Tier** | [LEGACY_TIER_LABEL] | [NEW_TIER_LABEL] |
| **Included users** | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| **Additional user rate** | $[LEGACY_RATE]/user | [INSERT `_root/03 §2 Block A` graduated-rate summary string verbatim — e.g. "Graduated ($25/$22/$20/$18)" per current §2 Block A canonical values] |

---

> **Section 3m — Operations-unchanged paragraph.**
>
> Drafter pastes one sentence per `_root/04 §4.5`:
> - DEFAULT variant — unless v6.2 `secondary_drivers` includes `included_user_reduction`.
> - IUR-FORK variant — when `secondary_drivers` includes `included_user_reduction` (per `_root/04 §4.5` IUR fork condition; `_root/04 §2.13` non-negotiable; cross-references `_root/05 §2.1.7` for Format A's URN+IUR pattern and `_root/05 §2.5.7` for the kii ABTS+IUR-style pattern).
>
> [INSERT `_root/04 §4.5` sentence — DEFAULT variant unless v6.2 `secondary_drivers` includes `included_user_reduction`; in that case, INSERT `_root/04 §4.5` IUR-fork variant. Verbatim — copy character-for-character.]

---

## What Happens Next

> **Section 3n — Close paragraph (Format A passive offer).**
>
> Drafter pastes the verbatim Format A close from `_root/04 §4.12` — the passive offer that distinguishes Format A from Format B's active meeting offer and from the CEO Letter's specific-date call commitment.
>
> [INSERT `_root/04 §4.12` Format A close — verbatim, passive variant. Substitute `[EFFECTIVE_DATE]`.]

> **Formal-notice line (immediately after the close, per `_root/04 §4.12`).**
>
> Required for Format A per `_root/04 §4.12`'s "immediately after each close, except Good News" instruction. Drafter pastes the verbatim italicized formal-notice line from `_root/04 §4.12`; substitute `[EFFECTIVE_DATE]`.
>
> [INSERT `_root/04 §4.12` formal-notice line — verbatim italicized form. Substitute `[EFFECTIVE_DATE]`.]

*Prepared [DATE]*

---

> **Section 4 — Pre-send drafter checklist.**
>
> The complete pre-send checklist is the 126-check `_root/08` Quality Bar; the drafter runs every QB-NNN whose `Applies to:` field covers Format A or "all formats" before posting the conformance block. The checks below are the Format-A-specific blockers most often surfaced during drafting — they are convenience pointers only; consulting `_root/08` directly is canonical.
>
> Drift-control + conformance (every session):
> - **QB-001** — manifest-echo contract.
> - **QB-002** — conformance block present in final reply, canonical format per `_root/00_manifest.md §5`.
> - **QB-003** — files-read completeness.
> - **QB-004** — no unauthorized archive reads.
> - **QB-007** — no rule restated outside its owning `_root/` doc.
>
> Routing (this brief is the right brief for this account):
> - **QB-011** — `ord_id` resolves cleanly to one v6.2 row, not filtered.
> - **QB-013** — format derived from the 6-step routing-decision flow per `_root/06 §2`.
> - **QB-018** — Δ_pct / Δ_mrr boundary handled per `_root/06 §3` precedence rule.
> - **QB-019** — entity-children do NOT receive a standalone Format A brief.
> - **QB-024** — brief written to `format-a-notices/`.
>
> Data-pipeline:
> - **QB-028** — canonical loader from `_root/07 §3`.
> - **QB-030** — three Postgres queries verbatim from `_root/07 §4`.
> - **QB-031** — derived metrics computed per `_root/07 §4.4`.
> - **QB-032** + **QB-110** — user-billing reconciliation per `_root/07 §4.5`; ⚠️ flag if threshold tripped.
> - **QB-036** + **QB-037** — routing block complete per `_root/07 §7` Format A matrix (including the Format-A-required `Expansion eligible` field).
>
> Voice / content (the highest-density section in `_root/08`):
> - **QB-040** / **QB-062** — lede leads with dollar + date, not percentage.
> - **QB-043** / **QB-068** / **QB-069** — no health bands or dimension scores in client copy.
> - **QB-045** / **QB-072** — universality claim uses "every account we work with" without hedge.
> - **QB-046** — "What's Coming in 2026" present verbatim from `_root/03 §3`; operator-note line stripped.
> - **QB-047** — internal routing-note blockquote removed from delivered version.
> - **QB-054** — no competitor-pricing reference (named OR unnamed).
> - **QB-059** — no "no account-specific adjustments" sentence.
> - **QB-071** — no peer-range dollar values anywhere in client copy.
> - **QB-077** — "above the midpoint" carries the `_root/04 §4.3` user-count clause.
> - **QB-079** — `_root/04 §4.5` operations-unchanged sentence verbatim; correct variant for the secondary-driver state.
> - **QB-080** — `_root/04 §4.6` platform-base-grown sentence verbatim with correct cohort year (when applicable — including the §2.5.4 placeholder for `at_book_tier_shift`).
> - **QB-082** — value-anchor inclusion / exclusion respects the `_root/04 §4.8` $200 threshold.
> - **QB-083** — billing-basis footnote verbatim after URN pricing table.
> - **QB-085** — "How This Compares" position vocabulary only; no peer-range dollars.
> - **QB-086** — Format A close verbatim per `_root/04 §4.12`; formal-notice line present.
> - **QB-087** — Watch / At Risk / Critical / VD<40 lede override applied if triggered.
> - **QB-088** — `_root/04 §4.14` discount-correction substitution applied when `migration_driver = platform_discount_correction`.
>
> Driver content:
> - **QB-089** — driver block verbatim from `_root/05 §N.M` for Format A.
> - **QB-090** — every bracketed placeholder substituted from v6.2 / Postgres.
> - **QB-091** — conditional sub-blocks (`[IF ...]`) rendered iff condition holds.
> - **QB-092** — secondary-driver weaving integrated within the primary block, not separately.
> - **QB-095** — no improvised content for drivers Format A does not carry (TBI, IUR, ADR).
>
> Product / pricing language:
> - **QB-099** — tier block verbatim from `_root/03 §1`.
> - **QB-100** — user-rate ladder uses the 1–10 / 11–25 / 26–50 / 51+ bands (`_root/03 §2 Block A`).
> - **QB-101** + **QB-102** — no unpublished SKU names, no INTERNAL peer / competitive tables in client copy.
>
> Math reconciliation:
> - **QB-104** — pricing-table Before total = `current_mrr`; After total = `new_total_mrr` exactly.
> - **QB-105** — stated Δ MRR = `new_total_mrr − current_mrr` within ±$1.
> - **QB-107** — `tier_base` and `included_users` match the assigned tier in `_root/03 §1`.
> - **QB-108** — boundary cases reconcile with `_root/06 §3` precedence.
> - **QB-110** — user-billing reconciliation per `_root/07 §4.5`.
> - **QB-111** — `support_fire = TRUE` ⚠️ flag handled correctly.
>
> The above is convenience indexing. The full `_root/08` checklist (drift-control §3, routing §4, data-pipeline §5, voice / content §6, math §7, audit-only §8, cross-doc §9) is the canonical pre-send gate. Drafter pastes Format-A-applicable QB-NNN results into the conformance block per `_root/00_manifest.md §5`.

---

*Cross-references: `_root/00_manifest.md` (required-reading map); `_root/CONTRACTS.md §5` (path-reference contract — this template carries pointers only, not rule prose); `_root/02 §1` (segment definitions Format A draws from: Core, Narrative-subset, Annual-natural-tier, Tailwind-MC); `_root/02 §3` / `§4` / `§5` (overlay rules that gate Format A); `_root/03 §1` (tier verbatim blocks); `_root/03 §2 Block A` (user-rate ladder); `_root/03 §3` ("What's Coming in 2026"); `_root/04` (voice rules — see Section 4 checklist for the relevant subsections); `_root/05 §2.1.4` / `§2.2.4` / `§2.5.4` / `§2.6.4` / `§2.8.4` / `§3.1.3` (Format A driver blocks); `_root/05 §4` (secondary-driver weaving matrix); `_root/06 §1` (Format A definition); `_root/06 §2` (routing-decision flow); `_root/06 §3` (delta-tier dispatch + precedence); `_root/06 §4` (overrides); `_root/07 §2` (v6.2 field guide); `_root/07 §4` (Postgres queries); `_root/07 §5` (fallback rules); `_root/07 §6` (file naming); `_root/07 §7` (routing-block matrix — canonical); `_root/08` (Quality Bar — 126 QB-NNN checks); `_meta/stage3_cleanup.md` (CL-001 / CL-003 / CL-004 / CL-005 / CL-011 / CL-013 history).*
