# Good News Notice — Brief Template
*CS-led | Δ MRR < $0 (decrease-side per `_root/06 §3` row 1) | Good News close per `_root/04 §4.12` (no formal-notice line)*

---

> **Operator notes — drafter-facing scaffolding; remove this entire blockquote before sending.**
>
> **When to use this template.** Good News Notice is the CS-led, warm low-touch decrease-side brief for accounts whose Δ MRR satisfies `Δ < $0` (any decrease) per `_root/06 §3` row 1. The mechanical scope, the 6-step routing-decision flow, and the Watch-band carve-out are all defined in `_root/06 §1` (Good News description), `_root/06 §2` (6-step routing-decision flow), `_root/06 §3` row 1 (decrease check), and `_root/06 §4.2` (Watch-band carve-out — Format-A-vs-Good-News interaction). Do not restate them here; consult `_root/06` when in doubt.
>
> **Who sends.** CS team — CSM signs per `_root/06 §1` + `_root/04 §4.12` Good News close register (operator-led, no ask). No CEO involvement, no CEO co-signature, no CEO awareness flag required (`CEO awareness required before send: NO (always)` per `_root/07 §7` Good-News row).
>
> **What this template is NOT for.**
> - `Δ ≥ $0` (any increase): out of scope per `_root/06 §3` — routes to Format A / Format B / CEO Letter / CEO Pre-Call → Format B per the standard delta-tier dispatch. Good News is decrease-side only.
> - Entity-children (`parent_entity` non-empty AND `parent_entity ≠ company`): fold into the entity packet per `_root/02 §3` and `_root/06 §4.1` — do NOT draft a standalone Good News for an entity-child even if Δ < $0. The entity packet covers the per-brand pricing detail.
> - Watch / At Risk / Critical (`health_band ∈ {Watch, At Risk, Critical}` OR `value_delivery_score < 40`): **DO NOT use this template** per `_root/06 §4.2` Format-A-vs-Good-News interaction. A Good-News-eligible account that is health-flagged routes through CSM for a health check-in BEFORE any pricing communication. Critical-band handling is per-account per `post_hold_action` per `_root/06 §4.2`; the operator decides per-account at routing-CSV maintenance time. Consult the routing CSV directly; escalate per `_root/CONTRACTS.md §2` if uncertain.
> - Increase-side `migration_driver` values (`user_rate_normalization`, `platform_discount_correction`, `tier_base_increase`, `included_user_reduction`, `at_book_tier_shift`, `multi_org_retirement`, `annual_discount_retirement`, `special_arrangement`): out of scope per `_root/05 §2` — those are the 8 increase-side drivers; Good News carries the 3 decrease-side drivers only per `_root/05 §3`. If the routing produces a Good News assignment with an increase-side driver, the routing is suspect — escalate per `_root/CONTRACTS.md §2`.
> - `already_migrated` status: filtered at the loader per `_root/07 §3`; no brief drafted per `_root/05 §1.4`.
>
> **Cleanup-tracker history embedded in this template.** Items applied as of authoring date: CL-001 (no "no account-specific adjustments" sentence anywhere — the archived Good News template did not carry the sentence; absence preserved via `_root/04 §3` row + the absence of a "How This Compares" section in Good News scope); CL-003 (no peer dollar ranges in client copy — universal per operator stamp 2026-05-22; archived Good News template already strips, absence preserved per `_root/04 §3` row); CL-004 (no "equivalent platforms" / unnamed-competitor pricing sentence anywhere — `_root/04 §3` row on competitor-pricing prohibition; archived Good News template already strips, absence preserved); CL-005 (mandatory "What's Coming in 2026" block via `_root/03 §3` pointer — ADDED to Good News per operator decision Q4 2026-05-22; the archived Good News template OMITS this section entirely, so this is an additive change; drafters trim other content to fit the 200–300-word length target per `_root/03 §3` coverage rule); CL-022 (the delivery email's routing-block field subset is inferred per Stage 3.1 + Stage 3.2 + Stage 3.3 precedent — see `good-news-notices/_delivery-email-template.md` Section 2 note; rule-layer extension to `_root/07 §7` is scheduled for the Wave 6 batch after all 4 Stage 3 templates land). Not Good-News-applicable (documented for completeness): CL-002 (value-anchor threshold — Good News does not carry a value-anchor section), CL-011 (`platform_discount_correction` rename — Good News does not carry PDC), CL-012 (TBI secondary marker — Good News does not carry TBI), CL-013 (Format A ABTS §4.6 inline cleanup — Good News does not carry ABTS), CL-014 (entity-packet template — separate Stage 3.5), CL-015 (Annual voice rules home — separate `_root/04 §4.15` filing), CL-016 (MOR templated IUR-secondary sub-block — Good News does not carry MOR), CL-017 (Critical-band per-account routing — Good News carve-out already documented at `_root/06 §4.2`), CL-018–CL-021 (Format A v2 exemplar regen items — Format A scope), CL-023 (v6.2 TBI+URN re-evaluation — Format B / CEO Letter scope). See `_meta/stage3_cleanup.md` for full item history.
>
> **Length target.** 200–300 words. This is an email-length brief, not a long-form notice. The archived Good News template established this scope (per the archived `_brief-template.md` line 18 — "200–300 words. This is an email-length notice, not a brief."); the new template preserves it. The 4-row "Your Pricing at a Glance" mini-summary table is a quick reference, not a full pricing breakdown — the driver block carries the per-driver pricing detail per `_root/05 §3.X.4` (table row templates).
>
> **Do not send if** (preserved from archived `_brief-template.md` lines 110–115; each item now points to a `_root/` rule):
> - Health band is Watch, At Risk, or Critical — route to CSM for health check-in first per `_root/06 §4.2`.
> - Account is Unscored — cannot assess risk per `_root/02 §4`; hold until health data is available; consult `post_hold_action` per `_root/06 §5.5`.
> - Account is part of an entity whose packet is not yet assembled per `_root/02 §3` + `_root/06 §4.1` — all sibling brands must receive notice in a coordinated batch via the entity packet; do not draft standalone Good News for an entity-child.
> - Annual contract with unknown renewal date — confirm renewal date and the ≥90-day notice window per `_root/02 §5` + `_root/06 §4.3` before sending.
>
> **After sending** (preserved from archived `_brief-template.md` lines 117–120, with "invoice" normalized to "pricing" per the 2026-05-26 operator-stamped subject-line normalization across all 4 formats — `_root/09_changelog.md` Stage 3.2 review pass entry):
> - Log send date in CRM; start the 60-day notice window clock per `_root/01 §3` operating principle 2 + `_root/06 §3`.
> - If account has an expansion_brief_type (t1_to_t2 or t2_to_t3): queue Format C for a separate conversation, after and only after a confirmed positive signal from this notice per `_root/04 §2.6`. Silence does not clear the gate.
> - If no response within 10 days, send a one-line follow-up: `"Just checking the above reached you — wanted to make sure the pricing change on [DATE] doesn't catch anyone off guard."` (Template scaffolding, operator-stamped 2026-05-26 for Stage 3.4 — NOT promoted to `_root/04`; same voice constraints as the original brief apply per `_root/04 §3` + `§4.12` Good News register.)
>
> **Drafter's responsibility.** Every `_root/XX §N.M` reference in this template is to a canonical rule doc. At draft time, the drafter (a) opens the referenced section, (b) copies the named verbatim content character-for-character, (c) substitutes any `[BRACKETED_TOKEN]` placeholders from v6.2 + Postgres data per `_root/07 §2` + `§4`. The template carries pointers; it does not carry rule prose. Pre-send: run the `_root/08` Quality Bar against the completed draft (the QB-NNN list under "Section 4 — Pre-send drafter checklist" below names the Good-News-specific blockers; the full 126-check checklist lives in `_root/08`).
>
> **Conformance block.** The drafter ends the session with the canonical conformance block defined in `_root/00_manifest.md §5`.

---

> **Section 2 — Internal routing note** (drafter-facing; remove before sending — matches the canonical field list per `_root/07 §7` for the Good-News row; field names and order match `_root/07 §7` exactly).
>
> Brief type: `good_news_notice` | Good News Notice (decrease)
> Account: [ACCOUNT_NAME] | Tier: [T1/T2/T3] | Wave: [WAVE]
> Migration driver: [DRIVER] | Health: [HEALTH_SCORE] — [HEALTH_BAND] | Risk label: [RISK_LABEL]
> Engagement: [E] | Adoption: [A] | Value Delivery: [VD] | Ops Health: [OH]
> Support fire: [YES/NO] | Behavioral floor applied: [YES/NO]
> Current MRR: $[CURRENT_MRR] | New MRR: $[NEW_MRR] | Delta: –$[DELTA]/month ([DELTA_PCT])
> Cohort: [COHORT_YEAR]
> Contract: [MONTHLY/ANNUAL] | Renewal date: [DATE or UNKNOWN]
> Earliest enforceable effective date: [EFFECTIVE_DATE]
> Comm_action: `Good-News Notice` (from routing CSV per `_root/06 §5`; or `Good-News Notice (after CSM touchpoint)` / `Good-News Notice (after renewal-date confirm)` per `post_hold_action` per `_root/06 §5.5`)
> **CEO awareness required before send: NO** (always — per `_root/07 §7` Good-News row)
> **Expansion eligible: [YES/NO]** — required per `_root/07 §7` Good-News row. If YES, queue Format C ONLY after a confirmed positive migration signal per `_root/04 §2.6`; never combined with this notice.
> **Watch health flag: [YES/NO]** — required per `_root/07 §7` Good-News row. **If YES: DO NOT use this template; escalate to CSM for health check-in first per `_root/06 §4.2`.** This is the Good-News-specific gate; the brief should not exist when the flag is YES.
>
> Conditional rows — include only when the condition holds, per `_root/07 §7` conditional-fields table:
> - `> **⚠️ SUPPORT FIRE: [N] days open. Production-ready. Operator decides send timing.**` — insert immediately after `Support fire:` row when `support_fire = TRUE`. Per `_root/07 §5` `support_fire = TRUE` handling: draft the brief in full; nothing about the support issue appears in client copy; operator decides send timing.
> - `> ⚠️ USER BILLING RECONCILIATION NEEDED — billed amount implies [M] excess users ($Y/month) but stated trailing average implies [N] excess users ($X/month). Confirm before sending.` — when `_root/07 §4.5` discrepancy threshold tripped. Relevant for `user_count_variance` and `rate_architecture` driver blocks where the table renders per-user math.
> - `> Billing entity: [NAME] — notice routes to billing contact` — when `billing_entity` is non-blank AND ≠ `company`.
> - `> Tenure acknowledgment required: YES — [YEARS] years (cohort [COHORT_YEAR])` — when `cohort_year ≤ 2016` (early adopter). Note: Good News does NOT carry the full `_root/04 §4.7` early-adopter tenure paragraph; the warm low-touch register per `_root/04 §4.12` Good News close keeps the brief short. The tenure flag in the routing block is informational; drafter may reference tenure lightly in the per-account context of the driver block but does not insert §4.7's verbatim paragraph.
>
> **Postgres live-data line OMITTED** per `_root/07 §7` footnote — Good-News briefs do not surface live operational metrics. The decrease is a structural mechanic; the lede leads with the dollar number, not platform-activity stats. (Cross-references `_root/06 §1` Good News description and `_root/04 §4.12` Good News close register — "math, not a favor.")
>
> Routing-block edits: if Postgres data was needed for a sub-computation (e.g. `user_count_variance` requires trailing-average user data — but per `_root/07 §4.2` the trailing average is sourced from v6.2 `trailing_avg_users`, not Postgres at draft time), use the v6.2 column. Live Postgres queries are not part of the Good-News pipeline per `_root/07 §7` footnote.

---

# [ACCOUNT_NAME]: Your Pricing Is Decreasing

*Effective [EFFECTIVE_DATE]*

---

> **Section 3b — Lede sentence (always present — drafter-generated).**
>
> Good News leads with the mechanical decrease fact in sentence one: dollar amount + effective date. No percentage in the lede per `_root/04 §2.1` (lead with dollars, not percentage) + `_root/04 §3` row on leading with a percentage. No relationship-stats lede (the brief is short; the warm-but-direct register per `_root/04 §4.12` Good News close handles the tone — the brief does not need a relationship preamble). No "thank you for being a customer" / "gift" / "reward" framing per `_root/04 §3` row on gift / reward / favor framing. This is drafter-generated prose — the lede sentence's exact wording is per-account, but the structural form below is canonical (matches the archived `_brief-template.md` line 38 pattern, preserved).
>
> Apply at every Good News lede:
> - Per `_root/04 §2.1`: lead with dollar amount and effective date; never lead with a percentage.
> - Per `_root/04 §3` row on minimizing language: do not say "modest," "small," "minor" — state the number plainly.
> - Per `_root/04 §3` row on apology for prior pricing: do NOT apologize for the prior invoice — the legacy structure produced the prior number; the new structure produces the new number.
> - Per `_root/04 §3` row on gift / reward / favor framing: state the mechanic; do NOT frame the decrease as a gift, reward, thank-you, or anything that implies a favor was conferred.
> - Per `_root/05 §3.1.5` / `§3.2.4` / `§3.3.4` voice posture notes: "math, not a favor." The decrease is the mechanic stated plainly.
>
> **Pattern (drafter-generated; archived `_brief-template.md` line 38 form preserved)**:
>
> `Your monthly pricing is decreasing from **$[CURRENT_MRR]** to **$[NEW_MRR]** — a reduction of **$[DELTA]/month** — effective **[EFFECTIVE_DATE]**.`
>
> [LEDE_SENTENCE — drafter-generated; one sentence; leads with dollar + date per the pattern above. Substitute `[CURRENT_MRR]`, `[NEW_MRR]`, `[DELTA]`, `[EFFECTIVE_DATE]` from v6.2 per `_root/07 §2`. No percentage in lede; no apology; no favor framing; no minimizing language.]

---

## Why the Number Is Changing

> **Section 3c — Driver dispatch (3 decrease-side drivers only).**
>
> The drafter selects ONE block based on the account's v6.2 `migration_driver` value and pastes the named `_root/05 §3.X.2` mechanic block verbatim into the `[INSERT_DRIVER_BLOCK]` placeholder below. The block prose is owned by `_root/05`; the template carries the dispatch table only. Good News carries the 3 decrease-side drivers per `_root/05 §3`; increase-side drivers are out of scope and flagged below for escalation if they ever appear on a Good News routing.
>
> | v6.2 `migration_driver` | Insert `_root/05` block verbatim from | Pricing table from | Notes |
> |---|---|---|---|
> | `module_compression` | `_root/05 §3.1.2` (Good News canonical mechanic block) | `_root/05 §3.1.4` (Good News canonical row template) | 8 v6.2 pending accounts distributed across 3 segments per `_root/05 §3.1.1`: Tailwind (ml, gc, dccl, pf — 4 accounts), Annual (mali, mah — 2 accounts; renewal-driven timing per `_root/02 §5` + `_root/06 §4.3`), Strategic (ap, mfc — 2 accounts; Watch-band per `_root/02 §4`, routing per `_root/06 §4.2` — Strategic Good-News-eligible accounts do NOT receive a Good News brief; consult `post_hold_action`). For the 4 Tailwind MC accounts that DO route to Good News, paste §3.1.2 verbatim. |
> | `user_count_variance` | `_root/05 §3.2.2` (Good News canonical mechanic block) | `_root/05 §3.2.3` (Good News canonical row template — required, not optional per `_root/05 §3.2.4` voice posture note) | 2 v6.2 pending accounts (rw, jyc — both Tailwind segment per `_root/05 §3.1.1`). Pricing table is REQUIRED for UCV (the per-user math is the proof of the recalibration per `_root/05 §3.2.4`); do not omit. |
> | `rate_architecture` | `_root/05 §3.3.2` (Good News canonical mechanic block) | `_root/05 §3.3.3` (Good News canonical row template) | 1 v6.2 pending account (mlg — Minka Lighting Group, Annual segment per `_root/05 §3.3.1`). Renewal-driven timing per `_root/02 §5`; brief substance unchanged per `_root/06 §4.3`. |
> | All 8 increase-side drivers (`user_rate_normalization`, `platform_discount_correction`, `tier_base_increase`, `included_user_reduction`, `at_book_tier_shift`, `multi_org_retirement`, `annual_discount_retirement`, `special_arrangement`) | NOT carried in Good News | n/a | Out of scope per `_root/05 §2` + `_root/06 §3` row 1. If routing produces an increase-side driver with `comm_action = Good-News Notice`, the routing is suspect — escalate per `_root/CONTRACTS.md §2`. |
> | `already_migrated` | n/a | n/a | Status-marker leak per `_root/05 §1.4`; loader filters per `_root/07 §3`. No brief drafted. |
>
> Good News drivers do not appear with secondary drivers in v6.2 (the 3 decrease-side primary rows in the deduped tally do not carry pipe-separated secondaries; see `_root/05 §3.1.7`-style integration notes if they ever apply). If `secondary_drivers` is non-empty on a Good News routing, consult `_root/05 §4` (secondary-driver weaving matrix); if no entry covers the combination, escalate per `_root/CONTRACTS.md §2`.

**Driver: [DRIVER]**

[INSERT_DRIVER_BLOCK — paste the verbatim block from the `_root/05 §3.X.2` named in the dispatch table above; substitute every bracketed token from v6.2 per `_root/07 §2`. The pricing table row template follows the driver prose per the dispatch table's "Pricing table from" column — paste the verbatim row template from `_root/05 §3.X.3` or `§3.X.4` (MC uses §3.1.4; UCV uses §3.2.3; RA uses §3.3.3). For `user_count_variance` the table is REQUIRED per `_root/05 §3.2.4`; for `module_compression` and `rate_architecture` the table is required per `_root/05 §3.1.4` / `§3.3.3` to land the math.]

---

> **Section 3d — Operations-unchanged sentence (Good News variant).**
>
> Drafter pastes the `_root/04 §4.5` Good News variant — operator-stamped 2026-05-26 at source per `_root/09_changelog.md` Stage 3.4 prep entry. The Good News variant is the default form ("Your workflow, your team's access, your catalog, and your integrations are unchanged. The only thing changing is the invoice.") — the IUR fork does NOT apply because Good News decrease-side scope does not produce `included_user_reduction` primary or secondary drivers per `_root/05 §3` driver coverage. Verbatim — copy character-for-character per `_root/04 §4.5` Good News variant.
>
> Per the strict-placeholder precedent operator-stamped 2026-05-26 (Stage 3.1 review pass — `_root/09_changelog.md`): the §4.5 Good News variant sentence is fetched from `_root/04 §4.5` verbatim, NOT inlined here.

[INSERT `_root/04 §4.5` Good News variant — verbatim, no substitution.]

---

> **Section 3e — Consolidated 2026 framing sentence (Good News variant — `_root/04 §3.1`).**
>
> Drafter pastes the `_root/04 §3.1` Good News consolidated 2026 framing sentence — operator-stamped 2026-05-26 at source per `_root/09_changelog.md` Stage 3.4 prep entry. **This is the Good-News-specific consolidated 2026 sentence; it is DISTINCT from the universal `_root/04 §3` row sentence that Format A / Format B / CEO Letter use.** The Good News variant matches the archived `_brief-template.md` line 88 form ("Every account at every tier is moving to the same pricing structure in 2026. This is the number your configuration produces under that structure.") preserved at `_root/04 §3.1` per the operator stamp.
>
> Per the strict-placeholder precedent operator-stamped 2026-05-26: the §3.1 Good News sentence is fetched from `_root/04 §3.1` verbatim, NOT inlined here. Per `_root/04 §3` row on the consolidated 2026 sentence (which carries the Good News exception explicitly): "Good News notices use the Good News consolidated 2026 sentence in §3.1 below instead of this universal sentence."

[INSERT `_root/04 §3.1` Good News consolidated 2026 framing sentence — verbatim, no substitution. Do NOT use the universal `_root/04 §3` row consolidated sentence; that variant is Format A / Format B / CEO Letter only.]

---

## What's Coming in 2026

> **Section 3f — Roadmap verbatim block (CL-005 — ADDED to Good News per operator decision Q4 2026-05-22).**
>
> Drafter pastes the verbatim "What's Coming in 2026" block from `_root/03 Section 3`. **This is the additive change in the Good News rebuild**: the archived Good News template OMITS this section entirely (the archived `_brief-template.md` ends after the operations-unchanged + consolidated 2026 sentences and proceeds directly to the "Your Pricing at a Glance" table); per operator decision Q4 2026-05-22 (CL-005), every Stage 3 brief template — including Good News — carries the roadmap block via a Section 3 pointer. Per `_root/03 §3` coverage rule rationale: "a price-decrease notice (Good News) reinforces the relationship by showing what's shipping even when the customer is not being asked for more. Drafters of Good News trim other sections to fit the 200–300-word length target; the roadmap is not the section that gets cut."
>
> The trailing `*[Operator note — remove before sending: …]*` line inside the §3 block is removed before send per `_root/04 §2.14` (operator-note removal as non-negotiable) and QB-046 in `_root/08`.

[INSERT `_root/03 Section 3` verbatim block — verbatim, no substitution; remove the trailing operator-note line before send.]

---

## Your Pricing at a Glance

> **Section 3g — Pricing-at-a-glance 4-row mini-summary table (every Good News brief).**
>
> A short 4-row summary table that recaps the dollar change, the annual change, and the effective date. The table's column / row layout is template scaffolding (drafter-facing structure), not rule prose. Every value the drafter substitutes is sourced from v6.2 per `_root/07 §2`.
>
> **Good News uses the 4-row mini-summary form, NOT the 6-row increase-side form.** The archived `_brief-template.md` lines 92–99 established this scope (Monthly / Annual / Change / Effective date — four rows total); the new template preserves it. The increase-side 6-row form (which adds `Tier` + `Included users` + `Additional user rate` rows per Format A Section 3l-continued, Format B Section 3n, CEO Letter Section 3m) is NOT used in Good News because the driver block above carries the per-driver pricing detail (tier, included users, user-rate math) inline via `_root/05 §3.X.3` / `§3.X.4` row templates. Good News' 4-row summary is intentionally trimmed to fit the 200–300-word length target.

| | Before | After |
|---|---|---|
| **Monthly** | $[CURRENT_MRR] | **$[NEW_MRR]** |
| **Annual** | $[CURRENT_ARR] | **$[NEW_ARR]** |
| **Change** | — | –$[DELTA]/month (–[DELTA_PCT]) |
| **Effective date** | — | [EFFECTIVE_DATE] |

---

> **Section 3h — Close paragraph (Good News no-ask close per `_root/04 §4.12`).**
>
> Drafter pastes the verbatim Good News close from `_root/04 §4.12` — the operator-led no-ask close that distinguishes Good News from Format A's passive offer, Format B's active meeting offer, and CEO Letter's specific-date call commitment. The §4.12 Good News close is "Questions about what's changing or how the new rate was calculated — reach out directly." Per `_root/04 §4.12`: "Good News notices do not include a meeting offer, a call commitment, or a follow-up trigger. The mechanic explains itself; the close confirms there is nothing the reader needs to do."

[INSERT `_root/04 §4.12` Good News close — verbatim, no-ask variant. No substitution required (no `[BRACKETED_TOKEN]` placeholders in the §4.12 Good News close).]

> **Formal-notice line — NOT REQUIRED for Good News per `_root/04 §4.12`.**
>
> Per `_root/04 §4.12` ("immediately after each close, **except Good News**"): the formal-notice italicized line ("*This document also serves as formal written notice of a pricing modification under your SuperCat licensing agreement, effective [EFFECTIVE_DATE].*") is NOT carried in Good News notices. This is the Good-News-specific exception explicitly named in §4.12 — do NOT paste the formal-notice line here. (Format A / Format B / CEO Letter all carry it immediately after their close per `_root/04 §4.12`; Good News alone omits it.)

---

*[CSM NAME] | [TITLE] | SuperCat*

---

> **Section 4 — Pre-send drafter checklist.**
>
> The complete pre-send checklist is the 126-check `_root/08` Quality Bar; the drafter runs every QB-NNN whose `Applies to:` field covers Good News or "all formats" before posting the conformance block. The checks below are the Good-News-specific blockers most often surfaced during drafting — they are convenience pointers only; consulting `_root/08` directly is canonical.
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
> - **QB-013** — format derived from the 6-step routing-decision flow per `_root/06 §2`; the decrease check (step 2) fired.
> - **QB-019** — entity-children do NOT receive a standalone Good News brief; route to entity packet per `_root/02 §3`.
> - **QB-021** — Good-News-eligible account that is Watch / At Risk / Critical does NOT receive a Good News brief; routes through CSM health check-in first per `_root/06 §4.2`. **This is the Good-News-specific blocker** — verify `health_band ∉ {Watch, At Risk, Critical}` AND `value_delivery_score ≥ 40` before drafting.
> - **QB-024** — brief written to `good-news-notices/`.
>
> Data-pipeline:
> - **QB-028** — canonical loader from `_root/07 §3`.
> - **QB-036** + **QB-037** — routing block complete per `_root/07 §7` Good-News matrix (including the Good-News-required fields: `CEO awareness required before send: NO (always)`, `Expansion eligible: required`, `Watch health flag: required`, `Current MRR / New MRR / Delta(negative)` substituted for the standard `Delta:` row, Postgres live-data line OMITTED).
>
> Voice / content (the highest-density section in `_root/08`):
> - **QB-040** / **QB-062** — lede leads with dollar + date, not percentage. (Good News: lede leads with the decrease dollar amount + effective date per Section 3b.)
> - **QB-043** / **QB-068** / **QB-069** — no health bands or dimension scores in client copy.
> - **QB-045** / **QB-072** — universality claim uses "every account we work with" without hedge (when applicable — the Good News consolidated 2026 sentence per `_root/04 §3.1` carries the structural-fairness signal).
> - **QB-046** — "What's Coming in 2026" present verbatim from `_root/03 §3`; operator-note line stripped. **(Particularly important for Good News: the archived template OMITS this section; the new template ADDS it via the CL-005 cleanup.)**
> - **QB-047** — internal routing-note blockquote removed from delivered version.
> - **QB-054** — no competitor-pricing reference (named OR unnamed).
> - **QB-059** — no "no account-specific adjustments" sentence (absence preserved; Good News does not carry a "How This Compares" section).
> - **QB-064** — **Good-News-specific blocker** — no favor framing ("gift," "reward for loyalty," "thank you for being a customer") per `_root/04 §3` row + `_root/05 §3.1.5` / `§3.2.4` / `§3.3.4` voice posture notes ("math, not a favor"). State the mechanic plainly.
> - **QB-065** — no apology for prior pricing.
> - **QB-071** — no peer-range dollar values anywhere in client copy.
> - **QB-085** — Good News does not carry a "How This Compares" section; the absence is the application of `_root/04 §4.11`'s structure-by-omission for Good News.
> - **QB-086** — Good News close verbatim per `_root/04 §4.12` (operator-led, no ask); **NO formal-notice line** per the `_root/04 §4.12` Good News exception ("immediately after each close, except Good News").
> - **QB-098** — **Good-News-specific blocker** — decrease-side drivers (`module_compression`, `user_count_variance`, `rate_architecture`) frame the decrease as a mechanic, not a favor; the Good News close from `_root/04 §4.12` is used per `_root/05 §3.1.5` / `§3.2.4` / `§3.3.4`.
>
> Driver content:
> - **QB-089** — driver block verbatim from `_root/05 §3.X.2` (MC: `§3.1.2`; UCV: `§3.2.2`; RA: `§3.3.2`); pricing table verbatim from `_root/05 §3.X.3` / `§3.X.4`.
> - **QB-090** — every bracketed placeholder substituted from v6.2 per `_root/07 §2`.
> - **QB-091** — conditional sub-blocks rendered iff condition holds (Good News' decrease-side drivers do not currently carry conditional sub-blocks per `_root/05 §3.X` — the mechanic blocks are standalone; the integration-flag note in the dispatch table above applies if v6.2 ever introduces a secondary).
>
> Product / pricing language:
> - **QB-099** — tier reference in the driver block uses the tier label per `_root/03 §1` (T1 — Catalog Essentials / T2 — Commerce Professional / T3 — Commerce Enterprise); tier codes in tables only per `_root/04 §3` row on tier codes in running prose. Good News does NOT carry the full "What You're Getting at $X" verbatim tier block (`_root/03 §1`) — that is an increase-side tier-upsell pattern not applicable to Good News.
> - **QB-100** — user-rate ladder bands (1–10 / 11–25 / 26–50 / 51+ at $25/$22/$20/$18 per `_root/03 §2 Block A`) appear ONLY in driver blocks that render the ladder — `user_count_variance` and `rate_architecture` reference the graduated rate per `_root/05 §3.2.3` / `§3.3.3` table row templates. `module_compression` does not render the ladder.
> - **QB-101** + **QB-102** — no unpublished SKU names, no INTERNAL peer / competitive tables in client copy.
>
> Math reconciliation:
> - **QB-104** — pricing-table Before total = `current_mrr`; After total = `new_total_mrr` exactly (per the driver block's `_root/05 §3.X.3` / `§3.X.4` row template).
> - **QB-105** — stated Δ MRR = `new_total_mrr − current_mrr` within ±$1; the routing block's `Delta: –$[DELTA]/month` matches the lede's `$[DELTA]/month`.
> - **QB-107** — `tier_base` and `included_users` match the assigned tier in `_root/03 §1` (rendered in the driver block's pricing table where applicable — UCV / RA tables surface tier base per `_root/05 §3.2.3` / `§3.3.3`).
> - **QB-111** — `support_fire = TRUE` ⚠️ flag handled correctly (drafted in full; flag in routing block; operator decides send timing).
>
> Cross-doc:
> - **QB-119** — no rule restated outside its owning `_root/` doc (path-reference contract — strict-placeholder precedent operator-stamped 2026-05-26; every `_root/XX §N.M` reference in this template is a pointer, not a restatement).
>
> The above is convenience indexing. The full `_root/08` checklist (drift-control §3, routing §4, data-pipeline §5, voice / content §6, math §7, audit-only §8, cross-doc §9) is the canonical pre-send gate. Drafter pastes Good-News-applicable QB-NNN results into the conformance block per `_root/00_manifest.md §5`.

---

*Cross-references: `_root/00_manifest.md` (required-reading map); `_root/CONTRACTS.md §5` (path-reference contract — this template carries pointers only, not rule prose); `_root/01 §1` (relationship-before-price principle — applies lightly to Good News' warm low-touch register per `_root/04 §4.12` Good News close); `_root/02 §1` (Tailwind segment definition + decrease-side spillover across Annual and Strategic per `_root/05 §3.1.1`); `_root/02 §3` / `§4` / `§5` (overlay rules that gate Good News — entity-children fold into packets; Watch-band carve-out preempts Good News per `_root/06 §4.2`; annual overlay supersedes timing not substance); `_root/03 §3` ("What's Coming in 2026" — added to Good News via CL-005); `_root/03 §6` (no unpublished SKU names); `_root/04 §2` (14 non-negotiables — Good-News-relevant: §2.1 dollar-first lede, §2.3 no apology, §2.5 no health-band names, §2.6 no expansion language, §2.7 universality without hedge, §2.9 "What's Coming in 2026" mandatory, §2.14 internal-routing-note removal); `_root/04 §3` (27-row forbidden-phrase table — Good-News-particularly-relevant rows: gift/reward/favor framing, apology for prior pricing, minimizing language, hedged universality, "transition" describing customer's side); **`_root/04 §3.1` (Good News consolidated 2026 framing sentence — operator-stamped 2026-05-26 — DISTINCT from universal §3 row)**; `_root/04 §4.5` (operations-unchanged sentence — **Good News variant operator-stamped 2026-05-26**; the IUR fork does NOT apply to Good News because decrease-side scope does not produce IUR drivers); `_root/04 §4.12` (Good News close — operator-led, no ask; **NO formal-notice line** — explicit Good News exception); `_root/05 §3.1.2` (MC mechanic block, Good News canonical) + `§3.1.4` (MC pricing table); `_root/05 §3.2.2` (UCV mechanic block) + `§3.2.3` (UCV pricing table — required not optional); `_root/05 §3.3.2` (RA mechanic block) + `§3.3.3` (RA pricing table); `_root/05 §3.1.5` / `§3.2.4` / `§3.3.4` (voice posture notes — "math, not a favor"); `_root/06 §1` (Good News definition + sender); `_root/06 §2` (6-step routing-decision flow); `_root/06 §3` row 1 (decrease check); `_root/06 §4.1` (entity overlay); `_root/06 §4.2` (Watch-band carve-out — Format-A-vs-Good-News interaction); `_root/06 §4.3` (annual overlay); `_root/06 §5` + `§5.5` (`comm_action` Good-News Notice + `post_hold_action` variants); `_root/07 §2` (v6.2 field guide); `_root/07 §5` (fallback rules — `support_fire` handling); `_root/07 §6` (file naming — `good-news-notices/[ord_id]__[company-slug]__brief.md`); `_root/07 §7` (routing-block matrix — canonical Good-News row including Watch health flag + Expansion eligible required + Current/New/Delta substitution + Postgres live-data omission); `_root/08` (Quality Bar — 126 QB-NNN checks; Good-News-specific: QB-021 + QB-064 + QB-098); `_meta/stage3_cleanup.md` (CL-001 / CL-003 / CL-004 / CL-005 / CL-022 history; CL-006 RESOLVED-into-CL-005 for the original Good News roadmap omission).*
