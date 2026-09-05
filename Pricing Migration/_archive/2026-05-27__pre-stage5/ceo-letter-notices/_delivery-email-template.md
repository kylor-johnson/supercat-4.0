# CEO Letter — Delivery Email Template
*CEO-sent | $400 ≤ Δ ≤ $599 | Wraps the CEO Letter brief; carries the specific-calendar-date call commitment per `_root/04 §4.12`*

---

> **Section 1 — Operator notes — drafter-facing scaffolding; remove this entire blockquote before sending.**
>
> **When to use.** The completed CEO Letter brief (per `ceo-letter-notices/_brief-template.md`) does the heavy lifting; this email is the CEO-sent wrapper that delivers it AND carries the CEO Letter's distinguishing close — the specific-calendar-date call commitment per `_root/04 §4.12`. The mechanical scope is CEO Letter's scope per `_root/06 §3` (`$400 ≤ Δ ≤ $599`). The substantive routing decision was already made when the brief template was selected. If you are second-guessing the format choice here, the answer is in `_root/06 §3` and the higher-touch-wins precedence rule.
>
> **Who sends.** The CEO sends from the CEO's own email address per `_root/06 §1` + `_root/02 §2`. CS team (Kylor) prepares the draft; the CEO reviews, personalizes the lede and close, and approves before send. CEO awareness is `YES (always)` per `_root/07 §7` CEO Letter row — non-negotiable; never sent without CEO sign-off. **Do not send from the CS queue.**
>
> **Length.** ~5–7 sentences across 3–4 short paragraphs. CEO Letter is longer than Format A's 4-sentence wrapper and Format B's ~6-sentence wrapper because (a) the specific-date call commitment per `_root/04 §4.12` is paragraph 4's payload, (b) the CEO opens peer-to-peer rather than as the CS team, and (c) the tenure acknowledgment for early-adopter accounts adds a one-sentence integration. Do not exceed a fifth paragraph; the substance lives in the attached brief, not in the email. If you find yourself writing five paragraphs, you've crossed into letter-not-email territory; back out and either trim or escalate per `_root/CONTRACTS.md §2`.
>
> **What is NEVER in this email.** The prohibitions below all cite specific rows in `_root/04 §3` or non-negotiables in `_root/04 §2`; do not restate the rules — consult the cited section if there is doubt. Absent rules surface as escalation per `_root/CONTRACTS.md §2`.
> - No percentage figure in the dollar-change sentence (`_root/04 §3` row on leading with a percentage; `_root/04 §2.1` non-negotiable). The brief carries the percentage in its summary table; the email leads with dollars.
> - No "we're adjusting your pricing" or minor variants (`_root/04 §3` row).
> - No minimizing language — "modest," "small," "minor" (`_root/04 §3` row).
> - No apology for the change or for the legacy structure (`_root/04 §2.3` + `_root/04 §3` row on apology for prior pricing).
> - No reference to other accounts, tiers, expansion opportunities, or upsells (`_root/04 §2.6` + `_root/04 §3` rows on expansion language). Migration first; Format C only after a confirmed positive signal per `_root/04 §2.6`. The CEO call commitment is a migration conversation (questions / context / next steps on this change), NOT a discovery call.
> - No vague timing ("soon," "in the coming days," "shortly") in the call commitment (`_root/04 §4.12` CEO Letter close anti-pattern). The date is a specific calendar date within 5 business days of send — same date that appears in the brief's Section 3o close AND in the Section 2 routing block below.
> - No "I'll have my assistant set up a time" or assistant-coordinated booking when the CEO is the named caller (per `_root/04 §4.12` CEO Letter register — the CEO calls personally, even if scheduling is assistant-coordinated; the email's commitment is "I'll call you," not "my office will reach out").
> - No active meeting offer ("happy to find time," "let's grab 20 minutes") in place of the specific-date commitment — that is Format B's register per `_root/04 §4.12` Format B close. CEO Letter commits to a date; it does not invite open-ended scheduling.
> - No passive offer ("if you'd like to talk through anything, reach out") in place of the specific-date commitment — that is Format A's register per `_root/04 §4.12` Format A close.
> - No health-band names or dimension scores anywhere (`_root/04 §2.5` + `_root/04 §3` rows on health-band names and dimension scores).
> - No peer-range dollar values, no competitor pricing references (named OR unnamed), no "no account-specific adjustments" sentence (`_root/04 §3` rows on peer-range dollar values, competitor pricing, and "no account-specific adjustments" — CL-003 / CL-004 / CL-001 universal). **CL-001 reminder**: the archived CEO Letter delivery email at `_archive/.../ceo-letter-notices/_delivery-email-template.md` does NOT carry the forbidden sentence (the archived brief at line 232 does, but the archived email is clean); the new email MUST NOT introduce it.
> - No unpublished SKU names (`_root/03 §6`).

---

> **Section 2 — Internal routing note** (drafter-facing; remove before sending). Section 2 follows the canonical per-format delivery-email routing-block matrix at `_root/07 §7.5` (operator-stamped 2026-05-26; CL-022 RESOLVED).
>
> Brief type: CEO Letter + Call Commitment | Delivery email
> Account: [ACCOUNT_NAME] | ord_id: [ORD_ID] | Tier: [T1/T2/T3] | Wave: [WAVE]
> Migration driver: [DRIVER] | Health: [HEALTH_SCORE] — [HEALTH_BAND]
> Current MRR: $[CURRENT_MRR] | New MRR: $[NEW_MRR] | Delta: +$[DELTA]/month ([DELTA_PCT])
> Cohort: [COHORT_YEAR] | Contract: [MONTHLY/ANNUAL] | Renewal date: [DATE or UNKNOWN]
> Earliest enforceable effective date: [EFFECTIVE_DATE]
> Attachment: [ord_id]__[company-slug]__brief.md (per `_root/07 §6` naming convention)
> Comm_action: CEO Letter + Call Commitment (from routing CSV per `_root/06 §5`)
> **CEO awareness confirmed before send: YES** (per `_root/07 §7` CEO Letter row — always, non-negotiable)
> **CEO call commitment date: [DATE — specific calendar date within 5 business days of send per `_root/04 §4.12`; MUST match the brief's Section 3o close and the brief's Section 2 routing block]**
> CEO name for sign-off: [CEO FIRST + LAST NAME]
> Support fire cleared: [YES/NO]
>
> Conditional rows — same conditional-fields convention as the brief per `_root/07 §7`:
> - `> **⚠️ SUPPORT FIRE: [N] days open. Production-ready. Operator decides send timing (CEO decides for CEO Letter).**` — when `support_fire = TRUE` per `_root/07 §7`. Per `_root/04 §3` row on support-issue context, NOTHING about the support issue appears in client copy; the ⚠️ flag is in this routing block (removed before send) and informs CEO send-timing. **For CEO Letter specifically**: the support fire flag must clear (or the CEO must explicitly accept proceeding with it open) before send; this is a stronger gate than Format A or Format B because the CEO is the named caller. Re-validate `[EFFECTIVE_DATE]` and `[CEO call commitment date]` at unfreeze to maintain the 60-day and 5-business-day windows.
> - `> ⚠️ CEO PRE-CALL REQUIRED — arrangement was negotiated by [NAME]. CEO must confirm context before this email goes out.` — when `migration_driver = special_arrangement` AND `angies_notes` / `discount_drivers` reference a named executive as originator. For CEO Letter this is typically the CEO confirming arrangement history with Finance before the call commitment is made per `_root/05 §2.8.6` operator note.
> - `> ⚠️ USER BILLING RECONCILIATION NEEDED — billed amount implies [M] excess users ($Y/month) but stated trailing average implies [N] excess users ($X/month). Confirm before sending.` — when `_root/07 §4.5` discrepancy threshold tripped; mirrors the brief's routing-block flag.
> - `> Billing entity: [NAME] — notice routes to billing contact` — when `billing_entity` is non-blank AND ≠ `company`.
> - `> Tenure acknowledgment in email: YES — [YEARS] years (cohort [COHORT_YEAR])` — when `cohort_year ≤ 2016`. The CEO Letter delivery email adds a one-sentence tenure acknowledgment after the short-version paragraph for early-adopter accounts; see Section 3 paragraph 2 below.
>
> Note: CEO Letter's delivery-email routing block does NOT carry `Expansion eligible` (that field is Format A only per `_root/07 §7` matrix and per `_root/04 §2.6` — CEO Letter's call commitment is NOT a discovery call) and does NOT carry Format B's `Comm_action = "CEO Pre-Call → Format B"` value (that routes to `format-b-notices/` per `_root/07 §6`; CEO Letter is bounded above at $599).

---

> **Section 3 — Email body skeleton.**
>
> The CEO writes / pastes the components below; CS team prepares the draft and the CEO reviews + personalizes before send. CEO Letter's email body is structured as 4 short paragraphs: (P1) CEO opener + dollar / date + brief pointer (peer-to-peer first-person; the CEO is named as the writer); (P2) the consolidated 2026 framing sentence + tenure acknowledgment for early-adopter accounts (conditional); (P3) operations-unchanged sentence per `_root/04 §4.5` with the IUR-fork variant when applicable; (P4) the specific-date call commitment per `_root/04 §4.12` CEO Letter close + formal-notice line. The signature is the CEO's, not the CSM's.

**Subject:** [ACCOUNT_NAME]: your SuperCat pricing is changing — effective [EFFECTIVE_DATE]

Hi [CONTACT_NAME],

> **Paragraph 1 — CEO peer-to-peer opener + dollar / date + brief pointer.**
>
> Drafter prepares the structure; CEO personalizes the exact wording before send. Sentence 1 is a one-sentence first-person opener that names the CEO as the writer ("I'm writing to you directly…" register, or equivalent — the CEO calibrates to the specific contact and relationship). Sentence 2 is the dollar-change effective-date sentence per `_root/04 §4.13` standalone form, with the attachment pointer appended. The §4.13 sentence is fetched verbatim per the strict-placeholder precedent operator-stamped 2026-05-26 (Stage 3.1 + 3.2 review passes — `_root/09_changelog.md`); only the CEO's opener and the attachment-pointer phrase are CEO-personalized / drafter-generated.
>
> **CEO-Letter-specific framing per `_root/04 §4.1` + `§4.12`**: the opener is peer-to-peer; the writer is the CEO, not "we" or "the SuperCat team." The opener may reference the relationship's significance, the size of the change, or the tenure context (the early-adopter tenure beat moves into Paragraph 2 for the delivery email; the lede beat is the CEO's voice, not stat enumeration — that's the brief's job).

[SENTENCE_1 — CEO-personalized, one sentence, first-person opener naming the CEO as the writer. Per `_root/04 §4.1` register; CEO calibrates to the specific contact and relationship.]

[SENTENCE_2 — drafter-generated using `_root/04 §4.13` standalone form with attachment pointer ("…the attached brief walks through what's behind it and what you're getting at the new price." register). The §4.13 sentence is verbatim from `_root/04 §4.13`; substitute `[EFFECTIVE_DATE]`, `[CURRENT_MRR]`, `[NEW_MRR]`, `[DELTA]` from v6.2 per `_root/07 §2`.]

> **Paragraph 2 — consolidated 2026 framing sentence + tenure acknowledgment (conditional).**
>
> Sentence 2a: drafter pastes the verbatim `_root/04 §3` consolidated 2026 sentence (the "Replacement" column text in the §3 table row). Uniform across Format A / Format B / CEO Letter. Drafter MAY pair this with a one-sentence framing tail (peer-to-peer, naming why CEO Letter accounts hear directly from the CEO) — the framing tail is CEO-personalized, not drafted from `_root/`; preserves the §3 sentence verbatim before the framing tail.
>
> Sentence 2b (CONDITIONAL — `cohort_year ≤ 2016`): drafter pastes a one-sentence tenure acknowledgment per `_root/04 §4.1` (CEO Letter delivery-email variant — first-person, peer-to-peer; the brief's Section 3b lede or Section 3e standalone paragraph carries the longer §4.7 paragraph; the email carries a single acknowledgment sentence). The archived CEO Letter delivery email line 37 captures this pattern ("You've been with us since [YEAR] — that relationship matters and I want you to hear this from me directly." register). The new template references `_root/04 §4.1` directly rather than inlining; substitute `[YEAR]` from `cohort_year`.

[INSERT `_root/04 §3` consolidated 2026 sentence — verbatim, no substitution. Optional CEO-personalized one-sentence framing tail.]

[IF cohort_year ≤ 2016: INSERT `_root/04 §4.1` tenure acknowledgment for CEO Letter delivery email — one sentence, first-person, peer-to-peer. Substitute `[YEAR]` from `cohort_year`. Otherwise omit.]

> **Paragraph 3 — operations-unchanged sentence + IUR fork.**
>
> Drafter pastes the `_root/04 §4.5` sentence — DEFAULT variant unless v6.2 `migration_driver = included_user_reduction` OR `secondary_drivers` includes `included_user_reduction`; in that case, the IUR-fork variant. Same selector as the brief's Section 3n (operations-unchanged paragraph). Verbatim — copy character-for-character per `_root/04 §4.5`. For IUR cases, the IUR-fork variant per `_root/04 §2.13` non-negotiable.
>
> The archived CEO Letter delivery email line 38 captures this fork as an operator note ("For `included_user_reduction` accounts (primary or secondary driver): replace…"); the new template references `_root/04 §4.5` directly rather than inlining the fork logic.

[INSERT `_root/04 §4.5` sentence — DEFAULT variant unless v6.2 `migration_driver = included_user_reduction` OR `secondary_drivers` includes `included_user_reduction`; in that case INSERT the IUR-fork variant. Verbatim.]

> **Paragraph 4 — specific-date call commitment + formal-notice line.**
>
> Drafter pastes the verbatim CEO Letter close from `_root/04 §4.12` — the "I'll Call You" variant with the specific calendar date that distinguishes CEO Letter from Format A's passive offer and Format B's active meeting offer. The §4.12 CEO Letter close is a hard commitment: a specific calendar date within 5 business days of send. **NEVER "soon" or "in the coming days"** — the §4.12 anti-pattern is explicitly named. The date in this paragraph MUST match the date in the brief's Section 3o close AND the date logged in the Section 2 routing block above.
>
> The CEO may add a one-sentence "if that timing doesn't work" tail for scheduling flexibility (per the archived CEO Letter delivery email line 27 pattern — "If you'd rather talk before then, reply here and we'll find time."); the tail is CEO-personalized, not drafted from `_root/`. The specific-date commitment is the structural rule; the tail is optional softening within the CEO Letter register.
>
> The formal-notice italicized line is required immediately after the close per `_root/04 §4.12`'s "immediately after each close, except Good News" instruction. Drafter pastes verbatim; substitute `[EFFECTIVE_DATE]`. Per the strict-placeholder precedent: the formal-notice line is fetched from `_root/04 §4.12`, not inlined here.

[INSERT `_root/04 §4.12` CEO Letter close — verbatim, "I'll Call You" variant with specific calendar date. Substitute `[SPECIFIC DATE]` from the CEO call commitment date logged in Section 2 above. Optional CEO-personalized one-sentence scheduling-flexibility tail.]

[INSERT `_root/04 §4.12` formal-notice line — verbatim italicized form. Substitute `[EFFECTIVE_DATE]`.]

[CEO FIRST NAME] [CEO LAST NAME] | CEO | SuperCat

---

> **Section 4 — Pre-send drafter checklist.**
>
> The complete pre-send checklist for the email + brief pair is the 126-check `_root/08` Quality Bar. The QB-NNN list in `ceo-letter-notices/_brief-template.md` Section 4 is the canonical convenience pointer. The email-specific checks below are the additional CEO-Letter-delivery items that surface during send — they are convenience pointers; `_root/08` is canonical.
>
> Pre-send (this email):
> - **QB-040** / **QB-062** — sentence 2 leads with dollar + date, not percentage.
> - **QB-041** — no "we're adjusting your pricing" variants.
> - **QB-042** / **QB-065** — no apology.
> - **QB-047** — internal routing-note blockquote (Section 2 above) removed from delivered version.
> - **QB-059** — no "no account-specific adjustments" sentence anywhere (CL-001 — the archived CEO Letter email is clean; the new email MUST stay clean).
> - **QB-063** — no minimizing language ("modest," "small," "minor").
> - **QB-067** — no support-issue context in body (the ⚠️ flag stays in the routing block).
> - **QB-068** / **QB-069** — no health-band names or dimension scores in body.
> - **QB-079** — paragraph 3 matches `_root/04 §4.5` verbatim in the correct variant (DEFAULT vs IUR-fork — same selector as the brief).
> - **QB-086** — paragraph 4 close matches `_root/04 §4.12` CEO Letter "I'll Call You" register with a SPECIFIC calendar date within 5 business days of send; NOT the Format A passive offer; NOT the Format B active meeting offer; NEVER vague timing ("soon," "in the coming days"); formal-notice italicized line present immediately after the close.
> - **QB-024** + **QB-025** — CEO awareness confirmed YES in the routing block before send; brief written to `ceo-letter-notices/`; the CEO has personally reviewed and approved this email's lede and close per `_root/02 §2` ownership boundary.
> - **QB-NNN cross-check** — the specific calendar date in this email's paragraph 4 MATCHES the specific calendar date in the brief's Section 3o close AND the date in the Section 2 routing block. Three-location parity is a CEO-Letter-specific blocker.
>
> Pre-send (the brief attachment):
> - The brief has already cleared its own `_root/08` checklist per `ceo-letter-notices/_brief-template.md` Section 4. The email's job is to deliver the brief without violating the email's own constraints; do not re-edit the brief at delivery time.
>
> Operational confirmations:
> - Confirm `[EFFECTIVE_DATE]` is at least 60 days from send date per `_root/01 §3` operating principle 2 + `_root/06 §3`. For Annual accounts, confirm the ≥90-day notice window per `_root/02 §5` / `_root/06 §4.3`.
> - Confirm the routing CSV's `comm_action` / `post_hold_action` for the account resolves to `CEO Letter + Call Commitment` — the brief was already routed; re-confirm at send time per `_root/06 §2` + `§5.5`.
> - Confirm the account is not on HOLD per `_root/06 §5` (entity-gating, health flag, unscored). HOLD rows resolve via `post_hold_action`; if `post_hold_action` is CEO Letter, the brief drafts apply.
> - Confirm the CEO call commitment date is on the CEO's calendar BEFORE the email goes out — `_root/04 §4.12` is a hard commitment; the call must actually happen by that date. Drafter logs the date in the routing block; CEO confirms calendar entry.
> - For Watch / At Risk / Critical / VD<40 surviving stabilization (rare for CEO Letter — most route to Strategic per `_root/02 §4` + `_root/06 §4.2`): the `_root/04 §4.13` CEO Letter health-band lede override fires in the brief's Section 3c; the email's Paragraph 1 sentence 2 mirrors the same dollar-change sentence per `_root/04 §4.13`.
>
> Post-send:
> - Log send date; start the 60-day notice clock per `_root/01 §3` operating principle 2.
> - The brief's close is the substantive CEO Letter close per `_root/04 §4.12`; this email's paragraph 4 reinforces it and locks the specific calendar date.
> - **CEO must place the call by the committed date.** This is the highest-stakes follow-up across all four formats — if the call slips, the §4.12 close becomes a credibility failure. CEO calendar is the source of truth; drafter does not re-prompt the CEO to call; the date was committed at send.
> - Audit-only: customer reply analysis per `_root/08 QB-112`; CEO call execution per `_root/08 QB-114`.

---

> **Section 5 — Voice calibration notes (drafter-facing).**
>
> The email's voice is CEO peer-to-peer; the brief carries the substance. Per `_root/04 §4.12` CEO Letter close register, the specific-date call commitment is the email's payload — but the commitment is a hard date, not soft scheduling. If you find yourself writing a fifth paragraph in Section 3 above, you've crossed into letter-not-email territory; back out and either trim or escalate per `_root/CONTRACTS.md §2`.
>
> Subject-line convention: matches Format A's and Format B's convention — account name leads (not "SuperCat pricing update") — personalization improves open rate and signals direct communication, not a bulk notice. The convention is template scaffolding shared across all four formats for cross-format consistency, not a `_root/04` rule; do not invent a new convention. The "pricing" wording (not "invoice") was operator-stamped 2026-05-26 across all 4 formats per `_root/09_changelog.md` — uniform.
>
> CEO Letter vs. Format B delivery — what changes (relevant when the routing produces $400 ≤ Δ ≤ $599 vs Δ ≥ $600 CEO Pre-Call → Format B): CEO Letter's close is a specific-date call commitment from the CEO directly; Format B's close (including CEO Pre-Call → Format B) is an active meeting offer from CS. CEO Pre-Call → Format B uses Format B's close register, NOT this one — the CEO has pre-engaged but CS sends and signs. CEO Letter is the only format where the CEO is the named caller in the close. Per `_root/06 §1` Format definitions and `_root/04 §4.12` register table.
>
> CEO Letter vs. Format A delivery — what changes: CEO Letter's close is a specific-date call commitment from the CEO; Format A's close is a passive offer from CS ("if you'd like to talk through anything, reach out"). The voice rules in `_root/04 §2` / `§3` / `§4` are universal; the close register is the format-specific differentiator.
>
> CEO Pre-Call → Format B variant — clarifying boundary: if the routing produces `Δ ≥ $600` and `comm_action = "CEO Pre-Call → Format B"`, use `format-b-notices/_delivery-email-template.md` (Stage 3.2), NOT this template. CEO Letter ends at $599 per `_root/06 §3`. The CEO has pre-engaged in both formats above $400, but the structural delivery is different: CEO Letter is CEO-sent with a specific-date commitment; CEO Pre-Call → Format B is CS-sent with an active meeting offer after the CEO has already called. Do not confuse the two.
>
> CEO personalization scope: the CEO personalizes (a) Paragraph 1 sentence 1 — first-person opener; (b) optional one-sentence framing tail in Paragraph 2; (c) optional one-sentence scheduling-flexibility tail in Paragraph 4. Everything else is fetched verbatim from `_root/` per the path-reference contract. The CEO does NOT improvise sentence-level wording on the §4.13 dollar-change sentence, the §3 consolidated 2026 sentence, the §4.5 operations-unchanged sentence, the §4.12 close, or the §4.12 formal-notice line; those are verbatim per `_root/CONTRACTS.md §2`.
>
> The full voice-rule library lives in `_root/04 §2` (14 non-negotiables), `§3` (27-row forbidden-phrase table), `§4` (14 named voice rules). Consult `_root/04` directly for any sentence the CEO or drafter is unsure about; do not improvise per `_root/CONTRACTS.md §2`.

---

*Cross-references: `_root/00_manifest.md` (required-reading map); `_root/CONTRACTS.md §5` (path-reference contract — this template carries pointers only, not rule prose); `_root/01 §1` (relationship-before-price principle) / `§3` (operating principle 2 — 60-day notice clock); `_root/02 §2` ($400 ownership boundary that triggers CEO authorship) / `§4` (health overlay) / `§5` (annual-cohort timing); `_root/03 §6` (no unpublished SKU names); `_root/04 §2` / `§3` / `§4.1` (relationship-before-price + tenure acknowledgment for CEO Letter delivery email) / `§4.5` (operations-unchanged + IUR fork) / `§4.12` (CEO Letter close "I'll Call You" + specific-calendar-date constraint + formal-notice line) / `§4.13` (health-band lede override mirrored for the email's paragraph 1 sentence 2); `_root/06 §1` (CEO Letter definition + $400 ownership boundary + sender) / `§3` (delta-tier dispatch — CEO Letter row 4 + CEO Pre-Call → Format B row 5 distinction) / `§4.2` (health override) / `§4.3` (annual overlay) / `§5` + `§5.5` (`comm_action` vocabulary + HOLD / `post_hold_action` resolution); `_root/07 §2` (v6.2 fields the email substitutes) / `§6` (file naming for the attached brief — `[ord_id]__[company-slug]__brief.md`) / `§7` (routing-block field list — CL-022 note on delivery-email subset enumeration above; CEO-Letter-required fields per the §7 CEO Letter row); `_root/08` (Quality Bar — see Section 4 above for the CEO-Letter-delivery convenience pointers including QB-114 CEO call execution audit); `_meta/stage3_cleanup.md` CL-001 (no "no account-specific adjustments" sentence universal) + CL-022 (delivery-email routing-block subset enumeration in `_root/07 §7`); `ceo-letter-notices/_brief-template.md` (companion brief template; this email wraps the completed brief at delivery time and carries the specific-date call commitment that anchors the brief's Section 3o close).*
