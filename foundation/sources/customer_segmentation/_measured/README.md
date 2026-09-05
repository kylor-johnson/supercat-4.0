---
id: MEAS-README
title: Measured against production — what, when, how to re-run
version: 1.0
status: evidence pack
date: 2026-08-31
owner: Kylor Johnson
database: supercatprod (read-only, via supercat-postgres-vpn MCP)
---

# What this is

The persona / JTBD / surface register in `../` was built from documents and a stamped CSV roster.
It is internally careful, but it **asserts** in a number of places where Postgres can **measure**.
This directory replaces assertion with measurement wherever the database can settle it, and says
explicitly where it cannot.

**This is evidence, not prose.** A later pass rebuilds the CEO readout from what is here.

## Rules this pack was produced under

1. **Read-only.** Every statement below came from a `SELECT`. No writes, no DDL. Where a query
   would have scanned something enormous it was aggregated or sampled, and the header says so.
2. **No number without a query.** Every figure carries a query id (`Q0NN`) and the run date.
3. **Nothing in `../` was edited.** All output is confined to this directory.
4. **Nothing was silently corrected.** Where a measured number disagrees with the register, both
   are recorded in `01-CALIBRATION.md`, with the query and a stated verdict.
5. **Every claim is tagged** `MEASURED`, `CODE-AUDIT`, `JUDGMENT`, or `UNVERIFIABLE-FROM-DB`.

## Where to start

| File | What is in it |
|---|---|
| **`00-FINDINGS.md`** | Ranked findings. **Read the first five.** |
| `01-CALIBRATION.md` | The register's stamped figures vs live, with a verdict on each, and a **"Must change in the readout"** section |
| `02-PERSONA-EVIDENCE.md` | Line A — which personas the behaviour actually supports |
| `03-JOB-DEMAND.md` | Line B — measured problem size per job |
| `04-REACH-AND-SIZING.md` | Line C — reach per job, re-ranked against `../engineering/03-ROADMAP.md` |
| `05-GAPS-SIZED.md` | Line D — the two client-data gaps in commercial terms, plus the target list |
| `06-SEGMENT-VARIATION.md` | Line E — the load-bearing 4-of-31 claim, retested live |
| `07-TRENDS.md` | Line F — direction of travel, 24 months |
| `08-UNVERIFIABLE.md` | What the database cannot settle, and exactly what would |
| `queries/QNNN.sql` | 47 queries. Each header carries purpose, run date, and its result |
| `data/QNNN.csv` | Result sets for the multi-row queries a later pass may want to chart |

## Definitions used throughout

These are applied consistently. Where the register used a different one, the difference is called
out rather than absorbed.

| Term | Definition |
|---|---|
| **Dealer buyer** | `org_users` with non-blank `customer_number` |
| **Internal user / rep** | `org_users` with blank `customer_number` |
| **Active iPad rep** | internal, `disabled IS NOT TRUE`, `last_ipad_login_at` within 90 days |
| **Active buyer** | buyer, `disabled IS NOT TRUE`, `last_ecat_online_login_at` within 90 days |
| **Active-client universe** | the **112** orgs with any non-deleted order in the trailing 12 months (`orders`) |
| **Has an invoice feed** | at least one row in `portal_invoices` (**56** orgs; only **44** have rows dated in the last 12 months) |
| **Has a territory master** | at least one row in `territories` (**26** orgs) |
| **Active product** | `products` where `deleted IS NOT TRUE AND hideable IS NOT TRUE` |
| **Order value** | `orders.total`, submitted and not marked deleted — **see the outlier warning in Q055** |
| **Record vs person** | `org_users` rows are per-org *memberships*. `org_users.user_id` is the *person*. The register counts records; both are given here |

## Schema notes that cost time

- `org_users.territory_codes` is `json`. Cast `::text` to test emptiness. Empty forms in the wild:
  `null`, `[]`, `{}`, `""`.
- `orders.order_items` is **TEXT**, not a table. eCat order lines are not queryable per-SKU.
  ERP-fed lines are, in `portal_order_items`.
- `products` has **no `created_at` and no `updated_at`**. Only `id`. (Q035)
- `portal_orders` / `portal_invoices` join to their item tables on
  `organization_id + order_number` / `invoice_number`. There is no foreign key.
- `rep_activities` returns **permission denied** for this role, and does not appear in
  `information_schema.columns` for us. (Q007)
- `login_events.user_id` is `users.id`, **not** `org_users.id`. Join on
  `user_id + organization_id` or the counts inflate.
- `organizations` has no `organization_id` column, and no portal / report / dashboard feature columns.
- `user_types.enable_online_ordering` is a **varchar**, not a boolean, and is a different thing from
  `mobile_sites.enable_online_ordering`.
- `qtt_sales_data_*` tables are transient query artefacts. Ignore them.

## How to re-run

Every file in `queries/` is standalone and re-runnable against `supercatprod` with a read-only role.
Run them in id order; nothing depends on anything else. Each header states the result it produced on
2026-08-31 so drift is visible immediately.

Two caveats for whoever re-runs this:

- **The 90-day windows slide.** Population counts will drift by tens of records within a week and by
  low hundreds within a month. That is expected and is not a finding.
- **`Q040` needs the roster.** Its `VALUES` list of 109 org shortname → v4 segment pairs comes from
  `../_working/data/orgs.csv`. The full list is reproduced in `data/Q040.csv` (columns `short`,
  `segment`, where segment is encoded `1` = Luxury Specification, `2` = Premium Trade Brand,
  `3` = Mid-Market Multi-Channel, `4` = Volume Distribution).

One operational note: the MCP query validator rejects `percentile_disc` / `percentile_cont`. Medians
in this pack are computed either as explicit band counts in SQL or in Python over a saved CSV. Both
routes are shown.
