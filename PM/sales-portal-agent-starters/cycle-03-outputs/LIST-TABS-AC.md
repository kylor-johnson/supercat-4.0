# List tabs AC — Bet A + Bet B shell (Customers / Orders / Invoices / Reports)

**Date:** 2026-07-17 · **Isolation:** ON (spec + mockup only)  
**Implements in demo:** `design-system/app/sales-portal-internal-demo.html`  
**Contract:** `DEMO-SURFACE-CONTRACT.md` · **Bet A law:** `FILTER-TRUTH-AC.md` · **S1 stamps:** `IR-v1-QUERIES.md`

This is what eng implements after `ISOLATION OFF — GO` — not demo chrome.  
What’s broken is a **non-shipping teaching surface**; behaviors must exist on these tabs.

---

## Metric law (restated)

- Sales / invoiced = `SUM(portal_invoices.net_amount)`, RTD-clamped, $5M cap, STRONG  
- Quotes ≠ sales · Export = UI · EBR-7 = `net_amount` (close, don’t rebuild)  
- Backlog ≠ sales  
- No RS-01 lead · no EBR-772/776 · no FULL completeness  

---

## LT-INV — Invoices (Bet A home · EBR-40)

| # | Given | When | Then |
|---|---|---|---|
| LT-INV.1 | Portal rep with territory grants; invoice feed current | Opens Invoices with default Fixed path | Hero shows **Invoiced total for current filters** = `SUM(net_amount)` for range + territory; not a meek strip |
| LT-INV.2 | Same | Changes **territory** | Hero total **and** visible row set both change to that territory’s book |
| LT-INV.3 | Same | Changes **date range** | Hero total and row scope recompute for the new window |
| LT-INV.4 | Same filters as on screen | Exports CSV | Export sales/amount sum = hero total (± rounding) — copy: “Export matches this total” (A2 / EBR-91) |
| LT-INV.5 | Bug / Broken path (demo or prod defect) | Territory selected but filter ignored | Mismatch is visible; Fixed is the **default** product feel |
| LT-INV.6 | List columns | — | Amount, customer, date carry the story; production-like invoice identifiers retained |

**Maps to:** FILTER-TRUTH A1.1, A2.1–A2.2, A4.

---

## LT-CUST — Customers

| # | Given | When | Then |
|---|---|---|---|
| LT-CUST.1 | Portal customer list | Changes **date range** | **Selected-range sales** hero recomputes (invoiced net) — not frozen LY/CY only |
| LT-CUST.2 | Same | Changes **territory** (Fixed) | List + selected-range hero scope to that territory; fail-closed rules per A1.4 |
| LT-CUST.3 | LY / CY / Backlog tiles | — | Secondary anchors; backlog labeled **not sales** |
| LT-CUST.4 | Same scope as screen | Exports CSV | Export sales sum = selected-range hero (A2) |
| LT-CUST.5 | Org with S1 decay cohort | Views list | ≥2–3 **Quietly dying** affordances (e.g. accounts from `IR-v1-QUERIES.md`: 29925, 32162, 31098) jump to Intelligence S1 (`#intel-s1`) |

**Maps to:** FILTER-TRUTH A1, A2, A4 · IR hook S1 / EBR-198.

---

## LT-ORD — Orders (EBR-87)

| # | Given | When | Then |
|---|---|---|---|
| LT-ORD.1 | Org with quote statuses in portal orders | Opens Orders | Visual split: **Confirmed / open order $** (primary) vs **Quotes $** (demoted); quotes never in anything labeled sales / confirmed |
| LT-ORD.2 | Quote rows present | Renders any “sales” or confirmed total | Quote amounts **excluded** |
| LT-ORD.3 | Backlog tile | — | Copy = open orders — **not sales** (A3.2) |
| LT-ORD.4 | Status filter includes Quote | User filters to Quote (or other status) | Visible rows and the confirmed/quote story **recompute**; Quote-only → confirmed = $0 |

**Maps to:** FILTER-TRUTH A3 · EBR-87.

---

## LT-RPT — Reports (Sales Summary)

| # | Given | When | Then |
|---|---|---|---|
| LT-RPT.1 | Advanced reports enabled for user | Opens Reports → Summary | Answer-first **invoiced net** total for selected range (table secondary) |
| LT-RPT.2 | Same org/window | Compares to Dashboard invoiced KPI + Intelligence C1 | **Same definition** — `SUM(portal_invoices.net_amount)` (A4 / C1 spine) |
| LT-RPT.3 | Date range changes | — | Report total recomputes; export matches that total |
| LT-RPT.4 | Product types | — | Do **not** invent new report types beyond existing Summary / Product Details / Monthly |

---

## LT-SHELL — Demo / shipping guardrails

| # | Given | When | Then |
|---|---|---|---|
| LT-SHELL.1 | Internal demo | Navigates What’s broken | Teaching surface only — **non-shipping**; last nav; not primary Bet A proof |
| LT-SHELL.2 | Territory-scoped $ on list tabs | Stakeholder demo | Labeled **illustrative** until warehouse filter ships; Intelligence / org LTM stamps stay live via `IR-v1-QUERIES.md` |
| LT-SHELL.3 | Settings hub | — | Later / Bet E — do not polish as shipping AC in this bet |
| LT-SHELL.4 | Intelligence | Deep-link from Customers S1 | `#intel-s1` (or equivalent) still works; heroes unchanged by list-tab work |

---

## Verify (pre-build)

- [ ] LT-INV.1–4 on named org (prefer wwjc / zero-exposure; avoid sarreid territory claims until 2196-class honest)  
- [ ] LT-CUST.1 + LT-CUST.5  
- [ ] LT-ORD.1–2 on quote-polluted org or fixture  
- [ ] LT-RPT.2 reconciles to C1 on same window  

**Build only after:** `ISOLATION OFF — GO on EBR-40` (and/or named list surface).

---

*Companion to `DEMO-SURFACE-CONTRACT.md` §2. Cite this file for Given/When/Then; cite FILTER-TRUTH / IR-v1 for law and stamps.*
