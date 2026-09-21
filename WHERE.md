# Where things live

> **Last updated**: 2026-09-16
>
> One page. If a path here disagrees with an older README, this file wins for
> *location*. Stamped numbers and the v4.0 roster still win for *content*.

There are **four trees**, not one SuperCat folder. GitHub is **two owners**, not one pile.

## The four trees (this Mac)

| Work | Path on this Mac | GitHub |
|---|---|---|
| **Ops** — skills, foundation, Insightful 4.0, Health V3, hang-tag | `~/repos/supercat-4.0` (this git working tree; remotes `origin` / `personal`) | `kylor-johnson/supercat-4.0` |
| **Live clients** — CSVs, `02_Implementation/<Client>/` | iCloud `SuperCat_Simple_Final` (also `~/repos/ecat-onboarding-workspace` symlink) | `kylor-johnson/ecat-onboarding-workspace` |
| **Product code** — Rails + iPad | `~/supercat-code/{supercat_server,sarreid_ios}` | `SuperCatSolutionsLLC/supercat_server`, `sarreid_ios` |
| **Company agents** — CEO system, factory `context/` | `~/repos/agent-factory` (one clone; never the nested copy inside SuperCat 4.0) | `SuperCatSolutionsLLC/agent-factory` |

Open **File → Open Workspace from File… →** `~/repos/supercat-4.0/SuperCat.code-workspace`.

**iCloud `SuperCat 4.0` is an unread trap.** Do not open it, do not commit from it. Leave it on disk.

Do **not** open nested iCloud `SuperCat 4.0/repos/`, `repos 2/`, or `SuperCat 4.0/agent-factory/`. Those were iCloud dumps of the same remotes.

## Who we serve — two homes, two questions

These are orthogonal. They do not share a folder name.

| Question | Canonical path | Do not |
|---|---|---|
| What game is this **client organisation** playing? (Lens 2 selling motion) | [`Customer Segmentation/current/`](Customer%20Segmentation/current/) — stamped v4.0, 109 orgs, MASTER csv + dark HTML | Re-derive the label; assign a segment to a prospect; restyle the roster |
| Who is logged into **our product**, and which surface do they use? | [`personas/00-PERSONA-GROUPS.md`](personas/00-PERSONA-GROUPS.md) — Admin / VP of sales / executive / sales rep / buyer (moved off `foundation/sources/` in the 2026-09-16 rehome) | Mint extra SuperCat personas from selling-motion cells |

`foundation/02_who_we_serve.md` is the **hour briefing** that cites both. `foundation/sources/` holds **stamped research packs** the briefing cites (pricing constitution, BCF profile). It is not the home of the persona product.

Lens 1 (Digital Selling Maturity / T1–T3) lives in the monetization pack under `foundation/sources/monetization_refresh_2026/`.

## GitHub — personal vs company

**Personal (`kylor-johnson/`)** — Kylor’s ops and live client files:

- `supercat-4.0` — this ops tree
- `ecat-onboarding-workspace` — live implementation
- `Insightful-2.0` — museum (nested remote under frozen Insightful 3.0)

**Company (`SuperCatSolutionsLLC/`)** — product, factory, CEO site, infra. Do **not** reshape this ops tree into factory L0–L4. Copy map is in `AGENTS.md`. Insightful 4.0 and personas stay **Hold** until Kylor lifts it.

Stale / do not treat as current: `agentic_operations`, old `insightful_product`, `SuperCatSolutionsLLC/foundation` (zombie overlap with this tree’s `foundation/`).

## Products we run (in this ops tree)

| Product | Path |
|---|---|
| Insightful 4.0 (active) | `Insightful Product 4.0/` |
| Health V3.4.0 (canonical `6a2f1d9f…`) | `Health V3/` |
| TTFV | `ttfv/` |
| Hang-tag spike | `hang-tag-spike/` |

Museums (do not open unless asked): [`_museums/`](_museums/README.md) — `Insightful Product 2.0/`, `Insightful Product 3.0/` (nested remote `kylor-johnson/Insightful-2.0`), `Health V2/`, `Customer Intelligence/`, `Pricing Migration/` (v1), `HPMKT 2.0/`. Active counterparts stay at root: Insightful 4.0, Health V3, Pricing Migration V2, HPMKT 2026. Sibling `iCloud Drive/Insightful Product/` is also frozen. `HTML System/` and `Scoping Build/` are gitignored at root (not museumed).

## Secrets

Live MCP: `~/.cursor/mcp.json`. Credentials: `~/.supercat/`. Never commit `cursor-to-claude-migration*`, `integrations/` keys, `mcp-config/`, `password_overrides.csv`.
