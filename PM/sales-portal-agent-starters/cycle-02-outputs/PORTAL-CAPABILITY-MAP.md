# PORTAL-CAPABILITY-MAP — every answer the Sales Portal can deterministically surface

**Agent:** CAPABILITY (06) · **Cycle:** 02 · **Date:** 2026-07-17
**Job:** map every answer the Sales Portal could computationally surface off the invoiced spine — the
data each needs and the confidence tier it can honestly carry. Gather + map only; no UI, no tech plan.

---

## Load confirmation (reading contract honored)

Loaded spine + provenance + runtime ground truth before mapping. The three authority paths:

1. `PM/sales-portal-agent-starters/00-PROGRAM-SPINE.md` — lanes / bets / WIP / metric law (Lane 2 = computational).
2. `Insightful Product 4.0/foundation/provenance_spine.md` — the metric-law authority (invoiced axiom, confidence tiers, `FEED_COMPLETENESS`, identity gates, gate catalog).
3. `Insightful Product 4.0/foundation/WHAT_ACTUALLY_RUNS.md` — runtime ground truth (24 query IDs, 14 signal detectors, 2 gating axes, one template family) — **precedence-topping.**

Also synthesized (equal sources): `CANON.md`, `query_library_v2.md` (LIVE 20 of 24 SQL bodies read), `report_product/signal_catalog_v4.md`, `foundation/capability/insights_moneymap_SYNTHESIS.md` (**roadmap, not runtime**), `value_moment_catalog` menu via `vm_runtime_index.md`, `segmentation_derivation.md` (🧊 FROZEN), `selling_customer_exception_layer.md` (S1 + C2 SQL), `profiles/sarreid.md` (worked reference).

**Grounding rule applied:** every `COMPUTABLE` row's Computation column reuses an **existing canonical query** cited by doc + id. No row is marked computable on hand-waving. Where the invoiced spine has no column, the row is a **HARD GAP**, not a capability.

---

## Metric law inherited (not re-derived — see provenance_spine §1, §5, §6, §7)

- **Revenue spine = `SUM(portal_invoices.net_amount)`** over a `report_through_date`-clamped window. `net_amount` is client-facing invoiced total, **negative for credit memos**. `portal_invoices.total_amount` is **NULL** for live orgs — not the sales figure (Spine §1).
- **RTD clamp:** `report_through_date = MAX(invoice_date) WHERE invoice_date ≤ CURRENT_DATE`; LTM = trailing 12mo ending at RTD, never `CURRENT_DATE` (Spine §6.4, §6.8 R1).
- **$5M single-row cap** unless the org is known to transact at that scale (Spine §6.6).
- **Customer grain = billing entity** (`customer_bill_to_number`); no native parent/corp key (Spine §7.2).
- **Confidence ceiling = STRONG** on a single invoice feed; **FULL unreachable** without `FEED_COMPLETENESS = CORROBORATED` (Spine §5, §6.3; `WHAT_ACTUALLY_RUNS` — code tops out at STRONG). Every number carries the single-feed caveat.
- **Gross-vs-net asymmetry is real:** some orgs net zero credits (sarreid — net ≈ gross-of-returns), others net thousands (cci = 4,765 credit rows). Any topline caveat must state which case the org is in (Spine §6.9; Money Map §3.0).
- **Two gating axes (WHAT_ACTUALLY_RUNS):** `COMMERCE_CONFIDENCE` ∈ {STRONG,PARTIAL,LIMITED,NONE} (set by `Q-ECON-00` — "can I show dollars?") and `REP_IDENTITY_TIER` ∈ {0,1,2} (set by `RP-2` — "can I name reps?"). `REPORT_INTELLIGENCE_TIER = LEAST(DATA_MASS_TIER, COMMERCE_CONFIDENCE)`.

**Real column inventory the map is allowed to touch** (Spine §3.1, code-verified):
`portal_invoices`: `net_amount`, `invoice_date`, `invoice_number`, `order_number`, `customer_bill_to_number`, `customer_bill_to_name`, `rep_number`, `customer_bill_to_state`, `freight_amount`, `tax_amount`, `discount_amount`.
`portal_invoice_items`: `item_number`, `unit_price`, `unit_price_discount`, `extended_price_discount`, `quantity_ordered`, `quantity_invoiced`, `quantity_returned`, `description`.
`portal_orders`: `order_origin` (sparse/advisory), `rep_number`, `rep_name` (the only name bridge), `customer_bill_to_number`, `order_date`, `total_amount` (booked, ≠ sales).
`products`: `item_number`, `collection_code`, `category_code`, `net_price` (semantics vary per org), `long_description`, `short_description`, `deleted`.
`orders` (eCat): eCat-SALE-filtered GMV, `rep_number`/`rep_name`/`org_user_id`.
**Absent at schema level (full `information_schema` scan, Spine §6.9):** no `unit_cost`/COGS/margin, no dealer AR/collections, no rebate/chargeback/coop, no claims/damage. These bound the hard-gap list below.

---

# 1. DETERMINISTIC-NOW — ship in a computational report (COMPUTABLE NOW)

Each rides the invoiced spine + within-table arithmetic, reuses a LIVE canonical query, and carries the single-feed STRONG caveat.

| # | Capability (the question a rep/owner asks) | Hero tier | Computation (canonical query · doc) | Columns required | Confidence ceiling | Data-availability risk | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | **"What did we actually sell — the one number that reconciles to the dollar?"** | Money Map **C1 / HERO 1** (VM-C1, tier S) | `SUM(portal_invoices.net_amount)` over RTD-clamped LTM (`Q-ECON-00` preflight sets source+RTD) · `query_library_v2` Domain 10 / `provenance_spine §6.8` | `net_amount`, `invoice_date` | **STRONG** (never FULL — single feed; §6.3) | Suppress on PROVABLY-INCOMPLETE (eCat > 1.05× invoiced, e.g. `sc`); DEAD feed (`heb`); clamp on STALE (`mhc`). Gross-only orgs → label "gross invoiced." | **COMPUTABLE NOW** |
| 2 | **"How exposed are we to one account?"** (single-account / top-10 / HHI) | Money Map **C3 / HERO 3** (VM-C3, tier A) | top-1/5/10 share + Herfindahl over `SUM(net_amount)` by customer · `Q-ECON-CONC` (`query_library_v2` L5031; live cci top-1 6.0%, HHI 54) | `net_amount`, `customer_bill_to_number` | **STRONG**, capped at `COMMERCE_CONFIDENCE` | Billing-entity grain only — a parent under many bill-to codes reads diversified; real concentration is **worse, never overstated** (§7.2). ORDERS/SALES_DATA source → cap PARTIAL/LIMITED. | **COMPUTABLE NOW** |
| 3 | **"Are we actually growing?"** (staleness-proof YoY / QoQ) | Money Map **C10** (VM-C10, tier A) | trailing-12mo vs prior-12mo `net_amount`, **both windows ending at RTD** · `Q-ECON-MOMENTUM` (`query_library_v2` L5130; live cci +5.2%) | `net_amount`, `invoice_date` | **STRONG**, capped at `COMMERCE_CONFIDENCE` | Suppress trend on LIMITED/SALES_DATA (no dates). A trailing window run into empty post-feed months fakes a crash — RTD anchor is mandatory (the `mhc` fix). | **COMPUTABLE NOW** |
| 4 | **"How much of our 'growth' is a few big deals?"** (honesty guard) | Money Map **C11** (VM-C11, tier S) | invoice-grain size distribution: top-1%/5% of invoices, ten-largest share, Gini · `Q-ECON-LUMP` (`query_library_v2` L5153; live cci Gini 0.532) | `net_amount`, `invoice_number` | **STRONG**, capped at `COMMERCE_CONFIDENCE` | Invoice grain: one big PO split across invoices reads as several mid invoices — annotate known contract orders. Rarely suppressed (it *is* the suppression check for #1/#3). | **COMPUTABLE NOW** |
| 5 | **"Which accounts are quietly dying, worth how much, who calls them?"** | Exception **S1** = VM-K8/S1 (tier A); Signal `SIG-ECON-RISK-01` | per-account equal 6mo-vs-prior-6mo decay + cadence gap; $-at-risk = account LTM; who-to-call = rep · `S1` SQL (`selling_customer_exception_layer.md`; live cci) | `net_amount`, `invoice_date`, `customer_bill_to_number`, `customer_bill_to_name`, `rep_number` (+`portal_orders.rep_name` for naming) | **STRONG**; **PARTIAL → dollar is a labeled floor**, NONE → suppress | **Must use equal windows** (6mo vs prior-6mo) — the 6-vs-18 form false-flagged accelerating WAYFAIR ($7.9M). CRITICAL is cadence-scaled w/ 14-day floor. Rep *name* needs Tier-2 bridge; else "rep &lt;n&gt;". | **COMPUTABLE NOW** |
| 6 | **"How much won demand never shipped?"** (fill / booked→invoiced leakage) | Money Map **C4 / HERO 4** (VM-C4, tier B) | within-line `SUM(quantity_invoiced)/SUM(quantity_ordered)`; leaked $ = (ordered−invoiced)×`unit_price` · Money Map C4 / `signal_catalog` SIG (within-line, **no header join**) | `quantity_ordered`, `quantity_invoiced`, `unit_price`, `item_number` | **STRONG** | Order→invoice header join ≈0% (§2) — **within-line only**; never sum order+invoice tables (double-count). Stale feed makes will-still-ship lines look leaked → clamp to aged cohorts at RTD. | **COMPUTABLE NOW** |
| 7 | **"How much of the book is durable reorder vs one-and-done?"** | Money Map **C7** (VM-C7, tier B) | customer recurring (bought prior window OR ≥2 distinct months) vs one-off share of LTM net · `Q-ECON-QUALITY` (`query_library_v2` L5068; live cci 94% recurring) | `net_amount`, `invoice_date`, `customer_bill_to_number` | **STRONG**, capped at `COMMERCE_CONFIDENCE` | Needs ≥2 comparable windows (≥24mo). Seasonal one-market-order/yr buyers look one-time — pair with #4/#8; suppress <2 windows. | **COMPUTABLE NOW** |
| 8 | **"What's our intra-year revenue rhythm / cash calendar?"** | Money Map **C8** (VM-C8, tier C) | month-share computed within each year, averaged across years; `years_observed` flags thin months · `Q-ECON-SEASON` (`query_library_v2` L5100; live cci Oct–Dec peak) | `net_amount`, `invoice_date` | **STRONG**, capped at `COMMERCE_CONFIDENCE` | Needs ≥2 (pref 3) full years; suppress otherwise. One-off big order distorts a month → median/avg-of-years, never a single year. | **COMPUTABLE NOW** |
| 9 | **"Where do we land the year?"** (pacing range, never a forecast) | Money Map **C9** (VM-C9, tier B) | YTD net, day-of-year annualization, trailing-12mo, same-period-prior-yr → a **band** seasonally-adjusted (C8) + lumpiness-widened (C11) · `Q-ECON-PACE` (`query_library_v2` L5191) | `net_amount`, `invoice_date` | **STRONG** (band only) | Needs ≥24mo. **Always a band, never a point**; forbidden words "forecast"/"oracle." Far-future corrupt dates poisoned buckets (`clm` yr 4107) → RTD clamp. | **COMPUTABLE NOW** |
| 10 | **"Are existing accounts worth more or less this year?"** ($ NRR) | Money Map **C17** (VM-C17, tier B) | prior-year cohort: this-year net ÷ prior-year base; expansion vs contraction $ + full-churn count · `Q-ECON-NRR` (`query_library_v2` L5229; live cci 88.0% NRR$) | `net_amount`, `invoice_date`, `customer_bill_to_number` | **STRONG**, capped at `COMMERCE_CONFIDENCE` | Needs ≥2 contiguous yrs + **stable customer keys**; ERP re-keying/bill-to splits fake churn/expansion → reconcile keys, present a band. | **COMPUTABLE NOW** |
| 11 | **"Which big accounts contribute less than their size?"** (contribution proxy) | Money Map **C20** (VM-C20, tier B) | per-account net − freight billed − returns; rank rev vs contribution, surface rank-drops · `Q-ECON-CONTRIB` (`query_library_v2` L5262; live cci) | `net_amount`, `freight_amount`, `customer_bill_to_number`, `customer_bill_to_name` | **STRONG** (proxy) | **Contribution proxy, NOT gross profit** — no COGS (hard gap). Freight is header-level; bundled-freight orgs understate the drag. Label precisely. | **COMPUTABLE NOW** |
| 12 | **"What are our top products, and how broadly distributed?"** | supporting cut (feeds product section) | top-25 items by `SUM(quantity_invoiced × unit_price)` LTM + distinct-dealer breadth · `Q-PROD-TOP` (`query_library_v2` L5368; live cci) | `item_number`, `quantity_invoiced`, `unit_price`, `customer_bill_to_number`, `products.long/short_description` | **STRONG**, capped at `COMMERCE_CONFIDENCE` | Note uses `CURRENT_DATE` window in shipped SQL (not RTD) — minor; sharpen to RTD on stale feeds. No margin/velocity claim. | **COMPUTABLE NOW** |
| 13 | **"Which product families/collections are growing?"** (LTM + YoY) | supporting cut | group invoiced lines by `products.collection_code`; LTM rev, YoY, dealer/SKU breadth · `Q-PROD-FAMILY` (`query_library_v2` L5402; live cci Bunny Williams +56%) | `item_number`, `quantity_invoiced`, `unit_price`, `products.collection_code`, `customer_bill_to_number` | **STRONG**, capped at `COMMERCE_CONFIDENCE` | Requires ≥1 non-null `collection_code`; org-defined/opaque codes (§7.4) — the label ships as-is, don't infer margin. Empty → graceful skip. | **COMPUTABLE NOW** |
| 14 | **"Which of our anchor-SKU dealers have never bought the growth family?"** (cross-sell gap) | supporting cut (field play) | #1 item × #1 family; return anchor-buyers not in target-family buyers · `Q-CROSS-SELL` (`query_library_v2` L5464; live cci 184 gap dealers) | `item_number`, `quantity_invoiced`, `unit_price`, `products.collection_code`, `customer_bill_to_number` | **STRONG**, capped at `COMMERCE_CONFIDENCE` | Factual count only — no propensity/intent modeling. Needs Q-PROD-TOP + Q-PROD-FAMILY non-empty. | **COMPUTABLE NOW** |
| 15 | **"Is topline carried by same-base expansion or new-dealer intake?"** (cohort flow + cadence) | supporting cut (Money Map C7/C17 sibling) | active/new/returning/lapsed cohorts, same-base lift, frequent/occasional/one-time cadence, 2nd-yr return · `Q-DEALER-COHORT` (`query_library_v2` L5531; live cci) | `net_amount`, `invoice_date`, `invoice_number`, `customer_bill_to_number` | **STRONG**, capped at `COMMERCE_CONFIDENCE` | Needs ≥2 contiguous years. Cohort labels observational (bought/didn't), not value judgments. | **COMPUTABLE NOW** |
| 16 | **"What's our real product revenue net of freight/tax pass-through?"** | Money Map **C16** (VM-C16, tier C) | decompose `net_amount` vs `freight_amount`/`tax_amount`/`discount_amount` (header) · Money Map C16 / VM-C16 (`Q-ECON-COMPOSITION`) | `net_amount`, `freight_amount`, `tax_amount`, `discount_amount` | **STRONG** | Orgs that fold freight into line price (component cols zero) → **suppress strip-out, report topline as-is**; don't double-subtract a discount already netted. | **COMPUTABLE NOW** (where itemized) |

---

# 2. COMPUTABLE-GATED — real, but only fires when a per-org gate passes

These use real columns but a preflight flag / feed state / identity tier decides FIRE vs DEGRADE vs SUPPRESS. Do not promise them blanket across orgs.

| # | Capability | Hero tier | Computation (canonical query · doc) | Columns required | Confidence ceiling | Gate that decides fire/suppress | Verdict |
|---|---|---|---|---|---|---|---|
| 17 | **"How much did we give away in discounts, and to whom?"** (price leakage) | Money Map **C2 / HERO 2** (VM-C2, tier A); `SIG-ECON-LEAK-01` | tier-aware **same-SKU realized-price dispersion** (true median; exclude recognized tiers & ≥10%-volume accounts; auto-flag house/sample) · `Q-ECON-LEAK` (`query_library_v2` L4754) | `item_number`, `unit_price`, `quantity_invoiced`, `customer_bill_to_number`, `rep_number` | **STRONG, always DIRECTIONAL**, capped at `COMMERCE_CONFIDENCE` | `leakage_dispersion_ok` = **priced invoice lines ≥60%** (`unit_price>0`, NOT a products join). **Mandatory human gut-check + per-org house-account confirm** before any dollar ships (the asi rep-69 "42% rogue" false positive). **"% off list" is prohibited** (§6.10). | **COMPUTABLE-GATED** |
| 18 | **"Is discretionary discounting concentrated in specific reps?"** (rogue-discount alarm) | Exception **C2** (VM-C2-rep, tier B); `SIG-ECON-LEAK-02` | `Q-ECON-LEAK` dispersion rolled up by rep, leaked $ + leak-rate · `C2` SQL (`selling_customer_exception_layer.md`; live asi) | as #17 + `portal_orders.rep_name` | **STRONG**, capped; internal-lead | Needs `leakage_dispersion_ok` **AND** rep-identity **Tier 2** (name bridge ≥82%) to name; Tier 1 → `rep_number` grain; Tier 0 → suppress. Gut-check mandatory. Known 30s Postgres-timeout risk on full Tier-2 books. | **COMPUTABLE-GATED** |
| 19 | **"What share of our invoiced business runs through eCat?"** (capture, not attribution) | Money Map **C14** (VM-C14/CHAN-1, tier B); `SIG-COMMERCE-01` | confirmed eCat-SALE GMV (`orders`) ÷ invoiced total · `Q-CHAN-05` (`query_library_v2` L1544) | `orders` (eCat-SALE filtered), `net_amount` | **STRONG** as a rate **only at CORROBORATED**; else absolute $ only, **LIMITED** | Rate valid only when `FEED_COMPLETENESS = CORROBORATED`. **Suppress entirely below 20% eCat penetration**; if eCat > 1.05× invoiced (`sc` 126%) the **feed is incomplete** → report the gap, never >100%. This is **capture ≠ attribution** (§4). | **COMPUTABLE-GATED** |
| 20 | **"Where do we sell — eCat vs every other channel?"** (headline split) | Channel **VM-CHAN-1** (tier B) | eCat (owned `orders`) vs non-eCat as share of invoiced total · `Q-CHAN-05` / `Q-CHAN-00` gate (`query_library_v2` L1544/L1654) | `orders`, `net_amount` | **STRONG** (abs $) / gated rate | Same CORROBORATED gate as #19. Always shows "eCat vs all other" — the remainder is **not** attributed to a sub-channel here. | **COMPUTABLE-GATED** |
| 21 | **"Break the non-eCat slice into sub-channels (EDI/web/phone/market)."** | Channel **VM-CHAN-2** (tier C) | `portal_orders.order_origin` % mix via maintained per-org map, applied to invoiced total · `Q-CHAN-10` (`query_library_v2` L1766) | `portal_orders.order_origin` + per-org channel map, `net_amount` | **STRONG** (mix on booked $) | `CHANNEL_CONFIDENCE ≠ NONE` (`Q-CHAN-00`: ≥60% booked $ attributed, ≥2 origins). **Blank for ~30/41 orgs; only `cci` tags eCat reliably** (`ril` over-tags 12×, `wwjc` 0.25×). Overlay eCat from `orders`, never origin. Suppress for NONE-tier. | **COMPUTABLE-GATED** |
| 22 | **"Which accounts/reps bill below our reference price?"** (off-list adherence) | Money Map **C12** (VM-C12, tier C) | realized unit price vs `products.net_price` / price-level; gap $ by rep/customer · Money Map C12 (`Q-ECON-OFFLIST`) | `unit_price`, `unit_price_discount`, `item_number`, `products.net_price`, `customer_bill_to_number`, `rep_number` | **STRONG** (descriptive) | `products.net_price` must be a **meaningful reference** — semantics vary per org (cci/scw/gh show 55–69% "off list" = normal wholesale spread, §6.10). Suppress off-list claim where `net_price` blank/0; present "below reference," never "unauthorized." | **COMPUTABLE-GATED** |
| 23 | **"How much did our list-price increase actually stick?"** (pass-through) | Money Map **C13** (VM-C13, tier C) | realized price before/after a known list-change date, net of mix · Money Map C13 (`Q-ECON-PASSTHRU`) | `unit_price`, `unit_price_discount`, `item_number`, `invoice_date` | **STRONG** (correlational) | Needs a **known increase date + stable item identity**; no dated `net_price` history in schema → realized step-change proxy, labeled. Mix shift confounds → control for mix. | **COMPUTABLE-GATED** |
| 24 | **"How much revenue reverses as returns/credits?"** | Money Map **C5** (VM-C5, tier B); `SIG` returns | `SUM(net_amount WHERE net_amount<0)` + line `quantity_returned` by item/customer · `Q-ECON-RETURNS` (`query_library_v2` Domain 10) | `net_amount` (credit rows), `quantity_returned`, `item_number`, `customer_bill_to_number` | **STRONG** | `RETURNS_IN_FEED = true`. **Gross-only orgs read a silent 0%** (sarreid, ufi, pf, jyc, bcf, kll, clm, lpf, wwjc) → **suppress/relabel "returns not represented," never "$0 returns."** | **COMPUTABLE-GATED** |
| 25 | **"How much recent-introduction revenue?"** (new-item vitality) | Money Map **C23** (VM-C23, tier C) | line net for items with derived first-sale <12mo ÷ total invoiced · Money Map C23 (`Q-ECON-NEWINTRO`) | `item_number`, line net, `invoice_date` (derived first-sale) | **STRONG** | Prefer **derived first-sale date** — `products.new_item` flags go stale and overstate vitality. | **COMPUTABLE-GATED** |
| 26 | **"How old is committed-but-unbilled backlog, and how fast does order→invoice turn?"** | Money Map **C15** (VM-C15, tier C) | open booked $ aged by `order_date`; cohort/distributional order-month→invoice-month lag · Money Map C15 (`Q-ECON-LEADTIME`) | `portal_orders.order_date`, `portal_invoices.invoice_date`, booked qty | **PARTIAL** (distributional) | Order→invoice join ≈0% (§2) → **cohort lag only, never per-order**; stale/partial feed bloats backlog → cap at RTD. Backorders legitimately stretch lag. | **COMPUTABLE-GATED** |
| 27 | **"Which reps drive the most invoiced revenue?"** (named rep leaderboard) | Rep **VM-R5 / RS-01** (tier C) | rep-grain `SUM(net_amount)` LTM, named via `portal_orders.rep_name` bridge · `RS-01` (`rep_copilot_operator.md`; **prior-year window `pending_query`**) | `net_amount`, `rep_number` (+`portal_orders.rep_name`) | **STRONG** (current-year $ only) | **Rep-identity Tier gate (§7.1):** Tier 2 named, Tier 1 `rep_number` only, Tier 0 suppress rep→revenue. **Never silently drop unmapped reps** (fabricates a leaderboard). Prior-year/YoY per rep is not yet authored — no rep YoY % until `RS-01` prior window ships. | **COMPUTABLE-GATED** |
| 28 | **"Where do we make money geographically?"** (contribution by state) | Money Map **C22** (VM-C22, tier C) | net/freight bridge rolled to `customer_bill_to_state`/ship-to · Money Map C22 (`Q-ECON-GEO`) | `net_amount`, `freight_amount`, `customer_bill_to_state` | **STRONG** (contribution, not profit) | Bill-to ≠ ship-to misplaces freight → prefer ship-to where present; **no cost = contribution map, labeled** (not margin). | **COMPUTABLE-GATED** |
| 29 | **"What's the value of the eCat quote pipeline?"** (pipeline, never sales) | Money Map **C24** (VM-C24, tier C) | `orders.order_type` funnel (the rows eCat-SALE *excludes*); cohort quote→confirmed→invoiced · Money Map C24 (`Q-ECON-PIPELINE`) | `orders.order_type` + per-org state map, `orders` GMV | **PARTIAL** | **Never sum quote $ into sales — the FAL trap** ($37.9M→$0.98M, 97% quotes). Cohort % only; `order_type` vocabulary is org-specific. Label "pipeline," never "sales." | **COMPUTABLE-GATED** |
| 30 | **"Segment our customers by behavior."** (product × price × behavior) | Segmentation (VM-K5 / `Q-SEG-DERIVE`) | per-org label-free clustering of cadence/AOV/breadth/price-band · `segmentation_derivation.md` | `net_amount`, `invoice_date`, `item_number`, `products.category/collection_code`, `products.net_price` | STRONG if built | **🧊 FROZEN (owner directive 2026-06-29, Spine §8).** Method is sound and computable but **not shipped**; no imposed labels/fit scores ever. Do not build in this cycle. | **COMPUTABLE-GATED (FROZEN — do not ship)** |

---

# 3. INFERENTIAL / LLM — list, but NO-GO this cycle

Per program spine (Lane 3, WIP hard rule: `computational insights > inferential OR talk-to-data`) and Money Map §6 park list. These are **not** deterministic and are explicitly parked behind [EBR-772](https://supercatsolutions.atlassian.net/browse/EBR-772).

| Capability | Origin | Why it's not deterministic | Verdict |
|---|---|---|---|
| **Natural-language "talk to your data" / anomaly agent** for the portal | EBR-772 under EBR-775 | LLM query layer over the spine; downstream of a trusted computational surface (spine F6). | **PARKED — no-go now** |
| **Companion / next-best product** (collaborative filtering) | `SIG-OPP-01` | Co-purchase extrapolation — always `[ESTIMATED]`, never a hard $; client-facing only as "Frequently Bought Together." | **PARKED (inferential estimate)** |
| **Predictive year-end forecast / "Quarter-End Oracle" nowcast** | Money Map §6 cut | eCat-as-leading-indicator collides with re-keying (intent ≠ transaction, ~0% join). Deterministic residue already lives in #9 pacing band. | **NO-GO (cut) — use #9 instead** |
| **Peer / percentile benchmarking ("The Mirror"), Economy Index** | Money Map §6 cut | Cross-client; out of single-client Layer-1 scope. | **NO-GO (cut)** |
| **Margin-leak early-warning ML, price-optimization engine** | Money Map §6 cut | Predictive on observational data; also cost-gated (no COGS). Rear-view residue = #17 leakage. | **NO-GO (cut)** |
| **Rep-behavior → coached-dollar fusion** (VM-R-FUSION) | vm_runtime_index | Internal-only; "juxtapose, not fuse" (Rung-4 Option A) — never one blended number. | **PARKED — internal only** |

---

# 4. HARD GAPS — do NOT promise (name the missing column so nobody re-litigates)

Confirmed absent at the schema level (Spine §6.9, full `information_schema` scan 2026-06-29). Each surfaces only as a "With Connected Data" upsell callout — **suppress, never estimate.**

| Capability the portal *cannot* honestly claim | Missing column / feed | Why it's a hard gap | Verdict |
|---|---|---|---|
| **Gross / true margin, margin mix (PVM), margin-weighted concentration** (Money Map C19/C21, VM-C19/C21) | landed **`unit_cost`** per item-period on the invoice line | No cost/COGS column anywhere; `Q-ECON-NETREV` is revenue net of freight, **not margin**. Missing/zero cost silently turns margin into revenue. This is *the one ask* (`SIG-EXT-06`). | **HARD GAP** |
| **AR / DSO / collections / cash / credit risk** | dealer **AR / collections** feed | **Invoiced ≠ collected** (§6.7); `terms` is billed, not collected. Only payment tables are SuperCat's own SaaS billing (`stripe_invoices`), not dealer AR (`SIG-EXT-07`). | **HARD GAP** |
| **"% off list" leakage as a headline** | trustworthy per-org list-price semantics | `products.net_price` is MSRP in some orgs, wholesale in others, not self-identifying (§6.10). "% off list" is **prohibited client-facing** — dispersion (#17) is the only safe form. | **HARD GAP (as %-off-list)** |
| **Parent / corporate-family roll-up** as exact | native **parent/corp key** | `customers.mapped_code` ~0% populated (max 41.5%); name roll-up low-yield/impossible (clli: 1 name across 2,838 codes, §7.2). Only a derived, gated "estimated family" (VM-K6), never exact (`SIG-EXT-03`). | **HARD GAP (exact); derived-only** |
| **Damage / claims by carrier** | carrier/claims feed | No claims data; carrier analytics = freight$/shipments only (§6.9) (`SIG-EXT-08`). | **HARD GAP** |
| **Quoted lead-time miss, inventory aging, market/showroom ROI** | quote-commit dates / dated backorder / market-cost input | No source in feed; market cost is a client input (§6.9). Trade-show ROI (C25) needs both market-coded `order_origin` **and** client show cost. | **HARD GAP** |
| **True cross-channel completeness / "your total business is $X, complete"** | independent second channel feed or client attestation | Single invoice feed can't prove it covers all channels (§6.3). ~1 in 3 orgs cannot be CORROBORATED. Present Total as complete only at CORROBORATED; else single-feed caveat. | **HARD GAP (completeness claim)** |
| **Confirmed competitive displacement** ("shifted $X eCat→phone") | reliable `order_origin` on invoices | `order_origin` lives on booked orders only, bespoke/sparse; can't certify invoice-side channel (§3). Only a hypothesis callout (`SIG-ANOMALY-03`), never "DETECTED." | **HARD GAP (as confirmed); hypothesis-only** |

---

# 5. One-screen: what the Sales Portal can HONESTLY claim vs cannot (for the CTO)

| The portal CAN deterministically claim (STRONG, single-feed caveat) | The portal CANNOT claim (suppress / gate / upsell) |
|---|---|
| **True invoiced topline** that reconciles to the dollar (C1) | Any topline as **"complete/collected"** — single feed, invoiced ≠ collected |
| **Single-account & top-10 concentration + HHI** (C3) | **Exact parent/corporate roll-up** — no native key (derived-only) |
| **Staleness-proof YoY / QoQ** on equal RTD-clamped windows (C10) | **Forecast / predictive nowcast** — pacing **band** only (C9) |
| **Lumpiness / big-deal dependence** honesty guard (C11) | **Peer benchmarking** — cross-client, out of scope |
| **Accounts quietly dying, $-at-risk, who-to-call** (S1) | **Margin-at-risk** — no COGS |
| **Fill / booked→invoiced leakage** within-line (C4) | **Order-to-invoice 1:1 trace** — join ≈0%; cohort grain only |
| **Recurring vs one-time durability** (C7), **$ NRR** (C17) | **AR / DSO / collections / cash risk** — no AR feed |
| **Seasonality / cash calendar** (C8) | **Gross / true margin, margin mix** (C19/C21) — the one ask (`unit_cost`) |
| **Contribution proxy tiering** (C20, labeled proxy) | **True account profit** — proxy only until cost lands |
| **Top products, family YoY, cross-sell gap, dealer cohort flow** (Q-PROD-*/COHORT) | **"% off list" leakage** — org-opaque; dispersion only |
| **Discount leakage as tier-aware dispersion** (C2) — *gated + gut-check* | **Rogue-rep $ without Tier-2 identity + gut-check** |
| **eCat capture in absolute $** (C14) — *rate only at CORROBORATED* | **eCat capture rate on partial/stale feed, or >100%** |
| **Named rep leaderboard** — *only at rep-identity Tier 2* | **Named rep→revenue at Tier 0/1**; silently dropping unmapped reps |
| **eCat vs all-other channel split** (CHAN-1) | **Sub-channel pie** for ~30/41 orgs (order_origin blank/wrong) |
| **Returns drag** — *only where RETURNS_IN_FEED* | **"$0 returns"** on a gross-only feed |
| **Damage-by-carrier, market ROI, inventory aging, NL query** | all **HARD GAP / EBR-772 PARKED** |

**The honest headline for the CTO:** the portal can surface a **computational Intelligence Report of ~16 deterministic answers now** (Section 1), plus ~13 more that are real but **gated per-org** (Section 2) — every one riding `SUM(portal_invoices.net_amount)` at a **STRONG ceiling with a single-feed caveat**. Everything requiring **cost, cash/AR, a channel tag, a parent key, or an LLM** is a named gap (Sections 3–4), not a roadmap ambiguity. Lane 2 Bet C's "True Topline + Concentration" heroes (C1 + C3) are the safest first surface: both are pure invoiced arithmetic, `AGREE 3/3` in the Money Map, and validated live on sarreid/cci.

---

*CAPABILITY (06) complete. Deterministic-now vs gated vs inferential vs hard-gap separated; every computable row cites a canonical query id + doc; every gap names its missing column. Paste to 05-ORCHESTRATOR for review.*
