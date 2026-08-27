---
id: ENG-03
title: Prioritised roadmap — all 31 jobs
version: 1.0
status: ready for engineering
date: 2026-08-27
owner: Kylor Johnson
depends_on: [JTBD-REG, PROD-MAP, PROD-GAPS]
---

# Roadmap — all 31 jobs, ordered

## The reasoning, in five lines

1. **Trust before features.** Fourteen of 31 jobs land on the Sales Portal. A6 fixes the defect that
   undermines every number on it, so it goes first and everything Portal-shaped queues behind it.
2. **Then protect what already works** — JTBD-013, 082, 083, 042 are the only things reps and buyers
   currently rely on. A regression here costs more than any new job earns.
3. **Then no-new-data value, cheapest first** — an aggregation, a small view, a surfaced timestamp.
4. **Then fields we add, by value ÷ effort** — one nullable column that unblocks a whole job beats a
   migration that unblocks a persona.
5. **Client-blocked work is ordered by whether we can start the conversation now**, not by job
   strength. The invoice feed degrades 13 of 31 jobs and is a commercial motion, not a sprint.

**One thing the ordering does not encode: fixing territory-master coverage would unblock more rep
value than any single build below.** `[SQL 2026-08-27]` only **23 of 145** orgs with active iPad reps
have a populated `territories` master, and **935 of 4,058** active reps carry no territory codes at
all. Under the mandatory fail-closed rule those reps see nothing. That is a data-coverage motion
sitting behind seven jobs (012, 021, 022, 024, 033, 062, 063) and it belongs next to the invoice-feed
push, not in an engineering queue.

---

**Rank is a single sequence over all 31 jobs.** Two jobs (031, 061) ship for feed orgs and are
blocked for the rest; they are ranked once, in bucket A, and cross-referenced in bucket C rather than
counted twice.

## A. Ship now — no new data (16 jobs)

| # | JTBD | Persona | Job | Size | Item |
|---:|---|---|---|---|---|
| 1 | **035** | PER-03 | Make the export match the screen | S | **A6 / SERV-2449** — gates trust in every Portal number |
| 2 | **013** | PER-01 | Work the appointment with no connectivity | — | **Protect.** SuperCat's strongest asset; the bar every new component must clear |
| 3 | **082** | PER-08 | Check what I ordered and was billed | — | **Protect.** The one thing ~79% of 17,532 active buyers can already do |
| 4 | **083** | PER-08 | See what I'm entitled to pay | — | **Protect.** eOL's real strength; SEG-03 price-code tail to 35 |
| 5 | **042** | PER-04 | Key an order from phone/email/EDI | — | **Protect.** Already served |
| 6 | **053** | PER-05 | Find where the catalog is broken | S | **A3.** 179,577 of 938,394 active items have no image `[SQL 2026-08-27]` |
| 7 | **032** | PER-03 | Know the team is actually using it | S | **A4, re-scoped** — login-based view, not the `enable_rep_activity` pilot |
| 8 | **063** | PER-06 | Is the sales organisation working | S | **A4**, same build at a different altitude |
| 9 | **084** | PER-08 | Know what's in stock before I promise it | S | **A2.** `max(inventories.updated_at)` is an exact snapshot age |
| 10 | **031** | PER-03 | Get one topline I can defend | S | Honesty labelling only — **STRONG, never FULL**. Ships for the 38 feed orgs |
| 11 | **041** | PER-04 | Reconstruct one account's history fast | — | Coverage, not build. Portal's strongest existing fit |
| 12 | **061** | PER-06 | Know the one true topline | — | Served by Insightful. Untrustworthy until #1 ships — `PER-06` says so explicitly |
| 13 | **033** | PER-03 | Why can't this user see their book | M | **A10.** 134 toggles / 39 flags / 6 layers [F10] — aggregation, no new data |
| 14 | **011** | PER-01 | Know my book before I walk in | L | **The iPad component** — `02-IPAD-ACCOUNT-BRIEF-SPEC.md`. Sequence after SERV-2196 |
| 15 | **081** | PER-08 | Reorder what I know sells | — | **Config, not build.** Cart `enable_online_ordering`, 58 of 257 orgs |
| 16 | **086** | PER-08 | See my own account performance | — | **Config, not build.** `:advanced_reports` 6 orgs → ~13,800 additional active buyers |

**Ranks 15–16 are entitlement decisions, not engineering work.** Both are configuration reaching a
large population rather than a sprint. **JTBD-086 is blocked on a client-risk review, not on job
strength** — pricing-entitlement and competitive exposure are our client's call about their own
customers, and two orgs (`vic`, `clm`) already run it and could be asked directly. JTBD-086 is ranked
last within bucket A deliberately: it has the largest reach in the register and the weakest *decision*
attached. Reach and job-strength are different axes.

---

## B. Needs a field we add (7 jobs)

Ordered by value ÷ effort, per `data-gaps.md` §D.

| # | JTBD | Persona | Job | Needs | Size |
|---:|---|---|---|---|---|
| 17 | **054** | PER-05 | Did the new introduction land | **A1** product launch date — one nullable column | S |
| 18 | **034** | PER-03 | Know the nightly data landed | **A5** push alerting + failure reason codes | S |
| 19 | **014** | PER-01 | Spot the account gone quiet | **A8** per-account baseline / seasonality | M |
| 20 | **062** | PER-06 | Which accounts are quietly slipping | **A8**, same store. SEG-01 lumpy buying needs an account-aware window | M |
| 21 | **044** | PER-04 | Catch the order that will fail | **A7** order-failure reason codes | M |
| 22 | **052** | PER-05 | Which options and finishes get chosen | **A13** normalised option capture. Only 16 CPQ orgs — but CPQ is the named differentiator | L |
| 23 | **051** | PER-05 | Know which products actually sell | **A14** inventory history for sell-through. Ranking ships labelled before that | L |

**A1 has the best ratio in the register** — one nullable date unblocks JTBD-054 entirely; everything
else in that job is already computable. **A8 is the best M** — one store, two jobs, two personas.

**A5 carries a trap worth naming in its ticket:** an `Error` row silently suppresses deletion of
omitted records — a failure that looks like success.

---

## C. Blocked on client data (4 jobs, plus 2 partially blocked)

No surface work fixes any of these.

| # | JTBD | Persona | Job | Blocker |
|---:|---|---|---|---|
| 24 | **012** | PER-01 | See only my territory, and trust it | **Territory master** — empty in 122 of 145 orgs with active reps `[SQL 2026-08-27]`. Full fix also needs **A11** multi-value `RepNumber` (L, EBR-180/SERV-2178, paused) |
| 25 | **015** | PER-01 | Answer "where is my order" | **ERP open-order status.** See correction below |
| 26 | **043** | PER-04 | Answer "where is it" with a defensible date | Same |
| 27 | **085** | PER-08 | Leave a market appointment with an order | Buyer's own browser has none of the iPad's caching. `surface-mapping.md` §5.7: **not solvable by the iPad-EC pattern**, and possibly not without a buyer-side app |
| ↑10 | **031** | PER-03 | Defensible topline — *for the 71 non-feed orgs only* | **Invoice feed.** Order value does not reconcile to a ledger; substituting it defeats the job. Ranked at #10 for the 38 feed orgs |
| ↑12 | **061** | PER-06 | One true topline — *for the 71 non-feed orgs only* | Same, at the highest consequence. **Not even STRONG** without a feed. Ranked at #12 for the 38 feed orgs |

**The invoice feed is the single largest constraint in the register — present for 38 of 109 roster
orgs, degrading 13 of 31 jobs.** The 13 do not fail uniformly: **seven degrade to a usable
order-based view and ship with a mandatory label** (011, 014, 041, 051, 062, 082, 086); **six fail
outright** (015, 043, 021, 023, 031, 061). Onboarding a feed is the highest-leverage single change
available for those 71 accounts, and it is a conversation, not a sprint.

**Correction to `data-gaps.md` B3.** It states ERP ship status / carrier / tracking is *"not in
SuperCat at all, and not on any current integration path."* That is overstated. `[SQL 2026-08-27]`:
`portal_invoices.tracking_number` is populated on **1,121,123 of 4,940,477** invoices across **26
organizations**, with `tracking_carrier` on 744,046 and `ship_via` on 2,712,248, plus a dedicated
`portal_invoice_tracking_records` table. **This does not unblock JTBD-015 or 043** — tracking is
post-invoice and those jobs ask about *open* orders — so both stay in this bucket. B3's conclusion
stands unchanged: **do not build a ship-date promise on data we do not hold.** But a "where did it
ship" answer for already-invoiced orders is available to 26 orgs today and is worth a separate look.

---

## D. Declined this cycle (4 jobs)

| # | JTBD | Persona | Job | Why |
|---:|---|---|---|---|
| 28 | **021** | PER-02 | Agency's whole book with one manufacturer | **No agency entity in the schema** |
| 29 | **022** | PER-02 | Which sub-rep is carrying the line | Same, plus `REP_IDENTITY_TIER` ≥ 2 |
| 30 | **023** | PER-02 | Prove agency value at renewal | Same |
| 31 | **024** | PER-02 | Show a sub-rep what they'll see | Needs **A9** view-as, not the agency entity — **severable**, see below |

**PER-02 is declined this cycle and is not reopened here.** The persona is real — `primary_rep_group`
on 142 of 1,980 user types across 39 orgs, 617 iPad-active — but there is no entity behind it, only a
boolean and **11,873 distinct free-text `company_name` values**. The cost is the migration, not the
schema. There is no partial version: an agency view built on free-text names would silently merge
distinct agencies and split single ones, producing a number that looks authoritative and is wrong.
Under principle 6 that is a **suppress** case, not a degrade case.

**JTBD-024 is the one severable piece.** It needs a scoped-preview mechanism (**A9**, M), not an
agency entity, and A9 also serves **JTBD-033** — which is already in bucket A at #13. If A9 gets
built for 033, 024 comes nearly free. It is a support job rather than the persona's reason to exist,
so it does not change the decline.

---

## Not on this roadmap, deliberately

Six jobs were cut in Phase 2 for absent data and are **kept visible, not deleted** —
`data-gaps.md` §C: rep commission, margin/COGS (three personas), AR/cash, CSAT, returns/RMA. **None
is a roadmap item.** They are recorded so that when someone asks why reps cannot see their
commission, the answer is a documented schema gap with a known cost rather than a shrug.

The most significant is **commission**. A rep is paid on what ships, not what they write, and the
system they use every day cannot tell them what they have earned. That is a finding about the
schema, not about the job. It would need ERP payroll integration. **No current path.**
