# Format A: Price Normalization Brief — Near-Flat Accounts (≤10% delta)
*Template | SuperCat Migration-Health Artifacts*

---

**When to use this template:** Accounts where the price change is ≤10%. Typically Wave 1, Thriving or Healthy health. The brief demonstrates that you know this client, explains the pricing change, confirms what they have, and tells them what's coming — in that order.

**Who sends it:** CS team, potentially CEO-signed for named accounts. Keep it brief. This does not need to be a call — it can land as a written notice with a follow-up offer.

> **Tone rule (remove before sending):** Begin by demonstrating that you know this client. The price change is the second thing they read, not the first. For accounts with 3+ years of tenure, sentence one names the relationship before anything about pricing. For 10+ year accounts, the weight of that history leads. For all accounts, prove you looked at this specific account — not any account. The lede names the relationship, then delivers the number. Never the reverse.

---

> **Internal routing note** (remove before sending):
> Brief type: `value_justification` | Format A (≤10% delta)
> Account: [ACCOUNT_NAME] | Tier: [TIER] | Wave: [WAVE]
> Migration driver: [DRIVER] | Health: [SCORE] — [BAND] | Risk label: [RISK]
> Engagement: [E_SCORE] | Adoption: [A_SCORE] | Value Delivery: [VD_SCORE] | Ops Health: [OH_SCORE]
> Support fire: [YES/NO] | Behavioral floor applied: [YES/NO]
> Expansion eligible: [YES/NO] — if yes, queue [EXPANSION_BRIEF_TYPE] after positive migration signal

---

# [ACCOUNT_NAME]: Your Pricing Is Changing

*Prepared for [ACCOUNT_NAME] | [DATE]*

---

**[LEDE BLOCK — Thriving and Healthy accounts only. If health_band is Watch, At Risk, or Critical: delete this entire block and the "What You've Built" section, and begin with the price change sentence below. See operator prompt Step 3a for population instructions.]**

[LEDE_PARAGRAPH — 2–3 sentences. Lead with what you know about this client — tenure, what they've built, how they use the platform. The price change lands in the same paragraph, but second. For accounts with 3+ years: name the tenure in sentence one. For all accounts: prove you looked at this specific account. Use unambiguous platform metrics (users, sessions, surfaces active, tenure) — not order counts as headline proof. If order count is used, scope it to "orders submitted through SuperCat." Do not frame logins as a ratio of provisioned users. Do not calculate per-order subscription costs in this section. Example for a long-tenured account: "[N] years, [X] active users, [STANDOUT: 'every platform surface in daily use' / 'X sessions in the last 90 days']. Your monthly invoice is moving from **$[CURRENT_MRR]** to **$[NEW_MRR]** — a $[DELTA] change — and this document explains exactly why."]

## What You've Built on SuperCat

[PLATFORM_STATS — 3–4 data point sentences using confirmed Step 2b data only. Do not estimate. If fewer than 2 data points are available, delete this section entirely. Frame each stat as the client's own output, not as a SuperCat measurement. Lead with unambiguous platform metrics: active users, session volume, surfaces in active use, tenure. If order count is used, scope it explicitly to "orders submitted through SuperCat" — never frame as the account's total order volume. Do not include per-order subscription cost calculations in this section. Keep each sentence to one fact.]

---

**[END LEDE BLOCK — for Watch/At Risk/Critical accounts, begin here:]**

Effective **[EFFECTIVE_DATE]**, your monthly invoice moves from **$[CURRENT_MRR]** to **$[NEW_MRR]** — a change of **$[DELTA]/month ([DELTA_PCT])**.

In 2026, we're moving every account to one clear pricing structure — here's exactly what that means for you. [ONE SENTENCE matching the driver and cohort year: "The tier structure and pricing model now reflect what the platform is today." / (≤5 year tenure): "Your rate was set in [YEAR] — this is the first time we've updated it." / (10+ year tenure): "Your rate has been unchanged since [YEAR] — this is the first time we've adjusted it."] Below is exactly why your number is changing and what you're getting at the new price.

---

## Why the Number Is Changing

**Driver: [DRIVER — use one of the blocks below, delete the others]**

> **Included user change rule (remove before sending):** For any account where `new_included_users` < `current_provided_users`: (1) Add a sentence naming the change: "The included user count for this tier standardizes to [N] users going forward." (2) Confirm whether the client's team is inside or outside the new base. (3) Threshold check — two cases: **If `trailing_avg_users < new_included_users` AND `trailing_avg_users ≥ (new_included_users − 3)`**: add "At your current team size, you have [X] users of room before additional charges apply at $25/user." **If `trailing_avg_users ≥ new_included_users`** (already in excess): do NOT use the "room" framing — instead note the overage directly: "[N] users fall above the included base and are billed at the graduated rate." The headroom sentence only applies to accounts currently inside the base but near the edge. Accounts already in overage need the overage acknowledged, not headroom stated.

> **Platform base repricing rule (remove before sending):** For any account where `new_tier_base` > `current_platform_mrr` — regardless of driver — add this sentence within the "Why the Number Is Changing" block, after the introductory framing: "The platform has grown considerably since [YEAR] — more surfaces, more capability, the infrastructure behind it. The rate now reflects what the platform is today." This is the answer to "what am I paying more for?" It applies to `user_rate_normalization`, `at_book_tier_shift`, `discount_correction`, and any other driver where the base line increases. Do not leave a base increase unexplained under any driver.

---
**IF `user_rate_normalization`:**

Your additional-user rate has been **$[LEGACY_USER_RATE]/user** since your account was set up in [YEAR]. That rate reflects the pricing in place at signing — it hasn't been updated to the current standard. Going forward, every account moves to the same graduated user structure.

The new user pricing follows a graduated curve applied consistently across all accounts:

| Additional users above included base | Rate |
|---|---|
| 1–10 excess users | $25/user |
| 11–25 excess users | $22/user |
| 26–50 excess users | $20/user |
| 51+ excess users | $18/user |

Here's how that plays out for your account:

| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] | $[NEW_BASE] ([TIER]) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS] users at $[LEGACY_RATE] = **$[LEGACY_USER_CHARGE]/month** | [NEW_EXCESS] users at graduated rate = **$[NEW_USER_CHARGE]/month** |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

[Optional: If the included-base expansion absorbs users: "The new included base absorbs [N] of your current additional users — those users no longer generate a charge. The net effect on your user charges is [+/–$X/month]."]

---
**IF `discount_correction`:**

Your current pricing reflects a [N%] discount applied at signing in [YEAR]. Going forward, account-level discounts are being retired — every account moves to the same standard tier pricing. Your new monthly rate is the standard rate for your usage profile.

| | Before | After |
|---|---|---|
| Platform rate | $[LEGACY_BASE] ([N]% below book) | $[NEW_BASE] (standard) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS] at $[LEGACY_RATE]/user | [NEW_EXCESS] at graduated rate |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

---
**IF `module_compression`:**

SuperCat's legacy pricing structured your account as separate module line items. Those modules are now part of a single unified tier. For [ACCOUNT_NAME], the consolidation means **your monthly price is decreasing from $[CURRENT_MRR] to $[NEW_MRR]** — the unified tier includes everything you were paying for separately, at a lower combined rate.

| | Before (modules) | After (tier) |
|---|---|---|
| [MODULE_1] | $[M1_PRICE] | — |
| [MODULE_2] | $[M2_PRICE] | — |
| [MODULE_3] | $[M3_PRICE] | — |
| **[TIER_NAME] base** | — | **$[NEW_BASE]** |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

---
**IF `at_book_tier_shift`:**

When your account was set up in [YEAR], the [TIER] tier was priced at **$[LEGACY_BASE]/month**. The current standard for [TIER] is **$[NEW_BASE]/month**. The platform has grown considerably since [YEAR] — more surfaces, more capability, the infrastructure behind it. The rate now reflects what the platform is today. Your tier is not changing, and neither is what your team has access to.

| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] ([TIER] at [YEAR] pricing) | $[NEW_BASE] ([TIER] current book rate) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS] at $[LEGACY_RATE]/user | [NEW_EXCESS] at graduated rate |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

---
**IF `multi_org_retirement`:**

[ACCOUNT_NAME] has been part of SuperCat's multi-organization pricing program — a structure that applied cross-entity pricing benefits across [PARENT_ORG] and its related accounts. That program is being retired. Going forward, each entity moves to individual standard [TIER] pricing.

Your pricing moves from the multi-org program rate to the standard [TIER] rate for your account's user count and configuration. Every [PARENT_ORG] entity is making the same move.

| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] (multi-org program rate) | $[NEW_BASE] ([TIER] standard) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS] at $[LEGACY_RATE]/user | [NEW_EXCESS] at graduated rate |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

---
**IF `special_arrangement`:**

Your current pricing reflects a custom arrangement from [YEAR] — a rate set outside the standard structure at the time. In 2026, every account moves to the same tier structure, including those on custom arrangements.

The new pricing is the standard [TIER] rate for your account's user count and configuration.

| | Before | After |
|---|---|---|
| Platform base | $[LEGACY_BASE] (custom arrangement, [YEAR]) | $[NEW_BASE] ([TIER] standard) |
| Included users | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| Additional billable users | [LEGACY_EXCESS] at $[LEGACY_RATE]/user | [NEW_EXCESS] at graduated rate |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

---

## What You're Getting at $[NEW_MRR]/Month

**[USE ONLY THE APPLICABLE BLOCK — delete the others]**

**IF Catalog Essentials (T1):**

At this rate, your team keeps the iPad rep app, admin console, and buyer-facing product catalog — the tools your reps use to sell from the field, your buyers use to browse, and your team uses to manage catalog and orders. Up to 10 users are included, with standard support. No separate line items.

---

**IF Commerce Professional (T2):**

At this rate, your team keeps everything they're already running — the rep app your field team sells from, your buyer-facing catalog, online ordering for your accounts, and order and invoice tracking for your buyers. Up to 15 users are included, along with a dedicated CSM and standard support. No separate line items.

---

**IF Commerce Enterprise (T3):**

At this rate, your team keeps everything they're already running — the rep app your field team sells from, your buyer-facing catalog, online ordering for your accounts, order and invoice tracking, and your sales intelligence dashboard. Up to 40 users are included, along with a dedicated CSM, priority support, and CPQ and credit card processing. No separate line items for any of it.

---

## What's Coming in 2026

At this rate, you have access to two releases already in progress:

**June 1**
- **Rebuilt admin console** — The admin console is getting its first major redesign in years. Faster to navigate, easier to update, cleaner day-to-day management from top to bottom.
- **Rapid fire scanning** — Optimized for high-volume market environments. Your reps write more orders, move between meetings faster, without losing momentum mid-floor.
- **Multiple active orders** — Open more than one order at a time. Start a cart for one account, shift to another buyer, come back without starting over.

**July 1**
- **Rep activity log** — Your reps log calls, visits, and follow-up notes inside SuperCat. You see it in one place. One source of truth for what's happening in the field — no separate system needed for the conversations that happen before an order.
- **Direct catalog editing** — Edit product data, configurations, and mappings in a live web view. The export-edit-reimport cycle for small catalog changes goes away.

*[Operator note — remove before sending: For T1 accounts, lead with the June 1 field-selling improvements. For T2/T3 accounts with larger rep teams, give equal weight to all five. All five features apply to all accounts.]*

---

## How This Compares

**[ACCOUNT_NAME]'s** new pricing of **$[NEW_MRR]/month** is [below the midpoint / near the midpoint / above the midpoint] of what [T1/T2/T3] accounts pay after migration. Across accounts we work with, [T1/T2/T3] monthly pricing after migration ranges from **$[PEER_LOW]–$[PEER_HIGH]**.

*[Internal reference — do not include in client copy: T1 range $774–$1,629/mo (midpoint $1,202) | T2: $1,295–$1,589/mo (midpoint $1,442) | T3: $2,295–$2,875/mo (midpoint $2,585). Use to populate PEER_LOW/PEER_HIGH above. Position rule: NEW_MRR < midpoint → "below the midpoint"; within ±$75 of midpoint → "near the midpoint"; NEW_MRR > midpoint + $75 → "above the midpoint". No percentile notation. ABOVE THE MIDPOINT — REQUIRED: the sentence must include a user-count clause explaining the position, e.g.: "…is above the midpoint of what [TIER] accounts pay after migration, driven by your team size at [N] users — the platform base itself is at the [TIER] standard." Do not state "above the midpoint" without the clause.]*

**[FOR T3 ACCOUNTS — add this sentence, delete for T1/T2:]** For external context: equivalent platforms offering comparable full-stack commercial operating scope are priced at $3,000–$3,500/month at comparable user scales.

This is the same structure going to every account we work with.

---

## Your Pricing at a Glance

| | Before | After |
|---|---|---|
| **Monthly** | $[CURRENT_MRR] | **$[NEW_MRR]** |
| **Annual** | $[CURRENT_ARR] | **$[NEW_ARR]** |
| **Change** | — | +$[DELTA]/month ([DELTA_PCT]) |
| **Tier** | [LEGACY_TIER_LABEL] | [NEW_TIER_LABEL] |
| **Included users** | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| **Additional user rate** | $[LEGACY_RATE]/user | Graduated ($25/$22/$20/$18) |

Your workflow, your team's access, your catalog, and your integrations are unchanged. The only thing changing is the invoice.

---

## What Happens Next

Your Customer Success contact will be in touch directly before [EFFECTIVE_DATE]. If you'd like to talk through the rate or anything about this before then — that conversation is welcome. Reach out now. There's no process here — just a direct conversation with someone who knows your account.

*Prepared [DATE]*
