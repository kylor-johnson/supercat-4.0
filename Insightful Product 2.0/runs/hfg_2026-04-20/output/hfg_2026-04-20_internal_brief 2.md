# Internal Intelligence Brief — Hubbardton Forge

*April 20, 2026 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Hubbardton Forge is a healthy, stable account in standard-cadence mode. Health score of 82 (Thriving) with perfect adoption (100) and strong value delivery (90) across both presentation tools and Sales Portal. No fires — zero churn risk, minimal support footprint (3 tickets in 180 days, all low severity), and positive trajectory (90). The meeting should focus on two optimization opportunities from the external report: the $869K dormant account reactivation opportunity and the $543K presentation feature uplift — both are offense plays for an account that needs no defense.

**Three Things That Matter:**

1. **$869K in recoverable dormant account GMV** — The external report identifies 25 dormant eCat accounts totaling $1.6M in trailing-12-month volume, with the top 5 representing $869K. This is the single largest commercial conversation for the meeting — no health risks complicate the pitch.
2. **3 HFG-specific Jira tickets untouched for 3+ years** — ECAT-436 (Smart Strings, High priority), ECAT-475 (Matrix Option Item Codes, Low), and ECAT-259 (Barcode Tags, High) are all in "To Do" with no updates since 2022–2023. The client likely still expects progress on smart strings. Decide before the meeting: close these or commit to a timeline.
3. **Stale config data dragging Operational Health** — 10 data entities haven't been refreshed since August 2025 (242 days). This is the one score weakness (Operational Health = 70) and connects to the external report's medium-priority recommendation to refresh pricing and matrix option data.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 82 / 100 | Maintain |
| **Band** | Thriving | Standard cadence — protect and optimize |

> Hubbardton Forge (iPad+Catalog+Portal) scores 82 Health → Maintain. Adoption (100) leads health; stable with standard cadence.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 60 | 🟢 Healthy | Moderate engagement at the floor of the Healthy band. The team is actively using the platform — external report confirms 13,554 all-time logins (110% above peer median) — but current 90-day login intensity and active user ratio are steady rather than exceptional. Room to convert high historical engagement into more frequent current-period activity. |
| Adoption (20%) | 100 | 🟢 Thriving | Perfect score. All 9 features available for the iPad+Catalog+Portal bundle are used above minimum thresholds: Product Search, Customer Selection, Presentations, Email Sharing, PDF Catalogs, Document Viewing, Stacks/Lists, eCat Online, and Sales Portal. Best-in-class result — no adoption gaps to address. |
| Value Delivery (30%) | 90 | 🟢 Thriving | For iPad+Catalog+Portal bundles, Value Delivery = (presentation_score + portal_engagement_score) / 2. At 90, both presentation tools and Sales Portal show strong usage depth. The team extracts real business value from both sides of the bundle — field-facing presentation workflows and management-facing Sales Portal analytics. |
| Operational Health (15%) | 70 | 🟢 Healthy | Weakest dimension. Catalog completeness is strong (96.7% of 1,099 products have images + pricing), but data freshness drags the score — 10 data entities (matrix options, pricing tiers, reporting data) haven't been refreshed since August 2025 (242 days stale). Import health appears solid where imports occur. A targeted config data refresh would likely push this above 80. |
| Trajectory (10%) | 90 | 🟢 Thriving | Strong positive momentum. Both the primary value metric (presentation actions + portal engagement average) and login trends are accelerating Q/Q, indicating the platform is gaining traction rather than plateauing. |

### Flags

No risk modifiers fired. No churn risk. No expansion-ready flag. All warning flags clear (`hs_lifecycle_stale`: false, `hs_join_missing`: false, `arr_data_gap`: false). Scoring status: complete — no missing data.

<details>
<summary>How Health Scoring Works</summary>

**The health score (0–100) combines five dimensions weighted by importance.** For Hubbardton Forge's bundle (iPad+Catalog+Portal), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measures login intensity (logins per active user) and active user ratio (active users / total users).
- **Adoption (20%)** — How many available features are being used above minimum thresholds? For iPad+Catalog+Portal, 9 features are measured: Product Search, Customer Selection, Presentations, Email Sharing, PDF Catalogs, Document Viewing, Stacks/Lists, eCat Online, and Sales Portal.
- **Value Delivery (30%)** — Is the platform generating business value? For iPad+Catalog+Portal bundles, this measures the average of presentation tool depth (email drafts, PDF catalogs, sharing) and Sales Portal engagement frequency.
- **Operational Health (15%)** — Is client data clean and current? Import success rate, catalog completeness (products with images + pricing), and data freshness (days since last critical update).
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares current 90-day metrics against the prior 90-day period.

**Classification** maps Health into an action mode:
- Health ≥ 60 = **Maintain** or **Expand** (depending on commercial opportunity)
- Health < 60 = **Stabilize First** or **Intervene** (depending on severity)

**Health Bands:** Thriving (80–100), Healthy (60–79), Watch (40–59), At Risk (20–39), Critical (0–19).

</details>

---

## Support & Issue Themes

> 2 conversations in 90 days (extended to 180 days for context: 3 total). Routine admin tasks, all low severity. No active fires.

### Themes

**1. Admin Console Configuration & Account Management** (3 tickets, 180 days)
- "Re: Help with Option $ add-ons" — pricing configuration help for option add-ons
- "URGENT: Need to move dougglassman@mac.com to doug@glassmanbrands.com" — rep email/account migration
- "Re: Upload a File" — data import/file upload issue requiring engineering intervention
- **Impact**: Minimal. Low-volume, routine admin needs. No pattern of platform failure — these are one-off configuration and account maintenance requests.
- **Root**: Small-scale admin changes (option pricing, user email migration, file uploads) that either don't self-serve well in the Admin Console or involve edge-case scenarios.
- **Action**: No systemic action needed. This is healthy low-volume support with quick resolution. The file upload ticket escalated to L3 and was logged on Jira, but has since been resolved.

### Escalation Profile

2 L1, 1 L3 (180 days). Peak severity: S4 (Low) across all conversations. The single L3 engineering escalation was a file upload issue (January 2026), resolved and logged on Jira. No L2 or L4 escalations. No S1/S2 high-severity issues.

### Open Tickets (0)

No currently open tickets. 1 ticket in "pending" status ("Re: Help with Option $ add-ons", created April 15 — 5 days old, customer-response pending). No tickets aging beyond thresholds.

| Subject | Days Open | Severity | Level | State | Action? |
|---|---|---|---|---|---|
| *No open tickets* | — | — | — | — | — |

**Jira Cross-Link**: 1 conversation tagged `status: logged on jira` — "Re: Upload a File" (January 9, 2026, closed). This data import issue may connect to broader data-sync work but does not directly map to the 3 open Jira tickets found in Section 4.

---

## Active Engineering & Projects

3 HFG-specific Jira tickets found. All are in "To Do" status, all unassigned, all massively stale. These are legacy feature requests — not active engineering work.

| Key | Summary | Status | Priority | Project | Age (days) | Days Since Update |
|---|---|---|---|---|---|---|
| [ECAT-436](https://supercatsolutions.atlassian.net/browse/ECAT-436) | Include Smart String in Order | To Do | High | eCat | ~1,525 | ~1,138 |
| [ECAT-259](https://supercatsolutions.atlassian.net/browse/ECAT-259) | Provide an easy way to print barcode tags — iPad | To Do | High | eCat | ~1,730 | ~1,291 |
| [ECAT-475](https://supercatsolutions.atlassian.net/browse/ECAT-475) | Reimplement matrix option item codes in terms of smart strings | To Do | Low | eCat | ~1,510 | ~1,459 |

**Flags:**
- ⚠️ **Stale**: All 3 tickets have had no updates in 1,100–1,459 days (3–4 years)
- ⚠️ **High Priority**: ECAT-436 and ECAT-259 are marked High priority but have never been started
- No tickets are blocked — they simply haven't been picked up

**Cross-Surface Links:**
- ECAT-475 is a child story of ECAT-436 — both relate to HFG's smart string order item numbering system, a custom feature specific to their manufacturing workflow
- ECAT-259 (barcode tags) was built in phases for HFG's showroom workflow — Harvest project links reference HFG-specific billing
- The recent support ticket "Re: Help with Option $ add-ons" (option pricing config) thematically connects to the smart string work (ECAT-436/475), which depends on option codes
- The closed HelpScout ticket "Re: Upload a File" was tagged `status: logged on jira` but does not directly map to these 3 tickets

**Assessment**: These are dormant feature requests, not active projects. The team should decide before the meeting whether to formally close them, move them to a backlog, or commit to delivery timelines — the client may ask about smart strings or barcodes.

---

## Meeting Playbook

### Talking Points

1. **Dormant accounts = largest commercial opportunity** — External report highlights $1.6M in trailing-12-month eCat GMV from 25 dormant accounts, with top 5 representing ~$869K. Internally, Health = 82 (Thriving) with no churn risk, so this is a pure offense conversation. The client is healthy enough to absorb a proactive outreach campaign without diverting from platform stability.
2. **Presentation feature gap is masked in Health but real** — External report flags 17/20 top reps underusing presentation tools (~$543K potential uplift). Internally, Value Delivery still scores 90 because iPad+Catalog+Portal VD averages presentation + portal engagement — strong portal usage compensates. The presentation gap is the external report's highest-impact coaching recommendation and deserves meeting time.
3. **Stale config data is the one internal-external overlap** — External report recommends refreshing 10 stale data entities (242 days). Internally, this is what holds Operational Health to 70 instead of 80+. This is a SuperCat action item — prepare to explain what a config refresh involves and offer to schedule it.

### Not in the External Report

- **Health score: 82/100 (Thriving)** — Classification: Maintain. This is internal-only scoring.
- **No churn risk** — All risk modifiers clear, all flags false. The account is stable.
- **Support history: 3 conversations in 180 days** — All S4 (Low), all Admin Console, all routine. The client is operationally self-sufficient and rarely contacts support.
- **3 dormant Jira tickets (ECAT-436, ECAT-475, ECAT-259)** — All HFG-specific feature requests, all 3+ years old, all unstarted. The client may have expectations around smart strings or barcodes.
- **ARR: $36,300** — Moderate-value account with full utilization of their bundle.

### SuperCat Action Items

- [ ] **Refresh stale configuration data** — 10 entities (matrix options, pricing tiers, reporting data) haven't been updated since August 2025. A targeted re-import would resolve the external report's medium-priority alert and push Operational Health above 80. Schedule this before or immediately after the meeting.
- [ ] **Decide on dormant Jira tickets** — ECAT-436 (Smart Strings, High), ECAT-475 (Matrix Option Items, Low), ECAT-259 (Barcode Tags, High) are all 3+ years stale. Before the meeting: close them formally, move to a low-priority backlog, or commit to a delivery timeline. The client may ask.
- [ ] **Prepare dormant account reactivation talking points** — The top 5 dormant accounts (CED, ILC Studios, IDC, Hotel Design Group, One Source Distributors) represent ~$869K. Have specific outreach plans ready to discuss — the external report frames this as the #1 priority action.
