# Internal Intelligence Brief — Fine Art Handcrafted Lighting

*2026-04-20 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Fine Art Handcrafted Lighting is an account that demands intervention despite strong underlying adoption. The platform is deeply used — perfect feature adoption (100/100), $38.1M in trailing iPad GMV, and 42% GMV growth momentum — but two structural issues are dragging Health to 58 (Watch): critically stale configuration data (255 days untouched, driving Operational Health to 30) and a severe Q/Q activity decline (Trajectory at 10). The meeting should be defensive — resolve the stale data, understand why platform activity is declining (including key rep Jim Coyle's complete disengagement at $3.1M annual risk), and address $3.2M at risk from seven decelerating customer accounts.

**Three Things That Matter:**

1. **Trajectory is critically low at 10** — Platform activity has declined sharply quarter-over-quarter, with both presentation actions and login volume falling. This aligns with key rep disengagement (Jim Coyle, $3.1M LTM, dropped to zero orders and zero logins) and seven customer accounts decelerating past their normal reorder cycles.
2. **255-day stale data is the most fixable issue** — 11 data entities (matrix options, placement reports, customer favorites) haven't been refreshed since August 2025. Reps are actively using these features with outdated information. Refreshing this data would immediately lift Operational Health from 30 toward the Healthy range.
3. **$3.2M customer deceleration risk needs a response ready** — Seven high-frequency accounts including Howard Design Group ($1.9M, 3× overdue) and Fine Art Lamps Accommodation ($489K, 13× overdue) have blown past their normal reorder cycles. The external report will surface this — the team should walk in with a plan.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 58/100 | Intervene |
| **Band** | Watch | Immediate action cadence |

> Fine Art Handcrafted Lighting (iPad-only) scores 58 Health → Intervene. Trajectory (10) is critically low; immediate attention required.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 60 | Healthy | Login frequency and active user ratio meet the Healthy threshold. The team has 26 qualifying reps and meaningful login volume, though Q/Q logins are declining (see Trajectory). |
| Adoption (20%) | 100 | Thriving | Perfect score — all 7 features available for the iPad-only bundle are used above minimum thresholds: product search, customer selection, presentations, email sharing, PDF catalogs, document viewing, and stacks/lists. This leads the peer group. |
| Value Delivery (30%) | 60 | Healthy | For iPad-only bundles, Value Delivery measures presentation tool usage (email drafting, PDF catalogs, document sharing). A score of 60 indicates moderate but not strong presentation volume in the trailing 90 days — the team closes deals through relationship selling more than digital sharing tools. |
| Operational Health (15%) | 30 | At Risk | The lowest dimension by far. The external report identifies 11 data entities stale for 255 days (since August 2025), including matrix options and placement reports. With days_since_critical_update well past 180, the data freshness sub-component scores zero. This is the primary drag on Operational Health. |
| Trajectory (10%) | 10 | Critical | Severe Q/Q decline. Both presentation actions (the primary value metric for iPad-only) and login volume have dropped sharply versus the prior quarter. Key contributors: Jim Coyle ($3.1M LTM) went from 30 orders to zero; multiple high-frequency accounts decelerated significantly. |

### Flags

- **Warning — hs_lifecycle_stale**: HubSpot lifecycle status shows "Lost" or "Churn" despite an active subscription in Postgres. This is a data hygiene issue — the HubSpot record lags operational reality. Does not affect scoring but should be corrected.
- No churn risk modifier fired.
- No risk modifier applied.

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Fine Art Handcrafted Lighting's bundle (iPad-only), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measured by login frequency per active user and active user ratio.
- **Adoption (20%)** — How many available features are being used above minimum thresholds? For iPad-only, 7 features apply: product search, customer selection, presentations, email sharing, PDF catalogs, document viewing, and stacks/lists.
- **Value Delivery (30%)** — Is the platform generating business value? For iPad-only bundles, this measures **presentation tool usage** — email drafting, PDF catalog creation, and document sharing. This is the heaviest-weighted dimension.
- **Operational Health (15%)** — Is client data clean and current? Import success rate, catalog completeness (products with images and prices), and data freshness (days since last update to products, customers, or inventory).
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares presentation actions and login volume against the prior 90-day period.

**Health Bands**: Thriving (80–100), Healthy (60–79), Watch (40–59), At Risk (20–39), Critical (0–19).

**Classification** determines the recommended action cadence:
- **Expand** — Healthy account with strong expansion signals
- **Maintain** — Healthy, protect with standard cadence
- **Stabilize First** — Needs health improvement before expansion
- **Intervene** — Immediate save/recovery plan needed

</details>

---

## Support & Issue Themes

> 3 conversations in 90 days. Low-volume, routine requests across unrelated topics. No active fires.

### Themes

With only 3 conversations — each tagged to a different type — there is no recurring support pattern. The volume is minimal and the issues are diverse:

**1. Admin & data configuration** (2 tickets)
- "Re: Displaying 'Terms' Field on Customer Card in eCat" (training, admin console)
- "Re: Product images missing on recent eCat POs" (image asset, admin console)
- **Impact**: Routine admin questions that don't signal deeper problems. The image issue may relate to the broader stale data theme identified in the external report.
- **Root**: Standard operational questions from an org that manages its own admin console.
- **Action**: No proactive action required. If the image issue recurs, connect it to the stale data refresh recommendation.

**2. eCat Online inquiry** (1 ticket)
- "Question Regarding eCat Online" (sales and finance, product-eol)
- **Impact**: Single inquiry about eCat Online from an iPad-only customer. May signal interest in expanding their bundle.
- **Root**: Exploring a product outside their current bundle.
- **Action**: Worth noting in the meeting — if FAL is asking about eCat Online, there may be a natural conversation about upgrading from iPad-only.

### Escalation Profile

2 L1, 1 L2. All S4 (low severity). No L3/L4 escalations. No executive involvement. The support relationship is quiet and healthy.

### Open Tickets (0)

No open tickets. All conversations are closed.

---

## Active Engineering & Projects

No active Jira tickets found for this client.

**Search strategies attempted:**
1. `text ~ "Fine Art Handcrafted Lighting" AND statusCategory != Done` → 0 results
2. `text ~ "fal" AND statusCategory != Done` → 0 results
3. `text ~ "Fine Art" AND statusCategory != Done` → 0 results

No HelpScout conversations tagged `status: logged on jira`.

---

## Meeting Playbook

### Talking Points

1. **Stale data is the easiest win** — External report highlights 11 data entities stale for 255 days (matrix options, placement reports, customer favorites). Internally, this drags Operational Health to 30 (At Risk). Prepare to explain what a configuration data refresh involves and timeline to resolve. This is the single most impactful action item.
2. **Trajectory decline aligns with rep disengagement** — External report will surface Jim Coyle's complete disengagement ($3.1M annual, zero activity current quarter) and seven decelerating customer accounts ($3.2M at risk). Internally, Trajectory scores 10 (Critical), confirming the platform usage drop is real and broad. The meeting should explore whether this reflects a seasonal pattern, competitive pressure, or operational change.
3. **Perfect adoption is a genuine bright spot** — External report highlights a 100/100 adoption score that leads the peer group. Internally, this means all 7 iPad-only features clear their minimum thresholds. Use this as a "the platform works, the team uses it" anchor when discussing the operational issues that need fixing.

### Not in the External Report

- **Health score: 58/100 (Watch band)** — Internal metric, not shared with client
- **Classification: Intervene** — Immediate action cadence recommended; driven by low trajectory and operational health
- **Trajectory score: 10 (Critical)** — The most alarming single dimension; represents severe Q/Q decline in both presentations and logins
- **Warning flag: hs_lifecycle_stale** — HubSpot shows this account as "Lost" or "Churn" despite active subscription; a data hygiene backlog item
- **Support history: quiet** — 3 low-severity conversations in 90 days, all resolved, no patterns of concern

### SuperCat Action Items

- [ ] **Refresh stale configuration data** — 11 entities at 255 days are driving Operational Health to 30. This is the highest-leverage fix.
- [ ] **Enable Clicky Analytics** — `has_clicky_portal = false`. Enable for portal traffic intelligence, even though FAL is iPad-only today.
- [ ] **Correct HubSpot lifecycle status** — `hs_lifecycle_stale = true`. Update HubSpot to reflect active subscription status.
