---
id: TAX-MAP
title: Layer A ↔ Layer B correspondence and back-test
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
source_lineage:
  - taxonomy/account-segments.md
  - taxonomy/prospect-archetypes.md
  - Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv  # answer key
depends_on: [TAX-A, TAX-B]
---

# Layer A ↔ Layer B — measured correspondence

Every number here is `[MEASURED]` 2026-08-25 by classifying the 87 automatically-observable roster
orgs with the Layer B rules and comparing against their stamped Layer A labels.

**This document reports what the archetypes actually predict. Three of four do not work.**

---

## 1. Back-test set and baselines

| | |
|---|---:|
| Roster | 109 |
| Automatically observable (the back-test set) | **87** |
| Excluded: manual-only, dead domain, no domain | 22 |
| Majority-class baseline **on this n=87 set** (call everything SEG-02) | **34.5%** (30/87) |
| Majority-class baseline on the **full n=109 roster**, for reference | 34.9% (38/109) |
| Baseline used by the prior 53% run (different set, different method) | 30.0% |

**Baseline discipline.** Three numbers circulate and they are not interchangeable:
**34.5% is the majority baseline on this n=87 back-test set** and is the bar every number in §3
must clear. **34.9%** is the same statistic on the full n=109 roster and is the bar for the Layer A
rule in `account-segments.md`. **30.0%** belongs to the prior run on a different set with a
different method — quoting it here would flatter these results.

---

## 2. The correspondence matrix

Rows = archetype (Layer B, pre-sale). Columns = stamped segment (Layer A, post-sale).

| | SEG-01 | SEG-02 | SEG-03 | SEG-04 | total |
|---|---:|---:|---:|---:|---:|
| **ARCH-01** Trade-Gated Access | **13** | 6 | 0 | 1 | 20 |
| **ARCH-02** Dealer-Locator Network | 8 | 7 | **10** | 0 | 25 |
| **ARCH-03** Open-Price Retail Presence | 3 | **14** | 4 | 5 | 26 |
| **ARCH-04** No Public Channel Signal | 3 | 3 | **5** | 5 | 16 |
| total | 27 | 30 | 19 | 11 | 87 |

---

## 3. Per-archetype accuracy — the real numbers

The a-priori mapping was declared **before** looking at the matrix: gated access → SEG-01,
dealer locator → SEG-02, open retail → SEG-03, no signal → SEG-04.

| ID | Archetype | n | A-priori → | **Precision** | vs 34.5% baseline | vs 30% prior |
|---|---|---:|---|---:|---|---|
| ARCH-01 | Trade-Gated Access | 20 | SEG-01 | **65.0%** | **BEATS** (+30.5pp) | BEATS |
| ARCH-02 | Dealer-Locator Network | 25 | SEG-02 | **28.0%** | **FAILS** | FAILS |
| ARCH-03 | Open-Price Retail Presence | 26 | SEG-03 | **15.4%** | **FAILS** | FAILS |
| ARCH-04 | No Public Channel Signal | 16 | SEG-04 | **31.2%** | **FAILS** | marginal |
| — | **Overall** | 87 | — | **33.3%** | **FAILS — below majority baseline** | marginal |

**Optimistic ceiling.** Re-pointing each archetype at its own modal segment — i.e. fitting the
mapping directly to the answer key, which is not a legitimate predictor — reaches 48.3%. That is
the upper bound of this feature set, not a result.

No archetype was deleted, widened, or re-pointed to improve these numbers. ARCH-02, ARCH-03 and
ARCH-04 are **retained and flagged**, per the brief.

---

## 4. What survives

### 4.1 ARCH-01 works, and works twice over

At 65.0% precision on n=20, **Trade-Gated Access is the only archetype that beats baseline** — by
30.5 points.

Its second property is more useful in the field: **0 of 20 Trade-Gated Access orgs are SEG-03**
(Mid-Market Multi-Channel), and only 1 is SEG-04. A visible trade gate is weak positive evidence
for SEG-01 but **strong negative evidence against SEG-03 and SEG-04** — 95% exclusion. For a field
kit that has to triage near-misses, a reliable disqualifier is worth more than a mediocre
classifier.

### 4.2 ARCH-03 points the opposite way from expectation

Consumer-visible pricing and cart mechanics were expected to indicate Mid-Market Multi-Channel.
Measured, they land on **SEG-02 Premium Trade Brand** (14 of 26, 53.8%) — SEG-03 is only 4 of 26.

Recorded as an observation, **not adopted.** Re-pointing ARCH-03 at SEG-02 would be fitting the
definition to the answer key. It becomes a Phase 4 hypothesis to test against fresh companies, not
a mapping change here.

### 4.3 Volume Distribution did not reproduce as predictable

The brief carries Volume Distribution at 89% predictability from the prior run. On this feature set
it is the *worst*-served segment: ARCH-04 captures 5 of 11 SEG-04 orgs while also collecting 3
SEG-01, 3 SEG-02 and 5 SEG-03.

The measured marker profile of SEG-04 is **absence**: 0/11 `REP_NETWORK`, 0/11 `CATALOG_DL`, 1/11
`TRADE_GATE`, 3/11 `CONTRACT_SPEC`, 7/11 `COLLECTIONS_NAV` (lowest of any segment). Whatever drove
89% in the prior run is not in these web-channel features — most likely it was catalog scale and
unit price, which are Layer A fields and unavailable pre-sale.

**This is a genuine discrepancy with an established input and is not resolved here.** It is logged
in `../ASSUMPTIONS.md`.

---

## 5. The governing conclusion

Layer B, built from every web feature that could actually be collected, predicts Layer A at
**33.3% against a 34.5% majority baseline** — i.e. **no better than guessing the largest segment.**
One archetype out of four carries real signal, and its most valuable property is exclusion rather
than prediction.

### 5.1 This is a method result, not a data result

The prior run scored 53% against a 30% baseline by having an **LLM read whole sites and infer
holistically**. This layer scores 33.3% by **extracting binary features and applying a rule**. Same
public web, different method — the gap between them is the method, not the data. See
`prospect-archetypes.md` §5 for the worked failure case: Interlude Home is plainly trade-oriented
and scores `TRADE_GATE = 0`, because it gates by "DESIGNER RESOURCES" rather than "to the trade".

The defensible claim is therefore narrow:

> **Binary public feature extraction cannot predict a v4.0 segment. Holistic reading reaches
> roughly 53%. Neither is good enough to put a v4.0 segment label on a prospect.**

Do **not** state this as "public data cannot predict segment." That overstates it, and it would
mislead the field kit — which runs the holistic method, not the checklist. The gap is deliberately
not closed with another experiment here; **Phase 4 tests it for free**, because a person reading a
candidate's site *is* the holistic method.

What both methods share is the real constraint. The features that most sharply discriminate selling
motion — AOV, order volume, price-code structure, catalog scale — exist only after a company is a
customer. And per `account-segments.md` §0, even those four reproduce the stamped label only 38.5%
of the time, because **the segments are stamped human judgment rather than a computation.** Layer B
is being asked to predict something that is not a function of measurable inputs at all — which
bounds how well *any* pre-sale method can ever do.

Operationally:

- **Do not assign a predicted Account Segment to a prospect.** Not as a label, not as a hint, not
  in a CRM field. The layers stay separate.
- **ARCH-01 is usable in the field** — as a disqualifier first, a weak positive second.
- **ARCH-02 / ARCH-03 / ARCH-04 are not decision-grade.** They are retained so Phase 4 can test
  whether they improve with manual observation (HPMKT footprint, headcount) that this pass could
  not collect.
- Phase 4 must therefore treat lane criteria as **hypotheses to be falsified**, not as a
  qualification model.

---

## 6. Reproduction

Working files (scratch, not checked in): `orgs.csv`, `features.csv`, `backtest_rows.csv`,
`seg_rule.py`, `markers.py`, `backtest.py`. Regenerating requires re-fetching the 87 sites; results
will drift as sites change.
