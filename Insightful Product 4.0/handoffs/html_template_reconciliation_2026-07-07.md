# Insightful Product 4.0 — HTML Template Reconciliation Handoff

**Date:** 2026-07-07
**Status:** The pipeline produces HTML. The HTML does not match the gold standard.
**Prior chat:** [Product recovery](876c6f43-23cd-42c5-8db8-2ad81c93b82c)

---

## The problem in one sentence

The deployed gold-standard report at **https://supercat-reports.pages.dev/sarreid/** uses the design system and section architecture from `_archive/html_report_template.html`. The 4.0 pipeline's `report.html.j2` diverged from that template — different sections, different components, different branding, and no native Mode-2/3 support. The Mode-2 ACTIVATION output is a wall of suppression notices instead of real platform-readiness content.

---

## Gold standard (what the client sees)

**File:** `_archive/html_report_template.html` (2,099 lines, 119K chars)
**Live:** https://supercat-reports.pages.dev/sarreid/ (access-code gated — branding reads `Insightful · Customer Intelligence`)

This is NOT wrong. This is NOT an old artifact to discard. It is the canonical HTML structure for every Insightful report — Mode 1, Mode 2, and Mode 3.

### What the gold standard has

| Component | Gold standard (2.0 template) | 4.0 pipeline (`report.html.j2`) |
|---|---|---|
| **Branding** | `Insightful · Customer Intelligence` | `Insightful · CEO Brief` |
| **Lines / size** | 2,099 lines / 119K | 381 lines / ~18K |
| **Mode 1 sections** | Signal Summary → Sales Team → Account Intelligence → Product Intelligence → Commerce Patterns → Platform Context → Appendix | 60-sec read → Do this week → Do this month → Growth → Team → Risk → Products → Dealer base → Channels → Methodology |
| **Mode 2 (Activation)** | Native: Activation Summary (highlights + priority actions) → Platform Readiness → Peer Benchmarking → Appendix | Not in HTML template. Hacked via `activation.md.j2` → 7 suppression notices piped through Mode-1 renderer |
| **Mode 3 (Reactivation)** | Native: Reactivation Summary → Historical Commerce → Platform Status → Peer Benchmarking → Appendix | Does not exist |
| **Key Highlights** | `<ul class="highlights">` — numbered highlight items with section anchor links | None — no equivalent component |
| **Priority Actions** | `.priorities` grid with urgency badges (High/Medium/Low), titles, descriptions, impact figures | Exists in CSS and used within summary section, but not as a standalone component pattern |
| **"What this tells you"** | `.what-this-means` box at the bottom of every subsection | Not present |
| **Peer Benchmarking** | Full component set: hero stat, narrative metric rows, range bars, quartile pills, top performers | Not present |
| **Data Confidence footer** | `.data-confidence` block per section | Not present |
| **Report mode banner** | `.mode-banner.activation` / `.mode-banner.reactivation` | Not present (gatestop has its own banner) |
| **Coaching cards** | Base style only in CSS (warn border-top); rich structural CONTENT patterns in operator comments (behavioral scorecards, selling archetypes, coaching opportunities) | More CSS variants (`.alarm`, `.growing`, `.pattern`) but less operator-guided content structure |
| **Progressive disclosure** | `details.section-collapse` for all sections | Same approach, compatible |
| **Sticky TOC** | Same `.toc-strip` pattern | Same, compatible |
| **CSS design system** | `--bg: #FAFAF8`, `--accent: #C47A4A`, DM Sans + IBM Plex Mono | Same vars, same fonts — shared DNA |
| **Print styles** | Full `@media print` with running header | Simplified `@media print` |
| **Template parameters** | `{{MUSTACHE}}` placeholders filled by LLM operator | Jinja2 `{{ variable }}` filled by Python pipeline |
| **Assembly model** | LLM operator + template = finished report | `gather.py` → `assemble.py` (Jinja2 MD) → `md_parse.py` → `sections.py` (Python section renderers) → `report.html.j2` |

### Mode 2 — the real gap

The gold standard's Mode 2 shows the client **what is configured and ready** — real data about their platform:

1. **Activation Summary** — 3–4 highlights about catalog/config readiness, peer context, 1–2 priority actions for first activation steps, "About this report" callout
2. **Platform Readiness** — catalog completeness, import health, seat utilization, config gaps (queries Q-08/09/10/11)
3. **Peer Benchmarking** — how similar accounts at this stage compare on catalog readiness and feature setup (conditional)
4. **Appendix** — data sources, freshness attribution, methodology

What the 4.0 pipeline produces for Mode 2 (after the 2026-07-07 recovery):

1. **60-second read** — one eCat GMV hero metric + posture table
2. **7 identical "suppressed" sections** — each says "connect ERP to unlock" and nothing else
3. **Channels** — one 2-cell table
4. **Unlock block** — a 10-row table listing what each section would show
5. **Appendix** — preflight posture dump

**The gold standard gives value.** The 4.0 ACTIVATION gives a wall of "you can't see this." That is the gap.

---

## Critical data gap — Q-08/09/10/11 NOT wired into the pipeline

The gold standard's Mode-2 Platform Readiness section uses queries Q-08, Q-09, Q-10, Q-11 (Data Freshness, Import Health, Feature Enablement, Configuration Completeness). These queries **exist in the query library** (`foundation/query_library_v2.md` lines 577–671) and are marked `Status: live | Source: Postgres MCP`. The SQL is defined and ready to run.

**However, the pipeline does NOT run or consume them:**

- `gather.py` only loads commerce-focused queries: `S1`, `RS-01`, `Q-CHAN-10`, `C2`, `Q-ECON-CONC`, `Q-ECON-CONTRIB`, `Q-PROD-TOP`, `Q-PROD-FAMILY`, `Q-DEALER-COHORT`, `Q-CROSS-SELL`
- `GatherBundle` (the dataclass that carries all gathered data) has NO fields for platform readiness, data freshness, import health, feature enablement, or configuration completeness
- For Mode-2 orgs, most of the existing gathered CSVs are empty anyway (no invoices = no decay, no reps, no products, no families, no dealer cohort)
- The `ecat_user_concentration` field referenced in `activation.md.j2` also does NOT exist in `GatherBundle` — the Jinja2 `is defined` check silently skips it

**What this means for the fix:** Building real Platform Readiness content requires:
1. Running Q-08/09/10/11 via Postgres MCP during cache population (`populate_cache.py`)
2. Adding new dataclasses to `gather.py` (e.g., `DataFreshness`, `ImportHealth`, `FeatureEnablement`, `ConfigCompleteness`)
3. Adding new loaders to `gather.py`
4. Adding new fields to `GatherBundle`
5. THEN the template can render real content

There is also **no peer benchmarking data** in the pipeline. No peer queries, no peer dataclasses, no peer loaders. If Mode-2 includes a peer section, that's a new data source to add.

---

## What is NOT wrong (keep these)

- **The pipeline plumbing works.** `run.sh` → `gather.py` → `preflight.py` → `assemble.py` → `smoke_check.py` → `html_renderer.py` → `step10_check.py`. The chain runs for all modes.
- **The ACTIVATION routing is correct.** `assemble.py` (line 78) correctly routes Mode-2 to `activation.md.j2`. `html_renderer.py` renders it. `smoke_check.py` and `step10_check.py` handle activation. This plumbing should stay.
- **The CSS design system is shared.** Both templates use the same colors, fonts, vars. Reconciling the HTML does not require a visual redesign.
- **The regression harness works.** `regression.sh` runs 6/6 (including `sca` ACTIVATION and `sarreid` SHIP). Keep it running.
- **Mode-1 Sarreid output is good.** The Sarreid SHIP report in `outputs/` is client-ready. Section names differ from the gold standard (60-sec read vs Signal Summary), but the content quality is there.

---

## What needs to happen

### Path A: Reconcile `report.html.j2` with the gold standard (preserves pipeline architecture)

**Layer 1 — Data (must come first):**
1. Add Q-08/09/10/11 to `populate_cache.py` so their CSVs land in `cache/{org}/{date}/`
2. Add dataclasses + loaders to `gather.py`: `DataFreshness`, `ImportHealth`, `FeatureEnablement`, `ConfigCompleteness`
3. Add these fields to `GatherBundle`
4. These queries run against Postgres MCP (same source as Q-ECON-00) — they work for ALL orgs regardless of mode

**Layer 2 — MD template:**
5. Rewrite `activation.md.j2` — from 7 suppression notices to real sections: Activation Summary (highlights, priority actions), Platform Readiness (freshness table, import health, feature gaps), Appendix
6. Update `md_parse.py` — add section IDs: `activation-summary`, `platform-readiness`, `appendix`

**Layer 3 — HTML template + renderers:**
7. Add Mode-2 HTML sections to `report.html.j2` — Activation Summary, Platform Readiness (port from gold standard lines 1872–1938, ~60 lines of HTML)
8. Add missing CSS to `report.html.j2` — `.highlights`, `.what-this-means`, `.mode-banner`, `.data-confidence`
9. Add `assemble_activation()` function to `html_renderer.py` — parallel to `assemble_mode1()` and `assemble_gatestop()`
10. Add section renderers to `sections.py`: `render_activation_summary()`, `render_platform_readiness()`

**Layer 4 — Validation + regression:**
11. Update `smoke_check.py` activation required sections to match new section names
12. Update `step10_check.py` if new sections introduce terms that need vocabulary rules
13. Refresh `golden_set.json` checksums for `sca` (and any other Mode-2 orgs)

### Path B: Adopt the gold standard template directly (larger rewrite)

Replace `report.html.j2` with the gold standard template. Refactor the pipeline to fill `{{MUSTACHE}}` slots instead of assembling free-form HTML:

1. Copy `_archive/html_report_template.html` → `report_render/templates/report.html.j2`
2. Convert `{{MUSTACHE}}` to Jinja2 `{{ var }}` and add conditionals
3. Refactor `html_renderer.py` to populate template vars instead of calling section renderers
4. Retire `sections.py` (its job moves to template var population)
5. Refactor `md_parse.py` to extract template vars from MD instead of chunking by H2
6. **Still need Layer 1 (data)** — Q-08/09/10/11 must be wired regardless of path

**Path A preserves the existing pipeline architecture and is lower risk.** Path B is a larger rewrite but produces exact gold-standard output. Both paths require the data layer work (Q-08/09/10/11).

### Decision for owner

Which path? The answer depends on whether Mode-1 section names should stay (60-sec read, Do this week) or align with the gold standard (Signal Summary, Sales Team, Account Intelligence). If Mode-1 section names stay, Path A. If they should match, Path B.

---

## File inventory

### Active pipeline (what runs today)

| File | Role |
|---|---|
| `report_render/templates/report.html.j2` | 381-line Jinja2 HTML template — the divergent descendant |
| `report_render/html_renderer.py` | Orchestrator: `render()` → `assemble_mode1()` or `assemble_gatestop()` → template |
| `report_render/md_parse.py` | Chunks MD by H2 → `ParsedReport` with section IDs |
| `report_render/sections.py` | Per-section HTML renderers (summary, thisweek, growth, team, …) |
| `report_render/md_render.py` | Markdown inline → HTML spans |
| `report_render/naming.py` | Filename derivation (ship, preview, activation) |
| `report_render/step10_check.py` | Post-render HTML validator |
| `pipeline/templates/activation.md.j2` | ACTIVATION MD template — 7 suppression notices + eCat table |
| `pipeline/templates/_base.md.j2` | Mode-1 MD template |
| `pipeline/templates/gatestop.md.j2` | Gate-STOP MD template |
| `pipeline/assemble.py` | Routes to correct MD template by mode; passes `posture` + `gather` + `signals` to Jinja2 context |
| `pipeline/gather.py` | Loads cached CSVs → `GatherBundle` dataclass (commerce-only today — NO platform readiness) |
| `pipeline/smoke_check.py` | Pre-render MD validator |
| `pipeline/preflight.py` | Determines `RunPosture` (mode, confidence, gates) from Q-ECON-00, Q-CHAN-00, RP-2 |
| `pipeline/run_report.py` | Pipeline orchestrator: cache → preflight → gather → signals → assemble → smoke_check |
| `run.sh` | Shell entry point (pipeline → render → validators → banner) |
| `pipeline/cache.py` | `CachePaths` — resolves `cache/{org}/{date}/` directory and CSV paths per query ID |

### Gold standard (the reference)

| File | Role |
|---|---|
| `_archive/html_report_template.html` | **THE gold standard.** 2,099-line template with Mode 1/2/3, full component library. Design and structural authority. |

### Data layer (queries that exist but aren't wired)

| Query | Defined at | What it returns | Needed for |
|---|---|---|---|
| Q-08 | `foundation/query_library_v2.md` line 577 | `data_versions` per entity — days since update, Fresh/Monitor/Stale | Platform Readiness (Mode 2) |
| Q-09 | line 599 | Monthly import counts + recent import error check | Platform Readiness (Mode 2) |
| Q-10 | line 631 | Feature flags: sales portal, online catalog, online ordering, kit items, contract prices, enrollments, SmartLists | Platform Readiness (Mode 2) |
| Q-11 | line 653 | `data_versions` rows >30 days stale + related record counts | Platform Readiness (Mode 2) |

All four run against **Postgres MCP** (same source as the preflight queries that already work). They need `{{ORG_ID}}` which `RunPosture.organization_id` already provides.

### Outputs (current quality)

| File | Mode | Quality |
|---|---|---|
| `outputs/Sarreid_CEO_intelligence_report_2026-06-29.html` | SHIP (Mode 1) | Good — client-ready, different section names from gold standard but strong content |
| `outputs/Shadow_Catchers_Activation_intelligence_report_2026-07-02.html` | ACTIVATION (Mode 2) | Bad — 7 suppression notices, no platform readiness |
| `outputs/Da_*_Activation_intelligence_report_2026-07-07.html` | ACTIVATION (Mode 2) | Bad — same problem as Shadow Catchers |

---

## Test commands

```bash
# Regression (must stay 6/6 after changes)
./regression.sh

# Mode 2 test org
./run.sh sca --date 2026-07-02

# Mode 1 regression anchor
./run.sh sarreid --date 2026-07-02
```

---

## Rules that carry forward

- Same CSS design system (colors, fonts, vars) — no visual redesign
- No fake invoiced dollars on NONE-commerce orgs (Mode 2)
- Mode 2 must show real platform readiness data, not suppression walls
- `smoke_check` and `step10_check` must not be weakened for Mode 1
- The deployed Sarreid at pages.dev is the client-facing reference
- The `_archive/html_report_template.html` is the structural authority

---

## Resume prompt

Paste this into a new chat to continue:

---

> **You are continuing the Insightful Product 4.0 HTML template reconciliation.**
>
> Read the handoff first:
> `Insightful Product 4.0/handoffs/html_template_reconciliation_2026-07-07.md`
>
> **Workspace:** `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Insightful Product 4.0/`
>
> **Summary:** The pipeline produces HTML reports. The Mode-1 Sarreid output (SHIP) is client-ready. The Mode-2 ACTIVATION output (da, sca) is broken — it renders 7 "suppressed — connect ERP" notices instead of real platform-readiness content. The gold standard template (`_archive/html_report_template.html`) has native Mode-2 support with Activation Summary, Platform Readiness, and Peer Benchmarking sections that show real value.
>
> **The critical gap is data, not just HTML.** The queries for Platform Readiness (Q-08, Q-09, Q-10, Q-11) exist in `foundation/query_library_v2.md` and run against Postgres MCP, but `gather.py` doesn't load them and `GatherBundle` has no fields for them. You must wire the data before you can render real content.
>
> **Your job:**
> 1. Read the handoff completely
> 2. Read the gold standard template: `_archive/html_report_template.html` (Mode-2 sections at lines 1872–1938)
> 3. Read the current pipeline: `gather.py`, `assemble.py`, `html_renderer.py`, `report_render/templates/report.html.j2`, `pipeline/templates/activation.md.j2`
> 4. Owner decision needed: Path A (port Mode-2 sections into existing pipeline) vs Path B (adopt gold standard template wholesale). If not specified, default to **Path A** — it's lower risk.
> 5. Implement in layers: Data (Q-08/09/10/11 → gather.py) → MD template (activation.md.j2) → HTML template + renderers → validation + regression
>
> **Test commands:**
> ```bash
> ./regression.sh          # must stay 6/6
> ./run.sh sca --date 2026-07-02   # must produce ACTIVATION HTML with real Platform Readiness content
> ./run.sh sarreid --date 2026-07-02  # must still SHIP (regression anchor)
> ```
>
> **Rules:**
> - `_archive/html_report_template.html` is the structural authority — do not discard it
> - Same CSS design system (shared vars/fonts) — no visual redesign needed
> - No fake invoiced dollars on Mode-2 orgs
> - Do not weaken `smoke_check` or `step10_check` for Mode-1
> - Mode 2 must show real platform data (freshness, import health, feature gaps), not suppression walls
