# Stage 4: Report Assembly
> **v1.1** — updated 2026-06-16. Folded §1 identity from section_01_executive_summary.md; removed validation_summary output.

## 1. Read Chain

1. Read `stage4_assembly.md` (this file)
2. Read `shared_rules.md`
3. Read `authority/html_report_template.html` — copy the `<style>` block verbatim
4. Read `cache/gate_flags.md` — for template parameter values and conditional section info
5. Read `cache/section_manifest.md` — for section inclusion/skip status
6. Read all `fragments/section_NN.html` files for INCLUDE sections
7. Read all `cache/section_NN_highlights.md` files for INCLUDE sections

## 2. Executive Summary (§1 of the report)

- **id**: `executive-summary`
- **title**: Executive Summary
- **section number**: 1
- **structure**: `<section id="executive-summary">` — NOT `<details class="section-collapse">`
- **built by**: Stage 4 assembler (not a Stage 2 section agent)

Executive Summary is always written LAST — after all section fragments are assembled.

### Compact presentation lock — no exceptions
The Executive Summary MUST use this structure exactly:
1. `<ul class="highlights">` with 5–6 numbered `<li>` items — FIRST element after section heading, NO prose before it
2. Priority Actions block
3. "Patterns that warrant a conversation" block (`.callout.insight` with 3 investigation-worthy questions)

**FORBIDDEN in the Executive Summary — these cause presentation drift and must never appear:**
- Any `<p class="prose">` before the highlights list — including a single "orientation sentence"
- Multiple `<p class="prose">` paragraphs before the highlights list
- A 3-paragraph narrative block above the highlights
- An introductory paragraph summarizing the whole account before the numbered list
- Any prose of any length before the highlights list
- Generic "action box" or `<div class="callout info"><ol>` replacing the Priority Actions block

### Highlight selection
- Read all `cache/section_NN_highlights.md` files
- Select 5–6 highlights from candidates, ranked by signal strength
- Each: **bold headline**, one sentence of context, section link (arrow to section-id)
- Each draws from a specific completed section
- **Dollar-first rule**: Every highlight MUST lead with a dollar figure or dollar-equivalent impact in the first clause. Percentages and counts are supporting evidence, not the headline. Example: "$2.2M at risk from 15 decelerating accounts" (not "15 accounts decelerating with $2.2M at risk"). If a highlight candidate has no plausible dollar figure, it is not strong enough for the executive summary — replace it with one that does.
- No statistics dump — synthesize into actionable signal
- At least one positive finding; at least one recommended action
- No segment labels, no health score, no bare numbers without time qualifiers
- Uses `<ul class="highlights"><li>` — NOT `<ol>`

### Priority Actions
- Select 2–4 from candidates, highest urgency first
- Use `.priorities` / `.priority` / `.priority-badge` / `.priority-title` / `.priority-desc` / `.priority-impact` pattern
- Include section link in each title
- Impact projections use hedging language ("potential," "could," "estimated") — literal `[HYPOTHETICAL]` tags must NOT appear in the HTML (see shared_rules.md Hard Rule 8)
- Wrap lower-priority actions in a collapsed `<details>` block

### Conversation Starters
After the Priority Actions block, add a "Patterns That Warrant a Conversation" block — 3 bullets drawn from the most investigation-worthy patterns in the data. These are NOT action items (those go in Priority Actions) — they are open questions that turn the report into a meeting agenda.

**Structure:**
```html
<div class="callout insight">
  <div class="callout-title">Patterns that warrant a conversation</div>
  <ol>
    <li>{{PATTERN_1}}</li>
    <li>{{PATTERN_2}}</li>
    <li>{{PATTERN_3}}</li>
  </ol>
</div>
```

**Selection criteria:**
- Each pattern must name a specific entity (account, rep, region, product) and a specific question
- Prefer cross-section patterns (e.g., a rep trend in §2 that correlates with a customer trend in §3)
- Frame as investigative questions, not conclusions — "Is this a territory reassignment or competitive dynamic?" not "This is a problem."
- Exactly 3 items. If the data only supports 2 strong patterns, a third can be a forward-looking question ("What's driving the Q2 acceleration in [region]?")

### HTML structure
- Open as `<section id="executive-summary">` — NOT a `<details class="section-collapse">`
- Section heading: `<span class="section-num">§1</span>` + `<h2 class="section-title">`
- Priority badge text: use "High" / "Medium" / "Low" (matching `.priority-badge` class variants `.high` / `.medium` / `.low`)
- Cross-link pattern in highlights: `<a href="#section-id">→ Section Name</a>`

## 3. Appendix (§9 of the report)

Open as `<section>` — NOT `<details class="section-collapse">`. One row per data source used. Each row states what the data is (plain English) and what time period it covers.

### Standard attribution rows

| Source used | Appendix row label | What to write |
|---|---|---|
| eCat orders (`orders`) | eCat Orders | "Submitted eCat orders from the platform database. Data current as of [DATE]." |
| Total all-channel business (`portal_orders`) | Total Business (All Channels) | "Orders synced from [client]'s business system — includes all channels: eCat, phone, EDI, trade shows, showroom, and any other origin. Total all-channel business, not buyer self-service activity on a portal. Data current as of [DATE]." |
| Customer accounts (`customers`) | Customer Data | "Account records from [client]'s business system as of [DATE]." |
| Inventory (`inventories`) | Inventory Data | "Point-in-time inventory snapshot as of [DATE]. We cannot determine how long any item has been out of stock." |
| Historical sales (`sales_data`) | Historical Sales Data | "All-time invoiced sales history from [client]'s business system. No invoice date available — figures are all-time cumulative, not period-specific." |
| Rep engagement (Mixpanel) | Rep Engagement Data | "Platform engagement event data aggregated per user. All-time cumulative totals as of [DATE]." |
| Portal traffic (Clicky) | Portal Traffic Data | "eCat Online portal analytics covering [PERIOD]. Includes daily visitors, pageviews, session duration, geographic traffic, and traffic sources." |
| Peer benchmarks | Peer Benchmark Data | "Anonymized median and percentile data from [PEER_GROUP_ID_EFFECTIVE] accounts. No individual account data is disclosed. Run date: [DATE]." If confidence is low/medium, add one plain-language directional framing sentence per `authority/peer_benchmark.md §7`. |
| Platform config (org_summary) | Platform Configuration | "Platform feature and configuration data as of [DATE]." |

### Data Completeness row (conditional)

Read `cache/section_confidence.md`. If **any** section's confidence tier is below FULL, add a single row at the end of the Appendix:

| `.appendix-label` | `.appendix-value` |
|---|---|
| Data Completeness | "Section-level data source notes appear at the bottom of each section. To discuss data integration options, contact your SuperCat account team." |

Use the standard `.appendix-row` / `.appendix-label` / `.appendix-value` classes. Add this row **once** regardless of how many sections are below FULL. If all sections are FULL, omit this row entirely.

### What never goes in the Appendix
- Omitted-sections tables or rationale
- Report mode
- Run parameters, generation metadata, platform bundle metadata
- Methodology notes or calculation documentation
- [ESTIMATED] tag explanation rows
- Gating explanations (e.g., "VM-45 skipped — Gate 2 failed")
- Partial-sync disclosure blocks
- Standing caveat blocks or data-quality disclaimers
- Org identity sections
- Internal identifiers: org IDs, table names, column names, VM codes, query IDs, dataset paths
- Package/tooling language, validation commentary, operator notes
- Import pipeline status or error details
- Risk/expansion flags, health score, internal segment labels, enrollment references

Projections and extrapolations use hedging language in client-facing HTML — literal `[HYPOTHETICAL]` and `[ESTIMATED]` tags are internal pipeline markers that appear only in cache/highlight files, never in delivered HTML. No Appendix subsection for projection methodology is needed or allowed.

## 4. HTML Assembly

### Build order
1. `<!DOCTYPE html>` + `<html>` + `<head>` — copy `<style>` block from `html_report_template.html` verbatim
2. Google Fonts link: `DM Sans` + `IBM Plex Mono`
3. `<body>` + `<div class="page">`
4. Header: `.header` > `.h-brand` ("Insightful · Customer Intelligence") + `.h-customer` + `.h-type` ("Customer Intelligence Report" for Mode 1) + `.h-meta` (format: "{{PERIOD_START}} – {{PERIOD_END}} (Trailing 12 Months) · Report Date: {{REPORT_DATE}} · {{BUNDLE_LABEL}}") + `.h-accent`
5. TOC: `<nav class="toc-strip" id="tocStrip">` — links only to INCLUDE sections from manifest
6. Executive Summary (§1)
7. Section fragments (§2–§8) in order — paste validated fragments verbatim
8. Appendix (§9) — open `<section>`, not `<details>`
9. Footer + JavaScript — copy scroll-spy script from template verbatim. The script MUST include the `openAndScroll` function: when a TOC link or highlight cross-link targets a collapsed `<details>` section, the script opens the `<details>` element before scrolling to the anchor. If the template script includes this function, copy verbatim. If it does not, add it.
10. Close `</div>` + `</body>` + `</html>`

### Template parameter substitution
Replace all `{{PARAM}}` placeholders with values from `cache/gate_flags.md`:
`{{CLIENT_NAME}}`, `{{REPORT_DATE}}`, `{{PERIOD_START}}`, `{{PERIOD_END}}`, `{{PERIOD_LABEL}}`, `{{ORG_SHORTNAME}}`, `{{BUNDLE_LABEL}}`

### Section inclusion
INCLUDE sections: paste fragment verbatim. SKIP sections: remove entirely — no placeholder, no "coming soon."

### Locked section ID verification (MANDATORY)

Before pasting each fragment, verify its `id` attribute matches the locked contract. If a fragment uses the wrong ID, fix it before pasting.

| Section | Required `id` | Common mistakes to catch |
|---|---|---|
| §1 Executive Summary | `executive-summary` | `summary`, `exec-summary` |
| §2 Sales Team | `sales` | `sales-team`, `sales-team-performance` |
| §3 Customer | `customers` | `customer`, `customer-intelligence` |
| §4 Product | `product` | `product-inventory`, `products` |
| §5 Commerce | `commerce` | `commerce-analytics` |
| §6 Portal | `portal` | `portal-engagement` |
| §7 Peer | `peer` | `peer-benchmarking`, `benchmarking` |
| §8 Platform | `platform` | `platform-utilization`, `platform-feature` |

TOC links, Executive Summary cross-links, and the scroll-spy script all depend on these exact IDs. A mismatch breaks navigation.

### Data confidence footers
Data confidence footer divs (`.data-confidence`) are part of each section fragment — paste them verbatim during assembly. Do not strip, modify, relocate, or re-style them.

### HTML comment stripping
Before saving, strip ALL `<!-- -->` nodes: operator guidance (`<!-- Operator: ... -->`), gating markers (`<!-- BEGIN/END ... GATE -->`), `<!-- HAS_* -->` flag references, `<!-- EXAMPLE ROW -->` hints, section banners (`<!-- ═══ §N ... ═══ -->`), and any other comment. After generating, search output for `<!--` — any hit must be resolved before saving.

### Forbidden patterns
- No `<header>` + `<main>` page-wrapper layout — use `.page` div structure
- No `--accent: #2563EB` or any blue-dominant palette
- No open `<section>` tags for §2–§8 — must be `<details class="section-collapse">`
- No `<p class="prose">` before highlights in Executive Summary
- No `<div class="callout info"><ol>` for priority actions
- No `<div class="h-title">` header format
- No single-font Google Fonts link without IBM Plex Mono pairing
- No `.section-contents` outside `<details class="section-collapse">` summary card
- No CSS not copied from `html_report_template.html`

## 5. Pre-Flight QC

Before saving, verify every check. If any fails, fix it before saving.

### Presentation
- [ ] Warm palette: `--accent: #C47A4A`, `--bg: #FAFAF8`, `--text: #2C2925` — not blue
- [ ] Google Fonts loads both `DM Sans` and `IBM Plex Mono`
- [ ] Header uses `.h-brand` + `.h-customer` + `.h-type` + `.h-meta` + `.h-accent` — not `<div class="h-title">`
- [ ] Exec Summary opens with `<ul class="highlights"><li>` as FIRST content — no `<p class="prose">` before it
- [ ] Priority Actions use `.priorities` > `.priority` cards — not `<div class="callout info"><ol>`
- [ ] §2–§8 use `<details class="section-collapse">` — not open `<section>` tags
- [ ] Each `<summary>` has meaningful `section-sub` and `section-contents`
- [ ] TOC is `<nav class="toc-strip" id="tocStrip">` — not `<nav class="toc">` with `<ol>`

### Structure
- [ ] §1 uses `id="executive-summary"` — NOT `id="summary"` or any other variant
- [ ] §2–§8 use locked IDs per the section ID table above (`sales`, `customers`, `product`, `commerce`, `portal`, `peer`, `platform`)
- [ ] §6 and §8 rendered as separate sections — not merged
- [ ] Summary layer written last
- [ ] TOC links only to sections actually rendered, using locked IDs
- [ ] Demand Signal Intelligence absent if HAS_CLICKY = false
- [ ] Peer Benchmarking included when peer data is available — not accidentally omitted
- [ ] All INCLUDE sections from manifest present in final output
- [ ] No remaining `{{PARAM}}` placeholders — all substituted

### Forbidden content
- [ ] Zero `<!--` HTML comment nodes in delivered HTML
- [ ] "ERP" not in report body (§1–§8 prose, labels, metric-notes, table footnotes)
- [ ] "Mixpanel" not in delivered HTML
- [ ] "Clicky" not in delivered HTML (body or Appendix)
- [ ] Internal Clicky table names / dataset paths / prefix values not in HTML
- [ ] `order_source = 'ipad'` code literals not in client-facing prose
- [ ] "health score" / "health scores" not anywhere in delivered HTML
- [ ] `benchmark_confidence`, `peer_group_level`, `peer_group_n` not in client-facing HTML
- [ ] `operational_health_score` row uses `peer-metric-title` = "Data & Operational Health" (if §7 present)

### Appendix contract
- [ ] Attribution rows only — no omitted-sections table, methodology, calculation docs
- [ ] No report mode, run parameters, or platform bundle metadata
- [ ] No gating explanations, partial-sync blocks, standing caveats, [ESTIMATED] explanation rows
- [ ] Plain language only — no internal table names, column names, org IDs, VM codes, query IDs, dataset paths
- [ ] No operator/debug language ("package defect," "pending engineering," "Gate 2 failed," etc.)

## 6. Save Output

- **HTML**: `output/{{shortname}}_{{YYYY-MM-DD}}_intelligence_report.html`
