# 00_PLAN.md — eCat iPad → Responsive Web: Estimation Substrate

**Status:** Phase 0 complete and approved. Phase 1 complete.
**Produced:** 2026-08-08

> **CORRECTION issued in Phase 1 — this document contains one wrong fact.**
> §1.3 below reports the Core Data model as having **25 entities / 214 attributes /
> 16 relationships**. That was read from `eCat.xcdatamodeld/eCat.xcdatamodel`, which
> is **not** the current version. `.xccurrentversion` declares the current model as
> `eCat 20260425`, which has **3 entities** (`Order`, `OrderItem`, `OrderItemOption`),
> 86 attributes, 5 relationships. The catalog left Core Data at version
> `eCat 20150407` and now lives in raw SQLite via FMDB (63 migration files, 47
> tables). Local persistence is **two** stacks, not one.
> See `01_CODE_CENSUS.md` §0.2. The counts in §1.3 below are left unedited so the
> error and its correction are both on the record.

---

## 0. Analysis pins

All subsequent phases run against these exact commits. The working checkouts in
`/Users/kylorjohnson/supercat-code/` are stale and are **not** used for analysis.

| Repo | Pin | Commit date | Worktree used for analysis |
|---|---|---|---|
| `sarreid_ios` (the eCat iPad app) | `129242b0e27401b9019f805066f1b8ea88da5380` (`origin/master`) | 2026-07-28 | `/tmp/ecat-audit/ios-master` |
| `supercat_server` | `bd7895a7e` (`origin/master`) | 2026-08-08 | `/tmp/ecat-audit/server-master` |
| `supercat_server` | `fa8a2cbe7` (`origin/spike/ecat-web`) | — | `/tmp/ecat-audit/server-ecatweb` |

Staleness measured, not assumed:

```
$ cd ~/supercat-code/sarreid_ios && git log -1 --format='%h %ad %s'
3b0fac82e Fri Nov 7 10:03:14 2025 -0500 Release 2025.4.4 - turns off liquid (gl)ass
$ git log -1 --format='%h %ad %s' origin/master
129242b0e Tue Jul 28 12:35:01 2026 -0400 increment build version

$ cd ~/supercat-code/supercat_server && git rev-list --count HEAD..origin/master
62
```

Worktrees were created with `git worktree add` so the user's checkouts are untouched.

---

## 1. Repository inventory

### 1.1 Raw `scc` output — iOS app (pin `129242b0e`, path `eCatalog/`)

Tool: `scc version 3.7.0`, installed via `brew install scc` during Phase 0.
Command: `scc --no-cocomo ios-master/eCatalog`

```
───────────────────────────────────────────────────────────────────────────────
Language            Files       Lines    Blanks  Comments       Code Complexity
───────────────────────────────────────────────────────────────────────────────
Swift                 346      35,304     6,221     2,964     26,119      3,417
C Header              343       9,472     1,988     2,466      5,018          1
Objective C           325      77,179    14,219     4,759     58,201      7,006
SQL                    63       1,577        89        42      1,446          0
Plain Text             13      31,346       176         0     31,170          0
JSON                   12       7,509         0         0      7,509          0
Ruby                    8         472        95        83        294         21
Go Template             5          13         2         0         11          0
Shell                   5          43        11        10         22          1
JavaScript              2         587        79       132        376         58
Python                  2         550        69        78        403          8
HTML                    1           1         0         0          1          0
Makefile                1          25         7         0         18          0
───────────────────────────────────────────────────────────────────────────────
Total               1,126     164,078    22,956    10,534    130,588     10,512
───────────────────────────────────────────────────────────────────────────────
Processed 9194692 bytes, 9.195 megabytes (SI)
───────────────────────────────────────────────────────────────────────────────
```

Command: `scc --no-cocomo ios-master/eCatalog/Classes` (application source only,
excludes assets, SQL seeds, test fixtures, vendored ZipArchive/sqlite-vec):

```
───────────────────────────────────────────────────────────────────────────────
Language            Files       Lines    Blanks  Comments       Code Complexity
───────────────────────────────────────────────────────────────────────────────
Swift                 332      34,292     6,051     2,773     25,468      3,351
C Header              331       9,312     1,949     2,386      4,977          1
Objective C           301      74,671    13,714     4,557     56,400      6,982
Plain Text              1          27         7         0         20          0
───────────────────────────────────────────────────────────────────────────────
Total                 965     118,302    21,721     9,716     86,865     10,334
───────────────────────────────────────────────────────────────────────────────
Processed 4157628 bytes, 4.158 megabytes (SI)
───────────────────────────────────────────────────────────────────────────────
```

**Headline countable:** the in-scope application source is **86,865 code lines**
across **965 files**, split Objective-C 56,400 / Swift 25,468 / C headers 4,977.
This is a **two-language codebase mid-migration from Objective-C to Swift**, which
is itself a Phase 1 finding: the ObjC:Swift ratio per unit is a measurable signal
about which units have already been touched recently.

`scc` does **not** count `.storyboard` / `.xib` XML. Those are counted separately
in §1.3 and will be inventoried in Phase 1.1.

### 1.2 Raw `scc` output — supercat_server (context, not primary scope)

Command: `scc --no-cocomo server-master/app server-master/lib`

```
───────────────────────────────────────────────────────────────────────────────
Language            Files       Lines    Blanks  Comments       Code Complexity
───────────────────────────────────────────────────────────────────────────────
Ruby HTML           1,044      60,304     4,838       528     54,938      3,369
Ruby                  949     115,515    17,436    11,501     86,578      6,275
JavaScript            105      33,716     3,947    11,475     18,294      3,264
SVG                    83       1,306        63        34      1,209          0
Sass                   75      15,893     1,501       699     13,693         43
CSS                    16       3,294       339       331      2,624          0
Markdown                6         782       145         0        637          0
───────────────────────────────────────────────────────────────────────────────
Total               2,278     230,810    28,269    24,568    177,973     12,951
───────────────────────────────────────────────────────────────────────────────
Processed 8677096 bytes, 8.677 megabytes (SI)
───────────────────────────────────────────────────────────────────────────────
```

### 1.3 Structural counts (measured)

| Thing | Count | Source |
|---|---|---|
| Build targets | 2 (`eCat`, `SuperCatTest`) | `rg -o 'PBXNativeTarget "[^"]+"' eCatalog.xcodeproj/project.pbxproj \| sort -u` |
| Xcode logical groups | 59 | `rg -c 'isa = PBXGroup' eCatalog.xcodeproj/project.pbxproj` |
| Files at `Classes/` root (flat) | 1,039 | `find Classes -maxdepth 1 -type f \| wc -l` |
| Subdirectories under `Classes/` | 3 (`RepActivity`, `SemanticSearch`, `ShowroomCart`) | `ls -d Classes/*/` |
| `.storyboard` + `.xib` files | 95 | `find . -name "*.storyboard" -o -name "*.xib" \| wc -l` |
| `.xib` files | 72 | `find . -name "*.xib" \| wc -l` |
| Storyboard scene elements | 99 | `rg -o '<viewController \|<tableViewController \|<collectionViewController \|<navigationController ' Classes/*.storyboard \| wc -l` |
| Objective-C view controller `@interface` decls | 52 | `rg -o '@interface\s+\w+\s*:\s*\w*(ViewController\|TableViewController\|CollectionViewController)' Classes/ \| wc -l` |
| Swift view controller class decls | 50 | `rg -o 'class\s+\w+\s*:\s*[^{]*(UIViewController\|UITableViewController\|UICollectionViewController)' Classes/ \| wc -l` |
| SwiftUI `View` structs | 0 | `rg -o 'struct\s+\w+\s*:\s*View\b' Classes/ \| wc -l` |
| Core Data model versions | 19 | `ls eCatalog/eCat.xcdatamodeld/` |
| Entities in current model | 25 | parsed from `eCat.xcdatamodeld/eCat.xcdatamodel/contents` |
| Attributes in current model | 214 | same |
| Relationships in current model | 16 | same |

**Two structural facts that shape the whole analysis:**

1. **`Classes/` is flat.** 1,039 of 1,062 files sit at one directory level. There is
   no filesystem module boundary to inherit. Unit boundaries for Phase 3 must
   therefore be *derived*, not read off the tree. My intended derivation source is
   the **59 Xcode `PBXGroup` entries** in `project.pbxproj` (observed group names
   include `Sync`, `Orders`, `Products`, `Pricing`, `Options`, `Placements`,
   `Login`, `Query`, `Settings`, `Images`, `Resources`), cross-checked against
   storyboard clustering and the `#import` graph. This is a methodology choice I
   want approved before Phase 1, because every downstream rollup inherits it.
2. **Zero SwiftUI.** All 102 view controller classes are UIKit. There is no
   declarative-UI layer to translate; the UI tier is imperative UIKit plus 95
   Interface Builder documents.

### 1.4 Third-party dependencies (from `eCatalog/Podfile`, verbatim)

```
platform :ios, '16.0'
use_frameworks!

target "eCat" do
  pod "AFNetworking",         "~> 3.1"
  pod "SBJson",               "~> 5.0.0"
  pod "Firebase/Crashlytics", "~> 8.9.1"
  pod "Firebase/Analytics",   "~> 8.9.1"
  pod "Mixpanel",             "~> 3.6.1"
  pod "FMDB",                 "~> 2.7.5"
  pod "PromisesSwift"
  pod "SSZipArchive"
  pod 'ZXingObjC',            '~> 3.6.4'
end
```

Plus non-Pod native components observed in the tree: `sqlite-vec` /
`sqlite_vec.xcframework` (vector search), `CoreMLModels/` (on-device embeddings),
`ZipArchive/`. `pspdfkit_activated` appears as a telemetry event, implying a
PSPDFKit integration to confirm in Phase 1.6.

Each of these is a Phase 1.6 port-hazard candidate. Note that **FMDB + Core Data +
sqlite-vec + CoreML** together mean the local persistence story is not one
mechanism but at least three.

---

## 2. Prior art discovered in Phase 0 — this changes the shape of the analysis

This was not in the brief's assumptions and I flag it before proceeding.

### 2.1 `supercat_server` branch `spike/ecat-web` — a partial eCat web already exists

```
$ git rev-list --count origin/master..origin/spike/ecat-web
34
$ git diff --stat $(git merge-base origin/master origin/spike/ecat-web) origin/spike/ecat-web | tail -1
249 files changed, 57588 insertions(+), 130 deletions(-)
```

Directory distribution of changed files (`git diff --name-only ... | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn`):

```
  36 docs/design/design-system/ds/primitives
  19 app/views/ecat_products
  14 app/views/ecat_order_process
  13 test/controllers
  13 app/services/ecat
  12 app/javascript/controllers
  11 vendor/design_system/primitives
  10 docs/design/design-system/ds/tokens
   8 vendor/design_system/tokens
   8 test/services/ecat
   8 app/views/ecat_customer_picker
   7 docs/design/design-system
   7 app/views/layouts/ecat
   6 docs/design/design-system/app
   6 app/components/sc/ecat
   5 app/controllers
   4 docs/superpowers/specs
```

Commit subjects show a working catalog index, PDP (`show_v2` with an allowlisted
presenter), cart with Turbo Stream badge updates, customer picker, an
`Ecat::ShellPresenter` for v2 chrome, **mobile catalog navigation**, and
controller/service tests.

**Consequence:** the rewrite is not greenfield. Some units are already
`MECHANICAL` *because this spike established the pattern*, and some are already
partially built. Phase 3 must carry a field distinguishing "not yet built" from
"pattern established by spike" from "already built in spike," or the ledger will
overstate the remaining bill of materials. **I propose adding a non-time field
`spike_status: NOT_STARTED | PATTERN_ESTABLISHED | PARTIALLY_BUILT | UNKNOWN` to
the Phase 3 schema.** It is a categorical, not a duration. Requesting approval.

### 2.2 `sarreid_ios` branch `spike/iphone-compatibility`

```
$ git rev-list --count origin/master..origin/spike/iphone-compatibility
1
43d7c6089 WIP iphone liquid glass form factor
44 files changed, 1262 insertions(+), 341 deletions(-)
```

Touches `SwitchableSplitViewController.m`, `UIViewController+eCat.m`,
`SingleItemViewController.m`. This is direct evidence about how hard the
iPad→small-form-factor reflow is *in the existing codebase*, which is the closest
available proxy for the responsive-reflow problem. It is a Phase 6 calibration
candidate.

### 2.3 eCat Online already exists as a web surface

`app/controllers/` on server master contains `ecat_online_controller.rb`,
`ecat_products_controller.rb`, `ecat_orders_controller.rb`,
`ecat_order_process_controller.rb`, `ecat_customers_controller.rb`,
`ecat_dashboard_controller.rb`, `ecat_reports_controller.rb`,
`ecat_rma_requests_controller.rb`, `ecat_sessions_controller.rb`,
`mobile_sites_controller.rb` (`ls app/controllers/ | rg -i 'ipad|sync|ecat|mobile|api'`).

**This is an unresolved scoping question, not a finding.** "Rewrite eCat iPad as
responsive web" could mean (a) new surface, (b) extend `spike/ecat-web`, or
(c) bring eCat Online to parity. These have different bills of materials. This
goes to the invention register as **the first entry**, and I am not going to pick
one silently.

---

## 3. MCP endpoint enumeration — tested, not assumed

Five MCP servers were advertised. I probed each. Results:

| Server | Status | Verified capability | Usable for this analysis |
|---|---|---|---|
| `user-supercat-postgres-vpn` | **ready, verified** | 9 tools; `execute_sql` read-only against `supercatprod` | **Yes — primary Phase 2 source** |
| `user-bigquery-admin` | **ready, verified** | 13 tools; `query`, `list_datasets`, `list_tables`, `get_table_schema` | **Yes — primary Phase 2 usage source** |
| `plugin-atlassian-atlassian` | advertised | Jira/Confluence | Read-only per workspace rule; Phase 3 `behavior_specification` evidence only |
| `plugin-linear-linear` | advertised, not probed | unknown | To probe if Phase 3 needs ticket provenance |
| `user-Notion` | advertised, not probed | unknown | To probe if Phase 3 needs spec provenance |

### 3.1 Postgres — `supercatprod`

Verified live:

```sql
select current_database(), current_user, version(), pg_size_pretty(pg_database_size(current_database()))
-- → supercatprod | crunchy_reader | PostgreSQL 15.17 | 84 GB
```

```sql
select (select count(*) from organizations) as orgs_total,
       (select count(*) from information_schema.tables where table_schema='public') as public_tables,
       (select count(*) from information_schema.columns where table_schema='public') as public_columns
-- → 255 | 116 | 1953
```

**Architecture fact that matters:** this is **one multi-tenant database**, not 255
tenant instances. "Query every reachable tenant instance" in the brief resolves to
"one query, grouped by organization." Every tenant is reachable. Tenant-census
coverage is therefore structurally complete for anything stored in Postgres — a
better position than the brief anticipated.

Single schema: `public`, 116 tables. Tables identified as load-bearing for Phase 2:

| Table | Cols | Phase 2 use |
|---|---|---|
| `organizations` | **98** | Configuration reality — the real flag combinatorics |
| `org_setting_definitions` / `org_setting_values` | 12 / 10 | Second settings surface, must be counted separately |
| `user_types` | **72** | User-group permission surface |
| `products` | **231** | Catalog scale + custom-field variance |
| `product_inventory` | **220** | Same, inventory side |
| `orders` | **66** | Order volume; candidate offline-gap evidence |
| `login_events` | 16 | Session/blast-radius indicator |
| `custom_fields`, `customer_custom_fields`, `inventory_custom_fields`, `option_custom_fields`, `order_custom_fields` | 16/7/8/7/12 | Schema variance — distinct shapes per tenant |
| `smart_stacks`, `ipad_reports`, `mobile_sites`, `showroom_locations`, `commitment_reports`, `placement_reports`, `rma_requests`, `kit_items`, `matrix_options`, `option_mappings` | — | Per-tenant feature adoption |
| `data_versions` | 4 | Sync versioning |
| `import_events` | 4 | Data-pipeline activity |

The `organizations` table having **98 columns** is itself the Phase 2 headline
risk: the theoretical configuration surface is enormous and the brief correctly
demands I count *actual distinct configurations in production* instead.

### 3.2 BigQuery — 24 datasets, and the iPad telemetry is real

`list_datasets` returned 24. The relevant ones:

- **`mixpanel`** — `events` table: **10,661,150 rows / 4.15 GB**, last modified 2026-08-07.
  Also `user_org_mapping` (3,162 rows), `organization_customer_mapping` (226 rows),
  and views `org_feature_usage_report`, `user_feature_usage_report`.
- `google_analytics_ecat`, `google_analytics_ecat_online` — web surfaces, page-path
  level. **Not iPad.** Relevant only as eCat Online context.

Verified segmentation of `mixpanel.events`:

```sql
SELECT mp_lib, COUNT(*) AS events, COUNT(DISTINCT event_name) AS distinct_events,
       COUNT(DISTINCT device_id) AS devices,
       MIN(DATE(TIMESTAMP_SECONDS(CAST(time AS INT64)))) AS first_day,
       MAX(DATE(TIMESTAMP_SECONDS(CAST(time AS INT64)))) AS last_day
FROM `mixpanel.events` GROUP BY 1 ORDER BY events DESC
```

| mp_lib | events | distinct_events | devices | first_day | last_day |
|---|---|---|---|---|---|
| `iphone` | 10,188,262 | 49 | 5,970 | 2024-11-01 | 2026-08-07 |
| `ruby` | 472,888 | 1 | 0 | 2024-11-01 | 2026-08-07 |

`mp_lib='iphone'` is the iPad app. **Window available: 2024-11-01 → 2026-08-07.**

Tenant-attribution path, verified (the obvious column is the wrong one):

```sql
SELECT COUNT(*) AS ipad_events, COUNT(current_organization_shortname) AS has_cur_org,
       COUNT(DISTINCT current_organization_shortname) AS distinct_cur_org,
       COUNT(DISTINCT username) AS distinct_username, COUNTIF(wifi IS NOT NULL) AS has_wifi
FROM `mixpanel.events` WHERE mp_lib='iphone'
-- → 10,188,262 | 10,185,685 | 191 | 4,245 | 10,184,745
```

`organization_shortname` is **NULL on all iPad rows**; the correct join key is
**`current_organization_shortname`**, populated on 99.97% of rows, covering
**191 distinct orgs**. Recording this because using the obvious column would
silently return zero and I would have reported "no tenant attribution available."

Also present and populated on ~100% of iPad rows: **`wifi` (BOOLEAN)** — this is a
genuine, if indirect, connectivity signal, and is the single most promising
Scenario A/B evidence source found in Phase 0.

---

## 4. The hard coverage limit I found — state it now, not in Phase 7

**Telemetry is feature-level, not screen-level.**

There are 49 instrumented iPad event names against 99 storyboard scenes, 72 XIBs,
and 102 view controller classes. The instrumented events are named for user
actions (`product_search`, `order_submitted`, `view_kit`), not for screens.

**Consequence for Phase 2:** the brief asks, for every screen from 1.1, for
"tenants with any use, tenants with regular use, total sessions touching it." For
roughly the 49 instrumented behaviors, I can answer that precisely, per tenant,
over a 21-month window. **For the remaining screens, I cannot, and I will not
infer it.** Those screens will be reported with `usage_evidence: NONE_AVAILABLE`
rather than a modelled number.

I can partially compensate — not substitute — with Postgres *configuration and
artifact* evidence: a tenant with zero `smart_stacks` rows has no SmartList
screens in use; zero `kit_items` means no kit screens. That is evidence of
**feature enablement**, which is weaker than usage and will be labelled as such in
a separate column. The kill list in Phase 5 will be split accordingly, and
`LOW_USE` claims will be sourced only from actual telemetry, never from
enablement.

The 49 event names are already informative — a preview, with full per-tenant
distributions deferred to Phase 2:

| Event | orgs (of 191) |
|---|---|
| `selected_org` | 191 |
| `product_search` | 157 |
| `customer_selection` | 150 |
| `view_kit` | 24 |
| `add_kit_to_order` | 20 |
| `view_flipbook` | 11 |
| `view_commitments` | 5 |
| `flipbook_add_to_order` | 5 |
| `flipbook_add_to_list` | 4 |

Flipbook (11 orgs), Commitments (5 orgs), and Kits (20–24 orgs) are already
visible as kill-list candidates. I am **ranking, not recommending** — and these
counts are org-reach, not intensity; Phase 5 will carry both plus named tenants.

---

## 5. Exact commands and queries for Phases 1–2

### 5.1 Phase 1 — codebase census

**1.1 Surface inventory.** Parse `project.pbxproj` for group membership; parse each
`.storyboard`/`.xib` XML for scene elements, `customClass` bindings, and segue
elements to build the navigation graph:

```bash
# scenes + custom class bindings
rg -o 'customClass="([^"]+)"' -r '$1' Classes/*.storyboard Classes/*.xib | sort -u
# navigation edges
rg -o '<segue[^>]*destination="([^"]+)"[^>]*kind="([^"]+)"' Classes/*.storyboard
# programmatic navigation not expressible as segues
rg -n 'pushViewController|presentViewController|presentModalViewController|performSegueWithIdentifier|instantiateViewControllerWithIdentifier|showDetailViewController' Classes/
```

Zero-inbound-edge scenes → `reachability: UNREACHABLE_CANDIDATE`. Programmatic
navigation is why I will not rely on segues alone; the ObjC-era code predates
storyboard segues in places.

**1.2 The three-way LOC split.** Proposed **mechanical** rule, applied per
function/method, stated here for approval *before* it is applied:

- **UI** — the file is a `*ViewController`, `*View`, `*Cell`, `*Presenter`, or the
  method body references `UIKit` layout/appearance symbols (`layoutSubviews`,
  `NSLayoutConstraint`, `frame`, `UIColor`, `UIFont`, `drawRect`, `animateWithDuration`,
  `prepareForSegue`, `tableView:cellForRowAtIndexPath:`) and no domain symbol.
- **LOGIC** — method body references pricing, order, option/config, kit, inventory,
  discount, surcharge, tax, validation, filter/search-ranking, or sync-resolution
  symbols. Determined by matching against an identifier allowlist derived from the
  25 Core Data entity names plus a domain-term list, published in `01_CODE_CENSUS.md`.
- **GLUE** — Core Data stack, `AppDelegate`, threading/GCD, keychain, file
  management, networking transport, DI/singletons, logging, analytics wiring.
- Precedence when a method matches more than one: **LOGIC > GLUE > UI**, so the
  split never flatters the logic tier by leaking it into UI.
- Mixed files are split per method, and the count of split files is reported.
- Anything matching none of the three: `UNCLASSIFIED`, reported as its own bucket
  rather than distributed.

`.storyboard`/`.xib` XML is reported as a **separate fourth quantity (IB_XML)** in
element counts, never folded into `ui_loc` — XML line counts are not comparable to
code lines and folding them in would corrupt the headline ratio.

**1.3 Data model.** Parse all 19 `.xcdatamodel/contents`; per version, entity /
attribute / relationship counts; diff adjacent versions to count migrations and
identify entities that changed shape.

**1.4 Sync and offline engine.** Identify sync sources from the Xcode `Sync` group
and `Sync.storyboard`, then:

```bash
rg -n 'conflict|merge|lastWriteWins|resolve|stale|dirty|pending|queue|retry|backoff|reachab' Classes/ --type-add 'objc:*.{m,h}' -tobjc -tswift
```

Counts required: conflict-resolution branches, entity types participating, retry/
backoff paths, last-write-wins vs merge-resolved paths.

**1.5 Integration surface.** Extract client-side endpoint strings from iOS, then
reconcile against server routes:

```bash
# iOS side
rg -o '"(/[a-z0-9_/.{}:-]+)"' Classes/ | sort -u
rg -n 'AFHTTPSessionManager|URLSession|NSURLRequest|GET:|POST:|PUT:|DELETE:' Classes/
# server side
cd server-master && rg -n '' config/routes.rb
find app/controllers/api -name '*.rb'   # 24 files, api/v1/* + api/onboarding/*
```

Shared-vs-iPad-only determined by cross-referencing call sites in Admin Console,
Sales Portal, and eCat Online view/controller code in the same repo.

**1.6 Port hazards.** Fixed probe list, each producing call sites + affected screens:

```bash
rg -n 'NSManagedObject|NSPersistentStoreCoordinator|FMDatabase' Classes/        # local persistence
rg -n 'PencilKit|PKCanvas|UIDragInteraction|UIDropInteraction' Classes/         # pencil / drag-drop
rg -n 'AVCaptureSession|ZXing|AVCaptureMetadataOutput' Classes/                 # camera / barcode
rg -n 'NSFileManager|NSSearchPathForDirectoriesInDomains|SSZipArchive' Classes/ # filesystem / zip
rg -n 'beginBackgroundTask|BGTaskScheduler|UNUserNotification|APNS' Classes/    # background / push
rg -n 'UIPrintInteractionController|PDFKit|PSPDFKit|UIGraphicsPDF' Classes/     # print / PDF
rg -n 'WKWebView|UIWebView|evaluateJavaScript' Classes/                         # webview bridges
rg -n 'SecItemAdd|Keychain' Classes/                                            # keychain
rg -n 'MLModel|CoreML|sqlite_vec|sqlite3_vec' Classes/                          # on-device ML / vector
```

**1.7 Confidence signals.** Test files under `SuperCatTest/` (48 files) and `test/`
(8 files) mapped to units; `scc` complexity per unit (already emitted per-language);
`rg -c 'TODO|FIXME|HACK|XXX' Classes/`. Reported as safety signals only. Xcode
coverage requires a successful build; if the build fails, I will report
`coverage: TOOLING_FAILED` rather than substitute a guess.

**1.8 Dead code.** Zero-inbound-edge screens from 1.1; symbols declared in headers
with no reference outside their own file; feature flags from `organizations`
columns that are false for all 255 orgs (cross-checked in Phase 2); tenant-gated
paths where the tenant no longer exists.

### 5.2 Phase 2 — tenant census

**Configuration reality** (the brief's "distinct actual configurations"):

```sql
-- per boolean flag column on organizations, how many orgs true / false / null
-- generated dynamically from information_schema, one row per column
-- then: count DISTINCT full flag-tuples across orgs = the real combinatorial surface
```

**Catalog scale distribution** — reported as min / p10 / median / p90 / max **plus
the full 255-row per-tenant table**, never as a mean:

```sql
select o.short_name,
       count(distinct p.id) as skus,
       count(distinct pi_.id) as images,
       count(distinct k.id) as kit_items,
       count(distinct opt.id) as options
from organizations o
left join products p on p.organization_id = o.id and p.deleted is not true
...
group by 1 order by skus desc
```

**Schema variance:** `count(distinct custom-field-name-set)` per tenant across the
five `*_custom_fields` tables → count of distinct shapes.

**Feature adoption:** per-tenant row counts in `smart_stacks`, `kit_items`,
`matrix_options`, `option_mappings`, `ipad_reports`, `showroom_locations`,
`commitment_reports`, `placement_reports`, `rma_requests`, `mobile_sites`.

**Usage per tenant** (BigQuery, the 49 instrumented behaviors):

```sql
SELECT current_organization_shortname AS org, event_name,
       COUNT(*) AS events, COUNT(DISTINCT username) AS users,
       COUNT(DISTINCT DATE(TIMESTAMP_SECONDS(CAST(time AS INT64)))) AS active_days,
       MAX(DATE(TIMESTAMP_SECONDS(CAST(time AS INT64)))) AS last_used
FROM `mixpanel.events`
WHERE mp_lib='iphone'
GROUP BY 1,2
```

"Any use" = ≥1 event. "Regular use" will be defined as a **countable threshold on
active_days within the window**, with the threshold stated explicitly and results
also shown at adjacent thresholds so the cut point is visible rather than hidden.

**Offline evidence for the fork** — three independent probes, reported separately,
with an explicit statement of what each does and does not prove:

1. `wifi=false` event share, per tenant, and run-length of consecutive
   `wifi=false` events per `device_id` — measures *cellular vs wifi*, which is
   **not** the same as disconnected. I will label it as such.
2. Postgres `orders`: difference between on-device creation timestamp and
   server-receipt timestamp, per order, distribution per tenant. Phase 2 must first
   verify that `orders` (66 columns) actually carries a device-side timestamp; if
   it does not, this probe is reported as unavailable.
3. `mixpanel` event-time vs `mp_processing_time_ms` / `mp_api_timestamp_ms` gap —
   the Mixpanel iOS SDK batches and flushes on connectivity, so a large
   client-event-time to server-ingest-time gap is a **direct** disconnection
   signal. This is the strongest of the three and I will lead with it.

If none of the three yields usable data, Phase 2 says so plainly and the fork
stays entirely in the invention register.

**Blast-radius inputs:** per tenant — `org_users` count, `login_events` count,
`orders` count, catalog size. **No revenue, contract value, `subscriptions`,
`subscription_plans`, `subscription_tiers`, `stripe_invoices`, or
`subscription_invoices` will be queried or recorded**, per the brief. Noting that
those tables exist and are deliberately excluded.

---

## 6. What I cannot see

| Gap | Evidence | Effect |
|---|---|---|
| **GitHub API unavailable** — `gh` not authenticated (`gh auth status` → "not logged into any GitHub hosts"). SSH git works. | Cannot enumerate org repos. | I cannot confirm `sarreid_ios` is the *canonical* eCat iOS repo rather than one client fork. Evidence *for* canonical: single `eCat` build target, runtime org selection (`selected_org` telemetry across 191 orgs), `GlobalThemes.plist`. **Not yet proven.** Needs either `gh auth login` or your confirmation. |
| **No CocoaPods checkout** | `Pods/` absent from the tree | Third-party LOC not counted. Correct for a rewrite BOM (you don't rewrite AFNetworking), but it means complexity totals exclude dependency internals. |
| **Build not verified** | `xcodebuild` present; no build attempted in Phase 0 | Coverage instrumentation (1.7) and AST-accurate analysis may be unavailable. Will be reported as `TOOLING_FAILED`, not estimated. |
| **No server-side pin for iPad API contract** | — | Endpoint reconciliation (1.5) is text-matching between two repos, not a typed contract. Ambiguous matches → `UNKNOWN`. |
| **Screen-level telemetry absent** | 49 events vs 99 scenes (§4) | The single largest evidence gap. Cannot be closed from available sources. |
| **64 orgs in Postgres with no iPad telemetry** | 255 orgs vs 191 in Mixpanel | Not yet explained — could be inactive orgs, non-iPad products, or pre-instrumentation. Phase 2 will classify them rather than drop them. |
| **Mixpanel window is 21 months** | 2024-11-01 → 2026-08-07 | Anything used less often than annually may look unused. Phase 5 will flag seasonal-risk candidates instead of ranking them as dead. |
| **Linear / Notion unprobed** | — | Phase 3 `behavior_specification` may under-report `SPECIFIED` if specs live there. Will probe before Phase 3. |

---

## 7. Decisions I need from you before Phase 1

1. **Unit-boundary derivation** (§1.3): approve the 59 Xcode `PBXGroup` entries as
   the unit-boundary source, cross-checked against storyboard clustering and the
   import graph. Everything downstream inherits this.
2. **UI/LOGIC/GLUE classification rule** (§5.2 1.2): approve the rule and the
   `LOGIC > GLUE > UI` precedence before I apply it mechanically.
3. **`spike_status` field** (§2.1): approve adding it to the Phase 3 schema.
   Without it the ledger will treat already-built work as unbuilt.
4. **eCat Online scoping** (§2.3): is the target a new surface, an extension of
   `spike/ecat-web`, or eCat Online brought to parity? If you'd rather this stay an
   open question, say so and it becomes invention-register entry #1 — that is a
   legitimate answer and I will not pick one for you.
5. **`gh auth login`** (§6): permits confirming repo canonicity. Optional; without
   it that stays an explicit unknown.
6. **Phase 6 calibration units:** the brief says you will name 2–3 already-built
   units. `spike/ecat-web` (catalog / PDP / cart / customer picker) and
   `spike/iphone-compatibility` are natural candidates found in Phase 0. Name the
   ones you want and I will run Phases 1 and 3 against them without looking at
   actuals.

---

## SELF-AUDIT — Phase 0

**Does any output contain a time unit, or a scale that implies one?**
No. Checked every number in this document. All are counts of countable things
(files, lines, commits, rows, columns, orgs, events, devices, entities, scenes) or
dates used as data-window boundaries and commit provenance. Dates identifying
*when a commit happened* or *what window telemetry covers* are provenance, not
effort. No durations, story points, t-shirt sizes, or effort scores appear. The
proposed `spike_status` field is categorical with levels defined without reference
to time.

**Does every factual row have a `source`?**
Yes. Every table row and headline number carries either a pasted command, a pasted
SQL/BigQuery query with its result, or a file path. No rows were deleted for
missing provenance, because none were written without it. Two statements are
explicitly marked as *not yet proven* rather than asserted: repo canonicity (§6)
and the PSPDFKit integration (§1.4, inferred from a telemetry event name, flagged
for Phase 1 confirmation).

**Did I report distributions where tenants differ, or did I average?**
No averaging occurred. The only per-tenant numbers presented are org-reach counts
in §4, and they are labelled as org-reach rather than intensity. Phase 2 query
designs in §5.2 specify min/p10/median/p90/max **plus** the full per-tenant table,
and explicitly forbid means for catalog scale.

**Did I mark anything `MECHANICAL` that actually depends on an unmade decision?**
No Phase 3 classification was performed. Pre-emptively: §2.1 flags the risk that
spike-established patterns get marked `MECHANICAL` when the underlying scoping
decision (§2.3) is unmade, which is exactly the failure mode this question guards.
That risk is now recorded before any classification happens.

**Did I fill any field with a plausible guess rather than `UNKNOWN`?**
No. Specifically resisted: repo canonicity left unproven rather than assumed from
the single build target; Linear and Notion marked unprobed rather than assumed
empty; the 64 telemetry-less orgs left unexplained rather than assumed inactive;
build/coverage availability left untested rather than assumed working; the `wifi`
signal explicitly labelled as *not* equivalent to disconnection rather than
promoted into offline evidence.

**Did I run tooling, or did I read and approximate?**
Ran tooling throughout. `scc` was installed (absent at start) and its output pasted
verbatim. All structural counts came from `rg`/`find`/`python3` XML parsing with
the command shown. All tenant facts came from executed MCP queries with results
pasted. The one place reading substituted for tooling — the directory distribution
of `spike/ecat-web` — used `git diff --name-only` piped through `sort | uniq -c`,
shown inline. Two tooling failures are reported as failures rather than worked
around: `gh` unauthenticated, and `rg 'isa = PBXNativeTarget' -A3` returning
nothing (resolved with a different pattern, `rg -o 'PBXNativeTarget "[^"]+"'`).

---

**Phase 0 complete. Stopping here for approval per the brief.**
