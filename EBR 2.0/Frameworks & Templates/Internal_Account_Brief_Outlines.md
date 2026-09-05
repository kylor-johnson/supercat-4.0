# Internal Account Brief — Framework & Outlines

**Version:** 1.0 | **Date:** February 26, 2026 | **Author:** Kylor Johnson

> Two document formats for internal account intelligence. Both are promptable via Cursor/MCP against BigQuery (166 tables) and PostgreSQL (108 tables). Neither is scoped to a specific meeting type, role, or engagement.

---

## Version A: Account Snapshot

**Purpose:** Answer "what's going on with this account right now?" in 60 seconds.

**Audience:** Anyone on the team. No context assumed.

**Generation:** On-demand. Can be run across all 129 accounts for portfolio triage or generated for a single account before any interaction.

**Length:** One page. Density over depth.

---

### A1. Identity Header

A compact block — no more than 4 lines.

| Field | Source | Notes |
|---|---|---|
| Company Name | PostgreSQL `organizations` | — |
| Industry Segment | PostgreSQL `organizations` / HubSpot `company` | Lighting, Furniture, Occasional/Accent, Outdoor/Casual, Housewares/Giftware |
| Products Active | Stripe `subscription` / PostgreSQL `subscriptions` | eCat iPad, eCat Online, Sales Portal, Admin Console |
| Use-Case Profile | Derived: Mixpanel `Submit Order` events (zero in 90d = non-ordering) | Ordering / Non-Ordering / Non-Ordering + Pushed Data |
| Partner Since | HubSpot `deal` (original close date) | Tenure in months/years |
| MRR | Stripe `subscription` | Current monthly recurring revenue |
| Primary Contact(s) | HubSpot `contact` | Name(s) + role(s) of key stakeholders |
| Account Owner | HubSpot `owner` | Internal owner |

---

### A2. Quadrant Placement

The single most important element on the page. Displays both scores and the resulting quadrant.

| Element | Source | Display |
|---|---|---|
| Expansion Readiness Score | Scoring model output | Numeric (0–100) + band label (Active Target / Nurture / Not Ready) |
| Retention Risk Score | Scoring model output | Numeric (0–100) + band label (Low / Watch / Elevated / Critical) |
| Quadrant | Derived from both scores | **GROW** / **SAVE & GROW** / **MAINTAIN** / **INTERVENE** |

**Presenter note:** The quadrant determines engagement strategy. If this is the only thing someone reads, it should tell them how to approach this account.

---

### A3. Top 3 Signals

Auto-surfaced from the scoring component analysis. These are the three most anomalous, actionable, or time-sensitive signals for this account right now. Not a fixed list — the prompt selects whatever matters most.

**Signal selection logic:**
- Any scoring component in the top or bottom 10% of the portfolio
- Any metric with 3+ months of directional trend (improving or declining)
- Any binary flag (payment overdue, data stale >7 days)
- Any newly triggered expansion signal from the metrics framework Section 14
- **Operational callout:** If no Fathom meetings exist for this account AND no HubSpot account owner is assigned, surface as a signal: "No proactive engagement cadence on record — consider establishing structured outreach." This is a team recommendation, not an account health flag.

**Format:** Each signal in one sentence with the data point and the implication.

*Example outputs:*
- "MAU declining 3 consecutive months (72 → 64 → 58) — engagement decay, investigate cause"
- "3 new expansion signals triggered: No SmartPicks usage, High PDF + No Flipbook, Growing User Count"
- "Invoice 47 days overdue ($2,340) — financial flag, verify with accounting"
- "Fathom: competitor mentioned in last 2 calls (NuORDER) — competitive pressure signal"

---

### A4. Usage Pulse

One compact block showing engagement health at a glance.

| Metric | Source | Display |
|---|---|---|
| Active Users / Licensed Users | PostgreSQL `org_users`, `authenticated_sessions` | Ratio + percentage (e.g., "48/74 — 65%") |
| MAU Trend (3-month) | Mixpanel events | Arrow (↑ ↓ →) + values |
| Login Frequency | Mixpanel / PostgreSQL `login_events` | Avg logins per active user per month |
| Top 3 Features Used | Mixpanel events (highest event count) | Feature name + event count |
| Top 3 Features NOT Used | Mixpanel / PostgreSQL (enabled but zero events) | Feature name — highlights adoption gaps |
| Activity Ladder Summary | Mixpanel events | Levels active (e.g., "Levels 1-4 active, 5-6 unused") |

**For ordering clients, add:**

| Metric | Source | Display |
|---|---|---|
| Orders (period) | Admin Orders Report / PostgreSQL `orders` | Count + trend arrow |
| AOV | Admin Orders Report | Currency |
| Customer Activation Rate | PostgreSQL `customers` with orders / total | Percentage |

**For non-ordering clients, add:**

| Metric | Source | Display |
|---|---|---|
| Buyer-Facing Actions (period) | Mixpanel: Email Item Info + PDF Catalogs + Library Shares | Count + trend arrow |
| Customer Product Lists Created | Mixpanel / Admin Console CLM | Count |
| Catalog Engagement Depth | Mixpanel: searches, collection searches, filter/sort events | Summary count |

---

### A5. Recent Activity

The most recent signals only. Not comprehensive history — just enough to know the current state of the relationship and any active issues.

| Element | Source | Display |
|---|---|---|
| Last 2–3 HelpScout Tickets | BigQuery `helpscout__help_scout_tickets` | Subject + status (Open/Closed) + date. If tags available, include primary tag. |
| Last Fathom Call | BigQuery `fathom__ai_summaries` | Date + 1-line summary (extracted from AI summary) |
| Open HubSpot Deals | BigQuery `hubspot__deal` | Deal name + stage + amount (if any exist) |
| Days Since Last Interaction | Derived: most recent of Fathom call, HelpScout ticket, or HubSpot activity | Numeric — flags if >30 days |

---

### A6. Financial Status

Two lines maximum. Binary health check.

| Element | Source | Display |
|---|---|---|
| MRR | Stripe `subscription` | Currency |
| Payment Status | Stripe `invoice` / QuickBooks `invoice` | Current / Overdue (X days) |
| Last Invoice Date | Stripe `invoice` | Date |
| MRR Trend | Stripe `subscription` history | ↑ ↓ → (expanded, contracted, flat) |

---

### Snapshot Design Principles

1. **Everything fits on one screen.** If it scrolls, it's too long.
2. **Quadrant placement is the headline.** Visual hierarchy starts there.
3. **Signals over metrics.** Three interpreted signals beat twenty raw numbers.
4. **Recency over history.** Show what's happening now, not what happened six months ago.
5. **Use-case flex is automatic.** The prompt detects ordering vs. non-ordering and adjusts A4 accordingly.

---
---

## Version B: Account Intelligence Brief

**Purpose:** Answer "what do I need to know about this account?" in full depth.

**Audience:** Anyone on the team — CS, support, leadership, or someone new to the account. No meeting type or engagement context assumed.

**Generation:** On-demand via Cursor/MCP. Typically generated before any high-stakes or unfamiliar engagement, but usable as a standalone reference at any time.

**Length:** 3–5 pages depending on account complexity and data availability. Depth over density.

---

### B1. Account Identity & Context

The "who are these people and why are they our client" section. Static-ish information that changes infrequently, but essential for anyone unfamiliar with the account.

| Field | Source | Notes |
|---|---|---|
| Company Name | PostgreSQL `organizations` | — |
| Industry Segment | PostgreSQL `organizations` / HubSpot `company` | With brief industry context (e.g., "Lighting manufacturer, ~$85M revenue, national distribution") |
| Headquarters / Region | HubSpot `company` | — |
| Products Active | Stripe `subscription` / PostgreSQL `subscriptions` | Full module list with activation dates if available |
| Use-Case Profile | Derived | Ordering / Non-Ordering / Non-Ordering + Pushed Data — with explanation of what this means for this specific client |
| Partner Since | HubSpot `deal` (original close date) | Tenure + original deal context if available |
| Account Owner | HubSpot `owner` | Internal owner + any secondary contacts (support lead, etc.) |
| Contract & Billing | Stripe `subscription` + QuickBooks | MRR, billing frequency, payment terms |

**Relationship History Narrative** *(2–3 sentences, sourced from Fathom + HubSpot + institutional knowledge):*
How did they become a client? What was the original pain point? What's the arc of the relationship — has it expanded, contracted, or held steady? Any major milestones (added modules, key implementation, executive sponsor change)?

**Stakeholder Map:**

| Name | Role | Relationship to SuperCat | Last Interaction | Notes |
|---|---|---|---|---|
| *Populated from HubSpot contacts + Fathom attendees* | Title | Champion / Decision Maker / Technical Lead / End User | Date + channel (Fathom/HelpScout/email) | Key context: what they care about, communication style, influence level |

**Industry & Company Context** *(1–2 sentences, sourced from web search or institutional knowledge):*
Recent company news, market position, competitive landscape, trade show activity, strategic direction if known. This is the context that makes discovery questions feel specific rather than generic.

---

### B2. Account Scores — Full Component Breakdown

Both scores with every component visible. This is the analytical core of the document.

#### Expansion Readiness Score: [X/100] — [Band Label]

| Component | Weight | Score | Key Drivers |
|---|---|---|---|
| Adoption Depth | 30% | [X] | Activity Ladder levels active, Feature Breadth Score, Subscription Completeness (X/4 products), Active User Ratio |
| Business Impact | 25% | [X] | *Ordering:* Order volume trend, AOV, Customer Activation Rate, Self-Service Rate. *Non-ordering:* Buyer-facing action volume + trend, PDF catalogs, library sharing, Customer Product Lists |
| Growth Signals | 25% | [X] | User growth trend, MAU direction, new territories, expansion signals triggered, Fathom pain themes → unused features, open HubSpot expansion deals |
| Relationship Strength | 20% | [X] | Fathom meeting cadence, days since last interaction, stakeholder breadth, HelpScout responsiveness, onboarding ticket activity |

#### Retention Risk Score: [X/100] — [Band Label]

| Component | Weight | Score | Key Drivers |
|---|---|---|---|
| Engagement Decline | 30% | [X] | MAU trend (X months direction), login frequency trend, Active User Ratio change, user count change |
| Relationship Cooling | 25% | [X] | Fathom: days since last meeting, competitor mentions, negative themes. HelpScout: ticket silence from previously active account, unresolved tickets, wait time, billing/cancellation tags, thread depth |
| Financial Distress | 25% | [X] | Payment status, invoice aging, MRR trend (expansion/contraction/flat), order revenue trend (ordering clients) |
| Operational Deterioration | 20% | [X] | Data freshness (days since last import), import error rate, repeated support issues, inventory staleness |

#### Quadrant: [GROW / SAVE & GROW / MAINTAIN / INTERVENE]

*1–2 sentence interpretation of what the scores mean for this specific account.*

**Insufficient Data Flags:** *(list any components scored as N/A due to thin data — e.g., "Fathom: no meetings recorded in last 90 days — Relationship Strength and Relationship Cooling scored with redistributed weight")*

---

### B3. Rep Performance Intelligence

How the client's sales team uses the platform. Framed as behavioral intelligence, not adoption scoring.

| Element | Source | Notes |
|---|---|---|
| Total Reps / Active Reps | PostgreSQL `org_users` / Mixpanel | Licensed vs. actually using |
| Activity Ladder Results | Mixpanel events | Org-level summary: which levels are active, which are dark. Distribution of reps across levels |
| Power Users | Mixpanel (top 3 reps by composite activity) | Names + key metrics (logins, searches, emails drafted, orders if applicable) |
| Enablement Gaps | Mixpanel (bottom quartile reps) | Reps with logins but narrow feature usage — training candidates |
| Concentration Risk | Mixpanel / Admin Orders Report | Top rep's share of total activity or orders. If >50%, flag as bus factor risk |
| Feature Utilization Highlights | Mixpanel / Admin Console CLM | Top 5 features by usage, bottom 5 enabled-but-unused features |

**For ordering clients, add:**
- Orders per rep, AOV per rep, territory distribution
- Order type breakdown (Confirmed / Quote / HFC)
- Territory performance summary (top/bottom territories by revenue)

**For non-ordering clients, add:**
- Buyer-facing actions per rep (emails drafted, PDFs created, library shares, customer product lists)
- Catalog engagement depth per rep (searches, collection searches, filter/sort)
- Maybe List conversion rate (if applicable)

---

### B4. Customer Intelligence

What the platform reveals about the client's customer base and buyer behavior.

| Element | Source | Notes |
|---|---|---|
| Total Customers in System | PostgreSQL `customers` | Scale of the customer database |
| Customer Activation Rate | Derived: customers with orders or engagement / total | For ordering: customers ordering. For non-ordering: customers selected/searched by reps |
| Inactive Buyer Flags | Derived: customers with historical activity but none in last 30/60/90 days | Tiered by dormancy period |
| Reorder Gap Analysis | Derived: products historically purchased by customer but not reordered in 6–8 weeks | If data available — strongest for ordering clients |
| Self-Service Adoption | PostgreSQL / Mixpanel: eCat Online customer logins | Buyer self-service readiness |
| Customer Concentration | Admin Orders Report | Top customer's share of total orders/revenue — dependency risk |
| Territory Coverage | Admin Orders Report / PostgreSQL `territories` | Territories with orders vs. total territories configured — identifies dormant territories |

---

### B5. Relationship & Support History

The full picture of the relationship — both proactive (our outreach) and reactive (their inbound).

#### Fathom — Meeting Intelligence (Last 90 Days)

| Element | Source |
|---|---|
| Meeting Count | BigQuery `fathom__ai_summaries` |
| Meeting Cadence | Derived: average days between meetings |
| Last Meeting Date + Attendees | `fathom__ai_summaries` |
| Pain Themes (recurring) | `fathom__sales_meetings_from_fathom_hubspot` — MEDDIC Pain field |
| Action Items (open) | `fathom__ai_summaries` — extracted next steps from most recent calls |
| Competitor Mentions | `fathom__sales_meetings_from_fathom_hubspot` — Competitors field |
| Objections Raised | `fathom__sales_meetings_from_fathom_hubspot` — Objections field |
| Sentiment Summary | Derived from pain themes + objections + overall tone of recent summaries |

*For each of the last 2–3 calls, include: date, attendees, 2–3 sentence summary, key action items.*

#### HelpScout — Support & Onboarding (Last 90 Days)

| Element | Source |
|---|---|
| Ticket Volume (90d) | BigQuery `helpscout__help_scout_tickets` |
| Ticket Volume Trend | Derived: current 90d vs. prior 90d |
| Open Tickets | `helpscout__help_scout_tickets` where status = open/pending |
| Recurring Themes | Derived from `ticket_subject` + `ticket_tags` clustering |
| Avg Customer Wait Time | `ticket_customer_waiting_secs` |
| Escalations | Tickets with high thread depth or reassignment patterns |
| Recent Tickets (last 3–5) | Subject + status + date + assignee + primary tag |

#### Combined Relationship Signals

| Signal | Source | Interpretation |
|---|---|---|
| Days Since Last Touchpoint | Most recent of: Fathom call, HelpScout ticket, HubSpot activity | >30 days = note for awareness (not an automatic risk flag — context matters) |
| Communication Direction | Ratio of inbound (HelpScout) to outbound (Fathom) | All inbound + no outbound = operational callout: "Consider establishing proactive cadence." This is a team recommendation, not an account health flag. |
| Stakeholder Breadth | Distinct contacts across Fathom + HelpScout | Single-threaded (1 contact) = champion dependency risk |

**Fathom / HelpScout Absence Protocol:**
- If Fathom has zero meetings for this account: populate the Fathom subsection with "No proactive meeting history on record" and a recommendation to establish a cadence. Do NOT frame as a gap, risk, or health issue.
- If HelpScout has zero or very few tickets for a high-engagement account: this is a positive signal (self-sufficient, well-implemented). Note the low ticket volume as a strength, not a concern.
- Fathom CESSATION (meetings were happening regularly, then stopped) and HelpScout PATTERN CHANGE (established cadence dropped off) ARE meaningful signals and should be surfaced with context.

---

### B6. Expansion Whitespace

Concrete growth opportunities with business context.

| Element | Source | Notes |
|---|---|---|
| Unused Modules | Stripe `subscription` vs. full product suite | List each missing module + list price + what it would give them |
| Triggered Expansion Signals | Metrics framework Section 14 | Only signals that are currently active for this account, with the specific detection data |
| Peer Benchmarking | Aggregated internal data (129 orgs) | "Companies like you in [segment] with similar rep count typically also leverage [feature/module]" — framed as peer context, not pressure |
| Feature Adoption Gaps | Mixpanel: features enabled but unused or underused vs. segment median | Specific features with the business case for adoption |
| Seat Expansion Headroom | PostgreSQL `org_users`: billable vs. licensed vs. total potential | If the client's sales force is larger than their licensed count |

---

### B7. Open Risks & Issues

The honest "what could go wrong" section. Everything that needs attention or monitoring.

| Element | Source | Notes |
|---|---|---|
| Unresolved Support Tickets | HelpScout: open tickets with age + priority | Sorted by age (oldest first) |
| Stalled HubSpot Deals | HubSpot: deals unchanged >30 days | Deal name + stage + days stalled |
| Financial Flags | Stripe/QuickBooks: overdue invoices, MRR contraction | Specific amounts and timelines |
| Operational Flags | PostgreSQL: stale data (>7 days), import errors, integration failures | Specific data types affected |
| Relationship Flags | Fathom: competitor mentions, champion silence, missed meetings | With dates and context |
| Concentration Risk | Mixpanel / Admin Orders Report: single rep or customer dependency | Specific names and percentages |

---

### B8. Context & Preparation *(Optional — Only Generated When Context Is Specified)*

This section is NOT part of the default brief. It generates only when the user provides a specific engagement context in the prompt (e.g., "EBR next Tuesday," "CEO meeting about product feedback," "support call about implementation issues").

When generated, this section contains:

| Element | Logic |
|---|---|
| Engagement Objective(s) | 2–3 suggested objectives based on the brief data + the stated context |
| Key Data Points to Surface | The 3–5 most relevant metrics/findings from the brief for this specific engagement |
| Topics to Explore | Questions or discussion areas informed by the data |
| Topics to Handle Carefully | Sensitive areas based on open risks, relationship flags, or recent friction |
| Commitments from Prior Engagement | Last Fathom call action items, last HelpScout resolution promises |

**Context-specific adaptations:**

| If context is... | Section emphasizes... |
|---|---|
| EBR / QBR | Scoring detail, rep intelligence, expansion whitespace, peer benchmarking |
| Product feedback meeting | HelpScout feature request themes, Fathom product-related pain themes, Jira tickets related to their requests |
| Renewal conversation | Financial status, retention risk components, relationship strength, delivered value narrative |
| Support / implementation | Data health, integration status, open tickets, technical config, onboarding progress |
| Executive briefing | Identity context, relationship arc, quadrant placement, top 3 signals, financial status |
| New team member handoff | Everything — the full brief IS the handoff document |

---

### Intelligence Brief Design Principles

1. **Context-neutral by default.** The body of the document makes no assumptions about why you're reading it. It's a factual intelligence reference.
2. **Scoring is the spine.** The quadrant placement and component breakdown frame every other section — they tell you what to pay attention to and why.
3. **Data-sourced, not opinion-based.** Every element traces to a specific data source. The brief reports what the data shows. Interpretation happens in the scoring model and the optional Context section.
4. **Use-case flex is silent.** The prompt detects ordering vs. non-ordering and adjusts B3, B4, and the Business Impact scoring component automatically. The reader doesn't need to know which version they're looking at.
5. **Insufficient data is surfaced, not hidden.** If Fathom has no meetings or HelpScout has no tickets, the brief says so explicitly. However, absence of Fathom/HelpScout data is framed as an operational callout ("consider establishing proactive cadence"), NOT as a health or risk signal. Self-sufficient, well-implemented clients are not penalized for not needing meetings or support. Only pattern CHANGES (meetings that stopped, ticket cadence that dropped off) are surfaced as meaningful signals.
6. **The optional Context section is the only subjective layer.** Everything above it is factual. The Context section is where the brief becomes a talk track — and it only appears when asked for.

---

## Appendix: Data Source Quick Reference

| Data Need | Primary Source | Secondary Source |
|---|---|---|
| Account identity & config | PostgreSQL `organizations`, `org_users`, `subscriptions` | HubSpot `company` |
| Stakeholder contacts | HubSpot `contact` | Fathom `ai_summaries` (attendees) |
| Subscription & billing | Stripe `subscription`, `invoice` | QuickBooks `invoice` |
| Product usage & engagement | Mixpanel `events` | Admin Console CLM export |
| Rep-level behavior | Mixpanel `events` | Admin Console CLM export |
| Orders & revenue | PostgreSQL `orders`, `portal_orders` | Admin Orders Report, Stripe |
| Customer data | PostgreSQL `customers`, `customer_favorites` | Mixpanel (customer-selection events) |
| Territory config | PostgreSQL `territories` | Admin Orders Report |
| Support tickets | BigQuery `helpscout__help_scout_tickets` | `helpscout__conversation_threads` |
| Meeting intelligence | BigQuery `fathom__ai_summaries` | `fathom__sales_meetings_from_fathom_hubspot` |
| Pipeline & deals | BigQuery `hubspot__deal` | `hubspot__engagement` |
| Data health & imports | PostgreSQL `import_events`, `data_versions` | `audit_log_entries` |
| Financial health | Stripe `invoice`, `charge`, `subscription` | QuickBooks `invoice`, `payment` |
| Benchmarking | Aggregated internal (129 orgs) | Mixpanel `org_feature_usage_report` |

---

**Version:** 1.0 | **Date:** Feb 26, 2026 | **Author:** Kylor Johnson
