# Internal Intelligence Brief — Kindel Karges Furniture

*April 20, 2026 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Kindel Karges Furniture is an account in serious decline that requires immediate intervention. Health scores 56 (Watch band), classification is **Intervene**, and HubSpot lifecycle data flags this account as churned or lost — while the subscription remains technically active. No eCat orders have been submitted in over 12 months, no support history is attributable (no email domain mapping), and no Jira engineering work is in flight. The meeting should be entirely defense-focused: understand what caused the disengagement, commit to a stale-data refresh as the prerequisite for reactivation, and leave with a concrete timeline for returning reps to active selling. This is a save conversation, not an optimization discussion.

**Three Things That Matter:**

1. **HubSpot says this account is lost** — `hs_lifecycle_stale = True` means HubSpot lifecycle status shows "Lost" or "Churn" for Kindel. The subscription is active but the CRM data gap means this account may be falling through the cracks organizationally. Verify the actual account status and update HubSpot before the meeting.
2. **Value Delivery has collapsed to Watch-band levels** — At 40/100, presentation tool usage (the primary value metric for iPad-only bundles) has declined sharply. The external report confirms zero ordering in 12+ months despite 23 users still logging in. The infrastructure is ready (99.6% catalog completeness); the reps have stopped using it to sell.
3. **13 stale configuration entities block any reactivation** — Options, finishes, price levels, inventory, and sales quotas have been stale since August 2025 (255 days). Even if reps returned to active selling tomorrow, they would be presenting outdated data. This refresh is the non-negotiable first step.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 56/100 | Intervene |
| **Band** | Watch | Immediate save/recovery plan required |

> Kindel Karges Furniture (iPad-only) scores 56 Health / 43 Growth → Intervene. Value Delivery (40) is critically low; immediate attention required.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 50 | 🟡 Watch | Login intensity and active user ratio are moderate. 23 users logged in over the past 90 days — the audience exists — but engagement depth falls below the peer median (50 vs. 60). The warm login base is not translating into deep platform usage. |
| Adoption (20%) | 57 | 🟡 Watch | Using roughly 4 of 7 available iPad-only features above minimum thresholds. Library access (834 all-time events), product search (607), and PDF catalog creation (251) are strong historically, but Smart Stacks (0 views) and other features remain dormant. |
| Value Delivery (30%) | 40 | 🟡 Watch | For iPad-only bundles, Value Delivery = presentation tool usage (email sharing, PDF catalogs, document sharing). At 40, presentation activity has declined significantly from historical highs. The reps browse and search but have stopped creating PDFs and sending emails at the volumes that drive this score. The external report confirms the gap is behavioral, not infrastructural. |
| Operational Health (15%) | 100 | 🟢 Thriving | Outstanding. Import pipeline is active (29 imports in April 2026, all clean), catalog completeness is 99.6%, and product data was refreshed 6 days ago. Top-of-class operational health. Note: the model scores import health and catalog completeness but does not penalize stale configuration entities (options, price levels) separately — those are captured in the external report. |
| Trajectory (10%) | 50 | 🟡 Watch | Flat to slightly positive Q/Q trend. The recent import activity surge (April 2026) and continued login base create a modest positive signal despite the 12-month ordering lapse. Trajectory of 50 vs. peer median of 25 places this account in the top 30% for momentum among comparable Furniture accounts. |

### Flags

- **⚠ hs_lifecycle_stale = True** — HubSpot engagement status shows "Lost" or "Churn." The subscription is active and the account is scored, but this flag indicates the CRM lifecycle data is out of sync with operational reality. Immediate follow-up required.
- No risk modifiers fired (RM-1 through RM-4 not triggered)
- No churn risk flag set (health_score ≥ 20 and no risk modifier fired)
- Not expansion ready (health < 60)
- `hs_join_missing = False` — HubSpot join exists
- `arr_data_gap = False` — ARR data present ($9,540)

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Kindel Karges Furniture's bundle (**iPad-only**), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measures login intensity (logins per active user) and active user ratio (active users / total users).
- **Adoption (20%)** — How many available features are being used above minimum thresholds? For iPad-only, 7 features are tracked: Product Search, Customer Selection, Presentations, Email Sharing, PDF Catalogs, Document Viewing, and Stacks/Lists.
- **Value Delivery (30%)** — Is the platform generating business value? For iPad-only bundles, this measures **presentation tool usage**: email sharing + PDF catalog creation + document sharing events in the trailing 90 days.
- **Operational Health (15%)** — Is client data clean and current? Import success rate, catalog completeness (products with image + price), and data freshness (days since last critical update).
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares presentation actions and login totals between the current 90-day period and the prior 90-day period.

**Classification** maps Health × Growth into an action quadrant:
- Health ≥ 60 + Growth ≥ 60 = **Expand** (upsell/cross-sell)
- Health ≥ 60 + Growth < 60 = **Maintain** (protect with standard cadence)
- Health < 60 + Growth ≥ 60 = **Stabilize First** (fix before selling)
- Health < 60 + Growth < 60 = **Intervene** (immediate save/recovery plan)

</details>

---

## Support & Issue Themes

> Support data unavailable — no email domain mapping exists for Kindel Karges Furniture (`kkc`) in the HelpScout attribution system.

No HelpScout conversations can be attributed to this client. The `pg_domain_map.csv` does not contain a domain entry for `kkc`, meaning email-based ticket matching is not possible.

**Implication for the meeting**: We have no visibility into whether Kindel has been contacting support. If the account has been submitting tickets from an unmapped domain, those conversations exist but are invisible to this analysis. Establishing the domain mapping is an immediate action item.

### Open Tickets

No data available.

---

## Active Engineering & Projects

> No Jira tickets found for Kindel Karges Furniture.

**Search strategies attempted:**
1. `text ~ "Kindel" AND statusCategory != Done` → 0 results
2. `text ~ "kkc" AND statusCategory != Done` → 0 results

No active engineering work, client-specific projects, or support escalations are tracked in Jira for this client. This is consistent with the absence of support data — there is no visible internal activity for this account across any system.

---

## Meeting Playbook

### Talking Points

1. **External report frames reactivation — internally, it's an intervention** — The external Customer Intelligence Report positions the catalog readiness and 23 active logins as assets for a reactivation push. Internally, health is 56 (Watch), classification is Intervene, and HubSpot flags the account as lost. The gap between external framing and internal reality means the team should lead with understanding the disengagement before presenting the opportunity.
2. **Operational health masks deeper behavioral decline** — Operational Health scores 100 (Thriving) and the external report highlights top-quartile data infrastructure vs. peers. But Value Delivery (40), Engagement (50), and Adoption (57) are all in Watch band. The infrastructure is excellent; the people have stopped using it. Acknowledge the platform is ready while pressing on what broke in the selling workflow.
3. **13 stale config entities are the tactical prerequisite** — The external report's top priority action is refreshing options, finishes, price levels, and inventory (255 days stale). This aligns with the internal assessment. The meeting should secure a commitment and timeline for this data refresh — it is the gate before any re-engagement effort can begin.

### Not in the External Report

- **Health score: 56/100 (Watch band)** — Classification: Intervene. The external report contains no scoring data.
- **HubSpot lifecycle stale** — `hs_lifecycle_stale = True`. CRM data shows this account as Lost/Churn. Internal data quality issue requiring immediate resolution.
- **No churn risk flag triggered** — Despite the Intervene classification and stale HubSpot status, no formal churn risk flag is set because no risk modifier fired and health is above 20.
- **Support history is invisible** — No email domain mapping for HelpScout attribution. Zero visibility into support interactions.
- **No Jira engineering work** — No tickets in any project. No tracked internal activity.
- **Parent entity: Baker Interiors Group** — Kindel sits under the Baker Interiors Group umbrella. Account decisions may be influenced by parent-entity dynamics.

### SuperCat Action Items

- [ ] **Establish email domain mapping** — Add Kindel's email domain(s) to `pg_domain_map.csv` so future support interactions are attributable. Without this, we have zero visibility into their support experience.
- [ ] **Enable Clicky Analytics** — `has_clicky_portal = false`. Enable for portal traffic intelligence.
- [ ] **Update HubSpot lifecycle status** — `hs_lifecycle_stale = True`. CRM shows Lost/Churn but subscription is active. Reconcile.
- [ ] **Refresh stale configuration data** — Options, finishes, price levels, inventory, and sales quotas are 255 days stale. Coordinate with client to prioritize this refresh.
- [ ] **Confirm bundle classification** — External report identifies bundle as "iPad + Catalog + Portal" but MAL/Health V2 scores as "iPad-only." Verify and update the MAL if needed.
