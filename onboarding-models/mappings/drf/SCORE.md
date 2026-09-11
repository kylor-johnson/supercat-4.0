# drf — the blind-run score

Mapping written from `Source Data/` alone (`BLIND_BOUNDARY.md`), discrepancy
report committed to disk (`DISCREPANCY.md`), **then** unblinded against a
**pinned** `products.csv` (917,371 bytes, 1,627 rows, pinned 2026-09-04 before
scoring — `score_blind.py` refuses otherwise).

---

## The score is: there is no score, and that is the result

```
reference   1,627 rows, 43 columns
produced       72 rows, 23 columns
shared keys     0
```

**Zero key overlap.** The built catalogue is keyed on pattern × colourway
(`ADELINA-UV-ASH`, `ADELINA-UV-BIRCH`, `ADELINA-UV-CASHMERE`); my mapping is
keyed on pattern (`ADELINA-UV`), because the pattern is all the source contains.

A per-column score over an empty intersection is vacuous — every column is
trivially "exact" on no rows. `score_blind.py` reported **21 byte-exact columns**
on that empty set before I caught it. It now refuses, which is the same rule as
the red test: a green that cannot go red proves nothing.

### The reconciliation the score becomes instead

```
built SKUs                                    1,627
  attributable to one of my 72 patterns         743   (45.7%)
  belonging to a pattern absent from my source   884   (54.3%)

built pattern families (CollectionCodes)        115
my source patterns                               72
  of which appear in the build                   55
  of which appear NOWHERE in the build           17   AMELIE-C0, BRUNELLE-C0,
                                                      CALDER-UV, CALYPSO-C0,
                                                      CHAOS, GIDEON-UV, ...
colourways per pattern in the build      min 4, max 28, mean 13.5
```

**The file I was given is one season's supplement, not the catalogue.** Its name
says so — *"Characteristics Interwoven spring 2026"* — and 54% of the live
catalogue is outside it. Nothing in `Source Data/` says that.

---

## The prediction

`BLIND_BOUNDARY.md`, written before any file was opened:

> The product source will not contain enough rows to explain the built
> catalogue, and that discrepancy — not any column mapping — will be the
> finding.

**Held, with numbers.** The profiler's "what doesn't add up" check is what
earned its keep, and it earned it by refusing to produce a catalogue rather than
by producing a wrong one.

---

## What the blind run got right — every finding confirmed by the build

Each of these was reported from the source alone. The build's own behaviour is
the confirmation, because in each case the build had to *fix the same thing*:

| blind finding | confirmed by |
|---|---|
| `LongDesc` is a **classification**, not a description — 3 distinct values across 72 rows | the build **discards it** and derives its own: 1,627 distinct `LongDesc` values of the form `Adelina-UV Ash` |
| `NewItem` carries `NEW ITEM`/`ACTIVE`, not a boolean | the build normalises it to `Y` on 1,404 rows and blank on 223 |
| the taxonomy never reached the taxonomy columns — `CollectionCodes`/`CategoryCodes` 1 of 72 | the build fills them from elsewhere: 115 collections, 11 categories |
| `ImageFileName` empty on all 72 | the build supplies 1,565 filenames — and **62 rows carry the literal string `-`** as an image name, which matches no file |
| `NetPrice` empty on all 72 | the build ships `NetPrice = 1` on **all 1,627 rows**, with real money in `Price_List`/`Price_Retail`/8 others. (Already recorded as by-design — OPEN_ITEMS A9. Not re-raised.) |
| `Minimum` (yardage) is not `MinimumQuantity` (integer) — **not joined** | the build keeps `Minimum` as its own column and leaves `MinimumQuantity` separate |
| two header rows | third client in a row |

**Zero wrong calls.** Not because the mapping was clever — because on this client
there was almost nothing to be clever *with*, and the disciplined answer was to
map the 72 rows the source supports and stop.

---

## Genuinely unknowable — the questions that cost two weeks

Every one of these is answerable in a sentence by a person and by nothing in the
client's files:

| # | question |
|---|---|
| U1 | **Where does the colourway list live?** 1,627 SKUs from 72 patterns, mean 13.5 colourways each. No source file carries one. |
| U2 | **Where does the rest of the catalogue live?** 884 of 1,627 SKUs (54%) belong to 60 pattern families absent from the file I was given. |
| U3 | **Are the 17 patterns in my source but not the build deliberate exclusions, or a season not yet loaded?** |
| U4 | **Where do prices come from, and which of the 10 price columns does a rep see?** `NetPrice` is a constant `1`. |
| U5 | **Where do images come from?** Zero image files exist in the client tree; the build references 1,564 distinct names plus 62 literal `-`. |
| U6 | **Is `SubClass` one taxonomy or two?** The build carries both `CHENILLE` and `Chenille` — 15 values where the source has 7. |

---

## What this client says about the layer

The three previous clients tested whether a mapping can reproduce a decision.
drf tests whether it can **recognise that no decision has been made**, and that
is the failure mode that actually cost this programme two weeks and a Showtime.

The layer's useful output here is a page of questions and a refusal — delivered
from an 11.7 KB file in the first hour, instead of after a build produced 1,627
rows that looked fine and imported clean.

Two tooling defects were found by this run and fixed:

1. **`score_blind.py` reported 21 byte-exact columns over 0 shared rows.** Now
   refuses and explains why the empty intersection is itself the finding.
2. The same shape as libco's float-tail threshold: a check that reads as a pass
   when it has nothing to measure. Worth watching for a third instance.
