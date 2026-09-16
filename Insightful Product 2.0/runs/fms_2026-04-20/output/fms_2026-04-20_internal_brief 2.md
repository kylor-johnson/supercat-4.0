# Internal Intelligence Brief — Visual Comfort - Studio /Fans

*2026-04-20 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Visual Comfort - Studio /Fans is a thriving iPad-only account with near-perfect platform health (88) and strong expansion signals. The meeting should be offense-focused: the $882K rep disengagement risk and stale configuration data are the only two threads to manage, and both are addressable. The external report will highlight two silent high-value reps and 1,278 lapsed buyers — internally, the expansion case is strong (bundle upgrade signal at 100), and the support profile is essentially clean with just 2 conversations in 180 days.

**Three Things That Matter:**

1. **$882K in rep GMV has gone silent** — Beth Miller ($575K) and Charity Queen ($307K) have zero iPad orders in the current 90-day period despite active logins. The external report will surface this. Be ready to discuss whether this is seasonal, role-related, or disengagement — it is the single largest near-term risk to this account's value realization.
2. **Stale configuration data is the one fixable gap** — 10 entity types (price levels, options, kit items) have been frozen since August 2025, dragging Operational Health to 54 (Watch). This is the sole reason the account isn't top quartile across all 5 peer benchmark dimensions. A config refresh is a SuperCat action item, not a client ask.
3. **Expansion-ready: bundle upgrade signal is strongest lever** — iPad-only bundle with all 7 features adopted, perfect presentation scores, and accelerating trajectory. Evidence supports a conversation about eCat Online or Cart capabilities, but health first — resolve the config staleness before pushing expansion.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 88/100 | Expand |
| **Band** | Thriving | |

> Visual Comfort - Studio /Fans (iPad-only) scores 88 Health → Expand. Trajectory (100) drives health; strong platform adoption across all available features.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 80 | Thriving | Strong login activity and active user ratio across the 23-rep sales team. Login intensity and user activation both score in the top tier, reflecting a team that uses the iPad app as a core selling tool. |
| Adoption (20%) | 100 | Thriving | Perfect score — all 7 available features for the iPad-only bundle are in active use above minimum thresholds: product search, customer selection, presentations, email sharing, PDF catalogs, document viewing, and stacks/lists. |
| Value Delivery (30%) | 100 | Thriving | For iPad-only bundles, Value Delivery equals the presentation score. A perfect 100 means presentation actions (magic button adds, email drafts, PDF catalogs, document emails) exceeded 1,000 in the 90-day period — the highest threshold. This team is generating substantial selling activity through the platform. |
| Operational Health (15%) | 54 | Watch | The weak spot. Driven by stale configuration data — 10 entity types (price levels, options, kit items, and 7 others) have been frozen since August 2025, severely dragging down data freshness. Catalog completeness sits at 85.9% (1,296 products missing images, 772 missing prices). Import health for products, customers, and inventory is functional, but the configuration freeze is the anchor. |
| Trajectory (10%) | 100 | Thriving | Perfect Q/Q trend. Both presentation actions (primary value metric for iPad-only) and login activity are accelerating strongly compared to the prior quarter, indicating increasing team engagement with the platform. |

### Flags

- **hs_lifecycle_stale**: HubSpot lifecycle status shows "Lost" or "Churn" for this org, but the subscription is active in Postgres. This is a data hygiene issue in HubSpot, not a real churn indicator. Should be corrected in HubSpot to align with operational reality.

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Visual Comfort - Studio /Fans's bundle (iPad-only), the formula is:
- **Engagement (25%)** — Are users logging in and actively using the platform? Measures login intensity and active user ratio.
- **Adoption (20%)** — How many of the 7 available features are being used above minimum thresholds? Features include product search, customer selection, presentations, email sharing, PDF catalogs, document viewing, and stacks/lists.
- **Value Delivery (30%)** — Is the platform generating business value? For iPad-only bundles, this measures presentation tool usage — magic button adds, email drafts, PDF catalogs, and document emails. A score of 100 means 1,000+ presentation actions in the 90-day period.
- **Operational Health (15%)** — Is client data clean and current? Import success rate, catalog completeness (images + prices), and data freshness (days since last critical update).
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares presentation actions and login volume between current and prior 90-day periods.

**Classification** determines the recommended action cadence:
- **Expand** — healthy account with strong expansion signals
- **Maintain** — healthy, protect with standard cadence
- **Stabilize First** — needs health improvement before expansion
- **Intervene** — immediate save/recovery plan needed

</details>

---

## Support & Issue Themes

> 2 conversations in 180 days (extended from 90-day window — only 1 conversation in standard period). Low-touch, low-friction account. No active fires.

### Themes

**1. Platform Access & Authentication** (1 ticket)
- "Supercat Login" (2026-04-09) — Sales Portal login issue requiring engineering intervention
- **Impact**: Minor friction, but the escalation to L3 (engineering) for a login issue suggests either an edge case in auth flow or a gap in L1/L2 tooling for this type of issue.
- **Root**: Likely a one-off authentication issue specific to the Sales Portal product, which is not part of their iPad-only bundle. May indicate exploratory use of portal features.
- **Action**: Resolved. No follow-up needed. Note that the Sales Portal mention is interesting given their iPad-only bundle — could be an organic signal of interest in portal capabilities.

**2. User Management** (1 ticket)
- "E cat" (2025-12-30) — resolved at first touch (L1, S4)
- **Impact**: Routine. First-touch resolution indicates a well-handled low-severity request.
- **Root**: Standard user administration workflow.
- **Action**: None. This is the profile of a self-sufficient account.

### Escalation Profile

1 L1, 1 L3. Peak severity: S3 (Supercat Login bug). No L2 or L4 escalations. The L3 escalation for a login issue is noteworthy but was resolved — no pattern of engineering-grade issues.

### Open Tickets (0)

No open tickets. All conversations resolved.

---

## Active Engineering & Projects

3 Jira tickets found related to this client via text search for "fms". All are legacy enhancement requests in Triaging status — none are actively being worked.

| Key | Summary | Status | Priority | Project | Age (days) | Days Since Update |
|---|---|---|---|---|---|---|
| [EBR-300](https://supercatsolutions.atlassian.net/browse/EBR-300) | Showroom reporting (Moes and FMS requests) | Triaging | High | EBR | 1,531 | 234 |
| [EBR-90](https://supercatsolutions.atlassian.net/browse/EBR-90) | Capture dealer stock inventories | Triaging | Medium | EBR | 1,818 | 234 |
| [EBR-174](https://supercatsolutions.atlassian.net/browse/EBR-174) | Integrate Placements On Display with sales data | Triaging | Lowest | EBR | 1,733 | 234 |

**Flags:**
- **Stale**: All 3 tickets have had no update in 234+ days (last touched 2025-08-30). These appear to be dormant backlog items rather than active work.
- **High priority**: EBR-300 (Showroom reporting) is marked High but has been in Triaging for 4+ years with no assignee.
- **No blocked tickets.**

**Cross-Surface Links:**
- No HelpScout tickets tagged `status: logged on jira`.
- EBR-300 (showroom reporting) connects to the external report's Sales Team Performance section — the team has 5 showroom accounts excluded from rep analysis, and showroom reporting was a specific FMS request.
- EBR-90 (dealer stock inventories) connects to the external report's Product & Inventory section — inventory capture at dealer locations would complement the existing product catalog and OOS tracking capabilities.

---

## Meeting Playbook

### Talking Points

1. **External report highlights $882K in silent rep GMV** — internally, health is 88 (Thriving) and trajectory is perfect (100), so this is not a systemic engagement problem. It's concentrated in two high-value specialists (Beth Miller, Charity Queen) who may be seasonal or role-shifted. The meeting question: "Has anything changed with these reps?" is a natural opener.
2. **External report flags 10 configuration entities frozen since August 2025** — internally, this drags Operational Health to 54 (Watch) and is the sole reason for a below-median peer benchmark in one dimension. This is a SuperCat action item: prepare to explain what a config refresh involves and offer to execute it. Closing this gap makes the account top quartile across all 5 dimensions.
3. **External report surfaces 1,278 lapsed eCat buyers** — internally, Value Delivery is perfect (100) and adoption is 100%, meaning the platform is delivering value for active users. The lapsed buyer opportunity is about extending that value to more of the customer base, not about fixing a platform problem. This aligns with the Expand classification.

### Not in the External Report

- **Health score: 88/100 (Thriving)** — Classification: Expand. This is an internal-only metric. The account is in the top health tier.
- **No churn risk** — No risk modifiers fired. Subscription is active. The hs_lifecycle_stale flag in HubSpot is a data hygiene issue, not a real concern.
- **Expansion readiness: bundle upgrade signal** — The iPad-only bundle shows strong behavioral signals for upgrade (high presentation volume, team scale, potential ordering interest). This is the strongest growth lever but should be discussed internally before presenting to the client.
- **Support history: 2 conversations in 180 days** — Extremely low-touch account. Both resolved. No patterns of concern.
- **HubSpot lifecycle stale** — HubSpot shows "Lost"/"Churn" status for this org despite an active subscription. This should be corrected in HubSpot as a data hygiene task.
- **3 dormant Jira tickets** — All in Triaging, none updated in 234+ days. These are legacy enhancement requests (showroom reporting, stock inventories, placement analytics) that may be worth revisiting in the context of an expansion conversation.

### SuperCat Action Items

- [ ] **Refresh stale configuration data** — 10 entity types frozen since August 2025 (price levels, options, kit items). This is the root cause of the below-median operational benchmark and the only gap in an otherwise top-quartile account. Execute before or immediately after the meeting.
- [ ] **Correct HubSpot lifecycle status** — `hs_lifecycle_stale` flag is true. Update HubSpot to reflect active subscription status. This is a data hygiene task, not a client conversation.
- [ ] **Review 3 stale Jira tickets** — EBR-300 (showroom reporting, High priority), EBR-90 (stock inventories), EBR-174 (placement analytics) are all 234+ days stale. Close or update before the meeting — having 4-year-old unresolved enhancement requests is a bad look if the client asks about them.
- [ ] **Prepare expansion talking points** — Bundle upgrade signal is at 100. If the meeting goes well, be ready to discuss eCat Online or Sales Portal capabilities. The "Supercat Login" support ticket for Sales Portal suggests at least one user has explored portal features organically.
