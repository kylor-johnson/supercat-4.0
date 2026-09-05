# CTO pre-read — Friday show-and-tell

**Status:** `Review for show-and-tell · Isolation ON · NOT ready to build until explicit GO`
**Owner:** Kylor · **Date:** 2026-07-20 · **Read time:** ~3 min
**Friday = demo + appetite check, not build approval for the whole program.**

---

> ## Decision requested
> **Primary:** after Friday, if the demo lands, verbal alignment to lift isolation on the filter fix — the GO phrase is `ISOLATION OFF — GO on EBR-40` (Bet A).
> **Explicit:** I am **not** asking for GO on the intelligence layer (EBR-775) or the settings hub (Bet E) in this meeting. Those are context only.

---

## The problem in five lines

Reps don't trust the Sales Portal's numbers, so they rebuild them in Excel. A rep picks their territory and the total on screen doesn't change. When they export, the spreadsheet doesn't match what the portal showed. Open quotes get added into "sales," so the total reads bigger than what we actually invoiced. Until those are fixed, nothing built on top of them is trustworthy — which is why the whole program starts here.

## Headline stats

- **Territory doesn't limit the total.** A rep picks a territory and still sees the whole company — so they export to Excel to get their own accounts (EBR-40 / EBR-212, open since 2022).
- **Export ≠ what's on screen.** The exported total doesn't reconcile to what the portal displayed for the same view (EBR-91).
- **Quotes counted as sales.** Open quotes land inside figures labeled "sales," inflating the total (EBR-87).
- **Intelligence is blocked behind this.** The reporting under EBR-775 is worthless if a filtered total can't be trusted — so trust ships first.
- **Settings sprawl is real but later.** 134 portal settings across 6 layers, no admin screen — that's Bet E, sequenced after the fix (see `PROGRAM-ROADMAP-cycle03.md`).

## Why now

The intelligence work the market keeps asking for only pays off if a filtered total means the same thing on screen, in the export, and in the report. It doesn't today. Fix the total first; everything else compounds on it.

## What we'll show Friday (~10–15 min)

- **Start — Bet A pitch demo** (`../../../design-system/app/sales-portal-bet-a-pitch-demo.html`): Invoices → Customers → Orders → What's broken. Pick a territory and watch the total, the rows, and the "export matches this total" badge move together; flip the bug simulation to show today's behavior.
- **If the room is aligned — full program demo** (`../../../design-system/app/sales-portal-internal-demo.html`): a preview of the intelligence view. **Skip the settings hub unless asked.**
- Point to the decision record (`TRD-Bet-A-filter-truth.md`) and roadmap (`PROGRAM-ROADMAP-cycle03.md`).

## What Bet A ships

- **Territory limits the list and the total** — pick a territory, the total recomputes to only that territory's customers.
- **Export matches the screen** — same filters, same definition, CSV total = on-screen total.
- **Quotes are never counted as sales** — open quotes shown separately from confirmed orders.
- **One invoiced spine** — every total labeled sales is invoiced net, reconciling to the ledger.
- **Answer-first list tabs** — Invoices / Customers / Orders / Reports lead with the answer; these ride **with** Bet A, not as a separate bet.

## Explicit no-gos (not Friday, not this GO)

- Multi-territory rep rewrite (EBR-180 / XL).
- LLM / talk-to-data (EBR-772 / EBR-776).
- A "portal 2.0" grab-bag.
- Verifying territory scoping on **sarreid** — 99.8% multi-territory accounts would surface a separate over-grant; use **wwjc** or a zero-exposure org.
- Shipping "What's broken" as real product navigation — it's a teaching surface only.

## Attachments

| Doc | Purpose |
|---|---|
| This pre-read | Scan before Friday |
| `TRD-Bet-A-filter-truth.md` | Decision record for the filter fix |
| `PROGRAM-ROADMAP-cycle03.md` | Shaped follow-ons — **not** this GO |
| Bet A pitch HTML | Open first |
| Full demo HTML | Friday only — do not pre-explore as "the build" |

## Suggested CTO actions

1. Read this pre-read, then the Bet A decision record (`TRD-Bet-A-filter-truth.md`).
2. Open the Bet A pitch HTML and click through territory + export once.
3. Attend Friday's walk.
4. If it lands, align on `ISOLATION OFF — GO on EBR-40`.
