# SuperCat Solutions — Executive Business Review Template Frameworks

**Version:** Working Draft | **Date:** March 2026

---

## Data Pipeline Notes (Updated 2026-03-04)

- **Revenue:** Always `SUM(order_items[].extended_price)` from Postgres.
  Never `orders.total` (includes shipping/tax).
- **Date range:** TTM = last 12 complete months ending last complete month.
  Never YTD. Never partial current month.
- **Rep attribution:** Postgres `orders.rep_first_name + rep_last_name`.
  BQ `order_submitted` is unreliable for some orgs (e.g. clm had 149 PG
  orders, 2 BQ events). Validate before using BQ for rep ranking.
- **Licensed users:** `allow_ipad_logins = true`, exclude Employee%,
  Customer%, Touchscreen%, IMAP%, eCat%, z-SuperCat, Automation, Meridian.
- **No CSVs:** All data from Postgres MCP + BigQuery MCP directly.

---

## How to Use This Document

Three structurally distinct EBR frameworks are presented below. Each is designed to be universal across all SuperCat clients — ordering and non-ordering use cases, all segments, all module configurations. The frameworks differ in what leads the conversation and how data is positioned relative to strategic dialogue.

Each section includes:
- **Purpose** — why this section exists
- **Content** — what goes in it
- **Data Inputs** — which metrics and sources populate it
- **Presenter Notes** — how to deliver it
- **Use-Case Flex** — how the section adapts for ordering vs. non-ordering clients

---

# Template A: Discovery-Led

> **Philosophy:** Open with the client's world, use data as supporting evidence mid-conversation, close with co-created next steps. The meeting is a strategic conversation that happens to be informed by data — not a data presentation with discussion bolted on.

> **Best for:** Relationship-first engagements where strategic dialogue and trust-building are the primary value. Clients who value being heard over being shown.

---

## A1. Partnership Snapshot

**Purpose:** Ground the room in the relationship. This is not a company overview — it's a reminder that this meeting exists because of a shared history and shared goals.

**Content:**
- Relationship tenure (e.g., "Partner since March 2023")
- Active products (eCat iPad, eCat Online, Sales Portal, Admin Console — which are live)
- Key stakeholders in the room and their roles
- One-line framing: "This is your review — our goal today is to understand where your business is heading and how we can support that."

**Data Inputs:**
- Contract start date (HubSpot / Stripe)
- Active module list (Stripe subscription data, Admin Console)
- Contact roles (HubSpot contacts)

**Presenter Notes:**
- Spend no more than 90 seconds here. This slide exists to orient, not to impress.
- If this is a first EBR, briefly acknowledge the relationship arc. If ongoing, reference what was agreed in the last session.

**Use-Case Flex:** None needed — this section is universal.

---

## A2. Your Business & Market

**Purpose:** Open the discovery conversation. Before any data is presented, understand what's changed in the client's world. This section is designed to *listen*, not present.

**Content:**
- 3-5 pre-seeded questions tailored to the account, based on internal prep:
  - "What's shifted in your market since we last spoke?"
  - "Are you expanding into new channels — hospitality, designers, new retail segments?"
  - "How is your sales team structure evolving? Any territory changes or new hires?"
  - "Any changes on the ERP, supply chain, or fulfillment side?"
  - "What's keeping your leadership up at night right now?"
- Space for notes / live capture

**Data Inputs:**
- Pre-meeting research: recent company news, trade show appearances, hiring signals, industry trends
- Fathom call history: pain themes, competitor mentions, objections from recent conversations
- HubSpot: any open deals, recent engagement notes
- Internal account brief: known business context, strategic opportunities flagged

**Presenter Notes:**
- This is the most important section of the meeting. Resist the urge to fill silence.
- The questions should feel specific to *this* client, not generic. "I noticed you were at High Point Market last month — how did that go?" is better than "Any market changes?"
- Capture responses — they inform everything that follows and feed back into the internal brief.

**Use-Case Flex:** Questions should reflect how the client uses SuperCat. For non-ordering clients, lean into catalog presentation workflows, showroom strategy, and buyer engagement rather than transaction-oriented questions.

---

## A3. Platform Utilization Overview

**Purpose:** Provide an objective snapshot of how the client's organization is using SuperCat today. Framed as operational visibility, not a scorecard.

**Content:**
- Module-level view: which products are active, user counts per module
- Utilization rate: active users vs. licensed users
- Engagement trend: MAU trend (6-month) showing trajectory
- Feature adoption summary: high-level view of which capability clusters are being used (mapped to Activity Ladder levels but presented in business language, not framework terminology)
- Channel mix (if applicable): iPad vs. web usage patterns

**Data Inputs:**
- Active User Ratio (PostgreSQL MCP, Admin Console)
- MAU Trend — 6-month (Mixpanel)
- Feature Adoption Rate (Mixpanel, PostgreSQL MCP)
- Mobile vs. Web Split (Mixpanel)
- User Growth Trend (PostgreSQL MCP)
- Subscription Completeness (Stripe, Admin Console)
- Channel Revenue Share / Channel Adoption Trend (Admin Orders Report, Mixpanel) — ordering clients only

**Presenter Notes:**
- Translate every metric into business language. Not "Feature Adoption Rate: 62%" but "Your team is actively using about two-thirds of the capabilities available to them — let's look at where the gaps are."
- For non-ordering clients, do NOT show order-based metrics. Lead with engagement depth and feature breadth.
- This section should take 3-5 minutes of presentation, with natural pauses for client reaction.

**Use-Case Flex:**
- **Ordering clients:** Include order velocity (orders per active user, AOV, daily order average) and channel performance (iPad vs. web revenue share, channel AOV comparison).
- **Non-ordering clients:** Focus on catalog engagement metrics — PDF catalog creation rate, product searches, customer list creation, SmartPicks usage, resource library access. Frame around "how your team is using eCat as a selling tool."

---

## A4. Your Sales Team in Action

**Purpose:** Deliver the rep behavioral intelligence the client wants for their own sales management. This is *their* data — SuperCat is the lens.

**Content:**
- Rep-level activity summary: which reps are leveraging which capabilities
  - Door reports / SmartStack usage
  - Placement views and management
  - SmartPicks usage
  - List creation (My Lists, Smart Lists)
  - Customer Favorites and Backorder views
  - PDF Catalog creation
  - Item email drafting
  - Barcode scanning (market/trade show contexts)
- Power user identification: who's using the platform deeply
- Enablement opportunities: reps with low engagement across key behaviors
- Activity Ladder summary: presented as behavioral maturity, not a score (e.g., "These reps are strong in product discovery and customer targeting but haven't yet adopted the personalization tools")
- ~~Optional: raw data export (CSV) available as a companion deliverable~~ **DEPRECATED** — all data sourced live from Postgres MCP + BigQuery MCP

**Data Inputs:**
- All Activity Ladder events per rep (Mixpanel)
- Orders per Rep (Mixpanel, Admin Console) — ordering clients only
- Feature Breadth Score per rep (Mixpanel)
- User Concentration Risk (Mixpanel)
- Rep Activity Ranking (Mixpanel)
- PDF Catalogs per Order / per rep (Mixpanel)
- SmartPicks Usage per rep (Mixpanel)
- Email Item Info per rep (Mixpanel)
- Scan Item Usage per rep (Mixpanel)

**Presenter Notes:**
- Frame this as "here's what your team is doing" not "here's how your team scores."
- For non-ordering clients, explicitly acknowledge: "We know orders flow through other channels — what we can show you is the selling behaviors happening inside the platform and which reps are leveraging the tools available."
- Be prepared to provide the raw spreadsheet. Some stakeholders (the Beth Miller profile) want the CSV to run their own analysis. Have it ready.
- The correlation question will come up: "Does this actually drive sales?" For clients where orders don't flow through eCat, invite them to overlay their own performance data. Offer to support that analysis.

**Use-Case Flex:**
- **Ordering clients:** Pair behavioral data with order metrics (orders per rep, revenue per rep, orders per login). The correlation story is self-contained.
- **Non-ordering clients:** Behavioral data only. Position as: "Here's the engagement picture. You hold the sales performance data — let's talk about how these patterns map to what you're seeing."

---

## A5. Your Customer Signals

**Purpose:** Surface intelligence about the client's own customer base — their retailers, dealers, distributors, designers. Revenue leak detection that only exists because their operations flow through SuperCat.

**Content:**
- Inactive buyer flag: customers who didn't place an order this month when historical patterns suggest they should have
- Reorder gap analysis: products a customer has historically purchased but hasn't reordered within 6-8 weeks
- Customer Activation Rate: what percentage of their customer accounts are actively engaging through the platform
- Digital Self-Service Rate (if on eCat Online): which customers are using self-service ordering vs. relying entirely on rep-mediated transactions
- Top customer engagement summary: most active buyers, emerging accounts, declining accounts

**Data Inputs:**
- Customer Activation Rate (Admin Console, PostgreSQL MCP)
- Digital Self-Service Rate (Mixpanel, Admin Console)
- Order Frequency by customer (Admin Orders Report)
- eCat Online Activation (Admin Console, PostgreSQL MCP)
- Customer-level order history for gap analysis (Admin Orders Report, PostgreSQL MCP)
- Sales data pushed into eCat by the client (for non-ordering clients who push sales data)

**Presenter Notes:**
- This section has high perceived value because it's directly actionable. The client can take these lists to their next sales meeting.
- For non-ordering clients who push sales data into eCat, the inactive buyer and gap analysis still work — clarify this.
- Position as: "These are the patterns the platform can see across your entire dealer network that individual reps might miss."

**Use-Case Flex:**
- **Ordering clients:** Full transaction-based analysis — order gaps, reorder patterns, customer-level AOV trends.
- **Non-ordering clients (with sales data pushed):** Same analysis using the pushed sales data. Acknowledge the data source difference transparently.
- **Non-ordering clients (no sales data pushed):** This section thins considerably. Focus on customer activation through platform engagement (logins, catalog views) rather than order behavior. Flag this as an opportunity: "If we can get sales data flowing in, we can unlock this intelligence for you."

---

## A6. Opportunities on the Horizon

**Purpose:** Based on what was heard in discovery and what the data shows, surface relevant opportunities. These should feel co-created, not prescribed.

**Content:**
- 2-3 specific opportunities tied to the conversation and data findings
- For each opportunity:
  - What it is (feature enablement, module adoption, workflow improvement, channel expansion)
  - Why it's relevant now (connected to a client-expressed need or a data-surfaced pattern)
  - What it looks like in practice (peer context — anonymized, segment-level)
  - What the next step would be
- Expansion signals identified from the data (drawn from the 20+ expansion signals in the metrics framework, but only those relevant to this client)

**Data Inputs:**
- Expansion Signals table (cross-referenced against this client's data)
- Subscription Completeness (Stripe, Admin Console) — what modules are available but not active
- Cross-Entity Feature Gap (Mixpanel) — for multi-entity accounts
- Industry Segment Benchmarks — peer comparison context
- Fathom pain themes — what the client has expressed as challenges in recent calls

**Presenter Notes:**
- Never present more than 3 opportunities. Prioritize ruthlessly.
- Every opportunity must connect to something the client said in the discovery section or something the data revealed that the client confirmed matters. If neither condition is met, don't present it.
- Peer context is powerful but must be anonymized. "Companies in your segment with similar catalog sizes typically see X" — never name competitors.

**Use-Case Flex:**
- **Ordering clients:** Opportunities may include eCat Online expansion (self-service ordering), Sales Portal activation (customer-facing dashboards), channel optimization.
- **Non-ordering clients:** Opportunities may include deeper feature adoption (SmartPicks, placements, configured items), eCat Online as a buyer-facing catalog, Sales Portal for customer self-service on order status and invoices (especially if sales data is pushed).

---

## A7. Shared Priorities & Next Steps

**Purpose:** Close with a co-created action plan. The meeting produces commitments, not just conversation.

**Content:**
- 3-5 prioritized action items
- For each: what, who owns it (both sides), target date
- Agreed cadence for next check-in
- Any data or deliverables to be shared post-meeting (raw CSV exports, follow-up analysis, etc.)

**Data Inputs:** None — this is generated live in the meeting.

**Presenter Notes:**
- Write this section collaboratively in real time. The client should see their input reflected.
- Send a formalized version within 48 hours.
- Feed all commitments back into the internal account brief and CRM.

**Use-Case Flex:** None — universal.

---
---

# Template B: Intelligence-Led

> **Philosophy:** Lead with the data the client can't get anywhere else — rep behavior and customer signals — then broaden into strategic conversation. The intelligence earns the right to have the strategic dialogue.

> **Best for:** Operationally-minded clients whose stakeholders are sales leaders and ops people. Clients who want to see the data first and discuss implications second. The BCG/Visual Comfort profile.

---

## B1. Partnership Context

**Purpose:** Brief anchor. Same function as Template A — orient the room, establish the relationship frame.

**Content:**
- Relationship tenure, active products, stakeholders present
- One-line framing: "Today we're sharing intelligence about your sales team and customer base, and we want your guidance on what matters most."

**Data Inputs:** Same as A1.

**Presenter Notes:** 60-90 seconds. Move quickly — this audience wants to get to the data.

**Use-Case Flex:** None.

---

## B2. Sales Team Performance Intelligence

**Purpose:** The headline section. Deliver the rep behavioral data the client needs for sales management — in a format that's immediately actionable.

**Content:**
- **Rep Activity Dashboard:** Every rep mapped against key behaviors:
  - Door reports / SmartStack views (by rep AND by customer)
  - Placement views and updates
  - SmartPicks usage
  - List creation and sharing
  - Customer Favorites and Backorder views
  - PDF Catalog creation
  - Item email drafting
  - Barcode scanning activity
  - Invoice and Favorites review
- **Power User Profiles:** Top 3-5 reps by engagement depth, with specific behaviors highlighted
- **Enablement Gaps:** Reps with low or zero activity on key behaviors, presented as a list
- **Concentration Risk:** If one rep accounts for a disproportionate share of activity or orders, flag it
- **Behavioral Trends:** MoM comparison — is the team using the platform more or less than last period?
- ~~**Raw Data Companion:** CSV export of the full activity dataset~~ **DEPRECATED** — data sourced live from Postgres MCP + BigQuery MCP

**Data Inputs:**
- Full Activity Ladder events per rep (Mixpanel)
- All rep-level metrics from Section 6 of the metrics framework
- User Concentration Risk (Mixpanel)
- Feature Breadth Score per rep (Mixpanel)
- Orders per Rep, Revenue per Rep (Admin Console) — ordering clients only
- Login Frequency per rep (Mixpanel, Admin Console)

**Presenter Notes:**
- This is the section Beth Miller is asking for. Lead with names, specific behaviors, specific numbers.
- Organize by rep, not by feature. The client thinks in terms of people, not capabilities.
- For non-ordering clients, explicitly frame: "We're showing you everything we can see about how your reps work inside the platform. The piece we can't see is the final transaction — that's where we'd love your input on whether these behaviors are correlating with the results you're tracking."
- ~~Have the CSV ready before the meeting starts.~~ **DEPRECATED** — data pulled live via MCP; exports generated on demand if needed.

**Use-Case Flex:**
- **Ordering clients:** Full picture — behavioral data paired with order data per rep. Include orders per login, revenue per rep, channel usage (iPad vs. web per rep).
- **Non-ordering clients:** Behavioral data only, organized identically but without order columns. Include a "correlation opportunity" note: "If you can share rep performance data, we can map behavioral patterns to outcomes."

---

## B3. Customer Base Health

**Purpose:** Surface intelligence about the client's customers — the retailers, dealers, and buyers they serve.

**Content:**
- **Inactive Buyer Flags:** Customers with no order this month who have historical ordering patterns suggesting they should have ordered
- **Reorder Gap Analysis:** Specific products historically purchased by specific customers that haven't been reordered in 6-8 weeks — presented as an actionable list
- **Customer Activation Rate:** What percentage of the client's customer accounts are actively engaging
- **Customer-Level Activity:** For key accounts, which reps are servicing them, what activities are happening (door reports run, placements checked, etc.)
- **Self-Service Adoption** (if on eCat Online): Which customers are using self-service vs. remaining fully rep-dependent

**Data Inputs:**
- Customer Activation Rate (Admin Console, PostgreSQL MCP)
- Customer-level order and engagement data (Admin Orders Report, PostgreSQL MCP)
- Digital Self-Service Rate (Mixpanel, Admin Console)
- eCat Online Activation by customer (Admin Console, PostgreSQL MCP)
- Rep-to-customer activity mapping (Mixpanel — Select Customer, Search Customer events)

**Presenter Notes:**
- The inactive buyer list and reorder gap analysis are the highest-value deliverables in this section. They're directly actionable in the client's next sales meeting.
- Present customer-level data organized by territory or rep assignment where possible — this is how the client's sales leadership thinks.
- For non-ordering clients without sales data pushed, this section will be thinner. Be transparent about what's available and what could be unlocked.

**Use-Case Flex:** Same as A5.

---

## B4. Platform & Data Health

**Purpose:** Operational health check — is the engine running clean? Matters to admin/ops stakeholders and builds trust.

**Content:**
- Data freshness: when were products, customers, inventory last updated
- Import success rate (30-day)
- Integration status: FTP/API health
- Catalog completeness: products with images %, category/collection depth
- Territory configuration status
- Any error patterns or sync issues

**Data Inputs:**
- All metrics from Section 9 of the metrics framework (Data Health & Operational Efficiency)
- Data Freshness Score (PostgreSQL MCP)
- Import Error Rate (PostgreSQL MCP)
- Last Sync Timestamp (PostgreSQL MCP)
- Products with Images % (PostgreSQL MCP)
- Territory Configuration (PostgreSQL MCP)

**Presenter Notes:**
- Keep this section brief — 2-3 minutes. It's a trust builder, not a deep dive.
- If there are issues (stale data, import errors), surface them proactively. The client will respect honesty.
- If everything is healthy, say so quickly and move on.

**Use-Case Flex:** Universal — applies to all clients regardless of ordering behavior.

---

## B5. Business Context & Market Check-In

**Purpose:** The discovery section — but positioned after the intelligence sections have set context. Now the conversation has shared data to reference.

**Content:**
- Facilitated discussion anchored to what the data revealed:
  - "We saw [X pattern] in your customer base — is that reflecting something you're seeing in the market?"
  - "Your team's usage of [feature] has increased — what's driving that?"
  - "Are there changes in your business that would help us make this data more useful?"
- Open questions about business direction, competitive landscape, strategic priorities

**Data Inputs:**
- Pre-meeting research (same as A2)
- Fathom call history
- Patterns surfaced in B2, B3, B4 that warrant discussion

**Presenter Notes:**
- This section has more traction than Template A's discovery because both sides now have shared context. Use the data as conversation starters.
- Don't re-present data — reference it conversationally. "We showed you that SmartPicks usage is low — is that a training issue, or does the feature not fit your workflow?"

**Use-Case Flex:** Same as A2.

---

## B6. Utilization & Growth Opportunities

**Purpose:** Module adoption view plus specific opportunities surfaced by the data.

**Content:**
- Current module footprint vs. full platform capability
- Specific unused capabilities tied to patterns from earlier sections
- Peer context: what similar companies in their segment are leveraging
- 2-3 prioritized recommendations with business case framing

**Data Inputs:**
- Subscription Completeness (Stripe, Admin Console)
- Expansion Signals (cross-referenced against this client)
- Industry Segment Benchmarks
- Cross-Entity Feature Gap (for multi-entity accounts)

**Presenter Notes:**
- This section should feel like a natural conclusion to the data story, not a sales pitch.
- Every recommendation connects to something surfaced earlier in the meeting.

**Use-Case Flex:** Same as A6.

---

## B7. Action Plan

**Purpose:** Prioritized next steps with owners and dates.

**Content:** Same as A7.

**Presenter Notes:** Same as A7. For this audience, be especially crisp and specific — ops-minded stakeholders want clarity, not open-ended commitments.

**Use-Case Flex:** Universal.

---
---

# Template C: Benchmark-Forward

> **Philosophy:** Structure the entire meeting around where the client sits relative to their potential — in platform utilization and in the business outcomes the platform enables. Peer comparison and maturity framing drive the conversation.

> **Best for:** Competitive, benchmark-oriented clients who want to know where they stand. Clients who are motivated by peer comparison and maturity frameworks.

---

## C1. Partnership Snapshot

**Purpose:** Same brief anchor as Templates A and B.

**Content:** Same as A1.

**Data Inputs:** Same as A1.

**Presenter Notes:** Same as A1.

**Use-Case Flex:** None.

---

## C2. Where You Stand: Adoption Maturity

**Purpose:** The centerpiece. A clear visual of where the client sits relative to the full platform capability set and relative to their peers.

**Content:**
- **Module Adoption Map:** Visual showing which SuperCat products are active vs. available. Clear, simple — green/gray or similar.
- **Feature Utilization Heatmap:** Across all active modules, which capabilities are being used deeply, lightly, or not at all. Organized by Activity Ladder levels but labeled in business language.
- **Peer Benchmark Overlay:** Anonymized comparison to similar companies in their segment (by vertical, by size, by product suite). "Companies like yours in lighting with similar catalog sizes typically leverage these capabilities at these levels."
- **Maturity Stage:** A simple framework — Early (foundational use), Growing (expanding capabilities), Optimized (deep utilization across suite). Where does this client sit? Non-judgmental, aspirational framing.

**Data Inputs:**
- Subscription Completeness (Stripe, Admin Console)
- Feature Adoption Rate (Mixpanel, PostgreSQL MCP)
- All Activity Ladder metrics (Mixpanel)
- Industry Segment Benchmarks (Section 15 of metrics framework)
- Benchmarking Dimensions: Org Size, Tenure, Product Suite, Integration Maturity (Section 15)
- Active User Ratio (PostgreSQL MCP, Admin Console)
- MAU Trend (Mixpanel)

**Presenter Notes:**
- This section needs strong visuals. The maturity map should be immediately legible — the client should grasp where they stand in 10 seconds.
- Peer benchmarks must be anonymized. "In your segment" or "among companies with 20-50 reps" — never name competitors.
- Frame gaps as opportunities, not deficiencies. "You're strong in product discovery — companies that also activate the personalization layer tend to see deeper rep engagement."
- This is where the Kent Phillips model lives. Benchmark what they use, show them what peers use, and let the gap do the talking.

**Use-Case Flex:**
- **Ordering clients:** Benchmarks include transaction metrics (AOV, orders per user, customer activation rate) alongside behavioral metrics.
- **Non-ordering clients:** Benchmarks focus on engagement depth, feature breadth, catalog utilization, and selling behaviors. Exclude order-based comparisons — or note them as "among clients who transact through eCat" to maintain transparency.

---

## C3. Your Reps vs. the Benchmark

**Purpose:** Apply the same benchmarking lens to the rep level — where do this client's reps sit relative to the 7,000+ rep universe?

**Content:**
- **Activity Ladder Results:** Organization-level aggregate showing strength at each level
  - Level 1: Customer Targeting
  - Level 2: Product Discovery
  - Level 3: Information Sharing
  - Level 4: Personalization
  - Level 5: Advanced Features
  - Level 6: Engagement Depth
- **Segment Benchmark:** How this organization's Activity Ladder profile compares to their vertical peers
- **Rep Distribution:** How many reps are at each maturity level — are a few power users pulling the average up, or is adoption broad?
- **Power User Spotlight:** Top performers and what they're doing differently
- **Enablement Opportunities:** Specific behaviors with low adoption that peer organizations have activated successfully

**Data Inputs:**
- Activity Ladder scoring per rep (Mixpanel, Admin Console User Feature Report)
- Rep-level metrics from Section 6 of the metrics framework
- Feature Breadth Score per rep (Mixpanel)
- User Concentration Risk (Mixpanel)
- Segment-level Activity Ladder benchmarks (aggregated from 129 active orgs)

**Presenter Notes:**
- The power of this section is the 7,000+ rep benchmark universe. Most vendors cannot offer this — lean into it.
- Present the organizational aggregate first, then allow drill-down into individual reps if the client wants it.
- ~~Have the raw CSV ready — same principle as Template B.~~ **DEPRECATED** — data pulled live via MCP.
- Frame around "potential" not "gaps." "Your team is strong at Levels 1 and 2 — the next unlock for organizations like yours is typically Level 3 and 4 behaviors."

**Use-Case Flex:**
- **Ordering clients:** Include order-based metrics in the rep comparison (orders per rep, revenue per rep).
- **Non-ordering clients:** Pure behavioral benchmarking. "Among all reps using eCat as a selling tool (not just ordering), here's where your team sits."

---

## C4. Your Customer Engagement Profile

**Purpose:** Customer-level intelligence with benchmark context where possible.

**Content:**
- **Customer Activation Rate vs. Segment Median:** What percentage of the client's customers are actively engaging, compared to peers
- **Self-Service Adoption** (if on eCat Online): Percentage of customers using self-service, benchmarked
- **Inactive Buyer Flags:** Customers with no recent orders who historically order regularly
- **Reorder Gap Analysis:** Products historically purchased but not reordered in 6-8 weeks
- **Top/Declining Customer Summary:** Most engaged and most at-risk customer accounts

**Data Inputs:**
- Customer Activation Rate (Admin Console, PostgreSQL MCP) + segment benchmarks
- Digital Self-Service Rate (Mixpanel) + segment benchmarks
- Customer-level order history (Admin Orders Report, PostgreSQL MCP)
- eCat Online Activation (Admin Console, PostgreSQL MCP)

**Presenter Notes:**
- The benchmark context here is the differentiator. "Your customer activation rate is 45% — the segment median for furniture companies your size is 62%. Let's talk about what's driving that gap."
- Inactive buyer flags and reorder gaps are the actionable outputs — benchmark framing provides the strategic context, these lists provide the tactical follow-up.

**Use-Case Flex:** Same as A5.

---

## C5. What's Changed Since Last Review

**Purpose:** Brief retrospective. Kept intentionally short — the benchmarks and current-state data carry the weight.

**Content:**
- Progress against previously agreed priorities
- Notable shifts in usage patterns (positive or negative)
- Support themes worth highlighting (ticket trends, resolution improvements, recurring issues)
- Any milestones or achievements worth acknowledging

**Data Inputs:**
- Previous EBR commitments (CRM / meeting notes)
- MAU Trend comparison period-over-period (Mixpanel)
- Support Health metrics (HelpScout) — ticket volume, trend, themes
- TTFV for any newly onboarded users (Mixpanel)

**Presenter Notes:**
- Maximum 2-3 minutes. This section exists for continuity, not as a deep dive.
- If a previously agreed action wasn't completed (by either side), acknowledge it honestly.
- Support themes are worth surfacing here because they often connect to training opportunities that the benchmark sections identified.

**Use-Case Flex:** Universal.

---

## C6. Discovery: What's Ahead

**Purpose:** Open strategic conversation — but positioned after benchmarking so the client has context for what "more" could look like.

**Content:**
- Facilitated discussion:
  - "Based on where you sit relative to peers, what resonates? What surprised you?"
  - "What's changing in your business that might shift your priorities?"
  - "Which of these gaps matter to you, and which don't?"
  - "Where are you headed in the next 6-12 months?"
- The benchmark naturally prompts the client to ask "how do we close those gaps?" — be ready with answers but let them drive.

**Data Inputs:**
- Pre-meeting research (same as A2)
- Fathom call history
- Patterns from the benchmark sections

**Presenter Notes:**
- The benchmark sections do the heavy lifting of seeding the conversation. Discovery here is about priorities and direction, not problem identification — the data already surfaced the problems.
- Listen for which gaps the client cares about vs. which they dismiss. This tells you where expansion energy should focus.

**Use-Case Flex:** Same as A2, adapted for the benchmark context.

---

## C7. Recommendations & Roadmap

**Purpose:** Specific, prioritized recommendations tied to the benchmark gaps and the discovery conversation.

**Content:**
- 2-3 recommendations, each structured as:
  - **The Gap:** What the benchmark revealed
  - **The Opportunity:** What closing the gap could look like (business outcome, not feature)
  - **The Path:** Practical next steps — training, enablement, module activation, workflow change
  - **Peer Evidence:** What similar organizations did and what resulted (anonymized)
- Rough timeline for each recommendation
- Ownership model: what SuperCat provides, what the client needs to do

**Data Inputs:**
- Expansion Signals (cross-referenced against this client)
- Subscription Completeness (Stripe, Admin Console)
- Industry Segment Benchmarks
- Fathom pain themes

**Presenter Notes:**
- Recommendations must connect to gaps the client validated as important in the discovery section. Don't recommend closing a gap they explicitly said doesn't matter.
- Peer evidence is the unique asset here. "When [segment peer] activated SmartPicks and ran enablement training, their Level 5 adoption went from 12% to 47% in one quarter." Anonymized but specific.

**Use-Case Flex:** Same as A6.

---

## C8. Commitments & Next Steps

**Purpose:** Mutual action items, review cadence, accountability.

**Content:** Same as A7.

**Presenter Notes:** For benchmark-oriented clients, commit to sharing updated benchmarks at the next review. This creates a natural cadence and gives the client a reason to reconvene.

**Use-Case Flex:** Universal.

---
---

# Cross-Template Reference: Use-Case Profile Flag

All three templates require a **use-case profile** determination before meeting prep begins. This drives which metrics appear and how sections are framed.

| Profile | Characteristics | Metrics Emphasis | Sections Affected |
|---|---|---|---|
| **Ordering Client** | Places orders through eCat iPad and/or eCat Online | Full transaction + behavioral metrics | A3, A4, A5, B2, B3, C2, C3, C4 |
| **Non-Ordering / Sales Enablement** | Uses eCat for catalog, presentation, buyer engagement; orders via EDI/fax/email/other | Behavioral and engagement metrics only; correlation opportunity with client's own data | A3, A4, A5, B2, B3, C2, C3, C4 |
| **Non-Ordering + Sales Data Pushed** | Same as above, but client pushes sales/invoice data into eCat | Behavioral metrics + customer intelligence from pushed data | A5, B3, C4 (customer sections gain depth) |

This flag should be the first field in the internal account brief and should be confirmed before any EBR content is assembled.

---

# Appendix: Data Source Quick Reference

| Data Need | Primary Source | Backup Source |
|---|---|---|
| Module activation | Stripe subscriptions | Admin Console |
| User counts & utilization | PostgreSQL MCP | Admin Console |
| Rep-level behavior (feature adoption) | BigQuery Mixpanel events | — |
| Rep attribution (who placed orders) | PostgreSQL `orders.rep_first_name + rep_last_name` | BigQuery `order_submitted` (only if validated) |
| Order & revenue data | PostgreSQL `orders` + `SUM(order_items[].extended_price)` | — |
| Customer engagement | PostgreSQL MCP | Mixpanel |
| Support health | HelpScout (BigQuery) | — |
| Meeting intelligence | Fathom (BigQuery) | — |
| Pipeline & deals | HubSpot (BigQuery) | — |
| Billing & MRR | Stripe | QuickBooks |
| Data health & integration | PostgreSQL MCP | — |
| Industry benchmarks | Aggregated internal data (129 orgs) | — |
