# Internal Intelligence Brief — Charleston Forge

*April 20, 2026 · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

Charleston Forge is a moderately stressed account with exceptional product adoption masking serious engagement and trajectory declines. The platform is deeply embedded in their workflow (Adoption 89, top quartile among peers), but users are logging in less and the primary value metric is declining quarter over quarter. Dan Minor — who drives 47% of iPad GMV — saw a 50% order volume drop in the last 90 days, and territory activation sits at just 9%. The meeting should focus on re-engagement and stabilization, not feature expansion: address the top rep's declining activity, push dormant buyer reactivation (721 lapsed accounts, $155K+ in top-5 dormant value), and refresh 9 stale data entities that drag Operational Health.

**Three Things That Matter:**

1. **Engagement is critically low at 20 — the #1 health deficit** — Login frequency and active user ratio are well below peers (peer median: 35). This single dimension is the primary reason the account falls into Watch territory. The external report confirms the team uses the platform heavily for browsing and presenting but actual login intensity is declining. Solving this is prerequisite to any expansion conversation.

2. **Top rep's activity dropped 50% in 90 days** — Dan Minor contributes 47% of iPad GMV ($351K trailing 12 months) and his order volume halved in the most recent quarter. Erica Reece and Minor together account for nearly half of all iPad revenue. This concentration risk + declining trajectory (score: 30, At Risk) makes rep re-engagement the most urgent conversation topic.

3. **721 lapsed buyers are the biggest upside — but stabilize first** — The external report identifies 721 dormant eCat accounts and $155K in top-5 dormant value. eCat Online independently acquired 22 new buyers (39% of total new orderers). The opportunity is real, but this is a Stabilize First account — health must improve before expansion programs can succeed.

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | **52** / 100 | **Stabilize First** |
| **Band** | Watch | Fix health before expansion |

> Charleston Forge (iPad+Catalog+Cart) scores 52 Health → Stabilize First. Engagement (20) is the primary health deficit; stabilize engagement before pursuing expansion.

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| **Engagement** (25%) | 20 | 🔴 At Risk | Critically low login frequency and active user ratio. Peer median engagement is 35 — Charleston Forge is 43% below peers. The external report confirms declining login activity and orders per user at 0.08 vs. peer median of 0.83. This is the single largest drag on overall health. |
| **Adoption** (20%) | 89 | 🟢 Thriving | Using 8 of 9 available features above minimum thresholds (iPad+Catalog+Cart bundle: product search, customer selection, presentations, email sharing, PDF catalogs, document viewing, stacks, eCat Online, and order submission). Top quartile among peers (peer median: 78). Platform is deeply embedded. |
| **Value Delivery** (30%) | 60 | 🟢 Healthy | For iPad+Catalog+Cart bundles, Value Delivery = average of Order Volume Score + Customer Activation Score + eCat Online Share Score. Score of 60 indicates moderate performance: eCat Online order share has grown from 17% to ~50% (strong), but order volume is declining and customer activation rate is low (only 200 of 921 accounts active in trailing 12 months). |
| **Operational Health** (15%) | 54 | 🟡 Watch | Nine data entities haven't been refreshed since August 2025 (8+ months). Core catalog data (products, customers, options) remains fresh, but the stale entities drag Data Freshness down. Import health and catalog completeness appear adequate. This is a SuperCat-side maintenance issue. |
| **Trajectory** (10%) | 30 | 🔴 At Risk | Q/Q trend is declining. The primary value metric (orders for iPad+Catalog+Cart bundles) dropped quarter over quarter, driven by Dan Minor's 50% order decline and flat activity from other reps. Login activity is also declining. Peer median trajectory is 80 — Charleston Forge is severely below peers. |

### Flags

- No risk modifier fired
- No churn risk flagged (despite Watch band — health score is 52, above the 20 threshold)
- ⚠️ **`hs_lifecycle_stale = true`** — HubSpot shows stale lifecycle status for this org. Does not affect scoring but warrants CRM data hygiene follow-up.
- ⚠️ **`hs_join_missing = true`** — No HubSpot join exists for this org. Peer benchmarking falls to bundle-only (Tier 3) cohort instead of vertical × stack (Tier 1).
- `arr_data_gap = false` — ARR data is present ($21,066)
- Scoring status: complete (no missing data)

<details>
<summary><strong>How Health Scoring Works</strong></summary>

The health score (0-100) combines five dimensions weighted by importance. For Charleston Forge's bundle (iPad+Catalog+Cart), the formula is:

- **Engagement (25%)** — Are users logging in and actively using the platform? Measured by login frequency and the ratio of active to provisioned users.
- **Adoption (20%)** — How many of the 9 available features are being used above minimum thresholds? Features include product search, customer selection, presentations, email sharing, PDF catalogs, document viewing, stacks, eCat Online, and order submission.
- **Value Delivery (30%)** — Is the platform generating business value? For iPad+Catalog+Cart bundles, this is the average of Order Volume Score (how many orders are submitted), Customer Activation Score (what % of customers are placing orders), and eCat Online Share Score (what % of orders come through the self-service storefront vs. iPad).
- **Operational Health (15%)** — Is client data clean and current? Three sub-scores: Import Health (50%), Catalog Completeness (30%), and Data Freshness (20%).
- **Trajectory (10%)** — Is activity trending up, flat, or down? Compares the most recent 90 days to the prior 90 days on login activity and the primary value metric (orders for this bundle).

**Health Bands**: Thriving (80-100), Healthy (60-79), Watch (40-59), At Risk (20-39), Critical (0-19).

**Classification** determines the recommended action cadence:
- **Expand** — healthy account with strong expansion signals
- **Maintain** — healthy, protect with standard cadence
- **Stabilize First** — needs health improvement before any expansion ← Charleston Forge is here
- **Intervene** — immediate save/recovery plan needed

</details>

---

## Support & Issue Themes

> 9 conversations in 90 days. Training-forward, low volume. No active fires.

### Themes

**1. Training & onboarding workflows** (3 of 9 tickets)
- Link to Philip's eCat Training Videos, Link?, Additions to meeting
- **Impact**: Three tickets in a single cluster (Jan 29) around training video access and meeting prep. Indicates the team was actively preparing for a training/onboarding session — a healthy engagement signal, not a problem.
- **Root**: Scheduled training session required quick-turn support for links and logistics.
- **Action**: Confirm the training session went well. If platform engagement didn't increase post-training, the session may not have stuck — use the meeting to discuss what follow-up training could help.

**2. Data sync & catalog management** (2 of 9 tickets)
- FW: Ecat Price Change Help, Issues with Collections showing up in catalog
- **Impact**: Price change workflows and catalog display issues suggest the team manages active catalog updates but encounters friction. Aligns with the 9 stale data entities identified in the external report.
- **Root**: Data management workflows require support touchpoints. The stale entity backlog may create confusion about which data is current.
- **Action**: Tie to the config refresh SuperCat action item. Refreshing stale entities will reduce future data sync tickets.

**3. User management & access** (2 of 9 tickets)
- Product gone (eOL), Log in issue for Susan Barber
- **Impact**: Access and visibility issues on eCat Online and Admin Console. The "Product gone" ticket (S3/Medium — the only non-S4 ticket) suggests a product visibility issue on the online storefront.
- **Root**: User-level access management and catalog visibility settings.
- **Action**: Low-impact theme. Standard L1 support, both resolved.

### Escalation Profile

9 of 9 conversations at L1 (frontline resolved). No L2, L3, L4, or executive escalations. Peak severity: S3/Medium (product visibility on eOL). All other 8 tickets S4/Low. This is a clean support profile — no operational fires.

### Open Tickets (0)

No open support tickets. Clean inbox.

---

## Active Engineering & Projects

1 open Jira ticket references Charleston Forge. It is extremely stale and likely a zombie ticket.

| Key | Summary | Status | Priority | Project | Age | Last Update |
|---|---|---|---|---|---|---|
| [SERV-1661](https://supercatsolutions.atlassian.net/browse/SERV-1661) | Something about overhauling eOL L&F | To Do | 🔴 High | Server | 788d | Jul 2024 (657d ago) |

### Flags

- 🔴 **STALE**: SERV-1661 has not been updated in 657 days. High priority but unassigned with a vague summary. Likely a zombie ticket that should be triaged, scoped, or closed.
- 🔴 **HIGH PRIORITY**: Marked High but in To Do with no assignee — priority doesn't match the lack of attention.

### Cross-Surface Links

- **No HelpScout → Jira cross-links**: Zero support conversations tagged `status: logged on jira` in the 90-day window. Support issues are being handled at L1 without engineering escalation.
- **eOL theme**: SERV-1661 references eOL look-and-feel overhaul. The "Product gone" support ticket (eOL product visibility issue) and the growing eCat Online order share (17% → 50%) suggest the storefront experience matters increasingly. If this ticket represents real work, it's worth reviving.

*JQL search strategies: `text ~ "Charleston Forge"` (1 result), `text ~ "cfg"` (3 results, 2 filtered as not client-specific).*

---

## Meeting Playbook

### Talking Points

1. **721 lapsed buyers = biggest revenue opportunity** — The external report headlines 721 dormant eCat accounts with $155K in the top 5 alone. Internally, Value Delivery is at 60 (Healthy) with customer activation at roughly 22% (200 of 921 accounts active). The reactivation conversation is pure upside — but frame carefully given the Stabilize First classification. Re-engaging lapsed buyers works best alongside re-engaging lapsed reps.

2. **Dan Minor's declining trajectory is the internal alarm** — The external report identifies a 50% order drop from the #1 iPad GMV contributor. Internally, this directly drives the Trajectory score (30, At Risk) and Engagement score (20, At Risk). This is not in the external report's framing as an internal health metric — but the rep-level data is. Use it to open a conversation about team enablement and whether the decline is a platform issue or a business cycle.

3. **eCat Online is a growing success story — lean into it** — External report shows eCat Online order share grew from 17% to ~50% and independently acquired 22 new buyers (39% of total). Internally, portal draws 223 daily visitors with 6.4-minute sessions. This is a genuine platform win to celebrate. Frame the self-service channel growth as validation of their iPad+Catalog+Cart investment.

### Not in the External Report

These facts are internal-only — the client will never see them:
- **Health score: 52 (Watch)** — scores, bands, and classifications are never shown externally
- **Classification: Stabilize First** — health must improve before expansion programs can succeed
- **No churn risk flagged** — despite Watch band, health score (52) is above the 20 threshold for churn_risk
- **Warning flags active**: `hs_lifecycle_stale` and `hs_join_missing` — HubSpot data is stale/missing for this org, affecting CRM data quality but not scoring
- **Support pattern**: Training-forward, low volume, all frontline resolved. Zero open tickets.
- **Jira**: 1 extremely stale ticket (SERV-1661, 657 days since update). No active engineering work for this client.

### SuperCat Action Items

- [ ] **Refresh 9 stale data entities** — All 9 share the same August 2025 import date, suggesting an abandoned batch. Refreshing pricing, inventory, and stale configuration data will improve the Operational Health score (currently 54) and close the data freshness gap flagged in peer benchmarking.
- [ ] **Triage or close SERV-1661** — High priority, To Do, no assignee, 657 days since last update. Either scope the eOL L&F overhaul as real work (the storefront matters more now with 50% order share) or close the ticket. Don't let a zombie ticket misrepresent engineering commitment.
- [ ] **Investigate HubSpot data gaps** — Both `hs_lifecycle_stale` and `hs_join_missing` are flagged. Populate `hubspot_company_id` and update lifecycle status. Not urgent for scoring, but improves CRM hygiene and peer benchmarking accuracy (currently Tier 3 fallback instead of Tier 1).
- [ ] **Prepare re-engagement discussion** — Engagement at 20 and Trajectory at 30 are the two critical dimensions. Come to the meeting with a concrete plan for rep re-engagement (especially Dan Minor) and lapsed buyer reactivation sequencing.

---

*Brief generated from: Health V2 v2.5.1 (2026-04-14), HelpScout via BigQuery (2026-04-21), Jira via Atlassian MCP (2026-04-21), org_summary. External report: cfg_2026-04-20.*
