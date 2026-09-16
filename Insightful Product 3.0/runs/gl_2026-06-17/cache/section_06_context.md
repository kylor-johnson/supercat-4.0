# Section 6 Context Bundle — Golden Lighting (gl)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Golden Lighting (gl, org_id=187)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | True | recurring_services contains B2B Cart: True |
| HAS_PORTAL_ORDERS | True | portal_order_count=6096, portal_order_gmv=$2.6M |
| HAS_INVENTORY | True | inventory_count=3058 |
| HAS_SALES_DATA | True | sales_data_count=36842 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=1 engagement_reps=28 (threshold: >=5) |
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
| VM45_GATE_1 | PASS | erp_gmv=$2.6M > ecat_gmv=$131,176: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 1 | 1 |
| ENGAGEMENT_REP_COUNT | 28 | engagement_reps=28 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 51 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 240, Mixpanel total submit_order (Q-01): 59 |
| USER_GROUP_SPLIT_AVAILABLE | True | join_rate=98.0%, ambiguous_rate=0.0%, showroom_event_share=13.9% |
| USER_GROUP_JOIN_RATE | 98% | 50 of 51 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 14% | showroom+admin share of matched events: 13.9% |
| ADMIN_REPS_IN_LEADERBOARD | True | 2 admin/showroom users in leaderboard: Sholeh Duncan, Sholeh Duncan |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=2 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=905 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=856 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Golden Lighting
- **Shortname**: gl
- **Org ID**: 187
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Golden Lighting (gl, org_id=187)
- **Run date**: 2026-06-17

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | False |
| PORTAL_CUSTOMER_DATA_PRESENT | True |
| PORTAL_ORDERS_FRESH | True |
| HAS_PORTAL_ORDERS | True |
| HAS_INVENTORY | True |
| HAS_SALES_DATA | True |
| INVENTORY_FRESH | True |
| SALES_DATA_FRESH | False |
| CUSTOMER_DATA_FRESH | True |

## Computed Tiers

| Section | Tier | Determining Condition |
| --- | --- | --- |
| §2 Sales Team | STRONG | See Derived Gate 6 §2 formula |
| §3 Customer | FULL | See Derived Gate 6 §3 formula |
| §4 Product | STRONG | See Derived Gate 6 §4 formula |
| §5 Commerce | FULL | See Derived Gate 6 §5 formula |

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

# Signal Rank — Golden Lighting (gl, org_id=187)
- **Run date**: 2026-06-17
- **Total signals fired**: 35 (P0: 20, P1: 10, P2: 5)
- **Org GMV**: $0.1M eCat LTM, $2.6M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-ANOMALY-02 | Stock Out — 9903-24 MG (Ziva by Golden Lighting Autumn Twilight ) $79,468 LTM, 0 available | P0 | §3 Product | 10.0 | $79,468 | 3.0 | 2,384,038 | RISK |
| 2 | SIG-ANOMALY-02 | Stock Out — 3118-L BLK-SD (Yep by Golden Lighting Hines 1-light 14i) $74,996 LTM, 0 available | P0 | §3 Product | 10.0 | $74,996 | 3.0 | 2,249,878 | RISK |
| 3 | SIG-ANOMALY-02 | Stock Out — 9903-12 MG (Ziva by Golden Lighting Autumn Twilight ) $67,163 LTM, 0 available | P0 | §3 Product | 10.0 | $67,163 | 3.0 | 2,014,876 | RISK |
| 4 | SIG-ANOMALY-02 | Stock Out — 7312-L BP (Golden Lighting Bartlett 2-light Pendant) $58,825 LTM, 0 available | P0 | §3 Product | 10.0 | $58,825 | 3.0 | 1,764,763 | RISK |
| 5 | SIG-ANOMALY-02 | Stock Out — 6805-6 BLK-NR (Golden Lighting Everly 6-light Chandelie) $42,401 LTM, 0 available | P0 | §3 Product | 10.0 | $42,401 | 3.0 | 1,272,043 | RISK |
| 6 | SIG-ANOMALY-02 | Stock Out — 9903-6 MG (Ziva by Golden Lighting Autumn Twilight ) $41,930 LTM, 0 available | P0 | §3 Product | 10.0 | $41,930 | 3.0 | 1,257,908 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 6937-M BLK-NR (Golden Lighting Valentina 1-light Pendan) $41,561 LTM, 0 available | P0 | §3 Product | 10.0 | $41,561 | 3.0 | 1,246,826 | RISK |
| 8 | SIG-ANOMALY-02 | Stock Out — 1270-13 BLK (Wry Lighting Morgon 2-light 13" Flush Mo) $41,544 LTM, 0 available | P0 | §3 Product | 10.0 | $41,544 | 3.0 | 1,246,329 | RISK |
| 9 | SIG-ANOMALY-02 | Stock Out — 6950-L MBS (Golden Lighting Shepard 1-light Pendant ) $34,834 LTM, 0 available | P0 | §3 Product | 10.0 | $34,834 | 3.0 | 1,045,015 | RISK |
| 10 | SIG-ANOMALY-02 | Stock Out — 7312-L CP (Golden Lighting Bartlett 2-light Pendant) $32,869 LTM, 0 available | P0 | §3 Product | 10.0 | $32,869 | 3.0 | 986,058 | RISK |
| 11 | SIG-ANOMALY-02 | Stock Out — 6070-LP BLK-BLK (Golden Lighting Tribeca 5-light Island L) $32,606 LTM, 0 available | P0 | §3 Product | 10.0 | $32,606 | 3.0 | 978,173 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — 1017-69 BLK (Golden Lighting Alastair 15-light 2-tier) $28,315 LTM, 0 available | P0 | §3 Product | 10.0 | $28,315 | 3.0 | 849,450 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — 1017-96 BLK (Golden Lighting Alastair 15-light 2-tier) $28,248 LTM, 0 available | P0 | §3 Product | 10.0 | $28,248 | 3.0 | 847,438 | RISK |
| 14 | SIG-ANOMALY-02 | Stock Out — 3118-L PW-SD (Yep by Golden Lighting Hines 1-light 14i) $27,819 LTM, 0 available | P0 | §3 Product | 10.0 | $27,819 | 3.0 | 834,563 | RISK |
| 15 | SIG-ANOMALY-02 | Stock Out — 8001-BA3 BLK-SD (Golden Lighting Parrish 3-light Vanity i) $25,628 LTM, 0 available | P0 | §3 Product | 10.0 | $25,628 | 3.0 | 768,844 | RISK |
| 16 | SIG-ANOMALY-02 | Stock Out — 3118-L RBZ-SD (Yep by Golden Lighting Hines 1-light 14i) $25,317 LTM, 0 available | P0 | §3 Product | 10.0 | $25,317 | 3.0 | 759,502 | RISK |
| 17 | SIG-OPP-01 | Next Best Product — 3164-FM BCB-HWG/3164-FM BLK-HWG co-purchase pattern across 10 customers | P0 | §2/§3 | 1.0 | $293,278 | 2.0 | 586,555 | POSITIVE |
| 18 | SIG-COMMERCE-01 | Capture Rate — eCat captures 5.0% of $3M total business; each +1pt = $26K | P0 | §4 Commerce | 4.7 | $26,000 | 3.0 | 370,324 | POSITIVE |
| 19 | SIG-MOM-01 | Account Acceleration — THE LIGHTING DESIGN CO. 2 consecutive QoQ acceleration quarters, $11,875 peak quarter (+191% QoQ) | P0 | §2 Accounts | 6.4 | $11,875 | 3.0 | 226,694 | POSITIVE |
| 20 | SIG-OPP-04 | New Item Adoption Gap — 30 new items with $0 platform orders | P2 | §3 Product | 3.0 | $50,000 | 1.0 | 150,000 | POSITIVE |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 3 | 0 | 0 | 3 | |
| §3 Product Intelligence | 16 | 0 | 1 | 17 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §6 Platform Context | 0 | 9 | 4 | 13 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — 3164-FM BCB-HWG/3164-FM BLK-HWG co-purchase pattern across 10 customers
2. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 5.0% of $3M total business; each +1pt = $26K
3. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — THE LIGHTING DESIGN CO. 2 consecutive QoQ acceleration quarters, $11,875 peak quarter (+191% QoQ)
4. **[POSITIVE/MOMENTUM]** SIG-OPP-04: New Item Adoption Gap — 30 new items with $0 platform orders
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 9903-24 MG (Ziva by Golden Lighting Autumn Twilight ) $79,468 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — 3118-L BLK-SD (Yep by Golden Lighting Hines 1-light 14i) $74,996 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 9903-12 MG (Ziva by Golden Lighting Autumn Twilight ) $67,163 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-08_results.md

# Q-08 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-08 — Data Freshness Monitor
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 22
- **Run date**: 2026-06-17


| entity_type | last_updated | days_since_update | status |
| --- | --- | --- | --- |
| sales_quotas | 2025-08-20 19:47:15 | 300 | Stale |
| customer_payment_informations | 2025-08-20 19:47:15 | 300 | Stale |
| riser_prices | 2025-08-20 19:47:15 | 300 | Stale |
| placement_reports | 2025-08-20 19:47:15 | 300 | Stale |
| commitment_reports | 2025-08-20 19:47:15 | 300 | Stale |
| kit_items | 2025-08-20 19:47:15 | 300 | Stale |
| contract_prices | 2025-08-20 19:47:15 | 300 | Stale |
| customer_favorites | 2025-08-20 19:47:15 | 300 | Stale |
| price_levels | 2025-11-03 15:37:26 | 225 | Stale |
| categories | 2026-01-26 21:45:32 | 141 | Monitor |
| groups | 2026-01-26 21:45:32 | 141 | Monitor |
| collections | 2026-03-16 12:02:20 | 92 | Monitor |
| trade_names | 2026-03-16 12:02:20 | 92 | Monitor |
| matrix_options | 2026-05-26 16:13:36 | 21 | Fresh |
| options | 2026-05-28 19:35:08 | 19 | Fresh |
| option_groups | 2026-05-28 19:35:08 | 19 | Fresh |
| products | 2026-06-15 13:40:50 | 1 | Fresh |
| portal_orders | 2026-06-16 10:01:15 | 0 | Fresh |
| customers | 2026-06-16 19:46:34 | 0 | Fresh |
| smart_stacks | 2026-06-16 20:00:45 | 0 | Fresh |
| inventories | 2026-06-16 21:02:06 | 0 | Fresh |
| portal_invoices | 2026-06-16 22:02:13 | 0 | Fresh |

### Q-09_results.md

# Q-09 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-09 — Import Health — Monthly Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 7
- **Run date**: 2026-06-17


| month | import_count |
| --- | --- |
| 2026-06-01 | 115 |
| 2026-05-01 | 279 |
| 2026-04-01 | 219 |
| 2026-03-01 | 221 |
| 2026-02-01 | 40 |
| 2026-01-01 | 240 |
| 2025-12-01 | 121 |

### Q-09_recent_results.md

# Q-09-recent Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-09-recent — Import Health — Recent Errors
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| created_at | data |
| --- | --- |
| 2026-06-17 05:03:19 | ---
- - Product Stories
  - - - :warning
      - 'Line 3: Product not found, record ignored, BaseItemCode=0304-BA3 BLK'
    - - :warning
      - 'Line 19: Product not found, record ignored, BaseItemCode=0305-BA3 CH-CLR'
    - - :warning
      - 'Line 84: Product not found, record ignored, BaseItemCode=0511-FM BLK-CLR'
    - - :warning
      - 'Line 248: Product not found, record ignored, BaseItemCode=1048-6 GMT'
    - - :warning
      - 'Line 273: Product not found, record ignored, BaseItemCode=1081-SF BLK-PSG'
    - - :warning
      - 'Line 315: Product not found, record ignored, BaseItemCode=1096-M BLK-SD'
    - - :warning
      - 'Line 338: Product not found, record ignored, BaseItemCode=1208-6 DNI'
    - - :warning
      - 'Line 339: Product not found, record ignored, BaseItemCode=1208-9 DNI'
    - - :warning
      - 'Line 353: Product not found, record ignored, BaseItemCode=1405-1W RBZ-AG'
    - - :warning
      - 'Line 425: Product not found, record ignored, BaseItemCode=2073-4 GMT'
    - - :warning
      - 'Line 720: Product not found, record ignored, BaseItemCode=3167-6 BLK-BLK'
    - - :warning
      - 'Line 732: Product not found, record ignored, BaseItemCode=3167-9 PW-PW'
    - - :warning
      - 'Line 738: Product not found, record ignored, BaseItemCode=3167-LP PW'
    - - :warning
      - 'Line 749: Product not found, record ignored, BaseItemCode=3171-FM24 BLK-CW'
    - - :warning
      - 'Line 770: Product not found, record ignored, BaseItemCode=3219-SF AB-AB'
    - - :warning
      - 'Line 1450: Product not found, record ignored, BaseItemCode=3417-SF PW-CC'
    - - :warning
      - 'Line 1493: Product not found, record ignored, BaseItemCode=3602-14 CH-GY'
    - - :warning
      - 'Line 2029: Product not found, record ignored, BaseItemCode=3604-L PW-RD'
    - - :warning
      - 'Line 2201: Product not found, record ignored, BaseItemCode=4309-FM BLK-SD'
    - - :warning
      - 'Line 2240: Product not found, record ignored, BaseItemCode=4855-FM PW-CLR'
    - - :warning
      - 'Line 2636: Product not found, record ignored, BaseItemCode=7866-SF VDW'
    - - :warning
      - 'Line 2688: Product not found, record ignored, BaseItemCode=8606-D5 BLK-CLR'
    - - :warning
      - 'Line 2710: Product not found, record ignored, BaseItemCode=9130-FM17 BLK-OP'
    - - :warning
      - 'Line 2751: Product not found, record ignored, BaseItemCode=DDDD-BA1'
    - - :warning
      - 'Line 2755: Product not found, record ignored, BaseItemCode=DDDD-BA3'
 |
| 2026-06-16 22:02:13 | ---
- - Portal Invoices
  - []
 |
| 2026-06-16 21:02:06 | ---
- - Inventory
  - - - :warning
      - 'Line 3: Product not found, record ignored., BaseItemCode=0304-BA3 BLK'
    - - :warning
      - 'Line 256: Product not found, record ignored., BaseItemCode=1048-6 GMT'
    - - :warning
      - 'Line 318: Product not found, record ignored., BaseItemCode=1096-M BLK-SD'
    - - :warning
      - 'Line 344: Product not found, record ignored., BaseItemCode=1208-6 DNI'
    - - :warning
      - 'Line 345: Product not found, record ignored., BaseItemCode=1208-9 DNI'
    - - :warning
      - 'Line 916: Product not found, record ignored., BaseItemCode=3167-6 BLK-BLK'
    - - :warning
      - 'Line 926: Product not found, record ignored., BaseItemCode=3167-9 PW-PW'
    - - :warning
      - 'Line 931: Product not found, record ignored., BaseItemCode=3167-LP PW'
    - - :warning
      - 'Line 959: Product not found, record ignored., BaseItemCode=3219-SF AB-AB'
    - - :warning
      - 'Line 3050: Product not found, record ignored., BaseItemCode=DDDD-BA1'
    - - :warning
      - 'Line 3054: Product not found, record ignored., BaseItemCode=DDDD-BA3'
 |
| 2026-06-16 19:46:34 | ---
- - Customers
  - - - :error
      - 'Line 2269: error=Validation failed: Code is too long (maximum is 20 characters):
        Customer # = mseasholtz@fromm.cpm060050'
 |
| 2026-06-16 16:01:20 | ---
- - Inventory
  - - - :warning
      - 'Line 3: Product not found, record ignored., BaseItemCode=0304-BA3 BLK'
    - - :warning
      - 'Line 256: Product not found, record ignored., BaseItemCode=1048-6 GMT'
    - - :warning
      - 'Line 318: Product not found, record ignored., BaseItemCode=1096-M BLK-SD'
    - - :warning
      - 'Line 344: Product not found, record ignored., BaseItemCode=1208-6 DNI'
    - - :warning
      - 'Line 345: Product not found, record ignored., BaseItemCode=1208-9 DNI'
    - - :warning
      - 'Line 916: Product not found, record ignored., BaseItemCode=3167-6 BLK-BLK'
    - - :warning
      - 'Line 926: Product not found, record ignored., BaseItemCode=3167-9 PW-PW'
    - - :warning
      - 'Line 931: Product not found, record ignored., BaseItemCode=3167-LP PW'
    - - :warning
      - 'Line 959: Product not found, record ignored., BaseItemCode=3219-SF AB-AB'
    - - :warning
      - 'Line 3050: Product not found, record ignored., BaseItemCode=DDDD-BA1'
    - - :warning
      - 'Line 3054: Product not found, record ignored., BaseItemCode=DDDD-BA3'
 |
| 2026-06-16 10:01:15 | ---
- - Portal Orders
  - []
 |
| 2026-06-16 09:02:20 | ---
- - Inventory
  - - - :warning
      - 'Line 3: Product not found, record ignored., BaseItemCode=0304-BA3 BLK'
    - - :warning
      - 'Line 256: Product not found, record ignored., BaseItemCode=1048-6 GMT'
    - - :warning
      - 'Line 318: Product not found, record ignored., BaseItemCode=1096-M BLK-SD'
    - - :warning
      - 'Line 344: Product not found, record ignored., BaseItemCode=1208-6 DNI'
    - - :warning
      - 'Line 345: Product not found, record ignored., BaseItemCode=1208-9 DNI'
    - - :warning
      - 'Line 916: Product not found, record ignored., BaseItemCode=3167-6 BLK-BLK'
    - - :warning
      - 'Line 926: Product not found, record ignored., BaseItemCode=3167-9 PW-PW'
    - - :warning
      - 'Line 931: Product not found, record ignored., BaseItemCode=3167-LP PW'
    - - :warning
      - 'Line 959: Product not found, record ignored., BaseItemCode=3219-SF AB-AB'
    - - :warning
      - 'Line 3050: Product not found, record ignored., BaseItemCode=DDDD-BA1'
    - - :warning
      - 'Line 3054: Product not found, record ignored., BaseItemCode=DDDD-BA3'
 |
| 2026-06-16 05:01:18 | ---
- - Product Stories
  - - - :warning
      - 'Line 3: Product not found, record ignored, BaseItemCode=0304-BA3 BLK'
    - - :warning
      - 'Line 19: Product not found, record ignored, BaseItemCode=0305-BA3 CH-CLR'
    - - :warning
      - 'Line 84: Product not found, record ignored, BaseItemCode=0511-FM BLK-CLR'
    - - :warning
      - 'Line 248: Product not found, record ignored, BaseItemCode=1048-6 GMT'
    - - :warning
      - 'Line 273: Product not found, record ignored, BaseItemCode=1081-SF BLK-PSG'
    - - :warning
      - 'Line 315: Product not found, record ignored, BaseItemCode=1096-M BLK-SD'
    - - :warning
      - 'Line 338: Product not found, record ignored, BaseItemCode=1208-6 DNI'
    - - :warning
      - 'Line 339: Product not found, record ignored, BaseItemCode=1208-9 DNI'
    - - :warning
      - 'Line 353: Product not found, record ignored, BaseItemCode=1405-1W RBZ-AG'
    - - :warning
      - 'Line 425: Product not found, record ignored, BaseItemCode=2073-4 GMT'
    - - :warning
      - 'Line 720: Product not found, record ignored, BaseItemCode=3167-6 BLK-BLK'
    - - :warning
      - 'Line 732: Product not found, record ignored, BaseItemCode=3167-9 PW-PW'
    - - :warning
      - 'Line 738: Product not found, record ignored, BaseItemCode=3167-LP PW'
    - - :warning
      - 'Line 749: Product not found, record ignored, BaseItemCode=3171-FM24 BLK-CW'
    - - :warning
      - 'Line 770: Product not found, record ignored, BaseItemCode=3219-SF AB-AB'
    - - :warning
      - 'Line 1450: Product not found, record ignored, BaseItemCode=3417-SF PW-CC'
    - - :warning
      - 'Line 1493: Product not found, record ignored, BaseItemCode=3602-14 CH-GY'
    - - :warning
      - 'Line 2029: Product not found, record ignored, BaseItemCode=3604-L PW-RD'
    - - :warning
      - 'Line 2201: Product not found, record ignored, BaseItemCode=4309-FM BLK-SD'
    - - :warning
      - 'Line 2240: Product not found, record ignored, BaseItemCode=4855-FM PW-CLR'
    - - :warning
      - 'Line 2636: Product not found, record ignored, BaseItemCode=7866-SF VDW'
    - - :warning
      - 'Line 2688: Product not found, record ignored, BaseItemCode=8606-D5 BLK-CLR'
    - - :warning
      - 'Line 2710: Product not found, record ignored, BaseItemCode=9130-FM17 BLK-OP'
    - - :warning
      - 'Line 2751: Product not found, record ignored, BaseItemCode=DDDD-BA1'
    - - :warning
      - 'Line 2755: Product not found, record ignored, BaseItemCode=DDDD-BA3'
 |
| 2026-06-15 22:02:14 | ---
- - Portal Invoices
  - []
 |
| 2026-06-15 21:01:38 | ---
- - Inventory
  - - - :warning
      - 'Line 3: Product not found, record ignored., BaseItemCode=0304-BA3 BLK'
    - - :warning
      - 'Line 256: Product not found, record ignored., BaseItemCode=1048-6 GMT'
    - - :warning
      - 'Line 318: Product not found, record ignored., BaseItemCode=1096-M BLK-SD'
    - - :warning
      - 'Line 344: Product not found, record ignored., BaseItemCode=1208-6 DNI'
    - - :warning
      - 'Line 345: Product not found, record ignored., BaseItemCode=1208-9 DNI'
    - - :warning
      - 'Line 916: Product not found, record ignored., BaseItemCode=3167-6 BLK-BLK'
    - - :warning
      - 'Line 926: Product not found, record ignored., BaseItemCode=3167-9 PW-PW'
    - - :warning
      - 'Line 931: Product not found, record ignored., BaseItemCode=3167-LP PW'
    - - :warning
      - 'Line 959: Product not found, record ignored., BaseItemCode=3219-SF AB-AB'
    - - :warning
      - 'Line 3050: Product not found, record ignored., BaseItemCode=DDDD-BA1'
    - - :warning
      - 'Line 3054: Product not found, record ignored., BaseItemCode=DDDD-BA3'
 |

### Q-10_results.md

# Q-10 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-10 — Feature Enablement Gap Analysis
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| enable_sales_portal | enable_online_catalog | enable_online_ordering | kit_item_count | contract_price_count | enrollment_count | smart_stack_count | shared_resource_count | portal_order_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 0 | 530 | 14 | 28 | 6,102 |

### Q-11_results.md

# Q-11 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-11 — Configuration Completeness
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 13
- **Run date**: 2026-06-17


| entity_type | last_updated | days_stale | related_record_count |
| --- | --- | --- | --- |
| sales_quotas | 2025-08-20 19:47:15 | 300 | 0 |
| customer_payment_informations | 2025-08-20 19:47:15 | 300 | — |
| riser_prices | 2025-08-20 19:47:15 | 300 | — |
| placement_reports | 2025-08-20 19:47:15 | 300 | — |
| commitment_reports | 2025-08-20 19:47:15 | 300 | — |
| kit_items | 2025-08-20 19:47:15 | 300 | 0 |
| contract_prices | 2025-08-20 19:47:15 | 300 | 0 |
| customer_favorites | 2025-08-20 19:47:15 | 300 | — |
| price_levels | 2025-11-03 15:37:26 | 225 | — |
| categories | 2026-01-26 21:45:32 | 141 | — |
| groups | 2026-01-26 21:45:32 | 141 | — |
| collections | 2026-03-16 12:02:20 | 92 | — |
| trade_names | 2026-03-16 12:02:20 | 92 | — |

### Q-22_results.md

# Q-22 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-22 — Feature Usage Depth
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | submit_order | select_a_customer | search_for_customer | email_item_info | create_pdf_catalog | view_library_entry | view_smartpicks | access_sales_portal | filter_products | search_products | search_collections | order_configured_item | view_kit | order_kit | share_my_list | export_data_to_csv | export_data_to_excel | total_events | total_users |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gl | Golden Lighting | 59 | 697 | 580 | 183 | 361 | 1,692 | 12 | 1 | 170 | 6,509 | 229 | 10 | 0 | 0 | 7 | 4 | 6 | 20,594 | 51 |

### Q-CI-02_results.md

# Q-CI-02 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-CI-02 — Peer Comparison
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | peer_standing | orders_vs_peer_pct | logins_vs_peer_pct | mrr_vs_peer_pct | peer_orders_median | peer_logins_median | peer_mrr_median |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gl | Golden Lighting | Commerce-Active | Needs Attention | -76.80 | 12.50 | 113 | 254 | 2,833 | 920 |

### Q-CI-03_results.md

# Q-CI-03 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-CI-03 — Feature Adoption Benchmarking
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | feature_depth | has_clicky_portal | arr |
| --- | --- | --- | --- | --- | --- |
| gl | Golden Lighting | Commerce-Active | 6 | 0 | 24,595 |

### Q-CI-03_benchmarks_results.md

# Q-CI-03-bench Results — Golden Lighting (gl, org_id=187)
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
