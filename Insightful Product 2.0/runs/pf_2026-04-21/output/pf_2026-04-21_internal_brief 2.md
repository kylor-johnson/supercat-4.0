# Internal Intelligence Brief — Palecek

*2026-04-21 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Palecek is the highest-ARR client in the portfolio ($39,010) and the healthiest by score — 91/100, Thriving, with perfect Adoption and Value Delivery. No fires, no risk signals, no open support tickets. The meeting should be pure offense: the $2.6M dormant account reactivation opportunity, investigating Gina Sgambellone's 90% order decline, and positioning the stale data refresh as a quick operational win. This is a "protect and grow" conversation with a client who has been on the platform since 2012.

**Three Things That Matter:**

1. **$2.6M in dormant accounts is the biggest opportunity** — 4,320 lapsed eCat accounts represent substantial reactivation upside. The external report highlights the top 15 by historical value, led by Furnitureland South ($627K). With health at 91 and no operational concerns, this is pure offense.
2. **Gina Sgambellone's 90% order decline warrants investigation** — The #3 rep by trailing 12-month iPad GMV ($1.74M) dropped from 74 to 7 orders this quarter. Overall Trajectory remains strong (90), but this individual decline could represent over $1M in annualized risk if it continues.
3. **4 Jira tickets are 180+ days stale — clean up the backlog** — CSP-14 (product data characterization, marked "active" but untouched 181 days), SERV-2157 (option panel sorting, 280 days), and two EBR items have no recent activity. Either advance or close them before the meeting.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 91/100 | Maintain |
| **Band** | Thriving | Protect with standard cadence |

> 91 Health → Maintain. Value Delivery (100) leads health; stable with standard cadence.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 80 | 🟢 Thriving | Strong login activity with 118 active users in the trailing 90 days across a distributed rep network. Login intensity and active user ratio both exceed healthy thresholds. Above Furniture peer median. |
| Adoption (20%) | 100 | 🟢 Thriving | Maximum score — all 8 features available for iPad+Catalog are used above minimum thresholds: Product Search, Customer Selection, Presentations, Email Sharing, PDF Catalogs, Document Viewing, Stacks/Lists, and eCat Online. 100th percentile among Furniture peers. |
| Value Delivery (30%) | 100 | 🟢 Thriving | For iPad+Catalog bundles, Value Delivery measures presentation_score — depth of presentation tool usage (email, PDF, sharing). Palecek's presentation actions are at the maximum tier (≥1,000 in 90 days), reflecting deep selling-tool engagement across the rep team. |
| Operational Health (15%) | 80 | 🟢 Thriving | 100% catalog completeness (all 1,520 products have images and pricing). Daily automated imports run cleanly. Minor drag from 12 data entities (categories, groups, collections, pricing) stale for 190+ days — data freshness is what prevents a perfect score. |
| Trajectory (10%) | 90 | 🟢 Thriving | Strong positive Q/Q momentum — both presentation actions and login activity trending up. Score of 90 is 40 points above the Furniture peer median of 50, reflecting sustained acceleration. |

### Flags

No flags. No risk modifiers fired. No churn risk. All warning flags clear (hs_lifecycle_stale: false, hs_join_missing: false, arr_data_gap: false).

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Palecek's bundle (iPad+Catalog), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measures login frequency and active user ratio.
- **Adoption (20%)** — How many available features are being used above minimum thresholds? iPad+Catalog has 8 eligible features.
- **Value Delivery (30%)** — Is the platform generating business value? For iPad+Catalog bundles, this measures presentation_score — the depth of presentation tool usage including email sharing, PDF catalog creation, and document distribution.
- **Operational Health (15%)** — Is client data clean and current? Evaluates import success rate, catalog completeness (products with images and pricing), and data freshness.
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares current 90-day period to prior 90-day period.

**Classification** determines the recommended action cadence:
- **Expand** — healthy account with strong expansion signals
- **Maintain** — healthy, protect with standard cadence
- **Stabilize First** — needs health improvement before expansion
- **Intervene** — immediate save/recovery plan needed

</details>

---

## Support & Issue Themes

> 9 conversations in 90 days. Configuration and image support, low-severity. No active fires.

### Themes

**1. Configuration & Freight Issues** (3 tickets)
- "Re: PALECEK question –", "Re: Palecek Freight Calculator IP Update", "Re: eCat Freight Calculation - Live Instance"
- **Impact**: Freight calculator configuration has required recurring engineering involvement (2× L3 escalation), consuming disproportionate support resources for a low-severity issue.
- **Root**: The freight calculation system relies on IP-specific configuration that requires manual updates when infrastructure changes; not self-service.
- **Action**: Evaluate whether freight config can be moved to self-service admin controls to eliminate recurring L3 escalations.

**2. Image Asset Issues** (3 tickets)
- "Re: Palecek - Image Error", "Re: Palecek - Production Image Error", "FW: eCat"
- **Impact**: Recurring image errors in production — all resolved quickly at L1 (2 were first-touch resolved), but the pattern is persistent.
- **Root**: Image processing pipeline occasionally fails on certain asset formats or sizes, requiring manual intervention to re-process.
- **Action**: Review image validation rules in the import pipeline to catch format issues before they surface to end users.

**3. Platform Usage & Operations** (3 tickets)
- "Re: Option Orders", "Rep issue with ECAT", "Re: eCat Freight Calculation - Live Instance" (bug)
- **Impact**: A mix of how-to questions, manual work requests, and one bug report — typical for a mature, high-adoption client with a large rep team.
- **Root**: Normal operational questions; no systemic issue.
- **Action**: No proactive action needed; continue standard support cadence.

### Escalation Profile

5 L1, 2 L2, 2 L3. No L4 executive escalations. Peak severity: S3 (freight calculator). No S1/S2 critical issues.

### Open Tickets (0)

No active open tickets. One conversation ("Re: PALECEK question –", Apr 9, S4/L1, config issue) is in "pending" status — ball is in the customer's court.

---

## Active Engineering & Projects

5 open Jira tickets found for Palecek. 1 recently created; 4 are aging backlog items.

### Recent / Active

| Key | Summary | Project | Status | Priority | Assignee | Age | Days Since Update |
|---|---|---|---|---|---|---|---|
| [SERV-2323](https://supercatsolutions.atlassian.net/browse/SERV-2323) | FEA: Palecek option SortValue update for Table Top Finish ordering on iPad | Server | To Do | **High** | Unassigned | 6d | 6d |

### Backlog (all stale — 180+ days without update)

| Key | Summary | Project | Status | Priority | Assignee | Age | Days Since Update |
|---|---|---|---|---|---|---|---|
| [CSP-14](https://supercatsolutions.atlassian.net/browse/CSP-14) | pf review plans for new characterization of product data | CSP | Active | Unprioritized | Brent Sanders | 242d | 181d |
| [EBR-684](https://supercatsolutions.atlassian.net/browse/EBR-684) | improve bespoke surcharges functionality | EBR | Submitted | Unprioritized | Unassigned | 201d | 186d |
| [EBR-686](https://supercatsolutions.atlassian.net/browse/EBR-686) | eCat: .xlsx file wont open in Library | EBR | Submitted | Unprioritized | Brent Sanders | 193d | 190d |
| [SERV-2157](https://supercatsolutions.atlassian.net/browse/SERV-2157) | HS-12848: Re: Palecek - Order Option Panel - Sorting Order | Server | To Do | Unprioritized | Brent Sanders | 281d | 280d |

**Flags:**
- 🔴 **High priority**: SERV-2323 is High priority and unassigned
- 🔴 **Stale**: 4 tickets (CSP-14, EBR-684, EBR-686, SERV-2157) have had no update in 180+ days

**Cross-Surface Links:**
- SERV-2323 (option SortValue) and SERV-2157 (option panel sorting) are related — both address option ordering behavior on iPad, suggesting this is a longstanding client request now getting renewed attention with a new ticket.
- The freight calculator support theme (3 HelpScout conversations, 2× L3) has no corresponding Jira ticket — recurrent engineering escalations without a tracking item is a gap worth closing.

---

## Meeting Playbook

### Talking Points

1. **Dormant account reactivation is the headline opportunity** — The external report highlights $2.6M in dormant high-value accounts and a 20% eCat retention rate. Internally, health is at 91 with perfect Value Delivery, so the dormant reactivation push is pure upside with zero health risk. Lead the conversation with reactivation strategy for the top 15 lapsed accounts.
2. **Sgambellone's order decline is worth discussing, not alarming** — The external report flags a 90% order drop for the #3 rep ($1.74M trailing GMV). Internally, overall Trajectory is still 90 (Thriving) — the broader team is compensating. Raise it as an individual investigation point, not an account-level concern.
3. **Stale data entities are the easy operational win** — The external report notes 12 data entities stale for 190+ days (categories, groups, collections, pricing). Internally, this is what keeps Operational Health at 80 instead of 100. A config refresh is straightforward and would bring health even closer to perfect. Prepare to explain what the refresh involves.

### Not in the External Report

- **Health score**: 91/100, Thriving band — highest ARR client in the portfolio at $39,010
- **Classification**: Maintain — healthy, protect with standard cadence
- **No churn risk** — zero risk modifiers fired, all warning flags clear
- **Support pattern**: 9 conversations in 90 days, dominated by config/image issues, no open tickets, no S1/S2 severity, no active fires
- **Jira backlog**: 4 tickets 180+ days stale need triage or closure; 1 new High-priority ticket (SERV-2323) is unassigned
- **Cohort**: On the platform since 2012 — one of the longest-tenured clients

### SuperCat Action Items

- [ ] **Assign SERV-2323** — High-priority option SortValue update is unassigned; needs an owner before the meeting
- [ ] **Triage stale Jira backlog** — 4 tickets (CSP-14, EBR-684, EBR-686, SERV-2157) have not been updated in 180+ days; advance or close
- [ ] **Refresh stale data entities** — Categories, groups, collections, and pricing data (190+ days old) to bring Operational Health to full score
- [ ] **Create Jira ticket for freight config** — Recurring L3 support escalations for freight calculator changes have no engineering tracking item
