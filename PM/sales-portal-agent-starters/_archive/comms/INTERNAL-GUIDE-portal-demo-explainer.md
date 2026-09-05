# Sales Portal Demo — Internal Guide

> **Purpose:** Plain-language explainer for the Cycle 03 Sales Portal mockups — what each tab means, what the jargon is, and how the EBR tickets fit in.
>
> **Audience:** Internal (PM, eng, leadership, show-and-tell attendees)
>
> **Last updated:** 2026-07-20
>
> **Status:** Mockup-only · ISOLATION ON (no Rails shipped yet)

---

## At a glance

| Item | Value |
|---|---|
| **Program home** | `SuperCat 4.0/PM/sales-portal-agent-starters/` |
| **Full demo** | `design-system/app/sales-portal-internal-demo.html` |
| **Bet A pitch demo** | `design-system/app/sales-portal-bet-a-pitch-demo.html` |
| **Demo org** | Sarreid, Ltd. (`sarreid`) — rich data; some numbers live-stamped from Postgres |
| **Live anchor number** | Org LTM invoiced net **$16,022,554** (verified 2026-07-17) |

---

## What this is (and is not)

### What it is

- **Interactive HTML mockups** in the design-system — spec artifacts for Cycle 03, not production Rails.
- A **walkthrough of the product direction**: fix trust first (Bet A), modernize list tabs (Bet B), add Intelligence (Bet C), shape Settings later (Bet E).
- **Partially live-grounded:** the org-wide LTM invoiced total and Intelligence C1/S1 numbers come from real Postgres queries. Territory splits and many row amounts are **illustrative** until eng ships warehouse filtering.

### What it is not

- Not shipped product code.
- Not proof that EBR tickets are resolved — **all Bet A tickets are still open**.
- Not a complete inventory of every EBR ticket in Jira — the demo **curates** what matters per bet.

> 💡 **ISOLATION ON** means agents and PM can diagnose and spec, but **no production code changes** until Kylor explicitly lifts isolation: `ISOLATION OFF — GO on <ticket>`.

---

## Two demos — same story, different audience

| File | Opens on | Use when |
|---|---|---|
| **`sales-portal-internal-demo.html`** | Dashboard | Eng handoff, full show-and-tell, density audit, Intelligence, Settings, Reports |
| **`sales-portal-bet-a-pitch-demo.html`** | Invoices | 5-minute appetite / betting-table pitch — **Bet A only** |

The pitch demo is a **trimmed fork**. Dashboard, Reports, Intelligence, and Settings show as stubs (“Not in Bet A pitch”). The full demo contract lives in `DEMO-SURFACE-CONTRACT.md`.

### Walk order — full demo

1. **Dashboard** — production-density home
2. **Invoices** — Bet A proof (territory + date + export)
3. **Customers** — selected-range sales; Quietly dying → Intelligence
4. **Orders** — confirmed vs quotes
5. **Reports** — Sales Summary = same invoiced spine as Dashboard / C1
6. **Intelligence** — C1 + S1 + team strip (Bet C)
7. **Settings** — Bet E shaped (skip unless asked)
8. **What's broken** — teaching sim last (not the Bet A story)

### Walk order — Bet A pitch (5 min)

1. **Invoices** — Bet A proof
2. **Customers** — selected-range + export
3. **Orders** — quotes ≠ sales
4. **What's broken** — Broken \| Fixed teaching sim

---

## Sidebar tabs — what each one answers

Each tab is designed around **one primary question**. The big hero number is the answer; the list/feed is supporting evidence.

---

### 1. Dashboard

**Question:** *How's the business doing overall?*

| Element | Meaning |
|---|---|
| **Backlog Total** ($77.8M on Sarreid) | Open orders — **not sales**. Sarreid has empty status exclusions, so backlog includes completed orders. Labeled explicitly. |
| **Invoiced tile** ($16.0M TTM) | Trailing-12-month invoiced net from `portal_invoices.net_amount`. |
| **Chart** | Gold = invoices, blue = orders (matches production Chart.js pattern). |
| **Budget / quota** | Illustrative pacing (sarreid has quota rows; figures are demo). |
| **Top-N panels** | Production-density parity — photos, item #, units, amount. |
| **Territory filter warning** | Points to **What's broken** — today's portal doesn't honor territory reliably on dashboard. |

---

### 2. Customers

**Question:** *How much did these customers sell in the date range I picked?*

| Element | Meaning |
|---|---|
| **Hero — selected-range sales** | Invoiced net for current date range. Recomputes when range changes. Same spine as Invoices / C1. |
| **LY calendar / CY calendar** | Secondary calendar anchors — not the primary answer. |
| **Backlog · not sales** | Open order book — explicitly **not** labeled sales. |
| **Export matches this total** | CSV sum must equal the hero for the same filters (Bet A / EBR-91). |
| **Quietly dying rows** (3 accounts) | Jump-off to Intelligence S1 — accounts fading ≥40%. Internal demo only; pitch demo omits these. |

---

### 3. Orders

**Question:** *What's confirmed vs what's still a quote?*

| Element | Meaning |
|---|---|
| **Hero — confirmed / open $** | Real order book (primary number). |
| **Quotes $ card** | Demoted, dashed — **never labeled "sales."** |
| **Filter Status = Quote** | Confirmed hero goes to **$0**; quotes card keeps pipeline $. |
| **Backlog** | Open orders — not sales. |

**Ticket:** EBR-87 — quotes must not pollute any figure labeled sales/invoiced.

---

### 4. Invoices ⭐ Bet A proof surface

**Question:** *What did we invoice under these filters?*

This is the **centerpiece of the Bet A pitch.** Change territory or date range → hero total, row count, and export badge should **all move together**.

| Element | Meaning |
|---|---|
| **Hero — invoiced total** | `SUM(net_amount)` for current territory + date range. |
| **Export matches this total** | Trust test — same filters, same definition; CSV sum = hero (EBR-91). |
| **Rows in scope** | Visible feed follows the same filters as the hero. |
| **Simulate today's filter bug** | Demo-only checkbox. Hero stays whole-org; export card flips to mismatch styling — shows **broken** behavior. |
| **Invoice feed** | Amount · customer · date lead the story. Row amounts illustrative. |

**Tickets:** EBR-40 (invoice list territory), EBR-212 (dashboard territory — same mechanism), EBR-91 (export reconcile).

---

### 5. Reports (3 sub-tabs)

**Question:** *Same invoiced answer, in report format.*

| Sub-tab | Job |
|---|---|
| **Summary** | Big invoiced net hero — must match Dashboard invoiced KPI and Intelligence C1. |
| **Product Details** | Breakdown by product; table secondary to total. |
| **Monthly** | Month-by-month invoiced; table secondary to total. |

**Rule:** Dashboard invoiced · Intelligence C1 · Report Summary total = one spine (`SUM(portal_invoices.net_amount)`).

---

### 6. Intelligence (NEW — Bet C)

**Question:** *Insights beyond scrolling lists.*

Under epic **EBR-775** — computational first, **not LLM** (772/776 parked).

| Block | What it is | Ticket |
|---|---|---|
| **C1 — Invoiced sales** | Ledger total — same $16,022,554 as everywhere else. | EBR-775 v1 |
| **S1 — Accounts fading** | "Quietly dying" — 25 accounts down ≥40% vs prior 6mo; $1.69M LTM on flagged accounts. Top 5 live-stamped. | EBR-198 |
| **Team strip** | eCat activity — active seats, logins, top writers (30 days). Behavior floor, not invoiced-rep revenue. | Q-R1 / Q-18 |

> ⚠️ **Not in v1 default:** RS-01 named invoiced-rep revenue leaderboard · EBR-772/776 LLM · dumping five Dashboard Top-N tables onto Intelligence.

---

### 7. Settings hub (Later — Bet E)

**Question:** *Where should 134 portal toggles live?*

- **Bet E shaped** — AC locked in `SETTINGS-hub-v1-AC.md`.
- Wave badges, Delete buttons, static decision tree = **demo chrome**, not eng directives.
- **Not** the Bet A proof surface. Skip in pitch unless asked.

---

### 8. What's broken (teaching page)

**Question:** *Why can't reps trust the portal today?*

- **Last item** in internal demo nav — not the Bet A pitch opener.
- **Non-shipping** teaching surface (may not become permanent customer-facing nav).
- **Broken \| Fixed** toggle + territory picker — interactive sim of today's bug vs desired behavior.
- Spec pointer: `FILTER-TRUTH-AC.md`. Real Bet A proof lives on **Invoices / Customers**, not here.

---

## "Why only 3 EBR tickets?" — clarified

**You did not resolve 3 tickets.** Nothing in these demos is "done." The tickets are still open Jira work.

What looks like "3" is the **What's broken** page: **three problems**, not three closed tickets.

| # | Problem (plain English) | EBR ticket(s) | Demo status |
|---|---|---|---|
| **1** | Picking a territory doesn't change what I see | EBR-40 (invoice list) + EBR-212 (dashboard) | Still open — same mechanism, two surfaces |
| **2** | CSV export doesn't match the on-screen total | EBR-91 | Still open |
| **3** | Quotes show up as "sales" | EBR-87 | Still open |

**Bet A** bundles fixing these three problems (~4 tickets + EBR-7 close recommendation).

### EBR-7 — close, don't rebuild

EBR-7 asked for discounts in sales totals. **Doctrine answer:** discounts are already in `net_amount`. Prod Council denied a separate build in 2022. PM recommends **closing the ticket**, not shipping new work.

### Why the demo doesn't show every EBR ticket

There are **dozens** of portal EBR tickets (`EBR-AFFINITY-PORTAL.md`). The demo curates intentionally:

| Category | Examples | Why not in Bet A demo |
|---|---|---|
| **Bet A (in pitch)** | 40, 212, 91, 87 | Core pitch — 3 problems, ~4 tickets |
| **Bet C (Intelligence)** | 775 epic, 198 (S1) | Separate tab / bet |
| **Parked LLM** | 772, 776 | Explicitly downstream of computational IR |
| **XL shelf** | 180 (multi-territory RepNumber) | Separate appetite — SERV-2178 class |
| **Deferred** | 197, 213, 278, 629, 687, … | Post-v1 or org-specific |

---

## Jargon decoder

### The Invoices provenance line

> **Fixed path · territory limits the total · STRONG · org LTM live $16,022,554**

| Phrase | Plain English |
|---|---|
| **Fixed path** | Desired post–Bet A behavior: filters actually scope data. Opposite = **Broken path** (today's bug, or "Simulate today's filter bug" checked). |
| **territory limits the total** | Pick NE → big number shrinks to NE's share; list rows shrink too. "All territories" = whole assigned book (or whole org for admins). |
| **STRONG** | **Confidence / provenance label** — not "this metric is strong/good." Means: number comes from **one invoice feed** (`portal_invoices.net_amount`), report-through-date clamped, $5M single-row cap. We **never** claim FULL completeness. Same vocabulary as Insightful 4.0. |
| **org LTM live $16,022,554** | **Real Postgres query** for Sarreid trailing 12 months (verified 2026-07-17). Hero may round to $16.02M; footnote has exact cents. When territory ≠ All, the **slice is illustrative** until warehouse filter ships — but the org-wide anchor is live. |

### Other labels you'll see

| Label | Means |
|---|---|
| **Invoiced net_amount** | Sales = invoice net, not order totals. Discounts already netted. |
| **Export matches this total** | CSV sum = on-screen hero for same filters (EBR-91). |
| **Backlog · not sales** | Open orders — never labeled sales. |
| **Confirmed / open · never "sales"** | Orders hero is book value, not invoiced revenue. |
| **Illustrative share until warehouse filter ships** | NE/SE/MW $ splits are demo fudge, not live territory joins. Sarreid is 99.8% multi-territory bill-tos — real fix is hard (SERV-2196 class). |
| **Mockup-only / ISOLATION ON** | HTML is spec art, not production. |
| **Names masked** | Customer names anonymized in demo. |
| **LIVE / live-stamped** | Number recomputed from Postgres on grade date. |
| **Bet E shaped** | Settings hub has locked AC; not built yet. |

---

## Broken vs Fixed — the teaching interaction

On **What's broken** (and the Invoices "Simulate today's filter bug" checkbox):

| Mode | What happens when you pick Northeast |
|---|---|
| **Broken (today)** | Still see **1,417 customers · $16.02M** — whole org. Territory ignored. |
| **Fixed (Bet A ships)** | Scoped set — fewer customers, smaller $. List + total + export all agree. |

**Three things must be true before Intelligence is trustworthy:**

1. Territory filter scopes the book (EBR-40 / 212)
2. Export reconciles to UI (EBR-91)
3. Quotes never in sales (EBR-87)

---

## How the bets map to the demo

| Bet | Lane | What it is | Where in demo |
|---|---|---|---|
| **A** | Trust / Fix | Filters + metric law | Invoices, Customers, Orders, What's broken |
| **B** | Legible / UX | Answer-first list tabs (big hero + feed) | Shell on Invoices, Customers, Orders |
| **C** | Smart / Computational | Intelligence Reports (C1, S1, team) | Intelligence tab |
| **E** | Later | Settings control plane | Settings hub |

**Trust order:** Bet A first → then Intelligence numbers mean something → LLM (772/776) explicitly later.

---

## Metric law (one spine everywhere)

Every hero labeled **sales** or **invoiced** must use the same definition:

```
Revenue / sales / invoiced = SUM(portal_invoices.net_amount)
  · report-through-date clamped
  · $5M single-row cap
  · customer_bill_to_number grain
  · confidence ceiling STRONG (never FULL)
```

| Rule | Detail |
|---|---|
| Quotes ≠ sales | EBR-87 — quotes excluded from any sales/invoiced figure |
| Export = UI | EBR-91 — same scope + same spine |
| Backlog ≠ sales | Open orders labeled backlog, never sales |
| EBR-7 | Answered by `net_amount` — close ticket |
| Warehouse dashboard | Not validation ground truth — label "invoiced ledger" |

---

## Hero numbers cheat sheet

| Tab | Big number means | Is NOT |
|---|---|---|
| Dashboard — Invoiced | Invoiced net for date range | Backlog, quotes |
| Customers — hero | Selected-range invoiced sales | Backlog |
| Orders — hero | Confirmed / open order $ | Quotes (shown separately, demoted) |
| Invoices — hero | Invoiced net for current filters | Order book |
| Reports — Summary | Same invoiced net as Dashboard / C1 | A new definition |
| Intelligence — C1 | Same $16,022,554 ledger total | Warehouse dashboard rollup |

---

## Demo → production guardrails

| Demo element | Build meaning |
|---|---|
| Territory scoped $ on lists | Illustrative share math until warehouse filter ships |
| "Simulate today's filter bug" | Demo-only — shows Broken path |
| Category-glyph thumbnails | Placeholder for real catalog photos |
| Furniture descriptions / row amounts | Illustrative unless live-stamped |
| Customer names | Masked |
| Org switcher (sarreid / cci) | Demo chrome |
| Chart.js CDN | Mockup only — reuse production chart lib in Rails |
| C1 / S1 / team numbers from `IR-v1-QUERIES.md` | Live-stamped — recompute at build on grade orgs |
| What's broken page | Teaching surface — behaviors must exist on real tabs |
| Large list-tab heroes | Shipping UX intent (Bet B shell) |

---

## Spec pack — where to go deeper

| Need | File |
|---|---|
| Demo surface contract | `cycle-03-outputs/DEMO-SURFACE-CONTRACT.md` |
| Internal walk order | `cycle-03-outputs/INTERNAL-DEMO-RUNBOOK.md` |
| Bet A pitch walk | `cycle-03-outputs/BET-A-PITCH-DEMO-RUNBOOK.md` |
| Bet A acceptance criteria | `cycle-03-outputs/FILTER-TRUTH-AC.md` |
| List-tab Given/When/Then | `cycle-03-outputs/LIST-TABS-AC.md` |
| Intelligence AC | `cycle-03-outputs/INSIGHT-IR-v1-AC.md` |
| Live SQL stamps | `cycle-03-outputs/IR-v1-QUERIES.md` |
| EBR ticket affinity | `cycle-03-outputs/EBR-AFFINITY-PORTAL.md` |
| Eng handoff | `cycle-03-outputs/ENG-HANDOFF-bet-a-b-c-e.md` |
| Program spine | `00-PROGRAM-SPINE.md` |

---

## Bottom line

These HTML files are a **spec walkthrough** for: *make portal numbers trustworthy → make them legible → add Intelligence.*

- The **"3"** = three broken behaviors Bet A fixes — not three resolved tickets.
- **STRONG** = data provenance (single feed), not a quality judgment.
- **$16,022,554** = the one real org-wide anchor; territory splits around it are demo illustration until eng ships the filter.
- **Nothing is shipped yet** — ISOLATION ON until explicit GO.

---

*Copy this doc into Notion via Import → Markdown, or paste sections directly. File path: `PM/sales-portal-agent-starters/cycle-03-outputs/INTERNAL-GUIDE-portal-demo-explainer.md`*
