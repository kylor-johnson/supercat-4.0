# Metrics Framework for Executive Insights, QBRs & Expansion

**Full Surface Area Reference** | v3.0 — Feb 2026

> Covers every metric derivable from the SuperCat data stack: BigQuery (HelpScout, Fathom, HubSpot, Mixpanel, Stripe, QuickBooks), PostgreSQL via MCP, Admin Console reports, and TTFV analysis. Organized for both generic QBR use and client-specific EBR depth.

---

## 1. Platform Adoption & Engagement

| Metric | Definition | Insight Value | Data Source |
|---|---|---|---|
| **Active User Ratio** | Active users / Billable users | License utilization; low ratios = training opportunity | PostgreSQL MCP, Admin Console |
| **Login Frequency** | Logins / Active user (monthly) | Engagement depth; benchmarkable by segment | Mixpanel, Admin Console |
| **Feature Adoption Rate** | Features used / Features enabled | Unused capabilities = expansion conversation | Mixpanel, PostgreSQL MCP |
| **Mobile vs. Web Split** | eCat orders / Total orders | Sales team mobility patterns | Mixpanel (`Submit Order` by device) |
| **User Growth Trend** | MoM user count change | Leading indicator of account health | PostgreSQL MCP, Admin Console |
| **Products with Images %** | Products with images / Total products | Visual readiness; affects rep effectiveness | PostgreSQL MCP |
| **Monthly Active Users (MAU)** | Distinct users with any event in calendar month | Core engagement metric; trendable MoM | Mixpanel |
| **Daily Active Users (DAU)** | Distinct users with any event in calendar day | Granular engagement pulse | Mixpanel |
| **MAU Trend (6-month)** | MAU plotted month-over-month | Engagement trajectory for QBR slides | Mixpanel |
| **User Utilization Rate** | Active users / Licensed users (per entity) | More precise than Active User Ratio for multi-entity accounts | PostgreSQL MCP, Admin Console |

### Licensed Users — Filter
- Table: `org_users` JOIN `users` JOIN `user_types`
- Filter: `user_types.allow_ipad_logins = true`
- Exclude: `users.disabled = true`
- Exclude user type names: Employee%, Customer%, Touchscreen%, IMAP%,
  eCat%, z-SuperCat, Automation, Meridian
- Internal emails: exclude kylor@, brent@, cwiebe@ supercat.io

### Active Users
- Source: BigQuery `mixpanel__events` where `event_name = 'selected_org'`
- Period: TTM window
- Note: active > licensed is possible (BQ catches users not in PG filter)

---

## 2. Sales Velocity & Order Performance

### Revenue — Source of Truth
- Table: `orders`
- Field: `SUM(order_items[].extended_price)` via jsonb_array_elements
- Deduplication: order number suffix logic (keep highest suffix per base number)
- Date field: `submit_date` (not `created_at` or `order_date`)
- Filters: `is_submitted = true`, `is_marked_deleted = false`
- Validation: matches Admin Console CSV within 0.3%

### Rep Attribution — Source Hierarchy
1. Primary: `orders.rep_first_name + orders.rep_last_name` (Postgres)
2. Fallback: BigQuery `order_submitted` event username
3. Validation gate: if BQ order_submitted < 50% of Postgres order count,
   use Postgres for all rep slides

| Metric | Definition | Insight Value | Data Source |
|---|---|---|---|
| **Average Order Value (AOV)** | Order total / Order count | Benchmarkable by industry segment | Admin Orders Report |
| **Orders per Active User** | Order count / Active users | Rep productivity proxy | Mixpanel, Admin Console |
| **Customer Activation Rate** | Customers ordering / Total customers | Buyer engagement; expansion signal when low | Admin Console, PostgreSQL MCP |
| **Digital Self-Service Rate** | eOL orders / Total orders | Channel maturity indicator | Mixpanel, Admin Console |
| **Order Frequency** | Orders / Ordering customers | Purchase velocity | Admin Orders Report |
| **Revenue per Active User** | Order total / Active users | Productivity benchmark | Admin Orders Report |
| **Items per Order** | Total items ordered / Total orders | Order complexity indicator (ASI: 88.1, MPC: 96.3) | PostgreSQL (`cart_items` joined to `orders`) |
| **Daily Order Average** | Orders / Business days in period | Smoothed velocity metric | Admin Orders Report |
| **Daily Revenue Average** | Revenue / Business days in period | Run rate indicator | Admin Orders Report |
| **YTD Annualized Run Rate** | (YTD Revenue / Days elapsed) × 365 | Projection vs LTM; shows growth trajectory | Admin Orders Report |
| **Monthly Revenue Breakdown** | Revenue by calendar month | Seasonality detection and month-over-month pacing | Admin Orders Report |
| **LTM Order Revenue** | Trailing 12-month order total | Baseline for YoY comparison | Admin Orders Report |
| **Order Type Breakdown** | Orders by type: Confirmed, Quote, HFC (Hold for Confirmation) | Order composition; Quote-to-Confirmed conversion rate and HFC resolution rate are process maturity indicators | Admin Orders Report |
| **Quote-to-Order Conversion Rate** | Confirmed orders originating from Quotes / Total Quotes | Sales process efficiency; low conversion = pricing friction or buyer hesitation | Admin Orders Report |
| **HFC Rate** | HFC orders / Total orders | Fulfillment process indicator; high HFC rate may signal inventory or credit issues | Admin Orders Report |
| **Order Origin Mix** | Orders by origin (Regular, Market/Event name) | Trade show and market event attribution; measures order volume tied to specific events (e.g., Dallas Market, High Point) | Admin Orders Report |
| **Market-Attributed Revenue** | Order value from event-originated orders | ROI indicator for trade show participation; trendable across events | Admin Orders Report |

---

## 2a. Territory Performance

| Metric | Definition | Insight Value | Data Source |
|---|---|---|---|
| **Territory Order Volume** | Orders per territory | Territory-level sales activity; identifies active vs. dormant territories | Admin Orders Report |
| **Territory Revenue** | Total order value per territory | Revenue distribution across sales org; highlights concentration and gaps | Admin Orders Report |
| **Territory AOV** | Order total / Orders per territory | Territory-level pricing patterns; significant variance may indicate customer mix or discounting differences | Admin Orders Report |
| **Territory Customer Count** | Unique ordering customers per territory | Customer penetration by territory; low count relative to assigned accounts = activation opportunity | Admin Orders Report |
| **Territory Rep Activity** | Rep engagement events by territory (from CLM cross-referenced with territory assignment) | Behavioral patterns by territory; identifies territories where reps are active but not converting, or converting without deep engagement | Admin Console CLM, Admin Orders Report |
| **Territory Customer Concentration** | Top customer's % of territory revenue | Revenue risk by territory; single-customer dependency within a territory | Admin Orders Report |

---

## 3. Channel Performance (iPad vs. Web)

| Metric | Definition | Insight Value | Data Source |
|---|---|---|---|
| **Channel Revenue Share** | iPad revenue / Total revenue | iPad dominance = eCat Online opportunity | Mixpanel (channel detection via event source) |
| **Channel AOV Comparison** | iPad AOV vs. Web AOV | Abaline: iPad $3,985 vs Web $1,361 (3x) | Mixpanel + Admin Orders Report |
| **Channel Items per Order** | Items/order by channel | Channel-specific ordering behavior | Mixpanel + PostgreSQL (`cart_items`) |
| **Channel Adoption Trend** | MoM % of orders by channel | Is eCat Online growing or stagnant? | Mixpanel (`Submit Order` + device context) |
| **Channel User Split** | iPad users vs. Web-only users | Which reps are multi-channel? | Mixpanel |
| **eCat Online Activation** | Customers with eOL logins / Total customers | Buyer self-service readiness | Admin Console, PostgreSQL MCP |

---

## 4. Feature Utilization

| Metric | Definition | Insight Value | Data Source |
|---|---|---|---|
| **PDF Catalog Creation Rate** | PDF catalogs created / Active users | Presentation-heavy sales culture | Mixpanel |
| **SmartPicks Usage** | SmartPicks views / Total searches | AI recommendation adoption | Mixpanel |
| **Kit/Configured Item Orders** | Configured orders / Total orders | Product complexity utilization | Mixpanel |
| **Flipbook Engagement** | Flipbook views + orders | Digital catalog adoption | Mixpanel |
| **Resource Library Usage** | Library views / Active users | Training material consumption | Mixpanel |
| **Commitments/Interests Tracking** | Feature usage count | Pipeline visibility adoption | Mixpanel |
| **Customer List Creation** | Lists created / Active users | Personalization feature adoption | Mixpanel |
| **Scan Item Usage** | Camera scans / Active users | Mobile feature utilization | Mixpanel |
| **Email Item Info** | Item emails drafted / Active users | Buyer enablement activity (MPC 13x higher than ASI) | Mixpanel |
| **View Customer Favorites** | Favorites views / Active users | Relationship-selling depth | Mixpanel |
| **View Customer Backorders** | Backorder views / Active users | Fulfillment awareness | Mixpanel |
| **Filter & Sort Usage** | Filter + sort events / Active users | Catalog navigation sophistication | Mixpanel |
| **Order Review Rate** | Order views / Orders submitted | QA behavior — Leo reviews 35% of his orders | Mixpanel |
| **Show Sales in Catalog** | Sales-view events / Active users | Pricing transparency feature adoption | Mixpanel |
| **View Placements** | Placement views / Active users | Showroom/visual merchandising engagement | Mixpanel |
| **Search Collections** | Collection search events / Active users | Collection-based navigation behavior; indicates reps browsing by curated grouping rather than free search | Mixpanel, Admin Console CLM |
| **Customer Product List Creation** | Customer product lists created / Active users | Buyer-specific curation — distinct from personal "My List"; indicates reps building tailored selections for individual customers | Mixpanel, Admin Console CLM |
| **Customer Product List Views** | Customer product list views / Active users | Follow-through on buyer-specific curation; high views relative to creates = reps revisiting tailored selections | Mixpanel, Admin Console CLM |
| **Maybe List Creation** | Maybe lists created / Active users | Consideration-stage behavior; items parked for potential follow-up | Mixpanel, Admin Console CLM |
| **Maybe List Conversion Rate** | Orders from Maybe List / Maybe lists created | Conversion funnel: consideration → order. Measures how effectively "parked" items convert to transactions | Mixpanel, Admin Console CLM |
| **My List Edit Rate** | My List edits / My Lists created | List refinement behavior; high ratio = reps actively curating and maintaining lists vs. one-time creation | Mixpanel, Admin Console CLM |
| **Library Entry Sharing Rate** | (Single + Multiple library emails) / Library views | Buyer enablement action — what share of library access results in content being shared externally | Mixpanel, Admin Console CLM |
| **Library Single Email** | Single library entry emails / Active users | Targeted content sharing — rep sends specific collateral to a buyer | Mixpanel, Admin Console CLM |
| **Library Multi-Email** | Multiple library entry emails / Active users | Bulk content sharing — rep sends multiple resources at once | Mixpanel, Admin Console CLM |
| **PDF Search Usage** | PDF search events / Active users | In-document/catalog content search; distinct from product catalog search — indicates reps searching within generated PDFs or catalog content | Mixpanel, Admin Console CLM |
| **Cross-Product Access (Sales Portal from iPad)** | Sales Portal access events from iPad / Active users | Cross-product engagement — reps accessing Sales Portal dashboards from within the iPad app | Mixpanel, Admin Console CLM |

---

## 5. Sales Activity Ladder

A behavior-to-outcome correlation model. Each level represents increasingly sophisticated platform usage. Assessed per rep and benchmarkable across 7,000+ B2B sales reps in the platform.

| Level | Activity Cluster | Key Events | Correlation to Orders | Assessment Scale |
|---|---|---|---|---|
| **1. Customer Targeting** | Select Customer, Search Customer | `Select Customer`, `Search Customer` | 0.96+ (highest) | Foundation of selling |
| **2. Product Discovery** | Search Products, Filter, Sort, Search Collections | `Search Products`, `Filter Products`, `Change Catalog Sort`, `Search Collections` | High | Catalog engagement |
| **3. Information Sharing** | Email Item Info, PDF Catalogs, Library Sharing | `Email Item Info`, `Create PDF Catalog`, `Email Single Library Entry`, `Email Multiple Library Entries` | Medium | Buyer enablement |
| **4. Personalization** | Lists, Customer Product Lists, Favorites, Backorders | `My Lists`, `Edit My List`, `Share My List`, `Create Customer Product List`, `View Cust. Product List`, `View Cust. Favorites`, `View Cust. Backorders` | Medium | Relationship depth |
| **5. Advanced Features** | SmartPicks, Configured Items, Kits, Maybe List Conversion | `View SmartPicks`, `Order Configured Item`, `Order Kit`, `Create Maybe List`, `Order From Maybe List` | Lower | Power user signals |
| **6. Engagement Depth** | Order Review, Library, Placements, Cross-Product, PDF Search | `View iPad Orders`, `View Library Entry`, `View Placements`, `Access Sales Portal`, `PDF searches` | Variable | Workflow refinement |

**Scoring:** Each rep receives a per-level rating (Excellent / Good / Moderate / Low / Not Used) based on event counts relative to their order volume. Aggregate scores per org show adoption maturity.

**Data source:** Mixpanel events in BigQuery, Admin Console User Feature Report

---

## 6. Rep-Level Performance

| Metric | Definition | Insight Value | Data Source |
|---|---|---|---|
| **Orders per Rep** | Individual rep order volume | Identifies power users and laggards | Mixpanel, Admin Console |
| **Orders per Login** | Orders / Logins (per rep) | Efficiency ratio — Leo: 1.2, Mike S: 2.0 | Mixpanel, Admin Console |
| **Product Searches per Order** | Searches / Orders (per rep) | Discovery efficiency — Leo: 2.2, Almo: 25.8 | Mixpanel |
| **Customer Searches per Order** | Cust. searches / Orders (per rep) | Targeting efficiency | Mixpanel |
| **PDF Catalogs per Order** | PDFs created / Orders (per rep) | Presentation intensity | Mixpanel |
| **User Concentration Risk** | Top rep's % of total orders | Leo = 70% of ASI orders — bus factor risk | Mixpanel, Admin Console |
| **Feature Breadth Score** | Distinct features used per rep | Shallow vs. deep adopter identification | Mixpanel |
| **Rep Activity Ranking** | Composite activity event count | Leaderboard for training prioritization | Mixpanel |
| **Login-to-Order Ratio** | Logins / Orders (per rep) | Inverse of efficiency — high ratio = browsing without buying | Mixpanel |
| **Single-Day Activity Snapshot** | Daily event breakdown per rep | Point-in-time coaching data | Mixpanel |
| **Rep-to-Customer Mapping** | Customers touched per rep (via Select Customer / Search Customer events cross-referenced with orders) | Territory alignment validation; identifies reps whose activity patterns don't match assigned customer base | Mixpanel, Admin Orders Report |
| **Customer Concentration (Order-Level)** | Unique customers per rep / Total assigned customers | Customer penetration by rep; low ratio = rep working a narrow slice of their book | Admin Orders Report, Admin Console |

---

## 7. Time to First Value (TTFV)

| Metric | Definition | Insight Value | Data Source |
|---|---|---|---|
| **TTFV (days)** | Days from deal close date to first value event | Onboarding speed; target <14 days | Mixpanel + HubSpot close dates |
| **TTFV by Event Type** | First add-to-list vs. first email drafted | Which value path activates faster | Mixpanel |
| **Monthly TTFV Average** | Avg TTFV for monthly cohort of new clients | Trending onboarding efficiency | `ttfv/2025_clients_monthly_averages.csv` |
| **Trailing 90-Day TTFV** | Rolling 90-day average | Smoothed trend for QBR slides | `ttfv/2025_clients_trailing_90day_ttfv.csv` |
| **TTFV by Org** | Per-client TTFV | Identifies slow onboarders for intervention | Mixpanel |
| **% Users Reaching Value** | Users with TTFV event / Total non-admin users | Rep activation rate — how many actually do real work | Mixpanel |

### TTFV Definition

TTFV = the earliest date a non-admin sales rep performed either:
1. `item_added_via_magic_button` — added a product to a list
2. `document_email_drafted` or `item_email_drafted` — drafted a product email

Excludes SuperCat internal admin usernames. Calculated per user per organization.

**Data source:** `mixpanel__events` in BigQuery, cross-referenced with `ttfv/2025_clients.csv` for close dates

---

## 8. Multi-Entity / Account Structure Analysis

For accounts with multiple organizations under one parent (e.g., Abaline = ASI + MPC).

| Metric | Definition | Insight Value | Data Source |
|---|---|---|---|
| **Entity Revenue Split** | Revenue per entity / Total combined | ASI: 65% vs MPC: 35% | Admin Orders Report |
| **Cross-Entity Feature Gap** | Features used by Entity A but not B | SmartPicks: ASI uses, MPC = 0 | Mixpanel, Admin Console |
| **Entity AOV Comparison** | AOV per entity | Identifies pricing/catalog differences | Admin Orders Report |
| **Per-Entity User Utilization** | Active / Licensed per entity | ASI: 78%, MPC: 85% | PostgreSQL MCP, Admin Console |
| **Subscription Gap Analysis** | Products enabled per entity vs. full suite | MPC missing Sales Portal ($395/mo) | Stripe, Admin Console |
| **Combined MRR/ARR** | Sum of all entities under parent | Total account value | Stripe, QuickBooks |
| **Entity Parity Score** | Feature/usage overlap between entities | Low parity = training opportunity for lagging entity | Mixpanel |

---

## 9. Data Health & Operational Efficiency

| Metric | Definition | Insight Value | Data Source |
|---|---|---|---|
| **Catalog Size** | Total products | Scale indicator | PostgreSQL MCP |
| **Category/Collection Depth** | Categories + Collections | Taxonomy organization maturity | PostgreSQL MCP |
| **Price Level Count** | Number of price tiers | Pricing sophistication | PostgreSQL MCP |
| **Import Error Rate** | Errors / Total imports (30 days) | Integration health | PostgreSQL MCP |
| **Data Freshness Score** | Days since product/customer/inventory update | Sync health; stale data = risk | PostgreSQL MCP |
| **Inventory Update Frequency** | Updates per week | Real-time data health | PostgreSQL MCP |
| **Options Configured** | Option record count | Product configuration maturity | PostgreSQL MCP |
| **Report Format Count** | Configured report templates | Output flexibility | PostgreSQL MCP |
| **FTP/Integration Status** | Active / Inactive / Error state | Connectivity health | PostgreSQL MCP |
| **Last Sync Timestamp** | Most recent product/customer/inventory import | Stale data risk (>7 days = red flag) | PostgreSQL MCP |
| **Import Success Rate (30d)** | Successful imports / Total imports | Integration reliability | PostgreSQL MCP |
| **Territory Configuration** | Territories configured: count + coverage | Sales org structure completeness; 0 = consultation needed | PostgreSQL MCP |
| **Mobile Site Configuration** | eCat Online setup completeness | Channel readiness | PostgreSQL MCP |
| **Custom Report Formats** | Report templates configured | Output customization maturity | PostgreSQL MCP |
| **eCat Version Currency** | Count of reps on outdated app versions (below minimumEcatVersion threshold) | Hygiene metric; reps on significantly old versions may lack features added in later binaries. Only relevant if minimumEcatVersion enforcement is active or versions are substantially outdated | Admin Console CLM |

---

## 10. Customer Support Health

| Metric | Definition | Insight Value | Data Source |
|---|---|---|---|
| **Ticket Volume** | Open + closed tickets (rolling 90 days) | Customer friction indicator | HelpScout (BigQuery) |
| **Ticket Volume Trend** | QoQ ticket change % | Improving or degrading experience | HelpScout (BigQuery) |
| **Tickets by Product Area** | Tag distribution | Pain point identification | HelpScout (BigQuery) |
| **Time to Resolution** | Avg days ticket open → closed | Support efficiency | HelpScout (BigQuery) |
| **Repeat Issue Rate** | Tickets on same topic / Total | Training opportunity signal | HelpScout (BigQuery) |
| **Ticket Velocity** | Tickets per month | Smoothed friction rate (Abaline: ~1/mo = low friction) | HelpScout (BigQuery) |
| **Tickets by Agent** | Ticket distribution by support agent | Team workload balance | HelpScout (BigQuery) |
| **Feature Request Patterns** | Recurring request themes | Product feedback loop | HelpScout (BigQuery) |
| **Customer Wait Time** | Avg time customer waiting for response | Responsiveness indicator | HelpScout (BigQuery) |

---

## 11. Sales Intelligence (Fathom)

| Metric | Definition | Insight Value | Data Source |
|---|---|---|---|
| **Meeting Volume** | Calls with customer (rolling 90d) | Engagement frequency | `fathom__ai_summaries` |
| **Meeting Duration (avg)** | Avg call length in minutes | Depth of engagement | `fathom__ai_summaries` |
| **Pain Themes** | AI-extracted customer pain points | VoC for QBR narrative | `fathom__sales_meetings_from_fathom_hubspot` |
| **Objection Frequency** | Distinct objections raised across calls | Risk signals | `fathom__sales_meetings_from_fathom_hubspot` |
| **Competitor Mentions** | Competitors named in calls | Competitive pressure | `fathom__sales_meetings_from_fathom_hubspot` |
| **Next Steps Tracking** | Action items extracted per meeting | Follow-through accountability | `fathom__ai_summaries` |
| **MEDDIC Completeness** | MEDDIC fields populated / Total fields | Sales process maturity | `fathom__sales_meetings_from_fathom_hubspot` |
| **Meeting-to-Deal Ratio** | Meetings / Open deals | Engagement intensity per opportunity | Fathom + HubSpot |
| **External vs. Internal Calls** | Calls with external attendees / Total | Customer-facing time allocation | `fathom__ai_summaries` |

### MEDDIC Fields Available

| Field | Description | QBR Use |
|---|---|---|
| Situation | Current state/context | Account narrative |
| Pain | Customer pain points | Challenge identification |
| Impact | Business impact of pain | ROI justification |
| Critical Event | Compelling event/deadline | Urgency assessment |
| Decision Process | How they make decisions | Deal risk assessment |
| Economic Buyer | Who signs the check | Stakeholder mapping |
| Solution Fit | How SuperCat solves it | Value alignment |
| Tech Stack | Customer technology | Integration planning |
| Objections | Concerns raised | Risk mitigation |
| Competitors | Who we compete against | Competitive intelligence |
| Timeline | Expected timeline | Forecasting |

---

## 12. Pipeline & Deal Intelligence (HubSpot)

| Metric | Definition | Insight Value | Data Source |
|---|---|---|---|
| **Pipeline Value by Stage** | Sum of deal amounts per stage | Expansion visibility | `hubspot__deal` |
| **Deal Velocity** | Avg days from create → close | Sales cycle health | `hubspot__deal` |
| **Win Rate** | Closed Won / (Won + Lost) | Conversion effectiveness | `hubspot__deal` |
| **Stalled Deals** | Deals unchanged >30 days | Pipeline hygiene | `hubspot__deal` |
| **Deal-to-Meeting Ratio** | Open deals / Fathom meetings | Engagement-to-pipeline correlation | HubSpot + Fathom |
| **Expansion Deal Count** | Deals tagged as upsell/cross-sell | Growth from existing accounts | `hubspot__deal` |
| **Average Deal Size** | Total pipeline value / Deal count | Expansion sizing | `hubspot__deal` |
| **Closed Won Revenue (period)** | Revenue from won deals in period | New business contribution | `hubspot__deal` |
| **Owner Performance** | Deals by rep/owner | Sales team productivity | `hubspot__deal` + `hubspot__owner` |

---

## 13. Revenue & Account Health

| Metric | Definition | Insight Value | Data Source |
|---|---|---|---|
| **MRR** | Monthly recurring revenue | Account value | Stripe, QuickBooks |
| **ARR** | Annual recurring revenue | Account value (annualized) | Stripe, QuickBooks |
| **MRR by Product Line** | Breakdown: iPad, eCat Online, Sales Portal, Admin Console | Revenue composition | Stripe |
| **Subscription Completeness** | Products enabled / Total product suite | Whitespace for expansion | Stripe, Admin Console |
| **Payment Status** | Current / Overdue | Collections health | Stripe, QuickBooks |
| **Payment Collection Rate** | Amount paid / Amount due | AR health | Stripe, QuickBooks |
| **Invoice Aging** | Days outstanding by bucket | Collections risk | QuickBooks |
| **Revenue Trend** | YoY order total change | Growth trajectory | Admin Orders Report |
| **Seat Utilization** | Billable users / Licensed users | Expansion headroom | PostgreSQL MCP |
| **Expansion Revenue Potential** | Missing products × list price | Quantified upsell (Abaline: $4,740/yr) | Stripe + product catalog |
| **Net Revenue Retention** | Current ARR / Prior period ARR (same accounts) | Growth vs. churn | Stripe, QuickBooks |
| **Revenue per User** | ARR / Active users | Per-seat value | Stripe + Mixpanel |

---

## 14. Expansion Signals

| Signal | Detection Method | Recommended Action | Data Source |
|---|---|---|---|
| **Underutilized Features** | Enabled but <10% peer usage | Feature training/enablement | Mixpanel, PostgreSQL MCP |
| **High AOV + Low Activation** | Above-median AOV, below-median customer ordering % | Buyer enablement program | Admin Console |
| **Single Price Level** | Price levels = 1 | Tiered pricing strategy | PostgreSQL MCP |
| **No eOL Orders** | eOL orders = 0 with eOL enabled | Self-service activation | Mixpanel, PostgreSQL MCP |
| **High PDF + No Flipbook** | PDF usage high, Flipbook = 0 | Digital catalog upsell | Mixpanel |
| **Growing User Count** | MoM users increasing | Seat expansion conversation | PostgreSQL MCP |
| **Stale Inventory Data** | Last update >7 days | Integration enhancement | PostgreSQL MCP |
| **No Portal Usage** | Sales Portal enabled, no logins | Dashboard training | PostgreSQL MCP, Mixpanel |
| **High Support Volume** | Tickets > 2x segment median | CSM intervention / training | HelpScout (BigQuery) |
| **Territory Count = 0** | No territories configured | Sales org structure consultation | PostgreSQL MCP |
| **Subscription Gaps** | Entity missing products siblings have | Cross-sell within account | Stripe |
| **Cross-Entity Feature Gap** | One entity uses feature, sibling doesn't | Training for lagging entity | Mixpanel |
| **User Concentration Risk** | Top rep >50% of orders | Training + adoption broadening | Mixpanel |
| **High TTFV** | TTFV >30 days | Onboarding intervention | Mixpanel |
| **Low % Users Reaching Value** | <50% of reps have TTFV event | Activation program | Mixpanel |
| **Fathom Pain Signals** | Repeated pain themes across calls | Proactive outreach | Fathom (BigQuery) |
| **Stalled Pipeline Deals** | Deals unchanged >30 days | Re-engagement campaign | HubSpot (BigQuery) |
| **iPad-Only + High Volume** | No eCat Online, >100 orders/mo | eCat Online pilot | Mixpanel, PostgreSQL MCP |
| **No SmartPicks Usage** | SmartPicks enabled, 0 events | AI feature training | Mixpanel |
| **Low Activity Ladder Score** | Levels 3-6 unused | Feature adoption workshop | Mixpanel |
| **High Maybe List, Low Conversion** | Maybe Lists created but Order From Maybe List near zero | Workflow training — converting consideration to action | Mixpanel, Admin Console CLM |
| **Library Access Without Sharing** | High View Library Entry, low Email Library Entry | Content sharing enablement — reps consuming but not distributing collateral to buyers | Mixpanel, Admin Console CLM |
| **Customer Product List Gap** | Create Customer Product List = 0 while My List usage is active | Buyer-specific curation training — reps personalizing for themselves but not for individual customers | Mixpanel, Admin Console CLM |
| **Territory Revenue Concentration** | Top territory >40% of total revenue | Territory diversification / rep enablement in underperforming territories | Admin Orders Report |
| **High Quote, Low Conversion** | Quote orders submitted but low Confirmed conversion | Pricing friction or buyer hesitation; may indicate need for pricing strategy review | Admin Orders Report |
| **Dormant Territories** | Territories with zero orders in rolling 30 days | Territory coverage gap; may indicate rep inactivity or customer churn in region | Admin Orders Report |

---

## 15. Industry Segment Benchmarks

| Segment | Key Benchmark Metrics | Active Orgs (examples) |
|---|---|---|
| **Lighting** | AOV, Configured item %, Kit orders, Options utilization | Kichler, Maxim, Visual Comfort, Savoy House, Troy |
| **Furniture** | PDF catalogs, Commitments tracking, Customer activation | Hooker, Century, Rowe, Braxton Culler |
| **Occasional/Accent** | eOL adoption, Customer activation rate | Currey & Company, Jamie Young, Elk Home |
| **Outdoor/Casual** | Seasonal order patterns, Contract vs. retail split | Summer Classics, Ratana |
| **Housewares/Giftware** | Items per order, Search-to-order ratio | Godinger, Home Essentials |

### Benchmarking Dimensions

| Dimension | Segments | Key Comparison Metrics |
|---|---|---|
| **Org Size** | Small (<10 users), Medium (10-50), Large (50+) | AOV, activation rate, feature breadth |
| **Tenure** | New (<6mo), Established (6-24mo), Mature (2yr+) | TTFV, support ticket velocity, feature adoption |
| **Product Suite** | iPad-only, iPad + eCat Online, Full suite | Revenue per user, self-service rate |
| **Integration Maturity** | Manual upload, FTP, API | Data freshness, error rates, import success rate |

**Benchmark universe:** 129 active organizations (per `ttfv/active_orgs.csv`)

---

## 16. Account Scoring — Two-Lens Model

Two independent scores replace the single composite health score. Expansion Readiness and Retention Risk are not inversely correlated — an account can be high on both, low on both, or any combination.

### Quadrant Matrix

|  | **Low Retention Risk** | **High Retention Risk** |
|---|---|---|
| **High Expansion Readiness** | **GROW** — EBR with expansion agenda | **SAVE & GROW** — Fix risk first, then expand |
| **Low Expansion Readiness** | **MAINTAIN** — Light-touch, data-driven touchpoints | **INTERVENE** — Retention conversation, not EBR |

### Score A: Expansion Readiness

Answers: **Should we invest more in this account?**

| Component | Weight | Inputs | Data Source |
|---|---|---|---|
| **Adoption Depth** | 30% | Activity Ladder aggregate, Feature Breadth Score, Subscription Completeness, Active User Ratio | Mixpanel, Stripe, PostgreSQL |
| **Business Impact** | 25% | **Ordering:** order volume trend, AOV, Customer Activation Rate, Self-Service Rate. **Non-ordering:** buyer-facing email events (`Email Item Info`, `item_email_drafted`, `document_email_drafted`), PDF Catalogs, Library Entry sharing, Customer Product List creation, trend on all buyer-facing actions. **Non-ordering + Pushed Data:** all non-ordering inputs PLUS pushed order volume trend, pushed revenue trend, and pushed AOV — weighted at 50% of their ordering-client value (the platform is central to order-to-cash but reps don't use the transactional Submit Order workflow) | Mixpanel, PostgreSQL, Admin Orders Report |
| **Growth Signals** | 25% | User Growth Trend, growing MAU, new territories configured, Expansion Signals triggered (Section 14), Fathom pain themes mapping to unused features, HubSpot expansion deals | Mixpanel, PostgreSQL, Fathom, HubSpot |
| **Relationship Strength** | 20% | Fathom meeting cadence (90d) — **N/A if no data, weight redistributes; absence is not a penalty**, days since last interaction, stakeholder breadth (distinct contacts across Fathom + HelpScout), HelpScout ticket responsiveness, onboarding ticket activity | Fathom (BigQuery), HelpScout (BigQuery) |

**Interpretation:**
- **80–100**: Active expansion target — build the business case, schedule EBR
- **60–79**: Nurture — foundation present, focus on enablement first
- **Below 60**: Not ready — expansion push would feel premature

### Score B: Retention Risk

Answers: **Are we about to lose this account?**

| Component | Weight | Inputs | Data Source |
|---|---|---|---|
| **Engagement Decline** | 30% | MAU trend (3+ months declining), login frequency trend, Active User Ratio drop, user count decrease | Mixpanel, PostgreSQL |
| **Relationship Cooling** | 25% | Fathom: days since last meeting (increasing) — **N/A if no data, weight redistributes; only a risk signal when meetings were previously happening and stopped**, missed/cancelled meetings, competitor mentions, negative pain themes. HelpScout: ticket pattern change from established cadence (deviation from norm, not absolute silence), unresolved tickets with high wait time, rising ticket volume from mature account, billing/cancellation tags, thread depth (back-and-forth per ticket) | Fathom (BigQuery), HelpScout (BigQuery) |
| **Financial Distress** | 25% | Payment status (overdue), invoice aging (60+ days), MRR contraction, declining order revenue (ordering clients) | Stripe, QuickBooks, PostgreSQL |
| **Operational Deterioration** | 20% | Data freshness declining, import error rate rising, repeated support issues (same-topic tickets), stale inventory (>7 days) | PostgreSQL, HelpScout (BigQuery) |

**Interpretation:**
- **Below 30**: Low risk — monitor normally
- **30–50**: Watch — investigate specific components
- **50–70**: Elevated risk — proactive outreach within 2 weeks
- **Above 70**: Critical risk — immediate intervention required

### Design Notes

- **Use-case profile detection (three profiles):** Determine before scoring. Query Mixpanel for `Submit Order` events and PostgreSQL `orders` table for the last 90 days.
  - **Ordering:** Submit Order events exist in Mixpanel → full transactional scoring.
  - **Non-Ordering:** Zero Submit Order events AND zero orders in PostgreSQL → buyer-facing action scoring only.
  - **Non-Ordering + Pushed Data:** Zero Submit Order events in Mixpanel BUT orders exist in PostgreSQL (ERP-pushed imports) → hybrid scoring. Business Impact uses all non-ordering inputs PLUS pushed order metrics at 50% weight. Import cadence and pushed data volume are first-class signals in both Data Health and Business Impact.
- **Canonical Active User definition:** Active User = distinct Mixpanel usernames with ≥1 event in the measurement period, excluding SuperCat admin/test usernames (see Appendix C). This is the single definition used across all scoring components, all brief sections, and all metrics. PostgreSQL `authenticated_sessions` and HubSpot active user counts may be referenced for context but are NOT the canonical measure. When computing Active User Ratio, the denominator is billable users from HubSpot or PostgreSQL `org_users` (whichever is available), and the numerator is canonical Mixpanel active users.
- **Insufficient data handling:** Components with absent or thin data (<30 days history, no Fathom meetings, no HelpScout tickets) score as "N/A" with weight redistributed to remaining components. New accounts do not auto-flag as at-risk.
- **Weight validation:** All weights are starting assumptions. Validate by running across all 129 accounts, comparing to team intuition, then backtesting against actual churn/expansion events after 6–12 months.
- **Source selection:** PostgreSQL for real-time signals (last login, subscription status, import health). BigQuery for trended analysis (Mixpanel events, HelpScout patterns, Fathom cadence, Stripe payment history).
- **Billing model detection:** Not all accounts have Stripe subscriptions. Some are manual invoice-based. Query Stripe `subscription` first; if zero rows, fall back to Stripe `invoice` for MRR derivation, then QuickBooks `invoice`. Framework components referencing "Stripe subscription" should follow this fallback hierarchy: Stripe subscription → Stripe invoice → QuickBooks invoice → PostgreSQL subscriptions.
- **Admin Console data availability:** Metrics sourced from Admin Console CSV exports (CLM and Orders Report) are NOT available via MCP. Approximately 30 metrics depend on these exports. The prompt requires both CSVs to be uploaded before generating a brief. If not present, the prompt stops and requests them.

---

## 17. QBR Dashboard Summary

### At-a-Glance Metrics (single slide)

| Row | Metric | Source | Format |
|---|---|---|---|
| 1 | MRR / ARR | Stripe, QuickBooks | Currency |
| 2 | Active Users / Licensed Users | PostgreSQL MCP | Ratio + % |
| 3 | Orders (YTD) + AOV | Admin Orders Report | Count + currency |
| 4 | MAU Trend (6-month sparkline) | Mixpanel | Trend line |
| 5 | TTFV (trailing 90-day avg) | Mixpanel | Days |
| 6 | Support Tickets (90d) + Trend | HelpScout | Count + arrow |
| 7 | Expansion Readiness Score | Scoring Model | Score + quadrant |
| 8 | Retention Risk Score | Scoring Model | Score + quadrant |

### QBR Slide Structure

1. **Executive Summary** — Health score, headline metrics, 3 key takeaways
2. **Revenue Performance** — Orders, revenue, AOV, channel split, run rate vs LTM
3. **User Engagement** — MAU trend, active user ratio, login frequency
4. **Feature Adoption** — Activity Ladder summary, top/bottom features, rep leaderboard
5. **TTFV & Onboarding** — New user activation, TTFV trend
6. **Support Health** — Ticket volume, trends, themes
7. **Expansion Opportunities** — Top 2-3 signals with quantified revenue potential
8. **Action Items** — Owner, date, next review

### EBR-Specific Additions (annual/bi-annual)

| Section | Additional Depth |
|---|---|
| **Delivered Value** | Revenue growth attribution, productivity gains (hrs/rep/week), operational savings |
| **Sales Intelligence** | Fathom pain themes, competitor landscape, MEDDIC summary |
| **Pipeline Review** | HubSpot deal stages, velocity, stalled deals |
| **Rep Performance** | Top performer analysis, concentration risk, training recommendations |
| **Multi-Entity Analysis** | Entity comparison, feature gaps, subscription parity |
| **Future Goals** | Updated success plan with KPIs, expansion business cases |

---

## Appendix A: Data Source Inventory

| System | BigQuery Tables | Sync Frequency | Primary Use |
|---|---|---|---|
| **HelpScout** | `helpscout__conversation`, `helpscout__conversation_threads`, `helpscout__help_scout_tickets`, `helpscout__customer`, `helpscout__tag`, `helpscout__user` | Daily | Support tickets, resolution times, themes |
| **Fathom** | `fathom__ai_summaries`, `fathom__call_transcripts`, `fathom__sales_meetings_from_fathom_hubspot` | Daily | Meeting intelligence, MEDDIC, VoC |
| **HubSpot** | `hubspot__company`, `hubspot__contact`, `hubspot__deal`, `hubspot__owner`, `hubspot__engagement` | Daily | CRM, pipeline, deal velocity |
| **Mixpanel** | `mixpanel__events` | Daily | Product analytics, feature usage, MAU, TTFV |
| **Stripe** | `stripe__invoice`, `stripe__customer`, `stripe__subscription` | Daily | Billing, MRR/ARR, payment status |
| **QuickBooks** | `quickbooks__invoice`, `quickbooks__payment`, `quickbooks__client_revenue_insights` | Daily/Weekly | Accounting, revenue insights, invoice aging |
| **PostgreSQL** | Via MCP (`supercat-postgres-vpn`) | Real-time | Org config, product/customer/user counts, import events, territories |
| **Admin Console** | CSV exports (Feature Usage / CLM, Orders Report) | On-demand | Per-org/per-user feature and order reports; CLM provides granular per-rep activity counts; Orders Report provides order type, origin, territory, and customer-level detail |

---

## Appendix B: Key Mixpanel Events for Feature Tracking

| Event Name | Activity Ladder Level | Description |
|---|---|---|
| `Submit Order` | — | Order submitted (iPad or Web) |
| `Select Customer` | 1 | Customer selected from list |
| `Search Customer` | 1 | Customer search performed |
| `Search Products` | 2 | Product catalog search |
| `Filter Products` | 2 | Catalog filter applied |
| `Change Catalog Sort` | 2 | Catalog sort changed |
| `Email Item Info` | 3 | Product info emailed to buyer |
| `Create PDF Catalog` | 3 | PDF catalog generated |
| `View Cust. Favorites` | 4 | Customer favorites viewed |
| `View Cust. Backorders` | 4 | Customer backorders viewed |
| `My Lists` | 4 | Personal lists viewed |
| `Share My List` | 4 | List shared with colleague/buyer |
| `View SmartPicks` | 5 | AI recommendations viewed |
| `Order Configured Item` | 5 | Configured product ordered |
| `Order Kit` | 5 | Kit/bundle ordered |
| `View iPad Orders` | 6 | Past orders reviewed |
| `View Library Entry` | 6 | Resource library accessed |
| `View Placements` | 6 | Placement/showroom view |
| `Access Sales Portal` | 6 | Sales Portal accessed from iPad app (cross-product) |
| `PDF searches` | 6 | Search within PDF/catalog content |
| `Search Collections` | 2 | Collection-based catalog navigation |
| `Create Customer Product List` | 4 | Buyer-specific product list created |
| `View Cust. Product List` | 4 | Buyer-specific product list viewed |
| `Create Maybe List` | 5 | Consideration-stage list created |
| `Order From Maybe List` | 5 | Order placed from Maybe List (conversion event) |
| `Edit My List` | 4 | Personal list refined/updated |
| `Email Single Library Entry` | 3 | Single collateral item emailed to buyer |
| `Email Multiple Library Entries` | 3 | Multiple collateral items emailed to buyer |
| `item_added_via_magic_button` | TTFV | Product added to list (TTFV trigger) |
| `document_email_drafted` | TTFV | Document email drafted (TTFV trigger) |
| `item_email_drafted` | TTFV | Item email drafted (TTFV trigger) |

### Event Name Mapping — Legacy ↔ Modern SDK

Orgs on the modern SDK use snake_case event names. The Activity Ladder and all Mixpanel queries must account for both conventions. **When querying Mixpanel, try both names.** If legacy names return zero rows, fall back to modern names.

| Framework Name (Legacy) | Modern SDK Name (snake_case) | Activity Ladder Level | Notes |
|---|---|---|---|
| `Submit Order` | `submit_order` | — | May not exist for non-ordering clients |
| `Select Customer` | `customer_selection` | 1 | — |
| `Search Customer` | `customer_search` | 1 | — |
| `Search Products` | `product_search` | 2 | — |
| `Filter Products` | `filter_button_pressed` | 2 | — |
| `Change Catalog Sort` | `product_sort_changed` | 2 | — |
| `Search Collections` | `collection_search` | 2 | — |
| `Email Item Info` | `item_email_drafted` | 3 | Also a TTFV event |
| `Create PDF Catalog` | `pdf_catalog_generated` | 3 | — |
| `Email Single Library Entry` | `document_email_drafted` | 3 | Also a TTFV event |
| `Email Multiple Library Entries` | *(not found as distinct event)* | 3 | May be collapsed into `document_email_drafted` |
| `View Cust. Favorites` | `view_favorites` | 4 | — |
| `View Cust. Backorders` | *(not found)* | 4 | May not exist on modern SDK |
| `My Lists` | `view_stack` | 4 | — |
| `Edit My List` | `edit_stack` | 4 | — |
| `Share My List` | *(not found)* | 4 | May not exist on modern SDK |
| `Create Customer Product List` | `create_stack` | 4 | Overloaded — same event may cover personal + customer lists |
| `View Cust. Product List` | *(not found as distinct event)* | 4 | May be collapsed into `view_stack` |
| `View SmartPicks` | `view_customer_smart_picks` | 5 | — |
| `Order Configured Item` | *(not found)* | 5 | — |
| `Order Kit` | *(not found)* | 5 | — |
| `Create Maybe List` | *(not found as distinct event)* | 5 | May be captured differently |
| `Order From Maybe List` | `add_to_order_from_maybe_list` | 5 | — |
| `View iPad Orders` | `view_customer_orders` | 6 | — |
| `View Library Entry` | `view_document` | 6 | — |
| `View Placements` | `view_customer_placements` | 6 | — |
| `Access Sales Portal` | `view_portal` | 6 | Cross-product |
| `PDF searches` | *(not found)* | 6 | May not exist on modern SDK |
| `item_added_via_magic_button` | `item_added_via_magic_button` | TTFV | Same in both conventions |
| `Login` / `login` | `selected_org` | — | Login proxy: fires when user selects org post-auth. Use as login frequency proxy when no `login` event exists. |

**Query protocol:** For each Mixpanel query, first run a top-events check (`SELECT DISTINCT event_name FROM mixpanel__events WHERE [org filter] LIMIT 50`) to determine which naming convention the org uses. Then apply the correct names for all subsequent queries. Do not assume one convention.

***(not found)* entries:** These events may not exist on the modern SDK, may be named differently than expected, or may be collapsed into other events. When encountered, log as a data gap in Generation Notes rather than scoring as zero usage.

---

## Appendix C: TTFV Excluded Usernames

SuperCat internal admin/test users excluded from TTFV and per-org engagement calculations:

```
swt, kjael, cwiebe, angie, kylor_johnson, mcp-admin, brentsanders,
chuck-admin, sarahm, jthrasher, jlowe1, support, jonv, chuck-user,
brucew, badkins, ognezdyonova, kyla, mridge, wale
```

---

## Appendix D: Active Organization Universe

129 active organizations available for benchmarking (source: `ttfv/active_orgs.csv`). Segments include Lighting, Furniture, Outdoor/Casual, Housewares/Giftware, and Occasional/Accent.

---

**Version:** 5.1 | **Date:** Feb 26, 2026 | **Author:** Kylor Johnson
**v5.1 changelog:** Fathom absence protocol: Fathom inputs are N/A (weight redistributes) when no data exists — clients are not penalized for being self-sufficient. Fathom cessation (meetings previously happening, then stopped) remains a risk signal. HelpScout silence reframed as pattern deviation, not absolute threshold.
**v5.0 changelog:** Post-Crystorama test run fixes. Added Event Name Mapping table to Appendix B (legacy PascalCase ↔ modern snake_case for all 30 Mixpanel events + query protocol). Added third use-case profile: Non-Ordering + Pushed Data with hybrid Business Impact scoring (pushed order metrics at 50% weight). Defined canonical Active User metric (Mixpanel distinct users with ≥1 event, excluding admin usernames). Added billing model detection fallback hierarchy (Stripe subscription → Stripe invoice → QuickBooks → PostgreSQL). Added Admin Console data availability note. Added `selected_org` as login proxy event.
**v4.0 changelog:** Replaced single Composite Health Score (Section 16) with Two-Lens Account Scoring Model: Expansion Readiness Score + Retention Risk Score with quadrant matrix (Grow / Save & Grow / Maintain / Intervene). Added non-ordering client business impact inputs (email drafted events, PDF catalogs, library sharing, customer product lists). Moved HelpScout support signals from operational component to Relationship Health/Cooling. Added financial distress component (Stripe/QuickBooks). Added insufficient data handling and weight validation strategy. Added Cursor/MCP architecture context for promptable execution.
**v3.0 changelog:** Added Search Collections, Customer Product Lists, Maybe List conversion funnel, My List editing, Library Entry sharing (single/multi), PDF Search, Cross-Product Access (Sales Portal from iPad), Order Type breakdown (Confirmed/Quote/HFC), Order Origin (market attribution), Territory Performance section (2a), Rep-to-Customer Mapping, Customer Concentration, eCat Version Currency, and 7 new Expansion Signals. Updated Activity Ladder levels 2-6 with expanded event coverage. Updated Appendix A (Admin Console CLM/Orders detail) and Appendix B (12 new events).
