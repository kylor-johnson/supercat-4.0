# Section 6 Context Bundle — EGLO Canada (eglo_can)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — EGLO Canada (eglo_can, org_id=232)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | False | portal_order_count=0, portal_order_gmv=$0 |
| HAS_INVENTORY | True | inventory_count=1691 |
| HAS_SALES_DATA | True | sales_data_count=6618 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=1 engagement_reps=17 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Commerce-Active |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | N/A |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | SKIP |  |
| VM45_GATE_2 | SKIP |  |
| VM45_RENDER | False |  |
| QUALIFYING_REP_COUNT | 1 | 1 |
| ENGAGEMENT_REP_COUNT | 17 | engagement_reps=17 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 26 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 43, Mixpanel total submit_order (Q-01): 130 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=73.1%, ambiguous_rate=73.7%, showroom_event_share=38.1% |
| USER_GROUP_JOIN_RATE | 73% | 19 of 26 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 38% | showroom+admin share of matched events: 38.1% |
| ADMIN_REPS_IN_LEADERBOARD | True | 1 admin/showroom users in leaderboard: Karen Hoffman |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False |  |
| PORTAL_REP_DATA_PRESENT | False |  |
| PORTAL_CUSTOMER_DATA_PRESENT | False |  |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=495 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | PARTIAL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | PARTIAL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: EGLO Canada
- **Shortname**: eglo_can
- **Org ID**: 232
- **Bundle**: 4
- **Bundle label for report**: 4

## Validation Log

- portal_orders LTM count=0, gmv=0.0 — HAS_PORTAL_ORDERS overridden to false

## Section Confidence

# Section Confidence Tiers — EGLO Canada (eglo_can, org_id=232)
- **Run date**: 2026-06-17

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | False |
| PORTAL_CUSTOMER_DATA_PRESENT | False |
| PORTAL_ORDERS_FRESH | False |
| HAS_PORTAL_ORDERS | False |
| HAS_INVENTORY | True |
| HAS_SALES_DATA | True |
| INVENTORY_FRESH | True |
| SALES_DATA_FRESH | False |
| CUSTOMER_DATA_FRESH | True |

## Computed Tiers

| Section | Tier | Determining Condition |
| --- | --- | --- |
| §2 Sales Team | STRONG | See Derived Gate 6 §2 formula |
| §3 Customer | PARTIAL | See Derived Gate 6 §3 formula |
| §4 Product | STRONG | See Derived Gate 6 §4 formula |
| §5 Commerce | PARTIAL | See Derived Gate 6 §5 formula |

## Section Guide — section_06_platform.md

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

## TARGET STRUCTURE — Gold Standard (MATCH THIS MARKUP EXACTLY)

This is the corresponding section from the canonical reference report. It is the source of truth for HTML structure: tag nesting, class names, column headers, subsection order, which subsections carry a `what-this-means` block, and the `<thead>`/`<tbody>`/`row-highlight` patterns. The data values below are illustrative — replace them with this client's data — but reproduce the STRUCTURE exactly. Where this target and the prose guide disagree on markup, THIS WINS.

```html
<details class="section-collapse" id="platform">
  <summary>
    <div class="section-title">Platform Context</div>
    <div class="section-sub">Actionable items only &middot; data freshness, feature adoption gaps</div>
    <div class="section-contents">Stale data alerts, underused features with revenue impact</div>
    <span class="expand-hint">Expand section</span>
  </summary>
  <div class="section"><div class="subsection">
      <div class="subsection-title">Data Freshness</div>
      <div class="sub-label">Only showing entities with stale data (>7 days since last sync)</div>
      <table>
        <thead>
          <tr><th>Data Source</th><th>Last Updated</th><th>Staleness</th><th>Impact</th></tr>
        </thead>
        <tbody>
          <tr class="row-warn"><td><strong>Inventory Feed</strong></td><td>Jun 14, 2026</td><td>3 days</td><td>Low &mdash; within normal refresh window</td></tr>
          <tr class="row-danger"><td><strong>Customer Master (Ship-Tos)</strong></td><td>May 28, 2026</td><td>20 days</td><td>Medium &mdash; new locations for Lakeside Living not reflected</td></tr>
          <tr class="row-warn"><td><strong>Product Images (Outdoor)</strong></td><td>Jun 2, 2026</td><td>15 days</td><td>Low &mdash; 4 new Outdoor SKUs missing lifestyle photos</td></tr>
        </tbody>
      </table>
      <div class="what-this-means">
        <strong>Action:</strong> Lakeside Living opened a 7th showroom location (confirmed in their recent orders) but the ship-to address isn&rsquo;t in the customer file yet. Update and re-import customers.csv to prevent order-entry friction for their new location. Also upload lifestyle photos for the 4 Outdoor SKUs launched June 2 &mdash; these products show well with room-scene imagery.
      </div>
    </div><div class="subsection">
      <div class="subsection-title">Feature Adoption Gaps</div>
      <div class="sub-label">Underused features with estimated revenue impact if adopted</div>
      <table>
        <thead>
          <tr><th>Feature</th><th>Current Usage</th><th>Opportunity</th><th>Est. Impact</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>Saved Carts / Quick Reorder</strong></td><td>8 of 32 reps (25%)</td><td>Reduces reorder friction; Power Users who use it convert 23% faster</td><td>+$240K/year</td></tr>
          <tr><td><strong>Presentation Builder</strong></td><td>12 of 32 reps (38%)</td><td>Presentations convert to orders at 74% vs 41% for browse-only sessions</td><td>+$180K/year</td></tr>
          <tr><td><strong>Multi-Ship (per-location orders)</strong></td><td>3 of 32 reps (9%)</td><td>Accounts with multiple locations could consolidate orders</td><td>+$92K/year</td></tr>
          <tr><td><strong>Inventory Visibility</strong></td><td>Enabled but underused</td><td>Only 4 reps regularly check stock before quoting</td><td>Prevents $186K stockout friction</td></tr>
        </tbody>
      </table>
      <div class="what-this-means">
        <strong>Action:</strong> Saved Carts and Presentation Builder together represent an estimated $420K annual opportunity. Run a 2-week &ldquo;feature sprint&rdquo; with your top 10 reps (who already have the order volume): teach Saved Carts in week 1, Presentation Builder in week 2. Rachel Simmons and Patricia Nakamura can lead peer demos since they already use both features daily.
      </div>
    </div>

  </div>
</details>
```

## Section Shared Contract

# Section Shared Contract — Insightful Product 3.0

> Referenced by all section guides (§1–§6). Contains processes that are identical
> across sections. Each section guide provides section-specific parameters;
> this file provides the canonical process. **Do not duplicate these processes
> in individual guides.**

---

## 1. Pre-Build Gate Check Process

Before generating any HTML for a section:

1. Open `cache/gate_flags.md` and `cache/section_confidence.md`.
2. For each row in the section guide's **PRE-BUILD GATE CHECK** table:
   - Check the gate condition against `gate_flags.md`.
   - Check whether the cache file exists AND contains data rows.
   - Record: subsection name, MANDATORY or CONDITIONAL, gate MET or NOT MET.
3. **Write down your list** of subsections that will render before proceeding.
   Use this list as a checklist while building the fragment.
4. Skipping a MANDATORY subsection when its gate is met = **defective fragment**.

---

## 2. Data Confidence Header (MANDATORY for §2–§5)

Every section fragment (§2 through §5) MUST include a data confidence header.
If this header is missing, the fragment is **DEFECTIVE**.

**STEP 1 — Read the tier.** Open `cache/section_confidence.md` and read the
EXACT value of `SECTION_CONFIDENCE_N` (where N is this section's number). The
value is one of: `FULL`, `STRONG`, `PARTIAL`, `LIMITED`. **Use THIS value.
Do NOT infer or recompute the tier from gate flags — the data gathering script
already computed it.**

**STEP 2 — Select the template** from the section guide's confidence header
table (each guide defines its own template IDs, variable sources, and fallback
rules).

**STEP 3 — Position the header:** ALWAYS immediately after the header metrics,
BEFORE the first subsection content. This applies to ALL tiers including FULL.

**STEP 4 — Build the HTML:**

```html
<div class="data-confidence">
  <span class="data-confidence-label">{{TIER_LABEL}}</span>
  <span class="data-confidence-action">{{TEMPLATE_TEXT}}</span>
</div>
```

If the tier is `LIMITED`, use `<div class="data-confidence limited">` instead.

§6 (Platform Context) does NOT use a confidence header.

---

## 3. Fragment Wrapper

Sections §2–§5 use the `<details class="section-collapse">` wrapper per
`shared_rules.md` Section C. Each section guide specifies its Section ID and
Section Number.

**CORRECT HTML structure** (match exactly — rendering breaks if elements are
outside `<summary>` or wrong tag types are used):

```html
<details class="section-collapse" id="{{SECTION_ID}}">
  <summary>
    <div class="section-title">{{SECTION_TITLE}}</div>
    <div class="section-sub">{{ONE-LINE STATS}}</div>
    <div class="section-contents">{{SUBSECTION_NAMES joined by · middots}}</div>
    <span class="expand-hint">Expand section</span>
  </summary>
  <div class="section">
    {{ALL SECTION CONTENT HERE}}
  </div>
</details>
```

Rules:
- `section-title` MUST be a `<div>`, not a `<span>`.
- `section-sub`, `section-contents`, and `expand-hint` MUST be INSIDE `<summary>`.
- If ANY of these elements are placed outside `<summary>`, the collapsed state
  renders incorrectly (text visible when section is collapsed).
- `section-contents` lists ONLY subsections that actually rendered (not skipped).

§1 (Signal Summary) renders as an open `<div class="section">` — it does NOT use `<details>`.
§6 (Platform Context) renders as a collapsed `<details>` (user must click to expand).

---

## 4. Highlight File Output

After building each section fragment, save `cache/section_NN_highlights.md`
per `shared_rules.md` Section K:

- 2–4 candidate highlights from the section's strongest signals.
- Each: bold headline + one sentence context + dollar figure + `surprise_score`
  + `signal_id` + section deep-link (e.g., `[→ §accounts]`).
- 0–1 priority action candidates with urgency level.
- At least 1 highlight MUST be positive.

Exception: §1 (Signal Summary) does NOT produce a highlights file — it consumes
highlights from all other sections. §6 produces 1–2 highlights only when issues
are severe (>180d staleness).

---

## 5. Conditional Subsection Checklist Process

Before saving a section fragment, verify against the section guide's
**Conditional Subsection Checklist** table:

1. For each row: confirm the subsection was rendered if its gate was met, or
   correctly skipped if its gate was not met.
2. Confirm the `section-contents` middot list in the HTML matches ONLY the
   subsections that actually rendered (not skipped ones).
3. Confirm every rendered subsection (except those noted otherwise in the guide)
   ends with a `<div class="what-this-means">` block that:
   - Starts with `<strong>Action:</strong>`
   - Contains max 3 sentences total
   - Names a specific entity and action (not generic advice)
4. Confirm the section-level `.what-this-means` is present (max 3 sentences,
   starts with `<strong>Action:</strong>`)
   — except §1 and §6 which have different rules per their guides.

---

## 6. Forbidden Terms Verification

Before saving any fragment, verify NONE of the following appear in the HTML:

| Forbidden | Replacement |
|-----------|-------------|
| ERP | "total business", "all-channel orders", "orders synced from your systems" |
| Mixpanel | "app usage data", "engagement events" |
| Clicky | Do not reference — suppress data source |
| health score | Use "Engagement Score" (§2 only) or describe the pattern |
| Segment labels (Platform-Embedded, etc.) | Describe the behavior instead |
| Internal IDs (org_id, customer_code, query IDs) | Remove entirely |
| Literal `[HYPOTHETICAL]` or `[ESTIMATED]` in HTML | Use prose hedging ("estimated", "projected") |
| portal orders / portal ordering | "total business", "all-channel orders" |
| platform (standalone) | "eCat", "the app", "your digital catalog" |
| platform-attributed revenue | "orders placed through eCat", "eCat volume" |
| platform engagement | "app usage", "digital catalog activity" |

Also verify:
- Every dollar figure has a time qualifier.
- Every finding names a specific entity — no generic "your accounts."
- Tables: top 5 visible, remainder in `<details>` (unless spec says otherwise).


# Shared Rules (excerpt for this section)

## A0. Editorial Voice — The North Star

**This is an intelligence report, not a risk report.**

The reader should finish this report thinking: *"I didn't know that about my
business — I need to pay for this."* NOT: *"Everything is broken, I should
churn."*

### Narrative Arc (MANDATORY)

Every section, and the report as a whole, follows this arc:

1. **MOMENTUM** — What's working. Celebrate wins, name the reps/accounts/products
   driving growth. This is NOT filler — it's the credibility foundation. If the
   reader doesn't trust that you understand their business, they won't act on risks.
2. **INTELLIGENCE** — What's interesting. Data-dense tables, penetration views,
   category breakdowns, behavioral patterns — the stuff they can't get from their
   own ERP. This is the "holy shit, I didn't know that" layer.
3. **OPPORTUNITY** — What could be better. Cross-sell whitespace, activation
   targets, coaching upside, conversion improvements. Frame as growth, not repair.
4. **RISK** — What to watch. Decay signals, displacement, contraction. These
   come LAST and are contextualized within the positive narrative. A $50K decay
  signal is alarming in isolation but manageable when prefaced by "$8.6M in eCat
  sales driven by 37 active reps."

### Tone Rules

- **Lead with strength.** The first subsection in every section should be the
  most impressive finding — the thing that makes the client proud of their business.
- **Risk findings are always contextualized.** Never "you're losing $X" in
  isolation. Always "you drove $Y through the platform; $X of that is at risk
  from [specific pattern]."
- **Frame negatives as opportunities.** "6 accounts show eCat share declining
  while total business grows — re-engaging them through the platform could
  recapture an estimated $Z" beats "COMPETITIVE DISPLACEMENT DETECTED — $X
  shifting away."
- **Ban doom headlines.** The words "ALERT", "DETECTED", "WARNING" in callout
  titles are reserved for genuine P0 operational issues (stock-outs affecting
  top customers, data staleness). Behavioral patterns, pricing shifts, and
  channel migration use `.callout.insight` not `.callout.alert`.
- **Celebrate specific wins by name.** "[Rep] converts at 26.8% — the highest
  on your team." "[Account] grew from $824 to $78.9K in 4 quarters on the
  platform." These are the findings that make clients say "I need this."

### Report-Level Balance Test (run before finalizing)

Count the findings across the Signal Summary:
- **Minimum 3 of 7 findings must be positive** (momentum, opportunity, or
  intelligence). If fewer than 3 are positive, demote the weakest risk finding
  and promote the next-best positive finding.
- **The FIRST finding must be positive.** The reader's first impression sets the
  tone for the entire report. Lead with the win.
- **Priority Actions balance:** At least 1 of 4 priority actions must be a GROWTH
  action (not a "fix this" or "re-engage that"). E.g., "Expand [product line]
  into [N] accounts that buy similar categories — estimated $X addressable."

---

## A1. Client-Facing Language — Write for Sales Leaders, Not SaaS PMs

The audience is a VP of Sales or owner at a lighting, furniture, or home decor
manufacturer. They think in reps, dealers, showrooms, orders, and products —
not platform metrics. Every term in the left column is **banned from client-facing
HTML**. Use the right column instead.

| Banned (SaaS / tech) | Use instead |
|---|---|
| "platform capture rate" / "capture rate" | "digital ordering share" or "share of orders placed through eCat" |
| "Capture Rate Economics" | "Digital Ordering Opportunity" |
| "platform GMV" | "eCat sales" or "orders placed through eCat" |
| "platform-attributed revenue" | "orders placed through eCat" or "eCat volume" |
| "collaborative filtering" | Describe the behavior: "customers who buy X also buy Y" |
| "cross-sell engine" | "products your customers buy together" or "companion products" |
| "Next Best Product" (as a title) | "Products Frequently Bought Together" or "Companion Product Opportunities" |
| "activation" (for accounts) | "onboarding" or "getting them ordering through the app" |
| "signal density" | Never in client-facing text — internal only |
| "behavioral data reveals" | "your team's usage patterns show" |
| "platform engagement" | "app usage" or "digital catalog activity" |
| "[assumes behavioral change]" | "[estimated]" — or drop if "estimated" already appears in the sentence |
| `[eCat ONLY]` / `[ALL-CHANNEL]` inline with dollar figures | Move these labels to **column headers** or **metric card labels** instead. In prose, say "eCat orders" or "total business across all channels" — never bracket-tags mid-sentence. |
| "platform" (standalone, as in "the platform") | "eCat" or "the app" or "your digital catalog" |
| "addressable" (as in "addressable revenue") | "potential" or "available" |

**Terms that are fine** — standard business vocabulary a sales leader uses daily:
conversion rate, year-over-year, trailing 12 months, reorder velocity, AOV,
LTM, quarter-over-quarter, fill rate, pipeline, territory, funnel.

**Inline data tags**: The `[eCat ONLY]` and `[ALL-CHANNEL]` bracket tags must
NOT appear inline with dollar figures in prose or table cells. Instead:
- In **metric cards**: put the scope in `.metric-note` (e.g., "eCat orders only")
- In **table headers**: append scope (e.g., "GMV (eCat)" or "GMV (all channels)")
- In **prose**: write it out ("$8.6M in eCat orders" or "$88M across all channels")
- These bracket tags ARE used in the **appendix labeling convention** and in
  **guide-internal documentation** to mark which data source applies — that is
  fine. The prohibition applies to client-facing rendered HTML only.

---

## H. What-This-Means Blocks

End every **section** (not subsection) with a `.what-this-means` div. Subsections also get their own `.what-this-means` per section guide specs.

- **Max 3 sentences.**
- **First sentence:** the strength to protect or the opportunity to capture
  (what's WORKING and how to build on it).
- **Second sentence:** the specific action that unlocks the next level of
  performance (growth-framed, not risk-framed).
- **Third sentence (optional):** what additional data would enable (data extension
  opportunity) OR the cost of inaction (but ONLY after the positive framing).
- **Never restate the statistics.** The reader already saw the table.
- **Never lead with doom.** "Your 37-rep team drove $8.6M through the platform —
  coaching the bottom quartile to median would add an estimated $1.2M" beats
  "10 reps convert below 10% — $1.2M at risk if nothing changes."

### H1. Self-Check (MANDATORY before saving any fragment)

After writing EVERY `.what-this-means` block, apply this 3-question test:

1. **Restatement test**: Could this sentence be produced by reading the first row of the table above it? If yes → REWRITE. The reader already read the table — your job is interpretation, not narration.
2. **Action test**: Does this block tell the reader what to DO or what it MEANS for their business? If it only tells them what the data SAYS → REWRITE.
3. **Specificity test**: Does this block reference at least one specific entity (rep name, account name, dollar figure, percentage) from THIS org's data? If it could apply to any org → REWRITE.

**FAILING EXAMPLES** (any of these patterns = automatic rewrite):
- "Your top performer generates $765K in iPad orders across 131 customers." ← This literally reads the table back.
- "This table shows your top 10 reps by GMV." ← Narrates the obvious.
- "Your top accounts are driving the majority of your revenue." ← Generic, applies to every org.
- "These accounts show declining order patterns." ← Restates without interpreting WHY or WHAT TO DO.

**PASSING EXAMPLES**:
- "The $485K gap between #1 and #10 suggests significant room to elevate mid-tier reps through coaching on customer targeting — if your bottom 5 matched your #5's AOV, that's an estimated $290K in annual incremental revenue."
- "Your most active rep presented to 49 accounts but only 3.6% converted to orders — high effort, lower yield. Meanwhile, your most efficient closer converts at 26.8% with far fewer presentations, suggesting targeted demos outperform high-volume prospecting for your product category."
- "The 63.8% decline at Lighting Connection ($926K→$335K) warrants immediate investigation: at that velocity, this was likely a deliberate channel shift rather than gradual drift. Three hypotheses: (1) they consolidated vendors, (2) they're sourcing this category direct-import, or (3) a competitor captured the relationship."

---

## K. Highlight File Contract

After building each section fragment, output `cache/section_NN_highlights.md`:

- **2–4 candidate highlights** per section.
- Each highlight: one-line headline + dollar figure + `surprise_score` +
  `signal_id`.
- Signal Summary builder reads **ALL** highlight files and selects top 5–7 by
  `SIGNAL_RANK`, subject to the diversity constraint (max 4 from any one section).
- `[HYPOTHETICAL]` tags appear in highlight files only — never in final HTML
  fragment.

---


## Cache Data

### signal_rank.md

# Signal Rank — EGLO Canada (eglo_can, org_id=232)
- **Run date**: can_2026-06-17
- **Total signals fired**: 26 (P0: 12, P1: 11, P2: 3)
- **Org GMV**: $0.0M eCat LTM, $0.0M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-ANOMALY-02 | Stock Out — 205989A (Trago 5 - 12" 5CCT LED Ceiling Light / P) $72,729 LTM, 0 available | P0 | §3 Product | 10.0 | $72,729 | 3.0 | 2,181,874 | RISK |
| 2 | SIG-ANOMALY-02 | Stock Out — 39267A (Climene - LED Pendant Light / LED Lumina) $25,446 LTM, 0 available | P0 | §3 Product | 10.0 | $25,446 | 3.0 | 763,388 | RISK |
| 3 | SIG-ANOMALY-02 | Stock Out — 205292A (Rafaelino - 1L Pendant Light / Luminaire) $22,094 LTM, 0 available | P0 | §3 Product | 10.0 | $22,094 | 3.0 | 662,809 | RISK |
| 4 | SIG-ANOMALY-02 | Stock Out — 390466A (Fruitera - 6L 3CCT LED Pendant Light / L) $21,901 LTM, 0 available | P0 | §3 Product | 10.0 | $21,901 | 3.0 | 657,026 | RISK |
| 5 | SIG-ANOMALY-02 | Stock Out — 205986A (Trago 5 - 9" 5CCT LED Ceiling Light / Pl) $18,183 LTM, 0 available | P0 | §3 Product | 10.0 | $18,183 | 3.0 | 545,492 | RISK |
| 6 | SIG-ANOMALY-02 | Stock Out — 205988A (Trago 5 - 7" 5CCT LED Ceiling Light / Pl) $13,266 LTM, 0 available | P0 | §3 Product | 10.0 | $13,266 | 3.0 | 397,989 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 206938A (Grazia - LED Linear Chandelier / Lustre ) $11,773 LTM, 0 available | P0 | §3 Product | 10.0 | $11,773 | 3.0 | 353,179 | RISK |
| 8 | SIG-ANOMALY-02 | Stock Out — 206937A (Grazia - LED Chandelier / Lustre DEL) $11,460 LTM, 0 available | P0 | §3 Product | 10.0 | $11,460 | 3.0 | 343,787 | RISK |
| 9 | SIG-ANOMALY-02 | Stock Out — 205131A (Troy 3 - 1L Pendant Light / Luminaire su) $10,553 LTM, 0 available | P0 | §3 Product | 10.0 | $10,553 | 3.0 | 316,577 | RISK |
| 10 | SIG-ANOMALY-02 | Stock Out — 85977A (Troy 3 - 1L Pendant Light / Luminaire su) $10,439 LTM, 0 available | P0 | §3 Product | 10.0 | $10,439 | 3.0 | 313,169 | RISK |
| 11 | SIG-ANOMALY-02 | Stock Out — 390342A (Dracera - 10L Linear LED Pendant / Lumin) $10,409 LTM, 0 available | P0 | §3 Product | 10.0 | $10,409 | 3.0 | 312,274 | RISK |
| 12 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 49% of eCat GMV | P1 | §4 Commerce | 1.2 | $126,661 | 2.0 | 308,350 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — 200146A (Ascoli - 1L Exterior Wall Light / Murale) $10,250 LTM, 0 available | P0 | §3 Product | 10.0 | $10,250 | 3.0 | 307,515 | RISK |
| 14 | SIG-OPP-04 | New Item Adoption Gap — 7 new items with $0 platform orders | P2 | §3 Product | 0.7 | $50,000 | 1.0 | 35,000 | POSITIVE |
| 15 | SIG-RISK-03 | Data Staleness — contract_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 16 | SIG-RISK-03 | Data Staleness — kit_items last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 17 | SIG-RISK-03 | Data Staleness — matrix_options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 18 | SIG-RISK-03 | Data Staleness — option_groups last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 19 | SIG-RISK-03 | Data Staleness — options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 20 | SIG-RISK-03 | Data Staleness — commitment_reports last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §3 Product Intelligence | 12 | 0 | 1 | 13 | |
| §4 Commerce Patterns | 0 | 1 | 0 | 1 | |
| §6 Platform Context | 0 | 10 | 2 | 12 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-04: New Item Adoption Gap — 7 new items with $0 platform orders
2. **[RISK]** SIG-ANOMALY-02: Stock Out — 205989A (Trago 5 - 12" 5CCT LED Ceiling Light / P) $72,729 LTM, 0 available
3. **[RISK]** SIG-ANOMALY-02: Stock Out — 39267A (Climene - LED Pendant Light / LED Lumina) $25,446 LTM, 0 available
4. **[RISK]** SIG-ANOMALY-02: Stock Out — 205292A (Rafaelino - 1L Pendant Light / Luminaire) $22,094 LTM, 0 available
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 390466A (Fruitera - 6L 3CCT LED Pendant Light / L) $21,901 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — 205986A (Trago 5 - 9" 5CCT LED Ceiling Light / Pl) $18,183 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 205988A (Trago 5 - 7" 5CCT LED Ceiling Light / Pl) $13,266 LTM, 0 available

**Balance check**: 1 positive (slots 1-1), 6 risk (slots 2-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-08_results.md

# Q-08 Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-08 — Data Freshness Monitor
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 22
- **Run date**: 2026-06-17


| entity_type | last_updated | days_since_update | status |
| --- | --- | --- | --- |
| contract_prices | 2025-08-07 23:13:11 | 313 | Stale |
| kit_items | 2025-08-07 23:13:11 | 313 | Stale |
| matrix_options | 2025-08-07 23:13:11 | 313 | Stale |
| option_groups | 2025-08-07 23:13:11 | 313 | Stale |
| options | 2025-08-07 23:13:11 | 313 | Stale |
| commitment_reports | 2025-08-07 23:13:11 | 313 | Stale |
| placement_reports | 2025-08-07 23:13:11 | 313 | Stale |
| riser_prices | 2025-08-07 23:13:11 | 313 | Stale |
| customer_payment_informations | 2025-08-07 23:13:11 | 313 | Stale |
| sales_quotas | 2025-08-07 23:13:11 | 313 | Stale |
| portal_orders | 2026-03-13 14:23:42 | 96 | Monitor |
| portal_invoices | 2026-03-13 14:23:42 | 96 | Monitor |
| products | 2026-05-08 18:15:34 | 40 | Monitor |
| smart_stacks | 2026-05-08 18:15:34 | 40 | Monitor |
| categories | 2026-05-08 18:15:35 | 40 | Monitor |
| collections | 2026-05-08 18:15:35 | 40 | Monitor |
| groups | 2026-05-08 18:15:35 | 40 | Monitor |
| trade_names | 2026-05-08 18:15:35 | 40 | Monitor |
| price_levels | 2026-06-10 12:22:14 | 7 | Fresh |
| customers | 2026-06-17 03:05:19 | 0 | Fresh |
| customer_favorites | 2026-06-17 03:05:21 | 0 | Fresh |
| inventories | 2026-06-17 19:34:15 | 0 | Fresh |

### Q-09_results.md

# Q-09 Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-09 — Import Health — Monthly Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 7
- **Run date**: 2026-06-17


| month | import_count |
| --- | --- |
| 2026-06-01 | 70 |
| 2026-05-01 | 115 |
| 2026-04-01 | 90 |
| 2026-03-01 | 90 |
| 2026-02-01 | 117 |
| 2026-01-01 | 166 |
| 2025-12-01 | 87 |

### Q-09_recent_results.md

# Q-09-recent Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-09-recent — Import Health — Recent Errors
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| created_at | data |
| --- | --- |
| 2026-06-17T19:34:15.303316 | ---
- - Inventory
  - - - :warning
      - 'Line 327: Product not found, record ignored., BaseItemCode=900375A'
    - - :warning
      - 'Line 330: Product not found, record ignored., BaseItemCode=200895A'
    - - :warning
      - 'Line 331: Product not found, record ignored., BaseItemCode=200899A'
    - - :warning
      - 'Line 332: Product not found, record ignored., BaseItemCode=201383A'
    - - :warning
      - 'Line 336: Product not found, record ignored., BaseItemCode=201735A'
    - - :warning
      - 'Line 338: Product not found, record ignored., BaseItemCode=202081A'
    - - :warning
      - 'Line 340: Product not found, record ignored., BaseItemCode=202149A'
    - - :warning
      - 'Line 342: Product not found, record ignored., BaseItemCode=202275A'
    - - :warning
      - 'Line 343: Product not found, record ignored., BaseItemCode=202357A'
    - - :warning
      - 'Line 346: Product not found, record ignored., BaseItemCode=202839A'
    - - :warning
      - 'Line 347: Product not found, record ignored., BaseItemCode=202842A'
    - - :warning
      - 'Line 348: Product not found, record ignored., BaseItemCode=202851A'
    - - :warning
      - 'Line 349: Product not found, record ignored., BaseItemCode=202864A'
    - - :warning
      - 'Line 350: Product not found, record ignored., BaseItemCode=202898A'
    - - :warning
      - 'Line 351: Product not found, record ignored., BaseItemCode=203249A'
    - - :warning
      - 'Line 352: Product not found, record ignored., BaseItemCode=203446A'
    - - :warning
      - 'Line 353: Product not found, record ignored., BaseItemCode=203542A'
    - - :warning
      - 'Line 354: Product not found, record ignored., BaseItemCode=203646A'
    - - :warning
      - 'Line 355: Product not found, record ignored., BaseItemCode=203753A'
    - - :warning
      - 'Line 356: Product not found, record ignored., BaseItemCode=203945A'
    - - :warning
      - 'Line 357: Product not found, record ignored., BaseItemCode=203962A'
    - - :warning
      - 'Line 359: Product not found, record ignored., BaseItemCode=204049A'
    - - :warning
      - 'Line 360: Product not found, record ignored., BaseItemCode=204077A'
    - - :warning
      - 'Line 363: Product not found, record ignored., BaseItemCode=204109A'
    - - :warning
      - 'Line 364: Product not found, record ignored., BaseItemCode=204141A'
    - - :warning
      - 'Line 365: Product not found, record ignored., BaseItemCode=204147A'
    - - :warning
      - 'Line 366: Product not found, record ignored., BaseItemCode=204195A'
    - - :warning
      - 'Line 370: Product not found, record ignored., BaseItemCode=204361A'
    - - :warning
      - 'Line 371: Product not found, record ignored., BaseItemCode=204375A'
    - - :warning
      - 'Line 372: Product not found, record ignored., BaseItemCode=204446A'
    - - :warning
      - 'Line 373: Product not found, record ignored., BaseItemCode=204447A'
    - - :warning
      - 'Line 374: Product not found, record ignored., BaseItemCode=204464A'
    - - :warning
      - 'Line 375: Product not found, record ignored., BaseItemCode=204466A'
    - - :warning
      - 'Line 376: Product not found, record ignored., BaseItemCode=204467A'
    - - :warning
      - 'Line 377: Product not found, record ignored., BaseItemCode=204539A'
    - - :warning
      - 'Line 378: Product not found, record ignored., BaseItemCode=204543A'
    - - :warning
      - 'Line 379: Product not found, record ignored., BaseItemCode=204544A'
    - - :warning
      - 'Line 380: Product not found, record ignored., BaseItemCode=204555A'
    - - :warning
      - 'Line 381: Product not found, record ignored., BaseItemCode=204587A'
    - - :warning
      - 'Line 382: Product not found, record ignored., BaseItemCode=204589A'
    - - :warning
      - 'Line 387: Product not found, record ignored., BaseItemCode=204708A'
    - - :warning
      - 'Line 390: Product not found, record ignored., BaseItemCode=205072A'
    - - :warning
      - 'Line 393: Product not found, record ignored., BaseItemCode=205327A'
    - - :warning
      - 'Line 394: Product not found, record ignored., BaseItemCode=205331A'
    - - :warning
      - 'Line 396: Product not found, record ignored., BaseItemCode=205621A'
    - - :warning
      - 'Line 397: Product not found, record ignored., BaseItemCode=205655A'
    - - :warning
      - 'Line 399: Product not found, record ignored., BaseItemCode=205843A'
    - - :warning
      - 'Line 400: Product not found, record ignored., BaseItemCode=205844A'
    - - :warning
      - 'Line 401: Product not found, record ignored., BaseItemCode=235003-5223A'
    - - :warning
      - 'Line 402: Product not found, record ignored., BaseItemCode=235112-5202A'
    - - :warning
      - 'Line 403: Product not found, record ignored., BaseItemCode=235112-6001A'
    - - :warning
      - 'Line 404: Product not found, record ignored., BaseItemCode=235112-6002A'
    - - :warning
      - 'Line 405: Product not found, record ignored., BaseItemCode=235112-6016A'
    - - :warning
      - 'Line 406: Product not found, record ignored., BaseItemCode=235997-2401A'
    - - :warning
      - 'Line 407: Product not found, record ignored., BaseItemCode=235997-3601A'
    - - :warning
      - 'Line 415: Product not found, record ignored., BaseItemCode=390249A'
    - - :warning
      - 'Line 417: Product not found, record ignored., BaseItemCode=39591A'
    - - :warning
      - 'Line 418: Product not found, record ignored., BaseItemCode=39615A'
    - - :warning
      - 'Line 419: Product not found, record ignored., BaseItemCode=39628A'
    - - :warning
      - 'Line 422: Product not found, record ignored., BaseItemCode=43256A'
    - - :warning
      - 'Line 425: Product not found, record ignored., BaseItemCode=43645A'
    - - :warning
      - 'Line 428: Product not found, record ignored., BaseItemCode=43682A'
    - - :warning
      - 'Line 429: Product not found, record ignored., BaseItemCode=43873A'
    - - :warning
      - 'Line 431: Product not found, record ignored., BaseItemCode=49619A'
    - - :warning
      - 'Line 436: Product not found, record ignored., BaseItemCode=86391A'
    - - :warning
      - 'Line 440: Product not found, record ignored., BaseItemCode=88968A'
    - - :warning
      - 'Line 442: Product not found, record ignored., BaseItemCode=91416A'
    - - :warning
      - 'Line 445: Product not found, record ignored., BaseItemCode=94465A'
    - - :warning
      - 'Line 448: Product not found, record ignored., BaseItemCode=97441A'
    - - :warning
      - 'Line 449: Product not found, record ignored., BaseItemCode=97442A'
    - - :warning
      - 'Line 450: Product not found, record ignored., BaseItemCode=97949A'
    - - :warning
      - 'Line 454: Product not found, record ignored., BaseItemCode=98441A'
    - - :warning
      - 'Line 457: Product not found, record ignored., BaseItemCode=99561A'
    - - :warning
      - 'Line 458: Product not found, record ignored., BaseItemCode=99562A'
    - - :warning
      - 'Line 465: Product not found, record ignored., BaseItemCode=200268A'
    - - :warning
      - 'Line 492: Product not found, record ignored., BaseItemCode=202274A'
    - - :warning
      - 'Line 497: Product not found, record ignored., BaseItemCode=202299A'
    - - :warning
      - 'Line 508: Product not found, record ignored., BaseItemCode=202633A'
    - - :warning
      - 'Line 509: Product not found, record ignored., BaseItemCode=202836A'
    - - :warning
      - 'Line 522: Product not found, record ignored., BaseItemCode=203187A'
    - - :warning
      - 'Line 523: Product not found, record ignored., BaseItemCode=203188A'
    - - :warning
      - 'Line 525: Product not found, record ignored., BaseItemCode=203221A'
    - - :warning
      - 'Line 526: Product not found, record ignored., BaseItemCode=203222A'
    - - :warning
      - 'Line 527: Product not found, record ignored., BaseItemCode=203246A'
    - - :warning
      - 'Line 528: Product not found, record ignored., BaseItemCode=203247A'
    - - :warning
      - 'Line 575: Product not found, record ignored., BaseItemCode=203998A'
    - - :warning
      - 'Line 577: Product not found, record ignored., BaseItemCode=204027A'
    - - :warning
      - 'Line 626: Product not found, record ignored., BaseItemCode=204362A'
    - - :warning
      - 'Line 637: Product not found, record ignored., BaseItemCode=204642A'
    - - :warning
      - 'Line 650: Product not found, record ignored., BaseItemCode=204895A'
    - - :warning
      - 'Line 669: Product not found, record ignored., BaseItemCode=205351A'
    - - :warning
      - 'Line 670: Product not found, record ignored., BaseItemCode=205363A'
    - - :warning
      - 'Line 675: Product not found, record ignored., BaseItemCode=205618A'
    - - :warning
      - 'Line 679: Product not found, record ignored., BaseItemCode=205643A'
    - - :warning
      - 'Line 689: Product not found, record ignored., BaseItemCode=205755A'
    - - :warning
      - 'Line 695: Product not found, record ignored., BaseItemCode=205766A'
    - - :warning
      - 'Line 725: Product not found, record ignored., BaseItemCode=206032A'
    - - :warning
      - 'Line 945: Product not found, record ignored., BaseItemCode=39499A'
    - - :warning
      - 'Line 949: Product not found, record ignored., BaseItemCode=39614A'
    - - :warning
      - 'Line 1106: Product not found, record ignored., BaseItemCode=91732A'
    - - :warning
      - 'Line 1107: Product not found, record ignored., BaseItemCode=91733A'
    - - :warning
      - 'Line 1127: Product not found, record ignored., BaseItemCode=94353A'
    - - :warning
      - 'Line 1136: Product not found, record ignored., BaseItemCode=95122A'
    - - :warning
      - 'Line 1146: Product not found, record ignored., BaseItemCode=96605A'
    - - :warning
      - 'Line 1147: Product not found, record ignored., BaseItemCode=96606A'
    - - :warning
      - 'Line 1148: Product not found, record ignored., BaseItemCode=96607A'
    - - :warning
      - 'Line 1149: Product not found, record ignored., BaseItemCode=96608A'
    - - :warning
      - 'Line 1151: Product not found, record ignored., BaseItemCode=96726A'
    - - :warning
      - 'Line 1158: Product not found, record ignored., BaseItemCode=97374A'
    - - :warning
      - 'Line 1160: Product not found, record ignored., BaseItemCode=97395A'
    - - :warning
      - 'Line 1161: Product not found, record ignored., BaseItemCode=97396A'
    - - :warning
      - 'Line 1162: Product not found, record ignored., BaseItemCode=97397A'
    - - :warning
      - 'Line 1173: Product not found, record ignored., BaseItemCode=97914A'
    - - :warning
      - 'Line 1237: Product not found, record ignored., BaseItemCode=200323A'
    - - :warning
      - 'Line 1239: Product not found, record ignored., BaseItemCode=200367A'
    - - :warning
      - 'Line 1240: Product not found, record ignored., BaseItemCode=200369A'
    - - :warning
      - 'Line 1241: Product not found, record ignored., BaseItemCode=200373A'
    - - :warning
      - 'Line 1242: Product not found, record ignored., BaseItemCode=200374A'
    - - :warning
      - 'Line 1243: Product not found, record ignored., BaseItemCode=200397A'
    - - :warning
      - 'Line 1244: Product not found, record ignored., BaseItemCode=200402A'
    - - :warning
      - 'Line 1245: Product not found, record ignored., BaseItemCode=200775A'
    - - :warning
      - 'Line 1246: Product not found, record ignored., BaseItemCode=200944A'
    - - :warning
      - 'Line 1247: Product not found, record ignored., BaseItemCode=201252A'
    - - :warning
      - 'Line 1248: Product not found, record ignored., BaseItemCode=201271A'
    - - :warning
      - 'Line 1249: Product not found, record ignored., BaseItemCode=201296A'
    - - :warning
      - 'Line 1250: Product not found, record ignored., BaseItemCode=201297A'
    - - :warning
      - 'Line 1254: Product not found, record ignored., BaseItemCode=201466A'
    - - :warning
      - 'Line 1255: Product not found, record ignored., BaseItemCode=201712A'
    - - :warning
      - 'Line 1257: Product not found, record ignored., BaseItemCode=201734A'
    - - :warning
      - 'Line 1258: Product not found, record ignored., BaseItemCode=201736A'
    - - :warning
      - 'Line 1259: Product not found, record ignored., BaseItemCode=201737A'
    - - :warning
      - 'Line 1261: Product not found, record ignored., BaseItemCode=202156A'
    - - :warning
      - 'Line 1262: Product not found, record ignored., BaseItemCode=202164A'
    - - :warning
      - 'Line 1263: Product not found, record ignored., BaseItemCode=202176A'
    - - :warning
      - 'Line 1265: Product not found, record ignored., BaseItemCode=202634A'
    - - :warning
      - 'Line 1266: Product not found, record ignored., BaseItemCode=202635A'
    - - :warning
      - 'Line 1267: Product not found, record ignored., BaseItemCode=202844A'
    - - :warning
      - 'Line 1268: Product not found, record ignored., BaseItemCode=202953A'
    - - :warning
      - 'Line 1269: Product not found, record ignored., BaseItemCode=203108A'
    - - :warning
      - 'Line 1270: Product not found, record ignored., BaseItemCode=203185A'
    - - :warning
      - 'Line 1272: Product not found, record ignored., BaseItemCode=203475A'
    - - :warning
      - 'Line 1274: Product not found, record ignored., BaseItemCode=203666A'
    - - :warning
      - 'Line 1275: Product not found, record ignored., BaseItemCode=203729A'
    - - :warning
      - 'Line 1276: Product not found, record ignored., BaseItemCode=203916A'
    - - :warning
      - 'Line 1277: Product not found, record ignored., BaseItemCode=203963A'
    - - :warning
      - 'Line 1279: Product not found, record ignored., BaseItemCode=204025A'
    - - :warning
      - 'Line 1280: Product not found, record ignored., BaseItemCode=204026A'
    - - :warning
      - 'Line 1281: Product not found, record ignored., BaseItemCode=204061A'
    - - :warning
      - 'Line 1282: Product not found, record ignored., BaseItemCode=204065'
    - - :warning
      - 'Line 1283: Product not found, record ignored., BaseItemCode=204069'
    - - :warning
      - 'Line 1284: Product not found, record ignored., BaseItemCode=204071'
    - - :warning
      - 'Line 1286: Product not found, record ignored., BaseItemCode=204102A'
    - - :warning
      - 'Line 1287: Product not found, record ignored., BaseItemCode=204105A'
    - - :warning
      - 'Line 1289: Product not found, record ignored., BaseItemCode=204213A'
    - - :warning
      - 'Line 1290: Product not found, record ignored., BaseItemCode=204214A'
    - - :warning
      - 'Line 1292: Product not found, record ignored., BaseItemCode=204472A'
    - - :warning
      - 'Line 1293: Product not found, record ignored., BaseItemCode=204554A'
    - - :warning
      - 'Line 1294: Product not found, record ignored., BaseItemCode=204569A'
    - - :warning
      - 'Line 1295: Product not found, record ignored., BaseItemCode=204586A'
    - - :warning
      - 'Line 1296: Product not found, record ignored., BaseItemCode=204595A'
    - - :warning
      - 'Line 1299: Product not found, record ignored., BaseItemCode=204701A'
    - - :warning
      - 'Line 1300: Product not found, record ignored., BaseItemCode=204702A'
    - - :warning
      - 'Line 1302: Product not found, record ignored., BaseItemCode=204923A'
    - - :warning
      - 'Line 1303: Product not found, record ignored., BaseItemCode=204924A'
    - - :warning
      - 'Line 1307: Product not found, record ignored., BaseItemCode=205588A'
    - - :warning
      - 'Line 1310: Product not found, record ignored., BaseItemCode=205841A'
    - - :warning
      - 'Line 1311: Product not found, record ignored., BaseItemCode=206089A'
    - - :warning
      - 'Line 1316: Product not found, record ignored., BaseItemCode=235003-4401A'
    - - :warning
      - 'Line 1317: Product not found, record ignored., BaseItemCode=235003-5201A'
    - - :warning
      - 'Line 1318: Product not found, record ignored., BaseItemCode=235003-5202A'
    - - :warning
      - 'Line 1319: Product not found, record ignored., BaseItemCode=235003-5218A'
    - - :warning
      - 'Line 1320: Product not found, record ignored., BaseItemCode=235100-5201A'
    - - :warning
      - 'Line 1321: Product not found, record ignored., BaseItemCode=235100-5202A'
    - - :warning
      - 'Line 1322: Product not found, record ignored., BaseItemCode=235112-5201A'
    - - :warning
      - 'Line 1323: Product not found, record ignored., BaseItemCode=235112-5216A'
    - - :warning
      - 'Line 1324: Product not found, record ignored., BaseItemCode=235112-5225A'
    - - :warning
      - 'Line 1325: Product not found, record ignored., BaseItemCode=235112-6025A'
    - - :warning
      - 'Line 1326: Product not found, record ignored., BaseItemCode=235997-1201A'
    - - :warning
      - 'Line 1327: Product not found, record ignored., BaseItemCode=235997-1202A'
    - - :warning
      - 'Line 1328: Product not found, record ignored., BaseItemCode=235997-2402A'
    - - :warning
      - 'Line 1329: Product not found, record ignored., BaseItemCode=235997-3602A'
    - - :warning
      - 'Line 1330: Product not found, record ignored., BaseItemCode=31372A'
    - - :warning
      - 'Line 1333: Product not found, record ignored., BaseItemCode=390024A'
    - - :warning
      - 'Line 1337: Product not found, record ignored., BaseItemCode=39249A'
    - - :warning
      - 'Line 1340: Product not found, record ignored., BaseItemCode=43197A'
    - - :warning
      - 'Line 1341: Product not found, record ignored., BaseItemCode=43311A'
    - - :warning
      - 'Line 1342: Product not found, record ignored., BaseItemCode=43617A'
    - - :warning
      - 'Line 1344: Product not found, record ignored., BaseItemCode=83241A'
    - - :warning
      - 'Line 1345: Product not found, record ignored., BaseItemCode=83733A'
    - - :warning
      - 'Line 1347: Product not found, record ignored., BaseItemCode=91046A'
    - - :warning
      - 'Line 1350: Product not found, record ignored., BaseItemCode=93374A'
    - - :warning
      - 'Line 1351: Product not found, record ignored., BaseItemCode=94304A'
    - - :warning
      - 'Line 1354: Product not found, record ignored., BaseItemCode=95143A'
    - - :warning
      - 'Line 1355: Product not found, record ignored., BaseItemCode=95996A'
    - - :warning
      - 'Line 1357: Product not found, record ignored., BaseItemCode=96801A'
    - - :warning
      - 'Line 1358: Product not found, record ignored., BaseItemCode=96932A'
    - - :warning
      - 'Line 1362: Product not found, record ignored., BaseItemCode=98735A'
    - - :warning
      - 'Line 1364: Product not found, record ignored., BaseItemCode=99364A'
    - - :warning
      - 'Line 1368: Product not found, record ignored., BaseItemCode=205842A'
    - - :warning
      - 'Line 1636: Product not found, record ignored., BaseItemCode=235848-6602A'
    - - :warning
      - 'Line 1637: Product not found, record ignored., BaseItemCode=235848-8402A'
    - - :warning
      - 'Line 1672: Product not found, record ignored., BaseItemCode=91988A'
 |
| 2026-06-17T15:06:41.901402 | ---
- - Inventory
  - - - :warning
      - 'Line 310: Product not found, record ignored., BaseItemCode=900375A'
    - - :warning
      - 'Line 313: Product not found, record ignored., BaseItemCode=200895A'
    - - :warning
      - 'Line 314: Product not found, record ignored., BaseItemCode=200899A'
    - - :warning
      - 'Line 315: Product not found, record ignored., BaseItemCode=201383A'
    - - :warning
      - 'Line 319: Product not found, record ignored., BaseItemCode=201735A'
    - - :warning
      - 'Line 321: Product not found, record ignored., BaseItemCode=202081A'
    - - :warning
      - 'Line 323: Product not found, record ignored., BaseItemCode=202149A'
    - - :warning
      - 'Line 325: Product not found, record ignored., BaseItemCode=202275A'
    - - :warning
      - 'Line 326: Product not found, record ignored., BaseItemCode=202357A'
    - - :warning
      - 'Line 329: Product not found, record ignored., BaseItemCode=202839A'
    - - :warning
      - 'Line 330: Product not found, record ignored., BaseItemCode=202842A'
    - - :warning
      - 'Line 331: Product not found, record ignored., BaseItemCode=202851A'
    - - :warning
      - 'Line 332: Product not found, record ignored., BaseItemCode=202864A'
    - - :warning
      - 'Line 333: Product not found, record ignored., BaseItemCode=202898A'
    - - :warning
      - 'Line 334: Product not found, record ignored., BaseItemCode=203249A'
    - - :warning
      - 'Line 335: Product not found, record ignored., BaseItemCode=203446A'
    - - :warning
      - 'Line 336: Product not found, record ignored., BaseItemCode=203542A'
    - - :warning
      - 'Line 337: Product not found, record ignored., BaseItemCode=203646A'
    - - :warning
      - 'Line 338: Product not found, record ignored., BaseItemCode=203753A'
    - - :warning
      - 'Line 339: Product not found, record ignored., BaseItemCode=203945A'
    - - :warning
      - 'Line 340: Product not found, record ignored., BaseItemCode=203962A'
    - - :warning
      - 'Line 342: Product not found, record ignored., BaseItemCode=204049A'
    - - :warning
      - 'Line 343: Product not found, record ignored., BaseItemCode=204077A'
    - - :warning
      - 'Line 346: Product not found, record ignored., BaseItemCode=204109A'
    - - :warning
      - 'Line 347: Product not found, record ignored., BaseItemCode=204141A'
    - - :warning
      - 'Line 348: Product not found, record ignored., BaseItemCode=204147A'
    - - :warning
      - 'Line 349: Product not found, record ignored., BaseItemCode=204195A'
    - - :warning
      - 'Line 353: Product not found, record ignored., BaseItemCode=204361A'
    - - :warning
      - 'Line 354: Product not found, record ignored., BaseItemCode=204375A'
    - - :warning
      - 'Line 355: Product not found, record ignored., BaseItemCode=204446A'
    - - :warning
      - 'Line 356: Product not found, record ignored., BaseItemCode=204447A'
    - - :warning
      - 'Line 357: Product not found, record ignored., BaseItemCode=204464A'
    - - :warning
      - 'Line 358: Product not found, record ignored., BaseItemCode=204466A'
    - - :warning
      - 'Line 359: Product not found, record ignored., BaseItemCode=204467A'
    - - :warning
      - 'Line 360: Product not found, record ignored., BaseItemCode=204539A'
    - - :warning
      - 'Line 361: Product not found, record ignored., BaseItemCode=204543A'
    - - :warning
      - 'Line 362: Product not found, record ignored., BaseItemCode=204544A'
    - - :warning
      - 'Line 363: Product not found, record ignored., BaseItemCode=204555A'
    - - :warning
      - 'Line 364: Product not found, record ignored., BaseItemCode=204587A'
    - - :warning
      - 'Line 365: Product not found, record ignored., BaseItemCode=204589A'
    - - :warning
      - 'Line 370: Product not found, record ignored., BaseItemCode=204708A'
    - - :warning
      - 'Line 373: Product not found, record ignored., BaseItemCode=205072A'
    - - :warning
      - 'Line 376: Product not found, record ignored., BaseItemCode=205327A'
    - - :warning
      - 'Line 377: Product not found, record ignored., BaseItemCode=205331A'
    - - :warning
      - 'Line 379: Product not found, record ignored., BaseItemCode=205621A'
    - - :warning
      - 'Line 380: Product not found, record ignored., BaseItemCode=205655A'
    - - :warning
      - 'Line 382: Product not found, record ignored., BaseItemCode=205843A'
    - - :warning
      - 'Line 383: Product not found, record ignored., BaseItemCode=205844A'
    - - :warning
      - 'Line 384: Product not found, record ignored., BaseItemCode=235003-5223A'
    - - :warning
      - 'Line 385: Product not found, record ignored., BaseItemCode=235112-5202A'
    - - :warning
      - 'Line 386: Product not found, record ignored., BaseItemCode=235112-6001A'
    - - :warning
      - 'Line 387: Product not found, record ignored., BaseItemCode=235112-6002A'
    - - :warning
      - 'Line 388: Product not found, record ignored., BaseItemCode=235112-6016A'
    - - :warning
      - 'Line 389: Product not found, record ignored., BaseItemCode=235997-2401A'
    - - :warning
      - 'Line 390: Product not found, record ignored., BaseItemCode=235997-3601A'
    - - :warning
      - 'Line 398: Product not found, record ignored., BaseItemCode=390249A'
    - - :warning
      - 'Line 400: Product not found, record ignored., BaseItemCode=39591A'
    - - :warning
      - 'Line 401: Product not found, record ignored., BaseItemCode=39615A'
    - - :warning
      - 'Line 402: Product not found, record ignored., BaseItemCode=39628A'
    - - :warning
      - 'Line 405: Product not found, record ignored., BaseItemCode=43256A'
    - - :warning
      - 'Line 408: Product not found, record ignored., BaseItemCode=43645A'
    - - :warning
      - 'Line 411: Product not found, record ignored., BaseItemCode=43682A'
    - - :warning
      - 'Line 412: Product not found, record ignored., BaseItemCode=43873A'
    - - :warning
      - 'Line 414: Product not found, record ignored., BaseItemCode=49619A'
    - - :warning
      - 'Line 419: Product not found, record ignored., BaseItemCode=86391A'
    - - :warning
      - 'Line 423: Product not found, record ignored., BaseItemCode=88968A'
    - - :warning
      - 'Line 425: Product not found, record ignored., BaseItemCode=91416A'
    - - :warning
      - 'Line 428: Product not found, record ignored., BaseItemCode=94465A'
    - - :warning
      - 'Line 431: Product not found, record ignored., BaseItemCode=97441A'
    - - :warning
      - 'Line 432: Product not found, record ignored., BaseItemCode=97442A'
    - - :warning
      - 'Line 433: Product not found, record ignored., BaseItemCode=97949A'
    - - :warning
      - 'Line 437: Product not found, record ignored., BaseItemCode=98441A'
    - - :warning
      - 'Line 440: Product not found, record ignored., BaseItemCode=99561A'
    - - :warning
      - 'Line 441: Product not found, record ignored., BaseItemCode=99562A'
    - - :warning
      - 'Line 448: Product not found, record ignored., BaseItemCode=200268A'
    - - :warning
      - 'Line 475: Product not found, record ignored., BaseItemCode=202274A'
    - - :warning
      - 'Line 480: Product not found, record ignored., BaseItemCode=202299A'
    - - :warning
      - 'Line 491: Product not found, record ignored., BaseItemCode=202633A'
    - - :warning
      - 'Line 492: Product not found, record ignored., BaseItemCode=202836A'
    - - :warning
      - 'Line 505: Product not found, record ignored., BaseItemCode=203187A'
    - - :warning
      - 'Line 506: Product not found, record ignored., BaseItemCode=203188A'
    - - :warning
      - 'Line 508: Product not found, record ignored., BaseItemCode=203221A'
    - - :warning
      - 'Line 509: Product not found, record ignored., BaseItemCode=203222A'
    - - :warning
      - 'Line 510: Product not found, record ignored., BaseItemCode=203246A'
    - - :warning
      - 'Line 511: Product not found, record ignored., BaseItemCode=203247A'
    - - :warning
      - 'Line 558: Product not found, record ignored., BaseItemCode=203998A'
    - - :warning
      - 'Line 560: Product not found, record ignored., BaseItemCode=204027A'
    - - :warning
      - 'Line 609: Product not found, record ignored., BaseItemCode=204362A'
    - - :warning
      - 'Line 620: Product not found, record ignored., BaseItemCode=204642A'
    - - :warning
      - 'Line 633: Product not found, record ignored., BaseItemCode=204895A'
    - - :warning
      - 'Line 654: Product not found, record ignored., BaseItemCode=205351A'
    - - :warning
      - 'Line 655: Product not found, record ignored., BaseItemCode=205363A'
    - - :warning
      - 'Line 660: Product not found, record ignored., BaseItemCode=205618A'
    - - :warning
      - 'Line 664: Product not found, record ignored., BaseItemCode=205643A'
    - - :warning
      - 'Line 675: Product not found, record ignored., BaseItemCode=205755A'
    - - :warning
      - 'Line 681: Product not found, record ignored., BaseItemCode=205766A'
    - - :warning
      - 'Line 712: Product not found, record ignored., BaseItemCode=206032A'
    - - :warning
      - 'Line 935: Product not found, record ignored., BaseItemCode=39499A'
    - - :warning
      - 'Line 939: Product not found, record ignored., BaseItemCode=39614A'
    - - :warning
      - 'Line 1100: Product not found, record ignored., BaseItemCode=91732A'
    - - :warning
      - 'Line 1101: Product not found, record ignored., BaseItemCode=91733A'
    - - :warning
      - 'Line 1121: Product not found, record ignored., BaseItemCode=94353A'
    - - :warning
      - 'Line 1130: Product not found, record ignored., BaseItemCode=95122A'
    - - :warning
      - 'Line 1140: Product not found, record ignored., BaseItemCode=96605A'
    - - :warning
      - 'Line 1141: Product not found, record ignored., BaseItemCode=96606A'
    - - :warning
      - 'Line 1142: Product not found, record ignored., BaseItemCode=96607A'
    - - :warning
      - 'Line 1143: Product not found, record ignored., BaseItemCode=96608A'
    - - :warning
      - 'Line 1145: Product not found, record ignored., BaseItemCode=96726A'
    - - :warning
      - 'Line 1152: Product not found, record ignored., BaseItemCode=97374A'
    - - :warning
      - 'Line 1154: Product not found, record ignored., BaseItemCode=97395A'
    - - :warning
      - 'Line 1155: Product not found, record ignored., BaseItemCode=97396A'
    - - :warning
      - 'Line 1156: Product not found, record ignored., BaseItemCode=97397A'
    - - :warning
      - 'Line 1167: Product not found, record ignored., BaseItemCode=97914A'
    - - :warning
      - 'Line 1233: Product not found, record ignored., BaseItemCode=200323A'
    - - :warning
      - 'Line 1235: Product not found, record ignored., BaseItemCode=200367A'
    - - :warning
      - 'Line 1236: Product not found, record ignored., BaseItemCode=200369A'
    - - :warning
      - 'Line 1237: Product not found, record ignored., BaseItemCode=200373A'
    - - :warning
      - 'Line 1238: Product not found, record ignored., BaseItemCode=200374A'
    - - :warning
      - 'Line 1239: Product not found, record ignored., BaseItemCode=200397A'
    - - :warning
      - 'Line 1240: Product not found, record ignored., BaseItemCode=200402A'
    - - :warning
      - 'Line 1241: Product not found, record ignored., BaseItemCode=200775A'
    - - :warning
      - 'Line 1242: Product not found, record ignored., BaseItemCode=200944A'
    - - :warning
      - 'Line 1243: Product not found, record ignored., BaseItemCode=201252A'
    - - :warning
      - 'Line 1244: Product not found, record ignored., BaseItemCode=201271A'
    - - :warning
      - 'Line 1245: Product not found, record ignored., BaseItemCode=201296A'
    - - :warning
      - 'Line 1246: Product not found, record ignored., BaseItemCode=201297A'
    - - :warning
      - 'Line 1250: Product not found, record ignored., BaseItemCode=201466A'
    - - :warning
      - 'Line 1251: Product not found, record ignored., BaseItemCode=201712A'
    - - :warning
      - 'Line 1253: Product not found, record ignored., BaseItemCode=201734A'
    - - :warning
      - 'Line 1254: Product not found, record ignored., BaseItemCode=201736A'
    - - :warning
      - 'Line 1255: Product not found, record ignored., BaseItemCode=201737A'
    - - :warning
      - 'Line 1257: Product not found, record ignored., BaseItemCode=202156A'
    - - :warning
      - 'Line 1258: Product not found, record ignored., BaseItemCode=202164A'
    - - :warning
      - 'Line 1259: Product not found, record ignored., BaseItemCode=202176A'
    - - :warning
      - 'Line 1261: Product not found, record ignored., BaseItemCode=202634A'
    - - :warning
      - 'Line 1262: Product not found, record ignored., BaseItemCode=202635A'
    - - :warning
      - 'Line 1263: Product not found, record ignored., BaseItemCode=202844A'
    - - :warning
      - 'Line 1264: Product not found, record ignored., BaseItemCode=202953A'
    - - :warning
      - 'Line 1265: Product not found, record ignored., BaseItemCode=203108A'
    - - :warning
      - 'Line 1266: Product not found, record ignored., BaseItemCode=203185A'
    - - :warning
      - 'Line 1268: Product not found, record ignored., BaseItemCode=203475A'
    - - :warning
      - 'Line 1270: Product not found, record ignored., BaseItemCode=203666A'
    - - :warning
      - 'Line 1271: Product not found, record ignored., BaseItemCode=203729A'
    - - :warning
      - 'Line 1272: Product not found, record ignored., BaseItemCode=203916A'
    - - :warning
      - 'Line 1273: Product not found, record ignored., BaseItemCode=203963A'
    - - :warning
      - 'Line 1275: Product not found, record ignored., BaseItemCode=204025A'
    - - :warning
      - 'Line 1276: Product not found, record ignored., BaseItemCode=204026A'
    - - :warning
      - 'Line 1277: Product not found, record ignored., BaseItemCode=204061A'
    - - :warning
      - 'Line 1278: Product not found, record ignored., BaseItemCode=204065'
    - - :warning
      - 'Line 1279: Product not found, record ignored., BaseItemCode=204069'
    - - :warning
      - 'Line 1280: Product not found, record ignored., BaseItemCode=204071'
    - - :warning
      - 'Line 1282: Product not found, record ignored., BaseItemCode=204102A'
    - - :warning
      - 'Line 1283: Product not found, record ignored., BaseItemCode=204105A'
    - - :warning
      - 'Line 1285: Product not found, record ignored., BaseItemCode=204213A'
    - - :warning
      - 'Line 1286: Product not found, record ignored., BaseItemCode=204214A'
    - - :warning
      - 'Line 1288: Product not found, record ignored., BaseItemCode=204472A'
    - - :warning
      - 'Line 1289: Product not found, record ignored., BaseItemCode=204554A'
    - - :warning
      - 'Line 1290: Product not found, record ignored., BaseItemCode=204569A'
    - - :warning
      - 'Line 1291: Product not found, record ignored., BaseItemCode=204586A'
    - - :warning
      - 'Line 1292: Product not found, record ignored., BaseItemCode=204595A'
    - - :warning
      - 'Line 1295: Product not found, record ignored., BaseItemCode=204701A'
    - - :warning
      - 'Line 1296: Product not found, record ignored., BaseItemCode=204702A'
    - - :warning
      - 'Line 1298: Product not found, record ignored., BaseItemCode=204923A'
    - - :warning
      - 'Line 1299: Product not found, record ignored., BaseItemCode=204924A'
    - - :warning
      - 'Line 1303: Product not found, record ignored., BaseItemCode=205588A'
    - - :warning
      - 'Line 1306: Product not found, record ignored., BaseItemCode=205841A'
    - - :warning
      - 'Line 1307: Product not found, record ignored., BaseItemCode=206089A'
    - - :warning
      - 'Line 1312: Product not found, record ignored., BaseItemCode=235003-4401A'
    - - :warning
      - 'Line 1313: Product not found, record ignored., BaseItemCode=235003-5201A'
    - - :warning
      - 'Line 1314: Product not found, record ignored., BaseItemCode=235003-5202A'
    - - :warning
      - 'Line 1315: Product not found, record ignored., BaseItemCode=235003-5218A'
    - - :warning
      - 'Line 1316: Product not found, record ignored., BaseItemCode=235100-5201A'
    - - :warning
      - 'Line 1317: Product not found, record ignored., BaseItemCode=235100-5202A'
    - - :warning
      - 'Line 1318: Product not found, record ignored., BaseItemCode=235112-5201A'
    - - :warning
      - 'Line 1319: Product not found, record ignored., BaseItemCode=235112-5216A'
    - - :warning
      - 'Line 1320: Product not found, record ignored., BaseItemCode=235112-5225A'
    - - :warning
      - 'Line 1321: Product not found, record ignored., BaseItemCode=235112-6025A'
    - - :warning
      - 'Line 1322: Product not found, record ignored., BaseItemCode=235997-1201A'
    - - :warning
      - 'Line 1323: Product not found, record ignored., BaseItemCode=235997-1202A'
    - - :warning
      - 'Line 1324: Product not found, record ignored., BaseItemCode=235997-2402A'
    - - :warning
      - 'Line 1325: Product not found, record ignored., BaseItemCode=235997-3602A'
    - - :warning
      - 'Line 1326: Product not found, record ignored., BaseItemCode=31372A'
    - - :warning
      - 'Line 1329: Product not found, record ignored., BaseItemCode=390024A'
    - - :warning
      - 'Line 1333: Product not found, record ignored., BaseItemCode=39249A'
    - - :warning
      - 'Line 1336: Product not found, record ignored., BaseItemCode=43197A'
    - - :warning
      - 'Line 1337: Product not found, record ignored., BaseItemCode=43311A'
    - - :warning
      - 'Line 1338: Product not found, record ignored., BaseItemCode=43617A'
    - - :warning
      - 'Line 1340: Product not found, record ignored., BaseItemCode=83241A'
    - - :warning
      - 'Line 1341: Product not found, record ignored., BaseItemCode=83733A'
    - - :warning
      - 'Line 1343: Product not found, record ignored., BaseItemCode=91046A'
    - - :warning
      - 'Line 1346: Product not found, record ignored., BaseItemCode=93374A'
    - - :warning
      - 'Line 1347: Product not found, record ignored., BaseItemCode=94304A'
    - - :warning
      - 'Line 1350: Product not found, record ignored., BaseItemCode=95143A'
    - - :warning
      - 'Line 1351: Product not found, record ignored., BaseItemCode=95996A'
    - - :warning
      - 'Line 1353: Product not found, record ignored., BaseItemCode=96801A'
    - - :warning
      - 'Line 1354: Product not found, record ignored., BaseItemCode=96932A'
    - - :warning
      - 'Line 1358: Product not found, record ignored., BaseItemCode=98735A'
    - - :warning
      - 'Line 1360: Product not found, record ignored., BaseItemCode=99364A'
    - - :warning
      - 'Line 1364: Product not found, record ignored., BaseItemCode=205842A'
    - - :warning
      - 'Line 1636: Product not found, record ignored., BaseItemCode=235848-6602A'
    - - :warning
      - 'Line 1637: Product not found, record ignored., BaseItemCode=235848-8402A'
    - - :warning
      - 'Line 1672: Product not found, record ignored., BaseItemCode=91988A'
 |
| 2026-06-17T09:05:18.181121 | ---
- - Inventory
  - - - :warning
      - 'Line 293: Product not found, record ignored., BaseItemCode=900375A'
    - - :warning
      - 'Line 296: Product not found, record ignored., BaseItemCode=200895A'
    - - :warning
      - 'Line 297: Product not found, record ignored., BaseItemCode=200899A'
    - - :warning
      - 'Line 298: Product not found, record ignored., BaseItemCode=201383A'
    - - :warning
      - 'Line 302: Product not found, record ignored., BaseItemCode=201735A'
    - - :warning
      - 'Line 304: Product not found, record ignored., BaseItemCode=202081A'
    - - :warning
      - 'Line 306: Product not found, record ignored., BaseItemCode=202149A'
    - - :warning
      - 'Line 308: Product not found, record ignored., BaseItemCode=202275A'
    - - :warning
      - 'Line 309: Product not found, record ignored., BaseItemCode=202357A'
    - - :warning
      - 'Line 312: Product not found, record ignored., BaseItemCode=202839A'
    - - :warning
      - 'Line 313: Product not found, record ignored., BaseItemCode=202842A'
    - - :warning
      - 'Line 314: Product not found, record ignored., BaseItemCode=202851A'
    - - :warning
      - 'Line 315: Product not found, record ignored., BaseItemCode=202864A'
    - - :warning
      - 'Line 316: Product not found, record ignored., BaseItemCode=202898A'
    - - :warning
      - 'Line 317: Product not found, record ignored., BaseItemCode=203249A'
    - - :warning
      - 'Line 318: Product not found, record ignored., BaseItemCode=203446A'
    - - :warning
      - 'Line 319: Product not found, record ignored., BaseItemCode=203542A'
    - - :warning
      - 'Line 320: Product not found, record ignored., BaseItemCode=203646A'
    - - :warning
      - 'Line 321: Product not found, record ignored., BaseItemCode=203753A'
    - - :warning
      - 'Line 322: Product not found, record ignored., BaseItemCode=203945A'
    - - :warning
      - 'Line 323: Product not found, record ignored., BaseItemCode=203962A'
    - - :warning
      - 'Line 325: Product not found, record ignored., BaseItemCode=204049A'
    - - :warning
      - 'Line 326: Product not found, record ignored., BaseItemCode=204077A'
    - - :warning
      - 'Line 329: Product not found, record ignored., BaseItemCode=204109A'
    - - :warning
      - 'Line 330: Product not found, record ignored., BaseItemCode=204141A'
    - - :warning
      - 'Line 331: Product not found, record ignored., BaseItemCode=204147A'
    - - :warning
      - 'Line 332: Product not found, record ignored., BaseItemCode=204195A'
    - - :warning
      - 'Line 336: Product not found, record ignored., BaseItemCode=204361A'
    - - :warning
      - 'Line 337: Product not found, record ignored., BaseItemCode=204375A'
    - - :warning
      - 'Line 338: Product not found, record ignored., BaseItemCode=204446A'
    - - :warning
      - 'Line 339: Product not found, record ignored., BaseItemCode=204447A'
    - - :warning
      - 'Line 340: Product not found, record ignored., BaseItemCode=204464A'
    - - :warning
      - 'Line 341: Product not found, record ignored., BaseItemCode=204466A'
    - - :warning
      - 'Line 342: Product not found, record ignored., BaseItemCode=204467A'
    - - :warning
      - 'Line 343: Product not found, record ignored., BaseItemCode=204539A'
    - - :warning
      - 'Line 344: Product not found, record ignored., BaseItemCode=204543A'
    - - :warning
      - 'Line 345: Product not found, record ignored., BaseItemCode=204544A'
    - - :warning
      - 'Line 346: Product not found, record ignored., BaseItemCode=204555A'
    - - :warning
      - 'Line 347: Product not found, record ignored., BaseItemCode=204587A'
    - - :warning
      - 'Line 348: Product not found, record ignored., BaseItemCode=204589A'
    - - :warning
      - 'Line 353: Product not found, record ignored., BaseItemCode=204708A'
    - - :warning
      - 'Line 356: Product not found, record ignored., BaseItemCode=205072A'
    - - :warning
      - 'Line 359: Product not found, record ignored., BaseItemCode=205327A'
    - - :warning
      - 'Line 360: Product not found, record ignored., BaseItemCode=205331A'
    - - :warning
      - 'Line 362: Product not found, record ignored., BaseItemCode=205621A'
    - - :warning
      - 'Line 363: Product not found, record ignored., BaseItemCode=205655A'
    - - :warning
      - 'Line 365: Product not found, record ignored., BaseItemCode=205843A'
    - - :warning
      - 'Line 366: Product not found, record ignored., BaseItemCode=205844A'
    - - :warning
      - 'Line 367: Product not found, record ignored., BaseItemCode=235003-5223A'
    - - :warning
      - 'Line 368: Product not found, record ignored., BaseItemCode=235112-5202A'
    - - :warning
      - 'Line 369: Product not found, record ignored., BaseItemCode=235112-6001A'
    - - :warning
      - 'Line 370: Product not found, record ignored., BaseItemCode=235112-6002A'
    - - :warning
      - 'Line 371: Product not found, record ignored., BaseItemCode=235112-6016A'
    - - :warning
      - 'Line 372: Product not found, record ignored., BaseItemCode=235997-2401A'
    - - :warning
      - 'Line 373: Product not found, record ignored., BaseItemCode=235997-3601A'
    - - :warning
      - 'Line 381: Product not found, record ignored., BaseItemCode=390249A'
    - - :warning
      - 'Line 383: Product not found, record ignored., BaseItemCode=39591A'
    - - :warning
      - 'Line 384: Product not found, record ignored., BaseItemCode=39615A'
    - - :warning
      - 'Line 385: Product not found, record ignored., BaseItemCode=39628A'
    - - :warning
      - 'Line 388: Product not found, record ignored., BaseItemCode=43256A'
    - - :warning
      - 'Line 391: Product not found, record ignored., BaseItemCode=43645A'
    - - :warning
      - 'Line 394: Product not found, record ignored., BaseItemCode=43682A'
    - - :warning
      - 'Line 395: Product not found, record ignored., BaseItemCode=43873A'
    - - :warning
      - 'Line 397: Product not found, record ignored., BaseItemCode=49619A'
    - - :warning
      - 'Line 402: Product not found, record ignored., BaseItemCode=86391A'
    - - :warning
      - 'Line 406: Product not found, record ignored., BaseItemCode=88968A'
    - - :warning
      - 'Line 408: Product not found, record ignored., BaseItemCode=91416A'
    - - :warning
      - 'Line 411: Product not found, record ignored., BaseItemCode=94465A'
    - - :warning
      - 'Line 414: Product not found, record ignored., BaseItemCode=97441A'
    - - :warning
      - 'Line 415: Product not found, record ignored., BaseItemCode=97442A'
    - - :warning
      - 'Line 416: Product not found, record ignored., BaseItemCode=97949A'
    - - :warning
      - 'Line 420: Product not found, record ignored., BaseItemCode=98441A'
    - - :warning
      - 'Line 423: Product not found, record ignored., BaseItemCode=99561A'
    - - :warning
      - 'Line 424: Product not found, record ignored., BaseItemCode=99562A'
    - - :warning
      - 'Line 431: Product not found, record ignored., BaseItemCode=200268A'
    - - :warning
      - 'Line 458: Product not found, record ignored., BaseItemCode=202274A'
    - - :warning
      - 'Line 463: Product not found, record ignored., BaseItemCode=202299A'
    - - :warning
      - 'Line 476: Product not found, record ignored., BaseItemCode=202633A'
    - - :warning
      - 'Line 477: Product not found, record ignored., BaseItemCode=202836A'
    - - :warning
      - 'Line 490: Product not found, record ignored., BaseItemCode=203187A'
    - - :warning
      - 'Line 491: Product not found, record ignored., BaseItemCode=203188A'
    - - :warning
      - 'Line 493: Product not found, record ignored., BaseItemCode=203221A'
    - - :warning
      - 'Line 494: Product not found, record ignored., BaseItemCode=203222A'
    - - :warning
      - 'Line 495: Product not found, record ignored., BaseItemCode=203246A'
    - - :warning
      - 'Line 496: Product not found, record ignored., BaseItemCode=203247A'
    - - :warning
      - 'Line 543: Product not found, record ignored., BaseItemCode=203998A'
    - - :warning
      - 'Line 545: Product not found, record ignored., BaseItemCode=204027A'
    - - :warning
      - 'Line 597: Product not found, record ignored., BaseItemCode=204362A'
    - - :warning
      - 'Line 608: Product not found, record ignored., BaseItemCode=204642A'
    - - :warning
      - 'Line 621: Product not found, record ignored., BaseItemCode=204895A'
    - - :warning
      - 'Line 642: Product not found, record ignored., BaseItemCode=205351A'
    - - :warning
      - 'Line 643: Product not found, record ignored., BaseItemCode=205363A'
    - - :warning
      - 'Line 648: Product not found, record ignored., BaseItemCode=205618A'
    - - :warning
      - 'Line 652: Product not found, record ignored., BaseItemCode=205643A'
    - - :warning
      - 'Line 663: Product not found, record ignored., BaseItemCode=205755A'
    - - :warning
      - 'Line 669: Product not found, record ignored., BaseItemCode=205766A'
    - - :warning
      - 'Line 700: Product not found, record ignored., BaseItemCode=206032A'
    - - :warning
      - 'Line 927: Product not found, record ignored., BaseItemCode=39499A'
    - - :warning
      - 'Line 931: Product not found, record ignored., BaseItemCode=39614A'
    - - :warning
      - 'Line 1093: Product not found, record ignored., BaseItemCode=91732A'
    - - :warning
      - 'Line 1094: Product not found, record ignored., BaseItemCode=91733A'
    - - :warning
      - 'Line 1114: Product not found, record ignored., BaseItemCode=94353A'
    - - :warning
      - 'Line 1123: Product not found, record ignored., BaseItemCode=95122A'
    - - :warning
      - 'Line 1134: Product not found, record ignored., BaseItemCode=96605A'
    - - :warning
      - 'Line 1135: Product not found, record ignored., BaseItemCode=96606A'
    - - :warning
      - 'Line 1136: Product not found, record ignored., BaseItemCode=96607A'
    - - :warning
      - 'Line 1137: Product not found, record ignored., BaseItemCode=96608A'
    - - :warning
      - 'Line 1139: Product not found, record ignored., BaseItemCode=96726A'
    - - :warning
      - 'Line 1146: Product not found, record ignored., BaseItemCode=97374A'
    - - :warning
      - 'Line 1148: Product not found, record ignored., BaseItemCode=97395A'
    - - :warning
      - 'Line 1149: Product not found, record ignored., BaseItemCode=97396A'
    - - :warning
      - 'Line 1150: Product not found, record ignored., BaseItemCode=97397A'
    - - :warning
      - 'Line 1162: Product not found, record ignored., BaseItemCode=97914A'
    - - :warning
      - 'Line 1230: Product not found, record ignored., BaseItemCode=200323A'
    - - :warning
      - 'Line 1232: Product not found, record ignored., BaseItemCode=200367A'
    - - :warning
      - 'Line 1233: Product not found, record ignored., BaseItemCode=200369A'
    - - :warning
      - 'Line 1234: Product not found, record ignored., BaseItemCode=200373A'
    - - :warning
      - 'Line 1235: Product not found, record ignored., BaseItemCode=200374A'
    - - :warning
      - 'Line 1236: Product not found, record ignored., BaseItemCode=200397A'
    - - :warning
      - 'Line 1237: Product not found, record ignored., BaseItemCode=200402A'
    - - :warning
      - 'Line 1238: Product not found, record ignored., BaseItemCode=200775A'
    - - :warning
      - 'Line 1239: Product not found, record ignored., BaseItemCode=200944A'
    - - :warning
      - 'Line 1240: Product not found, record ignored., BaseItemCode=201252A'
    - - :warning
      - 'Line 1241: Product not found, record ignored., BaseItemCode=201271A'
    - - :warning
      - 'Line 1242: Product not found, record ignored., BaseItemCode=201296A'
    - - :warning
      - 'Line 1243: Product not found, record ignored., BaseItemCode=201297A'
    - - :warning
      - 'Line 1247: Product not found, record ignored., BaseItemCode=201466A'
    - - :warning
      - 'Line 1248: Product not found, record ignored., BaseItemCode=201712A'
    - - :warning
      - 'Line 1250: Product not found, record ignored., BaseItemCode=201734A'
    - - :warning
      - 'Line 1251: Product not found, record ignored., BaseItemCode=201736A'
    - - :warning
      - 'Line 1252: Product not found, record ignored., BaseItemCode=201737A'
    - - :warning
      - 'Line 1254: Product not found, record ignored., BaseItemCode=202156A'
    - - :warning
      - 'Line 1255: Product not found, record ignored., BaseItemCode=202164A'
    - - :warning
      - 'Line 1256: Product not found, record ignored., BaseItemCode=202176A'
    - - :warning
      - 'Line 1258: Product not found, record ignored., BaseItemCode=202634A'
    - - :warning
      - 'Line 1259: Product not found, record ignored., BaseItemCode=202635A'
    - - :warning
      - 'Line 1260: Product not found, record ignored., BaseItemCode=202844A'
    - - :warning
      - 'Line 1261: Product not found, record ignored., BaseItemCode=202953A'
    - - :warning
      - 'Line 1262: Product not found, record ignored., BaseItemCode=203108A'
    - - :warning
      - 'Line 1263: Product not found, record ignored., BaseItemCode=203185A'
    - - :warning
      - 'Line 1265: Product not found, record ignored., BaseItemCode=203475A'
    - - :warning
      - 'Line 1267: Product not found, record ignored., BaseItemCode=203666A'
    - - :warning
      - 'Line 1268: Product not found, record ignored., BaseItemCode=203729A'
    - - :warning
      - 'Line 1269: Product not found, record ignored., BaseItemCode=203916A'
    - - :warning
      - 'Line 1270: Product not found, record ignored., BaseItemCode=203963A'
    - - :warning
      - 'Line 1272: Product not found, record ignored., BaseItemCode=204025A'
    - - :warning
      - 'Line 1273: Product not found, record ignored., BaseItemCode=204026A'
    - - :warning
      - 'Line 1274: Product not found, record ignored., BaseItemCode=204061A'
    - - :warning
      - 'Line 1275: Product not found, record ignored., BaseItemCode=204065'
    - - :warning
      - 'Line 1276: Product not found, record ignored., BaseItemCode=204069'
    - - :warning
      - 'Line 1277: Product not found, record ignored., BaseItemCode=204071'
    - - :warning
      - 'Line 1279: Product not found, record ignored., BaseItemCode=204102A'
    - - :warning
      - 'Line 1280: Product not found, record ignored., BaseItemCode=204105A'
    - - :warning
      - 'Line 1282: Product not found, record ignored., BaseItemCode=204213A'
    - - :warning
      - 'Line 1283: Product not found, record ignored., BaseItemCode=204214A'
    - - :warning
      - 'Line 1285: Product not found, record ignored., BaseItemCode=204472A'
    - - :warning
      - 'Line 1286: Product not found, record ignored., BaseItemCode=204554A'
    - - :warning
      - 'Line 1287: Product not found, record ignored., BaseItemCode=204569A'
    - - :warning
      - 'Line 1288: Product not found, record ignored., BaseItemCode=204586A'
    - - :warning
      - 'Line 1289: Product not found, record ignored., BaseItemCode=204595A'
    - - :warning
      - 'Line 1292: Product not found, record ignored., BaseItemCode=204701A'
    - - :warning
      - 'Line 1293: Product not found, record ignored., BaseItemCode=204702A'
    - - :warning
      - 'Line 1295: Product not found, record ignored., BaseItemCode=204923A'
    - - :warning
      - 'Line 1296: Product not found, record ignored., BaseItemCode=204924A'
    - - :warning
      - 'Line 1300: Product not found, record ignored., BaseItemCode=205588A'
    - - :warning
      - 'Line 1303: Product not found, record ignored., BaseItemCode=205841A'
    - - :warning
      - 'Line 1304: Product not found, record ignored., BaseItemCode=206089A'
    - - :warning
      - 'Line 1309: Product not found, record ignored., BaseItemCode=235003-4401A'
    - - :warning
      - 'Line 1310: Product not found, record ignored., BaseItemCode=235003-5201A'
    - - :warning
      - 'Line 1311: Product not found, record ignored., BaseItemCode=235003-5202A'
    - - :warning
      - 'Line 1312: Product not found, record ignored., BaseItemCode=235003-5218A'
    - - :warning
      - 'Line 1313: Product not found, record ignored., BaseItemCode=235100-5201A'
    - - :warning
      - 'Line 1314: Product not found, record ignored., BaseItemCode=235100-5202A'
    - - :warning
      - 'Line 1315: Product not found, record ignored., BaseItemCode=235112-5201A'
    - - :warning
      - 'Line 1316: Product not found, record ignored., BaseItemCode=235112-5216A'
    - - :warning
      - 'Line 1317: Product not found, record ignored., BaseItemCode=235112-5225A'
    - - :warning
      - 'Line 1318: Product not found, record ignored., BaseItemCode=235112-6025A'
    - - :warning
      - 'Line 1319: Product not found, record ignored., BaseItemCode=235997-1201A'
    - - :warning
      - 'Line 1320: Product not found, record ignored., BaseItemCode=235997-1202A'
    - - :warning
      - 'Line 1321: Product not found, record ignored., BaseItemCode=235997-2402A'
    - - :warning
      - 'Line 1322: Product not found, record ignored., BaseItemCode=235997-3602A'
    - - :warning
      - 'Line 1323: Product not found, record ignored., BaseItemCode=31372A'
    - - :warning
      - 'Line 1326: Product not found, record ignored., BaseItemCode=390024A'
    - - :warning
      - 'Line 1330: Product not found, record ignored., BaseItemCode=39249A'
    - - :warning
      - 'Line 1333: Product not found, record ignored., BaseItemCode=43197A'
    - - :warning
      - 'Line 1334: Product not found, record ignored., BaseItemCode=43311A'
    - - :warning
      - 'Line 1335: Product not found, record ignored., BaseItemCode=43617A'
    - - :warning
      - 'Line 1337: Product not found, record ignored., BaseItemCode=83241A'
    - - :warning
      - 'Line 1338: Product not found, record ignored., BaseItemCode=83733A'
    - - :warning
      - 'Line 1340: Product not found, record ignored., BaseItemCode=91046A'
    - - :warning
      - 'Line 1343: Product not found, record ignored., BaseItemCode=93374A'
    - - :warning
      - 'Line 1344: Product not found, record ignored., BaseItemCode=94304A'
    - - :warning
      - 'Line 1347: Product not found, record ignored., BaseItemCode=95143A'
    - - :warning
      - 'Line 1348: Product not found, record ignored., BaseItemCode=95996A'
    - - :warning
      - 'Line 1350: Product not found, record ignored., BaseItemCode=96801A'
    - - :warning
      - 'Line 1351: Product not found, record ignored., BaseItemCode=96932A'
    - - :warning
      - 'Line 1355: Product not found, record ignored., BaseItemCode=98735A'
    - - :warning
      - 'Line 1357: Product not found, record ignored., BaseItemCode=99364A'
    - - :warning
      - 'Line 1361: Product not found, record ignored., BaseItemCode=205842A'
    - - :warning
      - 'Line 1635: Product not found, record ignored., BaseItemCode=235848-6602A'
    - - :warning
      - 'Line 1636: Product not found, record ignored., BaseItemCode=235848-8402A'
    - - :warning
      - 'Line 1672: Product not found, record ignored., BaseItemCode=91988A'
 |
| 2026-06-17T03:05:21.221064 | ---
- - Customers
  - []
- - Sales Data
  - - - :error
      - 'Line 20: Base item code GE00016201 does not match an active product'
    - - :error
      - 'Line 79: Base item code ET1611 does not match an active product'
    - - :error
      - 'Line 80: Base item code ET1612 does not match an active product'
    - - :error
      - 'Line 145: Base item code GA000049W4 does not match an active product'
    - - :error
      - 'Line 154: Base item code GA00024304 does not match an active product'
    - - :error
      - 'Line 186: Base item code 3TRANS does not match an active product'
    - - :error
      - 'Line 187: Base item code 3TRANS does not match an active product'
    - - :error
      - 'Line 222: Base item code GE00027401 does not match an active product'
    - - :error
      - 'Line 243: Base item code GB00038301 does not match an active product'
    - - :error
      - 'Line 290: Base item code GL2761 does not match an active product'
    - - :error
      - 'Line 309: Base item code 3DIV does not match an active product'
    - - :error
      - 'Line 311: Base item code GE000103W0 does not match an active product'
    - - :error
      - 'Line 356: Base item code GA000051W4 does not match an active product'
    - - :error
      - 'Line 357: Base item code GE000091W5-R does not match an active product'
    - - :error
      - 'Line 367: Base item code GE000091W5-R does not match an active product'
    - - :error
      - 'Line 418: Base item code EG02000101 does not match an active product'
    - - :error
      - 'Line 419: Base item code GE000103W0 does not match an active product'
    - - :error
      - 'Line 445: Base item code GA000050W4 does not match an active product'
    - - :error
      - 'Line 446: Base item code GA00060701 does not match an active product'
    - - :error
      - 'Line 482: Base item code GE00027401 does not match an active product'
    - - :error
      - 'Line 491: Base item code GE000091W5-R does not match an active product'
    - - :error
      - 'Line 507: Base item code GA000049W4 does not match an active product'
    - - :error
      - 'Line 542: Base item code GA00047901 does not match an active product'
    - - :error
      - 'Line 543: Base item code GC00002405 does not match an active product'
    - - :error
      - 'Line 558: Base item code GA000464W4 does not match an active product'
    - - :error
      - 'Line 573: Base item code GE000091W5-R does not match an active product'
    - - :error
      - 'Line 592: Base item code GA000049W4 does not match an active product'
    - - :error
      - 'Line 722: Base item code GE000091W5-R does not match an active product'
    - - :error
      - 'Line 726: Base item code GC00002405 does not match an active product'
    - - :error
      - 'Line 796: Base item code GA000343W0-R does not match an active product'
    - - :error
      - 'Line 870: Base item code GA00014008 does not match an active product'
    - - :error
      - 'Line 880: Base item code 205852A does not match an active product'
    - - :error
      - 'Line 900: Base item code 206626A does not match an active product'
    - - :error
      - 'Line 945: Base item code GA000343W0-R does not match an active product'
    - - :error
      - 'Line 957: Base item code 202032A does not match an active product'
    - - :error
      - 'Line 958: Base item code 202103A does not match an active product'
    - - :error
      - 'Line 978: Base item code GA00062401 does not match an active product'
    - - :error
      - 'Line 992: Base item code GB00038301 does not match an active product'
    - - :error
      - 'Line 1041: Base item code GF00010001 does not match an active product'
    - - :error
      - 'Line 1075: Base item code 206626A does not match an active product'
    - - :error
      - 'Line 1107: Base item code NT010487R1-73 does not match an active product'
    - - :error
      - 'Line 1125: Base item code KATLCASOL25 does not match an active product'
    - - :error
      - 'Line 1126: Base item code MG011676R1 does not match an active product'
    - - :error
      - 'Line 1148: Base item code 206626A does not match an active product'
    - - :error
      - 'Line 1230: Base item code GA00014008 does not match an active product'
    - - :error
      - 'Line 1300: Base item code GE000103W0 does not match an active product'
    - - :error
      - 'Line 1332: Base item code GE000091W5-R does not match an active product'
    - - :error
      - 'Line 1352: Base item code GA00014008 does not match an active product'
    - - :error
      - 'Line 1399: Base item code KATLCA54 does not match an active product'
    - - :error
      - 'Line 1400: Base item code KATLCASOL25 does not match an active product'
    - - :error
      - 'Line 1774: Either quantity invoiced or quantity on order is required'
    - - :error
      - 'Line 2070: Either quantity invoiced or quantity on order is required'
    - - :error
      - 'Line 2547: Either quantity invoiced or quantity on order is required'
    - - :warning
      - "-242 more rows with invalid products"
 |
| 2026-06-16T19:32:15.072313 | ---
- - Inventory
  - - - :warning
      - 'Line 289: Product not found, record ignored., BaseItemCode=900375A'
    - - :warning
      - 'Line 292: Product not found, record ignored., BaseItemCode=200895A'
    - - :warning
      - 'Line 293: Product not found, record ignored., BaseItemCode=200899A'
    - - :warning
      - 'Line 294: Product not found, record ignored., BaseItemCode=201383A'
    - - :warning
      - 'Line 298: Product not found, record ignored., BaseItemCode=201735A'
    - - :warning
      - 'Line 300: Product not found, record ignored., BaseItemCode=202081A'
    - - :warning
      - 'Line 302: Product not found, record ignored., BaseItemCode=202149A'
    - - :warning
      - 'Line 304: Product not found, record ignored., BaseItemCode=202275A'
    - - :warning
      - 'Line 305: Product not found, record ignored., BaseItemCode=202357A'
    - - :warning
      - 'Line 308: Product not found, record ignored., BaseItemCode=202839A'
    - - :warning
      - 'Line 309: Product not found, record ignored., BaseItemCode=202842A'
    - - :warning
      - 'Line 310: Product not found, record ignored., BaseItemCode=202851A'
    - - :warning
      - 'Line 311: Product not found, record ignored., BaseItemCode=202864A'
    - - :warning
      - 'Line 312: Product not found, record ignored., BaseItemCode=202898A'
    - - :warning
      - 'Line 313: Product not found, record ignored., BaseItemCode=203249A'
    - - :warning
      - 'Line 314: Product not found, record ignored., BaseItemCode=203446A'
    - - :warning
      - 'Line 315: Product not found, record ignored., BaseItemCode=203542A'
    - - :warning
      - 'Line 316: Product not found, record ignored., BaseItemCode=203646A'
    - - :warning
      - 'Line 317: Product not found, record ignored., BaseItemCode=203753A'
    - - :warning
      - 'Line 318: Product not found, record ignored., BaseItemCode=203945A'
    - - :warning
      - 'Line 319: Product not found, record ignored., BaseItemCode=203962A'
    - - :warning
      - 'Line 321: Product not found, record ignored., BaseItemCode=204049A'
    - - :warning
      - 'Line 322: Product not found, record ignored., BaseItemCode=204077A'
    - - :warning
      - 'Line 325: Product not found, record ignored., BaseItemCode=204109A'
    - - :warning
      - 'Line 326: Product not found, record ignored., BaseItemCode=204141A'
    - - :warning
      - 'Line 327: Product not found, record ignored., BaseItemCode=204147A'
    - - :warning
      - 'Line 328: Product not found, record ignored., BaseItemCode=204195A'
    - - :warning
      - 'Line 332: Product not found, record ignored., BaseItemCode=204361A'
    - - :warning
      - 'Line 333: Product not found, record ignored., BaseItemCode=204375A'
    - - :warning
      - 'Line 334: Product not found, record ignored., BaseItemCode=204446A'
    - - :warning
      - 'Line 335: Product not found, record ignored., BaseItemCode=204447A'
    - - :warning
      - 'Line 336: Product not found, record ignored., BaseItemCode=204464A'
    - - :warning
      - 'Line 337: Product not found, record ignored., BaseItemCode=204466A'
    - - :warning
      - 'Line 338: Product not found, record ignored., BaseItemCode=204467A'
    - - :warning
      - 'Line 339: Product not found, record ignored., BaseItemCode=204539A'
    - - :warning
      - 'Line 340: Product not found, record ignored., BaseItemCode=204543A'
    - - :warning
      - 'Line 341: Product not found, record ignored., BaseItemCode=204544A'
    - - :warning
      - 'Line 342: Product not found, record ignored., BaseItemCode=204555A'
    - - :warning
      - 'Line 343: Product not found, record ignored., BaseItemCode=204587A'
    - - :warning
      - 'Line 344: Product not found, record ignored., BaseItemCode=204589A'
    - - :warning
      - 'Line 349: Product not found, record ignored., BaseItemCode=204708A'
    - - :warning
      - 'Line 352: Product not found, record ignored., BaseItemCode=205072A'
    - - :warning
      - 'Line 355: Product not found, record ignored., BaseItemCode=205327A'
    - - :warning
      - 'Line 356: Product not found, record ignored., BaseItemCode=205331A'
    - - :warning
      - 'Line 358: Product not found, record ignored., BaseItemCode=205621A'
    - - :warning
      - 'Line 359: Product not found, record ignored., BaseItemCode=205655A'
    - - :warning
      - 'Line 361: Product not found, record ignored., BaseItemCode=205843A'
    - - :warning
      - 'Line 362: Product not found, record ignored., BaseItemCode=205844A'
    - - :warning
      - 'Line 363: Product not found, record ignored., BaseItemCode=235003-5223A'
    - - :warning
      - 'Line 364: Product not found, record ignored., BaseItemCode=235112-5202A'
    - - :warning
      - 'Line 365: Product not found, record ignored., BaseItemCode=235112-6001A'
    - - :warning
      - 'Line 366: Product not found, record ignored., BaseItemCode=235112-6002A'
    - - :warning
      - 'Line 367: Product not found, record ignored., BaseItemCode=235112-6016A'
    - - :warning
      - 'Line 368: Product not found, record ignored., BaseItemCode=235997-2401A'
    - - :warning
      - 'Line 369: Product not found, record ignored., BaseItemCode=235997-3601A'
    - - :warning
      - 'Line 377: Product not found, record ignored., BaseItemCode=390249A'
    - - :warning
      - 'Line 379: Product not found, record ignored., BaseItemCode=39591A'
    - - :warning
      - 'Line 380: Product not found, record ignored., BaseItemCode=39615A'
    - - :warning
      - 'Line 381: Product not found, record ignored., BaseItemCode=39628A'
    - - :warning
      - 'Line 384: Product not found, record ignored., BaseItemCode=43256A'
    - - :warning
      - 'Line 387: Product not found, record ignored., BaseItemCode=43645A'
    - - :warning
      - 'Line 390: Product not found, record ignored., BaseItemCode=43682A'
    - - :warning
      - 'Line 391: Product not found, record ignored., BaseItemCode=43873A'
    - - :warning
      - 'Line 393: Product not found, record ignored., BaseItemCode=49619A'
    - - :warning
      - 'Line 398: Product not found, record ignored., BaseItemCode=86391A'
    - - :warning
      - 'Line 402: Product not found, record ignored., BaseItemCode=88968A'
    - - :warning
      - 'Line 404: Product not found, record ignored., BaseItemCode=91416A'
    - - :warning
      - 'Line 407: Product not found, record ignored., BaseItemCode=94465A'
    - - :warning
      - 'Line 410: Product not found, record ignored., BaseItemCode=97441A'
    - - :warning
      - 'Line 411: Product not found, record ignored., BaseItemCode=97442A'
    - - :warning
      - 'Line 412: Product not found, record ignored., BaseItemCode=97949A'
    - - :warning
      - 'Line 416: Product not found, record ignored., BaseItemCode=98441A'
    - - :warning
      - 'Line 419: Product not found, record ignored., BaseItemCode=99561A'
    - - :warning
      - 'Line 420: Product not found, record ignored., BaseItemCode=99562A'
    - - :warning
      - 'Line 427: Product not found, record ignored., BaseItemCode=200268A'
    - - :warning
      - 'Line 455: Product not found, record ignored., BaseItemCode=202274A'
    - - :warning
      - 'Line 460: Product not found, record ignored., BaseItemCode=202299A'
    - - :warning
      - 'Line 473: Product not found, record ignored., BaseItemCode=202633A'
    - - :warning
      - 'Line 474: Product not found, record ignored., BaseItemCode=202836A'
    - - :warning
      - 'Line 487: Product not found, record ignored., BaseItemCode=203187A'
    - - :warning
      - 'Line 488: Product not found, record ignored., BaseItemCode=203188A'
    - - :warning
      - 'Line 490: Product not found, record ignored., BaseItemCode=203221A'
    - - :warning
      - 'Line 491: Product not found, record ignored., BaseItemCode=203222A'
    - - :warning
      - 'Line 492: Product not found, record ignored., BaseItemCode=203246A'
    - - :warning
      - 'Line 493: Product not found, record ignored., BaseItemCode=203247A'
    - - :warning
      - 'Line 540: Product not found, record ignored., BaseItemCode=203998A'
    - - :warning
      - 'Line 542: Product not found, record ignored., BaseItemCode=204027A'
    - - :warning
      - 'Line 594: Product not found, record ignored., BaseItemCode=204362A'
    - - :warning
      - 'Line 605: Product not found, record ignored., BaseItemCode=204642A'
    - - :warning
      - 'Line 618: Product not found, record ignored., BaseItemCode=204895A'
    - - :warning
      - 'Line 639: Product not found, record ignored., BaseItemCode=205351A'
    - - :warning
      - 'Line 640: Product not found, record ignored., BaseItemCode=205363A'
    - - :warning
      - 'Line 645: Product not found, record ignored., BaseItemCode=205618A'
    - - :warning
      - 'Line 649: Product not found, record ignored., BaseItemCode=205643A'
    - - :warning
      - 'Line 660: Product not found, record ignored., BaseItemCode=205755A'
    - - :warning
      - 'Line 666: Product not found, record ignored., BaseItemCode=205766A'
    - - :warning
      - 'Line 698: Product not found, record ignored., BaseItemCode=206032A'
    - - :warning
      - 'Line 927: Product not found, record ignored., BaseItemCode=39499A'
    - - :warning
      - 'Line 931: Product not found, record ignored., BaseItemCode=39614A'
    - - :warning
      - 'Line 1093: Product not found, record ignored., BaseItemCode=91732A'
    - - :warning
      - 'Line 1094: Product not found, record ignored., BaseItemCode=91733A'
    - - :warning
      - 'Line 1114: Product not found, record ignored., BaseItemCode=94353A'
    - - :warning
      - 'Line 1123: Product not found, record ignored., BaseItemCode=95122A'
    - - :warning
      - 'Line 1134: Product not found, record ignored., BaseItemCode=96605A'
    - - :warning
      - 'Line 1135: Product not found, record ignored., BaseItemCode=96606A'
    - - :warning
      - 'Line 1136: Product not found, record ignored., BaseItemCode=96607A'
    - - :warning
      - 'Line 1137: Product not found, record ignored., BaseItemCode=96608A'
    - - :warning
      - 'Line 1139: Product not found, record ignored., BaseItemCode=96726A'
    - - :warning
      - 'Line 1146: Product not found, record ignored., BaseItemCode=97374A'
    - - :warning
      - 'Line 1148: Product not found, record ignored., BaseItemCode=97395A'
    - - :warning
      - 'Line 1149: Product not found, record ignored., BaseItemCode=97396A'
    - - :warning
      - 'Line 1150: Product not found, record ignored., BaseItemCode=97397A'
    - - :warning
      - 'Line 1162: Product not found, record ignored., BaseItemCode=97914A'
    - - :warning
      - 'Line 1230: Product not found, record ignored., BaseItemCode=200323A'
    - - :warning
      - 'Line 1232: Product not found, record ignored., BaseItemCode=200367A'
    - - :warning
      - 'Line 1233: Product not found, record ignored., BaseItemCode=200369A'
    - - :warning
      - 'Line 1234: Product not found, record ignored., BaseItemCode=200373A'
    - - :warning
      - 'Line 1235: Product not found, record ignored., BaseItemCode=200374A'
    - - :warning
      - 'Line 1236: Product not found, record ignored., BaseItemCode=200397A'
    - - :warning
      - 'Line 1237: Product not found, record ignored., BaseItemCode=200402A'
    - - :warning
      - 'Line 1238: Product not found, record ignored., BaseItemCode=200775A'
    - - :warning
      - 'Line 1239: Product not found, record ignored., BaseItemCode=200944A'
    - - :warning
      - 'Line 1240: Product not found, record ignored., BaseItemCode=201252A'
    - - :warning
      - 'Line 1241: Product not found, record ignored., BaseItemCode=201271A'
    - - :warning
      - 'Line 1242: Product not found, record ignored., BaseItemCode=201296A'
    - - :warning
      - 'Line 1243: Product not found, record ignored., BaseItemCode=201297A'
    - - :warning
      - 'Line 1247: Product not found, record ignored., BaseItemCode=201466A'
    - - :warning
      - 'Line 1248: Product not found, record ignored., BaseItemCode=201712A'
    - - :warning
      - 'Line 1250: Product not found, record ignored., BaseItemCode=201734A'
    - - :warning
      - 'Line 1251: Product not found, record ignored., BaseItemCode=201736A'
    - - :warning
      - 'Line 1252: Product not found, record ignored., BaseItemCode=201737A'
    - - :warning
      - 'Line 1254: Product not found, record ignored., BaseItemCode=202156A'
    - - :warning
      - 'Line 1255: Product not found, record ignored., BaseItemCode=202164A'
    - - :warning
      - 'Line 1256: Product not found, record ignored., BaseItemCode=202176A'
    - - :warning
      - 'Line 1258: Product not found, record ignored., BaseItemCode=202634A'
    - - :warning
      - 'Line 1259: Product not found, record ignored., BaseItemCode=202635A'
    - - :warning
      - 'Line 1260: Product not found, record ignored., BaseItemCode=202844A'
    - - :warning
      - 'Line 1261: Product not found, record ignored., BaseItemCode=202953A'
    - - :warning
      - 'Line 1262: Product not found, record ignored., BaseItemCode=203108A'
    - - :warning
      - 'Line 1263: Product not found, record ignored., BaseItemCode=203185A'
    - - :warning
      - 'Line 1265: Product not found, record ignored., BaseItemCode=203475A'
    - - :warning
      - 'Line 1267: Product not found, record ignored., BaseItemCode=203666A'
    - - :warning
      - 'Line 1268: Product not found, record ignored., BaseItemCode=203729A'
    - - :warning
      - 'Line 1269: Product not found, record ignored., BaseItemCode=203916A'
    - - :warning
      - 'Line 1270: Product not found, record ignored., BaseItemCode=203963A'
    - - :warning
      - 'Line 1272: Product not found, record ignored., BaseItemCode=204025A'
    - - :warning
      - 'Line 1273: Product not found, record ignored., BaseItemCode=204026A'
    - - :warning
      - 'Line 1274: Product not found, record ignored., BaseItemCode=204061A'
    - - :warning
      - 'Line 1275: Product not found, record ignored., BaseItemCode=204065'
    - - :warning
      - 'Line 1276: Product not found, record ignored., BaseItemCode=204069'
    - - :warning
      - 'Line 1277: Product not found, record ignored., BaseItemCode=204071'
    - - :warning
      - 'Line 1279: Product not found, record ignored., BaseItemCode=204102A'
    - - :warning
      - 'Line 1280: Product not found, record ignored., BaseItemCode=204105A'
    - - :warning
      - 'Line 1282: Product not found, record ignored., BaseItemCode=204213A'
    - - :warning
      - 'Line 1283: Product not found, record ignored., BaseItemCode=204214A'
    - - :warning
      - 'Line 1285: Product not found, record ignored., BaseItemCode=204472A'
    - - :warning
      - 'Line 1286: Product not found, record ignored., BaseItemCode=204554A'
    - - :warning
      - 'Line 1287: Product not found, record ignored., BaseItemCode=204569A'
    - - :warning
      - 'Line 1288: Product not found, record ignored., BaseItemCode=204586A'
    - - :warning
      - 'Line 1289: Product not found, record ignored., BaseItemCode=204595A'
    - - :warning
      - 'Line 1292: Product not found, record ignored., BaseItemCode=204701A'
    - - :warning
      - 'Line 1293: Product not found, record ignored., BaseItemCode=204702A'
    - - :warning
      - 'Line 1295: Product not found, record ignored., BaseItemCode=204923A'
    - - :warning
      - 'Line 1296: Product not found, record ignored., BaseItemCode=204924A'
    - - :warning
      - 'Line 1300: Product not found, record ignored., BaseItemCode=205588A'
    - - :warning
      - 'Line 1303: Product not found, record ignored., BaseItemCode=205841A'
    - - :warning
      - 'Line 1304: Product not found, record ignored., BaseItemCode=206089A'
    - - :warning
      - 'Line 1309: Product not found, record ignored., BaseItemCode=235003-4401A'
    - - :warning
      - 'Line 1310: Product not found, record ignored., BaseItemCode=235003-5201A'
    - - :warning
      - 'Line 1311: Product not found, record ignored., BaseItemCode=235003-5202A'
    - - :warning
      - 'Line 1312: Product not found, record ignored., BaseItemCode=235003-5218A'
    - - :warning
      - 'Line 1313: Product not found, record ignored., BaseItemCode=235100-5201A'
    - - :warning
      - 'Line 1314: Product not found, record ignored., BaseItemCode=235100-5202A'
    - - :warning
      - 'Line 1315: Product not found, record ignored., BaseItemCode=235112-5201A'
    - - :warning
      - 'Line 1316: Product not found, record ignored., BaseItemCode=235112-5216A'
    - - :warning
      - 'Line 1317: Product not found, record ignored., BaseItemCode=235112-5225A'
    - - :warning
      - 'Line 1318: Product not found, record ignored., BaseItemCode=235112-6025A'
    - - :warning
      - 'Line 1319: Product not found, record ignored., BaseItemCode=235997-1201A'
    - - :warning
      - 'Line 1320: Product not found, record ignored., BaseItemCode=235997-1202A'
    - - :warning
      - 'Line 1321: Product not found, record ignored., BaseItemCode=235997-2402A'
    - - :warning
      - 'Line 1322: Product not found, record ignored., BaseItemCode=235997-3602A'
    - - :warning
      - 'Line 1323: Product not found, record ignored., BaseItemCode=31372A'
    - - :warning
      - 'Line 1326: Product not found, record ignored., BaseItemCode=390024A'
    - - :warning
      - 'Line 1330: Product not found, record ignored., BaseItemCode=39249A'
    - - :warning
      - 'Line 1333: Product not found, record ignored., BaseItemCode=43197A'
    - - :warning
      - 'Line 1334: Product not found, record ignored., BaseItemCode=43311A'
    - - :warning
      - 'Line 1335: Product not found, record ignored., BaseItemCode=43617A'
    - - :warning
      - 'Line 1337: Product not found, record ignored., BaseItemCode=83241A'
    - - :warning
      - 'Line 1338: Product not found, record ignored., BaseItemCode=83733A'
    - - :warning
      - 'Line 1340: Product not found, record ignored., BaseItemCode=91046A'
    - - :warning
      - 'Line 1343: Product not found, record ignored., BaseItemCode=93374A'
    - - :warning
      - 'Line 1344: Product not found, record ignored., BaseItemCode=94304A'
    - - :warning
      - 'Line 1347: Product not found, record ignored., BaseItemCode=95143A'
    - - :warning
      - 'Line 1348: Product not found, record ignored., BaseItemCode=95996A'
    - - :warning
      - 'Line 1350: Product not found, record ignored., BaseItemCode=96801A'
    - - :warning
      - 'Line 1351: Product not found, record ignored., BaseItemCode=96932A'
    - - :warning
      - 'Line 1355: Product not found, record ignored., BaseItemCode=98735A'
    - - :warning
      - 'Line 1357: Product not found, record ignored., BaseItemCode=99364A'
    - - :warning
      - 'Line 1361: Product not found, record ignored., BaseItemCode=205842A'
    - - :warning
      - 'Line 1635: Product not found, record ignored., BaseItemCode=235848-6602A'
    - - :warning
      - 'Line 1636: Product not found, record ignored., BaseItemCode=235848-8402A'
    - - :warning
      - 'Line 1672: Product not found, record ignored., BaseItemCode=91988A'
 |
| 2026-06-16T15:07:36.686940 | ---
- - Inventory
  - - - :warning
      - 'Line 246: Product not found, record ignored., BaseItemCode=900375A'
    - - :warning
      - 'Line 249: Product not found, record ignored., BaseItemCode=200895A'
    - - :warning
      - 'Line 250: Product not found, record ignored., BaseItemCode=200899A'
    - - :warning
      - 'Line 251: Product not found, record ignored., BaseItemCode=201383A'
    - - :warning
      - 'Line 255: Product not found, record ignored., BaseItemCode=201735A'
    - - :warning
      - 'Line 257: Product not found, record ignored., BaseItemCode=202081A'
    - - :warning
      - 'Line 259: Product not found, record ignored., BaseItemCode=202149A'
    - - :warning
      - 'Line 261: Product not found, record ignored., BaseItemCode=202275A'
    - - :warning
      - 'Line 262: Product not found, record ignored., BaseItemCode=202357A'
    - - :warning
      - 'Line 265: Product not found, record ignored., BaseItemCode=202839A'
    - - :warning
      - 'Line 266: Product not found, record ignored., BaseItemCode=202842A'
    - - :warning
      - 'Line 267: Product not found, record ignored., BaseItemCode=202851A'
    - - :warning
      - 'Line 268: Product not found, record ignored., BaseItemCode=202864A'
    - - :warning
      - 'Line 269: Product not found, record ignored., BaseItemCode=202898A'
    - - :warning
      - 'Line 270: Product not found, record ignored., BaseItemCode=203249A'
    - - :warning
      - 'Line 271: Product not found, record ignored., BaseItemCode=203446A'
    - - :warning
      - 'Line 272: Product not found, record ignored., BaseItemCode=203542A'
    - - :warning
      - 'Line 273: Product not found, record ignored., BaseItemCode=203646A'
    - - :warning
      - 'Line 274: Product not found, record ignored., BaseItemCode=203753A'
    - - :warning
      - 'Line 275: Product not found, record ignored., BaseItemCode=203945A'
    - - :warning
      - 'Line 276: Product not found, record ignored., BaseItemCode=203962A'
    - - :warning
      - 'Line 278: Product not found, record ignored., BaseItemCode=204049A'
    - - :warning
      - 'Line 279: Product not found, record ignored., BaseItemCode=204077A'
    - - :warning
      - 'Line 282: Product not found, record ignored., BaseItemCode=204109A'
    - - :warning
      - 'Line 283: Product not found, record ignored., BaseItemCode=204141A'
    - - :warning
      - 'Line 284: Product not found, record ignored., BaseItemCode=204147A'
    - - :warning
      - 'Line 285: Product not found, record ignored., BaseItemCode=204195A'
    - - :warning
      - 'Line 289: Product not found, record ignored., BaseItemCode=204361A'
    - - :warning
      - 'Line 290: Product not found, record ignored., BaseItemCode=204375A'
    - - :warning
      - 'Line 291: Product not found, record ignored., BaseItemCode=204446A'
    - - :warning
      - 'Line 292: Product not found, record ignored., BaseItemCode=204447A'
    - - :warning
      - 'Line 293: Product not found, record ignored., BaseItemCode=204464A'
    - - :warning
      - 'Line 294: Product not found, record ignored., BaseItemCode=204466A'
    - - :warning
      - 'Line 295: Product not found, record ignored., BaseItemCode=204467A'
    - - :warning
      - 'Line 296: Product not found, record ignored., BaseItemCode=204539A'
    - - :warning
      - 'Line 297: Product not found, record ignored., BaseItemCode=204543A'
    - - :warning
      - 'Line 298: Product not found, record ignored., BaseItemCode=204544A'
    - - :warning
      - 'Line 299: Product not found, record ignored., BaseItemCode=204555A'
    - - :warning
      - 'Line 300: Product not found, record ignored., BaseItemCode=204587A'
    - - :warning
      - 'Line 301: Product not found, record ignored., BaseItemCode=204589A'
    - - :warning
      - 'Line 306: Product not found, record ignored., BaseItemCode=204708A'
    - - :warning
      - 'Line 309: Product not found, record ignored., BaseItemCode=205072A'
    - - :warning
      - 'Line 312: Product not found, record ignored., BaseItemCode=205327A'
    - - :warning
      - 'Line 313: Product not found, record ignored., BaseItemCode=205331A'
    - - :warning
      - 'Line 315: Product not found, record ignored., BaseItemCode=205621A'
    - - :warning
      - 'Line 316: Product not found, record ignored., BaseItemCode=205655A'
    - - :warning
      - 'Line 318: Product not found, record ignored., BaseItemCode=205843A'
    - - :warning
      - 'Line 319: Product not found, record ignored., BaseItemCode=205844A'
    - - :warning
      - 'Line 320: Product not found, record ignored., BaseItemCode=235003-5223A'
    - - :warning
      - 'Line 321: Product not found, record ignored., BaseItemCode=235112-5202A'
    - - :warning
      - 'Line 322: Product not found, record ignored., BaseItemCode=235112-6001A'
    - - :warning
      - 'Line 323: Product not found, record ignored., BaseItemCode=235112-6002A'
    - - :warning
      - 'Line 324: Product not found, record ignored., BaseItemCode=235112-6016A'
    - - :warning
      - 'Line 325: Product not found, record ignored., BaseItemCode=235997-2401A'
    - - :warning
      - 'Line 326: Product not found, record ignored., BaseItemCode=235997-3601A'
    - - :warning
      - 'Line 334: Product not found, record ignored., BaseItemCode=390249A'
    - - :warning
      - 'Line 336: Product not found, record ignored., BaseItemCode=39591A'
    - - :warning
      - 'Line 337: Product not found, record ignored., BaseItemCode=39615A'
    - - :warning
      - 'Line 338: Product not found, record ignored., BaseItemCode=39628A'
    - - :warning
      - 'Line 341: Product not found, record ignored., BaseItemCode=43256A'
    - - :warning
      - 'Line 344: Product not found, record ignored., BaseItemCode=43645A'
    - - :warning
      - 'Line 347: Product not found, record ignored., BaseItemCode=43682A'
    - - :warning
      - 'Line 348: Product not found, record ignored., BaseItemCode=43873A'
    - - :warning
      - 'Line 350: Product not found, record ignored., BaseItemCode=49619A'
    - - :warning
      - 'Line 355: Product not found, record ignored., BaseItemCode=86391A'
    - - :warning
      - 'Line 359: Product not found, record ignored., BaseItemCode=88968A'
    - - :warning
      - 'Line 361: Product not found, record ignored., BaseItemCode=91416A'
    - - :warning
      - 'Line 364: Product not found, record ignored., BaseItemCode=94465A'
    - - :warning
      - 'Line 367: Product not found, record ignored., BaseItemCode=97441A'
    - - :warning
      - 'Line 368: Product not found, record ignored., BaseItemCode=97442A'
    - - :warning
      - 'Line 369: Product not found, record ignored., BaseItemCode=97949A'
    - - :warning
      - 'Line 373: Product not found, record ignored., BaseItemCode=98441A'
    - - :warning
      - 'Line 376: Product not found, record ignored., BaseItemCode=99561A'
    - - :warning
      - 'Line 377: Product not found, record ignored., BaseItemCode=99562A'
    - - :warning
      - 'Line 387: Product not found, record ignored., BaseItemCode=200268A'
    - - :warning
      - 'Line 416: Product not found, record ignored., BaseItemCode=202274A'
    - - :warning
      - 'Line 421: Product not found, record ignored., BaseItemCode=202299A'
    - - :warning
      - 'Line 435: Product not found, record ignored., BaseItemCode=202633A'
    - - :warning
      - 'Line 436: Product not found, record ignored., BaseItemCode=202836A'
    - - :warning
      - 'Line 450: Product not found, record ignored., BaseItemCode=203187A'
    - - :warning
      - 'Line 451: Product not found, record ignored., BaseItemCode=203188A'
    - - :warning
      - 'Line 453: Product not found, record ignored., BaseItemCode=203221A'
    - - :warning
      - 'Line 454: Product not found, record ignored., BaseItemCode=203222A'
    - - :warning
      - 'Line 455: Product not found, record ignored., BaseItemCode=203246A'
    - - :warning
      - 'Line 456: Product not found, record ignored., BaseItemCode=203247A'
    - - :warning
      - 'Line 504: Product not found, record ignored., BaseItemCode=203998A'
    - - :warning
      - 'Line 506: Product not found, record ignored., BaseItemCode=204027A'
    - - :warning
      - 'Line 560: Product not found, record ignored., BaseItemCode=204362A'
    - - :warning
      - 'Line 573: Product not found, record ignored., BaseItemCode=204642A'
    - - :warning
      - 'Line 586: Product not found, record ignored., BaseItemCode=204895A'
    - - :warning
      - 'Line 608: Product not found, record ignored., BaseItemCode=205351A'
    - - :warning
      - 'Line 609: Product not found, record ignored., BaseItemCode=205363A'
    - - :warning
      - 'Line 616: Product not found, record ignored., BaseItemCode=205618A'
    - - :warning
      - 'Line 620: Product not found, record ignored., BaseItemCode=205643A'
    - - :warning
      - 'Line 632: Product not found, record ignored., BaseItemCode=205755A'
    - - :warning
      - 'Line 638: Product not found, record ignored., BaseItemCode=205766A'
    - - :warning
      - 'Line 674: Product not found, record ignored., BaseItemCode=206032A'
    - - :warning
      - 'Line 906: Product not found, record ignored., BaseItemCode=39499A'
    - - :warning
      - 'Line 910: Product not found, record ignored., BaseItemCode=39614A'
    - - :warning
      - 'Line 1083: Product not found, record ignored., BaseItemCode=91732A'
    - - :warning
      - 'Line 1084: Product not found, record ignored., BaseItemCode=91733A'
    - - :warning
      - 'Line 1104: Product not found, record ignored., BaseItemCode=94353A'
    - - :warning
      - 'Line 1113: Product not found, record ignored., BaseItemCode=95122A'
    - - :warning
      - 'Line 1126: Product not found, record ignored., BaseItemCode=96605A'
    - - :warning
      - 'Line 1127: Product not found, record ignored., BaseItemCode=96606A'
    - - :warning
      - 'Line 1128: Product not found, record ignored., BaseItemCode=96607A'
    - - :warning
      - 'Line 1129: Product not found, record ignored., BaseItemCode=96608A'
    - - :warning
      - 'Line 1131: Product not found, record ignored., BaseItemCode=96726A'
    - - :warning
      - 'Line 1138: Product not found, record ignored., BaseItemCode=97374A'
    - - :warning
      - 'Line 1140: Product not found, record ignored., BaseItemCode=97395A'
    - - :warning
      - 'Line 1141: Product not found, record ignored., BaseItemCode=97396A'
    - - :warning
      - 'Line 1142: Product not found, record ignored., BaseItemCode=97397A'
    - - :warning
      - 'Line 1154: Product not found, record ignored., BaseItemCode=97914A'
    - - :warning
      - 'Line 1226: Product not found, record ignored., BaseItemCode=200323A'
    - - :warning
      - 'Line 1228: Product not found, record ignored., BaseItemCode=200367A'
    - - :warning
      - 'Line 1229: Product not found, record ignored., BaseItemCode=200369A'
    - - :warning
      - 'Line 1230: Product not found, record ignored., BaseItemCode=200373A'
    - - :warning
      - 'Line 1231: Product not found, record ignored., BaseItemCode=200374A'
    - - :warning
      - 'Line 1232: Product not found, record ignored., BaseItemCode=200397A'
    - - :warning
      - 'Line 1233: Product not found, record ignored., BaseItemCode=200402A'
    - - :warning
      - 'Line 1234: Product not found, record ignored., BaseItemCode=200775A'
    - - :warning
      - 'Line 1235: Product not found, record ignored., BaseItemCode=200944A'
    - - :warning
      - 'Line 1236: Product not found, record ignored., BaseItemCode=201252A'
    - - :warning
      - 'Line 1237: Product not found, record ignored., BaseItemCode=201271A'
    - - :warning
      - 'Line 1238: Product not found, record ignored., BaseItemCode=201296A'
    - - :warning
      - 'Line 1239: Product not found, record ignored., BaseItemCode=201297A'
    - - :warning
      - 'Line 1243: Product not found, record ignored., BaseItemCode=201466A'
    - - :warning
      - 'Line 1244: Product not found, record ignored., BaseItemCode=201712A'
    - - :warning
      - 'Line 1246: Product not found, record ignored., BaseItemCode=201734A'
    - - :warning
      - 'Line 1247: Product not found, record ignored., BaseItemCode=201736A'
    - - :warning
      - 'Line 1248: Product not found, record ignored., BaseItemCode=201737A'
    - - :warning
      - 'Line 1250: Product not found, record ignored., BaseItemCode=202156A'
    - - :warning
      - 'Line 1251: Product not found, record ignored., BaseItemCode=202164A'
    - - :warning
      - 'Line 1252: Product not found, record ignored., BaseItemCode=202176A'
    - - :warning
      - 'Line 1254: Product not found, record ignored., BaseItemCode=202634A'
    - - :warning
      - 'Line 1255: Product not found, record ignored., BaseItemCode=202635A'
    - - :warning
      - 'Line 1256: Product not found, record ignored., BaseItemCode=202844A'
    - - :warning
      - 'Line 1257: Product not found, record ignored., BaseItemCode=202953A'
    - - :warning
      - 'Line 1258: Product not found, record ignored., BaseItemCode=203108A'
    - - :warning
      - 'Line 1259: Product not found, record ignored., BaseItemCode=203185A'
    - - :warning
      - 'Line 1261: Product not found, record ignored., BaseItemCode=203475A'
    - - :warning
      - 'Line 1263: Product not found, record ignored., BaseItemCode=203666A'
    - - :warning
      - 'Line 1264: Product not found, record ignored., BaseItemCode=203729A'
    - - :warning
      - 'Line 1265: Product not found, record ignored., BaseItemCode=203916A'
    - - :warning
      - 'Line 1266: Product not found, record ignored., BaseItemCode=203963A'
    - - :warning
      - 'Line 1268: Product not found, record ignored., BaseItemCode=204025A'
    - - :warning
      - 'Line 1269: Product not found, record ignored., BaseItemCode=204026A'
    - - :warning
      - 'Line 1270: Product not found, record ignored., BaseItemCode=204061A'
    - - :warning
      - 'Line 1271: Product not found, record ignored., BaseItemCode=204065'
    - - :warning
      - 'Line 1272: Product not found, record ignored., BaseItemCode=204069'
    - - :warning
      - 'Line 1273: Product not found, record ignored., BaseItemCode=204071'
    - - :warning
      - 'Line 1275: Product not found, record ignored., BaseItemCode=204102A'
    - - :warning
      - 'Line 1276: Product not found, record ignored., BaseItemCode=204105A'
    - - :warning
      - 'Line 1278: Product not found, record ignored., BaseItemCode=204213A'
    - - :warning
      - 'Line 1279: Product not found, record ignored., BaseItemCode=204214A'
    - - :warning
      - 'Line 1281: Product not found, record ignored., BaseItemCode=204472A'
    - - :warning
      - 'Line 1282: Product not found, record ignored., BaseItemCode=204554A'
    - - :warning
      - 'Line 1283: Product not found, record ignored., BaseItemCode=204569A'
    - - :warning
      - 'Line 1284: Product not found, record ignored., BaseItemCode=204586A'
    - - :warning
      - 'Line 1285: Product not found, record ignored., BaseItemCode=204595A'
    - - :warning
      - 'Line 1288: Product not found, record ignored., BaseItemCode=204701A'
    - - :warning
      - 'Line 1289: Product not found, record ignored., BaseItemCode=204702A'
    - - :warning
      - 'Line 1291: Product not found, record ignored., BaseItemCode=204923A'
    - - :warning
      - 'Line 1292: Product not found, record ignored., BaseItemCode=204924A'
    - - :warning
      - 'Line 1296: Product not found, record ignored., BaseItemCode=205588A'
    - - :warning
      - 'Line 1299: Product not found, record ignored., BaseItemCode=205841A'
    - - :warning
      - 'Line 1300: Product not found, record ignored., BaseItemCode=206089A'
    - - :warning
      - 'Line 1305: Product not found, record ignored., BaseItemCode=235003-4401A'
    - - :warning
      - 'Line 1306: Product not found, record ignored., BaseItemCode=235003-5201A'
    - - :warning
      - 'Line 1307: Product not found, record ignored., BaseItemCode=235003-5202A'
    - - :warning
      - 'Line 1308: Product not found, record ignored., BaseItemCode=235003-5218A'
    - - :warning
      - 'Line 1309: Product not found, record ignored., BaseItemCode=235100-5201A'
    - - :warning
      - 'Line 1310: Product not found, record ignored., BaseItemCode=235100-5202A'
    - - :warning
      - 'Line 1311: Product not found, record ignored., BaseItemCode=235112-5201A'
    - - :warning
      - 'Line 1312: Product not found, record ignored., BaseItemCode=235112-5216A'
    - - :warning
      - 'Line 1313: Product not found, record ignored., BaseItemCode=235112-5225A'
    - - :warning
      - 'Line 1314: Product not found, record ignored., BaseItemCode=235112-6025A'
    - - :warning
      - 'Line 1315: Product not found, record ignored., BaseItemCode=235997-1201A'
    - - :warning
      - 'Line 1316: Product not found, record ignored., BaseItemCode=235997-1202A'
    - - :warning
      - 'Line 1317: Product not found, record ignored., BaseItemCode=235997-2402A'
    - - :warning
      - 'Line 1318: Product not found, record ignored., BaseItemCode=235997-3602A'
    - - :warning
      - 'Line 1319: Product not found, record ignored., BaseItemCode=31372A'
    - - :warning
      - 'Line 1322: Product not found, record ignored., BaseItemCode=390024A'
    - - :warning
      - 'Line 1326: Product not found, record ignored., BaseItemCode=39249A'
    - - :warning
      - 'Line 1329: Product not found, record ignored., BaseItemCode=43197A'
    - - :warning
      - 'Line 1330: Product not found, record ignored., BaseItemCode=43311A'
    - - :warning
      - 'Line 1331: Product not found, record ignored., BaseItemCode=43617A'
    - - :warning
      - 'Line 1333: Product not found, record ignored., BaseItemCode=83241A'
    - - :warning
      - 'Line 1334: Product not found, record ignored., BaseItemCode=83733A'
    - - :warning
      - 'Line 1336: Product not found, record ignored., BaseItemCode=91046A'
    - - :warning
      - 'Line 1339: Product not found, record ignored., BaseItemCode=93374A'
    - - :warning
      - 'Line 1340: Product not found, record ignored., BaseItemCode=94304A'
    - - :warning
      - 'Line 1343: Product not found, record ignored., BaseItemCode=95143A'
    - - :warning
      - 'Line 1344: Product not found, record ignored., BaseItemCode=95996A'
    - - :warning
      - 'Line 1346: Product not found, record ignored., BaseItemCode=96801A'
    - - :warning
      - 'Line 1347: Product not found, record ignored., BaseItemCode=96932A'
    - - :warning
      - 'Line 1351: Product not found, record ignored., BaseItemCode=98735A'
    - - :warning
      - 'Line 1353: Product not found, record ignored., BaseItemCode=99364A'
    - - :warning
      - 'Line 1357: Product not found, record ignored., BaseItemCode=205842A'
    - - :warning
      - 'Line 1635: Product not found, record ignored., BaseItemCode=235848-6602A'
    - - :warning
      - 'Line 1636: Product not found, record ignored., BaseItemCode=235848-8402A'
    - - :warning
      - 'Line 1672: Product not found, record ignored., BaseItemCode=91988A'
 |
| 2026-06-16T09:02:24.149920 | ---
- - Inventory
  - - - :warning
      - 'Line 15: Product not found, record ignored., BaseItemCode=200268A'
    - - :warning
      - 'Line 17: Product not found, record ignored., BaseItemCode=200323A'
    - - :warning
      - 'Line 19: Product not found, record ignored., BaseItemCode=200367A'
    - - :warning
      - 'Line 21: Product not found, record ignored., BaseItemCode=200369A'
    - - :warning
      - 'Line 22: Product not found, record ignored., BaseItemCode=200373A'
    - - :warning
      - 'Line 23: Product not found, record ignored., BaseItemCode=200374A'
    - - :warning
      - 'Line 26: Product not found, record ignored., BaseItemCode=200397A'
    - - :warning
      - 'Line 29: Product not found, record ignored., BaseItemCode=200402A'
    - - :warning
      - 'Line 30: Product not found, record ignored., BaseItemCode=200775A'
    - - :warning
      - 'Line 35: Product not found, record ignored., BaseItemCode=200895A'
    - - :warning
      - 'Line 36: Product not found, record ignored., BaseItemCode=200899A'
    - - :warning
      - 'Line 37: Product not found, record ignored., BaseItemCode=200944A'
    - - :warning
      - 'Line 39: Product not found, record ignored., BaseItemCode=201252A'
    - - :warning
      - 'Line 40: Product not found, record ignored., BaseItemCode=201271A'
    - - :warning
      - 'Line 43: Product not found, record ignored., BaseItemCode=201296A'
    - - :warning
      - 'Line 44: Product not found, record ignored., BaseItemCode=201297A'
    - - :warning
      - 'Line 45: Product not found, record ignored., BaseItemCode=201383A'
    - - :warning
      - 'Line 50: Product not found, record ignored., BaseItemCode=201466A'
    - - :warning
      - 'Line 56: Product not found, record ignored., BaseItemCode=201712A'
    - - :warning
      - 'Line 62: Product not found, record ignored., BaseItemCode=201734A'
    - - :warning
      - 'Line 63: Product not found, record ignored., BaseItemCode=201735A'
    - - :warning
      - 'Line 64: Product not found, record ignored., BaseItemCode=201736A'
    - - :warning
      - 'Line 65: Product not found, record ignored., BaseItemCode=201737A'
    - - :warning
      - 'Line 82: Product not found, record ignored., BaseItemCode=202081A'
    - - :warning
      - 'Line 92: Product not found, record ignored., BaseItemCode=202149A'
    - - :warning
      - 'Line 93: Product not found, record ignored., BaseItemCode=202156A'
    - - :warning
      - 'Line 94: Product not found, record ignored., BaseItemCode=202164A'
    - - :warning
      - 'Line 97: Product not found, record ignored., BaseItemCode=202176A'
    - - :warning
      - 'Line 104: Product not found, record ignored., BaseItemCode=202274A'
    - - :warning
      - 'Line 105: Product not found, record ignored., BaseItemCode=202275A'
    - - :warning
      - 'Line 110: Product not found, record ignored., BaseItemCode=202299A'
    - - :warning
      - 'Line 114: Product not found, record ignored., BaseItemCode=202357A'
    - - :warning
      - 'Line 132: Product not found, record ignored., BaseItemCode=202633A'
    - - :warning
      - 'Line 133: Product not found, record ignored., BaseItemCode=202634A'
    - - :warning
      - 'Line 134: Product not found, record ignored., BaseItemCode=202635A'
    - - :warning
      - 'Line 135: Product not found, record ignored., BaseItemCode=202836A'
    - - :warning
      - 'Line 136: Product not found, record ignored., BaseItemCode=202839A'
    - - :warning
      - 'Line 137: Product not found, record ignored., BaseItemCode=202842A'
    - - :warning
      - 'Line 138: Product not found, record ignored., BaseItemCode=202844A'
    - - :warning
      - 'Line 139: Product not found, record ignored., BaseItemCode=202851A'
    - - :warning
      - 'Line 144: Product not found, record ignored., BaseItemCode=202864A'
    - - :warning
      - 'Line 147: Product not found, record ignored., BaseItemCode=202898A'
    - - :warning
      - 'Line 148: Product not found, record ignored., BaseItemCode=202953A'
    - - :warning
      - 'Line 157: Product not found, record ignored., BaseItemCode=203108A'
    - - :warning
      - 'Line 158: Product not found, record ignored., BaseItemCode=203185A'
    - - :warning
      - 'Line 160: Product not found, record ignored., BaseItemCode=203187A'
    - - :warning
      - 'Line 161: Product not found, record ignored., BaseItemCode=203188A'
    - - :warning
      - 'Line 165: Product not found, record ignored., BaseItemCode=203221A'
    - - :warning
      - 'Line 166: Product not found, record ignored., BaseItemCode=203222A'
    - - :warning
      - 'Line 167: Product not found, record ignored., BaseItemCode=203246A'
    - - :warning
      - 'Line 168: Product not found, record ignored., BaseItemCode=203247A'
    - - :warning
      - 'Line 169: Product not found, record ignored., BaseItemCode=203249A'
    - - :warning
      - 'Line 179: Product not found, record ignored., BaseItemCode=203446A'
    - - :warning
      - 'Line 185: Product not found, record ignored., BaseItemCode=203475A'
    - - :warning
      - 'Line 188: Product not found, record ignored., BaseItemCode=203542A'
    - - :warning
      - 'Line 190: Product not found, record ignored., BaseItemCode=203646A'
    - - :warning
      - 'Line 196: Product not found, record ignored., BaseItemCode=203666A'
    - - :warning
      - 'Line 202: Product not found, record ignored., BaseItemCode=203729A'
    - - :warning
      - 'Line 203: Product not found, record ignored., BaseItemCode=203753A'
    - - :warning
      - 'Line 228: Product not found, record ignored., BaseItemCode=203916A'
    - - :warning
      - 'Line 229: Product not found, record ignored., BaseItemCode=203945A'
    - - :warning
      - 'Line 232: Product not found, record ignored., BaseItemCode=203962A'
    - - :warning
      - 'Line 233: Product not found, record ignored., BaseItemCode=203963A'
    - - :warning
      - 'Line 235: Product not found, record ignored., BaseItemCode=203998A'
    - - :warning
      - 'Line 237: Product not found, record ignored., BaseItemCode=204025A'
    - - :warning
      - 'Line 238: Product not found, record ignored., BaseItemCode=204026A'
    - - :warning
      - 'Line 239: Product not found, record ignored., BaseItemCode=204027A'
    - - :warning
      - 'Line 248: Product not found, record ignored., BaseItemCode=204049A'
    - - :warning
      - 'Line 253: Product not found, record ignored., BaseItemCode=204061A'
    - - :warning
      - 'Line 255: Product not found, record ignored., BaseItemCode=204065'
    - - :warning
      - 'Line 256: Product not found, record ignored., BaseItemCode=204069'
    - - :warning
      - 'Line 257: Product not found, record ignored., BaseItemCode=204071'
    - - :warning
      - 'Line 263: Product not found, record ignored., BaseItemCode=204077A'
    - - :warning
      - 'Line 273: Product not found, record ignored., BaseItemCode=204102A'
    - - :warning
      - 'Line 274: Product not found, record ignored., BaseItemCode=204105A'
    - - :warning
      - 'Line 275: Product not found, record ignored., BaseItemCode=204109A'
    - - :warning
      - 'Line 289: Product not found, record ignored., BaseItemCode=204141A'
    - - :warning
      - 'Line 290: Product not found, record ignored., BaseItemCode=204147A'
    - - :warning
      - 'Line 291: Product not found, record ignored., BaseItemCode=204195A'
    - - :warning
      - 'Line 298: Product not found, record ignored., BaseItemCode=204213A'
    - - :warning
      - 'Line 299: Product not found, record ignored., BaseItemCode=204214A'
    - - :warning
      - 'Line 331: Product not found, record ignored., BaseItemCode=204361A'
    - - :warning
      - 'Line 332: Product not found, record ignored., BaseItemCode=204362A'
    - - :warning
      - 'Line 340: Product not found, record ignored., BaseItemCode=204375A'
    - - :warning
      - 'Line 343: Product not found, record ignored., BaseItemCode=204446A'
    - - :warning
      - 'Line 344: Product not found, record ignored., BaseItemCode=204447A'
    - - :warning
      - 'Line 345: Product not found, record ignored., BaseItemCode=204464A'
    - - :warning
      - 'Line 346: Product not found, record ignored., BaseItemCode=204466A'
    - - :warning
      - 'Line 347: Product not found, record ignored., BaseItemCode=204467A'
    - - :warning
      - 'Line 348: Product not found, record ignored., BaseItemCode=204472A'
    - - :warning
      - 'Line 354: Product not found, record ignored., BaseItemCode=204539A'
    - - :warning
      - 'Line 356: Product not found, record ignored., BaseItemCode=204543A'
    - - :warning
      - 'Line 357: Product not found, record ignored., BaseItemCode=204544A'
    - - :warning
      - 'Line 358: Product not found, record ignored., BaseItemCode=204554A'
    - - :warning
      - 'Line 359: Product not found, record ignored., BaseItemCode=204555A'
    - - :warning
      - 'Line 361: Product not found, record ignored., BaseItemCode=204569A'
    - - :warning
      - 'Line 362: Product not found, record ignored., BaseItemCode=204586A'
    - - :warning
      - 'Line 363: Product not found, record ignored., BaseItemCode=204587A'
    - - :warning
      - 'Line 364: Product not found, record ignored., BaseItemCode=204589A'
    - - :warning
      - 'Line 365: Product not found, record ignored., BaseItemCode=204595A'
    - - :warning
      - 'Line 376: Product not found, record ignored., BaseItemCode=204642A'
    - - :warning
      - 'Line 380: Product not found, record ignored., BaseItemCode=204701A'
    - - :warning
      - 'Line 381: Product not found, record ignored., BaseItemCode=204702A'
    - - :warning
      - 'Line 384: Product not found, record ignored., BaseItemCode=204708A'
    - - :warning
      - 'Line 407: Product not found, record ignored., BaseItemCode=204895A'
    - - :warning
      - 'Line 413: Product not found, record ignored., BaseItemCode=204923A'
    - - :warning
      - 'Line 414: Product not found, record ignored., BaseItemCode=204924A'
    - - :warning
      - 'Line 424: Product not found, record ignored., BaseItemCode=205072A'
    - - :warning
      - 'Line 459: Product not found, record ignored., BaseItemCode=205327A'
    - - :warning
      - 'Line 460: Product not found, record ignored., BaseItemCode=205331A'
    - - :warning
      - 'Line 462: Product not found, record ignored., BaseItemCode=205351A'
    - - :warning
      - 'Line 463: Product not found, record ignored., BaseItemCode=205363A'
    - - :warning
      - 'Line 473: Product not found, record ignored., BaseItemCode=205588A'
    - - :warning
      - 'Line 477: Product not found, record ignored., BaseItemCode=205618A'
    - - :warning
      - 'Line 478: Product not found, record ignored., BaseItemCode=205621A'
    - - :warning
      - 'Line 486: Product not found, record ignored., BaseItemCode=205643A'
    - - :warning
      - 'Line 489: Product not found, record ignored., BaseItemCode=205655A'
    - - :warning
      - 'Line 502: Product not found, record ignored., BaseItemCode=205755A'
    - - :warning
      - 'Line 509: Product not found, record ignored., BaseItemCode=205766A'
    - - :warning
      - 'Line 526: Product not found, record ignored., BaseItemCode=205841A'
    - - :warning
      - 'Line 527: Product not found, record ignored., BaseItemCode=205842A'
    - - :warning
      - 'Line 528: Product not found, record ignored., BaseItemCode=205843A'
    - - :warning
      - 'Line 529: Product not found, record ignored., BaseItemCode=205844A'
    - - :warning
      - 'Line 561: Product not found, record ignored., BaseItemCode=206032A'
    - - :warning
      - 'Line 582: Product not found, record ignored., BaseItemCode=206089A'
    - - :warning
      - 'Line 1130: Product not found, record ignored., BaseItemCode=235003-4401A'
    - - :warning
      - 'Line 1131: Product not found, record ignored., BaseItemCode=235003-5201A'
    - - :warning
      - 'Line 1132: Product not found, record ignored., BaseItemCode=235003-5202A'
    - - :warning
      - 'Line 1133: Product not found, record ignored., BaseItemCode=235003-5218A'
    - - :warning
      - 'Line 1134: Product not found, record ignored., BaseItemCode=235003-5223A'
    - - :warning
      - 'Line 1135: Product not found, record ignored., BaseItemCode=235100-5201A'
    - - :warning
      - 'Line 1136: Product not found, record ignored., BaseItemCode=235100-5202A'
    - - :warning
      - 'Line 1137: Product not found, record ignored., BaseItemCode=235112-5201A'
    - - :warning
      - 'Line 1138: Product not found, record ignored., BaseItemCode=235112-5202A'
    - - :warning
      - 'Line 1139: Product not found, record ignored., BaseItemCode=235112-5216A'
    - - :warning
      - 'Line 1140: Product not found, record ignored., BaseItemCode=235112-5225A'
    - - :warning
      - 'Line 1141: Product not found, record ignored., BaseItemCode=235112-6001A'
    - - :warning
      - 'Line 1142: Product not found, record ignored., BaseItemCode=235112-6002A'
    - - :warning
      - 'Line 1143: Product not found, record ignored., BaseItemCode=235112-6016A'
    - - :warning
      - 'Line 1144: Product not found, record ignored., BaseItemCode=235112-6025A'
    - - :warning
      - 'Line 1145: Product not found, record ignored., BaseItemCode=235848-6602A'
    - - :warning
      - 'Line 1146: Product not found, record ignored., BaseItemCode=235848-8402A'
    - - :warning
      - 'Line 1147: Product not found, record ignored., BaseItemCode=235997-1201A'
    - - :warning
      - 'Line 1148: Product not found, record ignored., BaseItemCode=235997-1202A'
    - - :warning
      - 'Line 1149: Product not found, record ignored., BaseItemCode=235997-2401A'
    - - :warning
      - 'Line 1150: Product not found, record ignored., BaseItemCode=235997-2402A'
    - - :warning
      - 'Line 1151: Product not found, record ignored., BaseItemCode=235997-3601A'
    - - :warning
      - 'Line 1152: Product not found, record ignored., BaseItemCode=235997-3602A'
    - - :warning
      - 'Line 1155: Product not found, record ignored., BaseItemCode=31372A'
    - - :warning
      - 'Line 1169: Product not found, record ignored., BaseItemCode=390024A'
    - - :warning
      - 'Line 1194: Product not found, record ignored., BaseItemCode=390249A'
    - - :warning
      - 'Line 1246: Product not found, record ignored., BaseItemCode=39249A'
    - - :warning
      - 'Line 1254: Product not found, record ignored., BaseItemCode=39499A'
    - - :warning
      - 'Line 1256: Product not found, record ignored., BaseItemCode=39591A'
    - - :warning
      - 'Line 1261: Product not found, record ignored., BaseItemCode=39614A'
    - - :warning
      - 'Line 1262: Product not found, record ignored., BaseItemCode=39615A'
    - - :warning
      - 'Line 1263: Product not found, record ignored., BaseItemCode=39628A'
    - - :warning
      - 'Line 1316: Product not found, record ignored., BaseItemCode=43197A'
    - - :warning
      - 'Line 1320: Product not found, record ignored., BaseItemCode=43256A'
    - - :warning
      - 'Line 1323: Product not found, record ignored., BaseItemCode=43311A'
    - - :warning
      - 'Line 1339: Product not found, record ignored., BaseItemCode=43617A'
    - - :warning
      - 'Line 1343: Product not found, record ignored., BaseItemCode=43645A'
    - - :warning
      - 'Line 1349: Product not found, record ignored., BaseItemCode=43682A'
    - - :warning
      - 'Line 1360: Product not found, record ignored., BaseItemCode=43873A'
    - - :warning
      - 'Line 1386: Product not found, record ignored., BaseItemCode=49619A'
    - - :warning
      - 'Line 1417: Product not found, record ignored., BaseItemCode=83241A'
    - - :warning
      - 'Line 1420: Product not found, record ignored., BaseItemCode=83733A'
    - - :warning
      - 'Line 1441: Product not found, record ignored., BaseItemCode=86391A'
    - - :warning
      - 'Line 1451: Product not found, record ignored., BaseItemCode=88968A'
    - - :warning
      - 'Line 1461: Product not found, record ignored., BaseItemCode=900375A'
    - - :warning
      - 'Line 1506: Product not found, record ignored., BaseItemCode=91046A'
    - - :warning
      - 'Line 1507: Product not found, record ignored., BaseItemCode=91416A'
    - - :warning
      - 'Line 1509: Product not found, record ignored., BaseItemCode=91732A'
    - - :warning
      - 'Line 1510: Product not found, record ignored., BaseItemCode=91733A'
    - - :warning
      - 'Line 1511: Product not found, record ignored., BaseItemCode=91988A'
    - - :warning
      - 'Line 1534: Product not found, record ignored., BaseItemCode=93374A'
    - - :warning
      - 'Line 1544: Product not found, record ignored., BaseItemCode=94304A'
    - - :warning
      - 'Line 1546: Product not found, record ignored., BaseItemCode=94353A'
    - - :warning
      - 'Line 1550: Product not found, record ignored., BaseItemCode=94465A'
    - - :warning
      - 'Line 1562: Product not found, record ignored., BaseItemCode=95122A'
    - - :warning
      - 'Line 1565: Product not found, record ignored., BaseItemCode=95143A'
    - - :warning
      - 'Line 1576: Product not found, record ignored., BaseItemCode=95996A'
    - - :warning
      - 'Line 1582: Product not found, record ignored., BaseItemCode=96605A'
    - - :warning
      - 'Line 1583: Product not found, record ignored., BaseItemCode=96606A'
    - - :warning
      - 'Line 1584: Product not found, record ignored., BaseItemCode=96607A'
    - - :warning
      - 'Line 1585: Product not found, record ignored., BaseItemCode=96608A'
    - - :warning
      - 'Line 1587: Product not found, record ignored., BaseItemCode=96726A'
    - - :warning
      - 'Line 1589: Product not found, record ignored., BaseItemCode=96801A'
    - - :warning
      - 'Line 1591: Product not found, record ignored., BaseItemCode=96932A'
    - - :warning
      - 'Line 1596: Product not found, record ignored., BaseItemCode=97374A'
    - - :warning
      - 'Line 1598: Product not found, record ignored., BaseItemCode=97395A'
    - - :warning
      - 'Line 1599: Product not found, record ignored., BaseItemCode=97396A'
    - - :warning
      - 'Line 1600: Product not found, record ignored., BaseItemCode=97397A'
    - - :warning
      - 'Line 1601: Product not found, record ignored., BaseItemCode=97441A'
    - - :warning
      - 'Line 1602: Product not found, record ignored., BaseItemCode=97442A'
    - - :warning
      - 'Line 1619: Product not found, record ignored., BaseItemCode=97914A'
    - - :warning
      - 'Line 1621: Product not found, record ignored., BaseItemCode=97949A'
    - - :warning
      - 'Line 1637: Product not found, record ignored., BaseItemCode=98441A'
    - - :warning
      - 'Line 1642: Product not found, record ignored., BaseItemCode=98735A'
    - - :warning
      - 'Line 1666: Product not found, record ignored., BaseItemCode=99364A'
    - - :warning
      - 'Line 1676: Product not found, record ignored., BaseItemCode=99561A'
    - - :warning
      - 'Line 1677: Product not found, record ignored., BaseItemCode=99562A'
 |
| 2026-06-16T03:02:22.080142 | ---
- - Customers
  - []
- - Sales Data
  - - - :error
      - 'Line 20: Base item code GE00016201 does not match an active product'
    - - :error
      - 'Line 79: Base item code ET1611 does not match an active product'
    - - :error
      - 'Line 80: Base item code ET1612 does not match an active product'
    - - :error
      - 'Line 145: Base item code GA000049W4 does not match an active product'
    - - :error
      - 'Line 154: Base item code GA00024304 does not match an active product'
    - - :error
      - 'Line 186: Base item code 3TRANS does not match an active product'
    - - :error
      - 'Line 187: Base item code 3TRANS does not match an active product'
    - - :error
      - 'Line 233: Base item code GB00038301 does not match an active product'
    - - :error
      - 'Line 280: Base item code GL2761 does not match an active product'
    - - :error
      - 'Line 299: Base item code 3DIV does not match an active product'
    - - :error
      - 'Line 301: Base item code GE000103W0 does not match an active product'
    - - :error
      - 'Line 346: Base item code GA000051W4 does not match an active product'
    - - :error
      - 'Line 347: Base item code GE000091W5-R does not match an active product'
    - - :error
      - 'Line 357: Base item code GE000091W5-R does not match an active product'
    - - :error
      - 'Line 408: Base item code EG02000101 does not match an active product'
    - - :error
      - 'Line 409: Base item code GE000103W0 does not match an active product'
    - - :error
      - 'Line 435: Base item code GA000050W4 does not match an active product'
    - - :error
      - 'Line 436: Base item code GA00060701 does not match an active product'
    - - :error
      - 'Line 485: Base item code GA00047901 does not match an active product'
    - - :error
      - 'Line 486: Base item code GC00002405 does not match an active product'
    - - :error
      - 'Line 501: Base item code GA000464W4 does not match an active product'
    - - :error
      - 'Line 523: Base item code GE00027401 does not match an active product'
    - - :error
      - 'Line 532: Base item code GE000091W5-R does not match an active product'
    - - :error
      - 'Line 548: Base item code GA000049W4 does not match an active product'
    - - :error
      - 'Line 563: Base item code GE000091W5-R does not match an active product'
    - - :error
      - 'Line 582: Base item code GA000049W4 does not match an active product'
    - - :error
      - 'Line 712: Base item code GE000091W5-R does not match an active product'
    - - :error
      - 'Line 716: Base item code GC00002405 does not match an active product'
    - - :error
      - 'Line 781: Base item code GA000343W0-R does not match an active product'
    - - :error
      - 'Line 855: Base item code GA00014008 does not match an active product'
    - - :error
      - 'Line 865: Base item code 205852A does not match an active product'
    - - :error
      - 'Line 885: Base item code 206626A does not match an active product'
    - - :error
      - 'Line 930: Base item code GA000343W0-R does not match an active product'
    - - :error
      - 'Line 942: Base item code 202032A does not match an active product'
    - - :error
      - 'Line 943: Base item code 202103A does not match an active product'
    - - :error
      - 'Line 963: Base item code GA00062401 does not match an active product'
    - - :error
      - 'Line 977: Base item code GB00038301 does not match an active product'
    - - :error
      - 'Line 1026: Base item code GF00010001 does not match an active product'
    - - :error
      - 'Line 1060: Base item code 206626A does not match an active product'
    - - :error
      - 'Line 1092: Base item code NT010487R1-73 does not match an active product'
    - - :error
      - 'Line 1110: Base item code KATLCASOL25 does not match an active product'
    - - :error
      - 'Line 1111: Base item code MG011676R1 does not match an active product'
    - - :error
      - 'Line 1133: Base item code 206626A does not match an active product'
    - - :error
      - 'Line 1215: Base item code GA00014008 does not match an active product'
    - - :error
      - 'Line 1271: Base item code GE000103W0 does not match an active product'
    - - :error
      - 'Line 1303: Base item code GE000091W5-R does not match an active product'
    - - :error
      - 'Line 1323: Base item code GA00014008 does not match an active product'
    - - :error
      - 'Line 1370: Base item code KATLCA54 does not match an active product'
    - - :error
      - 'Line 1371: Base item code KATLCASOL25 does not match an active product'
    - - :error
      - 'Line 1372: Base item code KATNCA25/01 does not match an active product'
    - - :error
      - 'Line 1719: Either quantity invoiced or quantity on order is required'
    - - :error
      - 'Line 1988: Either quantity invoiced or quantity on order is required'
    - - :error
      - 'Line 2463: Either quantity invoiced or quantity on order is required'
    - - :warning
      - "-237 more rows with invalid products"
 |
| 2026-06-15T19:32:14.464495 | ---
- - Inventory
  - - - :warning
      - 'Line 202: Product not found, record ignored., BaseItemCode=900375A'
    - - :warning
      - 'Line 205: Product not found, record ignored., BaseItemCode=200895A'
    - - :warning
      - 'Line 206: Product not found, record ignored., BaseItemCode=200899A'
    - - :warning
      - 'Line 207: Product not found, record ignored., BaseItemCode=201383A'
    - - :warning
      - 'Line 211: Product not found, record ignored., BaseItemCode=201735A'
    - - :warning
      - 'Line 213: Product not found, record ignored., BaseItemCode=202081A'
    - - :warning
      - 'Line 215: Product not found, record ignored., BaseItemCode=202149A'
    - - :warning
      - 'Line 217: Product not found, record ignored., BaseItemCode=202275A'
    - - :warning
      - 'Line 218: Product not found, record ignored., BaseItemCode=202357A'
    - - :warning
      - 'Line 221: Product not found, record ignored., BaseItemCode=202839A'
    - - :warning
      - 'Line 222: Product not found, record ignored., BaseItemCode=202842A'
    - - :warning
      - 'Line 223: Product not found, record ignored., BaseItemCode=202851A'
    - - :warning
      - 'Line 224: Product not found, record ignored., BaseItemCode=202864A'
    - - :warning
      - 'Line 225: Product not found, record ignored., BaseItemCode=202898A'
    - - :warning
      - 'Line 226: Product not found, record ignored., BaseItemCode=203249A'
    - - :warning
      - 'Line 227: Product not found, record ignored., BaseItemCode=203446A'
    - - :warning
      - 'Line 228: Product not found, record ignored., BaseItemCode=203542A'
    - - :warning
      - 'Line 229: Product not found, record ignored., BaseItemCode=203646A'
    - - :warning
      - 'Line 230: Product not found, record ignored., BaseItemCode=203753A'
    - - :warning
      - 'Line 231: Product not found, record ignored., BaseItemCode=203945A'
    - - :warning
      - 'Line 232: Product not found, record ignored., BaseItemCode=203962A'
    - - :warning
      - 'Line 234: Product not found, record ignored., BaseItemCode=204049A'
    - - :warning
      - 'Line 235: Product not found, record ignored., BaseItemCode=204077A'
    - - :warning
      - 'Line 238: Product not found, record ignored., BaseItemCode=204109A'
    - - :warning
      - 'Line 239: Product not found, record ignored., BaseItemCode=204141A'
    - - :warning
      - 'Line 240: Product not found, record ignored., BaseItemCode=204147A'
    - - :warning
      - 'Line 241: Product not found, record ignored., BaseItemCode=204195A'
    - - :warning
      - 'Line 245: Product not found, record ignored., BaseItemCode=204361A'
    - - :warning
      - 'Line 246: Product not found, record ignored., BaseItemCode=204375A'
    - - :warning
      - 'Line 247: Product not found, record ignored., BaseItemCode=204446A'
    - - :warning
      - 'Line 248: Product not found, record ignored., BaseItemCode=204447A'
    - - :warning
      - 'Line 249: Product not found, record ignored., BaseItemCode=204464A'
    - - :warning
      - 'Line 250: Product not found, record ignored., BaseItemCode=204466A'
    - - :warning
      - 'Line 251: Product not found, record ignored., BaseItemCode=204467A'
    - - :warning
      - 'Line 252: Product not found, record ignored., BaseItemCode=204539A'
    - - :warning
      - 'Line 253: Product not found, record ignored., BaseItemCode=204543A'
    - - :warning
      - 'Line 254: Product not found, record ignored., BaseItemCode=204544A'
    - - :warning
      - 'Line 255: Product not found, record ignored., BaseItemCode=204555A'
    - - :warning
      - 'Line 256: Product not found, record ignored., BaseItemCode=204587A'
    - - :warning
      - 'Line 257: Product not found, record ignored., BaseItemCode=204589A'
    - - :warning
      - 'Line 262: Product not found, record ignored., BaseItemCode=204708A'
    - - :warning
      - 'Line 265: Product not found, record ignored., BaseItemCode=205072A'
    - - :warning
      - 'Line 268: Product not found, record ignored., BaseItemCode=205327A'
    - - :warning
      - 'Line 269: Product not found, record ignored., BaseItemCode=205331A'
    - - :warning
      - 'Line 271: Product not found, record ignored., BaseItemCode=205621A'
    - - :warning
      - 'Line 272: Product not found, record ignored., BaseItemCode=205655A'
    - - :warning
      - 'Line 274: Product not found, record ignored., BaseItemCode=205843A'
    - - :warning
      - 'Line 275: Product not found, record ignored., BaseItemCode=205844A'
    - - :warning
      - 'Line 276: Product not found, record ignored., BaseItemCode=235003-5223A'
    - - :warning
      - 'Line 277: Product not found, record ignored., BaseItemCode=235112-5202A'
    - - :warning
      - 'Line 278: Product not found, record ignored., BaseItemCode=235112-6001A'
    - - :warning
      - 'Line 279: Product not found, record ignored., BaseItemCode=235112-6002A'
    - - :warning
      - 'Line 280: Product not found, record ignored., BaseItemCode=235112-6016A'
    - - :warning
      - 'Line 281: Product not found, record ignored., BaseItemCode=235997-2401A'
    - - :warning
      - 'Line 282: Product not found, record ignored., BaseItemCode=235997-3601A'
    - - :warning
      - 'Line 290: Product not found, record ignored., BaseItemCode=390249A'
    - - :warning
      - 'Line 292: Product not found, record ignored., BaseItemCode=39591A'
    - - :warning
      - 'Line 293: Product not found, record ignored., BaseItemCode=39615A'
    - - :warning
      - 'Line 294: Product not found, record ignored., BaseItemCode=39628A'
    - - :warning
      - 'Line 297: Product not found, record ignored., BaseItemCode=43256A'
    - - :warning
      - 'Line 300: Product not found, record ignored., BaseItemCode=43645A'
    - - :warning
      - 'Line 303: Product not found, record ignored., BaseItemCode=43682A'
    - - :warning
      - 'Line 304: Product not found, record ignored., BaseItemCode=43873A'
    - - :warning
      - 'Line 306: Product not found, record ignored., BaseItemCode=49619A'
    - - :warning
      - 'Line 311: Product not found, record ignored., BaseItemCode=86391A'
    - - :warning
      - 'Line 315: Product not found, record ignored., BaseItemCode=88968A'
    - - :warning
      - 'Line 317: Product not found, record ignored., BaseItemCode=91416A'
    - - :warning
      - 'Line 320: Product not found, record ignored., BaseItemCode=94465A'
    - - :warning
      - 'Line 323: Product not found, record ignored., BaseItemCode=97441A'
    - - :warning
      - 'Line 324: Product not found, record ignored., BaseItemCode=97442A'
    - - :warning
      - 'Line 325: Product not found, record ignored., BaseItemCode=97949A'
    - - :warning
      - 'Line 329: Product not found, record ignored., BaseItemCode=98441A'
    - - :warning
      - 'Line 332: Product not found, record ignored., BaseItemCode=99561A'
    - - :warning
      - 'Line 333: Product not found, record ignored., BaseItemCode=99562A'
    - - :warning
      - 'Line 343: Product not found, record ignored., BaseItemCode=200268A'
    - - :warning
      - 'Line 373: Product not found, record ignored., BaseItemCode=202274A'
    - - :warning
      - 'Line 378: Product not found, record ignored., BaseItemCode=202299A'
    - - :warning
      - 'Line 394: Product not found, record ignored., BaseItemCode=202633A'
    - - :warning
      - 'Line 395: Product not found, record ignored., BaseItemCode=202836A'
    - - :warning
      - 'Line 409: Product not found, record ignored., BaseItemCode=203187A'
    - - :warning
      - 'Line 410: Product not found, record ignored., BaseItemCode=203188A'
    - - :warning
      - 'Line 412: Product not found, record ignored., BaseItemCode=203221A'
    - - :warning
      - 'Line 413: Product not found, record ignored., BaseItemCode=203222A'
    - - :warning
      - 'Line 414: Product not found, record ignored., BaseItemCode=203246A'
    - - :warning
      - 'Line 415: Product not found, record ignored., BaseItemCode=203247A'
    - - :warning
      - 'Line 464: Product not found, record ignored., BaseItemCode=203998A'
    - - :warning
      - 'Line 466: Product not found, record ignored., BaseItemCode=204027A'
    - - :warning
      - 'Line 522: Product not found, record ignored., BaseItemCode=204362A'
    - - :warning
      - 'Line 542: Product not found, record ignored., BaseItemCode=204642A'
    - - :warning
      - 'Line 555: Product not found, record ignored., BaseItemCode=204895A'
    - - :warning
      - 'Line 578: Product not found, record ignored., BaseItemCode=205351A'
    - - :warning
      - 'Line 579: Product not found, record ignored., BaseItemCode=205363A'
    - - :warning
      - 'Line 586: Product not found, record ignored., BaseItemCode=205618A'
    - - :warning
      - 'Line 590: Product not found, record ignored., BaseItemCode=205643A'
    - - :warning
      - 'Line 602: Product not found, record ignored., BaseItemCode=205755A'
    - - :warning
      - 'Line 608: Product not found, record ignored., BaseItemCode=205766A'
    - - :warning
      - 'Line 646: Product not found, record ignored., BaseItemCode=206032A'
    - - :warning
      - 'Line 890: Product not found, record ignored., BaseItemCode=39499A'
    - - :warning
      - 'Line 894: Product not found, record ignored., BaseItemCode=39614A'
    - - :warning
      - 'Line 1070: Product not found, record ignored., BaseItemCode=91732A'
    - - :warning
      - 'Line 1071: Product not found, record ignored., BaseItemCode=91733A'
    - - :warning
      - 'Line 1092: Product not found, record ignored., BaseItemCode=94353A'
    - - :warning
      - 'Line 1101: Product not found, record ignored., BaseItemCode=95122A'
    - - :warning
      - 'Line 1115: Product not found, record ignored., BaseItemCode=96605A'
    - - :warning
      - 'Line 1116: Product not found, record ignored., BaseItemCode=96606A'
    - - :warning
      - 'Line 1117: Product not found, record ignored., BaseItemCode=96607A'
    - - :warning
      - 'Line 1118: Product not found, record ignored., BaseItemCode=96608A'
    - - :warning
      - 'Line 1120: Product not found, record ignored., BaseItemCode=96726A'
    - - :warning
      - 'Line 1127: Product not found, record ignored., BaseItemCode=97374A'
    - - :warning
      - 'Line 1129: Product not found, record ignored., BaseItemCode=97395A'
    - - :warning
      - 'Line 1130: Product not found, record ignored., BaseItemCode=97396A'
    - - :warning
      - 'Line 1131: Product not found, record ignored., BaseItemCode=97397A'
    - - :warning
      - 'Line 1144: Product not found, record ignored., BaseItemCode=97914A'
    - - :warning
      - 'Line 1220: Product not found, record ignored., BaseItemCode=200323A'
    - - :warning
      - 'Line 1222: Product not found, record ignored., BaseItemCode=200367A'
    - - :warning
      - 'Line 1223: Product not found, record ignored., BaseItemCode=200369A'
    - - :warning
      - 'Line 1224: Product not found, record ignored., BaseItemCode=200373A'
    - - :warning
      - 'Line 1225: Product not found, record ignored., BaseItemCode=200374A'
    - - :warning
      - 'Line 1226: Product not found, record ignored., BaseItemCode=200397A'
    - - :warning
      - 'Line 1227: Product not found, record ignored., BaseItemCode=200402A'
    - - :warning
      - 'Line 1228: Product not found, record ignored., BaseItemCode=200775A'
    - - :warning
      - 'Line 1229: Product not found, record ignored., BaseItemCode=200944A'
    - - :warning
      - 'Line 1230: Product not found, record ignored., BaseItemCode=201252A'
    - - :warning
      - 'Line 1231: Product not found, record ignored., BaseItemCode=201271A'
    - - :warning
      - 'Line 1232: Product not found, record ignored., BaseItemCode=201296A'
    - - :warning
      - 'Line 1233: Product not found, record ignored., BaseItemCode=201297A'
    - - :warning
      - 'Line 1237: Product not found, record ignored., BaseItemCode=201466A'
    - - :warning
      - 'Line 1238: Product not found, record ignored., BaseItemCode=201712A'
    - - :warning
      - 'Line 1240: Product not found, record ignored., BaseItemCode=201734A'
    - - :warning
      - 'Line 1241: Product not found, record ignored., BaseItemCode=201736A'
    - - :warning
      - 'Line 1242: Product not found, record ignored., BaseItemCode=201737A'
    - - :warning
      - 'Line 1244: Product not found, record ignored., BaseItemCode=202156A'
    - - :warning
      - 'Line 1245: Product not found, record ignored., BaseItemCode=202164A'
    - - :warning
      - 'Line 1246: Product not found, record ignored., BaseItemCode=202176A'
    - - :warning
      - 'Line 1248: Product not found, record ignored., BaseItemCode=202634A'
    - - :warning
      - 'Line 1249: Product not found, record ignored., BaseItemCode=202635A'
    - - :warning
      - 'Line 1250: Product not found, record ignored., BaseItemCode=202844A'
    - - :warning
      - 'Line 1251: Product not found, record ignored., BaseItemCode=202953A'
    - - :warning
      - 'Line 1252: Product not found, record ignored., BaseItemCode=203108A'
    - - :warning
      - 'Line 1253: Product not found, record ignored., BaseItemCode=203185A'
    - - :warning
      - 'Line 1255: Product not found, record ignored., BaseItemCode=203475A'
    - - :warning
      - 'Line 1257: Product not found, record ignored., BaseItemCode=203666A'
    - - :warning
      - 'Line 1258: Product not found, record ignored., BaseItemCode=203729A'
    - - :warning
      - 'Line 1259: Product not found, record ignored., BaseItemCode=203916A'
    - - :warning
      - 'Line 1260: Product not found, record ignored., BaseItemCode=203963A'
    - - :warning
      - 'Line 1262: Product not found, record ignored., BaseItemCode=204025A'
    - - :warning
      - 'Line 1263: Product not found, record ignored., BaseItemCode=204026A'
    - - :warning
      - 'Line 1264: Product not found, record ignored., BaseItemCode=204061A'
    - - :warning
      - 'Line 1265: Product not found, record ignored., BaseItemCode=204065'
    - - :warning
      - 'Line 1266: Product not found, record ignored., BaseItemCode=204069'
    - - :warning
      - 'Line 1267: Product not found, record ignored., BaseItemCode=204071'
    - - :warning
      - 'Line 1269: Product not found, record ignored., BaseItemCode=204102A'
    - - :warning
      - 'Line 1270: Product not found, record ignored., BaseItemCode=204105A'
    - - :warning
      - 'Line 1272: Product not found, record ignored., BaseItemCode=204213A'
    - - :warning
      - 'Line 1273: Product not found, record ignored., BaseItemCode=204214A'
    - - :warning
      - 'Line 1275: Product not found, record ignored., BaseItemCode=204472A'
    - - :warning
      - 'Line 1276: Product not found, record ignored., BaseItemCode=204554A'
    - - :warning
      - 'Line 1277: Product not found, record ignored., BaseItemCode=204569A'
    - - :warning
      - 'Line 1278: Product not found, record ignored., BaseItemCode=204586A'
    - - :warning
      - 'Line 1279: Product not found, record ignored., BaseItemCode=204595A'
    - - :warning
      - 'Line 1282: Product not found, record ignored., BaseItemCode=204701A'
    - - :warning
      - 'Line 1283: Product not found, record ignored., BaseItemCode=204702A'
    - - :warning
      - 'Line 1285: Product not found, record ignored., BaseItemCode=204923A'
    - - :warning
      - 'Line 1286: Product not found, record ignored., BaseItemCode=204924A'
    - - :warning
      - 'Line 1290: Product not found, record ignored., BaseItemCode=205588A'
    - - :warning
      - 'Line 1293: Product not found, record ignored., BaseItemCode=205841A'
    - - :warning
      - 'Line 1294: Product not found, record ignored., BaseItemCode=206089A'
    - - :warning
      - 'Line 1299: Product not found, record ignored., BaseItemCode=235003-4401A'
    - - :warning
      - 'Line 1300: Product not found, record ignored., BaseItemCode=235003-5201A'
    - - :warning
      - 'Line 1301: Product not found, record ignored., BaseItemCode=235003-5202A'
    - - :warning
      - 'Line 1302: Product not found, record ignored., BaseItemCode=235003-5218A'
    - - :warning
      - 'Line 1303: Product not found, record ignored., BaseItemCode=235100-5201A'
    - - :warning
      - 'Line 1304: Product not found, record ignored., BaseItemCode=235100-5202A'
    - - :warning
      - 'Line 1305: Product not found, record ignored., BaseItemCode=235112-5201A'
    - - :warning
      - 'Line 1306: Product not found, record ignored., BaseItemCode=235112-5216A'
    - - :warning
      - 'Line 1307: Product not found, record ignored., BaseItemCode=235112-5225A'
    - - :warning
      - 'Line 1308: Product not found, record ignored., BaseItemCode=235112-6025A'
    - - :warning
      - 'Line 1309: Product not found, record ignored., BaseItemCode=235997-1201A'
    - - :warning
      - 'Line 1310: Product not found, record ignored., BaseItemCode=235997-1202A'
    - - :warning
      - 'Line 1311: Product not found, record ignored., BaseItemCode=235997-2402A'
    - - :warning
      - 'Line 1312: Product not found, record ignored., BaseItemCode=235997-3602A'
    - - :warning
      - 'Line 1313: Product not found, record ignored., BaseItemCode=31372A'
    - - :warning
      - 'Line 1316: Product not found, record ignored., BaseItemCode=390024A'
    - - :warning
      - 'Line 1320: Product not found, record ignored., BaseItemCode=39249A'
    - - :warning
      - 'Line 1323: Product not found, record ignored., BaseItemCode=43197A'
    - - :warning
      - 'Line 1324: Product not found, record ignored., BaseItemCode=43311A'
    - - :warning
      - 'Line 1325: Product not found, record ignored., BaseItemCode=43617A'
    - - :warning
      - 'Line 1327: Product not found, record ignored., BaseItemCode=83241A'
    - - :warning
      - 'Line 1328: Product not found, record ignored., BaseItemCode=83733A'
    - - :warning
      - 'Line 1330: Product not found, record ignored., BaseItemCode=91046A'
    - - :warning
      - 'Line 1333: Product not found, record ignored., BaseItemCode=93374A'
    - - :warning
      - 'Line 1334: Product not found, record ignored., BaseItemCode=94304A'
    - - :warning
      - 'Line 1337: Product not found, record ignored., BaseItemCode=95143A'
    - - :warning
      - 'Line 1338: Product not found, record ignored., BaseItemCode=95996A'
    - - :warning
      - 'Line 1340: Product not found, record ignored., BaseItemCode=96801A'
    - - :warning
      - 'Line 1341: Product not found, record ignored., BaseItemCode=96932A'
    - - :warning
      - 'Line 1345: Product not found, record ignored., BaseItemCode=98735A'
    - - :warning
      - 'Line 1347: Product not found, record ignored., BaseItemCode=99364A'
    - - :warning
      - 'Line 1351: Product not found, record ignored., BaseItemCode=205842A'
    - - :warning
      - 'Line 1634: Product not found, record ignored., BaseItemCode=235848-6602A'
    - - :warning
      - 'Line 1635: Product not found, record ignored., BaseItemCode=235848-8402A'
    - - :warning
      - 'Line 1671: Product not found, record ignored., BaseItemCode=91988A'
 |
| 2026-06-15T15:07:24.304659 | ---
- - Inventory
  - - - :warning
      - 'Line 15: Product not found, record ignored., BaseItemCode=200268A'
    - - :warning
      - 'Line 17: Product not found, record ignored., BaseItemCode=200323A'
    - - :warning
      - 'Line 19: Product not found, record ignored., BaseItemCode=200367A'
    - - :warning
      - 'Line 21: Product not found, record ignored., BaseItemCode=200369A'
    - - :warning
      - 'Line 22: Product not found, record ignored., BaseItemCode=200373A'
    - - :warning
      - 'Line 23: Product not found, record ignored., BaseItemCode=200374A'
    - - :warning
      - 'Line 26: Product not found, record ignored., BaseItemCode=200397A'
    - - :warning
      - 'Line 29: Product not found, record ignored., BaseItemCode=200402A'
    - - :warning
      - 'Line 30: Product not found, record ignored., BaseItemCode=200775A'
    - - :warning
      - 'Line 35: Product not found, record ignored., BaseItemCode=200895A'
    - - :warning
      - 'Line 36: Product not found, record ignored., BaseItemCode=200899A'
    - - :warning
      - 'Line 37: Product not found, record ignored., BaseItemCode=200944A'
    - - :warning
      - 'Line 39: Product not found, record ignored., BaseItemCode=201252A'
    - - :warning
      - 'Line 40: Product not found, record ignored., BaseItemCode=201271A'
    - - :warning
      - 'Line 43: Product not found, record ignored., BaseItemCode=201296A'
    - - :warning
      - 'Line 44: Product not found, record ignored., BaseItemCode=201297A'
    - - :warning
      - 'Line 45: Product not found, record ignored., BaseItemCode=201383A'
    - - :warning
      - 'Line 50: Product not found, record ignored., BaseItemCode=201466A'
    - - :warning
      - 'Line 56: Product not found, record ignored., BaseItemCode=201712A'
    - - :warning
      - 'Line 62: Product not found, record ignored., BaseItemCode=201734A'
    - - :warning
      - 'Line 63: Product not found, record ignored., BaseItemCode=201735A'
    - - :warning
      - 'Line 64: Product not found, record ignored., BaseItemCode=201736A'
    - - :warning
      - 'Line 65: Product not found, record ignored., BaseItemCode=201737A'
    - - :warning
      - 'Line 82: Product not found, record ignored., BaseItemCode=202081A'
    - - :warning
      - 'Line 92: Product not found, record ignored., BaseItemCode=202149A'
    - - :warning
      - 'Line 93: Product not found, record ignored., BaseItemCode=202156A'
    - - :warning
      - 'Line 94: Product not found, record ignored., BaseItemCode=202164A'
    - - :warning
      - 'Line 97: Product not found, record ignored., BaseItemCode=202176A'
    - - :warning
      - 'Line 104: Product not found, record ignored., BaseItemCode=202274A'
    - - :warning
      - 'Line 105: Product not found, record ignored., BaseItemCode=202275A'
    - - :warning
      - 'Line 110: Product not found, record ignored., BaseItemCode=202299A'
    - - :warning
      - 'Line 114: Product not found, record ignored., BaseItemCode=202357A'
    - - :warning
      - 'Line 132: Product not found, record ignored., BaseItemCode=202633A'
    - - :warning
      - 'Line 133: Product not found, record ignored., BaseItemCode=202634A'
    - - :warning
      - 'Line 134: Product not found, record ignored., BaseItemCode=202635A'
    - - :warning
      - 'Line 135: Product not found, record ignored., BaseItemCode=202836A'
    - - :warning
      - 'Line 136: Product not found, record ignored., BaseItemCode=202839A'
    - - :warning
      - 'Line 137: Product not found, record ignored., BaseItemCode=202842A'
    - - :warning
      - 'Line 138: Product not found, record ignored., BaseItemCode=202844A'
    - - :warning
      - 'Line 139: Product not found, record ignored., BaseItemCode=202851A'
    - - :warning
      - 'Line 144: Product not found, record ignored., BaseItemCode=202864A'
    - - :warning
      - 'Line 147: Product not found, record ignored., BaseItemCode=202898A'
    - - :warning
      - 'Line 148: Product not found, record ignored., BaseItemCode=202953A'
    - - :warning
      - 'Line 157: Product not found, record ignored., BaseItemCode=203108A'
    - - :warning
      - 'Line 158: Product not found, record ignored., BaseItemCode=203185A'
    - - :warning
      - 'Line 160: Product not found, record ignored., BaseItemCode=203187A'
    - - :warning
      - 'Line 161: Product not found, record ignored., BaseItemCode=203188A'
    - - :warning
      - 'Line 165: Product not found, record ignored., BaseItemCode=203221A'
    - - :warning
      - 'Line 166: Product not found, record ignored., BaseItemCode=203222A'
    - - :warning
      - 'Line 167: Product not found, record ignored., BaseItemCode=203246A'
    - - :warning
      - 'Line 168: Product not found, record ignored., BaseItemCode=203247A'
    - - :warning
      - 'Line 169: Product not found, record ignored., BaseItemCode=203249A'
    - - :warning
      - 'Line 179: Product not found, record ignored., BaseItemCode=203446A'
    - - :warning
      - 'Line 185: Product not found, record ignored., BaseItemCode=203475A'
    - - :warning
      - 'Line 188: Product not found, record ignored., BaseItemCode=203542A'
    - - :warning
      - 'Line 190: Product not found, record ignored., BaseItemCode=203646A'
    - - :warning
      - 'Line 196: Product not found, record ignored., BaseItemCode=203666A'
    - - :warning
      - 'Line 202: Product not found, record ignored., BaseItemCode=203729A'
    - - :warning
      - 'Line 203: Product not found, record ignored., BaseItemCode=203753A'
    - - :warning
      - 'Line 228: Product not found, record ignored., BaseItemCode=203916A'
    - - :warning
      - 'Line 229: Product not found, record ignored., BaseItemCode=203945A'
    - - :warning
      - 'Line 232: Product not found, record ignored., BaseItemCode=203962A'
    - - :warning
      - 'Line 233: Product not found, record ignored., BaseItemCode=203963A'
    - - :warning
      - 'Line 235: Product not found, record ignored., BaseItemCode=203998A'
    - - :warning
      - 'Line 237: Product not found, record ignored., BaseItemCode=204025A'
    - - :warning
      - 'Line 238: Product not found, record ignored., BaseItemCode=204026A'
    - - :warning
      - 'Line 239: Product not found, record ignored., BaseItemCode=204027A'
    - - :warning
      - 'Line 248: Product not found, record ignored., BaseItemCode=204049A'
    - - :warning
      - 'Line 253: Product not found, record ignored., BaseItemCode=204061A'
    - - :warning
      - 'Line 255: Product not found, record ignored., BaseItemCode=204065'
    - - :warning
      - 'Line 256: Product not found, record ignored., BaseItemCode=204069'
    - - :warning
      - 'Line 257: Product not found, record ignored., BaseItemCode=204071'
    - - :warning
      - 'Line 263: Product not found, record ignored., BaseItemCode=204077A'
    - - :warning
      - 'Line 273: Product not found, record ignored., BaseItemCode=204102A'
    - - :warning
      - 'Line 274: Product not found, record ignored., BaseItemCode=204105A'
    - - :warning
      - 'Line 275: Product not found, record ignored., BaseItemCode=204109A'
    - - :warning
      - 'Line 289: Product not found, record ignored., BaseItemCode=204141A'
    - - :warning
      - 'Line 290: Product not found, record ignored., BaseItemCode=204147A'
    - - :warning
      - 'Line 291: Product not found, record ignored., BaseItemCode=204195A'
    - - :warning
      - 'Line 298: Product not found, record ignored., BaseItemCode=204213A'
    - - :warning
      - 'Line 299: Product not found, record ignored., BaseItemCode=204214A'
    - - :warning
      - 'Line 331: Product not found, record ignored., BaseItemCode=204361A'
    - - :warning
      - 'Line 332: Product not found, record ignored., BaseItemCode=204362A'
    - - :warning
      - 'Line 340: Product not found, record ignored., BaseItemCode=204375A'
    - - :warning
      - 'Line 343: Product not found, record ignored., BaseItemCode=204446A'
    - - :warning
      - 'Line 344: Product not found, record ignored., BaseItemCode=204447A'
    - - :warning
      - 'Line 345: Product not found, record ignored., BaseItemCode=204464A'
    - - :warning
      - 'Line 346: Product not found, record ignored., BaseItemCode=204466A'
    - - :warning
      - 'Line 347: Product not found, record ignored., BaseItemCode=204467A'
    - - :warning
      - 'Line 348: Product not found, record ignored., BaseItemCode=204472A'
    - - :warning
      - 'Line 354: Product not found, record ignored., BaseItemCode=204539A'
    - - :warning
      - 'Line 356: Product not found, record ignored., BaseItemCode=204543A'
    - - :warning
      - 'Line 357: Product not found, record ignored., BaseItemCode=204544A'
    - - :warning
      - 'Line 358: Product not found, record ignored., BaseItemCode=204554A'
    - - :warning
      - 'Line 359: Product not found, record ignored., BaseItemCode=204555A'
    - - :warning
      - 'Line 361: Product not found, record ignored., BaseItemCode=204569A'
    - - :warning
      - 'Line 362: Product not found, record ignored., BaseItemCode=204586A'
    - - :warning
      - 'Line 363: Product not found, record ignored., BaseItemCode=204587A'
    - - :warning
      - 'Line 364: Product not found, record ignored., BaseItemCode=204589A'
    - - :warning
      - 'Line 365: Product not found, record ignored., BaseItemCode=204595A'
    - - :warning
      - 'Line 376: Product not found, record ignored., BaseItemCode=204642A'
    - - :warning
      - 'Line 380: Product not found, record ignored., BaseItemCode=204701A'
    - - :warning
      - 'Line 381: Product not found, record ignored., BaseItemCode=204702A'
    - - :warning
      - 'Line 384: Product not found, record ignored., BaseItemCode=204708A'
    - - :warning
      - 'Line 407: Product not found, record ignored., BaseItemCode=204895A'
    - - :warning
      - 'Line 413: Product not found, record ignored., BaseItemCode=204923A'
    - - :warning
      - 'Line 414: Product not found, record ignored., BaseItemCode=204924A'
    - - :warning
      - 'Line 424: Product not found, record ignored., BaseItemCode=205072A'
    - - :warning
      - 'Line 459: Product not found, record ignored., BaseItemCode=205327A'
    - - :warning
      - 'Line 460: Product not found, record ignored., BaseItemCode=205331A'
    - - :warning
      - 'Line 462: Product not found, record ignored., BaseItemCode=205351A'
    - - :warning
      - 'Line 463: Product not found, record ignored., BaseItemCode=205363A'
    - - :warning
      - 'Line 473: Product not found, record ignored., BaseItemCode=205588A'
    - - :warning
      - 'Line 477: Product not found, record ignored., BaseItemCode=205618A'
    - - :warning
      - 'Line 478: Product not found, record ignored., BaseItemCode=205621A'
    - - :warning
      - 'Line 486: Product not found, record ignored., BaseItemCode=205643A'
    - - :warning
      - 'Line 489: Product not found, record ignored., BaseItemCode=205655A'
    - - :warning
      - 'Line 502: Product not found, record ignored., BaseItemCode=205755A'
    - - :warning
      - 'Line 509: Product not found, record ignored., BaseItemCode=205766A'
    - - :warning
      - 'Line 526: Product not found, record ignored., BaseItemCode=205841A'
    - - :warning
      - 'Line 527: Product not found, record ignored., BaseItemCode=205842A'
    - - :warning
      - 'Line 528: Product not found, record ignored., BaseItemCode=205843A'
    - - :warning
      - 'Line 529: Product not found, record ignored., BaseItemCode=205844A'
    - - :warning
      - 'Line 561: Product not found, record ignored., BaseItemCode=206032A'
    - - :warning
      - 'Line 582: Product not found, record ignored., BaseItemCode=206089A'
    - - :warning
      - 'Line 1130: Product not found, record ignored., BaseItemCode=235003-4401A'
    - - :warning
      - 'Line 1131: Product not found, record ignored., BaseItemCode=235003-5201A'
    - - :warning
      - 'Line 1132: Product not found, record ignored., BaseItemCode=235003-5202A'
    - - :warning
      - 'Line 1133: Product not found, record ignored., BaseItemCode=235003-5218A'
    - - :warning
      - 'Line 1134: Product not found, record ignored., BaseItemCode=235003-5223A'
    - - :warning
      - 'Line 1135: Product not found, record ignored., BaseItemCode=235100-5201A'
    - - :warning
      - 'Line 1136: Product not found, record ignored., BaseItemCode=235100-5202A'
    - - :warning
      - 'Line 1137: Product not found, record ignored., BaseItemCode=235112-5201A'
    - - :warning
      - 'Line 1138: Product not found, record ignored., BaseItemCode=235112-5202A'
    - - :warning
      - 'Line 1139: Product not found, record ignored., BaseItemCode=235112-5216A'
    - - :warning
      - 'Line 1140: Product not found, record ignored., BaseItemCode=235112-5225A'
    - - :warning
      - 'Line 1141: Product not found, record ignored., BaseItemCode=235112-6001A'
    - - :warning
      - 'Line 1142: Product not found, record ignored., BaseItemCode=235112-6002A'
    - - :warning
      - 'Line 1143: Product not found, record ignored., BaseItemCode=235112-6016A'
    - - :warning
      - 'Line 1144: Product not found, record ignored., BaseItemCode=235112-6025A'
    - - :warning
      - 'Line 1145: Product not found, record ignored., BaseItemCode=235848-6602A'
    - - :warning
      - 'Line 1146: Product not found, record ignored., BaseItemCode=235848-8402A'
    - - :warning
      - 'Line 1147: Product not found, record ignored., BaseItemCode=235997-1201A'
    - - :warning
      - 'Line 1148: Product not found, record ignored., BaseItemCode=235997-1202A'
    - - :warning
      - 'Line 1149: Product not found, record ignored., BaseItemCode=235997-2401A'
    - - :warning
      - 'Line 1150: Product not found, record ignored., BaseItemCode=235997-2402A'
    - - :warning
      - 'Line 1151: Product not found, record ignored., BaseItemCode=235997-3601A'
    - - :warning
      - 'Line 1152: Product not found, record ignored., BaseItemCode=235997-3602A'
    - - :warning
      - 'Line 1155: Product not found, record ignored., BaseItemCode=31372A'
    - - :warning
      - 'Line 1169: Product not found, record ignored., BaseItemCode=390024A'
    - - :warning
      - 'Line 1194: Product not found, record ignored., BaseItemCode=390249A'
    - - :warning
      - 'Line 1246: Product not found, record ignored., BaseItemCode=39249A'
    - - :warning
      - 'Line 1254: Product not found, record ignored., BaseItemCode=39499A'
    - - :warning
      - 'Line 1256: Product not found, record ignored., BaseItemCode=39591A'
    - - :warning
      - 'Line 1261: Product not found, record ignored., BaseItemCode=39614A'
    - - :warning
      - 'Line 1262: Product not found, record ignored., BaseItemCode=39615A'
    - - :warning
      - 'Line 1263: Product not found, record ignored., BaseItemCode=39628A'
    - - :warning
      - 'Line 1316: Product not found, record ignored., BaseItemCode=43197A'
    - - :warning
      - 'Line 1320: Product not found, record ignored., BaseItemCode=43256A'
    - - :warning
      - 'Line 1323: Product not found, record ignored., BaseItemCode=43311A'
    - - :warning
      - 'Line 1339: Product not found, record ignored., BaseItemCode=43617A'
    - - :warning
      - 'Line 1343: Product not found, record ignored., BaseItemCode=43645A'
    - - :warning
      - 'Line 1349: Product not found, record ignored., BaseItemCode=43682A'
    - - :warning
      - 'Line 1360: Product not found, record ignored., BaseItemCode=43873A'
    - - :warning
      - 'Line 1386: Product not found, record ignored., BaseItemCode=49619A'
    - - :warning
      - 'Line 1417: Product not found, record ignored., BaseItemCode=83241A'
    - - :warning
      - 'Line 1420: Product not found, record ignored., BaseItemCode=83733A'
    - - :warning
      - 'Line 1441: Product not found, record ignored., BaseItemCode=86391A'
    - - :warning
      - 'Line 1451: Product not found, record ignored., BaseItemCode=88968A'
    - - :warning
      - 'Line 1461: Product not found, record ignored., BaseItemCode=900375A'
    - - :warning
      - 'Line 1506: Product not found, record ignored., BaseItemCode=91046A'
    - - :warning
      - 'Line 1507: Product not found, record ignored., BaseItemCode=91416A'
    - - :warning
      - 'Line 1509: Product not found, record ignored., BaseItemCode=91732A'
    - - :warning
      - 'Line 1510: Product not found, record ignored., BaseItemCode=91733A'
    - - :warning
      - 'Line 1511: Product not found, record ignored., BaseItemCode=91988A'
    - - :warning
      - 'Line 1534: Product not found, record ignored., BaseItemCode=93374A'
    - - :warning
      - 'Line 1544: Product not found, record ignored., BaseItemCode=94304A'
    - - :warning
      - 'Line 1546: Product not found, record ignored., BaseItemCode=94353A'
    - - :warning
      - 'Line 1550: Product not found, record ignored., BaseItemCode=94465A'
    - - :warning
      - 'Line 1562: Product not found, record ignored., BaseItemCode=95122A'
    - - :warning
      - 'Line 1565: Product not found, record ignored., BaseItemCode=95143A'
    - - :warning
      - 'Line 1576: Product not found, record ignored., BaseItemCode=95996A'
    - - :warning
      - 'Line 1582: Product not found, record ignored., BaseItemCode=96605A'
    - - :warning
      - 'Line 1583: Product not found, record ignored., BaseItemCode=96606A'
    - - :warning
      - 'Line 1584: Product not found, record ignored., BaseItemCode=96607A'
    - - :warning
      - 'Line 1585: Product not found, record ignored., BaseItemCode=96608A'
    - - :warning
      - 'Line 1587: Product not found, record ignored., BaseItemCode=96726A'
    - - :warning
      - 'Line 1589: Product not found, record ignored., BaseItemCode=96801A'
    - - :warning
      - 'Line 1591: Product not found, record ignored., BaseItemCode=96932A'
    - - :warning
      - 'Line 1596: Product not found, record ignored., BaseItemCode=97374A'
    - - :warning
      - 'Line 1598: Product not found, record ignored., BaseItemCode=97395A'
    - - :warning
      - 'Line 1599: Product not found, record ignored., BaseItemCode=97396A'
    - - :warning
      - 'Line 1600: Product not found, record ignored., BaseItemCode=97397A'
    - - :warning
      - 'Line 1601: Product not found, record ignored., BaseItemCode=97441A'
    - - :warning
      - 'Line 1602: Product not found, record ignored., BaseItemCode=97442A'
    - - :warning
      - 'Line 1619: Product not found, record ignored., BaseItemCode=97914A'
    - - :warning
      - 'Line 1621: Product not found, record ignored., BaseItemCode=97949A'
    - - :warning
      - 'Line 1637: Product not found, record ignored., BaseItemCode=98441A'
    - - :warning
      - 'Line 1642: Product not found, record ignored., BaseItemCode=98735A'
    - - :warning
      - 'Line 1666: Product not found, record ignored., BaseItemCode=99364A'
    - - :warning
      - 'Line 1676: Product not found, record ignored., BaseItemCode=99561A'
    - - :warning
      - 'Line 1677: Product not found, record ignored., BaseItemCode=99562A'
 |

### Q-10_results.md

# Q-10 Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-10 — Feature Enablement Gap Analysis
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-11_results.md

# Q-11 Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-11 — Configuration Completeness
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 18
- **Run date**: 2026-06-17


| entity_type | last_updated | days_stale | related_record_count |
| --- | --- | --- | --- |
| contract_prices | 2025-08-07 23:13:11 | 313 | 0 |
| kit_items | 2025-08-07 23:13:11 | 313 | 0 |
| matrix_options | 2025-08-07 23:13:11 | 313 | — |
| option_groups | 2025-08-07 23:13:11 | 313 | — |
| options | 2025-08-07 23:13:11 | 313 | — |
| commitment_reports | 2025-08-07 23:13:11 | 313 | — |
| placement_reports | 2025-08-07 23:13:11 | 313 | — |
| riser_prices | 2025-08-07 23:13:11 | 313 | — |
| customer_payment_informations | 2025-08-07 23:13:11 | 313 | — |
| sales_quotas | 2025-08-07 23:13:11 | 313 | 0 |
| portal_orders | 2026-03-13 14:23:42 | 96 | — |
| portal_invoices | 2026-03-13 14:23:42 | 96 | — |
| products | 2026-05-08 18:15:34 | 40 | — |
| smart_stacks | 2026-05-08 18:15:34 | 40 | — |
| categories | 2026-05-08 18:15:35 | 40 | — |
| collections | 2026-05-08 18:15:35 | 40 | — |
| groups | 2026-05-08 18:15:35 | 40 | — |
| trade_names | 2026-05-08 18:15:35 | 40 | — |

### Q-22_results.md

# Q-22 Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-22 — Feature Usage Depth
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | submit_order | select_a_customer | search_for_customer | email_item_info | create_pdf_catalog | view_library_entry | view_smartpicks | access_sales_portal | filter_products | search_products | search_collections | order_configured_item | view_kit | order_kit | share_my_list | export_data_to_csv | export_data_to_excel | total_events | total_users |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| eglo_can | EGLO Canada | 130 | 1,108 | 1,643 | 14 | 172 | 606 | 14 | 0 | 184 | 14,443 | 21 | 0 | 0 | 0 | 11 | 6 | 15 | 28,348 | 26 |

### Q-CI-02_results.md

# Q-CI-02 Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-CI-02 — Peer Comparison
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | peer_standing | orders_vs_peer_pct | logins_vs_peer_pct | mrr_vs_peer_pct | peer_orders_median | peer_logins_median | peer_mrr_median |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| eglo_can | EGLO Canada | Commerce-Active | Below Average | -48.80 | -20.10 | 78 | 254 | 2,833 | 920 |

### Q-CI-03_results.md

# Q-CI-03 Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-CI-03 — Feature Adoption Benchmarking
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | feature_depth | has_clicky_portal | arr |
| --- | --- | --- | --- | --- | --- |
| eglo_can | EGLO Canada | Commerce-Active | 4 | 0 | 9,680 |

### Q-CI-03_benchmarks_results.md

# Q-CI-03-bench Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-CI-03-bench — Segment Benchmarks Monthly
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 3
- **Run date**: 2026-06-17


| segment | benchmark_month | org_count | submit_order_p10 | submit_order_p25 | submit_order_median | submit_order_p75 | submit_order_p90 | total_logins_p25 | total_logins_median | total_logins_p75 | search_products_p25 | search_products_median | search_products_p75 | mrr_p25 | mrr_median | mrr_p75 | arr_p25 | arr_median | arr_p75 | feature_kit_items_pct | feature_portal_orders_pct | feature_sales_portal_pct | feature_library_pct | feature_pdf_catalog_pct | feature_cpq_pct | created_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Commerce-Active | 2026-06-01 | 51 | 85 | 107 | 254 | 352 | 393 | 1,758 | 2,833 | 7,482 | 4,998 | 5,482 | 34,413 | 652.50 | 920 | 1,637.50 | 7,902.50 | 10,240 | 22,228.50 | 0.08 | 0.49 | 0.49 | 1 | 0.96 | 0.14 | 2026-06-01 10:00 |
| Commerce-Active | 2026-05-01 | 52 | 83 | 105 | 254 | 343 | 394 | 1,639 | 2,703 | 5,899 | 4,414 | 5,181 | 29,505 | 652.50 | 920 | 1,637.50 | 7,902.50 | 10,240 | 22,228.50 | 0.08 | 0.50 | 0.50 | 1 | 0.96 | 0.12 | 2026-05-01 10:00 |
| Commerce-Active | 2026-04-01 | 52 | 74 | 103 | 245 | 290 | 369 | 1,476 | 2,578 | 5,605 | 3,455 | 5,017 | 28,432 | 652.50 | 920 | 1,637.50 | 7,902.50 | 10,240 | 22,228.50 | 0.08 | 0.50 | 0.50 | 1 | 0.94 | 0.12 | 2026-04-01 10:00 |

### Q-CI-05_results.md

(not present — file does not exist or is empty)

### peer_benchmark_extract.md

(not present — file does not exist or is empty)
