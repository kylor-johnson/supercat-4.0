---
id: MEAS-05
title: Line D — the two client-data gaps in commercial terms
version: 1.0
status: evidence pack
date: 2026-08-31
database: supercatprod
---

# Line D — what the two gaps actually cost, and who to call

The register asserts these two gates "more value than the entire build list." That is a claim about
magnitude with no magnitude attached. Here it is.

Universe throughout: the **112 orgs** with any non-deleted order in the trailing 12 months (Q003).

---

## Gap 1 — the invoice feed

`MEASURED` · Q020

| | Has a feed | **No feed** |
|---|---:|---:|
| Orgs | 48 | **64** |
| Orders, 12m | 145,358 | **33,578** (18.8%) |
| Order value, 12m | $672.5M | **$126.9M** (15.9%) |
| **Active reps** | 1,947 | **1,893 — 49.3% of the rep base** |
| **Active buyers** | 17,599 (93.8%) | **1,164 — 6.2%** |
| Customer records | 456,237 | **211,841** |
| Also have a territory master | 22 | **2** |

### The finding the register does not have

**The invoice-feed gap costs us half the rep base and almost none of the buyer base.**

Buyer-heavy orgs are already fed — 93.8% of active buyers sit behind a feed. So the 13 jobs the
register says are degraded do not degrade for the buyer population at all; they degrade for reps and
for internal leadership. That makes the feed push a **rep-enablement motion**, not a universal
unblock, and it is the smaller half of the business by dollars.

It also means the six jobs that "fail outright" without a feed (015, 043, 021, 023, 031, 061) fail
for a population of 1,893 reps and the leadership of 64 orgs — real, but a different and more
specific claim than "13 of 31 jobs degraded."

### A second gap inside the first

**Only 44 of the 56 feed orgs have an invoice dated in the last 12 months** (Q003). Twelve feeds have
stopped. For any job that asks "what happened this year," coverage is **44 of 112 (39%)**, not 48.
Those twelve are a cheaper conversation than the 64 — the integration exists and has lapsed.

### The target list — where the commercial push goes

`MEASURED` · Q021, Q022 · full list in `data/Q021.csv`

**64.1% of the missing order value sits in 6 orgs. 74.6% sits in 10.**

| # | Org | Name | Orders 12m | Order value 12m | Active reps | Active buyers |
|---:|---|---|---:|---:|---:|---:|
| 1 | `uhc` | Uniware Housewares Corp. | 3,780 | **$21.8M** | 16 | 0 |
| 2 | `wag` | Wendover Art Group | 3,385 | **$16.2M** | 45 | 0 |
| 3 | `mpc` | Pioneer Morton | 5,623 | **$15.6M** | 9 | 45 |
| 4 | `kii` | Kennedy International, Inc. | 2,640 | **$13.6M** | 17 | 15 |
| 5 | `wac` | WAC/Modern Forms Lighting | 1,693 | **$7.3M** | **98** | 0 |
| 6 | `ah` | Alfresco Home | 1,137 | **$6.8M** | 32 | 245 |
| | | **Top 6 subtotal** | | **$81.4M (64.1%)** | 217 | 305 |
| 7 | `da` | Dainolite Ltd. | 4,335 | $4.8M | 28 | 0 |
| 8 | `fms` | Visual Comfort – Studio/Fans | 949 | $2.9M | 79 | 1 |
| 9 | `vcg` | Visual Comfort Signature | 496 | $2.9M | 69 | 0 |
| 10 | `tla` | Visual Comfort – Modern | 210 | $2.7M | 70 | 0 |
| | | **Top 10 subtotal** | | **$94.7M (74.6%)** | | |

**Two things jump out of this list.**

1. **Three of the top ten are Visual Comfort entities** (`fms`, `vcg`, `tla`) with 218 active reps
   between them and $8.4M of order value. That is one commercial relationship, not three
   conversations — and it is the highest rep-count cluster in the whole no-feed population.
2. **`wac` carries 98 active reps** — more than any other no-feed org, and the fifth-largest by
   value. On rep-unblock-per-conversation it arguably outranks `uhc`.

`JUDGMENT` — **recommended call order**, weighting rep unblock alongside dollars:
`uhc` → `wag` → **Visual Comfort (`fms`+`vcg`+`tla` as one)** → `wac` → `mpc` → `kii` → `ah`.
Seven conversations, ~$89.8M of order value (70.8% of the gap), 435 active reps unblocked.

---

## Gap 2 — the territory master

`MEASURED` · Q003, Q004, Q038, Q052

| | Count |
|---|---:|
| Orgs with any `territories` row | **26** of 258 |
| Orgs with active iPad reps | **144** |
| Of those, with a territory master | **23** |
| **Of those, without one** | **121** |
| Active reps who cannot be scoped | **3,371 of 4,026 (83.7%)** |
| — in people | **1,808 of 2,141** |
| Reps carrying no territory codes on their own record | 938 |
| Reps scopeable today | **655 records / 559 people, in 20 orgs** |

### The shape of the problem is not what the register implies

**3,088 of 4,026 active reps already carry territory codes on their own record.** Only 655 of them
are scopeable — because the *org* has no territory master to resolve those codes against. The
binding constraint is **26 org-level master files**, not 4,026 rep records.

That is a much smaller ask than "fix territory coverage." For the 121 rep-bearing orgs with no
master, the missing artefact is one file per org.

### What fail-closed is buying, as a number

`MEASURED` · Q038 · Under a naive whole-org fallback, the 3,371 unscopeable reps across 143 orgs
would collectively be exposed to **27,258,121 rep × customer-record pairs**. The 655 scopeable reps
sit against 4,787,430.

That is the blast radius the mandatory fail-closed rule prevents, and it is the strongest available
argument for keeping the rule non-negotiable.

### The split-experience population

`MEASURED` · Q052 · **226 people are scopeable at one manufacturer and not at another.** Same human,
same iPad, same afternoon: their book at org A, a blank panel at org B. The register does not name
this group and it is the one that will generate support tickets on day one of the rep component.

---

## Both gaps together, against the build list

The register's claim is that these two "unlock more than everything on the roadmap." Measured:

| | Unlocks |
|---|---|
| **Invoice feed** (64 orgs; 10 conversations = 75%) | 1,893 reps, $126.9M of order value into invoiced-truth reporting, 6 jobs from "fails" to "ships" |
| **Territory master** (121 orgs; 26 master files exist today) | 3,371 rep records / 1,808 people, 7 jobs, and raises the rep component's launch population from 559 people to potentially ~2,100 |
| **Everything in roadmap bucket A** | 18,057 buyers (081) + 17,522 (086) + 241 orgs of catalog QA (053) |

`JUDGMENT`: the register's claim is **true for the rep-facing half of the register and false for the
buyer-facing half.** The two client-data gaps gate almost everything a rep or an executive would
want. They gate almost nothing a dealer buyer would want — and the buyer population is 6× larger and
growing three times faster (Q054).

**The honest CEO framing is not "these gate more than the build list." It is: "these gate the rep
story entirely, and the buyer story not at all — so they are the right push only if the rep story is
the priority."** That is a question the readout should put to him rather than answer.
