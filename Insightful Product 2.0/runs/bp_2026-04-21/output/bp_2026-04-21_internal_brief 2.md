# Internal Intelligence Brief — Buster & Punch

*2026-04-21 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Buster & Punch is an underperforming iPad-only account in Intervene mode. Health is 41 (Watch band) driven by critically low Value Delivery (20) — the presentation workflow that defines success for their bundle is barely being used. The team is logging in near peer-median levels, so the problem is not engagement but conversion: sessions aren't translating to productive selling activity. Two high-priority Jira bugs have been stale for 9–12 months, and catalog completeness sits at 45%. The meeting should be defense-first: establish a concrete plan to activate presentation tools and address data quality before discussing growth.

**Three Things That Matter:**

1. **Value Delivery is critically low at 20** — Presentation tools (email, PDF, sharing) define the iPad-only value metric, and usage is near-zero in 90 days. This is the single biggest drag on health and the most actionable lever for improvement.
2. **Two high-priority bugs stale for 9+ months** — ECAT-1272 (placements UI bug, 276 days untouched) and SERV-2068 (product rendering crash, 371 days) are both High priority and sitting in To Do. If the product crash affects this client's workflow, it could directly explain low presentation usage.
3. **Catalog completeness at 45% undermines operational health** — 1,226 products lack pricing data, dragging Operational Health to 36. A bulk pricing feed update is the single highest-leverage data fix and would improve both the catalog experience and health score.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 41/100 | Intervene |
| **Band** | Watch | Immediate improvement plan needed |

> Buster & Punch (iPad-only) scores 41 Health → Intervene. Value Delivery (20) is critically low; immediate attention required.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 60 | 🟢 Healthy | Login activity is competitive — 2,411 total logins across 48 active users sits only 6.5% below the peer median. The team is present and using the platform regularly. The engagement base does not need a ramp-up; the gap is in what happens after login. |
| Adoption (20%) | 57 | 🟡 Watch | For the iPad-only bundle, 7 features are available (Product Search, Customer Selection, Presentations, Email Sharing, PDF Catalogs, Document Viewing, Stacks/Lists). At 57, roughly 4 of 7 features exceed minimum thresholds. Product Search (2,244 events) and Customer Selection (1,586) dominate; presentation tools (email sharing, PDF catalogs) and document viewing are likely underused. |
| Value Delivery (30%) | 20 | 🔴 At Risk | For iPad-only bundles, Value Delivery = presentation_score. A score of 20 means presentation actions (magic button adds, emails drafted, PDF catalogs, document emails) are above zero but below 50 total in 90 days. The core selling workflow that drives value on an iPad-only bundle is barely being used. |
| Operational Health (15%) | 36 | 🔴 At Risk | The import pipeline runs daily (414 imports over 7 months; customers and inventory are fresh at 0 days). However, catalog completeness is only 45.2% (1,226 products missing pricing) and 11 entities have been stale since Aug 2025 (256 days). Stale entities and low catalog completeness drag the score well below the Watch threshold. |
| Trajectory (10%) | 30 | 🔴 At Risk | Q/Q trend is declining. The primary value metric for iPad-only (presentation_actions) and login activity both show negative momentum vs. the prior quarter. Q1 2026 ordering showed a slight uptick (3 orders, $24K), but the presentation workflow has not recovered. |

### Flags

- **No churn risk** — no risk modifiers fired despite low health score
- **No risk modifier applied**
- ⚠️ **hs_lifecycle_stale** — HubSpot lifecycle status is stale (shows Lost/Churn or no status), but the org has an active subscription. This is a data hygiene issue, not a scoring blocker.
- ⚠️ **hs_join_missing** — No HubSpot join exists for this org. Vertical and lifecycle data unavailable for peer benchmarking (falls to bundle-only cohort).

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Buster & Punch's bundle (iPad-only), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform?
- **Adoption (20%)** — How many of the 7 available features are being used above minimum thresholds?
- **Value Delivery (30%)** — Is the platform generating business value? For iPad-only bundles, this measures **presentation tool usage** — email drafts, PDF catalogs, magic button adds, and document sharing. This is the heaviest-weighted dimension because it directly measures whether reps are using eCat to sell.
- **Operational Health (15%)** — Is client data clean and current? Import success, catalog completeness, data freshness.
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter?

**Classification** determines the recommended action cadence:
- **Expand** — healthy account with strong expansion signals
- **Maintain** — healthy, protect with standard cadence
- **Stabilize First** — needs health improvement before expansion
- **Intervene** — immediate save/recovery plan needed

Buster & Punch is classified **Intervene** — both health (41) and growth signals are below the 60 threshold, requiring an immediate improvement plan focused on activating the presentation workflow and fixing data quality.

</details>

---

## Support & Issue Themes

> 3 conversations in 90 days. User management-forward, minimal volume, all routine. No active fires.

### Themes

**1. User Management & Onboarding** (2 tickets)

- "Ecat invitation clarification" (Mar 6), "Re: new eCat users" (Feb 4)
- **Impact**: Both conversations relate to setting up new users through the admin console — a positive signal that the client is actively expanding their eCat user base, but needs hand-holding through the process.
- **Root**: The admin console user management workflow may not be self-service enough; also possible the team lacks a designated admin champion who owns onboarding.
- **Action**: Proactively provide a user management walkthrough or quick-start guide for the admin console. Identify whether there's a single admin owner.

**2. Feature Inquiry — eCat Online** (1 ticket)

- "Re: eCat online" (Jan 26)
- **Impact**: The client asked about eCat Online capabilities — potential interest in expanding beyond iPad-only. Their bundle currently excludes eCat Online as a full product, though the catalog site exists.
- **Root**: Current iPad-only bundle limits functionality. The client may be exploring whether they need the Catalog bundle. The external report confirms eCat Online is configured but has 0 server orders.
- **Action**: Use this as an opening in the meeting to discuss eCat Online capabilities and a potential bundle upgrade.

### Escalation Profile

3 L1, 0 L2+. Peak severity: S4 (low). All handled by frontline support with no escalations. The support relationship is low-touch and routine.

### Open Tickets (0)

No open support tickets. All conversations resolved.

---

## Active Engineering & Projects

2 open Jira tickets found for Buster & Punch. Both are High-priority bugs in To Do status, and both are severely stale.

| Key | Summary | Project | Status | Priority | Assignee | Age (days) | Days Since Update |
|---|---|---|---|---|---|---|---|
| [ECAT-1272](https://supercatsolutions.atlassian.net/browse/ECAT-1272) | Placements button showing even when there are no showroom locations | eCat | To Do | High | Unassigned | 429 | 276 |
| [SERV-2068](https://supercatsolutions.atlassian.net/browse/SERV-2068) | Crash rendering product | Server | To Do | High | Brent Sanders | 436 | 371 |

**Flags:**
- 🔴 **STALE**: Both tickets have had no update in 14+ days — ECAT-1272 at 276 days, SERV-2068 at 371 days. These are effectively abandoned.
- 🔴 **HIGH PRIORITY**: Both tickets are High priority bugs that have never left To Do.
- ⚠️ **UNASSIGNED**: ECAT-1272 has no assignee.

**Cross-Surface Links:**
- SERV-2068 ("Crash rendering product") may directly relate to the low Value Delivery score (20). If product rendering crashes affect this client's catalog, it could impair the presentation workflow that drives their iPad-only value metric. Worth confirming whether this crash still reproduces in their environment.
- No HelpScout tickets tagged `status: logged on jira` — these bugs were not surfaced through the support channel.

---

## Meeting Playbook

### Talking Points

1. **Presentation tools are the path to value** — External report highlights $36K GMV on just 9 iPad orders with only 7 active buyers. Internally, Value Delivery scores 20 because the presentation workflow (email, PDF, sharing) is critically underused. The meeting should center on activating these tools as the first step to expanding the active buyer base and increasing order volume.
2. **Login-to-order conversion is the gap, not engagement** — External report shows login activity near the peer median (2,411 vs. 2,578) but order volume in the bottom 25% of peers (66 vs. peer median 245). Internally, Engagement is 60 (Healthy) while Trajectory is 30 (declining). The team shows up — they just aren't converting sessions into selling activity.
3. **Data quality has a concrete fix** — External report flags catalog completeness at 45.2% with 1,226 products missing pricing. Internally, this drags Operational Health to 36. A bulk pricing feed update is the single highest-leverage data fix and a SuperCat action item we should prepare to walk through.

### Not in the External Report

- **Health score 41 (Watch band) and Classification Intervene** — immediate improvement plan needed; not client-facing
- **No churn risk flagged** despite low health — no risk modifiers fired; the account is underperforming but not at the emergency threshold
- **Warning flags: hs_lifecycle_stale, hs_join_missing** — HubSpot data hygiene issues; the org has no HubSpot join and a stale lifecycle status. Does not affect scoring but limits our CRM visibility.
- **Support pattern is actually positive** — all 3 recent conversations are user management / onboarding requests, suggesting the team is actively expanding eCat usage
- **Two high-priority Jira bugs (ECAT-1272, SERV-2068) stale for 9–12 months** — neither has been triaged or actioned; the product rendering crash (SERV-2068) could be impacting this client's workflow

### SuperCat Action Items

- [ ] **Enable Clicky Analytics** — `has_clicky_portal = false`. Enable portal traffic intelligence to measure eCat Online engagement.
- [ ] **Refresh stale configuration data** — 11 entities frozen since Aug 2025 (256 days). Products, categories, collections, groups, trade names, and smart stacks all need a refresh cycle.
- [ ] **Update or close stale Jira tickets** — ECAT-1272 (276 days, unassigned) and SERV-2068 (371 days) are both High priority bugs in To Do. Triage before the meeting: still relevant? Still reproducing? Confirm SERV-2068 doesn't affect this client's product rendering.
- [ ] **Address catalog completeness** — Coordinate a bulk pricing feed update for the 1,226 products missing price data. This is the single highest-leverage data fix for Operational Health.
