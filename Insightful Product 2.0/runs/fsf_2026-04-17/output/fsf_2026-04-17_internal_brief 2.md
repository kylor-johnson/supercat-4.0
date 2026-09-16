# Internal Intelligence Brief — Four Seasons Furniture

*2026-04-17 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Four Seasons Furniture is a healthy, high-performing account running the Full bundle at $22,560 ARR. Platform value delivery is maxed out — perfect 100 across all four components — and adoption is deep at 90. The single drag on the health score is Engagement at 30 (At Risk), which reflects concentrated activity among fewer sessions rather than broad daily usage. There are zero support conversations in the last 180 days and no active fires. The meeting should be offense-oriented: close the engagement gap, push presentation tool adoption, and reactivate dormant accounts.

**Three Things That Matter:**

1. **Engagement at 30 is the only thing holding health back** — Despite a perfect Value Delivery score (100) and deep adoption (90), login frequency sits in the bottom quartile of peers. Improving per-rep login habits could push health from 75 into the mid-80s with no other changes.
2. **Zero support conversations in 180 days** — This account is entirely self-sufficient. No fires, no escalations, no open tickets. The meeting has zero defensive topics from the support side.
3. **Four stale Jira tickets need cleanup before the meeting** — Two High-priority items (ECAT-1014, EBR-353) and two enhancement requests are all 90+ days without an update. Address or close these to demonstrate responsiveness.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 75/100 | Maintain |
| **Band** | Healthy | |

> 75 Health → Maintain. Value Delivery (100) leads health; stable with standard cadence.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 30 | 🔴 At Risk | Login frequency and active user ratio are critically low. Peer benchmarking shows FSF in the bottom quartile for engagement despite leading on output metrics. High order volume is concentrated among fewer active sessions rather than broad daily platform usage. |
| Adoption (20%) | 90 | 🟢 Thriving | Using 9 of 10 available features for the Full bundle. All major capabilities are active — Product Search, Presentations, eCat Online, Order Submission, Sales Portal, Smart Stacks (5), Kit Items (223), and Library Resources (185). Only minor feature gaps remain. |
| Value Delivery (30%) | 100 | 🟢 Thriving | All four Full-bundle components are maxed: order volume (600–725 orders/month), customer activation (85.8% eCat retention across 435 active accounts), eCat Online share (87% of order volume), and portal engagement (125 daily visitors with 9+ minute sessions). |
| Operational Health (15%) | 94 | 🟢 Thriving | Import health is strong with regular data updates. Catalog completeness is high. Minor concern: kit item imports have a 133-day gap (last updated Dec 2025) while product and option data refresh daily. |
| Trajectory (10%) | 50 | 🟡 Watch | Q/Q trend is flat. Login activity and primary value metrics (orders) are holding steady but not accelerating relative to the prior quarter. eCat order volume grew 3× over the past 12 months, but recent quarters show stabilization. |

### Flags

No risk modifiers fired. No churn risk. All warning flags clear (hs_lifecycle_stale: false, hs_join_missing: false, arr_data_gap: false). No flags.

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Four Seasons Furniture's bundle (Full), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measured by login frequency per active user and active user ratio.
- **Adoption (20%)** — How many available features are being used above minimum thresholds? For the Full bundle, 10 features are tracked including Product Search, Presentations, eCat Online, Order Submission, and Sales Portal.
- **Value Delivery (30%)** — Is the platform generating business value? For Full bundles, this averages four components: order volume score, customer activation score, eCat Online share score, and portal engagement score.
- **Operational Health (15%)** — Is client data clean and current? Import success rate, catalog completeness (products with images and pricing), and data freshness (days since last critical update).
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares current 90-day metrics against the prior 90-day period.

**Classification** determines the recommended action cadence:
- **Expand** — healthy account with strong expansion signals
- **Maintain** — healthy, protect with standard cadence
- **Stabilize First** — needs health improvement before expansion
- **Intervene** — immediate save/recovery plan needed

</details>

---

## Support & Issue Themes

> 0 conversations in 180 days. Completely silent — no support contact of any kind. No active fires.

### Themes

No support themes to analyze. Four Seasons Furniture has had zero HelpScout conversations attributed to their corporate domain (4sfurniture.com) in the last 180 days. This is a self-sufficient account with no recent support needs.

### Escalation Profile

No escalations. Zero conversations means zero escalation or severity tags to report.

### Open Tickets (0)

No open support tickets.

---

## Active Engineering & Projects

4 open Jira tickets found across two projects. All are stale (no update in 14+ days). Two carry High priority.

### Recent / Active

| Key | Summary | Project | Status | Priority | Assignee | Age (days) | Days Since Update |
|---|---|---|---|---|---|---|---|
| [ECAT-1336](https://supercatsolutions.atlassian.net/browse/ECAT-1336) | Riser pricing not working for second option set | eCat | QA | Unprioritized | Brent Sanders | 217 | 91 ⚠️ |
| [ECAT-1014](https://supercatsolutions.atlassian.net/browse/ECAT-1014) | Sometimes option images do not display | eCat | To Do | **High** | Unassigned | 793 | 717 🔴 |
| [EBR-353](https://supercatsolutions.atlassian.net/browse/EBR-353) | eOL: Allow anonymous users to configure product | EBR | Triaging | **High** | chuck | 1,396 | 230 🔴 |
| [EBR-552](https://supercatsolutions.atlassian.net/browse/EBR-552) | Add one custom line to option selection | EBR | Triaging | Unprioritized | Unassigned | 778 | 230 ⚠️ |

### Flags

- 🔴 **Stale**: All 4 tickets have no update in 14+ days (range: 91–717 days since last update)
- 🔴 **High priority**: ECAT-1014 (option images not displaying) and EBR-353 (anonymous product configuration) are both High priority and stale
- **Unassigned**: ECAT-1014 and EBR-552 have no assignee

### Cross-Surface Links

- ECAT-1336 (riser pricing bug) relates to the product configuration workflow — the external report flagged that 197 new-introduction items have zero revenue, and pricing bugs could be a contributing factor for configuration-heavy product lines.
- EBR-353 (anonymous product configuration on eCat Online) connects to the external report's portal engagement findings — 125 daily visitors and strong session depth suggest buyer-facing catalog browsing is an active channel, making this enhancement request relevant to the portal experience.
- No HelpScout tickets tagged `status: logged on jira` — zero support conversations means no direct cross-link between support and engineering.

---

## Meeting Playbook

### Talking Points

1. **Presentation tool gap aligns with engagement deficit** — The external report highlights that only 2 of 10+ reps use presentation features consistently. Internally, this maps directly to the 30 Engagement score — reps produce strong orders but don't engage with discovery and sharing tools, which is why engagement lags despite near-perfect value delivery.
2. **$440K in dormant accounts is pure upside** — The external report flags 25 dormant high-value accounts representing ~$440K in historical eCat GMV. Internally, Value Delivery is already at 100, meaning reactivating these buyers adds revenue with no risk to the current health score.
3. **3× order growth validates the Full bundle investment** — The external report documents eCat orders growing from 185/month to 600–725/month with eCat Online now handling 87% of volume. Internally, this explains the perfect Value Delivery score and supports the case that FSF is getting full value from every product in their stack.

### Not in the External Report

- **Health score**: 75 (Healthy) with Maintain classification — account is in standard-cadence mode
- **Engagement is the single weak dimension** at 30 (At Risk), dragging the overall score 10+ points below its ceiling
- **No churn risk** — all flags clear, no risk modifiers fired, all warning signals negative
- **Zero support activity in 180 days** — entirely self-sufficient, no open tickets
- **Four stale Jira tickets** across ECAT and EBR projects, including two at High priority with no recent progress

### SuperCat Action Items

- [ ] **Update or close 4 stale Jira tickets** — All FSF-related tickets are 90+ days stale. ECAT-1014 and EBR-353 are High priority with 717 and 230 days since update respectively. Triage and either advance or formally deprioritize before the meeting.
- [ ] **Prepare engagement improvement recommendations** — The 30 Engagement score is the single biggest opportunity to improve health. Come to the meeting with specific suggestions for increasing per-rep login frequency and session depth.
- [ ] **Refresh kit item data** — The external report flagged a 133-day gap between kit imports (Dec 2025) and daily product/option updates. This risks stale kit configurations reaching buyers.
