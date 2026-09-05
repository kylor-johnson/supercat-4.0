# Summer Classics Wholesale — Account Intelligence Brief

**Generated:** March 2, 2026 | **Data Period:** Jan 1 – Mar 2, 2026 (90 days) | **Framework:** v1.0

---

## B1. Account Identity & Context

| Field | Value |
|---|---|
| **Company Name** | Gabriella White (PostgreSQL org shortname: `sc`, ID: 69) |
| **Industry Segment** | Outdoor/Casual — premium outdoor furniture and home furnishings. Parent brand Summer Classics manufactures and retails through company-owned showrooms across the Southeast, Mid-Atlantic, and Southwest. Retail-direct model (not B2B wholesale through this entity). |
| **Headquarters / Region** | Pelham, AL (3140 Pelham Parkway, 35124) |
| **Products Active** | eCat iPad (CPQ) — since at least 2014. eCat Online — activated Aug 2025. Sales Portal — activated Aug 2025. eCat Online Closed Site — activated Aug 2025. **4/4 full suite + add-on.** |
| **Use-Case Profile** | **Ordering** — reps use Submit Order on iPad at point of sale in showrooms. 4,430 `order_submitted` Mixpanel events and 5,336 PostgreSQL orders in the 90-day period. Orders export via StdJSONv2 to `web.summerclassics.com`. |
| **Partner Since** | February 5, 2014 — **12.1 years.** One of the longest-tenured accounts in the portfolio. |
| **Account Owner** | HubSpot owner data unavailable (schema query failed). Operational callout: no assigned owner on record. |
| **Contract & Billing** | Billed monthly via QuickBooks. Combined parent entity "Summer Classics, Inc." invoiced ~$6,752–$6,986/mo (covers scw + sc); "SC Home/Gabby LLC" invoiced ~$1,917–$2,025/mo (covers gh). All invoices current ($0 balance). Stripe customer `cus_SXChHLspKtOS44` exists but subscriptions show 0 rows; deleted invoices suggest billing migrated to QuickBooks. Estimated sc entity MRR: ~$2,900–$3,200. |

**Relationship History Narrative:**
Summer Classics/Gabriella White has been a SuperCat client since February 2014, making it one of the earliest and most deeply embedded accounts. The relationship spans four eCat entities under one parent: Gabby (gh), Summer Classics Retail/Gabriella White (sc), Summer Classics Wholesale (scw), and Summer Classics Contract (sccon). The sc entity is the retail arm operating company-owned showrooms. The account expanded to the full 4-product suite in August 2025 (adding eCat Online, Portal, and Closed Site). With 155 licensed users, 27,173 products, 322,514 matrix options, and 91,081 customers, this is one of the most complex catalog configurations in the portfolio.

**Stakeholder Map:**

| Name | Role | Relationship to SuperCat | Last Interaction | Notes |
|---|---|---|---|---|
| Jonah Tibbs | eCat Administrator | Primary Technical Contact | Feb 3, 2026 (HelpScout) | Files majority of support tickets. Pushes feature requests and bug reports. Power admin — deeply engaged with platform capabilities. |
| Ben Erickson | eCat Administrator | Secondary Technical Contact | Jan 21, 2026 (HelpScout) | Handles integration and technical issues (import errors, order export). Also files enhancement requests. |
| Crayton Arivett | Operations (inferred) | End User Contact | Sep 17, 2025 (HelpScout) | Filed customer-facing issues (phone number display, password resets). |
| Sateesh Donti | Leadership (inferred) | Executive Sponsor (potential) | Feb 11, 2026 (CLM login) | Minimal app usage (2 logins, 0 feature events). May be oversight/approval role. |

**Industry & Company Context:**
Summer Classics is a premium outdoor furniture manufacturer headquartered in Pelham, AL. The Gabriella White brand is the retail-direct arm operating showrooms in Atlanta, Charlotte, Raleigh, Nashville, Annapolis, Scottsdale, Winter Park, Jacksonville, Chestnut Hill, San Antonio, and Pelham (showroom + outlet). The company also operates licensee locations (Richmond, Chicago, Dallas, Houston, Louisville, Southlake, St. Louis). The outdoor/casual furniture segment is seasonal with spring/summer peaks. Summer Classics competes in the premium tier with brands like Ratana, Brown Jordan, and Kingsley Bate.

---

## B2. Account Scores — Full Component Breakdown

### Expansion Readiness Score: 62/100 — Nurture

| Component | Weight | Score | Key Drivers |
|---|---|---|---|
| **Adoption Depth** | 30% | **88** | Active User Ratio: 84.5% (131/155) → 100. Activity Ladder: 6/6 levels active → 100. Feature Breadth: 9.8 avg features/user → 50. Subscription Completeness: 4/4 + add-on → 100. |
| **Business Impact** | 25% | **44** | Order Volume Trend: Growing 3mo (Dec→Jan→Feb) → 100. AOV $4,105 vs segment → 75. Customer Activation Rate: 2.2% → 0 (retail model distortion — 91K customers are end consumers, not B2B buyers). Digital Self-Service Rate: 0% (iPad-only ordering) → 0. |
| **Growth Signals** | 25% | **58** | MAU Trend: Flat (118→119→117) → 50. User Growth: Flat → 25. Expansion Signals: 5+ triggered → 100. Fathom Pain→Feature: N/A. HubSpot Deals: N/A (data unavailable). |
| **Relationship Strength** | 20% | **53** | Fathom Cadence: N/A (no meetings — redistributed). Days Since Last Interaction: 28d → 75. Stakeholder Breadth: 4 contacts → 50. HelpScout Responsiveness: Multiple pending, actively worked → 35. |

### Retention Risk Score: 24/100 — Low Risk

| Component | Weight | Score | Key Drivers |
|---|---|---|---|
| **Engagement Decline** | 30% | **38** | MAU Trend: Flat → 50. Active User Ratio Change: Flat (Dec→Feb ±1pt) → 50. Login Frequency: Increasing (events/user: 324→388→547) → 0. User Count: Flat → 50. |
| **Relationship Cooling** | 25% | **33** | Fathom inputs: N/A (no data — redistributed). HelpScout Pattern: Normal cadence maintained (~4 tickets/mo, consistent with historical) → 0. Unresolved Ticket Age: Oldest 54 days (#13779) → 100. Billing/Cancellation Tags: 0 → 0. |
| **Financial Distress** | 25% | **6** | Payment Status: Current → 0. Invoice Aging: All paid → 0. MRR Trend: Flat → 25. Order Revenue Trend: Growing strongly (Jan $3.6M → Feb $7.0M) → 0. |
| **Operational Deterioration** | 20% | **13** | Data Freshness: Today → 0. Import Error Rate: 0% → 0. Repeated Support Issues: 2 repeats (Copy Order bug, Import Error) → 50. Inventory Staleness: Today → 0. |

### Quadrant: GROW

Expansion Readiness of 62 places this account at the low end of Nurture — the adoption foundation is exceptionally strong (88 Adoption Depth), but Business Impact scoring is artificially suppressed by the retail showroom model's incompatibility with the Customer Activation Rate and Digital Self-Service Rate metrics (designed for B2B wholesale). Retention Risk of 24 confirms stability across all dimensions. The unresolved ticket age (54 days) is the only elevated risk input and reflects active feature development, not friction.

**Insufficient Data Flags:**
- Fathom: No meetings recorded for this account in last 180 days. Relationship Strength and Relationship Cooling Fathom inputs scored as N/A with weight redistributed. Surfaced as operational callout.
- HubSpot: Deal and company detail queries failed (column schema mismatch). Could not assess expansion deals or account owner assignment.
- Stripe Subscriptions: 0 rows in BigQuery. Billing appears to flow through QuickBooks. MRR estimated from Stripe deleted invoices and QB invoice amounts.

---

## B3. Rep Performance Intelligence

| Element | Value |
|---|---|
| **Total Reps / Active Reps** | 155 billable / 131 Mixpanel active (84.5%) / 114 CLM active with logins / 55 submitting orders |
| **Activity Ladder Results** | All 6 levels active org-wide. Level 1–2 (Customer Targeting + Product Discovery) dominant. Level 5 (Advanced: Kit/Configured Items) unusually strong — 6,969 kit orders, 1,964 configured items reflects the CPQ-heavy catalog. Levels 3–4 moderate. Level 6 present but lighter. |
| **Concentration Risk** | **Low.** Top order submitter (Julie Smallwood) = 8.9% of Submit Orders. Top 10 reps account for ~45% — well distributed across the sales force. |

**Power Users (Top 5 by composite activity):**

| Rep | Total Events | Logins | Submit Orders | Key Behaviors |
|---|---|---|---|---|
| Julie Smallwood | 16,506 | 139 | 1,094 | Highest order volume. 17 features used. Heavy customer search (7,820). |
| Dierdre Essix | 14,104 | 280 | 684 | Most logins. 16 features. Customer search leader (5,536). |
| LindaLee Counts | 13,218 | 300 | 596 | Highest login count. 20 features. Strong across all levels. |
| Jennifer Gormley | 11,472 | 206 | 413 | 19 features. Collection search power user (2,250). |
| Natalie Debruin | 10,485 | 157 | 528 | 21 features. Highest feature breadth in top 5. PDF catalog creator (129). |

**Enablement Gaps:**
- 59 users (38%) have CLM logins but zero Submit Order events — they browse catalog and search customers but don't complete transactions. These may be support staff, delivery personnel (e.g., "sc-delivery302"), or reps not yet activated on ordering.
- 7 users with zero logins in the period (fully inactive).
- Features with zero org-wide usage: Edit My List, Share My List, Create Maybe List, Export CSV/Excel, PDF Searches, Order From Maybe List, View Placements, View Commitments, View Flipbook, Add to List from Flipbook, Order from Flipbook.

**Feature Utilization Highlights:**

| Rank | Feature | Total Events | % Users Using |
|---|---|---|---|
| 1 | Search Products | 113,981 | ~95% |
| 2 | Search for Customer | 89,092 | ~80% |
| 3 | Select a Customer | 37,796 | ~70% |
| 4 | View Kit | 27,438 | ~50% |
| 5 | Order Kit | 20,989 | ~45% |
| Bottom | View Flipbook | 0 | 0% |
| Bottom | View Placements | 0 | 0% |
| Bottom | View Commitments | 0 | 0% |
| Bottom | Share My List | 0 | 0% |
| Bottom | Edit My List | 0 | 0% |

**Ordering Breakdown:**

| Metric | Value |
|---|---|
| Order Type | Confirmed: 1,647 (60.4%) · Quote: 1,067 (39.1%) · TEST: 12 |
| Order Origin (Top 5) | Pelham Showroom: 344 ($1.72M) · Atlanta Store: 319 ($1.37M) · Pelham Outlet: 272 ($745K) · Charlotte Store: 237 ($1.59M) · Scottsdale Store: 222 ($648K) |
| Territory (Top 5 by revenue) | 304: $799K · 301: $613K · 302: $586K · 303: $459K · 306: $415K |
| Orders per Active User | 2,726 / 131 = 20.8 orders/user in period |
| Revenue per Active User | $11.19M / 131 = $85,411/user in period |

---

## B4. Customer Intelligence

| Element | Value |
|---|---|
| **Total Customers in System** | 91,081 |
| **Customer Activation Rate** | 2,020 / 91,081 = 2.2% (60-day period). **Context:** This is a retail-direct model — "customers" are end consumers accumulated since 2014. The 2.2% rate reflects recent purchasing activity against a 12-year customer database, not B2B buyer activation. 2,020 unique purchasing customers in 2 months is substantial for a showroom retailer. |
| **Customer Concentration** | **Very low.** Top customer (Louise Copeland) = 1.5% of revenue ($168K). Top 10 customers = 5.7% of revenue. Extremely well-diversified customer base. |
| **Customer Favorites** | 129,925 customer favorite records — strong buyer engagement signal. |
| **Sales Data** | 109,507 sales data records imported — active ERP integration. |
| **Territory Coverage** | 0 territories configured in PostgreSQL. Territory assignments flow through the order system (42 distinct territory codes in the Orders CSV). This is a data gap — territory configuration in the app would enable territory-level filtering and Sales Portal dashboards. |

**Store Performance (Order Origins):**

| Store | Orders | Revenue | AOV |
|---|---|---|---|
| Pelham Showroom | 344 | $1,719,581 | $4,999 |
| Atlanta Store | 319 | $1,372,401 | $4,303 |
| Charlotte Store | 237 | $1,587,296 | $6,696 |
| Nashville Store | 204 | $998,041 | $4,892 |
| Raleigh Store | 209 | $879,489 | $4,208 |
| Annapolis Store | 207 | $523,161 | $2,527 |
| Scottsdale Store | 222 | $648,263 | $2,920 |
| Jacksonville Store | 153 | $517,143 | $3,380 |
| Pelham Outlet | 272 | $744,521 | $2,737 |
| Winter Park Store | 161 | $345,258 | $2,144 |
| Chestnut Hill Store | 132 | $419,998 | $3,182 |
| Richmond Licensee | 145 | $789,367 | $5,444 |
| Atlanta Outlet | 112 | $639,033 | $5,706 |

Charlotte Store and Atlanta Outlet have the highest AOVs ($6,696 and $5,706 respectively), while Winter Park and Annapolis have the lowest ($2,144 and $2,527). The variance suggests different customer mixes or product category focus across locations.

---

## B5. Relationship & Support History

### Fathom — Meeting Intelligence (Last 90 Days)

**No proactive meeting history on record for this account.** Fathom summaries reference Summer Classics only in internal support standups:
- Feb 2, 2026: Internal support standup (Kyla/Chuck) — SC "shared orders" bug is a priority for bug-fix release.
- Jan 28, 2026: Internal support standup — SC shared orders issue mentioned as pending user response.

**Recommendation:** Consider establishing a structured engagement cadence for this 12-year, ~$3K/mo account, especially given the EBR context and the active feature request pipeline from Jonah Tibbs/Ben Erickson. A quarterly check-in at minimum would surface expansion opportunities and demonstrate investment in the relationship.

### HelpScout — Support & Onboarding (Last 90 Days)

| Element | Value |
|---|---|
| **Ticket Volume (90d)** | 12 distinct tickets |
| **Ticket Volume Trend** | Consistent with historical cadence (~3–4 tickets/month). Not escalating. |
| **Open Tickets** | 7 open/pending |
| **Recurring Themes** | Order display/management issues (3), Bug reports (2), Feature enhancement requests (2), Import errors (2) |
| **Primary Contacts** | Jonah Tibbs (7 tickets), Ben Erickson (5 tickets) |
| **Assigned Agent** | Kyla Bosch (primary), Brent Sanders (secondary) |

**Recent Tickets (Last 5):**

| # | Subject | Status | Created | Threads | Notes |
|---|---|---|---|---|---|
| 13950 | Services Slow/Unresponsive | Closed | Feb 3 | 2 | Resolved same day. Platform-wide issue. |
| 13941 | No Warning When Dropped Products On Order | Pending | Feb 2 | 4 | Feature request — wants warning when discontinued items are on active orders. |
| 13928 | File Import Error | Pending | Jan 29 | 2 | Import processing issue. |
| 13893 | User Issue: Viewing Other Users' Quotes | Pending | Jan 23 | 5 | User permissions issue — reps seeing other reps' quotes. |
| 13872 | Copy Order and Option Form Bug | Pending | Jan 21 | 1 | Recurring bug — also reported Nov 2025. |

**Older Open Tickets of Note:**
- #13841 "Enhancement Request: Option Fields" (Jan 16, pending) — feature request for option field improvements.
- #13836 "All Orders & Quotes Issue" (Jan 15, pending) — 7 threads, order visibility issue.
- #13779 "eCat Issue - Blank Active Orders" (Jan 7, pending, **14 threads**) — longest-running open ticket. Complex issue with extensive back-and-forth.

### Combined Relationship Signals

| Signal | Value | Interpretation |
|---|---|---|
| **Days Since Last Touchpoint** | 28 days (HelpScout Feb 3) | Within normal range. All engagement is inbound (support-initiated). |
| **Communication Direction** | 100% inbound (HelpScout only). 0% outbound (no Fathom meetings). | Operational callout: consider establishing proactive outreach cadence. Not a risk flag — account is self-sufficient and engaged. |
| **Stakeholder Breadth** | 4 distinct contacts (Jonah Tibbs, Ben Erickson, Crayton Arivett, Sateesh Donti) | Moderately single-threaded on admin side (Jonah/Ben handle 95% of interactions). |

---

## B6. Expansion Whitespace

| Element | Detail |
|---|---|
| **Unused Modules** | None — 4/4 suite already active. However, eCat Online and Sales Portal were activated Aug 2025 and show minimal adoption (235 `view_portal` events). eCat Online ordering adoption = 0. These modules are technically enabled but not operationally activated. |
| **Triggered Expansion Signals** | **5+ active:** (1) Territory Count = 0 — no territories configured in PostgreSQL; (2) View Flipbook = 0 — Flipbook not enabled/adopted; (3) View Placements = 0 — Placements feature unused despite being enabled; (4) Library Access Without Sharing — 1,894 view_document events but only 382 email events (20% share rate); (5) Customer Product List Gap — 7 create_stack events vs. heavy My List usage; (6) High Quote rate (39%) may indicate pricing review opportunity. |
| **Feature Adoption Gaps** | **Placements:** Enabled (`placements_includes_discontinued_products: true`) but zero usage. For a retail showroom model with 13+ locations, Placements could drive showroom floor audits and reorder workflows. **Flipbook:** Not enabled (`enable_flipbook_support: false`). Given the retail presentation model, digital flipbooks could replace or augment the PDF catalog workflow. **Maybe Lists:** Zero usage — consideration-stage feature that could help reps track "thinking about it" items during showroom visits. **My List Sharing:** Zero Share My List events despite active My List usage — cross-rep collaboration opportunity. |
| **Seat Expansion Headroom** | 155 current users. With 13+ retail locations and licensee territories, there may be additional rep/store staff who could benefit from iPad access. The `sc-delivery302` user suggests delivery teams use the app — potential expansion to all delivery/warehouse staff. |

**Specific Expansion Recommendations:**

1. **Placements Activation** (high impact) — With 13+ showroom locations, Placements could provide national floor inventory visibility, drive reorder workflows, and evidence rep visit cadence. This is the single highest-value unused feature for a retail showroom model.

2. **Sales Portal Training** (medium impact) — Only 235 `view_portal` events in 90 days despite being enabled since Aug 2025. Reps and managers may not know the Sales Portal exists. Dashboard training could surface territory performance data currently invisible.

3. **Territory Configuration** (enabling) — 0 territories in PostgreSQL despite 42+ territory codes in order data. Configuring territories would unlock territory-level filtering in the app, Sales Portal dashboards, and rep performance segmentation.

4. **eCat Online Buyer Self-Service** (long-term) — Currently 0% digital self-service. Given the retail model, eCat Online could serve as a customer-facing catalog for post-visit browsing, wish list creation, and potentially online ordering. The infrastructure is already enabled.

---

## B7. Open Risks & Issues

| Element | Detail |
|---|---|
| **Unresolved Support Tickets** | 7 open/pending. Oldest: #13779 "Blank Active Orders" (Jan 7, 54 days, 14 threads). #13872 "Copy Order Bug" is a recurring issue (also reported Nov 2025). |
| **Stalled HubSpot Deals** | Data unavailable. |
| **Financial Flags** | None. All QuickBooks invoices current ($0 balance). Stripe not delinquent. |
| **Operational Flags** | None critical. Data freshness: today. Import frequency: ~13/day (1,190 in 90 days). Import error rate: 0%. Import types include Inventory, Customers, Images, Portal data. Integration is healthy and automated. |
| **Relationship Flags** | No Fathom meetings. No assigned account owner in HubSpot. All engagement is reactive (inbound support). For a 12-year, premium-tier account, this represents an underinvestment in proactive relationship management. |
| **Concentration Risk** | Low. Top order submitter = 8.9% of orders. Top customer = 1.5% of revenue. No single-point dependency. |

---

## B8. Context & Preparation — EBR with Gabby/Summer Classics Leadership

**Engagement Context:** EBR preparation — executive review with Gabby/Summer Classics leadership. This is one of four entities under the parent account (Gabby `gh`, Summer Classics Wholesale `scw`, Summer Classics Contract `sccon`, Summer Classics Retail/Gabriella White `sc`). Focus on this entity's data with cross-entity awareness.

### Engagement Objectives

1. **Acknowledge the depth of the partnership** — 12+ years, 155 users, full product suite, 27K+ products, and strong ordering velocity ($11.2M in 2 months) position this as one of the most embedded accounts in the portfolio.
2. **Surface Placements as the next activation frontier** — with 13+ showroom locations, this is the highest-value unused capability and aligns with their retail model.
3. **Establish a proactive engagement cadence** — transition from 100% inbound/reactive to scheduled touchpoints. This EBR itself is a first step.

### Key Data Points to Surface

- **$11.2M in order revenue** over 61 days (Jan–Mar 2) across 2,726 orders — demonstrating massive platform-driven business value.
- **84.5% Active User Ratio** — 131 of 155 reps actively using the platform. This is well above portfolio benchmarks.
- **6/6 Activity Ladder levels active** — deep and broad adoption across all feature tiers, including strong Level 5 (CPQ) engagement.
- **13+ store locations** with distinct performance profiles — Charlotte ($6,696 AOV) vs. Winter Park ($2,144 AOV) suggests localized opportunities.
- **Order volume growth: +53% MoM** (Jan → Feb) — the platform is becoming more central to operations, not less.

### Topics to Explore

- What's driving the Feb order surge? Seasonal (spring buying) or structural (new store, marketing push)?
- How are they using the retail showrooms' customer favorite data (129,925 records)?
- Is there interest in Placements for showroom floor management across all locations?
- What's the vision for eCat Online — buyer-facing catalog, online ordering, or both?
- Are there plans to onboard additional locations or licensees?

### Topics to Handle Carefully

- **7 open support tickets** — Jonah Tibbs has been actively filing feature requests and bug reports. Acknowledge the open items, provide timeline updates, and demonstrate that his feedback is valued and tracked.
- **The "Blank Active Orders" issue (#13779)** has 14 threads over 54 days. This should be addressed proactively before the EBR.
- **The "Copy Order Bug"** has been reported twice (Nov 2025 and Jan 2026). If it's still unresolved, it may surface as a frustration point.
- **No assigned account owner** — if leadership asks "who's our person?" be prepared to clarify the support structure and any proposed changes.

### Cross-Entity Observations

- Mixpanel shows `sc-*` prefix users accessing all four entities: sc (116,398 events), gh (31,509), scw (26,004), sccon (15,428). Shared rep pool across entities means feature adoption in one entity can be leveraged across others.
- QuickBooks billing is consolidated under "Summer Classics, Inc." and "SC Home/Gabby LLC" — combined parent MRR is ~$8,700/mo.
- Fathom mentions reference "Summer Classics shared orders" as a known bug being prioritized for fix — this may come up in the EBR.

### Commitments from Prior Engagement

No formal prior engagement commitments on record (no Fathom meeting history). However, the following HelpScout commitments are implicit:
- Fix for "Copy Order and Option Form Bug" (recurring since Nov 2025)
- Resolution of "Blank Active Orders" display issue (54 days open)
- Enhancement review for "Option Fields" feature request
- Investigation of "Viewing Other Users' Quotes" permissions issue
