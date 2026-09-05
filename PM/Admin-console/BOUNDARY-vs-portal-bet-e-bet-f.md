# BOUNDARY — Feature Usage vs Portal · Bet E · Bet F · self-serve

**One-pager** · Phase 1 · 2026-07-24  
**This project home:** `PM/Admin-console/`  
**Placement lineage:** `SURFACE-PLACEMENT.md` §B2 / Phase-4 CLOSE · Program F7

---

## This project (inside the line)

| | |
|---|---|
| **Surface** | Admin Console |
| **Audience** | SuperCat administrators (CS / GTM / internal ops) |
| **Job** | Org-wide eCat **adoption / feature usage** — logins (active days), active users, category mix, leaderboard, user drill-down |
| **Data** | Mixpanel → BigQuery → nightly Postgres analytics_* |
| **Why it exists** | GTM/CS operationalize “No Portal Usage” / value demos — not a rep commerce answer |

---

## vs Sales Portal Intelligence team strip

| | Portal Intelligence strip | This report |
|---|---|---|
| **Home** | Sales Portal → Intelligence | Admin Console |
| **Audience** | Owner / rep portal seats | SuperCat admins only |
| **Job** | Behavior floor tied to a **commerce** answer (Q-R1 logins pulse + Q-18 eCat GMV leaderboard or Q-01 fallback) | Org adoption analytics as a **GTM/CS** tool |
| **Overlap** | Both mention “activity” / logins | Different questions, different homes — do not merge |
| **Rule** | Never add Feature Usage nav/KPI/leaderboard to Sales Portal product IA for v0 |

Frozen seed (`SURFACE-PLACEMENT` B2): *behavior floor tied to commerce* → Portal; *org-wide adoption analytics* → Admin Console.

---

## vs Bet E — Portal & Access Settings hub

| | Bet E | This report |
|---|---|---|
| **Home** | Admin Console → Portal & Access (Settings) | Admin Console → Feature Usage / analytics dashboard |
| **Job** | Config plane: enablement, territory/data access, display, export; SuperCat-locked revenue definitions | Read-only adoption analytics |
| **Audience mix** | Client org-admin self-serve (~18 survivors) + SuperCat locked levers | **SuperCat-admin only** (AC-9) — not client Settings |
| **Rule** | Do not bury Feature Usage inside Settings hub IA; do not re-triage 134 toggles as part of this bet |

---

## vs Bet F — persona IA

| | Bet F | This report |
|---|---|---|
| **Job** | Who sees what **first** on the shared Sales Portal surface (defaults + fail-closed rules) | Build the Admin Feature Usage product |
| **Status** | Shaped / betting-table ready; placement documented | Separate PM/eng project (this folder) |
| **Rule** | Bet F may **cite placement only**; it does not spec, build, or demo Feature Usage charts |

Phase-4 CLOSE (2026-07-24): Feature Usage is **not** a Bet F deliverable. Project home = `PM/Admin-console/`.

---

## vs future client self-serve

| | |
|---|---|
| **CTO non-goal (v0)** | Customer-facing / manufacturer self-serve version of this dashboard |
| **Rule** | No “ship to client org-admin later” scope in Phase 1–2; revisit only as a new shaped bet |

---

## Contamination checklist (Orchestrator)

Fail Phase review if the pack:

- Puts Feature Usage in Sales Portal nav or Friday demos  
- Treats this as Bet E Settings work  
- Reopens Bet F to own the build  
- Adds client self-serve, benchmarks, realtime, alerting, or WoW trends as v0 must-haves  
- Expands into Admin Console “2.0”

---

*Boundary SoT for Phase 1. Keep builds in this folder; keep Portal / Bet E / Bet F out.*
