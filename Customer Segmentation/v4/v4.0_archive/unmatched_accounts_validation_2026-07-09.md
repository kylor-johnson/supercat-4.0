# Validation of the 5 `??` (unmatched) accounts — 2026-07-09

> Post-stamp propagation task (handoff item D). Resolves the 5 accounts the v4.0 build script
> could not join to a Postgres `organizations` row.
>
> **Round 1 finding (superseded — see Round 2 below): 4 of 5 are real, active orgs the build
> script simply failed to match; 1 of 5 (Gabriella White) is an exact duplicate already counted
> elsewhere.** This was believed to change the stamped universe from 109 → 108 and Premium Trade
> Brand from 38 → 37.
>
> **Round 2 finding: Round 1 was wrong about Gabriella White.** It is not a duplicate — it's the
> parent LLC of a 3-entity brand family (Gabriella White / Summer Classics / Summer Classics
> Contract), each separately billed and active in Postgres. The org that Round 1 thought was
> "Summer Classics, already counted" (`sc`) is actually Gabriella White itself; the real Summer
> Classics org (`scw`) had data pulled but was never attached to any roster row. **Net effect:
> the universe is 109 (matching the original stamp exactly), not 108** — see "Round 2" section
> below for the full trace.
>
> **Round 3 finding (independent audit, same day): Round 2's identity claim is correct.** Also
> found and fixed an enrichment hole Round 1/2 left on the five newly-matched orgs
> (`leg`/`soi`/`tel`/`ilc`/`abol`) — shortnames were remapped but PRODUCT/CUSTOMER/ORDER/CAT/IPAD
> dicts had no entries, so those CSV rows were blank. Headline counts unchanged. See Round 3.

## Method (Round 1)
Queried `organizations` directly by company name (`ilike`) instead of the exact-string join the
build script used. All 5 names matched on the first pass.

## Findings (Round 1 — Gabriella White row superseded by Round 2)

| Company (as listed) | Resolution | org | Postgres org id | Live signal |
|---|---|---|---|---|
| **Gabriella White** | ~~Duplicate — remove from roster~~ **SUPERSEDED, see Round 2 below** | `sc` | 69 | ~~This Postgres org's `name` field is literally `"Gabriella White"` (a legacy/DBA name that was never updated), but it is the same org already counted in the roster as "Summer Classics"~~ — **wrong**. `sc`'s `company_website` is `www.GabriellaWhite.com`; it is genuinely Gabriella White, a distinct billing entity from the real Summer Classics (`scw`). Round 1 conflated the two because the v3.2 roster had mismapped "Summer Classics" onto `sc` since its original build. |
| **Legrand US** | **Real org — matched** | `leg` | 273 | 1,012 products loaded, 1 customer, 0 orders yet. Matches TAM's own numbers for this account (near-zero activity, 2026 start) — reads as a **brand-new onboarding**, not a fake account. |
| **Silver One** | **Real org — matched** | `soi` | 230 | 1,106 products loaded, 0 customers, 0 orders. Catalog-loaded but not yet commercially active — pre-launch state. |
| **Tomlinson Companies** | **Real org — matched** | `tel` | 86 | 2,253 products, 287 customers, 14 orders (most recent 2022-03). Real and previously active; order activity looks dormant/thin recently — worth a light activity check but not a data artifact. |
| **Ideal Living** | **Real org — matched** | `ilc` | 234 | 336 products, 0 customers, 0 orders. Catalog-loaded, not yet commercially active. |

## Open flag — do not auto-resolve

There is a **second, separate** Postgres org named `legrand` (lowercase), shortname `lna`, org id 93:
101 products, 14 customers, 3 orders, **last order 2015-07-06**. This looks like an old/dormant
legacy org — possibly a predecessor Legrand entity or an unrelated historical account — not the
current active "Legrand US" relationship (which is `leg`, id 273, per TAM's near-zero 2026 activity
profile). **Left unresolved by design** — flagging for a human (Kjael/Kylor) to confirm `leg` is the
correct account and `lna` should stay excluded from the universe, rather than guessing.

Also noted in passing: a `TEST Gabriella White Wholesale TEST` org (id 172, shortname `gww`, 0
everything) exists in Postgres — a test fixture, correctly excluded from the universe already.

## Round 2 — the deeper identity fix (2026-07-09, same day)

Prompted by the user flagging "we have child/parent (entity) accounts" after Round 1's dedup
decision was presented back to them. Investigated further:

- Queried `organizations` for `id`, `name`, `company_website`, `company_email`, `created_at`,
  `billing_organization_id` for orgs 69 (`sc`), 87 (`scw`), 88 (`sccon`).
- `sc` (id 69): `name` = "Gabriella White", `company_website` = `www.GabriellaWhite.com`.
- `scw` (id 87): `name` = "Summer Classics", `company_website` = `www.summerclassics.com`.
- `sccon` (id 88): `name` = "Summer Classics Contract", `company_website` = `www.summerclassicscontract.com`.
- `billing_organization_id` on all three points to itself (no native Postgres parent-child FK) —
  consistent with `VM-K6` ("no native parent key... never present a derived family as a native
  hierarchy"). All three show recent order activity (`orders_last_90d` > 0) — genuinely separate,
  simultaneously-active billing entities, not a stale/duplicate/renamed account.
- **Root cause:** the v3.2 baseline mapped "Summer Classics" (the company name) onto org `sc`
  (which is really Gabriella White). This mismapping predates v4.0 and predates this validation
  pass — Round 1 inherited it and, seeing `sc`'s huge numbers already sitting under "Summer
  Classics," concluded the separate "Gabriella White" `??` row must be the duplicate. It was
  backwards: `sc` was never Summer Classics to begin with.
- Real-world structure (per company websites/public info): **Gabriella White is the parent
  holding company; Summer Classics and Summer Classics Contract are its brand-level operating
  entities.** Each has its own SuperCat catalog, customer base, and billing — the correct grain
  for this roster (per the segmentation methodology's own "grain: billing entity" principle) is
  one row per entity, not one row for the family.

**Corrected resolution:**

| Company | org | org_id | product_count | customer_count | order_count | invoiced_net |
|---|---|---|---|---|---|---|
| Gabriella White | `sc` | 69 | 17,510 | 92,470 | 333,740 | $122.7M |
| Summer Classics | `scw` | 87 | 6,941 | 8,463 | 119,686 | $166.1M |
| Summer Classics Contract | `sccon` | 88 | 10,149 | 5,375 | 65,941 | $74.3M |

All three land in **Premium Trade Brand** (Brand-Building / Outdoor) — consistent with the
qualitative anchor already in `build_v4.py` for `sc` and `sccon`; `scw` was newly anchored to the
same bucket for consistency with its siblings (not previously classified because the row didn't
exist under the right org).

**Open flag left for human review:** no one has re-examined whether each sibling's *individual*
selling motion still supports Brand-Building now that they're properly split — the qualitative
anchor was carried over by analogy to the siblings, not independently re-derived from Gabriella
White's retail-store/licensing model.

## Changes applied

- **Round 1 (superseded):** removed the "Gabriella White" `??` row, believing it a duplicate of
  "Summer Classics" (`sc`). This was wrong — see Round 2.
- **Round 2 (current):** fixed at the root in `build_v4.py` via a `SHORTNAME_CORRECTIONS` map
  applied during `build_master()`, not a hand-patched CSV: `('Summer Classics','sc') → 'scw'` and
  `('Gabriella White','??') → 'sc'` (plus the other 4 unmatched-account fixes from Round 1, now
  folded into the same mechanism). The full pipeline was re-run from the v3.2 source CSV, so the
  output is reproducible, not hand-edited. `scw` was also added to the `BRAND` anchor tuple in
  `classify_how_they_sell()` so it doesn't fall through to the generic price-based heuristic.
- Also added `compute_enrichment_medians()` to `build_v4.py`, fixing a latent bug where several
  §3 "median" figures in the analysis doc were actually single raw org values (e.g. the reported
  "median AOV $5,295" for Specification was literally org `ihw`'s AOV). All of §3/§6 in
  `current/SuperCat_Client_Segmentation_v4.0.md` were regenerated from this function.
- **Net effect: 109 accounts (Luxury Specification 33 / Premium Trade Brand 38 / Mid-Market
  Multi-Channel 24 / Volume Distribution 14) — matching the original Kjael-stamped headline
  counts exactly.** What changed from the as-stamped document is which org 2 of those 109 rows
  point at, plus the corrected §3 medians — not the totals.
- `SuperCat_Client_Segmentation_v4.0.md` (archive copy) and the stamped handoff's headline table
  were **not** edited in place (they're the stamped record of what Kjael reviewed) — see the
  updated header note at the top of that file instead.
  `current/SuperCat_Client_Segmentation_v4.0.md` carries the fully corrected numbers and is
  canonical going forward.

## Round 3 — independent audit (2026-07-09, same day)

Fresh-agent re-check of Round 2, driven by
`Customer Segmentation/handoffs/segmentation_v4.0_audit_handoff_2026-07-09.md`. Did **not**
trust prior-agent prose; re-derived load-bearing facts from live Postgres via
`user-supercat-postgres-vpn` (SELECT only) plus public web sources.

### 1. Core identity — **CONFIRMED**

| id | shortname | name | company_website | billing_organization_id | stripe_customer_id | created_at |
|---|---|---|---|---|---|---|
| 69 | `sc` | Gabriella White | www.GabriellaWhite.com | 69 (self) | cus_SXChHLspKtOS44 | 2014-02-05 |
| 87 | `scw` | Summer Classics | www.summerclassics.com | 87 (self) | cus_SXCh70eQmJpFAl | 2015-04-28 |
| 88 | `sccon` | Summer Classics Contract | www.summerclassicscontract.com | 88 (self) | cus_SXChSnV1ju6Thl | 2015-04-28 |

Independent public confirmation: PR Newswire / Furniture Today describe **Gabriella White LLC as
parent** of Summer Classics, Gabby, and Wendy Jane — not the reverse. Round 2's identity claim
is correct.

### 2. Three separate active accounts — **CONFIRMED**

Live Postgres (2026-07-09 afternoon; non-deleted products):

| org | products | customers | orders | last_order_at | orders_last_30d | orders_last_90d |
|---|---:|---:|---:|---|---:|---:|
| `sc` (69) | 19,072 | 92,474 | 333,764 | 2026-07-09 | 2,116 | 7,293 |
| `scw` (87) | 7,596 | 8,465 | 120,396 | 2026-07-09 | 1,302 | 4,509 |
| `sccon` (88) | 11,426 | 5,376 | 66,081 | 2026-07-09 | 727 | 2,293 |

All three posted orders the same day as this audit. Not one-live + two-stale.

**Hardcoded-dict drift (standing risk, flagged):** `build_v4.py` still uses a past snapshot —
e.g. org 87 products 6,941 in dict vs 7,596 live; org 69 products 17,510 vs 19,072 live. Direction
and relative scale are fine for segmentation; absolute counts will keep drifting until the script
queries Postgres live. Round 2's quoted validation-memo numbers matched the snapshot, not today's
live totals — expected.

### 3. Parent/child linkage — **CONFIRMED no native parent key**

`organizations` has `billing_organization_id` and `sandbox_of_id` only — no `parent_organization_id`,
no family/entity table. Related-name search finds only test fixtures (`sc_test` id 85, `gww` id
172), each with `billing_organization_id` pointing to itself. All three production orgs bill
themselves and have distinct Stripe customer IDs. Round 2's "no native parent key" claim holds;
`VM-K6` still applies.

### 4. Other 4 originally-unmatched accounts — **CONFIRMED matches; enrichment was incomplete**

| Company | shortname | id | live products | customers | orders | last order |
|---|---|---:|---:|---:|---:|---|
| Legrand US | `leg` | 273 | 1,012 | 1 | 0 | — |
| Silver One | `soi` | 230 | 1,106 | 0 | 0 | — |
| Tomlinson Companies | `tel` | 86 | 2,253 | 287 | 14 | 2022-03 |
| Ideal Living | `ilc` | 234 | 336 | 0 | 0 | — |

Matches Round 1. Dormant `lna` (id 93, "legrand", last order 2015-07-06) remains correctly
excluded — still an open human flag, not auto-resolved.

**Bug found (Round 3 fix):** `ORG_MAP` already listed `leg`/`soi`/`tel`/`ilc`/`abol`, and
`SHORTNAME_CORRECTIONS` remapped the roster rows onto them, but `PRODUCT_STATS` /
`CUSTOMER_STATS` / `ORDER_STATS` / `CAT_DIVERSITY` / `IPAD_USERS` had **no entries** for those
org ids. After Round 2's rebuild, those five CSV rows carried blank `product_count` and zeros
for customers/orders/iPad/categories — even though live Postgres has real catalogs (and, for
`tel`/`abol`, customers). Round 3 backfilled those dicts from live Postgres and added the five
shortnames to the `BRAND` anchor tuple so the `avg_price > 800` fallthrough would not shove
`tel`/`ilc` into Specification once prices were present.

### 5. §3 medians — **CONFIRMED method; Brand-Building figures updated after backfill**

Independently recomputed from the MASTER CSV with `statistics.median` (skipping non-floatable
empties — same behavior as `compute_enrichment_medians()`). Pre-backfill doc figures matched the
Round 2 CSV. After the Round 3 enrichment backfill, Brand-Building medians shifted (other
segments unchanged):

| Metric | Round 2 doc | After Round 3 backfill |
|---|---:|---:|
| Median AOV (Brand-Building) | $3,807 | $3,864 |
| Median product count | 2,148 | 1,962 |
| Median distinct categories | 27 | 36 |

`current/SuperCat_Client_Segmentation_v4.0.md` §3 updated to the post-backfill values.
Zero-inclusion note in `compute_enrichment_medians()` is intentional and consistent with how
`build_master()` writes missing lookups — not a bug for coverage-style fields; invoice medians
already correctly exclude zeros via `invoiced_nonzero`.

### 6. Reproducibility — **CONFIRMED**

Re-ran `python3 build_v4.py` from `v4/v4.0_archive/`; output CSV is byte-identical to
`current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` after the Round 3 copy. Headline
counts remain **109 / 33 / 38 / 24 / 14**.

### 7. Qualitative classification (`sc` / `scw`) — **left open, not moved**

Public GTM: Gabriella White runs ~19 branded retail stores (Gabby + Summer Classics under one
roof), a designer trade program, and wholesale — genuine multi-channel signals for the *family*.
Inside Postgres, though: `sc` looks like a consolidated wholesale/trade catalog org (92k
customers, 1 price code → `Wholesale (Dealers)`); `scw` already carries `Mixed (Trade + Retail)`
via 14 price codes. Keeping both in Premium Trade Brand / Brand-Building is defensible for
co-pilot grain (premium outdoor brand family, sibling to `sccon`) and matches the stamped
bucket. A human could still argue Multi-Channel for `sc` (or the family as a whole) — **do not
auto-move**; same open flag Round 2 left.

### 8. Stale-number sweep

Canonical live paths (`Customer Segmentation/current/`, `foundation/02_who_we_serve.md`,
`Insightful Product 4.0/foundation/segmentation_derivation.md`) already say **109 / 38**.
Remaining "108 / Gabriella White duplicate" references are in **explicitly superseded** artifacts
and were left alone:

- `Customer Segmentation/handoffs/segmentation_v4.1_handoff.md` (header: STALE — superseded)
- `Customer Segmentation/v4/v4.0_archive/build_segmentation_html.py` (pre-Round-2 HTML builder;
  still says "Gabriella White removed" / "108 orgs" — archive tooling, not current)
- Historical Round 1 prose inside this validation memo (kept for the audit trail)

### Round 3 changes applied

- `build_v4.py`: backfilled PRODUCT/CUSTOMER/ORDER/CAT/IPAD dicts for orgs 273/230/86/234/235;
  added `leg`/`soi`/`tel`/`ilc`/`abol` to `BRAND` anchor
- Regenerated both MASTER CSVs (archive + current) — still 109 rows, same segment counts
- Updated §3 Brand-Building medians + header errata in `current/SuperCat_Client_Segmentation_v4.0.md`
- Updated `current/README.md` to mention Round 3

**Verdict:** Round 2's identity fix is correct. Round 1's four other matches are correct. The
tidy "109 again" headline is real, not manufactured — but Round 2 left an enrichment hole on
five rows that Round 3 closed. Classification of the Gabriella White family remains a human
judgment call, not a data error.
