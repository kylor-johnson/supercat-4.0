# Stage 1 — Data Collection

**Purpose:** Collect all quantitative metrics and assign stage status per client.
**Runs after:** Step 0 of `RUN_PROMPT.md` (shortnames resolved to orgs + `client_domains`).
**Next step:** `Validation_Layer_Fathom_HelpScout.md`.

**Sources:**
- **Postgres** (`user-supercat-postgres-vpn`) — eCat configuration / stage-readiness. Authoritative; no BigQuery mirror exists for this data.
- **BigQuery** (`user-bigquery-admin`, project `supercat-data-pipeline`) — usage activity + enrichment.

> Anti-hallucination rules apply (see `README.md`). No metric without a tool call. On failure: `❓ QUERY FAILED: [error]`, never substitute.

---

## STEP 1 — PostgreSQL configuration metrics

All eCat config data is queried via `user-supercat-postgres-vpn`.

### Batch pattern (recommended for multi-client runs)

Replace single-client `WHERE o.shortname = '[SHORTNAME]'` with a set and add `o.shortname` to SELECT + `GROUP BY o.shortname`:

```sql
WHERE o.shortname IN ('tcs','pebl','libco','drf')
```

Example (batched product metrics):

```sql
SELECT o.shortname,
  COUNT(*) AS total_products,
  COUNT(CASE WHEN p.image_exists = true THEN 1 END) AS products_with_images,
  COUNT(DISTINCT p.category_code) AS unique_categories,
  COUNT(DISTINCT p.collection_code) AS unique_collections,
  MAX(p.last_modified_at) AS last_product_update
FROM products p
JOIN organizations o ON p.organization_id = o.id
WHERE o.shortname IN ('tcs','pebl','libco','drf') AND p.deleted = false
GROUP BY o.shortname
ORDER BY o.shortname
```

The single-client queries below are the per-client form.

> ⚠️ **Never put a global `LIMIT` on a batched (`IN (...)`) query.** A single `LIMIT N` over multiple orgs is consumed by whichever orgs sort first, silently truncating the rest. This bit a real run: a batched `import_events` query with `LIMIT 120 ORDER BY shortname` let `drf`+`libco` eat the cap and returned **zero** rows for `pebl`/`tcs`. Query 10 (`import_events`) is the one that carries a `LIMIT` — for it, either **run per-client**, or window per org:
> ```sql
> -- safe batched form for any LIMIT/"last N" query
> SELECT * FROM (
>   SELECT o.shortname, ie.id, ie.created_at, LEFT(ie.data::text, 500) AS data_preview,
>     ROW_NUMBER() OVER (PARTITION BY o.shortname ORDER BY ie.created_at DESC) AS rn
>   FROM import_events ie JOIN organizations o ON ie.organization_id = o.id
>   WHERE o.shortname IN ('tcs','pebl','libco','drf')
> ) WHERE rn <= 30
> ```
> Aggregate queries (`COUNT`, `MAX`, `GROUP BY`) are unaffected — the trap is specific to row-returning queries with `LIMIT`.

### Query 1 — Organization info
```sql
SELECT id, name, shortname, created_at, order_email_recipient, send_order_email_on_submit
FROM organizations
WHERE shortname = '[SHORTNAME]'
```

### Query 2 — Product metrics
```sql
SELECT COUNT(*) AS total_products,
  COUNT(CASE WHEN image_exists = true THEN 1 END) AS products_with_images,
  COUNT(DISTINCT category_code) AS unique_categories,
  COUNT(DISTINCT collection_code) AS unique_collections,
  MAX(last_modified_at) AS last_product_update
FROM products p
JOIN organizations o ON p.organization_id = o.id
WHERE o.shortname = '[SHORTNAME]' AND p.deleted = false
```
> Category/collection counts come from `products` (`unique_categories`, `unique_collections`). There are no separate `categories`/`collections` tables.

### Query 3 — Customer metrics
```sql
SELECT COUNT(*) AS total_customers, MAX(updated_at) AS last_customer_update
FROM customers c
JOIN organizations o ON c.organization_id = o.id
WHERE o.shortname = '[SHORTNAME]'
```

### Query 4 — User metrics (excluding SuperCat staff)
```sql
SELECT COUNT(*) AS total_users,
  COUNT(CASE WHEN ou.is_admin = true THEN 1 END) AS admin_users,
  COUNT(CASE WHEN ou.is_admin = false THEN 1 END) AS non_admin_users
FROM org_users ou
JOIN organizations o ON ou.organization_id = o.id
JOIN users u ON ou.user_id = u.id
WHERE o.shortname = '[SHORTNAME]' AND u.email NOT LIKE '%@supercatsolutions.com'
```

### Query 5 — Price levels
```sql
SELECT code, name
FROM price_levels pl
JOIN organizations o ON pl.organization_id = o.id
WHERE o.shortname = '[SHORTNAME]'
ORDER BY code
```

### Query 8 — Options
```sql
SELECT COUNT(*) AS options_count
FROM options opt
JOIN organizations o ON opt.organization_id = o.id
WHERE o.shortname = '[SHORTNAME]'
```
> Count **records** in `options`, not option columns in the schema.

### Query 9 — Territories
```sql
SELECT COUNT(*) AS territory_count
FROM territories t
JOIN organizations o ON t.organization_id = o.id
WHERE o.shortname = '[SHORTNAME]'
```

### Query 10 — Import events (last 30)
```sql
SELECT id, created_at, LEFT(data::text, 500) AS data_preview
FROM import_events ie
JOIN organizations o ON ie.organization_id = o.id
WHERE o.shortname = '[SHORTNAME]'
ORDER BY ie.created_at DESC
LIMIT 30
```
> `data` is YAML text. Look for `:error` entries to identify import failures.

### Query 11 — Inventories
```sql
SELECT COUNT(*) AS inventory_count, MAX(updated_at) AS last_inventory_update
FROM inventories inv
JOIN organizations o ON inv.organization_id = o.id
WHERE o.shortname = '[SHORTNAME]'
```

### Query 12 — Mobile sites (eCat Online / Sales Portal)
```sql
SELECT ms.url_key, ms.custom_cname, ms.title, ms.enable_online_catalog,
  ms.enable_sales_portal, ms.document_logo_file_name
FROM mobile_sites ms
JOIN organizations o ON o.id = ms.organization_id
WHERE o.shortname = '[SHORTNAME]'
```

### Query 13 — Report formats (iPad reports)
```sql
SELECT COUNT(*) AS report_format_count
FROM ipad_reports ir
JOIN organizations o ON ir.organization_id = o.id
WHERE o.shortname = '[SHORTNAME]'
```

### Query 14 — Orders (DB)
```sql
SELECT COUNT(*) AS order_count
FROM orders ord
JOIN organizations o ON ord.organization_id = o.id
WHERE o.shortname = '[SHORTNAME]'
```

### Query 15 — User types & permissions
```sql
SELECT ut.id, ut.name, ut.allow_ipad_logins, ut.enable_online_ordering, ut.allow_user_enrollment
FROM user_types ut
JOIN organizations o ON ut.organization_id = o.id
WHERE o.shortname = '[SHORTNAME]'
ORDER BY ut.name
```

---

## STEP 2 — BigQuery usage metrics

Use `user-bigquery-admin` (project `supercat-data-pipeline`). SQL passes through unchanged — backticks and standard SQL are fine.

### 2a — Usage breadth (per-org snapshot)
```sql
SELECT org_shortname, total_users, active_users, total_logins,
  submit_order, view_ipad_orders, search_products, access_sales_portal,
  create_pdf_catalog, share_my_list, scan_item_with_camera
FROM `supercat-data-pipeline.mixpanel.org_feature_usage_report`
WHERE org_shortname IN ('tcs','pebl','libco','drf')
```
> This view is all-time-ish — use it for "do they use feature X / breadth," **not** for precise recency.

### 2b — iPad orders (precise 90-day window)
```sql
SELECT
  COALESCE(NULLIF(organization_shortname,''), NULLIF(current_organization_shortname,'')) AS org,
  COUNT(*) AS ipad_orders_90d,
  COUNT(DISTINCT username) AS unique_ordering_users,
  CAST(TIMESTAMP_SECONDS(CAST(MAX(time) AS INT64)) AS STRING) AS last_ipad_order
FROM `supercat-data-pipeline.mixpanel.events`
WHERE event_name = 'order_submitted'
  AND time >= UNIX_SECONDS(TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY))
  AND COALESCE(NULLIF(organization_shortname,''), NULLIF(current_organization_shortname,'')) IN ('tcs','pebl','libco','drf')
GROUP BY org
ORDER BY org
```
> `event_name = 'order_submitted'`; `time` is FLOAT unix-seconds; org attribution is 100% populated on the native table — **no `api_access` subquery needed**. Compare this iPad-order count against Postgres Query 14 (`orders`): a gap (Mixpanel events but 0 DB orders) means the order pipeline isn't persisting — flag it.

### 2c — Enrichment (established orgs only)
```sql
SELECT org_shortname, segment, health_score, arr, mrr, billing_status, peer_standing
FROM `supercat-data-pipeline.insightful_product.org_summary`
WHERE org_shortname IN ('tcs','pebl','libco','drf')
```
> Often empty for brand-new onboarding orgs — that is expected, not an error. Use when present for context.

---

## STAGE VALIDATION CRITERIA

### Products supported
| Product | Required stages |
|---|---|
| eCat iPad | 1, 2, 3, 4*, 5, 6, 7 |
| eCat Online | 1, 2, 3, 4*, 5, 6, 8, 9, 10* |
| Sales Portal | 1, 2, 3, 4*, 5, 6, 8, 9, 11 |

\*Conditional on feature enablement.

### Stage 1 — Account Foundation
| Check | Source | TRUE condition |
|---|---|---|
| Company name exists | Q1 | `name` not empty |
| Account active | Q1 | org record exists |
| Admin user exists | Q4 | ≥1 `is_admin = true` (non-SuperCat) |

🔴 any FALSE · 🟢 all TRUE

### Stage 2 — Catalog Setup
| Check | Source | TRUE condition |
|---|---|---|
| Products imported | Q2 | `total_products >= 10` |
| Products have images | Q2 | `products_with_images >= 10` |
| Categories exist | Q2 | `unique_categories >= 1` |
| Collections exist | Q2 | `unique_collections >= 1` |

🔴 products < 10 · 🟡 10–100 · 🟢 ≥100 (✅ bonus if `last_product_update` within 30d)

### Stage 3 — Pricing
| Check | Source | TRUE condition |
|---|---|---|
| Price levels exist | Q5 | count ≥ 1 |
| Multiple price levels | Q5 | count ≥ 2 |
| Descriptive names | Q5 | names not "Price Level 1/2" |

🔴 count = 0 · 🟡 1 level OR generic names · 🟢 2+ with descriptive names

### Stage 4 — Options (conditional)
| Check | Source | TRUE condition |
|---|---|---|
| Options enabled | Q8 | `options_count > 0` |
| Options configured | Q8 | `options_count >= 5` |

⚪ N/A if options not part of the catalog model (e.g. discrete-SKU lighting/fabric) · 🔴 enabled but broken · 🟡 1–4 · 🟢 5+

### Stage 5 — Customer & User Setup
| Check | Source | TRUE condition |
|---|---|---|
| Customers imported | Q3 | `total_customers >= 10` |
| Users configured | Q4 | `total_users >= 2` |
| Multiple user types | Q15 | count ≥ 2 |

🔴 customers < 10 OR users < 2 · 🟡 customers 10–100 · 🟢 ≥100 (✅ bonus if `last_customer_update` within 30d)

### Stage 6 — Operational Data
| Check | Source | TRUE condition |
|---|---|---|
| No critical import errors | Q10 | no `:error` in last 30 events |
| Inventory data exists | Q11 | `inventory_count > 0` |
| Inventory fresh | Q11 | `last_inventory_update` within 7d |

🔴 import errors OR inventory enabled but empty · 🟡 stale inventory (7+ d) · 🟢 fresh + no errors

### Stage 7 — iPad Order-Ready (eCat iPad)
| Check | Source | TRUE condition |
|---|---|---|
| User types exist | Q15 | >1 user type |
| iPad activity exists | 2b | `ipad_orders_90d >= 1` |
| Report formats configured | Q13 | `report_format_count >= 3` |
| Orders exist | Q14 | `order_count >= 1` |
| Order email configured | Q1 | `order_email_recipient` not null |

⚪ N/A if not implementing iPad · 🔴 any critical FALSE · 🟡 critical pass but order email missing · 🟢 all TRUE

### Stage 8 — eCat Online Site
| Check | Source | TRUE condition |
|---|---|---|
| Site enabled | Q12 | `enable_online_catalog = true` OR `enable_sales_portal = true` |
| Web portal configured | Q12 | `custom_cname` OR `title` not empty |
| Logo uploaded | Q12 | `document_logo_file_name` not null |

⚪ N/A if neither eCat Online nor Sales Portal · 🔴 no site/branding · 🟡 site but no logo · 🟢 enabled + branding + logo

### Stage 9 — eCat Online User Access
| Check | Source | TRUE condition |
|---|---|---|
| Non-public user types | Q15 | ≥1 |
| Non-admin users | Q4 | `non_admin_users >= 1` |
| Multiple user types | Q15 | count ≥ 2 |

⚪ N/A if public site sufficient · 🔴 no user types / no non-admins · 🟡 1 user type · 🟢 multiple + non-admins

### Stage 10 — eCat Online Ordering (B2B)
| Check | Source | TRUE condition |
|---|---|---|
| Order email configured | Q1 | `order_email_recipient` not empty |
| Order email on submit | Q1 | `send_order_email_on_submit = true` |

⚪ N/A if catalog-only · 🔴 no recipient · 🟡 configured but `send_order_email_on_submit = false` · 🟢 both

### Stage 11 — Sales Portal Configuration
| Check | Source | TRUE condition |
|---|---|---|
| Portal enabled | Q12 | `enable_sales_portal = true` |
| Territories configured | Q9 | `territory_count >= 1` |
| Non-admin users | Q4 | `non_admin_users >= 1` |
| Multiple user types | Q15 | count ≥ 2 |

⚪ N/A if no Sales Portal · 🔴 disabled / no territories / no non-admins · 🟡 1 user type · 🟢 enabled + territories + multiple types

---

## OUTPUT OF THIS STAGE (per client)

Record the metrics + stage statuses for hand-off to Stage 2. No validation flags or narrative here.

```markdown
## CLIENT: [SHORTNAME] ([Company Name])
**Data Collection Date:** [RUN_DATE]
**Days Active:** [from created_at]
**Client Domains:** [from Step 0]
**Product(s):** [eCat iPad / eCat Online / Sales Portal]

### Stage Results
| Stage | Status | Evidence |
|---|---|---|
| 1 Account Foundation | [🔴/🟡/🟢] | [metrics] |
| 2 Catalog Setup | [🔴/🟡/🟢] | [X products, Y% images, Z categories] |
| 3 Pricing | [🔴/🟡/🟢] | [X levels: names] |
| 4 Options | [🔴/🟡/🟢/⚪] | [X options or N/A] |
| 5 Customer & User | [🔴/🟡/🟢] | [X customers, Y users] |
| 6 Operational Data | [🔴/🟡/🟢] | [import + inventory status] |
| 7 iPad Order-Ready | [🔴/🟡/🟢/⚪] | [orders, reports, iPad activity] |
| 8 eCat Online Site | [🔴/🟡/🟢/⚪] | [site status] |
| 9 eCat Online Access | [🔴/🟡/🟢/⚪] | [user types] |
| 10 eCat Online Ordering | [🔴/🟡/🟢/⚪] | [order config] |
| 11 Sales Portal | [🔴/🟡/🟢/⚪] | [portal status] |

### Raw Metrics
- Products / with images / categories / collections
- Price levels (names) · Options · Customers · Users (admin/non-admin) · User types
- Territories · Orders (DB) · iPad orders 90d (Mixpanel) · Report formats
- Web portal configured (name) · Last product/customer/inventory update · Import errors (30d)
- Enrichment (if present): segment, health_score, ARR

### Current Stage & Readiness
- Current Stage: [X — name] · Stages Passed: [X/Y] · Readiness: [X]%

### Blockers Identified
1. [from stage checks]
```

---

**Next:** `Validation_Layer_Fathom_HelpScout.md` (matches on `client_domains`).
