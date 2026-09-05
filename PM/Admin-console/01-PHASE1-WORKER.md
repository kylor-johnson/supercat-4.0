# WORKER — Phase 1 · Capture / shape · Admin Feature Usage Report

You are a **Program / shaping agent** for **Admin Console — eCat Feature Usage Report** only.  
Write the Phase 1 shape pack under `PM/Admin-console/`. You do **not** implement Rails, touch Sales Portal demos, or open a Bet F rewrite.

## Isolation (hard)

- **Write only** under `SuperCat 4.0/PM/Admin-console/`
- **Never** edit `supercat-code/` / `supercat_server`
- **Never** modify Sales Portal Friday demos:
  - `design-system/app/sales-portal-bet-a-pitch-demo.html`
  - `design-system/app/sales-portal-internal-demo.html`
  - `design-system/app/sales-portal-persona-ia-demo.html`
- Jira = **READ-ONLY** (no comments/creates/transitions)
- Does **not** unlock `ISOLATION OFF — GO on Admin Feature Usage`
- No HTML this phase (Phase 3 optional later)

## Project locks (do not re-litigate)

| Lock | Value |
|---|---|
| Home | **Admin Console** |
| Audience | **SuperCat administrators only** |
| Not | Sales Portal nav · Bet E Settings · Bet F · client self-serve |
| Job | Per-org engagement / feature usage for CS + GTM (“No Portal Usage”, at-risk orgs, value demos) |
| Exemplar | Courchesne Feature Usage Report UI (screenshots / lovable reference) |
| Data path (CTO, 2026-07-15) | Mixpanel → BQ dataset `supercat-data-pipeline.mixpanel` → 3 materialized views → nightly Postgres analytics_* tables → Chart.js + Stimulus admin_v2 |
| Login | Distinct calendar **active days** with ≥1 event — not raw session count |
| Engagement tiers | High ≥50 actions/day avg · Medium 10–49 · Low &lt;10 |
| Taxonomy categories | Search/Find · Share · Serve · Sell · Scan · Save (+ excluded meta events list) |
| Freshness | ≤24h stale |
| Non-goals | Cross-org benchmarks · realtime · alerting · customer-facing self-serve · WoW/MoM trend lines (future) |

## CTO / architecture authority (encode; do not invent)

Kylor’s capture (and any screenshots he attaches) is the product AC source. Encode these decisions:

**Desired end state — dashboard must show (date-range filtered, default = current quarter):**
1. Summary KPIs — total logins (active days), active users, search actions, orders submitted, items scanned  
2. Feature usage by category — bar chart  
3. Category breakdown — % distribution  
4. Logins by user — bar chart  
5. User activity leaderboard — rank, name, logins, total actions, last active, engagement tier (sortable)  
6. Individual user drill-down — per-feature counts, device model, app version, last active  

**Architecture (finalized unless you find a blocking contradiction with evidence):**
- BQ MVs: `mv_org_daily_kpis`, `mv_user_daily_activity`, `mv_user_device_info`  
- Org resolution in MV via `COALESCE(event.org, user_org_mapping)`  
- Postgres cache tables: `analytics_org_daily_summaries`, `analytics_user_daily_summaries`, `analytics_user_profiles`, `analytics_sync_logs`  
- Sync via CronTask + google-cloud-bigquery gem  
- Frontend: AdminController pattern (`RepActivitiesController` / admin_v2), Chart.js + Stimulus + Turbo Frames  
- Taxonomy: `config/analytics_taxonomy.yml` (configurable)  

**AC-1…AC-9** (from CTO handoff) must appear as Given/When/Then or equivalent crisp AC rows in `AC-feature-usage-v0.md`.

**Subtasks ST-1…ST-4** may be summarized as an eng wave map — do not start implementing them.

## Mandatory reads

1. `PM/Admin-console/README.md`  
2. `PM/Admin-console/00-ORCHESTRATOR.md` (phase machine + locks)  
3. `PM/sales-portal-agent-starters/cycle-03-outputs/SURFACE-PLACEMENT.md` (B2 + CLOSE note)  
4. `PM/sales-portal-agent-starters/00-PROGRAM-SPINE.md` — isolation; F7; SERV-2421/2336  
5. `PM/sales-portal-agent-starters/00a-DOCTRINE-shapeup-ddd-affinity.md` — Shape Up pitch rules (skim)  
6. Any CTO paste / screenshots Kylor provides in this chat  

Optional read-only Rails (cite paths only, no edits): search for `RepActivitiesController`, `admin_v2`, existing analytics routes — only to name pattern references in the pitch/spine.

## Deliverables (create under `PM/Admin-console/`)

### 1. `00-PROJECT-SPINE.md`
Router for this project: problem, audience, data path, phase status, isolation, links to pack files, explicit “not Bet F / not Bet E / not Sales Portal.”

### 2. `PITCH-feature-usage.md`
Shape Up pitch: problem · appetite · solution elements · rabbit holes · no-gos.

### 3. `AC-feature-usage-v0.md`
AC-1…AC-9 as testable criteria; KPI definitions; login/active-user/engagement-tier definitions; SuperCat-admin-only access; freshness ≤24h; taxonomy configurable.

### 4. `TAXONOMY-events.md`
Category → event list + excluded meta events (from CTO). Note: implementation encodes via YAML later — this file is the product SoT for Phase 1.

### 5. `BOUNDARY-vs-portal-bet-e-bet-f.md`
One-pager:
- vs Sales Portal Intelligence team strip  
- vs Bet E Settings hub  
- vs Bet F persona IA (placement only; project home is this folder)  
- vs future client self-serve (non-goal)

## Do not

- Build Rails / BQ views / Chart.js  
- Create HTML demos this phase  
- Rewrite Bet A/F packs  
- Post to Jira  
- Expand into Admin Console “2.0” rebuild  

## Done criteria

All five files on disk, internally consistent with CTO locks, isolation honored, clear “ready for Orchestrator Review Card — Phase 1.”

## When finished

Reply with: paths written · 5-bullet summary ·  
`Ready for Orchestrator Review Card — Phase 1` · stop (do not start Phase 2).
