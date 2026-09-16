# Internal CEO/CS Prep Sheet — Sarreid, Ltd.
*INTERNAL ONLY — never share with client*

---

> Account: **Sarreid, Ltd.**
> Tier: T3 | Migration brief format: B | Expansion eligible: NO
> Delta: +$655/month (+33.1%) | Effective date: July 17, 2026
> Migration driver: user_rate_normalization (+ platform base correction) | Health: 95.8 — Thriving
> Wave: 2 | Risk label: 6-Significant (>30%)
> Cohort playbook: **value_led** — Thriving account, large delta; CEO call mandatory before delivery
> ⚠️ FLAG: high_risk_delta — flagged in routing CSV. CEO must call before brief is delivered. Do not send cold via email.

---

## Account Snapshot

| Field | Value |
|---|---|
| Customer since | 2014 — 12 years |
| Current MRR | $1,978 |
| New MRR | $2,633 |
| Delta | +$655/month (+33.1%) |
| Tier | T3 → T3 (same tier, price correction) |
| Health score | 95.8/100 — Thriving |
| Primary migration driver | user_rate_normalization + platform base correction |
| Contract renewal date | N/A — monthly contract |
| CSM on account | Unknown — confirm before outreach |
| CEO relationship | Unknown — confirm with CS before call |
| Last CEO touchpoint | None on record |

---

## Contract Status

*Determines enforceable effective date — confirmed before sending.*

| Field | Value |
|---|---|
| Contract structure | MONTHLY |
| Initial term ended | YES — on file since 2014, 12 years running |
| Contract renewal date | N/A — monthly billing, no fixed renewal |
| Last price increase date | None on record |
| Earliest enforceable effective date | **July 17, 2026** (60 days from May 18, 2026 delivery date) |
| Notice recipient | Unknown — confirm contract signatory name and email with Finance before outreach |

> **Gate:** Contract structure is Monthly — confirmed. Effective date = July 17, 2026. Notice recipient is unknown; do not deliver the brief until Finance confirms the contract signatory.

---

## Health V3 Snapshot

*Source: Health V3 run 2026-05-13 (5 days old — well within 60-day window). No individual scorecard file; data from client_health_scores_2026-05-13.csv.*

| Dimension | Score | Band | Key narrative |
|---|---|---|---|
| **Composite** | 95.8/100 | Thriving | Performing well across the board — every dimension at 85 or above; consistent strength with no single area carrying the composite. |
| **Engagement** | 85.0/100 | — | 5,990 logins in 90 days; 60 of 105 reps active; pace holding at 1.1x baseline — no engagement concern. |
| **Adoption** | 100.0/100 | — | Using every configured feature — nothing unused. |
| **Value Delivery** | 100.0/100 | — | All configured channels are producing outcomes. |
| **Operational Health** | 97.7/100 | — | Catalog 93% complete; all 10 import feeds healthy; Product Stories feed is 68 days overdue against an ~11-day expected cadence — CS action item. |

| Flag | Status |
|---|---|
| Support fire | NO |
| Behavioral floor override | NO |
| Ghost account flag | NO |
| Health trend (last 3 months) | Stable — single run on file (2026-05-13); trend direction not calculable from one data point |

**What to know before the call:** Sarreid is one of the strongest accounts in the install base — 95.8 composite with perfect scores in Adoption and Value Delivery. Engagement is healthy at 85 (the relative floor here, not a concern). The one operational item to be aware of: the Product Stories import feed is 68 days overdue — this is a CS follow-up item, not a customer complaint, but be prepared if they raise data freshness during the call. Do not lead with platform health on the pricing conversation; the story is entirely value-positive.

| Usage metric | Value |
|---|---|
| Trailing avg billable users | 54 |
| Active reps (last 90d) | 60 of 105 |
| Orders (trailing annual) | Not available — no IP2.0 run on file |
| GMV (trailing annual estimate) | Not available — no IP2.0 run on file |
| B2B Cart active | NO — not in current stack (iPad+Catalog+Portal) |
| Buyers loaded | Not available — no IP2.0 run on file |
| Portal sessions (90d) | Not available — no IP2.0 run on file |

*If the CEO wants order volume or GMV context before the call, run on-demand queries against user-supercat-postgres-vpn and user-bigquery-vpn per Step 2b of the operator prompt.*

---

## Migration Driver: What You're Correcting

**user_rate_normalization + platform base correction**

Sarreid signed in 2014 at a negotiated platform rate of $1,370/month (covering iPad, Catalog, and Portal — below what would later become the T3 standard of $2,295) and a per-user rate of $16/user — one of the deepest legacy user discounts in the install base. Both were set before SuperCat established a consistent rate card. The platform correction moves the base from $1,370 to the T3 standard of $2,295 (+$925/month). The user rate correction moves from $16/user flat to the new graduated structure, but the concurrent expansion of included users from 25 to 40 absorbs 15 users and reduces per-user charges by $270/month. Net delta: +$655/month (+33.1%).

---

## Likely Objections — With Responses

### "Why is this happening now?"

> "We've been working through a full pricing standardization this year — the first time we've applied a consistent structure across all accounts. That's overdue given how much the platform has grown since your contract was signed in 2014."

### "My original rate was part of a deal — I earned that."

*Applies here: early adopter (2014), user_rate_normalization + platform base correction.*

> "Your early rate was set at a time when SuperCat was early-stage and your commitment helped us build something real. We're not pretending that rate was arbitrary — you did take a risk on us. What we're doing now is bringing every account onto the same structure, because running materially different rates indefinitely isn't fair to accounts who joined later at book rate. I want to make sure we handle this in a way that respects twelve years of partnership, and that's why I'm delivering this personally."

### "Why us? Are other accounts getting this too?"

> "Yes — 100% of the install base is moving to the same structure. You're not being singled out. Accounts at every tier and tenure level are getting the same correction. Your number reflects your user count and tier, nothing else."

### "This is a 33% increase. That's not something we can absorb easily."

> "I understand that. [IF willing to offer ramp:] We can phase this in over three months — here's what that looks like: [RAMP_OPTION]. The effective date of July 17, 2026 gives you approximately 60 days to plan for it. I'm happy to work with your finance team on timing if that's helpful."

### "What happens if we say no?"

*Prepare for this — have a clear answer before the call.*

> Option 1 (firm): "This is a standard migration we're completing across the full install base. The effective date is July 17, 2026. I want to work with you to make the transition smooth, but the pricing structure itself is the same for everyone."
> Option 2 (accommodation available): "We're not looking for an adversarial conversation here. If you have a specific budget constraint — a fiscal year challenge or a renewal timing issue — let's talk about what we can do to bridge the gap. I can offer [SPECIFIC_ACCOMMODATION]. What I can't do is hold a legacy rate indefinitely."

---

## Concession Hierarchy

*Work down the hierarchy — do not skip levels. Confirm approval authority before the call.*

**Guardrail:** No combination of concessions should reduce the effective first-year uplift by more than **25% of the gross delta**. Above that threshold requires CEO approval regardless of tier.

| Level | Lever | Who can approve | Available here? | Notes |
|---|---|---|---|---|
| **1 — CSM can offer** | Phase-in ramp: 50% first 60 days, then full rate | CSM | YES | Recommended given 33.1% delta — offer proactively if early tension is felt |
| **1 — CSM can offer** | Delayed effective date: push to next billing cycle (≤30 days) | CSM | YES | Administrative only — does not reduce the rate |
| **2 — Manager/council** | Extended ramp: 3–6 month phase-in with council sign-off | Manager + pricing council | YES — confirm before call | Appropriate for this delta level on a Thriving account; document ramp schedule if offered |
| **2 — Manager/council** | One-time bridge credit against first invoice | Manager + pricing council | YES — amount: up to $655 | Cap: 1 month delta. Applied as a credit, not a rate reduction. |
| **3 — CEO only** | Annual commitment at same rate (no discount) | CEO | YES | Locks revenue; appropriate if Sarreid asks for billing certainty |
| **3 — CEO only** | Subscription discount: max 10%, max 12 months, time-limited | CEO | Caution — only if needed | 10% = $263/month reduction; requires documented business reason |
| **NEVER** | Hold at current rate indefinitely | Not available | **NO** | Undermines install base standardization — this answer must be consistent across all accounts |

**Pre-call: confirm which level of authority is on the call.** CEO call is required before delivery (delta >25%). All three levels are in scope on a CEO call.

**25% uplift guardrail check:** Annual delta = $655 × 12 = **$7,860**. Maximum concession value = **$1,965** (25% of gross annual uplift). Any offer above this cap requires CEO sign-off before commitment.

---

## Churn Risk Assessment

| Signal | Status |
|---|---|
| Health band | Thriving (95.8/100) |
| Health trend | Stable — single run on file; no declining signal |
| Open support issues | NO |
| CSM confidence | Unknown — confirm with CS before call |
| Competitor known | Unknown — flag for CS to confirm before CEO call |
| Contract renewal proximity | N/A — monthly contract |
| Churn risk label | LOW — Thriving health with perfect Adoption and Value Delivery, but 33.1% delta and high_risk_delta routing flag mean CEO-first delivery is non-negotiable |

**Note:** Despite strong health, the `high_risk_delta` flag reflects the size of the rate correction (33.1%), not account instability. The risk is in the surprise of the number — mitigated by CEO personal delivery and the proactive call commitment.

---

## Expansion Notes

*Expansion brief type: none — no expansion conversation is queued for this account.*

Do not raise expansion during the migration conversation. If the account responds positively to the migration brief and asks about additional capabilities, route to CS for a follow-up conversation. No Format C brief is authorized at this time.

---

## Internal Notes

*CSM: add anything else the CEO should know before this call — relationship nuance, recent support history, known sensitivities, open renewal discussion, etc.*

- Sarreid signed in 2014 at a negotiated rate that predates SuperCat's standard rate card. The $16/user rate is among the deepest legacy user discounts in the install base; the platform base of $1,370 is also well below current T3 standard. Both corrections are justified and defensible.
- The `high_risk_delta` routing flag means this brief must not be sent cold. CEO call must precede delivery.
- Product Stories import feed is 68 days overdue — independent CS action item. Do not raise on the pricing call unless the client brings up data quality.
- No IP2.0 run exists for this account. If the CEO wants order volume, buyer count, or GMV figures before the call, run on-demand queries per the operator prompt Step 2b.
- No prior CEO touchpoint on record. Treat this as a relationship-building moment, not just a pricing notification.

---

*Internal prep sheet | Prepared May 18, 2026 | Paired with client-facing brief: sarreid_format-b_2026-05-18.md*
