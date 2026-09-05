# WORKER — Phase 2 · Eng-ready plan · Admin Feature Usage Report

You are a **Program / FIX agent** for **Admin Console — eCat Feature Usage Report** only.  
Produce an eng-ready technical plan under `PM/Admin-console/`. You do **not** implement Rails, apply BQ MVs, edit Sales Portal demos, or unlock isolation.

## Isolation (hard)

- **Write only** under `SuperCat 4.0/PM/Admin-console/`
- **Never** edit `supercat-code/` / `supercat_server` (read-only cite OK)
- **Never** create/apply BQ views, migrations, CronTasks, or PRs
- **Never** modify Sales Portal Friday demos:
  - `design-system/app/sales-portal-bet-a-pitch-demo.html`
  - `design-system/app/sales-portal-internal-demo.html`
  - `design-system/app/sales-portal-persona-ia-demo.html`
- Jira = **READ-ONLY**
- Does **not** unlock `ISOLATION OFF — GO on Admin Feature Usage`
- No HTML demo this phase (Phase 3 optional later)

## Phase 1 SoT (locked — do not re-litigate)

Read end-to-end before writing:

1. `PM/Admin-console/00-PROJECT-SPINE.md`
2. `PM/Admin-console/PITCH-feature-usage.md`
3. `PM/Admin-console/AC-feature-usage-v0.md` (AC-1…AC-9 + KPI defs)
4. `PM/Admin-console/TAXONOMY-events.md` (product SoT for YAML)
5. `PM/Admin-console/BOUNDARY-vs-portal-bet-e-bet-f.md`
6. `PM/Admin-console/00-ORCHESTRATOR.md` + `README.md`
7. Placement lineage: `PM/sales-portal-agent-starters/cycle-03-outputs/SURFACE-PLACEMENT.md` §B2 / Phase-4 CLOSE

**Orchestrator Phase 1 PASS carry-forwards (must address in plan):**

| # | Item |
|---|---|
| CF-1 | Dashboard surfaces **#3 Category % breakdown** and **#4 Logins by user bar chart** are must-show in AC pack but lack dedicated AC IDs — encode as explicit eng acceptance rows (fold into AC-3/AC-4 or add AC-3a/AC-4a) so they cannot be dropped |
| CF-2 | Align org field naming: spine/pitch say `event.org`; AC/taxonomy say `organization_shortname` — verify against live Mixpanel BQ schema **read-only** and lock one name in the plan |
| CF-3 | If Kylor pastes CTO capture / screenshots, spot-check taxonomy event lists; if no paste, plan from `TAXONOMY-events.md` and flag “taxonomy unverified vs raw CTO paste” |

## Product locks (unchanged)

| Lock | Value |
|---|---|
| Home | Admin Console only · route `/:org_shortname/analytics_dashboard` |
| Audience | SuperCat administrators only (AC-9) |
| Login | Distinct calendar **active days** (≥1 event), not sessions |
| Engagement | High ≥50 · Medium 10–49 · Low &lt;10 actions/day avg over active days |
| Taxonomy | Search/Find · Share · Serve · Sell · Scan · Save + excluded meta → YAML |
| Data path | Mixpanel → `supercat-data-pipeline.mixpanel` → 3 MVs → nightly Postgres `analytics_*` → Chart.js / Stimulus / Turbo Frames |
| Freshness | ≤24h + “Last synced” |
| Non-goals | Portal nav · Bet E · Bet F build · client self-serve · benchmarks · realtime · alerting · WoW/MoM · Admin Console 2.0 |

## Eng wave (summarize → detail; do not implement)

| ST | Scope |
|---|---|
| **ST-1** | BQ MVs (`mv_org_daily_kpis`, `mv_user_daily_activity`, `mv_user_device_info`) + `config/analytics_taxonomy.yml` (+ generator note) |
| **ST-2** | google-cloud-bigquery gem, migrations for `analytics_*` tables, `Analytics::BigQuerySync`, CronTask / K8s CronJob |
| **ST-3** | `AnalyticsDashboardController` &lt; AdminController, org-scoped routes, SuperCat-admin ACL |
| **ST-4** | admin_v2 views, Chart.js, Stimulus, Turbo Frames, leaderboard sort, user drill-down |

Order: ST-1 → ST-2 → ST-3 → ST-4 (Stimulus shell may parallel ST-3).

## Read-only diagnosis (cite paths; no edits)

When useful for the plan, skim and **cite**:

- `supercat_server/app/controllers/rep_activities_controller.rb`
- `supercat_server/app/services/rep_activities/build_dashboard_stats.rb`
- `supercat_server/app/views/rep_activities/dashboard_v2.html.erb`
- `supercat_server/app/models/cron_task.rb`
- Org-scoped routes under `:org_shortname`
- Existing Admin ACL / `enforce_permissions` patterns
- Optional: BQ MCP / inventory for Mixpanel table column names (read-only) — do not CREATE/ALTER views

## Deliverables (create under `PM/Admin-console/`)

### 1. `TECHNICAL-PLAN-feature-usage.md` (required)

Must include:

1. **Architecture diagram / data flow** — Mixpanel → MVs → sync → Postgres → controller → UI (match Phase 1 names unless CF-2 forces a rename with evidence)
2. **ST-1…ST-4 work packages** — inputs, outputs, owner-shaped slices, dependencies, rough sizing (S/M/L)
3. **Schema sketch** — MV column intents + Postgres `analytics_*` tables (enough for eng betting; not a migration file)
4. **YAML taxonomy contract** — how `TAXONOMY-events.md` maps to `config/analytics_taxonomy.yml`; regen steps for MVs
5. **Rails surface map** — controller actions, services (`Analytics::BuildDashboard`, `BuildUserDetail`, sync), routes, ACL check points for AC-1 / AC-9
6. **UI map** — which Chart.js / Stimulus / Turbo Frame pieces cover AC-2…AC-6 **plus CF-1 surfaces** (category %, logins-by-user)
7. **Freshness / sync** — Cron cadence, MV refresh assumption, `analytics_sync_logs`, failure visibility (AC-7)
8. **Gap checklist** — unknowns, risks, decisions needed from Kylor/CTO before GO (explicit open questions)
9. **Isolation reminder** — plan does not authorize apply; GO phrase required
10. **Out of scope** — restates boundary one-pager in one short table

### 2. Optional: eng-handoff appendix

If useful, a short `ENG-HANDOFF-feature-usage.md` (ST checklist + first PR suggestion order). Prefer folding into the technical plan unless length demands a split.

### 3. Update `00-PROJECT-SPINE.md`

- Phase 2 status → done / awaiting Review Card  
- Link new plan file(s)  
- Do **not** change product locks

## Do not

- Implement any ST  
- Author Phase 3 HTML  
- Rewrite Phase 1 AC/taxonomy product locks (only clarify CF-1/CF-2)  
- Pull Bet A/E/F or Portal Intelligence into scope  
- Post to Jira  

## Done criteria

`TECHNICAL-PLAN-feature-usage.md` on disk, CF-1…CF-3 addressed, gap checklist honest, isolation held, ready for Orchestrator Review Card — Phase 2.

## When finished

Reply with: paths written · 5-bullet summary ·  
`Ready for Orchestrator Review Card — Phase 2` · stop.
