# CEO Letter — Brief Template
*60-Day Notice | >10% delta | CEO-sent (CEO Letter + Call Commitment tier)*

---

> **Internal routing note** (remove before sending):
> Brief type: `CEO Letter` | >10% delta
> Account: [ACCOUNT_NAME] | Tier: [T1/T2/T3] | Wave: [WAVE]
> Migration driver: [DRIVER] | Health: [SCORE] — [BAND]
> Engagement: [E] | Adoption: [A] | Value Delivery: [VD] | Ops Health: [OH]
> Support fire: [YES/NO — IF YES: ⚠️ [N] days open. Confirm send timing with CEO before this goes out.] | Behavioral floor applied: [YES/NO]
> Delta: [DELTA_PCT] (+$[DELTA]/month)
> Cohort: [YEAR] [— NOTE IF EARLY ADOPTER: "20XX cohort — tenure acknowledgment required"]
> Contract: [MONTHLY/ANNUAL] | Renewal date: [DATE or UNKNOWN — confirm before sending]
> Earliest enforceable effective date: July 19, 2026 (61 days from May 19 — confirm for annual contracts)
> Comm_action: CEO Letter + Call Commitment
> **CEO awareness required before send: YES — CEO must review and personalize before this goes out**
> CEO call commitment date: [DATE — specific, within 5 business days of send]
> CEO name for sign-off: [CEO FIRST + LAST NAME]

---

# [ACCOUNT_NAME]: Your Pricing Is Changing

*Prepared for [ACCOUNT_NAME] | [DATE]*

---

[LEDE — 3–4 sentences. CEO is writing directly. Open by acknowledging the relationship or the significance of the news — this is a peer writing to a peer, not a CSM sending a notice. Then land the price change in dollars, not a percentage. Then commit to the call. Structure: "I'm writing to you directly because [relationship acknowledgment / this is a change of this size]. Your monthly invoice is moving from $[CURRENT_MRR] to $[NEW_MRR] — a change of $[DELTA]/month, effective [DATE]. Below is the full explanation of why that number is what it is and what you're getting at the new rate. I'll call you personally by [SPECIFIC DATE] to talk through any of this." For early adopter cohorts (pre-2016), acknowledge tenure explicitly and personally: "You've been with us since [YEAR] — [N] years. A change this size from us to you deserves a direct conversation, not a form letter." For Watch/At Risk health bands, skip activity stats in the lede and lead directly with the dollar change and CEO's direct commitment to the call.

**HIGH-DELTA LEDE RULE (delta >30%):** The lede must directly acknowledge the annual dollar impact before moving to the explanation. Do not soften it. Add a sentence after the monthly delta: "That's $[DELTA × 12]/year — a real budget line, and you deserve a straight explanation of exactly what changed and why." Then proceed to the call commitment. Accounts with delta >30% have already done the math. Naming the annual figure first is disarming, not alarming — it signals the CEO knows the size of the ask.]

SuperCat is standardizing its pricing across all accounts in 2026 — the first time we've applied a consistent structure across the board. Your rate was set at signing and hasn't been updated since. Below is exactly why your number is changing and what you're getting at the new rate.

**[ADD FOR EARLY ADOPTER COHORTS — signed before 2016:]**
You've been with us since [YEAR] — [N] years. A change of this size from us warrants a real conversation, not a form letter. The platform you're running today is a fundamentally different product than it was in [YEAR]: your reps, your buyers, and your analytics team are all working from the same catalog, the same customer file, and the same order infrastructure. The pricing should reflect that. I'll call you personally by [SPECIFIC DATE] so we can talk through this directly.

**[ADD FOR PLATFORM_DISCOUNT_CORRECTION ACCOUNTS — replace the "rate at signing" sentence above:]**
Your rate reflects a discount applied at signing that's being retired as part of this change.

---

## Why the Number Is Changing

**[USE ONLY THE APPLICABLE BLOCK — delete all others]**

---
**DRIVER: `user_rate_normalization`**

Your additional-user rate has been **$[LEGACY_USER_RATE]/user** since your account was set up in [YEAR]. That rate was locked in at signing and hasn't been updated to the current rate card. We're standardizing all accounts to the same graduated structure as part of this refresh.

[IF platform base also changes alongside the user rate (Before platform base ≠ After platform base) — add this sentence:]
Your platform base is also standardizing from $[LEGACY_BASE] to the current [TIER] rate of $[NEW_BASE] — this reflects the move from legacy module pricing to the current bundled tier structure.

The new user pricing follows a graduated curve applied consistently across all accounts:

| Additional users above included base | Rate |
|---|---|
| 1–10 excess users | $25/user |
| 11–25 excess users | $22/user |
| 26–50 excess users | $20/user |
| 51+ excess users | $18/user |

[IF trailing avg users ≤ new included base — user charge goes to $0:]
Your included user base is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]. With [TRAILING_AVG] average users, all of your users are now covered within the included base — your user charge goes to $0/month.

[IF excess users remain AND new included base > legacy included base (base expanding):]
Your included user base is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED] — absorbing [N] users who no longer generate a charge. The remaining [NEW_EXCESS] excess users are billed at the graduated rate: [EXCESS_MATH_BREAKDOWN] = $[NEW_USER_CHARGE]/month.

[IF excess users remain AND secondary driver = included_user_reduction (base shrinking from legacy to current tier standard):]
Your included base is also adjusting from the legacy [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED]. With [TRAILING_AVG] average users, [NEW_EXCESS] are now above the [NEW_INCLUDED]-user included base, billed at the graduated rate: [EXCESS_MATH_BREAKDOWN] = $[NEW_USER_CHARGE]/month.

Here's how that plays out on your invoice:

| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] | $[NEW_BASE] ([TIER]) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS] users at $[LEGACY_RATE] = **$[LEGACY_USER_CHARGE]/month** | [NEW_EXCESS] users at graduated rate = **$[NEW_USER_CHARGE]/month** |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

*User billing is based on enabled accounts in your SuperCat environment — the user figures above reflect your current enabled count.*

---
**DRIVER: `tier_base_increase`**

When your account was set up in [YEAR], the [TIER] platform was priced at **$[LEGACY_BASE]/month** — the book rate at that time. The current standard rate for this tier is **$[NEW_BASE]/month**. Your invoice is moving to the current standard — your tier isn't changing, only the rate.

[IF secondary driver = user_rate_normalization AND included base expands — add this paragraph:]
Additionally, the included user base for this tier is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED].

[IF trailing avg users ≤ new included base — user charge goes to $0:]
With your team averaging [TRAILING_AVG] users, everyone is now within the included base — your current user charge of $[LEGACY_USER_CHARGE]/month goes to $0.

[IF excess users remain after new included base:]
The remaining [NEW_EXCESS] users above the new included base are billed at the graduated rate: [EXCESS_MATH_BREAKDOWN] = $[NEW_USER_CHARGE]/month.

Here's how that plays out on your invoice:

| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] ([YEAR] rate) | $[NEW_BASE] ([TIER] standard) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS_DESCRIPTION] | [NEW_EXCESS_DESCRIPTION] |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

---
**DRIVER: `included_user_reduction`**

Your account was set up with **[LEGACY_INCLUDED] included users** in [YEAR] — more than the [NEW_INCLUDED] users standard for the [TIER] tier. That expanded allotment was part of your original arrangement. As part of this refresh, the included base is moving to the current [TIER] standard.

The new user pricing follows a graduated curve applied consistently across all accounts:

| Additional users above included base | Rate |
|---|---|
| 1–10 excess users | $25/user |
| 11–25 excess users | $22/user |
| 26–50 excess users | $20/user |
| 51+ excess users | $18/user |

[IF secondary driver = user_rate_normalization — add:]
Your per-user rate is also moving from **$[LEGACY_USER_RATE]/user** to the current graduated standard.

With [TRAILING_AVG] average users, [NEW_EXCESS] users are now above the [NEW_INCLUDED]-user included base, billed at the graduated rate: [EXCESS_MATH_BREAKDOWN] = $[NEW_USER_CHARGE]/month.

Here's how that plays out on your invoice:

| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] | $[NEW_BASE] ([TIER]) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS] users at $[LEGACY_RATE] = **$[LEGACY_USER_CHARGE]/month** | [NEW_EXCESS] users at graduated rate = **$[NEW_USER_CHARGE]/month** |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

*User billing is based on enabled accounts in your SuperCat environment — the user figures above reflect your current enabled count.*

---
**DRIVER: `platform_discount_correction`**

Your current pricing reflects a discount applied at signing in [YEAR]. As part of this refresh, legacy account-level discounts are being retired across all accounts. Everyone is moving to the same standard tier pricing. Your new monthly rate is the [TIER] standard rate for your account profile.

[IF no user structure change:]
The change is entirely on the platform side — your user count and user structure are unchanged.

| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] ([YEAR] discounted rate) | $[NEW_BASE] ([TIER] standard) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS_DESCRIPTION] | [NEW_EXCESS_DESCRIPTION] |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

---
**DRIVER: `at_book_tier_shift`**

When your account was set up in [YEAR], the [TIER] tier was priced at **$[LEGACY_BASE]/month**. The current book rate for [TIER] is **$[NEW_BASE]/month**. Your invoice is moving to the current book rate — your tier is not changing, only the rate.

| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] ([YEAR] book rate) | $[NEW_BASE] (current [TIER] book rate) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS_DESCRIPTION] | [NEW_EXCESS_DESCRIPTION] |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

---
**DRIVER: `multi_org_retirement`**

[ACCOUNT_NAME] has been part of SuperCat's multi-organization pricing program — a structure that applied cross-entity benefits across [PARENT_ORG] and its related accounts. That program is being retired as part of this refresh. Each entity moves to individual standard [TIER] pricing.

| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] (multi-org program) | $[NEW_BASE] ([TIER] standard) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS_DESCRIPTION] | [NEW_EXCESS_DESCRIPTION] |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

---
**DRIVER: `annual_discount_retirement`**

Your account has been billed at an annual commitment rate since [YEAR] — a discount applied at signing for annual prepayment. As part of this refresh, annual-commitment discounts are being retired across all accounts. Your new rate is the [TIER] standard monthly rate.

Annual prepay remains available if you prefer that billing structure — terms are the same, only the base rate is changing. If you'd like to continue annual billing, we'll document that as part of this transition.

| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] ([YEAR] annual rate) | $[NEW_BASE] ([TIER] standard) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS_DESCRIPTION] | [NEW_EXCESS_DESCRIPTION] |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

---
**DRIVER: `special_arrangement`**

Your current pricing reflects a custom arrangement from [YEAR] — a rate set outside SuperCat's standard commercial structure. As we bring all accounts onto the same pricing structure in 2026, custom arrangements are moving to standard tier rates. This is not a judgment about your account — it's a structural decision: one rate card, applied consistently. The new price is what every account at your tier and user count pays.

| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] (custom arrangement) | $[NEW_BASE] ([TIER] standard) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS_DESCRIPTION] | [NEW_EXCESS_DESCRIPTION] |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

> **Operator note:** For `special_arrangement` accounts with delta >30%, confirm the account history with Finance before outreach. The CEO must be prepared to answer "what was the arrangement and why is it changing?"

---

## What You're Getting at $[NEW_MRR]/Month

**[USE TIER-APPROPRIATE BLOCK — delete the others]**

**Catalog Essentials (T1):** At this rate, your team keeps what they're already running — the rep iPad app and your buyer-facing catalog. Your reps carry the full catalog offline, write orders in the field, and sync back. [NEW_INCLUDED] users included and standard support.

**Commerce Professional (T2):** At this rate, your team keeps everything they're already running — the rep app, your buyer-facing catalog, online ordering for your accounts, and order and invoice tracking. Your reps and your buyers are both working from the same catalog and customer file. [NEW_INCLUDED] users included, plus a dedicated CSM.

**Commerce Enterprise (T3):** At this rate, your team keeps everything they're already running — the rep app your field team sells from, your buyer-facing catalog, online ordering for your accounts, order and invoice tracking, and your sales intelligence dashboard. Up to 40 users are included, along with a dedicated CSM, priority support, and CPQ and credit card processing. No separate line items for any of it.

---

## What This Works Out To

[VALUE ANCHOR — calculate from Postgres data. Two formulas:
1. Per-order cost: new_mrr × 12 / ltm_orders
2. Delta per order: delta_mrr × 12 / ltm_orders

Express as: "Across [ltm_orders] eCat orders last year, the new annual subscription works out to approximately $[COST_PER_ORDER] per order. That's the cost of the full platform per transaction — catalog, ordering, buyer access, and intelligence infrastructure included." Then, IF delta_per_order < $50, add a second sentence: "The annual rate increase works out to approximately $[DELTA_PER_ORDER] per order." If delta_per_order ≥ $50, omit the second sentence entirely — the figure would work against the message.

Only include this section at all if ltm_orders > 0 and cost_per_order < $200. If ltm_orders is 0 or the per-order figure looks bad, omit this section entirely.]

---

## How This Compares

At **$[NEW_MRR]**, your new rate is [at the base rate for / below the midpoint for / above the midpoint for] accounts at this platform level. The same pricing structure is going to every account we work with — there are no account-specific adjustments in how your number was calculated.

[GUIDANCE: "at the base rate" = account lands at the tier floor ($774 T1 / $1,295 T2 / $2,295 T3). "below the midpoint" = between floor and midpoint. "above the midpoint" = above midpoint — REQUIRED when using "above the midpoint": append a clause connecting the position to user count, not tier premium: e.g., ", driven by your team size at [N] users — the platform base itself is at the [TIER] standard." This is mandatory to prevent the client from reading "above midpoint" as a premium or arbitrary upcharge. T3 midpoint ≈ $2,585. Delete this guidance before sending.]

---

## Your Pricing at a Glance

| | Before | After |
|---|---|---|
| **Monthly** | $[CURRENT_MRR] | **$[NEW_MRR]** |
| **Annual** | $[CURRENT_ARR] | **$[NEW_ARR]** |
| **Change** | — | +$[DELTA]/month ([DELTA_PCT]) |
| **Tier** | [LEGACY_TIER_LABEL] | [NEW_TIER_LABEL] |
| **Included users** | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| **Additional user rate** | [LEGACY_RATE_DESCRIPTION] | [NEW_RATE_DESCRIPTION] |

[IF primary or secondary driver is NOT `included_user_reduction`:]
Your workflow, your team's access, your catalog, and your integrations are unchanged. The only thing changing is the invoice.

[IF primary or secondary driver IS `included_user_reduction`:]
Your workflow, your team's access, your catalog, and your integrations are unchanged. The included user base and the invoice are both changing — the breakdown above explains exactly how.

---

## I'll Call You

I'll call you personally by **[SPECIFIC DATE]** — this isn't something I want to leave to email. If that timing doesn't work or you'd rather get ahead of it, reply to this email directly.

*This document also serves as formal written notice of a pricing modification under your SuperCat licensing agreement, effective [EFFECTIVE_DATE].*

---

*[CEO FIRST NAME] [CEO LAST NAME] | CEO | SuperCat*
*[DATE]*
