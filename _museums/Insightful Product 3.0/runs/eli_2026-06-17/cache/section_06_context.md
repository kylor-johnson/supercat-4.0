# Section 6 Context Bundle — Elegant Furniture & Lighting (eli)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Elegant Furniture & Lighting (eli, org_id=68)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | True | recurring_services contains B2B Cart: True |
| HAS_PORTAL_ORDERS | False | portal_order_count=0, portal_order_gmv=$0 |
| HAS_INVENTORY | True | inventory_count=11543 |
| HAS_SALES_DATA | False | sales_data_count=0 |
| HAS_SALES_SECTION | True | qualifying_reps=8 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
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
| QUALIFYING_REP_COUNT | 8 | 8 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 88 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 319, Mixpanel total submit_order (Q-01): 565 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=97.7%, ambiguous_rate=1.2%, showroom_event_share=9.1% |
| USER_GROUP_JOIN_RATE | 98% | 86 of 88 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 9% | showroom+admin share of matched events: 9.1% |
| ADMIN_REPS_IN_LEADERBOARD | True | 2 admin/showroom users in leaderboard: My Dang, John Pugh |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False |  |
| PORTAL_REP_DATA_PRESENT | False |  |
| PORTAL_CUSTOMER_DATA_PRESENT | False |  |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 27d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=233 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | PARTIAL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | PARTIAL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Elegant Furniture & Lighting
- **Shortname**: eli
- **Org ID**: 68
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- portal_orders LTM count=0, gmv=0.0 — HAS_PORTAL_ORDERS overridden to false

## Section Confidence

# Section Confidence Tiers — Elegant Furniture & Lighting (eli, org_id=68)
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
| HAS_SALES_DATA | False |
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

# Signal Rank — Elegant Furniture & Lighting (eli, org_id=68)
- **Run date**: 2026-06-17
- **Total signals fired**: 16 (P0: 0, P1: 13, P2: 3)
- **Org GMV**: $0.0M eCat LTM, $0.0M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 59% of eCat GMV | P1 | §4 Commerce | 1.5 | $193,183 | 2.0 | 569,679 | RISK |
| 2 | SIG-DECAY-03 | Rep Trajectory — Hector Reyes orders -34.8% QoQ, $36,091 current 90d GMV | P1 | §5 Team | 1.4 | $144,364 | 2.0 | 401,909 | RISK |
| 3 | SIG-RISK-03 | Data Staleness — option_groups last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 4 | SIG-RISK-03 | Data Staleness — options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 5 | SIG-RISK-03 | Data Staleness — matrix_options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 6 | SIG-RISK-03 | Data Staleness — kit_items last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 7 | SIG-RISK-03 | Data Staleness — customer_favorites last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 8 | SIG-RISK-03 | Data Staleness — contract_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 9 | SIG-RISK-03 | Data Staleness — commitment_reports last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 10 | SIG-RISK-03 | Data Staleness — placement_reports last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 11 | SIG-RISK-03 | Data Staleness — riser_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 12 | SIG-RISK-03 | Data Staleness — customer_payment_informations last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 13 | SIG-RISK-03 | Data Staleness — sales_quotas last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 14 | SIG-RISK-03 | Data Staleness — price_levels last updated 103d ago | P2 | §6 Platform | 1.1 | $1 | 2.0 | 2 | RISK |
| 15 | SIG-RISK-03 | Data Staleness — portal_orders last updated 96d ago | P2 | §6 Platform | 1.1 | $1 | 2.0 | 2 | RISK |
| 16 | SIG-RISK-03 | Data Staleness — portal_invoices last updated 96d ago | P2 | §6 Platform | 1.1 | $1 | 2.0 | 2 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §4 Commerce Patterns | 0 | 1 | 0 | 1 | |
| §5 Team Intelligence | 0 | 1 | 0 | 1 | |
| §6 Platform Context | 0 | 11 | 3 | 14 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[RISK]** SIG-RISK-01: Revenue Concentration — top 5 accounts generate 59% of eCat GMV
2. **[RISK]** SIG-DECAY-03: Rep Trajectory — Hector Reyes orders -34.8% QoQ, $36,091 current 90d GMV
3. **[RISK]** SIG-RISK-03: Data Staleness — option_groups last updated 313d ago
4. **[RISK]** SIG-RISK-03: Data Staleness — options last updated 313d ago
5. **[RISK]** SIG-RISK-03: Data Staleness — matrix_options last updated 313d ago
6. **[RISK]** SIG-RISK-03: Data Staleness — kit_items last updated 313d ago
7. **[RISK]** SIG-RISK-03: Data Staleness — customer_favorites last updated 313d ago

**Balance check**: 0 positive (slots 1-0), 7 risk (slots 1-7). Finding #1 is RISK. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-08_results.md

# Q-08 Results — Elegant Furniture & Lighting (eli, org_id=68)
- **Query**: Q-08 — Data Freshness Monitor
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 22
- **Run date**: 2026-06-17


| entity_type | last_updated | days_since_update | status |
| --- | --- | --- | --- |
| option_groups | 2025-08-07 23:13:01 | 313 | Stale |
| options | 2025-08-07 23:13:01 | 313 | Stale |
| matrix_options | 2025-08-07 23:13:01 | 313 | Stale |
| kit_items | 2025-08-07 23:13:01 | 313 | Stale |
| customer_favorites | 2025-08-07 23:13:01 | 313 | Stale |
| contract_prices | 2025-08-07 23:13:01 | 313 | Stale |
| commitment_reports | 2025-08-07 23:13:01 | 313 | Stale |
| placement_reports | 2025-08-07 23:13:01 | 313 | Stale |
| riser_prices | 2025-08-07 23:13:01 | 313 | Stale |
| customer_payment_informations | 2025-08-07 23:13:01 | 313 | Stale |
| sales_quotas | 2025-08-07 23:13:01 | 313 | Stale |
| price_levels | 2026-03-06 20:20:22 | 103 | Monitor |
| portal_orders | 2026-03-13 14:23:30 | 96 | Monitor |
| portal_invoices | 2026-03-13 14:23:30 | 96 | Monitor |
| customers | 2026-05-21 15:00:06 | 27 | Fresh |
| products | 2026-06-16 14:23:09 | 1 | Fresh |
| smart_stacks | 2026-06-16 14:23:09 | 1 | Fresh |
| categories | 2026-06-16 14:23:12 | 1 | Fresh |
| collections | 2026-06-16 14:23:12 | 1 | Fresh |
| groups | 2026-06-16 14:23:12 | 1 | Fresh |
| trade_names | 2026-06-16 14:23:12 | 1 | Fresh |
| inventories | 2026-06-17 07:02:48 | 0 | Fresh |

### Q-09_results.md

# Q-09 Results — Elegant Furniture & Lighting (eli, org_id=68)
- **Query**: Q-09 — Import Health — Monthly Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 7
- **Run date**: 2026-06-17


| month | import_count |
| --- | --- |
| 2026-06-01 | 41 |
| 2026-05-01 | 63 |
| 2026-04-01 | 106 |
| 2026-03-01 | 61 |
| 2026-02-01 | 61 |
| 2026-01-01 | 116 |
| 2025-12-01 | 68 |

### Q-09_recent_results.md

# Q-09-recent Results — Elegant Furniture & Lighting (eli, org_id=68)
- **Query**: Q-09-recent — Import Health — Recent Errors
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| created_at | data |
| --- | --- |
| 2026-06-17 07:02:48 | ---
- - Inventory
  - - - :warning
      - 'Line 9: Product not found, record ignored., BaseItemCode=1101D28BR'
    - - :warning
      - 'Line 102: Product not found, record ignored., BaseItemCode=1107F18BR'
    - - :warning
      - 'Line 686: Product not found, record ignored., BaseItemCode=1451D20C'
    - - :warning
      - 'Line 687: Product not found, record ignored., BaseItemCode=1452D18PN'
    - - :warning
      - 'Line 694: Product not found, record ignored., BaseItemCode=1453D17DB'
    - - :warning
      - 'Line 695: Product not found, record ignored., BaseItemCode=1453W13PN'
    - - :warning
      - 'Line 696: Product not found, record ignored., BaseItemCode=1458D13BZ'
    - - :warning
      - 'Line 697: Product not found, record ignored., BaseItemCode=1458D13VN'
    - - :warning
      - 'Line 700: Product not found, record ignored., BaseItemCode=1461W13PN'
    - - :warning
      - 'Line 703: Product not found, record ignored., BaseItemCode=1471G44SL'
    - - :warning
      - 'Line 704: Product not found, record ignored., BaseItemCode=1472G39BB'
    - - :warning
      - 'Line 708: Product not found, record ignored., BaseItemCode=1473G52PN'
    - - :warning
      - 'Line 709: Product not found, record ignored., BaseItemCode=1485D15VN'
    - - :warning
      - 'Line 716: Product not found, record ignored., BaseItemCode=1503D18IW'
    - - :warning
      - 'Line 717: Product not found, record ignored., BaseItemCode=1504D35VN'
    - - :warning
      - 'Line 723: Product not found, record ignored., BaseItemCode=1512D9GI'
    - - :warning
      - 'Line 726: Product not found, record ignored., BaseItemCode=1537W5VB'
    - - :warning
      - 'Line 727: Product not found, record ignored., BaseItemCode=1702D18ASL'
    - - :warning
      - 'Line 731: Product not found, record ignored., BaseItemCode=1710D12FB'
    - - :warning
      - 'Line 817: Product not found, record ignored., BaseItemCode=2105W10C/RC'
    - - :warning
      - 'Line 826: Product not found, record ignored., BaseItemCode=2116D26C/RC'
    - - :warning
      - 'Line 827: Product not found, record ignored., BaseItemCode=2116D32C/RC'
    - - :warning
      - 'Line 828: Product not found, record ignored., BaseItemCode=2116G63C/RC'
    - - :warning
      - 'Line 831: Product not found, record ignored., BaseItemCode=2117W33C/RC'
    - - :warning
      - 'Line 1372: Product not found, record ignored., BaseItemCode=5100D5C'
    - - :warning
      - 'Line 1386: Product not found, record ignored., BaseItemCode=5200D32C'
    - - :warning
      - 'Line 1388: Product not found, record ignored., BaseItemCode=5200D36C'
    - - :warning
      - 'Line 1389: Product not found, record ignored., BaseItemCode=5200D42C'
    - - :warning
      - 'Line 1397: Product not found, record ignored., BaseItemCode=5201D5C'
    - - :warning
      - 'Line 1398: Product not found, record ignored., BaseItemCode=5202D22C'
    - - :warning
      - 'Line 1400: Product not found, record ignored., BaseItemCode=5202D24C'
    - - :warning
      - 'Line 1401: Product not found, record ignored., BaseItemCode=5202D24G'
    - - :warning
      - 'Line 1407: Product not found, record ignored., BaseItemCode=5203D16G'
    - - :warning
      - 'Line 1456: Product not found, record ignored., BaseItemCode=7872D17C'
    - - :warning
      - 'Line 1457: Product not found, record ignored., BaseItemCode=7872D17SS'
    - - :warning
      - 'Line 1589: Product not found, record ignored., BaseItemCode=BR20LED102-6PK'
    - - :warning
      - 'Line 1658: Product not found, record ignored., BaseItemCode=CF3004'
    - - :warning
      - 'Line 1812: Product not found, record ignored., BaseItemCode=KIT20204'
    - - :warning
      - 'Line 1813: Product not found, record ignored., BaseItemCode=KIT20402'
    - - :warning
      - 'Line 1814: Product not found, record ignored., BaseItemCode=KIT40606'
    - - :warning
      - 'Line 1815: Product not found, record ignored., BaseItemCode=KIT40804'
    - - :warning
      - 'Line 1882: Product not found, record ignored., BaseItemCode=LD2239C'
    - - :warning
      - 'Line 1919: Product not found, record ignored., BaseItemCode=LD2259BR'
    - - :warning
      - 'Line 1936: Product not found, record ignored., BaseItemCode=LD2274BK'
    - - :warning
      - 'Line 1938: Product not found, record ignored., BaseItemCode=LD2275BR'
    - - :warning
      - 'Line 1942: Product not found, record ignored., BaseItemCode=LD2277C'
    - - :warning
      - 'Line 1955: Product not found, record ignored., BaseItemCode=LD2300BR'
    - - :warning
      - 'Line 1958: Product not found, record ignored., BaseItemCode=LD2301BR'
    - - :warning
      - 'Line 1959: Product not found, record ignored., BaseItemCode=LD2301C'
    - - :warning
      - 'Line 1960: Product not found, record ignored., BaseItemCode=LD2302BK'
    - - :warning
      - 'Line 1961: Product not found, record ignored., BaseItemCode=LD2302BR'
    - - :warning
      - 'Line 1962: Product not found, record ignored., BaseItemCode=LD2302C'
    - - :warning
      - 'Line 1966: Product not found, record ignored., BaseItemCode=LD2304BK'
    - - :warning
      - 'Line 1969: Product not found, record ignored., BaseItemCode=LD2305BK'
    - - :warning
      - 'Line 1970: Product not found, record ignored., BaseItemCode=LD2305BR'
    - - :warning
      - 'Line 1971: Product not found, record ignored., BaseItemCode=LD2305C'
    - - :warning
      - 'Line 1972: Product not found, record ignored., BaseItemCode=LD2306BR'
    - - :warning
      - 'Line 1975: Product not found, record ignored., BaseItemCode=LD2307BR'
    - - :warning
      - 'Line 1979: Product not found, record ignored., BaseItemCode=LD2309C'
    - - :warning
      - 'Line 1980: Product not found, record ignored., BaseItemCode=LD2310BK'
    - - :warning
      - 'Line 1984: Product not found, record ignored., BaseItemCode=LD2311BR'
    - - :warning
      - 'Line 2037: Product not found, record ignored., BaseItemCode=LD2337BK'
    - - :warning
      - 'Line 2038: Product not found, record ignored., BaseItemCode=LD2337BR'
    - - :warning
      - 'Line 2039: Product not found, record ignored., BaseItemCode=LD2337C'
    - - :warning
      - 'Line 2040: Product not found, record ignored., BaseItemCode=LD2338BK'
    - - :warning
      - 'Line 2041: Product not found, record ignored., BaseItemCode=LD2338BR'
    - - :warning
      - 'Line 2042: Product not found, record ignored., BaseItemCode=LD2338C'
    - - :warning
      - 'Line 2043: Product not found, record ignored., BaseItemCode=LD2339BK'
    - - :warning
      - 'Line 2044: Product not found, record ignored., BaseItemCode=LD2339BR'
    - - :warning
      - 'Line 2045: Product not found, record ignored., BaseItemCode=LD2339C'
    - - :warning
      - 'Line 2046: Product not found, record ignored., BaseItemCode=LD2340BK'
    - - :warning
      - 'Line 2047: Product not found, record ignored., BaseItemCode=LD2340BR'
    - - :warning
      - 'Line 2048: Product not found, record ignored., BaseItemCode=LD2340C'
    - - :warning
      - 'Line 2049: Product not found, record ignored., BaseItemCode=LD2341BR'
    - - :warning
      - 'Line 2050: Product not found, record ignored., BaseItemCode=LD2344BK'
    - - :warning
      - 'Line 2051: Product not found, record ignored., BaseItemCode=LD2344BR'
    - - :warning
      - 'Line 2063: Product not found, record ignored., BaseItemCode=LD2350BK'
    - - :warning
      - 'Line 2064: Product not found, record ignored., BaseItemCode=LD2350BR'
    - - :warning
      - 'Line 2068: Product not found, record ignored., BaseItemCode=LD2352BK'
    - - :warning
      - 'Line 2069: Product not found, record ignored., BaseItemCode=LD2352BR'
    - - :warning
      - 'Line 2096: Product not found, record ignored., BaseItemCode=LD2363BK'
    - - :warning
      - 'Line 2097: Product not found, record ignored., BaseItemCode=LD2363BR'
    - - :warning
      - 'Line 2098: Product not found, record ignored., BaseItemCode=LD2364BK'
    - - :warning
      - 'Line 2099: Product not found, record ignored., BaseItemCode=LD2364BR'
    - - :warning
      - 'Line 2100: Product not found, record ignored., BaseItemCode=LD2364RED'
    - - :warning
      - 'Line 2101: Product not found, record ignored., BaseItemCode=LD2364WH'
    - - :warning
      - 'Line 2102: Product not found, record ignored., BaseItemCode=LD2365BK'
    - - :warning
      - 'Line 2103: Product not found, record ignored., BaseItemCode=LD2365BR'
    - - :warning
      - 'Line 2108: Product not found, record ignored., BaseItemCode=LD2367WH'
    - - :warning
      - 'Line 2110: Product not found, record ignored., BaseItemCode=LD2401WH'
    - - :warning
      - 'Line 2113: Product not found, record ignored., BaseItemCode=LD2404BN'
    - - :warning
      - 'Line 2115: Product not found, record ignored., BaseItemCode=LD2405HG'
    - - :warning
      - 'Line 2119: Product not found, record ignored., BaseItemCode=LD2407HG'
    - - :warning
      - 'Line 2126: Product not found, record ignored., BaseItemCode=LD2410WH'
    - - :warning
      - 'Line 2127: Product not found, record ignored., BaseItemCode=LD2411HG'
    - - :warning
      - 'Line 2128: Product not found, record ignored., BaseItemCode=LD2412WH'
    - - :warning
      - 'Line 2134: Product not found, record ignored., BaseItemCode=LD2450BK'
    - - :warning
      - 'Line 2135: Product not found, record ignored., BaseItemCode=LD2450BR'
    - - :warning
      - 'Line 2136: Product not found, record ignored., BaseItemCode=LD2450C'
    - - :warning
      - 'Line 2140: Product not found, record ignored., BaseItemCode=LD2453FLBK'
    - - :warning
      - 'Line 2141: Product not found, record ignored., BaseItemCode=LD2453FLBR'
    - - :warning
      - 'Line 2142: Product not found, record ignored., BaseItemCode=LD2453FLCG'
    - - :warning
      - 'Line 2158: Product not found, record ignored., BaseItemCode=LD4008D11BK'
    - - :warning
      - 'Line 2164: Product not found, record ignored., BaseItemCode=LD4017D48BRB'
    - - :warning
      - 'Line 2291: Product not found, record ignored., BaseItemCode=LD5016D17BK'
    - - :warning
      - 'Line 2302: Product not found, record ignored., BaseItemCode=LD5023'
    - - :warning
      - 'Line 2370: Product not found, record ignored., BaseItemCode=LD520D10BK'
    - - :warning
      - 'Line 2371: Product not found, record ignored., BaseItemCode=LD520D10BR'
    - - :warning
      - 'Line 2372: Product not found, record ignored., BaseItemCode=LD520D10C'
    - - :warning
      - 'Line 2373: Product not found, record ignored., BaseItemCode=LD520D13BK'
    - - :warning
      - 'Line 2374: Product not found, record ignored., BaseItemCode=LD520D13BR'
    - - :warning
      - 'Line 2375: Product not found, record ignored., BaseItemCode=LD520D13C'
    - - :warning
      - 'Line 2376: Product not found, record ignored., BaseItemCode=LD520D16BK'
    - - :warning
      - 'Line 2377: Product not found, record ignored., BaseItemCode=LD520D16BR'
    - - :warning
      - 'Line 2378: Product not found, record ignored., BaseItemCode=LD520D16C'
    - - :warning
      - 'Line 2379: Product not found, record ignored., BaseItemCode=LD520D18BK'
    - - :warning
      - 'Line 2380: Product not found, record ignored., BaseItemCode=LD520D18BR'
    - - :warning
      - 'Line 2381: Product not found, record ignored., BaseItemCode=LD520D18C'
    - - :warning
      - 'Line 2382: Product not found, record ignored., BaseItemCode=LD520D20BR'
    - - :warning
      - 'Line 2391: Product not found, record ignored., BaseItemCode=LD6005D12BR'
    - - :warning
      - 'Line 2408: Product not found, record ignored., BaseItemCode=LD6010D26BN'
    - - :warning
      - 'Line 2414: Product not found, record ignored., BaseItemCode=LD6012D15G'
    - - :warning
      - 'Line 2425: Product not found, record ignored., BaseItemCode=LD6016'
    - - :warning
      - 'Line 2471: Product not found, record ignored., BaseItemCode=LD6077C'
    - - :warning
      - 'Line 2481: Product not found, record ignored., BaseItemCode=LD6100C'
    - - :warning
      - 'Line 2495: Product not found, record ignored., BaseItemCode=LD6109BR'
    - - :warning
      - 'Line 2502: Product not found, record ignored., BaseItemCode=LD6124C'
    - - :warning
      - 'Line 2509: Product not found, record ignored., BaseItemCode=LD6133BR'
    - - :warning
      - 'Line 2537: Product not found, record ignored., BaseItemCode=LD6170C'
    - - :warning
      - 'Line 2540: Product not found, record ignored., BaseItemCode=LD6173BR'
    - - :warning
      - 'Line 2543: Product not found, record ignored., BaseItemCode=LD6176C'
    - - :warning
      - 'Line 2544: Product not found, record ignored., BaseItemCode=LD6178BR'
    - - :warning
      - 'Line 2558: Product not found, record ignored., BaseItemCode=LD6205C'
    - - :warning
      - 'Line 2568: Product not found, record ignored., BaseItemCode=LD6220C'
    - - :warning
      - 'Line 2574: Product not found, record ignored., BaseItemCode=LD6232C'
    - - :warning
      - 'Line 2575: Product not found, record ignored., BaseItemCode=LD6238C'
    - - :warning
      - 'Line 2581: Product not found, record ignored., BaseItemCode=LD6248BR'
    - - :warning
      - 'Line 2587: Product not found, record ignored., BaseItemCode=LD6259C'
    - - :warning
      - 'Line 2603: Product not found, record ignored., BaseItemCode=LD642D36BR'
    - - :warning
      - 'Line 2604: Product not found, record ignored., BaseItemCode=LD642D36BRK'
    - - :warning
      - 'Line 2605: Product not found, record ignored., BaseItemCode=LD643D36BK'
    - - :warning
      - 'Line 2620: Product not found, record ignored., BaseItemCode=LD648F26BK'
    - - :warning
      - 'Line 2622: Product not found, record ignored., BaseItemCode=LD648F26BRK'
    - - :warning
      - 'Line 2633: Product not found, record ignored., BaseItemCode=LD652D30BR'
    - - :warning
      - 'Line 2642: Product not found, record ignored., BaseItemCode=LD655D18BR'
    - - :warning
      - 'Line 2643: Product not found, record ignored., BaseItemCode=LD655D18BRK'
    - - :warning
      - 'Line 2650: Product not found, record ignored., BaseItemCode=LD6802D14C'
    - - :warning
      - 'Line 2683: Product not found, record ignored., BaseItemCode=LD7024D25BK'
    - - :warning
      - 'Line 2685: Product not found, record ignored., BaseItemCode=LD7024D25SN'
    - - :warning
      - 'Line 2752: Product not found, record ignored., BaseItemCode=LD7044D26WD'
    - - :warning
      - 'Line 2760: Product not found, record ignored., BaseItemCode=LD7047D28BR'
    - - :warning
      - 'Line 2779: Product not found, record ignored., BaseItemCode=LD7057D20BK'
    - - :warning
      - 'Line 2809: Product not found, record ignored., BaseItemCode=LD7071D14BK'
    - - :warning
      - 'Line 2879: Product not found, record ignored., BaseItemCode=LD7301W15CH'
    - - :warning
      - 'Line 2892: Product not found, record ignored., BaseItemCode=LD7302W24BLK'
    - - :warning
      - 'Line 2900: Product not found, record ignored., BaseItemCode=LD7302W6CH'
    - - :warning
      - 'Line 2917: Product not found, record ignored., BaseItemCode=LD7304W22BRA'
    - - :warning
      - 'Line 2922: Product not found, record ignored., BaseItemCode=LD7304W7BLK'
    - - :warning
      - 'Line 2942: Product not found, record ignored., BaseItemCode=LD7307W24CH'
    - - :warning
      - 'Line 2976: Product not found, record ignored., BaseItemCode=LD7310W23BLK'
    - - :warning
      - 'Line 3147: Product not found, record ignored., BaseItemCode=LD7327W6BLK'
    - - :warning
      - 'Line 3159: Product not found, record ignored., BaseItemCode=LD7331W7BLK'
    - - :warning
      - 'Line 3218: Product not found, record ignored., BaseItemCode=LD8049D10BR'
    - - :warning
      - 'Line 3240: Product not found, record ignored., BaseItemCode=LD810F19SL'
    - - :warning
      - 'Line 3293: Product not found, record ignored., BaseItemCode=LD8801D43GB'
    - - :warning
      - 'Line 3323: Product not found, record ignored., BaseItemCode=LDOD3004-6PK'
    - - :warning
      - 'Line 3324: Product not found, record ignored., BaseItemCode=LDOD3006-4PK'
    - - :warning
      - 'Line 3339: Product not found, record ignored., BaseItemCode=LDOD4010BK'
    - - :warning
      - 'Line 3341: Product not found, record ignored., BaseItemCode=LDOD4011BK'
    - - :warning
      - 'Line 3343: Product not found, record ignored., BaseItemCode=LDOD4011WH'
    - - :warning
      - 'Line 3347: Product not found, record ignored., BaseItemCode=LDOD4013WH'
    - - :warning
      - 'Line 3354: Product not found, record ignored., BaseItemCode=LDOD4016BK'
    - - :warning
      - 'Line 3356: Product not found, record ignored., BaseItemCode=LDOD4016WH'
    - - :warning
      - 'Line 3395: Product not found, record ignored., BaseItemCode=LDPD2000BN'
    - - :warning
      - 'Line 3403: Product not found, record ignored., BaseItemCode=LDPD2003BN'
    - - :warning
      - 'Line 3409: Product not found, record ignored., BaseItemCode=LDPD2017'
    - - :warning
      - 'Line 3424: Product not found, record ignored., BaseItemCode=LDPD2045HG'
    - - :warning
      - 'Line 3427: Product not found, record ignored., BaseItemCode=LDPD2046WH'
    - - :warning
      - 'Line 3474: Product not found, record ignored., BaseItemCode=LDPG2256BK'
    - - :warning
      - 'Line 3475: Product not found, record ignored., BaseItemCode=LDPG2256BR'
    - - :warning
      - 'Line 3483: Product not found, record ignored., BaseItemCode=LDPG6037BR'
    - - :warning
      - 'Line 3499: Product not found, record ignored., BaseItemCode=MF53047BL'
    - - :warning
      - 'Line 3509: Product not found, record ignored., BaseItemCode=MF6-1008S'
    - - :warning
      - 'Line 3517: Product not found, record ignored., BaseItemCode=MF6-1036AW'
    - - :warning
      - 'Line 3518: Product not found, record ignored., BaseItemCode=MF6-1036BL'
    - - :warning
      - 'Line 3523: Product not found, record ignored., BaseItemCode=MF61060AW'
    - - :warning
      - 'Line 3524: Product not found, record ignored., BaseItemCode=MF61060AW-F1'
    - - :warning
      - 'Line 3525: Product not found, record ignored., BaseItemCode=MF61072BL'
    - - :warning
      - 'Line 3585: Product not found, record ignored., BaseItemCode=MF72038BK'
    - - :warning
      - 'Line 3597: Product not found, record ignored., BaseItemCode=MF73016BK'
    - - :warning
      - 'Line 3616: Product not found, record ignored., BaseItemCode=MF82002WH'
    - - :warning
      - 'Line 3623: Invalid next scheduled receipt date'
    - - :warning
      - 'Line 3842: Product not found, record ignored., BaseItemCode=MR33248BL'
    - - :warning
      - 'Line 3843: Product not found, record ignored., BaseItemCode=MR33272BL'
    - - :warning
      - 'Line 3865: Product not found, record ignored., BaseItemCode=MR4044WH'
    - - :warning
      - 'Line 3875: Product not found, record ignored., BaseItemCode=MR4054GR'
    - - :warning
      - 'Line 3894: Product not found, record ignored., BaseItemCode=MR4071BL'
    - - :warning
      - 'Line 3916: Product not found, record ignored., BaseItemCode=MR41828BL'
    - - :warning
      - 'Line 3924: Product not found, record ignored., BaseItemCode=MR42036BL'
    - - :warning
      - 'Line 3937: Product not found, record ignored., BaseItemCode=MR42736BL'
    - - :warning
      - 'Line 3994: Product not found, record ignored., BaseItemCode=MR4718BL'
    - - :warning
      - 'Line 3998: Product not found, record ignored., BaseItemCode=MR4721BL'
    - - :warning
      - 'Line 4000: Product not found, record ignored., BaseItemCode=MR4721GR'
    - - :warning
      - 'Line 4035: Product not found, record ignored., BaseItemCode=MR52736'
    - - :warning
      - 'Line 4036: Product not found, record ignored., BaseItemCode=MR53648'
    - - :warning
      - 'Line 4037: Product not found, record ignored., BaseItemCode=MR53660'
    - - :warning
      - 'Line 4058: Product not found, record ignored., BaseItemCode=MR652828BK'
    - - :warning
      - 'Line 4147: Product not found, record ignored., BaseItemCode=MR913240'
    - - :warning
      - 'Line 4155: Invalid next scheduled receipt date'
    - - :warning
      - 'Line 4156: Product not found, record ignored., BaseItemCode=MR9239'
    - - :warning
      - 'Line 4190: Product not found, record ignored., BaseItemCode=MRE32432BK'
    - - :warning
      - 'Line 4193: Product not found, record ignored., BaseItemCode=MRE32471BK'
    - - :warning
      - 'Line 4209: Product not found, record ignored., BaseItemCode=MRE52036'
    - - :warning
      - 'Line 4210: Product not found, record ignored., BaseItemCode=MRE52040'
    - - :warning
      - 'Line 4211: Product not found, record ignored., BaseItemCode=MRE52436'
    - - :warning
      - 'Line 4212: Product not found, record ignored., BaseItemCode=MRE52440'
    - - :warning
      - 'Line 4213: Product not found, record ignored., BaseItemCode=MRE52730'
    - - :warning
      - 'Line 4214: Product not found, record ignored., BaseItemCode=MRE52736'
    - - :warning
      - 'Line 4215: Product not found, record ignored., BaseItemCode=MRE52740'
    - - :warning
      - 'Line 4216: Product not found, record ignored., BaseItemCode=MRE53030'
    - - :warning
      - 'Line 4217: Product not found, record ignored., BaseItemCode=MRE53072'
    - - :warning
      - 'Line 4218: Product not found, record ignored., BaseItemCode=MRE53648'
    - - :warning
      - 'Line 4219: Product not found, record ignored., BaseItemCode=MRE54260'
    - - :warning
      - 'Line 4302: Product not found, record ignored., BaseItemCode=MRE92030'
    - - :warning
      - 'Line 4303: Product not found, record ignored., BaseItemCode=MRE92436'
    - - :warning
      - 'Line 4306: Product not found, record ignored., BaseItemCode=MRE93248'
    - - :warning
      - 'Line 4307: Product not found, record ignored., BaseItemCode=MRE93272'
    - - :warning
      - 'Line 4414: Product not found, record ignored., BaseItemCode=RN61550RF-4PK'
    - - :warning
      - 'Line 4415: Product not found, record ignored., BaseItemCode=RS41050SDK-4PK'
    - - :warning
      - 'Line 4484: Product not found, record ignored., BaseItemCode=TC5R-E26-6PK'
    - - :warning
      - 'Line 4485: Product not found, record ignored., BaseItemCode=TC6R-E26-6PK'
    - - :warning
      - 'Line 4505: Product not found, record ignored., BaseItemCode=TKACP-MW'
    - - :warning
      - 'Line 4506: Product not found, record ignored., BaseItemCode=TKAEF-MW'
    - - :warning
      - 'Line 4507: Product not found, record ignored., BaseItemCode=TKAFCF-BK'
    - - :warning
      - 'Line 4508: Product not found, record ignored., BaseItemCode=TKALC-BK'
    - - :warning
      - 'Line 4509: Product not found, record ignored., BaseItemCode=TKATC-BK'
    - - :warning
      - 'Line 4510: Product not found, record ignored., BaseItemCode=TKATC-MW'
    - - :warning
      - 'Line 4511: Product not found, record ignored., BaseItemCode=TKH210BK-6PK'
    - - :warning
      - 'Line 4512: Product not found, record ignored., BaseItemCode=TKL4BK'
    - - :warning
      - 'Line 4513: Product not found, record ignored., BaseItemCode=TKL4MW'
    - - :warning
      - 'Line 4525: Product not found, record ignored., BaseItemCode=V1800D24BK/RC'
    - - :warning
      - 'Line 4603: Product not found, record ignored., BaseItemCode=V1803W12SG/RC'
    - - :warning
      - 'Line 4638: Product not found, record ignored., BaseItemCode=V2006F14C/RC'
    - - :warning
      - 'Line 4640: Product not found, record ignored., BaseItemCode=V2006F16C/RC'
    - - :warning
      - 'Line 4648: Product not found, record ignored., BaseItemCode=V2011D21G/RC'
    - - :warning
      - 'Line 4705: Product not found, record ignored., BaseItemCode=V2032D24C/RC'
    - - :warning
      - 'Line 4711: Product not found, record ignored., BaseItemCode=V2032F14C/RC'
    - - :warning
      - 'Line 4718: Product not found, record ignored., BaseItemCode=V2032W30BK/RC'
    - - :warning
      - 'Line 4719: Product not found, record ignored., BaseItemCode=V2032W36BK/RC'
    - - :warning
      - 'Line 4724: Product not found, record ignored., BaseItemCode=V2033D24C/RC'
    - - :warning
      - 'Line 4726: Product not found, record ignored., BaseItemCode=V2033F14C/RC'
    - - :warning
      - 'Line 4733: Product not found, record ignored., BaseItemCode=V2034D28C/RC'
    - - :warning
      - 'Line 4736: Product not found, record ignored., BaseItemCode=V2035D28C/RC'
    - - :warning
      - 'Line 4737: Product not found, record ignored., BaseItemCode=V2075D18C/RC'
    - - :warning
      - 'Line 4748: Product not found, record ignored., BaseItemCode=V2100D35C/RC'
    - - :warning
      - 'Line 4796: Product not found, record ignored., BaseItemCode=V3100D40C/RC'
    - - :warning
      - 'Line 4798: Product not found, record ignored., BaseItemCode=V6801D14C/RC'
    - - :warning
      - 'Line 4799: Product not found, record ignored., BaseItemCode=V6801D19G/RC'
    - - :warning
      - 'Line 4801: Product not found, record ignored., BaseItemCode=V7803D11B-JT/RC'
    - - :warning
      - 'Line 4805: Product not found, record ignored., BaseItemCode=V7804D15GS-GS/RC'
    - - :warning
      - 'Line 4807: Product not found, record ignored., BaseItemCode=V7804D15PE/RC'
    - - :warning
      - 'Line 4808: Product not found, record ignored., BaseItemCode=V7804D15PK-RO/RC'
    - - :warning
      - 'Line 4882: Product not found, record ignored., BaseItemCode=V9800D20G/RC'
    - - :warning
      - 'Line 4883: Product not found, record ignored., BaseItemCode=V9800D24C/RC'
    - - :warning
      - 'Line 4884: Product not found, record ignored., BaseItemCode=V9800D24G/RC'
    - - :warning
      - 'Line 4885: Product not found, record ignored., BaseItemCode=V9800D28C/RC'
    - - :warning
      - 'Line 4894: Product not found, record ignored., BaseItemCode=V9805F10BK/RC'
    - - :warning
      - 'Line 4895: Product not found, record ignored., BaseItemCode=V9805F10C/RC'
    - - :warning
      - 'Line 4896: Product not found, record ignored., BaseItemCode=V9805F10G/RC'
    - - :warning
      - 'Line 4969: Product not found, record ignored., BaseItemCode=VF-1030VM'
    - - :warning
      - 'Line 4999: Product not found, record ignored., BaseItemCode=VF12319GR'
    - - :warning
      - 'Line 5030: Product not found, record ignored., BaseItemCode=VF12360DGR-VW'
    - - :warning
      - 'Line 5148: Product not found, record ignored., BaseItemCode=VF13060DAB-VW'
    - - :warning
      - 'Line 5153: Product not found, record ignored., BaseItemCode=VF13060DVM-VW'
    - - :warning
      - 'Line 5192: Product not found, record ignored., BaseItemCode=VF15032GN'
    - - :warning
      - 'Line 5328: Product not found, record ignored., BaseItemCode=VF17018WH'
    - - :warning
      - 'Line 5581: Product not found, record ignored., BaseItemCode=VF27048GN'
    - - :warning
      - 'Line 5769: Product not found, record ignored., BaseItemCode=VF41048MGN'
    - - :warning
      - 'Line 5799: Product not found, record ignored., BaseItemCode=VF42524MGN'
    - - :warning
      - 'Line 5800: Product not found, record ignored., BaseItemCode=VF42524MMP'
    - - :warning
      - 'Line 5872: Product not found, record ignored., BaseItemCode=VF43030CG'
    - - :warning
      - 'Line 5879: Product not found, record ignored., BaseItemCode=VF43040WB'
    - - :warning
      - 'Line 5889: Product not found, record ignored., BaseItemCode=VF43524MWH'
    - - :warning
      - 'Line 5898: Product not found, record ignored., BaseItemCode=VF43530MMP'
    - - :warning
      - 'Line 5899: Product not found, record ignored., BaseItemCode=VF43530MMP-BS'
    - - :warning
      - 'Line 5900: Product not found, record ignored., BaseItemCode=VF43530MTK'
    - - :warning
      - 'Line 5901: Product not found, record ignored., BaseItemCode=VF43530MTK-BS'
    - - :warning
      - 'Line 5920: Product not found, record ignored., BaseItemCode=VF43536MWT'
    - - :warning
      - 'Line 5921: Product not found, record ignored., BaseItemCode=VF43536MWT-BS'
    - - :warning
      - 'Line 5973: Product not found, record ignored., BaseItemCode=VF44524MMP'
    - - :warning
      - 'Line 5975: Product not found, record ignored., BaseItemCode=VF44524MTK'
    - - :warning
      - 'Line 5983: Product not found, record ignored., BaseItemCode=VF44530MWT'
    - - :warning
      - 'Line 5995: Product not found, record ignored., BaseItemCode=VF44536MWH'
    - - :warning
      - 'Line 6016: Product not found, record ignored., BaseItemCode=VF44548MMP'
    - - :warning
      - 'Line 6019: Product not found, record ignored., BaseItemCode=VF44548MWH'
    - - :warning
      - 'Line 6029: Product not found, record ignored., BaseItemCode=VF46030MBL'
    - - :warning
      - 'Line 6036: Product not found, record ignored., BaseItemCode=VF46036MBL'
    - - :warning
      - 'Line 6049: Product not found, record ignored., BaseItemCode=VF46048MBL'
    - - :warning
      - 'Line 6050: Product not found, record ignored., BaseItemCode=VF46048MMP'
    - - :warning
      - 'Line 6090: Product not found, record ignored., BaseItemCode=VF47042MBL'
    - - :warning
      - 'Line 6093: Product not found, record ignored., BaseItemCode=VF47042MMP'
    - - :warning
      - 'Line 6094: Product not found, record ignored., BaseItemCode=VF47042MMP-BS'
    - - :warning
      - 'Line 6115: Product not found, record ignored., BaseItemCode=VF48018MBL'
    - - :warning
      - 'Line 6117: Product not found, record ignored., BaseItemCode=VF48018MWH'
    - - :warning
      - 'Line 6118: Product not found, record ignored., BaseItemCode=VF48018MWT'
    - - :warning
      - 'Line 6119: Product not found, record ignored., BaseItemCode=VF48018NT'
    - - :warning
      - 'Line 6160: Product not found, record ignored., BaseItemCode=VF48060DMTK'
    - - :warning
      - 'Line 6167: Product not found, record ignored., BaseItemCode=VF48818MW'
    - - :warning
      - 'Line 6168: Product not found, record ignored., BaseItemCode=VF48818MWH'
    - - :warning
      - 'Line 6170: Product not found, record ignored., BaseItemCode=VF48818NT'
    - - :warning
      - 'Line 6196: Product not found, record ignored., BaseItemCode=VF48832MBL'
    - - :warning
      - 'Line 6197: Product not found, record ignored., BaseItemCode=VF48832MBL-BS'
    - - :warning
      - 'Line 6244: Product not found, record ignored., BaseItemCode=VF48848MBL'
    - - :warning
      - 'Line 6249: Product not found, record ignored., BaseItemCode=VF48848MWH'
    - - :warning
      - 'Line 6250: Product not found, record ignored., BaseItemCode=VF48848MWT'
    - - :warning
      - 'Line 6251: Product not found, record ignored., BaseItemCode=VF48848NT'
    - - :warning
      - 'Line 6305: Product not found, record ignored., BaseItemCode=VF50060DGN'
    - - :warning
      - 'Line 6328: Product not found, record ignored., BaseItemCode=VF53042GN'
    - - :warning
      - 'Line 6336: Product not found, record ignored., BaseItemCode=VF53060DBL'
    - - :warning
      - 'Line 6506: Product not found, record ignored., BaseItemCode=VF90242MGN'
    - - :warning
      - 'Line 6507: Product not found, record ignored., BaseItemCode=VF90242MGN-BS'
    - - :warning
      - 'Line 6516: Product not found, record ignored., BaseItemCode=VF90248MGN'
    - - :warning
      - 'Line 6517: Product not found, record ignored., BaseItemCode=VF90248MGN-BS'
    - - :warning
      - 'Line 6528: Product not found, record ignored., BaseItemCode=VM13236AB'
    - - :warning
      - 'Line 7012: Product not found, record ignored., BaseItemCode=MR6C2132BLK'
    - - :warning
      - 'Line 7478: Product not found, record ignored., BaseItemCode=W122-DB'
    - - :warning
      - 'Line 9461: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY01'
    - - :warning
      - 'Line 9462: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY02'
    - - :warning
      - 'Line 9463: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY03'
    - - :warning
      - 'Line 9464: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY04'
    - - :warning
      - 'Line 9465: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY06'
    - - :warning
      - 'Line 9466: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY07'
    - - :warning
      - 'Line 9467: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY20'
    - - :warning
      - 'Line 9468: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK01'
    - - :warning
      - 'Line 9469: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK02'
    - - :warning
      - 'Line 9470: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK03'
    - - :warning
      - 'Line 9471: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK04'
    - - :warning
      - 'Line 9472: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK05'
    - - :warning
      - 'Line 9473: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK20'
    - - :warning
      - 'Line 9474: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK21'
    - - :warning
      - 'Line 9475: Product not found, record ignored., BaseItemCode=LVFSN7-GRY01'
    - - :warning
      - 'Line 9476: Product not found, record ignored., BaseItemCode=LVFSN7-GRY02'
    - - :warning
      - 'Line 9477: Product not found, record ignored., BaseItemCode=LVFSN7-GRY03'
    - - :warning
      - 'Line 9478: Product not found, record ignored., BaseItemCode=LVFSN7-GRY04'
    - - :warning
      - 'Line 9479: Product not found, record ignored., BaseItemCode=LVFSN7-GRY06'
    - - :warning
      - 'Line 9480: Product not found, record ignored., BaseItemCode=LVFSN7-GRY07'
    - - :warning
      - 'Line 9481: Product not found, record ignored., BaseItemCode=LVFSN7-GRY20'
    - - :warning
      - 'Line 9482: Product not found, record ignored., BaseItemCode=LVFSN7-OAK01'
    - - :warning
      - 'Line 9483: Product not found, record ignored., BaseItemCode=LVFSN7-OAK02'
    - - :warning
      - 'Line 9484: Product not found, record ignored., BaseItemCode=LVFSN7-OAK03'
    - - :warning
      - 'Line 9485: Product not found, record ignored., BaseItemCode=LVFSN7-OAK04'
    - - :warning
      - 'Line 9486: Product not found, record ignored., BaseItemCode=LVFSN7-OAK05'
    - - :warning
      - 'Line 9487: Product not found, record ignored., BaseItemCode=LVFSN7-OAK20'
    - - :warning
      - 'Line 9488: Product not found, record ignored., BaseItemCode=LVFSN7-OAK21'
    - - :warning
      - 'Line 9489: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY01'
    - - :warning
      - 'Line 9490: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY02'
    - - :warning
      - 'Line 9491: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY03'
    - - :warning
      - 'Line 9492: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY04'
    - - :warning
      - 'Line 9493: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY06'
    - - :warning
      - 'Line 9494: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY07'
    - - :warning
      - 'Line 9495: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY20'
    - - :warning
      - 'Line 9496: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK01'
    - - :warning
      - 'Line 9497: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK02'
    - - :warning
      - 'Line 9498: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK03'
    - - :warning
      - 'Line 9499: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK04'
    - - :warning
      - 'Line 9500: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK05'
    - - :warning
      - 'Line 9501: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK20'
    - - :warning
      - 'Line 9502: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK21'
    - - :warning
      - 'Line 9503: Product not found, record ignored., BaseItemCode=LVRDM7-GRY01'
    - - :warning
      - 'Line 9504: Product not found, record ignored., BaseItemCode=LVRDM7-GRY02'
    - - :warning
      - 'Line 9505: Product not found, record ignored., BaseItemCode=LVRDM7-GRY03'
    - - :warning
      - 'Line 9506: Product not found, record ignored., BaseItemCode=LVRDM7-GRY04'
    - - :warning
      - 'Line 9507: Product not found, record ignored., BaseItemCode=LVRDM7-GRY06'
    - - :warning
      - 'Line 9508: Product not found, record ignored., BaseItemCode=LVRDM7-GRY07'
    - - :warning
      - 'Line 9509: Product not found, record ignored., BaseItemCode=LVRDM7-GRY20'
    - - :warning
      - 'Line 9510: Product not found, record ignored., BaseItemCode=LVRDM7-OAK01'
    - - :warning
      - 'Line 9511: Product not found, record ignored., BaseItemCode=LVRDM7-OAK02'
    - - :warning
      - 'Line 9512: Product not found, record ignored., BaseItemCode=LVRDM7-OAK03'
    - - :warning
      - 'Line 9513: Product not found, record ignored., BaseItemCode=LVRDM7-OAK04'
    - - :warning
      - 'Line 9514: Product not found, record ignored., BaseItemCode=LVRDM7-OAK05'
    - - :warning
      - 'Line 9515: Product not found, record ignored., BaseItemCode=LVRDM7-OAK20'
    - - :warning
      - 'Line 9516: Product not found, record ignored., BaseItemCode=LVRDM7-OAK21'
    - - :warning
      - 'Line 9517: Product not found, record ignored., BaseItemCode=LVST-GRY01'
    - - :warning
      - 'Line 9518: Product not found, record ignored., BaseItemCode=LVST-GRY02'
    - - :warning
      - 'Line 9519: Product not found, record ignored., BaseItemCode=LVST-GRY03'
    - - :warning
      - 'Line 9520: Product not found, record ignored., BaseItemCode=LVST-GRY04'
    - - :warning
      - 'Line 9521: Product not found, record ignored., BaseItemCode=LVST-GRY06'
    - - :warning
      - 'Line 9522: Product not found, record ignored., BaseItemCode=LVST-GRY07'
    - - :warning
      - 'Line 9523: Product not found, record ignored., BaseItemCode=LVST-GRY20'
    - - :warning
      - 'Line 9524: Product not found, record ignored., BaseItemCode=LVST-OAK01'
    - - :warning
      - 'Line 9525: Product not found, record ignored., BaseItemCode=LVST-OAK02'
    - - :warning
      - 'Line 9526: Product not found, record ignored., BaseItemCode=LVST-OAK03'
    - - :warning
      - 'Line 9527: Product not found, record ignored., BaseItemCode=LVST-OAK04'
    - - :warning
      - 'Line 9528: Product not found, record ignored., BaseItemCode=LVST-OAK05'
    - - :warning
      - 'Line 9529: Product not found, record ignored., BaseItemCode=LVST-OAK20'
    - - :warning
      - 'Line 9530: Product not found, record ignored., BaseItemCode=LVST-OAK21'
    - - :warning
      - 'Line 9531: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY01'
    - - :warning
      - 'Line 9532: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY02'
    - - :warning
      - 'Line 9533: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY03'
    - - :warning
      - 'Line 9534: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY04'
    - - :warning
      - 'Line 9535: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY06'
    - - :warning
      - 'Line 9536: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY07'
    - - :warning
      - 'Line 9537: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY20'
    - - :warning
      - 'Line 9538: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK01'
    - - :warning
      - 'Line 9539: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK02'
    - - :warning
      - 'Line 9540: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK03'
    - - :warning
      - 'Line 9541: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK04'
    - - :warning
      - 'Line 9542: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK05'
    - - :warning
      - 'Line 9543: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK20'
    - - :warning
      - 'Line 9544: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK21'
    - - :warning
      - 'Line 9545: Product not found, record ignored., BaseItemCode=LVTM7-GRY01'
    - - :warning
      - 'Line 9546: Product not found, record ignored., BaseItemCode=LVTM7-GRY02'
    - - :warning
      - 'Line 9547: Product not found, record ignored., BaseItemCode=LVTM7-GRY03'
    - - :warning
      - 'Line 9548: Product not found, record ignored., BaseItemCode=LVTM7-GRY04'
    - - :warning
      - 'Line 9549: Product not found, record ignored., BaseItemCode=LVTM7-GRY06'
    - - :warning
      - 'Line 9550: Product not found, record ignored., BaseItemCode=LVTM7-GRY07'
    - - :warning
      - 'Line 9551: Product not found, record ignored., BaseItemCode=LVTM7-GRY20'
    - - :warning
      - 'Line 9552: Product not found, record ignored., BaseItemCode=LVTM7-OAK01'
    - - :warning
      - 'Line 9553: Product not found, record ignored., BaseItemCode=LVTM7-OAK02'
    - - :warning
      - 'Line 9554: Product not found, record ignored., BaseItemCode=LVTM7-OAK03'
    - - :warning
      - 'Line 9555: Product not found, record ignored., BaseItemCode=LVTM7-OAK04'
    - - :warning
      - 'Line 9556: Product not found, record ignored., BaseItemCode=LVTM7-OAK05'
    - - :warning
      - 'Line 9557: Product not found, record ignored., BaseItemCode=LVTM7-OAK20'
    - - :warning
      - 'Line 9558: Product not found, record ignored., BaseItemCode=LVTM7-OAK21'
 |
| 2026-06-16 20:45:48 | ---
- - Inventory
  - - - :warning
      - 'Line 9: Product not found, record ignored., BaseItemCode=1101D28BR'
    - - :warning
      - 'Line 102: Product not found, record ignored., BaseItemCode=1107F18BR'
    - - :warning
      - 'Line 686: Product not found, record ignored., BaseItemCode=1451D20C'
    - - :warning
      - 'Line 687: Product not found, record ignored., BaseItemCode=1452D18PN'
    - - :warning
      - 'Line 694: Product not found, record ignored., BaseItemCode=1453D17DB'
    - - :warning
      - 'Line 695: Product not found, record ignored., BaseItemCode=1453W13PN'
    - - :warning
      - 'Line 696: Product not found, record ignored., BaseItemCode=1458D13BZ'
    - - :warning
      - 'Line 697: Product not found, record ignored., BaseItemCode=1458D13VN'
    - - :warning
      - 'Line 700: Product not found, record ignored., BaseItemCode=1461W13PN'
    - - :warning
      - 'Line 703: Product not found, record ignored., BaseItemCode=1471G44SL'
    - - :warning
      - 'Line 704: Product not found, record ignored., BaseItemCode=1472G39BB'
    - - :warning
      - 'Line 708: Product not found, record ignored., BaseItemCode=1473G52PN'
    - - :warning
      - 'Line 709: Product not found, record ignored., BaseItemCode=1485D15VN'
    - - :warning
      - 'Line 716: Product not found, record ignored., BaseItemCode=1503D18IW'
    - - :warning
      - 'Line 717: Product not found, record ignored., BaseItemCode=1504D35VN'
    - - :warning
      - 'Line 723: Product not found, record ignored., BaseItemCode=1512D9GI'
    - - :warning
      - 'Line 726: Product not found, record ignored., BaseItemCode=1537W5VB'
    - - :warning
      - 'Line 727: Product not found, record ignored., BaseItemCode=1702D18ASL'
    - - :warning
      - 'Line 731: Product not found, record ignored., BaseItemCode=1710D12FB'
    - - :warning
      - 'Line 817: Product not found, record ignored., BaseItemCode=2105W10C/RC'
    - - :warning
      - 'Line 826: Product not found, record ignored., BaseItemCode=2116D26C/RC'
    - - :warning
      - 'Line 827: Product not found, record ignored., BaseItemCode=2116D32C/RC'
    - - :warning
      - 'Line 828: Product not found, record ignored., BaseItemCode=2116G63C/RC'
    - - :warning
      - 'Line 831: Product not found, record ignored., BaseItemCode=2117W33C/RC'
    - - :warning
      - 'Line 1372: Product not found, record ignored., BaseItemCode=5100D5C'
    - - :warning
      - 'Line 1386: Product not found, record ignored., BaseItemCode=5200D32C'
    - - :warning
      - 'Line 1388: Product not found, record ignored., BaseItemCode=5200D36C'
    - - :warning
      - 'Line 1389: Product not found, record ignored., BaseItemCode=5200D42C'
    - - :warning
      - 'Line 1397: Product not found, record ignored., BaseItemCode=5201D5C'
    - - :warning
      - 'Line 1398: Product not found, record ignored., BaseItemCode=5202D22C'
    - - :warning
      - 'Line 1400: Product not found, record ignored., BaseItemCode=5202D24C'
    - - :warning
      - 'Line 1401: Product not found, record ignored., BaseItemCode=5202D24G'
    - - :warning
      - 'Line 1407: Product not found, record ignored., BaseItemCode=5203D16G'
    - - :warning
      - 'Line 1456: Product not found, record ignored., BaseItemCode=7872D17C'
    - - :warning
      - 'Line 1457: Product not found, record ignored., BaseItemCode=7872D17SS'
    - - :warning
      - 'Line 1589: Product not found, record ignored., BaseItemCode=BR20LED102-6PK'
    - - :warning
      - 'Line 1658: Product not found, record ignored., BaseItemCode=CF3004'
    - - :warning
      - 'Line 1812: Product not found, record ignored., BaseItemCode=KIT20204'
    - - :warning
      - 'Line 1813: Product not found, record ignored., BaseItemCode=KIT20402'
    - - :warning
      - 'Line 1814: Product not found, record ignored., BaseItemCode=KIT40606'
    - - :warning
      - 'Line 1815: Product not found, record ignored., BaseItemCode=KIT40804'
    - - :warning
      - 'Line 1882: Product not found, record ignored., BaseItemCode=LD2239C'
    - - :warning
      - 'Line 1919: Product not found, record ignored., BaseItemCode=LD2259BR'
    - - :warning
      - 'Line 1936: Product not found, record ignored., BaseItemCode=LD2274BK'
    - - :warning
      - 'Line 1938: Product not found, record ignored., BaseItemCode=LD2275BR'
    - - :warning
      - 'Line 1942: Product not found, record ignored., BaseItemCode=LD2277C'
    - - :warning
      - 'Line 1955: Product not found, record ignored., BaseItemCode=LD2300BR'
    - - :warning
      - 'Line 1958: Product not found, record ignored., BaseItemCode=LD2301BR'
    - - :warning
      - 'Line 1959: Product not found, record ignored., BaseItemCode=LD2301C'
    - - :warning
      - 'Line 1960: Product not found, record ignored., BaseItemCode=LD2302BK'
    - - :warning
      - 'Line 1961: Product not found, record ignored., BaseItemCode=LD2302BR'
    - - :warning
      - 'Line 1962: Product not found, record ignored., BaseItemCode=LD2302C'
    - - :warning
      - 'Line 1966: Product not found, record ignored., BaseItemCode=LD2304BK'
    - - :warning
      - 'Line 1969: Product not found, record ignored., BaseItemCode=LD2305BK'
    - - :warning
      - 'Line 1970: Product not found, record ignored., BaseItemCode=LD2305BR'
    - - :warning
      - 'Line 1971: Product not found, record ignored., BaseItemCode=LD2305C'
    - - :warning
      - 'Line 1972: Product not found, record ignored., BaseItemCode=LD2306BR'
    - - :warning
      - 'Line 1975: Product not found, record ignored., BaseItemCode=LD2307BR'
    - - :warning
      - 'Line 1979: Product not found, record ignored., BaseItemCode=LD2309C'
    - - :warning
      - 'Line 1980: Product not found, record ignored., BaseItemCode=LD2310BK'
    - - :warning
      - 'Line 1984: Product not found, record ignored., BaseItemCode=LD2311BR'
    - - :warning
      - 'Line 2037: Product not found, record ignored., BaseItemCode=LD2337BK'
    - - :warning
      - 'Line 2038: Product not found, record ignored., BaseItemCode=LD2337BR'
    - - :warning
      - 'Line 2039: Product not found, record ignored., BaseItemCode=LD2337C'
    - - :warning
      - 'Line 2040: Product not found, record ignored., BaseItemCode=LD2338BK'
    - - :warning
      - 'Line 2041: Product not found, record ignored., BaseItemCode=LD2338BR'
    - - :warning
      - 'Line 2042: Product not found, record ignored., BaseItemCode=LD2338C'
    - - :warning
      - 'Line 2043: Product not found, record ignored., BaseItemCode=LD2339BK'
    - - :warning
      - 'Line 2044: Product not found, record ignored., BaseItemCode=LD2339BR'
    - - :warning
      - 'Line 2045: Product not found, record ignored., BaseItemCode=LD2339C'
    - - :warning
      - 'Line 2046: Product not found, record ignored., BaseItemCode=LD2340BK'
    - - :warning
      - 'Line 2047: Product not found, record ignored., BaseItemCode=LD2340BR'
    - - :warning
      - 'Line 2048: Product not found, record ignored., BaseItemCode=LD2340C'
    - - :warning
      - 'Line 2049: Product not found, record ignored., BaseItemCode=LD2341BR'
    - - :warning
      - 'Line 2050: Product not found, record ignored., BaseItemCode=LD2344BK'
    - - :warning
      - 'Line 2051: Product not found, record ignored., BaseItemCode=LD2344BR'
    - - :warning
      - 'Line 2063: Product not found, record ignored., BaseItemCode=LD2350BK'
    - - :warning
      - 'Line 2064: Product not found, record ignored., BaseItemCode=LD2350BR'
    - - :warning
      - 'Line 2068: Product not found, record ignored., BaseItemCode=LD2352BK'
    - - :warning
      - 'Line 2069: Product not found, record ignored., BaseItemCode=LD2352BR'
    - - :warning
      - 'Line 2096: Product not found, record ignored., BaseItemCode=LD2363BK'
    - - :warning
      - 'Line 2097: Product not found, record ignored., BaseItemCode=LD2363BR'
    - - :warning
      - 'Line 2098: Product not found, record ignored., BaseItemCode=LD2364BK'
    - - :warning
      - 'Line 2099: Product not found, record ignored., BaseItemCode=LD2364BR'
    - - :warning
      - 'Line 2100: Product not found, record ignored., BaseItemCode=LD2364RED'
    - - :warning
      - 'Line 2101: Product not found, record ignored., BaseItemCode=LD2364WH'
    - - :warning
      - 'Line 2102: Product not found, record ignored., BaseItemCode=LD2365BK'
    - - :warning
      - 'Line 2103: Product not found, record ignored., BaseItemCode=LD2365BR'
    - - :warning
      - 'Line 2108: Product not found, record ignored., BaseItemCode=LD2367WH'
    - - :warning
      - 'Line 2110: Product not found, record ignored., BaseItemCode=LD2401WH'
    - - :warning
      - 'Line 2113: Product not found, record ignored., BaseItemCode=LD2404BN'
    - - :warning
      - 'Line 2115: Product not found, record ignored., BaseItemCode=LD2405HG'
    - - :warning
      - 'Line 2119: Product not found, record ignored., BaseItemCode=LD2407HG'
    - - :warning
      - 'Line 2126: Product not found, record ignored., BaseItemCode=LD2410WH'
    - - :warning
      - 'Line 2127: Product not found, record ignored., BaseItemCode=LD2411HG'
    - - :warning
      - 'Line 2128: Product not found, record ignored., BaseItemCode=LD2412WH'
    - - :warning
      - 'Line 2134: Product not found, record ignored., BaseItemCode=LD2450BK'
    - - :warning
      - 'Line 2135: Product not found, record ignored., BaseItemCode=LD2450BR'
    - - :warning
      - 'Line 2136: Product not found, record ignored., BaseItemCode=LD2450C'
    - - :warning
      - 'Line 2140: Product not found, record ignored., BaseItemCode=LD2453FLBK'
    - - :warning
      - 'Line 2141: Product not found, record ignored., BaseItemCode=LD2453FLBR'
    - - :warning
      - 'Line 2142: Product not found, record ignored., BaseItemCode=LD2453FLCG'
    - - :warning
      - 'Line 2158: Product not found, record ignored., BaseItemCode=LD4008D11BK'
    - - :warning
      - 'Line 2164: Product not found, record ignored., BaseItemCode=LD4017D48BRB'
    - - :warning
      - 'Line 2291: Product not found, record ignored., BaseItemCode=LD5016D17BK'
    - - :warning
      - 'Line 2302: Product not found, record ignored., BaseItemCode=LD5023'
    - - :warning
      - 'Line 2370: Product not found, record ignored., BaseItemCode=LD520D10BK'
    - - :warning
      - 'Line 2371: Product not found, record ignored., BaseItemCode=LD520D10BR'
    - - :warning
      - 'Line 2372: Product not found, record ignored., BaseItemCode=LD520D10C'
    - - :warning
      - 'Line 2373: Product not found, record ignored., BaseItemCode=LD520D13BK'
    - - :warning
      - 'Line 2374: Product not found, record ignored., BaseItemCode=LD520D13BR'
    - - :warning
      - 'Line 2375: Product not found, record ignored., BaseItemCode=LD520D13C'
    - - :warning
      - 'Line 2376: Product not found, record ignored., BaseItemCode=LD520D16BK'
    - - :warning
      - 'Line 2377: Product not found, record ignored., BaseItemCode=LD520D16BR'
    - - :warning
      - 'Line 2378: Product not found, record ignored., BaseItemCode=LD520D16C'
    - - :warning
      - 'Line 2379: Product not found, record ignored., BaseItemCode=LD520D18BK'
    - - :warning
      - 'Line 2380: Product not found, record ignored., BaseItemCode=LD520D18BR'
    - - :warning
      - 'Line 2381: Product not found, record ignored., BaseItemCode=LD520D18C'
    - - :warning
      - 'Line 2382: Product not found, record ignored., BaseItemCode=LD520D20BR'
    - - :warning
      - 'Line 2391: Product not found, record ignored., BaseItemCode=LD6005D12BR'
    - - :warning
      - 'Line 2408: Product not found, record ignored., BaseItemCode=LD6010D26BN'
    - - :warning
      - 'Line 2414: Product not found, record ignored., BaseItemCode=LD6012D15G'
    - - :warning
      - 'Line 2425: Product not found, record ignored., BaseItemCode=LD6016'
    - - :warning
      - 'Line 2471: Product not found, record ignored., BaseItemCode=LD6077C'
    - - :warning
      - 'Line 2481: Product not found, record ignored., BaseItemCode=LD6100C'
    - - :warning
      - 'Line 2495: Product not found, record ignored., BaseItemCode=LD6109BR'
    - - :warning
      - 'Line 2502: Product not found, record ignored., BaseItemCode=LD6124C'
    - - :warning
      - 'Line 2509: Product not found, record ignored., BaseItemCode=LD6133BR'
    - - :warning
      - 'Line 2537: Product not found, record ignored., BaseItemCode=LD6170C'
    - - :warning
      - 'Line 2540: Product not found, record ignored., BaseItemCode=LD6173BR'
    - - :warning
      - 'Line 2543: Product not found, record ignored., BaseItemCode=LD6176C'
    - - :warning
      - 'Line 2544: Product not found, record ignored., BaseItemCode=LD6178BR'
    - - :warning
      - 'Line 2558: Product not found, record ignored., BaseItemCode=LD6205C'
    - - :warning
      - 'Line 2568: Product not found, record ignored., BaseItemCode=LD6220C'
    - - :warning
      - 'Line 2574: Product not found, record ignored., BaseItemCode=LD6232C'
    - - :warning
      - 'Line 2575: Product not found, record ignored., BaseItemCode=LD6238C'
    - - :warning
      - 'Line 2581: Product not found, record ignored., BaseItemCode=LD6248BR'
    - - :warning
      - 'Line 2587: Product not found, record ignored., BaseItemCode=LD6259C'
    - - :warning
      - 'Line 2603: Product not found, record ignored., BaseItemCode=LD642D36BR'
    - - :warning
      - 'Line 2604: Product not found, record ignored., BaseItemCode=LD642D36BRK'
    - - :warning
      - 'Line 2605: Product not found, record ignored., BaseItemCode=LD643D36BK'
    - - :warning
      - 'Line 2620: Product not found, record ignored., BaseItemCode=LD648F26BK'
    - - :warning
      - 'Line 2622: Product not found, record ignored., BaseItemCode=LD648F26BRK'
    - - :warning
      - 'Line 2633: Product not found, record ignored., BaseItemCode=LD652D30BR'
    - - :warning
      - 'Line 2642: Product not found, record ignored., BaseItemCode=LD655D18BR'
    - - :warning
      - 'Line 2643: Product not found, record ignored., BaseItemCode=LD655D18BRK'
    - - :warning
      - 'Line 2650: Product not found, record ignored., BaseItemCode=LD6802D14C'
    - - :warning
      - 'Line 2683: Product not found, record ignored., BaseItemCode=LD7024D25BK'
    - - :warning
      - 'Line 2685: Product not found, record ignored., BaseItemCode=LD7024D25SN'
    - - :warning
      - 'Line 2752: Product not found, record ignored., BaseItemCode=LD7044D26WD'
    - - :warning
      - 'Line 2760: Product not found, record ignored., BaseItemCode=LD7047D28BR'
    - - :warning
      - 'Line 2779: Product not found, record ignored., BaseItemCode=LD7057D20BK'
    - - :warning
      - 'Line 2809: Product not found, record ignored., BaseItemCode=LD7071D14BK'
    - - :warning
      - 'Line 2879: Product not found, record ignored., BaseItemCode=LD7301W15CH'
    - - :warning
      - 'Line 2892: Product not found, record ignored., BaseItemCode=LD7302W24BLK'
    - - :warning
      - 'Line 2900: Product not found, record ignored., BaseItemCode=LD7302W6CH'
    - - :warning
      - 'Line 2917: Product not found, record ignored., BaseItemCode=LD7304W22BRA'
    - - :warning
      - 'Line 2922: Product not found, record ignored., BaseItemCode=LD7304W7BLK'
    - - :warning
      - 'Line 2942: Product not found, record ignored., BaseItemCode=LD7307W24CH'
    - - :warning
      - 'Line 2976: Product not found, record ignored., BaseItemCode=LD7310W23BLK'
    - - :warning
      - 'Line 3147: Product not found, record ignored., BaseItemCode=LD7327W6BLK'
    - - :warning
      - 'Line 3159: Product not found, record ignored., BaseItemCode=LD7331W7BLK'
    - - :warning
      - 'Line 3218: Product not found, record ignored., BaseItemCode=LD8049D10BR'
    - - :warning
      - 'Line 3240: Product not found, record ignored., BaseItemCode=LD810F19SL'
    - - :warning
      - 'Line 3293: Product not found, record ignored., BaseItemCode=LD8801D43GB'
    - - :warning
      - 'Line 3323: Product not found, record ignored., BaseItemCode=LDOD3004-6PK'
    - - :warning
      - 'Line 3324: Product not found, record ignored., BaseItemCode=LDOD3006-4PK'
    - - :warning
      - 'Line 3339: Product not found, record ignored., BaseItemCode=LDOD4010BK'
    - - :warning
      - 'Line 3341: Product not found, record ignored., BaseItemCode=LDOD4011BK'
    - - :warning
      - 'Line 3343: Product not found, record ignored., BaseItemCode=LDOD4011WH'
    - - :warning
      - 'Line 3347: Product not found, record ignored., BaseItemCode=LDOD4013WH'
    - - :warning
      - 'Line 3354: Product not found, record ignored., BaseItemCode=LDOD4016BK'
    - - :warning
      - 'Line 3356: Product not found, record ignored., BaseItemCode=LDOD4016WH'
    - - :warning
      - 'Line 3395: Product not found, record ignored., BaseItemCode=LDPD2000BN'
    - - :warning
      - 'Line 3403: Product not found, record ignored., BaseItemCode=LDPD2003BN'
    - - :warning
      - 'Line 3409: Product not found, record ignored., BaseItemCode=LDPD2017'
    - - :warning
      - 'Line 3424: Product not found, record ignored., BaseItemCode=LDPD2045HG'
    - - :warning
      - 'Line 3427: Product not found, record ignored., BaseItemCode=LDPD2046WH'
    - - :warning
      - 'Line 3474: Product not found, record ignored., BaseItemCode=LDPG2256BK'
    - - :warning
      - 'Line 3475: Product not found, record ignored., BaseItemCode=LDPG2256BR'
    - - :warning
      - 'Line 3483: Product not found, record ignored., BaseItemCode=LDPG6037BR'
    - - :warning
      - 'Line 3499: Product not found, record ignored., BaseItemCode=MF53047BL'
    - - :warning
      - 'Line 3509: Product not found, record ignored., BaseItemCode=MF6-1008S'
    - - :warning
      - 'Line 3517: Product not found, record ignored., BaseItemCode=MF6-1036AW'
    - - :warning
      - 'Line 3518: Product not found, record ignored., BaseItemCode=MF6-1036BL'
    - - :warning
      - 'Line 3523: Product not found, record ignored., BaseItemCode=MF61060AW'
    - - :warning
      - 'Line 3524: Product not found, record ignored., BaseItemCode=MF61060AW-F1'
    - - :warning
      - 'Line 3525: Product not found, record ignored., BaseItemCode=MF61072BL'
    - - :warning
      - 'Line 3585: Product not found, record ignored., BaseItemCode=MF72038BK'
    - - :warning
      - 'Line 3597: Product not found, record ignored., BaseItemCode=MF73016BK'
    - - :warning
      - 'Line 3616: Product not found, record ignored., BaseItemCode=MF82002WH'
    - - :warning
      - 'Line 3623: Invalid next scheduled receipt date'
    - - :warning
      - 'Line 3842: Product not found, record ignored., BaseItemCode=MR33248BL'
    - - :warning
      - 'Line 3843: Product not found, record ignored., BaseItemCode=MR33272BL'
    - - :warning
      - 'Line 3865: Product not found, record ignored., BaseItemCode=MR4044WH'
    - - :warning
      - 'Line 3875: Product not found, record ignored., BaseItemCode=MR4054GR'
    - - :warning
      - 'Line 3894: Product not found, record ignored., BaseItemCode=MR4071BL'
    - - :warning
      - 'Line 3916: Product not found, record ignored., BaseItemCode=MR41828BL'
    - - :warning
      - 'Line 3924: Product not found, record ignored., BaseItemCode=MR42036BL'
    - - :warning
      - 'Line 3937: Product not found, record ignored., BaseItemCode=MR42736BL'
    - - :warning
      - 'Line 3994: Product not found, record ignored., BaseItemCode=MR4718BL'
    - - :warning
      - 'Line 3998: Product not found, record ignored., BaseItemCode=MR4721BL'
    - - :warning
      - 'Line 4000: Product not found, record ignored., BaseItemCode=MR4721GR'
    - - :warning
      - 'Line 4035: Product not found, record ignored., BaseItemCode=MR52736'
    - - :warning
      - 'Line 4036: Product not found, record ignored., BaseItemCode=MR53648'
    - - :warning
      - 'Line 4037: Product not found, record ignored., BaseItemCode=MR53660'
    - - :warning
      - 'Line 4058: Product not found, record ignored., BaseItemCode=MR652828BK'
    - - :warning
      - 'Line 4147: Product not found, record ignored., BaseItemCode=MR913240'
    - - :warning
      - 'Line 4155: Invalid next scheduled receipt date'
    - - :warning
      - 'Line 4156: Product not found, record ignored., BaseItemCode=MR9239'
    - - :warning
      - 'Line 4190: Product not found, record ignored., BaseItemCode=MRE32432BK'
    - - :warning
      - 'Line 4193: Product not found, record ignored., BaseItemCode=MRE32471BK'
    - - :warning
      - 'Line 4209: Product not found, record ignored., BaseItemCode=MRE52036'
    - - :warning
      - 'Line 4210: Product not found, record ignored., BaseItemCode=MRE52040'
    - - :warning
      - 'Line 4211: Product not found, record ignored., BaseItemCode=MRE52436'
    - - :warning
      - 'Line 4212: Product not found, record ignored., BaseItemCode=MRE52440'
    - - :warning
      - 'Line 4213: Product not found, record ignored., BaseItemCode=MRE52730'
    - - :warning
      - 'Line 4214: Product not found, record ignored., BaseItemCode=MRE52736'
    - - :warning
      - 'Line 4215: Product not found, record ignored., BaseItemCode=MRE52740'
    - - :warning
      - 'Line 4216: Product not found, record ignored., BaseItemCode=MRE53030'
    - - :warning
      - 'Line 4217: Product not found, record ignored., BaseItemCode=MRE53072'
    - - :warning
      - 'Line 4218: Product not found, record ignored., BaseItemCode=MRE53648'
    - - :warning
      - 'Line 4219: Product not found, record ignored., BaseItemCode=MRE54260'
    - - :warning
      - 'Line 4302: Product not found, record ignored., BaseItemCode=MRE92030'
    - - :warning
      - 'Line 4303: Product not found, record ignored., BaseItemCode=MRE92436'
    - - :warning
      - 'Line 4306: Product not found, record ignored., BaseItemCode=MRE93248'
    - - :warning
      - 'Line 4307: Product not found, record ignored., BaseItemCode=MRE93272'
    - - :warning
      - 'Line 4414: Product not found, record ignored., BaseItemCode=RN61550RF-4PK'
    - - :warning
      - 'Line 4415: Product not found, record ignored., BaseItemCode=RS41050SDK-4PK'
    - - :warning
      - 'Line 4484: Product not found, record ignored., BaseItemCode=TC5R-E26-6PK'
    - - :warning
      - 'Line 4485: Product not found, record ignored., BaseItemCode=TC6R-E26-6PK'
    - - :warning
      - 'Line 4505: Product not found, record ignored., BaseItemCode=TKACP-MW'
    - - :warning
      - 'Line 4506: Product not found, record ignored., BaseItemCode=TKAEF-MW'
    - - :warning
      - 'Line 4507: Product not found, record ignored., BaseItemCode=TKAFCF-BK'
    - - :warning
      - 'Line 4508: Product not found, record ignored., BaseItemCode=TKALC-BK'
    - - :warning
      - 'Line 4509: Product not found, record ignored., BaseItemCode=TKATC-BK'
    - - :warning
      - 'Line 4510: Product not found, record ignored., BaseItemCode=TKATC-MW'
    - - :warning
      - 'Line 4511: Product not found, record ignored., BaseItemCode=TKH210BK-6PK'
    - - :warning
      - 'Line 4512: Product not found, record ignored., BaseItemCode=TKL4BK'
    - - :warning
      - 'Line 4513: Product not found, record ignored., BaseItemCode=TKL4MW'
    - - :warning
      - 'Line 4525: Product not found, record ignored., BaseItemCode=V1800D24BK/RC'
    - - :warning
      - 'Line 4603: Product not found, record ignored., BaseItemCode=V1803W12SG/RC'
    - - :warning
      - 'Line 4638: Product not found, record ignored., BaseItemCode=V2006F14C/RC'
    - - :warning
      - 'Line 4640: Product not found, record ignored., BaseItemCode=V2006F16C/RC'
    - - :warning
      - 'Line 4648: Product not found, record ignored., BaseItemCode=V2011D21G/RC'
    - - :warning
      - 'Line 4705: Product not found, record ignored., BaseItemCode=V2032D24C/RC'
    - - :warning
      - 'Line 4711: Product not found, record ignored., BaseItemCode=V2032F14C/RC'
    - - :warning
      - 'Line 4718: Product not found, record ignored., BaseItemCode=V2032W30BK/RC'
    - - :warning
      - 'Line 4719: Product not found, record ignored., BaseItemCode=V2032W36BK/RC'
    - - :warning
      - 'Line 4724: Product not found, record ignored., BaseItemCode=V2033D24C/RC'
    - - :warning
      - 'Line 4726: Product not found, record ignored., BaseItemCode=V2033F14C/RC'
    - - :warning
      - 'Line 4733: Product not found, record ignored., BaseItemCode=V2034D28C/RC'
    - - :warning
      - 'Line 4736: Product not found, record ignored., BaseItemCode=V2035D28C/RC'
    - - :warning
      - 'Line 4737: Product not found, record ignored., BaseItemCode=V2075D18C/RC'
    - - :warning
      - 'Line 4748: Product not found, record ignored., BaseItemCode=V2100D35C/RC'
    - - :warning
      - 'Line 4796: Product not found, record ignored., BaseItemCode=V3100D40C/RC'
    - - :warning
      - 'Line 4798: Product not found, record ignored., BaseItemCode=V6801D14C/RC'
    - - :warning
      - 'Line 4799: Product not found, record ignored., BaseItemCode=V6801D19G/RC'
    - - :warning
      - 'Line 4801: Product not found, record ignored., BaseItemCode=V7803D11B-JT/RC'
    - - :warning
      - 'Line 4805: Product not found, record ignored., BaseItemCode=V7804D15GS-GS/RC'
    - - :warning
      - 'Line 4807: Product not found, record ignored., BaseItemCode=V7804D15PE/RC'
    - - :warning
      - 'Line 4808: Product not found, record ignored., BaseItemCode=V7804D15PK-RO/RC'
    - - :warning
      - 'Line 4882: Product not found, record ignored., BaseItemCode=V9800D20G/RC'
    - - :warning
      - 'Line 4883: Product not found, record ignored., BaseItemCode=V9800D24C/RC'
    - - :warning
      - 'Line 4884: Product not found, record ignored., BaseItemCode=V9800D24G/RC'
    - - :warning
      - 'Line 4885: Product not found, record ignored., BaseItemCode=V9800D28C/RC'
    - - :warning
      - 'Line 4894: Product not found, record ignored., BaseItemCode=V9805F10BK/RC'
    - - :warning
      - 'Line 4895: Product not found, record ignored., BaseItemCode=V9805F10C/RC'
    - - :warning
      - 'Line 4896: Product not found, record ignored., BaseItemCode=V9805F10G/RC'
    - - :warning
      - 'Line 4969: Product not found, record ignored., BaseItemCode=VF-1030VM'
    - - :warning
      - 'Line 4999: Product not found, record ignored., BaseItemCode=VF12319GR'
    - - :warning
      - 'Line 5030: Product not found, record ignored., BaseItemCode=VF12360DGR-VW'
    - - :warning
      - 'Line 5148: Product not found, record ignored., BaseItemCode=VF13060DAB-VW'
    - - :warning
      - 'Line 5153: Product not found, record ignored., BaseItemCode=VF13060DVM-VW'
    - - :warning
      - 'Line 5192: Product not found, record ignored., BaseItemCode=VF15032GN'
    - - :warning
      - 'Line 5328: Product not found, record ignored., BaseItemCode=VF17018WH'
    - - :warning
      - 'Line 5581: Product not found, record ignored., BaseItemCode=VF27048GN'
    - - :warning
      - 'Line 5769: Product not found, record ignored., BaseItemCode=VF41048MGN'
    - - :warning
      - 'Line 5799: Product not found, record ignored., BaseItemCode=VF42524MGN'
    - - :warning
      - 'Line 5800: Product not found, record ignored., BaseItemCode=VF42524MMP'
    - - :warning
      - 'Line 5872: Product not found, record ignored., BaseItemCode=VF43030CG'
    - - :warning
      - 'Line 5879: Product not found, record ignored., BaseItemCode=VF43040WB'
    - - :warning
      - 'Line 5889: Product not found, record ignored., BaseItemCode=VF43524MWH'
    - - :warning
      - 'Line 5898: Product not found, record ignored., BaseItemCode=VF43530MMP'
    - - :warning
      - 'Line 5899: Product not found, record ignored., BaseItemCode=VF43530MMP-BS'
    - - :warning
      - 'Line 5900: Product not found, record ignored., BaseItemCode=VF43530MTK'
    - - :warning
      - 'Line 5901: Product not found, record ignored., BaseItemCode=VF43530MTK-BS'
    - - :warning
      - 'Line 5920: Product not found, record ignored., BaseItemCode=VF43536MWT'
    - - :warning
      - 'Line 5921: Product not found, record ignored., BaseItemCode=VF43536MWT-BS'
    - - :warning
      - 'Line 5973: Product not found, record ignored., BaseItemCode=VF44524MMP'
    - - :warning
      - 'Line 5975: Product not found, record ignored., BaseItemCode=VF44524MTK'
    - - :warning
      - 'Line 5983: Product not found, record ignored., BaseItemCode=VF44530MWT'
    - - :warning
      - 'Line 5995: Product not found, record ignored., BaseItemCode=VF44536MWH'
    - - :warning
      - 'Line 6016: Product not found, record ignored., BaseItemCode=VF44548MMP'
    - - :warning
      - 'Line 6019: Product not found, record ignored., BaseItemCode=VF44548MWH'
    - - :warning
      - 'Line 6029: Product not found, record ignored., BaseItemCode=VF46030MBL'
    - - :warning
      - 'Line 6036: Product not found, record ignored., BaseItemCode=VF46036MBL'
    - - :warning
      - 'Line 6049: Product not found, record ignored., BaseItemCode=VF46048MBL'
    - - :warning
      - 'Line 6050: Product not found, record ignored., BaseItemCode=VF46048MMP'
    - - :warning
      - 'Line 6090: Product not found, record ignored., BaseItemCode=VF47042MBL'
    - - :warning
      - 'Line 6093: Product not found, record ignored., BaseItemCode=VF47042MMP'
    - - :warning
      - 'Line 6094: Product not found, record ignored., BaseItemCode=VF47042MMP-BS'
    - - :warning
      - 'Line 6115: Product not found, record ignored., BaseItemCode=VF48018MBL'
    - - :warning
      - 'Line 6117: Product not found, record ignored., BaseItemCode=VF48018MWH'
    - - :warning
      - 'Line 6118: Product not found, record ignored., BaseItemCode=VF48018MWT'
    - - :warning
      - 'Line 6119: Product not found, record ignored., BaseItemCode=VF48018NT'
    - - :warning
      - 'Line 6160: Product not found, record ignored., BaseItemCode=VF48060DMTK'
    - - :warning
      - 'Line 6167: Product not found, record ignored., BaseItemCode=VF48818MW'
    - - :warning
      - 'Line 6168: Product not found, record ignored., BaseItemCode=VF48818MWH'
    - - :warning
      - 'Line 6170: Product not found, record ignored., BaseItemCode=VF48818NT'
    - - :warning
      - 'Line 6196: Product not found, record ignored., BaseItemCode=VF48832MBL'
    - - :warning
      - 'Line 6197: Product not found, record ignored., BaseItemCode=VF48832MBL-BS'
    - - :warning
      - 'Line 6244: Product not found, record ignored., BaseItemCode=VF48848MBL'
    - - :warning
      - 'Line 6249: Product not found, record ignored., BaseItemCode=VF48848MWH'
    - - :warning
      - 'Line 6250: Product not found, record ignored., BaseItemCode=VF48848MWT'
    - - :warning
      - 'Line 6251: Product not found, record ignored., BaseItemCode=VF48848NT'
    - - :warning
      - 'Line 6305: Product not found, record ignored., BaseItemCode=VF50060DGN'
    - - :warning
      - 'Line 6328: Product not found, record ignored., BaseItemCode=VF53042GN'
    - - :warning
      - 'Line 6336: Product not found, record ignored., BaseItemCode=VF53060DBL'
    - - :warning
      - 'Line 6506: Product not found, record ignored., BaseItemCode=VF90242MGN'
    - - :warning
      - 'Line 6507: Product not found, record ignored., BaseItemCode=VF90242MGN-BS'
    - - :warning
      - 'Line 6516: Product not found, record ignored., BaseItemCode=VF90248MGN'
    - - :warning
      - 'Line 6517: Product not found, record ignored., BaseItemCode=VF90248MGN-BS'
    - - :warning
      - 'Line 6528: Product not found, record ignored., BaseItemCode=VM13236AB'
    - - :warning
      - 'Line 7012: Product not found, record ignored., BaseItemCode=MR6C2132BLK'
    - - :warning
      - 'Line 7478: Product not found, record ignored., BaseItemCode=W122-DB'
    - - :warning
      - 'Line 9461: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY01'
    - - :warning
      - 'Line 9462: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY02'
    - - :warning
      - 'Line 9463: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY03'
    - - :warning
      - 'Line 9464: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY04'
    - - :warning
      - 'Line 9465: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY06'
    - - :warning
      - 'Line 9466: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY07'
    - - :warning
      - 'Line 9467: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY20'
    - - :warning
      - 'Line 9468: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK01'
    - - :warning
      - 'Line 9469: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK02'
    - - :warning
      - 'Line 9470: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK03'
    - - :warning
      - 'Line 9471: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK04'
    - - :warning
      - 'Line 9472: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK05'
    - - :warning
      - 'Line 9473: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK20'
    - - :warning
      - 'Line 9474: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK21'
    - - :warning
      - 'Line 9475: Product not found, record ignored., BaseItemCode=LVFSN7-GRY01'
    - - :warning
      - 'Line 9476: Product not found, record ignored., BaseItemCode=LVFSN7-GRY02'
    - - :warning
      - 'Line 9477: Product not found, record ignored., BaseItemCode=LVFSN7-GRY03'
    - - :warning
      - 'Line 9478: Product not found, record ignored., BaseItemCode=LVFSN7-GRY04'
    - - :warning
      - 'Line 9479: Product not found, record ignored., BaseItemCode=LVFSN7-GRY06'
    - - :warning
      - 'Line 9480: Product not found, record ignored., BaseItemCode=LVFSN7-GRY07'
    - - :warning
      - 'Line 9481: Product not found, record ignored., BaseItemCode=LVFSN7-GRY20'
    - - :warning
      - 'Line 9482: Product not found, record ignored., BaseItemCode=LVFSN7-OAK01'
    - - :warning
      - 'Line 9483: Product not found, record ignored., BaseItemCode=LVFSN7-OAK02'
    - - :warning
      - 'Line 9484: Product not found, record ignored., BaseItemCode=LVFSN7-OAK03'
    - - :warning
      - 'Line 9485: Product not found, record ignored., BaseItemCode=LVFSN7-OAK04'
    - - :warning
      - 'Line 9486: Product not found, record ignored., BaseItemCode=LVFSN7-OAK05'
    - - :warning
      - 'Line 9487: Product not found, record ignored., BaseItemCode=LVFSN7-OAK20'
    - - :warning
      - 'Line 9488: Product not found, record ignored., BaseItemCode=LVFSN7-OAK21'
    - - :warning
      - 'Line 9489: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY01'
    - - :warning
      - 'Line 9490: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY02'
    - - :warning
      - 'Line 9491: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY03'
    - - :warning
      - 'Line 9492: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY04'
    - - :warning
      - 'Line 9493: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY06'
    - - :warning
      - 'Line 9494: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY07'
    - - :warning
      - 'Line 9495: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY20'
    - - :warning
      - 'Line 9496: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK01'
    - - :warning
      - 'Line 9497: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK02'
    - - :warning
      - 'Line 9498: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK03'
    - - :warning
      - 'Line 9499: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK04'
    - - :warning
      - 'Line 9500: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK05'
    - - :warning
      - 'Line 9501: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK20'
    - - :warning
      - 'Line 9502: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK21'
    - - :warning
      - 'Line 9503: Product not found, record ignored., BaseItemCode=LVRDM7-GRY01'
    - - :warning
      - 'Line 9504: Product not found, record ignored., BaseItemCode=LVRDM7-GRY02'
    - - :warning
      - 'Line 9505: Product not found, record ignored., BaseItemCode=LVRDM7-GRY03'
    - - :warning
      - 'Line 9506: Product not found, record ignored., BaseItemCode=LVRDM7-GRY04'
    - - :warning
      - 'Line 9507: Product not found, record ignored., BaseItemCode=LVRDM7-GRY06'
    - - :warning
      - 'Line 9508: Product not found, record ignored., BaseItemCode=LVRDM7-GRY07'
    - - :warning
      - 'Line 9509: Product not found, record ignored., BaseItemCode=LVRDM7-GRY20'
    - - :warning
      - 'Line 9510: Product not found, record ignored., BaseItemCode=LVRDM7-OAK01'
    - - :warning
      - 'Line 9511: Product not found, record ignored., BaseItemCode=LVRDM7-OAK02'
    - - :warning
      - 'Line 9512: Product not found, record ignored., BaseItemCode=LVRDM7-OAK03'
    - - :warning
      - 'Line 9513: Product not found, record ignored., BaseItemCode=LVRDM7-OAK04'
    - - :warning
      - 'Line 9514: Product not found, record ignored., BaseItemCode=LVRDM7-OAK05'
    - - :warning
      - 'Line 9515: Product not found, record ignored., BaseItemCode=LVRDM7-OAK20'
    - - :warning
      - 'Line 9516: Product not found, record ignored., BaseItemCode=LVRDM7-OAK21'
    - - :warning
      - 'Line 9517: Product not found, record ignored., BaseItemCode=LVST-GRY01'
    - - :warning
      - 'Line 9518: Product not found, record ignored., BaseItemCode=LVST-GRY02'
    - - :warning
      - 'Line 9519: Product not found, record ignored., BaseItemCode=LVST-GRY03'
    - - :warning
      - 'Line 9520: Product not found, record ignored., BaseItemCode=LVST-GRY04'
    - - :warning
      - 'Line 9521: Product not found, record ignored., BaseItemCode=LVST-GRY06'
    - - :warning
      - 'Line 9522: Product not found, record ignored., BaseItemCode=LVST-GRY07'
    - - :warning
      - 'Line 9523: Product not found, record ignored., BaseItemCode=LVST-GRY20'
    - - :warning
      - 'Line 9524: Product not found, record ignored., BaseItemCode=LVST-OAK01'
    - - :warning
      - 'Line 9525: Product not found, record ignored., BaseItemCode=LVST-OAK02'
    - - :warning
      - 'Line 9526: Product not found, record ignored., BaseItemCode=LVST-OAK03'
    - - :warning
      - 'Line 9527: Product not found, record ignored., BaseItemCode=LVST-OAK04'
    - - :warning
      - 'Line 9528: Product not found, record ignored., BaseItemCode=LVST-OAK05'
    - - :warning
      - 'Line 9529: Product not found, record ignored., BaseItemCode=LVST-OAK20'
    - - :warning
      - 'Line 9530: Product not found, record ignored., BaseItemCode=LVST-OAK21'
    - - :warning
      - 'Line 9531: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY01'
    - - :warning
      - 'Line 9532: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY02'
    - - :warning
      - 'Line 9533: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY03'
    - - :warning
      - 'Line 9534: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY04'
    - - :warning
      - 'Line 9535: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY06'
    - - :warning
      - 'Line 9536: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY07'
    - - :warning
      - 'Line 9537: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY20'
    - - :warning
      - 'Line 9538: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK01'
    - - :warning
      - 'Line 9539: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK02'
    - - :warning
      - 'Line 9540: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK03'
    - - :warning
      - 'Line 9541: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK04'
    - - :warning
      - 'Line 9542: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK05'
    - - :warning
      - 'Line 9543: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK20'
    - - :warning
      - 'Line 9544: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK21'
    - - :warning
      - 'Line 9545: Product not found, record ignored., BaseItemCode=LVTM7-GRY01'
    - - :warning
      - 'Line 9546: Product not found, record ignored., BaseItemCode=LVTM7-GRY02'
    - - :warning
      - 'Line 9547: Product not found, record ignored., BaseItemCode=LVTM7-GRY03'
    - - :warning
      - 'Line 9548: Product not found, record ignored., BaseItemCode=LVTM7-GRY04'
    - - :warning
      - 'Line 9549: Product not found, record ignored., BaseItemCode=LVTM7-GRY06'
    - - :warning
      - 'Line 9550: Product not found, record ignored., BaseItemCode=LVTM7-GRY07'
    - - :warning
      - 'Line 9551: Product not found, record ignored., BaseItemCode=LVTM7-GRY20'
    - - :warning
      - 'Line 9552: Product not found, record ignored., BaseItemCode=LVTM7-OAK01'
    - - :warning
      - 'Line 9553: Product not found, record ignored., BaseItemCode=LVTM7-OAK02'
    - - :warning
      - 'Line 9554: Product not found, record ignored., BaseItemCode=LVTM7-OAK03'
    - - :warning
      - 'Line 9555: Product not found, record ignored., BaseItemCode=LVTM7-OAK04'
    - - :warning
      - 'Line 9556: Product not found, record ignored., BaseItemCode=LVTM7-OAK05'
    - - :warning
      - 'Line 9557: Product not found, record ignored., BaseItemCode=LVTM7-OAK20'
    - - :warning
      - 'Line 9558: Product not found, record ignored., BaseItemCode=LVTM7-OAK21'
 |
| 2026-06-16 15:01:38 | ---
- - Images
  - - - :information
      - 'The following images were imported: MRE83672_8.jpg, MRE82730_5.jpg, MRE83636_1.jpg,
        MRE83048_8.jpg, MRE83648_1.jpg, MRE82440_16.jpg, MRE81836_15.jpg, MRE84272_4.jpg,
        MRE82436_11.jpg, MRE81830.jpg, MRE83040_7.jpg, MRE81836_12.jpg, MRE83648_13.jpg,
        MRE82030_8.jpg, MRE82436_10.jpg, MRE81836_14.jpg, MRE82440_15.jpg, MRE83636_8.jpg,
        MRE84272_13.jpg, MRE82730.jpg, MRE81830_10.jpg, MRE82040_8.jpg, MRE83030.jpg,
        MRE82740_7.jpg, MRE82740_6.jpg, MRE83036_2.jpg, MRE82430_5.jpg, MRE82030_16.jpg,
        MRE83648_3.jpg, MRE82440_11.jpg and 43 more images'
 |
| 2026-06-16 14:52:29 | ---
- - Images
  - - - :information
      - 'The following images were imported: MRE83072_7.jpg, MRE82436_6.jpg, MRE81836_2.jpg,
        MRE84272_1.jpg, MRE84260_8.jpg, MRE82430_15.jpg, MRE82040.jpg, MRE81830_12.jpg,
        MRE83672_4.jpg, MRE83040_4.jpg, MRE82430_10.jpg, MRE83040_16.jpg, MRE82430_14.jpg,
        MRE83040_15.jpg, MRE83040_3.jpg, MRE82730_4.jpg, MRE84272_8.jpg, MRE82736.jpg,
        MRE84260_4.jpg, MRE83672_2.jpg, MRE83660_12.jpg, MRE82730_1.jpg, MRE82030_7.jpg,
        MRE82040_5.jpg, MRE83648_9.jpg, MRE82736_5.jpg, MRE83030_10.jpg, MRE83036_12.jpg,
        MRE81830_1.jpg, MRE82030_14.jpg and 227 more images'
 |
| 2026-06-16 14:27:54 | ---
- - Images
  - - - :information
      - 'The following images were imported: MRE83040_5.jpg, MRE84272_14.jpg, MRE82036_15.jpg,
        MRE82030.jpg, MRE83648_7.jpg, MRE82030_2.jpg, MRE83636_3.jpg, MRE82036_14.jpg,
        MRE83030_11.jpg, MRE82030_10.jpg, MRE82440_10.jpg, MRE82440.jpg, MRE84272_15.jpg,
        MRE83636_14.jpg, MRE83636_16.jpg, MRE83048.jpg, MRE83048_4.jpg, MRE83648_6.jpg,
        MRE83036_11.jpg, MRE83636_7.jpg, MRE82740_8.jpg, MRE82436_13.jpg, MRE82040_15.jpg,
        MRE83048_13.jpg, MRE83036_1.jpg, MRE84272_2.jpg, MRE83660_5.jpg, MRE82030_3.jpg,
        MRE83030_15.jpg, MRE83048_15.jpg and 30 more images'
 |
| 2026-06-16 14:24:22 | ---
- - Products
  - - - :warning
      - 'Line 10272: ImageFileName: 1012D42BK-01CR(0).JPG is not valid and will not
        be imported'
    - - :warning
      - 'Line 10272: ImageFileName: 1012D42BK-01CR_(1).JPG is not valid and will not
        be imported'
    - - :warning
      - 'Line 10273: ImageFileName: 1012D42C-01CR(0).JPG is not valid and will not
        be imported'
    - - :warning
      - 'Line 10273: ImageFileName: 1012D42C-01CR_(1).JPG is not valid and will not
        be imported'
    - - :warning
      - 'Line 10274: ImageFileName: 1012D42SG-01CR(0).JPG is not valid and will not
        be imported'
    - - :warning
      - 'Line 10274: ImageFileName: 1012D42SG-01CR_(1).JPG is not valid and will not
        be imported'
    - - :information
      - 'The following items were missing category codes and asssigned to ''Other''
        category: BS1324WH, BS1330WH, BS1332WH, BS1336WH, BS1342WH, BS1348WH'
 |
| 2026-06-16 14:17:53 | ---
- - Images
  - - - :information
      - 'The following images were imported: MRE8513K.jpg, MRE8525K.jpg, MRE8515K.jpg,
        MRE8535k.JPG, MRE8503K.jpg, MRE8523K.jpg, MRE8533k_1.JPG, MRE8505K.jpg, MRE8533K.JPG,
        MRE8535k_1.JPG'
 |
| 2026-06-16 14:13:32 | ---
- - Images
  - []
 |
| 2026-06-16 07:09:59 | ---
- - Inventory
  - - - :warning
      - 'Line 9: Product not found, record ignored., BaseItemCode=1101D28BR'
    - - :warning
      - 'Line 102: Product not found, record ignored., BaseItemCode=1107F18BR'
    - - :warning
      - 'Line 686: Product not found, record ignored., BaseItemCode=1451D20C'
    - - :warning
      - 'Line 687: Product not found, record ignored., BaseItemCode=1452D18PN'
    - - :warning
      - 'Line 694: Product not found, record ignored., BaseItemCode=1453D17DB'
    - - :warning
      - 'Line 695: Product not found, record ignored., BaseItemCode=1453W13PN'
    - - :warning
      - 'Line 696: Product not found, record ignored., BaseItemCode=1458D13BZ'
    - - :warning
      - 'Line 697: Product not found, record ignored., BaseItemCode=1458D13VN'
    - - :warning
      - 'Line 700: Product not found, record ignored., BaseItemCode=1461W13PN'
    - - :warning
      - 'Line 703: Product not found, record ignored., BaseItemCode=1471G44SL'
    - - :warning
      - 'Line 704: Product not found, record ignored., BaseItemCode=1472G39BB'
    - - :warning
      - 'Line 708: Product not found, record ignored., BaseItemCode=1473G52PN'
    - - :warning
      - 'Line 709: Product not found, record ignored., BaseItemCode=1485D15VN'
    - - :warning
      - 'Line 716: Product not found, record ignored., BaseItemCode=1503D18IW'
    - - :warning
      - 'Line 717: Product not found, record ignored., BaseItemCode=1504D35VN'
    - - :warning
      - 'Line 723: Product not found, record ignored., BaseItemCode=1512D9GI'
    - - :warning
      - 'Line 726: Product not found, record ignored., BaseItemCode=1537W5VB'
    - - :warning
      - 'Line 727: Product not found, record ignored., BaseItemCode=1702D18ASL'
    - - :warning
      - 'Line 731: Product not found, record ignored., BaseItemCode=1710D12FB'
    - - :warning
      - 'Line 817: Product not found, record ignored., BaseItemCode=2105W10C/RC'
    - - :warning
      - 'Line 826: Product not found, record ignored., BaseItemCode=2116D26C/RC'
    - - :warning
      - 'Line 827: Product not found, record ignored., BaseItemCode=2116D32C/RC'
    - - :warning
      - 'Line 828: Product not found, record ignored., BaseItemCode=2116G63C/RC'
    - - :warning
      - 'Line 831: Product not found, record ignored., BaseItemCode=2117W33C/RC'
    - - :warning
      - 'Line 1372: Product not found, record ignored., BaseItemCode=5100D5C'
    - - :warning
      - 'Line 1386: Product not found, record ignored., BaseItemCode=5200D32C'
    - - :warning
      - 'Line 1388: Product not found, record ignored., BaseItemCode=5200D36C'
    - - :warning
      - 'Line 1389: Product not found, record ignored., BaseItemCode=5200D42C'
    - - :warning
      - 'Line 1397: Product not found, record ignored., BaseItemCode=5201D5C'
    - - :warning
      - 'Line 1398: Product not found, record ignored., BaseItemCode=5202D22C'
    - - :warning
      - 'Line 1400: Product not found, record ignored., BaseItemCode=5202D24C'
    - - :warning
      - 'Line 1401: Product not found, record ignored., BaseItemCode=5202D24G'
    - - :warning
      - 'Line 1407: Product not found, record ignored., BaseItemCode=5203D16G'
    - - :warning
      - 'Line 1456: Product not found, record ignored., BaseItemCode=7872D17C'
    - - :warning
      - 'Line 1457: Product not found, record ignored., BaseItemCode=7872D17SS'
    - - :warning
      - 'Line 1589: Product not found, record ignored., BaseItemCode=BR20LED102-6PK'
    - - :warning
      - 'Line 1658: Product not found, record ignored., BaseItemCode=CF3004'
    - - :warning
      - 'Line 1812: Product not found, record ignored., BaseItemCode=KIT20204'
    - - :warning
      - 'Line 1813: Product not found, record ignored., BaseItemCode=KIT20402'
    - - :warning
      - 'Line 1814: Product not found, record ignored., BaseItemCode=KIT40606'
    - - :warning
      - 'Line 1815: Product not found, record ignored., BaseItemCode=KIT40804'
    - - :warning
      - 'Line 1882: Product not found, record ignored., BaseItemCode=LD2239C'
    - - :warning
      - 'Line 1919: Product not found, record ignored., BaseItemCode=LD2259BR'
    - - :warning
      - 'Line 1936: Product not found, record ignored., BaseItemCode=LD2274BK'
    - - :warning
      - 'Line 1938: Product not found, record ignored., BaseItemCode=LD2275BR'
    - - :warning
      - 'Line 1942: Product not found, record ignored., BaseItemCode=LD2277C'
    - - :warning
      - 'Line 1955: Product not found, record ignored., BaseItemCode=LD2300BR'
    - - :warning
      - 'Line 1958: Product not found, record ignored., BaseItemCode=LD2301BR'
    - - :warning
      - 'Line 1959: Product not found, record ignored., BaseItemCode=LD2301C'
    - - :warning
      - 'Line 1960: Product not found, record ignored., BaseItemCode=LD2302BK'
    - - :warning
      - 'Line 1961: Product not found, record ignored., BaseItemCode=LD2302BR'
    - - :warning
      - 'Line 1962: Product not found, record ignored., BaseItemCode=LD2302C'
    - - :warning
      - 'Line 1966: Product not found, record ignored., BaseItemCode=LD2304BK'
    - - :warning
      - 'Line 1969: Product not found, record ignored., BaseItemCode=LD2305BK'
    - - :warning
      - 'Line 1970: Product not found, record ignored., BaseItemCode=LD2305BR'
    - - :warning
      - 'Line 1971: Product not found, record ignored., BaseItemCode=LD2305C'
    - - :warning
      - 'Line 1972: Product not found, record ignored., BaseItemCode=LD2306BR'
    - - :warning
      - 'Line 1975: Product not found, record ignored., BaseItemCode=LD2307BR'
    - - :warning
      - 'Line 1979: Product not found, record ignored., BaseItemCode=LD2309C'
    - - :warning
      - 'Line 1980: Product not found, record ignored., BaseItemCode=LD2310BK'
    - - :warning
      - 'Line 1984: Product not found, record ignored., BaseItemCode=LD2311BR'
    - - :warning
      - 'Line 2037: Product not found, record ignored., BaseItemCode=LD2337BK'
    - - :warning
      - 'Line 2038: Product not found, record ignored., BaseItemCode=LD2337BR'
    - - :warning
      - 'Line 2039: Product not found, record ignored., BaseItemCode=LD2337C'
    - - :warning
      - 'Line 2040: Product not found, record ignored., BaseItemCode=LD2338BK'
    - - :warning
      - 'Line 2041: Product not found, record ignored., BaseItemCode=LD2338BR'
    - - :warning
      - 'Line 2042: Product not found, record ignored., BaseItemCode=LD2338C'
    - - :warning
      - 'Line 2043: Product not found, record ignored., BaseItemCode=LD2339BK'
    - - :warning
      - 'Line 2044: Product not found, record ignored., BaseItemCode=LD2339BR'
    - - :warning
      - 'Line 2045: Product not found, record ignored., BaseItemCode=LD2339C'
    - - :warning
      - 'Line 2046: Product not found, record ignored., BaseItemCode=LD2340BK'
    - - :warning
      - 'Line 2047: Product not found, record ignored., BaseItemCode=LD2340BR'
    - - :warning
      - 'Line 2048: Product not found, record ignored., BaseItemCode=LD2340C'
    - - :warning
      - 'Line 2049: Product not found, record ignored., BaseItemCode=LD2341BR'
    - - :warning
      - 'Line 2050: Product not found, record ignored., BaseItemCode=LD2344BK'
    - - :warning
      - 'Line 2051: Product not found, record ignored., BaseItemCode=LD2344BR'
    - - :warning
      - 'Line 2063: Product not found, record ignored., BaseItemCode=LD2350BK'
    - - :warning
      - 'Line 2064: Product not found, record ignored., BaseItemCode=LD2350BR'
    - - :warning
      - 'Line 2068: Product not found, record ignored., BaseItemCode=LD2352BK'
    - - :warning
      - 'Line 2069: Product not found, record ignored., BaseItemCode=LD2352BR'
    - - :warning
      - 'Line 2096: Product not found, record ignored., BaseItemCode=LD2363BK'
    - - :warning
      - 'Line 2097: Product not found, record ignored., BaseItemCode=LD2363BR'
    - - :warning
      - 'Line 2098: Product not found, record ignored., BaseItemCode=LD2364BK'
    - - :warning
      - 'Line 2099: Product not found, record ignored., BaseItemCode=LD2364BR'
    - - :warning
      - 'Line 2100: Product not found, record ignored., BaseItemCode=LD2364RED'
    - - :warning
      - 'Line 2101: Product not found, record ignored., BaseItemCode=LD2364WH'
    - - :warning
      - 'Line 2102: Product not found, record ignored., BaseItemCode=LD2365BK'
    - - :warning
      - 'Line 2103: Product not found, record ignored., BaseItemCode=LD2365BR'
    - - :warning
      - 'Line 2108: Product not found, record ignored., BaseItemCode=LD2367WH'
    - - :warning
      - 'Line 2110: Product not found, record ignored., BaseItemCode=LD2401WH'
    - - :warning
      - 'Line 2113: Product not found, record ignored., BaseItemCode=LD2404BN'
    - - :warning
      - 'Line 2115: Product not found, record ignored., BaseItemCode=LD2405HG'
    - - :warning
      - 'Line 2119: Product not found, record ignored., BaseItemCode=LD2407HG'
    - - :warning
      - 'Line 2126: Product not found, record ignored., BaseItemCode=LD2410WH'
    - - :warning
      - 'Line 2127: Product not found, record ignored., BaseItemCode=LD2411HG'
    - - :warning
      - 'Line 2128: Product not found, record ignored., BaseItemCode=LD2412WH'
    - - :warning
      - 'Line 2134: Product not found, record ignored., BaseItemCode=LD2450BK'
    - - :warning
      - 'Line 2135: Product not found, record ignored., BaseItemCode=LD2450BR'
    - - :warning
      - 'Line 2136: Product not found, record ignored., BaseItemCode=LD2450C'
    - - :warning
      - 'Line 2140: Product not found, record ignored., BaseItemCode=LD2453FLBK'
    - - :warning
      - 'Line 2141: Product not found, record ignored., BaseItemCode=LD2453FLBR'
    - - :warning
      - 'Line 2142: Product not found, record ignored., BaseItemCode=LD2453FLCG'
    - - :warning
      - 'Line 2158: Product not found, record ignored., BaseItemCode=LD4008D11BK'
    - - :warning
      - 'Line 2164: Product not found, record ignored., BaseItemCode=LD4017D48BRB'
    - - :warning
      - 'Line 2291: Product not found, record ignored., BaseItemCode=LD5016D17BK'
    - - :warning
      - 'Line 2302: Product not found, record ignored., BaseItemCode=LD5023'
    - - :warning
      - 'Line 2370: Product not found, record ignored., BaseItemCode=LD520D10BK'
    - - :warning
      - 'Line 2371: Product not found, record ignored., BaseItemCode=LD520D10BR'
    - - :warning
      - 'Line 2372: Product not found, record ignored., BaseItemCode=LD520D10C'
    - - :warning
      - 'Line 2373: Product not found, record ignored., BaseItemCode=LD520D13BK'
    - - :warning
      - 'Line 2374: Product not found, record ignored., BaseItemCode=LD520D13BR'
    - - :warning
      - 'Line 2375: Product not found, record ignored., BaseItemCode=LD520D13C'
    - - :warning
      - 'Line 2376: Product not found, record ignored., BaseItemCode=LD520D16BK'
    - - :warning
      - 'Line 2377: Product not found, record ignored., BaseItemCode=LD520D16BR'
    - - :warning
      - 'Line 2378: Product not found, record ignored., BaseItemCode=LD520D16C'
    - - :warning
      - 'Line 2379: Product not found, record ignored., BaseItemCode=LD520D18BK'
    - - :warning
      - 'Line 2380: Product not found, record ignored., BaseItemCode=LD520D18BR'
    - - :warning
      - 'Line 2381: Product not found, record ignored., BaseItemCode=LD520D18C'
    - - :warning
      - 'Line 2382: Product not found, record ignored., BaseItemCode=LD520D20BR'
    - - :warning
      - 'Line 2391: Product not found, record ignored., BaseItemCode=LD6005D12BR'
    - - :warning
      - 'Line 2408: Product not found, record ignored., BaseItemCode=LD6010D26BN'
    - - :warning
      - 'Line 2414: Product not found, record ignored., BaseItemCode=LD6012D15G'
    - - :warning
      - 'Line 2425: Product not found, record ignored., BaseItemCode=LD6016'
    - - :warning
      - 'Line 2471: Product not found, record ignored., BaseItemCode=LD6077C'
    - - :warning
      - 'Line 2481: Product not found, record ignored., BaseItemCode=LD6100C'
    - - :warning
      - 'Line 2495: Product not found, record ignored., BaseItemCode=LD6109BR'
    - - :warning
      - 'Line 2502: Product not found, record ignored., BaseItemCode=LD6124C'
    - - :warning
      - 'Line 2509: Product not found, record ignored., BaseItemCode=LD6133BR'
    - - :warning
      - 'Line 2537: Product not found, record ignored., BaseItemCode=LD6170C'
    - - :warning
      - 'Line 2540: Product not found, record ignored., BaseItemCode=LD6173BR'
    - - :warning
      - 'Line 2543: Product not found, record ignored., BaseItemCode=LD6176C'
    - - :warning
      - 'Line 2544: Product not found, record ignored., BaseItemCode=LD6178BR'
    - - :warning
      - 'Line 2558: Product not found, record ignored., BaseItemCode=LD6205C'
    - - :warning
      - 'Line 2568: Product not found, record ignored., BaseItemCode=LD6220C'
    - - :warning
      - 'Line 2574: Product not found, record ignored., BaseItemCode=LD6232C'
    - - :warning
      - 'Line 2575: Product not found, record ignored., BaseItemCode=LD6238C'
    - - :warning
      - 'Line 2581: Product not found, record ignored., BaseItemCode=LD6248BR'
    - - :warning
      - 'Line 2587: Product not found, record ignored., BaseItemCode=LD6259C'
    - - :warning
      - 'Line 2603: Product not found, record ignored., BaseItemCode=LD642D36BR'
    - - :warning
      - 'Line 2604: Product not found, record ignored., BaseItemCode=LD642D36BRK'
    - - :warning
      - 'Line 2605: Product not found, record ignored., BaseItemCode=LD643D36BK'
    - - :warning
      - 'Line 2620: Product not found, record ignored., BaseItemCode=LD648F26BK'
    - - :warning
      - 'Line 2622: Product not found, record ignored., BaseItemCode=LD648F26BRK'
    - - :warning
      - 'Line 2633: Product not found, record ignored., BaseItemCode=LD652D30BR'
    - - :warning
      - 'Line 2642: Product not found, record ignored., BaseItemCode=LD655D18BR'
    - - :warning
      - 'Line 2643: Product not found, record ignored., BaseItemCode=LD655D18BRK'
    - - :warning
      - 'Line 2650: Product not found, record ignored., BaseItemCode=LD6802D14C'
    - - :warning
      - 'Line 2683: Product not found, record ignored., BaseItemCode=LD7024D25BK'
    - - :warning
      - 'Line 2685: Product not found, record ignored., BaseItemCode=LD7024D25SN'
    - - :warning
      - 'Line 2752: Product not found, record ignored., BaseItemCode=LD7044D26WD'
    - - :warning
      - 'Line 2760: Product not found, record ignored., BaseItemCode=LD7047D28BR'
    - - :warning
      - 'Line 2779: Product not found, record ignored., BaseItemCode=LD7057D20BK'
    - - :warning
      - 'Line 2809: Product not found, record ignored., BaseItemCode=LD7071D14BK'
    - - :warning
      - 'Line 2879: Product not found, record ignored., BaseItemCode=LD7301W15CH'
    - - :warning
      - 'Line 2892: Product not found, record ignored., BaseItemCode=LD7302W24BLK'
    - - :warning
      - 'Line 2900: Product not found, record ignored., BaseItemCode=LD7302W6CH'
    - - :warning
      - 'Line 2917: Product not found, record ignored., BaseItemCode=LD7304W22BRA'
    - - :warning
      - 'Line 2922: Product not found, record ignored., BaseItemCode=LD7304W7BLK'
    - - :warning
      - 'Line 2942: Product not found, record ignored., BaseItemCode=LD7307W24CH'
    - - :warning
      - 'Line 2976: Product not found, record ignored., BaseItemCode=LD7310W23BLK'
    - - :warning
      - 'Line 3147: Product not found, record ignored., BaseItemCode=LD7327W6BLK'
    - - :warning
      - 'Line 3159: Product not found, record ignored., BaseItemCode=LD7331W7BLK'
    - - :warning
      - 'Line 3218: Product not found, record ignored., BaseItemCode=LD8049D10BR'
    - - :warning
      - 'Line 3240: Product not found, record ignored., BaseItemCode=LD810F19SL'
    - - :warning
      - 'Line 3293: Product not found, record ignored., BaseItemCode=LD8801D43GB'
    - - :warning
      - 'Line 3323: Product not found, record ignored., BaseItemCode=LDOD3004-6PK'
    - - :warning
      - 'Line 3324: Product not found, record ignored., BaseItemCode=LDOD3006-4PK'
    - - :warning
      - 'Line 3339: Product not found, record ignored., BaseItemCode=LDOD4010BK'
    - - :warning
      - 'Line 3341: Product not found, record ignored., BaseItemCode=LDOD4011BK'
    - - :warning
      - 'Line 3343: Product not found, record ignored., BaseItemCode=LDOD4011WH'
    - - :warning
      - 'Line 3347: Product not found, record ignored., BaseItemCode=LDOD4013WH'
    - - :warning
      - 'Line 3354: Product not found, record ignored., BaseItemCode=LDOD4016BK'
    - - :warning
      - 'Line 3356: Product not found, record ignored., BaseItemCode=LDOD4016WH'
    - - :warning
      - 'Line 3395: Product not found, record ignored., BaseItemCode=LDPD2000BN'
    - - :warning
      - 'Line 3403: Product not found, record ignored., BaseItemCode=LDPD2003BN'
    - - :warning
      - 'Line 3409: Product not found, record ignored., BaseItemCode=LDPD2017'
    - - :warning
      - 'Line 3424: Product not found, record ignored., BaseItemCode=LDPD2045HG'
    - - :warning
      - 'Line 3427: Product not found, record ignored., BaseItemCode=LDPD2046WH'
    - - :warning
      - 'Line 3474: Product not found, record ignored., BaseItemCode=LDPG2256BK'
    - - :warning
      - 'Line 3475: Product not found, record ignored., BaseItemCode=LDPG2256BR'
    - - :warning
      - 'Line 3483: Product not found, record ignored., BaseItemCode=LDPG6037BR'
    - - :warning
      - 'Line 3499: Product not found, record ignored., BaseItemCode=MF53047BL'
    - - :warning
      - 'Line 3509: Product not found, record ignored., BaseItemCode=MF6-1008S'
    - - :warning
      - 'Line 3517: Product not found, record ignored., BaseItemCode=MF6-1036AW'
    - - :warning
      - 'Line 3518: Product not found, record ignored., BaseItemCode=MF6-1036BL'
    - - :warning
      - 'Line 3523: Product not found, record ignored., BaseItemCode=MF61060AW'
    - - :warning
      - 'Line 3524: Product not found, record ignored., BaseItemCode=MF61060AW-F1'
    - - :warning
      - 'Line 3525: Product not found, record ignored., BaseItemCode=MF61072BL'
    - - :warning
      - 'Line 3585: Product not found, record ignored., BaseItemCode=MF72038BK'
    - - :warning
      - 'Line 3597: Product not found, record ignored., BaseItemCode=MF73016BK'
    - - :warning
      - 'Line 3616: Product not found, record ignored., BaseItemCode=MF82002WH'
    - - :warning
      - 'Line 3623: Invalid next scheduled receipt date'
    - - :warning
      - 'Line 3842: Product not found, record ignored., BaseItemCode=MR33248BL'
    - - :warning
      - 'Line 3843: Product not found, record ignored., BaseItemCode=MR33272BL'
    - - :warning
      - 'Line 3865: Product not found, record ignored., BaseItemCode=MR4044WH'
    - - :warning
      - 'Line 3875: Product not found, record ignored., BaseItemCode=MR4054GR'
    - - :warning
      - 'Line 3894: Product not found, record ignored., BaseItemCode=MR4071BL'
    - - :warning
      - 'Line 3916: Product not found, record ignored., BaseItemCode=MR41828BL'
    - - :warning
      - 'Line 3924: Product not found, record ignored., BaseItemCode=MR42036BL'
    - - :warning
      - 'Line 3937: Product not found, record ignored., BaseItemCode=MR42736BL'
    - - :warning
      - 'Line 3994: Product not found, record ignored., BaseItemCode=MR4718BL'
    - - :warning
      - 'Line 3998: Product not found, record ignored., BaseItemCode=MR4721BL'
    - - :warning
      - 'Line 4000: Product not found, record ignored., BaseItemCode=MR4721GR'
    - - :warning
      - 'Line 4035: Product not found, record ignored., BaseItemCode=MR52736'
    - - :warning
      - 'Line 4036: Product not found, record ignored., BaseItemCode=MR53648'
    - - :warning
      - 'Line 4037: Product not found, record ignored., BaseItemCode=MR53660'
    - - :warning
      - 'Line 4058: Product not found, record ignored., BaseItemCode=MR652828BK'
    - - :warning
      - 'Line 4147: Product not found, record ignored., BaseItemCode=MR913240'
    - - :warning
      - 'Line 4155: Invalid next scheduled receipt date'
    - - :warning
      - 'Line 4156: Product not found, record ignored., BaseItemCode=MR9239'
    - - :warning
      - 'Line 4190: Product not found, record ignored., BaseItemCode=MRE32432BK'
    - - :warning
      - 'Line 4193: Product not found, record ignored., BaseItemCode=MRE32471BK'
    - - :warning
      - 'Line 4209: Product not found, record ignored., BaseItemCode=MRE52036'
    - - :warning
      - 'Line 4210: Product not found, record ignored., BaseItemCode=MRE52040'
    - - :warning
      - 'Line 4211: Product not found, record ignored., BaseItemCode=MRE52436'
    - - :warning
      - 'Line 4212: Product not found, record ignored., BaseItemCode=MRE52440'
    - - :warning
      - 'Line 4213: Product not found, record ignored., BaseItemCode=MRE52730'
    - - :warning
      - 'Line 4214: Product not found, record ignored., BaseItemCode=MRE52736'
    - - :warning
      - 'Line 4215: Product not found, record ignored., BaseItemCode=MRE52740'
    - - :warning
      - 'Line 4216: Product not found, record ignored., BaseItemCode=MRE53030'
    - - :warning
      - 'Line 4217: Product not found, record ignored., BaseItemCode=MRE53072'
    - - :warning
      - 'Line 4218: Product not found, record ignored., BaseItemCode=MRE53648'
    - - :warning
      - 'Line 4219: Product not found, record ignored., BaseItemCode=MRE54260'
    - - :warning
      - 'Line 4302: Product not found, record ignored., BaseItemCode=MRE92030'
    - - :warning
      - 'Line 4303: Product not found, record ignored., BaseItemCode=MRE92436'
    - - :warning
      - 'Line 4306: Product not found, record ignored., BaseItemCode=MRE93248'
    - - :warning
      - 'Line 4307: Product not found, record ignored., BaseItemCode=MRE93272'
    - - :warning
      - 'Line 4414: Product not found, record ignored., BaseItemCode=RN61550RF-4PK'
    - - :warning
      - 'Line 4415: Product not found, record ignored., BaseItemCode=RS41050SDK-4PK'
    - - :warning
      - 'Line 4484: Product not found, record ignored., BaseItemCode=TC5R-E26-6PK'
    - - :warning
      - 'Line 4485: Product not found, record ignored., BaseItemCode=TC6R-E26-6PK'
    - - :warning
      - 'Line 4505: Product not found, record ignored., BaseItemCode=TKACP-MW'
    - - :warning
      - 'Line 4506: Product not found, record ignored., BaseItemCode=TKAEF-MW'
    - - :warning
      - 'Line 4507: Product not found, record ignored., BaseItemCode=TKAFCF-BK'
    - - :warning
      - 'Line 4508: Product not found, record ignored., BaseItemCode=TKALC-BK'
    - - :warning
      - 'Line 4509: Product not found, record ignored., BaseItemCode=TKATC-BK'
    - - :warning
      - 'Line 4510: Product not found, record ignored., BaseItemCode=TKATC-MW'
    - - :warning
      - 'Line 4511: Product not found, record ignored., BaseItemCode=TKH210BK-6PK'
    - - :warning
      - 'Line 4512: Product not found, record ignored., BaseItemCode=TKL4BK'
    - - :warning
      - 'Line 4513: Product not found, record ignored., BaseItemCode=TKL4MW'
    - - :warning
      - 'Line 4525: Product not found, record ignored., BaseItemCode=V1800D24BK/RC'
    - - :warning
      - 'Line 4603: Product not found, record ignored., BaseItemCode=V1803W12SG/RC'
    - - :warning
      - 'Line 4638: Product not found, record ignored., BaseItemCode=V2006F14C/RC'
    - - :warning
      - 'Line 4640: Product not found, record ignored., BaseItemCode=V2006F16C/RC'
    - - :warning
      - 'Line 4648: Product not found, record ignored., BaseItemCode=V2011D21G/RC'
    - - :warning
      - 'Line 4705: Product not found, record ignored., BaseItemCode=V2032D24C/RC'
    - - :warning
      - 'Line 4711: Product not found, record ignored., BaseItemCode=V2032F14C/RC'
    - - :warning
      - 'Line 4718: Product not found, record ignored., BaseItemCode=V2032W30BK/RC'
    - - :warning
      - 'Line 4719: Product not found, record ignored., BaseItemCode=V2032W36BK/RC'
    - - :warning
      - 'Line 4724: Product not found, record ignored., BaseItemCode=V2033D24C/RC'
    - - :warning
      - 'Line 4726: Product not found, record ignored., BaseItemCode=V2033F14C/RC'
    - - :warning
      - 'Line 4733: Product not found, record ignored., BaseItemCode=V2034D28C/RC'
    - - :warning
      - 'Line 4736: Product not found, record ignored., BaseItemCode=V2035D28C/RC'
    - - :warning
      - 'Line 4737: Product not found, record ignored., BaseItemCode=V2075D18C/RC'
    - - :warning
      - 'Line 4748: Product not found, record ignored., BaseItemCode=V2100D35C/RC'
    - - :warning
      - 'Line 4796: Product not found, record ignored., BaseItemCode=V3100D40C/RC'
    - - :warning
      - 'Line 4798: Product not found, record ignored., BaseItemCode=V6801D14C/RC'
    - - :warning
      - 'Line 4799: Product not found, record ignored., BaseItemCode=V6801D19G/RC'
    - - :warning
      - 'Line 4801: Product not found, record ignored., BaseItemCode=V7803D11B-JT/RC'
    - - :warning
      - 'Line 4805: Product not found, record ignored., BaseItemCode=V7804D15GS-GS/RC'
    - - :warning
      - 'Line 4807: Product not found, record ignored., BaseItemCode=V7804D15PE/RC'
    - - :warning
      - 'Line 4808: Product not found, record ignored., BaseItemCode=V7804D15PK-RO/RC'
    - - :warning
      - 'Line 4882: Product not found, record ignored., BaseItemCode=V9800D20G/RC'
    - - :warning
      - 'Line 4883: Product not found, record ignored., BaseItemCode=V9800D24C/RC'
    - - :warning
      - 'Line 4884: Product not found, record ignored., BaseItemCode=V9800D24G/RC'
    - - :warning
      - 'Line 4885: Product not found, record ignored., BaseItemCode=V9800D28C/RC'
    - - :warning
      - 'Line 4894: Product not found, record ignored., BaseItemCode=V9805F10BK/RC'
    - - :warning
      - 'Line 4895: Product not found, record ignored., BaseItemCode=V9805F10C/RC'
    - - :warning
      - 'Line 4896: Product not found, record ignored., BaseItemCode=V9805F10G/RC'
    - - :warning
      - 'Line 4969: Product not found, record ignored., BaseItemCode=VF-1030VM'
    - - :warning
      - 'Line 4999: Product not found, record ignored., BaseItemCode=VF12319GR'
    - - :warning
      - 'Line 5030: Product not found, record ignored., BaseItemCode=VF12360DGR-VW'
    - - :warning
      - 'Line 5148: Product not found, record ignored., BaseItemCode=VF13060DAB-VW'
    - - :warning
      - 'Line 5153: Product not found, record ignored., BaseItemCode=VF13060DVM-VW'
    - - :warning
      - 'Line 5192: Product not found, record ignored., BaseItemCode=VF15032GN'
    - - :warning
      - 'Line 5328: Product not found, record ignored., BaseItemCode=VF17018WH'
    - - :warning
      - 'Line 5581: Product not found, record ignored., BaseItemCode=VF27048GN'
    - - :warning
      - 'Line 5769: Product not found, record ignored., BaseItemCode=VF41048MGN'
    - - :warning
      - 'Line 5799: Product not found, record ignored., BaseItemCode=VF42524MGN'
    - - :warning
      - 'Line 5800: Product not found, record ignored., BaseItemCode=VF42524MMP'
    - - :warning
      - 'Line 5872: Product not found, record ignored., BaseItemCode=VF43030CG'
    - - :warning
      - 'Line 5879: Product not found, record ignored., BaseItemCode=VF43040WB'
    - - :warning
      - 'Line 5889: Product not found, record ignored., BaseItemCode=VF43524MWH'
    - - :warning
      - 'Line 5898: Product not found, record ignored., BaseItemCode=VF43530MMP'
    - - :warning
      - 'Line 5899: Product not found, record ignored., BaseItemCode=VF43530MMP-BS'
    - - :warning
      - 'Line 5900: Product not found, record ignored., BaseItemCode=VF43530MTK'
    - - :warning
      - 'Line 5901: Product not found, record ignored., BaseItemCode=VF43530MTK-BS'
    - - :warning
      - 'Line 5920: Product not found, record ignored., BaseItemCode=VF43536MWT'
    - - :warning
      - 'Line 5921: Product not found, record ignored., BaseItemCode=VF43536MWT-BS'
    - - :warning
      - 'Line 5973: Product not found, record ignored., BaseItemCode=VF44524MMP'
    - - :warning
      - 'Line 5975: Product not found, record ignored., BaseItemCode=VF44524MTK'
    - - :warning
      - 'Line 5983: Product not found, record ignored., BaseItemCode=VF44530MWT'
    - - :warning
      - 'Line 5995: Product not found, record ignored., BaseItemCode=VF44536MWH'
    - - :warning
      - 'Line 6016: Product not found, record ignored., BaseItemCode=VF44548MMP'
    - - :warning
      - 'Line 6019: Product not found, record ignored., BaseItemCode=VF44548MWH'
    - - :warning
      - 'Line 6029: Product not found, record ignored., BaseItemCode=VF46030MBL'
    - - :warning
      - 'Line 6036: Product not found, record ignored., BaseItemCode=VF46036MBL'
    - - :warning
      - 'Line 6049: Product not found, record ignored., BaseItemCode=VF46048MBL'
    - - :warning
      - 'Line 6050: Product not found, record ignored., BaseItemCode=VF46048MMP'
    - - :warning
      - 'Line 6090: Product not found, record ignored., BaseItemCode=VF47042MBL'
    - - :warning
      - 'Line 6093: Product not found, record ignored., BaseItemCode=VF47042MMP'
    - - :warning
      - 'Line 6094: Product not found, record ignored., BaseItemCode=VF47042MMP-BS'
    - - :warning
      - 'Line 6115: Product not found, record ignored., BaseItemCode=VF48018MBL'
    - - :warning
      - 'Line 6117: Product not found, record ignored., BaseItemCode=VF48018MWH'
    - - :warning
      - 'Line 6118: Product not found, record ignored., BaseItemCode=VF48018MWT'
    - - :warning
      - 'Line 6119: Product not found, record ignored., BaseItemCode=VF48018NT'
    - - :warning
      - 'Line 6160: Product not found, record ignored., BaseItemCode=VF48060DMTK'
    - - :warning
      - 'Line 6167: Product not found, record ignored., BaseItemCode=VF48818MW'
    - - :warning
      - 'Line 6168: Product not found, record ignored., BaseItemCode=VF48818MWH'
    - - :warning
      - 'Line 6170: Product not found, record ignored., BaseItemCode=VF48818NT'
    - - :warning
      - 'Line 6196: Product not found, record ignored., BaseItemCode=VF48832MBL'
    - - :warning
      - 'Line 6197: Product not found, record ignored., BaseItemCode=VF48832MBL-BS'
    - - :warning
      - 'Line 6244: Product not found, record ignored., BaseItemCode=VF48848MBL'
    - - :warning
      - 'Line 6249: Product not found, record ignored., BaseItemCode=VF48848MWH'
    - - :warning
      - 'Line 6250: Product not found, record ignored., BaseItemCode=VF48848MWT'
    - - :warning
      - 'Line 6251: Product not found, record ignored., BaseItemCode=VF48848NT'
    - - :warning
      - 'Line 6305: Product not found, record ignored., BaseItemCode=VF50060DGN'
    - - :warning
      - 'Line 6328: Product not found, record ignored., BaseItemCode=VF53042GN'
    - - :warning
      - 'Line 6336: Product not found, record ignored., BaseItemCode=VF53060DBL'
    - - :warning
      - 'Line 6506: Product not found, record ignored., BaseItemCode=VF90242MGN'
    - - :warning
      - 'Line 6507: Product not found, record ignored., BaseItemCode=VF90242MGN-BS'
    - - :warning
      - 'Line 6516: Product not found, record ignored., BaseItemCode=VF90248MGN'
    - - :warning
      - 'Line 6517: Product not found, record ignored., BaseItemCode=VF90248MGN-BS'
    - - :warning
      - 'Line 6528: Product not found, record ignored., BaseItemCode=VM13236AB'
    - - :warning
      - 'Line 7012: Product not found, record ignored., BaseItemCode=MR6C2132BLK'
    - - :warning
      - 'Line 7478: Product not found, record ignored., BaseItemCode=W122-DB'
    - - :warning
      - 'Line 9461: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY01'
    - - :warning
      - 'Line 9462: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY02'
    - - :warning
      - 'Line 9463: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY03'
    - - :warning
      - 'Line 9464: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY04'
    - - :warning
      - 'Line 9465: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY06'
    - - :warning
      - 'Line 9466: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY07'
    - - :warning
      - 'Line 9467: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY20'
    - - :warning
      - 'Line 9468: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK01'
    - - :warning
      - 'Line 9469: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK02'
    - - :warning
      - 'Line 9470: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK03'
    - - :warning
      - 'Line 9471: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK04'
    - - :warning
      - 'Line 9472: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK05'
    - - :warning
      - 'Line 9473: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK20'
    - - :warning
      - 'Line 9474: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK21'
    - - :warning
      - 'Line 9475: Product not found, record ignored., BaseItemCode=LVFSN7-GRY01'
    - - :warning
      - 'Line 9476: Product not found, record ignored., BaseItemCode=LVFSN7-GRY02'
    - - :warning
      - 'Line 9477: Product not found, record ignored., BaseItemCode=LVFSN7-GRY03'
    - - :warning
      - 'Line 9478: Product not found, record ignored., BaseItemCode=LVFSN7-GRY04'
    - - :warning
      - 'Line 9479: Product not found, record ignored., BaseItemCode=LVFSN7-GRY06'
    - - :warning
      - 'Line 9480: Product not found, record ignored., BaseItemCode=LVFSN7-GRY07'
    - - :warning
      - 'Line 9481: Product not found, record ignored., BaseItemCode=LVFSN7-GRY20'
    - - :warning
      - 'Line 9482: Product not found, record ignored., BaseItemCode=LVFSN7-OAK01'
    - - :warning
      - 'Line 9483: Product not found, record ignored., BaseItemCode=LVFSN7-OAK02'
    - - :warning
      - 'Line 9484: Product not found, record ignored., BaseItemCode=LVFSN7-OAK03'
    - - :warning
      - 'Line 9485: Product not found, record ignored., BaseItemCode=LVFSN7-OAK04'
    - - :warning
      - 'Line 9486: Product not found, record ignored., BaseItemCode=LVFSN7-OAK05'
    - - :warning
      - 'Line 9487: Product not found, record ignored., BaseItemCode=LVFSN7-OAK20'
    - - :warning
      - 'Line 9488: Product not found, record ignored., BaseItemCode=LVFSN7-OAK21'
    - - :warning
      - 'Line 9489: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY01'
    - - :warning
      - 'Line 9490: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY02'
    - - :warning
      - 'Line 9491: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY03'
    - - :warning
      - 'Line 9492: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY04'
    - - :warning
      - 'Line 9493: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY06'
    - - :warning
      - 'Line 9494: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY07'
    - - :warning
      - 'Line 9495: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY20'
    - - :warning
      - 'Line 9496: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK01'
    - - :warning
      - 'Line 9497: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK02'
    - - :warning
      - 'Line 9498: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK03'
    - - :warning
      - 'Line 9499: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK04'
    - - :warning
      - 'Line 9500: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK05'
    - - :warning
      - 'Line 9501: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK20'
    - - :warning
      - 'Line 9502: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK21'
    - - :warning
      - 'Line 9503: Product not found, record ignored., BaseItemCode=LVRDM7-GRY01'
    - - :warning
      - 'Line 9504: Product not found, record ignored., BaseItemCode=LVRDM7-GRY02'
    - - :warning
      - 'Line 9505: Product not found, record ignored., BaseItemCode=LVRDM7-GRY03'
    - - :warning
      - 'Line 9506: Product not found, record ignored., BaseItemCode=LVRDM7-GRY04'
    - - :warning
      - 'Line 9507: Product not found, record ignored., BaseItemCode=LVRDM7-GRY06'
    - - :warning
      - 'Line 9508: Product not found, record ignored., BaseItemCode=LVRDM7-GRY07'
    - - :warning
      - 'Line 9509: Product not found, record ignored., BaseItemCode=LVRDM7-GRY20'
    - - :warning
      - 'Line 9510: Product not found, record ignored., BaseItemCode=LVRDM7-OAK01'
    - - :warning
      - 'Line 9511: Product not found, record ignored., BaseItemCode=LVRDM7-OAK02'
    - - :warning
      - 'Line 9512: Product not found, record ignored., BaseItemCode=LVRDM7-OAK03'
    - - :warning
      - 'Line 9513: Product not found, record ignored., BaseItemCode=LVRDM7-OAK04'
    - - :warning
      - 'Line 9514: Product not found, record ignored., BaseItemCode=LVRDM7-OAK05'
    - - :warning
      - 'Line 9515: Product not found, record ignored., BaseItemCode=LVRDM7-OAK20'
    - - :warning
      - 'Line 9516: Product not found, record ignored., BaseItemCode=LVRDM7-OAK21'
    - - :warning
      - 'Line 9517: Product not found, record ignored., BaseItemCode=LVST-GRY01'
    - - :warning
      - 'Line 9518: Product not found, record ignored., BaseItemCode=LVST-GRY02'
    - - :warning
      - 'Line 9519: Product not found, record ignored., BaseItemCode=LVST-GRY03'
    - - :warning
      - 'Line 9520: Product not found, record ignored., BaseItemCode=LVST-GRY04'
    - - :warning
      - 'Line 9521: Product not found, record ignored., BaseItemCode=LVST-GRY06'
    - - :warning
      - 'Line 9522: Product not found, record ignored., BaseItemCode=LVST-GRY07'
    - - :warning
      - 'Line 9523: Product not found, record ignored., BaseItemCode=LVST-GRY20'
    - - :warning
      - 'Line 9524: Product not found, record ignored., BaseItemCode=LVST-OAK01'
    - - :warning
      - 'Line 9525: Product not found, record ignored., BaseItemCode=LVST-OAK02'
    - - :warning
      - 'Line 9526: Product not found, record ignored., BaseItemCode=LVST-OAK03'
    - - :warning
      - 'Line 9527: Product not found, record ignored., BaseItemCode=LVST-OAK04'
    - - :warning
      - 'Line 9528: Product not found, record ignored., BaseItemCode=LVST-OAK05'
    - - :warning
      - 'Line 9529: Product not found, record ignored., BaseItemCode=LVST-OAK20'
    - - :warning
      - 'Line 9530: Product not found, record ignored., BaseItemCode=LVST-OAK21'
    - - :warning
      - 'Line 9531: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY01'
    - - :warning
      - 'Line 9532: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY02'
    - - :warning
      - 'Line 9533: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY03'
    - - :warning
      - 'Line 9534: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY04'
    - - :warning
      - 'Line 9535: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY06'
    - - :warning
      - 'Line 9536: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY07'
    - - :warning
      - 'Line 9537: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY20'
    - - :warning
      - 'Line 9538: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK01'
    - - :warning
      - 'Line 9539: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK02'
    - - :warning
      - 'Line 9540: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK03'
    - - :warning
      - 'Line 9541: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK04'
    - - :warning
      - 'Line 9542: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK05'
    - - :warning
      - 'Line 9543: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK20'
    - - :warning
      - 'Line 9544: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK21'
    - - :warning
      - 'Line 9545: Product not found, record ignored., BaseItemCode=LVTM7-GRY01'
    - - :warning
      - 'Line 9546: Product not found, record ignored., BaseItemCode=LVTM7-GRY02'
    - - :warning
      - 'Line 9547: Product not found, record ignored., BaseItemCode=LVTM7-GRY03'
    - - :warning
      - 'Line 9548: Product not found, record ignored., BaseItemCode=LVTM7-GRY04'
    - - :warning
      - 'Line 9549: Product not found, record ignored., BaseItemCode=LVTM7-GRY06'
    - - :warning
      - 'Line 9550: Product not found, record ignored., BaseItemCode=LVTM7-GRY07'
    - - :warning
      - 'Line 9551: Product not found, record ignored., BaseItemCode=LVTM7-GRY20'
    - - :warning
      - 'Line 9552: Product not found, record ignored., BaseItemCode=LVTM7-OAK01'
    - - :warning
      - 'Line 9553: Product not found, record ignored., BaseItemCode=LVTM7-OAK02'
    - - :warning
      - 'Line 9554: Product not found, record ignored., BaseItemCode=LVTM7-OAK03'
    - - :warning
      - 'Line 9555: Product not found, record ignored., BaseItemCode=LVTM7-OAK04'
    - - :warning
      - 'Line 9556: Product not found, record ignored., BaseItemCode=LVTM7-OAK05'
    - - :warning
      - 'Line 9557: Product not found, record ignored., BaseItemCode=LVTM7-OAK20'
    - - :warning
      - 'Line 9558: Product not found, record ignored., BaseItemCode=LVTM7-OAK21'
 |
| 2026-06-15 20:18:48 | ---
- - Inventory
  - - - :warning
      - 'Line 9: Product not found, record ignored., BaseItemCode=1101D28BR'
    - - :warning
      - 'Line 102: Product not found, record ignored., BaseItemCode=1107F18BR'
    - - :warning
      - 'Line 686: Product not found, record ignored., BaseItemCode=1451D20C'
    - - :warning
      - 'Line 687: Product not found, record ignored., BaseItemCode=1452D18PN'
    - - :warning
      - 'Line 694: Product not found, record ignored., BaseItemCode=1453D17DB'
    - - :warning
      - 'Line 695: Product not found, record ignored., BaseItemCode=1453W13PN'
    - - :warning
      - 'Line 696: Product not found, record ignored., BaseItemCode=1458D13BZ'
    - - :warning
      - 'Line 697: Product not found, record ignored., BaseItemCode=1458D13VN'
    - - :warning
      - 'Line 700: Product not found, record ignored., BaseItemCode=1461W13PN'
    - - :warning
      - 'Line 703: Product not found, record ignored., BaseItemCode=1471G44SL'
    - - :warning
      - 'Line 704: Product not found, record ignored., BaseItemCode=1472G39BB'
    - - :warning
      - 'Line 708: Product not found, record ignored., BaseItemCode=1473G52PN'
    - - :warning
      - 'Line 709: Product not found, record ignored., BaseItemCode=1485D15VN'
    - - :warning
      - 'Line 716: Product not found, record ignored., BaseItemCode=1503D18IW'
    - - :warning
      - 'Line 717: Product not found, record ignored., BaseItemCode=1504D35VN'
    - - :warning
      - 'Line 723: Product not found, record ignored., BaseItemCode=1512D9GI'
    - - :warning
      - 'Line 726: Product not found, record ignored., BaseItemCode=1537W5VB'
    - - :warning
      - 'Line 727: Product not found, record ignored., BaseItemCode=1702D18ASL'
    - - :warning
      - 'Line 731: Product not found, record ignored., BaseItemCode=1710D12FB'
    - - :warning
      - 'Line 817: Product not found, record ignored., BaseItemCode=2105W10C/RC'
    - - :warning
      - 'Line 826: Product not found, record ignored., BaseItemCode=2116D26C/RC'
    - - :warning
      - 'Line 827: Product not found, record ignored., BaseItemCode=2116D32C/RC'
    - - :warning
      - 'Line 828: Product not found, record ignored., BaseItemCode=2116G63C/RC'
    - - :warning
      - 'Line 831: Product not found, record ignored., BaseItemCode=2117W33C/RC'
    - - :warning
      - 'Line 1372: Product not found, record ignored., BaseItemCode=5100D5C'
    - - :warning
      - 'Line 1386: Product not found, record ignored., BaseItemCode=5200D32C'
    - - :warning
      - 'Line 1388: Product not found, record ignored., BaseItemCode=5200D36C'
    - - :warning
      - 'Line 1389: Product not found, record ignored., BaseItemCode=5200D42C'
    - - :warning
      - 'Line 1397: Product not found, record ignored., BaseItemCode=5201D5C'
    - - :warning
      - 'Line 1398: Product not found, record ignored., BaseItemCode=5202D22C'
    - - :warning
      - 'Line 1400: Product not found, record ignored., BaseItemCode=5202D24C'
    - - :warning
      - 'Line 1401: Product not found, record ignored., BaseItemCode=5202D24G'
    - - :warning
      - 'Line 1407: Product not found, record ignored., BaseItemCode=5203D16G'
    - - :warning
      - 'Line 1456: Product not found, record ignored., BaseItemCode=7872D17C'
    - - :warning
      - 'Line 1457: Product not found, record ignored., BaseItemCode=7872D17SS'
    - - :warning
      - 'Line 1589: Product not found, record ignored., BaseItemCode=BR20LED102-6PK'
    - - :warning
      - 'Line 1658: Product not found, record ignored., BaseItemCode=CF3004'
    - - :warning
      - 'Line 1812: Product not found, record ignored., BaseItemCode=KIT20204'
    - - :warning
      - 'Line 1813: Product not found, record ignored., BaseItemCode=KIT20402'
    - - :warning
      - 'Line 1814: Product not found, record ignored., BaseItemCode=KIT40606'
    - - :warning
      - 'Line 1815: Product not found, record ignored., BaseItemCode=KIT40804'
    - - :warning
      - 'Line 1882: Product not found, record ignored., BaseItemCode=LD2239C'
    - - :warning
      - 'Line 1919: Product not found, record ignored., BaseItemCode=LD2259BR'
    - - :warning
      - 'Line 1936: Product not found, record ignored., BaseItemCode=LD2274BK'
    - - :warning
      - 'Line 1938: Product not found, record ignored., BaseItemCode=LD2275BR'
    - - :warning
      - 'Line 1942: Product not found, record ignored., BaseItemCode=LD2277C'
    - - :warning
      - 'Line 1955: Product not found, record ignored., BaseItemCode=LD2300BR'
    - - :warning
      - 'Line 1958: Product not found, record ignored., BaseItemCode=LD2301BR'
    - - :warning
      - 'Line 1959: Product not found, record ignored., BaseItemCode=LD2301C'
    - - :warning
      - 'Line 1960: Product not found, record ignored., BaseItemCode=LD2302BK'
    - - :warning
      - 'Line 1961: Product not found, record ignored., BaseItemCode=LD2302BR'
    - - :warning
      - 'Line 1962: Product not found, record ignored., BaseItemCode=LD2302C'
    - - :warning
      - 'Line 1966: Product not found, record ignored., BaseItemCode=LD2304BK'
    - - :warning
      - 'Line 1969: Product not found, record ignored., BaseItemCode=LD2305BK'
    - - :warning
      - 'Line 1970: Product not found, record ignored., BaseItemCode=LD2305BR'
    - - :warning
      - 'Line 1971: Product not found, record ignored., BaseItemCode=LD2305C'
    - - :warning
      - 'Line 1972: Product not found, record ignored., BaseItemCode=LD2306BR'
    - - :warning
      - 'Line 1975: Product not found, record ignored., BaseItemCode=LD2307BR'
    - - :warning
      - 'Line 1979: Product not found, record ignored., BaseItemCode=LD2309C'
    - - :warning
      - 'Line 1980: Product not found, record ignored., BaseItemCode=LD2310BK'
    - - :warning
      - 'Line 1984: Product not found, record ignored., BaseItemCode=LD2311BR'
    - - :warning
      - 'Line 2037: Product not found, record ignored., BaseItemCode=LD2337BK'
    - - :warning
      - 'Line 2038: Product not found, record ignored., BaseItemCode=LD2337BR'
    - - :warning
      - 'Line 2039: Product not found, record ignored., BaseItemCode=LD2337C'
    - - :warning
      - 'Line 2040: Product not found, record ignored., BaseItemCode=LD2338BK'
    - - :warning
      - 'Line 2041: Product not found, record ignored., BaseItemCode=LD2338BR'
    - - :warning
      - 'Line 2042: Product not found, record ignored., BaseItemCode=LD2338C'
    - - :warning
      - 'Line 2043: Product not found, record ignored., BaseItemCode=LD2339BK'
    - - :warning
      - 'Line 2044: Product not found, record ignored., BaseItemCode=LD2339BR'
    - - :warning
      - 'Line 2045: Product not found, record ignored., BaseItemCode=LD2339C'
    - - :warning
      - 'Line 2046: Product not found, record ignored., BaseItemCode=LD2340BK'
    - - :warning
      - 'Line 2047: Product not found, record ignored., BaseItemCode=LD2340BR'
    - - :warning
      - 'Line 2048: Product not found, record ignored., BaseItemCode=LD2340C'
    - - :warning
      - 'Line 2049: Product not found, record ignored., BaseItemCode=LD2341BR'
    - - :warning
      - 'Line 2050: Product not found, record ignored., BaseItemCode=LD2344BK'
    - - :warning
      - 'Line 2051: Product not found, record ignored., BaseItemCode=LD2344BR'
    - - :warning
      - 'Line 2063: Product not found, record ignored., BaseItemCode=LD2350BK'
    - - :warning
      - 'Line 2064: Product not found, record ignored., BaseItemCode=LD2350BR'
    - - :warning
      - 'Line 2068: Product not found, record ignored., BaseItemCode=LD2352BK'
    - - :warning
      - 'Line 2069: Product not found, record ignored., BaseItemCode=LD2352BR'
    - - :warning
      - 'Line 2096: Product not found, record ignored., BaseItemCode=LD2363BK'
    - - :warning
      - 'Line 2097: Product not found, record ignored., BaseItemCode=LD2363BR'
    - - :warning
      - 'Line 2098: Product not found, record ignored., BaseItemCode=LD2364BK'
    - - :warning
      - 'Line 2099: Product not found, record ignored., BaseItemCode=LD2364BR'
    - - :warning
      - 'Line 2100: Product not found, record ignored., BaseItemCode=LD2364RED'
    - - :warning
      - 'Line 2101: Product not found, record ignored., BaseItemCode=LD2364WH'
    - - :warning
      - 'Line 2102: Product not found, record ignored., BaseItemCode=LD2365BK'
    - - :warning
      - 'Line 2103: Product not found, record ignored., BaseItemCode=LD2365BR'
    - - :warning
      - 'Line 2108: Product not found, record ignored., BaseItemCode=LD2367WH'
    - - :warning
      - 'Line 2110: Product not found, record ignored., BaseItemCode=LD2401WH'
    - - :warning
      - 'Line 2113: Product not found, record ignored., BaseItemCode=LD2404BN'
    - - :warning
      - 'Line 2115: Product not found, record ignored., BaseItemCode=LD2405HG'
    - - :warning
      - 'Line 2119: Product not found, record ignored., BaseItemCode=LD2407HG'
    - - :warning
      - 'Line 2126: Product not found, record ignored., BaseItemCode=LD2410WH'
    - - :warning
      - 'Line 2127: Product not found, record ignored., BaseItemCode=LD2411HG'
    - - :warning
      - 'Line 2128: Product not found, record ignored., BaseItemCode=LD2412WH'
    - - :warning
      - 'Line 2134: Product not found, record ignored., BaseItemCode=LD2450BK'
    - - :warning
      - 'Line 2135: Product not found, record ignored., BaseItemCode=LD2450BR'
    - - :warning
      - 'Line 2136: Product not found, record ignored., BaseItemCode=LD2450C'
    - - :warning
      - 'Line 2140: Product not found, record ignored., BaseItemCode=LD2453FLBK'
    - - :warning
      - 'Line 2141: Product not found, record ignored., BaseItemCode=LD2453FLBR'
    - - :warning
      - 'Line 2142: Product not found, record ignored., BaseItemCode=LD2453FLCG'
    - - :warning
      - 'Line 2158: Product not found, record ignored., BaseItemCode=LD4008D11BK'
    - - :warning
      - 'Line 2164: Product not found, record ignored., BaseItemCode=LD4017D48BRB'
    - - :warning
      - 'Line 2291: Product not found, record ignored., BaseItemCode=LD5016D17BK'
    - - :warning
      - 'Line 2302: Product not found, record ignored., BaseItemCode=LD5023'
    - - :warning
      - 'Line 2370: Product not found, record ignored., BaseItemCode=LD520D10BK'
    - - :warning
      - 'Line 2371: Product not found, record ignored., BaseItemCode=LD520D10BR'
    - - :warning
      - 'Line 2372: Product not found, record ignored., BaseItemCode=LD520D10C'
    - - :warning
      - 'Line 2373: Product not found, record ignored., BaseItemCode=LD520D13BK'
    - - :warning
      - 'Line 2374: Product not found, record ignored., BaseItemCode=LD520D13BR'
    - - :warning
      - 'Line 2375: Product not found, record ignored., BaseItemCode=LD520D13C'
    - - :warning
      - 'Line 2376: Product not found, record ignored., BaseItemCode=LD520D16BK'
    - - :warning
      - 'Line 2377: Product not found, record ignored., BaseItemCode=LD520D16BR'
    - - :warning
      - 'Line 2378: Product not found, record ignored., BaseItemCode=LD520D16C'
    - - :warning
      - 'Line 2379: Product not found, record ignored., BaseItemCode=LD520D18BK'
    - - :warning
      - 'Line 2380: Product not found, record ignored., BaseItemCode=LD520D18BR'
    - - :warning
      - 'Line 2381: Product not found, record ignored., BaseItemCode=LD520D18C'
    - - :warning
      - 'Line 2382: Product not found, record ignored., BaseItemCode=LD520D20BR'
    - - :warning
      - 'Line 2391: Product not found, record ignored., BaseItemCode=LD6005D12BR'
    - - :warning
      - 'Line 2408: Product not found, record ignored., BaseItemCode=LD6010D26BN'
    - - :warning
      - 'Line 2414: Product not found, record ignored., BaseItemCode=LD6012D15G'
    - - :warning
      - 'Line 2425: Product not found, record ignored., BaseItemCode=LD6016'
    - - :warning
      - 'Line 2471: Product not found, record ignored., BaseItemCode=LD6077C'
    - - :warning
      - 'Line 2481: Product not found, record ignored., BaseItemCode=LD6100C'
    - - :warning
      - 'Line 2495: Product not found, record ignored., BaseItemCode=LD6109BR'
    - - :warning
      - 'Line 2502: Product not found, record ignored., BaseItemCode=LD6124C'
    - - :warning
      - 'Line 2509: Product not found, record ignored., BaseItemCode=LD6133BR'
    - - :warning
      - 'Line 2537: Product not found, record ignored., BaseItemCode=LD6170C'
    - - :warning
      - 'Line 2540: Product not found, record ignored., BaseItemCode=LD6173BR'
    - - :warning
      - 'Line 2543: Product not found, record ignored., BaseItemCode=LD6176C'
    - - :warning
      - 'Line 2544: Product not found, record ignored., BaseItemCode=LD6178BR'
    - - :warning
      - 'Line 2558: Product not found, record ignored., BaseItemCode=LD6205C'
    - - :warning
      - 'Line 2568: Product not found, record ignored., BaseItemCode=LD6220C'
    - - :warning
      - 'Line 2574: Product not found, record ignored., BaseItemCode=LD6232C'
    - - :warning
      - 'Line 2575: Product not found, record ignored., BaseItemCode=LD6238C'
    - - :warning
      - 'Line 2581: Product not found, record ignored., BaseItemCode=LD6248BR'
    - - :warning
      - 'Line 2587: Product not found, record ignored., BaseItemCode=LD6259C'
    - - :warning
      - 'Line 2603: Product not found, record ignored., BaseItemCode=LD642D36BR'
    - - :warning
      - 'Line 2604: Product not found, record ignored., BaseItemCode=LD642D36BRK'
    - - :warning
      - 'Line 2605: Product not found, record ignored., BaseItemCode=LD643D36BK'
    - - :warning
      - 'Line 2620: Product not found, record ignored., BaseItemCode=LD648F26BK'
    - - :warning
      - 'Line 2622: Product not found, record ignored., BaseItemCode=LD648F26BRK'
    - - :warning
      - 'Line 2633: Product not found, record ignored., BaseItemCode=LD652D30BR'
    - - :warning
      - 'Line 2642: Product not found, record ignored., BaseItemCode=LD655D18BR'
    - - :warning
      - 'Line 2643: Product not found, record ignored., BaseItemCode=LD655D18BRK'
    - - :warning
      - 'Line 2650: Product not found, record ignored., BaseItemCode=LD6802D14C'
    - - :warning
      - 'Line 2683: Product not found, record ignored., BaseItemCode=LD7024D25BK'
    - - :warning
      - 'Line 2685: Product not found, record ignored., BaseItemCode=LD7024D25SN'
    - - :warning
      - 'Line 2752: Product not found, record ignored., BaseItemCode=LD7044D26WD'
    - - :warning
      - 'Line 2760: Product not found, record ignored., BaseItemCode=LD7047D28BR'
    - - :warning
      - 'Line 2779: Product not found, record ignored., BaseItemCode=LD7057D20BK'
    - - :warning
      - 'Line 2809: Product not found, record ignored., BaseItemCode=LD7071D14BK'
    - - :warning
      - 'Line 2879: Product not found, record ignored., BaseItemCode=LD7301W15CH'
    - - :warning
      - 'Line 2892: Product not found, record ignored., BaseItemCode=LD7302W24BLK'
    - - :warning
      - 'Line 2900: Product not found, record ignored., BaseItemCode=LD7302W6CH'
    - - :warning
      - 'Line 2917: Product not found, record ignored., BaseItemCode=LD7304W22BRA'
    - - :warning
      - 'Line 2922: Product not found, record ignored., BaseItemCode=LD7304W7BLK'
    - - :warning
      - 'Line 2942: Product not found, record ignored., BaseItemCode=LD7307W24CH'
    - - :warning
      - 'Line 2976: Product not found, record ignored., BaseItemCode=LD7310W23BLK'
    - - :warning
      - 'Line 3147: Product not found, record ignored., BaseItemCode=LD7327W6BLK'
    - - :warning
      - 'Line 3159: Product not found, record ignored., BaseItemCode=LD7331W7BLK'
    - - :warning
      - 'Line 3218: Product not found, record ignored., BaseItemCode=LD8049D10BR'
    - - :warning
      - 'Line 3240: Product not found, record ignored., BaseItemCode=LD810F19SL'
    - - :warning
      - 'Line 3293: Product not found, record ignored., BaseItemCode=LD8801D43GB'
    - - :warning
      - 'Line 3323: Product not found, record ignored., BaseItemCode=LDOD3004-6PK'
    - - :warning
      - 'Line 3324: Product not found, record ignored., BaseItemCode=LDOD3006-4PK'
    - - :warning
      - 'Line 3339: Product not found, record ignored., BaseItemCode=LDOD4010BK'
    - - :warning
      - 'Line 3341: Product not found, record ignored., BaseItemCode=LDOD4011BK'
    - - :warning
      - 'Line 3343: Product not found, record ignored., BaseItemCode=LDOD4011WH'
    - - :warning
      - 'Line 3347: Product not found, record ignored., BaseItemCode=LDOD4013WH'
    - - :warning
      - 'Line 3354: Product not found, record ignored., BaseItemCode=LDOD4016BK'
    - - :warning
      - 'Line 3356: Product not found, record ignored., BaseItemCode=LDOD4016WH'
    - - :warning
      - 'Line 3395: Product not found, record ignored., BaseItemCode=LDPD2000BN'
    - - :warning
      - 'Line 3403: Product not found, record ignored., BaseItemCode=LDPD2003BN'
    - - :warning
      - 'Line 3409: Product not found, record ignored., BaseItemCode=LDPD2017'
    - - :warning
      - 'Line 3424: Product not found, record ignored., BaseItemCode=LDPD2045HG'
    - - :warning
      - 'Line 3427: Product not found, record ignored., BaseItemCode=LDPD2046WH'
    - - :warning
      - 'Line 3474: Product not found, record ignored., BaseItemCode=LDPG2256BK'
    - - :warning
      - 'Line 3475: Product not found, record ignored., BaseItemCode=LDPG2256BR'
    - - :warning
      - 'Line 3483: Product not found, record ignored., BaseItemCode=LDPG6037BR'
    - - :warning
      - 'Line 3499: Product not found, record ignored., BaseItemCode=MF53047BL'
    - - :warning
      - 'Line 3509: Product not found, record ignored., BaseItemCode=MF6-1008S'
    - - :warning
      - 'Line 3517: Product not found, record ignored., BaseItemCode=MF6-1036AW'
    - - :warning
      - 'Line 3518: Product not found, record ignored., BaseItemCode=MF6-1036BL'
    - - :warning
      - 'Line 3523: Product not found, record ignored., BaseItemCode=MF61060AW'
    - - :warning
      - 'Line 3524: Product not found, record ignored., BaseItemCode=MF61060AW-F1'
    - - :warning
      - 'Line 3525: Product not found, record ignored., BaseItemCode=MF61072BL'
    - - :warning
      - 'Line 3585: Product not found, record ignored., BaseItemCode=MF72038BK'
    - - :warning
      - 'Line 3597: Product not found, record ignored., BaseItemCode=MF73016BK'
    - - :warning
      - 'Line 3616: Product not found, record ignored., BaseItemCode=MF82002WH'
    - - :warning
      - 'Line 3623: Invalid next scheduled receipt date'
    - - :warning
      - 'Line 3842: Product not found, record ignored., BaseItemCode=MR33248BL'
    - - :warning
      - 'Line 3843: Product not found, record ignored., BaseItemCode=MR33272BL'
    - - :warning
      - 'Line 3865: Product not found, record ignored., BaseItemCode=MR4044WH'
    - - :warning
      - 'Line 3875: Product not found, record ignored., BaseItemCode=MR4054GR'
    - - :warning
      - 'Line 3894: Product not found, record ignored., BaseItemCode=MR4071BL'
    - - :warning
      - 'Line 3916: Product not found, record ignored., BaseItemCode=MR41828BL'
    - - :warning
      - 'Line 3924: Product not found, record ignored., BaseItemCode=MR42036BL'
    - - :warning
      - 'Line 3937: Product not found, record ignored., BaseItemCode=MR42736BL'
    - - :warning
      - 'Line 3994: Product not found, record ignored., BaseItemCode=MR4718BL'
    - - :warning
      - 'Line 3998: Product not found, record ignored., BaseItemCode=MR4721BL'
    - - :warning
      - 'Line 4000: Product not found, record ignored., BaseItemCode=MR4721GR'
    - - :warning
      - 'Line 4035: Product not found, record ignored., BaseItemCode=MR52736'
    - - :warning
      - 'Line 4036: Product not found, record ignored., BaseItemCode=MR53648'
    - - :warning
      - 'Line 4037: Product not found, record ignored., BaseItemCode=MR53660'
    - - :warning
      - 'Line 4058: Product not found, record ignored., BaseItemCode=MR652828BK'
    - - :warning
      - 'Line 4147: Product not found, record ignored., BaseItemCode=MR913240'
    - - :warning
      - 'Line 4155: Invalid next scheduled receipt date'
    - - :warning
      - 'Line 4156: Product not found, record ignored., BaseItemCode=MR9239'
    - - :warning
      - 'Line 4190: Product not found, record ignored., BaseItemCode=MRE32432BK'
    - - :warning
      - 'Line 4193: Product not found, record ignored., BaseItemCode=MRE32471BK'
    - - :warning
      - 'Line 4209: Product not found, record ignored., BaseItemCode=MRE52036'
    - - :warning
      - 'Line 4210: Product not found, record ignored., BaseItemCode=MRE52040'
    - - :warning
      - 'Line 4211: Product not found, record ignored., BaseItemCode=MRE52436'
    - - :warning
      - 'Line 4212: Product not found, record ignored., BaseItemCode=MRE52440'
    - - :warning
      - 'Line 4213: Product not found, record ignored., BaseItemCode=MRE52730'
    - - :warning
      - 'Line 4214: Product not found, record ignored., BaseItemCode=MRE52736'
    - - :warning
      - 'Line 4215: Product not found, record ignored., BaseItemCode=MRE52740'
    - - :warning
      - 'Line 4216: Product not found, record ignored., BaseItemCode=MRE53030'
    - - :warning
      - 'Line 4217: Product not found, record ignored., BaseItemCode=MRE53072'
    - - :warning
      - 'Line 4218: Product not found, record ignored., BaseItemCode=MRE53648'
    - - :warning
      - 'Line 4219: Product not found, record ignored., BaseItemCode=MRE54260'
    - - :warning
      - 'Line 4302: Product not found, record ignored., BaseItemCode=MRE92030'
    - - :warning
      - 'Line 4303: Product not found, record ignored., BaseItemCode=MRE92436'
    - - :warning
      - 'Line 4306: Product not found, record ignored., BaseItemCode=MRE93248'
    - - :warning
      - 'Line 4307: Product not found, record ignored., BaseItemCode=MRE93272'
    - - :warning
      - 'Line 4414: Product not found, record ignored., BaseItemCode=RN61550RF-4PK'
    - - :warning
      - 'Line 4415: Product not found, record ignored., BaseItemCode=RS41050SDK-4PK'
    - - :warning
      - 'Line 4484: Product not found, record ignored., BaseItemCode=TC5R-E26-6PK'
    - - :warning
      - 'Line 4485: Product not found, record ignored., BaseItemCode=TC6R-E26-6PK'
    - - :warning
      - 'Line 4505: Product not found, record ignored., BaseItemCode=TKACP-MW'
    - - :warning
      - 'Line 4506: Product not found, record ignored., BaseItemCode=TKAEF-MW'
    - - :warning
      - 'Line 4507: Product not found, record ignored., BaseItemCode=TKAFCF-BK'
    - - :warning
      - 'Line 4508: Product not found, record ignored., BaseItemCode=TKALC-BK'
    - - :warning
      - 'Line 4509: Product not found, record ignored., BaseItemCode=TKATC-BK'
    - - :warning
      - 'Line 4510: Product not found, record ignored., BaseItemCode=TKATC-MW'
    - - :warning
      - 'Line 4511: Product not found, record ignored., BaseItemCode=TKH210BK-6PK'
    - - :warning
      - 'Line 4512: Product not found, record ignored., BaseItemCode=TKL4BK'
    - - :warning
      - 'Line 4513: Product not found, record ignored., BaseItemCode=TKL4MW'
    - - :warning
      - 'Line 4525: Product not found, record ignored., BaseItemCode=V1800D24BK/RC'
    - - :warning
      - 'Line 4603: Product not found, record ignored., BaseItemCode=V1803W12SG/RC'
    - - :warning
      - 'Line 4638: Product not found, record ignored., BaseItemCode=V2006F14C/RC'
    - - :warning
      - 'Line 4640: Product not found, record ignored., BaseItemCode=V2006F16C/RC'
    - - :warning
      - 'Line 4648: Product not found, record ignored., BaseItemCode=V2011D21G/RC'
    - - :warning
      - 'Line 4705: Product not found, record ignored., BaseItemCode=V2032D24C/RC'
    - - :warning
      - 'Line 4711: Product not found, record ignored., BaseItemCode=V2032F14C/RC'
    - - :warning
      - 'Line 4718: Product not found, record ignored., BaseItemCode=V2032W30BK/RC'
    - - :warning
      - 'Line 4719: Product not found, record ignored., BaseItemCode=V2032W36BK/RC'
    - - :warning
      - 'Line 4724: Product not found, record ignored., BaseItemCode=V2033D24C/RC'
    - - :warning
      - 'Line 4726: Product not found, record ignored., BaseItemCode=V2033F14C/RC'
    - - :warning
      - 'Line 4733: Product not found, record ignored., BaseItemCode=V2034D28C/RC'
    - - :warning
      - 'Line 4736: Product not found, record ignored., BaseItemCode=V2035D28C/RC'
    - - :warning
      - 'Line 4737: Product not found, record ignored., BaseItemCode=V2075D18C/RC'
    - - :warning
      - 'Line 4748: Product not found, record ignored., BaseItemCode=V2100D35C/RC'
    - - :warning
      - 'Line 4796: Product not found, record ignored., BaseItemCode=V3100D40C/RC'
    - - :warning
      - 'Line 4798: Product not found, record ignored., BaseItemCode=V6801D14C/RC'
    - - :warning
      - 'Line 4799: Product not found, record ignored., BaseItemCode=V6801D19G/RC'
    - - :warning
      - 'Line 4801: Product not found, record ignored., BaseItemCode=V7803D11B-JT/RC'
    - - :warning
      - 'Line 4805: Product not found, record ignored., BaseItemCode=V7804D15GS-GS/RC'
    - - :warning
      - 'Line 4807: Product not found, record ignored., BaseItemCode=V7804D15PE/RC'
    - - :warning
      - 'Line 4808: Product not found, record ignored., BaseItemCode=V7804D15PK-RO/RC'
    - - :warning
      - 'Line 4882: Product not found, record ignored., BaseItemCode=V9800D20G/RC'
    - - :warning
      - 'Line 4883: Product not found, record ignored., BaseItemCode=V9800D24C/RC'
    - - :warning
      - 'Line 4884: Product not found, record ignored., BaseItemCode=V9800D24G/RC'
    - - :warning
      - 'Line 4885: Product not found, record ignored., BaseItemCode=V9800D28C/RC'
    - - :warning
      - 'Line 4894: Product not found, record ignored., BaseItemCode=V9805F10BK/RC'
    - - :warning
      - 'Line 4895: Product not found, record ignored., BaseItemCode=V9805F10C/RC'
    - - :warning
      - 'Line 4896: Product not found, record ignored., BaseItemCode=V9805F10G/RC'
    - - :warning
      - 'Line 4969: Product not found, record ignored., BaseItemCode=VF-1030VM'
    - - :warning
      - 'Line 4999: Product not found, record ignored., BaseItemCode=VF12319GR'
    - - :warning
      - 'Line 5030: Product not found, record ignored., BaseItemCode=VF12360DGR-VW'
    - - :warning
      - 'Line 5148: Product not found, record ignored., BaseItemCode=VF13060DAB-VW'
    - - :warning
      - 'Line 5153: Product not found, record ignored., BaseItemCode=VF13060DVM-VW'
    - - :warning
      - 'Line 5192: Product not found, record ignored., BaseItemCode=VF15032GN'
    - - :warning
      - 'Line 5328: Product not found, record ignored., BaseItemCode=VF17018WH'
    - - :warning
      - 'Line 5581: Product not found, record ignored., BaseItemCode=VF27048GN'
    - - :warning
      - 'Line 5769: Product not found, record ignored., BaseItemCode=VF41048MGN'
    - - :warning
      - 'Line 5799: Product not found, record ignored., BaseItemCode=VF42524MGN'
    - - :warning
      - 'Line 5800: Product not found, record ignored., BaseItemCode=VF42524MMP'
    - - :warning
      - 'Line 5872: Product not found, record ignored., BaseItemCode=VF43030CG'
    - - :warning
      - 'Line 5879: Product not found, record ignored., BaseItemCode=VF43040WB'
    - - :warning
      - 'Line 5889: Product not found, record ignored., BaseItemCode=VF43524MWH'
    - - :warning
      - 'Line 5898: Product not found, record ignored., BaseItemCode=VF43530MMP'
    - - :warning
      - 'Line 5899: Product not found, record ignored., BaseItemCode=VF43530MMP-BS'
    - - :warning
      - 'Line 5900: Product not found, record ignored., BaseItemCode=VF43530MTK'
    - - :warning
      - 'Line 5901: Product not found, record ignored., BaseItemCode=VF43530MTK-BS'
    - - :warning
      - 'Line 5920: Product not found, record ignored., BaseItemCode=VF43536MWT'
    - - :warning
      - 'Line 5921: Product not found, record ignored., BaseItemCode=VF43536MWT-BS'
    - - :warning
      - 'Line 5973: Product not found, record ignored., BaseItemCode=VF44524MMP'
    - - :warning
      - 'Line 5975: Product not found, record ignored., BaseItemCode=VF44524MTK'
    - - :warning
      - 'Line 5983: Product not found, record ignored., BaseItemCode=VF44530MWT'
    - - :warning
      - 'Line 5995: Product not found, record ignored., BaseItemCode=VF44536MWH'
    - - :warning
      - 'Line 6016: Product not found, record ignored., BaseItemCode=VF44548MMP'
    - - :warning
      - 'Line 6019: Product not found, record ignored., BaseItemCode=VF44548MWH'
    - - :warning
      - 'Line 6029: Product not found, record ignored., BaseItemCode=VF46030MBL'
    - - :warning
      - 'Line 6036: Product not found, record ignored., BaseItemCode=VF46036MBL'
    - - :warning
      - 'Line 6049: Product not found, record ignored., BaseItemCode=VF46048MBL'
    - - :warning
      - 'Line 6050: Product not found, record ignored., BaseItemCode=VF46048MMP'
    - - :warning
      - 'Line 6090: Product not found, record ignored., BaseItemCode=VF47042MBL'
    - - :warning
      - 'Line 6093: Product not found, record ignored., BaseItemCode=VF47042MMP'
    - - :warning
      - 'Line 6094: Product not found, record ignored., BaseItemCode=VF47042MMP-BS'
    - - :warning
      - 'Line 6115: Product not found, record ignored., BaseItemCode=VF48018MBL'
    - - :warning
      - 'Line 6117: Product not found, record ignored., BaseItemCode=VF48018MWH'
    - - :warning
      - 'Line 6118: Product not found, record ignored., BaseItemCode=VF48018MWT'
    - - :warning
      - 'Line 6119: Product not found, record ignored., BaseItemCode=VF48018NT'
    - - :warning
      - 'Line 6160: Product not found, record ignored., BaseItemCode=VF48060DMTK'
    - - :warning
      - 'Line 6167: Product not found, record ignored., BaseItemCode=VF48818MW'
    - - :warning
      - 'Line 6168: Product not found, record ignored., BaseItemCode=VF48818MWH'
    - - :warning
      - 'Line 6170: Product not found, record ignored., BaseItemCode=VF48818NT'
    - - :warning
      - 'Line 6196: Product not found, record ignored., BaseItemCode=VF48832MBL'
    - - :warning
      - 'Line 6197: Product not found, record ignored., BaseItemCode=VF48832MBL-BS'
    - - :warning
      - 'Line 6244: Product not found, record ignored., BaseItemCode=VF48848MBL'
    - - :warning
      - 'Line 6249: Product not found, record ignored., BaseItemCode=VF48848MWH'
    - - :warning
      - 'Line 6250: Product not found, record ignored., BaseItemCode=VF48848MWT'
    - - :warning
      - 'Line 6251: Product not found, record ignored., BaseItemCode=VF48848NT'
    - - :warning
      - 'Line 6305: Product not found, record ignored., BaseItemCode=VF50060DGN'
    - - :warning
      - 'Line 6328: Product not found, record ignored., BaseItemCode=VF53042GN'
    - - :warning
      - 'Line 6336: Product not found, record ignored., BaseItemCode=VF53060DBL'
    - - :warning
      - 'Line 6506: Product not found, record ignored., BaseItemCode=VF90242MGN'
    - - :warning
      - 'Line 6507: Product not found, record ignored., BaseItemCode=VF90242MGN-BS'
    - - :warning
      - 'Line 6516: Product not found, record ignored., BaseItemCode=VF90248MGN'
    - - :warning
      - 'Line 6517: Product not found, record ignored., BaseItemCode=VF90248MGN-BS'
    - - :warning
      - 'Line 6528: Product not found, record ignored., BaseItemCode=VM13236AB'
    - - :warning
      - 'Line 7012: Product not found, record ignored., BaseItemCode=MR6C2132BLK'
    - - :warning
      - 'Line 7478: Product not found, record ignored., BaseItemCode=W122-DB'
    - - :warning
      - 'Line 9461: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY01'
    - - :warning
      - 'Line 9462: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY02'
    - - :warning
      - 'Line 9463: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY03'
    - - :warning
      - 'Line 9464: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY04'
    - - :warning
      - 'Line 9465: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY06'
    - - :warning
      - 'Line 9466: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY07'
    - - :warning
      - 'Line 9467: Product not found, record ignored., BaseItemCode=LVFSN5.5-GRY20'
    - - :warning
      - 'Line 9468: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK01'
    - - :warning
      - 'Line 9469: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK02'
    - - :warning
      - 'Line 9470: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK03'
    - - :warning
      - 'Line 9471: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK04'
    - - :warning
      - 'Line 9472: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK05'
    - - :warning
      - 'Line 9473: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK20'
    - - :warning
      - 'Line 9474: Product not found, record ignored., BaseItemCode=LVFSN5.5-OAK21'
    - - :warning
      - 'Line 9475: Product not found, record ignored., BaseItemCode=LVFSN7-GRY01'
    - - :warning
      - 'Line 9476: Product not found, record ignored., BaseItemCode=LVFSN7-GRY02'
    - - :warning
      - 'Line 9477: Product not found, record ignored., BaseItemCode=LVFSN7-GRY03'
    - - :warning
      - 'Line 9478: Product not found, record ignored., BaseItemCode=LVFSN7-GRY04'
    - - :warning
      - 'Line 9479: Product not found, record ignored., BaseItemCode=LVFSN7-GRY06'
    - - :warning
      - 'Line 9480: Product not found, record ignored., BaseItemCode=LVFSN7-GRY07'
    - - :warning
      - 'Line 9481: Product not found, record ignored., BaseItemCode=LVFSN7-GRY20'
    - - :warning
      - 'Line 9482: Product not found, record ignored., BaseItemCode=LVFSN7-OAK01'
    - - :warning
      - 'Line 9483: Product not found, record ignored., BaseItemCode=LVFSN7-OAK02'
    - - :warning
      - 'Line 9484: Product not found, record ignored., BaseItemCode=LVFSN7-OAK03'
    - - :warning
      - 'Line 9485: Product not found, record ignored., BaseItemCode=LVFSN7-OAK04'
    - - :warning
      - 'Line 9486: Product not found, record ignored., BaseItemCode=LVFSN7-OAK05'
    - - :warning
      - 'Line 9487: Product not found, record ignored., BaseItemCode=LVFSN7-OAK20'
    - - :warning
      - 'Line 9488: Product not found, record ignored., BaseItemCode=LVFSN7-OAK21'
    - - :warning
      - 'Line 9489: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY01'
    - - :warning
      - 'Line 9490: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY02'
    - - :warning
      - 'Line 9491: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY03'
    - - :warning
      - 'Line 9492: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY04'
    - - :warning
      - 'Line 9493: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY06'
    - - :warning
      - 'Line 9494: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY07'
    - - :warning
      - 'Line 9495: Product not found, record ignored., BaseItemCode=LVRDM5.5-GRY20'
    - - :warning
      - 'Line 9496: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK01'
    - - :warning
      - 'Line 9497: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK02'
    - - :warning
      - 'Line 9498: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK03'
    - - :warning
      - 'Line 9499: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK04'
    - - :warning
      - 'Line 9500: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK05'
    - - :warning
      - 'Line 9501: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK20'
    - - :warning
      - 'Line 9502: Product not found, record ignored., BaseItemCode=LVRDM5.5-OAK21'
    - - :warning
      - 'Line 9503: Product not found, record ignored., BaseItemCode=LVRDM7-GRY01'
    - - :warning
      - 'Line 9504: Product not found, record ignored., BaseItemCode=LVRDM7-GRY02'
    - - :warning
      - 'Line 9505: Product not found, record ignored., BaseItemCode=LVRDM7-GRY03'
    - - :warning
      - 'Line 9506: Product not found, record ignored., BaseItemCode=LVRDM7-GRY04'
    - - :warning
      - 'Line 9507: Product not found, record ignored., BaseItemCode=LVRDM7-GRY06'
    - - :warning
      - 'Line 9508: Product not found, record ignored., BaseItemCode=LVRDM7-GRY07'
    - - :warning
      - 'Line 9509: Product not found, record ignored., BaseItemCode=LVRDM7-GRY20'
    - - :warning
      - 'Line 9510: Product not found, record ignored., BaseItemCode=LVRDM7-OAK01'
    - - :warning
      - 'Line 9511: Product not found, record ignored., BaseItemCode=LVRDM7-OAK02'
    - - :warning
      - 'Line 9512: Product not found, record ignored., BaseItemCode=LVRDM7-OAK03'
    - - :warning
      - 'Line 9513: Product not found, record ignored., BaseItemCode=LVRDM7-OAK04'
    - - :warning
      - 'Line 9514: Product not found, record ignored., BaseItemCode=LVRDM7-OAK05'
    - - :warning
      - 'Line 9515: Product not found, record ignored., BaseItemCode=LVRDM7-OAK20'
    - - :warning
      - 'Line 9516: Product not found, record ignored., BaseItemCode=LVRDM7-OAK21'
    - - :warning
      - 'Line 9517: Product not found, record ignored., BaseItemCode=LVST-GRY01'
    - - :warning
      - 'Line 9518: Product not found, record ignored., BaseItemCode=LVST-GRY02'
    - - :warning
      - 'Line 9519: Product not found, record ignored., BaseItemCode=LVST-GRY03'
    - - :warning
      - 'Line 9520: Product not found, record ignored., BaseItemCode=LVST-GRY04'
    - - :warning
      - 'Line 9521: Product not found, record ignored., BaseItemCode=LVST-GRY06'
    - - :warning
      - 'Line 9522: Product not found, record ignored., BaseItemCode=LVST-GRY07'
    - - :warning
      - 'Line 9523: Product not found, record ignored., BaseItemCode=LVST-GRY20'
    - - :warning
      - 'Line 9524: Product not found, record ignored., BaseItemCode=LVST-OAK01'
    - - :warning
      - 'Line 9525: Product not found, record ignored., BaseItemCode=LVST-OAK02'
    - - :warning
      - 'Line 9526: Product not found, record ignored., BaseItemCode=LVST-OAK03'
    - - :warning
      - 'Line 9527: Product not found, record ignored., BaseItemCode=LVST-OAK04'
    - - :warning
      - 'Line 9528: Product not found, record ignored., BaseItemCode=LVST-OAK05'
    - - :warning
      - 'Line 9529: Product not found, record ignored., BaseItemCode=LVST-OAK20'
    - - :warning
      - 'Line 9530: Product not found, record ignored., BaseItemCode=LVST-OAK21'
    - - :warning
      - 'Line 9531: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY01'
    - - :warning
      - 'Line 9532: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY02'
    - - :warning
      - 'Line 9533: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY03'
    - - :warning
      - 'Line 9534: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY04'
    - - :warning
      - 'Line 9535: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY06'
    - - :warning
      - 'Line 9536: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY07'
    - - :warning
      - 'Line 9537: Product not found, record ignored., BaseItemCode=LVTM5.5-GRY20'
    - - :warning
      - 'Line 9538: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK01'
    - - :warning
      - 'Line 9539: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK02'
    - - :warning
      - 'Line 9540: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK03'
    - - :warning
      - 'Line 9541: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK04'
    - - :warning
      - 'Line 9542: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK05'
    - - :warning
      - 'Line 9543: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK20'
    - - :warning
      - 'Line 9544: Product not found, record ignored., BaseItemCode=LVTM5.5-OAK21'
    - - :warning
      - 'Line 9545: Product not found, record ignored., BaseItemCode=LVTM7-GRY01'
    - - :warning
      - 'Line 9546: Product not found, record ignored., BaseItemCode=LVTM7-GRY02'
    - - :warning
      - 'Line 9547: Product not found, record ignored., BaseItemCode=LVTM7-GRY03'
    - - :warning
      - 'Line 9548: Product not found, record ignored., BaseItemCode=LVTM7-GRY04'
    - - :warning
      - 'Line 9549: Product not found, record ignored., BaseItemCode=LVTM7-GRY06'
    - - :warning
      - 'Line 9550: Product not found, record ignored., BaseItemCode=LVTM7-GRY07'
    - - :warning
      - 'Line 9551: Product not found, record ignored., BaseItemCode=LVTM7-GRY20'
    - - :warning
      - 'Line 9552: Product not found, record ignored., BaseItemCode=LVTM7-OAK01'
    - - :warning
      - 'Line 9553: Product not found, record ignored., BaseItemCode=LVTM7-OAK02'
    - - :warning
      - 'Line 9554: Product not found, record ignored., BaseItemCode=LVTM7-OAK03'
    - - :warning
      - 'Line 9555: Product not found, record ignored., BaseItemCode=LVTM7-OAK04'
    - - :warning
      - 'Line 9556: Product not found, record ignored., BaseItemCode=LVTM7-OAK05'
    - - :warning
      - 'Line 9557: Product not found, record ignored., BaseItemCode=LVTM7-OAK20'
    - - :warning
      - 'Line 9558: Product not found, record ignored., BaseItemCode=LVTM7-OAK21'
 |

### Q-10_results.md

# Q-10 Results — Elegant Furniture & Lighting (eli, org_id=68)
- **Query**: Q-10 — Feature Enablement Gap Analysis
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| enable_sales_portal | enable_online_catalog | enable_online_ordering | kit_item_count | contract_price_count | enrollment_count | smart_stack_count | shared_resource_count | portal_order_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 10 | 0 | 1,263 | 16 | 32 | 0 |

### Q-11_results.md

# Q-11 Results — Elegant Furniture & Lighting (eli, org_id=68)
- **Query**: Q-11 — Configuration Completeness
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 14
- **Run date**: 2026-06-17


| entity_type | last_updated | days_stale | related_record_count |
| --- | --- | --- | --- |
| option_groups | 2025-08-07 23:13:01 | 313 | — |
| options | 2025-08-07 23:13:01 | 313 | — |
| matrix_options | 2025-08-07 23:13:01 | 313 | — |
| kit_items | 2025-08-07 23:13:01 | 313 | 10 |
| customer_favorites | 2025-08-07 23:13:01 | 313 | — |
| contract_prices | 2025-08-07 23:13:01 | 313 | 0 |
| commitment_reports | 2025-08-07 23:13:01 | 313 | — |
| placement_reports | 2025-08-07 23:13:01 | 313 | — |
| riser_prices | 2025-08-07 23:13:01 | 313 | — |
| customer_payment_informations | 2025-08-07 23:13:01 | 313 | — |
| sales_quotas | 2025-08-07 23:13:01 | 313 | 0 |
| price_levels | 2026-03-06 20:20:22 | 103 | — |
| portal_orders | 2026-03-13 14:23:30 | 96 | — |
| portal_invoices | 2026-03-13 14:23:30 | 96 | — |

### Q-22_results.md

# Q-22 Results — Elegant Furniture & Lighting (eli, org_id=68)
- **Query**: Q-22 — Feature Usage Depth
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | submit_order | select_a_customer | search_for_customer | email_item_info | create_pdf_catalog | view_library_entry | view_smartpicks | access_sales_portal | filter_products | search_products | search_collections | order_configured_item | view_kit | order_kit | share_my_list | export_data_to_csv | export_data_to_excel | total_events | total_users |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| eli | Elegant Furniture & Lighting | 565 | 3,694 | 6,222 | 807 | 1,047 | 4,304 | 9 | 0 | 521 | 31,742 | 242 | 2 | 0 | 0 | 17 | 0 | 0 | 80,303 | 88 |

### Q-CI-02_results.md

# Q-CI-02 Results — Elegant Furniture & Lighting (eli, org_id=68)
- **Query**: Q-CI-02 — Peer Comparison
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | peer_standing | orders_vs_peer_pct | logins_vs_peer_pct | mrr_vs_peer_pct | peer_orders_median | peer_logins_median | peer_mrr_median |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| eli | Elegant Furniture & Lighting | Platform-Embedded | Needs Attention | -79.60 | 25 | 46.90 | 2,764 | 6,896 | 1,685 |

### Q-CI-03_results.md

# Q-CI-03 Results — Elegant Furniture & Lighting (eli, org_id=68)
- **Query**: Q-CI-03 — Feature Adoption Benchmarking
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | feature_depth | has_clicky_portal | arr |
| --- | --- | --- | --- | --- | --- |
| eli | Elegant Furniture & Lighting | Platform-Embedded | 5 | 0 | 27,060 |

### Q-CI-03_benchmarks_results.md

# Q-CI-03-bench Results — Elegant Furniture & Lighting (eli, org_id=68)
- **Query**: Q-CI-03-bench — Segment Benchmarks Monthly
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 3
- **Run date**: 2026-06-17


| segment | benchmark_month | org_count | submit_order_p10 | submit_order_p25 | submit_order_median | submit_order_p75 | submit_order_p90 | total_logins_p25 | total_logins_median | total_logins_p75 | search_products_p25 | search_products_median | search_products_p75 | mrr_p25 | mrr_median | mrr_p75 | arr_p25 | arr_median | arr_p75 | feature_kit_items_pct | feature_portal_orders_pct | feature_sales_portal_pct | feature_library_pct | feature_pdf_catalog_pct | feature_cpq_pct | created_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Platform-Embedded | 2026-06-01 | 48 | 561 | 992 | 2,764 | 4,600 | 7,927 | 4,922 | 6,896 | 9,296 | 20,725 | 36,666 | 45,385 | 0 | 1,685 | 2,030 | 0 | 16,980 | 25,555 | 0.29 | 0.67 | 0.67 | 1 | 1 | 0.40 | 2026-06-01 10:00 |
| Platform-Embedded | 2026-05-01 | 47 | 578 | 1,045 | 2,891 | 5,553 | 7,484 | 4,757 | 6,848 | 9,186 | 19,425 | 35,124 | 44,759 | 0 | 1,685 | 2,030 | 0 | 16,980 | 25,555 | 0.30 | 0.66 | 0.66 | 1 | 1 | 0.40 | 2026-05-01 10:00 |
| Platform-Embedded | 2026-04-01 | 47 | 543 | 935 | 2,748 | 5,196 | 7,092 | 4,681 | 6,458 | 8,730 | 18,101 | 33,085 | 44,759 | 0 | 1,685 | 2,030 | 0 | 16,980 | 25,555 | 0.28 | 0.66 | 0.66 | 1 | 1 | 0.40 | 2026-04-01 10:00 |

### Q-CI-05_results.md

(not present — file does not exist or is empty)

### peer_benchmark_extract.md

(not present — file does not exist or is empty)
