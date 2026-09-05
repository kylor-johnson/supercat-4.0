# WORKER — Phase 3b · Elite rewrite · Admin Feature Usage demo

You are a **UX / product illustration agent**. **Rewrite in place**  
`design-system/app/admin-feature-usage-demo.html` so it feels like the **Admin Console upgrade from a shitty CSV export** — clickable, dynamic, org-scoped, SuperCat-admin only — not a static Courchesne poster and **not** Sales Portal Intelligence / Insightful CEO report.

## Isolation (hard)

- **Edit only** `design-system/app/admin-feature-usage-demo.html` + update `PM/Admin-console/PHASE3-DEMO-RUNBOOK.md` + Phase 3 status line in `00-PROJECT-SPINE.md`
- **Never** edit Sales Portal Friday demos, `supercat-code/`, BQ, or Jira
- **Never** open a Bet E Settings build or Portal nav item
- Steal **dimensions / jobs** from Insightful 4.0 foundation docs — **do not** copy CEO prose, $ upside, peer benchmarks, or Portal Q-R1/Q-18 commerce strip
- Does **not** unlock `ISOLATION OFF — GO on Admin Feature Usage`

## Why Phase 3 FAILED (fix these)

| Fail | Fix |
|---|---|
| Date range only nudges a meta string | **Recompute** KPIs + charts + leaderboard + drill from an in-page dataset when range changes |
| Only leaderboard → drill is clickable | Full **filter chain**: KPI / category / user chart / row all drill or filter |
| Feels like a chart collage | Frame as **CS/GTM admin ops tool** replacing export-and-sort-in-Excel |
| No Insightful-informed admin jobs | Borrow seat/cold/feature-depth *questions* — not CEO report layout |
| Risk of Portal/Settings bleed | Admin chrome only; nav may mention Import Status as sibling Admin tool — **do not** deep-link Settings as Feature Usage home |

## Mandatory reads (before rewrite)

**This project (locks):**
1. `PM/Admin-console/00-PROJECT-SPINE.md`
2. `PM/Admin-console/AC-feature-usage-v0.md` + `TAXONOMY-events.md`
3. `PM/Admin-console/TECHNICAL-PLAN-feature-usage.md` §6 (AC-2…AC-6, **AC-3a**, **AC-4a**)
4. `PM/Admin-console/BOUNDARY-vs-portal-bet-e-bet-f.md`

**Admin pattern (read-only cite):**
5. `supercat-code/supercat_server/docs/REP_ACTIVITY_TRACKING.md` — Admin dashboard = insight cards + ranked tables (not CSV). Feature Usage should feel like that class of Admin tool, Mixpanel-backed.

**Insightful 4.0 — steal questions only (not the CEO product):**
6. `Insightful Product 4.0/foundation/query_library_v2.md` — skim **Q-05 Seat Utilization**, **Q-22 Feature Usage Depth**, **Q-46 workflow maturity** (Mixpanel denominator idea), **Q-R1** only to know what *not* to become (Portal behavior floor)
7. `Insightful Product 4.0/foundation/provenance_spine.md` — Mixpanel depth ≠ Postgres login floor; `last_ipad_login_at` seat proxy language for “cold / quiet” users
8. `Insightful Product 4.0/operators/report_operator.md` — Axis B = Mixpanel **context, never a dollar** (Admin copy rule)

**Do not read / do not merge:** `PM/sales-portal-agent-starters/` packs (except boundary already locked). Do not use Insightful 2.0/3.0.

## Product job (hyper-focused Admin only)

The demo must make these **SuperCat-admin** jobs obvious in &lt;30 seconds:

1. **At-risk org glance** — near-zero active days / users this quarter (“No Portal Usage” operationalized)
2. **Who’s cold vs power** — engagement tiers + quiet/dark-style recency (Admin language; not Portal GMV leaderboard)
3. **Where adoption lives** — Search/Find · Share · Serve · Sell · Scan · Save mix (taxonomy)
4. **Support diagnosis** — one click to user → feature counts + device + app version
5. **Call prep** — date-scoped numbers you’d formerly dump to CSV and pivot

Explicit non-jobs (must not appear as primary UI):
- Manufacturer Owner/rep commerce answers  
- Insightful CEO signals / $ / peer benchmarks / narrative  
- Bet E toggle config  
- File Import Status detail (sibling Admin nav OK as inert link)

## Data model inside the HTML (required)

Build a small **in-browser fact store** (JS object), fictional/anonymized:

```
RANGES: q3 | q2 | 30d
ORG: demoorg
per range:
  kpis: { logins, users, search, orders, scans }
  categories: { search_find, share, serve, sell, scan, save }  // absolute counts
  users: [{ id, name, logins, actions, last, tier, device, version,
            features: [[event, count], ...],
            catShare: { ... } optional }]
```

Rules:
- Changing **Range** reloads every surface from that range’s facts (no “static demo” meta shrug)
- **Active days** language everywhere logins appear
- Unlisted taxonomy events never invent new categories
- Optional: 1–2 “cold” users with 0–1 logins in range to show at-risk coaching targets

## Interaction model (required — clickable + dynamic)

Implement this drill/filter chain (breadcrumb or chip bar shows active filters; **Clear** resets):

```
Org (fixed: demoorg)
  └─ Range (q3 default)  → recomputes all
       ├─ Click KPI “Active users”     → focus leaderboard (scroll + highlight)
       ├─ Click KPI “Orders / Scans / Search” → filter leaderboard to users with that signal > 0
       ├─ Click category bar OR doughnut segment → filter leaderboard + logins chart to contributors of that category; show chip “Category: Sell”
       ├─ Click logins-by-user bar     → open that user’s drill-down
       └─ Click leaderboard row        → drill-down (feature mix + device + version + last active)
            └─ Click a feature row in drill → optional toast/detail: event name + count in range (no new page required)
```

Also required:
- Leaderboard **sortable** (keep)
- Charts use Chart.js `onClick` (not decorative only)
- Selected user + selected category visually obvious
- URL hash optional (`#user=…&cat=sell&range=q3`) nice-to-have for “feels productized”

## UI chrome (Admin, not Portal)

- Keep **SuperCat Admin / Admin Console** shell + org chip
- Title area: **Feature Usage** + one-line job: “Org adoption for CS / GTM — replaces spreadsheet exports”
- Show **Last synced**
- Default range **current quarter**
- Surfaces still cover AC-2, AC-3, AC-3a, AC-4, AC-4a, AC-5, AC-6, AC-7 affordance
- Plain-language feature labels in drill OK (`Product search` with mono event under) — Insightful Q-22 external naming hygiene, Admin-facing
- **No** GMV, order $, margin, peer %, “Intelligence” portal nav, Owner persona copy

## Visual / craft bar

- One composition that reads as a **working Admin tool**, not a dashboard of orphan cards
- Use design-system tokens already linked
- Motion: short highlight/scroll-into-view on drill; chart hover already OK — avoid noise
- Mobile: stack gracefully; drill still usable

## Deliverables

1. **Rewrite** `design-system/app/admin-feature-usage-demo.html` (same path)
2. **Rewrite** `PM/Admin-console/PHASE3-DEMO-RUNBOOK.md` — open steps, interaction walk (click path), AC map, Insightful-borrowed jobs vs non-overlap list, fake vs ST-4
3. **Touch** `00-PROJECT-SPINE.md` — Phase 3 note: “3b rewrite awaiting Review Card” + link this worker

## Done criteria

- Range change visibly changes numbers/charts/users  
- Category click filters people  
- User click (chart or table) opens rich drill  
- Feels like Admin ops upgrade from CSV — not Portal, not Insightful HTML report  
- Fast walk script in runbook (≤2 min) proving the click path  
- Isolation held  

## When finished

Reply with paths · 5-bullet summary of what became dynamic ·  
`Ready for Orchestrator Review Card — Phase 3b` · stop.
