# Reconciliation — framework v3.5 vs. current skills vs. live schema

Verified 2026-08-18 against the live DB and the `~/.claude/skills/ecat-*` set
(last updated 2026-08-11, i.e. newer than every file in `onboarding-models/`).

Where they disagree, **the live schema wins, then the skills, then the framework.**
Each item below is either already applied in `queries.py` / `collector.py`, or is
flagged as an open decision for you.

---

## 1. BLOCKER (fixed) — `customers.company_name` does not exist

`Phase_Anchors.md § Phase 7` clause 3 matches orders to customers on
`lower(trim(customers.company_name))`.

There is no `company_name` column on `customers`. The real column is **`name`**.
Verified column list: `id, organization_id, created_at, updated_at, billing_*,
buyer_*, code, default_price_code, distribution_source, name, shortname, terms,
territory_codes, trade_name_codes, custom_fields, ...`

Run verbatim, every Phase 7 evaluation throws `UndefinedColumn`. Since Phase 7 is
the terminal gate, the framework could never have completed a run.

**Applied:** `queries.py § ORDERS_MATCHED_TO_CUSTOMERS` uses `customers.name`.
Validated live on tcd — 7 submitted orders, 6 matching a real customer row.

**Action for you:** fix the clause in `Phase_Anchors.md` so the two don't drift.

---

## 2. HubSpot is dropped as an identity source — and it has to be

`Phase_Anchors.md` already demotes HubSpot for cohort detection, but keeps it as
step 3 of `client_domains[]` resolution. In practice it is worse than unused —
it is actively misleading:

| shortname | `org_master.hubspot_company_id` | resolves? |
|---|---|---|
| leg | 36296098959 | **dangling** — no such row in `hubspot.company` |
| mali, pebl, tcd | present | yes |
| drf, libco, tcs | **absent** | no |

Routing identity through HubSpot resolves 3 of 7 clients. Routing it through
Postgres resolves 7 of 7.

**Applied:** `resolve_client_domains()` implements override → `order_email_recipient`
→ admin-email fallback, with HubSpot removed entirely.

Verified: `order_email_recipient` alone resolves drf, libco, pebl, tcd. `leg` and
`mali` are blank and fall to the admin-email fallback; for `leg` that yields
`legrand.com` cleanly (6 users, `supercatsolutions.com` excluded), which matches
7 Fathom meetings and 5 HelpScout tickets.

**Action for you:** delete step 3 from `Phase_Anchors.md § Resolving client_domains[]`.

---

## 3. `onboarding_assessment.onboarding_clients` is broken right now

The view references `hubspot.company.properties_hs_date_entered_evangelist`.
HubSpot renamed it to **`properties_hs_v_2_date_entered_evangelist`**. Every query
against the view fails to parse.

Given #2, the right fix is probably to **retire the view**, not repair it.
`fathom_recent_meetings` and `helpscout_tickets` are healthy and current (both had
rows from 2026-08-18 when checked).

---

## 4. `onboarding_assessment.client_self_names` does not exist

`Phase_Anchors.md § Phase 7` says: *"If `client_self_names[]` is set in
`onboarding_assessment.client_self_names`, it is used as an additional exclusion."*

That table has never been created — the dataset contains only the three views.
The clause is conditional so it degrades safely, but it reads as if a real
exclusion list is in play when none is.

**Applied:** the collector emits `unmatched_order_names` (submitted orders whose
bill-to matches no customer row) so `SELF_TEST_SUSPECTED_NOT_CUSTOMER` can fire
from data rather than from a table that doesn't exist.

---

## 5. Three undocumented `import_events` block types

Enumerated from live data across drf/mali/pebl/tcd/leg:

| block type | occurrences | in spec? |
|---|---|---|
| Images | 612 | mentioned in passing |
| Products | 429 | yes |
| Option Groups | 77 | yes |
| Options | 67 | yes |
| **Option Images** | 62 | **no** |
| Inventory | 55 | yes |
| Product Stories | 49 | yes |
| Customers | 44 | yes |
| **Matrix Options** | 30 | **no** |
| **Taxonomies** | 6 | **no** |

`Taxonomies` matters: `ecat-onboarding-orchestrator` lists "taxonomy
pre-registration" as a pre-import gate (*"groups never auto-create — real fatals
in mali's log"*), so a fatal Taxonomies block is a real signal the framework
currently ignores.

Also confirms the spec's own warning empirically: **Images + Option Images are 674
of 1,431 events**, so any "last N rows" window buries core-file events. The
collector's `IMPORT_EVENTS` query is deliberately unwindowed.

**Applied:** `OBSERVED_FILE_TYPES` and `NOISE_FILE_TYPES` in `queries.py`.

---

## 6. The cohort has fully turned over since the framework was written

`RUN_PROMPT.md` says the cohort is `tcs, drf, libco, pebl` as of 2026-06-05.
Today the auto-cohort query returns exactly one org:

```
leg — Legrand US — onboarding — created 2025-06-10
```

`drf`, `libco`, `pebl` are now `status='active'`; `tcs` is `fully_suspended`.

Two consequences:
- The framework has never been run against its own cohort, and that cohort no
  longer exists. **The only forward test available is `leg`.**
- Every other validation has to be a backtest.

---

## 7. Status vocabulary — take it from the skill, not the framework

`ecat-postgres-audit` (2026-08-11) carries the authoritative enum, which the
framework does not state:

```
Organization::Status = onboarding | inactive (default) | demo | test
                     | active | sync_suspended | fully_suspended
```

`sync_allowed?` is false for **both** suspended values — a suspended org will not
sync no matter how clean the import. The framework's cohort filter excludes
`demo`/`test` but says nothing about the suspended states.

**Open decision:** should `sync_suspended` / `fully_suspended` be an explicit
cohort exclusion rather than relying on them not being `'onboarding'`? I left the
spec's filter as-is — changing a cohort rule is your call, not a bug fix.

---

## 8. The TCD "hideable" example is stale

`Phase_Anchors.md § Phase 3` cites TCD as the "imported but hidden via Hideable
strategy" pattern. Live today: **397 active products, 397 visible, 0 hidden.**
The metric is still worth collecting; the example no longer illustrates it.

---

## 9. Unused signal — the onboarding health API

`ecat-postgres-audit` documents
`GET /api/v1/<shortname>/mcp/organizations/health`, returning a six-category
onboarding scorecard (foundational, catalog, customer/pricing, inventory, orders,
engagement).

The framework derives several of these by hand from raw counts. Worth deciding
whether the API becomes the source and the framework grades against it, or the
framework stays independent so the two can disagree usefully. **Not wired up** —
it needs the Rails MCP API auth from `~/.supercat/mcp-credentials.json`, and it's
inside the VPN like everything else.

---

## 10. `scripts/stage_gated_data_collector.py` cannot run

The v2 collector expects `DATABASE_URL` or `PG*` env vars. None are set,
`psycopg2` is not installed, and it points at a **different** BigQuery service
account (`...-dbfab43c27bb.json`) than the one your MCP actually uses
(`...-ac0671b8d44a.json`).

It belongs in `_archive/` alongside the rest of the v2 stage-gated framework.

---

## 11. The constraint that shaped this collector

`mcp-postgres-tools.tools.supercatsolutions.com` is **split-horizon DNS**:

```
@8.8.8.8       → NXDOMAIN
@VPN resolver  → 172.100.120.49, 172.100.142.183
```

Nothing outside the network can resolve it, so no cloud-hosted agent can query
Postgres regardless of credentials. The collector runs inside the VPN and pushes a
dated snapshot to BigQuery; the agent reads the snapshot.

This is the same contract `preflight_gate.py` already uses (`--live-state` passed
in, never queried), and it has the same benefit: the snapshot is dated, so stale
state can never be silently reported as current.

---

## Open credential ask (exactly one)

**Read-only Postgres credentials** (a `DATABASE_URL` against a read replica, usable
from inside the VPN). That is the only thing standing between this collector and an
unattended cron job.

Without it the MCP path works today, but it needs a human or a headless Claude Code
run to execute the statements.

Everything else is already in hand:
- BigQuery service account — exists, non-interactive, portable to any host
- Fathom + HelpScout — already in BigQuery, fresh to today
- No HubSpot access needed
- No VPN change, no tunnel, no Cloudflare service token
