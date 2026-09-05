---
name: insightful-report
description: Run an Insightful Product 2.0 Customer Intelligence Report end-to-end from a client shortname (runs data_gather.py, builds section fragments, assembles HTML, runs the static checker). This is the LEGACY 2.0 report. Use ONLY when the user explicitly asks for "2.0", the "Customer Intelligence Report", or "the old/legacy report" — do NOT trigger on a bare "run a report for X" (that defaults to insightful-report-4).
---

# Insightful Product 2.0 — Report Runner

Run a complete Customer Intelligence Report from **just a client shortname**.

## What the user gives you

The user will say something like:
- "Run the report for UFI"
- "Generate the intelligence report for Palecek"
- "Run insightful for cci"

Extract the **shortname** from their message. That is the only required input.

Optional overrides the user may provide (use defaults below if not):
- `client_name` — display name override (default: looked up from Postgres)
- `run_date` — report date override (default: today)
- `dry_run` — if the user says "dry run" or "preview", pass `--dry-run`

## Step 0 — Resolve parameters

All 8 parameters in the run prompt are derivable from the shortname + today's date.

### 0a. Look up org_id and client_name

Query Postgres via the `supercat-postgres-vpn` MCP:

```sql
SELECT id, shortname, name FROM organizations WHERE shortname = '<shortname>' LIMIT 1;
```

If no row is returned, stop and tell the user the shortname wasn't found.
Set:
- `ORG_ID` = the `id` value
- `CLIENT_NAME` = the `name` value (unless the user gave an override)
- `SHORTNAME` = the shortname (as provided)

### 0b. Compute dates

- `YYYY-MM-DD` = today's date (e.g. `2026-06-16`)
- `REPORT_DATE_DISPLAY` = today in long form (e.g. `June 16, 2026`)
- `PERIOD_END` = the month before the run date (e.g. `May 2026`)
- `PERIOD_START` = 12 months before PERIOD_END (e.g. `May 2025`)
- `BUNDLE_LABEL` = leave blank — will be filled from `gate_flags.md` after Step 1

### 0c. Confirm to the user

Before running, print a short confirmation:

```
Running Insightful Report:
  Client:    Universal Forest Industries (ufi)
  Org ID:    241
  Run date:  2026-06-16
  Period:    May 2025 – May 2026
```

Then proceed immediately — do not wait for approval unless the user explicitly
asked for a dry run.

## Step 1–4 — Execute the run prompt

Read `Insightful Product 2.0/operators/external/run_prompt.md` and execute
Steps 1 through 4 exactly as written, substituting the resolved parameters.

The run prompt is the single source of truth for the workflow. Follow it to the
letter — do not skip steps, do not reorder, do not improvise.

### Quick reference (do NOT substitute for reading the full run prompt):

1. **Step 1 — Data Gathering**: Run `data_gather.py` with the resolved params.
   Report the checkpoint summary to chat, then continue.
1b. **Step 1b — Build Context Bundles**: Run `build_context.py` with the same
   `--shortname` and `--run-date`. Produces one `cache/section_NN_context.md`
   per INCLUDE section, bundling the section guide, shared rules, gate flags,
   and all cache data into a single file.
2. **Step 2 — Build Section Fragments**: For each INCLUDE section, read its
   `cache/section_NN_context.md` (contains everything needed). Build the HTML
   fragment per the section guide within.
3. **Step 3 — Assemble Final Report**: Combine fragments into the final HTML
   using the template, highlights, and assembly rules.
4. **Step 4 — Post-Build Check**: Run `check_static.sh` on the output. Report
   PASS/WARN/FAIL.

### Context management

Context bundles eliminate most of the file-reading overhead. Each section agent
reads one file (`cache/section_NN_context.md`) instead of 10+. If you are
running low on context:

- Build sections sequentially, not in parallel.
- After finishing each section fragment, you can release the context bundle from
  active consideration — the fragments are independent.
- The critical file to keep in context for assembly (Step 3) is
  `html_report_template.html`.

## After completion

Report the final summary per the run prompt's "Final Report to Chat" section,
including:
- Output file path
- Static check result
- Confirmation the report is ready for browser review

## Scope boundaries

This skill produces the **external** Customer Intelligence Report only.

- For the **internal CS brief**, the user should run
  `operators/internal/generate_internal_brief.md` separately.
- For **per-customer briefs** (Customer Intelligence product), see
  `Customer Intelligence/operators/customer_brief_run_prompt.md`.
- This skill does NOT modify authority files, query library, section guides, or
  any system documentation.
