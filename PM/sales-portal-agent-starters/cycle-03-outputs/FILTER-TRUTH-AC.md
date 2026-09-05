# Bet A — Filter + metric law AC (EBR-40 / 212 / 91)

> **Engineering source of truth moved to Confluence (2026-07-28).** SERV tickets and
> eng cite the Confluence page, which carries this content plus the PO decisions block:
> EOL › eCat Online Sales Portal › **Bet A — Filter Truth AC (EBR-40 / EBR-212 / EBR-91)**.
> Keep this file as the PM working copy; if the two ever disagree, Confluence wins.

**Date:** 2026-07-17 · **Validated:** 2026-07-21 · **GO:** 2026-07-24 (`ISOLATION OFF — GO on EBR-40`) · **Lane:** 0 Trust/Fix  
**Pitch:** `PITCH-phase1-filter-metric-law.md`  
**Validation:** `BUG-VALIDATION-PACK.md` (filled)  
**Eng footnotes (not program keys):** SERV-2178 / 2196 / 2395 — see cycle-01 `FIX-diagnosis-territory-datefilter.md`  
**Shelf:** EBR-180 (XL) · **Parked:** EBR-87 (no dedicated build) · **Close (doctrine):** EBR-7 (`net_amount`)

---

## Problem (one mechanism)

Rep/CSM picks a **territory** on Sales Portal **invoice list** (EBR-40) or **dashboard** (EBR-212) and the book is wrong (all / none / other territories). Separately, Customers export / date blocks drift from the on-screen period (EBR-91 / SERV-2395-class).

**2026-07-21 validation:** EBR-40 still real on wwjc; EBR-212 same mechanism (partial surface — wwjc multi-terr reps lack dashboard); EBR-91 still real as **period drift**; EBR-87 **parked** (not universal — only `cci`/`ril` have quote statuses, both already backlog-excluded).

**Done for this bet** = filters scope the book + every total on that surface; “sales” = invoiced `net_amount`; Customers UI period, selected-range total, and export use one period definition.

---

## AC-A1 — Territory filter scopes the book (EBR-40 + EBR-212)

| # | Given | When | Then |
|---|---|---|---|
| A1.1 | Portal rep with assigned territories `[T1,T2]`, warehouse ETL current | Selects **T1** on **invoice list** | Only invoice rows for customers in T1; invoice total = `SUM(net_amount)` for that scope |
| A1.2 | Same filter stack on **dashboard** (when dashboard enabled for that user) | Selects **T1** | Invoiced KPI + top-N panels use the same T1 scope (not org-wide). *Note (wwjc 2026-07-21): multi-terr reps may lack dashboard; Office/SuperCat often have all-totals — verify on a dash-enabled path, not only cmallon.* |
| A1.3 | Same rep | Selects **All territories** | Book = union of assigned territories only (not whole org), unless user-type has all-customer totals |
| A1.4 | Portal-enabled rep with **empty** `territory_codes` and **not** authorized for all-customer totals | Opens Customers / Invoices / Dashboard | **Fail-closed:** empty book + clear empty-state — never full org |
| A1.5 | Org with empty `territories` master (32/55 today) | Opens territory filter | No promise of named rollups; filter still must not silently show whole org to unterritoried reps |

**Surfaces in scope:** invoice list (primary), dashboard territory control when enabled, and any summary tiles driven by that filter.  
**Out of scope:** EBR-180 multi-territory RepNumber rewrite; iPad shared drafts / order-email CC.

**Evidence (2026-07-21):** wwjc `cmallon` YTD bill-to book **1,404 / $1.46M** → T1 `105:1 Gigi Lane` **710 / $777k**. Org remains trust flagship (multi-terr + comma-rep). Kalco Ferguson/`0016` URLs stale (bill-to is `0999`). Ship-to bridge case bug still in code.

**Diagnosis handoff (Rails, read-only today):** portal scopes via warehouse `territory_keys` CTE (`WarehouseAccess`), not live `org_users.territory_codes`. Empty keys + all-totals permission → whole-org leak. Ship-to over-grant (bill-to OR ship-to match) is the SERV-2196 class — fix with Bet A or immediately after; do not demo territory scoping on sarreid (99.8% multi-territory bill-tos) until that path is honest.

---

## AC-A2 — Export / period reconciles to UI (EBR-91) — rewritten 2026-07-21

Ticket text is empty (“Needs definition”). AC is defined by live repro, not Jira.

**Root class:** **period drift** (SERV-2395), not a second sales definition. Customers CY/LY blocks ignore the date dropdown; selected-range export column only appears for `previous_ytd` / `custom` (substring gate).

| # | Given | When | Then |
|---|---|---|---|
| A2.1 | Customers page, any standard date_range (incl. `current_ytd`, `current_mtd`, etc.) | User views the page | A **selected-range** invoiced total is visible and uses `Eol::DateRanges` for that selection — not only CY/LY fixed anchors |
| A2.2 | Same view as A2.1 | User exports Customers CSV | Export includes a sales column for **that same selected range**; SUM equals the on-screen selected-range total (± rounding) |
| A2.3 | Spine | — | Selected-range UI + export use `SUM(portal_invoices.net_amount)`; CY/LY blocks stay labeled as calendar anchors if kept |
| A2.4 | Mismatch found | — | Fix is **period/scope alignment** (gate + endpoint), not “add a second number” |

**Out of AC-A2:** inventing a new revenue definition; changing CY/LY semantics for row columns without an explicit product call.

---

## AC-A3 — Quotes never in sales (EBR-87) — PARKED

> **Validated 2026-07-21:** Not a universal Bet A build. Quote statuses live only on `cci` (`Q`) and `ril` (`Quote`); both already exclude those from backlog via `excluded_portal_order_backlog_order_statuses`. `kal` has **zero** quote portal orders today. Invoiced sales is `portal_invoices.net_amount` — quotes do not land there.

| # | Given | When | Then |
|---|---|---|---|
| A3.1 | — | — | **No dedicated EBR-87 build in Bet A GO** |
| A3.2 | Metric-law copy | Any figure labeled sales / invoiced | Remains invoiced `net_amount` only (AC-A4) |
| A3.3 | Backlog | Org config | May exclude quote statuses; backlog labeled backlog, never sales |

Optional later: Orders-list UX clarity for `cci`/`ril` — not this GO.

---

## AC-A4 — Metric law stubs (feeds Bet C)

Locked for every hero and every portal total labeled sales:

- Revenue = `SUM(portal_invoices.net_amount)`, RTD-clamped, $5M single-row cap  
- Confidence ceiling **STRONG** (single feed); never FULL  
- Quotes ≠ sales (copy / spine only — EBR-87 parked as a build)  
- EBR-7: discounts already in `net_amount` — **close ticket, don’t rebuild** (wwjc YTD: net_amount present, total_amount null)  
- Warehouse dashboard rollups are **not** validation ground truth — label “invoiced ledger”

---

## No-gos

- Starting EBR-180 / comma-RepNumber schema without separate GO  
- New IR heroes inside this bet  
- LLM / EBR-772/776  
- iPad tickets  
- Dedicated EBR-87 quote-exclusion build (parked)  
- Expanding scope into Bet C / E / F / EBR-180 without a separate GO  

---

## Verify (pre-build checklist)

- [x] A1.1 expected book on wwjc (`cmallon` → T1 `105:1 Gigi Lane`) — SQL 2026-07-21; optional UI confirm  
- [ ] A1.2 dashboard path on a dash-enabled user (Office/SuperCat or enable dash on a rep)  
- [x] A2 period-drift class confirmed in code (SERV-2395) — fix still to ship  
- [x] A3 parked with evidence  
- [x] A4 / EBR-7 doctrine holds on wwjc  

**Build only after:** `ISOLATION OFF — GO on EBR-40` (or EBR-212 / named path).

---

*Validation: `BUG-VALIDATION-PACK.md`. Companion: `TECHNICAL-PLAN.md` §3 · cycle-01 FIX diagnosis (SERV footnotes).*
