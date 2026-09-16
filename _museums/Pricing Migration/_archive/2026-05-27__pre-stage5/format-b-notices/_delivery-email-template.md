# Format B — Delivery Email Template
*Notice + Meeting Offer | CS-sent | Wraps the Format B brief; carries an active meeting offer; supports the CEO Pre-Call → Format B variant*

---

> **Section 1 — Operator notes — drafter-facing scaffolding; remove this entire blockquote before sending.**
>
> **When to use.** The completed Format B brief (per `format-b-notices/_brief-template.md`) does the heavy lifting; this email is the wrapper that delivers it AND carries Format B's distinguishing close — the active meeting offer per `_root/04 §4.12`. The mechanical scope is Format B's scope per `_root/06 §3` (standard `$81 ≤ Δ ≤ $399`; CEO Pre-Call → Format B for `Δ ≥ $600`). The substantive routing decision was already made when the brief template was selected. If you are second-guessing the format choice here, the answer is in `_root/06 §3` and the higher-touch-wins precedence rule.
>
> **Who sends.** CS team (Kylor). For standard Format B — no CEO co-signature or pre-engagement per `_root/06 §1`. For CEO Pre-Call → Format B — the CEO has already called the account BEFORE this email is sent; CS still sends and signs the email; the CEO does NOT co-sign (CEO-signed delivery is the CEO Letter format per `_root/06 §1`). The CEO-awareness state is recorded in Section 2 below per `_root/07 §7` matrix.
>
> **Length.** ~5–6 sentences across 3 short paragraphs. Format B is longer than Format A's 4-sentence wrapper because the active meeting offer (per `_root/04 §4.12`) plus the optional one-sentence relationship hook plus the variant CEO Pre-Call acknowledgement push the count up. Do not exceed a fourth paragraph; the substance lives in the attached brief, not in the email. If you find yourself writing four paragraphs, you've crossed into CEO Letter territory (specific-date call commitment, CEO sign-off, longer narrative); back out and consult `ceo-letter-notices/_delivery-email-template.md` (when authored) or escalate per `_root/CONTRACTS.md §2`.
>
> **What is NEVER in this email.** The prohibitions below all cite specific rows in `_root/04 §3` or non-negotiables in `_root/04 §2`; do not restate the rules — consult the cited section if there is doubt. Absent rules surface as escalation per `_root/CONTRACTS.md §2`.
> - No percentage figure in the dollar-change sentence (`_root/04 §3` row on leading with a percentage; `_root/04 §2.1` non-negotiable). The brief carries the percentage in its summary table; the email leads with dollars.
> - No "we're adjusting your pricing" or minor variants (`_root/04 §3` row).
> - No minimizing language — "modest," "small," "minor" (`_root/04 §3` row).
> - No apology for the change or for the legacy structure (`_root/04 §2.3` + `_root/04 §3` row on apology for prior pricing).
> - No reference to other accounts, tiers, expansion opportunities, or upsells (`_root/04 §2.6` + `_root/04 §3` rows on expansion language). Migration first; Format C only after a confirmed positive signal per `_root/04 §2.6`. Format B's meeting offer is a migration meeting (questions / context / next steps on this change), NOT a discovery call.
> - No specific-date call commitment (that is the CEO Letter's distinguishing feature per `_root/06 §1` and `_root/04 §4.12` CEO Letter close). Format B's meeting offer is an active invitation — "happy to find time" / "let's grab 20 minutes" register — not a calendar lock.
> - No "I'll have my assistant set up a time" or assistant-coordinated booking (also CEO Letter register per `_root/04 §4.12`). Format B's CSM coordinates directly with the contact.
> - No health-band names or dimension scores anywhere (`_root/04 §2.5` + `_root/04 §3` rows on health-band names and dimension scores).
> - No peer-range dollar values, no competitor pricing references (named OR unnamed), no "no account-specific adjustments" sentence (`_root/04 §3` rows on peer-range dollar values, competitor pricing, and "no account-specific adjustments" — CL-003 / CL-004 / CL-001 universal).
> - No unpublished SKU names (`_root/03 §6`).
> - No mention of the prior CEO call's content in detail for the CEO Pre-Call → Format B variant — a one-sentence acknowledgement ("As [CEO_NAME] mentioned…" register) is fine; do not re-summarize the CEO conversation. The CEO call's substance is not re-litigated in writing.

---

> **Section 2 — Internal routing note** (drafter-facing; remove before sending). Section 2 follows the canonical per-format delivery-email routing-block matrix at `_root/07 §7.5` (operator-stamped 2026-05-26; CL-022 RESOLVED).
>
> Brief type: Format B — Notice + Meeting Offer | Delivery email
> Account: [ACCOUNT_NAME] | Tier: [T1/T2/T3] | Wave: [WAVE]
> Migration driver: [DRIVER] | Health: [HEALTH_SCORE] — [HEALTH_BAND]
> Current MRR: $[CURRENT_MRR] | New MRR: $[NEW_MRR] | Delta: +$[DELTA]/month ([DELTA_PCT])
> Cohort: [COHORT_YEAR] | Contract: [MONTHLY/ANNUAL] | Renewal date: [DATE or UNKNOWN]
> Earliest enforceable effective date: [EFFECTIVE_DATE]
> Attachment: [ord_id]__[company-slug]__brief.md (per `_root/07 §6` naming convention)
> Comm_action: [Format B — Notice + Meeting Offer / CEO Pre-Call → Format B] (from routing CSV per `_root/06 §5`)
> CEO awareness required before send: [NO for standard Notice + Meeting Offer / YES for CEO Pre-Call → Format B] (per `_root/07 §7` Format B matrix — conditional on `comm_action`)
>
> Conditional rows — same conditional-fields convention as the brief per `_root/07 §7`:
> - `> **⚠️ SUPPORT FIRE: [N] days open. Production-ready. Operator decides send timing.**` — when `support_fire = TRUE` per `_root/07 §7`. Per `_root/04 §3` row on support-issue context, NOTHING about the support issue appears in client copy; the ⚠️ flag is in this routing block (removed before send) and informs operator send-timing.
> - `> ⚠️ CEO PRE-CALL CONFIRMED — [CEO_NAME] called [CONTACT_NAME] on [PRE_CALL_DATE]. Email reflects that conversation.` — when `comm_action = "CEO Pre-Call → Format B"`. Drafter confirms the CEO call happened BEFORE send; if the call has not happened, escalate per `_root/CONTRACTS.md §2` (do not send Format B in advance of the pre-call).
> - `> ⚠️ CEO PRE-CALL REQUIRED — arrangement was negotiated by [NAME]. Do not send at CSM level before CEO confirms.` — when `migration_driver = special_arrangement` AND `angies_notes` / `discount_drivers` reference a named executive as originator; mirrors the brief's routing-block flag.
> - `> Billing entity: [NAME] — notice routes to billing contact` — when `billing_entity` is non-blank AND ≠ `company`.
>
> Note: Format B's delivery-email routing block does NOT carry `Expansion eligible` (that field is Format A only per `_root/07 §7` matrix and per `_root/04 §2.6` — Format B's meeting offer is NOT a discovery call) and does NOT carry `CEO call commitment date` / `CEO name for sign-off` (those are CEO Letter only).

---

> **Section 3 — Email body skeleton.**
>
> The drafter writes / pastes the components below. Format B's email body is structured as 3 short paragraphs: (P1) dollar / date opener + brief pointer, optionally preceded by a one-sentence relationship hook OR (for the CEO Pre-Call variant) a one-sentence CEO-call acknowledgement; (P2) operations-unchanged sentence per `_root/04 §4.5`; (P3) active meeting offer per `_root/04 §4.12` Format B close + formal-notice line. The signature follows.

**Subject:** [ACCOUNT_NAME]: your SuperCat pricing is changing — effective [EFFECTIVE_DATE]

Hi [CONTACT_NAME],

> **Paragraph 1 — opener.**
>
> Sentence 1a (CONDITIONAL — one of three forms):
> - **DEFAULT (standard Format B, Thriving / Healthy)**: drafter writes a one-sentence relationship hook — names the relationship in 8–15 words ("Wanted to give you a heads-up directly given how long we've worked together," register, or equivalent). Per `_root/04 §4.1` relationship-before-price principle; per `_root/04 §4.2` lede stat guardrail (no provisioned-vs.-active ratio, no per-order subscription cost, eCat-scoped order language if used). Tenure may be referenced; specific stats stay in the brief.
> - **CEO PRE-CALL VARIANT (`comm_action = "CEO Pre-Call → Format B"`)**: drafter writes a one-sentence acknowledgement of the prior CEO call ("Following up on [CEO_NAME]'s call last week," register, or equivalent — does not re-summarize the CEO conversation's content per Section 1 above). One sentence; no recap.
> - **HEALTH-OVERRIDE EDGE CASE (Watch / At Risk / Critical / VD<40 that survives stabilization and lands on Format B)**: OMIT sentence 1a entirely per `_root/04 §4.13` — the email opens directly with the dollar-change sentence (sentence 1b). Most health-flagged accounts route to Strategic per `_root/02 §4` + `_root/06 §4.2`; this fork is preserved for the rare Format-B-eligible edge case.
>
> Sentence 1b (always present): drafter writes a one-sentence dollar-change effective-date sentence per `_root/04 §4.13` standalone form, ending with a brief pointer. Lead with dollar amount and effective date per `_root/04 §2.1`. The email's first content sentence mirrors the brief's Section 3c sentence trimmed for email delivery — same dollar and date, with the attachment pointer appended. Drafter substitutes `[EFFECTIVE_DATE]`, `[CURRENT_MRR]`, `[NEW_MRR]`, `[DELTA]` from v6.2 per `_root/07 §2`. Per the strict-placeholder precedent operator-stamped 2026-05-26 (Stage 3.1 review pass): the §4.13 sentence is fetched from `_root/04 §4.13`, NOT inlined here; only the attachment-pointer phrase is drafter-generated.

[SENTENCE_1a — drafter-generated, one sentence; one of three forms per the selector above. OMIT for the health-override edge case.]

[SENTENCE_1b — drafter-generated, one sentence; per `_root/04 §4.13` standalone form with attachment pointer ("…the attached brief walks through what's behind it and what you're getting at the new price."). Substitute v6.2 tokens.]

> **Paragraph 2 — operations-unchanged.**
>
> Drafter pastes the `_root/04 §4.5` sentence — DEFAULT variant unless v6.2 `migration_driver = included_user_reduction` OR `secondary_drivers` includes `included_user_reduction`; in that case, the IUR-fork variant. Same selector as the brief's Section 3o (operations-unchanged paragraph). Verbatim — copy character-for-character per `_root/04 §4.5`. For IUR cases, the IUR-fork variant per `_root/04 §2.13` non-negotiable.

[INSERT `_root/04 §4.5` sentence — DEFAULT variant unless v6.2 `migration_driver = included_user_reduction` OR `secondary_drivers` includes `included_user_reduction`; in that case INSERT the IUR-fork variant. Verbatim.]

> **Paragraph 3 — active meeting offer + formal-notice line.**
>
> Drafter pastes the verbatim Format B close from `_root/04 §4.12` — the active meeting offer that distinguishes Format B from Format A's passive offer and from the CEO Letter's specific-date call commitment. The §4.12 Format B close is an active invitation; the drafter may calibrate one sentence to the specific contact (preserving the active register; never a specific date, never an assistant-coordinated booking) but the §4.12 verbatim form is the canonical close text. **For the CEO Pre-Call → Format B variant**: the close MAY be adjusted to acknowledge the prior CEO call ("…happy to pick up where [CEO_NAME] left off if it helps," register) per the archived Format B delivery email's operator note + `_root/04 §4.12` register. The active register is unchanged; the §4.12 verbatim close is still canonical.
>
> The formal-notice italicized line is required immediately after the close per `_root/04 §4.12`'s "immediately after each close, except Good News" instruction. Drafter pastes verbatim; substitute `[EFFECTIVE_DATE]`. Per the strict-placeholder precedent: the formal-notice line is fetched from `_root/04 §4.12`, not inlined here.

[INSERT `_root/04 §4.12` Format B close — verbatim, active meeting offer. Optional per-account adjustment for CEO Pre-Call → Format B variant per Section 1 above + `_root/04 §4.12` register.]

[INSERT `_root/04 §4.12` formal-notice line — verbatim italicized form. Substitute `[EFFECTIVE_DATE]`.]

[CSM_NAME] | Customer Success | SuperCat

---

> **Section 4 — Pre-send drafter checklist.**
>
> The complete pre-send checklist for the email + brief pair is the 126-check `_root/08` Quality Bar. The QB-NNN list in `format-b-notices/_brief-template.md` Section 4 is the canonical convenience pointer. The email-specific checks below are the additional Format-B-delivery items that surface during send — they are convenience pointers; `_root/08` is canonical.
>
> Pre-send (this email):
> - **QB-040** / **QB-062** — sentence 1b leads with dollar + date, not percentage.
> - **QB-041** — no "we're adjusting your pricing" variants.
> - **QB-042** / **QB-065** — no apology.
> - **QB-047** — internal routing-note blockquote (Section 2 above) removed from delivered version.
> - **QB-063** — no minimizing language ("modest," "small," "minor").
> - **QB-067** — no support-issue context in body (the ⚠️ flag stays in the routing block).
> - **QB-068** / **QB-069** — no health-band names or dimension scores in body.
> - **QB-079** — paragraph 2 matches `_root/04 §4.5` verbatim in the correct variant.
> - **QB-086** — paragraph 3 close matches `_root/04 §4.12` Format B active meeting-offer register; NOT the Format A passive register; NOT the CEO Letter specific-date call commitment; formal-notice line present immediately after the close.
> - **QB-025** — for CEO Pre-Call → Format B: routing block carries `CEO awareness required before send: YES`; the CEO call has actually happened before send (drafter confirms in routing block); the email's sentence 1a acknowledges the prior call without re-summarizing per Section 1.
>
> Pre-send (the brief attachment):
> - The brief has already cleared its own `_root/08` checklist per `format-b-notices/_brief-template.md` Section 4. The email's job is to deliver the brief without violating the email's own constraints; do not re-edit the brief at delivery time.
>
> Operational confirmations:
> - Confirm `[EFFECTIVE_DATE]` is at least 60 days from send date per `_root/01 §3` operating principle 2 + `_root/06 §3`. For Annual accounts, confirm the ≥90-day notice window per `_root/02 §5` / `_root/06 §4.3`.
> - Confirm the routing CSV's `comm_action` / `post_hold_action` for the account resolves to Format B (standard OR CEO Pre-Call → Format B) — the brief was already routed; re-confirm at send time per `_root/06 §2` + `§5.5`.
> - Confirm the account is not on HOLD per `_root/06 §5` (entity-gating, health flag, unscored). HOLD rows resolve via `post_hold_action`; if `post_hold_action` is Format B, the brief drafts apply.
> - For CEO Pre-Call → Format B: confirm the CEO call has happened and is logged (drafter records `[PRE_CALL_DATE]` in the routing block). If the call has not happened, escalate per `_root/CONTRACTS.md §2` — do NOT send Format B in advance of the pre-call.
>
> Post-send:
> - Log send date; start the 60-day notice clock per `_root/01 §3` operating principle 2.
> - The brief's close is the substantive Format B close per `_root/04 §4.12`; this email's paragraph 3 reinforces it and opens the active calendar invitation.
> - Day 7 follow-up if no meeting accepted — see Section 5. (Format B follows up sooner than Format A's day-10 because the meeting offer is active; an unaccepted meeting offer at day 7 signals the customer wants to absorb the change on their own — convert to passive-mode follow-up or escalate per `_root/CONTRACTS.md §2`.)
> - Audit-only: customer reply analysis per `_root/08 QB-112`.

---

> **Section 5 — Day-7 follow-up (drafter-facing template).**
>
> A short one-sentence follow-up sent only if the customer has not accepted the meeting offer within 7 days. The follow-up does not re-explain the change; it confirms the email landed and reopens the meeting offer once. Same voice constraints as the original email — no minimizing language, no apology, no specific-date call commitment, no assistant-coordinated booking (`_root/04 §3` + `§4.12`). If the customer does not respond to the day-7 follow-up, the offer stays open passively until the effective date; do NOT send a third active prompt (would cross into pressure register per `_root/04 §2.4` proportional-pressure principle and `_root/04 §4.12` Format B register).
>
> The signature is the same CSM. For the CEO Pre-Call → Format B variant: the day-7 follow-up may reference the CEO conversation if the meeting offer was specifically anchored to picking up where the CEO left off; otherwise it does not.

**Subject:** Re: [ACCOUNT_NAME]: your SuperCat pricing is changing — effective [EFFECTIVE_DATE]

Hi [CONTACT_NAME],

[FOLLOWUP_SENTENCE — drafter-generated, one sentence, confirms the original landed AND reopens the meeting offer once; matches the original email's voice per `_root/04` voice rules. For CEO Pre-Call → Format B variant: optionally reference the prior CEO call if anchoring is natural; otherwise no reference.]

[CSM_NAME] | SuperCat

---

> **Section 6 — Voice calibration notes (drafter-facing).**
>
> The email's voice is warm-direct; the brief carries the substance. Per `_root/04 §4.12` Format B close register, the active meeting offer is the email's payload — but the offer is invitation, not pressure (per `_root/04 §2.4` proportional-pressure principle). If you find yourself writing a fourth paragraph in Section 3 above, you've crossed into CEO Letter territory (specific-date call commitment, CEO sign-off, longer narrative); back out and either trim or escalate per `_root/CONTRACTS.md §2` if the account does not match Format B's scope.
>
> Subject-line convention: matches Format A's convention — account name leads (not "SuperCat pricing update") — personalization improves open rate and signals direct communication, not a bulk notice. The convention is template scaffolding shared across Format A and Format B delivery emails for cross-format consistency, not a `_root/04` rule; do not invent a new convention.
>
> CEO Pre-Call → Format B variant — voice posture: the email is still CS-voiced and CS-signed; it is NOT a CEO-voiced email even though the CEO has pre-engaged. The CEO call was the relational signal; the email is the operational delivery. Per `_root/04 §4.12` register and `_root/06 §1` Format B definition.
>
> Format B vs. Format A delivery — what changes: (a) sentence 1a relationship hook OR CEO-call acknowledgement is present in Format B, NOT in Format A; (b) the close is active meeting offer per `_root/04 §4.12` Format B, NOT the passive offer per Format A; (c) the formal-notice italicized line is present in BOTH per `_root/04 §4.12` "immediately after each close, except Good News" rule. The voice rules in `_root/04 §2` / `§3` / `§4` are universal; the close register is the format-specific differentiator.
>
> Format B vs. CEO Letter delivery — what changes (relevant when the routing produces CEO Pre-Call → Format B and the drafter is calibrating): Format B's close is an active meeting offer (open-ended invitation); CEO Letter's close is a specific-date call commitment from the CEO. CEO Pre-Call → Format B uses Format B's close register, NOT the CEO Letter close, even though the CEO has pre-engaged. Per `_root/06 §1` Format B definition and `_root/04 §4.12` register table.
>
> The full voice-rule library lives in `_root/04 §2` (14 non-negotiables), `§3` (27-row forbidden-phrase table), `§4` (14 named voice rules). Consult `_root/04` directly for any sentence the drafter is unsure about; do not improvise per `_root/CONTRACTS.md §2`.

---

*Cross-references: `_root/00_manifest.md` (required-reading map); `_root/CONTRACTS.md §5` (path-reference contract — this template carries pointers only, not rule prose); `_root/01 §1` (relationship-before-price principle) / `§3` (operating principle 2 — 60-day notice clock); `_root/02 §4` / `§5` (health overlay and annual-cohort timing); `_root/04 §2` / `§3` / `§4.1` / `§4.2` / `§4.5` / `§4.12` / `§4.13` (voice rules referenced above); `_root/06 §1` (Format B definition + CEO Pre-Call → Format B routing pattern) / `§3` (delta-tier dispatch) / `§4.2` (health override) / `§4.3` (annual overlay) / `§5` + `§5.5` (`comm_action` vocabulary + HOLD / `post_hold_action` resolution); `_root/07 §2` (v6.2 fields the email substitutes) / `§6` (file naming for the attached brief) / `§7` (routing-block field list — CL-022 note on delivery-email subset enumeration above); `_root/08` (Quality Bar — see Section 4 above for the Format-B-delivery convenience pointers); `_meta/stage3_cleanup.md` CL-022 (delivery-email routing-block subset enumeration in `_root/07 §7`); `format-b-notices/_brief-template.md` (companion brief template; this email wraps the completed brief at delivery time).*
