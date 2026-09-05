# SERV-2178 — Diagnosis (Lane 0 / FIX) — ISOLATION ON (markdown only, no code applied)

**Ticket:** [SERV-2178](https://supercatsolutions.atlassian.net/browse/SERV-2178) — "Sales Portal doesn't grant access to all territories" · Story · High · In Progress · assignee Brent Sanders
**Scope of ticket (per Chuck's clarification):** the **RepNumber-on-the-order/invoice** access path only, gated by the managed feature `territory_access_via_rep_number`. The customer-file/rep-record path is the sibling ticket [SERV-2180](https://supercatsolutions.atlassian.net/browse/SERV-2180).
**Date:** 2026-07-16

---

## 1. Root cause (plain language)

When `territory_access_via_rep_number` is on, the portal grants a rep access to an order/invoice if the record's **RepNumber** matches one of the rep's territory codes. RepNumber is meant to be a **list** of territory codes (rep code = territory code, and a record can belong to several).

**The whole pipeline treats RepNumber as a single scalar territory code — it is never split on the comma.** So a record with `RepNumber = "SA,SA,SCB"` is turned into **one** territory key `"<orgid>-sa,sa,scb"`, which is not a real territory and matches no rep. The list is effectively lost.

The single point of failure is `format_territory_key`, which just lowercases and prefixes the raw string:

```29:33:/Users/kylorjohnson/supercat-code/supercat_server/app/services/warehouse/extracts_and_transforms/format.rb
  def format_territory_key(organization_id, territory_code)
    return nil if territory_code.blank?

    "#{organization_id.to_s}-#{territory_code.downcase}"
  end
```

It is called on the raw `rep_number` in every producer that stamps a territory onto warehouse rows:

- Sales facts (order + invoice + unshipped + legacy paths):
```230:230:/Users/kylorjohnson/supercat-code/supercat_server/app/services/warehouse/extracts_and_transforms/sales_portal_sales_fact.rb
        format_territory_key(organization_id, portal_order.rep_number),
```
(also lines 306, 647, 787 in the same file)
- Order dimension:
```56:56:/Users/kylorjohnson/supercat-code/supercat_server/app/services/warehouse/extracts_and_transforms/sales_portal_order_dimension.rb
      format_territory_key(portal_order.organization_id, portal_order.rep_number),
```
- Invoice dimension: `sales_portal_invoice_dimension.rb:34` (same pattern).

The **access predicate** then compares that scalar fact key against the rep's real (single-valued) territory keys, so a composite key can never match:

```424:435:/Users/kylorjohnson/supercat-code/supercat_server/app/models/warehouse_access.rb
  def territory_code_limit_subquery(org_user = nil, prefix = 'sf')
    return 'true' if org_user && UserTypePermissions.may_access_all_customer_sales_totals?(org_user)

    if Feature.enabled?(:territory_access_via_rep_number, org_user.organization, org_user)
      "(#{prefix}.customer_key IN (select * FROM customer_keys)
          OR #{prefix}.ship_to_key IN (select * FROM ship_to_keys)
          OR #{prefix}.territory_key IN (SELECT * FROM territory_keys))"
    else
      "(#{prefix}.customer_key IN (select * FROM customer_keys)
          OR #{prefix}.ship_to_key IN (select * FROM ship_to_keys))"
    end
  end
```

Same scalar assumption in the page-query path (`FilterItemsByTerritoryCode`, used by Orders / Invoices pages):

```29:34:/Users/kylorjohnson/supercat-code/supercat_server/app/services/warehouse/filter_items_by_territory_code.rb
    if territory_access_via_rep_number
      sql = "#{tablename}.customer_key IN (?)
              OR #{tablename}.ship_to_key IN (?)
              OR #{tablename}.territory_key IN (?)"
      entity.
        where(sql, customer_bridge.select(:customer_key), ship_to_bridge.select(:ship_to_key), territories)
```

…and in the Portal-data investigator (the diagnostic tool), which reports the RepNumber as a single territory:

```152:158:/Users/kylorjohnson/supercat-code/supercat_server/app/services/admin/investigate_portal_data.rb
    def record_territory_codes
      return [] unless record.rep_number.present?

      return [] unless Feature.enabled?(:territory_access_via_rep_number, organization, org_user)

      [record.rep_number]
    end
```

Confirmation that RepNumber is stored raw (no split at import) — the importer maps the CSV `repnumber` straight to the string column, so the comma list is preserved end-to-end but never parsed:

```80:80:/Users/kylorjohnson/supercat-code/supercat_server/app/models/importer/portal_order_importer.rb
        'repnumber'                 => { :type => 'S', :required => false, :field => 'rep_number' },
```

**Net:** the bug is a **single-vs-multi-value modeling gap in the warehouse territory dimension for the RepNumber path**, not an import or a permissions-config problem. (The ticket text says "only the first territory"; the current code is actually stricter — a multi-value RepNumber matches **no** territory via this path. Either way the rep-number grant is broken for lists. Records may still surface via the customer/ship-to territory bridge, so this only breaks the *direct RepNumber grant*.)

Note: `format_territory_key` returns `nil` for blank, but does **not** trim — a trailing comma (e.g. `"ELI,"`) also yields a broken key `"<orgid>-eli,"`, so even effectively-single values with a stray comma break.

---

## 2. Repro steps / org evidence (Postgres MCP, read-only)

**Feature is enabled** for exactly two orgs (code-config YAML, not DB):

```80:82:/Users/kylorjohnson/supercat-code/supercat_server/config/initializers/enabled_features.rb
:territory_access_via_rep_number:
- el
- ctest
```

- `el` = **Eurofase Inc.** (id 152) — feature on, but **0** comma RepNumbers today (so no live customer impact right now).
- `ctest` = **ChuckTest** (id 178) — feature on, **666** orders with comma RepNumbers → this is where Chuck reproduced it ("the plot just thickened").

Sample `ctest` order RepNumbers (org 178):

| rep_number | # orders | resulting (broken) territory key |
|---|---|---|
| `SA,SA,SCB` | 126 | `178-sa,sa,scb` (matches no territory) |
| `ELI,HO,ELI` | 36 | `178-eli,ho,eli` |
| `SA,HO,SCB` | 45 | `178-sa,ho,scb` |
| `ELI,` | 26 | `178-eli,` (trailing comma also breaks) |

**The component codes are real territories.** Across orgs carrying comma RepNumbers, most split codes are genuine customer territory codes — e.g. for `jyc` (Jamie Young), **96 of 135** distinct split RepNumber codes exist as real customer `territory_codes`. So reps assigned to `scb`, `aro`, etc. *should* see these records via the RepNumber grant but do not.

Scale of latent data if the feature is turned on more broadly (orders / invoices with comma RepNumbers):

| org | shortname | orders w/ comma rep | invoices w/ comma rep |
|---|---|---|---|
| 8 | wwjc (Wildwood/Chelsea) | 26,747 | 31,275 |
| 76 | jyc (Jamie Young) | 607 | 111,366 |
| 22 | asi (Abaline) | 5,571 | 6,730 |
| 178 | ctest | 666 | 1 |

**Reproduce in-app:** on `ctest`, as a rep whose territory_codes include `scb` (but not the composite), open Sales Portal → Orders/Invoices. Orders whose only territory link is `RepNumber = "SA,SA,SCB"` do **not** appear via the rep-number grant. Admin → Portal-data investigator on such an order prints *"belongs to territory: SA,SA,SCB"* (singular) — visibly the un-split string.

*(Warehouse fact/dimension tables live in a separate warehouse DB not reachable from the current MCP connection; evidence above is from the source `portal_orders`/`portal_invoices`/`customers` tables plus code trace. A warehouse-side confirmation query is listed in AC below.)*

**Adjacent, not the same:** the KLL analysis (`documentation/KLL_Territory_Sales_Portal_Analysis_Feb_2026.md`) is the *same F1 mechanism* (portal territory access breaks) but a different cause — missing territory assignments / empty `territories` table (SERV-2180 family), not RepNumber list parsing. Keep them separate.

---

## 3. Proposed fix + risk (markdown only — do not apply)

**Design principle:** RepNumber is already stored as a raw comma string in the public DB and the importer already accepts it — so **no public-schema migration and no import-format change are needed** (this shrinks scope vs. the "modify PortalOrder + import process" path floated on the ticket). The gap is purely: *the warehouse represents territory-per-record as a single value.* Fix it in the **warehouse ETL + access predicate** only.

A single record can map to N territories, and `sales_fact` rows are **summed** for totals — so we must NOT emit duplicate fact rows (that would double-count money). Two correct shapes:

### Option A (recommended, smallest correct): array-valued territory key + overlap match
1. **ETL** — split RepNumber into a set of keys instead of one:
   - In the three producers, replace `format_territory_key(org_id, rep_number)` with
     `rep_number.to_s.split(',').map(&:strip).reject(&:blank?).uniq.map { format_territory_key(org_id, _1) }`
     and store into a new `territory_keys text[]` column (keep/deprecate the scalar `territory_key`).
2. **Warehouse schema** — add `territory_keys text[]` to `sales_fact*`, `order_dimension`, `invoice_dimension`; add a GIN index; **bump `schema_version`** on the affected ET classes to force a rebuild.
3. **Access predicate** — change the rep-number branch from scalar `IN` to array overlap:
   - `warehouse_access.rb#territory_code_limit_subquery`: `sf.territory_keys && ARRAY(SELECT territory_key FROM territory_keys)`
   - `FilterItemsByTerritoryCode`: `#{tablename}.territory_keys && ARRAY[...]`
4. **Investigator** — `investigate_portal_data.rb#record_territory_codes` / `record_rep_number_info`: split on comma so diagnostics tell the truth.

No fact-row duplication → totals unchanged. Overlap is only ever used in a WHERE filter, never in a SUM/GROUP, so money math is untouched.

### Option B (more normalized alt): a rep→territory bridge for records
Add warehouse bridge tables `territory_to_order_bridge` / `territory_to_invoice_bridge` (record_key, territory_key), one row per split code; change the rep-number access branch to `EXISTS (… bridge … WHERE territory_key IN territory_keys)`. Keep `sales_fact.territory_key` scalar. Mirrors the existing `territory_to_customer_bridge` pattern; more tables/joins than Option A.

### Rejected: full many-to-many on `PortalOrder`/import (the ticket's "XL")
Bruce White sized the ticket XL assuming we make `PortalOrder` itself many-to-many (schema + import + ETL + warehouse). Not necessary — RepNumber already round-trips as a string; only the warehouse read model needs to understand the comma. Recommend **Option A** and re-size down from XL.

### Risk
- **Layout / catalog coupling:** low. Changes are data-access (warehouse ETL + SQL predicates), not views; no `layouts/ecat` or catalog code touched.
- **Blast radius:** the access predicate is shared by Dashboard + Orders + Invoices + Customers + top-N widgets. Change is additive (widen the rep-number branch); customer/ship-to grants unchanged. Only orgs with the feature on are affected (today: `el`, `ctest`).
- **ETL rebuild required:** bumping `schema_version` triggers a full warehouse rebuild for affected entities — schedule/observe ETL runtime.
- **Data hygiene:** must `strip`/`reject(&:blank?)`/`uniq` to handle trailing commas (`"ELI,"`) and dup codes (`"SA,SA,SCB"`).
- **Totals safety:** must implement as a filter (overlap/EXISTS), never as a fan-out JOIN, or invoice/order totals will inflate. Add a before/after total reconciliation on `ctest`.

---

## 4. Acceptance criteria

1. With `territory_access_via_rep_number` on, a rep whose `territory_codes` include **any** code in a record's RepNumber list sees that order **and** invoice in Sales Portal (Dashboard totals, Orders, Invoices, Customers, top-N).
2. `RepNumber = "SA,SA,SCB"` grants access to reps in `sa`, `scb` (dupes collapsed); `"ELI,"` behaves exactly like `"ELI"`.
3. Reps **not** in any listed territory (and lacking a customer/ship-to grant) still do **not** see the record — no over-grant.
4. **Totals unchanged:** order/invoice/backlog dollar totals on `ctest` are identical before vs. after (no double counting). Reconciliation query passes.
5. Portal-data investigator reports the **split** list (e.g. *"accessible by territories: sa, scb"*), not the raw string.
6. Feature **off** → behavior byte-for-byte unchanged (customer/ship-to bridge only).
7. Warehouse verification query (run against warehouse DB post-rebuild): **0** territory keys derived from RepNumber contain a comma; every derived key resolves to a row in `territory_dimension`.
8. Regression: an org **without** the feature (any normal portal org) shows no change in visible records or totals.

---

## 5. Handoff

Stop here (isolation on). Paste this into the Orchestrator (05) for a Review Card. **Recommend Option A**, re-size from XL → M (warehouse-only; no public migration / import change). Do not implement until: `ISOLATION OFF — GO on SERV-2178`.

Related but out of scope for this ticket: SERV-2180 (customer-file/rep-record territory bridge), SERV-2196 (ShipToTerritoryCodes restriction), SERV-2113 (Portal Checker — note its `record_territory_codes` shares this same un-split bug and should be fixed in the same PR).
