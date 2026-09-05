# TECHNICAL PLAN — Sales Analytics Bet A + Bet C + Bet E (EBR-only)

**Date:** 2026-07-17 · **Updated:** 2026-07-18 (eng-handoff written — this file is now the **shaping companion**; Bet E AC freeze — §8 points at SETTINGS-hub-v1-AC) · **Isolation:** ON — plan only; no `supercat-code/` edits  

> **Eng entrypoint = [`ENG-HANDOFF-bet-a-b-c-e.md`](ENG-HANDOFF-bet-a-b-c-e.md).** That doc is the single implementation SoT for Bet A + Bet B shell + Bet C IR v1 + Bet E (scope/GO gates, AC→code file:line, IR JSON read-model §E.2, Mixpanel degrade §E.3, test plan, PR batches). This TECHNICAL-PLAN remains the **architecture/shaping companion**; where the two could disagree, the ENG-HANDOFF wins. Do not treat this file as a second, conflicting SoT.

**Epic (Bet C):** [EBR-775](https://supercatsolutions.atlassian.net/browse/EBR-775) · **Bet E:** Lane 0→1 control plane (no EBR yet — downstream eng)  
**Authority:** spine §5 · `INSIGHT-IR-v1-AC.md` · `PITCH-phase1-filter-metric-law.md` · `PORTAL-CAPABILITY-MAP.md` · `PORTAL-SETTINGS-CONTROL-PLANE.md` · `SETTINGS-hub-v1-DEMO-SPEC.md` · **`SETTINGS-hub-v1-AC.md`** · `SHIP-READINESS-bet-e.md`  
**Gap tracker:** `SPEC-GAP-CHECKLIST.md`  
**Demo → Rails shell contract:** `DEMO-SURFACE-CONTRACT.md` (nav order, list-tab substance, demo≠prod guardrails)  
**List-tab AC (Given/When/Then):** `LIST-TABS-AC.md`

---

## 1. Goals

1. **Bet A:** Portal territory filter truth (EBR-40 + EBR-212) + metric-law AC (EBR-91, EBR-87).  
2. **Bet C:** Computational IR v1 on Sales Portal — C1 + S1 + team strip under EBR-775.  
3. **Bet E:** Collapse 134 toggles / 6 layers into one **Portal & Access** hub — ~18 client self-service settings, locked revenue definitions, Experiments lab for YAML canaries.  
4. Keep SERV as downstream eng after GO; XL EBR-180 shelved.

---

## 2. Architecture (one spine, two presentations)

```
ERP invoice_data / order_data
        │ ACL
        ▼
portal_invoices.net_amount  ←── Insightful query library (C1, S1, Q-ECON-*)
login_events / orders / Mixpanel ←── Q-R1, Q-18, Q-01, Q-63*
        │
        ├── Sales Portal IR surface (Bet C UI)
        └── Insightful CEO report (existing factory)
```

- Portal warehouse dashboard is **not** validation ground truth — label “invoiced ledger.”  
- Team strip is ERP-optional; commerce heroes require invoice feed.

---

## 3. Bet A — structural (shape → diagnose → GO → build)

| Step | Owner | Output |
|---|---|---|
| Pitch (done) | PROGRAM | `PITCH-phase1-filter-metric-law.md` |
| **AC lock (done)** | PROGRAM | **`FILTER-TRUTH-AC.md`** — AC-A1…A4 (EBR-40/212/91/87 + metric law) |
| Diagnosis (eng footnotes) | FIX / cycle-01 | `FIX-diagnosis-territory-datefilter.md` (SERV-2178/2196 paths) |
| Build | Eng after GO | Implement portal filter + export/quote truth per AC — not EBR-180 |

**Out of plan build:** SERV-2178/2180 (EBR-180 XL), iPad SERV-2395.

---

## 4. Bet C — computational IR v1

| Layer | Choice |
|---|---|
| Computation | Reuse Insightful IDs: C1 / S1 / Q-R1 / Q-18|Q-01; RTD clamp mandatory |
| Read model | org_id → JSON heroes + provenance stamps |
| Presentation | Sales Portal answer-first surface (App kit); EBR-687 = drill pattern later |
| Gates | `Q-ECON-00`; rep-identity for names only; Mixpanel coverage for depth |

### Scopes (Shape Up)

1. **Topline read model** (C1 + stamps) — core, small, novel clamp  
2. **S1 exception list** (EBR-198)  
3. **Team strip** (Q-R1 + leaderboard fallback)  
4. **Portal shell** (flagged layout; wireframe → Rails on GO)  
5. ~Nice: C3 concentration degrade  

### Rabbit holes patched

| Hole | Patch |
|---|---|
| Named rep revenue | Out of v1 |
| Stale CURRENT_DATE windows | RTD only |
| clm future dates | Clamp |
| Quote in sales | EBR-87 / FAL |
| Territory demo on sarreid | Avoid until Bet A / zero-exposure org |

---

## 5. Process gate (Kylor WIP)

```
Stories → features → specs/AC → prototype/demo → customer feedback
  → update AC → build (ISOLATION OFF) → staging → verify → prod → document/promote
```

Current position:
- **Bet A:** `FILTER-TRUTH-AC.md` locked; **Invoices** is the Bet A proof surface; Customers/Orders/Reports answer-first; **What’s broken** last (teaching only).  
- **Bet B shell:** `DEMO-SURFACE-CONTRACT.md` + **`LIST-TABS-AC.md`** — Dashboard default; Intelligence after Reports; Settings Later.  
- **Bet C:** AC + **`IR-v1-QUERIES.md`** live-stamped; Customers → S1 hook; build blocked on GO.  
- **Bet E:** **AC frozen** (`SETTINGS-hub-v1-AC.md`); Settings nav stays Later; betting-table GO still required before build.

---

## 5a. Bet B — list tabs (shell after GO)

Answer-first list surfaces ship with Bet A filter/metric law — not as stub tables. Cite, don’t rediscover from HTML:

| Surface | Primary answer | Spec |
|---|---|---|
| Invoices | Invoiced total for filters | `LIST-TABS-AC.md` LT-INV · contract § Invoices |
| Customers | Selected-range sales + S1 jump | LT-CUST · A1/A2/A4 |
| Orders | Confirmed $ vs Quotes $ (demoted) | LT-ORD · A3 / EBR-87 |
| Reports | Invoiced net = C1 spine | LT-RPT |

**Now specified in the eng-handoff (no longer leftovers):** JSON IR read-model → `ENG-HANDOFF` §E.2; Rails file:line diagnosis (A3) → `ENG-HANDOFF` §C.1; Mixpanel map/degrade (C5) → `ENG-HANDOFF` §E.3. Bet E hub AC = **`SETTINGS-hub-v1-AC.md`** (cite; do not rediscover control-plane).

> **Bet F (ordering authority — not in this GO).** Persona-priority IA is shaped beside this plan (`IA-RECOMMENDATION-v0.md`, `IA-PRIORITY-MATRIX.md`). It is the **who-sees-what-first ordering law for future Bet B work** (role-aware defaults over one shared surface). It does **not** unlock Rails, does **not** rewrite Bet A TRD/AC, and is **not** part of this TECHNICAL-PLAN’s build scope. Illustration only: `design-system/app/sales-portal-persona-ia-demo.html`. Admin Console Feature Usage Report is a **separate project** under `PM/Admin-console/` — not Bet F, not this plan.

---

## 6. Test plan (pre-build — Bet A + Bet C)

### Bet A (`FILTER-TRUTH-AC.md`)
- [ ] A1.1–A1.4 territory scope on invoice list + dashboard  
- [ ] A2.1 export sum = UI for same scope  
- [ ] A3.1 quotes excluded from sales labels  
- [ ] A4 spine = invoiced `net_amount`  

### Bet C (`IR-v1-QUERIES.md`)
- [x] C1 reconciles on sarreid (2026-07-17 stamp)  
- [ ] C1 re-stamp on cci at build  
- [x] S1 decay cohort stamped on sarreid (25 / $1.69M; equal 6=6)  
- [x] Team strip Q-R1 + Q-18 stamped on sarreid (no RS-01)  
- [ ] Re-stamp grade orgs cci + kll before ship  

---

## 7. Explicit no-gos (program-wide)

Rails without GO · EBR-772/776 · EBR-180 XL · iPad tickets · margin · talk-to-data  

**Bet E add-ons:** exposing revenue-definition settings to clients · deleting 4 dormant-wired flags without ship/cut call · changing metric meaning without INSIGHT sign-off · implying hub exists in Rails while only mockup ships.

---

## 8. Bet E — Portal & Access control plane

**Problem (F10):** 134 toggles across 6 decision layers (39 YAML feature flags, no UI). Every non-trivial portal change is a SuperCat ticket; access rules (`territory_access_via_rep_number`, SERV-2178 class) hide in deploy config.

**Appetite:** Big batch. **Wave 0–1** (delete dead flags + graduate stable flags) is the safe small-batch down-payment.

**Authority chain:** `PORTAL-SETTINGS-CONTROL-PLANE.md` (triage + migration) → this section (build plan) → **`SETTINGS-hub-v1-AC.md` (build Given/When/Then — frozen)** → `SETTINGS-hub-v1-DEMO-SPEC.md` (prototype scope only) → `SHIP-READINESS-bet-e.md` (GO gate).

### 8.1 Target architecture

```
Today (6 layers, no hub)
  Feature YAML (39) · Organization (57) · MobileSite (13)
  · UserType (18) · Permissions (3) · OrgUser (4)
        │
        ▼
Target: "Portal & Access" hub (Admin Console / portal settings route TBD)
  ├─ 1 Enablement          — allow_view_sales_portal? decision tree
  ├─ 2 Territory & access  — customer_synching, totals perm, match mode (SuperCat)
  ├─ 3 Portal display      — currency, qty cols, customer graph (self-service)
  ├─ 4 Reports & export    — unified export permission (consolidate 3–4 toggles)
  ├─ 5 Revenue definitions 🔒 — metric-law org settings (SuperCat + INSIGHT only)
  └─ 6 Experiments         — canary YAML with owner + ticket + sunset date
```

**North star:** ~30 portal-relevant survivors surfaced in one hub; ~18 client self-service; ~6 locked revenue definitions; ~11 sunset-dated YAML in Experiments lab.

**Out of hub (routed elsewhere):** Catalog/pricing toggles → Site settings or existing User-Type ACL UIs. See control-plane Part A bucket rules.

### 8.2 Build layers (when GO arrives)

| Layer | Choice |
|---|---|
| Data model | Graduate flags → labeled Org / MobileSite / UserType columns or JSON settings; YAML read-through shim one release |
| Access tree | Ship in-product copy from `ecat_permissions_helper.rb` + `eol_left_nav_dataflow.rb` (verified in control-plane B.3) |
| Revenue lock | Visible-but-readonly section; changes require SuperCat + INSIGHT workflow + audit log |
| Experiments lab | Superadmin-only; replaces open-ended `enabled_features.rb` allowlists |
| Demo → prod | `sales-portal-internal-demo.html` Portal & Access view is layout/copy reference only until Rails GO |

### 8.3 Sequenced waves (from control-plane Part C — not applied)

| Wave | Work | Risk | Demo badge |
|---|---|---|---|
| **0** | Delete 5 dead flag entries from `enabled_features.rb` (`eol_dashboard_filters`, `tcgc_name_fields`, `allow_user_group_from_selecting_price_levels`, `sales_quotas` flag, `option_mapping` flag) | Low — zero call sites | Wave 0 |
| **1** | Graduate high-usage stable flags (`advanced_reports`, `twenty_option_types`, …) to labeled settings | Med — YAML shim | Wave 1 |
| **2** | Build hub UI: **Enablement + decision tree**, then **Territory & data access** | High — access chain | Wave 2 |
| **3** | Self-service display toggles + export unification | Low | Wave 3 |
| **4** | Consolidate access; `territory_access_via_rep_number` → superadmin **Territory match mode** | **Critical** — pair with Bet A / SERV-2178 | Wave 4 |
| **5** | Stand up locked **Revenue definitions** section + change logging | Metric-law | Wave 5 |

**Cross-lane handoff:** Wave 4 territory match mode ships with Lane-0 filter-truth fix. Wave 5 revenue settings require INSIGHT sign-off before any UI exposes them.

### 8.4 Build acceptance criteria — **frozen**

**Canonical AC:** [`SETTINGS-hub-v1-AC.md`](SETTINGS-hub-v1-AC.md) — AC-E0 (waves/appetite) through AC-E6 (count the win), plus no-gos + verify orgs.  
**Ship gate:** [`SHIP-READINESS-bet-e.md`](SHIP-READINESS-bet-e.md) — status NOT READY TO BUILD until GO.

Do **not** treat the old draft bullets in this section as authority. Summary only:

| ID | One-liner |
|---|---|
| E0 | Wave 0–1 = Small; Wave 2–5 = Big hub; Wave 4 pairs Bet A; Wave 5 = INSIGHT lock |
| E1 | In-product enablement tree (`ecat_permissions_helper` + `eol_left_nav_dataflow`) |
| E2 | ~18 named self-serve survivors |
| E3 | Six revenue defs visible-locked; SuperCat + INSIGHT |
| E4 | Territory match mode superadmin-only; ships with Bet A |
| E5 | Experiments: owner + ticket + sunset |
| E6 | 134/6 → ~1 hub / ~30 / ~18 / sunset YAML |

**Betting-table GO still required** before Rails — AC freeze ≠ isolation lift.

### 8.5 Pre-build gates (Bet E)

| Gate | Status |
|---|---|
| Control-plane triage (134 toggles) | Done — `PORTAL-SETTINGS-CONTROL-PLANE.md` |
| Demo spec + internal mockup | Done — `SETTINGS-hub-v1-DEMO-SPEC.md`, `sales-portal-internal-demo.html` |
| Build AC freeze | **Done** — `SETTINGS-hub-v1-AC.md` |
| `SHIP-READINESS-bet-e.md` | **Done** — NOT READY TO BUILD until GO |
| Confluence 1813676033 row finalize (~47 Org rows) | **Pending** — human; before Wave 2 |
| Dormant-wired flags ship/cut decision (4 flags) | **Pending** — product call |
| Betting table include E | **Pending** — Wave 0–1 may ride with A |
| Isolation lift | **Blocked** — `ISOLATION OFF — GO on Bet E` (or Wave 0 / named SERV path) |

### 8.6 Test plan (pre-build — Bet E)

- [ ] Decision tree copy matches verified Rails chain (`ecat_permissions_helper`, `eol_left_nav_dataflow`)  
- [ ] Wave 0 flag deletes: zero `Feature.enabled?` / `enabled_for_organization?` regressions on orgs that had allowlists  
- [ ] sarreid vs cci backlog-status exclusion renders correctly in locked Revenue definitions (demo parity)  
- [ ] Client self-service toggles do not touch metric-law columns  
- [ ] Territory match mode change requires superadmin + audit log  
- [ ] Hub does not surface catalog/pricing toggles mislabeled as portal settings  

### 8.7 Demo ↔ build traceability (Bet E)

| Hub section | Demo spec | Control-plane | Build wave | Editor |
|---|---|---|---|---|
| Enablement | §3.1 + decision tree | B.2, B.3 | Wave 2 | Client admin (+ SuperCat for force-on) |
| Territory & data access | §3.2 | A.4 `customer_synching`, A.5 perm, A.1 `territory_access_via_rep_number` | Wave 2–4 | SuperCat (match mode) · client (synch/totals) |
| Portal display | §3.3 | A.2–A.3 display rows | Wave 3 | Client self-service |
| Reports & export | §3.4 | A.1 export flags + A.4 `can_export_eol_data` | Wave 2–3 | Client admin |
| Revenue definitions 🔒 | §3.5 | A.2 metric-law org settings | Wave 5 | SuperCat + INSIGHT |
| Experiments | §3.6 | A.1 KEEP-YAML / dormant | Wave 1 + lab | SuperCat superadmin |

**Demo-only (not build AC):** FUTURE/WAVE badges, static sarreid values, non-interactive decision tree — see `SETTINGS-hub-v1-DEMO-SPEC.md` §5.

---

*Technical plan covers Bet A/C shaping + Bet E blueprint. Bet C implementation waits on feedback + isolation lift. Bet E AC is frozen (`SETTINGS-hub-v1-AC.md`); build waits on betting-table GO + `ISOLATION OFF — GO on Bet E`.*
