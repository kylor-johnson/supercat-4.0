# Format B — Notice + Meeting Offer (and CEO Pre-Call → Format B) — Brief Template
*CS-led | Meaningful delta ($81 ≤ Δ ≤ $399 standard; Δ ≥ $600 with CEO Pre-Call) | Meeting-offer close per `_root/04 §4.12`*

---

> **Operator notes — drafter-facing scaffolding; remove this entire blockquote before sending.**
>
> **When to use this template.** Format B is the CS-led 60-Day Notice with an active meeting-offer close. Two routing patterns land in this template: (a) standard Format B — Notice + Meeting Offer for `$81 ≤ Δ ≤ $399` per `_root/06 §3`; (b) CEO Pre-Call → Format B for `Δ ≥ $600` per `_root/06 §1` (5th routing pattern) + `_root/06 §3` row 5 — the CEO has personally pre-engaged the account by phone BEFORE CS sends this brief. The mechanical scope, the 6-step routing-decision flow, the higher-touch-wins precedence rule, and the dispatch table are all defined in `_root/06 §1`, `§2`, and `§3`. Do not restate them here; consult `_root/06` when in doubt.
>
> **Who sends.** CS team — Kylor — per `_root/06 §1`. For the CEO Pre-Call → Format B variant, the CEO has already called the account; the CEO does NOT sign this brief (signing the brief is the CEO Letter format per `_root/06 §1`). CS still sends; CEO awareness is confirmed in the routing block per `_root/07 §7` Format B matrix.
>
> **What this template is NOT for.**
> - Δ ≤ $80 / Δ_pct ≤ 10% (Format A — 60-Day Notice): out of scope per `_root/06 §3` dispatch table.
> - `$400 ≤ Δ ≤ $599` (CEO Letter + Call Commitment): out of scope per `_root/06 §3` — that is the CEO-authored format per `_root/06 §1`.
> - `Δ < $0` (decrease-side): out of scope per `_root/06 §3` row 1 — routes to Good News.
> - Entity-children (`parent_entity` non-empty AND `parent_entity ≠ company`): fold into the entity packet per `_root/02 §3` and `_root/06 §4.1` — do NOT draft a standalone Format B.
> - Boundary cases ($75 / 12%; $700 / 8%): the higher-touch format wins per the `_root/06 §3` precedence rule. A $75 / 12% account routes to Format B (not Format A); a $700 / 8% account routes to CEO Pre-Call → Format B (not standard Format B or Format A). If the routing produces a counterintuitive Format B assignment, escalate per `_root/CONTRACTS.md §2`.
> - Watch / At Risk / Critical (`health_band ∈ {Watch, At Risk, Critical}` OR `value_delivery_score < 40`): the health override fires per `_root/02 §4` + `_root/06 §4.2`; the account is in `notice_cohort = 'Post-Migration'` and the brief is deferred until CEO-led stabilization. Critical-band routing is per-account per `post_hold_action` — consult the routing CSV directly per `_root/06 §4.2`. The §4.13 health-band lede override (Section 3b below) still applies on the rare Format-B-eligible health-flagged brief that survives stabilization.
> - `migration_driver ∈ {module_compression, user_count_variance, rate_architecture}` (decrease-side): out of scope per `_root/05 §3` — routes to Good News per `_root/06 §3` row 1. Format B's mechanical scope (Δ ≥ $81) does not produce decrease drivers. If the routing produces a Format B assignment with one of those primary drivers, the routing is suspect — escalate per `_root/CONTRACTS.md §2`.
>
> **Cleanup-tracker history embedded in this template.** Items applied as of authoring date: CL-001 (no "no account-specific adjustments" sentence anywhere — the archived Format B template already omits it; absence preserved via `_root/04 §4.11` structure); CL-002 (value-anchor threshold uses `cost_per_order < $200` per `_root/04 §4.8` operator stamp 2026-05-22 — NOT the archived $35); CL-003 (no peer dollar ranges in client copy — universal per operator stamp 2026-05-22; archived Format B template already strips, preserved); CL-004 (no "equivalent platforms" / unnamed-competitor pricing sentence anywhere — `_root/04 §3` row on competitor-pricing prohibition); CL-005 (mandatory "What's Coming in 2026" block via `_root/03 §3` pointer — ADDED to Format B; the archived Format B template omits this entirely, this is the most additive change in the rebuild); CL-012 (the `tier_base_increase` dispatch row references `_root/05 §2.3.2` and follows whatever marker §2.3.2 currently carries — marker state reported in conformance block); CL-016 (the `multi_org_retirement` dispatch row references `_root/05 §2.6.2` + `§2.6.6` IUR-secondary conditional context + `§4` weaving matrix per operator stamp 2026-05-22; current state of `_root/05`'s templated IUR-secondary coverage reported in conformance block). See `_meta/stage3_cleanup.md` for full item history.
>
> **Drafter's responsibility.** Every `_root/XX §N.M` reference in this template is to a canonical rule doc. At draft time, the drafter (a) opens the referenced section, (b) copies the named verbatim content character-for-character, (c) substitutes any `[BRACKETED_TOKEN]` placeholders from v6.2 + Postgres data per `_root/07 §2` + `§4`. The template carries pointers; it does not carry rule prose. Pre-send: run the `_root/08` Quality Bar against the completed draft (the QB-NNN list under "Section 4 — Pre-send drafter checklist" below names the Format-B-specific blockers; the full 126-check checklist lives in `_root/08`).
>
> **Conformance block.** The drafter ends the session with the canonical conformance block defined in `_root/00_manifest.md §5`.

---

> **Section 2 — Internal routing note** (drafter-facing; remove before sending — matches the canonical field list per `_root/07 §7` for Format B; field names and order match `_root/07 §7` exactly):
>
> Brief type: `Format B — Notice + Meeting Offer` | meaningful delta
> Account: [ACCOUNT_NAME] | Tier: [T1/T2/T3] | Wave: [WAVE]
> Migration driver: [DRIVER] | Health: [HEALTH_SCORE] — [HEALTH_BAND] | Risk label: [RISK_LABEL]
> Engagement: [E] | Adoption: [A] | Value Delivery: [VD] | Ops Health: [OH]
> Support fire: [YES/NO] | Behavioral floor applied: [YES/NO]
> Delta: [DELTA_PCT] (+$[DELTA_MRR]/month)
> Cohort: [COHORT_YEAR]
> Contract: [MONTHLY/ANNUAL] | Renewal date: [DATE or UNKNOWN]
> Earliest enforceable effective date: [EFFECTIVE_DATE]
> Comm_action: [Format B — Notice + Meeting Offer / CEO Pre-Call → Format B] (from routing CSV per `_root/06 §5`)
> Postgres live data ([YYYY-MM-DD]): active_org_users=[N] | logged_in_90d=[N] | total_logins_90d=[N] | ltm_orders=[N] | ltm_gmv=$[N] | ltm_customers_served=[N]
> CEO awareness required before send: [NO for standard Notice + Meeting Offer / YES for CEO Pre-Call → Format B] (per `_root/07 §7` Format B matrix — conditional on `comm_action`)
>
> Conditional rows — include only when the condition holds, per `_root/07 §7` conditional-fields table:
> - `> **⚠️ SUPPORT FIRE: [N] days open. Production-ready. Operator decides send timing.**` — insert immediately after `Support fire:` row when `support_fire = TRUE`.
> - `> ⚠️ CEO PRE-CALL REQUIRED — arrangement was negotiated by [NAME]. Do not send at CSM level before CEO confirms.` — when `migration_driver = special_arrangement` AND `angies_notes` / `discount_drivers` reference a named executive as originator.
> - `> ⚠️ USER BILLING RECONCILIATION NEEDED — billed amount implies [M] excess users ($Y/month) but stated trailing average implies [N] excess users ($X/month). Confirm before sending.` — when `_root/07 §4.5` discrepancy threshold tripped.
> - `> Billing entity: [NAME] — notice routes to billing contact` — when `billing_entity` is non-blank AND ≠ `company`.
> - `> Tenure acknowledgment required: YES — [YEARS] years (cohort [COHORT_YEAR])` — when `cohort_year ≤ 2016` (early adopter).
>
> Routing-block edits: if Postgres data was unavailable for any sub-field, render the fallback per `_root/07 §5` (e.g. `Postgres live data: UNAVAILABLE — fell back to composite_narrative` for §4.1 failure; `ltm_orders = 0 — value anchor omitted` for §4.3 empty). Do not delete the line — render the prescribed fallback per the §5 table.
>
> Note: Format B's routing block does NOT carry `Expansion eligible` (that field is Format A only per `_root/07 §7` matrix) and does NOT carry `CEO call commitment date` / `CEO name for sign-off` (those are CEO Letter only per `_root/07 §7` matrix).

---

# [ACCOUNT_NAME]: Your Pricing Is Changing

*Prepared for [ACCOUNT_NAME] | [DATE]*

---

> **Section 3b — Lede paragraph (Thriving / Healthy accounts only).**
>
> The drafter writes a 2–3 sentence lede that names the relationship before the number, per `_root/04 §4.1`. This is the ONE section of the brief where the prose is drafter-generated rather than pasted from a `_root/` block — the lede is tuned to the specific account. Format B's lede integrates tenure into the opening sentence as a relationship signal and lands the dollar change in the same paragraph.
>
> **Apply at every Format B lede (Thriving / Healthy):**
> - Per `_root/04 §4.1`: lead with the relationship (tenure + at least one account-specific stat), deliver the dollar / date second. Tenure-band variants live in §4.1; substitute by `cohort_year` from v6.2.
> - Per `_root/04 §4.2`: use unambiguous platform metrics (tenure, active users, session volume, surfaces in use). Order counts are supporting evidence only; when used, scope explicitly to "orders submitted through SuperCat" or "eCat orders" — never the account's total order volume. No provisioned-vs.-active ratio. No per-order subscription cost in the lede.
> - Per `_root/04 §4.4`: when `delta_pct > 30%`, the lede MUST name the annual dollar impact alongside the monthly change (Format B variant — "a change of $[DELTA]/month ($[DELTA × 12]/year)" inside the same sentence). This is more common in Format B than in Format A given Format B's $81–$399 scope.
> - Per `_root/01 §1` relationship-before-price principle: the lede's organizing principle.
>
> **Skip the relationship-stats lede entirely if `health_band ∈ {Watch, At Risk, Critical}` OR `value_delivery_score < 40`.** The §4.13 health-band override suppresses the relationship-stats lede; the brief opens with the standalone dollar-change sentence (Section 3c below; same sentence, no preceding relationship stats). Most health-flagged accounts route to Strategic per `_root/02 §4` + `_root/06 §4.2`; the lede-suppression rule is preserved here for the rare Format-B-eligible edge case.
>
> **CEO Pre-Call → Format B variant**: when `comm_action = "CEO Pre-Call → Format B"`, the lede may reference the CEO conversation that preceded the brief (per `_root/04 §4.12` Format B close register + the variant pattern documented in the archived Format B delivery email's operator notes). The exact phrasing is per-account narrative; the brief's structural rule is unchanged — the lede still names the relationship first and lands the dollar / date in the same paragraph per §4.1. Do not invent a new lede structure; the §4.1 form holds, with one account-specific sentence acknowledging the prior call.
>
> **Postgres data sourcing for lede stats** (per `_root/07 §4`):
> - `total_logins_90d` from `_root/07 §4.2`.
> - `active_org_users` and `logged_in_90d` from `_root/07 §4.2` — load into the routing block; per `_root/04 §4.2`, never expressed as a provisioned-vs.-active ratio in client copy.
> - `ltm_orders` and `ltm_customers_served` from `_root/07 §4.3` — when surfaced, framed as "eCat orders" per `_root/07 §4.3` rendering constraint.
> - Tenure: `cohort_year` from v6.2.
> - "Surfaces in use": derived from drafter judgment + v6.2 `current_stack` + Postgres activity.
> - Fallback when Postgres unavailable: `composite_narrative` from v6.2 per `_root/07 §5`; note the fallback in the routing block.
>
> **[LEDE_PARAGRAPH — 2–3 sentences; relationship first, dollar / date second; follows `_root/04 §4.1` + `§4.2` + (if delta_pct > 30%) `§4.4` + (if comm_action = "CEO Pre-Call → Format B") per-account adjustment per `_root/04 §4.12`. For Watch / At Risk / Critical / VD<40: skip this paragraph entirely; the brief opens with Section 3c below per `_root/04 §4.13`.]**

---

> **Section 3c — Effective-date sentence (always present, for all health bands).**
>
> The standalone dollar-change sentence is owned by `_root/04 §4.13`. For Thriving / Healthy accounts this is the second sentence after the lede paragraph; for Watch / At Risk / Critical / VD<40 accounts (Section 3b lede skipped) this IS the lede. Per the strict-placeholder precedent operator-stamped 2026-05-26 (Stage 3.1 review pass — `_root/09_changelog.md`): the sentence is fetched from §4.13, never inlined here, even though it has only 4 bracketed tokens — preserves the path-reference contract end-to-end.
>
> [INSERT `_root/04 §4.13` standalone sentence — verbatim, with `[EFFECTIVE_DATE]`, `[CURRENT_MRR]`, `[NEW_MRR]`, `[DELTA]`, `[DELTA_PCT]` substituted from v6.2 per `_root/07 §2`.]

---

> **Section 3d — Consolidated 2026 framing sentence.**
>
> Per `_root/04 §3` row on the consolidated 2026 sentence: replace the legacy "SuperCat is standardizing its pricing..." phrasing with the operator-stamped iteration. Drafter pastes the sentence verbatim from `_root/04 §3` (the table row's "Replacement" column carries the canonical text).
>
> [INSERT `_root/04 §3` consolidated 2026 sentence — verbatim, no substitution.]

---

> **Section 3e — Tenure-aware variant sentence (with PDC substitution).**
>
> One short sentence after the consolidated 2026 sentence that names the account's signing-year context. Per `_root/04 §4.1` tenure-band variants:
> - `cohort_year ≤ 2015` (10+ year tenure): use the §4.1 long-tenure variant — "Your rate has been unchanged since [YEAR] — this is the first time we've adjusted it." (verbatim per §4.1).
> - `2016 ≤ cohort_year` (≤5 year tenure typical for Format B's $81–$399 scope, though longer tenures also land here when the early-adopter paragraph in Section 3f does the heavier tenure work): use the §4.1 standard variant — "Your rate was set in [YEAR] — this is the first time we've updated it." (verbatim per §4.1).
> - `migration_driver = platform_discount_correction`: REPLACE this sentence entirely with the `_root/04 §4.14` discount-correction substitution — "Your rate reflects a discount applied at signing that's being retired as part of this change." (verbatim per §4.14). The tenure-aware variant is NOT used when §4.14 fires (per `_root/04 §4.14` posture rule).
>
> [INSERT one of: `_root/04 §4.1` tenure-aware variant (selected by `cohort_year`), OR `_root/04 §4.14` substitution (when `migration_driver = platform_discount_correction`). Verbatim; substitute `[YEAR]` from `cohort_year`.]

---

> **Section 3f — Early-adopter tenure paragraph (conditional).**
>
> [IF `cohort_year ≤ 2015`: insert the early-adopter tenure paragraph from `_root/04 §4.7` Format B variant. The paragraph names the year, names the years of tenure, and frames the platform-then-versus-platform-now distinction with the "fundamentally different product" framing. Verbatim per `_root/04 §4.7`. The archived Format B template inlined this as an "ADD FOR EARLY ADOPTER COHORTS" block; the new template references §4.7 instead per the path-reference contract.]
>
> [IF `cohort_year > 2015`: omit this section entirely.]
>
> [INSERT `_root/04 §4.7` Format B early-adopter tenure paragraph — verbatim, with `[YEAR]` substituted from `cohort_year`.]

---

Below is exactly why your number is changing and what you're getting at the new price.

---

## Why the Number Is Changing

> **Section 3g — Driver dispatch.**
>
> The drafter selects ONE block based on the account's v6.2 `migration_driver` value and pastes the named `_root/05 §N.M` block verbatim into the `[INSERT_DRIVER_BLOCK]` placeholder below. The block prose is owned by `_root/05`; the template carries the dispatch table only. Format B carries all 8 increase-side drivers; decrease-side drivers route to Good News per `_root/06 §3` and are flagged below for escalation if they ever appear on a Format B routing.
>
> | v6.2 `migration_driver` | Insert `_root/05` block verbatim from | Conditional sub-blocks + secondary handling | Notes |
> |---|---|---|---|
> | `user_rate_normalization` | `_root/05 §2.1.2` | `§2.1.6` (conditional context paragraphs — billing-basis footnote per `_root/04 §4.9`; platform-base-grown per `_root/04 §4.6`; platform-base conditional per `_root/04 §4.10`; early-adopter per `_root/04 §4.7`; IUR-variant close per `_root/04 §4.5` when secondary = IUR) + `§2.1.7` (URN + IUR secondary integration per the §2.1.2 `[IF excess users remain after new included base]` sub-block) | Format B canonical block. Most common driver (37 v6.2 accounts; 7 with IUR secondary). |
> | `platform_discount_correction` | `_root/05 §2.2.2` | `§2.2.6` (platform-base-grown per `_root/04 §4.6`; lede substitution already applied at Section 3e per `_root/04 §4.14`; no billing-basis footnote per `_root/04 §4.9`) + `§2.2.7` (no secondary combinations in v6.2) | Format B canonical. The Section 3e PDC substitution carries the discount-correction lede framing; do not re-state in the driver block. |
> | `tier_base_increase` | `_root/05 §2.3.2` | `§2.3.6` (platform-base-grown per `_root/04 §4.6`; no billing-basis footnote unless IUR involved per `_root/04 §4.9`; IUR-variant close per `_root/04 §4.5` when secondary = IUR; early-adopter per `_root/04 §4.7`) + `§2.3.7` (secondary combinations — see CL-012 note below) | Format B canonical. **CL-012 note**: the `_root/05 §2.3.2` block carries a `[IF secondary driver = …]` marker whose label may not match the integrated sentence's IUR-style content (see `§2.3.2` naming note). Drafter follows §2.3.2 verbatim — including whichever marker label §2.3.2 carries — and integrates the sub-paragraph when the v6.2 secondary configuration matches. The resolution of the marker label belongs to `_root/05 §2.3.2`, not to this template. |
> | `included_user_reduction` | `_root/05 §2.4.2` | `§2.4.6` (billing-basis footnote required per `_root/04 §4.9`; IUR-variant close required per `_root/04 §4.5` non-negotiable §2.13; platform-base-grown per `_root/04 §4.6`; early-adopter per `_root/04 §4.7`) + `§2.4.7` (URN secondary integration per the `[IF secondary driver = user_rate_normalization]` sub-block in §2.4.2) | Format B canonical. The IUR-variant close per `_root/04 §4.5` is non-negotiable for every IUR primary brief per `_root/04 §2.13`. |
> | `at_book_tier_shift` | `_root/05 §2.5.2` | `§2.5.6` (platform-base-grown per `_root/04 §4.6` as a separate follow-on paragraph after the pricing table when `new_tier_base > current_platform_mrr`; OMITTED when `new_tier_base < current_platform_mrr` per the kii special case in §2.5.6; no billing-basis footnote per `_root/04 §4.9`; early-adopter per `_root/04 §4.7`; default close per `_root/04 §4.5` unless secondary = IUR) + `§2.5.7` (no templated secondary integration in v6.2; per-account narrative pattern per the kii exemplar precedent — flag if a templated combination ever appears) | Format B canonical. The `_root/04 §4.6` sentence is a separate follow-on paragraph for Format B (and CEO Letter); Format A inlines via the §2.5.4 placeholder per CL-013 resolution. Format B does NOT inline §4.6 into the §2.5.2 block; the §4.6 sentence appears after the pricing table as a standalone paragraph. |
> | `multi_org_retirement` | `_root/05 §2.6.2` + (when `secondary_drivers` includes `included_user_reduction`) `_root/05 §2.6.6` IUR-secondary context paragraphs + `_root/05 §4` weaving matrix row for `multi_org_retirement \| included_user_reduction` | `§2.6.7` (URN secondary integration via per-account narrative per the kii / da exemplar pattern — no templated sub-block) | Format B canonical. **CL-016 (operator-stamped 2026-05-22)**: when `secondary_drivers` includes `included_user_reduction` (6 v6.2 accounts), the drafter ALSO integrates the included-base move alongside the multi-org rate retirement, per the templated coverage directed by `_root/05 §2.6.6` and `§4`. When `secondary_drivers` includes `user_rate_normalization` (2 v6.2 accounts), the drafter integrates the URN move per per-account narrative (no templated sub-block — see §2.6.7). The current state of `_root/05`'s templated IUR-secondary sub-block coverage is reported in the conformance block. |
> | `annual_discount_retirement` | `_root/05 §2.7.2` | `§2.7.6` (platform-base-grown per `_root/04 §4.6`; no billing-basis footnote per `_root/04 §4.9`; default close per `_root/04 §4.5` unless secondary = IUR; early-adopter per `_root/04 §4.7`; annual-cohort timing per `_root/02 §5` — brief substance unchanged, timing routes off renewal calendar) + `§2.7.7` (no secondary combinations in v6.2 deduped tally) | Format B canonical. Annual overlay (`_root/02 §5`) applies on timing only; routing per `_root/06 §4.3`. The §2.7.2 block contains the word "transition" in the permitted administrative context per `_root/04 §3` row exception. |
> | `special_arrangement` | `_root/05 §2.8.2` | `§2.8.6` (operator note removed before send; platform-base-grown per `_root/04 §4.6`; early-adopter per `_root/04 §4.7`; high-delta lede rule per `_root/04 §4.4` when `delta_pct > 30%` — common for SA; default close per `_root/04 §4.5`; no billing-basis footnote per `_root/04 §4.9`) + `§2.8.7` (no secondary combinations in v6.2) | Format B canonical. **Operator note from `_root/05 §2.8.6`** (internal-only; removed before send): for SA accounts with `delta_pct > 30%`, confirm account history with Finance before outreach; the CEO must be prepared to answer "what was the arrangement and why is it changing?" Cite as drafter note pointing to `_root/05 §2.8` definition. |
> | `module_compression` | NOT carried in Format B | n/a | Decrease-side; routes to Good News per `_root/06 §3` row 1. If routing produces this driver in Format B, escalate per `_root/CONTRACTS.md §2`. |
> | `user_count_variance` | NOT carried in Format B | n/a | Decrease-side; Good News only per `_root/05 §3.2`. If routing produces this driver in Format B, escalate per `_root/CONTRACTS.md §2`. |
> | `rate_architecture` | NOT carried in Format B | n/a | Decrease-side; Good News only per `_root/05 §3.3`. If routing produces this driver in Format B, escalate per `_root/CONTRACTS.md §2`. |
> | `already_migrated` | n/a | n/a | Status-marker leak per `_root/05 §1.4`; loader filters per `_root/07 §3`. No brief drafted. |

**Driver: [DRIVER]**

[INSERT_DRIVER_BLOCK — paste the verbatim block from the `_root/05 §N.2` named in the dispatch table above; substitute every bracketed token from v6.2 + Postgres per `_root/07 §2` + `§4`. The block carries its own pricing-table row template per `_root/05 §N.5` — paste that too, immediately after the driver prose. For `multi_org_retirement` with `included_user_reduction` secondary, additionally apply the `_root/05 §2.6.6` IUR-secondary integration per CL-016. For all drivers, apply the conditional context paragraphs named in the dispatch row above (each is a pointer to `_root/04 §N.M`; the drafter fetches the verbatim sentence and substitutes tokens from v6.2 + Postgres).]

---

> **Section 3h — Secondary-driver weaving (conditional).**
>
> [IF v6.2 `secondary_drivers` is non-empty: consult `_root/05 §4` (secondary-driver weaving matrix) and apply the named integration pattern within the driver block above — never as a separate section per `_root/05 §1.3`. If no entry in `_root/05 §4` covers the combination, escalate per `_root/CONTRACTS.md §2`.]
>
> The 7 v6.2-actually-exhibited combinations are enumerated in `_root/05 §4`. The Format-B-relevant rows: URN + IUR (7 accounts), MOR + IUR (6 accounts — CL-016 templated sub-block), MOR + URN (2 accounts — per-account narrative per §2.6.7).

---

> **Section 3i — Pricing-table row template (per driver).**
>
> The pricing table immediately follows the driver prose. The row template is owned by the driver's `_root/05 §N.5` block (URN: `§2.1.5`; PDC: `§2.2.5`; TBI: `§2.3.5`; IUR: `§2.4.5`; ABTS: `§2.5.5`; MOR: `§2.6.5`; ADR: `§2.7.5`; SA: `§2.8.5`). Drafter pastes the row template from the matching `_root/05 §N.5`; the templates render as fenced code blocks in `_root/05` (the driver-prose blockquotes contain markdown special chars).
>
> **Billing-basis footnote** — required for URN per `_root/04 §4.9` (referenced from `_root/05 §2.1.6`) AND for IUR per `_root/04 §4.9` (referenced from `_root/05 §2.4.6`). Drafter pastes the `_root/04 §4.9` verbatim italicized sentence immediately after the URN or IUR pricing table, before the next `---` separator. Per `_root/04 §4.9`, the footnote does NOT apply to TBI, PDC, ABTS, MOR, ADR, or SA blocks.
>
> **Platform-base-grown follow-on paragraph (`_root/04 §4.6`)** — Format B applies §4.6 as a separate follow-on paragraph AFTER the pricing table, whenever `new_tier_base > current_platform_mrr`. Format B does NOT inline §4.6 into the driver block (that is Format A's pattern via the §2.5.4 placeholder per CL-013). Drafter pastes the `_root/04 §4.6` verbatim sentence with `[YEAR]` substituted from `cohort_year`.

---

## What You're Getting at $[NEW_MRR]/Month

> **Section 3j — Tier verbatim block.**
>
> Drafter pastes the verbatim "What You're Getting at $X" block for the account's `assigned_tier` from `_root/03 Section 1` (T1 / T2 / T3). Substitute `[NEW_INCLUDED]` from v6.2 `included_users` (T1 default 10, T2 default 15; T3's block hard-codes "Up to 40 users" per `_root/03 §1` T3 drafter note — no substitution).
>
> [INSERT `_root/03 Section 1` — [T1 — Catalog Essentials | T2 — Commerce Professional | T3 — Commerce Enterprise] verbatim block — verbatim, with `[NEW_INCLUDED]` substituted from v6.2 `included_users` per `_root/07 §2` for T1 and T2; T3's block carries hard-coded "Up to 40 users" per `_root/03 §1` drafter note.]

---

## What This Works Out To

> **Section 3k — "What This Works Out To" value-anchor section (conditional).**
>
> [IF derived metric `cost_per_order < $200` per `_root/04 §4.8` (operator-stamped 2026-05-22 — **CL-002 cleanup applied; NOT the archived $35 threshold**): include the value-anchor section using `_root/04 §4.8` structure. Otherwise: omit the entire `## What This Works Out To` heading.]
>
> **Drafter computes** `cost_per_order` and `delta_per_order` per `_root/07 §4.4` formulas using `new_total_mrr` from v6.2 and `ltm_orders` from Postgres §4.3. **Inclusion gates per `_root/04 §4.8`**: `ltm_orders > 0` AND `cost_per_order < $200`. Append the second sentence (delta-per-order reframe) iff `delta_per_order < $50`; otherwise omit the second sentence (the figure would work against the message). If `ltm_orders = 0` OR `cost_per_order ≥ $200`, omit the entire section. Operator-judgment borderline cases: log the inclusion decision in the routing block.
>
> The §4.8 verbatim sentence structure is NOT inlined here per the strict-placeholder precedent; drafter follows §4.8 exactly.
>
> [INSERT — section structure per `_root/04 §4.8` if the inclusion gates fire; otherwise omit the entire `## What This Works Out To` heading. Drafter substitutes `[ltm_orders]`, `[COST_PER_ORDER]`, `[DELTA_PER_ORDER]` from `_root/07 §4.4` derivations.]

---

## What's Coming in 2026

> **Section 3l — Roadmap verbatim block (CL-005 — ADDED to Format B per operator decision 2026-05-22).**
>
> Drafter pastes the verbatim "What's Coming in 2026" block from `_root/03 Section 3`. **This is the most additive change in the Format B rebuild**: the archived Format B template OMITS this section entirely; per operator decision Q4 2026-05-22 (CL-005), every Stage 3 brief template — including Format B — carries the block via a Section 3 pointer. The trailing `*[Operator note — remove before sending: …]*` line inside the §3 block is removed before send per `_root/04 §2.14` (operator-note removal as non-negotiable) and QB-046 in `_root/08`.
>
> [INSERT `_root/03 Section 3` verbatim block — verbatim, no substitution; remove the trailing operator-note line before send.]

---

> **Section 3m — "How This Compares" section (conditional; drafter judgment whether to include).**
>
> [IF the drafter judges that a peer-positioning sentence adds clarity for this account AND `_root/04 §4.11` indicates the section is appropriate: include the section using the `_root/04 §4.11` structure. Otherwise: omit the entire `## How This Compares` heading.]
>
> **If included, the section follows `_root/04 §4.11` exactly:**
> - **No peer dollar ranges anywhere in client copy** — CL-003 + operator stamp 2026-05-22 universal. Peer dollar values (the T1 / T2 / T3 floor / midpoint / ceiling table in `_root/03 §5`) stay INTERNAL-ONLY; they appear in the operator's prep sheet, not in this brief. The archived Format B template already strips these correctly via its `[GUIDANCE]` block; the new template preserves the strip via `_root/04 §4.11` reference.
> - **No "equivalent platforms" / unnamed-competitor pricing sentence** — CL-004 + operator stamp 2026-05-22 universal. The archived Format B template's `[GUIDANCE]` block forbids comparative language; the new template references `_root/04 §3` row on competitor-pricing prohibition (broadened to named OR unnamed per the operator stamp).
> - **No "no account-specific adjustments" sentence** — CL-001 + `_root/04 §3` row. The archived Format B template already omits this (only CEO Letter and `da` exemplar carried it); absence preserved.
> - **Use the plain-English position vocabulary** from `_root/04 §4.11`: "at the base rate" / "below the midpoint" / "near the midpoint" / "above the midpoint". Compute the position against the tier midpoint using the INTERNAL-ONLY peer-range table in `_root/03 §5` (drafter check only, never quoted to the customer).
> - **Apply `_root/04 §4.3`** when the computed position is "above the midpoint": the mandatory user-count clause naming team size explicitly while confirming the platform base is at the tier standard.
> - **Apply `_root/04 §4.11` canonical client-facing form** — one position sentence + one structural-fairness sentence ("This is the same structure going to every account we work with"). The structural-fairness sentence echoes `_root/04 §2.7` non-negotiable.

## How This Compares

[INSERT — section structure per `_root/04 §4.11` if drafter judgment supports inclusion; otherwise omit the entire `## How This Compares` heading. Position vocabulary per `_root/04 §4.11`; user-count clause per `_root/04 §4.3` when "above the midpoint" applies; structural-fairness sentence per `_root/04 §2.7` / §4.11.]

---

## Your Pricing at a Glance

> **Section 3n — Pricing-at-a-glance summary table (every Format B brief).**
>
> A short summary table that recaps the dollar change, the tier label, and the included-users move. The table's column / row layout is template scaffolding (drafter-facing structure), not rule prose. Every value the drafter substitutes is sourced from v6.2 + the driver block above per `_root/07 §2`, or from `_root/03 §2 Block A` for the graduated-rate ladder summary string.
>
> This section appears in BOTH Format A and Format B (matches Stage 3.1's Format A `_brief-template.md` Section 3l-continued structure for cross-format consistency; the initial Stage 3.2 prompt draft incorrectly claimed it was unique to Format B and the delta-pass corrected this). Match Stage 3.1's form exactly; Format-B-specific data variation comes from the row values themselves (Format B handles 8 drivers vs Format A's 6 carriers, so some Format B `LEGACY_RATE` strings may differ in structure).
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

> **Section 3o — Operations-unchanged paragraph + IUR fork.**
>
> Drafter pastes one sentence per `_root/04 §4.5`:
> - DEFAULT variant — unless v6.2 `migration_driver = included_user_reduction` OR `secondary_drivers` includes `included_user_reduction`.
> - IUR-FORK variant — when IUR is primary or secondary (per `_root/04 §4.5` IUR fork condition; `_root/04 §2.13` non-negotiable). For Format B, the IUR fork fires on IUR primary (11 accounts), URN + IUR secondary (7 accounts), MOR + IUR secondary (6 accounts), and any future IUR-secondary combination v6.2 introduces.
>
> [INSERT `_root/04 §4.5` sentence — DEFAULT variant unless v6.2 `migration_driver = included_user_reduction` OR `secondary_drivers` includes `included_user_reduction`; in that case, INSERT `_root/04 §4.5` IUR-fork variant. Verbatim — copy character-for-character.]

---

## Let's Talk

> **Section 3p — Close paragraph (Format B active meeting offer).**
>
> Drafter pastes the verbatim Format B close from `_root/04 §4.12` — the active meeting offer that distinguishes Format B from Format A's passive offer and from the CEO Letter's specific-date call commitment.
>
> [INSERT `_root/04 §4.12` Format B close — verbatim, meeting-offer variant.]
>
> **CEO Pre-Call → Format B variant adjustment**: when `comm_action = "CEO Pre-Call → Format B"`, the close may be adjusted per-account to acknowledge the CEO conversation that preceded (per the archived Format B delivery email's operator note + `_root/04 §4.12` register). The adjustment is per-account narrative — the §4.12 verbatim close is still the canonical close text; the drafter may add or substitute one sentence acknowledging the CEO call. The structural rule (Format B uses §4.12's meeting-offer register, not the CEO Letter's specific-date call commitment) is unchanged.

> **Formal-notice line (immediately after the close, per `_root/04 §4.12`).**
>
> Required for Format B per `_root/04 §4.12`'s "immediately after each close, except Good News" instruction. Drafter pastes the verbatim italicized formal-notice line from `_root/04 §4.12`; substitute `[EFFECTIVE_DATE]`.
>
> [INSERT `_root/04 §4.12` formal-notice line — verbatim italicized form. Substitute `[EFFECTIVE_DATE]`.]

---

*[CSM NAME] | Customer Success | SuperCat*
*[DATE]*

---

> **Section 4 — Pre-send drafter checklist.**
>
> The complete pre-send checklist is the 126-check `_root/08` Quality Bar; the drafter runs every QB-NNN whose `Applies to:` field covers Format B or "all formats" before posting the conformance block. The checks below are the Format-B-specific blockers most often surfaced during drafting — they are convenience pointers only; consulting `_root/08` directly is canonical.
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
> - **QB-019** — entity-children do NOT receive a standalone Format B brief.
> - **QB-024** — brief written to `format-b-notices/`.
> - **QB-025** — CEO Pre-Call → Format B brief carries `CEO awareness required before send: YES` in the routing block.
>
> Data-pipeline:
> - **QB-028** — canonical loader from `_root/07 §3`.
> - **QB-030** — three Postgres queries verbatim from `_root/07 §4`.
> - **QB-031** — derived metrics computed per `_root/07 §4.4`.
> - **QB-032** + **QB-110** — user-billing reconciliation per `_root/07 §4.5`; ⚠️ flag if threshold tripped.
> - **QB-036** + **QB-037** — routing block complete per `_root/07 §7` Format B matrix (including the conditional CEO-awareness handling for the CEO Pre-Call variant).
>
> Voice / content (the highest-density section in `_root/08`):
> - **QB-040** / **QB-062** — lede leads with dollar + date, not percentage.
> - **QB-043** / **QB-068** / **QB-069** — no health bands or dimension scores in client copy.
> - **QB-045** / **QB-072** — universality claim uses "every account we work with" without hedge.
> - **QB-046** — "What's Coming in 2026" present verbatim from `_root/03 §3`; operator-note line stripped. **(Particularly important for Format B: the archived template OMITS this section; the new template ADDS it via the CL-005 cleanup.)**
> - **QB-047** — internal routing-note blockquote removed from delivered version.
> - **QB-054** — no competitor-pricing reference (named OR unnamed).
> - **QB-059** — no "no account-specific adjustments" sentence.
> - **QB-071** — no peer-range dollar values anywhere in client copy.
> - **QB-077** — "above the midpoint" carries the `_root/04 §4.3` user-count clause when applicable.
> - **QB-078** — high-delta annual-dollar sentence in lede when `delta_pct > 30%` (common in Format B).
> - **QB-079** — `_root/04 §4.5` operations-unchanged sentence verbatim; correct variant for the IUR-primary / IUR-secondary state.
> - **QB-080** — `_root/04 §4.6` platform-base-grown sentence verbatim with correct cohort year (when applicable — applied as a follow-on paragraph after the pricing table for Format B per Section 3i).
> - **QB-082** — value-anchor inclusion / exclusion respects the `_root/04 §4.8` $200 threshold (CL-002; **NOT the archived $35**).
> - **QB-083** — billing-basis footnote verbatim after URN or IUR pricing table per `_root/04 §4.9`.
> - **QB-084** — URN platform-base conditional sentence (Format B form) when Before platform base ≠ After platform base per `_root/04 §4.10`.
> - **QB-085** — "How This Compares" position vocabulary only; no peer-range dollars.
> - **QB-086** — Format B close verbatim per `_root/04 §4.12`; formal-notice line present.
> - **QB-087** — Watch / At Risk / Critical / VD<40 lede override applied if triggered (rare for Format B; most route to Strategic).
> - **QB-088** — `_root/04 §4.14` discount-correction substitution applied at Section 3e when `migration_driver = platform_discount_correction`.
>
> Driver content:
> - **QB-089** — driver block verbatim from `_root/05 §N.2` for Format B.
> - **QB-090** — every bracketed placeholder substituted from v6.2 / Postgres.
> - **QB-091** — conditional sub-blocks (`[IF ...]`) rendered iff condition holds.
> - **QB-092** — secondary-driver weaving integrated within the primary block, not separately.
> - **QB-093** — MOR + IUR integration applied per `_root/05 §2.6.6` + `§4` weaving matrix per CL-016 (operator-stamped 2026-05-22).
> - **QB-094** — MOR + URN per-account narrative integration applied per `_root/05 §2.6.7` + `§4` matrix.
>
> Product / pricing language:
> - **QB-099** — tier block verbatim from `_root/03 §1`.
> - **QB-100** — user-rate ladder uses the 1–10 / 11–25 / 26–50 / 51+ bands (`_root/03 §2 Block A`).
> - **QB-101** + **QB-102** — no unpublished SKU names, no INTERNAL peer / competitive tables in client copy.
>
> Math reconciliation:
> - **QB-104** — pricing-table Before total = `current_mrr`; After total = `new_total_mrr` exactly.
> - **QB-105** — stated Δ MRR = `new_total_mrr − current_mrr` within ±$1.
> - **QB-106** — when `delta_pct > 30%`, annual figure = `delta_mrr × 12` within ±$1.
> - **QB-107** — `tier_base` and `included_users` match the assigned tier in `_root/03 §1`.
> - **QB-108** — boundary cases reconcile with `_root/06 §3` precedence.
> - **QB-110** — user-billing reconciliation per `_root/07 §4.5`.
> - **QB-111** — `support_fire = TRUE` ⚠️ flag handled correctly.
>
> The above is convenience indexing. The full `_root/08` checklist (drift-control §3, routing §4, data-pipeline §5, voice / content §6, math §7, audit-only §8, cross-doc §9) is the canonical pre-send gate. Drafter pastes Format-B-applicable QB-NNN results into the conformance block per `_root/00_manifest.md §5`.

---

*Cross-references: `_root/00_manifest.md` (required-reading map); `_root/CONTRACTS.md §5` (path-reference contract — this template carries pointers only, not rule prose); `_root/01 §1` (relationship-before-price principle); `_root/02 §1` (segment definitions Format B draws from: Narrative primary, Core boundary cases, Pre-Engagement Δ ≥ $600); `_root/02 §3` / `§4` / `§5` (overlay rules that gate Format B); `_root/03 §1` (tier verbatim blocks); `_root/03 §2 Block A` (user-rate ladder); `_root/03 §3` ("What's Coming in 2026" — added to Format B via CL-005); `_root/04 §2` (14 non-negotiables); `_root/04 §3` (27-row forbidden-phrase table); `_root/04 §4.1` (relationship-before-price lede + tenure variants); `_root/04 §4.2` (lede stat guardrail); `_root/04 §4.3` (above-the-midpoint user-count clause); `_root/04 §4.4` (high-delta annual-dollar sentence); `_root/04 §4.5` (operations-unchanged sentence + IUR fork); `_root/04 §4.6` (platform-base-grown sentence — Format B applies as follow-on paragraph); `_root/04 §4.7` (early-adopter tenure paragraph); `_root/04 §4.8` (value anchor `cost_per_order < $200` — CL-002); `_root/04 §4.9` (billing-basis footnote — URN + IUR); `_root/04 §4.10` (platform-base conditional inside URN); `_root/04 §4.11` ("How This Compares" structure — CL-003 + CL-004); `_root/04 §4.12` (Format B close + formal-notice line); `_root/04 §4.13` (health-band lede override + standalone effective-date sentence); `_root/04 §4.14` (discount-correction lede substitution); `_root/05 §2.1.2` / `§2.2.2` / `§2.3.2` / `§2.4.2` / `§2.5.2` / `§2.6.2` / `§2.7.2` / `§2.8.2` (Format B driver blocks); `_root/05 §2.6.6` (MOR conditional context paragraphs — CL-016 IUR-secondary); `_root/05 §4` (secondary-driver weaving matrix); `_root/06 §1` (Format B definition + CEO Pre-Call → Format B routing pattern); `_root/06 §2` (routing-decision flow); `_root/06 §3` (delta-tier dispatch + precedence); `_root/06 §4` (overrides); `_root/06 §5` (`comm_action` vocabulary); `_root/07 §2` (v6.2 field guide); `_root/07 §4` (Postgres queries + derived metrics); `_root/07 §5` (fallback rules); `_root/07 §6` (file naming); `_root/07 §7` (routing-block matrix — canonical Format B row); `_root/08` (Quality Bar — 126 QB-NNN checks); `_meta/stage3_cleanup.md` (CL-001 / CL-002 / CL-003 / CL-004 / CL-005 / CL-012 / CL-016 history).*
