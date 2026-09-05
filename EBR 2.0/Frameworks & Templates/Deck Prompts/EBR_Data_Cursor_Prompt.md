# Cursor Prompt: EBR Data Layer — Inputs, Logic & Contextual Intelligence
## SuperCat / eCat · Data Update & Enrichment Pass

---

## Purpose

This prompt governs the **data layer** of the EBR deck. The design system, slide structure, and HTML architecture are already defined in `EBR_Cursor_Prompt.md`. This prompt focuses exclusively on:

1. What data fields are required and where they map
2. How to handle seasonality and market calendar context
3. What logic governs calculations, thresholds, and risk flags
4. What to display vs. suppress based on data availability
5. What is stubbed vs. live vs. deferred to a separate data pipeline

---

## Critical Principle: Seasonality Is Not a Footnote — It Is the Frame

This account operates in the **outdoor / luxury furniture industry**. Sales activity, order volume, platform usage, and rep behavior are **not linear** — they spike dramatically around trade market events. Any metric involving period-over-period change (growth %, volume deltas, rep activity) **must be interpreted through the market calendar lens**, not presented as raw MoM or arbitrary date range comparisons.

### The Market Calendar

Flag the following events inline wherever period comparisons appear. Priority 1 events drive the largest platform activity spikes and must always be called out explicitly.

```
PRIORITY 1 (highest activity impact — always flag):
- Atlanta Market:             Jan 13–19, 2026 | Jul 14–20, 2026
- Dallas Total Home & Gift:   Jan 7–13, 2026  | Jun 24–30, 2026
- Artisan Resource @ NY NOW:  Feb 1–3, 2026   | Aug 2–4, 2026
- NeoCon:                     Jun 8–10, 2026
- High Point Market (Fall):   Oct 17–21, 2026
- Furniture Today:            December 2026

STANDARD (notable but secondary):
- Las Vegas Market:           Jan 25–29, 2026 | Jul 26–30, 2026
- High Point Market (Spring): Apr 25–29, 2026
- ICFF:                       May 17–19, 2026
- LightFair:                  May 2026
- BDNY:                       Nov 8–9, 2026
```

### How to Apply the Calendar

**In ALL period-over-period comparisons:**
- Always check whether the comparison window overlaps with a Priority 1 market event
- If a spike is present and coincides with a market event, label it: `[Atlanta Market]` or `[Market-Driven]`
- If a dip is present and the prior period contained a Priority 1 event, note: `[Post-Market Normalization]`
- Never present MoM change without this context — it misleads

**In TTM framing:**
- TTM is the preferred window for all revenue and order metrics
- For sub-TTM trend lines or recent period comparisons, always anchor to the nearest market event
- Example: "Feb revenue reflects Atlanta Market (Jan 13–19) and Artisan Resource (Feb 1–3) activity"
- Never label a growth figure as structural vs. seasonal without flagging that the determination requires multi-year TTM comparison

**In rep performance:**
- Market weeks inflate logins, product searches, and presentation activity significantly
- Rep output during market weeks is not comparable to off-market weeks
- When analyzing high/low performer gaps, note whether the observation window included market weeks

**In feature adoption:**
- Platform events like "Product Search", "Kit View", and "Camera Scan" will spike during market prep and market weeks
- Aggregate TTM figures mask this — wherever possible, note whether figures are market-weighted

---

## Data Inputs Required Per Slide

### Slide 2 — Industry & Company Context (Stub → Live)

**Source: HubSpot + Manual Input**

| Field | Source | Notes |
|-------|--------|-------|
| Industry & segment description | Manual / HubSpot Company record | 1–2 sentences |
| SuperCat Fit Score | HubSpot custom property | Numeric or tier (Low/Mid/High) |
| Recent engagement summary | HubSpot Activities + HelpScout | Last 90 days: calls, emails, tickets |
| Strategic context / initiatives | Manual — AE notes | What they told you matters this year |
| Account score narrative | Derived from B2 scoring model | 1–2 sentences translating inputs |
| Instance health summary | eCat data export | Setup completeness, data freshness |

**Display rule:** If HubSpot data is unavailable, render the stub with clearly labeled placeholder fields. Never invent context.

---

### Slide 3 — Partnership Overview

**Required fields (per entity):**

| Field | Label in deck | Notes |
|-------|--------------|-------|
| Entity display name | Card header | e.g. "SC Retail" |
| Entity code | Tag line | e.g. "SCW · Retail / DTC" |
| Licensed user count | "Users" row numerator | Total licenses allocated |
| Active user count | "Users" row denominator | Active = logged in within TTM |
| TTM order count | "Orders (TTM)" | Confirmed + submitted |
| TTM revenue | "Revenue (TTM)" | Confirmed orders only |

**Account-level stat row:**
- Entities: count of divisions
- Active Users: sum across all entities (deduplicated if reps appear in multiple)
- Orders (TTM): sum across all entities
- Revenue (TTM): sum across all entities

---

### Slide 6 — Platform Impact

**Required fields:**

| Field | Label | Notes |
|-------|-------|-------|
| TTM total revenue | Hero stat | Sum of confirmed revenue |
| TTM total transactions | Hero stat | All confirmed + submitted orders |
| Active user count | Hero stat | Deduplicated across entities |
| Adoption rate | Hero stat | Active / Licensed × 100 |
| Total login events (TTM) | Insight line | |
| Total product search events (TTM) | Insight line | |
| Total configured items (TTM) | Insight line | |
| Notable single-month revenue | Insight line | Call out peak month + link to market event |

**Market calendar note:** The insight line should explicitly name the market event(s) driving any notable single-month figure. Example: "February alone ($18.5M) — driven by Atlanta Market (Jan 13–19) trailing activity and Artisan Resource (Feb 1–3)."

---

### Slide 7 — Entity Performance + Growth

**Cross-entity table fields (per entity):**

| Field | Label | Notes |
|-------|-------|-------|
| TTM order count | Orders (TTM) | |
| TTM revenue | Revenue (TTM) | |
| Average order value | AOV | Revenue / Orders |
| Recent period growth % | Recent Growth | See growth calculation rules below |
| Self-service % | Self-Service % | Self-service orders / total orders |

**Growth card fields (per growing entity):**
- Period label (e.g. "Jan → Feb")
- Prior period revenue
- Current period revenue
- Absolute delta

**Growth calculation rules:**
- Default to most recent full month vs. prior full month
- If either month overlaps a Priority 1 market event: add `[Market-Driven]` tag and a footnote
- If the prior period contained a market event and the current does not: label `[Post-Market Normalization]` — do not present as a decline without this context
- Never show MoM growth as the headline without a TTM reference point alongside it

**Self-service %:**
- Only show for B2B entities (Wholesale, Contract) — not applicable to Retail/DTC
- Show as N/A for Retail with a brief note

---

### Slide 8 — Sales Team Intelligence

**Section A: Adoption table (per entity)**

Same fields as Partnership Overview plus:
- Revenue per active user (derived: Revenue / Active Users)

**Section B: Power Users — REVISED APPROACH**

Do NOT show a division-by-division breakdown. Instead:

Show a **single cross-entity leaderboard** of top performers ranked by total platform contribution. Each row = one unique rep (not one rep-entity pair).

| Field | Label | Notes |
|-------|-------|-------|
| Rep full name | Rep | |
| Total TTM orders (all entities combined) | Total Orders | |
| Total TTM revenue (all entities combined) | Total Revenue | |
| Number of entities active in | Entities | e.g. "2 of 4" |
| Feature breadth score | Breadth | See breadth definition below |
| Most recent active date | Last Active | |

**Breadth — definition and display:**
Breadth = the count of **distinct feature types** a rep has used at least once in the TTM window. Feature types are the named platform capabilities (Product Search, Kit View, Order Kit, Camera Scan, PDF Catalog, Sales Portal, SmartPicks, Config Items, Customer Lists, Submit Order, Show Sales, Maybe List). Maximum possible = 12.

Display as: `9 / 12` or with a brief tooltip/footnote: "Breadth = distinct platform features used (TTM). Max: 12."

**Section C: Rep Concentration Risk**

One card per entity showing:
- Entity name
- Top rep name
- Top rep % of entity's total TTM orders
- Risk level

**Concentration % definition:** Top rep's TTM order count ÷ entity total TTM order count × 100.

**20% threshold — rationale to display in deck:**
> "The 20% threshold is a continuity heuristic: if a single rep accounts for more than 1-in-5 orders and leaves, is reassigned, or goes on extended leave, the entity faces a structural throughput risk. It is not a performance concern — it is a succession and coverage planning signal."

**Risk levels:**
- < 10%: Low Risk (green)
- 10–19%: Moderate (gold)
- ≥ 20%: High Risk (red)

**Ben Erickson / SC Contract at 0% — explanation to show:**
> "SC Contract's orders are distributed across reps with no single rep dominating — Ben Erickson is listed as the top rep by a narrow margin. 0% here reflects rounding or near-equal distribution, not an absence of orders. Contract's small licensed team (29 reps) and high per-order AOV ($15K+) make even small concentrations meaningful — watch as the dataset grows."

---

### Slide 9 — Feature Intelligence

**Heavy Adoption column — display rules:**
- Show any feature with TTM event count > 1,000 across all entities combined
- Rank by volume descending

**Zero / Near-Zero column — CRITICAL RULE:**
- **Only show features that are:**
  1. Turned ON for at least one entity, AND
  2. Have near-zero or zero usage despite being available

- **Do NOT show:**
  - Features that are not activated / not part of their product tier
  - Features like "View Placements" or "View Commitments" if those modules are not enabled — showing a zero for a feature they don't have is meaningless and confusing

- **Annotation rule:** For any near-zero feature, add a brief reason column or footnote: "Available but unused" vs. "Not activated" vs. "Limited to specific workflow"

**Feature benchmarking table — color logic:**
Current implementation uses arbitrary green shading. Replace with rational heat-mapping:

- For each feature row, find the maximum value across all entities
- Color intensity = entity value / row maximum
- Scale: 0% → white, 100% → full green (`rgba(74,124,89,.25)`)
- Exception: if all entities show zero for a feature, shade all cells red (`rgba(196,93,93,.07)`)
- The Leader column shows the entity with the max value for that row
- If all entities are near-zero (< 100 events), suppress the Leader column entry and show `—`

---

### Slide 10 — Customer Intelligence

**Top Concentration — definition to display:**
> "Top Concentration = the single largest customer's confirmed order revenue as a % of that entity's total TTM confirmed revenue. This flags customer dependency — not a negative signal on its own, but a continuity and diversification consideration."

Show the actual customer name and dollar amount in the callout card, not just the percentage.

---

### Slide 11 — Data-Anchored Discovery

**Market calendar linkage:**
- Question referencing a growth figure must name the specific market event(s) in the question
- Example: "SC Retail nearly doubled in February — that window overlaps with Atlanta Market activity. Is that pattern consistent year-over-year, or was February unusually strong?"

---

### Slide 12 — Growth Opportunities + Cross-Entity Playbook

**Market calendar rule:**
- Any recommendation that touches volume, timing, or rep activation must acknowledge market seasonality
- Example: if recommending a new feature rollout, note the best window relative to the market calendar — e.g., "Recommend activating SmartPicks before High Point (Oct 17) so reps can use it during market prep"

---

### Slide 13 — Feature Roadmap

**Suppression rule:** Same as Slide 9 — do not list features as "Not Started" if they are not part of the account's product tier. Only show features that are available and unused.

---

### Slide 14 — Housekeeping + Next Steps

**These fields require actual data — do not leave generic:**

| Field | Required Input | Source |
|-------|---------------|--------|
| Open Tickets | Count + most recent ticket summary | HelpScout |
| Payment Status | Current / Overdue + days outstanding if applicable | Billing system |
| Data & Platform Health | Last data sync date, eCat version per entity, any import errors | eCat admin |
| Engagement Cadence | Last EBR date, last QBR, last check-in | HubSpot |

If live data is unavailable at generation time, render as stub fields — never fabricate status.

---

## Data Quality & Suppression Rules (Global)

These apply everywhere in the deck:

### 1. Feature suppression
Never show a zero-usage stat for a feature that is not enabled for that entity. Showing "Flipbook: 0" when Flipbook doesn't exist is actively misleading. Check feature activation status before rendering any feature row.

### 2. Period labeling
- All time-period labels must be explicit: TTM, Recent Period (Jan–Feb 2026), or a named window
- Never show unlabeled percentages or deltas
- Whenever a comparison window overlaps a Priority 1 market event, add a market flag

### 3. Derived metrics transparency
- AOV: always show the formula footnote on first use — "AOV = Confirmed Revenue ÷ Confirmed Orders"
- Breadth: define on first use — see Slide 8 rules above
- Concentration %: define on first use — see Slide 10 rules above
- Adoption rate: define on first use — "Active Users ÷ Licensed Users"

### 4. Multi-entity rep deduplication
- When a rep appears in multiple entities, their cross-entity total is the SUM across entities
- When showing "Active Users" at the account level, deduplicate — a rep active in 2 entities = 1 unique user
- Clearly label when you are showing deduplicated vs. entity-level counts

### 5. Market-weighted interpretation
- If a spike or dip can be explained by a Priority 1 market event, say so explicitly
- Do not allow the deck to imply structural growth or structural decline without acknowledging seasonality
- Pattern recognition > single data point; delta over a comparable period > raw MoM

---

## Deferred Data Dependencies (Separate Pipeline)

The following items are **not** part of this data update pass. They are documented here so the prompt is complete, but they require separate data sources or models to implement.

| Item | What's needed | Dependency |
|------|--------------|------------|
| Rep performance through 6 activities | Definition of the 6 activity types + per-rep event data by activity | eCat activity schema |
| Low/mid/high performer cohort analysis | Cohort thresholds + rep-level TTM activity data | Rep segmentation model |
| Account scores (B2) | Adoption depth score, business impact score, growth signal score | B2 scoring model |
| Instance health detail | eCat version, iOS mix, order pipeline, import errors per entity | eCat admin API |
| HubSpot SuperCat Fit | Fit score + company profile fields | HubSpot integration |
| Recent engagement narrative | Last 90-day HubSpot + HelpScout activity log | HubSpot/HelpScout API |
| Account score → narrative translation | Score inputs → 1–2 sentence summary | Scoring model output |
| TTM trend chart | Monthly revenue by entity over 12 months | Time-series data |
| B2B commerce funnel | Quotes → confirmed → self-service funnel by entity | eCat funnel data |

---

## Output Quality Checklist (Data Pass)

Before delivering, verify:

- [ ] No "YTD" anywhere — TTM or named windows only
- [ ] Every growth % has a market calendar flag if the window overlaps a Priority 1 event
- [ ] No zero-usage features shown for features that aren't activated
- [ ] Breadth is defined on first use with max denominator shown
- [ ] Top Concentration is defined on first use with customer name + dollar amount
- [ ] 20% concentration threshold has rationale text visible in the deck
- [ ] Ben Erickson / SC Contract 0% has explanatory note
- [ ] Feature benchmarking color scale is rationally heat-mapped (not arbitrary)
- [ ] Power Users section shows cross-entity leaderboard, not division-by-division
- [ ] Housekeeping slide has actual data fields, not placeholder status text
- [ ] All deferred items are clearly stubbed, not fabricated
- [ ] Market calendar is referenced at least once in the Growth slide, Discovery slide, and Recommendations slide
