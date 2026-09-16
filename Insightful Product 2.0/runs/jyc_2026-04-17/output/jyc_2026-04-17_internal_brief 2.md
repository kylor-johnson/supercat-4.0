# Internal Intelligence Brief — Jamie Young Company

*2026-04-17 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Jamie Young Company is a healthy, deeply adopted Full-bundle account in standard-cadence mode. The platform is running well — 100% feature adoption, $8.0M in platform GMV trailing 12 months, zero open support tickets, and no churn risk. The single health weakness is Engagement at 30 (At Risk), driven by low login activity relative to 92 provisioned users. The meeting should be opportunity-focused: dormant customer reactivation (3,654 lapsed accounts), top-rep re-engagement (Charlee Lowery's 88% order decline), and closing the 240-day stale config data gap that drags Operational Health.

**Three Things That Matter:**

1. **Engagement is the one health drag** — At 30, it's the only dimension below Healthy and the primary factor keeping health at 66 instead of 75+. The external report flagged Charlee Lowery's 88% order decline and 43% login drop, which compounds this signal. Active user ratio is low against 92 provisioned users.
2. **3,654 lapsed eCat accounts are the largest growth lever** — The external report highlights this as the #1 customer intelligence finding. Only 35.2% of the 5,640 historical eCat buyers remain active. Converting even 10% would add ~365 active accounts.
3. **240-day stale config data is an easy operational win** — Options, option groups, and price level files haven't been refreshed since August 2025 while the core catalog updates daily. This drags Operational Health from what would be 80+ down to 60 and risks reps seeing outdated product configurations.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 66/100 | Maintain |
| **Band** | Healthy | Standard cadence |

> Jamie Young Company (Full) scores 66 Health → Maintain. Adoption (100) leads health; stable with standard cadence.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 30 | 🔴 At Risk | Low login frequency relative to 92 provisioned users. Active user ratio likely below 10%. Peers in the Full bundle average higher engagement — JYC is 32.7% above the peer login median but the active-user-ratio pulls the composite score down. |
| Adoption (20%) | 100 | 🟢 Thriving | All 10 features available for the Full bundle are used above minimum thresholds: iPad, eCat Online, B2B Cart, Sales Portal, search, presentations, email sharing, PDF catalogs, documents, and stacks. Perfect score. |
| Value Delivery (30%) | 75 | 🟢 Healthy | Full bundle formula: (order_volume + customer_activation + eol_share + portal_engagement) / 4. Strong order flow (8,295 orders, $8.0M GMV LTM) and growing eCat Online share (47%) drive the score. Customer activation could be higher — 35.2% retention rate suggests room to improve the activation component. |
| Operational Health (15%) | 60 | 🟢 Healthy | Active import pipeline (~68 imports/month) keeps core data fresh, but 12 supplemental entities (options, pricing, quotas) haven't been updated in 240 days, pulling the data freshness sub-score down. Catalog completeness is solid. Import success rate is healthy. |
| Trajectory (10%) | 70 | 🟢 Healthy | Positive Q/Q trend. Order volume stable in the 600–784/month range. Login activity trending slightly up. The primary value metric (orders) is steady, not declining — a 70 reflects moderate positive momentum without acceleration. |

### Flags

No risk modifiers fired. No churn risk. Not expansion ready. Not flagged as healthy-complete. All warning flags clear (`hs_lifecycle_stale` = false, `hs_join_missing` = false, `arr_data_gap` = false). Scoring status: complete.

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Jamie Young Company's bundle (Full), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measures login intensity (logins per active user) and active user ratio (active users / total users).
- **Adoption (20%)** — How many of the 10 available features are being used above minimum thresholds? Full bundles have the most features: iPad core (search, customer selection, presentations, email, PDF, documents, stacks), eCat Online, Order Submission, and Sales Portal.
- **Value Delivery (30%)** — Is the platform generating business value? For Full bundles, this measures four components equally: order volume, customer activation rate, eCat Online order share, and Sales Portal engagement.
- **Operational Health (15%)** — Is client data clean and current? Import success rate (50% weight), catalog completeness (30%), and data freshness (20%).
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares primary value metric and logins between current 90 days and prior 90 days.

**Classification** maps Health into an action mode:
- Health ≥ 60 = **Maintain** or **Expand** (depending on growth signals)
- Health 40–59 = **Watch** territory
- Health < 40 = **At Risk/Critical** — requires intervention

</details>

---

## Support & Issue Themes

> 10 conversations in 90 days. Admin-focused, routine volume, all L1. No active fires.

### Themes

**1. Data Sync & Imports** (2 tickets)
- "Re: Jamie Young eCat Support Request" (import/export assistance)
- "Import error (JYC)" (S3 — medium severity import issue)
- **Impact**: Import issues can disrupt the daily data refresh pipeline that keeps the catalog current. Given JYC's ~68 imports/month, occasional errors are expected but worth monitoring for patterns.
- **Root**: Standard import formatting issues or field-mapping errors during routine data updates.
- **Action**: Ensure import error patterns are resolved so the 240-day stale supplemental data doesn't worsen. Consider proactive import health check before the meeting.

**2. Training & Admin Workflows** (2 tickets)
- "Customer Set-Up Support for Jamie Young" (new customer setup)
- "Re: Delegation" (enrollment delegation workflow)
- **Impact**: Training requests indicate an actively managed platform with ongoing onboarding. JYC has 5,640 historical eCat accounts — customer setup is a regular workflow.
- **Root**: Complexity of the delegated enrollment system and customer hierarchy management for a large buyer base.
- **Action**: No action needed — healthy signal of active admin engagement.

**3. Sales & Finance** (2 tickets)
- "Fwd: Jamie Young Portal Question" (logged on Jira → EBR-730)
- "Re: Payment Overdue Notice" (payment banner visibility issue)
- **Impact**: The payment banner issue directly led to a Jira feature request (EBR-730). Reps seeing overdue payment notices on enrollment pages creates a poor user experience.
- **Root**: Platform displays payment status banners to all users with Admin Console access, including reps.
- **Action**: Track EBR-730 resolution. This is a UX issue that JYC's admin team flagged explicitly.

### Escalation Profile

9 of 10 conversations tagged L1 (handled by frontline support). 1 untagged. Zero L2+ escalations. Peak severity: S3 (medium) on 2 conversations. No S1/S2 high-severity issues. Lowest-friction support profile possible.

### Open Tickets (0)

No open support tickets. All 10 conversations in the 90-day window are closed.

---

## Active Engineering & Projects

7 open Jira tickets found for Jamie Young Company. 1 recent, 6 legacy backlog. All are stale.

### Recent / Active

| Key | Summary | Status | Priority | Project | Age | Days Since Update |
|---|---|---|---|---|---|---|
| [EBR-730](https://supercatsolutions.atlassian.net/browse/EBR-730) | Remove Payment Banner from enrollment pages | Triaging | Unprioritized | EBR | 55d | 53d ⚠️ |
| [SERV-2056](https://supercatsolutions.atlassian.net/browse/SERV-2056) | Resale number field (Jamie Young) | In Progress | Unprioritized | SERV | 446d | 416d 🔴 |

### Backlog (Triaging — Legacy Requests)

| Key | Summary | Status | Priority | Project | Age | Days Since Update |
|---|---|---|---|---|---|---|
| [EBR-502](https://supercatsolutions.atlassian.net/browse/EBR-502) | Add 2nd contact & email to eOL enrollment & eCat order | Triaging | **High** 🔴 | EBR | 913d | 233d |
| [EBR-422](https://supercatsolutions.atlassian.net/browse/EBR-422) | Report: when customer placed first order | Triaging | Unprioritized | EBR | 1176d | 233d |
| [EBR-420](https://supercatsolutions.atlassian.net/browse/EBR-420) | "How did you hear about us?" enrollment survey | Triaging | Medium | EBR | 1176d | 233d |
| [EBR-417](https://supercatsolutions.atlassian.net/browse/EBR-417) | Customize login and apply-for-access pages | Triaging | Medium | EBR | 1176d | 233d |
| [EBR-384](https://supercatsolutions.atlassian.net/browse/EBR-384) | Delegated Enrollment: sort on Admin Console list | Triaging | Low | EBR | 1322d | 233d |

**Flags:**
- 🔴 **Stale**: All 7 tickets have no update in 14+ days. SERV-2056 shows "In Progress" but hasn't been updated in 416 days.
- 🔴 **High priority**: EBR-502 is marked High — add 2nd contact/email to enrollment and orders. Assigned to Sarah Moravec. 913 days old with no resolution.
- ⚠️ **Note**: [EBR-726](https://supercatsolutions.atlassian.net/browse/EBR-726) (preferred carrier field) is a Braxton Culler request but references JYC as having a similar custom field. Relevant for cross-client feature patterning.

**Cross-Surface Links:**
- EBR-730 (payment banner) directly originated from the "Payment Overdue Notice" HelpScout conversation. The support ticket was tagged `status: logged on jira`.
- EBR-384 and EBR-502 both relate to the enrollment/delegation workflow that appeared in the training support theme.

---

## Meeting Playbook

### Talking Points

1. **Dormant customer reactivation is the biggest lever** — External report highlights 3,654 lapsed eCat accounts (64.8% of historical buyers). Internally, this aligns with strong platform health but moderate Value Delivery — the infrastructure is there, the buyer base just needs reactivation. Consider discussing targeted re-engagement campaigns during the meeting.
2. **240-day stale config data is a quick win** — External report flags 12 stale data entities from August 2025. Internally, this is the primary drag on Operational Health (60). Refreshing options, option groups, and pricing files would immediately improve data quality and rep experience. Prepare to explain what a config data refresh involves.
3. **Charlee Lowery's decline mirrors the Engagement weakness** — External report shows the team's #2 GMV contributor dropped 88% in orders with 43% fewer logins. Internally, Engagement is the only At Risk dimension at 30. This isn't a platform problem — it's a user-level re-engagement opportunity worth raising with JYC leadership.
4. **7 stale Jira tickets need triage or closure** — EBR-502 (High priority, 2nd contact/email) is 913 days old. SERV-2056 (resale number field) says "In Progress" but hasn't moved in 416 days. Before the meeting, decide which are still relevant and which should be closed.

### Not in the External Report

- **Health score: 66 (Healthy)** — classification is Maintain, standard cadence. No churn risk.
- **Engagement at 30 is At Risk** — the weakest dimension by far, but not triggering any risk modifiers because login_intensity is still above zero and no RM conditions are met.
- **Support is exceptionally clean** — 10 conversations in 90 days, all L1, all closed. No S1/S2 issues. This is one of the lowest-friction support profiles in the portfolio.
- **7 stale Jira tickets in the backlog** — the client may raise these. EBR-502 (High priority) and several enrollment-related feature requests are unresolved for 1–3 years.
- **Scoring status: complete** — all data inputs present, no missing data flags, no warning flags. This is a clean score.

### SuperCat Action Items

- [ ] **Refresh stale configuration data** — Re-import options, option groups, and price level files to close the 240-day drift with the daily-refreshed product catalog. This would improve Operational Health and reduce the risk of reps seeing outdated configurations.
- [ ] **Triage or close 7 stale Jira tickets** — Review EBR-502 (High, 913d), SERV-2056 (In Progress, 416d), and 5 legacy backlog tickets. Decide: still relevant → update status and communicate timeline, or no longer needed → close with a note to the client.
- [ ] **Prepare Charlee Lowery talking points** — If JYC raises her declining activity, have context ready: 88% order decline, 43% login decline. Frame as a re-engagement opportunity, not a platform issue.
