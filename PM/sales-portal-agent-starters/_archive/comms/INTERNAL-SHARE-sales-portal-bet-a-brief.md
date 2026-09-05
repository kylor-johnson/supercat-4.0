# Sales Portal — Bet A (Filter Truth) · Internal Brief

| | |
|---|---|
| **Owner** | Kylor |
| **Date** | July 20, 2026 |
| **Status** | Review for show-and-tell · **Isolation ON** · NOT ready to build until explicit GO |
| **Read time** | ~8 min (this doc) · ~3 min (decision record) |
| **Friday** | Demo + appetite check — **not** build approval for the whole program |

---

> **How to read this pack**
>
> What you're looking at here is the **decision layer** — the TRD for Bet A (filter truth). That's the doc I'd want someone to read before we talk GO.
>
> The full eng spec is done too. I left it off this attach list on purpose so you're not staring at a wall of Rails. It's `ENG-HANDOFF-bet-a-b-c-e.md`: AC→code file:line maps, the read-model schema, test plan, and PR batches for Bet A, B, C, and E. Happy to send it over if you want to dig into the dev side.
>
> **Nothing's been built yet.** Isolation is still on until you give the GO.

---

## Decision requested

| | |
|---|---|
| **Primary ask** | After Friday, if the demo lands — verbal alignment to lift isolation on the filter fix |
| **GO phrase (verbatim)** | `ISOLATION OFF — GO on EBR-40` |
| **Not in this GO** | Intelligence layer (EBR-775 / Bet C) · Settings hub (Bet E) · LLM / talk-to-data (Bet D) |

---

## The problem in five lines

Reps don't trust the Sales Portal's numbers, so they rebuild them in Excel.

1. A rep picks their territory and the **total on screen doesn't change**.
2. When they export, the **spreadsheet doesn't match** what the portal showed.
3. **Open quotes get added into "sales,"** so the total reads bigger than what we actually invoiced.
4. Until those are fixed, **nothing built on top of them is trustworthy** — which is why the whole program starts here.
5. The intelligence work the market keeps asking for only pays off if a filtered total means the same thing on screen, in the export, and in the report. It doesn't today.

---

## Headline stats

| Issue | Ticket(s) | What reps experience |
|---|---|---|
| Territory doesn't limit the total | EBR-40, EBR-212 (open since 2022) | Pick a territory, still see the whole company — export to Excel to filter themselves |
| Export ≠ what's on screen | EBR-91 | CSV total doesn't reconcile to the on-screen total for the same view |
| Quotes counted as sales | EBR-87 | Open quotes land inside figures labeled "sales," inflating the total |
| Intelligence blocked behind this | EBR-775 | Reporting is worthless if a filtered total can't be trusted — trust ships first |
| Settings sprawl is real but later | Bet E | 134 portal settings across 6 layers, no admin screen — sequenced after the fix |

---

## What Bet A ships

**Appetite:** small batch — a fixed, single-cycle fix, not a territory data-model rewrite. Fixed time, variable scope.

| Outcome | Detail |
|---|---|
| **Territory limits the list and the total** | Pick a territory → total recomputes to only that territory's customers |
| **Export matches the screen** | Same filters, same definition — CSV total = on-screen total (± rounding) |
| **Quotes are never counted as sales** | Open quotes shown separately from confirmed orders |
| **One invoiced spine** | Every total labeled sales is invoiced net, reconciling to the ledger |
| **Answer-first list tabs** | Invoices / Customers / Orders / Reports — ship **with** Bet A, not as a separate bet |

**Done means:** on a named production org, picking a territory limits both the list and every total on that surface to only that territory's customers; the export reconciles to the on-screen total for the same view; open quotes are never counted as sales; and every total labeled sales is invoiced net. When that's true, the intelligence answers that follow (Bet C) have a trustworthy total to reconcile against.

**Surfaces in scope:** invoice list, dashboard territory control, customers list, and any summary tile driven by that filter.

---

## Metric law (immutable)

Every portal total labeled sales, and every report answer that follows, obeys this — restated in code, not re-derived:

- **Sales = invoiced net** (`SUM(portal_invoices.net_amount)`), over a window anchored on the report-through date (never a bare "today"), with a $5M single-row cap.
- **Confidence ceiling is STRONG** — a single invoice feed; never claimed as complete.
- **Quotes are never sales** — open quote rows excluded from anything labeled sales or confirmed.
- **Export equals the screen** — one definition and one scope for both, not a second number.
- **Backlog is not sales** — open-order figures may exist but stay labeled backlog/open.
- **EBR-7 is already answered** — discounts are already reflected in invoiced net; close the ticket, don't build a discount engine.

> **Eng footnote:** the warehouse dashboard rollup is not the validation ground truth — label it "invoiced ledger."

---

## Acceptance criteria (summary)

Full Given/When/Then lives in `FILTER-TRUTH-AC.md` (AC-A1…A4) and `LIST-TABS-AC.md`.

| AC | What it proves |
|---|---|
| **A1 — Territory limits the list and total** | Selecting a territory scopes rows and every total. "All territories" = union of the rep's assigned territories, not the whole company. Unterritoried rep with no all-customer permission **fails closed** — empty view, never full company. |
| **A2 — Export reconciles** | Export sum = on-screen total for the same date range, territory, and customer scope (± rounding). Both use invoiced net. |
| **A3 — Quotes never in sales** | Quote rows excluded from any figure labeled sales, invoiced, or confirmed. Backlog labeled backlog, never sales. |
| **A4 — Metric-law spine** | Invoiced net only, report-through-date clamped, $5M cap, STRONG ceiling — same definition Bet C will reconcile to. |

---

## Explicit no-gos (not Friday, not this GO)

- Multi-territory rep rewrite (EBR-180 / XL)
- LLM / talk-to-data (EBR-772 / EBR-776)
- A "portal 2.0" grab-bag
- Verifying territory scoping on **sarreid** — 99.8% multi-territory accounts would surface a separate over-grant; use **wwjc** or a zero-exposure org
- Shipping "What's broken" as real product navigation — it's a teaching surface only
- New intelligence answers (Bet C) — gated on this fix landing first
- iPad tickets and the iPad/eOL date filter (different surface from portal Customers date fix)

---

## Rabbit holes & patches

| Risk | Patch |
|---|---|
| **sarreid** has 99.8% multi-territory accounts | Verify on **wwjc** or a zero-exposure org; don't demo territory scoping on sarreid until over-grant path is honest |
| Ship-to over-grant (SERV-2196 class) | Sequence after the fail-closed guard (SERV-2178); default preserves current behavior until then |
| 32 of 55 orgs have an empty territory master | No invented rollups; unterritoried rep still fails closed rather than seeing the whole company |
| Dashboard warehouse rollup ≠ invoiced ledger | Label it "invoiced ledger"; intelligence AC uses invoiced net only |

**Verify org:** **wwjc is the trust flagship** — intersection of both territory bugs. Recommended eng order: fail-closed leakage guard → ship-to over-grant fix → Customers date-aware block.

---

## What we'll show Friday (~10–15 min)

1. **Start — Bet A pitch demo**
   - File: `design-system/app/sales-portal-bet-a-pitch-demo.html`
   - Walk: Invoices → Customers → Orders → What's broken
   - Pick a territory and watch the total, the rows, and the "export matches this total" badge move together
   - Flip the bug simulation to show today's behavior

2. **If the room is aligned — full program demo**
   - File: `design-system/app/sales-portal-internal-demo.html`
   - Preview of the intelligence view
   - **Skip the settings hub unless asked**

3. Point to the decision record and roadmap (links below)

---

## Program context (not this GO)

One program, one order of operations: **trust first → modern UX → computational intelligence → inferential later.**

| Bet | What it is | Sequence | GO phrase |
|---|---|---|---|
| **A** | Filter truth — territory, export, quotes | **First (this GO)** | `ISOLATION OFF — GO on EBR-40` |
| **B** | Answer-first list tabs | Rides with A | (with A) |
| **C** | Computational Intelligence Report v1 | After A | `ISOLATION OFF — GO on EBR-775` |
| **D** | LLM / talk-to-data | Parked | — |
| **E** | Portal & Access settings hub | Shaped; Wave 0–1 may ride with A | `ISOLATION OFF — GO on Bet E` |

Bet C heroes (after A): C1 invoiced topline · S1 quietly dying accounts · Team strip (behavior floor). Bet E collapses 134 settings / 6 layers into one Portal & Access hub. Full detail: `PROGRAM-ROADMAP-cycle03.md`.

---

## Eng spec (available on request)

The implementation source of truth is **`ENG-HANDOFF-bet-a-b-c-e.md`**. I kept it out of the default attach list so this brief stays readable — ask and I'll send it if you want to review the dev work.

| What's in the eng handoff | |
|---|---|
| AC → code file:line maps | Bet A territory/export/quotes fixes with verified Rails cites |
| Read-model schema | Bet C IR v1 JSON contract (C1, S1, team strip) |
| Test plan | Staging verify checklist tied to AC ids (A, B, C, E) |
| PR batches | 7-batch sequencing after GO — trust core → surfaces → settings waves → IR |

**GO gates (verbatim phrases):**

| GO phrase | Ships |
|---|---|
| `ISOLATION OFF — GO on EBR-40` | Bet A + Bet B list-tab shell |
| `ISOLATION OFF — GO on EBR-775` | Bet C IR v1 |
| `ISOLATION OFF — GO on Bet E` | Bet E full hub |
| `ISOLATION OFF — GO on Bet E Wave 0` | Bet E small-batch (5 dead flag deletes + graduations) |

No GO = spec only. AC freeze ≠ isolation lift. **No `supercat-code/` edits until GO.**

---

## Document index

| Doc | Purpose | In default attach? |
|---|---|---|
| **This brief** | Scan before Friday / internal share | ✅ |
| `TRD-Bet-A-filter-truth.md` | Decision record for the filter fix | ✅ |
| `PROGRAM-ROADMAP-cycle03.md` | Shaped follow-ons — **not** this GO | ✅ |
| `CTO-PREREAD-friday-show-and-tell.md` | Shorter CTO scan (~3 min) | Optional |
| `ENG-HANDOFF-bet-a-b-c-e.md` | Full eng spec — AC→code, schema, tests, PR batches | **On request** |
| Bet A pitch HTML | Open first for demo | ✅ |
| Full demo HTML | Friday only — program preview | Optional |

**Authority chain (for eng):** `FILTER-TRUTH-AC.md` · `LIST-TABS-AC.md` · `INSIGHT-IR-v1-AC.md` · `SETTINGS-hub-v1-AC.md` · `cycle-01-outputs/FIX-diagnosis-territory-datefilter.md`

---

## Open questions for the room

1. **Verify org** — confirm wwjc as the trust flagship, or name a preferred zero-exposure org.
2. **Wave 0 settings alongside?** — do the safe settings-cleanup deletes (Bet E Wave 0) ride the same cycle as Bet A, or wait?
3. **Customers date-filter appetite** — the portal Customers date dropdown currently does nothing for most ranges; include the date-aware fix in this bet's scope, or fast-follow?

---

## Suggested actions

- [ ] Read this brief, then the Bet A decision record (`TRD-Bet-A-filter-truth.md`)
- [ ] Open the Bet A pitch HTML and click through territory + export once
- [ ] Attend Friday's walk
- [ ] If it lands, align on `ISOLATION OFF — GO on EBR-40`
- [ ] (Optional) Request `ENG-HANDOFF-bet-a-b-c-e.md` for dev review

---

*Cycle 03 · Sales Analytics program · Isolation ON until explicit GO*
