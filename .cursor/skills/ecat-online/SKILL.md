---
name: ecat-online
description: Configure, troubleshoot, and explain eCat Online (eOL) — the browser-based B2B catalog, Cart, buyer enrollment, My Account markup pricing, and Sales Portal tabs. Use for web catalog issues, cart/checkout, buyer login, mobile site setup, eOL vs iPad pricing differences, order_source server orders, or when a KB article describes per-browser "My Account" pricing (that is eOL, not iPad).
---

# eCat Online (eOL)

Scope: **browser-based eCat Online** (`MobileSite`, routes under `/e/`). This is **not**
the iPad app. Sales Portal **reporting** (ERP-fed order/invoice history) is a separate
surface that often shares the same mobile site — distinguish catalog/cart issues from
portal data issues.

Always-on iPad rules (`ecat-ground-truth`, `ecat-import-ops`, `ecat-data-model`) still
apply to the **shared catalog foundation** (products, customers, inventory, options).
When a question is "does org X have eOL?" or needs live state, consult
`supercat-data-routing` first, then `ecat-postgres-audit`.

## eOL vs iPad (memorize this split)

| Topic | iPad | eCat Online |
|-------|------|-------------|
| Auth | Device sync + API | Browser session login |
| Anonymous browse | No | Yes — public user on mobile site |
| Price picker | Cog menu on device | **My Account** session pricing (browser-only) |
| Cart | Local order draft on iPad | `CartItem` rows + `Order` in `'cart'` state |
| Submitted orders | `order_source = 'ipad'` | `order_source = 'server'` |
| User must have customer to order | Yes (on device) | Yes — `customer_number` on OrgUser |
| Catalog query | `Products::QueryForApi` | `Products::QueryForCatalog` (+ `hideable` filter) |
| Enrollment | N/A | Self-service, admin signup URL, rep-initiated |

For iPad-only pricing setup, use `ecat-pricing-levels`. For eOL **My Account** markup
/ retail / hide-prices behavior, stay in this skill.

## Product tiers (commercial)

| Module | What it is |
|--------|------------|
| **eCat Online** | Web catalog (browse-only or authenticated) |
| **B2B Cart** | Cart + checkout on a mobile site (`enable_online_ordering`) |
| **Sales Portal** | Dashboard / Customers / Orders / Invoices tabs on eOL (`enable_sales_portal`) |

Cart and Portal are optional add-ons. An org can have Projects without Cart. Confirm
provisioned modules in Postgres + billing before promising features.

## URLs & sites

**Standard path (code-verified):**

```
https://supercat.supercatsolutions.com/{org_shortname}/e/{url_key}/products
https://supercat.supercatsolutions.com/{org_shortname}/e/{url_key}/login
https://supercat.supercatsolutions.com/{org_shortname}/e/{url_key}/my-account
https://supercat.supercatsolutions.com/{org_shortname}/e/{url_key}/checkout
https://supercat.supercatsolutions.com/{org_shortname}/e/{url_key}/portal
```

**Buyer login** is `/login` on the same `/e/` scope (`config/routes.rb:168-169`,
`match '/login' => 'ecat_sessions#login'`). The route parameter is named
`:mobile_site_name`, but its **value** is the mobile site's `url_key`
(`eol_controller.rb:91-96`) — which is why the URLs above show `{url_key}`.

Legacy home redirect: `/{org}/m/{url_key}/` → eOL home.

**Custom CNAME:** `MobileSite#custom_cname` maps host → org + site via middleware
(`custom_mobile_cname.rb`). Root `/` on CNAME redirects to legacy `/m/` path.

**Admin Console** (not eOL): `https://supercat.supercatsolutions.com/supercat/sessions/new`
and org workspace `.../supercat/{shortname}`.

An org can have **multiple mobile sites** (unique `url_key` per org). Configure under
Admin → **Mobile Sites**.

## Enablement stack (all layers matter)

### 1. Organization (master gate)

| Setting | Where | Effect |
|---------|-------|--------|
| `mobile_enabled` | Org superadmin | **Required.** Without it, eOL is off entirely |
| `enrollment_enabled` | Org DB column | Buyer enrollment UI + admin enrollment section |
| `enable_gridview_ordering` | Org | Add-to-cart from product grid (plus other gates) |

Check: `select mobile_enabled, enrollment_enabled, enable_gridview_ordering from organizations where shortname = '<sn>';`

Org `properties` JSONB also holds portal/enrollment/RMA/payment flags — see
`Organization::FLAGS` in codebase.

### 2. Mobile site (`mobile_sites` table)

| Column | Default | Purpose |
|--------|---------|---------|
| `url_key` | — | URL segment; `[-a-z0-9]+`; unique per org |
| `allows_unauthenticated_users` | true | Anonymous "public user" browsing |
| `allows_authenticated_users` | false | Logged-in org users |
| `enable_online_catalog` | true | Show catalog |
| `enable_online_ordering` | false | **Site-level Cart** |
| `enable_sales_portal` | false | Portal tabs |
| `org_user_id` | required | **Public user** proxy for anonymous sessions |
| `default_user_type_id` | required | User group for approved enrollments |
| `price_level_id` | optional | Retail price level for My Account "retail" option |
| `custom_cname` | optional | Branded hostname |

Site `properties.flags` (tri-state via `get_flag`): `self_service_enrollment_enabled`
(default true), `enable_enrollment_by_users`, `enable_online_library`,
`hide_products_marked_hideable`, `display_quantity_available`, etc.

### 3. User group (UserType)

| Setting | Purpose |
|---------|---------|
| `display_order_function` | "Enable ordering?" — requires linked **customer** |
| `enable_online_ordering` | `'y'` / `'n'` / `nil` (inherit site) |
| `allow_user_enrollment` | Rep "Enroll Customer" button |
| `enable_sales_portal` | Portal tab visibility |
| Authorized price levels | Which levels appear (same as iPad) |

**Rep + customer number conflict (common):** If an OrgUser has BOTH territory/rep codes
AND a `customer_number`, the system treats them as a **customer**. They see only that
customer's `DefaultPriceCode` and cannot switch levels. Fix: remove customer number from
rep profiles. (HelpScout #12877; KB draft `price-levels-ecat-online-vs-ecat-ipad`.)

## Pricing on eOL

### Default price level (My Cost)

Same resolution as iPad:
- OrgUser with `customer_number` → customer's `DefaultPriceCode`
- Else → user type's authorized price levels (+ optional default)

### My Account (session-only — NOT iPad)

Path: `/{org}/e/{site}/my-account`. Only shown when mobile site has `price_level_id` set
(admin: **Retail Price Level** on mobile site).

| Session `preferred_pricing` | Label | Behavior |
|-----------------------------|-------|----------|
| `nil` / `'default'` | My Cost | Normal buyer/rep pricing |
| `'retail'` | Named retail level | Uses mobile site's `price_level` |
| `'catalog'` | Custom + markup % | Cost × `(1 + markup/100)` |
| `'none'` | Hide prices | No prices rendered |

Session keys: `session[:preferred_pricing]`, `session[:catalog_pricing_markup]`.

**Side effects when ANY non-default pricing is selected:**
- **Cart/checkout disabled** (`session[:preferred_pricing].nil?` required)
- **Sales Portal hidden**
- In `'catalog'` mode, cart prices hidden on product rows

Code: `ecat_permissions_helper.rb`, `renders_product_details.rb`, `my_account.html.erb`.

## Cart & checkout

### Permission checklist (all must pass)

1. Org `mobile_enabled?`
2. Mobile site `enable_online_ordering?`
3. User type `enable_online_ordering` not `'n'`
4. User type `display_order_function?` (linked customer)
5. `session[:preferred_pricing]` is **nil** (My Cost mode)
6. Checkout submit: authenticated user with valid `customer_number`

Grid add-to-cart also requires org `enable_gridview_ordering?`.

### Cart persistence (support-critical)

The cart is **browser/device-local**, not per user account:
- One cart per browser/device (cookies/local storage)
- Not tied to login — another user on same browser sees/overwrites it
- Incognito / cleared cookies = empty cart
- **Projects** are separate — they do NOT store configured options/qty/prices

Workarounds: same browser when customer returns; separate browser profiles on shared
machines; use Projects as a placeholder list only.

KB: `ecat-online-saving-your-cart-simple-guide`, `b2b-shopping-cart`.

### Order lifecycle

1. Add items → `cart_items` on org_user
2. Draft `orders` row: `order_state = 'cart'`, `order_source = 'server'`
3. Checkout → submit → `order_state = 'active'`, cart cleared, export/email

iPad orders stay `order_source = 'ipad'`. Analytics/dashboards split on this field.

## Buyer enrollment

**Prerequisites:** org `enrollment_enabled`, mobile site `default_user_type_id`,
site flag `self_service_enrollment_enabled` (default true).

| Flow | Entry |
|------|-------|
| Self-service | eOL login → "Apply for Access" → email token → form |
| Admin public URL | `/{org}/enrollment/signup/{key}` (key = first 6 of SHA512(shortname)) |
| Rep-initiated | Customer page → rep enroll → **immediate** approval |

Applicant saved with `is_ecat_online = true`. Admin approves at
`/{org}/enrollment/applicant/:id/process` → creates User + OrgUser + optional customer link.

Optional org flag `enrollment_requires_customer` validates customer number against
`customers.csv`.

KB: `ecat-online-quick-enrollment`, `ecat-online-1` (overview).

## Sales Portal on eOL

When `enable_sales_portal` on the mobile site:
- Left nav: Dashboard, Customers, Orders, Invoices (per user group flags)
- Uses **ERP-imported** `order_data.csv` / `invoice_data.csv` — NOT iPad-submitted orders
- Optional: `territories.csv`, `enable_portal_delta_imports` org flag

Portal troubleshooting → verify portal imports in `import_events`, not iPad order sync.
For portal-only reporting bugs, route engineering (Jira read-only). For missing ERP data,
fix the import files (`ecat-import-ops` Sales Portal section).

Do not conflate **eOL Cart orders** (`order_source = 'server'`) with **Portal order
history** (ERP `order_data.csv`).

## Shared catalog data (same as iPad)

eOL reads the same imports: options → option_groups → products → stories → inventory →
customers. No separate "eOL products file."

eOL-specific catalog behavior:
- Product `hideable` flag — when site flag `hide_products_marked_hideable`, hidden from catalog
- Smart stack filter on mobile site can limit visible products
- User group auth still governs price level visibility **and trade names**. Left nav
  is `TradeName.get_trade_name_collections_pairs(user_type, is_admin)`. Admins see
  all trade names. Groups with `trade_names_auth = 'c'` only see the join-table
  list. **A newly imported trade name is not auto-added to those lists.** That is
  why a brand can sync to iPad (admin / `auth = 'a'`) and be missing from the
  public eOL nav. Check the public proxy user (`mobile_sites.org_user_id`) and
  the logged-in groups separately — they are often different lists.

Importer runs mobile-related steps when `organization.mobile_enabled?`.

## Postgres audit snippets

Resolve org first (`ecat-postgres-audit`), then:

```sql
-- org gate + sites
select o.mobile_enabled, o.enrollment_enabled,
       ms.url_key, ms.enable_online_catalog, ms.enable_online_ordering,
       ms.enable_sales_portal, ms.allows_authenticated_users,
       ms.allows_unauthenticated_users, ms.custom_cname
from organizations o
left join mobile_sites ms on ms.organization_id = o.id
where o.shortname = '<sn>';

-- eOL-capable users + customer linkage
select ou.id, u.email, ou.customer_number, ut.name as user_group,
       ut.display_order_function, ut.enable_online_ordering,
       ou.last_ecat_online_login_at
from org_users ou
join users u on u.id = ou.user_id
join user_types ut on ut.id = ou.user_type_id
where ou.organization_id = :org_id
order by ou.last_ecat_online_login_at desc nulls last
limit 30;

-- recent eOL orders vs iPad
select order_source, count(*) filter (where is_submitted) as submitted
from orders where organization_id = :org_id
group by order_source;

-- pending enrollments
select status, count(*) from enrollment_applicants
where organization_id = :org_id group by status;

-- trade name auth (eOL left nav). 'a' = all, 'c' = join-table only, 'n' = none
select ut.name as user_group, ut.trade_names_auth, t.name as trade_name
from user_types ut
left join trade_names_user_types x on x.user_type_id = ut.id
left join taxonomies t on t.id = x.trade_name_id and t.type = 'TradeName'
where ut.organization_id = :org_id
order by ut.name, t.name;
```

For **usage/adoption** (not just provisioned), also query BigQuery
`google_analytics_ecat_online` per `supercat-data-routing`.

For a faster first look at the same live state over HTTP (no VPN/psql), see the
**MCP HTTP API** section below.

## MCP HTTP API (fast first look)

A read-only HTTP API that **complements** `supercat-postgres-vpn` for a quick first
look — not a replacement. The base path puts the shortname **between** `/api/v1/` and
`mcp`: `/api/v1/<shortname>/mcp/...`

Scope nesting: `namespace :api` (`config/routes.rb:652`) → `namespace :v1` (654) →
`scope '/:org_shortname/mcp'` (710).

Most valuable for eOL:

| Endpoint | Returns |
|----------|---------|
| `organizations/data/mobile_sites.json` | Site flags without hand-writing the `organizations`↔`mobile_sites` join |
| `organizations/data/smart_stacks.json` | Smart stacks |
| `organizations/data/org_users.json` | Org users |
| `organizations/data/price_levels.json` | Price levels |
| `organizations/customers/:customer_id/pricing_analysis.json` | Buyer price resolution (the My Account / `DefaultPriceCode` question) |
| `organizations/users/permissions_summary.json` | Permission summary |

**Auth is admin-only.** `verify_mcp_access` requires `is_admin?` on the user or
org-user, else 403 (`api/v1/mcp/base_controller.rb:12,18-30`). `AdminController#authenticate`
tries three methods **in this order** (`admin_controller.rb:6-14`):
1. Existing session cookie
2. `X-CLIENT-ID` + `X-API-KEY` headers (URL shortname must match the client-id's org,
   lines 53-65)
3. HTTP Basic (lines 21-25) — the practical choice for curl

**Two hard requirements:**
- **HTTPS only** (`prepend_before_action :require_https`).
- The **`.json` extension is MANDATORY** — `api_call?` treats only plist/json/csv as API
  requests (`admin_controller.rb:16-19`). Without it you're redirected to a login page and
  get HTML back, which looks like an auth failure but isn't.

```
curl -u 'USER:PASS' \
  https://supercat.supercatsolutions.com/api/v1/<shortname>/mcp/organizations/data/mobile_sites.json
```

## Troubleshooting router

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| Site 404 / "mobile not enabled" | `mobile_enabled` false or bad `url_key` | Check org + mobile_sites |
| Browse works, no Add to Cart | Site/user-group ordering off, or My Account not on My Cost | Check flags + `preferred_pricing` |
| "Must be assigned a customer" | OrgUser missing/invalid `customer_number` | Link to customer in Admin |
| Prices wrong for one user only | Rep+customer number conflict | Remove customer # from rep |
| Cart empty after login | Cart is browser-local, not account | Explain persistence; see KB |
| Portal tabs missing | `enable_sales_portal` off, user group flag, or My Account pricing active | Check mobile site + session |
| Portal orders blank | No/wrong `order_data.csv` import | Portal import path, not iPad |
| Product on iPad but not eOL | `hideable` + site flag, smart stack filter, or sync lag | Compare catalog query filters |
| Trade name on iPad, missing from eOL left nav | New trade name not authorized to the viewing group (`trade_names_auth = 'c'`). Public site user ≠ admin | Authorize the trade name to eOL Public Site and/or the logged-in eOL group. Confirm audience first (public vs enrolled) |
| Enrollment button missing | `enrollment_enabled` off or `self_service_enrollment_enabled` false | Org + site flags |

For reactive tickets, start with `ecat-support-triage` (eOL row), ground with
`ecat-postgres-audit`, draft with `ecat-client-email`.

## KB articles (Craft CMS)

| Topic | Slug |
|-------|------|
| Overview | `ecat-online-1` |
| B2B Cart | `b2b-shopping-cart` |
| Projects | `ecat-online-projects` |
| Cart persistence | `ecat-online-saving-your-cart-simple-guide` |
| My Account / retail pricing | `eol-retail-pricing` |
| eOL vs iPad price levels | `price-levels-ecat-online-vs-ecat-ipad` |
| Quick enrollment | `ecat-online-quick-enrollment` |

Base URL: `https://supercatsolutions.com/knowledgebase/{slug}`

## Code anchors (supercat_server)

| Topic | Path |
|-------|------|
| Routes | `config/routes.rb` |
| Site model | `app/models/mobile_site.rb` |
| Auth / org user resolution | `app/controllers/eol_controller.rb` |
| Permissions | `app/helpers/ecat_permissions_helper.rb` |
| My Account | `app/views/ecat/my_account.html.erb` |
| Cart/checkout | `app/controllers/ecat_order_process_controller.rb` |
| Enrollment (eOL) | `app/controllers/ecat_enrollment_controller.rb` |
| CNAME | `app/middleware/custom_mobile_cname.rb` |
| System test | `test/system/ecat_online_system_test.rb` |
