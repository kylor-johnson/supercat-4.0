# Section 6 Context Bundle — Schonbek Lighting (sbl)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Schonbek Lighting (sbl, org_id=182)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | False | portal_order_count=0, portal_order_gmv=$0 |
| HAS_INVENTORY | True | inventory_count=1886 |
| HAS_SALES_DATA | True | sales_data_count=7287 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=1 engagement_reps=69 (threshold: >=5) |
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
| ENGAGEMENT_REP_COUNT | 69 | engagement_reps=69 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 118 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 139, Mixpanel total submit_order (Q-01): 257 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=95.8%, ambiguous_rate=93.8%, showroom_event_share=2.4% |
| USER_GROUP_JOIN_RATE | 96% | 113 of 118 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 2% | showroom+admin share of matched events: 2.4% |
| ADMIN_REPS_IN_LEADERBOARD | False | 0 admin/showroom users in leaderboard |

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
| HAS_NEW_ITEMS | True | new_item_count=340 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | PARTIAL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | PARTIAL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Schonbek Lighting
- **Shortname**: sbl
- **Org ID**: 182
- **Bundle**: 4
- **Bundle label for report**: 4

## Validation Log

- portal_orders LTM count=0, gmv=0.0 — HAS_PORTAL_ORDERS overridden to false

## Section Confidence

# Section Confidence Tiers — Schonbek Lighting (sbl, org_id=182)
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

# Signal Rank — Schonbek Lighting (sbl, org_id=182)
- **Run date**: 2026-06-17
- **Total signals fired**: 15 (P0: 0, P1: 11, P2: 4)
- **Org GMV**: $0.0M eCat LTM, $0.0M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 56% of eCat GMV | P1 | §4 Commerce | 1.4 | $508,803 | 2.0 | 1,435,222 | RISK |
| 2 | SIG-OPP-04 | New Item Adoption Gap — 30 new items with $0 platform orders | P2 | §3 Product | 3.0 | $50,000 | 1.0 | 150,000 | POSITIVE |
| 3 | SIG-RISK-03 | Data Staleness — contract_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 4 | SIG-RISK-03 | Data Staleness — kit_items last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 5 | SIG-RISK-03 | Data Staleness — matrix_options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 6 | SIG-RISK-03 | Data Staleness — option_groups last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 7 | SIG-RISK-03 | Data Staleness — options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 8 | SIG-RISK-03 | Data Staleness — commitment_reports last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 9 | SIG-RISK-03 | Data Staleness — placement_reports last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 10 | SIG-RISK-03 | Data Staleness — riser_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 11 | SIG-RISK-03 | Data Staleness — customer_payment_informations last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 12 | SIG-RISK-03 | Data Staleness — sales_quotas last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 13 | SIG-RISK-03 | Data Staleness — price_levels last updated 145d ago | P2 | §6 Platform | 1.6 | $1 | 2.0 | 3 | RISK |
| 14 | SIG-RISK-03 | Data Staleness — portal_orders last updated 96d ago | P2 | §6 Platform | 1.1 | $1 | 2.0 | 2 | RISK |
| 15 | SIG-RISK-03 | Data Staleness — portal_invoices last updated 96d ago | P2 | §6 Platform | 1.1 | $1 | 2.0 | 2 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §3 Product Intelligence | 0 | 0 | 1 | 1 | |
| §4 Commerce Patterns | 0 | 1 | 0 | 1 | |
| §6 Platform Context | 0 | 10 | 3 | 13 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-04: New Item Adoption Gap — 30 new items with $0 platform orders
2. **[RISK]** SIG-RISK-01: Revenue Concentration — top 5 accounts generate 56% of eCat GMV
3. **[RISK]** SIG-RISK-03: Data Staleness — contract_prices last updated 313d ago
4. **[RISK]** SIG-RISK-03: Data Staleness — kit_items last updated 313d ago
5. **[RISK]** SIG-RISK-03: Data Staleness — matrix_options last updated 313d ago
6. **[RISK]** SIG-RISK-03: Data Staleness — option_groups last updated 313d ago
7. **[RISK]** SIG-RISK-03: Data Staleness — options last updated 313d ago

**Balance check**: 1 positive (slots 1-1), 6 risk (slots 2-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-08_results.md

# Q-08 Results — Schonbek Lighting (sbl, org_id=182)
- **Query**: Q-08 — Data Freshness Monitor
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 22
- **Run date**: 2026-06-17


| entity_type | last_updated | days_since_update | status |
| --- | --- | --- | --- |
| contract_prices | 2025-08-07 23:13:10 | 313 | Stale |
| kit_items | 2025-08-07 23:13:10 | 313 | Stale |
| matrix_options | 2025-08-07 23:13:10 | 313 | Stale |
| option_groups | 2025-08-07 23:13:10 | 313 | Stale |
| options | 2025-08-07 23:13:10 | 313 | Stale |
| commitment_reports | 2025-08-07 23:13:10 | 313 | Stale |
| placement_reports | 2025-08-07 23:13:10 | 313 | Stale |
| riser_prices | 2025-08-07 23:13:10 | 313 | Stale |
| customer_payment_informations | 2025-08-07 23:13:10 | 313 | Stale |
| sales_quotas | 2025-08-07 23:13:10 | 313 | Stale |
| price_levels | 2026-01-23 17:59:47 | 145 | Monitor |
| portal_orders | 2026-03-13 14:23:41 | 96 | Monitor |
| portal_invoices | 2026-03-13 14:23:41 | 96 | Monitor |
| products | 2026-04-21 13:08:15 | 57 | Monitor |
| smart_stacks | 2026-04-21 13:08:15 | 57 | Monitor |
| categories | 2026-04-21 13:08:16 | 57 | Monitor |
| collections | 2026-04-21 13:08:16 | 57 | Monitor |
| groups | 2026-04-21 13:08:16 | 57 | Monitor |
| trade_names | 2026-04-21 13:08:16 | 57 | Monitor |
| inventories | 2026-06-17 05:47:16 | 0 | Fresh |
| customers | 2026-06-17 05:47:37 | 0 | Fresh |
| customer_favorites | 2026-06-17 05:47:38 | 0 | Fresh |

### Q-09_results.md

# Q-09 Results — Schonbek Lighting (sbl, org_id=182)
- **Query**: Q-09 — Import Health — Monthly Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 7
- **Run date**: 2026-06-17


| month | import_count |
| --- | --- |
| 2026-06-01 | 18 |
| 2026-05-01 | 33 |
| 2026-04-01 | 45 |
| 2026-03-01 | 38 |
| 2026-02-01 | 30 |
| 2026-01-01 | 91 |
| 2025-12-01 | 42 |

### Q-09_recent_results.md

# Q-09-recent Results — Schonbek Lighting (sbl, org_id=182)
- **Query**: Q-09-recent — Import Health — Recent Errors
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| created_at | data |
| --- | --- |
| 2026-06-17T05:47:38.999411 | ---
- - Inventory
  - - - :warning
      - 'Line 5: Product not found, record ignored., BaseItemCode=1239-22A'
    - - :warning
      - 'Line 8: Product not found, record ignored., BaseItemCode=1239-23A'
    - - :warning
      - 'Line 13: Product not found, record ignored., BaseItemCode=1239-40A'
    - - :warning
      - 'Line 16: Product not found, record ignored., BaseItemCode=1239-48A'
    - - :warning
      - 'Line 19: Product not found, record ignored., BaseItemCode=1239-76A'
    - - :warning
      - 'Line 25: Product not found, record ignored., BaseItemCode=1241-48S'
    - - :warning
      - 'Line 30: Product not found, record ignored., BaseItemCode=1243-22A'
    - - :warning
      - 'Line 31: Product not found, record ignored., BaseItemCode=1243-23S'
    - - :warning
      - 'Line 40: Product not found, record ignored., BaseItemCode=1558-48R'
    - - :warning
      - 'Line 69: Product not found, record ignored., BaseItemCode=1701U-76'
    - - :warning
      - 'Line 78: Product not found, record ignored., BaseItemCode=1702U-76'
    - - :warning
      - 'Line 87: Product not found, record ignored., BaseItemCode=1703U-76'
    - - :warning
      - 'Line 102: Product not found, record ignored., BaseItemCode=1716U-76'
    - - :warning
      - 'Line 110: Product not found, record ignored., BaseItemCode=1718U-76'
    - - :warning
      - 'Line 111: Product not found, record ignored., BaseItemCode=2124A'
    - - :warning
      - 'Line 112: Product not found, record ignored., BaseItemCode=2220A'
    - - :warning
      - 'Line 115: Product not found, record ignored., BaseItemCode=2224A'
    - - :warning
      - 'Line 406: Product not found, record ignored., BaseItemCode=5075-48S'
    - - :warning
      - 'Line 520: Product not found, record ignored., BaseItemCode=5685-80R'
    - - :warning
      - 'Line 600: Product not found, record ignored., BaseItemCode=6816-40A'
    - - :warning
      - 'Line 1100: Product not found, record ignored., BaseItemCode=CM8519N-401A'
    - - :warning
      - 'Line 1647: Product not found, record ignored., BaseItemCode=SF-RCBT-WT'
    - - :warning
      - 'Line 1648: Product not found, record ignored., BaseItemCode=SF-WCBT-WT'
    - - :warning
      - 'Line 1649: Product not found, record ignored., BaseItemCode=SFCK-26'
    - - :warning
      - 'Line 1650: Product not found, record ignored., BaseItemCode=SFCK-51'
    - - :warning
      - 'Line 1651: Product not found, record ignored., BaseItemCode=SFDR-12-26'
    - - :warning
      - 'Line 1652: Product not found, record ignored., BaseItemCode=SFDR-12-51'
    - - :warning
      - 'Line 1653: Product not found, record ignored., BaseItemCode=SFDR-18-26'
    - - :warning
      - 'Line 1654: Product not found, record ignored., BaseItemCode=SFDR-18-51'
    - - :warning
      - 'Line 1655: Product not found, record ignored., BaseItemCode=SFDR-24-26'
    - - :warning
      - 'Line 1656: Product not found, record ignored., BaseItemCode=SFDR-24-51'
    - - :warning
      - 'Line 1657: Product not found, record ignored., BaseItemCode=SFDR-48-26'
    - - :warning
      - 'Line 1658: Product not found, record ignored., BaseItemCode=SFDR-48-51'
    - - :warning
      - 'Line 1659: Product not found, record ignored., BaseItemCode=SFDR-I-26'
    - - :warning
      - 'Line 1660: Product not found, record ignored., BaseItemCode=SFDR-I-51'
    - - :warning
      - 'Line 1666: Product not found, record ignored., BaseItemCode=SJ1012T24-RBL702R'
    - - :warning
      - 'Line 1667: Product not found, record ignored., BaseItemCode=SJ1012T24-RGO702R'
    - - :warning
      - 'Line 1668: Product not found, record ignored., BaseItemCode=SJ1012T24-RRE702R'
    - - :warning
      - 'Line 1683: Product not found, record ignored., BaseItemCode=SJ2310T24-RBL702R'
    - - :warning
      - 'Line 1684: Product not found, record ignored., BaseItemCode=SJ2310T24-RGO702R'
    - - :warning
      - 'Line 1685: Product not found, record ignored., BaseItemCode=SJ2310T24-RRE702R'
    - - :warning
      - 'Line 1700: Product not found, record ignored., BaseItemCode=SJ3611T24-RBL702R'
    - - :warning
      - 'Line 1701: Product not found, record ignored., BaseItemCode=SJ3611T24-RGO702R'
    - - :warning
      - 'Line 1702: Product not found, record ignored., BaseItemCode=SJ3611T24-RRE702R'
    - - :warning
      - 'Line 1733: Product not found, record ignored., BaseItemCode=SJ4914T24-RBL702R'
    - - :warning
      - 'Line 1734: Product not found, record ignored., BaseItemCode=SJ4914T24-RGO702R'
    - - :warning
      - 'Line 1735: Product not found, record ignored., BaseItemCode=SJ4914T24-RRE702R'
    - - :warning
      - 'Line 1817: Product not found, record ignored., BaseItemCode=SJ8813T24-RBL702R'
    - - :warning
      - 'Line 1818: Product not found, record ignored., BaseItemCode=SJ8813T24-RGO702R'
    - - :warning
      - 'Line 1819: Product not found, record ignored., BaseItemCode=SJ8813T24-RRE702R'
    - - :warning
      - 'Line 1887: Product not found, record ignored., BaseItemCode=WH-WS-WT'
- - Customers
  - - - :error
      - 'Line 1359: error=Validation failed: Shipping state can''t be blank: Customer
        # = 13172787'
- - Sales Data
  - - - :error
      - 'Line 45: Base item code SFCK-26 does not match an active product'
    - - :error
      - 'Line 46: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 108: Base item code 5685-80R does not match an active product'
    - - :error
      - 'Line 250: Base item code 1712U-76 does not match an active product'
    - - :error
      - 'Line 353: BillToCode (03983000) is invalid.'
    - - :error
      - 'Line 372: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 386: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 387: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 388: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 823: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 824: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 825: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 826: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 827: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 828: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 829: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 830: BillToCode (09371000) is invalid.'
    - - :error
      - 'Line 894: Base item code SF-RCBT-WT does not match an active product'
    - - :error
      - 'Line 895: Base item code SF-WCBT-WT does not match an active product'
    - - :error
      - 'Line 937: Base item code 1239-40A does not match an active product'
    - - :error
      - 'Line 986: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 1208: Base item code 1238N-48A does not match an active product'
    - - :error
      - 'Line 1209: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1415: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1419: Base item code 1248-22A does not match an active product'
    - - :error
      - 'Line 1452: Base item code 2124A does not match an active product'
    - - :error
      - 'Line 1454: Base item code 2995-40A does not match an active product'
    - - :error
      - 'Line 1455: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 1457: Base item code 3601-40A does not match an active product'
    - - :error
      - 'Line 1631: Base item code 1246-22A does not match an active product'
    - - :error
      - 'Line 1796: Base item code 1238N-22A does not match an active product'
    - - :error
      - 'Line 1801: Base item code 1239-76A does not match an active product'
    - - :error
      - 'Line 1805: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1807: Base item code 1241-22A does not match an active product'
    - - :error
      - 'Line 1810: Base item code 1241-48S does not match an active product'
    - - :error
      - 'Line 1818: Base item code 1243-22A does not match an active product'
    - - :error
      - 'Line 1820: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1908: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 2054: Base item code CM8519N-401A does not match an active product'
    - - :error
      - 'Line 2253: Base item code SFDR-18-26 does not match an active product'
    - - :error
      - 'Line 2254: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 2266: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2328: BillToCode (13171071) is invalid.'
    - - :error
      - 'Line 2500: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2501: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2579: BillToCode (13171471) is invalid.'
    - - :error
      - 'Line 2731: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2732: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2761: Base item code CM8326N-401A does not match an active product'
    - - :error
      - 'Line 2877: BillToCode (13172412) is invalid.'
    - - :warning
      - "-213 more rows with invalid products"
 |
| 2026-06-16T05:46:29.377341 | ---
- - Inventory
  - - - :warning
      - 'Line 2: Product not found, record ignored., BaseItemCode=1239-22A'
    - - :warning
      - 'Line 3: Product not found, record ignored., BaseItemCode=1239-23A'
    - - :warning
      - 'Line 5: Product not found, record ignored., BaseItemCode=1239-40A'
    - - :warning
      - 'Line 7: Product not found, record ignored., BaseItemCode=1239-48A'
    - - :warning
      - 'Line 9: Product not found, record ignored., BaseItemCode=1239-76A'
    - - :warning
      - 'Line 11: Product not found, record ignored., BaseItemCode=1240-22A'
    - - :warning
      - 'Line 13: Product not found, record ignored., BaseItemCode=1240-23A'
    - - :warning
      - 'Line 14: Product not found, record ignored., BaseItemCode=1240-40A'
    - - :warning
      - 'Line 15: Product not found, record ignored., BaseItemCode=1240-48A'
    - - :warning
      - 'Line 16: Product not found, record ignored., BaseItemCode=1240-76A'
    - - :warning
      - 'Line 18: Product not found, record ignored., BaseItemCode=1241-22A'
    - - :warning
      - 'Line 20: Product not found, record ignored., BaseItemCode=1241-23A'
    - - :warning
      - 'Line 21: Product not found, record ignored., BaseItemCode=1241-40A'
    - - :warning
      - 'Line 22: Product not found, record ignored., BaseItemCode=1241-48A'
    - - :warning
      - 'Line 23: Product not found, record ignored., BaseItemCode=1241-48S'
    - - :warning
      - 'Line 24: Product not found, record ignored., BaseItemCode=1241-76A'
    - - :warning
      - 'Line 29: Product not found, record ignored., BaseItemCode=1243-22A'
    - - :warning
      - 'Line 30: Product not found, record ignored., BaseItemCode=1243-23A'
    - - :warning
      - 'Line 31: Product not found, record ignored., BaseItemCode=1243-23S'
    - - :warning
      - 'Line 32: Product not found, record ignored., BaseItemCode=1243-40A'
    - - :warning
      - 'Line 34: Product not found, record ignored., BaseItemCode=1243-48A'
    - - :warning
      - 'Line 35: Product not found, record ignored., BaseItemCode=1243-76A'
    - - :warning
      - 'Line 49: Product not found, record ignored., BaseItemCode=2124A'
    - - :warning
      - 'Line 50: Product not found, record ignored., BaseItemCode=2220A'
    - - :warning
      - 'Line 51: Product not found, record ignored., BaseItemCode=2224A'
    - - :warning
      - 'Line 52: Product not found, record ignored., BaseItemCode=2274A'
    - - :warning
      - 'Line 56: Product not found, record ignored., BaseItemCode=2990-40A'
    - - :warning
      - 'Line 57: Product not found, record ignored., BaseItemCode=2991-40A'
    - - :warning
      - 'Line 59: Product not found, record ignored., BaseItemCode=2994-40A'
    - - :warning
      - 'Line 61: Product not found, record ignored., BaseItemCode=2999-40A'
    - - :warning
      - 'Line 91: Product not found, record ignored., BaseItemCode=5075-48S'
    - - :warning
      - 'Line 108: Product not found, record ignored., BaseItemCode=6816-40A'
    - - :warning
      - 'Line 389: Product not found, record ignored., BaseItemCode=CM8326N-401A'
    - - :warning
      - 'Line 390: Product not found, record ignored., BaseItemCode=CM8334N-401A'
    - - :warning
      - 'Line 391: Product not found, record ignored., BaseItemCode=CM8519N-401A'
    - - :warning
      - 'Line 653: Product not found, record ignored., BaseItemCode=SF-RCBT-WT'
    - - :warning
      - 'Line 654: Product not found, record ignored., BaseItemCode=SF-WCBT-WT'
    - - :warning
      - 'Line 655: Product not found, record ignored., BaseItemCode=SFCK-26'
    - - :warning
      - 'Line 656: Product not found, record ignored., BaseItemCode=SFCK-51'
    - - :warning
      - 'Line 657: Product not found, record ignored., BaseItemCode=SFDR-12-26'
    - - :warning
      - 'Line 658: Product not found, record ignored., BaseItemCode=SFDR-12-51'
    - - :warning
      - 'Line 659: Product not found, record ignored., BaseItemCode=SFDR-18-26'
    - - :warning
      - 'Line 660: Product not found, record ignored., BaseItemCode=SFDR-18-51'
    - - :warning
      - 'Line 661: Product not found, record ignored., BaseItemCode=SFDR-24-26'
    - - :warning
      - 'Line 662: Product not found, record ignored., BaseItemCode=SFDR-24-51'
    - - :warning
      - 'Line 663: Product not found, record ignored., BaseItemCode=SFDR-48-26'
    - - :warning
      - 'Line 664: Product not found, record ignored., BaseItemCode=SFDR-48-51'
    - - :warning
      - 'Line 665: Product not found, record ignored., BaseItemCode=SFDR-I-26'
    - - :warning
      - 'Line 666: Product not found, record ignored., BaseItemCode=SFDR-I-51'
    - - :warning
      - 'Line 714: Product not found, record ignored., BaseItemCode=WH-WS-WT'
- - Customers
  - - - :error
      - 'Line 1359: error=Validation failed: Shipping state can''t be blank: Customer
        # = 13172787'
- - Sales Data
  - - - :error
      - 'Line 45: Base item code SFCK-26 does not match an active product'
    - - :error
      - 'Line 46: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 108: Base item code 5685-80R does not match an active product'
    - - :error
      - 'Line 248: Base item code 1712U-76 does not match an active product'
    - - :error
      - 'Line 351: BillToCode (03983000) is invalid.'
    - - :error
      - 'Line 370: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 384: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 385: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 386: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 826: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 827: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 828: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 829: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 830: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 831: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 832: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 833: BillToCode (09371000) is invalid.'
    - - :error
      - 'Line 897: Base item code SF-RCBT-WT does not match an active product'
    - - :error
      - 'Line 898: Base item code SF-WCBT-WT does not match an active product'
    - - :error
      - 'Line 941: Base item code 1239-40A does not match an active product'
    - - :error
      - 'Line 990: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 1215: Base item code 1238N-48A does not match an active product'
    - - :error
      - 'Line 1216: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1423: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1427: Base item code 1248-22A does not match an active product'
    - - :error
      - 'Line 1460: Base item code 2124A does not match an active product'
    - - :error
      - 'Line 1462: Base item code 2995-40A does not match an active product'
    - - :error
      - 'Line 1463: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 1465: Base item code 3601-40A does not match an active product'
    - - :error
      - 'Line 1639: Base item code 1246-22A does not match an active product'
    - - :error
      - 'Line 1804: Base item code 1238N-22A does not match an active product'
    - - :error
      - 'Line 1809: Base item code 1239-76A does not match an active product'
    - - :error
      - 'Line 1813: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1815: Base item code 1241-22A does not match an active product'
    - - :error
      - 'Line 1818: Base item code 1241-48S does not match an active product'
    - - :error
      - 'Line 1826: Base item code 1243-22A does not match an active product'
    - - :error
      - 'Line 1828: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1916: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 2061: Base item code CM8519N-401A does not match an active product'
    - - :error
      - 'Line 2260: Base item code SFDR-18-26 does not match an active product'
    - - :error
      - 'Line 2261: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 2273: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2274: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2336: BillToCode (13171071) is invalid.'
    - - :error
      - 'Line 2509: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2510: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2588: BillToCode (13171471) is invalid.'
    - - :error
      - 'Line 2740: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2741: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2770: Base item code CM8326N-401A does not match an active product'
    - - :warning
      - "-214 more rows with invalid products"
 |
| 2026-06-15T05:46:38.788436 | ---
- - Inventory
  - - - :warning
      - 'Line 5: Product not found, record ignored., BaseItemCode=1239-22A'
    - - :warning
      - 'Line 8: Product not found, record ignored., BaseItemCode=1239-23A'
    - - :warning
      - 'Line 13: Product not found, record ignored., BaseItemCode=1239-40A'
    - - :warning
      - 'Line 16: Product not found, record ignored., BaseItemCode=1239-48A'
    - - :warning
      - 'Line 19: Product not found, record ignored., BaseItemCode=1239-76A'
    - - :warning
      - 'Line 24: Product not found, record ignored., BaseItemCode=1240-22A'
    - - :warning
      - 'Line 27: Product not found, record ignored., BaseItemCode=1240-23A'
    - - :warning
      - 'Line 32: Product not found, record ignored., BaseItemCode=1240-40A'
    - - :warning
      - 'Line 35: Product not found, record ignored., BaseItemCode=1240-48A'
    - - :warning
      - 'Line 38: Product not found, record ignored., BaseItemCode=1240-76A'
    - - :warning
      - 'Line 43: Product not found, record ignored., BaseItemCode=1241-22A'
    - - :warning
      - 'Line 46: Product not found, record ignored., BaseItemCode=1241-23A'
    - - :warning
      - 'Line 51: Product not found, record ignored., BaseItemCode=1241-40A'
    - - :warning
      - 'Line 54: Product not found, record ignored., BaseItemCode=1241-48A'
    - - :warning
      - 'Line 56: Product not found, record ignored., BaseItemCode=1241-48S'
    - - :warning
      - 'Line 58: Product not found, record ignored., BaseItemCode=1241-76A'
    - - :warning
      - 'Line 77: Product not found, record ignored., BaseItemCode=1243-22A'
    - - :warning
      - 'Line 80: Product not found, record ignored., BaseItemCode=1243-23A'
    - - :warning
      - 'Line 82: Product not found, record ignored., BaseItemCode=1243-23S'
    - - :warning
      - 'Line 86: Product not found, record ignored., BaseItemCode=1243-40A'
    - - :warning
      - 'Line 89: Product not found, record ignored., BaseItemCode=1243-48A'
    - - :warning
      - 'Line 92: Product not found, record ignored., BaseItemCode=1243-76A'
    - - :warning
      - 'Line 104: Product not found, record ignored., BaseItemCode=1558-48R'
    - - :warning
      - 'Line 133: Product not found, record ignored., BaseItemCode=1701U-76'
    - - :warning
      - 'Line 142: Product not found, record ignored., BaseItemCode=1702U-76'
    - - :warning
      - 'Line 151: Product not found, record ignored., BaseItemCode=1703U-76'
    - - :warning
      - 'Line 160: Product not found, record ignored., BaseItemCode=1704U-76'
    - - :warning
      - 'Line 173: Product not found, record ignored., BaseItemCode=1712-55'
    - - :warning
      - 'Line 174: Product not found, record ignored., BaseItemCode=1712U-76'
    - - :warning
      - 'Line 177: Product not found, record ignored., BaseItemCode=2124A'
    - - :warning
      - 'Line 179: Product not found, record ignored., BaseItemCode=2220A'
    - - :warning
      - 'Line 182: Product not found, record ignored., BaseItemCode=2224A'
    - - :warning
      - 'Line 193: Product not found, record ignored., BaseItemCode=2274A'
    - - :warning
      - 'Line 205: Product not found, record ignored., BaseItemCode=2642L-211O'
    - - :warning
      - 'Line 210: Product not found, record ignored., BaseItemCode=2990-40A'
    - - :warning
      - 'Line 213: Product not found, record ignored., BaseItemCode=2991-40A'
    - - :warning
      - 'Line 218: Product not found, record ignored., BaseItemCode=2994-40A'
    - - :warning
      - 'Line 221: Product not found, record ignored., BaseItemCode=2999-40A'
    - - :warning
      - 'Line 299: Product not found, record ignored., BaseItemCode=3608-40A'
    - - :warning
      - 'Line 560: Product not found, record ignored., BaseItemCode=5075-48S'
    - - :warning
      - 'Line 765: Product not found, record ignored., BaseItemCode=6816-40A'
    - - :warning
      - 'Line 834: Product not found, record ignored., BaseItemCode=AT1001N-23H'
    - - :warning
      - 'Line 1335: Product not found, record ignored., BaseItemCode=CM8326N-401A'
    - - :warning
      - 'Line 1337: Product not found, record ignored., BaseItemCode=CM8334N-401A'
    - - :warning
      - 'Line 1340: Product not found, record ignored., BaseItemCode=CM8519N-401A'
    - - :warning
      - 'Line 1452: Product not found, record ignored., BaseItemCode=MD1005N-51H'
    - - :warning
      - 'Line 1458: Product not found, record ignored., BaseItemCode=MD1006N-44H'
    - - :warning
      - 'Line 1509: Product not found, record ignored., BaseItemCode=RJ1003N-23H'
    - - :warning
      - 'Line 2419: Product not found, record ignored., BaseItemCode=SF-RCBT-WT'
    - - :warning
      - 'Line 2420: Product not found, record ignored., BaseItemCode=SF-WCBT-WT'
    - - :warning
      - 'Line 2421: Product not found, record ignored., BaseItemCode=SFCK-26'
    - - :warning
      - 'Line 2422: Product not found, record ignored., BaseItemCode=SFCK-51'
    - - :warning
      - 'Line 2423: Product not found, record ignored., BaseItemCode=SFDR-12-26'
    - - :warning
      - 'Line 2424: Product not found, record ignored., BaseItemCode=SFDR-12-51'
    - - :warning
      - 'Line 2425: Product not found, record ignored., BaseItemCode=SFDR-18-26'
    - - :warning
      - 'Line 2426: Product not found, record ignored., BaseItemCode=SFDR-18-51'
    - - :warning
      - 'Line 2427: Product not found, record ignored., BaseItemCode=SFDR-24-26'
    - - :warning
      - 'Line 2428: Product not found, record ignored., BaseItemCode=SFDR-24-51'
    - - :warning
      - 'Line 2429: Product not found, record ignored., BaseItemCode=SFDR-48-26'
    - - :warning
      - 'Line 2430: Product not found, record ignored., BaseItemCode=SFDR-48-51'
    - - :warning
      - 'Line 2431: Product not found, record ignored., BaseItemCode=SFDR-I-26'
    - - :warning
      - 'Line 2432: Product not found, record ignored., BaseItemCode=SFDR-I-51'
    - - :warning
      - 'Line 2438: Product not found, record ignored., BaseItemCode=SJ1012T24-RBL702R'
    - - :warning
      - 'Line 2439: Product not found, record ignored., BaseItemCode=SJ1012T24-RGO702R'
    - - :warning
      - 'Line 2440: Product not found, record ignored., BaseItemCode=SJ1012T24-RRE702R'
    - - :warning
      - 'Line 2456: Product not found, record ignored., BaseItemCode=SJ2310T24-RBL702R'
    - - :warning
      - 'Line 2457: Product not found, record ignored., BaseItemCode=SJ2310T24-RGO702R'
    - - :warning
      - 'Line 2458: Product not found, record ignored., BaseItemCode=SJ2310T24-RRE702R'
    - - :warning
      - 'Line 2473: Product not found, record ignored., BaseItemCode=SJ3611T24-RBL702R'
    - - :warning
      - 'Line 2474: Product not found, record ignored., BaseItemCode=SJ3611T24-RGO702R'
    - - :warning
      - 'Line 2475: Product not found, record ignored., BaseItemCode=SJ3611T24-RRE702R'
    - - :warning
      - 'Line 2506: Product not found, record ignored., BaseItemCode=SJ4914T24-RBL702R'
    - - :warning
      - 'Line 2507: Product not found, record ignored., BaseItemCode=SJ4914T24-RGO702R'
    - - :warning
      - 'Line 2508: Product not found, record ignored., BaseItemCode=SJ4914T24-RRE702R'
    - - :warning
      - 'Line 2594: Product not found, record ignored., BaseItemCode=SJ8813T24-RBL702R'
    - - :warning
      - 'Line 2595: Product not found, record ignored., BaseItemCode=SJ8813T24-RGO702R'
    - - :warning
      - 'Line 2596: Product not found, record ignored., BaseItemCode=SJ8813T24-RRE702R'
    - - :warning
      - 'Line 2783: Product not found, record ignored., BaseItemCode=WH-WS-WT'
- - Customers
  - - - :error
      - 'Line 1359: error=Validation failed: Shipping state can''t be blank: Customer
        # = 13172787'
- - Sales Data
  - - - :error
      - 'Line 44: Base item code SFCK-26 does not match an active product'
    - - :error
      - 'Line 45: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 107: Base item code 5685-80R does not match an active product'
    - - :error
      - 'Line 247: Base item code 1712U-76 does not match an active product'
    - - :error
      - 'Line 350: BillToCode (03983000) is invalid.'
    - - :error
      - 'Line 369: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 383: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 384: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 385: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 823: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 824: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 825: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 826: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 827: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 828: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 829: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 830: BillToCode (09371000) is invalid.'
    - - :error
      - 'Line 894: Base item code SF-RCBT-WT does not match an active product'
    - - :error
      - 'Line 895: Base item code SF-WCBT-WT does not match an active product'
    - - :error
      - 'Line 938: Base item code 1239-40A does not match an active product'
    - - :error
      - 'Line 987: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 1212: Base item code 1238N-48A does not match an active product'
    - - :error
      - 'Line 1213: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1420: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1424: Base item code 1248-22A does not match an active product'
    - - :error
      - 'Line 1457: Base item code 2124A does not match an active product'
    - - :error
      - 'Line 1459: Base item code 2995-40A does not match an active product'
    - - :error
      - 'Line 1460: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 1462: Base item code 3601-40A does not match an active product'
    - - :error
      - 'Line 1636: Base item code 1246-22A does not match an active product'
    - - :error
      - 'Line 1801: Base item code 1238N-22A does not match an active product'
    - - :error
      - 'Line 1806: Base item code 1239-76A does not match an active product'
    - - :error
      - 'Line 1810: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1812: Base item code 1241-22A does not match an active product'
    - - :error
      - 'Line 1815: Base item code 1241-48S does not match an active product'
    - - :error
      - 'Line 1823: Base item code 1243-22A does not match an active product'
    - - :error
      - 'Line 1825: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1912: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 2057: Base item code CM8519N-401A does not match an active product'
    - - :error
      - 'Line 2255: Base item code SFDR-18-26 does not match an active product'
    - - :error
      - 'Line 2256: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 2268: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2269: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2331: BillToCode (13171071) is invalid.'
    - - :error
      - 'Line 2503: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2504: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2574: BillToCode (13171471) is invalid.'
    - - :error
      - 'Line 2727: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2728: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2757: Base item code CM8326N-401A does not match an active product'
    - - :warning
      - "-214 more rows with invalid products"
 |
| 2026-06-14T05:46:39.312768 | ---
- - Inventory
  - - - :warning
      - 'Line 5: Product not found, record ignored., BaseItemCode=1239-22A'
    - - :warning
      - 'Line 8: Product not found, record ignored., BaseItemCode=1239-23A'
    - - :warning
      - 'Line 13: Product not found, record ignored., BaseItemCode=1239-40A'
    - - :warning
      - 'Line 16: Product not found, record ignored., BaseItemCode=1239-48A'
    - - :warning
      - 'Line 19: Product not found, record ignored., BaseItemCode=1239-76A'
    - - :warning
      - 'Line 24: Product not found, record ignored., BaseItemCode=1240-22A'
    - - :warning
      - 'Line 27: Product not found, record ignored., BaseItemCode=1240-23A'
    - - :warning
      - 'Line 32: Product not found, record ignored., BaseItemCode=1240-40A'
    - - :warning
      - 'Line 35: Product not found, record ignored., BaseItemCode=1240-48A'
    - - :warning
      - 'Line 38: Product not found, record ignored., BaseItemCode=1240-76A'
    - - :warning
      - 'Line 43: Product not found, record ignored., BaseItemCode=1241-22A'
    - - :warning
      - 'Line 46: Product not found, record ignored., BaseItemCode=1241-23A'
    - - :warning
      - 'Line 51: Product not found, record ignored., BaseItemCode=1241-40A'
    - - :warning
      - 'Line 54: Product not found, record ignored., BaseItemCode=1241-48A'
    - - :warning
      - 'Line 56: Product not found, record ignored., BaseItemCode=1241-48S'
    - - :warning
      - 'Line 58: Product not found, record ignored., BaseItemCode=1241-76A'
    - - :warning
      - 'Line 77: Product not found, record ignored., BaseItemCode=1243-22A'
    - - :warning
      - 'Line 80: Product not found, record ignored., BaseItemCode=1243-23A'
    - - :warning
      - 'Line 82: Product not found, record ignored., BaseItemCode=1243-23S'
    - - :warning
      - 'Line 86: Product not found, record ignored., BaseItemCode=1243-40A'
    - - :warning
      - 'Line 89: Product not found, record ignored., BaseItemCode=1243-48A'
    - - :warning
      - 'Line 92: Product not found, record ignored., BaseItemCode=1243-76A'
    - - :warning
      - 'Line 104: Product not found, record ignored., BaseItemCode=1558-48R'
    - - :warning
      - 'Line 133: Product not found, record ignored., BaseItemCode=1701U-76'
    - - :warning
      - 'Line 142: Product not found, record ignored., BaseItemCode=1702U-76'
    - - :warning
      - 'Line 151: Product not found, record ignored., BaseItemCode=1703U-76'
    - - :warning
      - 'Line 160: Product not found, record ignored., BaseItemCode=1704U-76'
    - - :warning
      - 'Line 173: Product not found, record ignored., BaseItemCode=1712-55'
    - - :warning
      - 'Line 174: Product not found, record ignored., BaseItemCode=1712U-76'
    - - :warning
      - 'Line 177: Product not found, record ignored., BaseItemCode=2124A'
    - - :warning
      - 'Line 179: Product not found, record ignored., BaseItemCode=2220A'
    - - :warning
      - 'Line 182: Product not found, record ignored., BaseItemCode=2224A'
    - - :warning
      - 'Line 193: Product not found, record ignored., BaseItemCode=2274A'
    - - :warning
      - 'Line 205: Product not found, record ignored., BaseItemCode=2642L-211O'
    - - :warning
      - 'Line 210: Product not found, record ignored., BaseItemCode=2990-40A'
    - - :warning
      - 'Line 213: Product not found, record ignored., BaseItemCode=2991-40A'
    - - :warning
      - 'Line 218: Product not found, record ignored., BaseItemCode=2994-40A'
    - - :warning
      - 'Line 221: Product not found, record ignored., BaseItemCode=2999-40A'
    - - :warning
      - 'Line 299: Product not found, record ignored., BaseItemCode=3608-40A'
    - - :warning
      - 'Line 560: Product not found, record ignored., BaseItemCode=5075-48S'
    - - :warning
      - 'Line 765: Product not found, record ignored., BaseItemCode=6816-40A'
    - - :warning
      - 'Line 834: Product not found, record ignored., BaseItemCode=AT1001N-23H'
    - - :warning
      - 'Line 1335: Product not found, record ignored., BaseItemCode=CM8326N-401A'
    - - :warning
      - 'Line 1337: Product not found, record ignored., BaseItemCode=CM8334N-401A'
    - - :warning
      - 'Line 1340: Product not found, record ignored., BaseItemCode=CM8519N-401A'
    - - :warning
      - 'Line 1452: Product not found, record ignored., BaseItemCode=MD1005N-51H'
    - - :warning
      - 'Line 1458: Product not found, record ignored., BaseItemCode=MD1006N-44H'
    - - :warning
      - 'Line 1509: Product not found, record ignored., BaseItemCode=RJ1003N-23H'
    - - :warning
      - 'Line 2419: Product not found, record ignored., BaseItemCode=SF-RCBT-WT'
    - - :warning
      - 'Line 2420: Product not found, record ignored., BaseItemCode=SF-WCBT-WT'
    - - :warning
      - 'Line 2421: Product not found, record ignored., BaseItemCode=SFCK-26'
    - - :warning
      - 'Line 2422: Product not found, record ignored., BaseItemCode=SFCK-51'
    - - :warning
      - 'Line 2423: Product not found, record ignored., BaseItemCode=SFDR-12-26'
    - - :warning
      - 'Line 2424: Product not found, record ignored., BaseItemCode=SFDR-12-51'
    - - :warning
      - 'Line 2425: Product not found, record ignored., BaseItemCode=SFDR-18-26'
    - - :warning
      - 'Line 2426: Product not found, record ignored., BaseItemCode=SFDR-18-51'
    - - :warning
      - 'Line 2427: Product not found, record ignored., BaseItemCode=SFDR-24-26'
    - - :warning
      - 'Line 2428: Product not found, record ignored., BaseItemCode=SFDR-24-51'
    - - :warning
      - 'Line 2429: Product not found, record ignored., BaseItemCode=SFDR-48-26'
    - - :warning
      - 'Line 2430: Product not found, record ignored., BaseItemCode=SFDR-48-51'
    - - :warning
      - 'Line 2431: Product not found, record ignored., BaseItemCode=SFDR-I-26'
    - - :warning
      - 'Line 2432: Product not found, record ignored., BaseItemCode=SFDR-I-51'
    - - :warning
      - 'Line 2438: Product not found, record ignored., BaseItemCode=SJ1012T24-RBL702R'
    - - :warning
      - 'Line 2439: Product not found, record ignored., BaseItemCode=SJ1012T24-RGO702R'
    - - :warning
      - 'Line 2440: Product not found, record ignored., BaseItemCode=SJ1012T24-RRE702R'
    - - :warning
      - 'Line 2456: Product not found, record ignored., BaseItemCode=SJ2310T24-RBL702R'
    - - :warning
      - 'Line 2457: Product not found, record ignored., BaseItemCode=SJ2310T24-RGO702R'
    - - :warning
      - 'Line 2458: Product not found, record ignored., BaseItemCode=SJ2310T24-RRE702R'
    - - :warning
      - 'Line 2473: Product not found, record ignored., BaseItemCode=SJ3611T24-RBL702R'
    - - :warning
      - 'Line 2474: Product not found, record ignored., BaseItemCode=SJ3611T24-RGO702R'
    - - :warning
      - 'Line 2475: Product not found, record ignored., BaseItemCode=SJ3611T24-RRE702R'
    - - :warning
      - 'Line 2506: Product not found, record ignored., BaseItemCode=SJ4914T24-RBL702R'
    - - :warning
      - 'Line 2507: Product not found, record ignored., BaseItemCode=SJ4914T24-RGO702R'
    - - :warning
      - 'Line 2508: Product not found, record ignored., BaseItemCode=SJ4914T24-RRE702R'
    - - :warning
      - 'Line 2594: Product not found, record ignored., BaseItemCode=SJ8813T24-RBL702R'
    - - :warning
      - 'Line 2595: Product not found, record ignored., BaseItemCode=SJ8813T24-RGO702R'
    - - :warning
      - 'Line 2596: Product not found, record ignored., BaseItemCode=SJ8813T24-RRE702R'
    - - :warning
      - 'Line 2783: Product not found, record ignored., BaseItemCode=WH-WS-WT'
- - Customers
  - - - :error
      - 'Line 1359: error=Validation failed: Shipping state can''t be blank: Customer
        # = 13172787'
- - Sales Data
  - - - :error
      - 'Line 44: Base item code SFCK-26 does not match an active product'
    - - :error
      - 'Line 45: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 107: Base item code 5685-80R does not match an active product'
    - - :error
      - 'Line 247: Base item code 1712U-76 does not match an active product'
    - - :error
      - 'Line 350: BillToCode (03983000) is invalid.'
    - - :error
      - 'Line 369: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 383: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 384: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 385: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 823: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 824: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 825: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 826: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 827: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 828: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 829: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 830: BillToCode (09371000) is invalid.'
    - - :error
      - 'Line 894: Base item code SF-RCBT-WT does not match an active product'
    - - :error
      - 'Line 895: Base item code SF-WCBT-WT does not match an active product'
    - - :error
      - 'Line 938: Base item code 1239-40A does not match an active product'
    - - :error
      - 'Line 987: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 1212: Base item code 1238N-48A does not match an active product'
    - - :error
      - 'Line 1213: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1420: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1424: Base item code 1248-22A does not match an active product'
    - - :error
      - 'Line 1457: Base item code 2124A does not match an active product'
    - - :error
      - 'Line 1459: Base item code 2995-40A does not match an active product'
    - - :error
      - 'Line 1460: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 1462: Base item code 3601-40A does not match an active product'
    - - :error
      - 'Line 1636: Base item code 1246-22A does not match an active product'
    - - :error
      - 'Line 1801: Base item code 1238N-22A does not match an active product'
    - - :error
      - 'Line 1806: Base item code 1239-76A does not match an active product'
    - - :error
      - 'Line 1810: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1812: Base item code 1241-22A does not match an active product'
    - - :error
      - 'Line 1815: Base item code 1241-48S does not match an active product'
    - - :error
      - 'Line 1823: Base item code 1243-22A does not match an active product'
    - - :error
      - 'Line 1825: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1912: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 2057: Base item code CM8519N-401A does not match an active product'
    - - :error
      - 'Line 2255: Base item code SFDR-18-26 does not match an active product'
    - - :error
      - 'Line 2256: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 2268: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2269: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2331: BillToCode (13171071) is invalid.'
    - - :error
      - 'Line 2503: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2504: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2574: BillToCode (13171471) is invalid.'
    - - :error
      - 'Line 2727: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2728: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2757: Base item code CM8326N-401A does not match an active product'
    - - :warning
      - "-214 more rows with invalid products"
 |
| 2026-06-13T05:46:37.315559 | ---
- - Inventory
  - - - :warning
      - 'Line 5: Product not found, record ignored., BaseItemCode=1239-22A'
    - - :warning
      - 'Line 8: Product not found, record ignored., BaseItemCode=1239-23A'
    - - :warning
      - 'Line 13: Product not found, record ignored., BaseItemCode=1239-40A'
    - - :warning
      - 'Line 16: Product not found, record ignored., BaseItemCode=1239-48A'
    - - :warning
      - 'Line 19: Product not found, record ignored., BaseItemCode=1239-76A'
    - - :warning
      - 'Line 24: Product not found, record ignored., BaseItemCode=1240-22A'
    - - :warning
      - 'Line 27: Product not found, record ignored., BaseItemCode=1240-23A'
    - - :warning
      - 'Line 32: Product not found, record ignored., BaseItemCode=1240-40A'
    - - :warning
      - 'Line 35: Product not found, record ignored., BaseItemCode=1240-48A'
    - - :warning
      - 'Line 38: Product not found, record ignored., BaseItemCode=1240-76A'
    - - :warning
      - 'Line 43: Product not found, record ignored., BaseItemCode=1241-22A'
    - - :warning
      - 'Line 46: Product not found, record ignored., BaseItemCode=1241-23A'
    - - :warning
      - 'Line 51: Product not found, record ignored., BaseItemCode=1241-40A'
    - - :warning
      - 'Line 54: Product not found, record ignored., BaseItemCode=1241-48A'
    - - :warning
      - 'Line 56: Product not found, record ignored., BaseItemCode=1241-48S'
    - - :warning
      - 'Line 58: Product not found, record ignored., BaseItemCode=1241-76A'
    - - :warning
      - 'Line 77: Product not found, record ignored., BaseItemCode=1243-22A'
    - - :warning
      - 'Line 80: Product not found, record ignored., BaseItemCode=1243-23A'
    - - :warning
      - 'Line 82: Product not found, record ignored., BaseItemCode=1243-23S'
    - - :warning
      - 'Line 86: Product not found, record ignored., BaseItemCode=1243-40A'
    - - :warning
      - 'Line 89: Product not found, record ignored., BaseItemCode=1243-48A'
    - - :warning
      - 'Line 92: Product not found, record ignored., BaseItemCode=1243-76A'
    - - :warning
      - 'Line 104: Product not found, record ignored., BaseItemCode=1558-48R'
    - - :warning
      - 'Line 133: Product not found, record ignored., BaseItemCode=1701U-76'
    - - :warning
      - 'Line 142: Product not found, record ignored., BaseItemCode=1702U-76'
    - - :warning
      - 'Line 151: Product not found, record ignored., BaseItemCode=1703U-76'
    - - :warning
      - 'Line 160: Product not found, record ignored., BaseItemCode=1704U-76'
    - - :warning
      - 'Line 173: Product not found, record ignored., BaseItemCode=1712-55'
    - - :warning
      - 'Line 174: Product not found, record ignored., BaseItemCode=1712U-76'
    - - :warning
      - 'Line 177: Product not found, record ignored., BaseItemCode=2124A'
    - - :warning
      - 'Line 179: Product not found, record ignored., BaseItemCode=2220A'
    - - :warning
      - 'Line 182: Product not found, record ignored., BaseItemCode=2224A'
    - - :warning
      - 'Line 193: Product not found, record ignored., BaseItemCode=2274A'
    - - :warning
      - 'Line 205: Product not found, record ignored., BaseItemCode=2642L-211O'
    - - :warning
      - 'Line 210: Product not found, record ignored., BaseItemCode=2990-40A'
    - - :warning
      - 'Line 213: Product not found, record ignored., BaseItemCode=2991-40A'
    - - :warning
      - 'Line 218: Product not found, record ignored., BaseItemCode=2994-40A'
    - - :warning
      - 'Line 221: Product not found, record ignored., BaseItemCode=2999-40A'
    - - :warning
      - 'Line 299: Product not found, record ignored., BaseItemCode=3608-40A'
    - - :warning
      - 'Line 560: Product not found, record ignored., BaseItemCode=5075-48S'
    - - :warning
      - 'Line 765: Product not found, record ignored., BaseItemCode=6816-40A'
    - - :warning
      - 'Line 834: Product not found, record ignored., BaseItemCode=AT1001N-23H'
    - - :warning
      - 'Line 1335: Product not found, record ignored., BaseItemCode=CM8326N-401A'
    - - :warning
      - 'Line 1337: Product not found, record ignored., BaseItemCode=CM8334N-401A'
    - - :warning
      - 'Line 1340: Product not found, record ignored., BaseItemCode=CM8519N-401A'
    - - :warning
      - 'Line 1452: Product not found, record ignored., BaseItemCode=MD1005N-51H'
    - - :warning
      - 'Line 1458: Product not found, record ignored., BaseItemCode=MD1006N-44H'
    - - :warning
      - 'Line 1509: Product not found, record ignored., BaseItemCode=RJ1003N-23H'
    - - :warning
      - 'Line 2419: Product not found, record ignored., BaseItemCode=SF-RCBT-WT'
    - - :warning
      - 'Line 2420: Product not found, record ignored., BaseItemCode=SF-WCBT-WT'
    - - :warning
      - 'Line 2421: Product not found, record ignored., BaseItemCode=SFCK-26'
    - - :warning
      - 'Line 2422: Product not found, record ignored., BaseItemCode=SFCK-51'
    - - :warning
      - 'Line 2423: Product not found, record ignored., BaseItemCode=SFDR-12-26'
    - - :warning
      - 'Line 2424: Product not found, record ignored., BaseItemCode=SFDR-12-51'
    - - :warning
      - 'Line 2425: Product not found, record ignored., BaseItemCode=SFDR-18-26'
    - - :warning
      - 'Line 2426: Product not found, record ignored., BaseItemCode=SFDR-18-51'
    - - :warning
      - 'Line 2427: Product not found, record ignored., BaseItemCode=SFDR-24-26'
    - - :warning
      - 'Line 2428: Product not found, record ignored., BaseItemCode=SFDR-24-51'
    - - :warning
      - 'Line 2429: Product not found, record ignored., BaseItemCode=SFDR-48-26'
    - - :warning
      - 'Line 2430: Product not found, record ignored., BaseItemCode=SFDR-48-51'
    - - :warning
      - 'Line 2431: Product not found, record ignored., BaseItemCode=SFDR-I-26'
    - - :warning
      - 'Line 2432: Product not found, record ignored., BaseItemCode=SFDR-I-51'
    - - :warning
      - 'Line 2438: Product not found, record ignored., BaseItemCode=SJ1012T24-RBL702R'
    - - :warning
      - 'Line 2439: Product not found, record ignored., BaseItemCode=SJ1012T24-RGO702R'
    - - :warning
      - 'Line 2440: Product not found, record ignored., BaseItemCode=SJ1012T24-RRE702R'
    - - :warning
      - 'Line 2456: Product not found, record ignored., BaseItemCode=SJ2310T24-RBL702R'
    - - :warning
      - 'Line 2457: Product not found, record ignored., BaseItemCode=SJ2310T24-RGO702R'
    - - :warning
      - 'Line 2458: Product not found, record ignored., BaseItemCode=SJ2310T24-RRE702R'
    - - :warning
      - 'Line 2473: Product not found, record ignored., BaseItemCode=SJ3611T24-RBL702R'
    - - :warning
      - 'Line 2474: Product not found, record ignored., BaseItemCode=SJ3611T24-RGO702R'
    - - :warning
      - 'Line 2475: Product not found, record ignored., BaseItemCode=SJ3611T24-RRE702R'
    - - :warning
      - 'Line 2506: Product not found, record ignored., BaseItemCode=SJ4914T24-RBL702R'
    - - :warning
      - 'Line 2507: Product not found, record ignored., BaseItemCode=SJ4914T24-RGO702R'
    - - :warning
      - 'Line 2508: Product not found, record ignored., BaseItemCode=SJ4914T24-RRE702R'
    - - :warning
      - 'Line 2594: Product not found, record ignored., BaseItemCode=SJ8813T24-RBL702R'
    - - :warning
      - 'Line 2595: Product not found, record ignored., BaseItemCode=SJ8813T24-RGO702R'
    - - :warning
      - 'Line 2596: Product not found, record ignored., BaseItemCode=SJ8813T24-RRE702R'
    - - :warning
      - 'Line 2783: Product not found, record ignored., BaseItemCode=WH-WS-WT'
- - Customers
  - - - :error
      - 'Line 1359: error=Validation failed: Shipping state can''t be blank: Customer
        # = 13172787'
- - Sales Data
  - - - :error
      - 'Line 44: Base item code SFCK-26 does not match an active product'
    - - :error
      - 'Line 45: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 107: Base item code 5685-80R does not match an active product'
    - - :error
      - 'Line 247: Base item code 1712U-76 does not match an active product'
    - - :error
      - 'Line 350: BillToCode (03983000) is invalid.'
    - - :error
      - 'Line 369: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 383: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 384: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 385: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 825: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 826: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 827: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 828: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 829: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 830: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 831: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 832: BillToCode (09371000) is invalid.'
    - - :error
      - 'Line 896: Base item code SF-RCBT-WT does not match an active product'
    - - :error
      - 'Line 897: Base item code SF-WCBT-WT does not match an active product'
    - - :error
      - 'Line 940: Base item code 1239-40A does not match an active product'
    - - :error
      - 'Line 989: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 1214: Base item code 1238N-48A does not match an active product'
    - - :error
      - 'Line 1215: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1422: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1426: Base item code 1248-22A does not match an active product'
    - - :error
      - 'Line 1459: Base item code 2124A does not match an active product'
    - - :error
      - 'Line 1461: Base item code 2995-40A does not match an active product'
    - - :error
      - 'Line 1462: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 1464: Base item code 3601-40A does not match an active product'
    - - :error
      - 'Line 1639: Base item code 1246-22A does not match an active product'
    - - :error
      - 'Line 1804: Base item code 1238N-22A does not match an active product'
    - - :error
      - 'Line 1809: Base item code 1239-76A does not match an active product'
    - - :error
      - 'Line 1813: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1815: Base item code 1241-22A does not match an active product'
    - - :error
      - 'Line 1818: Base item code 1241-48S does not match an active product'
    - - :error
      - 'Line 1826: Base item code 1243-22A does not match an active product'
    - - :error
      - 'Line 1828: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1915: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 2061: Base item code CM8519N-401A does not match an active product'
    - - :error
      - 'Line 2259: Base item code SFDR-18-26 does not match an active product'
    - - :error
      - 'Line 2260: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 2272: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2273: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2335: BillToCode (13171071) is invalid.'
    - - :error
      - 'Line 2507: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2508: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2578: BillToCode (13171471) is invalid.'
    - - :error
      - 'Line 2731: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2732: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2761: Base item code CM8326N-401A does not match an active product'
    - - :warning
      - "-214 more rows with invalid products"
 |
| 2026-06-12T05:46:28.772038 | ---
- - Inventory
  - - - :warning
      - 'Line 2: Product not found, record ignored., BaseItemCode=1239-22A'
    - - :warning
      - 'Line 3: Product not found, record ignored., BaseItemCode=1239-23A'
    - - :warning
      - 'Line 5: Product not found, record ignored., BaseItemCode=1239-40A'
    - - :warning
      - 'Line 7: Product not found, record ignored., BaseItemCode=1239-48A'
    - - :warning
      - 'Line 9: Product not found, record ignored., BaseItemCode=1239-76A'
    - - :warning
      - 'Line 11: Product not found, record ignored., BaseItemCode=1240-22A'
    - - :warning
      - 'Line 13: Product not found, record ignored., BaseItemCode=1240-23A'
    - - :warning
      - 'Line 14: Product not found, record ignored., BaseItemCode=1240-40A'
    - - :warning
      - 'Line 15: Product not found, record ignored., BaseItemCode=1240-48A'
    - - :warning
      - 'Line 16: Product not found, record ignored., BaseItemCode=1240-76A'
    - - :warning
      - 'Line 18: Product not found, record ignored., BaseItemCode=1241-22A'
    - - :warning
      - 'Line 20: Product not found, record ignored., BaseItemCode=1241-23A'
    - - :warning
      - 'Line 21: Product not found, record ignored., BaseItemCode=1241-40A'
    - - :warning
      - 'Line 22: Product not found, record ignored., BaseItemCode=1241-48A'
    - - :warning
      - 'Line 23: Product not found, record ignored., BaseItemCode=1241-48S'
    - - :warning
      - 'Line 24: Product not found, record ignored., BaseItemCode=1241-76A'
    - - :warning
      - 'Line 29: Product not found, record ignored., BaseItemCode=1243-22A'
    - - :warning
      - 'Line 30: Product not found, record ignored., BaseItemCode=1243-23A'
    - - :warning
      - 'Line 31: Product not found, record ignored., BaseItemCode=1243-23S'
    - - :warning
      - 'Line 32: Product not found, record ignored., BaseItemCode=1243-40A'
    - - :warning
      - 'Line 34: Product not found, record ignored., BaseItemCode=1243-48A'
    - - :warning
      - 'Line 35: Product not found, record ignored., BaseItemCode=1243-76A'
    - - :warning
      - 'Line 52: Product not found, record ignored., BaseItemCode=2124A'
    - - :warning
      - 'Line 53: Product not found, record ignored., BaseItemCode=2220A'
    - - :warning
      - 'Line 54: Product not found, record ignored., BaseItemCode=2224A'
    - - :warning
      - 'Line 55: Product not found, record ignored., BaseItemCode=2274A'
    - - :warning
      - 'Line 59: Product not found, record ignored., BaseItemCode=2990-40A'
    - - :warning
      - 'Line 60: Product not found, record ignored., BaseItemCode=2991-40A'
    - - :warning
      - 'Line 62: Product not found, record ignored., BaseItemCode=2994-40A'
    - - :warning
      - 'Line 64: Product not found, record ignored., BaseItemCode=2999-40A'
    - - :warning
      - 'Line 67: Product not found, record ignored., BaseItemCode=3608-40A'
    - - :warning
      - 'Line 96: Product not found, record ignored., BaseItemCode=5075-48S'
    - - :warning
      - 'Line 114: Product not found, record ignored., BaseItemCode=6816-40A'
    - - :warning
      - 'Line 394: Product not found, record ignored., BaseItemCode=CM8326N-401A'
    - - :warning
      - 'Line 395: Product not found, record ignored., BaseItemCode=CM8334N-401A'
    - - :warning
      - 'Line 396: Product not found, record ignored., BaseItemCode=CM8519N-401A'
    - - :warning
      - 'Line 658: Product not found, record ignored., BaseItemCode=SF-RCBT-WT'
    - - :warning
      - 'Line 659: Product not found, record ignored., BaseItemCode=SF-WCBT-WT'
    - - :warning
      - 'Line 660: Product not found, record ignored., BaseItemCode=SFCK-26'
    - - :warning
      - 'Line 661: Product not found, record ignored., BaseItemCode=SFCK-51'
    - - :warning
      - 'Line 662: Product not found, record ignored., BaseItemCode=SFDR-12-26'
    - - :warning
      - 'Line 663: Product not found, record ignored., BaseItemCode=SFDR-12-51'
    - - :warning
      - 'Line 664: Product not found, record ignored., BaseItemCode=SFDR-18-26'
    - - :warning
      - 'Line 665: Product not found, record ignored., BaseItemCode=SFDR-18-51'
    - - :warning
      - 'Line 666: Product not found, record ignored., BaseItemCode=SFDR-24-26'
    - - :warning
      - 'Line 667: Product not found, record ignored., BaseItemCode=SFDR-24-51'
    - - :warning
      - 'Line 668: Product not found, record ignored., BaseItemCode=SFDR-48-26'
    - - :warning
      - 'Line 669: Product not found, record ignored., BaseItemCode=SFDR-48-51'
    - - :warning
      - 'Line 670: Product not found, record ignored., BaseItemCode=SFDR-I-26'
    - - :warning
      - 'Line 671: Product not found, record ignored., BaseItemCode=SFDR-I-51'
    - - :warning
      - 'Line 718: Product not found, record ignored., BaseItemCode=WH-WS-WT'
- - Customers
  - - - :error
      - 'Line 1359: error=Validation failed: Shipping state can''t be blank: Customer
        # = 13172787'
- - Sales Data
  - - - :error
      - 'Line 44: Base item code SFCK-26 does not match an active product'
    - - :error
      - 'Line 45: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 107: Base item code 5685-80R does not match an active product'
    - - :error
      - 'Line 247: Base item code 1712U-76 does not match an active product'
    - - :error
      - 'Line 351: BillToCode (03983000) is invalid.'
    - - :error
      - 'Line 370: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 384: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 385: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 386: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 825: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 826: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 827: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 828: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 829: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 830: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 831: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 832: BillToCode (09371000) is invalid.'
    - - :error
      - 'Line 896: Base item code SF-RCBT-WT does not match an active product'
    - - :error
      - 'Line 897: Base item code SF-WCBT-WT does not match an active product'
    - - :error
      - 'Line 940: Base item code 1239-40A does not match an active product'
    - - :error
      - 'Line 989: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 1217: Base item code 1238N-48A does not match an active product'
    - - :error
      - 'Line 1218: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1425: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1429: Base item code 1248-22A does not match an active product'
    - - :error
      - 'Line 1462: Base item code 2124A does not match an active product'
    - - :error
      - 'Line 1464: Base item code 2995-40A does not match an active product'
    - - :error
      - 'Line 1465: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 1467: Base item code 3601-40A does not match an active product'
    - - :error
      - 'Line 1642: Base item code 1246-22A does not match an active product'
    - - :error
      - 'Line 1806: Base item code 1238N-22A does not match an active product'
    - - :error
      - 'Line 1811: Base item code 1239-76A does not match an active product'
    - - :error
      - 'Line 1815: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1817: Base item code 1241-22A does not match an active product'
    - - :error
      - 'Line 1820: Base item code 1241-48S does not match an active product'
    - - :error
      - 'Line 1828: Base item code 1243-22A does not match an active product'
    - - :error
      - 'Line 1830: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1917: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 2063: Base item code CM8519N-401A does not match an active product'
    - - :error
      - 'Line 2261: Base item code SFDR-18-26 does not match an active product'
    - - :error
      - 'Line 2262: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 2274: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2275: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2337: BillToCode (13171071) is invalid.'
    - - :error
      - 'Line 2508: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2509: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2579: BillToCode (13171471) is invalid.'
    - - :error
      - 'Line 2731: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2732: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2761: Base item code CM8326N-401A does not match an active product'
    - - :warning
      - "-214 more rows with invalid products"
 |
| 2026-06-11T05:46:47.616670 | ---
- - Inventory
  - - - :warning
      - 'Line 5: Product not found, record ignored., BaseItemCode=1239-22A'
    - - :warning
      - 'Line 8: Product not found, record ignored., BaseItemCode=1239-23A'
    - - :warning
      - 'Line 13: Product not found, record ignored., BaseItemCode=1239-40A'
    - - :warning
      - 'Line 16: Product not found, record ignored., BaseItemCode=1239-48A'
    - - :warning
      - 'Line 19: Product not found, record ignored., BaseItemCode=1239-76A'
    - - :warning
      - 'Line 24: Product not found, record ignored., BaseItemCode=1240-22A'
    - - :warning
      - 'Line 27: Product not found, record ignored., BaseItemCode=1240-23A'
    - - :warning
      - 'Line 32: Product not found, record ignored., BaseItemCode=1240-40A'
    - - :warning
      - 'Line 35: Product not found, record ignored., BaseItemCode=1240-48A'
    - - :warning
      - 'Line 38: Product not found, record ignored., BaseItemCode=1240-76A'
    - - :warning
      - 'Line 43: Product not found, record ignored., BaseItemCode=1241-22A'
    - - :warning
      - 'Line 46: Product not found, record ignored., BaseItemCode=1241-23A'
    - - :warning
      - 'Line 51: Product not found, record ignored., BaseItemCode=1241-40A'
    - - :warning
      - 'Line 54: Product not found, record ignored., BaseItemCode=1241-48A'
    - - :warning
      - 'Line 56: Product not found, record ignored., BaseItemCode=1241-48S'
    - - :warning
      - 'Line 58: Product not found, record ignored., BaseItemCode=1241-76A'
    - - :warning
      - 'Line 77: Product not found, record ignored., BaseItemCode=1243-22A'
    - - :warning
      - 'Line 80: Product not found, record ignored., BaseItemCode=1243-23A'
    - - :warning
      - 'Line 82: Product not found, record ignored., BaseItemCode=1243-23S'
    - - :warning
      - 'Line 86: Product not found, record ignored., BaseItemCode=1243-40A'
    - - :warning
      - 'Line 89: Product not found, record ignored., BaseItemCode=1243-48A'
    - - :warning
      - 'Line 92: Product not found, record ignored., BaseItemCode=1243-76A'
    - - :warning
      - 'Line 104: Product not found, record ignored., BaseItemCode=1558-48R'
    - - :warning
      - 'Line 133: Product not found, record ignored., BaseItemCode=1701U-76'
    - - :warning
      - 'Line 142: Product not found, record ignored., BaseItemCode=1702U-76'
    - - :warning
      - 'Line 151: Product not found, record ignored., BaseItemCode=1703U-76'
    - - :warning
      - 'Line 160: Product not found, record ignored., BaseItemCode=1704U-76'
    - - :warning
      - 'Line 173: Product not found, record ignored., BaseItemCode=1712-55'
    - - :warning
      - 'Line 174: Product not found, record ignored., BaseItemCode=1712U-76'
    - - :warning
      - 'Line 177: Product not found, record ignored., BaseItemCode=2124A'
    - - :warning
      - 'Line 179: Product not found, record ignored., BaseItemCode=2220A'
    - - :warning
      - 'Line 182: Product not found, record ignored., BaseItemCode=2224A'
    - - :warning
      - 'Line 193: Product not found, record ignored., BaseItemCode=2274A'
    - - :warning
      - 'Line 205: Product not found, record ignored., BaseItemCode=2642L-211O'
    - - :warning
      - 'Line 212: Product not found, record ignored., BaseItemCode=2990-40A'
    - - :warning
      - 'Line 217: Product not found, record ignored., BaseItemCode=2991-40A'
    - - :warning
      - 'Line 226: Product not found, record ignored., BaseItemCode=2994-40A'
    - - :warning
      - 'Line 231: Product not found, record ignored., BaseItemCode=2999-40A'
    - - :warning
      - 'Line 308: Product not found, record ignored., BaseItemCode=3608-40A'
    - - :warning
      - 'Line 571: Product not found, record ignored., BaseItemCode=5075-48S'
    - - :warning
      - 'Line 786: Product not found, record ignored., BaseItemCode=6816-40A'
    - - :warning
      - 'Line 853: Product not found, record ignored., BaseItemCode=AT1001N-23H'
    - - :warning
      - 'Line 1358: Product not found, record ignored., BaseItemCode=CM8326N-401A'
    - - :warning
      - 'Line 1360: Product not found, record ignored., BaseItemCode=CM8334N-401A'
    - - :warning
      - 'Line 1363: Product not found, record ignored., BaseItemCode=CM8519N-401A'
    - - :warning
      - 'Line 1475: Product not found, record ignored., BaseItemCode=MD1005N-51H'
    - - :warning
      - 'Line 1481: Product not found, record ignored., BaseItemCode=MD1006N-44H'
    - - :warning
      - 'Line 1526: Product not found, record ignored., BaseItemCode=RJ1003N-23H'
    - - :warning
      - 'Line 2435: Product not found, record ignored., BaseItemCode=SF-RCBT-WT'
    - - :warning
      - 'Line 2436: Product not found, record ignored., BaseItemCode=SF-WCBT-WT'
    - - :warning
      - 'Line 2437: Product not found, record ignored., BaseItemCode=SFCK-26'
    - - :warning
      - 'Line 2438: Product not found, record ignored., BaseItemCode=SFCK-51'
    - - :warning
      - 'Line 2439: Product not found, record ignored., BaseItemCode=SFDR-12-26'
    - - :warning
      - 'Line 2440: Product not found, record ignored., BaseItemCode=SFDR-12-51'
    - - :warning
      - 'Line 2441: Product not found, record ignored., BaseItemCode=SFDR-18-26'
    - - :warning
      - 'Line 2442: Product not found, record ignored., BaseItemCode=SFDR-18-51'
    - - :warning
      - 'Line 2443: Product not found, record ignored., BaseItemCode=SFDR-24-26'
    - - :warning
      - 'Line 2444: Product not found, record ignored., BaseItemCode=SFDR-24-51'
    - - :warning
      - 'Line 2445: Product not found, record ignored., BaseItemCode=SFDR-48-26'
    - - :warning
      - 'Line 2446: Product not found, record ignored., BaseItemCode=SFDR-48-51'
    - - :warning
      - 'Line 2447: Product not found, record ignored., BaseItemCode=SFDR-I-26'
    - - :warning
      - 'Line 2448: Product not found, record ignored., BaseItemCode=SFDR-I-51'
    - - :warning
      - 'Line 2454: Product not found, record ignored., BaseItemCode=SJ1012T24-RBL702R'
    - - :warning
      - 'Line 2455: Product not found, record ignored., BaseItemCode=SJ1012T24-RGO702R'
    - - :warning
      - 'Line 2456: Product not found, record ignored., BaseItemCode=SJ1012T24-RRE702R'
    - - :warning
      - 'Line 2469: Product not found, record ignored., BaseItemCode=SJ2310T24-RBL702R'
    - - :warning
      - 'Line 2470: Product not found, record ignored., BaseItemCode=SJ2310T24-RGO702R'
    - - :warning
      - 'Line 2471: Product not found, record ignored., BaseItemCode=SJ2310T24-RRE702R'
    - - :warning
      - 'Line 2486: Product not found, record ignored., BaseItemCode=SJ3611T24-RBL702R'
    - - :warning
      - 'Line 2487: Product not found, record ignored., BaseItemCode=SJ3611T24-RGO702R'
    - - :warning
      - 'Line 2488: Product not found, record ignored., BaseItemCode=SJ3611T24-RRE702R'
    - - :warning
      - 'Line 2519: Product not found, record ignored., BaseItemCode=SJ4914T24-RBL702R'
    - - :warning
      - 'Line 2520: Product not found, record ignored., BaseItemCode=SJ4914T24-RGO702R'
    - - :warning
      - 'Line 2521: Product not found, record ignored., BaseItemCode=SJ4914T24-RRE702R'
    - - :warning
      - 'Line 2607: Product not found, record ignored., BaseItemCode=SJ8813T24-RBL702R'
    - - :warning
      - 'Line 2608: Product not found, record ignored., BaseItemCode=SJ8813T24-RGO702R'
    - - :warning
      - 'Line 2609: Product not found, record ignored., BaseItemCode=SJ8813T24-RRE702R'
    - - :warning
      - 'Line 2806: Product not found, record ignored., BaseItemCode=WH-WS-WT'
- - Customers
  - - - :error
      - 'Line 1359: error=Validation failed: Shipping state can''t be blank: Customer
        # = 13172787'
- - Sales Data
  - - - :error
      - 'Line 44: Base item code SFCK-26 does not match an active product'
    - - :error
      - 'Line 45: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 107: Base item code 5685-80R does not match an active product'
    - - :error
      - 'Line 247: Base item code 1712U-76 does not match an active product'
    - - :error
      - 'Line 352: BillToCode (03983000) is invalid.'
    - - :error
      - 'Line 371: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 385: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 386: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 387: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 826: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 827: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 828: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 829: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 830: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 831: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 832: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 833: BillToCode (09371000) is invalid.'
    - - :error
      - 'Line 897: Base item code SF-RCBT-WT does not match an active product'
    - - :error
      - 'Line 898: Base item code SF-WCBT-WT does not match an active product'
    - - :error
      - 'Line 941: Base item code 1239-40A does not match an active product'
    - - :error
      - 'Line 990: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 1218: Base item code 1238N-48A does not match an active product'
    - - :error
      - 'Line 1219: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1426: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1430: Base item code 1248-22A does not match an active product'
    - - :error
      - 'Line 1463: Base item code 2124A does not match an active product'
    - - :error
      - 'Line 1465: Base item code 2995-40A does not match an active product'
    - - :error
      - 'Line 1466: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 1468: Base item code 3601-40A does not match an active product'
    - - :error
      - 'Line 1642: Base item code 1246-22A does not match an active product'
    - - :error
      - 'Line 1806: Base item code 1238N-22A does not match an active product'
    - - :error
      - 'Line 1811: Base item code 1239-76A does not match an active product'
    - - :error
      - 'Line 1815: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1817: Base item code 1241-22A does not match an active product'
    - - :error
      - 'Line 1820: Base item code 1241-48S does not match an active product'
    - - :error
      - 'Line 1828: Base item code 1243-22A does not match an active product'
    - - :error
      - 'Line 1830: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1917: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 2063: Base item code CM8519N-401A does not match an active product'
    - - :error
      - 'Line 2261: Base item code SFDR-18-26 does not match an active product'
    - - :error
      - 'Line 2262: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 2274: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2275: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2337: BillToCode (13171071) is invalid.'
    - - :error
      - 'Line 2500: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2501: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2571: BillToCode (13171471) is invalid.'
    - - :error
      - 'Line 2724: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2725: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2754: Base item code CM8326N-401A does not match an active product'
    - - :warning
      - "-215 more rows with invalid products"
 |
| 2026-06-10T05:46:40.504512 | ---
- - Inventory
  - - - :warning
      - 'Line 5: Product not found, record ignored., BaseItemCode=1239-22A'
    - - :warning
      - 'Line 8: Product not found, record ignored., BaseItemCode=1239-23A'
    - - :warning
      - 'Line 13: Product not found, record ignored., BaseItemCode=1239-40A'
    - - :warning
      - 'Line 16: Product not found, record ignored., BaseItemCode=1239-48A'
    - - :warning
      - 'Line 19: Product not found, record ignored., BaseItemCode=1239-76A'
    - - :warning
      - 'Line 24: Product not found, record ignored., BaseItemCode=1240-22A'
    - - :warning
      - 'Line 27: Product not found, record ignored., BaseItemCode=1240-23A'
    - - :warning
      - 'Line 32: Product not found, record ignored., BaseItemCode=1240-40A'
    - - :warning
      - 'Line 35: Product not found, record ignored., BaseItemCode=1240-48A'
    - - :warning
      - 'Line 38: Product not found, record ignored., BaseItemCode=1240-76A'
    - - :warning
      - 'Line 41: Product not found, record ignored., BaseItemCode=1241-22A'
    - - :warning
      - 'Line 45: Product not found, record ignored., BaseItemCode=1241-48A'
    - - :warning
      - 'Line 47: Product not found, record ignored., BaseItemCode=1241-48S'
    - - :warning
      - 'Line 49: Product not found, record ignored., BaseItemCode=1241-76A'
    - - :warning
      - 'Line 67: Product not found, record ignored., BaseItemCode=1243-22A'
    - - :warning
      - 'Line 69: Product not found, record ignored., BaseItemCode=1243-23S'
    - - :warning
      - 'Line 71: Product not found, record ignored., BaseItemCode=1243-48A'
    - - :warning
      - 'Line 74: Product not found, record ignored., BaseItemCode=1243-76A'
    - - :warning
      - 'Line 83: Product not found, record ignored., BaseItemCode=1558-48R'
    - - :warning
      - 'Line 112: Product not found, record ignored., BaseItemCode=1701U-76'
    - - :warning
      - 'Line 121: Product not found, record ignored., BaseItemCode=1702U-76'
    - - :warning
      - 'Line 130: Product not found, record ignored., BaseItemCode=1703U-76'
    - - :warning
      - 'Line 134: Product not found, record ignored., BaseItemCode=1704U-76'
    - - :warning
      - 'Line 143: Product not found, record ignored., BaseItemCode=1712U-76'
    - - :warning
      - 'Line 146: Product not found, record ignored., BaseItemCode=2124A'
    - - :warning
      - 'Line 148: Product not found, record ignored., BaseItemCode=2220A'
    - - :warning
      - 'Line 151: Product not found, record ignored., BaseItemCode=2224A'
    - - :warning
      - 'Line 162: Product not found, record ignored., BaseItemCode=2274A'
    - - :warning
      - 'Line 176: Product not found, record ignored., BaseItemCode=2990-40A'
    - - :warning
      - 'Line 181: Product not found, record ignored., BaseItemCode=2991-40A'
    - - :warning
      - 'Line 213: Product not found, record ignored., BaseItemCode=3608-40A'
    - - :warning
      - 'Line 389: Product not found, record ignored., BaseItemCode=5075-48S'
    - - :warning
      - 'Line 580: Product not found, record ignored., BaseItemCode=6816-40A'
    - - :warning
      - 'Line 645: Product not found, record ignored., BaseItemCode=AT1001N-23H'
    - - :warning
      - 'Line 1141: Product not found, record ignored., BaseItemCode=CM8326N-401A'
    - - :warning
      - 'Line 1143: Product not found, record ignored., BaseItemCode=CM8334N-401A'
    - - :warning
      - 'Line 1146: Product not found, record ignored., BaseItemCode=CM8519N-401A'
    - - :warning
      - 'Line 1251: Product not found, record ignored., BaseItemCode=MD1005N-51H'
    - - :warning
      - 'Line 2117: Product not found, record ignored., BaseItemCode=SF-RCBT-WT'
    - - :warning
      - 'Line 2118: Product not found, record ignored., BaseItemCode=SF-WCBT-WT'
    - - :warning
      - 'Line 2119: Product not found, record ignored., BaseItemCode=SFCK-26'
    - - :warning
      - 'Line 2120: Product not found, record ignored., BaseItemCode=SFCK-51'
    - - :warning
      - 'Line 2121: Product not found, record ignored., BaseItemCode=SFDR-12-26'
    - - :warning
      - 'Line 2122: Product not found, record ignored., BaseItemCode=SFDR-12-51'
    - - :warning
      - 'Line 2123: Product not found, record ignored., BaseItemCode=SFDR-18-26'
    - - :warning
      - 'Line 2124: Product not found, record ignored., BaseItemCode=SFDR-18-51'
    - - :warning
      - 'Line 2125: Product not found, record ignored., BaseItemCode=SFDR-24-26'
    - - :warning
      - 'Line 2126: Product not found, record ignored., BaseItemCode=SFDR-24-51'
    - - :warning
      - 'Line 2127: Product not found, record ignored., BaseItemCode=SFDR-48-26'
    - - :warning
      - 'Line 2128: Product not found, record ignored., BaseItemCode=SFDR-48-51'
    - - :warning
      - 'Line 2129: Product not found, record ignored., BaseItemCode=SFDR-I-26'
    - - :warning
      - 'Line 2130: Product not found, record ignored., BaseItemCode=SFDR-I-51'
    - - :warning
      - 'Line 2136: Product not found, record ignored., BaseItemCode=SJ1012T24-RBL702R'
    - - :warning
      - 'Line 2137: Product not found, record ignored., BaseItemCode=SJ1012T24-RGO702R'
    - - :warning
      - 'Line 2138: Product not found, record ignored., BaseItemCode=SJ1012T24-RRE702R'
    - - :warning
      - 'Line 2151: Product not found, record ignored., BaseItemCode=SJ2310T24-RBL702R'
    - - :warning
      - 'Line 2152: Product not found, record ignored., BaseItemCode=SJ2310T24-RGO702R'
    - - :warning
      - 'Line 2153: Product not found, record ignored., BaseItemCode=SJ2310T24-RRE702R'
    - - :warning
      - 'Line 2168: Product not found, record ignored., BaseItemCode=SJ3611T24-RBL702R'
    - - :warning
      - 'Line 2169: Product not found, record ignored., BaseItemCode=SJ3611T24-RGO702R'
    - - :warning
      - 'Line 2170: Product not found, record ignored., BaseItemCode=SJ3611T24-RRE702R'
    - - :warning
      - 'Line 2201: Product not found, record ignored., BaseItemCode=SJ4914T24-RBL702R'
    - - :warning
      - 'Line 2202: Product not found, record ignored., BaseItemCode=SJ4914T24-RGO702R'
    - - :warning
      - 'Line 2203: Product not found, record ignored., BaseItemCode=SJ4914T24-RRE702R'
    - - :warning
      - 'Line 2283: Product not found, record ignored., BaseItemCode=SJ8813T24-RBL702R'
    - - :warning
      - 'Line 2284: Product not found, record ignored., BaseItemCode=SJ8813T24-RGO702R'
    - - :warning
      - 'Line 2285: Product not found, record ignored., BaseItemCode=SJ8813T24-RRE702R'
    - - :warning
      - 'Line 2452: Product not found, record ignored., BaseItemCode=WH-WS-WT'
- - Customers
  - - - :error
      - 'Line 1359: error=Validation failed: Shipping state can''t be blank: Customer
        # = 13172787'
- - Sales Data
  - - - :error
      - 'Line 42: Base item code SFCK-26 does not match an active product'
    - - :error
      - 'Line 43: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 105: Base item code 5685-80R does not match an active product'
    - - :error
      - 'Line 245: Base item code 1712U-76 does not match an active product'
    - - :error
      - 'Line 349: BillToCode (03983000) is invalid.'
    - - :error
      - 'Line 368: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 382: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 383: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 384: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 822: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 823: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 824: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 825: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 826: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 827: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 828: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 829: BillToCode (09371000) is invalid.'
    - - :error
      - 'Line 893: Base item code SF-RCBT-WT does not match an active product'
    - - :error
      - 'Line 894: Base item code SF-WCBT-WT does not match an active product'
    - - :error
      - 'Line 937: Base item code 1239-40A does not match an active product'
    - - :error
      - 'Line 986: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 1213: Base item code 1238N-48A does not match an active product'
    - - :error
      - 'Line 1214: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1423: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1427: Base item code 1248-22A does not match an active product'
    - - :error
      - 'Line 1460: Base item code 2124A does not match an active product'
    - - :error
      - 'Line 1462: Base item code 2995-40A does not match an active product'
    - - :error
      - 'Line 1463: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 1465: Base item code 3601-40A does not match an active product'
    - - :error
      - 'Line 1639: Base item code 1246-22A does not match an active product'
    - - :error
      - 'Line 1803: Base item code 1238N-22A does not match an active product'
    - - :error
      - 'Line 1808: Base item code 1239-76A does not match an active product'
    - - :error
      - 'Line 1812: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1814: Base item code 1241-22A does not match an active product'
    - - :error
      - 'Line 1817: Base item code 1241-48S does not match an active product'
    - - :error
      - 'Line 1825: Base item code 1243-22A does not match an active product'
    - - :error
      - 'Line 1827: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1913: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 2059: Base item code CM8519N-401A does not match an active product'
    - - :error
      - 'Line 2257: Base item code SFDR-18-26 does not match an active product'
    - - :error
      - 'Line 2258: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 2270: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2271: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2333: BillToCode (13171071) is invalid.'
    - - :error
      - 'Line 2496: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2497: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2567: BillToCode (13171471) is invalid.'
    - - :error
      - 'Line 2720: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2721: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2750: Base item code CM8326N-401A does not match an active product'
    - - :warning
      - "-216 more rows with invalid products"
 |
| 2026-06-09T05:47:37.941908 | ---
- - Inventory
  - - - :warning
      - 'Line 5: Product not found, record ignored., BaseItemCode=1239-22A'
    - - :warning
      - 'Line 8: Product not found, record ignored., BaseItemCode=1239-23A'
    - - :warning
      - 'Line 13: Product not found, record ignored., BaseItemCode=1239-40A'
    - - :warning
      - 'Line 16: Product not found, record ignored., BaseItemCode=1239-48A'
    - - :warning
      - 'Line 19: Product not found, record ignored., BaseItemCode=1239-76A'
    - - :warning
      - 'Line 24: Product not found, record ignored., BaseItemCode=1240-22A'
    - - :warning
      - 'Line 27: Product not found, record ignored., BaseItemCode=1240-23A'
    - - :warning
      - 'Line 32: Product not found, record ignored., BaseItemCode=1240-40A'
    - - :warning
      - 'Line 35: Product not found, record ignored., BaseItemCode=1240-48A'
    - - :warning
      - 'Line 38: Product not found, record ignored., BaseItemCode=1240-76A'
    - - :warning
      - 'Line 41: Product not found, record ignored., BaseItemCode=1241-22A'
    - - :warning
      - 'Line 45: Product not found, record ignored., BaseItemCode=1241-48A'
    - - :warning
      - 'Line 48: Product not found, record ignored., BaseItemCode=1241-76A'
    - - :warning
      - 'Line 66: Product not found, record ignored., BaseItemCode=1243-22A'
    - - :warning
      - 'Line 69: Product not found, record ignored., BaseItemCode=1243-48A'
    - - :warning
      - 'Line 72: Product not found, record ignored., BaseItemCode=1243-76A'
    - - :warning
      - 'Line 81: Product not found, record ignored., BaseItemCode=1558-48R'
    - - :warning
      - 'Line 110: Product not found, record ignored., BaseItemCode=1701U-76'
    - - :warning
      - 'Line 119: Product not found, record ignored., BaseItemCode=1702U-76'
    - - :warning
      - 'Line 128: Product not found, record ignored., BaseItemCode=1703U-76'
    - - :warning
      - 'Line 133: Product not found, record ignored., BaseItemCode=1704U-76'
    - - :warning
      - 'Line 142: Product not found, record ignored., BaseItemCode=1712U-76'
    - - :warning
      - 'Line 145: Product not found, record ignored., BaseItemCode=2124A'
    - - :warning
      - 'Line 147: Product not found, record ignored., BaseItemCode=2220A'
    - - :warning
      - 'Line 150: Product not found, record ignored., BaseItemCode=2224A'
    - - :warning
      - 'Line 161: Product not found, record ignored., BaseItemCode=2274A'
    - - :warning
      - 'Line 175: Product not found, record ignored., BaseItemCode=2990-40A'
    - - :warning
      - 'Line 180: Product not found, record ignored., BaseItemCode=2991-40A'
    - - :warning
      - 'Line 212: Product not found, record ignored., BaseItemCode=3608-40A'
    - - :warning
      - 'Line 642: Product not found, record ignored., BaseItemCode=AT1001N-23H'
    - - :warning
      - 'Line 1111: Product not found, record ignored., BaseItemCode=CM8326N-401A'
    - - :warning
      - 'Line 1113: Product not found, record ignored., BaseItemCode=CM8334N-401A'
    - - :warning
      - 'Line 1116: Product not found, record ignored., BaseItemCode=CM8519N-401A'
    - - :warning
      - 'Line 1221: Product not found, record ignored., BaseItemCode=MD1005N-51H'
    - - :warning
      - 'Line 2087: Product not found, record ignored., BaseItemCode=SF-RCBT-WT'
    - - :warning
      - 'Line 2088: Product not found, record ignored., BaseItemCode=SF-WCBT-WT'
    - - :warning
      - 'Line 2089: Product not found, record ignored., BaseItemCode=SFCK-26'
    - - :warning
      - 'Line 2090: Product not found, record ignored., BaseItemCode=SFCK-51'
    - - :warning
      - 'Line 2091: Product not found, record ignored., BaseItemCode=SFDR-12-26'
    - - :warning
      - 'Line 2092: Product not found, record ignored., BaseItemCode=SFDR-12-51'
    - - :warning
      - 'Line 2093: Product not found, record ignored., BaseItemCode=SFDR-18-26'
    - - :warning
      - 'Line 2094: Product not found, record ignored., BaseItemCode=SFDR-18-51'
    - - :warning
      - 'Line 2095: Product not found, record ignored., BaseItemCode=SFDR-24-26'
    - - :warning
      - 'Line 2096: Product not found, record ignored., BaseItemCode=SFDR-24-51'
    - - :warning
      - 'Line 2097: Product not found, record ignored., BaseItemCode=SFDR-48-26'
    - - :warning
      - 'Line 2098: Product not found, record ignored., BaseItemCode=SFDR-48-51'
    - - :warning
      - 'Line 2099: Product not found, record ignored., BaseItemCode=SFDR-I-26'
    - - :warning
      - 'Line 2100: Product not found, record ignored., BaseItemCode=SFDR-I-51'
    - - :warning
      - 'Line 2106: Product not found, record ignored., BaseItemCode=SJ1012T24-RBL702R'
    - - :warning
      - 'Line 2107: Product not found, record ignored., BaseItemCode=SJ1012T24-RGO702R'
    - - :warning
      - 'Line 2108: Product not found, record ignored., BaseItemCode=SJ1012T24-RRE702R'
    - - :warning
      - 'Line 2122: Product not found, record ignored., BaseItemCode=SJ2310T24-RBL702R'
    - - :warning
      - 'Line 2123: Product not found, record ignored., BaseItemCode=SJ2310T24-RGO702R'
    - - :warning
      - 'Line 2124: Product not found, record ignored., BaseItemCode=SJ2310T24-RRE702R'
    - - :warning
      - 'Line 2139: Product not found, record ignored., BaseItemCode=SJ3611T24-RBL702R'
    - - :warning
      - 'Line 2140: Product not found, record ignored., BaseItemCode=SJ3611T24-RGO702R'
    - - :warning
      - 'Line 2141: Product not found, record ignored., BaseItemCode=SJ3611T24-RRE702R'
    - - :warning
      - 'Line 2172: Product not found, record ignored., BaseItemCode=SJ4914T24-RBL702R'
    - - :warning
      - 'Line 2173: Product not found, record ignored., BaseItemCode=SJ4914T24-RGO702R'
    - - :warning
      - 'Line 2174: Product not found, record ignored., BaseItemCode=SJ4914T24-RRE702R'
    - - :warning
      - 'Line 2254: Product not found, record ignored., BaseItemCode=SJ8813T24-RBL702R'
    - - :warning
      - 'Line 2255: Product not found, record ignored., BaseItemCode=SJ8813T24-RGO702R'
    - - :warning
      - 'Line 2256: Product not found, record ignored., BaseItemCode=SJ8813T24-RRE702R'
    - - :warning
      - 'Line 2423: Product not found, record ignored., BaseItemCode=WH-WS-WT'
- - Customers
  - - - :error
      - 'Line 1359: error=Validation failed: Shipping state can''t be blank: Customer
        # = 13172787'
- - Sales Data
  - - - :error
      - 'Line 42: Base item code SFCK-26 does not match an active product'
    - - :error
      - 'Line 43: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 105: Base item code 5685-80R does not match an active product'
    - - :error
      - 'Line 244: Base item code 1712U-76 does not match an active product'
    - - :error
      - 'Line 349: BillToCode (03983000) is invalid.'
    - - :error
      - 'Line 368: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 382: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 383: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 384: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 821: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 822: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 823: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 824: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 825: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 826: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 827: BillToCode (09371000) is invalid.'
    - - :error
      - 'Line 891: Base item code SF-RCBT-WT does not match an active product'
    - - :error
      - 'Line 892: Base item code SF-WCBT-WT does not match an active product'
    - - :error
      - 'Line 935: Base item code 1239-40A does not match an active product'
    - - :error
      - 'Line 985: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 1211: Base item code 1238N-48A does not match an active product'
    - - :error
      - 'Line 1212: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1423: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1427: Base item code 1248-22A does not match an active product'
    - - :error
      - 'Line 1461: Base item code 2124A does not match an active product'
    - - :error
      - 'Line 1463: Base item code 2995-40A does not match an active product'
    - - :error
      - 'Line 1464: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 1466: Base item code 3601-40A does not match an active product'
    - - :error
      - 'Line 1643: Base item code 1246-22A does not match an active product'
    - - :error
      - 'Line 1807: Base item code 1238N-22A does not match an active product'
    - - :error
      - 'Line 1812: Base item code 1239-76A does not match an active product'
    - - :error
      - 'Line 1816: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1818: Base item code 1241-22A does not match an active product'
    - - :error
      - 'Line 1828: Base item code 1243-22A does not match an active product'
    - - :error
      - 'Line 1830: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1916: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 2064: Base item code CM8519N-401A does not match an active product'
    - - :error
      - 'Line 2259: Base item code SFDR-18-26 does not match an active product'
    - - :error
      - 'Line 2260: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 2272: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2332: BillToCode (13171071) is invalid.'
    - - :error
      - 'Line 2495: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2496: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2566: BillToCode (13171471) is invalid.'
    - - :error
      - 'Line 2719: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2720: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2749: Base item code CM8326N-401A does not match an active product'
    - - :error
      - 'Line 2878: BillToCode (13172412) is invalid.'
    - - :error
      - 'Line 2879: BillToCode (13172412) is invalid.'
    - - :error
      - 'Line 2907: Base item code 1238N-48A does not match an active product'
    - - :warning
      - "-215 more rows with invalid products"
 |
| 2026-06-08T05:49:35.620771 | ---
- - Inventory
  - - - :warning
      - 'Line 5: Product not found, record ignored., BaseItemCode=1239-22A'
    - - :warning
      - 'Line 8: Product not found, record ignored., BaseItemCode=1239-23A'
    - - :warning
      - 'Line 13: Product not found, record ignored., BaseItemCode=1239-40A'
    - - :warning
      - 'Line 16: Product not found, record ignored., BaseItemCode=1239-48A'
    - - :warning
      - 'Line 19: Product not found, record ignored., BaseItemCode=1239-76A'
    - - :warning
      - 'Line 24: Product not found, record ignored., BaseItemCode=1240-22A'
    - - :warning
      - 'Line 27: Product not found, record ignored., BaseItemCode=1240-23A'
    - - :warning
      - 'Line 32: Product not found, record ignored., BaseItemCode=1240-40A'
    - - :warning
      - 'Line 35: Product not found, record ignored., BaseItemCode=1240-48A'
    - - :warning
      - 'Line 38: Product not found, record ignored., BaseItemCode=1240-76A'
    - - :warning
      - 'Line 41: Product not found, record ignored., BaseItemCode=1241-22A'
    - - :warning
      - 'Line 45: Product not found, record ignored., BaseItemCode=1241-48A'
    - - :warning
      - 'Line 48: Product not found, record ignored., BaseItemCode=1241-76A'
    - - :warning
      - 'Line 66: Product not found, record ignored., BaseItemCode=1243-22A'
    - - :warning
      - 'Line 69: Product not found, record ignored., BaseItemCode=1243-48A'
    - - :warning
      - 'Line 72: Product not found, record ignored., BaseItemCode=1243-76A'
    - - :warning
      - 'Line 81: Product not found, record ignored., BaseItemCode=1558-48R'
    - - :warning
      - 'Line 110: Product not found, record ignored., BaseItemCode=1701U-76'
    - - :warning
      - 'Line 119: Product not found, record ignored., BaseItemCode=1702U-76'
    - - :warning
      - 'Line 128: Product not found, record ignored., BaseItemCode=1703U-76'
    - - :warning
      - 'Line 133: Product not found, record ignored., BaseItemCode=1704U-76'
    - - :warning
      - 'Line 142: Product not found, record ignored., BaseItemCode=1712U-76'
    - - :warning
      - 'Line 145: Product not found, record ignored., BaseItemCode=2124A'
    - - :warning
      - 'Line 147: Product not found, record ignored., BaseItemCode=2220A'
    - - :warning
      - 'Line 150: Product not found, record ignored., BaseItemCode=2224A'
    - - :warning
      - 'Line 161: Product not found, record ignored., BaseItemCode=2274A'
    - - :warning
      - 'Line 175: Product not found, record ignored., BaseItemCode=2990-40A'
    - - :warning
      - 'Line 180: Product not found, record ignored., BaseItemCode=2991-40A'
    - - :warning
      - 'Line 213: Product not found, record ignored., BaseItemCode=3608-40A'
    - - :warning
      - 'Line 643: Product not found, record ignored., BaseItemCode=AT1001N-23H'
    - - :warning
      - 'Line 1114: Product not found, record ignored., BaseItemCode=CM8326N-401A'
    - - :warning
      - 'Line 1116: Product not found, record ignored., BaseItemCode=CM8334N-401A'
    - - :warning
      - 'Line 1119: Product not found, record ignored., BaseItemCode=CM8519N-401A'
    - - :warning
      - 'Line 1224: Product not found, record ignored., BaseItemCode=MD1005N-51H'
    - - :warning
      - 'Line 2090: Product not found, record ignored., BaseItemCode=SF-RCBT-WT'
    - - :warning
      - 'Line 2091: Product not found, record ignored., BaseItemCode=SF-WCBT-WT'
    - - :warning
      - 'Line 2092: Product not found, record ignored., BaseItemCode=SFCK-26'
    - - :warning
      - 'Line 2093: Product not found, record ignored., BaseItemCode=SFCK-51'
    - - :warning
      - 'Line 2094: Product not found, record ignored., BaseItemCode=SFDR-12-26'
    - - :warning
      - 'Line 2095: Product not found, record ignored., BaseItemCode=SFDR-12-51'
    - - :warning
      - 'Line 2096: Product not found, record ignored., BaseItemCode=SFDR-18-26'
    - - :warning
      - 'Line 2097: Product not found, record ignored., BaseItemCode=SFDR-18-51'
    - - :warning
      - 'Line 2098: Product not found, record ignored., BaseItemCode=SFDR-24-26'
    - - :warning
      - 'Line 2099: Product not found, record ignored., BaseItemCode=SFDR-24-51'
    - - :warning
      - 'Line 2100: Product not found, record ignored., BaseItemCode=SFDR-48-26'
    - - :warning
      - 'Line 2101: Product not found, record ignored., BaseItemCode=SFDR-48-51'
    - - :warning
      - 'Line 2102: Product not found, record ignored., BaseItemCode=SFDR-I-26'
    - - :warning
      - 'Line 2103: Product not found, record ignored., BaseItemCode=SFDR-I-51'
    - - :warning
      - 'Line 2109: Product not found, record ignored., BaseItemCode=SJ1012T24-RBL702R'
    - - :warning
      - 'Line 2110: Product not found, record ignored., BaseItemCode=SJ1012T24-RGO702R'
    - - :warning
      - 'Line 2111: Product not found, record ignored., BaseItemCode=SJ1012T24-RRE702R'
    - - :warning
      - 'Line 2125: Product not found, record ignored., BaseItemCode=SJ2310T24-RBL702R'
    - - :warning
      - 'Line 2126: Product not found, record ignored., BaseItemCode=SJ2310T24-RGO702R'
    - - :warning
      - 'Line 2127: Product not found, record ignored., BaseItemCode=SJ2310T24-RRE702R'
    - - :warning
      - 'Line 2142: Product not found, record ignored., BaseItemCode=SJ3611T24-RBL702R'
    - - :warning
      - 'Line 2143: Product not found, record ignored., BaseItemCode=SJ3611T24-RGO702R'
    - - :warning
      - 'Line 2144: Product not found, record ignored., BaseItemCode=SJ3611T24-RRE702R'
    - - :warning
      - 'Line 2174: Product not found, record ignored., BaseItemCode=SJ4914T24-RBL702R'
    - - :warning
      - 'Line 2175: Product not found, record ignored., BaseItemCode=SJ4914T24-RGO702R'
    - - :warning
      - 'Line 2176: Product not found, record ignored., BaseItemCode=SJ4914T24-RRE702R'
    - - :warning
      - 'Line 2256: Product not found, record ignored., BaseItemCode=SJ8813T24-RBL702R'
    - - :warning
      - 'Line 2257: Product not found, record ignored., BaseItemCode=SJ8813T24-RGO702R'
    - - :warning
      - 'Line 2258: Product not found, record ignored., BaseItemCode=SJ8813T24-RRE702R'
    - - :warning
      - 'Line 2425: Product not found, record ignored., BaseItemCode=WH-WS-WT'
- - Customers
  - - - :error
      - 'Line 1359: error=Validation failed: Shipping state can''t be blank: Customer
        # = 13172787'
- - Sales Data
  - - - :error
      - 'Line 41: Base item code SFCK-26 does not match an active product'
    - - :error
      - 'Line 42: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 104: Base item code 5685-80R does not match an active product'
    - - :error
      - 'Line 241: Base item code 1712U-76 does not match an active product'
    - - :error
      - 'Line 346: BillToCode (03983000) is invalid.'
    - - :error
      - 'Line 365: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 379: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 380: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 381: BillToCode (04561000) is invalid.'
    - - :error
      - 'Line 818: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 819: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 820: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 821: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 822: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 823: BillToCode (09115000) is invalid.'
    - - :error
      - 'Line 824: BillToCode (09371000) is invalid.'
    - - :error
      - 'Line 888: Base item code SF-RCBT-WT does not match an active product'
    - - :error
      - 'Line 889: Base item code SF-WCBT-WT does not match an active product'
    - - :error
      - 'Line 932: Base item code 1239-40A does not match an active product'
    - - :error
      - 'Line 982: Base item code 2642L-211O does not match an active product'
    - - :error
      - 'Line 1208: Base item code 1238N-48A does not match an active product'
    - - :error
      - 'Line 1209: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1420: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1424: Base item code 1248-22A does not match an active product'
    - - :error
      - 'Line 1458: Base item code 2124A does not match an active product'
    - - :error
      - 'Line 1460: Base item code 2995-40A does not match an active product'
    - - :error
      - 'Line 1461: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 1463: Base item code 3601-40A does not match an active product'
    - - :error
      - 'Line 1640: Base item code 1246-22A does not match an active product'
    - - :error
      - 'Line 1804: Base item code 1238N-22A does not match an active product'
    - - :error
      - 'Line 1809: Base item code 1239-76A does not match an active product'
    - - :error
      - 'Line 1813: Base item code 1240-48A does not match an active product'
    - - :error
      - 'Line 1815: Base item code 1241-22A does not match an active product'
    - - :error
      - 'Line 1825: Base item code 1243-22A does not match an active product'
    - - :error
      - 'Line 1827: Base item code 1243-23A does not match an active product'
    - - :error
      - 'Line 1913: Base item code 2998-40A does not match an active product'
    - - :error
      - 'Line 2061: Base item code CM8519N-401A does not match an active product'
    - - :error
      - 'Line 2255: Base item code SFDR-18-26 does not match an active product'
    - - :error
      - 'Line 2256: Base item code SFDR-24-26 does not match an active product'
    - - :error
      - 'Line 2268: BillToCode (13170513) is invalid.'
    - - :error
      - 'Line 2328: BillToCode (13171071) is invalid.'
    - - :error
      - 'Line 2491: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2492: BillToCode (13171384) is invalid.'
    - - :error
      - 'Line 2562: BillToCode (13171471) is invalid.'
    - - :error
      - 'Line 2715: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2716: BillToCode (13171732) is invalid.'
    - - :error
      - 'Line 2745: Base item code CM8326N-401A does not match an active product'
    - - :error
      - 'Line 2874: BillToCode (13172412) is invalid.'
    - - :error
      - 'Line 2875: BillToCode (13172412) is invalid.'
    - - :error
      - 'Line 2903: Base item code 1238N-48A does not match an active product'
    - - :warning
      - "-214 more rows with invalid products"
 |

### Q-10_results.md

# Q-10 Results — Schonbek Lighting (sbl, org_id=182)
- **Query**: Q-10 — Feature Enablement Gap Analysis
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-11_results.md

# Q-11 Results — Schonbek Lighting (sbl, org_id=182)
- **Query**: Q-11 — Configuration Completeness
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 19
- **Run date**: 2026-06-17


| entity_type | last_updated | days_stale | related_record_count |
| --- | --- | --- | --- |
| contract_prices | 2025-08-07 23:13:10 | 313 | 0 |
| kit_items | 2025-08-07 23:13:10 | 313 | 0 |
| matrix_options | 2025-08-07 23:13:10 | 313 | — |
| option_groups | 2025-08-07 23:13:10 | 313 | — |
| options | 2025-08-07 23:13:10 | 313 | — |
| commitment_reports | 2025-08-07 23:13:10 | 313 | — |
| placement_reports | 2025-08-07 23:13:10 | 313 | — |
| riser_prices | 2025-08-07 23:13:10 | 313 | — |
| customer_payment_informations | 2025-08-07 23:13:10 | 313 | — |
| sales_quotas | 2025-08-07 23:13:10 | 313 | 0 |
| price_levels | 2026-01-23 17:59:47 | 145 | — |
| portal_orders | 2026-03-13 14:23:41 | 96 | — |
| portal_invoices | 2026-03-13 14:23:41 | 96 | — |
| products | 2026-04-21 13:08:15 | 57 | — |
| smart_stacks | 2026-04-21 13:08:15 | 57 | — |
| categories | 2026-04-21 13:08:16 | 57 | — |
| collections | 2026-04-21 13:08:16 | 57 | — |
| groups | 2026-04-21 13:08:16 | 57 | — |
| trade_names | 2026-04-21 13:08:16 | 57 | — |

### Q-22_results.md

# Q-22 Results — Schonbek Lighting (sbl, org_id=182)
- **Query**: Q-22 — Feature Usage Depth
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | submit_order | select_a_customer | search_for_customer | email_item_info | create_pdf_catalog | view_library_entry | view_smartpicks | access_sales_portal | filter_products | search_products | search_collections | order_configured_item | view_kit | order_kit | share_my_list | export_data_to_csv | export_data_to_excel | total_events | total_users |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sbl | Schonbek Lighting | 257 | 4,189 | 3,867 | 37 | 169 | 3,450 | 41 | 0 | 231 | 15,048 | 527 | 0 | 0 | 0 | 11 | 0 | 0 | 43,416 | 118 |

### Q-CI-02_results.md

# Q-CI-02 Results — Schonbek Lighting (sbl, org_id=182)
- **Query**: Q-CI-02 — Peer Comparison
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | peer_standing | orders_vs_peer_pct | logins_vs_peer_pct | mrr_vs_peer_pct | peer_orders_median | peer_logins_median | peer_mrr_median |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sbl | Schonbek Lighting | Commerce-Active | On Track | 1.20 | 95.70 | 330.40 | 254 | 2,833 | 920 |

### Q-CI-03_results.md

# Q-CI-03 Results — Schonbek Lighting (sbl, org_id=182)
- **Query**: Q-CI-03 — Feature Adoption Benchmarking
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | feature_depth | has_clicky_portal | arr |
| --- | --- | --- | --- | --- | --- |
| sbl | Schonbek Lighting | Commerce-Active | 4 | 0 | 39,660 |

### Q-CI-03_benchmarks_results.md

# Q-CI-03-bench Results — Schonbek Lighting (sbl, org_id=182)
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
