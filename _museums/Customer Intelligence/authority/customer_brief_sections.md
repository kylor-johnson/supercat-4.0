# Customer Intelligence Brief — v2 Section Design

> **Status**: Production v5 — 2026-06-29 (Layer-3 re-anchor on the invoiced spine: every Total now carries a
> provenance label from **G-00**). v4 baseline updated 2026-06-16 (all audit findings applied).
> **Source**: Refined from 22+ briefs across 8 clients, with gap-closure extensions + v3 pilot audit
> **Authority**: This file defines the rendering spec for every section of the Customer Intelligence Brief.
> Sections are ordered by rendering priority. The brief generator must follow this order.

---

## Provenance labeling (v5 — applies to every Total in the brief)

> Run **G-00 `TOTAL_BUSINESS_PROVENANCE`** (`authority/customer_gate_rules.md`) before any section. It resolves
> `TOTAL_BUSINESS_SOURCE`, `COMMERCE_CONFIDENCE`, `FEED_COMPLETENESS`, and `report_through_date` — the contract
> inherited by every dollar Total (Spine §1, §5.3, §6.3; *Layer 1 is locked/read-only — the brief consumes it*).

- **Every Total prints its provenance**: `$X total business (invoiced through {report_through_date} ·
  {FEED_COMPLETENESS} · {COMMERCE_CONFIDENCE})`. Never a bare dollar.
- **Suppress on `PROVABLY INCOMPLETE` / `DEAD`**: do not print a "total business" number; show eCat **capture
  in absolute dollars only**, labeled "captured through eCat — not total business." The competitive-loss banner
  and the revenue-at-risk headline are also suppressed (they ride the Total).
- **`PARTIAL` / `STALE`**: print Totals as directional/ranged with the loud completeness caveat; all windows
  clamp to `report_through_date`.
- **Booked is a labeled fallback, never the headline**: when `TOTAL_BUSINESS_SOURCE = ORDERS`, every dollar is
  labeled "booked orders (no invoice feed)." Never present booked GMV as invoiced total business.
- **Never headline eCat capture > 100%** (Spine §4): cap the displayed capture at 100%; a raw ratio > 105% is
  the incompleteness signal, not a metric.

## Rendering Modes

The brief operates in one of three modes — `HAS_PORTAL_INVOICES` sets section availability, **G-00**
`TOTAL_BUSINESS_SOURCE` sets dollar trustworthiness:

| Mode | Condition | Available Sections |
|------|-----------|-------------------|
| **Full (invoiced)** | `HAS_PORTAL_INVOICES = true` AND `TOTAL_BUSINESS_SOURCE = INVOICES` | All always-on + all conditional where gates pass; Totals on invoiced net |
| **Orders-Only (booked)** | `HAS_PORTAL_INVOICES = false` AND `TOTAL_BUSINESS_SOURCE = ORDERS` | §1-2 (header/snapshot), §6 (trajectory), §7 (rhythm), §8 (channel), §9 (wallet share), §22 (health score), §23 (summary). No category/SKU/collection analysis. **All dollars labeled "booked."** |
| **Behavior-Only (suppressed)** | `TOTAL_BUSINESS_SOURCE = NONE` OR `FEED_COMPLETENESS ∈ {PROVABLY INCOMPLETE, DEAD}` | No dollar Totals. eCat capture in absolute dollars only; rhythm/cadence, rep engagement, catalog facts. The brief states why the Total is suppressed. |

## Section Numbering (v4, audit finding §9)

Sections use **sequential numbering in the rendered brief** — renumber to close gaps left by gated-out sections. The §-numbers in this spec file are the *canonical IDs* for reference; the brief generator assigns sequential display numbers (§1, §2, §3...) based on which sections actually render.

Example: If the rendered brief includes Header, Account at a Glance, Spend Trajectory, Buying Rhythm, and Strategic Summary (canonical §1, §2, §6, §7, §23), display them as §1, §2, §3, §4, §5.

---

## Always-On Sections (9)

These sections render for every customer regardless of gates (though individual subsections may be conditional).

### §1 — Header

**Query**: CQ-01 (customer_info portion) + CQ-23 (lifecycle stage) + Health Score (computed)

**Content**:
- Customer name, code, billing city/state
- Price level (`default_price_code`), territory (`territory_codes`), terms
- Ship-to count
- **Rep name** (v4, audit finding §10): Look up the assigned rep from the customer's `territory_codes`. Query: `SELECT name FROM org_users ou JOIN territories t ON t.org_user_id = ou.id WHERE t.organization_id = {{ORG_ID}} AND t.code = '{{TERRITORY_CODE}}' LIMIT 1`. If found, render as: *"Prepared for: [Rep Name] — Territory [code]"*. If the territory lookup returns no rep or the customer has no territory, render territory code only. If the customer has multiple territory codes, use the first.
- **Lifecycle stage badge**: New / Growing / Stable / Declining / Dormant (from CQ-23)
- **Account Health Score**: Composite 0–100 score with label (Strong / Healthy / Watch / At Risk / Critical). Computed per `authority/health_score_spec.md`. Rendered as progress bar + numeric score. **The score carries the G-00 `COMMERCE_CONFIDENCE` tier** (a composite never exceeds its lowest input — Spine §5.3).
- Last order date + days since last order
- **Risk coloring**: days_since_last_order > 90 = amber, > 180 = red
- **Provenance line** (v5): one line stating the Total's source/confidence/completeness from G-00, e.g. *"Total business: invoiced through 2026-05-31 · UNVERIFIED — SINGLE FEED · STRONG."* If `FEED_COMPLETENESS ∈ {PROVABLY INCOMPLETE, DEAD}`, this line states the Total is suppressed and why.

**Format**: Compact metadata block at top of brief. No prose — data only. Health score bar renders as:
```
Prepared for: Blake Fisher — Territory MW
GROWING ████████████████████░░░░  Score: 82/100 (Strong · STRONG confidence)
Total business: invoiced through 2026-05-31 · UNVERIFIED — SINGLE FEED · STRONG
```

---

### §2 — Account at a Glance

**Query**: CQ-01

**Content**:
- Total business LTM: txn count, **invoiced net** (`total_business_ltm`), last order date — with the G-00 provenance label (source/completeness/confidence). On `INVOICES` this is invoiced `net_amount`; on `ORDERS` it is booked GMV, labeled "booked"; on `PROVABLY INCOMPLETE`/`DEAD` it is **suppressed**.
- Total business prior year: txn count, **invoiced net** (`total_business_prior`)
- YoY change with directional arrow (↑ / ↓ / →) — from `total_business_yoy_pct` (computed on the canonical invoiced Total, not booked)
- **Conditional**: eCat metrics (orders, GMV, AOV, **capture %** = `ecat_capture_pct_display`, capped ≤100%) — only if `HAS_ECAT_ORDERS = true` AND customer has eCat orders > 0. Label this **eCat capture**, not "penetration of total business," and footnote `ecat_capture_pct_raw` only when it exceeds 100% (the incompleteness signal). If eCat = 0 for this customer, render single-line note: *"Account does not use eCat iPad — orders via [dominant channel from CQ-12]"*
- Days since last order as recency signal (computed against `report_through_date`, not `CURRENT_DATE`)
- **Competitive loss signal**: If CQ-01 shows `ecat_yoy_pct < 0` AND `total_business_yoy_pct > 0` (both now on **invoiced** truth), render callout: *"eCat capture declined [X]% while invoiced total business grew [Y]%. The ~$[gap] divergence suggests channel shift or competitive displacement."* The gap = `ecat_gmv_prior * (total_business_yoy_pct - ecat_yoy_pct) / 100`. **Suppressed when the Total is suppressed** (`PROVABLY INCOMPLETE`/`DEAD`) — it rides the invoiced Total. Also feeds into health score as a -5 penalty. See §16 (v4) for the promoted top-of-brief banner treatment.

**Format**: Summary table with YoY comparison columns + the provenance label line. Competitive loss callout (if applicable) below the table.

---

### §3 — Purchase DNA: Categories

**Query**: CQ-02 | **Gate**: `HAS_PORTAL_INVOICES`

**Content**:
- Category breakdown: name, LTM revenue, % of spend, units, YoY change %
- `is_new_category` flag for categories appearing only in LTM
- **Uncategorized callout** (v4, audit finding §12 — standardized tiered format):

  | Uncategorized % | Callout |
  |-----------------|---------|
  | ≤ 15% | No callout — acceptable noise level |
  | 16–50% | *"⚠ [X]% of spend ($[Y]) is uncategorized — category assignments in the product catalog would sharpen this analysis."* |
  | > 50% | Prominent callout at TOP of section: *"⚠ Category analysis limited: [X]% of this customer's spend ([Y] of [Z] items) has no product category assigned. The breakdown below covers only the categorized portion. Contact [org] about catalog enrichment to unlock full category-level intelligence."* |

  The >50% callout goes before the table, not after. The brief should still render whatever categorized data exists — partial category data is better than none.

**Format**: Table sorted by revenue DESC. YoY change with directional indicators.

**Prototype validation**: Single most valuable section across all 7 briefs. Star Furniture's motion collapse (-79%), Ferguson's sconce breakout (+225%), Capitol Lighting's furniture retreat — all surfaced here. v3 pilot: 11/12 scanned briefs had >25% uncategorized; 3 had >89%. Standardized callout format ensures consistent handling.

---

### §4 — Purchase DNA: Top Items

**Query**: CQ-03 | **Gate**: `HAS_PORTAL_INVOICES`

**Content**:
- Top 15 SKUs by revenue: item number, description, collection, units, revenue
- Inventory cross-reference: qty_available, qty_on_hand, qty_on_backorder, next_receipt_date
- **Ghost SKU vs. stock-out disambiguation** (v4, audit finding §3): Items with `qty_available = 0` must be classified into one of two distinct alert types based on whether the item has a matching product record:

  **Type 1 — Real Stock-Out** (item EXISTS in `products` table with `deleted=false`):
  Format: *"⚠ STOCK OUT — [item] ([description]) — [X] units sold LTM, 0 available, next receipt [date or 'no date scheduled']"*
  - These items can be cross-referenced with inventory, backorder status, and receipt dates.
  - Show alternative SKU suggestions (CQ-24) below each stock-out alert.

  **Type 2 — Ghost SKU** (item has NO matching record in `products`, or product is `deleted=true`):
  Format: *"⚠ GHOST SKU — [item] — [X] units invoiced LTM, no catalog record. Cannot verify stock status, description, or collection."*
  - Do NOT show inventory columns (they are meaningless for items not in the catalog).
  - Do NOT show alternative SKU suggestions (no collection to match against).
  - Do NOT present 0 available stock as a fulfillment problem — the item is simply untracked.

  **Detection rule**: In CQ-03 results, a ghost SKU is identified when the LEFT JOIN to `products` returns NULL for `long_description`. Equivalently: `p.item_number IS NULL` or `p.long_description IS NULL`.

- **Alternative SKU suggestions** (CQ-24): For each **real stock-out** item (Type 1 only) with a `collection_code`, show up to 3 same-collection alternatives that are in stock. Formatted as: *"Alternative: [item] ([description]) — [qty] available"* directly below each stock-out alert.

**Format**: Table with embedded inventory columns. Alert callout box precedes the table, with stock-outs and ghost SKUs in separate groups. Stock-outs first (actionable), then ghost SKUs (informational).

**Prototype validation**: Found stock-out risks in every brief — Baer's had 6/15 at zero, Nebraska's #2 item down to 28 units. v3 pilot found 7/12 scanned briefs had ghost SKUs that were visually identical to real stock-outs — now disambiguated.

---

### §5 — New Introduction Adoption

**Query**: CQ-05 | **Gate**: `HAS_PORTAL_INVOICES` AND `HAS_NEW_ITEMS` (v4, audit — empty section fix)

**Content**:
- Count of org's new items vs. how many this customer purchased
- Cohort average for comparison
- Top 5 new items this customer HASN'T purchased but similar customers (same state) have

**Format**: Summary stat + recommendation table.

**Guard** (v4): If `HAS_NEW_ITEMS` gate fails (org has zero products with `new_item=true`), skip this section entirely. Do not render an empty "No new items flagged" placeholder.

---

### §6 — Spend Trajectory

**Query**: CQ-10

**Content**:
- Quarterly revenue, order count, AOV for last 8 quarters
- QoQ change column (calculated: `(current - prior) / prior * 100`)
- Inflection point narrative if QoQ swing > 30%

**Format**: Table with 8 quarterly rows. QoQ change with directional indicators.

---

### §7 — Buying Rhythm

**Query**: CQ-07 (frequency) + CQ-08 (seasonality)

**Content**:
- Frequency metrics table with three columns — This Customer | Org Median | Percentile:
  - Orders per month: `orders_per_month` | `org_median_orders_per_month` | Top `100 - percentile_rank`%
  - Avg days between orders: `avg_days_between` | — | —
  - Active months (of last 12): `MIN(active_months, 12)` | — | — (v4, audit finding §8: cap display at 12. If `active_months > 12` due to LTM window spanning partial calendar months, display "12" and append note: *"All months active."* The underlying CQ-07 query may return 13 because `DATE_TRUNC('month', ...)` can count a partial month at each boundary — this is cosmetic, not a data error.)
- **Predicted next order window**: Derived from `last_order_date + avg_days_between` (CQ-07 + CQ-01). Rendered as a date range (center date ± 2 days). If the predicted date is already past, flag as: *"Predicted window was [date range] — [X] days overdue."* Guard: only render if `avg_days_between` is not null AND `total_orders >= 3`.
- Monthly seasonality (v4, audit finding §7 — ASCII bar chart visualization):
  - Show trailing 12 months of revenue as an ASCII bar chart (matching the Magnolia example format).
  - Bar width is proportional to revenue: max revenue month = 16 `█` characters. Other months scale linearly. Pad remaining width to 16 with `░`.
  - Format per line: `Mon ████████████░░░░  $XXK  [← annotation if peak/trough]`
  - Highlight top 3 revenue months with `← Peak` annotation.
  - If a month has zero orders but the same month in the prior year had activity, annotate with `← Gap (was $XXK last year)`.
  - Fall back to plain table format if the customer has fewer than 6 months of order history (insufficient data for meaningful visualization).
- Peak months highlighted (top 3 by revenue)
- **Gap detection**: If most recent 2 months show zero orders but historical pattern has activity, flag as potential rhythm break

**Format**: Frequency metrics as a comparison table (including org median and percentile rank), predicted next order as a stat line, seasonality as ASCII bar chart in a code block.

**ASCII bar chart spec**:
```
Jan ████████░░░░░░░░  $18K
Feb ██████░░░░░░░░░░  $14K
Mar ████████████░░░░  $28K  ← Peak (Pre-Spring Market)
Apr ██████████████░░  $32K  ← Peak
May ████████░░░░░░░░  $19K
Jun ██████████░░░░░░  $22K
Jul ████████░░░░░░░░  $17K
Aug ██████░░░░░░░░░░  $13K
Sep ████████████░░░░  $26K  ← Peak
Oct ██████████████░░  $31K
Nov ████████░░░░░░░░  $19K
Dec ████░░░░░░░░░░░░  $11K
```

---

### §8 — Channel Mix

**Query**: CQ-12

**Content**:
- Channel breakdown: channel name, orders, revenue, % of orders
- **Single-line characterization**: Classify as one of:
  - "EDI-dominant" (EDI > 70%)
  - "Rep-driven" (REP > 50%)
  - "Self-service" (CUSTOMER > 50%)
  - "Mixed channel" (no single channel > 50%)

**Format**: Compact table with characterization label.

---

### §9 — Wallet Share

**Query**: CQ-22

**Content**:
- Customer LTM revenue
- Same-state cohort: average revenue, max revenue, cohort size
- **Minimum cohort size** (v4, audit finding §11): If the state cohort has **fewer than 5 customers** (i.e., `cohort_size < 5` from CQ-22 Step 2), add disclaimer: *"⚠ Small cohort ([N] customers in [state]) — comparison is indicative only."* If cohort_size < 3, skip the cohort comparison entirely and render only: *"Wallet share comparison unavailable — fewer than 3 peers in [state]."* Show customer LTM revenue as a standalone stat.
- **Rank signal**: computed from customer revenue vs. cohort:
  - If customer > cohort_max * 0.9: *"Dominant — [X]% of state revenue"*
  - If customer > cohort_avg * 2: *"Top tier — [X]x the average [state] customer"*
  - If customer < cohort_avg * 0.5: *"Below cohort — opportunity to grow to state average"*

**Format**: Stat comparison with narrative label.

**Prototype validation**: Reframed every account relationship. Nebraska at 89% of NE, Ferguson at 39% of VA — these numbers change how a rep approaches the conversation. v3 pilot found fsf/03053 had a cohort of only 3 MA customers — too small for reliable comparison.

---

## Conditional Sections (6)

These sections only render when their gate is `true` AND the customer has relevant data.

### §10 — Market Commitments

**Query**: CQ-17 + CQ-25 (conversion analysis) | **Gate**: `HAS_COMMITMENT_REPORTS` AND customer has > 0 reports

**Content**:
- Commitment history: market code, date, item count
- Trend narrative: growing/stable/declining commitment volume
- Staleness flag if last commitment > 12 months ago
- **Conversion analysis** (CQ-25): For the most recent commitment (and optionally prior):
  - Overall conversion rate: items committed vs. items ordered post-commitment
  - Per-category conversion: which committed categories converted, which didn't
  - Uncommitted items: list with current inventory status (qty_available from `inventories`)
  - Firm vs. soft: items with `commitment_quantity > 0` are firm; `interest_quantity` only is soft interest

**Format**: History table + conversion summary table. Uncommitted items rendered as actionable list: *"[item] ([description]) — committed [qty], zero ordered, [stock status]"*

**Prototype validation**: Strong for UFI (Baer's APR2026 drop from 112 → 23 items). Conversion analysis adds the "so what" — which commitments turned into revenue and which didn't.

---

### §11 — Showroom Placements

**Query**: CQ-18 | **Gate**: `HAS_PLACEMENT_REPORTS` AND customer has > 0 reports

**Content**:
- Placement records: location, ship-to, item count, dates
- **Staleness alert**: If `days_since_update > 365`, flag as: *"⚠ Placement data is [X] days old — showroom audit recommended."*

**Format**: Table with staleness indicator.

**Prototype validation**: Data universally stale for UFI (2019-2020). The staleness itself is the insight — nobody has audited in 6 years.

---

### §12 — Rep Engagement

**Query**: CQ-13 + Engagement Score (computed per `authority/health_score_spec.md`) | **Gate**: `HAS_MIXPANEL_CUSTOMER` AND customer has events

**Content**:
- **Engagement score**: `X.X/10` with intensity label (High / Moderate / Low) and session-to-order rate. Computed from 4 components per `health_score_spec.md`: session-to-order rate (E1), event volume (E2), event diversity (E3), recency (E4). Rendered as: *"Engagement score: 8.4/10 — 31% session-to-order rate (vs. avg 12%)"*
- Event mix: event name, count (top 20)
- Rep breakdown: rep name, total events, orders submitted, searches, first/last activity
- **Handoff detection**: If > 1 rep active in last 6 months, flag as potential handoff and show timeline

**Format**: Engagement score as a headline stat, followed by two tables (event mix + rep breakdown).

**Prototype validation**: Transformational for SC. Kristen Finney (359 events, 3 reps) vs. Ashley Gilbreath (71 events, 5-month blackout) is the strongest contrast in the prototype set.

---

### §13 — Buyer Intelligence

**Query**: CQ-14 | **Gate**: `HAS_BUYER_NAMES` AND customer has > 1 distinct buyer with revenue

**Content**:
- Buyer breakdown: name, orders, revenue, % of revenue, first/last order
- New buyer detection: `is_new_buyer` if first order < 6 months ago
- Key person risk: if one buyer > 80% of revenue, flag as concentration risk

**Format**: Table with new buyer and concentration flags.

**Prototype validation**: Mostly empty in prototypes (buyer_name unpopulated for EDI accounts). Valuable when populated.

---

### §14 — Returns

**Query**: CQ-16 | **Gate**: `HAS_RMA` AND customer has > 0 returns

**Content**:
- Return breakdown: reason, item, count, units, date range
- Return rate relative to order volume if calculable

**Format**: Table. Skip entirely if no data — no "No returns found" placeholder.

**Prototype validation**: Zero data across all 7 test customers. Gate prevents rendering empty sections.

---

### §15 — Collection Mix

**Query**: CQ-04 | **Gate**: `COLLECTION_COVERAGE >= 50%` AND `HAS_PORTAL_INVOICES`

If `COLLECTION_COVERAGE < 50%`: fold into a single note under §3 (Categories): *"Collection data is sparse ([X]% coverage) — category-level analysis provides more reliable segmentation."*

**Content**:
- Collection breakdown: name, revenue, % of spend
- Only standalone section when collection taxonomy is well-populated

**Format**: Table sorted by revenue DESC.

---

## Advanced Insights (6)

These represent the premium analysis tier. Validated against live data across 22+ briefs.

### §16 — Reorder Decay Detection

**Query**: CQ-09 | **Gate**: `HAS_PORTAL_INVOICES` AND customer has ≥ 3 reorder cycles on any item

**Content**:
- Items where latest reorder interval exceeds historical average by > 20%
- Status classification: `ON_PACE`, `SLOWING` (> 1.2x avg), `DECAY_DETECTED` (> 1.5x avg)
- Historical avg, latest interval, and prior 2 intervals for trend visibility
- **Minimum interval filter**: Only items with avg_interval ≥ 7 days. Sub-daily cadences (warehouse/distribution accounts) produce false positives.
- **Inventory correlation note**: If a decaying item also shows `qty_available = 0` in CQ-03, add note: *"Stock-out may explain gap — verify if demand-driven or supply-constrained."*

**Format**: Alert table — only items with `SLOWING` or `DECAY_DETECTED` status shown.

**Validation**: Baer's returned 10 items with decay detected (Weekender collection: 36 reorders, avg 17.8 days, latest 53 days). Savoy House 71200 confirmed false positive risk at sub-daily intervals.

---

### §17 — Next Best Product

**Query**: CQ-06 (or CQ-06 recent-window variant) | **Gate**: `HAS_PORTAL_INVOICES` AND V-01 tiered volume check (see `customer_gate_rules.md`)

**Content**:
- For each of customer's top 5 items: items that other customers commonly purchase next (within 90 days)
- Only items the target customer has NOT already purchased
- Minimum 3 customers must show the pattern for inclusion
- **Volume-tiered approach** (v4, audit finding §4):
  - ≤ 5,000 LTM orders: Run CQ-06 as-is (full LTM window)
  - 5,001–50,000 LTM orders: Run CQ-06 **recent-window variant** (6-month invoice window for the sequence_pairs CTE). Add note: *"Based on most recent 6 months of purchase patterns."*
  - > 50,000 LTM orders: Skip entirely. Render: *"Purchase sequence analysis unavailable for ultra-high-volume accounts."*
- **MKTG/sample filter**: If results are dominated by marketing/sample SKUs (MKTG- prefix, $0 items), note reduced actionability.

**Format**: Recommendation table: anchor item → suggested next item, backed by customer_count.

**Validation**: Baer's showed 52 customers with Weekender Dresser → Long Key King Bed pattern. Timed out on Savoy House 71200 (83K orders). v4 recent-window approach enables analysis for mid-tier high-volume accounts that were previously blocked.

---

### §18 — Cross-Sell Opportunity

**Query**: CQ-19 (with v4 cohort fallback) | **Gate**: `HAS_PORTAL_INVOICES` AND cohort_spend returns ≥ 1 category gap

**Content**:
- Categories where cohort average exceeds this customer's spend
- Gap quantified in dollars
- Only categories where ≥ 5 cohort customers have data (statistical relevance threshold)
- **Cohort selection strategy** (v4, audit finding §5 — tiered fallback):

  The generator must try cohort definitions in this order, stopping at the first that yields ≥ 5 qualifying customers:

  | Priority | Cohort Definition | When It Works |
  |----------|-------------------|---------------|
  | 1 (default) | Same state + within 2x LTM revenue | Ideal for typical accounts with peers in the same state at a similar spend level |
  | 2 (fallback) | Same state, any revenue | Use when the spend-filtered cohort is too small (common for dominant accounts) |
  | 3 (fallback) | Org-wide, within 2x LTM revenue | Use for states with <5 total customers, or when the target account dwarfs all in-state peers |

  **Dominance guard**: If the target customer's LTM revenue exceeds the cohort average by >10x under any definition, add note: *"⚠ This account is [X]x the cohort average — cross-sell gaps reflect the account's outsized scale, not missed opportunities."* This prevents the brief from suggesting a $400K account should buy like a $4K average peer.

  Report which cohort tier was used: *"Compared against [N] [state/org-wide] customers [with similar revenue]."*

**Format**: Gap table sorted by largest gap, with cohort source noted.

**Validation status**: v3 pilot found state-level cohorts produced absurd results when the target dwarfs peers (Wayfair at 474x MA avg). v4 tiered approach provides meaningful comparisons across all account sizes.

---

### §19 — Same-Store Performance

**Query**: CQ-21 | **Gate**: `HAS_SHIP_TO_DATA` AND customer has 2+ distinct ship-to locations with order activity

**Content**:
- Per-location breakdown: ship-to code, location name, city, state, LTM orders, LTM revenue
- Top 15 locations by revenue
- Useful for multi-location accounts (retailers with branches, DCs, showrooms)

**Format**: Table sorted by revenue DESC. If only 1 ship-to location, skip this section entirely.

**Validation**: Craftmade/Ferguson 9800 returned 15+ ship-to locations (distribution centers + branches) with clear revenue ranking. 5 of 7 tested orgs have 100% ship-to population; UFI and SHL do not (gate correctly blocks).

---

### §20 — Fulfillment Impact on Reorder Behavior

**Query**: CQ-26 | **Gate**: `HAS_PORTAL_INVOICES` AND `FILL_RATE_POPULATION` (v4, audit §2) AND customer has backorder events (CQ-15 `total_backordered > 0`)

**Fill rate population guard** (v4): Before computing ANY fill rate metrics for this customer, check the org-level `FILL_RATE_POPULATION` gate (G-10). If the gate fails (< 50% of `quantity_invoiced` values are non-zero), **skip this entire section** and render: *"Fill rate data unavailable — this org does not populate invoice quantities."* This prevents false 0% fill rate alarms for orgs that don't track invoice quantities (confirmed: fsf, jyc, ril in v3 pilot).

**Content**:
- Per-item comparison: normal reorder interval vs. post-backorder interval, with slowdown multiplier
- Only items with sufficient data (≥ 2 normal intervals + ≥ 1 post-backorder interval)
- **Annualized revenue impact**: For items with `slowdown_multiplier > 1.0`, estimate lost revenue as `item_ltm_revenue * (1 - 1/slowdown_multiplier)`. Sum across all affected items for total impact.
- Render as: *"When backordered, this customer's reorder interval for [item] increases [X]x ([normal] days → [post-backorder] days). Projected impact from delayed reorders: -$[impact] annualized."*

**Format**: Alert table with items sorted by slowdown_multiplier DESC. Total annualized impact as a summary stat.

**Guard**: Skip entirely if CQ-15 shows `total_backordered = 0` or if CQ-26 returns no qualifying items. Not all orgs populate backorder quantities.

---

### §21 — Category Share Evolution

**Query**: CQ-20 | **Gate**: `HAS_PORTAL_INVOICES` AND customer has both LTM and prior-year data

**Content**:
- Category share comparison: LTM % vs. prior-year %, share shift in percentage points, revenue change
- Surfaces mix shifts even when total spend is flat
- Most useful for large accounts where absolute revenue may be stable but composition is changing

**Format**: Table with share shift column. Sorted by largest absolute shift.

**Validation**: Star Furniture showed clear drift (Motion collapsed from dominant to minor, Dining/Bedroom grew). Clean data, strong narrative value.

---

## Account Health (Always-On)

### §22 — Account Health Score Breakdown

**Query**: Health Score (computed) + CQ-23 (lifecycle + cohort forecasting)

**Content**:
- Per-signal breakdown table showing each health signal, its status, and points earned
- Competitive loss penalty line (if applicable)
- Total score with label
- Lifecycle stage from CQ-23 alongside the score for dual framing (stage = qualitative, score = quantitative)
- **Cohort lifecycle position** (from CQ-23 extended):
  - Relationship tenure: `relationship_months` months
  - vs. same-tenure cohort: `vs_cohort_pct`% (above/below curve)
  - Projected peak: `projected_peak_revenue` at Year `peak_tenure_years`
  - Addressable growth: `addressable_growth` if trajectory holds
  - Guard: only render forecast if CQ-23 returns `peak_cohort` data. If customer is already above all cohort benchmarks, note: *"Tracking above cohort curve — no higher-tenure benchmark available."*

**Format**: Signal breakdown table as shown in health_score_spec.md followed by lifecycle position narrative. Only include signals that were available (gated-on). Mark skipped signals as "N/A (data unavailable)" without penalizing the score.

**Guard**: Health score requires at least 3 scored signals. If fewer, render lifecycle stage label only with note: *"Health score requires more data signals — lifecycle stage shown instead."* Cohort forecast renders independently of health score.

---

## Strategic Summary (Always-On)

### §23 — Strategic Summary & Pre-Meeting Priorities

**Query**: None — synthesized from all rendered sections

**Content** (v4, audit finding §6 — expanded from 3 to 5-6 talking points):

The Strategic Summary has two parts:

**Part A — Situation Assessment** (2-3 bullets):
  1. **Strengths**: What's working (growing categories, strong wallet share, increasing commitments)
  2. **Risks**: What needs attention (declining categories, stock-outs on top items, dormant eCat, stale placements, reorder decay)
  3. **Opportunities**: Where to push (cross-sell gaps, new introductions not yet purchased, under-penetrated categories)

**Part B — Pre-Meeting Priorities** (5-6 numbered items, priority-sequenced):
  - Items are numbered 1–6 in descending priority order.
  - **Priority logic**: Revenue-at-risk items first (stock-outs on top SKUs, reorder decay on high-revenue items, fulfillment gaps), then growth opportunities (cross-sell gaps, uncommitted market items, new intros), then relationship items (new buyer relationships, rep handoff follow-up, placement refresh).
  - Each item must reference a specific data point: SKU number, dollar amount, date, or percentage from a rendered section.
  - Format each as: *"[Priority verb] [specific thing] — [data point and context]"*
  - Example: *"1. Flag Harlow Sofa backorder (their #2 item, $19.2K LTM) — zero available, next receipt July 12. Present Harlow Loveseat alternative (9 in stock)."*

  If the brief has fewer than 5 actionable findings, produce as many as the data supports (minimum 3). Do not pad with generic statements.

**Format**: Part A as bulleted narrative. Part B as a numbered list with clear priority sequencing ("Close this first, then explore this"). This is the "so what" section — it reads all prior sections and produces the synthesis.

**Hard rule**: Every bullet/item must cite a specific data point from a rendered section. No generic statements. No claims not backed by the data.

---

## Section Dependencies

```
§1 Header ← CQ-01, CQ-23, Health Score (computed)
§2 Account at a Glance ← CQ-01, CQ-12 (for channel note)
§3 Categories ← CQ-02
§4 Top Items ← CQ-03, CQ-24 (stock-out alternatives)
§5 New Intros ← CQ-05
§6 Trajectory ← CQ-10
§7 Rhythm ← CQ-07, CQ-08, CQ-01 (for predicted next order)
§8 Channel ← CQ-12
§9 Wallet Share ← CQ-22
§10 Commitments ← CQ-17, CQ-25 (conversion analysis)
§11 Placements ← CQ-18
§12 Rep Engagement ← CQ-13, Engagement Score (computed)
§13 Buyer Intel ← CQ-14
§14 Returns ← CQ-16
§15 Collection Mix ← CQ-04
§16 Reorder Decay ← CQ-09
§17 Next Best Product ← CQ-06
§18 Cross-Sell ← CQ-19
§19 Same-Store Performance ← CQ-21
§20 Fulfillment Impact ← CQ-26, CQ-15 (backorder gate), CQ-03 (item revenue)
§21 Category Evolution ← CQ-20
§22 Health Score ← CQ-01, CQ-02, CQ-07, CQ-15, CQ-17, CQ-20 (all signal sources)
§23 Strategic Summary ← All rendered sections
```

---

## Rendering Order

Sections are rendered in the order listed (§1 through §23). §22 (Health Score) is built after all data sections. §23 (Strategic Summary) is always built LAST because it synthesizes all prior sections including the health score. All other sections are independent and can be built in parallel.
