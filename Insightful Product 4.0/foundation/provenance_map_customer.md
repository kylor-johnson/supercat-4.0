# Customer & Segmentation Provenance Map — Tier 1

> **Inherits from [`provenance_spine.md`](provenance_spine.md).** Gates, tiers, and identity rules are canonical there; this map applies them to the **customer layer** and to **segmentation**. SQL lives in `query_library_v2.md` (Tier 2). The label-free segmentation *method* has its own companion doc: [`segmentation_derivation.md`](segmentation_derivation.md).
>
> **Two principles that govern this layer.**
> 1. **The billing entity is the default customer grain** — there is no reliable native parent/corporate-family key (Spine §7.2). Roll-ups above the billing entity are derived and gated.
> 2. **Segments are derived from first-party behavior, never labeled.** No fit scores, no imposed segment names. First-party Postgres transaction/catalog data *informs* segments; external enrichment is validated *against*, never seeded *from* (Spine §8). The TAM CSV `FIT_*`/`Segment_Opus_*` columns are **excluded** as inputs.
>
> **Audience:** owner/CEO (book composition, concentration) and sales leadership (who to grow/defend). Action-first.
>
> **Empirical basis:** 21-org live Postgres cohort, 2026-06-26 (§ Validation). `[from-live]` = diagnostic; `[ILLUSTRATIVE]` = design.

---

## 1. The model in one picture

```
WHO the customer is (identity)          WHAT they buy (segmentation dimensions, all first-party)
  customers.code / bill_to_number ──┐     products: category_code / collection_code  (product type)
  (billing entity = default grain)  │     products.net_price                          (price point)
  parent/family ── DERIVED, gated ──┘     portal_invoice_items                        (realized mix, AOV)
        │                                 order/invoice cadence                        (behavioral type)
        ▼                                 default_price_code                           (native tier proxy)
  CUSTOMER PROFILE  ◄──── enrich with ──── invoiced $ (Spine §6 gated) ────► VALUE / CONCENTRATION / DECLINE
  (segment = emergent cluster of the dimensions above — never an imposed label)
```

---

## 2. Feeds inventory — HAVE vs. CLIENT-MUST-ADD

| Feed | Grain | We HAVE | Client must add | Notes / gate |
|---|---|---|---|---|
| `customers` | billing entity | **Yes** — code, name, billing_state, `default_price_code`, territory, `mapped_code` | accuracy | `default_price_code` **100% populated** `[from-live]`; `mapped_code` ~0% (no parent key). |
| `portal_invoices` / `_items` | invoice / line | Only if `invoice_data.csv` sent | **invoice feed** | The value/behavior backbone. Gated by Spine §6 + customer identity §7.2. |
| `products` | item | **Yes** — `category_code(s)`, `collection_code(s)`, `net_price`, `trade_name_code` | clean codes | `product_type` **near-empty** — use category/collection (Spine §7.4). |
| territory (`customers.territory_codes`) | code(s) | **Yes** (uniformly JSON in cohort) | accuracy | Format preflight (Spine §7.3); links customer↔rep. |
| `sales_data` | coarse line | sometimes | — | LIMITED tier only (no dates) — magnitude, not trend. |

---

## 3. Customer identity resolution (this map's identity work) — *canonical def in Spine §7.2*

| Question | Native key? | Rule |
|---|---|---|
| Who is this customer? | **Yes** — `customer_bill_to_number` / `customers.code` | **Default grain. Report here.** |
| Ship-to → bill-to? | Yes — `customer_ship_to_number` → `customer_bill_to_number` | Roll ship-tos into their bill-to. |
| Bill-to → parent / corporate family? | **No** (`mapped_code` ~0% `[from-live]`) | **Derived + gated:** fuzzy name+address; never "exact." **Suppress where name is degenerate** (clli: 1 distinct invoice name across 2,838 codes). |
| Customer → rep/territory? | Partial (`territory_codes`) | Format preflight; territory presence ≠ correct assignment. |
| Customer "type" (retailer/designer/hospitality/contract)? | **No native field** | **Derived from behavior** (see §5 / `segmentation_derivation.md`); `default_price_code` is the only native tier proxy; never an imposed label. |

---

## 4. Provenance map — one row per customer insight (action-first)

| # | Insight (so-what) | Feeds required | We HAVE | Client must add | Confidence if complete | If a piece is missing |
|---|---|---|---|---|---|---|
| **K1** | **Customer value ranking** — who actually drives invoiced revenue | `portal_invoices`, customer identity | identity only | **invoice feed** | **STRONG** (FULL needs CORROBORATED, Spine §6.3) | No feed → suppress $ ranking; offer order-activity ranking (intent, labeled). |
| **K2** | **Concentration & single-account risk** — % of book on top N accounts | `portal_invoices`, customer identity | identity only | **invoice feed** | **STRONG** | Billing-entity grain unless a parent roll-up is derived+gated (§3). |
| **K3** | **Account decline / churn-risk** — accounts quietly shrinking | `portal_invoices` (≥2 periods), identity | identity only | **invoice feed w/ history** | **STRONG** | <2 periods of history → suppress trend; show current-period only. |
| **K4** | **New vs. reactivated vs. lapsed** — book composition by tenure | `portal_invoices` (dated), identity | identity only | dated invoice feed | **STRONG** | `sales_data` only (no dates) → cannot compute tenure → suppress. |
| **K5** | **Segment composition of the book** — what *kinds* of customers the revenue rides on | `portal_invoices`, `products`, `customers` | products + identity | invoice feed | **STRONG** (segments emergent, §5) | No feed → segment on catalog exposure only (weaker), labeled. |
| **K6** | **Parent/corporate-family roll-up** — true enterprise exposure | derived parent map + `portal_invoices` | nothing native | invoice feed | **PARTIAL** (derived identity) | Always labeled "estimated family"; suppress where name degenerate. |
| **K7** | **Price-realization leakage** — same product sold cheaper to some accounts, in $ | `portal_invoice_items` + identity | identity only | **invoice feed (line-level)** | **STRONG** (gut-check required for $) | Gate `leakage_dispersion_ok` (join ≥60%, Spine §6.8). **Dispersion, never "% off list"** (Spine §6.10). Suppress where join < 60% (e.g. pf-style namespace mismatch is *rescued* by dispersion; truly no lines → suppress). |
| **K8** | **Account-health $-at-risk** — accounts quietly dying, flagged 90d early w/ $ + who-to-call | `portal_invoices` (≥2 equal periods), identity, `rep_number` | identity only | **invoice feed w/ history** | **STRONG** | **Equal-length decay windows** (last 6mo vs prior 6mo) — unequal windows false-flag accelerating accounts (live: WAYFAIR $7.9M). $ at risk = LTM revenue. Pushed via the exception layer (§8). |

---

## 5. Segmentation inputs (summary — full method in `segmentation_derivation.md`)
> **🧊 FROZEN (owner directive, 2026-06-29).** Segmentation is the **final step** of this program and is deferred. The notes below are preserved as-is; **do not advance the method, add dimensions, cluster, or ship segmentation** until the owner unfreezes it. `Q-SEG-DERIVE` (K5) is frozen in the library. See `selling_customer_SKEPTICAL_AUDIT_handoff.md` §5.
- **Dimensions are all first-party and emergent:** **product type** (`category_code`/`collection_code` — `product_type` is empty), **price point** (`net_price`; realized via `portal_invoice_items`), and **behavioral customer type** (cadence, AOV, reorder rate, category breadth, `default_price_code` tier).
- **No imposed labels.** Segments are clusters/quantile bands over these dimensions, named descriptively from their own data (e.g., "high-AOV, low-frequency, single-category"), not mapped to a predefined taxonomy.
- **Enrichment is a validation check, not an input.** The TAM CSV `FIT_*`/`Segment_Opus_*` columns are excluded (Spine §8). First-party SuperCat columns may be features.
- **Price band is derived from REALIZED price, not list** (hardening R4). `NTILE` over each customer's average realized line price → segmentation works even on list-absent orgs (live: ufi, list 0%, segments cleanly into a non-degenerate 9-cell grid). Do not gate segmentation on `products.net_price`.

---

## 6b. Economics layer (Domain 10) — what reconciled in, 2026-06-29 (audit-remediated)

The selling/customer **economics** queries were hardened on a fresh 22-org cohort (`selling_customer_pilot_test_worksheet.md`) and authored into `query_library_v2.md` Domain 10 (renumbered from 9). They inherit the **Spine §6.8 `Q-ECON-00` gate**, the **§6.9 hard gaps**, and the **§6.10 dispersion-leakage rule**. Customer-layer GO queries: `Q-ECON-LEAK` (K7), `Q-ECON-RETURNS`, `Q-SELL-QC` (vanity-quoting flag), plus `Q-ECON-NETREV/-TERMS/-LEADTIME/-CARRIER` on the commerce side. **`Q-SEG-DERIVE` (§5/K5) is 🧊 FROZEN** — segmentation is the program's final step, deferred by owner directive (2026-06-29). **Confidence is now completeness-capped** (`selling_customer_confidence_audit.md`, 2026-06-29): `Q-ECON-00` emits `COMMERCE_CONFIDENCE` and every economics number reports at `LEAST(own ceiling, COMMERCE_CONFIDENCE)`; `FULL` is unreachable. `Q-ECON-LEAK` is now **tier-aware** (median + tier/volume guard, with `house_suspect` auto-detect) and `Q-SELL-QC` is relabeled an **eCat-channel** proxy (LIMITED, suppressed below 20% eCat share). **Client-facing confidence labels were APPROVED by the owner 2026-06-29 and applied** (leakage capped at `COMMERCE_CONFIDENCE`; `Q-SELL-QC` → LIMITED) — see `selling_customer_label_signoff.md`.

**Hard gaps that bound this layer (Spine §6.9 — suppress, do not approximate):** true/gross margin (no COGS), AR/DSO/credit risk (no dealer AR; `terms` is billed-not-collected), damage-by-carrier, inventory aging, market/showroom ROI.

---

## 7. Reconciled identity & data outliers (economics hardening)

| finding `[from-live]` | rule it sets |
|---|---|
| `pf` has 100% list coverage but **0% invoice-line→product join** | leakage eligibility = **join coverage**, never list presence (Spine §6.8 R2); dispersion (K7) still works |
| `products.net_price` is MSRP for some orgs, wholesale for others (cci/scw/gh 55–69% "off list" = wholesale spread) | leakage = **dispersion**, "% off list" prohibited (Spine §6.10) |
| **clli invoices carry blank `customer_bill_to_name` on all 1.09M rows** | resolve customer names via the `customers` join for every customer-facing output (extends §3 clli rule) |
| `clm` invoice dated **4107**, `jyc` **2032** | clamp `report_through_date ≤ today` (Spine §6.8 R1) |
| `terms` free-text (clli 48 variants); returns 35% by count vs **8% by dollars** | normalize terms; measure returns by **dollars** |

---

## 8. Exception-push synthesis layer (answers, not dashboards)

The customer layer feeds [`selling_customer_exception_layer.md`](selling_customer_exception_layer.md) — the operator that turns these insights into **pushed exceptions with a dollar figure and a name**, per Customer-Intelligence v4 design (`../Customer Intelligence/09_v4_design.md` §15 revenue-at-risk, §16 alert banners). First two exception types, both validated live (2026-06-29):
- **S1 — Account-health $-at-risk** (from K8): *"HATCH P down 79% over 6 months, $70K LTM at risk — call rep MKJ."* Equal-window decay (refinement above).
- **C2 — Leakage-by-rep** (from K7): *"Rep 69 is giving away $1.35M = 42% of their own revenue (peers ~5%)."* Report leaked-$ **and** leak-rate so a big book isn't mistaken for a rogue discounter.

Every exception inherits `Q-ECON-00` confidence and is **suppressed below STRONG** for any dollar figure; leakage dollars additionally require a human gut-check (worksheet A.5.6).

---

## 9. Validation appendix `[from-live]`
**Cohort:** 21 orgs (segmentation/identity, 2026-06-26) + 22-org economics cohort (2026-06-29, `selling_customer_pilot_test_worksheet.md`), read-only Postgres.

| Identity / dimension claim | Evidence |
|---|---|
| Billing entity is the only reliable grain | `customer_bill_to_number` clean; **`mapped_code` populated 0% in 18/21 orgs** (max sc 41.5%, scw 9.6%, gh 5.5%) |
| Name-based parent roll-up is low-yield / sometimes impossible | bill-to codes ≈ distinct names in nearly every org; **clli = 1 distinct invoice name across 2,838 codes** |
| No native customer type; price-code is the only native tier | `default_price_code` **100%** populated all 21 orgs (distinct codes 1–41); `distribution_source` ~0% |
| Product type must come from category/collection | `product_type` 0% in 19/21 orgs; `category_code` 10–285 distinct/org; `collection_code` 6–703/org |
| Price point is a strong native dimension | `net_price` numeric, well-populated; org averages span **$14 (heb) → $3,437 (pf)** — distinct price architectures |
| Territory present (links customer↔rep) | `territory_codes` 100% JSON-array, 0 blank in cohort (format-variance risk remains library-wide) |

*(Re-run on the live cohort before client use.)*
