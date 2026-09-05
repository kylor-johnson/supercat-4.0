# CEO Letter + Call Commitment — Brief Template
*CEO-authored | $400 ≤ Δ ≤ $599 (Executive segment per `_root/02 §1`) | "I'll Call You" close with specific date per `_root/04 §4.12`*

---

> **Operator notes — drafter-facing scaffolding; remove this entire blockquote before sending.**
>
> **When to use this template.** CEO Letter + Call Commitment is the CEO-authored format for accounts whose Δ MRR satisfies `$400 ≤ Δ ≤ $599`. The mechanical scope, the routing-decision flow, the higher-touch-wins precedence rule, and the $400 ownership boundary that triggers CEO authorship are all defined in `_root/06 §1` (CEO Letter description), `_root/06 §2` (6-step routing-decision flow), `_root/06 §3` (delta-tier dispatch row 4), and `_root/02 §2` (ownership boundary). Do not restate them here; consult `_root/06` + `_root/02` when in doubt.
>
> **Who sends.** CEO authors / signs / personalizes the lede + close per `_root/06 §1` + `_root/02 §2`; CS team (Kylor) prepares the draft and executes delivery once the CEO has reviewed and approved. The delivery email goes from the CEO's own email address (see `ceo-letter-notices/_delivery-email-template.md`). CEO awareness is `YES (always)` per `_root/07 §7` CEO Letter row — non-negotiable; never sent without CEO sign-off.
>
> **What this template is NOT for.**
> - Δ ≤ $399 (Format A — 60-Day Notice or Format B — Notice + Meeting Offer): out of scope per `_root/06 §3` dispatch table.
> - Δ ≥ $600 (CEO Pre-Call → Format B): out of scope per `_root/06 §3` row 5 + `_root/06 §1` — CEO calls FIRST, then CS sends a Format B notice; the brief is Format B's, not this one. Stage 3.2 territory.
> - Entity-children (`parent_entity` non-empty AND `parent_entity ≠ company`): fold into the entity packet per `_root/02 §3` and `_root/06 §4.1` — do NOT draft a standalone CEO Letter for an entity-child. The CEO-Led Entity Pre-Engagement → Coordinated Notices pattern in `_root/06 §1` is a separate routing pattern that uses entity packets, NOT this template; the parent conversation is CEO-led but the per-child notices route to their own format folders.
> - `Δ < $0` (decrease-side): out of scope per `_root/06 §3` row 1 — routes to Good News.
> - Boundary cases ($595 / 30%; $605 / 8%): the higher-touch format wins per the `_root/06 §3` precedence rule — a $605 account routes to CEO Pre-Call → Format B (not CEO Letter); a $595 / 30%+ delta still routes to CEO Letter per row 4. If the routing produces a counterintuitive CEO Letter assignment, escalate per `_root/CONTRACTS.md §2`.
> - Watch / At Risk / Critical (`health_band ∈ {Watch, At Risk, Critical}` OR `value_delivery_score < 40`): the health override fires per `_root/02 §4` + `_root/06 §4.2`; most health-flagged accounts route to Strategic and the brief is deferred until CEO-led stabilization. Critical-band routing is per-account per `post_hold_action` — consult the routing CSV directly per `_root/06 §4.2`. The CEO-Letter-specific §4.13 lede override (Section 3c below — call commitment moves to the second sentence) applies on the rare CEO-Letter-eligible health-flagged brief that survives stabilization.
> - `migration_driver ∈ {module_compression, user_count_variance, rate_architecture}` (decrease-side): out of scope per `_root/05 §3` — routes to Good News per `_root/06 §3` row 1. CEO Letter's mechanical scope (`$400 ≤ Δ ≤ $599`) does not produce decrease drivers. If the routing produces a CEO Letter assignment with one of those primary drivers, the routing is suspect — escalate per `_root/CONTRACTS.md §2`.
>
> **Cleanup-tracker history embedded in this template.** Items applied as of authoring date: CL-001 (no "no account-specific adjustments" sentence anywhere — the archived CEO Letter template at `_archive/.../ceo-letter-notices/_brief-template.md` line 232 carried this forbidden sentence; the new template removes it entirely via `_root/04 §4.11` structure reference; this is the single most consequential cleanup for CEO Letter); CL-003 (no peer dollar ranges in client copy — universal per operator stamp 2026-05-22; archived CEO Letter template already strips, preserved); CL-004 (no "equivalent platforms" / unnamed-competitor pricing sentence anywhere — `_root/04 §3` row on competitor-pricing prohibition); CL-005 (mandatory "What's Coming in 2026" block via `_root/03 §3` pointer — ADDED to CEO Letter; the archived CEO Letter template OMITS this section entirely; this is the second most additive change in the CEO Letter rebuild); CL-012 (RESOLVED 2026-05-26 at source — the `tier_base_increase` dispatch row references `_root/05 §2.3.3` and pastes the §2.3.3 block verbatim; the secondary-driver marker now reads `[IF secondary driver = included_user_reduction]` per the operator stamp 2026-05-26 — no per-template marker carve-out needed); CL-016 (RESOLVED 2026-05-26 at source — the `multi_org_retirement` dispatch row references `_root/05 §2.6.3` which now carries the `[IF secondary driver = included_user_reduction]` templated sub-block directly; the 6 v6.2 multi_org + IUR-secondary accounts get templated coverage automatically when drafters paste §2.6.3 as-written; the 2 multi_org + URN-secondary accounts continue with per-account narrative integration per `_root/05 §2.6.7`); CL-022 (the delivery email's routing-block field subset is inferred per Stage 3.1 + Stage 3.2 precedent — see `ceo-letter-notices/_delivery-email-template.md` Section 2 note; rule-layer extension to `_root/07 §7` is scheduled for the Wave 6 batch after all 4 Stage 3 templates land). See `_meta/stage3_cleanup.md` for full item history.
>
> **Drafter's responsibility.** Every `_root/XX §N.M` reference in this template is to a canonical rule doc. At draft time, the drafter (a) opens the referenced section, (b) copies the named verbatim content character-for-character, (c) substitutes any `[BRACKETED_TOKEN]` placeholders from v6.2 + Postgres data per `_root/07 §2` + `§4`. The template carries pointers; it does not carry rule prose. CEO reviews the draft and personalizes the lede + close + sign-off before delivery — that personalization is the only client-facing prose authored at draft time; everything else is fetched verbatim from `_root/`. Pre-send: run the `_root/08` Quality Bar against the completed draft (the QB-NNN list under "Section 4 — Pre-send drafter checklist" below names the CEO-Letter-specific blockers; the full 126-check checklist lives in `_root/08`).
>
> **Conformance block.** The drafter ends the session with the canonical conformance block defined in `_root/00_manifest.md §5`.

---

> **Section 2 — Internal routing note** (drafter-facing; remove before sending — matches the canonical field list per `_root/07 §7` for CEO Letter; field names and order match `_root/07 §7` exactly):
>
> Brief type: `CEO Letter + Call Commitment` | $400 ≤ Δ ≤ $599 (Executive segment)
> Account: [ACCOUNT_NAME] | Tier: [T1/T2/T3] | Wave: [WAVE]
> Migration driver: [DRIVER] | Health: [HEALTH_SCORE] — [HEALTH_BAND] | Risk label: [RISK_LABEL]
> Engagement: [E] | Adoption: [A] | Value Delivery: [VD] | Ops Health: [OH]
> Support fire: [YES/NO] | Behavioral floor applied: [YES/NO]
> Delta: [DELTA_PCT] (+$[DELTA_MRR]/month)
> Cohort: [COHORT_YEAR]
> Contract: [MONTHLY/ANNUAL] | Renewal date: [DATE or UNKNOWN]
> Earliest enforceable effective date: [EFFECTIVE_DATE]
> Comm_action: [CEO Letter + Call Commitment | CEO Letter + Call Commitment (+$XXX) per `post_hold_action` variant] (from routing CSV per `_root/06 §5` + `§5.5`)
> Postgres live data ([YYYY-MM-DD]): active_org_users=[N] | logged_in_90d=[N] | total_logins_90d=[N] | ltm_orders=[N] | ltm_gmv=$[N] | ltm_customers_served=[N]
> **CEO awareness required before send: YES — CEO must review and personalize before this goes out** (per `_root/07 §7` CEO Letter row — always, non-negotiable)
> CEO call commitment date: [DATE — specific calendar date within 5 business days of send per `_root/04 §4.12`; NEVER "soon" or "in the coming days"]
> CEO name for sign-off: [CEO FIRST + LAST NAME]
>
> Conditional rows — include only when the condition holds, per `_root/07 §7` conditional-fields table:
> - `> **⚠️ SUPPORT FIRE: [N] days open. Production-ready. Operator decides send timing.**` — insert immediately after `Support fire:` row when `support_fire = TRUE`. Per `_root/07 §5` `support_fire = TRUE` handling: draft the brief in full; nothing about the support issue appears in client copy; CEO decides send timing.
> - `> ⚠️ CEO PRE-CALL REQUIRED — arrangement was negotiated by [NAME]. Do not send at CSM level before CEO confirms.` — when `migration_driver = special_arrangement` AND `angies_notes` / `discount_drivers` reference a named executive as originator. For CEO Letter this typically reinforces the existing CEO-awareness requirement; the CEO is already sign-off-required, but the SA arrangement may need additional CEO preparation per `_root/05 §2.8.6` operator note (Finance check before outreach; CEO prepared to answer "what was the arrangement and why is it changing?").
> - `> ⚠️ USER BILLING RECONCILIATION NEEDED — billed amount implies [M] excess users ($Y/month) but stated trailing average implies [N] excess users ($X/month). Confirm before sending.` — when `_root/07 §4.5` discrepancy threshold tripped.
> - `> Billing entity: [NAME] — notice routes to billing contact` — when `billing_entity` is non-blank AND ≠ `company`.
> - `> Tenure acknowledgment required: YES — [YEARS] years (cohort [COHORT_YEAR])` — when `cohort_year ≤ 2016` (early adopter). For CEO Letter, the §4.7 CEO Letter variant in the lede integrates this acknowledgment first-person; see Section 3b + Section 3e below.
>
> Routing-block edits: if Postgres data was unavailable for any sub-field, render the fallback per `_root/07 §5` (e.g. `Postgres live data: UNAVAILABLE — fell back to composite_narrative` for §4.1 failure; `ltm_orders = 0 — value anchor omitted` for §4.3 empty). Do not delete the line — render the prescribed fallback per the §5 table.
>
> Note: CEO Letter's routing block does NOT carry `Expansion eligible` (that field is Format A only per `_root/07 §7` matrix) and does NOT carry the Format B CEO Pre-Call variant `Comm_action = "CEO Pre-Call → Format B"` value (that routes to `format-b-notices/` per `_root/07 §6` — CEO Letter is bounded above at $599 per `_root/06 §3`).

---

# [ACCOUNT_NAME]: Your Pricing Is Changing

*Prepared for [ACCOUNT_NAME] | [DATE]*

---

> **Section 3b — Lede paragraph (CEO Letter integrated structure — Thriving / Healthy accounts).**
>
> The CEO writes a 3–4 sentence peer-to-peer lede that opens by acknowledging the relationship or the significance of the news, lands the dollar change in dollars (not percentage), and commits to the specific-date call in the same paragraph. This is the ONE section of the brief where the prose is drafter-generated rather than pasted from a `_root/` block — the CEO personalizes the lede before delivery; CS prepares a draft using the structure below. The CEO Letter lede is more elaborate than Format A's or Format B's because the CEO is writing peer-to-peer to a buyer the company has had a multi-year relationship with, and the call commitment is structurally integral rather than tacked-on.
>
> **Apply at every CEO Letter lede (Thriving / Healthy):**
> - Per `_root/04 §4.1`: lead with the relationship (tenure + at least one account-specific stat) before delivering the number. Tenure-band variants live in §4.1; the CEO Letter integrates the relationship signal into a first-person peer-to-peer paragraph rather than the Format A/B sentence-one tenure pattern. For 3+ year tenure, sentence one names the relationship before any reference to pricing; for 10+ year tenure, the weight of the history leads.
> - Per `_root/04 §4.2`: use unambiguous platform metrics (tenure, active users, session volume, surfaces in use). Order counts are supporting evidence only; when used, scope explicitly to "orders submitted through SuperCat" or "eCat orders" — never the account's total order volume. No provisioned-vs.-active ratio. No per-order subscription cost in the lede.
> - Per `_root/04 §4.4` (CEO Letter variant): when `delta_pct > 30%`, the lede MUST name the annual dollar impact BETWEEN the monthly delta sentence and the call-commitment sentence. The §4.4 CEO Letter verbatim sentence — "That's $[DELTA × 12]/year — a real budget line, and you deserve a straight explanation of exactly what changed and why." — is fetched from `_root/04 §4.4` per the strict-placeholder precedent (operator-stamped 2026-05-26, Stage 3.1 review pass — `_root/09_changelog.md`). The CEO Letter form is distinct from Format B's "($[DELTA × 12]/year)" parenthetical-in-same-sentence form per `_root/04 §4.4`.
> - Per `_root/04 §4.7` (CEO Letter variant): when `cohort_year ≤ 2015`, the CEO Letter integrates the early-adopter tenure paragraph into the lede (first-person, peer-to-peer, ending with the call commitment). The CEO Letter §4.7 variant is longer and first-person, distinct from the Format B variant. Drafter may integrate into the lede paragraph directly OR render as a standalone Section 3e paragraph per CEO judgment.
> - Per `_root/04 §4.12` (CEO Letter close — "I'll Call You"): the call commitment is a specific calendar date within 5 business days of send. The §4.12 close text lives at Section 3n; the lede's call commitment may be a one-sentence forward-reference ("I'll call you personally by [SPECIFIC DATE] to walk through this directly.") OR the full §4.7 paragraph's closing sentence when §4.7 fires. NEVER "soon" or "in the coming days" — the §4.12 anti-pattern is explicitly named.
> - Per `_root/04 §4.14`: when `migration_driver = platform_discount_correction`, the lede framing block's "rate at signing" sentence is replaced by the §4.14 verbatim substitution. The §4.14 substitution is uniform across Format A / Format B / CEO Letter per §4.14.
> - Per `_root/01 §1` relationship-before-price principle: the lede's organizing principle. CEO is writing peer-to-peer to a multi-year relationship; the lede integrates this more explicitly than Format A/B.
>
> **Skip the relationship-stats lede entirely if `health_band ∈ {Watch, At Risk, Critical}` OR `value_delivery_score < 40`.** The §4.13 health-band override suppresses the relationship-stats lede AND, for CEO Letter specifically, moves the call commitment to the SECOND sentence (per the `_root/04 §4.13` CEO Letter sub-paragraph). See Section 3c below for the override structure. Most health-flagged accounts route to Strategic per `_root/02 §4` + `_root/06 §4.2`; the lede-suppression rule is preserved here for the rare CEO-Letter-eligible edge case where the override does not fully reroute.
>
> **Postgres data sourcing for lede stats** (per `_root/07 §4`):
> - `total_logins_90d` from `_root/07 §4.2`.
> - `active_org_users` and `logged_in_90d` from `_root/07 §4.2` — load into the routing block; per `_root/04 §4.2`, never expressed as a provisioned-vs.-active ratio in client copy.
> - `ltm_orders` and `ltm_customers_served` from `_root/07 §4.3` — when surfaced, framed as "eCat orders" per `_root/07 §4.3` rendering constraint.
> - Tenure: `cohort_year` from v6.2.
> - "Surfaces in use": derived from drafter judgment + v6.2 `current_stack` + Postgres activity.
> - Fallback when Postgres unavailable: `composite_narrative` from v6.2 per `_root/07 §5`; note the fallback in the routing block.
>
> **[LEDE_PARAGRAPH — 3–4 sentences; CEO first-person peer-to-peer; relationship signal first, dollar / date second, (if delta_pct > 30%) `_root/04 §4.4` CEO Letter annual sentence verbatim between monthly delta and call commitment, then call-commitment sentence (full §4.12 close text lives at Section 3n; the lede references the same specific date). Follows `_root/04 §4.1` + `§4.2` + (if delta_pct > 30%) `§4.4` + (if cohort_year ≤ 2015) `§4.7` CEO Letter variant + `§4.12` + (if migration_driver = platform_discount_correction) `§4.14`. The CEO personalizes the exact wording before delivery; CS prepares a draft. For Watch / At Risk / Critical / VD<40: skip this paragraph entirely; the brief opens with Section 3c below per `_root/04 §4.13` CEO Letter sub-paragraph.]**

---

> **Section 3c — Watch / At-Risk / Critical lede override (CEO-Letter-specific call-commitment-moves-to-sentence-two pattern).**
>
> [IF `health_band ∈ {Watch, At Risk, Critical}` OR `value_delivery_score < 40`: insert the CEO Letter variant of the `_root/04 §4.13` health-band lede override. The CEO Letter sub-paragraph differs from Format A/B's standalone-sentence form — the call commitment moves to the SECOND sentence (no transition through activity stats), and the §4.13 CEO Letter sub-paragraph carries the verbatim form. The structure: sentence one is the standalone dollar-change sentence; sentence two is the call commitment.]
>
> [IF `health_band ∈ {Thriving, Healthy}` AND `value_delivery_score ≥ 40`: omit this section entirely; the lede in Section 3b above stands.]
>
> Per the strict-placeholder precedent operator-stamped 2026-05-26 (Stage 3.1 review pass — `_root/09_changelog.md`): the §4.13 CEO Letter sub-paragraph is fetched from `_root/04 §4.13` verbatim, never inlined here, even though it carries only a handful of bracketed tokens. The CEO Letter health-band lede override is distinct from Format A/B's standalone-sentence form; drafter selects the CEO Letter variant per §4.13.
>
> Note per `_root/02 §4` + `_root/06 §4.2`: a Watch / At-Risk / Critical CEO Letter is rare because the Strategic override typically routes the account away from CEO Letter entirely. The lede-suppression rule is preserved here for the rare edge case where CEO Letter still applies (e.g. the override resolves and the post-stabilization Δ-tier places the account back in CEO Letter's $400–$599 scope).
>
> [INSERT `_root/04 §4.13` CEO Letter sub-paragraph — verbatim, with `[EFFECTIVE_DATE]`, `[CURRENT_MRR]`, `[NEW_MRR]`, `[DELTA]`, `[SPECIFIC DATE]` substituted from v6.2 per `_root/07 §2` + the CEO call commitment date logged in the Section 2 routing block above.]

---

> **Section 3d — Consolidated 2026 framing sentence.**
>
> Per `_root/04 §3` row on the consolidated 2026 sentence: replace the legacy "SuperCat is standardizing its pricing..." phrasing with the operator-stamped iteration. Drafter pastes the sentence verbatim from `_root/04 §3` (the table row's "Replacement" column carries the canonical text). Uniform across Format A / Format B / CEO Letter.
>
> [INSERT `_root/04 §3` consolidated 2026 sentence — verbatim, no substitution.]

---

> **Section 3e — Tenure-aware variant sentence (with PDC substitution and early-adopter integration).**
>
> One short sentence after the consolidated 2026 sentence that names the account's signing-year context. Per `_root/04 §4.1` tenure-band variants:
> - `cohort_year ≤ 2015` (10+ year tenure): the §4.7 CEO Letter variant typically already covers this in the lede paragraph (Section 3b) as a first-person, peer-to-peer integrated paragraph that ends with the call commitment. If §4.7 was integrated into Section 3b's lede, omit a separate §4.1 sentence here (the §4.7 paragraph subsumes it). If §4.7 was rendered as a standalone Section 3e paragraph (see below), still omit a separate §4.1 sentence here; the §4.7 paragraph carries the year-naming framing.
> - `2016 ≤ cohort_year` (≤ 9 year tenure): use the §4.1 standard variant — "Your rate was set in [YEAR] — this is the first time we've updated it." (verbatim per §4.1).
> - `migration_driver = platform_discount_correction`: REPLACE this sentence entirely with the `_root/04 §4.14` discount-correction substitution — "Your rate reflects a discount applied at signing that's being retired as part of this change." (verbatim per §4.14). The tenure-aware variant is NOT used when §4.14 fires (per `_root/04 §4.14` posture rule). Uniform across Format A / Format B / CEO Letter per §4.14.
>
> **Early-adopter tenure paragraph (CEO Letter variant) — conditional standalone rendering.**
>
> [IF `cohort_year ≤ 2015` AND the CEO opted not to integrate §4.7 into the Section 3b lede: insert the early-adopter tenure paragraph from `_root/04 §4.7` CEO Letter variant as a standalone Section 3e paragraph here. The CEO Letter §4.7 variant is longer, first-person, and ends with the call commitment per `_root/04 §4.7` — distinct from Format B's shorter structural form. The archived CEO Letter template inlined this at lines 35–36; the new template references §4.7 instead per the path-reference contract.]
>
> [IF `cohort_year ≤ 2015` AND §4.7 was already integrated into the Section 3b lede: omit the standalone paragraph here; the lede carries it.]
>
> [IF `cohort_year > 2015`: omit the early-adopter paragraph entirely.]
>
> [INSERT one of: (a) `_root/04 §4.1` tenure-aware variant for 2016+ cohorts, OR (b) the `_root/04 §4.14` discount-correction substitution when `migration_driver = platform_discount_correction`, OR (c) `_root/04 §4.7` CEO Letter standalone early-adopter paragraph when `cohort_year ≤ 2015` AND CEO opted for standalone rendering. Verbatim; substitute `[YEAR]`, `[N]` (years), `[SPECIFIC DATE]` from `cohort_year` + the CEO call commitment date logged in Section 2.]

---

Below is exactly why your number is changing and what you're getting at the new price.

---

## Why the Number Is Changing

> **Section 3f — Driver dispatch.**
>
> The drafter selects ONE block based on the account's v6.2 `migration_driver` value and pastes the named `_root/05 §N.M` block verbatim into the `[INSERT_DRIVER_BLOCK]` placeholder below. The block prose is owned by `_root/05`; the template carries the dispatch table only. CEO Letter carries all 8 increase-side drivers; decrease-side drivers route to Good News per `_root/06 §3` and are flagged below for escalation if they ever appear on a CEO Letter routing.
>
> | v6.2 `migration_driver` | Insert `_root/05` block verbatim from | Conditional sub-blocks + secondary handling | Notes |
> |---|---|---|---|
> | `user_rate_normalization` | `_root/05 §2.1.3` | `§2.1.6` (conditional context paragraphs — billing-basis footnote per `_root/04 §4.9`; platform-base-grown per `_root/04 §4.6`; platform-base conditional per `_root/04 §4.10` CEO Letter variant; early-adopter per `_root/04 §4.7` CEO Letter variant; IUR-variant close per `_root/04 §4.5` when secondary = IUR) + `§2.1.7` (URN + IUR secondary integration via the §2.1.3 `[IF excess users remain AND secondary driver = included_user_reduction]` sub-block) | CEO Letter canonical block. Most common driver (37 v6.2 accounts overall; the 8-account Executive segment skews heavily toward URN primary per `_root/05 §5` correlation table). Note: the §2.1.3 CEO Letter URN block uses the explicit `[IF excess users remain AND secondary driver = included_user_reduction]` marker (distinct from Format B's `[IF excess users remain after new included base]` marker per §2.1.7 documentation). |
> | `platform_discount_correction` | `_root/05 §2.2.3` | `§2.2.6` (platform-base-grown per `_root/04 §4.6`; lede substitution already applied at Section 3e per `_root/04 §4.14`; no billing-basis footnote per `_root/04 §4.9`; early-adopter per `_root/04 §4.7` CEO Letter variant) + `§2.2.7` (no secondary combinations in v6.2) | CEO Letter canonical. Note: §2.2.3 CEO Letter PDC block uses "as part of this **refresh**" (vs Format B's "as part of this **change**") per the §2.2.3 doc-level note. The Section 3e PDC substitution carries the discount-correction lede framing; do not re-state in the driver block. |
> | `tier_base_increase` | `_root/05 §2.3.3` | `§2.3.6` (platform-base-grown per `_root/04 §4.6`; no billing-basis footnote unless IUR involved per `_root/04 §4.9`; IUR-variant close per `_root/04 §4.5` when secondary = IUR; early-adopter per `_root/04 §4.7` CEO Letter variant) + `§2.3.7` (secondary combinations — marker now reads `[IF secondary driver = included_user_reduction]` post-CL-012 source fix; see notes column) | CEO Letter canonical. **CL-012 RESOLVED 2026-05-26 at source** per operator stamp — the §2.3.3 secondary-driver marker was amended from `[IF secondary driver = user_rate_normalization AND included base expands]` to `[IF secondary driver = included_user_reduction]`; the Format B and CEO Letter TBI blocks are identical character-for-character per the §2.3 doc-level note. Drafter pastes §2.3.3 verbatim — no per-template marker carve-out needed; the marker is now correct. CL-023 was filed in lockstep for v6.2 re-evaluation of TBI primary rows historically coded with URN secondary; that's a v6.2 maintenance question, not a CEO Letter template concern. |
> | `included_user_reduction` | `_root/05 §2.4.3` | `§2.4.6` (billing-basis footnote required per `_root/04 §4.9`; IUR-variant close required per `_root/04 §4.5` non-negotiable §2.13; platform-base-grown per `_root/04 §4.6`; early-adopter per `_root/04 §4.7` CEO Letter variant) + `§2.4.7` (URN secondary integration per the `[IF secondary driver = user_rate_normalization]` sub-block in §2.4.3) | CEO Letter canonical. Note: §2.4.3 CEO Letter IUR block uses "as part of this **refresh**" per the §2.4.3 doc-level note. The IUR-variant close per `_root/04 §4.5` is non-negotiable for every IUR primary brief per `_root/04 §2.13`. |
> | `at_book_tier_shift` | `_root/05 §2.5.3` | `§2.5.6` (platform-base-grown per `_root/04 §4.6` as a separate follow-on paragraph after the pricing table when `new_tier_base > current_platform_mrr`; OMITTED when `new_tier_base < current_platform_mrr` per the kii special case in §2.5.6; no billing-basis footnote per `_root/04 §4.9`; early-adopter per `_root/04 §4.7` CEO Letter variant; default close per `_root/04 §4.5` unless secondary = IUR) + `§2.5.7` (no templated secondary integration in v6.2; per-account narrative pattern per the kii exemplar precedent — flag if a templated combination ever appears) | CEO Letter canonical. The `_root/04 §4.6` sentence is a separate follow-on paragraph for CEO Letter (and Format B); CEO Letter does NOT inline §4.6 into the §2.5.3 block. The CL-013 cleanup applied 2026-05-26 at `_root/05 §2.5.4` source preserved this CEO Letter pattern (the CEO Letter ABTS block already referenced §4.6 by pointer; the source fix brought Format A into alignment); `_root/05 §2.5.6` now documents that all three formats reference `_root/04 §4.6` by pointer. |
> | `multi_org_retirement` | `_root/05 §2.6.3` (now carries the `[IF secondary driver = included_user_reduction]` templated sub-block at source per CL-016 fix 2026-05-26) | `§2.6.6` (conditional context paragraphs — billing-basis footnote NOT required for MOR-primary standalone or MOR + URN-secondary; REQUIRED for MOR + IUR-secondary when the IUR-secondary sub-block's included-base move produces excess users per `_root/04 §4.9`; platform-base-grown per `_root/04 §4.6`; early-adopter per `_root/04 §4.7` CEO Letter variant; IUR-variant close per `_root/04 §4.5` when secondary = IUR) + `§2.6.7` (per-secondary-driver guidance — IUR-secondary points to templated sub-block; URN-secondary continues per-account narrative per operator stamp's IUR-only scope) + `§4` (weaving matrix for MOR + URN-secondary narrative integration via kii / da exemplar pattern) | CEO Letter canonical. Note: §2.6.3 CEO Letter MOR block uses "as part of this **refresh**" per the §2.6.3 doc-level note. **CL-016 RESOLVED 2026-05-26 at source** per operator stamp — drafter pastes §2.6.3 verbatim; the `[IF secondary driver = included_user_reduction]` templated sub-block fires automatically for the 6 v6.2 multi_org + IUR-secondary accounts. The 2 v6.2 multi_org + URN-secondary accounts: the sub-block does NOT fire; drafter integrates per-account narrative per the kii / da exemplar patterns documented in §4. |
> | `annual_discount_retirement` | `_root/05 §2.7.3` | `§2.7.6` (platform-base-grown per `_root/04 §4.6`; no billing-basis footnote per `_root/04 §4.9`; default close per `_root/04 §4.5` unless secondary = IUR; early-adopter per `_root/04 §4.7` CEO Letter variant; annual-cohort timing per `_root/02 §5` — brief substance unchanged, timing routes off renewal calendar) + `§2.7.7` (no secondary combinations in v6.2 deduped tally) | CEO Letter canonical. Note: §2.7.3 CEO Letter ADR block uses "as part of this **refresh**" per the §2.7.3 doc-level note. Annual overlay (`_root/02 §5`) applies on timing only; routing per `_root/06 §4.3`. The §2.7.3 block contains the word "transition" in the permitted administrative context per `_root/04 §3` row exception. |
> | `special_arrangement` | `_root/05 §2.8.3` | `§2.8.6` (operator note removed before send — for SA accounts with `delta_pct > 30%`, confirm account history with Finance before outreach; CEO must be prepared to answer "what was the arrangement and why is it changing?"; platform-base-grown per `_root/04 §4.6`; early-adopter per `_root/04 §4.7` CEO Letter variant; high-delta lede rule per `_root/04 §4.4` CEO Letter variant when `delta_pct > 30%`; default close per `_root/04 §4.5`; no billing-basis footnote per `_root/04 §4.9`) + `§2.8.7` (no secondary combinations in v6.2) | CEO Letter canonical. **Per §2.8.3 doc-level note**: the CEO Letter SA block is materially longer and more direct than Format B's — it adds the explicit "this is not a judgment about your account" reframe and the "one rate card, applied consistently" closing line. The divergence is intentional: SA in CEO Letter context is a peer-to-peer conversation about a custom arrangement, and the longer framing earns the move. Operator note from `_root/05 §2.8.6` (internal-only; removed before send): SA accounts with `delta_pct > 30%` require Finance confirmation before outreach + CEO preparation for "what was the arrangement and why is it changing?" — CEO Letter is the format most likely to surface this question given the peer-to-peer register. |
> | `module_compression` | NOT carried in CEO Letter | n/a | Decrease-side; routes to Good News per `_root/06 §3` row 1. If routing produces this driver in CEO Letter, escalate per `_root/CONTRACTS.md §2`. |
> | `user_count_variance` | NOT carried in CEO Letter | n/a | Decrease-side; Good News only per `_root/05 §3.2`. If routing produces this driver in CEO Letter, escalate per `_root/CONTRACTS.md §2`. |
> | `rate_architecture` | NOT carried in CEO Letter | n/a | Decrease-side; Good News only per `_root/05 §3.3`. If routing produces this driver in CEO Letter, escalate per `_root/CONTRACTS.md §2`. |
> | `already_migrated` | n/a | n/a | Status-marker leak per `_root/05 §1.4`; loader filters per `_root/07 §3`. No brief drafted. |

**Driver: [DRIVER]**

[INSERT_DRIVER_BLOCK — paste the verbatim block from the `_root/05 §N.3` named in the dispatch table above; substitute every bracketed token from v6.2 + Postgres per `_root/07 §2` + `§4`. The block carries its own pricing-table row template per `_root/05 §N.5` — paste that too, immediately after the driver prose. For `multi_org_retirement` with `included_user_reduction` secondary, the `[IF secondary driver = included_user_reduction]` sub-block inside §2.6.3 fires automatically when drafters paste the block verbatim (CL-016 source fix). For `tier_base_increase` with `included_user_reduction` secondary, the `[IF secondary driver = included_user_reduction]` sub-block inside §2.3.3 fires automatically when drafters paste the block verbatim (CL-012 source fix). For all drivers, apply the conditional context paragraphs named in the dispatch row above (each is a pointer to `_root/04 §N.M`; the drafter fetches the verbatim sentence and substitutes tokens from v6.2 + Postgres).]

---

> **Section 3g — Secondary-driver weaving (conditional).**
>
> [IF v6.2 `secondary_drivers` is non-empty: consult `_root/05 §4` (secondary-driver weaving matrix) and apply the named integration pattern within the driver block above — never as a separate section per `_root/05 §1.3`. If no entry in `_root/05 §4` covers the combination, escalate per `_root/CONTRACTS.md §2`.]
>
> The 7 v6.2-actually-exhibited combinations are enumerated in `_root/05 §4`. The CEO-Letter-relevant rows (per `_root/05 §5` correlation table — Executive segment skews toward URN primary + IUR secondary): URN + IUR (7 accounts overall — the §2.1.3 sub-block fires automatically), MOR + IUR (6 accounts overall — the §2.6.3 templated sub-block fires automatically per CL-016 source fix), MOR + URN (2 accounts overall — per-account narrative per §2.6.7), IUR + URN (per the §2.4.3 sub-block).

---

> **Section 3h — Pricing-table row template (per driver).**
>
> The pricing table immediately follows the driver prose. The row template is owned by the driver's `_root/05 §N.5` block (URN: `§2.1.5`; PDC: `§2.2.5`; TBI: `§2.3.5`; IUR: `§2.4.5`; ABTS: `§2.5.5`; MOR: `§2.6.5`; ADR: `§2.7.5`; SA: `§2.8.5`). Drafter pastes the row template from the matching `_root/05 §N.5`; the templates render as fenced code blocks in `_root/05` (the driver-prose blockquotes contain markdown special chars).
>
> **Billing-basis footnote** — required for URN per `_root/04 §4.9` (referenced from `_root/05 §2.1.6`) AND for IUR per `_root/04 §4.9` (referenced from `_root/05 §2.4.6`) AND for MOR + IUR-secondary per `_root/05 §2.6.6` (updated 2026-05-26 in the CL-016 source fix). Drafter pastes the `_root/04 §4.9` verbatim italicized sentence immediately after the URN, IUR, or MOR-with-IUR-secondary pricing table, before the next `---` separator. Per `_root/04 §4.9`, the footnote does NOT apply to TBI, PDC, ABTS, ADR, SA, or MOR-primary standalone / MOR + URN-secondary blocks.
>
> **Platform-base-grown follow-on paragraph (`_root/04 §4.6`)** — CEO Letter applies §4.6 as a separate follow-on paragraph AFTER the pricing table, whenever `new_tier_base > current_platform_mrr`. CEO Letter does NOT inline §4.6 into the driver block. Drafter pastes the `_root/04 §4.6` verbatim sentence with `[YEAR]` substituted from `cohort_year`. This is CEO Letter's existing pattern, preserved by the CL-013 source fix at `_root/05 §2.5.4` per `_root/05 §2.5.6` documentation that "all three formats reference `_root/04 §4.6` by pointer."

---

## What You're Getting at $[NEW_MRR]/Month

> **Section 3i — Tier verbatim block.**
>
> Drafter pastes the verbatim "What You're Getting at $X" block for the account's `assigned_tier` from `_root/03 Section 1` (T1 / T2 / T3). Substitute `[NEW_INCLUDED]` from v6.2 `included_users` (T1 default 10, T2 default 15; T3's block hard-codes "Up to 40 users" per `_root/03 §1` T3 drafter note — no substitution).
>
> CEO Letter accounts in v6.2 trend toward T3 given the $400+ delta scope (per `_root/05 §5` correlation table — Executive segment), but T1 and T2 CEO Letters also exist; drafter selects by `assigned_tier`.
>
> [INSERT `_root/03 Section 1` — [T1 — Catalog Essentials | T2 — Commerce Professional | T3 — Commerce Enterprise] verbatim block — verbatim, with `[NEW_INCLUDED]` substituted from v6.2 `included_users` per `_root/07 §2` for T1 and T2; T3's block carries hard-coded "Up to 40 users" per `_root/03 §1` drafter note.]

---

## What This Works Out To

> **Section 3j — "What This Works Out To" value-anchor section (conditional).**
>
> [IF derived metric `cost_per_order < $200` per `_root/04 §4.8` (operator-stamped 2026-05-22): include the value-anchor section using `_root/04 §4.8` structure. Otherwise: omit the entire `## What This Works Out To` heading.]
>
> **Drafter computes** `cost_per_order` and `delta_per_order` per `_root/07 §4.4` formulas using `new_total_mrr` from v6.2 and `ltm_orders` from Postgres §4.3. **Inclusion gates per `_root/04 §4.8`**: `ltm_orders > 0` AND `cost_per_order < $200`. Append the second sentence (delta-per-order reframe) iff `delta_per_order < $50`; otherwise omit the second sentence (the figure would work against the message). If `ltm_orders = 0` OR `cost_per_order ≥ $200`, omit the entire section. Operator-judgment borderline cases: log the inclusion decision in the routing block.
>
> The §4.8 verbatim sentence structure is NOT inlined here per the strict-placeholder precedent; drafter follows §4.8 exactly.
>
> Note: the archived CEO Letter template already uses the $200 threshold per line 226 — CEO Letter does NOT need the CL-002 cleanup that applies to Format B (which had a stale $35 threshold). Verify when reading §4.8 that the threshold is $200; if you find $35, STOP — the rule layer was not updated and the cleanup cannot proceed.
>
> [INSERT — section structure per `_root/04 §4.8` if the inclusion gates fire; otherwise omit the entire `## What This Works Out To` heading. Drafter substitutes `[ltm_orders]`, `[COST_PER_ORDER]`, `[DELTA_PER_ORDER]` from `_root/07 §4.4` derivations.]

---

## What's Coming in 2026

> **Section 3k — Roadmap verbatim block (CL-005 — ADDED to CEO Letter per operator decision 2026-05-22).**
>
> Drafter pastes the verbatim "What's Coming in 2026" block from `_root/03 Section 3`. **This is the second most additive change in the CEO Letter rebuild** (after CL-001's "no account-specific adjustments" sentence removal): the archived CEO Letter template OMITS this section entirely; per operator decision Q4 2026-05-22 (CL-005), every Stage 3 brief template — including CEO Letter — carries the block via a Section 3 pointer. The trailing `*[Operator note — remove before sending: …]*` line inside the §3 block is removed before send per `_root/04 §2.14` (operator-note removal as non-negotiable) and QB-046 in `_root/08`.
>
> [INSERT `_root/03 Section 3` verbatim block — verbatim, no substitution; remove the trailing operator-note line before send.]

---

> **Section 3l — "How This Compares" section (conditional; drafter judgment whether to include) — CL-001 CRITICAL.**
>
> [IF the drafter judges that a peer-positioning sentence adds clarity for this account AND `_root/04 §4.11` indicates the section is appropriate: include the section using the `_root/04 §4.11` structure. Otherwise: omit the entire `## How This Compares` heading.]
>
> **If included, the section follows `_root/04 §4.11` exactly:**
> - **No "no account-specific adjustments" sentence** — CL-001 + `_root/04 §3` row + `_root/04 §4.11`. **This is the CL-001 CEO Letter cleanup — the archived CEO Letter template at `_archive/.../ceo-letter-notices/_brief-template.md` line 232 carries this forbidden sentence ("The same pricing structure is going to every account we work with — there are no account-specific adjustments in how your number was calculated."); the new template MUST NOT carry it in any form.** The same sentence also appears in the archived exemplars (`da` line 72; `shl` line 80; `hfg` line 71) — those exemplars need regeneration when Stage 4 production drafting begins; the new template prevents recurrence by referencing `_root/04 §4.11`'s structure instead of inlining the legacy sentence.
> - **No peer dollar ranges anywhere in client copy** — CL-003 + operator stamp 2026-05-22 universal. Peer dollar values (the T1 / T2 / T3 floor / midpoint / ceiling table in `_root/03 §5`) stay INTERNAL-ONLY; they appear in the operator's prep sheet, not in this brief. The archived CEO Letter template already strips these correctly per CL-003 + Wave 1 operator stamp; the new template preserves the absence via `_root/04 §4.11` reference.
> - **No "equivalent platforms" / unnamed-competitor pricing sentence** — CL-004 + operator stamp 2026-05-22 universal. The archived CEO Letter template does not carry this sentence; the new template MUST NOT introduce it. The §3 row on competitor-pricing prohibition is broadened to named OR unnamed per the operator stamp.
> - **Use the plain-English position vocabulary** from `_root/04 §4.11`: "at the base rate" / "below the midpoint" / "near the midpoint" / "above the midpoint". Compute the position against the tier midpoint using the INTERNAL-ONLY peer-range table in `_root/03 §5` (drafter check only, never quoted to the customer).
> - **Apply `_root/04 §4.3`** when the computed position is "above the midpoint": the mandatory user-count clause naming team size explicitly while confirming the platform base is at the tier standard. Without the clause, "above the midpoint" reads as a premium or arbitrary upcharge — the clause is what makes the position math-readable per `_root/04 §4.3`.
> - **Apply `_root/04 §4.11` canonical client-facing form** — one position sentence + one structural-fairness sentence ("This is the same structure going to every account we work with"). The structural-fairness sentence echoes `_root/04 §2.7` non-negotiable. The §4.11 structure handles the same intent as the forbidden CL-001 sentence without the defensive register.

## How This Compares

[INSERT — section structure per `_root/04 §4.11` if drafter judgment supports inclusion; otherwise omit the entire `## How This Compares` heading. Position vocabulary per `_root/04 §4.11`; user-count clause per `_root/04 §4.3` when "above the midpoint" applies; structural-fairness sentence per `_root/04 §2.7` / §4.11. NEVER include the CL-001 "no account-specific adjustments" sentence (deleted entirely per `_root/04 §3` row).]

---

## Your Pricing at a Glance

> **Section 3m — Pricing-at-a-glance summary table (every CEO Letter brief).**
>
> A short summary table that recaps the dollar change, the tier label, and the included-users move. The table's column / row layout is template scaffolding (drafter-facing structure), not rule prose. Every value the drafter substitutes is sourced from v6.2 + the driver block above per `_root/07 §2`, or from `_root/03 §2 Block A` for the graduated-rate ladder summary string.
>
> This section appears in Format A (Stage 3.1 `_brief-template.md` Section 3l-continued), Format B (Stage 3.2 `_brief-template.md` Section 3n), and CEO Letter (the archived CEO Letter template lines 238–253 carry it). Match the cross-format table structure exactly for consistency.
>
> The annual rows surface `current_mrr × 12` and `new_total_mrr × 12`. The "Additional user rate" row uses the legacy rate before; the after-column value is fetched from `_root/03 §2 Block A` per the strict-placeholder precedent operator-stamped 2026-05-26 (Stage 3.1 review pass) — the canonical ladder values live in §2 Block A alone, not inline here.

| | Before | After |
|---|---|---|
| **Monthly** | $[CURRENT_MRR] | **$[NEW_MRR]** |
| **Annual** | $[CURRENT_ARR] | **$[NEW_ARR]** |
| **Change** | — | +$[DELTA]/month ([DELTA_PCT]) |
| **Tier** | [LEGACY_TIER_LABEL] | [NEW_TIER_LABEL] |
| **Included users** | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| **Additional user rate** | [LEGACY_RATE_DESCRIPTION] | [INSERT `_root/03 §2 Block A` graduated-rate summary string verbatim — e.g. "Graduated ($25/$22/$20/$18)" per current §2 Block A canonical values] |

---

> **Section 3n — Operations-unchanged paragraph + IUR fork.**
>
> Drafter pastes one sentence per `_root/04 §4.5`:
> - DEFAULT variant — unless v6.2 `migration_driver = included_user_reduction` OR `secondary_drivers` includes `included_user_reduction`.
> - IUR-FORK variant — when IUR is primary or secondary (per `_root/04 §4.5` IUR fork condition; `_root/04 §2.13` non-negotiable). For CEO Letter, the IUR fork fires on IUR primary, URN + IUR secondary (the §2.1.3 sub-block), MOR + IUR secondary (the §2.6.3 templated sub-block per CL-016 source fix), TBI + IUR secondary (the §2.3.3 sub-block per CL-012 source fix), and any future IUR-secondary combination v6.2 introduces.
>
> [INSERT `_root/04 §4.5` sentence — DEFAULT variant unless v6.2 `migration_driver = included_user_reduction` OR `secondary_drivers` includes `included_user_reduction`; in that case, INSERT `_root/04 §4.5` IUR-fork variant. Verbatim — copy character-for-character.]

---

## I'll Call You

> **Section 3o — Close paragraph (CEO Letter "I'll Call You" — specific calendar date within 5 business days of send).**
>
> Drafter pastes the verbatim CEO Letter close from `_root/04 §4.12` — the "I'll Call You" variant with the specific calendar date that distinguishes CEO Letter from Format A's passive offer and Format B's active meeting offer. The call commitment is the structural feature of CEO Letter; it is a hard commitment, not a soft offer.
>
> **CEO-specific constraint per `_root/04 §4.12`**: the call-commitment date is a specific calendar date within 5 business days of send. **NEVER "soon" or "in the coming days"** — the §4.12 anti-pattern is explicitly named. The date appears in this close section AND is logged in the internal routing block per Section 2 above AND is logged in the delivery email's routing block — the three locations must carry the same specific calendar date.
>
> [INSERT `_root/04 §4.12` CEO Letter close — verbatim, "I'll Call You" variant with specific calendar date. Substitute `[SPECIFIC DATE]` from the CEO call commitment date logged in Section 2 routing block above.]

> **Formal-notice line (immediately after the close, per `_root/04 §4.12`).**
>
> Required for CEO Letter per `_root/04 §4.12`'s "immediately after each close, except Good News" instruction. Drafter pastes the verbatim italicized formal-notice line from `_root/04 §4.12`; substitute `[EFFECTIVE_DATE]`.
>
> [INSERT `_root/04 §4.12` formal-notice line — verbatim italicized form. Substitute `[EFFECTIVE_DATE]`.]

---

*[CEO FIRST NAME] [CEO LAST NAME] | CEO | SuperCat*
*[DATE]*

---

> **Section 4 — Pre-send drafter checklist.**
>
> The complete pre-send checklist is the 126-check `_root/08` Quality Bar; the drafter runs every QB-NNN whose `Applies to:` field covers CEO Letter or "all formats" before posting the conformance block. The checks below are the CEO-Letter-specific blockers most often surfaced during drafting — they are convenience pointers only; consulting `_root/08` directly is canonical.
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
> - **QB-018** — Δ_pct / Δ_mrr boundary handled per `_root/06 §3` precedence rule (CEO Letter is bounded above at $599; Δ ≥ $600 routes to CEO Pre-Call → Format B, not CEO Letter).
> - **QB-019** — entity-children do NOT receive a standalone CEO Letter brief; route to entity packet per `_root/02 §3`.
> - **QB-024** — brief written to `ceo-letter-notices/`.
>
> Data-pipeline:
> - **QB-028** — canonical loader from `_root/07 §3`.
> - **QB-030** — three Postgres queries verbatim from `_root/07 §4`.
> - **QB-031** — derived metrics computed per `_root/07 §4.4`.
> - **QB-032** + **QB-110** — user-billing reconciliation per `_root/07 §4.5`; ⚠️ flag if threshold tripped.
> - **QB-036** + **QB-037** — routing block complete per `_root/07 §7` CEO Letter matrix (including the CEO-Letter-required fields: `CEO awareness required before send: YES (always)`, `CEO call commitment date: required`, `CEO name for sign-off: required`).
>
> Voice / content (the highest-density section in `_root/08`):
> - **QB-040** / **QB-062** — lede leads with dollar + date, not percentage.
> - **QB-043** / **QB-068** / **QB-069** — no health bands or dimension scores in client copy.
> - **QB-045** / **QB-072** — universality claim uses "every account we work with" without hedge.
> - **QB-046** — "What's Coming in 2026" present verbatim from `_root/03 §3`; operator-note line stripped. **(Particularly important for CEO Letter: the archived template OMITS this section; the new template ADDS it via the CL-005 cleanup — second most additive change in the rebuild.)**
> - **QB-047** — internal routing-note blockquote removed from delivered version.
> - **QB-054** — no competitor-pricing reference (named OR unnamed).
> - **QB-059** — no "no account-specific adjustments" sentence. **(CRITICAL for CEO Letter: the archived template at line 232 carries this forbidden sentence; the new template MUST NOT carry it in any form. CL-001 cleanup.)**
> - **QB-071** — no peer-range dollar values anywhere in client copy.
> - **QB-077** — "above the midpoint" carries the `_root/04 §4.3` user-count clause when applicable.
> - **QB-078** — high-delta annual-dollar sentence in lede when `delta_pct > 30%` (CEO Letter variant per `_root/04 §4.4` — the §4.4 CEO Letter sentence lands BETWEEN the monthly delta and the call commitment in the lede paragraph; distinct from Format B's parenthetical-in-same-sentence form).
> - **QB-079** — `_root/04 §4.5` operations-unchanged sentence verbatim; correct variant for the IUR-primary / IUR-secondary state (including CL-016 templated MOR + IUR-secondary sub-block coverage and CL-012 templated TBI + IUR-secondary sub-block coverage).
> - **QB-080** — `_root/04 §4.6` platform-base-grown sentence verbatim with correct cohort year (when applicable — applied as a follow-on paragraph after the pricing table for CEO Letter per Section 3h).
> - **QB-081** — `_root/04 §4.7` early-adopter tenure paragraph (CEO Letter variant — first-person, peer-to-peer, ends with the call commitment) when `cohort_year ≤ 2015` (integrated into Section 3b lede OR rendered as Section 3e standalone per CEO judgment).
> - **QB-082** — value-anchor inclusion / exclusion respects the `_root/04 §4.8` $200 threshold (archived CEO Letter template already uses $200 — CL-002 does NOT apply to CEO Letter).
> - **QB-083** — billing-basis footnote verbatim after URN or IUR pricing table per `_root/04 §4.9`; also after MOR + IUR-secondary pricing table per `_root/05 §2.6.6` (updated 2026-05-26 in CL-016 source fix).
> - **QB-084** — URN platform-base conditional sentence (CEO Letter form) when Before platform base ≠ After platform base per `_root/04 §4.10`.
> - **QB-085** — "How This Compares" position vocabulary only; no peer-range dollars.
> - **QB-086** — CEO Letter close verbatim per `_root/04 §4.12` (specific calendar date within 5 business days of send; NEVER "soon" or "in the coming days"); formal-notice line present immediately after the close; the call-commitment date in the close section matches the date logged in the Section 2 routing block AND the date logged in the delivery email's routing block.
> - **QB-087** — Watch / At Risk / Critical / VD<40 lede override applied if triggered (CEO Letter variant per `_root/04 §4.13` CEO Letter sub-paragraph — call commitment moves to the SECOND sentence, distinct from Format A/B's standalone-sentence form).
> - **QB-088** — `_root/04 §4.14` discount-correction substitution applied at Section 3e when `migration_driver = platform_discount_correction`.
>
> Driver content:
> - **QB-089** — driver block verbatim from `_root/05 §N.3` for CEO Letter (note: CEO Letter uses §N.3, distinct from Format B's §N.2 and Format A's §N.4).
> - **QB-090** — every bracketed placeholder substituted from v6.2 / Postgres.
> - **QB-091** — conditional sub-blocks (`[IF ...]`) rendered iff condition holds.
> - **QB-092** — secondary-driver weaving integrated within the primary block, not separately.
> - **QB-093** — MOR + IUR integration via the templated sub-block at `_root/05 §2.6.3` (CL-016 RESOLVED 2026-05-26 at source) — drafter pastes §2.6.3 verbatim; the `[IF secondary driver = included_user_reduction]` sub-block fires automatically.
> - **QB-094** — MOR + URN per-account narrative integration applied per `_root/05 §2.6.7` + `§4` matrix (no templated sub-block per operator stamp's IUR-only scope).
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
> - **QB-114** (audit-only) — CEO call-commitment date on CEO calendar; call actually placed by that date per `_root/04 §4.12`.
>
> The above is convenience indexing. The full `_root/08` checklist (drift-control §3, routing §4, data-pipeline §5, voice / content §6, math §7, audit-only §8, cross-doc §9) is the canonical pre-send gate. Drafter pastes CEO-Letter-applicable QB-NNN results into the conformance block per `_root/00_manifest.md §5`.

---

*Cross-references: `_root/00_manifest.md` (required-reading map); `_root/CONTRACTS.md §5` (path-reference contract — this template carries pointers only, not rule prose); `_root/01 §1` (relationship-before-price principle — load-bearing for CEO Letter's peer-to-peer lede); `_root/02 §1` (Executive segment definition $401 ≤ Δ ≤ $600 healthy standalone — CEO Letter's primary home); `_root/02 §2` ($400 ownership boundary that triggers CEO authorship); `_root/02 §3` / `§4` / `§5` (overlay rules that gate CEO Letter); `_root/03 §1` (tier verbatim blocks); `_root/03 §2 Block A` (user-rate ladder); `_root/03 §3` ("What's Coming in 2026" — added to CEO Letter via CL-005); `_root/04 §2` (14 non-negotiables); `_root/04 §3` (27-row forbidden-phrase table — including CL-001 "no account-specific adjustments" row); `_root/04 §4.1` (relationship-before-price lede + tenure variants — CEO Letter integrates into peer-to-peer paragraph); `_root/04 §4.2` (lede stat guardrail); `_root/04 §4.3` (above-the-midpoint user-count clause); `_root/04 §4.4` (high-delta annual-dollar sentence — CEO Letter variant); `_root/04 §4.5` (operations-unchanged sentence + IUR fork); `_root/04 §4.6` (platform-base-grown sentence — CEO Letter applies as follow-on paragraph); `_root/04 §4.7` (early-adopter tenure paragraph — CEO Letter first-person variant ending with call commitment); `_root/04 §4.8` (value anchor `cost_per_order < $200` — CEO Letter archive already uses $200, no cleanup needed); `_root/04 §4.9` (billing-basis footnote — URN + IUR + MOR-with-IUR-secondary); `_root/04 §4.10` (platform-base conditional inside URN); `_root/04 §4.11` ("How This Compares" structure — CL-001 + CL-003 + CL-004); `_root/04 §4.12` (CEO Letter close "I'll Call You" + formal-notice line + specific-calendar-date constraint); `_root/04 §4.13` (health-band lede override + CEO Letter call-commitment-moves-to-sentence-two sub-paragraph); `_root/04 §4.14` (discount-correction lede substitution); `_root/05 §2.1.3` / `§2.2.3` / `§2.3.3` / `§2.4.3` / `§2.5.3` / `§2.6.3` / `§2.7.3` / `§2.8.3` (CEO Letter driver blocks); `_root/05 §2.3.3` (CL-012 RESOLVED 2026-05-26 at source — IUR-secondary marker amended); `_root/05 §2.6.3` (CL-016 RESOLVED 2026-05-26 at source — IUR-secondary templated sub-block added); `_root/05 §2.6.6` (MOR conditional context — billing-basis footnote conditionality updated 2026-05-26); `_root/05 §4` (secondary-driver weaving matrix); `_root/06 §1` (CEO Letter definition + $400 ownership boundary); `_root/06 §2` (routing-decision flow); `_root/06 §3` (delta-tier dispatch + precedence); `_root/06 §4` (overrides); `_root/06 §5` (`comm_action` vocabulary including CEO Letter variants); `_root/07 §2` (v6.2 field guide); `_root/07 §4` (Postgres queries + derived metrics); `_root/07 §5` (fallback rules); `_root/07 §6` (file naming — `ceo-letter-notices/[ord_id]__[company-slug]__brief.md`); `_root/07 §7` (routing-block matrix — canonical CEO Letter row including CEO awareness YES (always) + CEO call commitment date required + CEO name for sign-off required); `_root/08` (Quality Bar — 126 QB-NNN checks); `_meta/stage3_cleanup.md` (CL-001 / CL-003 / CL-004 / CL-005 / CL-012 / CL-016 / CL-022 history).*
