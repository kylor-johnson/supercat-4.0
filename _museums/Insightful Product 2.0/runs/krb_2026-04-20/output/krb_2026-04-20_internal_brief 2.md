# Internal Intelligence Brief — Kaleen Rugs & Broadloom

*2026-04-20 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Kaleen Rugs & Broadloom is the lowest-health account in the portfolio at 18/100 (Critical), classified as Intervene. The platform is functionally dormant — zero presentation tool usage, 0% image completeness across the entire 1,493-product catalog, and configuration data that hasn't been refreshed since December 2025. Risk modifier RM-4 has fired and churn risk is active at near-term severity. The meeting should be about whether this account can be reactivated with concrete steps or is heading toward churn, and what it would take to make the platform usable for their team.

**Three Things That Matter:**

1. **Value Delivery is zero — the platform generates no business value** — No presentation tool activity (emails, PDFs, magic button additions) in the current 90-day period. For an iPad-only bundle, presentations are the entire value metric. The external report confirms only 1 eCat order has ever been placed, and the catalog has zero product images — reps have nothing visual to work with.
2. **Data freshness crisis triggered a churn risk flag** — RM-4 fired because 2+ entity types haven't been updated in 180+ days. The external report shows the oldest data is 255 days stale (inventory, kit items, options), and no imports have occurred since December 2025. This is both a health score issue and a practical blocker to any re-engagement effort.
3. **Untagged support history signals incomplete onboarding** — All 5 HelpScout conversations (180-day window) are completely untagged — no severity, type, or escalation classification. The subjects suggest an onboarding sequence that stalled: "Quick Intro — SuperCat Onboarding," "eCat checklist," "Status Update for Kaleen." One conversation has been pending customer response for 74+ days.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 18/100 | Intervene |
| **Band** | Critical | Immediate save/recovery plan needed |

> Kaleen Rugs & Broadloom (iPad-only) scores 18 Health → Intervene. Value Delivery (0) is critically low; immediate attention required.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 30 | 🟡 At Risk | Some login activity exists but is minimal. A score of 30 suggests low login frequency and/or a small fraction of provisioned users are active. Peer benchmarking from the external report shows Kaleen at 30 vs. the peer median of 70 — a 40-point gap, bottom 5% of comparable accounts. |
| Adoption (20%) | 14 | 🔴 Critical | For the iPad-only bundle, 7 features are available (product search, customer selection, presentations, email sharing, PDF catalogs, document viewing, stacks/lists). A score of 14 means only ~1 of 7 features exceeds minimum usage thresholds. Core selling capabilities like email sharing, PDF catalogs, and stacks are not being utilized. |
| Value Delivery (30%) | 0 | 🔴 Critical | For iPad-only bundles, Value Delivery = presentation_score, measuring email drafts, PDF catalog generation, magic button additions, and document emails. A score of 0 means zero presentation tool activity in the current 90-day period. The platform is not being used for its core purpose — assisted selling and product presentation. |
| Operational Health (15%) | 8 | 🔴 Critical | Reflects a severe data freshness crisis. The external report confirms all 22 tracked data entity types are beyond the 30-day threshold. Newest data is 38 days old; oldest (inventory, kit items, options) is 255 days stale. No imports have occurred since December 2025. Import infrastructure exists (345 lifetime imports) but has gone dormant. Catalog completeness is also degraded — 0% image completeness across all 1,493 products. |
| Trajectory (10%) | 60 | 🟢 Healthy | The one relative bright spot. At 60, the Q/Q trend is flat to slightly positive — activity in the current period has not declined significantly further from the prior period. This suggests the account hasn't accelerated its decline, though the baseline is already extremely low. Among peers, Trajectory is the narrowest gap (60 vs. peer median 80). |

### Flags

- **Risk modifier RM-4 fired** — `days_since_critical_update` > 180 for 2+ entity types. Cap: 30. Severity: near-term. The raw health score of 18 falls below the cap, so the modifier does not reduce the score further, but it does trigger the churn risk flag.
- **Churn risk: Active** — Near-term severity, triggered by RM-4.
- **Warning flag: hs_lifecycle_stale** — HubSpot lifecycle status is stale for this org (shows "Lost" or "Churn" status while the subscription remains active). This is a data hygiene issue, not a scoring input, but signals that HubSpot records need updating.

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Kaleen Rugs & Broadloom's bundle (iPad-only), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measures login frequency and active user ratio.
- **Adoption (20%)** — How many of the 7 available iPad-only features are being used above minimum thresholds? Features include product search, customer selection, presentations, email sharing, PDF catalogs, document viewing, and stacks/lists.
- **Value Delivery (30%)** — Is the platform generating business value? For iPad-only bundles, this measures **presentation tool usage**: email drafts, PDF catalog creation, magic button additions, and document emails. This is the highest-weighted dimension because it directly measures whether the platform delivers on its core promise.
- **Operational Health (15%)** — Is client data clean and current? Import success rates, catalog completeness (images + pricing), and data freshness (days since last update to products, customers, or inventory).
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares current 90-day period to the prior 90-day period for both the primary value metric and login volume.

**Classification** determines the recommended action cadence:
- **Expand** — Healthy account with strong expansion signals
- **Maintain** — Healthy, protect with standard cadence
- **Stabilize First** — Needs health improvement before expansion
- **Intervene** — Immediate save/recovery plan needed

Kaleen Rugs & Broadloom is classified **Intervene** — the most urgent action mode.

</details>

---

## Support & Issue Themes

> 5 conversations in 180 days (extended from 90-day default due to sparse volume — only 2 conversations in 90 days). Onboarding and re-engagement tenor. No active fires.

### Themes

**Note:** All 5 conversations have zero HelpScout tags (no severity, type, escalation, or status tags applied). Theme analysis is based on subject-line and conversation context inference rather than structured tag data. This tagging gap should be addressed by the support team.

**1. Onboarding & Setup** (3 conversations)
- "Re: Quick Intro - SuperCat Onboarding" (Feb 5, 2026 — 10 threads)
- "Re: eCat checklist" (Oct 31, 2025 — 4 threads)
- "Re: FW: Status Update for Kaleen" (Oct 28, 2025 — 9 threads)
- **Impact**: The onboarding sequence appears to have stalled. Three of the five conversations are directly about setup and status, suggesting the client never fully completed initial onboarding and configuration.
- **Root**: Likely a combination of client-side resource constraints and the foundational data gaps (no images, stale data) that make the platform feel incomplete before onboarding can progress.
- **Action**: Before the meeting, assess where onboarding actually stands. If foundational data (images, fresh imports) isn't in place, onboarding cannot succeed — address the data first.

**2. Platform Re-engagement** (2 conversations)
- "Re: FW: eCAT update" (Apr 14, 2026 — 3 threads)
- "Re: today's meeting" (Dec 15, 2025 — 5 threads)
- **Impact**: These conversations suggest periodic attempts to re-engage the client on the platform, but without follow-through. The pattern of meeting-related conversations that don't translate into sustained activity reinforces the stalled adoption narrative.
- **Root**: Re-engagement attempts may lack a concrete action plan. Without addressing the underlying blockers (no images, stale data), meetings alone won't drive adoption.
- **Action**: The next re-engagement touchpoint needs a concrete, achievable action plan — not just a status check. "Load images for your top 50 products" is more actionable than "let's discuss eCat."

### Escalation Profile

No escalation or severity tags present on any of the 5 conversations. The support interaction profile is entirely unclassified. No L2+ escalations, no high-severity issues. The tenor is low-intensity onboarding support, not break/fix.

### Open Tickets (0 active / 2 pending)

No tickets with "active" status. Two conversations are in "pending" status (awaiting customer response):

| Subject | Days Open | Severity | Level | State | Action? |
|---|---|---|---|---|---|
| Re: FW: eCAT update | 6 | Untagged | Untagged | CUSTOMER_WAITING | — |
| Re: Quick Intro - SuperCat Onboarding | 74 | Untagged | Untagged | CUSTOMER_WAITING | 🔴 74 days pending |

The 74-day pending onboarding conversation is a red flag — not because it requires agent action, but because a 74-day silence from the client on an onboarding thread strongly suggests disengagement. Consider proactively re-opening this thread before the meeting.

---

## Active Engineering & Projects

1 Jira ticket found for this client. Search strategies: `text ~ "Kaleen"` (0 results), `text ~ "krb"` (1 result — matched via import URL in description).

| Key | Summary | Project | Status | Priority | Assignee | Age (days) | Days Since Update |
|---|---|---|---|---|---|---|---|
| [EBR-608](https://supercatsolutions.atlassian.net/browse/EBR-608) | Unhelpful error when omitting optional field from kit_item file upload | EBR | Triaging | Unprioritized | Unassigned | 403 | 234 |

**Flags:**
- 🔴 **Stale**: EBR-608 has not been updated in 234 days (last update: Aug 30, 2025). This ticket has been in "Triaging" status for over a year with no assignee.
- ⚠️ **Unassigned & Unprioritized**: No one owns this ticket and it has no priority level set.

**Cross-Surface Links:**
- EBR-608 directly relates to Kaleen's import experience — the bug was filed from a KRB import event (kit_item file upload). This connects to the data freshness crisis flagged in Section 2 (Operational Health = 8) and the external report's finding that no imports have occurred since December 2025. While the bug affects an edge case (optional field handling), the broader signal is that import-related friction may be one barrier to the client resuming data updates.
- No HelpScout conversations tagged `status: logged on jira` — the cross-link is inferred from the Jira ticket description mentioning the KRB import URL.

---

## Meeting Playbook

### Talking Points

1. **Zero images across the entire catalog is the adoption blocker** — The external report highlights 0% image completeness across 1,493 products. Internally, this aligns with Value Delivery at 0 and Adoption at 14 (both Critical). For a home décor and rug manufacturer, images aren't optional — they are the product experience. Until images are loaded, the platform cannot function as a visual selling tool, and adoption will remain near zero.
2. **255-day-stale data triggered a churn risk flag** — The external report flags all 22 data entity types beyond the 30-day freshness threshold, with the oldest at 255 days. Internally, this fired risk modifier RM-4 and set churn risk to active (near-term severity). The client needs to resume imports — the infrastructure exists (345 lifetime imports) — and we have a dormant Jira bug (EBR-608) related to their import experience that should be resolved first.
3. **The onboarding appears to have stalled — re-engagement needs a concrete plan** — Support history shows an onboarding sequence (checklist, status updates, quick intro) that trailed off. The most recent thread ("eCAT update") is 6 days old. The meeting should propose a specific, bounded reactivation plan: load images for top products, refresh customer/inventory data, then drive one rep to complete a presentation workflow.

### Not in the External Report

- **Health score: 18/100 (Critical)** — Lowest health in the portfolio. Band: Critical.
- **Classification: Intervene** — Immediate save/recovery plan needed. This is the most urgent action mode in the model.
- **Churn risk: Active, near-term severity** — Triggered by RM-4 (data staleness > 180 days for 2+ entity types).
- **Support history: 5 conversations in 180 days, all untagged** — Low-volume onboarding support with no severity or escalation classification. Tagging gap is a support process issue.
- **HubSpot lifecycle stale** — `hs_lifecycle_stale` flag is true, meaning HubSpot records show this account as Lost/Churn while the subscription is still active. HubSpot needs updating.
- **Jira ticket EBR-608** — Import bug open for 403 days, unassigned, unprioritized, stale for 234 days. Directly related to client's import workflow.

### SuperCat Action Items

- [ ] **Refresh stale configuration data** — Operational Health is 8 (Critical) driven by data that is 38–255 days stale across all 22 entity types. Prepare to walk the client through what a data refresh involves and what files they need to provide.
- [ ] **Resolve or close EBR-608** — Import bug open 403 days, unassigned, in Triaging. Assign, prioritize, and either fix or close before/after the meeting. Having a known import bug open while asking the client to resume imports is a bad look.
- [ ] **Re-engage on the stalled onboarding thread** — The "Quick Intro - SuperCat Onboarding" conversation has been pending customer response for 74 days. Proactively reach out before the meeting to reset the relationship.
- [ ] **Update HubSpot lifecycle status** — `hs_lifecycle_stale` is true. Correct the HubSpot record to reflect the active subscription. This is a data hygiene task, not client-facing.
