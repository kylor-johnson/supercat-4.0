# Bet A pitch demo — betting table walk

**File:** `design-system/app/sales-portal-bet-a-pitch-demo.html`  
**Audience:** betting table, CTO review, appetite conversation  
**Not for:** eng handoff / Cycle 03 full show-and-tell

---

## When to use this vs full demo

| Use | Open |
|---|---|
| Appetite / pitch / “is Bet A worth a cycle?” | **This file** — Invoices → Customers → Orders → What’s broken |
| Eng handoff, density audit, Intelligence, Settings, Reports | `design-system/app/sales-portal-internal-demo.html` + `INTERNAL-DEMO-RUNBOOK.md` |

Full demo contract stays canonical: `DEMO-SURFACE-CONTRACT.md`. This pitch is a **fork-by-extraction**, not a replacement.

---

## Open in browser

```
file:///Users/kylorjohnson/Library/Mobile%20Documents/com~apple~CloudDocs/SuperCat%204.0/design-system/app/sales-portal-bet-a-pitch-demo.html
```

Lands on **Invoices** (not Dashboard).

---

## 5-minute walk order

1. **Invoices** — Bet A proof  
2. **Customers** — selected-range + export  
3. **Orders** — quotes ≠ sales  
4. **What’s broken** — Broken \| Fixed teaching sim  

Skip stub nav items unless asked (they only show “out of scope”).

---

## Demo script (3 sentences per surface)

### 1. Invoices (AC-A1, A2, A4 · EBR-40 / 91)

1. Click territory **NE** — hero total, row count, and “Export matches this total” all shrink together (Fixed path).  
2. Check **Simulate today’s filter bug** — hero stays whole-org; export card flips to mismatch styling.  
3. Uncheck the bug — trust restored. Territory $ is illustrative; org LTM **$16,022,554** is the live stamp.

### 2. Customers (AC-A1, A2 · EBR-91)

1. Change date range (YTD → TTM) — selected-range hero and export badge recompute together.  
2. Change territory — feed scopes; same Fixed / bug-sim pattern as Invoices.  
3. Point at LY / CY / **Backlog ≠ sales** — no Quietly dying / Intelligence jump in this pitch.

### 3. Orders (AC-A3 · EBR-87)

1. Show confirmed hero vs demoted Quotes card.  
2. Filter Status = **Quote** — confirmed → **$0**, quotes card keeps pipeline $.  
3. One line: quotes never labeled sales; backlog is open orders, not sales.

### 4. What’s broken (teaching only)

1. Leave **Broken** — pick NE — result still whole-org $16.02M.  
2. Switch to **Fixed** — same pick shrinks to NE share.  
3. Close: three problems = territory scope + export reconcile + quotes out of sales (`FILTER-TRUTH-AC.md`).

---

## Explicit no-gos (shown by stubs)

Sidebar stubs (badge “Not in Bet A pitch”) — click → single message only:

- **Dashboard** — production density / charts  
- **Reports** — Summary / Product Detail / Monthly  
- **Intelligence** — C1 / S1 / team strip (Bet C)  
- **Settings** — Bet E hub  

Do not improvise those surfaces here. Point stakeholders to the full demo if needed.

---

## Spec pointers

`FILTER-TRUTH-AC.md` · `DEMO-SURFACE-CONTRACT.md` · `INTERNAL-DEMO-RUNBOOK.md` · eng §C in `ENG-HANDOFF-bet-a-b-c-e.md`

*Pitch-only. Do not merge into `sales-portal-internal-demo.html`.*
