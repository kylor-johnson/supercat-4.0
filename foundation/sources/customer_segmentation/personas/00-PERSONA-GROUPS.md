---
id: PERSONA-GROUPS
title: Persona groups — SuperCat personas, then selling-motion job packs
version: 0.3
status: draft
date: 2026-09-15
owner: Kylor Johnson
authority: SuperCat personas are who consumes which product. Selling motion parameterizes jobs on those surfaces. It does not mint eight extra SuperCat personas.
source_lineage:
  - foundation/PLATFORM_ANATOMY_CURRENT_STATE.md
  - Customer Segmentation/v4/v4.0_archive/SuperCat_Segment_Personas_v4.0_STARTER.md
  - Customer Segmentation/current/SuperCat_Client_Segmentation_v4.0.md
  - personas/PER-00-persona-set.md
depends_on: [TAX-A]
supersedes: v0.2 which treated motion × seat cells as the persona set
---

# Persona groups

**You were right.** The SuperCat persona set is who is in front of which product. We over-named the motion cells (PG-01…08) as if they were eight SuperCat users, and we mashed admin / VP / exec into one HQ blob. Anatomy already had the consumption cut; Mixpanel and Postgres confirm it.

Two layers. Do not collapse them.

| Layer | Question | Answer |
|---|---|---|
| **1. SuperCat persona** | Who is logged in, and which product do they actually use? | Admin · VP of sales · Executive · Sales rep · Customer/dealer/buyer |
| **2. Selling-motion job pack** | Given that persona, what job and what grain? | Look the **client** up on the v4.0 roster. Parameterize. Do not mint a new persona name. |

July 7's "personas within segments" was written for **co-pilot / brand_to_customer** — who *our client* sells to (designer vs dealer vs Walmart). That is Layer 2 on the **buyer** persona, and the job-pack on the **rep** persona. It is not eight SuperCat logins.

---

## Layer 1 — SuperCat personas (consumption)

From `PLATFORM_ANATOMY_CURRENT_STATE.md` plus executives on Insightful. Measured seats `[from-live]` Postgres 2026-09-15, excluding `demo`/`demo2`, enabled users, 90-day windows.

| Persona | Surface they consume | Why this is a persona, not a synonym | Headcount (enabled / 90d active on that surface) |
|---|---|---|---|
| **Admin** | **Admin Console** | Imports, users, catalog completeness, login/usage hygiene. Not an analytics dashboard. | `is_admin`: 2,226 enabled; 346 iPad-90d · 139 eOL-90d — they are not living in the catalog |
| **VP of sales / sales ops** | **Sales Portal** | Full customer / order / invoice analytics. Portal is **on for 52 of 102** `mobile_sites`. | Named groups exist (`Sales Managers`, `VP - Group`) but titles are messy; the *surface* is the discriminator |
| **Executive / owner** | **Insightful** (and Portal topline) | One number they can defend. Not catalog ops, not a territory walk-in. | User-type names `Executive` / `Execs` / `Admin and Executives` are small; the job is still distinct |
| **Sales rep** | **eCat iPad** | Selling instrument, offline. Mixpanel is this person. | 3,966 internal iPad-90d. They almost never live in Portal (below) |
| **Customer / dealer / buyer** | **eCat Online** | Our *client's* customer. ⚠️ Jobs only if they pay the manufacturer. | 87,013 enabled · **18,691 eOL-90d**. 62 of them touched iPad. Disjoint. |

**CS / order entry** sits with Portal (anatomy already says "sales leadership and CS"). **Merch** sits with Admin. Do not lose them inside "HQ." They are seats under VP/Admin, not a sixth and seventh SuperCat product.

### What the data actually says about consumption

**Sales reps do not live in Sales Portal.** Mixpanel is the iPad SDK — last 90 days `[from-live]`:

| Event | Distinct users | Events |
|---|---:|---:|
| `product_search` | 1,933 | 404,198 |
| `view_portal` (Portal opened from the iPad WebView) | 650 | 18,386 |

Q-04 on `mixpanel.user_feature_usage_report` (lifetime-in-table, 8,007 users): 2,077 classify as selling reps. Only **18** classify as "analytics/portal user" (`submit_order ≤ 2` and `access_sales_portal > 100`). Portal *events* are mostly attached to people who also sell (124k of ~149k `access_sales_portal` events sit on selling_rep). So: some reps tap Portal; it is not their home; it is not a distinct Mixpanel population of VPs. **Mixpanel cannot see a VP who only uses Portal in a browser.** Do not read Mixpanel as the VP persona.

**Buyers live on eOL catalog, not Portal.** GA `google_analytics_ecat_online.page_path`, last 90 days `[from-live]`:

| Path kind | Page views |
|---|---:|
| `/products` | 689,154 |
| `/login` | 239,857 |
| `/orders` | 60,385 |
| `/invoices` | 32,349 |
| `/portal` tab on eOL | **3,889** |

**Admins are not buyers and not field reps.** 2,226 enabled admins vs 87k buyers vs 3,966 iPad-active internals.

**Reps and buyers barely overlap.** Internal both-surfaces 90d: 561. Buyer iPad-90d: 62.

That is the consumption cut. It is load-bearing. Build surfaces to it.

---

## Layer 2 — selling motion parameterizes the job

Look the org up (109 / 33 / 38 / 24 / 14). Never put a segment on a prospect.

This is where I **push back** on "just the five."

### Do not fold the buyer persona into one eOL bet

The July 7 starter and the buyer-type reads are about *our client's customer*, not a SuperCat login. Michelle Gerson (designer / trade) and Walmart (mass) are both "customers." They will not use eCat Online the same way — Walmart will not log in at all.

eOL expansion targeting (June 29, still right):

| Client motion | Buyer persona's eOL fit |
|---|---|
| Luxury Spec | **Highest** — showrooms / designers will use a portal |
| Premium Trade | **High** — dealer restock |
| Multi-Channel | **Medium** — long tail only; Ferguson / Wayfair never |
| Volume | **Near-zero** — TJX / Walmart / Amazon never. Fringe only, and say so |

User-type names already split this on the seat file: `Customer - Designer`, `Customers- Dealer`, `eOL Customers`, vs chain bill-tos that show up in invoiced data with **0 eCat**. That is Layer 2 on the **same** buyer persona.

### Do not ship one analytics home screen for every sales rep

The *persona* is sales rep. The *device* is iPad. Mixpanel proves the job they actually do today is catalog / customer / order — not Portal.

The *analytics we would add* (iPad-EC) still changes grain by the client's motion. That is a job pack, not four new personas:

| Pack ID | When the client is… | What the rep's analytics job is |
|---|---|---|
| **PG-01** | Luxury Spec | What this account **specified**, 24 months, by collection. Not T90D "gone quiet." |
| **PG-03** | Premium Trade | This dealer's **line vs holes**, under-penetrated accounts |
| **PG-05** | Multi-Channel | The **dealer slice only** — exclude marketplace/EDI from "my book" |
| **PG-07** | Volume | Catalog as reference + fringe. **Default: skip an L panel.** Most volume revenue never touches the iPad. |

Same shell (WebView, extract, staleness, fail-closed). Different grain. Roster lookup, not AOV.

### Un-mash HQ — admin ≠ VP ≠ exec

v0.2 called these "PG-HQ, one group." Wrong as *personas*. Right as "most HQ *jobs* are shared."

| Persona | Home | Shared jobs | Motion-aware jobs |
|---|---|---|---|
| Admin | Admin Console | Catalog completeness, nightly import landed, why can't this user see their book | Load is worse at volume (catalog scale) — same job, paginate |
| VP / sales ops | Sales Portal | Export matches the screen (EBR-91 **first**), team using it, reconstruct an account | "Accounts slipping" **window**: project vs T12M vs replenishment |
| Executive | Insightful | One topline, honesty-labelled | Intro-landing is usually N/A at volume |

Agency principal is still unservable this cycle (no agency entity).

---

## How to use this without rebuilding the flattened model

| Question | Go here |
|---|---|
| Which SuperCat product is this for? | Layer 1 table |
| What should a spec-rep's analytics panel show vs a volume-rep's? | Layer 2 job packs PG-01 vs PG-07 |
| Should we sell eOL to this client? | Layer 2 eOL fit, from the roster |
| Login headcounts / disjoint populations | [`PER-00-persona-set.md`](PER-00-persona-set.md) |
| Jobs and build order | [`../analytics/jtbd-register.md`](../analytics/jtbd-register.md), [`../product/surface-mapping.md`](../product/surface-mapping.md) |

`JOB-*` IDs stay. They are jobs, not personas. `PG-01…08` stay as **job-pack IDs**, not the persona set.

---

## The eight job packs (kept, demoted)

Names from the July 7 starter. Volume's field pack was unnamed there; PG-07 is from the June selling-motion brief.

### SEG-01 · Luxury Specification

**PG-01 — Project specifier (sales-rep pack).** Unit of work is a *project*. Needs specified/invoiced by collection, finish/COM/lead time. Does not need pack/velocity or T90D retail decline.

**PG-02 — Trade showroom / designer (buyer pack).** Highest eOL fit. Spec sheets, finishes, floor stock, specified reorder.

Exemplars: Palecek, Theodore Alexander, Visual Comfort Signature, Currey.

### SEG-02 · Premium Trade Brand

**PG-03 — Brand-rep territory builder (sales-rep pack).** Dealer line vs holes, under-penetrated accounts, territory they can trust.

**PG-04 — Authorized dealer manager (buyer pack).** High eOL fit. Restock the line, tier price, stock.

### SEG-03 · Mid-Market Multi-Channel

**PG-05 — Channel-mix operator (sales-rep pack).** Dealer/contractor slice only. Marketplace/EDI is not "my book."

**PG-06 — Self-service reorder buyer (buyer pack).** Medium eOL — long tail. Entitlement is load-bearing. Not Wayfair.

Exemplars: Savoy House, Craftmade, Kichler, Maxim.

### SEG-04 · Volume Distribution

**PG-07 — Program / fringe-account (sales-rep pack).** Skip an L analytics panel by default.

**PG-08 — Replenishment / assortment (buyer pack).** eOL near-zero for the core. Walmart Retail Link will not be replaced. Confirmed in buyer-type reads (`asi`/Walmart, `bri`/PDI, Ferguson bill-tos with ~0 eCat).

Exemplars: Abaline, Home Essentials, Kennedy International, Bulbrite.

---

## What we are not doing

- **Not re-segmenting.** 109 orgs, 33 / 38 / 24 / 14. Roster lookup.
- **Not putting a segment on a prospect.**
- **Not treating Mixpanel as the VP or admin persona.** Mixpanel is iPad.
- **Not keeping PER-01…08 or PG-01…08 as the SuperCat persona set.** Seats and job packs, respectively.
- **Not going back to "jobs don't differ / build once not on segment"** for field analytics or eOL targeting.

Jobs and surfaces: [`../analytics/jtbd-register.md`](../analytics/jtbd-register.md), [`../product/surface-mapping.md`](../product/surface-mapping.md).
