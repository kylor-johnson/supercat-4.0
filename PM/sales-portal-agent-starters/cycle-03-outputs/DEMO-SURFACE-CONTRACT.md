# Demo surface contract — eng / tech-spec authority

**Date:** 2026-07-17 · **Updated:** list-tab substance (answer-first) · **Isolation:** ON  
**File:** `design-system/app/sales-portal-internal-demo.html`  
**Use when writing TECHNICAL-PLAN / eng-handoff:** cite this + `LIST-TABS-AC.md` — do not reverse-engineer architecture from HTML alone.

---

## 1. Nav order (canonical)

| # | Nav | Role |
|---|---|---|
| 1 | Dashboard | Default. Production-density portal chrome + live-grounded KPIs where stamped |
| 2 | Customers | Selected-range sales hero + territory + export=UI + S1 hooks |
| 3 | Orders | Confirmed vs Quotes split + backlog ≠ sales |
| 4 | Invoices | **Bet A proof** — invoiced total for filters + territory + export=UI (EBR-40) |
| 5 | Reports | Sales Summary total = invoiced net (C1 spine) |
| 6 | Intelligence | C1 + S1 + team strip (Bet C) — live-stamped via `IR-v1-QUERIES.md` |
| 7 | Settings hub | Bet E **shaped** (AC locked) — Later nav; not default landing; not Bet A proof |
| 8 | What’s broken | Last. Plain-English Broken\|Fixed sim — **non-shipping teaching surface** |

Former “Trust / Fix” meta AC wall is **retired**. Ticket IDs live in footnotes / `FILTER-TRUTH-AC.md`.

> **Bet F persona priority (illustration / ordering authority — not a demo change).** *Who sees what first* and the recommended default homes (rep → Customers · owner → Intelligence · ops → Settings hub — all HYPOTHESIS pending customer A/B) are shaped in Bet F (`IA-PRIORITY-MATRIX.md`, `IA-RECOMMENDATION-v0.md`). That matrix is the **ordering authority for future Bet B work** — the per-persona lead answer on each surface — **not** a change to the Friday demo HTML. This contract's nav order and per-surface primary jobs are **unchanged**; Bet F does not reorder nav or rewrite the primary jobs below. What's broken stays a **non-shipping teaching surface**, never a persona default.

---

## 2. Per-surface substance (must ship in Rails after GO)

### Dashboard
- Preserve production Top-N fidelity (photos, item #, units, amount) — see `DEMO-PORTAL-DENSITY-AUDIT.md`.
- Invoiced KPI = `SUM(portal_invoices.net_amount)` for range.
- Backlog labeled backlog; status exclusions are metric-law (Revenue defs), not self-serve.
- Territory control must eventually honor Bet A (demo may warn → What’s broken).

---

### Invoices — primary job

**Primary job:** Answer “What did we invoice under these filters?” with a large hero total that moves with territory + date range (Bet A / EBR-40).

| Aspect | Contract |
|---|---|
| Hero metric | **Invoiced total for current filters** — large answer number, not a meek strip |
| Spine | Invoiced `net_amount` only (A4) — never booked orders / quotes |
| Filter behavior | Territory + date range change **both** hero and visible rows. **Fixed** = default. Optional “Simulate today’s filter bug” may show Broken path |
| Export | First-class: “Export matches this total: $X” = hero (A2 / EBR-91) |
| AC ids | A1.1, A2, A4 · `LIST-TABS-AC.md` LT-INV.* |
| Demo→prod | Territory $ = **illustrative** share until warehouse filter ships. Org LTM **$16,022,554** (sarreid) = live stamp from `IR-v1-QUERIES.md` / density audit |
| Columns | Amount · customer · date lead the story; invoice # / order # / PO retained |

---

### Customers — primary job

**Primary job:** Answer “How much did these customers sell in the selected range?” with a recomputing selected-range sales hero, plus S1 jump-offs.

| Aspect | Contract |
|---|---|
| Hero metric | **Selected-range sales** (invoiced net) — recomputes with date range |
| Spine | Same invoiced net as Invoices / C1 for “sales”; LY/CY = calendar anchors (secondary); backlog = **not sales** |
| Filter behavior | Territory scopes list + hero (Fixed default; fail-closed per A1.4) |
| Export | “Export matches this total” = selected-range hero (A2) |
| IR hooks | 2–3 Quietly dying rows (e.g. 29925, 32162, 31098 from `IR-v1-QUERIES.md`) → Intelligence `#intel-s1` (S1 / EBR-198) |
| AC ids | A1, A2, A4 · LT-CUST.* |
| Demo→prod | Territory scope **illustrative**; S1 account IDs / decay % grounded in stamped queries; names masked |

---

### Orders — primary job

**Primary job:** Show open/confirmed book vs pipeline without letting quotes pollute sales (EBR-87).

| Aspect | Contract |
|---|---|
| Hero metric | **Confirmed / open order $** (primary) vs **Quotes $** (demoted / dashed) |
| Spine | Quotes ≠ sales / confirmed (A3). Backlog = open orders — **not sales** |
| Filter behavior | Status includes Quote; filtering recomputes visible story (Quote-only → confirmed $0). Territory may scope rows (illustrative) |
| Export | Not the Bet A reconciliation flagship (Invoices/Customers are); still must not export quotes as sales |
| AC ids | A3 · LT-ORD.* |
| Demo→prod | Row amounts illustrative; behavior (quote exclusion) is the shipping law |

---

### Reports — primary job

**Primary job:** Sales Summary answers with **invoiced net** for the selected range — same spine as Dashboard + Intelligence C1.

| Aspect | Contract |
|---|---|
| Hero metric | Answer-first invoiced net total; table is secondary |
| Spine | Explicit parity: Dashboard invoiced · Intelligence C1 · Report total = `SUM(portal_invoices.net_amount)` |
| Filter behavior | Date range (and report-by) recompute total; export matches total |
| Export | “Export matches this total” |
| AC ids | A4 · C1 · LT-RPT.* |
| Demo→prod | Do not invent new report types. Gate flags (`advanced_reports`, etc.) belong in Settings (Later) — not a mystery-admin banner on the answer |

---

### Intelligence
- Heroes per `INSIGHT-IR-v1-AC.md`; SQL stamps per `IR-v1-QUERIES.md`.
- Do **not** dump five Dashboard Top-N tables onto Intelligence by default.
- No RS-01 / named invoiced-rep revenue in v1 default.
- Deep-link target for Customers: `#intel-s1`.

### What’s broken
- Internal explanation + interactive Broken\|Fixed territory sim only.
- **Non-shipping** — not a permanent customer-facing nav name unless product decides later.
- Spec pointer: `FILTER-TRUTH-AC.md`. Bet A proof lives on **Invoices / Customers**, not here.

### Settings hub
- **Bet E shaped** — build AC = **`SETTINGS-hub-v1-AC.md`**; ship gate = `SHIP-READINESS-bet-e.md`; triage = `PORTAL-SETTINGS-CONTROL-PLANE.md`.
- Layout/copy reference only until `ISOLATION OFF — GO on Bet E`. Still **not** the primary Bet A proof surface (Invoices / Customers are).
- Demo chrome (Wave badges, Delete buttons, static decision tree) ≠ eng directive.

---

## 3. Demo → prod guardrails (non-negotiable)

| Demo element | Build meaning |
|---|---|
| Territory scoped $ on lists | Illustrative share math until warehouse filter ships |
| “Simulate today’s filter bug” | Demo-only control to show Broken path |
| Category-glyph thumbnails | Placeholder for real catalog photos |
| Furniture descriptions / amounts | Illustrative unless live-stamped |
| Customer names | Masked |
| Org switcher | Demo chrome |
| Chart.js CDN | Mockup only — reuse production chart lib in Rails |
| S1 / team / C1 numbers from `IR-v1-QUERIES.md` | Live-stamped reference — recompute at build on grade orgs |
| What’s broken page | Teaching surface — behaviors must exist on real tabs |
| Large list-tab heroes | Shipping UX intent (answer-first) — Bet B shell |

---

## 4. Metric law (unchanged)

- Revenue / sales / invoiced = `SUM(portal_invoices.net_amount)`, RTD-clamped, $5M cap, `customer_bill_to_number` grain, ceiling **STRONG**
- Quotes ≠ sales · Export = UI · EBR-7 answered by `net_amount`
- Team strip = behavior / eCat GMV only · no Universe E lead
- No EBR-772/776 · no margin/COGS · no FULL completeness claims

---

## 5. Spec pack pointers

| Need | File |
|---|---|
| List-tab Given/When/Then | **`LIST-TABS-AC.md`** |
| Bet A AC | `FILTER-TRUTH-AC.md` |
| Bet C AC | `INSIGHT-IR-v1-AC.md` |
| Stamped SQL | `IR-v1-QUERIES.md` |
| Eng plan | `TECHNICAL-PLAN.md` § Bet B list-tabs |
| Density / Top-N | `DEMO-PORTAL-DENSITY-AUDIT.md` |
| Gaps | `SPEC-GAP-CHECKLIST.md` |
| Internal walk | `INTERNAL-DEMO-RUNBOOK.md` |
| Bet E AC | **`SETTINGS-hub-v1-AC.md`** |
| Bet E ship gate | `SHIP-READINESS-bet-e.md` |

When an agent writes the technical spec, **cite this file** for demo→Rails shell (Bet B) and list-tab substance, **`LIST-TABS-AC.md`** for acceptance scenarios, `FILTER-TRUTH-AC` / `IR-v1-QUERIES` for Lane 0 / Lane 2, and **`SETTINGS-hub-v1-AC.md`** for Bet E — do not re-derive from HTML alone.

---

*Contract updated 2026-07-18 — Bet E AC locked; Settings still Later / not Bet A proof.*
