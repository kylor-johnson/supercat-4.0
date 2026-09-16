# Section Guide: §6 — Demand Signal Intelligence
> **v3.0** — reframed 2026-06-16. Previous: v2.0 "Portal Engagement" (traffic-metrics framing).

## Section Identity
- **id**: `portal`
- **title**: Demand Signal Intelligence
- **section number**: 6
- **include when**: `HAS_CLICKY = true` ONLY
- **skip when**: `HAS_CLICKY = false` — skip entirely. No placeholder. No mention of Clicky, portal analytics, portal traffic, or Private Storefront anywhere in the report.

## Query Inputs

Read these cache files:
- `cache/Q-CL-01_results.md` — Portal traffic health and monthly trend
- `cache/Q-CL-03_results.md` — Geographic portal demand
- `cache/Q-CL-05_results.md` — Traffic sources
- `cache/gate_flags.md` — for `HAS_CLICKY`, `CLICKY_PREFIX`

## Quality Floor

Every subsection whose gate is met **must** contain all of the following:

1. A **`.prose` analytical paragraph** (2–4 sentences minimum) that interprets the data — not just restates numbers. Speak as a smart analyst to a VP: compare periods, call out anomalies, frame magnitudes in context.
2. A **`.metrics-grid`** with `metric-card` elements for headline numbers (include `.metric-note` with time qualifier).
3. A **`<div class="what-this-means">`** closing block (1–3 sentences, actionable implication). Do not duplicate the prose paragraph — the what-this-means block tells the client *what to do about it* or *why it matters strategically*, not what the numbers are.

If a subsection has a table, the `.prose` paragraph must appear **above** the table and interpret highlights — do not let the table speak for itself.

Where a notable pattern exists (growth spike, seasonal anomaly, engagement outlier), add a **`.callout.insight`** block with a descriptive `.callout-title` and 1–2 sentences of context.

## Subsection Order (do not reorder — render every subsection whose gate is met)

### 1. Engagement Depth & Demand Signals (Q-CL-01)

Build from `Q-CL-01_results.md`.

**Framing principle**: Lead with engagement quality (session duration, pages per session), NOT visitor count. For B2B portals, 10 highly engaged visitors researching products for 5+ minutes are more valuable than 1,000 bounce-and-leave visits. Frame anonymous traffic as qualified pipeline — these are companies actively researching the client's products.

**Required content:**
- Metrics grid: **average session duration** (mm:ss format) as the lead metric, **pages per session** (total pageviews / total sessions), current-month unique visitors (as supporting context, not headline). Include time qualifier in `.metric-note`.
- Prose paragraph: lead with engagement depth framing — "X unique companies spent an average of Y minutes researching your products this month." Characterize what the session duration and pages-per-session signal about buyer intent (e.g., "5+ minute sessions with 3+ pages indicate active product evaluation, not casual browsing"). Compare to B2B portal norms if the data supports it (sessions >3 minutes are strong engagement for B2B).
- Frame the daily visitor count as a supporting metric, not the headline. For small counts (≤20/day), use framing like "a concentrated audience of serious buyers" rather than leading with the raw number.
- If the current month's engagement metrics differ from the trailing-period average by ≥15%, note the direction and magnitude.
- What-this-means: frame the engagement as a demand signal — "These visitors are actively researching your products. The depth of engagement suggests purchase intent, not casual browsing." If session durations are strong, suggest exploring ways to connect portal research to downstream ordering behavior.

### 2. Research Activity Trend (Q-CL-01)

Build from `Q-CL-01_results.md`.

**Required content:**
- Prose paragraph above the table: frame as "product research activity over time" rather than "traffic trend." Summarize whether research activity is growing, stable, or declining. Call out the highest and lowest months. If any month's engagement metrics deviate ≥25% from the period average, note the anomaly and hypothesize about what drove it (market event, catalog update, seasonal demand).
- Table: Month | Avg Session Duration | Pages/Session | Unique Visitors | Total Pageviews. Show all available months, most recent first. Session duration and pages/session are the lead columns.
- If a clear growth or decline trend exists (≥20% change from first to last month in either visitors or engagement depth), add a `.callout.insight` block framing the change as demand acceleration or deceleration — not just traffic.
- What-this-means: connect the trend to business context — does the trajectory suggest growing product interest, seasonal demand patterns, or the impact of catalog updates? Frame as actionable intelligence: "Research activity peaked in [month] — does this align with your ordering patterns?"

### 3. Geographic Demand (Q-CL-03)

Build from `Q-CL-03_results.md`.

**Gate**: Render unless Q-CL-03 data is absent or contains only a single unidentified region.

`[COLLAPSE]`

**Required content:**
- Prose paragraph: how many regions are represented? Where does traffic concentrate? Do the top regions align with the client's known sales territories or market presence?
- Table: top 5 regions by visitor count (Region | Visitors, trailing period). If more than 5 regions, place the next 5 in a collapsed `<details>` block.
- If the top 3 regions account for ≥50% of identified traffic, note the concentration.
- If any non-domestic region appears in the top 10 (e.g., Canada, Vietnam), note international interest.
- What-this-means: frame geographic patterns as market signal — does the traffic map match the client's sales footprint? Are there under-represented territories that suggest untapped portal awareness?

### 4. Traffic Sources (Q-CL-05)

Build from `Q-CL-05_results.md`.

**Gate**: If Q-CL-05 shows 100% direct traffic (single source with no meaningful breakdown), omit this subsection silently — it adds no analytical value for closed portals.

`[COLLAPSE]`

**Required content** (when rendered):
- Prose paragraph: characterize the source mix — is this a credentialed portal (expect high direct %) or public-facing (expect more search/social)? Frame the non-direct traffic as incremental discovery.
- Table: Source | Visitors (trailing period) | Share (%). Show all sources.
- If direct traffic is ≥90%, note that this is expected for a credentialed portal but still call out any non-trivial search or referral traffic.
- If search traffic is ≥5%, note the organic discoverability.
- What-this-means: practical implications — could SEO, advertising, or social channels broaden reach? Is the current source mix healthy for the portal's intended role?

## DOES NOT COVER (hard boundaries)

This section does NOT produce:
1. eCat ordering, commerce trends, or capture rate analysis → belongs in §5 Commerce Analytics
2. Rep-level performance, coaching, or behavioral analysis → belongs in §2 Sales Team Performance
3. Customer-level activation, penetration, or dormancy analysis → belongs in §3 Customer & Buyer Intelligence
4. Product catalog health, inventory, or sales-line analysis → belongs in §4 Product & Inventory
5. Peer benchmarking or cohort comparisons → belongs in §7 Peer Benchmarking
6. Platform feature utilization or data freshness → belongs in §8 Platform & Feature
7. Health score, churn risk, or expansion signals → internal only (GUARDRAILS.md §5)
8. VM-36 (portal traffic decline as churn signal) → internal only

Read: `GUARDRAILS.md` for the full query ownership table (§8) and rule set.

---

## Section-Specific Rules

- **VM-36 prohibition**: Do not surface VM-36 (portal traffic decline as a churn signal) externally. Portal traffic trend is descriptive — let the client draw their own conclusions about what the numbers mean for their business.
- **Clicky naming**: The word "Clicky" must never appear in delivered HTML. Reference the data as portal traffic or portal analytics — the Forbidden Phrases list in `shared_rules.md` applies.
- One `what-this-means` per subsection maximum. Do not add duplicate close blocks within the same subsection.
- **section-sub one-liner**: Lead with engagement depth, not visitor count (e.g., "5:35 avg session · 3.2 pages/visit · ~48 daily researchers · 44,929 pageviews (7 months)"). Do not use generic descriptions.
- **section-contents**: Must list every rendered subsection name, `&middot;`-separated. Use updated names: "Engagement Depth & Demand Signals · Research Activity Trend · Geographic Demand · Traffic Sources". If Geographic Demand or Traffic Sources are omitted due to their gate, exclude them from this list.
