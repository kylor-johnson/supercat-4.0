# Client Perspective Content Review — 5 Intelligence Reports

**Reviewed**: 2026-06-16
**Reports**: CCI (Currey & Company), UFI (Universal Furniture), HFG (Hubbardton Forge), RW (RENWIL), BCF (Braxton Culler)

---

## A. First Impressions (One Paragraph Per Report)

**CCI (Currey & Company)** — This report hits hard immediately. The executive summary leads with "$2.2M at risk from 15 decelerating accounts" and "top sellers out of stock while demand accelerates." Within 30 seconds of scrolling, I'm looking at named accounts (Lightopia, Pottery Barn) with specific dollar values at risk and specific remediation timeframes. The 9.8% capture rate against $87M total business is the kind of stat that makes a VP of Sales sit forward. This is the closest thing to a private intelligence briefing in the batch — it feels like someone spent a week studying my business and came back with findings I need to act on today.

**UFI (Universal Furniture)** — Strong but slightly colder than CCI. The data is richer (Clicky portal analytics, commitment reports), and the commerce section with its capture rate story ($13.4M eCat against $137.9M total business) is compelling. But with 17 reps versus CCI's 37, the sales team section feels thinner — the behavioral patterns are less dramatic because the population is smaller. The portal section adds interesting texture but doesn't create urgency. Good report for a relationship conversation, not quite the "holy shit" document.

**HFG (Hubbardton Forge)** — The standout is the 40% capture rate ($16.8M eCat vs $42.2M total business). That's genuinely impressive and the report frames it well. But the inventory section is absent (no inventory data), which means one of the most actionable subsections — top sellers out of stock — is missing entirely. The portal section shows 10 visitors/day with 5:35 sessions, which is well-narrated but doesn't create a phone-call moment. The sales section with 17 reps is detailed enough to be useful. Solid B+ report — useful but not explosive.

**RW (RENWIL)** — This is the data-poor test case, and it shows. No ERP data means no capture rate, no total business context, no pricing shift detection, no decelerating accounts measured against all-channel velocity. What's left is still surprisingly compelling: 47 reps, $10.6M eCat GMV, 8,667 orders. The commerce section works even without the total-business comparison because RENWIL's eCat volume is strong on its own terms. But the report feels like it's leaving a massive amount on the table — you can feel the gap where the "compare to total business" story should be. The data-poverty creates a natural upsell moment, but it's currently too implicit.

**BCF (Braxton Culler)** — The most interesting behavioral data in the batch. With B2B Cart active, there's a genuinely different platform usage pattern to analyze. The VM-45 capture rate is suppressed (ERP GMV < eCat GMV, which means the ERP sync isn't comprehensive), creating an odd situation where the report can't tell the full commerce story. The sales team section with 19 reps including 4 admin/showroom users in the leaderboard is a known issue — it slightly undermines trust if a VP sees "Matt Sorensen" as a top rep and knows that's an admin. The coaching opportunities and archetype analysis remain strong.

---

## B. "Holy Shit" Moments

1. **CCI §3 — Dormant High-Value Accounts with Names and Dollars**
   > "Furnitureland South — NC — Last eCat Order Feb 20, 2026 — 11 historical orders — $111,032"
   
   This works because it's not "you have 47 dormant accounts." It's a specific company name, a specific dollar figure, a specific last-order date. A VP sees this and thinks "why the hell hasn't someone called Furnitureland South?" This is the single most phone-call-generating pattern across all 5 reports.

2. **CCI §3 — Deceleration Alert with Revenue at Risk**
   > "15 accounts show order frequency stretching beyond 1.5× their historical average. Combined annual value at risk: $2.2M."
   
   Followed by named accounts (Lightopia $362K, Pottery Barn $350K) with specific deceleration ratios. This is intelligence you cannot get from your ERP unless you build the query yourself. The framing as "at risk" rather than "declining" is psychologically precise.

3. **CCI §5 — eCat Capture Rate at 9.8% with Headroom Framing**
   > "Even a modest increase in capture — from 9.8% to 15% — would represent approximately $4.5M in additional platform-attributed revenue annually."
   
   This is the money slide. Not "you're at 9.8%" (so what?) but "here's what the gap is worth in dollars." This justifies the entire platform relationship in one sentence.

4. **CCI §4 — Top Sellers Out of Stock with Named Products**
   > "Nottaway Grande Bronze Chandelier (9000-1130) — All-Time Sales: $872,209 — Next Receipt: Jul 16, 2026"
   
   A VP of Operations sees their #1 product sitting at zero stock with $872K in historical sales and a restock date that's a month out. That's not a data point — it's a fire drill. Even better: one product has "No date scheduled" in red. Somebody's getting an email.

5. **CCI §3 — New Decision-Maker Detection**
   > "The Treasure Chest added a new contact who placed $175,944 in their first engagement."
   
   This is uniquely SuperCat intelligence — no CRM or ERP surfaces "a new buyer just placed $175K through your platform and your rep doesn't know them yet." The framing as an opportunity (not just a data point) makes it actionable.

6. **CCI §2 — Presentation-to-Order Conversion Spread**
   > "Your most efficient closer converts at 26.8% with just 142 targeted presentations — fewer demos, better outcomes. The 50× conversion spread across the team reveals fundamentally different selling approaches."
   
   This isn't available from any other tool. Only SuperCat has the behavioral data to show that Stacey converts at 26.8% while Vivi converts at 0.5% — and can correlate it with revenue outcomes. A sales manager reads this and immediately has a coaching conversation to have.

7. **CCI §5 — Pricing Shift Detection**
   > "11 accounts show declining average unit prices quarter-over-quarter — combined current-quarter business: $679K."
   
   Named accounts with specific percentage declines (Designer Furniture Galleries down 55.5%). This surfaces competitive pressure or product substitution that would otherwise be invisible until quarterly revenue review. Early warning with enough specificity to act.

8. **CCI §3 — Geographic Revenue Growth with Customer Net-Adds**
   > "Virginia grew 102% quarter-over-quarter ($361K→$730K) with 57 net new customers."
   
   This isn't just "sales grew in Virginia." It's "your team is actively winning market share in Virginia right now, and here's the proof." A VP reads this and wants to know who the rep in Virginia is and what they're doing differently.

---

## C. "Why Is This Here?" List

1. **§8 Data Pipeline Health — Monthly Import Counts**
   - *Currently says*: "~425/mo average imports, 2,795 total imports trailing 7 months"
   - *Why it doesn't land*: No client cares about import counts. This is internal plumbing. The pipeline is either working or it isn't — expressing it as a count of imports per month is meaningless to a VP.
   - *Fix*: Cut to a one-line pass/fail: "Your data pipeline is healthy — core entities update daily." The detailed import table can go in an appendix or be omitted entirely.

2. **§8 Smart Stack Performance — Stack Names and Creation Dates**
   - *Currently says*: Table of 5 stacks with created/updated dates, count of published vs unpublished
   - *Why it doesn't land*: "You have 4 published Smart Stacks" tells a client nothing. They know what Smart Stacks they have — they created them. The dates are irrelevant.
   - *Fix*: Replace with *engagement* data — "Your 'NEW Spring 2026' stack was viewed X times and generated Y orders in its first month" would actually justify the section's existence. Without that data, cut the subsection.

3. **§6 Portal — Daily Visitor Counts (HFG: ~10/day)**
   - *Currently says*: "~11 avg daily visitors, 11,048 pageviews over 7 months, 5:35 avg session"
   - *Why it doesn't land*: For a B2B manufacturer, "10 visitors a day" sounds pathetic. The report tries to reframe it as "small but engaged" but a COO reading this thinks "why am I paying for a portal that gets 10 visitors a day?" The session duration is genuinely interesting but gets lost next to the embarrassing traffic number.
   - *Fix*: Lead with the engagement depth story, not the volume story. Frame as "Your portal visitors spend 5:35 per session — 3× the average for B2B product portals. This signals research-intent buying behavior, not casual browsing." Bury the daily count. Better: connect portal visitors to downstream orders ("X portal visitors placed orders within 7 days of their last session").

4. **§2 Selling vs Admin Time — Rep-Level Allocation Table**
   - *Currently says*: Table showing that reps spend 74–89% of platform time on selling
   - *Why it doesn't land*: The range is too tight (74–89%) to create meaningful differentiation. Unlike the 50× conversion rate spread, this doesn't surface a coaching opportunity — it says "your team is already using the platform correctly." That's validating but not actionable.
   - *Fix*: Either find a wider spread that creates a real coaching story or cut it. If the spread were 40% to 89%, it would be explosive. At 74–89%, it's "that's nice."

5. **§5 Order Type & Workflow — Distribution Table (RW)**
   - *Currently says*: "97.2% confirmed, 2.2% quotes, 0.4% HFC"
   - *Why it doesn't land*: "Your team places orders and most of them are confirmed" is not an insight. Every client knows their team places confirmed orders. The quote premium (4× AOV) is genuinely interesting but gets buried in a table that mostly says "normal ordering pattern."
   - *Fix*: Lead with the quote insight only: "Your quote orders average 4× the standard order value — $4,788 vs $1,222. Increasing quote-to-confirmed conversion is your highest-leverage volume opportunity." Kill the workflow distribution table.

6. **§3 New Buyer Acquisition — Monthly Count Table (CCI)**
   - *Currently says*: Monthly list showing 53–90 new iPad buyers per month
   - *Why it doesn't land*: "You acquired 70 new buyers per month" is useful context but isn't surprising or actionable. It's background, not foreground. The client can't do anything with this except feel good.
   - *Fix*: Keep as a supporting stat (one line in the section intro) but remove the month-by-month table. The space is better used for the next insight in the section.

7. **§3 Wallet Share Estimation — Below-Peer Accounts (CCI)**
   - *Currently says*: 20 accounts spending less than "peer group average" with a $381K gap
   - *Why it doesn't land*: The methodology is too visible and too questionable. All the accounts cluster at almost exactly $10,400–$10,530 in spending with a peer average of exactly $29,506. This looks like a data artifact (possibly a bin boundary) rather than genuine insight. A sophisticated client will see through this immediately.
   - *Fix*: Rethink the methodology. Show accounts with a demonstrated spending capacity (based on historical peak) that have contracted, rather than comparing to a synthetic "peer average." Or: show accounts where total-business spend is high but eCat share is low — the data exists via portal_orders.

---

## D. The Missing Killer Insights

### 1. "Your Biggest Customers Don't Use eCat At All"
**Example sentence**: "Your top 10 accounts by total business volume ($14.2M combined annual revenue) generate only $380K through eCat — a 2.7% platform share. Six of them have never placed an eCat order."

**Data**: `portal_orders` (total business) joined to `orders` (eCat) by customer, ranked by total-business GMV. Filter for accounts with high total-business but zero/minimal eCat.

**Why it's explosive**: This is the most powerful upsell narrative possible — "your most important customers don't know your platform exists." A VP sees this and immediately asks their team "why isn't [biggest customer] on eCat?"

**Section**: §3 Customers or §5 Commerce

---

### 2. "Rep-Level Capture Rate: Who's Converting Total Business to eCat?"
**Example sentence**: "Stacie Baker captures 31% of her territory's total business through eCat ($765K of $2.5M). Sandy Glosson captures 4% ($434K of $10.8M). The gap isn't effort — it's workflow."

**Data**: `orders` (rep-attributed eCat GMV) vs `portal_orders` (rep-attributed total-business GMV). Requires `PORTAL_REP_DATA_PRESENT = true`.

**Why it's explosive**: Naming reps with their capture rate creates an instant competitive dynamic. Sales managers will use this in one-on-ones. "Why is your capture rate 4% when Stacie's is 31%?" This is the question that drives adoption.

**Section**: §2 Sales Team (or bridge between §2 and §5)

---

### 3. "Products Being Browsed But Never Ordered"
**Example sentence**: "Your 'Carlisle Chandelier' was searched 847 times in the last 90 days but generated zero orders. It's the 3rd most-browsed product with no conversion — suggesting a pricing, availability, or configuration barrier."

**Data**: Mixpanel product discovery events (product_search, view_product_detail) cross-referenced with `orders` at the product level. Surface products with high behavioral interest but zero or near-zero orders.

**Why it's explosive**: This identifies invisible demand barriers. The client knows what sells — they don't know what *almost* sells. A merchandising team would kill for this data.

**Section**: §4 Product

---

### 4. "Customer-Level eCat Penetration Rate (ERP Customers vs eCat Customers)"
**Example sentence**: "You have 7,919 accounts in your customer file. Only 1,710 (21.6%) placed an eCat order in the trailing 12 months. Of your 643 Florida accounts, 219 are eCat-active (34%). Of your 315 California accounts, only 67 are active (21%). California is your biggest penetration gap by addressable value."

**Data**: `customers` table (all ERP accounts) vs `orders` (eCat ordering activity). Group by state for geographic penetration.

**Why it's explosive**: CCI already hints at this (§3 shows 38,950 total accounts, 1,710 active) but doesn't frame it as a penetration problem with geographic targeting. The geographic lens makes it actionable: "Go win California."

**Section**: §3 Customers

---

### 5. "Revenue You're Losing to Order Timing"
**Example sentence**: "23 orders totaling $187K were placed on Sunday evenings when your warehouse doesn't process until Monday. If these customers could self-serve via your online catalog, they'd get same-day processing at no additional rep cost."

**Data**: `orders` by day-of-week and time-of-day, cross-referenced with warehouse processing windows. Only applicable to clients with B2B Cart as an upsell or already active.

**Why it's explosive**: Quantifies the cost of not having 24/7 ordering. Creates a natural B2B Cart upsell with a dollar-value justification.

**Section**: §5 Commerce

---

### 6. "Seasonal Product Demand Forecasting"
**Example sentence**: "Based on trailing-3-year ordering patterns, your chandelier category peaks in October (High Point effect) and March (spring refresh). Last October, you had $278K in chandelier back-orders due to stock-outs. Restocking to 110% of seasonal demand by September 1st would prevent an estimated $200K in lost sales."

**Data**: `orders` by category by month (multi-year), cross-referenced with `inventories` and `sales_data` for historical patterns.

**Why it's explosive**: Nobody else can connect seasonal ordering patterns to real-time inventory. This is predictive rather than retrospective — it tells the client what's about to happen and what to do about it.

**Section**: §4 Product

---

### 7. "Your Reps Log In — But These Reps Don't"
**Example sentence**: "14 of your 51 assigned reps have not logged into eCat in the last 90 days. These 14 reps are responsible for 31% of your total business territory ($27M in combined territory revenue). Your platform investment is invisible to a third of your selling capacity."

**Data**: `org_users` (all assigned reps) vs `login_events` (90-day activity). Cross-reference with territory assignments and `portal_orders` for territory revenue context.

**Why it's explosive**: Frames non-adoption not as a "usage metric" but as a revenue gap. "$27M in territory revenue is being managed without your platform" is a sentence that makes a CEO pick up the phone.

**Section**: §2 Sales Team

---

## E. Redundancy Kills

1. **Executive Summary highlights → Section intros → Subsection callouts**
   The CCI report says "15 accounts decelerating with $2.2M at risk" in the executive summary, then repeats it nearly verbatim as the §3 Deceleration Alert callout, then repeats it again in the "What this tells you" box. The first mention creates impact; the third feels like padding.
   **Keep**: Executive summary (for the 5-minute reader) + the in-section data table (for the deep reader). **Cut**: The introductory callout box that restates the summary stat before showing the table.

2. **§2 "What this means" boxes often restate the table**
   The Rep Activity Ladder table shows Stacie Baker at $765K/131 customers. The "What this tells you" box below says "Your top performer generates $765K in iPad orders across 131 customers." This is literally reading the table back to the client.
   **Keep**: Only interpretive commentary that adds new information. "The $485K gap between #1 and #10 suggests room to elevate mid-tier performers" — that's additive. "Your top performer generates $765K across 131 customers" is not.

3. **§5 Total Business Context → §5 eCat Capture Rate**
   The "Total Business Context" subsection establishes $87.1M total business. The immediately following "eCat Capture Rate" subsection restates "$8.6M of $87.1M total business." These should be one subsection, not two.
   **Keep**: Merge into a single "Channel Mix & Capture Rate" subsection that states total business once and immediately pivots to the capture rate story.

4. **§2 Archetypes → §2 Coaching Opportunities overlap heavily**
   The archetype analysis says "Volume Relationship Seller needs order-value support." The coaching section then identifies the same reps with the same gap. The archetype section creates the mental model; the coaching section names the action — but the overlap makes it feel repetitive.
   **Keep**: Merge archetypes into the coaching section as a framing device. "Sandy Glosson (Volume Relationship Seller) — Gap: Presentation..." is tighter than two separate tables that reference the same reps.

5. **§4 Catalog Completeness appears in both §4 Product and §8 Platform**
   CCI's §8 opens with "Catalog Health: 3,386 visible products, 95.7% completeness, 144 missing images." §4 also discusses catalog completeness in the broader product context. Two sections claiming the same metric.
   **Keep**: §8 owns the operational "fix this" recommendation (upload 144 images). §4 should reference it once ("See §8 for catalog completeness details") and focus exclusively on sales performance of the catalog — what's selling, what's not, velocity trends.

---

## F. The Rewrite List (7 Changes)

### 1. Lead Every Executive Summary with a Dollar Figure, Not a Metric
**Current**: "81.7% fill rate with accelerating demand" (CCI highlight #1)
**Change to**: "$1.6M in potential lost sales from stockouts on your top 20 sellers" — then explain the fill rate as supporting evidence. Clients think in dollars, not percentages. Every highlight should have a $ value in the first clause.

### 2. Add "What This Would Look Like If You Synced [X]" Callouts to Data-Poor Reports
**Where**: RW (no ERP), BCF (partial ERP). Add a persistent subtle callout at the end of each gated-out subsection:
> "If total-business order data were connected, this section would show your eCat capture rate — how much of your full revenue flows through the platform. Clients with this data typically discover 70–90% of their business is invisible to their digital ordering platform."

This makes the upsell moment explicit without being salesy.

### 3. Replace the §6 Portal Section with "Demand Signal Intelligence"
**Current**: Traffic counts, session durations, monthly trend tables — metrics that make a B2B manufacturer say "why is this here?"
**Change to**: "Demand Signal Intelligence — 23 unique companies researched your products online this month but didn't place an order. Here's the estimated value they represent based on their browsing depth and your average order conversion."

This reframes anonymous web traffic as qualified pipeline. Use Clicky session depth + product page views to estimate commercial intent. Even without conversion data, "23 companies were looking at your chandeliers for 6+ minutes" is infinitely more interesting than "you had 11 daily visitors."

### 4. Collapse the §8 Platform Section to a One-Page "Health Check" Card
**Current**: 6 subsections totaling ~300 lines of HTML with tables, pipeline counts, and stack details
**Change to**: A single dense card with traffic-light indicators:
- ✅ Core pipeline healthy (products, customers, inventory updating daily)
- ⚠️ 3 alerts (Price Levels stale 299d, Options stale 299d, Library content stale 601d)
- 🔍 Feature opportunity (SmartPicks underused — 150 events vs 46K product searches)

The current section is comprehensive but reads like a sysadmin dashboard. A VP doesn't need to know about import counts — they need to know "is there a problem, and how do I fix it?"

### 5. Add a "Revenue-at-Stake" Calculation to Every Coaching Card
**Current**: "Coaching Opportunity: Sandy Glosson — +$69K potential annual GMV if AOV rises to team median"
**Problem**: The $69K estimate is useful but feels like it could be bigger. The framing buries the total team opportunity.
**Change to**: Add a team-level rollup at the top of the coaching section: "Combined coaching upside across 4 priority reps: $225K in annual incremental GMV. That's 2.6% of your current eCat revenue from behavioral coaching alone — with zero new customer acquisition required."

### 6. Make Peer Benchmarking Competitive, Not Abstract
**Current format** (inferred from gate flags — HAS_PEER_DATA = true for all 5): Percentile comparisons against segment cohort.
**Change to**: Frame as competitive positioning with stakes:
> "Brands in your segment's top quartile capture 3.2× the eCat order volume of bottom-quartile brands. You're at the 65th percentile — above average, but $4.3M in annual platform GMV separates you from the leaders. The difference isn't product or market — it's rep adoption depth and customer activation rate."

Competitive framing creates urgency. "You're in the 65th percentile" is a statistic. "Here's what separates you from the leaders, and it's fixable" is a catalyst.

### 7. Add a One-Paragraph "What We'd Investigate If We Had a Call" Section
**Where**: End of the executive summary, before the section deep-dives begin.
**Content** (CCI example):
> "Three patterns in this data warrant a 15-minute conversation: (1) Your Virginia expansion is outpacing coverage — who's managing that growth? (2) Five established reps declined 31–60% last quarter while five new reps surged — is this a territory reassignment or competitive dynamic? (3) Furnitureland South went dormant after 11 orders and $111K — do you know why?"

This is the conversion mechanism. It turns the report from a document into a conversation starter. It gives the SuperCat account manager a script.

---

## G. The Verdict

| Report | Forward to CEO? | Call SuperCat rep? | Sits in inbox? |
|--------|----------------|-------------------|----------------|
| **CCI** | **Yes.** The $2.2M at-risk accounts, the stockout alert on $872K products, and the 9.8% capture rate gap create genuine urgency. A CEO sees this and says "we need to talk about customer retention and platform adoption." | Yes — immediately. The stale price levels alone warrant a call, and the deceleration alert demands action. | No chance. |
| **UFI** | Maybe. The capture rate story ($13.4M of $137.9M) is strong enough to forward, but the sales team section is thinner and the portal section adds length without proportional impact. | Likely yes — the commerce data alone justifies a conversation about why 90% of their business still bypasses the platform. | Unlikely, but possible if the VP is busy. |
| **HFG** | Probably not. The 40% capture rate is impressive (and should be celebrated), which means the report is validating rather than alarming. Validation reports don't get forwarded — alarm reports do. | Yes, but for a "things are going well, here's what's next" conversation rather than an urgent one. The sales team data and portal trends give the rep something to discuss. | Possible. This is a "that's nice" report for a client who's already succeeding. |
| **RW** | No. Without ERP data, the report lacks the comparative context that creates urgency. "$10.6M in eCat GMV" is impressive but doesn't tell you what you're missing. The report works as a relationship touchpoint but doesn't create a CEO-level moment. | Maybe. The rep section with 47 reps is interesting, and the Clicky data adds color. But the primary value is as a proof-of-concept for "imagine what this report could be with full data." | Likely sits in inbox for most executives. Useful for a sales manager but not escalation-worthy. |
| **BCF** | Probably not. The VM-45 suppression (ERP GMV < eCat GMV) means the most compelling story (capture rate gap) can't be told. The sales team behavioral data is excellent but requires a sales-manager audience, not a CEO audience. | Yes — the behavioral coaching data (archetypes, conversion rates) is genuinely useful for whoever manages the rep team. The B2B Cart context also creates a product conversation. | For a CEO, yes. For a VP of Sales, no — they'd use it. |

### Summary Judgment

**CCI is the gold standard.** It's the only report in the batch that consistently creates "I need to act on this" reactions. The combination of named accounts + dollar values + urgency framing + actionable next steps makes it feel like a private intelligence briefing.

**The gap between data-rich and data-poor is massive — and it's mostly about one thing: the total-business comparison.** Without ERP data (portal_orders), you cannot tell the capture rate story, you cannot identify which customers are buying through other channels, and you cannot surface deceleration against all-channel velocity. The difference isn't 20% better — it's a fundamentally different product.

**The reports' biggest weakness is length.** A VP with 5 minutes will read the executive summary and click one section. If that section rewards them — specific names, specific dollars, specific actions — they'll read another. If it gives them a table of metrics they could get from their own CRM, they'll close the document. The reports need to front-load surprise and action, and back-load operational detail.

**The reports' biggest strength is specificity.** Named reps. Named accounts. Dollar figures. Dates. This isn't a dashboard — it's an intelligence document that names names. That specificity is what makes it impossible to replicate with Salesforce or a generic BI tool. Protect it.

**No competitor can do this.** The combination of per-rep behavioral data (Mixpanel) + eCat order outcomes + ERP total-business comparison + cross-instance peer benchmarking is uniquely SuperCat. The closest alternative would require a client to integrate Salesforce, their ERP, a behavioral analytics tool, and build their own peer comparison — a $200K+ BI project that would still lack the platform-specific behavioral taxonomy. These reports are a genuine competitive moat.
