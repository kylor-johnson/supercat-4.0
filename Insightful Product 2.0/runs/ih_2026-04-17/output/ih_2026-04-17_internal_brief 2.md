# Internal Intelligence Brief — Interlude Home

*2026-04-17 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Interlude Home is a healthy, high-performing account in standard-cadence maintenance mode. Health 89 (Thriving) with perfect Adoption and strong Value Delivery — this is one of the best-scoring iPad+Catalog+Portal clients in the portfolio. No fires, no churn risk, zero support conversations in 180 days. The only soft spot is Trajectory at 50 (Watch), likely reflecting the rep-level declines the external report surfaces. The meeting should be pure offense: address the declining reps before the revenue impact widens, and explore the massive unactivated customer base.

**Three Things That Matter:**

1. **$1.1M in rep revenue trending down** — The external report flags Niti Athre (dropped to zero) and Dustin Mirwaldt (orders halved). Internally, Trajectory at 50 confirms platform momentum is flattening. This is the single most actionable topic for the meeting — diagnose what's happening with these reps before it compounds.
2. **Perfect adoption, but 240-day stale config data** — Health scores 89 with Adoption at 100 and Operational Health at 94, but the external report reveals options, price levels, and option groups haven't been refreshed since August 2025. The health model tracks product/customer/inventory freshness (which are current), not configuration entities. Reps may be presenting outdated options to buyers. This is a SuperCat action item to prepare before the meeting.
3. **Support visibility gap — possible domain mismatch** — Zero HelpScout conversations in 180 days under `believeandbuild.com`, but Jira ticket EBR-760 references a user at `interludehome.com`. The domain mapping may be incomplete. Verify whether `interludehome.com` should be added to the domain map to capture support activity.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 89/100 | Maintain |
| **Band** | Thriving | |

> Interlude Home (iPad+Catalog+Portal) scores 89 Health → Maintain. Adoption (100) leads health; stable with standard cadence.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 90 | 🟢 Thriving | Login frequency and active user ratio are both top-tier. The external report confirms top-5% peer engagement among Furniture manufacturers — 30 points above the peer median. Users are consistently logging in and actively working in the platform. |
| Adoption (20%) | 100 | 🟢 Thriving | All 9 available features for iPad+Catalog+Portal are used above minimum thresholds: Product Search, Customer Selection, Presentations, Email Sharing, PDF Catalogs, Document Viewing, Stacks/Lists, eCat Online, and Sales Portal. Perfect breadth. |
| Value Delivery (30%) | 90 | 🟢 Thriving | For iPad+Catalog+Portal, VD = (presentation_score + portal_engagement_score) / 2. Both presentation tools (emails, PDFs, sharing) and Sales Portal access are generating strong business value. The platform processed $11.5M of $17.0M total business (67.7% capture rate). |
| Operational Health (15%) | 94 | 🟢 Thriving | Import success and catalog completeness are excellent. Core data (products, customers, inventory) is fresh. Note: the health model scores data freshness on critical entities — it does not capture the 240-day staleness on options, option groups, and price levels flagged in the external report. |
| Trajectory (10%) | 50 | 🟡 Watch | Q/Q momentum is flat. The primary value metric (presentation + portal activity) is roughly stable, but login trends may show slight softness — consistent with the rep-level declines (Athre to zero, Mirwaldt halved) visible in the external report. Not alarming yet, but worth monitoring. |

### Flags

No flags. No risk modifier fired. No churn risk. `hs_lifecycle_stale`: false. `hs_join_missing`: false. `arr_data_gap`: false.

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Interlude Home's bundle (iPad+Catalog+Portal), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measures login frequency and active user ratio.
- **Adoption (20%)** — How many available features are being used above minimum thresholds? For iPad+Catalog+Portal, 9 features are available.
- **Value Delivery (30%)** — Is the platform generating business value? For iPad+Catalog+Portal bundles, this measures the average of presentation tool usage (emails, PDFs, sharing) and Sales Portal engagement.
- **Operational Health (15%)** — Is client data clean and current? Import success, catalog completeness, data freshness for products/customers/inventory.
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter?

**Classification** determines the recommended action cadence:
- **Expand** — healthy account with strong expansion signals
- **Maintain** — healthy, protect with standard cadence
- **Stabilize First** — needs health improvement before expansion
- **Intervene** — immediate save/recovery plan needed

</details>

---

## Support & Issue Themes

> 0 conversations in 180 days (extended window). No support footprint under mapped domain. No active fires.

### Themes

No themes — zero conversations attributed to Interlude Home in the 180-day window.

**Domain coverage note:** HelpScout attribution uses `believeandbuild.com` (from domain map). However, Jira ticket EBR-760 references a HelpScout conversation from `smcfadden@interludehome.com`. The domain `interludehome.com` is not in the domain map, which means support conversations may exist but are not being attributed. This is a data gap, not evidence of zero support activity.

### Escalation Profile

No escalation data available (no attributed conversations).

### Open Tickets (0)

No open HelpScout tickets.

---

## Active Engineering & Projects

2 open Jira tickets found for Interlude Home in the EBR (Enhancements and Bug Requests) project. Both are feature requests in Submitted (To Do) status with no assignee.

| Key | Summary | Status | Priority | Project | Age (days) | Days Since Update |
|---|---|---|---|---|---|---|
| [EBR-760](https://supercatsolutions.atlassian.net/browse/EBR-760) | Attach Library PDFs (e.g. COM forms) to order acknowledgment email | Submitted | Unprioritized | EBR | 9 | 9 |
| [EBR-733](https://supercatsolutions.atlassian.net/browse/EBR-733) | Improve color contrast between library headings and content for better readability | Submitted | Unprioritized | EBR | 46 | 46 |

**Flags:**
- 🔴 **Stale:** EBR-733 has had no update in 46 days (threshold: 14 days). No assignee, no triage movement since creation.
- No blocked tickets.
- No high-priority tickets (both are Unprioritized).

**Cross-Surface Links:**
- EBR-760 originated from a HelpScout conversation ([HS #3279084605](https://secure.helpscout.net/conversation/3279084605/14262?viewId=8668531)) — a sales VP requesting Library PDF attachments on order confirmation emails. This is a workflow efficiency request from an active power user.
- EBR-733 originated from a HelpScout conversation ([HS #3241569480](https://secure.helpscout.net/conversation/3241569480/14044?viewId=8668531)) — a UX readability request for the Library feature.
- Both tickets reinforce that Interlude Home actively uses Library and order features, consistent with the perfect Adoption score.

---

## Meeting Playbook

### Talking Points

1. **Declining reps are the biggest risk in an otherwise thriving account** — The external report highlights $1.1M+ in trailing 12-month GMV at risk from Athre (zero activity) and Mirwaldt (orders halved). Internally, Trajectory at 50 (Watch) is the only dimension below Thriving — this is where the momentum softness shows up. Ask what's happening with these reps: territory changes, personnel transitions, or competitive displacement?
2. **Stale configuration data is invisible to the health score but visible to reps** — The external report flags 240-day-old options, price levels, and option groups. Internally, Operational Health is 94 because the scoring model tracks product/customer/inventory freshness (all current). Prepare to explain what a config refresh involves and offer to coordinate it.
3. **87% unactivated accounts represent the largest growth lever** — The external report shows 17,375 of 19,875 accounts have never ordered via eCat. Internally, Value Delivery is 90 and Adoption is 100 — the platform is being used deeply by those who use it. The conversation should explore how to expand the buyer base, not fix the tool.

### Not in the External Report

- **Health score: 89/100 (Thriving), Classification: Maintain** — internal-only metric confirming this is a healthy, stable account
- **No churn risk** — no risk modifiers fired, no severity flags
- **Zero support conversations in 180 days** (under mapped domain `believeandbuild.com`) — possible domain mapping gap with `interludehome.com`
- **2 open Jira enhancement requests** — both feature requests (Library PDF attachments, UI contrast), one stale at 46 days
- **ARR: $22,140** — contracted annual revenue, cohort year 2021
- **Scoring status: complete** — no missing data flags, full confidence in health score

### SuperCat Action Items

- [ ] **Update HelpScout domain mapping** — Add `interludehome.com` to the domain map for `ih` to capture support conversations currently invisible to attribution
- [ ] **Refresh stale configuration data** — Coordinate re-import of options, option groups, and price levels (240 days stale per external report) before the meeting
- [ ] **Triage or close stale Jira ticket** — EBR-733 (Library heading contrast) has had no movement in 46 days. Assign or close before meeting to demonstrate responsiveness
