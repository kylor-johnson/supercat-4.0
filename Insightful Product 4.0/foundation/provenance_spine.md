# The Provenance Spine — Tier 0 (canonical, domain-agnostic)

> **What this is.** The single source of truth for **how SuperCat's insight product establishes truth and confidence** — before any domain (Commerce, Rep, Customer) is considered. It is small and stable on purpose. Every domain provenance map (`§3.2`-style) and the query library **inherit** these rules instead of restating them. If a gate, tier, taxonomy, or identity rule is defined here, it must not be re-defined anywhere else — downstream docs *reference* it.
>
> **Why it exists.** The product is being built toward a paid, client-facing offering (Commerce truth + Rep Copilot + Customer Profiles). In a layered system, a "building-code" change is written **once** here and inherited everywhere. The monolith is exactly why `VM-45`'s capture gate went stale: the denominator rule lived in several places, `query_library_v2.md` updated one, and `external_vm_index.md` still carried the old `portal_orders` logic. The Spine ends that drift.
>
> **What inherits from this doc**
> - **Tier 1 — Domain maps:** Commerce ([`capability/insights_moneymap_SYNTHESIS.md`](capability/insights_moneymap_SYNTHESIS.md) §3 — roadmap), **Rep** (`provenance_map_rep.md`), **Customer/Segmentation** (`provenance_map_customer.md`).
> - **Tier 2 — Query library:** `query_library_v2.md` (implementation SQL) — carries a header pointer back here. LIVE IDs: see [`WHAT_ACTUALLY_RUNS.md`](WHAT_ACTUALLY_RUNS.md).
> - **Tier 3 — Synthesis catalogs:** Money Map / VM catalog live under `capability/` (roadmap, not factory).
> - **Semantic authority (capability):** [`capability/value_moment_catalog.md`](capability/value_moment_catalog.md) (**v4.2**). Not loaded to run a report.
>
> **Empirical basis.** Identity, completeness, and segmentation rules below are validated against a **21-org live Postgres cohort** (read-only, `user-supercat-postgres-vpn`), 2026-06-26. The cohort run is in §9. All dollar figures elsewhere are `[ILLUSTRATIVE]`; figures here are `[from-live]` diagnostics, labeled as such.

---

## Runtime mapping (factory — 2026-07-13 re-anchor)

> **Read this before the gate catalog.** The shipped factory (`./run.sh` →
> `pipeline/preflight.py`) resolves commerce posture from **`Q-ECON-00`**, not
> from `Q-PROV-00`. Live preflight IDs: `Q-ECON-00`, `Q-CHAN-00`, `Q-CHAN-06`,
> `RP-2` — see [`WHAT_ACTUALLY_RUNS.md`](WHAT_ACTUALLY_RUNS.md).
>
> | Spine concept | Factory reality |
> |---|---|
> | Commerce gate / `COMMERCE_CONFIDENCE` | **`Q-ECON-00`** (LIVE) — ceiling **STRONG** (never FULL) |
> | `Q-PROV-00` (§6.1) | **Doctrinal ancestor / BACKLOG SQL** in `query_library_v2.md` — axioms still bind; the factory does not execute this ID |
> | `FULL` confidence | Eligible as a data state when `FEED_COMPLETENESS=CORROBORATED`; **unreachable** as a shipped economics label on a single invoice feed |
>
> When a downstream doc says "run Q-PROV-00 first" for a **factory report**, read
> **run Q-ECON-00 first**. Keep §6.1 for meaning; do not delete it.

---

## How to use the Spine
1. **Every number the product emits carries two labels:** a **confidence tier** (§5) and, for any total/denominator, a **completeness state** (§6.3 `FEED_COMPLETENESS`). No bare numbers.
2. **Run the preflights first.** Factory: **`Q-ECON-00`** (commerce/economics), `Q-CHAN-00` / `Q-CHAN-06` (channel), and **`RP-2`** (rep identity) — before any insight query. Doctrinal ancestor `Q-PROV-00` (§6.1) defines the same axioms; it is not in `QUERIES_ALL`.
3. **Lowest input wins, or suppress.** A composite is never more confident than its weakest input (§5.3). When the binding rule says suppress, suppress — do not approximate.
4. **Capture is a fact; attribution is a gated estimate (§4).** Never present an attribution number as captured GMV, or a captured number as total business.
5. **Domains reference, never restate.** If you need a gate or identity rule in a domain map, link to its anchor here.

---

# 1. The commercial-truth axiom

**The ERP is the only source of commercial truth.** A sale is real when it is **invoiced** (shipped + billed) or, failing an invoice feed, when it is a **consummated/keyed order** in the ERP. Everything upstream of the ERP — an iPad order, a B2B-commerce cart, a quote — is **intent**, not a transaction.

- **The revenue spine is invoiced net.** The canonical topline is `SUM(portal_invoices.net_amount)` over a clamped window (§6.4). `net_amount` is the client-facing invoiced total, **negative for credit memos** (returns net themselves out). The header `portal_invoices.total_amount` is **not** the sales figure.
- **The only sanctioned fallbacks, in order:** invoiced (`portal_invoices`) → consummated orders (`portal_orders`, keyed/booked) → `sales_data` (coarse, no dates) → none. The chosen source is selected per org by the commerce preflight (**factory: `Q-ECON-00`**; doctrinal ancestor `Q-PROV-00` §6.1) and **stamped on every output** as `TOTAL_BUSINESS_SOURCE`.
- **Invoiced ≠ collected.** Invoiced net is billed revenue, not cash received. Never imply collection, AR health, or "money in the bank" (§6.7).
- **If there is no ERP feed, there is no commercial outcome to report.** Without invoices or keyed orders we **cannot** close the loop from activity to revenue. We can still analyze in-app **behavior** (the Rep layer, §7.1 / `provenance_map_rep.md`) — that layer is deliberately ERP-optional — but we may not claim a dollar outcome.

---

# 2. The re-keying distortion (first-class structural fact)

Almost no order flows straight from the iPad app into the ERP. The dominant real-world path is: **rep writes an order/quote on the iPad (or emails it) → HQ audits it → a human re-keys it into the ERP → it later ships and invoices.** Re-keying breaks the 1:1 trace.

**Consequences that bind every domain:**
- **An eCat order is intent, not a transaction.** It may be edited, split, partially shipped, cancelled, or never keyed.
- **The order→invoice join is effectively ~0%.** `orders.order_number` (eCat) does not reliably equal `portal_invoices.order_number` (ERP). Do **not** join eCat orders to invoices at the row level. Tie them only at **cohort/period grain** (e.g., "this rep's customers invoiced $X this quarter"), never line-to-line.
- **Our POV on commerce is structurally partial.** What we see through SuperCat rails (iPad + B2B-commerce) is only part of the client's revenue; the rest (other online, EDI, manual keying) reaches the ERP without ever touching us. This is the root of **capture vs attribution** (§4) and of `FEED_COMPLETENESS` (§6.3).
- **Therefore eCat "sales" are CAPTURE (verifiable GMV through our rails), never the client's total business.** The total is the ERP's, and only as complete as its feed (§6.3).

---

# 3. The Commerce Origin Taxonomy

Every dollar of a client's business originates in exactly one channel. Our visibility differs by channel — name the channel before trusting the number.

| Origin | What it is | Our visibility | Reaches ERP via |
|---|---|---|---|
| **iPad (eCat)** | Rep-written orders/quotes in the eCat app | **High** (we own `orders`) — but as *intent*, pre-re-key | Re-keyed/audited by HQ |
| **B2B-commerce (SuperCat)** | Buyer self-service orders on SuperCat B2B | **High** (our rails) — also pre-ERP | Re-keyed/integrated |
| **Other online** | Client's own webstore / marketplaces (not SuperCat) | **None** directly | Client's own integration |
| **EDI / manual-keyed** | EDI from large accounts, phone/email/manual entry | **None** directly | Direct to ERP |

- `portal_orders.order_origin` is the intended channel tag on the booked-orders feed, **but it is unreliable** (often null/uniform per org — confirmed in the commerce run). Treat `order_origin` as advisory; gate any channel split on `Q-CHAN-00` (§6.2).
- The **only channel we can quantify with certainty is SuperCat capture** (iPad + B2B-commerce), because we own those rails. Everything else is inferred from the gap between ERP total and SuperCat capture — an estimate, not a fact.

---

# 4. Capture vs Attribution (never blur these)

- **Capture = fact.** GMV that verifiably flowed through SuperCat rails: eCat `orders` that pass the **eCat-SALE filter** (§6.5), and B2B-commerce orders. Numerator and denominator are both ours. Reportable whenever the feed exists.
- **Attribution = gated estimate.** A claim about SuperCat's *influence on total ERP revenue* (e.g., "eCat capture rate = SuperCat GMV ÷ total invoiced business"). The denominator is the ERP's and is only as complete as `FEED_COMPLETENESS` allows; the numerator is intent (pre-re-key) measured against outcome (invoiced) — **different grains**.

**Binding rules:**
- A capture-rate / attribution number is **only valid when `FEED_COMPLETENESS` ∈ {CORROBORATED}** and `Q-PROV-00` confidence ≥ STRONG. Otherwise present **capture in absolute dollars only**, never as a rate of total business.
- Never present an attribution estimate as captured GMV, and never present captured GMV as the client's total business.
- The capture denominator (invoiced total) is itself only as complete as §6.3 allows — an attribution rate inherits the weaker of (denominator completeness, numerator confidence).

---

# 5. Confidence tiers and the binding rule

## 5.1 The five tiers
| Tier | Meaning | Reporting behavior |
|---|---|---|
| **FULL** | Internally consistent *and* corroborated complete | Report as headline truth |
| **STRONG** | Invoiced feed present, fresh, internally consistent; completeness not independently corroborated | Report with a one-line completeness caveat |
| **PARTIAL** | Feed present but stale, provably incomplete, or orders-only (no invoices) | Report **ranges/directional** only; label loudly |
| **LIMITED** | Only coarse `sales_data` (no dates/line detail) | Report magnitude only; most insights suppressed |
| **NONE** | No usable feed | **Suppress**; offer the behavior-only (Rep) layer instead |

## 5.2 What sets the tier
Tiers are assigned by `Q-PROV-00` (§6.1) for commerce, and by the domain identity/coverage gates (§7, and each domain map) for rep and customer. **`FULL` requires `FEED_COMPLETENESS = CORROBORATED` (§6.3)** — internal consistency alone caps you at `STRONG`.

## 5.3 The binding rule (one line)
> **A composite or derived number inherits the *lowest* confidence of its inputs, or it is suppressed. Confidence never increases by combining inputs.**

---

# 6. The gate catalog (defined once — referenced everywhere)

Each gate has: what it tests, its output values, and the behavior it forces. SQL bodies live in `query_library_v2.md` (Tier 2); this is the canonical *definition* of each gate's meaning and behavior.

## 6.1 `Q-PROV-00` — Commerce Provenance Preflight *(doctrinal ancestor / BACKLOG SQL)*

> **Factory note:** `./run.sh` does **not** execute `Q-PROV-00`. Live commerce
> posture comes from **`Q-ECON-00` (§6.8)**. This section keeps the *meaning* of
> the commerce preflight; the SQL body in `query_library_v2.md` is BACKLOG
> relative to `config.QUERIES_ALL`.

- **Tests:** which commercial feed exists (invoices / orders / sales_data / none), its freshness (`days_since_last_invoice`), internal consistency (`pct_netamount`, presence of returns/credit memos), and the portal config (`portal_data_type`, `portal_calculations`).
- **Emits:** `TOTAL_BUSINESS_SOURCE` ∈ {INVOICES, ORDERS, SALES_DATA, NONE}; `COMMERCE_CONFIDENCE` ∈ {FULL, STRONG, PARTIAL, LIMITED, NONE}; `report_through_date`.
- **Forces:** the source and confidence label stamped on every commerce number. **Factory: run `Q-ECON-00` before any commerce insight.**

## 6.2 `Q-CHAN-00` — Channel Availability Preflight
- **Tests:** whether `order_origin` (and any channel tag) is populated and varied enough to support a channel split.
- **Emits:** channel-availability flag per org.
- **Forces:** if channels are not reliably tagged, **suppress channel splits** and report blended only. (`order_origin` is advisory per §3.)

## 6.3 `FEED_COMPLETENESS` — the completeness gate (the assumption we cannot prove from one feed)
The hardest, most important gate: a present, internally-consistent invoice feed does **not** prove the feed covers *all* of the client's sales channels. Completeness is a **separate dimension** from internal consistency.

- **Tests (triangulation):** booked-vs-invoiced ratio (`portal_orders` GMV ÷ invoiced net), eCat-capture-vs-invoiced ratio (eCat-SALE GMV ÷ invoiced net), invoice freshness, and presence of returns.
- **Emits one state:**
  | State | Meaning | Behavior |
  |---|---|---|
  | **CORROBORATED** | A second independent signal agrees the invoiced feed is whole (e.g., booked≈invoiced within tolerance; eCat capture ≤ invoiced and consistent). **Coverage guard (live 2026-06-30):** the corroborating feed must be *materially present* — a sparse second feed (e.g. `bcf` `portal_orders` only ~11% of invoiced) cannot corroborate and falls back to UNVERIFIED-SINGLE-FEED, even with a clean topline | Eligible for **FULL**; "complete" language allowed |
  | **UNVERIFIED — SINGLE FEED** | Invoice feed present & consistent, but nothing corroborates completeness | Cap at **STRONG**; every total carries "as invoiced through our feed; cross-channel completeness not independently verified" |
  | **PROVABLY INCOMPLETE** | A known channel exceeds the invoiced total (e.g., **eCat capture > 1.05 × invoiced net** → invoices can't be the whole business) | **PARTIAL**; never call any total "complete/total business" |
  | **STALE** | Newest invoice far older than expected (`days_since_last_invoice` large) | **PARTIAL**; report through `report_through_date` only |
  | **DEAD / NONE** | No invoice feed | **Suppress** totals; behavior-only layer |
- **Forces:** the completeness word on every Total. **`FULL` is unreachable without `CORROBORATED`.** This is the gate that makes "your total business is $X" honest.
- **Presentation cap (product layer, conservative override):** `CORROBORATED` makes a total *eligible* for `FULL` as a **data state**, but the value-moment catalog deliberately **presents economics VMs at STRONG even when CORROBORATED** — one ERP's booked-vs-invoiced agreement is internal corroboration, not a truly independent second source. FULL-eligibility is never a license to tell a client "complete/total business" without the single-feed caveat. See `capability/value_moment_catalog.md` → How-to-Read → Confidence Ceiling.

## 6.4 Date clamps
- Clamp every window to `report_through_date` (newest real invoice/order); never report a "current month" that the feed hasn't reached. LTM = trailing 12 months ending at `report_through_date`, not at `CURRENT_DATE`.

## 6.5 The eCat-SALE filter
Applied to **every eCat GMV / capture numerator** (from `orders`) to exclude non-sales intent (quotes, holds, tests, wishlists):
```sql
AND COALESCE(NULLIF(TRIM(order_type), ''), 'Confirmed') NOT IN
    ('Quote','Estimate','Proforma','WishList','Wish List','Interest','Liked','Draft Order','Select Order Type')
AND order_type NOT ILIKE 'HFC%' AND order_type NOT ILIKE 'Hold%' AND order_type NOT ILIKE 'TEST%'
```
Also require `is_submitted = true` and exclude `is_marked_deleted = true` per the library.

## 6.6 The `$5M` row cap
A single-row sanity cap: any line/order/invoice amount above `$5,000,000` is treated as a data-entry artifact and excluded from sums (and flagged), unless the org is explicitly known to transact at that scale. Prevents one fat-fingered row from corrupting a topline.

## 6.7 `invoiced ≠ collected`
Invoiced net is **billed**, not **collected**. No output may imply cash received, AR aging, DSO, or "money in the bank" from invoice data alone.

## 6.8 `Q-ECON-00` — Economics Preflight (**LIVE factory commerce gate**)
The live factory counterpart (and practical successor) to `Q-PROV-00`: it decides which **money/selling** insights an org can support **and the confidence ceiling each may claim.** SQL body in `query_library_v2.md` Domain 10; **in `QUERIES_PREFLIGHT` / executed by `pipeline/preflight.py`**. Hardened on a 22-org live cohort, 2026-06-29; completeness-capped per the 2026-06-29 skeptical audit.
- **Tests:** invoice feed presence; **priced invoice-line coverage** (`unit_price>0` — NOT a `products` join); freight / terms / carrier / `ship_date` population; credit-memo presence; `order_origin` variety; **feed freshness and the eCat-capture-vs-invoiced ratio** (completeness).
- **Emits per-org flags:** `invoice_feed_present`, `leakage_dispersion_ok` (priced lines ≥60%), `netrev_freight_ok`, `returns_ok`, `terms_ok`, `carrier_ok`, `leadtime_ok`, `channel_ok`; a clamped `report_through_date`; **and `COMMERCE_CONFIDENCE` ∈ {STRONG, PARTIAL, NONE}** (see cap below).
- **Forces (the binding rules):**
  - **THE COMPLETENESS CAP (audit Defect A — the reason this gate exists):** every economics number reports at `LEAST(its own ceiling, COMMERCE_CONFIDENCE)`. A **stale** feed (`days_since_last_invoice > 45`, e.g. `bmc` at 213d) or a **provably-incomplete** feed (confirmed LTM eCat GMV > 1.05× invoiced LTM net, e.g. `sc` at 126%) forces **PARTIAL** no matter how green the availability flags are; no feed → **NONE** (suppress). **`FULL` is unreachable for economics** — it requires `FEED_COMPLETENESS = CORROBORATED` (§6.3), which a single invoice feed never provides. The economics ceiling is **STRONG**. A `sales_data` total far above invoiced LTM (`salesdata_over_invoiced` > ~1.3) is a soft second signal that the invoice feed is a channel subset (reinforces UNVERIFIED — SINGLE FEED, never FULL).
  - **R1 — bad-date clamp:** `report_through_date = MAX(invoice_date) ≤ CURRENT_DATE`. Live, `clm` carried an invoice dated **4107** and `jyc` **2032**; an unclamped window anchors on a fantasy date. Every windowed economics query clamps its window to `report_through_date`.
  - **R2 — priced lines, NOT a products join (corrected per audit):** leakage eligibility is gated on **priced invoice lines** (`unit_price>0`), never on a `products` join. The dispersion metric never reads `products`; gating it on the join wrongly suppressed `pf` (0% product-line join, fully valid dispersion — live-confirmed $2.9M).

## 6.9 Economics hard gaps (suppress — never approximate)
Confirmed absent at the schema level (full `information_schema` scan, 2026-06-29): **no cost/COGS/margin, no rebate/chargeback/coop, no claims/damage** column anywhere; the only payment tables (`stripe_invoices`, `subscription_invoices`) are SuperCat's **own SaaS billing**, not dealer AR. Therefore the following are **hard gaps** and must be suppressed with a one-line "no source" note, not estimated:
- **Gross / true margin** (no COGS) — `Q-ECON-NETREV` is revenue net of freight, **not margin**.
- **AR / DSO / collections / credit risk** (no dealer AR; `terms` is billed, not collected — extends §6.7).
- **Damage / claims by carrier** (no claims data) — carrier analytics = freight$/shipments only.
- **Quoted lead time, inventory aging, market/showroom ROI** — no source.

## 6.10 The price-realization rule (leakage = TIER-AWARE dispersion, not "% off list")
`products.net_price` semantics **vary per org and are not self-identifying** — MSRP/retail in some orgs (live: cci/scw/gh show 55–69% "off list" = the normal wholesale spread, **not** leakage), wholesale list in others. **A "% off list" leakage figure is prohibited as client-facing.** Discount leakage must be computed as **same-SKU realized-price dispersion** (a customer priced materially below that SKU's own cross-customer **median**), which is list-independent and reputationally safe. **Tier-aware (audit remediation 2026-06-29, owner-approved):** the dispersion must additionally (a) use a **true median** reference at customer grain, not a mean; (b) exclude **recognized price tiers** (a price shared by ≥5 customers); (c) exclude **strategic-volume accounts** (≥10% of a SKU's units) — otherwise negotiated/volume pricing reads as a false leak (live: it flipped asi "rep 69 = 42% rogue" into a normal 2.1%). **House/sample accounts are auto-detected + flagged** (`house_suspect`: `ZZ*` dropped + `ACCOM*`/`SAMPLE*`/… prefixes + the tiny-revenue/huge-leakage signature) and excluded from the headline pending a one-time per-org owner confirmation. Any leakage **dollar** figure still requires a human gut-check before client delivery, and is **capped at `COMMERCE_CONFIDENCE`**.

---

# 7. The identity-resolution spine (the unmapped join layer)

Every domain map joins on identities that SuperCat does **not** store as clean keys. These rules are canonical; each domain map references them and reports its **match rate** as a gate. Match rates below are `[from-live]` across the 21-org cohort (§9).

## 7.1 Rep identity — `rep_number ↔ org_users/users ↔ rep name`
- **eCat side is solid.** `orders` carries `rep_first_name`, `rep_last_name`, `rep_number`, and `org_user_id` directly. In-app rep behavior (the Rep layer) needs no external join — it stands on `orders`, `login_events`, `org_users`/`users`. **This is why the Rep layer is ERP-optional.**
- **ERP side is the gap, and it has THREE tiers, not two** (validated 2026-06-26, Phase-A rep census + spot-check). `portal_invoices` carries **only `rep_number`** (no name); `portal_orders` carries `rep_number` + `rep_name` (the sole name bridge). An org falls into one of:

  | Tier | Condition `[from-live]` | Orgs (date-aligned name-bridge %) | Rep-outcome behavior |
  |---|---|---|---|
  | **0 — no ERP rep key** | invoice `rep_number` ≈ **0%** (no key at all) **OR** zero invoice rows entirely (structural feed absence) | **ufi, heb, kll, lpf** (rep_number key absent on a populated invoice feed) · **sca** (no `portal_invoices` rows at all — added 2026-06-30 per PASS3 cohort finding; structural feed absence is the rule's vacuous-satisfaction case) | **Behavior-only.** No rep→revenue is possible; do not attempt. |
  | **1 — `rep_number`-only** (9 orgs) | `rep_number` present, but name bridge **<78%** (or inside the 78%–82% deadband and not a declared Tier-2 carry-over — see hysteresis note below) | gh (39%), scw (36%), sc (3.2%), clm, clli, bri, vic, shl, jyc (all 0%/sub-40% bridge) | Attribute to **`rep_number` grain only — no names**. |
  | **2 — named-rep reachable** (8 orgs) | `rep_number` present **and** `portal_orders.rep_name` bridge **≥82%** (promotion threshold), or **≥78% and declared Tier-2 carry-over** (deadband hold) | sarreid (100%), clc (100%), **mhc (100%, ⚠ DORMANT)**, cci (100%), wwjc (98.8%), pf (89.7%), ril (87.7%), **bcf (81.8% — held)** | Named rep→revenue allowed (still capped by `FEED_COMPLETENESS`). |

  **Tier-bridge hysteresis (2026-06-30).** The 80% boundary oscillates on real feeds (hfg moved 79.3% → 81.0% in 30h on natural data refresh — same run, different reported tier, different report shape). The boundary is therefore a **hysteresis band**, not a single threshold: **promote to Tier 2 at `name_bridge_pct ≥ 82%`; demote from Tier 2 only at `< 78%`; the 78%–82% deadband defaults to Tier 1 unless the org is a declared Tier-2 carry-over** (the hardcoded list in `rep_copilot_operator.md` §1 — currently `bcf` 81.8%, the only deadband carry-over). Same run twice on a boundary org returns the same tier because the resolution is fully deterministic from `name_bridge_pct` + the declared-carry-over list; there is no implicit per-run "previous tier" state. The implementation lives in `rep_copilot_operator.md` §1 RP-2 (the SQL emits Tier 2 at `≥82`, Tier 1 in the deadband; the operator's §1 cohort table holds bcf at Tier 2 in the application layer).

  *(**Bridge is date-aligned** — re-confirmed live 2026-06-29, see `rep_intelligence_layer2_build.md` §2: numerator uses the SAME trailing-12-month invoice `rep_number`s as the denominator, so `name_bridge_pct` caps at 100% and the boundary is mechanically reliable; the hysteresis above sits on top of that to absorb natural feed wobble in the deadband. The earlier un-dated "has any bridge" census overstated gh/scw/sc toward Tier 2 and **undercounted bcf** — bcf clears the deadband-hold rule (81.8%, declared carry-over) and is **Tier 2**, not Tier 1. **mhc** clears at 100% but its feed is **DORMANT** — flag before any client-facing named output. Tier 0 measured separately: ufi/heb/kll/lpf carry 0% `rep_number` across 120k–251k invoices each.)*
- **Rule:** tying a **commercial outcome** (invoiced $) to a **named rep** requires **Tier 2** (name-bridge ≥ 82% promotion, ≥ 78% deadband-hold for declared carry-overs — see the hysteresis note above). **Tier 1** → `rep_number` grain only (no names). **Tier 0** → suppress rep-level revenue entirely and ship **behavior-only** rep insights. **Never silently drop unmapped reps from a revenue ranking** — that fabricates a leaderboard.
- `org_users` ≠ rep roster for B2B orgs: it conflates reps and buyer/portal accounts (e.g., wwjc 20,740, jyc 16,181, gh 7,997 org_users vs ~40–160 actual iPad-active seats). Use `org_users.last_ipad_login_at IS NOT NULL` (or order authorship) as the rep-seat proxy, **not** raw `org_users` count.

## 7.2 Customer identity — billing entity ↔ parent/corporate family
- **Default grain is the billing entity** (`customer_bill_to_number` on `portal_invoices`/`portal_orders`; `customers.code`). This is the only reliable customer key.
- **There is no native parent/corporate-family key.** `customers.mapped_code` is **~0% populated** (max sc 41.5%; scw 9.6%; gh 5.5%; everyone else 0%). Name-based roll-up is low-yield (bill-to codes ≈ distinct names in nearly every org) and sometimes impossible (**clli invoices carry 1 distinct bill-to name across 2,838 codes** — name is unusable there).
- **Rule:** report at **billing-entity grain by default.** A parent/corporate roll-up is a **derived, gated** artifact (fuzzy name+address match), never presented as exact, and **suppressed** where the name field is degenerate (e.g., clli). Ship-to rolls up to its bill-to via `customer_ship_to_number → customer_bill_to_number`.

## 7.3 Territory format
- `customers.territory_codes` format **varies by org** (CSV `"C-14,C-15"` vs JSON `["C-14"]`); `territory_codes_json` is the JSON variant. In the 21-org cohort the values were **uniformly JSON-array and ~100% populated**, but the format-variance risk is real library-wide.
- **Rule:** always run the format preflight (`Q-43` style) before unnesting; never assume one format. Territory presence ≠ correct rep assignment.

## 7.4 Product identity (for segmentation joins)
- Products key on `item_number` (eCat) ↔ `base_item_code` (`sales_data`/inventory) ↔ `ecat_item_number`/`item_number` on order/invoice lines. Joins are per `organization_id`.
- The named field `product_type` is **near-empty** (0% for 19/21 orgs; the two exceptions hold a single constant value). The usable product-grouping signals are `category_code`/`category_codes` and `collection_code`/`collection_codes` — **org-defined and opaque**, not comparable across clients without a per-org interpretation pass (§ Customer/Segmentation map).

## 7.5 Customer "type" — not a native field
- There is **no native customer-type/channel field** (retailer vs designer vs hospitality vs contract). `distribution_source` is unused (~0% everywhere except clli). `default_price_code` is **100% populated** and is the only native tier signal, but its discriminating power varies (some orgs have a single price code; others 15–41).
- **Rule:** customer type is **derived from first-party behavior** (order cadence, AOV, category mix, price-tier) — never imposed from a label. See the Customer/Segmentation map for the method. **External enrichment (TAM CSV `FIT_*`/`Segment_Opus_*`) is excluded as an input** (§8).

---

# 8. Cross-cutting rules every domain obeys
- **Information hierarchy is action-first.** Lead with the decision/so-what ("bold AF"); method, rationale, and caveats are drill-down below. Never bury the action under mechanics.
- **Every total/money number carries completeness (§6.3) + confidence (§5).** Suppress rather than guess.
- **No fit scoring, no imposed segment labels.** First-party Postgres transaction/catalog data *informs* segments; enrichment is validated *against*, never seeded *from*. **Exclude the TAM CSV LLM columns** (`Segment_Opus_4.5`, `FIT_*_Opus_4.5`, the "Detected/Estimated" enrichment block) from any segmentation input — they are biasing and demonstrably wrong (identical hallucinated text across distinct companies).
- **Rep layer stands alone on in-app behavior (ERP-optional); commerce is the enrichment** that upgrades "activity → outcome," and only when the ERP feed + rep-identity gate (§7.1) permit.
- **Read-only Postgres** (`user-supercat-postgres-vpn`); validate every map across **10+ real orgs**; label live figures `[from-live]`, design figures `[ILLUSTRATIVE]`.

---

# 9. Validation provenance (this Spine's empirical basis)

**Cohort (21 orgs, by `organization_id`):** 149, 41, 40, 222, 139, 26, 166, 161, 64, 46, 18, 176, 76, 87, 69, 171, 32, 245, 8, 1, 55 — shortnames include sc, cci, pf, ufi, wwjc, gh, mhc, jyc, scw, clli, clm, sarreid, ril, clc, bri, kll, bcf, lpf, heb, vic, shl. **Run date:** 2026-06-26, read-only.

**What was measured and the headline finding:**
| Spine claim | Evidence `[from-live]` |
|---|---|
| Rep-identity ERP gap is real & has **3 tiers** (§7.1) | invoice `rep_number`→name mappability ranges **0%–100%**; **4 orgs have 0% `rep_number` at all** (ufi, heb, kll, lpf → behavior-only) **+ sca added 2026-06-30 as structural feed-absence Tier-0** (no `portal_invoices` rows at all); **9 are `rep_number`-only, 8 reach names** (date-aligned bridge, re-confirmed 2026-06-29; Phase-A rep census 2026-06-26) |
| No native parent key (§7.2) | `customers.mapped_code` populated **0%** in 18/21 orgs (max 41.5%); clli bill-to name degenerate (1 distinct across 2,838 codes) |
| Territory uniformly JSON here, but format-variance risk real (§7.3) | `territory_codes` 100% JSON-array, 0 blank across cohort |
| `product_type` unusable; use category/collection (§7.4) | `product_type` 0% in 19/21 orgs; `category_code` 10–285 distinct/org, `collection_code` 6–703/org |
| No native customer type; price-code is the only native tier (§7.5) | `default_price_code` **100%** populated all orgs (1–41 distinct); `distribution_source` ~0% |
| Rep behavior feed is solid & ERP-optional (§7.1) | `login_events` present & fresh (last login 2026-06-26) for 20/21 orgs; **mhc stale** (last 2026-02-28, matches its stale invoice feed) |
| Price-point is a strong native dimension | `net_price` numeric, well-populated; org averages span **$14–$3,437** (heb parts vs pf luxury) |

These figures are diagnostics, not client deliverables. Re-run on the live cohort before any client-facing use.

---

# 10. Notes & open items
- **Semantic authority (resolved 2026-06-29; shelved 2026-07-13).** The capability catalog lives at [`capability/value_moment_catalog.md`](capability/value_moment_catalog.md) (**v4.2**). It received the invoiced-spine + `FEED_COMPLETENESS` + capture-vs-attribution reconciliation (Domains 9–13). It is **roadmap**, not factory — see [`WHAT_ACTUALLY_RUNS.md`](WHAT_ACTUALLY_RUNS.md). There is a separate **`Customer Intelligence/`** MVP. **Reconciled (2026-06-29):** economics/segmentation flows through `Q-ECON-00` (§6.8), the hard-gap register (§6.9), and the dispersion-leakage rule (§6.10); exception-push synthesis is in `selling_customer_exception_layer.md` / `provenance_map_customer.md` §7–§8.
- **Economics validation provenance.** Domain-9 (selling/customer economics) was hardened on a **fresh 22-org live cohort** (13 net-new beyond the §9 foundation 21), read-only, 2026-06-29 — see `selling_customer_pilot_test_worksheet.md`. That pilot is the empirical basis for §6.8–§6.10.
- **Mixpanel/BigQuery.** Rep behavioral *depth* (feature usage beyond logins) lives in BigQuery (`user-bigquery-admin`), not Postgres. The Rep map gates on Mixpanel coverage there; Postgres `login_events` is the always-available floor.

