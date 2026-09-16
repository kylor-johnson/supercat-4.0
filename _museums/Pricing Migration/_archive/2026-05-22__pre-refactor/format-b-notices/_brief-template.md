# Format B — Brief Template
*60-Day Notice | >10% delta | CS-sent (Notice + Meeting tier)*

---

> **Internal routing note** (remove before sending):
> Brief type: `Format B` | >10% delta
> Account: [ACCOUNT_NAME] | Tier: [T1/T2/T3] | Wave: [WAVE]
> Migration driver: [DRIVER] | Health: [SCORE] — [BAND]
> Engagement: [E] | Adoption: [A] | Value Delivery: [VD] | Ops Health: [OH]
> Support fire: [YES/NO — IF YES: ⚠️ [N] days open. Confirm send timing with CEO before this goes out.] | Behavioral floor applied: [YES/NO]
> Delta: [DELTA_PCT] (+$[DELTA]/month)
> Cohort: [YEAR] [— NOTE IF EARLY ADOPTER: "2014 cohort — tenure acknowledgment required"]
> Contract: [MONTHLY/ANNUAL] | Renewal date: [DATE or UNKNOWN — confirm before sending]
> Earliest enforceable effective date: July 19, 2026 (61 days from May 19 — confirm for annual contracts)
> Comm_action: [FORMAT B TIER — Notice + Meeting / CEO Letter + Call Commitment / CEO Pre-Call → Format B]
> **CEO awareness required before send: [YES for CEO Letter and CEO Pre-Call tiers / NO for Notice + Meeting]**

---

# [ACCOUNT_NAME]: Your Pricing Is Changing

*Prepared for [ACCOUNT_NAME] | [DATE]*

---

[LEDE — 2–3 sentences. Always open with a relationship signal — tenure and platform activity — before landing the price. Integrate tenure naturally into the opening sentence for all healthy accounts: "[X years on SuperCat / Since [YEAR]], [activity stat — X eCat orders across Y customers, or X sessions in the last 90 days]. Your monthly invoice is moving from $[CURRENT_MRR] to $[NEW_MRR] — a change of $[DELTA]/month — and this document explains exactly why." Do not include per-order cost math here — that belongs in "What This Works Out To" only. Watch/At Risk/Critical health bands exception: skip the stats and lead directly with the dollar change. For accounts with delta >30%, the annual figure must appear alongside the monthly change: "a change of $[DELTA]/month ($[DELTA_ANNUAL]/year)."]

In 2026, we're moving every account to one clear pricing structure — here's exactly what that means for you. Your rate was set in [YEAR] — this is the first time we've updated it. Below is exactly why your number is changing and what you're getting at the new rate.

**[ADD FOR EARLY ADOPTER COHORTS — signed before 2016:]**
A change of this size warrants a real explanation. The platform you're running today is a fundamentally different product than it was in [YEAR]: your reps, your buyers, and your analytics team are all working from the same catalog, the same customer file, and the same order infrastructure. That's worth naming when this relationship is moving to a new price.

**[ADD FOR PLATFORM_DISCOUNT_CORRECTION ACCOUNTS — replace the "this is the first time we've updated it" sentence above:]**
Your rate reflects a discount applied at signing that's being retired as part of this change.

---

## Why the Number Is Changing

**[USE ONLY THE APPLICABLE BLOCK — delete all others]**

---
**DRIVER: `user_rate_normalization`**

Your additional-user rate has been **$[LEGACY_USER_RATE]/user** since your account was set up in [YEAR]. That rate reflects the pricing in place at signing — it hasn't been updated to the current standard. Going forward, every account moves to the same graduated user structure.

[REQUIRED when Before platform base ≠ After platform base — always include:]
Your platform base is also moving from $[LEGACY_BASE] to $[NEW_BASE] — this is the current [TIER] standard.

The new user pricing follows a graduated curve applied consistently across all accounts:

| Additional users above included base | Rate |
|---|---|
| 1–10 excess users | $25/user |
| 11–25 excess users | $22/user |
| 26–50 excess users | $20/user |
| 51+ excess users | $18/user |

[IF trailing avg users ≤ new included base — user charge goes to $0:]
Your included user base is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]. With [TRAILING_AVG] average users, all of your users are now covered within the included base — your user charge goes to $0/month.

[IF excess users remain after new included base:]
Your included user base is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED] — absorbing [N] users who no longer generate a charge. The remaining [NEW_EXCESS] excess users are billed at the graduated rate: [EXCESS_MATH_BREAKDOWN] = $[NEW_USER_CHARGE]/month.

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

Your account was set up with **[LEGACY_INCLUDED] included users** in [YEAR] — more than the [NEW_INCLUDED] users standard for the [TIER] tier. That expanded allotment was part of your original arrangement. As part of this change, the included base is moving to the current [TIER] standard.

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

Your current pricing reflects a discount applied at signing in [YEAR]. As part of this change, legacy account-level discounts are being retired across all accounts. Everyone is moving to the same standard tier pricing. Your new monthly rate is the [TIER] standard rate for your account profile.

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

[ACCOUNT_NAME] has been part of SuperCat's multi-organization pricing program — a structure that applied cross-entity benefits across [PARENT_ORG] and its related accounts. That program is being retired as part of this change. Each entity moves to individual standard [TIER] pricing.

| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] (multi-org program) | $[NEW_BASE] ([TIER] standard) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS_DESCRIPTION] | [NEW_EXCESS_DESCRIPTION] |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

---
**DRIVER: `annual_discount_retirement`**

Your account has been billed at an annual commitment rate since [YEAR] — a discount applied at signing for annual prepayment. As part of this change, annual-commitment discounts are being retired across all accounts. Your new rate is the [TIER] standard monthly rate.

Annual prepay remains available if you prefer that billing structure — terms are the same, only the base rate is changing. If you'd like to continue annual billing, we'll document that as part of this transition.

| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] ([YEAR] annual rate) | $[NEW_BASE] ([TIER] standard) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS_DESCRIPTION] | [NEW_EXCESS_DESCRIPTION] |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

---
**DRIVER: `special_arrangement`**

Your current pricing reflects a custom arrangement from [YEAR] — a rate set outside SuperCat's standard structure. In 2026, every account is moving to one clear pricing structure. The new rate is the [TIER] standard for your tier and user count.

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

Only include this section at all if ltm_orders > 0 and cost_per_order ≤ $35. If ltm_orders is 0, cost_per_order > $35, or the per-order figure would work against the message, omit this section entirely.]

---

## How This Compares

[USE THE APPLICABLE FORM — delete the other:]

[IF new_mrr = new_tier_base (no excess user charge — account lands at tier floor):]
At **$[NEW_MRR]**, your rate is the [TIER] standard. This is the same structure going to every account we work with.

[IF new_mrr > new_tier_base (account has additional user billing above the floor):]
At **$[NEW_MRR]**, your rate reflects the [TIER] standard — $[TIER_BASE] for the platform base, plus $[EXCESS_CHARGE]/month in additional user billing at the graduated rate. This is the same structure going to every account we work with.

[GUIDANCE: Do not use comparative language — "below the midpoint," "above the midpoint," peer ranges, or any claim the client cannot verify from the table. The tier floor ($[TIER_BASE] from new_tier_base in model data) and the excess user charge (already in the invoice table above) are both verifiable. Comparative claims are not. Delete this guidance before sending.]

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

## Let's Talk

I'll reach out in the next few days to walk through this together. If you want to get ahead of that — or if you have questions before then — reply directly and we'll find time.

*This document also serves as formal written notice of a pricing modification under your SuperCat licensing agreement, effective [EFFECTIVE_DATE].*

---

*[CSM NAME] | Customer Success | SuperCat*
*[DATE]*
