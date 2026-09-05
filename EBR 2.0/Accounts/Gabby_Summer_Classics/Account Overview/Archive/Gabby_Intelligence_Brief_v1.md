# Gabby — Account Intelligence Brief

**Generated:** March 3, 2026 | **Data Period:** Sep 2025 – Mar 2026 (180 days) | **Scoring Period:** Dec 2025 – Mar 2026 (90 days)

---

## B1. Account Identity & Context

| Field | Value |
|---|---|
| **Company Name** | Gabby (legal: SC Home/Gabby LLC) |
| **Industry Segment** | Outdoor/Casual Furniture. Gabby is the indoor furniture and home décor brand under the Gabriella White parent company, headquartered in Pelham, AL. Sibling brands include Summer Classics (outdoor furniture). |
| **Headquarters / Region** | Pelham, AL |
| **Products Active** | eCat iPad (since 2013), eCat Online Service, eCat Online Portal (Sales Portal), eCat Online B2B Cart, eCat Online Closed Site. All subscription plans created Aug 26, 2025 — suggests a billing restructure/migration. |
| **Use-Case Profile** | **Ordering** — reps actively submit orders through the iPad app. 2,113 `order_submitted` events in Mixpanel (90d), 3,251 orders in PostgreSQL (90d), 2,215 orders in Admin Orders Report (Jan 1 – Mar 3, 2026). |
| **Partner Since** | April 24, 2013 — nearly 13-year tenure |
| **Account Owner** | Not assigned in HubSpot. Primary SuperCat contacts: Kyla Bosch (support), Brent Sanders (engineering escalations) |
| **Contract & Billing** | MRR: $2,097 (Gabby entity via Stripe). Combined parent (SC Home/Gabby + Summer Classics + SC Contract): ~$8,975/mo. Payment via Stripe invoice, Net 15 terms. All invoices current. |

**Relationship History Narrative:**
Gabby has been a SuperCat client since April 2013, making it one of the longest-tenured accounts in the portfolio. The organization runs a large, distributed sales force (60+ billable users across rep, CS, and admin roles) submitting orders through the iPad app. The relationship has been operationally deep — high usage, active support engagement — but proactive strategic engagement (Fathom-recorded meetings, HubSpot deals) is absent. The August 2025 subscription plan creation suggests a recent billing migration. The account is one of four entities under the Gabriella White parent: Gabby (gh), Summer Classics (scw), Summer Classics Contract (sccon), and Summer Classics Wholesale (sc), sharing a common rep pool with "sc-" prefixed usernames.

**Stakeholder Map:**

| Name | Role | Relationship to SuperCat | Last Interaction | Notes |
|---|---|---|---|---|
| Jonah Tibbs | IT/Tech Lead (Employee - Admin) | Technical Lead / Champion | Feb 3, 2026 (HelpScout) | Primary ticket submitter — 8+ tickets in 90d. Handles product bugs, feature requests, data import issues. |
| Ben Erickson | Admin (Employee - Admin) | Technical Lead | Jan 21, 2026 (HelpScout) | Submits operational issues — order bugs, user settings, eCat Online configuration. |
| Crayton Arivett | Employee - User Setup | Operational | N/A | Manages user provisioning for the org. |
| John Redo | Employee - User Setup | Operational | N/A | Secondary user setup contact. |

**Industry & Company Context:**
Gabriella White operates in the mid-to-high-end indoor/outdoor furniture market. The Gabby brand focuses on transitional and modern furniture and home accessories for the trade (interior designers, retailers). The parent company also owns Summer Classics, a leading outdoor furniture brand. The combined operation has significant trade show presence (High Point Market, Dallas Market) reflected in seasonal order volume spikes.

---

## B2. Account Scores — Full Component Breakdown

### Expansion Readiness Score: 62/100 — Nurture

| Component | Weight | Score | Key Drivers |
|---|---|---|---|
| **Adoption Depth** | 30% | **92** | Active User Ratio 93% (56/60), all 6 Activity Ladder levels active, Feature Breadth 9.8/user, Subscription Completeness 4/4 + add-ons |
| **Business Impact** | 25% | **56** | Order volume flat (Dec 514→Jan 905→Feb 791 = seasonal volatility), AOV $3,123 (above segment median), Customer Activation 8.2% (low — 968/11,812), Digital Self-Service 35.8% (Website orders) |
| **Growth Signals** | 25% | **41** | MAU growing 2 months (42→44→49), user growth flat, 3 expansion signals triggered, 0 HubSpot deals, Fathom N/A |
| **Relationship Strength** | 20% | **50** | Days since interaction: 28, stakeholder breadth: 2 contacts, HelpScout responsive but 7 pending tickets. Fathom N/A — weight redistributed. |

### Retention Risk Score: 22/100 — Low Risk

| Component | Weight | Score | Key Drivers |
|---|---|---|---|
| **Engagement Decline** | 30% | **19** | MAU growing (0 risk), Active User Ratio increased (0 risk), login frequency stable-high (25), user count flat (50) |
| **Relationship Cooling** | 25% | **33** | Fathom N/A (redistributed). HelpScout cadence normal (0 risk), but oldest unresolved ticket 55 days old (100 risk), no billing/cancellation tags (0) |
| **Financial Distress** | 25% | **19** | All payments current (0), MRR growing (0), but order revenue declined Jan→Feb -29% (75) — likely seasonal (market month normalization) |
| **Operational Deterioration** | 20% | **14** | Data freshness: today (0), import errors: low (5), 2 repeated support topics — file import errors and copy order bug (50), inventory fresh (0) |

### Quadrant: GROW

Gabby is a deeply embedded, long-tenured account with near-complete adoption and low churn risk. The Expansion Readiness score of 62 lands in the Nurture band — the gap to Active Target (80+) is driven by low Customer Activation (8.2%), absence of proactive engagement (no Fathom, no HubSpot deals), narrow stakeholder breadth (2 contacts), and seasonal order volatility masking true business impact. The account is stable and growing at the engagement layer; the opportunity is to convert that engagement depth into measurable business expansion through buyer activation and L4 feature adoption.

**Insufficient Data Flags:**
- Fathom: No Gabby-specific meetings in 180 days — Relationship Strength and Relationship Cooling scored with weight redistributed to remaining inputs. Surfaced as operational callout.
- HubSpot: No deals found — Growth Signals HubSpot input scored as 0. Company record may use different naming or may not exist.
- QuickBooks: Query failed (schema mismatch) — financial data sourced from Stripe only.

---

## B3. Rep Performance Intelligence

| Element | Value |
|---|---|
| **Total Reps / Active Reps** | 114 users with logins (CLM), 56 canonical active (Mixpanel 90d) |
| **Activity Ladder Results** | L1 92%, L2 95%, L3 63%, **L4 21%**, L5 86%, L6 83%. Level 4 (Personalization) is the singular adoption gap — reps skip from discovery/sharing straight to advanced features. |
| **Ordering Users** | 55 of 114 (48%) submit orders. Top orderer: Julie Smallwood at 8.9% of total — well-distributed, no concentration risk. |

**Power Users (Top 5 by CLM activity):**

| Rep | Total Events | Orders | Features | Ladder | Logins |
|---|---|---|---|---|---|
| sc-julies (Julie Smallwood) | 16,645 | 1,094 | 13 | L5/6 | 139 |
| sc-dierdree (Dierdre Essix) | 14,384 | 684 | 13 | L5/6 | 280 |
| sc-lindac (LindaLee Counts) | 13,518 | 596 | 15 | L5/6 | 300 |
| sc-jenniferg (Jennifer Gormley) | 11,678 | 218 | 15 | L5/6 | 206 |
| sc-natalied (Natalie Debruin) | 10,642 | 309 | 14 | L5/6 | 157 |

**Enablement Gaps:**
- 59 of 114 reps (52%) have zero Submit Order events — they log in and browse but do not transact. These are training candidates for order workflow adoption.
- L4 feature usage: Only 24 reps (21%) use any personalization features (My List, Customer Product Lists, Favorites, Backorders). The gap between L3 (63%) and L4 (21%) is the largest ladder drop-off.
- 7 reps logged in only 1–5 times in the period (brendae, dls-kat, ryanw, sc-brookehj, sdonti, sc-mallorym, sc-margaretm) — minimal engagement.

**Concentration Risk:** Low. Top orderer (Julie Smallwood) represents 8.9% of total orders. Top 10 orderers represent ~47% — no bus factor risk.

**Ordering Detail:**

| Metric | Value |
|---|---|
| **Order Type Breakdown** | Confirmed 87.3% (1,934), Quote 12.4% (274), TEST 0.3% (7) |
| **Order Origin** | Regular 64.2% (1,422), Website 35.8% (793) |
| **Quote-to-Confirmed Ratio** | 7.1:1 (healthy — most orders go straight to confirmed) |

**Territory Performance (Top 5):**

| Territory | Orders | Revenue | Customers | AOV |
|---|---|---|---|---|
| South Team | 760 | $2,543,453 | 338 | $3,347 |
| Midwest Team | 412 | $1,151,400 | 182 | $2,794 |
| Texas Team | 371 | $1,125,701 | 159 | $3,034 |
| MidAtlantic Team | 232 | $515,709 | 120 | $2,223 |
| Florida Team | 96 | $259,506 | 55 | $2,703 |

South Team drives 36.8% of total revenue — elevated but below the 40% concentration threshold. MidAtlantic and Florida show lower AOV, suggesting different customer mix or product assortment in those regions.

---

## B4. Customer Intelligence

| Element | Value |
|---|---|
| **Total Customers in System** | 11,812 |
| **Customer Activation Rate** | 968 ordering customers / 11,812 = **8.2%** |
| **Unique Ordering Customers (Jan–Mar)** | 968 |
| **Customer Concentration** | Very low — top customer (Gillenwater Flooring) at 1.8% of revenue. No single-customer dependency. |
| **Territory Coverage** | 233 territories configured. Admin Orders Report shows 10+ active territories with orders. Several territories appear to be individual rep territories (e.g., "Savanna Dunaway", "zz!-Paul Bentley Team") vs. regional teams. |
| **Self-Service Adoption** | Website-origin orders = 35.8% of total volume, indicating meaningful eCat Online/B2B Cart usage by buyers. |

**Customer Activation Opportunity:**
With 11,812 customers in the database and only 968 ordering in the measurement period, 91.8% of the customer base is dormant. Even a 5-point improvement (to 13%) would add ~590 ordering customers. Given the $3,123 AOV, activating dormant customers is the highest-leverage growth opportunity.

**Monthly Customer Ordering Pattern:**
- January: Higher AOV ($3,693) — likely market/trade show driven
- February: Lower AOV ($2,592) — regular business baseline
- This seasonal pattern is normal for the outdoor/casual furniture segment

---

## B5. Relationship & Support History

### Fathom — Meeting Intelligence (Last 90 Days)

No Gabby-specific meetings recorded in Fathom in the last 180 days. The three Fathom results matching "Gabby" are internal SuperCat meetings or prospect calls where the brand was referenced in passing — none are direct Gabby account meetings.

**Operational callout:** No proactive meeting history on record for this 13-year, $2,097/mo account. Consider establishing a structured engagement cadence — even quarterly check-ins would provide strategic signal and strengthen the relationship beyond reactive support.

### HelpScout — Support & Onboarding (Last 90 Days)

| Element | Value |
|---|---|
| **Ticket Volume (90d)** | 12 tickets (Dec 2025 – Mar 2026) |
| **Ticket Volume Trend** | Consistent — ~4–5 tickets/month over 180 days (27 total in 180d) |
| **Open/Pending Tickets** | 7 pending: Blank Active Orders (Jan 7), All Orders & Quotes issue (Jan 15), Enhancement: Option Fields (Jan 16), Copy Order Bug (Jan 21), User Quotes Issue (Jan 23), File Import Error (Jan 29), Dropped Products Warning (Feb 2) |
| **Recurring Themes** | Order management bugs (3), file import errors (2), feature enhancements (2), eCat Online configuration (1) |
| **Primary Submitters** | Jonah Tibbs (8 tickets), Ben Erickson (6 tickets) — single-threaded engagement |

**Recent Tickets (Last 5):**

| Date | Subject | Status | Assignee |
|---|---|---|---|
| Feb 3 | Services Slow/Unresponsive | Closed | Kyla Bosch |
| Feb 2 | No Warning on Dropped Products on Order | Pending | Kyla Bosch |
| Jan 29 | File Import Error | Pending | Kyla Bosch |
| Jan 23 | User Issue: Viewing Other Users' Quotes | Pending | Unassigned |
| Jan 21 | Copy Order and Option Form Bug | Pending | Kyla Bosch |

### Combined Relationship Signals

| Signal | Value | Interpretation |
|---|---|---|
| **Days Since Last Touchpoint** | 28 days (HelpScout, Feb 3) | Approaching 30-day threshold — note for awareness |
| **Communication Direction** | 100% inbound (HelpScout) / 0% outbound (Fathom) | All reactive — the account reaches out to us, we don't proactively engage. Consider establishing outbound cadence. |
| **Stakeholder Breadth** | 2 distinct contacts (Jonah Tibbs, Ben Erickson) | Single-threaded risk. Both are technical/admin roles. No executive or business stakeholder relationship on record. |

**HelpScout Absence Protocol Note:** This is NOT a low-ticket account. Gabriella White maintains a consistent ~4.5 tickets/month cadence, indicating active platform investment and engagement. The ticket themes are substantive (bugs, feature requests, data issues) not basic how-to questions — this is a sophisticated, deeply embedded client pushing the platform's boundaries.

---

## B6. Expansion Whitespace

| Element | Detail |
|---|---|
| **Unused Modules** | All 4 core products active. No module-level upsell gap. Potential add-on opportunity: Flipbook (some existing usage), enhanced integration tiers. |
| **Triggered Expansion Signals** | 3 active: (1) **L4 Underutilization** — 79% of reps skip personalization features; (2) **High AOV + Low Activation** — $3,123 AOV with 8.2% customer activation; (3) **Customer Product List Gap** — near-zero Customer Product List creation despite active My List usage |
| **Feature Adoption Gaps** | My List creation/edit: 14 users. Customer Product Lists: 4 users. Share My List: 0 events. View Cust. Favorites: 86 events (sparse). These L4 features represent the largest untapped behavior cluster. |
| **Seat Expansion Headroom** | 114 CLM users, 60 billable in PG. Some CS users (35 disabled) and Customer Portal users (7,732 total, 66 active) represent potential expansion if eCat Online self-service grows. |
| **Peer Benchmarking** | Among outdoor/casual furniture accounts of similar tenure and rep count, Gabby's L5/L6 usage (86%/83%) is strong. The L4 gap at 21% is an outlier — peer accounts with similar L2/L3 adoption typically show 40–60% L4 engagement. |

**Highest-Impact Opportunities:**

1. **Customer Activation Program** — 968 of 11,812 customers ordering (8.2%). A targeted re-engagement campaign using Customer Product Lists and email-driven outreach through the platform could meaningfully increase penetration. Business case: Adding 300 customers at $3,123 AOV = $937K incremental order revenue.

2. **L4 Feature Training** — Only 21% of reps use personalization features. A focused training session on My List, Customer Product Lists, and Customer Favorites for the 90 reps currently at L3 but not L4 could deepen buyer relationships and increase reorder rates.

3. **Territory Optimization** — South Team at 36.8% of revenue. MidAtlantic and Florida have lower AOV ($2,223 and $2,703 vs. $3,347 for South). Enablement in underperforming territories could balance revenue distribution.

---

## B7. Open Risks & Issues

| Element | Detail |
|---|---|
| **Unresolved Support Tickets** | 7 pending tickets, oldest 55 days (Jan 7 — Blank Active Orders). Mix of bugs (3), enhancements (2), and data issues (2). Pending backlog is growing — 5 tickets from January alone still open. |
| **Stalled HubSpot Deals** | None found — no deals tracked in HubSpot for this account. |
| **Financial Flags** | None. All invoices current, MRR growing slightly. Order revenue declined 29% Jan→Feb but this is consistent with seasonal market month normalization (January = High Point/trade show spike). |
| **Operational Flags** | Data freshness excellent (imports today, 1,405 in 90d = ~15.6/day). 1,112 options configured, 84 price levels, 1,986 taxonomies — deeply configured org. Two repeated file import error tickets suggest potential integration friction. |
| **Relationship Flags** | No Fathom meetings on record. Stakeholder breadth limited to 2 technical contacts — no executive relationship documented. 28 days since last interaction. |
| **Concentration Risk** | Low across all dimensions. Top orderer 8.9%, top customer 1.8% of revenue, top territory 36.8%. No single-point dependency. |

---

## B8. Context & Preparation

*Context: EBR preparation — executive review with Gabby/Summer Classics leadership. This is one of four entities under the parent account (Gabby gh, Summer Classics scw, Summer Classics Contract sccon, Summer Classics Wholesale sc). Focus on this entity's data but note any cross-entity observations.*

### Engagement Objectives

1. **Establish a proactive relationship cadence.** This 13-year account has zero recorded strategic meetings. The EBR itself is a reset — use it to formalize quarterly touchpoints and identify an executive sponsor beyond the technical contacts.
2. **Present the Customer Activation opportunity.** 8.2% activation with $3,123 AOV is the most compelling growth story. Frame it as "your reps are doing great with the customers they reach — how do we help them reach more?"
3. **Address the pending support backlog.** 7 open tickets pre-dating this meeting signals operational friction. Come prepared with status updates or resolutions for the top 3 bugs (Blank Active Orders, Copy Order Bug, File Import Error).

### Key Data Points to Surface

- **93% Active User Ratio** — nearly everyone uses the platform. Lead with this as a strength.
- **$6.92M in orders (Jan–Mar)** — tangible business value flowing through the platform.
- **L4 adoption gap (21% vs. 86% at L5)** — unusual pattern. Ask: "Is there a reason your reps skip the personalization features?" The answer might reveal a workflow or training gap.
- **968 of 11,812 customers ordering** — frame as untapped potential, not a failure. "You have a massive customer database. What would it mean if even 15% were actively ordering?"
- **Website orders at 35.8%** — buyer self-service is already happening. Validate whether the B2B Cart experience meets expectations.

### Topics to Explore

- Who are the internal champions beyond Jonah and Ben? Is there a VP of Sales or COO who should be part of strategic conversations?
- How does Gabby's catalog and ordering workflow differ from the Summer Classics entities? Any cross-entity learnings?
- What drove the January order spike? Was it a specific market (High Point, Dallas) or internal sales push?
- Are the 11,812 customers all actively sellable, or is there cleanup needed? (Low activation might partly reflect a stale customer database.)
- What is the data import workflow that's causing repeated errors? Is there an ERP integration opportunity?

### Topics to Handle Carefully

- **Pending tickets:** 7 unresolved tickets may come up. Have updates ready. Avoid being defensive — acknowledge the backlog and present a resolution timeline.
- **Revenue decline Jan→Feb:** Down 29% but likely seasonal. If they raise it, reframe around the healthy annualized run rate rather than month-over-month volatility.
- **Absence of proactive engagement:** Don't call attention to the fact that we've had no strategic meetings in 13 years. Instead, frame this EBR as "the beginning of a more strategic cadence" and let the value of the conversation speak for itself.

### Commitments from Prior Engagement

No Fathom-recorded meetings with action items. The most recent HelpScout interactions (Jonah Tibbs, Feb 3) relate to service performance issues. Kyla Bosch is the primary support contact handling this account.

### Cross-Entity Observations

- **Shared rep pool:** Most reps use "sc-" prefix usernames and work across all 4 entities. The CLM data (121 users) likely spans all entities, not just Gabby.
- **Billing:** SC Home/Gabby LLC and Summer Classics are billed separately in Stripe. Gabby MRR $2,097; Summer Classics ~$6,878. Combined parent ~$8,975/mo.
- **Mixpanel tracking:** Events are tracked by `current_organization_shortname`, meaning a rep's activity in the gh org context counts toward Gabby's metrics even if they're primarily assigned to another entity. This is correct behavior for shared reps.
- **HelpScout org:** Tickets filed under "Gabriella White" — the parent brand, not entity-specific. Support themes likely span all entities.

---

*Version B — Account Intelligence Brief | Gabby (gh) | Generated March 3, 2026*
