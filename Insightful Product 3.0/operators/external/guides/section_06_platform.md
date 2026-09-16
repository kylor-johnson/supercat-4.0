# Section Guide: Platform Context
> **v3.1** — signal-first architecture + 2.0 health-check depth. Collapsed by default. Actionable staleness, peer gaps, AND operational health.

## Section Identity

- **id**: `platform`
- **title**: Platform Context
- **section number**: 6
- **include when**: Any signal fired with `Section Home = Platform Context`, OR data freshness issues exist (any entity > 90 days stale), OR alternate gate passes (feature utilization or config data available)
- **skip when**: All entities are fresh AND no signals fired AND no feature/config gaps — nothing worth showing
- **render mode**: Always collapsed (`<details class="section-collapse">` — the user must click to expand)

## PRE-BUILD GATE CHECK
> Follow `section_shared_contract.md` §1 for the gate check process.

Platform Context renders when any signal fired with Section Home = Platform Context, OR any entity is stale, OR feature/config data is available. Skip only when nothing is worth showing.

## Query Inputs

Read these cache files:

- `cache/signal_rank.md` — ranked signal manifest
- `cache/Q-07_results.md` — Catalog completeness (products, missing images, missing price)
- `cache/Q-08_results.md` — Data freshness / last import timestamps per entity
- `cache/Q-09_results.md` — Import pipeline health (monthly import cadence)
- `cache/Q-09_recent_results.md` — Recent import activity detail
- `cache/Q-10_results.md` — Platform configuration state (smart stacks, options, etc.)
- `cache/Q-11_results.md` — User/role summary and configuration alerts
- `cache/Q-22_results.md` — Feature utilization summary (Mixpanel feature usage depth)
- ~~`cache/Q-CI-02_results.md`~~ — **EXCLUDED**: Peer benchmarking data deemed unreliable. Do not read or reference.
- ~~`cache/Q-CI-03_results.md`~~ — **EXCLUDED**
- ~~`cache/Q-CI-03_benchmarks_results.md`~~ — **EXCLUDED**
- ~~`cache/Q-CI-05_results.md`~~ — **EXCLUDED**
- ~~`cache/peer_benchmark_extract.md`~~ — **EXCLUDED**
- `cache/gate_flags.md` — data availability gates, `MIXPANEL_ORDER_TRACKING_GAP`, `USER_GROUP_SPLIT_AVAILABLE`
- `cache/user_group_mapping.md` — conditional: only if `USER_GROUP_SPLIT_AVAILABLE = true`

---

## Guiding Principle

**Don't waste space on things that are fine.** This section exists to surface actionable staleness, missed capabilities, operational health, and peer gaps. If everything is fresh and well-configured, this section is minimal. But when there ARE gaps, this section should be dense and specific — a VP reading it should know exactly what to fix and why.

**This section owns operational catalog completeness recommendations.** §3 (Product Intelligence) references catalog completeness for sales performance framing but defers operational "upload X images" actions here.

---

## Rendering Model: Operational Health Check

The section renders as a dense operational status card — "Is there a problem, and how do I fix it?"

**PEER BENCHMARKING EXCLUDED**: Subsections 5 and 6 (Feature Adoption vs Peers, Peer Benchmarking Summary) are permanently excluded from this report. The peer benchmark data has been deemed unreliable and must not be rendered, referenced, or used as context in any section. Do not read peer benchmark cache files.

---

## Content Blocks (render in this order — each is independently gated)

### 1. Platform Health Status Dashboard (MANDATORY when any data available)

**Gate**: Q-08 OR Q-09 OR Q-07 OR Q-22 has data. (At least one of these will always be present.)

Build a `.metrics-grid` with 4–5 status indicator cards using traffic-light badge semantics:

| Indicator | Source | Badge logic |
|-----------|--------|-------------|
| Core Pipeline | Q-09 avg monthly imports | `.badge.ok` "Healthy" if ≥50/mo avg; `.badge.warn` "Low Volume" if <50/mo; `.badge.danger` "Stalled" if <10/mo or recent month = 0 |
| Data Freshness | Q-08 entity counts | `.badge.ok` if 0 Stale entities (>90d); `.badge.warn` if 1–3 Stale; `.badge.danger` if >3 Stale |
| Catalog | Q-07 completeness % | `.badge.ok` if ≥95%; `.badge.warn` if 80–94%; `.badge.danger` if <80% |
| Feature Adoption | Q-22 distinct active features | `.badge.ok` if ≥5 active features; `.badge.warn` if 3–4; `.badge.danger` if ≤2 |
| Smart Stacks | Q-10 smart stack count | `.badge.ok` if >0 published; `.badge.muted` "Not configured" if 0. Omit card entirely if org has zero smart stacks and never configured any. |

```html
<div class="subsection">
  <div class="subsection-title">Platform Health Status</div>
  <div class="metrics-grid">
    <div class="metric-card">
      <div class="metric-val"><span class="badge {{BADGE_CLASS}}">{{STATUS}}</span></div>
      <div class="metric-label">{{INDICATOR_NAME}}</div>
      <div class="metric-note">{{ONE_LINE_EXPLANATION}}</div>
    </div>
    {{REPEAT FOR EACH INDICATOR}}
  </div>
```

After the metrics grid, one `.prose` paragraph (2–3 sentences) synthesizing the health picture: lead with what's working, then note what needs attention. Frame for a VP, not a sysadmin.

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{HEALTH_SYNTHESIS — e.g., "Your import pipeline is healthy with consistent monthly activity, but 3 entity types haven't been refreshed in over 6 months — every section of this report that depends on inventory, options, or pricing is working with stale data. A single round of imports would immediately improve platform reliability."}}
  </div>
</div>
```

### 2. Operational Alerts (conditional: any entity stale OR configuration drift detected)

**Gate**: Q-08 shows any entity > 90 days stale OR Q-11 surfaces configuration drift.

**CRITICAL: Only show problems.** Do not render if everything is fresh and configured. Do not render "no issues found."

```html
<div class="subsection">
  <div class="subsection-title">Action Required</div>
  <div class="callout alert">
    <div class="callout-title">{{N}} items need attention</div>
  </div>
  <table>
    <tr><th>Entity / Feature</th><th>Status</th><th>Last Updated</th><th>Impact</th><th>Fix</th></tr>
    {{ROWS — one per stale entity or configuration issue, sorted by impact severity}}
  </table>
```

**Column details:**
- "Entity / Feature": Human-friendly names (e.g., "Price Levels", "Option Groups", "All-Channel Orders"). Never raw snake_case identifiers.
- "Status": `.badge.warn` for Stale (91–180d), `.badge.danger` for Critical (181+)
- "Last Updated": Date and days since
- "Impact": One sentence explaining what this staleness causes (e.g., "Inventory shows quantities from 6 months ago — reps can't trust stock availability.")
- "Fix": Specific action (e.g., "Upload current inventory.csv via FTP")

Group related entities where possible (e.g., "Options, Option Groups & Matrix Options" as one row).

```html
  <div class="what-this-means">
    <strong>Action:</strong> Stale data degrades every section of this report. {{MOST_IMPACTFUL_STALENESS — e.g., "Your inventory data is 147 days old — every stock-out finding in this report may be inaccurate. A single inventory import would immediately improve the reliability of product intelligence."}} Enabled-but-stale features create a worse experience than not having the feature at all — reps see outdated information and lose trust in the platform.
  </div>
</div>
```

**Freshness labels** — use ONLY these:
- Fresh (≤30d) — DO NOT RENDER
- Monitor (31–90d) — DO NOT RENDER
- Stale (91–180d) — `.badge.warn`
- Critical (181+) — `.badge.danger`

**Entity-specific overrides** (stricter than the general 90d threshold):
- Products / price levels: Stale after 30 days without import
- Inventory: Stale after 7 days without import
- All other entities: General 90d threshold applies

### 3. Feature Utilization (conditional: Q-22 data available)

**Gate**: `Q-22_results.md` has feature usage data with at least 3 distinct features tracked.

Shows which platform capabilities are being actively used and which are dormant.

```html
<div class="subsection">
  <div class="subsection-title">Feature Utilization</div>
  <div class="callout insight">
    <div class="callout-title">{{ACTIVE_COUNT}} of {{TOTAL_COUNT}} tracked features show active usage</div>
    <p>{{DOMINANT_FEATURE_PATTERN — e.g., "Product Search dominates at X events, accounting for Y% of all feature activity. Catalog creation and email sharing are strong secondary features. SmartPicks and Saved Lists show minimal adoption despite being available."}}</p>
  </div>
  <table>
    <tr><th>Feature</th><th>Events (LTM)</th><th>% of Activity</th><th>Intensity</th></tr>
    {{ROWS — sorted by event count desc}}
  </table>
```

**Intensity column badges:**
- Heavy (>10% of total): `.badge.ok`
- Moderate (2–10%): `.badge.muted`
- Light (<2%): `.badge.warn`
- Zero: `.badge.danger`

If an underutilized high-value feature is detected (e.g., SmartPicks at <1% while Product Search is heavy), add a `.callout.opportunity`:

```html
  <div class="callout opportunity">
    <div class="callout-title">{{FEATURE}} Coaching Opportunity</div>
    <p>{{GAP_NARRATIVE — e.g., "Your reps search for products 8,000+ times per month but use SmartPicks only 12 times. SmartPicks surfaces personalized recommendations based on customer purchase history — it's the difference between browsing and being guided to the right product."}}</p>
  </div>
```

**Mixpanel Order-Tracking Gap handling**: If `MIXPANEL_ORDER_TRACKING_GAP = true` in gate_flags:
- Remove "Order Submission" from the table entirely (the zero is a tracking artifact)
- Do not characterize the platform as non-transactional
- Use neutral replacement if needed: "Order submission tracking is handled outside the behavioral analytics layer for this organization."

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{FEATURE_UTILIZATION_IMPLICATION — e.g., "Heavy product search with low SmartPicks adoption means your reps are doing the work that the algorithm could do for them. Activating SmartPicks across your team would reduce browsing time and increase the relevance of product suggestions during customer presentations."}}
  </div>
</div>
```

`[COLLAPSE]` — wrap in inner `<details>` to keep the health card scannable.

### 4. Catalog Operational Recommendations (conditional: catalog completeness < 95% OR > 50 items missing assets)

**Gate**: Q-07 shows catalog completeness < 95% OR more than 50 items need images or pricing.

This subsection owns the operational remediation actions that §3 (Product) references but defers.

```html
<div class="subsection">
  <div class="subsection-title">Catalog Remediation</div>
  <table>
    <tr><th>Visibility</th><th>Products</th><th>Missing Images</th><th>Missing Price</th><th>Complete %</th></tr>
    {{ROWS — from Q-07}}
  </table>
```

If price-level pricing detected (all products missing per-product price), note as valid configuration — not a gap.

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{CATALOG_IMPLICATION — e.g., "X visible items are missing images or pricing. Every missing image is a product your reps skip in presentations — that's revenue left on the table. Upload product photos to FTP /images and they'll be available on the iPad within 30–45 minutes of processing."}}
  </div>
</div>
```

`[COLLAPSE]`

### ~~5. Feature Adoption vs Peers~~ — PERMANENTLY EXCLUDED

**DO NOT RENDER.** Peer benchmark data is unreliable. Skip this subsection entirely regardless of data availability.

### ~~6. Peer Benchmarking Summary~~ — PERMANENTLY EXCLUDED

**DO NOT RENDER.** Peer benchmark data is unreliable. Skip this subsection entirely regardless of data availability.

### 7. Import Pipeline Detail (conditional: pipeline data shows interesting patterns)

**Gate**: Q-09 has monthly import data AND either pipeline is stalled (recent month = 0) OR cadence is notably irregular.

**SKIP if pipeline is healthy and consistent.** Only render when there's a story worth telling.

```html
<div class="subsection">
  <div class="subsection-title">Import Pipeline</div>
  <table>
    <tr><th>Month</th><th>Imports</th></tr>
    {{5 MOST RECENT MONTHS}}
  </table>
  <div class="what-this-means">
    <strong>Action:</strong> {{PIPELINE_NARRATIVE — e.g., "Your import volume dropped from 85/month to 12/month over the last quarter. This correlates with the staleness in your inventory and pricing data — the pipeline slowdown is the root cause of the freshness alerts above."}}
  </div>
</div>
```

`[COLLAPSE]`

---

## Section-Level What-This-Means

**Not required for Platform Context.** Each subsection has its own `.what-this-means` close, and a section-level close would be redundant for an operational reference section.

---

## Highlight File Output

Save `cache/section_06_highlights.md`:

- 1–2 candidate highlights (only if staleness or gaps are severe enough to warrant Signal Summary inclusion)
- Each: bold headline, one sentence context, `[→ §platform]`
- Typically 0 priority action candidates — platform context is rarely urgent enough for the top-level priority list
- Exception: If core entities (products, inventory, customers) are > 180 days stale, this IS priority-action-worthy — data staleness at that level undermines every other section

---

## Section-Specific Rules

**Data freshness labels** — use ONLY these three in client-facing output:
- **Fresh**: last updated ≤30 days ago
- **Monitor**: last updated 31–90 days ago
- **Stale**: last updated >90 days ago (91–180d = `.badge.warn`, 181+ = `.badge.danger`)

**Entity names in client-facing HTML**: Use human-friendly names (e.g., "Price Levels", "Option Groups", "All-Channel Orders"), not raw identifiers (`price_levels`, `option_groups`, `portal_orders`).

**Feature gaps prohibition**: Do not list CPQ, Online Ordering, or other products as "gaps" if the client doesn't have that product. Only surface utilization data for features the client has access to.

**Terminology rules**: See `shared_rules.md` §E and §A1 for forbidden terms and required substitutions (ERP, Mixpanel, portal_orders, etc.).

---

## Conditional Subsection Checklist

- [ ] Health Status Dashboard: rendered with 4-5 status indicator cards (traffic-light badges). Prose synthesis present.
- [ ] Operational Alerts: rendered ONLY if stale entities or config drift exist. No "everything is fine" filler.
- [ ] Feature Utilization: rendered if Q-22 has data. Mixpanel Order-Tracking Gap handled correctly. `[COLLAPSE]`.
- [ ] Catalog Remediation: rendered ONLY if completeness < 95% or > 50 items missing assets. `[COLLAPSE]`.
- [ ] Feature Adoption vs Peers: **PERMANENTLY EXCLUDED** — do NOT render regardless of data availability.
- [ ] Peer Benchmarking: **PERMANENTLY EXCLUDED** — do NOT render regardless of data availability.
- [ ] Import Pipeline Detail: rendered ONLY if pipeline is stalled or irregular. `[COLLAPSE]`.
- [ ] Section rendered as collapsed `<details>` (user must click to expand)
- [ ] Every rendered subsection has a `.what-this-means` close
- [ ] No section-level `.what-this-means` (not required for this section)
- [ ] `cache/section_06_highlights.md` saved
- [ ] Forbidden terms check passed (see section_shared_contract.md §6)
- [ ] Every metric has a time qualifier
- [ ] No "everything is fine" filler — if nothing is wrong, the subsection doesn't render
- [ ] Status indicator badges match the defined thresholds (no custom badge logic)
