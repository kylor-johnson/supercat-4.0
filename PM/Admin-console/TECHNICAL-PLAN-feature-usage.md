# TECHNICAL PLAN — Admin Console · eCat Feature Usage Report

**Phase 2** · 2026-07-24  
**Isolation:** ON — this plan does **not** authorize Rails apply, BQ CREATE/ALTER, CronTask deploy, or PRs  
**Unlock required:** `ISOLATION OFF — GO on Admin Feature Usage`  
**Phase 1 SoT:** spine · pitch · AC · taxonomy · boundary (locked — do not re-litigate product)

---

## 0. Carry-forwards (Orchestrator Phase 1)

| # | Resolution in this plan |
|---|---|
| **CF-1** | Surfaces #3 (category %) and #4 (logins-by-user) get explicit eng ACs **AC-3a** / **AC-4a** (§6) so they cannot be dropped under AC-3/AC-4 alone |
| **CF-2** | Live BQ schema has **no** `org` column. Canonical name locked: **`organization_shortname`**. Spine/pitch `event.org` was informal shorthand — superseded here with evidence (§1.1) |
| **CF-3** | No raw CTO paste/screenshots in this Phase 2 chat. Plan uses `TAXONOMY-events.md`. Spot-check: all listed taxonomy events exist in `mixpanel.events` with non-zero counts (read-only). **Flag: taxonomy unverified vs raw CTO paste** |

---

## 1. Architecture / data flow

```
Mixpanel (eCat app)
    │  Weld sync (existing)
    ▼
BigQuery  supercat-data-pipeline.mixpanel
    │  events · people · user_org_mapping
    │  (+ ignore schema-only org/user_feature_usage_report tables)
    ▼
ST-1  Materialized views (YAML-driven CASE/IN lists)
    │  mv_org_daily_kpis
    │  mv_user_daily_activity
    │  mv_user_device_info
    ▼
ST-2  Analytics::BigQuerySync  (nightly CronTask / K8s CronJob)
    │  → Postgres analytics_* + analytics_sync_logs
    ▼
ST-3  AnalyticsDashboardController < AdminController
    │  routes /:org_shortname/analytics_dashboard(+ /users/:id)
    │  SuperCat-admin ACL (AC-1, AC-9)
    ▼
ST-4  admin_v2 ERB · Chart.js · Stimulus · Turbo Frames
         KPIs · category bar · % pie/donut · logins-by-user · leaderboard · drill-down
```

**Read-only pattern cites (do not edit until GO):**

| Pattern | Path |
|---|---|
| Admin controller + date params + admin_v2 | `supercat_server/app/controllers/rep_activities_controller.rb` |
| Service → Struct for dashboard | `supercat_server/app/services/rep_activities/build_dashboard_stats.rb` |
| admin_v2 layout + InsightCard / DataTable | `supercat_server/app/views/rep_activities/dashboard_v2.html.erb` |
| Cron entrypoint style | `supercat_server/app/models/cron_task.rb` |
| Org-scoped admin routes | `config/routes.rb` `scope '/:org_shortname'` → e.g. `rep_activities#dashboard` |
| ACL primitives | `AdminController#authenticate` / `#enforce_permissions` · `UserTypePermissions.verify_web_request` |
| Stimulus / Turbo already in app | `config/importmap.rb` (Stimulus + Turbo pinned; **Chart.js not yet pinned** — add in ST-4) |
| BQ gem | **Not present** in `Gemfile` today — add in ST-2 |

### 1.1 Org field naming lock (CF-2) — evidence

Read-only `INFORMATION_SCHEMA` + counts on `mixpanel.events` (2026-07-24):

| Column | Present? | Non-null ≈ |
|---|---|---|
| `org` | **No** | — |
| `organization_shortname` | Yes | ~462k / 10.4M (sparse) |
| `current_organization_shortname` | Yes | ~9.96M / 10.4M (dense) |
| `user_org_mapping.organization_shortname` | Yes | join on `username` |

**Plan lock for MVs / Postgres / Rails:**

- Canonical org key name everywhere after materialization: **`organization_shortname`**
- Recommended event-time resolve (evidence-backed; confirm with CTO before GO):

```sql
COALESCE(
  NULLIF(e.organization_shortname, ''),
  NULLIF(e.current_organization_shortname, ''),
  NULLIF(u.organization_shortname, '')
) AS organization_shortname
```

- Rows still NULL after COALESCE → **exclude** (~914 events in a full-table check — noise)
- Rails sync/filter keys on `organization_shortname` matching `Organization#shortname` for the Admin route

**Open Q-ORG:** AC/taxonomy text only names `organization_shortname` + mapping. Including `current_organization_shortname` is required for usable coverage given sparsity of the former. Treat as CTO confirm-at-betting, default = include (recommended).

---

## 2. ST-1 … ST-4 work packages

Order: **ST-1 → ST-2 → ST-3 → ST-4** (Stimulus shell / Chart.js pin may start parallel with ST-3).

### ST-1 — BQ MVs + taxonomy YAML · sizing **M**

| | |
|---|---|
| **Inputs** | `TAXONOMY-events.md` → `config/analytics_taxonomy.yml`; Mixpanel tables above; CF-2 org COALESCE |
| **Outputs** | `config/analytics_taxonomy.yml`; generator script/docs that emit MV SQL from YAML; three MVs in `supercat-data-pipeline.mixpanel` (names locked) |
| **Owner-shaped slices** | (a) YAML authoring from taxonomy SoT (b) SQL generator (c) MV create + 24h refresh schedule (ops) (d) smoke query vs one exemplar org |
| **Deps** | None (blocks ST-2) |
| **Do not** | Use `org_feature_usage_report` / `user_feature_usage_report` (schema-only, no date dim) |

### ST-2 — Gem, migrations, sync, cron · sizing **M**

| | |
|---|---|
| **Inputs** | MVs live; BQ credentials / workload identity (ops) |
| **Outputs** | `google-cloud-bigquery` gem; Postgres `analytics_*` tables + indexes; `Analytics::BigQuerySync`; `CronTask.run_analytics_bigquery_sync` (name flexible) + K8s CronJob nightly; writes to `analytics_sync_logs` |
| **Owner-shaped slices** | (a) gem + client wrapper (b) migrations (c) sync service upsert/replace strategy (d) cron + failure logging (e) dry-run against staging |
| **Deps** | ST-1 |
| **Freshness** | Nightly sync + MV ≤24h refresh → AC-7 |

### ST-3 — Controller, routes, ACL · sizing **S**

| | |
|---|---|
| **Inputs** | Postgres cache populated; AdminController patterns |
| **Outputs** | `AnalyticsDashboardController < AdminController`; routes under `/:org_shortname`; services wired for show/user; **SuperCat-admin-only** gate (AC-9) |
| **Owner-shaped slices** | (a) routes (b) controller actions + before_actions (c) ACL tests (d) org scope via `@current_org` |
| **Deps** | ST-2 schema (can stub services with fixtures for controller tests) |
| **ACL note** | Default `enforce_permissions` allows **OrgUser** admins for permitted controllers. AC-9 requires **SuperCat platform admins only** (`User#is_admin?`), not client org-admins. Add an explicit `before_action` (e.g. `require_supercat_admin`) that denies OrgUser-only sessions — do not rely on `UserTypePermissions` alone. Exact helper name = eng choice; behavior locked. |

### ST-4 — admin_v2 UI · sizing **L**

| | |
|---|---|
| **Inputs** | Controller + services; Courchesne exemplar visuals |
| **Outputs** | Views under admin_v2; Chart.js pin + Stimulus controllers; Turbo Frames for date-range reload; leaderboard sort; user drill-down |
| **Owner-shaped slices** | (a) page shell + KPI strip (b) category bar + % chart (c) logins-by-user chart (d) leaderboard + sort (e) user detail (f) Last synced badge |
| **Deps** | ST-3 for routes/ACL; can parallel Stimulus/Chart scaffolding with ST-3 |
| **UI kit cite** | Prefer existing `Sc::PageHeaderComponent`, `Sc::FilterBarComponent`, `Sc::InsightCardComponent`, `Sc::DataTableComponent` as in `dashboard_v2` |

---

## 3. Schema sketch (betting-grade, not a migration)

### 3.1 MV column intents

**`mv_org_daily_kpis`** — grain: `(organization_shortname, activity_date)`

| Column intent | Notes |
|---|---|
| `organization_shortname` | Resolved org (CF-2) |
| `activity_date` | Calendar date (UTC or product-locked TZ — see Q-TZ) |
| `login_count` | Distinct users with ≥1 event that day (= org active-day contribution units; see KPI def: org total logins = sum of user active days) |
| `active_users` | Distinct usernames with ≥1 event that day |
| `search_actions` | Count Search/Find taxonomy events |
| `orders_submitted` | Count `order_submitted` |
| `items_scanned` | Count `item_scanned` |
| `cat_search_find` … `cat_save` | Per-category event counts (6 ints) |
| `total_categorized_actions` | Sum of categorized (excludes meta) |

*Implementation detail:* org-level `login_count` for the KPI “total logins” must equal **sum of user-level active days** in range (AC defs). Prefer deriving org KPI from `mv_user_daily_activity` in Rails, **or** define MV `login_count` as that sum-equivalent (distinct user-days). Eng must not use Mixpanel session counts.

**`mv_user_daily_activity`** — grain: `(organization_shortname, username, activity_date)`

| Column intent | Notes |
|---|---|
| `organization_shortname`, `username`, `activity_date` | Keys |
| `is_active_day` | Always true for a row (presence = login day) |
| `total_actions` | Categorized feature events that day (**not** counting the login-day itself as an action) |
| `cat_*` (6) | Per-category counts |
| `orders_submitted`, `items_scanned`, `search_actions` | Optional denorm for drill-down speed |
| `event_counts_json` *(optional)* | Per-event-name map for AC-6 feature list — or join raw; prefer pre-agg in MV or a 4th slim structure if needed |

**`mv_user_device_info`** — grain: `(username)` or `(organization_shortname, username)`

| Column intent | Source hint |
|---|---|
| `username` / `distinct_id` | Join key |
| `device_model` | `people.ios_device_model` and/or latest `events.model` / `mp_device_model` |
| `app_version` | `people.ios_app_version` / `events.app_version_string` |
| `last_seen_at` | `people.last_seen` |

### 3.2 Postgres `analytics_*` (mirror MV grains)

| Table | Role |
|---|---|
| `analytics_org_daily_summaries` | Cache of `mv_org_daily_kpis` |
| `analytics_user_daily_summaries` | Cache of `mv_user_daily_activity` |
| `analytics_user_profiles` | Cache of `mv_user_device_info` (+ display name if available) |
| `analytics_sync_logs` | `started_at`, `finished_at`, `status`, `rows_*`, `error_message`, `source` |

Indexes (intent): `(organization_shortname, activity_date)`; `(organization_shortname, username, activity_date)`; unique sync log id.

**Sync strategy (recommendation):** nightly full replace for trailing N months / all history from MVs (dataset is ~10M events but MVs are daily grains — small). Idempotent truncate-or-upsert by natural key. Record success/failure in `analytics_sync_logs`.

---

## 4. YAML taxonomy contract (AC-8)

Product SoT: [`TAXONOMY-events.md`](TAXONOMY-events.md)  
Rails/BQ artifact: `config/analytics_taxonomy.yml`

### Shape

```yaml
categories:
  search_find:
    label: "Search / Find"
    events:
      - product_search
      - filter_button_pressed
      # ...
  share:
    label: "Share"
    events: [...]
  serve:
    label: "Serve"
    events: [...]
  sell:
    label: "Sell"
    events: [...]
  scan:
    label: "Scan"
    events: [...]
  save:
    label: "Save"
    events: [...]
excluded:
  - selected_org
  - api_access
  # ... full list from TAXONOMY-events.md
kpi_callouts:
  search_actions: search_find          # whole category
  orders_submitted: order_submitted    # single event
  items_scanned: item_scanned
```

### Regen steps (ops/eng)

1. Update `TAXONOMY-events.md` (product) then YAML  
2. Run generator → emit MV SQL (`CASE event_name WHEN …` / `IN (...)`)  
3. `CREATE OR REPLACE` MVs (or drop/create) in BQ — **only after GO**  
4. Trigger sync (or wait nightly) so Postgres mirrors new categories  
5. Rails loads YAML at boot/request for labels + drill-down feature lists — **no hardcoded per-category SQL in app queries**

Unlisted events are **not** auto-bucketed (taxonomy rule).

---

## 5. Rails surface map

### Routes (under existing `scope '/:org_shortname'`)

| Method | Path | Action | AC |
|---|---|---|---|
| GET | `/:org_shortname/analytics_dashboard` | `show` | AC-1, AC-2…AC-5, AC-7, AC-9 |
| GET | `/:org_shortname/analytics_dashboard/users/:username` | `user` (or `show_user`) | AC-6 |

Query params: `from_date`, `to_date` (default = current quarter, mirror `RepActivitiesController` date parsing style).

Named helpers (suggested): `analytics_dashboard_path(org)`, `analytics_dashboard_user_path(org, username)`.

### Controller

`AnalyticsDashboardController < AdminController`

```
layout admin_v2 (via UiSwitchable / explicit render like RepActivities)
before_action :require_https
before_action :authenticate
before_action :enforce_permissions
before_action :require_supercat_admin   # AC-9 — platform User#is_admin? only
# set @date_from / @date_to (default current quarter)
```

### Services

| Service | Responsibility | Feeds |
|---|---|---|
| `Analytics::BigQuerySync` | Pull MVs → Postgres; write sync logs | ST-2 / AC-7 |
| `Analytics::BuildDashboard` | KPIs, category series, %, logins-by-user, leaderboard | `show` |
| `Analytics::BuildUserDetail` | Per-feature counts, device, app version, last active | `user` |
| `Analytics::Taxonomy` *(thin)* | Load YAML; category labels; excluded set | both builders |

Suggested `BuildDashboard` methods (align AC eng map + CF-1):

- `#build_kpis` → AC-2  
- `#build_category_breakdown` → AC-3 + AC-3a (% from same totals)  
- `#build_logins_by_user` → AC-4a  
- `#build_leaderboard` → AC-4  

### ACL checkpoints

| Check | Where | Pass criteria |
|---|---|---|
| Authenticated | `authenticate` | Session present |
| Web permission | `enforce_permissions` | Does not alone satisfy AC-9 |
| **SuperCat admin** | dedicated before_action | `@current_user.is_admin?` (User); deny client OrgUser admins |
| Org scope | `@current_org` from route | Queries filter `organization_shortname = @current_org.shortname` |

---

## 6. UI map (AC-2…AC-6 + CF-1)

| Surface | Eng AC | Chart.js / Stimulus / Turbo | Data |
|---|---|---|---|
| Summary KPI strip (5) | **AC-2** | ERB InsightCards (Chart optional) | `build_kpis` |
| Feature usage by category — **bar** | **AC-3** | Chart.js bar · Stimulus `analytics_charts_controller` | category counts |
| Category breakdown — **% distribution** | **AC-3a** *(new eng row)* | Chart.js doughnut/pie · same Stimulus | `count/sum*100` over categorized |
| Logins by user — **bar** | **AC-4a** *(new eng row)* | Chart.js horizontal/vertical bar | active days per username |
| User activity leaderboard | **AC-4** | HTML table + Stimulus sort (`analytics_leaderboard_controller`) | rank, name, logins, total actions, last active, tier |
| Date range picker | **AC-5** | `date_range_controller` + Turbo Frame wrapping KPI/charts/leaderboard | `from_date`/`to_date` |
| User drill-down | **AC-6** | Separate page or Turbo Frame slide-over | `BuildUserDetail` |
| Last synced | **AC-7** | Badge in page header | latest successful `analytics_sync_logs.finished_at` |

### Eng acceptance rows (CF-1 — cannot drop)

#### AC-3a — Category % breakdown

**Given** categorized actions in the selected range  
**When** the dashboard renders  
**Then** a % distribution visualization is shown for the six taxonomy categories  
**And** percentages sum to ~100% of categorized actions (excluded meta omitted)  
**And** this surface is present even if the category bar (AC-3) is also present  

#### AC-4a — Logins by user (bar chart)

**Given** users with ≥1 active day in the selected range  
**When** the dashboard renders  
**Then** a bar chart shows logins (active days) per user  
**And** this is distinct from the leaderboard table (AC-4)  

Engagement tiers (leaderboard): High ≥50 · Medium 10–49 · Low &lt;10 **avg actions/day over active days in range**.

---

## 7. Freshness / sync (AC-7)

| Layer | Cadence | Owner |
|---|---|---|
| Mixpanel → BQ `events` | Existing Weld (assume continuous/near-daily) | Data platform (out of this bet except dependency) |
| BQ MVs | Refresh ≤24h (schedule TBD with data eng — Q-MV) | ST-1 ops |
| Postgres sync | **Nightly** `CronTask` / K8s CronJob calling `Analytics::BigQuerySync` | ST-2 |
| UI | Show **Last synced** from latest `analytics_sync_logs` where `status = success` | ST-4 |

**Failure visibility:** failed sync rows in `analytics_sync_logs`; UI may show stale warning if last success &gt; 24h (AC-7). No paging/alerting product in v0 (non-goal) — ops can watch logs/CronJob.

---

## 8. Gap checklist / open questions (before GO)

| ID | Item | Needed from |
|---|---|---|
| **Q-ORG** | Confirm COALESCE includes `current_organization_shortname` (recommended yes — evidence) | CTO / Kylor |
| **Q-TZ** | Activity date timezone: UTC vs org-local vs America/Denver | CTO |
| **Q-MV** | MV refresh mechanism (BQ scheduled query vs continuous vs nightly CREATE) + who owns dataset IAM | Data eng / CTO |
| **Q-NAME** | Display name on leaderboard: Mixpanel username only vs join SuperCat `users`/`org_users` | Product |
| **Q-NAV** | Admin Console nav entry label/placement (not Sales Portal; not Bet E Settings hub) | Kylor |
| **Q-ACL** | Confirm platform `User#is_admin?` is the SuperCat-admin signal for AC-9 | Eng + Kylor |
| **Q-TAX** | Spot-check taxonomy against **raw CTO paste** when available — currently unverified vs paste (CF-3) | Kylor paste |
| **Q-HIST** | How much history to sync into Postgres (all MV history vs rolling 8 quarters) | Eng sizing |
| **Q-CRED** | BQ credentials path for Rails (Workload Identity / service account JSON — secrets store) | Ops |
| **Risk** | `organization_shortname` alone is too sparse — wrong COALESCE → empty dashboards | Mitigate via Q-ORG |
| **Risk** | Chart.js not in importmap yet | ST-4 pin from CDN like sortablejs |
| **Risk** | Client org-admin accidentally allowed if ACL only uses `enforce_permissions` | Explicit SuperCat gate |
| **Risk** | Confusing login with Mixpanel sessions | Locked definition in AC; enforce in MV SQL |

---

## 9. Isolation reminder

| Allowed now | Forbidden until GO phrase |
|---|---|
| PM docs under `PM/Admin-console/` | Edit `supercat-code/` / `supercat_server` |
| Read-only BQ / Rails diagnosis | CREATE/ALTER MVs, migrations, CronTask deploy, PRs |
| | Edit Sales Portal Friday demos |
| | Jira writes |

**This document does not authorize apply.** Betting / Phase 4 GO brief comes after Orchestrator Phase 2 PASS (and optional Phase 3 HTML).

---

## 10. Out of scope (boundary restated)

| Out | Why |
|---|---|
| Sales Portal nav / Intelligence strip | Different job (commerce behavior floor) — `BOUNDARY` + `SURFACE-PLACEMENT` B2 |
| Bet E Portal & Access Settings | Config plane, not adoption analytics |
| Bet F persona IA | Placement only; closed as Feature Usage owner |
| Client self-serve dashboard | CTO non-goal |
| Cross-org benchmarks · realtime · alerting · WoW/MoM | CTO non-goals |
| Admin Console 2.0 / toggle re-triage | Out of appetite |
| Reuse empty `*_feature_usage_report` BQ tables | No date dimension |

Placement lineage: `PM/sales-portal-agent-starters/cycle-03-outputs/SURFACE-PLACEMENT.md` §B2 / Phase-4 CLOSE → project home `PM/Admin-console/`.

---

## 11. Eng handoff — suggested PR / betting order

After `ISOLATION OFF — GO on Admin Feature Usage`:

1. **PR-A (ST-1):** `analytics_taxonomy.yml` + MV SQL generator + MV apply runbook (may be data-eng PR / console, not Rails)  
2. **PR-B (ST-2):** gem + migrations + `Analytics::BigQuerySync` + CronTask + sync log  
3. **PR-C (ST-3):** controller, routes, SuperCat ACL + request specs  
4. **PR-D (ST-4):** admin_v2 views, Chart.js, Stimulus, Turbo Frames (can split charts vs leaderboard if needed)

Smoke org for QA: any high-volume shortname (taxonomy events confirmed live in BQ; exemplar UI remains Courchesne).

---

*Phase 2 eng-ready plan. Ready for Orchestrator Review Card — Phase 2.*
