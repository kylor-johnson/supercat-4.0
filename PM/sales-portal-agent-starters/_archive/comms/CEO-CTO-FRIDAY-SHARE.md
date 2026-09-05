# Sales Portal — Bet A (Filter Truth) — Decision Brief

> **Current ask (validation closed 2026-07-21)**
>
> Approve starting **Bet A — Filter Truth** with locked scope: **keep EBR-40 + EBR-91** (+ **EBR-212 paired**), **park EBR-87**, **close EBR-7** by doctrine.
>
> **GO phrase:** `ISOLATION OFF — GO on EBR-40`
>
> Evidence: filled `BUG-VALIDATION-PACK.md` (production SQL + Rails). Optional UI: `cmallon` → Invoices YTD → `105:1 Gigi Lane` → ~710 / ~$777k.
>
> **Not in this GO:** Intelligence · Settings hub · LLM · Dashboard redesign · dedicated EBR-87 build.

| | |
|---|---|
| **Owner** | Kylor |
| **Date** | 2026-07-20 · **Updated** 2026-07-21 |
| **Status** | Mockup-only · **ISOLATION ON** · **Validation complete** · No Rails shipped |
| **Next touch** | Validation readout → GO decision |

---

## Assumptions — verified

| Assumption | Result (2026-07-21) |
|---|---|
| EBR-40 still valid | **Yes** — wwjc `cmallon` YTD 1,404/$1.46M → T1 `105:1 Gigi Lane` 710/$777k |
| EBR-212 still valid | **Partial** — same mechanism; wwjc multi-terr reps lack dashboard. **Keep paired.** |
| EBR-91 still valid | **Yes — period drift** (SERV-2395). AC-A2 rewritten. |
| Quotes inflate “sales” universally (EBR-87) | **No** — **parked**. Only `cci`/`ril` have quotes; both backlog-excluded. `kal` has none. |
| wwjc = trust flagship | **Confirmed** (≠ zero-exposure synonym) |

---

## TL;DR

Reps don’t trust the portal’s numbers, so they rebuild them in Excel.

**Bet A** (validated scope) fixes:

1. Territory filters limit the list **and** the total (EBR-40 + 212 paired)
2. Customers selected-range total and export share one period (EBR-91)

**Parked:** universal “quotes as sales” build (EBR-87). **Close:** EBR-7 via `net_amount`. Nothing in the demos is “done.” **No Rails until explicit GO.**

---

## The story

```
TODAY — what reps hit (validated)
─────────────────────────────────────────────
Rep picks a territory  ──▶  wrong / untrusted book
                           ← EBR-40 / 212  (still real)

Customers date/export  ──▶  period drift vs on-screen
                           ← EBR-91  (still real)

"Quotes as sales"      ──▶  NOT universal — parked
                           ← EBR-87

        │
        ▼
┌──────────── BET A — GO scope ────────────────┐
│  Territory limits the list AND the total      │
│  Customers period + export reconcile          │
│  → one invoiced number, same everywhere       │
└───────────────────────┬──────────────────────┘
                        ▼
              Numbers are trustworthy
```

---

## How the next leadership touch runs

| Step | What | Link / artifact |
|---|---|---|
| **1. Start here** | **Validation readout** — filled pack + dispositions | `BUG-VALIDATION-PACK.md` · `DRAFT-CTO-REPLY-validation.md` |
| **2. Optional UI** | Live: `cmallon` Invoices YTD → `105:1 Gigi Lane` · or pitch demo | — |
| **3. Decision** | GO on locked scope | `ISOLATION OFF — GO on EBR-40` |

**Rule for the room:** no full internal demo (Dashboard / Intelligence / Settings) as the default.

### Pre-read

| Doc | Why |
|---|---|
| This page | Framing + verified scope |
| `BUG-VALIDATION-PACK.md` | Filled results + rollup |
| `DRAFT-CTO-REPLY-validation.md` | Paste-ready readout |
| `TRD-Bet-A-filter-truth.md` | Decision record |
| `FILTER-TRUTH-AC.md` | AC-A2 rewritten; A3 parked |
| `IA-PERSONA-TRACK.md` | Parallel track — not this GO |

**No Rails until:** `ISOLATION OFF — GO on EBR-40`

---

## What you’re looking at

| It is | It is not |
|---|---|
| Interactive HTML mockups in the design system | Shipped product / production Rails |
| Spec + appetite for Cycle 03 | Proof that EBR tickets are resolved |
| Trust-first product direction | Approval of Intelligence, Settings, or LLM |
| Partially live-grounded (org LTM + SQL validation 2026-07-21) | Live territory-scoped dollars in demos (illustrative until eng ships) |

**Two demos, same story**

| Demo | Opens on | Use when |
|---|---|---|
| Bet A pitch | Invoices | Optional click-through for readout |
| Full internal | Dashboard | Off default path — program preview only |

---

## Why this looks small (and isn’t undercounting Jira)

Nothing in these demos is done. Tickets are still open. Validation decided which problems stay in appetite.

| # | Problem | EBR ticket(s) | Validated |
|---|---|---|---|
| 1 | Picking a territory doesn’t change what I see | EBR-40 + EBR-212 | **Still real** / partial dash — **keep** |
| 2 | CSV / period ≠ on-screen total | EBR-91 | **Still real** (period drift) — **keep** + rewrite AC |
| 3 | Quotes show up as “sales” | EBR-87 | **Not universal** — **park** |

**Bet A outcome set:** fix 40 + 91 (+ 212 paired) + **close EBR-7**. No dedicated EBR-87 build.

### There are dozens of other portal EBRs — here’s where they go

| Bucket | Examples | Why not in the Bet A ask |
|---|---|---|
| **Bet A (this GO)** | 40, 212, 91 (+ close 7) | Validated trust pitch |
| **Parked from Bet A** | 87 | Not universal; config already excludes on cci/ril |
| **Bet C — Intelligence** | 775 epic, 198 | Separate bet — after trusted totals |
| **Parked LLM** | 772, 776 | Downstream of computational IR |
| **XL shelf** | 180 | Separate appetite |
| **Deferred / one-org** | 197, 213, 278, … | Post-v1 or org-specific |
| **Out of this program** | iPad / order-email / catalog | Different surfaces |

Full routing: `EBR-AFFINITY-PORTAL.md`.

---

## What Bet A ships

**Appetite:** small batch — fixed time, variable scope. A trust fix, not a territory data-model rewrite.

| Outcome | Detail |
|---|---|
| Territory limits list **and** total | Pick a territory → rows and every total recompute to that book |
| Customers period + export reconcile | Selected-range UI total = export column (EBR-91 / SERV-2395) |
| One invoiced spine | Every “sales” total = invoiced net |
| Answer-first list tabs | May ride with A later — **not** the proof story for GO (Track 2) |

**Done means:** on **wwjc**, territory scopes invoice list + totals; Customers selected-range and export agree; every sales total is invoiced net.

**Explicit no-gos:** EBR-180 · LLM · Dashboard redesign · dedicated EBR-87 build · verifying territory on **sarreid** · shipping “What’s broken” as product nav.

---

## Metric law (one spine)

```
Revenue / sales / invoiced = SUM(portal_invoices.net_amount)
· report-through-date clamped
· $5M single-row cap
· confidence ceiling STRONG — never FULL
```

| Rule | Detail |
|---|---|
| Quotes ≠ sales | Metric-law copy only — EBR-87 **parked** as build |
| Export / period = UI | EBR-91 — AC-A2 rewritten |
| Backlog ≠ sales | Open orders labeled backlog, never sales |
| EBR-7 | Already answered by `net_amount` — close ticket |
| Warehouse dashboard | Not validation ground truth — label “invoiced ledger” |

**STRONG** means provenance (one invoice feed), not “this metric is good.”  
**$16,022,554** is the live Sarreid org-wide LTM anchor (verified 2026-07-17).

---

## Decisions for CTO

1. **GO on Bet A?** Locked scope above → `ISOLATION OFF — GO on EBR-40`.
2. **Verify org** — confirm **wwjc** (recommended).
3. **Customers date filter** — in this bet (recommended; it *is* the EBR-91 fix) vs fast-follow.
4. **Settings Wave 0** — ride with A this cycle, or wait?

Do **not** treat Dashboard / Intelligence mockups as part of the GO decision. Persona + IA is Track 2 (`IA-PERSONA-TRACK.md`).

---

# Appendix — Demo walkthrough & decoder

*For people who will click the tabs. Not required to decide Friday.*

---

## Sidebar tabs (full internal demo)

Each tab answers one primary question. The big hero is the answer; the list is evidence.

### 1. Dashboard — How’s the business doing overall?

| Element | Meaning |
|---|---|
| Backlog Total — $77.8M on Sarreid | Open orders — **not sales**. Sarreid has empty status exclusions, so backlog can include completed orders. Labeled explicitly. |
| Invoiced tile — $16.0M TTM | Trailing-12-month invoiced net from `portal_invoices.net_amount`. |
| Chart | Gold = invoices, blue = orders. Matches production Chart.js pattern. |
| Budget / quota | Illustrative pacing. |
| Top-N panels | Production-density parity. |
| Territory filter warning | Points to What’s broken — today the portal doesn’t honor territory reliably on dashboard. |

### 2. Customers — How much did these customers sell in the selected range?

| Element | Meaning |
|---|---|
| Hero — selected-range sales | Invoiced net for current date range. Same spine as Invoices / C1. |
| LY / CY calendar | Secondary anchors, not the primary answer. |
| Backlog · not sales | Open order book — never labeled sales. |
| Export matches this total | CSV sum = hero for same filters (EBR-91). |
| Accounts fading rows | Jump to Intelligence S1 — **internal demo only**; pitch omits these. |

### 3. Orders — What’s confirmed vs what’s still a quote?

| Element | Meaning |
|---|---|
| Hero — confirmed / open $ | Real order book — primary number. |
| Quotes $ card | Demoted, dashed, never labeled “sales.” |
| Filter Status = Quote | Confirmed hero → $0; quotes card keeps open-quote $. |
| Backlog | Open orders, not sales. |

**Note:** EBR-87 parked from Bet A GO (2026-07-21) — teaching chrome only.

### 4. Invoices — Bet A proof surface

**Centerpiece of the pitch.** Change territory or date → hero, row count, and export badge move together.

| Element | Meaning |
|---|---|
| Hero — invoiced total | `SUM(net_amount)` for current territory + date range. |
| Export matches this total | Trust test — EBR-91. |
| Rows in scope | Feed follows the same filters as the hero. |
| Simulate today’s filter bug | Demo-only. Hero stays whole-org; export card flips to mismatch. |
| Invoice feed | Amount, customer, date lead. Row amounts illustrative. |

**Tickets:** EBR-40, EBR-212, EBR-91.

### 5. Reports — Same invoiced answer, report format

| Sub-tab | Job |
|---|---|
| Summary | Big invoiced net — must match Dashboard invoiced KPI and Intelligence C1 |
| Product Details | Breakdown by product; table secondary |
| Monthly | Month-by-month invoiced; table secondary |

**Rule:** Dashboard invoiced · Intelligence C1 · Report Summary = one spine.

### 6. Intelligence — Insights beyond scrolling lists

Under epic **EBR-775**. Computational first — not LLM. EBR-772 / 776 parked.

| Block | What it is | Ticket |
|---|---|---|
| C1 — Invoiced sales | Ledger total — same $16,022,554 | EBR-775 v1 |
| S1 — Accounts fading | 25 accounts down ≥40% vs prior 6mo; $1.69M LTM on flagged. Top 5 live-stamped. | EBR-198 |
| Team strip | Active seats, logins, top writers — 30 days. Behavior floor, not invoiced-rep revenue. | Q-R1 / Q-18 |

**Not in v1 default:** RS-01 named invoiced-rep revenue leaderboard · LLM · dumping five Dashboard Top-N tables onto Intelligence.

### 7. Settings hub — Bet E (later)

Shaped; AC locked. Demo chrome (wave badges, Delete buttons, decision tree) ≠ eng directive until GO. Skip in pitch unless asked.

### 8. What’s broken — Why can’t reps trust the portal today?

Last in internal nav; **not** the pitch opener. Non-shipping teaching surface. Broken | Fixed toggle + territory picker. Real Bet A proof lives on **Invoices / Customers**.

---

## Broken vs Fixed

| Mode | Pick Northeast → |
|---|---|
| **Broken (today)** | Still 1,417 customers · $16.02M — whole org. Territory ignored. |
| **Fixed (Bet A ships)** | Scoped set — fewer customers, smaller $. List + total + export agree. |

Three things must be true before Intelligence is trustworthy:

1. Territory scopes the book — EBR-40 / 212  
2. Export reconciles to UI — EBR-91  
3. *(Parked)* Quotes-as-sales universal build — EBR-87 — metric-law copy only  

---

## Jargon decoder

### Invoices provenance line

`Fixed path · territory limits the total · STRONG · org LTM live $16,022,554`

| Phrase | Plain English |
|---|---|
| Fixed path | Desired post–Bet A behavior. Opposite = Broken path. |
| Territory limits the total | Pick NE → number and rows shrink to NE. “All territories” = assigned book (or whole org for admins). |
| STRONG | Provenance label — one invoice feed, RTD clamp, $5M row cap. **Not** “metric is good.” |
| Org LTM live $16,022,554 | Real Sarreid TTM query (2026-07-17). Territory slices illustrative until filter ships. |

### Other labels

| Label | Means |
|---|---|
| Invoiced net_amount | Sales = invoice net, not order totals. Discounts already netted. |
| Export matches this total | CSV = on-screen hero for same filters. |
| Backlog · not sales | Open orders — never sales. |
| Illustrative share until warehouse filter ships | NE/SE/MW $ are demo fudge. |
| Mockup-only / ISOLATION ON | Spec art, not production. |
| LIVE / live-stamped | Recomputed from Postgres on grade date. |
| Bet E shaped | Settings AC locked; not built. |

---

## How bets map to the demos

| Bet | What | Where |
|---|---|---|
| **A** | Filter truth + metric law | Pitch: Invoices, Customers, Orders, What’s broken |
| **B** | Answer-first list tabs | Heroes on list tabs — rides with A |
| **C** | Computational Intelligence | Full demo: Intelligence tab |
| **E** | Settings control plane | Full demo: Settings hub (context only) |

**Trust order:** A → then Intelligence means something → LLM later.

---

## Demo → production guardrails

| Demo element | Build meaning |
|---|---|
| Territory-scoped $ on lists | Illustrative until warehouse filter ships |
| “Simulate today’s filter bug” | Demo-only teaching control |
| Category-glyph thumbnails | Placeholder for catalog photos |
| Furniture descriptions / row amounts | Illustrative unless live-stamped |
| Customer names | Masked |
| Org switcher | Demo chrome |
| C1 / S1 / team from `IR-v1-QUERIES.md` | Live-stamped; recompute at build on grade orgs |
| What’s broken page | Teaching surface — behaviors must live on real tabs |
| Large list-tab heroes | Shipping UX intent (Bet B shell) |

---

## Spec pack (if you want depth)

| Need | File |
|---|---|
| CTO feedback capture | `CTO-FEEDBACK-2026-07-20.md` |
| Bug validation pack | `BUG-VALIDATION-PACK.md` |
| Draft CTO reply | `DRAFT-CTO-REPLY-validation.md` |
| IA / persona track (not GO) | `IA-PERSONA-TRACK.md` |
| Notion paste mirror | `NOTION-MIRROR-bet-a-post-cto.md` |
| Bet A decision record | `TRD-Bet-A-filter-truth.md` |
| Program roadmap (context) | `PROGRAM-ROADMAP-cycle03.md` |
| Bet A AC | `FILTER-TRUTH-AC.md` |
| List-tab AC | `LIST-TABS-AC.md` |
| Intelligence AC | `INSIGHT-IR-v1-AC.md` |
| Live SQL stamps | `IR-v1-QUERIES.md` |
| EBR affinity / routing | `EBR-AFFINITY-PORTAL.md` |
| Eng handoff (full) | `ENG-HANDOFF-bet-a-b-c-e.md` |
| Pitch walk order | `BET-A-PITCH-DEMO-RUNBOOK.md` |
| Full demo walk order | `INTERNAL-DEMO-RUNBOOK.md` |
| Program spine | `00-PROGRAM-SPINE.md` |

---

## Bottom line

**Make portal numbers trustworthy → make them legible → add Intelligence.**

- **Validation closed:** keep **EBR-40 + 91** (+ **212 paired**); **park EBR-87**; close **EBR-7**
- **Ask:** `ISOLATION OFF — GO on EBR-40` if scope is good
- Dashboard / Intelligence visuals are **not** this decision (Track 2 for IA)
- Isolation stays ON until you say the GO phrase