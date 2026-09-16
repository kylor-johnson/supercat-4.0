# Section 6 Context Bundle — Currey & Company (cci)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Currey & Company (cci, org_id=161)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=57730, portal_order_gmv=$87.6M |
| HAS_INVENTORY | True | inventory_count=3443 |
| HAS_SALES_DATA | True | sales_data_count=110748 |
| HAS_SALES_SECTION | True | mode=orders order_reps=37 engagement_reps=0 (threshold: >=5) |
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
| VM45_GATE_1 | PASS | erp_gmv=$87.6M > ecat_gmv=$8.6M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 37 | 37 |
| ENGAGEMENT_REP_COUNT | 0 |  |
| SALES_SECTION_MODE | orders | orders |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 76 rows |
| SHOWROOM_EXCLUSIONS | 3 | 3 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 3985, Mixpanel total submit_order (Q-01): 6616 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=97.4%, ambiguous_rate=0.0%, showroom_event_share=8.5% |
| USER_GROUP_JOIN_RATE | 97% | 74 of 76 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 9% | showroom+admin share of matched events: 8.5% |
| ADMIN_REPS_IN_LEADERBOARD | True | 4 admin/showroom users in leaderboard: Atlanta Showroom, CC Dallas Showroom, Highpoint Showroom, Allan Otto |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=2 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=53 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=7906 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=369 |
| HAS_BUYER_DATA | True | distinct_buyers_6mo=3184 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Currey & Company
- **Shortname**: cci
- **Org ID**: 161
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Currey & Company (cci, org_id=161)
- **Run date**: 2026-06-17

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | True |
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
| §2 Sales Team | FULL | See Derived Gate 6 §2 formula |
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

# Signal Rank — Currey & Company (cci, org_id=161)
- **Run date**: 2026-06-17
- **Total signals fired**: 56 (P0: 34, P1: 21, P2: 1)
- **Org GMV**: $8.6M eCat LTM, $87.6M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-TEAM-01 | Rep/Agency Capture Rate Gap — 8 reps at 0% eCat capture on $31.5M total business | P1 | §5 Team | 252.0 | $31,500,000 | 2.0 | 15,876,000,000 | POSITIVE |
| 2 | SIG-OPP-01 | Next Best Product — 9000-0135/9000-0143 co-purchase pattern across 77 customers | P0 | §2/§3 | 7.7 | $32,879,194 | 2.0 | 506,339,588 | POSITIVE |
| 3 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $13.9M+ total business, zero eCat orders | P1 | §2 Accounts | 13.9 | $13,861,823 | 2.0 | 384,300,274 | POSITIVE |
| 4 | SIG-COMMERCE-01 | Capture Rate — eCat captures 9.8% of $88M total business; each +1pt = $876K | P0 | §4 Commerce | 4.5 | $876,000 | 3.0 | 11,850,000 | POSITIVE |
| 5 | SIG-MOM-01 | Account Acceleration — LILLIAN JAMES DESIGN GROUP 4 consecutive QoQ acceleration quarters, $110,380 peak quarter (+934% QoQ) | P0 | §2 Accounts | 31.1 | $110,380 | 3.0 | 10,312,818 | POSITIVE |
| 6 | SIG-ANOMALY-03 | Competitive Displacement — DEFINED INTERIORS total biz +541% but eCat -100% | P0 | §2 Accounts | 42.7 | $57,855 | 3.0 | 7,413,567 | RISK |
| 7 | SIG-MOM-01 | Account Acceleration — BAY DESIGN 3 consecutive QoQ acceleration quarters, $78,913 peak quarter (+925% QoQ) | P0 | §2 Accounts | 30.8 | $78,913 | 3.0 | 7,298,634 | POSITIVE |
| 8 | SIG-MOM-01 | Account Acceleration — WILSON LIGHTING - OVERLAND PRK 2 consecutive QoQ acceleration quarters, $77,581 peak quarter (+616% QoQ) | P0 | §2 Accounts | 20.5 | $77,581 | 3.0 | 4,779,784 | POSITIVE |
| 9 | SIG-MOM-01 | Account Acceleration — WESTEND PROPERTIES LTD 2 consecutive QoQ acceleration quarters, $112,801 peak quarter (+404% QoQ) | P0 | §2 Accounts | 13.5 | $112,801 | 3.0 | 4,553,775 | POSITIVE |
| 10 | SIG-MOM-01 | Account Acceleration — CROMWELL AUSTRALIA PTY LTD 2 consecutive QoQ acceleration quarters, $100,868 peak quarter (+418% QoQ) | P0 | §2 Accounts | 13.9 | $100,868 | 3.0 | 4,218,293 | POSITIVE |
| 11 | SIG-DECAY-04 | Spending Contraction — BEYOND INC -77.4% YoY ($306,714→$69,264), $237,450 gap | P0 | §2 Accounts | 3.9 | $237,450 | 3.0 | 2,756,791 | RISK |
| 12 | SIG-DECAY-04 | Spending Contraction — DESIGNSOURCE INTERNATIONAL -70.8% YoY ($327,412→$95,532), $231,880 gap | P0 | §2 Accounts | 3.5 | $231,880 | 3.0 | 2,462,566 | RISK |
| 13 | SIG-MOM-01 | Account Acceleration — ROBB & STUCKY INTERNATIONAL 2 consecutive QoQ acceleration quarters, $96,623 peak quarter (+187% QoQ) | P0 | §2 Accounts | 6.2 | $96,623 | 3.0 | 1,806,850 | POSITIVE |
| 14 | SIG-DECAY-04 | Spending Contraction — LAMPS.COM -55.3% YoY ($324,958→$145,295), $179,663 gap | P0 | §2 Accounts | 2.8 | $179,663 | 3.0 | 1,490,306 | RISK |
| 15 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 53% of eCat GMV | P1 | §4 Commerce | 1.3 | $541,073 | 2.0 | 1,431,238 | RISK |
| 16 | SIG-MOM-01 | Account Acceleration — CAI DESIGNS 2 consecutive QoQ acceleration quarters, $133,301 peak quarter (+105% QoQ) | P0 | §2 Accounts | 3.5 | $133,301 | 3.0 | 1,394,326 | POSITIVE |
| 17 | SIG-MOM-01 | Account Acceleration — FURNITURELAND SOUTH 2 consecutive QoQ acceleration quarters, $139,458 peak quarter (+98% QoQ) | P0 | §2 Accounts | 3.3 | $139,458 | 3.0 | 1,363,902 | POSITIVE |
| 18 | SIG-ANOMALY-03 | Competitive Displacement — ROBB & STUCKY INTERNATIONAL total biz +55% but eCat -20% | P0 | §2 Accounts | 5.0 | $88,611 | 3.0 | 1,329,164 | RISK |
| 19 | SIG-DECAY-03 | Rep Trajectory — Rip Nance orders -37.9% QoQ, $105,764 current 90d GMV | P1 | §5 Team | 1.5 | $423,056 | 2.0 | 1,282,706 | RISK |
| 20 | SIG-DECAY-03 | Rep Trajectory — Atlanta Showroom orders -40.5% QoQ, $92,410 current 90d GMV | P1 | §5 Team | 1.6 | $369,640 | 2.0 | 1,197,634 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 33 | 1 | 0 | 34 | |
| §3 Product Intelligence | 0 | 0 | 1 | 1 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §5 Team Intelligence | 0 | 8 | 0 | 8 | |
| §6 Platform Context | 0 | 11 | 0 | 11 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-TEAM-01: Rep/Agency Capture Rate Gap — 8 reps at 0% eCat capture on $31.5M total business
2. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — 9000-0135/9000-0143 co-purchase pattern across 77 customers
3. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $13.9M+ total business, zero eCat orders
4. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 9.8% of $88M total business; each +1pt = $876K
5. **[RISK]** SIG-ANOMALY-03: Competitive Displacement — DEFINED INTERIORS total biz +541% but eCat -100%
6. **[RISK]** SIG-DECAY-04: Spending Contraction — BEYOND INC -77.4% YoY ($306,714→$69,264), $237,450 gap
7. **[RISK]** SIG-DECAY-04: Spending Contraction — DESIGNSOURCE INTERNATIONAL -70.8% YoY ($327,412→$95,532), $231,880 gap

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-07_results.md

# Q-07 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 2
- **Run date**: 2026-06-17


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| hidden | 2,736 | 277 | 2 | 89.90 |
| visible | 3,394 | 144 | 17 | 95.80 |

### Q-08_results.md

# Q-08 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-08 — Data Freshness Monitor
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 22
- **Run date**: 2026-06-17


| entity_type | last_updated | days_since_update | status |
| --- | --- | --- | --- |
| price_levels | 2025-08-20 19:47:14 | 301 | Stale |
| collections | 2025-08-20 19:47:14 | 301 | Stale |
| trade_names | 2025-08-20 19:47:14 | 301 | Stale |
| contract_prices | 2025-08-20 19:47:14 | 301 | Stale |
| kit_items | 2025-08-20 19:47:14 | 301 | Stale |
| matrix_options | 2025-08-20 19:47:14 | 301 | Stale |
| option_groups | 2025-08-20 19:47:14 | 301 | Stale |
| options | 2025-08-20 19:47:14 | 301 | Stale |
| commitment_reports | 2025-08-20 19:47:14 | 301 | Stale |
| riser_prices | 2025-08-20 19:47:14 | 301 | Stale |
| sales_quotas | 2025-08-20 19:47:14 | 301 | Stale |
| placement_reports | 2026-04-15 14:17:20 | 63 | Monitor |
| categories | 2026-04-27 12:42:49 | 51 | Monitor |
| groups | 2026-04-27 12:42:49 | 51 | Monitor |
| customer_payment_informations | 2026-06-17 09:32:09 | 0 | Fresh |
| customers | 2026-06-17 09:50:37 | 0 | Fresh |
| customer_favorites | 2026-06-17 09:51:33 | 0 | Fresh |
| portal_orders | 2026-06-17 09:53:59 | 0 | Fresh |
| portal_invoices | 2026-06-17 09:56:04 | 0 | Fresh |
| products | 2026-06-18 04:17:15 | 0 | Fresh |
| smart_stacks | 2026-06-18 04:17:15 | 0 | Fresh |
| inventories | 2026-06-18 05:07:21 | 0 | Fresh |

### Q-09_results.md

# Q-09 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-09 — Import Health — Monthly Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 7
- **Run date**: 2026-06-17


| month | import_count |
| --- | --- |
| 2026-06-01 | 272 |
| 2026-05-01 | 507 |
| 2026-04-01 | 530 |
| 2026-03-01 | 467 |
| 2026-02-01 | 392 |
| 2026-01-01 | 432 |
| 2025-12-01 | 189 |

### Q-09_recent_results.md

# Q-09-recent Results — Currey & Company (cci, org_id=161)
- **Query**: Q-09-recent — Import Health — Recent Errors
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| created_at | data |
| --- | --- |
| 2026-06-18T05:07:21.814834 | ---
- - Inventory
  - []
 |
| 2026-06-18T04:17:52.268028 | ---
- - Products
  - - - :warning
      - 'Line 338: Related item: ''9600-0004'' not found, BaseItemCode=5500-0001'
    - - :warning
      - 'Line 338: Related item: ''9500-0003'' not found, BaseItemCode=5500-0001'
    - - :warning
      - 'Line 338: Related item: ''9600-0003'' not found, BaseItemCode=5500-0001'
    - - :error
      - "Line 3711: BaseItemCode: 4000-0206: Invalid category code: 'FUR\tACCENTPIE'"
    - - :warning
      - 'Line 5266: 12 image limit exceeded, image(s) (1200-1127_13.jpg,1200-1127_14.jpg,1200-1127_15.jpg)
        not imported., BaseItemCode=1200-1127'
 |
| 2026-06-18T01:09:20.204128 | ---
- - Inventory
  - []
 |
| 2026-06-17T22:07:10.971731 | ---
- - Images
  - - - :information
      - 'The following images were imported: 5900-0009_6.jpg'
 |
| 2026-06-17T21:04:21.469536 | ---
- - Inventory
  - []
 |
| 2026-06-17T20:09:51.959503 | ---
- - Products
  - - - :warning
      - 'Line 338: Related item: ''9600-0004'' not found, BaseItemCode=5500-0001'
    - - :warning
      - 'Line 338: Related item: ''9500-0003'' not found, BaseItemCode=5500-0001'
    - - :warning
      - 'Line 338: Related item: ''9600-0003'' not found, BaseItemCode=5500-0001'
    - - :error
      - "Line 3711: BaseItemCode: 4000-0206: Invalid category code: 'FUR\tACCENTPIE'"
    - - :warning
      - 'Line 5266: 12 image limit exceeded, image(s) (1200-1127_13.jpg,1200-1127_14.jpg,1200-1127_15.jpg)
        not imported., BaseItemCode=1200-1127'
 |
| 2026-06-17T17:06:22.600208 | ---
- - Inventory
  - []
 |
| 2026-06-17T13:06:20.410688 | ---
- - Inventory
  - []
 |
| 2026-06-17T12:16:48.341315 | ---
- - Products
  - - - :warning
      - 'Line 338: Related item: ''9600-0004'' not found, BaseItemCode=5500-0001'
    - - :warning
      - 'Line 338: Related item: ''9500-0003'' not found, BaseItemCode=5500-0001'
    - - :warning
      - 'Line 338: Related item: ''9600-0003'' not found, BaseItemCode=5500-0001'
    - - :error
      - "Line 3711: BaseItemCode: 4000-0206: Invalid category code: 'FUR\tACCENTPIE'"
    - - :warning
      - 'Line 5266: 12 image limit exceeded, image(s) (1200-1127_13.jpg,1200-1127_14.jpg,1200-1127_15.jpg)
        not imported., BaseItemCode=1200-1127'
 |
| 2026-06-17T09:56:04.256614 | ---
- - Sales Data
  - - - :warning
      - 'Line 1: Unclosed quoted field in line 1.'
    - - :error
      - 'Line 754: Base item code 9000-1268-SHADE does not match an active product'
    - - :error
      - 'Line 890: Base item code MISC does not match an active product'
    - - :error
      - 'Line 1163: Base item code 9000-K4 does not match an active product'
    - - :error
      - 'Line 3197: Base item code 6000-1006-FIN does not match an active product'
    - - :error
      - 'Line 5368: Base item code 0500-0090 does not match an active product'
    - - :error
      - 'Line 7707: Base item code 8000-0155-SHADE does not match an active product'
    - - :error
      - 'Line 9301: Base item code MISC does not match an active product'
    - - :error
      - 'Line 10979: BillToCode (0007978) is invalid.'
    - - :error
      - 'Line 10980: BillToCode (0007978) is invalid.'
    - - :error
      - 'Line 10981: BillToCode (0007978) is invalid.'
    - - :error
      - 'Line 11277: Base item code 1500-4804 does not match an active product'
    - - :error
      - 'Line 11622: Base item code 0919 does not match an active product'
    - - :error
      - 'Line 11802: Base item code 0500-0037 does not match an active product'
    - - :error
      - 'Line 11803: Base item code 0500-0038 does not match an active product'
    - - :error
      - 'Line 11983: Base item code MISC does not match an active product'
    - - :error
      - 'Line 12091: BillToCode (0008617) is invalid.'
    - - :error
      - 'Line 12092: BillToCode (0008617) is invalid.'
    - - :error
      - 'Line 12093: BillToCode (0008617) is invalid.'
    - - :error
      - 'Line 12094: BillToCode (0008617) is invalid.'
    - - :error
      - 'Line 12095: BillToCode (0008617) is invalid.'
    - - :error
      - 'Line 12096: BillToCode (0008617) is invalid.'
    - - :error
      - 'Line 12097: BillToCode (0008617) is invalid.'
    - - :error
      - 'Line 12098: BillToCode (0008617) is invalid.'
    - - :error
      - 'Line 12099: BillToCode (0008617) is invalid.'
    - - :error
      - 'Line 13213: Base item code 0500-0038 does not match an active product'
    - - :error
      - 'Line 14681: Base item code 2295-00 does not match an active product'
    - - :error
      - 'Line 17386: Base item code 2295-00 does not match an active product'
    - - :error
      - 'Line 18445: Base item code 0500-0055 does not match an active product'
    - - :error
      - 'Line 18446: Base item code 0500-0056 does not match an active product'
    - - :error
      - 'Line 18974: Base item code L090-0021-20 does not match an active product'
    - - :error
      - 'Line 20256: Base item code 6000-1026-SHADE does not match an active product'
    - - :error
      - 'Line 20865: BillToCode (0012861) is invalid.'
    - - :error
      - 'Line 20866: BillToCode (0012861) is invalid.'
    - - :error
      - 'Line 21459: Base item code MISC does not match an active product'
    - - :error
      - 'Line 22117: Base item code 9000-1339-KIT does not match an active product'
    - - :error
      - 'Line 25032: Base item code 967-999 does not match an active product'
    - - :error
      - 'Line 26347: BillToCode (0016050) is invalid.'
    - - :error
      - 'Line 26348: BillToCode (0016050) is invalid.'
    - - :error
      - 'Line 26349: BillToCode (0016050) is invalid.'
    - - :error
      - 'Line 26350: BillToCode (0016050) is invalid.'
    - - :error
      - 'Line 26351: BillToCode (0016050) is invalid.'
    - - :error
      - 'Line 26352: BillToCode (0016050) is invalid.'
    - - :error
      - 'Line 26353: BillToCode (0016050) is invalid.'
    - - :error
      - 'Line 26604: BillToCode (0016186) is invalid.'
    - - :error
      - 'Line 26605: BillToCode (0016186) is invalid.'
    - - :error
      - 'Line 27960: Base item code MISC does not match an active product'
    - - :error
      - 'Line 28262: BillToCode (0017178) is invalid.'
    - - :error
      - 'Line 28263: BillToCode (0017178) is invalid.'
    - - :error
      - 'Line 28264: BillToCode (0017178) is invalid.'
    - - :error
      - 'Line 28265: BillToCode (0017178) is invalid.'
    - - :warning
      - "-318 more rows with invalid products"
- - Portal Orders
  - []
- - Portal Invoices
  - []
 |

### Q-10_results.md

# Q-10 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-10 — Feature Enablement Gap Analysis
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| enable_sales_portal | enable_online_catalog | enable_online_ordering | kit_item_count | contract_price_count | enrollment_count | smart_stack_count | shared_resource_count | portal_order_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 0 | 0 | 5 | 104 | 157,122 |

### Q-11_results.md

# Q-11 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-11 — Configuration Completeness
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 14
- **Run date**: 2026-06-17


| entity_type | last_updated | days_stale | related_record_count |
| --- | --- | --- | --- |
| price_levels | 2025-08-20 19:47:14 | 301 | — |
| collections | 2025-08-20 19:47:14 | 301 | — |
| trade_names | 2025-08-20 19:47:14 | 301 | — |
| contract_prices | 2025-08-20 19:47:14 | 301 | 0 |
| kit_items | 2025-08-20 19:47:14 | 301 | 0 |
| matrix_options | 2025-08-20 19:47:14 | 301 | — |
| option_groups | 2025-08-20 19:47:14 | 301 | — |
| options | 2025-08-20 19:47:14 | 301 | — |
| commitment_reports | 2025-08-20 19:47:14 | 301 | — |
| riser_prices | 2025-08-20 19:47:14 | 301 | — |
| sales_quotas | 2025-08-20 19:47:14 | 301 | 0 |
| placement_reports | 2026-04-15 14:17:20 | 63 | — |
| categories | 2026-04-27 12:42:49 | 51 | — |
| groups | 2026-04-27 12:42:49 | 51 | — |

### Q-22_results.md

# Q-22 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-22 — Feature Usage Depth
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | submit_order | select_a_customer | search_for_customer | email_item_info | create_pdf_catalog | view_library_entry | view_smartpicks | access_sales_portal | filter_products | search_products | search_collections | order_configured_item | view_kit | order_kit | share_my_list | export_data_to_csv | export_data_to_excel | total_events | total_users |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cci | Currey & Company | 6,616 | 16,664 | 46,341 | 612 | 874 | 2,623 | 154 | 376 | 1,101 | 46,279 | 6 | 0 | 0 | 0 | 24 | 0 | 0 | 176,379 | 76 |

### Q-CI-02_results.md

# Q-CI-02 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-CI-02 — Peer Comparison
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | peer_standing | orders_vs_peer_pct | logins_vs_peer_pct | mrr_vs_peer_pct | peer_orders_median | peer_logins_median | peer_mrr_median |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cci | Currey & Company | Platform-Embedded | Top Performer | 139.40 | 44.40 | 31.20 | 2,764 | 6,896 | 1,685 |

### Q-CI-03_results.md

# Q-CI-03 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-CI-03 — Feature Adoption Benchmarking
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | feature_depth | has_clicky_portal | arr |
| --- | --- | --- | --- | --- | --- |
| cci | Currey & Company | Platform-Embedded | 5 | 0 | 26,420 |

### Q-CI-03_benchmarks_results.md

# Q-CI-03-bench Results — Currey & Company (cci, org_id=161)
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
