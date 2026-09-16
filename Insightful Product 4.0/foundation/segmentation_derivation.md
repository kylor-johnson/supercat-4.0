# Segmentation Derivation — label-free, first-party method

> **Scope note — do not conflate with SuperCat's own client segmentation.** This document is the
> **frozen** (VM-K5 / Q-SEG-DERIVE, owner directive 2026-06-29 — see `capability/value_moment_catalog.md`)
> method for segmenting a *single client's own customers* (the buyers within one manufacturer's
> book) by behavior. It is unrelated to, and unaffected by, **SuperCat's segmentation of its own
> ~109 client organizations** (Luxury Specification / Premium Trade Brand / Mid-Market
> Multi-Channel / Volume Distribution — by selling motion) — that work is stamped v4.0, lives in
> `Customer Segmentation/current/`, and does not touch, extend, or unfreeze the method below. If
> you are here because of the client-segmentation propagation handoff: nothing in this file needed
> to change — the "5 segments"/Specialty references it warned about don't exist in this doc or
> elsewhere in this foundation folder; this note exists purely to prevent a future reader from
> conflating the two.
>
> **Companion to [`provenance_map_customer.md`](provenance_map_customer.md); inherits [`provenance_spine.md`](provenance_spine.md).** This is the **method** for deriving segments from a client's own SuperCat data — *product type × price point × customer type* — **without imposing labels or fit scores**.
>
> **The non-negotiable principle (Spine §8).** Segments are **emergent** from first-party Postgres transaction/catalog data. We do **not** start from a taxonomy and sort customers into it. We do **not** score "fit." The TAM CSV LLM columns (`Segment_Opus_4.5`, `FIT_*_Opus_4.5`, the "Detected/Estimated" enrichment block) are **excluded as inputs** — they are biasing and demonstrably wrong (identical hallucinated text across distinct companies). Enrichment may only be used **after** derivation, as an external **agreement check** — never as a seed.
>
> **Why this is the unlock.** Segmentation has been hard precisely because it was attempted from labels/intuition. Bringing first-party Postgres transaction data to the table — product mix, realized price, buying cadence — lets segments fall out of the data itself.

---

## 1. The three dimension families (all first-party; all validated `[from-live]`)

### A. Product type — from `category_code` / `collection_code`, **not** `product_type`
- **Finding:** the named `product_type` column is **near-empty** (0% populated in 19/21 orgs). The real grouping signal is `category_code`/`category_codes` and `collection_code`/`collection_codes`.
- **These codes are org-defined and opaque.** They are *not* comparable across clients without a per-org interpretation pass. Example `[from-live]`, org 41 (a lighting maker):

  | category_code | items | avg $ | min–max $ |
  |---|---|---|---|
  | `CHAND` | 457 | 447 | 29–3,433 |
  | `PENDA` | 526 | 290 | 36–6,723 |
  | `SCONC` | 485 | 96 | 11–368 |
  | `BATH` | 537 | 133 | 15–387 |
  | `DOWNR` | 163 | 28 | 5–50 |
  | `PARTS` | 64 | 14 | 4–58 |

  A human reads these as chandeliers / pendants / sconces / bath / downlights / parts — **but the code strings are meaningless across orgs.** Derivation runs **per-org**; cross-client roll-ups require a per-org code→type mapping (a curated step), never a string match.

### B. Price point — from `products.net_price` (catalog) and `portal_invoice_items` (realized)
- **Finding:** `net_price` is numeric and well-populated; org-level price architectures differ enormously (org avg **$14 → $3,437** across the cohort). Within a single category the spread is also wide (org 41 `PENDA`: avg $290, max $6,723).
- **Method:** band price **within org and within category** (e.g., quartiles or natural breaks of `net_price`), because absolute dollars mean different things in a $15-parts catalog vs a $3,000-luxury catalog. Prefer **realized** price (`portal_invoice_items` unit price net of discount) when an invoice feed exists; fall back to catalog `net_price` otherwise.

### C. Customer type — **derived from behavior** (no native field)
- **Finding:** there is **no native customer-type/channel field**. `distribution_source` is unused (~0%); `default_price_code` is **100% populated** and is the only native tier signal (but discriminating power varies — some orgs have 1 price code, others 41).
- **Behavioral features (first-party, per billing entity):** order/invoice **cadence** (orders/yr, reorder interval), **AOV** (avg invoice net), **category breadth** (distinct categories bought), **mix concentration** (share in top category), **price-band centroid** (which price bands they buy), and **`default_price_code` tier** as a native cross-check. Customer "type" is the **cluster of these features**, not a label.

---

## 2. The derivation pipeline (per-org, label-free)

```
1. PREFLIGHT   Spine gates: Q-PROV-00 (feed), FEED_COMPLETENESS, customer identity (§7.2).
               Segmentation on invoiced data needs ≥ STRONG; else catalog-exposure-only (weaker, labeled).
2. PRODUCT     Map items to category/collection (per-org). Band net_price WITHIN category (quartiles/Jenks).
3. CUSTOMER    Build per-billing-entity behavioral feature vector (cadence, AOV, breadth, mix, price-centroid, tier).
4. DERIVE      Cluster (or quantile-grid) the feature space. Let k be data-driven (silhouette / elbow), small (3–6).
5. DESCRIBE    Name each segment FROM ITS OWN STATISTICS, descriptively — e.g.
               "high-AOV · low-frequency · single-category · top price band"
               NEVER "Interior Designer", "A-tier", a fit score, or any imposed taxonomy term.
6. VALIDATE    (optional) Compare emergent segments to external enrichment for AGREEMENT only (§3). Never relabel.
```

- **Grain:** billing entity (Spine §7.2). Parent/family roll-ups are derived+gated and reported separately.
- **Output of the method:** for a client, *its* segment set with sizes, revenue share, and the dimension centroids that define each — plus the action ("which segment to grow/defend"). No scores, no stars, no imposed names.

---

## 3. Enrichment is validated AGAINST, never seeded FROM
- After deriving segments from first-party data, you **may** overlay external enrichment (e.g., a customer's stated channel) to measure **agreement** — "do our behavior-derived clusters line up with what the world says they are?"
- **Disagreement does not override the data.** It flags either an enrichment error (common — the TAM CSV has hallucinated, duplicated descriptions) or an interesting behavioral reality. Either way, the **first-party derivation stands**; enrichment never relabels a customer.
- **Hard exclusion:** `Segment_Opus_4.5`, `FIT_*_Opus_4.5`, and the "Detected/Estimated" enrichment block are not inputs at any stage. First-party SuperCat columns (catalog, invoices, customers) are the only features.

---

## 4. Confidence & limits
- **Segments require ≥ STRONG commerce confidence** (an invoiced feed) to be behavior-true; on catalog-exposure-only data they are weaker and must be labeled as exposure-based, not purchase-based.
- **Cross-client segments are not free.** Because category codes are org-opaque, a cross-client segmentation product needs a per-org code→type curation layer; do not pretend `category_code` strings are comparable across clients.
- **No imposed labels ever leak downstream** — this is enforced at the Spine (§8) and re-checked in the value-moment authority refresh.

---

## 5. Validation provenance `[from-live]`
21-org cohort, read-only Postgres, 2026-06-26.
- `product_type` 0% in 19/21 orgs → category/collection are the product-type signal.
- `category_code` 10–285 distinct/org; `collection_code` 6–703/org → rich, but org-defined.
- `net_price` org averages $14 (heb) → $3,437 (pf); intra-category spread wide (org 41 PENDA 36–6,723) → band within org+category.
- `default_price_code` 100% populated (1–41 distinct) → native tier cross-check, variable power.
- `distribution_source` ~0% → not a usable channel/type field.

*(Demonstration cut is org 41; re-derive per client on the live cohort before client use.)*
