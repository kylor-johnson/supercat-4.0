# Internal Intelligence Brief — Sarreid, Ltd.

*2026-04-17 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Sarreid, Ltd. is the healthiest account in the portfolio — Health 97, all five dimensions scoring 80 or above, zero warning flags, zero open support tickets. The meeting should be entirely offense: highlight the external report's product intelligence (out-of-stock demand opportunity, eCat capture rate growth potential) and use the health data as proof that the platform investment is paying off. The only internal housekeeping items are 13 stale supplemental data files and a backlog of dormant Jira tickets that should be triaged.

**Three Things That Matter:**

1. **Portfolio's top-performing account** — Health 97 with perfect Engagement (100), Adoption (100), and Value Delivery (100). No fires, no risk. This meeting is a celebration and an optimization conversation.
2. **$705K out-of-stock demand is the biggest talking point** — The external report reveals significant proven demand sitting on empty shelves across 5 top-selling products. This is a merchandising conversation, not a platform one — the data pipeline is clean (100% import success rate, zero errors in 877 imports).
3. **5 stale Jira tickets need triage before the meeting** — Three High-priority tickets (Quota, price-level descriptions, portal dashboard) have been dormant 6+ months. Either close them or update status so the team isn't caught off-guard if Sarreid asks about outstanding feature requests.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 97/100 | Maintain |
| **Band** | Thriving | |

> 97 Health → Maintain. Value Delivery (100) leads health; stable with standard cadence.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 100 | 🟢 Thriving | Login intensity and active user ratio both at maximum tier (≥50 logins/active user, ≥30% active ratio). The team is consistently on the platform — engagement is 40 points above the peer median of 60. |
| Adoption (20%) | 100 | 🟢 Thriving | All 9 available features for iPad+Catalog+Portal are used above minimum thresholds: Product Search, Customer Selection, Presentations, Email Sharing, PDF Catalogs, Document Viewing, Stacks/Lists, eCat Online, and Sales Portal. Full feature catalog adoption. |
| Value Delivery (30%) | 100 | 🟢 Thriving | For iPad+Catalog+Portal, VD = (presentation_score + portal_engagement_score) / 2. Both presentation tool usage (email, PDF, catalog sharing) and Sales Portal engagement are at maximum tier, indicating strong business value generation across both channels. |
| Operational Health (15%) | 94 | 🟢 Thriving | Import pipeline at 100% success rate (~130 imports/month, 877 in 6 months, zero errors). Catalog completeness at 90.5%. Minor drag from 13 stale supplemental data entities (options, kit items, categories, collections) last refreshed August 2025 — the only thing keeping this from 100. |
| Trajectory (10%) | 80 | 🟢 Thriving | Q/Q trend is positive. Primary value metrics (presentation actions + portal engagement) trending up vs. prior period, indicating accelerating platform value delivery. Login activity also trending upward. |

### Flags

No risk modifiers fired. No churn risk. All warning flags clear (hs_lifecycle_stale: false, hs_join_missing: false, arr_data_gap: false). No flags.

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Sarreid's bundle (iPad+Catalog+Portal), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measured by login intensity (logins per active user) and active user ratio (active users / total users).
- **Adoption (20%)** — How many available features are being used above minimum thresholds? Sarreid's bundle has 9 applicable features; all 9 are active.
- **Value Delivery (30%)** — Is the platform generating business value? For iPad+Catalog+Portal bundles, this measures a blend of presentation tool usage (email drafts, PDF catalogs, magic button presentations) and Sales Portal engagement. Formula: (presentation_score + portal_engagement_score) / 2.
- **Operational Health (15%)** — Is client data clean and current? Import success rate, catalog completeness (products with images and prices), and data freshness (days since critical updates).
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares primary value metric and login volume between current and prior 90-day periods.

**Classification** determines the recommended action cadence:
- **Expand** — healthy account with strong expansion signals
- **Maintain** — healthy, protect with standard cadence
- **Stabilize First** — needs health improvement before expansion
- **Intervene** — immediate save/recovery plan needed

</details>

---

## Support & Issue Themes

> 5 conversations in 90 days. Admin-focused, low volume. No active fires.

### Themes

**1. Billing & Finance Questions** (2 tickets)
- "Re: General billing question" (Feb 9), "Re: General billing question" (Feb 18)
- **Impact**: Minimal — routine billing inquiries, both resolved at L1/S4. No signal of process breakdown.
- **Root**: Periodic questions about subscription or invoice details — standard for a long-tenured account (since 2014).
- **Action**: Consider adding billing FAQ to knowledge base (one ticket already tagged "add to knowledge base").

**2. Data Import & Sync** (1 ticket)
- "Import error - Sales Data" (Apr 9)
- **Impact**: The only ticket to escalate above L1 (L3 engineering, S3 medium), indicating a non-trivial data pipeline issue that required engineering diagnosis.
- **Root**: Import configuration or data format mismatch in the sales data feed. Resolved within 3 threads.
- **Action**: Confirm root cause is resolved and monitor next import cycle. Connects to the external report's finding of 13 stale supplemental data entities — verify whether the import error was related to the broader data freshness gap.

**3. Training & Feature Requests** (2 tickets)
- "Force sign in timeout" (Jan 30, first-touch resolved), "Question about Admin Reports" (Feb 18)
- **Impact**: Low — isolated questions about platform mechanics from an otherwise self-sufficient team.
- **Root**: Normal usage questions from power users exploring advanced functionality.
- **Action**: The admin reports feature request may connect to Jira ticket EBR-729 (CSV export for usage reports). Check alignment.

### Escalation Profile

4 L1, 1 L3. Peak severity: S3 (Import error — Sales Data). No L2 or L4 escalations. No high-severity (S1/S2) issues.

### Open Tickets (0)

All 5 conversations resolved. No aging tickets. No action needed.

---

## Active Engineering & Projects

5 Jira tickets reference Sarreid. All are stale (no update in 14+ days). Three carry High priority. One recent ticket; four are legacy backlog items.

### Recent / Active

| Key | Summary | Status | Priority | Project | Age | Days Since Update |
|---|---|---|---|---|---|---|
| [EBR-729](https://supercatsolutions.atlassian.net/browse/EBR-729) | Add CSV Export Option to Detailed Usage Report | Approved | Low | EBR | 57d | 15d ⚠️ |

### Older / Backlog

| Key | Summary | Status | Priority | Project | Age | Days Since Update |
|---|---|---|---|---|---|---|
| [SERV-1912](https://supercatsolutions.atlassian.net/browse/SERV-1912) | Quota | In Progress | High 🔴 | Server | 563d | 492d 🔴 |
| [SERV-1673](https://supercatsolutions.atlassian.net/browse/SERV-1673) | Update item descriptions when price level changed | To Do | High 🔴 | Server | 772d | 631d 🔴 |
| [EBR-213](https://supercatsolutions.atlassian.net/browse/EBR-213) | Sales portal dashboard — quota/budget information | In Progress | High 🔴 | EBR | 1682d | 491d 🔴 |
| [EBR-61](https://supercatsolutions.atlassian.net/browse/EBR-61) | Disallow customer viewing for user without sync access | Triaging | Medium | EBR | 1831d | 230d 🔴 |

**Flags:**
- 🔴 **Stale**: All 5 tickets have no update in 14+ days. The 4 backlog items range from 230 to 631 days since last update.
- 🔴 **High priority**: SERV-1912 (Quota), SERV-1673 (price-level descriptions), EBR-213 (portal dashboard quota) — all High priority, all dormant.

**Cross-Surface Links:**
- EBR-213 and SERV-1912 both relate to **Sales Portal quota/budget functionality** — a feature enhancement that could deepen portal value delivery for a team already scoring 100 on that dimension.
- The support ticket "Question about Admin Reports" (feature request) may align with EBR-729 (CSV export for usage reports) — both relate to reporting capabilities.
- No HelpScout tickets tagged `status: logged on jira` — support and engineering backlogs are disconnected.

---

## Meeting Playbook

### Talking Points

1. **$705K out-of-stock demand meets a perfect data pipeline** — The external report highlights $705K in proven demand across 5 top sellers sitting on empty shelves. Internally, Operational Health is 94 with zero import errors — the data is clean and trustworthy. This is a supply/merchandising conversation, not a data quality one. Use the insight as a high-value talking point.
2. **eCat captures 19% of GMV — the path to 30%** — The external report shows eCat captures 19% of $14.5M in total business by value but only 6.4% by order count, meaning reps preferentially use the platform for larger deals. Internally, Engagement (100) and Adoption (100) confirm the tools are fully adopted — the opportunity is migrating more mid-value orders from paper to eCat. Position as optimization, not adoption.
3. **13 stale supplemental data files are the only blemish** — The external report identifies 13 data entities unchanged since August 2025 (options, kit items, categories, collections). Internally, this is the sole drag on Operational Health (94 vs. potential 100). A targeted reimport would clear it. Prepare to explain what a supplemental data refresh involves if Sarreid asks about data currency.

### Not in the External Report

- **Health Score: 97/100 (Thriving)** — highest in the entire portfolio. Classification: Maintain.
- **No churn risk.** No risk modifiers fired, no warning flags, all eligibility signals clean.
- **Support history:** 5 conversations in 90 days, all closed. Only one escalation above L1 (import error, resolved). Volume is among the lowest in the portfolio for an account of this size.
- **Jira backlog:** 5 open tickets, 3 High-priority, all dormant 6+ months. Sarreid may ask about portal quota/budget features (EBR-213, open since 2021).
- **ARR: $27,968** — long-tenured account since 2014, iPad+Catalog+Portal bundle.

### SuperCat Action Items

- [ ] **Triage 5 stale Jira tickets** — Review and close or update SERV-1912 (Quota), SERV-1673 (price-level descriptions), EBR-213 (portal dashboard), EBR-61 (customer viewing permissions), and EBR-729 (CSV export). Three are High priority and have been dormant 6+ months.
- [ ] **Coordinate supplemental data reimport** — 13 data entities (options, kit items, categories, collections) last refreshed August 2025. A reimport would bring Operational Health from 94 to near-100 and resolve the only data freshness gap flagged in the external report.
- [ ] **Prepare for portal quota/budget question** — EBR-213 has been open since 2021. If Sarreid raises this in the meeting, have a clear status update or decision ready (ship it, descope it, or explain timeline).
