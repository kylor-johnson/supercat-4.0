# AGENTS.md — SuperCat 4.0 workspace

> **Last updated**: 2026-09-16

Orientation for any agent working in this repo. Read this first, then the
`.cursor/rules/*.mdc` files (auto-loaded) and `CLAUDE.md` (same rules, ported).

**This file supersedes `README.md` for agent orientation.**

There are **four trees**. If a path here disagrees with an older doc,
[`WHERE.md`](WHERE.md) wins for *location*.

| Work | Path on this Mac | GitHub |
|---|---|---|
| **Ops** — skills, foundation, Insightful 4.0, Health V3, hang-tag | `~/repos/supercat-4.0` (this git working tree; remotes `origin` / `personal`) | `kylor-johnson/supercat-4.0` |
| **Live clients** — CSVs, `02_Implementation/<Client>/` | iCloud `SuperCat_Simple_Final` (also `~/repos/ecat-onboarding-workspace` symlink) | `kylor-johnson/ecat-onboarding-workspace` |
| **Product code** — Rails + iPad | `~/supercat-code` | `SuperCatSolutionsLLC/supercat_server`, `sarreid_ios` |
| **Company agents** — CEO system, factory `context/` | `~/repos/agent-factory` (never the nested copy inside SuperCat 4.0) | `SuperCatSolutionsLLC/agent-factory` |

**What this GitHub repo is:** the SuperCat operations subset — agent skills,
business foundation docs, PM material, onboarding *models*, and tracked analysis
trees. It is *not* the product codebase, *not* the live client-file tree, and
*not* a mirror of every folder sitting on disk next to this working tree.

Application source (`supercat_server`, `sarreid_ios`) lives at `~/supercat-code`.
Live client onboarding lives in iCloud **`SuperCat_Simple_Final`**
(`02_Implementation/<Client>/`, GitHub `kylor-johnson/ecat-onboarding-workspace`).
Company weekly agents live in `~/repos/agent-factory`
(`SuperCatSolutionsLLC/agent-factory`).

Personas (who is logged into the product): [`personas/00-PERSONA-GROUPS.md`](personas/00-PERSONA-GROUPS.md)
(Admin / VP of sales / executive / sales rep / buyer). Canonical after the 2026-09-16 rehome.
Selling-motion cells stay in `Customer Segmentation/current/`.

### Copy map — this tree → agent-factory

Keep these folder names here. Map on copy; do not reshape this ops tree into L0–L4.

| SuperCat 4.0 | Factory |
|---|---|
| `Insightful Product 4.0/` source (no `outputs/`, no `.venv-renderer/`) | **Hold** — do not copy until Kylor says the 4.0 pipeline is ready (factory #344 reverted) |
| `.cursor/skills/insightful-report-4/SKILL.md` | same hold |
| `Health V3/health_operator_v3.py` (V3.4.0, equal weights) + `{README,METHODOLOGY,RUN_PROMPT,FRESH_RUN_GUIDE,CHANGELOG,MAINTENANCE,ENVIRONMENT}` | `agents/ceo_system/onboarding_reality/health_v3/` — **factory copy is stale on V3.3.0 weights; port before relying on it** |
| Persona / JTBD (`personas/` — `00-PERSONA-GROUPS.md`) + splices in `foundation/00`–`02` and `CEO_SYSTEM_CONTEXT.md` | **Hold** — do not splice into factory `context/` (factory #347 closed) |
| `ttfv/` methodology + prompt (no result CSVs) | `agents/ceo_system/ttfv/` (factory PR #348, still open) |
| `_museums/Insightful Product 2.0/` / `3.0/`, `_museums/Health V2/`, Implementation CSVs, `eCat_Onboarding/` | **Do not copy** — onboarding agent is unfinished local work |
| `hang-tag-spike/` | **Do not copy** — hang-tag Next prototype stays in this ops repo |

Open **File → Open Workspace from File… →**
`~/repos/supercat-4.0/SuperCat.code-workspace`.

That folder **is** `kylor-johnson/supercat-4.0` (remotes `origin` and `personal`).

**iCloud `SuperCat 4.0` is an unread trap.** Do not open it, do not commit from
it. Leave it on disk; it is not the working tree.

The other Mac also uses `~/repos/supercat-4.0` — see `HANDOFF_OTHER_MACHINE.md`
and `SuperCat.macbook.code-workspace`. Live clients on this Mac stay iCloud
`SuperCat_Simple_Final` (also the `~/repos/ecat-onboarding-workspace` symlink).
Hang-tag: `npm install` locally in `~/repos/supercat-4.0/hang-tag-spike` if you
use it (`node_modules` is gitignored).

---

## What GitHub tracks vs what stays local

`git status` against `origin/main` (or `personal/main`) is the GitHub tree. Venvs, secrets, and the
nested company `agent-factory/` clone stay gitignored. Health and Insightful
**source** (not venvs) are tracked here so they can be copied into
`SuperCatSolutionsLLC/agent-factory`.

### Tracked in `kylor-johnson/supercat-4.0`

Skills, rules, foundation, onboarding-models, PM, reports, design-system,
Customer Segmentation, Peer Benchmark, Pricing Migration V2,
EBR/HPMKT 2026, eCat_Onboarding pointers, kb-articles, documentation, prompts,
scripts (the tracked files), ttfv, validation-reports,
`Health V3/` (source + runs, no venv),
`Insightful Product 4.0/` (active pipeline),
`_museums/` (Insightful 2.0/3.0, Health V2, Customer Intelligence, Pricing Migration v1, HPMKT 2.0),
`Migration-Health Artifacts/`, `hang-tag-spike/` (Next prototype; no `node_modules`).

### Local-only — do not copy into git

| Folder | Why |
|---|---|
| `agent-factory/` (nested) | Already `SuperCatSolutionsLLC/agent-factory`. Use `~/repos/agent-factory`. |
| `cursor-to-claude-migration/` and `-macbook/` | Live secrets (BQ keys, Fathom, VPN, MCP passwords). |
| `.venv/`, `.venv-renderer/`, `.venv_broken*` | Python environments. Recreate locally. |
| `chat-history/`, `scratch/`, `files 2/`, `_archive/`, `Scoping Build/`, `HTML System/` | Dumps, Finder dupes, empty skeleton (successor is `design-system/`). |
| `_museums/Insightful Product 3.0/password_overrides.csv` | Hosted-report passwords. |
| `repos/` / `repos 2/` | iCloud dump of nested clones. Hang-tag lives at `hang-tag-spike/`. |

### Never commit

Secrets, keys, tokens, VPN profiles — including
`cursor-to-claude-migration/`, `cursor-to-claude-migration-macbook/`,
`integrations/bigquery/`, `integrations/fathom/`, `integrations/hubspot/`,
`mcp-config/`, Notion helper scripts under `scripts/`, and
`password_overrides.csv`.
Live MCP is `~/.cursor/mcp.json`. Credentials live in `~/.supercat/`.

---

## Workspace map

### Agent infrastructure
| Path | Purpose |
|---|---|
| `.claude/skills/` | Claude Code project skills (in-repo): `supercat-foundation`, `truth-discipline`. |
| `.cursor/skills/` | 31 Cursor agent skills (in-repo, git-tracked). See skill index below. |
| `.cursor/rules/` | 8 always-on rules (`.mdc`) — import ground truth, data model, Jira read-only, canvas ban, legacy freeze. |
| `CLAUDE.md` | The `alwaysApply` rules ported for Claude Code. Generated from `.cursor/rules/`. |
| `.cursorignore` | Excludes `_museums/` (legacy Insightful/Health/program folders) and migration attics from indexing. Insightful 4.0 stays indexed. |
| `prompts/`, `KB Creation prompts/` | Reusable prompt material. |

### Business foundation
| Path | Purpose |
|---|---|
| `foundation/` | The socializable company context. `00`–`06` strategic pillar; `07` epistemic (how we establish truth); `08`–`09` operating pillar (how we build, agent factory); plus `CEO_SYSTEM_CONTEXT.md` and `PLATFORM_ANATOMY_CURRENT_STATE.md`. |
| `foundation/sources/` | The **stamped sources** `foundation/` cites and summarizes — pricing constitution, monetization/competitive/install-base research, CEO-system artifact catalog, FY26 plan, BCF reference instance, segmentation README + buyer-type reads. **On conflict, the stamped source wins over `foundation/`.** Imported from the 2026-08-05 foundation pack. Not the home of the persona product. |
| `personas/` | Five consumption roles (Admin / VP of sales / executive / sales rep / buyer). Canon: `personas/00-PERSONA-GROUPS.md`. Orthogonal to `Customer Segmentation/current/`. |
| `Supercat_CEO_system_README.md`, `QBO_Invoice_BigQuery_Dedup_Guide_README.md` | Root-level companions — operating-cadence overview, and the mandatory dedup pattern for `quickbooks__invoice` in BigQuery (read before any AR/balance/overdue query). |
| `PM/` | Program material — Admin console, Sales Portal docs, eCat web rewrite estimates, agent starters. |

### Client onboarding
| Path | Purpose |
|---|---|
| `eCat_Onboarding/` | **Pointers only** — kickoff, registry, `jcusa.md`. Live client folders are in iCloud `SuperCat_Simple_Final/02_Implementation/`. **Never recreate client folders here.** |
| `onboarding-models/` | Phase framework, output contracts, HTML artifact contract, questionnaire, rendering pipeline. |
| `kb-articles/`, `KB - Net New/`, `documentation/` | Knowledge-base source and drafts. |

### Analysis & reporting (tracked)
| Path | Purpose |
|---|---|
| `reports/` | Generated client reports (EBR, closed deals, feature analysis) in `.md` + `.html`. |
| `Customer Segmentation/`, `Peer Benchmark/` | Segmentation and benchmarking analysis. |
| `Pricing Migration V2/` | Pricing migration program (v1 is in `_museums/`). |
| `EBR 2.0/`, `HPMKT 2026/` | Business-review and High Point Market material (HPMKT 2.0 is in `_museums/`). |
| `ttfv/`, `Data Scoping/`, `validation-reports/` | Time-to-first-value, scoping, and validation datasets. |
| `scripts/` | Tracked analysis scripts only. Untracked dumps and Notion helpers stay local. |
| `Health V3/` | Account-health scoring — the single source of truth. Source + runs + 7-month backfill (venv gitignored). Read `MAINTENANCE.md` first. Health V2 is in `_museums/`. |
| `Insightful Product 4.0/` | Active CEO-intelligence pipeline (`CANON.md`, `run.sh`, `pipeline/`). |
| `_museums/` | Frozen Insightful 2.0/3.0, Health V2, Customer Intelligence, Pricing Migration v1, HPMKT 2.0. |
| `Migration-Health Artifacts/` | Pricing-migration health brief templates. |

### Presentation
| Path | Purpose |
|---|---|
| `design-system/` | Shared design system, templates, data contracts for HTML deliverables. |

---

## Active vs frozen

**Frozen — do not read, grep, cite, or run without an explicit per-conversation request:**

| Folder | Location |
|---|---|
| `Insightful Product` (original) | `iCloud Drive/Insightful Product/` — sibling to this folder |
| `_museums/` | Insightful 2.0/3.0, Health V2, Customer Intelligence, Pricing Migration v1, HPMKT 2.0. Nested remote `kylor-johnson/Insightful-2.0` under 3.0. Do not open unless asked. |

The freeze is enforced by `.cursorignore` and `.cursor/rules/insightful-legacy-frozen.mdc`.

- **Active Insightful work is `Insightful Product 4.0/`** in this repo (venv gitignored)
  plus `~/repos/agent-factory/agents/insightful_product`. A bare "run a report for X"
  means the 4.0 report (`insightful-report-4`), never 2.0.
- The `insightful-report` skill targets frozen 2.0 at `_museums/Insightful Product 2.0/` — only invoke it when the
  user explicitly says "2.0" or "legacy".
- If it is ambiguous whether a request means 4.0 or a legacy version, ask once
  before touching a frozen path.

Also treat as low-trust rather than frozen: `_archive/`, `scratch/`, `files 2/`,
`Scoping Build/`, `HTML System/`, and any `* 2.md` / `* 2.py` duplicate — copies,
not sources of truth. Finder ` 2` / ` 3` copies are gitignored (`* 2.*`, `* 2/`,
`* 3/`); versioned trees (`EBR 2.0`, `Health V2`, `HPMKT 2026`, `* 2.0`) are not.

`Health V3/` is current scoring — one folder, no companion clone (the old
`Health V3 Backfill/` was merged into it on 2026-09-16). Health V2 is in
`_museums/`. Do not treat health scoring as the Insightful 4.0 pipeline.

---

## File conventions

**Output format**
- Results go in **chat** as markdown — tables, bullets, fenced code.
- Saved deliverables are normal repo files (`.md`, `.csv`, `.html`).

**Naming**
- Dated artifacts: `YYYY-MM-DD` prefix or suffix (`2026-07-16__name.md`).
- Assessment / ground-truth is keyed by **org shortname** (`mali`, `libco`, `drf`, `pebl`, `leg`).
  Live implementation folders use full client names in iCloud `SuperCat_Simple_Final`.
- Reports commonly ship as a `.md` + `.html` pair with the same stem.
- Docs carry a `> **Last updated**: YYYY-MM-DD` line near the top — **bump it when
  you change the file.** Several `foundation/` docs currently have edits that
  were made without bumping the stamp; do not add to that.

**Never commit**
- Secrets — `.env`, `*service-account*.json`, HubSpot/Fathom/BigQuery keys under `integrations/`, Notion/Craft tokens, `mcp-config/`
- `Ready_For_Import/*.csv` (staging payloads)
- Transcript archives (`*transcript*.zip`)
- Live client CSVs into *this* repo — they belong in the private
  `kylor-johnson/ecat-onboarding-workspace` repo (this Mac: iCloud `SuperCat_Simple_Final`)
- Recreated `eCat_Onboarding/<client>/` trees
- Nested `agent-factory/`, `_archive/`, `Scoping Build/`
- Venvs, `password_overrides.csv`, migration-kit secret dumps

**Skills live in three places.**

| Location | Holds | Read by |
|---|---|---|
| `.cursor/skills/` | 31 skills, in-repo, tracked | Cursor |
| `~/.claude/skills/` | independent copies of the same skill set, outside the repo | Claude Code (user scope) |
| `.claude/skills/` | `supercat-foundation`, `truth-discipline` — in-repo, tracked | Claude Code (project scope) |

The first two are **copies, not symlinks**. **When you edit a skill that exists
in both, update both copies** or they drift. `.claude/skills/` is the in-repo
home for new Claude Code skills; add there rather than deepening the two-copy
split.

---

## Data routing (mandatory)

For **any** live org/account/customer question — org settings, feature flags
(eOL, Sales Portal, iPad), users, imports, inventory, adoption, health, support
history, billing — consult the **`supercat-data-routing`** skill *before*
querying and *before* any customer-facing draft. Use `supercat-postgres-vpn` or
`bigquery-admin` as it directs. **`supercat-cs-tools` is retired — do not use it.**

Operational rules (Jira read-only, canvas ban, GraphQL introspection, import
ground truth) live in `CLAUDE.md` and `.cursor/rules/` — auto-loaded, not
restated here.

---

## Skill index

31 skills in `.cursor/skills/`. Two of those (`supercat-foundation`,
`truth-discipline`) are also copied under `.claude/skills/`.

### Company context
| Skill | Use it for |
|---|---|
| `supercat-foundation` | **Before** answering anything about what SuperCat is, who we serve, pricing/ACV/tiers, competitors, strategic bets, or FY26 targets — including in customer-, investor-, or board-facing drafts. A router: it holds no figures, it points at `foundation/` and `foundation/sources/`. Never answer these from memory; the figures move quarterly. |
| `truth-discipline` | **Whenever an output will state a figure** about customers, revenue, GMV, orders, reps, adoption, health, or market size — reports, charts, decks, a Slack answer, a number dropped mid-sentence. Confidence tiers, capture vs. attribution, billed ≠ collected, suppress-rather-than-guess, and the QuickBooks invoice dedup trap. Binds on the output, not the question. |
| `finish-the-job` | Standing working agreement — finish the whole request in one pass; decide instead of asking when a default exists; verify instead of assuming. |

### Onboarding orchestration
| Skill | Use it for |
|---|---|
| `ecat-onboarding-orchestrator` | Drive an onboarding end to end — read client state, determine phase, route to the right skill, enforce the phase gate. **Start here** when unsure which skill applies. |
| `ecat-session-handoff` | End-of-session handoff so the next chat starts with full context. |
| `ecat-session-prep` | Ten-minute pre-call brief: what moved, what we committed to, what is still unanswered, what to show. |
| `ecat-support-triage` | One-off ticket or client email — diagnose, route, ground in live state, draft a reply. Use instead of the orchestrator for ad-hoc issues. |
| `ecat-correspondence` | Inbox loop: decide what needs a reply, route to triage, draft, gate whether it is safe to send. Drafts only — never sends. |
| `ecat-config-check` | Read-only Admin Console config audit by shortname — wrong, missing, or contradictory settings. |

### eCat build & configuration
| Skill | Use it for |
|---|---|
| `ecat-core-files` | `products.csv` / `stories.csv` / `inventory.csv` — fields, lengths, validation, build workflow. |
| `ecat-customers-build` | `customers.csv` — bill-to/ship-to, DefaultPriceCode, TerritoryCodes, ERP mapping. |
| `ecat-options-and-mapping` | Options stack and Admin Option Mapping cascades. |
| `ecat-pricing-levels` | Imported vs arithmetic price levels, `Price_<code>`, promo levels, divisions, matrix pricing. |
| `ecat-images-ftp` | Product/option images over FTP, filename normalization, missing-image triage. |
| `ecat-smartlists` | Query-based and hand-picked SmartLists, publishing, user-group authorization. |
| `ecat-go-live` | Data-loaded → rep-ready: users, groups, invitations, territories, order email, go-live checklist. |

### eCat surfaces & runtime
| Skill | Use it for |
|---|---|
| `ecat-ipad-app` | iPad runtime behavior — sync, permissions, territory filtering, on-device pricing, order submit. |
| `ecat-online` | eCat Online (eOL) — web catalog, Cart, buyer enrollment, My Account markup pricing. |
| `ecat-sales-portal-onboarding` | Net-new Sales Portal builds — `order_data.csv`, `invoice_data.csv`, territories, ERP history. |
| `ecat-postgres-audit` | Read-only Postgres audits by shortname — counts, imports, image matching, config. |
| `ecat-admin-write` | Apply a live-org change through Admin Console HTTP as a logged-in user. Postgres MCP is read-only; this is the write path. |
| `supercat-mcp-access` | Capability map for live-org writes (`~/.supercat/mcp-credentials.json`) and wedged-session diagnosis. |

### Client communication
| Skill | Use it for |
|---|---|
| `ecat-client-email` | Onboarding/support email in Kylor's voice. **Not** for pricing-migration notices. |
| `hpmkt-follow-up-email` | High Point Market follow-ups from transcripts, Kjael style. |

### Reporting & data
| Skill | Use it for |
|---|---|
| `supercat-data-routing` | **Consult before any org/data question or customer-facing draft.** |
| `insightful-report-4` | **Default** Insightful 4.0 CEO Intelligence Report. |
| `insightful-report` | Legacy 2.0 report — targets a frozen folder. Explicit request only. |
| `supercat-jira` | Search Jira before proposing engineering work; write tickets in house format. Duplicate search before any draft. |

### Engineering (targets `~/supercat-code`)
| Skill | Use it for |
|---|---|
| `admin-page-migration` | Legacy Bootstrap/jQuery → Tailwind/Stimulus/ViewComponent admin pages. |
| `migration-audit` | Admin v2 migration coverage — which controller actions render in v2 layouts. |
| `rails-code-review` | Rails PR/branch review. |

Harness-provided skills (`dataviz`, `artifact-design`, `code-review`, `loop`,
`schedule`, `claude-api`, …) are not installed here and are not listed above.
