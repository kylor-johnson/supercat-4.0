# Phase 3c demo runbook — Admin Feature Usage

**File:** `design-system/app/admin-feature-usage-demo.html`  
**Audience:** betting table / appetite — **CS/GTM Admin ops tool** (CSV-export upgrade)  
**Not:** live Mixpanel · Rails UI · Sales Portal Friday demos · Insightful CEO report · GO unlock

---

## Open locally

```
file:///Users/kylorjohnson/Library/Mobile%20Documents/com~apple~CloudDocs/SuperCat%204.0/design-system/app/admin-feature-usage-demo.html
```

Or from repo root:

```bash
open "design-system/app/admin-feature-usage-demo.html"
```

Needs network once for Chart.js CDN. Tokens: `../ds/tokens/`.

Optional deep-link hash (productized feel):

```
#range=q3&cat=sell&user=arivera
```

Non-seller hint deep-link (Q3):

```
#range=q3&user=cmorin
```

---

## ≤2 min click path (prove dynamic)

1. **Chrome** — SuperCat Admin · org `demoorg` · job line “replaces spreadsheet exports” · Last synced · Import Status as inert sibling (not Settings home).
2. **So what strip** — 2–3 coaching lines (quiet/cold + declining · Sell thin vs Search · old app versions). Switch **Q3 → Q2 → Last 30d** and watch the lines recompute (counts change; still Mixpanel-only — no $).
3. **Status chips** — leaderboard **Status** column: Excelling / Steady / Declining / Quiet-Cold (engagement tier kept as mono sublabel). Visible mix across users; Quiet-Cold rows keep the left-dot emphasis.
4. **Category filter** — click **Sell** on the bar (or doughnut). Chip `Category: Sell` · leaderboard + logins chart shrink to contributors · Clear resets.
5. **KPI filter** — click **Orders submitted** → only users with orders · click **Active users** → scroll/highlight leaderboard.
6. **User drill** — click a logins bar **or** leaderboard row → AC-6 panel (features + device + version + last active + status). Open **C. Morin** on Q3 → quiet hint *Busy in catalog · not submitting orders*. Click a feature row → toast with plain label + event + count.
7. **Sort** — click Actions / Logins / Status headers (sort kept).

Stop. Isolation held — no Portal / Bet E / Insightful $ / peer % / GMV.

---

## Status rules (demo fact store)

| Status | Rule (Mixpanel-only) |
|---|---|
| **Excelling** | High engagement tier **and** active days/actions ≥ prior comparable window |
| **Steady** | Mid activity; not clearly up or down |
| **Declining** | Active days or actions **down** vs prior window (same length) — **no GMV** |
| **Quiet/Cold** | ≤1 active day in current range |

Precomputed per user per range in `FACTS` (`status` field). High/Med/Low tier remains as secondary sublabel.

---

## Surface → AC map

| Surface in demo | AC / eng row | Notes |
|---|---|---|
| KPI strip (5) — clickable | **AC-2** | Logins = active days; KPI click filters/focuses |
| Feature usage by category — bar | **AC-3** | Six taxonomy cats; `onClick` filters |
| Category breakdown — doughnut + % | **AC-3a** | Same totals; segment click filters |
| Logins by user — horizontal bar | **AC-4a** | Distinct from table; bar click → drill |
| User activity leaderboard | **AC-4** | Rank, name, logins, actions, last, **status chip** (+ tier sublabel); sort + row drill |
| Org “so what” strip | Phase 3c | 2–3 computed coaching lines; updates with range |
| User drill-down panel | **AC-6** | Per-feature (plain + mono), device, version, last, status; optional non-seller hint |
| Date range control | **AC-5** | Default = current quarter (Q3 2026); reloads fact store |
| Last synced badge | **AC-7** (UI affordance) | Fake timestamp |

Chrome: **Admin Console / SuperCat Admin** + `demoorg` — not Sales Portal nav.

---

## Insightful-borrowed jobs vs non-overlap

| Borrowed *question* (Admin language) | Must not become |
|---|---|
| Seat / quiet seats (Q-05 · quiet/dark style) | Portal Q-R1 commerce behavior floor · GMV leaderboard |
| Feature depth naming hygiene (Q-22 plain labels) | CEO report · peer benchmarks · $ upside |
| Mixpanel depth ≠ login floor (provenance) | Dollar Axis B fused into ranks |
| Non-seller *hint* idea (Q-04 shape) | Full role taxonomy UI |
| Trajectory *shape* for status (Q-06, ignore GMV) | WoW chart product · $ decline narrative |
| Workflow maturity *signal* idea (Q-46) | Insightful HTML narrative / Mode templates |

Admin copy rule: Mixpanel = **context, never a dollar**. Zero Portal. Zero $.

---

## Fake vs eng (ST-4)

| Fake (this HTML) | Eng wires later (TECHNICAL-PLAN §6 / ST-4) |
|---|---|
| In-page `FACTS` per range (q3 / q2 / 30d) + `status` | `Analytics::BuildDashboard` + Postgres `analytics_*` |
| Client filter chain + hash | Turbo Frames + Stimulus controllers |
| Chart.js CDN + `onClick` | importmap Chart.js + `analytics_charts_controller` |
| Client-side leaderboard sort | `analytics_leaderboard_controller` |
| Inline drill + feature toast + non-seller hint | `…/users/:username` + `BuildUserDetail` |
| “Last synced” string | `analytics_sync_logs.finished_at` |
| Fictional Northwind / anonymized names | Live Mixpanel-derived org data |

ST-1…ST-3 (MVs, sync, controller/ACL) not illustrated beyond chrome + ACL footnote.

---

## Explicit out-of-bounds

- **Not** Sales Portal / Friday demos  
- **Does not** unlock `ISOLATION OFF — GO on Admin Feature Usage`  
- **Not** Bet E Settings hub (Settings nav inert) · **not** Import Status detail  
- **Not** Insightful CEO signals / $ / peers · **not** client self-serve · **not** benchmarks / alerts / WoW

---

*Phase 3c so-what layer. Ready for Orchestrator Review Card — Phase 3c.*
