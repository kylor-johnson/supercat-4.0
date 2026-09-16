# Section Guide: §6 — Portal Engagement
> **v1.0** — validated 2026-04-17 (RENWIL run). Last updated: 2026-04-17.

## Section Identity
- **id**: `portal`
- **title**: Portal Engagement
- **section number**: 6
- **include when**: `HAS_CLICKY = true` ONLY
- **skip when**: `HAS_CLICKY = false` — skip entirely. No placeholder. No mention of Clicky, portal analytics, portal traffic, or Private Storefront anywhere in the report.

## Query Inputs

Read these cache files:
- `cache/Q-CL-01_results.md` — Portal traffic health and monthly trend
- `cache/Q-CL-03_results.md` — Geographic portal demand
- `cache/Q-CL-05_results.md` — Traffic sources
- `cache/gate_flags.md` — for `HAS_CLICKY`, `CLICKY_PREFIX`

## Subsection Order (do not reorder — render every subsection whose gate is met)

### 1. Traffic Health (Q-CL-01)

Build from `Q-CL-01_results.md`. Surface current portal traffic health — visitors, pageviews, session duration.

### 2. Monthly Traffic Trend (Q-CL-01)

Build from `Q-CL-01_results.md`. Surface the monthly trend of portal traffic over the reporting period.

### 3. Geographic Demand (Q-CL-03)

Build from `Q-CL-03_results.md`. Surface geographic distribution of portal traffic.

`[COLLAPSE]`

### 4. Traffic Sources (Q-CL-05)

Build from `Q-CL-05_results.md`. Surface where portal traffic originates (direct, search, referral, etc.).

If Q-CL-05 shows 100% direct traffic (single source with no meaningful breakdown), omit this subsection silently — it adds no analytical value for closed portals. `[COLLAPSE]`

## Section-Specific Rules

- **VM-36 prohibition**: Do not surface VM-36 (portal traffic decline as a churn signal) externally. Portal traffic trend is descriptive — let the client draw their own conclusions about what the numbers mean for their business.
- **Clicky naming**: The word "Clicky" must never appear in delivered HTML. Reference the data as portal traffic or portal analytics — the Forbidden Phrases list in `shared_rules.md` applies.
- One `what-this-means` per subsection maximum. Do not add duplicate close blocks within the same subsection.
