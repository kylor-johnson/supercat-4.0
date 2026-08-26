---
id: JTBD-REG
title: JTBD register — all jobs, flat
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
depends_on: [PER-00, PER-01, PER-02, PER-03, PER-04, PER-05, PER-06, PER-08]
---

# JTBD register

**31 jobs across 7 personas.** The flat index; detail lives in the persona files.

Current state: **Not served** · **Partial** · **Served** · **Served badly** (exists but defective).

| ID | Persona | Job (short) | Primary metric | Trigger / cadence | Segment variation | Current state |
|---|---|---|---|---|---|---|
| **JTBD-011** | PER-01 rep | Know my book before I walk in | Invoiced net for this account, T12M vs prior | Pre-appointment, daily | — | **Not served** ⚠️ |
| **JTBD-012** | PER-01 rep | See only my territory, and trust it | % sessions where displayed total matches actual book | Every session | **SEG-02** (median 41 territories) | **Served badly** (EBR-40/212/91) |
| **JTBD-013** | PER-01 rep | Work the appointment with no connectivity | % appointments completed uninterrupted | Every field appointment | **SEG-04** (4,498 products) | **Served** — protect it |
| **JTBD-014** | PER-01 rep | Spot the account gone quiet | # my accounts down >X% on T90D | Weekly planning | — | **Not served** |
| **JTBD-015** | PER-01 rep | Answer "where is my order" | % status questions answered without escalating | Reactive, weekly | — | **Partial** — capped by ERP |
| **JTBD-021** | PER-02 agency | See the agency's whole book with one manufacturer | Agency invoiced net vs prior year | Monthly / contract review | **SEG-02** | **Not served** ⚠️ |
| **JTBD-022** | PER-02 agency | Which sub-rep is carrying the line | Invoiced net per sub-rep | Monthly | — | **Not served** — identity-gated |
| **JTBD-023** | PER-02 agency | Prove agency value at renewal | Agency invoiced net, multi-year | Annual | — | **Not served** |
| **JTBD-024** | PER-02 agency | Show a sub-rep what they'll see | Access issues resolved without escalation | On onboarding | — | **Not served** — authority question |
| **JTBD-031** | PER-03 VP/ops | Get one topline I can defend | Invoiced net, org-wide, period | Monthly close | — | **Served**, STRONG ceiling ⚠️ |
| **JTBD-032** | PER-03 VP/ops | Know the team is actually using it | Reps active in 30d ÷ seats licensed | Monthly | — | **Partial** — gated to 7 orgs |
| **JTBD-033** | PER-03 VP/ops | Why can't this user see their book | Access issues resolved in-house | Reactive | — | **Not served** (F10) |
| **JTBD-034** | PER-03 VP/ops | Know the nightly data landed | # import jobs failed in 24h | Daily, morning | **SEG-04** | **Partial** — reactive only |
| **JTBD-035** | PER-03 VP/ops | Make the export match the screen | Export-to-UI reconciliation rate | Monthly close | — | **Served badly** (EBR-91) |
| **JTBD-041** | PER-04 CS | Reconstruct one account's history fast | % enquiries resolved first contact | Daily, continuous | — | **Served** — best existing fit |
| **JTBD-042** | PER-04 CS | Key an order from phone/email/EDI | Order-entry error rate | Daily, continuous | **SEG-03 vs SEG-04** (price codes) | **Served** |
| **JTBD-043** | PER-04 CS | Answer "where is it" with a defensible date | % answered without escalating | Daily | — | **Partial** — capped by ERP |
| **JTBD-044** | PER-04 CS | Catch the order that will fail | Orders corrected downstream per 1,000 | Per order | — | **Not served** — missing field |
| **JTBD-051** | PER-05 product | Know which products actually sell | Units + invoiced net by item, ranked | Pre-market, biannual | — | **Partial** — Top Products on *ordered* |
| **JTBD-052** | PER-05 product | Which options and finishes get chosen | Order-line count per option value | Pre-market | — (matters only for 16 CPQ orgs) | **Not served** |
| **JTBD-053** | PER-05 product | Find where the catalog is broken | # active items failing completeness | Weekly, urgent pre-market | **SEG-04** (4,498 products / 30 collections) | **Not served** — cheapest new job |
| **JTBD-054** | PER-05 product | Did the new introduction land | Distinct accounts ordering new collection, weekly | Weekly post-market | — | **Not served** — no launch date |
| **JTBD-061** | PER-06 owner | Know the one true topline | Invoiced net with provenance line | Monthly | — | **Served** by Insightful ⚠️ |
| **JTBD-062** | PER-06 owner | Which accounts are quietly slipping | Dollar value at risk from declining accounts | Monthly | **SEG-01** (lumpy project buying) | **Not served** in Portal |
| **JTBD-063** | PER-06 owner | Is the sales organisation working | % licensed reps active in 30d | Quarterly | — | **Partial** — gated to 7 orgs |
| **JTBD-081** | PER-08 buyer ⚠️ | Reorder what I know sells | Buyer-initiated orders as % of all orders | Weekly–monthly | — | **Partial** — Cart in 58 orgs |
| **JTBD-082** | PER-08 buyer ⚠️ | Check what I ordered and was billed | Self-service lookups per inbound CS enquiry | Monthly reconciliation | — | **Served** — protect it |
| **JTBD-083** | PER-08 buyer ⚠️ | See what I'm entitled to pay | % product views showing customer-specific price | Every session | **SEG-03** (price-code spread to 35) | **Served** |
| **JTBD-084** | PER-08 buyer ⚠️ | Know what's in stock before I promise | % buyer orders against in-stock items | Every quote | — | **Partial** — no staleness disclosure |
| **JTBD-085** | PER-08 buyer ⚠️ | Leave a market appointment with an order | Orders written per attending dealer, market week | Market week | — | **Partial** — buyer side not offline |
| **JTBD-086** | PER-08 buyer ⚠️ | See my own account performance | Buyer's invoiced net, trailing 24 months | Quarterly | — | **Not served** — 2 orgs |

⚠️ = the anatomy-vs-spec persona conflict, or a binding honesty ceiling, changes the answer. Flagged, not resolved.

---

## Cuts by the numbers

**31 jobs kept. 20 candidate jobs cut.** Cut reasons, aggregated:

| Reason | Count | Examples |
|---|---:|---|
| **Schema-absent data** — suppress, never estimate | 6 | margin/COGS (×3 personas), AR/cash, commission, CSAT. **Not deleted** — carried in [`../product/data-gaps.md`](../product/data-gaps.md) §C as *job exists, data doesn't* |
| **No decision changes** | 4 | rep leaderboard, recruit sub-reps, CS ticket volume |
| **Wrong system** — ERP, helpdesk, or the dealer's own | 5 | shipment tracking, pricing strategy, retail inventory |
| **Cross-client / governance** | 3 | assortment benchmarking, cross-manufacturer comparison, competitor comparison |
| **Against our client's interest** | 1 | buyer comparing prices across manufacturers |
| **False precision** | 1 | splitting buyer into dealer/designer/contract |

---

## Segment variation — the headline result

**4 of 31 jobs vary by Account Segment. 27 do not.**

| JTBD | Persona | Variation, and the measured basis |
|---|---|---|
| JTBD-012 | rep | **SEG-02** — highest median territory count (41); territory scoping is load-bearing for broad dealer networks |
| JTBD-013 | rep | **SEG-04** — median 4,498 products, 5,759 orders; cache size and sync duration are a different problem |
| JTBD-053 | product | **SEG-04** — largest catalogs, least structure (median 30 collections); manual QA doesn't scale |
| JTBD-083 | buyer | **SEG-03** — widest price-code spread (median 2, tail to 35); entitlement is genuinely hard |

Three more are noted inside persona files as *conditional rather than variant*: JTBD-021 (SEG-02
agency aggregation), JTBD-042 (SEG-03 vs SEG-04 price-code complexity), JTBD-062 (SEG-01 lumpy
buying breaks a naive decline rule).

**The finding: one surface serves everyone for the overwhelming majority of jobs.** Where variation
exists it is driven by **catalog scale, territory count and price-code count** — structural facts
that can be read off a single org's own data — **not by the selling-motion segment as such.** A job
does not need to know whether an org is Luxury Specification; it needs to know how many price codes
and products the org has. **Build the surface once, parameterise on the org's own structure, and do
not condition on segment.** That is simpler, cheaper, and better supported than the alternative —
which matters given Layer A reproduces at 38.5% against a 34.9% baseline.

---

## Cross-cutting dependencies

Four items block or degrade many jobs at once. Ranked by blast radius:

| Blocker | Jobs affected | Note |
|---|---|---|
| **Invoice feed present for only 38 of 109 roster orgs** | 011, 014, 015, 021, 023, 031, 041, 043, 051, 061, 062, 082, 086 — **13 jobs** | The single largest constraint in the register. Not a build problem; a client data problem |
| **Territory master empty in 32 of 55 orgs** [F11] | 012, 021, 022, 024, 033, 062, 063 — **7 jobs** | Fail-closed is mandatory: never fall back to whole-org |
| **No agency entity in the schema** | 021, 022, 023, 024 — **all of PER-02** | This persona cannot be served at all without it |
| **`enable_rep_activity` on 7 of 257 orgs** | 032, 063 | Data exists; the surface is switched off |

Full data-work backlog: [`../product/data-gaps.md`](../product/data-gaps.md) (Phase 3).
