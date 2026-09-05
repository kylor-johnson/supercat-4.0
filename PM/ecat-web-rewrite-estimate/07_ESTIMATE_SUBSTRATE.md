# 07_ESTIMATE_SUBSTRATE.md — eCat iPad → Responsive Web

**Produced:** 2026-08-08. Rollup of `00_PLAN.md`, `01_CODE_CENSUS.{json,md}`,
`02_TENANT_CENSUS.{json,md}`, `03_UNIT_LEDGER.{json,md}`,
`04_INVENTION_REGISTER.md`, `05_KILL_LIST.md`, `06_CALIBRATION.md`.

This is a bill of materials, a classification ledger, an invention register and a
kill list. It is not an estimate. Converting it to time requires a calibrated
rate card that is not in this document and was not used to produce it.

---

## 1. Scope of analysis, and what could not be seen

### What was analysed

| Artifact | Pin | Scope |
|---|---|---|
| `sarreid_ios` (eCat iPad) | `129242b0e27401b9019f805066f1b8ea88da5380` | Full census; 86,610 LOC, 34 classified units |
| `supercat_server` | `bd7895a7e` | API surface, importer behaviour, component registry |
| `supercat_server` `spike/ecat-web` | `fa8a2cbe7` | Spike measurement, Phase 6 calibration |
| `sarreid_ios` `spike/iphone-compatibility` | `43d7c6089` | Phase 6 calibration |
| Production Postgres | queried 2026-08-08 | 255 tenants |
| Mixpanel via BigQuery | 2024-11-01 → 2026-08-07 | 10,661,150 events, 192 tenants, 5,970 devices |

Analysis ran in detached worktrees under `/tmp/ecat-audit/`. No user checkout was
modified. All Postgres and Jira access was read-only.

### What could not be seen

| Gap | Consequence |
|---|---|
| **`gh` unauthenticated** | Cannot confirm `sarreid_ios` is the canonical eCat iOS repository rather than one client fork. Circumstantial evidence favours canonical (single `eCat` build target, runtime org selection across 191 tenants, global themes plist) but it is **unproven**. IR-25. |
| **No CocoaPods checkout** | Third-party LOC uncounted. Correct for a rewrite bill of materials — you do not rewrite AFNetworking — but complexity totals exclude dependency internals. |
| **Build never verified** | No coverage instrumentation. Test *reference* counts are reported; executed coverage is unavailable, not estimated. |
| **Linear and Notion never probed** | Recorded in Phase 0 and never closed. This gap grew in importance: an iPad specification was found in the *server* repository after Phase 1 asserted none existed, so the remaining `CODE_ONLY` population may shrink further. IR-24. |
| **iPad-only vs shared endpoints** | `ipad_only_vs_shared: UNKNOWN`. 17 distinct iOS endpoint resources and 75 server API actions were enumerated, but which are exclusive to the iPad could not be determined mechanically. |
| **Revenue and contract values** | Not queried, per instruction. Blast radius uses users, devices, sessions, order counts and catalog size only. |
| **Offline composition sessions** | No instrument exists. Order-gap telemetry measures creation-to-submission, not how long a rep works disconnected before reconnecting. A structural blind spot in the Scenario A evidence. |

---

## 2. Scenario A vs Scenario B — the countable delta

**8 of 34 units change `port_class`. 21,772 LOC, 14,743 of it LOGIC.**

| Unit | LOC | LOGIC | Scenario A | Scenario B |
|---|--:|--:|---|---|
| `Order related` | 13,531 | 9,902 | **INVENTION** | RESPECIFICATION |
| `Kit/Options related` | 2,982 | 2,292 | **INVENTION** | RESPECIFICATION |
| `Categories` | 2,138 | 1,127 | RESPECIFICATION | MECHANICAL |
| `Documents Related` | 1,300 | 289 | RESPECIFICATION | MECHANICAL |
| `RepActivity` | 1,166 | 837 | RESPECIFICATION | MECHANICAL |
| `Placements` | 435 | 264 | RESPECIFICATION | MECHANICAL |
| `Database Migration` | 177 | 32 | **INVENTION** | MECHANICAL |
| `Core Data Support` | 43 | 0 | **INVENTION** | MECHANICAL |

26 units do not change. The single most consequential non-change is `Sync`:
**INVENTION under both scenarios**, 3,935 LOC, 255 tenants, `SPINE`, 0 test files.

**Invention delta:** Scenario A carries 5 INVENTION units / 20,668 LOC. Scenario B
carries 1 / 3,935 LOC. **The fork is worth 4 units and 16,733 LOC of invention.**

Two asymmetries are larger than their LOC suggests. `Database Migration` and
`Core Data Support` total 220 LOC but represent 63 SQLite migration files, 1,577
SQL lines, 47 tables, 19 Core Data model versions, 18 inter-version migrations and
372 combined persistence call sites across 83 files. Under B they largely
disappear; under A they must be reinvented on an unchosen browser storage engine.

---

## 3. Rollups

### By port class

| Port class | A units | A LOC | B units | B LOC |
|---|--:|--:|--:|--:|
| MECHANICAL | 5 | 2,021 | 11 | 7,280 |
| RESPECIFICATION | 19 | 60,957 | 17 | 72,431 |
| **INVENTION** | **5** | **20,668** | **1** | **3,935** |
| REQUIRES_PRODUCT_DECISION | 4 | 2,490 | 4 | 2,490 |
| UNKNOWN | 1 | 327 | 1 | 327 |

`MECHANICAL` is the smallest bucket under both scenarios. That is the substantive
finding of the ledger: **almost nothing in this codebase can be ported by
transcription.**

### By blast radius (scenario-invariant)

| Blast radius | Units | LOC |
|---|--:|--:|
| **SPINE** | 7 | 29,042 |
| MULTI_SURFACE | 10 | 34,956 |
| ISOLATED | 16 | 22,138 |
| UNKNOWN | 1 | 327 |

The 7 SPINE units — `Global classes`, `Data objects`, `Sync`, `Login`,
`Custom UI controls`, `Database Migration`, `Core Data Support` — are all
`CUTOVER_ONLY`. Assigned from the measured import graph, not asserted:
`Global classes` fan-in 24, `Data objects` fan-in 20, the two highest in the
codebase.

### By fidelity bar

| Fidelity bar | Units | LOC |
|---|--:|--:|
| OUTCOME_EQUIVALENT | 20 | — |
| **UNDECIDED** | **11** | **25,029** |
| BEHAVIOR_PARITY | 2 | — |
| PIXEL_PARITY | 1 | 6,548 |

### By reversibility and acceptance

| Reversibility | Units | | Acceptance | Units |
|---|--:|---|---|--:|
| FLAGGABLE | 26 | | TESTABLE_NOT_TESTED | 20 |
| CUTOVER_ONLY | 7 | | TEST_EXISTS | 10 |
| UNKNOWN | 1 | | HUMAN_JUDGMENT_ONLY | 4 |
| DUAL_RUNNABLE | **0** | | | |

**No unit is `DUAL_RUNNABLE`.** Nothing in this codebase can be run in parallel
against the existing implementation to compare outputs, which removes the cheapest
available verification strategy.

### By spike status and specification coverage (measured)

| Spike status | Units | LOC | | Registry coverage | Units | LOC |
|---|--:|--:|---|---|--:|--:|
| NOT_STARTED | 24 | 46,730 | | DEDICATED_SPEC | 14 | 73,479 |
| PARTIALLY_BUILT | 9 | 38,746 | | REFERENCED | 11 | 6,918 |
| PATTERN_ESTABLISHED | 1 | 987 | | NONE | 9 | 6,066 |

---

## 4. Total LOC by UI / LOGIC / GLUE, in scope and killed

**Baseline: 86,610 LOC.** 34 units classified = 86,463; excluded infrastructure
pseudo-units = 147. Reconciles exactly.

| Class | LOC | Share |
|---|--:|--:|
| LOGIC | 54,023 | 62.4% |
| UI | 10,228 | 11.8% |
| GLUE | 6,592 | 7.6% |
| UNCLASSIFIED | 15,767 | 18.2% |

Interface Builder XML is counted separately, as agreed in Phase 0: **95 documents,
19,246 lines**, not included in the 86,610.

### The sensitivity that bounds this table

The approved rule resolves mixed methods with `LOGIC > GLUE > UI` precedence.
**18,929 LOC matches both LOGIC and UI patterns**, and 470 files are mixed-class.
Re-running with UI-first precedence gives:

| Class | LOGIC-first (approved) | UI-first (sensitivity) |
|---|--:|--:|
| LOGIC | 54,023 | 32,065 |
| UI | 10,228 | 33,653 |
| GLUE | 6,592 | 5,129 |
| UNCLASSIFIED | 15,767 | 15,763 |

**The LOGIC/UI split is not robust to the precedence rule.** LOGIC ranges from
32,065 to 54,023 depending on a classification choice, not on a measurement. Any
rate card that prices LOGIC differently from UI must be applied with this range in
view. Both totals are reported rather than one, because reporting only the
approved figure would imply a precision the method does not have.

### Killed

| Category | Items | LOC not rewritten |
|---|--:|--:|
| `UNREACHABLE` — zero inbound navigation edges | 5 screens | 104 |
| `UNREACHABLE` — referenced only by own header/impl pair | 6 classes | 290 |
| `UNREACHABLE` — on disk, not in Xcode project | 3 files | not compiled |
| `UNREACHABLE` — orphan IB documents | 8 of 95 | XML, outside baseline |
| `LOW_USE` — ranked, tenant conversation required | 7 units | 4,418 (3,055 LOGIC) |
| **Ceiling if every item were dropped** | **18** | **4,812** |

**4,812 LOC is 5.6% of the baseline.** In scope after a maximal kill: 81,651 LOC.
The kill list removes **no** invention item and unblocks **no** SPINE unit.

---

## 5. Port hazards, ranked by tenants touched

23 hazards were probed. **7 have zero call sites** — `pencilkit_handwriting`,
`drag_and_drop`, `background_tasks`, `keyboard_hardware_input`,
`sqlite_vec_vector_search`, `coreml_on_device_embeddings` — meaning the capability
is not used and is not a porting concern. The remaining 17:

| Hazard | Max tenants | Units | Downstream LOC | Call sites | Files | Web equivalent |
|---|--:|--:|--:|--:|--:|---|
| `fmdb_sqlite_direct` | 255 | 8 | 54,368 | 151 | 34 | POLYFILLABLE |
| `popover_presentation` | 255 | 8 | 45,241 | 32 | 16 | **REQUIRES_PRODUCT_DECISION** |
| `core_data_local_persistence` | 255 | 6 | 43,926 | 221 | 49 | **REQUIRES_PRODUCT_DECISION** |
| `local_filesystem` | 255 | 8 | 41,874 | 66 | 19 | **REQUIRES_PRODUCT_DECISION** |
| `printing` | 255 | 3 | 28,311 | 10 | 3 | POLYFILLABLE |
| `webview_bridge` | 255 | 5 | 27,300 | 36 | 6 | NATIVE_EQUIVALENT |
| `device_orientation` | 255 | 3 | 25,038 | 8 | 3 | **REQUIRES_PRODUCT_DECISION** |
| `pdf_generation_or_render` | 255 | 5 | 23,778 | 37 | 13 | POLYFILLABLE |
| `split_view_ipad_multitasking` | 255 | 3 | 22,777 | 23 | 9 | **REQUIRES_PRODUCT_DECISION** |
| `firebase_crashlytics_analytics` | 255 | 1 | 11,302 | 10 | 3 | NATIVE_EQUIVALENT |
| `mixpanel_telemetry` | 255 | 1 | 11,302 | 6 | 3 | NATIVE_EQUIVALENT |
| `push_local_notifications` | 255 | 1 | 11,302 | 2 | 2 | POLYFILLABLE |
| `zip_archive` | 255 | 1 | 3,935 | 2 | 1 | POLYFILLABLE |
| `biometric_auth` | 255 | 1 | 1,606 | 16 | 3 | POLYFILLABLE |
| `keychain` | 255 | 1 | 1,606 | 9 | 1 | POLYFILLABLE |
| `mailcompose_native_share` | 157 | 4 | 31,840 | 47 | 15 | POLYFILLABLE |
| `camera_barcode_scanning` | 124 | 2 | 20,079 | 18 | 6 | POLYFILLABLE |

**5 hazards require a product decision**, and they are concentrated in the largest
units: `popover_presentation` and `core_data_local_persistence` between them reach
`Order related`, `Global classes`, `Data objects`, `Grid view related`,
`Customer`, `Kit/Options related` and `Categories`.

Note that `fmdb_sqlite_direct` tops the ranking with 151 call sites and 54,368
downstream LOC while being marked `POLYFILLABLE`. Under Scenario B it mostly
vanishes; under Scenario A "polyfillable" means a browser storage engine must be
chosen, which is IR-06.

---

## 6. Open invention items

**Open invention items: 26.**

| Group | Items | Nature |
|---|--:|---|
| A — Scenario and target | 3 | Everything inherits these |
| B — Scenario-A-conditional inventions | 3 | Void if the fork resolves to B |
| C — Port hazards | 5 | Design decisions; call sites measured |
| D — Keep or kill | 4 | Commercial; tenants named |
| E — Fidelity bar and contested specification | 5 | 1 + 4 documented conflicts |
| F — Unresolved unknowns | 6 | Evidence gaps, not decisions |

Under the brief's literal scope — `INVENTION`, `REQUIRES_PRODUCT_DECISION` and
unresolved `UNKNOWN` — the count is **20**. Composition is given in
`04_INVENTION_REGISTER.md` so it can be recomputed under either definition.

**N is the width of this estimate's uncertainty, and the estimate should not be
treated as converged while N is large.** Two properties matter more than the
number. It is **top-heavy**: IR-01, the scenario fork, reclassifies 8 units and
21,772 LOC and voids or activates all three Group B items, so one decision
collapses a disproportionate share of the range. And IR-02 **survives every
resolution** — the sync engine is INVENTION under both scenarios, so no answer to
the fork removes it.

---

## 7. `CODE_ONLY` behaviour count — the archaeology backlog

**17 units, 9,609 LOC — 11% of the classified baseline.**

This figure was corrected during Phase 3 and the correction is the largest single
change in the analysis. The first pass reported **28 units / 61,512 LOC (71%)**,
inheriting Phase 1's finding that no documentation existed. Phase 1 had searched
the **iOS** repository. `docs/design/ecat-component-registry/` — a 22-file,
19,329-line structured specification of the iPad application dated 2026-04-03,
covering 84 components, 5 workflows, 40 SQLite tables, 4 Core Data entities and
236 configuration settings — lives on `supercat_server` `origin/master`.

| `behavior_specification` | First pass | Corrected |
|---|---|---|
| CODE_ONLY | 28 units / 61,512 LOC | **17 units / 9,609 LOC** |
| SPECIFIED | 2 units / 2,495 LOC | 13 units / 54,398 LOC |
| CONTESTED | 4 units / 22,456 LOC | 4 units / 22,456 LOC |

The remaining archaeology backlog is concentrated in small units. The largest are
`Documents Related` (1,300), `RepActivity` (1,166), `Custom UI controls` (1,024),
`ShowroomCart` (1,014) and `Organization chooser` (987). **No `CODE_ONLY` unit
exceeds 1,300 LOC.**

Three qualifications on the credit given to the specification:

1. It self-reports status `needs_attention` — 10 broken dependency
   cross-references and 3 components referenced but never registered
   (`action-popover`, `order-list`, `commitments-view`).
2. It lags the code. Dated 2026-04-03, it documents 4 Core Data entities; the
   model in force (`eCat 20260425`) has 3.
3. Per-unit coverage is uneven — 85.7% of `Left Nav`'s files are named, versus
   5.6% of `Pricing`'s.

**A separate count that documentation does not reduce:** 15 units have **zero test
files and majority-LOGIC content** — 14,544 LOGIC LOC across 21,981 total LOC.
Specification is not an executable check. 20 of 34 units remain
`TESTABLE_NOT_TESTED`, and 4 are `HUMAN_JUDGMENT_ONLY`.

**4 units are `CONTESTED`** — 22,456 LOC where a document exists *and* disagrees
with the implementation: `Data objects` (fixed 40-table shape documented vs 240
tenants carrying custom fields, max 185), `Grid view related` (6 images vs 12),
`Pricing` (eCat Online markup rules misattributed to the iPad), `Query`
(SmartList delimiter). `CONTESTED` is a stronger claim than `CODE_ONLY`, not a
weaker one.

---

## 8. Coverage gaps

### What the codebase could not answer

| Gap | Detail |
|---|---|
| iPad-only vs shared endpoints | `UNKNOWN`. 17 iOS endpoint resources and 75 server API actions enumerated; exclusivity not mechanically determinable. |
| Executed test coverage | Build never verified; only test *references* counted. |
| Swift coupling | `#import`-based graph cannot see Swift sibling references. 8 units report fan-in and fan-out 0 and are 100% Swift — measurement blindness, flagged `UNKNOWN_SWIFT_OPAQUE`, not proven isolation. |
| `Spreadsheet Import` entry point | 327 LOC with no traceable caller and no usage signal. `port_class`, `blast_radius`, `reversibility` all `UNKNOWN`. |
| Repository canonicity | `gh` unauthenticated. |
| XIB-level port difficulty | The iPhone plan buckets 72 XIBs into 5 difficulty tiers. The ledger has no axis at that granularity — a unit containing both a trivial and a rebuild-required XIB receives one `port_class`. **A limitation of the PBXGroup unit boundary.** |

### What the tenants could not answer

| Gap | Detail |
|---|---|
| Offline composition sessions | Not instrumented. The order-gap probe measures creation-to-submission, not disconnected working sessions. Structural. |
| `ShowroomCart`, `RepActivity`, `Spreadsheet Import` usage | **No telemetry event exists.** Reach for the first two is Postgres configuration, not measured usage; the third has neither. |
| Push notification delivery | Not in the telemetry schema. `Notifications` reach is `UNKNOWN`. |
| 63 tenants absent from telemetry | 255 tenants in Postgres, 192 in Mixpanel. The 63 are unexplained rather than assumed inactive. |
| Mixpanel queue truncation | The on-device queue is bounded, so long disconnections may be dropped. All delay figures are **lower bounds**. |

### Defects found in the instrumentation itself

Two independent defects in the prebuilt `org_feature_usage_report` BigQuery view,
found by querying raw events instead:

1. **Phase 2:** three features reported zero usage because the view filtered on
   `type` discriminators the data does not carry — it expected `my_list`,
   `customer_product_list` and `maybe_list` where the column holds `user`,
   `customer` and `maybe`. It also double-counted `view_customer_on_order_items`.
2. **Phase 5:** six event names the view relies on **do not exist** in the
   telemetry: `add_to_list_from_flipbook`, `order_from_flipbook`, `order_kit`,
   `order_configured_item`, `view_placements`, `view_showroom_cart`. The live
   catalog holds 50 distinct names, dumped to `out/p5_event_catalog.txt`.

Additionally, **non-production organizations were inflating reach counts**.
`demo`, `demo2`, `demo3`, `test1`, `pf_test`, `sc_test`, `ufistaging` and
`ihw_staging` appear in the telemetry. Separating them changed conclusions:
`Commitments` reaches 4 organizations, of which **2 are customers**.

This view should not be treated as load-bearing.

### One methodological error found and corrected

Phase 1 searched for documentation in the repository under analysis and concluded
none existed. The specification was in the adjacent repository. The corrected
figure — 9,609 rather than 61,512 `CODE_ONLY` LOC — is a 6.4× change in the
headline finding, produced by widening a search scope rather than by any new
tooling. `01_CODE_CENSUS.md` carries the correction notice; `03_UNIT_LEDGER.json`
retains `behavior_specification_first_pass` on every row so the change is
auditable. Linear and Notion remain unprobed, so the same class of error may still
be present.

---

## SELF-AUDIT

**Does any output contain a time unit, or a scale that implies one?**
No duration, no disguised duration, no rate. Every figure is a count or a
categorical level. Deliberate exclusions, each disclosed at the point of use:
`docs/design/ecat-web-spike.md` states a team size and a timebox;
`docs/iphone-adaptation-plan.md` has an "Effort Estimates" section with day ranges
in its headers, which I saw and did not use (disclosed in `06_CALIBRATION.md`);
the spike performance document states p95 latency budgets. Where elapsed time
appears in `04_INVENTION_REGISTER.md` it describes **observed tenant behaviour** —
how long devices stayed disconnected — which is the measurement the scenario fork
turns on, not a quantity of work.

**Does every factual row have a `source`?**
Yes. Section 1 pins every artifact to a commit or a query date. Sections 2 through
7 aggregate `03_UNIT_LEDGER.json` (68 rows, each with `source` and
`tenants_touched_basis`), `01_CODE_CENSUS.json` and `02_TENANT_CENSUS.json`, all
of which carry per-row provenance. Rollups are reproducible from
`scripts/p3_ledger.py`, `p4_downstream.py`, `p5_tables.py`, `p6_calibration.py`
and `p7`'s hazard ranking, with raw output retained under `out/`. No row was
deleted for missing provenance in any phase.

**Did I report distributions where tenants differ, or did I average?**
Distributions. Section 5 ranks hazards by maximum tenant reach and shows unit
counts rather than a mean. The scenario-fork evidence reports full bucket
distributions and per-device peaks, because the tail is the argument. Catalog scale
is reported min / p10 / median / p90 / max with outlier tenants named individually
(`5` at 1,669,094 matrix rows; `109` at 770,494). The kill list names every
affected tenant rather than counting them. The one place a single number could
have hidden variance — the LOGIC/UI split — is reported as a range under both
precedence rules instead.

**Did I mark anything MECHANICAL that actually depends on an unmade decision?**
`MECHANICAL` is the smallest bucket under both scenarios (5 units / 2,021 LOC
under A; 11 / 7,280 under B), which is the outcome this check is meant to produce.
It was re-run after the specification was discovered — the strongest temptation to
upgrade — and **no unit was reclassified**, because a document describing iPad
behaviour is not a known web equivalent. Three units were held back from
`MECHANICAL` deliberately (`Notifications`, `ActionPopover`, `Scan Groups`) and
four were escalated out of port classification entirely because keep-or-kill
precedes porting.

**Did I fill any field with a plausible guess rather than `UNKNOWN`?**
No. `UNKNOWN` survives in the final rollup: one unit's `port_class`,
`blast_radius` and `reversibility`; two units' `tenants_touched`; 11 units'
`fidelity_bar`; the iPad-only-vs-shared endpoint split; repository canonicity; and
coupling for 8 Swift-only units. Each is carried into
`04_INVENTION_REGISTER.md` Group F with a named resolution path.

**Did I run tooling, or did I read and approximate?**
Tooling, and it corrected the analysis four times: the LOC partition assertion
caught a missing 109-LOC unit; the registry scan overturned the `CODE_ONLY`
headline; raw event queries invalidated six event names in a prebuilt view; and
separating demo organizations halved a tenant count. Reading was used for one
purpose only — extracting *decisions* recorded in design documents, which are not
countable — and those passages are quoted with file paths and branch names so they
can be checked.

**Did I volunteer a time estimate anywhere?**
No. There is no conclusion, no recommendation and no timeline in this document,
and the one thing that would make this analysis worthless is not present in it.
