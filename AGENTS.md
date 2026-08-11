# AGENTS.md — SuperCat 4.0 workspace

Orientation for any agent working in this repo. Read this first, then the
`.cursor/rules/*.mdc` files (auto-loaded) and `CLAUDE.md` (same rules, ported).

**This file supersedes `README.md` for agent orientation.** `README.md` describes
an earlier, narrower scope and is stale.

**What this repo is:** the SuperCat operations workspace — client onboarding,
agent skills, business foundation docs, reporting pipelines, and PM material.
It is *not* the product codebase. Application source (`supercat_server`,
`sarreid_ios`) lives at `~/supercat-code` and is opened as a second root via
`SuperCat.code-workspace` (see `WORKSPACE.md`).

**Location caveat:** this workspace lives in iCloud Drive
(`~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0`). Paths contain
spaces and `~` characters — always quote paths in shell commands.

---

## Workspace map

### Agent infrastructure
| Path | Purpose |
|---|---|
| `.cursor/skills/` | 22 agent skills (in-repo, git-tracked). See skill index below. |
| `.cursor/rules/` | 8 always-on rules (`.mdc`) — import ground truth, data model, Jira read-only, canvas ban, legacy freeze. |
| `CLAUDE.md` | The `alwaysApply` rules ported for Claude Code. Generated from `.cursor/rules/`. |
| `.cursorignore` | Excludes frozen Insightful folders from indexing. |
| `mcp-config/`, `integrations/` | MCP and external-service config (BigQuery, Craft CMS, Fathom, HubSpot, Notion). |
| `prompts/`, `KB Creation prompts/` | Reusable prompt material. |

### Business foundation
| Path | Purpose |
|---|---|
| `foundation/` | The socializable company context. `00`–`06` strategic pillar; `07` epistemic (how we establish truth); `08`–`09` operating pillar (how we build, agent factory); plus `CEO_SYSTEM_CONTEXT.md` and `PLATFORM_ANATOMY_CURRENT_STATE.md`. |
| `PM/` | Program material — Admin console, Sales Portal docs, eCat web rewrite estimates, agent starters. |

### Client onboarding
| Path | Purpose |
|---|---|
| `eCat_Onboarding/` | Per-client workspaces (`drf`, `leg`, `libco`, `mali`, `pebl`, …) plus `_Template/` and `00_KICKOFF_PROMPT.md`. |
| `onboarding-models/` | Phase framework, output contracts, HTML artifact contract, questionnaire, rendering pipeline. |
| `kb-articles/`, `KB - Net New/`, `documentation/` | Knowledge-base source and drafts. |

### Analysis & reporting
| Path | Purpose |
|---|---|
| `Insightful Product 4.0/` | **Active** Insightful work — pipeline, `CANON.md`, knowledge, handoffs. |
| `reports/` | Generated client reports (EBR, closed deals, feature analysis) in `.md` + `.html`. |
| `Customer Intelligence/`, `Customer Segmentation/`, `Peer Benchmark/` | Segmentation and benchmarking analysis. |
| `Health V2/`, `Health V3/`, `Health V3 Backfill/`, `Migration-Health Artifacts/` | Account-health scoring generations. |
| `Pricing Migration/`, `Pricing Migration V2/` | Pricing migration program. |
| `EBR 2.0/`, `HPMKT 2.0/`, `HPMKT 2026/` | Business-review and High Point Market material. |
| `ttfv/`, `Data Scoping/`, `Scoping Build/`, `validation-reports/` | Time-to-first-value, scoping, and validation datasets. |
| `scripts/`, `bigquery/` | Analysis scripts and BigQuery service-account config. |

### Presentation
| Path | Purpose |
|---|---|
| `design-system/`, `HTML System/` | Shared design system, templates, data contracts for HTML deliverables. |

### Housekeeping
| Path | Purpose |
|---|---|
| `_archive/`, `chat-history/`, `AGENT_CHAT_INDEX.md` | Archived material and agent transcript index. |
| `scratch/`, `files 2/` | Scratch space — not authoritative. |
| `cursor-to-claude-migration/`, `cursor-to-claude-migration-macbook/` | Tooling migration notes. |

---

## Active vs frozen

**Frozen — do not read, grep, cite, or run without an explicit per-conversation request:**

| Folder | Location |
|---|---|
| `Insightful Product` (original) | `iCloud Drive/Insightful Product/` — sibling to this repo |
| `Insightful Product 2.0/` | in-repo |
| `Insightful Product 3.0/` | in-repo |

The freeze is enforced by `.cursorignore` and `.cursor/rules/insightful-legacy-frozen.mdc`.

- **Active Insightful work is `Insightful Product 4.0/`.** A bare "run a report
  for X" means the 4.0 report (`insightful-report-4`), never 2.0.
- The `insightful-report` skill targets frozen 2.0 — only invoke it when the
  user explicitly says "2.0" or "legacy".
- If it is ambiguous whether a request means 4.0 or a legacy version, ask once
  before touching a frozen path.

Also treat as low-trust rather than frozen: `_archive/`, `scratch/`, `files 2/`,
and any `* 2.md` / `* 2.py` duplicate — these are copies, not sources of truth.

---

## File conventions

**Output format**
- Results go in **chat** as markdown — tables, bullets, fenced code.
- Saved deliverables are normal repo files (`.md`, `.csv`, `.html`).

**Naming**
- Dated artifacts: `YYYY-MM-DD` prefix or suffix (`2026-07-16__name.md`).
- Client work is keyed by **org shortname** (`mali`, `libco`, `drf`, `pebl`, `leg`).
- Reports commonly ship as a `.md` + `.html` pair with the same stem.
- Docs carry a `> **Last updated**: YYYY-MM-DD` line near the top — **bump it when
  you change the file.** Several `foundation/` docs currently have edits that
  were made without bumping the stamp; do not add to that.

**Never commit**
- Client data (`customers.csv`, `Ready_For_Import/*.csv`)
- Secrets — `.env`, `bigquery/service-account/`, `*service-account*.json`
- Transcript archives (`*transcript*.zip`)

**Skills live in two places.** `.cursor/skills/` (in-repo, tracked) and
`~/.claude/skills/` (home, untracked) hold independent copies of the same 22
skills. They are not symlinks. As of 2026-08-11 all 22 `SKILL.md` files are
byte-identical — **when you edit a skill, update both copies** or they drift.

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

22 skills, identical in `.cursor/skills/` and `~/.claude/skills/`.

### Onboarding orchestration
| Skill | Use it for |
|---|---|
| `ecat-onboarding-orchestrator` | Drive an onboarding end to end — read client state, determine phase, route to the right skill, enforce the phase gate. **Start here** when unsure which skill applies. |
| `ecat-session-handoff` | End-of-session handoff so the next chat starts with full context. |
| `ecat-support-triage` | One-off ticket or client email — diagnose, route, ground in live state, draft a reply. Use instead of the orchestrator for ad-hoc issues. |

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

### Engineering (targets `~/supercat-code`)
| Skill | Use it for |
|---|---|
| `admin-page-migration` | Legacy Bootstrap/jQuery → Tailwind/Stimulus/ViewComponent admin pages. |
| `migration-audit` | Admin v2 migration coverage — which controller actions render in v2 layouts. |
| `rails-code-review` | Rails PR/branch review. |

Harness-provided skills (`dataviz`, `artifact-design`, `code-review`, `loop`,
`schedule`, `claude-api`, …) are not installed here and are not listed above.
