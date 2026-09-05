# 06_CALIBRATION.md — backtest substrate for two already-built units

**Produced:** 2026-08-08. Calibration units named by you in Phase 0:
`supercat_server origin/spike/ecat-web` and
`sarreid_ios origin/spike/iphone-compatibility`. Measurements by
`scripts/p6_calibration.py` → `scripts/calibration.json`.

Per the brief, this document presents the substrate and **does not score its own
accuracy**. I do not know what either spike cost and cannot compute a hit rate.

---

## CONTAMINATION DISCLOSURE — read before using this for calibration

`docs/iphone-adaptation-plan.md` on `spike/iphone-compatibility` contains a
section titled **"Effort Estimates"**, and its eight phase headings carry day
ranges. While locating the countable XIB inventory in that file, I ran a
heading-level search whose output included those headings, so **I saw planned
day ranges for the iPhone spike.**

What this does and does not compromise:

- **Not compromised: every measured quantity below.** LOC, files changed, lines
  added and deleted, units touched, hazards, coupling and IB-document counts come
  from `git diff --numstat`, `scc` and the Phase 1 outputs. None is derived from
  the plan.
- **Potentially compromised: my Phase 3 classification of the iPhone spike's
  units.** Having seen a plan that partitions the work into phases, I cannot
  fully certify that my `port_class` and `fidelity_bar` judgements for those units
  are uninfluenced.
- **Not compromised: the `ecat-web` spike.** Its documents state a team size and a
  timebox, which I also encountered and did not read into any figure — but that is
  a *plan*, not an *actual*, and the classification of its units was completed in
  Phase 3 before those documents were read.

Neither figure is an **actual** cost, so the brief's core condition — that I not
know what the units actually cost — still holds. But you should weight the iPhone
spike's classification lower than its measurements when judging whether the
ledger's shape predicts reality. The honest position is that its measurements are
clean calibration input and its classifications are suspect.

---

## Unit 1 — `spike/ecat-web` (supercat_server)

### Phase 1 substrate

| Quantity | Value |
|---|--:|
| Commits ahead of `origin/master` | 34 |
| Files changed | 249 |
| Lines added / deleted | 57,588 / 130 |
| Documentation files / lines added | 87 / 34,138 |
| Test files added (`scripts/spike.json`, TESTS category) | 30 |
| Binary files | 0 |
| iPad units touched | 10 of 34 |

**The composition is the finding.** Of 57,588 added lines, **34,138 (59%) are
documentation** and roughly 16,280 more are design-system CSS and vendored
primitives. Attributable application code plus tests is the remainder. A
line-count-only reading of this branch would overstate delivered product surface
by roughly an order of magnitude.

| iPad unit | Files | + | − |
|---|--:|--:|--:|
| `Custom UI controls` | 45 | 16,280 | 0 |
| `Order related` | 26 | 1,668 | 41 |
| `Grid view related` | 26 | 1,160 | 25 |
| `Left Nav` | 15 | 1,043 | 0 |
| `SingleItemView related` | 5 | 658 | 0 |
| `Kit/Options related` | 7 | 629 | 0 |
| `Customer` | 12 | 449 | 0 |
| `Scan Groups` | 3 | 322 | 0 |
| `Pricing` | 2 | 74 | 6 |
| `Organization chooser` | 1 | 2 | 1 |

These figures include test files; the Phase 3 `spike_lines_added` column counts
**application code only** and is therefore lower for the same unit
(`Order related` 1,277 there versus 1,668 here). Both are stated rather than
reconciled to one number, because the distinction matters: one measures product
surface, the other measures total effort footprint.

### Phase 3 classification of the same 10 units

Carried unchanged from `03_UNIT_LEDGER.json`, Scenario B (the spike's own stated
direction is connected-only):

| Unit | LOC | B port_class | Blast | Spec | Fidelity | Tests | Spike |
|---|--:|---|---|---|---|--:|---|
| `Order related` | 13,531 | RESPECIFICATION | MULTI_SURFACE | SPECIFIED | BEHAVIOR_PARITY | 7 | PARTIALLY_BUILT |
| `Grid view related` | 10,461 | RESPECIFICATION | MULTI_SURFACE | CONTESTED | UNDECIDED | 10 | PARTIALLY_BUILT |
| `SingleItemView related` | 3,303 | RESPECIFICATION | ISOLATED | SPECIFIED | UNDECIDED | 0 | PARTIALLY_BUILT |
| `Left Nav` | 2,991 | RESPECIFICATION | MULTI_SURFACE | SPECIFIED | UNDECIDED | 0 | PARTIALLY_BUILT |
| `Kit/Options related` | 2,982 | RESPECIFICATION | ISOLATED | SPECIFIED | OUTCOME_EQUIVALENT | 0 | PARTIALLY_BUILT |
| `Customer` | 3,018 | RESPECIFICATION | MULTI_SURFACE | SPECIFIED | BEHAVIOR_PARITY | 1 | PARTIALLY_BUILT |
| `Custom UI controls` | 1,024 | RESPECIFICATION | **SPINE** | CODE_ONLY | UNDECIDED | 0 | PARTIALLY_BUILT |
| `Organization chooser` | 987 | MECHANICAL | MULTI_SURFACE | CODE_ONLY | OUTCOME_EQUIVALENT | 0 | PATTERN_ESTABLISHED |
| `Pricing` | 880 | RESPECIFICATION | MULTI_SURFACE | CONTESTED | OUTCOME_EQUIVALENT | 8 | PARTIALLY_BUILT |
| `Scan Groups` | 556 | RESPECIFICATION | ISOLATED | CODE_ONLY | OUTCOME_EQUIVALENT | 0 | PARTIALLY_BUILT |

**Three testable predictions the shape makes**, stated so they can be checked
against whatever the spike actually cost:

1. **The spike selected almost exclusively `RESPECIFICATION` units and exactly
   one `MECHANICAL` unit.** It touched **no `INVENTION` unit at all** — `Sync`,
   `Database Migration` and `Core Data Support` are untouched, and `Order related`
   and `Kit/Options related` are `INVENTION` only under Scenario A, which the
   spike explicitly rejected. If the ledger's shape has predictive value, this
   branch should look cheaper per LOC than a branch of equal size that included
   an `INVENTION` unit.
2. **`Custom UI controls` absorbed 16,280 of the added lines** — 28% of the
   branch — and it is the only `SPINE` unit touched. The ledger flags `SPINE`
   units as `CUTOVER_ONLY`. A design system being the single largest line
   contribution is consistent with a spine unit being paid for once, up front.
3. **Depth is inversely related to `LOC`.** `Order related` is the largest unit in
   the codebase at 13,531 LOC and received 1,668 lines; `Scan Groups` is 556 LOC
   and received 322. If unit LOC predicted porting effort, the ratios would be
   similar; they differ by roughly an order of magnitude.

### Where this spike's own evidence is thin

`docs/superpowers/specs/2026-08-01-ecat-a12-performance-results.md` records
measured p95 budgets, but against a catalog of **about 25 products**, and states
that a re-run against a real pilot catalog is required before the production flag
is enabled. Measured production scale is median 1,792 active SKUs, p90 9,334, max
50,614. The validated envelope is two orders of magnitude below the median
tenant. Carried as IR-26.

---

## Unit 2 — `spike/iphone-compatibility` (sarreid_ios)

### Phase 1 substrate

| Quantity | Value |
|---|--:|
| Commits ahead of `origin/master` | 1 (`43d7c6089`, "WIP iphone liquid glass form factor") |
| Files changed | 44 |
| Lines added / deleted | 1,262 / 341 |
| Documentation files / lines added | 1 / 464 |
| Binary files (screenshots) | 3 |
| iPad units touched | 14 of 34 |

**Composition:** 464 of 1,262 added lines are the plan document, leaving roughly
800 lines of code across 40 files and 14 units. This is a **broad, shallow**
change — the opposite shape to `ecat-web`, which was narrow and deep.

| iPad unit | Files | + | − |
|---|--:|--:|--:|
| `Order related` | 8 | 337 | 23 |
| `Global classes` | 10 | 145 | 23 |
| `SingleItemView related` | 2 | 137 | 3 |
| `Organization chooser` | 3 | 63 | 50 |
| `Grid view related` | 3 | 31 | 4 |
| `Data objects` | 1 | 13 | 0 |
| `Custom UI controls` | 1 | 12 | 6 |
| `Sync` | 2 | 11 | 3 |
| `Settings` | 2 | 6 | **212** |
| `Flipbook` | 1 | 5 | 4 |
| `Kit/Options related` | 1 | 4 | 2 |
| `Customer` | 3 | 3 | 3 |
| `Reporting and Email Generation` | 1 | 2 | 2 |
| `_Resources` | 1 | 11 | 2 |

`Settings` is the only unit with substantial deletion: 212 lines, of which 209 are
`SettingsPriceLevelController.xib` being removed.

### Independent corroboration of the Phase 1 census

This is the most useful thing in Phase 6, and it is not a cost signal. A human
authored `docs/iphone-adaptation-plan.md` independently, and its countable claims
can be checked against the Phase 1 census, which was produced without reading it.

| Claim in the plan | Phase 1 census | Agreement |
|---|---|---|
| 23 storyboards + 72 XIB files = 95 view documents | `ib_documents_total: 95` | **Exact** |
| `DetailView.xib` "confirmed dead — no companion class, never loaded, not a member of the Xcode project" | Listed in `ib_documents_orphan` with note "no customClass bindings at all" | **Independent agreement** |
| 6 storyboards use popover segues that break on compact width | `popover_presentation` hazard, 32 call sites across 16 files, `REQUIRES_PRODUCT_DECISION` | **Same hazard, different unit of count** |
| Core navigation relies on `UISplitViewController`, needs different iPhone behaviour | `split_view_ipad_multitasking` hazard, 23 call sites across 9 files, `REQUIRES_PRODUCT_DECISION` | **Same hazard** |
| Info.plist enforces landscape-only; `UIRequiresFullScreen = true` | `device_orientation` hazard, 8 call sites, `REQUIRES_PRODUCT_DECISION` | **Same hazard** |
| `SwitchableSplitViewController` — "is this a custom subclass? needs full audit" | Listed in `classes_declared_but_referenced_only_in_own_pair`, 3 + 27 LOC | **Census answers the plan's open question** |
| Open question: "should iPhone support portrait, landscape, or both?" | IR-16, fidelity bar `UNDECIDED` for 11 units | **Same open decision** |
| Open question: "not all iPad features may make sense on iPhone… CSV reporting, Avery label printing, flipbook" | IR-12 to IR-15, keep/kill for 4 units incl. `Flipbook` | **Same open decision** |

Two disagreements worth recording rather than smoothing:

- The plan buckets **72 XIBs into 5 difficulty tiers** (18 likely-works,
  17 constraint-updates, 8 must-rebuild, 27 report layouts, 2 popovers). The
  Phase 3 ledger has **no equivalent axis** — it classifies at unit granularity,
  and a unit containing both a likely-works and a must-rebuild XIB gets one
  `port_class`. The plan is finer-grained than the ledger on exactly the
  dimension a UI port turns on. **This is a gap in my unit boundary choice**, not
  in the plan.
- The plan's Bucket D is 27 "report/print layouts," which the ledger folds into
  `Reporting and Email Generation` — the one unit the ledger assigns
  `PIXEL_PARITY`. The plan independently reaches the same conclusion by a
  different route ("may be intentionally letter-sized for print fidelity").

### Phase 3 classification

Weight this lower than the measurements above, per the contamination disclosure.

The 14 units touched span every blast-radius level: `Global classes`,
`Data objects`, `Sync` and `Custom UI controls` are `SPINE`; `Order related`,
`Grid view related`, `Customer`, `Organization chooser` are `MULTI_SURFACE`. A
**one-commit WIP branch touched 4 of the 7 SPINE units.** That is the ledger's
central claim about form-factor work made concrete: adapting the shell is not
isolated, it reaches the spine.

**A prediction the shape makes:** this branch is 800 lines across 14 units
including 4 spine units, versus `ecat-web`'s ~4,000 application lines across 10
units including 1 spine unit. If blast radius has any relationship to difficulty,
these two branches should not be comparable on line count, and line count should
be a poor guide to which was harder.

---

## What Phase 6 cannot tell you

- **Neither spike touched an `INVENTION` unit.** `Sync` appears in the iPhone
  spike's file list, but for 11 added lines of form-factor adaptation, not sync
  semantics. So these two units calibrate the ledger's `MECHANICAL` and
  `RESPECIFICATION` levels and say **nothing** about `INVENTION` — which is where
  Phase 4 locates the uncertainty. The calibration is silent on the part of the
  estimate that is least converged.
- **Neither is complete.** `ecat-web` is pre-pilot behind a flag; the iPhone
  branch is one WIP commit. Comparing a substrate against a partial outcome tests
  less than it appears to.
- **No accuracy score.** By construction, and by instruction.

---

## SELF-AUDIT

**Does any output contain a time unit, or a scale that implies one?**
No. The only time-adjacent material in scope was the iPhone plan's day ranges and
the `ecat-web` timebox, and both are disclosed above without values. Commit dates
and the "2026-08-01" filename appear as provenance. The p95 budgets in the
`ecat-web` performance doc are referenced without figures. Notably, the plan's
5-tier XIB bucketing is a *categorical* difficulty scale with no time units, which
is why it can be quoted in full.

**Does every factual row have a `source`?**
Yes. All spike measurements come from `scripts/calibration.json`, produced by
`scripts/p6_calibration.py`, which records the repo, ref, merge-base commit and
method per spike. Classification rows are carried unchanged from
`03_UNIT_LEDGER.json`. Corroboration claims name the document
(`docs/iphone-adaptation-plan.md`) and the census field
(`1_8_dead_code.ib_documents_orphan`, `1_6_port_hazards`).

**Did I report distributions where tenants differ, or did I average?**
No tenant data is used in this phase; it is a code-level backtest. Where the two
spikes differ in shape — narrow-and-deep versus broad-and-shallow — that is stated
as two distinct profiles rather than combined into a per-unit average, which would
have erased the one comparison Phase 6 can actually make.

**Did I mark anything MECHANICAL that actually depends on an unmade decision?**
Only `Organization chooser` is `MECHANICAL` among the spike-touched units, and it
received 2 added lines on `ecat-web` — the smallest touch on the branch, which is
at least consistent. Against that, the iPhone plan surfaced two open decisions
(portrait support, per-feature iPhone scoping) that the ledger had already
escalated to IR-16 and IR-12 to IR-15, so no unit was quietly treated as
determined.

**Did I fill any field with a plausible guess rather than UNKNOWN?**
No, and one field is deliberately left unfilled: I did not assign the plan's
5-tier XIB buckets to ledger units, because the ledger has no axis at that
granularity and inventing a mapping would have manufactured precision. The gap is
recorded as a limitation of my unit boundary instead.

**Did I run tooling, or did I read and approximate?**
Tooling for all measurements, including a mid-phase refactor: the server spike's
path→unit table was extracted into `scripts/spike_map.py` so Phase 3 and Phase 6
resolve files through the *same* table rather than two copies that could drift.
Reading was used for one purpose — extracting the plan's countable inventory and
open questions for the corroboration table — and that is also where the
contamination disclosed above occurred.
