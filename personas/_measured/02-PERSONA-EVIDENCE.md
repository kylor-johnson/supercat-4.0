---
id: MEAS-02
title: Line A — behavioural persona evidence
version: 1.0
status: evidence pack
date: 2026-08-31
database: supercatprod
---

# Line A — do the personas cluster the way the register says?

The register defines personas as **roles with headcounts**. This tests whether behaviour actually
clusters that way. It does not, in three specific and consequential places.

---

## 1. The internal/rep population splits into three bands, not one persona

`MEASURED` · Q010, Q012

Of the 4,026 rep records counted "active" (logged in within 90 days):

| Band | Reps | Share | Orders 90d | Share of orders | Value 90d | Avg active days /90 | On 1–5 days | On 30+ days |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **A — wrote nothing** | 2,806 | 69.7% | 0 | 0% | $0 | 12.4 | 1,324 | 368 |
| **B — 1–19 orders** | 867 | 21.5% | 4,447 | 13.7% | $23.5M | 26.5 | 111 | 309 |
| **C — 20+ orders** | 353 | **8.8%** | 28,087 | **86.3%** | **$143.4M (85.9%)** | 54.2 | **0** | 314 |

Maximum for any single rep: 424 orders, 238 distinct customers.

**Why this is not an artefact.** The bands were constructed from orders written. They separate just
as cleanly on a variable that had no part in building them — the number of distinct days a rep
generated a login event (Q012). Producers are on the device 54 of 90 days and **not one** is below
six days. The gradient is monotonic and steep.

**The band A finding is the important one.** 2,806 reps write nothing, but they are not dormant:
they average 12.4 active days per quarter and **368 of them are on the iPad on 30 or more separate
days**. That is a heavy user of a catalog, price and availability tool who never submits an order
through it — because the order goes to the manufacturer by phone, email or EDI, or because the rep's
role is presentation rather than order capture.

**Verdict: the register's PER-01 is at least two personas.**

- **The order-writer (band C, 353 records).** The account brief in `02-IPAD-ACCOUNT-BRIEF-SPEC.md`
  is built for this person. They would open it daily. JTBD-011, 014, 012 are theirs.
- **The reference user (band A, 2,806 records, of whom ~368 are heavy).** Their jobs are catalog
  fidelity, current price, and stock — JTBD-013, 083, 084, 053. An invoiced-dollars account panel
  answers a question they are not asking.

`JUDGMENT`: band B is a genuine middle rather than a third type; it behaves like a less-intense C.
The defensible split is two, with B assigned to C's design.

**Caveat, stated plainly.** Orders are attributed via `orders.org_user_id`. A rep whose orders are
keyed by customer service under a different user would appear in band A incorrectly. The login-days
evidence makes a *wholesale* attribution failure unlikely — band A's engagement profile is genuinely
lower — but the exact 69.7% should be read as "the large majority," not as a precise headcount.

---

## 2. Rep records are not rep people — and the multi-line rep is the modal case

`MEASURED` · Q051, Q052, Q053

| | Records | Distinct people | Memberships each |
|---|---:|---:|---:|
| Active iPad reps | 4,026 | **2,141** | 1.88 |
| Active eOL buyers | 18,764 | **12,972** | 1.45 |

The typical active SuperCat rep carries **about two manufacturers on the same iPad.** That is not a
footnote — it is the central fact about the rep population, and the register does not contain it.

It produces a specific, testable product problem. Of 2,141 people:

- **559** are territory-scopeable at at least one of their orgs
- **1,808** are unscopeable at at least one of their orgs
- 559 + 1,808 = 2,367 > 2,141, so **226 people are scopeable at one manufacturer and not at another**

Under the mandatory fail-closed rule, those 226 people see their book when they open manufacturer A
and a blank panel when they open manufacturer B — on the same device, in the same afternoon. That is
the worst experience the rule can produce, and it is currently unnamed in the register.

**The rep component's launch population is 559 people, not 664 or 655 records.**

---

## 3. `primary_rep_group` reps behave measurably differently — PER-02 is behaviourally real even though it is structurally invisible

`MEASURED` · Q011, Q070, Q071

| | Reps | Zero-order | % zero | Avg orders 90d | Value 90d |
|---|---:|---:|---:|---:|---:|
| Not `primary_rep_group` | 3,436 | 2,450 | 71.3% | 7.46 | $142.2M |
| **`primary_rep_group`** | **590** | 356 | **60.3%** | **11.67** | $24.7M |

Agency reps are **more productive** than other reps on both measures. The persona the register
declines is the one that performs best.

That does not reverse the decline — there is still no join from a principal to their sub-reps — but
it changes the reason, and the register's stated reason is wrong:

- 11,799 distinct internal `company_name` values `MEASURED` Q071 — reproduces the register's 11,880
- Case-insensitive dedup only reaches 11,612, so **casing is not the problem**
- **Only 868 of 4,026 active reps (21.6%) have `company_name` populated at all**
- Among `primary_rep_group` active reps: **125 of 590 (21.2%)**, across 81 distinct values

**Normalising 11,880 names is not the blocker. The field is empty for 78% of the live rep
population.** Normalisation cannot fix absence. Keep the decline; replace the reason.

---

## 4. "Dealer buyer" is at least three populations

`MEASURED` · Q013, Q015, Q016, Q017

**By ordering behaviour**, of 18,764 active buyer records over 12 months:

| Behaviour | Buyers | Share | Value |
|---|---:|---:|---:|
| **Logged in, never ordered** | 11,868 | **63.2%** | $0 |
| One order | 2,769 | 14.8% | — |
| 2–5 orders | 2,873 | 15.3% | — |
| 6–20 orders | 1,013 | 5.4% | — |
| **>20 orders** | **241** | **1.3%** | **$23.6M of $59.9M (39.4%)** |

Maximum for a single buyer: 835 orders.

Two-thirds of active buyers use eCat Online purely as a **catalog and account-lookup surface**. That
is direct measured support for the register's instinct that JTBD-082 (check what I ordered and was
billed) and JTBD-083 (see what I'm entitled to pay) are the load-bearing buyer jobs — and it puts a
number on it. JTBD-081 (reorder) serves 36.8% of the active base at most.

**By program size** — the brief's specific question, whether buyers at large programs behave
differently from the long tail (Q015):

| | Active buyers | Distinct buyers ordering | Penetration | Orders | Orders per ordering buyer | Avg order |
|---|---:|---:|---:|---:|---:|---:|
| **Top 6 orgs** | 12,473 | 6,769 | **54.3%** | 21,576 | **3.19** | **$1,700** |
| **Tail (31 orgs)** | 6,291 | 2,309 | **36.7%** | 17,710 | **7.67** | **$1,674** |

**Yes — but not on the axis you would guess. Basket size is identical ($1,700 vs $1,674).** What
differs is penetration and frequency, and they run in opposite directions: large programs get *more
buyers ordering, less often each*; the tail gets *fewer buyers ordering, more than twice as often*.

`JUDGMENT`: that is consistent with two different commercial relationships — broad self-service
enrolment at scale programs, versus a small set of committed reorder accounts at smaller ones. It
argues that a single "reorder" surface is right (basket behaviour is the same) but that adoption
tactics should differ. It does **not** argue for two products.

**Ship-tos**: of the 3,987 buyers with a resolvable `ship_to_code`, only **75 (1.9%) used more than
one**. The multi-ship-to buyer is not a population worth designing for. `MEASURED` Q016.
*Caveat*: `ship_to_code` is sparse — populated for well under half the buyers who ordered — so this
is directional, not definitive.

---

## 5. Personas the data cannot see at all

`UNVERIFIABLE-FROM-DB`

The readout marks PER-04 (customer service / order entry) and PER-05 (product / merchandising) as
"not counted." That is correct and worth stating precisely: **neither role exists in the schema.**
There is no attribute on `org_users`, `user_types`, or anywhere else that distinguishes a CS agent
or a merchandiser from any other internal user. They sit inside the 25,801 internal records
undifferentiated.

Two weak proxies exist and neither is good enough to publish:

- CS agents plausibly appear as high-order-count internal users at orgs with few reps — but that is
  indistinguishable from a productive rep.
- `is_admin` (2,460 records) spans VP/ops, CS leads and IT, and cannot be decomposed.

**What would settle it:** a role or job-function attribute on `org_users`, or an audit-log analysis
of which Admin Console surfaces each internal user touches (`audit_log_entries`, 21.2M rows — not
attempted here because the surface-to-role mapping would itself be an assumption). Named in
`08-UNVERIFIABLE.md`.

---

## Summary — what the data supports

| Register persona | Verdict | Evidence |
|---|---|---|
| **PER-01 independent sales rep** | **Splits into two.** Order-writer (353 records) vs reference user (2,806) | Q010, Q012 |
| **PER-02 rep agency principal** | **Behaviourally real and more productive.** Structurally invisible — but because the field is *empty*, not messy | Q011, Q071 |
| **PER-03 VP / sales ops** | Cannot be isolated. 2,460 `is_admin` records span several roles | Q001 |
| **PER-04 customer service** | **Invisible.** No schema attribute | — |
| **PER-05 product / merchandising** | **Invisible.** No schema attribute | — |
| **PER-06 owner / exec** | Cannot be isolated; overlaps PER-03 | — |
| **PER-08 dealer buyer** | **Splits into three** by engagement (63% never order), and into two by program size on frequency — **not** on basket size | Q015, Q016 |
| *(not in the register)* | **The multi-line rep.** 1.88 org memberships per person; 226 people get a split scoping experience | Q051, Q052 |
