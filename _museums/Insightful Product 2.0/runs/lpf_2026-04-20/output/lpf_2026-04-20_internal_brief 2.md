# Internal Intelligence Brief — Linon/Powell Furniture

*2026-04-20 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Linon/Powell Furniture is a healthy, stable Full-bundle account in standard-cadence mode. Platform adoption is perfect (100/100) and Value Delivery is strong at 85, driven by solid order volume across both iPad and eCat Online channels. The meeting should focus on two data quality opportunities — the 45% catalog completeness gap and stale configuration data — which are the clearest paths to lifting Operational Health from its current Watch band into Healthy territory.

**Three Things That Matter:**

1. **Catalog completeness at 45% is the #1 data gap** — 2,564 products are missing pricing data, dragging Operational Health to 56 and sitting 49 points below the peer median. Addressing this is the single highest-impact action item for this account.
2. **Live inventory initiative stalled for 14+ months** — EBR-600 (High priority) and SERV-2069 both track "Live inventory (Linon)" with no updates since February 2025. This initiative would reduce the manual import friction seen in recurring support tickets and should be re-evaluated.
3. **718 lapsed eCat buyers are the biggest growth conversation** — The external report identifies $200K+ in dormant account value. With Value Delivery already at 85, the re-engagement campaign is a pure-upside discussion with no platform health risk.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 69/100 | Maintain |
| **Band** | Healthy | |

> Linon/Powell Furniture (Full) scores 69 Health → Maintain. Adoption (100) leads health; stable with standard cadence.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 40 | 🟡 Watch | Login intensity and active user ratio sit below the healthy threshold. With 69 users provisioned across the Full bundle, the proportion regularly logging in is modest — peer benchmark confirms engagement is below the cohort median. |
| Adoption (20%) | 100 | 🟢 Thriving | Perfect score. All 10 features available for the Full bundle are in active use above minimum thresholds — product search, customer selection, presentations, email sharing, PDF catalogs, document viewing, stacks, eCat Online, order submission, and Sales Portal. |
| Value Delivery (30%) | 85 | 🟢 Thriving | Strong across all four Full-bundle components: order volume, customer activation, eCat Online share (56% of orders flow through eOL), and portal engagement. Value Delivery is in the top 10% of the peer cohort. |
| Operational Health (15%) | 56 | 🟡 Watch | The weak spot. Catalog completeness sits at 45% (2,564 products missing pricing), and 12 configuration entities are stale since August 2025 (242 days). Data freshness scores near zero on the >180-day threshold, pulling this dimension into Watch band. |
| Trajectory (10%) | 50 | 🟡 Watch | Flat quarter-over-quarter — neither meaningfully accelerating nor declining. Peer median for trajectory is 80, placing Linon/Powell in the bottom quartile for momentum. |

### Flags

No flags. No risk modifiers fired. No churn risk. All warning flags clear (hs_lifecycle_stale: false, hs_join_missing: false, arr_data_gap: false).

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Linon/Powell Furniture's bundle (Full), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measures login intensity (logins per active user) and active user ratio (active users / total users).
- **Adoption (20%)** — How many available features are being used above minimum thresholds? For Full bundles, all 10 features are scored: product search, customer selection, presentations, email sharing, PDF catalogs, document viewing, stacks, eCat Online, order submission, and Sales Portal.
- **Value Delivery (30%)** — Is the platform generating business value? For Full bundles, this averages four components: order volume score, customer activation score, eCat Online share score, and portal engagement score.
- **Operational Health (15%)** — Is client data clean and current? Import success rate, catalog completeness (% of products with images + pricing), and data freshness (days since last critical update).
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares current 90-day order volume and login count against the prior 90-day period.

**Classification** determines the recommended action cadence:
- **Expand** — healthy account with strong expansion signals
- **Maintain** — healthy, protect with standard cadence
- **Stabilize First** — needs health improvement before expansion
- **Intervene** — immediate save/recovery plan needed

</details>

---

## Support & Issue Themes

> 6 conversations in 90 days. Data-import and platform-ops forward, low volume. No active fires.

### Themes

**1. Data Sync & Import Issues** (2 tickets)

- "RE: FW: AC Chairs Unreleased for ECAT" (Jan 25, L3/S3), "RE: FW: AC Chairs Unreleased for ECAT" (Feb 13, L1/S4)
- **Impact**: Recurring issues around product release/import workflows indicate friction in the data pipeline between Linon's ERP and the eCat platform. Both tickets required multiple threads (8 each) to resolve.
- **Root**: Product release configuration requires manual intervention — unreleased items don't flow through automatically, creating a repeated support cycle.
- **Action**: Explore automating the product release workflow during the meeting. The in-flight "Live inventory" Jira initiative (EBR-600) would address this root cause if completed.

**2. Order Integration Bug** (1 ticket)

- "Re: FW: Thank you for your order" (Mar 9, L3/S3)
- **Impact**: An order confirmation email issue required engineering intervention (L3, S3). This is the highest-severity ticket in the window and the only bug classification.
- **Root**: Order confirmation email behavior not functioning as expected — likely a configuration or template gap in the order pipeline.
- **Action**: Confirm the fix is deployed and stable. Monitor for recurrence.

**3. General Platform Operations** (3 tickets)

- "Re: Smartlist with all images" (Apr 15, L1/S4), "Re: Linon - export to excel not working" (Mar 3, L1/S4), "Website Customization Capabilities" (Feb 13, L1/S4)
- **Impact**: Mix of image management, training/how-to, and feature exploration for eCat Online customization. Indicates an engaged team probing platform boundaries — not a systemic issue.
- **Root**: Standard operational questions from active users.
- **Action**: No intervention needed. The feature request for website customization (eCat Online) is worth noting for the product roadmap.

### Escalation Profile

4 L1, 2 L3. Peak severity: S3 (order confirmation bug, data import issues). No L2 or L4 executive escalations. The L3 tickets were resolved without client impact escalation.

### Open Tickets (0)

No open tickets. All 6 conversations in the 90-day window are resolved.

---

## Active Engineering & Projects

2 unique initiatives across 3 Jira tickets. Both "Live inventory" tickets track the same initiative in different projects.

| Key | Summary | Project | Status | Priority | Age (days) | Days Since Update |
|---|---|---|---|---|---|---|
| [EBR-600](https://supercatsolutions.atlassian.net/browse/EBR-600) | Live inventory (Linon) | EBR | In Progress | High | 456 | 435 |
| [SERV-2069](https://supercatsolutions.atlassian.net/browse/SERV-2069) | Live inventory (Linon) | Server | To Do | Unprioritized | 440 | 424 |
| [EBR-250](https://supercatsolutions.atlassian.net/browse/EBR-250) | Full price level switching in eOL | EBR | Triaging | Lowest | 1,604 | 234 |

**Flags:**

- 🔴 **STALE**: All 3 tickets have had no updates in 14+ days. EBR-600 and SERV-2069 have been untouched for **14+ months**.
- 🔴 **HIGH PRIORITY**: EBR-600 is marked High priority but has been stale for over a year with no assignee.
- No blocked tickets.

**Cross-Surface Links:**

- The **Live inventory** initiative (EBR-600 / SERV-2069) connects directly to the data-sync import support theme — live inventory feeds would eliminate the manual import friction seen in the "AC Chairs Unreleased" HelpScout tickets (L3 escalations).
- **EBR-250** (price level switching in eOL) relates to the external report's catalog completeness gap — 2,564 products missing pricing may be partially due to limitations in how price levels are managed for eCat Online.

---

## Meeting Playbook

### Talking Points

1. **Catalog completeness is the biggest quick win** — External report highlights 45% catalog completeness (2,564 products missing pricing) as the widest peer benchmark gap (43% vs. 92% median). Internally, this directly drags Operational Health to 56. Prioritizing price data for top-selling products would move both the client-visible and internal metrics.
2. **Dormant account re-engagement is pure upside** — External report identifies 718 lapsed eCat buyers representing $200K+ in dormant value. Internally, Value Delivery is already strong at 85 and the platform is fully adopted, so this campaign carries no health risk — it's offense, not defense.
3. **Stale configuration data is a SuperCat-side fix** — External report flags 12 configuration entities stale since August 2025 (242 days). Internally, this contributes to the Operational Health Watch band. A single import cycle could refresh these and move data freshness from near-zero to 80+.

### Not in the External Report

- **Health score: 69/100 (Healthy), Classification: Maintain** — standard cadence, no immediate intervention needed
- **No churn risk.** No risk modifiers fired. Account is stable and complete-scoring.
- **Engagement is the weakest health dimension at 40 (Watch)** — suggests user activation could be improved; not all 69 provisioned users are regularly active
- **Support history**: 6 conversations in 90 days, all resolved. Two required engineering intervention (L3) for data import and order confirmation issues.
- **3 Jira tickets open**, including a High-priority "Live inventory" initiative stale for 14+ months

### SuperCat Action Items

- [ ] **Refresh stale configuration data** — 12 entities (price levels, options, option groups, sales quotas) stale since Aug 2025; a single import cycle would improve Operational Health from 56 toward 70+
- [ ] **Address catalog pricing gap** — 2,564 products missing pricing (45% completeness); coordinate with Linon on price data import, prioritizing top-selling items
- [ ] **Update or close stale Jira tickets** — EBR-600 (High priority, 14+ months untouched) and SERV-2069 need a status check; either advance the live inventory initiative or close with rationale
- [ ] **Investigate low engagement** — Engagement score of 40 with a Full bundle warrants exploration of whether user provisioning is bloated or if targeted training could drive more regular platform use
