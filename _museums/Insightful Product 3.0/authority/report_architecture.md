# Report Architecture — Insightful Product 3.0

> **Status**: Active
> **Replaces**: `external_report_blueprint.md` (Insightful Product 2.0)
> **Organizing principle**: Signal-first. The report leads with what's most surprising and actionable, not what domain it belongs to.
> **Design origin**: Customer Intelligence v4 per-customer briefs scaled to org-level delivery.

---

## Core Philosophy

**This report should make the client say: "Holy shit — I didn't know that about
my business. I need to keep paying for this."**

The 2.0 report was domain-ordered and QBR-flavored. 3.0 is **intelligence-first**:
- Sections lead with what's WORKING, then surface intelligence the client can't
  get elsewhere, then show opportunities, then contextualize risks
- Every insight is item-level specific with named customers, dollar amounts, and
  clear actions
- Sections render if they have any fired signal OR their data gate passes
- The goal is DATA-DENSE, BALANCED output — comprehensive intelligence that
  makes the client smarter about their business, not an alarm board

**The tests**:
1. If a finding could appear on a generic industry dashboard, it doesn't belong here.
2. If the report makes the client feel bad about their business, the framing is wrong.
3. If the client reads only the Signal Summary and says "we should churn," the
   tone balance has failed — rewrite.

> **Narrative arc and editorial voice rules** are defined in `shared_rules.md`
> Section A0. They are not duplicated here. Every section builder receives
> `shared_rules.md` via the context bundle.

---

## Report Modes

### Mode 1 — Standard
**Gate**: LTM commerce > 0 (any channel).
Full signal-first report. All sections eligible.

### Mode 2 — Activation
**Gate**: Zero commerce ever recorded.
Only renders: Platform Context (expanded) and a "What becomes possible" section projecting value based on the org's own data trajectory. No commerce analysis, no account intelligence.

### Mode 3 — Reactivation
**Gate**: Had commerce, now lapsed (zero orders in trailing 90 days after prior activity).
Renders: Historical context (peak metrics, top accounts before lapse), re-engagement signals (which accounts are still active elsewhere), platform readiness state, and a recovery playbook with specific accounts to target first.

---

## Data Mass Assessment (Pre-Report Gate)

Before rendering any section, compute the **DATA_MASS_TIER** for this org. This determines whether the report can produce genuinely surprising intelligence or is limited to confirming what the client already knows.

### Computation

| Factor | Points |
|--------|--------|
| LTM eCat orders > 500 | +2 |
| LTM eCat orders > 2,000 | +2 (cumulative with above) |
| Active accounts (12mo) > 20 | +2 |
| Active accounts (12mo) > 100 | +2 (cumulative) |
| Active reps > 5 | +1 |
| `HAS_PORTAL_ORDERS = true` | +3 |
| `MIXPANEL_USER_DATA_PRESENT = true` | +2 |
| `HAS_INVENTORY = true` | +1 |
| LTM eCat GMV > $500K | +2 |
| Months of order history > 12 | +1 |

### Tier Assignment

| Score | Tier | Label |
|-------|------|-------|
| 14+ | `FULL` | Full Intelligence |
| 10–13 | `STRONG` | Strong Intelligence |
| 6–9 | `MODERATE` | Moderate Intelligence |
| 3–5 | `EARLY` | Early-Stage Intelligence |
| 0–2 | `MINIMAL` | Minimal Data |

### Thin-Data Handling (EARLY or MINIMAL tier)

When `DATA_MASS_TIER` is `EARLY` or `MINIMAL`, the full report still renders (all sections that pass their gates), but the following MANDATORY additions apply:

1. **Prominent Report Header Disclosure**: Immediately after the report title and before §1 Signal Summary, render:

```html
<div class="data-maturity-notice">
  <div class="data-maturity-title">Data Maturity: {{TIER_LABEL}}</div>
  <div class="data-maturity-body">
    <p>This report draws from {{ORDERS}} eCat orders across {{ACCOUNTS}} accounts over {{MONTHS}} months. The intelligence below is accurate for what we can see — but the picture is incomplete.</p>
    <p><strong>What limits this report:</strong></p>
    <ul>
      {{FOR EACH MISSING GATE: <li>{{WHAT_WE_DONT_HAVE}} — {{WHAT_IT_WOULD_ENABLE}}</li>}}
    </ul>
    <p><strong>What becomes possible with more data:</strong> As order volume grows and additional data sources connect, this report will surface cross-customer purchase patterns, predictive reorder intelligence, competitive displacement detection, and behavioral coaching opportunities that are not yet statistically meaningful.</p>
  </div>
</div>
```

2. **Per-Section "With More Data" Enhancement**: Each section's what-this-means block for EARLY/MINIMAL tiers MUST include a forward-looking sentence: "With [X more months of data / N more active accounts / portal_orders connected], this section will show [specific intelligence type]."

3. **Signal Summary Framing**: Finding #1 in thin-data reports should still be positive but grounded: "Your first 4 accounts generated $X in eCat orders over Y months — early, but these are the relationships that will compound as adoption grows."

4. **Never apologize, never dismiss.** The report is NOT less valuable for being early-stage — it's a DIFFERENT kind of value: baseline establishment, first-mover identification, and a clear picture of what's possible. Frame as "here's your starting position and here's the trajectory if adoption continues" — not "sorry we don't have enough data."

### Example "What We Don't Have" Items

| Missing Gate | What We Don't Have | What It Would Enable |
|---|---|---|
| `HAS_PORTAL_ORDERS = false` | Total business order history | Competitive displacement detection, wallet share analysis, capture rate trending |
| `MIXPANEL_USER_DATA_PRESENT = false` | App behavioral data | Rep efficiency ranking, presentation-to-close conversion, archetype coaching |
| Active accounts < 20 | Sufficient account diversity | Cross-customer pattern detection, collaborative filtering, category whitespace analysis |
| LTM orders < 500 | Statistical significance | Reorder velocity prediction, seasonal pattern identification, decay signal confidence |

---

## Section Architecture — Fixed Positions

All section positions are **deterministic**. There is no fluid ordering.

| Position | Section | § | Guide |
|----------|---------|---|-------|
| 1st (always) | Signal Summary | §1 | `section_01_signals.md` |
| 2nd (always) | Team Intelligence | §5 | `section_05_team.md` |
| 3rd (always) | Account Intelligence | §2 | `section_02_accounts.md` |
| 4th (always) | Commerce Patterns | §4 | `section_04_commerce.md` |
| 5th (always) | Product Intelligence | §3 | `section_03_product.md` |
| 6th (always) | Platform Context | §6 | `section_06_platform.md` |
| Last (always) | Appendix | — | (defined below) |

**Rationale:** The VP of Sales sees their team first (§5), then customer
intelligence (§2), then commerce patterns (§4), then product detail (§3),
with operational context last (§6). This ordering is stable across all clients.

### Section Render Gates

A section renders if ANY of the following are true:
- It has ≥ 1 fired P0 or P1 signal
- Its section guide's alternate include gate passes
- It contains a query-driven subsection with data that passes the guide's specificity test

A section is suppressed only if it has zero fired signals AND its alternate
gate fails. Suppressed sections are omitted from the TOC and body.

---

## Section Summaries

Each section's full subsection spec lives in its guide file. Below is purpose only.

### §1 Signal Summary
Built LAST, rendered FIRST. The executive who reads nothing else gets the full
picture in 30 seconds. 5–7 findings, priority actions, conversation questions.

### §5 Team Intelligence
Rep leaderboard, behavioral archetypes, coaching cards. Suppressed if < 5
active reps. Only coaching interventions worth > $50K estimated upside.

### §2 Account Intelligence
Per-customer deep intelligence with top 10 mini-briefs. The core value section —
what no ERP dashboard provides.

### §4 Commerce Patterns
Only non-obvious cross-system patterns. If a metric appears on any standard
dashboard, it doesn't belong here.

### §3 Product Intelligence
Item-level intelligence connecting product performance to specific customer
behavior. Fill rate, ghost SKUs, velocity signals, adoption gaps.

### §6 Platform Context
Operational health — actionable staleness, feature adoption gaps. Collapsed by
default. Only expands for P0/P1 signals.

---

## Appendix

**Render position**: Always last.
**Purpose**: Data provenance and methodology. Nothing actionable lives here.

### Data Sources

| Source | Records | Date Range | Refresh |
|--------|---------|------------|---------|
| eCat Orders | [N] | [START] – [END] | [FREQ] |
| All-Channel Orders (synced from ERP) | [N] | [START] – [END] | [FREQ] |
| Product Catalog | [N] active items | as of [DATE] | [FREQ] |
| Inventory | [N] items | as of [DATE] | [FREQ] |
| Customer Master | [N] accounts | as of [DATE] | [FREQ] |

### Methodology Notes

- LTM = Last Twelve Months from report generation date
- YoY = Same period comparison (LTM vs prior LTM)
- Signal scoring: `surprise_score × dollar_impact × actionability_multiplier` (see signal_catalog.md)
- Collaborative filtering: Jaccard similarity on category purchase vectors, minimum 3 shared categories
- Reorder interval: Median days-between-orders, minimum 5 order cycles to qualify

### Labeling Convention

| Label | Meaning |
|-------|---------|
| `[HYPOTHETICAL]` | Projection assuming a behavioral change. Not guaranteed. |
| `[ESTIMATED]` | Extrapolation from partial data. Directionally correct, not precise. |
| `[eCat ONLY]` | Metric covers eCat platform orders only, not total business. |
| `[ALL-CHANNEL]` | Metric includes all order sources synced from ERP systems. |

---

## Generation Sequence

The report is built in this order (not the rendered order):

1. **Data gather** — execute query library, materialize results
2. **Signal detection** — run each signal's detection logic against materialized data
3. **Signal scoring** — compute `SIGNAL_RANK` for all fired signals
4. **Context bundles** — build per-section context bundles (MANDATORY)
5. **Section rendering** — build each qualifying section's content from its bundle
6. **Signal Summary** — select top 5–7 by SIGNAL_RANK, generate Priority Actions and Conversation Patterns
7. **HTML assembly** — compose final document in FIXED render order
8. **Structural verification** — verify all mandatory subsections rendered
9. **Static check** — run check_static.sh

This ensures the Signal Summary always reflects the actual report content (it's written last, rendered first).

---

## Rendered Document Skeleton

```html
<article class="insightful-report" data-mode="[1|2|3]" data-generated="[ISO_DATE]">

  <section id="signal-summary" data-position="1">
    <!-- Signal Summary — always first -->
  </section>

  <section id="team" data-position="2">
    <!-- Team Intelligence — always second -->
  </section>

  <section id="accounts" data-position="3">
    <!-- Account Intelligence — always third -->
  </section>

  <section id="commerce" data-position="4">
    <!-- Commerce Patterns — always fourth -->
  </section>

  <section id="product" data-position="5">
    <!-- Product Intelligence — always fifth -->
  </section>

  <section id="platform" data-position="6">
    <!-- Platform Context — always sixth, collapsed -->
  </section>

  <section id="appendix" data-position="last">
    <!-- Data sources, methodology, labels -->
  </section>

</article>
```

---

## Relationship to Other Authority Files

| File | Role |
|------|------|
| `signal_catalog.md` | Defines every detectable signal, its scoring formula, and output format |
| `query_library.md` | SQL queries that materialize the raw data for signal detection |
| `shared_rules.md` | Editorial voice, client-facing language, formatting rules, dollar math — the universal ruleset |
| `html_report_template.html` | The actual HTML/CSS shell that rendered content is injected into |
| **this file** | The structural blueprint — modes, data mass, section order, generation sequence |
| Section guides (`section_0N_*.md`) | Per-section subsection specs, gate checks, and checklists |
| `section_shared_contract.md` | Cross-section processes (confidence headers, gate checks, forbidden terms) |
