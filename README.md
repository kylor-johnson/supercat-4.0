# SuperCat 4.0 — operations workspace

> **Last updated**: 2026-09-15

Personal GitHub repo (`kylor-johnson/supercat-4.0`) for SuperCat operations:
Cursor/Claude skills, import rules, onboarding models, foundation docs, PM
material, and tracked analysis/report trees.

It is **not** the product codebase (`~/supercat-code`) and **not** the live
client-implementation tree. It is also **not** a dump of every folder in the
local SuperCat 4.0 directory — Health / Insightful museums, venvs, and nested
`agent-factory/` stay on disk and out of git.

## This Mac — how to open

**File → Open Workspace from File… →**
`~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/SuperCat.code-workspace`

That iCloud folder **is** this git working tree (remote `personal` →
`kylor-johnson/supercat-4.0`). `~/repos/supercat-4.0` does not exist on this Mac.
Do not recreate that clone here.

Three roots:

| Root | Path | What lives there |
|---|---|---|
| SuperCat Ops | iCloud `SuperCat 4.0` | This repo |
| eCat Implementation | `~/repos/ecat-onboarding-workspace` | Live client CSVs + build work (`02_Implementation/`) |
| supercat-code | `~/supercat-code` | Rails / iOS application source |

The **other Mac** clones under `~/repos` and opens
`SuperCat.macbook.code-workspace` (Ops root = `~/repos/supercat-4.0`).
See [`HANDOFF_OTHER_MACHINE.md`](./HANDOFF_OTHER_MACHINE.md).

## Source of truth

| Work | Where |
|---|---|
| Skills, rules, onboarding-models, PM, foundation, reports | This working tree (iCloud `SuperCat 4.0` on this Mac) |
| Live client onboarding (Legrand, jcusa, Fine Art, …) | `~/repos/ecat-onboarding-workspace` → `02_Implementation/<Client>/` |
| Company weekly agents / PRs | `~/repos/agent-factory` |
| Active Insightful 4.0 pipeline (runtime + outputs) | local `Insightful Product 4.0/` (gitignored); source also in `agent-factory/agents/insightful_product` |

`eCat_Onboarding/` in this repo is **pointers + kickoff + registry only**.
Do not recreate live client folders here.

## Client data

Working CSVs (customers, products, order/invoice, territories) live in the
**private** `kylor-johnson/ecat-onboarding-workspace` repo by intent. This
ops repo does not hold those payloads. `Ready_For_Import/` stays gitignored.

## Never commit

- Secrets — `.env`, `*service-account*.json`, HubSpot/Fathom/BigQuery keys under `integrations/`, Notion/Craft tokens, `mcp-config/`, `password_overrides.csv`
- `Ready_For_Import/*.csv`
- Transcript archives (`*transcript*.zip`)
- Python venvs (`.venv/`, `.venv-renderer/`)
- Nested `agent-factory/` (company repo; clone is `~/repos/agent-factory`)
- `cursor-to-claude-migration/` dumps (live keys)
- `_archive/`, `Scoping Build/`, `HTML System/`

## What's in here

| Path | Description |
|---|---|
| `.cursor/skills/`, `.cursor/rules/` | Agent skills and always-on import/data-model rules |
| `onboarding-models/` | Phase framework, acceptance checks, ground-truth, collector |
| `eCat_Onboarding/` | Kickoff prompt, registry, pointers to Implementation |
| `foundation/` | Company context (figures live in `foundation/sources/`) |
| `PM/` | Program material |
| Analysis trees | Customer Intelligence, Segmentation, Pricing Migration, HPMKT, EBR, reports |

Agent orientation: [`AGENTS.md`](./AGENTS.md). Workspace: [`WORKSPACE.md`](./WORKSPACE.md).
Other-Mac setup: [`HANDOFF_OTHER_MACHINE.md`](./HANDOFF_OTHER_MACHINE.md).
