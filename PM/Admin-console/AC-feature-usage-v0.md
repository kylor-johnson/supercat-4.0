# AC — eCat Feature Usage Report (v0)

**Product:** Admin Console · SuperCat administrators only  
**Source:** CTO handoff / Brent Sanders implementation mapping (2026-07-15) + Kylor placement lock (2026-07-24)  
**Companion:** `TAXONOMY-events.md`, `PITCH-feature-usage.md`  
**Isolation:** ON — these ACs shape; they do not authorize Rails apply

---

## KPI & term definitions (product locks)

| Term | Definition |
|---|---|
| **Login** | A distinct calendar date on which a user generated ≥1 Mixpanel event (**active day**). Not raw session count. |
| **Active user** | A user with ≥1 login in the selected date range. |
| **Total logins (org KPI)** | Sum of user-level active days in range (org aggregate). |
| **Search actions** | Count of events in taxonomy category **Search / Find** in range. |
| **Orders submitted** | Count of `order_submitted` events in range (Sell category; KPI callout). |
| **Items scanned** | Count of `item_scanned` events in range (Scan category; KPI callout). |
| **Total actions (leaderboard)** | Sum of categorized feature events in range (**excluding** login-day itself as an action; excluding meta/excluded events). |
| **Engagement tier** | From avg actions/day over active days in range: **High** ≥50 · **Medium** 10–49 · **Low** &lt;10. |
| **Organization** | Resolved in BQ MVs via `COALESCE(event.organization_shortname, user_org_mapping.organization_shortname)`. Rows still NULL after COALESCE are excluded. |
| **Default date range** | Current calendar quarter (from quarter start through today, or full quarter when browsing history — UI default = current quarter). |
| **Freshness** | Data displayed is ≤24 hours stale; UI exposes last successful sync time. |

---

## Acceptance criteria

### AC-1 — Org-scoped navigation

**Given** a SuperCat administrator authenticated in Admin Console  
**When** they open the Feature Usage / analytics dashboard for an organization  
**Then** the view is scoped to that org only (route pattern `/:org_shortname/analytics_dashboard`)  
**And** they can navigate to the same dashboard for any other org they are allowed to administer  

*Implemented by (eng map):* `AnalyticsDashboardController#show` + org-scoped route · **ST-3**

---

### AC-2 — Summary KPIs for selected range

**Given** an org dashboard with a selected date range  
**When** the page loads  
**Then** it shows five KPIs for that range:  
1. Total logins (active days)  
2. Active users  
3. Search actions  
4. Orders submitted  
5. Items scanned  

*Implemented by:* `Analytics::BuildDashboard#build_kpis` ← `analytics_org_daily_summaries` · **ST-4**

---

### AC-3 — Feature usage by category

**Given** the taxonomy in `TAXONOMY-events.md` / `config/analytics_taxonomy.yml`  
**When** the dashboard renders  
**Then** feature usage is visualized by category (bar chart) aggregating only categorized events  
**And** excluded meta events do not appear in category totals  

*Implemented by:* `Analytics::BuildDashboard#build_category_breakdown` + Chart.js · **ST-4**

---

### AC-4 — User activity leaderboard

**Given** users with activity in the selected range  
**When** the leaderboard renders  
**Then** each row shows: rank, name, logins, total actions, last active, engagement tier  
**And** the table is sortable by those columns  
**And** default rank order is by total actions descending  

*Implemented by:* `Analytics::BuildDashboard#build_leaderboard` + sortable table Stimulus · **ST-4**

---

### AC-5 — Date range picker (default current quarter)

**Given** the dashboard  
**When** the admin opens it with no date params  
**Then** the range defaults to the **current quarter**  
**When** they change the range  
**Then** KPIs, charts, and leaderboard reload for the new range (Turbo Frame acceptable)  

*Implemented by:* `date_range_controller.js` + Turbo Frames · **ST-4**

---

### AC-6 — Individual user drill-down

**Given** a user on the leaderboard (or drill-down route)  
**When** the admin opens that user’s detail  
**Then** they see per-feature counts for the selected range, device model, app version, and last active  

*Implemented by:* `Analytics::BuildUserDetail` + `analytics_user_profiles` / daily summaries · **ST-4**

---

### AC-7 — Freshness ≤24h

**Given** the BQ MV + nightly Postgres sync pipeline  
**When** an admin views the dashboard  
**Then** underlying data is no more than **24 hours** stale  
**And** the UI shows a “Last synced” (or equivalent) timestamp from sync logs  

*Implemented by:* BQ MV 24h refresh + `Analytics::BigQuerySync` + `analytics_sync_logs` · **ST-1, ST-2**

---

### AC-8 — Configurable event taxonomy

**Given** product needs to add or reclassify an event later  
**When** eng updates `config/analytics_taxonomy.yml` (and regenerates MVs as needed)  
**Then** category aggregation changes without rewriting hardcoded per-category SQL in ad-hoc queries  

*Implemented by:* shared YAML loaded by BQ view generator + Rails services · **ST-1**

---

### AC-9 — SuperCat administrators only

**Given** a non–SuperCat-admin session (e.g. client org user / unauthenticated)  
**When** they request the analytics dashboard URL  
**Then** access is denied  
**Given** a SuperCat administrator  
**When** they request it  
**Then** access is allowed  

*Implemented by:* `authenticate` + `enforce_permissions` on `AnalyticsDashboardController` &lt; `AdminController` · **ST-3**

---

## Dashboard surfaces (must show — date-range filtered)

| # | Surface |
|---|---|
| 1 | Summary KPIs (AC-2) |
| 2 | Feature usage by category — bar chart (AC-3) |
| 3 | Category breakdown — % distribution |
| 4 | Logins by user — bar chart |
| 5 | User activity leaderboard (AC-4) |
| 6 | Individual user drill-down (AC-6) |

## Non-goals (fail AC if built as v0)

- Cross-org benchmarks  
- Realtime / streaming  
- Alerting on engagement drops  
- Customer-facing / client self-serve version  
- Historical WoW / MoM trend lines  

## Eng subtask map (reference only)

| ST | Delivers |
|---|---|
| ST-1 | MVs + taxonomy YAML |
| ST-2 | Gem, migrations, sync, CronTask |
| ST-3 | Controller, routes, ACL (AC-1, AC-9) |
| ST-4 | Views / charts / leaderboard / drill-down (AC-2…AC-6) |

---

*AC v0 SoT for Phase 1. Do not implement until isolation GO.*
