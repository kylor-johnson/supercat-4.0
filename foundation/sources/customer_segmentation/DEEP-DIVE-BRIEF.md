# Brief — measure the persona register against production

> **2026-09-15 — historical prompt.** This brief measured the Aug 25 *seat* register. Do not re-run
> it as if JTBD-0xx / “31 jobs” were current. Output lives in `_measured/` and is scoped there.
> Canonical set: [`personas/00-PERSONA-GROUPS.md`](personas/00-PERSONA-GROUPS.md).

**For:** Claude Code, with read-only Postgres MCP access to `supercatprod` and the foundation repo on disk.
**Written:** 2026-08-31, after a first verification pass that reproduced most of the register's figures and found one wrong.

## The goal

The persona / jobs-to-be-done / surface register in `foundation/sources/customer_segmentation/` was built
from documents and a stamped CSV roster. It is internally careful but it **asserts** where the database
could **measure**. Your job is to replace assertion with measurement wherever Postgres can settle it, and
to say clearly and specifically where it cannot.

You are producing **evidence, not prose.** A separate pass will rebuild the CEO readout from what you leave
behind. Optimise for a later reader who needs to trust and re-run every number.

## Non-negotiables

1. **Read-only.** Never write, update, or run DDL against the database. If a query would scan something
   enormous, sample or aggregate and say so in the query header.
2. **No number without a query.** Every figure you report carries a query id and the date it ran.
3. **Do not edit existing register files.** Write only into a new `_measured/` directory.
4. **Never silently correct the register.** Where your number disagrees, record both, the query, and which
   you believe and why.
5. **Tag every claim** as `MEASURED` (a query), `CODE-AUDIT` (from the app repo or config), or `JUDGMENT`.
   Feature gates are not in Postgres — see the schema notes. Mark those `UNVERIFIABLE-FROM-DB` rather than
   reasoning your way to a number.
6. **Reproduce before you extend.** Start by re-running the register's own headline figures as a calibration
   check. Failing to reproduce one is itself a finding.

## Files to produce — all under `sources/customer_segmentation/_measured/`

| Path | Contents |
|---|---|
| `README.md` | What was measured, when, against which database, and how to re-run |
| `00-FINDINGS.md` | Ranked findings. Each: claim, number, query id, what it changes, confidence |
| `01-CALIBRATION.md` | The register's stamped figures vs live, with deltas and a verdict on each |
| `02-PERSONA-EVIDENCE.md` | Line A — behavioural persona work |
| `03-JOB-DEMAND.md` | Line B — measured problem size per job |
| `04-REACH-AND-SIZING.md` | Line C — reach per job, re-ranked |
| `05-GAPS-SIZED.md` | Line D — the two client-data gaps in commercial terms |
| `06-SEGMENT-VARIATION.md` | Line E — the 4-of-31 claim retested live |
| `07-TRENDS.md` | Line F — direction of travel |
| `08-UNVERIFIABLE.md` | What the database cannot settle, and exactly what would |
| `queries/QNNN.sql` | One file per query. Header comment: purpose, date, one-line result |
| `data/QNNN.csv` | Result set for any multi-row query a later pass might chart |

## Schema orientation — established already, do not rediscover

- **`org_users`** — `customer_number` non-blank ⇒ dealer buyer; blank ⇒ internal / rep. `is_admin` boolean.
  `last_ipad_login_at`, `last_ecat_online_login_at`. **`territory_codes` is `json`** — cast `::text` to test
  emptiness; empty forms seen in the wild: `null`, `[]`, `{}`, `""`. `company_name` is free text.
  `user_type_id` → `user_types`.
- **`user_types`** — `primary_rep_group` boolean marks agency rep groups (142 of 1,983). Also carries its own
  `enable_online_ordering`; do not confuse it with the `mobile_sites` column.
- **`mobile_sites.enable_online_ordering`** — 58 rows true across **55 distinct orgs**. The register reports
  this as "58 orgs" and is wrong.
- **`territories`** — the territory master. Only **23** of the 146 orgs with active iPad reps have any row.
- **`portal_invoices`** — the invoice feed. **56** distinct orgs have rows. Also holds `tracking_number`,
  `tracking_carrier`, `ship_via`; there is a `portal_invoice_tracking_records` table too.
- **`products`** — active is `deleted IS NOT TRUE AND hideable IS NOT TRUE`. Completeness fields:
  `image_exists`, `net_price`, `prices_json`, `category_codes`, `category_code`.
- **`organizations`** — 258 rows. `enable_rep_activity` true for 7. **No** portal / report / dashboard
  feature columns exist here.
- **`org_setting_definitions` / `org_setting_values`** — only **3 definitions total. A dead end.** The feature
  gates the register leans on (`:portal_portal`, `:advanced_reports`, `:link_to_customer_dashboard`) live in
  application YAML, not the database.
- **`orders`** — **113** distinct orgs have orders in the last 12 months. Treat that as the live "active
  client" universe; the register's n=109 roster comes from a CSV outside the repo.
- Other tables that exist and may matter: `customers`, `inventory` / `inventories`, `login_events`,
  `sales_quotas`, `shipping_locations`, `options`, `option_groups`, `matrix_options`, `subscriptions`,
  `subscription_plans`, `subscription_tiers`,
  `billing_and_shipping_codes_to_territory_codes_bridge`.
- **Confirm column names via `information_schema` before writing any query.** Several plausible names do not
  exist, and `organizations` has no `organization_id`.

## Figures to settle first (calibration)

| The register says | Status | What to do |
|---|---|---|
| 58 orgs have Cart | **Wrong** — 58 sites, 55 orgs | Confirm and record the correction |
| 38 of 109 orgs have an invoice feed | Roster-based, unverifiable as stated | Measure against the 113-org live universe |
| Ungating `enable_rep_activity` serves JTBD-032/063 | **Wrong** per the 08-27 pack | Confirm flag counts. `rep_activities` may return permission-denied — record that |
| ~13,800 additional buyers from rolling out reports | **Unverifiable** | Bound it: active buyers per org, so a defensible *range* replaces the point estimate |
| Territory master empty in 32 of 55 orgs [F11] | Superseded | Measure against orgs with active reps (came out 123 of 146) |
| 7.7:1 buyers over reps on the Sales Portal | Scoping unreproducible from the DB | Recompute on eCat Online (came out 7.5:1 — 18,763 vs 2,487) |
| 2,365 admin records | Stale | Re-measure (came out 2,460) |
| 4,058 reps / 87,927 buyers / 667 scopeable / 618 with feed | Reproduced within drift | Re-run and record today's values |

## Investigation lines

### A. Behavioural personas — the highest-value line
The register defines personas as roles with headcounts. Test whether behaviour actually clusters that way.

For internal users: distribution of orders written, distinct customers touched, login and sync recency,
territory-code count, price-code exposure. **How many "active" reps write zero orders in 90 days?** Is there
a real low-volume / high-volume split? Do `primary_rep_group` members behave differently from other reps?

For buyers: order frequency, basket size, distinct SKUs, single vs multiple ship-tos.
**Specifically test whether "dealer buyer" is one population or several** — the top 6 orgs hold 12,473 of
18,763 active buyers, so test whether buyers at large programs behave differently from the long tail.

Output a defensible statement about which personas the data supports, which it splits, and which it cannot
see at all.

### B. Job demand — turn each job into a sized problem
For as many of the 31 jobs as the schema allows, measure the size of the problem the job claims to solve.
Starters, not a complete list — find more:

- Orders with no linked invoice (041, 082)
- Orders referencing deleted or hidden products (044)
- Distribution of inventory snapshot age across orgs (084)
- Collections or products first ordered within the last 12 months (054)
- Active items failing each completeness check *separately*, by org (053)
- Option-value selection counts where options are captured (052)
- Accounts whose trailing-90-day order value is down >30% against their own prior period, per org (014, 062)
- Users whose territory scope would resolve to whole-org today under a naive rule (012)

Where a job's problem cannot be measured, say so explicitly rather than skipping it.
Output per job: problem size, unit, orgs affected, query id.

### C. Reach and sizing
Replace the inherited S / M / L with measured reach: per job, how many orgs, how many users, how many
transactions per period it touches. Rank by reach against inherited effort, and **note every place that
ranking disagrees with `engineering/03-ROADMAP.md`.**

### D. Size the two gaps in commercial terms
For clients with no invoice feed: how much order volume, how many buyers, how many reps, how many customer
records sit behind them? Same for orgs with no territory master. The goal is to turn "these gate more than
the entire build list" into a number a CEO can weigh against engineering cost.

Also produce the target list: of the clients with no feed, which are largest by order volume — that is the
commercial push, in priority order.

### E. Retest the 4-of-31 segment-variation claim
Recompute the structural distributions — price-code count, product count, territory count, order count per
org — from Postgres rather than the roster CSV. Test whether the variation is genuinely structural rather
than segment-driven, and whether the four named jobs (012, 013, 053, 083) are the right four.

**This claim is load-bearing for "build one layer, parameterised." If it breaks, that is the most important
finding in the whole exercise.** Do not soften it either way.

### F. Direction of travel
Everything in the register is point-in-time. Measure 12–24 month trends in active buyers, active reps,
orders per org, orgs with invoice feeds, and catalog size. Is the buyer population growing faster than the
rep population? Does any trend reverse a priority?

### G. One more attempt at the entitlement question
Before declaring the feature gates unverifiable, check `subscriptions`, `subscription_plans`,
`subscription_tiers` and any join table for anything encoding plan-level entitlement. If a plan implies
reports or portal access, that partially grounds the "6 orgs / zero orgs / 13,800 buyers" claims. If it does
not, write the negative result in `08-UNVERIFIABLE.md` and name **exactly which file in the app repo** would
settle it.

## Definition of done

- Every file listed above exists and is populated.
- `00-FINDINGS.md` opens with the five findings that would most change what we build, each with its number
  and query id.
- Any figure in `PERSONA-READOUT.html` that your work contradicts is listed explicitly in
  `01-CALIBRATION.md` under a heading "Must change in the readout".
- No claim anywhere without a query id or an explicit `CODE-AUDIT` / `JUDGMENT` tag.
- Every query is saved and re-runnable, with its result summarised in the file header.

## What this feeds

A CEO readout answering three things, in his words: a substantive improvement to the persona-group view; a
jobs-to-be-done requirements view for analytics per persona group; and where each of those lands on the
existing product. Anything that does not serve one of those three is background — measure it if it is cheap,
but do not let it drive the findings.
