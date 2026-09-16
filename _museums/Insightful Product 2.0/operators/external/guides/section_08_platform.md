# Section Guide: §8 — Platform & Feature Utilization
> **v2.0** — hardened 2026-06-16. Previous: v1.0 (unversioned, validated 2026-04-17).

## Section Identity
- **id**: `platform`
- **title**: Platform & Feature Utilization
- **section number**: 8
- **include when**: Always
- **skip when**: Never — this section is always rendered

## Query Inputs

Read these cache files:
- `cache/Q-07_results.md` — Catalog completeness (shared with §4)
- `cache/Q-08_results.md` — Data freshness per entity type
- `cache/Q-09_results.md` — Import pipeline health
- `cache/Q-10_results.md` — Catalog health
- `cache/Q-11_results.md` — Configuration completeness / alerts
- `cache/Q-22_results.md` — Feature usage depth
- `cache/Q-46_results.md` — **conditional**: eCat selling workflow maturity (submit-through rate). Only present when Mixpanel coverage exists. If absent, omit workflow maturity context from §8.2 — do not mention the metric or leave a placeholder.
- `cache/Q-47_results.md` — **conditional**: Smart stack effectiveness (per-stack metadata, staleness). If absent, build §8.6 from Q-10 smart stack count only.
- `cache/Q-50_results.md` — **conditional**: Library / document engagement (document inventory, staleness). If absent, omit library analysis from §8.1 — do not mention documents or leave a placeholder.
- `cache/gate_flags.md` — for org identity, feature flags, `MIXPANEL_ORDER_TRACKING_GAP`, and `USER_GROUP_SPLIT_AVAILABLE`
- `cache/user_group_mapping.md` — **conditional read**: only if `USER_GROUP_SPLIT_AVAILABLE = true` in `gate_flags.md`. Contains the aggregate activity split between field reps and showroom/operational accounts.

**Mixpanel Order-Tracking Gap**: If `MIXPANEL_ORDER_TRACKING_GAP = true` in `gate_flags.md`, Mixpanel is not tracking iPad order submissions for this org. Apply all of the following:

1. **Remove the "Order Submission" row** from the Q-22 Feature Usage table entirely. Do not display "0" — the zero is a tracking artifact, not a usage signal.
2. **Do not write narrative** that frames order submission as absent, missing, unused, or a gap. This includes Feature Usage Intensity prose, `what-this-means` blocks, and the `section-sub` stat line.
3. **Do not characterize the platform** as non-transactional or presentation-only when the gap flag is set. If historical Postgres orders exist, ordering activity has occurred — Mixpanel instrumentation was not active for that workflow.
4. **Neutral replacement** (only if the section would otherwise reference order submission): "Order submission tracking is handled outside the behavioral analytics layer for this organization. Postgres order data is the authoritative source for ordering activity."
5. **Feature intensity notes** in cache commentary (`Q-22_results.md`): Do not classify "Order Submission" under "Zero activity" when the gap flag is set. Omit it from the intensity summary entirely.

Do not call out the tracking gap by name — just omit the misleading metric and avoid contradicting Postgres order data.

When `MIXPANEL_ORDER_TRACKING_GAP = false` or absent from `gate_flags.md`, render Q-22 normally with no changes.

## Quality Floor

Every subsection **must** contain all of the following:

1. A **`.prose` analytical paragraph** (2–4 sentences minimum) that interprets the data — not just restates numbers. Speak as a smart analyst to a VP: compare counts to context, call out anomalies, frame what the numbers mean for platform health.
2. A **`.metrics-grid`** with `metric-card` elements for headline numbers (include `.metric-note` with time qualifier per Hard Rule #7).
3. A **`<div class="what-this-means">`** closing block (1–3 sentences, actionable implication). Do not duplicate the prose paragraph — the what-this-means block tells the client *what to do about it* or *why it matters strategically*, not what the numbers are.

If a subsection has a table, the `.prose` paragraph must appear **above** the table and interpret highlights — do not let the table speak for itself.

Where a notable pattern exists (feature dominance, stale data cluster, configuration drift), add a **`.callout.insight`** block with a descriptive `.callout-title` and 1–2 sentences of context.

## Rendering Model: Health-Check Card

This section renders as a **single dense health-check card** rather than 6 independent subsections. The goal is VP-level readability: "Is there a problem, and how do I fix it?" — not a sysadmin dashboard.

**This section owns the operational catalog completeness recommendation.** §4 Product references catalog completeness for its sales performance framing but defers operational "upload X images" actions here.

### Card Structure

The section body contains ONE subsection with this layout:

1. **Status row** — a `.metrics-grid` with 3–5 status indicators using traffic-light badge semantics
2. **Alerts block** — configuration issues or stale data requiring action (if any)
3. **Feature opportunity** — one underutilized feature worth highlighting (if any)
4. **Detailed data** — full tables in a collapsed `<details>` for readers who want depth

### 1. Status Indicators (metrics grid)

Build from Q-07, Q-08, Q-09, Q-10 cache files. Produce a `.metrics-grid` with these cards:

| Indicator | Source | Badge logic |
|-----------|--------|-------------|
| Core Pipeline | Q-09 avg monthly imports | `.badge.ok` "Healthy" if ≥50/mo avg; `.badge.warn` "Low Volume" if <50/mo; `.badge.danger` "Stalled" if <10/mo or recent month = 0 |
| Data Freshness | Q-08 entity counts | `.badge.ok` if 0 Stale entities; `.badge.warn` if 1–3 Stale; `.badge.danger` if >3 Stale |
| Catalog | Q-07 completeness % | `.badge.ok` if ≥95%; `.badge.warn` if 80–94%; `.badge.danger` if <80% |
| Feature Adoption | Q-22 distinct active features | `.badge.ok` if ≥5 active features; `.badge.warn` if 3–4; `.badge.danger` if ≤2 |
| Smart Stacks | Q-10 smart stack count | `.badge.ok` if >0 published; `.badge.muted` "Not configured" if 0. Omit card entirely if org has zero smart stacks. |

Each `.metric-card` shows the status badge as `.metric-val` and a one-line explanation as `.metric-note`.

### 2. Alerts Block (Q-08, Q-11 — conditional)

If Q-08 shows any Stale entities OR Q-11 surfaces configuration drift:

- Render a `.callout.alert` with title "Action Required"
- List each alert as a single line: **Entity/Feature** — issue description — recommended action
- Group related entities (e.g., "Options, Option Groups & Matrix Options" as one line)
- Use the 3-label freshness scale only: Fresh (≤30d) / Monitor (31–180d) / Stale (>180d)
- `portal_orders` entity label rule still applies: use "All-Channel Orders" in all client-facing text

If no alerts, omit this block entirely — do not render an empty "no issues found" callout.

### 3. Feature Opportunity (Q-22, Q-46 conditional — conditional)

If Q-22 reveals an underutilized high-value feature (e.g., SmartPicks minimal vs heavy Product Search activity), render a single `.callout.opportunity`:

- Title: the opportunity (e.g., "SmartPicks Coaching Opportunity")
- Body: 1–2 sentences framing the gap and potential value
- If Q-46 is present, weave submit-through rate context into the opportunity framing (translate band labels into client-friendly language — never use raw band names)

**Platform Activity Composition** (conditional — render ONLY when `USER_GROUP_SPLIT_AVAILABLE = true`):

If the gate is true, read the `Aggregate Split` table from `cache/user_group_mapping.md`. Append a single contextual sentence to the feature opportunity or the prose paragraph:

> "Of tracked platform activity, approximately X% is attributed to field representatives and Y% to showroom and operational accounts."

Rules:
- Use **percentages only** — no absolute event counts for the split
- Combine `showroom` and `admin_internal` buckets into "showroom and operational accounts"
- Round to nearest whole number; do not name individual accounts
- No negative framing ("inflated", "skewed", "misleading")

If `USER_GROUP_SPLIT_AVAILABLE = false` or absent, do nothing — no mention of user groups.

If no notable feature opportunity exists, omit this block.

### 4. Detailed Data (collapsed `<details>`)

Wrap ALL detailed operational data in a single collapsed `<details>` block with summary "View detailed platform data". Inside, include:

**Catalog detail** (Q-07, Q-10, Q-50 conditional):
- Table: Visibility | Products | Missing Images | Missing Price | Complete %
- If Q-50 present: library/document inventory with age context
- If price-level pricing detected (all products missing per-product price), note as valid configuration

**Data freshness detail** (Q-08):
- Table of all entities with freshness labels (`.badge.ok` Fresh / `.badge.warn` Monitor / `.badge.danger` Stale)
- Use human-friendly entity names, not raw snake_case identifiers
- Group stale entities by category if possible (Pricing, Product Config, Sales, Customer)

**Pipeline detail** (Q-09):
- One-line summary: average monthly imports, cadence characterization
- Table: Month | Imports (5 most recent months only). No monthly import count narrative — the status indicator already covers pipeline health.

**Configuration alerts detail** (Q-11 — if present):
- Table: Feature | Status badge | Issue | Action (same columns as before)
- Omit if all entities Fresh and no drift detected

**Smart stack detail** (Q-47 conditional):
- If Q-47 present: table Stack Name | Status | Created | Last Updated (top 5 by recency)
- If Q-47 absent: stack count metric only with cross-reference to Q-22 Collection Search events
- Omit entirely if smart_stacks = 0

### Prose and What-This-Means

- One `.prose` paragraph above the detailed data `<details>`: synthesize the health picture in 2–3 sentences. Lead with what's working, then note what needs attention. Frame for a VP, not a sysadmin.
- One `.what-this-means` block: 1–3 sentences of prioritized action. What is the single most impactful thing the client should do? If everything is healthy, acknowledge the operational discipline.

### Mixpanel Order-Tracking Gap

All rules from the Query Inputs section still apply. If `MIXPANEL_ORDER_TRACKING_GAP = true`:
- Remove "Order Submission" from any feature adoption assessment
- Do not characterize the platform as non-transactional
- Use neutral replacement language per Query Inputs rules

## DOES NOT COVER (hard boundaries)

This section does NOT produce:
1. Rep-level performance, coaching, or behavioral analysis → belongs in §2 Sales Team Performance
2. Customer-level activation, penetration, or dormancy analysis → belongs in §3 Customer & Buyer Intelligence
3. Product sales analysis, velocity, or new introduction performance → belongs in §4 Product & Inventory
4. Order trends, channel mix, or capture rate analysis → belongs in §5 Commerce Analytics
5. Portal traffic analytics (Clicky) → belongs in §6 Demand Signal Intelligence
6. Peer benchmarking or cohort comparisons → belongs in §7 Peer Benchmarking
7. Health score, churn risk, or expansion signals → internal only (GUARDRAILS.md §5)

Read: `GUARDRAILS.md` for the full query ownership table (§8) and rule set.

---

## Section-Specific Rules

**Data freshness labels** — use ONLY these three. No other labels. No 5-label severity system:
- **Fresh**: last updated ≤30 days ago
- **Monitor**: last updated 31–180 days ago
- **Stale**: last updated >180 days ago

**Feature gaps prohibition**: Do not list CPQ, Online Ordering, or other products as "gaps" if the client doesn't have that product. Only surface utilization data for features the client has access to.

**Entity names in client-facing HTML**: Use human-friendly names (e.g., "Price Levels", "Option Groups", "All-Channel Orders"), not raw identifiers (`price_levels`, `option_groups`, `portal_orders`).

- The `section-sub` one-liner should contain 3–4 key status indicators (e.g., "Pipeline healthy · 2 stale entities · 95% catalog completeness · 5 active features"). Do not dump all metrics into the section headline.
- The `section-contents` middot list uses: "Platform Health Check" (single entry — this section renders as one card, not multiple subsections).
