# Sales Portal settings inventory — SOURCE (pasted from Confluence 2026-07-17)

Confluence: space `EOL`, page id **1813676033**. Preserved here because the page is auth-gated
and MCP access is intermittent. This is the authoritative raw inventory for `08-SETTINGS-AUDIT`.
Source of the catalog: `supercat_server` models + `config/initializers/enabled_features.rb`.
Originally published from a Cursor canvas (`sales-portal-settings-inventory.canvas.tsx`, 2026-07-16).

## Headline counts
- **Catalogued toggles: 134**
- **Feature flag keys: 39**
- **Portal-scoped: 40**
- **Orphaned / unused: 9**

## Why this feels unmanageable
Portal behavior is decided by up to **six layers** with no single admin surface. Feature flags are
code/YAML only (no UI). Company Settings → Sales Portal exposes only two fields today. The SHL /
Ferguson issue (`territory_access_via_rep_number` on for el/ctest only) is the textbook failure: a
data-access rule hidden in deploy config, invisible next to the settings operators already use.

## Long-term fix — one control plane, three audiences
1. **Product capabilities** — promote mature Feature flags into Organization/MobileSite settings with
   clear labels. Kill orphaned flags. Keep YAML only for true kill-switches / canaries with an expiry.
2. **Access policy** — one "Territory & data access" section (territory_key vs customer_key rules,
   access_all_customer_sales_totals, ship_to_code, customer_synching).
3. **Experience polish** — display toggles (currency, backlog statuses, qty columns, graphs, export,
   dashboard) in an expanded Sales Portal Preferences.

## Proposed IA — "Portal & Access" admin hub
| Section | Who edits | What moves here |
|---|---|---|
| Enablement | Org admin | Site `enable_sales_portal`, user-type `enable_sales_portal` / dashboard / totals / export |
| Territory & data access | Superadmin + org admin | `territory_access_via_rep_number` → named setting; `portal_data_type`; `customer_synching` defaults; `access_all_customer_sales_totals` |
| Portal display | Org admin | currency, backlog exclusions, qty columns, customer graph, backlog vs invoiced label |
| Reports & export | Org admin | `advanced_reports`, `xlsx_export`, `can_export_eol_data` — as product settings, not YAML |
| Feature lab (temporary) | Superadmin only | true experiments with owner, ticket, sunset date — replaces open-ended YAML allowlists |

**Migration rule:** if a Feature flag has been org-allowlisted for >2 customers and has a stable UX,
graduate it to a Company Setting. If unused (orphaned), delete. If still experimental, keep in Feature
lab with UI visibility for support.

## Decision layers (today)
| Layer | Storage | Editable in UI? | Count |
|---|---|---|---|
| Feature | `enabled_features.rb` YAML | No — deploy/code change | 39 |
| Organization | columns + properties + FLAGS | Yes — Company Settings | 57 |
| MobileSite | columns + FLAGS | Yes — Mobile Sites | 13 |
| UserType | columns + FLAGS + properties | Yes — User Types | 18 |
| Permissions | `user_types.permissions` JSON | Yes — User Types | 3 |
| OrgUser | `territory_codes`, `ship_to_code`, … | Yes — Users | 4 |

## Portal access is AND/OR spaghetti
`allow_view_sales_portal?` combines `MobileSite.enable_sales_portal`, UserType flags, Feature
`:force_portal_display`, Feature `:portal_portal`, and `Organization.enable_portal_dashboard`.
Territory filtering then optionally adds Feature `:territory_access_via_rep_number`. Operators cannot
see this chain in one place.

## Orphaned / unused flags (9) — delete or wire-up candidates
| Key | Layer | Controls | Enabled for |
|---|---|---|---|
| eol_dashboard_filters | feature | intended portal dashboard filters — no `Feature.enabled?` usage | cci, sarreid |
| sales_quotas | feature | listed for sarreid, not checked via `Feature.enabled?` | sarreid |
| allow_user_group_from_selecting_price_levels | feature | no usage found | ihw, mhc + users |
| option_mapping | feature | no usage — option mappings exist ungated | opame, yw, demos, omc |
| tcgc_name_fields | feature | no usage found | sarreid |
| product_url_variable | feature | product URL custom-field alias when online catalog on | — |
| credit_card_support | feature | adds Customer Payment Information to import file types | — |
| placements_field_configuration | feature | configure placements gridview fields | — |
| avery_5392_landscape | feature | Avery 5392 landscape shape | — |

## Feature flags (YAML) — 39
(see full table below; portal-relevant highlighted in 08 mission)

admin_rma_email_notification · advanced_reports · allow_user_group_from_selecting_price_levels(orphaned) ·
asi_shared_orders · avery_5392_landscape(orphaned) · backlog_instead_of_amount_invoiced ·
credit_card_support(orphaned) · enable_disable_portal_export_by_user_group · eol_customer_graph ·
eol_dashboard_filters(orphaned) · force_portal_display · internal_warehouse_unsubmitted_orders ·
link_to_customer_dashboard · manage_smart_stacks_permission · market_commitments · minimum_ecat_version ·
more_placement_fields · multifile_ephemeral_import · netsuite_rest_api · option_forms ·
option_mapping(orphaned) · order_item_tags · org_user_ship_to_code · override_company_info_at_group ·
override_eol_login · override_order_footer_text · placements_field_configuration(orphaned) · portal_portal ·
price_level_enforce_order_quantity · product_url_variable(orphaned) · promo_price_level · rma_custom_fields ·
sales_quotas(orphaned) · ship_cancel_date_tweaks · suppress_buyer_email · tcgc_name_fields(orphaned) ·
territory_access_via_rep_number · twenty_option_types · xlsx_export

## Layer inventories (summarized)
- **Organization Company Settings (57):** pricing (allow_double_discounting, contract_prices_always_win,
  …), orders (attach_pdf_to_order_email, enable_shared_orders, enable_distribution_centers, …), catalog
  (drilldown_*, kit_items_enabled, enable_twelve_product_images, …), portal (enable_portal_dashboard,
  enable_portal_delta_imports, excluded_portal_order_backlog_order_statuses, sales_portal_currency_code,
  link_to_customer_dashboard, enable_sales_data), hidden (max_portal_data_age_months, portal_calculations
  [legacy vs PORTAL_CALCULATIONS_20180720], portal_data_type [OVERLAPS/DOESNT_OVERLAP/DOESNT_CORRELATE],
  sales_portal_sales_facts_filter_configuration).
- **MobileSite / eOL (13):** enable_sales_portal (master site switch), display_quantity_available,
  display_quantity_backordered, enable_customer_dashboard_landing_page, enable_online_catalog/ordering/
  library/…, price_level_id, smart_stack_filter_id, send_*_email.
- **UserType (18):** *_auth columns, allow_*_discounting, can_export_eol_data, customer_synching
  (All/None/Associated), display_sales_portal_totals, enable_portal_dashboard, enable_sales_portal,
  primary_rep_group, territory_url/label, order_item_quantity_enforcement.
- **UserType permissions (3):** access_all_customer_sales_totals, view_sales_reports, view_* admin perms.
- **OrgUser (4):** settings/ui_preference, ship_to_code, states, territory_codes.

## Metric-law-critical settings (call out — conflict with invoiced-net spine)
- `backlog_instead_of_amount_invoiced` (clm) — shows Backlog Total instead of amount invoiced.
- `portal_data_type` — OVERLAPS / DOESNT_OVERLAP / DOESNT_CORRELATE (changes how facts combine).
- `portal_calculations` — legacy vs PORTAL_CALCULATIONS_20180720.
- `excluded_portal_order_backlog_order_statuses` — which statuses count as backlog/open.
- `sales_portal_currency_code`, `sales_portal_sales_facts_filter_configuration`.

## Suggested next steps (from the page)
1. Graduate `territory_access_via_rep_number` to an org setting (SHL-class bugs become a visible checkbox).
2. Delete or wire up orphaned Feature keys.
3. Expand the Sales Portal Preferences tab (surface site + user-type portal toggles with deep links).
4. Add a Feature-lab UI for remaining YAML flags (support can see experiments without reading the repo).
5. Document the decision tree for `allow_view_sales_portal?` ("Why can't this user see the portal?").

## Notes
- Always-on for shortnames test1/demo/demo1/demo2 (every Feature). All Features on in `Rails.env.test?`.
- Historical migrated flags: s3_images → use_s3_product_images; faster_product_sync → enable_faster_product_sync.
- `OrgSettingRegistry` (integration settings) registrations currently commented out.

> The full 134-row table (per-key Scope / Controls / UI / Default / Status) lives on Confluence page
> 1813676033. If you need a specific row's exact UI location or default, pull it live with
> `getConfluencePage(id=1813676033)`.
