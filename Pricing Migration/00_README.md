# SuperCat 2026 Pricing Migration — Communications System

> **STUB — to be finalized in Stage 2.8** after all `_root/` docs are authored.
>
> **Last updated**: 2026-05-22 (scaffolding only)
> **Owner**: CEO

---

## What this folder is

The single source of truth for the 2026 pricing migration communications system. Templates, prompts, root rules, source data, and per-account drafts all live here. The folder is designed so a fresh agent in a fresh session can produce a correct draft for any account by reading `_root/` and following the format-specific template — without consulting any external file, prior chat, or archived artifact.

## How to navigate

1. **Always start at**: `_root/00_manifest.md` (the required-reading entry point)
2. **Active templates and agent prompts**: `format-a-notices/`, `format-b-notices/`, `ceo-letter-notices/`, `good-news-notices/`
3. **Read-only source data**: `_master-account-data-v6.2.csv` (authoritative), `migration_comm_tiers_2026-05-19.csv` (routing), `_reference/` (execution plan v3.3 + HTML revenue model)
4. **Never read**: `_archive/` — superseded artifacts; see `_archive/2026-05-22__pre-refactor/DO_NOT_READ.md`

## Folder structure (post Stage 1.1)

```
Pricing Migration/
├── 00_README.md                                (this file)
├── AGENTS.md                                   (agent orientation)
├── _master-account-data-v6.2.csv               (authoritative account data)
├── migration_comm_tiers_2026-05-19.csv         (routing data)
├── _root/                                      (authoritative rules — read first)
│   ├── 00_manifest.md
│   ├── CONTRACTS.md
│   ├── 01_why_we_are_migrating.md
│   ├── 02_who_is_being_migrated.md
│   ├── 03_what_we_sell.md
│   ├── 04_communication_posture.md
│   ├── 05_driver_taxonomy.md
│   ├── 06_format_routing.md
│   ├── 07_data_pipeline.md
│   ├── 08_quality_bar.md
│   └── 09_changelog.md
├── _reference/                                 (read-only source data)
│   ├── 2026-05-20__execution_plan_v3.3.md
│   └── migration_revenue_model_2026-05-14.html
├── _meta/                                      (system-authoring artifacts; read only when directed)
│   └── stage2_prompts/                         (fresh-agent prompts for root-doc authoring)
├── format-a-notices/                           (active templates — populated Stage 3)
├── format-b-notices/                           (active templates — populated Stage 3)
├── ceo-letter-notices/                         (active templates — populated Stage 3)
├── good-news-notices/                          (active templates — populated Stage 3)
└── _archive/2026-05-22__pre-refactor/          (DO NOT READ — see DO_NOT_READ.md inside)
```

## Reading paths by role

[STUB — to be finalized in Stage 2.8 once root docs exist.]

## Current state

**Stage 1.1 (folder reorganization) complete as of 2026-05-22.** Next: Stage 2 — root doc authoring. See `_root/09_changelog.md` for the rolling log.
