# Internal Intelligence Brief — Currey & Company

*April 17, 2026 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Currey & Company is a healthy, stable account in standard-cadence mode. Platform is deeply adopted (89/100), engagement is 2× the peer median, and all five health dimensions are green. No fires — no churn risk, no risk modifiers, no high-severity open issues. The meeting should be offense, not defense: push on the rep presentation gap ($230K potential uplift) and address the 240-day stale configuration data, which is a SuperCat action item.

**Three Things That Matter:**

1. **Presentation gap is the money on the table** — 8 of CCI's top 20 reps have near-zero presentation activity despite thousands of product discovery events. The external report quantifies ~$230K in potential GMV uplift if presenting reps' AOV patterns replicate. This is the #1 talking point.

2. **Support is healthy — training-forward, no fires** — 5 tickets in 90 days, all L1/S4 except one resolved L3 engineering escalation (Amex payment gateway, now closed and Jira-tracked). Dominant theme is training and admin questions — a sign they're actively exploring the platform. Two open tickets are aging (12 and 21 days) — close before the meeting.

3. **Config refresh is on us, not them** — 11 configuration entities (pricing, options, collections) have been stale since August 2025 (240 days). This drags Operational Health to 64 — the weakest dimension and the only one below 70. The external report flags it; the client may not understand what these entities are. Prepare to explain what a config refresh involves and own it as a SuperCat action.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | **77** / 100 | **Maintain** |
| **Band** | Healthy | Standard cadence |

> Currey & Company (iPad+Catalog+Portal) scores 77 Health → Maintain. Adoption (89) leads health; stable with standard cadence.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| **Engagement** (25%) | 80 | 🟢 Thriving | High login frequency and strong active user ratio. The external report confirms CCI's engagement is 2× the peer median among comparable lighting manufacturers on the same bundle. No concern here. |
| **Adoption** (20%) | 89 | 🟢 Thriving | Using 8 of 9 available features above minimum thresholds (iPad+Catalog+Portal bundle). Near-complete platform adoption — product search, customer selection, presentations, email sharing, PDF catalogs, document viewing, stacks, and Sales Portal all active. |
| **Value Delivery** (30%) | 80 | 🟢 Thriving | For iPad+Catalog+Portal bundles, Value Delivery = average of Presentation Score + Portal Engagement Score. CCI's team actively uses presentation tools (email, PDF, sharing) AND the Sales Portal. The platform is integrated into their selling workflow, not just installed. |
| **Operational Health** (15%) | 64 | 🟢 Healthy | **Weakest dimension.** Import health and catalog completeness are solid, but Data Freshness is dragging the score down — 11 configuration entities (pricing, options, collections) haven't been refreshed since August 2025 (240 days). This is a SuperCat-side data maintenance issue. |
| **Trajectory** (10%) | 60 | 🟢 Healthy | Q1 2026 activity was roughly flat vs. Q4 2025. Login and value metric changes both in the neutral range (-5% to +10%). Not declining (stable), but not accelerating either. |

### Flags

- No risk modifier fired
- No churn risk
- Warning flags: all clear (`hs_lifecycle_stale = false`, `hs_join_missing = false`, `arr_data_gap = false`)
- Scoring status: complete (no missing data)

<details>
<summary><strong>How Health Scoring Works</strong></summary>

The health score (0-100) combines five dimensions weighted by importance. For CCI's bundle (iPad+Catalog+Portal), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measured by login frequency and the ratio of active to provisioned users.
- **Adoption (20%)** — How many of the 9 available features are being used above minimum thresholds? Features include product search, customer selection, presentations, email sharing, PDF catalogs, document viewing, stacks, eCat Online, and Sales Portal.
- **Value Delivery (30%)** — Is the platform generating business value? For iPad+Catalog+Portal bundles, this is the average of Presentation Score (how much reps use email, PDF, and sharing tools) and Portal Engagement Score (Sales Portal usage depth).
- **Operational Health (15%)** — Is client data clean and current? Three sub-scores: Import Health (50%), Catalog Completeness (30%), and Data Freshness (20%).
- **Trajectory (10%)** — Is activity trending up, flat, or down? Compares the most recent 90 days to the prior 90 days on login activity and the primary value metric.

**Health Bands**: Thriving (80-100), Healthy (60-79), Watch (40-59), At Risk (20-39), Critical (0-19).

**Classification** determines the recommended action cadence:
- **Expand** — healthy account with strong expansion signals
- **Maintain** — healthy, protect with standard cadence ← CCI is here
- **Stabilize First** — needs health improvement before any expansion
- **Intervene** — immediate save/recovery plan needed

</details>

---

## Support & Issue Themes

> 5 conversations in 90 days. Training-forward, low volume. No active fires.

### Themes

**1. Training & admin workflows** (3 of 5 tickets)
- Inactive account management in eCat, placement vs. display data discrepancy, old quotes being submitted
- **Impact**: CCI is actively exploring platform capabilities beyond basic ordering — this is a maturity signal, not a problem signal
- **Root**: Growing admin-level sophistication; they're outgrowing standard L1 support for admin console questions
- **Action**: Consider offering a targeted admin training session during or after the meeting. Proactive offer demonstrates partnership and reduces future support volume.

**2. Orders & payment integration** (2 of 5 tickets)
- Amex credit card payment gateway error (L3/S3, resolved), old quotes submission workflow
- **Impact**: The Amex issue was the only escalation — an engineering-level product bug, not a user error. It was resolved and logged on Jira. The quotes issue was a feature request.
- **Root**: Payment gateway edge case (Amex-specific). One-time, not systemic.
- **Action**: Confirm the Jira-tracked Amex fix is fully deployed. Mention proactively if the client raises payment topics.

### Escalation Profile

6 of 8 tagged conversations at L1 (frontline). 1 at L3 (engineering — Amex gateway, closed). No L2, L4, or executive escalations. Peak severity: S3/Medium on the Amex issue; all others S4/Low.

### Open Tickets (2)

| Subject | Days Open | Severity | Level | State | Action? |
|---|---|---|---|---|---|
| Placements entered & On Display showing Different? | 21 | S4 - Low | L1 | UNKNOWN | 🔴 > 14 days — resolve before meeting |
| Inactive Accounts & Prevent creating new accounts in eCat | 12 | S4 - Low | L1 | UNKNOWN | 🟡 > 7 days — respond or close |

*Conversation state is UNKNOWN — BigQuery `helpscout.conversations` does not include thread-level data. Both tickets are low severity/L1 training questions. Recommend resolving both before the client meeting regardless of whose court the ball is in.*

**Jira cross-link**: 1 conversation tagged `status: logged on jira` — the Amex payment gateway error (closed in HelpScout). Confirm Jira ticket status.

---

## Active Engineering & Projects

7 open Jira tickets reference Currey & Company. The two most recent are directly linked to the "old quotes" HelpScout support ticket and were filed with CCI leadership confirmation.

### Recent / Active (last 6 months)

| Key | Summary | Status | Priority | Project | Age | Last Update |
|---|---|---|---|---|---|---|
| [EBR-735](https://supercatsolutions.atlassian.net/browse/EBR-735) | Show Creation Date on Quote Documents | Approved | 🔴 High | EBR | 46d | Apr 2 |
| [EBR-734](https://supercatsolutions.atlassian.net/browse/EBR-734) | Quote Expiration / Configurable Validity Period | Approved | 🔴 High | EBR | 46d | Apr 2 |
| [EBR-616](https://supercatsolutions.atlassian.net/browse/EBR-616) | Block order edit if resubmissions disallowed | Triaging | Unprioritized | EBR | 341d | Apr 2 |

### Older / Backlog

| Key | Summary | Status | Priority | Project | Age |
|---|---|---|---|---|---|
| [ECAT-639](https://supercatsolutions.atlassian.net/browse/ECAT-639) | Plumb ShipTo Email/Phone fields through eCat and eOL | To Do | High | ECAT | 3+ yrs |
| [ECAT-355](https://supercatsolutions.atlassian.net/browse/ECAT-355) | Capture credit card info by camera | To Do | Lowest | ECAT | 4+ yrs |
| [ECAT-251](https://supercatsolutions.atlassian.net/browse/ECAT-251) | Support credit cards — eCat (epic) | In Progress | Highest | ECAT | 4+ yrs |
| [EBR-199](https://supercatsolutions.atlassian.net/browse/EBR-199) | Show configurable banners on product photos | Triaging | Lowest | EBR | 4+ yrs |

### Cross-Surface Links

- **HelpScout → Jira connection confirmed**: The "Old Quotes being submitted" support ticket (HelpScout #14082, closed) directly sourced EBR-734 and EBR-735. Both are now Approved/High priority. CCI leadership confirmed interest in a 30-day quote expiration. These are the most relevant tickets to mention if the client asks about feature progress.
- **Credit card theme**: ECAT-251 (credit card epic, Highest priority) and ECAT-355 connect to the resolved Amex payment gateway support escalation. The credit card infrastructure is in progress but the epic is 4+ years old with no recent update — worth checking actual status.
- **Stale backlog items**: EBR-199, EBR-150, EBR-207 are 4+ years old and in Triaging. These are feature requests, not active work. Do not mention to the client unless they raise the topic.

---

## Meeting Playbook

### Talking Points

1. **Presentation gap → AOV uplift opportunity**: The external report headlines that 8 of CCI's top 20 reps have near-zero presentation activity, with presenters achieving $2,044-$2,745 AOV vs. $1,314-$1,866 for non-presenters. Internally, Adoption is 89 (Thriving) because adoption measures feature breadth, not depth — the gap is within Value Delivery. Frame as "you're already healthy, here's the next level" not "you have a problem."

2. **eCat captures 9.9% of $83.8M total business**: External report highlights significant headroom. There's behavioral evidence CCI could benefit from B2B Cart (upgrade from iPad+Catalog+Portal → Full). If CCI expresses interest in expanding digital ordering to their buyer base, that's the natural expansion path.

3. **Config data staleness — own it**: The external report flags 11 stale configuration entities since August 2025. Internally, Operational Health at 64 is the weakest green dimension because of this. The client may not understand what "pricing, options, and collections data" means operationally. Prepare to explain and present a timeline for refreshing these entities. This is a SuperCat deliverable, not a client ask.

### Not in the External Report

These facts are internal-only — the client will never see them:
- **Health score: 77 (Healthy)** — scores, bands, and classifications are never shown externally
- **Classification: Maintain** — CCI is in standard-cadence mode; no urgent health action needed
- **No churn risk** — no risk modifiers fired, all warning flags clear
- **Support pattern**: Training-forward, low volume, one resolved L3 engineering escalation. Two open tickets aging.
- **Jira backlog**: 7 open tickets, 2 recent high-priority feature requests (quote expiration, quote date display) both Approved

### SuperCat Action Items

- [ ] **Resolve 2 open support tickets** — both are aging (12 and 21 days). Low severity, but closing them before the meeting demonstrates responsiveness.
- [ ] **Enable Clicky Analytics** — CCI has iPad+Catalog+Portal but `has_clicky_portal = false`. Enabling Clicky would unlock portal traffic intelligence for future external reports and improve data visibility.
- [ ] **Refresh configuration data** — 11 entities stale since August 2025 (240 days). Schedule a config refresh cycle covering pricing, options, and collections. This will improve the Operational Health score.
- [ ] **Prepare update on EBR-734 & EBR-735** — Both are Approved/High: quote expiration (30-day validity period) and showing creation date on quotes. CCI leadership asked for these. Be ready to share timeline if the client asks.
- [ ] **Check ECAT-251 credit card epic status** — Marked "In Progress" but 4+ years old with Highest priority. Verify actual state — the Amex payment gateway HelpScout escalation ties to this.

---

*Brief generated from: Health V2 v2.5.1 (2026-04-14), HelpScout via BigQuery (2026-04-20), Jira via Atlassian MCP (2026-04-20), org_summary. External report: cci_2026-04-17.*
