# PROJECT SPINE — Admin Console · eCat Feature Usage Report

**Opened:** 2026-07-24  
**Phase status:** **Phase 4 Final PASS** — [`BETTING-BRIEF.md`](BETTING-BRIEF.md) · ready for betting table · Isolation still ON  

**Isolation:** **ON** until Kylor writes verbatim `ISOLATION OFF — GO on Admin Feature Usage`  
**Jira:** READ-ONLY (no comments / creates / transitions)

---

## One-liner

Org-scoped **eCat Feature Usage / adoption** dashboard in **Admin Console** for **SuperCat administrators** — Mixpanel → BigQuery → nightly Postgres → Chart.js — so CS/GTM can run customer-success conversations, spot at-risk orgs (“No Portal Usage”), and demo product value.

## Problem

Mixpanel usage data lives in `supercat-data-pipeline.mixpanel` (~10M events, 4,400+ users, 170 orgs, Nov 2024–present) and is **not surfaced** anywhere SuperCat admins work. Adoption is already a GTM metric (EBR “No Portal Usage” / F7) with no operational UI.

## Audience (locked)

| In | Out |
|---|---|
| SuperCat administrators / CS / GTM | Client org-admins in Sales Portal |
| Ops using Admin Console on an org | Manufacturer reps / Owner portal seats |

## Product home (locked)

**Admin Console only** — org-scoped route pattern `/:org_shortname/analytics_dashboard` (CTO AC-1 / ST-3).  
**Not** Sales Portal nav. **Not** Bet E Settings hub. **Not** Bet F. **Not** client self-serve.

## Exemplar

Courchesne Feature Usage Report UI (lovable reference + screenshots 2026-07-24): KPI row · category bar · % breakdown · logins-by-user · activity leaderboard · quarter date range · user drill-down.

## Data path (CTO, finalized 2026-07-15)

```
Mixpanel → BQ dataset supercat-data-pipeline.mixpanel
        → MVs: mv_org_daily_kpis · mv_user_daily_activity · mv_user_device_info
        → nightly Analytics::BigQuerySync → Postgres analytics_* tables
        → AnalyticsDashboardController (admin_v2) + Chart.js + Stimulus + Turbo Frames
```

Org resolution in MVs: coalesce to **`organization_shortname`** (no `event.org` column in live BQ — see Phase 2 plan CF-2); unmapped NULL orgs excluded.

## Locked definitions

| Term | Lock |
|---|---|
| Login | Distinct calendar **active days** with ≥1 event — **not** raw session count |
| Active user | ≥1 login in selected date range |
| Engagement tier | High ≥50 actions/day avg · Medium 10–49 · Low &lt;10 |
| Taxonomy | Search/Find · Share · Serve · Sell · Scan · Save (+ excluded meta) via `config/analytics_taxonomy.yml` |
| Freshness | ≤24h stale (“Last synced” from `analytics_sync_logs`) |
| Default date range | Current quarter |

## Explicitly not this project

| Thing | Why |
|---|---|
| **Bet F** (persona IA) | Placement only — closed; home is this folder |
| **Bet E** Portal & Access Settings | Config plane, different job |
| **Sales Portal Intelligence** team strip | Commerce-tied behavior floor (Q-R1 / Q-18), not org adoption GTM |
| **Client self-serve** dashboard | CTO non-goal |
| Cross-org benchmarks · realtime · alerting · WoW/MoM trends | CTO non-goals / future |
| Admin Console “2.0” rebuild | Out of appetite |

Parallel de-conflict (footnote only): SERV-2421 / SERV-2336 (Mixpanel adoption) — not Lane 2 IR; this project owns the Admin Feature Usage surface.

## Phase machine

| Phase | Status | Deliverables |
|---|---|---|
| **1 Capture / shape** | **Done** | Spine · Pitch · AC · Taxonomy · Boundary |
| **2 Eng-ready plan** | **Done** | [`TECHNICAL-PLAN-feature-usage.md`](TECHNICAL-PLAN-feature-usage.md) (eng-handoff folded into §11) |
| **3 HTML (optional)** | **Done (3b PASS · 3c so-what)** | [`design-system/app/admin-feature-usage-demo.html`](../../design-system/app/admin-feature-usage-demo.html) · [`PHASE3-DEMO-RUNBOOK.md`](PHASE3-DEMO-RUNBOOK.md) — never edit Sales Portal Friday demos |
| **4 Betting / GO brief** | **Final PASS** | [`BETTING-BRIEF.md`](BETTING-BRIEF.md) |

## Eng wave map (summarize only — do not implement)

| Subtask | Scope |
|---|---|
| **ST-1** | BQ MVs + `analytics_taxonomy.yml` (no Rails UI) |
| **ST-2** | Gem, migrations, `Analytics::BigQuerySync`, CronTask / K8s CronJob |
| **ST-3** | `AnalyticsDashboardController` + routes + SuperCat-admin ACL |
| **ST-4** | admin_v2 views, Chart.js, Stimulus, Turbo Frames |

Order: ST-1 → ST-2 → ST-3 → ST-4 (ST-4 Stimulus can start parallel with ST-3).

## Pattern references (read-only Rails — cite only)

- `supercat_server/app/controllers/rep_activities_controller.rb` — AdminController + UiSwitchable + date params  
- `supercat_server/app/services/rep_activities/build_dashboard_stats.rb` — service → Struct  
- `supercat_server/app/views/rep_activities/dashboard_v2.html.erb` — admin_v2 layout  
- `supercat_server/app/models/cron_task.rb` — CronTask entry  
- Org-scoped routes under `:org_shortname`

## Pack index

| File | Role |
|---|---|
| [`README.md`](README.md) | Folder entry |
| [`00-ORCHESTRATOR.md`](00-ORCHESTRATOR.md) | Review Cards / phase routing |
| [`01-PHASE1-WORKER.md`](01-PHASE1-WORKER.md) | Phase 1 worker starter (done) |
| [`02-PHASE2-WORKER.md`](02-PHASE2-WORKER.md) | Phase 2 worker starter (done) |
| [`03-PHASE3-WORKER.md`](03-PHASE3-WORKER.md) | Phase 3 HTML worker (superseded by 3b) |
| [`03b-PHASE3-REWRITE-WORKER.md`](03b-PHASE3-REWRITE-WORKER.md) | Phase 3b elite rewrite worker |
| [`03c-PHASE3-SOWHAT-WORKER.md`](03c-PHASE3-SOWHAT-WORKER.md) | Phase 3c thin so-what layer worker |
| [`00-PROJECT-SPINE.md`](00-PROJECT-SPINE.md) | This router |
| [`PITCH-feature-usage.md`](PITCH-feature-usage.md) | Shape Up pitch |
| [`AC-feature-usage-v0.md`](AC-feature-usage-v0.md) | AC-1…AC-9 |
| [`TAXONOMY-events.md`](TAXONOMY-events.md) | Category → events SoT |
| [`BOUNDARY-vs-portal-bet-e-bet-f.md`](BOUNDARY-vs-portal-bet-e-bet-f.md) | Placement boundaries |
| [`TECHNICAL-PLAN-feature-usage.md`](TECHNICAL-PLAN-feature-usage.md) | Phase 2 eng-ready plan |
| [`PHASE3-DEMO-RUNBOOK.md`](PHASE3-DEMO-RUNBOOK.md) | Phase 3 HTML open/walk + AC map |
| [`BETTING-BRIEF.md`](BETTING-BRIEF.md) | Phase 4 ready-for-table / GO brief |
| Demo HTML | `design-system/app/admin-feature-usage-demo.html` (net-new) |

## Isolation reminder

Write under `PM/Admin-console/` only until GO. No `supercat-code/` edits, no BQ apply, no Friday-demo HTML edits, no Jira writes.

---

*Spine for Admin Feature Usage only. Phase 4 Final PASS — Isolation ON until GO phrase.*
