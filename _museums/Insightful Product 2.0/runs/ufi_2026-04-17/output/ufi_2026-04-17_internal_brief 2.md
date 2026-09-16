# Internal Intelligence Brief — Universal Furniture

*2026-04-17 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Universal Furniture is a healthy, deeply adopted account in standard-cadence Maintain mode. Platform health is Thriving at 81 with perfect adoption across all 9 bundle features, strong presentation and portal engagement, and only 8 low-severity support conversations in 90 days. The single area of concern is Trajectory — at 10/100 (Critical), both value delivery and login activity have declined sharply quarter-over-quarter. No fires. The meeting should be offensive: dormant account reactivation ($631K opportunity from the external report), stale price data refresh, and understanding whether the trajectory dip is seasonal or structural.

**Three Things That Matter:**

1. **Trajectory decline demands monitoring** — Despite an overall Thriving health score of 81, the Trajectory dimension is Critical at 10/100. Both platform activity and login trends have declined significantly Q/Q. This is the only internal signal that breaks the otherwise clean picture and should be tracked for sustained deceleration.
2. **$631K dormant reactivation is the top talking point** — The external report identifies 5 dormant accounts (Compass Interiors, Furniture Warehouse Sales, Birmingham Wholesale, Colorado Country Style, Gregorie Douglas) totaling $631K in prior eCat orders. With the account healthy and no fires, this is the highest-value conversation topic.
3. **205-day stale price data is a quick win** — Refreshing price level data would resolve the external report's catalog completeness benchmark gap and lift Operational Health from 70 (Healthy) into the Thriving range by fixing the data freshness sub-component.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 81/100 | Maintain |
| **Band** | Thriving | |

> Universal Furniture (iPad+Catalog+Portal) scores 81 Health → Maintain. Adoption (100) leads health; stable with standard cadence.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 90 | Thriving | Strong login activity with high active user participation. Both login intensity and active user ratio are in the top tier — the team is regularly and broadly using the platform. |
| Adoption (20%) | 100 | Thriving | Perfect score — all 9 available features for the iPad+Catalog+Portal bundle are actively used above minimum thresholds (Product Search, Customer Selection, Presentations, Email Sharing, PDF Catalogs, Document Viewing, Stacks/Lists, eCat Online, Sales Portal). |
| Value Delivery (30%) | 90 | Thriving | For iPad+Catalog+Portal bundles, VD = (presentation_score + portal_engagement_score) / 2. Both presentation tool usage and Sales Portal engagement score in the Thriving range, indicating the platform is generating real business value through both channels. |
| Operational Health (15%) | 70 | Healthy | Import health and catalog coverage are solid, but data freshness is the drag — critical configuration data (price levels) has not been updated in 205+ days, scoring 0 on the freshness sub-component and pulling Operational Health down from what would otherwise be Thriving. |
| Trajectory (10%) | 10 | Critical | Significant quarter-over-quarter decline in both the primary value metric (presentation activity + portal access average) and login activity. This is the lone critical dimension and the only red flag in an otherwise strong health profile. Monitor for sustained deceleration vs. seasonal dip. |

### Flags
- No risk modifiers fired. No churn risk. All warning flags clear (hs_lifecycle_stale: false, hs_join_missing: false, arr_data_gap: false).

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Universal Furniture's bundle (iPad+Catalog+Portal), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measures login intensity (logins per active user) and active user ratio (active users / total users).
- **Adoption (20%)** — How many available features are being used above minimum thresholds? For iPad+Catalog+Portal, 9 features are available (Product Search, Customer Selection, Presentations, Email Sharing, PDF Catalogs, Document Viewing, Stacks/Lists, eCat Online, Sales Portal).
- **Value Delivery (30%)** — Is the platform generating business value? For iPad+Catalog+Portal bundles, this measures the average of presentation tool usage (emails, PDFs, sharing) and Sales Portal engagement (portal access events).
- **Operational Health (15%)** — Is client data clean and current? Combines import success rate (50%), catalog completeness (30%), and data freshness (20%).
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares current 90-day primary value metric and login counts against the prior 90-day period.

**Classification** determines the recommended action cadence:
- **Expand** — healthy account with strong expansion signals
- **Maintain** — healthy, protect with standard cadence
- **Stabilize First** — needs health improvement before expansion
- **Intervene** — immediate save/recovery plan needed

</details>

---

## Support & Issue Themes

> 8 conversations in 90 days. Operational and admin-focused, low volume. No active fires.

### Themes

**1. Data Sync & Imports** (2 tickets)
- "Universal Furniture - Multi File Product Update" (L2, Admin Console)
- "file processing" (L1, Admin Console)
- **Impact**: Import workflows are the most complex support interaction for this client — the only L2 escalation in the period involved a multi-file product update requiring internal collaboration.
- **Root**: Multi-file product updates push beyond standard import patterns, requiring coordination between the client and internal teams.
- **Action**: Proactively check if their current import process is stable or if they need workflow simplification ahead of the next catalog update.

**2. Bugs & App Issues** (2 tickets)
- "FW: Ecat change" (L1, eCat, closed)
- "Question about NOTE on Sales Rep orders" (L1, eCat, pending 28 days — waiting on customer)
- **Impact**: Minor eCat behavior questions, both low severity. The pending ticket is 28 days old but in a customer-waiting state.
- **Root**: Normal operational questions about eCat order behavior and interface changes.
- **Action**: No immediate action required. The pending ticket is in the customer's court.

**3. User Management** (2 tickets)
- "Deleting Old Orders" (L1, eCat)
- "Add user already set up" (L1, Admin Console)
- **Impact**: Routine admin tasks — adding/removing users, cleaning up old data. No systemic issue.
- **Root**: Normal account maintenance by an active admin team.
- **Action**: No action required. Healthy self-service pattern.

*Note: 2 conversations were untagged — "Re: app crashing - URGENT" (closed, Apr 21) and "Re: Universal Furniture - Sales Data" (closed, Mar 11). The "app crashing" subject sounds urgent but was resolved and closed with 7 threads.*

### Escalation Profile
5 L1, 1 L2. All tagged severity is S4 (Low). No L3/L4 escalations. No S1/S2 high-severity issues. This is a low-friction, self-sufficient support profile.

### Open Tickets (0 active, 1 pending)

| Subject | Days Open | Severity | Level | State | Action? |
|---|---|---|---|---|---|
| Re: Question about "NOTE" on Sales Rep orders | 28 | S4 (Low) | L1 | CUSTOMER_WAITING | — |

No active (agent-needs-to-act) tickets. One pending ticket at 28 days, but the ball is in the customer's court. No tickets flagged for aging action.

---

## Active Engineering & Projects

One Jira ticket found related to Universal Furniture (search: `text ~ "Universal Furniture"`, `text ~ "ufi"`).

| Key | Summary | Project | Status | Priority | Assignee | Age (days) | Days Since Update |
|---|---|---|---|---|---|---|---|
| [SERV-2311](https://supercatsolutions.atlassian.net/browse/SERV-2311) | Thread-safety race condition in Warehouse table name resolution causes cross-org query errors | Server | Ready to Accept | Unprioritized | Bruce White | 33 | 5 |

**Flags:**
- No stale tickets (SERV-2311 was updated 5 days ago)
- No blocked tickets
- Priority is "Unprioritized" — may warrant reprioritization given it directly affects client portal reporting

**Context**: SERV-2311 is a platform-level bug where concurrent requests from different organizations can cause cross-org query errors in Warehouse (portal reporting) tables. The error trace explicitly references UFI — a request for another org (`clli`) erroneously included a `_ufi` table reference. This means Universal Furniture's portal reporting data could intermittently appear in other orgs' queries, and vice versa. A thread-local fix has been designed and the ticket is in "Ready to Accept" status.

**Cross-Surface Links:**
- No HelpScout tickets are tagged `status: logged on jira` for this client. The SERV-2311 bug may not have surfaced as a support complaint from UFI directly, but if the client reports portal data inconsistencies, this is the likely root cause.

---

## Meeting Playbook

### Talking Points
1. **External report flags $631K dormant reactivation** — Internally, the account is Thriving with no fires, making this a pure-upside conversation. Five dormant accounts (Compass Interiors, Furniture Warehouse Sales, Birmingham Wholesale, Colorado Country Style, Gregorie Douglas) went silent 90–176 days ago. Safe to lead the meeting with this opportunity.
2. **205-day stale price data bridges external and internal findings** — The external report highlights stale price levels affecting catalog completeness benchmarks. Internally, this same staleness drags the data freshness sub-component to 0 and holds Operational Health at 70 instead of Thriving. Refreshing this data is a quick win that improves both the client-visible metrics and internal health scoring.
3. **Trajectory decline is invisible to the client but critical to track** — The external report shows UFI leading peers in engagement, adoption, and value delivery. Internally, the Q/Q trajectory tells a different story: score of 10 (Critical). This disconnect between strong absolute positioning and sharp recent decline should inform how we frame the meeting — acknowledge the strength while probing for changes in team activity, seasonal patterns, or market shifts that explain the dip.

### Not in the External Report
- **Health score: 81/100 (Thriving)** — Classification: Maintain. Strong across 4 of 5 dimensions.
- **No churn risk.** No risk modifiers fired. All warning flags clear.
- **Not expansion-ready** — health is strong but near-term growth signals are moderate. Standard cadence is appropriate.
- **Support profile: 8 conversations / 90 days.** All low severity (S4), overwhelmingly L1. One L2 for a multi-file import. No fires, no patterns of concern.
- **Trajectory at 10/100 (Critical)** — The most concerning internal metric. Both platform activity and logins are declining Q/Q. Not yet triggering risk modifiers, but sustained deceleration would erode the Thriving score.
- **SERV-2311 race condition** — A platform bug directly involving UFI's Warehouse data. Fix is designed and in "Ready to Accept." If the client mentions portal reporting anomalies, this is the explanation.

### SuperCat Action Items
- [ ] **Refresh stale configuration data** — Price levels are 205+ days stale. This drags Operational Health and affects catalog completeness benchmarks in the external report. Coordinate with the client on a data refresh.
- [ ] **Monitor trajectory for sustained deceleration** — Set a 30-day checkpoint to re-evaluate whether the Q/Q activity decline is seasonal or structural. If trajectory remains Critical at next scoring, escalate to proactive outreach.
- [ ] **Track SERV-2311 resolution** — The Warehouse race condition directly references UFI data. Ensure the fix is deployed before the next portal reporting cycle and confirm no data integrity issues were surfaced.
- [ ] **Tag untagged support conversations** — 2 of 8 conversations in the period lack tags. Ensure the support team tags "Re: app crashing - URGENT" and "Universal Furniture - Sales Data" for accurate future trend analysis.
