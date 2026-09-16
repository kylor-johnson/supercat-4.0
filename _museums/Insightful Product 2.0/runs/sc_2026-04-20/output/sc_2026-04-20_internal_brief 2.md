# Internal Intelligence Brief — Gabriella White

*2026-04-20 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Gabriella White is a thriving, deeply-adopted account running on autopilot. Health is 89/100 with perfect Adoption — every available feature in their iPad+Catalog+Portal bundle is actively used above threshold. The support inbox is active but not alarming: 27 conversations in 90 days, dominated by bugs and data-sync issues, with no open fires. Two high-priority Jira bugs (ECAT-1351, SERV-2318) are both near completion. The meeting should be low-key and forward-looking — reinforce the relationship and discuss any product improvements in the pipeline.

**Three Things That Matter:**

1. **Perfect Adoption is rare — protect it** — All 9 bundle features are above minimum thresholds. This is one of the strongest adoption profiles in the portfolio. Worth acknowledging internally as a reference account and ensuring nothing disrupts the current workflow.
2. **Two high-priority bugs are near resolution** — ECAT-1351 (order entry screen refresh) is in Ready to QA; SERV-2318 (admin password reset) is in Ready to Merge. Both are client-reported. Be prepared to give a progress update if asked, but don't overpromise ship dates.
3. **Stale backlog items may surface in conversation** — ECAT-1350 ("You Saved" pricing feature, 32 days stale) and EBR-754 (max order quantity, 18 days stale) are unassigned feature requests from this client. Have a position ready if they ask for status.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 89/100 | Maintain |
| **Band** | Thriving | Protect with standard cadence |

> Gabriella White (iPad+Catalog+Portal) scores 89 Health → Maintain. Adoption (100) leads health; stable with standard cadence.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 90 | 🟢 Thriving | Login frequency and active user ratio are both strong. Users are regularly engaging with the platform with high login intensity — well above the ≥35 logins/user threshold and ≥20% active user ratio needed for this band. |
| Adoption (20%) | 100 | 🟢 Thriving | All 9 features available for iPad+Catalog+Portal (Product Search, Customer Selection, Presentations, Email Sharing, PDF Catalogs, Document Viewing, Stacks/Lists, eCat Online, Sales Portal) are in active use above minimum thresholds. Perfect score. |
| Value Delivery (30%) | 90 | 🟢 Thriving | For iPad+Catalog+Portal bundles, Value Delivery = (presentation_score + portal_engagement_score) / 2. Both presentation tools (email, PDF, sharing) and Sales Portal usage are generating strong business value. |
| Operational Health (15%) | 82 | 🟢 Thriving | Import health, catalog completeness, and data freshness are all in good shape. No significant data quality drag — import success rate and catalog coverage are above the 95% threshold. |
| Trajectory (10%) | 70 | 🟢 Healthy | Quarter-over-quarter trend is positive. Primary value metrics (presentation actions + portal engagement) and login activity are holding steady or growing moderately vs. prior 90 days. |

### Flags

No risk modifiers fired. No churn risk. All warning flags clear (`hs_lifecycle_stale` = false, `hs_join_missing` = false, `arr_data_gap` = false). No flags.

<details>
<summary>How Health Scoring Works</summary>

**How Health Scoring Works**: The health score (0–100) combines five dimensions weighted by importance. For Gabriella White's bundle (iPad+Catalog+Portal), the formula is:
- **Engagement (25%)** — Are users logging in and actively using the platform? Measures login intensity and active user ratio.
- **Adoption (20%)** — How many available features are being used above minimum thresholds? For iPad+Catalog+Portal, 9 features are evaluated: Product Search, Customer Selection, Presentations, Email Sharing, PDF Catalogs, Document Viewing, Stacks/Lists, eCat Online, and Sales Portal.
- **Value Delivery (30%)** — Is the platform generating business value? For iPad+Catalog+Portal bundles, this measures the average of presentation tool usage (email, PDF, sharing actions) and Sales Portal engagement (portal access frequency).
- **Operational Health (15%)** — Is client data clean and current? Import success rate, catalog completeness (products with images and pricing), and data freshness (days since last critical update).
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares current 90-day primary value metrics and login activity against the prior 90-day period.

**Classification** determines the recommended action cadence:
- **Expand** — healthy account with strong expansion signals
- **Maintain** — healthy, protect with standard cadence
- **Stabilize First** — needs health improvement before expansion
- **Intervene** — immediate save/recovery plan needed

</details>

---

## Support & Issue Themes

> 27 conversations in 90 days. Bug-heavy with frequent engineering involvement (41% L3). No active fires — all high-severity incidents resolved.

### Themes

**1. Bugs & Platform Defects** (7 tickets)
- "eCat Down," "Customer Cannot Progress Order," "FW: ECat weirding out," "Services Slow/Unresponsive," "Orders Not Being Exported," "RE: File Import Error"
- **Impact**: A quarter of all interactions involve software defects across iPad app, eCat Online, and Admin Console. Frequent enough to erode trust if not tracked.
- **Root**: A spread of legitimate product bugs — order entry display issues, service slowdowns, and import processing errors — rather than a single systemic failure.
- **Action**: Active Jira tickets (ECAT-1351, SERV-2318) are addressing the most recent reports. Continue prioritizing client-reported bugs to maintain confidence.

**2. Data Sync & Import Issues** (4 tickets)
- "Orders not processing," "Import error (GH)," "eCat Online - Search/Browse Issue," "Submitted Quote Not Showing on iPad"
- **Impact**: Data movement between systems is a recurring friction point affecting order flow, catalog accuracy, and cross-platform sync.
- **Root**: Complex data pipelines with multiple import/export paths; errors arise when import configurations encounter edge cases or when sync timing creates stale data across platforms.
- **Action**: A proactive import configuration audit could reduce these tickets. Consider a health check of their data sync configuration.

**3. User Management & Access** (4 tickets)
- "Account Cleanup," "User Password Reset," "eCAT dev app on the iPad," "Customer Cannot Place Orders in Customer Portal"
- **Impact**: Routine admin tasks consume support bandwidth on mundane operations. Not high-severity but high-frequency.
- **Root**: Limited self-service tooling for common user administration tasks (password resets, account provisioning, access configuration). The admin password reset bug (SERV-2318) exacerbated this.
- **Action**: SERV-2318 (admin reset fix) is Ready to Merge — will directly reduce these tickets once deployed.

### Escalation Profile

11 L1, 2 L2, 11 L3. No L4 executive escalations. Peak severity: S1 (Services Slow/Unresponsive — resolved Feb 2026), S2 (Orders Not Being Exported — resolved). The high L3 rate (46% of tagged conversations) reflects the bug-heavy support profile — engineering involvement was needed, not a sign of dissatisfaction.

### Open Tickets (2)

| Subject | Days Open | Severity | Level | State | Action? |
|---|---|---|---|---|---|
| Updating Options Is Not Reflected on Order Entry Screen | 7 | S3 | L3 | PENDING (logged on Jira → ECAT-1351) | — |
| Re: Smart Search | 42 | S4 | L2 | PENDING (config issue) | 🔴 > 14 days |

**Jira Cross-Link**: 3 conversations tagged `status: logged on jira`:
- "Updating Options Is Not Reflected on Order Entry Screen" → [ECAT-1351](https://supercatsolutions.atlassian.net/browse/ECAT-1351)
- "You Saved Functionality" → [ECAT-1350](https://supercatsolutions.atlassian.net/browse/ECAT-1350)
- "No Warning Message When Dropped Products Are On Order" → [SERV-2279](https://supercatsolutions.atlassian.net/browse/SERV-2279)

---

## Active Engineering & Projects

| Key | Summary | Status | Priority | Project | Age | Days Since Update |
|---|---|---|---|---|---|---|
| [ECAT-1351](https://supercatsolutions.atlassian.net/browse/ECAT-1351) | Order entry screen does not refresh option/finish selections after editing | Ready to QA | High | eCat | 7d | 5d |
| [SERV-2318](https://supercatsolutions.atlassian.net/browse/SERV-2318) | Fix admin Edit User page reset password | Ready to Merge | High | Server | 11d | 0d |
| [EBR-754](https://supercatsolutions.atlassian.net/browse/EBR-754) | FEA: Maximum order quantity per product | Submitted | Unprioritized | EBR | 18d | 18d ⚠️ |
| [ECAT-1350](https://supercatsolutions.atlassian.net/browse/ECAT-1350) | "You Saved" not displayed when order-level price level is changed | To Do | Medium | eCat | 32d | 32d ⚠️ |
| [SERV-2279](https://supercatsolutions.atlassian.net/browse/SERV-2279) | Fea: Warning message when dropped products are on order | To Do | Medium | Server | 77d | 77d ⚠️ |

<details>
<summary>Backlog / Cross-Client (2 tickets)</summary>

| Key | Summary | Status | Priority | Project | Age | Days Since Update |
|---|---|---|---|---|---|---|
| [EBR-656](https://supercatsolutions.atlassian.net/browse/EBR-656) | Configurable search across SuperCat | Ready for Test | High | EBR | 243d | 18d ⚠️ |
| [EBR-654](https://supercatsolutions.atlassian.net/browse/EBR-654) | FEA: Customer-facing quoting with product configuration | Approved | Medium | EBR | 244d | 73d ⚠️ |

These are multi-client feature requests (Gabriella White & Summer Classics) tracked in the EBR backlog.

</details>

**Flags**:
- 🔴 **High priority**: ECAT-1351 (High), SERV-2318 (High), EBR-656 (High)
- ⚠️ **Stale (no update 14+ days)**: EBR-754 (18d), ECAT-1350 (32d), SERV-2279 (77d), EBR-656 (18d), EBR-654 (73d)

**Cross-Surface Links**:
- ECAT-1351 directly addresses HelpScout "Updating Options Is Not Reflected on Order Entry Screen" (L3, S3, pending)
- SERV-2318 addresses HelpScout "User Password Reset" — the admin reset button was silently failing
- ECAT-1350 addresses HelpScout "You Saved Functionality" (L1, S4, logged on Jira)
- SERV-2279 addresses HelpScout "No Warning Message When Dropped Products Are On Order" (L1, S4, logged on Jira)
- EBR-656 (Configurable Search) relates to the pending "Smart Search" HelpScout ticket (42 days, L2, S4)

---

## Meeting Playbook

### Talking Points

1. **Active bugs are progressing, not stalling** — The two most recent client-reported bugs (ECAT-1351 order entry refresh, SERV-2318 password reset) are both in late-stage development (Ready to QA and Ready to Merge). Support-to-Jira pipeline is working as expected. If the client asks about these, confirm they're in QA/merge — don't commit to release dates.
2. **Heavy platform usage drives support volume, not dissatisfaction** — 27 tickets in 90 days sounds active, but with Adoption at 100 and Engagement at 90, this is the support profile of a power user, not an unhappy customer. The L3 rate (46%) reflects the bug mix, not escalation frustration.
3. **Search improvements are coming** — EBR-656 (Configurable Search) is in Ready for Test. This directly addresses the "Smart Search" support thread that's been pending 42 days. When deployed, it will improve the product experience for Gabriella White and other clients.

### Not in the External Report

- **Health score: 89/100 (Thriving)**, Classification: Maintain — internal-only metric, not shared with client
- **No churn risk** — no risk modifiers fired, all warning flags clear
- **Support volume: 27 tickets in 90 days** — 41% required engineering intervention (L3); peak severity S1 was resolved in February
- **Two HelpScout tickets still pending** — "Smart Search" has been open 42 days
- **5 Jira tickets stale** — EBR-754, ECAT-1350, SERV-2279, EBR-656, EBR-654 have had no updates in 14+ days

### SuperCat Action Items

- [ ] **Follow up on Smart Search HelpScout ticket** — 42 days pending is too long. Either close with a link to EBR-656 or provide a status update to the client.
- [ ] **Triage stale Jira backlog** — ECAT-1350 (32d), SERV-2279 (77d), EBR-754 (18d) need status updates or closure. Be ready with answers if the client asks.
- [ ] **Verify SERV-2318 deployment plan** — Password reset fix is Ready to Merge. Confirm merge and release timing so support can stop working around the bug.
