# 03_UNIT_LEDGER.md — eCat iPad → Responsive Web

**Status:** Phase 3 complete, and **amended twice after the first pass**.
Machine-readable companion: `03_UNIT_LEDGER.json` (68 rows = 34 units × 2
scenarios). **Produced:** 2026-08-08

---

## Two amendments you should read before the tables

Both amendments correct the first pass. Both are recorded in
`03_UNIT_LEDGER.json → amendments_to_first_pass`, and every affected row keeps
`behavior_specification_first_pass` so the change is auditable rather than
silently overwritten.

### Amendment 1 — `spike_status` was approved and then omitted

Phase 0 §2.1 proposed a categorical `spike_status` field and it was approved.
The first Phase 3 pass did not include it. Without it the ledger silently treats
already-built work as unbuilt. It is now measured from
`git diff --numstat` between the merge-base and
`supercat_server origin/spike/ecat-web`, with a mechanical threshold:
`PARTIALLY_BUILT` ≥ 50 added lines of unit-specific application code,
`PATTERN_ESTABLISHED` 1–49, `NOT_STARTED` 0.

### Amendment 2 — an iPad specification exists, and Phase 1 missed it

`docs/design/ecat-component-registry/` on **`supercat_server` `origin/master`**
is a 22-file, 19,329-line structured specification **of the iPad app**, dated
2026-04-03. By its own validation report it documents **84 components, 5
workflows, 40 SQLite tables, 4 Core Data entities and 236 configuration
settings**, including a 517-line `_sync-protocol.yaml` and a
`workflows/sync-cycle.yaml`.

Phase 1 did not find it because Phase 1 searched the **iOS** repository. The
specification for the iOS app lives in the **server** repository. That is a
coverage error in Phase 1, and it invalidated the first pass's headline finding.

**Effect on the archaeology backlog:**

| `behavior_specification` | First pass | Amended |
|---|---|---|
| CODE_ONLY | 28 units, 61,512 LOC | **17 units, 9,609 LOC** |
| SPECIFIED | 2 units, 2,495 LOC | **13 units, 54,398 LOC** |
| CONTESTED | 4 units, 22,456 LOC | 4 units, 22,456 LOC |

The first pass reported that 71% of the codebase was undocumented behaviour.
The measured figure is **11%**. Coverage was assigned mechanically: a unit is
`SPECIFIED` when a registry component or workflow file whose *subject* is that
unit exists (the mapping is one auditable line per unit in
`scripts/p3_ledger.py → DEDICATED`), `CONTESTED` when a document exists *and
disagrees* with the implementation, and `CODE_ONLY` otherwise. `CONTESTED`
outranks `SPECIFIED`, because a document that disagrees with the code is worse
than no document.

**Three cautions against over-crediting the registry.** It self-reports status
`needs_attention`, with 10 broken dependency cross-references and 3 components
referenced but never registered — `action-popover`, `order-list` and
`commitments-view`. It is dated 2026-04-03 and describes 4 Core Data entities,
whereas the model in force (`eCat 20260425`, per `.xccurrentversion`) has 3, so
it is already behind the code by at least one entity. And it names only a
fraction of each unit's files — 85.7% for `Left Nav` but 5.6% for `Pricing` —
so per-unit coverage is uneven and the percentage column below matters as much
as the level.

**What the registry did not change: the sync classification.** `_sync-protocol.yaml`
independently confirms Phase 1.4. It states that products use incremental sync
and **every other entity uses full-replacement** — "download everything and
replace local data" — and it contains no conflict, merge, last-write-wins or
tombstone semantics anywhere in 517 lines. The specification describes a
one-way, server-authoritative protocol. `Sync` therefore moves from CODE_ONLY to
SPECIFIED and stays **INVENTION in both scenarios**: the document makes it
*certain*, rather than merely likely, that there is no conflict resolver to port.

---

## Unit boundary — justified once

A **unit** here is one Xcode `PBXGroup`-derived code unit, the boundary approved
in Phase 0 §1.3. That choice is kept for one reason that matters to this
document's arithmetic: **PBXGroup units partition the source**, so `loc_ui +
loc_logic + loc_glue` summed over units equals the Phase 1.2 totals exactly, with
no double counting.

Engines are therefore **not** separate rows — each engine already *is* a unit
(`Sync`, `Pricing`, `Kit/Options related`, `Query`, `Database Migration`), and
each row records its `engine_role`. Introducing an "ENGINE_CPQ" row alongside
`Kit/Options related` would double-count 2,982 LOC.

**Partition reconciliation:** 34 units classified = 86,463 LOC. Excluded
infrastructure pseudo-units = 147 LOC (`_Other Sources` 129, `_SuperCatTest` 11,
`_UNMAPPED` 7 — none carry first-party product behaviour). 86,463 + 147 = 86,610
= the Phase 1.2 total. **Reconciles.**

Two units carry `tenants_touched: UNKNOWN` rather than a number:
`Spreadsheet Import` and `Notifications`. No telemetry event and no Postgres
table maps to either, so their reach is unmeasured. Both are escalated to Phase 4
as evidence gaps rather than filled with a plausible figure.

---

## Rollups

### By port class

| Port class | Scenario A units | Scenario A LOC | Scenario B units | Scenario B LOC |
|---|--:|--:|--:|--:|
| MECHANICAL | 5 | 2,021 | 11 | 7,280 |
| RESPECIFICATION | 19 | 60,957 | 17 | 72,431 |
| **INVENTION** | **5** | **20,668** | **1** | **3,935** |
| REQUIRES_PRODUCT_DECISION | 4 | 2,490 | 4 | 2,490 |
| UNKNOWN | 1 | 327 | 1 | 327 |

**The countable delta between the scenarios is 4 units and 16,733 LOC of
INVENTION.** Scenario A carries 5 INVENTION units totalling 20,668 LOC; Scenario
B carries 1, the sync engine, at 3,935 LOC. Eight of 34 units change class; 26 do
not.

### By blast radius (scenario-invariant)

| Blast radius | Units | LOC |
|---|--:|--:|
| **SPINE** | 7 | 29,042 |
| MULTI_SURFACE | 10 | 34,956 |
| ISOLATED | 16 | 22,138 |
| UNKNOWN | 1 | 327 |

The 7 SPINE units are `Global classes`, `Data objects`, `Sync`, `Login`,
`Custom UI controls`, `Database Migration`, `Core Data Support`. SPINE was
assigned from the measured coupling graph, not asserted: `Global classes` has
fan-in 24 and `Data objects` fan-in 20, the two highest in the codebase.

### By behaviour specification (amended)

| Specification | Units | LOC |
|---|--:|--:|
| SPECIFIED | 13 | 54,398 |
| CONTESTED | 4 | 22,456 |
| **CODE_ONLY** | **17** | **9,609** |

**CODE_ONLY count: 17 units, 9,609 LOC — 11% of the classified codebase.** That
is the archaeology backlog: behaviour that exists nowhere but the implementation.
It is heavily concentrated in the small units. The largest are `Documents
Related` (1,300), `RepActivity` (1,166), `Custom UI controls` (1,024),
`ShowroomCart` (1,014) and `Organization chooser` (987); no CODE_ONLY unit
exceeds 1,300 LOC.

The 4 CONTESTED units carry a named, evidenced disagreement each, recorded in
`contested_because`: `Data objects` (the registry documents a fixed 40-table /
4-entity shape, but 240 tenants carry product custom fields, median 33.5 and max
185), `Grid view related` (6 documented product images vs 12 under the paid
`enable_twelve_product_images` flag), `Pricing` (KB describes eCat Online
per-browser markup rules that do not apply to the iPad, where visibility is
governed by user group; the registry names 1 of 18 Pricing files), and `Query`
(SmartList item lists documented comma-separated, implemented newline-separated).

### By spike status (measured)

| Spike status | Units | LOC |
|---|--:|--:|
| NOT_STARTED | 24 | 46,730 |
| PARTIALLY_BUILT | 9 | 38,746 |
| PATTERN_ESTABLISHED | 1 | 987 |

Nine units have a working web surface on `origin/spike/ecat-web`. Of the branch's
57,588 added lines, only about 4,000 are unit-attributable application code —
34,138 lines are design documentation and 16,280 are the design system and CSS.
The spike is a **thin vertical slice with heavy documentation**, not a
substantially complete port, and the per-unit line counts in the amendments table
show how thin: `Order related` 1,277, `Left Nav` 694, `Kit/Options related` 547,
`Grid view related` 491, `SingleItemView related` 471.

### By registry coverage (measured)

| Registry coverage | Units | LOC |
|---|--:|--:|
| DEDICATED_SPEC | 14 | 73,479 |
| REFERENCED | 11 | 6,918 |
| NONE | 9 | 6,066 |

### By acceptance determinism and fidelity bar

| Acceptance | Units | | Fidelity bar | Units |
|---|--:|---|---|--:|
| TESTABLE_NOT_TESTED | 20 | | OUTCOME_EQUIVALENT | 20 |
| TEST_EXISTS | 10 | | **UNDECIDED** | **11** |
| HUMAN_JUDGMENT_ONLY | 4 | | BEHAVIOR_PARITY | 2 |
| | | | PIXEL_PARITY | 1 |

The registry changed no acceptance value. It documents behaviour; it does not
execute. 20 units remain testable but untested.

11 units have an `UNDECIDED` fidelity bar. The spike narrows this without
settling it: `docs/design/ecat-web-spike.md` records the decision "this is a
**full UX redesign**, not a responsive patch," which rules out PIXEL_PARITY for
spike-covered units, and the spike ships both `_desktop_shell_nav` and
`_phone_shell_nav`. But the same document also states that "detailed
UX/interaction design from a designer is still needed for the full vision," and
the Phase 2.7 device spread (1024×768 through 1366×1024, 12 devices in portrait,
1 phone) still has no stated target. Escalated to Phase 4.

`PIXEL_PARITY` is assigned to precisely one unit, `Reporting and Email
Generation`, and it is forced by the artifact rather than chosen: the output is a
PDF a rep hands to a buyer, so correctness is judged by appearance.

---
### Master ledger

| Unit | LOC | UI | LOGIC | GLUE | UNCL | A | B | Blast | Tenants | Rev | Spec | Accept | Fidelity | in | out | Spike | Reg |
|---|--:|--:|--:|--:|--:|---|---|---|--:|---|---|---|---|--:|--:|---|---|
| Order related | 13531 | 1358 | 9902 | 530 | 1741 | **INV** | RESPEC | MULTI | 117 | FLAG | SPEC | TEST | BEHAVIOR | 10 | 12 | **PART** | **SPEC** |
| Global classes | 11302 | 1508 | 6071 | 992 | 2731 | RESPEC | RESPEC | **SPINE** | 255 | CUTOVER | SPEC | TEST | OUTCOME | 24 | 19 | -- | **SPEC** |
| Data objects | 10955 | 25 | 6919 | 491 | 3520 | RESPEC | RESPEC | **SPINE** | 255 | CUTOVER | **CONTESTED** | TEST | OUTCOME | 20 | 7 | -- | **SPEC** |
| Grid view related | 10461 | 1642 | 6451 | 572 | 1796 | RESPEC | RESPEC | MULTI | 157 | FLAG | **CONTESTED** | TEST | UNDECIDED | 12 | 11 | **PART** | **SPEC** |
| Reporting and Email Generation | 6548 | 1567 | 3223 | 321 | 1437 | RESPEC | RESPEC | ISO | 124 | FLAG | SPEC | HUMAN | PIXEL | 4 | 4 | -- | **SPEC** |
| Sync | 3935 | 149 | 2540 | 741 | 505 | **INV** | **INV** | **SPINE** | 255 | CUTOVER | SPEC | TESTABLE | UNDECIDED | 5 | 6 | -- | **SPEC** |
| SingleItemView related | 3303 | 650 | 1840 | 279 | 534 | RESPEC | RESPEC | ISO | 157 | FLAG | SPEC | HUMAN | UNDECIDED | 4 | 10 | **PART** | **SPEC** |
| Customer | 3018 | 242 | 2457 | 57 | 262 | RESPEC | RESPEC | MULTI | 150 | FLAG | SPEC | TEST | BEHAVIOR | 3 | 3 | **PART** | **SPEC** |
| Left Nav | 2991 | 590 | 1955 | 201 | 245 | RESPEC | RESPEC | MULTI | 123 | FLAG | SPEC | TESTABLE | UNDECIDED | 4 | 6 | **PART** | **SPEC** |
| Kit/Options related | 2982 | 170 | 2292 | 216 | 304 | **INV** | RESPEC | ISO | 43 | FLAG | SPEC | TESTABLE | OUTCOME | 3 | 7 | **PART** | **SPEC** |
| Settings | 2507 | 427 | 1776 | 96 | 208 | RESPEC | RESPEC | ISO | 255 | FLAG | SPEC | TESTABLE | OUTCOME | 3 | 7 | -- | **SPEC** |
| Categories | 2138 | 193 | 1127 | 188 | 630 | RESPEC | MECH | MULTI | 123 | FLAG | SPEC | TEST | OUTCOME | 19 | 4 | -- | -- |
| Login | 1606 | 182 | 878 | 279 | 267 | RESPEC | RESPEC | **SPINE** | 255 | CUTOVER | SPEC | TEST | OUTCOME | 3 | 6 | -- | **SPEC** |
| Documents Related | 1300 | 300 | 289 | 353 | 358 | RESPEC | MECH | ISO | 151 | FLAG | CODE_ONLY | TESTABLE | OUTCOME | 4 | 3 | -- | ref |
| RepActivity | 1166 | 65 | 837 | 112 | 152 | RESPEC | MECH | ISO | 7 | FLAG | CODE_ONLY | TESTABLE | OUTCOME | 0 | 0 | -- | -- |
| Custom UI controls | 1024 | 326 | 546 | 60 | 92 | RESPEC | RESPEC | **SPINE** | 255 | CUTOVER | CODE_ONLY | HUMAN | UNDECIDED | 11 | 3 | **PART** | ref |
| ShowroomCart | 1014 | 99 | 788 | 76 | 51 | RPD | RPD | ISO | 2 | FLAG | CODE_ONLY | TEST | UNDECIDED | 0 | 0 | -- | -- |
| Organization chooser | 987 | 195 | 584 | 143 | 65 | MECH | MECH | MULTI | 191 | FLAG | CODE_ONLY | TESTABLE | OUTCOME | 1 | 4 | pat | ref |
| Pricing | 880 | 0 | 762 | 8 | 110 | RESPEC | RESPEC | MULTI | 235 | FLAG | **CONTESTED** | TEST | OUTCOME | 10 | 4 | **PART** | ref |
| Scan Groups | 556 | 25 | 493 | 11 | 27 | RESPEC | RESPEC | ISO | 91 | FLAG | CODE_ONLY | TESTABLE | OUTCOME | 0 | 0 | **PART** | ref |
| Commitments | 510 | 22 | 349 | 20 | 119 | RPD | RPD | ISO | 5 | FLAG | CODE_ONLY | TESTABLE | UNDECIDED | 0 | 0 | -- | -- |
| Flipbook | 510 | 99 | 368 | 3 | 40 | RPD | RPD | ISO | 11 | FLAG | CODE_ONLY | TESTABLE | UNDECIDED | 1 | 0 | -- | ref |
| ActionPopover | 498 | 69 | 341 | 20 | 68 | RESPEC | RESPEC | MULTI | 255 | FLAG | CODE_ONLY | HUMAN | UNDECIDED | 4 | 6 | -- | ref |
| SemanticSearch | 456 | 27 | 251 | 132 | 46 | RPD | RPD | ISO | 13 | FLAG | CODE_ONLY | TESTABLE | UNDECIDED | 2 | 1 | -- | -- |
| Placements | 435 | 53 | 264 | 49 | 69 | RESPEC | MECH | ISO | 41 | FLAG | CODE_ONLY | TESTABLE | OUTCOME | 0 | 0 | -- | ref |
| _Third Party | 357 | 0 | 33 | 278 | 46 | MECH | MECH | ISO | 255 | FLAG | SPEC | TESTABLE | OUTCOME | 3 | 0 | -- | -- |
| Spreadsheet Import | 327 | 103 | 198 | 3 | 23 | UNK | UNK | UNK | UNKNOWN | UNK | CODE_ONLY | TESTABLE | UNDECIDED | 0 | 0 | -- | ref |
| Select List | 292 | 19 | 251 | 5 | 17 | MECH | MECH | MULTI | 255 | FLAG | CODE_ONLY | TESTABLE | OUTCOME | 5 | 4 | -- | ref |
| External code | 205 | 31 | 0 | 153 | 21 | MECH | MECH | ISO | 255 | FLAG | CODE_ONLY | TESTABLE | OUTCOME | 1 | 0 | -- | -- |
| SuperCat Notices | 180 | 23 | 7 | 29 | 121 | MECH | MECH | ISO | 114 | FLAG | SPEC | TESTABLE | OUTCOME | 0 | 0 | -- | **SPEC** |
| Database Migration | 177 | 0 | 32 | 138 | 7 | **INV** | MECH | **SPINE** | 255 | CUTOVER | CODE_ONLY | TESTABLE | OUTCOME | 2 | 3 | -- | -- |
| Query | 160 | 0 | 160 | 0 | 0 | RESPEC | RESPEC | MULTI | 190 | FLAG | **CONTESTED** | TEST | OUTCOME | 0 | 0 | -- | **SPEC** |
| Notifications | 109 | 69 | 28 | 0 | 12 | RESPEC | RESPEC | ISO | UNKNOWN | FLAG | CODE_ONLY | TESTABLE | OUTCOME | 1 | 0 | -- | ref |
| Core Data Support | 43 | 0 | 0 | 36 | 7 | **INV** | MECH | **SPINE** | 255 | CUTOVER | CODE_ONLY | TESTABLE | OUTCOME | 1 | 1 | -- | -- |
| **TOTAL (34 units)** | **86463** | **10228** | **54012** | **6592** | **15631** | | | | | | | | | | | | |


### The two Phase 3 amendments, unit by unit

Units whose `behavior_specification` changed once the component registry was found, and what the spike has already built.

| Unit | LOC | First pass | Amended | Unit files named in registry | Spike lines added | Spike status |
|---|--:|---|---|---|--:|---|
| Order related | 13531 | CODE_ONLY | SPECIFIED | 41 of 142 (28.9%) | 1277 | PARTIALLY_BUILT |
| Global classes | 11302 | CODE_ONLY | SPECIFIED | 27 of 172 (15.7%) | 0 | NOT_STARTED |
| Grid view related | 10461 | CONTESTED | CONTESTED | 50 of 104 (48.1%) | 491 | PARTIALLY_BUILT |
| Reporting and Email Generation | 6548 | CODE_ONLY | SPECIFIED | 19 of 108 (17.6%) | 0 | NOT_STARTED |
| Sync | 3935 | CODE_ONLY | SPECIFIED | 8 of 32 (25.0%) | 0 | NOT_STARTED |
| SingleItemView related | 3303 | CODE_ONLY | SPECIFIED | 7 of 24 (29.2%) | 471 | PARTIALLY_BUILT |
| Customer | 3018 | CODE_ONLY | SPECIFIED | 9 of 27 (33.3%) | 292 | PARTIALLY_BUILT |
| Left Nav | 2991 | CODE_ONLY | SPECIFIED | 18 of 21 (85.7%) | 694 | PARTIALLY_BUILT |
| Kit/Options related | 2982 | CODE_ONLY | SPECIFIED | 14 of 33 (42.4%) | 547 | PARTIALLY_BUILT |
| Settings | 2507 | CODE_ONLY | SPECIFIED | 9 of 25 (36.0%) | 0 | NOT_STARTED |
| Login | 1606 | CODE_ONLY | SPECIFIED | 8 of 17 (47.1%) | 0 | NOT_STARTED |
| Custom UI controls | 1024 | CODE_ONLY | CODE_ONLY | 4 of 20 (20.0%) | 16280 | PARTIALLY_BUILT |
| Organization chooser | 987 | CODE_ONLY | CODE_ONLY | 4 of 7 (57.1%) | 2 | PATTERN_ESTABLISHED |
| Pricing | 880 | CONTESTED | CONTESTED | 1 of 18 (5.6%) | 74 | PARTIALLY_BUILT |
| Scan Groups | 556 | CODE_ONLY | CODE_ONLY | 4 of 5 (80.0%) | 159 | PARTIALLY_BUILT |
| SuperCat Notices | 180 | CODE_ONLY | SPECIFIED | 2 of 6 (33.3%) | 0 | NOT_STARTED |


### Scenario delta, unit by unit

| Unit | LOC | A | B | What changes |
|---|--:|---|---|---|
| Order related | 13531 | INVENTION | RESPECIFICATION | B redesigns a determined behaviour. A additionally requires deciding whether offline submission is permitted at all, against 185 tenants configured to forbid it. |
| Kit/Options related | 2982 | INVENTION | RESPECIFICATION | B evaluates configurations server-side. A must decide how 1.67M matrix rows reach a browser, or that they do not. |
| Categories | 2138 | RESPECIFICATION | MECHANICAL | B transcribes; A must decide local materialisation. |
| Documents Related | 1300 | RESPECIFICATION | MECHANICAL | B serves documents; A must decide the caching policy. |
| RepActivity | 1166 | RESPECIFICATION | MECHANICAL | B is a form and a list; A must queue entries locally. |
| Placements | 435 | RESPECIFICATION | MECHANICAL | B renders a report; A must queue captures offline. |
| Database Migration | 177 | INVENTION | MECHANICAL | The largest single asymmetry in the ledger: B deletes two local persistence stacks and their migration histories; A must reinvent both on an unchosen browser storage engine. |
| Core Data Support | 43 | INVENTION | MECHANICAL | B removes the stack; A must replace it. |


### Units with zero test coverage and majority LOGIC

| Unit | LOC | LOGIC | LOGIC % | Tests | Spec | Accept |
|---|--:|--:|--:|--:|---|---|
| Sync | 3935 | 2540 | 64.5% | 0 | SPECIFIED | TESTABLE_NOT_TESTED |
| SingleItemView related | 3303 | 1840 | 55.7% | 0 | SPECIFIED | HUMAN_JUDGMENT_ONLY |
| Left Nav | 2991 | 1955 | 65.4% | 0 | SPECIFIED | TESTABLE_NOT_TESTED |
| Kit/Options related | 2982 | 2292 | 76.9% | 0 | SPECIFIED | TESTABLE_NOT_TESTED |
| Settings | 2507 | 1776 | 70.8% | 0 | SPECIFIED | TESTABLE_NOT_TESTED |
| RepActivity | 1166 | 837 | 71.8% | 0 | CODE_ONLY | TESTABLE_NOT_TESTED |
| Custom UI controls | 1024 | 546 | 53.3% | 0 | CODE_ONLY | HUMAN_JUDGMENT_ONLY |
| Organization chooser | 987 | 584 | 59.2% | 0 | CODE_ONLY | TESTABLE_NOT_TESTED |
| Scan Groups | 556 | 493 | 88.7% | 0 | CODE_ONLY | TESTABLE_NOT_TESTED |
| Commitments | 510 | 349 | 68.4% | 0 | CODE_ONLY | TESTABLE_NOT_TESTED |
| Flipbook | 510 | 368 | 72.2% | 0 | CODE_ONLY | TESTABLE_NOT_TESTED |
| SemanticSearch | 456 | 251 | 55.0% | 0 | CODE_ONLY | TESTABLE_NOT_TESTED |
| Placements | 435 | 264 | 60.7% | 0 | CODE_ONLY | TESTABLE_NOT_TESTED |
| Spreadsheet Import | 327 | 198 | 60.6% | 0 | CODE_ONLY | TESTABLE_NOT_TESTED |
| Select List | 292 | 251 | 86.0% | 0 | CODE_ONLY | TESTABLE_NOT_TESTED |

15 units, 14544 LOGIC LOC, 21981 total LOC.


### Hazards carried, by unit

| Unit | Hazards |
|---|---|
| Order related | camera_barcode_scanning:POLYFILLABLE, core_data_local_persistence:REQUIRES_PRODUCT_DECISION, device_orientation:REQUIRES_PRODUCT_DECISION, fmdb_sqlite_direct:POLYFILLABLE, mailcompose_native_share:POLYFILLABLE, popover_presentation:REQUIRES_PRODUCT_DECISION, webview_bridge:NATIVE_EQUIVALENT |
| Global classes | core_data_local_persistence:REQUIRES_PRODUCT_DECISION, device_orientation:REQUIRES_PRODUCT_DECISION, firebase_crashlytics_analytics:NATIVE_EQUIVALENT, fmdb_sqlite_direct:POLYFILLABLE, local_filesystem:REQUIRES_PRODUCT_DECISION, mixpanel_telemetry:NATIVE_EQUIVALENT, pdf_generation_or_render:POLYFILLABLE, popover_presentation:REQUIRES_PRODUCT_DECISION, printing:POLYFILLABLE, push_local_notifications:POLYFILLABLE, split_view_ipad_multitasking:REQUIRES_PRODUCT_DECISION, webview_bridge:NATIVE_EQUIVALENT |
| Data objects | core_data_local_persistence:REQUIRES_PRODUCT_DECISION, fmdb_sqlite_direct:POLYFILLABLE, local_filesystem:REQUIRES_PRODUCT_DECISION |
| Grid view related | fmdb_sqlite_direct:POLYFILLABLE, local_filesystem:REQUIRES_PRODUCT_DECISION, mailcompose_native_share:POLYFILLABLE, pdf_generation_or_render:POLYFILLABLE, popover_presentation:REQUIRES_PRODUCT_DECISION, printing:POLYFILLABLE, split_view_ipad_multitasking:REQUIRES_PRODUCT_DECISION |
| Reporting and Email Generation | camera_barcode_scanning:POLYFILLABLE, mailcompose_native_share:POLYFILLABLE, printing:POLYFILLABLE |
| Sync | local_filesystem:REQUIRES_PRODUCT_DECISION, zip_archive:POLYFILLABLE |
| SingleItemView related | popover_presentation:REQUIRES_PRODUCT_DECISION |
| Customer | core_data_local_persistence:REQUIRES_PRODUCT_DECISION, fmdb_sqlite_direct:POLYFILLABLE |
| Kit/Options related | core_data_local_persistence:REQUIRES_PRODUCT_DECISION, popover_presentation:REQUIRES_PRODUCT_DECISION |
| Settings | fmdb_sqlite_direct:POLYFILLABLE |
| Categories | core_data_local_persistence:REQUIRES_PRODUCT_DECISION, fmdb_sqlite_direct:POLYFILLABLE, local_filesystem:REQUIRES_PRODUCT_DECISION, popover_presentation:REQUIRES_PRODUCT_DECISION |
| Login | biometric_auth:POLYFILLABLE, keychain:POLYFILLABLE, local_filesystem:REQUIRES_PRODUCT_DECISION |
| Documents Related | local_filesystem:REQUIRES_PRODUCT_DECISION, mailcompose_native_share:POLYFILLABLE, pdf_generation_or_render:POLYFILLABLE, webview_bridge:NATIVE_EQUIVALENT |
| ShowroomCart | popover_presentation:REQUIRES_PRODUCT_DECISION, split_view_ipad_multitasking:REQUIRES_PRODUCT_DECISION |
| Organization chooser | webview_bridge:NATIVE_EQUIVALENT |
| Flipbook | pdf_generation_or_render:POLYFILLABLE, popover_presentation:REQUIRES_PRODUCT_DECISION |
| SemanticSearch | fmdb_sqlite_direct:POLYFILLABLE |
| External code | device_orientation:REQUIRES_PRODUCT_DECISION, pdf_generation_or_render:POLYFILLABLE |
| SuperCat Notices | webview_bridge:NATIVE_EQUIVALENT |
| Database Migration | local_filesystem:REQUIRES_PRODUCT_DECISION |

**Legend.** A/B = `port_class` under each scenario. `MECH` MECHANICAL, `RESPEC`
RESPECIFICATION, `INV` INVENTION, `RPD` REQUIRES_PRODUCT_DECISION, `UNK` UNKNOWN.
Blast: `ISO` ISOLATED, `MULTI` MULTI_SURFACE. Rev: `FLAG` FLAGGABLE, `CUTOVER`
CUTOVER_ONLY. Spec: `SPEC` SPECIFIED. Accept: `TEST` TEST_EXISTS, `TESTABLE`
TESTABLE_NOT_TESTED, `HUMAN` HUMAN_JUDGMENT_ONLY. Fidelity: `OUTCOME`
OUTCOME_EQUIVALENT, `BEHAVIOR` BEHAVIOR_PARITY, `PIXEL` PIXEL_PARITY. `in`/`out`
= `coupling_fan_in`/`coupling_fan_out`. Spike: `PART` PARTIALLY_BUILT, `pat`
PATTERN_ESTABLISHED, `--` NOT_STARTED. Reg: `SPEC` DEDICATED_SPEC, `ref`
REFERENCED, `--` NONE. Full rationale for every row, including the evidence
behind each `tenants_touched`, is in `03_UNIT_LEDGER.json`.

**LOC reconciliation note.** The TOTAL row shows 54,012 LOGIC and 15,631
UNCLASSIFIED against Phase 1.2 totals of 54,023 and 15,767. The differences are
exactly the excluded infrastructure pseudo-units: `_SuperCatTest` contributes 11
LOGIC, and `_Other Sources` (129) plus `_UNMAPPED` (7) contribute 136
UNCLASSIFIED. 54,012 + 11 = 54,023 and 15,631 + 136 = 15,767.

---

## Three measurement limits that bound this ledger

**Coupling is blind to Swift.** `coupling_fan_in` and `coupling_fan_out` are
resolved from `#import "Foo.h"` against the file→unit map. Swift sibling types
inside one module need no import statement, so a Swift-only unit scores 0/0 by
construction. Every unit reporting 0/0 — `RepActivity`, `ShowroomCart`,
`Scan Groups`, `Commitments`, `Placements`, `Spreadsheet Import`,
`SuperCat Notices`, `Query` — is **100% Swift**. Those zeros are measurement
blindness, not evidence of isolation, and each row carries
`coupling_confidence: UNKNOWN_SWIFT_OPAQUE`. Two further units are
`PARTIAL_SWIFT_OPAQUE` (`Reporting and Email Generation` at 87.8% Swift,
`Customer` at 53.8%), so their measured coupling is a lower bound.

**Registry coverage is a lower bound too.** Per-unit coverage was measured by
resolving iOS source basenames named in the registry through the file→unit map.
The registry documents *components* narratively and does not exhaustively name
every file, so `registry_pct_unit_files_documented` understates behavioural
coverage. It is reported because the spread is what matters: 85.7% for `Left Nav`
versus 5.6% for `Pricing` means those two units are not equally specified even
though both sit above `NONE`.

**LOC understates two units severely.** `Database Migration` is 177 LOC of driver
code that executes 63 SQLite migration files totalling 1,577 SQL lines and
creating 47 tables, alongside a Core Data model with 19 versions and 18
inter-version migrations. `Core Data Support` is 43 LOC that anchors 221 Core Data
call sites across 49 files. For these two, LOC is the wrong quantity and the
migration-file and call-site counts are the real ones. Both are flagged in their
rationale.

---

## The riskiest rows, by construction

Fifteen units have **zero test files referencing them and majority-LOGIC
content** — 14,544 LOGIC LOC across 21,981 total LOC. Business logic with no
acceptance anchor is where a naive reimplementation produces a wrong business
answer that nothing catches. Note that the registry does **not** reduce this
number: documentation is not an executable check.

Three deserve naming:

- **`Sync` (3,935 LOC, 64.5% LOGIC, 0 tests).** INVENTION in *both* scenarios.
  Phase 1.4 found zero conflict-resolution branches in the code, and
  `_sync-protocol.yaml` independently confirms the design is one-way and
  server-authoritative. Scenario A cannot transcribe a conflict resolver that
  does not exist. Scenario B still must invent a freshness and invalidation
  policy for the 22 server-versioned entity types. Classifying this
  RESPECIFICATION is the specific error the brief warns against, and two
  independent sources now say INVENTION.
- **`Kit/Options related` (2,982 LOC, 76.9% LOGIC, 0 tests).** The CPQ engine.
  Concentrated rather than broad: `order_configured_item` reaches 43 tenants but
  fires 134,377 times. Scenario A is INVENTION on scale grounds — `matrix_options`
  reaches 1,669,094 rows for tenant `5` and 770,494 for tenant `109`.
- **`Pricing` (880 LOC, 86.6% LOGIC, zero UI, 8 tests).** The purest business
  logic in the codebase, and the least documented of the large logic units: the
  registry names 1 of its 18 files. CONTESTED, with tenant configurations
  diverging sharply — 235 tenants with price levels up to 326, 53 with matrix
  pricing, 19 with contract prices, 52 with surcharges.

Note the asymmetry, and note what it is *not* used for. Test references per unit
run from 22 (`Global classes`) down to 0, and they are inversely related to stakes
in at least one place: `Pricing`, 880 LOC, has 8 referencing test files, while
`Sync`, 3,935 LOC and the most consequential unit in the ledger, has 0. That
comparison is a statement about how safely each unit can be reimplemented and
verified. It is not an effort signal, and no axis in this ledger is derived from
test counts.

---

## SELF-AUDIT

**Does any output contain a time unit, or a scale that implies one?**
No. Every quantity here is a count (units, LOC, files, methods, tenants, call
sites, migration files, test files, registry lines, spike lines, fan-in/fan-out)
or a level on a categorical axis defined without reference to time. Axis
vocabularies, including the two new fields, are in
`03_UNIT_LEDGER.json → axis_definitions_used`. Two deliberate omissions:
`docs/design/ecat-web-spike.md` states a team size and a timebox for the spike,
and `docs/superpowers/specs/2026-08-01-ecat-a12-performance-results.md` states
p95 latency budgets. **Neither figure is carried into this document.** The
timebox is disclosed rather than quoted because a reader of Phase 6 needs to know
it exists and that it was not used as an anchor.

**Does every factual row have a `source`?**
Yes. All 68 rows carry a `source` naming the six contributing artifacts
(`01_CODE_CENSUS.json` §1.2 and §1.7, `scripts/coupling.json`,
`scripts/swiftshare.json`, `02_TENANT_CENSUS.json`, `scripts/spike.json`,
`scripts/registry.json`), and every `tenants_touched` carries a separate
`tenants_touched_basis`. The two new fields carry their own provenance:
`registry_dedicated_docs` names the specific YAML files, and `spike_lines_added`
is a `git diff --numstat` figure. No rows were deleted for missing provenance.

**Did I report distributions where tenants differ, or did I average?**
No averaging. `tenants_touched` is a count of tenants, and where reach is
concentrated the rationale gives both the tenant count and the event volume so
the two cannot be confused (`Kit/Options related`: 43 tenants, 134,377 events).
Where scale drives a classification the outlier tenants are named individually
(`5`, `109`). Registry coverage is likewise reported per unit, with the 85.7%
versus 5.6% spread stated rather than collapsed to a mean.

**Did I mark anything MECHANICAL that actually depends on an unmade decision?**
Re-checked, and re-checked again after Amendment 2, because a newly discovered
specification is exactly the kind of evidence that tempts an upgrade to
MECHANICAL. No unit was reclassified on the strength of the registry. The reason
is definitional: MECHANICAL requires the target behaviour to be transcribable
against a *known web equivalent*, and a document describing iPad behaviour does
not supply a web equivalent. MECHANICAL remains the smallest bucket — 5 units
and 2,021 LOC under A, 11 units and 7,280 LOC under B. Three candidates were
deliberately not marked MECHANICAL: `Notifications` (web push needs a permission
grant, a service worker, and on iOS Safari home-screen installation, so delivery
is not equivalent), `ActionPopover` (what replaces a popover on a narrow viewport
is a design decision), and `Scan Groups` (symbologies are tenant-configured via
`supported_camera_scan_symbologies`). Four units were escalated to
`REQUIRES_PRODUCT_DECISION` rather than classified at all, because a keep/kill
decision precedes any port classification: `ShowroomCart` (2 tenants),
`Commitments` (5), `Flipbook` (11), `SemanticSearch` (13).

**Did I fill any field with a plausible guess rather than UNKNOWN?**
No. `Spreadsheet Import` keeps `port_class`, `blast_radius`, `reversibility` and
`tenants_touched` as UNKNOWN — no telemetry event and no Postgres table maps to
it. `Notifications` keeps `tenants_touched: UNKNOWN`, with an explicit note that
`view_notifications` (114 tenants) belongs to `SuperCat Notices`. 11 units keep
`fidelity_bar: UNDECIDED` even though the spike's "full UX redesign" decision
narrows the range, because narrowing is not deciding. All are escalated to
Phase 4.

**Did I run tooling, or did I read and approximate?**
Tooling throughout, and the tooling caught both amendments. The LOC partition
assertion in `scripts/p3_ledger.py` failed on its first run over a missing
109-LOC unit (`Notifications`), which was added; it now reconciles exactly. The
specification amendment was produced by `scripts/p3_registry.py`, which resolves
registry file references through the same file→unit map used in Phase 1 rather
than by my reading the YAML and judging coverage; the script also prints the 11
amended units by name so the diff is visible. `scripts/p3_spike.py` measures the
spike by `git diff --numstat` with an explicit, file-by-file auditable path→unit
table. What remains judgement is the classification itself, which is why every
row carries a `rationale` that can be contested individually.

**New question, added because the first pass failed it: did I search for
specifications outside the repository under analysis?**
The first pass did not, and asserted CODE_ONLY for 61,512 LOC as a result. The
specification of the iOS app was in the server repository the whole time. The
remaining exposure is that Linear and Notion were never probed (recorded as a
Phase 0 gap and still open), so tickets and product docs held there could further
reduce the CODE_ONLY population of 9,609 LOC. This is carried into Phase 4 as an
evidence gap rather than left implicit.
