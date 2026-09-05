# 04 — Communication Posture

> **What this doc owns**: The voice + language rules for every client-facing artifact in the migration communications system. Audience definition (CFO / business owner / principal — not procurement). The internal-vs.-client boundary. The non-negotiable list. The forbidden-phrase / replacement table. All named voice rules: relationship-before-price opening, lede stat guardrail, above-the-midpoint clause, high-delta lede rule, "only thing changing" line + IUR fork, platform-base-grown sentence, tenure acknowledgment for early-adopter cohorts, value anchor delta-per-order reframe, billing-basis footnote, platform-base conditional inside the URN block, "How This Compares" structure, format-by-format close variants, health-band lede overrides, discount-correction posture. Driver-voice orientation (one paragraph; the driver narrative content itself lives in `_root/05`).
>
> **What this doc DOES NOT own**: Per-driver narrative content (`_root/05`); tier feature language (`_root/03`); segment / format routing (`_root/02` + `_root/06`); data field meanings (`_root/07`); the verification checklist itself (`_root/08` — which imports rules from this doc by reference).
>
> **Last updated**: 2026-05-26 (Stage 4 prep Source-fix Session A — Extension 1: `§1.1` Audience register table added at the end of §1 [4-row table contrasting program audience (CFO/owner/principal of furniture/lighting/decor wholesaler) with SaaS-renewal-drift audiences (procurement, IT buyer, "platform admin") per `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix A.2; framing sentence "Write for a principal who runs a wholesale business, not a software buyer renewing a SaaS seat." pasted verbatim; cross-references to `_root/04 §3` + `§4` + `_root/01 §1` relationship-before-price thesis]. Extension 2: 6 SaaS-renewal forbidden-phrase rows added to `§3` table (1 renewal-vocabulary cluster row grouping "renewal" + "auto-renew" + "subscription renewal" + "at renewal we're adjusting…" per existing percentile-row precedent; 1 "rate card alignment" row distinct from existing "rate card" row; 1 "we're adjusting your pricing" row making the §2.2 non-negotiable greppable in §3; 3 audience-drift rows for "platform admin"-family + "procurement"-family + "IT buyer" per Appendix A.6 + Appendix A.2 audience-register implications). Extension 3: `§4.16` Annual-cohort voice rules NEW sub-section authored [4 sub-sub-sections: §4.16.1 Scope; §4.16.2 Lede effective-date shift; §4.16.3 Close + formal-notice line; §4.16.4 Drafter judgment + surfacing] per `_meta/stage3_cleanup.md` CL-015 + `_reference/2026-05-20__execution_plan_v3.3.md` §III — renewal-date framing replaces migration-effective-date framing in the lede; `_root/04 §4.12` close text + formal-notice line unchanged with `[EFFECTIVE_DATE]` = `[RENEWAL_DATE]` token resolution for Annual accounts; CL-015 RESOLVED at source (location updated §4.15 → §4.16 per 2026-05-26 Stage 3.5 prep annotation). Three additive edits; zero edits to §2 non-negotiables, §3.1 Good News framing sentence, §4.1–§4.15 prose, §5 driver-voice orientation, or §6 footer. Prior 2026-05-26 entry: Stage 3.5 prep — §4.15 Parent-letter voice register added: 6 sub-sections covering voice fork by `delivery_owner` [CEO-delivered + Kylor-delivered HoCS], multi-brand portfolio acknowledgment, cross-brand consolidation lens, per-brand mechanics restraint, default-only pricing posture, routing pointer to per-child notices; cross-format CSM-role note at §4.15.1 — SuperCat's CSM support role does NOT handle migration conversations; "CSM-sent" role-marker filled by Kylor in HoCS role across all 5 Stage 3 templates. **Stage 3.5 review-pass amendment 2026-05-26**: §4.15.1 voice-fork counts reconciled to `_master-entity-data-v6.2.csv` Master Entity tab ground truth — CEO-delivered fork count corrected 3→4 entities [Thesis added: CSV row 13 `delivery_owner = CEO`]; Kylor-delivered fork count corrected 11 rollup→9 rollup entities [Thesis removed; Ferguson exclusion annotation added — Ferguson is Kylor-delivered but excluded from Stage 3.5 template scope per `_root/06 §1.6` mixed-direction exception]; CSV is canonical, rule layer reconciles to CSV. Prior 2026-05-26 entry: Stage 3.4 prep — Good News consolidated 2026 framing sentence at §3.1; Good News operations-unchanged variant at §4.5.)
> **Owner**: CEO
> **Primary sources**: archived `_handoff-prompt.md` §Non-Negotiables + §Language Register + §Driver Framing + §Quality Bar; archived `_template-test-prompt.md` CHECKs 1–8; archived `_current-state.md` §Template Fixes Applied (2026-05-19); archived Format A / Format B / CEO Letter / Good News brief templates and the Migration-Health Artifacts seed templates; archived per-account exemplars (kal, kii, ih, da, pf).
> **Supersedes**: voice rules previously scattered across the templates and orchestration files listed above. Where a template still carries the rule inline (`> **... rule:**` blockquotes), the template should be edited in Stage 3 to reference this doc instead.

---

## Section 1 — Audience and posture

**Audience.** The reader is the CFO, business owner, or principal of a B2B furniture, lighting, or decor wholesaler. They are not a software procurement agent and they are not an end-user. They read a small number of vendor pricing communications per year and they are sophisticated about the ones they do read. They notice tone. They will not respond well to corporate-speak, hedged language, or apology — and they will not respond at all to a brief that fails to demonstrate the writer looked at their specific account.

**Voice posture.** Declarative. Professional. Empathetic on impact. Firm on architecture. The relationship is peer-to-peer (CEO Letter) or vendor-to-principal (Format A / Format B / Good News) — never service-rep-to-buyer and never marketing-to-prospect. The writer is delivering a number the reader has the standing to question, not a pitch the reader is expected to evaluate.

**Internal-vs.-client boundary.** Every artifact in this system is either CLIENT-FACING or INTERNAL-ONLY. Briefs, delivery emails, and the formal-notice line are CLIENT-FACING. The internal routing-note blockquote at the top of every brief, the internal prep sheet (`internal_ceo_cs_prep_sheet.md`), root docs, agent prompts, and the peer-range dollar values are INTERNAL-ONLY. The routing-note blockquote is removed before sending — every time, no exceptions. This boundary is non-negotiable and is named in §2 below.

### §1.1 — Audience register (operator-stamped 2026-05-26)

The audience and posture paragraphs above are elaborated by the audience-register table below. The table contrasts this program's reader — the wholesaler principal defined in the Audience paragraph — with the SaaS-renewal-drift audiences a Stage 4 drafter is most likely to slip into addressing. Per `_root/01 §1`, the migration's purpose is to preserve the relationships that justify SuperCat's embedded position in each customer's workflow; the relationship-before-price thesis forecloses the SaaS-renewal register entirely. Every Stage 4 per-account brief inherits this register by `_root/04 §1` pointer.

| Dimension | This program | SaaS-renewal drift to forbid |
|---|---|---|
| Reader | CFO / owner / principal of a furniture / lighting / decor wholesaler | Procurement, IT buyer, "platform admin" |
| Relationship | Vendor-to-principal or CEO-to-CEO (CEO Letter) | Service-rep-to-buyer, CSM check-in |
| Register | Declarative, empathetic on impact, firm on architecture | Cheerful renewal, "excited to partner," soft upsell |
| What they're evaluating | A specific invoice change with a mechanical explanation | Subscription tier change or contract term sheet |

> Write for a principal who runs a wholesale business, not a software buyer renewing a SaaS seat.

*Cross-references: `_root/04 §3` (the forbidden-phrase table codifies the SaaS-renewal drift register at the phrase level — including the audience-drift rows for "platform admin," "procurement," and "IT buyer" framings); `_root/04 §4` (the named voice rules operate inside this audience register); `_root/01 §1` (the thesis — preserve the relationships that justify the embedded position; relationship-before-price is the strategic anchor this register protects).*

---

## Section 2 — The non-negotiables

Every client-facing draft must pass all of the following. Each item is a single declarative rule with a one-sentence rationale. Numbering here is canonical; templates and prompts may reference items as `_root/04 §2.N`.

1. **Lead with the dollar amount and effective date. Never lead with a percentage.** Percentages amplify the change; dollars ground it in what the reader is actually being asked to pay.
2. **Never use the phrase "we're adjusting your pricing."** Corporate hedging signals a writer who is uncomfortable with the change; the reader notices.
3. **Never apologize for the change.** Apology implies the prior invoice was wrong. It was not wrong — it reflected the legacy structure. Apology also weakens the structural argument the brief is built on.
4. **Confirm operations are unchanged early, using the verbatim sentence in §4.5.** The reader's first question is "what breaks?" The answer is "nothing operational" and they need to see that answer before they will read further.
5. **Never include health scores, health bands, or dimension scores in client-facing copy.** "Thriving," "Healthy," "Watch," "At Risk," "Critical," "Engagement: 81," "Value Delivery: 100" — none of it appears anywhere a client can see. These are internal vocabulary for routing and risk; surfacing them reads as either patronizing or alarming.
6. **Never include expansion or upgrade language in a migration notice.** Format C is a separate document. It is not combined with the migration notice and it is not pre-figured in the migration close. Migration first; expansion only after a confirmed positive signal.
7. **State "every account we work with is moving to the same structure" without hedge.** This is the structural argument for fairness; hedging it ("most accounts," "many accounts," "the broader install base") undermines the only defense the brief has against "why are you doing this to me."
8. **Apply the lede stat guardrail in every brief that has a relationship-stats lede.** Lead with unambiguous platform metrics (users active, sessions, surfaces in use, tenure). If order count is used, scope it explicitly to "orders submitted through SuperCat" — never the account's total order volume. Never frame logins as a provisioned-vs.-active ratio. Never calculate per-order subscription cost in the lede. (Detail: §4.2.)
9. **Every Format A brief includes the "What's Coming in 2026" section verbatim, with no edits.** This section is the asset side of the trade — the reader is being asked to pay more, and they are also being told what is shipping. Skipping it leaves the brief one-sided. (The verbatim block itself is owned by `_root/03`; this doc owns the rule that it must appear.)
10. **When the platform base increases under any driver, include the verbatim platform-base-grown sentence (§4.6).** Do not leave a base increase unexplained. This is the answer to "what am I paying more for?" and it is the same answer regardless of which driver is primary.
11. **When delta exceeds 30%, the lede must name the annual dollar impact (§4.4).** Above 30%, the reader has already done the annualization in their head. Naming it first is disarming, not alarming — it signals the writer knows the size of the ask.
12. **When using "above the midpoint," include the mandatory user-count clause (§4.3).** Without the clause, "above the midpoint" reads as a premium or an arbitrary upcharge. The clause is what makes the position math-readable.
13. **When the `included_user_reduction` driver is primary or secondary, use the IUR-variant close (§4.5) and apply the billing-basis footnote and threshold check.** The IUR account is being told that the included base is moving against them — the unmodified "only thing changing is the invoice" sentence reads as a lie in that case.
14. **The internal routing-note blockquote at the top of every brief is removed before sending.** This is the most common drift event in the system; it is named here as a non-negotiable because it has happened.

---

## Section 3 — Forbidden phrases and their replacements

The table below is comprehensive. The intent is that a future drafter can `grep` it for a phrase they are tempted to use and find either a replacement or a rationale for cutting. Each row pairs one specific forbidden expression with one specific replacement — no aggregation, no "and similar phrases."

| Do not write | Replacement | Why |
|---|---|---|
| "trailing 12-month average" | "your team averages around [N] users" | Operator-internal stat language; alienates a CFO reader. |
| "install base" | "all accounts we work with" / "every account we work with" | Industry jargon; not how a wholesaler principal talks. |
| "full-stack commercial operating system" | Describe what it actually is — "the rep iPad app, your buyer-facing catalog, online ordering, order and invoice tracking, and your sales intelligence dashboard" | Marketing-speak; lands as evasive in a brief that is otherwise specific. |
| "five connected surfaces" | Same — describe each surface by what it does | Internal product vocabulary; the reader does not count surfaces. |
| "p25," "p75," "75th percentile," "interquartile" | "below the midpoint" / "near the midpoint" / "above the midpoint" (plain English position only) | Percentile notation reads as a research paper, not a notice. |
| "T1," "T2," "T3" in running prose | The tier name in prose ("Catalog Essentials," "Commerce Professional," "Commerce Enterprise"). Tier codes are permitted in tables only. | Tier codes belong in tables; in prose they signal the writer is reading from an internal system. |
| Comparison to any competitor's pricing — named OR unnamed (includes phrasings like "equivalent platforms range from $3,000–$3,500/month," "comparable solutions cost roughly $X," or any dollar range positioned against an external category) | Cut entirely. The plain-English position vocabulary in §4.11 ("at the base rate" / "below the midpoint" / "near the midpoint" / "above the midpoint") carries the comparison without exposing a competitive figure. | Competitive pricing references — named or unnamed — are unverifiable by the reader and expose the brief to argument over a number we cannot defend. The "unnamed equivalent" form (e.g. "equivalent platforms range from $3,000–$3,500") is a peer-range-by-stealth and falls under the same prohibition. Operator decision 2026-05-22: the prohibition is universal. Format A and Format B templates currently include this sentence for T3 accounts and require Stage 3 cleanup. |
| "rate card" | "our current standard pricing" / "the standard rate" | "Rate card" is sales-org vocabulary; reads as bureaucratic to a CFO. |
| "as part of this refresh" | "going forward" | "Refresh" minimizes a real change. |
| "SuperCat is standardizing its pricing... first time we've applied a consistent commercial structure..." | The consolidated 2026 sentence: "In 2026, we're moving every account to one clear pricing structure — here's exactly what that means for you." | Iterated to exact wording; copy verbatim. **Good News exception** — Good News notices use the Good News consolidated 2026 sentence in §3.1 below instead of this universal sentence. |
| "Your rate at signing predates the current rate card and we're bringing it in line with the standard structure." | Use the tenure-aware variants in §4.1: (≤5 yrs) "Your rate was set in [YEAR] — this is the first time we've updated it." / (10+ yrs) "Your rate has been unchanged since [YEAR] — this is the first time we've adjusted it." | Generic phrasing; the tenure framing is what earns the explanation. |
| "There are no account-specific adjustments in how [ACCOUNT_NAME]'s number was calculated." | Delete entirely — never write this sentence. | Reads as defensive and triggers the suspicion it tries to disarm. (See open question in conformance: this sentence currently appears in the archived CEO Letter template and in the `da` exemplar — both predate this consolidation and require correction before reuse.) |
| "[X of Y] users logged in in the last 90 days" — provisioned-vs.-active ratio | Output-metric framing: "[Y] sessions logged in the last 90 days across [N] active users." | Ratios read as failure; the same data framed as output reads as proof. (Detail: §4.2.) |
| Per-order subscription cost in the lede ("That works out to $X/order…") | Place per-order math in the "What This Works Out To" section only, under §4.8 | Per-order math earns trust mid-document; in the lede it reads as advance justification. |
| Leading with a percentage ("a 60.7% change…") | Lead with the dollar amount and effective date; the percentage may follow inside the same sentence or in the summary table. | Percentages amplify; dollars ground. (Non-negotiable §2.1.) |
| "modest," "small," "minor" change | Quote the number. If the number is small, it reads small without help. | Minimizing language reads as condescension to a CFO. |
| "gift," "reward for loyalty," "thank you for being a customer" (in a Good News notice) | State the mechanic plainly: "the consolidation produces a lower combined rate" / "the recalculated rate produces a lower invoice" | Decreases are math, not favors. Framing as favor invites the next question — "what do I owe you?" |
| Apology for prior pricing ("we're sorry the legacy structure was…") | Describe the legacy structure neutrally and the new structure plainly | Apology implies the prior invoice was wrong; it was the legacy structure. |
| The account's total ERP-side order volume as a lede stat | Scope to "orders submitted through SuperCat" / "eCat orders" only | Total order volume is not ours to claim; SuperCat-submitted volume is verifiable. |
| Support-issue context in client copy ("we've been working through your support issue…") | Never reference. Flag in the internal routing-note block only; CEO decides send timing. | Pricing and support are separate conversations; conflating them weakens both. |
| Health-band names anywhere ("Thriving," "Healthy," "Watch," "At Risk," "Critical") | Strip entirely | Internal routing vocabulary; never client-facing. (Non-negotiable §2.5.) |
| Dimension scores ("Engagement: 81," "Value Delivery: 100") | Strip entirely | Internal scoring vocabulary; never client-facing. (Non-negotiable §2.5.) |
| Expansion-tier feature names in a migration brief ("at the next tier you'd also get…") | Cut. Format C is a separate document, queued only after a confirmed positive migration signal. | Conflates migration with sell-up; loses both. (Non-negotiable §2.6.) |
| Peer-range dollar values ("Commerce Professional ranges from $1,295–$1,589") in ANY client copy (Format A, Format B, CEO Letter) | Use the verifiable "How This Compares" structure (§4.11) without dollar ranges. Peer dollar values stay INTERNAL-ONLY across every format. | Peer dollars are not verifiable by the reader; the brief loses credibility the moment a number cannot be backed up. Operator decision 2026-05-22: the rule applies uniformly to all four formats. The Format A template still includes peer dollar ranges and requires Stage 3 cleanup to strip them. |
| Hedging the universality claim ("most accounts," "many accounts," "across the broader install base") | "Every account we work with" / "all accounts we work with" — no hedge | Non-negotiable §2.7. Hedging undermines the structural-fairness argument. |
| "Transition" used to describe the customer's side of the move (e.g. "as you transition to the new pricing") | "Going forward" / "Effective [DATE]" — the change is on the invoice, not on the customer | "Transition" implies the customer has work to do. They do not — §4.5 is explicit that operations are unchanged. (Note: "transition" is permitted in narrow administrative contexts such as "we'll document that as part of this transition" inside the `annual_discount_retirement` block — the existing template usage stands until edited.) |
| "Renewal," "auto-renew," "subscription renewal," "at renewal we're adjusting…" | Cut entirely. The pricing change is not a contract-renewal event; lead with the dollar amount and effective date per non-negotiable §2.1, and explain the change via the driver mechanic from `_root/05`. For Annual-cohort accounts, the effective date resolves to the renewal date per `_root/04 §4.16` — but the lede frames the change mechanically, not as a renewal-cycle artifact. | SaaS-renewal vocabulary; signals the wrong audience register per §1.1 (the program is a book normalization, not a subscription-renewal cycle). Operator-stamped 2026-05-26 (Stage 4 prep) via `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix A.6 first bullet — grouped as one row per the percentile-row + health-band-row grouping precedent above. |
| "Rate card alignment" (without tenure / driver context) | Use the tenure-aware variants in §4.1 + the driver-specific framing in `_root/05`. The bare phrase "rate card alignment" is forbidden in any client-facing copy. | Compounds the "rate card" sales-org vocabulary (already prohibited in the row above) with "alignment" — a softening verb that implies the customer was misaligned. Both halves signal SaaS-renewal register per §1.1. Distinct from the "rate card" row above: that row covers the noun alone; this row covers the full noun-phrase construction. |
| "We're adjusting your pricing" | Lead with the dollar amount and effective date per non-negotiable §2.1; describe the structural reason via the driver framing in `_root/05`. | Corporate hedging that signals a writer uncomfortable with the change; the reader notices. Already prohibited at non-negotiable §2.2; this row makes the phrase greppable in the §3 table per the table's stated design intent (a future drafter can `grep` it for a phrase they are tempted to use). |
| "platform admin," "platform admin login," "platform admin role" | Cut entirely. The reader is the principal of a wholesale business, not a software-product administrator. | Software-product vocabulary; signals the wrong audience per §1.1 (Reader column). A wholesaler principal does not have "a platform admin" — they have buyers and reps using the app. |
| "procurement," "your procurement team," "procurement contact" | Cut entirely; address the principal directly by name per §4.1. | The wholesaler principal IS the decision-maker; "procurement" framing misroutes the audience per §1.1 (Reader column) and softens the relationship register from Vendor-to-principal to Vendor-to-procurement-intermediary. |
| "IT buyer," "IT decision-maker" | Cut entirely; address the principal directly per §4.1. | Same wrong-audience signal as "procurement" framing above; the wholesaler principal evaluates pricing themselves, not via an IT-buyer intermediary. SaaS-renewal-drift vocabulary per §1.1. |

### §3.1 — Good News consolidated 2026 framing sentence (operator-stamped 2026-05-26)

Good News notices (`Δ MRR < $0` per `_root/06 §3` row 1) use this sentence **instead of** the universal consolidated 2026 sentence in the §3 row above. Format A, Format B, and CEO Letter continue to use the universal sentence.

> "Every account at every tier is moving to the same pricing structure in 2026. This is the number your configuration produces under that structure."

Copy character-for-character. Do not paraphrase.

---

## Section 4 — Named voice rules

Each subsection states one rule, gives one example that follows the rule, and gives one example that violates it. Rule names are stable identifiers; templates and prompts reference these (e.g. "per `_root/04` §4.6, include the platform-base-grown sentence").

### §4.1 — Opening: relationship before price

The lede paragraph names the relationship before it delivers the number. Tenure and platform-activity stats land in the same paragraph as the dollar change, but they land first. The lede must prove the writer looked at this specific account — not any account.

Tenure-band variations:
- **3+ years tenure**: sentence one names the relationship (years + one activity stat) before any reference to pricing.
- **10+ years tenure**: the weight of the history leads — explicit year reference, named long-tenure framing.

For all accounts, the lede includes at least one stat that demonstrates account-specific reading (sessions, active users, surfaces in use, or scoped order count). Generic ledes ("Thank you for being a SuperCat customer") are categorically prohibited.

```
Follows: "Seven years on SuperCat, and Kalco Lighting / Allegri Crystal is running the full platform — 1,194 sessions logged in the last 90 days, 159 eCat orders submitted across 89 customers in the past year. Your monthly invoice is moving from $2,590 to $2,809 — a $219 change — and this document explains exactly why."
Violates: "Thank you for being a SuperCat customer. Effective July 19, 2026, your monthly invoice will increase by 8.5%."
```

### §4.2 — Lede stat guardrail

The lede uses unambiguous platform metrics: tenure, active users, session volume, surfaces in use. Order counts are supporting evidence, not headline proof. When order count is used, it must be scoped explicitly to "orders submitted through SuperCat" or "eCat orders" — the account's total ERP-side order volume is never the headline.

Two specific prohibitions:
1. **No provisioned-vs.-active user ratio.** "X of Y users logged in" reads as failure even when X is healthy. Express logins as raw output ("[N] sessions logged in the last 90 days across [M] active users"), not as a ratio against provisioned seats.
2. **No per-order subscription cost in the lede.** Per-order math has a place — in "What This Works Out To" (§4.8). In the lede, it reads as advance justification before the reader has seen the rationale.

If Postgres data is unavailable, the lede falls back to `composite_narrative` from the v6.2 CSV and the fallback is noted in the internal routing block. The lede does not invent stats.

```
Follows: "1,071 sessions logged in the last 90 days. 2,501 orders submitted through eCat in the past 12 months, serving 483 active buying accounts."
Violates: "17 of your 66 users logged in last quarter, and across the platform you processed $13M in order volume."
```

### §4.3 — Above-the-midpoint user-count clause

When the brief uses "above the midpoint" in the "How This Compares" section, the sentence MUST include a clause connecting the position to user count — not to a tier premium or arbitrary upcharge. The platform base itself is at the tier standard; the position above midpoint is driven by the account's team size.

Threshold for which position label to use (computed against the tier midpoint — peer dollar values are INTERNAL-ONLY per §4.11):
- `NEW_MRR < midpoint − $75` → "below the midpoint"
- `midpoint − $75 ≤ NEW_MRR ≤ midpoint + $75` → "near the midpoint"
- `NEW_MRR > midpoint + $75` → "above the midpoint" — clause required

The required clause names team size explicitly and confirms the platform base is at standard. Without the clause, "above the midpoint" reads as a premium or penalty; the clause is what makes it math-readable.

```
Follows: "Your new pricing of $2,809/month is above the midpoint of what Commerce Enterprise accounts pay after migration, driven by your team size at 22 billable users — the platform base itself is at the Commerce Enterprise standard."
Violates: "Your new pricing of $2,809/month is above the midpoint of what Commerce Enterprise accounts pay after migration." (no clause — reads as an arbitrary premium)
```

### §4.4 — High-delta lede rule (delta > 30%)

When `delta_pct > 30%`, the lede must directly acknowledge the annual dollar impact before moving to the explanation. The reader has already done the annualization mentally; naming it first is disarming, not alarming.

For the CEO Letter, the verbatim sentence to insert after the monthly delta:

> "That's $[DELTA × 12]/year — a real budget line, and you deserve a straight explanation of exactly what changed and why."

For Format B (where the lede is one paragraph rather than the CEO Letter's call-commitment structure), the annual figure appears alongside the monthly change in the same sentence:

> "…a change of $[DELTA]/month ($[DELTA × 12]/year)…"

Either form satisfies the rule; the choice depends on which template owns the brief. The annual figure is never omitted at delta > 30%.

```
Follows: "Your monthly invoice is moving from $745 to $1,197, effective July 19, 2026. That's $5,424/year — a real budget line, and you deserve a straight explanation of exactly what changed and why."
Violates: "Your monthly invoice is moving from $745 to $1,197 — a 60.7% increase. We'll explain below." (no annual figure; leads with the percentage)
```

### §4.5 — "Only thing changing" line + IUR fork

Every brief includes a single closing-summary sentence that confirms operations are unchanged. The sentence has two variants, dispatched on whether `included_user_reduction` is the primary or any secondary driver.

**Default form** (IUR not present as primary or secondary):

> "Your workflow, your team's access, your catalog, and your integrations are unchanged. The only thing changing is the invoice."

**IUR variant** (IUR primary or secondary):

> "Your workflow, your team's access, your catalog, and your integrations are unchanged. The included user base and the invoice are both changing — the breakdown above explains exactly how."

The IUR variant is required because the unmodified default reads as inaccurate when the included user base is also moving — and a CFO reader will catch that immediately. The variant acknowledges the second moving part and points back to the explanation table above. (Verbatim sentences — copy character-for-character. Do not paraphrase.)

```
Follows (IUR account): "Your workflow, your team's access, your catalog, and your integrations are unchanged. The included user base and the invoice are both changing — the breakdown above explains exactly how."
Violates (IUR account): "Your workflow, your team's access, your catalog, and your integrations are unchanged. The only thing changing is the invoice." (false — the included user base is also changing)
```

**Good News variant** (operator-stamped 2026-05-26 — Good News notices only; IUR fork does not apply because decrease-side Good News scope does not produce `included_user_reduction` primary or secondary drivers):

> "Your workflow, your team's access, your catalog, and your integrations are unchanged. The only thing changing is the invoice."

Copy character-for-character. Do not paraphrase. Good News templates reference this variant via `[INSERT _root/04 §4.5 Good News variant — verbatim]`; increase-side formats continue to use the default or IUR-fork variants above.

### §4.6 — Platform-base-grown sentence

For any account where `new_tier_base > current_platform_mrr` — regardless of which driver is primary — the "Why the Number Is Changing" block includes the following verbatim sentence:

> "The platform has grown considerably since [YEAR] — more surfaces, more capability, the infrastructure behind it. The rate now reflects what the platform is today."

This sentence is the answer to "what am I paying more for?" It applies to `user_rate_normalization`, `at_book_tier_shift`, `discount_correction`, `tier_base_increase`, and any other driver where the base line increases. Do not leave a base increase unexplained under any driver.

**The sentence is verbatim. Do not paraphrase, do not synthesize, copy character-for-character.** The `[YEAR]` token is the account's cohort year (signing year).

```
Follows: "The platform has grown considerably since 2019 — more surfaces, more capability, the infrastructure behind it. The rate now reflects what the platform is today."
Violates: "The platform has matured significantly over the years, and the new rate captures that maturity." (paraphrase; reads as marketing copy where the verbatim reads as plain accounting)
```

### §4.7 — Tenure acknowledgment for early-adopter cohorts

For any account with cohort year ≤ 2015 (signed before 2016), the brief includes an explicit, named-year tenure paragraph in or immediately after the lede. The paragraph names the year, names the number of years, and frames the platform-then versus platform-now distinction with the "fundamentally different product" framing.

For Format B (CS-led) the paragraph is shorter and structural:

> "A change of this size warrants a real explanation. The platform you're running today is a fundamentally different product than it was in [YEAR]: your reps, your buyers, and your analytics team are all working from the same catalog, the same customer file, and the same order infrastructure. That's worth naming when this relationship is moving to a new price."

For the CEO Letter (peer-to-peer) the paragraph is longer, first-person, and ends with the call commitment:

> "You've been with us since [YEAR] — [N] years. A change of this size from us warrants a real conversation, not a form letter. The platform you're running today is a fundamentally different product than it was in [YEAR]: your reps, your buyers, and your analytics team are all working from the same catalog, the same customer file, and the same order infrastructure. The pricing should reflect that. I'll call you personally by [SPECIFIC DATE] so we can talk through this directly."

Required content in both: named years, "fundamentally different product" framing, peer-to-peer tone. Do not substitute generic gratitude language.

```
Follows: "You've been with us since 2013 — 13 years. A change of $452/month warrants a direct conversation, and I'm writing because I want you to hear the explanation from me before it arrives."
Violates: "Thank you for your 13 years of partnership. We appreciate your business and want to walk you through this change." (generic gratitude; no named-year framing; loses the peer-to-peer register)
```

### §4.8 — Value anchor: per-order cost + delta-per-order reframe

The "What This Works Out To" section uses two formulas:

1. **Per-order cost**: `new_mrr × 12 / ltm_orders`
2. **Delta per order**: `delta_mrr × 12 / ltm_orders`

The section is expressed as:

> "Across [ltm_orders] eCat orders last year, the new annual subscription works out to approximately $[COST_PER_ORDER] per order. That's the cost of the full platform per transaction — catalog, ordering, buyer access, and intelligence infrastructure included."

If `delta_per_order < $50`, append a second sentence:

> "The annual rate increase works out to approximately $[DELTA_PER_ORDER] per order."

If `delta_per_order ≥ $50`, omit the second sentence entirely — the figure would work against the message.

**Inclusion gates** (the section is included only if all are true):
- `ltm_orders > 0` (Postgres data confirmed)
- `cost_per_order < $200`
- The per-order figure does not work against the message in context (operator judgment for borderline cases — log the omission)

If `ltm_orders = 0` or `cost_per_order ≥ $200`, omit the entire section.

```
Follows (delta-per-order < $50): "Across 3,472 eCat orders last year, the new annual subscription works out to approximately $7.93 per order. That's the cost of the full platform per transaction — catalog, ordering, buyer access, and intelligence infrastructure included. The annual rate increase works out to approximately $1.37 per order."
Violates (delta-per-order = $54.63): including the second sentence at $54.63 would amplify rather than disarm — the rule says omit it. (Documented mlc case in `_current-state.md` §Decisions Made.)
```

### §4.9 — Billing basis footnote

Immediately after the pricing table inside the `user_rate_normalization` block AND inside the `included_user_reduction` block (before the next `---` separator), the brief includes the following italicized footnote, verbatim:

> *"User billing is based on enabled accounts in your SuperCat environment — the user figures above reflect your current enabled count."*

The footnote is required because both URN and IUR briefs name user counts in the table, and the CFO reader will ask which user count is being billed. The footnote answers the question once, in line, without expanding into a separate definition section.

The footnote does NOT appear after tables for `tier_base_increase`, `discount_correction`, `at_book_tier_shift`, `multi_org_retirement`, `annual_discount_retirement`, or `special_arrangement` blocks — those blocks do not turn on enabled-account billing as a primary lever.

```
Follows: After the URN table, on its own line in italics: "User billing is based on enabled accounts in your SuperCat environment — the user figures above reflect your current enabled count."
Violates: The URN pricing table is followed immediately by a `---` separator with no footnote. (CHECK 2 / CHECK 3 fail.)
```

**Drafter-facing operational note (operator-stamped 2026-05-26, Stage 4.1 `lpf` production proof finding)**: the verbatim customer-facing footnote above stays unchanged. Internally, After-row user figures reflect v6.2 modeled-canonical values (per `_root/05 §2.1.5` + `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix B). When `_root/07 §4.5` reconciliation flag fires (35% of pending cohort per 2026-05-26 sweep), the gap between billing-implied enabled count and v6.2 modeled is resolved via SuperCat-side ops cleanup pre-`[EFFECTIVE_DATE]` (disable phantom enabled accounts in the customer's environment so billing-side enabled aligns with v6.2 modeled by the effective date). The footnote is operationally accurate by `[EFFECTIVE_DATE]` because by that date enabled = v6.2 modeled. NEVER edit the footnote to hedge the reconciliation (e.g. "if your enabled count changes…"); the ops cleanup discipline IS the hedge, executed internally. Per-account ops cleanup tasks tracked at `_meta/v6_2_reconciliation_log.md`.

### §4.10 — Platform-base conditional inside the URN block

When the primary driver is `user_rate_normalization` AND `Before platform base ≠ After platform base`, the URN block must include a sentence explaining the platform-base change. Without it, the brief presents a per-user-rate change while silently also moving the base — the reader will catch the discrepancy in the table and lose trust.

Two acceptable forms, depending on context:

For Format B (where the change is straightforward base-to-current-standard):

> "Your platform base is also moving from $[LEGACY_BASE] to $[NEW_BASE] — this is the current [TIER] standard."

For the CEO Letter (where the change involves a structural reframing, e.g. module → bundled tier):

> "Your platform base is also standardizing from $[LEGACY_BASE] to the current [TIER] rate of $[NEW_BASE] — this reflects the move from legacy module pricing to the current bundled tier structure."

If neither matches the account's actual situation, the platform-base-grown sentence (§4.6) may stand in — but a sentence is required, never silence.

```
Follows: "Your platform base is also moving from $1,740 to $2,295 — this is the current Commerce Enterprise standard."
Violates: The URN block jumps from "We're standardizing all accounts to the same graduated structure" directly to the user-rate table, leaving the +$555 platform base move on the table unaddressed in prose. (CHECK 1 fail.)
```

### §4.11 — "How This Compares" structure

The "How This Compares" section is two sentences:

1. A position sentence (where the account sits relative to the tier midpoint, in plain English — never percentiles).
2. A why-the-comparison-is-fair sentence (the same structure applies to every account).

The position vocabulary is fixed: **"at the base rate"** (account lands at the tier floor with no excess user charge); **"below the midpoint"** (between floor and midpoint); **"near the midpoint"** (within ±$75); **"above the midpoint"** (with the §4.3 user-count clause appended).

Peer-range dollar values (e.g. "Commerce Professional ranges from $1,295–$1,589/month") are **INTERNAL-ONLY** across every format — they appear in the internal routing block and in `internal_ceo_cs_prep_sheet.md`, but they are stripped from the client-facing version for Format A, Format B, the CEO Letter, and Good News alike. (Operator decision 2026-05-22 — see §3 row on peer-range dollar values.)

A canonical client-facing form (no peer dollar range, used across all formats):

> "At $[NEW_MRR], your rate is the [TIER] standard for your account profile. This is the same structure going to every account we work with."

The Format A template currently still includes peer dollar ranges in client copy and requires Stage 3 cleanup to bring it into alignment.

```
Follows: "At $2,295, your rate is the current platform standard for your account profile. This is the same structure going to every account we work with."
Violates: "Your new rate of $1,395/month sits at the 65th percentile of Commerce Professional accounts. There are no account-specific adjustments in how your number was calculated." (percentile notation; forbidden defensive sentence)
```

### §4.12 — Close variants by format

Each format closes with a verbatim block. Do not invent new close language; the four below are the canonical set. Each is followed by the formal-notice line.

**Format A close — "What Happens Next" (CS-led, passive offer):**

> "Your Customer Success contact will be in touch directly before [EFFECTIVE_DATE]. If you'd like to talk through the rate or anything about this before then — that conversation is welcome. Reach out now. There's no process here — just a direct conversation with someone who knows your account."

**Format B close — "Let's Talk" (CS-led, meeting offer):**

> "I'll reach out in the next few days to walk through this together. If you want to get ahead of that — or if you have questions before then — reply directly and we'll find time."

**CEO Letter close — "I'll Call You" (CEO-led, specific date commitment):**

> "I'll call you personally by **[SPECIFIC DATE]** — this isn't something I want to leave to email. If that timing doesn't work or you'd rather get ahead of it, reply to this email directly."

The CEO call-commitment date is specific (an actual calendar date within 5 business days of send), not "soon" or "in the coming days." The date appears in the CEO Letter close and is also logged in the internal routing block.

**Good News close (operator-led, no ask):**

> "Questions about what's changing or how the new rate was calculated — reach out directly."

Good News notices do not include a meeting offer, a call commitment, or a follow-up trigger. The mechanic explains itself; the close confirms there is nothing the reader needs to do.

**Formal-notice line** (immediately after each close, except Good News):

> "*This document also serves as formal written notice of a pricing modification under your SuperCat licensing agreement, effective [EFFECTIVE_DATE].*"

```
Follows (CEO Letter): "I'll call you personally by May 28, 2026 — this isn't something I want to leave to email. If that timing doesn't work or you'd rather get ahead of it, reply to this email directly."
Violates (CEO Letter): "I'll be in touch sometime over the next few weeks to discuss." (no specific date; no first-person commitment; reads as a delegate-able promise)
```

### §4.13 — Health-band lede overrides

The relationship-stats lede (§4.1) and the "What You've Built" section are SUPPRESSED for accounts whose health band is Watch, At Risk, or Critical — OR whose Value Delivery score is below 40. For these accounts, the brief begins with the standalone price-change sentence:

> "Effective **[EFFECTIVE_DATE]**, your monthly invoice moves from **$[CURRENT_MRR]** to **$[NEW_MRR]** — a change of **$[DELTA]/month ([DELTA_PCT])**."

Rationale: a Watch / At Risk / Critical account by definition has a strained relationship; leading with platform-activity stats reads as either tone-deaf (the stats are weak, and the brief will be pointing that out) or sarcastic (the stats are stronger than the relationship, and the writer is making a thinly-veiled point). The dollar-first opening is more respectful of the actual state of the account.

Health-band names themselves never appear in client copy (non-negotiable §2.5). The override is a structural rule for the writer, not a label that surfaces to the reader.

For the CEO Letter specifically, Watch / At Risk accounts also receive the call commitment immediately after the dollar change — no transition through activity stats:

> "Effective [EFFECTIVE_DATE], your monthly invoice moves from $[CURRENT_MRR] to $[NEW_MRR] — a change of $[DELTA]/month. I'll call you personally by [SPECIFIC DATE] to walk through this directly."

```
Follows (Watch-band account): "Effective July 19, 2026, your monthly invoice moves from $2,100 to $2,395 — a change of $295/month (+14.0%)."
Violates (Watch-band account): "Five years on SuperCat, and your team is running the full platform — though we've seen rep engagement decline over the past two quarters. Your monthly invoice is moving from $2,100 to $2,395…" (surfaces a health concern in client copy; lectures the reader)
```

### §4.14 — Discount-correction posture

For accounts whose primary driver is `platform_discount_correction`, the standard "rate at signing" sentence in the lede framing block is replaced by the following verbatim sentence:

> "Your rate reflects a discount applied at signing that's being retired as part of this change."

This substitution applies in Format A, Format B, and the CEO Letter — in each case it replaces the tenure-aware variant of the "rate was set" sentence (see §4.1). The substitution is verbatim across templates.

The `platform_discount_correction` driver block in "Why the Number Is Changing" also uses the structural framing "legacy account-level discounts are being retired across all accounts" rather than the URN-style "rate locked at signing" framing. The driver's content itself is owned by `_root/05`; this rule is only about the lede-sentence substitution.

```
Follows: "Your rate reflects a discount applied at signing that's being retired as part of this change."
Violates: "Your rate was set in 2018 — this is the first time we've updated it." (uses the default URN-tenure framing for a discount_correction account; misrepresents the structural reason)
```

### §4.15 — Parent-letter voice register (entity-packet program) (operator-stamped 2026-05-26)

**Section map** (navigation aid for future operators):

- §4.15.1 — Voice fork by `delivery_owner` (CEO-delivered vs Kylor-delivered)
- §4.15.2 — Multi-brand portfolio acknowledgment (opening framing)
- §4.15.3 — Cross-brand consolidation lens (program framing block)
- §4.15.4 — Per-brand mechanics restraint (parent-letter exclusions)
- §4.15.5 — Default-pricing posture (default_only — operator-stamped 2026-05-26)
- §4.15.6 — Routing pointer to per-child notices (closing transition)

For entity-packet program accounts (per `_root/06 §1.6` — 13 rollup entities + 1 standalone_multi_org per `_master-entity-data-v6.2.csv` Master Entity tab), the parent letter is a multi-brand consolidated framing artifact sent BEFORE per-child notices. Per-child notices follow §4.1–§4.14 for the format each child is routed to (Format A / Format B / CEO Letter / Good News — determined per child by `_root/06`). The voice register differs from per-account briefs in the structural ways defined below.

#### §4.15.1 — Voice fork by `delivery_owner`

The parent letter has two voice variants determined by the `delivery_owner` column in the Master Entity tab:

**CEO-delivered fork** (`delivery_owner = CEO` — 4 entities: Gabriella White / Jonathan Charles / Rock House Farm / Thesis):

- First-person CEO voice (same register as the CEO Letter peer-to-peer paragraph in §4.7 + the §4.12 CEO Letter close).
- CEO-to-CEO peer-to-peer voice posture: recipient is entity's principal/CEO; sender is SuperCat's CEO. Both parties have signing authority for their respective companies; the letter is written as a peer communication between two leaders.
- Closes with a specific call commitment per §4.12 CEO Letter close — calendar date within 5 business days of send, first-person, "I'll call you personally by [DATE]". The 3-location date parity contract operator-stamped 2026-05-26 (Stage 3.3 review pass) applies.
- Signature: SuperCat CEO.

**Kylor-delivered fork** (`delivery_owner = Kylor` — 9 rollup entities + Maxim standalone_multi_org; 10 total. Ferguson Enterprises is Kylor-delivered but EXCLUDED from Stage 3.5 template scope per `_root/06 §1.6` mixed-direction exception):

- First-person Head of Customer Success voice (Kylor Johnson, SuperCat Head of Customer Success — operator-stamped 2026-05-26).
- Direct-relationship CS-leadership voice posture: recipient is entity's principal/CEO; sender is SuperCat's operator-of-record for the account (the person who knows the account best at SuperCat). NOT founder-to-CEO peer voice; NOT generic-CSM register; specifically the HoCS direct-relationship register that mirrors §4.7 tenure acknowledgment depth without the §4.12 CEO Letter close.
- Closes WITHOUT a specific calendar-date commitment (CEO Letter close is CEO-specific per §4.12). Closes with self-continuity to per-child notices (the same person who sent the parent letter will send the per-child notices): see §4.15.6 Kylor-delivered close.
- Signature: Kylor Johnson, Head of Customer Success.

**Cross-format CSM-role note (operator-stamped 2026-05-26)**: SuperCat's CSM support role does NOT handle migration conversations. Across all 5 Stage 3 templates (Format A + Format B + CEO Letter + Good News + entity-packet parent letter), the "CSM-sent" role-marker per `_root/06 §1` is filled by Kylor (HoCS) in practice. CEO-sent templates (CEO Letter + CEO-delivered entity-packet parent letter) are filled by SuperCat's CEO. The role-marker terminology in `_root/06 §1` + `_root/02 §2` remains canonical (CSM / CEO routing rules unchanged); the role-to-person mapping for the migration program is documented here.

In both forks: aligns with §1 voice posture ("peer-to-peer or vendor-to-principal — never service-rep-to-buyer and never marketing-to-prospect"). Both forks are first-person, named, direct relationship, with personal commitment in the close.

#### §4.15.2 — Multi-brand portfolio acknowledgment (opening framing)

The parent letter opens with a portfolio-level acknowledgment naming every member brand by name. The opening framing IS the multi-brand recognition. Required content:

- Every member brand named (use `member_accounts` column from Master Entity tab — pipe-separated; render as natural-language list in customer copy).
- Total entity impact stated as a single dollar number: `Across [N] brands under [ENTITY_NAME], your monthly pricing is changing by $[DEFAULT_DELTA]/month — effective [EFFECTIVE_DATE].`
- Relationship-historicity construction (not transactional): the opening acknowledges the multi-brand relationship's tenure ("We've worked with the [ENTITY_NAME] portfolio since [YEAR]" or similar — use `cohort_year` from the earliest member brand).

The opening does NOT: lead with the dollar number (per §4.2 lede stat guardrail — same rule applies at entity level); disaggregate per-brand impact in the opening (per-brand impact lives in §4.15.3); use vendor-to-customer formality ("We are pleased to inform you that...", "It is with great care that we share...").

#### §4.15.3 — Cross-brand consolidation lens (program framing block)

After the opening, the parent letter delivers the cross-brand consolidation lens — naming WHY a multi-brand entity needs a single coordinated communication. Required content:

- Structural reason for coordinated communication: "[ENTITY_NAME] operates as a portfolio of [N] brands under one parent. Rather than sending [N] independent notices that might miss the cross-brand picture, we've consolidated the portfolio-level framing here. Each brand's specific pricing follows in a separate note."
- Deal-type heterogeneity acknowledgment IF `has_annual = TRUE` OR `mixed_segment` is populated: name the heterogeneity explicitly ("[ENTITY_NAME] includes [X] monthly-billed brands + [Y] annual-billed brands; the per-brand notices reflect each brand's billing rhythm").
- Tier heterogeneity acknowledgment IF `mixed_tiers = YES`: "[ENTITY_NAME]'s brands span [tier list — e.g. 'Catalog Essentials (T1) and Commerce Enterprise (T3)']; each brand's tier mapping reflects its scale and use pattern".
- Per-brand narrative threading: parent letter REFERENCES per-brand narratives via the `entity_messaging_headline` column (Master Entity tab) — formats as a compact list (one sentence per brand naming the brand + the headline snippet). Does NOT reproduce per-child driver mechanics here (that's §4.15.4 exclusion territory).

#### §4.15.4 — Per-brand mechanics restraint

The parent letter explicitly EXCLUDES:

- Per-brand driver mechanics (no `_root/05` driver detail blocks; driver narrative lives in per-child notices).
- Per-brand "Why the Number Is Changing" prose (per-child territory).
- Per-brand tier feature lists (per-child territory).
- Per-brand pricing tables (parent letter carries only entity-level delta; per-child notices carry the "Your Pricing at a Glance" table).
- Per-brand value-anchor sections (per-order cost reframes, etc. — per-child territory).
- Per-brand call commitments (parent letter has ONE call commitment — the entity-level commitment per §4.15.1; per-brand call commitments dilute it).

Drift here breaks the parent/child architecture: when a per-brand mechanic appears in the parent letter, the recipient stops reading the per-child notice for that brand because "I already saw this in the parent letter."

```
Follows: parent letter states "[ENTITY_NAME]'s pricing is changing by $X/month across [N] brands; each brand's specifics follow in a separate note."
Violates: parent letter inlines "[BRAND_A]'s pricing is changing by $X due to user_rate_normalization; [BRAND_B]'s pricing is changing by $Y due to multi_org_retirement..." (per-brand mechanics in the parent letter — drift)
```

#### §4.15.5 — Default-pricing posture (default_only — operator-stamped 2026-05-26)

Parent letter presents only the DEFAULT pricing scenario (`default_mrr`, `default_delta`, `default_delta_pct` from the Master Entity tab). The consolidated-savings scenario (`consolidated_delta`, `consolidation_saving`, `consolidation_saving_pct`) is INTERNAL-ONLY:

- Parent letter does NOT present a "consolidation savings opt-in" CTA.
- Parent letter does NOT mention the consolidated-savings opportunity (no pointer sentence; no soft mention).
- Consolidation savings live in the CSM/CEO post-send prep sheet; surfaced ONLY in post-send conversation if the entity raises it OR if the conversation warrants it.

Rationale (operator-stamped 2026-05-26): migration delivery is firm/declarative; consolidation sales motion is consultative/opt-in; mixing dilutes both. Per §1, the parent letter delivers a number the recipient has the standing to question, not a pitch they're expected to evaluate. Consolidation savings are 1.6–6.2% of entity MRR across the 13 rollup entities ($75–$687/mo range); the value of separating the two motions exceeds the value of bundling them.

**Terminology constraint**: when `migration_driver = multi_org_retirement` (legacy multi-org discount being retired across a child brand), the parent letter MAY name the discount retirement in per-brand threading (§4.15.3) — that "consolidation" is the migration mechanic (an old discount retiring across one entity), NOT the new consolidation-savings opportunity (a new multi-brand discount opt-in). Use precise language ("the [legacy multi-org] discount is retiring" — past-tense, structural) vs. (no mention of new consolidation savings — internal-only).

```
Follows: parent letter names the entity-level default delta; consolidation savings not mentioned in customer copy; post-send CSM/CEO conversation surfaces if relevant.
Violates: parent letter says "Your default monthly impact is $X; if you'd like to consolidate billing across brands, we can offer $Y in savings" (mixes migration delivery with sales CTA — dilutes both).
```

#### §4.15.6 — Routing pointer to per-child notices (closing transition)

Parent letter closes (before signature) with a transition pointing to where per-brand specifics live and approximately when each brand's notice arrives:

**CEO-delivered close** (per §4.15.1 CEO-delivered fork):

> I'll call you personally by [SPECIFIC_DATE] to walk through the portfolio together — this isn't something I want to leave to email. Each brand's specific pricing will follow in a separate note within 48 hours of this letter; please read those alongside our conversation.

**Kylor-delivered close** (per §4.15.1 Kylor-delivered fork):

> Each brand's specific pricing will follow in a separate note from me within 48 hours of this letter. If you'd rather we walk through the portfolio together first, reply directly to this email and we'll set time before the per-brand notices arrive.

The routing pointer is required in both forks: the parent letter MUST tell the recipient that per-brand notices are coming and approximately when. This prevents per-brand notices from feeling like "another shoe dropping" — the parent letter is the umbrella; the per-brand notices are the implementation under that umbrella.

The 48-hour timing is operator-stamped 2026-05-26 as the canonical Stage 3.5 sequencing (parent letter sends first; per-brand notices follow within 2 business days). Revising the 48-hour window requires the rule-change protocol per `_root/CONTRACTS.md §3`.

### §4.16 — Annual-cohort voice rules (operator-stamped 2026-05-26)

Annual-cohort accounts receive notice referencing the **renewal date** as the effective date, not a flat migration effective date. The data trigger is `deal_type = 'Annual'` at the account level (per `_root/07 §2`) or `has_annual = TRUE` at the entity level (per the dual-canonical v6.2 architecture; entity-level signal applies to entity-packet parent letters covering Annual member-brands). The timing companion — the ≥90-day notice window and `notice_cohort = 'Renewal-Based'` batching — lives at `_root/06 §4.3`; the scope (which accounts qualify) lives at `_root/02 §5`. This sub-section owns only the voice consequence: how the lede sentence, formal-notice line, and per-format close render when the effective date is a renewal date rather than a flat cohort effective date.

This sub-section closes `CL-015` (Annual overlay voice rules need a home in `_root/04`) at the rule layer.

#### §4.16.1 — Scope

This voice rule fires for any account or entity flagged Annual in v6.2 — `deal_type = 'Annual'` at the account level (canonical signal per `_root/07 §2`) or `has_annual = TRUE` at the entity level (canonical signal per the v6.2 Master Entity tab). Account-level enumeration lives at `_root/02 §5` (11 pending Annual accounts among the 107-account program; cohort total Δ +$2,321/mo; all carrying `migration_segment = 'Annual'` and `notice_cohort = 'Renewal-Based'`).

The voice rule applies across all four increase-side formats (Format A, Format B, CEO Letter, Good News) AND the entity-packet parent letter when any member-brand is Annual.

The timing consequence of the Annual overlay — the ≥90-day notice window (60-day legal minimum + 30-day buffer) and the Renewal-Based cohort batching — is owned by `_root/06 §4.3`. The voice consequence — renewal-date framing in the lede and formal-notice line — is owned by this §4.16. `_root/02 §5` and `_root/06 §4.3` are timing companions to this voice rule; they are not duplicated here.

#### §4.16.2 — Lede effective-date shift

Non-negotiable §2.1 ("Lead with the dollar amount and effective date — never lead with a percentage") applies as-is for Annual accounts. The Annual variant supplements §2.1 by specifying that the effective date in the lede is the renewal date, not a flat migration effective date.

The lede sentence pattern (per-format adaptation of the tenure-aware variants in §4.1 and the lede stat guardrail in §4.2):

> Your monthly pricing is changing from $[CURRENT_MRR] to $[NEW_MRR] effective at your renewal on [RENEWAL_DATE].

Format-specific renderings adapt this pattern through the existing per-format lede rules at §4.1 (tenure-aware relationship lede), §4.2 (lede stat guardrail), §4.4 (high-delta annual-dollar-impact lede above 30%), and §4.13 (health-band overrides). For Good News Annual accounts, the lede follows the Good News decrease pattern (one-sentence dollar-first) with `[EFFECTIVE_DATE]` resolving to `[RENEWAL_DATE]`. Per-format lede patterns are not restated here — they live at §4.1 / §4.2 / §4.4 / §4.13 and propagate to Annual accounts via the `[EFFECTIVE_DATE]` = `[RENEWAL_DATE]` token resolution.

Drafter pulls `[RENEWAL_DATE]` from v6.2. If the v6.2 account-level table does not carry a `renewal_date` column at draft time, fallback follows `_root/07 §5` — the routing CSV's `nuances` column may carry per-account renewal-date annotations for the 11 Annual pending accounts; otherwise the drafter surfaces to operator per §4.16.4 before drafting.

The operations-unchanged sentence (§4.5) and the consolidated 2026 framing sentence (§3 universal row; Good News exception at §3.1) apply as-is for Annual accounts. Only the per-account effective-date sentence shifts to renewal-date framing — the "moving every account to one clear pricing structure" framing is timing-independent.

#### §4.16.3 — Close + formal-notice line

The format-specific close text (§4.12) applies as-is for Annual accounts; the close commitment per format (passive Format A / active Format B / specific-date CEO Letter / Good News no-ask) does not shift on the Annual overlay. The Annual voice rule changes the lede effective date; it does not change the close.

The formal-notice line per §4.12 ("This serves as a pricing modification under your SuperCat licensing agreement effective [EFFECTIVE_DATE]") resolves `[EFFECTIVE_DATE]` to `[RENEWAL_DATE]` for Annual accounts. The formal-notice-line text itself is not modified — only the date token resolution shifts.

The CEO Letter 3-location date parity contract (operator-stamped at Stage 3.3 review pass 2026-05-26 via template-level QB-086 + cross-check) applies as-is for Annual CEO Letter accounts. The specific calendar date in the close commitment + brief routing-block + delivery-email routing-block may be (a) the call commitment date, (b) the renewal date itself, or (c) both — the drafter surfaces both options at draft time and operator stamps per-account.

For Good News Annual accounts, §4.12's "no formal-notice line, except Good News" rule continues to apply — Good News does not carry a formal-notice line. The Annual variant changes only the lede effective date for Good News Annual accounts.

#### §4.16.4 — Drafter judgment + surfacing

The Annual voice rule presumes a clean `[RENEWAL_DATE]` resolution at draft time. Three surfacing requirements:

1. **Missing or ambiguous renewal date.** If `renewal_date` is absent from the v6.2 account-level CSV, absent from the routing CSV `nuances` column, OR carries an ambiguous value (e.g. only month/year without a specific day), the drafter surfaces to operator before drafting. Do NOT default to a migration effective date — the drafter pauses and asks. The renewal-date audit conducted during the readiness sprint per `_root/02 §5` is the authoritative source if v6.2 has not yet absorbed the audit's results.

2. **Cohort mismatch.** If `deal_type = 'Annual'` (or `has_annual = TRUE`) but the routing CSV carries `notice_cohort` other than `'Renewal-Based'` (e.g. an operator-override placing the account in a standard monthly cohort), the drafter surfaces the routing-cohort mismatch to operator. The Annual voice rule fires off the data signal, not the routing cohort — but a cohort mismatch implies an upstream operator decision the drafter should not paper over.

3. **Entity-packet × Annual interaction.** If an entity has both Annual and non-Annual member-brands, the parent letter's deal-type heterogeneity acknowledgment at §4.15.3 fires; the parent letter is sent at parent timing (Day 0 per §4.15.6 48-hour sequencing) and per-child Annual notices follow their renewal-date timing per this §4.16 — which may extend beyond the 48-hour window for Annual children. The parent letter's routing pointer at §4.15.6 carries the per-brand timing variance. Drafter flags to operator at per-brief draft time whenever an entity packet routes an Annual child outside the standard 48-hour window.

*Cross-references: `_root/06 §4.3` (Annual overlay timing — 90-day notice window + Renewal-Based cohort); `_root/02 §5` (Annual overlay scope — which accounts are Annual; renewal-date audit); `_root/07 §2` (`deal_type` account-level + `has_annual` entity-level data fields); `_root/07 §5` (9-row fallback table for missing or ambiguous data); `_root/04 §2.1` (non-negotiable lede pattern — Annual rule supplements rather than amends); `_root/04 §4.1` (tenure-aware lede variants — Annual rule resolves `[EFFECTIVE_DATE]` to `[RENEWAL_DATE]` within these patterns); `_root/04 §4.2` (lede stat guardrail — applies as-is); `_root/04 §4.4` (high-delta annual-dollar-impact lede — applies as-is above 30%); `_root/04 §4.5` (operations-unchanged sentence — applies as-is); `_root/04 §4.13` (health-band overrides — apply as-is); `_root/04 §3` + `§3.1` (consolidated 2026 framing — applies as-is, including Good News exception); `_root/04 §4.12` (format-specific close + formal-notice line — date token resolves to `[RENEWAL_DATE]`); `_root/04 §4.15.3` (entity-packet deal-type heterogeneity acknowledgment for parent letters covering Annual + non-Annual brands).*

---

## Section 5 — Driver-voice orientation

Each migration driver shapes the voice of the brief slightly differently — the voice rules in §4 hold across all drivers, but the framing in the "Why the Number Is Changing" block leads differently depending on which driver is primary. `user_rate_normalization` leads with the per-user rate history (locked at signing, moving to graduated standard). `included_user_reduction` leads with the included-base normalization (often acknowledged as an expanded allotment that was part of the original arrangement — a structural fact, not a favor being revoked). `tier_base_increase` and `at_book_tier_shift` lead with the "platform has grown" framing (§4.6 verbatim sentence). `platform_discount_correction` leads with the discount-retiring framing and uses the §4.14 lede substitution. `multi_org_retirement` and `annual_discount_retirement` lead with the named-program retirement and the structural move to individual standard pricing. `special_arrangement` leads with the relationship-historicity framing — direct, no euphemism, with operator-prepared answer to "what was the arrangement and why is it changing?" `module_compression` is decrease-only and routes to the Good News format. **Do not author per-driver narrative content here** — the actual driver prose is owned by `_root/05_driver_taxonomy.md`. This section names only that the voice shifts per driver, and points forward.

---

## Section 6 — What this doc does NOT own

The following live in other root docs. References should point there, not duplicate the rules here.

- **Per-driver narrative content** (the actual "Why the Number Is Changing" prose for each driver, with conditionals, exact phrasing of the structural framing, dual-driver patterns) → `_root/05_driver_taxonomy.md`
- **Tier feature language** ("Catalog Essentials includes…," "Commerce Enterprise includes…," the "What's Coming in 2026" verbatim block) → `_root/03_what_we_sell.md`
- **Segment / format mapping** (who gets Format A vs. Format B vs. CEO Letter vs. Good News, including the delta-bucket thresholds and the health-band overrides on format selection) → `_root/02_who_is_being_migrated.md` + `_root/06_format_routing.md`
- **Data field meanings** (what `migration_driver` is, what `secondary_drivers` is, what `value_delivery_score` is, how `trailing_avg_users` is computed, source-of-truth hierarchy for any field used in a brief) → `_root/07_data_pipeline.md`
- **The quality checklist** (the verification procedure run before send, the per-file pre-send gates) → `_root/08_quality_bar.md`. **The conformance-block format** → `_root/00_manifest.md §5` (migrated from `_root/08` to the manifest at Stage 5, 2026-05-22). `_root/08` imports the rules from this doc by reference; it does not restate them.

---

*Cross-references: `_root/00_manifest.md` (required-reading map); `_root/CONTRACTS.md` §5 (path-reference contract, which this doc's structure enforces); `_root/09_changelog.md` (log entries for every edit to this doc).*
