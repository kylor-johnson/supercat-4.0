# TAXONOMY — eCat Feature Usage events

**Product SoT for Phase 1** · CTO event mapping (spec)  
**Implementation later:** `config/analytics_taxonomy.yml` (BQ view generator + Rails) — do not hardcode per-category SQL  
**Dataset:** `supercat-data-pipeline.mixpanel`

---

## Categories (6)

| Category | Job (plain language) | Events |
|---|---|---|
| **Search / Find** | Product discovery | `product_search`, `filter_button_pressed`, `product_sort_changed`, `collection_search`, `view_stack`, `view_smart_stack`, `view_kit`, `view_flipbook` |
| **Share** | Sending product info outbound | `item_email_drafted`, `document_email_drafted`, `email_stack`, `pdf_catalog_started`, `pdf_catalog_generated`, `generate_xlsx_catalog`, `csv_report_generated` |
| **Serve** | Customer-context actions | `customer_search`, `customer_selection`, `view_customer_orders`, `view_favorites`, `view_customer_placements`, `view_commitments`, `view_customer_smart_picks`, `view_customer_on_order_items` |
| **Sell** | Order creation / modification | `order_submitted`, `add_configured_item_to_order`, `add_kit_to_order`, `item_added_via_magic_button`, `add_to_order_from_maybe_list`, `copy_order`, `copy_order_items`, `flipbook_add_to_order` |
| **Scan** | Camera / barcode scanning | `item_scanned` |
| **Save** | List / stack curation | `create_stack`, `edit_stack`, `flipbook_add_to_list` |

### KPI callouts (subset of taxonomy)

| KPI | Event / category basis |
|---|---|
| Search actions | All **Search / Find** events |
| Orders submitted | `order_submitted` |
| Items scanned | `item_scanned` |

---

## Excluded meta / system events

These must **not** count toward category totals, leaderboard “total actions,” or category % breakdown:

| Event |
|---|
| `selected_org` |
| `api_access` |
| `view_portal` |
| `pspdfkit_activated` |
| `view_document` |
| `view_notifications` |
| `reload_button_pressed` |
| `search_settings_saved` |
| `smart_search_embeddings_generated` |
| `smart_search_toggled` |
| `show_on_display_setting_changed` |
| `item_scan_failed` |
| `show_customer_sales_setting_changed` |
| `preview_order_show_current_customer_orders` |
| `preview_order_show_territory_orders` |

**Note:** Exclusion list is product SoT for v0. Unlisted events are **not** auto-categorized — do not invent buckets; add via YAML + product decision later.

---

## Org resolution (affects who counts)

- Prefer `organization_shortname` on the event.  
- Else join `user_org_mapping` (username → org).  
- Still NULL → **exclude** (unmapped / test).  
- Encoded in MVs at materialization time (`COALESCE`), not at Rails request time.

---

## YAML shape (implementation hint — not authored this phase)

```yaml
categories:
  search_find:
    label: "Search / Find"
    events: [product_search, filter_button_pressed, ...]
  share:
    label: "Share"
    events: [...]
  # serve, sell, scan, save ...
excluded:
  - selected_org
  - api_access
  # ...
```

---

## Inventory context (reference only — not AC)

| BQ table | Role |
|---|---|
| `mixpanel.events` | Raw events (~9.76M+) |
| `mixpanel.people` | Device / last seen attributes |
| `mixpanel.user_org_mapping` | username → org |
| `mixpanel.organization_customer_mapping` | org → customer / HubSpot |
| `mixpanel.org_feature_usage_report` | Schema only / no date — **do not use for v0** |
| `mixpanel.user_feature_usage_report` | Schema only / no date — **do not use for v0** |

Planned MVs: `mv_org_daily_kpis`, `mv_user_daily_activity`, `mv_user_device_info`.

---

*Taxonomy SoT for Phase 1. Changes require product update here before YAML/MV regen.*
