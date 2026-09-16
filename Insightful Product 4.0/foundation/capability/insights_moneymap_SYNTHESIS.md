# The Money Map — Definitive Synthesis (Layer 1: Commerce Truth Bones)

> ## ⚠️ CAPABILITY / ROADMAP — not executed by `./run.sh`
> **Location:** `foundation/capability/` (shelved 2026-07-13 re-anchor). Do **not**
> load this file to run a report. Design/build-planning synthesis only. Runtime:
> **14** detectors / **24** query IDs. Ground truth:
> [`../WHAT_ACTUALLY_RUNS.md`](../WHAT_ACTUALLY_RUNS.md). Invoiced-net + gates:
> [`../provenance_spine.md`](../provenance_spine.md).

> **What this is.** The merged, de-duplicated build-bible for the **commerce money layer** of SuperCat's insight product — the "bones" of the financial-intelligence stack. It fuses three independent strategist catalogs (Operator, Visionary, Skeptic) into one canonical set of insights about **the economics of how a SuperCat client sells**: revenue, realization, concentration, conversion, returns, channel, margin, and revenue quality. Audience: **owner / CEO / CFO / PE owner**.
>
> **What this is NOT.** Not a moonshot deck, not a forecasting product, not cross-client benchmarking, and not the rep or customer layers. Everything here is grounded in **one client's own order/invoice data** and is buildable-or-suppressible today. Ideas that depend on rep identity/behavior or customer-relationship modeling are **tagged and parked** (Section 6), not designed. Speculative/predictive/peer bets are **cut** (with a record of why, Section 6).
>
> **Grounding.** Every entry maps to the real tables — `orders` (eCat), `portal_orders`/`portal_order_items` (booked, all channels, `order_origin`), `portal_invoices`/`portal_invoice_items` (shipped + billed truth), `sales_data`, `products`, `customers`, `inventories` — and obeys the guardrails in `query_library_v2.md` (eCat-SALE filter, invoiced `net_amount` = truth, Q-PROV-00 confidence gates, Q-CHAN-00 channel gate, date clamps, `$5M` row cap).
>
> **All dollar figures are `[ILLUSTRATIVE]`.** This is a design/build-planning artifact; nothing here is a live client result.

---

## How to read this document

1. **Hero lineup** — the 3–5 insights that lead the product.
2. **Master ranked table** — value × defensibility × feasibility, with build-confidence (where the three artifacts agree).
3. **Canonical Commerce Data-Provenance Map** *(the centerpiece)* — for every insight: what feeds it needs, what we already have, what the client must add, confidence if complete, and degrade-vs-suppress behavior. Plus the **origin taxonomy** and the **capture-vs-attribution** distinction.
4. **Canonical merged insight catalog** — one entry per distinct insight, action-first.
5. **Keep-us-honest appendix** — the invoiced spine, the trap list, the re-keying distortion, and the Danger List.
6. **Parked Layer-2/3 on-ramp** — tagged-only (no design) + what we cut and why.

**Presentation rule (every entry obeys it):** lead with the **DECISION & DOLLAR** (the so-what), then the method, rationale, and caveats as drill-down below. Never bury the action under mechanics.

**Source legend per entry:** `[O]` Operator · `[V]` Visionary · `[S]` Skeptic. `AGREE (3/3)` = highest build-confidence.

---

# 1. HERO LINEUP — what leads the product

These five are the spine of the Money Map. The first four ride **only invoiced `net_amount` and within-table arithmetic** (no cost, no channel tag, no order→invoice join), so they are simultaneously the highest-value and the hardest to argue with. The fifth fuses them into one owner-assigned worklist — the literal "money map."

### HERO 1 — The True Topline `[S]` · `AGREE (3/3 rely on it)`
**DECISION & DOLLAR:** *"The revenue number in your board deck can be off by up to **9×**. Here is the one figure that reconciles to your own Sales Portal to the dollar — `$XXM` invoiced `[ILLUSTRATIVE]` — and the monthly shape behind it."*
This is the denominator of every other money metric. Get it wrong (the `portal_orders.total_amount` habit) and capture rate, concentration, retention, and pacing all silently corrupt. Selling the *correct* topline first is the price of admission to sell everything else.
→ Detail: **C1**.

### HERO 2 — Net Realization & Discount Leakage `[O][V][S]` · `AGREE (3/3)`
**DECISION & DOLLAR:** *"You think you sell at list. You don't — you gave away **`$X`** in discounts and credits last 12 months, and **40% went to accounts that didn't grow in return.** A 2-point realization gain on a `$40M` book is **`$800K` of pure margin** with zero extra units sold. `[ILLUSTRATIVE]`"*
Found money, computable **today** from columns already on every invoice line. The most actionable lever a CFO controls without selling one more unit.
→ Detail: **C2**.

### HERO 3 — Revenue Concentration & Single-Account Risk `[O][V][S]` · `AGREE (3/3)`
**DECISION & DOLLAR:** *"**62%** of your invoiced revenue rides on **9 accounts**; your largest is **`Y%`** of the company and its spend has quietly fallen **18%** — a **`$4.1M`** hole forming in plain sight. `[ILLUSTRATIVE]`"*
The number that sets enterprise value, covenant terms, insurance, and the M&A story. Pure invoiced arithmetic — unimpeachable.
→ Detail: **C3**.

### HERO 4 — Booked→Invoiced Conversion & Fill Leakage `[O][V][S]` · `AGREE (3/3)`
**DECISION & DOLLAR:** *"You earned **`$Y`** in orders and shipped **`$Z`**. The **N%** you dropped is mostly fixable fulfillment — in-stock, reorderable demand — not lost customers. `[ILLUSTRATIVE]`"*
Computed **inside one table** (`quantity_ordered` vs `quantity_invoiced` on the same line), so it sidesteps the order→invoice join problem entirely. Turns a fuzzy "we have stockouts" into a sized buy-inventory decision.
→ Detail: **C4**.

### HERO 5 — The Recoverable Margin Pool `[O composite]` · *fusion of C2 + C4 + C5 + C18*
**DECISION & DOLLAR:** *"**`$R` of margin is sitting in your own transaction data** — here is the ranked, owner-assigned worklist to go get it: renegotiate these discounts, restock these lines, fix these returns, re-price this freight."*
Not a new data ask — a **fusion and attribution** of four independently buildable-now components into a single prioritized cash-recovery campaign, each dollar traceable to a line and an action. This is the artifact the title promises. **Only built once the components are trusted in production, and netted carefully** (a discounted line that also returns is one event, not two).
→ Detail: **COMPOSITE** (after the catalog).

---

# 2. MASTER RANKED TABLE

Ranked by **Value × Defensibility × Feasibility** (each 1–5; 5 = highest/ships-now/board-proof). **Build-confidence** flags where the three artifacts agree: `AGREE 3/3` = all three reached it (highest confidence to build); `2/3` and `1/3` noted. **Cost-gated** rows are the highest-value ideas we cannot ship until a `unit_cost` column lands — that gap is the point, not a flaw.

| # | Canonical insight | V | D | F | Score | Build-confidence | Primary gate / ships when |
|---|---|--|--|--|---|---|---|
| C1 | **True Topline** (canonical invoiced revenue) | 5 | 5 | 5 | **125** | AGREE 3/3 (spine) | `TOTAL_BUSINESS_SOURCE=INVOICES` · now |
| C2 | **Net Realization & Discount Leakage** | 5 | 5 | 5 | **125** | AGREE 3/3 | discount cols populated · now |
| C3 | **Revenue Concentration & Single-Account Risk** | 5 | 5 | 5 | **125** | AGREE 3/3 | invoiced source · now |
| C11 | **Revenue Lumpiness / Big-Deal Dependence** | 4 | 5 | 5 | **100** | 1/3 (S) | invoice grain · now (guardrail) |
| C10 | **Comparable-Window Momentum** (staleness-proof YoY) | 5 | 4 | 5 | **100** | 1/3 (S) | ≥24 fully-billed months · now |
| C4 | **Booked→Invoiced Conversion & Fill Leakage** | 5 | 4 | 4 | **80** | AGREE 3/3 | line-level fill · now |
| C5 | **Returns & Credit-Memo Drag** | 4 | 4 | 5 | **80** | AGREE 3/3 | `RETURNS_IN_FEED=true` · now |
| C9 | **Run-Rate Pacing** (range, not forecast) | 4 | 4 | 4 | **64** | 2/3 (O,S) | ≥24 mo, FULL/STRONG · now |
| C7 | **Revenue Quality: Recurring vs One-Time** | 4 | 4 | 4 | **64** | AGREE 3/3 | ≥2 comparable windows · now |
| C14 | **eCat Capture / Platform Footprint** | 4 | 4 | 4 | **64** | 2/3 (O,S) | `NOT PARTIAL_INVOICE_FEED` · now |
| C8 | **Seasonality & Market-Month Calendar** | 3 | 4 | 5 | **60** | 2/3 (O,S) | ≥2–3 yrs · now |
| C12 | **Price Realization by Account & Off-List Adherence** | 4 | 3 | 4 | **48** | AGREE 3/3 | price-tier/list context · now (descriptive) |
| C16 | **Revenue Composition Strip-Out** (freight/tax/discount) | 3 | 4 | 4 | **48** | 1/3 (S) | header component cols · now |
| C17 | **Net Revenue Retention ($-based)** | 4 | 3 | 4 | **48** | 1/3 (O) | ≥2 yrs, stable keys · now |
| C23 | **New-Introduction Revenue Vitality** | 3 | 4 | 4 | **48** | 1/3 (O) | derived first-sale date · now |
| C20 | **Customer Contribution / Account Margin Tiering** | 5 | 3 | 3 | **45** | 2/3 (O,V) | proxy now; true margin needs cost |
| C13 | **Price-Increase Pass-Through** | 4 | 3 | 3 | **36** | 2/3 (O,V) | list-price history · soon |
| C18 | **Freight & Small-Order Recovery** | 3 | 3 | 4 | **36** | 2/3 (O,V) | charged now; recovery needs carrier cost |
| C6 | **Channel Economics in Dollars** | 4 | 3 | 3 | **36** | AGREE 3/3 (idea) | `CHANNEL_CONFIDENCE≠NONE` (~8/41 orgs) |
| C24 | **Quote-to-Cash Pipeline Value** (eCat) | 3 | 3 | 4 | **36** | 2/3 (O,V) | `order_type` map; label pipeline |
| C15 | **Working Capital: Backlog Aging & Booking-to-Cash Lag** | 3 | 3 | 3 | **27** | 2/3 (O,V) | cohort grain · now |
| C22 | **Geographic Profit Map** | 3 | 3 | 3 | **27** | 1/3 (V) | freight now; margin needs cost |
| C19 | **Margin Pool & Mix** (PVM bridge) | 5 | 2 | 2 | **20** | 2/3 (O,S) | **`unit_cost` feed** (the one ask) |
| C21 | **Margin-Weighted Concentration** | 4 | 2 | 2 | **16** | 1/3 (S) | depends on C19 (cost) |
| C25 | **Market & Trade-Show Dollar ROI** | 3 | 2 | 2 | **12** | 1/3 (V) | market origin tags + client show cost |
| — | **COMPOSITE: Recoverable Margin Pool** | 5 | 4 | 4 | **80** | 1/3 (O) fusion | after C2/C4/C5/C18 trusted |

**Reading the ranking.** The top of the table is the same place all three strategists landed independently (topline, realization, concentration, conversion) — that convergence *is* the build signal. The middle is single-artifact ideas that earn their place because they ride invoiced truth (lumpiness, momentum, composition strip-out, NRR$). The bottom is dominated by **cost-gated** margin work: genuinely the highest *value* (C19 margin mix is V5) but unbuildable until one ERP column arrives — so it ranks low on feasibility and we lobby for the column rather than fake it.

---

# 3. CANONICAL COMMERCE DATA-PROVENANCE MAP  *(THE CENTERPIECE)*

> **Inherits from the Provenance Spine (Tier 0).** The gates, tiers, taxonomy, capture-vs-attribution distinction, and identity rules used below are **defined canonically in [`provenance_spine.md`](provenance_spine.md)** and are not redefined here. This section is the **Commerce domain map** (the `§3.2` table) — it *applies* the Spine to commerce. Where this map names a gate (`Q-PROV-00`, `Q-CHAN-00`, `FEED_COMPLETENESS`, eCat-SALE, date clamps, `$5M` cap, `invoiced ≠ collected`) or a confidence tier (`FULL/STRONG/PARTIAL/LIMITED/NONE`), see the Spine for the authoritative definition and behavior. No logic changed in this refactor — only the source of truth was lifted up a tier.

This is the deliverable's heart: **the complete commerce money model, and exactly what each client must hand us to light up each part.** Read it as a contract — "give us *this* feed, and *this* insight lights up at *this* confidence; withhold it, and here is precisely how the insight degrades or goes dark."

**Two structural facts gate the whole map (both code-verified, see Appendix):**
- **The order→invoice header join is ≈0%** and orders are re-keyed/edited/merged between iPad and ERP — so any booked↔invoiced work is **cohort / line / quantity grain**, never a 1:1 trace.
- **`order_origin` is bespoke and sparse** (~8 of 41 live orgs usable; only `cci` tags eCat reliably) — so channel-level cuts are gated by `Q-CHAN-00` and otherwise degrade to "eCat vs all other channels."

**Confidence vocabulary** (from `Q-PROV-00`): `FULL` > `STRONG` > `PARTIAL` > `LIMITED` > `NONE`. **The binding rule: a money number is shown at its lowest input's confidence, or not at all.**

> ### ⚠️ 3.0 FEED-COMPLETENESS — the assumption we cannot prove (empirical, validated 2026-06-26)
>
> **The flaw this section fixes.** The rest of this map originally said we "HAVE" the invoiced topline at `FULL` confidence because `net_amount` "reconciles to the client's own Sales Portal." **That reconciliation is circular** — the Sales Portal reads *the same feed rows we do* (the validation worksheet states the dashboard is **not** ground truth). If a client's ERP exports only part of its book (e.g. direct + eCat but not EDI), the dashboard is *also* partial, and the two match perfectly **while both are wrong**. We were conflating two different things:
>
> | Dimension | What `Q-PROV-00`'s FULL/STRONG actually measures | What it does **NOT** measure |
> |---|---|---|
> | **Internal-consistency confidence** | `net_amount` populated, dates sane, fresh, returns present, default reconciliation | — |
> | **Feed-completeness confidence** *(new — was missing)* | — | **Whether the feed contains ALL channels' invoices.** No client sells only through eCat; the invoiced book is mostly WEB / EDI / direct / CS / market business that carries **no channel tag** and that we have **no independent source to check against.** |
>
> **Why `order_origin` does NOT rescue this** (the user's instinct, corrected): `order_origin` lives on `portal_orders` (booked orders), **not on `portal_invoices`**, so it can never certify invoice completeness. And empirically it is unusable for most orgs anyway (21-org run): **blank for 8/21** (`clli`,`shl`,`heb`,`lpf`,`clm`,`vic`,`pf`,`bcf`), **single-bucket for 2** (`bri`,`kll`), and **actively wrong where present** — `scw` is ~79% eCat by our own truth but has **no eCat bucket** in origin; `wwjc`'s "eCAT Order" origin shows $2.3M vs our confirmed $9.2M (under-tags 4×). Only `cci` tags reliably.
>
> **The one real corroboration we DO have: booked-vs-invoiced triangulation.** Where the ERP feeds a *complete* `portal_orders`, LTM booked ≈ LTM invoiced (two independently-fed ERP tables agreeing within ~10–25% — booked slightly higher, as expected since not all booked ships). That agreement is meaningful evidence the invoice feed is plausibly complete. Where the order feed is partial, the ratio collapses and we have **no second opinion**. **Caveat that still bites:** if the ERP omits a whole channel from *both* orders and invoices, the two still agree and we remain blind. So corroboration raises confidence; it never proves completeness.
>
> **New gate — `FEED_COMPLETENESS`** (run alongside `Q-PROV-00`; sets the label every Total must carry):
> | Label | Test | Behavior |
> |---|---|---|
> | **CORROBORATED** | `0.90 ≤ LTM booked / LTM invoiced ≤ 1.30`, feed fresh, eCat not > invoiced | Report Total; label "cross-checked against booked orders," completeness **STRONG** (not proven) |
> | **UNVERIFIED — SINGLE FEED** | order feed partial/absent (ratio < 0.9 or no orders) | **Report Total only with an explicit "single-source; channel completeness unverified" disclaimer**, cap completeness at **PARTIAL** |
> | **PROVABLY INCOMPLETE** | confirmed eCat LTM > 1.05 × invoiced LTM (`PARTIAL_INVOICE_FEED`) | **Suppress the Total**; report the completeness gap as the finding |
> | **STALE** | days since last invoice > 45 | Cap window at `REPORT_THROUGH_DATE`; never run a trailing window into empty months |
> | **DEAD / NONE** | no recent invoices, or `sales_data` $0 | **Suppress**; never print `$0` or a years-stale "total" |
>
> **What the 21-org run found** (LTM, `[ILLUSTRATIVE-from-live]`; `booked/inv` and `eCat/inv` are the diagnostics):
>
> | Org | Invoiced LTM | booked/inv | eCat/inv | Completeness verdict |
> |---|--:|--:|--:|---|
> | `ufi` | $134.2M | 1.03 | 0.10 | CORROBORATED (gross-only) |
> | `kll` | $87.4M | 1.05 | 0.005 | CORROBORATED (origin single-bucket; gross-only) |
> | `cci` | $70.1M | 1.25 | 0.11 | CORROBORATED + reliable origin (best case) |
> | `clc` | $58.9M | 1.08 | 0.01 | CORROBORATED |
> | `shl` | $49.4M | 1.02 | 0.01 | CORROBORATED (origin blank) |
> | `scw` | $44.8M | 1.07 | 0.79 | CORROBORATED (origin omits eCat — do not trust channel split) |
> | `clli` | $44.6M | 1.07 | 0.003 | CORROBORATED (origin blank) |
> | **`pf`** | $44.3M | **0.26** | 0.37 | **UNVERIFIED — single feed** (order feed partial) |
> | `clm` | $39.6M | 1.02 | 0.01 | CORROBORATED (net_amount 98.9% — just under FULL) |
> | `gh` | $38.6M | 1.09 | 0.71 | CORROBORATED |
> | **`sc`** | $34.1M | 0.99 | **1.27** | **PROVABLY INCOMPLETE** — confirmed eCat exceeds invoiced; suppress Total |
> | **`mhc`** | $28.8M* | 1.10 | 0.02 | **STALE** — last invoice 186 days ago; window understated |
> | `lpf` | $26.2M | 1.05 | 0.17 | CORROBORATED (gross-only) |
> | **`ril`** | $25.3M | **0.68** | 0.02 | **UNVERIFIED — single feed** |
> | `bri` | $21.3M | 0.89 | 0.17 | CORROBORATED (borderline; origin single-bucket) |
> | **`jyc`** | $20.1M | **0.17** | 0.34 | **UNVERIFIED — single feed** (gross-only) |
> | **`bcf`** | $19.8M | **0.11** | 0.35 | **UNVERIFIED — single feed** (≈8.9× order undercount; gross-only) |
> | `wwjc` | $18.0M | 1.09 | 0.51 | CORROBORATED (origin under-tags eCat 4×; gross-only) |
> | `sarreid` | $15.7M | 1.00 | 0.13 | CORROBORATED (gross-only) |
> | `vic` | $8.7M | 1.13 | 0.003 | CORROBORATED (origin blank) |
> | **`heb`** | — | — | — | **DEAD** — last invoice 2020-06; suppress Total entirely |
>
> **Headline for the deck:** across 21 real orgs, **~14 are completeness-CORROBORATED, but ~7 (1 in 3) are not** — 4 single-feed/unverified, 1 provably incomplete (`sc`), 1 stale (`mhc`), 1 dead (`heb`). **We must therefore stop presenting any Total as definitively complete.** Every Total ships with its `FEED_COMPLETENESS` label, and we suppress rather than guess on PROVABLY-INCOMPLETE / DEAD.
>
> **Two more honest gaps this run surfaced:**
> - **Invoiced ≠ paid/collected.** We have *invoiced* dollars (shipped + billed). There is **no AR / cash-receipt feed** in the schema, so we can never say "collected." Every Total is "invoiced," explicitly, never "revenue you've banked."
> - **Gross-only is more common than the source artifacts implied.** Zero credit memos LTM observed for `ufi`, `kll`, `clm`, `lpf`, `jyc`, `bcf`, `wwjc`, `sarreid` (and `pf` ≈ gross with 1). Net-of-returns must be **suppressed** for all of these, not just the original four.

### 3.1 The model in one picture — what we already get vs. what we must be given

| Feed | Table / columns | Status today | Unlocks |
|---|---|---|---|
| **Invoiced sales (the spine)** | `portal_invoices.net_amount`, `invoice_date`, `customer_bill_to_number`, `rep_number`, `customer_bill_to_state` | **HAVE the feed** (~100% populated where invoices exist) — but **completeness across channels is unverified** unless `FEED_COMPLETENESS=CORROBORATED` (§3.0) | C1, C3, C7, C8, C9, C10, C11, C17 |
| **Invoice line economics** | `portal_invoice_items`: `unit_price`, `unit_price_discount`, `extended_price_discount`, `quantity_invoiced`, `quantity_ordered`, `quantity_returned` | **HAVE** | C2, C4, C5, C12, C16 |
| **Invoice header components** | `portal_invoices`: `discount_amount`, `freight_amount`, `tax_amount` | **HAVE (where itemized)** | C16, C18 |
| **eCat orders (confirmed)** | `orders` + eCat-SALE filter | **HAVE** | C14, C24 |
| **Booked orders (all channels)** | `portal_orders` / `portal_order_items` | **HAVE** | C4, C15, C24 |
| **List / reference price** | `products.net_price`, customer `DefaultPriceCode`, price-level table | **PARTIAL** (blank/0 for some orgs) | C12, C13 |
| **Channel tag** | `portal_orders.order_origin` + per-org canonical map | **SPARSE** (~8/41; only `cci` eCat-reliable) | C6, C25, taxonomy |
| **Returns** | credit memos (`net_amount<0`) and/or `quantity_returned` | **PER-ORG** (gross-only: `ufi`,`pf`,`jyc`,`bcf`) | C5, and the "net" half of C2/C20 |
| **Cost / COGS** | landed `unit_cost` per item-period on the invoice line | **MISSING — the one ERP column to lobby for** | C19, C21, true-margin half of C20/C22 |
| **Carrier freight cost** | external freight-cost feed/model | **MISSING** | recovery-% half of C18 |
| **List-price history** | dated `products.net_price` effective dating | **MISSING** | clean version of C13 |
| **Show cost** | client-supplied per-market cost | **CLIENT INPUT** | C25 |

### 3.2 The provenance map — one row per insight

> Columns: **Insight** · **Fields/feeds required** · **What we already get** · **What the client must additionally provide** · **Confidence if complete** · **Behavior if a piece is missing (degrade vs suppress)**

| Insight | Fields/feeds required | What we already get | Client must additionally provide | Confidence if complete | If a piece is missing |
|---|---|---|---|---|---|
| **C1 True Topline** | `portal_invoices.net_amount` + dates | The feed (internally clean) — **not a verified-complete book** (§3.0) | A complete `portal_orders` feed (for booked-vs-invoiced corroboration) and/or a one-time client confirmation of which channels their ERP export covers | **FULL on internal consistency; completeness only STRONG when `CORROBORATED`** | `PROVABLY INCOMPLETE` (eCat>invoiced, e.g. `sc`) → **suppress**. `UNVERIFIED—SINGLE FEED` (e.g. `pf`,`jyc`,`bcf`,`ril`) → report with "single-source; channel completeness unverified" disclaimer, cap PARTIAL. Stale (`mhc`) → cap at `REPORT_THROUGH_DATE`. Dead (`heb`) / `NONE` / `$0 sales_data` (`da`) → **suppress, never print a `$0` total**. Gross-only → "gross invoiced," cap STRONG. |
| **C2 Net Realization & Discount Leakage** | line `unit_price`, `unit_price_discount`, `extended_price_discount`, `quantity_invoiced`; `quantity_returned` for the net half | All of it | Nothing | **FULL** (discount); **STRONG** (net-of-returns) | Org bakes discount into `unit_price` (zeroed discount cols) → leakage reads false-0; **detect via discount-col fill-rate, suppress the leakage claim** if unpopulated. Gross-only → show discount, **suppress net-of-returns**. |
| **C3 Concentration & Single-Account Risk** | `net_amount` by `customer_bill_to_number` (+ `_state`, `rep_number`) | All of it | Optional: parent→child account map (firmographics) | **FULL** | No parent map → measure **billing entities**, state the grain (real concentration is *worse*, never overstated). `ORDERS`/`SALES_DATA` source → cap PARTIAL/LIMITED. |
| **C4 Booked→Invoiced Conversion & Fill** | `portal_order_items`/`portal_invoice_items` `quantity_ordered` & `quantity_invoiced` (same line); `quantity_returned`; `inventories` for stockout split | Quantities + inventory | Nothing (fresher feed sharpens it) | **STRONG** | Stale feed makes will-still-ship lines look leaked → clamp to fully-aged cohorts at `REPORT_THROUGH_DATE`. Non-OVERLAPS org → **do not sum order+invoice tables** (double-count); keep within-line fill. Split structural (discontinued) vs addressable. |
| **C5 Returns & Credit-Memo Drag** | `net_amount<0` and/or `quantity_returned` | Both signals where present | Returns actually fed into the warehouse | **STRONG** | `RETURNS_IN_FEED=false` → **suppress/relabel** "returns not represented," **never imply 0% returns**. |
| **C6 Channel Economics ($)** | `portal_orders.order_origin` + maintained per-org map; `orders` for eCat truth; `net_amount` denominator | eCat truth + denominator | A maintained `order_origin→channel` map; reliable origin tagging | **STRONG** (≤~8 orgs) | `CHANNEL_CONFIDENCE=NONE` (~30 orgs blank) → **suppress sub-channel split; show "eCat vs all other" only.** Over/under-tagged eCat (`ril` 12×, `wwjc` 0.25×) → overlay eCat from `orders`, never from origin. Magnitudes are booked → caption "channel mix from booked orders, applied to invoiced total." |
| **C7 Revenue Quality: Recurring vs One-Time** | `net_amount` by customer over ≥2 comparable windows | All of it | Nothing | **STRONG** | <2 windows or `LIMITED` source → **suppress**. Seasonal buyer (one market order/yr) looks one-time → classify on multi-year cadence; pair with C11. |
| **C8 Seasonality & Market Calendar** | multi-year monthly `net_amount`; optional `order_origin` market codes | Invoiced series | Optional market tags | **STRONG** | <2–3 yrs → **suppress**. One-off big order skews a month → median-of-years per month. Invoicing lag shifts a market's revenue → caveat booking-vs-shipping. |
| **C9 Run-Rate Pacing** | multi-year `net_amount`; `portal_orders` backlog; C6/C7/C11 inputs | Invoiced + backlog | Nothing | **STRONG** (range only) | <24 mo or lumpy → widen/withhold band. Corrupt far-future dates poison buckets → date clamp. **Always a range, never a point**; framed pacing, not prediction. |
| **C10 Comparable-Window Momentum** | ≥24 contiguous billed months of `net_amount` | All of it | Nothing | **STRONG** | Stale tail → current window runs into empty months → fake crash; **both windows must end at `REPORT_THROUGH_DATE`.** `LIMITED`/no-date source → **suppress trend.** |
| **C11 Revenue Lumpiness / Big-Deal** | invoice-grain `net_amount` | All of it | Nothing | **FULL** | Separate credit memos from the size distribution. Legit large contract orders → annotate, don't auto-discount. *(This metric is itself the suppression check for others — rarely suppressed.)* |
| **C12 Price Realization by Account / Off-List** | line realized price; `products.net_price`; customer `DefaultPriceCode`/price-level table | Realized price | A clean list/reference price and the price-level table | **STRONG** | `net_price` blank/0 → **suppress off-list claim.** Tiered/contract pricing looks like leakage → net out known levels first, present "below reference," not "unauthorized"; **suppress the recoverable-$ claim** where tiers unknown (show spread descriptively). |
| **C13 Price-Increase Pass-Through** | realized price over time; a list-change date / `net_price` history | Realized price over time | Dated list-price history or an announced-increase date | **STRONG** | No price history → use realized-price step-change as proxy, label it. Mix shift masquerades as pass-through → control for category/item mix. |
| **C14 eCat Capture / Platform Footprint** | confirmed eCat GMV (eCat-SALE) ÷ invoiced total | Both | Nothing | **STRONG** | `PARTIAL_INVOICE_FEED` (eCat LTM > 1.05× invoiced LTM, e.g. `sc` 126.9%) → **suppress; report the completeness gap as the finding; never publish >100% or fall back to order-header denominator.** Stale → cap window. |
| **C15 Working Capital: Backlog Aging & Lag** | `portal_orders.order_date`; `portal_invoices.invoice_date`; open booked qty; `inventories.next_scheduled_receipt_date` | Dates + backlog | Nothing | **PARTIAL** | No 1:1 join → **distributional/cohort lag only**, present as such. Backorders legitimately stretch lag → pair with C4. Stale/partial feed bloats backlog → cap at `REPORT_THROUGH_DATE`. |
| **C16 Revenue Composition Strip-Out** | `net_amount` vs `freight_amount`, `tax_amount`, `discount_amount` (header) | Header columns | Nothing | **STRONG** | Org folds freight into line price (component cols zero) → **suppress strip-out, report topline as-is.** Don't double-subtract a discount already netted into `net_amount`. |
| **C17 Net Revenue Retention ($)** | `net_amount` by customer, ≥2 yrs, stable keys | All of it | Optional: stable/parent customer keys | **STRONG** | Customer-number changes/bill-to splits → fake churn/expansion; reconcile keys, present a band. Gross-of-returns slightly inflates retention. |
| **C18 Freight & Small-Order Recovery** | `freight_amount` charged; order size; carrier cost for recovery % | Charged freight + order size | A carrier freight-cost feed/model | **STRONG** (charged); cost completes recovery % | Bundled freight (col zero) → looks like 100% give-away → **detect fill-rate, present "itemized freight only."** No cost side → report *charged* freight trends, not recovery %. Exclude free-freight promos/prepaid. |
| **C19 Margin Pool & Mix** | `portal_invoice_items` + **landed `unit_cost`** per item-period + `products` | Everything except cost | **Verified, current, landed `unit_cost`** | **STRONG** if cost clean | No/stale/zero cost silently turns margin into revenue → **exclude any item without verified cost; never impute. If cost coverage <90% of invoiced $, show revenue mix only, flag "margin pending cost feed."** Trend/mix decomposition survives imperfect cost; level does not — label separately. |
| **C20 Customer Contribution / Margin Tiering** | C2 + C5 + C18 components (now); `unit_cost` (later) | Discount/returns/freight components | Cost for true gross margin | **STRONG** (proxy); FULL with cost | Without cost it is a **contribution proxy, not gross profit** — label precisely. Inherits every C2/C5/C18 gate. |
| **C21 Margin-Weighted Concentration** | C19 margin by `customer_bill_to_number` | — | Same `unit_cost` as C19 | **STRONG** if cost clean | **Suppress whenever C19 is suppressed.** Bad cost inverts the ranking — gate hard. |
| **C22 Geographic Profit Map** | price/freight/(cost) bridge rolled to `customer_bill_to_state`/region | Revenue + freight by geo | Cost (full margin); prefer ship-to geo | **STRONG** (contribution); FULL with cost | Bill-to ≠ ship-to misplaces freight → prefer ship-to where present. Without cost → contribution map, labeled. |
| **C23 New-Introduction Revenue Vitality** | line `net_amount` for items with derived first-sale date (or `products.new_item`) | Invoice lines | Nothing (prefer derived date over stale flag) | **STRONG** | `new_item` flags go stale (never cleared) → overstate vitality → **prefer derived first-sale date.** |
| **C24 Quote-to-Cash Pipeline Value** | `orders` full `order_type` spectrum + timestamps; `portal_invoices` downstream | eCat order states + invoices | Per-org `order_type` state map | **PARTIAL** | **Never sum quote $ into sales (the FAL trap).** Conversion can't be traced 1:1 (join ≈0%) → cohort % only, heavily caveated. Always label "pipeline," never "sales." |
| **C25 Market & Trade-Show $ ROI** | market-coded `order_origin`; conversion (C4); reorder value; show cost | Booked/invoiced + conversion | Market origin tags **and** per-market show cost | **PARTIAL** | Market codes exist for few orgs (gated by `Q-CHAN-00`) and show cost is a client input → **suppress** without both. Conversion uses cohort grain (C4 caveats). |

### 3.3 The Commerce Origin Taxonomy (explained)

Every dollar a client books originates in one of four worlds:

| # | Origin | How it reaches the ERP | Can we see it? |
|---|---|---|---|
| **(a)** | **SuperCat iPad orders** | Rep writes on iPad → sent to HQ → **audited and manually re-keyed** into ERP | In `orders` (our side) as *intent*; in the ERP **indistinguishable** once re-keyed unless `order_origin` is tagged |
| **(b)** | **SuperCat B2B-commerce orders** | eCat Online / portal → ERP (often still re-keyed) | Same as (a) |
| **(c)** | **Other online orders** | Client's own web/EDI storefront → ERP | Only via `order_origin` tag |
| **(d)** | **Other: EDI / phone / email / manually-keyed** | CS or EDI directly into ERP | Only via `order_origin` tag |

**The hard truth:** from the ERP's vantage, (a)–(d) are **often indistinguishable once re-keyed**, because the re-keying strips the channel of origin. The only way to separate them at the ERP/invoice grain is a reliable `order_origin` tag — which is **bespoke and sparse: ~8 of 41 live orgs carry usable multi-channel origin, and only `cci` tags eCat reliably** (`ril` over-tags eCat 12×, `wwjc` captures 0.25×). This is why the channel split (C6) is a gated luxury, not a default, and why "eCat vs all other channels" (Q-CHAN-05) is the headline we can almost always defend while the full pie (Q-CHAN-10) is the one we usually suppress.

### 3.4 Capture vs. Attribution — the distinction we must never blur

These are **two different questions**, and conflating them is the fastest way to lose a CFO's trust:

| | **eCat CAPTURE** | **eCat ATTRIBUTION / INFLUENCE** |
|---|---|---|
| **Question** | What *provably flowed through our rails*? | How much of ERP revenue did we *drive*? |
| **Basis** | Confirmed eCat GMV (eCat-SALE) ÷ invoiced total (Q-CHAN-05 / Q-45) | An estimate of eCat's influence on the broader ERP book |
| **Status** | **A fact** (gated by `PARTIAL_INVOICE_FEED`) | **A confidence-gated ESTIMATE — never a fact** |
| **When valid** | Whenever the invoice feed is complete | Only with reliable `order_origin` tagging (≈`cci`-grade) |
| **Default behavior** | **Report** as capture | **Suppress** absent reliable tagging; never dress an estimate as capture |

**The re-keying distortion makes this unavoidable.** Because almost nothing flows iPad→ERP directly — a rep's order is audited and manually re-keyed, then edited/merged — an eCat order is **rep-submitted intent, not a transaction.** Commercial truth lives only on the ERP/invoice side. So:
- **Capture** (C14) is honest: it measures *our confirmed GMV* against *their invoiced truth*, with the ordered-vs-invoiced basis caveat attached. **But the denominator (invoiced total) is only as complete as §3.0 allows** — if the invoice feed is `UNVERIFIED`/`PROVABLY INCOMPLETE`, capture % is computed against a partial book and **overstates** our share; gate capture on `FEED_COMPLETENESS ∈ {CORROBORATED}` (and never publish >100%, the `sc` case).
- **Attribution** ("eCat drove $X of your ERP revenue") requires knowing which re-keyed ERP lines *originated* in eCat — which needs the tag we mostly don't have. Present it only as a clearly-labeled, confidence-gated estimate, and only where `order_origin` reconciles.

---

# 4. CANONICAL MERGED INSIGHT CATALOG

> One entry per distinct insight, synthesized (not concatenated) from the best of all three artifacts. Each leads with **DECISION & DOLLAR**, then drills down. `AGREE 3/3` marks the highest-confidence builds. Every entry obeys the Appendix rules.

---

### C1 — True Topline (Canonical Invoiced Revenue) `[S]` · `AGREE 3/3 rely on it` · **Rank 1**
**DECISION & DOLLAR:** *"Here is the one revenue number that reconciles to your own Sales Portal to the dollar — and the monthly shape behind it. The `portal_orders` figure you may have seen can be off by up to 9×."*
- **Question:** What did we actually sell (ship + bill) this period, across every channel?
- **Method:** `SUM(COALESCE(net_amount, Σ line discount-adjusted amount))` over `portal_invoices`, by month/quarter/LTM; credit memos (`net_amount<0`) included as legitimate negatives. Date-clamp `2010-01-01 .. CURRENT_DATE+90d`.
- **Defensibility / failure / suppression:** `net_amount` reproduces the warehouse sales fact and is ~100% populated (code-verified) — this proves **internal consistency, not cross-channel completeness** (§3.0; the dashboard "reconciliation" is circular). **FULL on internal consistency** only when fresh, contiguous, returns-in-feed, default reconciliation (`OVERLAPS`+`20180720`); **completeness is a separate label** (`FEED_COMPLETENESS`): present the Total as definitively complete only when `CORROBORATED` (booked≈invoiced), otherwise attach a "single-source; channel completeness unverified" disclaimer. **Suppress** when `PROVABLY INCOMPLETE` (eCat>invoiced, `sc`), `DEAD` (`heb`), or `TOTAL_BUSINESS_SOURCE=NONE`; never print a `$0`/years-stale "total" (the `da`/`heb` phantoms). Stale → cap at `REPORT_THROUGH_DATE`. Gross-only → "gross invoiced sales," cap STRONG. **Always label "invoiced," never "collected"** — there is no AR/cash feed.
- **Why it's the spine:** it is the denominator of every other money metric; being right here is the price of admission.
- **Who pays:** CEO / CFO.

### C2 — Net Realization & Discount Leakage `[O][V][S]` · `AGREE 3/3` · **Rank 2**
**DECISION & DOLLAR:** *"You gave away `$X` in discounts and credits last 12 months; the **20% of accounts and reps eating 60% of it have no volume growth to justify it.** A 2-point realization gain on a `$40M` book = `$800K` of pure margin. `[ILLUSTRATIVE]`"*
- **Question:** Where is realized price below list, who grants it, and is the discount buying us anything?
- **Method:** Per line — **gross** = `quantity_invoiced × unit_price`; **net** = `quantity_invoiced × (unit_price − unit_price_discount) − extended_price_discount`; **leakage** = gross − net; **realized %** = net/gross. Present as a **list→net waterfall** (base discount → line discount → returns) and roll up by `customer_bill_to_number`, `rep_number`, `category_code`. Cross-plot discount% vs the account's YoY growth — the "high-discount / no-growth" quadrant is the recoverable pool.
- **Defensibility / failure / suppression:** Clean within-table arithmetic; warehouse prorates line discounts to header `net_amount` (verified). **Failure:** an org that bakes discount into `unit_price` (zeroed discount cols) reads false-0 leakage → **detect via discount-col fill-rate before publishing; suppress if unpopulated.** Gross-only orgs → show discount, **suppress net-of-returns.** Frame as "realized vs reference price," never "overcharging."
- **Who pays:** CFO / VP Sales — directly recoverable margin; re-arms discount policy.

### C3 — Revenue Concentration & Single-Account Risk (HHI) `[O][V][S]` · `AGREE 3/3` · **Rank 3**
**DECISION & DOLLAR:** *"**62%** of revenue rides on **9 accounts**; your #1 is `Y%` of the company and quietly fell **18%** — a `$4.1M` hole forming. Here's your exposure by account, rep, category, and geography. `[ILLUSTRATIVE]`"*
- **Question:** How concentrated — and therefore how fragile — is the revenue base, and which top account is shrinking?
- **Method:** `SUM(net_amount)` by `customer_bill_to_number` over LTM; top-1/5/10 share, **Herfindahl index (HHI)**, Pareto curve, and a **walk-away sensitivity** (revenue if account N reverts to its own trailing run-rate or zero). Repeat by `rep_number` (key-person risk) and category; layer geography from `customer_bill_to_state`. Decline signal compares two complete comparable windows ending at `REPORT_THROUGH_DATE`.
- **Defensibility / failure / suppression:** Pure invoiced arithmetic; stable keys. **Failure:** multiple bill-to codes for one parent **understate** concentration (it's worse, never overstated) → state the grain; offer optional parent roll-up. Gross-of-returns → cap STRONG, label "gross invoiced." `ORDERS`/`SALES_DATA` source → cap PARTIAL/LIMITED.
- **Who pays:** Owner / CFO / board / lenders / acquirers — sets enterprise value, covenants, the M&A narrative.

### C4 — Booked→Invoiced Conversion & Fill Leakage `[O][V][S]` · `AGREE 3/3` · **Rank 6**
**DECISION & DOLLAR:** *"You earned `$Y` in orders and shipped `$Z`. The **N% you dropped** is mostly fixable fulfillment — in-stock, reorderable demand — not lost customers. `[ILLUSTRATIVE]`"*
- **Question:** How much won demand never converts to cash, and where does it leak (stockout, cancel, substitution, return)?
- **Method:** Within `portal_invoice_items`/`portal_order_items` — **fill rate** = `SUM(quantity_invoiced)/SUM(quantity_ordered)` on the **same line** (no header join); **leaked $** = (ordered − invoiced) × `unit_price`. Segment by `item_number` (join `inventories` to split *stockout* from *cancel*) and category. Add the post-ship layer from `quantity_returned`. Annualize. Open backlog = `quantity_ordered − quantity_invoiced`(+`quantity_backordered`) × price.
- **Defensibility / failure / suppression:** Its strength is that both quantities live on one line — **no order→invoice join.** **Failure:** stale feed makes will-still-ship lines look leaked → clamp to fully-aged cohorts at `REPORT_THROUGH_DATE`. Non-OVERLAPS orgs → **never sum order+invoice tables (double-count); keep within-line fill.** Split structural (discontinued) vs addressable (reorderable).
- **Who pays:** CFO / COO / demand planning.

### C5 — Returns & Credit-Memo Drag `[O][V][S]` · `AGREE 3/3` · **Rank 7**
**DECISION & DOLLAR:** *"Gross sales say `$A`; after returns and credits you kept `$B`. The N-point drag is concentrated in **M items and K accounts** — and it's a product-quality early-warning. `[ILLUSTRATIVE]`"*
- **Question:** How much booked revenue reverses, and where does it concentrate?
- **Method:** Return rate $ = `SUM(net_amount WHERE net_amount<0)` / gross positive, plus line `SUM(quantity_returned × unit_price)`. Rank by `item_number`, `category_code`, `customer_bill_to_number`; trend monthly to catch a worsening defect/fit problem.
- **Defensibility / failure / suppression:** Requires the org to actually **feed credits/returns** (`RETURNS_IN_FEED=true`). **Failure:** gross-only orgs (`ufi`, `pf`, `jyc`, `bcf`) read a silent 0% → **suppress/relabel "returns not represented in your feed," never "$0 returns."** Timing mismatch (return posts later than sale) distorts short windows.
- **Who pays:** CFO / Ops / Quality.

### C6 — Channel Economics in Dollars `[O][V][S]` · `AGREE 3/3 (idea), heavily gated` · **Rank 18**
**DECISION & DOLLAR:** *"Here's the actual revenue flowing through eCat vs every other channel — in dollars, not vibes. EDI may be 35% of volume but a smaller share of margin; eCat carries the highest AOV and lowest discount. `[ILLUSTRATIVE]`"*
- **Question:** Which channels carry the revenue (and, with cost, the margin)?
- **Method:** **Level 1 (almost always defensible):** eCat (confirmed `orders`) vs non-eCat as a share of invoiced total (Q-CHAN-05). **Level 2 (rare):** split the non-eCat slice by `order_origin` via a **maintained per-org map** (Q-CHAN-10), expressed as **% mix applied to the invoiced total**, captioned "channel mix from booked orders." Overlay realized-price% (C2) and margin (C19, when cost lands).
- **Defensibility / failure / suppression:** Gate on `Q-CHAN-00` (`CHANNEL_CONFIDENCE≠NONE`: ≥60% booked $ attributed, ≥2 origins, ≥25 rows). **Failure:** `order_origin` blank for ~30 orgs; over/under-tagged eCat (`ril` 12×, `wwjc` 0.25×) → **overlay eCat from `orders` truth, never read it from origin.** **Suppress the sub-channel pie for NONE-tier orgs — present "eCat vs all other channels" only.** Magnitudes are booked, not sold.
- **Adjudication:** Visionary's confident channel-matrix optimism is **overruled by the Skeptic's gate** — the full pie is suppressed for ~33 of 41 orgs; the eCat-vs-all-other headline is what ships by default.
- **Who pays:** CEO / CRO.

### C7 — Revenue Quality: Recurring vs One-Time `[O][V][S]` · `AGREE 3/3` · **Rank 8**
**DECISION & DOLLAR:** *"Only **58%** of revenue is durable reorder business; the rest is one-and-done you re-win every year — your 'growth' is lumpier than it looks. `[ILLUSTRATIVE]`"*
- **Question:** How much of the book is durable, reorder-driven revenue vs fragile one-time buys?
- **Method:** Classify each account's revenue as **recurring** (invoiced in both this and the prior comparable window / ≥2 periods) vs **one-off**; report the $ split and trend. Layer reorder-interval stability as a quality grade. *(Revenue-composition, not churn — dollar durability, not attrition.)*
- **Defensibility / failure / suppression:** ≥2 full comparable windows ending at `REPORT_THROUGH_DATE`. **Failure:** short history makes everything look "new"; **seasonal buyers (one market order/yr) look one-time but are durable** → classify on multi-year cadence; pair with C11. **Suppress** <2 windows or `LIMITED` source.
- **Who pays:** CFO / board / investors — durable-revenue share drives the multiple.

### C8 — Seasonality & Market-Month Calendar `[O][S]` (+V partial) · **Rank 10**
**DECISION & DOLLAR:** *"Two market months drive a third of your year — shape your cash, inventory, and staffing around that curve (you probably aren't). `[ILLUSTRATIVE]`"*
- **Question:** What is the true intra-year revenue rhythm, and where are the cash peaks/troughs?
- **Method:** Multi-year monthly `net_amount` normalized to a **month-share curve**; identify recurring market/showroom spikes (cross-ref `order_origin` market codes where present); peak-to-trough swing → cash calendar; note booking-vs-shipping lead/lag.
- **Defensibility / failure / suppression:** ≥2–3 years; date-clamped. **Failure:** a one-off big order distorts a month → use **median-of-years per month**, not a single year; invoicing lag shifts a market's revenue → caveat. **Suppress** <2 years.
- **Who pays:** CFO / Ops — inventory build, credit-line timing, staffing.

### C9 — Run-Rate Pacing (a range, not a forecast) `[O][S]` · **Rank 9**
**DECISION & DOLLAR:** *"At today's pace plus your open book, you land the year at `$W ± band` — that's X% off last year, and you can see the gap building now, not in December. A pacing line, not a crystal ball. `[ILLUSTRATIVE]`"*
- **Question:** Where do we finish the period if current dynamics hold, adjusted for our own seasonality?
- **Method:** Seasonally-adjusted trailing run-rate (apply prior years' month-share to YTD actuals) + open backlog (C4, discounted by historical fill) + recurring-base floor (C7); express as a **band** widened by lumpiness (C11). Hard-cap the window at `REPORT_THROUGH_DATE`.
- **Defensibility / failure / suppression:** **Framed as pacing, explicitly NOT a prediction.** ≥24 months, `FULL`/`STRONG`. **Failure:** corrupt far-future dates poison buckets (`clm` yr 4107, `jyc` 2032) → clamp; extrapolating lumpy/short history → widen band. **Suppress a point estimate always — only ever a band.**
- **Adjudication:** Visionary's **"Quarter-End Oracle" nowcast is downgraded here.** Its premise — eCat orders as a real-time leading indicator of ERP revenue — collides with the re-keying distortion (eCat = intent, ~0% join to invoices). The defensible residue is a **caveated pacing line built on invoiced history + open backlog**, not a predictive product. (Full reasoning: Section 6 cut list.)
- **Who pays:** CEO / CFO / FP&A — the number every board meeting opens with.

### C10 — Comparable-Window Momentum (staleness-proof YoY) `[S]` · **Rank 5**
**DECISION & DOLLAR:** *"Your real YoY growth is **N%** — measured on equal, fully-billed windows so a lagging feed can't fake a crash."*
- **Question:** Are we actually growing, and how fast, net of feed artifacts?
- **Method:** Trailing-12-mo invoiced vs prior-12-mo, **both ending at `REPORT_THROUGH_DATE`**; same for QoQ; decompose growth into volume vs price/realization (using C2).
- **Defensibility / failure / suppression:** Both windows fully billed and equal length. **Failure (the classic):** a trailing window runs into empty post-feed months → fake collapse (`mhc`, feed stopped Dec-2025). **Suppress trend** on `LIMITED`/`SALES_DATA` (no date grain) and beyond a single capped window on stale feeds.
- **Why single-artifact but high-rank:** only the Skeptic isolated it, but it rides pure invoiced truth at near-perfect defensibility and feasibility — it earns a top-5 slot.
- **Who pays:** CEO / board — prevents the worst kind of false alarm.

### C11 — Revenue Lumpiness / Big-Deal Dependence `[S]` · **Rank 4 (the honesty metric)**
**DECISION & DOLLAR:** *"That record quarter was three invoices — strip them out and you were flat. Here's how much of your 'growth' is broad-based vs a few big deals."*
- **Question:** How much of a period's growth is durable breadth vs a handful of large transactions?
- **Method:** Distribution of invoiced dollars by invoice size; share of period revenue from top 1%/5% of invoices; **"ex-top-N" growth vs headline growth**; Gini on invoice size.
- **Defensibility / failure / suppression:** Invoice grain (not customer grain) so a true single large deal is visible. **Failure:** legitimate large contract/hospitality orders flagged as anomalies → annotate, don't auto-discount; separate credit memos from the size distribution. **Suppress:** essentially never — *this is the suppression check that keeps the rest of the catalog honest.*
- **Who pays:** CFO / FP&A — protects the forecast and the board narrative from one-time distortions.

### C12 — Price Realization by Account & Off-List Adherence `[O][V][S]` · **Rank 12**
**DECISION & DOLLAR:** *"Your deepest-discounted accounts aren't your biggest, and on **N% of lines you billed below your own published/entitled price** — here's the $ and the reps doing it most. `[ILLUSTRATIVE]`"*
- **Question:** Which accounts/reps deviate from the official price book or the customer's entitled price level, and what does it cost?
- **Method (merges three lenses):** (a) **Discount ROI** — per-customer realized-vs-list ratio (C2 inputs) plotted against invoiced volume; flag low-volume/high-discount cells. (b) **Off-list** — realized unit price vs catalog `products.net_price` for the same item. (c) **Price-level integrity** — realized price vs the price implied by the customer's `DefaultPriceCode`. Aggregate the gap $ by rep/customer/category.
- **Defensibility / failure / suppression:** `products.net_price` must be a meaningful reference (some orgs blank/0) → **suppress off-list claim where empty.** **Tiered/contract pricing looks like leakage** → net out known price levels first; present **"below reference," not "unauthorized"**; **suppress the recoverable-$ claim where tiers aren't known** (show the spread descriptively). Mix differences (cheaper lines) masquerade as discount → control for mix.
- **Who pays:** VP Sales / CFO — a discount-discipline target list with a dollar prize.

### C13 — Price-Increase Pass-Through `[O][V]` · **Rank 16**
**DECISION & DOLLAR:** *"You announced a **6%** list increase; you realized **3.8%** — here's where the other 2.2 points leaked back out as discount, and whether volume even moved. `[ILLUSTRATIVE]`"*
- **Question:** When we raise list prices, how much sticks to realized price?
- **Method:** For items with a known list-change date, compare realized price (`unit_price − unit_price_discount`) before vs after, net of mix; **pass-through %** = realized Δ ÷ list Δ; pair with volume change for a *correlational* realized-elasticity read by category/segment. Tie back to C2 (discount offsetting the increase).
- **Defensibility / failure / suppression:** Needs a known increase date and stable item identity across it. **Failure:** mix shift masquerades as pass-through → control for category/item mix; concurrent promos confound → isolate clean SKUs. No `net_price` history → use realized-price step-change as proxy, label it. Elasticity is correlational — hedge, never sell as causal.
- **Who pays:** CFO / VP Sales — proves price actions reach the P&L.

---

### C14 — eCat Capture / Platform Footprint `[O][S]` · **Rank 9** · *capture, not attribution*
**DECISION & DOLLAR:** *"eCat carries **X%** of your total invoiced sales — and that share is climbing `N` points a year. The rest flows through every other channel. `[ILLUSTRATIVE]`"*
- **Question:** What share of total invoiced sales does our platform provably carry?
- **Method:** Confirmed eCat GMV (eCat-SALE filter, Q-45 numerator) ÷ invoiced total business (Q-CHAN-05); trend and posture band.
- **Defensibility / failure / suppression:** `TOTAL_BUSINESS_SOURCE ∈ {INVOICES, ORDERS}` and **`NOT PARTIAL_INVOICE_FEED`** (eCat LTM > 1.05× invoiced LTM ⇒ feed incomplete, e.g. `sc` 126.9%). **Failure:** quotes inflate the numerator (FAL); partial feed → >100%; ordered-vs-invoiced basis mismatch (always caveat). **Suppress on partial/stale feed; report the completeness gap as the finding; never publish >100% or fall back to the order-header denominator.** Low capture is **not** a failure — it's legitimate multi-channel business.
- **This is CAPTURE, not attribution** (see 3.4) — never present it as "eCat drove X% of your revenue."
- **Who pays:** SuperCat (the honest ROI/retention story) + CEO (channel strategy).

### C15 — Working Capital: Backlog Aging & Booking-to-Cash Lag `[O][V]` · **Rank 20**
**DECISION & DOLLAR:** *"`$4.7M` of booked orders are >90 days unshipped, and you wait N days on average from order to cash — every extra day is `$D` of working capital tied up. `[ILLUSTRATIVE]`"*
- **Question:** How much demand is committed but unbilled, how old is it, and how fast does booking turn into cash?
- **Method:** Open booked dollars (`portal_orders` not yet matched to invoiced qty) aged by `order_date`; expected ship via `inventories.next_scheduled_receipt_date`; cohort lag from order-month → invoice-month (distributional, since 1:1 join is unreliable); days × daily revenue = tied-up cash.
- **Defensibility / failure / suppression:** Built on **cohort conversion (C4), not header joins** — present as a distributional lag, not per-order. **Failure:** backorders legitimately stretch lag → pair with C4 so it reads as fulfillment, not billing dysfunction; stale/partial feed bloats backlog → cap at `REPORT_THROUGH_DATE`; dead never-to-ship orders inflate backlog → age them out.
- **Who pays:** CFO / Treasury — cash-conversion-cycle and production planning.

### C16 — Revenue Composition Strip-Out (freight / tax / discount) `[S]` · **Rank 13**
**DECISION & DOLLAR:** *"**6%** of your 'revenue' is freight and tax pass-through — your real product sales are smaller (and your margin % higher) than you think. `[ILLUSTRATIVE]`"*
- **Question:** What is product revenue net of freight/tax/discount, and is the topline inflated by pass-throughs?
- **Method:** Decompose `portal_invoices`: `net_amount` vs `freight_amount`, `tax_amount`, `discount_amount`; produce product-only revenue and a clean margin denominator.
- **Defensibility / failure / suppression:** Header component columns must be populated and mean what they say (ERP-specific). **Failure:** orgs that fold freight into line price (component cols zero) → strip-out shows nothing → **suppress, report topline as-is**; don't double-subtract a discount already netted into `net_amount`.
- **Why it earns inclusion:** small on its own, but it makes the denominators in C2/C19/C20 correct — foundational plumbing.
- **Who pays:** CFO.

### C17 — Net Revenue Retention ($-based, all-channel) `[O]` · **Rank 13**
**DECISION & DOLLAR:** *"Your existing accounts are worth **96 cents on the dollar** year-over-year — you're refilling a leaky bucket before you count a single new logo. `[ILLUSTRATIVE]`"*
- **Question:** Are we growing the book we already have, net of shrinkage, independent of new wins?
- **Method:** Cohort accounts by first-invoice period; for a fixed cohort, this-year `net_amount` ÷ last-year `net_amount` = **NRR$**; decompose into expansion vs contraction dollars. *(Stays in money — revenue retention, not a churn list.)*
- **Defensibility / failure / suppression:** ≥2 years contiguous invoices, stable keys. **Failure:** customer-number changes / bill-to splits create fake churn/expansion → reconcile keys, present a band; gross-of-returns slightly inflates retention.
- **Scope note:** money-framed only; the *who's-churning-and-why* version is **parked → Customer Profiles 1.0** (Section 6).
- **Who pays:** CEO / CFO / investors — NRR is the headline durability metric for valuation.

### C18 — Freight & Small-Order Recovery `[O][V]` · **Rank 16**
**DECISION & DOLLAR:** *"You under-recovered `$C` in freight last year — small per order, six figures in aggregate — and orders under `$500` lose money once you net freight. You ship **9,000** of them a year. `[ILLUSTRATIVE]`"*
- **Question:** Are we passing through shipping cost, and at what order size does cost-to-serve exceed margin?
- **Method:** `SUM(freight_amount)` charged vs modeled freight cost by order size/region/channel; identify the break-even order value and the loss tail; recommend a minimum-order / freight-policy threshold with a dollar impact; trend recovery rate.
- **Defensibility / failure / suppression:** Org must itemize `freight_amount` (many bundle it). **Failure:** bundled freight reads $0 → looks like 100% give-away → **detect freight-col fill-rate, present "itemized freight only."** Without a cost side, report *charged* freight trends, not recovery %. Exclude free-freight promos / prepaid terms.
- **Who pays:** CFO / Ops — a quiet margin leak that scales with volume.

### C19 — Margin Pool & Mix (PVM bridge) `[O][S]` · **Rank 22** · `COST-GATED — the one ask`
**DECISION & DOLLAR:** *"Revenue is flat but gross margin slid **2.3 points** — you're selling the same dollars of cheaper-margin mix. Your biggest revenue line isn't your biggest profit line. `[ILLUSTRATIVE]`"*
- **Question:** Where does gross margin come from (category/customer/channel), and how is the mix shifting?
- **Method:** Margin% = (net − cost) / net per line; margin pool by dimension; trend org-level margin% and decompose the change into **price** (C2), **mix** (category share), and **cost** effects — the classic price/volume/mix bridge on invoice lines.
- **Defensibility / failure / suppression:** Needs a **trustworthy landed `unit_cost` per item-period.** **Failure (the single most fragile input in the catalog):** missing/zero/stale cost silently turns margin into revenue; standard-cost date drift misattributes which period earned the margin. **Suppress:** exclude any item without verified cost (never impute); **if cost coverage <90% of invoiced $, show revenue mix only and flag "margin pending cost feed."** The *trend* and *mix* decomposition survive imperfect cost; the *level* does not — label them separately.
- **Adjudication / honest feasibility:** the **highest-value idea we cannot ship until cost arrives.** This is the lobbying target — one ERP column (`unit_cost` on the invoice line) unlocks C19, C21, and the true-margin half of C20/C22.
- **Who pays:** CFO — margin erosion is the silent killer revenue dashboards miss.

### C20 — Customer Contribution & Account Margin Tiering `[O][V]` · **Rank 15**
**DECISION & DOLLAR:** *"Your **#3 account by revenue is your #11 by what you actually keep** — and your #5 by sales is your #2 by margin *loss*. Discounts, returns, and freight eat the difference. `[ILLUSTRATIVE]`"*
- **Question:** Who are the *profitable* customers vs the merely *big* ones?
- **Method:** Per account: revenue (`net_amount`) − discount (C2) − returns (C5) − under-recovered freight (C18) = **contribution proxy**; add true gross margin when cost lands. Build a sales-vs-margin quadrant; surface the biggest "rank drops" (big & thin accounts) for renegotiation.
- **Defensibility / failure / suppression:** Inherits every C2/C5/C18 gate. **Without cost it is a contribution proxy, not gross profit — label it precisely.** Freight allocation is assumption-heavy.
- **Who pays:** CFO / VP Sales — reprioritizes account investment toward kept dollars, not vanity revenue.

### C21 — Margin-Weighted Concentration `[S]` · **Rank 23** · `COST-GATED`
**DECISION & DOLLAR:** *"Your revenue looks diversified; your **profit depends on three accounts.** Here's the concentration that actually matters. `[ILLUSTRATIVE]`"*
- **Question:** How concentrated is *gross margin* (vs revenue), and where's the profit fragility?
- **Method:** Re-run C3 concentration on **margin** (needs C19 cost) instead of revenue; compare revenue-HHI vs margin-HHI.
- **Defensibility / failure / suppression:** Same cost caveat as C19 (the binding constraint). **Failure:** bad cost inverts the ranking. **Suppress whenever C19 is suppressed.**
- **Who pays:** CFO / board — profit-risk is the truer risk; reframes the diversification conversation.

### C22 — Geographic Profit Map `[V]` · **Rank 20**
**DECISION & DOLLAR:** *"The Northeast is your **#1 region by sales and #4 by margin** — freight and discounts eat the difference. `[ILLUSTRATIVE]`"*
- **Question:** Where do we make money geographically once freight (and cost) are netted?
- **Method:** Roll the price/freight/(cost) bridge to `customer_bill_to_state`/region; margin per dollar and per shipment by geography; overlay rep/territory.
- **Defensibility / failure / suppression:** **Failure:** bill-to ≠ ship-to misplaces freight → prefer ship-to where present; region rollups need a clean state field. Without cost → a **contribution** map, labeled (not profit).
- **Why single-artifact, low-rank:** a useful *dimension* of C18/C19/C20 rather than a standalone build; included as a derivative cut once those exist.
- **Who pays:** CRO / Ops — territory design, regional pricing, DC placement.

### C23 — New-Introduction Revenue Vitality `[O]` · **Rank 13**
**DECISION & DOLLAR:** *"Items launched in the last 12 months are **9%** of revenue — your innovation engine is either compounding or stalling, and now you can see which. `[ILLUSTRATIVE]`"*
- **Question:** How much current revenue comes from recent introductions (innovation contribution), in dollars?
- **Method:** `SUM(net_amount line)` for items with first-sale < 12mo (or `products.new_item=true`) ÷ total invoiced revenue; trend the vitality % over time. *(Money framing only — not per-item assortment curation.)*
- **Defensibility / failure / suppression:** **Failure:** `new_item` flags go stale (never cleared) and overstate vitality → **prefer a derived first-sale date.**
- **Scope note:** kept because it's pure revenue-composition on the client's own invoice lines; the *which-items-to-cut/keep* version is assortment work, out of Layer 1.
- **Who pays:** CEO / CFO — innovation contribution is a growth-durability signal.

### C24 — Quote-to-Cash Pipeline Value (eCat) `[O][V]` · **Rank 18** · *pipeline, never sales*
**DECISION & DOLLAR:** *"Your reps wrote `$Q` in eCat quotes; historically **~22%** convert and bill within 60 days — `$700K` of forecastable pipeline nobody's tracking. **This is pipeline, not revenue.** `[ILLUSTRATIVE]`"*
- **Question:** What is the dollar value and conversion velocity of the eCat pipeline that precedes booked/invoiced revenue?
- **Method:** Use `order_type` states (Quote/Estimate/Hold/WishList vs Confirmed) as a funnel — the rows the eCat-SALE filter *excludes* from sales; measure cohort quote→confirmed→invoiced conversion and timing; value the live pipeline.
- **Defensibility / failure / suppression:** **Never sum quote $ into sales — this is the FAL trap (`fal` $37.9M → $0.98M, 97% quotes).** Conversion can't be traced 1:1 (join ≈0% + re-keying) → **cohort % only, heavily caveated.** `order_type` vocabulary is org-specific → needs a per-org state map. Label every quote figure "pipeline, not sales."
- **Scope note:** money-framed pipeline sizing stays in Layer 1; rep coaching off this funnel is **parked → Rep Copilot 1.0.**
- **Who pays:** VP Sales / CFO — forward visibility without overstating it.

### C25 — Market & Trade-Show Dollar ROI `[V]` · **Rank 24** · `GATED + client input`
**DECISION & DOLLAR:** *"High Point booked `$2.1M`; only `$1.3M` invoiced and just **18%** of those buyers reordered — your show ROI is half what the booking number implies. `[ILLUSTRATIVE]`"*
- **Question:** What do trade-show/showroom orders convert to in real revenue and durable reorder business, per market?
- **Method:** Isolate market-coded orders (`order_origin`: HPMKT, AMKT, LVMKT, market rooms); run them through booked→invoiced conversion (C4) and forward reorder value; compute ROI vs show cost.
- **Defensibility / failure / suppression:** Market codes exist for few orgs and are bespoke (gated by `Q-CHAN-00`); **show cost is a client input.** **Suppress without both.** Conversion uses cohort grain (C4 caveats). Booked ≠ sold.
- **Who pays:** CEO / VP Sales / Marketing — the perennial "is market worth it?" answered in dollars.

---

## COMPOSITE — The Recoverable Margin Pool *(the literal Money Map)* `[O-fusion]`
**DECISION & DOLLAR:** *"**`$R` of margin is sitting in your own transaction data.** Here is the ranked, owner-assigned worklist to go get it — each dollar traced to a line, a customer/rep, and an action."*

| Lever | Source insight | Action owner |
|---|---|---|
| Off-policy discount | C2 + C12 | VP Sales / pricing |
| Dropped fillable demand | C4 | Demand planning / Ops |
| Returns drag | C5 | Quality / Ops |
| Under-recovered freight | C18 | Finance / Ops |

- **Why it's defensible (not a moonshot):** every component is independently buildable-now and individually defensible. The composite adds **fusion and attribution, not new data.** It is the artifact the title promises.
- **The one hard rule:** **net carefully to avoid double-counting** — a discounted line that also returns is *one* event, not two. Build it **only after C2/C4/C5/C18 are trusted in production**, and show it at the **lowest confidence of its inputs.**
- **Who pays:** CFO + owner — a prioritized cash-recovery campaign with a dollar at the top.

> **Cut from this tier:** an ML-driven *predictive* margin-leak early-warning and a price-**optimization** engine were proposed by Visionary (X2) and Operator (MS2). Both are **cut** as speculative/predictive product bets (Section 6). The Recoverable Margin Pool is the rear-view, fully-grounded version that survives.

---

# 5. KEEP-US-HONEST APPENDIX

These are **non-negotiable rules every insight above obeys.** They are not caveats; they are the reason these numbers survive a hostile board.

## 5.1 The spine — what "revenue" actually is
"Total business" = **invoiced sales** `SUM(portal_invoices.net_amount)` (line-total fallback), date-clamped, per-org reconciliation respected. It is **NOT** `SUM(portal_orders.total_amount)` (booked headers), **NOT** eCat `orders.total`, **NOT** `sales_data` unless nothing better exists. The report **starts here**; consummated/keyed orders are the only other accepted truth.

> **Completeness caveat (do not skip — §3.0).** "Matches what the client sees in their own Sales Portal" is **NOT proof of completeness** — the dashboard reads the same feed we do, so a partial feed matches a partial dashboard. The invoiced topline is `FULL` on **internal consistency** but its **cross-channel completeness is a separate, weaker label** (`FEED_COMPLETENESS`): only **CORROBORATED** (booked≈invoiced) where we have a second feed to triangulate; **UNVERIFIED** otherwise; **suppressed** where provably incomplete (`sc`), stale (`mhc`), or dead (`heb`). And it is always **invoiced**, never **collected** (no AR feed). Empirically ~1 in 3 orgs cannot be completeness-corroborated — never present their Total as definitively whole.

## 5.2 The re-keying distortion (first-class structural fact)
**Almost nothing flows iPad→ERP directly.** A rep writes a quote/order on the iPad, sends it to HQ, where it is **audited and manually re-keyed** into the ERP — and edited/merged/transformed along the way. Consequences that bind the whole catalog:
1. An eCat order is **rep-submitted intent, not a transaction.** Commercial truth is only the ERP/invoice side.
2. The **order→invoice header join is ≈0%**, *and* the order is transformed in between — so booked↔invoiced work is **cohort / line / quantity grain only, never a 1:1 trace** (C4, C9, C15, C24, C25 all honor this).
3. Channel of origin is **stripped** by re-keying unless `order_origin` is explicitly tagged — which is why **capture is a fact but attribution is an estimate** (3.4).

## 5.3 The five traps (each maps to a documented, real failure)
1. **Booked ≠ sold.** Order headers miss by **4×–9×** (`bcf` $2.25M booked vs **$19.94M** invoiced ≈ 8.9× undercount; `jyc` 5.7×, `pf` 3.9×; `cci` 25% *over*count; `rw` shows `$0` orders).
2. **Quotes ≠ sales.** eCat includes Quote/Estimate/Proforma/Hold/WishList. The **FAL disaster**: $37.9M → **$0.98M** real (97% quotes); `sccon` −88%, `sc` −69%, `clli` −84%. Apply the **eCat-SALE filter** to every sales/GMV/capture numerator; pipeline may be shown but labeled "activity/pipeline," never "sales."
3. **Invoiced lags / is partial.** If confirmed eCat already booked more than the feed shows (`sc` 126.9% capture) or the feed went stale (`mhc` stopped Dec-2025), any ratio/trend on it is fiction → **suppress, cap at `REPORT_THROUGH_DATE`.**
4. **Channel tags are bespoke and mostly empty.** `order_origin` is blank for ~30 orgs, free-text elsewhere; only **`cci`** tags eCat reliably (`ril` 12×, `wwjc` 0.25×). A channel split is a confidence-gated luxury (`Q-CHAN-00`), not a default.
5. **Cost & "net" are the softest fields.** Cost/COGS is **not in the schema today**; "net of returns" only works where returns are actually fed (gross-only: `ufi`, `pf`, `jyc`, `bcf`). A margin or net number on a gross-only/no-cost feed is a guess wearing a suit.

**The binding confidence rule:** every number carries a tier (`FULL`/`STRONG`/`PARTIAL`/`LIMITED`/`NONE` from `Q-PROV-00`). **A money number is shown at its lowest input's confidence, or not at all.**

## 5.4 The Danger List — seductive-but-wrong money "insights" (never ship)
| # | Tempting "insight" | Why it's wrong | The rule |
|---|---|---|---|
| **D1** | Total business = `SUM(portal_orders.total_amount)` | Booked ≠ shipped/billed; misses 4×–9× (`bcf` 8.9× under, `cci` 25% over, `rw` $0); breaks every downstream ratio | Total = invoiced `net_amount`; use orders only as labeled `PARTIAL` "booked orders" when no invoices exist |
| **D2** | "eCat sales" that include quotes/holds/wishlists | `order_type` carries pipeline states; FAL $37.9M→$0.98M | Apply eCat-SALE filter to every numerator; pipeline labeled "activity," never "sales" |
| **D3** | Capture / channel share on a partial or stale feed | >100% means the **feed is incomplete**, not eCat dominance (`sc` 126.9%); a stale tail fakes a collapse (`mhc`) | Gate on `PARTIAL_INVOICE_FEED` (>1.05×) and cap at `REPORT_THROUGH_DATE`; report the gap, never the ratio; never fall back to order-header denominator |
| **D4** | A tidy channel pie from `order_origin` | Blank for ~30 orgs, free-text/bespoke, only `cci` eCat-reliable; magnitudes are booked | Run `Q-CHAN-00`; suppress sub-channel for NONE-tier → "eCat vs all other" only; maintained per-org map; % mix on invoiced total; overlay eCat from `orders` |
| **D5** | Margin / net numbers from cost & returns that aren't there | Missing/zero/stale cost turns margin into revenue; gross-only orgs fabricate a 0% return rate; summing order+invoice on OVERLAPS double-counts | Exclude items without verified landed cost (never impute); require ≥90% cost coverage; net-of-returns only when `RETURNS_IN_FEED=true`; respect `portal_data_type`/`portal_calculations` |
| **D6** | "Your total business is `$X`" presented as a **complete** number because it matches their dashboard | **Circular validation** — the Sales Portal reads the same feed; a partial ERP export matches a partial dashboard. No client sells only via eCat, so the book is mostly WEB/EDI/direct/CS/market invoices with **no channel tag and no independent cross-check**. Live proof: `sc` confirmed eCat **exceeds** its invoiced total (feed incomplete); `heb` invoice feed dead since 2020; `pf`/`jyc`/`bcf`/`ril` have no order feed to corroborate against | Run `FEED_COMPLETENESS` (§3.0). Present a Total as complete **only when CORROBORATED** (booked≈invoiced); otherwise attach "single-source; channel completeness unverified," cap PARTIAL. **Suppress** PROVABLY-INCOMPLETE/DEAD. Always say "**invoiced**," never "collected." `order_origin` does **not** fix this (it's on orders, not invoices, and is blank/wrong for most orgs). |

---

# 6. PARKED LAYER-2/3 ON-RAMP  *(tagged only — no design here)*

These ideas reached one or more artifacts but depend on **rep identity/activity** or **customer-relationship behavior** — outside the Layer-1 commerce bones. They are tagged and parked, **not designed**.

| Parked idea | Origin | Tag |
|---|---|---|
| eCat Economic Lift — does selling *through* eCat produce bigger/less-discounted orders? (matched cohorts, adoption dates, selection bias) | V-M9 | **→ Rep Copilot 1.0** (in-app behavior → outcome; the canonical "activity→outcome" enrichment case) |
| Rep Book Economics & Revenue-at-Risk — per-rep concentration + login/usage gaps on revenue | V-M15 | **→ Rep Copilot 1.0** (rep identity + `login_events`/`org_users`) |
| Quote-funnel rep coaching (off C24's pipeline) | O-M14 / V-M11 | **→ Rep Copilot 1.0** |
| Prospecting / fit-based lookalike accounts | (implied) | **→ Rep Copilot 2.0** |
| Customer churn-and-why (the relationship version of NRR$/contribution) | O-M10 / V-M13 | **→ Customer Profiles 1.0** |
| Segmentation unlock: **product type × price point × customer type** (Postgres-MCP) | brief | **→ Customer Profiles 1.0** |

**Architectural principle for whoever picks these up (do NOT build it here):** rep insights must **stand alone on in-app behavior** (ERP-optional). The commerce truth in this document is the **enrichment layer** that upgrades "activity" into "activity → outcome," and that linkage is **gated on the client having ERP**. The bones run **in parallel** to Rep Copilot 1.0 and are the bridge the two layers converge on — they are not a prerequisite for shipping rep behavior insights.

## 6.1 What we CUT, and why (adjudicated out of scope)
| Cut idea | Origin | Reason |
|---|---|---|
| **The Mirror** — anonymized peer/percentile benchmarking | V-H3 | **Cross-client.** Out of scope (Layer 1 is one client's own data). |
| **SuperCat Home-Furnishings Economy Index** | V-X1 | **Cross-client + new external product.** Out of scope. |
| **Quarter-End Oracle** — eCat-as-leading-indicator nowcast | V-H1 | **Predictive product**, and its premise (eCat orders lead ERP revenue) is undermined by the re-keying distortion (intent ≠ transaction, ~0% join). Defensible residue → **C9 pacing line** (range, not prophecy). |
| **Revenue Assurance** — backtested board-grade forecast with track record | V-X3 | **Forecasting product.** Out of scope. |
| **Margin-Leak Early-Warning** — predictive ML on accounts/reps | V-X2 | **Predictive product** (and partly cross-client training). Rear-view residue → **Recoverable Margin Pool composite**. |
| **Price-Elasticity / Optimal-Discount Engine** | O-MS2 | **Speculative optimization product** on observational data. The descriptive, correlational read survives inside **C13**. |

**Adjudication of Visionary optimism vs. Skeptic suppression (summary):** wherever the two collided, the **Skeptic's gate wins on what *ships*, the Visionary's framing wins on what we *aspire to* once a feed lands.** Concretely: the channel pie (V) is suppressed to "eCat vs all other" (S) for ~33/41 orgs (C6); the nowcast (V) degrades to a pacing range (S) (C9); margin stories (V) are kept but **cost-gated and suppressed below 90% coverage** (S) (C19/C21); peer/predictive bets (V) are cut entirely. Nothing rigorous was lost — the Visionary's high-value targets (margin, channel, pass-through) all survive as **gated** entries with a named path to light up.

---

# 7. SOURCE CRITIQUE  *(what we leaned on for what)*

**Operator** — *the build spine.* Strengths: the cleanest **buildable-now vs needs-cost** discipline, the sharpest "no order→invoice join" framing (C4), and the only **composite worklist** (Recoverable Margin Pool) that turns the catalog into an action. Its rankings (Value × Feasibility × Defensibility) became the backbone of our master table. Weakness: occasionally optimistic on channel/forecast feasibility without the Skeptic's hard gates. **Leaned on for:** catalog structure, feasibility scoring, C2/C4/C18, and the composite hero.

**Skeptic** — *the conscience.* Strengths: the **spine + five traps + Danger List**, the confidence-tier discipline, and the unique guardrail metrics the others missed (**C11 lumpiness**, **C10 staleness-proof momentum**, **C16 composition strip-out**). Its suppression rules are the reason the whole document is board-safe. Weakness: deliberately conservative — it under-weights high-upside-if-data-lands ideas (margin, channel) that are worth keeping as gated entries. **Leaned on for:** the entire Keep-Us-Honest appendix, every suppression gate, and the three guardrail insights.

**Visionary** — *the upside map.* Strengths: the **widest aperture** (geographic profit, market/show ROI, pass-through elasticity, the list→net waterfall framing of C2) and the clearest articulation of *which* ideas are high-value. It pushed the catalog beyond the obvious four heroes. Weakness: its biggest swings (The Mirror, Economy Index, the Oracle, ML early-warning) are **out of Layer-1 scope** (cross-client / predictive) and several assume away the re-keying distortion. **Leaned on for:** breadth (C13, C22, C25), the waterfall presentation of realization, and as the source of the cut/park list that defines the scope fence.

**Net:** the Operator gave us the *bones and the build order*, the Skeptic gave us the *rules that keep them standing*, and the Visionary gave us the *reach* — bounded back to Layer 1. Where they agreed (topline, realization, concentration, conversion), we have the highest build-confidence; where only one reached, we kept it only if it rides the invoiced spine and cut it if it required data or scope we don't own. **All three artifacts shared one blind spot — they treated the invoiced topline as a *complete* number rather than an internally-consistent one; §3.0 / D6 / the `FEED_COMPLETENESS` gate are the empirical correction.**

---

# 8. EMPIRICAL VALIDATION RECORD  *(live Postgres, 2026-06-26)*

**Why this section exists.** A reviewer challenged the "we HAVE the full picture / FULL confidence" claims. We ran the live read-only Postgres MCP (`user-supercat-postgres-vpn`, `execute_sql`) across a 21-org cohort to test completeness empirically, rather than assert it. The §3.0 `FEED_COMPLETENESS` gate, the D6 danger, the gross-only correction, and the invoiced≠collected caveat are all outputs of this run.

**Cohort (by org id):** 149 `clli`, 41 `shl`, 40 `clc`, 222 `bri`, 139 `lpf`, 26 `heb`, 166 `kll`, 161 `cci`, 64 `clm`, 46 `mhc`, 18 `ufi`, 176 `vic`, 76 `jyc`, 87 `scw`, 69 `sc`, 171 `bcf`, 32 `pf`, 245 `ril`, 8 `wwjc`, 1 `sarreid`, 55 `gh`. (Test orgs `clctest`/`sc_test`/`demo` excluded.)

**Checks run:** (1) commerce census — row counts of `portal_invoices` / `portal_orders` / `sales_data` / `orders` per org; (2) `order_origin` fill-rate + distinct origins on `portal_orders`; (3) LTM dollar triangulation — invoiced (`net_amount`) vs booked (`total_amount`, $5M-capped) vs confirmed eCat GMV (eCat-SALE filter), plus freshness, `net_amount` fill, credit-memo counts; (4) `order_origin` dollar breakdown for the four richest-tagged orgs (`cci`,`gh`,`scw`,`wwjc`).

**Key findings → where applied:**
1. **Booked-feed is not an all-channel cross-check for many orgs** — `portal_orders` is a tiny fraction of `portal_invoices` for `jyc` (711 vs 111K), `bcf`, `pf`, `ril`, `rw` (0 orders). → introduced the `CORROBORATED` vs `UNVERIFIED—SINGLE FEED` distinction.
2. **`order_origin` is blank (8/21), single-bucket (2/21), or wrong where present** — `scw` ~79% eCat with no eCat origin bucket; `wwjc` "eCAT Order" $2.3M vs confirmed $9.2M (4× under). → §3.0 "order_origin does NOT rescue completeness"; reinforces C6 / D4.
3. **One org provably incomplete:** `sc` confirmed eCat $43.1M > invoiced $34.1M (1.27×) → `PARTIAL_INVOICE_FEED`, suppress Total. **One dead:** `heb` last invoice 2020-06. **One stale:** `mhc` 186 days. → §3.0 verdict table; D6.
4. **Booked≈invoiced corroboration holds where the order feed is complete** — `ufi` 1.03, `kll` 1.05, `clc` 1.08, `cci` 1.25, `gh` 1.09, `sarreid` 1.00, etc. → the basis for the `CORROBORATED` label.
5. **Gross-only (0 credit memos LTM) is wider than the artifacts said** — add `kll`, `clm`, `lpf`, `wwjc`, `sarreid` to the known `ufi`/`pf`/`jyc`/`bcf`. → C5/C2 net-of-returns suppression list expanded.
6. **No AR/cash feed exists** — every Total is *invoiced*, never *collected*. → caveat added to C1, §3.0, §5.

**Caveat on the caveat (intellectual honesty):** `CORROBORATED` means *two independently-fed ERP tables agree*, which makes completeness *likely*, not *proven*. If a client's ERP omits a whole channel from **both** the order and invoice exports, the two still agree and we stay blind. The only way to close that residual gap is a **client attestation of which channels their ERP export covers** — a one-line onboarding question now added to the data-provenance contract (§3.2, C1 "what the client must additionally provide"). Until we have it, the honest posture is a labeled confidence, never a claim of certainty.





