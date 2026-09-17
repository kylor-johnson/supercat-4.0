# W1 evidence — P0-7, P0-8, P0-10

Branch `exec/W1`, off `exec/phase-0-baseline`. Worker session, 2026-09-17.
Brief: [`W1_brief.md`](W1_brief.md). Everything below ran offline from
`pipeline/cache/`, no VPN, no Postgres, no `ANTHROPIC_API_KEY`.

**Headline:** `bmc` reaches SHIP. All 11 orgs now ship deterministically, at
every confidence level. HFG's §8 names the $2.64M project. No org changed
outcome except `bmc` (exit 1 → SHIP).

---

## Files changed

| File | Task | What |
|---|---|---|
| `pipeline/templates/_macros.md.j2` | P0-10, P0-7 | `sensitivity_hedge()`; `signal_single_door_project()` |
| `pipeline/templates/section_01_hero.md.j2` | P0-10 | §Q hedge under the §1 metric cards below STRONG |
| `pipeline/templates/section_03_thismonth.md.j2` | P0-10 | §Q hedge on the deterministic cross-sell play body |
| `pipeline/templates/section_08_products.md.j2` | P0-7, P0-8 | project lead sentence; `display_description` at 6 sites |
| `pipeline/templates/section_05_layers.md.j2` | P0-8 | `display_description` |
| `pipeline/gather.py` | P0-8 | `normalize_product_description()` + `ProductRow.display_description` |
| `pipeline/signals.py` | P0-7 | `single_door_project` kind, two relative thresholds, `detect_single_door_project()` |
| `pipeline/fact_bundles.py` | P0-8 | cross-sell play title uses the readable label |
| `run.sh` | P0-10 | accepts `--no-narrative` (**out-of-scope file — see note**) |
| `README.md` | P0-10 | the deterministic-fallback claim, made true |
| `tests/test_deterministic_fallback.py` | P0-10 | new, 16 tests |
| `tests/test_product_descriptions.py` | P0-8 | new, 49 tests + 6 skips |
| `tests/test_single_door_project.py` | P0-7 | new, 18 tests |

**Scope note — `run.sh` is not on the brief's In list.** The P0-10 DoD explicitly
offers it (*"use the module form above, or add the flag to `run.sh` — your call,
but say which and why"*), so I read that as authorising this one file. **Which:**
added the flag. **Why:** the brief's other half is that `README.md` documents an
entrypoint that rejects the flag. Documenting the module form instead would leave
the documented entrypoint broken and the README merely honest about it. The
change is a pass-through that defaults off; `cohort_run.sh` calls `run.sh` and is
byte-unaffected. Nothing else outside the In list was touched.

---

## P0-10 — the deterministic fallback at PARTIAL

### Before

```
$ ./run.sh bmc --date 2026-07-09
preflight: mode=Mode 1 - Tier-1 degraded confidence=PARTIAL tier=1
signals: 28 fired
slots: all skipped (no API key)
wrote: .../outputs/bmc_DRAFT_2026-07-09.md
smoke_check: FAIL
  - SENSITIVITY HEDGE: $2.27M in ## The 60-second read without marker (confidence=PARTIAL)
  - SENSITIVITY HEDGE: $218K in ## Do this month without marker (confidence=PARTIAL)
  - SENSITIVITY HEDGE: $0.33M in ## Do this month without marker (confidence=PARTIAL)
ERROR: pipeline failed (exit 1)
```

Two render sites, both deterministic:

1. **§1 metric cards** — `section_01_hero.md.j2:203`, the `Revenue at risk` row.
   The §1 lead-in already carries *"All figures below are directional"*, but by
   the time the cards render it is well past the gate's ±400-char window.
2. **§3 cross-sell play body** — `section_03_thismonth.md.j2:18`. The §3
   section-level hedge sits above play 1; play 2's dollars are out of range.

### The fix

`_macros.md.j2` gains `sensitivity_hedge(posture, subject, singular)`. It is not
a bracket — it names the uncertainty class, which is what §Q.4(a) asks of a
collective hedge, and it says a different thing on a frozen feed than on an
un-cross-verified one:

```
What would change this read: every dollar figure above is directional — a floor
drawn from an invoice feed that stopped updating 223 days (about 7 months) ago.
A refreshed feed moves the size of these numbers, not their direction;
pressure-test the size before you plan against it.
```

```
Fynn Display Cabinet is the anchor item — $218K invoiced (LTM) across 44
dealers. The NONE family is $0.33M, -45% YoY, across 12 dealers and 35 SKUs.
What would change this read: Both figures are directional — a floor drawn from
an invoice feed that stopped updating 223 days (about 7 months) ago. A refreshed
feed moves the size of these numbers, not their direction; pressure-test the
size before you plan against it.
```

`smoke_check` was not weakened — `_HEDGE_MARKERS` and `_check_sensitivity_hedge`
are untouched. The marker tokens (`directional`, `floor`) and the §Q.2 phrasings
(*"What would change this read"*, *"pressure-test"*) are in the macro's own text,
with a comment saying both gates read it.

**Tension I am flagging rather than resolving silently:** §Q.3 says the hedge
*"must be authored, not templated."* That rule assumes an author. The
deterministic fallback has none, so its only choices are a templated hedge or no
report at all. The macro is written to carry real content rather than satisfy a
regex, but this is the owner's call to overturn.

The hedge fires at `commerce_confidence not in ["STRONG", "NONE"]`. `bmc` is the
only such org in the pinned cohort, so it is the only org whose text moves.

### After

```
$ ./run.sh bmc --date 2026-07-09
preflight: mode=Mode 1 - Tier-1 degraded confidence=PARTIAL tier=1
signals: 28 fired
slots: all skipped (no API key)
wrote: .../outputs/bmc_DRAFT_2026-07-09.md
smoke_check: PASS
rendered bmc_DRAFT_2026-07-09.md → .../Bassett_Mirror_CEO_intelligence_report_2026-07-09.html (61,411 bytes)
PASS  Bassett_Mirror_CEO_intelligence_report_2026-07-09.html  · [4 8 9 11 12 all pass]

┌──────────────────────────────────────────────────────────┐
│  SHIP                                                    │
│  smoke_check: PASS  ·  step10: PASS                     │
└──────────────────────────────────────────────────────────┘
```

### The escape hatch, all 11 orgs through the documented entrypoint

`run.sh` now takes `--no-narrative` and forwards it to the module. The whole
cohort, deterministic-only, offline:

```
org      confidence           smoke_check        step10   rc  outcome
sarreid  confidence=STRONG    smoke_check: PASS  PASS     0   SHIP
cci      confidence=STRONG    smoke_check: PASS  PASS     0   SHIP
da       confidence=NONE      smoke_check: PASS  PASS     0   SHIP
clc      confidence=STRONG    smoke_check: PASS  PASS     0   SHIP
hfg      confidence=STRONG    smoke_check: PASS  PASS     0   SHIP
kal      confidence=STRONG    smoke_check: PASS  PASS     0   SHIP
ali      confidence=STRONG    smoke_check: PASS  PASS     0   SHIP
sca      confidence=NONE      smoke_check: PASS  PASS     0   SHIP
bsc      confidence=NONE      smoke_check: PASS  n/a      2   REDIRECT
bmc      confidence=PARTIAL   smoke_check: PASS  PASS     0   SHIP
bri      confidence=STRONG    smoke_check: PASS  PASS     0   SHIP
```

`bsc` rc=2 is the correct-refusal path, unchanged. **STRONG, PARTIAL and NONE are
all covered** — the DoD asked for one PARTIAL and one STRONG.

`README.md` now reads *"…no prose file, at every commerce-confidence level
(verified across the pinned cohort: STRONG, PARTIAL and NONE all reach
`smoke_check: PASS` deterministically)"*, and the quick-start block shows the flag.

### Is the new test real?

Reverting only the two templates, with everything else in place:

```
FAILED tests/test_deterministic_fallback.py::test_deterministic_render_satisfies_sensitivity_hedge[bmc]
FAILED tests/test_deterministic_fallback.py::test_hero_cards_carry_the_hedge_below_strong[PARTIAL]
FAILED tests/test_deterministic_fallback.py::test_hero_cards_carry_the_hedge_below_strong[LIMITED]
3 failed, 13 passed in 0.40s
```

`test_cohort_still_exercises_a_hedged_confidence_level` guards against the
parametrised test going vacuous if the cohort ever drifts to all-STRONG — every
§Q check short-circuits at STRONG, so an all-STRONG cohort would pass while
testing nothing.

---

## P0-8 — SKU descriptions as raw spec strings

`pipeline/gather.normalize_product_description(description, item_number)`, reached
through `ProductRow.display_description`. The raw `description` is untouched, so
`derive_description_families()` — which tokenises it — is byte-stable. This is a
**render-time** rule, which is where `AUDIT_FINDINGS.md` §4 puts P0-8.

Four structural rules, applied to each `|`-delimited segment:

1. drop a segment that is the item number repeated back;
2. drop a **dimension-only** segment (`34.5" H x 64.5" D x 92.5" L`) — requires at
   least one quoted measurement, so a bare `5 x 3` is never silently eaten;
3. strip a leading purchase-order reference (`PO644283`, `po-78500`, `PO Y0964`)
   or a bare numeric code of 6+ digits;
4. collapse whitespace runs.

Then **one** case rule, and it is deliberately timid. A segment is title-cased
only if it is fully uppercase, contains **no digit-welded unit token** (`20W`,
`1300LM`, `90CRI`, `3CCT`, `4PK`), and every remaining token is either a real word
(3+ letters with a vowel), a known unit, or a part code. `LT` and `IN` are
deliberately *not* units — `6LT` and `48IN` are how `kal` names a product, not
how it specs one.

The unit-token bail is what respects the brief's warning. `ali`'s catalog is
entirely spec strings, so **not one ali row changes**: `FLMNT RND` does not become
`Flmnt Rnd`, and `PEN` / `VAN` / `MIR` are not title-cased into words they are not.
`bri`'s part codes are likewise untouched.

### Before / after, every org that has a catalog

Coverage is 8 of 11, exactly as the brief states: `da` has no product CSVs, `sca`
and `bsc` have them with zero rows.

**`hfg` — 4 of 25**

| item | before | after |
|---|---|---|
| `9N00145405-3-14-DL105` | `9N00145405-3-14-DL105 \| TYPE DL-105 \| 34.5" H x 64.5" D x 92.5" L \| OPEN CENTER, ACRYLIC BOTTOM AND TOP DIFFUSERS` | `Type DL-105 — Open Center, Acrylic Bottom and Top Diffusers` |
| `9N00145405-2-14-DL104` | `9N00145405-2-14-DL104 \| TYPE DL-104 \| 24.5" H x 64.5" x 64.5"` | `Type DL-104` |
| `9N00145405-1-14-DL103` | `9N00145405-1-14-DL103 \| TYPE DL-103 \| 24.5" H x 38.5" D x 96.5" L` | `Type DL-103` |
| `9N00145405-4-14-DL107` | `9N00145405-4-14-DL107 \| TYPE DL-107 \| 16.3" H x 96" OD` | `Type DL-107` |

**`cci` — 25 of 25** (all case; the 30-char source truncation is not repairable
from here and is left visible)

| before | after |
|---|---|
| `NOTTAWAY LARGE BRONZE CHANDELI` | `Nottaway Large Bronze Chandeli` |
| `NOTTAWAY GRANDE BRONZE CHANDEL` | `Nottaway Grande Bronze Chandel` |
| `NOTTAWAY SMALL BRONZE CHANDELI` | `Nottaway Small Bronze Chandeli` |
| `RAINFOREST LARGE BRONZE CHANDE` | `Rainforest Large Bronze Chande` |
| `LUNARIA SMALL SILVER CHANDELIE` | `Lunaria Small Silver Chandelie` |
| `BRIALLEN WHITE DEMI-LUNE CABIN` | `Briallen White Demi-Lune Cabin` |
| `BRIALLEN BLACK DEMI-LUNE CABIN` | `Briallen Black Demi-Lune Cabin` |
| `MAGNUM OPUS GRANDE CHANDELIER` | `Magnum Opus Grande Chandelier` |
| `MAGNUM OPUS LARGE CHANDELIER` | `Magnum Opus Large Chandelier` |
| `MEREWORTH OVAL ROPE CHANDELIER` | `Mereworth Oval Rope Chandelier` |
| `LUNARIA SILVER OVAL CHANDELIER` | `Lunaria Silver Oval Chandelier` |
| `TIRRELL LARGE BLACK CHANDELIER` | `Tirrell Large Black Chandelier` |
| `SAXON LARGE BLACK CHANDELIER` | `Saxon Large Black Chandelier` |
| `FOREST DAWN GOLD CHANDELIER` | `Forest Dawn Gold Chandelier` |
| `FOREST LIGHT GOLD CHANDELIER` | `Forest Light Gold Chandelier` |
| `SOMMELIER GREEN CHANDELIER` | `Sommelier Green Chandelier` |
| `MALVASIA BRASS WALL SCONCE` | `Malvasia Brass Wall Sconce` |
| `BRUSSELS BLACK CHANDELIER` | `Brussels Black Chandelier` |
| `MARILEE MEDIUM CHANDELIER` | `Marilee Medium Chandelier` |
| `BRADSHAW CHANDELIER` | `Bradshaw Chandelier` |
| `VICHY CHANDELIER` | `Vichy Chandelier` |
| `LUCIEN CHANDELIER` | `Lucien Chandelier` |
| `MENEFEE GOLD CHANDELIER` | `Menefee Gold Chandelier` |
| `DAZE LARGE PENDANT` | `Daze Large Pendant` |
| `DAZE MEDIUM PENDANT` | `Daze Medium Pendant` |

**`kal` — 12 of 25**

| before | after |
|---|---|
| `FLINT 5 LT MULTI DROP` | `Flint 5 LT Multi Drop` |
| `FLINT 3 LT MULTI DROP PENDANT` | `Flint 3 LT Multi Drop Pendant` |
| `FLINT LED WALL SCONCE PENDANT` | `Flint LED Wall Sconce Pendant` |
| `VERDE 6LT CHANDELIER` | `Verde 6LT Chandelier` |
| `CADERE ISLAND LIGHT` | `Cadere Island Light` |
| `CADERE 40 IN CHANDELIER` | `Cadere 40 IN Chandelier` |
| `SPHERE 36 IN PENDANT` | `Sphere 36 IN Pendant` |
| `FRANGIA 29 IN PENDANT` | `Frangia 29 IN Pendant` |
| `UROKO 28 IN PENDANT BN` | `Uroko 28 IN Pendant BN` |
| `ESTRELLA 48IN PENDANT` | `Estrella 48IN Pendant` |
| `CAPE LED WALL SCONCE NAT` | `Cape LED Wall Sconce NAT` |
| `CUSTOM QUADRO 3 TIER PENDANT` | `Custom Quadro 3 Tier Pendant` |

**`bmc` — 12 of 25**

| before | after |
|---|---|
| `po-78500 Brookings Floor Mirror` | `Brookings Floor Mirror` |
| `PO-Y2723 Newport Rect Cocktail` | `Newport Rect Cocktail` |
| `PO644283 Eltham Wall Mirror` | `Eltham Wall Mirror` |
| `PO Y0964 Hudson Server` | `Hudson Server` |
| `PO11124 Beaded Floor Mirror` | `Beaded Floor Mirror` |
| `040002053 White/ Nickel` | `White/ Nickel` |
| `040003492 Round Coffee Table` | `Round Coffee Table` |
| `040003683 Ent Console` | `Ent Console` |
| `040003271 Gold` | `Gold` |
| `SIMPLICITY CHEST` | `Simplicity Chest` |
| `5 DRAWER CHEST` | `5 Drawer Chest` |
| `6 DRAWER CHEST` | `6 Drawer Chest` |

**`sarreid` — 9 of 25**, all double-space collapse:
`Lilac Sideboard  Blue Finish` → `Lilac Sideboard Blue Finish`;
`Giselle Jupe Dining Table  Lg  Lt Mink` → `… Lg Lt Mink`;
`Giselle Jupe Table  Medium  Light Mink`; `Beacon Hill Display Case  Ebony`;
`Ciborium Chest Of Drawers  Fruitwood`; `Coolidge Leather Swivel Chair  Cuba Brn`;
`Covent Gardens Sideboard  Ebony`; `Gideon Shagreen Console Table  Ant.grey`;
`Hudson Console  Brown`.

**`clc` — 0 of 25.** **`ali` — 0 of 25.** **`bri` — 0 of 25.**

### No two SKUs collide

`clc` already ships two SKUs labelled `4 Light Pendant` (6 collision groups) —
that is in the source data. The rule must not *add* one. Per org, comparing the
set of colliding SKU groups before and after:

| org | collision groups before | after | introduced |
|---|---|---|---|
| sarreid | 0 | 0 | **0** |
| cci | 0 | 0 | **0** |
| clc | 6 | 6 | **0** |
| hfg | 3 | 3 | **0** |
| kal | 0 | 0 | **0** |
| ali | 0 | 0 | **0** |
| bmc | 0 | 0 | **0** |
| bri | 0 | 0 | **0** |

`test_no_new_sku_collisions_in_any_catalog` asserts `after ⊆ before` for every
catalog, and `test_no_catalog_row_renders_a_dimension_or_pipe` asserts no label
is empty, carries a pipe, or keeps a dimensional tail.

### Residuals I did not fix, deliberately

- **`bmc` → `Gold`** (`3235-263SD`, was `040003271 Gold`). Stripping the PO code
  leaves a finish word as the whole label. It is strictly better than a bare
  purchase-order number, but the real problem is that bmc's `description` is a
  free-text notes field. No rule fixes that; a source-data conversation does.
- **`cci`'s 30-character truncation** (`…CHANDELI`, `…CHANDE`). Repairing it means
  inventing the missing letters. Left visible.
- **`sarreid`'s leading `*`** (`*the Harley Chair`, `*drake Distilled Leather
  Chair`). Unknown ERP semantics — probably a discontinued/custom marker. Not
  stripped, and it renders literally in markdown.
- **`hfg`'s `Type DL-104`** and friends lose everything but the type code, because
  the rest of the field really was only dimensions. That is the identifying head,
  which is what the brief asked for.

---

## P0-7 — single-door project concentration

**Recommendation: yes, it is generically detectable — with two gates, not one,
and both relative.** Implemented; the constants are the owner's to move.

### The naive rule is not enough

`dealer_count == 1 AND item_revenue > ~2% of inv_ltm_net` fires only on hfg's two
biggest SKUs, and never states the thing worth stating — that **four** SKUs,
`$2.64M`, **6.4% of a $41.2M year**, are one project in one door. Clustering by
SKU prefix is what turns two line items into a project.

But prefix clustering alone produces a false positive. `ali`'s `SB-23941-MBL/OPL`
and `SB-23768-MBL-CHN` share a 5-character prefix, are one dealer each, and are
**2.58% of LTM** — over any sensible share floor.

### What separates a project from a channel

A project fabricates a handful of units at an enormous unit price. A single-door
high-volume SKU is a marketplace or direct account — already covered by the
concentration signals. So gate 2 is **unit price against the org's own catalog
median**, which keeps it relative (AUDIT §2.1) rather than an absolute floor:

- hfg's cluster: 63 units at **$41,871** — **26.0×** its catalog median.
- ali's `SB-23` pair: 2,750 units at **$69** — **0.9×**.

### Cohort sweep — all 11 orgs, three candidate threshold pairs

| org | LTM | catalog | single-door SKUs | biggest single-door cluster | $ | % LTM | $/unit | vs median | 2% / 5× | 3% / 8× | 5% / 10× |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sarreid | 15,767,336 | 25 rows | 0 | — | — | — | — | — | no | no | no |
| cci | 70,016,164 | 25 rows | 0 | — | — | — | — | — | no | no | no |
| da | 0 | none (no product CSVs) | — | — | — | — | — | — | — | — | — |
| clc | 58,930,000 | 25 rows | 0 | — | — | — | — | — | no | no | no |
| **hfg** | 41,170,115 | 25 rows | 4 | `9N00145405-` ×4 | 2,637,850 | **6.41%** | 41,871 | **26.0×** | **FIRES** | **FIRES** | **FIRES** |
| kal | 8,761,029 | 25 rows | 1 | `MODD-3TIER-QUADRO` ×1 | 52,374 | 0.60% | 17,458 | 17.1× | no | no | no |
| ali | 7,341,307 | 25 rows | 6 | `SB-23` ×2 | 189,468 | 2.58% | 69 | 0.9× | no | no | no |
| sca | 0 | empty (0 rows) | — | — | — | — | — | — | — | — | — |
| bsc | 0 | empty (0 rows) | — | — | — | — | — | — | — | — | — |
| bmc | 6,944,922 | 25 rows | 7 | `5572-DR-576D` ×1 | 100,033 | 1.44% | 599 | 1.8× | no | no | no |
| bri | 21,248,755 | 25 rows | 0 | — | — | — | — | — | no | no | no |

**One true positive, zero false positives, at all three candidate settings.**

Two things the reviewer should weigh:

- **The cohort does not discriminate between the candidates.** All three give the
  same answer. I shipped the middle pair —
  `PROJECT_MIN_SHARE_OF_LTM = 0.03`, `PROJECT_MIN_UNIT_PRICE_RATIO = 8.0` —
  because it has headroom on both sides of ali's 2.58%/0.9× and kal's
  0.60%/17.1×. Those numbers are the owner's per `EXECUTION_PLAN.md`; moving them
  is a one-line edit with a test that asserts the boundary behaves.
- **`kal`'s `MODD-3TIER-QUADRO` is a genuine custom one-off** (`CUSTOM QUADRO 3
  TIER PENDANT`, 3 units, 17.1× median unit price) that the share gate excludes
  at 0.60% of LTM. That is the gate doing its job — it is a real project and an
  immaterial one — but it is the row that will move first if the share floor is
  lowered.

### Known limits of the rule

- **`Q-PROD-TOP` is the top 25 items only.** A project whose SKUs rank below that
  is invisible. Every gate is a floor, so the rule under-detects and never
  over-detects.
- **`dealers` is per-SKU.** A project split across two doors does not fire.
- **Prefix clustering is an approximation** of "same project". It is right on hfg
  (`9N00145405-*`) and the unit-price gate is what stops it being wrong on ali.

### What HFG now says

`§8 What's selling` leads with it, in two paragraphs (the renderer lifts a
section's first paragraph into its summary card; one long paragraph truncated
mid-clause):

> **4 of the items below share the 9N00145405- prefix and went to a single dealer
> — $2.64M invoiced (LTM), 6.4% of the year, on 63 units.**
>
> At $41,871 a unit — 26× the median item on this list — that is one project, not
> a line the field can reorder. The catalog reads differently once you set it
> aside: everything below it is the repeatable business.

---

## Verification

### `make check`

```
.venv-renderer/bin/python -m pytest tests/ -q
150 passed, 6 skipped in 0.62s
./regression.sh --verify
── sarreid (SHIP, date=2026-07-02) ──
  FAIL deterministic core: Sarreid_Ltd._CEO_intelligence_report_2026-07-02.html
    expected: 00e99822f64beb2324d431000bc228eb15e8173d2170b0d7cc3f95563e30afad
    actual:   6755c70d98593cac796c4bc76b5848a1d71b652a10ecc88d3183cf665b07a7ae
── cci (SHIP, date=2026-07-02) ──
  FAIL deterministic core: Currey_and_Company_CEO_intelligence_report_2026-07-02.html
    expected: cf7fd16c0fbe37bc4af51900849be9a6c1d460eff6fa304686548fedbc97da56
    actual:   a21287bca5d5e7892a57e94c5fbf688a610ab4c5aa4a2070fc11bbac9629ca5d
── da (SHIP, date=2026-07-09) ──
  FAIL deterministic core: Dainolite_Ltd._CEO_intelligence_report_2026-07-09.html
    expected: c6b7a125eb062fd9aa50d5d99bb2338fb2426c18496d9718df95e4a4749597f9
    actual:   edc763eb990752fa74abc91512ad46dc3f167a7208acba27c5273110f8972842
── clc (SHIP, date=2026-07-09) ──
  FAIL deterministic core: Capital_Lighting_Fixture_Co._CEO_intelligence_report_2026-07-09.html
    expected: 48dda77b29c96ff7a56b1c9bacc19b236d06e90e7e3b922be13484623d5dfc54
    actual:   84141d1a68d20227c83139ade7c092ab89a9c0ff0ce579db2d75c9ae3f229485

  GOLDEN SET: FAIL (0 passed, 4 failed)
make: *** [golden] Error 1
```

**`make check` cannot be green on this branch, and was not green when W1 started.**
`regression.sh --verify` was 0/4 at the Phase-0 audit (`AUDIT_FINDINGS.md` §5 —
*"Not broken — stale"*), and the golden re-freeze is Phase 2, reviewer-only.
`config/golden_set.json` is on the brief's do-not-touch list, so a worker cannot
make this pass. **Tests and cohort are the gates W1 can actually meet, and both
are met.** Two of the four goldens (`da`, `clc`) still match their *pre-W1* actual
byte-for-byte; the other two moved, justified below.

### Cohort

`./tools/cohort_diff.sh` compares against `_baseline/`, captured at Phase 0 —
*before* the reviewer's P0-1…P0-11 commits. So its table shows the whole of
Phase 1, not W1. Both are recorded.

**vs `_baseline` (all of Phase 1):**

```
ORG      TEXT       CORE-SHA  OUTCOME    NOTE
----------------------------------------------------------------------
sarreid  +5/-7      CHANGED   SHIP
cci      +20/-22    CHANGED   SHIP
da       +15/-42    CHANGED   SHIP
clc      +20/-62    CHANGED   SHIP
hfg      +12/-10    CHANGED   SHIP
kal      +272/-169  CHANGED   SHIP       outcome exit1 → SHIP
ali      +5/-7      CHANGED   SHIP
sca      +17/-44    CHANGED   SHIP
bsc      +3/-1      CHANGED   REDIRECT
bmc      +356/-198  CHANGED   SHIP       outcome exit1 → SHIP
bri      +0/-2      CHANGED   SHIP
----------------------------------------------------------------------
COHORT: CHANGED
```

**vs a snapshot taken at W1 start — this is W1's own delta:**

| org | visible-text lines changed (both sides of the diff) | outcome | core_sha |
|---|---|---|---|
| sarreid | 0 | SHIP → SHIP | `e6cce02aab70` → `6755c70d9859` |
| cci | 12 | SHIP → SHIP | `f24e548e3fc4` → `a21287bca5d5` |
| da | 0 | SHIP → SHIP | unchanged |
| clc | 0 | SHIP → SHIP | unchanged |
| hfg | 16 | SHIP → SHIP | `9954debbe00e` → `6eb108b9b887` |
| kal | 12 | SHIP → SHIP | `b474005d57e8` → `c85e1f783b33` |
| ali | 0 | SHIP → SHIP | unchanged |
| sca | 0 | SHIP → SHIP | unchanged |
| bsc | 0 | REDIRECT → REDIRECT | unchanged |
| bmc | 554 | **exit1 → SHIP** | `2f804ff40c3d` → `f0b57613038e` |
| bri | 0 | SHIP → SHIP | unchanged |

Six orgs byte-identical. One outcome changed, and it is the one the brief asked
for.

### One line of justification per changed checksum

| org | why it moved |
|---|---|
| **sarreid** | P0-8 whitespace only. The §3 play title and its two nav copies read `Lilac Sideboard  Blue Finish` (double space) and now read `Lilac Sideboard Blue Finish`. Visible-text delta is 0 because `html_to_text` already collapsed it; the HTML did not. Verified by diffing the extracted cores of the pre- and post-change HTML — 3 lines, all the same string. |
| **cci** | P0-8 case only. `NOTTAWAY LARGE BRONZE CHANDELI` → `Nottaway Large Bronze Chandeli` in the play title, the nav, the §8 "most-distributed" sentence and the §8 cross-sell sentence — four prose sites `_clean_cell` never reached, because it only re-cases table cells. Plus one table cell, `Briallen White Demi-lune Cabin` → `Demi-Lune` (hyphenated words now capitalise on both sides). |
| **hfg** | P0-7 + P0-8. Four §8 table rows lose their pipe-delimited spec tails (`Type DL-105 — Open Center, Acrylic Bottom and Top Diffusers`), the §8 cross-sell sentence picks up the same label, and §8 gains the two-paragraph project lead. The §3 play title is unchanged — `looks_like_code` still reads the raw field, so hfg keeps `Axis cross-sell` instead of a 60-character heading. |
| **kal** | P0-8 case only. `FLINT 5 LT MULTI DROP` → `Flint 5 LT Multi Drop` in the play title, the nav and two §8 prose sentences; `Sphere 36 in Pendant` → `Sphere 36 IN Pendant` in the table (`IN` is inches, and the render-time caser had been lowercasing it as a connector). |
| **bmc** | P0-10 + P0-8. The run went from exit 1 with no HTML to a full SHIP, so the artifact type itself changed (`bmc_DRAFT_2026-07-09.md` → `Bassett_Mirror_CEO_intelligence_report_2026-07-09.html`). Content changes inside it: two §Q hedge sentences, and 12 §8 labels losing purchase-order prefixes. |
| **da, clc, ali, sca, bsc, bri** | byte-identical, no justification needed. |

### Tests

```
$ .venv-renderer/bin/python -m pytest tests/ -q
150 passed, 6 skipped in 0.62s
```

67 before W1, 150 after. The 6 skips are the three cohort-parametrised suites on
`da`, `sca` and `bsc`, which have no catalog rows.

---

## Self-assessment against the DoD

### P0-10

| DoD line | Verdict |
|---|---|
| `bmc` reaches SHIP with `smoke_check: PASS` and `step10: PASS` | **Met.** Output pasted above. |
| hedges read as English a CEO would accept, not as a bracket | **Met, and it is the line most worth a human read.** Both hedge texts are quoted in full above. They name the uncertainty class and change wording on a stale feed. §Q.3's *"must be authored"* tension is flagged, not hidden. |
| deterministic-only verified on ≥1 PARTIAL and ≥1 STRONG org | **Exceeded** — all 11, through `run.sh`, covering STRONG, PARTIAL and NONE. |
| say which route you took and why | **Met** — added the flag to `run.sh`; reasoning in *Files changed*. |
| no other org changes outcome | **Met.** Only `bmc` moved, exit1 → SHIP. |
| `README.md`'s claim made true or amended | **Made true**, and strengthened to name the confidence levels it was verified at. |

### P0-7

| DoD line | Verdict |
|---|---|
| a written recommendation with the sweep table | **Met.** 11 orgs × 3 candidate threshold pairs, with the ali counter-example that kills the one-gate rule. |
| if implemented, HFG's §8 names the project | **Met.** Lead quoted above. |
| no other org gains a false positive | **Met.** `test_fires_on_hfg_and_nowhere_else` asserts silence on all 10 others against live cache. |
| thresholds are size-relative | **Met.** Both gates are ratios — share of the org's LTM, and unit price against the org's own catalog median. `test_thresholds_are_size_relative_not_absolute` scales a catalog 20× and asserts the verdict and both ratios are unchanged. |
| *"propose, do not unilaterally ship a new signal"* | **Judgment call — flag it.** The brief's next sentence is *"If the rule is clean, implement it"*, and the sweep is clean at every candidate. I implemented, because G1 is the owner reading HFG and a memo does not put the sentence in front of them. The constants are named and owner-pickable; reverting the render half is one `if` in `section_08_products.md.j2`. |

### P0-8

| DoD line | Verdict |
|---|---|
| every org that *has* a catalog is checked, not just HFG | **Met.** All 8 swept; before/after tables for the 5 that changed, explicit zeros for `clc`, `ali`, `bri`. |
| no two SKUs collide | **Met.** Per-org table above; `clc`'s 6 pre-existing collisions carried through unchanged, none introduced. Asserted in tests against live cache. |
| before/after table for every affected org in the evidence file | **Met.** |
| rule survives all 11 catalogs | **Met, with the brief's own correction**: 8 catalogs exist. `da` has no product CSVs; `sca` and `bsc` have them with zero rows. |
| keep the identifying head / drop the dimensional tail / never invent a name / never collapse two SKUs | **Met.** The one place it is thin is `bmc`'s `Gold`, called out under *Residuals*. |

---

## For the reviewer

1. **The `run.sh` scope call** is the one thing I did that the In list does not
   name. Authorised by the DoD's own wording; say if you want it reverted to the
   module form.
2. **The §Q.3 "authored, not templated" tension** in P0-10 is doctrine, and the
   owner's call.
3. **`PROJECT_MIN_SHARE_OF_LTM` and `PROJECT_MIN_UNIT_PRICE_RATIO`** are owner
   constants per `EXECUTION_PLAN.md`. The cohort cannot pick between the three
   candidates; I picked the middle for headroom.
4. **`make check` stays red on golden** — pre-existing, Phase-2 work, worker-blocked.
   `da` and `clc` still match their pre-W1 actual exactly; `sarreid`, `cci`,
   `hfg`, `kal`, `bmc` moved with one line of justification each.
5. **P0-6 untouched**, as instructed.
