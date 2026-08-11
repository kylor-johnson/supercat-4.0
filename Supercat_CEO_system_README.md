# CEO System

The CEO System is an autonomous intelligence layer that generates 15 weekly
executive report types (16 runs/week — the AE brief runs once per rep) across
sales, support, product, growth, and market sensing. Reports deploy to
[ceosystem.io](https://ceosystem.io) via Vercel.

> **New here?** For *how the system composes context into a report* (the
> architecture, not the folder tour), read
> [`skills/ceo_system/ARCHITECTURE.md`](skills/ceo_system/ARCHITECTURE.md).
> Canonical counts live in its §7.

> **Downstream consumer — the Executive Scorecard.** A *separate* pipeline
> (`scripts/*_scorecard*.py`, its own runtime `~/repos/scorecard-runtime/`) reads
> these reports weekly/monthly and reasons them into the investor-facing scorecard
> at [supercatscorecard.ceosystem.io](https://supercatscorecard.ceosystem.io). It
> consumes each report's `## SLACK_SUMMARY` bullets + ```json``` blocks, so changing
> a report's JSON contract or SLACK_SUMMARY shape changes what the scorecard can say.
> If you touch the scorecard, read [`docs/SCORECARD_AGENT_BRIEFING.md`](docs/SCORECARD_AGENT_BRIEFING.md)
> and [`docs/RUNTIME_SYNC_GUARDRAILS.md`](docs/RUNTIME_SYNC_GUARDRAILS.md) first.

**Last updated**: 2026-07-17 | **Prompt count**: 16 active (15 scheduled, 1 on-demand) + 10 deprecated

## Architecture

```
skills/ceo_system/
├── prompts/              # 22 canonical prompts (the system's source of truth)
├── orchestrator/         # Autonomous execution engine (Python + Anthropic API)
│   ├── runner.py         # Agent loop: prompt → Claude API → tools → markdown
│   ├── scheduler.py      # DAG scheduler (Mon–Fri, dependency-aware)
│   ├── tools.py          # BigQuery, file I/O, pipeline tools for Claude
│   ├── config.yaml       # Schedule, model selection, retry policy
│   ├── notifier.py       # Slack notifications (per-prompt + daily summary)
│   └── launchd/          # macOS launchd plists for unattended execution
├── <artifact>/scripts/   # Per-report HTML renderers (14 renderers)
├── artifacts/            # Supporting data (customer registry, etc.)
├── plans/                # Design ADRs and decisions
├── ARCHITECTURE.md           # Architecture: context stack, runtime assembly, DAG, spine, counts
├── CEO_SYSTEM_GUARDRAILS.md  # Law: dependencies, surface ownership, delta rules
└── ARTIFACT_CATALOG.md       # Inventory: prompt ↔ output ↔ renderer ↔ brand
```

> **Foundation dependency:** 11 prompts read `foundation/CEO_SYSTEM_CONTEXT.md`
> at runtime for strategic grounding (ICP, pricing, competitors). That file
> must be synced into the runtime mirror — see `ARCHITECTURE.md` §6.

## Weekly Operating Rhythm

| Day | Reports | Model |
|-----|---------|-------|
| **Monday** | Market Scan, Operating Newspaper | Sonnet 4.6 |
| **Tuesday** | Growth Reality, Sales Pipeline Reality → AE Week Ahead, CEO Deal Assist | Sonnet 4.6 |
| **Wednesday** | Support Reality + Onboarding Reality → Support CEO Assist | Sonnet 4.6 |
| **Thursday** | Product & Engineering Reality, Finance Reality | Sonnet 4.6 |
| **Friday** | **Voice of Market** → Weekly CEO Digest | **Opus 4.6** |

Voice of Market (v8.0 "Hear the Market") and Weekly CEO Digest run on
Opus 4.6 via the Anthropic API. VoM is the system's most important prompt —
a two-pass transcript architecture that reads full, untruncated call
transcripts for the 5 highest-signal buyer/customer conversations each week.

## Pipeline per Prompt

```
1. Read prompt (skills/ceo_system/prompts/<name>.md)
2. Claude API agent loop (tool_use: BigQuery, file reads, pipelines)
3. Write markdown → reports/ceo_system/<name>_<date>.md
4. Render HTML → skills/ceo_system/<name>/scripts/render_html_wholesale.py
5. Validate HTML (>5KB, no PLACEHOLDER_ tokens, no excessive MISSING DATA)
6. Deploy → scripts/deploy_to_ceosystem.sh (git push → Vercel)
7. Slack notification (success + ceosystem.io link, or failure + error)
```

## Key Files

| File | Role |
|------|------|
| `CEO_SYSTEM_GUARDRAILS.md` | Artifact dependencies, surface ownership, delta discipline, quarterly review |
| `ARTIFACT_CATALOG.md` | Prompt ↔ output ↔ renderer ↔ brand inventory |
| `orchestrator/config.yaml` | Schedule, model selection (Opus 4.6 for VoM + Digest), retry policy |
| `scripts/deploy_to_ceosystem.sh` | Copy HTML → ceosystem repo → git push → Vercel auto-deploy |
| `artifacts/customer_org_shortnames.csv` | Customer registry for call classification |

## Running Reports

```bash
# Autonomous (scheduled via launchd at 6:00 AM weekdays)
# The orchestrator handles everything — no manual intervention needed.

# Manual: run a single prompt
python3 -m skills.ceo_system.orchestrator.runner \
  --prompt voice_of_market --date 2026-03-29

# Manual: run today's full schedule
python3 -m skills.ceo_system.orchestrator.scheduler

# Manual: run a specific day's schedule
python3 -m skills.ceo_system.orchestrator.scheduler --day friday

# Dry run (agent loop + markdown, skip render + deploy)
python3 -m skills.ceo_system.orchestrator.runner \
  --prompt market_scan --date 2026-03-31 --dry-run
```

## Data Sources

| Source | Access | Used by |
|--------|--------|---------|
| **BigQuery** (warehouse) | `google-cloud-bigquery` SDK | All prompts (HubSpot, Fathom, Help Scout, Stripe, QuickBooks, Mixpanel, LinkedIn Ads) |
| **Fathom** (call transcripts) | BigQuery tables (`Fathom.ai-summaries`, `Fathom.call-transcripts`) | Voice of Market (primary), Weekly CEO Digest (by citation) |
| **Local files** | `pathlib` reads | Prior reports, customer registry, guardrails |
| **Postgres** (instance health) | Optional — not in autonomous pipeline | Weekly CEO Digest, on-demand prompts (graceful degradation) |

## Customer Org Shortnames

Before classifying calls or querying customer health, resolve company names
via `skills/ceo_system/artifacts/customer_org_shortnames.csv`. See
`artifacts/ORG_SHORTNAMES_README.md` for the lookup process.

## Documentation Layers

| Layer | File | Purpose |
|-------|------|---------|
| **Map** | This file | Onboarding, folder tour, quick-start |
| **Inventory** | `ARTIFACT_CATALOG.md` | Prompt ↔ outputs ↔ renderer ↔ brand |
| **Law** | `CEO_SYSTEM_GUARDRAILS.md` | Dependencies, surface ownership, delta rules |
| **Architecture** | `ARCHITECTURE.md` | How context composes into a report: the context stack, runtime assembly, the dependency DAG, the dual-location spine, canonical counts (§7) |
| **Design ADR** | `plans/autonomous_execution_plan.md` | Original design ADR (March 2026) — decisions preserved, details superseded by this file |
| **Downstream** | [`docs/SCORECARD_AGENT_BRIEFING.md`](docs/SCORECARD_AGENT_BRIEFING.md) | Executive Scorecard pipeline (separate consumer of these reports): reasoning layer, cadence, guardrails, canonical-vs-runtime |

## Runtime Environment & Sync

The CEO System executes from a **runtime mirror** (`~/repos/ceo-system-runtime/`), NOT directly from this iCloud-backed workspace. This exists because macOS returns `EPERM` to background `launchd` processes attempting to read iCloud-evicted files.

**Architecture:**
```
~/Desktop/Cursor/supercat-local-ops/    ← You edit here (iCloud Drive)
        │
        │  sync_from_icloud.sh (daily at 5:55 AM)
        ▼
~/repos/ceo-system-runtime/             ← Scheduler executes here (local SSD)
├── orchestrator/     ← runner.py, scheduler.py, notifier.py, tools.py, config.yaml
├── lib/              ← Shared Python helpers (hubspot_client, ops_paths, etc.)
├── renderers/        ← Per-artifact template.html + render_html_wholesale.py (×14)
├── pipelines/        ← fetch_github_surface.py, sales_calls/, support/, voc/, deals/
├── scripts/          ← deploy_to_ceosystem.sh, sync_from_icloud.sh
└── data/
    ├── prompts/      ← All 15+ prompt .md files
    ├── reports/      ← Prior reports (for cross-week delta reads)
    ├── skills/       ← Feed registries, fetch scripts, agent_research frameworks
    └── editorial_memory/
```

**Sync mechanism:**
- `io.ceosystem.daily-sync` (launchd) runs `sync_from_icloud.sh` at **5:55 AM daily**
- Pre-warms iCloud files via `brctl download`, validates each copy with `cmp`
- Alerts to Slack if any file fails to sync
- Manual run: `bash ~/repos/ceo-system-runtime/scripts/sync_from_icloud.sh`

**Critical implication for agents:** editing a prompt, renderer, orchestrator file, or pipeline script in this workspace does **not** immediately affect the next scheduled run. The change propagates at next sync (5:55 AM) or via manual `bash ~/repos/ceo-system-runtime/scripts/sync_from_icloud.sh`. If you need immediate effect (e.g., triggering a fresh run after a hotfix), run the sync script manually first.

**Second runtime — the Executive Scorecard.** The scorecard is a *separate* pipeline with its **own** runtime mirror (`~/repos/scorecard-runtime/`), distinct from `ceo-system-runtime`. Unlike the CEO System it has **no automated daily-sync job** — after editing any `scripts/*_scorecard*.py` (or `run_scorecard.sh` / `scorecard_prototype.html`) you must **manually `cp`** the file into `~/repos/scorecard-runtime/` (canonical workspace remains source-of-truth; never edit the runtime copy). Its cron reads CEO reports from `ceo-system-runtime`, so it depends on the CEO System having synced first. Exact commands: [`docs/RUNTIME_SYNC_GUARDRAILS.md`](docs/RUNTIME_SYNC_GUARDRAILS.md).
