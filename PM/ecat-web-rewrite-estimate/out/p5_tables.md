### A. UNREACHABLE — no inbound navigation edge, no tenant conversation

| Screen | Unit | LOC | IB document | Evidence |
|---|---|--:|---|---|
| `OrderItemTagGroupSelectionViewController` | Order related | 47 | none | zero inbound navigation edges |
| `EditReportTitlesViewController` | Reporting and Email Generation | 32 | none | zero inbound navigation edges |
| `SettingsAboutController` | Settings | 15 | none | zero inbound navigation edges |
| `OrderItemActionMenuViewController` | Global classes | 10 | OrderItems.storyboard | zero inbound navigation edges |
| `FullScreenViewController` | (unmapped) | 0 | FullScreen.xib | zero inbound navigation edges |

**Total LOC that would not be rewritten: 104.**


### B. Compiled but referenced only by its own header/impl pair

| Class | Unit | Header LOC | Impl LOC |
|---|---|--:|--:|
| `BuildsSearchAndFilterPanel` | Left Nav | 3 | 41 |
| `SceneDelegate` | Global classes | 4 | 47 |
| `SelectProductFilterViewController` | Grid view related | 3 | 119 |
| `SettingsAboutController` | Settings | 3 | 12 |
| `SwitchableNavigationController` | Global classes | 3 | 25 |
| `SwitchableSplitViewController` | Global classes | 3 | 27 |

**Total: 290 LOC across 6 classes.**


### C. On disk but not in the Xcode project — not compiled at all

| File |
|---|
| `Classes/Functional.swift` |
| `Classes/SurchargeType.swift` |
| `Classes/SurchargeValue.swift` |


### D. Orphan Interface Builder documents

| Document | Custom classes bound | Note |
|---|---|---|
| `DetailView.xib` | — | no customClass bindings at all |
| `FullScreen.xib` | `FullScreenViewController`, `UIResponder` |  |
| `Launch Screen.storyboard` | — | no customClass bindings at all |
| `NoneCell.xib` | `UIResponder` |  |
| `OrderOptionsCell.xib` | — | no customClass bindings at all |
| `OrderTableHeader.xib` | — | no customClass bindings at all |
| `SettingsPriceLevelController.xib` | — | no customClass bindings at all |
| `StandardToolbar.xib` | — | no customClass bindings at all |

8 of 95 Interface Builder documents.


### E. LOW_USE — ranked by removal candidacy

Ranked on two measured quantities together: how many production tenants touch the unit, and how much they actually do with it. Depth matters as much as breadth -- a unit reaching 12 tenants that fired 74 times in a year is a weaker attachment than one reaching 2 that fired 2,242 times.

| Rank | Unit | LOC | LOGIC | Prod tenants | Non-prod | Events (12mo) | Most recent use | Reach basis | Registry | Tests |
|--:|---|--:|--:|--:|--:|--:|---|---|---|--:|
| 1 | SemanticSearch | 456 | 251 | 12 | 1 | 74 | 2026-05-19 | telemetry | **none** | 0 |
| 2 | ShowroomCart | 1014 | 788 | 2 | — | not instrumented | UNKNOWN | Postgres table | **none** | 1 |
| 3 | Commitments | 510 | 349 | 2 | 2 | 2242 | 2026-07-27 | telemetry | **none** | 0 |
| 4 | RepActivity | 1166 | 837 | 7 | — | not instrumented | UNKNOWN | Postgres table | **none** | 0 |
| 5 | Spreadsheet Import | 327 | 198 | UNKNOWN | — | not instrumented | UNKNOWN | Postgres table | ref | 0 |
| 6 | Flipbook | 510 | 368 | 10 | 1 | 6053 | 2026-08-07 | telemetry | ref | 0 |
| 7 | Placements | 435 | 264 | 31 | 3 | 6855 | 2026-08-07 | telemetry | ref | 0 |
| — | Kit/Options related | 2982 | 2292 | 38 | 4 | 236343 | 2026-08-07 | telemetry | SPEC | 0 |

**Ranked LOW_USE total: 4418 LOC, 3055 of it LOGIC, across 7 units.** The final row is included for contrast and is **not** a candidate: `Kit/Options related` reaches a comparable number of tenants but fired 236,343 times.


### F. Named tenants, per low-use unit

**SemanticSearch** — 456 LOC, 0 test files
- Production tenants (12): `clc`, `cst`, `da`, `gc`, `gh`, `kii`, `mh`, `pf`, `sc`, `scw`, `uhc`, `wag`
- Non-production (1): `demo2`

**Commitments** — 510 LOC, 0 test files
- Production tenants (2): `mh`, `ufi`
- Non-production (2): `demo`, `demo2`

**Flipbook** — 510 LOC, 0 test files
- Production tenants (10): `clli`, `eglo`, `eglo_can`, `fms`, `jyc`, `tla`, `vcg`, `vcgcon`, `wag`, `yw`
- Non-production (1): `demo2`

**Placements** — 435 LOC, 0 test files
- Production tenants (31): `afx`, `ali`, `all`, `arl`, `bp`, `bri`, `cci`, `clli`, `clm`, `cst`, `df`, `el`, `fal`, `fms`, `gc`, `gcl`, `gl`, `kal`, `kl`, `luc`, `mh`, `mlc`, `mlg`, `mli`, `prog`, `sbl`, `tla`, `ufi`, `vcg`, `vcgcon`, `wac`
- Non-production (3): `demo`, `demo2`, `demo3`

**Kit/Options related** — 2982 LOC, 0 test files
- Production tenants (38): `ah`, `all`, `am`, `ap`, `bcf`, `big`, `cfg`, `cst`, `fal`, `fsf`, `gcl`, `gh`, `gl`, `hfg`, `hun`, `ihm`, `ihw`, `jc`, `kkc`, `kll`, `mali`, `mh`, `ol`, `pebl`, `pf`, `rf`, `ril`, `rw`, `sbmh`, `sc`, `sccon`, `scw`, `sp`, `ta`, `tam`, `tcs`, `wag`, `yw`
- Non-production (4): `demo2`, `demo3`, `pf_test`, `test1`

