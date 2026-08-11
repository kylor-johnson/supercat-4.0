# SuperCat Product Capability Map — M3 Input

> **Purpose**: Code- and database-verified inventory of every product capability, its gating mechanism, current monetization, and adoption. This is the foundation for the Feature-Value Matrix (M3 Exercise 1).
>
> **Sources**: `code/supercat_server/` (Rails models, controllers, routes, helpers, services), `code/sarreid_ios/` (iOS view controllers, synchronizer, schema), `supercat-postgres` (production DB queries), `supercat_feature_menu_2026-01-27.md`, Angie's billing audit.
>
> **Date**: January 28, 2026

---

## How to Read This Document

- **Product Surface**: The distinct user-facing application or module.
- **Capability**: A discrete unit of functionality a user can observe and use.
- **Gate Type**: How the capability is currently controlled (subscription plan, org flag, mobile_site flag, feature allowlist, implicit/data-driven, or ungated).
- **Current Monetization**: How (if at all) it's separately priced today.
- **Adoption**: Active org count from production DB (118 active orgs, 61 mobile sites).
- **M3 Relevance**: Whether this capability is a candidate for tier fencing, add-on treatment, or base inclusion.

---

## Gating Taxonomy

The platform uses **five layers** of feature control, from coarsest to finest:

| Layer | Mechanism | Where Stored | Who Controls |
|-------|-----------|-------------|--------------|
| **1. Subscription Plan** | Billing record linking org → plan | `subscriptions` + `subscription_plans` tables | SuperCat ops (manual) |
| **2. Organization Property/Flag** | Boolean or JSON property on org record | `organizations.properties` JSON + direct boolean columns | SuperCat ops via admin |
| **3. Mobile Site Flag** | Boolean or JSON property on mobile site | `mobile_sites` columns + `mobile_sites.properties` JSON | Customer admin or SuperCat ops |
| **4. Code-Level Feature Allowlist** | Org/User/OrgUser allowlists in initializer | `config/initializers/enabled_features.rb` (hardcoded lists) | Engineering deployment |
| **5. UserType Permission** | Role-based permission matrix | `user_types` table + `UserTypePermissions` model | Customer admin |

**Critical for M3**: Only Layers 1–3 are operationally feasible for packaging gates today. Layer 4 requires code deployments. Layer 5 is customer-controlled granularity within an already-enabled surface.

---

## Current Subscription Plan Architecture

These are the actual billing SKUs in production (`subscription_plans` table):

| Plan Name | Base Price | Per-User Price | User Limit | Active Orgs | Description |
|-----------|-----------|---------------|-----------|------------|-------------|
| **eCat iPad** | $725/mo | $20/user | 25 included | 88 | Base iPad service |
| **eCat (iPad) Service with CPQ** | $795/mo | $20/user | 25 included | 16 | iPad + configurable products |
| **eCat Online Service** (Catalog) | $295/mo | — | — | 48 | Public online catalog |
| **eCat Online – B2B Cart** | $295/mo | — | — | 26 | Online ordering/checkout |
| **eCat Online – Sales Portal** | $395/mo | — | — | 32 | Sales analytics + data portal |
| **eCat Online – Closed Site** | $100/mo | — | — | 43 | Authenticated-only catalog |
| **eCat Online – Closed Site with Cart** | $495/mo | — | — | 1 | Closed site + cart bundle |
| **eCat (iPad) CPQ** (standalone) | $195/mo | — | — | 1 | CPQ add-on (not bundled) |
| **eCat (iPad) Product Configuration** | $195/mo | — | — | 1 | CPQ variant (same capability) |
| **eCat (iPad) Library FlipBook** | $195/mo | — | — | 5 | Interactive PDF/hotspotting |
| **eCat (iPad) Secure Credit Card** | $195/mo | — | — | 5 | Credit card capture |
| **eCat (iPad) Credit Card PCI** | $195/mo | $195/mo | — | 1 | PCI compliance |
| **Additional Users** | $625/mo | — | 25 block | 1 | User block purchase |
| **Enhanced Support & Advisory** | $850/mo | — | — | 1 | Premium support |

**Total CPQ subscribers**: 18 orgs (16 bundled at $795 + 1 standalone at $195 + 1 "Product Configuration" at $195)

**Observation**: Image Upgrade ($95/mo, enables 12 vs. 6 product images) exists in billing but has no corresponding subscription plan record — likely billed as a manual line item.

---

## Surface 1: eCat iPad App

**Base subscription**: $725/mo (88 active orgs)
**Code evidence**: `code/sarreid_ios/eCatalog/Classes/` (~80 view controllers), `code/supercat_server/app/controllers/api_controller.rb` + `api/v1/` controllers

### Core Capabilities (Included in Base)

| # | Capability | What It Does | Code Evidence | Adoption |
|---|-----------|-------------|--------------|----------|
| 1.1 | **Offline catalog browsing** | Full product catalog synced locally; grid/list/row views; browse by tradenames, collections, categories, groups | `CatalogViewController`, `GroupsCategoriesViewController`, `TradenamesCollectionsViewController` (iOS); `Synchronizer.m` downloads `products.json`, `categories.json`, `groups.json`, `trade_names.json` | Universal (88/88) |
| 1.2 | **Product detail** | Product page with images (up to 6 standard), specs, custom fields, pricing, inventory status, related items | `SingleItemViewController`, `RelatedItemsNavViewController` (iOS); product images synced via `Synchronizer.m` | Universal |
| 1.3 | **Multi-price-level support** | View and apply wholesale, retail, and custom price levels; per-customer contract pricing | `SettingsPriceLevelController`, `PriceLevelPickerViewController` (iOS); `price_levels.plist` sync | Universal |
| 1.4 | **Order creation & management** | Create orders, add items with qty/options/notes, apply discounts, surcharges, preview, submit | `OrderListViewController`, `OrderItemsViewController`, `OrderPreviewViewController`, `OrderSummaryViewController`, `OrderSurchargeViewController` (iOS); `CreateSingleOrderItemViewController` | Universal |
| 1.5 | **Customer selection & management** | Browse/search customers, select ship-to addresses, create local customers | `CustomerSelectionViewController`, `CustomerNavViewController`, `CreateOrEditCustomerViewController`, `ShipToSelectionViewController` (iOS); `customers.json` sync | Universal |
| 1.6 | **Smart stacks & user lists** | Server-defined curated product collections + user-created personal lists | `SmartStacksViewController`, `MyStacksViewController`, `EditStackViewController` (iOS); `smart_stacks.json` + `user_stacks.json` sync | Universal |
| 1.7 | **Library / documents** | Browse and view shared resources (PDFs, documents) synced from server | `DocumentListViewController`, `PDFLibraryDocumentViewController`, `LibrarySectionsViewController` (iOS); `shared_resources.json` sync | 70/118 orgs have library enabled (MS flag) |
| 1.8 | **Product reports / tearsheets** | Generate formatted product reports, placement reports, commitment reports | `ReportPreviewViewController`, `CsvReportPreviewViewController`, `EditReportItemsViewController`, `PlacementsListViewController` (iOS); `ipad_reports` table | Universal |
| 1.9 | **Sync & data management** | Full/incremental sync of all data entities (38+ entity types); backup/restore of local data | `SyncController`, `Synchronizer.m` (iOS); `api_controller.rb` `modified_entities` | Universal |
| 1.10 | **Order submission & email** | Submit orders to server; email confirmation to buyer and internal recipients | `OrderHandoffViewController` (iOS); `EcatOrderProcessController#submit` (server); org flag `send_order_email_on_submit` | Universal |
| 1.11 | **Inventory display** | Show quantity available and backordered per product | Product detail views (iOS); `inventories.json` sync; MS flags `display_quantity_available`, `display_quantity_backordered` | Universal |
| 1.12 | **Settings & configuration** | Organization switcher, price level selection, tradename filtering, account management | `SettingsMoreViewController`, `OrganizationChooserViewController`, `MyAccountViewController` (iOS) | Universal |

### Gated Capabilities

| # | Capability | What It Does | Gate | Current Price | Code Evidence | Adoption |
|---|-----------|-------------|------|--------------|--------------|----------|
| 1.13 | **Configurable products (CPQ)** | Configure products via option sets (up to 8 or 20); option mappings filter downstream choices; riser prices adjust price by selection; matrix options for size/color grids | Subscription plan ($795 bundle or $195 add-on) | $195/mo (or $70 effective premium in $795 bundle) | `OrderItemConfigurator.m`, `KitConfigurator.m`, `OptionMappings.swift`, `ConfiguredItemNumberBuilder.swift` (iOS); `Product#options` YAML with `:custom: true`; `OptionMapping` model; `RiserPrice` model; `option_mappings.json` API sync | **18/118 orgs** subscribed; **6/116 orgs** have configurable products in catalog (`:custom: true`); **25/118 orgs** have kit items |
| 1.14 | **Kit items** | Bundle multiple products into a kit; configure each kit item's options individually; group kit items with order notes | Org property `kit_items_enabled` + data-driven (products must have kits) | Included with CPQ subscription | `KitContentsViewController` (iOS); `KitItem` model; `EcatOrderProcessController#add_kit_to_order`; org flag `kit_items_enabled`, `group_kit_items_with_order_item_notes`, `allow_editing_individual_kit_item_quantities` | **25/118 orgs** have kit item data; **0/118** have `kit_items_enabled` flag explicitly set |
| 1.15 | **Camera / barcode scanning** | Scan UPC/EAN barcodes to look up products; QR scanning for customers | Org column `enable_camera_scanning` | Included (no add-on charge) | `OrderItemScanView` (iOS); `AddScanGroupToOrderViewController`; org column `enable_camera_scanning` + `supported_camera_scan_symbologies` property | **82/118 orgs** (69.5%) |
| 1.16 | **Gridview ordering** | Bulk order entry in a grid/spreadsheet-style interface | Org column `enable_gridview_ordering` | Included | `SelectRowViewColumnsViewController` (iOS); gated by `EcatPermissionsHelper#allow_gridview_ordering?` | **42/118 orgs** (35.6%) |
| 1.17 | **FlipBook / interactive PDFs** | View flipbook-format catalogs with hotspot linking to products; increased document upload limits (30→150MB, 1→4GB storage) | Subscription plan ($195/mo) + org flag `enable_flipbook_support` | $195/mo | `FlipbookProductViewController`, `FlipbookFrameViewController`, `FlipbookAddToOrderViewController` (iOS); org flag `enable_flipbook_support` | **5/118 orgs** (4.2%) |
| 1.18 | **Credit card capture** | Capture and store credit card information on orders; charge cards at submission | Subscription plan ($195/mo) + org flag `enable_charging_credit_cards` | $195/mo | `AddPaymentInformationViewController`, `SelectPaymentInformationViewController` (iOS); `PaymentIntegrations` service; org `payment_integration_configuration` | **5-6/118 orgs** (~5%) |
| 1.19 | **Image upgrade (6→12)** | Increase product image slots from 6 to 12 per product | Org property `enable_twelve_product_images` | $95/mo (manual billing) | Org flag `enable_twelve_product_images` in `Organization::FLAGS` | **0/118** via flag (billed externally) |
| 1.20 | **Copy order** | Duplicate an existing order as a new draft | Org property `enable_copy_order` | Included | `CopyOrderViewController` (iOS); org flag `enable_copy_order` | **0/118 orgs** (feature exists, not enabled) |
| 1.21 | **Shared order drafts** | Hand off order drafts between iPad and eOL surfaces | Org property `enable_shared_orders` | Included | `OrderHandoffViewController` (iOS); `SharedOrderDraft` model; API routes | **0/118** explicitly enabled (system creates drafts during normal submission for 111/244 orgs) |
| 1.22 | **Contract pricing** | Customer-specific contract prices that override price-level pricing | Org column `contract_pricing_enabled` | Included | `contract_prices.json` sync; `ContractPrices` local table (iOS); `Products::PriceCalculator`; org flags `contract_pricing_enabled`, `contract_prices_always_win` | **38/118 orgs** (32.2%) |
| 1.23 | **Sales data / customer favorites** | View customer purchase history and favorites in catalog context | Org column `enable_sales_data` + `customer_favorites_enabled` | Included | `customer_favorites.json` sync; `CustomerFavorites` local table (iOS) | **92/118 orgs** (78%) |
| 1.24 | **Notices / announcements** | Push notifications/announcements to iPad users | Org admin permission `manage_notices` | Included | `NoticesViewController`, `SuperCatNoticesViewController` (iOS); `Notices` model + controller | Universal (admin feature) |

### Embedded Portal on iPad

| # | Capability | What It Does | Gate | Code Evidence | Adoption |
|---|-----------|-------------|------|--------------|----------|
| 1.25 | **Sales Portal (embedded WebView)** | Full Sales Portal experience embedded in iPad via WKWebView | Requires Sales Portal subscription ($395/mo) | `TerritoryPortalViewController` (iOS, WKWebView wrapper); `TerritoryViewController` | Same as Portal adoption (32 orgs) |

---

## Surface 2: eCat Online (eOL Web)

**Code evidence**: `code/supercat_server/app/controllers/ecat_*_controller.rb` (11 controllers), routes under `/:org_shortname/e/:mobile_site_name/`

### Sub-surface 2A: Online Catalog

**Subscription**: $295/mo (48 active orgs)
**Gate**: Mobile site column `enable_online_catalog` (default: true)

| # | Capability | What It Does | Code Evidence | Adoption |
|---|-----------|-------------|--------------|----------|
| 2.1 | **Product browsing** | Browse products by tradename, collection, category, group; left-nav taxonomy navigation with drill-down | `EcatProductsController#index`; `CatalogController` (left-nav dataflow); routes for products | 48 orgs (catalog subscription) |
| 2.2 | **Product detail** | Product page with images, options preview, pricing, inventory, custom fields | `EcatProductsController#show`, `#by_number` | 48 orgs |
| 2.3 | **Product search & filtering** | Search products; apply taxonomy filters; clear filters | `EcatController#set_filter`, `#clear_filter`; `SelectProductFilterViewController` equivalent | 48 orgs |
| 2.4 | **Favorites** | Mark products as favorites; view favorites list | `EcatProductsController#favorites`; `EcatController#email_favorites` | 48 orgs |
| 2.5 | **Library / documents** | Browse and download shared resources | `EcatController#library`; gated by MS flag `enable_online_library` | 0/61 mobile sites have `enable_online_library` flag set (may be managed differently) |
| 2.6 | **User account** | My account, change password, change email, preferred pricing | `EcatController#my_account`, `#change_password`, `#change_email`, `#preferred_pricing` | 48 orgs |

### Sub-surface 2B: B2B Cart (Online Ordering)

**Subscription**: $295/mo (26 active orgs)
**Gate**: Mobile site column `enable_online_ordering` + `EcatPermissionsHelper#user_type_allows_ordering?`

| # | Capability | What It Does | Code Evidence | Adoption |
|---|-----------|-------------|--------------|----------|
| 2.7 | **Shopping cart** | Add products to cart, update quantities, configure options, delete items, clear cart | `EcatOrderProcessController#add_to_cart`, `#add_multiple_to_cart`, `#update_cart_item`, `#delete_cart_item`, `#clear_cart` | 26 orgs (cart subscription); 35/61 mobile sites have `enable_online_ordering` |
| 2.8 | **Product configuration (eOL)** | Configure option sets during add-to-cart; option mapping filtering; riser price updates | `EcatOrderProcessController#qty_notes_popup`, `#product_option_set`; `_option_set.erb` partial; Turbo Frame price updates | Available to cart subscribers with configurable products |
| 2.9 | **Kit ordering (eOL)** | Add kit products to order with per-kit-item configuration | `EcatOrderProcessController#add_kit_to_order` | Available to cart subscribers with kit items |
| 2.10 | **Checkout flow** | Multi-step checkout: review → payment info → submit → confirmation | `EcatOrderProcessController#checkout`, `#checkout_review`, `#checkout_edit_payment_information`, `#submit` | 26 orgs |
| 2.11 | **Order confirmation email** | Compose and send order confirmation to buyer, rep, order email | `EcatOrderProcessController#compose_confirmation`, `#send_confirmation`; MS flags `send_order_confirmation_emails`, `send_confirmation_email_to_rep_of_record` | 26 orgs |
| 2.12 | **Projects** | Save product selections as named projects; add/remove products; migrate, restore, email | `EcatProjectsController` (full CRUD + `add_product`, `remove_product`, `migrate`, `email`) | Available to catalog/cart subscribers |

### Sub-surface 2C: Closed Site (Authenticated Access)

**Subscription**: $100/mo (43 active orgs)
**Gate**: Mobile site columns `allows_authenticated_users` + `allows_unauthenticated_users`

| # | Capability | What It Does | Code Evidence | Adoption |
|---|-----------|-------------|--------------|----------|
| 2.13 | **Authenticated-only access** | Restrict catalog browsing to logged-in users (no public access) | `EolController` session management; MS `allows_authenticated_users` / `allows_unauthenticated_users` flags | 43 orgs |
| 2.14 | **Self-service enrollment** | Allow buyers to request accounts; admin approval workflow; delegated enrollment | `EcatEnrollmentController#request_account`, `#enrollment`; `EnrollmentController` (admin); org flag `enrollment_enabled`; MS flag `enable_enrollment_by_users` | 56/118 orgs have enrollment enabled; 39/118 had applicants in 90d |

### Sub-surface 2D: Buyer Session Features

| # | Capability | What It Does | Code Evidence | Adoption |
|---|-----------|-------------|--------------|----------|
| 2.15 | **Authentication** | Login/logout, forgot username/password, password reset | `EcatSessionsController#login`, `#logout`, `#forgot_username`, `#forgot_password`, `#reset_password` | Universal for eOL |
| 2.16 | **Organization switching** | Users belonging to multiple orgs can switch context | `EcatController#change_org` | Available when user has multiple org memberships |
| 2.17 | **RMA requests** | Request returns/exchanges against invoices | `EcatRmaRequestsController#new`, `#create`; `EcatInvoicesController#rma_request`; gated by `EcatPermissionsHelper#allow_rma?` (org `enable_rma` + rma_return_codes exist) | **0/118** orgs with `enable_rma` active; minimal adoption |

---

## Surface 3: Sales Portal

**Subscription**: $395/mo (32 active orgs)
**Gate**: Mobile site column `enable_sales_portal` + `EcatPermissionsHelper#allow_view_sales_portal?` (checks user type permission)
**Code evidence**: `EcatDashboardController`, `EcatOrdersController`, `EcatInvoicesController`, `EcatCustomersController`, `EcatReportsController`

| # | Capability | What It Does | Code Evidence | Adoption |
|---|-----------|-------------|--------------|----------|
| 3.1 | **Dashboard home** | Sales overview: top products, top tradenames, top collections, top customers, top territories; backlog and invoice totals | `EcatDashboardController#index`, `#top_products`, `#top_tradenames`, `#top_collections`, `#top_customers`, `#top_territories`, `#backlog_total`, `#invoice_total` | 32 orgs (portal subscription); 36/61 mobile sites enabled |
| 3.2 | **Sales graphs** | Visual sales performance graphs; budget graphs; all-period graphs | `EcatDashboardController#graph`, `#budget_graph`, `#all_graph` | 32 orgs |
| 3.3 | **Customer management** | Customer listing with sales totals (LY, CY, backlog); open orders by customer; purchase export | `EcatCustomersController#index`, `#show`, `#ly_sales_total`, `#cy_sales_total`, `#backlog_total`, `#open_orders`, `#export_purchases` | 32 orgs |
| 3.4 | **Order management** | View submitted orders; order detail; email order | `EcatOrdersController#index`, `#show`, `#email_order`; filter by date, customer, territory | 32 orgs; 283K portal orders across 38 orgs |
| 3.5 | **Invoice management** | View invoices; invoice detail; CSV export; email invoice | `EcatInvoicesController#index`, `#show`, `#export_csv`, `#email_invoice` | 32 orgs |
| 3.6 | **Reports** | Product detail report, monthly report, sales summary; CSV/XLSX export | `EcatReportsController#product_detail`, `#monthly`, `#sales_summary`, `#export_csv` | 32 orgs |
| 3.7 | **Data export** | Export customer purchases, invoices, reports as CSV | Gated by `EcatPermissionsHelper#allow_export_eol_data?` (user type permission) | 32 orgs |

### Portal Sub-features (Gated Within Portal)

| # | Capability | Gate | Code Evidence | Adoption |
|---|-----------|------|--------------|----------|
| 3.8 | **Portal dashboard (advanced)** | Org property `enable_portal_dashboard` + feature flag `portal_portal` + user type permission | `EcatPermissionsHelper#should_display_portal_dashboard?` | 0/118 via org flag |
| 3.9 | **Advanced reports** | Feature allowlist `advanced_reports` (org + user level) | `EcatPermissionsHelper#should_display_advanced_reports?` | Code-level allowlist (not broadly enabled) |
| 3.10 | **Customer dashboard** | Link from customer view to detailed dashboard | Org flag `link_to_customer_dashboard` + feature allowlist; `EcatPermissionsHelper#allow_view_customer_dashboard?` | Code-level allowlist |

---

## Surface 4: Admin Console

**Included with**: eCat iPad subscription (no separate charge)
**Code evidence**: `code/supercat_server/app/controllers/` (60+ admin controllers), routes under `/:org_shortname/`
**Access control**: `UserTypePermissions` model with 16 admin permissions

### Core Admin Capabilities

| # | Capability | UserType Permission | Code Evidence |
|---|-----------|-------------------|--------------|
| 4.1 | **Dashboard** | `view_dashboard` | `SiteController#dashboard` |
| 4.2 | **Product catalog browsing** | `view_products` | `ProductsController#index`, `#show` |
| 4.3 | **Taxonomy management** (categories, collections, tradenames, groups) | `view_products` | `CategoriesController`, `CollectionsController`, `TradeNamesController`, `GroupsController` (full CRUD + reorder) |
| 4.4 | **Smart stacks management** | `manage_smart_stacks` | `SmartStacksController` (CRUD + preview + reorder) |
| 4.5 | **Customer management** | `view_customers` | `CustomersController` (CRUD); `CustomerCustomFieldsController` |
| 4.6 | **Order management** | `view_orders` / `manage_orders` | `OrdersController` (CRUD + export CSV + print); `OrderItemsController` |
| 4.7 | **User management** | `view_users` / `manage_users` / `manage_users_limited` | `OrgUsersController` (CRUD + search + import/export CSV); `UserTypesController`; `UserStacksController` |
| 4.8 | **User enrollment management** | `manage_user_enrollment` | `EnrollmentController` (admin side) |
| 4.9 | **Library / shared resources** | `manage_library` | `SharedResourcesController` (CRUD + reorder directories/entries) |
| 4.10 | **Reports (iPad)** | `manage_catalogs` | `IpadReportsController` (CRUD + generate XLSX + tearsheet) |
| 4.11 | **Reports (sales/admin)** | `view_sales_reports` / `view_admin_reports` | `ReportsController` (product summary/detail, monthly, sales summary, orders, CSV/XLSX export) |
| 4.12 | **Price level management** | (admin access) | `PriceLevelsController` (CRUD + reorder) |
| 4.13 | **Mobile site management** | (admin access) | `MobileSitesController` (CRUD) |
| 4.14 | **Import monitoring** | (admin access) | `ImportEventsController#index`, `#show` |
| 4.15 | **Tools** (missing images, user usage, file upload, refresh inventory) | `view_admin_reports` | `ToolsController` |
| 4.16 | **Custom fields** (product, customer, order, inventory, option) | (admin access) | `CustomFieldsController`, `CustomerCustomFieldsController`, `OrderCustomFieldsController`, `InventoryCustomFieldsController`, `OptionCustomFieldsController` |
| 4.17 | **Notices / announcements** | `manage_notices` | `NoticesController` (CRUD + reorder) |

### Admin Capabilities Related to Gated Features

| # | Capability | Requires | Code Evidence |
|---|-----------|---------|--------------|
| 4.18 | **Option mappings management** | CPQ subscription | `OptionMappingsController` (CRUD + connections) |
| 4.19 | **Option forms management** | Feature allowlist `option_forms` | `OptionFormsController`, `OptionFormFieldsController` |
| 4.20 | **Kit items management** | CPQ subscription + org flag `kit_items_enabled` | `KitItemsController#index` |
| 4.21 | **Contract prices management** | Org flag `contract_pricing_enabled` | `ContractPricesController#index` |
| 4.22 | **Surcharge management** | Org flag `enable_auto_add_surcharges` | `SurchargeTypesController` (CRUD) |
| 4.23 | **Distribution centers** | Org flag `enable_distribution_centers` | `DistributionCentersController` (CRUD) |
| 4.24 | **RMA configuration** (custom fields, return codes) | Org flag `enable_rma` | `RmaCustomFieldsController`, `RmaReturnCodesController` |
| 4.25 | **Payment methods** | Credit Card subscription | `PaymentMethodsController` |
| 4.26 | **Order credit card transactions** | `manage_credit_card_transactions` permission | `OrdersController#charge`, `#transactions` |
| 4.27 | **Placement reports** | Org flags for placement features | `PlacementReportsController` (create, index, export CSV) |
| 4.28 | **Commitment reports** | Feature allowlist `market_commitments` | `CommitmentReportsController` |

---

## Surface 5: Data Integration & Platform

**Not a user-facing surface**, but critical for packaging:

| # | Capability | What It Does | Gate | Adoption |
|---|-----------|-------------|------|----------|
| 5.1 | **FTP data import** | Automated product/customer/inventory sync via FTP file drops | Org flag `enable_ftp_import` (default: true) | Universal |
| 5.2 | **Order export / ERP integration** | Export submitted orders as STD JSON v2 to customer ERP | Org export configuration | Unknown (no flag) |
| 5.3 | **Address verification** | Verify shipping addresses during checkout via third-party service | Org `address_verification_configuration` | 89/244 orgs had verified orders in 90d |
| 5.4 | **CDN / image hosting** | Dedicated CDN configuration for product images | `CdnConfigurationsController` | Configuration-based |
| 5.5 | **API access** (external) | Pull orders via external JSON API | API credentials + routes `/:org_shortname/ext/new_orders` | Configuration-based |
| 5.6 | **Bluelink integration** | Available-to-promise and freight/fuel lookups | `BluelinkController` | Customer-specific |

---

## Adoption Summary — Gatable Capabilities

Ranked by current adoption among 118 active orgs:

| Capability | Adoption | Current Gate | Current Price | M3 Gate Candidate? |
|-----------|---------|-------------|--------------|-------------------|
| Sales data / customer favorites | 92 (78%) | Org flag | Included | Base (table stakes) |
| Camera scanning | 82 (70%) | Org flag | Included | Base (table stakes) |
| Enrollment | 56 (47%) | Org flag | Included | Base or Tier 2 |
| Public catalog (eOL) | 48 (41%) | Subscription | $295/mo | Tier gate |
| Closed site | 43 (36%) | Subscription | $100/mo | Tier gate or add-on |
| Gridview ordering | 42 (36%) | Org flag | Included | Tier gate candidate |
| Contract pricing | 38 (32%) | Org flag | Included | Tier gate candidate |
| Sales Portal | 32 (27%) | Subscription | $395/mo | Tier gate |
| B2B Cart | 26 (22%) | Subscription | $295/mo | Tier gate |
| Kit items (data presence) | 25 (21%) | Data-driven | Included with CPQ | Included with CPQ |
| CPQ / configurable products | 18 (15%) | Subscription | $195-$795/mo | Add-on or tier gate |
| Riser prices | 6 (5%) | Data-driven | Included with CPQ | Included with CPQ |
| FlipBook | 5 (4%) | Subscription + flag | $195/mo | Add-on |
| Credit card capture | 5-6 (5%) | Subscription + flag | $195/mo | Add-on |
| PCI compliance | 1 (<1%) | Subscription | $195/mo | Add-on |
| Enhanced support | 1 (<1%) | Subscription | $850/mo | Service add-on |
| Image upgrade (6→12) | ~few | Manual billing | $95/mo | Add-on or tier perk |
| Copy order | 0 | Org flag | Included | Feature exists but unused |
| Shared orders | 0 | Org flag | Included | Feature exists but unused |
| RMA | 0 | Org flag + MS flag | Included | Feature exists but unused |
| Portal dashboard (advanced) | 0 | Org flag | Included | Feature exists but unused |

---

## Key Findings for M3

### 1. The Current Architecture Is Modular, Not Tiered
Today's billing uses **à la carte subscription plans** stacked on top of each other. An org subscribes to iPad ($725), then separately adds Catalog ($295), Cart ($295), Portal ($395), Closed Site ($100), CPQ ($195), etc. There are no tiers — just module stacking.

### 2. Five Natural Packaging Surfaces Exist
The product has five distinct surfaces that could serve as tier fences:
1. **iPad App** (catalog + ordering) — the core product
2. **Online Catalog** (buyer-facing browse)
3. **B2B Cart** (buyer-facing ordering)
4. **Sales Portal** (rep/manager analytics)
5. **Configurable Products / CPQ** (specialized capability)

### 3. Configurable Products Is a Meaningful Differentiator
CPQ is the **only iPad capability with separate monetization** ($195/mo add-on or $795/mo bundle). 18 orgs pay for it. It enables a fundamentally different product experience — configurable ordering with option sets, mappings, riser pricing, and kit items. This is a strong tier fence or add-on candidate.

### 4. Many "Gated" Features Are Actually Free
Camera scanning (70% adoption), contract pricing (32%), gridview ordering (36%), enrollment (47%), and sales data (78%) are all gated by org flags but not monetized. These represent either:
- **Table-stakes** features that should be in base (camera scanning, sales data)
- **Tier-fence candidates** that could justify premium positioning (contract pricing, gridview ordering)

### 5. Feature Flag Debt Is Significant
60+ org-level flags, 15+ mobile site flags, 30+ code-level allowlists, and 16 admin permissions create a complex permission matrix. For M3, the packaging architecture should simplify this to a manageable number of tier-determining gates.

### 6. eOL Feature Menu Note
The feature menu reported "eOL: No" for Kit items & configurable ordering (line 54), but code evidence shows `EcatOrderProcessController#add_kit_to_order`, `#qty_notes_popup`, and `_option_set.erb` are fully functional in eOL. **Configurable ordering IS available on eOL web**, not just iPad — the feature menu was inaccurate on this point.

---

## Appendix: Complete Organization Flag Reference

### Organization Boolean Columns (Direct Attributes)
`mobile_enabled`, `enable_split_discounting_behavior`, `enable_import_users`, `enrollment_enabled`, `enable_camera_scanning`, `enable_gridview_ordering`, `enable_sales_data`, `contract_pricing_enabled`, `customer_favorites_enabled`, `imports_options`, `disable_sync`, `disable_upc_validation`, `hide_order_totals`, `skip_nonconfirmed_orders`, `enable_item_email_template`, `matrix_completeness_warning`, `alphabetize_shared_resources`, `alphabetize_collections`, `collection_related_items`, `is_multifile`, `order_by_pack`, `send_order_email_on_submit`, `expand_collections_to_groups`, `expand_groups_to_collections`, `product_synch_requires_photo`, `legacy_display_all_customers`, `legacy_allow_discounting`, `legacy_allow_scanned_orders`

### Organization Property Flags (JSON, 56 flags)
`kit_items_enabled`, `allow_editing_individual_kit_item_quantities`, `group_kit_items_with_order_item_notes`, `require_order_type_on_submission`, `enable_order_review`, `show_price_level_on_order`, `attach_pdf_to_order_email`, `enable_ftp_import`, `enable_restricting_order_resubmission`, `display_placement_report_quantities`, `enable_placement_reports_for_all_shipping_locations`, `include_missing_customers_in_placements_export`, `enable_historical_placements`, `prune_historical_orders_on_ipad`, `import_taxonomies`, `enable_customer_duplication_mitigation`, `enable_portal_dashboard`, `enable_rep_enrollment`, `enable_admin_order_reporting`, `enable_distribution_centers`, `enable_shared_orders`, `require_address_for_local_customers`, `require_online_order_submission`, `placements_includes_discontinued_products`, `enable_delegated_enrollment`, `drilldown_leftnav_collections`, `drilldown_leftnav_categories`, `drilldown_library_items`, `require_valid_options_to_submit_orders`, `enable_placements_gallery_audit`, `enable_auto_add_surcharges`, `enable_flipbook_support`, `enable_copy_order`, `enable_twelve_product_images`, `enable_portal_delta_imports`, `enable_rma`, `allow_double_discounting`, `cc_buyer_on_order_email`, `restrict_changing_tradename_filter`, `customer_tradename_filters`, `enable_country_validation`, `enable_charging_credit_cards`, `require_unique_po_numbers`, `enable_order_ship_date`, `enable_order_cancel_date`, `enable_changed_address_warning`, `display_ship_to_code_in_shipping_address`, `enable_export_images`, `enable_product_notes`, `link_to_customer_dashboard`, `enable_row_view`, `enable_back_button`, `enable_order_item_email_templates`, `enable_strict_tcgc_import_validation`, `enable_new_product_importer`, `contract_prices_always_win`

### Mobile Site Flags (15 flags)
`send_order_confirmation_emails`, `send_confirmation_email_to_rep_of_record`, `enable_enrollment_by_users`, `enable_online_library`, `enable_product_image_download`, `enable_rma_processing`, `collapse_left_nav_tcgc`, `hide_in_global_site_switcher`, `enable_tearsheet_download`, `self_service_enrollment_enabled`, `display_quantity_available`, `display_quantity_backordered`, `charge_credit_card_at_checkout`, `enable_customer_dashboard_landing_page`, `hide_products_marked_hideable`

### Code-Level Feature Allowlists (27 org-level features)
`advanced_reports`, `tcgc_name_fields`, `market_commitments`, `override_company_info_at_group`, `manage_smart_stacks_permission`, `price_level_enforce_order_quantity`, `more_placement_fields`, `allow_user_group_from_selecting_price_levels`, `backlog_instead_of_amount_invoiced`, `enable_disable_portal_export_by_user_group`, `eol_customer_graph`, `option_forms`, `asi_shared_orders`, `twenty_option_types`, `minimum_ecat_version`, `territory_access_via_rep_number`, `admin_rma_email_notification`, `override_order_footer_text`, `suppress_buyer_email`, `eol_dashboard_filters`, `promo_price_level`, `link_to_customer_dashboard`, `order_item_tags`, `rma_custom_fields`, `ship_cancel_date_tweaks`, `org_user_ship_to_code`, `internal_warehouse_unsubmitted_orders`
