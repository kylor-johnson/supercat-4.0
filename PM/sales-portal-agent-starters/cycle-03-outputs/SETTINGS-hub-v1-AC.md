# Bet E — Portal & Access hub AC (build)

**Date:** 2026-07-18 · **Lane:** 0→1 · **Isolation:** ON (spec only)  
**Demo-only companion (NOT this file):** `SETTINGS-hub-v1-DEMO-SPEC.md`  
**Triage authority (do not re-triage 134 toggles):** `cycle-02-outputs/PORTAL-SETTINGS-CONTROL-PLANE.md`  
**Plan pointer:** `TECHNICAL-PLAN.md` §8  
**Eng footnotes:** SERV-2254 (self-service anchor) · SERV-2178 class (territory match) · see `FILTER-TRUTH-AC.md` + `cycle-01-outputs/FIX-diagnosis-territory-datefilter.md`  
**Ship gate:** `SHIP-READINESS-bet-e.md` — build only after `ISOLATION OFF — GO on Bet E` (or Wave 0 / named SERV)

> **Bet F persona note (footnote — no AC change).** The Portal & Access hub is the **Admin/ops persona's default home** in Bet F (`IA-PRIORITY-MATRIX.md`, `SURFACE-PLACEMENT.md` B3). The client-org-admin vs SuperCat-superadmin gates here are exactly Bet F's fail-closed rules **R3** (revenue definitions visible-but-locked) and **R4** (client vs SuperCat gates) — one persona, permission tier. Bet F places this hub as the ops home; it does not add or move any AC-E section. This AC body is unchanged.

---

## Problem (one mechanism)

134 toggles · 6 layers · 39 YAML flags · zero admin surface → every non-trivial portal change is a SuperCat ticket, and access rules (`territory_access_via_rep_number`) hide in deploy config. An org-admin cannot answer “why can’t this user see the portal?” in-product.

**Done for this bet** = Wave 0–1 down-payment landed; hub surfaces ~30 portal survivors; ~18 client self-serve; revenue definitions visible-locked; Experiments = sunset-dated YAML only; territory match mode graduates with Bet A — not alone.

---

## AC-E0 — Waves / appetite (frozen)

| Appetite | Waves | What ships | Shape Up size |
|---|---|---|---|
| **Small-batch down-payment** | **0–1** | Dead-flag deletes + graduate named stable flags (YAML shim OK one release) | 1–2 weeks |
| **Big-batch hub** | **2–5** | 6-section Portal & Access hub + self-service + locked revenue + Experiments accountability | Full cycle (or sequential smalls inside one bet) |

### Wave 0 — Delete 5 dead flag entries (exact)

Remove allowlist entries from `config/initializers/enabled_features.rb` only. Features that ship without the flag stay.

| Flag | Why DEPRECATE | Receipt |
|---|---|---|
| `eol_dashboard_filters` | Allowlisted (cci, sarreid); **0** code reads | control-plane headline Cat. 1 |
| `tcgc_name_fields` | Allowlisted (sarreid); **0** refs | same |
| `allow_user_group_from_selecting_price_levels` | Allowlisted (ihw, mhc + users); **0** refs | same |
| `sales_quotas` **(flag entry only)** | Feature gated by `@current_org.sales_quotas.exists?`, not the flag | same |
| `option_mapping` **(flag entry only)** | `OptionMapping` CRUD/importer ungated | same |

**Do NOT delete** (product ship/cut — human gate): `avery_5392_landscape`, `placements_field_configuration`, `product_url_variable`, `credit_card_support`.

### Wave 1 — Graduate named high-usage stable flags

Promote to labeled Org/UserType/Site settings; keep YAML read-through shim one release. Minimum set (control-plane C.1 / TECHNICAL-PLAN §8.3):

`advanced_reports` · `twenty_option_types` · `market_commitments` · `option_forms` · `ship_cancel_date_tweaks` · `order_item_tags` · `rma_custom_fields` · `override_order_footer_text` · `admin_rma_email_notification`

Catalog-adjacent graduates may land outside the Portal hub (Site / catalog settings) — still count toward “leave YAML.”

### Wave 2–3 — Hub UI (Big)

| Wave | Sections | Editor |
|---|---|---|
| **2** | **Enablement** (+ in-product decision tree) → then **Territory & data access** (synching/totals; match mode UI shell may be read-only until Wave 4) | Client admin (+ SuperCat for force-on) |
| **2–3** | **Reports & export** (advanced reports + unify export) | Client admin |
| **3** | **Portal display** self-service | Client self-service |

### Wave 4 — Territory match mode (pairs with Bet A)

`territory_access_via_rep_number` → labeled **Territory match mode**, SuperCat superadmin only.  
**Ships with Bet A / SERV-2178 class — not alone.** See AC-E4.

### Wave 5 — Revenue definitions locked + audit

Six metric-law settings visible read-only; mutation = SuperCat + **INSIGHT** sign-off + audit log. See AC-E3.

### Betting-table note

Wave 0–1 **may ride with Bet A** in the same cycle if the table says so (small-batch de-risk). Hub UI (2–5) remains the Big appetite. WIP progression stays structural trust → shell → IR; Bet E is the control-plane bet shaped now — not a permanent recentering on Settings.

---

## AC-E1 — Enablement decision tree

| # | Given | When | Then |
|---|---|---|---|
| E1.1 | Org-admin opens Portal & Access → Enablement | Diagnoses “why can’t this user see the portal?” | In-product tree walks site → data → preview → user-type portal → (separately) dashboard gates; identifies blocking layer without a support ticket |
| E1.2 | Same | Blocking layer is site off | Copy names `mobile_sites.enable_sales_portal` and offers fix in Enablement |
| E1.3 | Same | Blocking layer is user-type portal off | Copy names `user_types.enable_sales_portal` (default true; explicit OFF exists) |
| E1.4 | Same | Portal visible but dashboard missing | Tree shows dashboard AND-chain separately (not conflated with portal nav) |

### Decision tree → Rails mapping (build copy must match)

```
Can this user see the Sales Portal?
│
├─ 1. Site ON or force-display?
│     MobileSite.enable_sales_portal?
│       OR Feature :force_portal_display
│     Cite: ecat_permissions_helper.rb:20–26
│     └─ NO → “Portal is off for this site.” Fix: Enablement site switch
│           (force-display = SuperCat override only)
│
├─ 2. Dataflow :should_show_portal?
│     any_portal_records_for_org (PortalOrder OR PortalInvoice for org)
│       AND any_portal_records_for_user (customer_number OR not sync_no_customers)
│     Cite: eol_left_nav_dataflow.rb:336–352
│     Consumed at: ecat_permissions_helper.rb:27
│     └─ NO → “No portal orders/invoices imported”
│           OR “user scoped to zero customers”
│           (import order_data/invoice_data.csv; or Territory → customer_synching / territory_codes)
│
├─ 3. Not in ordering-preview?
│     session[:preferred_pricing] must be nil
│     Cite: ecat_permissions_helper.rb:28
│     └─ NO → “User is in a pricing-preview session.” (transient)
│
└─ 4. User-type allows portal?
      user_type.enable_sales_portal
      Cite: ecat_permissions_helper.rb:29
      └─ NO → “This user-type has the portal disabled.”
      └─ YES → ✅ Portal visible (nav)

Then, SEPARATELY — Dashboard (should_display_portal_dashboard?):
   @show_customers
   AND (Feature :portal_portal OR Org.enable_portal_dashboard)
   AND user_type.enable_portal_dashboard   (default false)
   AND user_type.display_sales_portal_totals (default true)
   Cite: ecat_permissions_helper.rb:54–58
```

**Cross-lane:** This tree diagnoses **access/enablement**. It does **not** replace invoice/dashboard **filter truth** (Bet A / `FILTER-TRUTH-AC.md`). What’s broken remains the teaching surface for filter lies; Settings is the long-term home for access/display toggles.

---

## AC-E2 — Client self-service survivors (~18)

Org-admin (or end-user where noted) can change these **without YAML / deploy / SuperCat ticket**. Named from control-plane survivors (B.2 / north-star) — not a re-triage.

| # | Setting / capability | Hub section | Who edits |
|---|---|---|---|
| 1 | `mobile_sites.enable_sales_portal` | Enablement | Org-admin |
| 2 | `user_types.enable_sales_portal` | Enablement | Org-admin |
| 3 | `user_types.enable_portal_dashboard` | Enablement | Org-admin |
| 4 | Org `enable_portal_dashboard` (unified enablement model) | Enablement | Org-admin |
| 5 | `user_types.display_sales_portal_totals` | Enablement / Reports | Org-admin |
| 6 | `user_types.customer_synching` (All / Associated / None) | Territory & access | Org-admin |
| 7 | Permission `access_all_customer_sales_totals` | Territory & access | Org-admin (+ SuperCat audit) |
| 8 | `sales_portal_currency_code` | Portal display | Org-admin / self-service |
| 9 | `display_quantity_available` | Portal display | Org-admin / self-service |
| 10 | `display_quantity_backordered` | Portal display | Org-admin / self-service |
| 11 | `eol_customer_graph` (graduated) | Portal display | Org-admin / self-service |
| 12 | `link_to_customer_dashboard` (flag+org consolidated) | Portal display | Org-admin / self-service |
| 13 | Backlog vs invoiced **label** (display chrome only — not metric flag) | Portal display | Org-admin / self-service |
| 14 | `advanced_reports` (graduated) | Reports & export | Org-admin |
| 15 | Unified **export** permission (folds `xlsx_export` + `can_export_eol_data` + `enable_disable_portal_export_by_user_group`) | Reports & export | Org-admin |
| 16 | Permission `view_sales_reports` | Reports & export | Org-admin |
| 17 | `user_types.territory_url` / `territory_url_label` | Portal display | Org-admin / self-service |
| 18 | End-user `ui_preference` / settings (existing self-serve) | (user prefs — linked from hub) | End user |

| # | Given | When | Then |
|---|---|---|---|
| E2.1 | Org-admin with hub access | Enables portal for a site + user-type gates | Reps in that type see portal without YAML edit |
| E2.2 | Same | Changes display toggles (currency, qty cols, customer graph) | Portal UX updates; **no** metric-law columns mutate |
| E2.3 | Same | Sets export per user-group via unified control | One answer to “can this group export?” — not three conflicting toggles |

**SuperCat-only (not in the 18):** `force_portal_display`, Territory match mode, Experiments canaries, Revenue definitions, `portal_portal` until folded into enablement model.

---

## AC-E3 — Revenue definitions locked

| # | Given | When | Then |
|---|---|---|---|
| E3.1 | Org-admin opens Revenue definitions | Views section | All six settings render **visible, read-only** with 🔒 |
| E3.2 | Same | Attempts to mutate any row | UI refuses; copy: changes require **SuperCat + INSIGHT** |
| E3.3 | SuperCat operator | Changes a definition after INSIGHT sign-off | Audit log records who/when/old/new |

### Named locked settings (metric law)

| Setting | Why locked |
|---|---|
| `portal_data_type` | Orders↔invoices correlation — changes dashboard math |
| `portal_calculations` | Calc engine version — metric law |
| `excluded_portal_order_backlog_order_statuses` | Changes what “backlog” means (sarreid `[]` vs cci `["C","Q","X","Z"]`) |
| `sales_portal_sales_facts_filter_configuration` | Defines sales-facts filter set |
| `backlog_instead_of_amount_invoiced` | Headline meaning (orders page) — KEEP-YAML→INSIGHT today |
| `max_portal_data_age_months` | Caps history window for totals |

**Copy requirement (exact intent):**  
> “This setting is managed by SuperCat + INSIGHT. Changes require a support request to ensure metric reconciliation to invoiced `net_amount`.”

**Also hand to INSIGHT (not client-editable):** `internal_warehouse_unsubmitted_orders` (which orders count).

**Metric law unchanged:** sales / invoiced = `SUM(portal_invoices.net_amount)` (RTD-clamped, $5M cap, STRONG); quotes ≠ sales; export = UI; backlog ≠ sales; no FULL; no RS-01 lead; no EBR-772/776.

---

## AC-E4 — Territory match mode (pairs with Bet A)

| # | Given | When | Then |
|---|---|---|---|
| E4.1 | SuperCat superadmin | Opens Territory & data access | Sees labeled **Territory match mode** (`territory_access_via_rep_number` or successor label); options: `territory_codes` (default) vs `rep_number` |
| E4.2 | Org-admin (non-superadmin) | Same | Control is **disabled / read-only** — cannot flip match mode |
| E4.3 | Wave 4 ships | Match mode graduates from YAML | Change is audited; allowlist in `enabled_features.rb` is not the long-term UI |
| E4.4 | Bet A filter honesty **not** shipped | Hub UI shows match mode | Copy must **not** claim invoice-list / dashboard territory filters are fixed |

### Rails / diagnosis pairing (mandatory)

| Fact | Cite |
|---|---|
| Flag switches warehouse WHERE to include `territory_key` | `warehouse_access.rb:427–434` |
| Also read on orders/invoices/items paths | `get_orders_for_orders_page.rb:124` · `get_invoices_for_invoices_page.rb:126–127` · `filter_items_by_territory_code_limit.rb:44` |
| Allowlisted today | `enabled_features.rb` → `el`, `ctest` only |
| Bet A AC | `FILTER-TRUTH-AC.md` A1.* (fail-closed empty keys; assigned territories scope book) |
| Eng diagnosis | `FIX-diagnosis-territory-datefilter.md` — warehouse bridge, not live `org_users.territory_codes`; SERV-2178 / 2196 class |
| SERV footnotes | SERV-2178 / 2180 (EBR-180 XL shelf — separate appetite); SERV-2196 ship-to over-grant |

### Demo / trust note (sarreid)

**sarreid** has **99.8%** multi-territory bill-tos → territory-scoped demos can surface SERV-2196 over-grant live. Do not treat Settings Territory section as proof that filter truth is fixed. Prefer **wwjc** (comma-rep ∩ over-grant) or a zero-exposure org for filter honesty demos; Settings may still show sarreid config values for enablement / revenue comparison.

**Rule:** Wave 4 **does not ship without** a Bet A path (same cycle GO or explicit dependency). Shipping hub chrome that implies filter truth without Bet A = fail AC-E4.4.

---

## AC-E5 — Experiments lab

| # | Given | When | Then |
|---|---|---|---|
| E5.1 | SuperCat superadmin opens Experiments | Views lab | Every remaining YAML canary row shows: flag · human label · **owner** · **ticket** · **sunset date** · current state |
| E5.2 | Any canary without sunset | — | **Cannot** stay as open-ended allowlist; must get sunset or ship/cut decision |
| E5.3 | Wave 0 complete | Dead flags listed above | Removed from YAML; not shown as “active experiments” |

### Canary roster (seed — fill owner/ticket/sunset at build)

| Flag | Class | Notes |
|---|---|---|
| `netsuite_rest_api` | Active canary | shl; integrations owner |
| `multifile_ephemeral_import` | Active canary | Import pipeline |
| `override_eol_login` | Auth-sensitive | Superadmin only |
| `override_company_info_at_group` | SC-internal | sc / sc_test |
| `asi_shared_orders` | Partner-specific | Keep gated |
| `avery_5392_landscape` | Dormant-wired | **Ship/cut human gate** — `ipad_report.rb:311` |
| `placements_field_configuration` | Dormant-wired | Ship/cut — gridview fields |
| `product_url_variable` | Dormant-wired | Ship/cut — `custom_field.rb:344` |
| `credit_card_support` | Dormant-wired | Ship/cut — `tools_controller.rb:397` |

Revenue-meaning flags (`backlog_instead_of_amount_invoiced`, `internal_warehouse_unsubmitted_orders`) are **not** Experiments — they belong under Revenue / INSIGHT (AC-E3).

---

## AC-E6 — Count the win

| Metric | Today | Target (done) |
|---|---|---|
| Total toggles | 134 across 6 layers | **~1 hub**, **~30 portal-relevant survivors** surfaced (rest routed to Catalog/Site/User-Type UIs) |
| YAML feature flags | 39, no UI | **5 deleted** (Wave 0) · ~23 graduated · **~11 in Experiments with sunset** · **0** open-ended allowlists without expiry |
| Portal decision layers | 6 | **1** Portal & Access hub + documented decision tree |
| Client self-service | ~0 | **~18 of ~30** (AC-E2) |

| # | Given | When | Then |
|---|---|---|---|
| E6.1 | Post Wave 0–5 (or agreed slice) | Scorecard counted | Numbers meet control-plane C.2 targets (± consolidation renaming) |
| E6.2 | Client org-admin | Day-2 ops | Can enable portal, set territory/data access (non–match-mode), adjust display **without** a SuperCat ticket |
| E6.3 | Support | “Why can’t this user see the portal?” | Answered from in-product tree (E1) |

---

## No-gos

- Client-editable **revenue definitions** (or any UI that mutates metric meaning without INSIGHT)
- Deleting the **4 dormant-wired** flags without an explicit ship/cut call
- Changing metric meaning / spine without INSIGHT sign-off
- Shipping hub UI that **implies filter truth is fixed** when Bet A isn’t (AC-E4.4)
- Shipping Wave 4 territory match mode **alone** (without Bet A / SERV-2178-class path)
- Re-triaging all 134 toggles from zero (diff against control-plane only)
- Unparking EBR-772 / EBR-776
- **Rails / `supercat-code/` edits while ISOLATION ON**
- Expanding What’s broken into Settings; rebuilding list tabs / Intelligence inside this bet

---

## Verify checklist (pre-build / staging)

### Enablement tree + backlog exclusion display

| Org | Why |
|---|---|
| **sarreid** | Portal ON; `excluded_portal_order_backlog_order_statuses = []` (inflated backlog teaching); 99.8% multi-territory — **do not** use as filter-truth proof |
| **cci** | Portal ON; backlog exclusions `["C","Q","X","Z"]` — locked Revenue section contrast |
| **pf** (optional unlock) | Clean Tier-2; blocked today by `enable_sales_portal = false` — Enablement win story |
| **wwjc** / zero-exposure org | Prefer for Bet A territory honesty when pairing Wave 4 |

- [ ] E1 tree copy matches `ecat_permissions_helper.rb:20–58` + `eol_left_nav_dataflow.rb:336–352`
- [ ] E3 sarreid vs cci backlog-status exclusion renders correctly (locked)
- [ ] E2 toggles do not write metric-law columns
- [ ] E4 match mode requires superadmin + audit; disabled for org-admin
- [ ] E5 every canary has owner + ticket + sunset (or ship/cut)
- [ ] Hub does not mislabel catalog/pricing toggles as portal settings
- [ ] **Wave 0 regression:** zero `Feature.enabled?` / `enabled_for_organization?` breakages on formerly allowlisted orgs (cci, sarreid, ihw, mhc, opame, yw, omc, demos for dead set)
- [ ] Wave 4 not released without Bet A path confirmation

**Build only after:** `ISOLATION OFF — GO on Bet E` (or `ISOLATION OFF — GO on Bet E Wave 0` / named SERV-2254 path). See `SHIP-READINESS-bet-e.md`.

---

## Cross-lane rules (frozen into this AC)

1. **Wave 4 ↔ Bet A** — Territory match mode pairs with `FILTER-TRUTH-AC.md` / SERV-2178 footnotes / `FIX-diagnosis-territory-datefilter.md`.  
2. **Wave 5 ↔ metric law / INSIGHT** — never client self-serve.  
3. **Enablement tree ≠ filter truth** — access diagnosis does not replace invoice/dashboard territory scoping honesty.  
4. **What’s broken = teaching; Settings = long-term home** for access/display toggles.  
5. **Demo chrome** (Wave badges, Delete buttons, static trees) ≠ eng directive — `DEMO-SURFACE-CONTRACT.md` + demo-spec §5.

---

## Artifact map

| Artifact | Role |
|---|---|
| `PORTAL-SETTINGS-CONTROL-PLANE.md` | Triage + migration (consume) |
| `SETTINGS-hub-v1-DEMO-SPEC.md` | Prototype scope only |
| **`SETTINGS-hub-v1-AC.md`** (this file) | Build Given/When/Then |
| `SHIP-READINESS-bet-e.md` | GO gate |
| `TECHNICAL-PLAN.md` §8 | Waves + architecture |
| `design-system/app/sales-portal-internal-demo.html` | Settings view — layout/copy reference |

---

*Bet E AC freeze 2026-07-18. Demo-spec is not build AC. Betting-table GO still required before Rails.*
