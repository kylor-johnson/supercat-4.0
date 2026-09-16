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

## Where eOL sits commercially

Packaging is **three tiers**, not a la carte modules. The old "eCat Online / B2B Cart /
Sales Portal as separate add-ons" framing is retired — legacy `recurring_services`
strings still read that way on old accounts, but that is billing history, not entitlement.

| Tier | /mo | /yr | Users | eOL-relevant contents |
|---|---:|---:|---:|---|
| **T1 Catalog Essentials** | $749 | $8,988 | 10 | Online Product Catalog (browse), iPad app, Admin Console, ERP import, multi-price lists |
| **T2 Commerce Professional** | $1,295 | $15,540 | 15 | **+ Online Ordering, Private Storefront, Buyer Registration, Order & Invoice Tracking, Customer-Specific Pricing, Quick-Order Grid, Product Configurator (CPQ), Payment Processing (PCI), Address validation** |
| **T3 Commerce Enterprise** | $2,295 | $27,540 | 40 | **+ Sales Intelligence Dashboard (the Sales Portal), Territory & Performance Views, Sales Reports & Summaries, Data Export, dedicated CSM, priority support w/ SLA** |

So: **buyer cart and order/invoice tracking are T2. The Sales Portal reporting layer is T3.**

> **Source-of-truth rule.** <https://supercatsolutions.com/pricing> is canonical for what
> is in each tier. `Pricing Migration/_root/03_what_we_sell.md` is *comms language* and has
> been observed stale on feature placement (it puts CPQ, card processing and the CSM in the
> wrong tiers). If the two disagree, the live page wins. Never quote a tier's contents from
> memory or from the migration doc alone.

**Site flags are not entitlement.** `enable_online_ordering` / `enable_sales_portal` on a
mobile site can be `true` on an account whose subscription never covered them — commonly on
orgs that used a feature years ago. Provisioned ≠ paid for. Check the flags in Postgres
*and* the commercial position (migration CSV / Jon & Emery) before promising anything.

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

### Custom hostname is self-service — no engineering ticket

Admin Console → **Mobile Sites → [site] → Custom Hostname Configuration**
(`CdnConfigurationsController` → `AwsManager::Cdn.ensure_cdn`, async). Requires admin + HTTPS.

1. Set `custom_cname` on the mobile site.
2. The page shows **CNAME #1** (name + value) for SSL validation, with a deadline.
3. The certificate issues automatically once DNS propagates; status goes to `ISSUED`.
4. Refresh until the CDN distribution reads `Deployed`, then it shows **CNAME #2** to point
   the hostname at the CDN.

Two customer-facing records total. Tell the client's IT team: **CNAME only.** Per KB
`publishing-ecat-online`, an **A record will break the catalog when we move servers**, and
records on internal DNS servers cause split-horizon failures. Custom domain is never a
go-live dependency — run on the standard path first and add the hostname later.

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
| `enable_online_ordering` | `'y'` / `'n'` / `''`/`nil` (inherit site) |
| `allow_user_enrollment` | Rep "Enroll Customer" button |
| `customer_synching` | `'a'` all / `'o'` own-territory / `'n'` none. Drives `Customer.get_customers`, which gates the customer list **and** the portal's fallback scope |
| Authorized price levels | Which levels appear (same as iPad) — via `price_levels_user_types` |
| SmartStack visibility | via `smart_stacks_user_types` (`smart_stack_id` + `user_type_id`) |

There is **no `enable_sales_portal` column on `user_types`** — portal visibility is the
mobile-site flag plus the gate in §"Sales Portal on eOL". Don't look for it.

### The one-group constraint (governs what you can promise)

**`org_users.user_type_id` is a single column.** A user belongs to exactly one group per
org — there is no many-to-many. And `smart_stacks` has **no per-surface flag**.

Consequences, both of which get promised wrongly on calls:

- You **cannot** give the same rep one set of SmartStacks on the iPad and a different set
  on the web. One group governs both surfaces. To scope web SmartStacks for reps, either
  unpublish the list or accept it shows in both places.
- Creating a parallel "<group> — online version" and moving reps into it **changes their
  iPad experience too**. Safe for *buyers* (they were never in a rep group); not safe for reps.

### Two different smart-stack filters — different scopes

| Column | Scope | Applied in |
|---|---|---|
| `mobile_sites.smart_stack_filter_id` | **Web only** | `QueryForCatalog#for_mobile_site` |
| `user_types.smart_stack_filter_id` | **Both surfaces** | `BuildQueryConditions` → `QueryForApi` (iPad) *and* `QueryForCatalog#for_user_type` |

Both restrict the visible **product set** (not SmartStack list visibility). Only the
site-level one is a web-only lever.

**Rep + customer number conflict (common):** If an OrgUser has BOTH territory/rep codes
AND a `customer_number`, the system treats them as a **customer**. They see only that
customer's `DefaultPriceCode` and cannot switch levels. Fix: remove customer number from
rep profiles. (HelpScout #12877. Note: the KB article that used to cover this,
`price-levels-ecat-online-vs-ecat-ipad`, is dead — explain it directly, don't link.)

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

KB: `b2b-shopping-cart`. (`ecat-online-saving-your-cart-simple-guide` is dead — cart
persistence is documented here only.)

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

Quick-enroll specifics (KB `streamlined-eol-enrollment`): a Sales Portal user can only
enroll users for customers **already in their own customer list**; approval is immediate
with credentials emailed; the new user lands in the **default user group at the default
price level**, and changing that requires a request to SuperCat.

### Migrating an existing buyer base — invitations vs. just logging in

**Existing users cannot be invited.** `OrganizationInvitation` validates
`user_does_not_exist_in_org` and rejects any email already attached to an org user. So for
a client moving buyers off a legacy portal, the flow splits:

| Buyer state | What happens |
|---|---|
| Already an org user | **No invitation.** They go to the eOL URL and sign in with existing credentials. Password reset covers anyone who's forgotten. |
| Not in eCat | Invitation from their email; they set their own password on first use. |

Invitation mechanics: token URL `https://<host>/onboarding/<token>`, **1-week default
expiry** (`default_expiration_period`), bulk CSV import at Admin → Invitations →
`import_from_file` with headers `email, username, first_name, last_name, user_type,
territory_codes, customer_number`. `create_with_email` sends immediately via
`OrganizationInvitationMailer`; `from:` is the **org's display name at a SuperCat address**.
Tokens are exportable if a client wants to send the mail themselves — but mind the 1-week
expiry against their send schedule.

**Branding the enrollment mail:** Admin → Tools → **Company Settings → Email Templates**
(`enrollment_welcome_template`). Variables `%username%`, `%password%` (renders
"[your current password]" when blank, so it works for existing users too),
`%existingsitemessage%`. **URL placeholders are NOT substituted** — hard-code the real eOL
URL or the mail server turns the placeholder text into a broken tracked link. That's the
whole subject of KB `fixing-invalid-urls-in-custom-enrollment-email-templates`.

KB: `ecat-online-quick-enrollment`, `streamlined-eol-enrollment`, `user-enrollment`,
`delegated-enrollment`, `ecat-online-1` (overview).

## Sales Portal on eOL

When `enable_sales_portal` on the mobile site:
- Left nav: Dashboard, Customers, Orders, Invoices (per user group flags)
- Uses **ERP-imported** `order_data.csv` / `invoice_data.csv` — NOT iPad-submitted orders
- Optional: `territories.csv`, `enable_portal_delta_imports` org flag

### Who sees which rows — `customer_number` wins

`PortalOrder.get_orders` / `PortalInvoice` branch on the org user first:

```ruby
if org_user.customer_number.present?
  # scoped to EXACTLY [org_user.customer_number]
elsif parameters[:customer_bill_to_number]
  # scoped to the requested account (rep/admin drilling into one customer)
else
  # scoped to Customer.get_customer_codes_for_org_user(org_user)  → territory path
end
```

Verified against master @ `3d99376` (2026-08-25): `portal_order.rb:31`, `portal_invoice.rb:21`.

So a user with a `customer_number` sees **only that one account**, and their territory
codes are irrelevant to portal orders and invoices. A buyer carrying stray territory codes
is a hygiene problem (per `b2b-shopping-cart`, it can surface a customer list they
shouldn't see in the catalog UI) but it does **not** leak portal order/invoice rows.
Don't over-warn about it; don't under-warn either — the system spec §7.6 lists separate
open authorization risks on customer-detail and invoice-show that are not covered here.

### Portal visibility gate

`eol_left_nav_dataflow.rb` requires `customer_number.present? || !sync_no_customers?`.

A user in a `customer_synching = 'n'` group **with no customer number sees no portal at
all**. That is the usual cause of "the buyer can't see the portal," and it is also why
buyer accounts missing a customer number are broken twice over — no portal *and* no cart
(the cart needs a valid customer number too).

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
- User group auth still governs price level visibility

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
```

For **usage/adoption** (not just provisioned), also query BigQuery
`google_analytics_ecat_online` per `supercat-data-routing`.

## HTTP APIs

> **The `/api/v1/<shortname>/mcp/...` API does not exist in production.** Verified
> 2026-08-25: every documented endpoint returns a Rails JSON `404 No route matches`, under
> every path variant tried (shortname before `mcp`, after `mcp`, omitted, org-prefixed).
> Auth succeeds — it is the route that is absent, so this is not a credentials problem.
> Confirmed at source: `grep -c mcp config/routes.rb` returns **0** on master @ `3d99376`
> (2026-08-25). The routes were never shipped, so this is not a deploy-lag issue.
> Use `supercat-postgres-vpn` for live state. Do not restore this section without
> re-testing against production.

**Order Download API** — real, documented at KB `order-download-api`.

```
GET https://supercat.supercatsolutions.com/<org>/orders.json    # HTTP Basic
```

| Param | Purpose |
|---|---|
| `export_format` | `stdjson` \| `stdjsonv2` \| `default` (v2 adds custom product fields per item) |
| `submit_from` / `submit_to` | Filter by submission date (`yyyy-mm-dd` or ISO8601) |
| `receipt_from` / `receipt_to` | Filter by server receipt date |
| `single_document` | Return one JSON array instead of line-delimited objects |

Default output is one JSON document per order, one per line. This is the right answer when a
client asks for recurring or automated order downloads — better than walking them through
Admin Console CSV export. Related: `batch-order-transfer-api`, `json-order-export-push`,
`json-order-fields`. The Admin credentials in `~/.supercat/mcp-credentials.json` are **not**
authorized for it (401) — it needs the org's own API credentials.

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
| Enrollment button missing | `enrollment_enabled` off or `self_service_enrollment_enabled` false | Org + site flags |

For reactive tickets, start with `ecat-support-triage` (eOL row), ground with
`ecat-postgres-audit`, draft with `ecat-client-email`.

## KB articles (Craft CMS)

Base URL: `https://supercatsolutions.com/knowledgebase/{slug}`. Slugs below verified live
2026-08-25 against the full 146-article index (crawl the 8 category pages for the current set).

| Topic | Slug |
|-------|------|
| Overview | `ecat-online-1` |
| Sales Portal overview | `ecat-online-sales-portal` |
| B2B Cart | `b2b-shopping-cart` |
| Projects | `ecat-online-projects` |
| My Account / retail pricing | `eol-retail-pricing`, `select-eol-catalog-price` |
| Quick enrollment | `ecat-online-quick-enrollment`, `streamlined-eol-enrollment` |
| Other enrollment paths | `user-enrollment`, `delegated-enrollment`, `creating-delegates-for-enrollment`, `eol-accounts-for-prospective-customers` |
| Enrollment email templates | `fixing-invalid-urls-in-custom-enrollment-email-templates` |
| User groups / users | `user-groups`, `user-management`, `inactive-users-report` |
| Price levels | `price-levels`, `pricelevelchanges`, `catalog-pricing`, `comparison-price-level`, `discount-market-promo-price-levels`, `import-contract-prices` |
| Custom domain / URL | `publishing-ecat-online`, `ecat-online-url` |
| Portal setup + verification | `publish-portal-dashboard`, `sales-portal-data-verification`, `sales-portal-file-specifications` |
| Orders | `required-order-header-fields`, `custom-order-header-fields`, `order-surcharges`, `order-email-template`, `about-order-page` |
| Order APIs | `order-download-api`, `batch-order-transfer-api`, `json-order-export-push`, `json-order-fields` |
| Complete-order display | `hide-show-complete-orders-in-ecat-online` |
| Payments | `supercat-credit-card-support`, `capture-credit-card-information`, `capture-credit-card-funds-for-an-order` |

**Dead slugs — do not cite** (404 as of 2026-08-25, absent from the index):
`ecat-online-saving-your-cart-simple-guide`, `price-levels-ecat-online-vs-ecat-ipad`.
Cart-persistence behaviour is documented in this skill only; there is no live KB article
for it, so explain it in your own words rather than linking.

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
