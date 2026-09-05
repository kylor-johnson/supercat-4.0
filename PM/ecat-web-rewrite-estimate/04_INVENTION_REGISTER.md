# 04_INVENTION_REGISTER.md — eCat iPad → Responsive Web

**Produced:** 2026-08-08. Inputs: `01_CODE_CENSUS.json`, `02_TENANT_CENSUS.json`,
`03_UNIT_LEDGER.json`, `scripts/registry.json`, `scripts/spike.json`,
`out/p4_downstream.txt`.

Every item below is a decision a human must make. For each: the question, what is
already determined so the decision-maker is not re-deriving it, what sits
downstream with LOC and tenant counts, and whether evidence that would resolve it
is obtainable from the codebase, the tenants, or neither.

Downstream rollups are computed, not asserted — `scripts/p4_downstream.py` sums
them over Phase 3 ledger rows, output in `out/p4_downstream.txt`.

---

## Group A — Scenario and target. Everything else inherits these.

### IR-01 — Does the web application sell while disconnected?

**Decision:** Adopt Scenario A (offline parity) or Scenario B (connected-only,
iPad remains in service for disconnected use)?

**Already determined:**

- There is no conflict-resolution engine to port. Phase 1.4 found zero conflict,
  last-write-wins, tombstone, etag or vector-clock branches in the 3,935-LOC sync
  unit, and `_sync-protocol.yaml` (517 lines) independently describes a one-way,
  server-authoritative protocol: products sync incrementally, **all other entity
  types are full-replacement** — "download everything and replace local data."
- **Configured policy forbids extended disconnection for most tenants.**
  `force_sync_threshold_days` is 3 for 189 tenants, 1 for 4, 0 for 2, 15 for 1,
  99 for 1, absent for 58. `require_online_order_submission` is set by 218
  tenants: **true for 185, false for 33**. `disable_sync` is true for 16.
- **Measured disconnection is mostly short, with a real tail.** Of 140,788
  iPad-sourced orders in the trailing 12 months, 138,302 were submitted within 5
  minutes of creation; 643 fell in 1–24 hours, 266 in 1–3 days, 346 in 3–30 days
  and 746 beyond 30 days. The independent telemetry probe agrees in shape: of
  5,898,726 events, 5,343,108 arrived within 1 minute, but per-device peaks show
  **6,087 of 10,188 devices never exceeded 5 minutes while 2,212 peaked in the
  1–24 hour band, 629 in 1–3 days and 330 beyond 3 days**. Both are lower bounds.
- **A documented decision already exists, scoped to a pilot.**
  `docs/design/ecat-web-spike.md` (`supercat_server origin/spike/ecat-web`)
  states that the prior plan's "SQLite-in-the-browser with a sync engine" phase is
  "the opposite of the no-sync, fully web-based direction" and is **superseded by
  this spike**. That is Scenario B, decided for one pilot organization — not for
  the 255-tenant fleet, and not as a decision to retire the iPad.

**Downstream:** 8 of 34 units change `port_class` between scenarios — 21,772 LOC,
14,743 of it LOGIC. Scenario A carries **5 INVENTION units / 20,668 LOC**;
Scenario B carries **1 / 3,935 LOC**. The countable delta is 4 units and 16,733
LOC of invention.

**Evidence that would resolve it:** **Neither.** This is a product and commercial
decision. The tenants have already answered the closest measurable proxy — most
forbid offline submission by configuration — but 33 tenants permit it and 330
devices show multi-day telemetry gaps, so the data constrains the decision without
making it. One blind spot cannot be closed by any query available here: Probe 1
measures the gap between order creation and submission, not the session a rep
spends *composing* offline before reconnecting. A rep who builds for two days and
submits on reconnect registers a near-zero gap.

**Note the tension.** In Phase 0 this was left open at your direction. A
documented decision has since been found on the spike branch. Those are
reconcilable — one pilot org on a connected surface does not decide the fleet —
but the register should not present as open a question that someone may consider
closed.

### IR-02 — When the device and the server disagree, who wins?

**Decision:** Specify merge and conflict semantics. Under Scenario A, for
bidirectional sync. Under Scenario B, a freshness, cache-invalidation and reload-
granularity policy is still required.

**Already determined:** 22 server-side entity types are versioned through
`data_versions`, each covering 235–253 tenants. A full sync deletes all rows by
`organizationID` and re-downloads. Products carry `transaction_type='U'`/`'D'`
for incremental update and soft-delete. Order lifecycle is documented as
draft → queued → submitted, with retry on next network availability and a
partial-acceptance path. Nothing anywhere specifies what happens when two writers
disagree, because today only one writer exists.

**Downstream:** `Sync`, 3,935 LOC (2,540 LOGIC), 255 tenants, `SPINE`,
`CUTOVER_ONLY`, **0 test files**, fan-in 5 / fan-out 6.

**Evidence that would resolve it:** **Neither.** No amount of code reading
produces semantics that were never designed. This is the item most likely to be
mistaken for `RESPECIFICATION`, and it is `INVENTION` under both scenarios.

### IR-03 — What is the rewrite target?

**Decision:** A new surface, an extension of `spike/ecat-web`, or eCat Online
brought to parity? And does the iPad application remain in service?

**Already determined:**

- eCat Online already exists as a web surface (`ecat_online`, `ecat_products`,
  `ecat_orders`, `mobile_sites` controllers).
- `spike/ecat-web` is 34 commits and 249 files ahead of its merge-base, 57,588
  lines added. **9 units are `PARTIALLY_BUILT`.** But the slice is thin: only
  about 4,000 of those lines are unit-attributable application code — 34,138 are
  design documentation and 16,280 the design system and CSS. Per unit:
  `Order related` 1,277, `Left Nav` 694, `Kit/Options related` 547,
  `Grid view related` 491, `SingleItemView related` 471, `Customer` 292,
  `Scan Groups` 159, `Pricing` 74.
- The approach is documented as evolving eCat Online via a `_v2` template overlay
  behind an **org-level** feature flag, one pilot org, with the sales portal
  covered by the same pass and the existing ~6,300-line tablet-first stylesheet
  deliberately not loaded.
- The iPad app is a minority order surface already: in the trailing 12 months
  140,796 orders came from iPad across 110 tenants and 40,019 from the server
  across 33.

**Downstream:** all 34 units, 86,463 LOC. This item sets whether `spike_status`
credit applies at all.

**Evidence that would resolve it:** codebase and tenants have both been read as
far as they go; the remaining input is a product decision about the iPad's future.

---

## Group B — Scenario-A-conditional inventions. Void if IR-01 resolves to B.

### IR-04 — May an order be submitted from a disconnected browser?

**Decision:** Does the web app permit offline order construction and queued
submission, given that 185 of the 218 tenants who set the flag forbid it?

**Already determined:** The mechanism is specified — `workflows/order-creation.yaml`
documents the full state machine including the queued state, retry on network
availability, and partial acceptance. So this is not "how would queuing work." It
is whether to build a capability that most tenants have configured off.

**Downstream:** `Order related`, 13,531 LOC (**9,902 LOGIC**, the largest logic
concentration in the codebase), 117 tenants, `MULTI_SURFACE`, 7 test files.
`INVENTION` under A, `RESPECIFICATION` under B.

**Evidence:** from the tenants, already gathered and decisive in shape (185 vs
33). The decision is whether to serve the 33.

### IR-05 — Does configurable-product pricing evaluate on the server or in the browser?

**Decision:** For Scenario A, how does CPQ reach a disconnected client — or does
it not?

**Already determined:** `matrix_options` totals 4,865,643 rows across 53
tenants, distributed min 4, p10 52, **median 3,563, p90 244,181, max 1,669,094**
(tenant `5`; tenant `109` holds 770,494). `kit_items` totals 78,222 across 49
tenants, max 32,332. `options` totals 47,264 across 91 tenants, max 7,630. The
spike already evaluates matrix pricing server-side (`matrix_grid_presenter`,
`_matrix_grid_v2`, 547 lines).

**Downstream:** `Kit/Options related`, 2,982 LOC (**76.9% LOGIC**, the highest
logic share of any substantial unit), 43 tenants, **0 test files**. Reach is
narrow but intense: `order_configured_item` fires 134,377 times across those 43.

**Evidence:** the scale numbers are measured and sufficient. Whether a
1.67-million-row pricing matrix can or should reach a browser is an architecture
decision, not a measurement.

### IR-06 — Which browser storage engine, and is the migration history in scope?

**Decision:** For Scenario A, what replaces two local persistence stacks, and does
the existing migration history need to be reproduced?

**Already determined:** The iPad runs **two** local stacks. Core Data: 19 model
versions, 18 inter-version migrations, 3 entities in the version actually in force
(`eCat 20260425`), 221 call sites across 49 files. SQLite via FMDB: 63 migration
files, 1,577 SQL lines, 47 tables created, 151 call sites across 34 files. The
superseded plan proposed SQLite-in-the-browser. The scale that would have to land
locally is measured: active SKUs median 1,792 / p90 9,334 / max 50,614, and
2,851,826 product images in total with a max of 131,596 for one tenant.

**Downstream:** `Database Migration` (177 LOC) and `Core Data Support` (43 LOC),
both `SPINE`, both `CUTOVER_ONLY`, both 255 tenants. **LOC badly understates
these two** — they are driver code for the migration corpus and call-site anchors
above. This is the largest single scenario asymmetry in the ledger: under B both
units are `MECHANICAL` and largely disappear; under A both are `INVENTION`.

**Evidence:** obtainable from neither. Browser storage quota behaviour could be
measured by a spike, which does not exist for this question.

---

## Group C — Port hazards requiring a product decision.

Five hazards are present in the code and have no default web equivalent. Three
further hazards carry `REQUIRES_PRODUCT_DECISION` in Phase 1.6 but have **zero
call sites** — `sqlite_vec_vector_search`, `coreml_on_device_embeddings`,
`background_tasks` — so they are not open items; the capability is unused.

| # | Hazard | Call sites | Files | Units | Downstream LOC | Max tenants |
|---|---|--:|--:|--:|--:|--:|
| IR-07 | `core_data_local_persistence` | 221 | 49 | 6 | 43,926 | 255 |
| IR-08 | `popover_presentation` | 32 | 16 | 8 | 45,241 | 255 |
| IR-09 | `local_filesystem` | 66 | 19 | 8 | 41,874 | 255 |
| IR-10 | `device_orientation` | 8 | 3 | 3 | 25,038 | 255 |
| IR-11 | `split_view_ipad_multitasking` | 23 | 9 | 3 | 22,777 | 255 |

**IR-07** is the same decision as IR-06 seen from the call-site side, and it is
listed separately because its blast radius is wider than the two persistence
units: it reaches `Order related`, `Global classes`, `Data objects`, `Customer`,
`Kit/Options related` and `Categories`.

**IR-08 — what replaces a popover?** 32 call sites across 8 units, including two
units whose keep/kill decision is itself open (`ShowroomCart`, `Flipbook`). On a
1024×768 viewport a popover is viable; on a phone it is not. Downstream of IR-16.

**IR-09 — what is the local file store for?** 66 call sites. The sync engine
writes NDJSON streams and zip archives; presentations write PDFs; images cache
locally. Under Scenario B most of this evaporates; under A it needs a browser
equivalent.

**IR-10 and IR-11 — is rotation supported, and is side-by-side multitasking?**
Small call-site counts, large downstream LOC, because both hazards sit in
`Global classes` and `Grid view related`. Phase 2.7 measured 12 devices operating
in portrait out of 4,619 reporting geometry, and `ShowroomCart` — 2 tenants — is
the only unit whose *purpose* involves split view.

**Evidence for all five:** call sites are measured and complete. What each should
become on the web is a design decision, downstream of IR-16.

---

## Group D — Keep or kill. These precede any port classification.

Four units are classified `REQUIRES_PRODUCT_DECISION` rather than given a port
class, because deciding to port them at all comes first. All four are
`ISOLATED`, all four have `UNDECIDED` fidelity bars, and none has a test file
except `ShowroomCart` (1).

| # | Unit | LOC | LOGIC | Tenants | Registry coverage | Note |
|---|---|--:|--:|--:|---|---|
| IR-12 | `ShowroomCart` | 1,014 | 788 | **2** | NONE | Only unit whose purpose needs split view |
| IR-13 | `Commitments` | 510 | 349 | **5** | NONE | Registry references `commitments-view` but never registers it |
| IR-14 | `Flipbook` | 510 | 368 | **11** | REFERENCED | Carries PDF-render and popover hazards |
| IR-15 | `SemanticSearch` | 456 | 251 | **13** | NONE | On-device embedding and vector-search hazards both have 0 call sites |

**Total: 2,490 LOC, 1,756 of it LOGIC, none reaching more than 13 of 255
tenants.**

**Already determined:** the tenant counts above are measured usage, not
entitlement. `SemanticSearch` is additionally the only unit whose two nominal
hazards are entirely unexercised, which suggests it is unfinished rather than
merely unpopular — Phase 5 ranks it.

**Evidence:** obtainable from the tenants and already gathered. The named tenants
are in `05_KILL_LIST.md`. The decision to migrate or drop them is commercial.

---

## Group E — Fidelity and contested specification.

### IR-16 — What is the responsive fidelity bar, per unit?

**Decision:** Which form factors are targets, and what is the acceptance standard
for each unit — outcome equivalence, behaviour parity, or visual parity?

**Already determined:**

- **21 distinct screen geometries across 4,619 devices.** Landscape tablet
  dominates: 1180×820 (1,285 devices), 1080×810 (1,012), 1366×1024 (820),
  1024×768 (573), 1194×834 (378). **1024×768 is the non-Retina generation and
  sets the low end.** 12 devices run portrait. Exactly one reports phone geometry
  (402×874).
- The spike has decided *part* of this: `docs/design/ecat-web-spike.md` states the
  work is "a **full UX redesign**, not a responsive patch," which rules out
  visual parity for spike-covered units, and it ships both `_desktop_shell_nav`
  and `_phone_shell_nav`. The same document states that "detailed UX/interaction
  design from a designer is still needed for the full vision."

**Downstream:** **11 units, 25,029 LOC, 15,627 LOGIC** carry
`fidelity_bar: UNDECIDED` — `Grid view related`, `Sync`,
`SingleItemView related`, `Left Nav`, `Custom UI controls`, `ShowroomCart`,
`Commitments`, `Flipbook`, `ActionPopover`, `SemanticSearch`,
`Spreadsheet Import`. IR-08, IR-10 and IR-11 are all downstream of this item.

**Evidence:** the device distribution is measured and complete. The target set is
a product decision; the per-unit acceptance standard needs a designer, which the
spike document itself identifies as an open dependency.

### IR-17 to IR-20 — Four units where the documentation and the code disagree

`CONTESTED` is a stronger claim than `CODE_ONLY`: a specification exists **and**
conflicts with the implementation, so someone must declare which is authoritative
before the behaviour can be ported.

| # | Unit | LOC | Tenants | The disagreement |
|---|---|--:|--:|---|
| IR-17 | `Data objects` | 10,955 | 255 | `_data-model.yaml` documents a fixed 40-table / 4-entity shape. **240 tenants carry product custom fields — median 33.5, p90 84.1, max 185, 9,641 in total**; 102 carry customer custom fields up to 25. No fixed shape exists in production. |
| IR-18 | `Grid view related` | 10,461 | 157 | Documentation states 6 product images. 12 are available under the paid `enable_twelve_product_images` flag. |
| IR-19 | `Pricing` | 880 | 235 | KB describes per-browser "My Account" markup rules that belong to eCat Online, not the iPad, where visibility is governed by user group. The registry names **1 of 18** Pricing files. Tenant configuration diverges hard: price levels up to 326, 53 tenants on matrix pricing, 19 on contract prices, 52 on surcharges. |
| IR-20 | `Query` | 160 | 190 | SmartList item lists are documented comma-separated; the importer and app expect newline-separated. |

**IR-17 is the consequential one.** `Data objects` is `SPINE`, `CUTOVER_ONLY`,
fan-in 20, and reaches all 255 tenants. The decision — fixed schema, EAV, or
per-tenant extension — determines the data layer of the entire web application,
and it cannot be read off the iPad code because the iPad code assumes a shape the
tenants do not actually share.

**Evidence:** obtainable from the tenants for all four, and already gathered. Each
needs an owner to declare which behaviour is correct.

---

## Group F — Unresolved unknowns and evidence gaps.

These are not product decisions. They are places where the analysis could not
measure something and refused to guess.

### IR-21 — `Spreadsheet Import` is unclassifiable on current evidence
327 LOC, 198 LOGIC, 100% Swift, 0 tests. **No telemetry event and no Postgres
table maps to it**, so `port_class`, `blast_radius`, `reversibility` and
`tenants_touched` are all `UNKNOWN`. *Resolvable from:* the codebase, by tracing
its entry point; or from a tenant instance if a usage signal can be identified.

### IR-22 — `Notifications` reach is unmeasured
109 LOC, the smallest classified unit. `tenants_touched: UNKNOWN`. The
`view_notifications` event (114 tenants) belongs to `SuperCat Notices`, a
different unit. *Resolvable from:* neither, as instrumented — push delivery is not
in the telemetry schema.

### IR-23 — The specification is incomplete and already stale
The registry self-reports status `needs_attention`: 10 broken dependency
cross-references and **3 components referenced but never registered** —
`action-popover`, `order-list`, `commitments-view`. Two of those three correspond
to open items already (`ActionPopover` carries `UNDECIDED` fidelity;
`Commitments` is IR-13). It is dated 2026-04-03 and documents 4 Core Data
entities against 3 in the model in force, so it lags the code by at least one
entity. *Resolvable from:* the codebase, by re-validating the registry.

### IR-24 — Linear and Notion were never probed
Recorded as a Phase 0 gap and still open. This matters more after Amendment 2 than
before: the iPad specification turned out to live in a repository nobody expected,
so the remaining `CODE_ONLY` population of **17 units / 9,609 LOC** may be
further reduced by documents in a tracker. *Resolvable from:* those systems
directly.

### IR-25 — Repository canonicity is unproven
`gh` is unauthenticated, so `sarreid_ios` could not be confirmed as the canonical
eCat iOS repository rather than one client fork. Circumstantial evidence favours
canonical — a single `eCat` build target, runtime org selection across 191
tenants, a global themes plist. *Resolvable from:* the codebase, with
`gh auth login`, or by your confirmation.

### IR-26 — The spike's performance evidence does not cover production scale
`docs/superpowers/specs/2026-08-01-ecat-a12-performance-results.md` records
measured p95 budgets for the catalog index and the scan endpoint, but explicitly
against "a representative small catalog" of **about 25 products**, and states that
a re-run against a pilot org with real product counts is required before the
production flag is enabled. Measured production scale is median 1,792 active SKUs,
p90 9,334, max 50,614 — so the validated envelope is roughly two orders of
magnitude below the median tenant. This is a gap in the spike's evidence, not a
defect in the spike. *Resolvable from:* the tenants, by re-running the existing
test against a real catalog.

---

## Coverage of this register

| Group | Items | Nature |
|---|--:|---|
| A — Scenario and target | 3 | Product decisions; everything inherits them |
| B — Scenario-A-conditional inventions | 3 | Void if IR-01 resolves to Scenario B |
| C — Port hazards | 5 | Design decisions, call sites measured |
| D — Keep or kill | 4 | Commercial decisions, tenants named |
| E — Fidelity and contested spec | 5 | 1 fidelity bar + 4 documented conflicts |
| F — Unresolved unknowns | 6 | Evidence gaps, not decisions |

Composition is given so the count can be recomputed under a narrower definition.
The brief's literal scope — units classed `INVENTION`, units carrying
`REQUIRES_PRODUCT_DECISION`, and unresolved `UNKNOWN`s — yields **20** items
(Groups A through D plus IR-16, IR-21 and IR-22). The four `CONTESTED` units are
included here because a specification that disagrees with the implementation is an
unmade decision by any useful definition, and IR-23 through IR-26 are included
because they are gaps that block classification rather than gaps in taste.

**Open invention items: 26.**

**N — not a padded percentage — is the width of this estimate's uncertainty.**
Each of the 26 is a question no amount of further code reading or tenant querying
will answer on its own; 20 of them require a human to decide something, and 6
require evidence that has not been gathered. The estimate should not be treated as
converged while N is large.

Two properties of N matter more than its size. First, it is **top-heavy**: IR-01
alone reclassifies 8 units and 21,772 LOC and voids or activates all three Group B
items, so resolving one item collapses a disproportionate share of the range.
Second, IR-02 survives every resolution — the sync engine is `INVENTION` under
both scenarios, so no answer to IR-01 removes it.

---

## SELF-AUDIT

**Does any output contain a time unit, or a scale that implies one?**
No. Quantities here are counts (units, LOC, tenants, call sites, files, rows,
events, devices, orders, geometries) or categorical levels. Three sources
contained time quantities and none was carried forward: `force_sync_threshold_days`
appears as a **configuration value tenants have set**, which is a property of the
fleet and not an effort quantity; the spike document states a team size and a
timebox, disclosed in IR-03 and IR-26 without the figures; and the performance
doc states p95 budgets, referred to in IR-26 without the numbers. The order-gap
and telemetry-delay buckets in IR-01 are elapsed-time *observations of production
behaviour* — they are the measurement the fork turns on, and they describe tenant
conduct, not work.

**Does every factual row have a `source`?**
Yes, by inheritance and by name. Every count traces to `01_CODE_CENSUS.json`,
`02_TENANT_CENSUS.json`, `03_UNIT_LEDGER.json`, `scripts/registry.json` or
`scripts/spike.json`, each of which carries per-row provenance; downstream
rollups are reproducible via `scripts/p4_downstream.py` into
`out/p4_downstream.txt`. Documentary claims name the file
(`_sync-protocol.yaml`, `workflows/order-creation.yaml`,
`docs/design/ecat-web-spike.md`,
`docs/superpowers/specs/2026-08-01-ecat-a12-performance-results.md`) and the
branch it lives on. No row was dropped for missing provenance.

**Did I report distributions where tenants differ, or did I average?**
Distributions throughout, and deliberately so where the distribution *is* the
argument. IR-01 reports the full order-gap and per-device-peak buckets rather than
a central figure, because the tail — 746 orders beyond 30 days, 330 devices
peaking beyond 3 days — is the entire case for Scenario A and a mean would erase
it. IR-05 and IR-17 name outlier tenants individually (`5`, `109`) and give
min/p10/median/p90/max. IR-16 gives per-geometry device counts. The only means in
this document are the medians and percentiles carried from Phase 2, always beside
their min and max.

**Did I mark anything MECHANICAL that actually depends on an unmade decision?**
This register is the check, and it caught one class of error in Phase 3: four
units that a naive pass would have port-classified were escalated to
`REQUIRES_PRODUCT_DECISION` instead, because keep-or-kill precedes porting
(Group D). Going the other way, Amendment 2 to Phase 3 discovered a specification
for 11 units and **no unit was upgraded to MECHANICAL as a result** — a document
describing iPad behaviour is not a known web equivalent. `MECHANICAL` remains the
smallest bucket in the ledger.

**Did I fill any field with a plausible guess rather than UNKNOWN?**
No. Group F exists precisely to hold what could not be measured: two units with
unmeasured tenant reach, one of which is fully `UNKNOWN` on four axes; a
specification known to be incomplete and stale; two systems never probed; and one
performance claim whose validity envelope is two orders of magnitude below
production scale. Each is stated as a gap with a named resolution path rather than
closed with an estimate.

**Did I run tooling, or did I read and approximate?**
Downstream LOC and tenant rollups were computed by `scripts/p4_downstream.py` over
the ledger rather than added by hand. Hazard call sites, unit LOC, tenant
distributions and spike line counts are all carried from executed tooling.
Reading was used for exactly one purpose — extracting the *decisions* recorded in
the spike's design documents, which is not a countable quantity and cannot be
measured. Those passages are quoted and their file paths given so they can be
checked.
