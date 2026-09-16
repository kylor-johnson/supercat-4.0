---
id: MEAS-06
title: Line E — the 4-of-31 segment-variation claim, retested live
version: 1.0
status: evidence pack
date: 2026-08-31
database: supercatprod
---

# Line E — is the variation structural, or segment-driven?

> **2026-09-15 — historical measurement of *seat* jobs, not current product doctrine.**
> This file retested “only 4 of 31 jobs vary.” That claim is **withdrawn** as a build rule.
> What still stands: org *shape* (product count, price-code tail, territory emptiness) varies and
> should size extracts / paginate views. What does **not** stand: PG-01 and PG-07 sharing a home
> screen. Canonical set: [`../personas/00-PERSONA-GROUPS.md`](../personas/00-PERSONA-GROUPS.md).

**Tagging:** every figure in this file is `MEASURED` via **Q040** unless marked otherwise. Interpretive
readings are marked `JUDGMENT` inline.

**This claim was load-bearing for "build one layer, parameterised."** It is retested here from
Postgres rather than from the roster CSV. Treat the numbers as evidence about **org shape**, not as
permission to ship one analytics surface for all four motions.

**Verdict as of 2026-08-31 (seats): the seat-register architecture decision looked supported; two of
the four supporting job-level attributions did not survive.** Verdict as of 2026-09-15 (persona
groups): do not implement that architecture.

---

## Method

`MEASURED` · Q040 · per-org row set in `data/Q040.csv`

Structural measures for all **109 roster orgs**, computed live: price levels, active products,
collections, territories, customer records, distinct customer price codes, orders in 12 months,
active reps, active buyers, option groups, invoice-feed presence.

Segment labels come from `../_working/data/orgs.csv` (the stamped v4 roster — the authority, per the
register's own operating rule that segment is a roster lookup and not a recomputation). All 109
matched an organization by `shortname`.

Two statistics are reported per driver:

- **η² (eta-squared)** on a log1p scale — the share of total variance explained by segment membership
- **Between-segment median spread vs within-population IQR** — a plain-language version of the same
  question: does the segment label move the number more than ordinary variation between orgs does?

---

## Result: segment explains almost nothing

| Structural driver | η² (variance explained by segment) | Between-segment median spread | Within-population IQR | Spread beats IQR? |
|---|---:|---:|---:|:--:|
| Price codes | **1.7%** | 2 | 10 | no |
| Active products | **1.9%** | 2,489 | 4,317 | no |
| Orders (12m) | **2.8%** | 460 | 1,671 | no |
| Territories | **3.4%** | 0 | 0 | n/a |
| Customer records | **4.9%** | 3,212 | 4,629 | no |
| Customer price codes | **5.2%** | 3 | 5 | no |
| Collections | **10.9%** | 372 | 434 | no |

**On every single driver, the variation within segments exceeds the variation between them.**
The best case, collections, still only reaches 10.9%. Five of seven are under 5%.

### Per-segment medians

| Driver | Luxury Spec (33) | Premium Trade (38) | Mid-Market MC (24) | Volume Dist (14) | All (109) |
|---|---:|---:|---:|---:|---:|
| Price codes | 7 | 8 | 9 | 8 | 8 |
| Customer price codes | 4 | 4 | 2 | 1 | 3 |
| Active products | 2,016 | 2,286 | 2,738 | **4,505** | 2,499 |
| Collections | 114 | 178 | **429** | **58** | 182 |
| Territories | **0** | **0** | **0** | **0** | **0** |
| Orders 12m | 148 | 292 | 96 | 556 | 203 |
| Customer records | 4,763 | 2,574 | 1,551 | 1,670 | 2,272 |

---

## What this means for the architecture decision

**Keep "build the surface once, parameterise on the org's own structure, do not condition on
segment" — and state it more confidently than the register does.**

The register hedges it against the Layer A reproduction result (38.5% vs a 34.9% baseline). That
hedge is unnecessary. Layer A measures whether structure *predicts the segment label*. This measures
whether the segment label *predicts structure*. Both point the same way, and this one is the
direction that matters for a build decision: **knowing an org's segment tells you almost nothing
about how to parameterise a surface for it. Knowing its structure tells you everything.**

A job does not need to know an org is Luxury Specification. It needs to know it has 55 price codes
and 18,675 products — and those two facts vary enormously *inside* Luxury Specification.

---

## But two of the four named attributions are wrong

The register names four jobs as segment-varying and attaches a specific segment and measure to each.
Retested:

### JTBD-013 — SEG-04, catalog scale — **REPRODUCES** ✓

Register: SEG-04, median 4,498 products, 5,759 orders. Measured: **SEG-04 median 4,505 products** —
the largest of the four segments, reproducing to within 7 items. Cache size and sync duration
genuinely are a different problem for Volume Distribution orgs.

### JTBD-053 — SEG-04, largest catalogs / least structure — **REPRODUCES DIRECTIONALLY** ✓

Register: SEG-04, median 4,498 products / 30 collections. Measured: SEG-04 has both the **largest
catalogs (4,505)** and the **fewest collections (58)** — the rank order holds exactly. The collection
figure drifts (30 → 58) but the claim "largest catalogs carry the least structure" is confirmed.

### JTBD-012 — SEG-02, "median 41 territories" — **DOES NOT REPRODUCE** ✗

| | Luxury Spec | Premium Trade | Mid-Market MC | Volume Dist |
|---|---:|---:|---:|---:|
| Orgs with **any** territory row | 6 of 33 | 8 of 38 | 5 of 24 | **0 of 14** |
| Median territories (all orgs) | **0** | **0** | **0** | **0** |
| Median among orgs that have any | 73 | **102** | 42 | — |
| Max | 238 | 232 | 61 | 0 |

**90 of 109 roster orgs have zero territories.** The median is 0 in every segment, so no segment can
have a median of 41. Among the 19 orgs that do have a master, SEG-02's median is **102**, not 41 —
and 41 is close to Mid-Market's 42, suggesting the original figure was computed on a different
segment, a different denominator, or both.

**The deeper problem: territory count cannot be a segment-varying driver, because 83% of orgs have
no territory data at all.** JTBD-012's variation is driven by *presence or absence of a master file*,
which is an onboarding fact, not a structural or segment one.

### JTBD-083 — SEG-03, "widest price-code spread (median 2, tail to 35)" — **MISATTRIBUTED** ✗

| | Luxury Spec | Premium Trade | Mid-Market MC | Volume Dist |
|---|---:|---:|---:|---:|
| Price codes — median | 7 | 8 | 9 | 8 |
| Price codes — p90 | 36 | **69** | 44 | 30 |
| Price codes — **max** | 138 | **192** | 67 | 35 |
| Customer price codes — median | 4 | 4 | **2** | 1 |
| Customer price codes — max | 42 | 41 | 37 | 21 |

The "median 2" reproduces — SEG-03's median customer price-code count is exactly 2. But that is the
**second-narrowest** of the four, not the widest. And the tail does not stop at 35: the widest spread
by any measure belongs to **SEG-02 (max 192, p90 69)**.

The extreme price-code orgs span three segments: `eli` 192 (Premium Trade), `fms` 138 (Luxury Spec),
`gh` 84 (Luxury Spec), `scw` 81 (Premium Trade), `sc` 73 (Premium Trade), `mli` 67 (Mid-Market).

**Price-code complexity is not a SEG-03 property. It is an org property that occurs across segments.**

---

## Are these the right four jobs?

`JUDGMENT`, grounded in Q040.

The four jobs are the right four **as jobs** — they are the ones whose design genuinely changes with
catalog scale, territory count and price-code count. What is wrong is the *segment* attached to two
of them, and in JTBD-012's case the driver itself.

Two candidates the register does not list, which vary on structure at least as much:

- **JTBD-042 (key an order at the right price level)** — the register already flags it as
  "conditional rather than variant." Measured, price-code count runs from 0 to 192, a wider spread
  than any driver behind the four named jobs. Picking a price level is a genuine decision in `eli`
  and a non-decision in `sca` (1 price code). This has a stronger structural case than JTBD-083 does.
- **JTBD-081/086 (buyer jobs)** — buyer counts run from 0 to 3,954 per org (Q040), a 100% spread with
  no segment signal whatsoever. Whether a buyer surface is worth configuring is entirely an org-level
  fact.

**Recommendation:** keep the count at four but restate the drivers, and replace the segment labels
with the structural thresholds themselves. "SEG-04 has the largest catalogs" is a fact about a
correlation. "This org has 4,505 products, so use the paged sync path" is a parameter. The second is
what the build needs, and the register's own conclusion already says so.

---

## The honest summary

| Claim | Status |
|---|---|
| Only 4 of 31 jobs vary by Account Segment | **Holds** — and the true figure is arguably lower, since two attributions fail |
| Variation tracks catalog scale, territory count, price-code count — not selling motion | **Strongly confirmed.** η² ≤ 10.9% on every driver |
| Build once, parameterise on org structure, do not condition on segment | **Confirmed, and should be stated more confidently** |
| JTBD-013 varies on SEG-04 catalog scale | **Reproduces** (4,505 vs 4,498) |
| JTBD-053 varies on SEG-04 catalog scale / low structure | **Reproduces directionally** (collections 58, not 30) |
| JTBD-012 varies on SEG-02, median 41 territories | **Fails.** Median is 0 in all four segments; 90 of 109 orgs have none |
| JTBD-083 varies on SEG-03, widest price-code spread | **Fails.** SEG-03 is second-narrowest; the widest is SEG-02 (max 192) |

**The load-bearing claim did not break. Two of the four numbers cited in support of it did.**
Do not repeat those two in the readout.
