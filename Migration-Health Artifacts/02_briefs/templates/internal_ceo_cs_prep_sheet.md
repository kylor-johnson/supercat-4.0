# Internal CEO/CS Prep Sheet
*Template | SuperCat Migration-Health Artifacts — INTERNAL ONLY, never share with client*

---

**Purpose:** This is the document the CEO and CSM read before any pricing conversation. It contains the account history, the risk profile, the likely objections, the negotiation boundaries, and the expansion notes. The client-facing brief is clean and restrained — this is where the full context lives.

**Use this before:**
- Sending Format A or B to the account
- Getting on a call to discuss pricing
- Responding to pushback
- Deciding whether to offer a transition accommodation

---

> Account: **[ACCOUNT_NAME]**
> Tier: [TIER] | Migration brief format: [A / B] | Expansion eligible: [YES/NO]
> Delta: +$[DELTA]/month ([DELTA_PCT]) | Effective date: [DATE]
> Migration driver: [DRIVER] | Health: [SCORE] — [BAND]
> Wave: [WAVE] | Risk label: [RISK]
> Cohort playbook: **[zero_friction / value_led / careful / high_touch / watch_sequence]**
> — zero_friction: ≤10% delta, Thriving/Healthy | value_led: >10% delta, Thriving/Healthy | careful: Watch band | high_touch: At Risk/Critical | watch_sequence: multi-step, hold until health improves

---

## Account Snapshot

| Field | Value |
|---|---|
| Customer since | [YEAR] — [N] years |
| Current MRR | $[CURRENT_MRR] |
| New MRR | $[NEW_MRR] |
| Delta | +$[DELTA]/month (+[DELTA_PCT]) |
| Tier | [CURRENT_TIER] → [NEW_TIER] (same tier, price correction) |
| Health score | [SCORE]/100 — [BAND] |
| Primary migration driver | [DRIVER] |
| Contract renewal date | [DATE or "unknown"] |
| CSM on account | [CSM_NAME] |
| CEO relationship | [STRONG / MODERATE / COLD / UNKNOWN] |
| Last CEO touchpoint | [DATE or "none on record"] |

---

## Contract Status

*Determines enforceable effective date — confirm before sending any brief.*

| Field | Value |
|---|---|
| Contract structure | [MONTHLY / ANNUAL] |
| Initial term ended | [YES / NO / UNKNOWN] |
| Contract renewal date | [DATE or "unknown — flag for legal/finance check"] |
| Last price increase date | [DATE or "none on record"] |
| Earliest enforceable effective date | [For monthly: 60 days from delivery date / For annual: no later than 90 days before renewal — calculate and fill before sending] |
| Notice recipient | [CONTRACT SIGNATORY NAME + EMAIL or "unknown — do not send until confirmed"] |

> **Gate:** If contract structure is UNKNOWN or renewal date is UNKNOWN, do not send Format B cold. Confirm with Finance before outreach. For Format A (≤10% delta), flag but proceed with 60-day notice assumption if monthly.

---

## Health V3 Snapshot

*Source: Health V3 latest run — pull from `Health V3/runs/[LATEST_RUN_DATE]/[ORG_SLUG]_scorecard.md`. Do not use stale data older than 60 days.*

| Dimension | Score | Band | Key narrative |
|---|---|---|---|
| **Composite** | [COMPOSITE_SCORE]/100 | [THRIVING / HEALTHY / WATCH / AT RISK / CRITICAL] | [One sentence from composite narrative] |
| **Engagement** | [E_SCORE]/100 | — | [Rep login frequency, active user share — one sentence] |
| **Adoption** | [A_SCORE]/100 | — | [Feature enablement, channel mix — one sentence] |
| **Value Delivery** | [VD_SCORE]/100 | — | [Order volume, GMV trend, buyer activation — one sentence] |
| **Operational Health** | [OH_SCORE]/100 | — | [Data freshness, support burden, config completeness — one sentence] |

| Flag | Status |
|---|---|
| Support fire | [YES — describe / NO] |
| Behavioral floor override | [YES — composite was floor-adjusted / NO] |
| Ghost account flag | [YES — low engagement ghost / NO] |
| Health trend (last 3 months) | [IMPROVING / STABLE / DECLINING — with score delta if declining] |

**What to know before the call:** [2–3 sentences synthesizing the Health V3 picture. Lead with the most call-relevant insight. Examples: "Rep engagement is strong (Engagement: 81) but buyer-side adoption is near zero — B2B Cart is configured but unused. Frame this as an operational gap the team can close, not a platform problem." OR "Composite dropped from 74 to 58 over 90 days, driven by a Value Delivery decline — GMV is down 22% trailing. Address the platform health separately from pricing; do not conflate the two on this call."]

| Usage metric | Value |
|---|---|
| Trailing avg billable users | [BILLABLE_USERS] |
| Active reps (last 90d) | [ACTIVE_REPS] of [TOTAL_REPS] |
| Orders (trailing annual) | [ORDERS_ANNUAL] |
| GMV (trailing annual estimate) | $[GMV] |
| B2B Cart active | [YES / NO / CONFIGURED ONLY] |
| Buyers loaded | [BUYER_COUNT] |
| Portal sessions (90d) | [PORTAL_SESSIONS] |

---

## Migration Driver: What You're Correcting

**[DRIVER]**

[Plain-language explanation of why this account's pricing is changing. E.g.: "Sarreid signed in 2014 at $1,370/month platform rate and $16/user — both set before SuperCat had a rate card. The platform base correction is $925/month. The user rate correction nets to –$270/month after included-base expansion. Net delta: +$655/month."]

---

## Likely Objections — With Responses

### "Why is this happening now?"

> "We've been working through a full pricing standardization this year — the first time we've applied a consistent structure across all accounts. [If long tenure:] That's overdue given how much the platform has grown since your contract was signed."

### "My original rate was part of a deal — I earned that."

*Use for: early adopters (pre-2016) being hit with user_rate_normalization or platform_base_correction.*

> "Your early rate was set at a time when SuperCat was early-stage and your commitment helped us build something real. We're not pretending that rate was arbitrary — you did take a risk on us. What we're doing now is bringing every account onto the same structure, because running materially different rates indefinitely isn't fair to accounts who joined later at book rate. [IF strong tenure relationship:] I want to make sure we handle this in a way that respects twelve years of partnership, and that's why I'm delivering this personally."

### "Why us? Are other accounts getting this too?"

> "Yes — 100% of the install base is moving to the same structure. You're not being singled out. Accounts at every tier and tenure level are getting the same correction. Your number reflects your user count and tier, nothing else."

### "This is a [X%] increase. That's not something we can absorb easily."

> "I understand that. [IF willing to offer ramp:] We can phase this in over [N] months — here's what that looks like: [RAMP_OPTION]. [IF not offering ramp:] The effective date is [DATE], which gives you [N] billing cycles to plan for it. I'm happy to work with your finance team on timing if that's helpful."

### "What happens if we say no?"

*Prepare for this — have a clear answer before the call.*

> Option 1 (firm): "This is a standard migration we're completing across the full install base. The effective date is [DATE]. I want to work with you to make the transition smooth, but the pricing structure itself is the same for everyone."
> Option 2 (accommodation available): "We're not looking for an adversarial conversation here. If you have a specific budget constraint — a renewal timing issue, a fiscal year challenge — let's talk about what we can do to bridge the gap. I can offer [SPECIFIC_ACCOMMODATION]. What I can't do is hold a legacy rate indefinitely."

---

## Concession Hierarchy

*What can be offered, by whom, and in what order. Work down the hierarchy — do not skip levels. Fill in approval status before the call.*

**Guardrail:** No combination of concessions should reduce the effective first-year uplift by more than **25% of the gross delta**. Above that threshold requires CEO approval regardless of tier.

| Level | Lever | Who can approve | Available here? | Notes |
|---|---|---|---|---|
| **1 — CSM can offer** | Phase-in ramp: 50% first 60 days, then full rate | CSM | [YES / NO] | Default offer for Watch-band accounts with delta >15% |
| **1 — CSM can offer** | Delayed effective date: push to next billing cycle (≤30 days) | CSM | [YES / NO] | Purely administrative — does not reduce the rate |
| **2 — Manager/council** | Extended ramp: 3–6 month phase-in with council sign-off | Manager + pricing council | [YES / NO — confirm before call] | Use for delta >25% on Healthy+ accounts; document the ramp schedule |
| **2 — Manager/council** | One-time bridge credit against first invoice | Manager + pricing council | [YES / NO — amount: $___] | Cap: not to exceed 1 month delta. Applies as a credit, not a rate reduction. |
| **3 — CEO only** | Annual commitment at same rate (no discount) | CEO | [YES / NO] | Annual locks revenue; appropriate for strategic accounts asking for certainty |
| **3 — CEO only** | Subscription discount: max 10%, max 12 months, time-limited | CEO | [YES / NO — % and duration: ___] | Rare. Requires documentation of specific business reason. |
| **NEVER** | Hold at current rate indefinitely | Not available | **NO** | Undermines install base standardization — this answer must be consistent across all accounts |

**Pre-call: confirm which level of authority is on the call.** If the CEO is calling, all three levels are available. If CSM-only, only Level 1 is in scope — escalate if the account pushes to Level 2 territory.

**25% uplift guardrail check:** First-year gross uplift = $[DELTA] × 12 = **$[ANNUAL_DELTA]**. Maximum concession value = **$[ANNUAL_DELTA × 0.25]**. Any offer above this cap requires CEO sign-off before commitment.

---

## Churn Risk Assessment

| Signal | Status |
|---|---|
| Health band | [BAND] |
| Health trend | [STABLE / IMPROVING / DECLINING] |
| Open support issues | [YES / NO — if yes, resolve before outreach] |
| CSM confidence | [HIGH / MEDIUM / LOW] |
| Competitor known | [YES: competitor name / NO] |
| Contract renewal proximity | [N months away] |
| Churn risk label | [LOW / MODERATE / HIGH / CRITICAL] |

**If churn risk is HIGH or CRITICAL:** Do not send Format B cold. CEO calls first, brief follows. Consider whether a transition accommodation is appropriate before the account hears the number.

---

## Expansion Notes

**[ONLY IF expansion_brief_type is not "none"]**

Expansion brief type: [t1_to_t2 / t2_to_t3]
Expansion eligible: [YES — after positive migration signal]

**Do not raise the expansion opportunity during the migration conversation.** Wait for:
- Explicit acknowledgment of the new price, OR
- Account asks about features available at the next tier, OR
- 14 days post-delivery with no objection (confirmed by CSM)

Pre-expansion context:
- [1–2 sentences on why this account is a good upgrade candidate: specific usage pattern, known pain point, buyer count, rep load, etc.]

---

## Internal Notes

*CSM: add anything else the CEO should know before this call — relationship nuance, recent support history, known sensitivities, open renewal discussion, etc.*

[FREEFORM FIELD]

---

*Internal prep sheet | Prepared [DATE] | Paired with client-facing brief: [BRIEF_FILENAME]*
