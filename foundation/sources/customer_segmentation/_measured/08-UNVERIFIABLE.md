---
id: MEAS-08
title: What the database cannot settle, and exactly what would
version: 1.0
status: evidence pack
date: 2026-08-31
database: supercatprod
---

# Unverifiable from the database

Everything here was attempted and failed, or was ruled out on inspection. Each row names the
specific artefact that would settle it. Nothing here was reasoned to a number.

---

## 1. Fine-grained feature gates — `:portal_portal`, `:advanced_reports`, `:link_to_customer_dashboard`

**Status:** `UNVERIFIABLE-FROM-DB` — but the ground under it has shifted. See §2.

Confirmed dead ends:

- `org_setting_definitions` holds **3 rows total**; `org_setting_values` holds **2**. A dead end, as
  the brief anticipated.
- `organizations` has **35 boolean columns** and none is a portal, report, or dashboard gate.
  `enable_rep_activity` (7 orgs) is the CRM activity-logging pilot, not a reporting gate.
- `mobile_sites` has `enable_online_catalog`, `enable_online_ordering`, `enable_sales_portal` — but
  no report-level gate.

**What would settle it:** the application YAML that defines these symbols. In the SuperCat Rails
repo, look for the feature-flag definition file and its per-org override — search the repo for the
literal symbols `:advanced_reports`, `:portal_portal`, `:link_to_customer_dashboard`, most likely
under `config/` (a `features.yml` / `settings.yml` / Rails-config initializer) or wherever the
`Feature`/`Setting` model resolves them. **One `grep -rn "advanced_reports" config/ app/` against the
app repo produces the list of six orgs and collapses this entire section.** That grep was not run
here because this pass had database access only.

## 2. …but plan-level entitlement **is** in the database, and the register missed it

`MEASURED` · Q060, Q061 · **This is a correction to the register's own "unverifiable" verdict.**

`subscription_plans` + `subscriptions` fully encode commercial entitlement:

- **`eCat Online - Portal`** — *"Sales Portal service with enhanced sales reporting"*, $395/mo —
  **37 orgs**
- **`eCat Online - B2B Cart`** — $295/mo — **32 orgs**, against 55 orgs with the flag on →
  **25 orgs run Cart with no subscription**
- CPQ entitlement (plans 3+9+12) — **21 orgs**
- T1/T2/T3 tiers exist; only **5 orgs** are on them

**So the register's statement "feature gates live in application YAML, not Postgres" is half wrong.**
The *sub-feature* gates do. The *product entitlement they sit inside* does not, and it changes the
denominator for every gated claim: the population for `:advanced_reports` is not 258 orgs, it is the
**37** that pay for the Portal.

## 3. The "~13,800 additional buyers" figure — bounded, not settled

`MEASURED` ceiling, `UNVERIFIABLE-FROM-DB` floor · Q062

| | Buyer records |
|---|---:|
| All active buyers | 18,764 |
| At orgs on the Portal plan | 17,637 |
| At orgs with the Portal flag on | 17,526 |
| **At orgs with BOTH the Portal plan and an invoice feed** — the true ceiling, since 086 needs invoiced history | **17,522** |

**Defensible range: ~5,100 to ~17,500 buyer records** (~3,500–12,100 people at 1.45 records/person).
The low end assumes the 6 orgs already running purchase history are the 6 largest (12,473 buyers);
the high end assumes they are small.

The register's 13,800 **sits inside the range and is not defensible as a point estimate.**

**What would settle it:** naming the six orgs. The same grep as §1 collapses the range to a single
number in one command.

## 4. `rep_activities` — permission denied

`UNVERIFIABLE-FROM-DB` · Q007

The table exists (`pg_class` estimates 635 rows) but `SELECT` returns **`permission denied for table
rep_activities`**, and it does not appear in `information_schema.columns` for this role.

So the 2026-08-27 pack's correction — that ungating `enable_rep_activity` would render empty tables
because it gates a separate CRM-style activity pilot — **can be neither confirmed nor refuted here.**
The flag count reproduces (7 of 258, Q006); the contents do not.

`JUDGMENT`: 635 rows across a 7-org pilot is consistent with "barely used," which is consistent with
the 08-27 conclusion. That is an inference from a row estimate, not a measurement, and it is not
strong enough to act on.

**What would settle it:** a `SELECT` grant on `rep_activities` for the reporting role, or a one-off
count run by someone with the grant.

## 5. Roles that do not exist in the schema

`UNVERIFIABLE-FROM-DB`

**PER-04 (customer service / order entry) and PER-05 (product / merchandising) have no schema
representation whatsoever.** No attribute on `org_users`, `user_types`, or anywhere else
distinguishes them. They sit inside the 25,801 internal records undifferentiated. The readout's
"not counted" is correct.

`is_admin` (2,460 records) spans VP/ops, CS leads and IT and cannot be decomposed, so **PER-03 and
PER-06 cannot be separated from each other or from the rest** either.

**What would settle it:** a role or job-function attribute on `org_users`. Failing that, an analysis
of `audit_log_entries` (21.2M rows) mapping which Admin Console controllers each internal user
touches — but the controller-to-role mapping would itself be an assumption, so this would produce a
hypothesis rather than a measurement.

## 6. The access-rule sprawl count [F10] — "134 toggles / 39 flags / 6 layers"

`CODE-AUDIT` · not reproducible here · Q070

Measured: `user_types` has **12** boolean columns, `organizations` has **35**. Those do not
reconcile to 134 by any obvious route, so the original figure must have counted something else —
probably including varchar and text toggles, join-table grants (`price_levels_user_types`,
`collections_user_types`, `smart_stacks_user_types`, `distribution_centers_user_types`, and eight
more), and YAML flags together.

The figure is **not contradicted**; it is simply not checkable from column counts.

**What would settle it:** re-run the F10 audit with its counting method written down. JTBD-033 is
ranked 13 and sized M on the strength of this number, so the method matters.

## 7. Job-level things the schema genuinely cannot see

| JTBD | Why not measurable |
|---|---|
| **035** export/UI reconciliation | A UI defect. Leaves no database artefact. Needs the EBR-91/SERV-2449 reproduction |
| **051** true sell-through | Needs inventory **history**. `inventories` is overwritten on every import and no snapshot table exists. This is exactly what A14 would create |
| **085** buyer offline ordering | A client-side capability. Needs a browser/service-worker audit of the eOL app |
| **024** view-as preview | A mechanism that does not exist. Nothing to measure until A9 is specified |
| **011** whether a rep *acts* on the brief | Reach is measurable (Q010); behaviour change is not. Needs the market field test the register already plans |
| **015 / 043** whether normalising status would help | The 125 status values are measured (Q032). Whether each org's feed **refreshes** status on a useful cadence is not tested — and a normalised status is worthless if it updates weekly. Needs a per-org `max(order_date)` vs status-change cadence analysis, or the integration spec |

## 8. Things measured here that should not be trusted as precise

Stated so a later reader does not over-read them.

- **The 69.7% zero-order rep figure** (Q010) depends on `orders.org_user_id` attribution. A rep whose
  orders are keyed by customer service under another user would land in band A wrongly. The
  independent login-days evidence (Q012) makes wholesale misattribution unlikely, but read this as
  "the large majority," not as a precise headcount.
- **The 44% at-risk account figure** (Q037) compares Jun–Aug to Mar–May and therefore crosses a
  market cycle. The direction (a fixed rule is unusable) is solid; the magnitude is inflated by
  seasonality.
- **Ship-to multiplicity** (Q016) rests on `ship_to_code`, which is populated for well under half the
  buyers who ordered. Directional only.
- **Buyer/rep "people" counts** (Q051–Q053) assume `org_users.user_id` is a stable person identity
  across orgs. Spot-checking supports this (1.88 and 1.45 memberships per person are plausible
  multi-line figures) but it was not independently validated against `users`.
- **`buyers_at_portal_plan_orgs` summed distinct people per org** (Q062) and therefore double-counts
  people who buy from more than one manufacturer. Use the record figures for that comparison.

---

## The single highest-value next action

**One grep against the SuperCat Rails application repo settles §1 and §3 together** — the six
`:advanced_reports` orgs, the `:portal_portal` and `:link_to_customer_dashboard` populations, and
with them the largest remaining unknown in the register: the true incremental reach of JTBD-086,
currently a range spanning 12,000 buyers.

Search for the literal flag symbols under `config/` and wherever the feature-resolution model lives.
It is minutes of work and it removes the last "we cannot quote this" panel from the readout.
