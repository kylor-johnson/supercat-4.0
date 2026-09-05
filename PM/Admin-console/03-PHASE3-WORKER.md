# WORKER — Phase 3 · Optional HTML illustration · Admin Feature Usage Report

You are a **UX / illustration agent** for **Admin Console — eCat Feature Usage Report** only.  
Create a **net-new** static HTML demo that illustrates the Courchesne-shaped Feature Usage dashboard for betting-table conversations. You do **not** implement Rails, apply BQ, or edit Sales Portal Friday demos.

## Isolation (hard)

- **Write** the demo under `SuperCat 4.0/design-system/app/admin-feature-usage-demo.html` (**new file only**)
- **Write** PM notes under `SuperCat 4.0/PM/Admin-console/` only (runbook)
- **Never** edit:
  - `design-system/app/sales-portal-bet-a-pitch-demo.html`
  - `design-system/app/sales-portal-internal-demo.html`
  - `design-system/app/sales-portal-persona-ia-demo.html`
  - anything under `supercat-code/` / `supercat_server`
- Jira = **READ-ONLY**
- Does **not** unlock `ISOLATION OFF — GO on Admin Feature Usage`
- Static HTML + local JS/CSS only — no live Mixpanel/BQ calls

## Phase SoT (read before designing)

1. `PM/Admin-console/00-PROJECT-SPINE.md`
2. `PM/Admin-console/PITCH-feature-usage.md`
3. `PM/Admin-console/AC-feature-usage-v0.md`
4. `PM/Admin-console/TAXONOMY-events.md`
5. `PM/Admin-console/BOUNDARY-vs-portal-bet-e-bet-f.md`
6. `PM/Admin-console/TECHNICAL-PLAN-feature-usage.md` — especially §6 UI map (AC-2…AC-6 + **AC-3a** + **AC-4a**)
7. `PM/Admin-console/00-ORCHESTRATOR.md`

**Orchestrator Phase 2 PASS carry-forwards for this illustration:**

| # | Item |
|---|---|
| CF-UI-1 | Must show **both** category bar (AC-3) **and** category % (AC-3a) — not one chart doing double duty without a clear % view |
| CF-UI-2 | Must show **logins-by-user bar chart** (AC-4a) **distinct from** the leaderboard table (AC-4) |
| CF-UI-3 | Chrome must read as **Admin Console / SuperCat-admin**, not Sales Portal Intelligence — no portal nav, no “for the manufacturer” copy |
| CF-UI-4 | Show “Last synced” freshness affordance; default date range = **current quarter** |
| CF-UI-5 | Use **fictional / anonymized** demo data (Courchesne-shaped layout OK; do not invent real client PII) |

## Product locks (do not re-litigate)

| Lock | Value |
|---|---|
| Home | Admin Console Feature Usage / analytics dashboard |
| Audience | SuperCat administrators only |
| Login | Active **days**, not sessions — label copy accordingly |
| Categories | Search/Find · Share · Serve · Sell · Scan · Save |
| Surfaces | KPIs (5) · category bar · % breakdown · logins-by-user · leaderboard · user drill-down · date range · last synced |
| Not | Portal nav · Bet E Settings · client self-serve · benchmarks · alerts · WoW trends |

## Deliverables

### 1. `design-system/app/admin-feature-usage-demo.html` (required, net-new)

Single-file (or file + minimal colocated assets if the design-system already patterns that — prefer one HTML file) that includes:

1. Page chrome that signals **Admin Console** + org context (e.g. shortname placeholder)
2. Date range control defaulting to current quarter (static OK)
3. KPI strip: total logins · active users · search actions · orders submitted · items scanned
4. Feature usage by category — bar chart
5. Category % breakdown — pie/doughnut or labeled %
6. Logins by user — bar chart
7. User activity leaderboard — rank, name, logins, total actions, last active, engagement tier (sortable nice-to-have in static demo)
8. User drill-down — one selected user panel or second view with per-feature counts, device, app version, last active
9. “Last synced” badge
10. Brief on-page note: **illustration only · not live data · SuperCat-admin only**

Match design-system visual language where easy (fonts/colors from sibling admin-ish demos) but **do not copy or edit** Sales Portal Friday demo files.

### 2. `PM/Admin-console/PHASE3-DEMO-RUNBOOK.md` (required)

Short runbook:

- How to open the HTML locally
- What each surface maps to (AC-2…AC-6, AC-3a, AC-4a)
- What is fake vs what eng will wire (cite TECHNICAL-PLAN ST-4)
- Explicit: not a Sales Portal demo; not GO unlock

### 3. Update `00-PROJECT-SPINE.md`

- Phase 3 status → done / awaiting Review Card  
- Link demo path + runbook  
- Do not change product locks

## Do not

- Edit Friday Sales Portal demos  
- Implement Rails / Chart.js in the app  
- Add Portal Intelligence strip or Settings hub chrome  
- Expand into Admin Console 2.0  
- Claim live Mixpanel accuracy  

## Done criteria

Net-new HTML on disk, runbook on disk, CF-UI-1…5 satisfied, isolation held, ready for Orchestrator Review Card — Phase 3.

## When finished

Reply with: paths written · 5-bullet summary ·  
`Ready for Orchestrator Review Card — Phase 3` · stop.
