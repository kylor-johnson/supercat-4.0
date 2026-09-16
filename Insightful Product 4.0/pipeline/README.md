# Insightful Pipeline

A deterministic Python factory that produces ship-ready CEO Intelligence Report
drafts on demand for any SuperCat org. Same shortname + same cache date + same
pipeline commit = byte-identical output.

The factory implements the operator spec in
[`../operators/report_operator.md`](../operators/report_operator.md) as
deterministic Python — no per-report agent context, no re-interpreting the
spec each run. If a behavior needs to change, the pipeline changes; the
spec stays authoritative for what the report SHOULD say.

For the end-to-end run instructions, see
[`../operators/external/run_prompt.md`](../operators/external/run_prompt.md).

---

## What this is (and isn't)

**It is:**
- A CLI that reads cached query results + a ratified profile and emits a
  Markdown draft into `outputs/{org}_DRAFT_{date}.md`.
- A cohort orchestrator (`run_cohort.sh`) that fans across N orgs and
  emits a 4-bucket sales-workflow segmentation.
- The Health V3 pattern applied to the Insightful spec:
  `cache → preflight → gather → signals → assemble`.

**It is not:**
- A free-text generator. Six bounded prose slots (hero, talking points,
  coaching, plays, growth connective, outreach) may be filled by an LLM or
  by a Cursor agent writing `outputs/{org}_prose_{date}.json`. Every slot
  has a fact bundle, a number-parity / voice gate, and a **deterministic
  template fallback**. The LLM expresses; it never selects or computes.
  Without a prose file or API key the report still ships.
- A profile-ratification workflow. Profiles get ratified one-at-a-time
  when a prospect graduates to a real demo — the pipeline can *emit*
  inline drafts under `--cohort-validation`, but human ratification is
  still required before the artifact is client-facing.
- An edit to canon. `foundation/`, `operators/`, `report_product/`,
  `knowledge/`, and ratified `profiles/*.md` are read-only inputs.

---

## Architecture (Health V3 pattern)

```
        ┌─ cache/{org}/{date}/*.csv  (immutable per date)
        │
foundation/query_library_v2.md  ──►  cache.py  (extract SQL, execute, write CSVs)
                                        │
                                        ▼
                                  preflight.py  (RunPosture)
                                        │
                                        ▼
                                    gather.py  (typed dataclasses)
                                        │
                                        ▼
                                    signals.py  (SIGNAL_RANK, top-N)
                                        │
                          ┌─────────────┴─────────────┐
                          ▼                           ▼
                    narrative.py               assemble.py  (Jinja2 → MD)
                    (six prose slots)                 │
                          └─────────────┬─────────────┘
                                        ▼
                        outputs/{org}_DRAFT_{date}.md
                                        │
                                        ▼
                        report_render/  →  outputs/{Org}_CEO_intelligence_report_{date}.html
```

**Surface ownership (the bug is cross-talk):**

| Module          | Reads              | Writes                        | Never |
|-----------------|--------------------|-------------------------------|-------|
| `cache`         | canon SQL, Postgres| `cache/{org}/{date}/*.csv`    | reads results |
| `preflight`     | cache CSVs         | `RunPosture` dataclass        | runs SQL |
| `gather`        | cache CSVs         | typed data bundles            | runs SQL |
| `signals`       | gather + posture   | fired `Signal` list           | writes prose |
| `assemble`      | posture + gather + signals | rendered Markdown     | runs SQL, detects signals |
| `narrative`     | posture + gather + signals | six slot strings (or fallback) | reads cache directly |
| `smoke_check`   | draft MD           | pass/fail                     | is a gate library |

---

## Directory layout

```
pipeline/
  README.md                 you are here
  _archive/SURGICAL_EDIT_GUIDE.md   (archived — surgical edit step eliminated)
  __init__.py               module surface docstring
  config.py                 paths, PG connection, query-id manifest
  cache.py                  SQL extraction + CSV population
  preflight.py              Q-ECON-00 / Q-CHAN-00 / RP-2 → RunPosture
  gather.py                 all other queries → typed dataclasses
  signals.py                detection rules + SIGNAL_RANK
  assemble.py               Jinja2 orchestration
  narrative.py              §1 hero framing (only LLM call)
  smoke_check.py            minimal structural validator
  run_report.py             single-org CLI
  populate_cache.py         cache-only CLI (one-off per org per date)
  run_cohort.py             cohort orchestrator + summarizer
  run_cohort.sh             bash wrapper (per-org fan-out)
  templates/                Jinja2 .md.j2 templates (one per section + gatestop)
  cache/                    runtime; each {org}/{date}/ is immutable
  cohort_runs/              runtime; per run_id status.csv + run.log
```

---

## Prerequisites

**Environment:**
- `.venv-renderer` (Python 3.14) at repo root — same venv the renderer uses.
- Install `requirements-pipeline.txt` (adds `jinja2`, `psycopg2-binary`,
  `pandas`, `anthropic`).

**Postgres (for cache population):**
- VPN active (SuperCat prod is not public).
- `DATABASE_URL` or `PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD` env vars.
- The MCP server `user-supercat-postgres-vpn` uses the same backing DB;
  when local creds aren't set up, the agent can populate cache through
  MCP + `cache.import_from_dicts(query_id, org, date, rows)`.

**LLM (for the six prose slots):**
- `ANTHROPIC_API_KEY` in env. Optional: `INSIGHTFUL_NARRATIVE_MODEL`.
  Without a key, the pipeline looks for `outputs/{org}_prose_{date}.json`
  (agent-authored). If that file is missing, every slot falls back to
  deterministic template prose. Pipeline never crashes on this. The
  archived surgical-edit step (`pipeline/_archive/SURGICAL_EDIT_GUIDE.md`)
  is not part of the run.

---

## How to run

### Single org (the common case)

```bash
# populate cache (once per org per date; immutable after that)
.venv-renderer/bin/python -m pipeline.populate_cache --org sarreid --date 2026-06-30

# run the report
.venv-renderer/bin/python -m pipeline.run_report --org sarreid --date 2026-06-30

# smoke-check the draft
.venv-renderer/bin/python -m pipeline.smoke_check outputs/sarreid_DRAFT_2026-06-30.md

# render to HTML (prose already in the draft via slots or template fallback)
.venv-renderer/bin/python -m report_render.html_renderer outputs/sarreid_DRAFT_2026-06-30.md
```

### Fresh prospect (no ratified profile)

```bash
# --cohort-validation skips the ratified-profile gate, emits an inline
# profile draft to profiles/{org}.draft.md, and marks the output as a
# VALIDATION ARTIFACT (not client-facing until the profile is walked).
.venv-renderer/bin/python -m pipeline.run_report --org bmc --date 2026-06-30 --cohort-validation
```

### Cohort run (5-org example)

```bash
# runs pipeline per org, appends per-org row to a shared status.csv,
# prints the 4-bucket sales-workflow segmentation at the end
pipeline/run_cohort.sh --orgs sarreid,cci,hfg,kal,sca --date 2026-06-30 --run-id 2026-06-30

# outputs:
#   outputs/{org}_DRAFT_{date}.md   or   outputs/{org}_GATESTOP_{date}.md
#   pipeline/cohort_runs/{run-id}/status.csv
#   pipeline/cohort_runs/{run-id}/run.log
```

### Re-summarize a past run

```bash
.venv-renderer/bin/python -m pipeline.run_cohort --summarize --run-id 2026-06-30
```

---

## The four sales-workflow buckets

The cohort summarizer produces a segmentation table with these buckets
(from the plan and `operators/report_operator.md` §5b):

| Bucket                                 | Meaning                              | Pipeline output          |
|---------------------------------------|--------------------------------------|--------------------------|
| Mode-1 STRONG (premium pitch)         | full CEO Intelligence Report         | `{org}_DRAFT_{date}.md`  |
| Mode-1 degraded (mid pitch with gap)  | Standard mode but Tier-1 named       | `{org}_DRAFT_{date}.md`  |
| Mode-2 (Rep Copilot pitch)            | NONE-feed → Rep Copilot redirect     | `{org}_GATESTOP_{date}.md` |
| Gate-STOP                             | no commerce signal at all            | `{org}_GATESTOP_{date}.md` |

---

## Immutability contract (Health V3, verbatim)

> Once `cache/{org}/{date}/` exists, it is never modified. To re-run
> with fresher data, populate a NEW dated directory.

This makes re-runs free during iteration (signal-rule edits, template
tweaks) and guarantees a report is reproducible from its cache dir.

---

## How this relates to `report_render/`

`report_render/` is untouched by this build. The pipeline stops at
Markdown; `report_render.html_renderer` picks up the surgically-polished
`.md` and produces the final client-facing HTML.

```
pipeline           →   outputs/{org}_DRAFT_{date}.md
      ↓ (surgical polish)
      →   outputs/{org}_FINAL_{date}.md
report_render      →   outputs/{Org_Display}_CEO_intelligence_report_{date}.html
```

`report_render/step10_check.py` still runs the HTML-side gate checks
(§P forbidden vocab, §Q sensitivity hedges, §R concentration, §S
addressable base) — those live at the render boundary, not here.

---

## Growth Loop maintenance

After every 3–5 real cohort runs, review:
1. What surgical edits fired repeatedly? → codify into templates or signals.
2. What broke that smoke_check missed? → add the check (only if it
   would have fired on ≥2 real drafts — no speculative gates).
3. What signals stayed silent when a human would have flagged them? →
   new detection rule in `signals.py`.

This is ongoing maintenance, not a separate phase. The factory exists;
every report is a Growth Loop iteration that compounds.
