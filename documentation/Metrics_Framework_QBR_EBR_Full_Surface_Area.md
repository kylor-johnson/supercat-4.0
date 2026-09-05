# Metrics Framework for Executive Insights, QBRs & Expansion

**Full Surface Area Reference** | v2.0 — Feb 2026

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

---

## 2. Sales Velocity & Order Performance

| Metric | Definition | Insight Value | Data Source |
|---|---|---|---|
| **Average Order Value (AOV)** | Order total / Order count | Benchmarkable by industry segment | Admin Sales Summary |
| **Orders per Active User** | Order count / Active users | Rep productivity proxy | Mixpanel, Admin Console |
| **Customer Activation Rate** | Customers ordering / Total customers | Buyer engagement; expansion signal when low | Admin Console, PostgreSQL MCP |
| **Digital Self-Service Rate** | eOL orders / Total orders | Channel maturity indicator | Mixpanel, Admin Console |
| **Order Frequency** | Orders / Ordering customers | Purchase velocity | Admin Sales Summary |
| **Revenue per Active User** | Order total / Active users | Productivity benchmark | Admin Sales Summary |
| **Items per Order** | Total items ordered / Total orders | Order complexity indicator (ASI: 88.1, MPC: 96.3) | Admin Sales Summary |
| **Daily Order Average** | Orders / Business days in period | Smoothed velocity metric | Admin Sales Summary |
| **Daily Revenue Average** | Revenue / Business days in period | Run rate indicator | Admin Sales Summary |
| **YTD Annualized Run Rate** | (YTD Revenue / Days elapsed) × 365 | Projection vs LTM; shows growth trajectory | Admin Sales Summary |
| **Monthly Revenue Breakdown** | Revenue by calendar month | Seasonality detection and month-over-month pacing | Admin Sales Summary |
| **LTM Order Revenue** | Trailing 12-month order total | Baseline for YoY comparison | Admin Sales Summary |

---

## 3. Channel Performance (iPad vs. Web)

| Metric | Definition | Insight Value | Data Source |
|---|---|---|---|
| **Channel Revenue Share** | iPad revenue / Total revenue | iPad dominance = eCat Online opportunity | Admin Sales Summary, Mixpanel |
| **Channel AOV Comparison** | iPad AOV vs. Web AOV | Abaline: iPad $3,985 vs Web $1,361 (3x) | Admin Sales Summary |
| **Channel Items per Order** | Items/order by channel | Channel-specific ordering behavior | Admin Sales Summary |
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

---

## 5. Sales Activity Ladder

A behavior-to-outcome correlation model. Each level represents increasingly sophisticated platform usage. Assessed per rep and benchmarkable across 7,000+ B2B sales reps in the platform.

| Level | Activity Cluster | Key Events | Correlation to Orders | Assessment Scale |
|---|---|---|---|---|
| **1. Customer Targeting** | Select Customer, Search Customer | `Select Customer`, `Search Customer` | 0.96+ (highest) | Foundation of selling |
| **2. Product Discovery** | Search Products, Filter, Sort | `Search Products`, `Filter Products`, `Change Catalog Sort` | High | Catalog engagement |
| **3. Information Sharing** | Email Item Info, PDF Catalogs | `Email Item Info`, `Create PDF Catalog` | Medium | Buyer enablement |
| **4. Personalization** | Lists, Favorites, Backorders | `My Lists`, `Share My List`, `View Cust. Favorites`, `View Cust. Backorders` | Medium | Relationship depth |
| **5. Advanced Features** | SmartPicks, Configured Items, Kits | `View SmartPicks`, `Order Configured Item`, `Order Kit` | Lower | Power user signals |
| **6. Engagement Depth** | Order Review, Library, Placements | `View iPad Orders`, `View Library Entry`, `View Placements` | Variable | Workflow refinement |

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
| **Entity Revenue Split** | Revenue per entity / Total combined | ASI: 65% vs MPC: 35% | Admin Sales Summary |
| **Cross-Entity Feature Gap** | Features used by Entity A but not B | SmartPicks: ASI uses, MPC = 0 | Mixpanel, Admin Console |
| **Entity AOV Comparison** | AOV per entity | Identifies pricing/catalog differences | Admin Sales Summary |
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
| **Revenue Trend** | YoY order total change | Growth trajectory | Admin Sales Summary |
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

## 16. Composite Health Score

| Component | Weight | Calculation | Data Source |
|---|---|---|---|
| **Engagement** | 25% | (Login frequency + Feature adoption) vs. segment median | Mixpanel |
| **Sales Performance** | 25% | (Orders/user + Customer activation) vs. segment median | Admin Console, Mixpanel |
| **Data Health** | 20% | Freshness scores + Import error rate | PostgreSQL MCP |
| **Support Health** | 15% | Ticket volume trend + Resolution time | HelpScout (BigQuery) |
| **Feature Utilization** | 15% | Features used / Features enabled | Mixpanel, PostgreSQL MCP |

**Score Interpretation:**
- **80-100%**: Healthy, expansion-ready
- **60-79%**: Stable, optimization opportunities
- **<60%**: At-risk, requires intervention

---

## 17. QBR Dashboard Summary

### At-a-Glance Metrics (single slide)

| Row | Metric | Source | Format |
|---|---|---|---|
| 1 | MRR / ARR | Stripe, QuickBooks | Currency |
| 2 | Active Users / Licensed Users | PostgreSQL MCP | Ratio + % |
| 3 | Orders (YTD) + AOV | Admin Sales Summary | Count + currency |
| 4 | MAU Trend (6-month sparkline) | Mixpanel | Trend line |
| 5 | TTFV (trailing 90-day avg) | Mixpanel | Days |
| 6 | Support Tickets (90d) + Trend | HelpScout | Count + arrow |
| 7 | Health Score | Composite | % + color |
| 8 | Top Expansion Signal | Expansion Signals table | Text |

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
| **Admin Console** | CSV exports (Feature Usage, Sales Summary, Monthly Usage) | On-demand | Per-org/per-user feature and order reports |

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
| `item_added_via_magic_button` | TTFV | Product added to list (TTFV trigger) |
| `document_email_drafted` | TTFV | Document email drafted (TTFV trigger) |
| `item_email_drafted` | TTFV | Item email drafted (TTFV trigger) |

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

**Version:** 2.0 | **Date:** Feb 25, 2026 | **Author:** Kylor Johnson
