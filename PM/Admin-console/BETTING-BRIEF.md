# BETTING BRIEF — Admin Console · eCat Feature Usage Report

**Ready-for-table / GO note** · Phase 4 · 2026-07-24  
**Home:** `PM/Admin-console/`  
**Isolation:** ON — this brief does **not** unlock code apply

---

## 1. Bet one-liner

**Admin Console · SuperCat-admin · org Viewer Usage** — Mixpanel → BQ MVs → nightly Postgres → Chart.js dashboard so CS/GTM can open any org and see adoption (active-day logins, category mix, leaderboard, user drill-down).

## 2. Problem / appetite

Mixpanel usage sits in BigQuery (~10M events, ~170 orgs) and powers EBR/F7 “No Portal Usage” language, but admins have no operational UI — only CSV/export-style workflows. Appetite: **small-to-batch** ship of one org-scoped Admin report on the CTO-finalized spine (2026-07-15), not a warehouse product or Admin 2.0.

## 3. Done when

| Gate | Bar |
|---|---|
| **ACs** | AC-1…AC-9 + eng rows **AC-3a** (category % chart) + **AC-4a** (logins-by-user chart) |
| **Eng wave** | ST-1 → ST-2 → ST-3 → ST-4 complete |
| **Demo parity** | ST-4 matches Phase 3 HTML: filters, user drill, range recompute |
| **So-what (v0 must-haves · Phase 3c)** | Status chips (Excelling / Steady / Declining / Quiet-Cold) · org so-what strip (2–3 Mixpanel-only coaching lines) · non-seller drill hint when busy-but-not-submitting — **no GMV / no Portal** |

A SuperCat admin opens `/:org_shortname/analytics_dashboard`, defaults to current quarter, sees KPIs + charts + sortable leaderboard with status chips, a short so-what strip, drills a user (incl. non-seller hint when relevant), trusts data ≤24h old — without leaving Admin Console.

## 4. Architecture lock

```
Mixpanel → supercat-data-pipeline.mixpanel
        → mv_org_daily_kpis · mv_user_daily_activity · mv_user_device_info
        → nightly Analytics::BigQuerySync → Postgres analytics_*
        → AnalyticsDashboardController (admin_v2) + Chart.js + Stimulus + Turbo Frames
```

Cite: [`TECHNICAL-PLAN-feature-usage.md`](TECHNICAL-PLAN-feature-usage.md) §1 / §11. Login = distinct calendar **active days** (not sessions). Taxonomy via YAML (not hardcoded SQL).

## 5. Not betting

Portal Intelligence strip · Bet E Settings hub · Bet F build · client self-serve · cross-org benchmarks · realtime · alerting · WoW/MoM · Admin Console 2.0 · Insightful CEO report / $ signals.

## 6. Open decisions for the table

| ID | Item | Recommended default |
|---|---|---|
| **Q-ORG** | COALESCE include `current_organization_shortname`? | **Yes** (sparse `organization_shortname` alone → empty dashboards) |
| **Q-TZ** | Activity date timezone | Confirm UTC vs org-local vs America/Denver at table |
| **Q-MV** | MV refresh + IAM owner | ≤24h refresh; data eng owns dataset IAM |
| **Q-NAV** | Admin nav label/placement | Admin Console only — **not** Portal, **not** Bet E Settings |
| **Q-ACL** | SuperCat-admin signal for AC-9 | Confirm `User#is_admin?` + explicit gate (deny OrgUser-only) |
| **Q-TAX** | Taxonomy vs raw CTO paste | Spot-check when paste available; YAML from `TAXONOMY-events.md` until then |
| **Q-HIST** | Postgres sync window | Trailing history from MVs (all vs ~8 quarters) — eng size at kickoff |
| **Q-CRED** | BQ credentials for Rails | Workload Identity / SA via secrets store (ops) |

## 7. Eng wave / PR order

After GO phrase only ([`TECHNICAL-PLAN-feature-usage.md`](TECHNICAL-PLAN-feature-usage.md) §11):

| PR | ST | Slice |
|---|---|---|
| **PR-A** | ST-1 | `analytics_taxonomy.yml` + MV SQL generator + MV apply runbook |
| **PR-B** | ST-2 | gem + migrations + `Analytics::BigQuerySync` + CronTask / CronJob |
| **PR-C** | ST-3 | controller, routes, SuperCat ACL + request specs |
| **PR-D** | ST-4 | admin_v2 views, Chart.js, Stimulus, Turbo Frames |

Order: ST-1 → ST-2 → ST-3 → ST-4 (Stimulus/Chart pin may start parallel with ST-3).

## 8. Demo pointer

- **HTML:** `design-system/app/admin-feature-usage-demo.html`  
- **Runbook:** [`PHASE3-DEMO-RUNBOOK.md`](PHASE3-DEMO-RUNBOOK.md)  
- **ST-4 interaction target:** filters (category/KPI), user drill, range recompute, status chips, so-what strip, non-seller hint — open once before betting table ([`PHASE3-DEMO-RUNBOOK.md`](PHASE3-DEMO-RUNBOOK.md))

## 9. GO phrase

Exact unlock (Kylor only):

```
ISOLATION OFF — GO on Admin Feature Usage
```

This brief **names** the phrase; it does **not** soft-unlock isolation.

## 10. Risks

| Risk | Why it matters |
|---|---|
| Sparse `organization_shortname` | Wrong COALESCE → empty org dashboards (mitigate Q-ORG) |
| OrgUser ACL trap | Default `enforce_permissions` allows client org-admins — AC-9 needs explicit SuperCat gate |
| Chart.js pin | Not in importmap today — ST-4 must add |
| Taxonomy paste gap | Events SoT unverified vs raw CTO paste (Q-TAX) |

---

*Phase 4 betting brief · Orchestrator Final PASS 2026-07-24 — does not authorize Rails/BQ apply.*
