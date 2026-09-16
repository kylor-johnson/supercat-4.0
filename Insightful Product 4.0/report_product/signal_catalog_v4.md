# Signal Catalog v4 — Insightful 4.0

> **Canonical truth lives elsewhere — do not re-derive it here.** The
> invoiced-net axiom and the confidence-gate rule
> (`signal_confidence = LEAST(ceiling, COMMERCE_CONFIDENCE)`, `FULL` unreachable)
> are defined **once** in [`provenance_spine.md`](../foundation/provenance_spine.md);
> this catalog *applies* them. For which signals actually fire (14 detectors in
> `pipeline/signals.py`, not the full 3.0-lineage set below), see
> [`WHAT_ACTUALLY_RUNS.md`](../foundation/WHAT_ACTUALLY_RUNS.md).

> **Status**: Active (merge build, 2026-06-29)
> **Lineage**: The **3.0 signal catalog** (`Insightful Product 3.0/authority/signal_catalog.md`, 26 signals across
> 9 categories) **re-anchored onto the 4.0 provenance foundation**. Every signal keeps its 3.0 detection idea and
> output shape; what changes is the **dollar it's allowed to print** and **when it's allowed to fire**.
> **Read with**: [`report_product_architecture.md`](report_product_architecture.md),
> [`provenance_spine.md`](../foundation/provenance_spine.md), [`query_library_v2.md`](../foundation/query_library_v2.md),
> [`selling_customer_exception_layer.md`](../foundation/selling_customer_exception_layer.md).

---

## How a signal works now (the only structural change from 3.0)

3.0 signal = Detection · Surprise Score · Dollar Impact · Output Format · Priority · Section Home · Data Gate.
**4.0 adds one mandatory field to every signal: the Provenance Binding.**

| Field | 3.0 | 4.0 change |
|---|---|---|
| **Detection** | unchanged | unchanged |
| **Surprise Score** | unchanged | unchanged |
| **Dollar Impact** | LTM revenue of entity | **must resolve to invoiced net** (`Q-ECON-00` / `TOTAL_BUSINESS_SOURCE`); if only eCat/booked exists, the signal is **eCat-channel, labeled LIMITED** |
| **Provenance Binding** | — | **NEW**: which feed, what confidence ceiling, what completeness state suppresses it, whether it's rep-identity-gated |
| **Priority** | P0/P1/P2 | unchanged |

**Scoring (re-anchored):**
```
SIGNAL_RANK = surprise_score × dollar_impact × actionability_multiplier
signal_confidence = LEAST(signal_ceiling, COMMERCE_CONFIDENCE)     # FULL unreachable for $ signals
fires ONLY IF its data gate passes AND its feed clears FEED_COMPLETENESS for that claim
```
A signal that can't earn its dollar **does not fire** — it does not get demoted to a smaller number. Suppress, never approximate.

**Three universal re-anchors applied to the whole catalog:**
1. **Topline/contraction/decay dollars → invoiced net**, equal fully-billed windows, clamped `report_through_date`.
   (Kills 3.0's booked `portal_orders.total_amount` basis — the 4×–9× error.)
2. **Capture/eCat-share signals → "capture, not attribution," LIMITED**; suppress eCat-share below 20% eCat penetration; show absolute eCat $ unless `FEED_COMPLETENESS = CORROBORATED`.
3. **Any rep-named signal → rep-identity tier gate** (Spine §7.1): Tier 2 named, Tier 1 `rep_number` only, Tier 0 suppress rep→revenue.

---

## Category 1 — Decay

### SIG-DECAY-01 · Customer Reorder-Frequency Collapse — P0 · Account
- **Detection (kept):** top-50 accounts, `current_gap / avg_days_between > 2.5×`, account LTM > $10K.
- **Dollar Impact (re-anchored):** account **invoiced** LTM (not booked GMV).
- **Provenance Binding:** feed = invoiced (`portal_orders` keyed-fallback only, labeled booked). Ceiling STRONG;
  cap at `COMMERCE_CONFIDENCE`. Suppress on `FEED_COMPLETENESS ∈ {PROVABLY-INCOMPLETE, DEAD}`. This is also the
  account-grain feeder for exception **S1** (§ Account revenue-at-risk).
- **Output (kept):** *"[CUSTOMER] — reorder silence at [X]× normal cadence… at $[INVOICED_LTM] LTM."*

### SIG-DECAY-02 · Item-Level Reorder Collapse (per-customer) — P0 · Account
- **Detection (kept):** items with 5+ reorder cycles, `latest/avg interval > 3.0×`, item LTM at customer > $5K.
- **Dollar Impact:** item invoiced revenue at that customer where invoice line detail exists; **else eCat order
  lines, labeled eCat-channel.**
- **Provenance Binding:** invoice→eCat line join is ~0% (Spine §2) — **never join line-to-line**; compute at
  customer×item×period grain. Ceiling STRONG; cap at `COMMERCE_CONFIDENCE`.

### SIG-DECAY-03 · Rep Engagement Trajectory Decline — P1 · Team
- **Detection (kept):** rep order count recent-90 vs prior-90, decline > 25%, prior ≥10 orders, rep LTM > $50K.
- **Provenance Binding (rep-gated):** **name the rep only at Tier 2**; Tier 1 → "Rep #[rep_number]"; Tier 0 →
  suppress. Order-count trajectory is eCat behavior (allowed at any tier); the **$ annualization is eCat-channel,
  labeled LIMITED** unless tied to invoiced via rep_number bridge ≥80%.

### SIG-DECAY-04 · Spending Contraction (YoY) — P0 · Account
- **Detection (kept):** account LTM > $25K, YoY decline > 20%, LTM > $50K.
- **Dollar Impact (re-anchored):** absolute **invoiced** decline (prior_invoiced − ltm_invoiced) on **equal,
  fully-billed windows** (the WAYFAIR equal-window fix — never compare a partial current window to a full prior one).
- **Provenance Binding:** invoiced only; ceiling STRONG; cap at `COMMERCE_CONFIDENCE`; suppress on incomplete feed.
  Triggers the **competitive-hypothesis block** (editorial rules §M) at >25% / >$50K.

---

## Category 2 — Anomaly

### SIG-ANOMALY-01 · Ghost SKU — P0 · Product
- **Detection (kept):** invoiced/ordered item codes with revenue but no `products` record, > $5K LTM.
- **Provenance Binding:** prefer **invoiced** line revenue; if only eCat, label eCat-channel. Surprise fixed 3.0.
  Unaffected by economics confidence (it's a data-integrity finding) but the **dollar** still carries its source tag.

### SIG-ANOMALY-02 · Stock-Out on High-Demand Item — P0 · Product
- **Detection (kept):** top-50 items by LTM revenue with `qty_available = 0`, LTM > $10K.
- **Provenance Binding:** demand ranking on invoiced revenue where available; inventory grain is as-of date —
  carry the inventory `as_of` staleness label. No margin claim (no COGS).

### SIG-ANOMALY-03 · Competitive Displacement (eCat down, total up) — P0 · Account
- **Detection (re-anchored):** eCat YoY (`orders`) < −10% **AND total-business YoY > +5%** where total = **invoiced
  net**, account invoiced LTM > $25K.
- **Provenance Binding:** the single most upgraded signal — 3.0 compared eCat to booked total; 4.0 compares eCat
  capture to **invoiced** total. Requires both feeds on equal windows; **suppress if invoiced feed is
  PROVABLY-INCOMPLETE** (you can't claim "buying more overall" if you can't prove the overall). Framed as the
  competitive-hypothesis callout, not "DETECTED."

---

## Category 3 — Opportunity

### SIG-OPP-01 · Companion Products / Next-Best (collaborative filtering) — P0 · Account + Product
- **Detection (kept):** co-purchase pairing across ≥10 customers within 90 days; target account has $0 on the SKU.
- **Dollar Impact (re-anchored + labeled):** estimated addressable = co-purchase count × avg invoiced revenue/purchase;
  tag **`[ESTIMATED]`** (it's an extrapolation) — and per editorial rules, client-facing title is
  *"Products Frequently Bought Together,"* never "collaborative filtering / Next Best Product."
- **Provenance Binding:** needs item-level history across customers; estimate is always `[ESTIMATED]`, never a hard $.

### SIG-OPP-02 · Unactivated High-Value Accounts — P1 · Account
- **Detection (re-anchored):** accounts with **invoiced** total > $50K but **zero lifetime eCat orders**, excluding
  the **Enterprise Channel** exclusion (≥500 total orders + 0 eCat + no B2B Cart → EDI/marketplace, not an eCat
  activation target; surfaced separately, collapsed).
- **Provenance Binding:** total = invoiced; the "opportunity" is **eCat onboarding** (capture), framed as "getting
  them ordering through the app," **not** "addressable revenue." LIMITED claim about channel, not total business.

---

## Category 4 — Momentum (positive — protects narrative balance)

### SIG-MOM-01 · Account/Rep/Product Growth Standouts — P0 · (multi)
- **Detection (kept):** top YoY growers by invoiced revenue (accounts), eCat GMV (reps, behavior-allowed), units (products).
- **Dollar Impact (re-anchored):** invoiced growth $ on equal windows for accounts; eCat for reps (labeled).
- **Provenance Binding:** this is the **mandatory positive P0** — Finding #1 and ≥3-of-7 positive rule depend on it.
  Even when economics confidence is only PARTIAL, a growth standout can ship as **directional/eCat-labeled** so the
  report always opens on a win (3.0 balance rule preserved). Rep names tier-gated.

### SIG-MOM-02/03 · New-buyer growth, category expansion — P2 · Commerce/Product
- Kept; eCat-channel labeled; cap at `COMMERCE_CONFIDENCE`.

---

## Category 5 — Risk

### SIG-RISK-01 · Revenue Concentration (single-account) — P0 · Account *(promoted)*
- **Detection (re-anchored):** top-1 / top-10 account share of **invoiced** LTM. Fires when top-1 > 15% or top-10 > 40%.
- **Dollar Impact:** invoiced $ on the concentrated account(s) = the at-risk amount.
- **Provenance Binding:** invoiced only; STRONG ceiling; this is the validated Sarreid headline (top-1 ~30% / top-10 ~46%).
  Pair with the AR/DSO **"with connected data"** callout (cash-risk is a hard gap — don't fake DSO).

### SIG-RISK-02 · Data Staleness — P0/P1 · Platform
- Kept (operational). Carries `FEED_COMPLETENESS = STALE` to the root document attribute when feeds are stale.

### SIG-RISK-04 · Rep Concentration — P1 · Team
- **Detection (kept):** single rep > 30% or top-3 > 60% of eCat GMV.
- **Provenance Binding:** rep-identity gated for naming; the $-at-risk is eCat-channel unless rep→invoiced bridge ≥80%.

---

## Category 6 — Behavioral (Mixpanel)

### SIG-BEH-01 · Presentation-to-Close Conversion Gap — P1 · Team
### SIG-BEH-02 · High-Activity Zero-Output Users — P2 · Team
- **Detection (kept).** **Provenance Binding:** Mixpanel-coverage gate (degrade to login/order effort if absent —
  never fabricate engagement); rep naming tier-gated; the **$ upside is `[HYPOTHETICAL]`** and eCat-channel.
  These are the behavior axis that **Rung-4 Option A juxtaposes beside** C2/S1 dollars — never fused into one number.

---

## Category 7 — Commerce

### SIG-COMMERCE-01 · Digital Ordering Share with per-point math — P0 · Commerce
- **Detection (re-anchored):** eCat GMV as a % of **invoiced** total; per-point $ = invoiced_total / 100.
- **Provenance Binding (capture≠attribution):** the share is valid **only when `FEED_COMPLETENESS = CORROBORATED`
  and confidence ≥ STRONG**; otherwise present **eCat capture in absolute dollars only**, labeled LIMITED /
  "digital ordering share" (never "capture rate" client-facing). **Suppress entirely below 20% eCat penetration**
  (`Q-CHAN-05` / eCat capture gates — factory LIVE). **`Q-SELL-QC` is BACKLOG** in the
  query library (not in `QUERIES_ALL`). This is the biggest behavioral upgrade: 3.0 printed a
  capture % freely; 4.0 gates it hard.

### SIG-COMMERCE-02 · Quote AOV Spread — P1 · Commerce
- Kept; `[HYPOTHETICAL]` on the conversion-improvement scenario; eCat-channel.

### SIG-COMMERCE-03 · New-Buyer Acquisition Decline — P1 · Commerce
- Kept; eCat-channel labeled.

---

## Category 8 — Product Commerce

### SIG-PRODUCT-01 · Velocity × Stock-Out Collision — P1 · Product
- Kept; demand on invoiced where available; inventory `as_of` staleness carried; no margin claim.

---

## Category 9 — Team Commerce

### SIG-TEAM-01 · Rep/Agency Digital-Ordering Gap — P1 · Team
### SIG-TEAM-02 · Presentation-to-Close Spread — P1 · Team
- Kept; rep-identity gated; capture-not-attribution labeling; `[HYPOTHETICAL]` on upside.

---

## Category 10 — Economics & Leakage (NET-NEW from 4.0 — the dope 3.0 never had)

These are the signals 4.0 invented and 3.0 lacked. They are the reason the merged product can talk about **money
left on the table** with a straight face.

### SIG-ECON-LEAK-01 · Same-SKU Price Leakage — P0 · Commerce *(directional)*
- **Detection:** tier-aware same-SKU price **dispersion** (`Q-ECON-LEAK` / C2) — **never "% off list."** Tiers +
  volume accounts excluded; **house/sample accounts auto-flagged (`house_suspect`) and removed.**
- **Dollar Impact:** recoverable margin from resetting the worst dispersion to tier floor.
- **Provenance Binding (hard rules):** **always directional**, capped at `COMMERCE_CONFIDENCE`; requires a
  **per-report human gut-check + per-org house-account confirm** before any dollar ships (the asi rep-69 "42% rogue"
  false-positive lesson). Present as a **range or withheld dollar** if the house review isn't done in-session.
  Client-facing label per `selling_customer_label_signoff.md`.

### SIG-ECON-RISK-01 · Account Revenue-at-Risk (S1) — P0 · Account
- **Detection:** exception **S1** — account-health $-at-risk (declining/dormant invoiced accounts), deduped against
  SIG-DECAY-01 so a dollar is counted once (the cci/CLIVE D $111,927 pattern).
- **Provenance Binding:** invoiced; STRONG ceiling; cap at `COMMERCE_CONFIDENCE`; **suppress the §15-style headline
  on PROVABLY-INCOMPLETE** (the `sc` suppression). Feeds the Account section + the competitive-loss banner.

### SIG-ECON-LEAK-02 · Rep Leakage / Coaching Hypothesis (C2-by-rep) — P1 · Team *(internal, directional)*
- **Detection:** C2 leakage attributed by rep, **Tier-2 orgs only**, juxtaposed beside Mixpanel depth/cadence.
- **Provenance Binding:** **no fused single number** (Rung-4 Option A discipline); internal/coaching-grade; capped
  at `COMMERCE_CONFIDENCE`; per-report gut-check + per-org house confirm. **Open perf item:** C2-by-rep can exceed
  the 30s restricted-mode Postgres limit on full Tier-2 books → needs a non-restricted/precomputed path.

---

## Signals that require extended data (3.0 "If You Gave Us X" → 4.0 hard-gap upsell)

Carried forward verbatim and merged with 4.0's suppressed hard gaps. These **do not fire**; they render as the
**"With Connected Data" callout** (max 1/section), framed as opportunity:

| Signal | Required data | Unlocks |
|---|---|---|
| SIG-EXT-01 · Product velocity time-series | `invoice_date` on line detail | per-item demand curves, seasonal prediction |
| SIG-EXT-02 · Channel-attributed displacement | `order_origin` populated | "shifted $X eCat→phone," precise displacement |
| SIG-EXT-03 · Parent/family relationship | customer parent key | combined-relationship view (no native key today) |
| SIG-EXT-04 · Quote pipeline aging | quote/commitment dates | "$X in quotes aging past 60 days" |
| SIG-EXT-05 · Fill-rate → reorder correlation | invoice_date + backorder tracking | "$X lost repeat business from fulfillment failures" |
| **SIG-EXT-06 · True margin** *(new)* | **COGS / `unit_cost` feed** | gross margin, leakage-after-cost — the headline upsell |
| **SIG-EXT-07 · Cash / DSO** *(new)* | dealer AR / collections feed | cash-risk on concentration (invoiced ≠ collected) |
| **SIG-EXT-08 · Damage by carrier** *(new)* | carrier/claims feed | claims cost, carrier scorecard |

---

## Signal count

| Category | 3.0 | v4 | Notes |
|---|---|---|---|
| Decay | 4 | 4 | dollars → invoiced; rep-gated where named |
| Anomaly | 3 | 3 | displacement re-anchored to invoiced total |
| Opportunity | 4 | 4 | activation = capture/onboarding, labeled |
| Momentum | 3 | 3 | mandatory positive preserved |
| Risk | 4 | 4 | concentration promoted to P0, invoiced |
| Behavioral | 2 | 2 | Mixpanel-gated, `[HYPOTHETICAL]` |
| Commerce | 3 | 3 | capture≠attribution hard gate |
| Product Commerce | 1 | 1 | inventory as-of carried |
| Team Commerce | 2 | 2 | rep-gated |
| **Economics & Leakage (NEW)** | 0 | **3** | leakage, S1 revenue-at-risk, rep-coaching |
| **Total** | **26** | **29** | + 3 hard-gap upsell signals (EXT-06/07/08) |

**Balance preserved:** the 3.0 rule still holds — ≥3 positive findings, Finding #1 positive — and the new economics
signals are P0 risk/opportunity that the narrative arc places **last**, contextualized by the momentum opener.
