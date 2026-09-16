# Stage 4: Report Assembly
> **v1.0** — validated 2026-04-17 (RENWIL run). Last updated: 2026-04-17.

## 1. Read Chain

1. Read `stage4_assembly.md` (this file)
2. Read `shared_rules.md`
3. Read `report-system/html_report_template.html` — copy the `<style>` block verbatim
4. Read `cache/gate_flags.md` — for template parameter values and conditional section info
5. Read `cache/section_manifest.md` — for section inclusion/skip status
6. Read all `fragments/section_NN.html` files for INCLUDE sections
7. Read all `cache/section_NN_highlights.md` files for INCLUDE sections

## 2. Executive Summary (§1 of the report)

Executive Summary is always written LAST — after all section fragments are assembled.

### Compact presentation lock — no exceptions
The Executive Summary MUST use this structure exactly:
1. `<ul class="highlights">` with 5–6 numbered `<li>` items — FIRST element after section heading, NO prose before it
2. Priority Actions block

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
| Peer benchmarks | Peer Benchmark Data | "Anonymized median and percentile data from [PEER_GROUP_ID_EFFECTIVE] accounts. No individual account data is disclosed. Run date: [DATE]." If confidence is low/medium, add one plain-language directional framing sentence per `dependencies/PEER_BENCHMARK.md §7`. |
| Platform config (org_summary) | Platform Configuration | "Platform feature and configuration data as of [DATE]." |

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

Before saving, verify every check. If any fails, flag in the validation summary — do not silently deliver.

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
- [ ] §6 and §8 rendered as separate sections — not merged
- [ ] Summary layer written last
- [ ] TOC links only to sections actually rendered
- [ ] Portal Engagement absent if HAS_CLICKY = false
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

- **HTML** (primary): `output/{{shortname}}_{{YYYY-MM-DD}}_intelligence_report.html`
- **Validation summary**: `output/{{shortname}}_{{YYYY-MM-DD}}_validation_summary.md`
