# Insightful Product 4.0

CEO intelligence reports for SuperCat's furniture/lighting wholesale clients.
Takes a client shortname, reads cached query data, and produces a ship-ready HTML
report.

**Architecture (v9 — Option C Hybrid Prose):** the pipeline is deterministic for
numbers, ranks, and section structure. Six bounded prose slots (hero, talking
points, coaching, plays, growth connective, outreach) may be filled by an LLM or
by a Cursor agent writing `outputs/{org}_prose_{date}.json`. Every slot has a
fact bundle, number-parity gate, voice lint, and **deterministic template
fallback** — so a run still ships with `--no-narrative` / no API key / no prose
file, at every commerce-confidence level (verified across the pinned cohort:
STRONG, PARTIAL and NONE all reach `smoke_check: PASS` deterministically).
The LLM **expresses**; it never selects or computes.

Governance / reading contract: [`CANON.md`](CANON.md). Runtime map:
[`foundation/WHAT_ACTUALLY_RUNS.md`](foundation/WHAT_ACTUALLY_RUNS.md). Re-anchor
plan: [`handoffs/REANCHOR_PLAN_2026-07-13.md`](handoffs/REANCHOR_PLAN_2026-07-13.md).

## Quick start

```bash
./run.sh sarreid                       # full run → SHIP
./run.sh sarreid --date 2026-07-02     # pinned cache date
./run.sh ali --preview                 # draft-profile run → PREVIEW
./run.sh da --date 2026-07-07          # Mode-2 org → ACTIVATION HTML
./run.sh bmc --date 2026-07-09 --no-narrative   # deterministic templates only
./run.sh --cohort sarreid,cci,hfg,kal  # batch run
./regression.sh                        # golden-set regression (6 orgs, checksum-verified)
```

## Prerequisites

- **Python venv:** `.venv-renderer/` (Python 3.14). Set up once:
  ```bash
  python3 -m venv .venv-renderer
  .venv-renderer/bin/pip install -r requirements-pipeline.txt
  ```
- **Data:** Cached query results in `pipeline/cache/{org}/{date}/` (16 CSVs per org). Populate via `--populate-cache` flag or MCP (`user-supercat-postgres-vpn`).

## Output naming

| Outcome | Filename pattern | Example |
|---------|------------------|---------|
| **SHIP** | `{DisplayName}_CEO_intelligence_report_{date}.html` | `Sarreid_Ltd._CEO_intelligence_report_2026-07-02.html` |
| **ACTIVATION** | `{DisplayName}_Activation_intelligence_report_{date}.html` | `Shadow_Catchers_Activation_intelligence_report_2026-07-02.html` |
| **PREVIEW** | `{org}_PREVIEW_{date}.html` | `ali_PREVIEW_2026-07-01.html` |
| **DRAFT** | `{org}_DRAFT_{date}.md` | `cci_DRAFT_2026-07-02.md` |
| **REDIRECT** | `{org}_GATESTOP_{date}.md` | (internal-only, zero-signal orgs) |

Display names come from the ratified profile H1 (`report_render/naming.py`). Do not hand-name SHIP HTML files.

## Golden-set regression

```bash
./regression.sh              # re-run the frozen golden set + verify checksums
./regression.sh --verify     # checksum only (no re-run)
```

Frozen baselines live in `config/golden_set.json` **v11 — 4 orgs**: `sarreid`, `cci`, `da`, `clc` (stamped 2026-07-20). Root copy that said “6 golden orgs” was stale: `hfg`, `kal`, `ali`, and `sca` were dropped from the freeze instead of finishing completeness review, and they are the anti-Sarreid set Track 4 will re-include after owner sign-off. Do not treat checksums as authority until that freeze. A passing freeze run prints `GOLDEN SET: PASS (4/4)`.

## Four outcomes

Every run ends with exactly one of these:

| Outcome | When | Output | Client-facing? |
|---------|------|--------|----------------|
| **SHIP** | Ratified profile + Mode-1 + smoke PASS + step10 PASS | `outputs/{Org}_CEO_intelligence_report_{date}.html` | Yes |
| **ACTIVATION** | Mode-2 + eCat signal present + no invoice feed | `outputs/{Org}_Activation_intelligence_report_{date}.html` | Yes |
| **PREVIEW** | Draft profile or `--preview` flag | `outputs/{org}_PREVIEW_{date}.html` | No |
| **REDIRECT** | Zero signal (no invoices AND no eCat) | No HTML created; internal Gate-STOP MD only | No |

Exit codes: `0` = SHIP/ACTIVATION/PREVIEW success, `1` = quality-gate failure, `2` = REDIRECT, `3` = hard failure.

ACTIVATION briefs use the same Sarreid CSS shell and voice. Sections requiring invoiced data are suppressed with canonical §O templates + explicit unlock language ("Connect an invoiced ERP feed…").

## Clients

### Ratified (SHIP via run.sh)

| Org | Profile | Notes |
|-----|---------|-------|
| sarreid | `profiles/sarreid.md` | Original validation org |
| cci | `profiles/cci.md` | Currey & Company |
| hfg | `profiles/hfg.md` | Hubbardton Forge |
| kal | `profiles/kal.md` | Kalco Lighting |
| sca | `profiles/sca.md` | **ACTIVATION** — eCat-only ($890K GMV), no invoice feed |

### Preview (draft profiles, not ship-ready)

| Org | Profile | Notes |
|-----|---------|-------|
| ali | `profiles/ali.draft.md` | Access Lighting; <2yr history |
| bri | `profiles/bri.draft.md` | Bulbrite; Tier-1 rep identity |
| da | `profiles/da.draft.md` | **ACTIVATION** — $4.87M eCat GMV, 0 invoices |

## Folder map

```
Canon     → foundation/ + knowledge/ + report_product/ + CANON.md
Clients   → profiles/
Factory   → pipeline/ + report_render/ + config/ + run.sh
Output    → outputs/
Ops       → handoffs/ + build_notes/ + _archive/  (historical; not required reading)
```

- **Canon** defines truth, voice, and report structure. Start at `CANON.md` for the governance index.
- **Clients** has one profile per org — the ratified facts the pipeline consumes.
- **Factory** is the Python pipeline + HTML renderer + quality gates.
- **Output** is where reports land. SHIP outputs are client-ready; everything else is internal.
- **Ops** is session history and build notes. Ignore unless debugging a past decision.

## Governance depth

See `CANON.md` for the full precedence chain, reading contract, and canon doc index. You do not need to read it to run a report — `run.sh` encodes the rules.

## New client

Any org in the SuperCat Postgres database can be run:
```bash
./run.sh newclient --populate-cache
```
This auto-generates a draft profile (`profiles/newclient.draft.md`) and produces a PREVIEW. Ratify the profile to unlock SHIP.
