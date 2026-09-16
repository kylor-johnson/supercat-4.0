# Client Profile — Shadow Catchers (`sca`)

> **What this is.** Reading-contract input #2 (see [`../CANON.md`](../CANON.md)): the cached, human-ratified
> statement of Shadow Catchers' **stable context**. Loaded after `foundation/provenance_spine.md`, before
> `knowledge/industry_context.md`. **Facts and scope decisions only — no findings, no framing.** See
> [`README.md`](README.md) for the allowed/forbidden rule and the derive→ratify→cache workflow.
>
> **Status:** RATIFIED 2026-06-30 — verified via live Postgres probe of `subscriptions` / `subscription_plans`
> and lifetime-zero counts on the ERP-truth axis (`portal_invoices` / `portal_orders` / `sales_data` all = 0
> rows ever since org creation 2015-05-05). Shadow Catchers is **structurally eCat-only by design**, not a
> connector gap: subscription plan = `eCat iPad` (the iPad-rep-only tier; does NOT include the Sales Portal /
> Intelligence tier that ships an ERP integration); pricing-migration tier T1 Catalog Essentials. A `sca.md`
> will **never** drive a client-facing Mode-1 body via this report operator; sca permanently routes through
> `rep_copilot_operator.md` Tier-0 behavior-only. See Ratification log.

---

## 1. Identity (the hard key — prevents running the wrong org)

| Field | Value | How derived |
|---|---|---|
| Client name | Shadow Catchers | confirmed via `organizations.name` |
| `organization_id` (Postgres) | `90` | Step-1 preflight |
| Shortname | `sca` | confirmed via `organizations.shortname` |
| Same-name disambiguation | none flagged in cohort | preflight |
| `report_through_date` policy | `LEAST(MAX(invoice_date), CURRENT_DATE)` | gate-computed — **NULL** (no invoice ever exists to anchor on) |
| Rep-identity tier | **Tier 0** (no `portal_invoices.rep_number` — there is no invoice feed at all) | RP-2 gate (`../operators/rep_copilot_operator.md` §1) |

## 2. Business model / segment

- **Model:** lighting / home-décor wholesaler (display, mirror, and shade lines per the product catalog
  surfaced in eCat orders — confirm with the owner before ratification).
- **Client segment (SuperCat v4.0, stamped):** Mid-Market Multi-Channel
- **How they sell (axis):** Multi-Channel
- **What they sell (axis):** Decor/Art
- **Who they sell to (axis):** Wholesale (Dealers/Retailers)
- **Price (continuous, not a boundary):** best available unit price ≈ $260 (from Client Segmentation v4.0 MASTER; price is a correlate within segment, not the classifier)
- **Source:** `Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` · stamped 2026-07-09 · join org=sca · org_id=90 (verified)
- _Client segment above = SuperCat's stamped **selling-motion** class (Workstream A), stamped from catalog/order-behavior data (this org has no ERP invoice feed — see §3/§7). It is distinct from the 🧊 FROZEN in-client customer segmentation (Q-SEG-DERIVE, Spine §8), which stays out of scope and is not a profile field._

## 3. Channel model (how they sell)

- The ERP-truth axis is **empty** for this org — `portal_invoices`, `portal_orders`, and `sales_data` carry
  **zero rows ever** (lifetime, not just LTM). Whatever Shadow Catchers' true sales channel mix is, none
  of it reaches us through the ERP rails the report operator measures against.
- The **only signal currently visible** is the iPad eCat surface — orders written by a small set of
  in-house users, against a customer list curated on-device. eCat is therefore the **only** measurable
  channel, but it cannot be sized as a share of total business because the denominator (invoiced revenue)
  does not exist in this data feed.
- _Scope decision: until a real ERP feed arrives, sca runs on the Rep Copilot operator's Tier-0
  behavior-only branch — never on this report operator._

## 4. House / sample / marketplace accounts to screen

- **`SHADOW CATCHERS, INC.` (bill-to code `SHA-1000`)** is the org's own bill-to in the eCat customer list —
  treat as a **house / showroom / sample pattern** when any future leakage / dispersion logic runs.
  Currently captures roughly **$17K LTM** as the 5th-largest "customer" by eCat GMV (pure house pattern;
  not screened by canon's invoice-only `house_suspect` regex because it runs on the customer-side
  bill-to, and the canonical invoice-side regex set never sees this row in the absence of `portal_invoices`).
- **`customer_num IS NULL`** is the **single largest "customer" bucket in the eCat data** (187 confirmed
  orders / $478K LTM = 53.8% of org-wide eCat GMV, of which ~$420K is written by the dominant in-house
  user — see §6). These are eCat orders without a customer linkage at write-time. Treat as a **data-hygiene
  issue, not a customer**, in any future analysis; do not let it anchor a top-customer list.
- Standard house/sample bill-to patterns (`ZZ*`, `HOUSE*`, `ACCOM*`, `SAMPLE*`, `DISPLAY*`, `SHOWROOM*`,
  `TEST*`, `MODEL*`, `PHOTO*`) apply once an invoice feed arrives.
- _Scope decision: these will set which rows the leakage / dispersion math runs on **once an invoice feed
  exists**; today there are no priced invoice lines to disperse against._

## 5. Buyer-type context

- The eCat customer list contains a mix of **independent furniture / design dealers** (Traditions ; Sharon
  Garfield, Rusticks, Meg Brown Home Furnishings, The Shops at Carolina Furn., Sprintz Furniture Showroom,
  Pamella & Rose, Kay Fuller Int) and a few **single-buyer / project accounts** (Bay Design Store,
  Verdalee, The Quite Moose). 80 distinct `customer_num` values appear in the LTM eCat feed.
- Without an invoice feed there is no way to validate "designer / project / trade" buyer mix; **owner must
  confirm the buyer-type read at ratification.**

## 6. Structural concentration (context, NOT a finding)

- **One in-house user (`org_user_id = 7435`) writes the dominant share of eCat orders** — 241 of 299 LTM
  confirmed orders (80.6%), $787K of $890K LTM eCat GMV (**88.5%**), across 73 of the 80 distinct
  `customer_num` values. The remaining 8 active users sum to 11.5%; 4 of those wrote a single confirmed
  order each in the LTM window.
- This is the **operator §5b.3 user-grain concentration pattern** — a single-user-dependent eCat capture,
  surfaced as **structural concentration**, never as a coachable performance finding. The PASS2 →
  PASS3 drift across one day was 88.7% → 88.5% (three new orders against the LTM base); the pattern is
  stable across runs.
- Login activity (a separate behavior signal) is **broader than order authorship**: 27 distinct users have
  logged into the iPad in the LTM window across 1,228 login events, with the most recent login today
  (`days_since_last_login = 0`). The "one user writes the orders" pattern coexists with "27 users use the
  app" — that's the structural shape to surface in a behavior-only run, not the order-authorship gap
  framed as a coaching problem.

## 7. Report mode default + scope exclusions

- **Default mode:** **Mode 2 — Activation (behavior-only)**, **permanent lock** (NOT an "until feed
  arrives" hold) — `COMMERCE_CONFIDENCE = NONE` on the truth axis (no `portal_invoices`, no `portal_orders`,
  no `sales_data`, never populated since org creation 2015-05-05; verified 2026-06-30). Sca's subscription
  plan is `eCat iPad`, which does not provision an ERP integration; pricing-migration tier T1 Catalog
  Essentials. The gate resolves mode live each run but **cannot ever return Mode 1** on this org's current
  product configuration. Per the patched report operator §5b.1, this org **must redirect to
  `rep_copilot_operator.md`** Tier-0 branch — the report operator does not run a body on sca. **Re-ratify
  only** if Shadow Catchers upgrades to a tier that ships an ERP integration AND `portal_invoices` begins
  to populate.
- **Confirmed hard-gap suppressions** for this org (all of these are gated by the missing invoice feed;
  surface as "with connected data" only):
  - **Total / invoiced business** — no invoice feed; no denominator exists.
  - **Booked-orders companion** — no `portal_orders` feed; no order-grain ERP signal exists either.
  - **Rep → revenue at any grain** — `REP_IDENTITY_TIER = 0` because no `rep_number` exists on the
    (non-existent) invoice feed.
  - **Gross / true margin, AR / DSO / collections, returns, stock-outs, carrier / damage, inventory aging,
    market-ROI, segmentation** — all gated by the missing invoice feed plus the canon hard gaps
    (`provenance_spine.md` §6.9).
  - **Channel decomposition** — `Q-CHAN-00` returns `NONE` because `portal_orders` is empty; `eCat` is
    the only visible channel and renders only in absolute dollars from `orders` truth.

## 8. Sensitive callouts — per-client scrubbing policy *(gold-stamp 2026-06-30)*

**Automatic top-1-share rule — N/A for this org as currently constituted.** The auto-rule computes top-1
share of LTM invoiced revenue (`Q-ECON-CONC`); with `inv_ltm_net = 0`, the denominator is undefined and the
rule does not fire. The closest analogue in the available data is **user-grain capture concentration** at
88.5% (§6 above), which is treated as a **structural finding per operator §5b.3**, not a sensitive callout
under §8.

**Per-account overrides:** none set.

**Ratified resolutions (2026-06-30, verified via live Postgres probe):**

1. **eCat-only by design — RATIFIED.** Verified via three independent signals: (a) `subscriptions` row
   for org 90 shows `subscription_plan_id` → `subscription_plans.name = 'eCat iPad'` (active since
   2025-08-26, monthly billing); (b) `portal_invoices` / `portal_orders` / `sales_data` carry **zero rows
   ever** for organization_id = 90 (lifetime, not just LTM); (c) the 2026-05-26 pricing-migration brief
   classifies sca as **Tier T1 Catalog Essentials** ("the rep iPad app and your buyer-facing catalog… 10
   users included and standard support"), a product tier that does not ship the ERP integration that would
   populate `portal_invoices`. Sca has been on the platform 11 years (since 2015-05-05) and has accumulated
   3,065 eCat orders / 2,782 curated customers / 5,114 products on the eCat surface without ever populating
   the ERP-truth axis. This is not a feed bug; it is the product they buy.
2. **`org_user_id = 7435` = Unknown.** The 88.5% user-grain concentration pattern is surfaced as a
   **structural** finding per operator §5b.3, not as a coachable problem; downstream framing reads the
   pattern as expected (owner / admin) by default unless the rep-copilot operator inspects the user record
   to identify them. Re-ratify with the owner-vs-rep-vs-admin call only if the Tier-0 behavior-only branch
   begins to render a sentence whose meaning hinges on that distinction.
3. **`SHADOW CATCHERS, INC.` (`SHA-1000`) — house pattern confirmed.** Name match is unambiguous; treat as
   the org's own bill-to / sample pattern in any future leakage / dispersion math. No invoice feed exists
   today against which to apply the screen.
4. **`customer_num IS NULL` bucket = data-hygiene flag, not a customer.** 187 orders / $478K / 53.8% of
   org-wide eCat GMV — recorded as an investigation item for the rep-copilot operator (whether write-time
   data-entry gap, quoting pattern, or intentional); never anchored as a top-customer finding.

**Cascade rule** (orphaned-hero-hedge fix): not applicable in Mode 2 (no §1 / §5 / §10 customer-facing
copy renders in the gate-STOP artifact).

_Forbidden here: any judgment about whether the user-concentration pattern or the SHADOW CATCHERS / NULL
bucket is good or bad for the client. The policy is a scope decision (which rows the math runs on once a
feed arrives), not a finding (whether the pattern is a problem)._

---

### Ratification log
- 2026-06-30 — Inline-DRAFT derived during PASS3 `--cohort-validation` cold re-run against the 2026-06-30
  cohort patch + gold-stamp absorption. Identity / mode / hard-gap suppressions / user-grain concentration /
  house-pattern data points captured from Step-1 preflight + Step-2 gather. — Kylor (via agent)
- 2026-06-30 (PM) — **RATIFIED.** Four §8 open questions resolved (see "Ratified resolutions" above): the
  load-bearing strategic question — eCat-only vs connector-gap — resolved as **structurally eCat-only by
  design** on three independent live-data signals (subscription plan = `eCat iPad`; lifetime-zero on
  `portal_invoices` / `portal_orders` / `sales_data` for org 90 since 2015; pricing-migration tier T1
  Catalog Essentials per `Pricing Migration/format-b-notices/sca__shadow-catchers__brief.md` 2026-05-26).
  Mode-2 permanent lock added to §7 (not "until feed arrives"). user_7435 / SHA-1000 / NULL-bucket
  resolutions noted at the level of detail this profile's product surface (Tier-0 behavior-only rep-copilot
  branch) actually needs. §1–§7 sanity-checked against the sca PASS3 Gate-STOP output and accepted as
  live-derived facts. Renamed `sca.draft.md` → `sca.md`. Standing leakage gut-check held vacuously: no
  invoice feed exists against which a leakage finding could be authored. — Kylor

