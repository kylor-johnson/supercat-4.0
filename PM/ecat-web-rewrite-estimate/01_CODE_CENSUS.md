# 01_CODE_CENSUS.md — eCat iPad codebase census

**Machine-readable companion:** `01_CODE_CENSUS.json` (375 KB, every row with `source`).
**Scripts (all deterministic, re-runnable):** `scripts/p1_units.py`, `p1_loc_split.py`,
`p1_diag.py`, `p1_surface.py`, `p1_rest.py`, `p1_assemble.py`.

**Pins:** iOS `129242b0e27401b9019f805066f1b8ea88da5380`; server `bd7895a7e`.
Analysis ran in detached worktrees under `/tmp/ecat-audit/`; user checkouts untouched.

---

## CORRECTION issued during Phase 3 — read this first

**A specification of the iPad app exists and this census missed it.**
`docs/design/ecat-component-registry/` on `supercat_server` `origin/master` is a
22-file, 19,329-line structured specification of the eCat iPad application, dated
2026-04-03, documenting 84 components, 5 workflows, 40 SQLite tables, 4 Core Data
entities and 236 configuration settings — including a 517-line
`_sync-protocol.yaml`.

**Why it was missed:** §1.7 searched the **iOS** repository for docs, tests and
tickets. The iOS app's specification lives in the **server** repository. The
search scope, not the tooling, was wrong.

**What it changes:** Phase 3's `behavior_specification` axis. The first Phase 3
pass, inheriting this census, classified 28 units / 61,512 LOC as `CODE_ONLY`
("behaviour exists nowhere but the implementation"). Measured against the
registry, the figure is **17 units / 9,609 LOC**. See
`03_UNIT_LEDGER.md → Amendment 2` and `scripts/p3_registry.py` for the per-unit
measurement.

**What it does not change:** every count in this document. LOC, screens,
entities, endpoints, hazards, call sites, tests and complexity were measured from
the iOS source and are unaffected. In particular §0.1 below — that there is no
conflict-resolution engine to port — is *confirmed* by the registry, which
describes a one-way, server-authoritative protocol with no conflict, merge or
tombstone semantics in 517 lines.

**Still-open exposure:** Linear and Notion were never probed (Phase 0 §6 gap).
Further specification may exist there.

---

## 0. Three findings that change the analysis

Stated first because each one invalidates a natural assumption.

### 0.1 There is no conflict-resolution engine to port

The brief warned against classifying the sync engine as `RESPECIFICATION` when it is
`INVENTION`. The evidence is stronger than that: **there is nothing to respecify.**

Across all 964 source files in `Classes/`, ripgrep finds **zero** occurrences of
`conflict`, `lastwritewins`, `last_write`, `tombstone`, `etag`, `if-modified-since`,
or `vector clock`. No `NSMergePolicy` is ever declared (the string appears in
`DataStore.m` only). Method names in `Synchronizer.m` (1,842 lines) describe a
**purge-and-replace** pipeline, not a merge:

```
calculateSyncNecessity   isUpdateAvailable:      getModifiedEntitiesForDate:
performPurge             shouldPurge:            buildPurgeInfo
resetDatabaseState       clearData               commitData
executeBackupOrRestoreOfUserCreatedData
```

Server data is authoritative and replaced wholesale, with a modified-date delta
check. Locally-created data survives the wipe by being **backed up and restored
around it** (`executeBackupOrRestoreOfUserCreatedData`), then uploaded by the
`Transfers*` family. So:

- `conflict_resolution_branches`: **0**
- `lww_paths`: **0**
- `merge_resolved_paths`: **0**

Consequence: Scenario A cannot be scoped as "port the existing offline engine."
The existing design depends on a native app's ability to hold a private on-disk
database and perform a controlled destroy-and-rebuild. Reproducing that in a
browser is not transcription. **This is `INVENTION` and it goes to Phase 4.**

### 0.2 Local persistence is two stacks with two migration histories

The Core Data model has 19 versions, but the current one — declared in
`.xccurrentversion`, **not** the last one alphabetically — is `eCat 20260425`, and
it contains **3 entities**: `Order`, `OrderItem`, `OrderItemOption`.

The version trajectory shows exactly when this happened:

| Core Data version | entities | attributes | relationships |
|---|---|---|---|
| eCat 20130326 | 25 | 215 | 18 |
| eCat 20150227 | 25 | 223 | 18 |
| **eCat 20150407** | **3** | **72** | **4** |
| eCat 20240722 | 3 | 83 | 5 |
| **eCat 20260425** (current) | **3** | **86** | **5** |
| eCat (base, not current) | 25 | 214 | 16 |

At version `20150407` the catalog left Core Data. It now lives in **raw SQLite via
FMDB**, with its own migration history in `eCatalog/Database/`:

| SQLite stack (catalog) | Count |
|---|---|
| Migration files | 63 |
| SQL lines | 1,577 |
| Tables created across migrations | 47 |
| Views created across migrations | 3 |
| FMDB / `sqlite3_` call sites | 151 across 34 files |

So a rewrite replaces **two** persistence layers, **two** schemas (3 Core Data
entities + 47 SQLite tables), and **two** migration chains (18 + 62). Reading only
`eCat.xcdatamodeld` — as my own Phase 0 plan did, reporting "25 entities" — gets
this wrong. **Phase 0 §1.3 is corrected by this section.**

### 0.3 The headline UI/LOGIC ratio is rule-sensitive, and the real number is entanglement

Under the approved rule the split is decisive; under the opposite precedence it
nearly inverts:

| Bucket | Approved (LOGIC-first) | Sensitivity (UI-first) |
|---|---|---|
| UI | 10,228 (11.8%) | 33,653 (38.9%) |
| LOGIC | 54,023 (62.4%) | 32,065 (37.0%) |
| GLUE | 6,592 (7.6%) | 5,129 (5.9%) |
| UNCLASSIFIED | 15,767 (18.2%) | 15,763 (18.2%) |

Neither is "the" answer. The number that survives both rules is the overlap:
**18,929 code lines (25.7% of all in-method LOC) match business-domain terms AND
UIKit presentation terms in the same method.** Business logic is not in a service
layer being displayed by views; it is interleaved with presentation.

Full co-occurrence, by code lines inside method bodies (73,639 total):

| logic | ui | glue | LOC | % |
|---|---|---|---|---|
| yes | no | no | 22,194 | 30.1% |
| yes | **yes** | no | 12,863 | 17.5% |
| no | no | no | 10,415 | 14.1% |
| no | yes | no | 9,266 | 12.6% |
| yes | no | yes | 7,255 | 9.9% |
| yes | **yes** | yes | 6,066 | 8.2% |
| no | no | yes | 4,293 | 5.8% |
| no | yes | yes | 1,287 | 1.7% |

Logic-only 29,449 · UI-only 10,553 · **entangled 18,929**.

Corroborating count from an independent path: the 105 screens hold **29,041 LOC,
of which 19,473 classify as LOGIC**. Two thirds of the code inside view
controllers is domain behavior.

---

## 1.1 Surface inventory

105 screens, from three unioned sources (declared Objective-C classes, declared
Swift classes, IB documents with a `customClass` binding).

| Metric | Count |
|---|---|
| Screens total | 105 |
| Declared in Objective-C | 52 |
| Declared in Swift | 51 |
| IB-only (no source class found) | 2 |
| IB documents (`.storyboard` + `.xib`) | 95 |
| Storyboard/relationship/root nav edges | 112 |
| Programmatic nav edges | 85 |
| Storyboard initial view controllers (entry points) | 14 |
| `REACHABLE` | 86 |
| `ENTRY_POINT` | 14 |
| **`UNREACHABLE_CANDIDATE`** | **5** |
| Screens with an IB document | 75 |
| Screens with no IB document (programmatic UI) | 30 |
| LOC held in screens | 29,041 |
| …of which LOGIC | 19,473 |

**Navigation-edge method.** Storyboard edges come from parsing each IB document's
XML and resolving `<segue destination=...>` element ids to the owning scene's
controller class. Programmatic edges use a deliberately over-connecting rule: in
any method body containing a navigation verb (`pushViewController`,
`presentViewController`, `showDetailViewController`, `setViewControllers`,
`instantiateViewController`, `performSegue`, `addChildViewController`), every other
known screen class named in that body becomes an out-edge. Over-connecting means
`UNREACHABLE_CANDIDATE` is a **conservative** claim — a screen flagged unreachable
survived a generous inbound search.

### The 5 unreachable candidates

| Screen | Unit | LOC | IB document |
|---|---|---|---|
| `OrderItemTagGroupSelectionViewController` | Order related | 47 | — |
| `EditReportTitlesViewController` | Reporting and Email Generation | 32 | — |
| `SettingsAboutController` | Settings | 15 | — |
| `OrderItemActionMenuViewController` | Global classes | 10 | `OrderItems.storyboard` |
| `FullScreenViewController` | (unmapped) | 0 | `FullScreen.xib` |

Total 104 LOC. These are small; the kill list's value will come from Phase 2 usage,
not from reachability.

### Largest screens

| Screen | Unit | LOC | in | out | reachability |
|---|---|---|---|---|---|
| `CatalogViewController` | Grid view related | 2,714 | 2 | 5 | REACHABLE |
| `OrderItemsViewController` | Order related | 2,084 | 0 | 9 | ENTRY_POINT |
| `OrderPreviewViewController` | Order related | 1,521 | 0 | 2 | ENTRY_POINT |
| `SingleItemViewController` | SingleItemView related | 1,226 | 0 | 3 | ENTRY_POINT |
| `CreateOrEditCustomerViewController` | Customer | 1,110 | 2 | 1 | REACHABLE |
| `CustomerNavViewController` | Left Nav | 896 | 1 | 3 | REACHABLE |
| `TradenamesCollectionsViewController` | Grid view related | 853 | 2 | 1 | REACHABLE |
| `OrderListViewController` | Customer | 818 | 1 | 1 | REACHABLE |
| `TopLevelLeftNavViewController` | Left Nav | 764 | 1 | 12 | REACHABLE |
| `MainViewController` | Global classes | 755 | 0 | 7 | ENTRY_POINT |

`TopLevelLeftNavViewController` has out-degree 12 — the highest fan-out in the app
and a structural hub. Per-screen rows for all 105 are in the JSON.

---

## 1.2 The three-way LOC split

### Unit boundaries

Per the approved methodology, units are Xcode `PBXGroup` entries, because
`Classes/` is flat on disk (1,039 of 1,062 files at one level).

| Metric | Count |
|---|---|
| PBXGroups parsed | 59 |
| Units derived | 43 (36 under `Classes/`, 7 outside, prefixed `_`) |
| File references placed | 1,409 |
| Unresolved child references | 1 |
| Source files on disk in `Classes/` | 964 |
| On disk but absent from the project | 3 |

### Reconciliation against `scc`

My classifier counts **86,610** code lines. `scc --no-cocomo` on the same tree
reports **86,865**. Gap **255 lines (0.3%)**, attributable to differing
blank/comment handling and one 20-line plain-text file `scc` includes. Reported
rather than reconciled away.

### The rule as applied

Per method, precedence **LOGIC > GLUE > UI**, `UNCLASSIFIED` as its own bucket.
Storyboard/XIB XML is counted **separately** as `IB_XML` (95 files, 19,246 XML
lines) and never folded into `ui_loc`.

**Two documented refinements to the Phase 0 rule**, both published in
`01_CODE_CENSUS.json → 1_2_loc_split.classification_rule`:

1. **LOGIC is two-tiered.** Tier 1 is domain-computation identifiers
   (`extendedPrice`, `explodeKit`, `qtyAvailable`, `optionMapping`, …) and matches
   unconditionally. Tier 2 is bare Core Data entity nouns (`Customer`, `Order`) and
   matches **only** if the method also contains an arithmetic, comparison,
   aggregation, or predicate token. Reason: bare entity nouns saturate pure
   presentation code (`CustomerCell`, `OrderTableHeader`); tier-1-only matching
   would have absorbed cell-rendering methods into LOGIC, and under LOGIC
   precedence that error is unrecoverable.
2. **A structural GLUE fallback.** A method matching no term family, whose name is
   `init*`/`dealloc`/`deinit`/`copyWithZone`/`encodeWithCoder`/`description`/
   `hash`/`isEqual`, is GLUE. Object construction is platform plumbing.

Term lists were extended once, after a diagnostic pass, for symbols that were
simply absent (`awakeFromNib`, `preferredStatusBarStyle` → UI;
`observeValueForKeyPath`, `entityName`, `availableMigrations`, `WKWebView` → GLUE).
Both the pre- and post-extension totals were inspected; the rule was then frozen.
It was **not** iterated toward a pleasing number.

### Accounting transparency

| Quantity | Value |
|---|---|
| Code lines inside method bodies | 73,639 |
| Residue (imports, ivars, `@property`, type decls) assigned to each file's dominant class | 12,971 |
| Files containing more than one class of method | 470 |
| `UNCLASSIFIED`, trivial (methods ≤3 LOC — accessors) | 3,575 LOC in 1,267 methods |
| `UNCLASSIFIED`, substantive (methods >3 LOC) | 6,277 LOC in 875 methods |
| `UNCLASSIFIED`, residue in files with no classified method | remainder |

The 6,277 substantive unclassified lines are the honest floor on this method's
resolution.

### Per-unit split

| Unit | total | UI | LOGIC | GLUE | UNCL | %logic |
|---|---|---|---|---|---|---|
| Order related | 13,531 | 1,358 | 9,902 | 530 | 1,741 | 73.2 |
| Global classes | 11,302 | 1,508 | 6,071 | 992 | 2,731 | 53.7 |
| Data objects | 10,955 | 25 | 6,919 | 491 | 3,520 | 63.2 |
| Grid view related | 10,461 | 1,642 | 6,451 | 572 | 1,796 | 61.7 |
| Reporting and Email Generation | 6,548 | 1,567 | 3,223 | 321 | 1,437 | 49.2 |
| Sync | 3,935 | 149 | 2,540 | 741 | 505 | 64.5 |
| SingleItemView related | 3,303 | 650 | 1,840 | 279 | 534 | 55.7 |
| Customer | 3,018 | 242 | 2,457 | 57 | 262 | 81.4 |
| Left Nav | 2,991 | 590 | 1,955 | 201 | 245 | 65.4 |
| Kit/Options related | 2,982 | 170 | 2,292 | 216 | 304 | 76.9 |
| Settings | 2,507 | 427 | 1,776 | 96 | 208 | 70.8 |
| Categories | 2,138 | 193 | 1,127 | 188 | 630 | 52.7 |
| Login | 1,606 | 182 | 878 | 279 | 267 | 54.7 |
| Documents Related | 1,300 | 300 | 289 | 353 | 358 | 22.2 |
| RepActivity | 1,166 | 65 | 837 | 112 | 152 | 71.8 |
| Custom UI controls | 1,024 | 326 | 546 | 60 | 92 | 53.3 |
| ShowroomCart | 1,014 | 99 | 788 | 76 | 51 | 77.7 |
| Organization chooser | 987 | 195 | 584 | 143 | 65 | 59.2 |
| Pricing | 880 | 0 | 762 | 8 | 110 | 86.6 |
| Scan Groups | 556 | 25 | 493 | 11 | 27 | 88.7 |
| Commitments | 510 | 22 | 349 | 20 | 119 | 68.4 |
| Flipbook | 510 | 99 | 368 | 3 | 40 | 72.2 |
| ActionPopover | 498 | 69 | 341 | 20 | 68 | 68.5 |
| SemanticSearch | 456 | 27 | 251 | 132 | 46 | 55.0 |
| Placements | 435 | 53 | 264 | 49 | 69 | 60.7 |
| Spreadsheet Import | 327 | 103 | 198 | 3 | 23 | 60.6 |
| Select List | 292 | 19 | 251 | 5 | 17 | 86.0 |
| SuperCat Notices | 180 | 23 | 7 | 29 | 121 | 3.9 |
| Database Migration | 177 | 0 | 32 | 138 | 7 | 18.1 |
| Query | 160 | 0 | 160 | 0 | 0 | 100.0 |
| Notifications | 109 | 69 | 28 | 0 | 12 | 25.7 |
| Core Data Support | 43 | 0 | 0 | 36 | 7 | 0.0 |
| _Third Party | 357 | 0 | 33 | 278 | 46 | 9.2 |
| External code | 205 | 31 | 0 | 153 | 21 | 0.0 |

### Language mix per unit — a migration-progress signal

Objective-C 56,385 · Swift 25,248 · C headers 4,977. Per unit, the Swift share
indicates which areas have been rewritten recently in-place:

| Unit | total | ObjC | Swift | headers | Swift % |
|---|---|---|---|---|---|
| RepActivity | 1,166 | 0 | 1,166 | 0 | 100% |
| ShowroomCart | 1,014 | 0 | 1,014 | 0 | 100% |
| Commitments | 510 | 0 | 510 | 0 | 100% |
| Placements | 435 | 0 | 435 | 0 | 100% |
| Scan Groups | 556 | 0 | 556 | 0 | 100% |
| Spreadsheet Import | 327 | 0 | 327 | 0 | 100% |
| Reporting and Email Generation | 6,548 | 760 | 5,752 | 36 | 88% |
| Customer | 3,018 | 1,348 | 1,624 | 46 | 54% |
| Order related | 13,531 | 8,630 | 4,379 | 522 | 32% |
| Grid view related | 10,461 | 7,494 | 2,575 | 392 | 25% |
| Global classes | 11,302 | 8,555 | 1,656 | 1,091 | 15% |
| Data objects | 10,955 | 8,431 | 1,219 | 1,305 | 11% |
| **Sync** | **3,935** | **3,626** | **84** | **225** | **2%** |
| SingleItemView related | 3,303 | 3,119 | 0 | 184 | 0% |
| Organization chooser | 987 | 970 | 0 | 17 | 0% |

The Sync unit is 2% Swift — the least-modernized substantial unit in the app, and
simultaneously the one Phase 4 will class as `INVENTION`. Recorded as a
safety-of-reimplementation signal, **not** as an effort signal.

---

## 1.3 Data model

See §0.2. Summary of both stacks:

| | Core Data | SQLite / FMDB |
|---|---|---|
| Scope | locally-created orders only | full catalog |
| Current schema | `eCat 20260425` | `Database/*.sql` head |
| Entities / tables | 3 | 47 |
| Attributes | 86 | (per-table, in JSON) |
| Relationships | 5 | 3 views |
| Migration steps | 18 (19 versions) | 62 (+ base) |
| Migration source lines | — | 1,577 |

Entity/table participation in sync: **2** of 3 Core Data entities are named in the
Sync unit; **29** SQLite tables are named in the Sync unit plus `DataStore.m` /
`BuildsDataObjects.m` / `DataObject.m` / `ProductQuery.m`. Total distinct types
crossing the sync boundary: **31**.

Entities with more than one schema variant in the wild is deferred to Phase 2
(per-tenant custom fields), as planned.

---

## 1.4 Sync and offline engine

| Metric | Value |
|---|---|
| Files in Sync unit | 31 |
| LOC total | 3,935 |
| LOC LOGIC | 2,540 |
| LOC GLUE | 741 |
| LOC UI | 149 |
| Objective-C methods in unit | 293 |
| Entity/table types crossing sync | 31 |
| **Conflict-resolution branches** | **0** |
| **Last-write-wins paths** | **0** |
| **Merge-resolved paths** | **0** |
| `NSMergePolicy` declarations | 0 (string appears in `DataStore.m` only) |
| Files with retry/attempt logic | 6 |
| Files with `backoff` | 0 |

Vocabulary probe (ripgrep `-ci` over `Classes/**/*.{m,h,swift}`), match count and
files touched:

| Term | Matches | Files |
|---|---|---|
| `conflict` | **0** | 0 |
| `lastwritewins` / `last_write` | **0** | 0 |
| `tombstone` | **0** | 0 |
| `etag` / `if-modified-since` | **0** | 0 |
| `vector clock` | **0** | 0 |
| `backoff` | **0** | 0 |
| `merge` | 16 | 9 |
| `resolve` | 25 | 12 |
| `overwrite` | 4 | 3 |
| `stale` | 12 | 6 |
| `dirty` | 85 | 17 |
| `pending` | 301 | 60 |
| `retry` | 34 | 6 |
| `reachab` | 170 | 7 |
| `timeout` | 26 | 11 |
| `cancel` | 454 | 100 |
| `purge` | 18 | 3 |
| `rollback` | 11 | 10 |
| `transaction` | 25 | 7 |

`dirty` (85) and `pending` (301) describe **local order state**, not sync conflict
state. `cancel` (454) reflects that the sync pipeline is a cancellable chain
(`executeCancellableChain:`) — cancellation is a first-class concern; merge is not.

---

## 1.5 Integration surface

All URL construction funnels through a single chokepoint, `Classes/MakesURLs.m`
(213 lines), with **123 `MakesURLs` call sites** across the app. Two hardcoded
hosts: `staging.k8s.supercatsolutions.com`, `supercat.supercatsolutions.com`.
API base is `{loginHost}/api/v1/{resource}`.

Scanning for bare `"/path"` literals returned only 11 results and was effectively
a tooling failure; the corrected extraction reads the `resource` arguments at
`MakesURLs` call sites. **17 distinct endpoint resources:**

| Resource | Call sites |
|---|---|
| `users/current.json` | 3 |
| `users/authorize.plist` | 3 |
| `organizations.plist` | 3 |
| `passwordless_sessions/request_link` | 2 |
| `passwordless_sessions/verify_passcode` | 2 |
| `passwordless_sessions/verify_token` | 2 |
| `ecat_broadcasts.json` / `?unread=true` | 1 / 1 |
| `orders.json` | 1 |
| `documents/local_customers` | 1 |
| `documents/orders` | 1 |
| `documents/current_order_status` | 1 |
| `documents/lists` | 1 |
| `customer_mapping` | 1 |
| `matrix_options.db` | 1 |
| `users/%@/change_email.json` | 1 |
| `eCat` | 1 |

Server side (pin `bd7895a7e`): **24 API controllers** under `app/controllers/api/`
exposing **75 public actions**, plus **13 `ecat_*` web controllers** that render
HTML rather than call `/api/v1`.

**`ipad_only_vs_shared`: `UNKNOWN`** for every endpoint. The iPad consumes
`/api/v1/*`, which any client can reach; the server's 13 `ecat_*` controllers are a
separate HTML surface. Establishing per-endpoint exclusivity needs server-side
request-log attribution, which the read-only Postgres MCP does not expose. Left
`UNKNOWN` rather than guessed. Note the asymmetry worth carrying forward: the iPad
uses 17 resources against 75 available API actions.

---

## 1.6 Platform-native dependencies — port hazards

Ranked by call sites. `screens` = distinct screens whose files touch the pattern.

| Hazard | Call sites | Files | Screens | `web_equivalent` |
|---|---|---|---|---|
| Core Data local persistence | 221 | 49 | 7 | `REQUIRES_PRODUCT_DECISION` |
| FMDB / direct SQLite | 151 | 34 | 6 | `POLYFILLABLE` |
| Local filesystem | 66 | 19 | 5 | `REQUIRES_PRODUCT_DECISION` |
| Mail compose / native share | 47 | 15 | 7 | `POLYFILLABLE` |
| PDF generation / render | 37 | 13 | 2 | `POLYFILLABLE` |
| WebView bridge | 36 | 6 | 6 | `NATIVE_EQUIVALENT` |
| Popover presentation | 32 | 16 | 8 | `REQUIRES_PRODUCT_DECISION` |
| Split view / iPad multitasking | 23 | 9 | 4 | `REQUIRES_PRODUCT_DECISION` |
| Camera / barcode scanning | 18 | 6 | 0 | `POLYFILLABLE` |
| Biometric auth | 16 | 3 | 1 | `POLYFILLABLE` |
| Printing | 10 | 3 | 3 | `POLYFILLABLE` |
| Firebase Crashlytics / Analytics | 10 | 3 | 0 | `NATIVE_EQUIVALENT` |
| Keychain | 9 | 1 | 0 | `POLYFILLABLE` |
| Device orientation | 8 | 3 | 1 | `REQUIRES_PRODUCT_DECISION` |
| Mixpanel telemetry | 6 | 3 | 0 | `NATIVE_EQUIVALENT` |
| Zip archive | 2 | 1 | 0 | `POLYFILLABLE` |
| Push / local notifications | 2 | 2 | 0 | `POLYFILLABLE` |
| PencilKit / handwriting | 0 | 0 | 0 | `NONE` (absent) |
| Drag and drop | 0 | 0 | 0 | absent |
| Background tasks | 0 | 0 | 0 | absent |
| Hardware keyboard | 0 | 0 | 0 | absent |

**PencilKit, drag-and-drop, background tasks, and hardware-keyboard handling are
absent from this codebase.** The brief anticipated them; they are not here.

### Shipped-but-dormant native assets

Reporting 0 call sites alone would misrepresent these as absent, so they are
recorded separately:

- `sqlite-vec` static libraries + `sqlite_vec.xcframework` (0.1.6, arm64 + simulator)
- `CoreMLModels/SentenceTransformer.mlpackage` + `vocab.txt`
- Build scripts `update_sqlite_vec.py`, `convert_sentence_transformer_to_coreml.py`

The **only** reference in `Classes/` is a comment: `DataStore.h:352: // sqlite-vec
testing`. The `SemanticSearch` unit's Swift files import only `Foundation`.
Vector/semantic search is vendored and wired into the build but has no live
integration in application source. Phase 2 telemetry corroborates:
`smart_search_embeddings_generated` fired 37 times across 13 orgs and
`smart_search_toggled` 37 times across 11 orgs, both stopping in 2026-04/05.

---

## 1.7 Confidence signals

**Safety-of-reimplementation signals only. Not effort signals.**

| Signal | Value |
|---|---|
| Test files (`SuperCatTest/`) | 45 |
| Test lines | 3,435 |
| Test files (`test/`) | 0 |
| Ratio of test lines to app code lines | 3,435 : 86,610 |
| `TODO` | 33 |
| `HACK` | 5 |
| `XXX` | 4 |
| `DEPRECATED` | 1 |
| `FIXME` | 0 |
| `WORKAROUND` | 0 |
| Code coverage | **unavailable** |

**Coverage is `TOOLING_FAILED_NOT_ATTEMPTED`.** Xcode coverage requires building
and running the test target against a provisioned simulator. Not attempted, so not
reported. No reading-based approximation was substituted.

Cyclomatic complexity via `scc --by-file --format json`, aggregated by unit:

| Unit | Complexity | Code | Files | Units' files named by tests |
|---|---|---|---|---|
| Order related | 1,452 | 13,573 | 123 | 7 |
| Grid view related | 1,280 | 10,466 | 91 | 10 |
| Global classes | 1,108 | 11,332 | 163 | 22 |
| Data objects | 1,080 | 10,955 | 142 | 9 |
| Reporting and Email Generation | 802 | 6,549 | 79 | 2 |
| **Sync** | **555** | **3,935** | **31** | **0** |
| Customer | 487 | 3,019 | 22 | 1 |
| SingleItemView related | 447 | 3,303 | 21 | 0 |
| Kit/Options related | 409 | 2,982 | 32 | 0 |
| Left Nav | 407 | 2,991 | 21 | 0 |
| Categories | 365 | 2,138 | 57 | 8 |
| Settings | 266 | 2,507 | 21 | 0 |
| Pricing | 223 | 880 | 18 | 8 |
| ShowroomCart | 210 | 1,015 | 6 | 1 |

Units with zero files named by any test: **Sync, SingleItemView related,
Kit/Options related, Left Nav, Settings, Documents Related, Commitments,
Placements, Flipbook, Scan Groups, RepActivity, Organization chooser,
SemanticSearch, Select List, Notifications, Spreadsheet Import, SuperCat Notices,
Database Migration, Custom UI controls**. `Pricing` (223 complexity, 8 files named
by tests) is the best-covered domain-logic unit; `Sync` (555 complexity, 0) the
least.

---

## 1.8 Dead code

| Category | Count | Detail |
|---|---|---|
| Source files on disk but absent from `project.pbxproj` (not compiled) | **3** | `Classes/Functional.swift`, `Classes/SurchargeType.swift`, `Classes/SurchargeValue.swift` |
| Unreachable screen candidates | 5 | §1.1, 104 LOC total |
| IB documents, total | 95 | — |
| IB documents with a `customClass` not declared anywhere in source | **2** | `FullScreen.xib` (`FullScreenViewController`), `NoneCell.xib` (`UIResponder` only) |
| IB documents with no `customClass` bindings at all | 6 | `DetailView.xib`, `Launch Screen.storyboard`, `OrderOptionsCell.xib`, `OrderTableHeader.xib`, `SettingsPriceLevelController.xib`, `StandardToolbar.xib` — **normal** (File's Owner pattern), not dead |
| Classes referenced only within their own `.h`/`.m` pair | 6 | below |

The three uncompiled files were verified twice: zero references in
`project.pbxproj` and zero references in any other source file. `Functional.swift`
and `SurchargeType.swift` have no references anywhere;
`SurchargeValue.swift` is distinct from the compiled
`CalculateSurchargeValue.swift`.

Classes referenced only in their own header/implementation pair:

| Class | Header LOC | Impl LOC |
|---|---|---|
| `SelectProductFilterViewController` | 3 | 119 |
| `SceneDelegate` | 4 | 47 |
| `BuildsSearchAndFilterPanel` | 3 | 41 |
| `SwitchableSplitViewController` | 3 | 27 |
| `SwitchableNavigationController` | 3 | 25 |
| `SettingsAboutController` | 3 | 12 |

These are **candidates, not confirmed dead**. `SceneDelegate`,
`SwitchableSplitViewController`, and `SwitchableNavigationController` are plausibly
instantiated by name from `Info.plist` or a storyboard rather than referenced in
code, and `SwitchableSplitViewController` is actively modified on
`spike/iphone-compatibility`. Feature flags permanently off, and code paths gated
on tenants that no longer exist, are cross-checks deferred to Phase 2 as planned.

---

## SELF-AUDIT — Phase 1

**Does any output contain a time unit, or a scale that implies one?**
No. Every number is a count (files, code lines, methods, screens, edges, entities,
tables, migration steps, call sites, matches, complexity points, orgs, events) or a
percentage of such a count. Dates appear only as Core Data schema version
identifiers, commit provenance, and telemetry-window bounds. No durations, story
points, t-shirt sizes, or effort scores. Complexity and test counts are explicitly
labelled safety signals, not effort signals, in §1.7 and in the Sync language-mix
note.

**Does every factual row have a `source`?**
Yes. Every section names the script that produced it; `01_CODE_CENSUS.json` carries
per-row `source` strings (`p1_units.py` pbxproj parse, `p1_loc_split.py` per-method
classification, `p1_surface.py` IB XML + nav scan, `p1_rest.py` ripgrep/ElementTree
with the exact pattern recorded per hazard). No rows were deleted for missing
provenance. Three claims are explicitly marked unresolved rather than asserted:
`ipad_only_vs_shared` (`UNKNOWN`), code coverage (`TOOLING_FAILED_NOT_ATTEMPTED`),
and the six single-pair classes (candidates, not confirmed).

**Did I report distributions where tenants differ, or did I average?**
No tenant data is in Phase 1 beyond two corroborating org-reach counts for
semantic-search telemetry, both given as counts of orgs. Per-unit and per-screen
figures are given as full tables, not means. The one ratio pair reported — the
LOGIC-first vs UI-first split — is presented as both endpoints plus the overlap,
never as a midpoint.

**Did I mark anything `MECHANICAL` that actually depends on an unmade decision?**
No Phase 3 classification was performed here. Phase 1 pre-emptively removes the
biggest such risk: §0.1 establishes with zero-match evidence that the sync engine
has no conflict-resolution logic to transcribe, so it cannot be `MECHANICAL` or
`RESPECIFICATION`. Six hazards are already marked `REQUIRES_PRODUCT_DECISION`,
which will force them out of `MECHANICAL` in Phase 3.

**Did I fill any field with a plausible guess rather than `UNKNOWN`?**
No. Held as unknown: per-endpoint iPad-exclusivity; code coverage; whether the six
single-pair classes are truly dead; whether the two IB documents with undeclared
`customClass` values are dead or loaded dynamically. I also declined to interpret
the 6 IB documents lacking `customClass` as dead, because the File's Owner pattern
explains them.

**Did I run tooling, or did I read and approximate?**
Ran tooling; six scripts totalling the analysis, all re-runnable, plus `scc` and
`ripgrep`. Four tooling errors were found and corrected rather than shipped, and
each correction is recorded in the script that contains it:
1. A `re.S` comment group in the pbxproj parser matched across newlines, assigning
   wrong group IDs and dropping the `RepActivity` unit entirely.
2. Walking only the `Classes` group dropped files grouped elsewhere
   (`NetworkStatusMonitor.{h,m}`) and misreported them as dead code.
3. Reading the last `.xcdatamodel` alphabetically instead of `.xccurrentversion`
   reported 3 entities as 25 and concealed the two-stack persistence architecture —
   this one also propagated into Phase 0 §1.3, now corrected in §0.2.
4. Scanning for bare `"/path"` literals found 11 endpoints; reading `resource`
   arguments at the `MakesURLs` chokepoint found 17 and identified the chokepoint.
A fifth, milder error — comparing all IB documents against screen-referenced files
— reported 64 orphan XIBs; the corrected test (is any `customClass` declared in
source?) reports 2.

---

**Phase 1 complete.** Phase 2 (tenant census) is next and is the gate on the
Scenario A/B evidence, the kill list, and the schema-variance cross-checks deferred
from §1.3 and §1.8.
