---
name: ecat-ipad-app
description: >-
  How the eCat iPad app works at runtime — sync, local SQLite, User Group permissions,
  territory customer filtering, on-device pricing, options/matrix, SmartLists, and order
  submission. Use when diagnosing rep-facing iPad behavior ("wrong price", "customers
  disappeared", "SmartList missing", "sync stuck", "order won't submit"), explaining how
  Admin settings affect what reps see, or distinguishing iPad from eCat Online / Sales
  Portal. For CSV builds and imports, use ecat-core-files / ecat-ground-truth instead.
---

# eCat iPad App — Runtime Behavior

Scope: **the native eCat iPad app** (`sarreid_ios/eCatalog/`) and the server APIs it
calls. **Not** eCat Online (eOL) — owned by `ecat-online`; **not** Sales Portal —
owned by `ecat-sales-portal-onboarding`; **not** Admin import mechanics — those are
`ecat-core-files` + the `ecat-import-ops` rule. Those are separate surfaces with
different pricing and auth rules.

Always-on import rules (`ecat-ground-truth`, `ecat-data-model`) still apply when the
root cause is bad/missing imported data. This skill explains what happens **after** data
is loaded and a rep opens the app.

## Mental model

The iPad is an **offline-first catalog + order writer**:

1. Rep logs in → app **syncs** changed entities from `supercat_server`.
2. Sync streams JSON/plist into **local SQLite** on the device (`BuildsDataObjects.m`).
3. Browse, price, configure options, and draft orders **entirely on-device**.
4. Submit sends `POST /:org/orders.json`; server validates, stores, and may export to ERP.

There is **no full-catalog prebuilt SQLite on the server**. The only server-built DB is
**matrix options** (`BuildsIpadDatabases` → zip → `matrix_options/prebuilt.json`). Everything
else is assembled on the iPad during sync.

## Boundaries (stop misrouting)

| Surface | What it is | iPad skill applies? |
|---------|------------|---------------------|
| **eCat iPad** | Rep catalog, presentations, order writing | **Yes** |
| **eCat Online (eOL)** | Buyer web catalog, Cart, "My Account" markup pricing | **No** — owned by `ecat-online` |
| **Sales Portal** | ERP-fed order/invoice history inside eOL | **No** — owned by `ecat-sales-portal-onboarding` (`order_data.csv` / `invoice_data.csv`) |
| **Admin Console** | Config + imports | Partially — settings here **drive** iPad behavior |
| **Portal orders in DB** | `order_source = 'server'` | Not iPad-submitted orders |

When a ticket mentions "web works but iPad doesn't" (or the reverse), **split the
diagnosis** — do not apply eOL KB articles to iPad pricing.

## The rep journey

```
Login → Sync (Wi‑Fi) → Browse catalog → [optional Smart Stack] → Select customer
  → Price level defaults → Configure options → Build order → Submit → Server export
```

**First-line support:** most "I don't see X" tickets resolve with **sync on Wi‑Fi** +
confirm the rep's **User Group** (not `DefaultUserGroup`) + confirm **territory codes**
align between rep profile and `customers.csv`.

## Sync — how data reaches the iPad

### Orchestration

1. iPad calls `GET /:org/api/modified_entities.json?previous_version=&modified_after=`.
2. `DataVersion` returns per-entity change counts + `current_version`.
3. Non-zero counts trigger re-download of that entity's endpoint.
4. Device rebuilds local tables, then downloads **product/option images** separately.

Key server files: `api_controller.rb`, `data_version.rb`. Key iOS files: `Synchronizer.m`,
`BuildsDataObjects.m`, `SyncController.m`.

### What gets downloaded (representative URLs from `Synchronizer.m`)

| Entity | Endpoint |
|--------|----------|
| Products | `products.json` |
| Customers | `customers.json` |
| Smart stacks | `smart_stacks.json` |
| Price levels | `price_levels.plist` |
| Options / groups | `options.plist`, `option_groups.plist` |
| Inventory | `inventories.json` |
| Matrix options | `matrix_options/prebuilt.json` (SQLite zip) |
| Org config | `organizations.plist` |
| Contract / riser prices | `contract_prices.json`, `riser_prices.json` |

### Sync can be blocked or incomplete when

| Condition | Effect |
|-----------|--------|
| Org `disable_sync` (non-admin rep) | Sync refused |
| Org status sync-suspended / fully suspended | Sync refused |
| Rep `allow_ipad_logins = false` on User Group | Login blocked |
| Rep never synced after last import | Stale catalog/customers/prices |
| User stuck in `DefaultUserGroup` | Permissions/territory filters never apply |
| `perform_full_synch` / `full_synch` flag on org_user | Forces full re-download |

**Product sync nuance:** product re-download requires both a `DataVersion[:products]`
bump **and** a product `timestamp` change — version alone may not trigger product sync.

### Server-side filtering at sync time (per User Group)

Before products reach the device, the server filters by the rep's **UserType** (User Group):

- Authorized **trade names** and **collections**
- **Smart stack filter** (optional hard cap on entire catalog to one stack's items)
- Custom field filters
- Admin-only collections excluded

Customers are filtered separately — see Territory below.

## User Groups (UserType) — the permission layer

Admin → Users → **User Groups**. Every rep belongs to exactly one group. This is the
primary control for what appears on iPad.

### Auth pattern

Most resources use `*_auth`: `'a'` = all, `'n'` = none, `'c'` = selected subset:

- Trade names, collections, price levels, smart stacks, custom fields, shared resources,
  distribution centers, iPad reports, surcharge types

### Customer sync mode (`customer_synching`)

| Value | Meaning on iPad |
|-------|-----------------|
| `'a'` (All) | Every customer in org syncs; **no territory filter** |
| `'n'` (None) | No customers sync |
| Default / territory mode | Customers filtered by rep ↔ customer **territory code overlap** |

Admin UI labels this "show all customers" vs "show only associated customers" in go-live
docs — it maps to `customer_synching`.

### Other high-impact flags

| Flag | Effect |
|------|--------|
| `dont_send_orders` | Blocks `POST orders.json` |
| `allow_ipad_logins` | Blocks login when false |
| `display_contract_prices` | Contract price sync; turning off forces stale local deletion |
| `allow_order_discounting` / `hide_order_totals` | Order pad behavior |
| `smart_stack_filter_id` | Hard-limits entire product catalog to one stack |
| `require_valid_options_to_submit_orders` | Option validation on submit (org can also set) |
| `allow_price_levels_different_from_default_when_customer_selected` | Cog-menu level switching |

Full flag list + org hash keys: see [Code & Config Reference](#code--config-reference) below.

## Territory → which customers sync

Code: `Customer.filter_for_org_user` in `supercat_server/app/models/customer.rb`.

**When group syncs by territory (not "All"):**

1. Rep `territory_codes` must **intersect** customer `TerritoryCodes` (case-insensitive).
2. If only a **ship-to** matches, customer syncs but non-matching locations are marked
   `hidden`.
3. Customers (and ship-tos) with **blank territory codes are excluded** unless the group
   syncs all customers.

**Import vs runtime trap:** `TerritoryCodes` is KB-required but **not importer-fatal**.
A clean import with blank territories succeeds — then reps in territory mode see **zero
customers**. Always verify territory population in live DB, not just import status.

Rep invitation CSV: `territory_codes` comma-separated, no spaces (e.g. `1,2`). Server
stores as JSON array; `OrgUser#rep_number` = first territory code.

## Pricing on the iPad

For **price level configuration** (imported vs arithmetic, `Price_<code>` columns,
promos, matrix file build), use `ecat-pricing-levels`. This section is **runtime resolution**.

### Chain (in order)

1. **Rep selects customer** → device's active price level = customer `DefaultPriceCode`
   (from synced `customers.csv` data).
2. **User Group** controls which levels the rep may see/select in the cog menu.
3. **On-device calculator** (`PriceCalculator.m`, `OrderItemPriceCalculator.m`) resolves
   the dollar amount.

### Price level list synced to device

`OrgUser#authorized_price_levels` (server):

- If rep profile has a **`customer_number`** linked to a customer with
  `default_price_code` → sync **only that one** price level (rep treated as that customer).
- Else → User Group's authorized price levels.

**Classic misconfiguration (Ticket #12877 / Visual Comfort):** rep has BOTH territory
codes AND a `customer_number` on their profile → they see only that customer's single
price level. **Fix:** clear `customer_number` from rep profiles unless they truly are a
buyer-login user.

**API ≥ 2.13.2:** server may send **all org price levels**; device still applies group
visibility rules. Do not assume "server sent it" = "rep can select it."

### On-device calculation order

1. Base: imported `netPrice` / ad-hoc `Price_<code>` / arithmetic factor × base level
2. Quantity-break redirect (if applicable)
3. Promotional price/factor (if beats regular)
4. Contract price (if enabled for group + level)
5. **Matrix options:** local SQLite lookup → `matrixedAddonBasePrice`
6. Non-matrix option addons/factors + riser pricing
7. Round per level's `roundPricing`

Hide list/net from a group: **do not authorize `net_price`** for that User Group.

### Quick pricing diagnosis

| Symptom | Likely cause | Route |
|---------|--------------|-------|
| $0 / blank price | Empty `Price_<code>` or blank `NetPrice` in Net display mode | `ecat-pricing-levels` + re-sync |
| Promo item **$0.00** after selecting a no-promo / excluded level | Level `promo_factor` is `0` (iPad allows promo and multiplies by zero). `-1` hides promo | `ecat-pricing-levels` — then Wi-Fi sync |
| Only one price level | `customer_number` on rep profile | `ecat-go-live` — clear it |
| Wrong price per customer | Customer `DefaultPriceCode` mismatch | `ecat-customers-build` |
| Promo button missing | Invalid `DiscountPriceLevelCode` or group not authorized | `ecat-pricing-levels` |
| Web shows price, iPad doesn't | eOL vs iPad config split | Split diagnosis; check group + sync |

## Options and matrix pricing

- **Options / option groups:** synced as plist → local tables; layout from Admin **Option
  Mapping**.
- **Matrixed option sets:** product marks set as matrixed; price comes from local
  `matrix_options.db` (built from imported `matrix_options.csv` on server).
- **Submit validation:** org/group may require all option sets filled before submit.

Build/troubleshoot the files: `ecat-options-and-mapping`. Runtime "wrong matrix price":
confirm matrix zip rebuilt after import (`DataVersion[:matrix_options]`) + full sync.

## SmartLists (Smart Stacks)

Curated product lists on iPad — **not** a catalog filter for the whole app.

Visibility requires **all** of:

1. Stack **published**
2. Stack **authorized** to rep's User Group
3. Items ∩ rep's **authorized products** (server intersects at sync)
4. Device **synced** after publish

Two types:

- **Query (SQL):** self-maintaining against `product_inventory` view; bad SQL → stack
  goes dormant + error email.
- **Item list:** SKUs **newline-separated** (NOT comma — KB is wrong here).

Details: `ecat-smartlists`.

## Orders — iPad → server

Flow: `OrderSubmitter.m` → `POST /:org/orders.json` → `Orders::Create`.

| Check | Blocks submit when |
|-------|-------------------|
| `dont_send_orders` on User Group | Yes |
| Invalid option sets (when required) | Yes |
| Missing order type (org flag) | Yes |
| Duplicate PO (org flag) | Yes |

**Resubmission safety:** server dedupes on order number + total + submit date + bill-to
(network retry idempotency).

After submit: `GET /:org/orders/submitted_orders.json` reconciles local UUIDs on next sync.

Orders in Postgres with `order_source = 'ipad'` are **rep-submitted**. `order_source =
'server'` is eOL/Cart — not comparable for iPad order troubleshooting.

## Admin settings → iPad behavior (quick reference)

| Setting | Where | iPad effect |
|---------|-------|-------------|
| User Group auth flags | Users → User Groups | Catalog, customers, prices, stacks, reports |
| `customer_synching` | User Group | All / none / territory-filtered customers |
| Rep `territory_codes` | User profile | Which customers sync |
| Rep `customer_number` | User profile | Overrides to single-customer price levels |
| Price levels | Products → Price Levels | What can be imported and calculated |
| Option Mapping | Admin | Option picker layout |
| Smart Stacks | Admin | Curated lists |
| iPad Reports | Admin + group auth | Tear sheets / barcode reports |
| Order email template | Company Settings | Post-submit email (not iPad UI) |
| `disable_sync` / org status | Organization | Sync/login gates |
| `comparison_price_level_code` | Organization | Strike-through / comparison pricing |

More keys from `Organizations::BuildOrganizationHash`: see [Code & Config Reference](#code--config-reference).

## Diagnosis playbook

Run this before guessing:

```
1. CONFIRM SURFACE → iPad rep issue, not eOL/Portal? If eOL, stop and switch to
                     ecat-online; if Sales Portal, switch to ecat-sales-portal-onboarding.
2. IDENTIFY ORG    → shortname; ground with ecat-postgres-audit if state-dependent
3. CHECK USER      → User Group (not DefaultUserGroup?), territory_codes, customer_number
4. CHECK SYNC      → last sync time, Wi‑Fi, import_events since last sync
5. MAP SYMPTOM     → table below
6. ROUTE           → specialized ecat-* skill for the fix
7. REPLY           → ecat-client-email; "sync on Wi‑Fi" when appropriate
```

| Symptom | First checks | Route |
|---------|--------------|-------|
| Missing images | FTP flat `/images`, filename = `ImageFileName`, sync | `ecat-images-ftp` |
| Customers disappeared | Territory overlap; blank TerritoryCodes; customer_synching; HARD-delete import | `ecat-go-live`, `ecat-customers-build`, `ecat-ground-truth` |
| Catalog empty / tiny | Trade name/collection auth; smart_stack_filter | `ecat-go-live` |
| Wrong / blank price | DefaultPriceCode; customer_number on rep; Price_ columns | `ecat-pricing-levels` |
| SmartList missing | Published + group auth + sync | `ecat-smartlists` |
| Options / matrix wrong | Option mapping; matrix_options import + sync | `ecat-options-and-mapping` |
| Order won't send | dont_send_orders; option validation; order type required | `ecat-go-live` + org flags |
| Stale data after import | Rep didn't sync; DataVersion not bumped | Re-sync; check import_events |

## Skill routing (this skill vs others)

| Task | Skill |
|------|-------|
| **How iPad behaves / rep-facing diagnosis** | **ecat-ipad-app** (this) |
| Build products/stories/inventory CSV | `ecat-core-files` |
| Build customers CSV | `ecat-customers-build` |
| Configure price levels / columns | `ecat-pricing-levels` |
| Options files + Option Mapping | `ecat-options-and-mapping` |
| SmartList creation | `ecat-smartlists` |
| Rep invites, groups, go-live | `ecat-go-live` |
| Live DB counts / import_events | `ecat-postgres-audit` |
| HelpScout / email triage | `ecat-support-triage` |
| Full onboarding | `ecat-onboarding-orchestrator` |
| eCat Online (eOL) buyer web catalog | `ecat-online` |
| Sales Portal build / analytics | `ecat-sales-portal-onboarding` |
| Import delete semantics | `ecat-ground-truth` (always-on rule) |

## KB vs code (trust code)

| Topic | KB / assumption | Code reality |
|-------|-----------------|--------------|
| SmartList item list | Comma-separated | **Newline-separated** (`SmartStack.parse_item_numbers_str`) |
| TerritoryCodes | Required for import | Not importer-fatal; **blank = won't sync** to territory reps |
| `builds_ipad_databases.rb` | Sounds like full catalog DB | **Matrix options only** |
| iPad price visibility | User group only | **`customer_number` on rep → single level** |
| eOL "My Account" markup | Catalog Pricing KB | **eOL only** — ignore for iPad |
| Rep number | Separate field | **`territory_codes[0]`** |
| Contract prices disabled | Skip download | Server forces re-download so iPad **deletes** stale local rows |

## Code map

Server (`SuperCatSolutionsLLC/supercat_server`) + iOS (`sarreid_ios/eCatalog/`).

**Read server code from GitHub, not the local checkout** — `~/supercat-code/supercat_server`
goes stale (10 weeks / ~55 PRs behind on 2026-08-25) and verifying against it has already put
wrong facts into skills. Use `gh repo clone SuperCatSolutionsLLC/supercat_server /tmp/scs_repo -- --depth 1`
and cite the commit SHA for any code-derived claim.
Full file list: [Code & Config Reference](#code--config-reference).

**Start here for a bug class:**

| Bug class | Read first |
|-----------|------------|
| Sync / stale data | `Synchronizer.m`, `api_controller.rb`, `data_version.rb` |
| Customer visibility | `customer.rb` (`filter_for_org_user`), `user_type.rb` |
| Price levels synced | `org_user.rb` (`authorized_price_levels`) |
| On-device price | `PriceCalculator.m`, `OrderItemPriceCalculator.m` |
| Matrix price | `builds_ipad_databases.rb`, local matrix DB on device |
| Smart stacks | `smart_stack.rb`, `smart_stack_sync.rb` |
| Order submit | `orders_controller.rb`, `Orders::Create`, `OrderSubmitter.m` |
| Org config payload | `organizations/build_organization_hash.rb` |

## Live data

For "what does org X actually have enabled / imported / visible," use
`supercat-data-routing` → Postgres (`ecat-postgres-audit` queries). Never guess counts
or import timestamps from local markdown alone.

## MCP HTTP API (read-only, fast first look)

A read-only HTTP API exposes org runtime state for diagnosis without opening Admin.
Base path (from `config/routes.rb:652,654,710`): `/api/v1/<shortname>/mcp/...`.
Use it as the **first-look, runtime-diagnosis entry point**; for deep schema auditing
(counts, import_events, joins) route to `ecat-postgres-audit`.

`.json`-suffixed endpoints (from `config/routes.rb:710-760`):

| Endpoint (append `.json`) | Answers |
|---------------------------|---------|
| `organizations/users/permissions_summary` | Per-group auth flags |
| `organizations/users/:user_id/visibility_analysis` | Why a rep sees what they see |
| `organizations/customers/:customer_id/pricing_analysis` | Price level resolution for a customer |
| `organizations/territories` | Territory ↔ customer mapping |
| `organizations/customers/hierarchy` | Bill-to / ship-to tree |
| `organizations/data/summary` | Entity counts + config snapshot |
| `organizations/data/smart_stacks` | Stack publish/auth state |

**Auth — admin only, three methods** (`base_controller.rb:9-12,18-30`, in order):
session cookie → `X-CLIENT-ID` + `X-API-KEY` (shortname must match) → HTTP Basic.

**Two hard requirements:** HTTPS only (`require_https`, `base_controller.rb:9`); the
`.json` suffix is mandatory (`format: :json` on the scope, `routes.rb:710`).

```
curl -u 'USER:PASS' \
  https://app.supercatsolutions.com/api/v1/<shortname>/mcp/organizations/data/summary.json
```

---

# Code & Config Reference

Read this when you need file-level debugging context.

## Repository layout

| Path | Role |
|------|------|
| `supercat-code/sarreid_ios/eCatalog/` | Native iPad app (Objective-C/Swift) |
| `SuperCatSolutionsLLC/supercat_server` (GitHub) | Rails API, importers, sync endpoints |

## Server — sync & versioning

| File | Role |
|------|------|
| `app/controllers/api_controller.rb` | `modified_entities.json` — sync orchestration |
| `app/models/data_version.rb` | Per-entity version timestamps; `ENTITIES` list |
| `app/models/importer/builds_ipad_databases.rb` | Builds **matrix_options.db** zip only |
| `app/models/prebuilt_import_file.rb` | S3 storage for prebuilt zips |

## Server — entity endpoints

| File | Endpoint |
|------|----------|
| `app/controllers/api/v1/products_controller.rb` | `GET /:org/products.json` |
| `app/controllers/api/v1/customers_controller.rb` | `GET /api/v1/:org/customers.json` |
| `app/controllers/smart_stacks_controller.rb` | `GET /:org/smart_stacks.json` (NDJSON) |
| `app/controllers/organizations_controller.rb` | `GET /:org/organizations.plist` |
| `app/controllers/users_controller.rb` | Login + authorization plist |
| `app/controllers/orders_controller.rb` | `POST /:org/orders.json`, submitted_orders |
| `app/controllers/matrix_options_controller.rb` | `GET /:org/matrix_options/prebuilt.json` |
| `app/services/organizations/build_organization_hash.rb` | Org config hash → iPad |
| `app/services/products/build_query_conditions.rb` | Product visibility filters |
| `app/services/smart_stack_sync.rb` | Smart stack rendering |
| `app/services/orders/create.rb` | Order validation + idempotent resubmit |
| `app/services/orders/build.rb` | iPad JSON → Order model |

## Server — models (behavior)

| File | Role |
|------|------|
| `app/models/customer.rb` | `filter_for_org_user` — territory filtering at sync |
| `app/models/org_user.rb` | Rep profile; `authorized_price_levels`, territories |
| `app/models/user_type.rb` | User Group; `customer_synching`, auth flags |
| `app/models/price_level.rb` | Level types (ad-hoc, arithmetic, QPB) |
| `app/models/smart_stack.rb` | SQL + item-list stacks; newline item parsing |
| `app/models/ipad_report.rb` | Tear sheet / barcode report configs |

## iOS — sync, pricing, orders

| File | Role |
|------|------|
| `Classes/Synchronizer.m` | Full sync pipeline, URL list, image download |
| `Classes/SyncController.m` | Sync UI |
| `Classes/BuildsDataObjects.m` | JSON/plist → local SQLite |
| `Classes/DataStore.m` | Local state; customer → default price level |
| `Classes/PriceCalculator.m` | Base price math (arithmetic, QPB, ad-hoc) |
| `Classes/OrderItemPriceCalculator.m` | Line price: base + promo + contract + matrix + options |
| `Classes/OrderSubmitter.m` | POST order JSON |
| `Classes/OrderSubmissionFlow.m` | Submit routing (production vs show server) |
| `Classes/OrgUser.m` | Parses server auth plist (`dont_send_orders`, etc.) |
| `SuperCatTest/PriceCalculatorTest.m` | Pricing unit tests |
| `SuperCatTest/OrderItemPriceCalculatorTest.m` | Line pricing tests |

## Sync sequence (technical)

```
iPad                              Server
  |-- modified_entities.json ---->|
  |<-- { products: N, customers: M, current_version: V, ... }
  |-- products.json (if N>0) ---->|
  |-- customers.json (if M>0) --->|
  |-- smart_stacks.json --------->|
  |-- price_levels.plist -------->|
  |-- matrix_options/prebuilt.json -> redirect to S3 zip
  |-- organizations.plist ------->|
  |-- [images by modified_after] ->|
  |-- BuildsDataObjects -> SQLite |
```

Incremental product sync also passes `previous_version` (product timestamp watermark).

Every ~20 syncs (`SYNC_PURGE_COUNT`), orphaned local images may be purged.

## UserType `customer_synching` constants

From `user_type.rb`:

| Constant | Value | Admin meaning |
|----------|-------|---------------|
| `CUSTOMER_SYNCHING_ALL` | `'a'` | All customers; no territory filter |
| `CUSTOMER_SYNCHING_NONE` | `'n'` | No customers |
| `CUSTOMER_SYNCHING_OWN` | `'o' (Associated)` | Filter by territory overlap |

`OrgUser#sync_all_customers?` delegates to `user_type.synch_all_customers?`.

## Territory filter logic (exact)

From `Customer.filter_for_org_user`:

1. If customer AND all ship-tos have **blank** territory codes:
   - Return customer only when `org_user.sync_all_customers?`
   - Else return `nil` (customer not synced)
2. Else intersect rep `territory_codes` with customer `territory_codes`:
   - Match → full customer
   - No bill-to match → check ship-tos; mark non-matching `hidden`
   - No visible ship-tos → `nil`

Territory codes are downcased on validation (`customer.rb` before_validation).

## Pricing — server → device

`OrgUser#authorized_price_levels`:

```ruby
# Pseudocode from org_user.rb
if org_user.customer_number present?
  customer = associated_customer
  if customer.default_price_code → valid PriceLevel
    return [that one PriceLevel]
  end
end
user_type.authorized_price_levels  # subset or all per price_levels_auth
```

On device (`DataStore.m`): active level = selected customer's `defaultPriceCode`,
falling back to first authorized level.

`PriceLevel::SEND_ALL_VERSION` (API ≥ 2.13.2): all org levels may be transmitted;
User Group still governs visibility in UI.

## On-device line price stack

`OrderItemPriceCalculator.m` order of operations:

1. Resolve price level; reject if `factor` < 0 (hides **all** prices)
2. Include promo only if `promo_factor` is nil or `>= 0`. **`0` still includes promo**
   and multiplies it to $0.00. **Negative (`-1`) skips promo** and uses regular.
   (Server/eOL treats `0` as hide-promo — this $0 bug is iPad-specific.)
3. Choose promo vs contract (lower wins when both provided)
4. `PriceCalculator` base price for qty + level
5. Add matrixed addon base (from local matrix DB)
6. Apply option addons/factors, riser pricing
7. Round per level rules

## Order submission

**Request:** `POST /:org/orders.json` with JSON body + `api_version` / `ecat_version`.

**Guards:**

- `org_user.allow_sending_orders?` (inverse of `dont_send_orders`)
- Order number sequence validation
- UUID uniqueness
- Optional: order type required, unique PO, valid options

**Resubmit detection:** same order number + total + submit_date + bill_to → 200 without duplicate.

**Post-submit:** `OrderExporting.maybe_enqueue_order_for_export` if configured.

**Reconciliation:** `GET /:org/orders/submitted_orders.json` returns UUIDs; iPad marks local orders confirmed.

**Field naming:** iPad sends `customer_ponum`; server accepts `customer_po_num` too (`Orders::Build`).

## Smart stacks

| Concern | Detail |
|---------|--------|
| Item list delimiter | Newline (`SmartStack.parse_item_numbers_str`) |
| SQL target | `product_inventory` view |
| Bad SQL | Stack marked dormant; error email |
| Visibility | `retrieve_item_numbers(org_user)` ∩ authorized products |
| Auth | `smart_stacks_auth` on UserType ('a'/'n'/'c') |
| Catalog filter | Optional `smart_stack_filter_id` on UserType — restricts **entire** catalog |

## Org hash (`BuildOrganizationHash`) — common iPad keys

Non-exhaustive; inspect the service for the full ~100 keys:

- Image base URLs, logo URLs
- Order header/footer custom fields
- Ship date / cancel date rules
- Surcharge configuration
- Theme/branding
- `minimum_ecat_version`
- `prune_historical_orders_on_ipad`
- `require_order_type_on_submission`
- `require_unique_po_numbers`
- `comparison_price_level_code`
- `enable_shared_orders`
- Order template identifiers

## Postgres fields useful for iPad diagnosis

| Table / column | Use |
|----------------|-----|
| `orders.order_source` | `'ipad'` vs `'server'` |
| `org_users.territory_codes` | Rep territory JSON |
| `org_users.last_ipad_login_at` | Active rep signal |
| `user_types.customer_synching` | Customer sync mode |
| `import_events` | What actually loaded + when |
| `data_versions` | Sync version state |

Use `ecat-postgres-audit` / `supercat-data-routing` — never `supercat-cs-tools` (retired).

## Related KB articles (Craft CMS)

| Topic | Slug / ID |
|-------|-----------|
| Price Levels: eCat Online vs iPad | `price-levels-ecat-online-vs-ecat-ipad` (41706, draft) |
| Import customers | `/knowledgebase/import-customers` |
| Discount / promo price levels | `/knowledgebase/discount-market-promo-price-levels` |
| Comparison price level | `/knowledgebase/comparison-price-level` |

When KB conflicts with code, **code wins** — see KB vs code table above.

## Analytics

iPad usage analytics: BigQuery `google_analytics_ecat` per `supercat-data-routing`.
Login events also stored server-side (`LoginEvent` — ecat version, iOS version, iPad model).
