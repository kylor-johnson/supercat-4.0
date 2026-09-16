# Insightful Product 2.0 — HTML Output Tuning Handoff

You are picking up work on the Insightful Product 2.0 external report system. The data gathering pipeline is complete and verified. Your job is to **tune the HTML output** — the section building and assembly phase (Steps 2-3 of the run prompt). Read this entire handoff before starting any work.

---

## System Overview

This system generates per-client Customer Intelligence Reports from eCat platform data, Mixpanel behavioral analytics, BigQuery warehouse data, and (where available) ERP order data synced to `portal_orders`.

**Entry point**: `Insightful Product 2.0/operators/external/run_prompt.md`

The workflow has 4 steps:
1. **Data Gathering** (Step 1) — a Python script (`scripts/data_gather.py`) that runs ~40 queries in parallel and writes cache files in ~45 seconds. **This is done and verified.**
2. **Section Building** (Step 2) — an agent reads cache files + section guides and builds HTML fragments for each report section. **This is where your work is.**
3. **Assembly** (Step 3) — agent stitches fragments into a single HTML report.
4. **Post-Build Check** (Step 4) — static checker validates the output.

---

## What Changed in the Prior Session

A significant amount of work was done to the documentation and pipeline. Here's what's new:

### 1. Python Data Gathering Script (NEW)
- `scripts/data_gather.py` — replaces MCP-based data gathering entirely
- Connects to Postgres via MCP SSE server, BigQuery via service account key
- Runs all queries in parallel batches, computes all gate flags and derived gates
- Writes all cache files in the locked markdown format
- **Verified against 4 live clients**: PF (Palecek), UFI, CCI, HFG, RW — all pass

### 2. ERP Enrichment Queries (NEW — Q-51 through Q-54)
Added to `authority/query_library.md` and `operators/external/guides/stage1_preflight_and_queries.md`:

| Query | What It Does | Gate |
|-------|-------------|------|
| Q-51 | Rep-Level eCat Capture vs. Total Business | `HAS_PORTAL_ORDERS` + `PORTAL_REP_DATA_PRESENT` |
| Q-52 | Customer-Level eCat Penetration | `HAS_PORTAL_ORDERS` + `PORTAL_CUSTOMER_DATA_PRESENT` |
| Q-53 | Unactivated High-Value ERP Accounts | `HAS_PORTAL_ORDERS` + `PORTAL_CUSTOMER_DATA_PRESENT` |
| Q-54 | Geographic eCat Penetration | `HAS_PORTAL_ORDERS` + `PORTAL_CUSTOMER_DATA_PRESENT` |

These queries produce cache files (`Q-51_results.md` through `Q-54_results.md`) that the section guides reference. **The data is being gathered correctly. The section builder is NOT consistently rendering these new subsections.**

### 3. Data Confidence Framework (NEW)
- Each report section gets a confidence tier: `FULL`, `STRONG`, `PARTIAL`, or `LIMITED`
- Tiers are computed by the data gathering script and stored in `cache/section_confidence.md`
- Section guides have rendering rules for confidence footers using `.data-confidence` CSS classes
- Templates are locked in `operators/external/guides/shared_rules.md` Section J
- **These ARE rendering in the HTML** — footers like "PARTIAL VIEW", "STRONG VIEW", "FULL VIEW" appear correctly

### 4. Admin-in-Leaderboard Disclosure (NEW)
- Gate flag `ADMIN_REPS_IN_LEADERBOARD` detects internal/admin users in sales leaderboards
- Disclosure text is defined in `shared_rules.md` as `§2-ADMIN-DISCLOSURE`
- Should render as an additive append inside the §2 confidence footer
- **Inconsistently rendering** — HFG shows it, CCI and RW don't despite the flag being true

### 5. Run Prompt Simplified
- Step 1 now only has the script path (MCP-based manual gathering was removed)
- Parallel section building guidance added to Step 2
- Runtime estimate updated to 5-10 minutes total

---

## Known Issues to Fix

These were identified by comparing 4 old archived reports against fresh runs.

### CRITICAL — Section Builder Not Rendering New Subsections

The section guides were updated with instructions for new ERP-enriched subsections, but the agent building sections doesn't consistently follow them. Results from validation:

| New Subsection | Section Guide | HFG | CCI | UFI | RW |
|---|---|---|---|---|---|
| Rep eCat Adoption vs. Total Business (Q-51) | `section_02_sales_team.md` | Rendered | **Missing** | N/A (no rep data) | N/A (no ERP) |
| eCat Penetration of Total Business (Q-52) | `section_03_customers.md` | Rendered | **Missing** | **Missing** | N/A |
| Unactivated High-Value Accounts (Q-53) | `section_03_customers.md` | Rendered | **Missing** | **Missing** | N/A |
| Geographic eCat Penetration (Q-54) | `section_03_customers.md` | Rendered | **Missing** | **Missing** | N/A |
| Total Business enrichment on Top Buyers (Q-52) | `section_05_commerce.md` | Rendered | Partial | N/A | N/A |

**Root cause**: The section guides have the instructions, but they may not be explicit enough. The agent sometimes skips subsections when the cache file exists but isn't listed forcefully enough in the guide's "Query Inputs" block. Consider making the guides more directive: "If `Q-52_results.md` exists in cache, you MUST render subsection N."

### MEDIUM — Lynn Ross Duplication (HFG)
One rep appears twice in the sales leaderboard table. This is a rendering/dedup issue in §2 section building, not a data issue. The cache data only has one entry.

### LOW — Peer Benchmark Methodology Shift
Old reports used all-time metrics for peer ranking. New reports use LTM (last twelve months). This changes the client's ranking (e.g., HFG went from "Top 5%" to "Top 35%"). This is correct per the current query library — just be aware clients who saw old reports may notice.

### LOW — CCI New Introduction Count Jump
CCI's "New Introduction" metric jumped from 354 to 1,390. Likely a methodology change in how new items are counted, not fabrication. Worth investigating if CCI is a priority client.

---

## File Map (What to Read and Edit)

### Authority files (read, don't edit unless fixing a bug)
- `authority/query_library.md` — all SQL queries with semantic rules
- `authority/value_moment_catalog.md` — semantic authority for all claims
- `authority/html_report_template.html` — CSS `<style>` and JS `<script>` blocks (VERBATIM in every report)
- `authority/peer_benchmark.md` — peer comparison framing rules

### Section guides (THIS IS WHERE YOUR EDITS GO)
- `operators/external/guides/section_02_sales_team.md` — §2 Sales Team
- `operators/external/guides/section_03_customers.md` — §3 Customer Intelligence
- `operators/external/guides/section_04_product.md` — §4 Product & Inventory
- `operators/external/guides/section_05_commerce.md` — §5 Commerce Analytics
- `operators/external/guides/section_06_portal.md` — §6 Portal Engagement
- `operators/external/guides/section_07_peer.md` — §7 Peer Benchmarking
- `operators/external/guides/section_08_platform.md` — §8 Platform Utilization

### Shared rules and assembly
- `operators/external/guides/shared_rules.md` — forbidden phrases, CSS classes, confidence framework, locked templates
- `operators/external/guides/stage4_assembly.md` — assembly rules for final HTML

### Run prompt (the operator)
- `operators/external/run_prompt.md` — what the executing agent follows

### Data gathering (done, don't touch)
- `scripts/data_gather.py` — Python data gathering script
- `operators/external/guides/stage1_preflight_and_queries.md` — gate logic reference

---

## Test Runs Available

These runs have both cache data and finished HTML output for comparison:

| Client | Shortname | Org ID | Run Dir | Old Report |
|--------|-----------|--------|---------|------------|
| Universal Furniture | ufi | (in gate_flags) | `runs/ufi_2026-06-15/` | `hosted/ufi.html` |
| Century Furniture | cci | (in gate_flags) | `runs/cci_2026-06-15/` | `hosted/cci.html` |
| Hooker Furnishings | hfg | (in gate_flags) | `runs/hfg_2026-06-15/` | `hosted/hfg.html` |
| Rowe Furniture | rw | (in gate_flags) | `runs/rw_2026-06-15/` | `hosted/rw.html` |
| Palecek | pf | 32 | `runs/pf_2026-06-15/` | N/A |

Each `runs/{shortname}_2026-06-15/` has:
- `cache/` — all Q-XX_results.md, gate_flags.md, section_manifest.md, section_confidence.md
- `output/` — the generated HTML report
- `fragments/` — individual section HTML fragments (if present)

---

## How to Iterate

1. **Pick a section guide** to tune (e.g., `section_03_customers.md`)
2. **Read its current cache files** from one of the test runs (e.g., `runs/hfg_2026-06-15/cache/Q-52_results.md`)
3. **Edit the section guide** to make instructions more explicit
4. **Re-run just Step 2 for that section** against the existing cache (no need to re-run the data gathering script)
5. **Compare the new fragment** against the old one and the archived report
6. **Repeat** for other sections

The cache files are stable and correct — they don't change unless you re-run the script. So you can iterate on section building as many times as needed without touching Step 1.

---

## Priority Order

1. Fix the section guides so Q-51/52/53/54 subsections render when data exists
2. Fix the admin-in-leaderboard disclosure rendering in §2
3. Fix the Lynn Ross duplication issue in §2 (dedup logic)
4. General HTML output tuning per operator feedback
5. Review confidence footer language and placement

---

## Key Rules

See [`GUARDRAILS.md`](GUARDRAILS.md) for the canonical rule set.
