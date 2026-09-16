# Internal Intelligence Brief — Somerset Bay and Modern History

*2026-04-20 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Somerset Bay and Modern History is a healthy, operationally mature account running the Full bundle at $26K ARR. The platform is deeply adopted (100/100) and generating strong business value ($10.9M GMV trailing 12 months), but engagement is the outlier problem — at 20, it's the lowest health dimension by a wide margin and sits at half the peer median. The meeting should be offense-focused: address the engagement gap and stale configuration data while highlighting the $800K+ dormant account reactivation opportunity.

**Three Things That Matter:**

1. **Engagement is critically low at 20 (At Risk)** — Despite perfect adoption and strong value delivery, login frequency is at half the peer median (20 vs 40). Two top-15 producers (Douglas Hall, Daniel Allen) dropped to zero orders this quarter. Understanding what's driving the login gap is the single highest-leverage health improvement available.
2. **$800K+ in dormant buyer accounts to reactivate** — 3,420 lapsed eCat buyers and 25 high-value dormant accounts (Teresa's on Main at $85K, White House Interiors at $62K, Carolina Furniture at $59K) represent the biggest commercial opportunity surfaced in the external report. Value Delivery is Thriving at 80, so reactivation efforts carry no health risk.
3. **Configuration data is 8 months stale** — 11 of 22 data entities haven't been updated since August 2025, dragging Operational Health to 60 (vs peer median 85). Categories, price levels, and options may be showing outdated info to reps and buyers. A single import cycle would fix half of all tracked entities.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 63/100 | Maintain |
| **Band** | Healthy | Action: protect with standard cadence |

> 63 Health → Maintain. Adoption (100) leads health; stable with standard cadence.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 20 | 🔴 At Risk | Login frequency and active user ratio are critically low. At half the peer median (20 vs 40), very few users are logging in regularly. Two top-15 producers dropped to zero activity this quarter. This is the single biggest drag on overall health. |
| Adoption (20%) | 100 | 🟢 Thriving | All 10 features available in the Full bundle are used above minimum thresholds — product search, customer selection, presentations, email sharing, PDF catalogs, document viewing, stacks/lists, eCat Online, order submission, and Sales Portal. Perfect score. |
| Value Delivery (30%) | 80 | 🟢 Thriving | For the Full bundle, VD averages order volume, customer activation, eCat Online share, and portal engagement. All four components are generating strong business value — $10.9M GMV trailing 12 months, healthy buyer activation, consistent portal traffic (~120 daily visitors). |
| Operational Health (15%) | 60 | 🟢 Healthy | Catalog completeness is excellent at 99.2% (top quartile vs peers). However, data freshness drags the score down — 11 of 22 data entities are 243+ days stale (categories, price levels, groups from August 2025). Core data (products, customers, inventory) is current. |
| Trajectory (10%) | 50 | 🟡 Watch | Quarter-over-quarter trend is flat. Primary value metric (order volume) and login trends are in the −5% to +10% range — stable but showing no momentum in either direction. |

### Flags

No flags. No risk modifier fired. No churn risk. Warning flags all clear (hs_lifecycle_stale: false, hs_join_missing: false, arr_data_gap: false).

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Somerset Bay and Modern History's bundle (Full), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measures login frequency per active user and active user ratio.
- **Adoption (20%)** — How many available features are being used above minimum thresholds? For Full bundles, 10 features are tracked across iPad, eCat Online, B2B Cart, and Sales Portal.
- **Value Delivery (30%)** — Is the platform generating business value? For Full bundles, this measures the average of four components: order volume, customer activation rate, eCat Online vs iPad order mix, and Sales Portal engagement.
- **Operational Health (15%)** — Is client data clean and current? Import success rate, catalog completeness (products with images and pricing), and data freshness (days since critical updates).
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares current 90-day period to prior 90-day period for primary value metric and logins.

**Classification** determines the recommended action cadence:
- **Expand** — healthy account with strong expansion signals
- **Maintain** — healthy, protect with standard cadence
- **Stabilize First** — needs health improvement before expansion
- **Intervene** — immediate save/recovery plan needed

</details>

---

## Support & Issue Themes

> 3 conversations in 90 days. Low volume, admin-focused. No active fires.

### Themes

**1. Admin & rep management** (2 tickets)
- "SALES REP GROUP" (Mar 18) · "Re: SALES REP USER GROUP" (Feb 10)
- **Impact**: Recurring user/group management requests indicate the client's admin team may not be fully confident navigating Admin Console workflows independently.
- **Root**: Admin Console user management UI complexity or staff turnover requiring repeated walkthroughs for the same task category.
- **Action**: Offer a targeted training session on Admin Console user and group management for the client's admin team.

**2. Order confirmation bug** (1 ticket)
- "Re: FW: Modern History/Somerset Bay Order Confirmation" (Mar 9)
- **Impact**: A bug in order confirmations escalated to L3 engineering, indicating a workflow issue that could affect buyer trust and rep confidence in the ordering pipeline.
- **Root**: Bug in order email or confirmation logic that required engineering intervention to resolve.
- **Action**: Confirm this issue was fully resolved and has not recurred. If it did, prioritize a fix before the meeting.

### Escalation Profile

2 L1, 0 L2, 1 L3. Peak severity: S3 (order confirmation bug). No S1/S2 critical issues. No L4 executive escalations.

### Open Tickets (0)

No open tickets. All 3 conversations from the past 90 days are closed.

---

## Active Engineering & Projects

4 Jira tickets found for this client. All are stale enhancement requests — no active engineering work in flight.

| Key | Summary | Status | Priority | Project | Age | Days Since Update |
|---|---|---|---|---|---|---|
| [EBR-537](https://supercatsolutions.atlassian.net/browse/EBR-537) | Sort eOL customer index by city (Modern History) | Triaging | Unprioritized | EBR | 812d | 233d ⚠️ |
| [EBR-406](https://supercatsolutions.atlassian.net/browse/EBR-406) | Allow multiple email recipients on order email | Triaging | Unprioritized | EBR | 1,218d | 233d ⚠️ |
| [ECAT-349](https://supercatsolutions.atlassian.net/browse/ECAT-349) | Order surcharges don't auto add for locally created customers | To Do | Unprioritized | ECAT | 1,649d | 1,592d 🔴 |
| [SERV-451](https://supercatsolutions.atlassian.net/browse/SERV-451) | Support credit cards — eOL | To Do | Low | SERV | 1,732d | 1,161d 🔴 |

**Flags:**
- 🔴 **Stale**: All 4 tickets have had no update in 233+ days. ECAT-349 and SERV-451 are 3–4 years without update.
- No blocked tickets.
- No high-priority tickets (all Unprioritized or Low).

**Cross-Surface Links:**
- EBR-537 (city sort for eOL customer index) connects to portal engagement — SBMH's eCat Online portal has strong traffic (~120 daily visitors); this enhancement would improve the dealer/buyer discovery experience.
- EBR-406 (multiple email recipients) connects to the order confirmation support theme — the HelpScout L3 ticket about order confirmations touches the same order email workflow.
- ECAT-349 (surcharges for local customers) was originally reported by Daniel Allen at SBMH — one of the two top-15 producers flagged in the external report as disengaging.

---

## Meeting Playbook

### Talking Points

1. **Dormant account reactivation is the top commercial opportunity** — External report highlights 3,420 lapsed eCat buyers worth $800K+ in historical value. Internally, Value Delivery is Thriving at 80 and customer concentration is healthy (top 5 = 13.2% of GMV), so reactivation is pure upside with no health risk. Lead the meeting with a joint reactivation plan for the top 25 dormant accounts.
2. **Stale config data is a fixable health drag** — External report flags 11 entities 243+ days stale (categories, price levels, groups). Internally, this drags Operational Health to 60 (vs peer median 85). Prepare to explain what a configuration refresh involves — a single import cycle using the August 2025 batch would bring half of all tracked entities current.
3. **Engagement gap needs investigation** — External report surfaces rep engagement at 20 vs peer median 40, with Douglas Hall and Daniel Allen disengaging. Internally, Engagement at 20 (At Risk) is the single largest health dimension deficit. Use the meeting to explore what's driving the login gap — is it a workflow change, team turnover, or a tool adoption issue?

### Not in the External Report

- **Health score: 63 (Healthy)** with Maintain classification — internal only per semantic guardrails
- **No churn risk** — no risk modifiers fired, all warning flags clear
- **No expansion readiness** — growth signals are developing but not yet actionable
- **Support history**: Only 3 conversations in 90 days, all resolved, no open tickets — extremely low-touch account
- **4 stale Jira enhancement requests** from 2021–2024 remain open but untouched (oldest: SERV-451 from July 2021)
- **All 7 shared library resources are 530+ days stale** despite 1,718 library views — active usage with outdated content

### SuperCat Action Items

- [ ] **Refresh stale configuration data** — 11 entities (categories, price levels, groups) are 243+ days old; re-running the August 2025 import batch would bring half of all tracked entities current
- [ ] **Triage or close 4 stale Jira tickets** — EBR-537, EBR-406, ECAT-349, and SERV-451 are all 233+ days without update; determine if any are still relevant before the meeting
- [ ] **Update shared library resources** — all 7 library documents are 530+ days stale despite active usage (1,718 views); low-effort improvement
- [ ] **Confirm order confirmation bug resolution** — the L3 HelpScout ticket from March 9 about order confirmations should be verified as fully resolved
