---
id: MEAS-04
title: Line C — measured reach per job, and where it disagrees with the roadmap
version: 1.0
status: evidence pack
date: 2026-08-31
database: supercatprod
depends_on: [MEAS-03, ENG-03]
---

# Line C — reach, measured

The register carries inherited S / M / L effort sizes. It has no measured **reach**. This supplies
one: per job, how many orgs, how many users, and how many transactions per period it touches.

Effort sizes below are quoted from `../engineering/03-ROADMAP.md` unchanged — this pass measured
reach, not cost. Every disagreement with the roadmap's rank order is flagged **⚠**.

---

## The reach table

Users are given as **records**, with people in brackets where the distinction matters (Q051–Q053).

| Rank (roadmap) | JTBD | Orgs reached | Users reached | Transactions / period | Effort | Query |
|---:|---|---:|---:|---|---|---|
| 1 | **035** export/UI | 50 (Portal flag on) · 37 paying | 2,490 internal | every Portal number | S | Q002, Q060 |
| 2 | 013 offline | 144 | 4,026 (2,141 people) | 139,513 iPad orders/yr | protect | Q001, Q014 |
| 3 | 082 order+invoice history | 27 | **17,599 buyers** | 1.28M ERP orders/yr | protect | Q017, Q030 |
| 4 | 083 entitled price | 31 | **18,057 buyers** | every session | protect | Q017 |
| 5 | 042 order entry | ~111 | internal, not isolable | 178,944 orders/yr | protect | Q041 |
| 6 | **053** catalog completeness | **241** | internal, not isolable | 153,084 image + 98,441 price gaps | S | Q005, Q046 |
| 7 | 032 rep activity | 50 | 2,490 internal | 2,806 zero-order reps flagged | S | Q010 |
| 8 | 063 org health | 50 | small (owner) | same | S | Q010 |
| 9 | **084** stock age | 48 Cart orgs | **17,550 buyers** — but only **205** see stale data | 687,455 inventory rows | S | Q033, Q034 |
| 10 | 031 topline | **44 live-feed** (not 48) | 2,490 internal | $672.5M invoiced base | S | Q003, Q020 |
| 11 | 041 account history | 43 | internal, not isolable | 167,884 orphan orders/yr | coverage | Q030 |
| 12 | 061 owner topline | 44 live-feed | small | same | — | Q003 |
| 13 | 033 access debug | 258 | 2,460 admin | — | M | Q001 |
| 14 | **011** account brief | **20** | **655 (559 people)** | — | L | Q004, Q052 |
| 15 | **081** reorder | **31 of 55 Cart orgs have buyers** | **18,057 buyers (96.2%)** | 39,422 web orders/yr | config | Q014, Q017 |
| 16 | **086** buyer history | **24** | **17,522 ceiling** | — | config | Q062 |
| 17 | 054 launch landed | 119 | internal | 19,197 collections/yr | S + A1 | Q035 |
| 18 | 034 import alerts | **107** | 2,460 admin | **6,092 errors / 30d in 71 orgs** | S + A5 | Q043 |
| 19 | 014 fading account | 40 | 353 producing reps | **23,243 at-risk accounts** | M + A8 | Q037 |
| 20 | 062 slipping accounts | 40 | small (owner) | same, $112.9M | M + A8 | Q037 |
| 21 | 044 failing order | **16** | internal | **1,862 orders/yr** | M + A7 | Q041 |
| 22 | 052 option choice | **92 hold data · 7 have cascade** | internal | not captured | L + A13 | Q039 |
| 23 | 051 sell-through | 44 live-feed | internal | needs history | L + A14 | — |
| 24 | 012 territory scope | **143 affected** | **3,371 (1,808 people)** | 27.3M exposed record-pairs | blocked | Q004, Q038 |
| 25–27 | 015 / 043 order status | **43** | internal + buyers | 1.28M rows, 125 statuses | blocked → **re-test** | Q031, Q032 |
| 28–31 | 021–024 agency | 42 | 590 agency reps | — | declined | Q070 |

---

## Where reach disagrees with the roadmap rank ⚠

### ⚠ 1. JTBD-081 and 086 are ranked last in bucket A and have the largest reach in it

The roadmap puts the two buyer configuration items at **15 and 16 of 16**, explicitly acknowledging
that 086 "has the largest reach in the register and the weakest *decision* attached." The measurement
strengthens that tension considerably:

- **081 reaches 18,057 active buyers (96.2% of the entire buyer base)** — Cart is already switched on
  at orgs holding nearly all of them. The roadmap's "55 of 258 orgs" framing makes this look like a
  minority capability. By users it is near-universal. `MEASURED` Q017
- **086's ceiling is 17,522** — 93.4% of active buyers. `MEASURED` Q062
- And buyer web ordering is **the fastest-growing channel in the system, +29.2% over eight quarters
  against +10.2% for iPad**. `MEASURED` Q054

Against that, **JTBD-011 — the flagship rep component, effort L — reaches 655 records / 559 people in
20 orgs.** That is 28× fewer users than 081 at incomparably higher cost (32× on people).

`JUDGMENT`: reach is not job strength, and the roadmap is explicit that it ranks on strength. But
the gap here is two orders of magnitude on users and it runs the same direction as the growth trend.
**The ordering of bucket A deserves an explicit revisit rather than a footnote.**

### ⚠ 2. JTBD-053's reach is the widest of any build item — 241 orgs

Catalog completeness touches **241 orgs** — more than any other item on the roadmap, and 2× the
active-client universe because it includes orgs with catalogs but no recent orders. It is ranked 6th
and sized S. **On reach ÷ effort it is the strongest item in the register**, and the roadmap's own
logic ("no-new-data value, cheapest first") points at it.

The caveat from `03-JOB-DEMAND.md` applies: the spec must change (drop category/collection checks,
make the price check org-relative, exclude test orgs) or it ships ~118,000 false positives.

### ⚠ 3. JTBD-034 reaches 107 orgs and sits at rank 18, behind items reaching 20–44

Import errors hit **71 orgs in 30 days**. The job is ranked 18 because it needs A5. But its *problem*
reach is third-widest in the register, behind only 053 (241) and 033 (258). `MEASURED` Q043

### ⚠ 4. JTBD-044 is ranked 21 on a problem of 1,862 orders in 16 orgs

The smallest measured problem of any build item. The register put it in bucket B needing A7
(failure reason codes) — and those partly exist already (Q041). Both facts point the same way:
**this is the weakest build case in the register, and should be ranked below 052 rather than above
it.** `MEASURED` Q041, Q042

### ⚠ 5. JTBD-031 and 061 ship for 44 orgs, not 48

The roadmap says both "ship for the 38 feed orgs." Measured, 48 active orgs have *any* invoice row
but only **44 have one dated in the last 12 months** (Q003). A defensible topline needs a *current*
feed. Twelve orgs have a feed that has stopped, and shipping a topline to them would produce
confidently stale numbers — precisely the failure mode JTBD-031's honesty ceiling exists to prevent.

### ⚠ 6. JTBD-084's reach is 48 orgs but its *problem* reaches 205 buyers

Ranked 9 and sized S, which is fine. But the roadmap's implicit justification — that buyers are being
misled by stale stock — is measured at **205 buyers**, because 90.2% of buyers sit at orgs refreshing
within 2 days (Q034). Ship it as a cheap correctness improvement, not as a buyer-trust initiative.

### ⚠ 7. JTBD-052's reporting reach is 92 orgs, not 16

The roadmap ranks 052 at 22 (effort L) partly because it "matters only for 16 CPQ orgs." Option data
exists at **92 orgs**; the configurator cascade at **7**. Neither is 16. The job's reach depends
which is meant, and the roadmap's rationale should name it. `MEASURED` Q039

---

## Reach ÷ effort, measured

Restricting to items where both reach and effort are known, and using active users touched:

| JTBD | Users reached | Effort | Verdict |
|---|---:|---|---|
| **081** reorder | 18,057 | config | **Highest reach per unit effort in the register** |
| **086** buyer history | 17,522 | config | Second — blocked on client risk, not engineering |
| **083 / 082** | 17,599–18,057 | protect | Highest-value things to not break |
| **053** completeness | 241 orgs | S | **Best build ÷ effort**, once re-specified |
| **084** stock age | 17,550 (205 affected) | S | Cheap, correct, low impact |
| 032 / 063 | 2,490 | S | Good |
| **011** account brief | 655 (559 people) | **L** | **Worst reach ÷ effort of any build item** |
| 012 territory | 3,371 blocked | client data | Highest *unlock* value — and not engineering work |

**The single largest reach-to-effort item in the register is a configuration change we have ranked
last, and the lowest is the flagship build.** That is not an argument to cancel the rep component —
`02-PERSONA-EVIDENCE.md` shows band C reps are a real, valuable population — but it is the
comparison the CEO readout should carry, stated plainly.
