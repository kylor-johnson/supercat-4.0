# AGENTS.md — SuperCat 4.0 workspace

> **Last updated**: 2026-09-15

Orientation for any agent working in this repo. Read this first, then the
`.cursor/rules/*.mdc` files (auto-loaded) and `CLAUDE.md` (same rules, ported).

**This file supersedes `README.md` for agent orientation.**

**What this GitHub repo is:** the SuperCat operations subset — agent skills,
business foundation docs, PM material, onboarding *models*, and tracked analysis
trees. It is *not* the product codebase, *not* the live client-file tree, and
*not* a mirror of every folder sitting on disk next to this working tree.

Application source (`supercat_server`, `sarreid_ios`) lives at `~/supercat-code`.
Live client onboarding lives in the **private** repo
`~/repos/ecat-onboarding-workspace` (`02_Implementation/<Client>/`).
Company weekly agents live in `~/repos/agent-factory`
(`SuperCatSolutionsLLC/agent-factory`).

### Copy map — this tree → agent-factory

Keep these folder names here. Map on copy; do not reshape this ops tree into L0–L4.

| SuperCat 4.0 | Factory |
|---|---|
| `Insightful Product 4.0/` source (no `outputs/`, no `.venv-renderer/`) | **Hold** — do not copy until Kylor says the 4.0 pipeline is ready (factory #344 reverted) |
| `.cursor/skills/insightful-report-4/SKILL.md` | same hold |
| `Health V3/health_operator_v3.py` (V3.3.0) | `agents/ceo_system/onboarding_reality/health_v3/health_operator_v3.py` |
| `Health V3 Backfill/{README,METHODOLOGY,RUN_PROMPT,FRESH_RUN_GUIDE,CHANGELOG}` | same `health_v3/` folder |
| Persona / JTBD (`foundation/sources/customer_segmentation/{personas,analytics,product,taxonomy}`) + splices in `foundation/00`–`02` and `CEO_SYSTEM_CONTEXT.md` | **Hold** — do not splice into factory `context/` (factory #347 closed) |
| `ttfv/` methodology + prompt (no result CSVs) | `agents/ceo_system/ttfv/` (factory PR #348, still open) |
| `Insightful Product 2.0/` / `3.0/`, `Health V2/`, Implementation CSVs, `eCat_Onboarding/` | **Do not copy** — onboarding agent is unfinished local work |

**This Mac — source of truth (edit here):**

| Work | Path |
|---|---|
| Ops (this git working tree) | `~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0` |
| Live client implementation | `~/repos/ecat-onboarding-workspace` |
| Product code | `~/supercat-code` |
| Company agent-factory clone | `~/repos/agent-factory` (not the nested copy inside this folder) |

Open **File → Open Workspace from File… →**
`~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/SuperCat.code-workspace`.

That folder **is** `kylor-johnson/supercat-4.0` (remote name `personal`). There is
no `~/repos/supercat-4.0` on this Mac. Do not recreate that clone here.

The other Mac clones under `~/repos` — see `HANDOFF_OTHER_MACHINE.md` and
`SuperCat.code.macbook-workspace`.

---

## What GitHub tracks vs what stays local

`git status` against `personal/main` is the GitHub tree. Venvs, secrets, and the
nested company `agent-factory/` clone stay gitignored. Health and Insightful
**source** (not venvs) are tracked here so they can be copied into
`SuperCatSolutionsLLC/agent-factory`.

### Tracked in `kylor-johnson/supercat-4.0`

Skills, rules, foundation, onboarding-models, PM, reports, design-system,
Customer Intelligence/Segmentation, Peer Benchmark, Pricing Migration,
EBR/HPMKT, eCat_Onboarding pointers, kb-articles, documentation, prompts,
scripts (the tracked files), ttfv, validation-reports,
`Health V2/` / `Health V3/` / `Health V3 Backfill/` (source + runs, no venv),
`Insightful Product 2.0/` / `3.0/` / `4.0/` (source; 4.0 is the active pipeline),
`Migration-Health Artifacts/`.

### Local-only — do not copy into git

| Folder | Why |
|---|---|
| `agent-factory/` (nested) | Already `SuperCatSolutionsLLC/agent-factory`. Use `~/repos/agent-factory`. |
| `cursor-to-claude-migration/` and `-macbook/` | Live secrets (BQ keys, Fathom, VPN, MCP passwords). |
| `.venv/`, `.venv-renderer/`, `.venv_broken*` | Python environments. Recreate locally. |
| `chat-history/`, `scratch/`, `files 2/`, `_archive/`, `Scoping Build/`, `HTML System/` | Dumps, Finder dupes, empty skeleton (successor is `design-system/`). |
| `Insightful Product 3.0/password_overrides.csv` | Hosted-report passwords. |

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
| `.cursorignore` | Excludes frozen Insightful 2.0/3.0, Health museums, and migration attics from indexing. Insightful 4.0 stays indexed. |
| `prompts/`, `KB Creation prompts/` | Reusable prompt material. |

### Business foundation
| Path | Purpose |
|---|---|
| `foundation/` | The socializable company context. `00`–`06` strategic pillar; `07` epistemic (how we establish truth); `08`–`09` operating pillar (how we build, agent factory); plus `CEO_SYSTEM_CONTEXT.md` and `PLATFORM_ANATOMY_CURRENT_STATE.md`. |
| `foundation/sources/` | The **stamped sources** `foundation/` cites and summarizes — pricing constitution, monetization/competitive/install-base research, CEO-system artifact catalog, FY26 plan, BCF reference instance, segmentation README + buyer-type reads. **On conflict, the stamped source wins over `foundation/`.** Imported from the 2026-08-05 foundation pack. |
| `Supercat_CEO_system_README.md`, `QBO_Invoice_BigQuery_Dedup_Guide_README.md` | Root-level companions — operating-cadence overview, and the mandatory dedup pattern for `quickbooks__invoice` in BigQuery (read before any AR/balance/overdue query). |
| `PM/` | Program material — Admin console, Sales Portal docs, eCat web rewrite estimates, agent starters. |

### Client onboarding
| Path | Purpose |
|---|---|
| `eCat_Onboarding/` | **Pointers only** — kickoff, registry, `jcusa.md`. Live client folders are in `~/repos/ecat-onboarding-workspace/02_Implementation/`. **Never recreate client folders here.** |
| `onboarding-models/` | Phase framework, output contracts, HTML artifact contract, questionnaire, rendering pipeline. |
| `kb-articles/`, `KB - Net New/`, `documentation/` | Knowledge-base source and drafts. |

### Analysis & reporting (tracked)
| Path | Purpose |
|---|---|
| `reports/` | Generated client reports (EBR, closed deals, feature analysis) in `.md` + `.html`. |
| `Customer Intelligence/`, `Customer Segmentation/`, `Peer Benchmark/` | Segmentation and benchmarking analysis. |
| `Pricing Migration/`, `Pricing Migration V2/` | Pricing migration program. |
| `EBR 2.0/`, `HPMKT 2.0/`, `HPMKT 2026/` | Business-review and High Point Market material. |
| `ttfv/`, `Data Scoping/`, `validation-reports/` | Time-to-first-value, scoping, and validation datasets. |
| `scripts/` | Tracked analysis scripts only. Untracked dumps and Notion helpers stay local. |
| `Health V2/`, `Health V3/`, `Health V3 Backfill/` | Account-health scoring source + runs (venvs gitignored). |
| `Insightful Product 4.0/` | Active CEO-intelligence pipeline (`CANON.md`, `run.sh`, `pipeline/`). |
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
| `Insightful Product 2.0/` | in-repo; frozen. Do not use unless asked. |
| `Insightful Product 3.0/` | in-repo; frozen. Nested remote `kylor-johnson/Insightful-2.0`. Passwords not committed. |

The freeze is enforced by `.cursorignore` and `.cursor/rules/insightful-legacy-frozen.mdc`.

- **Active Insightful work is `Insightful Product 4.0/`** in this repo (venv gitignored)
  plus `~/repos/agent-factory/agents/insightful_product`. A bare "run a report for X"
  means the 4.0 report (`insightful-report-4`), never 2.0.
- The `insightful-report` skill targets frozen 2.0 — only invoke it when the
  user explicitly says "2.0" or "legacy".
- If it is ambiguous whether a request means 4.0 or a legacy version, ask once
  before touching a frozen path.

Also treat as low-trust rather than frozen: `_archive/`, `scratch/`, `files 2/`,
`Scoping Build/`, `HTML System/`, and any `* 2.md` / `* 2.py` duplicate — copies,
not sources of truth.

Health V2 / V3 / V3 Backfill are tracked historical scoring. Read them when the
user asks about health scoring or backfill; do not treat them as the Insightful 4.0 pipeline.

---

## File conventions

**Output format**
- Results go in **chat** as markdown — tables, bullets, fenced code.
- Saved deliverables are normal repo files (`.md`, `.csv`, `.html`).

**Naming**
- Dated artifacts: `YYYY-MM-DD` prefix or suffix (`2026-07-16__name.md`).
- Assessment / ground-truth is keyed by **org shortname** (`mali`, `libco`, `drf`, `pebl`, `leg`).
  Live implementation folders use full client names in `ecat-onboarding-workspace`.
- Reports commonly ship as a `.md` + `.html` pair with the same stem.
- Docs carry a `> **Last updated**: YYYY-MM-DD` line near the top — **bump it when
  you change the file.** Several `foundation/` docs currently have edits that
  were made without bumping the stamp; do not add to that.

**Never commit**
- Secrets — `.env`, `*service-account*.json`, HubSpot/Fathom/BigQuery keys under `integrations/`, Notion/Craft tokens, `mcp-config/`
- `Ready_For_Import/*.csv` (staging payloads)
- Transcript archives (`*transcript*.zip`)
- Live client CSVs into *this* repo — they belong in the private
  `kylor-johnson/ecat-onboarding-workspace` repo by intent
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
