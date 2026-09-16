# Section 3 Context Bundle — Currey & Company (cci)
Run date: 2026-06-16

## Gate Flags

# Gate Flags — Currey & Company (cci, org_id=161)
- **Run date**: 2026-06-16
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=57914, portal_order_gmv=$88.1M |
| HAS_INVENTORY | True | inventory_count=3441 |
| HAS_SALES_DATA | True | sales_data_count=110629 |
| HAS_SALES_SECTION | True | qualifying_reps=37 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | N/A |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$88.1M > ecat_gmv=$8.6M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 37 | 37 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 76 rows |
| SHOWROOM_EXCLUSIONS | 3 | 3 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 3983, Mixpanel total submit_order (Q-01): 6587 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=97.4%, ambiguous_rate=0.0%, showroom_event_share=8.5% |
| USER_GROUP_JOIN_RATE | 97% | 74 of 76 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 9% | showroom+admin share of matched events: 8.5% |
| ADMIN_REPS_IN_LEADERBOARD | True | 4 admin/showroom users in leaderboard: Atlanta Showroom, CC Dallas Showroom, Highpoint Showroom, Allan Otto |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=53 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=7919 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=369 |
| HAS_BUYER_DATA | True | distinct_buyers_6mo=3204 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Currey & Company
- **Shortname**: cci
- **Org ID**: 161
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Currey & Company (cci, org_id=161)
- **Run date**: 2026-06-16

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | True |
| PORTAL_CUSTOMER_DATA_PRESENT | True |
| PORTAL_ORDERS_FRESH | True |
| HAS_PORTAL_ORDERS | True |
| HAS_INVENTORY | True |
| HAS_SALES_DATA | True |
| INVENTORY_FRESH | True |
| SALES_DATA_FRESH | False |
| CUSTOMER_DATA_FRESH | True |

## Computed Tiers

| Section | Tier | Determining Condition |
| --- | --- | --- |
| §2 Sales Team | FULL | See Derived Gate 6 §2 formula |
| §3 Customer | FULL | See Derived Gate 6 §3 formula |
| §4 Product | STRONG | See Derived Gate 6 §4 formula |
| §5 Commerce | FULL | See Derived Gate 6 §5 formula |

## Section Guide — section_03_customers.md

# Section Guide: §3 — Customer & Buyer Intelligence
> **v1.1** — updated 2026-06-16 (CCI hardening run). Last updated: 2026-06-16.

## Section Identity
- **id**: `customers`
- **title**: Customer & Buyer Intelligence
- **section number**: 3
- **include when**: Always
- **skip when**: Never — this section is always rendered

## Query Inputs

Read these cache files:
- `cache/Q-12_results.md` — Customer activation & network health
- `cache/Q-14_results.md` — Reorder velocity & early warning
- `cache/Q-17_results.md` — Dormant high-value accounts
- `cache/Q-40_results.md` — Geographic distribution of eCat orders
- `cache/Q-41_results.md` — New eCat buyer acquisition
- `cache/gate_flags.md` — for `HAS_CART`, `PORTAL_CUSTOMER_DATA_PRESENT`
- `cache/Q-52_results.md` — eCat penetration of total business by customer (**MANDATORY when gate met**: if `PORTAL_CUSTOMER_DATA_PRESENT = true` AND this file contains data rows, subsection 2 MUST be rendered)
- `cache/Q-53_results.md` — Unactivated high-value accounts in business system with zero eCat history (**MANDATORY when gate met**: if `PORTAL_CUSTOMER_DATA_PRESENT = true` AND this file contains data rows, subsection 4 MUST be rendered)
- `cache/Q-54_results.md` — Geographic total-business enrichment by state (**MANDATORY when gate met**: if `PORTAL_CUSTOMER_DATA_PRESENT = true` AND this file contains data rows, subsection 5 MUST include enrichment columns)
- `cache/Q-14b_results.md` — Account velocity deceleration detection (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND this file contains data rows, subsection 6b MUST be rendered)
- `cache/Q-57_results.md` — Cross-sell whitespace by category (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND `PORTAL_CUSTOMER_DATA_PRESENT = true` AND this file contains data rows, subsection 8 MUST be rendered)
- `cache/Q-66_results.md` — Buyer-within-account intelligence (conditional: render subsection 9 if `HAS_PORTAL_ORDERS = true` AND `HAS_BUYER_DATA = true` AND data rows exist)
- `cache/Q-67_results.md` — Geographic revenue displacement (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND `PORTAL_CUSTOMER_DATA_PRESENT = true` AND this file contains data rows, subsection 10 MUST be rendered)
- `cache/Q-68_results.md` — Spending Contraction Detection (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND `PORTAL_CUSTOMER_DATA_PRESENT = true` AND this file contains data rows, subsection 11 MUST be rendered)
- `cache/section_confidence.md` — for `SECTION_CONFIDENCE_3` tier

## PRE-BUILD GATE CHECK — Complete Before Writing Any HTML

**Before generating any HTML**, read `gate_flags.md` and check each cache file below. Record which MANDATORY subsections will render. Skipping a MANDATORY subsection when its gate is met = defective fragment.

| Cache File | Gate Condition | If gate met + data rows exist → | Subsection |
|---|---|---|---|
| `Q-52_results.md` | `PORTAL_CUSTOMER_DATA_PRESENT = true` | **MUST render** | 2 (eCat Penetration) |
| `Q-53_results.md` | `PORTAL_CUSTOMER_DATA_PRESENT = true` | **MUST render** | 4 (Unactivated High-Value) |
| `Q-54_results.md` | `PORTAL_CUSTOMER_DATA_PRESENT = true` | **MUST add enrichment columns** | 5 (Geographic) |
| `Q-14b_results.md` | `HAS_PORTAL_ORDERS = true` | **MUST render** | 6b (Deceleration Alert) |
| `Q-57_results.md` | `HAS_PORTAL_ORDERS = true` + `PORTAL_CUSTOMER_DATA_PRESENT = true` | **MUST render** | 8 (Cross-Sell Whitespace) |
| `Q-67_results.md` | `HAS_PORTAL_ORDERS = true` + `PORTAL_CUSTOMER_DATA_PRESENT = true` | **MUST render** | 10 (Geographic Trends) |
| `Q-68_results.md` | `HAS_PORTAL_ORDERS = true` + `PORTAL_CUSTOMER_DATA_PRESENT = true` | **MUST render** | 11 (Spending Contraction) |

**Write down your list of MANDATORY subsections that will render before proceeding.** Use this list as a checklist while building.

## CRITICAL REQUIREMENTS

These rules are non-negotiable. Failing ANY of them produces a defective fragment:

1. **ERP ENRICHMENT SUBSECTIONS**: Every row in the Pre-Build Gate Check table above where the gate is met AND the cache file has data rows MUST produce a rendered subsection. If you skip one, the fragment is defective. HFG and BCF prove these render correctly — if CCI or UFI are missing them, the section builder is the problem, not the data.
2. **CONFIDENCE FOOTER**: Every §3 fragment MUST contain a confidence footer. Read `SECTION_CONFIDENCE_3` from `section_confidence.md` — use the EXACT tier value, do NOT infer it from gate flags. Position: FULL=bottom, STRONG/PARTIAL/LIMITED=top (after metrics, before first subsection).
3. **VERIFICATION**: After building, run through the Conditional Subsection Checklist at the bottom of this guide. Cross-check against your Pre-Build Gate Check list. Fix any failures before saving.

---

## Subsection Order (do not reorder — render in the order below)

### 1. Customer Activation & Network Health (Q-12)

Build from `Q-12_results.md`. Surface total account base size, active vs. inactive customer counts, and activation rates.

### 2. eCat Penetration of Total Business (Q-52)

**MANDATORY RENDER**: If `cache/Q-52_results.md` exists AND contains data rows AND `PORTAL_CUSTOMER_DATA_PRESENT = true` in `gate_flags.md`, this subsection MUST appear in the fragment. Omit ONLY when the file is absent, contains zero rows, or the gate is false.

**Data source**: `cache/Q-52_results.md`

**Rendering**: Table with top 15 customers by total business GMV:

| Column | Content |
|--------|---------|
| Customer Name | Display name (never expose `customer_code`) |
| State | Customer state |
| Total Business Orders | All-channel order count |
| Total Business GMV | All-channel GMV |
| eCat Orders | eCat-originated order count |
| eCat GMV | eCat-originated GMV |
| eCat Penetration % | `ecat_gmv / total_business_gmv × 100` |

Highlight customers with eCat Penetration > 50% using `.row-highlight` class. Show top 5 visible; remaining in a collapsed `<details>` element.

**Framing principle**: The penetration spread tells a story about where the platform is winning and where it's invisible. The what-this-means should identify geographic or customer-segment patterns in the penetration data: "Your New York accounts average 45% platform penetration while your California accounts average 8% — is that a territory coverage gap or a market difference?" Frame penetration as a winnable game: "Going from 8% to 20% in California alone would add an estimated $X in platform-attributed revenue."

**Claim rules**: Reference by `customer_name` only — never expose `customer_code`. "Your top account does $X in total business — Y% flows through eCat." Customers at 0% penetration are legitimate — they buy through other channels but haven't adopted eCat. Frame constructively as activation opportunity, not failure.

### 3. Dormant High-Value Accounts (Q-17)

Build from `Q-17_results.md`. Surface accounts that were previously active but have gone dormant, prioritized by historical value.

**Extrapolation tag rule**: Include prior GMV figure only when the `[ESTIMATED]` tag is appropriate (extrapolated annualized GMV). Exact LTM GMV does not require a tag.

Show top 5 dormant accounts by historical value. Remaining in collapsed `<details>`.

### 4. Unactivated High-Value Accounts (Q-53)

**MANDATORY RENDER**: If `cache/Q-53_results.md` exists AND contains data rows AND `PORTAL_CUSTOMER_DATA_PRESENT = true` in `gate_flags.md`, this subsection MUST appear in the fragment. Omit ONLY when the file is absent, contains zero rows, or the gate is false.

**Data source**: `cache/Q-53_results.md`

**Rendering**: Table with top 10 accounts from the business system that have zero eCat history:

| Column | Content |
|--------|---------|
| Customer Name | Display name (never expose `customer_code`) |
| State | Customer state |
| Total Business Orders | All-channel order count |
| Total Business GMV | All-channel GMV |

No `.row-highlight` class — these are opportunity rows, not performance highlights. Show all 10 visible (no collapse needed for this subsection).

**Framing principle**: Lead with the dollar magnitude of the blind spot — these are the client's biggest customers and the platform doesn't even know they exist. Frame as: "Your X highest-value accounts — representing $Y in annual business — have never placed a single platform order. Your reps are managing these relationships entirely offline." This is the "your biggest customers don't know your platform exists" insight.

**Claim rules**: Frame as activation opportunity with dollar-weighted urgency. Reference by `customer_name` only — never expose `customer_code`. Never say "they don't use your platform" — say "they haven't yet placed a platform order" or "their orders flow through other channels." The what-this-means should quantify the activation prize: "If even 10% of this $Y moved onto the platform, that's $Z in net-new platform-attributed revenue — with zero new customer acquisition required."

### 5. Geographic Distribution (Q-40, Q-54)

Build from `Q-40_results.md`. Surface geographic distribution of eCat ordering activity. `[COLLAPSE]`

**MANDATORY ENRICHMENT** (when `PORTAL_CUSTOMER_DATA_PRESENT = true` AND `cache/Q-54_results.md` exists with data rows): You MUST add columns from `cache/Q-54_results.md` to the state table — Total Business Customers, Total Business GMV, eCat Penetration %. Join on state. When `PORTAL_CUSTOMER_DATA_PRESENT = false` OR the file is absent OR it contains zero rows, render the Q-40-only table unchanged — do not add empty columns or placeholders.

**Geographic penetration narrative** (when Q-54 enrichment is present): After the table, add a `.callout.insight` identifying the highest-opportunity state — the one with the most total business GMV but lowest eCat penetration percentage. Frame as an actionable territory target: "Your [State] accounts represent $X in total business but only Y% flows through the platform. Go win [State] — moving penetration from Y% to Z% would add an estimated $W in platform-attributed revenue." Compute the dollar projection using current total business GMV × (target penetration - current penetration). Tag with hedging language. This is the "Go win California" insight.

### 6. Reorder Velocity & Early Warning (Q-14, Q-14b)

Build from `Q-14_results.md`. Surface reorder frequency patterns and flag accounts showing declining reorder velocity as early churn warnings.

Show top 5 high-frequency buyers and flagged decelerating accounts only.

**6b. Account Velocity Deceleration Alert (Q-14b)**

**MANDATORY RENDER**: If `cache/Q-14b_results.md` exists AND contains data rows AND `HAS_PORTAL_ORDERS = true` in `gate_flags.md`, this enrichment MUST be rendered as a second part within subsection 6. Omit ONLY when the file is absent, contains zero rows, or the gate is false.

**Data source**: `cache/Q-14b_results.md`

**Rendering**: After the Q-14 reorder frequency table, add a `.callout.alert` titled "Deceleration Alert" followed by a table:

| Column | Content |
|--------|---------|
| Account | Customer name (never expose `customer_bill_to_number`) |
| Historical Avg | Historical average order interval (days) |
| Recent Avg | Recent 6-month average order interval (days) |
| Deceleration | Ratio displayed as "X.Xx" (e.g., "1.8x") with `.badge.danger` if ≥2.0, `.badge.warn` if 1.5–1.99 |
| Annual Value | LTM all-channel GMV for this account |

Sort by annual GMV descending. Show top 5 visible; remaining in collapsed `<details>`.

After the table, include a summary callout: "X accounts show order frequency stretching beyond 1.5x their historical average. Combined annual value at risk: $Y." Use `.callout.insight` class.

**Claim rules**: "These accounts are ordering less frequently than their established pattern." Always hedge projections: "If this trend continues, projected at-risk revenue is approximately $Z." Use "all-channel order frequency" — never "portal orders" or "ERP." Reference accounts by name only.

### 7. New eCat Buyer Acquisition (Q-41)

Build from `Q-41_results.md`. Surface newly acquired buyers on the eCat platform.

**Framing principle**: Collapse this to a single acquisition stat — do NOT render a month-by-month table. Monthly acquisition counts are background context, not foreground insight. The reader can't do anything with "you acquired 70 new buyers per month" except feel good.

**Required content:**
- Compute the trailing-period average monthly new buyer count from Q-41 data.
- Render as a single `.metric-card` within the section or as a one-line prose stat: "Your platform averaged X new buyers per month over the trailing [period], with Y total new buyers acquired." If `HAS_CART = true`, split by channel: "X via iPad, Y via eCat Online."
- If the trend shows acceleration or deceleration (first-half vs. second-half average differs by ≥25%), add a brief trend note.
- What-this-means: frame as pipeline health — is the acquisition rate sufficient to offset natural attrition?

**Column rule**: The iPad channel is always present. eCat Online is included only if `HAS_CART = true`. If `HAS_CART = false`, show iPad acquisition data only.

`[COLLAPSE]`

### 8. Cross-Sell Whitespace Opportunity (Q-57)

**MANDATORY RENDER**: If `cache/Q-57_results.md` exists AND contains data rows AND `HAS_PORTAL_ORDERS = true` AND `PORTAL_CUSTOMER_DATA_PRESENT = true` in `gate_flags.md`, this subsection MUST appear in the fragment. Omit ONLY when the file is absent, contains zero rows, or either gate is false.

**Data source**: `cache/Q-57_results.md`

**Rendering**: Open with a `.callout.insight` block titled "Untapped Category Opportunity" with a summary: "Your top accounts have zero purchases in X categories where similar accounts are actively buying. Estimated addressable whitespace: $Y." Compute X as count of distinct `missing_category` values; compute Y as sum of `addressable_gap` across all rows.

Then render a table with top 10 rows sorted by `peer_median_spend` descending:

| Column | Content |
|--------|---------|
| Customer | `customer_bill_to_name` (never expose `customer_bill_to_number`) |
| Missing Category | `missing_category` |
| Customer Annual GMV | `customer_annual_gmv` formatted as currency |
| Peer Median Spend | `peer_median_spend` — what similar accounts spend in this category |
| Peers Buying | Count of other accounts actively purchasing in this category |

Show top 5 visible; remaining in collapsed `<details>`.

After the table, render a `<div class="what-this-means">`:

> **What this tells you:** These gaps represent product categories where your existing accounts are buying nothing — but similar accounts are actively purchasing. Each row is a specific conversation starter for your reps: "You buy heavily in Lighting but nothing in Mirrors — other accounts your size typically do both." This isn't a guarantee of captured revenue, but it identifies the lowest-friction expansion paths.

**Claim rules**: Always use hedging language — "estimated addressable whitespace," "if adoption matched peer behavior," "opportunity, not certainty." Never guarantee dollar amounts are capturable. Use "similar accounts" not "peers" in client-facing text. Never expose `customer_bill_to_number`. Never use "ERP" — use "your account base" or "accounts in your system."

### 9. Buyer-Within-Account Intelligence (Q-66)

**Gate**: Render ONLY if `HAS_PORTAL_ORDERS = true` AND `HAS_BUYER_DATA = true` AND `cache/Q-66_results.md` has data rows.

**Display**: Standalone (NOT collapsed). This is a unique signal no other report provides — new decision-maker detection within existing accounts.

**Data source**: `cache/Q-66_results.md`

**Rendering**: Open with a `.callout.insight` titled "New Decision-Maker Detection" summarizing: "X of your accounts show a new buyer placing orders in the last 90 days. The highest-impact: [top account] added a new contact who placed $Y in their first engagement. New decision-makers signal either internal expansion or a changing buying committee — both demand immediate rep attention."

Compute `X` as row count. Identify the top row by `new_buyer_revenue`.

Then render a table of accounts with new buyers (sorted by `new_buyer_revenue` descending):

| Column | Content |
|--------|---------|
| Account | `customer_bill_to_name` |
| New Buyers | `new_buyers` |
| Existing Buyers | `existing_buyers` |
| New Buyer Orders | `new_buyer_orders` |
| New Buyer Revenue | `new_buyer_revenue` formatted as currency |

Show top 5 visible; remaining in collapsed `<details>`.

After the table, render a `<div class="what-this-means">`:

> **What this tells you:** A new name placing orders within an existing account is one of the clearest signals that your customer relationship is evolving — either the business is growing and bringing on additional buyers, or a new decision-maker has taken over the account. In both cases, your rep needs to know immediately. Accounts with new buyers tend to expand to additional product categories within 6 months. Proactive outreach to these contacts — while they're still forming vendor preferences — is the highest-ROI relationship action available.

**Claim rules**: Never expose `buyer_name` or `customer_bill_to_number`. Use only account name. Frame as "new decision-maker detected" — expansion opportunity that demands immediate rep relationship-building. Never use "ERP." Never reveal internal buyer identifiers.

### 10. Geographic Revenue Trends (Q-67)

**Gate**: Render ONLY if `HAS_PORTAL_ORDERS = true` AND `PORTAL_CUSTOMER_DATA_PRESENT = true` AND `cache/Q-67_results.md` has data rows.

**Display**: Standalone (NOT collapsed). This is the strongest new insight in the CCI batch — quarter-over-quarter geographic shift analysis that no other section provides. Place AFTER the existing Geographic Distribution subsection (5).

**Data source**: `cache/Q-67_results.md`

**Rendering**: This is a standalone geographic analysis subsection (separate from subsection 5's static distribution view). Open with a `.callout.insight` titled "Geographic Revenue Shifts" with a punchy data-driven headline. Build it dynamically:

1. Identify the state with the largest positive `gmv_change_pct` — this is the "breakout market."
2. Identify the state with the largest negative `gmv_change_pct` — this is the "contracting market."
3. Construct the headline: "[Breakout state full name] grew [X]% quarter-over-quarter ($[prior]→$[current]) while [contracting state full name] contracted [Y]%. Your reps added [N] net new customers in growing states — that's market share being won in real time."

Example output: "Virginia grew 102% quarter-over-quarter ($361K→$730K) while Utah contracted 35.6%. Your reps added 57 net new customers in Virginia alone — that's market share being won in real time."

Use full state names in the callout headline (Virginia, not VA). Table rows may use abbreviations.

Then render a table of states (top 15 by `current_gmv` descending):

| Column | Content |
|--------|---------|
| State | `state` (abbreviation acceptable in table) |
| Current Quarter | `current_gmv` formatted as currency |
| Prior Quarter | `prior_gmv` formatted as currency |
| QoQ Change | `gmv_change_pct` with `.badge.ok` if positive, `.badge.warn` if -1% to -10%, `.badge.danger` if < -10% |
| Customers | `current_customers` (show `customer_change` as +/- delta, e.g., "643 (+30)") |

Show top 10 visible; remaining in collapsed `<details>`.

After the table, render a `<div class="what-this-means">`:

> **What this tells you:** Geography isn't static — it shifts quarter to quarter as reps win or lose momentum. States gaining both revenue and customers are proof of effective coverage; states losing revenue (especially while customer counts hold steady) may signal competitive displacement or shrinking wallet share. Use this as a territory-planning input: where you're growing, double down on coverage; where you're contracting, investigate whether you're losing deals or losing the relationship.

**Claim rules**: Never attribute decline to a specific named competitor or specific cause — say "may indicate competitive pressure," "could signal a coverage gap," or "warrants investigation." Frame growing states as momentum to protect and declining states as requiring attention. Use full state names in headline callouts; abbreviations are acceptable in table cells. Never use internal field names. Never use "ERP."

### 11. Spending Contraction Detection (Q-68)

**Gate**: Render ONLY if `HAS_PORTAL_ORDERS = true` AND `PORTAL_CUSTOMER_DATA_PRESENT = true` AND `cache/Q-68_results.md` has data rows.

**Display**: `[COLLAPSE]` — useful directional insight but historical-peak comparisons are approximate. Collapse keeps the section scannable while making this available for detail-oriented readers.

**Data source**: `cache/Q-68_results.md`

**Methodology (revised)**: Instead of comparing each account to a synthetic peer-group average (which can produce data artifacts when accounts cluster around decile boundaries), compare each account's trailing-12-month spend to their own **historical peak spending period**. This surfaces accounts with a demonstrated spending capacity that have contracted — accounts that HAVE spent more, not accounts that SHOULD spend more based on peers.

**Methodology explanation (MUST include in rendered output)**: Before the table, include a `.prose` paragraph:

> "We compare each account's trailing-12-month spend to their own historical peak — the highest rolling 12-month total in their order history. This surfaces accounts with a demonstrated spending capacity that has contracted. These are accounts that have spent more in the past, making re-engagement a recovery conversation rather than a cold growth pitch."

This explanation must appear every time this subsection renders — it is not optional.

**Rendering**: Open with a `.callout.insight` titled "Spending Contraction: Accounts Below Their Peak" summarizing: "X accounts are spending below their historical peak. The combined gap between current and peak spend represents $Y in demonstrated capacity that has not been recaptured."

Compute `X` as row count. Compute `Y` as sum of `gap_to_peak` across all rows.

Then render the methodology explanation `.prose` paragraph (above).

Then render a table of accounts with highest contraction (sorted by `gap_to_peak` descending):

| Column | Content |
|--------|---------|
| Account | `customer_bill_to_name` |
| State | `primary_state` |
| Current Annual Spend | `customer_spend` formatted as currency |
| Historical Peak Spend | `peak_spend` formatted as currency |
| Contraction | `gap_to_peak` formatted as currency with `.badge.warn` styling |
| Current vs Peak | `current_vs_peak_pct` displayed as percentage (e.g., "38% of peak") |

Show top 8 visible; remaining in collapsed `<details>`.

After the table, render a `<div class="what-this-means">`:

> **What this tells you:** These accounts have a demonstrated spending capacity that exceeds their current level — they've proven they can buy at their peak amount, and something changed. The contraction could reflect competitive displacement, changing business needs, relationship drift, or simply a market cycle. What makes these accounts high-value targets is that the rep conversation isn't "you should spend more" — it's "you used to spend $X, what changed?" That's a fundamentally different and more productive dialogue.

**Claim rules**: Always use "demonstrated capacity," "historical peak," and "contraction" — not "should be spending" or "underperforming." Frame as recovery opportunity, not failure. Never expose internal identifiers. Never use "ERP."

**Query modification note**: Q-68 SQL requires modification to compare customer LTM spend to their own max rolling-12-month total from `portal_orders` history, rather than to a state+spend-decile peer average. See `authority/query_library.md` for the updated query definition.

## Section-Specific Rules

**ERP label prohibition — applies to every HTML slot in this section:**

The VM-12 data source (`customers` table, synced from the client's ERP) contains total account counts including non-eCat accounts. When displaying metric cards or `metric-note` slots in this section:

- **`metric-note` text**: use "total account records" or "your full account base" — NEVER "all-time ERP records"
- **Percentage notes**: use "% of your full account base" or "% of total accounts" — NEVER "% of ERP base"
- **Inline prose**: use "accounts in your system" or "in your account base" — NEVER "ERP accounts"

These are the three most common ERP label leakage points in the Customer section. All three are forbidden in client-facing HTML.

## Data Confidence Footer

**You MUST render this footer.** Follow the numbered steps below exactly. Do NOT skip or reorder them.

**STEP 1 — Read the tier (MANDATORY).** Open `cache/section_confidence.md` and read the EXACT value of `SECTION_CONFIDENCE_3`. It is one of: `FULL`, `STRONG`, `PARTIAL`, `LIMITED`. **Use THIS value. Do NOT infer or recompute the tier from gate flags — the data gathering script already computed it.**

**STEP 2 — Select the template** matching the tier from STEP 1:

| STEP 1 value | Template | Label |
|---|---|---|
| `FULL` | `§3-FULL` | `FULL PICTURE` |
| `STRONG` | `§3-STRONG` | `STRONG VIEW` |
| `PARTIAL` | `§3-PARTIAL` | `PARTIAL VIEW` |
| `LIMITED` | `§3-PARTIAL` (with `.limited` class) | `LIMITED VIEW` |

Resolve template variables: `{{CUSTOMER_COUNT}}` from `gate_flags.md`, `{{LAST_PORTAL_ORDER_DATE}}` from enrichment preflight in `gate_flags.md`. If `{{CUSTOMER_COUNT}}` cannot be resolved, omit the parenthetical. If `{{LAST_PORTAL_ORDER_DATE}}` cannot be resolved for FULL or STRONG, fall back to `§3-PARTIAL`.

**STEP 3 — Position the footer:**
- If STEP 1 value is **FULL** → place the footer as the **last element** in the section fragment, after all subsection content.
- If STEP 1 value is **STRONG / PARTIAL / LIMITED** → place the footer **immediately after the key metrics row**, before the first subsection.

**STEP 4 — Build the HTML:**

```html
<div class="data-confidence">
  <span class="data-confidence-label">{{TIER_LABEL}}</span>
  <span class="data-confidence-action">{{TEMPLATE_TEXT}}</span>
</div>
```

If STEP 1 value is `LIMITED`, use `<div class="data-confidence limited">` instead.

## DOES NOT COVER (hard boundaries)

This section does NOT produce:
1. Rep-level performance, coaching, or behavioral analysis → belongs in §2 Sales Team Performance
2. Order channel mix, eCat capture rate, or commerce trends → belongs in §5 Commerce Analytics
3. Product catalog health, inventory, or sales-line analysis → belongs in §4 Product & Inventory
4. Portal traffic, Clicky analytics, or geographic demand → belongs in §6 Demand Signal Intelligence
5. Peer benchmarking or cohort comparisons → belongs in §7 Peer Benchmarking
6. Platform feature utilization or data freshness → belongs in §8 Platform & Feature
7. Health score, churn risk, or expansion signals → internal only (GUARDRAILS.md §5)

Read: `GUARDRAILS.md` for the full query ownership table (§8) and rule set.

---

## Conditional Subsection Checklist (verify before saving fragment)

Before writing `fragments/section_03.html`, confirm each item. **Treatment** column is authoritative — violating it is a rendering defect.

| # | Subsection | Gate(s) | Treatment | Mandatory? |
|---|-----------|---------|-----------|-----------|
| 1 | Customer Activation (Q-12) | Always | Standalone | Yes — always rendered |
| 2 | eCat Penetration (Q-52) | `PORTAL_CUSTOMER_DATA_PRESENT = true` + data rows | Standalone | Yes when gate met |
| 3 | Dormant High-Value (Q-17) | Always | Standalone | Yes — always rendered |
| 4 | Unactivated High-Value (Q-53) | `PORTAL_CUSTOMER_DATA_PRESENT = true` + data rows | Standalone | Yes when gate met |
| 5 | Geographic Distribution (Q-40/Q-54) | Always (Q-54 enrichment conditional) | `[COLLAPSE]` | Yes — always rendered |
| 6 | Reorder Velocity (Q-14/Q-14b) | Always (Q-14b enrichment conditional) | Standalone | Yes — always rendered |
| 7 | New Buyer Acquisition (Q-41) | Always | `[COLLAPSE]` | Yes — always rendered |
| 8 | Cross-Sell Whitespace (Q-57) | `HAS_PORTAL_ORDERS` + `PORTAL_CUSTOMER_DATA_PRESENT` + data rows | Standalone | Yes when gate met |
| 9 | Buyer-Within-Account (Q-66) | `HAS_PORTAL_ORDERS` + `HAS_BUYER_DATA` + data rows | **Standalone** | Conditional |
| 10 | Geographic Revenue Trends (Q-67) | `HAS_PORTAL_ORDERS` + `PORTAL_CUSTOMER_DATA_PRESENT` + data rows | **Standalone** | Yes when gate met |
| 11 | Spending Contraction Detection (Q-68) | `HAS_PORTAL_ORDERS` + `PORTAL_CUSTOMER_DATA_PRESENT` + data rows | **`[COLLAPSE]`** | Yes when gate met |

### Gate Verification Checklist

- [ ] Q-52 subsection (2): `PORTAL_CUSTOMER_DATA_PRESENT = true` + `Q-52_results.md` has data rows → rendered? (or gate false / 0 rows → correctly skipped?)
- [ ] Q-53 subsection (4): `PORTAL_CUSTOMER_DATA_PRESENT = true` + `Q-53_results.md` has data rows → rendered? (or gate false / 0 rows → correctly skipped?)
- [ ] Q-54 enrichment on Geographic Distribution (5): `PORTAL_CUSTOMER_DATA_PRESENT = true` + `Q-54_results.md` has data rows → enrichment columns added to state table? (or gate false / 0 rows → Q-40-only table rendered?)
- [ ] Q-14b deceleration alert (6b): `HAS_PORTAL_ORDERS = true` + `Q-14b_results.md` has data rows → alert table rendered within subsection 6? (or gate false / 0 rows → Q-14-only subsection rendered?)
- [ ] Q-57 whitespace (8): `HAS_PORTAL_ORDERS = true` + `PORTAL_CUSTOMER_DATA_PRESENT = true` + `Q-57_results.md` has data rows → subsection 8 rendered? (or gates false / 0 rows → correctly skipped?)
- [ ] Q-66 buyer intelligence (9): `HAS_PORTAL_ORDERS = true` + `HAS_BUYER_DATA = true` + `Q-66_results.md` has data rows → subsection 9 rendered as **standalone** (not collapsed)? (or gates false / 0 rows → correctly skipped?)
- [ ] Q-67 geographic trends (10): `HAS_PORTAL_ORDERS = true` + `PORTAL_CUSTOMER_DATA_PRESENT = true` + `Q-67_results.md` has data rows → subsection 10 rendered as **standalone** (not collapsed), placed after Geographic Distribution? (or gates false / 0 rows → correctly skipped?)
- [ ] Q-68 spending contraction (11): `HAS_PORTAL_ORDERS = true` + `PORTAL_CUSTOMER_DATA_PRESENT = true` + `Q-68_results.md` has data rows → subsection 11 rendered inside `[COLLAPSE]`? Methodology explanation paragraph present? (or gates false / 0 rows → correctly skipped?)
- [ ] Every rendered subsection has a `<div class="what-this-means">` close?
- [ ] Confidence footer present and matches `SECTION_CONFIDENCE_3` tier?
- [ ] No forbidden terms (ERP, health score, Mixpanel, Clicky, segment labels, internal IDs)?

## Shared Rules

# Shared Rules — All Section Agents
> **v1.1** — updated 2026-06-16. Scoped forbidden-phrase canonical claim, confidence footer scope.

> **Note:** This file is a runtime guide consumed by section-building agents. The
> canonical rule definitions live in [`GUARDRAILS.md`](../../../GUARDRAILS.md). If
> this file and `GUARDRAILS.md` conflict, `GUARDRAILS.md` wins.

## A. Semantic Guardrails

| Term | Correct Meaning | Never Use For |
|------|----------------|--------------|
| `orders` | eCat-originated orders only | ERP or total-business data |
| `order_source = 'ipad'` | Rep-submitted iPad orders | Online or self-service orders |
| `order_source = 'server'` | eCat Online / B2B Cart buyer self-service | Rep orders |
| `portal_orders` | ERP-synced all-channel total business | Buyer activity, "portal ordering," self-service |
| `Sales Portal` | Internal BI dashboard for client team | A buyer-facing ordering channel |
| `self-service` | B2B Cart / eCat Online only | Sales Portal, portal_orders |
| Segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) | Internal classification only — never in external output | Every section including Peer Benchmarking — in §7, use plain-language cohort framing derived from `peer_group_id_effective` |
| Health score | Never in Phase 1 external report | Any external output |
| `benchmark_confidence` | Internal rendering signal only — governs section inclusion and phrasing | Never as a visible label in client output |
| `peer_group_level` | Internal gating signal only | Never in client output (not even paraphrased as "tier 1/2/3") |
| `peer_group_n` | Internal calibration signal — governs framing strength | Never as a raw count in client-facing output. Use to calibrate plain-language phrasing only. |

## B. Hard Rules

Invariant. No exception, no workaround, no soft reference:

1. Never surface health score, health band, or health classification in any external output
2. Never surface VM-27, VM-28, VM-29, VM-36, VM-48 content externally
3. If `has_clicky = false`, the Demand Signal Intelligence section does not exist. No placeholder. No mention of Clicky anywhere.
4. `portal_orders` is never buyer activity. Never "portal ordering adoption."
5. Segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) are internal classification terms and must never appear anywhere in the external report — including the Peer Benchmarking section. In §7, describe the peer group using plain-language framing derived from `peer_group_id_effective` (e.g., "Lighting manufacturers on the same platform bundle") — not the raw label or segment classification terms.
6. Executive Summary is always written last
7. Every metric must include a time qualifier (e.g., "trailing 12 months," "last 90 days")
8. Every projection must be hedged with appropriate language ("potential," "estimated," "projected," "roughly," "could," "up to") in client-facing HTML. The literal tags `[HYPOTHETICAL]` and `[ESTIMATED]` are **internal pipeline markers only** — they appear in `cache/` highlight files and priority action candidates so validators and the Stage 4 assembler can track projections, but they must **never appear as visible text in HTML fragments**. If the literal string `[HYPOTHETICAL]` or `[ESTIMATED]` appears in a fragment, it is a rendering defect.
9. Every extrapolation must be hedged with appropriate language in client-facing HTML (same rule as #8 — see above).
10. Do not improvise around missing data — mark as N/A or omit per blueprint rules
11. `benchmark_confidence`, `peer_group_level`, and `peer_group_n` are internal signals only. Never expose these as labels in client-facing HTML — not in prose, callouts, section headers, or footnotes. Use them to calibrate plain-language benchmark framing only.

## C. Forbidden Phrases

> **Runtime copy of the canonical list in GUARDRAILS.md §4.** The post-build check in `qa/eval/check_static.sh` mirrors this list. If you add or remove a forbidden phrase, update GUARDRAILS.md first, then this file and the shell script.

Never in client-facing HTML:

- "health score" / "health scores"
- "portal orders" / "portal ordering" as buyer activity or entity label
- "net-new customers"
- "ERP" in any client-facing text — use "total business," "all-channel sales," "your business system," "your account base"
- "Mixpanel" — use "platform engagement data" or "engagement events"
- "Clicky" — never in delivered HTML
- Segment labels: "Platform-Embedded", "Commerce-Active", "Catalog-Focused"
- Internal identifiers: VM codes, query IDs, table names, column names, org IDs, dataset paths
- "bounce_rate"
- `order_source = 'ipad'` and similar code literals in client-facing prose
- "benchmark_confidence", "peer_group_level", "peer_group_n" as labels
- Literal `[HYPOTHETICAL]` or `[ESTIMATED]` tags — these are internal pipeline markers and must never appear in client-facing HTML

## D. Universal Formatting Rules

- Every metric has a time qualifier (Hard Rule #7)
- Projections use hedging language in HTML; `[HYPOTHETICAL]` tags in cache/highlights only — never in fragments (Hard Rule #8)
- Extrapolations use hedging language in HTML; `[ESTIMATED]` tags in cache/highlights only — never in fragments (Hard Rule #9)
- Dollar formatting: `$X,XXX` or `$X.XM`
- Do not improvise around missing data (Hard Rule #10)
- Every subsection ends with a "What this tells you" close (1–3 sentences, actionable implication)
- One `what-this-means` per subsection. Do not add a second section-level `what-this-means` after the last subsection's close.
- Coaching Opportunities & Selling Archetypes (§2.3) is the one exception to the `what-this-means` rule: coaching cards are self-contained action items and do NOT end with a `what-this-means` block.
- Do not surface operational exclusion methodology, showroom scan details, qualifying threshold explanations, or internal pipeline context in client-facing prose. The `section-sub` one-liner may reference an exclusion count (e.g., "1 showroom excluded") but not the methodology.

## E. Fragment Contract

Every section agent produces an HTML fragment in this exact wrapper:

```html
<details class="section-collapse" id="{{SECTION_ID}}">
  <summary>
    <div>
      <h2 class="section-title"><span class="section-num">§{{N}}</span> {{SECTION_TITLE}}</h2>
      <div class="section-sub">{{KEY_STATS_ONE_LINE}}</div>
      <div class="section-contents">{{SUBSECTION_LIST_MIDDOT_SEPARATED}}</div>
    </div>
    <span class="expand-hint">&#9662; Click to expand</span>
  </summary>
  <section class="section" style="margin-bottom:0;border-top:none;border-radius:0 0 var(--r) var(--r);">
    {{SUBSECTION_CONTENT}}
  </section>
</details>
```

**Section IDs (locked):** `§2=sales`, `§3=customers`, `§4=product`, `§5=commerce`, `§6=portal`, `§7=peer`, `§8=platform`

**Fragment rules:**
- Starts with `<details`, ends with `</details>` — nothing before or after
- No `<html>`, `<head>`, `<body>`, or `<style>` tags
- No HTML comments (`<!-- -->`)
- `section-contents`: every rendered subsection name, separated by ` · ` (`&middot;`) — must reflect ONLY subsections that actually appear in the fragment (not skipped subsections)
- `section-sub`: data-dense one-liner, not a generic description
- Every subsection: `<div class="subsection">` with `<div class="subsection-title">` as first child
- Every subsection ends with `<div class="what-this-means">` (exception: §2.3 Coaching Opportunities & Selling Archetypes — coaching cards are self-contained and omit what-this-means per Section D above)
- **Structural self-check before saving**: count of `what-this-means` divs must equal count of `subsection` divs minus any coaching-card subsections. If you have more `what-this-means` than subsections, you have a duplicate — remove it. If fewer, a subsection is missing its close.

## F. CSS Class Quick-Reference

From `authority/html_report_template.html` (aligned with gold reference `clm_2026-04-14`). Use these class names exactly.

| Class | Renders |
|-------|---------|
| `.subsection` | Subsection container (24px top margin) |
| `.subsection-title` | Bold 15px subsection heading |
| `.what-this-means` | Amber left-bordered panel box for actionable close |
| `.metrics-grid` | Auto-fill responsive grid of metric cards |
| `.metric-card` | Panel-bg rounded card for a single metric |
| `.metric-val` | Bold 24px metric number |
| `.metric-label` | Mono 9px uppercase muted label |
| `.metric-note` | 11px muted annotation; variants `.ok` / `.warn` / `.danger` |
| `.callout` + `.callout-title` | Rounded box with left border accent; 600-weight 13px title |
| `.callout.insight` | Panel bg + amber left border |
| `.callout.alert` | Danger-bg + red left border (use instead of `.callout.warning`) |
| `.callout.opportunity` | Ok-bg + green left border (use instead of `.callout.action`) |
| `.badge` | Inline mono 10px uppercase pill |
| `.badge.ok` / `.badge.warn` / `.badge.danger` / `.badge.info` / `.badge.muted` | Status pills (dot notation — space-separated classes) |
| `.coaching-card` | White card with warn-colored 3px top border |
| `.coaching-header` / `.coaching-name` | Flex header row; bold 15px name |
| `.coaching-body` / `.coaching-action` / `.coaching-impact` | 13px body; medium-weight action; mono green impact pill |
| `.prose` | 13.5px secondary-color paragraph with 16px bottom margin |
| `<details>` (inner) | Panel-bg summary with arrow and click-to-expand pattern |
| `.row-highlight` | Table row with green (`--ok-bg`) emphasis |
| `.section-num` | Mono 11px muted section number prefix (e.g., §2) |
| `.peer-hero` | Panel-bg flex container for hero benchmark stat |
| `.peer-hero-pctile` | 13px mono pill badge; `.above` (green) / `.below` (red) / `.on-par` (muted) |
| `.peer-metric-row` | 3-column grid row for benchmark breakdown |
| `.peer-metric-title` | 12px metric name |
| `.peer-range-bar` / `.peer-range-marker` | 6px bar with positioned dot; `.above` / `.below` / `.on-par` |
| `.quartile-pill` / `.peer-quartile-pill` | 9px mono uppercase pill; `.q4` (green) / `.q3` (blue) / `.q2` (amber) / `.q1` (red) |
| `.priorities` / `.priority` | Grid container; 3-column card (badge / title+desc / impact) |
| `.priority-badge` | Mono 9px urgency pill; `.high` (red) / `.medium` (amber) / `.low` (muted) |
| `.priority-title` / `.priority-desc` / `.priority-impact` | Bold 14px title; 13px desc; mono 11px muted impact |
| `.highlights` | Counter-numbered list (amber-circled counters, light bottom borders) |
| `.top-performer-list` | Container for top-performer behavioral pattern rows (§7.4) |
| `.top-performer-row` | Flex row: icon + text, bottom-bordered |
| `.top-performer-icon` | 26px accent-glow rounded icon cell (use Unicode arrows/symbols) |
| `.top-performer-text` | 13px secondary prose with bold strong elements |
| `.data-confidence` | Info-bg panel at bottom of section body, 12px muted text, info left-border |
| `.data-confidence.limited` | Warn-bg variant with warn left-border (staleness/quality issues) |
| `.data-confidence-label` | Mono 9px uppercase badge prefix (tier label) |
| `.data-confidence-action` | 12px medium-weight text for "what would complete this" line |

## G. Highlight Candidate Format

Each section agent outputs `cache/section_NN_highlights.md` alongside its fragment.

```markdown
# §N Section Title — Highlight Candidates

1. **Bold headline** — one sentence of context with data. [→ §section-id]
2. **Bold headline** — one sentence of context with data. [→ §section-id]

## Priority Action Candidate
- **URGENCY**: Action statement with quantified impact [HYPOTHETICAL]. [→ §section-id]
```

**Note:** `[HYPOTHETICAL]` tags in highlight/priority candidates are correct — these are internal cache files consumed by the Stage 4 assembler, not client-facing HTML. The assembler strips or replaces tags with hedging language when building the Executive Summary.

**Rules:**
- 2–4 highlight candidates per section, ranked by signal strength
- Each: **bold headline**, one sentence of context, section link
- 0–1 priority action candidates per section with urgency level
- Stage 4 assembler selects top 5–6 highlights and 2–4 priority actions from all candidates
- Section agents do not write the Executive Summary — they only propose candidates

**Anti-repetition rule:** Executive summary highlights must NOT be repeated verbatim as section-level introductory callouts. A stat may appear in both the executive summary and a section, but the section must present the underlying data table — the `what-this-means` box must add **new interpretation** beyond what the executive summary already stated. If the `what-this-means` text could be copy-pasted into the executive summary without losing meaning, it is restating, not interpreting. The reader already read the table; the `what-this-means` job is to tell them what it MEANS, not what it SAYS.

## H. Display Limits

- Maximum 15 rows displayed per table. Default visible rows: 5. If showing top 10, show 5 visible + remaining 5 in a collapsed `<details>` element. Section-specific display limits in individual section guides take precedence over these defaults.
- Do not dump all cache file rows into tables. The section guide specifies how many to show per subsection.

## I. Progressive Disclosure — Subsection Collapse

- Subsections marked `[COLLAPSE]` in their section guide are wrapped in an inner `<details>` element within the parent section body (inside the outer `<details class="section-collapse">`).
- Collapsed subsections still appear in the `section-contents` middot list.
- When the user opens the parent section, `[COLLAPSE]` subsections remain closed until individually expanded.

## J. Data Confidence Framework

The Data Confidence Framework provides deterministic, per-section disclosure about what data sources are present, their freshness, and what additional data would make the picture more complete. It is formula-driven — no judgment calls, no improvisation.

### J.1 Tier Definitions

| Tier | Condition | Visual Treatment | Footer Rendered? |
|------|-----------|-----------------|-----------------|
| FULL | All primary + enrichment sources present and fresh (≤30 days) | `.data-confidence` footer | Yes — positive-tone data provenance |
| STRONG | Primary sources present; enrichment source stale (31-180d) or one source missing | `.data-confidence` footer | Yes — with source list |
| PARTIAL | Core eCat data only; ERP context unavailable | `.data-confidence` footer + "what would complete this" | Yes — with action |
| LIMITED | Core data stale (>180d) or known quality issues | `.data-confidence.limited` footer with staleness callout | Yes — with warn styling |

### J.2 Rendering Rules

1. **FULL** — render a `.data-confidence` footer with label `FULL PICTURE` and a positive-tone data sources summary listing what went into the analysis. No "To see X, do Y" action prompt — just a clean statement of what's there. **Position: bottom** of the section (after all subsections).
2. **STRONG / PARTIAL** — render a `.data-confidence` footer with a data sources summary AND an action prompt explaining what additional data would complete the picture. **Position: top** of the section (immediately after the key metrics row, before the first subsection). The reader sees upfront that data is incomplete before investing attention in the analysis.

```html
<div class="data-confidence">
  <span class="data-confidence-label">{{TIER_LABEL}}</span>
  <span class="data-confidence-action">{{TEMPLATE_TEXT}}</span>
</div>
```

All four tiers use this structure. `{{TIER_LABEL}}` is one of: `FULL PICTURE` / `STRONG VIEW` / `PARTIAL VIEW` / `LIMITED VIEW`.

3. **LIMITED** — same structure but with the `.limited` modifier:

```html
<div class="data-confidence limited">
  <span class="data-confidence-label">LIMITED VIEW</span>
  <span class="data-confidence-action">{{TEMPLATE_TEXT}}</span>
</div>
```

4. The confidence footer is part of the section fragment. The assembler pastes it verbatim — it does not modify, strip, or relocate it.
5. Never use "ERP" in any confidence footer text — this is client-facing. Use "your business system," "total business," or "all-channel" per Section C.
6. Confidence tier labels (`FULL PICTURE`, etc.) must not appear anywhere else in the report — they are reserved for this footer.

### J.3 Locked Template Strings

Section builders use these exact strings based on their section ID and tier. Do not paraphrase, shorten, or editorialize.

**§2 Sales Team:**
- `§2-FULL`: "Data sources: eCat iPad orders, platform behavioral analytics ({{MIXPANEL_USER_COUNT}} active users), all-channel order data with rep attribution. Complete data for this section."
- `§2-FULL-NO-ERP`: "Data sources: eCat iPad orders, platform behavioral analytics ({{MIXPANEL_USER_COUNT}} active users). Complete eCat data for this section."
- `§2-PARTIAL`: "Data sources: eCat iPad orders. To see behavioral analytics and selling archetypes, ensure reps are using the eCat iPad app. To see how eCat adoption compares to each rep's total business, sync order data with rep attribution via your business system."
- `§2-STRONG`: "Data sources: eCat iPad orders, platform behavioral analytics. To see how eCat adoption compares to each rep's total business, sync order data with rep attribution via your business system."
- `§2-ADMIN-DISCLOSURE`: "Note: This section includes ordering activity from users assigned to internal or administrative roles in your platform configuration. Their activity reflects real orders but may include test or operational transactions."

The `§2-ADMIN-DISCLOSURE` template is an **additive append** — it is rendered as a second line inside the same `.data-confidence` div when `ADMIN_REPS_IN_LEADERBOARD = true`, regardless of tier. At FULL tier, append the disclosure as a `<br>` line inside the FULL PICTURE footer. At STRONG/PARTIAL, append as a `<br>` line inside the existing footer.

Use `§2-FULL` when `PORTAL_REP_DATA_PRESENT = true`. Use `§2-FULL-NO-ERP` when `PORTAL_REP_DATA_PRESENT = false` (eCat + Mixpanel data present, but no all-channel rep attribution).

**§3 Customer:**
- `§3-FULL`: "Data sources: eCat order history, account records ({{CUSTOMER_COUNT}} accounts), all-channel order data (last synced {{LAST_PORTAL_ORDER_DATE}}). Complete data for this section."
- `§3-PARTIAL`: "Data sources: eCat order history, account records. To see customer-level penetration of your total business and identify high-value unactivated accounts, sync order data via your business system."
- `§3-STRONG`: "Data sources: eCat order history, account records, all-channel order data. Order data was last synced {{LAST_PORTAL_ORDER_DATE}} — refresh for current total-business context."

**§4 Product:**
- `§4-FULL`: "Data sources: Product catalog ({{PRODUCT_COUNT}} items), inventory data, sales history. Complete data for this section."
- `§4-PARTIAL`: "Data sources: Product catalog. To see inventory status and sales performance by category, import inventory and sales history data."
- `§4-STRONG`: "Data sources: Product catalog, {{SOURCES_PRESENT}}. {{STALE_SOURCE}} was last updated {{STALE_DATE}} — refresh for current analysis."

**§5 Commerce:**
- `§5-FULL`: "Data sources: eCat orders, all-channel order data (last synced {{LAST_PORTAL_ORDER_DATE}}). Complete data for this section."
- `§5-PARTIAL`: "Data sources: eCat orders by channel and type. To see eCat's share of your total business and per-customer penetration, sync order data via your business system."
- `§5-STRONG`: "Data sources: eCat orders, all-channel order data. Order data was last synced {{LAST_PORTAL_ORDER_DATE}} — refresh for current context."

### J.4 Template Variable Resolution

- `{{LAST_PORTAL_ORDER_DATE}}` — from the ERP enrichment preflight (`most_recent_erp_order`), formatted as "Month DD, YYYY"
- `{{SOURCES_PRESENT}}` — comma-separated list of present sources (e.g., "inventory data, sales history")
- `{{STALE_SOURCE}}` — the specific source that is stale (e.g., "Inventory data", "Sales history")
- `{{STALE_DATE}}` — from Q-08 data_versions, formatted as "Month DD, YYYY"
- `{{MIXPANEL_USER_COUNT}}` — from `gate_flags.md` evidence for `MIXPANEL_USER_DATA_PRESENT` (the row count from Q-01 Step 1). If unavailable, omit the parenthetical from the FULL template and just say "platform behavioral analytics".
- `{{CUSTOMER_COUNT}}` — from `gate_flags.md` evidence for customer base count (Q-10 or equivalent). If unavailable, omit the parenthetical from the FULL template.
- `{{PRODUCT_COUNT}}` — from `gate_flags.md` evidence for product count (Q-08 catalog count). If unavailable, omit the parenthetical from the FULL template.

If a template variable cannot be resolved (source missing), use the PARTIAL template instead — never render a STRONG or FULL template with unresolved variables. For FULL templates, the parenthetical counts (`{{MIXPANEL_USER_COUNT}}`, `{{CUSTOMER_COUNT}}`, `{{PRODUCT_COUNT}}`) are the only exception — those may be gracefully omitted while keeping the FULL template.

### J.4b PARTIAL-Tier "What You'd See" Teaser

When a subsection is gated out due to missing data (e.g., `HAS_PORTAL_ORDERS = false` suppresses capture rate), section builders at PARTIAL or LIMITED tier MAY include a single `.callout.opportunity` teaser at the point where the gated subsection would appear. This makes the data-enrichment value proposition concrete without being salesy.

**Template:**

```html
<div class="callout opportunity">
  <div class="callout-title">What this section would show with connected data</div>
  <p>{{TEASER_TEXT}}</p>
</div>
```

**Per-section teaser text (use verbatim or adapt to context):**

- **§2 (rep capture):** "If total-business order data with rep attribution were connected, this section would show each rep's capture rate — what percentage of their territory's full revenue flows through the platform. Clients with this data typically discover a 5–30× spread across their team."
- **§3 (customer penetration):** "If total-business order data were connected, this section would show which of your highest-value accounts have never placed a platform order — and the combined revenue they represent through other channels."
- **§5 (capture rate):** "If total-business order data were connected, this section would show your platform capture rate — how much of your full revenue flows through the platform. Clients with this data typically discover 70–90% of their business is invisible to their digital ordering tools."

**Rules:**
- Maximum ONE teaser per section (not per gated subsection)
- Only at PARTIAL or LIMITED tier — never at STRONG or FULL
- Never in §6, §7, or §8 (no confidence framework)
- The teaser replaces the gated subsection's slot — do not leave a gap AND show a teaser

### J.5 Section Builder Contract

Each section builder that has a confidence tier (§2, §3, §4, §5):

1. Reads its tier from `cache/section_confidence.md` (e.g., `SECTION_CONFIDENCE_3`)
2. If tier is FULL — selects the matching `§X-FULL` template from J.3, resolves variables, and places the `.data-confidence` div with label `FULL PICTURE` as the **last element** in the section fragment (after all subsections)
3. If tier is STRONG or PARTIAL — selects the matching template from §J.3, resolves variables, and places the `.data-confidence` div **immediately after the key metrics row, before the first subsection**
4. If tier is LIMITED — uses the `.data-confidence.limited` variant with warn styling, positioned at the **top** (same as STRONG/PARTIAL)
5. Every section fragment for §2–§5 MUST contain exactly one `.data-confidence` footer. §6, §7, and §8 do not have confidence tiers and omit the footer

## Cache Data

### Q-12_results.md

# Q-12 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-12 — Customer Activation & ERP Penetration
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
| --- | --- | --- | --- | --- |
| 38,957 | 3,923 | 1,710 | 1,054 | 687 |

### Q-14_results.md

# Q-14 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-14 — Customer Reorder Frequency
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
| --- | --- | --- | --- | --- | --- | --- |
| BAER 2 | BAER' S FURNITURE COMPANY | 105 | $160,324 | 2025-07-31 23:45:25 | 2026-05-29 18:25:23 | 2.90 |
| CLIVE D | CLIVE DANIEL HOME | 52 | $70,827 | 2025-06-17 18:44:02 | 2026-06-03 19:10:18 | 6.90 |
| RS INTL | ROBB & STUCKY INTERNATIONAL | 50 | $94,796 | 2025-07-15 00:18:17 | 2026-06-12 22:32:47 | 6.80 |
| LIBUMC | LIGHTING IN STYLE | 50 | $39,988 | 2025-07-10 23:44:56 | 2026-06-16 16:18:04 | 7 |
| AWELL | A WELL DRESSED HOME | 41 | $50,689 | 2025-06-26 17:38:18 | 2026-06-05 21:34:28 | 8.60 |
| 0003564 | TRIBUS DESIGN STUDIO | 41 | $94,994 | 2025-07-02 13:45:32 | 2026-05-22 17:42:11 | 8.10 |
| VITOCH | VITOCH INTERIORS | 33 | $33,792 | 2025-06-17 03:13:41 | 2026-06-12 14:44:36 | 11.30 |
| NTDTX | NORTH TEXAS DESIGN GROUP | 31 | $50,140 | 2025-06-20 14:29:07 | 2026-06-08 20:14:26 | 11.80 |
| ST LGT | METRO LIGHTING, ST LOUIS | 30 | $35,339 | 2025-07-25 17:35:07 | 2026-06-10 16:48:18 | 11 |
| DEC UNL | THE DECORATORS UNLIMITED | 28 | $33,119 | 2025-06-25 18:35:36 | 2026-04-20 15:25:12 | 11.10 |
| DWS | DESIGN WORKS STUDIO, INC. NC | 28 | $29,292 | 2025-07-02 05:53:19 | 2026-06-09 20:49:29 | 12.70 |
| 0003330 | BUNNY WILLIAMS HOME | 26 | $37,492 | 2025-06-20 14:32:13 | 2026-06-16 18:14:24 | 14.40 |
| LYTE | LYTEWORKS | 25 | $28,724 | 2025-06-17 15:52:08 | 2026-06-09 22:11:02 | 14.90 |
| PULTE | PULTE INTERIORS | 21 | $27,514 | 2025-07-12 00:00:10 | 2026-06-01 21:26:03 | 16.20 |
| KCID | KELLY CARON DESIGNS | 21 | $31,100 | 2025-07-01 16:47:06 | 2026-05-25 16:38:02 | 16.40 |
| VOSSDES | VOSS DESIGNS | 21 | $31,988 | 2025-06-21 00:24:41 | 2026-06-15 19:55:08 | 18 |
| 0015859 | FIRST COAST LIGHTING AND FANS | 20 | $37,499 | 2025-07-01 15:01:05 | 2026-05-19 14:08:04 | 16.90 |
| CHD 3 | CUSTOM HOME DECORATING | 20 | $19,020 | 2025-06-17 19:46:24 | 2026-05-08 12:58:55 | 17.10 |
| 0014980 | NAPLES LIGHTING & FAN DEPOT | 20 | $22,736 | 2025-06-26 19:55:49 | 2026-06-12 00:10:24 | 18.40 |
| MEDER | BLACK SHEEP INTERIORS | 19 | $25,383 | 2025-06-30 15:05:03 | 2026-04-17 19:04:54 | 16.20 |

### Q-17_results.md

# Q-17 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-17 — Dormant eCat Customers — Lapsed
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 25
- **Run date**: 2026-06-16


| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
| --- | --- | --- | --- | --- | --- |
| FURLAND | FURNITURELAND SOUTH | NC | 2026-02-20 01:33:15 | 11 | $111,032 |
| TAL | TALAMORE AT OAK TERRACE | PA | 2026-02-09 18:06:26 | 1 | $46,696 |
| 0021471 | FONDA LANDHOLDINGS AND DESIGN | WI | 2026-01-29 22:44:09 | 2 | $30,910 |
| 0021046 | Palette and Parlor | NC | 2025-09-06 20:09:50 | 1 | $28,897 |
| 0008629 | FLOOR CO LLC | MS | 2025-09-25 00:49:18 | 1 | $28,506 |
| 0011082 | INTERIOR MARKETING GROUP | NY | 2025-08-21 21:15:45 | 2 | $28,038 |
| 0009768 | NATHAN VANAGS DESIGN | FL | 2026-03-11 00:09:34 | 5 | $27,482 |
| CRE & D | CREATIVE INTERIORS AND DESIGN | WA | 2026-02-09 17:13:24 | 1 | $24,340 |
| 0006755 | SAVANNAH COLLEGE OF ART DESIGN | GA | 2025-10-06 17:23:06 | 3 | $22,627 |
| CORKYS | CORKY'S FOOTWEAR INC. | AR | 2025-10-15 15:50:22 | 1 | $20,616 |
| GRAC NC | GRACE DESIGN | NC | 2026-02-12 18:21:51 | 5 | $20,208 |
| JST NC | JST INTERIOR DESIGN | NC | 2025-11-21 20:58:46 | 1 | $19,625 |
| 0019845 | MIRROR LAKE INNN | NY | 2025-08-11 17:00:25 | 2 | $18,855 |
| LGT 1ST | LIGHTING FIRST | FL | 2026-02-20 15:08:42 | 2 | $18,344 |
| WHIRLY | WHIRLYGIG DESIGNS | NC | 2025-08-15 16:59:53 | 3 | $17,833 |
| CFI | CAROLINA FURNITURE & INTERIORS | SC | 2025-06-25 23:13:06 | 1 | $16,944 |
| ELEKTRA | ELEKTRA LIGHTS & FANS, INC. | WI | 2026-02-25 21:52:05 | 2 | $16,682 |
| SCB | SAYBROOK HOME | CT | 2025-08-27 15:47:32 | 1 | $16,576 |
| 0005339 | BRITANY SIMON DESIGN | AZ | 2025-11-06 15:55:20 | 1 | $16,310 |
| 0005879 | REFLECTIONS L & M | NJ | 2025-09-17 13:43:17 | 5 | $16,264 |
| DCI 2 | COLLUM DESIGNS | TX | 2026-03-10 21:42:49 | 9 | $16,215 |
| WILSON3 | WILSON LIGHTING - ST. LOUIS | MO | 2026-01-20 17:53:27 | 11 | $15,462 |
| 0010671 | COTTAGE & LOFT INTERIORS | FL | 2026-03-16 16:48:50 | 2 | $15,102 |
| LIT DIR | LIGHTS DIRECT | MO | 2026-02-18 21:09:42 | 7 | $14,780 |
| 0005509 | CREATIVE TONIC | TX | 2025-11-19 20:59:43 | 4 | $14,754 |

### Q-17_atrisk_results.md

# Q-17-atrisk Results — Currey & Company (cci, org_id=161)
- **Query**: Q-17-atrisk — Dormant eCat Customers — At-Risk
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
| --- | --- | --- | --- | --- | --- |
| FURLAND | FURNITURELAND SOUTH | NC | $111,032 | 2026-02-20 01:33:15 | 116 |
| TAL | TALAMORE AT OAK TERRACE | PA | $46,696 | 2026-02-09 18:06:26 | 127 |
| 0021471 | FONDA LANDHOLDINGS AND DESIGN | WI | $30,910 | 2026-01-29 22:44:09 | 137 |
| 0021046 | Palette and Parlor | NC | $28,897 | 2025-09-06 20:09:50 | 283 |
| 0008629 | FLOOR CO LLC | MS | $28,506 | 2025-09-25 00:49:18 | 264 |
| 0011082 | INTERIOR MARKETING GROUP | NY | $28,038 | 2025-08-21 21:15:45 | 299 |
| 0009768 | NATHAN VANAGS DESIGN | FL | $27,482 | 2026-03-11 00:09:34 | 97 |
| CRE & D | CREATIVE INTERIORS AND DESIGN | WA | $24,340 | 2026-02-09 17:13:24 | 127 |
| 0006755 | SAVANNAH COLLEGE OF ART DESIGN | GA | $22,627 | 2025-10-06 17:23:06 | 253 |
| CORKYS | CORKY'S FOOTWEAR INC. | AR | $20,616 | 2025-10-15 15:50:22 | 244 |
| GRAC NC | GRACE DESIGN | NC | $20,208 | 2026-02-12 18:21:51 | 124 |
| JST NC | JST INTERIOR DESIGN | NC | $19,625 | 2025-11-21 20:58:46 | 207 |
| 0019845 | MIRROR LAKE INNN | NY | $18,855 | 2025-08-11 17:00:25 | 309 |
| LGT 1ST | LIGHTING FIRST | FL | $18,344 | 2026-02-20 15:08:42 | 116 |
| WHIRLY | WHIRLYGIG DESIGNS | NC | $17,833 | 2025-08-15 16:59:53 | 305 |
| CFI | CAROLINA FURNITURE & INTERIORS | SC | $16,944 | 2025-06-25 23:13:06 | 355 |
| ELEKTRA | ELEKTRA LIGHTS & FANS, INC. | WI | $16,682 | 2026-02-25 21:52:05 | 111 |
| SCB | SAYBROOK HOME | CT | $16,576 | 2025-08-27 15:47:32 | 293 |
| 0005339 | BRITANY SIMON DESIGN | AZ | $16,310 | 2025-11-06 15:55:20 | 222 |
| 0005879 | REFLECTIONS L & M | NJ | $16,264 | 2025-09-17 13:43:17 | 272 |

### Q-40_results.md

# Q-40 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-40 — Regional Sales Distribution
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| state | customer_count | ecat_order_count | ecat_gmv |
| --- | --- | --- | --- |
| FL | 220 | 810 | $1.6M |
| NC | 136 | 295 | $763,808 |
| TX | 180 | 369 | $648,598 |
| GA | 128 | 232 | $636,337 |
| SC | 76 | 269 | $536,389 |
| NY | 109 | 268 | $514,018 |
| AL | 79 | 150 | $385,175 |
| NJ | 76 | 177 | $347,808 |
| AZ | 73 | 164 | $333,657 |
| CA | 67 | 159 | $286,097 |
| PA | 43 | 98 | $234,200 |
| IL | 45 | 84 | $208,672 |
| TN | 39 | 67 | $153,383 |
| VA | 45 | 72 | $153,152 |
| MO | 21 | 83 | $143,483 |
| CT | 24 | 56 | $137,032 |
| MS | 25 | 54 | $135,547 |
| MA | 44 | 66 | $113,878 |
| KY | 16 | 45 | $104,464 |
| MD | 32 | 60 | $93,872 |

### Q-41_results.md

# Q-41 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 16
- **Run date**: 2026-06-16


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-03-01 | Rep-Acquired (iPad) | 45 |
| 2025-04-01 | Rep-Acquired (iPad) | 75 |
| 2025-05-01 | Rep-Acquired (iPad) | 77 |
| 2025-06-01 | Rep-Acquired (iPad) | 58 |
| 2025-07-01 | Rep-Acquired (iPad) | 62 |
| 2025-08-01 | Rep-Acquired (iPad) | 84 |
| 2025-09-01 | Rep-Acquired (iPad) | 85 |
| 2025-10-01 | Rep-Acquired (iPad) | 66 |
| 2025-11-01 | Rep-Acquired (iPad) | 76 |
| 2025-12-01 | Rep-Acquired (iPad) | 63 |
| 2026-01-01 | Rep-Acquired (iPad) | 53 |
| 2026-02-01 | Rep-Acquired (iPad) | 81 |
| 2026-03-01 | Rep-Acquired (iPad) | 90 |
| 2026-04-01 | Rep-Acquired (iPad) | 75 |
| 2026-05-01 | Rep-Acquired (iPad) | 64 |
| 2026-06-01 | Rep-Acquired (iPad) | 57 |

### Q-41_rep_results.md

# Q-41-rep Results — Currey & Company (cci, org_id=161)
- **Query**: Q-41-rep — First-Time eCat Orderers — By Rep
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 43
- **Run date**: 2026-06-16


| rep | new_ecat_buyers_acquired |
| --- | --- |
| CC Dallas Showroom | 150 |
| Stacie Baker | 105 |
| Shephalli Jain | 58 |
| Lesley Blair | 54 |
| Stacey Chiavetta | 51 |
| Stewart Haviland | 49 |
| Russ Jones | 48 |
| Joanie Martin | 47 |
| Atlanta Showroom | 46 |
| Rip Nance | 41 |
| Kinshasa Floyd | 39 |
| Jodie Veeder | 36 |
| Betty Robbins | 33 |
| Michael  Mosko | 32 |
| Mindy McEntire | 28 |
| Randy Gould | 28 |
| Margarethe Martin | 28 |
| Carrie Haymore | 27 |
| Rob Nance | 26 |
| Kristy Orison | 20 |
| Sandy Glosson | 20 |
| Nancy Hubbard | 16 |
| Tanner Gould | 15 |
| Brigette Fontenot | 14 |
| Deborah Wilson | 13 |
| Patty Miller | 12 |
| Mary Miller | 8 |
| Tim Shelton | 8 |
| Carey Yount | 7 |
| Highpoint Showroom | 6 |
| Cindy Rogers | 6 |
| Lee Kram | 6 |
| Natalie Murphy | 5 |
| Ornella Avakian | 5 |
| Kristin Ireland | 4 |
| Jess Remillard | 4 |
| Eliza Brantley | 3 |
| Penny Gould | 3 |
| Beth Cousins | 3 |
| Sandy Nakatsu | 3 |
| Alexsis Lopez | 2 |
| Nicole Casanova | 1 |
| Vivi Mira-Culmer | 1 |

### Q-52_results.md

# Q-52 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-52 — Customer-Level eCat Penetration
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 30
- **Run date**: 2026-06-16


| customer_code | customer_name | state | erp_orders | erp_gmv | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WAYFAIR | WAYFAIR | MA | 8,544 | $4.7M | 0 | $0 | 0 |
| BENNING | LUMENS | CA | 1,694 | $1.4M | 0 | $0 | 0 |
| FER ENT | FERGUSON ENTERPRISES | VA | 943 | $1.3M | 2 | $8,577 | 0.70 |
| IMPROV | FERGUSON HOME | CA | 1,243 | $1.1M | 0 | $0 | 0 |
| NY LITE | LIGHTING NEW YORK | PA | 1,369 | $1.0M | 0 | $0 | 0 |
| LAMPS + | LAMPS PLUS | CA | 1,522 | $981,912 | 0 | $0 | 0 |
| CL BOCA | CAPITOL LIGHTING - BOCA RATON | FL | 939 | $958,193 | 0 | $0 | 0 |
| FURLAND | FURNITURELAND SOUTH | NC | 315 | $436,907 | 11 | $111,032 | 25.40 |
| LGTOLGY | LIGHTOLOGY | IL | 377 | $397,989 | 0 | $0 | 0 |
| CAI | CAI DESIGNS | IL | 312 | $377,533 | 3 | $14,479 | 3.80 |
| KAT KUO | KATHY KUO DESIGNS | NY | 569 | $371,331 | 0 | $0 | 0 |
| LIGHTOP | LIGHTOPIA | CA | 408 | $362,411 | 0 | $0 | 0 |
| 0005698 | POTTERY BARN | MS | 466 | $353,653 | 0 | $0 | 0 |
| FOUNDRY | FOUNDRY LIGHTING | NY | 423 | $329,909 | 0 | $0 | 0 |
| 0011923 | LULU AND GEORGIA | CA | 642 | $329,104 | 0 | $0 | 0 |
| RS INTL | ROBB & STUCKY INTERNATIONAL | FL | 80 | $273,429 | 50 | $94,796 | 34.70 |
| BAER 2 | BAER' S FURNITURE COMPANY | FL | 201 | $266,319 | 105 | $160,324 | 60.20 |
| CROMWEL | CROMWELL AUSTRALIA PTY LTD | AU | 45 | $261,188 | 0 | $0 | 0 |
| CLIVE D | CLIVE DANIEL HOME | FL | 83 | $233,993 | 52 | $70,827 | 30.30 |
| THETREA | THE TREASURE CHEST | FL | 1 | $215,418 | 0 | $0 | 0 |
| SAFAVIE | SAFAVIEH HOME & CARPET | NY | 257 | $210,230 | 5 | $14,632 | 7 |
| 0010221 | IVY HOME | VA | 188 | $204,293 | 0 | $0 | 0 |
| 0009681 | DANIEL HOUSE CLUB | OR | 251 | $203,550 | 0 | $0 | 0 |
| GOFRAN | GOODFORM FRANCE AND SON | NY | 218 | $200,141 | 0 | $0 | 0 |
| LGT INC | LIGHTING INC | TX | 61 | $182,462 | 1 | $308 | 0.20 |
| WIL | WILSON LIGHTING OF NAPLES | FL | 80 | $181,716 | 6 | $37,270 | 20.50 |
| HAV 001 | HAVERTY'S FURNITURE COMPANIES | GA | 333 | $176,324 | 0 | $0 | 0 |
| SMITHE | W E SMITHE | IL | 126 | $175,248 | 2 | $3,402 | 1.90 |
| DOM EL | DOMINION ELECTRIC | VA | 89 | $172,621 | 1 | $788 | 0.50 |
| GRAHAMS | GRAHAM'S LIGHTING - FRANKLIN | TN | 56 | $172,326 | 0 | $0 | 0 |

### Q-53_results.md

# Q-53 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-53 — Unactivated High-Value ERP Accounts
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| customer_code | customer_name | state | erp_orders | erp_gmv |
| --- | --- | --- | --- | --- |
| WAYFAIR | WAYFAIR | MA | 8,544 | $4.7M |
| BENNING | LUMENS | CA | 1,694 | $1.4M |
| IMPROV | FERGUSON HOME | CA | 1,243 | $1.1M |
| NY LITE | LIGHTING NEW YORK | PA | 1,369 | $1.0M |
| LAMPS + | LAMPS PLUS | CA | 1,522 | $981,912 |
| CL BOCA | CAPITOL LIGHTING - BOCA RATON | FL | 939 | $958,193 |
| LGTOLGY | LIGHTOLOGY | IL | 377 | $397,989 |
| KAT KUO | KATHY KUO DESIGNS | NY | 569 | $371,331 |
| LIGHTOP | LIGHTOPIA | CA | 408 | $362,411 |
| 0005698 | POTTERY BARN | MS | 466 | $353,653 |
| FOUNDRY | FOUNDRY LIGHTING | NY | 423 | $329,909 |
| 0011923 | LULU AND GEORGIA | CA | 642 | $329,104 |
| CROMWEL | CROMWELL AUSTRALIA PTY LTD | AU | 45 | $261,188 |
| THETREA | THE TREASURE CHEST | FL | 1 | $215,418 |
| 0010221 | IVY HOME | VA | 188 | $204,293 |
| 0009681 | DANIEL HOUSE CLUB | OR | 251 | $203,550 |
| GOFRAN | GOODFORM FRANCE AND SON | NY | 218 | $200,141 |
| HAV 001 | HAVERTY'S FURNITURE COMPANIES | GA | 333 | $176,324 |
| GLOBE | GLOBE LIGHTING | OR | 102 | $171,594 |
| BCI LLC | BYRON CHANDLER INTERIORS, LLC | FL | 2 | $153,833 |

### Q-54_results.md

# Q-54 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-54 — Geographic eCat Penetration
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| state | erp_customers | erp_orders | erp_gmv | ecat_customers | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FL | 818 | 5,171 | $11.3M | 220 | 810 | $1.6M | 14.10 |
| CA | 575 | 8,622 | $8.8M | 67 | 159 | $286,097 | 3.20 |
| GA | 528 | 3,349 | $6.1M | 128 | 232 | $636,337 | 10.50 |
| MA | 251 | 9,269 | $5.8M | 44 | 66 | $113,878 | 2 |
| TX | 782 | 2,821 | $5.5M | 180 | 369 | $648,598 | 11.90 |
| NC | 447 | 2,223 | $5.0M | 136 | 295 | $763,808 | 15.40 |
| NY | 357 | 2,730 | $3.6M | 109 | 268 | $514,018 | 14.30 |
| VA | 226 | 2,060 | $3.4M | 45 | 72 | $153,152 | 4.50 |
| SC | 291 | 1,583 | $3.0M | 76 | 269 | $536,389 | 17.90 |
| PA | 220 | 2,677 | $2.9M | 43 | 98 | $234,200 | 8 |
| IL | 179 | 2,003 | $2.7M | 45 | 84 | $208,672 | 7.70 |
| AL | 216 | 876 | $2.2M | 79 | 150 | $385,175 | 17.40 |
| TN | 282 | 1,070 | $2.2M | 39 | 67 | $153,383 | 7 |
| AZ | 200 | 716 | $1.8M | 73 | 164 | $333,657 | 18.80 |
| NJ | 246 | 983 | $1.8M | 76 | 177 | $347,808 | 19.70 |
| OH | 167 | 814 | $1.5M | 5 | 7 | $20,180 | 1.40 |
| UT | 117 | 896 | $1.3M | 11 | 24 | $39,073 | 2.90 |
| MS | 75 | 1,108 | $1.2M | 25 | 54 | $135,547 | 11.20 |
| LA | 104 | 500 | $1.1M | 12 | 17 | $50,185 | 4.50 |
| CO | 154 | 520 | $1.1M | 21 | 30 | $70,896 | 6.40 |

### Q-14b_results.md

# Q-14b Results — Currey & Company (cci, org_id=161)
- **Query**: Q-14b — Account Velocity Deceleration Detection
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 15
- **Run date**: 2026-06-16


| customer_bill_to_number | customer_bill_to_name | total_intervals | historical_avg_interval | recent_avg_interval | deceleration_ratio | annual_gmv |
| --- | --- | --- | --- | --- | --- | --- |
| LIGHTOP | LIGHTOPIA | 597 | 0.80 | 1.20 | 1.50 | $362,411 |
| 0005698 | POTTERY BARN | 887 | 0.50 | 0.90 | 1.80 | $353,653 |
| GOFRAN | GOODFORM FRANCE AND SON | 278 | 1.70 | 2.70 | 1.59 | $200,141 |
| THE CAR | THE CARROLL COMPANIES | 8 | 40.70 | 77 | 1.89 | $155,686 |
| LAM CO | LAMPS.COM | 406 | 1.20 | 2 | 1.67 | $143,508 |
| AMBERIN | AMBER INTERIORS | 276 | 1.70 | 2.70 | 1.59 | $139,431 |
| 0017963 | LIV DESIGN PARTNERS | 15 | 17.60 | 30.10 | 1.71 | $133,850 |
| UNITED | DIRECTBUY OPERATIONS LLC | 119 | 3.80 | 6.20 | 1.63 | $125,075 |
| DESINTL | DESIGNSOURCE INTERNATIONAL | 44 | 11 | 16.50 | 1.50 | $95,532 |
| CORKYS | CORKY'S FOOTWEAR INC. | 11 | 7.80 | 34.50 | 4.42 | $88,403 |
| BUT ELE | BUTLERS ELECTRIC SUPPLY | 30 | 6.80 | 10.30 | 1.51 | $87,727 |
| 0001338 | FISH OUT OF WATER DESIGNS | 5 | 11.70 | 174.50 | 14.91 | $85,015 |
| 0012008 | LIGHT HOUSE CO | 157 | 3 | 4.60 | 1.53 | $82,701 |
| 0010851 | STEVEN SHELL LIVING | 28 | 14 | 26.70 | 1.91 | $82,450 |
| ANT SAN | ANTHEM | 20 | 17.10 | 41.70 | 2.44 | $80,071 |

### Q-57_results.md

# Q-57 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-57 — Cross-Sell Whitespace by Category
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### Q-66_results.md

# Q-66 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-66 — Buyer-Within-Account Intelligence
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| customer_bill_to_name | new_buyers | existing_buyers | new_buyer_orders | new_buyer_revenue | earliest_new_buyer |
| --- | --- | --- | --- | --- | --- |
| THE TREASURE CHEST | 1 | 0 | 1 | 175,944 | 2026-4-28 |
| ALERIE GARRETT | 1 | 0 | 1 | 112,423.50 | 2026-4-28 |
| ALEM DICKEY DESIGNED INTERIORS | 2 | 1 | 2 | 103,875 | 2026-4-26 |
| LILLIAN JAMES DESIGN GROUP | 2 | 1 | 3 | 93,019.40 | 2026-4-26 |
| J PEACH INTERIORS | 2 | 0 | 2 | 92,834.70 | 2026-4-25 |
| COLEY ELECTRIC & PLUMBING SUPP | 1 | 12 | 1 | 87,606 | 2026-6-13 |
| CROMWELL AUSTRALIA PTY LTD | 1 | 0 | 2 | 87,586.55 | 2026-4-26 |
| THE CARROLL COMPANIES | 1 | 1 | 1 | 86,950 | 2026-4-27 |
| FISH OUT OF WATER DESIGNS | 1 | 0 | 2 | 85,015 | 2026-4-6 |
| BAYSIDE INTERIORS | 1 | 0 | 1 | 75,210 | 2026-4-25 |
| ROOM AT THE BEACH | 2 | 0 | 2 | 70,978 | 2026-4-27 |
| METRY INTERIORS DBA I.C. | 3 | 0 | 3 | 70,464 | 2026-4-26 |
| BAY DESIGN | 2 | 1 | 3 | 66,560 | 2026-5-27 |
| VINEYARD BUILDING | 1 | 12 | 1 | 65,856 | 2026-6-13 |
| DEFINED INTERIORS | 1 | 0 | 1 | 63,048 | 2026-4-26 |
| JOHN RUDOLPH DESIGNS | 1 | 0 | 2 | 58,516 | 2026-5-4 |
| PONTON INTERIORS | 1 | 1 | 1 | 54,315 | 2026-4-26 |
| THREAD DESIGN GROUP | 1 | 0 | 2 | 54,215 | 2026-4-26 |
| FEATHERS CUSTOM FURNITURE, INC | 1 | 2 | 2 | 53,338 | 2026-4-1 |
| ECLECTIC HOME | 3 | 0 | 4 | 48,436 | 2026-4-13 |

### Q-67_results.md

# Q-67 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-67 — Geographic Revenue Displacement
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 25
- **Run date**: 2026-06-16


| state | prior_gmv | current_gmv | gmv_change_pct | current_customers | prior_customers | customer_change | current_orders |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FL | $3.1M | $4.7M | 51.30 | 653 | 613 | 40 | 2,084 |
| GA | $1.6M | $2.5M | 52.60 | 313 | 316 | -3 | 1,480 |
| TX | $1.3M | $1.9M | 49 | 405 | 378 | 27 | 1,312 |
| NC | $1.1M | $1.8M | 73.70 | 347 | 266 | 81 | 942 |
| CA | $1.4M | $1.3M | -4.30 | 318 | 341 | -23 | 1,156 |
| NY | $580,732 | $943,398 | 62.40 | 219 | 187 | 32 | 723 |
| SC | $784,455 | $940,812 | 19.90 | 231 | 224 | 7 | 614 |
| TN | $469,253 | $794,703 | 69.40 | 195 | 150 | 45 | 486 |
| VA | $361,340 | $740,047 | 104.80 | 172 | 115 | 57 | 418 |
| AL | $580,916 | $670,345 | 15.40 | 149 | 136 | 13 | 332 |
| NJ | $409,506 | $640,486 | 56.40 | 159 | 138 | 21 | 465 |
| AZ | $512,207 | $617,981 | 20.70 | 113 | 135 | -22 | 317 |
| IL | $345,618 | $557,267 | 61.20 | 137 | 108 | 29 | 446 |
| PA | $352,462 | $510,682 | 44.90 | 143 | 137 | 6 | 379 |
| MA | $386,758 | $463,097 | 19.70 | 185 | 160 | 25 | 464 |
| OH | $320,707 | $438,275 | 36.70 | 132 | 104 | 28 | 299 |
| CO | $261,848 | $419,314 | 60.10 | 106 | 105 | 1 | 275 |
| MI | $254,301 | $344,229 | 35.40 | 86 | 77 | 9 | 250 |
| LA | $219,070 | $336,339 | 53.50 | 83 | 68 | 15 | 200 |
| IN | $186,722 | $309,703 | 65.90 | 65 | 62 | 3 | 161 |
| MD | $164,689 | $296,106 | 79.80 | 114 | 78 | 36 | 239 |
| KY | $182,516 | $284,838 | 56.10 | 64 | 49 | 15 | 130 |
| CT | $207,921 | $255,836 | 23 | 99 | 96 | 3 | 225 |
| UT | $393,616 | $255,658 | -35 | 84 | 79 | 5 | 184 |
| ON | $231,657 | $231,337 | -0.10 | 56 | 49 | 7 | 126 |

### Q-68_results.md

# Q-68 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-68 — Spending Contraction Detection
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| customer_bill_to_name | primary_state | customer_spend | peak_spend | gap_to_peak | current_vs_peak_pct | active_months |
| --- | --- | --- | --- | --- | --- | --- |
| HG BUYING CORP | TX | $58,282 | $260,270 | $201,988 | 22.40 | 2 |
| DESIGNSOURCE INTERNATIONAL | Unknown | $137,465 | $312,994 | $175,529 | 43.90 | 10 |
| WALT DISNEY WORLD COMPANY | FL | $1,785 | $168,232 | $166,447 | 1.10 | 3 |
| HOLIDAY BEACH DECOR | PA | $14,827 | $132,412 | $117,585 | 11.20 | 5 |
| THE SHOWROOM AT FURNITURE ROW | CO | $16,008 | $131,337 | $115,329 | 12.20 | 3 |
| AMANDA OWENS DESIGN INC | GA | $7,518 | $114,044 | $106,526 | 6.60 | 4 |
| HOM FURNITURE, INC. | MN | $50,590 | $151,849 | $101,259 | 33.30 | 12 |
| SOURCE | NV | $19,542 | $118,583 | $99,041 | 16.50 | 7 |
| ROOM AT THE BEACH | CA | $96,580 | $192,027 | $95,447 | 50.30 | 10 |
| HAVERTY'S FURNITURE COMPANIES | VA | $190,898 | $279,944 | $89,046 | 68.20 | 13 |
| THE BRASS BED | AL | $26,668 | $115,297 | $88,629 | 23.10 | 2 |
| KRISTA WATTERWORTH DSGN STUDIO | FL | $37,491 | $125,876 | $88,384 | 29.80 | 9 |
| GREEN GATES MARKET | AL | $9,291 | $92,519 | $83,228 | 10 | 3 |
| CONSTRUCTION RESOURCES COMPANY | GA | $26,791 | $110,003 | $83,213 | 24.40 | 9 |
| JOSHUA G YOUNGNER INTERIORS | GA | $9,285 | $90,640 | $81,355 | 10.20 | 2 |
| A PROPER GARDEN | OH | $10,189 | $88,180 | $77,991 | 11.60 | 2 |
| TABLE AND CHAIR SHOP | FL | $17,552 | $95,219 | $77,667 | 18.40 | 7 |
| FERWERDA INTERIOR DESIGN | FL | $1,872 | $77,509 | $75,637 | 2.40 | 3 |
| CUVEE DESIGN & DEVELOPMENT | CO | $1,424 | $76,538 | $75,114 | 1.90 | 1 |
| LIFESTYLES STORES, INC. | OK | $28,687 | $102,468 | $73,781 | 28 | 11 |
