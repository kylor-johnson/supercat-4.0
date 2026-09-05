# PORTAL SETTINGS — CONTROL-PLANE BLUEPRINT
**Agent:** SETTINGS (08) · **Mode:** Agent, ISOLATION ON (read-only) · **Date:** 2026-07-17
**Deliverable for:** 05-ORCHESTRATOR review → betting table
**Scope:** inventory → triage → target control plane → migration roadmap. No code applied.

---

## Load confirmation (first-message behavior)
- ✅ Loaded `cycle-02-inputs/settings-inventory-source.md` (authoritative raw inventory, 134 toggles / 39 flags / 6 layers).
- ✅ Loaded `00-PROGRAM-SPINE.md` + `00b-PRODUCT-HANDOFF-analytics.md`.
- ✅ Read the real flag surface in `supercat-code/supercat_server`: `config/initializers/enabled_features.rb`, `app/models/feature.rb`, `ecat_permissions_helper.rb#allow_view_sales_portal?`, `eol_left_nav_dataflow.rb#should_show_portal`, `user_type_permissions.rb`, `user_type.rb` FLAGS.
- ✅ Verified all 9 "orphaned" flags against **actual** call sites (`Feature.enabled?`, `enabled_for_organization?`, and bare symbol references) — **the source's orphan list is wrong; corrected below with receipts.**
- ✅ Live Postgres adoption pass (read-only) to size the win and back GRADUATE calls.
- ⏭️ Confluence page 1813676033 **not** re-pulled: MCP intermittent + the source file is declared authoritative. Where I need a per-row default/UI-location that only lives on Confluence, I flag it `[confirm on 1813676033]` instead of guessing.

---

## 🔴 HEADLINE CORRECTION — the "9 orphaned flags" claim is materially wrong

The source (and the Confluence page) label 9 flags "orphaned" from a grep of `Feature.enabled?(:key`. That grep **misses two real call patterns**: `Feature.enabled_for_organization?(:key` and bare-symbol feature references. Re-verified, the 9 split into **two different categories that need opposite treatment**:

### Category 1 — TRULY DEAD FLAG (allowlisted to real orgs, but zero code reads it) → **DEPRECATE / delete allowlist**
| Flag | Allowlisted to (code) | Call sites found | Receipt |
|---|---|---|---|
| `eol_dashboard_filters` | cci, sarreid | **0** | No `Feature.enabled?`, no `enabled_for_organization?`, no bare ref anywhere. Dead. |
| `tcgc_name_fields` | sarreid | **0** | Zero references of any kind. Dead. |
| `allow_user_group_from_selecting_price_levels` | ihw, mhc (+8 users) | **0** | Zero references. Dead despite being allowlisted to 2 orgs + 8 named users — nothing reads it. |
| `sales_quotas` | sarreid | **0 flag reads** | The **feature is alive** but gated on `@current_org.sales_quotas.exists?` (`ecat_dashboard/_index_content.html.erb`, `_top_territories.html.erb`) + a `sales_quotas` table + importer, **not** the flag. Delete the flag entry; feature keeps working. |
| `option_mapping` | opame, yw, omc, +demos | **0 flag reads** | Option mappings are a **fully shipped, ungated feature** (routes `:option_mappings`, `OptionMapping` model, importer, order-process). The flag gates nothing. Delete the flag entry. |

### Category 2 — NOT ORPHANED. WIRED IN CODE, DORMANT IN PROD (no org allowlisted → off everywhere but test/demo) → **KEEP-YAML (dormant) or GRADUATE, do NOT delete**
| Flag | Allowlisted to | Call site (receipt) |
|---|---|---|
| `avery_5392_landscape` | *(none)* | `app/models/ipad_report.rb:311` — `Feature.enabled_for_organization?(:avery_5392_landscape, org)`. Source missed it because it uses `enabled_for_organization?`, not `enabled?`. |
| `placements_field_configuration` | *(none)* | `views/shared/_gridview_fields_v2.html.erb:7` + `_gridview_fields.html.erb:4`. |
| `product_url_variable` | *(none)* | `app/models/custom_field.rb:344` — `return [] unless Feature.enabled?(:product_url_variable, org, org_user)`. |
| `credit_card_support` | *(none)* | `app/controllers/tools_controller.rb:397`. |

**Consequence for the roadmap:** the "delete 9 orphans" wave is really **"delete 5 dead flag entries"** (3 fully dead + 2 flags whose feature ships without them). The other 4 are live code with zero prod adoption — a *product* decision (ship it or cut the code), not a safe delete.

---

# PART A — TRIAGED INVENTORY

Legend for **Verdict**: **KEEP-YAML** (true kill-switch/canary; needs sunset date) · **GRADUATE** (→ Org/MobileSite/UserType setting with a label) · **CONSOLIDATE** (fold into another setting or a user-group perm) · **DEPRECATE** (dead/duplicate) · **SELF-SERVICE** (safe for client org-admin to toggle).
Bucket: **REVENUE** (changes metric meaning) · **ACCESS** (data/visibility policy) · **DISPLAY** (experience polish) · **CATALOG** (catalog-adjacent, portal-irrelevant).
"Real usage" = allowlisted orgs/users from `enabled_features.rb` + count of `Feature.*` call sites (0 = orphaned flag).

## A.1 — Feature YAML layer (all 39, precise)

| Flag | What it does | Real usage (allowlist / call sites) | Bucket | Verdict | Audience | Migration risk |
|---|---|---|---|---|---|---|
| `portal_portal` | One of the OR-gates that turns on the portal dashboard for a user (`should_display_portal_dashboard?`). | 9 users + org_user[khl,cc,fc,pf] / **3** | ACCESS | **GRADUATE** → fold into a single "Portal enablement" model | client admin (enable) / SuperCat (audit) | High — it's inside `allow_view_sales_portal?`/dashboard OR-chain; must stay gated until the chain is refactored (see B decision tree). |
| `force_portal_display` | Overrides `MobileSite.enable_sales_portal` to force the portal on for specific org_users. | org_user[hfg:6, sbmh:5] / **1** (`ecat_permissions_helper:22`) | ACCESS | **CONSOLIDATE** into portal-enablement setting | SuperCat superadmin | High — override semantics; part of access spaghetti. |
| `territory_access_via_rep_number` | Switches territory filtering from `territory_codes` to rep-number join (orders/invoices/customers). **SERV-2178 root.** | el, ctest / **6** (`warehouse_access:427`, `get_orders_for_orders_page:124`, `get_invoices…:127`, `filter_items_by_territory_code_limit:44`, `investigate_portal_data:98,155`) | **ACCESS** | **GRADUATE** → named "Territory match mode" setting | SuperCat superadmin (data-access) | **Critical** — the textbook buried-access-rule; changes which customers a rep sees. Cross-lane with Lane-0 FIX. |
| `backlog_instead_of_amount_invoiced` | Orders page shows Backlog Total instead of amount invoiced. | clm / **1** (`ecat_orders/_index_content:32`) | **REVENUE** | **KEEP-YAML → hand to INSIGHT** | SuperCat + INSIGHT sign-off | **Metric-law.** Changes headline number meaning vs invoiced-net spine. Do not self-serve. |
| `advanced_reports` | Enables advanced Reports surface (gated with `display_sales_portal_totals`). | 7 orgs + 6 users + org_user[bmc,fc,shl] / **1** (`ecat_permissions_helper:50`) | ACCESS/DISPLAY | **GRADUATE** → "Reports & export" section toggle | client admin | Med — stable UX, >2 orgs. Safe to graduate. |
| `xlsx_export` | Adds xlsx export button on Reports. | 6 users + org_user[fc] / **2** | DISPLAY | **GRADUATE** (+ CONSOLIDATE with `enable_disable_portal_export_by_user_group` + UserType `can_export_eol_data`) | client admin | Med — three export toggles overlap; unify. |
| `enable_disable_portal_export_by_user_group` | Lets export be toggled per user-group. | clm / **2** (`_eol_behavior*`) | DISPLAY/ACCESS | **CONSOLIDATE** into one export permission | client admin | Med — overlaps xlsx_export + can_export_eol_data. |
| `eol_customer_graph` | Sales graph on the customer detail page. | bmc, sarreid + 7 users / **1** (`ecat_customers/show:43`) | DISPLAY | **GRADUATE / SELF-SERVICE** | client admin | Low — pure display; safe. |
| `link_to_customer_dashboard` | Shows "customer dashboard" link for associated customers. | vic, clm + 8 users / **1** (`ecat_permissions_helper:37`) | DISPLAY/ACCESS | **GRADUATE** | client admin | Low-med — visibility of a link; check associated-customer path. |
| `internal_warehouse_unsubmitted_orders` | Includes unsubmitted/shared-draft orders in warehouse order/customer extracts + a "submitted" filter. | vcg, fms, tla, vl, clc / **8** | REVENUE-ish | **KEEP-YAML → INSIGHT review** | SuperCat | Med-high — changes which orders count; touches order math. Flag to metric lane. |
| `admin_rma_email_notification` | RMA email notification config in Mobile Site form. | scw, gww, sc, sccon, gh, sctest / **2** | DISPLAY | **GRADUATE** | client admin | Low — admin-console only, not portal-runtime. |
| `option_forms` | Option-forms UI in order process + nav. | 8 orgs / **3** | CATALOG | **GRADUATE** (catalog, out of portal hub) | client admin | Low — catalog-adjacent; route to catalog settings, not Portal hub. |
| `asi_shared_orders` | ASI shared-order flow in order process. | asi, mpc, mah / **1** | CATALOG | **KEEP-YAML** (partner-specific) | SuperCat | Med — partner integration; keep gated. |
| `twenty_option_types` | Raises option types 8 → 20. | ~18 orgs / **1** (`organization:745`) | CATALOG | **GRADUATE** | client admin | Low — mature, widely used; graduate to org capability. |
| `minimum_ecat_version` | Enforces min iPad app version. | ~9 orgs / **1** | CATALOG | **GRADUATE** | SuperCat/client | Low. |
| `more_placement_fields` | Extra placement report fields. | fms, tla, vcg / **3** (`placement_report`) | CATALOG | **GRADUATE** | client admin | Low. |
| `market_commitments` | Market-commitment fields across org/user. | ufi, lcf, mh + 7 users / **4** | CATALOG | **GRADUATE** | client admin | Low-med. |
| `manage_smart_stacks_permission` | Adds `manage_smart_stacks` admin permission when on. | heb / **1** (`user_type_permissions:216` map) | ACCESS | **CONSOLIDATE** into user-type permissions | client admin | Low — already a permission bridge; just expose the permission directly. |
| `price_level_enforce_order_quantity` | Order-qty enforcement on price levels. | fc / **2** | CATALOG | **GRADUATE** | client admin | Low. |
| `promo_price_level` | Promo price-level UI. | cci / **2** | CATALOG | **GRADUATE** | client admin | Low. |
| `override_company_info_at_group` | Company info override at group. | sc, sc_test / **4** | DISPLAY | **KEEP-YAML** (SC-internal only) | SuperCat | Low — only SC orgs. |
| `override_order_footer_text` | Custom order footer text. | 5 orgs / **3** | DISPLAY | **GRADUATE** | client admin | Low. |
| `override_eol_login` | Alternate eOL login path. | org_user[jyc, cfg] / **1** (`eol_controller:60`) | ACCESS | **KEEP-YAML** (auth-sensitive canary) | SuperCat superadmin | High — login behavior; keep gated. |
| `suppress_buyer_email` | Suppresses buyer order email. | cci / **1** | DISPLAY | **GRADUATE** | client admin | Low. |
| `order_item_tags` | Order-item tags (admin-gated). | 5 orgs / **2** | CATALOG | **GRADUATE** | client admin | Low. |
| `rma_custom_fields` | Custom fields on RMA. | 5 orgs / **2** | CATALOG | **GRADUATE** | client admin | Low. |
| `ship_cancel_date_tweaks` | Ship/cancel date behavior tweaks. | 6 orgs (incl shl) / **3** | CATALOG | **GRADUATE** | client admin | Low-med. |
| `org_user_ship_to_code` | Adds ship-to-code field on org users. | clli / **2** | ACCESS | **GRADUATE** (pair with OrgUser.ship_to_code) | client admin | Low. |
| `netsuite_rest_api` | NetSuite REST integration. | shl / **1** (`netsuite:49`) | INTEGRATION | **KEEP-YAML** (integration canary, per NETSUITE guide) | SuperCat | Med — integration; keep gated w/ owner. |
| `multifile_ephemeral_import` | v3 multifile ephemeral import; ENV-driven too. | *(empty allowlist)* / **1** (`org_importer:55`) | INTEGRATION | **KEEP-YAML** (active canary) | SuperCat | Med — import pipeline; keep as lab flag with sunset. |
| `eol_dashboard_filters` | *(intended dashboard filters)* | cci, sarreid / **0** | — | **DEPRECATE** | — | **Zero-usage receipt above.** Delete allowlist. |
| `tcgc_name_fields` | *(intended name fields)* | sarreid / **0** | — | **DEPRECATE** | — | Zero references. Delete. |
| `allow_user_group_from_selecting_price_levels` | *(intended price-level selection)* | ihw, mhc +8 users / **0** | — | **DEPRECATE** | — | Zero references. Delete. |
| `sales_quotas` | *(flag)* — feature ships via `sales_quotas` table, not the flag | sarreid / **0 flag reads** | REVENUE (feature) | **DEPRECATE flag** (feature stays) | — | Delete flag entry only; dashboard quota rendering is data-gated and unaffected. |
| `option_mapping` | *(flag)* — option-mapping feature ships ungated | opame, yw, omc + demos / **0 flag reads** | CATALOG (feature) | **DEPRECATE flag** (feature stays) | — | Delete flag entry only; `OptionMapping` CRUD/importer unaffected. |
| `avery_5392_landscape` | Avery 5392 landscape label shape. | none / **1** (`ipad_report:311`) | CATALOG | **KEEP-YAML (dormant)** — decide ship-or-cut | SuperCat | Wired, no prod org. Not orphaned. |
| `placements_field_configuration` | Configure placements gridview fields. | none / **2** | CATALOG | **KEEP-YAML (dormant)** — decide ship-or-cut | SuperCat | Wired, no prod org. |
| `product_url_variable` | Product-URL custom-field alias when online catalog on. | none / **1** (`custom_field:344`) | CATALOG | **KEEP-YAML (dormant)** — decide ship-or-cut | SuperCat | Wired, no prod org. |
| `credit_card_support` | Adds Customer Payment Info to import file types. | none / **1** (`tools_controller:397`) | INTEGRATION | **KEEP-YAML (dormant)** — decide ship-or-cut | SuperCat | Wired, no prod org. |

**Flag-layer scorecard:** 39 flags → **5 DEPRECATE** (delete allowlist entries) · **19 GRADUATE** · **4 CONSOLIDATE** · **7 KEEP-YAML** (2 active canaries + 1 auth + 4 dormant-decide) · **2 KEEP-YAML→INSIGHT** (revenue-meaning) · plus `territory_access_via_rep_number` GRADUATE-but-superadmin. Net: **~23 flags leave YAML**, ~11 stay gated, 5 die.

## A.2 — Organization layer (57) — portal-scoped + metric-critical enumerated; rest bucketed

**Portal-scoped & metric-critical Organization settings (precise):**

| Setting | What it does | Real usage | Bucket | Verdict | Audience | Risk |
|---|---|---|---|---|---|---|
| `enable_portal_dashboard` | Org-level OR-gate for the portal dashboard (`should_display_portal_dashboard?`). | live (Org flag) | ACCESS | **GRADUATE** into unified "Portal enablement" | client admin | High — part of `allow_view_sales_portal?` chain. |
| `enable_portal_delta_imports` | Portal delta-import mode. | Org flag | REVENUE-adjacent | **KEEP** (SuperCat) | SuperCat | Med — data freshness/ingest. |
| `excluded_portal_order_backlog_order_statuses` | Which order statuses count as backlog/open. | Org setting | **REVENUE** | **KEEP → INSIGHT** | SuperCat + INSIGHT | **Metric-law.** Changes backlog definition. |
| `portal_data_type` (OVERLAPS / DOESNT_OVERLAP / DOESNT_CORRELATE) | How order & invoice facts combine. | hidden Org setting | **REVENUE** | **KEEP → INSIGHT** | SuperCat + INSIGHT | **Metric-law.** Never self-serve. |
| `portal_calculations` (legacy vs PORTAL_CALCULATIONS_20180720) | Which calc engine runs portal math. | hidden Org setting | **REVENUE** | **KEEP → INSIGHT** | SuperCat + INSIGHT | **Metric-law.** |
| `sales_portal_currency_code` | Currency label/formatting in portal. | Org setting | DISPLAY | **SELF-SERVICE** | client admin | Low — display only; **safe** (formatting, not math). |
| `sales_portal_sales_facts_filter_configuration` | Sales-facts filter config for dashboard. | hidden Org setting | **REVENUE** | **KEEP → INSIGHT** | SuperCat + INSIGHT | Metric-law — defines the fact filter. |
| `max_portal_data_age_months` | Caps how far back portal data shows. | hidden Org setting | ACCESS/DISPLAY | **GRADUATE** (superadmin default) | SuperCat | Med — affects totals window. |
| `enable_sales_data` | Enables sales-data surfaces. | Org flag | ACCESS | **CONSOLIDATE** into portal enablement | client admin | Med. |
| `link_to_customer_dashboard` (Org) | Org-level twin of the flag above. | Org flag | DISPLAY | **CONSOLIDATE** with the Feature flag | client admin | Low. |

**Remaining Organization settings (~47) — bucketed triage (individual rows to confirm on Confluence 1813676033):**

| Bucket | Examples from source | Verdict pattern | Audience |
|---|---|---|---|
| Pricing | `allow_double_discounting`, `contract_prices_always_win`, price-level toggles | **CATALOG — out of Portal hub.** Mostly **SELF-SERVICE** in a Pricing section; a few (contract-price-wins) stay client-admin. | client admin |
| Orders | `attach_pdf_to_order_email`, `enable_shared_orders`, `enable_distribution_centers` | **SELF-SERVICE / GRADUATE** — mature order behavior; safe for client admin. | client admin |
| Catalog | `drilldown_*`, `kit_items_enabled`, `enable_twelve_product_images` | **CATALOG — out of scope for Portal hub;** route to catalog settings. Note `enable_twelve_product_images` is paid-flag-gated (per eCat ground truth). | client admin / SuperCat (paid) |

**Why bucketed, not row-by-row:** the source provides these 47 as grouped examples, not a full column list, and the authoritative per-row table (name/default/UI) lives on Confluence 1813676033 (auth-gated, MCP intermittent). Rather than invent 47 rows, the migration rule is applied by bucket, with a `[finalize from 1813676033]` gate before any of them move. **None are metric-law-critical** (those are all enumerated above), so this is safe to defer to the build wave.

## A.3 — MobileSite layer (13)

| Setting | What it does | Real usage (live DB) | Bucket | Verdict | Audience | Risk |
|---|---|---|---|---|---|---|
| `enable_sales_portal` | **Master site switch** for the portal (real boolean column). | **48 / 253 orgs** have ≥1 site on | ACCESS | **GRADUATE** → the top control in "Enablement" | client admin | High — the front door; but it's already a clean boolean, ideal to surface. |
| `enable_customer_dashboard_landing_page` | Customer-dashboard landing behavior. | site flag | DISPLAY/ACCESS | **GRADUATE** | client admin | Med. |
| `display_quantity_available` | Show qty-available column. | site flag | DISPLAY | **SELF-SERVICE** | client admin | Low — display only. |
| `display_quantity_backordered` | Show qty-backordered column. | site flag | DISPLAY | **SELF-SERVICE** | client admin | Low. |
| `enable_online_catalog / _ordering / _library` | Catalog/site capabilities. | site flags | CATALOG | **out of Portal hub** (Site settings) | client admin | Low-med. |
| `price_level_id` | Site default price level. | column | CATALOG | **keep in Site settings** | client admin | Med — pricing. |
| `smart_stack_filter_id` | Site smart-stack filter. | column | CATALOG | **keep in Site settings** | client admin | Low. |
| `send_*_email` (order/confirmation) | Site email behavior. | site flags | DISPLAY | **SELF-SERVICE** | client admin | Low. |

*(13 total; the non-portal catalog/site ones stay in Site settings, not the Portal hub.)*

## A.4 — UserType layer (18) — with live adoption

Storage note: these live in `user_types.properties -> 'flags'` with **defaults** (`enable_sales_portal` default **true**, `enable_portal_dashboard` default **false**, `display_sales_portal_totals` default **true**, `can_export_eol_data` default **true**). Absent key = default, so counts below are *explicit overrides* against 1,934 user types.

| Setting | What it does | Real usage (live DB) | Bucket | Verdict | Audience | Risk |
|---|---|---|---|---|---|---|
| `enable_sales_portal` (UserType) | User-type gate in `allow_view_sales_portal?`. | default true; **57 explicitly OFF** | ACCESS | **GRADUATE** into portal enablement matrix | client admin | High — part of the access chain. |
| `enable_portal_dashboard` (UserType) | User-type gate for dashboard. | default false; **304 explicitly ON** | ACCESS | **GRADUATE** | client admin | High — chain member; real adoption (304). |
| `display_sales_portal_totals` | Gate for totals/advanced reports. | default true; **89 explicitly OFF** | ACCESS | **GRADUATE / SELF-SERVICE** | client admin | Med — hides money; commonly used to restrict. |
| `can_export_eol_data` | Allows portal data export. | default true; **10 explicitly OFF** | DISPLAY/ACCESS | **CONSOLIDATE** with export flags | client admin | Low-med. |
| `customer_synching` (All/None/Associated) | Which customers a user sees. | **962 All / 645 Associated / 327 None** | **ACCESS** | **GRADUATE** → the core of "Territory & data access" | client admin + SuperCat | **High** — the primary customer-visibility rule reps hit. |
| `territory_url` / `territory_url_label` | Territory display labels (real columns). | columns | DISPLAY | **SELF-SERVICE** | client admin | Low. |
| `primary_rep_group` | Primary rep-group flag (real column). | column | ACCESS | **GRADUATE** | client admin | Med. |
| `order_item_quantity_enforcement` | Qty enforcement behavior. | flag | CATALOG | **GRADUATE** | client admin | Low. |
| `*_auth` columns (trade_names/collections/custom_fields/price_levels/smart_stacks/…) | Catalog visibility ACLs. | `'a'` default | CATALOG | **out of Portal hub** (catalog ACLs) | client admin | Med. |
| `allow_*_discounting` | Discounting permissions. | boolean cols | CATALOG | **out of Portal hub** | client admin | Low. |

## A.5 — Permissions layer (3) — `user_types.permissions` JSON

| Permission | What it does | Bucket | Verdict | Audience | Risk |
|---|---|---|---|---|---|
| `access_all_customer_sales_totals` | Portal: see ALL customers' sales totals vs only own. Falls back to `view_all_portal_customers` then `synch_all_customers?` (`user_type_permissions.rb:129`). | **ACCESS** | **GRADUATE** → the second core "Territory & data access" control | client admin + SuperCat | **High** — reveals whole-book revenue; must reconcile with `customer_synching`. |
| `view_sales_reports` | Access to admin Sales Reports. | ACCESS | **GRADUATE** | client admin | Med. |
| `view_*` admin perms (dashboard/customers/orders/…) | Admin-console visibility. | ACCESS | **keep in User-Type permissions UI** | client admin | Low — already has a UI. |

## A.6 — OrgUser layer (4)

| Setting | What it does | Bucket | Verdict | Audience | Risk |
|---|---|---|---|---|---|
| `territory_codes` | Per-user territory list — drives portal territory filtering. | **ACCESS** | **keep on User record** (surface read-only in decision tree) | client admin | **High** — the data reps are scoped by; SERV-2178/2196 territory bugs live here. |
| `ship_to_code` | Ship-to scoping (with `org_user_ship_to_code` flag). | ACCESS | **CONSOLIDATE** with that flag | client admin | Med. |
| `states` | State-based scoping. | ACCESS | keep on User | client admin | Low-med. |
| `settings` / `ui_preference` | Per-user UI prefs. | DISPLAY | **SELF-SERVICE** (the user themselves) | end user | Low. |

---

# PART B — TARGET CONTROL PLANE ("Portal & Access" hub)

## B.1 — Pressure-test of the proposed 5-section IA
The source proposes: Enablement / Territory & data access / Portal display / Reports & export / Feature lab. **Verdict: keep 4, revise 1, and add an explicit non-negotiable.**

| Proposed section | Keep? | Change |
|---|---|---|
| **Enablement** | ✅ Keep | Make it the single home for the entire `allow_view_sales_portal?` OR-chain (site switch + user-type gates + `portal_portal`/`force_portal_display`). Today that logic is spread across 3 layers; the win is showing it in one place. |
| **Territory & data access** | ✅ Keep — **most important section** | This is where SERV-2178 gets fixed structurally: `customer_synching`, `access_all_customer_sales_totals`, `territory_access_via_rep_number` (as "Territory match mode"), read-only view of `territory_codes`. |
| **Portal display** | ✅ Keep | Pure polish: currency, qty columns, customer graph, backlog-vs-invoiced *label*. All client self-service. |
| **Reports & export** | ✅ Keep | `advanced_reports`, `xlsx_export`, `can_export_eol_data`, `enable_disable_portal_export_by_user_group` — **consolidate the 3–4 overlapping export toggles into one export permission.** |
| **Feature lab** | ✅ Keep, **rename "Experiments"** | Superadmin-only. Every entry needs owner + ticket + sunset date. This *replaces* open-ended YAML allowlists. |
| **➕ NEW: "Revenue definitions" (locked)** | **ADD** | The metric-law settings (`portal_data_type`, `portal_calculations`, `excluded_portal_order_backlog_order_statuses`, `sales_portal_sales_facts_filter_configuration`, `backlog_instead_of_amount_invoiced`) must be a **visible-but-locked** section owned jointly by SuperCat + INSIGHT. Making these self-service would let a client silently change what "sales" means and break reconciliation with the invoiced-net spine. This is the single biggest safety carve-out. |

## B.2 — Section → settings → editor → default

| Section | Settings landing here | Who edits | Default |
|---|---|---|---|
| **Enablement** | MobileSite `enable_sales_portal`; UserType `enable_sales_portal`/`enable_portal_dashboard`; flags `portal_portal`, `force_portal_display`, Org `enable_portal_dashboard`, `enable_sales_data` | **Client admin** (superadmin for `force_portal_display` overrides) | portal off; enable per site + user-type |
| **Territory & data access** | UserType `customer_synching`; perm `access_all_customer_sales_totals`; "Territory match mode" (`territory_access_via_rep_number`); read-only `territory_codes`/`ship_to_code` | **SuperCat superadmin** sets match-mode; **client admin** sets synch/totals | synch=All-or-Associated per org; match-mode=territory_codes |
| **Portal display** | `sales_portal_currency_code`, `display_quantity_available`, `display_quantity_backordered`, `eol_customer_graph`, `link_to_customer_dashboard`, backlog-vs-invoiced label | **Client self-service** | sensible display defaults |
| **Reports & export** | `advanced_reports`, `xlsx_export`, `can_export_eol_data`, `enable_disable_portal_export_by_user_group` (unified) | **Client admin** | reports on, export per user-group |
| **Revenue definitions (locked)** | `portal_data_type`, `portal_calculations`, `excluded_portal_order_backlog_order_statuses`, `sales_portal_sales_facts_filter_configuration`, `backlog_instead_of_amount_invoiced`, `max_portal_data_age_months` | **SuperCat + INSIGHT only** | current per-org value; changes logged |
| **Experiments (Feature lab)** | dormant/canary flags: `netsuite_rest_api`, `multifile_ephemeral_import`, `avery_5392_landscape`, `placements_field_configuration`, `product_url_variable`, `credit_card_support`, `override_eol_login`, `override_company_info_at_group` | **SuperCat superadmin** | off; each row shows owner/ticket/sunset |

**North-star scorecard:** of the ~30 portal-relevant survivors, **~18 become client self-service or client-admin**, **~8 stay SuperCat-gated** (access match-mode, overrides, integrations), and **~6 are locked revenue definitions**. Clients self-serve the majority; SuperCat keeps only the data-access/security/revenue-meaning levers.

## B.3 — Untangling `allow_view_sales_portal?` — the decision tree

Verified from `ecat_permissions_helper.rb:20` + `eol_left_nav_dataflow.rb:350`. The in-product answer to **"Why can't this user see the portal?"**:

```
Can this user see the Sales Portal?
│
├─ 1. Is the portal ENABLED for the site OR force-displayed for this user?
│     MobileSite.enable_sales_portal?  OR  Feature :force_portal_display (org/user/org_user)
│     └─ NO  → ❌ "Portal is off for this site." (fix: Enablement → turn on site switch)
│
├─ 2. Is there DATA to show?  (dataflow :should_show_portal)
│     any_portal_records_for_org  (PortalOrder/PortalInvoice exist for org)
│       AND any_portal_records_for_user (user has customer_number OR is not sync-no-customers)
│     └─ NO  → ❌ "No portal orders/invoices imported yet" OR "this user is scoped to zero customers."
│               (fix: import order_data/invoice_data.csv; or fix customer_synching/territory_codes)
│
├─ 3. Is the user in ordering-preview mode?
│     session[:preferred_pricing] must be nil
│     └─ NO  → ❌ "User is in a pricing-preview session." (transient)
│
└─ 4. Does the user's USER-TYPE allow the portal?
      user_type.enable_sales_portal  (default true; 57 user-types explicitly off)
      └─ NO  → ❌ "This user-type has the portal disabled." (fix: Enablement → user-type)
      └─ YES → ✅ Portal visible.

Then, SEPARATELY, the DASHBOARD (should_display_portal_dashboard?) needs ALL of:
   @show_customers  AND  (Feature :portal_portal OR Org.enable_portal_dashboard)
   AND user_type.enable_portal_dashboard (default false; 304 explicitly on)
   AND user_type.display_sales_portal_totals (default true; 89 explicitly off)
```

This tree is the copy that ships in-product (support + clients read it) and the spec for the Enablement section. It also localizes the SERV-2178 class of bug to **node 2 / Territory & data access**, not scattered YAML.

---

# PART C — MIGRATION PLAN (roadmap, not applied)

## C.1 — Sequenced waves

**Wave 0 — Delete dead flags (safe, isolated).** Remove the 5 DEPRECATE entries from `enabled_features.rb`: `eol_dashboard_filters`, `tcgc_name_fields`, `allow_user_group_from_selecting_price_levels`, `sales_quotas` (feature stays), `option_mapping` (feature stays). Zero-usage receipts in the headline table. *Do NOT touch the 4 "dormant-wired" flags — those are a product ship/cut decision, not cleanup.*

**Wave 1 — Graduate the high-usage, stable-UX flags.** Per migration rule (org-allowlisted >2 customers + stable UX → GRADUATE): `advanced_reports` (7 orgs), `twenty_option_types` (~18), `market_commitments`, `option_forms` (8), `ship_cancel_date_tweaks` (6), `order_item_tags`/`rma_custom_fields`/`override_order_footer_text` (5 each), `admin_rma_email_notification` (6). Promote to Org/UserType settings with labels; keep YAML as a read-through shim for one release.

**Wave 2 — Build the "Portal & Access" hub UI.** Ship the 6-section IA (B.1). Start with **Enablement + the decision tree** (directly answers the #1 support question) then **Territory & data access**.

**Wave 3 — Move display toggles to self-service.** `sales_portal_currency_code`, qty columns, `eol_customer_graph`, `link_to_customer_dashboard`, export unification. Low risk, high client-satisfaction.

**Wave 4 — Consolidate access + retire remaining YAML.** Fold `portal_portal`/`force_portal_display`/UserType gates into one enablement model; convert `territory_access_via_rep_number` → superadmin "Territory match mode"; unify export toggles; retire YAML for everything except the Experiments lab.

**Wave 5 — Lock revenue definitions.** Stand up the locked "Revenue definitions" section owned by SuperCat + INSIGHT; migrate the 6 metric-law settings there with change logging.

## C.2 — Count the win

| Metric | Today | Target |
|---|---|---|
| Total toggles | 134 across 6 layers | ~1 hub, **~30 portal-relevant survivors** surfaced (rest routed to Catalog/Site/User-Type UIs that already exist) |
| YAML feature flags | 39, no UI | **5 deleted**, ~23 graduated to settings, ~11 remain (2 canaries + 1 auth + 4 dormant-decide + 4 revenue-lab) → **~11 in an Experiments lab with sunset dates**, 0 open-ended allowlists |
| Portal-scoped decision layers | 6 | **1** ("Portal & Access" hub) with a documented decision tree |
| Client self-service | ~0 (two fields in Company Settings) | **~18 of ~30** survivors self-serve; only access/revenue/security stay SuperCat-gated |

## C.3 — Cross-lane handoffs (metric-law-critical → INSIGHT / Orchestrator)
Hand these to INSIGHT before any UI exposes them — they change what "sales" means and must reconcile to the invoiced-net spine:
- `portal_data_type` (OVERLAPS/DOESNT_OVERLAP/DOESNT_CORRELATE)
- `portal_calculations` (legacy vs PORTAL_CALCULATIONS_20180720)
- `excluded_portal_order_backlog_order_statuses`
- `backlog_instead_of_amount_invoiced` (clm)
- `sales_portal_sales_facts_filter_configuration`
- `internal_warehouse_unsubmitted_orders` (changes which orders count)

`territory_access_via_rep_number` is **cross-lane with Lane-0 FIX** (SERV-2178) — the audit confirms it's the buried access rule; the fix and the graduation should ship together.

## C.4 — Shaped bet (for the betting table)

> **Bet: "Portal & Access" control plane.**
> **Problem:** 134 toggles across 6 layers, 39 YAML flags with no UI; every non-trivial portal change is a SuperCat ticket, and access rules (SERV-2178) hide in deploy config.
> **Appetite:** big batch. Wave 0–1 (delete + graduate) is a small-batch down-payment that de-risks the rest.
> **Elements:** delete 5 dead flags → graduate ~23 flags → build the 6-section hub → move display toggles to self-service → lock revenue definitions.
> **No-gos:** exposing revenue-definition settings to clients; deleting the 4 dormant-wired flags without a product ship/cut call; changing metric meaning without INSIGHT sign-off; applying anything while ISOLATION is on.
> **Done = deployed hub:** a client org-admin can enable the portal, set territory/data access, and adjust display without a ticket; support can answer "why can't this user see the portal?" from the in-product decision tree; YAML holds only sunset-dated experiments.

---

## Receipts index (for review)
- Access chain: `app/helpers/ecat_permissions_helper.rb:20-59`, `app/models/eol_left_nav_dataflow.rb:336-357`.
- Flag resolution + always-on test/demo: `app/models/feature.rb:36-59`.
- Orphan receipts (zero refs): grep of `Feature.enabled?`/`enabled_for_organization?`/bare symbol across `supercat_server` (excluding `enabled_features.rb`) — no hits for `eol_dashboard_filters`, `tcgc_name_fields`, `allow_user_group_from_selecting_price_levels`; `sales_quotas`/`option_mapping` hits are table/model/route usage, **not** the flag.
- Dormant-wired receipts: `ipad_report.rb:311`, `_gridview_fields*.erb`, `custom_field.rb:344`, `tools_controller.rb:397`.
- Live DB (read-only): 253 orgs; 48 with site portal on; 54/55 with portal orders/invoices; UserType `customer_synching` = 962 All / 645 Associated / 327 None; UserType flags — 57 portal explicit-off, 304 dashboard explicit-on, 89 totals explicit-off, 10 export explicit-off (of 1,934 user types).

---

**Paste to 05-ORCHESTRATOR for review.**
