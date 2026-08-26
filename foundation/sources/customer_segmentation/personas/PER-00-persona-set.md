---
id: PER-00
title: The persona set — who is kept, who is dropped, and why
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
axis: persona (independent of Account Segment and Prospect Archetype)
source_lineage:
  - PM/sales-portal-agent-starters/cycle-03-outputs/PERSONA-ONE-PAGERS.md
  - PM/sales-portal-agent-starters/cycle-04-outputs/PERSONA-EVIDENCE.md
  - PM/Sales Portal Docs/00-SALES-PORTAL-SYSTEM-SPEC.md §3–4, §7, §11
  - foundation/PLATFORM_ANATOMY_CURRENT_STATE.md §1, §B
  - Postgres (read-only), 2026-08-25
depends_on: [TAX-A]
---

# The persona set

**Persona is a separate axis from Account Segment and from Prospect Archetype.** A persona is a
behavioural role with jobs; a segment is a property of the client organisation. They cross-tabulate
and neither predicts the other.

---

## 1. Measured user populations — the basis for keep/drop

`[MEASURED]` Postgres, 2026-08-25, across 253 orgs with users:

| Population | Records | Active 90d | Where |
|---|---:|---:|---|
| **Buyers** (`customer_number` present) | **87,927** | **17,532** on portal orgs · 21,260 eOL overall | eCat Online |
| **Reps / internal non-admin** | 23,424 | **4,058 iPad-active** across 146 orgs | eCat iPad |
| **Internal admins** (`is_admin`) | 2,365 | 377 iPad · **141 eOL** | Admin Console |
| Users active on **both** iPad and eOL | — | **593** | — |

**Two findings shape everything below.**

**(a) Reps and buyers are near-disjoint populations.** Only 593 users are active on both surfaces.
They do not share a screen, a session, or a mental model. `PERSONA-EVIDENCE.md` reached the same
conclusion from the code side — `should_show_customers_tab` requires `customer_number.blank?`, so a
buyer **cannot** reach the rep views by any configuration — and recommended dropping the persona
switcher. Confirmed.

**(b) The rep population is an order of magnitude smaller than the buyer population.** 4,058 active
reps vs 17,532 active buyers. Earlier figures citing ~15,987 "reps" counted *enabled eOL records on
portal orgs*, which overstates it — the real rep surface is the iPad.

---

## 2. Personas kept

| ID | Persona | Basis | Population |
|---|---|---|---|
| **PER-01** | **Independent sales rep** | The iPad is the install-base centre of gravity `[OBSERVED: PLATFORM_ANATOMY §1.3]`; Sales Portal spec §3 lists reps first among portal users | 4,058 iPad-active |
| **PER-02** | **Rep agency principal** | `user_types.primary_rep_group` exists on **142 of 1,980 user types, used by 39 orgs, 3,821 users, 617 iPad-active**. Internal users carry **11,873 distinct `company_name` values** — agencies, not the manufacturer `[MEASURED]` | 617 iPad-active in flagged rep groups |
| **PER-03** | **VP Sales / sales ops** | The Owner/VP seat in `PERSONA-ONE-PAGERS.md` Persona 2 + the ops half of Persona 3. **Manager folds here**, per the prior work's own precedent — a manager is an oversight-scoped viewer, a permission tier, not a new context | 2,365 admin records |
| **PER-04** | **Customer service / order entry** | Sales Portal spec §3 names them explicitly: *"customer-service representatives researching customer, order, and invoice history"* `[OBSERVED]` | Within the 2,365 admin records; not separately keyed |
| **PER-05** | **Product / merchandising** | Admin Console cluster 1 is *"Catalog & taxonomy ops"* `[OBSERVED: PLATFORM_ANATOMY §B]`. Catalog structure is the product they maintain — median 2,344–4,498 products and 30–381 collections per org `[MEASURED]` | Not separately keyed — **weakest-evidenced persona kept** |
| **PER-06** | **Owner / exec** | Kept, but **narrowly**. `PERSONA-ONE-PAGERS.md` locks the scope split: the portal seat is Owner/VP consuming a thin subset; *"the deep CEO factory is Insightful, not the portal"* | Small; overlaps PER-03 |
| **PER-08** | **Dealer buyer** ⚠️ *our-customer's-customer* | 87,927 enabled / 17,532 active — **7.7:1 over reps on active logins**. The largest population on any SuperCat surface | 17,532 active |

## 3. Personas dropped or folded

| Candidate | Verdict | Why |
|---|---|---|
| **IT / integrations** (PER-07, not issued) | **Dropped as an analytics persona** | They consume **job status and error logs, not analytics**. The integration rail is *"a spine rail, not a user-facing app"* `[OBSERVED: PLATFORM_ANATOMY §1.8]`. Its one analytics-shaped job — import health — is owned by whoever fields the consequence, which is PER-03 sales ops (see JTBD-034). Retained as a **stakeholder**, not a persona with jobs. Revisit if a customer names an IT user who needs a metric |
| **Manager** | **Folded into PER-03** | Prior work already adjudicated this: *"a manager is an owner-style viewer of the whole team who is scoped to several books... a permission tier, not a new bounded context."* Multi-territory manager is the EBR-180 XL shelf, out of frame. No reason to re-open |
| **Buyer sub-types** (dealer vs designer vs contract) | **Folded into PER-08** | The user-type names show the split is real — `Customer - Designer` (2,451), `eOL - Dealers/Designers` (2,117), `Customers- Wholesale` (7,820) — but they differ in *pricing entitlement*, not in the jobs they do on the surface. Splitting would triple the persona count without changing a single job |
| **SuperCat-internal CS / superadmin** | **Out of frame** | Real users, but they are *our* staff. This register is about our clients' users. The permission tier is already captured in `PERSONA-ONE-PAGERS.md` Persona 3 |

---

## 4. Two constraints that bind every JTBD below

**(a) There is no incumbent rep analytics surface.** The Sales Portal Territory Dashboard requires
`:portal_portal`, **enabled for zero organisations** — only 9 internal SuperCat usernames. Reports
requires `:advanced_reports`, **6 orgs** `[OBSERVED: PERSONA-EVIDENCE.md]`. Anything rep-facing and
analytics-shaped is being built where nothing currently ships.

**(b) The anatomy and the spec disagree about who the Sales Portal is for — unresolved.**
`PLATFORM_ANATOMY §1.6` says *"Sales Portal is where sales leadership and CS live."*
`00-SALES-PORTAL-SYSTEM-SPEC.md §3` lists *"sales representatives reviewing their customer/territory
book"* **first**. **Not resolved here.** Flagged at each JTBD where it changes the answer — see
JTBD-011, JTBD-021, JTBD-031. It bites hardest on default-home and gating decisions.

---

## 5. Segment variation — the default is "does not differ"

Layer A is stamped judgment reproducing at 38.5% against a 34.9% baseline. Building a
segment-conditional variant of every job would encode a distinction the data cannot carry.

**Default answer for every JTBD: DOES NOT DIFFER BY SEGMENT.** Variation is claimed only where it
can be pointed at a measured structural difference:

| Structural fact `[MEASURED]` | Where it legitimately changes a job |
|---|---|
| Price codes: SEG-01 med 4 · SEG-02 med 4 · SEG-03 med 2 · SEG-04 med 1 | Pricing-visibility jobs |
| Order count: SEG-03 med 210 · SEG-04 med 5,759 | Jobs whose cadence depends on transaction volume |
| Customer count: SEG-01 med 4,418 · SEG-03 med 1,544 | Book-size jobs |
| Territory count: SEG-02 med 41 (highest) | Territory-coverage jobs |

**Result: 4 of 31 jobs vary by segment.** The other 27 do not — **one surface serves everyone**,
which is the simpler and cheaper build. That is a finding, not an omission.

---

## 6. Index

| ID | Persona | Jobs | File |
|---|---|---:|---|
| PER-01 | Independent sales rep | 5 | [`PER-01-independent-sales-rep.md`](PER-01-independent-sales-rep.md) |
| PER-02 | Rep agency principal | 4 | [`PER-02-rep-agency-principal.md`](PER-02-rep-agency-principal.md) |
| PER-03 | VP Sales / sales ops | 5 | [`PER-03-vp-sales-sales-ops.md`](PER-03-vp-sales-sales-ops.md) |
| PER-04 | Customer service / order entry | 4 | [`PER-04-customer-service-order-entry.md`](PER-04-customer-service-order-entry.md) |
| PER-05 | Product / merchandising | 4 | [`PER-05-product-merchandising.md`](PER-05-product-merchandising.md) |
| PER-06 | Owner / exec | 3 | [`PER-06-owner-exec.md`](PER-06-owner-exec.md) |
| PER-08 | Dealer buyer ⚠️ | 6 | [`PER-08-dealer-buyer.md`](PER-08-dealer-buyer.md) |

Flat table of all 31 jobs: [`../analytics/jtbd-register.md`](../analytics/jtbd-register.md).
