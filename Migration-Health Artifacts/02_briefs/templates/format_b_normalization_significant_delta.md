# Format B: Price Normalization Brief — Significant Delta Accounts (>10% delta)
*Template | SuperCat Migration-Health Artifacts*

---

**When to use this template:** Accounts where the price change exceeds 10% — typically Wave 2. Two-part structure: a CEO letter (the deliverable the client reads) + a math appendix (for finance review). The letter is short, plain, and relational. The appendix is complete and auditable.

**Who sends it:** CEO — personally signed and, ideally, personally delivered. For the highest-delta accounts (>25%), the CEO should call before this lands in writing. This is not a template to send cold via email without a relationship primer.

**Do not conflate with expansion.** If this account also has an upgrade opportunity, that conversation happens separately — after the migration is acknowledged.

---

> **Internal routing note** (remove before sending):
> Brief type: `value_justification` | Format B (>10% delta)
> Account: [ACCOUNT_NAME] | Tier: [TIER] | Wave: [WAVE]
> Migration driver: [DRIVER] | Health: [SCORE] — [BAND] | Risk label: [RISK]
> Engagement: [E_SCORE] | Adoption: [A_SCORE] | Value Delivery: [VD_SCORE] | Ops Health: [OH_SCORE]
> Support fire: [YES/NO — if YES, resolve open issues before outreach] | Behavioral floor applied: [YES/NO]
> Delta: +[DELTA_PCT] (+$[DELTA]/month)
> Cohort: [YEAR] — [NOTE IF EARLY ADOPTER, e.g., "2013 cohort — tenure objection likely"]
> Contract structure: [MONTHLY / ANNUAL] | Initial term ended: [YES / NO / UNKNOWN] | Renewal date: [DATE or "unknown"]
> Earliest enforceable effective date: [60 days from delivery for monthly / 90 days before renewal for annual — flag UNKNOWN if contract status not confirmed]
> Expansion eligible: [YES/NO — if yes, queue only after confirmed positive migration signal]
> Cohort playbook: [zero_friction / value_led / careful / high_touch] — value_led = Thriving/Healthy + large delta; careful = Watch band; high_touch = At Risk/Critical
> **See internal prep sheet for objection handling and negotiation boundaries**

---

# [ACCOUNT_NAME]: Your Pricing Is Changing

*[DATE]*

---

**[LEDE BLOCK — Thriving and Healthy accounts only. If health_band is Watch, At Risk, or Critical: delete this block entirely and begin with the standalone price change sentence below. See operator prompt Step 3a for population instructions.]**

[LEDE_PARAGRAPH — 2–3 sentences. Weave the account's platform stats into the opening before landing the price change. Stats go inline — no separate section heading (this is a CEO letter, not a data document). Structure: "[ACCOUNT_NAME] has been on SuperCat since [YEAR] — [N] years. In that time [they've / you've] built [brief platform picture: active rep count, login volume or standout usage stat, feature adoption highlights — 1–2 stats max]. Your monthly subscription is moving from **$[CURRENT_MRR]** to **$[NEW_MRR]** — an increase of **$[DELTA]/month ([DELTA_PCT])** — and this letter explains exactly why." Do not use health score language, band names, or the word "health."]

**[END LEDE BLOCK — for Watch/At Risk/Critical accounts, begin here:]**

**[IF LEDE BLOCK was skipped — include this standalone price change sentence:]**
Effective **[EFFECTIVE_DATE]**, [ACCOUNT_NAME]'s monthly subscription moves from **$[CURRENT_MRR]** to **$[NEW_MRR]** — an increase of **$[DELTA]/month ([DELTA_PCT])**.

**[FOR EARLY ADOPTER COHORTS (signed before 2016) — include this paragraph; otherwise delete:]**
You've been with us since [YEAR], and I want to address this directly because you deserve that. A change of this size warrants a real explanation, not a form letter.

**[FOR ALL ACCOUNTS:]**
SuperCat is standardizing its pricing across the full install base for the first time. For years, pricing was set account by account at signing — which meant accounts that joined at different times ended up on materially different rates for the same platform. That's not fair to anyone, and 2026 is the year we fix it. **[ADD IF customer joined pre-2018:]** The platform is also a fundamentally different product than it was in [YEAR]. What you're running today — five connected surfaces sharing one catalog, one customer file, and one order infrastructure across rep, buyer, and analytics workflows — is a commercial operating system. The pricing should reflect that.

The math appendix at the end of this letter shows the full calculation. Here is the plain-language explanation.

---

## Why Your Number Is Changing

**[USE ONLY THE APPLICABLE BLOCK — delete the rest]**

---
**IF single driver — `user_rate_normalization`:**

Your additional-user rate has been **$[LEGACY_USER_RATE]/user** since your account was set up in [YEAR]. That rate was locked in at signing before SuperCat established a consistent rate card. We're standardizing all accounts to the same graduated structure.

The change moves your user pricing from $[LEGACY_RATE]/user flat to a graduated curve: $25/user for the first 10 above the included base, $22 for the next 15, $20 for the next 25, and $18 beyond that.

At the same time, your included user base is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED] — which absorbs [N] of your current additional users and reduces your per-user charges by $[USER_SAVINGS]/month.

The net:

| | Monthly Impact |
|---|---|
| Platform base correction | [+/–]$[BASE_CHANGE] |
| User rate + included base expansion | [+/–]$[USER_NET] |
| **Net change** | **+$[DELTA]/month** |

---
**IF dual driver — `user_rate_normalization` + `platform_base_correction`:**

Two things are changing on your invoice:

**1. Platform base: $[LEGACY_BASE] → $[NEW_BASE]**
Your platform rate reflects your original [YEAR] contract. The [TIER] base rate is $[NEW_BASE]. That's a +$[BASE_CHANGE]/month change on the platform side.

**2. User rate: $[LEGACY_RATE]/user → graduated standard**
Your additional users have been billed at **$[LEGACY_RATE]/user** — a rate from [YEAR]. The new graduated curve is:

| Additional users above included base | Rate |
|---|---|
| 1–10 excess users | $25/user |
| 11–25 excess users | $22/user |
| 26–50 excess users | $20/user |
| 51+ excess users | $18/user |

Your included user base expands from [LEGACY_INCLUDED] to [NEW_INCLUDED] — absorbing [N] users who no longer generate a charge. With [NEW_EXCESS] excess users at the new graduated rate, your user charges [increase/decrease] by $[USER_NET]/month.

**The net:**

| | Monthly Impact |
|---|---|
| Platform base correction | +$[BASE_CHANGE] |
| User rate correction + included user expansion | [+/–]$[USER_NET] |
| **Net change** | **+$[DELTA]/month** |

---
**IF `discount_correction`:**

Your current pricing reflects a [N%] discount applied at signing in [YEAR]. As part of this refresh, legacy account-level discounts are being retired across the install base. All accounts are moving to the same standard tier pricing. Your new monthly rate is the [TIER] standard rate for your account profile.

| | Monthly Impact |
|---|---|
| Discount removal | +$[DISCOUNT_VALUE] |
| User structure update (if applicable) | [+/–]$[USER_NET] |
| **Net change** | **+$[DELTA]/month** |

---
**IF `at_book_tier_shift`:**

When your account was set up in [YEAR], the [TIER] tier was priced at **$[LEGACY_BASE]/month**. The current book rate for [TIER] is **$[NEW_BASE]/month**. Your invoice is moving to the current book rate as part of this standardization — your tier is not changing, only the rate.

| | Monthly Impact |
|---|---|
| Platform base: $[LEGACY_BASE] → $[NEW_BASE] | +$[BASE_CHANGE] |
| User structure update (if applicable) | [+/–]$[USER_NET] |
| **Net change** | **+$[DELTA]/month** |

---
**IF `multi_org_retirement`:**

[ACCOUNT_NAME] has been part of SuperCat's multi-organization pricing program — a structure that applied cross-entity benefits across [PARENT_ORG] and its related accounts. That program is being retired as part of this refresh. Each entity moves to individual standard [TIER] pricing.

Two things are changing:

**1. Program rate → standard tier rate**
Your platform base moves from $[LEGACY_BASE] (multi-org program) to $[NEW_BASE] ([TIER] standard) — a +$[BASE_CHANGE]/month change.

**2. User pricing standardization**
[IF user rate is also changing: Your user rate moves from $[LEGACY_RATE]/user to the graduated standard. Your included base expands from [LEGACY_INCLUDED] to [NEW_INCLUDED], absorbing [N] users. Net user charge change: [+/–$USER_NET]/month.]
[IF user rate is already standard: User pricing is unchanged — your user structure is already aligned with the standard rate card.]

| | Monthly Impact |
|---|---|
| Multi-org program retirement | +$[BASE_CHANGE] |
| User structure update | [+/–]$[USER_NET] |
| **Net change** | **+$[DELTA]/month** |

---
**IF `special_arrangement`:**

Your current pricing reflects a custom arrangement from [YEAR] — a rate set outside SuperCat's standard commercial structure. I want to be direct about that, because a change of this size deserves a clear explanation.

As we bring all accounts onto the same pricing structure in 2026, custom arrangements are moving to standard tier rates. This is not a judgment about your account or the arrangement you had. It's a structural decision: one rate card, applied consistently. The new price is what every account at your tier and user count pays.

| | Monthly Impact |
|---|---|
| Custom arrangement → standard tier rate | +$[BASE_CHANGE] |
| User structure update (if applicable) | [+/–]$[USER_NET] |
| **Net change** | **+$[DELTA]/month** |

> **Operator note:** For `special_arrangement` accounts with delta >30%, always pair with an internal prep sheet. The CEO must be prepared to answer "what was the arrangement and why is it changing?" Confirm the account history with Finance before outreach if the nature of the original arrangement is unclear.

---

## What You're Getting at $[NEW_MRR]/Month

[One paragraph — not a bullet list for the letter portion. Describe what the tier includes and confirm the account is already using it. Use the tier-specific framing below, adapt to the account's actual stack.]

**IF Catalog Essentials (T1):** "Catalog Essentials is SuperCat's entry point — the iPad rep app and buyer-facing catalog running on shared infrastructure. Your reps carry your full catalog offline, write orders in the field, and sync back. The tier covers [N] included users and standard support."

**IF Commerce Professional (T2):** "Commerce Professional is the full rep-facing platform plus the buyer-side commerce stack — B2B Cart gives your buyers self-serve ordering directly against your catalog and pricing, and Order & Invoice Tracking gives them account visibility without involving your team. Your reps and your buyers are both working from the same infrastructure. That's what this tier covers — and it's what you're already running."

**IF Commerce Enterprise (T3):** "Commerce Enterprise is SuperCat's full commercial operating system — five connected surfaces sharing one catalog, one customer file, and one order infrastructure across every channel your sales team and buyers use. Everything in your current stack is included: iPad App, catalog, B2B Cart, Order & Invoice Tracking, and Sales Intelligence. At T3, you also get the Insights Layer — rep performance scorecards, cross-customer benchmarking against similar manufacturers, dormant customer signals, and 42 queryable value moments across 8 domains. Plus 40 included users, a dedicated CSM, priority support, and CPQ/Credit Card with no separate line item. This tier reflects what you're actually running."

---

## How This Compares

Across [T1/T2/T3] accounts after migration, monthly pricing ranges from **$[PEER_P25] to $[PEER_P75]** at the 25th–75th percentile. At $[NEW_MRR], [ACCOUNT_NAME] is [below / at / above] the midpoint — reflecting your [user count / usage profile / legacy rate].

**[FOR T3 ACCOUNTS — add this sentence, delete for T1/T2:]** For external context: equivalent platforms offering comparable full-stack commercial operating scope are priced at $3,000–$3,500/month at comparable user scales.

Every account in the install base is moving to this same structure.

*(T1 p25–p75: $774–$1,629/mo | T2: $1,295–$1,589/mo | T3: $2,295–$2,875/mo)*

---

## What Doesn't Change

Your workflow, your team's access, your catalog, your integrations, and your data — none of that changes. The platform operates identically. The only change is the invoice.

---

## Let's Talk

**[FOR >25% DELTA — mandatory personal close:]**
I know this is a real number, and I want to make sure we address it directly. **I will call you by [SPECIFIC DATE].** If you want to get ahead of that conversation — or if you'd prefer to have this in writing first — reply and we'll find time.

**[FOR 10–25% DELTA — standard close:]**
**[CEO/CSM NAME] will reach out by [SPECIFIC DATE]** to walk through this together. If you have questions before that, reply directly and we'll get on a call.

*This letter also serves as formal written notice of a pricing modification under your SuperCat licensing agreement, effective [EFFECTIVE_DATE].*

---

*[CEO NAME]*
*[TITLE], SuperCat*
*[DATE]*

---
---

# Appendix: Pricing Calculation Detail

*Complete reference — share with finance contacts as needed*

| | Current | After Migration |
|---|---|---|
| **Monthly total** | $[CURRENT_MRR] | **$[NEW_MRR]** |
| **Annual** | $[CURRENT_ARR] | **$[NEW_ARR]** |
| **Change** | — | +$[DELTA]/month ([DELTA_PCT]) |
| | | |
| Platform base | $[LEGACY_BASE] (legacy [YEAR] rate) | $[NEW_BASE] ([TIER]) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Trailing avg billable users | [BILLABLE_USERS] | [BILLABLE_USERS] |
| Users above included base | [LEGACY_EXCESS] at **$[LEGACY_RATE]/user** | **[NEW_EXCESS]** at graduated rate |
| User charge | $[LEGACY_USER_CHARGE] | $[NEW_USER_CHARGE] |
| | | |
| Additional user rate | $[LEGACY_RATE]/user flat ([YEAR] contract) | Graduated ($25/$22/$20/$18) |
| **Tier** | [LEGACY_TIER_LABEL] | [NEW_TIER_LABEL] |

*Peer context: [T1/T2/T3] accounts post-migration range from $[PEER_P25]–$[PEER_P75]/month (p25–p75 of install base).*
