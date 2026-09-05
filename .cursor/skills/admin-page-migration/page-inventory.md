# Admin Page Migration Inventory

Full tracking list derived from `docs/design/admin-page-taxonomy.yaml`. Each row is one migration unit.

## Org Admin Pages

| ID | Page | Controller | Archetype | Sprint | Status |
|----|------|-----------|-----------|--------|--------|
| `home` | Home | `SiteController#index` | `hub` | 1 | |
| `dashboard` | Dashboard | `SiteController#dashboard` | `dashboard` | 3 | |
| `dashboard_images` | Image Counts | `SiteController#dashboard_images` | `report` | 3 | |
| `users_list` | Users | `OrgUsersController#index` | `index` | 2 | |
| `invitations` | Invitations | `Admin::OrganizationInvitationsController` | `index` | 2 | |
| `user_groups` | User Groups | `UserTypesController` | `index` | 2 | |
| `enrollment` | Enrollment | `EnrollmentController` | `workflow` | 4 | |
| `orders_list` | Orders | `OrdersController#index` | `index` | 2 | |
| `order_custom_fields` | Custom Fields | `OrderCustomFieldsController` | `index` | 2 | |
| `surcharges` | Surcharges | `SurchargeTypesController` | `index` | 2 | |
| `order_item_tags` | Order Item Tags | `OrderItemTagGroupsController` | `index` | 2 | |
| `product_detail_report` | Product Detail | `ReportsController#product_detail` | `report` | 3 | |
| `sales_summary_report` | Summary | `ReportsController#sales_summary` | `report` | 3 | |
| `orders_report` | Orders Report | `ReportsController#orders` | `report` | 3 | |
| `products_list` | Products | `ProductsController#index` | `index` | 2 | |
| `trade_names` | Trade Names | `TradeNamesController` | `index` | 2 | |
| `groups_categories` | Groups & Categories | `GroupsController` | `index` | 2 | |
| `product_custom_fields` | Custom Fields | `CustomFieldsController` | `index` | 2 | |
| `options` | Options | `OptionGroupsController` | `index` | 2 | |
| `option_forms` | Option Forms | `OptionFormsController` | `index` | 2 | |
| `price_levels` | Price Levels | `PriceLevelsController` | `index` | 2 | |
| `distribution_centers` | Distribution Centers | `DistributionCentersController` | `index` | 2 | |
| `inventory_custom_fields` | Inventory Custom Fields | `InventoryCustomFieldsController` | `index` | 2 | |
| `option_custom_fields` | Option Custom Fields | `OptionCustomFieldsController` | `index` | 2 | |
| `option_mappings` | Option Mappings | `OptionMappingsController` | `index` | 2 | |
| `customers_list` | Customers | `CustomersController#index` | `index` | 2 | |
| `customer_custom_fields` | Customer Custom Fields | `CustomerCustomFieldsController` | `index` | 2 | |
| `smart_lists` | SmartLists | `SmartStacksController` | `index` | 2 | |
| `library` | Library | `SharedResourcesController` | `media_library` | 4 | |
| `presentation_formats` | Presentation Formats | `IpadReportsController#index` | `index` | 2 | |
| `org_tearsheet` | Organization Tearsheet | `IpadReportsController#org_tearsheet_edit` | `form` | 2 | |
| `notices` | Notices | `NoticesController` | `index` | 2 | |
| `company_settings` | Company Settings | `OrganizationsController#edit` | `settings_form` | 4 | |
| `integration_settings` | Integration Settings | `OrgSettingsController#index` | `settings_form` | 4 | |
| `mobile_sites` | Mobile Sites | `MobileSitesController` | `index` | 2 | |
| `rma_custom_fields` | RMA Custom Fields | `RmaCustomFieldsController` | `index` | 2 | |
| `rma_return_codes` | RMA Return Codes | `RmaReturnCodesController` | `index` | 2 | |
| `detailed_usage` | Detailed Usage | `ToolsController#user_usage` | `report` | 3 | |
| `summary_usage` | Summary Usage | `ToolsController#user_usage_summary` | `report` | 3 | |
| `inactive_users` | Inactive Users | `ToolsController#inactive_user` | `report` | 3 | |
| `file_import_status` | File Import Status | `ImportEventsController#index` | `index` | 2 | |
| `image_counts` | Image Counts | `SiteController#dashboard_images` | `report` | 3 | |
| `missing_images` | Missing Images | `ToolsController#missing_images` | `report` | 3 | |
| `missing_option_images` | Option Images Missing | `ToolsController#missing_option_images` | `report` | 3 | |
| `missing_primary_images` | Missing Primary Images | `ToolsController#missing_images` | `report` | 3 | |
| `orphan_product_images` | Orphan Product Images | `ToolsController#extra_images` | `report` | 3 | |
| `orphan_option_images` | Orphan Option Images | `ToolsController#orphan_option_images` | `report` | 3 | |
| `presentation_format_usage` | Format Usage | `PresentationFormatReportsController#new` | `report` | 3 | |
| `import_products` | Import Products | `ToolsController#index` | `upload` | 3 | |
| `import_product_images` | Import Product Images | `ToolsController#index` | `upload` | 3 | |
| `import_inventories` | Import Inventories | `ToolsController#index` | `upload` | 3 | |
| `import_customers` | Import Customers | `ToolsController#index` | `upload` | 3 | |
| `import_customer_pricing` | Import Customer Pricing | `ToolsController#index` | `upload` | 3 | |
| `import_orders` | Import Orders | `ToolsController#index` | `upload` | 3 | |
| `import_users` | Import Users | `OrgUsersController#import_users` | `upload` | 3 | |
| `refresh_websan` | Refresh Websan Data | `ToolsController` | `utility` | 5 | |
| `refresh_bluelink` | Refresh Bluelink Data | `ToolsController` | `utility` | 5 | |
| `customer_file_uploads` | Customer File Uploads | `Admin::OnboardingFileUploadsController` | `index` | 2 | |
| `payment_methods` | Payment Methods | `PaymentMethodsController` | `form` | 2 | |
| `org_subscriptions` | Subscriptions | `SubscriptionsController` | `index` | 2 | |
| `org_stripe_invoices` | Invoices | `StripeInvoicesController` | `index` | 2 | |

## SuperCat Admin Pages

| ID | Page | Controller | Archetype | Sprint | Status |
|----|------|-----------|-----------|--------|--------|
| `sc_organizations` | Organizations | `OrganizationsController#index` | `index` | 2 | |
| `sc_org_new` | New Organization | `OrganizationsController#new` | `form` | 2 | |
| `sc_org_clone` | Clone Organization | `OrganizationsController#new_clone` | `wizard` | 4 | |
| `sc_users_list` | Users | `UsersController#index` | `index` | 2 | |
| `sc_export_users` | Export Users | `UsersController#export_csv` | `export` | 3 | |
| `sc_customer_files` | Customer Files | `Admin::OnboardingFileUploadsController#all_uploads` | `index` | 2 | |
| `sc_all_subscriptions` | All Subscriptions | `SubscriptionsController#index` | `index` | 2 | |
| `sc_subscription_plans` | Subscription Plans | `SubscriptionPlansController` | `index` | 2 | |
| `sc_stripe_invoices` | Stripe Invoices | `StripeInvoicesController` | `index` | 2 | |
| `sc_help_files` | Help Files | `HelpInfosController` | `index` | 2 | |
| `sc_broadcasts` | eCat Broadcasts | `EcatBroadcastsController` | `index` | 2 | |
| `sc_user_merge` | Merge Users | `UserMergesController#new` | `wizard` | 4 | |
| `sc_latest_import_events` | Latest Import Events | `AdminReportingController` | `report` | 3 | |
| `sc_feature_usage` | Org Feature Usage | `AdminReportingController` | `report` | 3 | |
| `sc_statistics` | SuperCat Statistics | `AdminReportingController` | `report` | 3 | |
| `sc_unique_eol_logins` | Unique eOL Logins | `AdminReportingController` | `report` | 3 | |
| `sc_login_events` | Login Events | `AdminReportingController` | `report` | 3 | |
| `sc_jobs` | Current Jobs | `AdminReportingController` | `report` | 3 | |
| `sc_import_files` | Latest Import Files | `AdminReportingController` | `report` | 3 | |
| `sc_recent_imports` | Recent Import Events | `AdminReportingController` | `report` | 3 | |
| `sc_import_file_counts` | Import File Counts | `AdminReportingController` | `report` | 3 | |
| `sc_features` | Managed Features | `AdminReportingController` | `index` | 2 | |
| `sc_unique_devices` | Unique Devices | `AdminReportingController` | `report` | 3 | |
| `sc_memcache` | Memcache Stats | `AdminReportingController` | `report` | 3 | |
| `sc_cache_hit_ratio` | Cache Hit Ratio | `AdminReportingController` | `report` | 3 | |
| `sc_bloat` | Bloat | `AdminReportingController` | `report` | 3 | |
| `sc_underused_indexes` | Underused Indexes | `AdminReportingController` | `report` | 3 | |
| `sc_query_performance` | Query Performance | `AdminReportingController` | `report` | 3 | |
| `sc_warehouse_status` | Warehouse Status | `AdminReportingController` | `report` | 3 | |
| `sc_investigate_portal` | Investigate Portal | `AdminReportingController` | `utility` | 5 | |
| `sc_identify_image` | Identify Image/PDF | `AdminReportingController` | `utility` | 5 | |

## Global Pages

| ID | Page | Controller | Archetype | Sprint | Status |
|----|------|-----------|-----------|--------|--------|
| `login` | Sign In | `SessionsController#new` | `auth` | 1 | |
| `my_account` | My Account | `UsersController#my_account` | `profile` | 1 | |
| `passkeys` | Passkeys | `PasskeysController` | `settings_form` | 4 | |
| `logout` | Sign Out | `SessionsController#destroy` | `auth` | 1 | |
