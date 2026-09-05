# ENG HANDOFF — Bet A (+ B shell / C / E shaped, not this GO)

**Date:** 2026-07-18 · **Restored / updated:** 2026-07-24  
**GO (Bet A only):** `ISOLATION OFF — GO on EBR-40`  
**Sprint pack:** `SPRINT-PACK-bet-a.md` · **AC:** `FILTER-TRUTH-AC.md` · **Diagnosis detail:** `../cycle-01-outputs/FIX-diagnosis-territory-datefilter.md`

> **This file is the eng implementation SoT.** Architecture companion: `TECHNICAL-PLAN.md`. Where they disagree, this handoff wins.

---

## A. Scope / GO gates

| Bet | GO phrase | Status 2026-07-24 |
|---|---|---|
| **A** Filter truth | `ISOLATION OFF — GO on EBR-40` | **GO — build** |
| **B** List-tab shell | rides with A (proof surfaces) | Shaped — `LIST-TABS-AC.md` · optional polish, not GO proof |
| **C** IR v1 | `ISOLATION OFF — GO on EBR-775` | **Not this GO** — shaped only |
| **E** Settings hub | `ISOLATION OFF — GO on Bet E` | **Not this GO** — shaped only |
| **D** LLM | none | Parked |
| **F** Persona IA | none | Parallel research — no Rails |

**In Bet A GO:** EBR-40 + EBR-212 + EBR-91 · doctrine close EBR-7 · park EBR-87.  
**Out:** EBR-180 / SERV-2178 XL · Intelligence · Settings hub Waves 2+ · LLM · iPad SERV-2395 as the A2 ticket.

---

## B. Verify orgs

| Role | Org | Notes |
|---|---|---|
| **Trust flagship** | `wwjc` | Multi-terr + comma-rep intersection |
| Proof user | `cmallon` | YTD → T1 `105:1 Gigi Lane` ~710 / ~$777k |
| Dashboard path | wwjc Office/SuperCat or temp-enable dash | Multi-terr reps often `enable_portal_dashboard=false` |
| Avoid for territory demo | `sarreid` | 99.8% multi-territory bill-tos until SERV-2196-class honest |

---

## C. Bet A — AC → code map (BUILD THIS)

### C.1 Territory filter (EBR-40 + EBR-212) — AC-A1

| AC | Intent | Code locus | Fix direction |
|---|---|---|---|
| A1.1 | Invoice list T1 scopes rows + `SUM(net_amount)` | Portal invoice list → warehouse access CTE | Ensure selected territory filters `customer_key`/`ship_to_key` set used by list **and** total |
| A1.2 | Dashboard same scope when enabled | `Dashboard#invoice_total` → `sales_facts_for_invoices` with `territory_codes` | Same filter stack as list; verify on dash-enabled user |
| A1.3 | “All territories” = union of assigned | Same CTE | Not whole org unless all-totals permission |
| A1.4 | Empty territories → fail-closed | `app/models/warehouse_access.rb` **~424–434** `territory_code_limit_subquery` | When rep-type resolves empty keys and **not** `may_access_all_customer_sales_totals?`, return NONE — never leak full org |

**Architecture (do not rediscover):**

- Live assignment: `org_users.territory_codes` (`OrgUser#set_territory_codes`)
- Portal reads **warehouse** projection: `rep_to_territory_bridge` → `territory_keys` CTE (`warehouse_access.rb` ~1040), **not** live column
- Shared CTE powers customers / orders / invoices / reports — changes are org-wide across portal surfaces
- Prefer controller/query/service fixes over shared `ecat` layout partials (catalog coupling)

**Include with / immediately after A1:**

| Class | Locus | Fix |
|---|---|---|
| Ship-to bridge case mismatch | `territory_to_ship_to_bridge.rb` **:25** vs **:37–39** | Downcase map keys to match `format_territory_key` |
| Dual-path over-grant (SERV-2196) | `warehouse_access.rb` ~1048–1055 | Flag-gated ship-to-only model; default preserve bill-to OR ship-to |

### C.2 Customers period + export (EBR-91) — AC-A2

| AC | Intent | Code locus | Fix direction |
|---|---|---|---|
| A2.1 | Selected-range total for **any** standard `date_range` | `ecat_customers_controller.rb` **~294** (`show_custom_totals_by_bill_to?`) | Replace substring gate with explicit membership (or always show selected-range block) |
| A2.1 | Range math | `app/services/controllers/ecat_customer.rb` **~113–122** | CY/LY stay fixed anchors; add date-aware path via `Eol::DateRanges` |
| A2.2 | Export column for same range | Customers CSV export path | Selected-range column for all ranges that show the UI block; SUM = on-screen |
| A2.3–A2.4 | Spine | warehouse `invoice_totals_by_bill_to_for_date_range` → `net_amount` | Period alignment only — no second revenue definition |

**Not this ticket:** SERV-2395 (iPad Customer Dashboard on fsf) — same *class*, different surface.

### C.3 Metric law / park / close — AC-A3 / A4

| Item | Action |
|---|---|
| Sales = `SUM(portal_invoices.net_amount)` | Enforce in labels + totals touched by A1/A2 |
| EBR-87 | **No build** — park; cci/ril already backlog-exclude quotes |
| EBR-7 | **Close by doctrine** after A4 accepted — do not rebuild discount plumbing |

### C.4 Suggested PR batches

1. Fail-closed empty territory (A1.4) + tests  
2. Invoice list territory scope + totals (A1.1 / A1.3)  
3. Ship-to case fix (+ optional 2196 flag)  
4. Dashboard territory (A1.2)  
5. Customers selected-range + export (A2)  

### C.5 Test plan (Bet A)

- [ ] A1.1 wwjc `cmallon` → T1 book matches SQL baseline (~710 / ~$777k YTD)  
- [ ] A1.2 dashboard path on dash-enabled user  
- [ ] A1.3 All territories = assigned union  
- [ ] A1.4 unterritoried rep fail-closed  
- [ ] A2.1–A2.2 selected-range UI = export  
- [ ] A4 every “sales” total = invoiced net  

---

## D. Bet B — list tabs (shaped / rides with A — NOT GO proof)

**Cite:** `LIST-TABS-AC.md` · `DEMO-SURFACE-CONTRACT.md`

Answer-first heroes on Invoices / Customers / Orders / Reports may ship as the proof shell for filter truth. **Do not** expand Bet A into Dashboard redesign or What’s-broken as shipping nav. Persona ordering (Bet F) is footnote only.

---

## E. Bet C — IR v1 (NOT THIS GO)

**Cite:** `INSIGHT-IR-v1-AC.md` · `IR-v1-QUERIES.md` · `SHIP-READINESS-bet-c.md`  
**GO required:** `ISOLATION OFF — GO on EBR-775`  
**Gate before build:** re-stamp queries on **cci + kll**.

### E.1 Heroes (summary)

C1 True Topline · S1 accounts fading (EBR-198) · Team strip (Q-R1 + Q-18|Q-01) · optional concentration degrade · provenance stamps AC-5.

### E.2 JSON read-model (build-time when GO)

`org_id` → heroes + provenance `{confidence, feed_completeness, total_business_source, report_through_date}`.

### E.3 Mixpanel degrade

Depth renders only when Mixpanel status **CORROBORATED**; else degrade (NONE → PRESENT → CORROBORATED). Map is build-time data task.

---

## F. Bet E — Settings hub (NOT THIS GO)

**Cite:** `SETTINGS-hub-v1-AC.md` · `SHIP-READINESS-bet-e.md` · `PORTAL-SETTINGS-CONTROL-PLANE.md`  
**GO required:** `ISOLATION OFF — GO on Bet E` (or Wave 0)  
Wave 4 territory match mode **pairs with Bet A** — never ships alone. Wave 0–1 optional ride is a human call (`BET-TRIAGE-BOARD.md`).

---

## G. Explicit no-gos

Rails for C/E/F without GO · EBR-772/776 · EBR-180 XL as Bet A · iPad tickets as program keys · hygiene spam on EBR tickets · claiming sarreid territory truth early

---

*Eng entrypoint restored 2026-07-24. Bet A §C is the only build authorization under current GO.*
