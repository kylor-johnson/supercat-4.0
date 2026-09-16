# Section 6 Context Bundle — Coleto Brands | Progress Lighting (prog)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Coleto Brands | Progress Lighting (prog, org_id=286)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | False | portal_order_count=0, portal_order_gmv=$0 |
| HAS_INVENTORY | False | inventory_count=0 |
| HAS_SALES_DATA | False | sales_data_count=0 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=0 engagement_reps=14 (threshold: >=5) |
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
| QUALIFYING_REP_COUNT | 0 | 0 |
| ENGAGEMENT_REP_COUNT | 14 | engagement_reps=14 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 62 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 77, Mixpanel total submit_order (Q-01): 78 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=95.2%, ambiguous_rate=0.0%, showroom_event_share=1.9% |
| USER_GROUP_JOIN_RATE | 95% | 59 of 62 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 2% | showroom+admin share of matched events: 1.9% |
| ADMIN_REPS_IN_LEADERBOARD | True | 1 admin/showroom users in leaderboard: Michelle Miller |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False |  |
| PORTAL_REP_DATA_PRESENT | False |  |
| PORTAL_CUSTOMER_DATA_PRESENT | False |  |
| INVENTORY_FRESH | False | inventories not found in Q-08 data_versions |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | False | new_item_count=0 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | PARTIAL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | PARTIAL | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | PARTIAL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Coleto Brands | Progress Lighting
- **Shortname**: prog
- **Org ID**: 286
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- portal_orders LTM count=0, gmv=0.0 — HAS_PORTAL_ORDERS overridden to false

## Section Confidence

# Section Confidence Tiers — Coleto Brands | Progress Lighting (prog, org_id=286)
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
| HAS_INVENTORY | False |
| HAS_SALES_DATA | False |
| INVENTORY_FRESH | False |
| SALES_DATA_FRESH | False |
| CUSTOMER_DATA_FRESH | True |

## Computed Tiers

| Section | Tier | Determining Condition |
| --- | --- | --- |
| §2 Sales Team | STRONG | See Derived Gate 6 §2 formula |
| §3 Customer | PARTIAL | See Derived Gate 6 §3 formula |
| §4 Product | PARTIAL | See Derived Gate 6 §4 formula |
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

# Signal Rank — Coleto Brands | Progress Lighting (prog, org_id=286)
- **Run date**: 2026-06-17
- **Total signals fired**: 10 (P0: 0, P1: 2, P2: 8)
- **Org GMV**: $0.0M eCat LTM, $0.0M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 64% of eCat GMV | P1 | §4 Commerce | 1.6 | $88,456 | 2.0 | 285,248 | RISK |
| 2 | SIG-RISK-03 | Data Staleness — price_levels last updated 183d ago | P1 | §6 Platform | 2.0 | $1 | 2.0 | 4 | RISK |
| 3 | SIG-RISK-03 | Data Staleness — products last updated 126d ago | P2 | §6 Platform | 1.4 | $1 | 2.0 | 3 | RISK |
| 4 | SIG-RISK-03 | Data Staleness — smart_stacks last updated 126d ago | P2 | §6 Platform | 1.4 | $1 | 2.0 | 3 | RISK |
| 5 | SIG-RISK-03 | Data Staleness — categories last updated 126d ago | P2 | §6 Platform | 1.4 | $1 | 2.0 | 3 | RISK |
| 6 | SIG-RISK-03 | Data Staleness — collections last updated 126d ago | P2 | §6 Platform | 1.4 | $1 | 2.0 | 3 | RISK |
| 7 | SIG-RISK-03 | Data Staleness — groups last updated 126d ago | P2 | §6 Platform | 1.4 | $1 | 2.0 | 3 | RISK |
| 8 | SIG-RISK-03 | Data Staleness — trade_names last updated 126d ago | P2 | §6 Platform | 1.4 | $1 | 2.0 | 3 | RISK |
| 9 | SIG-RISK-03 | Data Staleness — portal_orders last updated 96d ago | P2 | §6 Platform | 1.1 | $1 | 2.0 | 2 | RISK |
| 10 | SIG-RISK-03 | Data Staleness — portal_invoices last updated 96d ago | P2 | §6 Platform | 1.1 | $1 | 2.0 | 2 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §4 Commerce Patterns | 0 | 1 | 0 | 1 | |
| §6 Platform Context | 0 | 1 | 8 | 9 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[RISK]** SIG-RISK-01: Revenue Concentration — top 5 accounts generate 64% of eCat GMV
2. **[RISK]** SIG-RISK-03: Data Staleness — price_levels last updated 183d ago
3. **[RISK]** SIG-RISK-03: Data Staleness — products last updated 126d ago
4. **[RISK]** SIG-RISK-03: Data Staleness — smart_stacks last updated 126d ago
5. **[RISK]** SIG-RISK-03: Data Staleness — categories last updated 126d ago
6. **[RISK]** SIG-RISK-03: Data Staleness — collections last updated 126d ago
7. **[RISK]** SIG-RISK-03: Data Staleness — groups last updated 126d ago

**Balance check**: 0 positive (slots 1-0), 7 risk (slots 1-7). Finding #1 is RISK. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-07_results.md

# Q-07 Results — Coleto Brands | Progress Lighting (prog, org_id=286)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| visible | 4,252 | 58 | 0 | 98.60 |

### Q-08_results.md

# Q-08 Results — Coleto Brands | Progress Lighting (prog, org_id=286)
- **Query**: Q-08 — Data Freshness Monitor
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| entity_type | last_updated | days_since_update | status |
| --- | --- | --- | --- |
| price_levels | 2025-12-16 18:01:50 | 183 | Stale |
| products | 2026-02-11 17:50:26 | 126 | Monitor |
| smart_stacks | 2026-02-11 17:50:27 | 126 | Monitor |
| categories | 2026-02-11 17:50:37 | 126 | Monitor |
| collections | 2026-02-11 17:50:37 | 126 | Monitor |
| groups | 2026-02-11 17:50:37 | 126 | Monitor |
| trade_names | 2026-02-11 17:50:37 | 126 | Monitor |
| portal_orders | 2026-03-13 14:23:47 | 96 | Monitor |
| portal_invoices | 2026-03-13 14:23:47 | 96 | Monitor |
| customers | 2026-06-17 12:05:29 | 0 | Fresh |

### Q-09_results.md

# Q-09 Results — Coleto Brands | Progress Lighting (prog, org_id=286)
- **Query**: Q-09 — Import Health — Monthly Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 5
- **Run date**: 2026-06-17


| month | import_count |
| --- | --- |
| 2026-06-01 | 5 |
| 2026-05-01 | 3 |
| 2026-02-01 | 4 |
| 2026-01-01 | 11 |
| 2025-12-01 | 125 |

### Q-09_recent_results.md

# Q-09-recent Results — Coleto Brands | Progress Lighting (prog, org_id=286)
- **Query**: Q-09-recent — Import Health — Recent Errors
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| created_at | data |
| --- | --- |
| 2026-06-17 12:05:29 | ---
- - Customers
  - []
 |
| 2026-06-16 20:11:15 | ---
- - Customers
  - - - :warning
      - 'Line 1: Field name BillTo_<customfield> is unknown.'
    - - :error
      - 'Line 1: Header field 17 is blank.'
    - - :error
      - 'Line 1: Header field 18 is blank.'
    - - :error
      - 'Line 1: Header field 19 is blank.'
    - - :error
      - 'Line 1: Header field 20 is blank.'
    - - :error
      - 'Line 1: Header field 21 is blank.'
 |
| 2026-06-16 20:03:25 | ---
- - Customers
  - - - :warning
      - 'Line 1: Field name BillTo_<customfield> is unknown.'
 |
| 2026-06-16 19:44:15 | ---
- - Customers
  - - - :warning
      - 'Line 1: Field name BillTo_<customfield> is unknown.'
    - - :error
      - 'Line 416: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202242'
    - - :error
      - 'Line 1308: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210988'
    - - :error
      - 'Line 1323: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211033'
    - - :error
      - 'Line 1332: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211054'
    - - :error
      - 'Line 1349: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211100'
    - - :error
      - 'Line 1350: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211118'
    - - :error
      - 'Line 1362: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211142'
    - - :error
      - 'Line 1366: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211154'
    - - :error
      - 'Line 1386: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211212'
    - - :error
      - 'Line 1388: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211226'
    - - :error
      - 'Line 1420: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211357'
    - - :error
      - 'Line 1450: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211440'
    - - :error
      - 'Line 1516: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249846'
    - - :error
      - 'Line 1810: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 264011'
    - - :error
      - 'Line 1816: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 264385'
    - - :error
      - 'Line 2001: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 286452'
    - - :error
      - 'Line 2030: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 288378'
    - - :error
      - 'Line 2078: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 292506'
    - - :error
      - 'Line 2079: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 292507'
    - - :error
      - 'Line 2080: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 292508'
    - - :error
      - 'Line 2081: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 292509'
    - - :error
      - 'Line 2099: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 294561'
    - - :error
      - 'Line 2168: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 306019'
    - - :error
      - 'Line 2178: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 306711'
    - - :error
      - 'Line 4139: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 253137'
    - - :error
      - 'Line 4270: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 262655'
    - - :error
      - 'Line 4318: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 266318'
    - - :error
      - 'Line 4745: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 321632'
    - - :error
      - 'Line 4809: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 326074'
 |
| 2026-06-16 19:00:50 | ---
- - Customers
  - - - :error
      - 'Line 1: Header field 2 is blank.'
    - - :warning
      - 'Line 1: Field name BillTo_<customfield> is unknown.'
    - - :error
      - 'Line 38: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200090'
    - - :error
      - 'Line 44: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200108'
    - - :error
      - 'Line 58: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200173'
    - - :error
      - 'Line 64: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200205'
    - - :error
      - 'Line 70: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200247'
    - - :error
      - 'Line 71: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200253'
    - - :error
      - 'Line 74: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200260'
    - - :error
      - 'Line 97: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200326'
    - - :error
      - 'Line 99: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200343'
    - - :error
      - 'Line 100: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200344'
    - - :error
      - 'Line 101: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200346'
    - - :error
      - 'Line 103: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200351'
    - - :error
      - 'Line 106: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200376'
    - - :error
      - 'Line 107: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200380'
    - - :error
      - 'Line 111: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200411'
    - - :error
      - 'Line 114: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200439'
    - - :error
      - 'Line 115: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200452'
    - - :error
      - 'Line 126: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200509'
    - - :error
      - 'Line 137: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200565'
    - - :error
      - 'Line 138: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200579'
    - - :error
      - 'Line 140: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200581'
    - - :error
      - 'Line 141: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200587'
    - - :error
      - 'Line 143: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200592'
    - - :error
      - 'Line 146: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200613'
    - - :error
      - 'Line 148: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200660'
    - - :error
      - 'Line 149: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200668'
    - - :error
      - 'Line 152: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200718'
    - - :error
      - 'Line 154: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200721'
    - - :error
      - 'Line 156: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200775'
    - - :error
      - 'Line 162: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200822'
    - - :error
      - 'Line 163: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200826'
    - - :error
      - 'Line 168: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200844'
    - - :error
      - 'Line 175: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200874'
    - - :error
      - 'Line 197: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200959'
    - - :error
      - 'Line 198: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200990'
    - - :error
      - 'Line 199: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200991'
    - - :error
      - 'Line 201: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201006'
    - - :error
      - 'Line 202: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201010'
    - - :error
      - 'Line 203: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201012'
    - - :error
      - 'Line 205: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201018'
    - - :error
      - 'Line 206: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201019'
    - - :error
      - 'Line 207: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201020'
    - - :error
      - 'Line 208: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201021'
    - - :error
      - 'Line 209: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201023'
    - - :error
      - 'Line 213: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201048'
    - - :error
      - 'Line 228: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201158'
    - - :error
      - 'Line 230: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201169'
    - - :error
      - 'Line 231: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201172'
    - - :error
      - 'Line 233: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201176'
    - - :error
      - 'Line 244: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201225'
    - - :error
      - 'Line 245: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201230'
    - - :error
      - 'Line 247: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201238'
    - - :error
      - 'Line 249: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201254'
    - - :error
      - 'Line 250: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201258'
    - - :error
      - 'Line 251: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201268'
    - - :error
      - 'Line 265: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201324'
    - - :error
      - 'Line 266: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201325'
    - - :error
      - 'Line 267: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201333'
    - - :error
      - 'Line 269: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201364'
    - - :error
      - 'Line 271: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201385'
    - - :error
      - 'Line 272: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201390'
    - - :error
      - 'Line 273: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201409'
    - - :error
      - 'Line 281: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201450'
    - - :error
      - 'Line 284: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201475'
    - - :error
      - 'Line 290: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201515'
    - - :error
      - 'Line 291: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201520'
    - - :error
      - 'Line 303: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201581'
    - - :error
      - 'Line 304: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201584'
    - - :error
      - 'Line 306: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201590'
    - - :error
      - 'Line 307: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201593'
    - - :error
      - 'Line 308: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201598'
    - - :error
      - 'Line 310: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201602'
    - - :error
      - 'Line 311: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201603'
    - - :error
      - 'Line 312: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201604'
    - - :error
      - 'Line 329: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201701'
    - - :error
      - 'Line 330: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201726'
    - - :error
      - 'Line 331: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201731'
    - - :error
      - 'Line 339: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201755'
    - - :error
      - 'Line 344: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201779'
    - - :error
      - 'Line 345: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201788'
    - - :error
      - 'Line 346: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201796'
    - - :error
      - 'Line 347: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201797'
    - - :error
      - 'Line 350: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201810'
    - - :error
      - 'Line 351: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201812'
    - - :error
      - 'Line 352: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201815'
    - - :error
      - 'Line 353: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201816'
    - - :error
      - 'Line 354: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201817'
    - - :error
      - 'Line 355: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201818'
    - - :error
      - 'Line 364: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201909'
    - - :error
      - 'Line 366: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202025'
    - - :error
      - 'Line 368: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202028'
    - - :error
      - 'Line 369: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202029'
    - - :error
      - 'Line 371: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202042'
    - - :error
      - 'Line 375: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202063'
    - - :error
      - 'Line 376: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202078'
    - - :error
      - 'Line 377: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202079'
    - - :error
      - 'Line 380: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202091'
    - - :error
      - 'Line 394: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202153'
    - - :error
      - 'Line 396: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202157'
    - - :error
      - 'Line 397: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202161'
    - - :error
      - 'Line 399: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202188'
    - - :error
      - 'Line 404: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202214'
    - - :error
      - 'Line 410: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202230'
    - - :error
      - 'Line 412: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202233'
    - - :error
      - 'Line 413: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202235'
    - - :error
      - 'Line 416: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202242'
    - - :error
      - 'Line 418: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202247'
    - - :error
      - 'Line 423: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202270'
    - - :error
      - 'Line 424: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202276'
    - - :error
      - 'Line 426: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202283'
    - - :error
      - 'Line 431: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202296'
    - - :error
      - 'Line 433: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202306'
    - - :error
      - 'Line 437: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202325'
    - - :error
      - 'Line 438: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202326'
    - - :error
      - 'Line 446: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202359'
    - - :error
      - 'Line 449: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202378'
    - - :error
      - 'Line 451: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202390'
    - - :error
      - 'Line 453: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202421'
    - - :error
      - 'Line 454: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202431'
    - - :error
      - 'Line 455: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202435'
    - - :error
      - 'Line 456: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202443'
    - - :error
      - 'Line 457: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202444'
    - - :error
      - 'Line 458: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202448'
    - - :error
      - 'Line 459: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202450'
    - - :error
      - 'Line 460: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202451'
    - - :error
      - 'Line 461: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202452'
    - - :error
      - 'Line 463: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202462'
    - - :error
      - 'Line 466: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202482'
    - - :error
      - 'Line 467: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202490'
    - - :error
      - 'Line 468: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202492'
    - - :error
      - 'Line 470: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202498'
    - - :error
      - 'Line 471: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202499'
    - - :error
      - 'Line 472: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202500'
    - - :error
      - 'Line 473: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202504'
    - - :error
      - 'Line 479: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202529'
    - - :error
      - 'Line 481: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202540'
    - - :error
      - 'Line 483: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202544'
    - - :error
      - 'Line 486: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202552'
    - - :error
      - 'Line 488: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202568'
    - - :error
      - 'Line 491: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202573'
    - - :error
      - 'Line 494: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202579'
    - - :error
      - 'Line 501: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202593'
    - - :error
      - 'Line 503: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202596'
    - - :error
      - 'Line 508: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202630'
    - - :error
      - 'Line 509: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202631'
    - - :error
      - 'Line 512: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202665'
    - - :error
      - 'Line 513: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202666'
    - - :error
      - 'Line 514: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202673'
    - - :error
      - 'Line 515: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202676'
    - - :error
      - 'Line 526: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202760'
    - - :error
      - 'Line 528: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202772'
    - - :error
      - 'Line 535: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202801'
    - - :error
      - 'Line 541: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202813'
    - - :error
      - 'Line 550: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202847'
    - - :error
      - 'Line 551: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202856'
    - - :error
      - 'Line 555: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202874'
    - - :error
      - 'Line 556: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202877'
    - - :error
      - 'Line 558: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202880'
    - - :error
      - 'Line 561: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202886'
    - - :error
      - 'Line 564: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202910'
    - - :error
      - 'Line 570: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202923'
    - - :error
      - 'Line 575: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202931'
    - - :error
      - 'Line 578: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202942'
    - - :error
      - 'Line 583: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202956'
    - - :error
      - 'Line 588: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202985'
    - - :error
      - 'Line 597: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203036'
    - - :error
      - 'Line 607: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203095'
    - - :error
      - 'Line 609: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203098'
    - - :error
      - 'Line 616: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203140'
    - - :error
      - 'Line 618: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203144'
    - - :error
      - 'Line 620: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203155'
    - - :error
      - 'Line 621: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203156'
    - - :error
      - 'Line 622: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203158'
    - - :error
      - 'Line 625: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203176'
    - - :error
      - 'Line 626: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203180'
    - - :error
      - 'Line 627: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203181'
    - - :error
      - 'Line 628: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203190'
    - - :error
      - 'Line 630: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203195'
    - - :error
      - 'Line 633: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203252'
    - - :error
      - 'Line 636: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203275'
    - - :error
      - 'Line 637: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203283'
    - - :error
      - 'Line 645: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203358'
    - - :error
      - 'Line 656: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203397'
    - - :error
      - 'Line 660: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203518'
    - - :error
      - 'Line 662: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203520'
    - - :error
      - 'Line 664: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203524'
    - - :error
      - 'Line 666: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203530'
    - - :error
      - 'Line 667: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203533'
    - - :error
      - 'Line 668: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203540'
    - - :error
      - 'Line 669: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203545'
    - - :error
      - 'Line 671: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203548'
    - - :error
      - 'Line 673: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203556'
    - - :error
      - 'Line 674: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203558'
    - - :error
      - 'Line 675: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203560'
    - - :error
      - 'Line 687: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203641'
    - - :error
      - 'Line 689: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203660'
    - - :error
      - 'Line 690: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203662'
    - - :error
      - 'Line 693: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203717'
    - - :error
      - 'Line 695: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203739'
    - - :error
      - 'Line 698: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203789'
    - - :error
      - 'Line 713: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203871'
    - - :error
      - 'Line 715: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203884'
    - - :error
      - 'Line 723: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203960'
    - - :error
      - 'Line 734: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204107'
    - - :error
      - 'Line 735: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204121'
    - - :error
      - 'Line 740: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204152'
    - - :error
      - 'Line 743: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204209'
    - - :error
      - 'Line 744: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204226'
    - - :error
      - 'Line 745: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204238'
    - - :error
      - 'Line 746: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204256'
    - - :error
      - 'Line 748: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204270'
    - - :error
      - 'Line 749: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204289'
    - - :error
      - 'Line 752: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204315'
    - - :error
      - 'Line 753: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204319'
    - - :error
      - 'Line 756: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204353'
    - - :error
      - 'Line 758: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204373'
    - - :error
      - 'Line 760: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204403'
    - - :error
      - 'Line 765: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204419'
    - - :error
      - 'Line 768: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204437'
    - - :error
      - 'Line 772: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204507'
    - - :error
      - 'Line 774: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204521'
    - - :error
      - 'Line 775: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204522'
    - - :error
      - 'Line 779: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204556'
    - - :error
      - 'Line 781: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204561'
    - - :error
      - 'Line 782: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204562'
    - - :error
      - 'Line 783: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204563'
    - - :error
      - 'Line 784: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204566'
    - - :error
      - 'Line 788: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204624'
    - - :error
      - 'Line 791: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204676'
    - - :error
      - 'Line 792: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204679'
    - - :error
      - 'Line 793: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204682'
    - - :error
      - 'Line 797: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204726'
    - - :error
      - 'Line 800: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204748'
    - - :error
      - 'Line 802: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204756'
    - - :error
      - 'Line 804: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204779'
    - - :error
      - 'Line 808: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204884'
    - - :error
      - 'Line 815: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204945'
    - - :error
      - 'Line 820: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204964'
    - - :error
      - 'Line 822: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205002'
    - - :error
      - 'Line 823: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205003'
    - - :error
      - 'Line 825: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205020'
    - - :error
      - 'Line 826: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205058'
    - - :error
      - 'Line 827: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205099'
    - - :error
      - 'Line 835: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205275'
    - - :error
      - 'Line 838: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205398'
    - - :error
      - 'Line 842: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205471'
    - - :error
      - 'Line 843: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205473'
    - - :error
      - 'Line 844: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205476'
    - - :error
      - 'Line 845: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205478'
    - - :error
      - 'Line 846: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205479'
    - - :error
      - 'Line 847: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205480'
    - - :error
      - 'Line 850: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205496'
    - - :error
      - 'Line 851: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205501'
    - - :error
      - 'Line 852: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205502'
    - - :error
      - 'Line 853: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205503'
    - - :error
      - 'Line 854: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205512'
    - - :error
      - 'Line 855: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205515'
    - - :error
      - 'Line 858: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205521'
    - - :error
      - 'Line 859: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205522'
    - - :error
      - 'Line 860: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205524'
    - - :error
      - 'Line 861: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205556'
    - - :error
      - 'Line 878: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206676'
    - - :error
      - 'Line 879: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206677'
    - - :error
      - 'Line 880: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206695'
    - - :error
      - 'Line 881: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206705'
    - - :error
      - 'Line 892: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206746'
    - - :error
      - 'Line 896: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206797'
    - - :error
      - 'Line 898: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206819'
    - - :error
      - 'Line 899: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206820'
    - - :error
      - 'Line 900: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206825'
    - - :error
      - 'Line 906: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206856'
    - - :error
      - 'Line 911: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206932'
    - - :error
      - 'Line 912: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206943'
    - - :error
      - 'Line 914: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206977'
    - - :error
      - 'Line 915: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206978'
    - - :error
      - 'Line 916: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207007'
    - - :error
      - 'Line 917: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207011'
    - - :error
      - 'Line 918: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207012'
    - - :error
      - 'Line 919: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207023'
    - - :error
      - 'Line 920: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207027'
    - - :error
      - 'Line 921: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207032'
    - - :error
      - 'Line 922: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207044'
    - - :error
      - 'Line 923: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207052'
    - - :error
      - 'Line 924: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207053'
    - - :error
      - 'Line 925: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207060'
    - - :error
      - 'Line 926: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207068'
    - - :error
      - 'Line 937: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207256'
    - - :error
      - 'Line 944: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207406'
    - - :error
      - 'Line 946: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207491'
    - - :error
      - 'Line 954: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207797'
    - - :error
      - 'Line 965: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207814'
    - - :error
      - 'Line 967: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207838'
    - - :error
      - 'Line 969: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207877'
    - - :error
      - 'Line 970: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207878'
    - - :error
      - 'Line 971: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207879'
    - - :error
      - 'Line 972: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207882'
    - - :error
      - 'Line 975: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207949'
    - - :error
      - 'Line 977: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207980'
    - - :error
      - 'Line 978: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207983'
    - - :error
      - 'Line 980: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208074'
    - - :error
      - 'Line 985: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208364'
    - - :error
      - 'Line 987: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208392'
    - - :error
      - 'Line 988: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208393'
    - - :error
      - 'Line 989: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208395'
    - - :error
      - 'Line 990: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208396'
    - - :error
      - 'Line 995: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208483'
    - - :error
      - 'Line 997: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208512'
    - - :error
      - 'Line 999: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208533'
    - - :error
      - 'Line 1000: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208553'
    - - :error
      - 'Line 1002: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208604'
    - - :error
      - 'Line 1003: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208654'
    - - :error
      - 'Line 1004: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208661'
    - - :error
      - 'Line 1005: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208663'
    - - :error
      - 'Line 1006: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208664'
    - - :error
      - 'Line 1007: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208668'
    - - :error
      - 'Line 1010: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208731'
    - - :error
      - 'Line 1019: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209060'
    - - :error
      - 'Line 1030: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209123'
    - - :error
      - 'Line 1034: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209178'
    - - :error
      - 'Line 1035: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209179'
    - - :error
      - 'Line 1036: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209180'
    - - :error
      - 'Line 1037: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209191'
    - - :error
      - 'Line 1038: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209195'
    - - :error
      - 'Line 1039: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209198'
    - - :error
      - 'Line 1040: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209199'
    - - :error
      - 'Line 1041: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209201'
    - - :error
      - 'Line 1042: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209202'
    - - :error
      - 'Line 1043: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209206'
    - - :error
      - 'Line 1044: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209219'
    - - :error
      - 'Line 1045: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209258'
    - - :error
      - 'Line 1046: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209263'
    - - :error
      - 'Line 1051: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209290'
    - - :error
      - 'Line 1052: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209294'
    - - :error
      - 'Line 1055: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209331'
    - - :error
      - 'Line 1056: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209333'
    - - :error
      - 'Line 1057: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209341'
    - - :error
      - 'Line 1060: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209362'
    - - :error
      - 'Line 1066: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209401'
    - - :error
      - 'Line 1068: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209417'
    - - :error
      - 'Line 1069: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209421'
    - - :error
      - 'Line 1071: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209434'
    - - :error
      - 'Line 1075: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209445'
    - - :error
      - 'Line 1077: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209463'
    - - :error
      - 'Line 1080: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209499'
    - - :error
      - 'Line 1081: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209500'
    - - :error
      - 'Line 1083: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209505'
    - - :error
      - 'Line 1084: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209508'
    - - :error
      - 'Line 1086: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209517'
    - - :error
      - 'Line 1087: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209525'
    - - :error
      - 'Line 1088: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209526'
    - - :error
      - 'Line 1089: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209527'
    - - :error
      - 'Line 1090: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209528'
    - - :error
      - 'Line 1093: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209540'
    - - :error
      - 'Line 1094: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209543'
    - - :error
      - 'Line 1100: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209590'
    - - :error
      - 'Line 1101: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209601'
    - - :error
      - 'Line 1118: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209645'
    - - :error
      - 'Line 1119: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209648'
    - - :error
      - 'Line 1120: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209649'
    - - :error
      - 'Line 1121: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209650'
    - - :error
      - 'Line 1122: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209656'
    - - :error
      - 'Line 1123: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209660'
    - - :error
      - 'Line 1124: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209665'
    - - :error
      - 'Line 1125: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209666'
    - - :error
      - 'Line 1128: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209690'
    - - :error
      - 'Line 1129: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209712'
    - - :error
      - 'Line 1136: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209733'
    - - :error
      - 'Line 1138: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209745'
    - - :error
      - 'Line 1140: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209765'
    - - :error
      - 'Line 1141: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209766'
    - - :error
      - 'Line 1144: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209786'
    - - :error
      - 'Line 1147: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209800'
    - - :error
      - 'Line 1149: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209823'
    - - :error
      - 'Line 1153: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209837'
    - - :error
      - 'Line 1159: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209880'
    - - :error
      - 'Line 1160: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209891'
    - - :error
      - 'Line 1161: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209894'
    - - :error
      - 'Line 1162: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209895'
    - - :error
      - 'Line 1163: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209900'
    - - :error
      - 'Line 1166: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209925'
    - - :error
      - 'Line 1177: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209957'
    - - :error
      - 'Line 1179: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209969'
    - - :error
      - 'Line 1182: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210016'
    - - :error
      - 'Line 1184: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210025'
    - - :error
      - 'Line 1188: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210057'
    - - :error
      - 'Line 1192: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210076'
    - - :error
      - 'Line 1211: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210118'
    - - :error
      - 'Line 1213: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210122'
    - - :error
      - 'Line 1214: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210130'
    - - :error
      - 'Line 1230: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210305'
    - - :error
      - 'Line 1237: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210356'
    - - :error
      - 'Line 1244: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210407'
    - - :error
      - 'Line 1245: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210408'
    - - :error
      - 'Line 1265: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210542'
    - - :error
      - 'Line 1267: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210553'
    - - :error
      - 'Line 1277: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210634'
    - - :error
      - 'Line 1278: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210635'
    - - :error
      - 'Line 1283: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210678'
    - - :error
      - 'Line 1284: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210696'
    - - :error
      - 'Line 1296: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210880'
    - - :error
      - 'Line 1308: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210988'
    - - :error
      - 'Line 1323: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211033'
    - - :error
      - 'Line 1328: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211047'
    - - :error
      - 'Line 1329: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211049'
    - - :error
      - 'Line 1330: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211050'
    - - :error
      - 'Line 1332: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211054'
    - - :error
      - 'Line 1338: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211069'
    - - :error
      - 'Line 1345: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211085'
    - - :error
      - 'Line 1349: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211100'
    - - :error
      - 'Line 1350: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211118'
    - - :error
      - 'Line 1358: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211134'
    - - :error
      - 'Line 1362: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211142'
    - - :error
      - 'Line 1366: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211154'
    - - :error
      - 'Line 1368: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211160'
    - - :error
      - 'Line 1386: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211212'
    - - :error
      - 'Line 1388: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211226'
    - - :error
      - 'Line 1413: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211341'
    - - :error
      - 'Line 1420: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211357'
    - - :error
      - 'Line 1438: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211413'
    - - :error
      - 'Line 1439: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211414'
    - - :error
      - 'Line 1441: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211419'
    - - :error
      - 'Line 1443: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211422'
    - - :error
      - 'Line 1445: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211429'
    - - :error
      - 'Line 1447: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211432'
    - - :error
      - 'Line 1449: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211438'
    - - :error
      - 'Line 1450: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211440'
    - - :error
      - 'Line 1451: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211444'
    - - :error
      - 'Line 1452: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211446'
    - - :error
      - 'Line 1454: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211460'
    - - :error
      - 'Line 1465: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211847'
    - - :error
      - 'Line 1467: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211858'
    - - :error
      - 'Line 1471: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211910'
    - - :error
      - 'Line 1474: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211981'
    - - :error
      - 'Line 1477: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 228408'
    - - :error
      - 'Line 1478: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 247934'
    - - :error
      - 'Line 1479: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 247949'
    - - :error
      - 'Line 1480: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 247994'
    - - :error
      - 'Line 1481: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 248005'
    - - :error
      - 'Line 1487: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 248125'
    - - :error
      - 'Line 1488: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 248141'
    - - :error
      - 'Line 1489: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 248149'
    - - :error
      - 'Line 1490: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 248174'
    - - :error
      - 'Line 1493: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249501'
    - - :error
      - 'Line 1497: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249612'
    - - :error
      - 'Line 1500: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249638'
    - - :error
      - 'Line 1502: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249653'
    - - :error
      - 'Line 1505: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249674'
    - - :error
      - 'Line 1506: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249709'
    - - :error
      - 'Line 1510: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249772'
    - - :error
      - 'Line 1515: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249806'
    - - :error
      - 'Line 1516: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249846'
    - - :error
      - 'Line 1520: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249967'
    - - :error
      - 'Line 1525: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250016'
    - - :error
      - 'Line 1530: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250098'
    - - :error
      - 'Line 1532: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250131'
    - - :error
      - 'Line 1533: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250156'
    - - :error
      - 'Line 1534: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250179'
    - - :error
      - 'Line 1535: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250183'
    - - :error
      - 'Line 1538: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250238'
    - - :error
      - 'Line 1539: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250240'
    - - :error
      - 'Line 1540: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250244'
    - - :error
      - 'Line 1542: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250281'
    - - :error
      - 'Line 1549: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250331'
    - - :error
      - 'Line 1551: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250333'
    - - :error
      - 'Line 1552: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250343'
    - - :error
      - 'Line 1553: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250347'
    - - :error
      - 'Line 1556: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250372'
    - - :error
      - 'Line 1562: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250439'
    - - :error
      - 'Line 1563: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250440'
    - - :error
      - 'Line 1564: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250441'
    - - :error
      - 'Line 1565: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250442'
    - - :error
      - 'Line 1566: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250443'
    - - :error
      - 'Line 1567: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250444'
    - - :error
      - 'Line 1568: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250445'
    - - :error
      - 'Line 1571: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250450'
    - - :error
      - 'Line 1577: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250560'
    - - :error
      - 'Line 1578: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250672'
    - - :error
      - 'Line 1580: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250723'
    - - :error
      - 'Line 1581: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250724'
    - - :error
      - 'Line 1582: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250737'
    - - :error
      - 'Line 1583: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250743'
    - - :error
      - 'Line 1584: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250756'
    - - :error
      - 'Line 1585: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250757'
    - - :error
      - 'Line 1586: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250771'
    - - :error
      - 'Line 1587: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250795'
    - - :error
      - 'Line 1593: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250867'
    - - :error
      - 'Line 1594: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250868'
    - - :error
      - 'Line 1595: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250869'
    - - :error
      - 'Line 1599: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250908'
    - - :error
      - 'Line 1601: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250918'
    - - :error
      - 'Line 1610: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 251105'
    - - :error
      - 'Line 1614: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 251154'
    - - :error
      - 'Line 1634: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 251956'
    - - :error
      - 'Line 1636: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252069'
    - - :error
      - 'Line 1649: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252456'
    - - :error
      - 'Line 1652: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252472'
    - - :error
      - 'Line 1653: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252494'
    - - :error
      - 'Line 1659: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252556'
    - - :error
      - 'Line 1664: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252702'
    - - :error
      - 'Line 1676: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 253351'
    - - :error
      - 'Line 1682: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 254368'
    - - :error
      - 'Line 1691: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 256080'
    - - :error
      - 'Line 1700: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 256696'
    - - :error
      - 'Line 1712: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 257135'
    - - :error
      - 'Line 1716: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 257331'
    - - :error
      - 'Line 1725: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 257752'
    - - :error
      - 'Line 1730: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 258054'
    - - :error
      - 'Line 1740: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 258934'
    - - :error
      - 'Line 1745: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 259163'
    - - :error
      - 'Line 1752: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 259435'
    - - :error
      - 'Line 1759: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 259981'
    - - :error
      - 'Line 1767: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 260736'
    - - :error
      - 'Line 1771: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 260872'
    - - :error
      - 'Line 1773: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 261046'
    - - :error
      - 'Line 1779: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 262012'
    - - :error
      - 'Line 1780: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 262019'
    - - :error
      - 'Line 1781: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 262102'
    - - :error
      - 'Line 1782: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 262183'
    - - :error
      - 'Line 1790: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 262490'
    - - :error
      - 'Line 1793: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 262657'
    - - :error
      - 'Line 1804: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 263394'
    - - :error
      - 'Line 1810: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 264011'
    - - :error
      - 'Line 1816: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 264385'
    - - :error
      - 'Line 1823: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 264695'
    - - :error
      - 'Line 1832: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 265771'
    - - :error
      - 'Line 1851: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 266612'
    - - :error
      - 'Line 1855: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 266795'
    - - :error
      - 'Line 1856: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 266796'
    - - :error
      - 'Line 1857: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 266797'
    - - :error
      - 'Line 1865: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 267082'
    - - :error
      - 'Line 1895: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 269320'
    - - :error
      - 'Line 1908: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 269881'
    - - :error
      - 'Line 1923: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 271149'
    - - :error
      - 'Line 1925: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 274875'
    - - :error
      - 'Line 1945: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 279101'
    - - :error
      - 'Line 1946: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 279110'
    - - :error
      - 'Line 1948: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 279232'
    - - :error
      - 'Line 1957: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 281693'
    - - :error
      - 'Line 1967: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 283907'
    - - :error
      - 'Line 1970: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 284044'
    - - :error
      - 'Line 1971: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 284228'
    - - :error
      - 'Line 1974: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 284431'
    - - :error
      - 'Line 1980: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 284911'
    - - :error
      - 'Line 1981: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 284912'
    - - :error
      - 'Line 1985: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 285496'
    - - :error
      - 'Line 1991: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 285901'
    - - :error
      - 'Line 1995: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 286073'
    - - :error
      - 'Line 1997: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 286249'
    - - :error
      - 'Line 2001: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 286452'
    - - :error
      - 'Line 2002: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 286474'
    - - :error
      - 'Line 2026: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 287880'
    - - :error
      - 'Line 2030: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 288378'
    - - :error
      - 'Line 2034: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 288885'
    - - :error
      - 'Line 2037: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 289370'
    - - :error
      - 'Line 2056: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 290644'
    - - :error
      - 'Line 2058: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 291336'
    - - :error
      - 'Line 2062: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 291429'
    - - :error
      - 'Line 2070: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 292163'
    - - :error
      - 'Line 2078: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 292506'
    - - :error
      - 'Line 2079: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 292507'
    - - :error
      - 'Line 2080: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 292508'
    - - :error
      - 'Line 2081: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 292509'
    - - :error
      - 'Line 2095: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 294134'
    - - :error
      - 'Line 2098: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 294534'
    - - :error
      - 'Line 2099: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 294561'
    - - :error
      - 'Line 2100: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 294576'
    - - :error
      - 'Line 2102: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 295241'
    - - :error
      - 'Line 2103: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 295242'
    - - :error
      - 'Line 2108: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 295434'
    - - :error
      - 'Line 2110: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 295585'
    - - :error
      - 'Line 2113: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 297805'
    - - :error
      - 'Line 2119: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 298373'
    - - :error
      - 'Line 2121: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 298456'
    - - :error
      - 'Line 2123: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 298576'
    - - :error
      - 'Line 2144: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 302193'
    - - :error
      - 'Line 2148: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 302937'
    - - :error
      - 'Line 2149: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 303339'
    - - :error
      - 'Line 2150: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 303340'
    - - :error
      - 'Line 2155: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 304558'
    - - :error
      - 'Line 2161: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 305524'
    - - :error
      - 'Line 2166: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 305731'
    - - :error
      - 'Line 2167: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 305892'
    - - :error
      - 'Line 2168: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 306019'
    - - :error
      - 'Line 2176: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 306466'
    - - :error
      - 'Line 2178: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 306711'
    - - :error
      - 'Line 2182: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 306866'
    - - :error
      - 'Line 2184: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 306923'
    - - :error
      - 'Line 2185: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 306925'
    - - :error
      - 'Line 2187: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 306952'
    - - :error
      - 'Line 2188: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 307074'
    - - :error
      - 'Line 2193: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 307978'
    - - :error
      - 'Line 2194: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 308134'
    - - :error
      - 'Line 2195: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 308192'
    - - :error
      - 'Line 2198: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 308531'
    - - :error
      - 'Line 2211: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 310797'
    - - :error
      - 'Line 2212: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 311221'
    - - :error
      - 'Line 2216: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 311739'
    - - :error
      - 'Line 2219: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 311885'
    - - :error
      - 'Line 2222: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 312065'
    - - :error
      - 'Line 2238: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 313365'
    - - :error
      - 'Line 2242: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 313516'
    - - :error
      - 'Line 2264: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 314931'
    - - :error
      - 'Line 2272: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 315225'
    - - :error
      - 'Line 2291: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 315782'
    - - :error
      - 'Line 2306: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 318848'
    - - :error
      - 'Line 2320: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 319076'
    - - :error
      - 'Line 2322: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 319575'
    - - :error
      - 'Line 2323: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 319580'
    - - :error
      - 'Line 2335: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 319884'
    - - :error
      - 'Line 2343: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 320132'
    - - :error
      - 'Line 2345: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 320152'
    - - :error
      - 'Line 2346: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 320153'
    - - :error
      - 'Line 2347: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 320155'
    - - :error
      - 'Line 2352: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 320225'
    - - :error
      - 'Line 2353: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 320284'
    - - :error
      - 'Line 2361: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 320595'
    - - :error
      - 'Line 2363: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 320633'
    - - :error
      - 'Line 2364: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 320640'
    - - :error
      - 'Line 2365: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 320694'
    - - :error
      - 'Line 2379: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 321244'
    - - :error
      - 'Line 2384: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 321337'
    - - :error
      - 'Line 2387: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 321470'
    - - :error
      - 'Line 2390: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 321512'
    - - :error
      - 'Line 2402: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 321795'
    - - :error
      - 'Line 2405: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 321890'
    - - :error
      - 'Line 2406: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 321891'
    - - :error
      - 'Line 2412: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 323578'
    - - :error
      - 'Line 2424: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 324432'
    - - :error
      - 'Line 2439: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 325350'
    - - :error
      - 'Line 2445: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 325510'
    - - :error
      - 'Line 2446: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 325519'
    - - :error
      - 'Line 2447: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 325529'
    - - :error
      - 'Line 2458: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 326390'
    - - :error
      - 'Line 2473: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 327787'
    - - :error
      - 'Line 2508: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 329861'
    - - :error
      - 'Line 2531: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 331754'
    - - :error
      - 'Line 2538: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 331997'
    - - :error
      - 'Line 2545: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 332690'
    - - :error
      - 'Line 2547: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 332739'
    - - :error
      - 'Line 2554: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 332819'
    - - :error
      - 'Line 2560: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 333086'
    - - :error
      - 'Line 2564: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 333266'
    - - :error
      - 'Line 2579: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 334418'
    - - :error
      - 'Line 2592: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 335305'
    - - :error
      - 'Line 2595: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 335854'
    - - :error
      - 'Line 2599: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 336127'
    - - :error
      - 'Line 2799: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 338327'
    - - :error
      - 'Line 2801: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 338579'
    - - :error
      - 'Line 2824: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 340815'
    - - :error
      - 'Line 2828: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 340936'
    - - :error
      - 'Line 2841: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 342091'
    - - :error
      - 'Line 2848: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 342249'
    - - :error
      - 'Line 2852: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 342255'
    - - :error
      - 'Line 2854: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 342260'
    - - :error
      - 'Line 2862: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 342288'
    - - :error
      - 'Line 2863: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 342289'
    - - :error
      - 'Line 2864: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 342290'
    - - :error
      - 'Line 2879: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 342310'
    - - :error
      - 'Line 2882: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 342340'
    - - :error
      - 'Line 2883: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 342341'
    - - :error
      - 'Line 2893: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 342448'
    - - :error
      - 'Line 2896: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 342460'
    - - :error
      - 'Line 2902: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 342475'
    - - :error
      - 'Line 2903: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 342476'
    - - :error
      - 'Line 2959: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200013'
    - - :error
      - 'Line 2988: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200106'
    - - :error
      - 'Line 3004: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200212'
    - - :error
      - 'Line 3005: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200213'
    - - :error
      - 'Line 3007: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200224'
    - - :error
      - 'Line 3008: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200228'
    - - :error
      - 'Line 3015: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200274'
    - - :error
      - 'Line 3019: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200353'
    - - :error
      - 'Line 3026: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200377'
    - - :error
      - 'Line 3027: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200387'
    - - :error
      - 'Line 3028: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200388'
    - - :error
      - 'Line 3029: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200389'
    - - :error
      - 'Line 3038: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200423'
    - - :error
      - 'Line 3049: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200519'
    - - :error
      - 'Line 3060: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200583'
    - - :error
      - 'Line 3067: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200606'
    - - :error
      - 'Line 3068: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200607'
    - - :error
      - 'Line 3069: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200608'
    - - :error
      - 'Line 3078: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200637'
    - - :error
      - 'Line 3081: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200659'
    - - :error
      - 'Line 3082: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200664'
    - - :error
      - 'Line 3096: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200713'
    - - :error
      - 'Line 3108: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200778'
    - - :error
      - 'Line 3109: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200801'
    - - :error
      - 'Line 3121: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200926'
    - - :error
      - 'Line 3122: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200927'
    - - :error
      - 'Line 3123: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200928'
    - - :error
      - 'Line 3124: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200929'
    - - :error
      - 'Line 3125: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200931'
    - - :error
      - 'Line 3126: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200933'
    - - :error
      - 'Line 3127: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200936'
    - - :error
      - 'Line 3128: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200938'
    - - :error
      - 'Line 3129: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200940'
    - - :error
      - 'Line 3130: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200941'
    - - :error
      - 'Line 3131: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200942'
    - - :error
      - 'Line 3135: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200962'
    - - :error
      - 'Line 3136: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200963'
    - - :error
      - 'Line 3137: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200964'
    - - :error
      - 'Line 3138: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200965'
    - - :error
      - 'Line 3139: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200967'
    - - :error
      - 'Line 3140: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200968'
    - - :error
      - 'Line 3141: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200969'
    - - :error
      - 'Line 3142: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200971'
    - - :error
      - 'Line 3143: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200972'
    - - :error
      - 'Line 3144: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200973'
    - - :error
      - 'Line 3145: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200974'
    - - :error
      - 'Line 3147: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 200983'
    - - :error
      - 'Line 3155: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201004'
    - - :error
      - 'Line 3160: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201037'
    - - :error
      - 'Line 3161: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201047'
    - - :error
      - 'Line 3162: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201050'
    - - :error
      - 'Line 3163: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201058'
    - - :error
      - 'Line 3164: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201060'
    - - :error
      - 'Line 3170: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201090'
    - - :error
      - 'Line 3171: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201108'
    - - :error
      - 'Line 3172: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201110'
    - - :error
      - 'Line 3174: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201130'
    - - :error
      - 'Line 3179: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201197'
    - - :error
      - 'Line 3185: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201266'
    - - :error
      - 'Line 3191: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201290'
    - - :error
      - 'Line 3193: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201315'
    - - :error
      - 'Line 3195: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201327'
    - - :error
      - 'Line 3196: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201328'
    - - :error
      - 'Line 3199: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201347'
    - - :error
      - 'Line 3202: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201396'
    - - :error
      - 'Line 3206: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201425'
    - - :error
      - 'Line 3238: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201636'
    - - :error
      - 'Line 3242: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201662'
    - - :error
      - 'Line 3246: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201691'
    - - :error
      - 'Line 3261: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 201789'
    - - :error
      - 'Line 3275: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202033'
    - - :error
      - 'Line 3279: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202049'
    - - :error
      - 'Line 3284: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202076'
    - - :error
      - 'Line 3285: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202077'
    - - :error
      - 'Line 3286: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202100'
    - - :error
      - 'Line 3292: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202128'
    - - :error
      - 'Line 3294: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202145'
    - - :error
      - 'Line 3296: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202159'
    - - :error
      - 'Line 3300: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202199'
    - - :error
      - 'Line 3302: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202215'
    - - :error
      - 'Line 3305: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202240'
    - - :error
      - 'Line 3311: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202267'
    - - :error
      - 'Line 3319: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202331'
    - - :error
      - 'Line 3321: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202345'
    - - :error
      - 'Line 3325: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202367'
    - - :error
      - 'Line 3330: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202418'
    - - :error
      - 'Line 3331: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202434'
    - - :error
      - 'Line 3339: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202503'
    - - :error
      - 'Line 3342: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202514'
    - - :error
      - 'Line 3343: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202517'
    - - :error
      - 'Line 3351: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202581'
    - - :error
      - 'Line 3354: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202614'
    - - :error
      - 'Line 3358: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202620'
    - - :error
      - 'Line 3361: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202641'
    - - :error
      - 'Line 3362: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202646'
    - - :error
      - 'Line 3371: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202700'
    - - :error
      - 'Line 3372: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202704'
    - - :error
      - 'Line 3373: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202714'
    - - :error
      - 'Line 3379: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202755'
    - - :error
      - 'Line 3380: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202756'
    - - :error
      - 'Line 3382: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202780'
    - - :error
      - 'Line 3384: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202815'
    - - :error
      - 'Line 3387: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202836'
    - - :error
      - 'Line 3388: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202839'
    - - :error
      - 'Line 3392: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202846'
    - - :error
      - 'Line 3395: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202863'
    - - :error
      - 'Line 3398: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202887'
    - - :error
      - 'Line 3403: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202917'
    - - :error
      - 'Line 3405: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202922'
    - - :error
      - 'Line 3407: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202939'
    - - :error
      - 'Line 3417: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 202986'
    - - :error
      - 'Line 3423: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203048'
    - - :error
      - 'Line 3430: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203116'
    - - :error
      - 'Line 3431: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203169'
    - - :error
      - 'Line 3439: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203199'
    - - :error
      - 'Line 3440: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203201'
    - - :error
      - 'Line 3444: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203230'
    - - :error
      - 'Line 3445: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203238'
    - - :error
      - 'Line 3449: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203246'
    - - :error
      - 'Line 3454: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203262'
    - - :error
      - 'Line 3458: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203289'
    - - :error
      - 'Line 3466: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203352'
    - - :error
      - 'Line 3472: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203413'
    - - :error
      - 'Line 3474: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203532'
    - - :error
      - 'Line 3477: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203570'
    - - :error
      - 'Line 3478: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203586'
    - - :error
      - 'Line 3484: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203609'
    - - :error
      - 'Line 3485: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203610'
    - - :error
      - 'Line 3487: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203644'
    - - :error
      - 'Line 3505: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203911'
    - - :error
      - 'Line 3508: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203957'
    - - :error
      - 'Line 3509: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 203961'
    - - :error
      - 'Line 3517: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204109'
    - - :error
      - 'Line 3518: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204120'
    - - :error
      - 'Line 3519: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204144'
    - - :error
      - 'Line 3525: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204237'
    - - :error
      - 'Line 3536: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204339'
    - - :error
      - 'Line 3539: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204357'
    - - :error
      - 'Line 3544: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204477'
    - - :error
      - 'Line 3546: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204499'
    - - :error
      - 'Line 3551: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204553'
    - - :error
      - 'Line 3555: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204612'
    - - :error
      - 'Line 3559: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204671'
    - - :error
      - 'Line 3560: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204692'
    - - :error
      - 'Line 3561: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204693'
    - - :error
      - 'Line 3567: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204716'
    - - :error
      - 'Line 3568: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204720'
    - - :error
      - 'Line 3569: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204832'
    - - :error
      - 'Line 3572: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204927'
    - - :error
      - 'Line 3573: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 204939'
    - - :error
      - 'Line 3576: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205035'
    - - :error
      - 'Line 3577: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205067'
    - - :error
      - 'Line 3579: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205128'
    - - :error
      - 'Line 3582: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205167'
    - - :error
      - 'Line 3587: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205428'
    - - :error
      - 'Line 3588: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205429'
    - - :error
      - 'Line 3589: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205432'
    - - :error
      - 'Line 3593: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205458'
    - - :error
      - 'Line 3594: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205468'
    - - :error
      - 'Line 3595: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205475'
    - - :error
      - 'Line 3597: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205482'
    - - :error
      - 'Line 3598: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205489'
    - - :error
      - 'Line 3599: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205491'
    - - :error
      - 'Line 3600: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205494'
    - - :error
      - 'Line 3601: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205495'
    - - :error
      - 'Line 3608: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205519'
    - - :error
      - 'Line 3611: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205534'
    - - :error
      - 'Line 3613: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205537'
    - - :error
      - 'Line 3614: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205538'
    - - :error
      - 'Line 3615: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205539'
    - - :error
      - 'Line 3616: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205540'
    - - :error
      - 'Line 3617: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205544'
    - - :error
      - 'Line 3618: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205558'
    - - :error
      - 'Line 3624: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205586'
    - - :error
      - 'Line 3625: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205591'
    - - :error
      - 'Line 3626: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 205739'
    - - :error
      - 'Line 3641: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206725'
    - - :error
      - 'Line 3642: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206748'
    - - :error
      - 'Line 3650: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206807'
    - - :error
      - 'Line 3656: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206885'
    - - :error
      - 'Line 3668: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206939'
    - - :error
      - 'Line 3672: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206961'
    - - :error
      - 'Line 3673: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 206996'
    - - :error
      - 'Line 3674: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207016'
    - - :error
      - 'Line 3678: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207072'
    - - :error
      - 'Line 3679: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207101'
    - - :error
      - 'Line 3680: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207106'
    - - :error
      - 'Line 3682: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207169'
    - - :error
      - 'Line 3683: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207170'
    - - :error
      - 'Line 3689: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207486'
    - - :error
      - 'Line 3690: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207489'
    - - :error
      - 'Line 3691: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207506'
    - - :error
      - 'Line 3699: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207563'
    - - :error
      - 'Line 3700: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207726'
    - - :error
      - 'Line 3702: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207783'
    - - :error
      - 'Line 3703: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207809'
    - - :error
      - 'Line 3706: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207898'
    - - :error
      - 'Line 3709: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 207976'
    - - :error
      - 'Line 3710: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208016'
    - - :error
      - 'Line 3711: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208073'
    - - :error
      - 'Line 3713: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208158'
    - - :error
      - 'Line 3716: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208203'
    - - :error
      - 'Line 3717: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208249'
    - - :error
      - 'Line 3719: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208270'
    - - :error
      - 'Line 3720: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208279'
    - - :error
      - 'Line 3721: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208475'
    - - :error
      - 'Line 3723: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208539'
    - - :error
      - 'Line 3726: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208727'
    - - :error
      - 'Line 3727: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 208728'
    - - :error
      - 'Line 3733: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209125'
    - - :error
      - 'Line 3744: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209379'
    - - :error
      - 'Line 3746: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209392'
    - - :error
      - 'Line 3747: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209407'
    - - :error
      - 'Line 3748: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209409'
    - - :error
      - 'Line 3749: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209415'
    - - :error
      - 'Line 3750: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209426'
    - - :error
      - 'Line 3751: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209433'
    - - :error
      - 'Line 3752: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209448'
    - - :error
      - 'Line 3758: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209488'
    - - :error
      - 'Line 3760: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209491'
    - - :error
      - 'Line 3761: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209521'
    - - :error
      - 'Line 3767: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209573'
    - - :error
      - 'Line 3769: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209593'
    - - :error
      - 'Line 3770: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209594'
    - - :error
      - 'Line 3771: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209595'
    - - :error
      - 'Line 3772: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209596'
    - - :error
      - 'Line 3773: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209597'
    - - :error
      - 'Line 3775: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209600'
    - - :error
      - 'Line 3776: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209609'
    - - :error
      - 'Line 3778: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209655'
    - - :error
      - 'Line 3782: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209675'
    - - :error
      - 'Line 3784: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209682'
    - - :error
      - 'Line 3785: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209683'
    - - :error
      - 'Line 3786: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209685'
    - - :error
      - 'Line 3788: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209687'
    - - :error
      - 'Line 3790: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209696'
    - - :error
      - 'Line 3792: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209703'
    - - :error
      - 'Line 3794: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209706'
    - - :error
      - 'Line 3796: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209739'
    - - :error
      - 'Line 3801: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209750'
    - - :error
      - 'Line 3809: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209771'
    - - :error
      - 'Line 3811: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209781'
    - - :error
      - 'Line 3814: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209834'
    - - :error
      - 'Line 3818: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209859'
    - - :error
      - 'Line 3822: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209947'
    - - :error
      - 'Line 3826: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209974'
    - - :error
      - 'Line 3827: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209976'
    - - :error
      - 'Line 3828: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 209977'
    - - :error
      - 'Line 3833: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210030'
    - - :error
      - 'Line 3836: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210072'
    - - :error
      - 'Line 3854: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210296'
    - - :error
      - 'Line 3865: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210365'
    - - :error
      - 'Line 3873: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210405'
    - - :error
      - 'Line 3879: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210492'
    - - :error
      - 'Line 3886: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210540'
    - - :error
      - 'Line 3888: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210543'
    - - :error
      - 'Line 3893: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210557'
    - - :error
      - 'Line 3899: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210621'
    - - :error
      - 'Line 3900: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210642'
    - - :error
      - 'Line 3903: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210681'
    - - :error
      - 'Line 3904: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210682'
    - - :error
      - 'Line 3907: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210686'
    - - :error
      - 'Line 3919: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210701'
    - - :error
      - 'Line 3923: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210859'
    - - :error
      - 'Line 3928: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 210895'
    - - :error
      - 'Line 3979: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211282'
    - - :error
      - 'Line 3982: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211333'
    - - :error
      - 'Line 3994: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211853'
    - - :error
      - 'Line 3998: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 211868'
    - - :error
      - 'Line 4000: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 247958'
    - - :error
      - 'Line 4002: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 248100'
    - - :error
      - 'Line 4003: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 248163'
    - - :error
      - 'Line 4006: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249566'
    - - :error
      - 'Line 4007: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249639'
    - - :error
      - 'Line 4008: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249652'
    - - :error
      - 'Line 4012: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249712'
    - - :error
      - 'Line 4013: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249713'
    - - :error
      - 'Line 4014: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249724'
    - - :error
      - 'Line 4015: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249725'
    - - :error
      - 'Line 4023: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249836'
    - - :error
      - 'Line 4024: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249838'
    - - :error
      - 'Line 4026: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249870'
    - - :error
      - 'Line 4028: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249959'
    - - :error
      - 'Line 4029: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 249998'
    - - :error
      - 'Line 4031: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250025'
    - - :error
      - 'Line 4037: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250197'
    - - :error
      - 'Line 4042: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250268'
    - - :error
      - 'Line 4050: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250339'
    - - :error
      - 'Line 4052: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250374'
    - - :error
      - 'Line 4055: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250386'
    - - :error
      - 'Line 4060: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250495'
    - - :error
      - 'Line 4062: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250527'
    - - :error
      - 'Line 4063: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250528'
    - - :error
      - 'Line 4067: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250545'
    - - :error
      - 'Line 4068: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250546'
    - - :error
      - 'Line 4071: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250669'
    - - :error
      - 'Line 4073: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250778'
    - - :error
      - 'Line 4074: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250861'
    - - :error
      - 'Line 4075: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250937'
    - - :error
      - 'Line 4077: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 250983'
    - - :error
      - 'Line 4078: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 251004'
    - - :error
      - 'Line 4088: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 251483'
    - - :error
      - 'Line 4089: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 251497'
    - - :error
      - 'Line 4092: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 251812'
    - - :error
      - 'Line 4094: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 251874'
    - - :error
      - 'Line 4099: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252060'
    - - :error
      - 'Line 4100: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252061'
    - - :error
      - 'Line 4101: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252062'
    - - :error
      - 'Line 4102: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252063'
    - - :error
      - 'Line 4103: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252064'
    - - :error
      - 'Line 4111: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252391'
    - - :error
      - 'Line 4112: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252394'
    - - :error
      - 'Line 4113: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252421'
    - - :error
      - 'Line 4115: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252426'
    - - :error
      - 'Line 4119: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252468'
    - - :error
      - 'Line 4121: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252507'
    - - :error
      - 'Line 4122: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252538'
    - - :error
      - 'Line 4126: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252806'
    - - :error
      - 'Line 4133: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252947'
    - - :error
      - 'Line 4134: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 252948'
    - - :error
      - 'Line 4137: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 253068'
    - - :error
      - 'Line 4139: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 253137'
    - - :error
      - 'Line 4141: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 253165'
    - - :error
      - 'Line 4142: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 253231'
    - - :error
      - 'Line 4147: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 253490'
    - - :error
      - 'Line 4150: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 254447'
    - - :error
      - 'Line 4151: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 254448'
    - - :error
      - 'Line 4152: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 254469'
    - - :error
      - 'Line 4153: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 254470'
    - - :error
      - 'Line 4157: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 255048'
    - - :error
      - 'Line 4158: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 255049'
    - - :error
      - 'Line 4160: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 255163'
    - - :error
      - 'Line 4165: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 255614'
    - - :error
      - 'Line 4166: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 255750'
    - - :error
      - 'Line 4170: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 255950'
    - - :error
      - 'Line 4173: error=Validation failed: Terms is too long (maximum is 30 characters):
        Customer # = 256039'
    - - :fatal
      - 'Line 4173: Too many errors, exception=Too many errors'
 |
| 2026-05-21 19:35:07 | ---
- - Customers
  - []
 |
| 2026-05-21 19:21:11 | ---
- - Customers
  - - - :error
      - 'Line 5092: error=Validation failed: Shipping state can''t be blank: Customer
        # = 342012'
    - - :error
      - Customer 342012 does not have at least 1 shipping location - failed to import
 |
| 2026-05-21 18:35:07 | ---
- - Customers
  - - - :error
      - 'Line 5092: error=Validation failed: Billing state can''t be blank: Customer
        # = 342012'
 |
| 2026-02-11 18:00:28 | ---
- - Images
  - - - :information
      - 'The following images were imported: PROG_P400462-009_main_PRODIMAGE.jpg,
        PROG_P400457-31M_main_PRODIMAGE.jpg, PROG_P400471-31M_main_PRODIMAGE.jpg,
        PROG_P500516-31M_main_PRODIMAGE.jpg, PROG_P500513-191_main_PRODIMAGE.jpg,
        PROG_P400459-191_main_PRODIMAGE.jpg, PROG_P560408-31M_main_PRODIMAGE.jpg,
        PROG_P500515-31M_main_PRODIMAGE.jpg, PROG_P560393-31M_main_PRODIMAGE.jpg,
        PROG_P300579-31M_main_PRODIMAGE.jpg, PROG_P300572-191_main_PRODIMAGE.jpg,
        PROG_P560394-020_main_PRODIMAGE.jpg, PROG_P400450-31M_main_PRODIMAGE.jpg,
        PROG_P560401-020_main_PRODIMAGE.jpg, PROG_P500510-009_main_PRODIMAGE.jpg,
        PROG_P500516-191_main_PRODIMAGE.jpg, PROG_P400450-009_main_PRODIMAGE.jpg,
        PROG_P400449-31M_main_PRODIMAGE.jpg, PROG_P550145-31M_main_PRODIMAGE.jpg,
        PROG_P710153-191_main_PRODIMAGE.jpg, PROG_P560406-020_main_PRODIMAGE.jpg,
        PROG_P500514-009_main_PRODIMAGE.jpg, PROG_P550145-020_main_PRODIMAGE.jpg,
        PROG_P300566-009_main_PRODIMAGE.jpg, PROG_P400458-009_main_PRODIMAGE.jpg,
        PROG_P400459-009_main_PRODIMAGE.jpg'
 |
| 2026-02-11 17:52:34 | ---
- - Images
  - - - :information
      - Image import halted early to let other jobs through. It will resume next chance
        available
    - - :information
      - 'The following images were imported: PROG_P540112-020_main_PRODIMAGE.jpg,
        PROG_P400477-009_main_PRODIMAGE.jpg, PROG_P400449-009_main_PRODIMAGE.jpg,
        PROG_P710157-31M_main_PRODIMAGE.jpg, PROG_P500515-191_main_PRODIMAGE.jpg,
        PROG_P500512-009_main_PRODIMAGE.jpg, PROG_P550146-31M_main_PRODIMAGE.jpg,
        PROG_P500514-191_main_PRODIMAGE.jpg, PROG_P400448-009_main_PRODIMAGE.jpg,
        PROG_P500513-009_main_PRODIMAGE.jpg, PROG_P560405-31M_main_PRODIMAGE.jpg,
        PROG_P400458-31M_main_PRODIMAGE.jpg, PROG_P400472-009_main_PRODIMAGE.jpg,
        PROG_P400464-31M_main_PRODIMAGE.jpg, PROG_P710154-191_main_PRODIMAGE.jpg,
        PROG_P560397-31M_main_PRODIMAGE.jpg, PROG_P500510-31M_main_PRODIMAGE.jpg,
        PROG_P400455-31M_main_PRODIMAGE.jpg, PROG_P560395-020_main_PRODIMAGE.jpg,
        PROG_P400459-31M_main_PRODIMAGE.jpg, PROG_P400461-009_main_PRODIMAGE.jpg,
        PROG_P400474-009_main_PRODIMAGE.jpg, PROG_P560404-020_main_PRODIMAGE.jpg,
        PROG_P400476-31M_main_PRODIMAGE.jpg, PROG_P710157-191_main_PRODIMAGE.jpg,
        PROG_P560406-31M_main_PRODIMAGE.jpg, PROG_P400460-31M_main_PRODIMAGE.jpg,
        PROG_P540112-31M_main_PRODIMAGE.jpg, PROG_P550147-31M_main_PRODIMAGE.jpg,
        PROG_P400454-009_main_PRODIMAGE.jpg and 93 more images'
 |

### Q-10_results.md

# Q-10 Results — Coleto Brands | Progress Lighting (prog, org_id=286)
- **Query**: Q-10 — Feature Enablement Gap Analysis
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-11_results.md

# Q-11 Results — Coleto Brands | Progress Lighting (prog, org_id=286)
- **Query**: Q-11 — Configuration Completeness
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 9
- **Run date**: 2026-06-17


| entity_type | last_updated | days_stale | related_record_count |
| --- | --- | --- | --- |
| price_levels | 2025-12-16 18:01:50 | 183 | — |
| products | 2026-02-11 17:50:26 | 126 | — |
| smart_stacks | 2026-02-11 17:50:27 | 126 | — |
| categories | 2026-02-11 17:50:37 | 126 | — |
| collections | 2026-02-11 17:50:37 | 126 | — |
| groups | 2026-02-11 17:50:37 | 126 | — |
| trade_names | 2026-02-11 17:50:37 | 126 | — |
| portal_orders | 2026-03-13 14:23:47 | 96 | — |
| portal_invoices | 2026-03-13 14:23:47 | 96 | — |

### Q-22_results.md

# Q-22 Results — Coleto Brands | Progress Lighting (prog, org_id=286)
- **Query**: Q-22 — Feature Usage Depth
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | submit_order | select_a_customer | search_for_customer | email_item_info | create_pdf_catalog | view_library_entry | view_smartpicks | access_sales_portal | filter_products | search_products | search_collections | order_configured_item | view_kit | order_kit | share_my_list | export_data_to_csv | export_data_to_excel | total_events | total_users |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| prog | Coleto Brands | Progress Lighting | 78 | 356 | 545 | 9 | 5 | 75 | 0 | 54 | 68 | 1,287 | 146 | 0 | 0 | 0 | 7 | 0 | 0 | 5,301 | 62 |

### Q-CI-02_results.md

# Q-CI-02 Results — Coleto Brands | Progress Lighting (prog, org_id=286)
- **Query**: Q-CI-02 — Peer Comparison
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | peer_standing | orders_vs_peer_pct | logins_vs_peer_pct | mrr_vs_peer_pct | peer_orders_median | peer_logins_median | peer_mrr_median |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| prog | Coleto Brands | Progress Lighting | Commerce-Active | Needs Attention | -69.30 | -80.20 | 3,128.30 | 254 | 2,833 | 920 |

### Q-CI-03_results.md

# Q-CI-03 Results — Coleto Brands | Progress Lighting (prog, org_id=286)
- **Query**: Q-CI-03 — Feature Adoption Benchmarking
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | feature_depth | has_clicky_portal | arr |
| --- | --- | --- | --- | --- | --- |
| prog | Coleto Brands | Progress Lighting | Commerce-Active | 5 | 0 | 29,700 |

### Q-CI-03_benchmarks_results.md

# Q-CI-03-bench Results — Coleto Brands | Progress Lighting (prog, org_id=286)
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
