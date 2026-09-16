# Internal Intelligence Brief — RENWIL

*April 20, 2026 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

RENWIL is a healthy, deeply adopted account in standard-cadence mode. Health score 84 (Thriving), driven by maximum Trajectory, near-perfect Operational Health, and strong Adoption at 89. No fires — zero open support tickets, no churn risk, no critical issues. The meeting should be offense-oriented: presentation tool coaching for the sales team ($231K opportunity from the external report), dormant account re-engagement ($323K historical value), and a status check on the surcharge calculator enhancement (SERV-2317) that's been in flight since February.

**Three Things That Matter:**

1. **$231K presentation coaching is the headline** — The external report identifies a team-wide presentation gap: 8 of 9 top reps use presentation tools below a 3% ratio vs. the 10% threshold. Suzanne Hogan's 52% ratio correlates with 6× the team-average AOV ($7,117 vs. $1,236). This is the meeting's primary talking point.

2. **Surcharge calculator in flight since February** — SERV-2317 addresses RENWIL's need for freight-on-post-discount and tax-on-subtotal+freight calculations. The HelpScout conversation spans 2+ months, now logged to Jira. Commercially waived per Brent. Confirm timeline with engineering before the meeting.

3. **8 of 9 Jira tickets are stale — housekeeping needed** — The payment integration cluster (SERV-2018, SERV-2022, SERV-2023, SERV-2164) is 460+ days old with Highest priority but no recent movement. Either close as superseded or update status before the meeting. Stale tickets make it hard to credibly discuss what's in progress for RENWIL.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 84/100 | Maintain |
| **Band** | Thriving | Healthy with limited near-term expansion; protect with standard cadence |

> RENWIL (iPad+Catalog+Portal) scores 84 Health → Maintain. Trajectory (100) leads health; stable with standard cadence.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 70 | 🟢 Healthy | Login intensity and active user ratio both in Healthy range. With a 63-rep sales team generating 7,690+ iPad orders in 12 months, platform usage is heavily iPad-driven. Portal visitors average 0.6/day — modest but expected for a Catalog+Portal bundle where the primary workflow is iPad-submitted orders. |
| Adoption (20%) | 89 | 🟢 Thriving | 8 of 9 available features used above minimum thresholds for iPad+Catalog+Portal (search, customer selection, presentations, email sharing, PDF catalogs, documents, stacks, eCat Online). Near-ceiling adoption. The only uncounted feature would be Sales Portal access — but with a score of 89, it's clearly being used. |
| Value Delivery (30%) | 80 | 🟢 Thriving | For iPad+Catalog+Portal, VD = (presentation_score + portal_engagement_score) / 2. Strong presentation tool volume (external report shows 1,600+ presentation actions team-wide) combined with active Sales Portal usage drives this to Thriving. The external report reveals a *depth* gap — most reps use presentation tools below 3% ratio — but the aggregate volume exceeds the scoring threshold. |
| Operational Health (15%) | 100 | 🟢 Thriving | Perfect score — imports running cleanly, catalog complete, data recently updated. Product data was refreshed 3 days before the external report date. However, the external report flags 12 configuration entities stale since August 2025 (options, collections, pricing). These fall outside the health model's `days_since_critical_update` scope (products, customers, inventory). The 100 is accurate to the model but masks a real config staleness issue. |
| Trajectory (10%) | 100 | 🟢 Thriving | Maximum score — strong positive momentum in both primary value metric and login activity vs. prior 90 days. External report confirms: Rob Trottier orders +45%, Cindy Smethurst +75%, Amy Reiman +73%. Team-wide trajectory is accelerating. |

### Flags

- **healthy_complete = true** — Healthy with limited near-term growth opportunity. Standard-cadence protection.
- No risk modifiers fired.
- No churn risk.
- No expansion readiness.
- Warning flags: all clear (hs_lifecycle_stale=false, hs_join_missing=false, arr_data_gap=false).
- Scoring status: complete (no missing data).

<details>
<summary>How Health Scoring Works</summary>

**How Health Scoring Works**: The health score (0–100) combines five dimensions weighted by importance. For RENWIL's bundle (iPad+Catalog+Portal), the formula is:
- **Engagement (25%)** — Are users logging in and actively using the platform? Measured by login intensity (logins per active user) and active user ratio.
- **Adoption (20%)** — How many available features are being used above minimum thresholds? RENWIL's bundle has 9 available features.
- **Value Delivery (30%)** — Is the platform generating business value? For iPad+Catalog+Portal bundles, this measures the average of presentation tool usage and Sales Portal engagement.
- **Operational Health (15%)** — Is client data clean and current? Import success rate, catalog completeness (products with images and prices), and data freshness.
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter? Compares primary value metric and logins current 90d vs. prior 90d.

**Classification** maps Health × Growth into an action quadrant:
- Health ≥ 60 + Growth ≥ 60 = **Expand** (upsell/cross-sell)
- Health ≥ 60 + Growth < 60 = **Maintain** (protect with standard cadence)
- Health < 60 + Growth ≥ 60 = **Stabilize First** (fix before selling)
- Health < 60 + Growth < 60 = **Intervene** (immediate save/recovery plan)

</details>

---

## Support & Issue Themes

> 6 conversations in 90 days. Engineering-heavy, low severity. No active fires.

### Themes

**1. Data Sync & Import Issues** (2 tickets)
- "Backup order PDF coming in blank" (L3, S3-medium) — Mar 10
- "Sync Cancelled Due to Error" (L3, S3-medium) — Jan 28
- **Impact**: Sync failures disrupt field rep workflows. Both required engineering intervention.
- **Root**: Backend data pipeline issues — PDF generation and sync error handling in eCat. Both are infrastructure-level, not client-caused.
- **Action**: Confirm both are fully resolved. These are the only S3 (medium severity) tickets in the window — no recurrence since March suggests root causes addressed.

**2. Surcharge & Pricing Configuration** (2 tickets)
- "Surcharge/Discount Calculations" (L2 → reopened as L3) — Feb 10 → Apr 8
- "Re: [External] Surcharge/Discount Calculations" (L3, tagged `status: logged on jira`) — Apr 8
- **Impact**: Core commercial workflow — pricing accuracy for field reps placing orders with freight, discounts, and Canadian provincial tax. Multi-month conversation now in Jira as SERV-2317.
- **Root**: Platform limitation. Surcharges calculate independently against raw subtotal rather than chaining (freight → tax on subtotal+freight). Existing custom calculator framework handles most requirements; one gap needs development.
- **Action**: Track SERV-2317 progress. This is the most active client-requested enhancement. Commercially waived per Brent (Apr 3, 2026).

**3. Platform Customization Requests** (2 tickets)
- "Information email template customization" (L1, S4-low) — Feb 10
- "Missing order" (L1, S4-low) — Mar 19
- **Impact**: Quality-of-life requests reflecting mature platform usage. The email template request is driven by Quebec bilingual requirements (English+French legally required).
- **Root**: RENWIL operates in Quebec where bilingual communication is mandatory. The Library item email template is hard-coded English-only, which is a product limitation.
- **Action**: EBR-727 addresses the bilingual email template need. Confirm timeline. The "missing order" ticket was an L1 resolved by frontline support.

### Escalation Profile

2 L1, 1 L2, 3 L3. Peak severity: S3 (medium). No S1/S2 critical issues. No L4 executive escalations. The 50% L3 rate is notably high but reflects the technical nature of RENWIL's requests (surcharge calculations, sync infrastructure) rather than service quality failures.

### Open Tickets (0)

No currently active (open) tickets. One ticket ("Surcharge/Discount Calculations") is in **pending** status (HelpScout "pending" = waiting on customer response), created April 8, 2026 (12 days). This ticket is logged on Jira as SERV-2317.

| Subject | Days Open | Severity | Level | State | Action? |
|---|---|---|---|---|---|
| Re: [External] Surcharge/Discount Calculations | 12 | S4 – Low | L3 | PENDING (awaiting customer) | Track via SERV-2317 |

---

## Active Engineering & Projects

> 9 Jira tickets found for RENWIL. 1 recent, 8 stale. Two dominant clusters: surcharge/pricing and payment integration.

### Recent / Active

| Key | Summary | Status | Priority | Project | Age | Days Since Update |
|---|---|---|---|---|---|---|
| [SERV-2317](https://supercatsolutions.atlassian.net/browse/SERV-2317) | Custom surcharge calculator — freight on post-discount subtotal, tax on subtotal+freight | To Do | Unprioritized | Server | 12d | 12d |
| [SERV-2164](https://supercatsolutions.atlassian.net/browse/SERV-2164) | Add capability for multiple Shuttle integrations (CAD/USD) | QA | Unprioritized | Server | 276d | 182d ⚠️ |
| [EBR-662](https://supercatsolutions.atlassian.net/browse/EBR-662) | Line Item Surcharges (Tariff Support) | Triaging | **High** | EBR | 239d | 130d ⚠️ |
| [EBR-727](https://supercatsolutions.atlassian.net/browse/EBR-727) | Make Library item email template configurable (bilingual) | Submitted | Low | EBR | 62d | 62d ⚠️ |

### Backlog (Stale)

| Key | Summary | Status | Priority | Project | Age | Days Since Update |
|---|---|---|---|---|---|---|
| [EBR-684](https://supercatsolutions.atlassian.net/browse/EBR-684) | Improve bespoke surcharges functionality | Submitted | Unprioritized | EBR | 201d | 186d ⚠️ |
| [EBR-683](https://supercatsolutions.atlassian.net/browse/EBR-683) | Retail sales tax support | Submitted | Unprioritized | EBR | 201d | 186d ⚠️ |
| [SERV-2023](https://supercatsolutions.atlassian.net/browse/SERV-2023) | (Maybe) Support multiple payment integrations per org | To Do | Unprioritized | Server | 489d | 470d ⚠️ |
| [SERV-2022](https://supercatsolutions.atlassian.net/browse/SERV-2022) | Configure Renwil payment integration | To Do | Unprioritized | Server | 489d | 470d ⚠️ |
| [SERV-2018](https://supercatsolutions.atlassian.net/browse/SERV-2018) | Renwil credit card integration | To Do | **Highest** | Server | 489d | 463d ⚠️ |

### Flags

- **Stale**: 8 of 9 tickets have no update in 14+ days. Five backlog tickets are 186–470 days stale.
- **High priority**: EBR-662 (High) — Line Item Surcharges, 130d since last update. SERV-2018 (Highest) — Credit card integration, 463d since last update.
- **Blocked**: None explicitly blocked, but SERV-2023 depends on SERV-2021 (which may be done — SERV-2164 is in QA for multi-Shuttle support).

### Cross-Surface Links

- **SERV-2317 ↔ HelpScout**: Directly linked. The "Surcharge/Discount Calculations" conversation (tagged `status: logged on jira`) originated this ticket in April 2026. The HelpScout thread shows a multi-month evolution from initial report (Feb 10) → internal collaboration (L2) → engineering assessment (L3) → Jira ticket creation (Apr 8).
- **Surcharge cluster**: SERV-2317 + EBR-662 + EBR-684 + EBR-683 all address surcharge/pricing logic. SERV-2317 is the newest and most specifically scoped (RENWIL's exact requirements). EBR-662 is the broader tariff support epic. Consider whether EBR-684 and EBR-683 are superseded.
- **Payment cluster**: SERV-2018 + SERV-2022 + SERV-2023 + SERV-2164 all address multi-gateway payment (CAD/USD). SERV-2164 is in QA — if it ships, the other three may be closeable.

---

## Meeting Playbook

### Talking Points

1. **Presentation coaching is pure upside on a healthy foundation** — External report highlights $231K+ coaching opportunity across top reps. Internally, health score is 84 (Thriving) and Adoption is 89 — the platform is deeply embedded. The gap is in presentation *depth* (most reps <3% ratio), not feature adoption. Coaching carries zero platform risk and high revenue leverage.

2. **Stale config data is real but invisible in health score** — External report flags 12 entities stale since August 2025 (options, categories, pricing). Internally, Operational Health scores 100 because `days_since_critical_update` measures products/customers/inventory (all fresh). Prepare to explain what a config refresh involves — this is a SuperCat action item, not a client ask.

3. **Surcharge calculator tracks to a live engineering ticket** — External report doesn't mention surcharges, but internally this is RENWIL's most active request. SERV-2317 was created April 8 and addresses freight+tax calculation accuracy. Be prepared to share timeline and confirm Brent's commercial waiver.

4. **Dormant account re-engagement is better after surcharge fix** — External report identifies $227K dormant opportunity (Ticking Stripe) and $323K across top dormant accounts. If pricing accuracy on orders is improved via SERV-2317, re-engagement outreach will land more credibly with buyers who expect correct surcharge calculations.

### Not in the External Report

- **Health Score: 84/100 (Thriving)** — Classification: Maintain. Healthy Complete flag active.
- **No churn risk.** No risk modifiers, no expansion readiness. All warning flags clear.
- **Support volume is low** (6 conversations / 90 days) with no active fires, but engineering escalation rate is high (50% L3) — reflecting technical request complexity, not service failures.
- **Surcharge enhancement (SERV-2317) is in progress** — commercially waived per Brent (Apr 3, 2026). Multi-month HelpScout thread now in Jira.
- **8 of 9 Jira tickets are stale** (14+ days since update), including 2 high/highest priority tickets (EBR-662, SERV-2018).
- **Payment integration cluster appears superseded** — SERV-2164 (multi-Shuttle) is in QA. If shipped, SERV-2018/2022/2023 may be closeable.

### SuperCat Action Items

- [ ] **Triage stale Jira tickets before the meeting** — 8 of 9 RENWIL tickets have no update in 14+ days. EBR-662 (High, 130d stale) and SERV-2018 (Highest, 463d stale) need status updates or closure. Close superseded tickets in the payment cluster if SERV-2164 (QA) covers the requirement.
- [ ] **Refresh options and category data imports** — External report documents 160+ day staleness for options and 88 days for categories. This is configuration drift that affects rep experience but doesn't block ordering.
- [ ] **Get SERV-2317 timeline from engineering** — Client has been in conversation since February. Confirm estimated delivery and communicate back to Haris Baig at RENWIL.
- [ ] **Confirm EBR-727 timeline** — Bilingual email template for Library items. Quebec compliance request. Low priority in Jira but high importance for a Canadian client with legal bilingual requirements.
