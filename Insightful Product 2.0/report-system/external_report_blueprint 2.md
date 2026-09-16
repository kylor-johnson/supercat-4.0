# External Report Blueprint

> **Status**: Execution mode — single report form (profiles retired).
> **Purpose**: Lean, operational assembly rules for the external customer intelligence report.
> **Authority**: Derived from `reference/value_moment_catalog.md` + locked design decisions.
> **Target**: Operator reads this file. It replaces the old formatting guide + report generation guide + editorial standards stack.

---

## 0. Section Order (Mode 1 Standard)

Single report form (profiles retired). The order below is Mode 1; see "Report Modes" for Modes 2/3.

| # | Section | Status | VMs |
|---|---------|--------|-----|
| 1 | Executive Summary | Always included — written last | Synthesis |
| 2 | Sales Team Performance | Conditional | VM-01–VM-06, VM-43, VM-46 |
| 3 | Customer & Buyer Intelligence | Always included | VM-12, VM-13, VM-14, VM-17, VM-41, VM-49 |
| 4 | Product & Inventory Intelligence | Conditional | VM-37, VM-38a, VM-39, VM-42 |
| 5 | Commerce Analytics | Always included | VM-16, VM-18, VM-19, VM-20, VM-21, VM-45 |
| 6 | Portal Engagement | Conditional (HAS_CLICKY) | VM-31–VM-35 |
| 7 | Peer Benchmarking | Conditional | VM-23, VM-24, VM-25, VM-26 |
| 8 | Platform & Feature Utilization | Always included | VM-07–VM-11, VM-22, VM-47, VM-50 |
| 9 | Appendix | Always included | Attribution only |

**Executive Summary rules:**
- 5–6 numbered highlights using `<ul class="highlights"><li>` structure
- Each highlight: one bold headline phrase, one sentence of context, section link
- No prose before the highlights list — highlights are the first content element
- Priority Actions block: 2–4 actions, highest urgency first, with urgency levels (HIGH / MEDIUM / LOW)
- Lower-priority actions may be wrapped in a collapsed `<details>` block

---

## 0. Report Modes

There are three output modes. The operator selects the correct mode in Stage 0 (Minimum-Commerce Gate) before generating anything. Each mode is a complete, intentional output — not a stripped-down version of another.

### Mode 1: Standard Intelligence Report

**Trigger**: LTM eCat orders > 0 OR LTM portal_orders > 0.

This is the full intelligence report. The client has measurable commerce activity and the platform is generating data worth analyzing. All sections are eligible (subject to standard conditional logic). The narrative should be grounded in what the data actually shows — not templated.

**Header label**: `Customer Intelligence Report`
**Report badge**: Platform bundle label (e.g., `Full · iPad + eCat Online + Sales Portal`)

---

### Mode 2: Platform Activation Report

**Trigger**: LTM eCat = 0 AND LTM portal_orders = 0 AND all-time eCat order count = 0.

This client has never placed an eCat order. They are configured and enrolled but the platform has not been used for commerce. This is not a failure state — it's an early-stage account that needs a different kind of story than a commerce-active client.

**Narrative shape**: The story is about platform readiness and untapped potential. The report surfaces what the platform is configured to do, how the account compares to peers at a similar stage, and what the first activation steps look like. It does not pretend to show commerce data that does not exist.

**Included sections**:

| # | Section | Notes |
|---|---------|-------|
| 1 | Activation Summary | Replaces Executive Summary — describes activation context and platform state |
| 2 | Platform Readiness | Replaces §8 — catalog completeness, data health, configuration status |
| 3 | Peer Benchmarking | §7 — if peer data available; frame as "how similar accounts have activated" |
| 4 | Appendix | Platform data sources, configuration notes |

**Excluded sections (all of these — do not include, do not reference)**:
- §2 Sales Team Performance
- §3 Customer & Buyer Intelligence
- §4 Product & Inventory Intelligence
- §5 Commerce Analytics
- §6 Portal Engagement

**Header label**: `Platform Activation Report`
**Report badge**: `Activation Stage · No eCat Commerce History`

**Tone**: Constructive, forward-looking. "Your platform is configured. Here's what's ready and what to activate first." Do not frame the absence of commerce as a problem to be solved urgently — frame it as an early stage with clear next steps.

**Disclosure note required — place in the Activation Summary section as a callout, NOT in the Appendix**: "This report reflects platform configuration and readiness context. Commerce sections are not included as no eCat ordering activity has been recorded." The Appendix remains attribution-only even in Mode 2 — it contains only data source rows for the sources that were actually used.

---

### Mode 3: Platform Reactivation Report

**Trigger**: LTM eCat = 0 AND LTM portal_orders = 0 AND all-time eCat order count > 0.

This client has used the platform before but has not had any eCat or ERP order activity in the trailing 12 months. They are lapsed — the platform exists, it was used, and then it stopped being used. This is a different story than activation: there is a history to reference and a gap to explain.

**Narrative shape**: The story is about what lapsed, what's still in place, and what re-engagement looks like. Reference historical commerce context (all-time figures, most recent active period) to anchor the narrative. The report surfaces what's still configured, what may have gone stale, and what the re-engagement path looks like. Do not manufacture urgency — but do be honest about what lapsed data means.

**Included sections**:

| # | Section | Notes |
|---|---------|-------|
| 1 | Reactivation Summary | Replaces Executive Summary — lapsed context, last-active period, re-engagement framing |
| 2 | Historical Commerce Context | Lightweight — all-time order count, last active period, approximate GMV if available. Mark all figures with their source period. |
| 3 | Platform Status | Replaces §8 — catalog health, data staleness (especially for lapsed accounts — staleness is likely), configuration state |
| 4 | Peer Benchmarking | §7 — if peer data available; caveat that benchmarks reflect current platform use, not the lapsed period |
| 5 | Appendix | Data sources, staleness disclosures, all-time commerce notes |

**Excluded sections (all of these — do not include, do not reference)**:
- §2 Sales Team Performance
- §3 Customer & Buyer Intelligence (no LTM data)
- §4 Product & Inventory Intelligence (inventory is point-in-time; if stale, note and skip)
- §5 Commerce Analytics (LTM data absent)
- §6 Portal Engagement

**Header label**: `Platform Reactivation Report`
**Report badge**: `Reactivation Stage · Lapsed — No LTM Commerce Activity`

**Tone**: Direct, honest, constructive. "The platform was active. It went quiet. Here's the current state and what re-engagement looks like." Do not apologize for the gap. Do not manufacture an urgency narrative. Reference historical figures accurately as historical.

**Staleness handling in reactivation mode**: For lapsed accounts, core data entities (products, inventories, customers) may themselves be stale. In the Platform Status section:
- Use the 3-label freshness scale (Fresh / Monitor / Stale) from Q-08 as usual
- If core entities are Stale (>180 days): explicitly flag this in the Reactivation Summary — re-activating on stale catalog data is a pre-requisite issue to resolve first
- Do not show Product & Inventory section if inventory is stale (>180 days)

**Disclosure note required — place in the Reactivation Summary section as a callout, NOT in the Appendix**: "This report reflects platform configuration and historical activity context. Commerce sections are not included as no eCat ordering activity has been recorded in the trailing 12 months. Last recorded eCat activity: [DATE]." The Appendix remains attribution-only even in Mode 3 — it contains only data source rows for the sources that were actually used.

---

## 1. Fixed Section Order (Standard Intelligence Report — Mode 1 only)

The section orders below apply to **Mode 1 (Standard Intelligence Report)** only. Modes 2 and 3 have their own section structures defined in §0 above. Do not apply these orders to activation or reactivation reports.

Sections must appear in the defined order. The operator does not reorder sections.

### Section Order

| # | Section | Status | VMs |
|---|---------|--------|-----|
| 1 | Executive Summary | Always included — written last | Synthesis (no dedicated VMs) |
| 2 | Sales Team Performance | Conditional | VM-01, VM-02, VM-03, VM-04, VM-05, VM-06, VM-43, VM-46 |
| 3 | Customer & Buyer Intelligence | Always included | VM-12, VM-13, VM-14, VM-17, VM-41, VM-49 |
| 4 | Product & Inventory Intelligence | Conditional | VM-37, VM-38a, VM-39, VM-42 |
| 5 | Commerce Analytics | Always included | VM-16, VM-18, VM-19, VM-20, VM-21, VM-45 |
| 6 | Portal Engagement | Conditional | VM-31, VM-32, VM-33, VM-34, VM-35 |
| 7 | Peer Benchmarking | Conditional | VM-23, VM-24, VM-25, VM-26 |
| 8 | Platform & Feature Utilization | Always included | VM-07, VM-08, VM-09, VM-10, VM-11, VM-22, VM-47, VM-50 |
| 9 | Appendix | Always included | Attribution only |

> **VM-24 note**: VM-24 (Feature Adoption Benchmarking) appears in §7 Peer Benchmarking. VM-22 (feature usage intensity, absolute) appears in §8 Platform & Feature Utilization. They remain distinct sections.

---

## 2. Conditional Logic

| Section | Include when | Skip when | Fallback if skipped |
|---------|-------------|-----------|-------------------|
| Sales Team Performance | 5+ active selling reps with 10+ eCat orders each in the period | Fewer than 5 qualifying reps | Omit section silently — no note in delivered report. |
| Product & Inventory Intelligence | `inventories` OR `sales_data` present for the org | Both absent | No section. No placeholder. |
| Portal Engagement | `has_clicky = true` | `has_clicky = false` | Section absent entirely. Do not mention Clicky, portal analytics, or traffic anywhere else in the report. |
| Peer Benchmarking | Peer benchmark data available (`dependencies/PEER_BENCHMARK.md` file exists and is current) | No peer data available | Omit section silently — no note in delivered report. |
| VM-19 (Channel Mix) | `has_cart = true` AND server-source eCat orders confirmed | iPad-only clients | State "All orders placed through the eCat iPad App." No channel mix table. |
| VM-15, VM-44 (Enrollment / Onboarding) | *(excluded from external scope)* | Always | Enrollment is intentionally out of scope for external reporting. Do not include, reference, or add an Appendix note about enrollment. |
| VM-16, VM-45 (ERP/Capture Rate) | `portal_orders` present | `portal_orders` absent | Omit VM-45 entirely. Omit VM-16 ERP context from Commerce Analytics. Do not create a denominator-less partial analysis. |
| VM-37, VM-39, VM-42 (Product Intel) | `sales_data` present | `sales_data` absent | Omit each silently. |
| VM-38a (Product Velocity) | `portal_order_items` present | Absent | Omit silently. |

---

## 3. Dollar Math Requirements

Dollar math may only be used when directly supported by data. Mark all projections `[HYPOTHETICAL]` and all extrapolations `[ESTIMATED]`.

| Section | Calculation | Formula | Only when |
|---------|-------------|---------|-----------|
| Sales Team Performance | Upside from coaching (VM-03) | `(peer_AOV − rep_AOV) × rep_order_count` | Rep's funnel gap is clearly identified AND peer AOV baseline exists; always tag `[HYPOTHETICAL]` |
| Customer & Buyer Intelligence | Lapsed GMV at risk (VM-17) | `lapsed_buyer_trailing_12mo_eCat_GMV` | Trailing 12-month eCat GMV confirmed for the lapsed buyer; always tag as trailing historical, not forward projection |
| Product & Inventory Intelligence | OOS demand context (VM-37) | `sum(sales_data.amount_invoiced) for items with qty_available = 0` | Both `sales_data` and `inventories` present; always caveat inventory is a point-in-time snapshot |
| Commerce Analytics | eCat capture rate (VM-45) | `eCat_order_count / portal_orders_count` and `eCat_GMV / portal_orders_GMV` | `portal_orders` present; always clarify denominator = "total orders synced from your ERP" |
| Commerce Analytics | Quote workflow opportunity (VM-20/21) | `(quote_AOV − confirmed_AOV) × confirmed_order_count` | 10+ Quote orders in period exist; always tag `[HYPOTHETICAL]` |

**Universal dollar math rule**: Never use a dollar figure to make a claim broader than the data supports. eCat dollar figures are eCat-channel only unless explicitly stated otherwise. `portal_orders` dollar figures represent ERP-synced total business.

---

## 4. Universal Rules

These rules apply to every section of every external report.

### Structure rules
1. **Executive Summary is written last.** It synthesizes the most important 5–6 signals from completed sections. It is never populated before section data is gathered and analyzed.
2. **Every section ends with a "What this tells you" close.** One to three sentences. Focuses on the actionable implication, not a summary of statistics.
3. **Every metric requires a time qualifier.** No bare numbers. "373 active eCat buyers in the trailing 12 months" — not "373 active eCat buyers."

### Claim rules
4. **Use `[HYPOTHETICAL]` on all projections.** Any dollar figure or outcome estimate that is not directly measured. Example: "If your rep's AOV increased to match the team average, that's ~$42K in incremental eCat GMV over 12 months [HYPOTHETICAL]."
5. **Use `[ESTIMATED]` on all extrapolations.** Any figure derived from incomplete data or interpolation. The tag plus the sentence it modifies is the complete disclosure — no separate Appendix entry required. Example: "Inventory snapshot suggests 8 top-selling items are currently unavailable — based on trailing 12-month demand, this represents ~$2.5M in historical sales volume [ESTIMATED]."
6. **Channel attribution belongs in Commerce Analytics body.** When eCat figures are cited, note the channel explicitly in Commerce Analytics. Do not bury the attribution in footnotes in other sections.
7. **Technical attribution belongs in the Appendix only.** Data source details, query methodology, and `portal_orders` definition belong in the Appendix. Do not repeat methodology in every section.

### Semantics rules (locked)
8. **`portal_orders` = total business context, never buyer activity.** Any reference to `portal_orders` in external prose must use one of these framings: "orders synced from your ERP," "your total business across all channels," "all-channel order volume." Never: "orders placed on your portal," "buyer self-service orders," "portal ordering activity."
9. **Clicky = binary gate.** If `has_clicky = false`, the Portal Engagement section does not exist. Do not reference portal traffic, portal analytics, or Clicky capabilities anywhere in the report.
10. **Health score is absent from Phase 1 external reports.** Do not reference health score, health band, or Health V2 classification in any external-facing section, the executive summary, or the appendix.
11. **Plain-language cohort framing only in Peer Benchmarking.** In the Peer Benchmarking section, describe the peer group in plain language derived from `peer_group_id_effective` (e.g., "Lighting manufacturers on the same platform bundle" — not the raw label "Lighting / iPad+Catalog+Portal"). Internal segment labels — "Platform-Embedded," "Commerce-Active," "Catalog-Focused" — must never appear anywhere in the external report, including the Peer Benchmarking section. Tier labels, confidence labels, and raw `peer_group_id_effective` values as literals must not appear in client-facing prose. See `dependencies/PEER_BENCHMARK.md §3` and §7 for approved external framing.
12. **Benchmark metadata is internal only.** `benchmark_confidence`, `peer_group_level`, and `peer_group_n` are internal rendering signals used to calibrate plain-language framing and section inclusion. None of these values — including `high`, `medium`, `low`, `tier1`, `tier2`, `tier3` — may appear in client-facing output. Benchmark context in the report body uses plain-language descriptions only (see `dependencies/PEER_BENCHMARK.md` §7 for approved language).

### Output rules
13. **Never improvise around missing data.** If a VM is gated and the gate condition is not met, skip the section or VM. Do not substitute a narrative, approximate with a related figure, or create a placeholder section.
14. **Cost-of-inaction math is optional, not universal.** Only include where: (a) the data directly supports it (lapsed GMV, OOS historical demand) and (b) the claim is honest and defensible. Do not manufacture urgency.
15. **ERP technical terminology must not appear in any delivered client-facing HTML element.** "ERP" is forbidden in every part of §1–§8 and §9 except one: the Appendix data source attribution row for total all-channel business data. This prohibition covers: body prose, metric labels, `metric-note` slots, table cell text, table footnotes, subsection headers, section descriptions, `section-sub` stat lines, callout boxes, and any other HTML element the client sees. Use plain-language alternatives everywhere: "total business," "all-channel sales," "total all-channel orders," "orders across all sales channels," "your account base," "your business system." **VM-12 specific**: When describing the customer account universe in §3 (Customer Activation & Network Health), replace "all-time ERP records" and "ERP base" with "total account records" or "your full account base." Replace "ERP accounts have never placed an eCat order" with "accounts in your system have never placed an eCat order."
16. **Internal/debug language must not appear in delivered HTML.** The delivered report is a client-facing document. Phrases like "package defect," "pending engineering," "query returned zero rows," "runtime workaround," "tooling limitation," "validation note," "Gate 2 failed," and "per documented requirement" are operator/agent vocabulary — they belong in validation logs, not in delivered HTML. If a limitation matters to the client, restate only the plain-language business conclusion in the Appendix.
17. **All HTML comments must be stripped from delivered HTML.** The template file (`html_report_template.html`) contains `<!-- ... -->` authoring comments to guide the operator. None of these comments may remain in the final delivered HTML file. This covers: `<!-- Operator: ... -->` guidance comments, `<!-- BEGIN/END ... GATE -->` gating markers, `<!-- HAS_* -->` flag references, `<!-- e.g., ... -->` example hints, `<!-- EXAMPLE ROW ... -->` blocks, section header banners (`<!-- ═══ §N ... ═══ -->`), and any other HTML comment node. The delivered HTML source must be comment-free. Search `<!--` in the delivered file and resolve every hit before delivery.

---

## 5. Executive Summary Rules

The Executive Summary is the first section in the delivered report but the last section written by the operator.

- 5–6 numbered highlights using `<ul class="highlights"><li>` structure — this is the first content element; no prose before the list
- Each highlight: one bold headline phrase, one sentence of context, section link
- Each highlight draws from a specific completed section
- No statistics dump — synthesize into actionable signal
- At least one positive finding
- At least one recommended action
- No segment labels, no health score, no bare numbers without time qualifiers
- Priority Actions block: 2–4 actions, highest urgency first (HIGH / MEDIUM / LOW urgency levels)
- Lower-priority actions may be wrapped in a collapsed `<details>` block

---

## 6. Appendix Contents

The Appendix is always included. It contains **data source attribution only**.

The Appendix is a client-facing section. Its purpose is to tell the client where the data in this report came from, what period it covers, and when it was last updated. Nothing more.

### Allowed in the Appendix

One row per data source used in the report. Each row states:
- what the data is (plain English name)
- what time period it covers (or "as of [date]" for point-in-time sources)
- when it was last updated

Peer benchmark data rows must also include: "No individual account data is disclosed." The row uses the same plain-language cohort framing used in the §7 body (e.g., "Anonymized median and percentile data from comparable lighting accounts on the same platform bundle. No individual account data is disclosed."). Never include peer_group_n as a raw count, benchmark_confidence, peer_group_level, tier labels, or raw `peer_group_id_effective` literals.

For total all-channel business data (if used), the row must clarify: "Includes all sales channels — eCat, phone, EDI, trade shows, showroom, and any other origin. This is total all-channel business, not buyer self-service activity on a portal."

Inventory data rows (if used) must clarify: "Point-in-time snapshot only. We cannot determine how long any item has been out of stock."

### Forbidden in the Appendix

**The Appendix is attribution-only.** Every item below belongs in the validation log only — none of it belongs in the delivered Appendix, regardless of report mode.

- Omitted-sections tables or rationale — sections that are absent must be omitted silently; no explanation in the Appendix
- Report mode (standard / activation / reactivation) — do not state the report mode in the Appendix
- Run parameters, run date context beyond a data-currency date, or any generation metadata
- Platform bundle metadata (bundle name, bundle tier, feature flags as descriptions)
- Methodology notes of any kind
- Calculation documentation ([HYPOTHETICAL] formulas, [ESTIMATED] methodology explanation rows)
- Gating explanations or gate result summaries (e.g., "VM-45 was skipped because Gate 2 failed," "Portal Engagement section omitted — HAS_CLICKY = false")
- Partial-sync disclosure blocks (e.g., "ERP sync is partial; portal_orders may not reflect total business" — if a sync limitation affects a specific figure, note it inline in the section, not in the Appendix)
- Standing caveat blocks, data-quality disclaimers, or operational health warnings
- [ESTIMATED] tag explanation rows or any separate disclosure for extrapolated figures — the inline tag in the section is the complete disclosure; no Appendix entry is needed or allowed
- Org identity blocks
- Internal org IDs or org shortnames as raw values
- Internal table or column names (`portal_orders`, `is_marked_deleted`, `ecat_item_number`, etc.)
- VM codes or query IDs (VM-38a, Q-43, etc.)
- Gate flags or flag values (`HAS_CART = false`, `Gate 2 failed`, etc.)
- Row counts or data volume figures from queries
- Internal dataset/table paths (BigQuery paths, Clicky table names, etc.)
- Package or tooling language ("not a package defect," "pending engineering," "tooling limitation," "runtime workaround," etc.)
- Validation or operator commentary ("per documented requirement," "rows confirmed," etc.)
- Risk or expansion flags (internal CS data)
- Health score or health band in any form
- Internal segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused)
- Enrollment or onboarding references
- Import pipeline status, error details, or support recommendations

> **Note on [HYPOTHETICAL] and [ESTIMATED] tags in report body**: These tags appear inline in the sections where the projections and extrapolations are cited. They do not require a separate Appendix section. The inline tag plus the sentence it modifies is the complete disclosure. Do not add a separate calculation-documentation subsection in the Appendix.
