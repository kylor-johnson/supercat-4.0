# Who actually uses the Sales Portal — production evidence

Status: decision-grade finding. Replaces the assumed persona model behind the
persona switcher in the internal and persona-IA demos.

Sources: `supercat_server` (permission/flag code paths) and production Postgres
(read-only). Counts taken 2026-07-27. "Active" = `org_users.last_ecat_online_login_at`
within 90 days. Buyer = `org_users.customer_number` present; rep = it is blank.

---

## 1. The portal's real audience is buyers, not reps

Across the 49 organizations with `mobile_sites.enable_sales_portal`:

| | Enabled users | Active (90d) |
|---|---:|---:|
| Buyers (dealer/customer-linked) | 76,297 | **17,567** |
| Reps / sales users | 14,926 | 2,203 |

Buyers outnumber reps 5:1 on account count and **8:1 on actual logins**. The skew
holds at the org level, not just in aggregate — the top orgs by portal activity:

| Org | Active buyers (90d) | Active reps (90d) |
|---|---:|---:|
| wwjc | 4,012 | 140 |
| jyc | 2,848 | 87 |
| gh | 2,125 | 41 |
| scw | 1,281 | 39 |
| sbmh | 1,159 | 15 |
| fc | 1,146 | 1,047 |

`fc` is the only org where reps are close to parity. Everywhere else the portal
is overwhelmingly a buyer surface.

**Every** active buyer already has the portal switched on: 76,297 of 76,297 have
both `enable_sales_portal` and `display_sales_portal_totals` true on their user
type. There is no dormant-entitlement story here — they can see dollar totals today.

## 2. But buyers can only see Orders and Invoices

The analytics surfaces above Orders/Invoices are gated by feature flags in
`config/initializers/enabled_features.rb`, not by user type:

- **Reports** (Sales Summary, Product Detail, Monthly) requires `:advanced_reports`,
  enabled for **6 orgs**: `scw`, `gww`, `gh`, `sccon`, `kal`, `sarreid`.
  Of the 17,567 active buyers, only ~3,719 (**21%**) are in one of those orgs.
  The other **79% have no Reports surface at all.**
- **Territory Dashboard** requires `:portal_portal`, enabled for **zero organizations** —
  only 9 individual usernames, all internal SuperCat staff.

So the dashboard we have been designing against is, in production, a staff-only
page. Nearly four in five active portal users see a two-item portal.

## 3. Buyers are structurally locked out of the rep view

This is not a config gap that can be flipped on. In
`app/models/eol_left_nav_dataflow.rb`, `should_show_customers_tab` requires
`org_user.customer_number.blank?`, and `should_display_portal_dashboard?` depends
on it. `EcatDashboardController#index` redirects anyone failing that check to the
catalog. A buyer cannot reach the territory dashboard or the multi-customer
Customers list by any configuration.

Buyers do get a *different* surface — their own customer analytics page, gated by
`:link_to_customer_dashboard` (2 orgs: `vic`, `clm`).

---

## What this means for the persona work

The persona switcher was modeling three coequal viewers of one dashboard. The
production system has **two structurally different products** sharing a nav:

1. **A buyer self-service surface** — 8 of every 9 logins, hard-scoped to one
   customer, currently limited to Orders and Invoices for 79% of its users.
2. **A rep territory surface** — the dashboard and multi-customer views, which
   almost no production org has turned on.

Consequences:

- **Drop the persona switcher.** It presents an audience split that the codebase
  resolves by hard redirect, not by preference. Showing a rep dashboard behind a
  "View as buyer" toggle misrepresents what a buyer can reach.
- **The biggest untapped surface is the buyer one**, and it is the one we have
  spent the least design time on. Rolling `:advanced_reports` from 6 orgs to all
  49 reaches ~13,800 additional active buyers — a far larger delta than any
  refinement to the territory dashboard.
- **Client sessions should be split by persona, not by toggle.** Talk to reps
  about the territory dashboard and to buyers about self-service history. Do not
  ask one person to evaluate both.
- **Sequence check for Bet F**: it assumed the dashboard is the center of gravity.
  The data says Orders/Invoices is, and Reports is the missing rung. Worth
  re-shaping before betting.

## Caveat on the measure

`last_ecat_online_login_at` records a login to eCat Online, which also serves
catalog and ordering. It proves who reaches the portal shell, not which tab they
opened — there is no page-level telemetry in the schema (`login_events` captures
logins only, with no route or surface). Read the counts as *audience reachable*,
not *analytics engaged*. That gap is itself worth fixing: we cannot currently
answer "did anyone open Reports" for any client.
