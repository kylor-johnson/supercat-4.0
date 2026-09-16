# Section 6 Context Bundle — Arabela Lighting (arl)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Arabela Lighting (arl, org_id=269)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | False | portal_order_count=0, portal_order_gmv=$0 |
| HAS_INVENTORY | True | inventory_count=77 |
| HAS_SALES_DATA | False | sales_data_count=0 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=4 engagement_reps=17 (threshold: >=5) |
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
| QUALIFYING_REP_COUNT | 4 | 4 |
| ENGAGEMENT_REP_COUNT | 17 | engagement_reps=17 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 64 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | True | Postgres LTM orders: 314, Mixpanel total submit_order (Q-01): 0 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=89.1%, ambiguous_rate=0.0%, showroom_event_share=46.9% |
| USER_GROUP_JOIN_RATE | 89% | 57 of 64 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 47% | showroom+admin share of matched events: 46.9% |
| ADMIN_REPS_IN_LEADERBOARD | True | 3 admin/showroom users in leaderboard: Lee Nemeth, Nadia Quintero, Sophia Wang |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False |  |
| PORTAL_REP_DATA_PRESENT | False |  |
| PORTAL_CUSTOMER_DATA_PRESENT | False |  |
| INVENTORY_FRESH | False | inventories last_updated 188d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | False | customers last_updated 85d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=196 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | PARTIAL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | LIMITED | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | PARTIAL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Arabela Lighting
- **Shortname**: arl
- **Org ID**: 269
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- portal_orders LTM count=0, gmv=0.0 — HAS_PORTAL_ORDERS overridden to false

## Section Confidence

# Section Confidence Tiers — Arabela Lighting (arl, org_id=269)
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
| INVENTORY_FRESH | False |
| SALES_DATA_FRESH | False |
| CUSTOMER_DATA_FRESH | False |

## Computed Tiers

| Section | Tier | Determining Condition |
| --- | --- | --- |
| §2 Sales Team | STRONG | See Derived Gate 6 §2 formula |
| §3 Customer | PARTIAL | See Derived Gate 6 §3 formula |
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

# Signal Rank — Arabela Lighting (arl, org_id=269)
- **Run date**: 2026-06-17
- **Total signals fired**: 17 (P0: 2, P1: 13, P2: 2)
- **Org GMV**: $0.0M eCat LTM, $0.0M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 50% of eCat GMV | P1 | §4 Commerce | 1.3 | $119,437 | 2.0 | 298,945 | RISK |
| 2 | SIG-DECAY-01 | Reorder Decay — Beautiful Things Lighting & Accessories 3.0x normal gap (55d vs 18d avg) | P0 | §2 Accounts | 3.0 | $18,963 | 3.0 | 170,667 | RISK |
| 3 | SIG-DECAY-01 | Reorder Decay — WAYFAIR 4.6x normal gap (79d vs 17d avg) | P0 | §2 Accounts | 4.6 | $11,650 | 3.0 | 160,770 | RISK |
| 4 | SIG-RISK-03 | Data Staleness — contract_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 5 | SIG-RISK-03 | Data Staleness — customer_favorites last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 6 | SIG-RISK-03 | Data Staleness — kit_items last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 7 | SIG-RISK-03 | Data Staleness — matrix_options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 8 | SIG-RISK-03 | Data Staleness — option_groups last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 9 | SIG-RISK-03 | Data Staleness — options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 10 | SIG-RISK-03 | Data Staleness — commitment_reports last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 11 | SIG-RISK-03 | Data Staleness — placement_reports last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 12 | SIG-RISK-03 | Data Staleness — riser_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 13 | SIG-RISK-03 | Data Staleness — customer_payment_informations last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 14 | SIG-RISK-03 | Data Staleness — sales_quotas last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 15 | SIG-RISK-03 | Data Staleness — inventories last updated 188d ago | P1 | §6 Platform | 2.1 | $1 | 2.0 | 4 | RISK |
| 16 | SIG-RISK-03 | Data Staleness — portal_orders last updated 96d ago | P2 | §6 Platform | 1.1 | $1 | 2.0 | 2 | RISK |
| 17 | SIG-RISK-03 | Data Staleness — portal_invoices last updated 96d ago | P2 | §6 Platform | 1.1 | $1 | 2.0 | 2 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 2 | 0 | 0 | 2 | |
| §4 Commerce Patterns | 0 | 1 | 0 | 1 | |
| §6 Platform Context | 0 | 12 | 2 | 14 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[RISK]** SIG-RISK-01: Revenue Concentration — top 5 accounts generate 50% of eCat GMV
2. **[RISK]** SIG-DECAY-01: Reorder Decay — Beautiful Things Lighting & Accessories 3.0x normal gap (55d vs 18d avg)
3. **[RISK]** SIG-DECAY-01: Reorder Decay — WAYFAIR 4.6x normal gap (79d vs 17d avg)
4. **[RISK]** SIG-RISK-03: Data Staleness — contract_prices last updated 313d ago
5. **[RISK]** SIG-RISK-03: Data Staleness — customer_favorites last updated 313d ago
6. **[RISK]** SIG-RISK-03: Data Staleness — kit_items last updated 313d ago
7. **[RISK]** SIG-RISK-03: Data Staleness — matrix_options last updated 313d ago

**Balance check**: 0 positive (slots 1-0), 7 risk (slots 1-7). Finding #1 is RISK. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-07_results.md

# Q-07 Results — Arabela Lighting (arl, org_id=269)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| visible | 196 | 1 | 0 | 99.50 |

### Q-08_results.md

# Q-08 Results — Arabela Lighting (arl, org_id=269)
- **Query**: Q-08 — Data Freshness Monitor
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 22
- **Run date**: 2026-06-17


| entity_type | last_updated | days_since_update | status |
| --- | --- | --- | --- |
| contract_prices | 2025-08-07 23:13:14 | 313 | Stale |
| customer_favorites | 2025-08-07 23:13:14 | 313 | Stale |
| kit_items | 2025-08-07 23:13:14 | 313 | Stale |
| matrix_options | 2025-08-07 23:13:14 | 313 | Stale |
| option_groups | 2025-08-07 23:13:14 | 313 | Stale |
| options | 2025-08-07 23:13:14 | 313 | Stale |
| commitment_reports | 2025-08-07 23:13:14 | 313 | Stale |
| placement_reports | 2025-08-07 23:13:14 | 313 | Stale |
| riser_prices | 2025-08-07 23:13:14 | 313 | Stale |
| customer_payment_informations | 2025-08-07 23:13:14 | 313 | Stale |
| sales_quotas | 2025-08-07 23:13:14 | 313 | Stale |
| inventories | 2025-12-11 15:14:10 | 188 | Stale |
| portal_orders | 2026-03-13 14:23:45 | 96 | Monitor |
| portal_invoices | 2026-03-13 14:23:45 | 96 | Monitor |
| customers | 2026-03-24 15:04:10 | 85 | Monitor |
| products | 2026-06-16 13:56:11 | 1 | Fresh |
| smart_stacks | 2026-06-16 13:56:11 | 1 | Fresh |
| categories | 2026-06-16 13:56:11 | 1 | Fresh |
| collections | 2026-06-16 13:56:11 | 1 | Fresh |
| groups | 2026-06-16 13:56:11 | 1 | Fresh |
| trade_names | 2026-06-16 13:56:11 | 1 | Fresh |
| price_levels | 2026-06-16 15:26:20 | 1 | Fresh |

### Q-09_results.md

# Q-09 Results — Arabela Lighting (arl, org_id=269)
- **Query**: Q-09 — Import Health — Monthly Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 5
- **Run date**: 2026-06-17


| month | import_count |
| --- | --- |
| 2026-06-01 | 22 |
| 2026-05-01 | 1 |
| 2026-03-01 | 3 |
| 2026-01-01 | 7 |
| 2025-12-01 | 54 |

### Q-09_recent_results.md

# Q-09-recent Results — Arabela Lighting (arl, org_id=269)
- **Query**: Q-09-recent — Import Health — Recent Errors
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| created_at | data |
| --- | --- |
| 2026-06-16T13:56:12.814928 | ---
- - Products
  - []
 |
| 2026-06-16T11:37:15.607008 | ---
- - Products
  - []
 |
| 2026-06-16T07:44:13.487362 | ---
- - Products
  - []
 |
| 2026-06-16T07:37:13.516447 | ---
- - Products
  - []
 |
| 2026-06-16T07:11:11.974503 | ---
- - Products
  - - - :warning
      - 'Error running cleancsv: 2026/06/16 07:11:11 parse error on line 2, column
        122: bare " in non-quoted-field

        '
    - - :warning
      - 'Line 2: Illegal quoting, probably in the following text: "86010-1-1.jpg ..OR..
        86010-1-4.jpg" ..OR.. W9"*H16"*D9" ..OR.. L16.25*W14.5*H10.75" ..OR.. D5*H1.25"
        ..OR.. 7" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 3: Illegal quoting, probably in the following text: "86120-1-1.jpg ..OR..
        86120-1-5.jpg" ..OR.. W9"*H16"*D9" ..OR.. L16.25*W14.5*H10.75" ..OR.. D5*H1.25"
        ..OR.. 7" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 4: Illegal quoting, probably in the following text: "86013-1-1.jpg ..OR..
        86013-1-2.jpg" ..OR.. W9"*H10"*D9" ..OR.. D5*H1.25" ..OR.. L16.5*W16.5*H10.75"
        ..OR.. 17.5" ..OR.. 71" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 5: Illegal quoting, probably in the following text: "86123-1-1.jpg ..OR..
        86123-1-3.jpg" ..OR.. W9"*H10"*D9" ..OR.. D5*H1.25" ..OR.. L16.5*W16.5*H10.75"
        ..OR.. 17.5" ..OR.. 71" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 6: Illegal quoting, probably in the following text: "86011-2-1.jpg ..OR..
        86011-2-5.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 15.5" ..OR.. 70" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 7: Illegal quoting, probably in the following text: "86121-2-1.jpg ..OR..
        86121-2-5.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 15.5" ..OR.. 70" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 8: Illegal quoting, probably in the following text: "86015-1-1.jpg ..OR..
        86015-1-3.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 18" ..OR.. 72" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 9: Illegal quoting, probably in the following text: "86125-1-1.jpg ..OR..
        86125-1-2.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 18" ..OR.. 72" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 10: Illegal quoting, probably in the following text: "86014-6-1.jpg
        ..OR.. 86014-6-5.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 21" ..OR.. 74" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 11: Illegal quoting, probably in the following text: "86124-6-1.jpg
        ..OR.. 86124-6-5.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 21" ..OR.. 74" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 12: Illegal quoting, probably in the following text: "86017-6-1.jpg
        ..OR.. 86017-6-2.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 25" ..OR.. 79" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 13: Illegal quoting, probably in the following text: "86127-6-1.jpg
        ..OR.. 86127-6-2.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 25" ..OR.. 79" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 14: Illegal quoting, probably in the following text: "86001-1-1.jpg
        ..OR.. 86001-1-3.jpg" ..OR.. W8"*H12"*D8" ..OR.. D6"*H1" ..OR.. L20*W13*H14.25"
        ..OR.. 16.5" ..OR.. 70.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 15: Illegal quoting, probably in the following text: "86002-3-1.jpg
        ..OR.. 86002-3-3.jpg" ..OR.. W17"*Max86"*17" ..OR.. L16.75"*W15.75"*H1.5"
        ..OR.. L24.5*W23*H17.5" ..OR.. 37.75" ..OR.. 85.75" ..OR.. 1*3"+3*6"+14*12"
        ..OR.. 120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 16: Illegal quoting, probably in the following text: "86003-6-1.jpg
        ..OR.. 86003-6-3.jpg" ..OR.. W28"*Max86"*28" ..OR.. L28"*W26.75"*H1.5" ..OR..
        L30.5*W30.5*H17.5" ..OR.. 61.75" ..OR.. 85.75" ..OR.. 3*3"+4*6"+22*12" ..OR..
        120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 17: Illegal quoting, probably in the following text: "86031-3-1.jpg
        ..OR.. 86031-3-3.jpg" ..OR.. W10"*H20"*D10" ..OR.. D5*H1" ..OR.. L15.5*W16.5*H11.75"
        ..OR.. 25.5" ..OR.. 79.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 18: Illegal quoting, probably in the following text: "86036-3-1.jpg
        ..OR.. W15"*H35"*D6" ..OR.. L28.5*W11*H12.5" ..OR.. D5*H1" ..OR.. 7" ..OR..
        W3*H12"'
    - - :warning
      - 'Line 19: Illegal quoting, probably in the following text: "86032-24-1.jpg
        ..OR.. 86032-24-3.jpg" ..OR.. W36"*H26"*D36" ..OR.. D5*H1" ..OR.. L24.75*W21*H24.5"
        ..OR.. 29.25" ..OR.. 102.5" ..OR.. 72" ..OR.. 1*12" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 20: Illegal quoting, probably in the following text: "86033-16-1.jpg
        ..OR.. 86033-16-2.jpg" ..OR.. W28"*H22"*D28" ..OR.. D5*H1" ..OR.. L19*W19*H23"
        ..OR.. 25.5" ..OR.. 97.75" ..OR.. 72" ..OR.. 1*10.25" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 21: Illegal quoting, probably in the following text: "86034-8-1.jpg
        ..OR.. 86034-8-3.jpg" ..OR.. W28"*H15"*D28" ..OR.. D5*H1" ..OR.. L18.5*W18.5*H16.25"
        ..OR.. 19.25" ..OR.. 88.5" ..OR.. 72" ..OR.. 1*10.25" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 22: Illegal quoting, probably in the following text: "85190-10-1.jpg
        ..OR.. 85190-10-3.jpg" ..OR.. W35"*H32"*D35" ..OR.. D7.13"*1.66" ..OR.. L28*W24*H27"
        ..OR.. 37" ..OR.. 110" ..OR.. 1*72" ..OR.. 120" ..OR.. L12.13*W9.13*D4"'
    - - :warning
      - 'Line 23: Illegal quoting, probably in the following text: "85191-11.jpg ..OR..
        85191-11_1.jpg" ..OR.. W60"*H20"*D20" ..OR.. D7*H1.5" ..OR.. L55*W24*H15"
        ..OR.. 26" ..OR.. 62" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 24: Illegal quoting, probably in the following text: W26"*H52"*D26"
        ..OR.. D7*H1.5" ..OR.. L44*W24*H15" ..OR.. 55" ..OR.. 127" ..OR.. 1*72" ..OR..
        120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 25: Illegal quoting, probably in the following text: W24"*H33"*D24"
        ..OR.. D7*H1.5" ..OR.. L29*W20*H15" ..OR.. 37" ..OR.. 109" ..OR.. 1*72" ..OR..
        120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 26: Illegal quoting, probably in the following text: "85195-2-1.jpg
        ..OR.. 85195-2-4.jpg" ..OR.. W22"*H28"*D5" ..OR.. D5.88"*H1.13" ..OR.. L18*W15*H14"
        ..OR.. 7" ..OR.. L12.13*W9.13*D4"'
    - - :warning
      - 'Line 27: Illegal quoting, probably in the following text: W9"*H21"*D5" ..OR..
        L13*W13*H16" ..OR.. D5.88*H1.4" ..OR.. 7" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 28: Illegal quoting, probably in the following text: "85390-10-1.jpg
        ..OR.. 85390-10-4.jpg" ..OR.. W39"*H28"*D39" ..OR.. D6"*H1.38" ..OR.. L26*W32*H27"
        ..OR.. 32" ..OR.. 106" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 29: Illegal quoting, probably in the following text: "85490-10-1.jpg
        ..OR.. 85490-10-5.jpg" ..OR.. W39"*H28"*D39" ..OR.. D6"*H1.38" ..OR.. L26*W32*H27"
        ..OR.. 32" ..OR.. 106" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 30: Illegal quoting, probably in the following text: "85391-6-1.jpg
        ..OR.. 85391-6-5.jpg" ..OR.. W32"*H25"*D32" ..OR.. D6"*H1.38" ..OR.. L26*W34*H15"
        ..OR.. 29" ..OR.. 103" ..OR.. 1*72" ..OR.. 1*9.5" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 31: Illegal quoting, probably in the following text: "85491-6-1.jpg
        ..OR.. 85491-6-5.jpg" ..OR.. W32"*H25"*D32" ..OR.. D6"*H1.38" ..OR.. L26*W34*H15"
        ..OR.. 29" ..OR.. 103" ..OR.. 1*72" ..OR.. 1*9.5" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 32: Illegal quoting, probably in the following text: "85394-5-1.jpg
        ..OR.. 85394-5-5.jpg" ..OR.. W33"*H20"*D20" ..OR.. D7.13"*0.88" ..OR.. L22*W28*H17"
        ..OR.. 25" ..OR.. 56" ..OR.. 3*12" ..OR.. 72" ..OR.. L19.25*W4.75*D12.25"'
    - - :warning
      - 'Line 33: Illegal quoting, probably in the following text: "85494-5-1.jpg
        ..OR.. 85494-5-5.jpg" ..OR.. W33"*H20"*D20" ..OR.. D7.13"*0.88" ..OR.. L22*W28*H17"
        ..OR.. 25" ..OR.. 56" ..OR.. 3*12" ..OR.. 72" ..OR.. L19.25*W4.75*D12.25"'
    - - :warning
      - 'Line 34: Illegal quoting, probably in the following text: "85492-10-1.jpg
        ..OR.. 85492-10-3.jpg" ..OR.. W50"*H21"*D30" ..OR.. L15.75"*W6"*H1.25" ..OR..
        L36.5*W20.75*H28" ..OR.. 24.75" ..OR.. 97" ..OR.. 72" ..OR.. 2*12" ..OR..
        120" ..OR.. D12.25*H4.75"'
    - - :warning
      - 'Line 35: Illegal quoting, probably in the following text: "85592-10-1.jpg
        ..OR.. 85592-10-3.jpg" ..OR.. W50"*H21"*D30" ..OR.. L15.75"*W6"*H1.25" ..OR..
        L36.5*W20.75*H28" ..OR.. 24.75" ..OR.. 97" ..OR.. 72" ..OR.. 2*12" ..OR..
        120" ..OR.. D12.25*H4.75"'
    - - :warning
      - 'Line 36: Illegal quoting, probably in the following text: "85395-1-1.jpg
        ..OR.. 85395-1-3.jpg" ..OR.. W16"*H18"*D10" ..OR.. L21*W22*H8" ..OR.. D4.75"*H0.75"
        ..OR.. 7" ..OR.. L19.25*W4.75*D15.63"'
    - - :warning
      - 'Line 37: Illegal quoting, probably in the following text: "85495-1-1.jpg
        ..OR.. 85495-1-3.jpg" ..OR.. W16"*H18"*D10" ..OR.. L21*W22*H8" ..OR.. D4.75"*H0.75"
        ..OR.. 7" ..OR.. L19.25*W4.75*D15.63"'
    - - :warning
      - 'Line 38: Illegal quoting, probably in the following text: "85250-16-1.jpg
        ..OR.. 85250-16-4.jpg" ..OR.. W35"*H23"*D35" ..OR.. L38*W38*H23" ..OR.. 33"
        ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 39: Illegal quoting, probably in the following text: "85350-16-1.jpg
        ..OR.. 85350-16-4.jpg" ..OR.. W35"*H23"*D35" ..OR.. L38*W38*H23" ..OR.. 33"
        ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 40: Illegal quoting, probably in the following text: "85251-9-1.jpg
        ..OR.. 85251-9-4.jpg" ..OR.. W28"*H16"*D28" ..OR.. L31*W31*H21" ..OR.. 26"
        ..OR.. 62" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 41: Illegal quoting, probably in the following text: "85351-9-1.jpg
        ..OR.. 85351-9-5.jpg" ..OR.. W28"*H16"*D28" ..OR.. L31*W31*H21" ..OR.. 26"
        ..OR.. 62" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 42: Illegal quoting, probably in the following text: "85254-6-1.jpg
        ..OR.. 85254-6-4.jpg" ..OR.. W47"*H9"*D12" ..OR.. W17.75"*D4.75"*H0.8" ..OR..
        L15*W50*H13" ..OR.. 18" ..OR.. 54" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 43: Illegal quoting, probably in the following text: "85354-6-1.jpg
        ..OR.. 85354-6-5.jpg" ..OR.. W47"*H9"*D12" ..OR.. W17.75"*D4.75"*H0.8" ..OR..
        L15*W50*H13" ..OR.. 18" ..OR.. 54" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 44: Illegal quoting, probably in the following text: "85256-4-1.jpg
        ..OR.. 85256-4-3.jpg" ..OR.. W12"*H20"*D7" ..OR.. L14*W19*H14" ..OR.. L16.5"*W5.5"*H0.75"
        ..OR.. 7" ..OR.. L9*W3"'
    - - :warning
      - 'Line 45: Illegal quoting, probably in the following text: "85356-4-1.jpg
        ..OR.. 85356-4-3.jpg" ..OR.. W12"*H20"*D7" ..OR.. L14*W19*H14" ..OR.. L16.5"*W5.5"*H0.75"
        ..OR.. 7" ..OR.. L9*W3"'
    - - :warning
      - 'Line 46: Illegal quoting, probably in the following text: "85133-16.jpg ..OR..
        85133-16_1.jpg" ..OR.. W30"*H42"*D30" ..OR.. D5.4*H0.88" ..OR.. L24*W24*H32"
        ..OR.. L30*W30*H30" ..OR.. 47" ..OR.. 117" ..OR.. 1*72" ..OR.. 120" ..OR..
        "L21*W4.88" ..OR.. L21*W4.88" ..OR.. L18.75*W4.88" ..OR.. L15.4*W4.88"'
    - - :warning
      - 'Line 47: Illegal quoting, probably in the following text: "85130-7-1.jpg
        ..OR.. 85130-7-4.jpg" ..OR.. W47"*H24"*D13" ..OR.. L16.5"*4.75"*H0.88" ..OR..
        L49*W16*H28" ..OR.. 29" ..OR.. 101" ..OR.. 1*72" ..OR.. 2*19.25" ..OR.. 120"'
    - - :warning
      - 'Line 48: Illegal quoting, probably in the following text: W26"*H36"*D26"
        ..OR.. D5.4*H0.88" ..OR.. L24*W24*H37" ..OR.. 39" ..OR.. 111" ..OR.. 1*72"
        ..OR.. 120" ..OR.. "L25*W4.75" ..OR.. L16.75*W4.75" ..OR.. L20*W4.75"'
    - - :warning
      - 'Line 49: Illegal quoting, probably in the following text: W20"*H32"*D20"
        ..OR.. D5.4*H0.88" ..OR.. L23*W23*H34" ..OR.. 34" ..OR.. 106" ..OR.. 1*72"
        ..OR.. 120"'
    - - :warning
      - 'Line 50: Illegal quoting, probably in the following text: W24"*H13"*D24"
        ..OR.. D5.88*H0.75" ..OR.. L23*W23*H16" ..OR.. 1*8.5" ..OR.. 7" ..OR.. L8.25*W3.25"'
    - - :warning
      - 'Line 51: Illegal quoting, probably in the following text: W7"*H15"*D5" ..OR..
        L15*W12*H12" ..OR.. L7.1*W4.75*H0.75" ..OR.. 7" ..OR.. "L7.6*W3.1" ..OR..
        L9.6*W3.1"'
    - - :warning
      - 'Line 52: Illegal quoting, probably in the following text: "85422-12-1.jpg
        ..OR.. 85422-12-3.jpg" ..OR.. W42"*H45"*D42" ..OR.. D5.88"*H1" ..OR.. L37*W37*H42"
        ..OR.. 49" ..OR.. 114.5" ..OR.. 1*72" ..OR.. 1*9+1*12" ..OR.. 120"'
    - - :warning
      - 'Line 53: Illegal quoting, probably in the following text: "85421-8-1.jpg
        ..OR.. 85421-8-3.jpg" ..OR.. W30"*H31"*D30" ..OR.. D5.88"*H1" ..OR.. L25*W25*H30"
        ..OR.. 35" ..OR.. 108.75" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120"'
    - - :warning
      - 'Line 54: Illegal quoting, probably in the following text: "85420-12-1.jpg
        ..OR.. 85420-12-5.jpg" ..OR.. W60"*H23"*D18" ..OR.. L21.5"*W4.75"*H0.75" ..OR..
        L55*W14*H23" ..OR.. 26" ..OR.. 99" ..OR.. 1*72" ..OR.. 2*12" ..OR.. 120"'
    - - :warning
      - 'Line 55: Illegal quoting, probably in the following text: "85424-1-1.jpg
        ..OR.. 85424-1-3.jpg" ..OR.. W9"*H13"*D9" ..OR.. D4.75"*H1" ..OR.. L15*W11*H14"
        ..OR.. 24" ..OR.. 59.5" ..OR.. 72"'
    - - :warning
      - 'Line 56: Illegal quoting, probably in the following text: "85425-5-1.jpg
        ..OR.. 85425-5-4.jpg" ..OR.. W28"*H10"*D28" ..OR.. D7.13"*H0.75" ..OR.. L23*W23*H11"
        ..OR.. 7"'
    - - :warning
      - 'Line 57: Illegal quoting, probably in the following text: "85426-4-1.jpg
        ..OR.. 85426-4-5.jpg" ..OR.. W25"*H5"*D5" ..OR.. L20*W9*H9" ..OR.. L13.75"*W5.13"*H0.75"
        ..OR.. 7"'
    - - :warning
      - 'Line 58: Illegal quoting, probably in the following text: "85427-6-1.jpg
        ..OR.. 85427-6-5.jpg" ..OR.. W35"*H6"*D5" ..OR.. L30*W9*H9" ..OR.. L13.75"*W5.13"*H0.75"
        ..OR.. 7"'
    - - :warning
      - 'Line 59: Illegal quoting, probably in the following text: "85423-1-1.jpg
        ..OR.. 85423-1-4.jpg" ..OR.. W11"*H20"*D5" ..OR.. L19*W10*H9" ..OR.. L12.38"*W5"*H1"
        ..OR.. 7"'
    - - :warning
      - 'Line 60: Illegal quoting, probably in the following text: "85202-16.jpg ..OR..
        85202-16_1.jpg" ..OR.. W36"*H48"*D36" ..OR.. D5.5*H1" ..OR.. L39*W39*H35"
        ..OR.. L31*W19*H16" ..OR.. 51" ..OR.. 125" ..OR.. 2*72" ..OR.. 120" ..OR..
        "L11.8*W6" ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 61: Illegal quoting, probably in the following text: "85207-9.jpg ..OR..
        85207-9-2.jpg" ..OR.. W24"*H36"*D24" ..OR.. D5.5"*H1" ..OR.. L28*W28*H30"
        ..OR.. 40" ..OR.. 112" ..OR.. 1*72" ..OR.. 120" ..OR.. L11.75*W5.88"+L9.63*W4.75"+L6.5*W4.88"'
    - - :warning
      - 'Line 62: Illegal quoting, probably in the following text: W30"*H24"*D30"
        ..OR.. D5.5*H1" ..OR.. L31*W31*H30" ..OR.. 30" ..OR.. 103" ..OR.. 1*72" ..OR..
        120" ..OR.. "L11.8*W6" ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 63: Illegal quoting, probably in the following text: "85203-6.jpg ..OR..
        85203-6_1.jpg" ..OR.. W53"*H22"*D10" ..OR.. L15*W4.4*H0.75" ..OR.. L54*W13*H14"
        ..OR.. 26" ..OR.. 98" ..OR.. 1*72" ..OR.. 120" ..OR.. "L11.8*W6" ..OR.. L9.6*W4.75"
        ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 64: Illegal quoting, probably in the following text: "85200-6-1.jpg
        ..OR.. 85200-6-3.jpg" ..OR.. W24"*H21"*D24" ..OR.. D5.5"*H1" ..OR.. L26*W26*H16"
        ..OR.. 24" ..OR.. 96" ..OR.. 1*72" ..OR.. 120" ..OR.. L11.75*W5.88"+L9.63*W4.75"+L6.5*W4.88"'
    - - :warning
      - 'Line 65: Illegal quoting, probably in the following text: "85206-4-1.jpg
        ..OR.. 85206-4-4.jpg" ..OR.. W29"*H10"*D6" ..OR.. L41*W31*H8" ..OR.. L25.63"*W4.75"*H1"
        ..OR.. 7" ..OR.. L9.63*W4.75" L7.63*W4.25" L6.13*W3.88"'
    - - :warning
      - 'Line 66: Illegal quoting, probably in the following text: "85205-2-1.jpg
        ..OR.. 85205-2-5.jpg" ..OR.. W21"*H10"*D6" ..OR.. L15*W23*H8" ..OR.. L17.75"*W4.75"*H1"
        ..OR.. 7" ..OR.. L9.63*W4.75" L7.63*W4.25" L6.13*W3.88"'
    - - :warning
      - 'Line 67: Illegal quoting, probably in the following text: W6"*H12"*D4" ..OR..
        L16*W10*H9" ..OR.. L6*W4.5*H0.63" ..OR.. 23" ..OR.. 90" ..OR.. 7" ..OR.. "L11.8*W6"
        ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 68: Illegal quoting, probably in the following text: "85412-17-1.jpg
        ..OR.. 85412-17-5.jpg" ..OR.. W39"*H23"*D39" ..OR.. D5.88"*H0.75" ..OR.. L42.5*W42.5*H22"
        ..OR.. L42.25*W31.5*H24.5" ..OR.. 33" ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72"
        ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 69: Illegal quoting, probably in the following text: "85512-17-1.jpg
        ..OR.. 85512-17-5.jpg" ..OR.. W39"*H23"*D39" ..OR.. D5.88"*H0.75" ..OR.. L42.5*W42.5*H22"
        ..OR.. L42.25*W31.5*H24.5" ..OR.. 33" ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72"
        ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 70: Illegal quoting, probably in the following text: W39"*H23"*D39"
        ..OR.. D5.5"*H0.75" ..OR.. L42.5*42.5*22" ..OR.. L31.5*W42.25*H24.5" ..OR..
        33" ..OR.. 84" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 71: Illegal quoting, probably in the following text: "85414-20-1.jpg
        ..OR.. 85414-20-5.jpg" ..OR.. W31"*H35"*D31" ..OR.. D5.88"*H0.75" ..OR.. L34*W34*H35"
        ..OR.. L42*W29*H25" ..OR.. 14" ..OR.. 80" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 72: Illegal quoting, probably in the following text: "85514-20-1.jpg
        ..OR.. 85514-20-6.jpg" ..OR.. W31"*H35"*D31" ..OR.. D5.88"*H0.75" ..OR.. L34*W34*H35"
        ..OR.. L42*W29*H25" ..OR.. 14" ..OR.. 80" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 73: Illegal quoting, probably in the following text: W31"*H35"*D31"
        ..OR.. D6*H0.75" ..OR.. L34*W34*H35" ..OR.. L29*W42*H25" ..OR.. 43.75" ..OR..
        94" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 74: Illegal quoting, probably in the following text: "85411-13-1.jpg
        ..OR.. 85411-13-5.jpg" ..OR.. W31"*H19"*D31" ..OR.. D5.5"*H0.75" ..OR.. L33*W33*H28"
        ..OR.. 29" ..OR.. 65" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 75: Illegal quoting, probably in the following text: "85511-13-1.jpg
        ..OR.. 85511-13-6.jpg" ..OR.. W31"*H19"*D31" ..OR.. D5.5"*H0.75" ..OR.. L33*W33*H28"
        ..OR.. 29" ..OR.. 65" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 76: Illegal quoting, probably in the following text: "85621-13-1.jpg
        ..OR.. 85621-13-4.jpg" ..OR.. W31"*H19"*D31" ..OR.. D5.25"*H0.75" ..OR.. L33.5*W33.5*H27.75"
        ..OR.. 18.5" ..OR.. 64.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75
        xW4.25 xH1.25"'
    - - :warning
      - 'Line 77: Illegal quoting, probably in the following text: "85410-7-1.jpg
        ..OR.. 85410-7-6.jpg" ..OR.. W26"*H17"*D26" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H27"
        ..OR.. 27" ..OR.. 63" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 78: Illegal quoting, probably in the following text: "85510-7-1.jpg
        ..OR.. 85510-7-5.jpg" ..OR.. W26"*H17"*D26" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H27"
        ..OR.. 27" ..OR.. 63" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 79: Illegal quoting, probably in the following text: "85620-7-1.jpg
        ..OR.. 85620-7-2.jpg" ..OR.. W26"*H17"*D26" ..OR.. D5.25"*H0.75" ..OR.. L27.75*W27.75*H27.25"
        ..OR.. 27" ..OR.. 63" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25
        xH1.25"'
    - - :warning
      - 'Line 80: Illegal quoting, probably in the following text: "85413-6-1.jpg
        ..OR.. 85413-6-4.jpg" ..OR.. W47"*H11"*D15" ..OR.. L15.75"*W5.13"*H1" ..OR..
        L50*W18*H23" ..OR.. 18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 81: Illegal quoting, probably in the following text: "85513-6-1.jpg
        ..OR.. 85513-6-5.jpg" ..OR.. W47"*H11"*D15" ..OR.. L15.75"*W5.13"*H1" ..OR..
        L50*W18*H23" ..OR.. 18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 82: Illegal quoting, probably in the following text: W47"*H11"*D15"
        ..OR.. D15.75" xH5.25" ..OR.. L17.75*W50.5*H23.25" ..OR.. L15.75*W5.25*H1"
        ..OR.. 18.25" ..OR.. 69" ..OR.. 2*3"+2*6"+8*12" ..OR.. 120" ..OR.. L8.75 xW4.25
        xH1.25"'
    - - :warning
      - 'Line 83: Illegal quoting, probably in the following text: "85415-2-1.jpg
        ..OR.. 85415-2-3.jpg" ..OR.. W15"*H11"*D8" ..OR.. L22*W16*H17" ..OR.. L6.25"*W5.88"*H0.75"
        ..OR.. 7" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 84: Illegal quoting, probably in the following text: "85515-2-1.jpg
        ..OR.. 85515-2-3.jpg" ..OR.. W15"*H11"*D8" ..OR.. L22*W16*H17" ..OR.. L6.25"*W5.88"*H0.75"
        ..OR.. 7" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 85: Illegal quoting, probably in the following text: W15"*H11"*D8" ..OR..
        L15.75*W21.75*H16.5" ..OR.. D6xH6.25" ..OR.. 7" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 86: Illegal quoting, probably in the following text: W34"*H37"*D34"
        ..OR.. D5.5*H1" ..OR.. L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR..
        75" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 87: Illegal quoting, probably in the following text: W34"*H37"*D34"
        ..OR.. D5.5*H1" ..OR.. L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR..
        75" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 88: Illegal quoting, probably in the following text: W34"*H37"*D34"
        ..OR.. D5.5*H1" ..OR.. L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR..
        75.25" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 89: Illegal quoting, probably in the following text: W23"*H29"*D23"
        ..OR.. D5.5*H1" ..OR.. L30*W29*H24" ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 90: Illegal quoting, probably in the following text: "85262-13.jpg ..OR..
        85262-13_1.jpg" ..OR.. W23"*H29"*D23" ..OR.. D5.5*H1" ..OR.. L30*W29*H24"
        ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 91: Illegal quoting, probably in the following text: W23"*H29"*D23"
        ..OR.. D5.5*H1" ..OR.. L30*W29*H24" ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 92: Illegal quoting, probably in the following text: "85161-5.jpg ..OR..
        85161-5_1.jpg" ..OR.. W17"*H20"*D17" ..OR.. D5.5*H1" ..OR.. L23*W20*H23" ..OR..
        28" ..OR.. 64" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 93: Illegal quoting, probably in the following text: W17"*H20"*D17"
        ..OR.. D5.5*H1" ..OR.. L23*W20*H23" ..OR.. 28" ..OR.. 64" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 94: Illegal quoting, probably in the following text: W17"*H20"*D17"
        ..OR.. D5.5*H1" ..OR.. L23*W20*H23" ..OR.. 28" ..OR.. 64" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 95: Illegal quoting, probably in the following text: W12"*H13"*D7" ..OR..
        L18*W13*H16" ..OR.. L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 96: Illegal quoting, probably in the following text: W12"*H13"*D7" ..OR..
        L18*W13*H16" ..OR.. L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 97: Illegal quoting, probably in the following text: W12"*H13"*D7" ..OR..
        L18*W13*H16" ..OR.. L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 98: Illegal quoting, probably in the following text: "85433-12-1.jpg
        ..OR.. 85433-12-3.jpg" ..OR.. W52"*H52"*D52" ..OR.. D5.88*H0.75" ..OR.. L29*W29*H12"
        ..OR.. 58" ..OR.. 126" ..OR.. 1*72" ..OR.. 144"'
    - - :warning
      - 'Line 99: Illegal quoting, probably in the following text: "85432-8-1.jpg
        ..OR.. 85432-8-3.jpg" ..OR.. W38"*H38"*D38" ..OR.. D5.13*H0.75" ..OR.. L56*W56*H14"
        ..OR.. 44" ..OR.. 112" ..OR.. 1*72" ..OR.. 144"'
    - - :warning
      - 'Line 100: Illegal quoting, probably in the following text: "85431-6-1.jpg
        ..OR.. 85431-6-3.jpg" ..OR.. W28"*H30"*D28" ..OR.. D5.13*H0.75" ..OR.. L41*W41*H12"
        ..OR.. 36" ..OR.. 104" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 101: Illegal quoting, probably in the following text: "85430-4-1.jpg
        ..OR.. 85430-4-3.jpg" ..OR.. W16"*H15"*D16" ..OR.. D4.75*H0.75" ..OR.. L31*W31*H10"
        ..OR.. 21" ..OR.. 89" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 102: Illegal quoting, probably in the following text: "85435-8-1.jpg
        ..OR.. 85435-8-5.jpg" ..OR.. W34"*H10"*D34" ..OR.. D5.13*H0.75" ..OR.. L10*W16*H11"
        ..OR.. 18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 103: Illegal quoting, probably in the following text: "85434-6-1.jpg
        ..OR.. 85434-6-4.jpg" ..OR.. W26"*H8"*D26" ..OR.. D5.13*H0.75" ..OR.. L37*W37*H13"
        ..OR.. 16" ..OR.. 53" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 104: Illegal quoting, probably in the following text: "85437-3-1.jpg
        ..OR.. 85437-3-5.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5.13*H0.75" ..OR.. L11*W15*H7"
        ..OR.. 7"'
    - - :warning
      - 'Line 105: Illegal quoting, probably in the following text: "85436-1-1.jpg
        ..OR.. 85436-1-4.jpg" ..OR.. W7"*H9"*D7" ..OR.. D5.13*H0.75" ..OR.. L19*W19*H12"
        ..OR.. 17" ..OR.. 53" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 106: Illegal quoting, probably in the following text: "85438-1-1.jpg
        ..OR.. 85438-1-4.jpg" ..OR.. W8"*H12"*D5" ..OR.. L14.5*W10.75*H7.5" ..OR..
        L9"*4.75"*H0.75" ..OR.. 7"'
    - - :warning
      - 'Line 107: Illegal quoting, probably in the following text: "85232-12.jpg
        ..OR.. 85232-12_1.jpg" ..OR.. W26"*H39"*D26" ..OR.. D5.5*H1" ..OR.. L30*W30*H14"
        ..OR.. 42" ..OR.. 115" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 108: Illegal quoting, probably in the following text: W48"*H24"*D15"
        ..OR.. L16.1*W5.88*H0.88" ..OR.. L50*W22*H11" ..OR.. 27" ..OR.. 100" ..OR..
        2*72" ..OR.. 2*15" ..OR.. 120" ..OR.. L47.25*W14.25*H8.25"'
    - - :warning
      - 'Line 109: Illegal quoting, probably in the following text: W27"*H25"*D27"
        ..OR.. D5.5*H1" ..OR.. L30*W30*H25" ..OR.. 28" ..OR.. 101" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 110: Illegal quoting, probably in the following text: W23"*H27"*D23"
        ..OR.. D5.5*H1" ..OR.. L26*W26*H15" ..OR.. 30" ..OR.. 103" ..OR.. 1*72" ..OR..
        120" ..OR.. D23*H8"'
    - - :warning
      - 'Line 111: Illegal quoting, probably in the following text: W15"*H12"*D15"
        ..OR.. D5.5*H1" ..OR.. L18*W18*H15" ..OR.. 1*3.25" ..OR.. 7" ..OR.. D15*H7"'
    - - :warning
      - 'Line 112: Illegal quoting, probably in the following text: W7"*H9.5"*D7"
        ..OR.. D5.5*H1" ..OR.. L16*W12*H10" ..OR.. 20" ..OR.. 56" ..OR.. 1*6"+3*12"
        ..OR.. 120"'
    - - :warning
      - 'Line 113: Illegal quoting, probably in the following text: W36"*H6"*D6" ..OR..
        L39*W9*H9" ..OR.. L35.38*W4.5*H0.75" ..OR.. 7" ..OR.. L36*W4.8*H5.88"'
    - - :warning
      - 'Line 114: Illegal quoting, probably in the following text: W25"*H6"*D5" ..OR..
        L28*W9*H9" ..OR.. L24.38*W4.5*H0.75" ..OR.. 7" ..OR.. L25*W4.8*H4.38"'
    - - :warning
      - 'Line 115: Illegal quoting, probably in the following text: W8"*H9"*D5" ..OR..
        L11*W10*H8" ..OR.. L6.5*W6.5*H0.75" ..OR.. 7" ..OR.. L8.38*W7.25*H4"'
    - - :warning
      - 'Line 116: Illegal quoting, probably in the following text: W37"*H58"*D37"
        ..OR.. D5.1*H0.75" ..OR.. L43*W40*H13" ..OR.. 67" ..OR.. 103" ..OR.. 120"
        ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 117: Illegal quoting, probably in the following text: "85244-7.jpg ..OR..
        85244-7_1.jpg" ..OR.. W26"*H46"*D26" ..OR.. D23.63*H1" ..OR.. L28*W26*H18"
        ..OR.. 52" ..OR.. 97" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 118: Illegal quoting, probably in the following text: "85242-6.jpg ..OR..
        85242-6_1.jpg" ..OR.. W24"*H45"*D24" ..OR.. D5.1*H0.75" ..OR.. L32*W27*H13"
        ..OR.. 53" ..OR.. 89" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 119: Illegal quoting, probably in the following text: W50"*H23"*D5"
        ..OR.. L50.38*W8.75*H0.75" ..OR.. L54*W15*H13" ..OR.. 32" ..OR.. 97" ..OR..
        120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 120: Illegal quoting, probably in the following text: W20"*H37"*D20"
        ..OR.. D5.1*H0.75" ..OR.. L26*W22*H18" ..OR.. 45" ..OR.. 81" ..OR.. 120" ..OR..
        D3.25*L20.75"'
    - - :warning
      - 'Line 121: Illegal quoting, probably in the following text: W5"*H23"*D5" ..OR..
        D5.1*H0.75" ..OR.. L24*W15*H8" ..OR.. 31" ..OR.. 67" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 122: Illegal quoting, probably in the following text: W6"*H32"*D7" ..OR..
        L35*W13*H10" ..OR.. 7" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 123: Illegal quoting, probably in the following text: "85286-68-1.jpg
        ..OR.. 85286-68-3.jpg" ..OR.. W20"*H54"*D20" ..OR.. D20"*H1.38" ..OR.. L24*W24*H31"
        ..OR.. 20" ..OR.. D3.88"'
    - - :warning
      - 'Line 124: Illegal quoting, probably in the following text: "85283-47-1.jpg
        ..OR.. 85283-47-4.jpg" ..OR.. W20"*H40"*D20" ..OR.. D20"*H1.38" ..OR.. L24*W24*H16"
        ..OR.. 20" ..OR.. D3.88"'
    - - :warning
      - 'Line 125: Illegal quoting, probably in the following text: "85281-19-1.jpg
        ..OR.. 85281-19-4.jpg" ..OR.. W20"*H20"*D20" ..OR.. D20"*H1.38" ..OR.. L24*W24*H16"
        ..OR.. 20" ..OR.. D3.88"'
    - - :warning
      - 'Line 126: Illegal quoting, probably in the following text: "85289-5-1.jpg
        ..OR.. 85289-5-4.jpg" ..OR.. W6"*H25"*D7" ..OR.. L8*W12*H20" ..OR.. L8.63"*W5.75"*H1.38"
        ..OR.. 7" ..OR.. D3.88"'
    - - :warning
      - 'Line 127: Illegal quoting, probably in the following text: "85288-3-1.jpg
        ..OR.. 85288-3-5.jpg" ..OR.. W6"*H15"*D7" ..OR.. L8*W12*H15" ..OR.. L8.63"*W5.75"*H1.38"
        ..OR.. 7" ..OR.. D3.88"'
    - - :warning
      - 'Line 128: Illegal quoting, probably in the following text: "85216-14.jpg
        ..OR.. 85216-14_1.jpg" ..OR.. W50"*H14"*D10" ..OR.. L50.5*W9.88*H1.38" ..OR..
        L54*W13*H15" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 129: Illegal quoting, probably in the following text: "85214-13.jpg
        ..OR.. 85214-13_1.jpg" ..OR.. W24"*H14"*D24" ..OR.. D24*H1.38" ..OR.. L35*W27*H9"
        ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 130: Illegal quoting, probably in the following text: W36"*H14"*D10"
        ..OR.. L36*W9.88*H1.38" ..OR.. L39*W13*H15" ..OR.. 23" ..OR.. 90" ..OR.. 120"
        ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 131: Illegal quoting, probably in the following text: "85213-6.jpg ..OR..
        85213-6_1.jpg" ..OR.. W16"*H14"*D16" ..OR.. D16*H1.38" ..OR.. L26*W19*H9"
        ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 132: Illegal quoting, probably in the following text: W10"*H14"*D10"
        ..OR.. D9.88*H1.25" ..OR.. L16*W15*H9" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR..
        D3.5*L12"'
    - - :warning
      - 'Line 133: Illegal quoting, probably in the following text: W6"*H14"*D6" ..OR..
        D5.88*H1.25" ..OR.. L15*W9*H9" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 134: Illegal quoting, probably in the following text: "85401-9-1.jpg
        ..OR.. 85401-9-3.jpg" ..OR.. W24"*H7"*D24" ..OR.. D24*1.38" ..OR.. L28*W28*H15"
        ..OR.. 51" ..OR.. 75" ..OR.. 1*5.25+31*32+1*7.38+1*1.38+1*8.63+1*10.13+1*6+1*8.75"
        ..OR.. 7" ..OR.. D4"'
    - - :warning
      - 'Line 135: Illegal quoting, probably in the following text: "85400-5-1.jpg
        ..OR.. 85400-5-3.jpg" ..OR.. W16"*H7"*D16" ..OR.. D15.75"*1.38" ..OR.. L20*W20*H15"
        ..OR.. 42" ..OR.. 66" ..OR.. 1*9"+15*12"+1*1.38"+1*6"+1*10.38"+1*3" ..OR..
        7" ..OR.. D4"'
    - - :warning
      - 'Line 136: Illegal quoting, probably in the following text: "85404-5-1.jpg
        ..OR.. 85404-5-5.jpg" ..OR.. W43"*H7"*D6" ..OR.. L43.25"*W6.25"*H1.38" ..OR..
        L10*W47*H15" ..OR.. 21" ..OR.. 57" ..OR.. 7*6+15*12" ..OR.. 7" ..OR.. D4"'
    - - :warning
      - 'Line 137: Illegal quoting, probably in the following text: "85406-1-1.jpg
        ..OR.. 85406-1-4.jpg" ..OR.. W6"*H7"*D4" ..OR.. D5.5"*H1.25" ..OR.. L9*W17*H8"
        ..OR.. 15" ..OR.. 51" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D4"'
    - - :warning
      - 'Line 138: Illegal quoting, probably in the following text: "85407-1-1.jpg
        ..OR.. 85407-1-5.jpg" ..OR.. W5"*H13"*D6" ..OR.. L13.13"*5.38"*1.25" ..OR..
        L11*W16*H9" ..OR.. 7" ..OR.. D4"'
    - - :warning
      - 'Line 139: Illegal quoting, probably in the following text: W36"*H34"*D36"
        ..OR.. 6.25"*1" ..OR.. L40*W40*H20" ..OR.. 41" ..OR.. 109" ..OR.. 1*72" ..OR..
        120" ..OR.. L13.75"*D1"'
    - - :warning
      - 'Line 140: Illegal quoting, probably in the following text: W45"*H26"*D12"
        ..OR.. L17.75"*W5"*H1" ..OR.. L17*W48*H18" ..OR.. 33" ..OR.. 100" ..OR.. 1*72"
        ..OR.. 120" ..OR.. L13.75"*D1"'
    - - :warning
      - 'Line 141: Illegal quoting, probably in the following text: "85101-8.jpg ..OR..
        85101-8_1.jpg" ..OR.. W30"*H26"*D30" ..OR.. D5.1*H0.75" ..OR.. L33*W33*H16"
        ..OR.. 29" ..OR.. 101" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 142: Illegal quoting, probably in the following text: W24"*H20"*D24"
        ..OR.. D5.1*H0.75" ..OR.. L27*W27*H14" ..OR.. 23" ..OR.. 95" ..OR.. 1*72"
        ..OR.. 1*8.7" ..OR.. 120" ..OR.. D1*H10.75"'
    - - :warning
      - 'Line 143: Illegal quoting, probably in the following text: W18"*H17"*D18"
        ..OR.. D5.1*H0.75" ..OR.. L21*W21*H14" ..OR.. 21" ..OR.. 92" ..OR.. 1*72"
        ..OR.. 1*6" ..OR.. 120" ..OR.. D1*H10.75"'
    - - :warning
      - 'Line 144: Illegal quoting, probably in the following text: "85109-4-1.jpg
        ..OR.. 85109-4-2.jpg" ..OR.. W21"*H12"*D21" ..OR.. D5"*D0.75" ..OR.. L25*W25*H10"
        ..OR.. 7" ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 145: Illegal quoting, probably in the following text: "85108-4-1.jpg
        ..OR.. 85108-4-5.jpg" ..OR.. W36"*H8"*D5" ..OR.. L10*W39*H13" ..OR.. L33"*W5"*H0.75"
        ..OR.. 7" ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 146: Illegal quoting, probably in the following text: "85107-3-1.jpg
        ..OR.. 85107-3-2.jpg" ..OR.. W26"*H8"*D5" ..OR.. L10*W30*H13" ..OR.. L23.5"*W5"*H0.75"
        ..OR.. 7" ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 147: Illegal quoting, probably in the following text: W9"*H26"*D9" ..OR..
        D5.1*H0.75" ..OR.. L20*W18*H11" ..OR.. 29" ..OR.. 101" ..OR.. 1*72" ..OR..
        1*12" ..OR.. 120" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 148: Illegal quoting, probably in the following text: "85106-1-1.jpg
        ..OR.. 85106-1-2.jpg" ..OR.. W7"*H20"*D5" ..OR.. L11*W23*H15" ..OR.. L15"*W4.25"*H0.75"
        ..OR.. 7" ..OR.. L19.25*D0.72"'
    - - :warning
      - 'Line 149: Illegal quoting, probably in the following text: W9"*H15"*D5" ..OR..
        L18*W12*H11" ..OR.. L8.25*W4.75*H0.75" ..OR.. 7" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 150: Illegal quoting, probably in the following text: "85171-12.jpg
        ..OR.. 85171-12_1.jpg" ..OR.. W32"*H12"*D32" ..OR.. L35*W35*H15" ..OR.. 20"
        ..OR.. 83" ..OR.. 120" ..OR.. "L6.75*W1.5*H0.6" ..OR.. L8.3*W1.5*H0.6" ..OR..
        L10*W1.5*H0.6"'
    - - :warning
      - 'Line 151: Illegal quoting, probably in the following text: W50"*H13"*D4"
        ..OR.. L19.63*W5.5*H0.88" ..OR.. L53*W13*H15" ..OR.. 20" ..OR.. 83" ..OR..
        120" ..OR.. "L6.75*W1.5*H0.6" ..OR.. L8.3*W1.5*H0.6" ..OR.. L10*W1.5*H0.6"'
    - - :warning
      - 'Line 152: Illegal quoting, probably in the following text: W10"*H12"*D5"
        ..OR.. L15*W12*H11" ..OR.. L11.75*W9.4*H0.75" ..OR.. 7" ..OR.. "L6.75*W1.5*H0.6"
        ..OR.. L8.3*W1.5*H0.6" ..OR.. L10*W1.5*H0.6"'
    - - :warning
      - 'Line 153: Illegal quoting, probably in the following text: W57"*H26"*D30"
        ..OR.. D7*H1.5" ..OR.. L60*W30*H27" ..OR.. 34" ..OR.. 70" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 154: Illegal quoting, probably in the following text: "85182-9.jpg ..OR..
        85182-9_1.jpg" ..OR.. W37"*H30"*D37" ..OR.. D7*H1.5" ..OR.. L35*W35*H28" ..OR..
        33" ..OR.. 105" ..OR.. 1*72" ..OR.. 120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 155: Illegal quoting, probably in the following text: W21"*H34"*D21"
        ..OR.. D7*H1.5" ..OR.. L32*W26*H17" ..OR.. 36" ..OR.. 109" ..OR.. 1*72" ..OR..
        120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 156: Illegal quoting, probably in the following text: W6"*H14"*D10"
        ..OR.. L18*W13*H9" ..OR.. D6*H1.5" ..OR.. 7" ..OR.. D6*H6"'
    - - :warning
      - 'Line 157: Illegal quoting, probably in the following text: "85270-12-1.jpg
        ..OR.. 85270-12-3.jpg" ..OR.. W32"*H40"*D32" ..OR.. L35*W35*H40" ..OR.. L34*26*15"
        ..OR.. 49" ..OR.. 85" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. "D9.88""+D7.88"'
    - - :warning
      - 'Line 158: Illegal quoting, probably in the following text: "85370-12-1.jpg
        ..OR.. 85370-12-4.jpg" ..OR.. W32"*H40"*D32" ..OR.. L35*W35*H40" ..OR.. L34*26*15"
        ..OR.. 49" ..OR.. 85" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. "D9.88""+D7.88"'
    - - :warning
      - 'Line 159: Illegal quoting, probably in the following text: "85271-12-1.jpg
        ..OR.. 85271-12-51.jpg" ..OR.. W25"*H34"*D25" ..OR.. D5.13"*H0.75" ..OR..
        L28*W28*H30.5" ..OR.. L28*W18*H21" ..OR.. 43" ..OR.. 79" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. "D5.88""+D7.13"'
    - - :warning
      - 'Line 160: Illegal quoting, probably in the following text: "85371-12-1.jpg
        ..OR.. 85371-12-4.jpg" ..OR.. W25"*H34"*D25" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H30.5"
        ..OR.. L28*W18*H21" ..OR.. 43" ..OR.. 79" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        "D5.88""+D7.13"'
    - - :warning
      - 'Line 161: Illegal quoting, probably in the following text: "85273-8-1.jpg
        ..OR.. 85273-8-4.jpg" ..OR.. W56"*H25"*D18" ..OR.. L27.13"*W5.13"*H1" ..OR..
        L59*W23.5*H22" ..OR.. L26*W26*H20" ..OR.. 33" ..OR.. 70" ..OR.. 2*6+6*12"
        ..OR.. 72" ..OR.. D7.88"+D9.88"'
    - - :warning
      - 'Line 162: Illegal quoting, probably in the following text: "85373-8-1.jpg
        ..OR.. 85373-8-1.jpg" ..OR.. W56"*H25"*D18" ..OR.. L27.13"*W5.13"*H1" ..OR..
        L59*W23.5*H22" ..OR.. L26*W26*H20" ..OR.. 33" ..OR.. 70" ..OR.. 2*6+6*12"
        ..OR.. 72" ..OR.. D7.88"+D9.88"'
    - - :warning
      - 'Line 163: Illegal quoting, probably in the following text: W14"*H19"*D14"
        ..OR.. D5.13"*H0.75" ..OR.. L20*W25*H18" ..OR.. 28" ..OR.. 64" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. D13.75"'
    - - :warning
      - 'Line 164: Illegal quoting, probably in the following text: "85376-1-1.jpg
        ..OR.. 85376-1-3.jpg" ..OR.. W14"*H19"*D14" ..OR.. D5.13"*H0.75" ..OR.. L20*W25*H18"
        ..OR.. 28" ..OR.. 64" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D13.75"'
    - - :warning
      - 'Line 165: Illegal quoting, probably in the following text: W10"*H14"*D10"
        ..OR.. D5.13"*H0.75" ..OR.. L18*W21*H14" ..OR.. 24" ..OR.. 60" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. D9.88"'
    - - :warning
      - 'Line 166: Illegal quoting, probably in the following text: "85375-1-1.jpg
        ..OR.. 85375-1-2.jpg" ..OR.. W10"*H14"*D10" ..OR.. D5.13"*H0.75" ..OR.. L18*W21*H14"
        ..OR.. 24" ..OR.. 60" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D9.88"'
    - - :warning
      - 'Line 167: Illegal quoting, probably in the following text: W38"*H38"*D38"
        ..OR.. D6.4*H1.88" ..OR.. L41*W41*H40" ..OR.. L32*W24*H24" ..OR.. L32*W24*H24"
        ..OR.. 48" ..OR.. 72" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D10*H1.5"'
    - - :warning
      - 'Line 168: Illegal quoting, probably in the following text: "85122-12.jpg
        ..OR.. 85122-12_1.jpg" ..OR.. W26"*H26"*D26" ..OR.. D6.4*H1.88" ..OR.. L31*W31*H31"
        ..OR.. L30*W24*H24" ..OR.. 36" ..OR.. 66" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR..
        D10*H1.5"'
    - - :warning
      - 'Line 169: Illegal quoting, probably in the following text: "85123-6.jpg ..OR..
        85123-6_1.jpg" ..OR.. W24"*H18"*D24" ..OR.. D6.4*H1.88" ..OR.. L28*W26*H26"
        ..OR.. 1*6" ..OR.. 7" ..OR.. D10*H1.5"'
    - - :warning
      - 'Line 170: Illegal quoting, probably in the following text: "85124-8-1.jpg
        ..OR.. 85124-8-5.jpg" ..OR.. W58"*H10"*D13" ..OR.. L16.88"*W5.88"*H0.88" ..OR..
        L54*W14*H16" ..OR.. 13" ..OR.. 49" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. D9.63"*1.63"'
    - - :warning
      - 'Line 171: Illegal quoting, probably in the following text: "85125-3-1.jpg
        ..OR.. 85125-3-2.jpg" ..OR.. W15"*H27"*D6" ..OR.. L24*W15*H13" ..OR.. D4.75"*H0.75"
        ..OR.. 7" ..OR.. D9.63"*1.63"'
    - - :warning
      - 'Line 172: Illegal quoting, probably in the following text: W24"*H27"*D24"
        ..OR.. D5.88*H0.88" ..OR.. L28*W28*H29" ..OR.. 36" ..OR.. 72" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D23.75*H23.75"'
    - - :warning
      - 'Line 173: Illegal quoting, probably in the following text: W16"*H19"*D16"
        ..OR.. D5.88*H0.88" ..OR.. L19.5*W19.5*H20.75" ..OR.. 29" ..OR.. 65" ..OR..
        1*6"+3*12" ..OR.. 120" ..OR.. D15.75*H15.75"'
    - - :warning
      - 'Line 174: Illegal quoting, probably in the following text: "85221-1.jpg ..OR..
        85221-1_1.jpg" ..OR.. W8"*H10"*D8" ..OR.. D5.88*H0.88" ..OR.. L11*W11*H13"
        ..OR.. 20" ..OR.. 56" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D7.5*H7.5"'
    - - :warning
      - 'Line 175: Illegal quoting, probably in the following text: W41"*H31"*D41"
        ..OR.. D5.5*H1" ..OR.. L43*W43*H9" ..OR.. 34" ..OR.. 106" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 176: Illegal quoting, probably in the following text: W29"*H27"*D29"
        ..OR.. D5.5*H1" ..OR.. L32*W32*H9" ..OR.. 32" ..OR.. 102" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 177: Illegal quoting, probably in the following text: W6"*H18"*D4" ..OR..
        L21*W8*H7" ..OR.. L18*W5.75*H1.25" ..OR.. 7"'
    - - :warning
      - 'Line 178: Illegal quoting, probably in the following text: "85111-6.jpg ..OR..
        85111-6_1.jpg" ..OR.. W36"*H18"*D36" ..OR.. D5.1*H0.75" ..OR.. L40*W40*H22"
        ..OR.. 32" ..OR.. 80" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D36*H18"'
    - - :warning
      - 'Line 179: Illegal quoting, probably in the following text: W24"*H12"*D24"
        ..OR.. D5.1*H0.75" ..OR.. L28*W28*H16" ..OR.. 32" ..OR.. 74" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D24*H12"'
    - - :warning
      - 'Line 180: Illegal quoting, probably in the following text: W16"*H16"*D16"
        ..OR.. D5.1*H0.75" ..OR.. L19*W19*H19" ..OR.. 30" ..OR.. 73" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D16*H15.5"'
    - - :warning
      - 'Line 181: Illegal quoting, probably in the following text: W36"*H21"*D36"
        ..OR.. D5.5*H1" ..OR.. L39*W39*H13" ..OR.. 24" ..OR.. 96" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 182: Illegal quoting, probably in the following text: "85141-6.jpg ..OR..
        85141-6_1.jpg" ..OR.. W27"*H18"*D27" ..OR.. D5.5*H1" ..OR.. L30*W30*H12" ..OR..
        21" ..OR.. 93" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 183: Illegal quoting, probably in the following text: W14"*H21"*D14"
        ..OR.. D5.5*H1" ..OR.. L18*W18*H30" ..OR.. 24" ..OR.. 96" ..OR.. "Iron ..OR..
        solid wood and glass" ..OR.. 1*72" ..OR.. 120" ..OR.. L11.6*W10*H3"'
    - - :warning
      - 'Line 184: Illegal quoting, probably in the following text: "65000-1.jpg ..OR..
        65000-6.jpg" ..OR.. W5"*H19"*D3" ..OR.. W4.72"*H18"'
    - - :warning
      - 'Line 185: Illegal quoting, probably in the following text: "65001-1.jpg ..OR..
        65001-7.jpg" ..OR.. W5"*H24"*D3" ..OR.. W4.72"*H24.7"'
    - - :warning
      - 'Line 186: Illegal quoting, probably in the following text: "65060-1.jpg ..OR..
        65060-5.jpg" ..OR.. W6"*H18"*D3"'
    - - :warning
      - 'Line 187: Illegal quoting, probably in the following text: "65061-1.jpg ..OR..
        65061-5.jpg" ..OR.. W6"*H27"*D3"'
    - - :warning
      - 'Line 188: Illegal quoting, probably in the following text: "65030-1.jpg ..OR..
        65030-4.jpg" ..OR.. W7"*H14"*D4" ..OR.. W7"*H14.37"'
    - - :warning
      - 'Line 189: Illegal quoting, probably in the following text: "65031-1.jpg ..OR..
        65031-4.jpg" ..OR.. W7"*H24"*D4" ..OR.. W7"*H24"'
    - - :warning
      - 'Line 190: Illegal quoting, probably in the following text: "65040-1.jpg ..OR..
        65040-5.jpg" ..OR.. W6"*H16"*D3" ..OR.. "Stainless steel ..OR..  aluminium
        and crystal"'
    - - :warning
      - 'Line 191: Illegal quoting, probably in the following text: "65041-1.jpg ..OR..
        65041-5.jpg" ..OR.. W6"*H24"*D3" ..OR.. "Stainless steel ..OR..  aluminium
        and crystal"'
    - - :warning
      - 'Line 192: Illegal quoting, probably in the following text: "65010-1.jpg ..OR..
        65010-5.jpg" ..OR.. W6"*H11"*D3" ..OR.. W4.72"*H4.3"'
    - - :warning
      - 'Line 193: Illegal quoting, probably in the following text: "65011-1.jpg ..OR..
        65011-5.jpg" ..OR.. W6"*H15"*D3" ..OR.. W4.72"*H4.3"'
    - - :warning
      - 'Line 194: Illegal quoting, probably in the following text: "65050-1.jpg ..OR..
        65050-5.jpg" ..OR.. W7"*H14"*D2"'
    - - :warning
      - 'Line 195: Illegal quoting, probably in the following text: "65051-1.jpg ..OR..
        65051-4.jpg" ..OR.. W7"*H18"*D2"'
    - - :warning
      - 'Line 196: Illegal quoting, probably in the following text: "65090-1.jpg ..OR..
        65090-4.jpg" ..OR.. W5"*H16"*D4"'
    - - :warning
      - 'Line 197: Illegal quoting, probably in the following text: "65091-1.jpg ..OR..
        65091-4.jpg" ..OR.. W5"*H24"*D4"'
 |
| 2026-06-16T07:10:09.612385 | ---
- - Products
  - - - :warning
      - 'Error running cleancsv: 2026/06/16 07:10:09 parse error on line 2, column
        122: bare " in non-quoted-field

        '
    - - :warning
      - 'Line 2: Illegal quoting, probably in the following text: "86010-1-1.jpg ..OR..
        86010-1-4.jpg" ..OR.. W9"*H16"*D9" ..OR.. L16.25*W14.5*H10.75" ..OR.. D5*H1.25"
        ..OR.. 7" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 3: Illegal quoting, probably in the following text: "86120-1-1.jpg ..OR..
        86120-1-5.jpg" ..OR.. W9"*H16"*D9" ..OR.. L16.25*W14.5*H10.75" ..OR.. D5*H1.25"
        ..OR.. 7" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 4: Illegal quoting, probably in the following text: "86013-1-1.jpg ..OR..
        86013-1-2.jpg" ..OR.. W9"*H10"*D9" ..OR.. D5*H1.25" ..OR.. L16.5*W16.5*H10.75"
        ..OR.. 17.5" ..OR.. 71" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 5: Illegal quoting, probably in the following text: "86123-1-1.jpg ..OR..
        86123-1-3.jpg" ..OR.. W9"*H10"*D9" ..OR.. D5*H1.25" ..OR.. L16.5*W16.5*H10.75"
        ..OR.. 17.5" ..OR.. 71" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 6: Illegal quoting, probably in the following text: "86011-2-1.jpg ..OR..
        86011-2-5.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 15.5" ..OR.. 70" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 7: Illegal quoting, probably in the following text: "86121-2-1.jpg ..OR..
        86121-2-5.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 15.5" ..OR.. 70" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 8: Illegal quoting, probably in the following text: "86015-1-1.jpg ..OR..
        86015-1-3.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 18" ..OR.. 72" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 9: Illegal quoting, probably in the following text: "86125-1-1.jpg ..OR..
        86125-1-2.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 18" ..OR.. 72" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 10: Illegal quoting, probably in the following text: "86014-6-1.jpg
        ..OR.. 86014-6-5.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 21" ..OR.. 74" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 11: Illegal quoting, probably in the following text: "86124-6-1.jpg
        ..OR.. 86124-6-5.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 21" ..OR.. 74" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 12: Illegal quoting, probably in the following text: "86017-6-1.jpg
        ..OR.. 86017-6-2.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 25" ..OR.. 79" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 13: Illegal quoting, probably in the following text: "86127-6-1.jpg
        ..OR.. 86127-6-2.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 25" ..OR.. 79" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 14: Illegal quoting, probably in the following text: "86001-1-1.jpg
        ..OR.. 86001-1-3.jpg" ..OR.. W8"*H12"*D8" ..OR.. D6"*H1" ..OR.. L20*W13*H14.25"
        ..OR.. 16.5" ..OR.. 70.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 15: Illegal quoting, probably in the following text: "86002-3-1.jpg
        ..OR.. 86002-3-3.jpg" ..OR.. W17"*Max86"*17" ..OR.. L16.75"*W15.75"*H1.5"
        ..OR.. L24.5*W23*H17.5" ..OR.. 37.75" ..OR.. 85.75" ..OR.. 1*3"+3*6"+14*12"
        ..OR.. 120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 16: Illegal quoting, probably in the following text: "86003-6-1.jpg
        ..OR.. 86003-6-3.jpg" ..OR.. W28"*Max86"*28" ..OR.. L28"*W26.75"*H1.5" ..OR..
        L30.5*W30.5*H17.5" ..OR.. 61.75" ..OR.. 85.75" ..OR.. 3*3"+4*6"+22*12" ..OR..
        120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 17: Illegal quoting, probably in the following text: "86031-3-1.jpg
        ..OR.. 86031-3-3.jpg" ..OR.. W10"*H20"*D10" ..OR.. D5*H1" ..OR.. L15.5*W16.5*H11.75"
        ..OR.. 25.5" ..OR.. 79.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 18: Illegal quoting, probably in the following text: "86036-3-1.jpg
        ..OR.. W15"*H35"*D6" ..OR.. L28.5*W11*H12.5" ..OR.. D5*H1" ..OR.. 7" ..OR..
        W3*H12"'
    - - :warning
      - 'Line 19: Illegal quoting, probably in the following text: "86032-24-1.jpg
        ..OR.. 86032-24-3.jpg" ..OR.. W36"*H26"*D36" ..OR.. D5*H1" ..OR.. L24.75*W21*H24.5"
        ..OR.. 29.25" ..OR.. 102.5" ..OR.. 72" ..OR.. 1*12" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 20: Illegal quoting, probably in the following text: "86033-16-1.jpg
        ..OR.. 86033-16-2.jpg" ..OR.. W28"*H22"*D28" ..OR.. D5*H1" ..OR.. L19*W19*H23"
        ..OR.. 25.5" ..OR.. 97.75" ..OR.. 72" ..OR.. 1*10.25" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 21: Illegal quoting, probably in the following text: "86034-8-1.jpg
        ..OR.. 86034-8-3.jpg" ..OR.. W28"*H15"*D28" ..OR.. D5*H1" ..OR.. L18.5*W18.5*H16.25"
        ..OR.. 19.25" ..OR.. 88.5" ..OR.. 72" ..OR.. 1*10.25" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 22: Illegal quoting, probably in the following text: "85190-10-1.jpg
        ..OR.. 85190-10-3.jpg" ..OR.. W35"*H32"*D35" ..OR.. D7.13"*1.66" ..OR.. L28*W24*H27"
        ..OR.. 37" ..OR.. 110" ..OR.. 1*72" ..OR.. 120" ..OR.. L12.13*W9.13*D4"'
    - - :warning
      - 'Line 23: Illegal quoting, probably in the following text: "85191-11.jpg ..OR..
        85191-11_1.jpg" ..OR.. W60"*H20"*D20" ..OR.. D7*H1.5" ..OR.. L55*W24*H15"
        ..OR.. 26" ..OR.. 62" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 24: Illegal quoting, probably in the following text: W26"*H52"*D26"
        ..OR.. D7*H1.5" ..OR.. L44*W24*H15" ..OR.. 55" ..OR.. 127" ..OR.. 1*72" ..OR..
        120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 25: Illegal quoting, probably in the following text: W24"*H33"*D24"
        ..OR.. D7*H1.5" ..OR.. L29*W20*H15" ..OR.. 37" ..OR.. 109" ..OR.. 1*72" ..OR..
        120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 26: Illegal quoting, probably in the following text: "85195-2-1.jpg
        ..OR.. 85195-2-4.jpg" ..OR.. W22"*H28"*D5" ..OR.. D5.88"*H1.13" ..OR.. L18*W15*H14"
        ..OR.. 7" ..OR.. L12.13*W9.13*D4"'
    - - :warning
      - 'Line 27: Illegal quoting, probably in the following text: W9"*H21"*D5" ..OR..
        L13*W13*H16" ..OR.. D5.88*H1.4" ..OR.. 7" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 28: Illegal quoting, probably in the following text: "85390-10-1.jpg
        ..OR.. 85390-10-4.jpg" ..OR.. W39"*H28"*D39" ..OR.. D6"*H1.38" ..OR.. L26*W32*H27"
        ..OR.. 32" ..OR.. 106" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 29: Illegal quoting, probably in the following text: "85490-10-1.jpg
        ..OR.. 85490-10-5.jpg" ..OR.. W39"*H28"*D39" ..OR.. D6"*H1.38" ..OR.. L26*W32*H27"
        ..OR.. 32" ..OR.. 106" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 30: Illegal quoting, probably in the following text: "85391-6-1.jpg
        ..OR.. 85391-6-5.jpg" ..OR.. W32"*H25"*D32" ..OR.. D6"*H1.38" ..OR.. L26*W34*H15"
        ..OR.. 29" ..OR.. 103" ..OR.. 1*72" ..OR.. 1*9.5" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 31: Illegal quoting, probably in the following text: "85491-6-1.jpg
        ..OR.. 85491-6-5.jpg" ..OR.. W32"*H25"*D32" ..OR.. D6"*H1.38" ..OR.. L26*W34*H15"
        ..OR.. 29" ..OR.. 103" ..OR.. 1*72" ..OR.. 1*9.5" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 32: Illegal quoting, probably in the following text: "85394-5-1.jpg
        ..OR.. 85394-5-5.jpg" ..OR.. W33"*H20"*D20" ..OR.. D7.13"*0.88" ..OR.. L22*W28*H17"
        ..OR.. 25" ..OR.. 56" ..OR.. 3*12" ..OR.. 72" ..OR.. L19.25*W4.75*D12.25"'
    - - :warning
      - 'Line 33: Illegal quoting, probably in the following text: "85494-5-1.jpg
        ..OR.. 85494-5-5.jpg" ..OR.. W33"*H20"*D20" ..OR.. D7.13"*0.88" ..OR.. L22*W28*H17"
        ..OR.. 25" ..OR.. 56" ..OR.. 3*12" ..OR.. 72" ..OR.. L19.25*W4.75*D12.25"'
    - - :warning
      - 'Line 34: Illegal quoting, probably in the following text: "85492-10-1.jpg
        ..OR.. 85492-10-3.jpg" ..OR.. W50"*H21"*D30" ..OR.. L15.75"*W6"*H1.25" ..OR..
        L36.5*W20.75*H28" ..OR.. 24.75" ..OR.. 97" ..OR.. 72" ..OR.. 2*12" ..OR..
        120" ..OR.. D12.25*H4.75"'
    - - :warning
      - 'Line 35: Illegal quoting, probably in the following text: "85592-10-1.jpg
        ..OR.. 85592-10-3.jpg" ..OR.. W50"*H21"*D30" ..OR.. L15.75"*W6"*H1.25" ..OR..
        L36.5*W20.75*H28" ..OR.. 24.75" ..OR.. 97" ..OR.. 72" ..OR.. 2*12" ..OR..
        120" ..OR.. D12.25*H4.75"'
    - - :warning
      - 'Line 36: Illegal quoting, probably in the following text: "85395-1-1.jpg
        ..OR.. 85395-1-3.jpg" ..OR.. W16"*H18"*D10" ..OR.. L21*W22*H8" ..OR.. D4.75"*H0.75"
        ..OR.. 7" ..OR.. L19.25*W4.75*D15.63"'
    - - :warning
      - 'Line 37: Illegal quoting, probably in the following text: "85495-1-1.jpg
        ..OR.. 85495-1-3.jpg" ..OR.. W16"*H18"*D10" ..OR.. L21*W22*H8" ..OR.. D4.75"*H0.75"
        ..OR.. 7" ..OR.. L19.25*W4.75*D15.63"'
    - - :warning
      - 'Line 38: Illegal quoting, probably in the following text: "85250-16-1.jpg
        ..OR.. 85250-16-4.jpg" ..OR.. W35"*H23"*D35" ..OR.. L38*W38*H23" ..OR.. 33"
        ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 39: Illegal quoting, probably in the following text: "85350-16-1.jpg
        ..OR.. 85350-16-4.jpg" ..OR.. W35"*H23"*D35" ..OR.. L38*W38*H23" ..OR.. 33"
        ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 40: Illegal quoting, probably in the following text: "85251-9-1.jpg
        ..OR.. 85251-9-4.jpg" ..OR.. W28"*H16"*D28" ..OR.. L31*W31*H21" ..OR.. 26"
        ..OR.. 62" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 41: Illegal quoting, probably in the following text: "85351-9-1.jpg
        ..OR.. 85351-9-5.jpg" ..OR.. W28"*H16"*D28" ..OR.. L31*W31*H21" ..OR.. 26"
        ..OR.. 62" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 42: Illegal quoting, probably in the following text: "85254-6-1.jpg
        ..OR.. 85254-6-4.jpg" ..OR.. W47"*H9"*D12" ..OR.. W17.75"*D4.75"*H0.8" ..OR..
        L15*W50*H13" ..OR.. 18" ..OR.. 54" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 43: Illegal quoting, probably in the following text: "85354-6-1.jpg
        ..OR.. 85354-6-5.jpg" ..OR.. W47"*H9"*D12" ..OR.. W17.75"*D4.75"*H0.8" ..OR..
        L15*W50*H13" ..OR.. 18" ..OR.. 54" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 44: Illegal quoting, probably in the following text: "85256-4-1.jpg
        ..OR.. 85256-4-3.jpg" ..OR.. W12"*H20"*D7" ..OR.. L14*W19*H14" ..OR.. L16.5"*W5.5"*H0.75"
        ..OR.. 7" ..OR.. L9*W3"'
    - - :warning
      - 'Line 45: Illegal quoting, probably in the following text: "85356-4-1.jpg
        ..OR.. 85356-4-3.jpg" ..OR.. W12"*H20"*D7" ..OR.. L14*W19*H14" ..OR.. L16.5"*W5.5"*H0.75"
        ..OR.. 7" ..OR.. L9*W3"'
    - - :warning
      - 'Line 46: Illegal quoting, probably in the following text: "85133-16.jpg ..OR..
        85133-16_1.jpg" ..OR.. W30"*H42"*D30" ..OR.. D5.4*H0.88" ..OR.. L24*W24*H32"
        ..OR.. L30*W30*H30" ..OR.. 47" ..OR.. 117" ..OR.. 1*72" ..OR.. 120" ..OR..
        "L21*W4.88" ..OR.. L21*W4.88" ..OR.. L18.75*W4.88" ..OR.. L15.4*W4.88"'
    - - :warning
      - 'Line 47: Illegal quoting, probably in the following text: "85130-7-1.jpg
        ..OR.. 85130-7-4.jpg" ..OR.. W47"*H24"*D13" ..OR.. L16.5"*4.75"*H0.88" ..OR..
        L49*W16*H28" ..OR.. 29" ..OR.. 101" ..OR.. 1*72" ..OR.. 2*19.25" ..OR.. 120"'
    - - :warning
      - 'Line 48: Illegal quoting, probably in the following text: W26"*H36"*D26"
        ..OR.. D5.4*H0.88" ..OR.. L24*W24*H37" ..OR.. 39" ..OR.. 111" ..OR.. 1*72"
        ..OR.. 120" ..OR.. "L25*W4.75" ..OR.. L16.75*W4.75" ..OR.. L20*W4.75"'
    - - :warning
      - 'Line 49: Illegal quoting, probably in the following text: W20"*H32"*D20"
        ..OR.. D5.4*H0.88" ..OR.. L23*W23*H34" ..OR.. 34" ..OR.. 106" ..OR.. 1*72"
        ..OR.. 120"'
    - - :warning
      - 'Line 50: Illegal quoting, probably in the following text: W24"*H13"*D24"
        ..OR.. D5.88*H0.75" ..OR.. L23*W23*H16" ..OR.. 1*8.5" ..OR.. 7" ..OR.. L8.25*W3.25"'
    - - :warning
      - 'Line 51: Illegal quoting, probably in the following text: W7"*H15"*D5" ..OR..
        L15*W12*H12" ..OR.. L7.1*W4.75*H0.75" ..OR.. 7" ..OR.. "L7.6*W3.1" ..OR..
        L9.6*W3.1"'
    - - :warning
      - 'Line 52: Illegal quoting, probably in the following text: "85422-12-1.jpg
        ..OR.. 85422-12-3.jpg" ..OR.. W42"*H45"*D42" ..OR.. D5.88"*H1" ..OR.. L37*W37*H42"
        ..OR.. 49" ..OR.. 114.5" ..OR.. 1*72" ..OR.. 1*9+1*12" ..OR.. 120"'
    - - :warning
      - 'Line 53: Illegal quoting, probably in the following text: "85421-8-1.jpg
        ..OR.. 85421-8-3.jpg" ..OR.. W30"*H31"*D30" ..OR.. D5.88"*H1" ..OR.. L25*W25*H30"
        ..OR.. 35" ..OR.. 108.75" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120"'
    - - :warning
      - 'Line 54: Illegal quoting, probably in the following text: "85420-12-1.jpg
        ..OR.. 85420-12-5.jpg" ..OR.. W60"*H23"*D18" ..OR.. L21.5"*W4.75"*H0.75" ..OR..
        L55*W14*H23" ..OR.. 26" ..OR.. 99" ..OR.. 1*72" ..OR.. 2*12" ..OR.. 120"'
    - - :warning
      - 'Line 55: Illegal quoting, probably in the following text: "85424-1-1.jpg
        ..OR.. 85424-1-3.jpg" ..OR.. W9"*H13"*D9" ..OR.. D4.75"*H1" ..OR.. L15*W11*H14"
        ..OR.. 24" ..OR.. 59.5" ..OR.. 72"'
    - - :warning
      - 'Line 56: Illegal quoting, probably in the following text: "85425-5-1.jpg
        ..OR.. 85425-5-4.jpg" ..OR.. W28"*H10"*D28" ..OR.. D7.13"*H0.75" ..OR.. L23*W23*H11"
        ..OR.. 7"'
    - - :warning
      - 'Line 57: Illegal quoting, probably in the following text: "85426-4-1.jpg
        ..OR.. 85426-4-5.jpg" ..OR.. W25"*H5"*D5" ..OR.. L20*W9*H9" ..OR.. L13.75"*W5.13"*H0.75"
        ..OR.. 7"'
    - - :warning
      - 'Line 58: Illegal quoting, probably in the following text: "85427-6-1.jpg
        ..OR.. 85427-6-5.jpg" ..OR.. W35"*H6"*D5" ..OR.. L30*W9*H9" ..OR.. L13.75"*W5.13"*H0.75"
        ..OR.. 7"'
    - - :warning
      - 'Line 59: Illegal quoting, probably in the following text: "85423-1-1.jpg
        ..OR.. 85423-1-4.jpg" ..OR.. W11"*H20"*D5" ..OR.. L19*W10*H9" ..OR.. L12.38"*W5"*H1"
        ..OR.. 7"'
    - - :warning
      - 'Line 60: Illegal quoting, probably in the following text: "85202-16.jpg ..OR..
        85202-16_1.jpg" ..OR.. W36"*H48"*D36" ..OR.. D5.5*H1" ..OR.. L39*W39*H35"
        ..OR.. L31*W19*H16" ..OR.. 51" ..OR.. 125" ..OR.. 2*72" ..OR.. 120" ..OR..
        "L11.8*W6" ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 61: Illegal quoting, probably in the following text: "85207-9.jpg ..OR..
        85207-9-2.jpg" ..OR.. W24"*H36"*D24" ..OR.. D5.5"*H1" ..OR.. L28*W28*H30"
        ..OR.. 40" ..OR.. 112" ..OR.. 1*72" ..OR.. 120" ..OR.. L11.75*W5.88"+L9.63*W4.75"+L6.5*W4.88"'
    - - :warning
      - 'Line 62: Illegal quoting, probably in the following text: W30"*H24"*D30"
        ..OR.. D5.5*H1" ..OR.. L31*W31*H30" ..OR.. 30" ..OR.. 103" ..OR.. 1*72" ..OR..
        120" ..OR.. "L11.8*W6" ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 63: Illegal quoting, probably in the following text: "85203-6.jpg ..OR..
        85203-6_1.jpg" ..OR.. W53"*H22"*D10" ..OR.. L15*W4.4*H0.75" ..OR.. L54*W13*H14"
        ..OR.. 26" ..OR.. 98" ..OR.. 1*72" ..OR.. 120" ..OR.. "L11.8*W6" ..OR.. L9.6*W4.75"
        ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 64: Illegal quoting, probably in the following text: "85200-6-1.jpg
        ..OR.. 85200-6-3.jpg" ..OR.. W24"*H21"*D24" ..OR.. D5.5"*H1" ..OR.. L26*W26*H16"
        ..OR.. 24" ..OR.. 96" ..OR.. 1*72" ..OR.. 120" ..OR.. L11.75*W5.88"+L9.63*W4.75"+L6.5*W4.88"'
    - - :warning
      - 'Line 65: Illegal quoting, probably in the following text: "85206-4-1.jpg
        ..OR.. 85206-4-4.jpg" ..OR.. W29"*H10"*D6" ..OR.. L41*W31*H8" ..OR.. L25.63"*W4.75"*H1"
        ..OR.. 7" ..OR.. L9.63*W4.75" L7.63*W4.25" L6.13*W3.88"'
    - - :warning
      - 'Line 66: Illegal quoting, probably in the following text: "85205-2-1.jpg
        ..OR.. 85205-2-5.jpg" ..OR.. W21"*H10"*D6" ..OR.. L15*W23*H8" ..OR.. L17.75"*W4.75"*H1"
        ..OR.. 7" ..OR.. L9.63*W4.75" L7.63*W4.25" L6.13*W3.88"'
    - - :warning
      - 'Line 67: Illegal quoting, probably in the following text: W6"*H12"*D4" ..OR..
        L16*W10*H9" ..OR.. L6*W4.5*H0.63" ..OR.. 23" ..OR.. 90" ..OR.. 7" ..OR.. "L11.8*W6"
        ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 68: Illegal quoting, probably in the following text: "85412-17-1.jpg
        ..OR.. 85412-17-5.jpg" ..OR.. W39"*H23"*D39" ..OR.. D5.88"*H0.75" ..OR.. L42.5*W42.5*H22"
        ..OR.. L42.25*W31.5*H24.5" ..OR.. 33" ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72"
        ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 69: Illegal quoting, probably in the following text: "85512-17-1.jpg
        ..OR.. 85512-17-5.jpg" ..OR.. W39"*H23"*D39" ..OR.. D5.88"*H0.75" ..OR.. L42.5*W42.5*H22"
        ..OR.. L42.25*W31.5*H24.5" ..OR.. 33" ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72"
        ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 70: Illegal quoting, probably in the following text: W39"*H23"*D39"
        ..OR.. D5.5"*H0.75" ..OR.. L42.5*42.5*22" ..OR.. L31.5*W42.25*H24.5" ..OR..
        33" ..OR.. 84" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 71: Illegal quoting, probably in the following text: "85414-20-1.jpg
        ..OR.. 85414-20-5.jpg" ..OR.. W31"*H35"*D31" ..OR.. D5.88"*H0.75" ..OR.. L34*W34*H35"
        ..OR.. L42*W29*H25" ..OR.. 14" ..OR.. 80" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 72: Illegal quoting, probably in the following text: "85514-20-1.jpg
        ..OR.. 85514-20-6.jpg" ..OR.. W31"*H35"*D31" ..OR.. D5.88"*H0.75" ..OR.. L34*W34*H35"
        ..OR.. L42*W29*H25" ..OR.. 14" ..OR.. 80" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 73: Illegal quoting, probably in the following text: W31"*H35"*D31"
        ..OR.. D6*H0.75" ..OR.. L34*W34*H35" ..OR.. L29*W42*H25" ..OR.. 43.75" ..OR..
        94" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 74: Illegal quoting, probably in the following text: "85411-13-1.jpg
        ..OR.. 85411-13-5.jpg" ..OR.. W31"*H19"*D31" ..OR.. D5.5"*H0.75" ..OR.. L33*W33*H28"
        ..OR.. 29" ..OR.. 65" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 75: Illegal quoting, probably in the following text: "85511-13-1.jpg
        ..OR.. 85511-13-6.jpg" ..OR.. W31"*H19"*D31" ..OR.. D5.5"*H0.75" ..OR.. L33*W33*H28"
        ..OR.. 29" ..OR.. 65" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 76: Illegal quoting, probably in the following text: "85621-13-1.jpg
        ..OR.. 85621-13-4.jpg" ..OR.. W31"*H19"*D31" ..OR.. D5.25"*H0.75" ..OR.. L33.5*W33.5*H27.75"
        ..OR.. 18.5" ..OR.. 64.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75
        xW4.25 xH1.25"'
    - - :warning
      - 'Line 77: Illegal quoting, probably in the following text: "85410-7-1.jpg
        ..OR.. 85410-7-6.jpg" ..OR.. W26"*H17"*D26" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H27"
        ..OR.. 27" ..OR.. 63" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 78: Illegal quoting, probably in the following text: "85510-7-1.jpg
        ..OR.. 85510-7-5.jpg" ..OR.. W26"*H17"*D26" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H27"
        ..OR.. 27" ..OR.. 63" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 79: Illegal quoting, probably in the following text: "85620-7-1.jpg
        ..OR.. 85620-7-2.jpg" ..OR.. W26"*H17"*D26" ..OR.. D5.25"*H0.75" ..OR.. L27.75*W27.75*H27.25"
        ..OR.. 27" ..OR.. 63" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25
        xH1.25"'
    - - :warning
      - 'Line 80: Illegal quoting, probably in the following text: "85413-6-1.jpg
        ..OR.. 85413-6-4.jpg" ..OR.. W47"*H11"*D15" ..OR.. L15.75"*W5.13"*H1" ..OR..
        L50*W18*H23" ..OR.. 18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 81: Illegal quoting, probably in the following text: "85513-6-1.jpg
        ..OR.. 85513-6-5.jpg" ..OR.. W47"*H11"*D15" ..OR.. L15.75"*W5.13"*H1" ..OR..
        L50*W18*H23" ..OR.. 18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 82: Illegal quoting, probably in the following text: W47"*H11"*D15"
        ..OR.. D15.75" xH5.25" ..OR.. L17.75*W50.5*H23.25" ..OR.. L15.75*W5.25*H1"
        ..OR.. 18.25" ..OR.. 69" ..OR.. 2*3"+2*6"+8*12" ..OR.. 120" ..OR.. L8.75 xW4.25
        xH1.25"'
    - - :warning
      - 'Line 83: Illegal quoting, probably in the following text: "85415-2-1.jpg
        ..OR.. 85415-2-3.jpg" ..OR.. W15"*H11"*D8" ..OR.. L22*W16*H17" ..OR.. L6.25"*W5.88"*H0.75"
        ..OR.. 7" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 84: Illegal quoting, probably in the following text: "85515-2-1.jpg
        ..OR.. 85515-2-3.jpg" ..OR.. W15"*H11"*D8" ..OR.. L22*W16*H17" ..OR.. L6.25"*W5.88"*H0.75"
        ..OR.. 7" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 85: Illegal quoting, probably in the following text: W15"*H11"*D8" ..OR..
        L15.75*W21.75*H16.5" ..OR.. D6xH6.25" ..OR.. 7" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 86: Illegal quoting, probably in the following text: W34"*H37"*D34"
        ..OR.. D5.5*H1" ..OR.. L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR..
        75" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 87: Illegal quoting, probably in the following text: W34"*H37"*D34"
        ..OR.. D5.5*H1" ..OR.. L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR..
        75" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 88: Illegal quoting, probably in the following text: W34"*H37"*D34"
        ..OR.. D5.5*H1" ..OR.. L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR..
        75.25" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 89: Illegal quoting, probably in the following text: W23"*H29"*D23"
        ..OR.. D5.5*H1" ..OR.. L30*W29*H24" ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 90: Illegal quoting, probably in the following text: "85262-13.jpg ..OR..
        85262-13_1.jpg" ..OR.. W23"*H29"*D23" ..OR.. D5.5*H1" ..OR.. L30*W29*H24"
        ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 91: Illegal quoting, probably in the following text: W23"*H29"*D23"
        ..OR.. D5.5*H1" ..OR.. L30*W29*H24" ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 92: Illegal quoting, probably in the following text: "85161-5.jpg ..OR..
        85161-5_1.jpg" ..OR.. W17"*H20"*D17" ..OR.. D5.5*H1" ..OR.. L23*W20*H23" ..OR..
        28" ..OR.. 64" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 93: Illegal quoting, probably in the following text: W17"*H20"*D17"
        ..OR.. D5.5*H1" ..OR.. L23*W20*H23" ..OR.. 28" ..OR.. 64" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 94: Illegal quoting, probably in the following text: W17"*H20"*D17"
        ..OR.. D5.5*H1" ..OR.. L23*W20*H23" ..OR.. 28" ..OR.. 64" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 95: Illegal quoting, probably in the following text: W12"*H13"*D7" ..OR..
        L18*W13*H16" ..OR.. L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 96: Illegal quoting, probably in the following text: W12"*H13"*D7" ..OR..
        L18*W13*H16" ..OR.. L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 97: Illegal quoting, probably in the following text: W12"*H13"*D7" ..OR..
        L18*W13*H16" ..OR.. L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 98: Illegal quoting, probably in the following text: "85433-12-1.jpg
        ..OR.. 85433-12-3.jpg" ..OR.. W52"*H52"*D52" ..OR.. D5.88*H0.75" ..OR.. L29*W29*H12"
        ..OR.. 58" ..OR.. 126" ..OR.. 1*72" ..OR.. 144"'
    - - :warning
      - 'Line 99: Illegal quoting, probably in the following text: "85432-8-1.jpg
        ..OR.. 85432-8-3.jpg" ..OR.. W38"*H38"*D38" ..OR.. D5.13*H0.75" ..OR.. L56*W56*H14"
        ..OR.. 44" ..OR.. 112" ..OR.. 1*72" ..OR.. 144"'
    - - :warning
      - 'Line 100: Illegal quoting, probably in the following text: "85431-6-1.jpg
        ..OR.. 85431-6-3.jpg" ..OR.. W28"*H30"*D28" ..OR.. D5.13*H0.75" ..OR.. L41*W41*H12"
        ..OR.. 36" ..OR.. 104" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 101: Illegal quoting, probably in the following text: "85430-4-1.jpg
        ..OR.. 85430-4-3.jpg" ..OR.. W16"*H15"*D16" ..OR.. D4.75*H0.75" ..OR.. L31*W31*H10"
        ..OR.. 21" ..OR.. 89" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 102: Illegal quoting, probably in the following text: "85435-8-1.jpg
        ..OR.. 85435-8-5.jpg" ..OR.. W34"*H10"*D34" ..OR.. D5.13*H0.75" ..OR.. L10*W16*H11"
        ..OR.. 18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 103: Illegal quoting, probably in the following text: "85434-6-1.jpg
        ..OR.. 85434-6-4.jpg" ..OR.. W26"*H8"*D26" ..OR.. D5.13*H0.75" ..OR.. L37*W37*H13"
        ..OR.. 16" ..OR.. 53" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 104: Illegal quoting, probably in the following text: "85437-3-1.jpg
        ..OR.. 85437-3-5.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5.13*H0.75" ..OR.. L11*W15*H7"
        ..OR.. 7"'
    - - :warning
      - 'Line 105: Illegal quoting, probably in the following text: "85436-1-1.jpg
        ..OR.. 85436-1-4.jpg" ..OR.. W7"*H9"*D7" ..OR.. D5.13*H0.75" ..OR.. L19*W19*H12"
        ..OR.. 17" ..OR.. 53" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 106: Illegal quoting, probably in the following text: "85438-1-1.jpg
        ..OR.. 85438-1-4.jpg" ..OR.. W8"*H12"*D5" ..OR.. L14.5*W10.75*H7.5" ..OR..
        L9"*4.75"*H0.75" ..OR.. 7"'
    - - :warning
      - 'Line 107: Illegal quoting, probably in the following text: "85232-12.jpg
        ..OR.. 85232-12_1.jpg" ..OR.. W26"*H39"*D26" ..OR.. D5.5*H1" ..OR.. L30*W30*H14"
        ..OR.. 42" ..OR.. 115" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 108: Illegal quoting, probably in the following text: W48"*H24"*D15"
        ..OR.. L16.1*W5.88*H0.88" ..OR.. L50*W22*H11" ..OR.. 27" ..OR.. 100" ..OR..
        2*72" ..OR.. 2*15" ..OR.. 120" ..OR.. L47.25*W14.25*H8.25"'
    - - :warning
      - 'Line 109: Illegal quoting, probably in the following text: W27"*H25"*D27"
        ..OR.. D5.5*H1" ..OR.. L30*W30*H25" ..OR.. 28" ..OR.. 101" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 110: Illegal quoting, probably in the following text: W23"*H27"*D23"
        ..OR.. D5.5*H1" ..OR.. L26*W26*H15" ..OR.. 30" ..OR.. 103" ..OR.. 1*72" ..OR..
        120" ..OR.. D23*H8"'
    - - :warning
      - 'Line 111: Illegal quoting, probably in the following text: W15"*H12"*D15"
        ..OR.. D5.5*H1" ..OR.. L18*W18*H15" ..OR.. 1*3.25" ..OR.. 7" ..OR.. D15*H7"'
    - - :warning
      - 'Line 112: Illegal quoting, probably in the following text: W7"*H9.5"*D7"
        ..OR.. D5.5*H1" ..OR.. L16*W12*H10" ..OR.. 20" ..OR.. 56" ..OR.. 1*6"+3*12"
        ..OR.. 120"'
    - - :warning
      - 'Line 113: Illegal quoting, probably in the following text: W36"*H6"*D6" ..OR..
        L39*W9*H9" ..OR.. L35.38*W4.5*H0.75" ..OR.. 7" ..OR.. L36*W4.8*H5.88"'
    - - :warning
      - 'Line 114: Illegal quoting, probably in the following text: W25"*H6"*D5" ..OR..
        L28*W9*H9" ..OR.. L24.38*W4.5*H0.75" ..OR.. 7" ..OR.. L25*W4.8*H4.38"'
    - - :warning
      - 'Line 115: Illegal quoting, probably in the following text: W8"*H9"*D5" ..OR..
        L11*W10*H8" ..OR.. L6.5*W6.5*H0.75" ..OR.. 7" ..OR.. L8.38*W7.25*H4"'
    - - :warning
      - 'Line 116: Illegal quoting, probably in the following text: W37"*H58"*D37"
        ..OR.. D5.1*H0.75" ..OR.. L43*W40*H13" ..OR.. 67" ..OR.. 103" ..OR.. 120"
        ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 117: Illegal quoting, probably in the following text: "85244-7.jpg ..OR..
        85244-7_1.jpg" ..OR.. W26"*H46"*D26" ..OR.. D23.63*H1" ..OR.. L28*W26*H18"
        ..OR.. 52" ..OR.. 97" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 118: Illegal quoting, probably in the following text: "85242-6.jpg ..OR..
        85242-6_1.jpg" ..OR.. W24"*H45"*D24" ..OR.. D5.1*H0.75" ..OR.. L32*W27*H13"
        ..OR.. 53" ..OR.. 89" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 119: Illegal quoting, probably in the following text: W50"*H23"*D5"
        ..OR.. L50.38*W8.75*H0.75" ..OR.. L54*W15*H13" ..OR.. 32" ..OR.. 97" ..OR..
        120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 120: Illegal quoting, probably in the following text: W20"*H37"*D20"
        ..OR.. D5.1*H0.75" ..OR.. L26*W22*H18" ..OR.. 45" ..OR.. 81" ..OR.. 120" ..OR..
        D3.25*L20.75"'
    - - :warning
      - 'Line 121: Illegal quoting, probably in the following text: W5"*H23"*D5" ..OR..
        D5.1*H0.75" ..OR.. L24*W15*H8" ..OR.. 31" ..OR.. 67" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 122: Illegal quoting, probably in the following text: W6"*H32"*D7" ..OR..
        L35*W13*H10" ..OR.. 7" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 123: Illegal quoting, probably in the following text: "85286-68-1.jpg
        ..OR.. 85286-68-3.jpg" ..OR.. W20"*H54"*D20" ..OR.. D20"*H1.38" ..OR.. L24*W24*H31"
        ..OR.. 20" ..OR.. D3.88"'
    - - :warning
      - 'Line 124: Illegal quoting, probably in the following text: "85283-47-1.jpg
        ..OR.. 85283-47-4.jpg" ..OR.. W20"*H40"*D20" ..OR.. D20"*H1.38" ..OR.. L24*W24*H16"
        ..OR.. 20" ..OR.. D3.88"'
    - - :warning
      - 'Line 125: Illegal quoting, probably in the following text: "85281-19-1.jpg
        ..OR.. 85281-19-4.jpg" ..OR.. W20"*H20"*D20" ..OR.. D20"*H1.38" ..OR.. L24*W24*H16"
        ..OR.. 20" ..OR.. D3.88"'
    - - :warning
      - 'Line 126: Illegal quoting, probably in the following text: "85289-5-1.jpg
        ..OR.. 85289-5-4.jpg" ..OR.. W6"*H25"*D7" ..OR.. L8*W12*H20" ..OR.. L8.63"*W5.75"*H1.38"
        ..OR.. 7" ..OR.. D3.88"'
    - - :warning
      - 'Line 127: Illegal quoting, probably in the following text: "85288-3-1.jpg
        ..OR.. 85288-3-5.jpg" ..OR.. W6"*H15"*D7" ..OR.. L8*W12*H15" ..OR.. L8.63"*W5.75"*H1.38"
        ..OR.. 7" ..OR.. D3.88"'
    - - :warning
      - 'Line 128: Illegal quoting, probably in the following text: "85216-14.jpg
        ..OR.. 85216-14_1.jpg" ..OR.. W50"*H14"*D10" ..OR.. L50.5*W9.88*H1.38" ..OR..
        L54*W13*H15" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 129: Illegal quoting, probably in the following text: "85214-13.jpg
        ..OR.. 85214-13_1.jpg" ..OR.. W24"*H14"*D24" ..OR.. D24*H1.38" ..OR.. L35*W27*H9"
        ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 130: Illegal quoting, probably in the following text: W36"*H14"*D10"
        ..OR.. L36*W9.88*H1.38" ..OR.. L39*W13*H15" ..OR.. 23" ..OR.. 90" ..OR.. 120"
        ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 131: Illegal quoting, probably in the following text: "85213-6.jpg ..OR..
        85213-6_1.jpg" ..OR.. W16"*H14"*D16" ..OR.. D16*H1.38" ..OR.. L26*W19*H9"
        ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 132: Illegal quoting, probably in the following text: W10"*H14"*D10"
        ..OR.. D9.88*H1.25" ..OR.. L16*W15*H9" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR..
        D3.5*L12"'
    - - :warning
      - 'Line 133: Illegal quoting, probably in the following text: W6"*H14"*D6" ..OR..
        D5.88*H1.25" ..OR.. L15*W9*H9" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 134: Illegal quoting, probably in the following text: "85401-9-1.jpg
        ..OR.. 85401-9-3.jpg" ..OR.. W24"*H7"*D24" ..OR.. D24*1.38" ..OR.. L28*W28*H15"
        ..OR.. 51" ..OR.. 75" ..OR.. 1*5.25+31*32+1*7.38+1*1.38+1*8.63+1*10.13+1*6+1*8.75"
        ..OR.. 7" ..OR.. D4"'
    - - :warning
      - 'Line 135: Illegal quoting, probably in the following text: "85400-5-1.jpg
        ..OR.. 85400-5-3.jpg" ..OR.. W16"*H7"*D16" ..OR.. D15.75"*1.38" ..OR.. L20*W20*H15"
        ..OR.. 42" ..OR.. 66" ..OR.. 1*9"+15*12"+1*1.38"+1*6"+1*10.38"+1*3" ..OR..
        7" ..OR.. D4"'
    - - :warning
      - 'Line 136: Illegal quoting, probably in the following text: "85404-5-1.jpg
        ..OR.. 85404-5-5.jpg" ..OR.. W43"*H7"*D6" ..OR.. L43.25"*W6.25"*H1.38" ..OR..
        L10*W47*H15" ..OR.. 21" ..OR.. 57" ..OR.. 7*6+15*12" ..OR.. 7" ..OR.. D4"'
    - - :warning
      - 'Line 137: Illegal quoting, probably in the following text: "85406-1-1.jpg
        ..OR.. 85406-1-4.jpg" ..OR.. W6"*H7"*D4" ..OR.. D5.5"*H1.25" ..OR.. L9*W17*H8"
        ..OR.. 15" ..OR.. 51" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D4"'
    - - :warning
      - 'Line 138: Illegal quoting, probably in the following text: "85407-1-1.jpg
        ..OR.. 85407-1-5.jpg" ..OR.. W5"*H13"*D6" ..OR.. L13.13"*5.38"*1.25" ..OR..
        L11*W16*H9" ..OR.. 7" ..OR.. D4"'
    - - :warning
      - 'Line 139: Illegal quoting, probably in the following text: W36"*H34"*D36"
        ..OR.. 6.25"*1" ..OR.. L40*W40*H20" ..OR.. 41" ..OR.. 109" ..OR.. 1*72" ..OR..
        120" ..OR.. L13.75"*D1"'
    - - :warning
      - 'Line 140: Illegal quoting, probably in the following text: W45"*H26"*D12"
        ..OR.. L17.75"*W5"*H1" ..OR.. L17*W48*H18" ..OR.. 33" ..OR.. 100" ..OR.. 1*72"
        ..OR.. 120" ..OR.. L13.75"*D1"'
    - - :warning
      - 'Line 141: Illegal quoting, probably in the following text: "85101-8.jpg ..OR..
        85101-8_1.jpg" ..OR.. W30"*H26"*D30" ..OR.. D5.1*H0.75" ..OR.. L33*W33*H16"
        ..OR.. 29" ..OR.. 101" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 142: Illegal quoting, probably in the following text: W24"*H20"*D24"
        ..OR.. D5.1*H0.75" ..OR.. L27*W27*H14" ..OR.. 23" ..OR.. 95" ..OR.. 1*72"
        ..OR.. 1*8.7" ..OR.. 120" ..OR.. D1*H10.75"'
    - - :warning
      - 'Line 143: Illegal quoting, probably in the following text: W18"*H17"*D18"
        ..OR.. D5.1*H0.75" ..OR.. L21*W21*H14" ..OR.. 21" ..OR.. 92" ..OR.. 1*72"
        ..OR.. 1*6" ..OR.. 120" ..OR.. D1*H10.75"'
    - - :warning
      - 'Line 144: Illegal quoting, probably in the following text: "85109-4-1.jpg
        ..OR.. 85109-4-2.jpg" ..OR.. W21"*H12"*D21" ..OR.. D5"*D0.75" ..OR.. L25*W25*H10"
        ..OR.. 7" ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 145: Illegal quoting, probably in the following text: "85108-4-1.jpg
        ..OR.. 85108-4-5.jpg" ..OR.. W36"*H8"*D5" ..OR.. L10*W39*H13" ..OR.. L33"*W5"*H0.75"
        ..OR.. 7" ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 146: Illegal quoting, probably in the following text: "85107-3-1.jpg
        ..OR.. 85107-3-2.jpg" ..OR.. W26"*H8"*D5" ..OR.. L10*W30*H13" ..OR.. L23.5"*W5"*H0.75"
        ..OR.. 7" ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 147: Illegal quoting, probably in the following text: W9"*H26"*D9" ..OR..
        D5.1*H0.75" ..OR.. L20*W18*H11" ..OR.. 29" ..OR.. 101" ..OR.. 1*72" ..OR..
        1*12" ..OR.. 120" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 148: Illegal quoting, probably in the following text: "85106-1-1.jpg
        ..OR.. 85106-1-2.jpg" ..OR.. W7"*H20"*D5" ..OR.. L11*W23*H15" ..OR.. L15"*W4.25"*H0.75"
        ..OR.. 7" ..OR.. L19.25*D0.72"'
    - - :warning
      - 'Line 149: Illegal quoting, probably in the following text: W9"*H15"*D5" ..OR..
        L18*W12*H11" ..OR.. L8.25*W4.75*H0.75" ..OR.. 7" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 150: Illegal quoting, probably in the following text: "85171-12.jpg
        ..OR.. 85171-12_1.jpg" ..OR.. W32"*H12"*D32" ..OR.. L35*W35*H15" ..OR.. 20"
        ..OR.. 83" ..OR.. 120" ..OR.. "L6.75*W1.5*H0.6" ..OR.. L8.3*W1.5*H0.6" ..OR..
        L10*W1.5*H0.6"'
    - - :warning
      - 'Line 151: Illegal quoting, probably in the following text: W50"*H13"*D4"
        ..OR.. L19.63*W5.5*H0.88" ..OR.. L53*W13*H15" ..OR.. 20" ..OR.. 83" ..OR..
        120" ..OR.. "L6.75*W1.5*H0.6" ..OR.. L8.3*W1.5*H0.6" ..OR.. L10*W1.5*H0.6"'
    - - :warning
      - 'Line 152: Illegal quoting, probably in the following text: W10"*H12"*D5"
        ..OR.. L15*W12*H11" ..OR.. L11.75*W9.4*H0.75" ..OR.. 7" ..OR.. "L6.75*W1.5*H0.6"
        ..OR.. L8.3*W1.5*H0.6" ..OR.. L10*W1.5*H0.6"'
    - - :warning
      - 'Line 153: Illegal quoting, probably in the following text: W57"*H26"*D30"
        ..OR.. D7*H1.5" ..OR.. L60*W30*H27" ..OR.. 34" ..OR.. 70" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 154: Illegal quoting, probably in the following text: "85182-9.jpg ..OR..
        85182-9_1.jpg" ..OR.. W37"*H30"*D37" ..OR.. D7*H1.5" ..OR.. L35*W35*H28" ..OR..
        33" ..OR.. 105" ..OR.. 1*72" ..OR.. 120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 155: Illegal quoting, probably in the following text: W21"*H34"*D21"
        ..OR.. D7*H1.5" ..OR.. L32*W26*H17" ..OR.. 36" ..OR.. 109" ..OR.. 1*72" ..OR..
        120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 156: Illegal quoting, probably in the following text: W6"*H14"*D10"
        ..OR.. L18*W13*H9" ..OR.. D6*H1.5" ..OR.. 7" ..OR.. D6*H6"'
    - - :warning
      - 'Line 157: Illegal quoting, probably in the following text: "85270-12-1.jpg
        ..OR.. 85270-12-3.jpg" ..OR.. W32"*H40"*D32" ..OR.. L35*W35*H40" ..OR.. L34*26*15"
        ..OR.. 49" ..OR.. 85" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D9.88"+D7.88"'
    - - :warning
      - 'Line 158: Illegal quoting, probably in the following text: "85370-12-1.jpg
        ..OR.. 85370-12-4.jpg" ..OR.. W32"*H40"*D32" ..OR.. L35*W35*H40" ..OR.. L34*26*15"
        ..OR.. 49" ..OR.. 85" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D9.88"+D7.88"'
    - - :warning
      - 'Line 159: Illegal quoting, probably in the following text: "85271-12-1.jpg
        ..OR.. 85271-12-51.jpg" ..OR.. W25"*H34"*D25" ..OR.. D5.13"*H0.75" ..OR..
        L28*W28*H30.5" ..OR.. L28*W18*H21" ..OR.. 43" ..OR.. 79" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. D5.88"+D7.13"'
    - - :warning
      - 'Line 160: Illegal quoting, probably in the following text: "85371-12-1.jpg
        ..OR.. 85371-12-4.jpg" ..OR.. W25"*H34"*D25" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H30.5"
        ..OR.. L28*W18*H21" ..OR.. 43" ..OR.. 79" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        D5.88"+D7.13"'
    - - :warning
      - 'Line 161: Illegal quoting, probably in the following text: "85273-8-1.jpg
        ..OR.. 85273-8-4.jpg" ..OR.. W56"*H25"*D18" ..OR.. L27.13"*W5.13"*H1" ..OR..
        L59*W23.5*H22" ..OR.. L26*W26*H20" ..OR.. 33" ..OR.. 70" ..OR.. 2*6+6*12"
        ..OR.. 72" ..OR.. D7.88"+D9.88"'
    - - :warning
      - 'Line 162: Illegal quoting, probably in the following text: "85373-8-1.jpg
        ..OR.. 85373-8-1.jpg" ..OR.. W56"*H25"*D18" ..OR.. L27.13"*W5.13"*H1" ..OR..
        L59*W23.5*H22" ..OR.. L26*W26*H20" ..OR.. 33" ..OR.. 70" ..OR.. 2*6+6*12"
        ..OR.. 72" ..OR.. D7.88"+D9.88"'
    - - :warning
      - 'Line 163: Illegal quoting, probably in the following text: W14"*H19"*D14"
        ..OR.. D5.13"*H0.75" ..OR.. L20*W25*H18" ..OR.. 28" ..OR.. 64" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. D13.75"'
    - - :warning
      - 'Line 164: Illegal quoting, probably in the following text: "85376-1-1.jpg
        ..OR.. 85376-1-3.jpg" ..OR.. W14"*H19"*D14" ..OR.. D5.13"*H0.75" ..OR.. L20*W25*H18"
        ..OR.. 28" ..OR.. 64" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D13.75"'
    - - :warning
      - 'Line 165: Illegal quoting, probably in the following text: W10"*H14"*D10"
        ..OR.. D5.13"*H0.75" ..OR.. L18*W21*H14" ..OR.. 24" ..OR.. 60" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. D9.88"'
    - - :warning
      - 'Line 166: Illegal quoting, probably in the following text: "85375-1-1.jpg
        ..OR.. 85375-1-2.jpg" ..OR.. W10"*H14"*D10" ..OR.. D5.13"*H0.75" ..OR.. L18*W21*H14"
        ..OR.. 24" ..OR.. 60" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D9.88"'
    - - :warning
      - 'Line 167: Illegal quoting, probably in the following text: W38"*H38"*D38"
        ..OR.. D6.4*H1.88" ..OR.. L41*W41*H40" ..OR.. L32*W24*H24" ..OR.. L32*W24*H24"
        ..OR.. 48" ..OR.. 72" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D10*H1.5"'
    - - :warning
      - 'Line 168: Illegal quoting, probably in the following text: "85122-12.jpg
        ..OR.. 85122-12_1.jpg" ..OR.. W26"*H26"*D26" ..OR.. D6.4*H1.88" ..OR.. L31*W31*H31"
        ..OR.. L30*W24*H24" ..OR.. 36" ..OR.. 66" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR..
        D10*H1.5"'
    - - :warning
      - 'Line 169: Illegal quoting, probably in the following text: "85123-6.jpg ..OR..
        85123-6_1.jpg" ..OR.. W24"*H18"*D24" ..OR.. D6.4*H1.88" ..OR.. L28*W26*H26"
        ..OR.. 1*6" ..OR.. 7" ..OR.. D10*H1.5"'
    - - :warning
      - 'Line 170: Illegal quoting, probably in the following text: "85124-8-1.jpg
        ..OR.. 85124-8-5.jpg" ..OR.. W58"*H10"*D13" ..OR.. L16.88"*W5.88"*H0.88" ..OR..
        L54*W14*H16" ..OR.. 13" ..OR.. 49" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. D9.63"*1.63"'
    - - :warning
      - 'Line 171: Illegal quoting, probably in the following text: "85125-3-1.jpg
        ..OR.. 85125-3-2.jpg" ..OR.. W15"*H27"*D6" ..OR.. L24*W15*H13" ..OR.. D4.75"*H0.75"
        ..OR.. 7" ..OR.. D9.63"*1.63"'
    - - :warning
      - 'Line 172: Illegal quoting, probably in the following text: W24"*H27"*D24"
        ..OR.. D5.88*H0.88" ..OR.. L28*W28*H29" ..OR.. 36" ..OR.. 72" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D23.75*H23.75"'
    - - :warning
      - 'Line 173: Illegal quoting, probably in the following text: W16"*H19"*D16"
        ..OR.. D5.88*H0.88" ..OR.. L19.5*W19.5*H20.75" ..OR.. 29" ..OR.. 65" ..OR..
        1*6"+3*12" ..OR.. 120" ..OR.. D15.75*H15.75"'
    - - :warning
      - 'Line 174: Illegal quoting, probably in the following text: "85221-1.jpg ..OR..
        85221-1_1.jpg" ..OR.. W8"*H10"*D8" ..OR.. D5.88*H0.88" ..OR.. L11*W11*H13"
        ..OR.. 20" ..OR.. 56" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D7.5*H7.5"'
    - - :warning
      - 'Line 175: Illegal quoting, probably in the following text: W41"*H31"*D41"
        ..OR.. D5.5*H1" ..OR.. L43*W43*H9" ..OR.. 34" ..OR.. 106" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 176: Illegal quoting, probably in the following text: W29"*H27"*D29"
        ..OR.. D5.5*H1" ..OR.. L32*W32*H9" ..OR.. 32" ..OR.. 102" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 177: Illegal quoting, probably in the following text: W6"*H18"*D4" ..OR..
        L21*W8*H7" ..OR.. L18*W5.75*H1.25" ..OR.. 7"'
    - - :warning
      - 'Line 178: Illegal quoting, probably in the following text: "85111-6.jpg ..OR..
        85111-6_1.jpg" ..OR.. W36"*H18"*D36" ..OR.. D5.1*H0.75" ..OR.. L40*W40*H22"
        ..OR.. 32" ..OR.. 80" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D36*H18"'
    - - :warning
      - 'Line 179: Illegal quoting, probably in the following text: W24"*H12"*D24"
        ..OR.. D5.1*H0.75" ..OR.. L28*W28*H16" ..OR.. 32" ..OR.. 74" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D24*H12"'
    - - :warning
      - 'Line 180: Illegal quoting, probably in the following text: W16"*H16"*D16"
        ..OR.. D5.1*H0.75" ..OR.. L19*W19*H19" ..OR.. 30" ..OR.. 73" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D16*H15.5"'
    - - :warning
      - 'Line 181: Illegal quoting, probably in the following text: W36"*H21"*D36"
        ..OR.. D5.5*H1" ..OR.. L39*W39*H13" ..OR.. 24" ..OR.. 96" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 182: Illegal quoting, probably in the following text: "85141-6.jpg ..OR..
        85141-6_1.jpg" ..OR.. W27"*H18"*D27" ..OR.. D5.5*H1" ..OR.. L30*W30*H12" ..OR..
        21" ..OR.. 93" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 183: Illegal quoting, probably in the following text: W14"*H21"*D14"
        ..OR.. D5.5*H1" ..OR.. L18*W18*H30" ..OR.. 24" ..OR.. 96" ..OR.. "Iron ..OR..
        solid wood and glass" ..OR.. 1*72" ..OR.. 120" ..OR.. L11.6*W10*H3"'
    - - :warning
      - 'Line 184: Illegal quoting, probably in the following text: "65000-1.jpg ..OR..
        65000-6.jpg" ..OR.. W5"*H19"*D3" ..OR.. W4.72"*H18"'
    - - :warning
      - 'Line 185: Illegal quoting, probably in the following text: "65001-1.jpg ..OR..
        65001-7.jpg" ..OR.. W5"*H24"*D3" ..OR.. W4.72"*H24.7"'
    - - :warning
      - 'Line 186: Illegal quoting, probably in the following text: "65060-1.jpg ..OR..
        65060-5.jpg" ..OR.. W6"*H18"*D3"'
    - - :warning
      - 'Line 187: Illegal quoting, probably in the following text: "65061-1.jpg ..OR..
        65061-5.jpg" ..OR.. W6"*H27"*D3"'
    - - :warning
      - 'Line 188: Illegal quoting, probably in the following text: "65030-1.jpg ..OR..
        65030-4.jpg" ..OR.. W7"*H14"*D4" ..OR.. W7"*H14.37"'
    - - :warning
      - 'Line 189: Illegal quoting, probably in the following text: "65031-1.jpg ..OR..
        65031-4.jpg" ..OR.. W7"*H24"*D4" ..OR.. W7"*H24"'
    - - :warning
      - 'Line 190: Illegal quoting, probably in the following text: "65040-1.jpg ..OR..
        65040-5.jpg" ..OR.. W6"*H16"*D3" ..OR.. "Stainless steel ..OR..  aluminium
        and crystal"'
    - - :warning
      - 'Line 191: Illegal quoting, probably in the following text: "65041-1.jpg ..OR..
        65041-5.jpg" ..OR.. W6"*H24"*D3" ..OR.. "Stainless steel ..OR..  aluminium
        and crystal"'
    - - :warning
      - 'Line 192: Illegal quoting, probably in the following text: "65010-1.jpg ..OR..
        65010-5.jpg" ..OR.. W6"*H11"*D3" ..OR.. W4.72"*H4.3"'
    - - :warning
      - 'Line 193: Illegal quoting, probably in the following text: "65011-1.jpg ..OR..
        65011-5.jpg" ..OR.. W6"*H15"*D3" ..OR.. W4.72"*H4.3"'
    - - :warning
      - 'Line 194: Illegal quoting, probably in the following text: "65050-1.jpg ..OR..
        65050-5.jpg" ..OR.. W7"*H14"*D2"'
    - - :warning
      - 'Line 195: Illegal quoting, probably in the following text: "65051-1.jpg ..OR..
        65051-4.jpg" ..OR.. W7"*H18"*D2"'
    - - :warning
      - 'Line 196: Illegal quoting, probably in the following text: "65090-1.jpg ..OR..
        65090-4.jpg" ..OR.. W5"*H16"*D4"'
    - - :warning
      - 'Line 197: Illegal quoting, probably in the following text: "65091-1.jpg ..OR..
        65091-4.jpg" ..OR.. W5"*H24"*D4"'
 |
| 2026-06-16T06:56:10.198762 | ---
- - Products
  - - - :warning
      - 'Error running cleancsv: 2026/06/16 06:56:09 parse error on line 2, column
        122: bare " in non-quoted-field

        '
    - - :warning
      - 'Line 2: Illegal quoting, probably in the following text: "86010-1-1.jpg ..OR..
        86010-1-4.jpg" ..OR.. W9"*H16"*D9" ..OR.. L16.25*W14.5*H10.75" ..OR.. D5*H1.25"
        ..OR.. 7" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 3: Illegal quoting, probably in the following text: "86120-1-1.jpg ..OR..
        86120-1-5.jpg" ..OR.. W9"*H16"*D9" ..OR.. L16.25*W14.5*H10.75" ..OR.. D5*H1.25"
        ..OR.. 7" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 4: Illegal quoting, probably in the following text: "86013-1-1.jpg ..OR..
        86013-1-2.jpg" ..OR.. W9"*H10"*D9" ..OR.. D5*H1.25" ..OR.. L16.5*W16.5*H10.75"
        ..OR.. 17.5" ..OR.. 71" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 5: Illegal quoting, probably in the following text: "86123-1-1.jpg ..OR..
        86123-1-3.jpg" ..OR.. W9"*H10"*D9" ..OR.. D5*H1.25" ..OR.. L16.5*W16.5*H10.75"
        ..OR.. 17.5" ..OR.. 71" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 6: Illegal quoting, probably in the following text: "86011-2-1.jpg ..OR..
        86011-2-5.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 15.5" ..OR.. 70" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 7: Illegal quoting, probably in the following text: "86121-2-1.jpg ..OR..
        86121-2-5.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 15.5" ..OR.. 70" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 8: Illegal quoting, probably in the following text: "86015-1-1.jpg ..OR..
        86015-1-3.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 18" ..OR.. 72" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 9: Illegal quoting, probably in the following text: "86125-1-1.jpg ..OR..
        86125-1-2.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 18" ..OR.. 72" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 10: Illegal quoting, probably in the following text: "86014-6-1.jpg
        ..OR.. 86014-6-5.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 21" ..OR.. 74" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 11: Illegal quoting, probably in the following text: "86124-6-1.jpg
        ..OR.. 86124-6-5.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 21" ..OR.. 74" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 12: Illegal quoting, probably in the following text: "86017-6-1.jpg
        ..OR.. 86017-6-2.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 25" ..OR.. 79" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 13: Illegal quoting, probably in the following text: "86127-6-1.jpg
        ..OR.. 86127-6-2.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 25" ..OR.. 79" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 14: Illegal quoting, probably in the following text: "86001-1-1.jpg
        ..OR.. 86001-1-3.jpg" ..OR.. W8"*H12"*D8" ..OR.. D6"*H1" ..OR.. L20*W13*H14.25"
        ..OR.. 16.5" ..OR.. 70.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 15: Illegal quoting, probably in the following text: "86002-3-1.jpg
        ..OR.. 86002-3-3.jpg" ..OR.. W17"*Max86"*17" ..OR.. L16.75"*W15.75"*H1.5"
        ..OR.. L24.5*W23*H17.5" ..OR.. 37.75" ..OR.. 85.75" ..OR.. 1*3"+3*6"+14*12"
        ..OR.. 120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 16: Illegal quoting, probably in the following text: "86003-6-1.jpg
        ..OR.. 86003-6-3.jpg" ..OR.. W28"*Max86"*28" ..OR.. L28"*W26.75"*H1.5" ..OR..
        L30.5*W30.5*H17.5" ..OR.. 61.75" ..OR.. 85.75" ..OR.. 3*3"+4*6"+22*12" ..OR..
        120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 17: Illegal quoting, probably in the following text: "86031-3-1.jpg
        ..OR.. 86031-3-3.jpg" ..OR.. W10"*H20"*D10" ..OR.. D5*H1" ..OR.. L15.5*W16.5*H11.75"
        ..OR.. 25.5" ..OR.. 79.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 18: Illegal quoting, probably in the following text: "86036-3-1.jpg
        ..OR.. W15"*H35"*D6" ..OR.. L28.5*W11*H12.5" ..OR.. D5*H1" ..OR.. 7" ..OR..
        W3*H12"'
    - - :warning
      - 'Line 19: Illegal quoting, probably in the following text: "86032-24-1.jpg
        ..OR.. 86032-24-3.jpg" ..OR.. W36"*H26"*D36" ..OR.. D5*H1" ..OR.. L24.75*W21*H24.5"
        ..OR.. 29.25" ..OR.. 102.5" ..OR.. 72" ..OR.. 1*12" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 20: Illegal quoting, probably in the following text: "86033-16-1.jpg
        ..OR.. 86033-16-2.jpg" ..OR.. W28"*H22"*D28" ..OR.. D5*H1" ..OR.. L19*W19*H23"
        ..OR.. 25.5" ..OR.. 97.75" ..OR.. 72" ..OR.. 1*10.25" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 21: Illegal quoting, probably in the following text: "86034-8-1.jpg
        ..OR.. 86034-8-3.jpg" ..OR.. W28"*H15"*D28" ..OR.. D5*H1" ..OR.. L18.5*W18.5*H16.25"
        ..OR.. 19.25" ..OR.. 88.5" ..OR.. 72" ..OR.. 1*10.25" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 22: Illegal quoting, probably in the following text: "85190-10-1.jpg
        ..OR.. 85190-10-3.jpg" ..OR.. W35"*H32"*D35" ..OR.. D7.13"*1.66" ..OR.. L28*W24*H27"
        ..OR.. 37" ..OR.. 110" ..OR.. 1*72" ..OR.. 120" ..OR.. L12.13*W9.13*D4"'
    - - :warning
      - 'Line 23: Illegal quoting, probably in the following text: "85191-11.jpg ..OR..
        85191-11_1.jpg" ..OR.. W60"*H20"*D20" ..OR.. D7*H1.5" ..OR.. L55*W24*H15"
        ..OR.. 26" ..OR.. 62" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 24: Illegal quoting, probably in the following text: W26"*H52"*D26"
        ..OR.. D7*H1.5" ..OR.. L44*W24*H15" ..OR.. 55" ..OR.. 127" ..OR.. 1*72" ..OR..
        120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 25: Illegal quoting, probably in the following text: W24"*H33"*D24"
        ..OR.. D7*H1.5" ..OR.. L29*W20*H15" ..OR.. 37" ..OR.. 109" ..OR.. 1*72" ..OR..
        120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 26: Illegal quoting, probably in the following text: "85195-2-1.jpg
        ..OR.. 85195-2-4.jpg" ..OR.. W22"*H28"*D5" ..OR.. D5.88"*H1.13" ..OR.. L18*W15*H14"
        ..OR.. 7" ..OR.. L12.13*W9.13*D4"'
    - - :warning
      - 'Line 27: Illegal quoting, probably in the following text: W9"*H21"*D5" ..OR..
        L13*W13*H16" ..OR.. D5.88*H1.4" ..OR.. 7" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 28: Illegal quoting, probably in the following text: "85390-10-1.jpg
        ..OR.. 85390-10-4.jpg" ..OR.. W39"*H28"*D39" ..OR.. D6"*H1.38" ..OR.. L26*W32*H27"
        ..OR.. 32" ..OR.. 106" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 29: Illegal quoting, probably in the following text: "85490-10-1.jpg
        ..OR.. 85490-10-5.jpg" ..OR.. W39"*H28"*D39" ..OR.. D6"*H1.38" ..OR.. L26*W32*H27"
        ..OR.. 32" ..OR.. 106" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 30: Illegal quoting, probably in the following text: "85391-6-1.jpg
        ..OR.. 85391-6-5.jpg" ..OR.. W32"*H25"*D32" ..OR.. D6"*H1.38" ..OR.. L26*W34*H15"
        ..OR.. 29" ..OR.. 103" ..OR.. 1*72" ..OR.. 1*9.5" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 31: Illegal quoting, probably in the following text: "85491-6-1.jpg
        ..OR.. 85491-6-5.jpg" ..OR.. W32"*H25"*D32" ..OR.. D6"*H1.38" ..OR.. L26*W34*H15"
        ..OR.. 29" ..OR.. 103" ..OR.. 1*72" ..OR.. 1*9.5" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 32: Illegal quoting, probably in the following text: "85394-5-1.jpg
        ..OR.. 85394-5-5.jpg" ..OR.. W33"*H20"*D20" ..OR.. D7.13"*0.88" ..OR.. L22*W28*H17"
        ..OR.. 25" ..OR.. 56" ..OR.. 3*12" ..OR.. 72" ..OR.. L19.25*W4.75*D12.25"'
    - - :warning
      - 'Line 33: Illegal quoting, probably in the following text: "85494-5-1.jpg
        ..OR.. 85494-5-5.jpg" ..OR.. W33"*H20"*D20" ..OR.. D7.13"*0.88" ..OR.. L22*W28*H17"
        ..OR.. 25" ..OR.. 56" ..OR.. 3*12" ..OR.. 72" ..OR.. L19.25*W4.75*D12.25"'
    - - :warning
      - 'Line 34: Illegal quoting, probably in the following text: "85492-10-1.jpg
        ..OR.. 85492-10-3.jpg" ..OR.. W50"*H21"*D30" ..OR.. L15.75"*W6"*H1.25" ..OR..
        L36.5*W20.75*H28" ..OR.. 24.75" ..OR.. 97" ..OR.. 72" ..OR.. 2*12" ..OR..
        120" ..OR.. D12.25*H4.75"'
    - - :warning
      - 'Line 35: Illegal quoting, probably in the following text: "85592-10-1.jpg
        ..OR.. 85592-10-3.jpg" ..OR.. W50"*H21"*D30" ..OR.. L15.75"*W6"*H1.25" ..OR..
        L36.5*W20.75*H28" ..OR.. 24.75" ..OR.. 97" ..OR.. 72" ..OR.. 2*12" ..OR..
        120" ..OR.. D12.25*H4.75"'
    - - :warning
      - 'Line 36: Illegal quoting, probably in the following text: "85395-1-1.jpg
        ..OR.. 85395-1-3.jpg" ..OR.. W16"*H18"*D10" ..OR.. L21*W22*H8" ..OR.. D4.75"*H0.75"
        ..OR.. 7" ..OR.. L19.25*W4.75*D15.63"'
    - - :warning
      - 'Line 37: Illegal quoting, probably in the following text: "85495-1-1.jpg
        ..OR.. 85495-1-3.jpg" ..OR.. W16"*H18"*D10" ..OR.. L21*W22*H8" ..OR.. D4.75"*H0.75"
        ..OR.. 7" ..OR.. L19.25*W4.75*D15.63"'
    - - :warning
      - 'Line 38: Illegal quoting, probably in the following text: "85250-16-1.jpg
        ..OR.. 85250-16-4.jpg" ..OR.. W35"*H23"*D35" ..OR.. L38*W38*H23" ..OR.. 33"
        ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 39: Illegal quoting, probably in the following text: "85350-16-1.jpg
        ..OR.. 85350-16-4.jpg" ..OR.. W35"*H23"*D35" ..OR.. L38*W38*H23" ..OR.. 33"
        ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 40: Illegal quoting, probably in the following text: "85251-9-1.jpg
        ..OR.. 85251-9-4.jpg" ..OR.. W28"*H16"*D28" ..OR.. L31*W31*H21" ..OR.. 26"
        ..OR.. 62" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 41: Illegal quoting, probably in the following text: "85351-9-1.jpg
        ..OR.. 85351-9-5.jpg" ..OR.. W28"*H16"*D28" ..OR.. L31*W31*H21" ..OR.. 26"
        ..OR.. 62" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 42: Illegal quoting, probably in the following text: "85254-6-1.jpg
        ..OR.. 85254-6-4.jpg" ..OR.. W47"*H9"*D12" ..OR.. W17.75"*D4.75"*H0.8" ..OR..
        L15*W50*H13" ..OR.. 18" ..OR.. 54" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 43: Illegal quoting, probably in the following text: "85354-6-1.jpg
        ..OR.. 85354-6-5.jpg" ..OR.. W47"*H9"*D12" ..OR.. W17.75"*D4.75"*H0.8" ..OR..
        L15*W50*H13" ..OR.. 18" ..OR.. 54" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 44: Illegal quoting, probably in the following text: "85256-4-1.jpg
        ..OR.. 85256-4-3.jpg" ..OR.. W12"*H20"*D7" ..OR.. L14*W19*H14" ..OR.. L16.5"*W5.5"*H0.75"
        ..OR.. 7" ..OR.. L9*W3"'
    - - :warning
      - 'Line 45: Illegal quoting, probably in the following text: "85356-4-1.jpg
        ..OR.. 85356-4-3.jpg" ..OR.. W12"*H20"*D7" ..OR.. L14*W19*H14" ..OR.. L16.5"*W5.5"*H0.75"
        ..OR.. 7" ..OR.. L9*W3"'
    - - :warning
      - 'Line 46: Illegal quoting, probably in the following text: "85133-16.jpg ..OR..
        85133-16_1.jpg" ..OR.. W30"*H42"*D30" ..OR.. D5.4*H0.88" ..OR.. L24*W24*H32"
        ..OR.. L30*W30*H30" ..OR.. 47" ..OR.. 117" ..OR.. 1*72" ..OR.. 120" ..OR..
        "L21*W4.88" ..OR.. L21*W4.88" ..OR.. L18.75*W4.88" ..OR.. L15.4*W4.88"'
    - - :warning
      - 'Line 47: Illegal quoting, probably in the following text: "85130-7-1.jpg
        ..OR.. 85130-7-4.jpg" ..OR.. W47"*H24"*D13" ..OR.. L16.5"*4.75"*H0.88" ..OR..
        L49*W16*H28" ..OR.. 29" ..OR.. 101" ..OR.. 1*72" ..OR.. 2*19.25" ..OR.. 120"'
    - - :warning
      - 'Line 48: Illegal quoting, probably in the following text: W26"*H36"*D26"
        ..OR.. D5.4*H0.88" ..OR.. L24*W24*H37" ..OR.. 39" ..OR.. 111" ..OR.. 1*72"
        ..OR.. 120" ..OR.. "L25*W4.75" ..OR.. L16.75*W4.75" ..OR.. L20*W4.75"'
    - - :warning
      - 'Line 49: Illegal quoting, probably in the following text: W20"*H32"*D20"
        ..OR.. D5.4*H0.88" ..OR.. L23*W23*H34" ..OR.. 34" ..OR.. 106" ..OR.. 1*72"
        ..OR.. 120"'
    - - :warning
      - 'Line 50: Illegal quoting, probably in the following text: W24"*H13"*D24"
        ..OR.. D5.88*H0.75" ..OR.. L23*W23*H16" ..OR.. 1*8.5" ..OR.. 7" ..OR.. L8.25*W3.25"'
    - - :warning
      - 'Line 51: Illegal quoting, probably in the following text: W7"*H15"*D5" ..OR..
        L15*W12*H12" ..OR.. L7.1*W4.75*H0.75" ..OR.. 7" ..OR.. "L7.6*W3.1" ..OR..
        L9.6*W3.1"'
    - - :warning
      - 'Line 52: Illegal quoting, probably in the following text: "85422-12-1.jpg
        ..OR.. 85422-12-3.jpg" ..OR.. W42"*H45"*D42" ..OR.. D5.88"*H1" ..OR.. L37*W37*H42"
        ..OR.. 49" ..OR.. 114.5" ..OR.. 1*72" ..OR.. 1*9+1*12" ..OR.. 120"'
    - - :warning
      - 'Line 53: Illegal quoting, probably in the following text: "85421-8-1.jpg
        ..OR.. 85421-8-3.jpg" ..OR.. W30"*H31"*D30" ..OR.. D5.88"*H1" ..OR.. L25*W25*H30"
        ..OR.. 35" ..OR.. 108.75" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120"'
    - - :warning
      - 'Line 54: Illegal quoting, probably in the following text: "85420-12-1.jpg
        ..OR.. 85420-12-5.jpg" ..OR.. W60"*H23"*D18" ..OR.. L21.5"*W4.75"*H0.75" ..OR..
        L55*W14*H23" ..OR.. 26" ..OR.. 99" ..OR.. 1*72" ..OR.. 2*12" ..OR.. 120"'
    - - :warning
      - 'Line 55: Illegal quoting, probably in the following text: "85424-1-1.jpg
        ..OR.. 85424-1-3.jpg" ..OR.. W9"*H13"*D9" ..OR.. D4.75"*H1" ..OR.. L15*W11*H14"
        ..OR.. 24" ..OR.. 59.5" ..OR.. 72"'
    - - :warning
      - 'Line 56: Illegal quoting, probably in the following text: "85425-5-1.jpg
        ..OR.. 85425-5-4.jpg" ..OR.. W28"*H10"*D28" ..OR.. D7.13"*H0.75" ..OR.. L23*W23*H11"
        ..OR.. 7"'
    - - :warning
      - 'Line 57: Illegal quoting, probably in the following text: "85426-4-1.jpg
        ..OR.. 85426-4-5.jpg" ..OR.. W25"*H5"*D5" ..OR.. L20*W9*H9" ..OR.. L13.75"*W5.13"*H0.75"
        ..OR.. 7"'
    - - :warning
      - 'Line 58: Illegal quoting, probably in the following text: "85427-6-1.jpg
        ..OR.. 85427-6-5.jpg" ..OR.. W35"*H6"*D5" ..OR.. L30*W9*H9" ..OR.. L13.75"*W5.13"*H0.75"
        ..OR.. 7"'
    - - :warning
      - 'Line 59: Illegal quoting, probably in the following text: "85423-1-1.jpg
        ..OR.. 85423-1-4.jpg" ..OR.. W11"*H20"*D5" ..OR.. L19*W10*H9" ..OR.. L12.38"*W5"*H1"
        ..OR.. 7"'
    - - :warning
      - 'Line 60: Illegal quoting, probably in the following text: "85202-16.jpg ..OR..
        85202-16_1.jpg" ..OR.. W36"*H48"*D36" ..OR.. D5.5*H1" ..OR.. L39*W39*H35"
        ..OR.. L31*W19*H16" ..OR.. 51" ..OR.. 125" ..OR.. 2*72" ..OR.. 120" ..OR..
        "L11.8*W6" ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 61: Illegal quoting, probably in the following text: "85207-9.jpg ..OR..
        85207-9-2.jpg" ..OR.. W24"*H36"*D24" ..OR.. D5.5"*H1" ..OR.. L28*W28*H30"
        ..OR.. 40" ..OR.. 112" ..OR.. 1*72" ..OR.. 120" ..OR.. L11.75*W5.88"+L9.63*W4.75"+L6.5*W4.88"'
    - - :warning
      - 'Line 62: Illegal quoting, probably in the following text: W30"*H24"*D30"
        ..OR.. D5.5*H1" ..OR.. L31*W31*H30" ..OR.. 30" ..OR.. 103" ..OR.. 1*72" ..OR..
        120" ..OR.. "L11.8*W6" ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 63: Illegal quoting, probably in the following text: "85203-6.jpg ..OR..
        85203-6_1.jpg" ..OR.. W53"*H22"*D10" ..OR.. L15*W4.4*H0.75" ..OR.. L54*W13*H14"
        ..OR.. 26" ..OR.. 98" ..OR.. 1*72" ..OR.. 120" ..OR.. "L11.8*W6" ..OR.. L9.6*W4.75"
        ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 64: Illegal quoting, probably in the following text: "85200-6-1.jpg
        ..OR.. 85200-6-3.jpg" ..OR.. W24"*H21"*D24" ..OR.. D5.5"*H1" ..OR.. L26*W26*H16"
        ..OR.. 24" ..OR.. 96" ..OR.. 1*72" ..OR.. 120" ..OR.. L11.75*W5.88"+L9.63*W4.75"+L6.5*W4.88"'
    - - :warning
      - 'Line 65: Illegal quoting, probably in the following text: "85206-4-1.jpg
        ..OR.. 85206-4-4.jpg" ..OR.. W29"*H10"*D6" ..OR.. L41*W31*H8" ..OR.. L25.63"*W4.75"*H1"
        ..OR.. 7" ..OR.. L9.63*W4.75" L7.63*W4.25" L6.13*W3.88"'
    - - :warning
      - 'Line 66: Illegal quoting, probably in the following text: "85205-2-1.jpg
        ..OR.. 85205-2-5.jpg" ..OR.. W21"*H10"*D6" ..OR.. L15*W23*H8" ..OR.. L17.75"*W4.75"*H1"
        ..OR.. 7" ..OR.. L9.63*W4.75" L7.63*W4.25" L6.13*W3.88"'
    - - :warning
      - 'Line 67: Illegal quoting, probably in the following text: W6"*H12"*D4" ..OR..
        L16*W10*H9" ..OR.. L6*W4.5*H0.63" ..OR.. 23" ..OR.. 90" ..OR.. 7" ..OR.. "L11.8*W6"
        ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 68: Illegal quoting, probably in the following text: "85412-17-1.jpg
        ..OR.. 85412-17-5.jpg" ..OR.. W39"*H23"*D39" ..OR.. D5.88"*H0.75" ..OR.. L42.5*W42.5*H22"
        ..OR.. L42.25*W31.5*H24.5" ..OR.. 33" ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72"
        ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 69: Illegal quoting, probably in the following text: "85512-17-1.jpg
        ..OR.. 85512-17-5.jpg" ..OR.. W39"*H23"*D39" ..OR.. D5.88"*H0.75" ..OR.. L42.5*W42.5*H22"
        ..OR.. L42.25*W31.5*H24.5" ..OR.. 33" ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72"
        ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 70: Illegal quoting, probably in the following text: W39"*H23"*D39"
        ..OR.. D5.5"*H0.75" ..OR.. L42.5*42.5*22" ..OR.. L31.5*W42.25*H24.5" ..OR..
        33" ..OR.. 84" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 71: Illegal quoting, probably in the following text: "85414-20-1.jpg
        ..OR.. 85414-20-5.jpg" ..OR.. W31"*H35"*D31" ..OR.. D5.88"*H0.75" ..OR.. L34*W34*H35"
        ..OR.. L42*W29*H25" ..OR.. 14" ..OR.. 80" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 72: Illegal quoting, probably in the following text: "85514-20-1.jpg
        ..OR.. 85514-20-6.jpg" ..OR.. W31"*H35"*D31" ..OR.. D5.88"*H0.75" ..OR.. L34*W34*H35"
        ..OR.. L42*W29*H25" ..OR.. 14" ..OR.. 80" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 73: Illegal quoting, probably in the following text: W31"*H35"*D31"
        ..OR.. D6*H0.75" ..OR.. L34*W34*H35" ..OR.. L29*W42*H25" ..OR.. 43.75" ..OR..
        94" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 74: Illegal quoting, probably in the following text: "85411-13-1.jpg
        ..OR.. 85411-13-5.jpg" ..OR.. W31"*H19"*D31" ..OR.. D5.5"*H0.75" ..OR.. L33*W33*H28"
        ..OR.. 29" ..OR.. 65" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 75: Illegal quoting, probably in the following text: "85511-13-1.jpg
        ..OR.. 85511-13-6.jpg" ..OR.. W31"*H19"*D31" ..OR.. D5.5"*H0.75" ..OR.. L33*W33*H28"
        ..OR.. 29" ..OR.. 65" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 76: Illegal quoting, probably in the following text: "85621-13-1.jpg
        ..OR.. 85621-13-4.jpg" ..OR.. W31"*H19"*D31" ..OR.. D5.25"*H0.75" ..OR.. L33.5*W33.5*H27.75"
        ..OR.. 18.5" ..OR.. 64.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75
        xW4.25 xH1.25"'
    - - :warning
      - 'Line 77: Illegal quoting, probably in the following text: "85410-7-1.jpg
        ..OR.. 85410-7-6.jpg" ..OR.. W26"*H17"*D26" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H27"
        ..OR.. 27" ..OR.. 63" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 78: Illegal quoting, probably in the following text: "85510-7-1.jpg
        ..OR.. 85510-7-5.jpg" ..OR.. W26"*H17"*D26" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H27"
        ..OR.. 27" ..OR.. 63" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 79: Illegal quoting, probably in the following text: "85620-7-1.jpg
        ..OR.. 85620-7-2.jpg" ..OR.. W26"*H17"*D26" ..OR.. D5.25"*H0.75" ..OR.. L27.75*W27.75*H27.25"
        ..OR.. 27" ..OR.. 63" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25
        xH1.25"'
    - - :warning
      - 'Line 80: Illegal quoting, probably in the following text: "85413-6-1.jpg
        ..OR.. 85413-6-4.jpg" ..OR.. W47"*H11"*D15" ..OR.. L15.75"*W5.13"*H1" ..OR..
        L50*W18*H23" ..OR.. 18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 81: Illegal quoting, probably in the following text: "85513-6-1.jpg
        ..OR.. 85513-6-5.jpg" ..OR.. W47"*H11"*D15" ..OR.. L15.75"*W5.13"*H1" ..OR..
        L50*W18*H23" ..OR.. 18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 82: Illegal quoting, probably in the following text: W47"*H11"*D15"
        ..OR.. D15.75" xH5.25" ..OR.. L17.75*W50.5*H23.25" ..OR.. L15.75*W5.25*H1"
        ..OR.. 18.25" ..OR.. 69" ..OR.. 2*3"+2*6"+8*12" ..OR.. 120" ..OR.. L8.75 xW4.25
        xH1.25"'
    - - :warning
      - 'Line 83: Illegal quoting, probably in the following text: "85415-2-1.jpg
        ..OR.. 85415-2-3.jpg" ..OR.. W15"*H11"*D8" ..OR.. L22*W16*H17" ..OR.. L6.25"*W5.88"*H0.75"
        ..OR.. 7" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 84: Illegal quoting, probably in the following text: "85515-2-1.jpg
        ..OR.. 85515-2-3.jpg" ..OR.. W15"*H11"*D8" ..OR.. L22*W16*H17" ..OR.. L6.25"*W5.88"*H0.75"
        ..OR.. 7" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 85: Illegal quoting, probably in the following text: W15"*H11"*D8" ..OR..
        L15.75*W21.75*H16.5" ..OR.. D6xH6.25" ..OR.. 7" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 86: Illegal quoting, probably in the following text: W34"*H37"*D34"
        ..OR.. D5.5*H1" ..OR.. L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR..
        75" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 87: Illegal quoting, probably in the following text: W34"*H37"*D34"
        ..OR.. D5.5*H1" ..OR.. L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR..
        75" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 88: Illegal quoting, probably in the following text: W34"*H37"*D34"
        ..OR.. D5.5*H1" ..OR.. L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR..
        75.25" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 89: Illegal quoting, probably in the following text: W23"*H29"*D23"
        ..OR.. D5.5*H1" ..OR.. L30*W29*H24" ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 90: Illegal quoting, probably in the following text: "85262-13.jpg ..OR..
        85262-13_1.jpg" ..OR.. W23"*H29"*D23" ..OR.. D5.5*H1" ..OR.. L30*W29*H24"
        ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 91: Illegal quoting, probably in the following text: W23"*H29"*D23"
        ..OR.. D5.5*H1" ..OR.. L30*W29*H24" ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 92: Illegal quoting, probably in the following text: "85161-5.jpg ..OR..
        85161-5_1.jpg" ..OR.. W17"*H20"*D17" ..OR.. D5.5*H1" ..OR.. L23*W20*H23" ..OR..
        28" ..OR.. 64" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 93: Illegal quoting, probably in the following text: W17"*H20"*D17"
        ..OR.. D5.5*H1" ..OR.. L23*W20*H23" ..OR.. 28" ..OR.. 64" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 94: Illegal quoting, probably in the following text: W17"*H20"*D17"
        ..OR.. D5.5*H1" ..OR.. L23*W20*H23" ..OR.. 28" ..OR.. 64" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 95: Illegal quoting, probably in the following text: W12"*H13"*D7" ..OR..
        L18*W13*H16" ..OR.. L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 96: Illegal quoting, probably in the following text: W12"*H13"*D7" ..OR..
        L18*W13*H16" ..OR.. L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 97: Illegal quoting, probably in the following text: W12"*H13"*D7" ..OR..
        L18*W13*H16" ..OR.. L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 98: Illegal quoting, probably in the following text: "85433-12-1.jpg
        ..OR.. 85433-12-3.jpg" ..OR.. W52"*H52"*D52" ..OR.. D5.88*H0.75" ..OR.. L29*W29*H12"
        ..OR.. 58" ..OR.. 126" ..OR.. 1*72" ..OR.. 144"'
    - - :warning
      - 'Line 99: Illegal quoting, probably in the following text: "85432-8-1.jpg
        ..OR.. 85432-8-3.jpg" ..OR.. W38"*H38"*D38" ..OR.. D5.13*H0.75" ..OR.. L56*W56*H14"
        ..OR.. 44" ..OR.. 112" ..OR.. 1*72" ..OR.. 144"'
    - - :warning
      - 'Line 100: Illegal quoting, probably in the following text: "85431-6-1.jpg
        ..OR.. 85431-6-3.jpg" ..OR.. W28"*H30"*D28" ..OR.. D5.13*H0.75" ..OR.. L41*W41*H12"
        ..OR.. 36" ..OR.. 104" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 101: Illegal quoting, probably in the following text: "85430-4-1.jpg
        ..OR.. 85430-4-3.jpg" ..OR.. W16"*H15"*D16" ..OR.. D4.75*H0.75" ..OR.. L31*W31*H10"
        ..OR.. 21" ..OR.. 89" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 102: Illegal quoting, probably in the following text: "85435-8-1.jpg
        ..OR.. 85435-8-5.jpg" ..OR.. W34"*H10"*D34" ..OR.. D5.13*H0.75" ..OR.. L10*W16*H11"
        ..OR.. 18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 103: Illegal quoting, probably in the following text: "85434-6-1.jpg
        ..OR.. 85434-6-4.jpg" ..OR.. W26"*H8"*D26" ..OR.. D5.13*H0.75" ..OR.. L37*W37*H13"
        ..OR.. 16" ..OR.. 53" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 104: Illegal quoting, probably in the following text: "85437-3-1.jpg
        ..OR.. 85437-3-5.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5.13*H0.75" ..OR.. L11*W15*H7"
        ..OR.. 7"'
    - - :warning
      - 'Line 105: Illegal quoting, probably in the following text: "85436-1-1.jpg
        ..OR.. 85436-1-4.jpg" ..OR.. W7"*H9"*D7" ..OR.. D5.13*H0.75" ..OR.. L19*W19*H12"
        ..OR.. 17" ..OR.. 53" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 106: Illegal quoting, probably in the following text: "85438-1-1.jpg
        ..OR.. 85438-1-4.jpg" ..OR.. W8"*H12"*D5" ..OR.. L14.5*W10.75*H7.5" ..OR..
        L9"*4.75"*H0.75" ..OR.. 7"'
    - - :warning
      - 'Line 107: Illegal quoting, probably in the following text: "85232-12.jpg
        ..OR.. 85232-12_1.jpg" ..OR.. W26"*H39"*D26" ..OR.. D5.5*H1" ..OR.. L30*W30*H14"
        ..OR.. 42" ..OR.. 115" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 108: Illegal quoting, probably in the following text: W48"*H24"*D15"
        ..OR.. L16.1*W5.88*H0.88" ..OR.. L50*W22*H11" ..OR.. 27" ..OR.. 100" ..OR..
        2*72" ..OR.. 2*15" ..OR.. 120" ..OR.. L47.25*W14.25*H8.25"'
    - - :warning
      - 'Line 109: Illegal quoting, probably in the following text: W27"*H25"*D27"
        ..OR.. D5.5*H1" ..OR.. L30*W30*H25" ..OR.. 28" ..OR.. 101" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 110: Illegal quoting, probably in the following text: W23"*H27"*D23"
        ..OR.. D5.5*H1" ..OR.. L26*W26*H15" ..OR.. 30" ..OR.. 103" ..OR.. 1*72" ..OR..
        120" ..OR.. D23*H8"'
    - - :warning
      - 'Line 111: Illegal quoting, probably in the following text: W15"*H12"*D15"
        ..OR.. D5.5*H1" ..OR.. L18*W18*H15" ..OR.. 1*3.25" ..OR.. 7" ..OR.. D15*H7"'
    - - :warning
      - 'Line 112: Illegal quoting, probably in the following text: W7"*H9.5"*D7"
        ..OR.. D5.5*H1" ..OR.. L16*W12*H10" ..OR.. 20" ..OR.. 56" ..OR.. 1*6"+3*12"
        ..OR.. 120"'
    - - :warning
      - 'Line 113: Illegal quoting, probably in the following text: W36"*H6"*D6" ..OR..
        L39*W9*H9" ..OR.. L35.38*W4.5*H0.75" ..OR.. 7" ..OR.. L36*W4.8*H5.88"'
    - - :warning
      - 'Line 114: Illegal quoting, probably in the following text: W25"*H6"*D5" ..OR..
        L28*W9*H9" ..OR.. L24.38*W4.5*H0.75" ..OR.. 7" ..OR.. L25*W4.8*H4.38"'
    - - :warning
      - 'Line 115: Illegal quoting, probably in the following text: W8"*H9"*D5" ..OR..
        L11*W10*H8" ..OR.. L6.5*W6.5*H0.75" ..OR.. 7" ..OR.. L8.38*W7.25*H4"'
    - - :warning
      - 'Line 116: Illegal quoting, probably in the following text: W37"*H58"*D37"
        ..OR.. D5.1*H0.75" ..OR.. L43*W40*H13" ..OR.. 67" ..OR.. 103" ..OR.. 120"
        ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 117: Illegal quoting, probably in the following text: "85244-7.jpg ..OR..
        85244-7_1.jpg" ..OR.. W26"*H46"*D26" ..OR.. D23.63*H1" ..OR.. L28*W26*H18"
        ..OR.. 52" ..OR.. 97" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 118: Illegal quoting, probably in the following text: "85242-6.jpg ..OR..
        85242-6_1.jpg" ..OR.. W24"*H45"*D24" ..OR.. D5.1*H0.75" ..OR.. L32*W27*H13"
        ..OR.. 53" ..OR.. 89" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 119: Illegal quoting, probably in the following text: W50"*H23"*D5"
        ..OR.. L50.38*W8.75*H0.75" ..OR.. L54*W15*H13" ..OR.. 32" ..OR.. 97" ..OR..
        120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 120: Illegal quoting, probably in the following text: W20"*H37"*D20"
        ..OR.. D5.1*H0.75" ..OR.. L26*W22*H18" ..OR.. 45" ..OR.. 81" ..OR.. 120" ..OR..
        D3.25*L20.75"'
    - - :warning
      - 'Line 121: Illegal quoting, probably in the following text: W5"*H23"*D5" ..OR..
        D5.1*H0.75" ..OR.. L24*W15*H8" ..OR.. 31" ..OR.. 67" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 122: Illegal quoting, probably in the following text: W6"*H32"*D7" ..OR..
        L35*W13*H10" ..OR.. 7" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 123: Illegal quoting, probably in the following text: "85286-68-1.jpg
        ..OR.. 85286-68-3.jpg" ..OR.. W20"*H54"*D20" ..OR.. D20"*H1.38" ..OR.. L24*W24*H31"
        ..OR.. 20" ..OR.. D3.88"'
    - - :warning
      - 'Line 124: Illegal quoting, probably in the following text: "85283-47-1.jpg
        ..OR.. 85283-47-4.jpg" ..OR.. W20"*H40"*D20" ..OR.. D20"*H1.38" ..OR.. L24*W24*H16"
        ..OR.. 20" ..OR.. D3.88"'
    - - :warning
      - 'Line 125: Illegal quoting, probably in the following text: "85281-19-1.jpg
        ..OR.. 85281-19-4.jpg" ..OR.. W20"*H20"*D20" ..OR.. D20"*H1.38" ..OR.. L24*W24*H16"
        ..OR.. 20" ..OR.. D3.88"'
    - - :warning
      - 'Line 126: Illegal quoting, probably in the following text: "85289-5-1.jpg
        ..OR.. 85289-5-4.jpg" ..OR.. W6"*H25"*D7" ..OR.. L8*W12*H20" ..OR.. L8.63"*W5.75"*H1.38"
        ..OR.. 7" ..OR.. D3.88"'
    - - :warning
      - 'Line 127: Illegal quoting, probably in the following text: "85288-3-1.jpg
        ..OR.. 85288-3-5.jpg" ..OR.. W6"*H15"*D7" ..OR.. L8*W12*H15" ..OR.. L8.63"*W5.75"*H1.38"
        ..OR.. 7" ..OR.. D3.88"'
    - - :warning
      - 'Line 128: Illegal quoting, probably in the following text: "85216-14.jpg
        ..OR.. 85216-14_1.jpg" ..OR.. W50"*H14"*D10" ..OR.. L50.5*W9.88*H1.38" ..OR..
        L54*W13*H15" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 129: Illegal quoting, probably in the following text: "85214-13.jpg
        ..OR.. 85214-13_1.jpg" ..OR.. W24"*H14"*D24" ..OR.. D24*H1.38" ..OR.. L35*W27*H9"
        ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 130: Illegal quoting, probably in the following text: W36"*H14"*D10"
        ..OR.. L36*W9.88*H1.38" ..OR.. L39*W13*H15" ..OR.. 23" ..OR.. 90" ..OR.. 120"
        ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 131: Illegal quoting, probably in the following text: "85213-6.jpg ..OR..
        85213-6_1.jpg" ..OR.. W16"*H14"*D16" ..OR.. D16*H1.38" ..OR.. L26*W19*H9"
        ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 132: Illegal quoting, probably in the following text: W10"*H14"*D10"
        ..OR.. D9.88*H1.25" ..OR.. L16*W15*H9" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR..
        D3.5*L12"'
    - - :warning
      - 'Line 133: Illegal quoting, probably in the following text: W6"*H14"*D6" ..OR..
        D5.88*H1.25" ..OR.. L15*W9*H9" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 134: Illegal quoting, probably in the following text: "85401-9-1.jpg
        ..OR.. 85401-9-3.jpg" ..OR.. W24"*H7"*D24" ..OR.. D24*1.38" ..OR.. L28*W28*H15"
        ..OR.. 51" ..OR.. 75" ..OR.. 1*5.25+31*32+1*7.38+1*1.38+1*8.63+1*10.13+1*6+1*8.75"
        ..OR.. 7" ..OR.. D4"'
    - - :warning
      - 'Line 135: Illegal quoting, probably in the following text: "85400-5-1.jpg
        ..OR.. 85400-5-3.jpg" ..OR.. W16"*H7"*D16" ..OR.. D15.75"*1.38" ..OR.. L20*W20*H15"
        ..OR.. 42" ..OR.. 66" ..OR.. 1*9"+15*12"+1*1.38"+1*6"+1*10.38"+1*3" ..OR..
        7" ..OR.. D4"'
    - - :warning
      - 'Line 136: Illegal quoting, probably in the following text: "85404-5-1.jpg
        ..OR.. 85404-5-5.jpg" ..OR.. W43"*H7"*D6" ..OR.. L43.25"*W6.25"*H1.38" ..OR..
        L10*W47*H15" ..OR.. 21" ..OR.. 57" ..OR.. 7*6+15*12" ..OR.. 7" ..OR.. D4"'
    - - :warning
      - 'Line 137: Illegal quoting, probably in the following text: "85406-1-1.jpg
        ..OR.. 85406-1-4.jpg" ..OR.. W6"*H7"*D4" ..OR.. D5.5"*H1.25" ..OR.. L9*W17*H8"
        ..OR.. 15" ..OR.. 51" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D4"'
    - - :warning
      - 'Line 138: Illegal quoting, probably in the following text: "85407-1-1.jpg
        ..OR.. 85407-1-5.jpg" ..OR.. W5"*H13"*D6" ..OR.. L13.13"*5.38"*1.25" ..OR..
        L11*W16*H9" ..OR.. 7" ..OR.. D4"'
    - - :warning
      - 'Line 139: Illegal quoting, probably in the following text: W36"*H34"*D36"
        ..OR.. 6.25"*1" ..OR.. L40*W40*H20" ..OR.. 41" ..OR.. 109" ..OR.. 1*72" ..OR..
        120" ..OR.. L13.75"*D1"'
    - - :warning
      - 'Line 140: Illegal quoting, probably in the following text: W45"*H26"*D12"
        ..OR.. L17.75"*W5"*H1" ..OR.. L17*W48*H18" ..OR.. 33" ..OR.. 100" ..OR.. 1*72"
        ..OR.. 120" ..OR.. L13.75"*D1"'
    - - :warning
      - 'Line 141: Illegal quoting, probably in the following text: "85101-8.jpg ..OR..
        85101-8_1.jpg" ..OR.. W30"*H26"*D30" ..OR.. D5.1*H0.75" ..OR.. L33*W33*H16"
        ..OR.. 29" ..OR.. 101" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 142: Illegal quoting, probably in the following text: W24"*H20"*D24"
        ..OR.. D5.1*H0.75" ..OR.. L27*W27*H14" ..OR.. 23" ..OR.. 95" ..OR.. 1*72"
        ..OR.. 1*8.7" ..OR.. 120" ..OR.. D1*H10.75"'
    - - :warning
      - 'Line 143: Illegal quoting, probably in the following text: W18"*H17"*D18"
        ..OR.. D5.1*H0.75" ..OR.. L21*W21*H14" ..OR.. 21" ..OR.. 92" ..OR.. 1*72"
        ..OR.. 1*6" ..OR.. 120" ..OR.. D1*H10.75"'
    - - :warning
      - 'Line 144: Illegal quoting, probably in the following text: "85109-4-1.jpg
        ..OR.. 85109-4-2.jpg" ..OR.. W21"*H12"*D21" ..OR.. D5"*D0.75" ..OR.. L25*W25*H10"
        ..OR.. 7" ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 145: Illegal quoting, probably in the following text: "85108-4-1.jpg
        ..OR.. 85108-4-5.jpg" ..OR.. W36"*H8"*D5" ..OR.. L10*W39*H13" ..OR.. L33"*W5"*H0.75"
        ..OR.. 7" ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 146: Illegal quoting, probably in the following text: "85107-3-1.jpg
        ..OR.. 85107-3-2.jpg" ..OR.. W26"*H8"*D5" ..OR.. L10*W30*H13" ..OR.. L23.5"*W5"*H0.75"
        ..OR.. 7" ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 147: Illegal quoting, probably in the following text: W9"*H26"*D9" ..OR..
        D5.1*H0.75" ..OR.. L20*W18*H11" ..OR.. 29" ..OR.. 101" ..OR.. 1*72" ..OR..
        1*12" ..OR.. 120" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 148: Illegal quoting, probably in the following text: "85106-1-1.jpg
        ..OR.. 85106-1-2.jpg" ..OR.. W7"*H20"*D5" ..OR.. L11*W23*H15" ..OR.. L15"*W4.25"*H0.75"
        ..OR.. 7" ..OR.. L19.25*D0.72"'
    - - :warning
      - 'Line 149: Illegal quoting, probably in the following text: W9"*H15"*D5" ..OR..
        L18*W12*H11" ..OR.. L8.25*W4.75*H0.75" ..OR.. 7" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 150: Illegal quoting, probably in the following text: "85171-12.jpg
        ..OR.. 85171-12_1.jpg" ..OR.. W32"*H12"*D32" ..OR.. L35*W35*H15" ..OR.. 20"
        ..OR.. 83" ..OR.. 120" ..OR.. "L6.75*W1.5*H0.6" ..OR.. L8.3*W1.5*H0.6" ..OR..
        L10*W1.5*H0.6"'
    - - :warning
      - 'Line 151: Illegal quoting, probably in the following text: W50"*H13"*D4"
        ..OR.. L19.63*W5.5*H0.88" ..OR.. L53*W13*H15" ..OR.. 20" ..OR.. 83" ..OR..
        120" ..OR.. "L6.75*W1.5*H0.6" ..OR.. L8.3*W1.5*H0.6" ..OR.. L10*W1.5*H0.6"'
    - - :warning
      - 'Line 152: Illegal quoting, probably in the following text: W10"*H12"*D5"
        ..OR.. L15*W12*H11" ..OR.. L11.75*W9.4*H0.75" ..OR.. 7" ..OR.. "L6.75*W1.5*H0.6"
        ..OR.. L8.3*W1.5*H0.6" ..OR.. L10*W1.5*H0.6"'
    - - :warning
      - 'Line 153: Illegal quoting, probably in the following text: W57"*H26"*D30"
        ..OR.. D7*H1.5" ..OR.. L60*W30*H27" ..OR.. 34" ..OR.. 70" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 154: Illegal quoting, probably in the following text: "85182-9.jpg ..OR..
        85182-9_1.jpg" ..OR.. W37"*H30"*D37" ..OR.. D7*H1.5" ..OR.. L35*W35*H28" ..OR..
        33" ..OR.. 105" ..OR.. 1*72" ..OR.. 120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 155: Illegal quoting, probably in the following text: W21"*H34"*D21"
        ..OR.. D7*H1.5" ..OR.. L32*W26*H17" ..OR.. 36" ..OR.. 109" ..OR.. 1*72" ..OR..
        120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 156: Illegal quoting, probably in the following text: W6"*H14"*D10"
        ..OR.. L18*W13*H9" ..OR.. D6*H1.5" ..OR.. 7" ..OR.. D6*H6"'
    - - :warning
      - 'Line 157: Illegal quoting, probably in the following text: "85270-12-1.jpg
        ..OR.. 85270-12-3.jpg" ..OR.. W32"*H40"*D32" ..OR.. L35*W35*H40" ..OR.. L34*26*15"
        ..OR.. 49" ..OR.. 85" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. "D9.88""+D7.88"'
    - - :warning
      - 'Line 158: Unclosed quoted field in line 1.'
    - - :warning
      - 'Line 159: Illegal quoting, probably in the following text: "85370-12-1.jpg
        ..OR.. 85370-12-4.jpg" ..OR.. W32"*H40"*D32" ..OR.. L35*W35*H40" ..OR.. L34*26*15"
        ..OR.. 49" ..OR.. 85" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. "D9.88""+D7.88"'
    - - :warning
      - 'Line 160: Unclosed quoted field in line 1.'
    - - :warning
      - 'Line 161: Illegal quoting, probably in the following text: "85271-12-1.jpg
        ..OR.. 85271-12-51.jpg" ..OR.. W25"*H34"*D25" ..OR.. D5.13"*H0.75" ..OR..
        L28*W28*H30.5" ..OR.. L28*W18*H21" ..OR.. 43" ..OR.. 79" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. "D5.88""+D7.13"'
    - - :warning
      - 'Line 162: Unclosed quoted field in line 1.'
    - - :warning
      - 'Line 163: Illegal quoting, probably in the following text: "85371-12-1.jpg
        ..OR.. 85371-12-4.jpg" ..OR.. W25"*H34"*D25" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H30.5"
        ..OR.. L28*W18*H21" ..OR.. 43" ..OR.. 79" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        "D5.88""+D7.13"'
    - - :warning
      - 'Line 164: Unclosed quoted field in line 1.'
    - - :warning
      - 'Line 165: Illegal quoting, probably in the following text: "85273-8-1.jpg
        ..OR.. 85273-8-4.jpg" ..OR.. W56"*H25"*D18" ..OR.. L27.13"*W5.13"*H1" ..OR..
        L59*W23.5*H22" ..OR.. L26*W26*H20" ..OR.. 33" ..OR.. 70" ..OR.. 2*6+6*12"
        ..OR.. 72" ..OR.. D7.88"+D9.88"'
    - - :warning
      - 'Line 166: Illegal quoting, probably in the following text: "85373-8-1.jpg
        ..OR.. 85373-8-1.jpg" ..OR.. W56"*H25"*D18" ..OR.. L27.13"*W5.13"*H1" ..OR..
        L59*W23.5*H22" ..OR.. L26*W26*H20" ..OR.. 33" ..OR.. 70" ..OR.. 2*6+6*12"
        ..OR.. 72" ..OR.. D7.88"+D9.88"'
    - - :warning
      - 'Line 167: Illegal quoting, probably in the following text: W14"*H19"*D14"
        ..OR.. D5.13"*H0.75" ..OR.. L20*W25*H18" ..OR.. 28" ..OR.. 64" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. D13.75"'
    - - :warning
      - 'Line 168: Illegal quoting, probably in the following text: "85376-1-1.jpg
        ..OR.. 85376-1-3.jpg" ..OR.. W14"*H19"*D14" ..OR.. D5.13"*H0.75" ..OR.. L20*W25*H18"
        ..OR.. 28" ..OR.. 64" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D13.75"'
    - - :warning
      - 'Line 169: Illegal quoting, probably in the following text: W10"*H14"*D10"
        ..OR.. D5.13"*H0.75" ..OR.. L18*W21*H14" ..OR.. 24" ..OR.. 60" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. D9.88"'
    - - :warning
      - 'Line 170: Illegal quoting, probably in the following text: "85375-1-1.jpg
        ..OR.. 85375-1-2.jpg" ..OR.. W10"*H14"*D10" ..OR.. D5.13"*H0.75" ..OR.. L18*W21*H14"
        ..OR.. 24" ..OR.. 60" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D9.88"'
    - - :warning
      - 'Line 171: Illegal quoting, probably in the following text: W38"*H38"*D38"
        ..OR.. D6.4*H1.88" ..OR.. L41*W41*H40" ..OR.. L32*W24*H24" ..OR.. L32*W24*H24"
        ..OR.. 48" ..OR.. 72" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D10*H1.5"'
    - - :warning
      - 'Line 172: Illegal quoting, probably in the following text: "85122-12.jpg
        ..OR.. 85122-12_1.jpg" ..OR.. W26"*H26"*D26" ..OR.. D6.4*H1.88" ..OR.. L31*W31*H31"
        ..OR.. L30*W24*H24" ..OR.. 36" ..OR.. 66" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR..
        D10*H1.5"'
    - - :warning
      - 'Line 173: Illegal quoting, probably in the following text: "85123-6.jpg ..OR..
        85123-6_1.jpg" ..OR.. W24"*H18"*D24" ..OR.. D6.4*H1.88" ..OR.. L28*W26*H26"
        ..OR.. 1*6" ..OR.. 7" ..OR.. D10*H1.5"'
    - - :warning
      - 'Line 174: Illegal quoting, probably in the following text: "85124-8-1.jpg
        ..OR.. 85124-8-5.jpg" ..OR.. W58"*H10"*D13" ..OR.. L16.88"*W5.88"*H0.88" ..OR..
        L54*W14*H16" ..OR.. 13" ..OR.. 49" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. D9.63"*1.63"'
    - - :warning
      - 'Line 175: Illegal quoting, probably in the following text: "85125-3-1.jpg
        ..OR.. 85125-3-2.jpg" ..OR.. W15"*H27"*D6" ..OR.. L24*W15*H13" ..OR.. D4.75"*H0.75"
        ..OR.. 7" ..OR.. D9.63"*1.63"'
    - - :warning
      - 'Line 176: Illegal quoting, probably in the following text: W24"*H27"*D24"
        ..OR.. D5.88*H0.88" ..OR.. L28*W28*H29" ..OR.. 36" ..OR.. 72" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D23.75*H23.75"'
    - - :warning
      - 'Line 177: Illegal quoting, probably in the following text: W16"*H19"*D16"
        ..OR.. D5.88*H0.88" ..OR.. L19.5*W19.5*H20.75" ..OR.. 29" ..OR.. 65" ..OR..
        1*6"+3*12" ..OR.. 120" ..OR.. D15.75*H15.75"'
    - - :warning
      - 'Line 178: Illegal quoting, probably in the following text: "85221-1.jpg ..OR..
        85221-1_1.jpg" ..OR.. W8"*H10"*D8" ..OR.. D5.88*H0.88" ..OR.. L11*W11*H13"
        ..OR.. 20" ..OR.. 56" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D7.5*H7.5"'
    - - :warning
      - 'Line 179: Illegal quoting, probably in the following text: W41"*H31"*D41"
        ..OR.. D5.5*H1" ..OR.. L43*W43*H9" ..OR.. 34" ..OR.. 106" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 180: Illegal quoting, probably in the following text: W29"*H27"*D29"
        ..OR.. D5.5*H1" ..OR.. L32*W32*H9" ..OR.. 32" ..OR.. 102" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 181: Illegal quoting, probably in the following text: W6"*H18"*D4" ..OR..
        L21*W8*H7" ..OR.. L18*W5.75*H1.25" ..OR.. 7"'
    - - :warning
      - 'Line 182: Illegal quoting, probably in the following text: "85111-6.jpg ..OR..
        85111-6_1.jpg" ..OR.. W36"*H18"*D36" ..OR.. D5.1*H0.75" ..OR.. L40*W40*H22"
        ..OR.. 32" ..OR.. 80" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D36*H18"'
    - - :warning
      - 'Line 183: Illegal quoting, probably in the following text: W24"*H12"*D24"
        ..OR.. D5.1*H0.75" ..OR.. L28*W28*H16" ..OR.. 32" ..OR.. 74" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D24*H12"'
    - - :warning
      - 'Line 184: Illegal quoting, probably in the following text: W16"*H16"*D16"
        ..OR.. D5.1*H0.75" ..OR.. L19*W19*H19" ..OR.. 30" ..OR.. 73" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D16*H15.5"'
    - - :warning
      - 'Line 185: Illegal quoting, probably in the following text: W36"*H21"*D36"
        ..OR.. D5.5*H1" ..OR.. L39*W39*H13" ..OR.. 24" ..OR.. 96" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 186: Illegal quoting, probably in the following text: "85141-6.jpg ..OR..
        85141-6_1.jpg" ..OR.. W27"*H18"*D27" ..OR.. D5.5*H1" ..OR.. L30*W30*H12" ..OR..
        21" ..OR.. 93" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 187: Illegal quoting, probably in the following text: W14"*H21"*D14"
        ..OR.. D5.5*H1" ..OR.. L18*W18*H30" ..OR.. 24" ..OR.. 96" ..OR.. "Iron ..OR..
        solid wood and glass" ..OR.. 1*72" ..OR.. 120" ..OR.. L11.6*W10*H3"'
    - - :warning
      - 'Line 188: Illegal quoting, probably in the following text: "65000-1.jpg ..OR..
        65000-6.jpg" ..OR.. W5"*H19"*D3" ..OR.. W4.72"*H18"'
    - - :warning
      - 'Line 189: Illegal quoting, probably in the following text: "65001-1.jpg ..OR..
        65001-7.jpg" ..OR.. W5"*H24"*D3" ..OR.. W4.72"*H24.7"'
    - - :warning
      - 'Line 190: Illegal quoting, probably in the following text: "65060-1.jpg ..OR..
        65060-5.jpg" ..OR.. W6"*H18"*D3"'
    - - :warning
      - 'Line 191: Illegal quoting, probably in the following text: "65061-1.jpg ..OR..
        65061-5.jpg" ..OR.. W6"*H27"*D3"'
    - - :warning
      - 'Line 192: Illegal quoting, probably in the following text: "65030-1.jpg ..OR..
        65030-4.jpg" ..OR.. W7"*H14"*D4" ..OR.. W7"*H14.37"'
    - - :warning
      - 'Line 193: Illegal quoting, probably in the following text: "65031-1.jpg ..OR..
        65031-4.jpg" ..OR.. W7"*H24"*D4" ..OR.. W7"*H24"'
    - - :warning
      - 'Line 194: Illegal quoting, probably in the following text: "65040-1.jpg ..OR..
        65040-5.jpg" ..OR.. W6"*H16"*D3" ..OR.. "Stainless steel ..OR..  aluminium
        and crystal"'
    - - :warning
      - 'Line 195: Illegal quoting, probably in the following text: "65041-1.jpg ..OR..
        65041-5.jpg" ..OR.. W6"*H24"*D3" ..OR.. "Stainless steel ..OR..  aluminium
        and crystal"'
    - - :warning
      - 'Line 196: Illegal quoting, probably in the following text: "65010-1.jpg ..OR..
        65010-5.jpg" ..OR.. W6"*H11"*D3" ..OR.. W4.72"*H4.3"'
    - - :warning
      - 'Line 197: Illegal quoting, probably in the following text: "65011-1.jpg ..OR..
        65011-5.jpg" ..OR.. W6"*H15"*D3" ..OR.. W4.72"*H4.3"'
    - - :warning
      - 'Line 198: Illegal quoting, probably in the following text: "65050-1.jpg ..OR..
        65050-5.jpg" ..OR.. W7"*H14"*D2"'
    - - :warning
      - 'Line 199: Illegal quoting, probably in the following text: "65051-1.jpg ..OR..
        65051-4.jpg" ..OR.. W7"*H18"*D2"'
    - - :warning
      - 'Line 200: Illegal quoting, probably in the following text: "65090-1.jpg ..OR..
        65090-4.jpg" ..OR.. W5"*H16"*D4"'
    - - :warning
      - 'Line 201: Illegal quoting, probably in the following text: "65091-1.jpg ..OR..
        65091-4.jpg" ..OR.. W5"*H24"*D4"'
 |
| 2026-06-16T06:28:12.584866 | ---
- - Products
  - - - :warning
      - 'Error running cleancsv: 2026/06/16 06:28:11 parse error on line 2, column
        179: bare " in non-quoted-field

        '
    - - :warning
      - 'Line 2: Illegal quoting, probably in the following text: "86010-1-1.jpg ..OR..
        86010-1-4.jpg" ..OR.. L16.25*W14.5*H10.75" ..OR.. D5*H1.25" ..OR.. 7" ..OR..
        W7.25*H7.25"'
    - - :warning
      - 'Line 3: Illegal quoting, probably in the following text: "86120-1-1.jpg ..OR..
        86120-1-5.jpg" ..OR.. L16.25*W14.5*H10.75" ..OR.. D5*H1.25" ..OR.. 7" ..OR..
        W7.25*H7.25"'
    - - :warning
      - 'Line 4: Illegal quoting, probably in the following text: "86013-1-1.jpg ..OR..
        86013-1-2.jpg" ..OR.. D5*H1.25" ..OR.. L16.5*W16.5*H10.75" ..OR.. 17.5" ..OR..
        71" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 5: Illegal quoting, probably in the following text: "86123-1-1.jpg ..OR..
        86123-1-3.jpg" ..OR.. D5*H1.25" ..OR.. L16.5*W16.5*H10.75" ..OR.. 17.5" ..OR..
        71" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 6: Illegal quoting, probably in the following text: "86011-2-1.jpg ..OR..
        86011-2-5.jpg" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25" ..OR.. 15.5" ..OR..
        70" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 7: Illegal quoting, probably in the following text: "86121-2-1.jpg ..OR..
        86121-2-5.jpg" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25" ..OR.. 15.5" ..OR..
        70" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 8: Illegal quoting, probably in the following text: "86015-1-1.jpg ..OR..
        86015-1-3.jpg" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25" ..OR.. 18" ..OR..
        72" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 9: Illegal quoting, probably in the following text: "86125-1-1.jpg ..OR..
        86125-1-2.jpg" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25" ..OR.. 18" ..OR..
        72" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 10: Illegal quoting, probably in the following text: "86014-6-1.jpg
        ..OR.. 86014-6-5.jpg" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75" ..OR..
        21" ..OR.. 74" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 11: Illegal quoting, probably in the following text: "86124-6-1.jpg
        ..OR.. 86124-6-5.jpg" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75" ..OR..
        21" ..OR.. 74" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 12: Illegal quoting, probably in the following text: "86017-6-1.jpg
        ..OR.. 86017-6-2.jpg" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75" ..OR..
        25" ..OR.. 79" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 13: Illegal quoting, probably in the following text: "86127-6-1.jpg
        ..OR.. 86127-6-2.jpg" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75" ..OR..
        25" ..OR.. 79" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 14: Illegal quoting, probably in the following text: "86001-1-1.jpg
        ..OR.. 86001-1-3.jpg" ..OR.. D6"*H1" ..OR.. L20*W13*H14.25" ..OR.. 16.5" ..OR..
        70.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 15: Illegal quoting, probably in the following text: "86002-3-1.jpg
        ..OR.. 86002-3-3.jpg" ..OR.. L16.75"*W15.75"*H1.5" ..OR.. L24.5*W23*H17.5"
        ..OR.. 37.75" ..OR.. 85.75" ..OR.. 1*3"+3*6"+14*12" ..OR.. 120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 16: Illegal quoting, probably in the following text: "86003-6-1.jpg
        ..OR.. 86003-6-3.jpg" ..OR.. L28"*W26.75"*H1.5" ..OR.. L30.5*W30.5*H17.5"
        ..OR.. 61.75" ..OR.. 85.75" ..OR.. 3*3"+4*6"+22*12" ..OR.. 120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 17: Illegal quoting, probably in the following text: "86031-3-1.jpg
        ..OR.. 86031-3-3.jpg" ..OR.. D5*H1" ..OR.. L15.5*W16.5*H11.75" ..OR.. 25.5"
        ..OR.. 79.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 18: Illegal quoting, probably in the following text: "86036-3-1.jpg
        ..OR.. L28.5*W11*H12.5" ..OR.. D5*H1" ..OR.. 7" ..OR.. W3*H12"'
    - - :warning
      - 'Line 19: Illegal quoting, probably in the following text: "86032-24-1.jpg
        ..OR.. 86032-24-3.jpg" ..OR.. D5*H1" ..OR.. L24.75*W21*H24.5" ..OR.. 29.25"
        ..OR.. 102.5" ..OR.. 72" ..OR.. 1*12" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 20: Illegal quoting, probably in the following text: "86033-16-1.jpg
        ..OR.. 86033-16-2.jpg" ..OR.. D5*H1" ..OR.. L19*W19*H23" ..OR.. 25.5" ..OR..
        97.75" ..OR.. 72" ..OR.. 1*10.25" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 21: Illegal quoting, probably in the following text: "86034-8-1.jpg
        ..OR.. 86034-8-3.jpg" ..OR.. D5*H1" ..OR.. L18.5*W18.5*H16.25" ..OR.. 19.25"
        ..OR.. 88.5" ..OR.. 72" ..OR.. 1*10.25" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 22: Illegal quoting, probably in the following text: "85190-10-1.jpg
        ..OR.. 85190-10-3.jpg" ..OR.. D7.13"*1.66" ..OR.. L28*W24*H27" ..OR.. 37"
        ..OR.. 110" ..OR.. 1*72" ..OR.. 120" ..OR.. L12.13*W9.13*D4"'
    - - :warning
      - 'Line 23: Illegal quoting, probably in the following text: "85191-11.jpg ..OR..
        85191-11_1.jpg" ..OR.. D7*H1.5" ..OR.. L55*W24*H15" ..OR.. 26" ..OR.. 62"
        ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 24: Illegal quoting, probably in the following text: D7*H1.5" ..OR..
        L44*W24*H15" ..OR.. 55" ..OR.. 127" ..OR.. 1*72" ..OR.. 120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 25: Illegal quoting, probably in the following text: D7*H1.5" ..OR..
        L29*W20*H15" ..OR.. 37" ..OR.. 109" ..OR.. 1*72" ..OR.. 120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 26: Illegal quoting, probably in the following text: "85195-2-1.jpg
        ..OR.. 85195-2-4.jpg" ..OR.. D5.88"*H1.13" ..OR.. L18*W15*H14" ..OR.. 7" ..OR..
        L12.13*W9.13*D4"'
    - - :warning
      - 'Line 27: Illegal quoting, probably in the following text: L13*W13*H16" ..OR..
        D5.88*H1.4" ..OR.. 7" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 28: Illegal quoting, probably in the following text: "85390-10-1.jpg
        ..OR.. 85390-10-4.jpg" ..OR.. D6"*H1.38" ..OR.. L26*W32*H27" ..OR.. 32" ..OR..
        106" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 29: Illegal quoting, probably in the following text: "85490-10-1.jpg
        ..OR.. 85490-10-5.jpg" ..OR.. D6"*H1.38" ..OR.. L26*W32*H27" ..OR.. 32" ..OR..
        106" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 30: Illegal quoting, probably in the following text: "85391-6-1.jpg
        ..OR.. 85391-6-5.jpg" ..OR.. D6"*H1.38" ..OR.. L26*W34*H15" ..OR.. 29" ..OR..
        103" ..OR.. 1*72" ..OR.. 1*9.5" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 31: Illegal quoting, probably in the following text: "85491-6-1.jpg
        ..OR.. 85491-6-5.jpg" ..OR.. D6"*H1.38" ..OR.. L26*W34*H15" ..OR.. 29" ..OR..
        103" ..OR.. 1*72" ..OR.. 1*9.5" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 32: Illegal quoting, probably in the following text: "85394-5-1.jpg
        ..OR.. 85394-5-5.jpg" ..OR.. D7.13"*0.88" ..OR.. L22*W28*H17" ..OR.. 25" ..OR..
        56" ..OR.. 3*12" ..OR.. 72" ..OR.. L19.25*W4.75*D12.25"'
    - - :warning
      - 'Line 33: Illegal quoting, probably in the following text: "85494-5-1.jpg
        ..OR.. 85494-5-5.jpg" ..OR.. D7.13"*0.88" ..OR.. L22*W28*H17" ..OR.. 25" ..OR..
        56" ..OR.. 3*12" ..OR.. 72" ..OR.. L19.25*W4.75*D12.25"'
    - - :warning
      - 'Line 34: Illegal quoting, probably in the following text: "85492-10-1.jpg
        ..OR.. 85492-10-3.jpg" ..OR.. L15.75"*W6"*H1.25" ..OR.. L36.5*W20.75*H28"
        ..OR.. 24.75" ..OR.. 97" ..OR.. 72" ..OR.. 2*12" ..OR.. 120" ..OR.. D12.25*H4.75"'
    - - :warning
      - 'Line 35: Illegal quoting, probably in the following text: "85592-10-1.jpg
        ..OR.. 85592-10-3.jpg" ..OR.. L15.75"*W6"*H1.25" ..OR.. L36.5*W20.75*H28"
        ..OR.. 24.75" ..OR.. 97" ..OR.. 72" ..OR.. 2*12" ..OR.. 120" ..OR.. D12.25*H4.75"'
    - - :warning
      - 'Line 36: Illegal quoting, probably in the following text: "85395-1-1.jpg
        ..OR.. 85395-1-3.jpg" ..OR.. L21*W22*H8" ..OR.. D4.75"*H0.75" ..OR.. 7" ..OR..
        L19.25*W4.75*D15.63"'
    - - :warning
      - 'Line 37: Illegal quoting, probably in the following text: "85495-1-1.jpg
        ..OR.. 85495-1-3.jpg" ..OR.. L21*W22*H8" ..OR.. D4.75"*H0.75" ..OR.. 7" ..OR..
        L19.25*W4.75*D15.63"'
    - - :warning
      - 'Line 38: Illegal quoting, probably in the following text: "85250-16-1.jpg
        ..OR.. 85250-16-4.jpg" ..OR.. L38*W38*H23" ..OR.. 33" ..OR.. 69" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 39: Illegal quoting, probably in the following text: "85350-16-1.jpg
        ..OR.. 85350-16-4.jpg" ..OR.. L38*W38*H23" ..OR.. 33" ..OR.. 69" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 40: Illegal quoting, probably in the following text: "85251-9-1.jpg
        ..OR.. 85251-9-4.jpg" ..OR.. L31*W31*H21" ..OR.. 26" ..OR.. 62" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 41: Illegal quoting, probably in the following text: "85351-9-1.jpg
        ..OR.. 85351-9-5.jpg" ..OR.. L31*W31*H21" ..OR.. 26" ..OR.. 62" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 42: Illegal quoting, probably in the following text: "85254-6-1.jpg
        ..OR.. 85254-6-4.jpg" ..OR.. W17.75"*D4.75"*H0.8" ..OR.. L15*W50*H13" ..OR..
        18" ..OR.. 54" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 43: Illegal quoting, probably in the following text: "85354-6-1.jpg
        ..OR.. 85354-6-5.jpg" ..OR.. W17.75"*D4.75"*H0.8" ..OR.. L15*W50*H13" ..OR..
        18" ..OR.. 54" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 44: Illegal quoting, probably in the following text: "85256-4-1.jpg
        ..OR.. 85256-4-3.jpg" ..OR.. L14*W19*H14" ..OR.. L16.5"*W5.5"*H0.75" ..OR..
        7" ..OR.. L9*W3"'
    - - :warning
      - 'Line 45: Illegal quoting, probably in the following text: "85356-4-1.jpg
        ..OR.. 85356-4-3.jpg" ..OR.. L14*W19*H14" ..OR.. L16.5"*W5.5"*H0.75" ..OR..
        7" ..OR.. L9*W3"'
    - - :warning
      - 'Line 46: Illegal quoting, probably in the following text: "85133-16.jpg ..OR..
        85133-16_1.jpg" ..OR.. D5.4*H0.88" ..OR.. L24*W24*H32" ..OR.. L30*W30*H30"
        ..OR.. 47" ..OR.. 117" ..OR.. 1*72" ..OR.. 120" ..OR.. "L21*W4.88" ..OR..
        L21*W4.88" ..OR.. L18.75*W4.88" ..OR.. L15.4*W4.88"'
    - - :warning
      - 'Line 47: Illegal quoting, probably in the following text: "85130-7-1.jpg
        ..OR.. 85130-7-4.jpg" ..OR.. L16.5"*4.75"*H0.88" ..OR.. L49*W16*H28" ..OR..
        29" ..OR.. 101" ..OR.. 1*72" ..OR.. 2*19.25" ..OR.. 120"'
    - - :warning
      - 'Line 48: Illegal quoting, probably in the following text: D5.4*H0.88" ..OR..
        L24*W24*H37" ..OR.. 39" ..OR.. 111" ..OR.. 1*72" ..OR.. 120" ..OR.. "L25*W4.75"
        ..OR.. L16.75*W4.75" ..OR.. L20*W4.75"'
    - - :warning
      - 'Line 49: Illegal quoting, probably in the following text: D5.4*H0.88" ..OR..
        L23*W23*H34" ..OR.. 34" ..OR.. 106" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 50: Illegal quoting, probably in the following text: D5.88*H0.75" ..OR..
        L23*W23*H16" ..OR.. 1*8.5" ..OR.. 7" ..OR.. L8.25*W3.25"'
    - - :warning
      - 'Line 51: Illegal quoting, probably in the following text: L15*W12*H12" ..OR..
        L7.1*W4.75*H0.75" ..OR.. 7" ..OR.. "L7.6*W3.1" ..OR.. L9.6*W3.1"'
    - - :warning
      - 'Line 52: Illegal quoting, probably in the following text: "85422-12-1.jpg
        ..OR.. 85422-12-3.jpg" ..OR.. D5.88"*H1" ..OR.. L37*W37*H42" ..OR.. 49" ..OR..
        114.5" ..OR.. 1*72" ..OR.. 1*9+1*12" ..OR.. 120"'
    - - :warning
      - 'Line 53: Illegal quoting, probably in the following text: "85421-8-1.jpg
        ..OR.. 85421-8-3.jpg" ..OR.. D5.88"*H1" ..OR.. L25*W25*H30" ..OR.. 35" ..OR..
        108.75" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120"'
    - - :warning
      - 'Line 54: Illegal quoting, probably in the following text: "85420-12-1.jpg
        ..OR.. 85420-12-5.jpg" ..OR.. L21.5"*W4.75"*H0.75" ..OR.. L55*W14*H23" ..OR..
        26" ..OR.. 99" ..OR.. 1*72" ..OR.. 2*12" ..OR.. 120"'
    - - :warning
      - 'Line 55: Illegal quoting, probably in the following text: "85424-1-1.jpg
        ..OR.. 85424-1-3.jpg" ..OR.. D4.75"*H1" ..OR.. L15*W11*H14" ..OR.. 24" ..OR..
        59.5" ..OR.. 72"'
    - - :warning
      - 'Line 56: Illegal quoting, probably in the following text: "85425-5-1.jpg
        ..OR.. 85425-5-4.jpg" ..OR.. D7.13"*H0.75" ..OR.. L23*W23*H11" ..OR.. 7"'
    - - :warning
      - 'Line 57: Illegal quoting, probably in the following text: "85426-4-1.jpg
        ..OR.. 85426-4-5.jpg" ..OR.. L20*W9*H9" ..OR.. L13.75"*W5.13"*H0.75" ..OR..
        7"'
    - - :warning
      - 'Line 58: Illegal quoting, probably in the following text: "85427-6-1.jpg
        ..OR.. 85427-6-5.jpg" ..OR.. L30*W9*H9" ..OR.. L13.75"*W5.13"*H0.75" ..OR..
        7"'
    - - :warning
      - 'Line 59: Illegal quoting, probably in the following text: "85423-1-1.jpg
        ..OR.. 85423-1-4.jpg" ..OR.. L19*W10*H9" ..OR.. L12.38"*W5"*H1" ..OR.. 7"'
    - - :warning
      - 'Line 60: Illegal quoting, probably in the following text: "85202-16.jpg ..OR..
        85202-16_1.jpg" ..OR.. D5.5*H1" ..OR.. L39*W39*H35" ..OR.. L31*W19*H16" ..OR..
        51" ..OR.. 125" ..OR.. 2*72" ..OR.. 120" ..OR.. "L11.8*W6" ..OR.. L9.6*W4.75"
        ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 61: Illegal quoting, probably in the following text: "85207-9.jpg ..OR..
        85207-9-2.jpg" ..OR.. D5.5"*H1" ..OR.. L28*W28*H30" ..OR.. 40" ..OR.. 112"
        ..OR.. 1*72" ..OR.. 120" ..OR.. "L11.75*W5.88"'
    - - :warning
      - 'Line 62: Illegal quoting, probably in the following text: +L9.63*W4.75"'
    - - :warning
      - 'Line 63: Illegal quoting, probably in the following text: +L6.5*W4.88"'
    - - :warning
      - 'Line 64: Illegal quoting, probably in the following text: D5.5*H1" ..OR..
        L31*W31*H30" ..OR.. 30" ..OR.. 103" ..OR.. 1*72" ..OR.. 120" ..OR.. "L11.8*W6"
        ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 65: Illegal quoting, probably in the following text: "85203-6.jpg ..OR..
        85203-6_1.jpg" ..OR.. L15*W4.4*H0.75" ..OR.. L54*W13*H14" ..OR.. 26" ..OR..
        98" ..OR.. 1*72" ..OR.. 120" ..OR.. "L11.8*W6" ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 66: Illegal quoting, probably in the following text: "85200-6-1.jpg
        ..OR.. 85200-6-3.jpg" ..OR.. D5.5"*H1" ..OR.. L26*W26*H16" ..OR.. 24" ..OR..
        96" ..OR.. 1*72" ..OR.. 120" ..OR.. "L11.75*W5.88"'
    - - :warning
      - 'Line 67: Illegal quoting, probably in the following text: +L9.63*W4.75"'
    - - :warning
      - 'Line 68: Illegal quoting, probably in the following text: +L6.5*W4.88"'
    - - :warning
      - 'Line 69: Illegal quoting, probably in the following text: "85206-4-1.jpg
        ..OR.. 85206-4-4.jpg" ..OR.. L41*W31*H8" ..OR.. L25.63"*W4.75"*H1" ..OR..
        7" ..OR.. "L9.63*W4.75"'
    - - :warning
      - 'Line 70: Illegal quoting, probably in the following text: L7.63*W4.25"'
    - - :warning
      - 'Line 71: Illegal quoting, probably in the following text: L6.13*W3.88"'
    - - :warning
      - 'Line 72: Illegal quoting, probably in the following text: "85205-2-1.jpg
        ..OR.. 85205-2-5.jpg" ..OR.. L15*W23*H8" ..OR.. L17.75"*W4.75"*H1" ..OR..
        7" ..OR.. "L9.63*W4.75"'
    - - :warning
      - 'Line 73: Illegal quoting, probably in the following text: L7.63*W4.25"'
    - - :warning
      - 'Line 74: Illegal quoting, probably in the following text: L6.13*W3.88"'
    - - :warning
      - 'Line 75: Illegal quoting, probably in the following text: L16*W10*H9" ..OR..
        L6*W4.5*H0.63" ..OR.. 23" ..OR.. 90" ..OR.. 7" ..OR.. "L11.8*W6" ..OR.. L9.6*W4.75"
        ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 76: Illegal quoting, probably in the following text: "85412-17-1.jpg
        ..OR.. 85412-17-5.jpg" ..OR.. D5.88"*H0.75" ..OR.. L42.5*W42.5*H22" ..OR..
        L42.25*W31.5*H24.5" ..OR.. 33" ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 77: Illegal quoting, probably in the following text: "85512-17-1.jpg
        ..OR.. 85512-17-5.jpg" ..OR.. D5.88"*H0.75" ..OR.. L42.5*W42.5*H22" ..OR..
        L42.25*W31.5*H24.5" ..OR.. 33" ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 78: Illegal quoting, probably in the following text: D5.5"*H0.75" ..OR..
        L42.5*42.5*22" ..OR.. L31.5*W42.25*H24.5" ..OR.. 33" ..OR.. 84" ..OR.. 1*3"+1*6"+4*12"
        ..OR.. 120" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 79: Illegal quoting, probably in the following text: "85414-20-1.jpg
        ..OR.. 85414-20-5.jpg" ..OR.. D5.88"*H0.75" ..OR.. L34*W34*H35" ..OR.. L42*W29*H25"
        ..OR.. 14" ..OR.. 80" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 80: Illegal quoting, probably in the following text: "85514-20-1.jpg
        ..OR.. 85514-20-6.jpg" ..OR.. D5.88"*H0.75" ..OR.. L34*W34*H35" ..OR.. L42*W29*H25"
        ..OR.. 14" ..OR.. 80" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 81: Illegal quoting, probably in the following text: D6*H0.75" ..OR..
        L34*W34*H35" ..OR.. L29*W42*H25" ..OR.. 43.75" ..OR.. 94" ..OR.. 1*3"+1*6"+4*12"
        ..OR.. 120" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 82: Illegal quoting, probably in the following text: "85411-13-1.jpg
        ..OR.. 85411-13-5.jpg" ..OR.. D5.5"*H0.75" ..OR.. L33*W33*H28" ..OR.. 29"
        ..OR.. 65" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 83: Illegal quoting, probably in the following text: "85511-13-1.jpg
        ..OR.. 85511-13-6.jpg" ..OR.. D5.5"*H0.75" ..OR.. L33*W33*H28" ..OR.. 29"
        ..OR.. 65" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 84: Illegal quoting, probably in the following text: "85621-13-1.jpg
        ..OR.. 85621-13-4.jpg" ..OR.. D5.25"*H0.75" ..OR.. L33.5*W33.5*H27.75" ..OR..
        18.5" ..OR.. 64.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25
        xH1.25"'
    - - :warning
      - 'Line 85: Illegal quoting, probably in the following text: "85410-7-1.jpg
        ..OR.. 85410-7-6.jpg" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H27" ..OR.. 27"
        ..OR.. 63" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 86: Illegal quoting, probably in the following text: "85510-7-1.jpg
        ..OR.. 85510-7-5.jpg" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H27" ..OR.. 27"
        ..OR.. 63" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 87: Illegal quoting, probably in the following text: "85620-7-1.jpg
        ..OR.. 85620-7-2.jpg" ..OR.. D5.25"*H0.75" ..OR.. L27.75*W27.75*H27.25" ..OR..
        27" ..OR.. 63" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 88: Illegal quoting, probably in the following text: "85413-6-1.jpg
        ..OR.. 85413-6-4.jpg" ..OR.. L15.75"*W5.13"*H1" ..OR.. L50*W18*H23" ..OR..
        18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 89: Illegal quoting, probably in the following text: "85513-6-1.jpg
        ..OR.. 85513-6-5.jpg" ..OR.. L15.75"*W5.13"*H1" ..OR.. L50*W18*H23" ..OR..
        18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 90: Illegal quoting, probably in the following text: D15.75" xH5.25"
        ..OR.. L17.75*W50.5*H23.25" ..OR.. L15.75*W5.25*H1" ..OR.. 18.25" ..OR.. 69"
        ..OR.. 2*3"+2*6"+8*12" ..OR.. 120" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 91: Illegal quoting, probably in the following text: "85415-2-1.jpg
        ..OR.. 85415-2-3.jpg" ..OR.. L22*W16*H17" ..OR.. L6.25"*W5.88"*H0.75" ..OR..
        7" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 92: Illegal quoting, probably in the following text: "85515-2-1.jpg
        ..OR.. 85515-2-3.jpg" ..OR.. L22*W16*H17" ..OR.. L6.25"*W5.88"*H0.75" ..OR..
        7" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 93: Illegal quoting, probably in the following text: L15.75*W21.75*H16.5"
        ..OR.. D6xH6.25" ..OR.. 7" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 94: Illegal quoting, probably in the following text: D5.5*H1" ..OR..
        L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR.. 75" ..OR.. 1*6"+3*12" ..OR..
        120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 95: Illegal quoting, probably in the following text: D5.5*H1" ..OR..
        L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR.. 75" ..OR.. 1*6"+3*12" ..OR..
        120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 96: Illegal quoting, probably in the following text: D5.5*H1" ..OR..
        L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR.. 75.25" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 97: Illegal quoting, probably in the following text: D5.5*H1" ..OR..
        L30*W29*H24" ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 98: Illegal quoting, probably in the following text: "85262-13.jpg ..OR..
        85262-13_1.jpg" ..OR.. D5.5*H1" ..OR.. L30*W29*H24" ..OR.. 37" ..OR.. 66"
        ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 99: Illegal quoting, probably in the following text: D5.5*H1" ..OR..
        L30*W29*H24" ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 100: Illegal quoting, probably in the following text: "85161-5.jpg ..OR..
        85161-5_1.jpg" ..OR.. D5.5*H1" ..OR.. L23*W20*H23" ..OR.. 28" ..OR.. 64" ..OR..
        1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 101: Illegal quoting, probably in the following text: D5.5*H1" ..OR..
        L23*W20*H23" ..OR.. 28" ..OR.. 64" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 102: Illegal quoting, probably in the following text: D5.5*H1" ..OR..
        L23*W20*H23" ..OR.. 28" ..OR.. 64" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 103: Illegal quoting, probably in the following text: L18*W13*H16" ..OR..
        L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 104: Illegal quoting, probably in the following text: L18*W13*H16" ..OR..
        L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 105: Illegal quoting, probably in the following text: L18*W13*H16" ..OR..
        L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 106: Illegal quoting, probably in the following text: "85433-12-1.jpg
        ..OR.. 85433-12-3.jpg" ..OR.. D5.88*H0.75" ..OR.. L29*W29*H12" ..OR.. 58"
        ..OR.. 126" ..OR.. 1*72" ..OR.. 144"'
    - - :warning
      - 'Line 107: Illegal quoting, probably in the following text: "85432-8-1.jpg
        ..OR.. 85432-8-3.jpg" ..OR.. D5.13*H0.75" ..OR.. L56*W56*H14" ..OR.. 44" ..OR..
        112" ..OR.. 1*72" ..OR.. 144"'
    - - :warning
      - 'Line 108: Illegal quoting, probably in the following text: "85431-6-1.jpg
        ..OR.. 85431-6-3.jpg" ..OR.. D5.13*H0.75" ..OR.. L41*W41*H12" ..OR.. 36" ..OR..
        104" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 109: Illegal quoting, probably in the following text: "85430-4-1.jpg
        ..OR.. 85430-4-3.jpg" ..OR.. D4.75*H0.75" ..OR.. L31*W31*H10" ..OR.. 21" ..OR..
        89" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 110: Illegal quoting, probably in the following text: "85435-8-1.jpg
        ..OR.. 85435-8-5.jpg" ..OR.. D5.13*H0.75" ..OR.. L10*W16*H11" ..OR.. 18" ..OR..
        54" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 111: Illegal quoting, probably in the following text: "85434-6-1.jpg
        ..OR.. 85434-6-4.jpg" ..OR.. D5.13*H0.75" ..OR.. L37*W37*H13" ..OR.. 16" ..OR..
        53" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 112: Illegal quoting, probably in the following text: "85437-3-1.jpg
        ..OR.. 85437-3-5.jpg" ..OR.. D5.13*H0.75" ..OR.. L11*W15*H7" ..OR.. 7"'
    - - :warning
      - 'Line 113: Illegal quoting, probably in the following text: "85436-1-1.jpg
        ..OR.. 85436-1-4.jpg" ..OR.. D5.13*H0.75" ..OR.. L19*W19*H12" ..OR.. 17" ..OR..
        53" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 114: Illegal quoting, probably in the following text: "85438-1-1.jpg
        ..OR.. 85438-1-4.jpg" ..OR.. L14.5*W10.75*H7.5" ..OR.. L9"*4.75"*H0.75" ..OR..
        7"'
    - - :warning
      - 'Line 115: Illegal quoting, probably in the following text: "85232-12.jpg
        ..OR.. 85232-12_1.jpg" ..OR.. D5.5*H1" ..OR.. L30*W30*H14" ..OR.. 42" ..OR..
        115" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 116: Illegal quoting, probably in the following text: L16.1*W5.88*H0.88"
        ..OR.. L50*W22*H11" ..OR.. 27" ..OR.. 100" ..OR.. 2*72" ..OR.. 2*15" ..OR..
        120" ..OR.. L47.25*W14.25*H8.25"'
    - - :warning
      - 'Line 117: Illegal quoting, probably in the following text: D5.5*H1" ..OR..
        L30*W30*H25" ..OR.. 28" ..OR.. 101" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 118: Illegal quoting, probably in the following text: D5.5*H1" ..OR..
        L26*W26*H15" ..OR.. 30" ..OR.. 103" ..OR.. 1*72" ..OR.. 120" ..OR.. D23*H8"'
    - - :warning
      - 'Line 119: Illegal quoting, probably in the following text: D5.5*H1" ..OR..
        L18*W18*H15" ..OR.. 1*3.25" ..OR.. 7" ..OR.. D15*H7"'
    - - :warning
      - 'Line 120: Illegal quoting, probably in the following text: D5.5*H1" ..OR..
        L16*W12*H10" ..OR.. 20" ..OR.. 56" ..OR.. 1*6"+3*12" ..OR.. 120"'
    - - :warning
      - 'Line 121: Illegal quoting, probably in the following text: L39*W9*H9" ..OR..
        L35.38*W4.5*H0.75" ..OR.. 7" ..OR.. L36*W4.8*H5.88"'
    - - :warning
      - 'Line 122: Illegal quoting, probably in the following text: L28*W9*H9" ..OR..
        L24.38*W4.5*H0.75" ..OR.. 7" ..OR.. L25*W4.8*H4.38"'
    - - :warning
      - 'Line 123: Illegal quoting, probably in the following text: L11*W10*H8" ..OR..
        L6.5*W6.5*H0.75" ..OR.. 7" ..OR.. L8.38*W7.25*H4"'
    - - :warning
      - 'Line 124: Illegal quoting, probably in the following text: D5.1*H0.75" ..OR..
        L43*W40*H13" ..OR.. 67" ..OR.. 103" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 125: Illegal quoting, probably in the following text: "85244-7.jpg ..OR..
        85244-7_1.jpg" ..OR.. D23.63*H1" ..OR.. L28*W26*H18" ..OR.. 52" ..OR.. 97"
        ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 126: Illegal quoting, probably in the following text: "85242-6.jpg ..OR..
        85242-6_1.jpg" ..OR.. D5.1*H0.75" ..OR.. L32*W27*H13" ..OR.. 53" ..OR.. 89"
        ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 127: Illegal quoting, probably in the following text: L50.38*W8.75*H0.75"
        ..OR.. L54*W15*H13" ..OR.. 32" ..OR.. 97" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 128: Illegal quoting, probably in the following text: D5.1*H0.75" ..OR..
        L26*W22*H18" ..OR.. 45" ..OR.. 81" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 129: Illegal quoting, probably in the following text: D5.1*H0.75" ..OR..
        L24*W15*H8" ..OR.. 31" ..OR.. 67" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 130: Illegal quoting, probably in the following text: L35*W13*H10" ..OR..
        7" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 131: Illegal quoting, probably in the following text: "85286-68-1.jpg
        ..OR.. 85286-68-3.jpg" ..OR.. D20"*H1.38" ..OR.. L24*W24*H31" ..OR.. 20" ..OR..
        D3.88"'
    - - :warning
      - 'Line 132: Illegal quoting, probably in the following text: "85283-47-1.jpg
        ..OR.. 85283-47-4.jpg" ..OR.. D20"*H1.38" ..OR.. L24*W24*H16" ..OR.. 20" ..OR..
        D3.88"'
    - - :warning
      - 'Line 133: Illegal quoting, probably in the following text: "85281-19-1.jpg
        ..OR.. 85281-19-4.jpg" ..OR.. D20"*H1.38" ..OR.. L24*W24*H16" ..OR.. 20" ..OR..
        D3.88"'
    - - :warning
      - 'Line 134: Illegal quoting, probably in the following text: "85289-5-1.jpg
        ..OR.. 85289-5-4.jpg" ..OR.. L8*W12*H20" ..OR.. L8.63"*W5.75"*H1.38" ..OR..
        7" ..OR.. D3.88"'
    - - :warning
      - 'Line 135: Illegal quoting, probably in the following text: "85288-3-1.jpg
        ..OR.. 85288-3-5.jpg" ..OR.. L8*W12*H15" ..OR.. L8.63"*W5.75"*H1.38" ..OR..
        7" ..OR.. D3.88"'
    - - :warning
      - 'Line 136: Illegal quoting, probably in the following text: "85216-14.jpg
        ..OR.. 85216-14_1.jpg" ..OR.. L50.5*W9.88*H1.38" ..OR.. L54*W13*H15" ..OR..
        23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 137: Illegal quoting, probably in the following text: "85214-13.jpg
        ..OR.. 85214-13_1.jpg" ..OR.. D24*H1.38" ..OR.. L35*W27*H9" ..OR.. 23" ..OR..
        90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 138: Illegal quoting, probably in the following text: L36*W9.88*H1.38"
        ..OR.. L39*W13*H15" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 139: Illegal quoting, probably in the following text: "85213-6.jpg ..OR..
        85213-6_1.jpg" ..OR.. D16*H1.38" ..OR.. L26*W19*H9" ..OR.. 23" ..OR.. 90"
        ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 140: Illegal quoting, probably in the following text: D9.88*H1.25" ..OR..
        L16*W15*H9" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 141: Illegal quoting, probably in the following text: D5.88*H1.25" ..OR..
        L15*W9*H9" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 142: Illegal quoting, probably in the following text: "85401-9-1.jpg
        ..OR.. 85401-9-3.jpg" ..OR.. D24*1.38" ..OR.. L28*W28*H15" ..OR.. 51" ..OR..
        75" ..OR.. 1*5.25+31*32+1*7.38+1*1.38+1*8.63+1*10.13+1*6+1*8.75" ..OR.. 7"
        ..OR.. D4"'
    - - :warning
      - 'Line 143: Illegal quoting, probably in the following text: "85400-5-1.jpg
        ..OR.. 85400-5-3.jpg" ..OR.. D15.75"*1.38" ..OR.. L20*W20*H15" ..OR.. 42"
        ..OR.. 66" ..OR.. 1*9"+15*12"+1*1.38"+1*6"+1*10.38"+1*3" ..OR.. 7" ..OR..
        D4"'
    - - :warning
      - 'Line 144: Illegal quoting, probably in the following text: "85404-5-1.jpg
        ..OR.. 85404-5-5.jpg" ..OR.. L43.25"*W6.25"*H1.38" ..OR.. L10*W47*H15" ..OR..
        21" ..OR.. 57" ..OR.. 7*6+15*12" ..OR.. 7" ..OR.. D4"'
    - - :warning
      - 'Line 145: Illegal quoting, probably in the following text: "85406-1-1.jpg
        ..OR.. 85406-1-4.jpg" ..OR.. D5.5"*H1.25" ..OR.. L9*W17*H8" ..OR.. 15" ..OR..
        51" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D4"'
    - - :warning
      - 'Line 146: Illegal quoting, probably in the following text: "85407-1-1.jpg
        ..OR.. 85407-1-5.jpg" ..OR.. L13.13"*5.38"*1.25" ..OR.. L11*W16*H9" ..OR..
        7" ..OR.. D4"'
    - - :warning
      - 'Line 147: Illegal quoting, probably in the following text: 6.25"*1" ..OR..
        L40*W40*H20" ..OR.. 41" ..OR.. 109" ..OR.. 1*72" ..OR.. 120" ..OR.. L13.75"*D1"'
    - - :warning
      - 'Line 148: Illegal quoting, probably in the following text: L17.75"*W5"*H1"
        ..OR.. L17*W48*H18" ..OR.. 33" ..OR.. 100" ..OR.. 1*72" ..OR.. 120" ..OR..
        L13.75"*D1"'
    - - :warning
      - 'Line 149: Illegal quoting, probably in the following text: "85101-8.jpg ..OR..
        85101-8_1.jpg" ..OR.. D5.1*H0.75" ..OR.. L33*W33*H16" ..OR.. 29" ..OR.. 101"
        ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 150: Illegal quoting, probably in the following text: D5.1*H0.75" ..OR..
        L27*W27*H14" ..OR.. 23" ..OR.. 95" ..OR.. 1*72" ..OR.. 1*8.7" ..OR.. 120"
        ..OR.. D1*H10.75"'
    - - :warning
      - 'Line 151: Illegal quoting, probably in the following text: D5.1*H0.75" ..OR..
        L21*W21*H14" ..OR.. 21" ..OR.. 92" ..OR.. 1*72" ..OR.. 1*6" ..OR.. 120" ..OR..
        D1*H10.75"'
    - - :warning
      - 'Line 152: Illegal quoting, probably in the following text: "85109-4-1.jpg
        ..OR.. 85109-4-2.jpg" ..OR.. D5"*D0.75" ..OR.. L25*W25*H10" ..OR.. 7" ..OR..
        L7*D0.75"'
    - - :warning
      - 'Line 153: Illegal quoting, probably in the following text: "85108-4-1.jpg
        ..OR.. 85108-4-5.jpg" ..OR.. L10*W39*H13" ..OR.. L33"*W5"*H0.75" ..OR.. 7"
        ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 154: Illegal quoting, probably in the following text: "85107-3-1.jpg
        ..OR.. 85107-3-2.jpg" ..OR.. L10*W30*H13" ..OR.. L23.5"*W5"*H0.75" ..OR..
        7" ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 155: Illegal quoting, probably in the following text: D5.1*H0.75" ..OR..
        L20*W18*H11" ..OR.. 29" ..OR.. 101" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120"
        ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 156: Illegal quoting, probably in the following text: "85106-1-1.jpg
        ..OR.. 85106-1-2.jpg" ..OR.. L11*W23*H15" ..OR.. L15"*W4.25"*H0.75" ..OR..
        7" ..OR.. L19.25*D0.72"'
    - - :warning
      - 'Line 157: Illegal quoting, probably in the following text: L18*W12*H11" ..OR..
        L8.25*W4.75*H0.75" ..OR.. 7" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 158: Illegal quoting, probably in the following text: "85171-12.jpg
        ..OR.. 85171-12_1.jpg" ..OR.. L35*W35*H15" ..OR.. 20" ..OR.. 83" ..OR.. 120"
        ..OR.. "L6.75*W1.5*H0.6" ..OR.. L8.3*W1.5*H0.6" ..OR.. L10*W1.5*H0.6"'
    - - :warning
      - 'Line 159: Illegal quoting, probably in the following text: L19.63*W5.5*H0.88"
        ..OR.. L53*W13*H15" ..OR.. 20" ..OR.. 83" ..OR.. 120" ..OR.. "L6.75*W1.5*H0.6"
        ..OR.. L8.3*W1.5*H0.6" ..OR.. L10*W1.5*H0.6"'
    - - :warning
      - 'Line 160: Illegal quoting, probably in the following text: L15*W12*H11" ..OR..
        L11.75*W9.4*H0.75" ..OR.. 7" ..OR.. "L6.75*W1.5*H0.6" ..OR.. L8.3*W1.5*H0.6"
        ..OR.. L10*W1.5*H0.6"'
    - - :warning
      - 'Line 161: Illegal quoting, probably in the following text: D7*H1.5" ..OR..
        L60*W30*H27" ..OR.. 34" ..OR.. 70" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 162: Illegal quoting, probably in the following text: "85182-9.jpg ..OR..
        85182-9_1.jpg" ..OR.. D7*H1.5" ..OR.. L35*W35*H28" ..OR.. 33" ..OR.. 105"
        ..OR.. 1*72" ..OR.. 120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 163: Illegal quoting, probably in the following text: D7*H1.5" ..OR..
        L32*W26*H17" ..OR.. 36" ..OR.. 109" ..OR.. 1*72" ..OR.. 120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 164: Illegal quoting, probably in the following text: L18*W13*H9" ..OR..
        D6*H1.5" ..OR.. 7" ..OR.. D6*H6"'
    - - :warning
      - 'Line 165: Illegal quoting, probably in the following text: "85270-12-1.jpg
        ..OR.. 85270-12-3.jpg" ..OR.. L35*W35*H40" ..OR.. L34*26*15" ..OR.. 49" ..OR..
        85" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. "D9.88""+D7.88"'
    - - :warning
      - 'Line 166: Unclosed quoted field in line 1.'
    - - :warning
      - 'Line 167: Illegal quoting, probably in the following text: "85370-12-1.jpg
        ..OR.. 85370-12-4.jpg" ..OR.. L35*W35*H40" ..OR.. L34*26*15" ..OR.. 49" ..OR..
        85" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. "D9.88""+D7.88"'
    - - :warning
      - 'Line 168: Unclosed quoted field in line 1.'
    - - :warning
      - 'Line 169: Illegal quoting, probably in the following text: "85271-12-1.jpg
        ..OR.. 85271-12-51.jpg" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H30.5" ..OR..
        L28*W18*H21" ..OR.. 43" ..OR.. 79" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. "D5.88""+D7.13"'
    - - :warning
      - 'Line 170: Unclosed quoted field in line 1.'
    - - :warning
      - 'Line 171: Illegal quoting, probably in the following text: "85371-12-1.jpg
        ..OR.. 85371-12-4.jpg" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H30.5" ..OR.. L28*W18*H21"
        ..OR.. 43" ..OR.. 79" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. "D5.88""+D7.13"'
    - - :warning
      - 'Line 172: Unclosed quoted field in line 1.'
    - - :warning
      - 'Line 173: Illegal quoting, probably in the following text: "85273-8-1.jpg
        ..OR.. 85273-8-4.jpg" ..OR.. L27.13"*W5.13"*H1" ..OR.. L59*W23.5*H22" ..OR..
        L26*W26*H20" ..OR.. 33" ..OR.. 70" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. D7.88"+D9.88"'
    - - :warning
      - 'Line 174: Illegal quoting, probably in the following text: "85373-8-1.jpg
        ..OR.. 85373-8-1.jpg" ..OR.. L27.13"*W5.13"*H1" ..OR.. L59*W23.5*H22" ..OR..
        L26*W26*H20" ..OR.. 33" ..OR.. 70" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. D7.88"+D9.88"'
    - - :warning
      - 'Line 175: Illegal quoting, probably in the following text: D5.13"*H0.75"
        ..OR.. L20*W25*H18" ..OR.. 28" ..OR.. 64" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        D13.75"'
    - - :warning
      - 'Line 176: Illegal quoting, probably in the following text: "85376-1-1.jpg
        ..OR.. 85376-1-3.jpg" ..OR.. D5.13"*H0.75" ..OR.. L20*W25*H18" ..OR.. 28"
        ..OR.. 64" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D13.75"'
    - - :warning
      - 'Line 177: Illegal quoting, probably in the following text: D5.13"*H0.75"
        ..OR.. L18*W21*H14" ..OR.. 24" ..OR.. 60" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        D9.88"'
    - - :warning
      - 'Line 178: Illegal quoting, probably in the following text: "85375-1-1.jpg
        ..OR.. 85375-1-2.jpg" ..OR.. D5.13"*H0.75" ..OR.. L18*W21*H14" ..OR.. 24"
        ..OR.. 60" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D9.88"'
    - - :warning
      - 'Line 179: Illegal quoting, probably in the following text: D6.4*H1.88" ..OR..
        L41*W41*H40" ..OR.. L32*W24*H24" ..OR.. L32*W24*H24" ..OR.. 48" ..OR.. 72"
        ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D10*H1.5"'
    - - :warning
      - 'Line 180: Illegal quoting, probably in the following text: "85122-12.jpg
        ..OR.. 85122-12_1.jpg" ..OR.. D6.4*H1.88" ..OR.. L31*W31*H31" ..OR.. L30*W24*H24"
        ..OR.. 36" ..OR.. 66" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D10*H1.5"'
    - - :warning
      - 'Line 181: Illegal quoting, probably in the following text: "85123-6.jpg ..OR..
        85123-6_1.jpg" ..OR.. D6.4*H1.88" ..OR.. L28*W26*H26" ..OR.. 1*6" ..OR.. 7"
        ..OR.. D10*H1.5"'
    - - :warning
      - 'Line 182: Illegal quoting, probably in the following text: "85124-8-1.jpg
        ..OR.. 85124-8-5.jpg" ..OR.. L16.88"*W5.88"*H0.88" ..OR.. L54*W14*H16" ..OR..
        13" ..OR.. 49" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. D9.63"*1.63"'
    - - :warning
      - 'Line 183: Illegal quoting, probably in the following text: "85125-3-1.jpg
        ..OR.. 85125-3-2.jpg" ..OR.. L24*W15*H13" ..OR.. D4.75"*H0.75" ..OR.. 7" ..OR..
        D9.63"*1.63"'
    - - :warning
      - 'Line 184: Illegal quoting, probably in the following text: D5.88*H0.88" ..OR..
        L28*W28*H29" ..OR.. 36" ..OR.. 72" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D23.75*H23.75"'
    - - :warning
      - 'Line 185: Illegal quoting, probably in the following text: D5.88*H0.88" ..OR..
        L19.5*W19.5*H20.75" ..OR.. 29" ..OR.. 65" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR..
        D15.75*H15.75"'
    - - :warning
      - 'Line 186: Illegal quoting, probably in the following text: "85221-1.jpg ..OR..
        85221-1_1.jpg" ..OR.. D5.88*H0.88" ..OR.. L11*W11*H13" ..OR.. 20" ..OR.. 56"
        ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D7.5*H7.5"'
    - - :warning
      - 'Line 187: Illegal quoting, probably in the following text: D5.5*H1" ..OR..
        L43*W43*H9" ..OR.. 34" ..OR.. 106" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 188: Illegal quoting, probably in the following text: D5.5*H1" ..OR..
        L32*W32*H9" ..OR.. 32" ..OR.. 102" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 189: Illegal quoting, probably in the following text: L21*W8*H7" ..OR..
        L18*W5.75*H1.25" ..OR.. 7"'
    - - :warning
      - 'Line 190: Illegal quoting, probably in the following text: "85111-6.jpg ..OR..
        85111-6_1.jpg" ..OR.. D5.1*H0.75" ..OR.. L40*W40*H22" ..OR.. 32" ..OR.. 80"
        ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D36*H18"'
    - - :warning
      - 'Line 191: Illegal quoting, probably in the following text: D5.1*H0.75" ..OR..
        L28*W28*H16" ..OR.. 32" ..OR.. 74" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D24*H12"'
    - - :warning
      - 'Line 192: Illegal quoting, probably in the following text: D5.1*H0.75" ..OR..
        L19*W19*H19" ..OR.. 30" ..OR.. 73" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D16*H15.5"'
    - - :warning
      - 'Line 193: Illegal quoting, probably in the following text: D5.5*H1" ..OR..
        L39*W39*H13" ..OR.. 24" ..OR.. 96" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 194: Illegal quoting, probably in the following text: "85141-6.jpg ..OR..
        85141-6_1.jpg" ..OR.. D5.5*H1" ..OR.. L30*W30*H12" ..OR.. 21" ..OR.. 93" ..OR..
        1*72" ..OR.. 120"'
    - - :warning
      - 'Line 195: Illegal quoting, probably in the following text: D5.5*H1" ..OR..
        L18*W18*H30" ..OR.. 24" ..OR.. 96" ..OR.. "Iron ..OR.. solid wood and glass"
        ..OR.. 1*72" ..OR.. 120" ..OR.. L11.6*W10*H3"'
    - - :warning
      - 'Line 196: Illegal quoting, probably in the following text: "65000-1.jpg ..OR..
        65000-6.jpg" ..OR.. W4.72"*H18"'
    - - :warning
      - 'Line 197: Illegal quoting, probably in the following text: "65001-1.jpg ..OR..
        65001-7.jpg" ..OR.. W4.72"*H24.7"'
    - - :warning
      - 'Line 200: Illegal quoting, probably in the following text: "65030-1.jpg ..OR..
        65030-4.jpg" ..OR.. W7"*H14.37"'
    - - :warning
      - 'Line 201: Illegal quoting, probably in the following text: "65031-1.jpg ..OR..
        65031-4.jpg" ..OR.. W7"*H24"'
    - - :warning
      - 'Line 204: Illegal quoting, probably in the following text: "65010-1.jpg ..OR..
        65010-5.jpg" ..OR.. W4.72"*H4.3"'
    - - :warning
      - 'Line 205: Illegal quoting, probably in the following text: "65011-1.jpg ..OR..
        65011-5.jpg" ..OR.. W4.72"*H4.3"'
 |
| 2026-06-16T06:11:10.550600 | ---
- - Products
  - - - :warning
      - 'Error running cleancsv: 2026/06/16 06:11:08 parse error on line 2, column
        122: bare " in non-quoted-field

        '
    - - :warning
      - 'Line 2: Illegal quoting, probably in the following text: "86010-1-1.jpg ..OR..
        86010-1-4.jpg" ..OR.. W9"*H16"*D9" ..OR.. L16.25*W14.5*H10.75" ..OR.. D5*H1.25"
        ..OR.. 7" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 3: Illegal quoting, probably in the following text: "86120-1-1.jpg ..OR..
        86120-1-5.jpg" ..OR.. W9"*H16"*D9" ..OR.. L16.25*W14.5*H10.75" ..OR.. D5*H1.25"
        ..OR.. 7" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 4: Illegal quoting, probably in the following text: "86013-1-1.jpg ..OR..
        86013-1-2.jpg" ..OR.. W9"*H10"*D9" ..OR.. D5*H1.25" ..OR.. L16.5*W16.5*H10.75"
        ..OR.. 17.5" ..OR.. 71" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 5: Illegal quoting, probably in the following text: "86123-1-1.jpg ..OR..
        86123-1-3.jpg" ..OR.. W9"*H10"*D9" ..OR.. D5*H1.25" ..OR.. L16.5*W16.5*H10.75"
        ..OR.. 17.5" ..OR.. 71" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 6: Illegal quoting, probably in the following text: "86011-2-1.jpg ..OR..
        86011-2-5.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 15.5" ..OR.. 70" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 7: Illegal quoting, probably in the following text: "86121-2-1.jpg ..OR..
        86121-2-5.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 15.5" ..OR.. 70" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 8: Illegal quoting, probably in the following text: "86015-1-1.jpg ..OR..
        86015-1-3.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 18" ..OR.. 72" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 9: Illegal quoting, probably in the following text: "86125-1-1.jpg ..OR..
        86125-1-2.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 18" ..OR.. 72" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 10: Illegal quoting, probably in the following text: "86014-6-1.jpg
        ..OR.. 86014-6-5.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 21" ..OR.. 74" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 11: Illegal quoting, probably in the following text: "86124-6-1.jpg
        ..OR.. 86124-6-5.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 21" ..OR.. 74" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 12: Illegal quoting, probably in the following text: "86017-6-1.jpg
        ..OR.. 86017-6-2.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 25" ..OR.. 79" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 13: Illegal quoting, probably in the following text: "86127-6-1.jpg
        ..OR.. 86127-6-2.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 25" ..OR.. 79" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 14: Illegal quoting, probably in the following text: "86001-1-1.jpg
        ..OR.. 86001-1-3.jpg" ..OR.. W8"*H12"*D8" ..OR.. D6"*H1" ..OR.. L20*W13*H14.25"
        ..OR.. 16.5" ..OR.. 70.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 15: Illegal quoting, probably in the following text: "86002-3-1.jpg
        ..OR.. 86002-3-3.jpg" ..OR.. W17"*Max86"*17" ..OR.. L16.75"*W15.75"*H1.5"
        ..OR.. L24.5*W23*H17.5" ..OR.. 37.75" ..OR.. 85.75" ..OR.. 1*3"+3*6"+14*12"
        ..OR.. 120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 16: Illegal quoting, probably in the following text: "86003-6-1.jpg
        ..OR.. 86003-6-3.jpg" ..OR.. W28"*Max86"*28" ..OR.. L28"*W26.75"*H1.5" ..OR..
        L30.5*W30.5*H17.5" ..OR.. 61.75" ..OR.. 85.75" ..OR.. 3*3"+4*6"+22*12" ..OR..
        120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 17: Illegal quoting, probably in the following text: "86031-3-1.jpg
        ..OR.. 86031-3-3.jpg" ..OR.. W10"*H20"*D10" ..OR.. D5*H1" ..OR.. L15.5*W16.5*H11.75"
        ..OR.. 25.5" ..OR.. 79.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 18: Illegal quoting, probably in the following text: "86036-3-1.jpg
        ..OR.. W15"*H35"*D6" ..OR.. L28.5*W11*H12.5" ..OR.. D5*H1" ..OR.. 7" ..OR..
        W3*H12"'
    - - :warning
      - 'Line 19: Illegal quoting, probably in the following text: "86032-24-1.jpg
        ..OR.. 86032-24-3.jpg" ..OR.. W36"*H26"*D36" ..OR.. D5*H1" ..OR.. L24.75*W21*H24.5"
        ..OR.. 29.25" ..OR.. 102.5" ..OR.. 72" ..OR.. 1*12" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 20: Illegal quoting, probably in the following text: "86033-16-1.jpg
        ..OR.. 86033-16-2.jpg" ..OR.. W28"*H22"*D28" ..OR.. D5*H1" ..OR.. L19*W19*H23"
        ..OR.. 25.5" ..OR.. 97.75" ..OR.. 72" ..OR.. 1*10.25" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 21: Illegal quoting, probably in the following text: "86034-8-1.jpg
        ..OR.. 86034-8-3.jpg" ..OR.. W28"*H15"*D28" ..OR.. D5*H1" ..OR.. L18.5*W18.5*H16.25"
        ..OR.. 19.25" ..OR.. 88.5" ..OR.. 72" ..OR.. 1*10.25" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 22: Illegal quoting, probably in the following text: "85190-10-1.jpg
        ..OR.. 85190-10-3.jpg" ..OR.. W35"*H32"*D35" ..OR.. D7.13"*1.66" ..OR.. L28*W24*H27"
        ..OR.. 37" ..OR.. 110" ..OR.. 1*72" ..OR.. 120" ..OR.. L12.13*W9.13*D4"'
    - - :warning
      - 'Line 23: Illegal quoting, probably in the following text: "85191-11.jpg ..OR..
        85191-11_1.jpg" ..OR.. W60"*H20"*D20" ..OR.. D7*H1.5" ..OR.. L55*W24*H15"
        ..OR.. 26" ..OR.. 62" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 24: Illegal quoting, probably in the following text: W26"*H52"*D26"
        ..OR.. D7*H1.5" ..OR.. L44*W24*H15" ..OR.. 55" ..OR.. 127" ..OR.. 1*72" ..OR..
        120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 25: Illegal quoting, probably in the following text: W24"*H33"*D24"
        ..OR.. D7*H1.5" ..OR.. L29*W20*H15" ..OR.. 37" ..OR.. 109" ..OR.. 1*72" ..OR..
        120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 26: Illegal quoting, probably in the following text: "85195-2-1.jpg
        ..OR.. 85195-2-4.jpg" ..OR.. W22"*H28"*D5" ..OR.. D5.88"*H1.13" ..OR.. L18*W15*H14"
        ..OR.. 7" ..OR.. L12.13*W9.13*D4"'
    - - :warning
      - 'Line 27: Illegal quoting, probably in the following text: W9"*H21"*D5" ..OR..
        L13*W13*H16" ..OR.. D5.88*H1.4" ..OR.. 7" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 28: Illegal quoting, probably in the following text: "85390-10-1.jpg
        ..OR.. 85390-10-4.jpg" ..OR.. W39"*H28"*D39" ..OR.. D6"*H1.38" ..OR.. L26*W32*H27"
        ..OR.. 32" ..OR.. 106" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 29: Illegal quoting, probably in the following text: "85490-10-1.jpg
        ..OR.. 85490-10-5.jpg" ..OR.. W39"*H28"*D39" ..OR.. D6"*H1.38" ..OR.. L26*W32*H27"
        ..OR.. 32" ..OR.. 106" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 30: Illegal quoting, probably in the following text: "85391-6-1.jpg
        ..OR.. 85391-6-5.jpg" ..OR.. W32"*H25"*D32" ..OR.. D6"*H1.38" ..OR.. L26*W34*H15"
        ..OR.. 29" ..OR.. 103" ..OR.. 1*72" ..OR.. 1*9.5" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 31: Illegal quoting, probably in the following text: "85491-6-1.jpg
        ..OR.. 85491-6-5.jpg" ..OR.. W32"*H25"*D32" ..OR.. D6"*H1.38" ..OR.. L26*W34*H15"
        ..OR.. 29" ..OR.. 103" ..OR.. 1*72" ..OR.. 1*9.5" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 32: Illegal quoting, probably in the following text: "85394-5-1.jpg
        ..OR.. 85394-5-5.jpg" ..OR.. W33"*H20"*D20" ..OR.. D7.13"*0.88" ..OR.. L22*W28*H17"
        ..OR.. 25" ..OR.. 56" ..OR.. 3*12" ..OR.. 72" ..OR.. L19.25*W4.75*D12.25"'
    - - :warning
      - 'Line 33: Illegal quoting, probably in the following text: "85494-5-1.jpg
        ..OR.. 85494-5-5.jpg" ..OR.. W33"*H20"*D20" ..OR.. D7.13"*0.88" ..OR.. L22*W28*H17"
        ..OR.. 25" ..OR.. 56" ..OR.. 3*12" ..OR.. 72" ..OR.. L19.25*W4.75*D12.25"'
    - - :warning
      - 'Line 34: Illegal quoting, probably in the following text: "85492-10-1.jpg
        ..OR.. 85492-10-3.jpg" ..OR.. W50"*H21"*D30" ..OR.. L15.75"*W6"*H1.25" ..OR..
        L36.5*W20.75*H28" ..OR.. 24.75" ..OR.. 97" ..OR.. 72" ..OR.. 2*12" ..OR..
        120" ..OR.. D12.25*H4.75"'
    - - :warning
      - 'Line 35: Illegal quoting, probably in the following text: "85592-10-1.jpg
        ..OR.. 85592-10-3.jpg" ..OR.. W50"*H21"*D30" ..OR.. L15.75"*W6"*H1.25" ..OR..
        L36.5*W20.75*H28" ..OR.. 24.75" ..OR.. 97" ..OR.. 72" ..OR.. 2*12" ..OR..
        120" ..OR.. D12.25*H4.75"'
    - - :warning
      - 'Line 36: Illegal quoting, probably in the following text: "85395-1-1.jpg
        ..OR.. 85395-1-3.jpg" ..OR.. W16"*H18"*D10" ..OR.. L21*W22*H8" ..OR.. D4.75"*H0.75"
        ..OR.. 7" ..OR.. L19.25*W4.75*D15.63"'
    - - :warning
      - 'Line 37: Illegal quoting, probably in the following text: "85495-1-1.jpg
        ..OR.. 85495-1-3.jpg" ..OR.. W16"*H18"*D10" ..OR.. L21*W22*H8" ..OR.. D4.75"*H0.75"
        ..OR.. 7" ..OR.. L19.25*W4.75*D15.63"'
    - - :warning
      - 'Line 38: Illegal quoting, probably in the following text: "85250-16-1.jpg
        ..OR.. 85250-16-4.jpg" ..OR.. W35"*H23"*D35" ..OR.. L38*W38*H23" ..OR.. 33"
        ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 39: Illegal quoting, probably in the following text: "85350-16-1.jpg
        ..OR.. 85350-16-4.jpg" ..OR.. W35"*H23"*D35" ..OR.. L38*W38*H23" ..OR.. 33"
        ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 40: Illegal quoting, probably in the following text: "85251-9-1.jpg
        ..OR.. 85251-9-4.jpg" ..OR.. W28"*H16"*D28" ..OR.. L31*W31*H21" ..OR.. 26"
        ..OR.. 62" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 41: Illegal quoting, probably in the following text: "85351-9-1.jpg
        ..OR.. 85351-9-5.jpg" ..OR.. W28"*H16"*D28" ..OR.. L31*W31*H21" ..OR.. 26"
        ..OR.. 62" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 42: Illegal quoting, probably in the following text: "85254-6-1.jpg
        ..OR.. 85254-6-4.jpg" ..OR.. W47"*H9"*D12" ..OR.. W17.75"*D4.75"*H0.8" ..OR..
        L15*W50*H13" ..OR.. 18" ..OR.. 54" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 43: Illegal quoting, probably in the following text: "85354-6-1.jpg
        ..OR.. 85354-6-5.jpg" ..OR.. W47"*H9"*D12" ..OR.. W17.75"*D4.75"*H0.8" ..OR..
        L15*W50*H13" ..OR.. 18" ..OR.. 54" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 44: Illegal quoting, probably in the following text: "85256-4-1.jpg
        ..OR.. 85256-4-3.jpg" ..OR.. W12"*H20"*D7" ..OR.. L14*W19*H14" ..OR.. L16.5"*W5.5"*H0.75"
        ..OR.. 7" ..OR.. L9*W3"'
    - - :warning
      - 'Line 45: Illegal quoting, probably in the following text: "85356-4-1.jpg
        ..OR.. 85356-4-3.jpg" ..OR.. W12"*H20"*D7" ..OR.. L14*W19*H14" ..OR.. L16.5"*W5.5"*H0.75"
        ..OR.. 7" ..OR.. L9*W3"'
    - - :warning
      - 'Line 46: Illegal quoting, probably in the following text: "85133-16.jpg ..OR..
        85133-16_1.jpg" ..OR.. W30"*H42"*D30" ..OR.. D5.4*H0.88" ..OR.. L24*W24*H32"
        ..OR.. L30*W30*H30" ..OR.. 47" ..OR.. 117" ..OR.. 1*72" ..OR.. 120" ..OR..
        "L21*W4.88" ..OR.. L21*W4.88" ..OR.. L18.75*W4.88" ..OR.. L15.4*W4.88"'
    - - :warning
      - 'Line 47: Illegal quoting, probably in the following text: "85130-7-1.jpg
        ..OR.. 85130-7-4.jpg" ..OR.. W47"*H24"*D13" ..OR.. L16.5"*4.75"*H0.88" ..OR..
        L49*W16*H28" ..OR.. 29" ..OR.. 101" ..OR.. 1*72" ..OR.. 2*19.25" ..OR.. 120"'
    - - :warning
      - 'Line 48: Illegal quoting, probably in the following text: W26"*H36"*D26"
        ..OR.. D5.4*H0.88" ..OR.. L24*W24*H37" ..OR.. 39" ..OR.. 111" ..OR.. 1*72"
        ..OR.. 120" ..OR.. "L25*W4.75" ..OR.. L16.75*W4.75" ..OR.. L20*W4.75"'
    - - :warning
      - 'Line 49: Illegal quoting, probably in the following text: W20"*H32"*D20"
        ..OR.. D5.4*H0.88" ..OR.. L23*W23*H34" ..OR.. 34" ..OR.. 106" ..OR.. 1*72"
        ..OR.. 120"'
    - - :warning
      - 'Line 50: Illegal quoting, probably in the following text: W24"*H13"*D24"
        ..OR.. D5.88*H0.75" ..OR.. L23*W23*H16" ..OR.. 1*8.5" ..OR.. 7" ..OR.. L8.25*W3.25"'
    - - :warning
      - 'Line 51: Illegal quoting, probably in the following text: W7"*H15"*D5" ..OR..
        L15*W12*H12" ..OR.. L7.1*W4.75*H0.75" ..OR.. 7" ..OR.. "L7.6*W3.1" ..OR..
        L9.6*W3.1"'
    - - :warning
      - 'Line 52: Illegal quoting, probably in the following text: "85422-12-1.jpg
        ..OR.. 85422-12-3.jpg" ..OR.. W42"*H45"*D42" ..OR.. D5.88"*H1" ..OR.. L37*W37*H42"
        ..OR.. 49" ..OR.. 114.5" ..OR.. 1*72" ..OR.. 1*9+1*12" ..OR.. 120"'
    - - :warning
      - 'Line 53: Illegal quoting, probably in the following text: "85421-8-1.jpg
        ..OR.. 85421-8-3.jpg" ..OR.. W30"*H31"*D30" ..OR.. D5.88"*H1" ..OR.. L25*W25*H30"
        ..OR.. 35" ..OR.. 108.75" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120"'
    - - :warning
      - 'Line 54: Illegal quoting, probably in the following text: "85420-12-1.jpg
        ..OR.. 85420-12-5.jpg" ..OR.. W60"*H23"*D18" ..OR.. L21.5"*W4.75"*H0.75" ..OR..
        L55*W14*H23" ..OR.. 26" ..OR.. 99" ..OR.. 1*72" ..OR.. 2*12" ..OR.. 120"'
    - - :warning
      - 'Line 55: Illegal quoting, probably in the following text: "85424-1-1.jpg
        ..OR.. 85424-1-3.jpg" ..OR.. W9"*H13"*D9" ..OR.. D4.75"*H1" ..OR.. L15*W11*H14"
        ..OR.. 24" ..OR.. 59.5" ..OR.. 72"'
    - - :warning
      - 'Line 56: Illegal quoting, probably in the following text: "85425-5-1.jpg
        ..OR.. 85425-5-4.jpg" ..OR.. W28"*H10"*D28" ..OR.. D7.13"*H0.75" ..OR.. L23*W23*H11"
        ..OR.. 7"'
    - - :warning
      - 'Line 57: Illegal quoting, probably in the following text: "85426-4-1.jpg
        ..OR.. 85426-4-5.jpg" ..OR.. W25"*H5"*D5" ..OR.. L20*W9*H9" ..OR.. L13.75"*W5.13"*H0.75"
        ..OR.. 7"'
    - - :warning
      - 'Line 58: Illegal quoting, probably in the following text: "85427-6-1.jpg
        ..OR.. 85427-6-5.jpg" ..OR.. W35"*H6"*D5" ..OR.. L30*W9*H9" ..OR.. L13.75"*W5.13"*H0.75"
        ..OR.. 7"'
    - - :warning
      - 'Line 59: Illegal quoting, probably in the following text: "85423-1-1.jpg
        ..OR.. 85423-1-4.jpg" ..OR.. W11"*H20"*D5" ..OR.. L19*W10*H9" ..OR.. L12.38"*W5"*H1"
        ..OR.. 7"'
    - - :warning
      - 'Line 60: Illegal quoting, probably in the following text: "85202-16.jpg ..OR..
        85202-16_1.jpg" ..OR.. W36"*H48"*D36" ..OR.. D5.5*H1" ..OR.. L39*W39*H35"
        ..OR.. L31*W19*H16" ..OR.. 51" ..OR.. 125" ..OR.. 2*72" ..OR.. 120" ..OR..
        "L11.8*W6" ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 61: Illegal quoting, probably in the following text: "85207-9.jpg ..OR..
        85207-9-2.jpg" ..OR.. W24"*H36"*D24" ..OR.. D5.5"*H1" ..OR.. L28*W28*H30"
        ..OR.. 40" ..OR.. 112" ..OR.. 1*72" ..OR.. 120" ..OR.. "L11.75*W5.88"'
    - - :warning
      - 'Line 62: Illegal quoting, probably in the following text: +L9.63*W4.75"'
    - - :warning
      - 'Line 63: Illegal quoting, probably in the following text: +L6.5*W4.88"'
    - - :warning
      - 'Line 64: Illegal quoting, probably in the following text: W30"*H24"*D30"
        ..OR.. D5.5*H1" ..OR.. L31*W31*H30" ..OR.. 30" ..OR.. 103" ..OR.. 1*72" ..OR..
        120" ..OR.. "L11.8*W6" ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 65: Illegal quoting, probably in the following text: "85203-6.jpg ..OR..
        85203-6_1.jpg" ..OR.. W53"*H22"*D10" ..OR.. L15*W4.4*H0.75" ..OR.. L54*W13*H14"
        ..OR.. 26" ..OR.. 98" ..OR.. 1*72" ..OR.. 120" ..OR.. "L11.8*W6" ..OR.. L9.6*W4.75"
        ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 66: Illegal quoting, probably in the following text: "85200-6-1.jpg
        ..OR.. 85200-6-3.jpg" ..OR.. W24"*H21"*D24" ..OR.. D5.5"*H1" ..OR.. L26*W26*H16"
        ..OR.. 24" ..OR.. 96" ..OR.. 1*72" ..OR.. 120" ..OR.. "L11.75*W5.88"'
    - - :warning
      - 'Line 67: Illegal quoting, probably in the following text: +L9.63*W4.75"'
    - - :warning
      - 'Line 68: Illegal quoting, probably in the following text: +L6.5*W4.88"'
    - - :warning
      - 'Line 69: Illegal quoting, probably in the following text: "85206-4-1.jpg
        ..OR.. 85206-4-4.jpg" ..OR.. W29"*H10"*D6" ..OR.. L41*W31*H8" ..OR.. L25.63"*W4.75"*H1"
        ..OR.. 7" ..OR.. "L9.63*W4.75"'
    - - :warning
      - 'Line 70: Illegal quoting, probably in the following text: L7.63*W4.25"'
    - - :warning
      - 'Line 71: Illegal quoting, probably in the following text: L6.13*W3.88"'
    - - :warning
      - 'Line 72: Illegal quoting, probably in the following text: "85205-2-1.jpg
        ..OR.. 85205-2-5.jpg" ..OR.. W21"*H10"*D6" ..OR.. L15*W23*H8" ..OR.. L17.75"*W4.75"*H1"
        ..OR.. 7" ..OR.. "L9.63*W4.75"'
    - - :warning
      - 'Line 73: Illegal quoting, probably in the following text: L7.63*W4.25"'
    - - :warning
      - 'Line 74: Illegal quoting, probably in the following text: L6.13*W3.88"'
    - - :warning
      - 'Line 75: Illegal quoting, probably in the following text: W6"*H12"*D4" ..OR..
        L16*W10*H9" ..OR.. L6*W4.5*H0.63" ..OR.. 23" ..OR.. 90" ..OR.. 7" ..OR.. "L11.8*W6"
        ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 76: Illegal quoting, probably in the following text: "85412-17-1.jpg
        ..OR.. 85412-17-5.jpg" ..OR.. W39"*H23"*D39" ..OR.. D5.88"*H0.75" ..OR.. L42.5*W42.5*H22"
        ..OR.. L42.25*W31.5*H24.5" ..OR.. 33" ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72"
        ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 77: Illegal quoting, probably in the following text: "85512-17-1.jpg
        ..OR.. 85512-17-5.jpg" ..OR.. W39"*H23"*D39" ..OR.. D5.88"*H0.75" ..OR.. L42.5*W42.5*H22"
        ..OR.. L42.25*W31.5*H24.5" ..OR.. 33" ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72"
        ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 78: Illegal quoting, probably in the following text: W39"*H23"*D39"
        ..OR.. D5.5"*H0.75" ..OR.. L42.5*42.5*22" ..OR.. L31.5*W42.25*H24.5" ..OR..
        33" ..OR.. 84" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 79: Illegal quoting, probably in the following text: "85414-20-1.jpg
        ..OR.. 85414-20-5.jpg" ..OR.. W31"*H35"*D31" ..OR.. D5.88"*H0.75" ..OR.. L34*W34*H35"
        ..OR.. L42*W29*H25" ..OR.. 14" ..OR.. 80" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 80: Illegal quoting, probably in the following text: "85514-20-1.jpg
        ..OR.. 85514-20-6.jpg" ..OR.. W31"*H35"*D31" ..OR.. D5.88"*H0.75" ..OR.. L34*W34*H35"
        ..OR.. L42*W29*H25" ..OR.. 14" ..OR.. 80" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 81: Illegal quoting, probably in the following text: W31"*H35"*D31"
        ..OR.. D6*H0.75" ..OR.. L34*W34*H35" ..OR.. L29*W42*H25" ..OR.. 43.75" ..OR..
        94" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 82: Illegal quoting, probably in the following text: "85411-13-1.jpg
        ..OR.. 85411-13-5.jpg" ..OR.. W31"*H19"*D31" ..OR.. D5.5"*H0.75" ..OR.. L33*W33*H28"
        ..OR.. 29" ..OR.. 65" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 83: Illegal quoting, probably in the following text: "85511-13-1.jpg
        ..OR.. 85511-13-6.jpg" ..OR.. W31"*H19"*D31" ..OR.. D5.5"*H0.75" ..OR.. L33*W33*H28"
        ..OR.. 29" ..OR.. 65" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 84: Illegal quoting, probably in the following text: "85621-13-1.jpg
        ..OR.. 85621-13-4.jpg" ..OR.. W31"*H19"*D31" ..OR.. D5.25"*H0.75" ..OR.. L33.5*W33.5*H27.75"
        ..OR.. 18.5" ..OR.. 64.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75
        xW4.25 xH1.25"'
    - - :warning
      - 'Line 85: Illegal quoting, probably in the following text: "85410-7-1.jpg
        ..OR.. 85410-7-6.jpg" ..OR.. W26"*H17"*D26" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H27"
        ..OR.. 27" ..OR.. 63" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 86: Illegal quoting, probably in the following text: "85510-7-1.jpg
        ..OR.. 85510-7-5.jpg" ..OR.. W26"*H17"*D26" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H27"
        ..OR.. 27" ..OR.. 63" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 87: Illegal quoting, probably in the following text: "85620-7-1.jpg
        ..OR.. 85620-7-2.jpg" ..OR.. W26"*H17"*D26" ..OR.. D5.25"*H0.75" ..OR.. L27.75*W27.75*H27.25"
        ..OR.. 27" ..OR.. 63" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25
        xH1.25"'
    - - :warning
      - 'Line 88: Illegal quoting, probably in the following text: "85413-6-1.jpg
        ..OR.. 85413-6-4.jpg" ..OR.. W47"*H11"*D15" ..OR.. L15.75"*W5.13"*H1" ..OR..
        L50*W18*H23" ..OR.. 18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 89: Illegal quoting, probably in the following text: "85513-6-1.jpg
        ..OR.. 85513-6-5.jpg" ..OR.. W47"*H11"*D15" ..OR.. L15.75"*W5.13"*H1" ..OR..
        L50*W18*H23" ..OR.. 18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 90: Illegal quoting, probably in the following text: W47"*H11"*D15"
        ..OR.. D15.75" xH5.25" ..OR.. L17.75*W50.5*H23.25" ..OR.. L15.75*W5.25*H1"
        ..OR.. 18.25" ..OR.. 69" ..OR.. 2*3"+2*6"+8*12" ..OR.. 120" ..OR.. L8.75 xW4.25
        xH1.25"'
    - - :warning
      - 'Line 91: Illegal quoting, probably in the following text: "85415-2-1.jpg
        ..OR.. 85415-2-3.jpg" ..OR.. W15"*H11"*D8" ..OR.. L22*W16*H17" ..OR.. L6.25"*W5.88"*H0.75"
        ..OR.. 7" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 92: Illegal quoting, probably in the following text: "85515-2-1.jpg
        ..OR.. 85515-2-3.jpg" ..OR.. W15"*H11"*D8" ..OR.. L22*W16*H17" ..OR.. L6.25"*W5.88"*H0.75"
        ..OR.. 7" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 93: Illegal quoting, probably in the following text: W15"*H11"*D8" ..OR..
        L15.75*W21.75*H16.5" ..OR.. D6xH6.25" ..OR.. 7" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 94: Illegal quoting, probably in the following text: W34"*H37"*D34"
        ..OR.. D5.5*H1" ..OR.. L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR..
        75" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 95: Illegal quoting, probably in the following text: W34"*H37"*D34"
        ..OR.. D5.5*H1" ..OR.. L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR..
        75" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 96: Illegal quoting, probably in the following text: W34"*H37"*D34"
        ..OR.. D5.5*H1" ..OR.. L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR..
        75.25" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 97: Illegal quoting, probably in the following text: W23"*H29"*D23"
        ..OR.. D5.5*H1" ..OR.. L30*W29*H24" ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 98: Illegal quoting, probably in the following text: "85262-13.jpg ..OR..
        85262-13_1.jpg" ..OR.. W23"*H29"*D23" ..OR.. D5.5*H1" ..OR.. L30*W29*H24"
        ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 99: Illegal quoting, probably in the following text: W23"*H29"*D23"
        ..OR.. D5.5*H1" ..OR.. L30*W29*H24" ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 100: Illegal quoting, probably in the following text: "85161-5.jpg ..OR..
        85161-5_1.jpg" ..OR.. W17"*H20"*D17" ..OR.. D5.5*H1" ..OR.. L23*W20*H23" ..OR..
        28" ..OR.. 64" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 101: Illegal quoting, probably in the following text: W17"*H20"*D17"
        ..OR.. D5.5*H1" ..OR.. L23*W20*H23" ..OR.. 28" ..OR.. 64" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 102: Illegal quoting, probably in the following text: W17"*H20"*D17"
        ..OR.. D5.5*H1" ..OR.. L23*W20*H23" ..OR.. 28" ..OR.. 64" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 103: Illegal quoting, probably in the following text: W12"*H13"*D7"
        ..OR.. L18*W13*H16" ..OR.. L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 104: Illegal quoting, probably in the following text: W12"*H13"*D7"
        ..OR.. L18*W13*H16" ..OR.. L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 105: Illegal quoting, probably in the following text: W12"*H13"*D7"
        ..OR.. L18*W13*H16" ..OR.. L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 106: Illegal quoting, probably in the following text: "85433-12-1.jpg
        ..OR.. 85433-12-3.jpg" ..OR.. W52"*H52"*D52" ..OR.. D5.88*H0.75" ..OR.. L29*W29*H12"
        ..OR.. 58" ..OR.. 126" ..OR.. 1*72" ..OR.. 144"'
    - - :warning
      - 'Line 107: Illegal quoting, probably in the following text: "85432-8-1.jpg
        ..OR.. 85432-8-3.jpg" ..OR.. W38"*H38"*D38" ..OR.. D5.13*H0.75" ..OR.. L56*W56*H14"
        ..OR.. 44" ..OR.. 112" ..OR.. 1*72" ..OR.. 144"'
    - - :warning
      - 'Line 108: Illegal quoting, probably in the following text: "85431-6-1.jpg
        ..OR.. 85431-6-3.jpg" ..OR.. W28"*H30"*D28" ..OR.. D5.13*H0.75" ..OR.. L41*W41*H12"
        ..OR.. 36" ..OR.. 104" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 109: Illegal quoting, probably in the following text: "85430-4-1.jpg
        ..OR.. 85430-4-3.jpg" ..OR.. W16"*H15"*D16" ..OR.. D4.75*H0.75" ..OR.. L31*W31*H10"
        ..OR.. 21" ..OR.. 89" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 110: Illegal quoting, probably in the following text: "85435-8-1.jpg
        ..OR.. 85435-8-5.jpg" ..OR.. W34"*H10"*D34" ..OR.. D5.13*H0.75" ..OR.. L10*W16*H11"
        ..OR.. 18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 111: Illegal quoting, probably in the following text: "85434-6-1.jpg
        ..OR.. 85434-6-4.jpg" ..OR.. W26"*H8"*D26" ..OR.. D5.13*H0.75" ..OR.. L37*W37*H13"
        ..OR.. 16" ..OR.. 53" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 112: Illegal quoting, probably in the following text: "85437-3-1.jpg
        ..OR.. 85437-3-5.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5.13*H0.75" ..OR.. L11*W15*H7"
        ..OR.. 7"'
    - - :warning
      - 'Line 113: Illegal quoting, probably in the following text: "85436-1-1.jpg
        ..OR.. 85436-1-4.jpg" ..OR.. W7"*H9"*D7" ..OR.. D5.13*H0.75" ..OR.. L19*W19*H12"
        ..OR.. 17" ..OR.. 53" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 114: Illegal quoting, probably in the following text: "85438-1-1.jpg
        ..OR.. 85438-1-4.jpg" ..OR.. W8"*H12"*D5" ..OR.. L14.5*W10.75*H7.5" ..OR..
        L9"*4.75"*H0.75" ..OR.. 7"'
    - - :warning
      - 'Line 115: Illegal quoting, probably in the following text: "85232-12.jpg
        ..OR.. 85232-12_1.jpg" ..OR.. W26"*H39"*D26" ..OR.. D5.5*H1" ..OR.. L30*W30*H14"
        ..OR.. 42" ..OR.. 115" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 116: Illegal quoting, probably in the following text: W48"*H24"*D15"
        ..OR.. L16.1*W5.88*H0.88" ..OR.. L50*W22*H11" ..OR.. 27" ..OR.. 100" ..OR..
        2*72" ..OR.. 2*15" ..OR.. 120" ..OR.. L47.25*W14.25*H8.25"'
    - - :warning
      - 'Line 117: Illegal quoting, probably in the following text: W27"*H25"*D27"
        ..OR.. D5.5*H1" ..OR.. L30*W30*H25" ..OR.. 28" ..OR.. 101" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 118: Illegal quoting, probably in the following text: W23"*H27"*D23"
        ..OR.. D5.5*H1" ..OR.. L26*W26*H15" ..OR.. 30" ..OR.. 103" ..OR.. 1*72" ..OR..
        120" ..OR.. D23*H8"'
    - - :warning
      - 'Line 119: Illegal quoting, probably in the following text: W15"*H12"*D15"
        ..OR.. D5.5*H1" ..OR.. L18*W18*H15" ..OR.. 1*3.25" ..OR.. 7" ..OR.. D15*H7"'
    - - :warning
      - 'Line 120: Illegal quoting, probably in the following text: W7"*H9.5"*D7"
        ..OR.. D5.5*H1" ..OR.. L16*W12*H10" ..OR.. 20" ..OR.. 56" ..OR.. 1*6"+3*12"
        ..OR.. 120"'
    - - :warning
      - 'Line 121: Illegal quoting, probably in the following text: W36"*H6"*D6" ..OR..
        L39*W9*H9" ..OR.. L35.38*W4.5*H0.75" ..OR.. 7" ..OR.. L36*W4.8*H5.88"'
    - - :warning
      - 'Line 122: Illegal quoting, probably in the following text: W25"*H6"*D5" ..OR..
        L28*W9*H9" ..OR.. L24.38*W4.5*H0.75" ..OR.. 7" ..OR.. L25*W4.8*H4.38"'
    - - :warning
      - 'Line 123: Illegal quoting, probably in the following text: W8"*H9"*D5" ..OR..
        L11*W10*H8" ..OR.. L6.5*W6.5*H0.75" ..OR.. 7" ..OR.. L8.38*W7.25*H4"'
    - - :warning
      - 'Line 124: Illegal quoting, probably in the following text: W37"*H58"*D37"
        ..OR.. D5.1*H0.75" ..OR.. L43*W40*H13" ..OR.. 67" ..OR.. 103" ..OR.. 120"
        ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 125: Illegal quoting, probably in the following text: "85244-7.jpg ..OR..
        85244-7_1.jpg" ..OR.. W26"*H46"*D26" ..OR.. D23.63*H1" ..OR.. L28*W26*H18"
        ..OR.. 52" ..OR.. 97" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 126: Illegal quoting, probably in the following text: "85242-6.jpg ..OR..
        85242-6_1.jpg" ..OR.. W24"*H45"*D24" ..OR.. D5.1*H0.75" ..OR.. L32*W27*H13"
        ..OR.. 53" ..OR.. 89" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 127: Illegal quoting, probably in the following text: W50"*H23"*D5"
        ..OR.. L50.38*W8.75*H0.75" ..OR.. L54*W15*H13" ..OR.. 32" ..OR.. 97" ..OR..
        120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 128: Illegal quoting, probably in the following text: W20"*H37"*D20"
        ..OR.. D5.1*H0.75" ..OR.. L26*W22*H18" ..OR.. 45" ..OR.. 81" ..OR.. 120" ..OR..
        D3.25*L20.75"'
    - - :warning
      - 'Line 129: Illegal quoting, probably in the following text: W5"*H23"*D5" ..OR..
        D5.1*H0.75" ..OR.. L24*W15*H8" ..OR.. 31" ..OR.. 67" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 130: Illegal quoting, probably in the following text: W6"*H32"*D7" ..OR..
        L35*W13*H10" ..OR.. 7" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 131: Illegal quoting, probably in the following text: "85286-68-1.jpg
        ..OR.. 85286-68-3.jpg" ..OR.. W20"*H54"*D20" ..OR.. D20"*H1.38" ..OR.. L24*W24*H31"
        ..OR.. 20" ..OR.. D3.88"'
    - - :warning
      - 'Line 132: Illegal quoting, probably in the following text: "85283-47-1.jpg
        ..OR.. 85283-47-4.jpg" ..OR.. W20"*H40"*D20" ..OR.. D20"*H1.38" ..OR.. L24*W24*H16"
        ..OR.. 20" ..OR.. D3.88"'
    - - :warning
      - 'Line 133: Illegal quoting, probably in the following text: "85281-19-1.jpg
        ..OR.. 85281-19-4.jpg" ..OR.. W20"*H20"*D20" ..OR.. D20"*H1.38" ..OR.. L24*W24*H16"
        ..OR.. 20" ..OR.. D3.88"'
    - - :warning
      - 'Line 134: Illegal quoting, probably in the following text: "85289-5-1.jpg
        ..OR.. 85289-5-4.jpg" ..OR.. W6"*H25"*D7" ..OR.. L8*W12*H20" ..OR.. L8.63"*W5.75"*H1.38"
        ..OR.. 7" ..OR.. D3.88"'
    - - :warning
      - 'Line 135: Illegal quoting, probably in the following text: "85288-3-1.jpg
        ..OR.. 85288-3-5.jpg" ..OR.. W6"*H15"*D7" ..OR.. L8*W12*H15" ..OR.. L8.63"*W5.75"*H1.38"
        ..OR.. 7" ..OR.. D3.88"'
    - - :warning
      - 'Line 136: Illegal quoting, probably in the following text: "85216-14.jpg
        ..OR.. 85216-14_1.jpg" ..OR.. W50"*H14"*D10" ..OR.. L50.5*W9.88*H1.38" ..OR..
        L54*W13*H15" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 137: Illegal quoting, probably in the following text: "85214-13.jpg
        ..OR.. 85214-13_1.jpg" ..OR.. W24"*H14"*D24" ..OR.. D24*H1.38" ..OR.. L35*W27*H9"
        ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 138: Illegal quoting, probably in the following text: W36"*H14"*D10"
        ..OR.. L36*W9.88*H1.38" ..OR.. L39*W13*H15" ..OR.. 23" ..OR.. 90" ..OR.. 120"
        ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 139: Illegal quoting, probably in the following text: "85213-6.jpg ..OR..
        85213-6_1.jpg" ..OR.. W16"*H14"*D16" ..OR.. D16*H1.38" ..OR.. L26*W19*H9"
        ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 140: Illegal quoting, probably in the following text: W10"*H14"*D10"
        ..OR.. D9.88*H1.25" ..OR.. L16*W15*H9" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR..
        D3.5*L12"'
    - - :warning
      - 'Line 141: Illegal quoting, probably in the following text: W6"*H14"*D6" ..OR..
        D5.88*H1.25" ..OR.. L15*W9*H9" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 142: Illegal quoting, probably in the following text: "85401-9-1.jpg
        ..OR.. 85401-9-3.jpg" ..OR.. W24"*H7"*D24" ..OR.. D24*1.38" ..OR.. L28*W28*H15"
        ..OR.. 51" ..OR.. 75" ..OR.. 1*5.25+31*32+1*7.38+1*1.38+1*8.63+1*10.13+1*6+1*8.75"
        ..OR.. 7" ..OR.. D4"'
    - - :warning
      - 'Line 143: Illegal quoting, probably in the following text: "85400-5-1.jpg
        ..OR.. 85400-5-3.jpg" ..OR.. W16"*H7"*D16" ..OR.. D15.75"*1.38" ..OR.. L20*W20*H15"
        ..OR.. 42" ..OR.. 66" ..OR.. 1*9"+15*12"+1*1.38"+1*6"+1*10.38"+1*3" ..OR..
        7" ..OR.. D4"'
    - - :warning
      - 'Line 144: Illegal quoting, probably in the following text: "85404-5-1.jpg
        ..OR.. 85404-5-5.jpg" ..OR.. W43"*H7"*D6" ..OR.. L43.25"*W6.25"*H1.38" ..OR..
        L10*W47*H15" ..OR.. 21" ..OR.. 57" ..OR.. 7*6+15*12" ..OR.. 7" ..OR.. D4"'
    - - :warning
      - 'Line 145: Illegal quoting, probably in the following text: "85406-1-1.jpg
        ..OR.. 85406-1-4.jpg" ..OR.. W6"*H7"*D4" ..OR.. D5.5"*H1.25" ..OR.. L9*W17*H8"
        ..OR.. 15" ..OR.. 51" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D4"'
    - - :warning
      - 'Line 146: Illegal quoting, probably in the following text: "85407-1-1.jpg
        ..OR.. 85407-1-5.jpg" ..OR.. W5"*H13"*D6" ..OR.. L13.13"*5.38"*1.25" ..OR..
        L11*W16*H9" ..OR.. 7" ..OR.. D4"'
    - - :warning
      - 'Line 147: Illegal quoting, probably in the following text: W36"*H34"*D36"
        ..OR.. 6.25"*1" ..OR.. L40*W40*H20" ..OR.. 41" ..OR.. 109" ..OR.. 1*72" ..OR..
        120" ..OR.. L13.75"*D1"'
    - - :warning
      - 'Line 148: Illegal quoting, probably in the following text: W45"*H26"*D12"
        ..OR.. L17.75"*W5"*H1" ..OR.. L17*W48*H18" ..OR.. 33" ..OR.. 100" ..OR.. 1*72"
        ..OR.. 120" ..OR.. L13.75"*D1"'
    - - :warning
      - 'Line 149: Illegal quoting, probably in the following text: "85101-8.jpg ..OR..
        85101-8_1.jpg" ..OR.. W30"*H26"*D30" ..OR.. D5.1*H0.75" ..OR.. L33*W33*H16"
        ..OR.. 29" ..OR.. 101" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 150: Illegal quoting, probably in the following text: W24"*H20"*D24"
        ..OR.. D5.1*H0.75" ..OR.. L27*W27*H14" ..OR.. 23" ..OR.. 95" ..OR.. 1*72"
        ..OR.. 1*8.7" ..OR.. 120" ..OR.. D1*H10.75"'
    - - :warning
      - 'Line 151: Illegal quoting, probably in the following text: W18"*H17"*D18"
        ..OR.. D5.1*H0.75" ..OR.. L21*W21*H14" ..OR.. 21" ..OR.. 92" ..OR.. 1*72"
        ..OR.. 1*6" ..OR.. 120" ..OR.. D1*H10.75"'
    - - :warning
      - 'Line 152: Illegal quoting, probably in the following text: "85109-4-1.jpg
        ..OR.. 85109-4-2.jpg" ..OR.. W21"*H12"*D21" ..OR.. D5"*D0.75" ..OR.. L25*W25*H10"
        ..OR.. 7" ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 153: Illegal quoting, probably in the following text: "85108-4-1.jpg
        ..OR.. 85108-4-5.jpg" ..OR.. W36"*H8"*D5" ..OR.. L10*W39*H13" ..OR.. L33"*W5"*H0.75"
        ..OR.. 7" ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 154: Illegal quoting, probably in the following text: "85107-3-1.jpg
        ..OR.. 85107-3-2.jpg" ..OR.. W26"*H8"*D5" ..OR.. L10*W30*H13" ..OR.. L23.5"*W5"*H0.75"
        ..OR.. 7" ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 155: Illegal quoting, probably in the following text: W9"*H26"*D9" ..OR..
        D5.1*H0.75" ..OR.. L20*W18*H11" ..OR.. 29" ..OR.. 101" ..OR.. 1*72" ..OR..
        1*12" ..OR.. 120" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 156: Illegal quoting, probably in the following text: "85106-1-1.jpg
        ..OR.. 85106-1-2.jpg" ..OR.. W7"*H20"*D5" ..OR.. L11*W23*H15" ..OR.. L15"*W4.25"*H0.75"
        ..OR.. 7" ..OR.. L19.25*D0.72"'
    - - :warning
      - 'Line 157: Illegal quoting, probably in the following text: W9"*H15"*D5" ..OR..
        L18*W12*H11" ..OR.. L8.25*W4.75*H0.75" ..OR.. 7" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 158: Illegal quoting, probably in the following text: "85171-12.jpg
        ..OR.. 85171-12_1.jpg" ..OR.. W32"*H12"*D32" ..OR.. L35*W35*H15" ..OR.. 20"
        ..OR.. 83" ..OR.. 120" ..OR.. "L6.75*W1.5*H0.6" ..OR.. L8.3*W1.5*H0.6" ..OR..
        L10*W1.5*H0.6"'
    - - :warning
      - 'Line 159: Illegal quoting, probably in the following text: W50"*H13"*D4"
        ..OR.. L19.63*W5.5*H0.88" ..OR.. L53*W13*H15" ..OR.. 20" ..OR.. 83" ..OR..
        120" ..OR.. "L6.75*W1.5*H0.6" ..OR.. L8.3*W1.5*H0.6" ..OR.. L10*W1.5*H0.6"'
    - - :warning
      - 'Line 160: Illegal quoting, probably in the following text: W10"*H12"*D5"
        ..OR.. L15*W12*H11" ..OR.. L11.75*W9.4*H0.75" ..OR.. 7" ..OR.. "L6.75*W1.5*H0.6"
        ..OR.. L8.3*W1.5*H0.6" ..OR.. L10*W1.5*H0.6"'
    - - :warning
      - 'Line 161: Illegal quoting, probably in the following text: W57"*H26"*D30"
        ..OR.. D7*H1.5" ..OR.. L60*W30*H27" ..OR.. 34" ..OR.. 70" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 162: Illegal quoting, probably in the following text: "85182-9.jpg ..OR..
        85182-9_1.jpg" ..OR.. W37"*H30"*D37" ..OR.. D7*H1.5" ..OR.. L35*W35*H28" ..OR..
        33" ..OR.. 105" ..OR.. 1*72" ..OR.. 120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 163: Illegal quoting, probably in the following text: W21"*H34"*D21"
        ..OR.. D7*H1.5" ..OR.. L32*W26*H17" ..OR.. 36" ..OR.. 109" ..OR.. 1*72" ..OR..
        120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 164: Illegal quoting, probably in the following text: W6"*H14"*D10"
        ..OR.. L18*W13*H9" ..OR.. D6*H1.5" ..OR.. 7" ..OR.. D6*H6"'
    - - :warning
      - 'Line 165: Illegal quoting, probably in the following text: "85270-12-1.jpg
        ..OR.. 85270-12-3.jpg" ..OR.. W32"*H40"*D32" ..OR.. L35*W35*H40" ..OR.. L34*26*15"
        ..OR.. 49" ..OR.. 85" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. "D9.88""+D7.88"'
    - - :warning
      - 'Line 166: Unclosed quoted field in line 1.'
    - - :warning
      - 'Line 167: Illegal quoting, probably in the following text: "85370-12-1.jpg
        ..OR.. 85370-12-4.jpg" ..OR.. W32"*H40"*D32" ..OR.. L35*W35*H40" ..OR.. L34*26*15"
        ..OR.. 49" ..OR.. 85" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. "D9.88""+D7.88"'
    - - :warning
      - 'Line 168: Unclosed quoted field in line 1.'
    - - :warning
      - 'Line 169: Illegal quoting, probably in the following text: "85271-12-1.jpg
        ..OR.. 85271-12-51.jpg" ..OR.. W25"*H34"*D25" ..OR.. D5.13"*H0.75" ..OR..
        L28*W28*H30.5" ..OR.. L28*W18*H21" ..OR.. 43" ..OR.. 79" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. "D5.88""+D7.13"'
    - - :warning
      - 'Line 170: Unclosed quoted field in line 1.'
    - - :warning
      - 'Line 171: Illegal quoting, probably in the following text: "85371-12-1.jpg
        ..OR.. 85371-12-4.jpg" ..OR.. W25"*H34"*D25" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H30.5"
        ..OR.. L28*W18*H21" ..OR.. 43" ..OR.. 79" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        "D5.88""+D7.13"'
    - - :warning
      - 'Line 172: Unclosed quoted field in line 1.'
    - - :warning
      - 'Line 173: Illegal quoting, probably in the following text: "85273-8-1.jpg
        ..OR.. 85273-8-4.jpg" ..OR.. W56"*H25"*D18" ..OR.. L27.13"*W5.13"*H1" ..OR..
        L59*W23.5*H22" ..OR.. L26*W26*H20" ..OR.. 33" ..OR.. 70" ..OR.. 2*6+6*12"
        ..OR.. 72" ..OR.. D7.88"+D9.88"'
    - - :warning
      - 'Line 174: Illegal quoting, probably in the following text: "85373-8-1.jpg
        ..OR.. 85373-8-1.jpg" ..OR.. W56"*H25"*D18" ..OR.. L27.13"*W5.13"*H1" ..OR..
        L59*W23.5*H22" ..OR.. L26*W26*H20" ..OR.. 33" ..OR.. 70" ..OR.. 2*6+6*12"
        ..OR.. 72" ..OR.. D7.88"+D9.88"'
    - - :warning
      - 'Line 175: Illegal quoting, probably in the following text: W14"*H19"*D14"
        ..OR.. D5.13"*H0.75" ..OR.. L20*W25*H18" ..OR.. 28" ..OR.. 64" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. D13.75"'
    - - :warning
      - 'Line 176: Illegal quoting, probably in the following text: "85376-1-1.jpg
        ..OR.. 85376-1-3.jpg" ..OR.. W14"*H19"*D14" ..OR.. D5.13"*H0.75" ..OR.. L20*W25*H18"
        ..OR.. 28" ..OR.. 64" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D13.75"'
    - - :warning
      - 'Line 177: Illegal quoting, probably in the following text: W10"*H14"*D10"
        ..OR.. D5.13"*H0.75" ..OR.. L18*W21*H14" ..OR.. 24" ..OR.. 60" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. D9.88"'
    - - :warning
      - 'Line 178: Illegal quoting, probably in the following text: "85375-1-1.jpg
        ..OR.. 85375-1-2.jpg" ..OR.. W10"*H14"*D10" ..OR.. D5.13"*H0.75" ..OR.. L18*W21*H14"
        ..OR.. 24" ..OR.. 60" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D9.88"'
    - - :warning
      - 'Line 179: Illegal quoting, probably in the following text: W38"*H38"*D38"
        ..OR.. D6.4*H1.88" ..OR.. L41*W41*H40" ..OR.. L32*W24*H24" ..OR.. L32*W24*H24"
        ..OR.. 48" ..OR.. 72" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D10*H1.5"'
    - - :warning
      - 'Line 180: Illegal quoting, probably in the following text: "85122-12.jpg
        ..OR.. 85122-12_1.jpg" ..OR.. W26"*H26"*D26" ..OR.. D6.4*H1.88" ..OR.. L31*W31*H31"
        ..OR.. L30*W24*H24" ..OR.. 36" ..OR.. 66" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR..
        D10*H1.5"'
    - - :warning
      - 'Line 181: Illegal quoting, probably in the following text: "85123-6.jpg ..OR..
        85123-6_1.jpg" ..OR.. W24"*H18"*D24" ..OR.. D6.4*H1.88" ..OR.. L28*W26*H26"
        ..OR.. 1*6" ..OR.. 7" ..OR.. D10*H1.5"'
    - - :warning
      - 'Line 182: Illegal quoting, probably in the following text: "85124-8-1.jpg
        ..OR.. 85124-8-5.jpg" ..OR.. W58"*H10"*D13" ..OR.. L16.88"*W5.88"*H0.88" ..OR..
        L54*W14*H16" ..OR.. 13" ..OR.. 49" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. D9.63"*1.63"'
    - - :warning
      - 'Line 183: Illegal quoting, probably in the following text: "85125-3-1.jpg
        ..OR.. 85125-3-2.jpg" ..OR.. W15"*H27"*D6" ..OR.. L24*W15*H13" ..OR.. D4.75"*H0.75"
        ..OR.. 7" ..OR.. D9.63"*1.63"'
    - - :warning
      - 'Line 184: Illegal quoting, probably in the following text: W24"*H27"*D24"
        ..OR.. D5.88*H0.88" ..OR.. L28*W28*H29" ..OR.. 36" ..OR.. 72" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D23.75*H23.75"'
    - - :warning
      - 'Line 185: Illegal quoting, probably in the following text: W16"*H19"*D16"
        ..OR.. D5.88*H0.88" ..OR.. L19.5*W19.5*H20.75" ..OR.. 29" ..OR.. 65" ..OR..
        1*6"+3*12" ..OR.. 120" ..OR.. D15.75*H15.75"'
    - - :warning
      - 'Line 186: Illegal quoting, probably in the following text: "85221-1.jpg ..OR..
        85221-1_1.jpg" ..OR.. W8"*H10"*D8" ..OR.. D5.88*H0.88" ..OR.. L11*W11*H13"
        ..OR.. 20" ..OR.. 56" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D7.5*H7.5"'
    - - :warning
      - 'Line 187: Illegal quoting, probably in the following text: W41"*H31"*D41"
        ..OR.. D5.5*H1" ..OR.. L43*W43*H9" ..OR.. 34" ..OR.. 106" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 188: Illegal quoting, probably in the following text: W29"*H27"*D29"
        ..OR.. D5.5*H1" ..OR.. L32*W32*H9" ..OR.. 32" ..OR.. 102" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 189: Illegal quoting, probably in the following text: W6"*H18"*D4" ..OR..
        L21*W8*H7" ..OR.. L18*W5.75*H1.25" ..OR.. 7"'
    - - :warning
      - 'Line 190: Illegal quoting, probably in the following text: "85111-6.jpg ..OR..
        85111-6_1.jpg" ..OR.. W36"*H18"*D36" ..OR.. D5.1*H0.75" ..OR.. L40*W40*H22"
        ..OR.. 32" ..OR.. 80" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D36*H18"'
    - - :warning
      - 'Line 191: Illegal quoting, probably in the following text: W24"*H12"*D24"
        ..OR.. D5.1*H0.75" ..OR.. L28*W28*H16" ..OR.. 32" ..OR.. 74" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D24*H12"'
    - - :warning
      - 'Line 192: Illegal quoting, probably in the following text: W16"*H16"*D16"
        ..OR.. D5.1*H0.75" ..OR.. L19*W19*H19" ..OR.. 30" ..OR.. 73" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D16*H15.5"'
    - - :warning
      - 'Line 193: Illegal quoting, probably in the following text: W36"*H21"*D36"
        ..OR.. D5.5*H1" ..OR.. L39*W39*H13" ..OR.. 24" ..OR.. 96" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 194: Illegal quoting, probably in the following text: "85141-6.jpg ..OR..
        85141-6_1.jpg" ..OR.. W27"*H18"*D27" ..OR.. D5.5*H1" ..OR.. L30*W30*H12" ..OR..
        21" ..OR.. 93" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 195: Illegal quoting, probably in the following text: W14"*H21"*D14"
        ..OR.. D5.5*H1" ..OR.. L18*W18*H30" ..OR.. 24" ..OR.. 96" ..OR.. "Iron ..OR..
        solid wood and glass" ..OR.. 1*72" ..OR.. 120" ..OR.. L11.6*W10*H3"'
    - - :warning
      - 'Line 196: Illegal quoting, probably in the following text: "65000-1.jpg ..OR..
        65000-6.jpg" ..OR.. W5"*H19"*D3" ..OR.. W4.72"*H18"'
    - - :warning
      - 'Line 197: Illegal quoting, probably in the following text: "65001-1.jpg ..OR..
        65001-7.jpg" ..OR.. W5"*H24"*D3" ..OR.. W4.72"*H24.7"'
    - - :warning
      - 'Line 198: Illegal quoting, probably in the following text: "65060-1.jpg ..OR..
        65060-5.jpg" ..OR.. W6"*H18"*D3"'
    - - :warning
      - 'Line 199: Illegal quoting, probably in the following text: "65061-1.jpg ..OR..
        65061-5.jpg" ..OR.. W6"*H27"*D3"'
    - - :warning
      - 'Line 200: Illegal quoting, probably in the following text: "65030-1.jpg ..OR..
        65030-4.jpg" ..OR.. W7"*H14"*D4" ..OR.. W7"*H14.37"'
    - - :warning
      - 'Line 201: Illegal quoting, probably in the following text: "65031-1.jpg ..OR..
        65031-4.jpg" ..OR.. W7"*H24"*D4" ..OR.. W7"*H24"'
    - - :warning
      - 'Line 202: Illegal quoting, probably in the following text: "65040-1.jpg ..OR..
        65040-5.jpg" ..OR.. W6"*H16"*D3" ..OR.. "Stainless steel ..OR..  aluminium
        and crystal"'
    - - :warning
      - 'Line 203: Illegal quoting, probably in the following text: "65041-1.jpg ..OR..
        65041-5.jpg" ..OR.. W6"*H24"*D3" ..OR.. "Stainless steel ..OR..  aluminium
        and crystal"'
    - - :warning
      - 'Line 204: Illegal quoting, probably in the following text: "65010-1.jpg ..OR..
        65010-5.jpg" ..OR.. W6"*H11"*D3" ..OR.. W4.72"*H4.3"'
    - - :warning
      - 'Line 205: Illegal quoting, probably in the following text: "65011-1.jpg ..OR..
        65011-5.jpg" ..OR.. W6"*H15"*D3" ..OR.. W4.72"*H4.3"'
    - - :warning
      - 'Line 206: Illegal quoting, probably in the following text: "65050-1.jpg ..OR..
        65050-5.jpg" ..OR.. W7"*H14"*D2"'
    - - :warning
      - 'Line 207: Illegal quoting, probably in the following text: "65051-1.jpg ..OR..
        65051-4.jpg" ..OR.. W7"*H18"*D2"'
    - - :warning
      - 'Line 208: Illegal quoting, probably in the following text: "65090-1.jpg ..OR..
        65090-4.jpg" ..OR.. W5"*H16"*D4"'
    - - :warning
      - 'Line 209: Illegal quoting, probably in the following text: "65091-1.jpg ..OR..
        65091-4.jpg" ..OR.. W5"*H24"*D4"'
 |
| 2026-06-16T06:10:10.189553 | ---
- - Products
  - - - :warning
      - 'Error running cleancsv: 2026/06/16 06:10:08 parse error on line 2, column
        122: bare " in non-quoted-field

        '
    - - :warning
      - 'Line 2: Illegal quoting, probably in the following text: "86010-1-1.jpg ..OR..
        86010-1-4.jpg" ..OR.. W9"*H16"*D9" ..OR.. L16.25*W14.5*H10.75" ..OR.. D5*H1.25"
        ..OR.. 7" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 3: Illegal quoting, probably in the following text: "86120-1-1.jpg ..OR..
        86120-1-5.jpg" ..OR.. W9"*H16"*D9" ..OR.. L16.25*W14.5*H10.75" ..OR.. D5*H1.25"
        ..OR.. 7" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 4: Illegal quoting, probably in the following text: "86013-1-1.jpg ..OR..
        86013-1-2.jpg" ..OR.. W9"*H10"*D9" ..OR.. D5*H1.25" ..OR.. L16.5*W16.5*H10.75"
        ..OR.. 17.5" ..OR.. 71" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 5: Illegal quoting, probably in the following text: "86123-1-1.jpg ..OR..
        86123-1-3.jpg" ..OR.. W9"*H10"*D9" ..OR.. D5*H1.25" ..OR.. L16.5*W16.5*H10.75"
        ..OR.. 17.5" ..OR.. 71" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H7.25"'
    - - :warning
      - 'Line 6: Illegal quoting, probably in the following text: "86011-2-1.jpg ..OR..
        86011-2-5.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 15.5" ..OR.. 70" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 7: Illegal quoting, probably in the following text: "86121-2-1.jpg ..OR..
        86121-2-5.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 15.5" ..OR.. 70" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 8: Illegal quoting, probably in the following text: "86015-1-1.jpg ..OR..
        86015-1-3.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 18" ..OR.. 72" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 9: Illegal quoting, probably in the following text: "86125-1-1.jpg ..OR..
        86125-1-2.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5*H1.25" ..OR.. L23.75*W19*H12.25"
        ..OR.. 18" ..OR.. 72" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H7.5"'
    - - :warning
      - 'Line 10: Illegal quoting, probably in the following text: "86014-6-1.jpg
        ..OR.. 86014-6-5.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 21" ..OR.. 74" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 11: Illegal quoting, probably in the following text: "86124-6-1.jpg
        ..OR.. 86124-6-5.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 21" ..OR.. 74" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 12: Illegal quoting, probably in the following text: "86017-6-1.jpg
        ..OR.. 86017-6-2.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 25" ..OR.. 79" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 13: Illegal quoting, probably in the following text: "86127-6-1.jpg
        ..OR.. 86127-6-2.jpg" ..OR.. W28"*H14"*D28" ..OR.. D6*H1.25" ..OR.. L31.5*W21.75*H15.75"
        ..OR.. 25" ..OR.. 79" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W13*H12.5"'
    - - :warning
      - 'Line 14: Illegal quoting, probably in the following text: "86001-1-1.jpg
        ..OR.. 86001-1-3.jpg" ..OR.. W8"*H12"*D8" ..OR.. D6"*H1" ..OR.. L20*W13*H14.25"
        ..OR.. 16.5" ..OR.. 70.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 15: Illegal quoting, probably in the following text: "86002-3-1.jpg
        ..OR.. 86002-3-3.jpg" ..OR.. W17"*Max86"*17" ..OR.. L16.75"*W15.75"*H1.5"
        ..OR.. L24.5*W23*H17.5" ..OR.. 37.75" ..OR.. 85.75" ..OR.. 1*3"+3*6"+14*12"
        ..OR.. 120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 16: Illegal quoting, probably in the following text: "86003-6-1.jpg
        ..OR.. 86003-6-3.jpg" ..OR.. W28"*Max86"*28" ..OR.. L28"*W26.75"*H1.5" ..OR..
        L30.5*W30.5*H17.5" ..OR.. 61.75" ..OR.. 85.75" ..OR.. 3*3"+4*6"+22*12" ..OR..
        120" ..OR.. W7.25*H12.25"'
    - - :warning
      - 'Line 17: Illegal quoting, probably in the following text: "86031-3-1.jpg
        ..OR.. 86031-3-3.jpg" ..OR.. W10"*H20"*D10" ..OR.. D5*H1" ..OR.. L15.5*W16.5*H11.75"
        ..OR.. 25.5" ..OR.. 79.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 18: Illegal quoting, probably in the following text: "86036-3-1.jpg
        ..OR.. W15"*H35"*D6" ..OR.. L28.5*W11*H12.5" ..OR.. D5*H1" ..OR.. 7" ..OR..
        W3*H12"'
    - - :warning
      - 'Line 19: Illegal quoting, probably in the following text: "86032-24-1.jpg
        ..OR.. 86032-24-3.jpg" ..OR.. W36"*H26"*D36" ..OR.. D5*H1" ..OR.. L24.75*W21*H24.5"
        ..OR.. 29.25" ..OR.. 102.5" ..OR.. 72" ..OR.. 1*12" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 20: Illegal quoting, probably in the following text: "86033-16-1.jpg
        ..OR.. 86033-16-2.jpg" ..OR.. W28"*H22"*D28" ..OR.. D5*H1" ..OR.. L19*W19*H23"
        ..OR.. 25.5" ..OR.. 97.75" ..OR.. 72" ..OR.. 1*10.25" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 21: Illegal quoting, probably in the following text: "86034-8-1.jpg
        ..OR.. 86034-8-3.jpg" ..OR.. W28"*H15"*D28" ..OR.. D5*H1" ..OR.. L18.5*W18.5*H16.25"
        ..OR.. 19.25" ..OR.. 88.5" ..OR.. 72" ..OR.. 1*10.25" ..OR.. 120" ..OR.. W3*H12"'
    - - :warning
      - 'Line 22: Illegal quoting, probably in the following text: "85190-10-1.jpg
        ..OR.. 85190-10-3.jpg" ..OR.. W35"*H32"*D35" ..OR.. D7.13"*1.66" ..OR.. L28*W24*H27"
        ..OR.. 37" ..OR.. 110" ..OR.. 1*72" ..OR.. 120" ..OR.. L12.13*W9.13*D4"'
    - - :warning
      - 'Line 23: Illegal quoting, probably in the following text: "85191-11.jpg ..OR..
        85191-11_1.jpg" ..OR.. W60"*H20"*D20" ..OR.. D7*H1.5" ..OR.. L55*W24*H15"
        ..OR.. 26" ..OR.. 62" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 24: Illegal quoting, probably in the following text: W26"*H52"*D26"
        ..OR.. D7*H1.5" ..OR.. L44*W24*H15" ..OR.. 55" ..OR.. 127" ..OR.. 1*72" ..OR..
        120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 25: Illegal quoting, probably in the following text: W24"*H33"*D24"
        ..OR.. D7*H1.5" ..OR.. L29*W20*H15" ..OR.. 37" ..OR.. 109" ..OR.. 1*72" ..OR..
        120" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 26: Illegal quoting, probably in the following text: "85195-2-1.jpg
        ..OR.. 85195-2-4.jpg" ..OR.. W22"*H28"*D5" ..OR.. D5.88"*H1.13" ..OR.. L18*W15*H14"
        ..OR.. 7" ..OR.. L12.13*W9.13*D4"'
    - - :warning
      - 'Line 27: Illegal quoting, probably in the following text: W9"*H21"*D5" ..OR..
        L13*W13*H16" ..OR.. D5.88*H1.4" ..OR.. 7" ..OR.. L9.5*H9.5"'
    - - :warning
      - 'Line 28: Illegal quoting, probably in the following text: "85390-10-1.jpg
        ..OR.. 85390-10-4.jpg" ..OR.. W39"*H28"*D39" ..OR.. D6"*H1.38" ..OR.. L26*W32*H27"
        ..OR.. 32" ..OR.. 106" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 29: Illegal quoting, probably in the following text: "85490-10-1.jpg
        ..OR.. 85490-10-5.jpg" ..OR.. W39"*H28"*D39" ..OR.. D6"*H1.38" ..OR.. L26*W32*H27"
        ..OR.. 32" ..OR.. 106" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 30: Illegal quoting, probably in the following text: "85391-6-1.jpg
        ..OR.. 85391-6-5.jpg" ..OR.. W32"*H25"*D32" ..OR.. D6"*H1.38" ..OR.. L26*W34*H15"
        ..OR.. 29" ..OR.. 103" ..OR.. 1*72" ..OR.. 1*9.5" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 31: Illegal quoting, probably in the following text: "85491-6-1.jpg
        ..OR.. 85491-6-5.jpg" ..OR.. W32"*H25"*D32" ..OR.. D6"*H1.38" ..OR.. L26*W34*H15"
        ..OR.. 29" ..OR.. 103" ..OR.. 1*72" ..OR.. 1*9.5" ..OR.. 120" ..OR.. L15.13*W14.75*D4.75"'
    - - :warning
      - 'Line 32: Illegal quoting, probably in the following text: "85394-5-1.jpg
        ..OR.. 85394-5-5.jpg" ..OR.. W33"*H20"*D20" ..OR.. D7.13"*0.88" ..OR.. L22*W28*H17"
        ..OR.. 25" ..OR.. 56" ..OR.. 3*12" ..OR.. 72" ..OR.. L19.25*W4.75*D12.25"'
    - - :warning
      - 'Line 33: Illegal quoting, probably in the following text: "85494-5-1.jpg
        ..OR.. 85494-5-5.jpg" ..OR.. W33"*H20"*D20" ..OR.. D7.13"*0.88" ..OR.. L22*W28*H17"
        ..OR.. 25" ..OR.. 56" ..OR.. 3*12" ..OR.. 72" ..OR.. L19.25*W4.75*D12.25"'
    - - :warning
      - 'Line 34: Illegal quoting, probably in the following text: "85492-10-1.jpg
        ..OR.. 85492-10-3.jpg" ..OR.. W50"*H21"*D30" ..OR.. L15.75"*W6"*H1.25" ..OR..
        L36.5*W20.75*H28" ..OR.. 24.75" ..OR.. 97" ..OR.. 72" ..OR.. 2*12" ..OR..
        120" ..OR.. D12.25*H4.75"'
    - - :warning
      - 'Line 35: Illegal quoting, probably in the following text: "85592-10-1.jpg
        ..OR.. 85592-10-3.jpg" ..OR.. W50"*H21"*D30" ..OR.. L15.75"*W6"*H1.25" ..OR..
        L36.5*W20.75*H28" ..OR.. 24.75" ..OR.. 97" ..OR.. 72" ..OR.. 2*12" ..OR..
        120" ..OR.. D12.25*H4.75"'
    - - :warning
      - 'Line 36: Illegal quoting, probably in the following text: "85395-1-1.jpg
        ..OR.. 85395-1-3.jpg" ..OR.. W16"*H18"*D10" ..OR.. L21*W22*H8" ..OR.. D4.75"*H0.75"
        ..OR.. 7" ..OR.. L19.25*W4.75*D15.63"'
    - - :warning
      - 'Line 37: Illegal quoting, probably in the following text: "85495-1-1.jpg
        ..OR.. 85495-1-3.jpg" ..OR.. W16"*H18"*D10" ..OR.. L21*W22*H8" ..OR.. D4.75"*H0.75"
        ..OR.. 7" ..OR.. L19.25*W4.75*D15.63"'
    - - :warning
      - 'Line 38: Illegal quoting, probably in the following text: "85250-16-1.jpg
        ..OR.. 85250-16-4.jpg" ..OR.. W35"*H23"*D35" ..OR.. L38*W38*H23" ..OR.. 33"
        ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 39: Illegal quoting, probably in the following text: "85350-16-1.jpg
        ..OR.. 85350-16-4.jpg" ..OR.. W35"*H23"*D35" ..OR.. L38*W38*H23" ..OR.. 33"
        ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 40: Illegal quoting, probably in the following text: "85251-9-1.jpg
        ..OR.. 85251-9-4.jpg" ..OR.. W28"*H16"*D28" ..OR.. L31*W31*H21" ..OR.. 26"
        ..OR.. 62" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 41: Illegal quoting, probably in the following text: "85351-9-1.jpg
        ..OR.. 85351-9-5.jpg" ..OR.. W28"*H16"*D28" ..OR.. L31*W31*H21" ..OR.. 26"
        ..OR.. 62" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 42: Illegal quoting, probably in the following text: "85254-6-1.jpg
        ..OR.. 85254-6-4.jpg" ..OR.. W47"*H9"*D12" ..OR.. W17.75"*D4.75"*H0.8" ..OR..
        L15*W50*H13" ..OR.. 18" ..OR.. 54" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 43: Illegal quoting, probably in the following text: "85354-6-1.jpg
        ..OR.. 85354-6-5.jpg" ..OR.. W47"*H9"*D12" ..OR.. W17.75"*D4.75"*H0.8" ..OR..
        L15*W50*H13" ..OR.. 18" ..OR.. 54" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. L9*W3"'
    - - :warning
      - 'Line 44: Illegal quoting, probably in the following text: "85256-4-1.jpg
        ..OR.. 85256-4-3.jpg" ..OR.. W12"*H20"*D7" ..OR.. L14*W19*H14" ..OR.. L16.5"*W5.5"*H0.75"
        ..OR.. 7" ..OR.. L9*W3"'
    - - :warning
      - 'Line 45: Illegal quoting, probably in the following text: "85356-4-1.jpg
        ..OR.. 85356-4-3.jpg" ..OR.. W12"*H20"*D7" ..OR.. L14*W19*H14" ..OR.. L16.5"*W5.5"*H0.75"
        ..OR.. 7" ..OR.. L9*W3"'
    - - :warning
      - 'Line 46: Illegal quoting, probably in the following text: "85133-16.jpg ..OR..
        85133-16_1.jpg" ..OR.. W30"*H42"*D30" ..OR.. D5.4*H0.88" ..OR.. L24*W24*H32"
        ..OR.. L30*W30*H30" ..OR.. 47" ..OR.. 117" ..OR.. 1*72" ..OR.. 120" ..OR..
        "L21*W4.88" ..OR.. L21*W4.88" ..OR.. L18.75*W4.88" ..OR.. L15.4*W4.88"'
    - - :warning
      - 'Line 47: Illegal quoting, probably in the following text: "85130-7-1.jpg
        ..OR.. 85130-7-4.jpg" ..OR.. W47"*H24"*D13" ..OR.. L16.5"*4.75"*H0.88" ..OR..
        L49*W16*H28" ..OR.. 29" ..OR.. 101" ..OR.. 1*72" ..OR.. 2*19.25" ..OR.. 120"'
    - - :warning
      - 'Line 48: Illegal quoting, probably in the following text: W26"*H36"*D26"
        ..OR.. D5.4*H0.88" ..OR.. L24*W24*H37" ..OR.. 39" ..OR.. 111" ..OR.. 1*72"
        ..OR.. 120" ..OR.. "L25*W4.75" ..OR.. L16.75*W4.75" ..OR.. L20*W4.75"'
    - - :warning
      - 'Line 49: Illegal quoting, probably in the following text: W20"*H32"*D20"
        ..OR.. D5.4*H0.88" ..OR.. L23*W23*H34" ..OR.. 34" ..OR.. 106" ..OR.. 1*72"
        ..OR.. 120"'
    - - :warning
      - 'Line 50: Illegal quoting, probably in the following text: W24"*H13"*D24"
        ..OR.. D5.88*H0.75" ..OR.. L23*W23*H16" ..OR.. 1*8.5" ..OR.. 7" ..OR.. L8.25*W3.25"'
    - - :warning
      - 'Line 51: Illegal quoting, probably in the following text: W7"*H15"*D5" ..OR..
        L15*W12*H12" ..OR.. L7.1*W4.75*H0.75" ..OR.. 7" ..OR.. "L7.6*W3.1" ..OR..
        L9.6*W3.1"'
    - - :warning
      - 'Line 52: Illegal quoting, probably in the following text: "85422-12-1.jpg
        ..OR.. 85422-12-3.jpg" ..OR.. W42"*H45"*D42" ..OR.. D5.88"*H1" ..OR.. L37*W37*H42"
        ..OR.. 49" ..OR.. 114.5" ..OR.. 1*72" ..OR.. 1*9+1*12" ..OR.. 120"'
    - - :warning
      - 'Line 53: Illegal quoting, probably in the following text: "85421-8-1.jpg
        ..OR.. 85421-8-3.jpg" ..OR.. W30"*H31"*D30" ..OR.. D5.88"*H1" ..OR.. L25*W25*H30"
        ..OR.. 35" ..OR.. 108.75" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120"'
    - - :warning
      - 'Line 54: Illegal quoting, probably in the following text: "85420-12-1.jpg
        ..OR.. 85420-12-5.jpg" ..OR.. W60"*H23"*D18" ..OR.. L21.5"*W4.75"*H0.75" ..OR..
        L55*W14*H23" ..OR.. 26" ..OR.. 99" ..OR.. 1*72" ..OR.. 2*12" ..OR.. 120"'
    - - :warning
      - 'Line 55: Illegal quoting, probably in the following text: "85424-1-1.jpg
        ..OR.. 85424-1-3.jpg" ..OR.. W9"*H13"*D9" ..OR.. D4.75"*H1" ..OR.. L15*W11*H14"
        ..OR.. 24" ..OR.. 59.5" ..OR.. 72"'
    - - :warning
      - 'Line 56: Illegal quoting, probably in the following text: "85425-5-1.jpg
        ..OR.. 85425-5-4.jpg" ..OR.. W28"*H10"*D28" ..OR.. D7.13"*H0.75" ..OR.. L23*W23*H11"
        ..OR.. 7"'
    - - :warning
      - 'Line 57: Illegal quoting, probably in the following text: "85426-4-1.jpg
        ..OR.. 85426-4-5.jpg" ..OR.. W25"*H5"*D5" ..OR.. L20*W9*H9" ..OR.. L13.75"*W5.13"*H0.75"
        ..OR.. 7"'
    - - :warning
      - 'Line 58: Illegal quoting, probably in the following text: "85427-6-1.jpg
        ..OR.. 85427-6-5.jpg" ..OR.. W35"*H6"*D5" ..OR.. L30*W9*H9" ..OR.. L13.75"*W5.13"*H0.75"
        ..OR.. 7"'
    - - :warning
      - 'Line 59: Illegal quoting, probably in the following text: "85423-1-1.jpg
        ..OR.. 85423-1-4.jpg" ..OR.. W11"*H20"*D5" ..OR.. L19*W10*H9" ..OR.. L12.38"*W5"*H1"
        ..OR.. 7"'
    - - :warning
      - 'Line 60: Illegal quoting, probably in the following text: "85202-16.jpg ..OR..
        85202-16_1.jpg" ..OR.. W36"*H48"*D36" ..OR.. D5.5*H1" ..OR.. L39*W39*H35"
        ..OR.. L31*W19*H16" ..OR.. 51" ..OR.. 125" ..OR.. 2*72" ..OR.. 120" ..OR..
        "L11.8*W6" ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 61: Illegal quoting, probably in the following text: "85207-9.jpg ..OR..
        85207-9-2.jpg" ..OR.. W24"*H36"*D24" ..OR.. D5.5"*H1" ..OR.. L28*W28*H30"
        ..OR.. 40" ..OR.. 112" ..OR.. 1*72" ..OR.. 120" ..OR.. "L11.75*W5.88"'
    - - :warning
      - 'Line 62: Illegal quoting, probably in the following text: +L9.63*W4.75"'
    - - :warning
      - 'Line 63: Illegal quoting, probably in the following text: +L6.5*W4.88"'
    - - :warning
      - 'Line 64: Illegal quoting, probably in the following text: W30"*H24"*D30"
        ..OR.. D5.5*H1" ..OR.. L31*W31*H30" ..OR.. 30" ..OR.. 103" ..OR.. 1*72" ..OR..
        120" ..OR.. "L11.8*W6" ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 65: Illegal quoting, probably in the following text: "85203-6.jpg ..OR..
        85203-6_1.jpg" ..OR.. W53"*H22"*D10" ..OR.. L15*W4.4*H0.75" ..OR.. L54*W13*H14"
        ..OR.. 26" ..OR.. 98" ..OR.. 1*72" ..OR.. 120" ..OR.. "L11.8*W6" ..OR.. L9.6*W4.75"
        ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 66: Illegal quoting, probably in the following text: "85200-6-1.jpg
        ..OR.. 85200-6-3.jpg" ..OR.. W24"*H21"*D24" ..OR.. D5.5"*H1" ..OR.. L26*W26*H16"
        ..OR.. 24" ..OR.. 96" ..OR.. 1*72" ..OR.. 120" ..OR.. "L11.75*W5.88"'
    - - :warning
      - 'Line 67: Illegal quoting, probably in the following text: +L9.63*W4.75"'
    - - :warning
      - 'Line 68: Illegal quoting, probably in the following text: +L6.5*W4.88"'
    - - :warning
      - 'Line 69: Illegal quoting, probably in the following text: "85206-4-1.jpg
        ..OR.. 85206-4-4.jpg" ..OR.. W29"*H10"*D6" ..OR.. L41*W31*H8" ..OR.. L25.63"*W4.75"*H1"
        ..OR.. 7" ..OR.. "L9.63*W4.75"'
    - - :warning
      - 'Line 70: Illegal quoting, probably in the following text: L7.63*W4.25"'
    - - :warning
      - 'Line 71: Illegal quoting, probably in the following text: L6.13*W3.88"'
    - - :warning
      - 'Line 72: Illegal quoting, probably in the following text: "85205-2-1.jpg
        ..OR.. 85205-2-5.jpg" ..OR.. W21"*H10"*D6" ..OR.. L15*W23*H8" ..OR.. L17.75"*W4.75"*H1"
        ..OR.. 7" ..OR.. "L9.63*W4.75"'
    - - :warning
      - 'Line 73: Illegal quoting, probably in the following text: L7.63*W4.25"'
    - - :warning
      - 'Line 74: Illegal quoting, probably in the following text: L6.13*W3.88"'
    - - :warning
      - 'Line 75: Illegal quoting, probably in the following text: W6"*H12"*D4" ..OR..
        L16*W10*H9" ..OR.. L6*W4.5*H0.63" ..OR.. 23" ..OR.. 90" ..OR.. 7" ..OR.. "L11.8*W6"
        ..OR.. L9.6*W4.75" ..OR.. L6.5*W5"'
    - - :warning
      - 'Line 76: Illegal quoting, probably in the following text: "85412-17-1.jpg
        ..OR.. 85412-17-5.jpg" ..OR.. W39"*H23"*D39" ..OR.. D5.88"*H0.75" ..OR.. L42.5*W42.5*H22"
        ..OR.. L42.25*W31.5*H24.5" ..OR.. 33" ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72"
        ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 77: Illegal quoting, probably in the following text: "85512-17-1.jpg
        ..OR.. 85512-17-5.jpg" ..OR.. W39"*H23"*D39" ..OR.. D5.88"*H0.75" ..OR.. L42.5*W42.5*H22"
        ..OR.. L42.25*W31.5*H24.5" ..OR.. 33" ..OR.. 69" ..OR.. 1*6+3*12" ..OR.. 72"
        ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 78: Illegal quoting, probably in the following text: W39"*H23"*D39"
        ..OR.. D5.5"*H0.75" ..OR.. L42.5*42.5*22" ..OR.. L31.5*W42.25*H24.5" ..OR..
        33" ..OR.. 84" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 79: Illegal quoting, probably in the following text: "85414-20-1.jpg
        ..OR.. 85414-20-5.jpg" ..OR.. W31"*H35"*D31" ..OR.. D5.88"*H0.75" ..OR.. L34*W34*H35"
        ..OR.. L42*W29*H25" ..OR.. 14" ..OR.. 80" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 80: Illegal quoting, probably in the following text: "85514-20-1.jpg
        ..OR.. 85514-20-6.jpg" ..OR.. W31"*H35"*D31" ..OR.. D5.88"*H0.75" ..OR.. L34*W34*H35"
        ..OR.. L42*W29*H25" ..OR.. 14" ..OR.. 80" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 81: Illegal quoting, probably in the following text: W31"*H35"*D31"
        ..OR.. D6*H0.75" ..OR.. L34*W34*H35" ..OR.. L29*W42*H25" ..OR.. 43.75" ..OR..
        94" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 82: Illegal quoting, probably in the following text: "85411-13-1.jpg
        ..OR.. 85411-13-5.jpg" ..OR.. W31"*H19"*D31" ..OR.. D5.5"*H0.75" ..OR.. L33*W33*H28"
        ..OR.. 29" ..OR.. 65" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 83: Illegal quoting, probably in the following text: "85511-13-1.jpg
        ..OR.. 85511-13-6.jpg" ..OR.. W31"*H19"*D31" ..OR.. D5.5"*H0.75" ..OR.. L33*W33*H28"
        ..OR.. 29" ..OR.. 65" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 84: Illegal quoting, probably in the following text: "85621-13-1.jpg
        ..OR.. 85621-13-4.jpg" ..OR.. W31"*H19"*D31" ..OR.. D5.25"*H0.75" ..OR.. L33.5*W33.5*H27.75"
        ..OR.. 18.5" ..OR.. 64.5" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75
        xW4.25 xH1.25"'
    - - :warning
      - 'Line 85: Illegal quoting, probably in the following text: "85410-7-1.jpg
        ..OR.. 85410-7-6.jpg" ..OR.. W26"*H17"*D26" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H27"
        ..OR.. 27" ..OR.. 63" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 86: Illegal quoting, probably in the following text: "85510-7-1.jpg
        ..OR.. 85510-7-5.jpg" ..OR.. W26"*H17"*D26" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H27"
        ..OR.. 27" ..OR.. 63" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 87: Illegal quoting, probably in the following text: "85620-7-1.jpg
        ..OR.. 85620-7-2.jpg" ..OR.. W26"*H17"*D26" ..OR.. D5.25"*H0.75" ..OR.. L27.75*W27.75*H27.25"
        ..OR.. 27" ..OR.. 63" ..OR.. 1*3"+1*6"+4*12" ..OR.. 120" ..OR.. L8.75 xW4.25
        xH1.25"'
    - - :warning
      - 'Line 88: Illegal quoting, probably in the following text: "85413-6-1.jpg
        ..OR.. 85413-6-4.jpg" ..OR.. W47"*H11"*D15" ..OR.. L15.75"*W5.13"*H1" ..OR..
        L50*W18*H23" ..OR.. 18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 89: Illegal quoting, probably in the following text: "85513-6-1.jpg
        ..OR.. 85513-6-5.jpg" ..OR.. W47"*H11"*D15" ..OR.. L15.75"*W5.13"*H1" ..OR..
        L50*W18*H23" ..OR.. 18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 90: Illegal quoting, probably in the following text: W47"*H11"*D15"
        ..OR.. D15.75" xH5.25" ..OR.. L17.75*W50.5*H23.25" ..OR.. L15.75*W5.25*H1"
        ..OR.. 18.25" ..OR.. 69" ..OR.. 2*3"+2*6"+8*12" ..OR.. 120" ..OR.. L8.75 xW4.25
        xH1.25"'
    - - :warning
      - 'Line 91: Illegal quoting, probably in the following text: "85415-2-1.jpg
        ..OR.. 85415-2-3.jpg" ..OR.. W15"*H11"*D8" ..OR.. L22*W16*H17" ..OR.. L6.25"*W5.88"*H0.75"
        ..OR.. 7" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 92: Illegal quoting, probably in the following text: "85515-2-1.jpg
        ..OR.. 85515-2-3.jpg" ..OR.. W15"*H11"*D8" ..OR.. L22*W16*H17" ..OR.. L6.25"*W5.88"*H0.75"
        ..OR.. 7" ..OR.. L8.75*W4.25*D1.13"'
    - - :warning
      - 'Line 93: Illegal quoting, probably in the following text: W15"*H11"*D8" ..OR..
        L15.75*W21.75*H16.5" ..OR.. D6xH6.25" ..OR.. 7" ..OR.. L8.75 xW4.25 xH1.25"'
    - - :warning
      - 'Line 94: Illegal quoting, probably in the following text: W34"*H37"*D34"
        ..OR.. D5.5*H1" ..OR.. L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR..
        75" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 95: Illegal quoting, probably in the following text: W34"*H37"*D34"
        ..OR.. D5.5*H1" ..OR.. L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR..
        75" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 96: Illegal quoting, probably in the following text: W34"*H37"*D34"
        ..OR.. D5.5*H1" ..OR.. L37*W37*H22" ..OR.. L35*W30*H16" ..OR.. 46" ..OR..
        75.25" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 97: Illegal quoting, probably in the following text: W23"*H29"*D23"
        ..OR.. D5.5*H1" ..OR.. L30*W29*H24" ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 98: Illegal quoting, probably in the following text: "85262-13.jpg ..OR..
        85262-13_1.jpg" ..OR.. W23"*H29"*D23" ..OR.. D5.5*H1" ..OR.. L30*W29*H24"
        ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 99: Illegal quoting, probably in the following text: W23"*H29"*D23"
        ..OR.. D5.5*H1" ..OR.. L30*W29*H24" ..OR.. 37" ..OR.. 66" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 100: Illegal quoting, probably in the following text: "85161-5.jpg ..OR..
        85161-5_1.jpg" ..OR.. W17"*H20"*D17" ..OR.. D5.5*H1" ..OR.. L23*W20*H23" ..OR..
        28" ..OR.. 64" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 101: Illegal quoting, probably in the following text: W17"*H20"*D17"
        ..OR.. D5.5*H1" ..OR.. L23*W20*H23" ..OR.. 28" ..OR.. 64" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 102: Illegal quoting, probably in the following text: W17"*H20"*D17"
        ..OR.. D5.5*H1" ..OR.. L23*W20*H23" ..OR.. 28" ..OR.. 64" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 103: Illegal quoting, probably in the following text: W12"*H13"*D7"
        ..OR.. L18*W13*H16" ..OR.. L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 104: Illegal quoting, probably in the following text: W12"*H13"*D7"
        ..OR.. L18*W13*H16" ..OR.. L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 105: Illegal quoting, probably in the following text: W12"*H13"*D7"
        ..OR.. L18*W13*H16" ..OR.. L7.1*W5.88*H0.75" ..OR.. 7" ..OR.. L9*W4*H1.2"'
    - - :warning
      - 'Line 106: Illegal quoting, probably in the following text: "85433-12-1.jpg
        ..OR.. 85433-12-3.jpg" ..OR.. W52"*H52"*D52" ..OR.. D5.88*H0.75" ..OR.. L29*W29*H12"
        ..OR.. 58" ..OR.. 126" ..OR.. 1*72" ..OR.. 144"'
    - - :warning
      - 'Line 107: Illegal quoting, probably in the following text: "85432-8-1.jpg
        ..OR.. 85432-8-3.jpg" ..OR.. W38"*H38"*D38" ..OR.. D5.13*H0.75" ..OR.. L56*W56*H14"
        ..OR.. 44" ..OR.. 112" ..OR.. 1*72" ..OR.. 144"'
    - - :warning
      - 'Line 108: Illegal quoting, probably in the following text: "85431-6-1.jpg
        ..OR.. 85431-6-3.jpg" ..OR.. W28"*H30"*D28" ..OR.. D5.13*H0.75" ..OR.. L41*W41*H12"
        ..OR.. 36" ..OR.. 104" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 109: Illegal quoting, probably in the following text: "85430-4-1.jpg
        ..OR.. 85430-4-3.jpg" ..OR.. W16"*H15"*D16" ..OR.. D4.75*H0.75" ..OR.. L31*W31*H10"
        ..OR.. 21" ..OR.. 89" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 110: Illegal quoting, probably in the following text: "85435-8-1.jpg
        ..OR.. 85435-8-5.jpg" ..OR.. W34"*H10"*D34" ..OR.. D5.13*H0.75" ..OR.. L10*W16*H11"
        ..OR.. 18" ..OR.. 54" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 111: Illegal quoting, probably in the following text: "85434-6-1.jpg
        ..OR.. 85434-6-4.jpg" ..OR.. W26"*H8"*D26" ..OR.. D5.13*H0.75" ..OR.. L37*W37*H13"
        ..OR.. 16" ..OR.. 53" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 112: Illegal quoting, probably in the following text: "85437-3-1.jpg
        ..OR.. 85437-3-5.jpg" ..OR.. W16"*H11"*D16" ..OR.. D5.13*H0.75" ..OR.. L11*W15*H7"
        ..OR.. 7"'
    - - :warning
      - 'Line 113: Illegal quoting, probably in the following text: "85436-1-1.jpg
        ..OR.. 85436-1-4.jpg" ..OR.. W7"*H9"*D7" ..OR.. D5.13*H0.75" ..OR.. L19*W19*H12"
        ..OR.. 17" ..OR.. 53" ..OR.. 1*6+3*12" ..OR.. 72"'
    - - :warning
      - 'Line 114: Illegal quoting, probably in the following text: "85438-1-1.jpg
        ..OR.. 85438-1-4.jpg" ..OR.. W8"*H12"*D5" ..OR.. L14.5*W10.75*H7.5" ..OR..
        L9"*4.75"*H0.75" ..OR.. 7"'
    - - :warning
      - 'Line 115: Illegal quoting, probably in the following text: "85232-12.jpg
        ..OR.. 85232-12_1.jpg" ..OR.. W26"*H39"*D26" ..OR.. D5.5*H1" ..OR.. L30*W30*H14"
        ..OR.. 42" ..OR.. 115" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 116: Illegal quoting, probably in the following text: W48"*H24"*D15"
        ..OR.. L16.1*W5.88*H0.88" ..OR.. L50*W22*H11" ..OR.. 27" ..OR.. 100" ..OR..
        2*72" ..OR.. 2*15" ..OR.. 120" ..OR.. L47.25*W14.25*H8.25"'
    - - :warning
      - 'Line 117: Illegal quoting, probably in the following text: W27"*H25"*D27"
        ..OR.. D5.5*H1" ..OR.. L30*W30*H25" ..OR.. 28" ..OR.. 101" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 118: Illegal quoting, probably in the following text: W23"*H27"*D23"
        ..OR.. D5.5*H1" ..OR.. L26*W26*H15" ..OR.. 30" ..OR.. 103" ..OR.. 1*72" ..OR..
        120" ..OR.. D23*H8"'
    - - :warning
      - 'Line 119: Illegal quoting, probably in the following text: W15"*H12"*D15"
        ..OR.. D5.5*H1" ..OR.. L18*W18*H15" ..OR.. 1*3.25" ..OR.. 7" ..OR.. D15*H7"'
    - - :warning
      - 'Line 120: Illegal quoting, probably in the following text: W7"*H9.5"*D7"
        ..OR.. D5.5*H1" ..OR.. L16*W12*H10" ..OR.. 20" ..OR.. 56" ..OR.. 1*6"+3*12"
        ..OR.. 120"'
    - - :warning
      - 'Line 121: Illegal quoting, probably in the following text: W36"*H6"*D6" ..OR..
        L39*W9*H9" ..OR.. L35.38*W4.5*H0.75" ..OR.. 7" ..OR.. L36*W4.8*H5.88"'
    - - :warning
      - 'Line 122: Illegal quoting, probably in the following text: W25"*H6"*D5" ..OR..
        L28*W9*H9" ..OR.. L24.38*W4.5*H0.75" ..OR.. 7" ..OR.. L25*W4.8*H4.38"'
    - - :warning
      - 'Line 123: Illegal quoting, probably in the following text: W8"*H9"*D5" ..OR..
        L11*W10*H8" ..OR.. L6.5*W6.5*H0.75" ..OR.. 7" ..OR.. L8.38*W7.25*H4"'
    - - :warning
      - 'Line 124: Illegal quoting, probably in the following text: W37"*H58"*D37"
        ..OR.. D5.1*H0.75" ..OR.. L43*W40*H13" ..OR.. 67" ..OR.. 103" ..OR.. 120"
        ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 125: Illegal quoting, probably in the following text: "85244-7.jpg ..OR..
        85244-7_1.jpg" ..OR.. W26"*H46"*D26" ..OR.. D23.63*H1" ..OR.. L28*W26*H18"
        ..OR.. 52" ..OR.. 97" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 126: Illegal quoting, probably in the following text: "85242-6.jpg ..OR..
        85242-6_1.jpg" ..OR.. W24"*H45"*D24" ..OR.. D5.1*H0.75" ..OR.. L32*W27*H13"
        ..OR.. 53" ..OR.. 89" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 127: Illegal quoting, probably in the following text: W50"*H23"*D5"
        ..OR.. L50.38*W8.75*H0.75" ..OR.. L54*W15*H13" ..OR.. 32" ..OR.. 97" ..OR..
        120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 128: Illegal quoting, probably in the following text: W20"*H37"*D20"
        ..OR.. D5.1*H0.75" ..OR.. L26*W22*H18" ..OR.. 45" ..OR.. 81" ..OR.. 120" ..OR..
        D3.25*L20.75"'
    - - :warning
      - 'Line 129: Illegal quoting, probably in the following text: W5"*H23"*D5" ..OR..
        D5.1*H0.75" ..OR.. L24*W15*H8" ..OR.. 31" ..OR.. 67" ..OR.. 120" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 130: Illegal quoting, probably in the following text: W6"*H32"*D7" ..OR..
        L35*W13*H10" ..OR.. 7" ..OR.. D3.25*L20.75"'
    - - :warning
      - 'Line 131: Illegal quoting, probably in the following text: "85286-68-1.jpg
        ..OR.. 85286-68-3.jpg" ..OR.. W20"*H54"*D20" ..OR.. D20"*H1.38" ..OR.. L24*W24*H31"
        ..OR.. 20" ..OR.. D3.88"'
    - - :warning
      - 'Line 132: Illegal quoting, probably in the following text: "85283-47-1.jpg
        ..OR.. 85283-47-4.jpg" ..OR.. W20"*H40"*D20" ..OR.. D20"*H1.38" ..OR.. L24*W24*H16"
        ..OR.. 20" ..OR.. D3.88"'
    - - :warning
      - 'Line 133: Illegal quoting, probably in the following text: "85281-19-1.jpg
        ..OR.. 85281-19-4.jpg" ..OR.. W20"*H20"*D20" ..OR.. D20"*H1.38" ..OR.. L24*W24*H16"
        ..OR.. 20" ..OR.. D3.88"'
    - - :warning
      - 'Line 134: Illegal quoting, probably in the following text: "85289-5-1.jpg
        ..OR.. 85289-5-4.jpg" ..OR.. W6"*H25"*D7" ..OR.. L8*W12*H20" ..OR.. L8.63"*W5.75"*H1.38"
        ..OR.. 7" ..OR.. D3.88"'
    - - :warning
      - 'Line 135: Illegal quoting, probably in the following text: "85288-3-1.jpg
        ..OR.. 85288-3-5.jpg" ..OR.. W6"*H15"*D7" ..OR.. L8*W12*H15" ..OR.. L8.63"*W5.75"*H1.38"
        ..OR.. 7" ..OR.. D3.88"'
    - - :warning
      - 'Line 136: Illegal quoting, probably in the following text: "85216-14.jpg
        ..OR.. 85216-14_1.jpg" ..OR.. W50"*H14"*D10" ..OR.. L50.5*W9.88*H1.38" ..OR..
        L54*W13*H15" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 137: Illegal quoting, probably in the following text: "85214-13.jpg
        ..OR.. 85214-13_1.jpg" ..OR.. W24"*H14"*D24" ..OR.. D24*H1.38" ..OR.. L35*W27*H9"
        ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 138: Illegal quoting, probably in the following text: W36"*H14"*D10"
        ..OR.. L36*W9.88*H1.38" ..OR.. L39*W13*H15" ..OR.. 23" ..OR.. 90" ..OR.. 120"
        ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 139: Illegal quoting, probably in the following text: "85213-6.jpg ..OR..
        85213-6_1.jpg" ..OR.. W16"*H14"*D16" ..OR.. D16*H1.38" ..OR.. L26*W19*H9"
        ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 140: Illegal quoting, probably in the following text: W10"*H14"*D10"
        ..OR.. D9.88*H1.25" ..OR.. L16*W15*H9" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR..
        D3.5*L12"'
    - - :warning
      - 'Line 141: Illegal quoting, probably in the following text: W6"*H14"*D6" ..OR..
        D5.88*H1.25" ..OR.. L15*W9*H9" ..OR.. 23" ..OR.. 90" ..OR.. 120" ..OR.. D3.5*L12"'
    - - :warning
      - 'Line 142: Illegal quoting, probably in the following text: "85401-9-1.jpg
        ..OR.. 85401-9-3.jpg" ..OR.. W24"*H7"*D24" ..OR.. D24*1.38" ..OR.. L28*W28*H15"
        ..OR.. 51" ..OR.. 75" ..OR.. 1*5.25+31*32+1*7.38+1*1.38+1*8.63+1*10.13+1*6+1*8.75"
        ..OR.. 7" ..OR.. D4"'
    - - :warning
      - 'Line 143: Illegal quoting, probably in the following text: "85400-5-1.jpg
        ..OR.. 85400-5-3.jpg" ..OR.. W16"*H7"*D16" ..OR.. D15.75"*1.38" ..OR.. L20*W20*H15"
        ..OR.. 42" ..OR.. 66" ..OR.. 1*9"+15*12"+1*1.38"+1*6"+1*10.38"+1*3" ..OR..
        7" ..OR.. D4"'
    - - :warning
      - 'Line 144: Illegal quoting, probably in the following text: "85404-5-1.jpg
        ..OR.. 85404-5-5.jpg" ..OR.. W43"*H7"*D6" ..OR.. L43.25"*W6.25"*H1.38" ..OR..
        L10*W47*H15" ..OR.. 21" ..OR.. 57" ..OR.. 7*6+15*12" ..OR.. 7" ..OR.. D4"'
    - - :warning
      - 'Line 145: Illegal quoting, probably in the following text: "85406-1-1.jpg
        ..OR.. 85406-1-4.jpg" ..OR.. W6"*H7"*D4" ..OR.. D5.5"*H1.25" ..OR.. L9*W17*H8"
        ..OR.. 15" ..OR.. 51" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D4"'
    - - :warning
      - 'Line 146: Illegal quoting, probably in the following text: "85407-1-1.jpg
        ..OR.. 85407-1-5.jpg" ..OR.. W5"*H13"*D6" ..OR.. L13.13"*5.38"*1.25" ..OR..
        L11*W16*H9" ..OR.. 7" ..OR.. D4"'
    - - :warning
      - 'Line 147: Illegal quoting, probably in the following text: W36"*H34"*D36"
        ..OR.. 6.25"*1" ..OR.. L40*W40*H20" ..OR.. 41" ..OR.. 109" ..OR.. 1*72" ..OR..
        120" ..OR.. L13.75"*D1"'
    - - :warning
      - 'Line 148: Illegal quoting, probably in the following text: W45"*H26"*D12"
        ..OR.. L17.75"*W5"*H1" ..OR.. L17*W48*H18" ..OR.. 33" ..OR.. 100" ..OR.. 1*72"
        ..OR.. 120" ..OR.. L13.75"*D1"'
    - - :warning
      - 'Line 149: Illegal quoting, probably in the following text: "85101-8.jpg ..OR..
        85101-8_1.jpg" ..OR.. W30"*H26"*D30" ..OR.. D5.1*H0.75" ..OR.. L33*W33*H16"
        ..OR.. 29" ..OR.. 101" ..OR.. 1*72" ..OR.. 1*12" ..OR.. 120" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 150: Illegal quoting, probably in the following text: W24"*H20"*D24"
        ..OR.. D5.1*H0.75" ..OR.. L27*W27*H14" ..OR.. 23" ..OR.. 95" ..OR.. 1*72"
        ..OR.. 1*8.7" ..OR.. 120" ..OR.. D1*H10.75"'
    - - :warning
      - 'Line 151: Illegal quoting, probably in the following text: W18"*H17"*D18"
        ..OR.. D5.1*H0.75" ..OR.. L21*W21*H14" ..OR.. 21" ..OR.. 92" ..OR.. 1*72"
        ..OR.. 1*6" ..OR.. 120" ..OR.. D1*H10.75"'
    - - :warning
      - 'Line 152: Illegal quoting, probably in the following text: "85109-4-1.jpg
        ..OR.. 85109-4-2.jpg" ..OR.. W21"*H12"*D21" ..OR.. D5"*D0.75" ..OR.. L25*W25*H10"
        ..OR.. 7" ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 153: Illegal quoting, probably in the following text: "85108-4-1.jpg
        ..OR.. 85108-4-5.jpg" ..OR.. W36"*H8"*D5" ..OR.. L10*W39*H13" ..OR.. L33"*W5"*H0.75"
        ..OR.. 7" ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 154: Illegal quoting, probably in the following text: "85107-3-1.jpg
        ..OR.. 85107-3-2.jpg" ..OR.. W26"*H8"*D5" ..OR.. L10*W30*H13" ..OR.. L23.5"*W5"*H0.75"
        ..OR.. 7" ..OR.. L7*D0.75"'
    - - :warning
      - 'Line 155: Illegal quoting, probably in the following text: W9"*H26"*D9" ..OR..
        D5.1*H0.75" ..OR.. L20*W18*H11" ..OR.. 29" ..OR.. 101" ..OR.. 1*72" ..OR..
        1*12" ..OR.. 120" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 156: Illegal quoting, probably in the following text: "85106-1-1.jpg
        ..OR.. 85106-1-2.jpg" ..OR.. W7"*H20"*D5" ..OR.. L11*W23*H15" ..OR.. L15"*W4.25"*H0.75"
        ..OR.. 7" ..OR.. L19.25*D0.72"'
    - - :warning
      - 'Line 157: Illegal quoting, probably in the following text: W9"*H15"*D5" ..OR..
        L18*W12*H11" ..OR.. L8.25*W4.75*H0.75" ..OR.. 7" ..OR.. D1*H13.75"'
    - - :warning
      - 'Line 158: Illegal quoting, probably in the following text: "85171-12.jpg
        ..OR.. 85171-12_1.jpg" ..OR.. W32"*H12"*D32" ..OR.. L35*W35*H15" ..OR.. 20"
        ..OR.. 83" ..OR.. 120" ..OR.. "L6.75*W1.5*H0.6" ..OR.. L8.3*W1.5*H0.6" ..OR..
        L10*W1.5*H0.6"'
    - - :warning
      - 'Line 159: Illegal quoting, probably in the following text: W50"*H13"*D4"
        ..OR.. L19.63*W5.5*H0.88" ..OR.. L53*W13*H15" ..OR.. 20" ..OR.. 83" ..OR..
        120" ..OR.. "L6.75*W1.5*H0.6" ..OR.. L8.3*W1.5*H0.6" ..OR.. L10*W1.5*H0.6"'
    - - :warning
      - 'Line 160: Illegal quoting, probably in the following text: W10"*H12"*D5"
        ..OR.. L15*W12*H11" ..OR.. L11.75*W9.4*H0.75" ..OR.. 7" ..OR.. "L6.75*W1.5*H0.6"
        ..OR.. L8.3*W1.5*H0.6" ..OR.. L10*W1.5*H0.6"'
    - - :warning
      - 'Line 161: Illegal quoting, probably in the following text: W57"*H26"*D30"
        ..OR.. D7*H1.5" ..OR.. L60*W30*H27" ..OR.. 34" ..OR.. 70" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 162: Illegal quoting, probably in the following text: "85182-9.jpg ..OR..
        85182-9_1.jpg" ..OR.. W37"*H30"*D37" ..OR.. D7*H1.5" ..OR.. L35*W35*H28" ..OR..
        33" ..OR.. 105" ..OR.. 1*72" ..OR.. 120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 163: Illegal quoting, probably in the following text: W21"*H34"*D21"
        ..OR.. D7*H1.5" ..OR.. L32*W26*H17" ..OR.. 36" ..OR.. 109" ..OR.. 1*72" ..OR..
        120" ..OR.. D6*H6"'
    - - :warning
      - 'Line 164: Illegal quoting, probably in the following text: W6"*H14"*D10"
        ..OR.. L18*W13*H9" ..OR.. D6*H1.5" ..OR.. 7" ..OR.. D6*H6"'
    - - :warning
      - 'Line 165: Illegal quoting, probably in the following text: "85270-12-1.jpg
        ..OR.. 85270-12-3.jpg" ..OR.. W32"*H40"*D32" ..OR.. L35*W35*H40" ..OR.. L34*26*15"
        ..OR.. 49" ..OR.. 85" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. "D9.88""+D7.88"'
    - - :warning
      - 'Line 166: Unclosed quoted field in line 1.'
    - - :warning
      - 'Line 167: Illegal quoting, probably in the following text: "85370-12-1.jpg
        ..OR.. 85370-12-4.jpg" ..OR.. W32"*H40"*D32" ..OR.. L35*W35*H40" ..OR.. L34*26*15"
        ..OR.. 49" ..OR.. 85" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. "D9.88""+D7.88"'
    - - :warning
      - 'Line 168: Unclosed quoted field in line 1.'
    - - :warning
      - 'Line 169: Illegal quoting, probably in the following text: "85271-12-1.jpg
        ..OR.. 85271-12-51.jpg" ..OR.. W25"*H34"*D25" ..OR.. D5.13"*H0.75" ..OR..
        L28*W28*H30.5" ..OR.. L28*W18*H21" ..OR.. 43" ..OR.. 79" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. "D5.88""+D7.13"'
    - - :warning
      - 'Line 170: Unclosed quoted field in line 1.'
    - - :warning
      - 'Line 171: Illegal quoting, probably in the following text: "85371-12-1.jpg
        ..OR.. 85371-12-4.jpg" ..OR.. W25"*H34"*D25" ..OR.. D5.13"*H0.75" ..OR.. L28*W28*H30.5"
        ..OR.. L28*W18*H21" ..OR.. 43" ..OR.. 79" ..OR.. 1*6+3*12" ..OR.. 72" ..OR..
        "D5.88""+D7.13"'
    - - :warning
      - 'Line 172: Unclosed quoted field in line 1.'
    - - :warning
      - 'Line 173: Illegal quoting, probably in the following text: "85273-8-1.jpg
        ..OR.. 85273-8-4.jpg" ..OR.. W56"*H25"*D18" ..OR.. L27.13"*W5.13"*H1" ..OR..
        L59*W23.5*H22" ..OR.. L26*W26*H20" ..OR.. 33" ..OR.. 70" ..OR.. 2*6+6*12"
        ..OR.. 72" ..OR.. D7.88"+D9.88"'
    - - :warning
      - 'Line 174: Illegal quoting, probably in the following text: "85373-8-1.jpg
        ..OR.. 85373-8-1.jpg" ..OR.. W56"*H25"*D18" ..OR.. L27.13"*W5.13"*H1" ..OR..
        L59*W23.5*H22" ..OR.. L26*W26*H20" ..OR.. 33" ..OR.. 70" ..OR.. 2*6+6*12"
        ..OR.. 72" ..OR.. D7.88"+D9.88"'
    - - :warning
      - 'Line 175: Illegal quoting, probably in the following text: W14"*H19"*D14"
        ..OR.. D5.13"*H0.75" ..OR.. L20*W25*H18" ..OR.. 28" ..OR.. 64" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. D13.75"'
    - - :warning
      - 'Line 176: Illegal quoting, probably in the following text: "85376-1-1.jpg
        ..OR.. 85376-1-3.jpg" ..OR.. W14"*H19"*D14" ..OR.. D5.13"*H0.75" ..OR.. L20*W25*H18"
        ..OR.. 28" ..OR.. 64" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D13.75"'
    - - :warning
      - 'Line 177: Illegal quoting, probably in the following text: W10"*H14"*D10"
        ..OR.. D5.13"*H0.75" ..OR.. L18*W21*H14" ..OR.. 24" ..OR.. 60" ..OR.. 1*6+3*12"
        ..OR.. 72" ..OR.. D9.88"'
    - - :warning
      - 'Line 178: Illegal quoting, probably in the following text: "85375-1-1.jpg
        ..OR.. 85375-1-2.jpg" ..OR.. W10"*H14"*D10" ..OR.. D5.13"*H0.75" ..OR.. L18*W21*H14"
        ..OR.. 24" ..OR.. 60" ..OR.. 1*6+3*12" ..OR.. 72" ..OR.. D9.88"'
    - - :warning
      - 'Line 179: Illegal quoting, probably in the following text: W38"*H38"*D38"
        ..OR.. D6.4*H1.88" ..OR.. L41*W41*H40" ..OR.. L32*W24*H24" ..OR.. L32*W24*H24"
        ..OR.. 48" ..OR.. 72" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D10*H1.5"'
    - - :warning
      - 'Line 180: Illegal quoting, probably in the following text: "85122-12.jpg
        ..OR.. 85122-12_1.jpg" ..OR.. W26"*H26"*D26" ..OR.. D6.4*H1.88" ..OR.. L31*W31*H31"
        ..OR.. L30*W24*H24" ..OR.. 36" ..OR.. 66" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR..
        D10*H1.5"'
    - - :warning
      - 'Line 181: Illegal quoting, probably in the following text: "85123-6.jpg ..OR..
        85123-6_1.jpg" ..OR.. W24"*H18"*D24" ..OR.. D6.4*H1.88" ..OR.. L28*W26*H26"
        ..OR.. 1*6" ..OR.. 7" ..OR.. D10*H1.5"'
    - - :warning
      - 'Line 182: Illegal quoting, probably in the following text: "85124-8-1.jpg
        ..OR.. 85124-8-5.jpg" ..OR.. W58"*H10"*D13" ..OR.. L16.88"*W5.88"*H0.88" ..OR..
        L54*W14*H16" ..OR.. 13" ..OR.. 49" ..OR.. 2*6+6*12" ..OR.. 72" ..OR.. D9.63"*1.63"'
    - - :warning
      - 'Line 183: Illegal quoting, probably in the following text: "85125-3-1.jpg
        ..OR.. 85125-3-2.jpg" ..OR.. W15"*H27"*D6" ..OR.. L24*W15*H13" ..OR.. D4.75"*H0.75"
        ..OR.. 7" ..OR.. D9.63"*1.63"'
    - - :warning
      - 'Line 184: Illegal quoting, probably in the following text: W24"*H27"*D24"
        ..OR.. D5.88*H0.88" ..OR.. L28*W28*H29" ..OR.. 36" ..OR.. 72" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D23.75*H23.75"'
    - - :warning
      - 'Line 185: Illegal quoting, probably in the following text: W16"*H19"*D16"
        ..OR.. D5.88*H0.88" ..OR.. L19.5*W19.5*H20.75" ..OR.. 29" ..OR.. 65" ..OR..
        1*6"+3*12" ..OR.. 120" ..OR.. D15.75*H15.75"'
    - - :warning
      - 'Line 186: Illegal quoting, probably in the following text: "85221-1.jpg ..OR..
        85221-1_1.jpg" ..OR.. W8"*H10"*D8" ..OR.. D5.88*H0.88" ..OR.. L11*W11*H13"
        ..OR.. 20" ..OR.. 56" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D7.5*H7.5"'
    - - :warning
      - 'Line 187: Illegal quoting, probably in the following text: W41"*H31"*D41"
        ..OR.. D5.5*H1" ..OR.. L43*W43*H9" ..OR.. 34" ..OR.. 106" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 188: Illegal quoting, probably in the following text: W29"*H27"*D29"
        ..OR.. D5.5*H1" ..OR.. L32*W32*H9" ..OR.. 32" ..OR.. 102" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 189: Illegal quoting, probably in the following text: W6"*H18"*D4" ..OR..
        L21*W8*H7" ..OR.. L18*W5.75*H1.25" ..OR.. 7"'
    - - :warning
      - 'Line 190: Illegal quoting, probably in the following text: "85111-6.jpg ..OR..
        85111-6_1.jpg" ..OR.. W36"*H18"*D36" ..OR.. D5.1*H0.75" ..OR.. L40*W40*H22"
        ..OR.. 32" ..OR.. 80" ..OR.. 1*6"+3*12" ..OR.. 120" ..OR.. D36*H18"'
    - - :warning
      - 'Line 191: Illegal quoting, probably in the following text: W24"*H12"*D24"
        ..OR.. D5.1*H0.75" ..OR.. L28*W28*H16" ..OR.. 32" ..OR.. 74" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D24*H12"'
    - - :warning
      - 'Line 192: Illegal quoting, probably in the following text: W16"*H16"*D16"
        ..OR.. D5.1*H0.75" ..OR.. L19*W19*H19" ..OR.. 30" ..OR.. 73" ..OR.. 1*6"+3*12"
        ..OR.. 120" ..OR.. D16*H15.5"'
    - - :warning
      - 'Line 193: Illegal quoting, probably in the following text: W36"*H21"*D36"
        ..OR.. D5.5*H1" ..OR.. L39*W39*H13" ..OR.. 24" ..OR.. 96" ..OR.. 1*72" ..OR..
        120"'
    - - :warning
      - 'Line 194: Illegal quoting, probably in the following text: "85141-6.jpg ..OR..
        85141-6_1.jpg" ..OR.. W27"*H18"*D27" ..OR.. D5.5*H1" ..OR.. L30*W30*H12" ..OR..
        21" ..OR.. 93" ..OR.. 1*72" ..OR.. 120"'
    - - :warning
      - 'Line 195: Illegal quoting, probably in the following text: W14"*H21"*D14"
        ..OR.. D5.5*H1" ..OR.. L18*W18*H30" ..OR.. 24" ..OR.. 96" ..OR.. "Iron ..OR..
        solid wood and glass" ..OR.. 1*72" ..OR.. 120" ..OR.. L11.6*W10*H3"'
    - - :warning
      - 'Line 196: Illegal quoting, probably in the following text: "65000-1.jpg ..OR..
        65000-6.jpg" ..OR.. W5"*H19"*D3" ..OR.. W4.72"*H18"'
    - - :warning
      - 'Line 197: Illegal quoting, probably in the following text: "65001-1.jpg ..OR..
        65001-7.jpg" ..OR.. W5"*H24"*D3" ..OR.. W4.72"*H24.7"'
    - - :warning
      - 'Line 198: Illegal quoting, probably in the following text: "65060-1.jpg ..OR..
        65060-5.jpg" ..OR.. W6"*H18"*D3"'
    - - :warning
      - 'Line 199: Illegal quoting, probably in the following text: "65061-1.jpg ..OR..
        65061-5.jpg" ..OR.. W6"*H27"*D3"'
    - - :warning
      - 'Line 200: Illegal quoting, probably in the following text: "65030-1.jpg ..OR..
        65030-4.jpg" ..OR.. W7"*H14"*D4" ..OR.. W7"*H14.37"'
    - - :warning
      - 'Line 201: Illegal quoting, probably in the following text: "65031-1.jpg ..OR..
        65031-4.jpg" ..OR.. W7"*H24"*D4" ..OR.. W7"*H24"'
    - - :warning
      - 'Line 202: Illegal quoting, probably in the following text: "65040-1.jpg ..OR..
        65040-5.jpg" ..OR.. W6"*H16"*D3" ..OR.. "Stainless steel ..OR..  aluminium
        and crystal"'
    - - :warning
      - 'Line 203: Illegal quoting, probably in the following text: "65041-1.jpg ..OR..
        65041-5.jpg" ..OR.. W6"*H24"*D3" ..OR.. "Stainless steel ..OR..  aluminium
        and crystal"'
    - - :warning
      - 'Line 204: Illegal quoting, probably in the following text: "65010-1.jpg ..OR..
        65010-5.jpg" ..OR.. W6"*H11"*D3" ..OR.. W4.72"*H4.3"'
    - - :warning
      - 'Line 205: Illegal quoting, probably in the following text: "65011-1.jpg ..OR..
        65011-5.jpg" ..OR.. W6"*H15"*D3" ..OR.. W4.72"*H4.3"'
    - - :warning
      - 'Line 206: Illegal quoting, probably in the following text: "65050-1.jpg ..OR..
        65050-5.jpg" ..OR.. W7"*H14"*D2"'
    - - :warning
      - 'Line 207: Illegal quoting, probably in the following text: "65051-1.jpg ..OR..
        65051-4.jpg" ..OR.. W7"*H18"*D2"'
    - - :warning
      - 'Line 208: Illegal quoting, probably in the following text: "65090-1.jpg ..OR..
        65090-4.jpg" ..OR.. W5"*H16"*D4"'
    - - :warning
      - 'Line 209: Illegal quoting, probably in the following text: "65091-1.jpg ..OR..
        65091-4.jpg" ..OR.. W5"*H24"*D4"'
 |

### Q-10_results.md

# Q-10 Results — Arabela Lighting (arl, org_id=269)
- **Query**: Q-10 — Feature Enablement Gap Analysis
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-11_results.md

# Q-11 Results — Arabela Lighting (arl, org_id=269)
- **Query**: Q-11 — Configuration Completeness
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| entity_type | last_updated | days_stale | related_record_count |
| --- | --- | --- | --- |
| contract_prices | 2025-08-07 23:13:14 | 313 | 0 |
| customer_favorites | 2025-08-07 23:13:14 | 313 | — |
| kit_items | 2025-08-07 23:13:14 | 313 | 0 |
| matrix_options | 2025-08-07 23:13:14 | 313 | — |
| option_groups | 2025-08-07 23:13:14 | 313 | — |
| options | 2025-08-07 23:13:14 | 313 | — |
| commitment_reports | 2025-08-07 23:13:14 | 313 | — |
| placement_reports | 2025-08-07 23:13:14 | 313 | — |
| riser_prices | 2025-08-07 23:13:14 | 313 | — |
| customer_payment_informations | 2025-08-07 23:13:14 | 313 | — |
| sales_quotas | 2025-08-07 23:13:14 | 313 | 0 |
| inventories | 2025-12-11 15:14:10 | 188 | — |
| portal_orders | 2026-03-13 14:23:45 | 96 | — |
| portal_invoices | 2026-03-13 14:23:45 | 96 | — |
| customers | 2026-03-24 15:04:10 | 85 | — |

### Q-22_results.md

# Q-22 Results — Arabela Lighting (arl, org_id=269)
- **Query**: Q-22 — Feature Usage Depth
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | submit_order | select_a_customer | search_for_customer | email_item_info | create_pdf_catalog | view_library_entry | view_smartpicks | access_sales_portal | filter_products | search_products | search_collections | order_configured_item | view_kit | order_kit | share_my_list | export_data_to_csv | export_data_to_excel | total_events | total_users |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arl | Arabela Lighting | 0 | 990 | 246 | 59 | 105 | 2,224 | 7 | 40 | 71 | 2,636 | 8 | 0 | 0 | 0 | 3 | 0 | 0 | 15,214 | 64 |

### Q-CI-02_results.md

# Q-CI-02 Results — Arabela Lighting (arl, org_id=269)
- **Query**: Q-CI-02 — Peer Comparison
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | peer_standing | orders_vs_peer_pct | logins_vs_peer_pct | mrr_vs_peer_pct | peer_orders_median | peer_logins_median | peer_mrr_median |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arl | Arabela Lighting | Catalog-Focused | Needs Attention | — | 738.50 | 1,100 | 0 | 278 | 725 |

### Q-CI-03_results.md

# Q-CI-03 Results — Arabela Lighting (arl, org_id=269)
- **Query**: Q-CI-03 — Feature Adoption Benchmarking
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | feature_depth | has_clicky_portal | arr |
| --- | --- | --- | --- | --- | --- |
| arl | Arabela Lighting | Catalog-Focused | 5 | 0 | 8,700 |

### Q-CI-03_benchmarks_results.md

# Q-CI-03-bench Results — Arabela Lighting (arl, org_id=269)
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
