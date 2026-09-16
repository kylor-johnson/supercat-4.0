# Internal Intelligence Brief — Jonathan Charles Fine Furniture Ltd.

*2026-04-21 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Jonathan Charles Fine Furniture Ltd. is a red-alert account in immediate intervention mode. Health score is 20 (At Risk), capped by risk modifier RM-2 after a catastrophic >60% drop in primary value metrics — Value Delivery scores just 10/100 and Trajectory is at 0. All eCat ordering activity ceased after December 2025 while the broader business continues at full pace ($4.1M in all-channel orders over the trailing 12 months). The platform is being ignored, not the business. This meeting should be entirely defensive: understand why iPad ordering stopped, determine if the market-show-only pattern is permanent or fixable, and build a concrete recovery plan before this $24K ARR account churns.

**Three Things That Matter:**

1. **RM-2 fired: platform value has collapsed** — Primary value metrics dropped >60% quarter-over-quarter with Value Delivery at 10 and Trajectory at 0. The iPad ordering workflow that generated $1.44M in market-show GMV has completely stopped since December 2025. This triggered an immediate-severity churn risk flag and capped the health score at 20.

2. **Market-show dependency is the structural problem** — All 40 eCat orders in the trailing 12 months were placed in a single 3-month window (Oct–Dec 2025) at furniture market shows. When there is no show, there is no eCat activity. The 35.1% GMV capture rate proves the channel works when active — the gap is between-event usage, and without it, every health dimension except Operational Health is dragged down.

3. **Billing inquiries from a dormant-usage account** — 4 of 10 support conversations in 180 days are invoice-related. A client questioning invoices while not using the platform is a classic cancellation precursor. Combined with $24K ARR at immediate churn risk, this pattern deserves direct attention in the meeting.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 20/100 | Intervene |
| **Band** | At Risk | Immediate save/recovery plan needed |

> 20 Health → Intervene. Trajectory (0) is critically low; immediate attention required.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 50 | 🟡 Watch | Login frequency and active user ratio place engagement mid-range — users are logging in periodically but not deeply. At 50, this is actually the strongest behavioral signal. For an iPad+Catalog+Portal bundle, this suggests basic platform familiarity without consistent daily workflow integration. Engagement is also the closest metric to peer median (50 vs. 60). |
| Adoption (20%) | 33 | 🔴 At Risk | For iPad+Catalog+Portal, 9 features are available. At 33, roughly 3 of 9 are used above minimum thresholds. The peer benchmark confirms all 6 benchmarked capabilities are technically "active" — including CPQ and Kit Items — but at insufficient volume levels. This is an intensity problem, not a breadth problem. |
| Value Delivery (30%) | 10 | 🔴 Critical | For iPad+Catalog+Portal, VD = (presentation_score + portal_engagement_score) / 2. At 10, both presentation tools and Sales Portal usage are critically underperforming. The external report confirms zero eCat orders since December 2025 and only $1.44M in market-show-driven GMV concentrated in Oct–Dec. Presentation actions and portal engagement have both fallen to near-zero in the current quarter. |
| Operational Health (15%) | 82 | 🟢 Thriving | The lone bright spot. Product and inventory data refreshes daily (1 day stale). Catalog completeness is 85.4% across 21,125 products, and import operations are clean. Customer data is 35 days stale, which slightly drags the score. The platform infrastructure is well-maintained — the problem is that nobody is using it. |
| Trajectory (10%) | 0 | 🔴 Critical | Q/Q comparison shows severe decline across all value metrics. For iPad+Catalog+Portal, primary value metric = (presentation_actions + mp_access_sales_portal) / 2, which fell >60% quarter-over-quarter. Login trends are also deeply negative. All eCat activity occurred Oct–Dec 2025; Jan–Apr 2026 shows zero activity, creating a catastrophic Q/Q decline that triggered RM-2. |

### Flags

- **Risk modifier RM-2 fired** (immediate severity): `primary_value_change_pct` < −60% AND `value_delivery_score` < 20. Health score capped at 20.
- **Churn risk**: Active. Severity: **immediate**.
- Warning flags: hs_lifecycle_stale = false, hs_join_missing = false, arr_data_gap = false. No data quality warnings.

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Jonathan Charles's bundle (iPad+Catalog+Portal), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measures login frequency and active user ratio.
- **Adoption (20%)** — How many available features are being used above minimum thresholds? For iPad+Catalog+Portal, 9 features are scored: Product Search, Customer Selection, Presentations, Email Sharing, PDF Catalogs, Document Viewing, Stacks/Lists, eCat Online, and Sales Portal.
- **Value Delivery (30%)** — Is the platform generating business value? For iPad+Catalog+Portal bundles, this measures the average of presentation tool usage (magic button adds, email drafts, PDF catalogs) and Sales Portal engagement. This is the most heavily weighted dimension because it captures whether the platform is actually driving revenue-generating activity.
- **Operational Health (15%)** — Is client data clean and current? Import success rates, catalog completeness (products with images and pricing), and data freshness across products, customers, and inventory.
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares current 90-day metrics to prior 90-day metrics for both the primary value metric and login activity.

**Classification** determines the recommended action cadence:
- **Expand** — healthy account with strong expansion signals
- **Maintain** — healthy, protect with standard cadence
- **Stabilize First** — needs health improvement before expansion
- **Intervene** — immediate save/recovery plan needed

</details>

---

## Support & Issue Themes

> 10 conversations in 180 days (extended window; only 1 in the most recent 90 days). Low-volume, training-forward with recurring billing inquiries. No active fires — all tickets are closed.

### Themes

**1. Platform Training & Onboarding** (5 tickets)
- "Re: JC eCat Support" · "Re: eCat Sales Portal check in" (×3) · "Re: eCat Sales Portal implementation"
- **Impact**: Training requests spanning eCat Online and Sales Portal suggest the platform is still in early adoption/onboarding phase. The training theme persisted from November 2025 through March 2026, indicating users have not built lasting platform fluency.
- **Root**: Inconsistent platform usage — the market-show-only ordering pattern means users go months without touching the platform, losing muscle memory between events. Sporadic check-ins are not a substitute for embedded workflows.
- **Action**: Offer a structured training refresh before the next market show cycle. Focus on converting event-driven adoption into sustained daily usage. This directly addresses the Value Delivery and Trajectory collapse.

**2. Billing & Invoice Inquiries** (4 tickets)
- "Re: Fw: New invoice from SuperCat Solutions, LLC #AOSJTJEG-0017" (×3) · "Re: Fw: Reminder: Your invoice is due in 2 days"
- **Impact**: Multiple invoice-related conversations from a client with near-zero platform utilization is a warning signal. Billing friction on an at-risk account can accelerate churn consideration.
- **Root**: Recurring billing questions may reflect unclear invoicing processes or, more concerning, the client internally questioning value-for-money given how little the platform is being used.
- **Action**: Ensure billing communications are crisp and proactive. Monitor this pattern — billing questions from an account with immediate churn risk and $24K ARR are a classic cancellation precursor. Raise with account management if the pattern continues.

**3. Configuration & Feature Gaps** (2 tickets)
- "Re: eCat Sales Portal check in" (config issue, S3 medium, L2) · "Re: eCat Sales Portal check in" (feature request — email template conditional logic)
- **Impact**: A config issue and a feature gap in the Sales Portal signal that the platform is not fully tailored to Jonathan Charles's workflow. The email template request (wanting conditional logic to hide empty product fields) indicates their product data inconsistency is creating a visible quality problem in client-facing emails.
- **Root**: Sales Portal implementation appears incomplete. The email template limitation is a known product gap now tracked as EBR-717 in Jira (see §4).
- **Action**: Address remaining Sales Portal config issues. Prioritize EBR-717 to remove a tangible adoption friction point — when emails look "janky" (their word), reps stop using the email workflow.

### Escalation Profile

7 L1 (frontline resolved), 3 L2 (required internal collaboration). Peak severity: S3 (medium) on 2 tickets. No L3 engineering escalations or L4 executive escalations. Support interactions are low-intensity — the risk is not support burden, it is silence.

### Open Tickets (0)

No currently open HelpScout conversations. All 10 tickets in the 180-day window are closed.

---

## Active Engineering & Projects

| Key | Summary | Status | Priority | Project | Age (days) | Days Since Update |
|---|---|---|---|---|---|---|
| [SERV-2314](https://supercatsolutions.atlassian.net/browse/SERV-2314) | eCat Online — item_numbers URL parameter causes Internal Server Error | Ready to Accept | Low | Server | 76 | 5 |
| [EBR-717](https://supercatsolutions.atlassian.net/browse/EBR-717) | Email Templates — Add conditional logic to hide empty fields and labels | Submitted | Low | EBR | 90 | 76 ⚠️ STALE |

**Flags:**
- 🔴 **Stale**: EBR-717 has had no update in 76 days. This is the email template feature request originating from Jonathan Charles (HelpScout conversation #3204928793, feature request from Thao Phung). Unassigned and sitting in "Submitted" status.
- SERV-2314 is active (updated 5 days ago) and progressing through the pipeline — no flag.

**Cross-Surface Links:**
- **EBR-717 ↔ Support Theme 3** (Configuration & Feature Gaps): This Jira ticket was created directly from HelpScout conversation #3204928793, where Jonathan Charles requested conditional logic in email templates to hide empty fields. The ticket description references the client by name and links back to the HelpScout thread. This is the most direct engineering connection to support friction.
- **SERV-2314 ↔ eCat Online usage**: The item_numbers URL bug affects eCat Online, which is part of Jonathan Charles's bundle. While Low priority, a server error on a core URL parameter could degrade the catalog browsing experience for their dealers.

---

## Meeting Playbook

### Talking Points

1. **Zero eCat orders since December 2025 — the external report's top finding — maps directly to health collapse** — The external report highlights $1.44M in market-show-only GMV and a 35.1% capture rate when active. Internally, this market-show dependency drove Trajectory to 0 and triggered RM-2, capping health at 20. The meeting must address whether sustained between-show ordering is achievable or if this account will permanently operate in burst mode.

2. **"Feature breadth matches top performers" is both the opportunity and the frustration** — The peer benchmark section of the external report shows Jonathan Charles has all 6 benchmarked capabilities active, including CPQ and Kit Items (rare among peers). Internally, Adoption scores just 33 because volume thresholds are not met. The platform infrastructure is there; the usage is not. This is the case for a focused re-engagement rather than feature enablement.

3. **Operational Health is the one thing to protect and build on** — The external report notes daily product updates and 349 library resources. Internally, Operational Health at 82 (Thriving) proves the data pipeline works. The 35-day-stale customer data is the one gap to fix — refreshing it is a quick win to show responsiveness before the meeting.

### Not in the External Report

- **Health score: 20/100 (At Risk)** with Intervene classification — this account requires an immediate save/recovery plan
- **Active churn risk at immediate severity** — RM-2 fired due to >60% primary value decline combined with Value Delivery score below 20
- **Support pattern**: 10 conversations in 180 days — training-dominated (5) and billing-inquiry-heavy (4), with billing questions from a dormant-usage account being a cancellation leading indicator
- **No expansion readiness** — this account requires stabilization first; all growth signals are secondary to preventing churn
- **Jira backlog**: EBR-717 (email template enhancement requested by JC) is stale at 76 days with no assignee

### SuperCat Action Items

- [ ] **Enable Clicky Analytics** — `has_clicky_portal` = false for a Sales Portal bundle account. Enabling Clicky would provide portal traffic intelligence and potentially reveal dealer engagement patterns that are invisible today.
- [ ] **Refresh customer data** — Customer lists and all-channel order history are 35 days stale while products update daily. Restoring Sales Intelligence Dashboard currency is a quick win ahead of the meeting.
- [ ] **Update or close EBR-717** — The email template feature request from Jonathan Charles has been stale for 76 days with no assignee. Either prioritize it as an adoption friction removal or communicate timeline to the client.
- [ ] **Develop account recovery plan** — Health 20, Trajectory 0, Value Delivery 10. This account needs a structured re-engagement strategy focused on converting market-show-only ordering into sustained between-event platform usage. The $24K ARR is at immediate risk.
