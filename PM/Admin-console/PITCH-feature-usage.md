# PITCH — Admin Console · eCat Feature Usage Report

**Shape Up pitch** · Phase 1 · 2026-07-24  
**Home:** Admin Console · SuperCat administrators only  
**Does not unlock** `ISOLATION OFF — GO on Admin Feature Usage`

---

## Problem

We already collect deep eCat rep usage in Mixpanel (synced to BigQuery: ~10M events across ~170 orgs). That signal powers GTM risk language (“No Portal Usage” in EBR decks) but **nobody can open an org and see engagement** — logins, who is active, which feature categories fire, who is cold.

CS and GTM need a **per-org adoption view** for success calls, at-risk triage, and value demos. Without it, adoption stays a slide metric, not an operational tool.

## Appetite

**Small-to-batch cycle** shaped around CTO’s already-finalized architecture (2026-07-15): three BigQuery MVs → nightly Postgres analytics cache → one Admin Console dashboard (Chart.js + Stimulus), not a new warehouse product.

Enough time to ship **one org-scoped report** with KPIs, category charts, logins-by-user, leaderboard, and user drill-down — not a suite of analytics products.

## Solution elements

1. **Org-scoped Admin dashboard** (`/:org_shortname/analytics_dashboard`) — SuperCat-admin only; follows `RepActivitiesController` / admin_v2 patterns.
2. **KPI strip (date-range filtered, default = current quarter)** — total logins (active days), active users, search actions, orders submitted, items scanned.
3. **Feature usage by category** — bar chart over Search/Find · Share · Serve · Sell · Scan · Save (YAML taxonomy).
4. **Category breakdown** — % distribution of categorized actions.
5. **Logins by user** — bar chart of active-day logins per rep.
6. **User activity leaderboard** — rank, name, logins, total actions, last active, engagement tier; sortable; ranked by feature interactions (excluding login-day counting as an “action”).
7. **User drill-down** — per-feature counts, device model, app version, last active.
8. **Freshness** — BQ MV refresh + nightly sync; UI shows “Last synced”; AC ≤24h stale.
9. **Configurable taxonomy** — `config/analytics_taxonomy.yml` drives BQ view generation and Rails services (no hardcoded per-category SQL).

**Data spine (locked):** Mixpanel → `supercat-data-pipeline.mixpanel` → `mv_org_daily_kpis` / `mv_user_daily_activity` / `mv_user_device_info` → `analytics_org_daily_summaries` / `analytics_user_daily_summaries` / `analytics_user_profiles` / `analytics_sync_logs` → Chart.js UI.

**Exemplar:** Courchesne Feature Usage Report (screenshots / lovable) — visual target, not a second product.

## Rabbit holes (call out / patch)

| Risk | Patch |
|---|---|
| Confusing **login** with Mixpanel session count | Lock: login = distinct calendar active days with ≥1 event |
| Building inside **Sales Portal** “for the demo” | Home = Admin Console; optional Phase 3 HTML is a **net-new** illustration file, never Friday demos / never portal nav |
| Reusing empty `*_feature_usage_report` BQ tables | Schema-only / no date dimension — **ignore for v0**; MVs are SoT |
| Org NULL on events | Resolve in MV via `COALESCE(event.org, user_org_mapping)`; drop still-NULL |
| Hardcoding event lists in SQL | YAML taxonomy shared by BQ generator + Rails |
| Scope creep into benchmarks / alerts / WoW / client self-serve | Explicit no-gos below |
| Merging with Bet E Settings or Bet F IA | Boundary one-pager; this folder is the only build home |
| Parallel SERV-2421/2336 confusion | De-conflict footnote; this project owns the Admin surface |

## No-gos

- Sales Portal nav item or Intelligence-strip replacement  
- Bet E Settings hub work  
- Bet F rewrite / persona IA scope  
- Customer-facing / client self-serve dashboard  
- Cross-org benchmarking  
- Realtime / streaming  
- Alerting on engagement drops  
- WoW / MoM trend lines (future phase)  
- Admin Console rebuild / toggle re-triage  
- Inventing metrics outside Mixpanel event taxonomy  
- Rails / BQ apply before isolation GO  

## Done looks like

A SuperCat admin opens any org’s Feature Usage dashboard, picks a date range (default current quarter), sees KPIs + category charts + logins-by-user + sortable leaderboard, drills into a user, and trusts data ≤24h old — without leaving Admin Console.

## Eng wave (for betting table later — not Phase 1 build)

ST-1 BQ MVs + YAML → ST-2 sync pipeline → ST-3 controller/ACL → ST-4 Chart.js UI.

---

*Pitch SoT for Phase 1. Companion: `AC-feature-usage-v0.md`, `TAXONOMY-events.md`.*
