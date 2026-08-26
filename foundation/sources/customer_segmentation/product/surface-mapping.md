---
id: PROD-MAP
title: Surface mapping — all 31 jobs to a surface
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
depends_on: [JTBD-REG, PER-00]
---

# Surface mapping

**Carried forward as established, applied to every row:**

1. **Sales Portal is the analytics surface. eOL Catalog/Cart is the buying surface.**
2. **There is no incumbent rep analytics surface.** Territory Dashboard requires `:portal_portal`,
   enabled for **zero organisations** — 9 internal SuperCat usernames only. Reports requires
   `:advanced_reports`, **6 orgs** `[OBSERVED: PERSONA-EVIDENCE.md]`. Anything rep-facing and
   analytics-shaped is greenfield, not a redesign.
3. **Build once, parameterise on org structure** — price-code count, territory count, product count.
   **No segment-conditional variants.** Only 4 of 31 jobs vary, and they vary on structure an org
   can read off its own data, not on selling motion.

Surfaces: **Portal** (Sales Portal) · **eOL** (Catalog/Cart/Closed Site) · **iPad-EC** (new
web-based component embedded in the offline iPad app) · **Admin** (Admin Console) · **Insightful**.

---

## 1. The mapping table

Build size: **S** ≤2 weeks · **M** 2–6 weeks · **L** >6 weeks or needs a new data structure.
Offline risk applies to iPad-EC rows only.

| JTBD | Persona | Surface | Data dependencies | Fields that don't exist | Size | Offline risk |
|---|---|---|---|---|---|---|
| JTBD-011 | rep | **iPad-EC** ⚠️ | `portal_invoices`, `orders`, customer, territory | — | **L** | **HIGH** |
| JTBD-012 | rep | **Portal + iPad-EC** | territory master, user territories, `access_all_customer_sales_totals` | `RepNumber` as multi-value | **M** (fix, not build) | **MED** |
| JTBD-013 | rep | **iPad** (existing) | local SQLite catalog/customers/pricing/inventory | — | — (protect) | **N/A — is the baseline** |
| JTBD-014 | rep | **iPad-EC** | `portal_invoices`, `orders` by customer by period | **per-account baseline / seasonality** | **M** | **MED** |
| JTBD-015 | rep | **iPad-EC** | `orders`, `portal_invoices` | **ERP ship status** (not ours) | **S** | **MED** |
| JTBD-021 | agency | **Portal** ⚠️ | invoices, multi-territory rollup | **agency entity**, sub-rep→principal | **L** | — |
| JTBD-022 | agency | **Portal** | per-rep attribution | **agency entity**, `REP_IDENTITY_TIER` ≥2 | **L** | — |
| JTBD-023 | agency | **Portal** | multi-year invoices | **agency entity**, customer "opened by" | **L** | — |
| JTBD-024 | agency | **Admin** | user territories, user types, `customer_synching` | **view-as / preview mechanism** | **M** | — |
| JTBD-031 | VP/ops | **Portal** (exists) ⚠️ | `portal_invoices`, `orders`, backlog calc | — | **S** (honesty labelling) | — |
| JTBD-032 | VP/ops | **Portal** | `last_ipad_login_at`, `last_ecat_online_login_at`, orders/user, seats | — | **S** — gate is off, not missing | — |
| JTBD-033 | VP/ops | **Admin** | 134 toggles / 39 flags / 6 layers, `customer_synching` | — (aggregation only) | **M** | — |
| JTBD-034 | VP/ops | **Admin** | import events, ETL delay | **push/alert channel**; failure reason codes | **S** | — |
| JTBD-035 | VP/ops | **Portal** | same query both paths | — | **S** (defect fix) | — |
| JTBD-041 | CS | **Portal** (exists) | `orders`, `portal_invoices`, ship-tos, linkage | — | — (coverage, not build) | — |
| JTBD-042 | CS | **Admin** (exists) | customers, price levels, options, inventory | — | — | — |
| JTBD-043 | CS | **Portal** | `orders`, `portal_invoices`, `NextReceiptDate` | **ERP ship/carrier/tracking** (not ours) | **S** | — |
| JTBD-044 | CS | **Admin** | product state, inventory freshness, import state | **order-failure reason codes** | **M** | — |
| JTBD-051 | product | **Portal** | order/invoice lines by item, taxonomy | **item lifecycle dates**, inventory history | **M** | — |
| JTBD-052 | product | **Portal** | option selections on order lines | **option selection capture** (varies by org) | **L** | — |
| JTBD-053 | product | **Admin** | products, images, prices, taxonomy, image-match results | — (aggregation only) | **S** — cheapest new job | — |
| JTBD-054 | product | **Portal** | order lines by collection, first-order date | **product launch date / "new" flag** | **M** | — |
| JTBD-061 | owner | **Insightful** (exists) ⚠️ | `portal_invoices` | — | — | — |
| JTBD-062 | owner | **Portal** | invoices by customer by period, rep ownership | **per-account baseline** (segment-aware window) | **M** | — |
| JTBD-063 | owner | **Portal** | login timestamps, territory coverage | — | **S** — gate is off | — |
| JTBD-081 | buyer | **eOL Cart** (exists) | history, pricing, inventory, cart | — | — (58 orgs entitled) | — |
| JTBD-082 | buyer | **eOL/Portal** (exists) | `orders`, `portal_invoices`, linkage | — | — **protect, don't regress** | — |
| JTBD-083 | buyer | **eOL** (exists) | `DefaultPriceCode`, price levels, markup | — | — | — |
| JTBD-084 | buyer | **eOL** | `inventory` incl. `NextReceiptDate` | **snapshot age / freshness indicator** | **S** | — |
| JTBD-085 | buyer | **eOL** | catalog, pricing, history | — | **L** (offline buyer session) | **HIGH — see §5.6** |
| JTBD-086 | buyer | **Portal** (buyer half) | invoices by customer, category mapping | — | **S** — config track, see §2 |

⚠️ = anatomy-vs-spec conflict changes the answer. Scoped in §6.

**Totals:** iPad-EC 5 · Portal 14 · Admin 5 · eOL 5 · Insightful 1 · existing-and-fine 6.
By size: **S 12 · M 8 · L 6** (5 rows are protect/coverage, not build).

---

## 2. The buyer-history config track — not a build item, and not mine to rank

`:advanced_reports` currently reaches **6 orgs**; rolling it to all portal orgs reaches
**~13,800 additional active buyers** `[OBSERVED: PERSONA-EVIDENCE.md]`. **This is a configuration
change, not a build**, so it does not belong in the ranking above and is not competing with
JTBD-053 or anything else for engineering time. It is listed separately because its gating question
is commercial rather than technical: **exposing a buyer's own purchase history is our client's
decision about their own customers, not ours.** The risks a client would need to weigh are
pricing-entitlement exposure (a buyer inferring their tier, or comparing across their own
locations) and competitive exposure (history views revealing assortment or volume patterns the
manufacturer would rather not surface). It is therefore **blocked on a client-risk review, not on
job strength** — a small number of orgs already run it (`:link_to_customer_dashboard` in `vic` and
`clm`) and could be asked directly. **Decision left with Kylor.**

---

## 3. First-class finding — there is no incumbent rep analytics surface

Worth stating plainly because it changes the build calculus rather than just the backlog:

**The Sales Portal Territory Dashboard — the surface a rep would use for JTBD-011, 012, 014 — is
enabled for zero organisations.** `:portal_portal` resolves to 9 internal SuperCat usernames.
Reports reaches 6 orgs. The dashboard variant has been stalled since 2022 (EBR-212).

Consequences:

- **Nothing is being displaced.** There is no user habit, no trained expectation, no migration path
  to preserve. Design freedom is unusually high.
- **There is also no usage evidence.** No telemetry, no complaints from a surface nobody has, no
  "reps do X today" baseline. Every design assumption here is untested — which is precisely why
  Phase 5's H1–H4 exist.
- **A shipped-but-disabled surface is not a shipped surface.** Any roadmap claiming rep analytics
  "exists and needs improvement" is wrong. It is greenfield.

---

## 4. PER-02 rep agency principal — not servable today

All four PER-02 jobs are capped by one missing structure. Current state `[MEASURED 2026-08-25]`:
`user_types.primary_rep_group` (a boolean, 142 of 1,980 user types, 39 orgs) and
`org_users.company_name` (**11,873 distinct free-text values**). Neither is an entity.

### What the entity would need to be

| Element | Requirement |
|---|---|
| **`agencies`** table | Stable id, canonical name, per-organisation scope. An agency is a real-world firm; today it is a string typed 11,873 different ways |
| **`org_users.agency_id`** | FK replacing free-text `company_name` as the authoritative link. Requires a **name-normalisation migration** over 11,873 values — the expensive part |
| **Principal flag** | Which user(s) in an agency may see the agency-wide roll-up |
| **Agency → territory mapping** | Many-to-many. Cannot ride on the scalar `RepNumber` — spec §7.5 already says comma-separated rep numbers are *"not reliably represented by the current scalar warehouse model"* |
| **Warehouse rollup** | Agency-level aggregation in the Portal warehouse, respecting fail-closed territory rules |
| **Identity tier** | `REP_IDENTITY_TIER` ≥ 2 before any per-sub-rep attribution; unmapped reps never silently dropped |

**Size: L, and the largest single item in this register.** It overlaps EBR-180 / SERV-2178, which
spec §7.5 already calls *"a separate, large implementation class."* The migration — not the schema —
is the cost: 11,873 free-text values must be resolved to canonical agencies, and no authoritative
external list exists.

### Is PER-02 servable before that exists?

**No.**

JTBD-021, 022 and 023 all require aggregating across sub-reps, which requires knowing who the
sub-reps are. That relationship is not recorded anywhere. There is no partial version: an
"agency view" built on free-text `company_name` would silently merge distinct agencies that typed
their name differently and split single agencies that didn't — producing a number that looks
authoritative and is wrong. Under principle 6 that is a suppress case, not a degrade case.

**The one exception is JTBD-024** (show a sub-rep their scoped view), which needs a preview
mechanism rather than an agency entity, and is **M** — but it is a support job, not the persona's
reason to exist.

**Recommendation: do not commit to PER-02 in this cycle.** Say so explicitly to anyone asking for
agency analytics, rather than shipping an approximation.

---

## 5. Offline constraints — the 5 iPad-embedded components only

Applies to **JTBD-011, 012, 014, 015** (rep analytics) and **JTBD-085** (buyer at market).
Not to the other 26.

**Precedent, noted not re-derived:** the iPad codebase already carries a WebView bridge — **36 call
sites, classed `NATIVE_EQUIVALENT`** `[OBSERVED: PM/ecat-web-rewrite-estimate/01_CODE_CENSUS.md]`.
Embedding a web component is an established pattern here, not a new architecture.

### 5.1 What must be cached locally, and its size

Rep analytics needs a **pre-aggregated per-rep extract**, never the raw tables. Shipping order and
invoice history to the device is not viable — SEG-04 orgs run a median 5,759 orders and SEG-01
orgs a median 4,418 customers `[MEASURED]`.

| Cached object | Grain | Estimated size |
|---|---|---|
| Account summary | one row per customer in the rep's territory: T12M invoiced, prior T12M, open order value, last order date | ~200 bytes × up to ~5,000 accounts ≈ **1 MB** |
| Category mix | customer × category, last 2 periods | ~50 bytes × ~20 categories × 5,000 ≈ **5 MB** |
| Decline flags | precomputed per account (JTBD-014) | negligible |
| Open order status | one row per open order | ~150 bytes × ~1,000 ≈ **0.15 MB** |
| **Total per rep** | | **≈ 6–8 MB typical; budget 15 MB for the SEG-04 / SEG-01 tail** |

Sized against the existing catalog cache this is small. **Parameterise the extract on territory
size and account count — the org's own structure — not on segment.**

### 5.2 Acceptable staleness

| Data | Acceptable | Rationale |
|---|---|---|
| Account summary / invoiced totals | **24 hours** | Warehouse ETL already runs on a delay (spec §5.3); intra-day precision is not a decision input for a pre-appointment brief |
| Open order status | **4 hours** | Changes during a business day and is quoted to a customer |
| Decline flags | **7 days** | A trend signal; daily recomputation is false precision |
| Territory/permission scope | **Must match server on last sync** | Never stale-serve an access decision — fail closed |

### 5.3 What the rep sees when stale

**Always show the data with its age. Never hide it, never silently serve it as current.**

- A persistent, non-modal age line: *"As of Tue 9:14am — 2 days old."*
- Past the acceptable window: the same numbers plus a visible warning state, still usable. A rep in
  a dealer's office with 6-day-old numbers is far better off than a rep with a spinner.
- **Never** an empty state where cached data exists.
- Anything quoted to a customer (open order status) past its window: label it explicitly as
  needing confirmation rather than presenting it as fact.

### 5.4 Zero connectivity on a market floor or dealer back office

This is the **normal** case, not the exception, and the design must assume it:

- All five components read **only** from the local extract. **No component may block on a network
  call.** A rep-facing analytics panel that spins on a market floor is worse than no panel — it
  breaks the one thing (JTBD-013) that already works and is SuperCat's strongest asset.
- No lazy-loaded remote assets — charts, fonts and icons ship with the component.
- Market week is the **worst** connectivity and the **highest** usage simultaneously. Treat it as
  the design case.
- Degradation order when the extract is missing entirely: show the customer record and catalog
  (existing behaviour), and state that the analytics extract has not synced — never a blank screen.

### 5.5 Sync and conflict handling

**These components are read-only, which removes the hard problem.** They display derived analytics;
they do not author data. Therefore:

- **No write conflicts by design.** The rep cannot edit an account summary.
- Sync is a **full replace of the extract**, not a merge — simpler and idempotent.
- Sync piggybacks the existing catalog/customer sync rather than adding a second channel.
- Partial sync failure must leave the **previous complete extract in place**, never a half-updated
  one. A stale-but-consistent view beats a fresh-but-partial one.
- **This is a deliberate scope boundary.** If a later job requires the rep to *write* through one of
  these components (e.g. dismissing a decline flag), conflict handling stops being trivial and must
  be re-specified. Keep them read-only.

### 5.6 Auth when offline

- The component runs inside an authenticated iPad session; it inherits that session and **must not
  present its own login**.
- **Permission scope is baked into the extract at sync time** — the extract contains only the
  accounts the rep is entitled to see. There is no client-side filtering of a wider dataset, so a
  compromised device cannot reveal a wider book.
- Consequence: **a permission change does not take effect until the next sync.** Acceptable for
  widening; **not** acceptable for revocation. Revocation must be enforced server-side at next
  sync, and the product must not claim real-time revocation it cannot deliver.
- **Fail closed:** no valid extract, or a territory set that is empty, → show nothing, never
  whole-org. This is the same rule as JTBD-012 and it is non-negotiable — it is the documented root
  trust failure (EBR-40).

### 5.7 JTBD-085 is a different and harder problem

JTBD-085 (buyer leaves a market appointment with an order) is the one row where the offline
constraint applies to a **buyer's own device in a browser**, not to the rep's iPad. The rep half is
offline-capable; the buyer half is not, and a browser session on a market floor has none of the
iPad's caching. **Sized L and flagged: this is not solvable by the same pattern**, and may not be
solvable at all without a buyer-side app. Do not assume the iPad-EC approach transfers.

---

## 6. The anatomy-vs-spec conflict — scoped, not resolved

`PLATFORM_ANATOMY §1.6`: Sales Portal is *"where sales leadership and CS live."*
`00-SALES-PORTAL-SYSTEM-SPEC.md §3`: its users are *"primarily sales representatives reviewing
their customer/territory book"* — reps listed **first**.

It bites at three jobs. Both readings are internally coherent; they build different things.

| | **Reading A — anatomy** (Portal = leadership + CS) | **Reading B — spec** (Portal = reps first) |
|---|---|---|
| **JTBD-011** know my book | Rep analytics belong on the **iPad**. Build iPad-EC (L). Portal stays leadership-facing | Rep analytics belong in the **Portal**; the gap is that Territory Dashboard was never enabled. Fix + enable (M) |
| **JTBD-021** agency book | Portal grows a third audience (external principals) — a new authorization surface | Natural extension of a rep-facing Portal, same territory machinery |
| **JTBD-031** topline | Portal's primary job. Rep scoping is secondary; simpler permission model | Portal must serve both altitudes; territory scoping becomes first-class (EBR-40 is then a P0, not a defect) |

**Cost of picking wrong:**

- **Wrong on A** (build iPad-EC, reps actually wanted it in the Portal): sunk iPad-EC build, plus a
  Portal that still fails territory scoping. **Recoverable** — the extract and aggregation logic
  are reusable; the wrapper is thrown away. Call it **the smaller loss**.
- **Wrong on B** (invest in Portal territory scoping, reps actually need it offline in the field):
  a correct Portal that reps cannot use where they work — a dealer's back office, a market floor.
  **Less recoverable**, because it fails on the constraint (offline) rather than on the surface, and
  the offline requirement then forces the iPad build anyway. **The larger loss.**

**The asymmetry is the useful part**: getting A wrong costs a wrapper; getting B wrong costs the
wrapper *and* leaves the field case unsolved. That argues for resolving the conflict before
committing to JTBD-011, not after.

**Still not picked.** Two stamped documents disagree and this is a product-owner decision.
**The cheapest way to settle it is Phase 5's walk list** — ask reps at market where they would look.
