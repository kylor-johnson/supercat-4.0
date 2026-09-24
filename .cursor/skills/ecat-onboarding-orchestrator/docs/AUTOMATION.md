# Weekly Track B Assessment — Cursor Automation Guide

**Phase 5 of IMPLEMENTATION_PLAN.md.**
This document explains how to configure, run, and verify the weekly
onboarding Phase Progression assessment as a Cursor Automation.

---

## What this automation does

Runs the Track B framework (`onboarding-agents/1-ingestion/RUN_PROMPT.md`) end-to-end:

1. Detects the active onboarding cohort from `REGISTRY.yaml` and the live Postgres.
2. Queries Postgres and BigQuery for per-client phase metrics and flags.
3. Writes three sibling output files to `onboarding-agents/1-ingestion/output/`:
   - `{YYYY-MM-DD}-phase-assessment.md` — human-readable standup record
   - `{YYYY-MM-DD}-phase-assessment.json` — structured data
   - `{YYYY-MM-DD}-phase-assessment.html` — rendered HTML (via `render_phase_assessment.py`)
4. Optionally runs the cross-tenant fingerprint scan for any open root causes.

Output is the weekly "what phase is each client on and what is the one thing blocking them"
standup input.  The automation surfaces this every Monday before the week's first client
session.

---

## Prerequisites

These are the Phase 0 items from `IMPLEMENTATION_PLAN.md §6`.  **All must be true
before the automation will succeed.**

| Prerequisite | Status | How to verify |
|---|---|---|
| Repo contains the four framework files | Required | `git ls-files onboarding-agents/1-ingestion/*.md` — must return `Phase_Progression_Framework.md`, `Phase_Anchors.md`, `Flags_and_Signals.md`, `Output_Contract.md` |
| `RUN_PROMPT.md` is committed | Required | `git ls-files onboarding-agents/1-ingestion/RUN_PROMPT.md` |
| `REGISTRY.yaml` is committed | Required | `git ls-files eCat_Onboarding/REGISTRY.yaml` |
| `render_phase_assessment.py` is committed | Required | `git ls-files onboarding-agents/1-ingestion/render_phase_assessment.py` |
| VPN active during the run | Required | The automation queries `supercat-postgres-vpn` (Postgres) and `bigquery-admin` (Fathom/HelpScout).  Both require VPN. |
| `overrides.yml` committed (if any overrides exist) | Conditional | `git ls-files onboarding-agents/1-ingestion/overrides.yml` |

> **Rule from `IMPLEMENTATION_PLAN.md §6.1`:**
> Cursor Automations can only reference committed files in the automation's own repo.
> Untracked files are invisible to the automation agent.  Run `git status` before
> setting up the automation and commit any outstanding files.

---

## Setting up the automation in Cursor

Open **Cursor → Automations** (the Automations panel or the menu bar item), then
click **+ New Automation**.  Fill in the fields below.

### Trigger

| Field | Value |
|---|---|
| Type | **Schedule** |
| Frequency | Weekly |
| Day | Monday |
| Time | 08:00 AM (your local time, before the first client session) |

### Name and description

| Field | Value |
|---|---|
| Name | `Weekly Onboarding Phase Assessment` |
| Description | `Run the Track B phase progression framework for all active onboarding clients and write the dated assessment files.` |

### Tools

Enable the following tools for the automation agent:

| Tool | Purpose |
|---|---|
| `supercat-postgres-vpn` | Per-client product / customer / import-event counts |
| `bigquery-admin` | Fathom meeting notes + HelpScout tickets |
| File system (read + write) | Read framework files; write assessment output |
| Terminal | Run `render_phase_assessment.py` to produce the HTML |

### Instructions (the automation prompt)

```
You are running this week's onboarding Phase Progression assessment.

Read and follow the run instructions in:
  onboarding-agents/1-ingestion/RUN_PROMPT.md

That file is the complete execution guide.  Follow every step in order.
Do not skip the sanity check (Step 5) or the JSON + HTML render (Step 4b).

After the assessment is complete and the output files are written, run the
fingerprint scan for any check that had a new hit in last week's session:

  python ${CLAUDE_SKILL_DIR}/scripts/reconcile/fingerprint_scan.py \
    --check orphan_inventory
  python ${CLAUDE_SKILL_DIR}/scripts/reconcile/fingerprint_scan.py \
    --check missing_images

Append a brief scan summary to the bottom of the markdown output under an
"## Cross-tenant fingerprint scan" heading.

Do not commit, push, or send any email.  Write only to
  onboarding-agents/1-ingestion/output/{YYYY-MM-DD}-phase-assessment.{md,json,html}
```

> **Why `RUN_PROMPT.md` and not inline instructions?**
> The run prompt is a committed file that evolves with the framework.  Keeping the
> automation prompt thin means the framework can be updated without re-editing the
> automation.  The automation is the scheduler; `RUN_PROMPT.md` is the spec.

---

## What a successful run looks like

After the automation completes, verify:

1. Three files exist in `onboarding-agents/1-ingestion/output/` with today's date:
   ```
   onboarding-agents/1-ingestion/output/2026-07-28-phase-assessment.md
   onboarding-agents/1-ingestion/output/2026-07-28-phase-assessment.json
   onboarding-agents/1-ingestion/output/2026-07-28-phase-assessment.html
   ```

2. Every cohort member from `REGISTRY.yaml` (lifecycle: onboarding) appears in
   the markdown, or is explicitly noted as excluded with a reason.

3. No `❓ QUERY FAILED` lines remain in the markdown output.

4. The HTML renders without missing tokens: open it in a browser and confirm
   the per-client cards and agenda buckets are populated.

5. The `## Cross-tenant fingerprint scan` section shows at least one check ran
   (even if all results were CLEAN or SKIP).

Run this golden-file test to confirm the renderer is intact (output should be `MATCH`):
```bash
python onboarding-agents/1-ingestion/render_phase_assessment.py \
    onboarding-agents/1-ingestion/EXAMPLE-2026-06-09-phase-assessment.json \
    --check onboarding-agents/1-ingestion/EXAMPLE-2026-06-09-phase-assessment.html
```

---

## Adding a new fingerprint check to the post-assessment scan

1. Add a `check_<name>` function to
   `${CLAUDE_SKILL_DIR}/scripts/reconcile/fingerprint_scan.py`
   that takes `(executor, org_id)` and returns a `ScanResult`.

2. Register it in the `CHECKS` dict at the bottom of the built-in checks section.

3. If a registry flag should suppress it, add the mapping to `FLAG_SUPPRESSIONS`.

4. Add the new `--check <name>` line to the automation's instructions above.

5. Commit the updated script and the updated `AUTOMATION.md` together.

Available built-in checks (run `--list-checks` to see current set):
```bash
python ${CLAUDE_SKILL_DIR}/scripts/reconcile/fingerprint_scan.py \
    --list-checks
```

---

## Running the assessment manually (outside the automation schedule)

```bash
# From the SuperCat 4.0 workspace root

# 1. Make sure VPN is active.

# 2. Run the assessment (same prompt the automation uses — or open RUN_PROMPT.md
#    in a fresh Cursor agent session and follow its instructions).

# 3. Render the HTML from the JSON the agent wrote:
python onboarding-agents/1-ingestion/render_phase_assessment.py \
    onboarding-agents/1-ingestion/output/{YYYY-MM-DD}-phase-assessment.json
# → writes onboarding-agents/1-ingestion/output/{YYYY-MM-DD}-phase-assessment.html

# 4. Run the fingerprint scan:
python ${CLAUDE_SKILL_DIR}/scripts/reconcile/fingerprint_scan.py \
    --check orphan_inventory

python ${CLAUDE_SKILL_DIR}/scripts/reconcile/fingerprint_scan.py \
    --check missing_images

# 5. Verify the golden file is still intact:
python onboarding-agents/1-ingestion/render_phase_assessment.py \
    onboarding-agents/1-ingestion/EXAMPLE-2026-06-09-phase-assessment.json \
    --check onboarding-agents/1-ingestion/EXAMPLE-2026-06-09-phase-assessment.html
```

---

## Troubleshooting

### VPN / DB connection failure
```
DB connection failed: Set DATABASE_URL to your SuperCat Postgres connection string.
```
VPN is not active or `DATABASE_URL` is not set.  Connect to VPN and export the
connection string before running manually; the automation's scheduled run also
requires VPN to be active.

### `QUERY FAILED` in the assessment output
The most common cause is a schema mismatch between the query library and the live DB.
Check `scripts/reconcile/queries.py` — each query's docstring lists the table and
column names that were verified.  Known corrections are documented in `IMPLEMENTATION_PLAN
Appendix A`.

### Unresolved tokens in HTML (`{{ ... }}` visible in the rendered page)
The JSON the agent wrote is missing a required field.  The generator (`render_phase_assessment.py`)
names the missing token in its error output.  Fix the JSON, then re-run the renderer.
Do not edit the template or the generator.

### Registry has no entries for the chosen lifecycle
The scan falls back to querying Postgres directly for orgs at that lifecycle.
If the fallback also returns nothing, check VPN and the lifecycle value.  The lifecycle
is stored in `organizations.properties->>'status'` (not `organizations.state`, which
is geographic).  See `IMPLEMENTATION_PLAN Appendix A`.

### Automation ran but no output files were written
Check whether the framework files are all committed to the branch the automation checked
out.  Run:
```bash
git log --oneline -5
git ls-files onboarding-agents/1-ingestion/RUN_PROMPT.md
git ls-files eCat_Onboarding/REGISTRY.yaml
```
Any file missing from `git ls-files` was not committed and was invisible to the agent.

---

## Key files

| File | Purpose |
|---|---|
| `onboarding-agents/1-ingestion/RUN_PROMPT.md` | Execution guide — the canonical spec for each run |
| `onboarding-agents/1-ingestion/Phase_Anchors.md` | Phase 1–7 definitions, auto-cohort SQL, flag taxonomy |
| `onboarding-agents/1-ingestion/Flags_and_Signals.md` | Hard rules (no metric without a tool call) + ambiguity flags A–F |
| `onboarding-agents/1-ingestion/Output_Contract.md` | Phase assignment algorithm, per-client output structure |
| `onboarding-agents/1-ingestion/overrides.yml` | Human-confirmed facts (client domains, confirmed net-price orgs, integration status) |
| `eCat_Onboarding/REGISTRY.yaml` | Cohort enumeration — archetype, flags, cutover date per client |
| `onboarding-agents/1-ingestion/render_phase_assessment.py` | HTML renderer — reads JSON, writes `.html`; do not edit |
| `scripts/reconcile/fingerprint_scan.py` | Cross-tenant check runner — sweep all orgs for a root-cause signature |
| `onboarding-agents/1-ingestion/output/` | Assessment output directory (`{date}-phase-assessment.{md,json,html}`) |
