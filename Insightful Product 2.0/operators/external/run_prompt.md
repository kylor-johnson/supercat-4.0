# Insightful Product 2.0 — External Report Run Prompt

Produces a client intelligence report end-to-end: data gathering → section
building → HTML assembly → post-build check. If anything fails, stop and report.
Do not improvise around missing data.

**Prerequisites:** Cursor with `user-supercat-postgres-vpn` and `user-bigquery-admin`
MCPs enabled. VPN active.

---

You are producing an external Customer Intelligence Report. Read the entire prompt before starting.

## Client Parameters

The only required input is the **shortname**. Resolve everything else automatically:

1. Query Postgres via `user-supercat-postgres-vpn`:
   `SELECT id, shortname, name FROM organizations WHERE shortname = '<shortname>' LIMIT 1;`
   If no row is returned, stop and report the error.
2. Set `ORG_ID` and `CLIENT_NAME` from the query result.
3. Set `RUN_DATE` to today (`YYYY-MM-DD`).
4. Set `REPORT_DATE_DISPLAY` to today in long form (e.g. "June 16, 2026").
5. Set `PERIOD_END` to the month before the run date (e.g. "May 2026").
6. Set `PERIOD_START` to 12 months before PERIOD_END (e.g. "May 2025").
7. `BUNDLE_LABEL` is filled from `gate_flags.md` Org Identity after Step 1.

**Run directory:** `Insightful Product 2.0/runs/{SHORTNAME}_{RUN_DATE}/`
Create `cache/`, `fragments/`, and `output/` subdirectories as needed.

---

## Step 1 — Data Gathering

Run the data gathering script:

```bash
cd "Insightful Product 2.0"
source scripts/.venv/bin/activate
python scripts/data_gather.py \
  --shortname {SHORTNAME} \
  --org-id {ORG_ID} \
  --run-date {RUN_DATE}
```

Add `--dry-run` to preview the query plan without executing. Add
`--client-name "Name"` to override the display name from the database.

The script writes all cache files to `runs/{SHORTNAME}_{RUN_DATE}/cache/`
including `gate_flags.md`, `section_manifest.md`, and `section_confidence.md`.

**After the script completes:** If it reports Mode 2 or Mode 3, follow the
mode-specific assembly in `stage1_preflight_and_queries.md` — stop here.
If Mode 1, proceed to Step 2.

**Showroom scan:** The script runs Pass 1 (keyword) and Pass 2 (brand-name)
automatically. Read `cache/showroom_scan_results.md` and review any flagged
names before proceeding.

**Rules:** Q-02 and Q-03 are NOT SQL queries — they are Step 2 derivations.
Do not attempt to run them (see `stage1_preflight_and_queries.md` §2.2a).

### Checkpoint

Report to chat: report mode, key gate flags, query execution summary (ran /
skipped / failed), section manifest (INCLUDE vs SKIP). Then proceed to Step 1b.

---

## Step 1b — Build Context Bundles

After data gathering completes (Mode 1 only), build context bundles that
pre-load everything each section builder needs into a single file:

```bash
python scripts/build_context.py --shortname {SHORTNAME} --run-date {RUN_DATE}
```

This produces one `cache/section_NN_context.md` per INCLUDE section, containing:
- The full section guide (verbatim)
- `shared_rules.md` (verbatim)
- Gate flags and section confidence
- All cache data files the section needs (verbatim, or explicitly marked as not present)
- Authority excerpts where required (Q-02/Q-03 derivation rules for §2, peer_benchmark.md for §7)

The script completes in under 1 second. Proceed to Step 2.

---

## Step 2 — Build Section Fragments

### Context bundles

Each INCLUDE section has a pre-built context bundle at
`cache/section_NN_context.md`. This single file contains the section guide,
shared rules, gate flags, and all cache data — everything needed to build the
fragment. **Read it instead of the individual files.**

Sections are independent and can be built in parallel.

### Per-section workflow

For each INCLUDE section:

1. **Read `cache/section_NN_context.md`** — it contains the section guide,
   shared rules, gate flags, section confidence, and all cache data. Do not
   read the individual cache files or guides separately.

2. **Build the fragment** per the section guide within the context bundle. Use
   the fragment contract from the Shared Rules section (Section E). Locked
   section IDs: `sales`, `customers`, `product`, `commerce`, `portal`, `peer`,
   `platform`. For every conditional cache file: check the gate flag. If the
   gate is `true` AND the cache data has rows, you MUST render the subsection.
   If the gate is `false` OR the data says "(not present)", skip silently.

3. **Verify** against the Conditional Subsection Checklist at the end of the
   section guide. Fix any failures before saving.

4. **Build highlights** — `cache/section_NN_highlights.md` with 2–4 candidates
   per the Shared Rules Section G. `[HYPOTHETICAL]` tags belong in highlight
   files only — never in the HTML fragment.

5. **Save** fragment to `fragments/section_NN.html`, highlights to cache.

---

## Step 3 — Assemble Final Report

Read:
- `operators/external/guides/stage4_assembly.md` — full assembly rules
- `authority/html_report_template.html` — `<style>` and `<script>` blocks (copy VERBATIM)
- All `cache/section_NN_highlights.md` files
- All `fragments/section_NN.html` files
- `cache/gate_flags.md` — for template parameters and Appendix data

### Build order (per stage4_assembly.md)

1. HTML boilerplate + `<style>` block VERBATIM from template
2. Header (`.h-brand`, `.h-customer`, `.h-type`, `.h-meta`, `.h-accent`)
3. TOC — links to INCLUDE sections + Executive Summary + Appendix
4. **Executive Summary (§1)** — built LAST from highlights. See `stage4_assembly.md` §2.
5. Section fragments (§2–§8) — paste each VERBATIM in order
6. Appendix (§9) — per `stage4_assembly.md` §3
7. Footer + `<script>` block VERBATIM from template

Replace all `{{PARAM}}` from gate_flags.md Org Identity. Verify zero `{{` remain.

### Save

`output/{SHORTNAME}_{RUN_DATE}_intelligence_report.html`

---

## Step 4 — Post-Build Check

Count the INCLUDE sections from `section_manifest.md` and run:

```bash
cd "Insightful Product 2.0"
bash qa/eval/check_static.sh \
  "runs/{SHORTNAME}_{RUN_DATE}/output/{SHORTNAME}_{RUN_DATE}_intelligence_report.html" \
  {INCLUDE_COUNT}
```

`PASS` = clean. `WARN` on review tokens (hedging, Appendix "ERP") is fine.
`FAIL` = defect — fix before delivery.

---

## Final Report to Chat

1. Report mode and gate flag summary
2. Per-section build status (built / skipped)
3. Highlight selection and priority action count
4. Static check result (PASS/WARN/FAIL)
5. Output file path
6. Confirmation: report is ready for browser review
