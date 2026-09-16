# Internal CEO/CS Prep Sheet
*SuperCat Migration-Health Artifacts — INTERNAL ONLY, never share with client*

---

> Account: **Braxton Culler**
> Tier: T3 | Migration brief format: A | Expansion eligible: NO
> Delta: +$15/month (+0.6%) | Effective date: July 17, 2026 (60-day notice assumption — contract structure unconfirmed, see Contract Status)
> Migration driver: user_rate_normalization | Health: 94.8 — Thriving
> Wave: 1 | Risk label: 3-Flat (0–10%)
> Cohort playbook: **zero_friction** — ≤10% delta, Thriving band

---

## Account Snapshot

| Field | Value |
|---|---|
| Customer since | 2022 — 4 years |
| Current MRR | $2,380 |
| New MRR | $2,395 |
| Delta | +$15/month (+0.6%) |
| Tier | T3 — Commerce Enterprise → T3 — Commerce Enterprise (same tier, price correction) |
| Health score | 94.8/100 — Thriving |
| Primary migration driver | user_rate_normalization |
| Contract renewal date | Unknown — confirm with Finance before sending |
| CSM on account | Unknown — confirm before delivery |
| CEO relationship | Unknown |
| Last CEO touchpoint | None on record |

---

## Contract Status

*Determines enforceable effective date — confirm before sending any brief.*

| Field | Value |
|---|---|
| Contract structure | UNKNOWN — no contract data in routing CSV or available files |
| Initial term ended | UNKNOWN |
| Contract renewal date | Unknown — flag for Finance confirmation |
| Last price increase date | None on record |
| Earliest enforceable effective date | July 17, 2026 (assumed: 60 days from delivery May 18, 2026, treating as monthly) |
| Notice recipient | Unknown — confirm contract signatory before sending |

> **Gate note:** Contract structure is unconfirmed. Per Format A gate rule: flagged and proceeding with 60-day notice assumption. Confirm with Finance before delivery. If annual contract, recalculate: effective date must be no later than 90 days before renewal.

---

## Health V3 Snapshot

*Source: Health V3 run 2026-05-13 — within 60 days, current.*

| Dimension | Score | Band | Key narrative |
|---|---|---|---|
| **Composite** | 94.8/100 | Thriving | Every dimension at 86 or higher — consistent platform strength across the board; no action needed, monitor at standard cadence. |
| **Engagement** | 90.7/100 | — | 56 of 63 reps logging in regularly; 3,655 logins in 90 days, pace holding at 1.3x baseline. |
| **Adoption** | 100.0/100 | — | Using every configured feature — nothing unused. |
| **Value Delivery** | 100.0/100 | — | All configured channels are producing outcomes. |
| **Operational Health** | 85.6/100 | — | Catalog 82% complete; all 13 import feeds healthy; data feeds running on cadence. |

| Flag | Status |
|---|---|
| Support fire | NO |
| Behavioral floor override | NO |
| Ghost account flag | NO |
| Health trend (last 3 months) | Unknown — single run on file (2026-05-13); no prior run available for comparison |

**What to know before the call:** This is a near-zero-friction migration at +$15/month. The account is running all four configured surfaces at full adoption with both Value Delivery and Adoption at 100 — every channel and feature is producing. The objection most likely to surface is procedural (billing cycle timing, who gets the notice), not strategic. Do not over-engineer the conversation; send the brief and offer a brief walkthrough.

| Usage metric | Value |
|---|---|
| Trailing avg billable users | 44 (25 included + avg 19 additional under legacy structure; new: 40 included + 4 excess) |
| Active reps (last 90d) | 56 of 63 (Health V3: 90.7 engagement; login_events query: 55 distinct users — aligns) |
| Orders (trailing annual) | 2,771 (confirmed via Postgres MCP query, org_id 171) |
| GMV (trailing annual estimate) | Not available (no BigQuery access during this run) |
| B2B Cart active | YES — enable_online_ordering = true (confirmed via mobile_sites table) |
| Buyers loaded | 2,021 (confirmed via Postgres MCP query, customers table, org_id 171) |
| Portal sessions (90d) | Not available (no analytics/Clicky data in Postgres) |

---

## Migration Driver: What You're Correcting

**user_rate_normalization**

Braxton Culler signed in 2022 at $20/user for additional users above a 25-user included base. That rate predates the current graduated rate card. Under the new structure: the included base expands from 25 to 40 users, absorbing 21 of the current 25 additional users at no charge. Remaining 4 excess users bill at $25/user (first tier of new graduated structure). New user charge: $100/month — down from $500/month. Platform base normalizes from $1,880 to $2,295 (+$415). Net delta: +$15/month (+0.6%).

---

## Likely Objections — With Responses

### "Why is this happening now?"

> "We've been working through a full pricing standardization this year — the first time we've applied a consistent structure across all accounts. Your rate at signing was set in 2022 and hasn't been updated since; we're bringing it in line with the standard structure."

### "My original rate was part of a deal — I earned that."

> "Your rate in 2022 reflected what we offered at signing. We're not pretending it was arbitrary. What we're doing now is bringing every account onto the same structure — it's not fair to accounts who joined later at book rate to leave legacy rates in place indefinitely. Your net change is $15/month, which reflects the fact that your expanded included base actually absorbed most of your additional user charges."

### "Why us? Are other accounts getting this too?"

> "Yes — 100% of the install base is moving to the same structure. You're not being singled out. Accounts at every tier and tenure level are getting the same correction. Your number reflects your user count and tier, nothing else."

### "This is a price increase. That's not something we can absorb easily."

> "I understand that. At $15/month, the effective change is less than a rounding error on a $2,380 invoice. The effective date is July 17, which gives you two billing cycles. I'm happy to walk through the math on a call if that's helpful — the user charge mechanics are the most useful thing to understand."

### "What happens if we say no?"

> Option 1 (firm): "This is a standard migration we're completing across the full install base. The effective date is July 17, 2026. I want to work with you to make the transition smooth, but the pricing structure itself is the same for everyone."

---

## Concession Hierarchy

*Work down the hierarchy — do not skip levels.*

**Guardrail:** No combination of concessions should reduce the effective first-year uplift by more than 25% of the gross delta.

| Level | Lever | Who can approve | Available here? | Notes |
|---|---|---|---|---|
| **1 — CSM can offer** | Phase-in ramp: 50% first 60 days, then full rate | CSM | YES | Unlikely needed at $15/month delta — offer only if client specifically requests it |
| **1 — CSM can offer** | Delayed effective date: push to next billing cycle (≤30 days) | CSM | YES | Purely administrative |
| **2 — Manager/council** | Extended ramp: 3–6 month phase-in | Manager + pricing council | YES | Almost certainly unnecessary at this delta |
| **2 — Manager/council** | One-time bridge credit against first invoice | Manager + pricing council | YES — amount: $15 cap | Cap equals one month delta |
| **3 — CEO only** | Annual commitment at same rate | CEO | YES | Appropriate if account wants rate certainty |
| **3 — CEO only** | Subscription discount: max 10%, max 12 months | CEO | NO | Not warranted at 0.6% delta |
| **NEVER** | Hold at current rate indefinitely | Not available | **NO** | Undermines install base standardization |

**25% uplift guardrail check:** Annual delta = $15 × 12 = **$180**. Maximum concession value = **$45**. Any single accommodation at this account will be within the guardrail without further calculation.

---

## Churn Risk Assessment

| Signal | Status |
|---|---|
| Health band | Thriving (94.8/100) |
| Health trend | Unknown — single run on file |
| Open support issues | NO (support_fire = false in routing and Health V3) |
| CSM confidence | Unknown — confirm before delivery |
| Competitor known | Unknown |
| Contract renewal proximity | Unknown — confirm with Finance |
| Churn risk label | **LOW** — Thriving band, 0.6% delta, full platform adoption |

---

## Expansion Notes

Expansion brief type: **none** — Braxton Culler is already on T3 (Commerce Enterprise), the top tier. No expansion path available. No expansion brief to queue.

---

## Internal Notes

*CSM: add anything else the CEO should know before this call — relationship nuance, recent support history, known sensitivities, open renewal discussion, etc.*

Contract structure must be confirmed before delivery. All pricing data sourced from routing CSV and Health V3 run 2026-05-13. IP2.0 run not on file; MCP queries run 2026-05-18 (orders: 2,771; buyers: 2,021; B2B Cart: active). No prior Health V3 run available for trend comparison.

---

*Internal prep sheet | Prepared May 18, 2026 | Paired with client-facing brief: bcf_format-a_v2_2026-05-18.md*
