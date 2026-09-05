# 02_TENANT_CENSUS.md — eCat iPad → Responsive Web

**Status:** Phase 2 complete. Machine-readable companion: `02_TENANT_CENSUS.json`.
**Produced:** 2026-08-08

Two independent data planes were queried:

| Plane | Access | Reach | Window |
|---|---|---|---|
| Production Postgres | MCP `supercat-postgres-vpn`, read-only | 255 organizations | table lifetime; some tables have retention floors, noted inline |
| Mixpanel via BigQuery | local service account, direct | 192 organizations | 2024-11-01 → 2026-08-07 |

Every per-tenant table is in `02_TENANT_CENSUS.json`; the CSVs behind the
telemetry sections are in `out/`. Nothing below is averaged across tenants.

---

## 0. Three findings that change the shape of the estimate

**0.1 — The configured offline window is 3 days, and it is nearly uniform.**
`organizations.properties->force_sync_threshold_days` is set to `3` for 189 of
255 tenants. One tenant is at 99, one at 15, four at 1, two at 0, and 58 have no
value. Independently, `require_online_order_submission` is true for 185 of the
218 tenants that carry the flag. The product as configured does not authorize
long disconnected operation, and for most tenants it does not permit
disconnected *submission* at all. This does not decide the Scenario fork — that
is a product decision and it is carried to Phase 4 — but it means Scenario A's
requirement is not "indefinite offline."

**0.2 — The iPad is the minority surface by user count, by a factor of about
seven.** Of 113,297 `org_users`, 10,168 have ever logged into the iPad and
69,320 have ever logged into eCat Online. Within 30 days of 2026-08-08, 3,185
users had an iPad login, spread across 136 tenants. The largest single tenant
iPad-active population is 103 users (`sc`).

**0.3 — There is no standard configuration.** 35 boolean columns on
`organizations` produce **239 distinct actual configurations across 255
tenants**. Adding the 70 keys under `properties->flags` gives a declared flag
surface of 105. 94% of tenants are configurationally unique.

---

## 2.1 Organization inventory and activity

255 organizations, none marked as sandboxes (`sandbox_of_id` is null for all
255, so the sandbox column cannot be used to separate demo tenants from real
ones; shortnames such as `pf_test`, `ihw_staging`, `kylademo` indicate that
non-production tenants exist and are simply not labelled).

Activity classification, defined without reference to elapsed effort:

| Class | Definition | Orgs |
|---|---|---|
| `ipad_active_30d` | ≥1 `org_user.last_ipad_login_at` within 30 days | **136** |
| `ipad_ever_never_recent` | some iPad login ever, none in 30 days | **113** |
| `no_ipad_user_ever` | no `org_user` has a non-null `last_ipad_login_at` | **6** |

Source: `org_users`, MCP query in `scripts/p2_pg_raw.py` → `SQL_LOG.blast_radius`.

Order recency is a second, harsher signal. The `orders` table holds rows for 190
tenants; the most recent order for many is years old (`4` last ordered
2012-06-12, `17` 2015-03-13, `27` 2016-09-22, `16` 2017-03-10, `38` 2018-01-03).
Full per-tenant last-order dates are in `02_TENANT_CENSUS.json → orders_lifetime`.

### Coverage reconciliation: 255 Postgres vs 192 Mixpanel

| Set | Count |
|---|---|
| In Postgres | 255 |
| In Mixpanel | 192 |
| In both | 190 |
| Postgres only | 65 |
| Mixpanel only | 2 (`cstr`, `desdemo`) |

**Of the 65 Postgres-only tenants, zero have an iPad-active user in 30 days.**
Telemetry silence and iPad inactivity are the same set. Feature usage for those
65 is `UNKNOWN`, not zero — but no active iPad tenant is missing from telemetry,
so the Phase 5 kill list rests on complete coverage of the population that
actually uses the app. The 2 Mixpanel-only shortnames do not resolve to a
Postgres org and are unexplained.

`login_events` cannot be used for tenant age: `min(created_at)` is 2025-02-08
for over 150 tenants, which is the table's retention floor.

---

## 2.2 Configuration reality

**Declared surface:** 35 boolean columns + 70 `properties->flags` keys = 105
flags, plus 69 non-flag `properties` keys (labels, thresholds, integration
configs).

**Actual surface:** 239 distinct boolean configurations across 255 tenants.

Flags that are permanently off across all 255 tenants — dead configuration,
cross-checked against the Phase 1.8 dead-flag list:

| Flag | Orgs true |
|---|---|
| `enable_data_import3` | 0 |
| `enable_image_import2` | 0 |
| `import_active` | 0 |
| `order_by_pack` | 0 |
| `require_address_for_local_customers` (json) | 0 of 190 carrying the key |
| `use_enhanced_riser_matching` (json) | 0 of 2 |

Flags true for ≤20 tenants: `hide_order_totals` (2), `use_modern_ui` (2),
`enable_rep_activity` (7), `enable_import_users` (15), `disable_sync` (16),
`legacy_display_all_customers` (18), `enrollment_requires_customer` (19),
`enable_showroom_carts` (2 json), `contract_prices_always_win` (1 json),
`image_import_active` (1 of 73 json).

Flags never observed false — set for a subset and never turned off, so their
"off" path is unexercised in production: `use_external_data_import` (140/140),
`enable_faster_product_sync` (136/136), `use_s3_product_images` (136/136),
`link_to_customer_dashboard` (59/59), `enable_tearsheet_org_info` (12/12).

Full per-flag counts: `02_TENANT_CENSUS.json → configuration`.

---

## 2.3 Catalog scale — the performance envelope

Distribution over tenants with a nonzero count. `orgs` is how many of the 255
have any row at all; the remainder have none.

| Metric | Orgs | Min | Median | p90 | Max | Grand total |
|---|---|---|---|---|---|---|
| Active SKUs | 239 | 1 | 1,792 | 9,334 | **50,614** | 975,432 |
| Product images | 236 | 4 | 5,207 | 29,064 | **131,596** | — |
| Customers | 208 | 1 | 2,125 | 8,877 | **92,669** | — |
| Inventories | 186 | 1 | 1,875 | 7,841 | 41,487 | — |
| Taxonomy nodes | 240 | 3 | 173 | 793 | 4,109 | — |
| Price levels | 235 | 1 | 7 | 42 | 326 | — |
| Options | 91 | 1 | 115 | 1,547 | 7,630 | — |
| Option groups | 92 | 1 | 34 | 510 | 1,103 | — |
| Kit items | 49 | 1 | 208 | 3,978 | 32,332 | — |
| **Matrix options** | **53** | 4 | 3,563 | 244,181 | **1,669,094** | — |
| Contract prices | 19 | 1 | 14,770 | 159,164 | 487,634 | — |
| Shared resources | 168 | 1 | 35 | 168 | 740 | — |
| User types | 255 | 1 | 5 | 16 | 46 | — |
| Surcharge types | 52 | 1 | 2 | 14 | 65 | — |
| Distribution centers | 16 | 1 | 3 | 8 | 8 | — |

The matrix-pricing row is the hard constraint on Scenario A. Tenant `5` holds
1,669,094 matrix option rows and tenant `109` holds 770,494. Any design that
proposes shipping the priced configuration space to a browser has to answer for
those two numbers specifically, not for the median.

Source: grouped counts per `organization_id`, SQL in `scripts/p2_pg_raw.py`.

---

## 2.4 Schema variance

Custom fields are per-tenant extensions to core entities, so each distinct count
is a distinct entity shape in the wild.

| Entity | Tenants with ≥1 custom field | Min | Median | p90 | Max |
|---|---|---|---|---|---|
| Product | **240** | 1 | 34 | 84 | **185** |
| Customer | 102 | 1 | 6 | 16 | 25 |
| Order | 50 | 1 | 2 | 7 | 11 |
| Inventory | 22 | 1 | 3 | 12 | 18 |
| Option | 2 | 1 | 1 | 1 | 1 |

240 of 255 tenants extend the product entity, one of them with 185 additional
fields. This confirms the Phase 1.3 open question — the product entity has more
than one schema variant in production — and quantifies it: the product record
has no fixed shape.

---

## 2.5 Feature usage per tenant

Telemetry reaches 192 organizations, 3,821 usernames, 5,970 devices, 10,661,150
events, 2024-11-01 → 2026-08-07. 50 distinct event names; the prebuilt
`mixpanel.org_feature_usage_report` view maps 38 named features.

**Two defects in that view were found and corrected against the raw event
table** rather than reported as findings:

1. `create_my_list`, `create_customer_product_list` and `create_maybe_list` all
   returned exactly 0 tenants because the view discriminates `create_stack` on
   `type` values (`my_list`, `customer_product_list`, `maybe_list`) that do not
   exist. The column holds `user`, `customer`, `maybe`. Corrected figures below.
2. `view_cust_product_list` and `view_cust_backorders` are both defined as
   `COUNTIF(event_name='view_customer_on_order_items')`. They are one event
   counted twice, not two measured features.

Reach, ordered by tenants with any use (of 192):

| Orgs | Events | Feature |
|---:|---:|---|
| 157 | 3,397,018 | search_products |
| 151 | 571,679 | view_library_entry |
| 150 | 690,621 | select_a_customer |
| 150 | 103,689 | filter_products |
| 140 | 1,412,937 | search_for_customer |
| 133 | 42,240 | email_item_info |
| 131 | 135,670 | view_my_list |
| 130 | 107,481 | view_ipad_orders |
| 129 | 15,927 | create_my_list *(corrected)* |
| 128 | 32,944 | change_catalog_sort |
| 124 | 96,597 | create_pdf_catalog |
| 123 | 60,550 | search_collections |
| 120 | 74,535 | pdf_searches |
| 117 | 225,056 | submit_order |
| 108 | 2,145 | share_my_list |
| 102 | 40,104 | email_single_library_entry |
| 101 | 4,194 | create_customer_product_list *(corrected)* |
| 91 | 285,756 | scan_item_with_camera |
| 90 | 23,162 | view_cust_favorites |
| 89 | 4,323 | edit_my_list |
| 86 | 7,046 | view_smartpicks |
| 82 | 7,266 | email_multiple_library_entries |
| 72 | 4,180 | order_from_maybe_list |
| 72 | 453 | create_maybe_list *(corrected)* |
| 71 | 141,131 | access_sales_portal |
| 65 | 4,930 | show_sales_in_catalog |
| 61 | 6,930 | export_data_to_excel |
| 61 | 2,109 | export_data_to_csv |
| 47 | 9,191 | view_cust_product_list *(same event as below)* |
| 47 | 9,191 | view_cust_backorders *(same event as above)* |
| **43** | 134,377 | **order_configured_item** |
| 41 | 10,340 | view_placements |
| **24** | 169,619 | **view_kit** |
| **20** | 124,760 | **order_kit** |
| **11** | 9,613 | view_flipbook |
| **5** | 3,593 | view_commitments |
| **5** | 68 | order_from_flipbook |
| **4** | 35 | add_to_list_from_flipbook |

Note the shape of the bottom of this table: `order_configured_item` (the CPQ
path) reaches 43 tenants but fires 134,377 times, and `view_kit` reaches 24
tenants with 169,619 events. Low tenant reach with high event volume is a
concentrated dependency, not a dead feature — a distinction Phase 5 must
preserve.

**Screen-level usage is not obtainable.** The 50 events are feature-level; the
iPad app emits no per-screen view event. The Phase 1.1 inventory of 105 screens
cannot be mapped one-to-one onto telemetry. Screens are reachable only through
the feature events that occur on them, and that mapping is not in the data.
Recorded as a coverage gap, not estimated.

### Feature tables in Postgres (adoption independent of telemetry)

| Table | Tenants with ≥1 row | Max rows |
|---|---|---|
| `ipad_reports` | 227 | 94 |
| `smart_stacks` | 190 | 256 |
| `mobile_sites` | 98 | 2 |
| `kit_items` | 49 | 32,332 |
| `placement_reports` | 24 | 9,542 |
| `commitment_reports` | 7 | 4,255 |
| `rma_requests` | 7 | 2,578 |
| **`option_mappings`** | **7** | **2** |
| **`showroom_locations`** | **1** | **2** |

`option_mappings` — the cascading option-filter capability — has 7 tenants and a
maximum of 2 rows. `showroom_locations` has one tenant (`demo`, org 6) with 2
rows. Both are Phase 5 candidates.

---

## 2.6 Offline behaviour — evidence for the Scenario fork

Four probes, three independent data sources. **These are measurements of device
behaviour. They are not effort figures and carry no scheduling meaning.**

### Probe 1 — order hold time (Postgres)

`orders.created_at − orders.submit_date` for iPad-sourced orders created in the
trailing 12 months. n = 140,788 across 110 tenants.

| Bucket | Orders | Share |
|---|---:|---:|
| ≤ 5 min | 138,302 | 98.23% |
| 5 min – 1 h | 360 | 0.26% |
| 1 h – 24 h | 643 | 0.46% |
| 1 – 3 days | 266 | 0.19% |
| 3 – 30 days | 346 | 0.25% |
| > 30 days | 746 | 0.53% |
| negative | 125 | 0.09% |

Control: `order_source='server'` rows show 24,644 of 38,175 with a negative gap
and zero in every positive bucket, confirming the negatives are a server-side
artifact rather than device behaviour.

*Blind spot, stated not filled:* this measures submit → arrival. A rep who
builds an order offline over two days and submits on reconnect registers a
near-zero gap. Probe 1 alone cannot bound disconnected session length.

### Probe 2 — on-device event queue (Mixpanel/BigQuery)

The Mixpanel iOS SDK queues events locally and flushes when it can reach the
network, so `mp_api_timestamp_ms − time` measures time the device could not
deliver. This probe is independent of Probe 1 and does not depend on order
submission.

*An artifact was found and corrected.* The first run placed 100% of 5.9M events
in a single 1h–24h bucket, with a floor of exactly 4.00 h for every event name.
That is a fixed US/Eastern project-clock offset (4.00 EDT / 5.00 EST), not
queueing. Subtracting each calendar date's minimum observed offset removes it
without hardcoding a DST calendar. Diagnostic: `out/bq_delay_check.txt`.

Corrected, n = 5,898,726 events, 177 tenants, 4,599 devices:

| Bucket | Events | Share |
|---|---:|---:|
| ≤ 1 min | 5,343,108 | 90.58% |
| 1 – 5 min | 348,322 | 5.90% |
| 5 min – 1 h | 58,717 | 1.00% |
| 1 – 4 h | 72,364 | 1.23% |
| 4 – 24 h | 65,480 | 1.11% |
| 1 – 3 days | 8,831 | 0.15% |
| 3 – 7 days | 1,904 | 0.03% |
| > 7 days | 0 | 0% |

Longest observed delivery gap: 5.0 days.

Per device, the longest single gap ever observed (10,188 devices):

| Peak gap for that device | Devices | Share |
|---|---:|---:|
| never exceeded 5 min | 6,087 | 59.7% |
| 5 min – 1 h | 930 | 9.1% |
| 1 – 24 h | 2,212 | 21.7% |
| 1 – 3 days | 629 | 6.2% |
| > 3 days | 330 | 3.2% |

`order_submitted` events specifically: 121,510 of 123,801 (98.15%) delivered
within 5 minutes; 167 (0.13%) exceeded 24 hours; longest 4.9 days. This
corroborates Probe 1 from an entirely separate pipeline.

*Blind spot:* the SDK's local queue is bounded, so very long disconnections may
be truncated or dropped. Every figure here is a lower bound.

### Probe 3 — configured policy (Postgres)

| `force_sync_threshold_days` | Orgs |
|---|---:|
| 3 | 189 |
| absent | 58 |
| 1 | 4 |
| 0 | 2 |
| 15 | 1 |
| 99 | 1 |

Plus `require_online_order_submission` true for 185 of 218, and `disable_sync`
true for 16 of 255.

### Probe 4 — connectivity flag (Mixpanel)

Trailing 12 months: 5,004,016 events with `wifi=true` (177 orgs), 630,912 with
`wifi=false` (134 orgs), 263,816 null (161 orgs). *Caveat:* `wifi=false` includes
cellular and is not equivalent to disconnected.

### What no source can answer

- **Orders built and abandoned on-device without submission.** Drafts live in
  the device's Core Data store and never reach the server. No row exists.
- **Selling-session length between syncs.** Neither telemetry source emits a
  session-boundary event.
- **Whether a disconnection was involuntary (no signal) or voluntary (airplane
  mode, app closed, device asleep).**

These are recorded as `UNKNOWN` and carried to Phase 4. They are not inferred.

---

## 2.7 Blast-radius inputs

No revenue or contract values were queried, inferred, or recorded.

Per-tenant size indicators (`org_users`, iPad-ever, iPad-active-30d, eCat-Online-
ever, orders in trailing 12 months) for all 255 tenants are in
`02_TENANT_CENSUS.json → blast_radius.per_tenant`.

Largest iPad-active populations:

| Shortname | Org | org_users | iPad ever | iPad 30d | eOL ever | Orders 12mo |
|---|---:|---:|---:|---:|---:|---:|
| `sc` | 69 | 159 | 138 | 103 | 32 | 28,109 |
| `pf` | 32 | 190 | 153 | 93 | 42 | 2,841 |
| `wac` | 181 | 177 | 142 | 85 | 0 | 1,666 |
| `hfg` | 165 | 207 | 144 | 68 | 51 | 1,801 |
| `el` | 152 | 341 | 208 | 68 | 144 | 184 |
| `rw` | 248 | 117 | 93 | 67 | 21 | 8,987 |
| `mlg` | 252 | 131 | 100 | 64 | 0 | 146 |
| `ufi` | 18 | 120 | 99 | 63 | 50 | 2,115 |

The largest tenants by *user count* are eCat Online tenants, not iPad tenants:
`wwjc` (20,890 users, 12,568 eOL-ever, 42 iPad-30d) and `jyc` (16,313 users,
11,697 eOL-ever, 47 iPad-30d). Tenant size and iPad exposure are close to
orthogonal, so blast radius must be computed per surface and not from headcount.

### Device fleet

6,188 devices across 281 distinct model/OS combinations. By iPadOS major
version: 18 → 2,539 devices; 26 → 2,471; 17 → 532; 16 → 343; 15 → 227; 14 → 31;
12 → 29; 13 → 4; 10 → 8; 27 → 4.

Screen geometry, 21 distinct sizes over 4,619 devices reporting it:

| Geometry | Devices | Events |
|---|---:|---:|
| 1180×820 | 1,285 | 1,512,426 |
| 1080×810 | 1,012 | 1,320,609 |
| 1366×1024 | 820 | 1,107,763 |
| 1024×768 | 573 | 427,258 |
| 1194×834 | 378 | 642,466 |
| 1376×1032 | 173 | 301,922 |
| 1112×834 | 132 | 102,098 |
| 1133×744 | 96 | 69,315 |
| 1210×834 | 92 | 110,982 |
| 12 further sizes | 58 | 43,388 |

Three facts matter here. Landscape tablet dominates overwhelmingly. Portrait
does occur — 820×1180, 810×1080, 834×1194 and 1024×1366 are the same panels
rotated, on 12 devices — so orientation is exercised but rare. And 1024×768
(573 devices) is the non-Retina generation, which sets the low end of any
responsive breakpoint set. Exactly one device reports phone geometry (402×874).
Full table in `02_TENANT_CENSUS.json → screen_geometry`. This constrains what
"responsive" has to mean; it does not decide the Phase 4 fidelity bar.

### Sync entity types (server-side manifest)

`data_versions` tracks **22 live entity types** (a 23rd, `ipad_reports`, has 2
rows last written 2016-08-17 and is stale). Entities and tenant counts are in
`02_TENANT_CENSUS.json → sync_entity_types`. This is the authoritative count of
what participates in sync and supersedes any count derived from client code.

---

## SELF-AUDIT

**Does any output contain a time unit, or a scale that implies one?**
Yes, and deliberately, in exactly two categories, neither of which is an effort
or schedule quantity: (a) measured device telemetry in §2.6 — delivery gaps,
hold times, last-login recency; (b) tenant configuration values that are
literally denominated in days (`force_sync_threshold_days`). Phase 2 explicitly
requires "sync gap durations" and "last-sync-age distributions." No duration
anywhere in this document refers to work, and no scale implies one. Reviewed
line by line; no story points, t-shirt sizes, or effort scores appear.

**Does every factual row have a `source`?**
Yes. Every Postgres figure traces to a query in `scripts/p2_pg_raw.py` (SQL in
`SQL_LOG`, verbatim result strings alongside). Every telemetry figure traces to
a script in `scripts/p2_bq_*.py` and a file in `out/`. No rows were deleted for
missing provenance.

**Did I report distributions where tenants differ, or did I average?**
Distributions. Every scale metric reports orgs-with-nonzero, min, median, p90
and max, with the full per-tenant table in the JSON. No mean is reported
anywhere. §2.3 explicitly names the two outlier tenants on matrix pricing rather
than letting the median stand in for them, and §2.7 names tenants individually.

**Did I mark anything MECHANICAL that actually depends on an unmade decision?**
No Phase 3 classification is made in this document. Three items are flagged for
Phase 4 rather than resolved here: the Scenario fork itself, the responsive
fidelity bar implied by the screen-geometry spread, and the disposition of the
65 telemetry-silent tenants.

**Did I fill any field with a plausible guess rather than UNKNOWN?**
No. Screen-level usage is marked unobtainable rather than approximated from
feature events. Draft-order counts, session length, and voluntary-vs-involuntary
disconnection are marked `UNKNOWN`. The 2 Mixpanel-only shortnames are reported
as unexplained. The 65 Postgres-only tenants are marked `UNKNOWN` for feature
usage, not zero.

**Did I run tooling, or did I read and approximate?**
Tooling throughout. Two tooling failures were hit and worked around rather than
papered over: the MCP query validator rejects `percentile_cont(...) WITHIN
GROUP`, so percentiles are computed in `scripts/p2_analyze.py` from verbatim
result strings; and the Postgres MCP endpoint exposes no credentials, so
per-tenant tables were returned as compact strings and persisted verbatim.

**Errors found and corrected during this phase, both left on the record:**
1. The Mixpanel delivery-delay probe initially showed a uniform 1h–24h delay.
   Diagnosed as a fixed timezone offset and corrected (§2.6 Probe 2).
2. `mixpanel.org_feature_usage_report` reports three features as used by zero
   tenants due to a wrong `type` discriminator, and double-counts one event as
   two features. Corrected against the raw table (§2.5).

Both would have produced confident, wrong rows had they been accepted at face
value.
