# Good News Notice — Tailwind Accounts (Price Decrease)
*Template | SuperCat Migration-Health Artifacts*

---

**When to use this template:** Accounts where the price is decreasing as a result of the 2026 pricing refresh. The mechanic — module compression, user count recalibration, or rate architecture correction — produces a lower invoice, and the notice exists to communicate it plainly. This is not a persuasion document. It requires no CEO co-signature, no pre-scheduled call, and no value justification. Send it, move on.

**Who sends it:** CS team. No CEO involvement required.

**Critical voice rules for this template:**
- Lead with the good news in the first sentence. Dollar amounts and effective date. No hedging, no setup.
- Do not call it a "gift," a "reward for loyalty," or anything that frames it as a favor. It is math. State it as math.
- Do not apologize for prior pricing. Do not imply the old invoice was wrong. It reflected the legacy structure; the new structure produces a different number.
- Do not bury the decrease after a paragraph of context.
- Do not include expansion opportunity language (Format C is a separate document, sent only after a confirmed positive migration signal — not here, not combined).
- Do not include percentage unless asked. Lead with dollar amount. The percentage is available in the summary table.

**Length target:** 200–300 words. This is an email-length notice, not a brief. Tables are optional for module_compression; required for user_count_variance.

---

> **Internal routing note** (remove before sending):
> Brief type: `good_news_notice` | Format: Tailwind (decrease)
> Account: [ACCOUNT_NAME] | Tier: [TIER] | Wave: [WAVE]
> Migration driver: [DRIVER] | Health: [SCORE] — [BAND]
> Current MRR: $[CURRENT_MRR] | New MRR: $[NEW_MRR] | Delta: –$[DELTA]/month
> Expansion eligible: [YES/NO] — if yes, queue Format C ONLY after confirmed positive migration signal (never combined with this notice)
> Watch health flag: [YES/NO] — if Watch or below: DO NOT use this template; escalate to CSM for health check-in first

---

# [ACCOUNT_NAME]: Your Invoice Is Decreasing

*Effective [EFFECTIVE_DATE]*

---

Your monthly invoice is decreasing from **$[CURRENT_MRR]** to **$[NEW_MRR]** — a reduction of **$[DELTA]/month** — effective **[EFFECTIVE_DATE]**.

[MECHANIC BLOCK — use one of the three below, delete the others]

---

**IF `module_compression`:**

As part of SuperCat's 2026 pricing restructure, the platform now moves to a unified tier model. For [ACCOUNT_NAME], this means the separate module charges that made up your current invoice are consolidating into a single [T1/T2/T3] tier subscription — at a lower combined rate.

| | Before | After |
|---|---|---|
| [MODULE_1 — e.g., iPad App] | $[M1_PRICE] | — |
| [MODULE_2 — e.g., Catalog] | $[M2_PRICE] | — |
| [MODULE_3 — if applicable] | $[M3_PRICE] | — |
| **[TIER_LABEL] subscription** | — | **$[NEW_MRR]** |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

---

**IF `user_count_variance`:**

Your current invoice is based on [CURRENT_BILLED_USERS] users. Your 6-month trailing average is [TRAILING_AVG_USERS] active users. As part of this refresh, user counts across all accounts are being aligned to trailing-average actuals. Your new invoice reflects [TRAILING_AVG_USERS] users at the current rate structure.

| | Before | After |
|---|---|---|
| Platform base ([TIER]) | $[BASE] | $[BASE] |
| Included users | [INCLUDED] | [INCLUDED] |
| Billable users | [OLD_EXCESS] users at $[OLD_RATE] = **$[OLD_USER_CHARGE]** | [NEW_EXCESS] users at graduated rate = **$[NEW_USER_CHARGE]** |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

---

**IF `rate_architecture`:**

Your current user rate was set at **$[LEGACY_RATE]/user** under the rate structure in place at signing. As part of the 2026 refresh, all accounts move to the same graduated rate card. For [ACCOUNT_NAME], the recalculated rate produces a lower invoice.

| | Before | After |
|---|---|---|
| Platform base ([TIER]) | $[BASE] | $[BASE] |
| Included users | [INCLUDED] | [INCLUDED] |
| Billable users | [OLD_EXCESS] users at $[OLD_RATE]/user = **$[OLD_USER_CHARGE]** | [NEW_EXCESS] users at graduated rate = **$[NEW_USER_CHARGE]** |
| **Monthly total** | **$[CURRENT_MRR]** | **$[NEW_MRR]** |

---

[END MECHANIC BLOCK]

Your workflow, your team's access, your catalog, and your integrations are unchanged. The only thing changing is the invoice.

Every account at every tier is moving to the same pricing structure in 2026. This is the number your configuration produces under that structure.

---

## Your Pricing at a Glance

| | Before | After |
|---|---|---|
| **Monthly** | $[CURRENT_MRR] | **$[NEW_MRR]** |
| **Annual** | $[CURRENT_ARR] | **$[NEW_ARR]** |
| **Change** | — | –$[DELTA]/month (–[DELTA_PCT]%) |
| **Effective date** | — | [EFFECTIVE_DATE] |

---

Questions about what's changing or how the new rate was calculated — reach out directly.

*[CSM NAME] | [TITLE] | SuperCat*

---

> **Operator notes (internal, remove before sending):**
>
> **Do not send if:**
> - Health band is Watch, At Risk, or Critical — route to CSM for health check-in first
> - Account is Unscored — cannot assess risk; hold until health data is available
> - Account is part of an entity whose packet is not yet assembled — all sibling brands must receive notice in a coordinated batch
> - Annual contract with unknown renewal date — confirm renewal date and 90-day window timing before sending
>
> **After sending:**
> - Log send date in CRM; start 60-day notice window clock
> - If account has an expansion_brief_type (t1_to_t2 or t2_to_t3): queue Format C for a separate conversation, after and only after a confirmed positive signal from this notice. Silence does not clear the gate.
> - If no response within 10 days: one-line follow-up ("Just checking the above reached you — wanted to make sure the invoice change on [DATE] doesn't catch anyone off guard.")
