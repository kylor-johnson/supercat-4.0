# Section 6 Context Bundle — Hudson Valley Lighting (hvl)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Hudson Valley Lighting (hvl, org_id=71)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | False | portal_order_count=0, portal_order_gmv=$0 |
| HAS_INVENTORY | True | inventory_count=5948 |
| HAS_SALES_DATA | True | sales_data_count=104574 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=0 engagement_reps=35 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Catalog-Focused |
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
| ENGAGEMENT_REP_COUNT | 35 | engagement_reps=35 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 91 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 1, Mixpanel total submit_order (Q-01): 7 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=96.7%, ambiguous_rate=6.8%, showroom_event_share=0.1% |
| USER_GROUP_JOIN_RATE | 97% | 88 of 91 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 0% | showroom+admin share of matched events: 0.1% |
| ADMIN_REPS_IN_LEADERBOARD | False | 0 admin/showroom users in leaderboard |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False |  |
| PORTAL_REP_DATA_PRESENT | False |  |
| PORTAL_CUSTOMER_DATA_PRESENT | False |  |
| INVENTORY_FRESH | False | inventories last_updated 313d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | False | customers last_updated 313d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=199 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | LIMITED | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | LIMITED | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | PARTIAL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Hudson Valley Lighting
- **Shortname**: hvl
- **Org ID**: 71
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- portal_orders LTM count=0, gmv=0.0 — HAS_PORTAL_ORDERS overridden to false

## Section Confidence

# Section Confidence Tiers — Hudson Valley Lighting (hvl, org_id=71)
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
| INVENTORY_FRESH | False |
| SALES_DATA_FRESH | False |
| CUSTOMER_DATA_FRESH | False |

## Computed Tiers

| Section | Tier | Determining Condition |
| --- | --- | --- |
| §2 Sales Team | STRONG | See Derived Gate 6 §2 formula |
| §3 Customer | LIMITED | See Derived Gate 6 §3 formula |
| §4 Product | LIMITED | See Derived Gate 6 §4 formula |
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

# Signal Rank — Hudson Valley Lighting (hvl, org_id=71)
- **Run date**: 2026-06-17
- **Total signals fired**: 23 (P0: 0, P1: 14, P2: 9)
- **Org GMV**: $0.0M eCat LTM, $0.0M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-OPP-04 | New Item Adoption Gap — 30 new items with $0 platform orders | P2 | §3 Product | 3.0 | $50,000 | 1.0 | 150,000 | POSITIVE |
| 2 | SIG-RISK-03 | Data Staleness — customers last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 3 | SIG-RISK-03 | Data Staleness — customer_favorites last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 4 | SIG-RISK-03 | Data Staleness — inventories last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 5 | SIG-RISK-03 | Data Staleness — placement_reports last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 6 | SIG-RISK-03 | Data Staleness — price_levels last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 7 | SIG-RISK-03 | Data Staleness — options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 8 | SIG-RISK-03 | Data Staleness — option_groups last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 9 | SIG-RISK-03 | Data Staleness — matrix_options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 10 | SIG-RISK-03 | Data Staleness — contract_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 11 | SIG-RISK-03 | Data Staleness — kit_items last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 12 | SIG-RISK-03 | Data Staleness — commitment_reports last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 13 | SIG-RISK-03 | Data Staleness — riser_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 14 | SIG-RISK-03 | Data Staleness — customer_payment_informations last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 15 | SIG-RISK-03 | Data Staleness — sales_quotas last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 16 | SIG-RISK-03 | Data Staleness — products last updated 153d ago | P2 | §6 Platform | 1.7 | $1 | 2.0 | 3 | RISK |
| 17 | SIG-RISK-03 | Data Staleness — smart_stacks last updated 153d ago | P2 | §6 Platform | 1.7 | $1 | 2.0 | 3 | RISK |
| 18 | SIG-RISK-03 | Data Staleness — categories last updated 153d ago | P2 | §6 Platform | 1.7 | $1 | 2.0 | 3 | RISK |
| 19 | SIG-RISK-03 | Data Staleness — collections last updated 153d ago | P2 | §6 Platform | 1.7 | $1 | 2.0 | 3 | RISK |
| 20 | SIG-RISK-03 | Data Staleness — groups last updated 153d ago | P2 | §6 Platform | 1.7 | $1 | 2.0 | 3 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §3 Product Intelligence | 0 | 0 | 1 | 1 | |
| §6 Platform Context | 0 | 14 | 8 | 22 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-04: New Item Adoption Gap — 30 new items with $0 platform orders
2. **[RISK]** SIG-RISK-03: Data Staleness — customers last updated 313d ago
3. **[RISK]** SIG-RISK-03: Data Staleness — customer_favorites last updated 313d ago
4. **[RISK]** SIG-RISK-03: Data Staleness — inventories last updated 313d ago
5. **[RISK]** SIG-RISK-03: Data Staleness — placement_reports last updated 313d ago
6. **[RISK]** SIG-RISK-03: Data Staleness — price_levels last updated 313d ago
7. **[RISK]** SIG-RISK-03: Data Staleness — options last updated 313d ago

**Balance check**: 1 positive (slots 1-1), 6 risk (slots 2-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-08_results.md

# Q-08 Results — Hudson Valley Lighting (hvl, org_id=71)
- **Query**: Q-08 — Data Freshness Monitor
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 22
- **Run date**: 2026-06-17


| entity_type | last_updated | days_since_update | status |
| --- | --- | --- | --- |
| customers | 2025-08-07 23:13:01 | 313 | Stale |
| customer_favorites | 2025-08-07 23:13:01 | 313 | Stale |
| inventories | 2025-08-07 23:13:01 | 313 | Stale |
| placement_reports | 2025-08-07 23:13:01 | 313 | Stale |
| price_levels | 2025-08-07 23:13:01 | 313 | Stale |
| options | 2025-08-07 23:13:01 | 313 | Stale |
| option_groups | 2025-08-07 23:13:01 | 313 | Stale |
| matrix_options | 2025-08-07 23:13:01 | 313 | Stale |
| contract_prices | 2025-08-07 23:13:01 | 313 | Stale |
| kit_items | 2025-08-07 23:13:01 | 313 | Stale |
| commitment_reports | 2025-08-07 23:13:01 | 313 | Stale |
| riser_prices | 2025-08-07 23:13:01 | 313 | Stale |
| customer_payment_informations | 2025-08-07 23:13:01 | 313 | Stale |
| sales_quotas | 2025-08-07 23:13:01 | 313 | Stale |
| products | 2026-01-14 21:54:55 | 153 | Monitor |
| smart_stacks | 2026-01-14 21:54:55 | 153 | Monitor |
| categories | 2026-01-14 21:55:06 | 153 | Monitor |
| collections | 2026-01-14 21:55:06 | 153 | Monitor |
| groups | 2026-01-14 21:55:06 | 153 | Monitor |
| trade_names | 2026-01-14 21:55:06 | 153 | Monitor |
| portal_orders | 2026-03-13 14:23:30 | 96 | Monitor |
| portal_invoices | 2026-03-13 14:23:30 | 96 | Monitor |

### Q-09_results.md

# Q-09 Results — Hudson Valley Lighting (hvl, org_id=71)
- **Query**: Q-09 — Import Health — Monthly Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| month | import_count |
| --- | --- |
| 2026-01-01 | 7 |

### Q-09_recent_results.md

# Q-09-recent Results — Hudson Valley Lighting (hvl, org_id=71)
- **Query**: Q-09-recent — Import Health — Recent Errors
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| created_at | data |
| --- | --- |
| 2026-01-15T17:52:39.357735 | ---
- - Images
  - []
 |
| 2026-01-15T17:49:37.756543 | ---
- - Images
  - []
 |
| 2026-01-15T17:42:23.885263 | ---
- - Images
  - - - :information
      - 'The following images were imported: H1080701-AGB_400.jpg, 567-36-VB_400.jpg,
        F3638-FOR_400.jpg, HL1138201-AGB_400.jpg, HL1157201-AGB_CFK_400.jpg, 568-01-VB_400.jpg,
        B4011-FOR_PBR_400.jpg, F4320-PBR_400.jpg, F1640-PBR_400.jpg, L2951-AGB_CTR_400.jpg,
        B2326-PBR_400.jpg, 577-02-VB_400.jpg, B4623-PBR_400.jpg, L2251-AGB_400.jpg,
        H1084701L-AGB_400.jpg, B8604-TBK_400.jpg, C4118-PBR_400.jpg, F1630-BRZ_400.jpg,
        B8602-TBK_400.jpg, C7216-PBR_GSL_400.jpg, 1374-AGB_400.jpg, H1098102-AGB_400.jpg,
        1613-PBR_400.jpg, 567-24-VB_400.jpg, F3852-PGL_400.jpg, PFL2064-PBR_400.jpg,
        B7517-PBR_400.jpg, F7536-PBR_400.jpg, 565-48-VB_400.jpg, 578-31-VB_400.jpg
        and 46 more images'
 |
| 2026-01-15T17:38:21.986604 | ---
- - Images
  - - - :information
      - 'The following images were imported: H1107302-AGB_400.jpg, H1128101-VGL_400.jpg,
        RTL8621-TBK_400.jpg, HL1112201-AGB_CYM_400.jpg, PTL3124-PBR_CSE_400.jpg, H1091701L-AGB_400.jpg,
        L3029-AGB_400.jpg, 1372-AGB_400.jpg, C6222-BRL_400.jpg, H1107301-PN_400.jpg,
        B2828-BRL_400.jpg, F2141-PBR_SSD_400.jpg, H1094803-AGB_400.jpg, H1111102-VGL_400.jpg,
        H1098101-AGB_400.jpg, F4810-PBR_400.jpg, C7212-PBR_GCR_400.jpg, L4321-AGB_400.jpg,
        B4617-PBR_400.jpg, H1132704-AGB_SAO_400.jpg, B5716-TBK_PBR_400.jpg, H1106101-AGB_400.jpg,
        L3371-AGB_CHJ_400.jpg, C4418-VGL_400.jpg, HL1115201-AGB_CHD_400.jpg, P7115-TBK_400.jpg,
        F3460-VGL_400.jpg, HL1158201-AGB_CBV_400.jpg, F6732-VGL_400.jpg, PFL8674-TBK_400.jpg
        and 116 more images'
 |
| 2026-01-14T21:56:09.614903 | ---
- - Products
  - - - :information
      - 'The following items were missing category codes and asssigned to ''Other''
        category: HVLG INTL-HANDWARMERS, HVLG INTL-TOTEBAGS, HVR-013-BB-TR, HVR-013-OB-TR,
        HVR-019-2-BB-220V, 40-04426-10592, 40-65677-42026, 18-00624-17898, 18-05539-98316,
        18-14657-60662, 18-26845-00406, 18-37071-58434, 18-38887-93302, 18-41277-27538,
        18-60261-61025, 18-60910-35701, 18-61343-37154, 18-65994-49766, 18-67574-44633,
        18-69183-35189 and 204 more products'
 |
| 2026-01-14T21:43:28.660024 | ---
- - Products
  - - - :warning
      - 'Error running cleancsv: 2026/01/14 21:42:20 EOF

        '
    - - :warning
      - "Line 1: Field name PK\x03\x04\x14\0\x06\0\b\0\0\0!\0bî is unknown."
    - - :fatal
      - 'Line 1: BaseItemCode field is missing'
    - - :fatal
      - 'Line 1: Column tradenamecode is missing and is required since your import
        method is Auto-Create.'
    - - :fatal
      - 'Line 1: Column collectioncodes is missing and is required since your import
        method is Auto-Create.'
 |
| 2026-01-14T21:16:32.089127 | ---
- - Products
  - - - :warning
      - 'Error running cleancsv: 2026/01/14 21:15:05 EOF

        '
    - - :warning
      - "Line 1: Field name PK\x03\x04\x14\0\x06\0\b\0\0\0!\0bî is unknown."
    - - :fatal
      - 'Line 1: BaseItemCode field is missing'
    - - :fatal
      - 'Line 1: Column tradenamecode is missing and is required since your import
        method is Auto-Create.'
    - - :fatal
      - 'Line 1: Column collectioncodes is missing and is required since your import
        method is Auto-Create.'
 |
| 2025-10-21T15:11:00.946324 | ---
- - Images
  - - - :information
      - 'The following images were imported: 7330-AGB_DB_400.jpg, 8923-AGB_400.jpg,
        552-24-VGL_400.jpg, 551-02-VB_400.jpg, 537-56-VPB_400.jpg, L3633-AGB_CRG_400.jpg,
        AH6308-AGB_400.jpg, 9309-DB_400.jpg, L2231-AGB_400.jpg, F3324-PBR_400.jpg,
        557-06-VB_400.jpg, AH5017-AGB_400.jpg, F5119-BRZ_400.jpg, 4831-AGB_400.jpg,
        PTL1729-PBR_CTU_400.jpg, 1963-WP_400.jpg'
 |
| 2025-10-21T15:06:19.672824 | ---
- - Images
  - - - :information
      - 'The following images were imported: 549-02-VB_400.jpg, 561-28-WSL_400.jpg,
        1823-CP_400.jpg, 520-19-VB_400.jpg, 533-40-VGL_400.jpg, 520-14-VB_400.jpg,
        5715-AGB_400.jpg, L6466-AGB_400.jpg, 5151-AGB_400.jpg, 1819-CP_400.jpg, 1813-VGL_400.jpg,
        557-02-VB_400.jpg, 1552-PGL_400.jpg, 545-13-VPB_400.jpg, AHL4519-PN_400.jpg,
        2862-VGL_400.jpg, 5817-HB_400.jpg, 544-04-VB_400.jpg, 536-32-VPB_400.jpg,
        9315-DB_400.jpg, 556-01-VB_400.jpg, 7324-AGB_400.jpg, 8922-AGB_400.jpg, F1960-PBR_400.jpg,
        AHL6403-BI_400.jpg, 5621-AGB_400.jpg, 543-54-VGL_400.jpg, 558-10-VB_400.jpg,
        3124-VGL_400.jpg, 9217-AGB_400.jpg and 36 more images'
 |
| 2025-10-21T15:01:06.961567 | ---
- - Images
  - - - :information
      - 'The following images were imported: L8329-BRZ_400.jpg, 557-18-VB_400.jpg,
        554-01-WSL_400.jpg, 1848-CP_400.jpg, 1836-VGL_400.jpg, 534-24-VGL_400.jpg,
        L9864-AGB_400.jpg, 2932-VGL_400.jpg, 9542-VGL_400.jpg, 554-01-VGL_400.jpg,
        5361-AGB_400.jpg, F1638-PBR_400.jpg, 522-59-TWL_400.jpg, L1434-AGB_CTE_400.jpg,
        8934-AGB_400.jpg, L1128-AGB_400.jpg, 559-36-OWB_400.jpg, L6351-HB_400.jpg,
        3041-AGB_DB_400.jpg, L1205-AGB_400.jpg, PTL1320-PBR_400.jpg, PTL1527-PBR_400.jpg,
        2016-AGB_400.jpg, 1339-VGL_400.jpg, 1630-AGB_400.jpg, AH6317-AGB_400.jpg,
        522-43-TWL_400.jpg, 1848-VGL_400.jpg, 2013-AGB_400.jpg, AH4640-AGB_400.jpg
        and 38 more images'
 |

### Q-10_results.md

# Q-10 Results — Hudson Valley Lighting (hvl, org_id=71)
- **Query**: Q-10 — Feature Enablement Gap Analysis
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-11_results.md

# Q-11 Results — Hudson Valley Lighting (hvl, org_id=71)
- **Query**: Q-11 — Configuration Completeness
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 22
- **Run date**: 2026-06-17


| entity_type | last_updated | days_stale | related_record_count |
| --- | --- | --- | --- |
| customers | 2025-08-07 23:13:01 | 313 | — |
| customer_favorites | 2025-08-07 23:13:01 | 313 | — |
| inventories | 2025-08-07 23:13:01 | 313 | — |
| placement_reports | 2025-08-07 23:13:01 | 313 | — |
| price_levels | 2025-08-07 23:13:01 | 313 | — |
| options | 2025-08-07 23:13:01 | 313 | — |
| option_groups | 2025-08-07 23:13:01 | 313 | — |
| matrix_options | 2025-08-07 23:13:01 | 313 | — |
| contract_prices | 2025-08-07 23:13:01 | 313 | 0 |
| kit_items | 2025-08-07 23:13:01 | 313 | 0 |
| commitment_reports | 2025-08-07 23:13:01 | 313 | — |
| riser_prices | 2025-08-07 23:13:01 | 313 | — |
| customer_payment_informations | 2025-08-07 23:13:01 | 313 | — |
| sales_quotas | 2025-08-07 23:13:01 | 313 | 0 |
| products | 2026-01-14 21:54:55 | 153 | — |
| smart_stacks | 2026-01-14 21:54:55 | 153 | — |
| categories | 2026-01-14 21:55:06 | 153 | — |
| collections | 2026-01-14 21:55:06 | 153 | — |
| groups | 2026-01-14 21:55:06 | 153 | — |
| trade_names | 2026-01-14 21:55:06 | 153 | — |
| portal_orders | 2026-03-13 14:23:30 | 96 | — |
| portal_invoices | 2026-03-13 14:23:30 | 96 | — |

### Q-22_results.md

# Q-22 Results — Hudson Valley Lighting (hvl, org_id=71)
- **Query**: Q-22 — Feature Usage Depth
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | submit_order | select_a_customer | search_for_customer | email_item_info | create_pdf_catalog | view_library_entry | view_smartpicks | access_sales_portal | filter_products | search_products | search_collections | order_configured_item | view_kit | order_kit | share_my_list | export_data_to_csv | export_data_to_excel | total_events | total_users |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hvl | Hudson Valley Lighting | 7 | 1,156 | 1,585 | 56 | 216 | 107 | 8 | 71 | 259 | 7,292 | 526 | 0 | 0 | 0 | 6 | 0 | 0 | 18,678 | 91 |

### Q-CI-02_results.md

# Q-CI-02 Results — Hudson Valley Lighting (hvl, org_id=71)
- **Query**: Q-CI-02 — Peer Comparison
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | peer_standing | orders_vs_peer_pct | logins_vs_peer_pct | mrr_vs_peer_pct | peer_orders_median | peer_logins_median | peer_mrr_median |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hvl | Hudson Valley Lighting | Catalog-Focused | Needs Attention | — | 785.60 | -100 | 0 | 278 | 725 |

### Q-CI-03_results.md

# Q-CI-03 Results — Hudson Valley Lighting (hvl, org_id=71)
- **Query**: Q-CI-03 — Feature Adoption Benchmarking
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | feature_depth | has_clicky_portal | arr |
| --- | --- | --- | --- | --- | --- |
| hvl | Hudson Valley Lighting | Catalog-Focused | 5 | 0 | — |

### Q-CI-03_benchmarks_results.md

# Q-CI-03-bench Results — Hudson Valley Lighting (hvl, org_id=71)
- **Query**: Q-CI-03-bench — Segment Benchmarks Monthly
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 3
- **Run date**: 2026-06-17


| segment | benchmark_month | org_count | submit_order_p10 | submit_order_p25 | submit_order_median | submit_order_p75 | submit_order_p90 | total_logins_p25 | total_logins_median | total_logins_p75 | search_products_p25 | search_products_median | search_products_p75 | mrr_p25 | mrr_median | mrr_p75 | arr_p25 | arr_median | arr_p75 | feature_kit_items_pct | feature_portal_orders_pct | feature_sales_portal_pct | feature_library_pct | feature_pdf_catalog_pct | feature_cpq_pct | created_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Catalog-Focused | 2026-06-01 | 93 | 0 | 0 | 0 | 2 | 12 | 10 | 278 | 1,487 | 0 | 280 | 3,178 | 0 | 725 | 920 | 0 | 1,450 | 8,700 | 0.11 | 0.31 | 0.31 | 0.70 | 0.55 | 0.20 | 2026-06-01 10:00 |
| Catalog-Focused | 2026-05-01 | 93 | 0 | 0 | 0 | 1 | 12 | 9 | 278 | 1,456 | 0 | 280 | 3,141 | 0 | 725 | 920 | 0 | 1,450 | 8,700 | 0.11 | 0.30 | 0.30 | 0.70 | 0.55 | 0.20 | 2026-05-01 10:00 |
| Catalog-Focused | 2026-04-01 | 93 | 0 | 0 | 0 | 1 | 12 | 9 | 271 | 1,315 | 0 | 254 | 2,929 | 0 | 725 | 920 | 0 | 1,450 | 8,700 | 0.11 | 0.30 | 0.30 | 0.70 | 0.55 | 0.19 | 2026-04-01 10:00 |

### Q-CI-05_results.md

(not present — file does not exist or is empty)

### peer_benchmark_extract.md

(not present — file does not exist or is empty)
