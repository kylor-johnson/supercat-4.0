# Internal Intelligence Brief — Kindel Karges Furniture

*April 23, 2026 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Kindel Karges Furniture is an underperforming account with excellent infrastructure but lapsed usage. Health is 56 (Watch), classified as Intervene. The platform is well-maintained — Operational Health is a perfect 100, catalog completeness is 99.6%, and imports are running error-free — but the team hasn't placed an order in 9 months and Value Delivery is critically low at 40. This meeting should focus on re-engagement: getting reps back on the platform with refreshed config data and a focused ordering pilot.

**Three Things That Matter:**

1. **Value Delivery is the health deficit** — At 40/100, presentation tool usage is critically low and dragging the overall health score. The external report shows $1.08M in historical GMV through July 2024, proving the platform delivers value when actively used.
2. **Infrastructure is ready for re-engagement** — Operational Health is a perfect 100 with 99.6% catalog completeness and error-free imports in April 2026. The foundation is solid; the problem is activating usage, not fixing the platform.
3. **12 stale config entities block ordering** — Pricing, options, and inventory data frozen since August 2025 must be refreshed before reps can reliably process orders. This is a SuperCat-side prerequisite for any re-engagement plan.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 56/100 | Intervene |
| **Band** | Watch | |

> Kindel Karges Furniture (iPad-only) scores 56 Health → Intervene. Value Delivery (40) is critically low; immediate attention required.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 50 | 🟡 Watch | Login activity and active user ratio are moderate. 24 active users out of 42 total — below the peer median of 60. The team is using the platform for browsing and catalog work but not with the consistency of a healthy account. |
| Adoption (20%) | 57 | 🟡 Watch | 57% feature adoption for iPad-only. Active features include Library, Product Search, PDF Catalog, and Configurable Items — ahead of many peers on configurables (only 19% of peers use them). Sales Portal is enabled but not active; Kit Items are not configured. |
| Value Delivery (30%) | 40 | 🟡 Watch | For iPad-only bundles, Value Delivery measures presentation tool usage (email, PDF, sharing). At 40, this is on par with the peer median but critically low for health. Presentation activity exists (253 PDF Catalog events, 846 Library views) but isn't generating enough business value throughput. |
| Operational Health (15%) | 100 | 🟢 Thriving | Perfect score. Import pipeline is running cleanly (41 error-free imports in April 2026 after reactivation), catalog completeness is 99.6% (766 products, only 3 missing images, 0 missing prices). This is well above the peer median of 65 and in the top quartile. |
| Trajectory (10%) | 50 | 🟡 Watch | Flat to slightly positive Q/Q trend. The April 2026 import pipeline reactivation after a 5-month gap is a positive signal, and the account ranks in the top 30% of peers on trajectory. However, no ordering activity in 9 months keeps this from being a strong positive. |

### Flags

- **hs_lifecycle_stale**: True — lifecycle data is stale, which may affect engagement and adoption scoring accuracy.
- No churn risk detected.
- No risk modifier applied.
- No ARR data gap.

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Kindel Karges Furniture's bundle (iPad-only), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform?
- **Adoption (20%)** — How many available features are being used above minimum thresholds?
- **Value Delivery (30%)** — Is the platform generating business value? For iPad-only bundles, this measures presentation tool usage — email presentations, PDF catalogs, and sharing activity.
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

> 4 conversations in 180 days (extended window — only 1 in the last 90 days). Low-volume, operationally diverse, all resolved. No active fires.

### Themes

**1. eCat App Support** (2 tickets)

- "Re: eCat Issues for Baker Taiwan Team" (Mar 2026, training)
- "Re: Sync Error for iPad App" (Jan 2026, bug — S3, required L3 engineering intervention)
- **Impact**: The Baker Taiwan team needed help with eCat app workflows, and a sync error required engineering to resolve. These are standard operational issues but the sync bug signals potential friction points for re-engagement.
- **Root**: The training request suggests reps in the broader Baker Interiors Group network need onboarding support. The sync error may relate to the stale configuration data.
- **Action**: Ensure sync issues are fully resolved before pushing a re-engagement pilot. Prepare onboarding materials for Baker Interiors Group team members.

**2. Platform Configuration & Pricing** (2 tickets)

- "Re: Custom Field Question" (Dec 2025, config issue — L2, required internal collaboration, meeting scheduled)
- "eCat Online Pricing Request" (Jan 2026, sales and finance)
- **Impact**: Configuration questions and pricing inquiries indicate the client is actively thinking about how to use the platform — a positive engagement signal despite the ordering gap.
- **Root**: Custom field configuration complexity and pricing setup for eCat Online are common needs when accounts are preparing to increase usage.
- **Action**: The "meeting scheduled" status on the custom field ticket suggests an active engagement thread. Follow up on the outcome of that meeting before the QBR.

### Escalation Profile

2 L1 (frontline), 1 L2 (internal collaboration), 1 L3 (engineering). Peak severity: S3 (iPad sync error). No L4 executive escalations. No S1/S2 critical or high-severity issues.

### Open Tickets (0)

No open tickets. All 4 conversations in the 180-day window are resolved.

---

## Active Engineering & Projects

No active Jira tickets found for this client.

**Search strategies attempted:**
- `text ~ "Kindel Karges" AND statusCategory != Done` → 0 results
- `text ~ "kkc" AND statusCategory != Done` → 0 results
- `text ~ "Kindel" AND statusCategory != Done` → 0 results

No HelpScout tickets tagged `status: logged on jira`. The L3 engineering intervention on the sync error (Jan 2026) was resolved without a Jira ticket, or the ticket has since been completed.

---

## Meeting Playbook

### Talking Points

1. **Stale config data is the re-engagement blocker** — External report flags 12 entities frozen since August 2025 (pricing, options, inventory). Internally, this hasn't dragged Operational Health (which measures import success and catalog completeness at 100), but it's a prerequisite for ordering. Prepare to walk the client through what a config refresh involves and timeline.
2. **$1.08M GMV history proves platform value** — External report highlights 41 orders totaling $1.08M through July 2024, all via iPad. Internally, Value Delivery is at 40 (Watch) because presentation activity has slowed. The opportunity is reactivation, not activation — this account knows how to use the platform.
3. **Import pipeline reactivation is a positive signal** — 41 imports in April 2026 after a 5-month gap shows someone on the client side is actively maintaining the platform. This aligns with the support activity (pricing inquiry, config questions) and suggests internal momentum toward re-engagement.

### Not in the External Report

- **Health score**: 56/100, Watch band — not at-risk, but needs intervention to recover Value Delivery
- **Classification**: Intervene — the model recommends an active save/recovery plan rather than standard cadence
- **No churn risk** detected despite the 9-month ordering gap — infrastructure health and continued platform engagement prevent the risk flags from firing
- **Support history**: Minimal (4 conversations in 180 days), all resolved, low severity — this is not a high-touch support account
- **Warning flag**: `hs_lifecycle_stale` — lifecycle data staleness may slightly depress engagement and adoption scores
- **Expansion readiness**: Not ready — health must improve before expansion signals activate

### SuperCat Action Items

- [ ] **Enable Clicky Analytics** — `has_clicky_portal` is false. Enable for portal traffic intelligence, especially with the Sales Portal enabled but not actively used.
- [ ] **Refresh stale configuration data** — 12 entities (pricing, options, inventory) frozen since August 2025 are the primary blocker for ordering re-engagement. This is a SuperCat-side action.
- [ ] **Follow up on "Custom Field Question" meeting** — The Dec 2025 support ticket had `status: meeting scheduled`. Confirm outcome and whether follow-up actions were completed.
- [ ] **Prepare re-engagement pilot plan** — With infrastructure at 100 and a clean catalog, the account is ready for a structured re-engagement with 2–3 reps once config data is refreshed.
