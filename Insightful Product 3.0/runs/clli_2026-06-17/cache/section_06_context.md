# Section 6 Context Bundle — Craftmade (clli)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Craftmade (clli, org_id=149)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=168198, portal_order_gmv=$47.7M |
| HAS_INVENTORY | True | inventory_count=2867 |
| HAS_SALES_DATA | True | sales_data_count=508787 |
| HAS_SALES_SECTION | True | qualifying_reps=9 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Commerce-Active |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | clli_eol_portal |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$47.7M > ecat_gmv=$881,333: True |
| VM45_GATE_2 | FAIL | ecat_gmv >= 5% of erp_gmv: False |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 9 | 9 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 91 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 228, Mixpanel total submit_order (Q-01): 371 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=83.5%, ambiguous_rate=15.8%, showroom_event_share=7.3% |
| USER_GROUP_JOIN_RATE | 84% | 76 of 91 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 7% | showroom+admin share of matched events: 7.3% |
| ADMIN_REPS_IN_LEADERBOARD | True | 4 admin/showroom users in leaderboard: David Raushchuber, Kevin Ailara, Andrew  Rivera, Shayna Petty |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False | days_since_last_erp_order=9999 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=1722 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=289 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | STRONG | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | STRONG | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Craftmade
- **Shortname**: clli
- **Org ID**: 149
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- VM-45 skipped: Gate1=PASS, Gate2=FAIL

## Section Confidence

# Section Confidence Tiers — Craftmade (clli, org_id=149)
- **Run date**: 2026-06-17

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | False |
| PORTAL_CUSTOMER_DATA_PRESENT | True |
| PORTAL_ORDERS_FRESH | False |
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
| §3 Customer | STRONG | See Derived Gate 6 §3 formula |
| §4 Product | STRONG | See Derived Gate 6 §4 formula |
| §5 Commerce | STRONG | See Derived Gate 6 §5 formula |

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

# Signal Rank — Craftmade (clli, org_id=149)
- **Run date**: 2026-06-17
- **Total signals fired**: 51 (P0: 36, P1: 13, P2: 2)
- **Org GMV**: $0.9M eCat LTM, $47.7M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $8.3M+ total business, zero eCat orders | P1 | §2 Accounts | 8.3 | $8,279,294 | 2.0 | 137,093,418 | POSITIVE |
| 2 | SIG-MOM-01 | Account Acceleration —  3 consecutive QoQ acceleration quarters, $622,312 peak quarter (+180% QoQ) | P0 | §2 Accounts | 6.0 | $622,312 | 3.0 | 11,195,390 | POSITIVE |
| 3 | SIG-DECAY-04 | Spending Contraction —  -89.7% YoY ($899,202→$92,187), $807,015 gap | P0 | §2 Accounts | 4.5 | $807,015 | 3.0 | 10,858,392 | RISK |
| 4 | SIG-DECAY-04 | Spending Contraction —  -59.2% YoY ($1,788,691→$729,998), $1,058,693 gap | P0 | §2 Accounts | 3.0 | $1,058,693 | 3.0 | 9,401,193 | RISK |
| 5 | SIG-DECAY-04 | Spending Contraction —  -78.3% YoY ($957,251→$208,171), $749,080 gap | P0 | §2 Accounts | 3.9 | $749,080 | 3.0 | 8,797,942 | RISK |
| 6 | SIG-ANOMALY-02 | Stock Out — BW414AG3 (Bellows IV 14" 3-Blade Indoor/Outdoor (D) $281,687 LTM, 0 available | P0 | §3 Product | 10.0 | $281,687 | 3.0 | 8,450,620 | RISK |
| 7 | SIG-DECAY-04 | Spending Contraction —  -61.5% YoY ($1,414,384→$545,054), $869,331 gap | P0 | §2 Accounts | 3.1 | $869,331 | 3.0 | 8,019,576 | RISK |
| 8 | SIG-ANOMALY-02 | Stock Out — BW321AG3 (Bellows III 18" 3-Blade Indoor/Outdoor () $266,996 LTM, 0 available | P0 | §3 Product | 10.0 | $266,996 | 3.0 | 8,009,889 | RISK |
| 9 | SIG-COMMERCE-01 | Capture Rate — eCat captures 1.8% of $48M total business; each +1pt = $477K | P0 | §4 Commerce | 4.9 | $477,000 | 3.0 | 7,022,800 | POSITIVE |
| 10 | SIG-MOM-01 | Account Acceleration —  2 consecutive QoQ acceleration quarters, $104,278 peak quarter (+594% QoQ) | P0 | §2 Accounts | 19.8 | $104,278 | 3.0 | 6,188,876 | POSITIVE |
| 11 | SIG-ANOMALY-02 | Stock Out — 50504-FB (Bolden 4 Light Vanity in Flat Black) $193,427 LTM, 0 available | P0 | §3 Product | 10.0 | $193,427 | 3.0 | 5,802,810 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — 19624BNK3 (Drake 3 Light Vanity in Brushed Polished) $174,443 LTM, 0 available | P0 | §3 Product | 10.0 | $174,443 | 3.0 | 5,233,279 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — BSCB-B (Surface Mount Die-Cast Builder's Series ) $162,869 LTM, 0 available | P0 | §3 Product | 10.0 | $162,869 | 3.0 | 4,886,060 | RISK |
| 14 | SIG-ANOMALY-02 | Stock Out — Z402-TB (2 Light Directional Bullet in Textured B) $146,102 LTM, 0 available | P0 | §3 Product | 10.0 | $146,102 | 3.0 | 4,383,061 | RISK |
| 15 | SIG-MOM-01 | Account Acceleration —  2 consecutive QoQ acceleration quarters, $83,118 peak quarter (+490% QoQ) | P0 | §2 Accounts | 16.3 | $83,118 | 3.0 | 4,073,595 | POSITIVE |
| 16 | SIG-ANOMALY-02 | Stock Out — PH-2BZ (2 Light PAR Holder in Bronze) $132,167 LTM, 0 available | P0 | §3 Product | 10.0 | $132,167 | 3.0 | 3,964,999 | RISK |
| 17 | SIG-DECAY-04 | Spending Contraction —  -33.2% YoY ($1,528,897→$1,021,173), $507,724 gap | P0 | §2 Accounts | 1.7 | $507,724 | 3.0 | 2,528,463 | RISK |
| 18 | SIG-DECAY-04 | Spending Contraction —  -59.4% YoY ($403,858→$164,014), $239,843 gap | P0 | §2 Accounts | 3.0 | $239,843 | 3.0 | 2,137,005 | RISK |
| 19 | SIG-DECAY-04 | Spending Contraction —  -55.6% YoY ($422,120→$187,615), $234,505 gap | P0 | §2 Accounts | 2.8 | $234,505 | 3.0 | 1,955,775 | RISK |
| 20 | SIG-MOM-01 | Account Acceleration —  2 consecutive QoQ acceleration quarters, $87,277 peak quarter (+164% QoQ) | P0 | §2 Accounts | 5.5 | $87,277 | 3.0 | 1,428,729 | POSITIVE |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 28 | 1 | 0 | 29 | |
| §3 Product Intelligence | 7 | 0 | 1 | 8 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §6 Platform Context | 0 | 11 | 1 | 12 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $8.3M+ total business, zero eCat orders
2. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration —  3 consecutive QoQ acceleration quarters, $622,312 peak quarter (+180% QoQ)
3. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 1.8% of $48M total business; each +1pt = $477K
4. **[POSITIVE/MOMENTUM]** SIG-OPP-04: New Item Adoption Gap — 30 new items with $0 platform orders
5. **[RISK]** SIG-ANOMALY-02: Stock Out — BW414AG3 (Bellows IV 14" 3-Blade Indoor/Outdoor (D) $281,687 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — BW321AG3 (Bellows III 18" 3-Blade Indoor/Outdoor () $266,996 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 50504-FB (Bolden 4 Light Vanity in Flat Black) $193,427 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-08_results.md

# Q-08 Results — Craftmade (clli, org_id=149)
- **Query**: Q-08 — Data Freshness Monitor
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 22
- **Run date**: 2026-06-17


| entity_type | last_updated | days_since_update | status |
| --- | --- | --- | --- |
| sales_quotas | 2025-08-20 19:47:14 | 301 | Stale |
| customer_payment_informations | 2025-08-20 19:47:14 | 301 | Stale |
| riser_prices | 2025-08-20 19:47:14 | 301 | Stale |
| placement_reports | 2025-08-20 19:47:14 | 301 | Stale |
| commitment_reports | 2025-08-20 19:47:14 | 301 | Stale |
| options | 2025-08-20 19:47:14 | 301 | Stale |
| option_groups | 2025-08-20 19:47:14 | 301 | Stale |
| matrix_options | 2025-08-20 19:47:14 | 301 | Stale |
| kit_items | 2025-08-20 19:47:14 | 301 | Stale |
| contract_prices | 2025-08-20 19:47:14 | 301 | Stale |
| customer_favorites | 2025-08-20 19:47:14 | 301 | Stale |
| price_levels | 2026-01-12 00:22:08 | 156 | Monitor |
| customers | 2026-06-17 13:19:24 | 0 | Fresh |
| portal_invoices | 2026-06-17 13:55:09 | 0 | Fresh |
| products | 2026-06-17 18:00:55 | 0 | Fresh |
| categories | 2026-06-17 18:00:56 | 0 | Fresh |
| collections | 2026-06-17 18:00:56 | 0 | Fresh |
| groups | 2026-06-17 18:00:56 | 0 | Fresh |
| trade_names | 2026-06-17 18:00:56 | 0 | Fresh |
| portal_orders | 2026-06-17 18:07:11 | 0 | Fresh |
| smart_stacks | 2026-06-17 18:38:11 | 0 | Fresh |
| inventories | 2026-06-17 20:21:19 | 0 | Fresh |

### Q-09_results.md

# Q-09 Results — Craftmade (clli, org_id=149)
- **Query**: Q-09 — Import Health — Monthly Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 7
- **Run date**: 2026-06-17


| month | import_count |
| --- | --- |
| 2026-06-01 | 768 |
| 2026-05-01 | 1,269 |
| 2026-04-01 | 1,214 |
| 2026-03-01 | 1,203 |
| 2026-02-01 | 1,052 |
| 2026-01-01 | 1,153 |
| 2025-12-01 | 513 |

### Q-09_recent_results.md

# Q-09-recent Results — Craftmade (clli, org_id=149)
- **Query**: Q-09-recent — Import Health — Recent Errors
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| created_at | data |
| --- | --- |
| 2026-06-17 20:21:19 | ---
- - Inventory
  - []
 |
| 2026-06-17 19:20:20 | ---
- - Inventory
  - []
 |
| 2026-06-17 18:20:18 | ---
- - Inventory
  - []
 |
| 2026-06-17 18:07:11 | ---
- - Portal Orders
  - []
 |
| 2026-06-17 18:01:16 | ---
- - Products
  - - - :warning
      - 'Line 1: Field name i.qty_available is unknown.'
    - - :warning
      - 'Line 23: ImageFileName:  is not valid and will not be imported'
    - - :warning
      - 'Line 272: BaseItemCode: 86226FB-T: The following scan group codes are already
        used as an item number: 86226'
    - - :warning
      - 'Line 366: ImageFileName:  is not valid and will not be imported'
    - - :warning
      - 'Line 582: field materials truncated to 50 characters, BaseItemCode=SOF42BNK3'
    - - :warning
      - 'Line 583: field materials truncated to 50 characters, BaseItemCode=SOF42SB3'
    - - :warning
      - 'Line 589: field materials truncated to 50 characters, BaseItemCode=WHL42BNK5C1'
    - - :warning
      - 'Line 590: field materials truncated to 50 characters, BaseItemCode=WHL42FB5C1'
    - - :warning
      - 'Line 591: field materials truncated to 50 characters, BaseItemCode=WHL42W5C1'
    - - :warning
      - 'Line 592: field materials truncated to 50 characters, BaseItemCode=WHL42BNK5C3'
    - - :warning
      - 'Line 593: field materials truncated to 50 characters, BaseItemCode=WHL42FB5C3'
    - - :warning
      - 'Line 594: field materials truncated to 50 characters, BaseItemCode=WHL42W5C3'
    - - :warning
      - 'Line 595: field materials truncated to 50 characters, BaseItemCode=WHL52BNK5C1'
    - - :warning
      - 'Line 596: field materials truncated to 50 characters, BaseItemCode=WHL52FB5C1'
    - - :warning
      - 'Line 597: field materials truncated to 50 characters, BaseItemCode=WHL52W5C1'
    - - :warning
      - 'Line 598: field materials truncated to 50 characters, BaseItemCode=WHL52BNK5C3'
    - - :warning
      - 'Line 599: field materials truncated to 50 characters, BaseItemCode=WHL52FB5C3'
    - - :warning
      - 'Line 600: field materials truncated to 50 characters, BaseItemCode=WHL52W5C3'
    - - :warning
      - 'Line 674: Related item: ''N/A'' not found, BaseItemCode=WCFL-1000'
    - - :warning
      - 'Line 674: BaseItemCode: WCFL-1000: The following scan group codes are already
        used as an item number: WCFL-1000'
    - - :warning
      - 'Line 687: BaseItemCode CLZ72FB6 listed more than once. Only last record updated.'
    - - :warning
      - 'Line 688: BaseItemCode CLZ72FB6 listed more than once. Only last record updated.'
    - - :warning
      - 'Line 716: 6 image limit exceeded, image(s) (CM-7W-LED.jpg) not imported.,
        BaseItemCode=MCY52BNK3'
    - - :warning
      - 'Line 970: field materials truncated to 50 characters, BaseItemCode=CHS52PLN5'
    - - :warning
      - 'Line 971: field materials truncated to 50 characters, BaseItemCode=CHS52SB5-NWF'
    - - :warning
      - 'Line 1153: BaseItemCode: 86263: The following scan group codes are already
        used as an item number: 86263'
    - - :warning
      - 'Line 1154: BaseItemCode: 86265: The following scan group codes are already
        used as an item number: 86265'
    - - :warning
      - 'Line 1155: BaseItemCode: 86266: The following scan group codes are already
        used as an item number: 86266'
    - - :warning
      - 'Line 1156: BaseItemCode: 86267: The following scan group codes are already
        used as an item number: 86267'
    - - :warning
      - 'Line 1157: BaseItemCode: 86268: The following scan group codes are already
        used as an item number: 86268'
    - - :warning
      - 'Line 1195: BaseItemCode: 9700: The following scan group codes are already
        used as an item number: 9700'
    - - :warning
      - 'Line 1196: BaseItemCode: CMAWF-ABZ: The following scan group codes are already
        used as an item number: CMAWF-ABZ'
    - - :warning
      - 'Line 1197: BaseItemCode: CMAWF-AN: The following scan group codes are already
        used as an item number: CMAWF-AN'
    - - :warning
      - 'Line 1198: BaseItemCode: CMAWF-BN: The following scan group codes are already
        used as an item number: CMAWF-BN'
    - - :warning
      - 'Line 1199: BaseItemCode: CMAWF-BNK: The following scan group codes are already
        used as an item number: CMAWF-BNK'
    - - :warning
      - 'Line 1200: BaseItemCode: CMAWF-ESP: The following scan group codes are already
        used as an item number: CMAWF-ESP'
    - - :warning
      - 'Line 1201: BaseItemCode: CMAWF-FB: The following scan group codes are already
        used as an item number: CMAWF-FB'
    - - :warning
      - 'Line 1202: BaseItemCode: CMAWF-PN: The following scan group codes are already
        used as an item number: CMAWF-PN'
    - - :warning
      - 'Line 1203: BaseItemCode: CMAWF-SB: The following scan group codes are already
        used as an item number: CMAWF-SB'
    - - :warning
      - 'Line 1204: BaseItemCode: CMAWF-W: The following scan group codes are already
        used as an item number: CMAWF-W'
    - - :warning
      - 'Line 1215: field materials truncated to 50 characters, BaseItemCode=SON52SB3-CAP-NWF'
    - - :warning
      - 'Line 1264: BaseItemCode: WUCI-1000: The following scan group codes are already
        used as an item number: WUCI-1000'
    - - :warning
      - 'Line 1337: 6 image limit exceeded, image(s) (WIDC-Remote.jpg) not imported.,
        BaseItemCode=JOU64BNK3'
    - - :warning
      - 'Line 2498: BaseItemCode: 86201: The following scan group codes are already
        used as an item number: 86201'
    - - :warning
      - 'Line 2499: BaseItemCode: 86202: The following scan group codes are already
        used as an item number: 86202'
    - - :warning
      - 'Line 2500: BaseItemCode: 86203: The following scan group codes are already
        used as an item number: 86203'
    - - :warning
      - 'Line 2501: BaseItemCode: 86216: The following scan group codes are already
        used as an item number: 86216'
    - - :warning
      - 'Line 2502: BaseItemCode: 86222: The following scan group codes are already
        used as an item number: 86222'
    - - :warning
      - 'Line 2503: BaseItemCode: 86224: The following scan group codes are already
        used as an item number: 86224'
    - - :warning
      - 'Line 2504: BaseItemCode: 86226: The following scan group codes are already
        used as an item number: 86226'
    - - :warning
      - 'Line 2505: BaseItemCode: 86233: The following scan group codes are already
        used as an item number: 86233'
    - - :warning
      - 'Line 2506: BaseItemCode: 86237: The following scan group codes are already
        used as an item number: 86237'
    - - :warning
      - 'Line 2507: BaseItemCode: 86243: The following scan group codes are already
        used as an item number: 86243'
    - - :warning
      - 'Line 2508: BaseItemCode: 86248: The following scan group codes are already
        used as an item number: 86248'
    - - :warning
      - 'Line 2509: BaseItemCode: 86249: The following scan group codes are already
        used as an item number: 86249'
    - - :warning
      - 'Line 2510: BaseItemCode: 86251: The following scan group codes are already
        used as an item number: 86251'
    - - :warning
      - 'Line 2511: BaseItemCode: 86252: The following scan group codes are already
        used as an item number: 86252'
    - - :warning
      - 'Line 2512: BaseItemCode: 86253: The following scan group codes are already
        used as an item number: 86253'
    - - :warning
      - 'Line 2513: BaseItemCode: 86254: The following scan group codes are already
        used as an item number: 86254'
    - - :warning
      - 'Line 2514: BaseItemCode: 86255: The following scan group codes are already
        used as an item number: 86255'
    - - :warning
      - 'Line 2515: BaseItemCode: 86258: The following scan group codes are already
        used as an item number: 86258'
    - - :warning
      - 'Line 2516: BaseItemCode: 86244: The following scan group codes are already
        used as an item number: 86244'
    - - :warning
      - 'Line 2601: BaseItemCode: T1610: The following scan group codes are already
        used as an item number: T1610'
    - - :warning
      - 'Line 2602: BaseItemCode: T1615: The following scan group codes are already
        used as an item number: T1615'
    - - :warning
      - 'Line 2603: BaseItemCode: T1630: The following scan group codes are already
        used as an item number: T1630'
    - - :warning
      - 'Line 2666: BaseItemCode: 106: The following scan group codes are already
        used as an item number: 106, 106'
    - - :warning
      - 'Line 2667: BaseItemCode: 391: The following scan group codes are already
        used as an item number: 391, 391'
    - - :warning
      - 'Line 2680: BaseItemCode: DR12W: The following scan group codes are already
        used as an item number: DR12W'
    - - :warning
      - 'Line 2710: BaseItemCode: DR18W: The following scan group codes are already
        used as an item number: DR18W'
    - - :warning
      - 'Line 2733: BaseItemCode: DR24W: The following scan group codes are already
        used as an item number: DR24W'
    - - :warning
      - 'Line 2735: BaseItemCode: DR3AG: The following scan group codes are already
        used as an item number: DR3AG'
    - - :warning
      - 'Line 2736: BaseItemCode: DR3AN: The following scan group codes are already
        used as an item number: DR3AN'
    - - :warning
      - 'Line 2737: BaseItemCode: DR3BN: The following scan group codes are already
        used as an item number: DR3BN'
    - - :warning
      - 'Line 2738: BaseItemCode: DR3BNK: The following scan group codes are already
        used as an item number: DR3BN'
    - - :warning
      - 'Line 2740: BaseItemCode: DR3FB: The following scan group codes are already
        used as an item number: DR3FB'
    - - :warning
      - 'Line 2741: BaseItemCode: DR3PB: The following scan group codes are already
        used as an item number: DR3PB'
    - - :warning
      - 'Line 2742: BaseItemCode: DR3RI: The following scan group codes are already
        used as an item number: DR3RI'
    - - :warning
      - 'Line 2743: BaseItemCode: DR3SB: The following scan group codes are already
        used as an item number: DR3SB'
    - - :warning
      - 'Line 2744: BaseItemCode: DR3W: The following scan group codes are already
        used as an item number: DR3W'
    - - :warning
      - 'Line 2760: BaseItemCode: DR36W: The following scan group codes are already
        used as an item number: DR36W'
    - - :warning
      - 'Line 2768: BaseItemCode: DR3CH: The following scan group codes are already
        used as an item number: DR3CH'
    - - :warning
      - 'Line 2769: BaseItemCode: DR4AG: The following scan group codes are already
        used as an item number: DR4AG'
    - - :warning
      - 'Line 2770: BaseItemCode: DR4AGV: The following scan group codes are already
        used as an item number: DR4AG'
    - - :warning
      - 'Line 2772: BaseItemCode: DR4BN: The following scan group codes are already
        used as an item number: DR4BN'
    - - :warning
      - 'Line 2773: BaseItemCode: DR4BNK: The following scan group codes are already
        used as an item number: DR4BN'
    - - :warning
      - 'Line 2774: BaseItemCode: DR4CH: The following scan group codes are already
        used as an item number: DR4CH'
    - - :warning
      - 'Line 2778: BaseItemCode: DR4FB: The following scan group codes are already
        used as an item number: DR4FB'
    - - :warning
      - 'Line 2779: BaseItemCode: DR4SB: The following scan group codes are already
        used as an item number: DR4SB'
    - - :warning
      - 'Line 2780: BaseItemCode: DR4W: The following scan group codes are already
        used as an item number: DR4W'
    - - :warning
      - 'Line 2799: BaseItemCode: DR48W: The following scan group codes are already
        used as an item number: DR48W'
    - - :warning
      - 'Line 2803: BaseItemCode: DR6AG: The following scan group codes are already
        used as an item number: DR6AG'
    - - :warning
      - 'Line 2804: BaseItemCode: DR6W: The following scan group codes are already
        used as an item number: DR6W'
    - - :warning
      - 'Line 2805: BaseItemCode: DR6AGV: The following scan group codes are already
        used as an item number: DR6AG'
    - - :warning
      - 'Line 2806: BaseItemCode: DR6AN: The following scan group codes are already
        used as an item number: DR6AN'
    - - :warning
      - 'Line 2808: BaseItemCode: DR6BR: The following scan group codes are already
        used as an item number: DR6BR'
    - - :warning
      - 'Line 2809: BaseItemCode: DR6CH: The following scan group codes are already
        used as an item number: DR6CH'
    - - :warning
      - 'Line 2812: BaseItemCode: DR6FB: The following scan group codes are already
        used as an item number: DR6FB'
    - - :warning
      - 'Line 2816: BaseItemCode: DR6OB: The following scan group codes are already
        used as an item number: DR6OB'
    - - :warning
      - 'Line 2817: BaseItemCode: DR6PR: The following scan group codes are already
        used as an item number: DR6PR'
    - - :warning
      - 'Line 2818: BaseItemCode: DR6SB: The following scan group codes are already
        used as an item number: DR6SB'
    - - :warning
      - 'Line 2819: BaseItemCode: DR6TI: The following scan group codes are already
        used as an item number: DR6TI'
    - - :warning
      - 'Line 2836: BaseItemCode: DR60W: The following scan group codes are already
        used as an item number: DR60W'
    - - :warning
      - 'Line 2849: BaseItemCode: DR72W: The following scan group codes are already
        used as an item number: DR72W'
    - - :warning
      - 'Line 2856: BaseItemCode RH787-WIFI listed more than once. Only last record
        updated.'
    - - :warning
      - 'Line 2856: BaseItemCode: RH787-WIFI: The following scan group codes are already
        used as an item number: RH787-WIFI'
    - - :warning
      - 'Line 2857: BaseItemCode RH787-WIFI-CCT listed more than once. Only last record
        updated.'
    - - :warning
      - 'Line 2857: BaseItemCode: RH787-WIFI-CCT: The following scan group codes are
        already used as an item number: RH787-WIFI'
    - - :warning
      - 'Line 2858: BaseItemCode RH790-WIFI listed more than once. Only last record
        updated.'
    - - :warning
      - 'Line 2858: BaseItemCode: RH790-WIFI: The following scan group codes are already
        used as an item number: RH790-WIFI'
    - - :warning
      - 'Line 2864: BaseItemCode: IDC-2000: The following scan group codes are already
        used as an item number: IDC-2000'
    - - :warning
      - 'Line 2866: BaseItemCode: 635A: The following scan group codes are already
        used as an item number: 635A'
    - - :warning
      - 'Line 2867: BaseItemCode: 635WF: The following scan group codes are already
        used as an item number: 635WF'
    - - :warning
      - 'Line 2891: BaseItemCode: OLK215-LED: The following scan group codes are already
        used as an item number: OLK215-LED'
    - - :warning
      - 'Line 2892: BaseItemCode: C3-BB: The following scan group codes are already
        used as an item number: C3-BB'
    - - :warning
      - 'Line 2893: BaseItemCode: C3-WW: The following scan group codes are already
        used as an item number: C3-WW'
    - - :warning
      - 'Line 2894: BaseItemCode: C6-CH: The following scan group codes are already
        used as an item number: C6-CH'
    - - :warning
      - 'Line 2895: BaseItemCode: C6-WW: The following scan group codes are already
        used as an item number: C6-WW'
    - - :warning
      - 'Line 2899: BaseItemCode: CM-6SDC: The following scan group codes are already
        used as an item number: CM-6SDC, CM-6SDC'
    - - :warning
      - 'Line 2900: BaseItemCode: CM-6W: The following scan group codes are already
        used as an item number: CM-6W'
    - - :warning
      - 'Line 2903: BaseItemCode: CM-8W: The following scan group codes are already
        used as an item number: CM-8W'
    - - :warning
      - 'Line 2909: BaseItemCode RH787-WIFI listed more than once. Only last record
        updated.'
    - - :warning
      - 'Line 2909: BaseItemCode: RH787-WIFI: The following scan group codes are already
        used as an item number: RH787-WIFI'
    - - :warning
      - 'Line 2910: BaseItemCode RH787-WIFI-CCT listed more than once. Only last record
        updated.'
    - - :warning
      - 'Line 2910: BaseItemCode: RH787-WIFI-CCT: The following scan group codes are
        already used as an item number: RH787-WIFI-CCT'
    - - :warning
      - 'Line 2911: BaseItemCode RH790-WIFI listed more than once. Only last record
        updated.'
    - - :warning
      - 'Line 2911: BaseItemCode: RH790-WIFI: The following scan group codes are already
        used as an item number: RH790-WIFI'
    - - :warning
      - 'Line 2921: BaseItemCode: PH-2W: The following scan group codes are already
        used as an item number: PH-2W'
    - - :warning
      - 'Line 2952: BaseItemCode: ICS-WALL: The following scan group codes are already
        used as an item number: ICS-WALL'
    - - :information
      - 'The following items were missing category codes and asssigned to ''Other''
        category: 62194-SB, ZA5902-TB, ZA5902-TW, ZA5912-TB, ZA5912-TW, ZA6102-TB,
        ZA6102-TW, ZA6112-TB, ZA6112-TW, RH787-WIFI, RH787-WIFI-CCT, RH790-WIFI'
 |
| 2026-06-17 17:40:40 | ---
- - Products
  - - - :warning
      - 'Line 1: Field name i.qty_available is unknown.'
    - - :warning
      - 'Line 23: ImageFileName:  is not valid and will not be imported'
    - - :warning
      - 'Line 272: BaseItemCode: 86226FB-T: The following scan group codes are already
        used as an item number: 86226'
    - - :warning
      - 'Line 366: ImageFileName:  is not valid and will not be imported'
    - - :warning
      - 'Line 582: field materials truncated to 50 characters, BaseItemCode=SOF42BNK3'
    - - :warning
      - 'Line 583: field materials truncated to 50 characters, BaseItemCode=SOF42SB3'
    - - :warning
      - 'Line 589: field materials truncated to 50 characters, BaseItemCode=WHL42BNK5C1'
    - - :warning
      - 'Line 590: field materials truncated to 50 characters, BaseItemCode=WHL42FB5C1'
    - - :warning
      - 'Line 591: field materials truncated to 50 characters, BaseItemCode=WHL42W5C1'
    - - :warning
      - 'Line 592: field materials truncated to 50 characters, BaseItemCode=WHL42BNK5C3'
    - - :warning
      - 'Line 593: field materials truncated to 50 characters, BaseItemCode=WHL42FB5C3'
    - - :warning
      - 'Line 594: field materials truncated to 50 characters, BaseItemCode=WHL42W5C3'
    - - :warning
      - 'Line 595: field materials truncated to 50 characters, BaseItemCode=WHL52BNK5C1'
    - - :warning
      - 'Line 596: field materials truncated to 50 characters, BaseItemCode=WHL52FB5C1'
    - - :warning
      - 'Line 597: field materials truncated to 50 characters, BaseItemCode=WHL52W5C1'
    - - :warning
      - 'Line 598: field materials truncated to 50 characters, BaseItemCode=WHL52BNK5C3'
    - - :warning
      - 'Line 599: field materials truncated to 50 characters, BaseItemCode=WHL52FB5C3'
    - - :warning
      - 'Line 600: field materials truncated to 50 characters, BaseItemCode=WHL52W5C3'
    - - :warning
      - 'Line 674: Related item: ''N/A'' not found, BaseItemCode=WCFL-1000'
    - - :warning
      - 'Line 674: BaseItemCode: WCFL-1000: The following scan group codes are already
        used as an item number: WCFL-1000'
    - - :warning
      - 'Line 687: BaseItemCode CLZ72FB6 listed more than once. Only last record updated.'
    - - :warning
      - 'Line 688: BaseItemCode CLZ72FB6 listed more than once. Only last record updated.'
    - - :warning
      - 'Line 716: 6 image limit exceeded, image(s) (CM-7W-LED.jpg) not imported.,
        BaseItemCode=MCY52BNK3'
    - - :warning
      - 'Line 970: field materials truncated to 50 characters, BaseItemCode=CHS52PLN5'
    - - :warning
      - 'Line 971: field materials truncated to 50 characters, BaseItemCode=CHS52SB5-NWF'
    - - :warning
      - 'Line 1153: BaseItemCode: 86263: The following scan group codes are already
        used as an item number: 86263'
    - - :warning
      - 'Line 1154: BaseItemCode: 86265: The following scan group codes are already
        used as an item number: 86265'
    - - :warning
      - 'Line 1155: BaseItemCode: 86266: The following scan group codes are already
        used as an item number: 86266'
    - - :warning
      - 'Line 1156: BaseItemCode: 86267: The following scan group codes are already
        used as an item number: 86267'
    - - :warning
      - 'Line 1157: BaseItemCode: 86268: The following scan group codes are already
        used as an item number: 86268'
    - - :warning
      - 'Line 1195: BaseItemCode: 9700: The following scan group codes are already
        used as an item number: 9700'
    - - :warning
      - 'Line 1196: BaseItemCode: CMAWF-ABZ: The following scan group codes are already
        used as an item number: CMAWF-ABZ'
    - - :warning
      - 'Line 1197: BaseItemCode: CMAWF-AN: The following scan group codes are already
        used as an item number: CMAWF-AN'
    - - :warning
      - 'Line 1198: BaseItemCode: CMAWF-BN: The following scan group codes are already
        used as an item number: CMAWF-BN'
    - - :warning
      - 'Line 1199: BaseItemCode: CMAWF-BNK: The following scan group codes are already
        used as an item number: CMAWF-BNK'
    - - :warning
      - 'Line 1200: BaseItemCode: CMAWF-ESP: The following scan group codes are already
        used as an item number: CMAWF-ESP'
    - - :warning
      - 'Line 1201: BaseItemCode: CMAWF-FB: The following scan group codes are already
        used as an item number: CMAWF-FB'
    - - :warning
      - 'Line 1202: BaseItemCode: CMAWF-PN: The following scan group codes are already
        used as an item number: CMAWF-PN'
    - - :warning
      - 'Line 1203: BaseItemCode: CMAWF-SB: The following scan group codes are already
        used as an item number: CMAWF-SB'
    - - :warning
      - 'Line 1204: BaseItemCode: CMAWF-W: The following scan group codes are already
        used as an item number: CMAWF-W'
    - - :warning
      - 'Line 1215: field materials truncated to 50 characters, BaseItemCode=SON52SB3-CAP-NWF'
    - - :warning
      - 'Line 1264: BaseItemCode: WUCI-1000: The following scan group codes are already
        used as an item number: WUCI-1000'
    - - :warning
      - 'Line 1337: 6 image limit exceeded, image(s) (WIDC-Remote.jpg) not imported.,
        BaseItemCode=JOU64BNK3'
    - - :warning
      - 'Line 2498: BaseItemCode: 86201: The following scan group codes are already
        used as an item number: 86201'
    - - :warning
      - 'Line 2499: BaseItemCode: 86202: The following scan group codes are already
        used as an item number: 86202'
    - - :warning
      - 'Line 2500: BaseItemCode: 86203: The following scan group codes are already
        used as an item number: 86203'
    - - :warning
      - 'Line 2501: BaseItemCode: 86216: The following scan group codes are already
        used as an item number: 86216'
    - - :warning
      - 'Line 2502: BaseItemCode: 86222: The following scan group codes are already
        used as an item number: 86222'
    - - :warning
      - 'Line 2503: BaseItemCode: 86224: The following scan group codes are already
        used as an item number: 86224'
    - - :warning
      - 'Line 2504: BaseItemCode: 86226: The following scan group codes are already
        used as an item number: 86226'
    - - :warning
      - 'Line 2505: BaseItemCode: 86233: The following scan group codes are already
        used as an item number: 86233'
    - - :warning
      - 'Line 2506: BaseItemCode: 86237: The following scan group codes are already
        used as an item number: 86237'
    - - :warning
      - 'Line 2507: BaseItemCode: 86243: The following scan group codes are already
        used as an item number: 86243'
    - - :warning
      - 'Line 2508: BaseItemCode: 86248: The following scan group codes are already
        used as an item number: 86248'
    - - :warning
      - 'Line 2509: BaseItemCode: 86249: The following scan group codes are already
        used as an item number: 86249'
    - - :warning
      - 'Line 2510: BaseItemCode: 86251: The following scan group codes are already
        used as an item number: 86251'
    - - :warning
      - 'Line 2511: BaseItemCode: 86252: The following scan group codes are already
        used as an item number: 86252'
    - - :warning
      - 'Line 2512: BaseItemCode: 86253: The following scan group codes are already
        used as an item number: 86253'
    - - :warning
      - 'Line 2513: BaseItemCode: 86254: The following scan group codes are already
        used as an item number: 86254'
    - - :warning
      - 'Line 2514: BaseItemCode: 86255: The following scan group codes are already
        used as an item number: 86255'
    - - :warning
      - 'Line 2515: BaseItemCode: 86258: The following scan group codes are already
        used as an item number: 86258'
    - - :warning
      - 'Line 2516: BaseItemCode: 86244: The following scan group codes are already
        used as an item number: 86244'
    - - :warning
      - 'Line 2601: BaseItemCode: T1610: The following scan group codes are already
        used as an item number: T1610'
    - - :warning
      - 'Line 2602: BaseItemCode: T1615: The following scan group codes are already
        used as an item number: T1615'
    - - :warning
      - 'Line 2603: BaseItemCode: T1630: The following scan group codes are already
        used as an item number: T1630'
    - - :warning
      - 'Line 2666: BaseItemCode: 106: The following scan group codes are already
        used as an item number: 106, 106'
    - - :warning
      - 'Line 2667: BaseItemCode: 391: The following scan group codes are already
        used as an item number: 391, 391'
    - - :warning
      - 'Line 2680: BaseItemCode: DR12W: The following scan group codes are already
        used as an item number: DR12W'
    - - :warning
      - 'Line 2710: BaseItemCode: DR18W: The following scan group codes are already
        used as an item number: DR18W'
    - - :warning
      - 'Line 2733: BaseItemCode: DR24W: The following scan group codes are already
        used as an item number: DR24W'
    - - :warning
      - 'Line 2735: BaseItemCode: DR3AG: The following scan group codes are already
        used as an item number: DR3AG'
    - - :warning
      - 'Line 2736: BaseItemCode: DR3AN: The following scan group codes are already
        used as an item number: DR3AN'
    - - :warning
      - 'Line 2737: BaseItemCode: DR3BN: The following scan group codes are already
        used as an item number: DR3BN'
    - - :warning
      - 'Line 2738: BaseItemCode: DR3BNK: The following scan group codes are already
        used as an item number: DR3BN'
    - - :warning
      - 'Line 2740: BaseItemCode: DR3FB: The following scan group codes are already
        used as an item number: DR3FB'
    - - :warning
      - 'Line 2741: BaseItemCode: DR3PB: The following scan group codes are already
        used as an item number: DR3PB'
    - - :warning
      - 'Line 2742: BaseItemCode: DR3RI: The following scan group codes are already
        used as an item number: DR3RI'
    - - :warning
      - 'Line 2743: BaseItemCode: DR3SB: The following scan group codes are already
        used as an item number: DR3SB'
    - - :warning
      - 'Line 2744: BaseItemCode: DR3W: The following scan group codes are already
        used as an item number: DR3W'
    - - :warning
      - 'Line 2760: BaseItemCode: DR36W: The following scan group codes are already
        used as an item number: DR36W'
    - - :warning
      - 'Line 2768: BaseItemCode: DR3CH: The following scan group codes are already
        used as an item number: DR3CH'
    - - :warning
      - 'Line 2769: BaseItemCode: DR4AG: The following scan group codes are already
        used as an item number: DR4AG'
    - - :warning
      - 'Line 2770: BaseItemCode: DR4AGV: The following scan group codes are already
        used as an item number: DR4AG'
    - - :warning
      - 'Line 2772: BaseItemCode: DR4BN: The following scan group codes are already
        used as an item number: DR4BN'
    - - :warning
      - 'Line 2773: BaseItemCode: DR4BNK: The following scan group codes are already
        used as an item number: DR4BN'
    - - :warning
      - 'Line 2774: BaseItemCode: DR4CH: The following scan group codes are already
        used as an item number: DR4CH'
    - - :warning
      - 'Line 2778: BaseItemCode: DR4FB: The following scan group codes are already
        used as an item number: DR4FB'
    - - :warning
      - 'Line 2779: BaseItemCode: DR4SB: The following scan group codes are already
        used as an item number: DR4SB'
    - - :warning
      - 'Line 2780: BaseItemCode: DR4W: The following scan group codes are already
        used as an item number: DR4W'
    - - :warning
      - 'Line 2799: BaseItemCode: DR48W: The following scan group codes are already
        used as an item number: DR48W'
    - - :warning
      - 'Line 2803: BaseItemCode: DR6AG: The following scan group codes are already
        used as an item number: DR6AG'
    - - :warning
      - 'Line 2804: BaseItemCode: DR6W: The following scan group codes are already
        used as an item number: DR6W'
    - - :warning
      - 'Line 2805: BaseItemCode: DR6AGV: The following scan group codes are already
        used as an item number: DR6AG'
    - - :warning
      - 'Line 2806: BaseItemCode: DR6AN: The following scan group codes are already
        used as an item number: DR6AN'
    - - :warning
      - 'Line 2808: BaseItemCode: DR6BR: The following scan group codes are already
        used as an item number: DR6BR'
    - - :warning
      - 'Line 2809: BaseItemCode: DR6CH: The following scan group codes are already
        used as an item number: DR6CH'
    - - :warning
      - 'Line 2812: BaseItemCode: DR6FB: The following scan group codes are already
        used as an item number: DR6FB'
    - - :warning
      - 'Line 2816: BaseItemCode: DR6OB: The following scan group codes are already
        used as an item number: DR6OB'
    - - :warning
      - 'Line 2817: BaseItemCode: DR6PR: The following scan group codes are already
        used as an item number: DR6PR'
    - - :warning
      - 'Line 2818: BaseItemCode: DR6SB: The following scan group codes are already
        used as an item number: DR6SB'
    - - :warning
      - 'Line 2819: BaseItemCode: DR6TI: The following scan group codes are already
        used as an item number: DR6TI'
    - - :warning
      - 'Line 2836: BaseItemCode: DR60W: The following scan group codes are already
        used as an item number: DR60W'
    - - :warning
      - 'Line 2849: BaseItemCode: DR72W: The following scan group codes are already
        used as an item number: DR72W'
    - - :warning
      - 'Line 2856: BaseItemCode RH787-WIFI listed more than once. Only last record
        updated.'
    - - :warning
      - 'Line 2856: BaseItemCode: RH787-WIFI: The following scan group codes are already
        used as an item number: RH787-WIFI'
    - - :warning
      - 'Line 2857: BaseItemCode RH787-WIFI-CCT listed more than once. Only last record
        updated.'
    - - :warning
      - 'Line 2857: BaseItemCode: RH787-WIFI-CCT: The following scan group codes are
        already used as an item number: RH787-WIFI'
    - - :warning
      - 'Line 2858: BaseItemCode RH790-WIFI listed more than once. Only last record
        updated.'
    - - :warning
      - 'Line 2858: BaseItemCode: RH790-WIFI: The following scan group codes are already
        used as an item number: RH790-WIFI'
    - - :warning
      - 'Line 2864: BaseItemCode: IDC-2000: The following scan group codes are already
        used as an item number: IDC-2000'
    - - :warning
      - 'Line 2866: BaseItemCode: 635A: The following scan group codes are already
        used as an item number: 635A'
    - - :warning
      - 'Line 2867: BaseItemCode: 635WF: The following scan group codes are already
        used as an item number: 635WF'
    - - :warning
      - 'Line 2891: BaseItemCode: OLK215-LED: The following scan group codes are already
        used as an item number: OLK215-LED'
    - - :warning
      - 'Line 2892: BaseItemCode: C3-BB: The following scan group codes are already
        used as an item number: C3-BB'
    - - :warning
      - 'Line 2893: BaseItemCode: C3-WW: The following scan group codes are already
        used as an item number: C3-WW'
    - - :warning
      - 'Line 2894: BaseItemCode: C6-CH: The following scan group codes are already
        used as an item number: C6-CH'
    - - :warning
      - 'Line 2895: BaseItemCode: C6-WW: The following scan group codes are already
        used as an item number: C6-WW'
    - - :warning
      - 'Line 2899: BaseItemCode: CM-6SDC: The following scan group codes are already
        used as an item number: CM-6SDC, CM-6SDC'
    - - :warning
      - 'Line 2900: BaseItemCode: CM-6W: The following scan group codes are already
        used as an item number: CM-6W'
    - - :warning
      - 'Line 2903: BaseItemCode: CM-8W: The following scan group codes are already
        used as an item number: CM-8W'
    - - :warning
      - 'Line 2909: BaseItemCode RH787-WIFI listed more than once. Only last record
        updated.'
    - - :warning
      - 'Line 2909: BaseItemCode: RH787-WIFI: The following scan group codes are already
        used as an item number: RH787-WIFI'
    - - :warning
      - 'Line 2910: BaseItemCode RH787-WIFI-CCT listed more than once. Only last record
        updated.'
    - - :warning
      - 'Line 2910: BaseItemCode: RH787-WIFI-CCT: The following scan group codes are
        already used as an item number: RH787-WIFI-CCT'
    - - :warning
      - 'Line 2911: BaseItemCode RH790-WIFI listed more than once. Only last record
        updated.'
    - - :warning
      - 'Line 2911: BaseItemCode: RH790-WIFI: The following scan group codes are already
        used as an item number: RH790-WIFI'
    - - :warning
      - 'Line 2921: BaseItemCode: PH-2W: The following scan group codes are already
        used as an item number: PH-2W'
    - - :warning
      - 'Line 2952: BaseItemCode: ICS-WALL: The following scan group codes are already
        used as an item number: ICS-WALL'
    - - :information
      - 'The following items were missing category codes and asssigned to ''Other''
        category: 62194-SB, ZA5902-TB, ZA5902-TW, ZA5912-TB, ZA5912-TW, ZA6102-TB,
        ZA6102-TW, ZA6112-TB, ZA6112-TW, RH787-WIFI, RH787-WIFI-CCT, RH790-WIFI'
 |
| 2026-06-17 17:22:19 | ---
- - Inventory
  - []
 |
| 2026-06-17 16:21:23 | ---
- - Inventory
  - []
 |
| 2026-06-17 15:22:22 | ---
- - Inventory
  - []
 |
| 2026-06-17 15:06:34 | ---
- - Portal Orders
  - []
 |

### Q-10_results.md

# Q-10 Results — Craftmade (clli, org_id=149)
- **Query**: Q-10 — Feature Enablement Gap Analysis
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| enable_sales_portal | enable_online_catalog | enable_online_ordering | kit_item_count | contract_price_count | enrollment_count | smart_stack_count | shared_resource_count | portal_order_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 0 | 1,495 | 40 | 165 | 696,123 |

### Q-11_results.md

# Q-11 Results — Craftmade (clli, org_id=149)
- **Query**: Q-11 — Configuration Completeness
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 12
- **Run date**: 2026-06-17


| entity_type | last_updated | days_stale | related_record_count |
| --- | --- | --- | --- |
| sales_quotas | 2025-08-20 19:47:14 | 301 | 0 |
| customer_payment_informations | 2025-08-20 19:47:14 | 301 | — |
| riser_prices | 2025-08-20 19:47:14 | 301 | — |
| placement_reports | 2025-08-20 19:47:14 | 301 | — |
| commitment_reports | 2025-08-20 19:47:14 | 301 | — |
| options | 2025-08-20 19:47:14 | 301 | — |
| option_groups | 2025-08-20 19:47:14 | 301 | — |
| matrix_options | 2025-08-20 19:47:14 | 301 | — |
| kit_items | 2025-08-20 19:47:14 | 301 | 0 |
| contract_prices | 2025-08-20 19:47:14 | 301 | 0 |
| customer_favorites | 2025-08-20 19:47:14 | 301 | — |
| price_levels | 2026-01-12 00:22:08 | 156 | — |

### Q-22_results.md

# Q-22 Results — Craftmade (clli, org_id=149)
- **Query**: Q-22 — Feature Usage Depth
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | submit_order | select_a_customer | search_for_customer | email_item_info | create_pdf_catalog | view_library_entry | view_smartpicks | access_sales_portal | filter_products | search_products | search_collections | order_configured_item | view_kit | order_kit | share_my_list | export_data_to_csv | export_data_to_excel | total_events | total_users |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clli | Craftmade | 371 | 3,607 | 3,350 | 392 | 1,298 | 16,039 | 77 | 2,777 | 930 | 31,394 | 102 | 0 | 0 | 0 | 25 | 1 | 1 | 113,726 | 91 |

### Q-CI-02_results.md

# Q-CI-02 Results — Craftmade (clli, org_id=149)
- **Query**: Q-CI-02 — Peer Comparison
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | peer_standing | orders_vs_peer_pct | logins_vs_peer_pct | mrr_vs_peer_pct | peer_orders_median | peer_logins_median | peer_mrr_median |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clli | Craftmade | Commerce-Active | On Track | 46.10 | 262.40 | 195.10 | 254 | 2,833 | 920 |

### Q-CI-03_results.md

# Q-CI-03 Results — Craftmade (clli, org_id=149)
- **Query**: Q-CI-03 — Feature Adoption Benchmarking
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| org_shortname | org_name | segment | feature_depth | has_clicky_portal | arr |
| --- | --- | --- | --- | --- | --- |
| clli | Craftmade | Commerce-Active | 6 | 1 | 26,065 |

### Q-CI-03_benchmarks_results.md

# Q-CI-03-bench Results — Craftmade (clli, org_id=149)
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
