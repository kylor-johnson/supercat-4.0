# TRD — Bet A: filter truth

**Technical Requirements — Bet A (Lane 0 Trust/Fix) · EBR-40 / 212 / 91**  
**(EBR-87 parked · EBR-7 doctrine close)**

**Status:** `GO 2026-07-24 · ISOLATION OFF — GO on EBR-40 · Ready for SERV / eng · NOT built yet`  
**Owner:** Kylor · **Date:** 2026-07-20 · **Updated:** 2026-07-24  
**Feedback:** `CTO-FEEDBACK-2026-07-20.md` · **`CTO-FEEDBACK-2026-07-24.md`** · **Validation (filled):** `BUG-VALIDATION-PACK.md`  
**Sprint pack:** `SPRINT-PACK-bet-a.md` · **Eng SoT:** `ENG-HANDOFF-bet-a-b-c-e.md`

> ## GO = Bet A only — scope locked by validation · **LIFTED 2026-07-24**.
> Verbatim: `ISOLATION OFF — GO on EBR-40`.  
> **In GO:** EBR-40 + EBR-212 (paired) + EBR-91 (period drift / AC-A2 rewrite) + close EBR-7.  
> **Parked:** EBR-87 (no dedicated build).  
> **Not in this GO:** Intelligence (EBR-775), Settings hub (Bet E), Dashboard redesign, LLM.

---

## Assumptions — verified 2026-07-21

| Assumption | Result |
|---|---|
| EBR-40 still valid | **Yes** — wwjc `cmallon` YTD 1,404 / $1.46M → T1 `105:1 Gigi Lane` 710 / $777k |
| EBR-212 still valid | **Partial** — same filter stack; wwjc multi-terr reps lack dashboard (Office/SuperCat all-totals). Keep paired. |
| EBR-91 still valid | **Yes — period drift** (SERV-2395). CY/LY ignore dropdown; selected-range export only for `previous_ytd`/`custom`. Rewrite AC-A2. |
| EBR-87 universal “quotes as sales” | **No** — park. Only `cci`/`ril` have quotes; both backlog-excluded. `kal` has zero quote orders. |
| wwjc = trust flagship | **Confirmed** (not a synonym for zero-exposure) |

Method: production SQL + live Rails code. Optional UI: `cmallon` → Invoices → Current YTD → `105:1 Gigi Lane` → ~710 / ~$777k.

---

## 1. Executive summary

A rep opens the Sales Portal, picks their territory, and cannot trust that the list and total are their book. Separately, on Customers, the date dropdown and export do not share one period definition with the on-screen sales number — so Excel still disagrees with the portal. Validation parked the old “quotes inflate sales” story as a universal build: invoiced sales is `net_amount`, and the two orgs with quote statuses already exclude them from backlog.

**Appetite:** small batch — fixed time, variable scope. Trust fix, not a territory data-model rewrite.

**Done means:** on **wwjc** (trust flagship), picking a territory limits invoice list rows and totals to that territory’s customers; Customers selected-range total and export use the same period; every total labeled sales is invoiced net. Dashboard territory control stays in AC when the surface is enabled for the user.

## 2. Problem & baseline

**Authority:** `PITCH-phase1-filter-metric-law.md` · **Evidence:** `BUG-VALIDATION-PACK.md`.

EBR-40 (invoice list) and EBR-212 (dashboard) are one mechanism on two surfaces. EBR-91 is period/export drift on Customers (not an empty “needs definition” forever — AC rewritten). EBR-87 is parked.

## 3. Scope — in

| Element | EBR | Outcome |
|---|---|---|
| Territory limits the invoice list (+ dashboard when enabled) | 40, 212 | List and total scope to that territory’s customers |
| Customers period + export reconcile | 91 | Selected-range UI total = export column for same range |
| One invoiced spine (metric law) | A4, closes 7 | Every “sales” total is invoiced net |
| Answer-first list tabs | Bet B shell | May ride later — not the GO proof story (`IA-PERSONA-TRACK.md`) |

## 4. Scope — out

- **EBR-87 dedicated build** — parked; metric-law copy only  
- **Multi-territory rep rewrite** (EBR-180 / XL)  
- **Intelligence / LLM / Settings hub / Dashboard redesign**  
- **iPad tickets**  
- **"What's broken"** as shipping product navigation  
- Claiming territory truth on **sarreid** until SERV-2196-class is honest  

## 5. Metric law (immutable)

- **Sales = invoiced net** (`SUM(portal_invoices.net_amount)`), RTD-clamped, $5M single-row cap  
- **Confidence ceiling STRONG**  
- **Quotes ≠ sales** — spine/copy only; no EBR-87 build  
- **Export equals the screen** for the **same period** (AC-A2)  
- **Backlog is not sales**  
- **EBR-7** — close via `net_amount`; don’t rebuild  

## 6. Acceptance criteria summary

Full Given/When/Then: `FILTER-TRUTH-AC.md` (updated 2026-07-21).

- **AC-A1** — territory limits list and total (invoice primary; dashboard when enabled)  
- **AC-A2** — Customers selected-range + export period alignment (SERV-2395 class)  
- **AC-A3** — parked (EBR-87)  
- **AC-A4** — invoiced spine + close EBR-7  

## 7. Solution elements (breadboard level)

Rep path: **select territory → invoiced total and rows recompute together → export matches that scope/period.** Teaching control (“simulate today’s filter bug”) stays demo-only.

## 8. Rabbit holes & patches

| Risk | Patch |
|---|---|
| sarreid multi-territory over-grant | Verify on **wwjc**; don’t claim sarreid territory truth until 2196-class honest |
| Ship-to bridge case mismatch | Still in code — include with Bet A / immediately after |
| wwjc reps without dashboard | Keep A1.2; verify on Office/SuperCat or enable dash on a rep |
| EBR-87 revival pressure | Point at validation pack — config already handles cci/ril backlog |

## 9. Verify orgs & sequencing

**wwjc is the trust flagship.** Zero-exposure orgs remain an *alternative* verify target, not a synonym. Eng order after GO: fail-closed leakage guard → ship-to case / over-grant → Customers date-aware selected-range + export (AC-A2).

## 10. Demo / readout artifacts

- **Primary for CTO:** filled `BUG-VALIDATION-PACK.md` + `DRAFT-CTO-REPLY-validation.md`  
- **Optional UI:** pitch demo or live `cmallon` click — not a Dashboard/Intelligence walk  
- Internal full demo stays off the default path for this decision  

## 11. Implementation (GO lifted)

**GO phrase recorded 2026-07-24:** `ISOLATION OFF — GO on EBR-40`

SoT: `ENG-HANDOFF-bet-a-b-c-e.md` §C + `cycle-01-outputs/FIX-diagnosis-territory-datefilter.md` (include SERV-2395 Customers path for AC-A2). Sprint board handoff: `SPRINT-PACK-bet-a.md`.

Rails may proceed against keep EBRs / linked SERV stories. Do not expand into Bet C/E/F without a separate GO.

## 12. Done means

- Territory limits invoice list (+ dashboard when enabled) on wwjc (AC-A1)  
- Customers selected-range total = export for same period (AC-A2)  
- Every sales total is invoiced net; EBR-7 closed by doctrine (AC-A4)  
- EBR-87 not required for done  

## 13. Decisions closed (CTO 2026-07-24)

1. **GO on Bet A** — yes; keep 40 + 91 (+ 212 paired), park 87, close 7.  
2. **Verify org** — wwjc.  
3. **Customers date-filter** — in this bet (EBR-91 / AC-A2).  
4. **Settings Wave 0** — triage separately (`BET-TRIAGE-BOARD.md`); not required for Bet A done.  

---

*Decision record for Bet A. GO lifted 2026-07-24. Program context: `PROGRAM-ROADMAP-cycle03.md`. AC: `FILTER-TRUTH-AC.md`.*
