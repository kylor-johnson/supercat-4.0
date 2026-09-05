# COPY AUDIT — Sales Portal mocks (industry voice, pre-CTO ship)

**Date:** 2026-07-20
**Scope:** User-visible copy only in the two Sales Portal HTML mocks. Layout, IDs,
`data-view`, filter behavior, and live stamp numbers ($16.02M / $16,022,554, 11,730,
45,494, backlog $77.8M) untouched.

**Files edited:**
1. `design-system/app/sales-portal-bet-a-pitch-demo.html`
2. `design-system/app/sales-portal-internal-demo.html`

**Authority:** `Insightful Product 4.0/knowledge/communication_guideline.md`
(gold-stamp test, anti-SaaS bar, pre-send checklist) and
`Insightful Product 4.0/knowledge/industry_context.md` (native vocabulary, anti-cute).

---

## Summary — before/after philosophy

The mocks were written in the voice of an internal RevOps product team: the customer
list was "the book," the big number on a card was "the hero," the invoiced ledger total
was "True Topline," fading accounts were "Quietly dying" a "decay cohort," and territory
filtering "scoped the book." That is dashboard-explanation voice — it narrates the
product's own machinery and reaches for clever labels the data can't back up. A furniture
or lighting sales manager doesn't say any of it. The rewrite swaps every internal/SaaS
label for the plain thing a manufacturer's sales ops person would say out loud: **the
list**, **the total**, **invoiced sales**, **accounts fading**, and filters that **limit
the list and total to a territory**. Numbers, names, and behavior are unchanged; only the
words a client can read moved — from "how the system works" to "what you're looking at."

---

## Every material change

### `sales-portal-bet-a-pitch-demo.html`

| Location | Old phrase | New phrase | Rationale |
|---|---|---|---|
| Invoices · page meta | `filter truth home` | `invoiced totals · territory + export` | "filter truth" is internal product jargon; say what the page shows. |
| Invoices · prov pill | `Fixed path · book scoped` | `Fixed path · territory limits the total` | "book scoped" → territory limiting a total (plain). |
| Invoices · export card | `CSV sum = hero` | `CSV sum = invoiced total` | "hero" is a UI label, not a client word. |
| Invoices · path pill | `Fixed · filter scopes the book` | `Fixed · filter limits the list and total` | Drops "scope"/"book". |
| Invoices · list footer | `hero + feed both collapse` | `total + feed both collapse` | Drops "hero". |
| Customers · page meta | `1,417 custs in LTM book` | `1,417 customers in trailing 12 months` | Drops "book" + "custs" abbrev. |
| Customers · question | `How much did this book sell?` | `How much did these customers buy?` | "the book" → the customers; native. |
| Customers · feed head | `Customer book` | `Customers in view` | Drops "book". |
| Orders · question | `What's on the books — excluding quotes?` | `What's confirmed — excluding quotes?` | "on the books" → confirmed orders (clearer). |
| Orders · quotes card | `Pipeline only. …` | `Open quotes only — not sales. …` | "Pipeline only" → open quotes (quotes context OK as "Open quotes"). |
| What's broken · intro | `can't trust the book` | `can't trust the numbers` | Drops "book". |
| What's broken · hint | `Fixed shrinks the book` | `Fixed limits it to that territory` | Plain rep English. |
| What's broken · territory option | `All territories (rep's book)` | `All territories (all your accounts)` | Drops "rep's book". |
| What's broken · row 1 head | `Territory pick doesn't change the book` | `Picking a territory doesn't change what I see` | Rep's-own-words framing (§rule 6). |
| What's broken · row 3 broken | `Pipeline / quote rows inflate sales so the book looks bigger than the ledger.` | `Open quotes get counted as sales, so the total looks bigger than what you actually invoiced.` | Drops "pipeline"/"book"/"ledger" jargon. |
| Stub panel | `filter truth on list tabs … + export reconciliation + quotes ≠ sales` | `filters that limit every total … + export that matches the screen + quotes never counted as sales` | Plain restatement of Bet A. |
| JS `TRUST_SCOPE.all.note` | `full book` | `all territories` | Rendered in Fixed result line. |
| JS `applyTrustFilter` pill | `Fixed · book scoped` | `Fixed · territory limits the list` | Consistency. |
| JS `onCustFilters` illust | `Fixed path · feed scoped` | `Fixed path · feed limited to territory` | Drops "scoped". |
| JS `onInvFilters` export note | `Export ≠ hero …` / `CSV sum = hero …` | `Export ≠ invoiced total …` / `CSV sum = invoiced total …` | Drops "hero". |
| JS `onInvFilters` pill | `Fixed · filter scopes the book` | `Fixed · filter limits the list and total` | Consistency. |
| JS `onInvFilters` prov | `Fixed path · book scoped ·` | `Fixed path · territory limits the total ·` | Consistency. |

### `sales-portal-internal-demo.html`

Same list-tab changes as above (Invoices meta/prov/export/pill/footer, Customers
question/feed head, Orders question/quotes card, What's broken intro/hint/option/row1/row3,
and the matching JS strings), plus:

| Location | Old phrase | New phrase | Rationale |
|---|---|---|---|
| Customers · risk rail label | `Quietly dying · jump to Intelligence` | `Accounts fading · jump to Intelligence` | Anti-cute; state the fact. |
| Customers · risk rail sub | `Live-stamped decay cohort` | `Live-stamped flagged accounts` | "cohort" → "flagged accounts". |
| Customers · risk rail rows | `$400K at risk` / `$285K` / `$184K` | `$400K LTM` / `$285K LTM` / `$184K LTM` | "at risk" is the account's LTM still on the books. |
| Customers · feed row pills (×3) | `Quietly dying` (button) | `Fading` | User-facing label must not say "Quietly dying". |
| Customers · footnote | `Quietly dying rail` | `Accounts fading rail` | Consistency. |
| Invoices · footnote | `Export = hero` | `Export = invoiced total` | Drops "hero". |
| Intelligence · Hero 1 eyebrow | `Hero 1 · True Topline (C1)` | `Invoiced sales · ledger total (C1)` | Drops "Hero"/"True Topline". |
| Intelligence · Hero 2 eyebrow | `Hero 2 · Quietly dying (S1 · EBR-198)` | `Accounts fading (S1 · EBR-198)` | Product ref kept; cute headline dropped (§rule 5). |
| Intelligence · S1 summary | `$1.69M at risk (LTM on flagged)` | `$1.69M LTM on flagged accounts` | Restate "at risk" as LTM. |
| Intelligence · S1 table header | `At risk` | `LTM on account` | Column is LTM still invoiced on the account. |
| Intelligence · footnote | `$1.69M decay` | `$1.69M fading` | Consistency with "Accounts fading". |
| Dashboard · caveat note | `Hub chrome ≠ filter truth. … over-grant live.` | `The dashboard header doesn't limit totals yet. … over-grants live.` | Drops "chrome"/"filter truth" jargon. |
| JS `onDashTerritory` | `Chrome doesn't scope yet` | `Header doesn't limit totals yet` | Drops "chrome"/"scope". |

**Not changed (intentional):** CSS/JS identifiers (`hero-grid`, `dying-pill`, `is-dying`,
`is-pipeline`, `is-risk`), `data-view`/element IDs, footnote ticket refs (EBR-40 / 212 /
91 / 87 / 198, FILTER-TRUTH-AC.md, IR-v1-QUERIES.md — allowed for eng), live stamp numbers,
and the "Backlog · not sales" / "quotes ≠ sales" metric-law lines (already correct voice).

---

## Approved phrase list (canonical strings for the CTO/Bet A story)

Use these verbatim as the shared vocabulary. They pass the gold-stamp test and match the
mocks after this audit:

1. **Invoiced sales** — the total we actually invoiced (net), reconciles to the ledger.
2. **Invoiced total** — the on-screen number a filter produces (was "hero").
3. **Ledger total (C1)** — invoiced sales for the range; not the warehouse rollup.
4. **The list and the total** — what a filter limits (was "the book").
5. **Territory limits the list and total** — what a working territory filter does.
6. **Only your territory's customers** — what a rep sees when territory is applied.
7. **All your accounts / all territories** — the unfiltered view (was "rep's book").
8. **Export matches the screen** — same filters, same definition, CSV = on-screen total.
9. **Open quotes — not sales** — quotes are never counted in sales/confirmed.
10. **Confirmed orders / backlog — not sales** — open orders stay labeled backlog.
11. **Accounts fading** — accounts down materially vs the prior six months (was "Quietly dying").
12. **LTM on account** — trailing-12-month invoiced still on a fading account (was "at risk").
13. **Flagged accounts** — the set S1 surfaces to call (was "cohort").
14. **Picking a territory doesn't change what I see** — the rep's plain statement of today's bug.
15. **The dashboard header doesn't limit totals yet** — the honest caveat (was "chrome ≠ filter truth").

---

## Pre-send checklist ticks (communication_guideline §Pre-send)

- **Machinery pass** (§6 — no "system/platform/dashboard/chrome" narrating itself):
  ✅ Removed "filter truth home," "Hub chrome ≠ filter truth," "Chrome doesn't scope,"
  and "hero" as a UI label. "Dashboard/header" remains only where it names a real screen,
  not the mechanism.
- **Cute pass** (§3 — no metaphor/idiom/clever label; use the literal number/fact):
  ✅ "Quietly dying," "True Topline," and "decay cohort" replaced with "Accounts fading,"
  "Invoiced sales · ledger total," and "flagged accounts." No metaphor survives as a label.
- **Jargon pass** (native vocabulary, industry_context §Vocabulary):
  ✅ "the book," "scope the book," "book scoped," "Pipeline only," "at risk," "custs,"
  and "cohort" replaced with plain sales-ops language (list/total/territory/accounts/
  open quotes/LTM). Kept true industry terms already present (invoiced net, backlog, quotes).

**Residual (allowed):** eng ticket refs and file names in footnotes (EBR-*, FILTER-TRUTH-AC.md,
IR-v1-QUERIES.md), and internal metric shorthand kept only in footnotes/eng-facing lines.
