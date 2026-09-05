# Sprint pack — Bet A Filter Truth (EBR → SERV)

**Date:** 2026-07-24 · **GO:** `ISOLATION OFF — GO on EBR-40`  
**CTO:** `CTO-FEEDBACK-2026-07-24.md` · **AC:** `FILTER-TRUTH-AC.md` · **Eng SoT:** `ENG-HANDOFF-bet-a-b-c-e.md` §C  
**Verify org:** **wwjc** · Proof user: `cmallon` · T1: `105:1 Gigi Lane`

---

## 1. Story split (bug-heavy)

| # | Program key | SERV implementation | Type | AC | Disposition |
|---|---|---|---|---|---|
| 1 | [EBR-40](https://supercatsolutions.atlassian.net/browse/EBR-40) | New SERV — invoice list territory filter | Bug | A1.1, A1.3, A1.4 | **Keep — build** |
| 2 | [EBR-212](https://supercatsolutions.atlassian.net/browse/EBR-212) | New SERV — dashboard territory (when enabled) | Bug | A1.2 | **Keep — paired with 40** |
| 3 | [EBR-91](https://supercatsolutions.atlassian.net/browse/EBR-91) | New SERV — Customers period/export drift | Bug | A2.1–A2.4 | **Keep — build** |
| 4 | [EBR-7](https://supercatsolutions.atlassian.net/browse/EBR-7) | None | Doctrine close | A4 | **Close after metric law accepted — no rebuild** |
| 5 | [EBR-87](https://supercatsolutions.atlassian.net/browse/EBR-87) | None | Park | A3 | **Park — no dedicated build** |

**Do not reuse as Bet A core:**

| Existing SERV | Why not |
|---|---|
| SERV-2178 / 2180 | EBR-180 XL comma-RepNumber — separate appetite |
| SERV-2196 | Ship-to over-grant — include with/after Bet A; not a substitute for EBR-40 |
| SERV-2395 | **iPad** Customer Dashboard date blocks (fsf) — same *class* as A2, different product surface |

---

## 2. SERV bodies (apply to Jira)

### SERV ← EBR-40 — Invoice list territory filter

**Summary:** Sales Portal invoice list territory filter does not scope rows + total (Bet A / EBR-40)

**Description:**

```markdown
## Bet A / EBR-40 — Invoice list territory filter

**Program:** Sales Analytics · `ISOLATION OFF — GO on EBR-40` (2026-07-24)  
**Program key:** EBR-40  
**AC:** FILTER-TRUTH-AC AC-A1.1 / A1.3 / A1.4  
**Eng SoT:** ENG-HANDOFF-bet-a-b-c-e.md §C.1  
**Verify:** wwjc · `cmallon` · Current YTD · territory `105:1 Gigi Lane`

### Problem (current)

Picking a territory on Sales Portal **Invoices** does not reliably limit both invoice rows and the invoiced total to that territory’s book.

### Acceptance

* A1.1 — Rep with `[T1,T2]` selects **T1** → only T1 rows; total = `SUM(net_amount)` for that scope
* A1.3 — **All territories** → union of assigned only (not whole org), unless user-type has all-customer totals
* A1.4 — Empty `territory_codes` + no all-totals → fail-closed empty book, never full org

### Evidence (2026-07-21)

wwjc `cmallon` YTD bill-to book ~1,404 / $1.46M → T1 `105:1 Gigi Lane` ~710 / $777k.

### Diagnosis pointers

* `warehouse_access.rb` ~424–434 — `territory_code_limit_subquery` / empty keys + all-totals leak
* Portal reads warehouse `territory_keys` CTE, not live `org_users.territory_codes`
* Pair with EBR-212 (same mechanism, dashboard surface)

### Out of scope

EBR-180 / SERV-2178 XL · Intelligence · Dashboard redesign · dedicated EBR-87 build
```

### SERV ← EBR-212 — Dashboard territory filter

**Summary:** Sales Portal dashboard territory filter should match invoice list scope (Bet A / EBR-212)

**Description:**

```markdown
## Bet A / EBR-212 — Dashboard territory (paired with EBR-40)

**Program:** Sales Analytics · GO on EBR-40  
**Program key:** EBR-212  
**AC:** FILTER-TRUTH-AC A1.2  
**Eng SoT:** ENG-HANDOFF-bet-a-b-c-e.md §C.1  
**Verify:** wwjc — use Office/SuperCat or dash-enabled multi-terr rep (cmallon often has dashboard off)

### Problem (current)

Same territory-filter mechanism as invoice list should scope dashboard invoiced KPIs + territory-scoped Top-N when dashboard is enabled. Not a separate big bet.

### Acceptance

* A1.2 — Select **T1** on dashboard (when enabled) → invoiced KPI + top-N use T1 scope, not org-wide
* Ships with EBR-40 / AC-A1 — do not score UI polish

### Out of scope

Dashboard redesign / Baby BI expansion · Intelligence · EBR-180
```

### SERV ← EBR-91 — Customers period / export drift

**Summary:** Customers selected-range total and export must share one period (Bet A / EBR-91)

**Description:**

```markdown
## Bet A / EBR-91 — Customers period + export reconcile

**Program:** Sales Analytics · GO on EBR-40  
**Program key:** EBR-91  
**AC:** FILTER-TRUTH-AC AC-A2  
**Eng SoT:** ENG-HANDOFF-bet-a-b-c-e.md §C.2  
**Verify:** wwjc (trust); sarreid OK for export math  
**Related class (not this ticket):** SERV-2395 = iPad Customer Dashboard — do not conflate

### Problem (current)

On eOL Sales Portal **Customers**, CY/LY blocks ignore the date dropdown; selected-range export column only appears for `previous_ytd` / `custom`. UI period and export drift.

### Acceptance

* A2.1 — Any standard `date_range` shows a **selected-range** invoiced total via `Eol::DateRanges`
* A2.2 — Export CSV sales column for that same range; SUM = on-screen selected-range total (± rounding)
* A2.3 — Spine = `SUM(portal_invoices.net_amount)`
* A2.4 — Fix is period/scope alignment, not a second revenue definition

### Diagnosis pointers

* `ecat_customers_controller.rb` ~294 — substring gate on `previous_ytd`/`custom`
* `ecat_customer.rb` ~113–122 — hardcoded CY/LY ranges ignore `params[:date_range]`

### Out of scope

EBR-7 discount rebuild · inventing new revenue definitions · iPad SERV-2395 as the same ticket
```

---

## 3. Link map (applied 2026-07-24)

| EBR | Link type | SERV | Notes |
|---|---|---|---|
| EBR-40 | Relates | [SERV-2447](https://supercatsolutions.atlassian.net/browse/SERV-2447) | Primary keep · sprint **June 2026** (active board 3) · EBR → Approved |
| EBR-212 | Relates | [SERV-2448](https://supercatsolutions.atlassian.net/browse/SERV-2448) | Paired · sprint June 2026 · EBR already In Progress |
| EBR-91 | Relates | [SERV-2449](https://supercatsolutions.atlassian.net/browse/SERV-2449) | Period drift · sprint June 2026 · EBR → Approved |
| EBR-40 | Relates | EBR-212 | Pair link created |
| — | Footnote only | SERV-2196 | Ship-to case — with/after A |
| — | XL shelf | SERV-2178 | Not Bet A GO |
| — | iPad class | SERV-2395 | Not eOL Customers A2 |

---

## 4. Eng order (after SERV pickup)

1. Fail-closed empty-territory leakage (`warehouse_access` path) — A1.4  
2. Invoice list territory scope + totals — A1.1 / A1.3  
3. Ship-to bridge case / over-grant if in batch — SERV-2196 class  
4. Dashboard territory when enabled — A1.2  
5. Customers selected-range + export — A2  

Verify on **wwjc** before claiming done. Do not claim territory truth on **sarreid** until 2196-class is honest.

---

## 5. Hygiene (PM only — no Jira comments)

| Ticket | Recommended later (needs Kylor OK) |
|---|---|
| EBR-7 | Transition Done / Won’t Do after metric law accepted |
| EBR-87 | Leave Triaging or Park label — no build |

---

*Sprint handoff for Bet A. SERV-2447/2448/2449 created, linked, and added to active SERV sprint. No hygiene comments posted.*
