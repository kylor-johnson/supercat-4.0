---
name: ecat-postgres-audit
description: Run read-only Postgres audits of a SuperCat org during eCat onboarding/troubleshooting — counts, import events, image matching, price levels, option/taxonomy state, user-group and distribution-center config. Use when verifying an org's live state by shortname, diagnosing why an import or image didn't take, or checking go-live readiness in the database.
---

# eCat Postgres Org Audit (consultant-only)

Use the `supercat-postgres-vpn` MCP (read-only). Always scope by the org
shortname; read the tool descriptor before the first call. These are starting
templates — confirm exact columns against the schema if a query errors.

First resolve the org id:

```sql
select id, shortname, name, state, properties ->> 'status' as status, import_active from organizations where shortname = '<shortname>';
```

`organizations.state` is the **geographic** state (TX, CA) and `import_active` is the feed
toggle — neither is a lifecycle field. Lifecycle status lives in the `properties` JSONB,
not a column:

```sql
select shortname, properties ->> 'status' as status, import_active
from organizations where shortname = '<shortname>';
```

Values (`Organization::Status`): `onboarding`, `inactive` (the default), `demo`, `test`,
`active`, `sync_suspended`, `fully_suspended`. The two suspended values are the ones with
teeth — `sync_allowed?` is false for both, so a suspended org will not sync no matter how
clean the import. This is the field `eCat_Onboarding/REGISTRY.yaml` means by `lifecycle`.

There is still no field that says "go-live blocked" — derive that from actual counts +
recent imports below (and the health API), never from `status` alone.

## Catalog & images

```sql
-- product + image coverage
select count(*) filter (where not deleted) as active_products,
       count(*) filter (where image_exists) as with_images
from products where organization_id = :org_id;

-- recent imports (backs Admin "File Import Status"; THE source of truth for what
-- actually loaded, not the local CSVs we prepared). `data` is a YAML blob whose
-- top key is the import type (Products/Images/Inventory/Customers/...) and whose
-- entries are tagged :information / :warning / :fatal.
select created_at, left(data, 4000) as data from import_events
where organization_id = :org_id order by created_at desc limit 20;
```

Read the latest event per type: `- []` under a type means a clean import; `:warning`
lines import the good rows but skip deletes; `:fatal` rejects the file. A client may have
run a NEWER import than the file we last sent — always check recency here before assuming
the local CSV reflects the live catalog.

Image not showing → compare `product_images` / `image_digests` against the
`ImageFileName` referenced in products. Files in FTP subfolders never import.

## Pricing & customers

```sql
select code, name, pl_type, factor from price_levels where organization_id = :org_id;
select count(*) from customers where organization_id = :org_id;
select count(*) from inventories where organization_id = :org_id;  -- confirm freshness via updated_at
```

Customer import "succeeded" but 0 rows → every `DefaultPriceCode` failed validation
(e.g. `0` or a status string not in `price_levels`).

## Options / smart SKU builder

```sql
select count(*) from options where organization_id = :org_id;
select count(*) from option_groups where organization_id = :org_id;
-- smart SKU builder is org property JSONB, NOT set by import:
select (properties ->> 'configured_item_number_builder') is not null as has_builder
from organizations where id = :org_id;
```

## User groups & distribution centers

```sql
-- DC auth: 'a' = all DCs, 'c' = custom (restricted)
select name, distribution_centers_auth from user_types where organization_id = :org_id;
```

DC user-group restriction governs the order ship-from selector, not catalog inventory
counts. Reps still in `DefaultUserGroup` bypass restrictions.

## Onboarding health

`GET /api/v1/<shortname>/mcp/organizations/health` returns the six-category onboarding
scorecard (foundational, catalog, customer/pricing, inventory, orders, engagement).
Use it to turn a catalog-strong/transaction-empty org into an ordered import backlog.
