# Internal Intelligence Brief — Magnussen Home

*2026-04-20 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Magnussen Home is a healthy account with genuine expansion potential, but two drag factors — stale operational data and a declining activity trajectory — need attention before the expansion conversation lands credibly. Health sits at 70 (Healthy) with peer-leading engagement and maximum adoption, yet Operational Health (30) and Trajectory (20) are both At Risk. The meeting should lean offense: use the deep platform penetration as proof of value while addressing the data pipeline freeze and re-engagement opportunities the external report will surface.

**Three Things That Matter:**

1. **Stale data pipeline drags Operational Health to 30** — Eight data entities have been frozen since August 2025 (256 days), including inventory, product options, and riser prices. Restoring this secondary import pipeline is the single highest-impact action for health improvement and aligns directly with the external report's top priority action.
2. **Expansion-ready but Trajectory is declining** — Classification is Expand with all 7 iPad features adopted, but Q/Q activity is trending down (Trajectory: 20). The 306 lapsed buyers and three disengaging top reps flagged in the external report confirm the velocity slowdown behind this score.
3. **10 stale Jira enhancement requests spanning 3 years** — Magnussen has 10 open enhancement requests, all in Triaging status, including a Highest-priority item (EBR-520: display placements for 100+ locations) filed in December 2023. None have been updated since August 2025.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 70/100 | Expand |
| **Band** | Healthy | |

> 70 Health → Expand. Adoption (100) drives health.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 80 | 🟢 Healthy | Login frequency and active user ratio are both strong — top 5% of the iPad-only peer cohort. The team is logging in regularly and using the platform actively. |
| Adoption (20%) | 100 | 🟢 Thriving | All 7 available features for the iPad-only bundle are being used above minimum thresholds — the highest adoption score in the peer cohort. Product search, presentations, email sharing, PDF catalogs, document viewing, and stacks are all active. |
| Value Delivery (30%) | 80 | 🟢 Healthy | For iPad-only, this measures presentation tool activity (emails drafted, PDFs created, items shared). Score of 80 indicates healthy presentation volume across the team. |
| Operational Health (15%) | 30 | 🔴 At Risk | Data freshness is the primary drag: 8 of 22 data entities have been frozen since August 2025 (256 days), including inventory, product options, and riser prices. Catalog completeness is strong at 96.7%, and the primary import pipeline runs daily — the secondary pipeline stalled. |
| Trajectory (10%) | 20 | 🔴 At Risk | Q/Q activity is declining. Key rep disengagement (Burnett, Tripoli at zero recent activity) and declining order cadence from top contributors (Champoux down 63% QoQ) are driving the downward trend. |

### Flags

- ⚠️ **hs_lifecycle_stale**: HubSpot lifecycle status is stale (showing Lost/Churn despite active subscription). Follow-up needed to update HubSpot records.
- ⚠️ **hs_join_missing**: No HubSpot company join exists for this org. HubSpot data cannot be joined for lifecycle or vertical context.
- No risk modifier applied. No churn risk.

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Magnussen Home's bundle (iPad-only), the formula is:
- **Engagement (25%)** — Are users logging in and actively using the platform?
- **Adoption (20%)** — How many available features are being used above minimum thresholds?
- **Value Delivery (30%)** — Is the platform generating business value? For iPad-only bundles, this measures presentation tool activity — emails drafted, PDFs created, items shared via the app.
- **Operational Health (15%)** — Is client data clean and current? Import success, catalog completeness, data freshness.
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter?

**Classification** determines the recommended action cadence:
- **Expand** — healthy account with strong expansion signals
- **Maintain** — healthy, protect with standard cadence
- **Stabilize First** — needs health improvement before expansion
- **Intervene** — immediate save/recovery plan needed

</details>

---

## Support & Issue Themes

> 3 conversations in 90 days. Engineering-forward, low volume. No active fires.

### Themes

**1. Platform Bug — Product Notes Feature** (1 ticket)
- "The Product Notes feature in eCat is not available."
- **Impact**: Feature regression affecting client workflow. Required L3 engineering intervention at S2 (high) severity.
- **Root**: Likely a release-related regression or configuration issue in the Product Notes feature, which is tracked as an in-progress epic (ECAT-1018) in Jira.
- **Action**: Confirm resolution is complete and verify with the client that Product Notes is functional. Connect to ECAT-1018 status in the meeting if raised.

**2. Market Preparation Admin** (1 ticket)
- "Reset Magnussen Commitments and Interests data for HP April Market 2026"
- **Impact**: Pre-market data resets are a recurring operational need that requires manual engineering intervention (L3). This is a workflow gap, not a platform failure.
- **Root**: No self-service mechanism for resetting market-specific Commitments & Interests data. Related to SERV-1714 (Multi-Market C&I epic) which remains in To Do status.
- **Action**: Evaluate whether self-service market data resets should be prioritized — this manual process will recur at every market cycle.

**3. User Access — eCat Pop Box** (1 ticket)
- "eCAT Pop Box"
- **Impact**: Low-severity (S4) user management question handled at L1. Routine support interaction.
- **Root**: Standard user onboarding/access question.
- **Action**: No action needed. Resolved at frontline.

### Escalation Profile

1 L1, 2 L3. Peak severity: S2 (Product Notes bug). No L2 or L4 escalations. Two-thirds of conversations required engineering intervention — notable for a 3-ticket sample.

### Open Tickets (0)

No open support tickets. All 3 conversations in the 90-day window are resolved.

---

## Active Engineering & Projects

10 open Jira tickets related to Magnussen Home. All are stale (no updates since August 2025 or earlier). The backlog is concentrated in the Enhancements and Bug Requests (EBR) project and reflects long-standing feature requests that have not progressed through triage.

### Recent / Active

| Key | Summary | Project | Status | Priority | Age | Days Since Update |
|---|---|---|---|---|---|---|
| [ECAT-1018](https://supercatsolutions.atlassian.net/browse/ECAT-1018) | Product Notes | eCat | In Progress | Unprioritized | 791d | 532d |
| [EBR-604](https://supercatsolutions.atlassian.net/browse/EBR-604) | Truncating decimals in price rounding (Magnussen) | EBR | Triaging | High | 454d | 234d |
| [SERV-1714](https://supercatsolutions.atlassian.net/browse/SERV-1714) | Multi-Market commitments and interests | Server | To Do | Unprioritized | 740d | 553d |

### Backlog (7 Enhancement Requests)

| Key | Summary | Priority | Age | Days Since Update |
|---|---|---|---|---|
| [EBR-520](https://supercatsolutions.atlassian.net/browse/EBR-520) | Display placements for 100+ locations (Magnussen) | Highest | 868d | 234d |
| [EBR-461](https://supercatsolutions.atlassian.net/browse/EBR-461) | Smart List product filtering (Magnussen) | High | 1,052d | 234d |
| [EBR-443](https://supercatsolutions.atlassian.net/browse/EBR-443) | Contract Pricing by ship-to and channel (Magnussen) | High | 1,113d | 234d |
| [EBR-539](https://supercatsolutions.atlassian.net/browse/EBR-539) | Library management API (Magnussen) | Unprioritized | 813d | 234d |
| [EBR-473](https://supercatsolutions.atlassian.net/browse/EBR-473) | Placement quantities (Magnussen) | Medium | 1,015d | 234d |
| [EBR-448](https://supercatsolutions.atlassian.net/browse/EBR-448) | Product black/whitelisting (Magnussen) | Unprioritized | 1,098d | 234d |
| [EBR-447](https://supercatsolutions.atlassian.net/browse/EBR-447) | Currency in sales data (Magnussen) | Unprioritized | 1,098d | 234d |

**Flags:**
- 🔴 **Stale**: All 10 tickets are stale (no update in 14+ days). Most haven't been touched since August 2025.
- 🔴 **High Priority**: EBR-520 (Highest), EBR-604 (High), EBR-461 (High), EBR-443 (High) — 4 tickets at High or above.
- No blocked tickets.

### Cross-Surface Links

- **ECAT-1018 (Product Notes)** directly addresses the recent support ticket about Product Notes being unavailable. The feature is tracked as In Progress but hasn't been updated in 532 days — the support ticket suggests it may have regressed or wasn't fully deployed.
- **SERV-1714 (Multi-Market C&I)** relates to the support request for market data resets. The manual work required for each market cycle could be eliminated if this epic progresses.

---

## Meeting Playbook

### Talking Points

1. **Dormant buyer reactivation is the headline opportunity** — The external report surfaces 306 lapsed buyers with $381K in dormant historical value. Internally, the declining Trajectory (20) confirms the velocity slowdown. Reactivation is a natural conversation topic that bridges the external report's findings with our expansion thesis.
2. **Data pipeline freeze is actionable and visible** — The external report flags 8 stale data entities since August 2025 as a top priority action. Internally, this drives Operational Health to 30 (At Risk). Come prepared to explain what restoring the secondary import pipeline involves and timeline it.
3. **Peer-leading adoption supports the value narrative** — Engagement (80, top 5%) and Adoption (100, highest in cohort) are strong proof points in the external report's peer benchmarking section. Lean into these during the meeting to anchor the relationship in demonstrated platform value before surfacing improvement areas.

### Not in the External Report

- **Health Score**: 70 / 100 (Healthy) — Classification: Expand
- **No churn risk** — no risk modifiers fired
- **Expansion readiness**: Bundle upgrade signal is strong; behavioral evidence suggests the account is outgrowing iPad-only
- **Support history**: 3 conversations in 90 days, all resolved. Engineering-forward (2 of 3 at L3). No active fires.
- **Jira backlog**: 10 stale enhancement requests, including 4 at High/Highest priority. Oldest is 3+ years. Client may raise undelivered feature requests.
- **Data quality warnings**: HubSpot lifecycle stale, HubSpot join missing. Neither affects scoring but both need cleanup.

### SuperCat Action Items

- [ ] **Enable Clicky Analytics** — `has_clicky_portal` is false. Enabling would provide portal traffic intelligence for future reporting.
- [ ] **Restore stale secondary import pipeline** — 8 data entities frozen since August 2025. Primary driver of Operational Health (30) and the external report's #1 priority action.
- [ ] **Triage stale Jira backlog** — 10 Magnussen-specific tickets, all stale. EBR-520 (Highest priority, display placements) has been in Triaging for 2+ years. Update or close before the client meeting to avoid being caught off-guard.
- [ ] **Update HubSpot records** — hs_lifecycle_stale and hs_join_missing flags indicate stale/missing HubSpot data. Update lifecycle status and establish company join.
