# SuperCat 4.0 — operations workspace

> **Last updated**: 2026-09-16

Personal GitHub repo (`kylor-johnson/supercat-4.0`) for SuperCat operations:
Cursor/Claude skills, import rules, onboarding models, foundation docs, PM
material, and tracked analysis/report trees.

It is **not** the product codebase (`~/supercat-code`) and **not** the live
client-implementation tree. It is also **not** a dump of every folder in the
local SuperCat 4.0 directory — Health / Insightful museums, venvs, and nested
`agent-factory/` stay on disk and out of git.

Location map: [`WHERE.md`](WHERE.md).

## This Mac — how to open

**File → Open Workspace from File… →**
`~/repos/supercat-4.0/SuperCat.code-workspace`

That folder **is** this git working tree (remotes `origin` / `personal` →
`kylor-johnson/supercat-4.0`).

**iCloud `SuperCat 4.0` is an unread trap.** Do not open it, do not commit from
it. Leave it on disk; it is not the working tree.

Four trees (this Mac):

| Work | Path | What lives there |
|---|---|---|
| SuperCat Ops | `~/repos/supercat-4.0` | This repo (remotes `origin` / `personal`) |
| Live clients | iCloud `SuperCat_Simple_Final` | Live client CSVs + build work (`02_Implementation/`) = `kylor-johnson/ecat-onboarding-workspace` (also `~/repos/ecat-onboarding-workspace` symlink) |
| Product code | `~/supercat-code` | Rails / iOS application source |
| Company agents | `~/repos/agent-factory` | Weekly agents / factory PRs (`SuperCatSolutionsLLC/agent-factory`) |

The **other Mac** also clones under `~/repos` and opens
`SuperCat.macbook.code-workspace` (Ops root = `~/repos/supercat-4.0`; live
clients there = `~/repos/ecat-onboarding-workspace`).
See [`HANDOFF_OTHER_MACHINE.md`](./HANDOFF_OTHER_MACHINE.md). Hang-tag: `npm install`
locally in `~/repos/supercat-4.0/hang-tag-spike` if you use it.

## Source of truth

| Work | Where |
|---|---|
| Skills, rules, onboarding-agents, PM, foundation, reports | This working tree (`~/repos/supercat-4.0` on this Mac) |
| Live client onboarding (Legrand, jcusa, Fine Art, …) | iCloud `SuperCat_Simple_Final` → `02_Implementation/<Client>/` |
| Company weekly agents / PRs | `~/repos/agent-factory` |
| Active Insightful 4.0 pipeline (runtime + outputs) | local `Insightful Product 4.0/` (gitignored); source also in `agent-factory/agents/insightful_product` |
| Personas (who uses the product) | `personas/00-PERSONA-GROUPS.md` (Phase 2 creates this path) |

`eCat_Onboarding/` in this repo is **pointers + kickoff + registry only**.
Do not recreate live client folders here.

## Client data

Working CSVs (customers, products, order/invoice, territories) live in the
**private** `kylor-johnson/ecat-onboarding-workspace` repo by intent (this Mac:
iCloud `SuperCat_Simple_Final`). This ops repo does not hold those payloads.
`Ready_For_Import/` stays gitignored.

## Never commit

- Secrets — `.env`, `*service-account*.json`, HubSpot/Fathom/BigQuery keys under `integrations/`, Notion/Craft tokens, `mcp-config/`, `password_overrides.csv`
- `Ready_For_Import/*.csv`
- Transcript archives (`*transcript*.zip`)
- Python venvs (`.venv/`, `.venv-renderer/`)
- Nested `agent-factory/` (company repo; clone is `~/repos/agent-factory`)
- `cursor-to-claude-migration/` dumps (live keys)
- `_archive/`, `Scoping Build/`, `HTML System/`
- Finder ` 2` / ` 3` copies (`* 2.*`, `* 2/`, `* 3/`) — not `Health V2`, `EBR 2.0`, `HPMKT 2026`, or `Insightful Product 2.0`

## What's in here

| Path | Description |
|---|---|
| `.cursor/skills/`, `.cursor/rules/` | Agent skills and always-on import/data-model rules |
| `onboarding-agents/` | The four onboarding agents in one folder (ingestion, config check, HelpScout triage, session prep); see its README |
| `eCat_Onboarding/` | Kickoff prompt, registry, pointers to Implementation |
| `foundation/` | Company context (figures live in `foundation/sources/`) |
| `personas/` | Five consumption roles — `00-PERSONA-GROUPS.md` (Phase 2) |
| `PM/` | Program material |
| Analysis trees | Customer Intelligence, Segmentation, Pricing Migration, HPMKT, EBR, reports |

Agent orientation: [`AGENTS.md`](./AGENTS.md). Workspace: [`WORKSPACE.md`](./WORKSPACE.md).
Location map: [`WHERE.md`](./WHERE.md).
Other-Mac setup: [`HANDOFF_OTHER_MACHINE.md`](./HANDOFF_OTHER_MACHINE.md).
