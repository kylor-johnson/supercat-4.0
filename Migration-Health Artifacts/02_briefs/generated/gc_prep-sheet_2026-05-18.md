# Internal CEO/CS Prep Sheet
*SuperCat Migration-Health Artifacts — INTERNAL ONLY, never share with client*

---

**Purpose:** This is the document the CEO and CSM read before any pricing conversation. It contains the account history, the risk profile, the likely objections, the negotiation boundaries, and the expansion notes. The client-facing brief is clean and restrained — this is where the full context lives.

**Use this before:**
- Sending Format A to the account
- Getting on a call to discuss pricing
- Responding to pushback
- Deciding whether to offer a transition accommodation

---

> Account: **Groupe Courchesne**
> Tier: T2 | Migration brief format: A | Expansion eligible: YES (gated — see Expansion Notes)
> Delta: –$120/month (–8.5%) | Effective date: July 17, 2026
> Migration driver: module_compression | Health: 62.3 — Healthy
> Wave: 1 | Risk label: 2-Decrease (0-10%)
> Cohort playbook: **zero_friction** — ≤10% delta, Healthy band, price decrease

---

## Account Snapshot

| Field | Value |
|---|---|
| Customer since | 2023 — 3 years |
| Current MRR | $1,415 |
| New MRR | $1,295 |
| Delta | –$120/month (–8.5%) |
| Tier | T2 → T2 (same tier; per-module billing consolidated to unified price) |
| Health score | 62.3/100 — Healthy |
| Primary migration driver | module_compression |
| Contract renewal date | Monthly rolling — no fixed renewal date |
| CSM on account | Confirm before outreach |
| CEO relationship | Unknown — confirm before outreach |
| Last CEO touchpoint | None on record |

---

## Contract Status

*Determines enforceable effective date — confirm before sending any brief.*

| Field | Value |
|---|---|
| Contract structure | Monthly |
| Initial term ended | Assumed YES (joined 2023; 12-month initial term likely ended 2024) — verify with Finance |
| Contract renewal date | Monthly rolling — no fixed date |
| Last price increase date | Not on record |
| Earliest enforceable effective date | July 17, 2026 (60 days from delivery date of May 18, 2026) |
| Notice recipient | Contract signatory — unknown; confirm with Finance before sending |

> **Gate:** Contract signatory not confirmed. For Format A (≤10% delta, price decrease), proceed with 60-day notice assumption and July 17, 2026 effective date. Confirm signatory before delivery.

---

## Health V3 Snapshot

*Source: Health V3 run 2026-05-13 — 5 days old at time of brief generation.*

| Dimension | Score | Band | Key narrative |
|---|---|---|---|
| **Composite** | 62.3/100 | Healthy | Reps are logging in at a limited rate and using only a portion of the platform; feature-coverage gap is the primary risk, not an activity problem. |
| **Engagement** | 61.7/100 | — | 781 logins in 90 days, but only 16 of 326 reps (5%) have logged in this quarter — most of the team isn't engaged; pace holding steady at 1.3x baseline. |
| **Adoption** | 57.1/100 | — | 4 of 7 applicable features in use; eCat Online Catalog and B2B Cart are enabled but generating zero traffic or orders in 90 days; Sales Data feed has not run in 90 days. |
| **Value Delivery** | 60.0/100 | — | 3 of 5 configured channels producing outcomes; online catalog and B2B Cart show zero activity in the trailing 90-day window. |
| **Operational Health** | 72.2/100 | — | Catalog 99% complete; 3 of 4 import feeds healthy; Multifile Import feed critically overdue — last ran 33 days ago against a ~1-day expected cadence. |

| Flag | Status |
|---|---|
| Support fire | NO |
| Behavioral floor override | NO |
| Ghost account flag | NO |
| Health trend (last 3 months) | Stable — single run on file; no prior run to compute delta |

**What to know before the call:** This call should be simple — the invoice is going down, not up, and the account is in good standing. The conversation risk is not price pushback; it's questions about what's actually running on the platform. Only 16 of 338 total users have logged in during the past 90 days, the B2B Cart and online catalog are generating zero traffic despite being configured, and the Multifile Import feed is critically overdue (33 days vs. ~1 day expected cadence). If these come up, separate them cleanly from the pricing conversation and route to a CS follow-up session on platform activation — they're operational gaps, not billing objections.

| Usage metric | Value |
|---|---|
| Trailing avg billable users | 12 (within 15-user T2 included base — no excess charges) |
| Active reps (last 90d) | 16 of 338 total (confirmed via login_events query) |
| Orders (trailing annual) | 1,575 |
| GMV (trailing annual estimate) | Not available |
| B2B Cart active | Configured — enable_online_ordering = TRUE; zero portal orders in 90 days per H3 |
| Buyers loaded | 4,451 total; 449 active (ordered in last 12mo); ~432 ordered historically, inactive 12mo+ |
| Portal sessions (90d) | Not available (enable_sales_portal = FALSE — Sales Portal not enabled) |

---

## Migration Driver: What You're Correcting

**module_compression**

Groupe Courchesne's billing was structured as four separate legacy module line items: eCat iPad ($725/month, 25-user limit at $20/user), eCat Online Service ($295/month), eCat Online – B2B Cart ($295/month), and eCat Online – Closed Site ($100/month) — summing to $1,415/month total. Those separate line items are now consolidated into the Commerce Professional (T2) unified tier at $1,295/month. The account carries 12 trailing average active users, which is within the new T2 15-user included base — no user excess charges apply before or after migration. Net effect: –$120/month, –8.5%.

---

## Likely Objections — With Responses

### "Why is this happening now?"

> "We've been working through a full pricing standardization this year — the first time we've applied a consistent structure across all accounts. Your account was on a legacy per-module billing structure; we're replacing that with the same unified tier model that applies to the rest of the install base."

### "My original rate was part of a deal — I earned that."

*Less likely here given this is a decrease, but prepare for it if the account views the module structure as locked.*

> "Your early module-level pricing reflected how we sold the platform at the time — individual components rather than a bundled tier. We're retiring that model across the board and consolidating to a single commercial structure. The result for you specifically is a lower combined rate."

### "Why us? Are other accounts getting this too?"

> "Yes — 100% of the install base is moving to the same structure. You're not being singled out. Accounts at every tier and tenure level are receiving the same standardization. Your number reflects your tier and usage profile, nothing else."

### "I had 25 included users before — now I only get 15. That's a reduction."

*This is the most likely substantive objection. Prepare for it.*

> "Your average active user count over the trailing period is 12 — well within the new 15-user included base. You're paying zero in user charges today, and you'll pay zero in user charges after migration. If your team grows above 15 active users, the graduated rate structure applies ($25/$22/$20/$18), but at your current usage pattern, the included base more than covers you. The invoice goes down, and your user profile is unchanged."

### "What happens if we say no?"

> "This is a standard migration we're completing across the full install base. The effective date is July 17, 2026. In your case, the change is in your favor — the invoice is decreasing. I want to make sure you have all the context you need, but the pricing structure itself is the same for everyone."

---

## Concession Hierarchy

*What can be offered, by whom, and in what order. This account is receiving a price decrease — concessions are unlikely to be required. Document for completeness.*

**Guardrail:** This brief involves a price decrease (–$120/month). The standard 25% uplift guardrail is not triggered. No concession is necessary to close this migration.

| Level | Lever | Who can approve | Available here? | Notes |
|---|---|---|---|---|
| **1 — CSM can offer** | Phase-in ramp: 50% first 60 days, then full rate | CSM | NO — not applicable for price decreases | N/A |
| **1 — CSM can offer** | Delayed effective date: push to next billing cycle (≤30 days) | CSM | YES | Purely administrative if account requests more lead time |
| **2 — Manager/council** | Extended ramp: 3–6 month phase-in with council sign-off | Manager + pricing council | NO — not applicable | N/A |
| **2 — Manager/council** | One-time bridge credit against first invoice | Manager + pricing council | NO — not applicable | N/A |
| **3 — CEO only** | Annual commitment at new rate ($1,295/month locked) | CEO | YES — appropriate if account requests price certainty | Locks revenue at the new lower rate |
| **3 — CEO only** | Subscription discount: max 10%, max 12 months | CEO | NO | Already below the peer midpoint; further discount not warranted |
| **NEVER** | Hold at current rate indefinitely | Not available | **NO** | Undermines install base standardization |

**25% uplift guardrail check:** Delta is –$120/month (a decrease). Annual delta = –$1,440. No guardrail applies — this is not a price increase.

---

## Churn Risk Assessment

| Signal | Status |
|---|---|
| Health band | Healthy |
| Health trend | Stable (single run on file — no prior run to compute delta) |
| Open support issues | NO (support_fire = False) |
| CSM confidence | Unknown — confirm before outreach |
| Competitor known | NO |
| Contract renewal proximity | Monthly rolling — no fixed renewal risk window |
| Churn risk label | LOW — price is decreasing; no financial friction on this migration |

**Note:** The platform utilization pattern (5% rep login rate, zero B2B Cart/catalog traffic) is worth monitoring as a medium-term retention signal. If the account isn't extracting value from the B2B Cart and catalog modules — despite having them configured — they may eventually question the tier value. This is a CS engagement priority separate from the pricing migration.

---

## Expansion Notes

Expansion brief type: t2_to_t3
Expansion eligible: YES — after positive migration signal

**GATED: Do not generate or present a Format C T2→T3 brief in this run.** Per run instructions, the expansion brief for gc is gated until migration acceptance is confirmed. Queue for follow-up outreach 14 days post-migration confirmation with no objection.

Pre-expansion context:
- gc has all three T2 surfaces configured (iPad, catalog, B2B Cart), making T3's Sales Portal and insights layer a natural next step if buyer-side activation improves. At current utilization levels, the T3 value proposition is harder to land — wait for the B2B Cart and catalog to show organic activity before opening the expansion conversation.

---

## Internal Notes

*CSM: add anything else the CEO should know before this call — relationship nuance, recent support history, known sensitivities, open renewal discussion, etc.*

- Contract signatory not confirmed — obtain before delivering the brief.
- Multifile Import feed is 33 days overdue (critical). Recommend CS outreach to investigate feed configuration before or alongside pricing brief delivery — a data integrity issue surfacing after the pricing notice could create unrelated friction.
- B2B Cart has zero order activity in 90 days despite being enabled. If the account asks about T2 value, route to a platform activation session rather than a pricing concession.

---

*Internal prep sheet | Prepared May 18, 2026 | Paired with client-facing brief: gc_format-a_2026-05-18.md*
