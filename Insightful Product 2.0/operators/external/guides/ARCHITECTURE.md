> **DESIGN HISTORY (2026-06-12).** Not a runtime entry point — the canonical flow is `operators/external/run_prompt.md` (see `operators/external/guides/orchestrator.md`). Retained in place because `operators/external/guides/stage1_preflight_and_queries.md` cites this file's cache-format spec (§4/§5). Do not delete or move without first migrating that spec into the guides.

# Staged Report Generation — Architecture Specification (LOCKED)

> **Purpose**: Complete blueprint for decomposing the monolithic v2 operator into a staged, multi-agent pipeline. This document governs the design of all staged operator files.
>
> **Source of truth**: `Insightful Product 2.0/operators/01_generate_external_report_v2.md` — every rule, query reference, gate condition, and rendering spec in this design is extracted from the v2 operator. Nothing is invented. Nothing is reinterpreted.

---

## 1. Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  USER INPUT: org shortname (e.g., "wwjc")                   │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 1: DATA GATHERER                                     │
│  ─────────────────────                                      │
│  • Resolve org identity                                     │
│  • Stage 0: Minimum-commerce gate → determine report mode   │
│  • If Mode 2/3: generate simple report directly. DONE.      │
│  • If Mode 1: run full preflight (all gates)                │
│  • Execute ALL queries, save to cache/                      │
│  • Pre-compute derived gates (VM-45, showroom, Mixpanel)    │
│  • Output section manifest                                  │
│  • Self-validate (counts > 0, tables exist)                 │
│                                                             │
│  Reads: stage1_preflight_and_queries.md, SKILL.md,          │
│         query_library.md                                    │
│  Writes: cache/gate_flags.md, cache/section_manifest.md,    │
│          cache/Q-*_results.md, cache/peer_benchmark_extract  │
│  MCP: Postgres + BigQuery (ONLY stage that needs MCP)       │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
               USER REVIEWS gate_flags.md
               + section_manifest.md
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 2: SECTION BUILDERS (parallel — one per section)     │
│  ──────────────────────────────────────────────────         │
│  • Each reads: shared_rules.md + section_NN_*.md            │
│    + relevant cache/Q-*_results.md files                    │
│  • Each writes: fragments/section_NN.html                   │
│    + cache/section_NN_highlights.md                         │
│  • No MCP needed — file read/write only                     │
│  • All sections launched in parallel                        │
│                                                             │
│  Agents: §2, §3, §4, §5, §6 (if CLICKY), §7 (if peer), §8│
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 3: VALIDATORS (parallel — one per section)           │
│  ─────────────────────────────────────────────              │
│  • Each reads: shared_rules.md + section_NN_*.md            │
│    + fragments/section_NN.html                              │
│  • Each writes: cache/validation_section_NN.md              │
│  • Per-section context: ~370 lines max                      │
│  • Aggregate results into validation_checklist.md           │
│  • If any section FAIL: re-dispatch = full regeneration     │
│    (agent gets guide + cache, NOT its previous fragment)    │
│  • Max 2 re-dispatches per section; then flag for human     │
│  • All validations launched in parallel                     │
│  • No MCP needed — file read only                           │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
               USER REVIEWS validation_checklist.md
               Authorizes re-dispatches or proceeds
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 4: ASSEMBLER                                         │
│  ─────────────────────                                      │
│  • Read all validated fragments + all highlight files        │
│  • Write Executive Summary (from highlights — written LAST) │
│  • Build Appendix (attribution-only rows)                   │
│  • Assemble full HTML: header + CSS + TOC + §1–§9 + footer  │
│  • Run pre-flight QC (grep: forbidden phrases, HTML         │
│    comments, missing sections, label compliance)            │
│  • Output: final report + validation summary                │
│  • No MCP needed — file read/write only                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. File Structure

### Permanent operator files (never change between runs)

```
Insightful Product 2.0/
├── operators/
│   ├── 01_generate_external_report_v2.md        ← marked REFERENCE ONLY
│   └── staged/
│       ├── ARCHITECTURE.md                       — this document
│       ├── orchestrator.md                       ~60 lines  — execution checklist + mechanics
│       ├── shared_rules.md                       ~165 lines — semantic rules, fragment contract, CSS ref
│       ├── stage1_preflight_and_queries.md       ~600 lines — gates, queries, cache format, manifest
│       ├── section_02_sales_team.md              ~100 lines — §2 subsections 1–6, all rendering guidance
│       ├── section_03_customers.md               ~70 lines  — §3 subsections 1–5
│       ├── section_04_product.md                 ~90 lines  — §4 subsections 1–5 + empty guard
│       ├── section_05_commerce.md                ~80 lines  — §5 subsections 1–7 + VM-45 gate
│       ├── section_06_portal.md                  ~50 lines  — §6 subsections 1–4 (Clicky only)
│       ├── section_07_peer.md                    ~140 lines — §7 subsections 1–6 + whitelist + math
│       ├── section_08_platform.md                ~80 lines  — §8 subsections 1–6
│       ├── stage3_validator.md                   ~80 lines  — validation checklist spec
│       └── stage4_assembly.md                    ~150 lines — exec summary + appendix + HTML assembly + QC
```

### Per-run workspace (ephemeral — one per client per run date)

```
Insightful Product 2.0/
├── runs/
│   └── {{shortname}}_{{YYYY-MM-DD}}/
│       ├── cache/
│       │   ├── gate_flags.md
│       │   ├── section_manifest.md
│       │   ├── Q-01_step1_results.md
│       │   ├── Q-01_step2_results.md
│       │   ├── Q-08_results.md
│       │   ├── ... (one file per executed query)
│       │   ├── peer_benchmark_extract.md
│       │   ├── showroom_scan_results.md
│       │   ├── validation_section_02.md
│       │   ├── validation_section_03.md
│       │   ├── ... (one per validated section)
│       │   ├── validation_checklist.md          ← aggregated
│       │   ├── section_02_highlights.md
│       │   ├── section_03_highlights.md
│       │   └── ... (one per built section)
│       ├── fragments/
│       │   ├── section_02.html
│       │   ├── section_03.html
│       │   └── ... (one per built section)
│       └── output/
│           ├── {{shortname}}_{{YYYY-MM-DD}}_intelligence_report.html
│           └── {{shortname}}_{{YYYY-MM-DD}}_validation_summary.md
```

### Cache file naming convention (locked)

```
Q-{ID}_results.md              — single-step queries (e.g., Q-08_results.md)
Q-{ID}_step{N}_results.md      — multi-step queries (e.g., Q-01_step1_results.md)
Q-CL-{ID}_results.md           — Clicky queries (e.g., Q-CL-01_results.md)
Q-CI-{ID}_results.md           — peer benchmark queries (e.g., Q-CI-03_results.md)
peer_benchmark_extract.md      — pre-extracted peer CSV data
showroom_scan_results.md       — operational account exclusion evidence
```

Section manifest (§5) references these exact filenames. Do not deviate.

---

## 3. Data Cache Format

Every query result is saved as a markdown file with a metadata header. This is the contract between Stage 1 (data gatherer) and Stage 2 (section builders).

### Example: `cache/Q-01_step2_results.md`

```markdown
# Q-01 Step 2: Rep Activity Leaderboard
- **Org**: Wildwood / Chelsea House (wwjc, org_id=8)
- **Period**: Trailing 12 months (iPad orders, is_submitted=true)
- **Rows**: 21 qualifying field reps (1 showroom excluded)
- **Showroom excluded**: Atlanta Showroom — 25 orders, $28,111 GMV (included in org totals, excluded from rep leaderboard)
- **Run date**: 2026-04-16

| Rep | Orders | GMV | AOV | Unique Customers |
|-----|--------|-----|-----|------------------|
| Daniel Ratchford | 412 | $835,682 | $2,029 | 181 |
| Roger Miles | 91 | $130,403 | $1,433 | 47 |
| Katherine McMullan | 90 | $136,748 | $1,519 | 52 |
| ... | ... | ... | ... | ... |
```

### Rules for all cache files:
- **Header**: query ID, org context, period, row count, run date, any exclusions applied
- **Body**: markdown table with all result columns
- **No truncation**: include all rows returned by the query (the section agent decides what to display)
- **No interpretation**: raw data only — no narrative, no "What this tells you," no analysis
- **Dollar formatting**: use `$X,XXX` or `$X.XM` consistently
- **Null handling**: show `—` for null values, never omit the row

---

## 4. Gate Flags Format

### `cache/gate_flags.md`

```markdown
# Gate Flags — {{CLIENT_NAME}} ({{shortname}}, org_id={{ORG_ID}})
- **Run date**: {{YYYY-MM-DD}}
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | false | org_summary.has_clicky_portal = false |
| HAS_CART | true | org_summary.has_cart = true; server order count = 4,968 |
| HAS_PORTAL_ORDERS | true | LTM portal_order_count = 14,832 |
| HAS_INVENTORY | true | inventory_count = 3,935 |
| HAS_SALES_DATA | true | sales_data_count = 98,285 |
| HAS_SALES_SECTION | true | 21 qualifying reps (≥10 iPad orders LTM) |
| HAS_PEER_DATA | true | peer_benchmark_2026-04-14.csv present, benchmark_eligible = True |
| BENCHMARK_ELIGIBLE | true | — |
| BENCHMARK_CONFIDENCE | high | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 8 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Lighting / Full | Source for plain-language cohort framing |
| CLICKY_PREFIX | — | N/A (HAS_CLICKY = false) |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | PASS | portal_orders_gmv ($17.83M) > ecat_gmv ($8.95M) |
| VM45_GATE_2 | PASS | ecat_gmv ($8.95M) >= 5% of portal_orders_gmv ($891K threshold) |
| VM45_RENDER | true | Both gates pass — render capture rate subsection |
| QUALIFYING_REP_COUNT | 21 | Number of reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 18 rows — subsections §2.2–§2.4 viable |
| SHOWROOM_EXCLUSIONS | 1 | See showroom_scan_results.md for names + evidence |

## Org Identity

- **Client name**: Wildwood / Chelsea House
- **Shortname**: wwjc
- **Org ID**: 8
- **Bundle**: Full (iPad + eCat Online + B2B Cart + Sales Portal)
- **Bundle label for report**: "Full · iPad + eCat Online + Sales Portal"

## Validation Log

- portal_orders: org_summary has_portal = true, LTM count = 14,832 → HAS_PORTAL_ORDERS = true
- Showroom scan: "Atlanta Showroom" identified — 25 orders, $28K — excluded from rep leaderboard
```

### Derived gate rule:
Any gate that requires computation or cross-referencing query results MUST be resolved in Stage 1 and stored as a pre-computed flag. Section agents consume booleans and pre-computed values — they never re-derive gates from raw query data.

---

## 5. Section Manifest Format

### `cache/section_manifest.md`

```markdown
# Section Manifest — {{CLIENT_NAME}} ({{shortname}})

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE | HAS_SALES_SECTION = true | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE | HAS_INVENTORY = true | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | SKIP | HAS_CLICKY = false | — |
| 7 | Peer Benchmarking | INCLUDE | HAS_PEER_DATA + ELIGIBLE + not tier4 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

## Query-to-Section Mapping (cache files each section agent reads)

| Section Agent | Cache Files |
|--------------|-------------|
| section_02 | Q-01_step1_results, Q-01_step2_results, Q-02_results, Q-03_results, Q-06_results, Q-43_results, showroom_scan_results, gate_flags |
| section_03 | Q-12_results, Q-14_results, Q-17_results, Q-40_results, Q-41_results, gate_flags |
| section_04 | Q-07_results, Q-37_results, Q-38a_results, Q-39_results, Q-42_results, gate_flags |
| section_05 | Q-13_results, Q-16_results, Q-18_results, Q-20_results, Q-21_results, Q-45_results, gate_flags |
| section_06 | Q-CL-01_results, Q-CL-03_results, Q-CL-05_results, gate_flags |
| section_07 | peer_benchmark_extract, Q-CI-03_results, Q-CI-05_results, gate_flags |
| section_08 | Q-07_results, Q-08_results, Q-09_results, Q-10_results, Q-11_results, Q-22_results, gate_flags |
```

---

## 6. Fragment Contract

Every section agent produces an HTML fragment wrapped in this exact structure. No variation.

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
    <!-- ALL SUBSECTION CONTENT HERE -->
  </section>
</details>
```

### Section IDs and titles (locked):

| § | id | Title |
|---|----|-------|
| 2 | sales | Sales Team Performance |
| 3 | customers | Customer & Buyer Intelligence |
| 4 | product | Product & Inventory Intelligence |
| 5 | commerce | Commerce Analytics |
| 6 | portal | Portal Engagement |
| 7 | peer | Peer Benchmarking |
| 8 | platform | Platform & Feature Utilization |

### Fragment rules:
- Fragment starts with `<details` and ends with `</details>` — nothing before or after
- No `<html>`, `<head>`, `<body>`, or `<style>` tags — the assembler adds those
- No HTML comments (`<!-- -->`) in the fragment
- `section-contents` lists every rendered subsection by name, separated by ` · ` (`&middot;`)
- `section-sub` is a data-dense one-liner, not a generic description
- Every subsection uses `<div class="subsection">` with `<div class="subsection-title">` as its first child
- Every subsection ends with a `<div class="what-this-means">` close (exception: §2.4 Coaching Opportunities — omits what-this-means per shared_rules.md Section D)

---

## 7. Highlight Candidates Format

Each section agent outputs a highlight file alongside its HTML fragment.

### Example: `cache/section_02_highlights.md`

```markdown
# §2 Sales Team Performance — Highlight Candidates

1. **21-rep field team with mixed momentum** — Daniel Ratchford leads at $836K iPad GMV but is trending down (-37% recent vs. prior 90 days). Tammy Preusse and Katherine McMullan are trending strongly upward. [→ §sales]
2. **Four distinct selling archetypes identified** — Volume Relationship Sellers drive breadth; Precision Closers drive deal size. Coaching should be archetype-specific, not one-size-fits-all. [→ §sales]
3. **Two reps with quantified coaching upside** — Erica Stein (+$45K potential annual GMV) and pcain (+$35K potential) show high browse activity with low submission conversion. [→ §sales]

## Priority Action Candidate
- **HIGH**: Activate per-user ordering across the team — orders-per-user is below peer median (0.09 vs. 0.14). Target reps with high browse but low submission for workflow coaching. Impact: meaningful incremental GMV [HYPOTHETICAL]. [→ §sales]
```

### Rules:
- 2–4 highlight candidates per section, ranked by signal strength
- Each follows the Executive Summary format: **bold headline**, one sentence of context, section link
- 0–1 priority action candidates per section with urgency level
- The Stage 4 assembler selects the top 5–6 highlights and 2–4 priority actions from all candidates
- Section agents do not write the Executive Summary — they only propose candidates

---

## 8. Validation Checklist Format

### Per-section validation file: `cache/validation_section_NN.md`

Each validator agent reads ONE section's guide + ONE fragment + shared_rules.md (~370 lines total). It produces a per-section result:

```markdown
# Validation: §2 Sales Team Performance

| Check | Status | Evidence |
|-------|--------|----------|
| Subsection 1: Rep Activity Ladder | PASS | subsection-title found |
| Subsection 2: Behavioral Scorecard | PASS | subsection-title found |
| Subsection 3: Selling Archetypes | PASS | subsection-title found; 4-column table present |
| Subsection 4: Coaching Opportunities | PASS | subsection-title found; .coaching-card elements found (2 cards) |
| Subsection 5: Rep Engagement Trajectory | PASS | subsection-title found |
| Rendering: Coaching uses cards not prose | PASS | .coaching-card class found; no bare prose in coaching subsection |
| Rendering: Archetype table has 4 cols | PASS | Archetype / Rep(s) / Signature / Implication |
| Forbidden phrases | PASS | Zero matches: "health score", "portal orders", "ERP", "Mixpanel" |
| Fragment contract | PASS | Opens with <details>, closes with </details>, correct id |
| what-this-means closes | PASS | Found for all 5 subsections |

**VERDICT: PASS**
```

### Aggregated file: `cache/validation_checklist.md`

Produced by mechanically concatenating per-section results (no synthesis, no interpretation):

```markdown
# Fragment Validation — {{CLIENT_NAME}} ({{shortname}})

## Summary

| § | Verdict | Issues |
|---|---------|--------|
| 2 | PASS | — |
| 3 | PASS | — |
| 4 | PASS | — |
| 5 | FAIL | Missing subsection 3: Top Buyers & Concentration |
| 7 | PASS | — |
| 8 | PASS | — |

## Re-dispatch Required

- **§5**: Missing "Top Buyers & Concentration (Q-13)" subsection. Data available in cache/Q-13_results.md.

## Per-Section Detail

[concatenated per-section validation tables below]
```

---

## 9. Re-dispatch Protocol

If a section fails validation:

1. **Re-dispatch is FULL REGENERATION, not targeted edit.** The section agent receives a fresh prompt containing:
   - `shared_rules.md`
   - `section_NN_*.md` (the full section guide)
   - Relevant `cache/Q-*_results.md` files
   - A **failure note** stating what was missing or wrong (e.g., "Your previous attempt was missing Coaching Opportunities as individual `.coaching-card` elements — the guide specifies this format")
   - The agent does **NOT** receive its previous fragment. It regenerates from scratch.

2. **Max 2 re-dispatches per section.** If a section fails validation after 2 full regenerations, flag for human review. At that point the issue is likely a guide deficiency or a data gap, not an agent execution failure.

3. **Why full regeneration, not targeted edit:** Targeted edits cause spotlight effects — the agent focuses on fixing X and loses track of Y, Z. This is the exact pattern that caused Pass 2 regressions. Full regeneration from an ~80-line guide is cheap (~30 seconds) and eliminates edit-induced regression entirely.

---

## 10. Shared Rules — Content Specification

`shared_rules.md` contains rules that apply to ALL section agents. It is deliberately compact (~165 lines).

### What goes in shared_rules.md:

**A. Semantic guardrails table** (from v2 operator "Non-Negotiable Semantics")
- The full term/meaning/forbidden table
- Segment label prohibition
- Health score prohibition
- benchmark_confidence/peer_group_level/peer_group_n = internal only

**B. Hard Rules**
- Rules 1–10 (plus 11) from v2 operator, copied verbatim

**C. Forbidden phrases list**
- "health score" / "health scores"
- "portal orders" / "portal ordering" (as buyer activity or entity label)
- "net-new customers"
- "ERP" (in any client-facing text)
- "Mixpanel" / "Clicky" (use "platform engagement data" / only if HAS_CLICKY)
- Segment labels: "Platform-Embedded", "Commerce-Active", "Catalog-Focused"
- Internal identifiers: VM codes, query IDs, table names, column names, org IDs
- "bounce_rate"
- Code literals like `order_source = 'ipad'` in client-facing prose
- "benchmark_confidence", "peer_group_level", "peer_group_n" as labels

**D. Universal formatting rules**
- Every metric has a time qualifier
- `[HYPOTHETICAL]` on projections; `[ESTIMATED]` on extrapolations
- Dollar formatting: `$X,XXX` or `$X.XM`
- No bare numbers without context
- Every subsection ends with a "What this tells you" close (exception: §2.4 Coaching Opportunities)

**E. Fragment contract** (the exact HTML wrapper from §6)

**F. CSS class quick-reference** (from html_report_template.html)

**G. Highlight candidate format** (the structure from §7)

**H. Display Limits**
- Maximum rows displayed per table, default visible rows, section-specific override precedence

**I. Progressive Disclosure**
- `[COLLAPSE]` tag semantics for inner `<details>` elements within section bodies

### What does NOT go in shared_rules.md:
- Section-specific rendering guidance (inline in section guides)
- Query SQL (in query_library.md, consumed by Stage 1 only)
- Gate resolution logic (in stage1_preflight_and_queries.md)
- Executive Summary rules (in stage4_assembly.md)
- Appendix contract (in stage4_assembly.md)

---

## 11. Section Guide — Content Specification

Each section guide contains ONLY what its agent needs. Nothing more.

### Structure (same for all section guides):

```markdown
# Section Guide: §N — Section Title

## Section Identity
- **id**: "section-id"
- **title**: "Section Title"
- **section number**: N
- **include when**: gate condition
- **skip when**: inverse gate condition

## Query Inputs
Read these cache files:
- `cache/Q-XX_results.md` — description
- `cache/Q-YY_results.md` — description
- `cache/gate_flags.md` — for conditional subsection gates

## Subsection Order (do not reorder — render every subsection whose gate is met)

1. **Subsection Name (Q-XX)** — gate condition if any
   [full rendering guidance: table columns, card structure, callout rules, omission rules]

2. **Subsection Name (Q-YY)** — gate condition if any
   [full rendering guidance]

...

## Section-Specific Rules
- [any rules unique to this section]

## Empty-Section Guard (if applicable)
- [conditions under which the entire section is omitted]
```

### Critical extraction rule:
Every line of rendering guidance in the v2 operator's §4.2–§4.8 maps to exactly one section guide. The build agent must verify: **for every line in v2 operator §4.X, there is a corresponding line in section_XX_*.md.** Nothing lost. Nothing summarized. Nothing reinterpreted.

---

## 12. Stage 4 Assembly — Content Specification

`stage4_assembly.md` handles three tasks the section agents cannot do:

### A. Executive Summary
- Extracted from v2 operator Stage 5 + Stage 6 presentation lock
- Reads all `cache/section_NN_highlights.md` files
- Selects 5–6 highlights + 2–4 priority actions from candidates
- Applies the compact presentation lock (highlights-first, no prose before list)
- Uses `<ul class="highlights"><li>` — NOT `<ol>`
- Priority Actions use `.priorities` > `.priority` cards
- Written LAST — after all section fragments are assembled

### B. Appendix
- Extracted from v2 operator Stage 6.4
- Attribution-only rows — one per data source used
- Uses the standard row templates from the operator
- Contains NOTHING from the forbidden list (methodology, gating explanations, internal identifiers, etc.)

### C. HTML Assembly
- Reads `authority/html_report_template.html` for the CSS `<style>` block (copy verbatim)
- Builds: `<!DOCTYPE html>` + `<head>` (CSS) + `<body>` (header + TOC + §1 + fragments + §9) + `</body>`
- TOC links only to INCLUDE sections from the manifest
- Populates all `{{PARAM}}` placeholders with values from `cache/gate_flags.md`
- Strips any remaining HTML comments (final grep for `<!--`)

### D. Pre-Flight QC
- Extracted from v2 operator Pre-Flight Quality Check
- Run every check; output results to validation summary
- If any check fails: flag in validation summary, do not silently deliver

---

## 13. Orchestrator — Content Specification

`orchestrator.md` is a ~60-line checklist. It does NOT duplicate content from other files. It references them.

For each stage, include:
- **What to run** (which file/guide)
- **What it reads** (input files)
- **What it writes** (output files with exact paths relative to run directory)
- **Execution model** (single Task vs. parallel Tasks, subagent type, MCP requirements)
- **Human checkpoint** (what the user reviews before proceeding)

Also include:
- The re-dispatch protocol summary (max 2, full regeneration, no previous fragment)
- A note that Mode 2/3 reports complete entirely within Stage 1

---

## 14. Execution Model (Cursor mechanics)

### Stage 1: Single Task
- **Subagent type**: `generalPurpose`
- **MCP access required**: Postgres (`user-supercat-postgres-vpn`) + BigQuery (`user-bigquery-admin`)
- **Prompt provides**: `stage1_preflight_and_queries.md` + `SKILL.md` + `query_library.md` + org shortname
- **Output**: all cache files written to `runs/{{shortname}}_{{date}}/cache/`
- The user reviews `gate_flags.md` and `section_manifest.md` before proceeding

### Stage 2: Multiple parallel Tasks
- **Subagent type**: `generalPurpose`
- **MCP access**: none needed — file read/write only
- **One Task per INCLUDE section** — all launched in a single message for parallel execution
- **Each prompt provides**: `shared_rules.md` + `section_NN_*.md` + specific cache file paths from the manifest
- **Each output**: `fragments/section_NN.html` + `cache/section_NN_highlights.md`

### Stage 3: Multiple parallel Tasks
- **Subagent type**: `generalPurpose` (read-only analysis + write validation result)
- **MCP access**: none needed
- **One Task per section** — all launched in a single message for parallel execution
- **Each prompt provides**: `shared_rules.md` + `section_NN_*.md` + `fragments/section_NN.html`
- **Each output**: `cache/validation_section_NN.md`
- **Aggregation**: a trivial follow-up Task concatenates per-section results into `validation_checklist.md`

### Stage 3 re-dispatch (if needed):
- New Task for the failed section only
- Prompt provides: guide + cache files + failure note
- Does NOT receive previous fragment
- Full regeneration from scratch
- Re-validate after regeneration

### Stage 4: Single Task
- **Subagent type**: `generalPurpose`
- **MCP access**: none needed
- **Prompt provides**: `stage4_assembly.md` + `shared_rules.md` + all fragment paths + all highlight paths + `html_report_template.html` + `gate_flags.md` + `section_manifest.md`
- **Output**: final HTML + validation summary in `runs/{{shortname}}_{{date}}/output/`

---

## 15. Build Order

| Phase | File | Depends On | Est. Lines |
|-------|------|-----------|------------|
| 2a | `shared_rules.md` | v2 operator §45–80 (semantics, hard rules) + §6.0 (rendering contract) | ~120 |
| 2b | `orchestrator.md` | Architecture spec (this document) | ~60 |
| 3a | `section_02_sales_team.md` | v2 operator §4.2 + shared_rules.md | ~100 |
| 3b | `section_03_customers.md` | v2 operator §4.3 + shared_rules.md | ~70 |
| 3c | `section_04_product.md` | v2 operator §4.4 + shared_rules.md | ~90 |
| 3d | `section_05_commerce.md` | v2 operator §4.5 + shared_rules.md | ~80 |
| 3e | `section_06_portal.md` | v2 operator §4.6 + shared_rules.md | ~50 |
| 3f | `section_07_peer.md` | v2 operator §4.7 + shared_rules.md + PEER_BENCHMARK.md | ~140 |
| 3g | `section_08_platform.md` | v2 operator §4.8 + shared_rules.md | ~80 |
| 4a | `stage1_preflight_and_queries.md` | v2 operator §0–§2 + SKILL.md | ~250 |
| 4b | `stage3_validator.md` | All section guides + validation checklist format | ~80 |
| 4c | `stage4_assembly.md` | v2 operator §5–§7 + Pre-Flight QC | ~150 |
| **TOTAL** | | | **~1,270** |

Phase 3 section guides (3a–3g) can be built in parallel — they have no dependencies on each other.

---

## 16. Extraction Verification Protocol

For every file built in Phases 3–4, the build agent must produce an extraction audit:

```markdown
## Extraction Audit: section_02_sales_team.md

### Source: v2 operator §4.2 (lines 523–593)

| v2 Operator Line/Rule | Present in Section Guide? | Location |
|----------------------|--------------------------|----------|
| Showroom pre-check (2-pass scan) | PRESENT | Lines 8–15 |
| Subsection 1: Rep Activity Ladder | PRESENT | Line 18 |
| Subsection 2: Behavioral Scorecard | PRESENT | Line 19–20 |
| Subsection 3: Selling Archetypes (full rendering guidance) | PRESENT | Lines 21–25 |
| Subsection 4: Coaching Opportunities (card format, potential framing) | PRESENT | Lines 26–30 |
| Subsection 5: Rep Engagement Trajectory | PRESENT | Line 31 |
| Subsection 6: Territory Coverage | PRESENT | Line 32 |
| Mixpanel dependency note (subsections 2–4) | PRESENT | Lines 34–35 |
| Clamp rule | PRESENT | Line 37 |

**Missing from source**: None
**Added beyond source**: None
```

This is the mechanical proof that nothing was lost in extraction. Every file gets one. No exceptions.

---

## 17. Context Load Summary

| Agent | Max Context | Task Type |
|-------|------------|-----------|
| **Monolithic (current)** | **~7,500 lines** | Data interpretation + narrative + HTML generation |
| Stage 1 (preflight) | ~3,000 lines | Mechanical query execution, no HTML |
| Stage 2 (section builder) | ~300–400 lines | Narrative + HTML from pre-gathered data |
| Stage 3 (validator) | ~370 lines | Pattern matching — guide vs. fragment |
| Stage 4 (assembler) | ~1,200 lines | Fragment stitching + highlight selection |

The hardest cognitive task (interpreting data, generating narrative, building structured HTML) happens at **300–400 lines of context** — a 95% reduction from the monolithic approach. Stage 4's higher context load is acceptable because assembly is categorically easier than generation: it's selecting from pre-written highlights and copy-pasting validated fragments.

---

## 18. Resolved Design Decisions

| Decision | Resolution | Rationale |
|----------|-----------|-----------|
| Cursor rule vs. prompt | Prompt. Orchestrator is a human-facing document. | A `.mdc` rule would inject ~60 lines into every agent, including section agents that only need their guide. |
| Re-dispatch limit | Max 2 re-dispatches, then flag human | If full regeneration fails twice, the issue is a guide deficiency or data gap, not agent execution. |
| Mode 2/3 architecture | Keep in `stage1_preflight_and_queries.md` | They're simple (3–4 sections, no cross-section dependencies). Extract later if they grow. |
| Gold reference in section guides | Self-contained. No external HTML reference. | Section guide IS the rendering spec. EXAMPLE CO patterns are already captured in the v2 operator guidance that feeds extraction. |
| Validator scope | Per-section (parallel), not all-at-once | Avoids the ~1,400-line attention danger zone. Same focused-agent principle as section builders. |
| Re-dispatch method | Full regeneration, not targeted edit | Targeted edits cause spotlight effects (Pass 2 regression pattern). Full regen from ~80-line guide is cheap and eliminates edit-induced regression. |

---

*END OF ARCHITECTURE SPECIFICATION*
