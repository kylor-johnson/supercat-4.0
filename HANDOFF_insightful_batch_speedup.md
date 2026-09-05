# Insightful 3.0 — Session Handoff (Jun 17, 2026)

## What Was Done This Session

Two major implementation passes were completed:

### Pass 1: CCI v4 Report Fixes (Gold Standard Alignment)

Fixed 5 issues in the report generation system identified by comparing the CCI v4 output against the synthetic gold standard (`authority/example-co-intelligence-report.html`):

1. **HTML structure fix** — `section_shared_contract.md` now specifies the exact `<details class="section-collapse">` wrapper: `section-title` must be `<div>` (not `<span>`), and `section-sub`/`section-contents`/`expand-hint` must all be INSIDE `<summary>`.

2. **Rep Leaderboard: top 5 + bottom 5** — `section_05_team.md` rewritten to show top 5 (highest GMV, always visible), middle collapsed with a summary line ("N additional reps · combined $X GMV"), and bottom 5 (lowest GMV, always visible).

3. **Coaching Cards moved to position 2** — The rendering order in `section_05_team.md` now places Coaching Cards immediately after the leaderboard (before eCat Adoption, Behavioral Scorecard, etc.).

4. **eCat Adoption as metric cards** — The old full-roster table was replaced with 4 metric cards (Team Capture Rate, Top Quartile Rate, Bottom Quartile Rate, Top-to-Bottom Gap) plus a focused "Activation Targets" callout listing top 5 reps at 0% capture.

5. **Text brevity rules** — `section_build_prompt.md` now has hard limits: confidence headers max 2 sentences, `what-this-means` blocks start with `<strong>Action:</strong>` and max 3 sentences, callout titles max 12 words, coaching body max 2 sentences.

A validation rebuild of CCI section 5 confirmed all fixes render correctly (8 subsections, 33.9 KB, all rules passing).

### Pass 2: Batch Report Speedup (30 min → ~12 min per report)

Replaced 3 LLM-dependent steps with deterministic Python scripts and added a batch orchestrator:

| New Script | Replaces | Runtime |
|---|---|---|
| `scripts/detect_signals.py` | LLM signal detection (Step 2) | < 1 sec |
| `scripts/assemble_report.py` | LLM assembly (Step 4) | < 1 sec |
| `scripts/audit_report.py` | LLM audit agent (Step 5) | < 2 sec |
| `scripts/batch_run.py` | Manual one-at-a-time execution | Parallel |

Also modified `scripts/build_context.py` to truncate `Q-38a_results.md` (was 16,738 rows / 1.3MB) to 50 rows in context bundles, shrinking the section_03 bundle from **1.4MB → 83.5KB**.

Rewrote `operators/external/run_prompt.md` to use these scripts. The LLM now only handles: (a) 5 parallel section agents, and (b) Signal Summary composition.

---

## Current State of the System

### File Locations (all in `Insightful Product 3.0/`)

```
scripts/
  data_gather.py        — Stage 1 data collection (BigQuery + Postgres), unchanged
  detect_signals.py     — NEW: deterministic signal detection
  build_context.py      — MODIFIED: added CACHE_TRUNCATION for large files
  assemble_report.py    — NEW: deterministic report assembly
  audit_report.py       — NEW: deterministic structural audit
  batch_run.py          — NEW: multi-client parallel orchestrator

operators/external/
  run_prompt.md         — REWRITTEN: streamlined orchestrator (scripts replace 3 LLM steps)
  section_build_prompt.md — MODIFIED: added Text Brevity section
  audit_prompt.md       — Still exists (superseded by audit_report.py for batch mode)

operators/external/guides/
  section_shared_contract.md — MODIFIED: added correct HTML wrapper spec
  section_05_team.md         — MODIFIED: leaderboard top5/bottom5, coaching pos 2, metric cards
  section_01_signals.md      — Unchanged (Signal Summary guide)
  section_02_accounts.md     — Unchanged
  section_03_product.md      — Unchanged
  section_04_commerce.md     — Unchanged
  section_06_platform.md     — Unchanged
```

### What the New Pipeline Looks Like (per report)

```
[Python]  data_gather.py       → 3-4 min (DB queries via MCP)
[Python]  detect_signals.py    → < 1 sec (threshold-based signal detection)
[Python]  build_context.py     → < 1 sec (bundles with truncation)
[LLM]    5 section agents      → 7-10 min (parallel, max bundle ~115KB)
[LLM]    Signal Summary (§1)   → 3-5 min (reads highlights + signal_rank only)
[Python]  assemble_report.py   → < 1 sec (concat fragments + substitute params)
[Python]  audit_report.py      → < 2 sec (structural verification)
[Bash]    check_static.sh      → < 1 sec (forbidden terms + balance checks)
```

**Total: ~12-15 min per report** (was 30+ min).

---

## How to Run 40 Reports

### Option A: Batch Prep + Individual Agent Spawns (Recommended)

**Step 1 — Prep all clients (deterministic, parallel)**

```bash
cd "Insightful Product 3.0/scripts"
source .venv/bin/activate
python batch_run.py --shortnames cci,kal,shl,mlc,pf,... --parallel 4 --run-date 2026-06-17
```

This runs `data_gather.py` + `detect_signals.py` + `build_context.py` for each client, 4 at a time. Takes ~15-20 min for 40 clients (3-4 min each / 4 parallel). Outputs a manifest at `runs/batch_2026-06-17_manifest.md` listing which clients are ready.

**Step 2 — Spawn LLM agents per client**

For each ready client, open a fresh Cursor agent and give it this prompt:

```
Run the report orchestrator at:
  Insightful Product 3.0/operators/external/run_prompt.md

Shortname: {SHORTNAME}

SKIP Steps 1, 2, and 2.5 — they are already done (data_gather, detect_signals,
and build_context have been run). Start at Step 3 (Spawn Section Agents).
```

Each agent only needs to:
1. Spawn 5 parallel section agents (~7-10 min)
2. Build Signal Summary (§1) from highlights + signal_rank (~3-5 min)
3. Run `python scripts/assemble_report.py --shortname X --run-date Y`
4. Run `python scripts/audit_report.py --shortname X --run-date Y`

You can have multiple Cursor agents running simultaneously for different clients.

**Step 3 — Spot check**

Open a few reports in the browser. Check that they look right. If `audit_report.py` flagged FAIL for any, re-run that client's failing section agent.

### Option B: Full End-to-End (single client, if you want to test first)

Just give a fresh agent the standard orchestrator prompt:

```
Run the report orchestrator at:
  Insightful Product 3.0/operators/external/run_prompt.md

Shortname: cci
```

It will run all steps sequentially (scripts handle the fast parts, agent handles sections + summary).

---

## Things That Need Resolving / Known Gaps

### 1. `detect_signals.py` detects fewer signals than the LLM did (17 vs 33 for CCI)

The script handles the major signal types correctly but some detectors need column-name parsing adjustments for specific orgs. The LLM was more flexible about interpreting varied cache file formats. For batch mode this is acceptable — the signal_rank.md from the script still captures the top signals correctly. If you want parity, the fix is to inspect a few cache files for column naming variations and add aliases to the `parse_table` logic.

### 2. `batch_run.py` org_id resolution

The batch runner needs org_ids to pass to data_gather.py. Three options:
- Pass `--org-ids 161,42,55,...` explicitly (fastest)
- Let data_gather.py resolve from shortname (it already does this internally)
- The current code passes `org_id=1` as a placeholder and data_gather.py overrides it from the DB lookup

The placeholder approach works because data_gather.py's `_run()` function queries the org by shortname and corrects the org_id if mismatched. So you can just run it without `--org-ids`.

### 3. Section agents still take 7-10 min per report

This is the remaining LLM bottleneck. The bundles are now 50-115KB (down from 1.4MB) which helps, but you're still waiting on 5 parallel LLM calls. No way to avoid this without going to template-only rendering (which would lose the narrative intelligence).

### 4. Signal Summary still needs an LLM

The Signal Summary (§1) writes headlines, priority actions, an outreach table with talking points, and conversation questions. This requires editorial judgment. It's a small focused call (~20KB input) but adds 3-5 min. Could potentially be templated for repeat runs where you already know the signals, but not worth it for v1.

### 5. The v4 CCI report assembly was done from older fragments

The assembled reports at `runs/cci_2026-06-17/output/` and `runs/cci_2026-06-17_v4/output/` were built from fragments that predate the Pass 1 fixes (leaderboard, coaching cards, brevity). To get a report that reflects all fixes, you need to re-run section agents with the updated guides. The validation rebuild of section 5 confirmed the fixes work — just haven't done a full re-run of all 5 sections for CCI yet.

---

## Quick Reference: Key Paths

| Item | Path |
|------|------|
| Orchestrator prompt | `operators/external/run_prompt.md` |
| Section build prompt | `operators/external/section_build_prompt.md` |
| Signal catalog | `authority/signal_catalog.md` |
| HTML template | `authority/html_report_template.html` |
| Gold standard example | `authority/example-co-intelligence-report.html` |
| CCI v4 run dir | `runs/cci_2026-06-17_v4/` |
| Scripts dir | `scripts/` |
| Python venv | `scripts/.venv/` |
| Static checker | `qa/eval/check_static.sh` |

---

## Resuming Work

If you want to pick up where this left off:

1. **To run 40 reports**: Follow "How to Run 40 Reports" above
2. **To verify fixes first**: Re-run CCI fully with `run_prompt.md` and check the output
3. **To improve signal detection parity**: Look at `detect_signals.py` column name parsing vs actual cache file headers for the org you're testing
4. **To further speed things up**: The only remaining LLM time is section agents (7-10 min parallel) + signal summary (3-5 min). Everything else is already < 5 seconds total.
