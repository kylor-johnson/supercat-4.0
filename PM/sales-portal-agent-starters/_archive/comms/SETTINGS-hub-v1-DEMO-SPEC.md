# Settings Hub v1 — Demo Spec (Bet E, cycle-03)
**Date:** 2026-07-17 · **Cycle:** 03 · **Scope:** Demo-only spec (not build AC)  
**Source authority:** `cycle-02-outputs/PORTAL-SETTINGS-CONTROL-PLANE.md` (full triage, verified against Rails)  
**Demo surface:** "Portal & Access" view in `design-system/app/sales-portal-internal-demo.html`

---

## 1. Why This Hub Exists (the problem in one line)

134 toggles · 6 layers · 39 YAML flags · zero admin surface → **every non-trivial portal change requires a SuperCat ticket** and access rules hide in deploy config. A client org-admin cannot answer "why can't my rep see the portal?" without calling support.

**Bet E target:** One hub where org-admins self-serve ~18 of ~30 portal-relevant settings. SuperCat keeps only access/revenue/security levers. YAML holds only sunset-dated experiments.

---

## 2. Hub IA — 6 Sections

| # | Section | Tagline | Who can edit | Wave |
|---|---|---|---|---|
| 1 | **Enablement** | "Turn the portal on / understand why it's off" | Client admin | Wave 2 |
| 2 | **Territory & data access** | "Which customers does each rep see?" | SuperCat superadmin (match mode) · Client admin (synching/totals) | Wave 2–4 |
| 3 | **Portal display** | "Rep-facing UX options you can change without a ticket" | Client self-service | Wave 3 |
| 4 | **Reports & export** | "What reps can download" | Client admin | Wave 2–3 |
| 5 | **Revenue definitions** 🔒 | "How "sales" is calculated — SuperCat + INSIGHT only" | SuperCat + INSIGHT sign-off | Wave 5 |
| 6 | **Experiments** | "Canary flags with owners and sunset dates" | SuperCat superadmin | Wave 1 |

---

## 3. Section Details (demo-faithful)

### Section 1 — Enablement

**Problem it solves:** Org-admin calls support because reps can't see the portal. The decision tree diagnoses the cause in < 60 seconds.

**Settings landing here:**
| Setting | Label | Type | Current value (sarreid demo) |
|---|---|---|---|
| `mobile_sites.enable_sales_portal` | Portal enabled (this site) | Toggle | ✅ ON |
| `user_types.enable_sales_portal` | User types with portal access | Matrix (user-type × toggle) | 11 types ON, 6 OFF |
| `user_types.enable_portal_dashboard` | Dashboard visible | Matrix | 11 types ON, 6 OFF, 3 default (false) |
| `org flags.enable_portal_dashboard` | Dashboard org gate | Toggle | ✅ ON (sarreid) |
| `Feature :portal_portal` | User-level force-on override | SuperCat-gated inline | 9 users on sarreid |

**In-product decision tree (copy for demo):**
```
Why can't a rep see the portal?

Step 1: Is the portal ON for this site?
  enable_sales_portal = [ON ✓ / OFF → FIX HERE]

Step 2: Are orders/invoices imported?
  portal_orders: 45,494 rows ✓
  portal_invoices: 43,715 rows ✓
  If zero → import order_data.csv / invoice_data.csv

Step 3: Is the user in pricing-preview mode?
  [Transient — sign out of preview session]

Step 4: Does this rep's user-type allow the portal?
  User type "Rep" → enable_sales_portal = [ON / OFF → FIX HERE]

Step 5: Does this rep's user-type allow the DASHBOARD?
  User type "Rep" → enable_portal_dashboard = [ON / OFF → FIX HERE]
  (Default is OFF — must be explicitly enabled)
```

**Demo talking point:** *"Today, answering step 4 or 5 requires a SuperCat ticket. This section answers it in one screen."*

---

### Section 2 — Territory & Data Access

**Problem it solves:** SERV-2196 (multi-territory bill-to over-grant) and SERV-2178 (rep-number territory match) both live here. A rep sees customers they shouldn't — or misses customers they should — because of three overlapping access rules that have no admin surface today.

**Settings landing here:**
| Setting | Label | Type | sarreid value | Risk |
|---|---|---|---|---|
| `user_types.customer_synching` | Customer visibility | Enum (All / Associated / None) | Mix: 11 All, 6 None, etc | **High** |
| `user_types.access_all_customer_sales_totals` | See all customers' totals? | Toggle per user-type | — | **High** |
| `territory_access_via_rep_number` | Territory match mode | Radio: territory_codes / rep_number | territory_codes (default) | **Critical** — SERV-2178 root |
| `user.territory_codes` (read-only) | Rep's territory list | Read-only list | 100 territories | — |

**Demo talking point (SERV-2196 context):**
> *"Sarreid has 99.8% multi-territory bill-to addresses — almost every customer has orders across more than one territory. Until the filter-truth fix ships (Bet A), any demo of territory-scoped views here will surface the over-grant live. In the hub, the 'Territory match mode' setting is where the SERV-2178 fix graduates from deploy config to a labeled admin control."*

**Wave note:** `territory_access_via_rep_number` graduation is **cross-lane** — ships alongside the SERV-2178 Lane-0 fix, not before.

---

### Section 3 — Portal Display

**Problem it solves:** Clients constantly ticket simple display preferences (currency format, showing qty columns, enabling the customer graph). These are safe to self-serve.

**Settings landing here:**
| Setting | Label | Type | sarreid value | Wave |
|---|---|---|---|---|
| `sales_portal_currency_code` | Currency | Select | USD | Wave 3 |
| `display_quantity_available` | Show "Qty Available" column | Toggle | — | Wave 3 |
| `display_quantity_backordered` | Show "Qty Backordered" column | Toggle | — | Wave 3 |
| `eol_customer_graph` | Show sales graph on customer detail | Toggle | true (sarreid) | Wave 3 |
| `link_to_customer_dashboard` | Show customer dashboard link | Toggle | true (sarreid) | Wave 3 |
| Backlog vs invoiced label | Dashboard total label | Select: Backlog / Invoiced | Backlog | Wave 3 |

**Demo talking point:** *"Six settings that are tickets today. Zero metric impact. Wave 3 converts all of them to self-service."*

---

### Section 4 — Reports & Export

**Problem it solves:** Three overlapping export toggles (`xlsx_export`, `can_export_eol_data`, `enable_disable_portal_export_by_user_group`) create conflicting behavior. Unify into one export permission per user-group.

**Settings landing here:**
| Setting | Label | Type | Wave |
|---|---|---|---|
| `advanced_reports` | Advanced reports section | Toggle | Wave 2 |
| Unified export permission | Export (per user-group) | User-group matrix toggle | Wave 3 |
| `view_sales_reports` permission | Admin sales reports | Permission toggle | Wave 2 |

**Demo talking point:** *"Today 'can this rep export?' depends on three different settings in three different places. This section collapses it to one answer per user group."*

---

### Section 5 — Revenue Definitions 🔒

**Problem it solves:** Clients could silently change what "sales" means and break reconciliation with the invoiced-net spine. These settings are **visible** (transparency) but **locked** (SuperCat + INSIGHT sign-off required to change).

**Settings in this section (visible-locked, not editable by client):**
| Setting | Label | Current value | Why locked |
|---|---|---|---|
| `excluded_portal_order_backlog_order_statuses` | Order statuses excluded from backlog | **sarreid: `[]` (none excluded)**; cci: `["C","Q","X","Z"]` | Changes what "backlog" means |
| `portal_data_type` | Orders/invoices correlation mode | null (default: OVERLAPS) | Changes dashboard math |
| `portal_calculations` | Calc engine version | null (default: modern) | Metric law |
| `sales_portal_sales_facts_filter_configuration` | Sales facts filter | — | Defines the fact set |
| `backlog_instead_of_amount_invoiced` | Dashboard shows backlog instead of invoiced | false (sarreid) | Changes headline number meaning |
| `max_portal_data_age_months` | Data history cap | "" (none) | Affects all totals windows |

**Demo talking point (sarreid vs cci comparison):**
> *"Look at this difference: sarreid's 'Backlog Total' includes EVERY order — completed, cancelled, everything — because excluded_portal_order_backlog_order_statuses is empty. CCI properly excludes C, Q, X, Z so only open orders count. A client can't change this themselves because it would silently change what their 'backlog' number means. The fix has to go through SuperCat + INSIGHT review."*

**Locked indicator design:** Settings shown with a 🔒 badge and copy: *"This setting is managed by SuperCat + INSIGHT. Changes require a support request to ensure metric reconciliation."*

---

### Section 6 — Experiments

**Problem it solves:** Today, experimental flags live in `enabled_features.rb` as open-ended allowlists with no UI, no owner, no sunset date. Experiments gives them a labeled home with accountability.

**Each row must show:** Flag name · Human label · Owner (ticket link) · Sunset date · Current state

**Demo entries (sarreid context):**
| Flag | Label | State on sarreid | Demo note |
|---|---|---|---|
| `eol_dashboard_filters` | Dashboard filters | cci + sarreid allowlisted — but **ZERO call sites** | "This flag does nothing — it's dead. Wave 0 deletes it." |
| `tcgc_name_fields` | TCGC name fields | sarreid allowlisted — **ZERO call sites** | "Dead — delete." |
| `netsuite_rest_api` | NetSuite REST API | shl only | "Active canary — stays gated. Owner: integrations." |
| `avery_5392_landscape` | Avery 5392 landscape label | No org allowlisted (wired, dormant) | "Ship-or-cut decision." |

**Wave note:** Wave 0 is the safe down-payment — delete the 5 dead flag entries from `enabled_features.rb`. No org notices; zero call sites confirmed in Rails.

---

## 4. Client Self-Service vs Locked Matrix

| Capability | Client self-service? | Notes |
|---|---|---|
| Turn portal on/off per site | ✅ | Enablement section, Wave 2 |
| Gate dashboard per user-type | ✅ | Enablement section, Wave 2 |
| Set customer visibility mode | ✅ (synching/totals) | Territory section; match-mode stays SuperCat |
| Currency display | ✅ | Display section |
| Qty columns, customer graph | ✅ | Display section |
| Export per user-group | ✅ | Reports section |
| Advanced reports on/off | ✅ | Reports section |
| Backlog status exclusions | ❌ LOCKED | Revenue definitions — SuperCat + INSIGHT |
| Portal data type / calc engine | ❌ LOCKED | Revenue definitions |
| Territory match mode | ❌ SuperCat superadmin only | Access-sensitive; cross-lane with SERV-2178 |
| Force-portal for individual user | ❌ SuperCat superadmin only | Override semantics |
| Experiments / canary flags | ❌ SuperCat superadmin only | Must have ticket + sunset |

---

## 5. Wave 0–1 as "Future" Badges in Demo

Sections that are **not yet built** carry a `FUTURE` / `WAVE N` badge in the demo mockup:
- All 6 sections: `WAVE 2–5` badge on section header (Experiments is Wave 1)
- Individual settings flagged where they're Wave 0–1 vs Wave 2+
- Copy at top of section: *"Not yet built — this is what it will look like when Bet E ships."*

This keeps demo honest — Kylor can show the hub and say *"this is where Bet E goes, here's what the settings will control"* without implying it's in Rails today.

---

## 6. Demo Flow for "Portal & Access" View

1. **Land on Enablement** → click the "Why can't this rep see the portal?" link → walk the decision tree (static mock, not interactive)
2. **Territory & data access** → show sarreid has 99.8% multi-territory exposure → "this is why we're fixing Bet A first"
3. **Revenue definitions** → show sarreid vs cci backlog-statuses difference → "this is metric law — can't be self-serve"
4. **Experiments** → show `eol_dashboard_filters` dead flag → "Wave 0 cleans this up; it's free and safe"

**Total time:** ~8 minutes of the 30-minute walk.

---

*Settings hub demo spec 2026-07-17. Source authority: PORTAL-SETTINGS-CONTROL-PLANE.md (cycle-02). **Build AC (not this file):** SETTINGS-hub-v1-AC.md · Ship gate: SHIP-READINESS-bet-e.md · Plan: TECHNICAL-PLAN.md §8 · Gap tracker: SPEC-GAP-CHECKLIST.md.*
