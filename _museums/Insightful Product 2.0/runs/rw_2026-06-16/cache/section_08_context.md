# Section 8 Context Bundle — RENWIL (rw)
Run date: 2026-06-16

## Gate Flags

# Gate Flags — RENWIL (rw, org_id=248)
- **Run date**: 2026-06-16
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: True; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | False | portal_order_count=0, portal_order_gmv=$0 |
| HAS_INVENTORY | True | inventory_count=2048 |
| HAS_SALES_DATA | False | sales_data_count=0 |
| HAS_SALES_SECTION | True | qualifying_reps=46 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | renwil_rw_eol |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | SKIP |  |
| VM45_GATE_2 | SKIP |  |
| VM45_RENDER | False |  |
| QUALIFYING_REP_COUNT | 46 | 46 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 90 rows |
| SHOWROOM_EXCLUSIONS | 1 | 1 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 8667, Mixpanel total submit_order (Q-01): 9991 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=93.3%, ambiguous_rate=1.2%, showroom_event_share=6.4% |
| USER_GROUP_JOIN_RATE | 93% | 84 of 90 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 6% | showroom+admin share of matched events: 6.4% |
| ADMIN_REPS_IN_LEADERBOARD | True | 3 admin/showroom users in leaderboard: Suzanne Hogan, Chuck Wiebe, Haris Baig |

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
| HAS_NEW_ITEMS | True | new_item_count=184 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | PARTIAL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | PARTIAL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: RENWIL
- **Shortname**: rw
- **Org ID**: 248
- **Bundle**: 7
- **Bundle label for report**: 7

## Validation Log

- portal_orders LTM count=0, gmv=0.0 — HAS_PORTAL_ORDERS overridden to false

## Section Confidence

# Section Confidence Tiers — RENWIL (rw, org_id=248)
- **Run date**: 2026-06-16

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

# Q-07 Results — RENWIL (rw, org_id=248)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| visible | 1,731 | 2 | 0 | 99.90 |

### Q-08_results.md

# Q-08 Results — RENWIL (rw, org_id=248)
- **Query**: Q-08 — Data Freshness Monitor
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 22
- **Run date**: 2026-06-16


| entity_type | last_updated | days_since_update | status |
| --- | --- | --- | --- |
| sales_quotas | 2025-08-20 19:47:15 | 300 | Stale |
| customer_payment_informations | 2025-08-20 19:47:15 | 300 | Stale |
| riser_prices | 2025-08-20 19:47:15 | 300 | Stale |
| placement_reports | 2025-08-20 19:47:15 | 300 | Stale |
| commitment_reports | 2025-08-20 19:47:15 | 300 | Stale |
| matrix_options | 2025-08-20 19:47:15 | 300 | Stale |
| kit_items | 2025-08-20 19:47:15 | 300 | Stale |
| customer_favorites | 2025-08-20 19:47:15 | 300 | Stale |
| contract_prices | 2025-08-20 19:47:15 | 300 | Stale |
| trade_names | 2025-08-20 19:47:15 | 300 | Stale |
| collections | 2025-08-20 19:47:15 | 300 | Stale |
| price_levels | 2025-08-20 19:47:15 | 300 | Stale |
| options | 2025-11-07 20:52:41 | 221 | Stale |
| option_groups | 2025-11-07 20:52:41 | 221 | Stale |
| portal_orders | 2026-03-13 18:54:01 | 95 | Monitor |
| categories | 2026-04-27 16:54:21 | 50 | Monitor |
| groups | 2026-04-27 16:54:21 | 50 | Monitor |
| products | 2026-06-10 16:20:31 | 6 | Fresh |
| smart_stacks | 2026-06-10 16:20:31 | 6 | Fresh |
| inventories | 2026-06-16 17:02:22 | 0 | Fresh |
| customers | 2026-06-16 20:28:11 | 0 | Fresh |
| portal_invoices | 2026-06-16 22:07:05 | 0 | Fresh |

### Q-09_results.md

# Q-09 Results — RENWIL (rw, org_id=248)
- **Query**: Q-09 — Import Health — Monthly Trend
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 7
- **Run date**: 2026-06-16


| month | import_count |
| --- | --- |
| 2026-06-01 | 37 |
| 2026-05-01 | 53 |
| 2026-04-01 | 50 |
| 2026-03-01 | 52 |
| 2026-02-01 | 37 |
| 2026-01-01 | 53 |
| 2025-12-01 | 9 |

### Q-09_recent_results.md

# Q-09-recent Results — RENWIL (rw, org_id=248)
- **Query**: Q-09-recent — Import Health — Recent Errors
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 10
- **Run date**: 2026-06-16


| created_at | data |
| --- | --- |
| 2026-06-16 22:07:05 | ---
- - Portal Invoices
  - []
 |
| 2026-06-16 20:28:11 | ---
- - Customers
  - - - :warning
      - BillToCode 13454291CANADAINC is greater than 15 characters
    - - :warning
      - BillToCode 15038979CANADAINC is greater than 15 characters
    - - :warning
      - BillToCode 2HINTERIORDESIGN is greater than 15 characters
    - - :warning
      - BillToCode 5CORNERSFURNITURE is greater than 15 characters
    - - :warning
      - BillToCode 95027405QUEBECINC is greater than 15 characters
    - - :warning
      - BillToCode 97300788CANADAINC is greater than 15 characters
    - - :warning
      - BillToCode ABINTERIORSOSHAWA is greater than 15 characters
    - - :warning
      - BillToCode ACANTHUSINTERIORS is greater than 15 characters
    - - :warning
      - BillToCode ACCESSCARPETBARN is greater than 15 characters
    - - :warning
      - BillToCode ACCESSCOLOURSTUDIO is greater than 15 characters
    - - :warning
      - BillToCode ACCESSCOUVREPLANCH is greater than 15 characters
    - - :warning
      - BillToCode ACCESSCREATIONSREK is greater than 15 characters
    - - :warning
      - BillToCode ACCESSCUISICONCEPT is greater than 15 characters
    - - :warning
      - BillToCode ACCESSDAYSPAINTS is greater than 15 characters
    - - :warning
      - BillToCode ACCESSDECORATORSCH is greater than 15 characters
    - - :warning
      - BillToCode ACCESSDECORBRASSAR is greater than 15 characters
    - - :warning
      - BillToCode ACCESSESPACEBLUDEC is greater than 15 characters
    - - :warning
      - BillToCode ACCESSFLORDECOARVI is greater than 15 characters
    - - :warning
      - BillToCode ACCESSGAUVINDRAP is greater than 15 characters
    - - :warning
      - BillToCode ACCESSHOMESCAPES is greater than 15 characters
    - - :warning
      - BillToCode ACCESSINNOVATIVE is greater than 15 characters
    - - :warning
      - BillToCode ACCESSJUNEAUFRERES is greater than 15 characters
    - - :warning
      - BillToCode ACCESSJUTRASDECOR is greater than 15 characters
    - - :warning
      - BillToCode ACCESSLAMONTAGNE is greater than 15 characters
    - - :warning
      - BillToCode ACCESSLEOPOLDBOUCH is greater than 15 characters
    - - :warning
      - BillToCode ACCESSMAISONDUDECO is greater than 15 characters
    - - :warning
      - BillToCode ACCESSMOUNTAINPAIN is greater than 15 characters
    - - :warning
      - BillToCode ACCESSPEINTUREDECO is greater than 15 characters
    - - :warning
      - BillToCode ACCESSPIERRECHOLET is greater than 15 characters
    - - :warning
      - BillToCode ACCESSSILVERBROOKP is greater than 15 characters
    - - :warning
      - BillToCode ACCESSSOUTHPAINT is greater than 15 characters
    - - :warning
      - BillToCode ACCESSTAPISCOWANS is greater than 15 characters
    - - :warning
      - BillToCode ACCESSTAPISNADON is greater than 15 characters
    - - :warning
      - BillToCode AJKPROPERTYMANAGE is greater than 15 characters
    - - :warning
      - BillToCode ALANAFLETCHERINTER is greater than 15 characters
    - - :warning
      - BillToCode ALBERTSLATEROTTAWA is greater than 15 characters
    - - :warning
      - BillToCode ALEXANDRACREVIER is greater than 15 characters
    - - :warning
      - BillToCode ALEXROSEINTERIORS is greater than 15 characters
    - - :warning
      - BillToCode ALIBUDDINTERIORS is greater than 15 characters
    - - :warning
      - BillToCode ALIGNDEVELOPMENTS is greater than 15 characters
    - - :warning
      - BillToCode ALIGNEDINTERIORS is greater than 15 characters
    - - :warning
      - BillToCode ALLEGROINTERIORS is greater than 15 characters
    - - :warning
      - BillToCode AMENAGEMENTSJMCINC is greater than 15 characters
    - - :warning
      - BillToCode ANAMEYERINTERIOR is greater than 15 characters
    - - :warning
      - BillToCode ANDERSONCARPETHOME is greater than 15 characters
    - - :warning
      - BillToCode ANDREAHYLTONHOME is greater than 15 characters
    - - :warning
      - BillToCode ANNEMARIELAFRANCE is greater than 15 characters
    - - :warning
      - BillToCode ANNIEGRANTDESIGNER is greater than 15 characters
    - - :warning
      - BillToCode ANNIEVERTEFEUILLE is greater than 15 characters
    - - :warning
      - BillToCode ANNJOHNSTONDESIGN is greater than 15 characters
    - - :warning
      - BillToCode ANTHEMPROPERTIES is greater than 15 characters
    - - :warning
      - BillToCode APPELQUISTINTERIOR is greater than 15 characters
    - - :warning
      - BillToCode ARTISTAINTERIORS is greater than 15 characters
    - - :warning
      - BillToCode ASHLEYMONTGOMERY is greater than 15 characters
    - - :warning
      - BillToCode ATELIERAVANTGARDE is greater than 15 characters
    - - :warning
      - BillToCode ATELIERLUXDESIGN is greater than 15 characters
    - - :warning
      - BillToCode ATHOMEJUDYDIAMOND is greater than 15 characters
    - - :warning
      - BillToCode AUBERGEDUVIEUXPORT is greater than 15 characters
    - - :warning
      - BillToCode AULOFTSTYLELIBRE is greater than 15 characters
    - - :warning
      - BillToCode AVENUELIGHTINGDES is greater than 15 characters
    - - :warning
      - BillToCode BARLOWREIDDESIGN is greater than 15 characters
    - - :warning
      - BillToCode BATHROOMKITCHENSOL is greater than 15 characters
    - - :warning
      - BillToCode BDINTERIORDESIGN is greater than 15 characters
    - - :warning
      - BillToCode BEAULIEULAMOUREUX is greater than 15 characters
    - - :warning
      - BillToCode BELLEAVENUEDESIGN is greater than 15 characters
    - - :warning
      - BillToCode BELLEWETHERCURATED is greater than 15 characters
    - - :warning
      - BillToCode BELMONTDEOCRATION is greater than 15 characters
    - - :warning
      - BillToCode BEVERLYREDLICKDE is greater than 15 characters
    - - :warning
      - BillToCode BLACKSHEEPINTERI is greater than 15 characters
    - - :warning
      - BillToCode BLISSSTUDIOGROUP is greater than 15 characters
    - - :warning
      - BillToCode BLOOMFIELDFLOWERS is greater than 15 characters
    - - :warning
      - BillToCode BOBECHEINTERIORS is greater than 15 characters
    - - :warning
      - BillToCode BOUTIQUEATELIERHOM is greater than 15 characters
    - - :warning
      - BillToCode BREATHEINTERIORS is greater than 15 characters
    - - :warning
      - BillToCode BRICKSANDBIRCHES is greater than 15 characters
    - - :warning
      - BillToCode BRUNEAULUMINAIRE is greater than 15 characters
    - - :warning
      - BillToCode BRUNORIDGEHOLDINGS is greater than 15 characters
    - - :warning
      - BillToCode BRUTONSDECORATING is greater than 15 characters
    - - :warning
      - BillToCode CANADIANHERITAGE is greater than 15 characters
    - - :warning
      - BillToCode CANADIANRENOVATION is greater than 15 characters
    - - :warning
      - BillToCode CARLYLEINTERIORS is greater than 15 characters
    - - :warning
      - BillToCode CAROLINEBOUFFARD is greater than 15 characters
    - - :warning
      - BillToCode CAROLINEDESBIENS is greater than 15 characters
    - - :warning
      - BillToCode CAROLYNCOLAGIOVANN is greater than 15 characters
    - - :warning
      - BillToCode CARRIAGELANEDESIGN is greater than 15 characters
    - - :warning
      - BillToCode CARRINGTONCONSTRUC is greater than 15 characters
    - - :warning
      - BillToCode CASTONGUAYDESIGN is greater than 15 characters
    - - :warning
      - BillToCode CATHELINECAVARROC is greater than 15 characters
    - - :warning
      - BillToCode CATHERINEBORDUAS is greater than 15 characters
    - - :warning
      - BillToCode CCINTERIORSHUNTS is greater than 15 characters
    - - :warning
      - BillToCode CENTREDECOUPEKSA is greater than 15 characters
    - - :warning
      - BillToCode CENTRESTAGEDESIGN is greater than 15 characters
    - - :warning
      - BillToCode CERAMIQUEDECHOIX is greater than 15 characters
    - - :warning
      - BillToCode CERAMIQUEDECORANDR is greater than 15 characters
    - - :warning
      - BillToCode CHAGALLCONSTRUCT is greater than 15 characters
    - - :warning
      - BillToCode CHAMBERLANDDESIGN is greater than 15 characters
    - - :warning
      - BillToCode CHARLOTTEMACDONALD is greater than 15 characters
    - - :warning
      - BillToCode CHEDIACBRANDSOURCE is greater than 15 characters
    - - :warning
      - BillToCode CHERVINFURNITURE is greater than 15 characters
    - - :warning
      - BillToCode CHERYLJASLOWDESIGN is greater than 15 characters
    - - :warning
      - Too many BillToCode length warnings, the remaining 881 warnings are not displayed
 |
| 2026-06-16 17:02:22 | ---
- - Inventory
  - - - :warning
      - 'Line 14: Product not found, record ignored., BaseItemCode=CHA071'
    - - :warning
      - 'Line 19: Product not found, record ignored., BaseItemCode=CHA088'
    - - :warning
      - 'Line 20: Product not found, record ignored., BaseItemCode=CHA089'
    - - :warning
      - 'Line 24: Product not found, record ignored., BaseItemCode=CHA094'
    - - :warning
      - 'Line 25: Product not found, record ignored., BaseItemCode=CHA095'
    - - :warning
      - 'Line 27: Product not found, record ignored., BaseItemCode=CHA097'
    - - :warning
      - 'Line 28: Product not found, record ignored., BaseItemCode=CHA098'
    - - :warning
      - 'Line 37: Product not found, record ignored., BaseItemCode=CL220'
    - - :warning
      - 'Line 38: Product not found, record ignored., BaseItemCode=CL239'
    - - :warning
      - 'Line 42: Product not found, record ignored., BaseItemCode=CL257'
    - - :warning
      - 'Line 76: Product not found, record ignored., BaseItemCode=LPC4058'
    - - :warning
      - 'Line 88: Product not found, record ignored., BaseItemCode=LPC4418'
    - - :warning
      - 'Line 92: Product not found, record ignored., BaseItemCode=LPC4434'
    - - :warning
      - 'Line 96: Product not found, record ignored., BaseItemCode=LPC4445'
    - - :warning
      - 'Line 98: Product not found, record ignored., BaseItemCode=LPC4454'
    - - :warning
      - 'Line 130: Product not found, record ignored., BaseItemCode=LPF3023'
    - - :warning
      - 'Line 133: Product not found, record ignored., BaseItemCode=LPF3071'
    - - :warning
      - 'Line 135: Product not found, record ignored., BaseItemCode=LPF3110'
    - - :warning
      - 'Line 136: Product not found, record ignored., BaseItemCode=LPF3111'
    - - :warning
      - 'Line 139: Product not found, record ignored., BaseItemCode=LPF3135'
    - - :warning
      - 'Line 145: Product not found, record ignored., BaseItemCode=LPF3146'
    - - :warning
      - 'Line 147: Product not found, record ignored., BaseItemCode=LPF3149'
    - - :warning
      - 'Line 151: Product not found, record ignored., BaseItemCode=LPF3153'
    - - :warning
      - 'Line 179: Product not found, record ignored., BaseItemCode=LPT1047'
    - - :warning
      - 'Line 180: Product not found, record ignored., BaseItemCode=LPT1057'
    - - :warning
      - 'Line 183: Product not found, record ignored., BaseItemCode=LPT1127'
    - - :warning
      - 'Line 186: Product not found, record ignored., BaseItemCode=LPT1159'
    - - :warning
      - 'Line 188: Product not found, record ignored., BaseItemCode=LPT1161'
    - - :warning
      - 'Line 191: Product not found, record ignored., BaseItemCode=LPT1173'
    - - :warning
      - 'Line 194: Product not found, record ignored., BaseItemCode=LPT1183'
    - - :warning
      - 'Line 203: Product not found, record ignored., BaseItemCode=LPT1216'
    - - :warning
      - 'Line 205: Product not found, record ignored., BaseItemCode=LPT1218'
    - - :warning
      - 'Line 206: Product not found, record ignored., BaseItemCode=LPT1219'
    - - :warning
      - 'Line 207: Product not found, record ignored., BaseItemCode=LPT1221'
    - - :warning
      - 'Line 208: Product not found, record ignored., BaseItemCode=LPT1222'
    - - :warning
      - 'Line 211: Product not found, record ignored., BaseItemCode=LPT1225'
    - - :warning
      - 'Line 217: Product not found, record ignored., BaseItemCode=LPT1234'
    - - :warning
      - 'Line 223: Product not found, record ignored., BaseItemCode=LPT1240'
    - - :warning
      - 'Line 224: Product not found, record ignored., BaseItemCode=LPT1241'
    - - :warning
      - 'Line 225: Product not found, record ignored., BaseItemCode=LPT1242'
    - - :warning
      - 'Line 226: Product not found, record ignored., BaseItemCode=LPT1243'
    - - :warning
      - 'Line 227: Product not found, record ignored., BaseItemCode=LPT1246'
    - - :warning
      - 'Line 228: Product not found, record ignored., BaseItemCode=LPT1249'
    - - :warning
      - 'Line 229: Product not found, record ignored., BaseItemCode=LPT1250'
    - - :warning
      - 'Line 234: Product not found, record ignored., BaseItemCode=LPT1257'
    - - :warning
      - 'Line 236: Product not found, record ignored., BaseItemCode=LPT1259'
    - - :warning
      - 'Line 245: Product not found, record ignored., BaseItemCode=LPT1268'
    - - :warning
      - 'Line 247: Product not found, record ignored., BaseItemCode=LPT1270'
    - - :warning
      - 'Line 248: Product not found, record ignored., BaseItemCode=LPT1271'
    - - :warning
      - 'Line 251: Product not found, record ignored., BaseItemCode=LPT1274'
    - - :warning
      - 'Line 252: Product not found, record ignored., BaseItemCode=LPT1275'
    - - :warning
      - 'Line 258: Product not found, record ignored., BaseItemCode=LPT1284'
    - - :warning
      - 'Line 261: Product not found, record ignored., BaseItemCode=LPT1287'
    - - :warning
      - 'Line 306: Product not found, record ignored., BaseItemCode=LPT1334'
    - - :warning
      - 'Line 333: Product not found, record ignored., BaseItemCode=LPT172'
    - - :warning
      - 'Line 334: Product not found, record ignored., BaseItemCode=LPT594'
    - - :warning
      - 'Line 336: Product not found, record ignored., BaseItemCode=LPT714'
    - - :warning
      - 'Line 337: Product not found, record ignored., BaseItemCode=LPT825'
    - - :warning
      - 'Line 338: Product not found, record ignored., BaseItemCode=LPT853'
    - - :warning
      - 'Line 339: Product not found, record ignored., BaseItemCode=LPT869'
    - - :warning
      - 'Line 340: Product not found, record ignored., BaseItemCode=LPT884'
    - - :warning
      - 'Line 341: Product not found, record ignored., BaseItemCode=LPT885'
    - - :warning
      - 'Line 343: Product not found, record ignored., BaseItemCode=LPT982'
    - - :warning
      - 'Line 344: Product not found, record ignored., BaseItemCode=MT1006'
    - - :warning
      - 'Line 347: Product not found, record ignored., BaseItemCode=MT1134'
    - - :warning
      - 'Line 348: Product not found, record ignored., BaseItemCode=MT1185'
    - - :warning
      - 'Line 350: Product not found, record ignored., BaseItemCode=MT1284'
    - - :warning
      - 'Line 360: Product not found, record ignored., BaseItemCode=MT1499'
    - - :warning
      - 'Line 366: Product not found, record ignored., BaseItemCode=MT1594'
    - - :warning
      - 'Line 371: Product not found, record ignored., BaseItemCode=MT1706'
    - - :warning
      - 'Line 377: Product not found, record ignored., BaseItemCode=MT1820'
    - - :warning
      - 'Line 383: Product not found, record ignored., BaseItemCode=MT1857'
    - - :warning
      - 'Line 403: Product not found, record ignored., BaseItemCode=MT2301'
    - - :warning
      - 'Line 404: Product not found, record ignored., BaseItemCode=MT2320'
    - - :warning
      - 'Line 424: Product not found, record ignored., BaseItemCode=MT2412'
    - - :warning
      - 'Line 432: Product not found, record ignored., BaseItemCode=MT2437'
    - - :warning
      - 'Line 433: Product not found, record ignored., BaseItemCode=MT2444'
    - - :warning
      - 'Line 438: Product not found, record ignored., BaseItemCode=MT2456'
    - - :warning
      - 'Line 439: Product not found, record ignored., BaseItemCode=MT2459'
    - - :warning
      - 'Line 442: Product not found, record ignored., BaseItemCode=MT2464'
    - - :warning
      - 'Line 443: Product not found, record ignored., BaseItemCode=MT2471'
    - - :warning
      - 'Line 448: Product not found, record ignored., BaseItemCode=MT2497'
    - - :warning
      - 'Line 459: Product not found, record ignored., BaseItemCode=MT2513'
    - - :warning
      - 'Line 470: Product not found, record ignored., BaseItemCode=MT2529'
    - - :warning
      - 'Line 472: Product not found, record ignored., BaseItemCode=MT2531'
    - - :warning
      - 'Line 479: Product not found, record ignored., BaseItemCode=MT2541'
    - - :warning
      - 'Line 493: Product not found, record ignored., BaseItemCode=MT2563'
    - - :warning
      - 'Line 495: Product not found, record ignored., BaseItemCode=MT2567'
    - - :warning
      - 'Line 503: Product not found, record ignored., BaseItemCode=MT2610'
    - - :warning
      - 'Line 504: Product not found, record ignored., BaseItemCode=MT2611'
    - - :warning
      - 'Line 509: Product not found, record ignored., BaseItemCode=MT2616'
    - - :warning
      - 'Line 515: Product not found, record ignored., BaseItemCode=MT2622'
    - - :warning
      - 'Line 517: Product not found, record ignored., BaseItemCode=MT2624'
    - - :warning
      - 'Line 519: Product not found, record ignored., BaseItemCode=MT2626'
    - - :warning
      - 'Line 530: Product not found, record ignored., BaseItemCode=MT2637'
    - - :warning
      - 'Line 531: Product not found, record ignored., BaseItemCode=MT2638'
    - - :warning
      - 'Line 535: Product not found, record ignored., BaseItemCode=MT2654'
    - - :warning
      - 'Line 598: Product not found, record ignored., BaseItemCode=MT849'
    - - :warning
      - 'Line 601: Product not found, record ignored., BaseItemCode=OL1485'
    - - :warning
      - 'Line 605: Product not found, record ignored., BaseItemCode=OL1717'
    - - :warning
      - 'Line 607: Product not found, record ignored., BaseItemCode=OL1730'
    - - :warning
      - 'Line 619: Product not found, record ignored., BaseItemCode=OL1965'
    - - :warning
      - 'Line 622: Product not found, record ignored., BaseItemCode=OL1978'
    - - :warning
      - 'Line 635: Product not found, record ignored., BaseItemCode=OL2058'
    - - :warning
      - 'Line 637: Product not found, record ignored., BaseItemCode=OL2065'
    - - :warning
      - 'Line 639: Product not found, record ignored., BaseItemCode=OL2067'
    - - :warning
      - 'Line 641: Product not found, record ignored., BaseItemCode=OL2069'
    - - :warning
      - 'Line 650: Product not found, record ignored., BaseItemCode=OL2090'
    - - :warning
      - 'Line 652: Product not found, record ignored., BaseItemCode=OL2096'
    - - :warning
      - 'Line 653: Product not found, record ignored., BaseItemCode=OL2098'
    - - :warning
      - 'Line 655: Product not found, record ignored., BaseItemCode=OL2101'
    - - :warning
      - 'Line 656: Product not found, record ignored., BaseItemCode=OL2102'
    - - :warning
      - 'Line 659: Product not found, record ignored., BaseItemCode=OL2107'
    - - :warning
      - 'Line 661: Product not found, record ignored., BaseItemCode=OL2110'
    - - :warning
      - 'Line 663: Product not found, record ignored., BaseItemCode=OL2112'
    - - :warning
      - 'Line 666: Product not found, record ignored., BaseItemCode=OL2115'
    - - :warning
      - 'Line 668: Product not found, record ignored., BaseItemCode=OL2117'
    - - :warning
      - 'Line 669: Product not found, record ignored., BaseItemCode=OL2121'
    - - :warning
      - 'Line 676: Product not found, record ignored., BaseItemCode=OL2130'
    - - :warning
      - 'Line 681: Product not found, record ignored., BaseItemCode=OL2136'
    - - :warning
      - 'Line 684: Product not found, record ignored., BaseItemCode=OL2139'
    - - :warning
      - 'Line 688: Product not found, record ignored., BaseItemCode=OL2143'
    - - :warning
      - 'Line 689: Product not found, record ignored., BaseItemCode=OL2144'
    - - :warning
      - 'Line 690: Product not found, record ignored., BaseItemCode=OL2145'
    - - :warning
      - 'Line 699: Product not found, record ignored., BaseItemCode=OL2155'
    - - :warning
      - 'Line 776: Product not found, record ignored., BaseItemCode=PF035'
    - - :warning
      - 'Line 777: Product not found, record ignored., BaseItemCode=PF043'
    - - :warning
      - 'Line 780: Product not found, record ignored., BaseItemCode=PF046'
    - - :warning
      - 'Line 782: Product not found, record ignored., BaseItemCode=PWFL1001'
    - - :warning
      - 'Line 783: Product not found, record ignored., BaseItemCode=PWFL1005'
    - - :warning
      - 'Line 784: Product not found, record ignored., BaseItemCode=PWFL1009'
    - - :warning
      - 'Line 785: Product not found, record ignored., BaseItemCode=PWFL1010'
    - - :warning
      - 'Line 786: Product not found, record ignored., BaseItemCode=PWFL1012'
    - - :warning
      - 'Line 787: Product not found, record ignored., BaseItemCode=PWFL1020'
    - - :warning
      - 'Line 789: Product not found, record ignored., BaseItemCode=PWFL1026'
    - - :warning
      - 'Line 790: Product not found, record ignored., BaseItemCode=PWFL1027'
    - - :warning
      - 'Line 791: Product not found, record ignored., BaseItemCode=PWFL1028'
    - - :warning
      - 'Line 792: Product not found, record ignored., BaseItemCode=PWFL1030'
    - - :warning
      - 'Line 793: Product not found, record ignored., BaseItemCode=PWFL1035'
    - - :warning
      - 'Line 794: Product not found, record ignored., BaseItemCode=PWFL1037'
    - - :warning
      - 'Line 795: Product not found, record ignored., BaseItemCode=PWFL1048'
    - - :warning
      - 'Line 804: Product not found, record ignored., BaseItemCode=PWFL1069'
    - - :warning
      - 'Line 805: Product not found, record ignored., BaseItemCode=PWFL1079'
    - - :warning
      - 'Line 806: Product not found, record ignored., BaseItemCode=PWFL1085'
    - - :warning
      - 'Line 810: Product not found, record ignored., BaseItemCode=PWFL1115'
    - - :warning
      - 'Line 811: Product not found, record ignored., BaseItemCode=PWFL1131'
    - - :warning
      - 'Line 812: Product not found, record ignored., BaseItemCode=PWFL1147'
    - - :warning
      - 'Line 813: Product not found, record ignored., BaseItemCode=PWFL1160'
    - - :warning
      - 'Line 814: Product not found, record ignored., BaseItemCode=PWFL1168'
    - - :warning
      - 'Line 815: Product not found, record ignored., BaseItemCode=PWFL1176'
    - - :warning
      - 'Line 816: Product not found, record ignored., BaseItemCode=PWFL1180'
    - - :warning
      - 'Line 817: Product not found, record ignored., BaseItemCode=PWFL1200'
    - - :warning
      - 'Line 819: Product not found, record ignored., BaseItemCode=PWFL1234'
    - - :warning
      - 'Line 820: Product not found, record ignored., BaseItemCode=PWFL1243'
    - - :warning
      - 'Line 822: Product not found, record ignored., BaseItemCode=PWFL1252'
    - - :warning
      - 'Line 825: Product not found, record ignored., BaseItemCode=PWFL1355'
    - - :warning
      - 'Line 826: Product not found, record ignored., BaseItemCode=PWFL1357'
    - - :warning
      - 'Line 827: Product not found, record ignored., BaseItemCode=PWFL1358'
    - - :warning
      - 'Line 829: Product not found, record ignored., BaseItemCode=PWFL1362'
    - - :warning
      - 'Line 830: Product not found, record ignored., BaseItemCode=PWFL1367'
    - - :warning
      - 'Line 831: Product not found, record ignored., BaseItemCode=PWFL1373'
    - - :warning
      - 'Line 832: Product not found, record ignored., BaseItemCode=PWFL1377'
    - - :warning
      - 'Line 833: Product not found, record ignored., BaseItemCode=PWFL1389'
    - - :warning
      - 'Line 835: Product not found, record ignored., BaseItemCode=PWFL1399'
    - - :warning
      - 'Line 837: Product not found, record ignored., BaseItemCode=PWFL1401'
    - - :warning
      - 'Line 838: Product not found, record ignored., BaseItemCode=PWFL1402'
    - - :warning
      - 'Line 839: Product not found, record ignored., BaseItemCode=PWFL1404'
    - - :warning
      - 'Line 840: Product not found, record ignored., BaseItemCode=PWFL1405'
    - - :warning
      - 'Line 841: Product not found, record ignored., BaseItemCode=PWFL1406'
    - - :warning
      - 'Line 843: Product not found, record ignored., BaseItemCode=PWFL1411'
    - - :warning
      - 'Line 844: Product not found, record ignored., BaseItemCode=PWFL1415'
    - - :warning
      - 'Line 846: Product not found, record ignored., BaseItemCode=PWFL1420'
    - - :warning
      - 'Line 847: Product not found, record ignored., BaseItemCode=PWFL1421'
    - - :warning
      - 'Line 848: Product not found, record ignored., BaseItemCode=PWFL1422'
    - - :warning
      - 'Line 851: Product not found, record ignored., BaseItemCode=PWFL1425'
    - - :warning
      - 'Line 855: Product not found, record ignored., BaseItemCode=PWFL1429'
    - - :warning
      - 'Line 856: Product not found, record ignored., BaseItemCode=PWFL1430'
    - - :warning
      - 'Line 857: Product not found, record ignored., BaseItemCode=PWFL1431'
    - - :warning
      - 'Line 858: Product not found, record ignored., BaseItemCode=PWFL1432'
    - - :warning
      - 'Line 859: Product not found, record ignored., BaseItemCode=PWFL1433'
    - - :warning
      - 'Line 860: Product not found, record ignored., BaseItemCode=PWFL1435'
    - - :warning
      - 'Line 861: Product not found, record ignored., BaseItemCode=PWFL1436'
    - - :warning
      - 'Line 862: Product not found, record ignored., BaseItemCode=PWFL1438'
    - - :warning
      - 'Line 863: Product not found, record ignored., BaseItemCode=PWFL1439'
    - - :warning
      - 'Line 864: Product not found, record ignored., BaseItemCode=PWFL1441'
    - - :warning
      - 'Line 865: Product not found, record ignored., BaseItemCode=PWFL1442'
    - - :warning
      - 'Line 867: Product not found, record ignored., BaseItemCode=PWFL1444'
    - - :warning
      - 'Line 869: Product not found, record ignored., BaseItemCode=PWFL1446'
    - - :warning
      - 'Line 870: Product not found, record ignored., BaseItemCode=PWFL1447'
    - - :warning
      - 'Line 871: Product not found, record ignored., BaseItemCode=PWFL1448'
    - - :warning
      - 'Line 873: Product not found, record ignored., BaseItemCode=PWFL1450'
    - - :warning
      - 'Line 875: Product not found, record ignored., BaseItemCode=PWFL1452'
    - - :warning
      - 'Line 877: Product not found, record ignored., BaseItemCode=PWFL1454'
    - - :warning
      - 'Line 879: Product not found, record ignored., BaseItemCode=PWFL1456'
    - - :warning
      - 'Line 886: Product not found, record ignored., BaseItemCode=PWFL1463'
    - - :warning
      - 'Line 897: Product not found, record ignored., BaseItemCode=PWFLO1000'
    - - :warning
      - 'Line 898: Product not found, record ignored., BaseItemCode=PWFLO1001'
    - - :warning
      - 'Line 899: Product not found, record ignored., BaseItemCode=PWFLO1003'
    - - :warning
      - 'Line 900: Product not found, record ignored., BaseItemCode=PWFLO1006'
    - - :warning
      - 'Line 901: Product not found, record ignored., BaseItemCode=PWFLO1007'
    - - :warning
      - 'Line 902: Product not found, record ignored., BaseItemCode=PWFLO1009'
    - - :warning
      - 'Line 903: Product not found, record ignored., BaseItemCode=PWFLO1010'
    - - :warning
      - 'Line 905: Product not found, record ignored., BaseItemCode=PWFLO1012'
    - - :warning
      - 'Line 909: Product not found, record ignored., BaseItemCode=PWFLO1017'
    - - :warning
      - 'Line 919: Product not found, record ignored., BaseItemCode=RALL-10002-810'
    - - :warning
      - 'Line 1135: Product not found, record ignored., BaseItemCode=SHE032'
    - - :warning
      - 'Line 1136: Product not found, record ignored., BaseItemCode=SHE033'
    - - :warning
      - 'Line 1140: Product not found, record ignored., BaseItemCode=STA479'
    - - :warning
      - 'Line 1143: Product not found, record ignored., BaseItemCode=STA571'
    - - :warning
      - 'Line 1144: Product not found, record ignored., BaseItemCode=STA575'
    - - :warning
      - 'Line 1146: Product not found, record ignored., BaseItemCode=STA665'
    - - :warning
      - 'Line 1147: Product not found, record ignored., BaseItemCode=STA689'
    - - :warning
      - 'Line 1148: Product not found, record ignored., BaseItemCode=STA693'
    - - :warning
      - 'Line 1152: Product not found, record ignored., BaseItemCode=STA747'
    - - :warning
      - 'Line 1153: Product not found, record ignored., BaseItemCode=STA757'
    - - :warning
      - 'Line 1159: Product not found, record ignored., BaseItemCode=STA773'
    - - :warning
      - 'Line 1162: Product not found, record ignored., BaseItemCode=STA786'
    - - :warning
      - 'Line 1179: Product not found, record ignored., BaseItemCode=TA177'
    - - :warning
      - 'Line 1181: Product not found, record ignored., BaseItemCode=TA198'
    - - :warning
      - 'Line 1188: Product not found, record ignored., BaseItemCode=TA447'
    - - :warning
      - 'Line 1197: Product not found, record ignored., BaseItemCode=TA459'
    - - :warning
      - 'Line 1198: Product not found, record ignored., BaseItemCode=TA460'
    - - :warning
      - 'Line 1199: Product not found, record ignored., BaseItemCode=TA461'
    - - :warning
      - 'Line 1200: Product not found, record ignored., BaseItemCode=TA462'
    - - :warning
      - 'Line 1209: Product not found, record ignored., BaseItemCode=TA475'
    - - :warning
      - 'Line 1215: Product not found, record ignored., BaseItemCode=TA488'
    - - :warning
      - 'Line 1221: Product not found, record ignored., BaseItemCode=TA497'
    - - :warning
      - 'Line 1257: Product not found, record ignored., BaseItemCode=THR1013'
    - - :warning
      - 'Line 1263: Product not found, record ignored., BaseItemCode=VAS118'
    - - :warning
      - 'Line 1268: Product not found, record ignored., BaseItemCode=VAS201'
    - - :warning
      - 'Line 1269: Product not found, record ignored., BaseItemCode=VAS205'
    - - :warning
      - 'Line 1270: Product not found, record ignored., BaseItemCode=VAS206'
    - - :warning
      - 'Line 1274: Product not found, record ignored., BaseItemCode=VAS211'
    - - :warning
      - 'Line 1275: Product not found, record ignored., BaseItemCode=VAS228'
    - - :warning
      - 'Line 1280: Product not found, record ignored., BaseItemCode=VAS240'
    - - :warning
      - 'Line 1284: Product not found, record ignored., BaseItemCode=VAS257'
    - - :warning
      - 'Line 1289: Product not found, record ignored., BaseItemCode=VAS262'
    - - :warning
      - 'Line 1290: Product not found, record ignored., BaseItemCode=VAS272'
    - - :warning
      - 'Line 1292: Product not found, record ignored., BaseItemCode=VAS274'
    - - :warning
      - 'Line 1294: Product not found, record ignored., BaseItemCode=VAS276'
    - - :warning
      - 'Line 1295: Product not found, record ignored., BaseItemCode=VAS277'
    - - :warning
      - 'Line 1300: Product not found, record ignored., BaseItemCode=VAS283'
    - - :warning
      - 'Line 1323: Product not found, record ignored., BaseItemCode=W6287'
    - - :warning
      - 'Line 1326: Product not found, record ignored., BaseItemCode=W6440'
    - - :warning
      - 'Line 1327: Product not found, record ignored., BaseItemCode=W6471'
    - - :warning
      - 'Line 1329: Product not found, record ignored., BaseItemCode=W6486'
    - - :warning
      - 'Line 1342: Product not found, record ignored., BaseItemCode=W6701'
    - - :warning
      - 'Line 1344: Product not found, record ignored., BaseItemCode=W6706'
    - - :warning
      - 'Line 1347: Product not found, record ignored., BaseItemCode=W6713'
    - - :warning
      - 'Line 1353: Product not found, record ignored., BaseItemCode=W6730'
    - - :warning
      - 'Line 1399: Product not found, record ignored., BaseItemCode=WS117'
    - - :warning
      - 'Line 1405: Product not found, record ignored., BaseItemCode=WS129'
    - - :warning
      - 'Line 1411: Product not found, record ignored., BaseItemCode=WS135'
    - - :warning
      - 'Line 1415: Product not found, record ignored., BaseItemCode=WS139'
    - - :warning
      - 'Line 1420: Product not found, record ignored., BaseItemCode=WS144'
    - - :warning
      - 'Line 1422: Product not found, record ignored., BaseItemCode=WS146'
    - - :warning
      - 'Line 1423: Product not found, record ignored., BaseItemCode=WS147'
    - - :warning
      - 'Line 1446: Product not found, record ignored., BaseItemCode=VAS253'
    - - :warning
      - 'Line 1464: Product not found, record ignored., BaseItemCode=LPT1379EV'
    - - :warning
      - 'Line 1473: Product not found, record ignored., BaseItemCode=LPT1388EV'
    - - :warning
      - 'Line 1485: Product not found, record ignored., BaseItemCode=LIGHTCLOUD'
    - - :warning
      - 'Line 1486: Product not found, record ignored., BaseItemCode=LPC125C'
    - - :warning
      - 'Line 1487: Product not found, record ignored., BaseItemCode=LPC4255'
    - - :warning
      - 'Line 1492: Product not found, record ignored., BaseItemCode=PWFL1007'
    - - :warning
      - 'Line 1496: Product not found, record ignored., BaseItemCode=PWFL1192'
    - - :warning
      - 'Line 1497: Product not found, record ignored., BaseItemCode=PWFL1257'
    - - :warning
      - 'Line 1498: Product not found, record ignored., BaseItemCode=PWFL1310'
    - - :warning
      - 'Line 1499: Product not found, record ignored., BaseItemCode=PWFL1313'
    - - :warning
      - 'Line 1500: Product not found, record ignored., BaseItemCode=PWFL1322'
    - - :warning
      - 'Line 1502: Product not found, record ignored., BaseItemCode=PWFL1391P'
    - - :warning
      - 'Line 1503: Product not found, record ignored., BaseItemCode=PWFLX1019'
    - - :warning
      - 'Line 1601: Product not found, record ignored., BaseItemCode=VAS249'
    - - :warning
      - 'Line 1603: Product not found, record ignored., BaseItemCode=W6345'
    - - :warning
      - 'Line 1604: Product not found, record ignored., BaseItemCode=WS053'
    - - :warning
      - 'Line 1605: Product not found, record ignored., BaseItemCode=ESM-W6005'
    - - :warning
      - 'Line 1606: Product not found, record ignored., BaseItemCode=PWFL1002'
    - - :warning
      - 'Line 1607: Product not found, record ignored., BaseItemCode=PWFL1008'
    - - :warning
      - 'Line 1608: Product not found, record ignored., BaseItemCode=PWFL1011'
    - - :warning
      - 'Line 1609: Product not found, record ignored., BaseItemCode=PWFL1018'
    - - :warning
      - 'Line 1610: Product not found, record ignored., BaseItemCode=PWFL1031'
    - - :warning
      - 'Line 1612: Product not found, record ignored., BaseItemCode=PWFL1039'
    - - :warning
      - 'Line 1614: Product not found, record ignored., BaseItemCode=PWFL1049'
    - - :warning
      - 'Line 1615: Product not found, record ignored., BaseItemCode=PWFL1050'
    - - :warning
      - 'Line 1616: Product not found, record ignored., BaseItemCode=PWFL1065'
    - - :warning
      - 'Line 1617: Product not found, record ignored., BaseItemCode=PWFL1088'
    - - :warning
      - 'Line 1618: Product not found, record ignored., BaseItemCode=PWFL1090'
    - - :warning
      - 'Line 1619: Product not found, record ignored., BaseItemCode=PWFL1095'
    - - :warning
      - 'Line 1620: Product not found, record ignored., BaseItemCode=PWFL1108'
    - - :warning
      - 'Line 1621: Product not found, record ignored., BaseItemCode=PWFL1113'
    - - :warning
      - 'Line 1622: Product not found, record ignored., BaseItemCode=PWFL1145'
    - - :warning
      - 'Line 1625: Product not found, record ignored., BaseItemCode=PWFL1237'
    - - :warning
      - 'Line 1627: Product not found, record ignored., BaseItemCode=PWFL1248'
    - - :warning
      - 'Line 1628: Product not found, record ignored., BaseItemCode=PWFL1261'
    - - :warning
      - 'Line 1629: Product not found, record ignored., BaseItemCode=PWFL1294'
    - - :warning
      - 'Line 1630: Product not found, record ignored., BaseItemCode=PWFL1298'
    - - :warning
      - 'Line 1632: Product not found, record ignored., BaseItemCode=PWFL1302'
    - - :warning
      - 'Line 1633: Product not found, record ignored., BaseItemCode=PWFL1317'
    - - :warning
      - 'Line 1634: Product not found, record ignored., BaseItemCode=PWFL1326'
    - - :warning
      - 'Line 1635: Product not found, record ignored., BaseItemCode=PWFL1327'
    - - :warning
      - 'Line 1636: Product not found, record ignored., BaseItemCode=PWFL1339'
    - - :warning
      - 'Line 1637: Product not found, record ignored., BaseItemCode=PWFL1342'
    - - :warning
      - 'Line 1638: Product not found, record ignored., BaseItemCode=PWFL1346'
    - - :warning
      - 'Line 1639: Product not found, record ignored., BaseItemCode=PWFLO1008'
    - - :warning
      - 'Line 1643: Product not found, record ignored., BaseItemCode=VAS245'
    - - :warning
      - 'Line 1644: Product not found, record ignored., BaseItemCode=VAS251'
    - - :warning
      - 'Line 1646: Product not found, record ignored., BaseItemCode=LPC149'
    - - :warning
      - 'Line 1652: Product not found, record ignored., BaseItemCode=ANTISLIP912'
    - - :warning
      - 'Line 1653: Product not found, record ignored., BaseItemCode=CHA064'
    - - :warning
      - 'Line 1654: Product not found, record ignored., BaseItemCode=FLP1024'
    - - :warning
      - 'Line 1655: Product not found, record ignored., BaseItemCode=FLP1616'
    - - :warning
      - 'Line 1656: Product not found, record ignored., BaseItemCode=PWFL1407'
    - - :warning
      - 'Line 1662: Product not found, record ignored., BaseItemCode=VAS282'
    - - :warning
      - 'Line 1664: Product not found, record ignored., BaseItemCode=W6714'
    - - :warning
      - 'Line 1665: Product not found, record ignored., BaseItemCode=W6715'
    - - :warning
      - 'Line 1666: Product not found, record ignored., BaseItemCode=W6732'
    - - :warning
      - 'Line 1682: Product not found, record ignored., BaseItemCode=LPC4488'
    - - :warning
      - 'Line 1996: Product not found, record ignored., BaseItemCode=PA0062'
 |
| 2026-06-15 22:06:07 | ---
- - Portal Invoices
  - []
 |
| 2026-06-15 17:02:17 | ---
- - Inventory
  - - - :warning
      - 'Line 14: Product not found, record ignored., BaseItemCode=CHA071'
    - - :warning
      - 'Line 19: Product not found, record ignored., BaseItemCode=CHA088'
    - - :warning
      - 'Line 20: Product not found, record ignored., BaseItemCode=CHA089'
    - - :warning
      - 'Line 24: Product not found, record ignored., BaseItemCode=CHA094'
    - - :warning
      - 'Line 25: Product not found, record ignored., BaseItemCode=CHA095'
    - - :warning
      - 'Line 27: Product not found, record ignored., BaseItemCode=CHA097'
    - - :warning
      - 'Line 28: Product not found, record ignored., BaseItemCode=CHA098'
    - - :warning
      - 'Line 37: Product not found, record ignored., BaseItemCode=CL220'
    - - :warning
      - 'Line 38: Product not found, record ignored., BaseItemCode=CL239'
    - - :warning
      - 'Line 42: Product not found, record ignored., BaseItemCode=CL257'
    - - :warning
      - 'Line 76: Product not found, record ignored., BaseItemCode=LPC4058'
    - - :warning
      - 'Line 88: Product not found, record ignored., BaseItemCode=LPC4418'
    - - :warning
      - 'Line 92: Product not found, record ignored., BaseItemCode=LPC4434'
    - - :warning
      - 'Line 96: Product not found, record ignored., BaseItemCode=LPC4445'
    - - :warning
      - 'Line 98: Product not found, record ignored., BaseItemCode=LPC4454'
    - - :warning
      - 'Line 130: Product not found, record ignored., BaseItemCode=LPF3023'
    - - :warning
      - 'Line 133: Product not found, record ignored., BaseItemCode=LPF3071'
    - - :warning
      - 'Line 135: Product not found, record ignored., BaseItemCode=LPF3110'
    - - :warning
      - 'Line 136: Product not found, record ignored., BaseItemCode=LPF3111'
    - - :warning
      - 'Line 139: Product not found, record ignored., BaseItemCode=LPF3135'
    - - :warning
      - 'Line 145: Product not found, record ignored., BaseItemCode=LPF3146'
    - - :warning
      - 'Line 147: Product not found, record ignored., BaseItemCode=LPF3149'
    - - :warning
      - 'Line 151: Product not found, record ignored., BaseItemCode=LPF3153'
    - - :warning
      - 'Line 179: Product not found, record ignored., BaseItemCode=LPT1047'
    - - :warning
      - 'Line 180: Product not found, record ignored., BaseItemCode=LPT1057'
    - - :warning
      - 'Line 183: Product not found, record ignored., BaseItemCode=LPT1127'
    - - :warning
      - 'Line 186: Product not found, record ignored., BaseItemCode=LPT1159'
    - - :warning
      - 'Line 188: Product not found, record ignored., BaseItemCode=LPT1161'
    - - :warning
      - 'Line 191: Product not found, record ignored., BaseItemCode=LPT1173'
    - - :warning
      - 'Line 194: Product not found, record ignored., BaseItemCode=LPT1183'
    - - :warning
      - 'Line 203: Product not found, record ignored., BaseItemCode=LPT1216'
    - - :warning
      - 'Line 205: Product not found, record ignored., BaseItemCode=LPT1218'
    - - :warning
      - 'Line 206: Product not found, record ignored., BaseItemCode=LPT1219'
    - - :warning
      - 'Line 207: Product not found, record ignored., BaseItemCode=LPT1221'
    - - :warning
      - 'Line 208: Product not found, record ignored., BaseItemCode=LPT1222'
    - - :warning
      - 'Line 211: Product not found, record ignored., BaseItemCode=LPT1225'
    - - :warning
      - 'Line 217: Product not found, record ignored., BaseItemCode=LPT1234'
    - - :warning
      - 'Line 223: Product not found, record ignored., BaseItemCode=LPT1240'
    - - :warning
      - 'Line 224: Product not found, record ignored., BaseItemCode=LPT1241'
    - - :warning
      - 'Line 225: Product not found, record ignored., BaseItemCode=LPT1242'
    - - :warning
      - 'Line 226: Product not found, record ignored., BaseItemCode=LPT1243'
    - - :warning
      - 'Line 227: Product not found, record ignored., BaseItemCode=LPT1246'
    - - :warning
      - 'Line 228: Product not found, record ignored., BaseItemCode=LPT1249'
    - - :warning
      - 'Line 229: Product not found, record ignored., BaseItemCode=LPT1250'
    - - :warning
      - 'Line 234: Product not found, record ignored., BaseItemCode=LPT1257'
    - - :warning
      - 'Line 236: Product not found, record ignored., BaseItemCode=LPT1259'
    - - :warning
      - 'Line 245: Product not found, record ignored., BaseItemCode=LPT1268'
    - - :warning
      - 'Line 247: Product not found, record ignored., BaseItemCode=LPT1270'
    - - :warning
      - 'Line 248: Product not found, record ignored., BaseItemCode=LPT1271'
    - - :warning
      - 'Line 251: Product not found, record ignored., BaseItemCode=LPT1274'
    - - :warning
      - 'Line 252: Product not found, record ignored., BaseItemCode=LPT1275'
    - - :warning
      - 'Line 258: Product not found, record ignored., BaseItemCode=LPT1284'
    - - :warning
      - 'Line 261: Product not found, record ignored., BaseItemCode=LPT1287'
    - - :warning
      - 'Line 306: Product not found, record ignored., BaseItemCode=LPT1334'
    - - :warning
      - 'Line 333: Product not found, record ignored., BaseItemCode=LPT172'
    - - :warning
      - 'Line 334: Product not found, record ignored., BaseItemCode=LPT594'
    - - :warning
      - 'Line 336: Product not found, record ignored., BaseItemCode=LPT714'
    - - :warning
      - 'Line 337: Product not found, record ignored., BaseItemCode=LPT825'
    - - :warning
      - 'Line 338: Product not found, record ignored., BaseItemCode=LPT853'
    - - :warning
      - 'Line 339: Product not found, record ignored., BaseItemCode=LPT869'
    - - :warning
      - 'Line 340: Product not found, record ignored., BaseItemCode=LPT884'
    - - :warning
      - 'Line 341: Product not found, record ignored., BaseItemCode=LPT885'
    - - :warning
      - 'Line 343: Product not found, record ignored., BaseItemCode=LPT982'
    - - :warning
      - 'Line 344: Product not found, record ignored., BaseItemCode=MT1006'
    - - :warning
      - 'Line 347: Product not found, record ignored., BaseItemCode=MT1134'
    - - :warning
      - 'Line 348: Product not found, record ignored., BaseItemCode=MT1185'
    - - :warning
      - 'Line 350: Product not found, record ignored., BaseItemCode=MT1284'
    - - :warning
      - 'Line 360: Product not found, record ignored., BaseItemCode=MT1499'
    - - :warning
      - 'Line 366: Product not found, record ignored., BaseItemCode=MT1594'
    - - :warning
      - 'Line 371: Product not found, record ignored., BaseItemCode=MT1706'
    - - :warning
      - 'Line 377: Product not found, record ignored., BaseItemCode=MT1820'
    - - :warning
      - 'Line 383: Product not found, record ignored., BaseItemCode=MT1857'
    - - :warning
      - 'Line 403: Product not found, record ignored., BaseItemCode=MT2301'
    - - :warning
      - 'Line 404: Product not found, record ignored., BaseItemCode=MT2320'
    - - :warning
      - 'Line 424: Product not found, record ignored., BaseItemCode=MT2412'
    - - :warning
      - 'Line 432: Product not found, record ignored., BaseItemCode=MT2437'
    - - :warning
      - 'Line 433: Product not found, record ignored., BaseItemCode=MT2444'
    - - :warning
      - 'Line 438: Product not found, record ignored., BaseItemCode=MT2456'
    - - :warning
      - 'Line 439: Product not found, record ignored., BaseItemCode=MT2459'
    - - :warning
      - 'Line 442: Product not found, record ignored., BaseItemCode=MT2464'
    - - :warning
      - 'Line 443: Product not found, record ignored., BaseItemCode=MT2471'
    - - :warning
      - 'Line 448: Product not found, record ignored., BaseItemCode=MT2497'
    - - :warning
      - 'Line 459: Product not found, record ignored., BaseItemCode=MT2513'
    - - :warning
      - 'Line 470: Product not found, record ignored., BaseItemCode=MT2529'
    - - :warning
      - 'Line 472: Product not found, record ignored., BaseItemCode=MT2531'
    - - :warning
      - 'Line 479: Product not found, record ignored., BaseItemCode=MT2541'
    - - :warning
      - 'Line 493: Product not found, record ignored., BaseItemCode=MT2563'
    - - :warning
      - 'Line 495: Product not found, record ignored., BaseItemCode=MT2567'
    - - :warning
      - 'Line 503: Product not found, record ignored., BaseItemCode=MT2610'
    - - :warning
      - 'Line 504: Product not found, record ignored., BaseItemCode=MT2611'
    - - :warning
      - 'Line 509: Product not found, record ignored., BaseItemCode=MT2616'
    - - :warning
      - 'Line 515: Product not found, record ignored., BaseItemCode=MT2622'
    - - :warning
      - 'Line 517: Product not found, record ignored., BaseItemCode=MT2624'
    - - :warning
      - 'Line 519: Product not found, record ignored., BaseItemCode=MT2626'
    - - :warning
      - 'Line 530: Product not found, record ignored., BaseItemCode=MT2637'
    - - :warning
      - 'Line 531: Product not found, record ignored., BaseItemCode=MT2638'
    - - :warning
      - 'Line 535: Product not found, record ignored., BaseItemCode=MT2654'
    - - :warning
      - 'Line 598: Product not found, record ignored., BaseItemCode=MT849'
    - - :warning
      - 'Line 601: Product not found, record ignored., BaseItemCode=OL1485'
    - - :warning
      - 'Line 605: Product not found, record ignored., BaseItemCode=OL1717'
    - - :warning
      - 'Line 607: Product not found, record ignored., BaseItemCode=OL1730'
    - - :warning
      - 'Line 619: Product not found, record ignored., BaseItemCode=OL1965'
    - - :warning
      - 'Line 622: Product not found, record ignored., BaseItemCode=OL1978'
    - - :warning
      - 'Line 635: Product not found, record ignored., BaseItemCode=OL2058'
    - - :warning
      - 'Line 637: Product not found, record ignored., BaseItemCode=OL2065'
    - - :warning
      - 'Line 639: Product not found, record ignored., BaseItemCode=OL2067'
    - - :warning
      - 'Line 641: Product not found, record ignored., BaseItemCode=OL2069'
    - - :warning
      - 'Line 650: Product not found, record ignored., BaseItemCode=OL2090'
    - - :warning
      - 'Line 652: Product not found, record ignored., BaseItemCode=OL2096'
    - - :warning
      - 'Line 653: Product not found, record ignored., BaseItemCode=OL2098'
    - - :warning
      - 'Line 655: Product not found, record ignored., BaseItemCode=OL2101'
    - - :warning
      - 'Line 656: Product not found, record ignored., BaseItemCode=OL2102'
    - - :warning
      - 'Line 659: Product not found, record ignored., BaseItemCode=OL2107'
    - - :warning
      - 'Line 661: Product not found, record ignored., BaseItemCode=OL2110'
    - - :warning
      - 'Line 663: Product not found, record ignored., BaseItemCode=OL2112'
    - - :warning
      - 'Line 666: Product not found, record ignored., BaseItemCode=OL2115'
    - - :warning
      - 'Line 668: Product not found, record ignored., BaseItemCode=OL2117'
    - - :warning
      - 'Line 669: Product not found, record ignored., BaseItemCode=OL2121'
    - - :warning
      - 'Line 676: Product not found, record ignored., BaseItemCode=OL2130'
    - - :warning
      - 'Line 681: Product not found, record ignored., BaseItemCode=OL2136'
    - - :warning
      - 'Line 684: Product not found, record ignored., BaseItemCode=OL2139'
    - - :warning
      - 'Line 688: Product not found, record ignored., BaseItemCode=OL2143'
    - - :warning
      - 'Line 689: Product not found, record ignored., BaseItemCode=OL2144'
    - - :warning
      - 'Line 690: Product not found, record ignored., BaseItemCode=OL2145'
    - - :warning
      - 'Line 699: Product not found, record ignored., BaseItemCode=OL2155'
    - - :warning
      - 'Line 776: Product not found, record ignored., BaseItemCode=PF035'
    - - :warning
      - 'Line 777: Product not found, record ignored., BaseItemCode=PF043'
    - - :warning
      - 'Line 780: Product not found, record ignored., BaseItemCode=PF046'
    - - :warning
      - 'Line 782: Product not found, record ignored., BaseItemCode=PWFL1001'
    - - :warning
      - 'Line 783: Product not found, record ignored., BaseItemCode=PWFL1005'
    - - :warning
      - 'Line 784: Product not found, record ignored., BaseItemCode=PWFL1009'
    - - :warning
      - 'Line 785: Product not found, record ignored., BaseItemCode=PWFL1010'
    - - :warning
      - 'Line 786: Product not found, record ignored., BaseItemCode=PWFL1012'
    - - :warning
      - 'Line 787: Product not found, record ignored., BaseItemCode=PWFL1020'
    - - :warning
      - 'Line 789: Product not found, record ignored., BaseItemCode=PWFL1026'
    - - :warning
      - 'Line 790: Product not found, record ignored., BaseItemCode=PWFL1027'
    - - :warning
      - 'Line 791: Product not found, record ignored., BaseItemCode=PWFL1028'
    - - :warning
      - 'Line 792: Product not found, record ignored., BaseItemCode=PWFL1030'
    - - :warning
      - 'Line 793: Product not found, record ignored., BaseItemCode=PWFL1035'
    - - :warning
      - 'Line 794: Product not found, record ignored., BaseItemCode=PWFL1037'
    - - :warning
      - 'Line 795: Product not found, record ignored., BaseItemCode=PWFL1048'
    - - :warning
      - 'Line 804: Product not found, record ignored., BaseItemCode=PWFL1069'
    - - :warning
      - 'Line 805: Product not found, record ignored., BaseItemCode=PWFL1079'
    - - :warning
      - 'Line 806: Product not found, record ignored., BaseItemCode=PWFL1085'
    - - :warning
      - 'Line 810: Product not found, record ignored., BaseItemCode=PWFL1115'
    - - :warning
      - 'Line 811: Product not found, record ignored., BaseItemCode=PWFL1131'
    - - :warning
      - 'Line 812: Product not found, record ignored., BaseItemCode=PWFL1147'
    - - :warning
      - 'Line 813: Product not found, record ignored., BaseItemCode=PWFL1160'
    - - :warning
      - 'Line 814: Product not found, record ignored., BaseItemCode=PWFL1168'
    - - :warning
      - 'Line 815: Product not found, record ignored., BaseItemCode=PWFL1176'
    - - :warning
      - 'Line 816: Product not found, record ignored., BaseItemCode=PWFL1180'
    - - :warning
      - 'Line 817: Product not found, record ignored., BaseItemCode=PWFL1200'
    - - :warning
      - 'Line 819: Product not found, record ignored., BaseItemCode=PWFL1234'
    - - :warning
      - 'Line 820: Product not found, record ignored., BaseItemCode=PWFL1243'
    - - :warning
      - 'Line 822: Product not found, record ignored., BaseItemCode=PWFL1252'
    - - :warning
      - 'Line 825: Product not found, record ignored., BaseItemCode=PWFL1355'
    - - :warning
      - 'Line 826: Product not found, record ignored., BaseItemCode=PWFL1357'
    - - :warning
      - 'Line 827: Product not found, record ignored., BaseItemCode=PWFL1358'
    - - :warning
      - 'Line 829: Product not found, record ignored., BaseItemCode=PWFL1362'
    - - :warning
      - 'Line 830: Product not found, record ignored., BaseItemCode=PWFL1367'
    - - :warning
      - 'Line 831: Product not found, record ignored., BaseItemCode=PWFL1373'
    - - :warning
      - 'Line 832: Product not found, record ignored., BaseItemCode=PWFL1377'
    - - :warning
      - 'Line 833: Product not found, record ignored., BaseItemCode=PWFL1389'
    - - :warning
      - 'Line 835: Product not found, record ignored., BaseItemCode=PWFL1399'
    - - :warning
      - 'Line 837: Product not found, record ignored., BaseItemCode=PWFL1401'
    - - :warning
      - 'Line 838: Product not found, record ignored., BaseItemCode=PWFL1402'
    - - :warning
      - 'Line 839: Product not found, record ignored., BaseItemCode=PWFL1404'
    - - :warning
      - 'Line 840: Product not found, record ignored., BaseItemCode=PWFL1405'
    - - :warning
      - 'Line 841: Product not found, record ignored., BaseItemCode=PWFL1406'
    - - :warning
      - 'Line 843: Product not found, record ignored., BaseItemCode=PWFL1411'
    - - :warning
      - 'Line 844: Product not found, record ignored., BaseItemCode=PWFL1415'
    - - :warning
      - 'Line 846: Product not found, record ignored., BaseItemCode=PWFL1420'
    - - :warning
      - 'Line 847: Product not found, record ignored., BaseItemCode=PWFL1421'
    - - :warning
      - 'Line 848: Product not found, record ignored., BaseItemCode=PWFL1422'
    - - :warning
      - 'Line 851: Product not found, record ignored., BaseItemCode=PWFL1425'
    - - :warning
      - 'Line 855: Product not found, record ignored., BaseItemCode=PWFL1429'
    - - :warning
      - 'Line 856: Product not found, record ignored., BaseItemCode=PWFL1430'
    - - :warning
      - 'Line 857: Product not found, record ignored., BaseItemCode=PWFL1431'
    - - :warning
      - 'Line 858: Product not found, record ignored., BaseItemCode=PWFL1432'
    - - :warning
      - 'Line 859: Product not found, record ignored., BaseItemCode=PWFL1433'
    - - :warning
      - 'Line 860: Product not found, record ignored., BaseItemCode=PWFL1435'
    - - :warning
      - 'Line 861: Product not found, record ignored., BaseItemCode=PWFL1436'
    - - :warning
      - 'Line 862: Product not found, record ignored., BaseItemCode=PWFL1438'
    - - :warning
      - 'Line 863: Product not found, record ignored., BaseItemCode=PWFL1439'
    - - :warning
      - 'Line 864: Product not found, record ignored., BaseItemCode=PWFL1441'
    - - :warning
      - 'Line 865: Product not found, record ignored., BaseItemCode=PWFL1442'
    - - :warning
      - 'Line 867: Product not found, record ignored., BaseItemCode=PWFL1444'
    - - :warning
      - 'Line 869: Product not found, record ignored., BaseItemCode=PWFL1446'
    - - :warning
      - 'Line 870: Product not found, record ignored., BaseItemCode=PWFL1447'
    - - :warning
      - 'Line 871: Product not found, record ignored., BaseItemCode=PWFL1448'
    - - :warning
      - 'Line 873: Product not found, record ignored., BaseItemCode=PWFL1450'
    - - :warning
      - 'Line 875: Product not found, record ignored., BaseItemCode=PWFL1452'
    - - :warning
      - 'Line 877: Product not found, record ignored., BaseItemCode=PWFL1454'
    - - :warning
      - 'Line 879: Product not found, record ignored., BaseItemCode=PWFL1456'
    - - :warning
      - 'Line 886: Product not found, record ignored., BaseItemCode=PWFL1463'
    - - :warning
      - 'Line 897: Product not found, record ignored., BaseItemCode=PWFLO1000'
    - - :warning
      - 'Line 898: Product not found, record ignored., BaseItemCode=PWFLO1001'
    - - :warning
      - 'Line 899: Product not found, record ignored., BaseItemCode=PWFLO1003'
    - - :warning
      - 'Line 900: Product not found, record ignored., BaseItemCode=PWFLO1006'
    - - :warning
      - 'Line 901: Product not found, record ignored., BaseItemCode=PWFLO1007'
    - - :warning
      - 'Line 902: Product not found, record ignored., BaseItemCode=PWFLO1009'
    - - :warning
      - 'Line 903: Product not found, record ignored., BaseItemCode=PWFLO1010'
    - - :warning
      - 'Line 905: Product not found, record ignored., BaseItemCode=PWFLO1012'
    - - :warning
      - 'Line 909: Product not found, record ignored., BaseItemCode=PWFLO1017'
    - - :warning
      - 'Line 919: Product not found, record ignored., BaseItemCode=RALL-10002-810'
    - - :warning
      - 'Line 1135: Product not found, record ignored., BaseItemCode=SHE032'
    - - :warning
      - 'Line 1136: Product not found, record ignored., BaseItemCode=SHE033'
    - - :warning
      - 'Line 1140: Product not found, record ignored., BaseItemCode=STA479'
    - - :warning
      - 'Line 1143: Product not found, record ignored., BaseItemCode=STA571'
    - - :warning
      - 'Line 1144: Product not found, record ignored., BaseItemCode=STA575'
    - - :warning
      - 'Line 1146: Product not found, record ignored., BaseItemCode=STA665'
    - - :warning
      - 'Line 1147: Product not found, record ignored., BaseItemCode=STA689'
    - - :warning
      - 'Line 1148: Product not found, record ignored., BaseItemCode=STA693'
    - - :warning
      - 'Line 1152: Product not found, record ignored., BaseItemCode=STA747'
    - - :warning
      - 'Line 1153: Product not found, record ignored., BaseItemCode=STA757'
    - - :warning
      - 'Line 1159: Product not found, record ignored., BaseItemCode=STA773'
    - - :warning
      - 'Line 1162: Product not found, record ignored., BaseItemCode=STA786'
    - - :warning
      - 'Line 1179: Product not found, record ignored., BaseItemCode=TA177'
    - - :warning
      - 'Line 1181: Product not found, record ignored., BaseItemCode=TA198'
    - - :warning
      - 'Line 1188: Product not found, record ignored., BaseItemCode=TA447'
    - - :warning
      - 'Line 1197: Product not found, record ignored., BaseItemCode=TA459'
    - - :warning
      - 'Line 1198: Product not found, record ignored., BaseItemCode=TA460'
    - - :warning
      - 'Line 1199: Product not found, record ignored., BaseItemCode=TA461'
    - - :warning
      - 'Line 1200: Product not found, record ignored., BaseItemCode=TA462'
    - - :warning
      - 'Line 1209: Product not found, record ignored., BaseItemCode=TA475'
    - - :warning
      - 'Line 1215: Product not found, record ignored., BaseItemCode=TA488'
    - - :warning
      - 'Line 1221: Product not found, record ignored., BaseItemCode=TA497'
    - - :warning
      - 'Line 1257: Product not found, record ignored., BaseItemCode=THR1013'
    - - :warning
      - 'Line 1263: Product not found, record ignored., BaseItemCode=VAS118'
    - - :warning
      - 'Line 1268: Product not found, record ignored., BaseItemCode=VAS201'
    - - :warning
      - 'Line 1269: Product not found, record ignored., BaseItemCode=VAS205'
    - - :warning
      - 'Line 1270: Product not found, record ignored., BaseItemCode=VAS206'
    - - :warning
      - 'Line 1274: Product not found, record ignored., BaseItemCode=VAS211'
    - - :warning
      - 'Line 1275: Product not found, record ignored., BaseItemCode=VAS228'
    - - :warning
      - 'Line 1280: Product not found, record ignored., BaseItemCode=VAS240'
    - - :warning
      - 'Line 1284: Product not found, record ignored., BaseItemCode=VAS257'
    - - :warning
      - 'Line 1289: Product not found, record ignored., BaseItemCode=VAS262'
    - - :warning
      - 'Line 1290: Product not found, record ignored., BaseItemCode=VAS272'
    - - :warning
      - 'Line 1292: Product not found, record ignored., BaseItemCode=VAS274'
    - - :warning
      - 'Line 1294: Product not found, record ignored., BaseItemCode=VAS276'
    - - :warning
      - 'Line 1295: Product not found, record ignored., BaseItemCode=VAS277'
    - - :warning
      - 'Line 1300: Product not found, record ignored., BaseItemCode=VAS283'
    - - :warning
      - 'Line 1323: Product not found, record ignored., BaseItemCode=W6287'
    - - :warning
      - 'Line 1326: Product not found, record ignored., BaseItemCode=W6440'
    - - :warning
      - 'Line 1327: Product not found, record ignored., BaseItemCode=W6471'
    - - :warning
      - 'Line 1329: Product not found, record ignored., BaseItemCode=W6486'
    - - :warning
      - 'Line 1342: Product not found, record ignored., BaseItemCode=W6701'
    - - :warning
      - 'Line 1344: Product not found, record ignored., BaseItemCode=W6706'
    - - :warning
      - 'Line 1347: Product not found, record ignored., BaseItemCode=W6713'
    - - :warning
      - 'Line 1353: Product not found, record ignored., BaseItemCode=W6730'
    - - :warning
      - 'Line 1399: Product not found, record ignored., BaseItemCode=WS117'
    - - :warning
      - 'Line 1405: Product not found, record ignored., BaseItemCode=WS129'
    - - :warning
      - 'Line 1411: Product not found, record ignored., BaseItemCode=WS135'
    - - :warning
      - 'Line 1415: Product not found, record ignored., BaseItemCode=WS139'
    - - :warning
      - 'Line 1420: Product not found, record ignored., BaseItemCode=WS144'
    - - :warning
      - 'Line 1422: Product not found, record ignored., BaseItemCode=WS146'
    - - :warning
      - 'Line 1423: Product not found, record ignored., BaseItemCode=WS147'
    - - :warning
      - 'Line 1446: Product not found, record ignored., BaseItemCode=VAS253'
    - - :warning
      - 'Line 1464: Product not found, record ignored., BaseItemCode=LPT1379EV'
    - - :warning
      - 'Line 1473: Product not found, record ignored., BaseItemCode=LPT1388EV'
    - - :warning
      - 'Line 1485: Product not found, record ignored., BaseItemCode=LIGHTCLOUD'
    - - :warning
      - 'Line 1486: Product not found, record ignored., BaseItemCode=LPC125C'
    - - :warning
      - 'Line 1487: Product not found, record ignored., BaseItemCode=LPC4255'
    - - :warning
      - 'Line 1492: Product not found, record ignored., BaseItemCode=PWFL1007'
    - - :warning
      - 'Line 1496: Product not found, record ignored., BaseItemCode=PWFL1192'
    - - :warning
      - 'Line 1497: Product not found, record ignored., BaseItemCode=PWFL1257'
    - - :warning
      - 'Line 1498: Product not found, record ignored., BaseItemCode=PWFL1310'
    - - :warning
      - 'Line 1499: Product not found, record ignored., BaseItemCode=PWFL1313'
    - - :warning
      - 'Line 1500: Product not found, record ignored., BaseItemCode=PWFL1322'
    - - :warning
      - 'Line 1502: Product not found, record ignored., BaseItemCode=PWFL1391P'
    - - :warning
      - 'Line 1503: Product not found, record ignored., BaseItemCode=PWFLX1019'
    - - :warning
      - 'Line 1601: Product not found, record ignored., BaseItemCode=VAS249'
    - - :warning
      - 'Line 1603: Product not found, record ignored., BaseItemCode=W6345'
    - - :warning
      - 'Line 1604: Product not found, record ignored., BaseItemCode=WS053'
    - - :warning
      - 'Line 1605: Product not found, record ignored., BaseItemCode=ESM-W6005'
    - - :warning
      - 'Line 1606: Product not found, record ignored., BaseItemCode=PWFL1002'
    - - :warning
      - 'Line 1607: Product not found, record ignored., BaseItemCode=PWFL1008'
    - - :warning
      - 'Line 1608: Product not found, record ignored., BaseItemCode=PWFL1011'
    - - :warning
      - 'Line 1609: Product not found, record ignored., BaseItemCode=PWFL1018'
    - - :warning
      - 'Line 1610: Product not found, record ignored., BaseItemCode=PWFL1031'
    - - :warning
      - 'Line 1612: Product not found, record ignored., BaseItemCode=PWFL1039'
    - - :warning
      - 'Line 1614: Product not found, record ignored., BaseItemCode=PWFL1049'
    - - :warning
      - 'Line 1615: Product not found, record ignored., BaseItemCode=PWFL1050'
    - - :warning
      - 'Line 1616: Product not found, record ignored., BaseItemCode=PWFL1065'
    - - :warning
      - 'Line 1617: Product not found, record ignored., BaseItemCode=PWFL1088'
    - - :warning
      - 'Line 1618: Product not found, record ignored., BaseItemCode=PWFL1090'
    - - :warning
      - 'Line 1619: Product not found, record ignored., BaseItemCode=PWFL1095'
    - - :warning
      - 'Line 1620: Product not found, record ignored., BaseItemCode=PWFL1108'
    - - :warning
      - 'Line 1621: Product not found, record ignored., BaseItemCode=PWFL1113'
    - - :warning
      - 'Line 1622: Product not found, record ignored., BaseItemCode=PWFL1145'
    - - :warning
      - 'Line 1625: Product not found, record ignored., BaseItemCode=PWFL1237'
    - - :warning
      - 'Line 1627: Product not found, record ignored., BaseItemCode=PWFL1248'
    - - :warning
      - 'Line 1628: Product not found, record ignored., BaseItemCode=PWFL1261'
    - - :warning
      - 'Line 1629: Product not found, record ignored., BaseItemCode=PWFL1294'
    - - :warning
      - 'Line 1630: Product not found, record ignored., BaseItemCode=PWFL1298'
    - - :warning
      - 'Line 1632: Product not found, record ignored., BaseItemCode=PWFL1302'
    - - :warning
      - 'Line 1633: Product not found, record ignored., BaseItemCode=PWFL1317'
    - - :warning
      - 'Line 1634: Product not found, record ignored., BaseItemCode=PWFL1326'
    - - :warning
      - 'Line 1635: Product not found, record ignored., BaseItemCode=PWFL1327'
    - - :warning
      - 'Line 1636: Product not found, record ignored., BaseItemCode=PWFL1339'
    - - :warning
      - 'Line 1637: Product not found, record ignored., BaseItemCode=PWFL1342'
    - - :warning
      - 'Line 1638: Product not found, record ignored., BaseItemCode=PWFL1346'
    - - :warning
      - 'Line 1639: Product not found, record ignored., BaseItemCode=PWFLO1008'
    - - :warning
      - 'Line 1643: Product not found, record ignored., BaseItemCode=VAS245'
    - - :warning
      - 'Line 1644: Product not found, record ignored., BaseItemCode=VAS251'
    - - :warning
      - 'Line 1646: Product not found, record ignored., BaseItemCode=LPC149'
    - - :warning
      - 'Line 1652: Product not found, record ignored., BaseItemCode=ANTISLIP912'
    - - :warning
      - 'Line 1653: Product not found, record ignored., BaseItemCode=CHA064'
    - - :warning
      - 'Line 1654: Product not found, record ignored., BaseItemCode=FLP1024'
    - - :warning
      - 'Line 1655: Product not found, record ignored., BaseItemCode=FLP1616'
    - - :warning
      - 'Line 1656: Product not found, record ignored., BaseItemCode=PWFL1407'
    - - :warning
      - 'Line 1662: Product not found, record ignored., BaseItemCode=VAS282'
    - - :warning
      - 'Line 1664: Product not found, record ignored., BaseItemCode=W6714'
    - - :warning
      - 'Line 1665: Product not found, record ignored., BaseItemCode=W6715'
    - - :warning
      - 'Line 1666: Product not found, record ignored., BaseItemCode=W6732'
    - - :warning
      - 'Line 1682: Product not found, record ignored., BaseItemCode=LPC4488'
    - - :warning
      - 'Line 1996: Product not found, record ignored., BaseItemCode=PA0062'
 |
| 2026-06-14 22:07:05 | ---
- - Portal Invoices
  - []
 |
| 2026-06-14 17:01:22 | ---
- - Inventory
  - - - :warning
      - 'Line 14: Product not found, record ignored., BaseItemCode=CHA071'
    - - :warning
      - 'Line 19: Product not found, record ignored., BaseItemCode=CHA088'
    - - :warning
      - 'Line 20: Product not found, record ignored., BaseItemCode=CHA089'
    - - :warning
      - 'Line 24: Product not found, record ignored., BaseItemCode=CHA094'
    - - :warning
      - 'Line 25: Product not found, record ignored., BaseItemCode=CHA095'
    - - :warning
      - 'Line 27: Product not found, record ignored., BaseItemCode=CHA097'
    - - :warning
      - 'Line 28: Product not found, record ignored., BaseItemCode=CHA098'
    - - :warning
      - 'Line 37: Product not found, record ignored., BaseItemCode=CL220'
    - - :warning
      - 'Line 38: Product not found, record ignored., BaseItemCode=CL239'
    - - :warning
      - 'Line 42: Product not found, record ignored., BaseItemCode=CL257'
    - - :warning
      - 'Line 76: Product not found, record ignored., BaseItemCode=LPC4058'
    - - :warning
      - 'Line 88: Product not found, record ignored., BaseItemCode=LPC4418'
    - - :warning
      - 'Line 92: Product not found, record ignored., BaseItemCode=LPC4434'
    - - :warning
      - 'Line 96: Product not found, record ignored., BaseItemCode=LPC4445'
    - - :warning
      - 'Line 98: Product not found, record ignored., BaseItemCode=LPC4454'
    - - :warning
      - 'Line 130: Product not found, record ignored., BaseItemCode=LPF3023'
    - - :warning
      - 'Line 133: Product not found, record ignored., BaseItemCode=LPF3071'
    - - :warning
      - 'Line 135: Product not found, record ignored., BaseItemCode=LPF3110'
    - - :warning
      - 'Line 136: Product not found, record ignored., BaseItemCode=LPF3111'
    - - :warning
      - 'Line 139: Product not found, record ignored., BaseItemCode=LPF3135'
    - - :warning
      - 'Line 145: Product not found, record ignored., BaseItemCode=LPF3146'
    - - :warning
      - 'Line 147: Product not found, record ignored., BaseItemCode=LPF3149'
    - - :warning
      - 'Line 151: Product not found, record ignored., BaseItemCode=LPF3153'
    - - :warning
      - 'Line 179: Product not found, record ignored., BaseItemCode=LPT1047'
    - - :warning
      - 'Line 180: Product not found, record ignored., BaseItemCode=LPT1057'
    - - :warning
      - 'Line 183: Product not found, record ignored., BaseItemCode=LPT1127'
    - - :warning
      - 'Line 186: Product not found, record ignored., BaseItemCode=LPT1159'
    - - :warning
      - 'Line 188: Product not found, record ignored., BaseItemCode=LPT1161'
    - - :warning
      - 'Line 191: Product not found, record ignored., BaseItemCode=LPT1173'
    - - :warning
      - 'Line 194: Product not found, record ignored., BaseItemCode=LPT1183'
    - - :warning
      - 'Line 203: Product not found, record ignored., BaseItemCode=LPT1216'
    - - :warning
      - 'Line 205: Product not found, record ignored., BaseItemCode=LPT1218'
    - - :warning
      - 'Line 206: Product not found, record ignored., BaseItemCode=LPT1219'
    - - :warning
      - 'Line 207: Product not found, record ignored., BaseItemCode=LPT1221'
    - - :warning
      - 'Line 208: Product not found, record ignored., BaseItemCode=LPT1222'
    - - :warning
      - 'Line 211: Product not found, record ignored., BaseItemCode=LPT1225'
    - - :warning
      - 'Line 217: Product not found, record ignored., BaseItemCode=LPT1234'
    - - :warning
      - 'Line 223: Product not found, record ignored., BaseItemCode=LPT1240'
    - - :warning
      - 'Line 224: Product not found, record ignored., BaseItemCode=LPT1241'
    - - :warning
      - 'Line 225: Product not found, record ignored., BaseItemCode=LPT1242'
    - - :warning
      - 'Line 226: Product not found, record ignored., BaseItemCode=LPT1243'
    - - :warning
      - 'Line 227: Product not found, record ignored., BaseItemCode=LPT1246'
    - - :warning
      - 'Line 228: Product not found, record ignored., BaseItemCode=LPT1249'
    - - :warning
      - 'Line 229: Product not found, record ignored., BaseItemCode=LPT1250'
    - - :warning
      - 'Line 234: Product not found, record ignored., BaseItemCode=LPT1257'
    - - :warning
      - 'Line 236: Product not found, record ignored., BaseItemCode=LPT1259'
    - - :warning
      - 'Line 245: Product not found, record ignored., BaseItemCode=LPT1268'
    - - :warning
      - 'Line 247: Product not found, record ignored., BaseItemCode=LPT1270'
    - - :warning
      - 'Line 248: Product not found, record ignored., BaseItemCode=LPT1271'
    - - :warning
      - 'Line 251: Product not found, record ignored., BaseItemCode=LPT1274'
    - - :warning
      - 'Line 252: Product not found, record ignored., BaseItemCode=LPT1275'
    - - :warning
      - 'Line 258: Product not found, record ignored., BaseItemCode=LPT1284'
    - - :warning
      - 'Line 261: Product not found, record ignored., BaseItemCode=LPT1287'
    - - :warning
      - 'Line 306: Product not found, record ignored., BaseItemCode=LPT1334'
    - - :warning
      - 'Line 333: Product not found, record ignored., BaseItemCode=LPT172'
    - - :warning
      - 'Line 334: Product not found, record ignored., BaseItemCode=LPT594'
    - - :warning
      - 'Line 336: Product not found, record ignored., BaseItemCode=LPT714'
    - - :warning
      - 'Line 337: Product not found, record ignored., BaseItemCode=LPT825'
    - - :warning
      - 'Line 338: Product not found, record ignored., BaseItemCode=LPT853'
    - - :warning
      - 'Line 339: Product not found, record ignored., BaseItemCode=LPT869'
    - - :warning
      - 'Line 340: Product not found, record ignored., BaseItemCode=LPT884'
    - - :warning
      - 'Line 341: Product not found, record ignored., BaseItemCode=LPT885'
    - - :warning
      - 'Line 343: Product not found, record ignored., BaseItemCode=LPT982'
    - - :warning
      - 'Line 344: Product not found, record ignored., BaseItemCode=MT1006'
    - - :warning
      - 'Line 347: Product not found, record ignored., BaseItemCode=MT1134'
    - - :warning
      - 'Line 348: Product not found, record ignored., BaseItemCode=MT1185'
    - - :warning
      - 'Line 350: Product not found, record ignored., BaseItemCode=MT1284'
    - - :warning
      - 'Line 360: Product not found, record ignored., BaseItemCode=MT1499'
    - - :warning
      - 'Line 366: Product not found, record ignored., BaseItemCode=MT1594'
    - - :warning
      - 'Line 371: Product not found, record ignored., BaseItemCode=MT1706'
    - - :warning
      - 'Line 377: Product not found, record ignored., BaseItemCode=MT1820'
    - - :warning
      - 'Line 383: Product not found, record ignored., BaseItemCode=MT1857'
    - - :warning
      - 'Line 403: Product not found, record ignored., BaseItemCode=MT2301'
    - - :warning
      - 'Line 404: Product not found, record ignored., BaseItemCode=MT2320'
    - - :warning
      - 'Line 424: Product not found, record ignored., BaseItemCode=MT2412'
    - - :warning
      - 'Line 432: Product not found, record ignored., BaseItemCode=MT2437'
    - - :warning
      - 'Line 433: Product not found, record ignored., BaseItemCode=MT2444'
    - - :warning
      - 'Line 438: Product not found, record ignored., BaseItemCode=MT2456'
    - - :warning
      - 'Line 439: Product not found, record ignored., BaseItemCode=MT2459'
    - - :warning
      - 'Line 442: Product not found, record ignored., BaseItemCode=MT2464'
    - - :warning
      - 'Line 443: Product not found, record ignored., BaseItemCode=MT2471'
    - - :warning
      - 'Line 448: Product not found, record ignored., BaseItemCode=MT2497'
    - - :warning
      - 'Line 459: Product not found, record ignored., BaseItemCode=MT2513'
    - - :warning
      - 'Line 470: Product not found, record ignored., BaseItemCode=MT2529'
    - - :warning
      - 'Line 472: Product not found, record ignored., BaseItemCode=MT2531'
    - - :warning
      - 'Line 479: Product not found, record ignored., BaseItemCode=MT2541'
    - - :warning
      - 'Line 493: Product not found, record ignored., BaseItemCode=MT2563'
    - - :warning
      - 'Line 495: Product not found, record ignored., BaseItemCode=MT2567'
    - - :warning
      - 'Line 503: Product not found, record ignored., BaseItemCode=MT2610'
    - - :warning
      - 'Line 504: Product not found, record ignored., BaseItemCode=MT2611'
    - - :warning
      - 'Line 509: Product not found, record ignored., BaseItemCode=MT2616'
    - - :warning
      - 'Line 515: Product not found, record ignored., BaseItemCode=MT2622'
    - - :warning
      - 'Line 517: Product not found, record ignored., BaseItemCode=MT2624'
    - - :warning
      - 'Line 519: Product not found, record ignored., BaseItemCode=MT2626'
    - - :warning
      - 'Line 530: Product not found, record ignored., BaseItemCode=MT2637'
    - - :warning
      - 'Line 531: Product not found, record ignored., BaseItemCode=MT2638'
    - - :warning
      - 'Line 535: Product not found, record ignored., BaseItemCode=MT2654'
    - - :warning
      - 'Line 598: Product not found, record ignored., BaseItemCode=MT849'
    - - :warning
      - 'Line 601: Product not found, record ignored., BaseItemCode=OL1485'
    - - :warning
      - 'Line 605: Product not found, record ignored., BaseItemCode=OL1717'
    - - :warning
      - 'Line 607: Product not found, record ignored., BaseItemCode=OL1730'
    - - :warning
      - 'Line 619: Product not found, record ignored., BaseItemCode=OL1965'
    - - :warning
      - 'Line 622: Product not found, record ignored., BaseItemCode=OL1978'
    - - :warning
      - 'Line 635: Product not found, record ignored., BaseItemCode=OL2058'
    - - :warning
      - 'Line 637: Product not found, record ignored., BaseItemCode=OL2065'
    - - :warning
      - 'Line 639: Product not found, record ignored., BaseItemCode=OL2067'
    - - :warning
      - 'Line 641: Product not found, record ignored., BaseItemCode=OL2069'
    - - :warning
      - 'Line 650: Product not found, record ignored., BaseItemCode=OL2090'
    - - :warning
      - 'Line 652: Product not found, record ignored., BaseItemCode=OL2096'
    - - :warning
      - 'Line 653: Product not found, record ignored., BaseItemCode=OL2098'
    - - :warning
      - 'Line 655: Product not found, record ignored., BaseItemCode=OL2101'
    - - :warning
      - 'Line 656: Product not found, record ignored., BaseItemCode=OL2102'
    - - :warning
      - 'Line 659: Product not found, record ignored., BaseItemCode=OL2107'
    - - :warning
      - 'Line 661: Product not found, record ignored., BaseItemCode=OL2110'
    - - :warning
      - 'Line 663: Product not found, record ignored., BaseItemCode=OL2112'
    - - :warning
      - 'Line 666: Product not found, record ignored., BaseItemCode=OL2115'
    - - :warning
      - 'Line 668: Product not found, record ignored., BaseItemCode=OL2117'
    - - :warning
      - 'Line 669: Product not found, record ignored., BaseItemCode=OL2121'
    - - :warning
      - 'Line 676: Product not found, record ignored., BaseItemCode=OL2130'
    - - :warning
      - 'Line 681: Product not found, record ignored., BaseItemCode=OL2136'
    - - :warning
      - 'Line 684: Product not found, record ignored., BaseItemCode=OL2139'
    - - :warning
      - 'Line 688: Product not found, record ignored., BaseItemCode=OL2143'
    - - :warning
      - 'Line 689: Product not found, record ignored., BaseItemCode=OL2144'
    - - :warning
      - 'Line 690: Product not found, record ignored., BaseItemCode=OL2145'
    - - :warning
      - 'Line 699: Product not found, record ignored., BaseItemCode=OL2155'
    - - :warning
      - 'Line 776: Product not found, record ignored., BaseItemCode=PF035'
    - - :warning
      - 'Line 777: Product not found, record ignored., BaseItemCode=PF043'
    - - :warning
      - 'Line 780: Product not found, record ignored., BaseItemCode=PF046'
    - - :warning
      - 'Line 782: Product not found, record ignored., BaseItemCode=PWFL1001'
    - - :warning
      - 'Line 783: Product not found, record ignored., BaseItemCode=PWFL1005'
    - - :warning
      - 'Line 784: Product not found, record ignored., BaseItemCode=PWFL1009'
    - - :warning
      - 'Line 785: Product not found, record ignored., BaseItemCode=PWFL1010'
    - - :warning
      - 'Line 786: Product not found, record ignored., BaseItemCode=PWFL1012'
    - - :warning
      - 'Line 787: Product not found, record ignored., BaseItemCode=PWFL1020'
    - - :warning
      - 'Line 789: Product not found, record ignored., BaseItemCode=PWFL1026'
    - - :warning
      - 'Line 790: Product not found, record ignored., BaseItemCode=PWFL1027'
    - - :warning
      - 'Line 791: Product not found, record ignored., BaseItemCode=PWFL1028'
    - - :warning
      - 'Line 792: Product not found, record ignored., BaseItemCode=PWFL1030'
    - - :warning
      - 'Line 793: Product not found, record ignored., BaseItemCode=PWFL1035'
    - - :warning
      - 'Line 794: Product not found, record ignored., BaseItemCode=PWFL1037'
    - - :warning
      - 'Line 795: Product not found, record ignored., BaseItemCode=PWFL1048'
    - - :warning
      - 'Line 804: Product not found, record ignored., BaseItemCode=PWFL1069'
    - - :warning
      - 'Line 805: Product not found, record ignored., BaseItemCode=PWFL1079'
    - - :warning
      - 'Line 806: Product not found, record ignored., BaseItemCode=PWFL1085'
    - - :warning
      - 'Line 810: Product not found, record ignored., BaseItemCode=PWFL1115'
    - - :warning
      - 'Line 811: Product not found, record ignored., BaseItemCode=PWFL1131'
    - - :warning
      - 'Line 812: Product not found, record ignored., BaseItemCode=PWFL1147'
    - - :warning
      - 'Line 813: Product not found, record ignored., BaseItemCode=PWFL1160'
    - - :warning
      - 'Line 814: Product not found, record ignored., BaseItemCode=PWFL1168'
    - - :warning
      - 'Line 815: Product not found, record ignored., BaseItemCode=PWFL1176'
    - - :warning
      - 'Line 816: Product not found, record ignored., BaseItemCode=PWFL1180'
    - - :warning
      - 'Line 817: Product not found, record ignored., BaseItemCode=PWFL1200'
    - - :warning
      - 'Line 819: Product not found, record ignored., BaseItemCode=PWFL1234'
    - - :warning
      - 'Line 820: Product not found, record ignored., BaseItemCode=PWFL1243'
    - - :warning
      - 'Line 822: Product not found, record ignored., BaseItemCode=PWFL1252'
    - - :warning
      - 'Line 825: Product not found, record ignored., BaseItemCode=PWFL1355'
    - - :warning
      - 'Line 826: Product not found, record ignored., BaseItemCode=PWFL1357'
    - - :warning
      - 'Line 827: Product not found, record ignored., BaseItemCode=PWFL1358'
    - - :warning
      - 'Line 829: Product not found, record ignored., BaseItemCode=PWFL1362'
    - - :warning
      - 'Line 830: Product not found, record ignored., BaseItemCode=PWFL1367'
    - - :warning
      - 'Line 831: Product not found, record ignored., BaseItemCode=PWFL1373'
    - - :warning
      - 'Line 832: Product not found, record ignored., BaseItemCode=PWFL1377'
    - - :warning
      - 'Line 833: Product not found, record ignored., BaseItemCode=PWFL1389'
    - - :warning
      - 'Line 835: Product not found, record ignored., BaseItemCode=PWFL1399'
    - - :warning
      - 'Line 837: Product not found, record ignored., BaseItemCode=PWFL1401'
    - - :warning
      - 'Line 838: Product not found, record ignored., BaseItemCode=PWFL1402'
    - - :warning
      - 'Line 839: Product not found, record ignored., BaseItemCode=PWFL1404'
    - - :warning
      - 'Line 840: Product not found, record ignored., BaseItemCode=PWFL1405'
    - - :warning
      - 'Line 841: Product not found, record ignored., BaseItemCode=PWFL1406'
    - - :warning
      - 'Line 843: Product not found, record ignored., BaseItemCode=PWFL1411'
    - - :warning
      - 'Line 844: Product not found, record ignored., BaseItemCode=PWFL1415'
    - - :warning
      - 'Line 846: Product not found, record ignored., BaseItemCode=PWFL1420'
    - - :warning
      - 'Line 847: Product not found, record ignored., BaseItemCode=PWFL1421'
    - - :warning
      - 'Line 848: Product not found, record ignored., BaseItemCode=PWFL1422'
    - - :warning
      - 'Line 851: Product not found, record ignored., BaseItemCode=PWFL1425'
    - - :warning
      - 'Line 855: Product not found, record ignored., BaseItemCode=PWFL1429'
    - - :warning
      - 'Line 856: Product not found, record ignored., BaseItemCode=PWFL1430'
    - - :warning
      - 'Line 857: Product not found, record ignored., BaseItemCode=PWFL1431'
    - - :warning
      - 'Line 858: Product not found, record ignored., BaseItemCode=PWFL1432'
    - - :warning
      - 'Line 859: Product not found, record ignored., BaseItemCode=PWFL1433'
    - - :warning
      - 'Line 860: Product not found, record ignored., BaseItemCode=PWFL1435'
    - - :warning
      - 'Line 861: Product not found, record ignored., BaseItemCode=PWFL1436'
    - - :warning
      - 'Line 862: Product not found, record ignored., BaseItemCode=PWFL1438'
    - - :warning
      - 'Line 863: Product not found, record ignored., BaseItemCode=PWFL1439'
    - - :warning
      - 'Line 864: Product not found, record ignored., BaseItemCode=PWFL1441'
    - - :warning
      - 'Line 865: Product not found, record ignored., BaseItemCode=PWFL1442'
    - - :warning
      - 'Line 867: Product not found, record ignored., BaseItemCode=PWFL1444'
    - - :warning
      - 'Line 869: Product not found, record ignored., BaseItemCode=PWFL1446'
    - - :warning
      - 'Line 870: Product not found, record ignored., BaseItemCode=PWFL1447'
    - - :warning
      - 'Line 871: Product not found, record ignored., BaseItemCode=PWFL1448'
    - - :warning
      - 'Line 873: Product not found, record ignored., BaseItemCode=PWFL1450'
    - - :warning
      - 'Line 875: Product not found, record ignored., BaseItemCode=PWFL1452'
    - - :warning
      - 'Line 877: Product not found, record ignored., BaseItemCode=PWFL1454'
    - - :warning
      - 'Line 879: Product not found, record ignored., BaseItemCode=PWFL1456'
    - - :warning
      - 'Line 886: Product not found, record ignored., BaseItemCode=PWFL1463'
    - - :warning
      - 'Line 897: Product not found, record ignored., BaseItemCode=PWFLO1000'
    - - :warning
      - 'Line 898: Product not found, record ignored., BaseItemCode=PWFLO1001'
    - - :warning
      - 'Line 899: Product not found, record ignored., BaseItemCode=PWFLO1003'
    - - :warning
      - 'Line 900: Product not found, record ignored., BaseItemCode=PWFLO1006'
    - - :warning
      - 'Line 901: Product not found, record ignored., BaseItemCode=PWFLO1007'
    - - :warning
      - 'Line 902: Product not found, record ignored., BaseItemCode=PWFLO1009'
    - - :warning
      - 'Line 903: Product not found, record ignored., BaseItemCode=PWFLO1010'
    - - :warning
      - 'Line 905: Product not found, record ignored., BaseItemCode=PWFLO1012'
    - - :warning
      - 'Line 909: Product not found, record ignored., BaseItemCode=PWFLO1017'
    - - :warning
      - 'Line 919: Product not found, record ignored., BaseItemCode=RALL-10002-810'
    - - :warning
      - 'Line 1135: Product not found, record ignored., BaseItemCode=SHE032'
    - - :warning
      - 'Line 1136: Product not found, record ignored., BaseItemCode=SHE033'
    - - :warning
      - 'Line 1140: Product not found, record ignored., BaseItemCode=STA479'
    - - :warning
      - 'Line 1143: Product not found, record ignored., BaseItemCode=STA571'
    - - :warning
      - 'Line 1144: Product not found, record ignored., BaseItemCode=STA575'
    - - :warning
      - 'Line 1146: Product not found, record ignored., BaseItemCode=STA665'
    - - :warning
      - 'Line 1147: Product not found, record ignored., BaseItemCode=STA689'
    - - :warning
      - 'Line 1148: Product not found, record ignored., BaseItemCode=STA693'
    - - :warning
      - 'Line 1152: Product not found, record ignored., BaseItemCode=STA747'
    - - :warning
      - 'Line 1153: Product not found, record ignored., BaseItemCode=STA757'
    - - :warning
      - 'Line 1159: Product not found, record ignored., BaseItemCode=STA773'
    - - :warning
      - 'Line 1162: Product not found, record ignored., BaseItemCode=STA786'
    - - :warning
      - 'Line 1179: Product not found, record ignored., BaseItemCode=TA177'
    - - :warning
      - 'Line 1181: Product not found, record ignored., BaseItemCode=TA198'
    - - :warning
      - 'Line 1188: Product not found, record ignored., BaseItemCode=TA447'
    - - :warning
      - 'Line 1197: Product not found, record ignored., BaseItemCode=TA459'
    - - :warning
      - 'Line 1198: Product not found, record ignored., BaseItemCode=TA460'
    - - :warning
      - 'Line 1199: Product not found, record ignored., BaseItemCode=TA461'
    - - :warning
      - 'Line 1200: Product not found, record ignored., BaseItemCode=TA462'
    - - :warning
      - 'Line 1209: Product not found, record ignored., BaseItemCode=TA475'
    - - :warning
      - 'Line 1215: Product not found, record ignored., BaseItemCode=TA488'
    - - :warning
      - 'Line 1221: Product not found, record ignored., BaseItemCode=TA497'
    - - :warning
      - 'Line 1257: Product not found, record ignored., BaseItemCode=THR1013'
    - - :warning
      - 'Line 1263: Product not found, record ignored., BaseItemCode=VAS118'
    - - :warning
      - 'Line 1268: Product not found, record ignored., BaseItemCode=VAS201'
    - - :warning
      - 'Line 1269: Product not found, record ignored., BaseItemCode=VAS205'
    - - :warning
      - 'Line 1270: Product not found, record ignored., BaseItemCode=VAS206'
    - - :warning
      - 'Line 1274: Product not found, record ignored., BaseItemCode=VAS211'
    - - :warning
      - 'Line 1275: Product not found, record ignored., BaseItemCode=VAS228'
    - - :warning
      - 'Line 1280: Product not found, record ignored., BaseItemCode=VAS240'
    - - :warning
      - 'Line 1284: Product not found, record ignored., BaseItemCode=VAS257'
    - - :warning
      - 'Line 1289: Product not found, record ignored., BaseItemCode=VAS262'
    - - :warning
      - 'Line 1290: Product not found, record ignored., BaseItemCode=VAS272'
    - - :warning
      - 'Line 1292: Product not found, record ignored., BaseItemCode=VAS274'
    - - :warning
      - 'Line 1294: Product not found, record ignored., BaseItemCode=VAS276'
    - - :warning
      - 'Line 1295: Product not found, record ignored., BaseItemCode=VAS277'
    - - :warning
      - 'Line 1300: Product not found, record ignored., BaseItemCode=VAS283'
    - - :warning
      - 'Line 1323: Product not found, record ignored., BaseItemCode=W6287'
    - - :warning
      - 'Line 1326: Product not found, record ignored., BaseItemCode=W6440'
    - - :warning
      - 'Line 1327: Product not found, record ignored., BaseItemCode=W6471'
    - - :warning
      - 'Line 1329: Product not found, record ignored., BaseItemCode=W6486'
    - - :warning
      - 'Line 1342: Product not found, record ignored., BaseItemCode=W6701'
    - - :warning
      - 'Line 1344: Product not found, record ignored., BaseItemCode=W6706'
    - - :warning
      - 'Line 1347: Product not found, record ignored., BaseItemCode=W6713'
    - - :warning
      - 'Line 1353: Product not found, record ignored., BaseItemCode=W6730'
    - - :warning
      - 'Line 1399: Product not found, record ignored., BaseItemCode=WS117'
    - - :warning
      - 'Line 1405: Product not found, record ignored., BaseItemCode=WS129'
    - - :warning
      - 'Line 1411: Product not found, record ignored., BaseItemCode=WS135'
    - - :warning
      - 'Line 1415: Product not found, record ignored., BaseItemCode=WS139'
    - - :warning
      - 'Line 1420: Product not found, record ignored., BaseItemCode=WS144'
    - - :warning
      - 'Line 1422: Product not found, record ignored., BaseItemCode=WS146'
    - - :warning
      - 'Line 1423: Product not found, record ignored., BaseItemCode=WS147'
    - - :warning
      - 'Line 1446: Product not found, record ignored., BaseItemCode=VAS253'
    - - :warning
      - 'Line 1464: Product not found, record ignored., BaseItemCode=LPT1379EV'
    - - :warning
      - 'Line 1473: Product not found, record ignored., BaseItemCode=LPT1388EV'
    - - :warning
      - 'Line 1485: Product not found, record ignored., BaseItemCode=LIGHTCLOUD'
    - - :warning
      - 'Line 1486: Product not found, record ignored., BaseItemCode=LPC125C'
    - - :warning
      - 'Line 1487: Product not found, record ignored., BaseItemCode=LPC4255'
    - - :warning
      - 'Line 1492: Product not found, record ignored., BaseItemCode=PWFL1007'
    - - :warning
      - 'Line 1496: Product not found, record ignored., BaseItemCode=PWFL1192'
    - - :warning
      - 'Line 1497: Product not found, record ignored., BaseItemCode=PWFL1257'
    - - :warning
      - 'Line 1498: Product not found, record ignored., BaseItemCode=PWFL1310'
    - - :warning
      - 'Line 1499: Product not found, record ignored., BaseItemCode=PWFL1313'
    - - :warning
      - 'Line 1500: Product not found, record ignored., BaseItemCode=PWFL1322'
    - - :warning
      - 'Line 1502: Product not found, record ignored., BaseItemCode=PWFL1391P'
    - - :warning
      - 'Line 1503: Product not found, record ignored., BaseItemCode=PWFLX1019'
    - - :warning
      - 'Line 1601: Product not found, record ignored., BaseItemCode=VAS249'
    - - :warning
      - 'Line 1603: Product not found, record ignored., BaseItemCode=W6345'
    - - :warning
      - 'Line 1604: Product not found, record ignored., BaseItemCode=WS053'
    - - :warning
      - 'Line 1605: Product not found, record ignored., BaseItemCode=ESM-W6005'
    - - :warning
      - 'Line 1606: Product not found, record ignored., BaseItemCode=PWFL1002'
    - - :warning
      - 'Line 1607: Product not found, record ignored., BaseItemCode=PWFL1008'
    - - :warning
      - 'Line 1608: Product not found, record ignored., BaseItemCode=PWFL1011'
    - - :warning
      - 'Line 1609: Product not found, record ignored., BaseItemCode=PWFL1018'
    - - :warning
      - 'Line 1610: Product not found, record ignored., BaseItemCode=PWFL1031'
    - - :warning
      - 'Line 1612: Product not found, record ignored., BaseItemCode=PWFL1039'
    - - :warning
      - 'Line 1614: Product not found, record ignored., BaseItemCode=PWFL1049'
    - - :warning
      - 'Line 1615: Product not found, record ignored., BaseItemCode=PWFL1050'
    - - :warning
      - 'Line 1616: Product not found, record ignored., BaseItemCode=PWFL1065'
    - - :warning
      - 'Line 1617: Product not found, record ignored., BaseItemCode=PWFL1088'
    - - :warning
      - 'Line 1618: Product not found, record ignored., BaseItemCode=PWFL1090'
    - - :warning
      - 'Line 1619: Product not found, record ignored., BaseItemCode=PWFL1095'
    - - :warning
      - 'Line 1620: Product not found, record ignored., BaseItemCode=PWFL1108'
    - - :warning
      - 'Line 1621: Product not found, record ignored., BaseItemCode=PWFL1113'
    - - :warning
      - 'Line 1622: Product not found, record ignored., BaseItemCode=PWFL1145'
    - - :warning
      - 'Line 1625: Product not found, record ignored., BaseItemCode=PWFL1237'
    - - :warning
      - 'Line 1627: Product not found, record ignored., BaseItemCode=PWFL1248'
    - - :warning
      - 'Line 1628: Product not found, record ignored., BaseItemCode=PWFL1261'
    - - :warning
      - 'Line 1629: Product not found, record ignored., BaseItemCode=PWFL1294'
    - - :warning
      - 'Line 1630: Product not found, record ignored., BaseItemCode=PWFL1298'
    - - :warning
      - 'Line 1632: Product not found, record ignored., BaseItemCode=PWFL1302'
    - - :warning
      - 'Line 1633: Product not found, record ignored., BaseItemCode=PWFL1317'
    - - :warning
      - 'Line 1634: Product not found, record ignored., BaseItemCode=PWFL1326'
    - - :warning
      - 'Line 1635: Product not found, record ignored., BaseItemCode=PWFL1327'
    - - :warning
      - 'Line 1636: Product not found, record ignored., BaseItemCode=PWFL1339'
    - - :warning
      - 'Line 1637: Product not found, record ignored., BaseItemCode=PWFL1342'
    - - :warning
      - 'Line 1638: Product not found, record ignored., BaseItemCode=PWFL1346'
    - - :warning
      - 'Line 1639: Product not found, record ignored., BaseItemCode=PWFLO1008'
    - - :warning
      - 'Line 1643: Product not found, record ignored., BaseItemCode=VAS245'
    - - :warning
      - 'Line 1644: Product not found, record ignored., BaseItemCode=VAS251'
    - - :warning
      - 'Line 1646: Product not found, record ignored., BaseItemCode=LPC149'
    - - :warning
      - 'Line 1652: Product not found, record ignored., BaseItemCode=ANTISLIP912'
    - - :warning
      - 'Line 1653: Product not found, record ignored., BaseItemCode=CHA064'
    - - :warning
      - 'Line 1654: Product not found, record ignored., BaseItemCode=FLP1024'
    - - :warning
      - 'Line 1655: Product not found, record ignored., BaseItemCode=FLP1616'
    - - :warning
      - 'Line 1656: Product not found, record ignored., BaseItemCode=PWFL1407'
    - - :warning
      - 'Line 1662: Product not found, record ignored., BaseItemCode=VAS282'
    - - :warning
      - 'Line 1664: Product not found, record ignored., BaseItemCode=W6714'
    - - :warning
      - 'Line 1665: Product not found, record ignored., BaseItemCode=W6715'
    - - :warning
      - 'Line 1666: Product not found, record ignored., BaseItemCode=W6732'
    - - :warning
      - 'Line 1682: Product not found, record ignored., BaseItemCode=LPC4488'
    - - :warning
      - 'Line 1996: Product not found, record ignored., BaseItemCode=PA0062'
 |
| 2026-06-13 22:06:05 | ---
- - Portal Invoices
  - []
 |
| 2026-06-13 17:03:20 | ---
- - Inventory
  - - - :warning
      - 'Line 14: Product not found, record ignored., BaseItemCode=CHA071'
    - - :warning
      - 'Line 19: Product not found, record ignored., BaseItemCode=CHA088'
    - - :warning
      - 'Line 20: Product not found, record ignored., BaseItemCode=CHA089'
    - - :warning
      - 'Line 24: Product not found, record ignored., BaseItemCode=CHA094'
    - - :warning
      - 'Line 25: Product not found, record ignored., BaseItemCode=CHA095'
    - - :warning
      - 'Line 27: Product not found, record ignored., BaseItemCode=CHA097'
    - - :warning
      - 'Line 28: Product not found, record ignored., BaseItemCode=CHA098'
    - - :warning
      - 'Line 37: Product not found, record ignored., BaseItemCode=CL220'
    - - :warning
      - 'Line 38: Product not found, record ignored., BaseItemCode=CL239'
    - - :warning
      - 'Line 42: Product not found, record ignored., BaseItemCode=CL257'
    - - :warning
      - 'Line 76: Product not found, record ignored., BaseItemCode=LPC4058'
    - - :warning
      - 'Line 88: Product not found, record ignored., BaseItemCode=LPC4418'
    - - :warning
      - 'Line 92: Product not found, record ignored., BaseItemCode=LPC4434'
    - - :warning
      - 'Line 96: Product not found, record ignored., BaseItemCode=LPC4445'
    - - :warning
      - 'Line 98: Product not found, record ignored., BaseItemCode=LPC4454'
    - - :warning
      - 'Line 130: Product not found, record ignored., BaseItemCode=LPF3023'
    - - :warning
      - 'Line 133: Product not found, record ignored., BaseItemCode=LPF3071'
    - - :warning
      - 'Line 135: Product not found, record ignored., BaseItemCode=LPF3110'
    - - :warning
      - 'Line 136: Product not found, record ignored., BaseItemCode=LPF3111'
    - - :warning
      - 'Line 139: Product not found, record ignored., BaseItemCode=LPF3135'
    - - :warning
      - 'Line 145: Product not found, record ignored., BaseItemCode=LPF3146'
    - - :warning
      - 'Line 147: Product not found, record ignored., BaseItemCode=LPF3149'
    - - :warning
      - 'Line 151: Product not found, record ignored., BaseItemCode=LPF3153'
    - - :warning
      - 'Line 179: Product not found, record ignored., BaseItemCode=LPT1047'
    - - :warning
      - 'Line 180: Product not found, record ignored., BaseItemCode=LPT1057'
    - - :warning
      - 'Line 183: Product not found, record ignored., BaseItemCode=LPT1127'
    - - :warning
      - 'Line 186: Product not found, record ignored., BaseItemCode=LPT1159'
    - - :warning
      - 'Line 188: Product not found, record ignored., BaseItemCode=LPT1161'
    - - :warning
      - 'Line 191: Product not found, record ignored., BaseItemCode=LPT1173'
    - - :warning
      - 'Line 194: Product not found, record ignored., BaseItemCode=LPT1183'
    - - :warning
      - 'Line 203: Product not found, record ignored., BaseItemCode=LPT1216'
    - - :warning
      - 'Line 205: Product not found, record ignored., BaseItemCode=LPT1218'
    - - :warning
      - 'Line 206: Product not found, record ignored., BaseItemCode=LPT1219'
    - - :warning
      - 'Line 207: Product not found, record ignored., BaseItemCode=LPT1221'
    - - :warning
      - 'Line 208: Product not found, record ignored., BaseItemCode=LPT1222'
    - - :warning
      - 'Line 211: Product not found, record ignored., BaseItemCode=LPT1225'
    - - :warning
      - 'Line 217: Product not found, record ignored., BaseItemCode=LPT1234'
    - - :warning
      - 'Line 223: Product not found, record ignored., BaseItemCode=LPT1240'
    - - :warning
      - 'Line 224: Product not found, record ignored., BaseItemCode=LPT1241'
    - - :warning
      - 'Line 225: Product not found, record ignored., BaseItemCode=LPT1242'
    - - :warning
      - 'Line 226: Product not found, record ignored., BaseItemCode=LPT1243'
    - - :warning
      - 'Line 227: Product not found, record ignored., BaseItemCode=LPT1246'
    - - :warning
      - 'Line 228: Product not found, record ignored., BaseItemCode=LPT1249'
    - - :warning
      - 'Line 229: Product not found, record ignored., BaseItemCode=LPT1250'
    - - :warning
      - 'Line 234: Product not found, record ignored., BaseItemCode=LPT1257'
    - - :warning
      - 'Line 236: Product not found, record ignored., BaseItemCode=LPT1259'
    - - :warning
      - 'Line 245: Product not found, record ignored., BaseItemCode=LPT1268'
    - - :warning
      - 'Line 247: Product not found, record ignored., BaseItemCode=LPT1270'
    - - :warning
      - 'Line 248: Product not found, record ignored., BaseItemCode=LPT1271'
    - - :warning
      - 'Line 251: Product not found, record ignored., BaseItemCode=LPT1274'
    - - :warning
      - 'Line 252: Product not found, record ignored., BaseItemCode=LPT1275'
    - - :warning
      - 'Line 258: Product not found, record ignored., BaseItemCode=LPT1284'
    - - :warning
      - 'Line 261: Product not found, record ignored., BaseItemCode=LPT1287'
    - - :warning
      - 'Line 306: Product not found, record ignored., BaseItemCode=LPT1334'
    - - :warning
      - 'Line 333: Product not found, record ignored., BaseItemCode=LPT172'
    - - :warning
      - 'Line 334: Product not found, record ignored., BaseItemCode=LPT594'
    - - :warning
      - 'Line 336: Product not found, record ignored., BaseItemCode=LPT714'
    - - :warning
      - 'Line 337: Product not found, record ignored., BaseItemCode=LPT825'
    - - :warning
      - 'Line 338: Product not found, record ignored., BaseItemCode=LPT853'
    - - :warning
      - 'Line 339: Product not found, record ignored., BaseItemCode=LPT869'
    - - :warning
      - 'Line 340: Product not found, record ignored., BaseItemCode=LPT884'
    - - :warning
      - 'Line 341: Product not found, record ignored., BaseItemCode=LPT885'
    - - :warning
      - 'Line 343: Product not found, record ignored., BaseItemCode=LPT982'
    - - :warning
      - 'Line 344: Product not found, record ignored., BaseItemCode=MT1006'
    - - :warning
      - 'Line 347: Product not found, record ignored., BaseItemCode=MT1134'
    - - :warning
      - 'Line 348: Product not found, record ignored., BaseItemCode=MT1185'
    - - :warning
      - 'Line 350: Product not found, record ignored., BaseItemCode=MT1284'
    - - :warning
      - 'Line 360: Product not found, record ignored., BaseItemCode=MT1499'
    - - :warning
      - 'Line 366: Product not found, record ignored., BaseItemCode=MT1594'
    - - :warning
      - 'Line 371: Product not found, record ignored., BaseItemCode=MT1706'
    - - :warning
      - 'Line 377: Product not found, record ignored., BaseItemCode=MT1820'
    - - :warning
      - 'Line 383: Product not found, record ignored., BaseItemCode=MT1857'
    - - :warning
      - 'Line 403: Product not found, record ignored., BaseItemCode=MT2301'
    - - :warning
      - 'Line 404: Product not found, record ignored., BaseItemCode=MT2320'
    - - :warning
      - 'Line 424: Product not found, record ignored., BaseItemCode=MT2412'
    - - :warning
      - 'Line 432: Product not found, record ignored., BaseItemCode=MT2437'
    - - :warning
      - 'Line 433: Product not found, record ignored., BaseItemCode=MT2444'
    - - :warning
      - 'Line 438: Product not found, record ignored., BaseItemCode=MT2456'
    - - :warning
      - 'Line 439: Product not found, record ignored., BaseItemCode=MT2459'
    - - :warning
      - 'Line 442: Product not found, record ignored., BaseItemCode=MT2464'
    - - :warning
      - 'Line 443: Product not found, record ignored., BaseItemCode=MT2471'
    - - :warning
      - 'Line 448: Product not found, record ignored., BaseItemCode=MT2497'
    - - :warning
      - 'Line 459: Product not found, record ignored., BaseItemCode=MT2513'
    - - :warning
      - 'Line 470: Product not found, record ignored., BaseItemCode=MT2529'
    - - :warning
      - 'Line 472: Product not found, record ignored., BaseItemCode=MT2531'
    - - :warning
      - 'Line 479: Product not found, record ignored., BaseItemCode=MT2541'
    - - :warning
      - 'Line 493: Product not found, record ignored., BaseItemCode=MT2563'
    - - :warning
      - 'Line 495: Product not found, record ignored., BaseItemCode=MT2567'
    - - :warning
      - 'Line 503: Product not found, record ignored., BaseItemCode=MT2610'
    - - :warning
      - 'Line 504: Product not found, record ignored., BaseItemCode=MT2611'
    - - :warning
      - 'Line 509: Product not found, record ignored., BaseItemCode=MT2616'
    - - :warning
      - 'Line 515: Product not found, record ignored., BaseItemCode=MT2622'
    - - :warning
      - 'Line 517: Product not found, record ignored., BaseItemCode=MT2624'
    - - :warning
      - 'Line 519: Product not found, record ignored., BaseItemCode=MT2626'
    - - :warning
      - 'Line 530: Product not found, record ignored., BaseItemCode=MT2637'
    - - :warning
      - 'Line 531: Product not found, record ignored., BaseItemCode=MT2638'
    - - :warning
      - 'Line 535: Product not found, record ignored., BaseItemCode=MT2654'
    - - :warning
      - 'Line 598: Product not found, record ignored., BaseItemCode=MT849'
    - - :warning
      - 'Line 601: Product not found, record ignored., BaseItemCode=OL1485'
    - - :warning
      - 'Line 605: Product not found, record ignored., BaseItemCode=OL1717'
    - - :warning
      - 'Line 607: Product not found, record ignored., BaseItemCode=OL1730'
    - - :warning
      - 'Line 619: Product not found, record ignored., BaseItemCode=OL1965'
    - - :warning
      - 'Line 622: Product not found, record ignored., BaseItemCode=OL1978'
    - - :warning
      - 'Line 635: Product not found, record ignored., BaseItemCode=OL2058'
    - - :warning
      - 'Line 637: Product not found, record ignored., BaseItemCode=OL2065'
    - - :warning
      - 'Line 639: Product not found, record ignored., BaseItemCode=OL2067'
    - - :warning
      - 'Line 641: Product not found, record ignored., BaseItemCode=OL2069'
    - - :warning
      - 'Line 650: Product not found, record ignored., BaseItemCode=OL2090'
    - - :warning
      - 'Line 652: Product not found, record ignored., BaseItemCode=OL2096'
    - - :warning
      - 'Line 653: Product not found, record ignored., BaseItemCode=OL2098'
    - - :warning
      - 'Line 655: Product not found, record ignored., BaseItemCode=OL2101'
    - - :warning
      - 'Line 656: Product not found, record ignored., BaseItemCode=OL2102'
    - - :warning
      - 'Line 659: Product not found, record ignored., BaseItemCode=OL2107'
    - - :warning
      - 'Line 661: Product not found, record ignored., BaseItemCode=OL2110'
    - - :warning
      - 'Line 663: Product not found, record ignored., BaseItemCode=OL2112'
    - - :warning
      - 'Line 666: Product not found, record ignored., BaseItemCode=OL2115'
    - - :warning
      - 'Line 668: Product not found, record ignored., BaseItemCode=OL2117'
    - - :warning
      - 'Line 669: Product not found, record ignored., BaseItemCode=OL2121'
    - - :warning
      - 'Line 676: Product not found, record ignored., BaseItemCode=OL2130'
    - - :warning
      - 'Line 681: Product not found, record ignored., BaseItemCode=OL2136'
    - - :warning
      - 'Line 684: Product not found, record ignored., BaseItemCode=OL2139'
    - - :warning
      - 'Line 688: Product not found, record ignored., BaseItemCode=OL2143'
    - - :warning
      - 'Line 689: Product not found, record ignored., BaseItemCode=OL2144'
    - - :warning
      - 'Line 690: Product not found, record ignored., BaseItemCode=OL2145'
    - - :warning
      - 'Line 699: Product not found, record ignored., BaseItemCode=OL2155'
    - - :warning
      - 'Line 776: Product not found, record ignored., BaseItemCode=PF035'
    - - :warning
      - 'Line 777: Product not found, record ignored., BaseItemCode=PF043'
    - - :warning
      - 'Line 780: Product not found, record ignored., BaseItemCode=PF046'
    - - :warning
      - 'Line 782: Product not found, record ignored., BaseItemCode=PWFL1001'
    - - :warning
      - 'Line 783: Product not found, record ignored., BaseItemCode=PWFL1005'
    - - :warning
      - 'Line 784: Product not found, record ignored., BaseItemCode=PWFL1009'
    - - :warning
      - 'Line 785: Product not found, record ignored., BaseItemCode=PWFL1010'
    - - :warning
      - 'Line 786: Product not found, record ignored., BaseItemCode=PWFL1012'
    - - :warning
      - 'Line 787: Product not found, record ignored., BaseItemCode=PWFL1020'
    - - :warning
      - 'Line 789: Product not found, record ignored., BaseItemCode=PWFL1026'
    - - :warning
      - 'Line 790: Product not found, record ignored., BaseItemCode=PWFL1027'
    - - :warning
      - 'Line 791: Product not found, record ignored., BaseItemCode=PWFL1028'
    - - :warning
      - 'Line 792: Product not found, record ignored., BaseItemCode=PWFL1030'
    - - :warning
      - 'Line 793: Product not found, record ignored., BaseItemCode=PWFL1035'
    - - :warning
      - 'Line 794: Product not found, record ignored., BaseItemCode=PWFL1037'
    - - :warning
      - 'Line 795: Product not found, record ignored., BaseItemCode=PWFL1048'
    - - :warning
      - 'Line 804: Product not found, record ignored., BaseItemCode=PWFL1069'
    - - :warning
      - 'Line 805: Product not found, record ignored., BaseItemCode=PWFL1079'
    - - :warning
      - 'Line 806: Product not found, record ignored., BaseItemCode=PWFL1085'
    - - :warning
      - 'Line 810: Product not found, record ignored., BaseItemCode=PWFL1115'
    - - :warning
      - 'Line 811: Product not found, record ignored., BaseItemCode=PWFL1131'
    - - :warning
      - 'Line 812: Product not found, record ignored., BaseItemCode=PWFL1147'
    - - :warning
      - 'Line 813: Product not found, record ignored., BaseItemCode=PWFL1160'
    - - :warning
      - 'Line 814: Product not found, record ignored., BaseItemCode=PWFL1168'
    - - :warning
      - 'Line 815: Product not found, record ignored., BaseItemCode=PWFL1176'
    - - :warning
      - 'Line 816: Product not found, record ignored., BaseItemCode=PWFL1180'
    - - :warning
      - 'Line 817: Product not found, record ignored., BaseItemCode=PWFL1200'
    - - :warning
      - 'Line 819: Product not found, record ignored., BaseItemCode=PWFL1234'
    - - :warning
      - 'Line 820: Product not found, record ignored., BaseItemCode=PWFL1243'
    - - :warning
      - 'Line 822: Product not found, record ignored., BaseItemCode=PWFL1252'
    - - :warning
      - 'Line 825: Product not found, record ignored., BaseItemCode=PWFL1355'
    - - :warning
      - 'Line 826: Product not found, record ignored., BaseItemCode=PWFL1357'
    - - :warning
      - 'Line 827: Product not found, record ignored., BaseItemCode=PWFL1358'
    - - :warning
      - 'Line 829: Product not found, record ignored., BaseItemCode=PWFL1362'
    - - :warning
      - 'Line 830: Product not found, record ignored., BaseItemCode=PWFL1367'
    - - :warning
      - 'Line 831: Product not found, record ignored., BaseItemCode=PWFL1373'
    - - :warning
      - 'Line 832: Product not found, record ignored., BaseItemCode=PWFL1377'
    - - :warning
      - 'Line 833: Product not found, record ignored., BaseItemCode=PWFL1389'
    - - :warning
      - 'Line 835: Product not found, record ignored., BaseItemCode=PWFL1399'
    - - :warning
      - 'Line 837: Product not found, record ignored., BaseItemCode=PWFL1401'
    - - :warning
      - 'Line 838: Product not found, record ignored., BaseItemCode=PWFL1402'
    - - :warning
      - 'Line 839: Product not found, record ignored., BaseItemCode=PWFL1404'
    - - :warning
      - 'Line 840: Product not found, record ignored., BaseItemCode=PWFL1405'
    - - :warning
      - 'Line 841: Product not found, record ignored., BaseItemCode=PWFL1406'
    - - :warning
      - 'Line 843: Product not found, record ignored., BaseItemCode=PWFL1411'
    - - :warning
      - 'Line 844: Product not found, record ignored., BaseItemCode=PWFL1415'
    - - :warning
      - 'Line 846: Product not found, record ignored., BaseItemCode=PWFL1420'
    - - :warning
      - 'Line 847: Product not found, record ignored., BaseItemCode=PWFL1421'
    - - :warning
      - 'Line 848: Product not found, record ignored., BaseItemCode=PWFL1422'
    - - :warning
      - 'Line 851: Product not found, record ignored., BaseItemCode=PWFL1425'
    - - :warning
      - 'Line 855: Product not found, record ignored., BaseItemCode=PWFL1429'
    - - :warning
      - 'Line 856: Product not found, record ignored., BaseItemCode=PWFL1430'
    - - :warning
      - 'Line 857: Product not found, record ignored., BaseItemCode=PWFL1431'
    - - :warning
      - 'Line 858: Product not found, record ignored., BaseItemCode=PWFL1432'
    - - :warning
      - 'Line 859: Product not found, record ignored., BaseItemCode=PWFL1433'
    - - :warning
      - 'Line 860: Product not found, record ignored., BaseItemCode=PWFL1435'
    - - :warning
      - 'Line 861: Product not found, record ignored., BaseItemCode=PWFL1436'
    - - :warning
      - 'Line 862: Product not found, record ignored., BaseItemCode=PWFL1438'
    - - :warning
      - 'Line 863: Product not found, record ignored., BaseItemCode=PWFL1439'
    - - :warning
      - 'Line 864: Product not found, record ignored., BaseItemCode=PWFL1441'
    - - :warning
      - 'Line 865: Product not found, record ignored., BaseItemCode=PWFL1442'
    - - :warning
      - 'Line 867: Product not found, record ignored., BaseItemCode=PWFL1444'
    - - :warning
      - 'Line 869: Product not found, record ignored., BaseItemCode=PWFL1446'
    - - :warning
      - 'Line 870: Product not found, record ignored., BaseItemCode=PWFL1447'
    - - :warning
      - 'Line 871: Product not found, record ignored., BaseItemCode=PWFL1448'
    - - :warning
      - 'Line 873: Product not found, record ignored., BaseItemCode=PWFL1450'
    - - :warning
      - 'Line 875: Product not found, record ignored., BaseItemCode=PWFL1452'
    - - :warning
      - 'Line 877: Product not found, record ignored., BaseItemCode=PWFL1454'
    - - :warning
      - 'Line 879: Product not found, record ignored., BaseItemCode=PWFL1456'
    - - :warning
      - 'Line 886: Product not found, record ignored., BaseItemCode=PWFL1463'
    - - :warning
      - 'Line 897: Product not found, record ignored., BaseItemCode=PWFLO1000'
    - - :warning
      - 'Line 898: Product not found, record ignored., BaseItemCode=PWFLO1001'
    - - :warning
      - 'Line 899: Product not found, record ignored., BaseItemCode=PWFLO1003'
    - - :warning
      - 'Line 900: Product not found, record ignored., BaseItemCode=PWFLO1006'
    - - :warning
      - 'Line 901: Product not found, record ignored., BaseItemCode=PWFLO1007'
    - - :warning
      - 'Line 902: Product not found, record ignored., BaseItemCode=PWFLO1009'
    - - :warning
      - 'Line 903: Product not found, record ignored., BaseItemCode=PWFLO1010'
    - - :warning
      - 'Line 905: Product not found, record ignored., BaseItemCode=PWFLO1012'
    - - :warning
      - 'Line 909: Product not found, record ignored., BaseItemCode=PWFLO1017'
    - - :warning
      - 'Line 919: Product not found, record ignored., BaseItemCode=RALL-10002-810'
    - - :warning
      - 'Line 1135: Product not found, record ignored., BaseItemCode=SHE032'
    - - :warning
      - 'Line 1136: Product not found, record ignored., BaseItemCode=SHE033'
    - - :warning
      - 'Line 1140: Product not found, record ignored., BaseItemCode=STA479'
    - - :warning
      - 'Line 1143: Product not found, record ignored., BaseItemCode=STA571'
    - - :warning
      - 'Line 1144: Product not found, record ignored., BaseItemCode=STA575'
    - - :warning
      - 'Line 1146: Product not found, record ignored., BaseItemCode=STA665'
    - - :warning
      - 'Line 1147: Product not found, record ignored., BaseItemCode=STA689'
    - - :warning
      - 'Line 1148: Product not found, record ignored., BaseItemCode=STA693'
    - - :warning
      - 'Line 1152: Product not found, record ignored., BaseItemCode=STA747'
    - - :warning
      - 'Line 1153: Product not found, record ignored., BaseItemCode=STA757'
    - - :warning
      - 'Line 1159: Product not found, record ignored., BaseItemCode=STA773'
    - - :warning
      - 'Line 1162: Product not found, record ignored., BaseItemCode=STA786'
    - - :warning
      - 'Line 1179: Product not found, record ignored., BaseItemCode=TA177'
    - - :warning
      - 'Line 1181: Product not found, record ignored., BaseItemCode=TA198'
    - - :warning
      - 'Line 1188: Product not found, record ignored., BaseItemCode=TA447'
    - - :warning
      - 'Line 1197: Product not found, record ignored., BaseItemCode=TA459'
    - - :warning
      - 'Line 1198: Product not found, record ignored., BaseItemCode=TA460'
    - - :warning
      - 'Line 1199: Product not found, record ignored., BaseItemCode=TA461'
    - - :warning
      - 'Line 1200: Product not found, record ignored., BaseItemCode=TA462'
    - - :warning
      - 'Line 1209: Product not found, record ignored., BaseItemCode=TA475'
    - - :warning
      - 'Line 1215: Product not found, record ignored., BaseItemCode=TA488'
    - - :warning
      - 'Line 1221: Product not found, record ignored., BaseItemCode=TA497'
    - - :warning
      - 'Line 1257: Product not found, record ignored., BaseItemCode=THR1013'
    - - :warning
      - 'Line 1263: Product not found, record ignored., BaseItemCode=VAS118'
    - - :warning
      - 'Line 1268: Product not found, record ignored., BaseItemCode=VAS201'
    - - :warning
      - 'Line 1269: Product not found, record ignored., BaseItemCode=VAS205'
    - - :warning
      - 'Line 1270: Product not found, record ignored., BaseItemCode=VAS206'
    - - :warning
      - 'Line 1274: Product not found, record ignored., BaseItemCode=VAS211'
    - - :warning
      - 'Line 1275: Product not found, record ignored., BaseItemCode=VAS228'
    - - :warning
      - 'Line 1280: Product not found, record ignored., BaseItemCode=VAS240'
    - - :warning
      - 'Line 1284: Product not found, record ignored., BaseItemCode=VAS257'
    - - :warning
      - 'Line 1289: Product not found, record ignored., BaseItemCode=VAS262'
    - - :warning
      - 'Line 1290: Product not found, record ignored., BaseItemCode=VAS272'
    - - :warning
      - 'Line 1292: Product not found, record ignored., BaseItemCode=VAS274'
    - - :warning
      - 'Line 1294: Product not found, record ignored., BaseItemCode=VAS276'
    - - :warning
      - 'Line 1295: Product not found, record ignored., BaseItemCode=VAS277'
    - - :warning
      - 'Line 1300: Product not found, record ignored., BaseItemCode=VAS283'
    - - :warning
      - 'Line 1323: Product not found, record ignored., BaseItemCode=W6287'
    - - :warning
      - 'Line 1326: Product not found, record ignored., BaseItemCode=W6440'
    - - :warning
      - 'Line 1327: Product not found, record ignored., BaseItemCode=W6471'
    - - :warning
      - 'Line 1329: Product not found, record ignored., BaseItemCode=W6486'
    - - :warning
      - 'Line 1342: Product not found, record ignored., BaseItemCode=W6701'
    - - :warning
      - 'Line 1344: Product not found, record ignored., BaseItemCode=W6706'
    - - :warning
      - 'Line 1347: Product not found, record ignored., BaseItemCode=W6713'
    - - :warning
      - 'Line 1353: Product not found, record ignored., BaseItemCode=W6730'
    - - :warning
      - 'Line 1399: Product not found, record ignored., BaseItemCode=WS117'
    - - :warning
      - 'Line 1405: Product not found, record ignored., BaseItemCode=WS129'
    - - :warning
      - 'Line 1411: Product not found, record ignored., BaseItemCode=WS135'
    - - :warning
      - 'Line 1415: Product not found, record ignored., BaseItemCode=WS139'
    - - :warning
      - 'Line 1420: Product not found, record ignored., BaseItemCode=WS144'
    - - :warning
      - 'Line 1422: Product not found, record ignored., BaseItemCode=WS146'
    - - :warning
      - 'Line 1423: Product not found, record ignored., BaseItemCode=WS147'
    - - :warning
      - 'Line 1446: Product not found, record ignored., BaseItemCode=VAS253'
    - - :warning
      - 'Line 1464: Product not found, record ignored., BaseItemCode=LPT1379EV'
    - - :warning
      - 'Line 1473: Product not found, record ignored., BaseItemCode=LPT1388EV'
    - - :warning
      - 'Line 1485: Product not found, record ignored., BaseItemCode=LIGHTCLOUD'
    - - :warning
      - 'Line 1486: Product not found, record ignored., BaseItemCode=LPC125C'
    - - :warning
      - 'Line 1487: Product not found, record ignored., BaseItemCode=LPC4255'
    - - :warning
      - 'Line 1492: Product not found, record ignored., BaseItemCode=PWFL1007'
    - - :warning
      - 'Line 1496: Product not found, record ignored., BaseItemCode=PWFL1192'
    - - :warning
      - 'Line 1497: Product not found, record ignored., BaseItemCode=PWFL1257'
    - - :warning
      - 'Line 1498: Product not found, record ignored., BaseItemCode=PWFL1310'
    - - :warning
      - 'Line 1499: Product not found, record ignored., BaseItemCode=PWFL1313'
    - - :warning
      - 'Line 1500: Product not found, record ignored., BaseItemCode=PWFL1322'
    - - :warning
      - 'Line 1502: Product not found, record ignored., BaseItemCode=PWFL1391P'
    - - :warning
      - 'Line 1503: Product not found, record ignored., BaseItemCode=PWFLX1019'
    - - :warning
      - 'Line 1601: Product not found, record ignored., BaseItemCode=VAS249'
    - - :warning
      - 'Line 1603: Product not found, record ignored., BaseItemCode=W6345'
    - - :warning
      - 'Line 1604: Product not found, record ignored., BaseItemCode=WS053'
    - - :warning
      - 'Line 1605: Product not found, record ignored., BaseItemCode=ESM-W6005'
    - - :warning
      - 'Line 1606: Product not found, record ignored., BaseItemCode=PWFL1002'
    - - :warning
      - 'Line 1607: Product not found, record ignored., BaseItemCode=PWFL1008'
    - - :warning
      - 'Line 1608: Product not found, record ignored., BaseItemCode=PWFL1011'
    - - :warning
      - 'Line 1609: Product not found, record ignored., BaseItemCode=PWFL1018'
    - - :warning
      - 'Line 1610: Product not found, record ignored., BaseItemCode=PWFL1031'
    - - :warning
      - 'Line 1612: Product not found, record ignored., BaseItemCode=PWFL1039'
    - - :warning
      - 'Line 1614: Product not found, record ignored., BaseItemCode=PWFL1049'
    - - :warning
      - 'Line 1615: Product not found, record ignored., BaseItemCode=PWFL1050'
    - - :warning
      - 'Line 1616: Product not found, record ignored., BaseItemCode=PWFL1065'
    - - :warning
      - 'Line 1617: Product not found, record ignored., BaseItemCode=PWFL1088'
    - - :warning
      - 'Line 1618: Product not found, record ignored., BaseItemCode=PWFL1090'
    - - :warning
      - 'Line 1619: Product not found, record ignored., BaseItemCode=PWFL1095'
    - - :warning
      - 'Line 1620: Product not found, record ignored., BaseItemCode=PWFL1108'
    - - :warning
      - 'Line 1621: Product not found, record ignored., BaseItemCode=PWFL1113'
    - - :warning
      - 'Line 1622: Product not found, record ignored., BaseItemCode=PWFL1145'
    - - :warning
      - 'Line 1625: Product not found, record ignored., BaseItemCode=PWFL1237'
    - - :warning
      - 'Line 1627: Product not found, record ignored., BaseItemCode=PWFL1248'
    - - :warning
      - 'Line 1628: Product not found, record ignored., BaseItemCode=PWFL1261'
    - - :warning
      - 'Line 1629: Product not found, record ignored., BaseItemCode=PWFL1294'
    - - :warning
      - 'Line 1630: Product not found, record ignored., BaseItemCode=PWFL1298'
    - - :warning
      - 'Line 1632: Product not found, record ignored., BaseItemCode=PWFL1302'
    - - :warning
      - 'Line 1633: Product not found, record ignored., BaseItemCode=PWFL1317'
    - - :warning
      - 'Line 1634: Product not found, record ignored., BaseItemCode=PWFL1326'
    - - :warning
      - 'Line 1635: Product not found, record ignored., BaseItemCode=PWFL1327'
    - - :warning
      - 'Line 1636: Product not found, record ignored., BaseItemCode=PWFL1339'
    - - :warning
      - 'Line 1637: Product not found, record ignored., BaseItemCode=PWFL1342'
    - - :warning
      - 'Line 1638: Product not found, record ignored., BaseItemCode=PWFL1346'
    - - :warning
      - 'Line 1639: Product not found, record ignored., BaseItemCode=PWFLO1008'
    - - :warning
      - 'Line 1643: Product not found, record ignored., BaseItemCode=VAS245'
    - - :warning
      - 'Line 1644: Product not found, record ignored., BaseItemCode=VAS251'
    - - :warning
      - 'Line 1646: Product not found, record ignored., BaseItemCode=LPC149'
    - - :warning
      - 'Line 1652: Product not found, record ignored., BaseItemCode=ANTISLIP912'
    - - :warning
      - 'Line 1653: Product not found, record ignored., BaseItemCode=CHA064'
    - - :warning
      - 'Line 1654: Product not found, record ignored., BaseItemCode=FLP1024'
    - - :warning
      - 'Line 1655: Product not found, record ignored., BaseItemCode=FLP1616'
    - - :warning
      - 'Line 1656: Product not found, record ignored., BaseItemCode=PWFL1407'
    - - :warning
      - 'Line 1662: Product not found, record ignored., BaseItemCode=VAS282'
    - - :warning
      - 'Line 1664: Product not found, record ignored., BaseItemCode=W6714'
    - - :warning
      - 'Line 1665: Product not found, record ignored., BaseItemCode=W6715'
    - - :warning
      - 'Line 1666: Product not found, record ignored., BaseItemCode=W6732'
    - - :warning
      - 'Line 1682: Product not found, record ignored., BaseItemCode=LPC4488'
    - - :warning
      - 'Line 1996: Product not found, record ignored., BaseItemCode=PA0062'
 |
| 2026-06-12 22:06:09 | ---
- - Portal Invoices
  - []
 |

### Q-10_results.md

# Q-10 Results — RENWIL (rw, org_id=248)
- **Query**: Q-10 — Feature Enablement Gap Analysis
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| enable_sales_portal | enable_online_catalog | enable_online_ordering | kit_item_count | contract_price_count | enrollment_count | smart_stack_count | shared_resource_count | portal_order_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 0 | 0 | 3 | 51 | 0 |

### Q-11_results.md

# Q-11 Results — RENWIL (rw, org_id=248)
- **Query**: Q-11 — Configuration Completeness
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 17
- **Run date**: 2026-06-16


| entity_type | last_updated | days_stale | related_record_count |
| --- | --- | --- | --- |
| sales_quotas | 2025-08-20 19:47:15 | 300 | 0 |
| customer_payment_informations | 2025-08-20 19:47:15 | 300 | — |
| riser_prices | 2025-08-20 19:47:15 | 300 | — |
| placement_reports | 2025-08-20 19:47:15 | 300 | — |
| commitment_reports | 2025-08-20 19:47:15 | 300 | — |
| matrix_options | 2025-08-20 19:47:15 | 300 | — |
| kit_items | 2025-08-20 19:47:15 | 300 | 0 |
| customer_favorites | 2025-08-20 19:47:15 | 300 | — |
| contract_prices | 2025-08-20 19:47:15 | 300 | 0 |
| trade_names | 2025-08-20 19:47:15 | 300 | — |
| collections | 2025-08-20 19:47:15 | 300 | — |
| price_levels | 2025-08-20 19:47:15 | 300 | — |
| options | 2025-11-07 20:52:41 | 221 | — |
| option_groups | 2025-11-07 20:52:41 | 221 | — |
| portal_orders | 2026-03-13 18:54:01 | 95 | — |
| categories | 2026-04-27 16:54:21 | 50 | — |
| groups | 2026-04-27 16:54:21 | 50 | — |

### Q-22_results.md

# Q-22 Results — RENWIL (rw, org_id=248)
- **Query**: Q-22 — Feature Usage Depth
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| org_shortname | org_name | submit_order | select_a_customer | search_for_customer | email_item_info | create_pdf_catalog | view_library_entry | view_smartpicks | access_sales_portal | filter_products | search_products | search_collections | order_configured_item | view_kit | order_kit | share_my_list | export_data_to_csv | export_data_to_excel | total_events | total_users |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rw | RENWIL | 9,995 | 15,622 | 31,290 | 284 | 786 | 3,198 | 93 | 606 | 692 | 45,286 | 52 | 16,443 | 0 | 0 | 47 | 2 | 5 | 173,537 | 90 |

### Q-46_pg_results.md

# Q-46-pg Results — RENWIL (rw, org_id=248)
- **Query**: Q-46-pg — Workflow Maturity — Postgres
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| submitted_ecat_orders_90d |
| --- |
| 2,347 |

### Q-46_bq_results.md

# Q-46-bq Results — RENWIL (rw, org_id=248)
- **Query**: Q-46-bq — Workflow Maturity — Mixpanel
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| customer_targeting_events | product_discovery_events | presentation_events |
| --- | --- | --- |
| 46,912 | 45,978 | 1,117 |

### Q-47_results.md

# Q-47 Results — RENWIL (rw, org_id=248)
- **Query**: Q-47 — Smart Stack Effectiveness
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 3
- **Run date**: 2026-06-16


| stack_id | stack_name | published | is_dormant | created_at | updated_at | days_since_update |
| --- | --- | --- | --- | --- | --- | --- |
| 9,695 | Sale | 1 | — | 2025-02-21 18:25:54 | 2026-06-10 16:20:31 | 6 |
| 10,191 | FW 2025 Collection | 1 | — | 2025-07-25 20:43:35 | 2026-06-10 16:20:31 | 6 |
| 10,541 | SS 2026 Collection | 1 | — | 2026-01-19 15:30:58 | 2026-06-10 16:20:31 | 6 |

### Q-50_results.md

# Q-50 Results — RENWIL (rw, org_id=248)
- **Query**: Q-50 — Library / Document Inventory
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 7
- **Run date**: 2026-06-16


| resource_id | document_name | resource_type | shared_document_file_name | created_at | updated_at | days_since_update |
| --- | --- | --- | --- | --- | --- | --- |
| 36,056 | — | directory | — | 2026-04-27 14:39:39 | 2026-04-27 14:42:27 | 50 |
| 34,575 | — | directory | — | 2025-11-12 21:23:25 | 2025-11-12 21:24:29 | 216 |
| 31,522 | — | directory | — | 2025-02-11 16:23:03 | 2025-07-29 20:04:39 | 322 |
| 31,159 | — | directory | — | 2025-01-13 14:59:52 | 2025-05-06 18:48:42 | 406 |
| 31,155 | — | directory | — | 2025-01-13 14:57:24 | 2025-05-06 18:48:25 | 406 |
| 31,184 | — | directory | — | 2025-01-13 16:36:50 | 2025-01-13 16:36:50 | 519 |
| 31,154 | — | directory | — | 2025-01-13 14:56:37 | 2025-01-13 14:56:37 | 519 |

### user_group_mapping.md

# User Group Mapping — RENWIL (rw, org_id=248)
- **Run date**: 2026-06-16
- **Total Postgres users**: 103
- **Matched to Mixpanel (Q-01 Step 1)**: 84 of 90 (93%)
- **Classification confidence**: LOW
- **Split available**: False

## Group Classification

| User Group (Admin Console) | Bucket | User Count |
| --- | --- | --- |
| Reps USA | field_rep | 58 |
| Reps Canada | field_rep | 14 |
| Renwil Internal | admin_internal | 12 |
| z-SuperCat | admin_internal | 6 |
| Reps Quebec | field_rep | 4 |
| 1-Default eOL User Group | admin_internal | 3 |
| Admin Group | admin_internal | 2 |
| Ferguson | other | 1 |
| Reps US/CAN | field_rep | 1 |
| Reps US/CAN | admin_internal | 1 |
| eOL Public Site | admin_internal | 1 |

## Aggregate Split

| Bucket | Users | Total Events | Event Share |
| --- | --- | --- | --- |
| field_rep | 70 | 158,233 | 92.7% |
| admin_internal | 13 | 10,933 | 6.4% |
| other | 1 | 1,564 | 0.9% |
