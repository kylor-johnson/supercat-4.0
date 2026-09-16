# Internal Intelligence Brief — Crystorama

*2026-04-20 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Crystorama is a healthy, high-performing account in expansion territory. Health scores 82 (Thriving) with perfect Adoption, Value Delivery, and Trajectory — the only soft spot is Engagement at 40, driven by a small but active user base where several top reps went silent this quarter. No fires, no churn risk, zero open support tickets. The meeting should play offense: highlight the platform value story, discuss the $135K silent-rep re-engagement opportunity, and explore bundle expansion signals.

**Three Things That Matter:**

1. **Engagement is the one weak link at 40** — Three high-GMV reps ($135K combined trailing-12-month iPad GMV) went silent this quarter. If they re-activate, Engagement improves and quarterly order volume recovers an estimated $30K–$50K. This is the biggest near-term action item for both the client and us.
2. **Platform value story is rock-solid** — 100/100 on both Adoption and Value Delivery, top-quartile peer performance, 100% catalog completeness across 2,077 products. Lead the meeting with this credibility before pivoting to opportunities.
3. **Three stale Jira tickets need housekeeping** — SERV-2297 (import BOM fix, High priority) has sat in To Do for 50 days. EBR-660 and SERV-1661 have been open 234+ and 657+ days respectively. Clean these up before the meeting to demonstrate responsiveness.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 82/100 | Expand |
| **Band** | Thriving | Action mode |

> Crystorama (iPad+Catalog+Portal) scores 82 Health → Expand. Full-score Adoption, Value Delivery, and Trajectory drive health; Engagement at 40 is the sole dimension in Watch territory.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 40 | 🟡 Watch | Login frequency and active user ratio are moderate. At 40, the active user ratio likely falls in the 5–10% range of total provisioned users. Consistent with the external report finding that 3 of 5 top reps went silent this quarter while overall login counts remain positive. |
| Adoption (20%) | 100 | 🟢 Thriving | All 9 features available for iPad+Catalog+Portal are used above minimum thresholds: Product Search, Customer Selection, Presentations, Email Sharing, PDF Catalogs, Document Viewing, Stacks/Lists, eCat Online, and Sales Portal. Perfect breadth. |
| Value Delivery (30%) | 100 | 🟢 Thriving | For iPad+Catalog+Portal bundles, Value Delivery averages presentation_score and portal_engagement_score. Both are at maximum — Crystorama exceeds 1,000 presentation actions and 300+ Sales Portal accesses per 90 days. External report confirms top-quartile vs. peers. |
| Operational Health (15%) | 80 | 🟢 Thriving | 100% catalog completeness (2,077 products with imagery and pricing). The 20-point gap from perfect is driven by data freshness — the external report identified 9 configuration entities (options, pricing, kits) stale since August 2025 while product data refreshes daily. |
| Trajectory (10%) | 100 | 🟢 Thriving | Strong Q/Q acceleration. Both the primary value metric (presentation + portal engagement average) and login activity grew well above +20% and +15% thresholds respectively vs. prior quarter. |

### Flags

- **hs_lifecycle_stale**: True — HubSpot lifecycle status for Crystorama may be stale (shows "Lost"/"Churn" or no record), but the org has an active subscription and is fully scored. This is a data hygiene flag, not a risk indicator. Recommend updating HubSpot to reflect active status.
- No risk modifiers fired. No churn risk.

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Crystorama's bundle (iPad+Catalog+Portal), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measured by login frequency per active user and the ratio of active users to total provisioned users.
- **Adoption (20%)** — How many available features are being used above minimum thresholds? For iPad+Catalog+Portal, there are 9 eligible features spanning iPad workflows, eCat Online, and Sales Portal.
- **Value Delivery (30%)** — Is the platform generating business value? For iPad+Catalog+Portal bundles, this averages presentation tool usage (emails, PDFs, catalog sharing) and Sales Portal engagement. This is the highest-weighted dimension.
- **Operational Health (15%)** — Is client data clean and current? Measures import success rate, catalog completeness (products with imagery and pricing), and data freshness (days since last critical update).
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares the primary value metric and login volume between the current and prior 90-day periods.

**Classification** determines the recommended action cadence:
- **Expand** — healthy account with strong expansion signals
- **Maintain** — healthy, protect with standard cadence
- **Stabilize First** — needs health improvement before expansion
- **Intervene** — immediate save/recovery plan needed

</details>

---

## Support & Issue Themes

> 3 conversations in 90 days. Engineering-heavy, import-focused. No active fires.

### Themes

**1. Data Sync & Import Failures** (2 tickets)
- "Re: URGENT – eCat Sales Data Export Failing (PG Connection Error)"
- "Re: HIGH PRIORITY: NetSuite Scheduled CSV Imports Failing Since Feb 27 – Previously Stable Process"
- **Impact**: Import pipeline reliability is critical for Crystorama's data freshness. Repeated failures create gaps in product/customer/inventory data and erode rep confidence in the catalog.
- **Root**: UTF-8 BOM characters introduced in NetSuite CSV exports break the import pipeline's header validation. This is a platform-level deficiency — the importer doesn't strip BOM before parsing.
- **Action**: Confirm SERV-2297 (BOM stripping fix) is prioritized for development. Validate whether current imports are running successfully since the initial workaround.

**2. Platform Performance** (1 ticket)
- "Performance Issues – eCat / MyCrystorama & iPad App"
- **Impact**: Performance issues in the iPad app and eCat Online directly affect the selling workflow for reps in the field.
- **Root**: Infrastructure or caching issue flagged as S1 critical. Was resolved quickly (tagged first-touch resolved).
- **Action**: No action needed — resolved. Monitor for recurrence.

### Escalation Profile

0 L1, 0 L2, 3 L3, 0 L4. Peak severity: S1 (critical — performance issue). All three conversations required engineering intervention. No executive escalations.

### Open Tickets (0)

No open support tickets. All conversations are closed and resolved.

---

## Active Engineering & Projects

| Key | Summary | Status | Priority | Project | Age (days) | Days Since Update |
|---|---|---|---|---|---|---|
| [SERV-2297](https://supercatsolutions.atlassian.net/browse/SERV-2297) | CSV imports failing due to UTF-8 BOM in export files | To Do | High | Server | 50 | 50 |
| [EBR-660](https://supercatsolutions.atlassian.net/browse/EBR-660) | Dates from inventory displaying without desired locale format | Triaging | Unprioritized | EBR | 242 | 234 |
| [SERV-1661](https://supercatsolutions.atlassian.net/browse/SERV-1661) | eOL Look & Feel overhaul (references CLM feedback) | To Do | High | Server | 789 | 657 |

**Flags:**
- 🔴 **Stale**: All three tickets have had no update in 14+ days. SERV-2297 is 50 days stale despite High priority. EBR-660 is 234 days stale. SERV-1661 is 657 days stale.
- 🔴 **High priority**: SERV-2297 (High) and SERV-1661 (High) are both in To Do status without assignees.
- No blocked tickets.

**Cross-Surface Links:**
- SERV-2297 (BOM fix) directly addresses the import failure support theme from Section 3 — the two "data-sync imports and exports" HelpScout conversations are about the underlying BOM issue that this Jira ticket was filed to fix.
- SERV-1661 (eOL L&F overhaul) connects to external report findings about eCat Online engagement and Crystorama's use of MyCrystorama as a dealer-facing portal. This ticket collected CLM feedback alongside CFG and others.
- EBR-660 (date locale formatting) is a display issue affecting inventory date fields in the Admin Console and eCat Online — low severity but lingering since August 2025.

---

## Meeting Playbook

### Talking Points

1. **Silent reps = biggest commercial lever and health gap** — The external report identifies $135K in trailing-12-month iPad GMV from 3 silent reps (Linder, Dobson, Trosclair). Internally, Engagement is 40 (Watch) — the only dimension below Thriving. Re-engaging these reps improves both the client's revenue and our health score. Make this the meeting's primary call to action.
2. **Import pipeline needs a permanent fix** — The external report flags 9 stale configuration entities since August 2025. Internally, two of three support tickets this quarter were about import failures (BOM issue), and SERV-2297 has sat in To Do for 50 days. This drags Operational Health from ~100 to 80. Prepare to explain that a platform-level fix is in the queue.
3. **Lead with the value story, then pivot to expansion** — The external report shows 100% catalog completeness and top-quartile Value Delivery vs. peers. Internally, Adoption is 100/100 and classification is Expand with strong bundle upgrade signals. Use the credibility of perfect scores to open the expansion conversation.

### Not in the External Report

- **Health score: 82 (Thriving)** — classification is Expand. The account is healthy with strong expansion signals.
- **No churn risk** — no risk modifiers fired, no churn risk severity assigned.
- **Expansion readiness** — strong bundle upgrade behavioral signals detected. Crystorama shows usage patterns consistent with outgrowing iPad+Catalog+Portal.
- **Support history**: 3 conversations in 90 days, all L3 engineering, all resolved. Zero open tickets. Peak severity was S1 (critical) for a performance issue that was resolved first-touch.
- **hs_lifecycle_stale flag**: HubSpot lifecycle data for Crystorama may be stale — does not reflect their active subscription status. Data hygiene follow-up needed.

### SuperCat Action Items

- [ ] **Update or close stale Jira tickets** — SERV-2297 (50 days, High), EBR-660 (234 days), and SERV-1661 (657 days) all need triage. At minimum, update status and assign SERV-2297 before the meeting.
- [ ] **Investigate hs_lifecycle_stale flag** — HubSpot status for Crystorama may not reflect their active subscription. Update HubSpot to match operational reality.
- [ ] **Confirm current import pipeline status** — After the BOM issue was filed as SERV-2297, verify whether Crystorama's automated NetSuite imports are running successfully or if a workaround is in place.
- [ ] **Prepare expansion conversation** — Bundle upgrade signals are strong. Have pricing and capability comparison ready for iPad+Catalog+Portal → Full bundle (adds B2B Cart).
