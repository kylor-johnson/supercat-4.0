# SuperCat 4.0 — operations workspace

Personal GitHub repo (`kylor-johnson/supercat-4.0`) for SuperCat operations:
Cursor/Claude skills, import rules, onboarding models, foundation docs, PM
material, and analysis/report trees.

It is **not** the product codebase (`~/supercat-code`) and **not** the live
client-implementation tree.

## How to open

**File → Open Workspace from File… → `~/repos/supercat-4.0/SuperCat.code-workspace`**

Three roots:

| Root | Clone | What lives there |
|---|---|---|
| SuperCat Ops | `~/repos/supercat-4.0` | This repo |
| eCat Implementation | `~/repos/ecat-onboarding-workspace` | Live client CSVs + build work (`02_Implementation/`) |
| supercat-code | `~/supercat-code` | Rails / iOS application source |

Do not open iCloud `SuperCat 4.0` as the working folder. iCloud is leftover
sync, not the edit surface.

## Source of truth

| Work | Repo |
|---|---|
| Skills, rules, onboarding-models, PM, foundation, reports | `~/repos/supercat-4.0` |
| Live client onboarding (Legrand, jcusa, Fine Art, …) | `~/repos/ecat-onboarding-workspace` → `02_Implementation/<Client>/` |
| Company weekly agents / PRs | `~/repos/agent-factory` |

`eCat_Onboarding/` in this repo is **pointers + kickoff + registry only**.
Do not recreate live client folders here.

## Client data

Working CSVs (customers, products, order/invoice, territories) live in the
**private** `kylor-johnson/ecat-onboarding-workspace` repo by intent. This
ops repo does not hold those payloads. `Ready_For_Import/` stays gitignored.

## Never commit

- Secrets — `.env`, `*service-account*.json`, HubSpot/Fathom/BigQuery keys under `integrations/`
- `Ready_For_Import/*.csv`
- Transcript archives (`*transcript*.zip`)
- Frozen Insightful / Health museum trees
- Nested `agent-factory/`

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
