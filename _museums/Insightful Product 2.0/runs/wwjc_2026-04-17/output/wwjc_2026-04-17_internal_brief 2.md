# Internal Intelligence Brief — Wildwood/Chelsea House

*2026-04-20 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Wildwood/Chelsea House is a healthy, stable Full-bundle account in standard-cadence mode. Health scores 76 (Healthy) with near-perfect Operational Health and strong Value Delivery — eCat captures over 50% of all-channel revenue and 80% of orders flow through buyer self-service. The one drag is Engagement at 40 (Watch), likely a structural artifact of their self-service-heavy ordering model rather than a disengagement signal. No fires, no churn risk, no escalations in progress. The meeting should focus on offense: the massive lapsed-account reactivation opportunity (7,044 accounts) and the open sales data purge request that's awaiting their confirmation.

**Three Things That Matter:**

1. **7,044 lapsed accounts are the biggest growth lever** — The external report will highlight that only 25.4% of accounts that have ever ordered via eCat remain active. Daniel Ratchford's territory alone has 2,457 dormant accounts. This is the headline talking point and should anchor the meeting conversation.

2. **Sales data purge request needs client sign-off** — CSP-36 is logged and engineering is ready, but we're waiting on Wildwood to confirm the time frame and scope for purging stale sales order data. This is tied to HelpScout conversation #3291979476 (Mike Studley, NetSuite Admin). Raise in the meeting — it's blocking.

3. **Engagement score masks strong underlying health** — At 40 (Watch), Engagement is the weakest dimension, but this is structural: 80% of orders come through eCat Online self-service, so iPad login frequency is naturally lower. The real health story is Value Delivery (85) and Adoption (90) — this account is deeply embedded in the platform.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 76/100 | Maintain |
| **Band** | Healthy | Standard cadence |

> Wildwood/Chelsea House (Full) scores 76 Health → Maintain. Operational Health (100) leads; stable with standard cadence.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 40 | 🟡 Watch | Login intensity and active user ratio are moderate. With 80% of orders flowing through eCat Online self-service, iPad login frequency is structurally lower. The large user base (9,400+ accounts) also dilutes active user ratio. Peer comparison: above median for overall engagement per the external report. |
| Adoption (20%) | 90 | 🟢 Thriving | 9 of 10 available features used above minimum thresholds for the Full bundle. Near-complete feature utilization across iPad, eCat Online, B2B Cart, and Sales Portal. |
| Value Delivery (30%) | 85 | 🟢 Thriving | Full bundle formula: average of order volume, customer activation, eCat Online share, and portal engagement. All four components score well — $9.0M captured through eCat (50.2% capture rate), strong buyer activation, 80% order share through eCat Online, and active Sales Portal usage. |
| Operational Health (15%) | 100 | 🟢 Thriving | Perfect score across import health, catalog completeness, and data freshness. Note: the external report flags 12 stale data entities (options/categories) from 240 days ago, but these don't impact the primary scored metrics enough to lower the score. |
| Trajectory (10%) | 80 | 🟢 Thriving | Strong positive Q/Q momentum. Both the primary value metric (orders) and login activity show healthy growth compared to the prior 90-day period. Recent quarter trending to 58% capture rate, up from 50.2% trailing 12-month average. |

### Flags

- **Churn risk**: None. No risk modifiers fired.
- **Expansion ready**: No (health ≥ 60 but growth below threshold).
- **Risk modifier**: None applied.
- **Warning flags**: All clear — `hs_lifecycle_stale` = false, `hs_join_missing` = false, `arr_data_gap` = false.
- **Scoring status**: Complete. No missing data.

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Wildwood/Chelsea House's bundle (Full), the formula is:
- **Engagement (25%)** — Are users logging in and actively using the platform? Measures login frequency per active user and active user ratio.
- **Adoption (20%)** — How many available features are being used above minimum thresholds? Full bundle has 10 features: Product Search, Customer Selection, Presentations, Email Sharing, PDF Catalogs, Document Viewing, Stacks/Lists, eCat Online, Order Submission, and Sales Portal.
- **Value Delivery (30%)** — Is the platform generating business value? For Full bundles, this is the average of four components: order volume score, customer activation score, eCat Online order share score, and portal engagement score.
- **Operational Health (15%)** — Is client data clean and current? Import success rate, catalog completeness (products with images + pricing), and data freshness.
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares current 90-day order volume and login activity against prior 90 days.

**Classification** maps Health × Growth into an action quadrant:
- Health ≥ 60 + Growth ≥ 60 = **Expand** (upsell/cross-sell)
- Health ≥ 60 + Growth < 60 = **Maintain** (protect with standard cadence)
- Health < 60 + Growth ≥ 60 = **Stabilize First** (fix before selling)
- Health < 60 + Growth < 60 = **Intervene** (immediate save/recovery plan)

</details>

---

## Support & Issue Themes

> 8 conversations in 90 days. Admin-forward, low volume. No active fires.

### Themes

**1. User Management & Account Administration** (4 tickets)
- "Re: Login notification emails", "Re: FW: Brubaker's Design", "Re: New Account Welcome / Lyteworks (30553)", "Re: Fw: Tammy Preusse Chelsea House"
- **Impact**: Routine account setup and access requests. High relative volume (50% of conversations) but all S4/low severity and L1/frontline resolved. Indicates active account management — they're onboarding new dealers and managing access.
- **Root**: Wildwood manages a large dealer network (9,400+ accounts). User provisioning and access questions are an expected operational cadence, not a systemic issue.
- **Action**: No intervention needed. If volume increases, consider a self-service user management guide or expanded Admin Console training for their team.

**2. Data & Integration** (2 tickets)
- "Sales Order Data" (pending — L3/engineering), "Slow loading / eOL" (closed — L3/engineering, S1-critical, first-touch resolved)
- **Impact**: The pending sales data purge request (CSP-36) is blocking Wildwood from cleaning up stale NetSuite order history. The S1-critical eOL performance issue was resolved quickly, showing responsive engineering support.
- **Root**: Stale sales order data from NetSuite integration causing confusion for reps. The performance issue was a one-time platform event.
- **Action**: Prioritize CSP-36 resolution. Needs client confirmation on purge scope before engineering can proceed. Raise in the meeting.

**3. Product & Feature Requests** (2 tickets)
- "Re: FW: Thank you for your order" (training/eOL), "Re: eOL users" (feature request/eOL)
- **Impact**: Minor. Training question about order confirmations and a feature request about eOL user management. Indicates active use of eCat Online.
- **Root**: Normal product feedback from an engaged Full-bundle client.
- **Action**: Log the feature request for product review. No urgency.

### Escalation Profile

6 L1 (frontline resolved), 2 L3 (engineering intervention). No L2 or L4 escalations. Peak severity: S1-critical (eOL slow loading — resolved). The L3 escalations were a performance bug (resolved) and the sales data purge (pending client input). No pattern of recurring engineering-level issues.

### Open Tickets (0 active, 1 pending)

| Subject | Days Open | Severity | Level | State | Action? |
|---|---|---|---|---|---|
| Sales Order Data | 5 | S4 — Low | L3 | PENDING (awaiting client) | Raise in meeting — needs scope confirmation |

*Note: No tickets in "active" (unhandled) status. The "Sales Order Data" conversation is in HelpScout "pending" status, meaning we've responded and are waiting on the client. Connected to Jira CSP-36.*

---

## Active Engineering & Projects

### Recent / Active (2 tickets)

| Key | Summary | Status | Priority | Project | Age | Days Since Update |
|---|---|---|---|---|---|---|
| [CSP-36](https://supercatsolutions.atlassian.net/browse/CSP-36) | Wildwood — Purge and rebuild sales_data (Sales Orders) | To Do | Medium | CSP | 4d | 4d |
| [EBR-728](https://supercatsolutions.atlassian.net/browse/EBR-728) | Sales rep activity logging (mainly 'visits') | Submitted | Unprioritized | EBR | 62d | 62d ⚠️ STALE |

### Backlog (4 tickets — all stale)

<details>
<summary>Older Wildwood-related tickets (backlog)</summary>

| Key | Summary | Status | Priority | Project | Age | Days Since Update |
|---|---|---|---|---|---|---|
| [SERV-1637](https://supercatsolutions.atlassian.net/browse/SERV-1637) | Sales Totals filter | To Do | High | Server | ~800d | ~800d 🔴 |
| [EBR-542](https://supercatsolutions.atlassian.net/browse/EBR-542) | Brandwise integration | Triaging | High | EBR | ~809d | ~233d 🔴 |
| [EBR-450](https://supercatsolutions.atlassian.net/browse/EBR-450) | Capture Credit Card funds during eOL Checkout | Triaging | Medium | EBR | ~1097d | ~233d 🔴 |
| [SERV-278](https://supercatsolutions.atlassian.net/browse/SERV-278) | Customers page: date range filter column behavior | To Do | Unprioritized | Server | ~1851d | ~1643d 🔴 |

</details>

### Flags

- **Stale (no update in 14+ days)**: EBR-728 (62 days), SERV-1637 (~800 days), EBR-542 (~233 days since last update), EBR-450 (~233 days), SERV-278 (~1643 days)
- **High priority**: SERV-1637 (High), EBR-542 (High) — both very old backlog items
- **Blocked**: None explicitly blocked
- **Unassigned**: CSP-36, EBR-728, SERV-1637, EBR-542, EBR-450 — all unassigned except SERV-278 (Jimmy Thrasher)

### Cross-Surface Links

- **CSP-36 ↔ HelpScout "Sales Order Data"**: CSP-36 was created directly from HelpScout conversation #3291979476. Mike Studley (NetSuite Admin at Wildwood) reported stale sales order data confusing their reps. Engineering is ready but awaiting client confirmation on purge scope and time frame.
- **EBR-728 ↔ External Report Rep Activity**: The "Sales rep activity logging (visits)" feature request from Whit (Wildwood) connects to the external report's finding that rep presentation and visit tracking is a gap. This could surface in the meeting as a product request.

---

## Meeting Playbook

### Talking Points

1. **Lapsed account reactivation is the anchor conversation** — The external report will highlight 7,044 lapsed eCat accounts (74.6% of all accounts that ever ordered). Internally, health is strong enough (76, Healthy) that the meeting should focus on offense rather than defense. The Ratchford territory (2,457 dormant accounts) and the overall 25.4% retention rate are the headline numbers.

2. **Sales data purge is an open action item** — CSP-36 is ready for engineering but waiting on Wildwood to confirm the purge scope. This directly impacts their reps' confidence in the data. Raise proactively in the meeting — it shows responsiveness and gets us the confirmation we need to close the ticket.

3. **12 stale data entities are a quick-win config refresh** — The external report flags 12 options/category entities from a 240-day-old import. While Operational Health still scores 100, this is a housekeeping item we can offer to resolve. Proactive move that reinforces data quality partnership.

4. **Engagement score is structurally lower — don't present it as a problem** — At 40, it's the weakest dimension, but 80% of orders come through eCat Online self-service. This is a feature, not a bug. If engagement comes up, frame it as evidence of strong B2B Cart adoption.

### Not in the External Report

- **Health score: 76 (Healthy)** — classified as Maintain. No churn risk, no risk modifiers.
- **Engagement at 40 is the only Watch-band dimension** — all others are Thriving (60+). The internal read: structurally lower due to self-service ordering dominance, not disengagement.
- **Support history is clean** — 8 conversations in 90 days, 6 of 8 resolved at L1. One S1-critical issue (eOL performance) was resolved at first touch. No active fires.
- **Sales data purge (CSP-36) is pending client input** — engineering is ready but blocked on scope confirmation from Mike Studley.
- **5 stale Jira backlog tickets** exist for Wildwood, including 2 High-priority items (SERV-1637 Sales Totals filter, EBR-542 Brandwise integration) that have been dormant for years. These are unlikely to surface but be aware if the client asks about historical requests.
- **Clicky Analytics not enabled** — `has_clicky_portal = false`. No portal traffic visibility currently.

### SuperCat Action Items

- [ ] **Enable Clicky Analytics** — `has_clicky_portal` is false. Enabling would provide portal traffic intelligence for eCat Online, which drives 80% of their order volume. High-value addition for this client.
- [ ] **Close the sales data purge loop** — Use the meeting to get Wildwood's confirmation on CSP-36 scope (time frame, which records, acknowledgment of permanent purge). Engineering is ready.
- [ ] **Offer 12-entity config data refresh** — The external report flags 12 stale option/category entities from 240 days ago. Offer to re-import as a proactive data quality gesture.
- [ ] **Triage stale Jira backlog** — EBR-728 (rep activity logging, 62 days stale) should be updated or closed. The 4 older tickets (800+ days) should be reviewed for relevance and closed if no longer applicable.
