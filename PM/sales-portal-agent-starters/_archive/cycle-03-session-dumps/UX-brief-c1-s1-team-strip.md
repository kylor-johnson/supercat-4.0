# UX / Lane 1 — C1 + S1 + Team strip (Bet B, cycle-03)

**Date:** 2026-07-17 · **Cycle-03 update:** 2026-07-17 (internal demo expanded; Bet E added to scope) · **Isolation:** ON — mockup/AC only  
**Supersedes cycle-01 heroes for program AC:** Concentration demoted; S1 (EBR-198) preferred as second commerce hero; team strip added (reboot §2.1).  
**Mockups (mockup-only, 2026-07-17):**
- **Customer feedback →** [`design-system/app/sales-portal-cycle03-mockup.html`](../../../design-system/app/sales-portal-cycle03-mockup.html) — C1 + S1 + team strip, lightweight wireframe rail (answer-first; low "is this built?" risk).
- **Internal show-and-tell (PRIMARY) →** [`design-system/app/sales-portal-internal-demo.html`](../../../design-system/app/sales-portal-internal-demo.html) — default **Dashboard**; Customers/Orders/Invoices/Reports are **answer-first list tabs** (large hero totals, export=UI, quotes demoted) at Dashboard density spirit — not stub tables and not Intelligence heroes copied onto every tab. **Intelligence** live-stamped; **What’s broken** last (plain-English sim). Settings hub Later. Contract: `DEMO-SURFACE-CONTRACT.md` · AC: `LIST-TABS-AC.md`.
- **Cycle-03 chrome (Intelligence-only) →** [`design-system/app/sales-portal-cycle03-chrome.html`](../../../design-system/app/sales-portal-cycle03-chrome.html) — Intelligence view only on shared shell. Remains valid for customer feedback sessions (low "is this built?" risk). Do not retire.
- Legacy: `sales-portal-cycle01-mockup.html` (concentration hero — superseded for Bet B/C).

**Bet E (Portal & Access) is in internal demo scope.** The `sales-portal-internal-demo.html` "Portal & Access" view demonstrates the 6-section settings hub (Enablement, Territory & data access, Portal display, Reports & export, Revenue definitions [locked], Experiments) grounded in live sarreid config. See `cycle-03-outputs/SETTINGS-hub-v1-DEMO-SPEC.md` for full spec.

---

## List-tab density bar (Bet B shell)

List tabs must sit next to Dashboard without feeling empty: one primary answer per tab (Invoices = invoiced-for-filters; Customers = selected-range sales; Orders = confirmed vs quotes; Reports = invoiced net = C1). Match Dashboard’s *density spirit* (filters + KPI + dense table), not the Intelligence hero grid. Territory $ on lists stays illustrative; Intelligence stamps stay authority. See `DEMO-PORTAL-DENSITY-AUDIT.md` for Dashboard fidelity and `LIST-TABS-AC.md` for shipping Given/When/Then.

## Composition (one job per panel)

| Panel | Question | Query / law | Travel |
|---|---|---|---|
| **Hero 1 — True Topline** | What did we actually sell? | C1 · `SUM(portal_invoices.net_amount)` RTD + $5M · STRONG | 55/55 |
| **Hero 2 — Quietly dying (S1)** | Which accounts are fading, worth how much? | S1 / EBR-198 · equal 6mo windows · `selling_customer_exception_layer` | Wide; rep name degrades to `rep_number` |
| **Team strip** | Who’s active / writing / quiet? | Q-R1 pulse always · Q-18 eCat GMV leaderboard **or** Q-01 engagement fallback · Mixpanel Q-63/64/65 if corroborated | ERP-optional; includes Tier-0 |
| **Optional degrade** | Concentration | C3 with “healthy diversification” when top1 &lt; 20% | Org-specific |

**Do not lead with** RS-01 / named invoiced-rep revenue (Universe E).

---

## Demo orgs

| Org | Why |
|---|---|
| `sarreid` | Dense demo; concentrated if C3 shown |
| `cci` or `ufi` | Opposite shape / Tier-0 behavior-only proof |

Avoid territory-scoped demo claims until Bet A filter truth is honest — or use a zero-exposure org.

---

## Feedback session

**Full facilitator script:** [`FEEDBACK-SESSION-SCRIPT.md`](FEEDBACK-SESSION-SCRIPT.md) (35–45 min, invite blurb + note sheet).

Questions (summary):
1. Is invoiced trailing-12 the number you trust as the hero default?  
2. Does “quietly dying accounts” (S1) beat “single-account concentration” as the second answer for your book?  
3. Is a behavior team strip (logins / eCat activity) useful when we **cannot** name invoiced-rep revenue (ufi/kll)?  
4. Masked vs real names on S1 / concentration lists for QBR screenshots?  
5. One follow-up after S1 — products, cadence, or who to call?  
6. Does App kit feel like an upgrade over classic portal?

**Feedback session status:** Script ready; session not yet run — update AC table below after the session.

### Post-feedback AC updates (fill after session)
| # | Decision | Date |
|---|---|---|
| — | *pending session* | — |

---

## Draft AC (overlay / eventual Rails — isolation ON)

- True Topline shows invoiced net for selected org + range; matches IR v1 reconciliation SQL.  
- Range change recomputes **all** heroes + team strip.  
- S1 lists decaying accounts with $-at-risk; suppresses or labels when commerce confidence NONE.  
- Team strip always renders Q-R1; leaderboard uses Q-18 when eCat orders exist, else Q-01 engagement.  
- Named invoiced-rep revenue **absent** from v1 default.  
- Feature-flagged portal-only layout; App kit tokens; no catalog paint.  
- No EBR-772 / talk-to-data.

## No-gos

- Leading with RS-01 · LLM · Phase-3 Rails without GO · iPad surfaces · fake placeholder metrics  

## Cross-lane

Depends on Bet A metric law (EBR-91/87) and filter honesty (EBR-40/212). Shares heroes with `INSIGHT-IR-v1-AC.md`.

---

*Cycle-03 UX brief. Cycle-01 wireframe remains valid chrome; content contract above is authoritative for Bet B/C.*
