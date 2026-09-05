# Format A — Delivery Email Template
*60-Day Notice | CS-sent | Wraps the Format A brief; nothing more*

---

> **Section 1 — Operator notes — drafter-facing scaffolding; remove this entire blockquote before sending.**
>
> **When to use.** The completed Format A brief (per `format-a-notices/_brief-template.md`) does the heavy lifting; this email is the wrapper that delivers it. The mechanical scope is Format A's scope per `_root/06 §3` — the substantive routing decision was already made when the brief template was selected. If you are second-guessing the format choice here, the answer is in `_root/06 §3` and the higher-touch-wins precedence rule.
>
> **Who sends.** CS team (Kylor). No CEO co-signature per `_root/06 §1`. No CEO awareness flag required for the standard Format A path.
>
> **Length.** 4 sentences. Do not exceed. If you find yourself writing a third paragraph, you've crossed into Format B territory (active meeting offer + lede activity stats); back out and consult `format-b-notices/_delivery-email-template.md` instead, or escalate per `_root/CONTRACTS.md §2` if the account does not match Format B's scope.
>
> **What is NEVER in this email.** The prohibitions below all cite specific rows in `_root/04 §3` or non-negotiables in `_root/04 §2`; do not restate the rules — consult the cited section if there is doubt. Absent rules surface as escalation per `_root/CONTRACTS.md §2`.
> - No percentage figure in the dollar-change sentence (`_root/04 §3` row on leading with a percentage; `_root/04 §2.1` non-negotiable). The brief carries the percentage in its summary table; the email leads with dollars.
> - No "we're adjusting your pricing" or minor variants (`_root/04 §3` row).
> - No minimizing language — "modest," "small," "minor" (`_root/04 §3` row).
> - No apology for the change or for the legacy structure (`_root/04 §2.3` + `_root/04 §3` row on apology for prior pricing).
> - No reference to other accounts, tiers, expansion opportunities, or upsells (`_root/04 §2.6` + `_root/04 §3` rows on expansion language). Migration first; Format C only after a confirmed positive signal per `_root/04 §2.6`.
> - No pre-committed call (that is Format B's distinguishing feature per `_root/06 §1` and `_root/04 §4.12` Format B close; Format A's close is the passive offer).
> - No health-band names or dimension scores anywhere (`_root/04 §2.5` + `_root/04 §3` rows on health-band names and dimension scores).
> - No peer-range dollar values, no competitor pricing references (named OR unnamed), no "no account-specific adjustments" sentence (`_root/04 §3` rows on peer-range dollar values, competitor pricing, and "no account-specific adjustments" — CL-003 / CL-004 / CL-001 universal).
> - No unpublished SKU names (`_root/03 §6`).

---

> **Section 2 — Internal routing note** (drafter-facing; remove before sending). Section 2 follows the canonical per-format delivery-email routing-block matrix at `_root/07 §7.5` (operator-stamped 2026-05-26; CL-022 RESOLVED).
>
> Brief type: Format A — 60-Day Notice | Delivery email
> Account: [ACCOUNT_NAME] | Tier: [T1/T2/T3] | Wave: [WAVE]
> Migration driver: [DRIVER] | Health: [HEALTH_SCORE] — [HEALTH_BAND]
> Current MRR: $[CURRENT_MRR] | New MRR: $[NEW_MRR] | Delta: +$[DELTA]/month ([DELTA_PCT])
> Cohort: [COHORT_YEAR] | Contract: [MONTHLY/ANNUAL] | Renewal date: [DATE or UNKNOWN]
> Earliest enforceable effective date: [EFFECTIVE_DATE]
> Attachment: [ord_id]__[company-slug]__brief.md (per `_root/07 §6` naming convention)
> Comm_action: `Format A — 60-Day Notice` (from routing CSV per `_root/06 §5`; or `Format A — 60-Day Notice (after CSM touchpoint)` / `(after renewal-date confirm)` per `_root/06 §5.5` `post_hold_action` variants)
> CEO awareness required before send: NO
> Expansion eligible: [YES/NO] — if YES, queue Format C only after confirmed positive signal per `_root/04 §2.6`.
>
> Conditional rows — same conditional-fields convention as the brief per `_root/07 §7`:
> - `> **⚠️ SUPPORT FIRE: [N] days open. Production-ready. Operator decides send timing.**` — when `support_fire = TRUE` per `_root/07 §7`. Per `_root/04 §3` row on support-issue context, NOTHING about the support issue appears in client copy; the ⚠️ flag is in this routing block (removed before send) and informs operator send-timing.
> - `> Billing entity: [NAME] — notice routes to billing contact` — when `billing_entity` is non-blank AND ≠ `company`.

---

> **Section 3 — Email body skeleton.**
>
> The drafter writes / pastes the components below. Sentence 1 is drafter-generated (the dollar-change effective-date sentence per `_root/04 §4.13`); sentence 2 is pasted verbatim from `_root/04 §4.5`; sentence 3 is drafter-generated (the passive offer matching the Format A close register per `_root/04 §4.12`); sentence 4 is the signature.

**Subject:** [ACCOUNT_NAME]: your SuperCat pricing is changing — effective [EFFECTIVE_DATE]

Hi [CONTACT_NAME],

> **Sentence 1 — dollar / date opener.**
>
> Drafter writes a one-sentence dollar-change effective-date sentence per `_root/04 §4.13`'s standalone form. Lead with dollar amount and effective date per `_root/04 §2.1` (and the `_root/04 §3` row on leading with a percentage). The email's first sentence is the brief's Section 3c sentence trimmed for email delivery — same dollar and date, one short attachment-pointer sentence. Drafter substitutes `[EFFECTIVE_DATE]`, `[CURRENT_MRR]`, `[NEW_MRR]`, `[DELTA]` from v6.2 per `_root/07 §2`.

[SENTENCE_1 — drafter-generated, one sentence, leads with dollars + date per `_root/04 §4.13` standalone form; ends by pointing to the attached brief. Substitute v6.2 tokens.]

> **Sentence 2 — operations-unchanged.**
>
> Drafter pastes the `_root/04 §4.5` sentence — DEFAULT variant unless `secondary_drivers` includes `included_user_reduction`; in that case, the IUR-fork variant. Same selector as the brief's Section 3m (operations-unchanged paragraph). Verbatim — copy character-for-character per `_root/04 §4.5`.

[INSERT `_root/04 §4.5` sentence — DEFAULT variant unless v6.2 `secondary_drivers` includes `included_user_reduction`; in that case INSERT the IUR-fork variant. Verbatim.]

> **Sentence 3 — passive offer.**
>
> Drafter writes a one-sentence echo of the Format A close per `_root/04 §4.12` Format A passive variant. Do NOT pre-commit a call (that's Format B's distinguishing feature per `_root/04 §4.12`). The sentence is "If you'd like to talk through anything before [EFFECTIVE_DATE] — reach out directly" register, but the drafter calibrates the exact wording to the account; the only structural requirement is the passive register (no call commitment, no specific date, no "I'll reach out").

[SENTENCE_3 — drafter-generated passive offer matching `_root/04 §4.12` Format A close register. No call commitment, no specific date, no active reach-out promise. One sentence.]

[CSM_NAME] | Customer Success | SuperCat

---

> **Section 4 — Pre-send drafter checklist.**
>
> The complete pre-send checklist for the email + brief pair is the 126-check `_root/08` Quality Bar. The QB-NNN list in `format-a-notices/_brief-template.md` Section 4 is the canonical convenience pointer. The email-specific checks below are the additional Format-A-delivery items that surface during send — they are convenience pointers; `_root/08` is canonical.
>
> Pre-send (this email):
> - **QB-040** / **QB-062** — sentence 1 leads with dollar + date, not percentage.
> - **QB-041** — no "we're adjusting your pricing" variants.
> - **QB-042** / **QB-065** — no apology.
> - **QB-047** — internal routing-note blockquote (Section 2 above) removed from delivered version.
> - **QB-063** — no minimizing language ("modest," "small," "minor").
> - **QB-079** — sentence 2 matches `_root/04 §4.5` verbatim in the correct variant.
> - **QB-086** — sentence 3 matches `_root/04 §4.12` Format A passive register; no pre-committed call.
> - **QB-067** — no support-issue context in body (the ⚠️ flag stays in the routing block).
>
> Pre-send (the brief attachment):
> - The brief has already cleared its own `_root/08` checklist per `format-a-notices/_brief-template.md` Section 4. The email's job is to deliver the brief without violating the email's own constraints; do not re-edit the brief at delivery time.
>
> Operational confirmations:
> - Confirm `[EFFECTIVE_DATE]` is at least 60 days from send date per `_root/01 §3` operating principle 2 + `_root/06 §3`. For Annual accounts, confirm the ≥90-day notice window per `_root/02 §5` / `_root/06 §4.3`.
> - Confirm the routing CSV's `comm_action` / `post_hold_action` for the account resolves to Format A — the brief was already routed; re-confirm at send time per `_root/06 §2` + `§5.5`.
> - Confirm the account is not on HOLD per `_root/06 §5` (entity-gating, health flag, unscored). HOLD rows resolve via `post_hold_action`; if `post_hold_action` is Format A, the brief drafts apply.
>
> Post-send:
> - Log send date; start the 60-day notice clock per `_root/01 §3` operating principle 2.
> - The brief's close is the substantive call invitation per `_root/04 §4.12` Format A passive variant; this email reinforces it.
> - Day 10 follow-up if no acknowledgment — see Section 5.
> - Audit-only: customer reply analysis per `_root/08 QB-112`.

---

> **Section 5 — Day-10 follow-up (drafter-facing template).**
>
> A short one-sentence follow-up sent only if the customer has not acknowledged the original delivery within 10 days. The follow-up does not re-explain the change; it confirms the email landed. Same voice constraints as the original email — no minimizing language, no apology, no pre-committed call (`_root/04 §3` + `§4.12`). The signature is the same CSM.

**Subject:** Re: [ACCOUNT_NAME]: your SuperCat pricing is changing — effective [EFFECTIVE_DATE]

Hi [CONTACT_NAME],

[FOLLOWUP_SENTENCE — drafter-generated, one sentence, confirms the original landed without re-explaining; matches the original email's voice per `_root/04` voice rules.]

[CSM_NAME] | SuperCat

---

> **Section 6 — Voice calibration notes (drafter-facing).**
>
> The email's voice is zero-friction; the brief carries the substance. Per `_root/04 §4.12` Format A close register, the passive offer is the point — no over-explanation in the email body. If you find yourself writing a third paragraph in Section 3 above, you've crossed into Format B territory; back out and either trim or escalate per `_root/CONTRACTS.md §2` if the account does not match Format A's scope.
>
> Subject-line convention: the account name leads (not "SuperCat pricing update") — personalization improves open rate and signals direct communication, not a bulk notice. The convention is template scaffolding, not a `_root/04` rule; do not invent a new convention.
>
> The full voice-rule library lives in `_root/04 §2` (14 non-negotiables), `§3` (27-row forbidden-phrase table), `§4` (14 named voice rules). Consult `_root/04` directly for any sentence the drafter is unsure about; do not improvise per `_root/CONTRACTS.md §2`.

---

*Cross-references: `_root/00_manifest.md` (required-reading map); `_root/CONTRACTS.md §5` (path-reference contract — this template carries pointers only, not rule prose); `_root/04 §2` / `§3` / `§4.5` / `§4.12` / `§4.13` (voice rules referenced above); `_root/06 §1` (Format A definition + sender) / `§3` (delta-tier dispatch) / `§5` + `§5.5` (`comm_action` vocabulary + HOLD / `post_hold_action` resolution); `_root/07 §2` (v6.2 fields the email substitutes) / `§6` (file naming for the attached brief) / `§7` (routing-block field list); `_root/08` (Quality Bar — see Section 4 above for the Format-A-delivery convenience pointers); `format-a-notices/_brief-template.md` (companion brief template; this email wraps the completed brief at delivery time).*
