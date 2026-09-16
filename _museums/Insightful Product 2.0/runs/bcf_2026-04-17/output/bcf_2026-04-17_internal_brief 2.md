# Internal Intelligence Brief — Braxton Culler

*2026-04-17 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Braxton Culler is a healthy Full-bundle account in standard-cadence mode. Platform deeply adopted (9 of 10 features active), value delivery is top-quartile among peers, and $6.6M in eCat GMV flows through a clean 98.9% confirmed-order pipeline. No fires, no churn risk. The sole internal concern is Engagement at 40 (Watch) — the team is using the platform broadly but not deeply enough per user, with per-rep order frequency trailing peers by nearly 50%. The meeting should be about offense: reactivating $185K in dormant accounts and lifting per-rep activity to close the gap to peer median.

**Three Things That Matter:**

1. **Engagement is the lone yellow dimension at 40** — Per-rep order frequency (0.55 orders/user/90d) trails the peer median of 1.12 by 51%. Closing this gap is the highest-leverage improvement for both the health score and real business outcomes. The external report's sales team data gives specific coaching targets.
2. **$185K in dormant account value is ready to recover** — 203 previously active accounts have gone quiet. Value Delivery is 90 (Thriving) and the ordering pipeline works, so any reactivation effort rides on a functioning system. The top 5 dormant accounts alone represent $185K in historical ordering.
3. **Active options config project signals deepening investment** — CSP-37 (new Epic, High priority) plus 4 new feature requests (EBR-755 through EBR-758) landed in April. Braxton Culler is investing in the platform — this is a relationship opportunity, not a maintenance conversation.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | 74/100 | Maintain |
| **Band** | Healthy | Standard cadence |

> Braxton Culler (Full) scores 74 Health → Maintain. Value Delivery (90) leads health; stable with standard cadence.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | 40 | 🟡 Watch | Login frequency and active user ratio are below thresholds for a 71-user team. Per-rep order frequency (0.55/90d) trails the peer median of 1.12 — the largest gap to close. Some reps (e.g., Andrea Teague) have fully disengaged. |
| Adoption (20%) | 90 | 🟢 Thriving | 9 of 10 available features active for the Full bundle. Configured item ordering (40% peer adoption) and kit configuration (28% peer adoption) are both in use — aligning with top-performer patterns. |
| Value Delivery (30%) | 90 | 🟢 Thriving | Full bundle formula: (order_volume + customer_activation + eol_share + portal_engagement) / 4. All four components score well — $6.6M eCat GMV across 2,608 orders, near 50/50 iPad–eCat Online split, strong customer activation. Top quartile vs. peers (90 vs. peer median 70). |
| Operational Health (15%) | 88 | 🟢 Thriving | Import health and core catalog data are current (product catalog refreshed 3 days ago). Catalog completeness at 82.4% trails the peer median of 95% — 394 products missing pricing, 207 missing images. Kit items (58 days stale) and price levels (44 days stale) are drifting from the catalog. |
| Trajectory (10%) | 60 | 🟢 Healthy | Stable Q/Q — maintaining pace rather than accelerating or declining. No dramatic swings in either value metric or login activity. |

### Flags

No flags. No risk modifier fired. No churn risk. Warning flags all clear (`hs_lifecycle_stale` = false, `hs_join_missing` = false, `arr_data_gap` = false).

<details>
<summary>How Health Scoring Works</summary>

The health score (0–100) combines five dimensions weighted by importance. For Braxton Culler's bundle (Full), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measures login frequency and active user ratio.
- **Adoption (20%)** — How many available features are being used above minimum thresholds? Full bundle has 10 trackable features.
- **Value Delivery (30%)** — Is the platform generating business value? For Full bundles, this measures the average of four components: order volume, customer activation rate, eCat Online share of orders, and Sales Portal engagement.
- **Operational Health (15%)** — Is client data clean and current? Import success rate, catalog completeness (images + pricing), and data freshness.
- **Trajectory (10%)** — Is activity trending up, flat, or down vs. last quarter?

**Classification** determines the recommended action cadence:
- **Expand** — healthy account with strong expansion signals
- **Maintain** — healthy, protect with standard cadence
- **Stabilize First** — needs health improvement before expansion
- **Intervene** — immediate save/recovery plan needed

</details>

---

## Support & Issue Themes

> 18 conversations in 90 days. Operationally active with recurring bug escalations resolved. No active fires.

### Themes

**1. Software Defects** (4 tickets)
- "eCat issues - URGEN" (L3, S3) · "eCat app issue - URGENT" (L3, S1) · "FW: eCat Order #: 117159" (L3, S3)
- **Impact**: Three of four required engineering intervention (L3). One was S1 critical — the most severe issue in the 90-day window. Platform bugs in ordering and configuration erode rep trust.
- **Root**: CPQ configurator complexity and order processing edge cases in the Full bundle.
- **Action**: Track CSP-37 (Options Config Epic) to resolution. Confirm EBR-758 addresses the image rendering issue connected to order emails.

**2. Image & Asset Display** (3 tickets)
- "Log in screen" (×2) · "How we make progress toward GOTO Vendor status"
- **Impact**: Recurring image display problems across login screens, order emails, and product views. Logged on Jira.
- **Root**: Image rendering pipeline not consistently serving assets across iPad, email, and portal channels.
- **Action**: Confirm EBR-758 (product images not rendering on order copy emails/PDFs) is the engineering fix for this pattern.

**3. Orders, Invoices & Payment Integration** (3 tickets)
- "FW: eCat Question on Carrier Info" · "FW: eCat Order #: 117159" · "Todd Teague - Screenshot"
- **Impact**: Order workflow gaps (missing carrier info, order errors) create friction for the sales team.
- **Root**: Custom ERP integration fields (preferred carrier) not yet in the platform; order processing edge cases.
- **Action**: Track EBR-726 (carrier field feature request, logged on Jira from HelpScout). Monitor CSP-37 for related options work.

### Escalation Profile

11 L1, 1 L2, 3 L3. Peak severity: S1 critical (eCat app issue, resolved). No L4 executive escalations. The three L3 engineering interventions all involved ordering or configuration bugs — now tracked in Jira.

### Open Tickets (0)

No currently open (active) HelpScout tickets. 5 conversations are in "pending" status (waiting on customer) — not actionable on our side.

**Jira Cross-Link**: 2 conversations tagged `status: logged on jira`:
1. "FW: How we make progress toward GOTO Vendor status" → connects to EBR-758 (image rendering) and the broader GOTO Vendor initiative
2. "FW: eCat Question on Carrier Info" → connects to EBR-726 (preferred carrier field feature request)

---

## Active Engineering & Projects

6 recent tickets (created in last 90 days) plus 10 backlog items across EBR, ECAT, SERV, and CSP projects.

### Recent / Active

| Key | Summary | Project | Status | Priority | Assignee | Age | Days Since Update |
|---|---|---|---|---|---|---|---|
| [CSP-37](https://supercatsolutions.atlassian.net/browse/CSP-37) | Options Config & Support Requests (April 2026) | CSP | Pending Client | High | Kyla Bosch | 0d | 0d |
| [EBR-758](https://supercatsolutions.atlassian.net/browse/EBR-758) | Product images not rendering on order copy emails/PDFs | EBR | Submitted | Medium | Unassigned | 18d | 0d |
| [EBR-757](https://supercatsolutions.atlassian.net/browse/EBR-757) | Search bar for finish selection in CPQ configurator | EBR | Submitted | Medium | Unassigned | 19d | 0d |
| [EBR-756](https://supercatsolutions.atlassian.net/browse/EBR-756) | Display replacement parts/credit memos on portal | EBR | Submitted | Medium | Unassigned | 19d | 0d |
| [EBR-755](https://supercatsolutions.atlassian.net/browse/EBR-755) | Customizable eCat landing page with category thumbnails | EBR | Submitted | Low | Unassigned | 19d | 0d |
| [EBR-726](https://supercatsolutions.atlassian.net/browse/EBR-726) | Preferred carrier field in customer info | EBR | Submitted | Low | Unassigned | 64d | ⚠️ 60d |

### Backlog (10 tickets — mostly stale)

| Key | Summary | Status | Priority | Age | Days Since Update |
|---|---|---|---|---|---|
| [ECAT-1336](https://supercatsolutions.atlassian.net/browse/ECAT-1336) | Riser pricing not working for second option set | QA | Unprioritized | 222d | 🔴 96d |
| [SERV-2172](https://supercatsolutions.atlassian.net/browse/SERV-2172) | eCat Order duplicate issue | To Do | Unprioritized | 265d | 🔴 249d |
| [SERV-2138](https://supercatsolutions.atlassian.net/browse/SERV-2138) | Missing Sales Portal Order | Code Review | Unprioritized | 336d | 🔴 335d |
| [EBR-568](https://supercatsolutions.atlassian.net/browse/EBR-568) | Retail customer ordering | Triaging | High | 685d | 🔴 234d |
| [EBR-507](https://supercatsolutions.atlassian.net/browse/EBR-507) | Discounting by a % | Triaging | High | 898d | 🔴 234d |
| [EBR-503](https://supercatsolutions.atlassian.net/browse/EBR-503) | Add Option (Fabric #) Search to Orders & Invoices | Triaging | High | 904d | 🔴 234d |
| [EBR-484](https://supercatsolutions.atlassian.net/browse/EBR-484) | Email variable %optionDescription% option forms | Triaging | High | 986d | 🔴 234d |
| [EBR-480](https://supercatsolutions.atlassian.net/browse/EBR-480) | Show/hide eOL ordering prices | Triaging | High | 986d | 🔴 234d |
| [EBR-445](https://supercatsolutions.atlassian.net/browse/EBR-445) | eOL pricing summary | Triaging | High | 1114d | 🔴 234d |
| [SERV-968](https://supercatsolutions.atlassian.net/browse/SERV-968) | Enable eOL print from within eCat | To Do | Medium | 1386d | 🔴 685d |

**Flags**:
- 🔴 **Stale backlog**: 10 of 16 tickets have no update in 14+ days. Six High-priority EBR tickets have sat in "Triaging" for 7+ months with no movement.
- ⚠️ **High priority tickets**: CSP-37 (High, active), plus 6 backlog tickets at High priority but no recent progress.
- **Unassigned**: EBR-758, EBR-757, EBR-756, EBR-755, EBR-726 — all recent submissions with no assignee.

**Cross-Surface Links**:
- EBR-758 (image rendering bug) ← HelpScout "Image & Asset Display" theme (3 conversations, 2 tagged `logged on jira`)
- EBR-726 (carrier field feature) ← HelpScout "eCat Question on Carrier Info" (`logged on jira`)
- CSP-37 (options config) ← HelpScout "Grand Options Program Scoping Call" (`status: support project`)

---

## Meeting Playbook

### Talking Points

1. **Dormant accounts are pure upside on a healthy platform** — External report highlights $185K in dormant account value (203 accounts gone quiet). Internally, Value Delivery is 90 (Thriving) and the ordering pipeline runs at 98.9% confirmed, so reactivation efforts ride on a working system with no platform risk.
2. **Per-rep ordering frequency is the biggest growth lever** — External report shows reps averaging 0.55 orders/user/90d vs. peer median of 1.12. Internally, this maps directly to Engagement at 40 (Watch) — the only non-green dimension. The external report's sales team data (coaching targets for Barbara Harper, Katrinka Barnhart, Jaime Hernandez) gives specific handles for improvement.
3. **Stale config data is a quiet risk** — External report flags 6 data entities stale since August 2025 (240 days) and kit items drifting from the refreshed catalog. Internally, Operational Health absorbs this at 88 (Thriving) because import health compensates, but catalog completeness at 82.4% trails the peer median of 95%. Prepare to explain what a config refresh involves.

### Not in the External Report

- **Health score 74 (Healthy), classification Maintain** — internal scoring, not shared with client
- **No churn risk** — all risk modifiers clear, all warning flags false
- **Engagement at 40 (Watch)** — the only dimension below Healthy; client sees per-rep data but not the aggregated health dimension
- **7 High-priority Jira tickets stagnant in Triaging** — oldest is 3+ years (EBR-445, eOL pricing summary); client may ask about long-standing feature requests
- **Active Options Config project (CSP-37)** — High priority Epic, pending client input; 4 new feature requests filed in April
- **Support history**: 18 conversations in 90 days, 3 L3 engineering escalations, 1 S1 critical (resolved)

### SuperCat Action Items

- [ ] **Enable Clicky Analytics** — `has_clicky_portal` = false. Portal traffic intelligence is unavailable for this Full-bundle client with 1,612 portal orders LTM.
- [ ] **Re-import kit items and matrix options** — Kit items are 58 days stale and price levels 44 days stale while the product catalog was refreshed 3 days ago. 2,086 kit configurations may reference outdated product data.
- [ ] **Triage or close stale backlog tickets** — 6 High-priority EBR tickets have been in "Triaging" for 7+ months. Either advance them or close with explanation before the client asks.
- [ ] **Assign EBR-758** — Image rendering bug (18 days old, unassigned) connects to a recurring HelpScout theme (3 conversations). Assign and prioritize.
- [ ] **Close the catalog completeness gap** — 394 products missing pricing and 207 missing images (82.4% vs. 95% peer median). A focused data cleanup would improve both Operational Health and the client-facing catalog experience.
