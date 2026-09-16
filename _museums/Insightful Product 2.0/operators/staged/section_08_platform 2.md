# Section Guide: §8 — Platform & Feature Utilization

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

## Subsection Order (do not reorder — render every subsection whose gate is met)

### 1. Catalog Health (Q-10)

Build from `Q-10_results.md`. Surface catalog health metrics — product count, category distribution, visibility status.

### 2. Feature Usage Intensity (Q-22)

Build from `Q-22_results.md`. Surface feature usage depth — which platform features the client actively uses and to what degree.

**Platform Activity Composition** (conditional — render ONLY when `USER_GROUP_SPLIT_AVAILABLE = true`):

If the gate is true, read the `Aggregate Split` table from `cache/user_group_mapping.md`. Append a single contextual sentence to the Feature Usage Intensity narrative that provides the percentage breakdown. Use this pattern:

> "Of tracked platform activity, approximately X% is attributed to field representatives and Y% to showroom and operational accounts."

Rules:
- Use **percentages only** — do not show absolute event counts for the split. The existing Q-22 headline number (total events) remains the single source of truth for totals. Percentages avoid any reconciliation mismatch between org-level Q-22 and per-user Q-01 aggregations.
- Combine the `showroom` and `admin_internal` buckets into a single "showroom and operational accounts" label. Do not break these out separately — the client doesn't need to know the internal distinction.
- Round percentages to the nearest whole number.
- Do not name individual showroom accounts or usernames.
- Do not add a separate subsection, table, or callout box for this — it is one sentence woven into the existing Feature Usage Intensity narrative.
- Do not use the words "inflated", "skewed", "misleading", or any negative framing. This is neutral context, not a warning.

If `USER_GROUP_SPLIT_AVAILABLE = false` (or the flag is absent from `gate_flags.md`), do **nothing**. Render Feature Usage Intensity exactly as before — no split sentence, no mention of user groups, no placeholder. The report is identical to the pre-P2 version.

### 3. Data Health Report (Q-08)

Build from `Q-08_results.md`. Surface last-updated dates for each data entity type using the **3-label freshness scale only**:

| Label | Threshold |
|-------|-----------|
| Fresh | Last updated ≤30 days ago |
| Monitor | Last updated 31–180 days ago |
| Stale | Last updated >180 days ago |

No other labels. No 5-label severity system.

**`portal_orders` entity label rule**: In the freshness table and all surrounding prose, label the `portal_orders` entity as **"All-Channel Orders"** — do not use the literal phrase "portal orders" in any client-facing text, even when naming a data entity. The same semantic guardrail that prohibits "portal orders" as buyer activity also applies to entity labels in delivered HTML.

Group entities by import file type (product file, customer file, options file, inventory file, sales data). Show a summary line: "X entities Fresh, Y Stale." Only surface stale entities in a collapsed `<details>` list — do not show all 22 entities in a flat table. Focus on entities the client can act on (pricing, options, categories, sales quotas) rather than system-managed entities that all update from the same import file.

Do not show import warning callouts unless there were critical file errors that failed processing entirely.

### 4. Data Pipeline Health (Q-09)

Build from `Q-09_results.md`. Surface import pipeline status — frequency, success rates, error patterns.

`[COLLAPSE]`

### 5. Platform Configuration Alerts (Q-11)

Build from `Q-11_results.md`. This subsection is **distinct from Data Health (Q-08)**:
- Q-08 reports entity-level import recency (when was each data type last updated)
- Q-11 reports configuration completeness — features that are enabled but have stale or unpopulated underlying data

Examples of configuration alerts:
- Kit Items configured but last imported 42+ days ago while Options were refreshed recently (drift risk)
- Sales Quotas enabled with rows but data 7+ months old (reps see outdated targets)
- Portal Analytics not established (blocking demand-side visibility)

Render as a table with these exact columns:

| Column | Content |
|--------|---------|
| Feature | Feature or configuration entity name |
| Status | Badge: Stale / Drift / Not Established |
| Issue | One sentence describing the problem |
| Action | One sentence recommended fix |

**Omission rule**: If all configuration entities are Fresh and no drift is detected, this subsection may be omitted.

`[COLLAPSE]`

### 6. Smart Stack Performance

**Gate**: `smart_stacks > 0` for the org (check cache data for smart stack count)

Surface smart stack configuration and performance metrics.

`[COLLAPSE]`

## Section-Specific Rules

**Data freshness labels** — use ONLY these three. No other labels. No 5-label severity system:
- **Fresh**: last updated ≤30 days ago
- **Monitor**: last updated 31–180 days ago
- **Stale**: last updated >180 days ago

**Feature gaps prohibition**: Do not list CPQ, Online Ordering, or other products as "gaps" if the client doesn't have that product. Only surface utilization data for features the client has access to.

- The `section-sub` one-liner should contain 3–4 key stats maximum (e.g., "X active features · Y stale entities · Z smart stacks · import pipeline healthy"). Do not dump all metrics into the section headline.
