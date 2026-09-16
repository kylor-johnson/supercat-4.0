# Section 8 Context Bundle — Hubbardton Forge (hfg)
Run date: 2026-06-16

## Gate Flags

# Gate Flags — Hubbardton Forge (hfg, org_id=165)
- **Run date**: 2026-06-16
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=22104, portal_order_gmv=$42.2M |
| HAS_INVENTORY | False | inventory_count=0 |
| HAS_SALES_DATA | True | sales_data_count=44934 |
| HAS_SALES_SECTION | True | qualifying_reps=17 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | hubbardton_forge_hfg_eol_portal |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$42.2M > ecat_gmv=$16.8M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 17 | 17 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 137 rows |
| SHOWROOM_EXCLUSIONS | 1 | 1 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 1871, Mixpanel total submit_order (Q-01): 3113 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=86.1%, ambiguous_rate=88.1%, showroom_event_share=3.5% |
| USER_GROUP_JOIN_RATE | 86% | 118 of 137 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 3% | showroom+admin share of matched events: 3.5% |
| ADMIN_REPS_IN_LEADERBOARD | True | 2 admin/showroom users in leaderboard: Shannon Rose, Retha Boles |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=47 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=2590 |
| INVENTORY_FRESH | False | inventories last_updated 300d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=57 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Hubbardton Forge
- **Shortname**: hfg
- **Org ID**: 165
- **Bundle**: 7
- **Bundle label for report**: 7

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Hubbardton Forge (hfg, org_id=165)
- **Run date**: 2026-06-16

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | True |
| PORTAL_CUSTOMER_DATA_PRESENT | True |
| PORTAL_ORDERS_FRESH | True |
| HAS_PORTAL_ORDERS | True |
| HAS_INVENTORY | False |
| HAS_SALES_DATA | True |
| INVENTORY_FRESH | False |
| SALES_DATA_FRESH | False |
| CUSTOMER_DATA_FRESH | True |

## Computed Tiers

| Section | Tier | Determining Condition |
| --- | --- | --- |
| §2 Sales Team | FULL | See Derived Gate 6 §2 formula |
| §3 Customer | FULL | See Derived Gate 6 §3 formula |
| §4 Product | STRONG | See Derived Gate 6 §4 formula |
| §5 Commerce | FULL | See Derived Gate 6 §5 formula |

## Section Guide — section_08_platform.md

# Section Guide: §8 — Platform & Feature Utilization
> **v2.0** — hardened 2026-06-16. Previous: v1.0 (unversioned, validated 2026-04-17).

## Section Identity
- **id**: `platform`
- **title**: Platform & Feature Utilization
- **section number**: 8
- **include when**: Always
- **skip when**: Never — this section is always rendered

## Query Inputs

Read these cache files:
- `cache/Q-07_results.md` — Catalog completeness (shared with §4)
- `cache/Q-08_results.md` — Data freshness per entity type
- `cache/Q-09_results.md` — Import pipeline health
- `cache/Q-10_results.md` — Catalog health
- `cache/Q-11_results.md` — Configuration completeness / alerts
- `cache/Q-22_results.md` — Feature usage depth
- `cache/Q-46_results.md` — **conditional**: eCat selling workflow maturity (submit-through rate). Only present when Mixpanel coverage exists. If absent, omit workflow maturity context from §8.2 — do not mention the metric or leave a placeholder.
- `cache/Q-47_results.md` — **conditional**: Smart stack effectiveness (per-stack metadata, staleness). If absent, build §8.6 from Q-10 smart stack count only.
- `cache/Q-50_results.md` — **conditional**: Library / document engagement (document inventory, staleness). If absent, omit library analysis from §8.1 — do not mention documents or leave a placeholder.
- `cache/gate_flags.md` — for org identity, feature flags, `MIXPANEL_ORDER_TRACKING_GAP`, and `USER_GROUP_SPLIT_AVAILABLE`
- `cache/user_group_mapping.md` — **conditional read**: only if `USER_GROUP_SPLIT_AVAILABLE = true` in `gate_flags.md`. Contains the aggregate activity split between field reps and showroom/operational accounts.

**Mixpanel Order-Tracking Gap**: If `MIXPANEL_ORDER_TRACKING_GAP = true` in `gate_flags.md`, Mixpanel is not tracking iPad order submissions for this org. Apply all of the following:

1. **Remove the "Order Submission" row** from the Q-22 Feature Usage table entirely. Do not display "0" — the zero is a tracking artifact, not a usage signal.
2. **Do not write narrative** that frames order submission as absent, missing, unused, or a gap. This includes Feature Usage Intensity prose, `what-this-means` blocks, and the `section-sub` stat line.
3. **Do not characterize the platform** as non-transactional or presentation-only when the gap flag is set. If historical Postgres orders exist, ordering activity has occurred — Mixpanel instrumentation was not active for that workflow.
4. **Neutral replacement** (only if the section would otherwise reference order submission): "Order submission tracking is handled outside the behavioral analytics layer for this organization. Postgres order data is the authoritative source for ordering activity."
5. **Feature intensity notes** in cache commentary (`Q-22_results.md`): Do not classify "Order Submission" under "Zero activity" when the gap flag is set. Omit it from the intensity summary entirely.

Do not call out the tracking gap by name — just omit the misleading metric and avoid contradicting Postgres order data.

When `MIXPANEL_ORDER_TRACKING_GAP = false` or absent from `gate_flags.md`, render Q-22 normally with no changes.

## Quality Floor

Every subsection **must** contain all of the following:

1. A **`.prose` analytical paragraph** (2–4 sentences minimum) that interprets the data — not just restates numbers. Speak as a smart analyst to a VP: compare counts to context, call out anomalies, frame what the numbers mean for platform health.
2. A **`.metrics-grid`** with `metric-card` elements for headline numbers (include `.metric-note` with time qualifier per Hard Rule #7).
3. A **`<div class="what-this-means">`** closing block (1–3 sentences, actionable implication). Do not duplicate the prose paragraph — the what-this-means block tells the client *what to do about it* or *why it matters strategically*, not what the numbers are.

If a subsection has a table, the `.prose` paragraph must appear **above** the table and interpret highlights — do not let the table speak for itself.

Where a notable pattern exists (feature dominance, stale data cluster, configuration drift), add a **`.callout.insight`** block with a descriptive `.callout-title` and 1–2 sentences of context.

## Rendering Model: Health-Check Card

This section renders as a **single dense health-check card** rather than 6 independent subsections. The goal is VP-level readability: "Is there a problem, and how do I fix it?" — not a sysadmin dashboard.

**This section owns the operational catalog completeness recommendation.** §4 Product references catalog completeness for its sales performance framing but defers operational "upload X images" actions here.

### Card Structure

The section body contains ONE subsection with this layout:

1. **Status row** — a `.metrics-grid` with 3–5 status indicators using traffic-light badge semantics
2. **Alerts block** — configuration issues or stale data requiring action (if any)
3. **Feature opportunity** — one underutilized feature worth highlighting (if any)
4. **Detailed data** — full tables in a collapsed `<details>` for readers who want depth

### 1. Status Indicators (metrics grid)

Build from Q-07, Q-08, Q-09, Q-10 cache files. Produce a `.metrics-grid` with these cards:

| Indicator | Source | Badge logic |
|-----------|--------|-------------|
| Core Pipeline | Q-09 avg monthly imports | `.badge.ok` "Healthy" if ≥50/mo avg; `.badge.warn` "Low Volume" if <50/mo; `.badge.danger` "Stalled" if <10/mo or recent month = 0 |
| Data Freshness | Q-08 entity counts | `.badge.ok` if 0 Stale entities; `.badge.warn` if 1–3 Stale; `.badge.danger` if >3 Stale |
| Catalog | Q-07 completeness % | `.badge.ok` if ≥95%; `.badge.warn` if 80–94%; `.badge.danger` if <80% |
| Feature Adoption | Q-22 distinct active features | `.badge.ok` if ≥5 active features; `.badge.warn` if 3–4; `.badge.danger` if ≤2 |
| Smart Stacks | Q-10 smart stack count | `.badge.ok` if >0 published; `.badge.muted` "Not configured" if 0. Omit card entirely if org has zero smart stacks. |

Each `.metric-card` shows the status badge as `.metric-val` and a one-line explanation as `.metric-note`.

### 2. Alerts Block (Q-08, Q-11 — conditional)

If Q-08 shows any Stale entities OR Q-11 surfaces configuration drift:

- Render a `.callout.alert` with title "Action Required"
- List each alert as a single line: **Entity/Feature** — issue description — recommended action
- Group related entities (e.g., "Options, Option Groups & Matrix Options" as one line)
- Use the 3-label freshness scale only: Fresh (≤30d) / Monitor (31–180d) / Stale (>180d)
- `portal_orders` entity label rule still applies: use "All-Channel Orders" in all client-facing text

If no alerts, omit this block entirely — do not render an empty "no issues found" callout.

### 3. Feature Opportunity (Q-22, Q-46 conditional — conditional)

If Q-22 reveals an underutilized high-value feature (e.g., SmartPicks minimal vs heavy Product Search activity), render a single `.callout.opportunity`:

- Title: the opportunity (e.g., "SmartPicks Coaching Opportunity")
- Body: 1–2 sentences framing the gap and potential value
- If Q-46 is present, weave submit-through rate context into the opportunity framing (translate band labels into client-friendly language — never use raw band names)

**Platform Activity Composition** (conditional — render ONLY when `USER_GROUP_SPLIT_AVAILABLE = true`):

If the gate is true, read the `Aggregate Split` table from `cache/user_group_mapping.md`. Append a single contextual sentence to the feature opportunity or the prose paragraph:

> "Of tracked platform activity, approximately X% is attributed to field representatives and Y% to showroom and operational accounts."

Rules:
- Use **percentages only** — no absolute event counts for the split
- Combine `showroom` and `admin_internal` buckets into "showroom and operational accounts"
- Round to nearest whole number; do not name individual accounts
- No negative framing ("inflated", "skewed", "misleading")

If `USER_GROUP_SPLIT_AVAILABLE = false` or absent, do nothing — no mention of user groups.

If no notable feature opportunity exists, omit this block.

### 4. Detailed Data (collapsed `<details>`)

Wrap ALL detailed operational data in a single collapsed `<details>` block with summary "View detailed platform data". Inside, include:

**Catalog detail** (Q-07, Q-10, Q-50 conditional):
- Table: Visibility | Products | Missing Images | Missing Price | Complete %
- If Q-50 present: library/document inventory with age context
- If price-level pricing detected (all products missing per-product price), note as valid configuration

**Data freshness detail** (Q-08):
- Table of all entities with freshness labels (`.badge.ok` Fresh / `.badge.warn` Monitor / `.badge.danger` Stale)
- Use human-friendly entity names, not raw snake_case identifiers
- Group stale entities by category if possible (Pricing, Product Config, Sales, Customer)

**Pipeline detail** (Q-09):
- One-line summary: average monthly imports, cadence characterization
- Table: Month | Imports (5 most recent months only). No monthly import count narrative — the status indicator already covers pipeline health.

**Configuration alerts detail** (Q-11 — if present):
- Table: Feature | Status badge | Issue | Action (same columns as before)
- Omit if all entities Fresh and no drift detected

**Smart stack detail** (Q-47 conditional):
- If Q-47 present: table Stack Name | Status | Created | Last Updated (top 5 by recency)
- If Q-47 absent: stack count metric only with cross-reference to Q-22 Collection Search events
- Omit entirely if smart_stacks = 0

### Prose and What-This-Means

- One `.prose` paragraph above the detailed data `<details>`: synthesize the health picture in 2–3 sentences. Lead with what's working, then note what needs attention. Frame for a VP, not a sysadmin.
- One `.what-this-means` block: 1–3 sentences of prioritized action. What is the single most impactful thing the client should do? If everything is healthy, acknowledge the operational discipline.

### Mixpanel Order-Tracking Gap

All rules from the Query Inputs section still apply. If `MIXPANEL_ORDER_TRACKING_GAP = true`:
- Remove "Order Submission" from any feature adoption assessment
- Do not characterize the platform as non-transactional
- Use neutral replacement language per Query Inputs rules

## DOES NOT COVER (hard boundaries)

This section does NOT produce:
1. Rep-level performance, coaching, or behavioral analysis → belongs in §2 Sales Team Performance
2. Customer-level activation, penetration, or dormancy analysis → belongs in §3 Customer & Buyer Intelligence
3. Product sales analysis, velocity, or new introduction performance → belongs in §4 Product & Inventory
4. Order trends, channel mix, or capture rate analysis → belongs in §5 Commerce Analytics
5. Portal traffic analytics (Clicky) → belongs in §6 Demand Signal Intelligence
6. Peer benchmarking or cohort comparisons → belongs in §7 Peer Benchmarking
7. Health score, churn risk, or expansion signals → internal only (GUARDRAILS.md §5)

Read: `GUARDRAILS.md` for the full query ownership table (§8) and rule set.

---

## Section-Specific Rules

**Data freshness labels** — use ONLY these three. No other labels. No 5-label severity system:
- **Fresh**: last updated ≤30 days ago
- **Monitor**: last updated 31–180 days ago
- **Stale**: last updated >180 days ago

**Feature gaps prohibition**: Do not list CPQ, Online Ordering, or other products as "gaps" if the client doesn't have that product. Only surface utilization data for features the client has access to.

**Entity names in client-facing HTML**: Use human-friendly names (e.g., "Price Levels", "Option Groups", "All-Channel Orders"), not raw identifiers (`price_levels`, `option_groups`, `portal_orders`).

- The `section-sub` one-liner should contain 3–4 key status indicators (e.g., "Pipeline healthy · 2 stale entities · 95% catalog completeness · 5 active features"). Do not dump all metrics into the section headline.
- The `section-contents` middot list uses: "Platform Health Check" (single entry — this section renders as one card, not multiple subsections).

## Shared Rules

# Shared Rules — All Section Agents
> **v1.1** — updated 2026-06-16. Scoped forbidden-phrase canonical claim, confidence footer scope.

> **Note:** This file is a runtime guide consumed by section-building agents. The
> canonical rule definitions live in [`GUARDRAILS.md`](../../../GUARDRAILS.md). If
> this file and `GUARDRAILS.md` conflict, `GUARDRAILS.md` wins.

## A. Semantic Guardrails

| Term | Correct Meaning | Never Use For |
|------|----------------|--------------|
| `orders` | eCat-originated orders only | ERP or total-business data |
| `order_source = 'ipad'` | Rep-submitted iPad orders | Online or self-service orders |
| `order_source = 'server'` | eCat Online / B2B Cart buyer self-service | Rep orders |
| `portal_orders` | ERP-synced all-channel total business | Buyer activity, "portal ordering," self-service |
| `Sales Portal` | Internal BI dashboard for client team | A buyer-facing ordering channel |
| `self-service` | B2B Cart / eCat Online only | Sales Portal, portal_orders |
| Segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) | Internal classification only — never in external output | Every section including Peer Benchmarking — in §7, use plain-language cohort framing derived from `peer_group_id_effective` |
| Health score | Never in Phase 1 external report | Any external output |
| `benchmark_confidence` | Internal rendering signal only — governs section inclusion and phrasing | Never as a visible label in client output |
| `peer_group_level` | Internal gating signal only | Never in client output (not even paraphrased as "tier 1/2/3") |
| `peer_group_n` | Internal calibration signal — governs framing strength | Never as a raw count in client-facing output. Use to calibrate plain-language phrasing only. |

## B. Hard Rules

Invariant. No exception, no workaround, no soft reference:

1. Never surface health score, health band, or health classification in any external output
2. Never surface VM-27, VM-28, VM-29, VM-36, VM-48 content externally
3. If `has_clicky = false`, the Demand Signal Intelligence section does not exist. No placeholder. No mention of Clicky anywhere.
4. `portal_orders` is never buyer activity. Never "portal ordering adoption."
5. Segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) are internal classification terms and must never appear anywhere in the external report — including the Peer Benchmarking section. In §7, describe the peer group using plain-language framing derived from `peer_group_id_effective` (e.g., "Lighting manufacturers on the same platform bundle") — not the raw label or segment classification terms.
6. Executive Summary is always written last
7. Every metric must include a time qualifier (e.g., "trailing 12 months," "last 90 days")
8. Every projection must be hedged with appropriate language ("potential," "estimated," "projected," "roughly," "could," "up to") in client-facing HTML. The literal tags `[HYPOTHETICAL]` and `[ESTIMATED]` are **internal pipeline markers only** — they appear in `cache/` highlight files and priority action candidates so validators and the Stage 4 assembler can track projections, but they must **never appear as visible text in HTML fragments**. If the literal string `[HYPOTHETICAL]` or `[ESTIMATED]` appears in a fragment, it is a rendering defect.
9. Every extrapolation must be hedged with appropriate language in client-facing HTML (same rule as #8 — see above).
10. Do not improvise around missing data — mark as N/A or omit per blueprint rules
11. `benchmark_confidence`, `peer_group_level`, and `peer_group_n` are internal signals only. Never expose these as labels in client-facing HTML — not in prose, callouts, section headers, or footnotes. Use them to calibrate plain-language benchmark framing only.

## C. Forbidden Phrases

> **Runtime copy of the canonical list in GUARDRAILS.md §4.** The post-build check in `qa/eval/check_static.sh` mirrors this list. If you add or remove a forbidden phrase, update GUARDRAILS.md first, then this file and the shell script.

Never in client-facing HTML:

- "health score" / "health scores"
- "portal orders" / "portal ordering" as buyer activity or entity label
- "net-new customers"
- "ERP" in any client-facing text — use "total business," "all-channel sales," "your business system," "your account base"
- "Mixpanel" — use "platform engagement data" or "engagement events"
- "Clicky" — never in delivered HTML
- Segment labels: "Platform-Embedded", "Commerce-Active", "Catalog-Focused"
- Internal identifiers: VM codes, query IDs, table names, column names, org IDs, dataset paths
- "bounce_rate"
- `order_source = 'ipad'` and similar code literals in client-facing prose
- "benchmark_confidence", "peer_group_level", "peer_group_n" as labels
- Literal `[HYPOTHETICAL]` or `[ESTIMATED]` tags — these are internal pipeline markers and must never appear in client-facing HTML

## D. Universal Formatting Rules

- Every metric has a time qualifier (Hard Rule #7)
- Projections use hedging language in HTML; `[HYPOTHETICAL]` tags in cache/highlights only — never in fragments (Hard Rule #8)
- Extrapolations use hedging language in HTML; `[ESTIMATED]` tags in cache/highlights only — never in fragments (Hard Rule #9)
- Dollar formatting: `$X,XXX` or `$X.XM`
- Do not improvise around missing data (Hard Rule #10)
- Every subsection ends with a "What this tells you" close (1–3 sentences, actionable implication)
- One `what-this-means` per subsection. Do not add a second section-level `what-this-means` after the last subsection's close.
- Coaching Opportunities & Selling Archetypes (§2.3) is the one exception to the `what-this-means` rule: coaching cards are self-contained action items and do NOT end with a `what-this-means` block.
- Do not surface operational exclusion methodology, showroom scan details, qualifying threshold explanations, or internal pipeline context in client-facing prose. The `section-sub` one-liner may reference an exclusion count (e.g., "1 showroom excluded") but not the methodology.

## E. Fragment Contract

Every section agent produces an HTML fragment in this exact wrapper:

```html
<details class="section-collapse" id="{{SECTION_ID}}">
  <summary>
    <div>
      <h2 class="section-title"><span class="section-num">§{{N}}</span> {{SECTION_TITLE}}</h2>
      <div class="section-sub">{{KEY_STATS_ONE_LINE}}</div>
      <div class="section-contents">{{SUBSECTION_LIST_MIDDOT_SEPARATED}}</div>
    </div>
    <span class="expand-hint">&#9662; Click to expand</span>
  </summary>
  <section class="section" style="margin-bottom:0;border-top:none;border-radius:0 0 var(--r) var(--r);">
    {{SUBSECTION_CONTENT}}
  </section>
</details>
```

**Section IDs (locked):** `§2=sales`, `§3=customers`, `§4=product`, `§5=commerce`, `§6=portal`, `§7=peer`, `§8=platform`

**Fragment rules:**
- Starts with `<details`, ends with `</details>` — nothing before or after
- No `<html>`, `<head>`, `<body>`, or `<style>` tags
- No HTML comments (`<!-- -->`)
- `section-contents`: every rendered subsection name, separated by ` · ` (`&middot;`) — must reflect ONLY subsections that actually appear in the fragment (not skipped subsections)
- `section-sub`: data-dense one-liner, not a generic description
- Every subsection: `<div class="subsection">` with `<div class="subsection-title">` as first child
- Every subsection ends with `<div class="what-this-means">` (exception: §2.3 Coaching Opportunities & Selling Archetypes — coaching cards are self-contained and omit what-this-means per Section D above)
- **Structural self-check before saving**: count of `what-this-means` divs must equal count of `subsection` divs minus any coaching-card subsections. If you have more `what-this-means` than subsections, you have a duplicate — remove it. If fewer, a subsection is missing its close.

## F. CSS Class Quick-Reference

From `authority/html_report_template.html` (aligned with gold reference `clm_2026-04-14`). Use these class names exactly.

| Class | Renders |
|-------|---------|
| `.subsection` | Subsection container (24px top margin) |
| `.subsection-title` | Bold 15px subsection heading |
| `.what-this-means` | Amber left-bordered panel box for actionable close |
| `.metrics-grid` | Auto-fill responsive grid of metric cards |
| `.metric-card` | Panel-bg rounded card for a single metric |
| `.metric-val` | Bold 24px metric number |
| `.metric-label` | Mono 9px uppercase muted label |
| `.metric-note` | 11px muted annotation; variants `.ok` / `.warn` / `.danger` |
| `.callout` + `.callout-title` | Rounded box with left border accent; 600-weight 13px title |
| `.callout.insight` | Panel bg + amber left border |
| `.callout.alert` | Danger-bg + red left border (use instead of `.callout.warning`) |
| `.callout.opportunity` | Ok-bg + green left border (use instead of `.callout.action`) |
| `.badge` | Inline mono 10px uppercase pill |
| `.badge.ok` / `.badge.warn` / `.badge.danger` / `.badge.info` / `.badge.muted` | Status pills (dot notation — space-separated classes) |
| `.coaching-card` | White card with warn-colored 3px top border |
| `.coaching-header` / `.coaching-name` | Flex header row; bold 15px name |
| `.coaching-body` / `.coaching-action` / `.coaching-impact` | 13px body; medium-weight action; mono green impact pill |
| `.prose` | 13.5px secondary-color paragraph with 16px bottom margin |
| `<details>` (inner) | Panel-bg summary with arrow and click-to-expand pattern |
| `.row-highlight` | Table row with green (`--ok-bg`) emphasis |
| `.section-num` | Mono 11px muted section number prefix (e.g., §2) |
| `.peer-hero` | Panel-bg flex container for hero benchmark stat |
| `.peer-hero-pctile` | 13px mono pill badge; `.above` (green) / `.below` (red) / `.on-par` (muted) |
| `.peer-metric-row` | 3-column grid row for benchmark breakdown |
| `.peer-metric-title` | 12px metric name |
| `.peer-range-bar` / `.peer-range-marker` | 6px bar with positioned dot; `.above` / `.below` / `.on-par` |
| `.quartile-pill` / `.peer-quartile-pill` | 9px mono uppercase pill; `.q4` (green) / `.q3` (blue) / `.q2` (amber) / `.q1` (red) |
| `.priorities` / `.priority` | Grid container; 3-column card (badge / title+desc / impact) |
| `.priority-badge` | Mono 9px urgency pill; `.high` (red) / `.medium` (amber) / `.low` (muted) |
| `.priority-title` / `.priority-desc` / `.priority-impact` | Bold 14px title; 13px desc; mono 11px muted impact |
| `.highlights` | Counter-numbered list (amber-circled counters, light bottom borders) |
| `.top-performer-list` | Container for top-performer behavioral pattern rows (§7.4) |
| `.top-performer-row` | Flex row: icon + text, bottom-bordered |
| `.top-performer-icon` | 26px accent-glow rounded icon cell (use Unicode arrows/symbols) |
| `.top-performer-text` | 13px secondary prose with bold strong elements |
| `.data-confidence` | Info-bg panel at bottom of section body, 12px muted text, info left-border |
| `.data-confidence.limited` | Warn-bg variant with warn left-border (staleness/quality issues) |
| `.data-confidence-label` | Mono 9px uppercase badge prefix (tier label) |
| `.data-confidence-action` | 12px medium-weight text for "what would complete this" line |

## G. Highlight Candidate Format

Each section agent outputs `cache/section_NN_highlights.md` alongside its fragment.

```markdown
# §N Section Title — Highlight Candidates

1. **Bold headline** — one sentence of context with data. [→ §section-id]
2. **Bold headline** — one sentence of context with data. [→ §section-id]

## Priority Action Candidate
- **URGENCY**: Action statement with quantified impact [HYPOTHETICAL]. [→ §section-id]
```

**Note:** `[HYPOTHETICAL]` tags in highlight/priority candidates are correct — these are internal cache files consumed by the Stage 4 assembler, not client-facing HTML. The assembler strips or replaces tags with hedging language when building the Executive Summary.

**Rules:**
- 2–4 highlight candidates per section, ranked by signal strength
- Each: **bold headline**, one sentence of context, section link
- 0–1 priority action candidates per section with urgency level
- Stage 4 assembler selects top 5–6 highlights and 2–4 priority actions from all candidates
- Section agents do not write the Executive Summary — they only propose candidates

**Anti-repetition rule:** Executive summary highlights must NOT be repeated verbatim as section-level introductory callouts. A stat may appear in both the executive summary and a section, but the section must present the underlying data table — the `what-this-means` box must add **new interpretation** beyond what the executive summary already stated. If the `what-this-means` text could be copy-pasted into the executive summary without losing meaning, it is restating, not interpreting. The reader already read the table; the `what-this-means` job is to tell them what it MEANS, not what it SAYS.

## H. Display Limits

- Maximum 15 rows displayed per table. Default visible rows: 5. If showing top 10, show 5 visible + remaining 5 in a collapsed `<details>` element. Section-specific display limits in individual section guides take precedence over these defaults.
- Do not dump all cache file rows into tables. The section guide specifies how many to show per subsection.

## I. Progressive Disclosure — Subsection Collapse

- Subsections marked `[COLLAPSE]` in their section guide are wrapped in an inner `<details>` element within the parent section body (inside the outer `<details class="section-collapse">`).
- Collapsed subsections still appear in the `section-contents` middot list.
- When the user opens the parent section, `[COLLAPSE]` subsections remain closed until individually expanded.

## J. Data Confidence Framework

The Data Confidence Framework provides deterministic, per-section disclosure about what data sources are present, their freshness, and what additional data would make the picture more complete. It is formula-driven — no judgment calls, no improvisation.

### J.1 Tier Definitions

| Tier | Condition | Visual Treatment | Footer Rendered? |
|------|-----------|-----------------|-----------------|
| FULL | All primary + enrichment sources present and fresh (≤30 days) | `.data-confidence` footer | Yes — positive-tone data provenance |
| STRONG | Primary sources present; enrichment source stale (31-180d) or one source missing | `.data-confidence` footer | Yes — with source list |
| PARTIAL | Core eCat data only; ERP context unavailable | `.data-confidence` footer + "what would complete this" | Yes — with action |
| LIMITED | Core data stale (>180d) or known quality issues | `.data-confidence.limited` footer with staleness callout | Yes — with warn styling |

### J.2 Rendering Rules

1. **FULL** — render a `.data-confidence` footer with label `FULL PICTURE` and a positive-tone data sources summary listing what went into the analysis. No "To see X, do Y" action prompt — just a clean statement of what's there. **Position: bottom** of the section (after all subsections).
2. **STRONG / PARTIAL** — render a `.data-confidence` footer with a data sources summary AND an action prompt explaining what additional data would complete the picture. **Position: top** of the section (immediately after the key metrics row, before the first subsection). The reader sees upfront that data is incomplete before investing attention in the analysis.

```html
<div class="data-confidence">
  <span class="data-confidence-label">{{TIER_LABEL}}</span>
  <span class="data-confidence-action">{{TEMPLATE_TEXT}}</span>
</div>
```

All four tiers use this structure. `{{TIER_LABEL}}` is one of: `FULL PICTURE` / `STRONG VIEW` / `PARTIAL VIEW` / `LIMITED VIEW`.

3. **LIMITED** — same structure but with the `.limited` modifier:

```html
<div class="data-confidence limited">
  <span class="data-confidence-label">LIMITED VIEW</span>
  <span class="data-confidence-action">{{TEMPLATE_TEXT}}</span>
</div>
```

4. The confidence footer is part of the section fragment. The assembler pastes it verbatim — it does not modify, strip, or relocate it.
5. Never use "ERP" in any confidence footer text — this is client-facing. Use "your business system," "total business," or "all-channel" per Section C.
6. Confidence tier labels (`FULL PICTURE`, etc.) must not appear anywhere else in the report — they are reserved for this footer.

### J.3 Locked Template Strings

Section builders use these exact strings based on their section ID and tier. Do not paraphrase, shorten, or editorialize.

**§2 Sales Team:**
- `§2-FULL`: "Data sources: eCat iPad orders, platform behavioral analytics ({{MIXPANEL_USER_COUNT}} active users), all-channel order data with rep attribution. Complete data for this section."
- `§2-FULL-NO-ERP`: "Data sources: eCat iPad orders, platform behavioral analytics ({{MIXPANEL_USER_COUNT}} active users). Complete eCat data for this section."
- `§2-PARTIAL`: "Data sources: eCat iPad orders. To see behavioral analytics and selling archetypes, ensure reps are using the eCat iPad app. To see how eCat adoption compares to each rep's total business, sync order data with rep attribution via your business system."
- `§2-STRONG`: "Data sources: eCat iPad orders, platform behavioral analytics. To see how eCat adoption compares to each rep's total business, sync order data with rep attribution via your business system."
- `§2-ADMIN-DISCLOSURE`: "Note: This section includes ordering activity from users assigned to internal or administrative roles in your platform configuration. Their activity reflects real orders but may include test or operational transactions."

The `§2-ADMIN-DISCLOSURE` template is an **additive append** — it is rendered as a second line inside the same `.data-confidence` div when `ADMIN_REPS_IN_LEADERBOARD = true`, regardless of tier. At FULL tier, append the disclosure as a `<br>` line inside the FULL PICTURE footer. At STRONG/PARTIAL, append as a `<br>` line inside the existing footer.

Use `§2-FULL` when `PORTAL_REP_DATA_PRESENT = true`. Use `§2-FULL-NO-ERP` when `PORTAL_REP_DATA_PRESENT = false` (eCat + Mixpanel data present, but no all-channel rep attribution).

**§3 Customer:**
- `§3-FULL`: "Data sources: eCat order history, account records ({{CUSTOMER_COUNT}} accounts), all-channel order data (last synced {{LAST_PORTAL_ORDER_DATE}}). Complete data for this section."
- `§3-PARTIAL`: "Data sources: eCat order history, account records. To see customer-level penetration of your total business and identify high-value unactivated accounts, sync order data via your business system."
- `§3-STRONG`: "Data sources: eCat order history, account records, all-channel order data. Order data was last synced {{LAST_PORTAL_ORDER_DATE}} — refresh for current total-business context."

**§4 Product:**
- `§4-FULL`: "Data sources: Product catalog ({{PRODUCT_COUNT}} items), inventory data, sales history. Complete data for this section."
- `§4-PARTIAL`: "Data sources: Product catalog. To see inventory status and sales performance by category, import inventory and sales history data."
- `§4-STRONG`: "Data sources: Product catalog, {{SOURCES_PRESENT}}. {{STALE_SOURCE}} was last updated {{STALE_DATE}} — refresh for current analysis."

**§5 Commerce:**
- `§5-FULL`: "Data sources: eCat orders, all-channel order data (last synced {{LAST_PORTAL_ORDER_DATE}}). Complete data for this section."
- `§5-PARTIAL`: "Data sources: eCat orders by channel and type. To see eCat's share of your total business and per-customer penetration, sync order data via your business system."
- `§5-STRONG`: "Data sources: eCat orders, all-channel order data. Order data was last synced {{LAST_PORTAL_ORDER_DATE}} — refresh for current context."

### J.4 Template Variable Resolution

- `{{LAST_PORTAL_ORDER_DATE}}` — from the ERP enrichment preflight (`most_recent_erp_order`), formatted as "Month DD, YYYY"
- `{{SOURCES_PRESENT}}` — comma-separated list of present sources (e.g., "inventory data, sales history")
- `{{STALE_SOURCE}}` — the specific source that is stale (e.g., "Inventory data", "Sales history")
- `{{STALE_DATE}}` — from Q-08 data_versions, formatted as "Month DD, YYYY"
- `{{MIXPANEL_USER_COUNT}}` — from `gate_flags.md` evidence for `MIXPANEL_USER_DATA_PRESENT` (the row count from Q-01 Step 1). If unavailable, omit the parenthetical from the FULL template and just say "platform behavioral analytics".
- `{{CUSTOMER_COUNT}}` — from `gate_flags.md` evidence for customer base count (Q-10 or equivalent). If unavailable, omit the parenthetical from the FULL template.
- `{{PRODUCT_COUNT}}` — from `gate_flags.md` evidence for product count (Q-08 catalog count). If unavailable, omit the parenthetical from the FULL template.

If a template variable cannot be resolved (source missing), use the PARTIAL template instead — never render a STRONG or FULL template with unresolved variables. For FULL templates, the parenthetical counts (`{{MIXPANEL_USER_COUNT}}`, `{{CUSTOMER_COUNT}}`, `{{PRODUCT_COUNT}}`) are the only exception — those may be gracefully omitted while keeping the FULL template.

### J.4b PARTIAL-Tier "What You'd See" Teaser

When a subsection is gated out due to missing data (e.g., `HAS_PORTAL_ORDERS = false` suppresses capture rate), section builders at PARTIAL or LIMITED tier MAY include a single `.callout.opportunity` teaser at the point where the gated subsection would appear. This makes the data-enrichment value proposition concrete without being salesy.

**Template:**

```html
<div class="callout opportunity">
  <div class="callout-title">What this section would show with connected data</div>
  <p>{{TEASER_TEXT}}</p>
</div>
```

**Per-section teaser text (use verbatim or adapt to context):**

- **§2 (rep capture):** "If total-business order data with rep attribution were connected, this section would show each rep's capture rate — what percentage of their territory's full revenue flows through the platform. Clients with this data typically discover a 5–30× spread across their team."
- **§3 (customer penetration):** "If total-business order data were connected, this section would show which of your highest-value accounts have never placed a platform order — and the combined revenue they represent through other channels."
- **§5 (capture rate):** "If total-business order data were connected, this section would show your platform capture rate — how much of your full revenue flows through the platform. Clients with this data typically discover 70–90% of their business is invisible to their digital ordering tools."

**Rules:**
- Maximum ONE teaser per section (not per gated subsection)
- Only at PARTIAL or LIMITED tier — never at STRONG or FULL
- Never in §6, §7, or §8 (no confidence framework)
- The teaser replaces the gated subsection's slot — do not leave a gap AND show a teaser

### J.5 Section Builder Contract

Each section builder that has a confidence tier (§2, §3, §4, §5):

1. Reads its tier from `cache/section_confidence.md` (e.g., `SECTION_CONFIDENCE_3`)
2. If tier is FULL — selects the matching `§X-FULL` template from J.3, resolves variables, and places the `.data-confidence` div with label `FULL PICTURE` as the **last element** in the section fragment (after all subsections)
3. If tier is STRONG or PARTIAL — selects the matching template from §J.3, resolves variables, and places the `.data-confidence` div **immediately after the key metrics row, before the first subsection**
4. If tier is LIMITED — uses the `.data-confidence.limited` variant with warn styling, positioned at the **top** (same as STRONG/PARTIAL)
5. Every section fragment for §2–§5 MUST contain exactly one `.data-confidence` footer. §6, §7, and §8 do not have confidence tiers and omit the footer

## Cache Data

### Q-07_results.md

# Q-07 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| visible | 1,082 | 48 | 0 | 95.60 |

### Q-08_results.md

# Q-08 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-08 — Data Freshness Monitor
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 22
- **Run date**: 2026-06-16


| entity_type | last_updated | days_since_update | status |
| --- | --- | --- | --- |
| sales_quotas | 2025-08-20 19:47:14 | 300 | Stale |
| customer_payment_informations | 2025-08-20 19:47:14 | 300 | Stale |
| riser_prices | 2025-08-20 19:47:14 | 300 | Stale |
| placement_reports | 2025-08-20 19:47:14 | 300 | Stale |
| commitment_reports | 2025-08-20 19:47:14 | 300 | Stale |
| kit_items | 2025-08-20 19:47:14 | 300 | Stale |
| inventories | 2025-08-20 19:47:14 | 300 | Stale |
| contract_prices | 2025-08-20 19:47:14 | 300 | Stale |
| price_levels | 2025-08-20 19:47:14 | 300 | Stale |
| options | 2026-04-23 03:33:13 | 54 | Monitor |
| option_groups | 2026-04-23 03:33:17 | 54 | Monitor |
| products | 2026-04-23 03:33:36 | 54 | Monitor |
| smart_stacks | 2026-04-23 03:33:36 | 54 | Monitor |
| categories | 2026-04-23 03:33:37 | 54 | Monitor |
| collections | 2026-04-23 03:33:37 | 54 | Monitor |
| groups | 2026-04-23 03:33:37 | 54 | Monitor |
| trade_names | 2026-04-23 03:33:37 | 54 | Monitor |
| matrix_options | 2026-04-23 03:33:40 | 54 | Monitor |
| customers | 2026-06-16 10:03:38 | 0 | Fresh |
| portal_orders | 2026-06-16 10:04:08 | 0 | Fresh |
| portal_invoices | 2026-06-16 10:04:43 | 0 | Fresh |
| customer_favorites | 2026-06-16 12:16:19 | 0 | Fresh |

### Q-09_results.md

# Q-09 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-09 — Import Health — Monthly Trend
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 7
- **Run date**: 2026-06-16


| month | import_count |
| --- | --- |
| 2026-06-01 | 33 |
| 2026-05-01 | 62 |
| 2026-04-01 | 74 |
| 2026-03-01 | 70 |
| 2026-02-01 | 92 |
| 2026-01-01 | 104 |
| 2025-12-01 | 72 |

### Q-09_recent_results.md

# Q-09-recent Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-09-recent — Import Health — Recent Errors
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 10
- **Run date**: 2026-06-16


| created_at | data |
| --- | --- |
| 2026-06-16T12:16:19.183339 | ---
- - Sales Data
  - []
 |
| 2026-06-16T10:08:08.977573 | ---
- - Customers
  - - - :warning
      - 'Error running cleancsv: 2026/06/16 10:01:10 parse error on line 11770, column
        39: extraneous or missing " in quoted-field

        '
    - - :error
      - 'Line 1724: Default price code ''t'' must be a valid price level code'
    - - :error
      - 'Line 1725: Default price code ''t'' must be a valid price level code'
    - - :error
      - 'Line 1726: Default price code ''t'' must be a valid price level code'
    - - :error
      - 'Line 1727: Default price code ''t'' must be a valid price level code'
    - - :warning
      - 'Line 11770: Any value after quoted field isn''t allowed in line 1.'
- - Portal Orders
  - - - :warning
      - 'Error running cleancsv: 2026/06/16 10:03:39 parse error on line 57521, column
        554: extraneous or missing " in quoted-field

        '
    - - :warning
      - 'Line 57521: Any value after quoted field isn''t allowed in line 1.'
- - Portal Invoices
  - - - :warning
      - 'Error running cleancsv: 2026/06/16 10:04:09 record on line 11002; parse error
        on line 11003, column 10: extraneous or missing " in quoted-field

        '
    - - :warning
      - 'Line 11002: Unclosed quoted field in line 1.'
- - Portal Invoice Tracking Data
  - - - :warning
      - 'Error running cleancsv: 2026/06/16 10:04:43 parse error on line 141697, column
        14: extraneous or missing " in quoted-field

        '
    - - :warning
      - 'Line 141697: Any value after quoted field isn''t allowed in line 1.'
- - Territories
  - []
 |
| 2026-06-15T12:16:21.928811 | ---
- - Sales Data
  - []
 |
| 2026-06-15T10:06:47.664578 | ---
- - Customers
  - - - :warning
      - 'Error running cleancsv: 2026/06/15 10:01:08 parse error on line 11770, column
        39: extraneous or missing " in quoted-field

        '
    - - :error
      - 'Line 1724: Default price code ''t'' must be a valid price level code'
    - - :error
      - 'Line 1725: Default price code ''t'' must be a valid price level code'
    - - :error
      - 'Line 1726: Default price code ''t'' must be a valid price level code'
    - - :error
      - 'Line 1727: Default price code ''t'' must be a valid price level code'
    - - :warning
      - 'Line 11770: Any value after quoted field isn''t allowed in line 1.'
- - Portal Orders
  - - - :warning
      - 'Error running cleancsv: 2026/06/15 10:03:05 parse error on line 57521, column
        554: extraneous or missing " in quoted-field

        '
    - - :warning
      - 'Line 57521: Any value after quoted field isn''t allowed in line 1.'
- - Portal Invoices
  - - - :warning
      - 'Error running cleancsv: 2026/06/15 10:03:37 record on line 11002; parse error
        on line 11003, column 10: extraneous or missing " in quoted-field

        '
    - - :warning
      - 'Line 11002: Unclosed quoted field in line 1.'
- - Portal Invoice Tracking Data
  - - - :warning
      - 'Error running cleancsv: 2026/06/15 10:04:09 parse error on line 141510, column
        14: extraneous or missing " in quoted-field

        '
    - - :warning
      - 'Line 141510: Any value after quoted field isn''t allowed in line 1.'
- - Territories
  - []
 |
| 2026-06-14T12:16:19.725475 | ---
- - Sales Data
  - []
 |
| 2026-06-14T10:06:31.851207 | ---
- - Customers
  - - - :warning
      - 'Error running cleancsv: 2026/06/14 10:01:08 parse error on line 11770, column
        39: extraneous or missing " in quoted-field

        '
    - - :error
      - 'Line 1724: Default price code ''t'' must be a valid price level code'
    - - :error
      - 'Line 1725: Default price code ''t'' must be a valid price level code'
    - - :error
      - 'Line 1726: Default price code ''t'' must be a valid price level code'
    - - :error
      - 'Line 1727: Default price code ''t'' must be a valid price level code'
    - - :warning
      - 'Line 11770: Any value after quoted field isn''t allowed in line 1.'
- - Portal Orders
  - - - :warning
      - 'Error running cleancsv: 2026/06/14 10:03:07 parse error on line 57521, column
        554: extraneous or missing " in quoted-field

        '
    - - :warning
      - 'Line 57521: Any value after quoted field isn''t allowed in line 1.'
- - Portal Invoices
  - - - :warning
      - 'Error running cleancsv: 2026/06/14 10:03:35 record on line 11002; parse error
        on line 11003, column 10: extraneous or missing " in quoted-field

        '
    - - :warning
      - 'Line 11002: Unclosed quoted field in line 1.'
- - Portal Invoice Tracking Data
  - - - :warning
      - 'Error running cleancsv: 2026/06/14 10:04:03 parse error on line 141510, column
        14: extraneous or missing " in quoted-field

        '
    - - :warning
      - 'Line 141510: Any value after quoted field isn''t allowed in line 1.'
- - Territories
  - []
 |
| 2026-06-13T12:15:19.065086 | ---
- - Sales Data
  - []
 |
| 2026-06-13T10:06:48.110417 | ---
- - Customers
  - - - :warning
      - 'Error running cleancsv: 2026/06/13 10:01:09 parse error on line 11770, column
        39: extraneous or missing " in quoted-field

        '
    - - :error
      - 'Line 1724: Default price code ''t'' must be a valid price level code'
    - - :error
      - 'Line 1725: Default price code ''t'' must be a valid price level code'
    - - :error
      - 'Line 1726: Default price code ''t'' must be a valid price level code'
    - - :error
      - 'Line 1727: Default price code ''t'' must be a valid price level code'
    - - :warning
      - 'Line 11770: Any value after quoted field isn''t allowed in line 1.'
- - Portal Orders
  - - - :warning
      - 'Error running cleancsv: 2026/06/13 10:03:07 parse error on line 57521, column
        554: extraneous or missing " in quoted-field

        '
    - - :warning
      - 'Line 57521: Any value after quoted field isn''t allowed in line 1.'
- - Portal Invoices
  - - - :warning
      - 'Error running cleancsv: 2026/06/13 10:03:39 record on line 11002; parse error
        on line 11003, column 10: extraneous or missing " in quoted-field

        '
    - - :warning
      - 'Line 11002: Unclosed quoted field in line 1.'
- - Portal Invoice Tracking Data
  - - - :warning
      - 'Error running cleancsv: 2026/06/13 10:04:09 parse error on line 141510, column
        14: extraneous or missing " in quoted-field

        '
    - - :warning
      - 'Line 141510: Any value after quoted field isn''t allowed in line 1.'
- - Territories
  - []
 |
| 2026-06-12T12:16:20.244710 | ---
- - Sales Data
  - []
 |
| 2026-06-12T10:08:13.105700 | ---
- - Customers
  - - - :warning
      - 'Error running cleancsv: 2026/06/12 10:01:08 parse error on line 11770, column
        39: extraneous or missing " in quoted-field

        '
    - - :error
      - 'Line 1724: Default price code ''t'' must be a valid price level code'
    - - :error
      - 'Line 1725: Default price code ''t'' must be a valid price level code'
    - - :error
      - 'Line 1726: Default price code ''t'' must be a valid price level code'
    - - :error
      - 'Line 1727: Default price code ''t'' must be a valid price level code'
    - - :warning
      - 'Line 11770: Any value after quoted field isn''t allowed in line 1.'
- - Portal Orders
  - - - :warning
      - 'Error running cleancsv: 2026/06/12 10:03:39 parse error on line 57521, column
        554: extraneous or missing " in quoted-field

        '
    - - :warning
      - 'Line 57521: Any value after quoted field isn''t allowed in line 1.'
- - Portal Invoices
  - - - :warning
      - 'Error running cleancsv: 2026/06/12 10:04:09 record on line 11002; parse error
        on line 11003, column 10: extraneous or missing " in quoted-field

        '
    - - :warning
      - 'Line 11002: Unclosed quoted field in line 1.'
- - Portal Invoice Tracking Data
  - - - :warning
      - 'Error running cleancsv: 2026/06/12 10:04:45 parse error on line 141324, column
        14: extraneous or missing " in quoted-field

        '
    - - :warning
      - 'Line 141324: Any value after quoted field isn''t allowed in line 1.'
- - Territories
  - []
 |

### Q-10_results.md

# Q-10 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-10 — Feature Enablement Gap Analysis
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| enable_sales_portal | enable_online_catalog | enable_online_ordering | kit_item_count | contract_price_count | enrollment_count | smart_stack_count | shared_resource_count | portal_order_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 0 | 2 | 7 | 412 | 56,414 |

### Q-11_results.md

# Q-11 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-11 — Configuration Completeness
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 18
- **Run date**: 2026-06-16


| entity_type | last_updated | days_stale | related_record_count |
| --- | --- | --- | --- |
| sales_quotas | 2025-08-20 19:47:14 | 300 | 0 |
| customer_payment_informations | 2025-08-20 19:47:14 | 300 | — |
| riser_prices | 2025-08-20 19:47:14 | 300 | — |
| placement_reports | 2025-08-20 19:47:14 | 300 | — |
| commitment_reports | 2025-08-20 19:47:14 | 300 | — |
| kit_items | 2025-08-20 19:47:14 | 300 | 0 |
| inventories | 2025-08-20 19:47:14 | 300 | — |
| contract_prices | 2025-08-20 19:47:14 | 300 | 0 |
| price_levels | 2025-08-20 19:47:14 | 300 | — |
| options | 2026-04-23 03:33:13 | 54 | — |
| option_groups | 2026-04-23 03:33:17 | 54 | — |
| products | 2026-04-23 03:33:36 | 54 | — |
| smart_stacks | 2026-04-23 03:33:36 | 54 | — |
| categories | 2026-04-23 03:33:37 | 54 | — |
| collections | 2026-04-23 03:33:37 | 54 | — |
| groups | 2026-04-23 03:33:37 | 54 | — |
| trade_names | 2026-04-23 03:33:37 | 54 | — |
| matrix_options | 2026-04-23 03:33:40 | 54 | — |

### Q-22_results.md

# Q-22 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-22 — Feature Usage Depth
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| org_shortname | org_name | submit_order | select_a_customer | search_for_customer | email_item_info | create_pdf_catalog | view_library_entry | view_smartpicks | access_sales_portal | filter_products | search_products | search_collections | order_configured_item | view_kit | order_kit | share_my_list | export_data_to_csv | export_data_to_excel | total_events | total_users |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hfg | Hubbardton Forge | 3,113 | 16,484 | 38,470 | 244 | 708 | 31,067 | 226 | 5,105 | 311 | 31,548 | 746 | 17,130 | 0 | 0 | 14 | 11 | 4 | 197,413 | 137 |

### Q-46_pg_results.md

# Q-46-pg Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-46-pg — Workflow Maturity — Postgres
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| submitted_ecat_orders_90d |
| --- |
| 443 |

### Q-46_bq_results.md

# Q-46-bq Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-46-bq — Workflow Maturity — Mixpanel
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| customer_targeting_events | product_discovery_events | presentation_events |
| --- | --- | --- |
| 54,954 | 31,859 | 966 |

### Q-47_results.md

# Q-47 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-47 — Smart Stack Effectiveness
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 7
- **Run date**: 2026-06-16


| stack_id | stack_name | published | is_dormant | created_at | updated_at | days_since_update |
| --- | --- | --- | --- | --- | --- | --- |
| 6,776 | New Product | 1 | — | 2022-03-03 13:25:14 | 2026-04-23 03:33:36 | 54 |
| 10,156 | Vegas Showroom | 1 | 0 | 2025-07-14 13:53:07 | 2026-04-23 03:33:36 | 54 |
| 10,372 | BDNY 2025 | 1 | 0 | 2025-10-30 16:40:55 | 2026-04-23 03:33:36 | 54 |
| 9,349 | High Point Showroom | 1 | 0 | 2024-10-14 15:31:09 | 2026-04-23 03:33:36 | 54 |
| 8,701 | Top Sellers | 1 | 0 | 2024-01-08 15:28:17 | 2026-04-23 03:33:36 | 54 |
| 8,783 | Dallas Showroom | 1 | 0 | 2024-02-01 17:29:46 | 2026-04-23 03:33:36 | 54 |
| 10,527 | New Product - Jan 2026 | 1 | — | 2026-01-10 15:21:29 | 2026-04-23 03:33:36 | 54 |

### Q-50_results.md

# Q-50 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-50 — Library / Document Inventory
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 16
- **Run date**: 2026-06-16


| resource_id | document_name | resource_type | shared_document_file_name | created_at | updated_at | days_since_update |
| --- | --- | --- | --- | --- | --- | --- |
| 33,739 | — | directory | — | 2025-08-26 14:39:33 | 2025-08-26 14:39:33 | 294 |
| 32,915 | — | directory | — | 2025-05-23 13:38:55 | 2025-05-23 13:38:55 | 389 |
| 30,005 | — | directory | — | 2024-10-08 11:51:22 | 2024-10-08 11:51:22 | 616 |
| 20,372 | — | directory | — | 2022-03-04 17:24:12 | 2024-09-06 18:57:50 | 648 |
| 27,201 | — | directory | — | 2024-01-30 14:39:43 | 2024-09-06 18:57:50 | 648 |
| 23,086 | — | directory | — | 2023-02-15 16:43:23 | 2024-09-06 18:57:50 | 648 |
| 23,873 | — | directory | — | 2023-04-27 19:26:39 | 2024-09-06 18:57:50 | 648 |
| 25,541 | — | directory | — | 2023-10-09 17:38:52 | 2024-09-06 18:57:50 | 648 |
| 20,375 | — | directory | — | 2022-03-04 17:24:42 | 2024-09-06 18:57:50 | 648 |
| 20,373 | — | directory | — | 2022-03-04 17:24:28 | 2024-09-06 18:57:50 | 648 |
| 20,370 | — | directory | — | 2022-03-04 17:23:43 | 2024-09-06 18:57:50 | 648 |
| 26,942 | — | directory | — | 2024-01-11 18:14:26 | 2024-09-06 18:57:50 | 648 |
| 20,346 | — | directory | — | 2022-03-01 21:14:31 | 2024-09-06 18:57:50 | 648 |
| 25,102 | — | directory | — | 2023-08-15 12:23:17 | 2024-09-06 18:57:50 | 648 |
| 20,347 | — | directory | — | 2022-03-01 21:15:23 | 2024-09-06 18:57:50 | 648 |
| 20,374 | — | directory | — | 2022-03-04 17:24:35 | 2024-09-06 18:57:50 | 648 |

### user_group_mapping.md

# User Group Mapping — Hubbardton Forge (hfg, org_id=165)
- **Run date**: 2026-06-16
- **Total Postgres users**: 206
- **Matched to Mixpanel (Q-01 Step 1)**: 118 of 137 (86%)
- **Classification confidence**: LOW
- **Split available**: False

## Group Classification

| User Group (Admin Console) | Bucket | User Count |
| --- | --- | --- |
| ResTradeGroup | other | 76 |
| ComGroup | other | 74 |
| ResTradeCom | other | 16 |
| AdminDefaultUserGroup | admin_internal | 11 |
| CanadaRes | other | 9 |
| InternalHFSales | admin_internal | 9 |
| 1 - Default eOL User Group | admin_internal | 4 |
| z-SuperCat | admin_internal | 4 |
| Decorating Den Group | admin_internal | 1 |
| Decorating Den Group | other | 1 |
| eCat Online Public Site | admin_internal | 1 |

## Aggregate Split

| Bucket | Users | Total Events | Event Share |
| --- | --- | --- | --- |
| admin_internal | 14 | 6,574 | 3.5% |
| other | 104 | 182,073 | 96.5% |
