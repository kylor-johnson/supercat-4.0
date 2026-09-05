# Account Scoring Framework — Two-Lens Model

**Version:** 3.0 | **Date:** February 26, 2026
**v3.0 changelog:** Fathom absence protocol: Fathom inputs are N/A when no data exists (weight redistributes), not scored as zero or penalized. Fathom cessation (meetings were happening, then stopped) remains a cooling signal. HelpScout silence reframed: only a risk signal when it represents a deviation from the account's established historical pattern. Self-sufficient, well-implemented clients are not penalized for low ticket volume.
**v2.0 changelog:** Post-Crystorama test run fixes. Added third use-case profile (Non-Ordering + Pushed Data) with hybrid Business Impact scoring at 50% order weight. Defined canonical Active User metric (Mixpanel distinct users ≥1 event, excluding admin usernames). Added billing model detection fallback hierarchy. Updated insufficient data handling guidance.

---

## Why Two Scores, Not One

A single composite health score compresses away the most important insight: whether an account needs investment or intervention — or both. An account that's simultaneously a strong expansion candidate AND showing churn signals gets a "medium" composite score, indistinguishable from a quiet, stable, low-value account. That ambiguity is where the biggest mistakes happen.

Two independent scores solve this:

- **Expansion Readiness Score** — How much growth potential does this account have, and how ready are they for that conversation?
- **Retention Risk Score** — How likely is this account to churn or contract in the next 90 days?

These are not inversely correlated. An account can be high on both, low on both, or any combination.

---

## The Quadrant

|  | **Low Retention Risk** | **High Retention Risk** |
|---|---|---|
| **High Expansion Readiness** | **GROW** — Ideal accounts for EBR with expansion agenda. Template A (Discovery-Led) or Template C (Benchmark-Forward). | **SAVE & GROW** — High potential but something's wrong. Fix the risk factor first, then expand. Template B (Intelligence-Led). |
| **Low Expansion Readiness** | **MAINTAIN** — Stable, limited upside. Light-touch engagement, data-driven touchpoints. Tier 3 cadence. | **INTERVENE** — At-risk and not embedded deeply enough to weather the storm. Retention conversation, not an EBR. |

Each quadrant maps to a different engagement strategy, EBR template approach, and urgency level.

---

## Architecture Context

This scoring model is designed to be **promptable** — executable by anyone on the team via Cursor with MCP access to:

- **BigQuery** (WELD_RAW) — 166 tables across HelpScout, HubSpot, Mixpanel, Stripe, QuickBooks, Fathom, Jira
- **PostgreSQL** (SuperCat Production) — 108 tables with live org, user, product, order, subscription, territory, and audit data

Every component input maps to a specific data source, table, and query logic. The scoring model serves as the analytical backbone of the prompt — it tells Cursor exactly what to query, how to weight it, and what the output means.

### Key Architectural Decisions

- **Use-case profile detection (three profiles):** Before scoring, the prompt must determine the account's use-case profile:
  - **Ordering:** Submit Order events exist in Mixpanel → full transactional Business Impact scoring.
  - **Non-Ordering:** Zero Submit Order events AND zero orders in PostgreSQL → Business Impact scores on buyer-facing actions only (emails drafted, PDFs, library shares, customer product lists).
  - **Non-Ordering + Pushed Data:** Zero Submit Order events in Mixpanel BUT orders exist in PostgreSQL from ERP imports → hybrid Business Impact scoring. All non-ordering inputs PLUS pushed order volume trend, pushed revenue trend, and pushed AOV weighted at 50% of their ordering-client value. The platform is central to the order-to-cash workflow even though reps don't use the transactional Submit Order feature.
- **Canonical Active User definition:** Active User = distinct Mixpanel usernames with ≥1 event in the measurement period, excluding SuperCat admin/test usernames. This is the single definition used across all scoring components and brief sections. PostgreSQL `authenticated_sessions` and HubSpot active user counts may be referenced for context but are NOT the canonical measure. Active User Ratio = Mixpanel active users / billable users (from HubSpot or PostgreSQL `org_users`).
- **Billing model detection:** Not all accounts have Stripe subscriptions. Fallback hierarchy: Stripe subscription → Stripe invoice → QuickBooks invoice → PostgreSQL subscriptions.
- **Source selection:** Postgres for real-time signals (last login, current subscription status, territory config, import health). BigQuery for trended analysis (Mixpanel event history, HelpScout ticket patterns, Fathom meeting cadence, Stripe payment history).
- **Insufficient data handling:** For any component where data is absent or too thin (<30 days of history, no Fathom meetings recorded, no HelpScout tickets ever), score as "N/A — insufficient data" and redistribute weight to remaining components. New accounts should not auto-flag as at-risk due to data absence.

---

## Score 1: Expansion Readiness

Answers: **Should we invest more in this account?**

This score is HIGH when the account is deeply engaged, using the platform well, has untapped modules or features, and shows signals of growing need.

### Components

#### Adoption Depth — 30%

What it measures: How deeply and broadly the account uses the platform. Deeper adoption = more trust = more receptive to expansion. Low Subscription Completeness with high engagement = whitespace opportunity.

**Inputs:**
- Activity Ladder aggregate score (org-level) — Mixpanel events in BigQuery
- Feature Breadth Score (distinct features used across the org) — Mixpanel events
- Subscription Completeness (products enabled / total suite) — Stripe `subscription` + Admin Console
- Active User Ratio — Postgres `org_users` + `authenticated_sessions`

#### Business Impact — 25%

What it measures: Is the platform driving measurable value for their business? High impact = easier expansion conversation.

**Inputs (ordering clients):**
- Order volume trend (MoM direction) — Postgres `orders` or BigQuery Mixpanel `Submit Order`
- AOV and AOV trend — Admin Orders Report / Postgres `orders`
- Customer Activation Rate — Postgres `customers` with orders / total customers
- Digital Self-Service Rate (eCat Online orders / total) — Mixpanel

**Inputs (non-ordering clients):**
- Buyer-facing email events: `Email Item Info`, `item_email_drafted`, `document_email_drafted` — Mixpanel
- PDF Catalog creation volume and trend — Mixpanel
- Library Entry sharing (single + multi email) — Mixpanel
- Customer Product List creation — Mixpanel
- Trend direction on all buyer-facing actions (MoM) — Mixpanel

**Inputs (non-ordering + pushed data clients):**
- ALL non-ordering inputs above, PLUS:
- Pushed order volume trend (MoM) — PostgreSQL `orders` or `import_events`
- Pushed revenue trend (MoM) — PostgreSQL `orders`
- Pushed AOV — PostgreSQL `orders`
- Import cadence (frequency and recency of ERP data pushes) — PostgreSQL `import_events`
- Pushed order metrics are weighted at 50% of their ordering-client value in the component score. Rationale: the platform is central to order-to-cash (data flows through it), but reps don't use the transactional order submission workflow, so transactional engagement is lower.

#### Growth Signals — 25%

What it measures: Active indicators that the account is growing or has expressed needs that map to unadopted capabilities.

**Inputs:**
- User Growth Trend (MoM user count change) — Postgres `org_users`
- Growing MAU — Mixpanel events
- New territories configured — Postgres `territories`
- Expansion Signals triggered from metrics framework Section 14 — cross-source
- Fathom pain themes that map to unused features — BigQuery `fathom__sales_meetings_from_fathom_hubspot`
- HubSpot expansion deals open — BigQuery `hubspot__deal`

#### Relationship Strength — 20%

What it measures: Is the relationship strong enough to support an expansion conversation? If we can't get a meeting, we can't expand regardless of the data.

**Inputs:**
- Fathom meeting cadence (rolling 90d) — BigQuery `fathom__ai_summaries` — **N/A if no Fathom data exists; weight redistributes to remaining inputs. Fathom absence is not a penalty — it's an operational callout.**
- Days since last meaningful interaction — Fathom + HelpScout
- Stakeholder engagement breadth (distinct contacts across Fathom + HelpScout) — cross-source
- HelpScout ticket responsiveness — are they engaged when they have issues? `helpscout__help_scout_tickets` → `ticket_customer_waiting_secs`, ticket resolution patterns
- HelpScout onboarding ticket activity (for newer accounts) — positive signal of investment in the platform

### Interpretation

- **80–100 — Active Expansion Target.** Build the business case, schedule the EBR, bring the recommendation.
- **60–79 — Nurture.** Foundation is there but something's missing — either relationship isn't deep enough or adoption hasn't hit the tipping point. Focus on enablement first.
- **Below 60 — Not Ready.** Engagement too shallow, business impact unproven, or relationship hasn't matured. Expansion push would feel premature.

---

## Score 2: Retention Risk

Answers: **Are we about to lose this account?**

This score is HIGH (meaning high risk) when signals point to potential churn or contraction.

### Components

#### Engagement Decline — 30%

What it measures: The single strongest churn predictor in monthly billing SaaS. If usage is declining, everything else is secondary.

**Inputs:**
- MAU trend — 3+ consecutive months of decline is a strong signal — Mixpanel events
- Login frequency trend (declining) — Postgres `login_events` or Mixpanel
- Active User Ratio drop (MoM comparison) — Postgres `org_users` + `authenticated_sessions`
- User count decrease — Postgres `org_users`

#### Relationship Cooling — 25%

What it measures: The relationship is fading or souring. Combines proactive signals (Fathom — are we talking to them?) with reactive signals (HelpScout — are they reaching out to us?).

**Inputs (Fathom):**
- Days since last meeting (increasing gap) — BigQuery `fathom__ai_summaries` — **N/A if no Fathom data exists; weight redistributes to HelpScout inputs. Fathom absence alone is not a cooling signal. Fathom CESSATION (meetings were happening, then stopped) IS a cooling signal.**
- Missed or cancelled meetings — Fathom + HubSpot engagement data
- Competitor mentions in recent calls — BigQuery `fathom__sales_meetings_from_fathom_hubspot`
- Negative pain themes or objections trending — BigQuery `fathom__sales_meetings_from_fathom_hubspot`

**Inputs (HelpScout):**
- Ticket pattern change from established cadence (a client averaging 3 tickets/month that goes silent for 90 days is a signal; a client that rarely submits tickets and continues not submitting is normal) — BigQuery `helpscout__help_scout_tickets`
- Unresolved tickets with high customer wait time — `ticket_customer_waiting_secs`
- Rising ticket volume from mature account (friction signal) — ticket count trend
- Tag-based sentiment: billing/cancellation-related tags vs. how-to/onboarding tags — `ticket_tags`
- Thread depth (high back-and-forth per ticket = poor resolution quality) — BigQuery `helpscout__conversation_threads`

#### Financial Distress — 25%

What it measures: Money signals are binary and high-impact. An account that stops paying is leaving.

**Inputs:**
- Payment Status (current / overdue) — Stripe `invoice`, `charge`
- Invoice Aging (days outstanding, bucketed) — QuickBooks `invoice`
- MRR contraction (subscription downgrades) — Stripe `subscription` history
- For ordering clients: declining order revenue trend — Admin Orders Report / Postgres `orders`

#### Operational Deterioration — 20%

What it measures: The platform is becoming less reliable or less maintained for this client. Could be cause or symptom of disengagement.

**Inputs:**
- Data freshness declining (days since last product/customer/inventory import) — Postgres `import_events`
- Import error rate rising — Postgres `import_events`
- Rising support ticket volume on repeated issues (Repeat Issue Rate) — BigQuery `helpscout__help_scout_tickets` with tag analysis
- Stale inventory (last update >7 days) — Postgres `inventories` or `import_events`

### Interpretation

- **Below 30 — Low Risk.** Stable across all dimensions. Monitor normally.
- **30–50 — Watch.** One or two signals flagging. Investigate specific components to determine if it's noise (seasonal dip, market week) or a real trend.
- **50–70 — Elevated Risk.** Multiple components signaling concern. Proactive outreach within 2 weeks. Do not wait for next scheduled touchpoint.
- **Above 70 — Critical Risk.** Immediate intervention. This account needs a retention plan, not an EBR.

---

## Weight Validation Strategy

All weights are informed assumptions, not empirically calibrated. They should be treated as a starting framework.

**Validation approach:**
1. Run the model across all 129 active accounts
2. Compare computed quadrant placement against team intuition — do the placements feel right?
3. Identify misclassified accounts and diagnose which component(s) drove the wrong signal
4. Adjust weights based on pattern analysis
5. After 6–12 months, backtest against actual churn and expansion events to derive empirical weights
6. Re-calibrate quarterly

The Cursor/MCP architecture makes this feedback loop fast — re-running the model with adjusted weights is essentially a prompt modification, not a rebuild.

---

## Next Deliverable: Query Specification

The bridge document between this scoring framework (what to measure) and the Cursor prompt (how to compute it). For each component input, the query spec will define:

- Exact data source (BigQuery table or Postgres table)
- Fields to query
- Aggregation logic
- Time window
- Threshold values
- Non-ordering client alternative (where applicable)
- Insufficient data handling

This makes the scoring model fully promptable and reproducible by any team member.
