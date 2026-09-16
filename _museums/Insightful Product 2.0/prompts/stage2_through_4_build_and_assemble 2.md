# Stages 2–4: Build & Assemble — {{CLIENT_NAME}} ({{SHORTNAME}})

## Objective

You are the **section builder and assembler** for the Insightful Product 2.0 report pipeline. Stage 1 (data gathering) is complete. Your job is to:

1. **Stage 2**: Build all INCLUDE section fragments (§2–§8) and highlight files
2. **Stage 4**: Assemble the final HTML report

## Client Parameters

| Parameter | Value |
|-----------|-------|
| Client name | {{CLIENT_NAME}} |
| Shortname | {{SHORTNAME}} |
| Report date display | {{REPORT_DATE_DISPLAY}} |
| Period start | {{PERIOD_START}} |
| Period end | {{PERIOD_END}} |
| Bundle label | {{BUNDLE_LABEL}} |

## Run Directory

- **Cache**: `Insightful Product 2.0/runs/{{SHORTNAME}}_{{YYYY-MM-DD}}/cache/`
- **Fragments**: `Insightful Product 2.0/runs/{{SHORTNAME}}_{{YYYY-MM-DD}}/fragments/` (create if needed)
- **Output**: `Insightful Product 2.0/runs/{{SHORTNAME}}_{{YYYY-MM-DD}}/output/` (create if needed)

## Read Chain (do this first)

Read these files in order and internalize before building any section:

1. `Insightful Product 2.0/operators/staged/shared_rules.md` — forbidden phrases, hard rules, fragment contract, CSS classes, formatting
2. `Insightful Product 2.0/operators/staged/stage4_assembly.md` — assembly rules (you'll need this for Stage 4)
3. `Insightful Product 2.0/operators/staged/section_01_executive_summary.md` — Executive Summary rendering rules
4. `Insightful Product 2.0/report-system/html_report_template.html` — copy `<style>` (lines 160–448) and `<script>` (lines 2133–2174) VERBATIM
5. `Insightful Product 2.0/runs/{{SHORTNAME}}_{{YYYY-MM-DD}}/cache/gate_flags.md`
6. `Insightful Product 2.0/runs/{{SHORTNAME}}_{{YYYY-MM-DD}}/cache/section_manifest.md`
7. `Insightful Product 2.0/dependencies/PEER_BENCHMARK.md` — §7 peer framing rules (for §7 builder and Appendix)

---

## STAGE 2: Build Section Fragments

For each section marked INCLUDE in the section manifest, build the fragment in order: §2, §3, §4, §5, §6, §7, §8.

Skip any section marked SKIP — no placeholder, no mention.

### Per-section workflow

For each INCLUDE section:

**Step 1: Read the section guide**

| § | Guide |
|---|-------|
| 2 | `operators/staged/section_02_sales_team.md` |
| 3 | `operators/staged/section_03_customers.md` |
| 4 | `operators/staged/section_04_product.md` |
| 5 | `operators/staged/section_05_commerce.md` |
| 6 | `operators/staged/section_06_portal.md` |
| 7 | `operators/staged/section_07_peer.md` |
| 8 | `operators/staged/section_08_platform.md` |

**Step 2: Read the cache files** listed in the section manifest's Query-to-Section Mapping for this section. Also read `cache/gate_flags.md` for conditional subsection gates. For §2, also read `Insightful Product 2.0/report-system/query_library.md` for Q-02/Q-03 derivation rules.

**Step 3: Build the fragment** following the section guide exactly. Produce an HTML fragment matching the fragment contract from `shared_rules.md` Section E:

```html
<details class="section-collapse" id="{{SECTION_ID}}">
  <summary>
    <div>
      <h2 class="section-title"><span class="section-num">§{{N}}</span> {{TITLE}}</h2>
      <div class="section-sub">{{DATA_DENSE_STAT_LINE}}</div>
      <div class="section-contents">{{SUBSECTION_NAMES_MIDDOT_SEPARATED}}</div>
    </div>
    <span class="expand-hint">&#9662; Click to expand</span>
  </summary>
  <section class="section" style="margin-bottom:0;border-top:none;border-radius:0 0 var(--r) var(--r);">
    {{SUBSECTION_CONTENT}}
  </section>
</details>
```

**Locked section IDs**: `§2=sales`, `§3=customers`, `§4=product`, `§5=commerce`, `§6=portal`, `§7=peer`, `§8=platform`

**Step 4: Build the highlight file** — `cache/section_NN_highlights.md` with 2–4 candidates per `shared_rules.md` Section G. `[HYPOTHETICAL]` tags belong in highlight files (internal cache). They must NOT appear in the HTML fragment.

**Step 5: Save**
- Fragment: `fragments/section_NN.html`
- Highlights: `cache/section_NN_highlights.md`

### Context management

After saving each section's fragment and highlights, treat them as done. Focus on the next section's guide + cache files. Do not re-read previous fragments during section building.

---

## STAGE 4: Assemble Final Report

After all INCLUDE sections are built, assemble the final HTML report.

### Read (if not already in context)
- `report-system/html_report_template.html` — for `<style>` and `<script>` blocks
- All `cache/section_NN_highlights.md` files
- All `fragments/section_NN.html` files
- `cache/gate_flags.md` — for template parameters and Appendix data

### Build order (per stage4_assembly.md §4)

1. **HTML boilerplate**: `<!DOCTYPE html>`, `<html lang="en">`, `<head>`, `<meta>`, `<title>{{CLIENT_NAME}} — Customer Intelligence Report</title>`, Google Fonts (DM Sans + IBM Plex Mono), `<style>` block VERBATIM from template
2. **Body + page wrapper**: `<body>`, `<div class="page">`
3. **Header**: `.h-brand` ("Insightful · Customer Intelligence"), `.h-customer` ({{CLIENT_NAME}}), `.h-type` ("Customer Intelligence Report"), `.h-meta` ("{{PERIOD_START}} – {{PERIOD_END}} (Trailing 12 Months) · Report Date: {{REPORT_DATE_DISPLAY}} · {{BUNDLE_LABEL}}"), `.h-accent`
4. **TOC**: `<nav class="toc-strip" id="tocStrip">` — links only to INCLUDE sections + Executive Summary + Appendix
5. **Executive Summary (§1)**: `<section id="executive-summary">` — built LAST from highlight candidates. Structure: `<ul class="highlights">` (5–6 items, NO prose before it) + `.priorities` > `.priority` cards (2–4, highest urgency first, lower priority collapsed in `<details>`). Strip `[HYPOTHETICAL]` tags from highlight text — use hedging language instead.
6. **Section fragments (§2–§8)**: Paste each fragment VERBATIM in order
7. **Appendix (§9)**: `<section id="appendix">` — attribution rows only per stage4_assembly.md §3. Include only data sources actually used (check gate_flags). Peer benchmark row includes directional framing per PEER_BENCHMARK.md §7 when confidence is low/medium.
8. **Footer**: `.footer` with brand and generation date
9. **JavaScript**: `<script>` block VERBATIM from template (includes scroll-spy + `openAndScroll`)
10. **Close**: `</div>`, `</body>`, `</html>`

### Template parameters

Replace all `{{PARAM}}` from gate_flags.md Org Identity section. Verify zero remaining `{{` after substitution.

### Save

- `output/{{SHORTNAME}}_{{YYYY-MM-DD}}_intelligence_report.html`

---

## Final Report to Chat

After saving, report:

1. Per-section build status (which built, which skipped)
2. Highlight selection (count, which sections)
3. Priority action count and urgency levels
4. Appendix rows included
5. Output file size
6. Confirmation: report is ready for browser review
