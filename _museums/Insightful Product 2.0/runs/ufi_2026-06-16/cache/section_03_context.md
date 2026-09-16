# Section 3 Context Bundle — Universal Furniture (ufi)
Run date: 2026-06-16

## Gate Flags

# Gate Flags — Universal Furniture (ufi, org_id=18)
- **Run date**: 2026-06-16
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=60988, portal_order_gmv=$137.9M |
| HAS_INVENTORY | True | inventory_count=2148 |
| HAS_SALES_DATA | True | sales_data_count=104838 |
| HAS_SALES_SECTION | True | qualifying_reps=17 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | ufi_eol |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$137.9M > ecat_gmv=$13.4M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 17 | 17 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 103 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 2131, Mixpanel total submit_order (Q-01): 3593 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=82.5%, ambiguous_rate=15.3%, showroom_event_share=14.7% |
| USER_GROUP_JOIN_RATE | 83% | 85 of 103 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 15% | showroom+admin share of matched events: 14.7% |
| ADMIN_REPS_IN_LEADERBOARD | False | 0 admin/showroom users in leaderboard |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=4382 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | True | commitment_reports_count=4255 |
| HAS_NEW_ITEMS | False | new_item_count=0 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Universal Furniture
- **Shortname**: ufi
- **Org ID**: 18
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Universal Furniture (ufi, org_id=18)
- **Run date**: 2026-06-16

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | False |
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
| §2 Sales Team | STRONG | See Derived Gate 6 §2 formula |
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
- `cache/Q-68_results.md` — Wallet share estimation (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND `PORTAL_CUSTOMER_DATA_PRESENT = true` AND this file contains data rows, subsection 11 MUST be rendered)
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
| `Q-68_results.md` | `HAS_PORTAL_ORDERS = true` + `PORTAL_CUSTOMER_DATA_PRESENT = true` | **MUST render** | 11 (Wallet Share) |

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

# Q-12 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-12 — Customer Activation & ERP Penetration
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
| --- | --- | --- | --- | --- |
| 14,651 | 2,890 | 556 | 388 | 277 |

### Q-14_results.md

# Q-14 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-14 — Customer Reorder Frequency
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
| --- | --- | --- | --- | --- | --- | --- |
| 46845 | SUZANNE WINSTON AND ASSOCIATES L L C | 46 | $90,250 | 2025-06-24 13:50:23 | 2026-06-05 14:57:57 | 7.70 |
| 1509 | RYAN YOUNG INTERIORS | 42 | $112,455 | 2025-07-01 14:55:57 | 2026-06-08 19:22:39 | 8.30 |
| 23269 | ENCORE RESALES INC | 39 | $261,420 | 2025-06-20 18:45:40 | 2026-05-29 12:21:27 | 9 |
| 6759 | WICHITA FURNITURE INC | 34 | $429,630 | 2025-08-14 19:01:45 | 2026-06-13 17:09:26 | 9.20 |
| 1377 | SUGAR BEACH INTERIORS INC | 29 | $72,040 | 2025-08-25 16:08:05 | 2026-05-01 14:47:43 | 8.90 |
| 1498 | SACKSTEDERS INTERIORS | 29 | $50,665 | 2025-06-26 18:43:36 | 2026-06-08 15:19:42 | 12.40 |
| 1534 | ROGERS FURNITURE INC | 27 | $65,020 | 2025-06-26 13:08:37 | 2026-06-05 12:16:18 | 13.20 |
| 50764 | COOPER AND CO HOME AND GIFT | 27 | $45,690 | 2025-06-23 15:01:50 | 2026-06-02 18:27:52 | 13.20 |
| 13606 | ALABAMA FURNITURE MARKET | 26 | $114,375 | 2025-06-26 13:10:53 | 2026-06-02 12:39:50 | 13.60 |
| 1770 | MISKELLYS FURNITURE WAREHOUSE INC | 25 | $429,495 | 2025-06-26 13:06:25 | 2026-05-27 19:37:35 | 14 |
| 2687 | CREATIVE DESIGN CONSULTANTS | 25 | $97,275 | 2025-06-19 14:25:10 | 2026-05-14 15:19:28 | 13.70 |
| 1131 | WOODLAND WAREHOUSE RETAIL FURNITURE INC | 24 | $81,680 | 2025-06-24 12:58:51 | 2026-06-10 15:26:45 | 15.30 |
| 15688 | TOUCH OF BRASS | 20 | $195,555 | 2025-09-02 17:37:52 | 2026-04-27 20:17:30 | 12.50 |
| 36893 | CREATIVE DISPLAYS AND DESIGNS INC | 17 | $167,690 | 2025-08-04 18:23:36 | 2026-05-20 15:07:12 | 18.10 |
| 88507 | WORLD MASTERCRAFTSMEN INC | 17 | $29,535 | 2025-06-26 12:35:00 | 2026-06-11 13:14:55 | 21.90 |
| 37230 | LINCO INVESTMENTS LLC | 16 | $26,405 | 2025-09-04 15:26:35 | 2026-06-15 16:32:23 | 18.90 |
| 33263 | CONSOLIDATED ENTERPRISES EAST | 15 | $48,035 | 2025-08-07 20:47:21 | 2026-05-30 15:19:25 | 21.10 |
| 38123 | JOSTEVE INC | 15 | $72,380 | 2025-07-07 15:07:15 | 2026-05-13 15:50:15 | 22.10 |
| 90521 | AT HOME COMFORT INC | 14 | $38,905 | 2025-11-12 23:48:19 | 2026-06-10 18:06:39 | 16.10 |
| 35755 | THE NEST EGG LLC | 13 | $53,705 | 2025-07-01 18:18:46 | 2026-04-06 15:22:09 | 23.20 |

### Q-17_results.md

# Q-17 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-17 — Dormant eCat Customers — Lapsed
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 25
- **Run date**: 2026-06-16


| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
| --- | --- | --- | --- | --- | --- |
| 44863 | COMPASS INTERIORS LLC | MI | 2025-11-13 17:09:34 | 7 | $164,325 |
| 28433 | ISRAELS DISTRIBUTORS LLC | MI | 2026-01-09 18:04:16 | 6 | $70,105 |
| 7318 | MCLAUGHLINS HOME FURNISHING DESIGNS | MI | 2026-02-26 20:21:59 | 5 | $62,899 |
| 7093 | BAILEY AND SHAMOUN INTERIORS | MI | 2025-10-02 21:50:23 | 4 | $61,160 |
| 3167 | R TORRES SA DE CV | N/A | 2026-01-20 03:04:43 | 1 | $55,205 |
| 90214 | JIM STAFF CARPET INC | IL | 2026-02-10 20:38:13 | 8 | $54,590 |
| 49197 | MERIDITH BAER HOME | CA | 2026-01-05 15:40:11 | 5 | $47,431 |
| 49974 | STAGGS CARPETS AND INTERIORS INC | MS | 2026-01-28 12:48:10 | 4 | $46,170 |
| 6363 | POWELLS FURNITURE INC | VA | 2025-11-14 17:39:39 | 6 | $40,535 |
| 30706 | JAMES A REID FURNITURE | MI | 2026-01-21 05:11:18 | 5 | $34,535 |
| 1690 | NORWOOD FURNITURE SALES INC | AZ | 2025-12-02 21:58:26 | 1 | $33,665 |
| 19171 | NORTHWESTERN HOME | MI | 2025-10-26 21:47:09 | 6 | $32,790 |
| 49641 | DAASTANN | MA | 2025-10-30 02:52:04 | 1 | $31,125 |
| 35697 | RANDOM HARVEST INC | DC | 2026-03-11 22:13:04 | 9 | $30,985 |
| 46105 | HOWSE RETAIL L L C | AR | 2026-02-20 14:39:46 | 1 | $29,980 |
| 48295 | DIAMOND BIZ INC | NC | 2026-01-14 15:48:16 | 2 | $29,860 |
| 19353 | RISING SUN PARTNERS LLC | PA | 2026-01-27 20:22:56 | 2 | $28,220 |
| 44413 | ORIENTAL ACCENTS L L C | AL | 2026-01-27 18:39:36 | 9 | $28,055 |
| 5558 | J & J FURNITURE | MD | 2026-02-20 23:20:45 | 5 | $26,900 |
| 36742 | CLAY PLATTE VENTURE GROUP LLC | MO | 2025-10-25 16:48:42 | 2 | $26,770 |
| 2088 | INTERIORS INC | PA | 2025-12-08 20:36:17 | 1 | $26,400 |
| 91012 | ALLURE DESIGN AND PUBLISHING INC | IA | 2025-11-20 20:06:47 | 1 | $25,690 |
| 2801 | CAROLINA FURNITURE MART INC | NC | 2026-02-20 15:32:13 | 3 | $25,240 |
| 89227 | GREIGE HOME LLC | LA | 2025-11-21 13:12:31 | 2 | $24,395 |
| 6409 | ASHLEY FURNITURE CO | SC | 2026-01-21 16:34:01 | 3 | $21,405 |

### Q-17_atrisk_results.md

# Q-17-atrisk Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-17-atrisk — Dormant eCat Customers — At-Risk
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
| --- | --- | --- | --- | --- | --- |
| 44863 | COMPASS INTERIORS LLC | MI | $164,325 | 2025-11-13 17:09:34 | 214 |
| 28433 | ISRAELS DISTRIBUTORS LLC | MI | $70,105 | 2026-01-09 18:04:16 | 157 |
| 7318 | MCLAUGHLINS HOME FURNISHING DESIGNS | MI | $62,899 | 2026-02-26 20:21:59 | 109 |
| 7093 | BAILEY AND SHAMOUN INTERIORS | MI | $61,160 | 2025-10-02 21:50:23 | 256 |
| 3167 | R TORRES SA DE CV | N/A | $55,205 | 2026-01-20 03:04:43 | 147 |
| 90214 | JIM STAFF CARPET INC | IL | $54,590 | 2026-02-10 20:38:13 | 125 |
| 49197 | MERIDITH BAER HOME | CA | $47,431 | 2026-01-05 15:40:11 | 161 |
| 49974 | STAGGS CARPETS AND INTERIORS INC | MS | $46,170 | 2026-01-28 12:48:10 | 138 |
| 6363 | POWELLS FURNITURE INC | VA | $40,535 | 2025-11-14 17:39:39 | 213 |
| 30706 | JAMES A REID FURNITURE | MI | $34,535 | 2026-01-21 05:11:18 | 145 |
| 1690 | NORWOOD FURNITURE SALES INC | AZ | $33,665 | 2025-12-02 21:58:26 | 195 |
| 19171 | NORTHWESTERN HOME | MI | $32,790 | 2025-10-26 21:47:09 | 232 |
| 49641 | DAASTANN | MA | $31,125 | 2025-10-30 02:52:04 | 229 |
| 35697 | RANDOM HARVEST INC | DC | $30,985 | 2026-03-11 22:13:04 | 96 |
| 46105 | HOWSE RETAIL L L C | AR | $29,980 | 2026-02-20 14:39:46 | 115 |
| 48295 | DIAMOND BIZ INC | NC | $29,860 | 2026-01-14 15:48:16 | 152 |
| 19353 | RISING SUN PARTNERS LLC | PA | $28,220 | 2026-01-27 20:22:56 | 139 |
| 44413 | ORIENTAL ACCENTS L L C | AL | $28,055 | 2026-01-27 18:39:36 | 139 |
| 5558 | J & J FURNITURE | MD | $26,900 | 2026-02-20 23:20:45 | 115 |
| 36742 | CLAY PLATTE VENTURE GROUP LLC | MO | $26,770 | 2025-10-25 16:48:42 | 233 |

### Q-40_results.md

# Q-40 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-40 — Regional Sales Distribution
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| state | customer_count | ecat_order_count | ecat_gmv |
| --- | --- | --- | --- |
| SC | 37 | 163 | $2.0M |
| AL | 50 | 309 | $1.5M |
| CA | 115 | 363 | $1.1M |
| MS | 23 | 157 | $915,617 |
| NJ | 13 | 64 | $497,625 |
| MI | 16 | 47 | $491,630 |
| FL | 29 | 146 | $475,939 |
| KS | 8 | 45 | $466,764 |
| NC | 15 | 31 | $403,987 |
| DE | 10 | 37 | $385,168 |
| KY | 17 | 58 | $359,559 |
| N/A | 23 | 58 | $297,685 |
| CO | 14 | 26 | $254,956 |
| VA | 9 | 51 | $216,417 |
| IN | 15 | 74 | $213,515 |
| PA | 19 | 35 | $205,225 |
| MO | 15 | 30 | $173,686 |
| OH | 12 | 37 | $169,518 |
| MD | 12 | 37 | $168,947 |
| AZ | 7 | 18 | $165,263 |

### Q-41_results.md

# Q-41 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 16
- **Run date**: 2026-06-16


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-03-01 | Rep-Acquired (iPad) | 9 |
| 2025-04-01 | Rep-Acquired (iPad) | 7 |
| 2025-05-01 | Rep-Acquired (iPad) | 10 |
| 2025-06-01 | Rep-Acquired (iPad) | 15 |
| 2025-07-01 | Rep-Acquired (iPad) | 10 |
| 2025-08-01 | Rep-Acquired (iPad) | 13 |
| 2025-09-01 | Rep-Acquired (iPad) | 11 |
| 2025-10-01 | Rep-Acquired (iPad) | 24 |
| 2025-11-01 | Rep-Acquired (iPad) | 16 |
| 2025-12-01 | Rep-Acquired (iPad) | 12 |
| 2026-01-01 | Rep-Acquired (iPad) | 14 |
| 2026-02-01 | Rep-Acquired (iPad) | 10 |
| 2026-03-01 | Rep-Acquired (iPad) | 10 |
| 2026-04-01 | Rep-Acquired (iPad) | 20 |
| 2026-05-01 | Rep-Acquired (iPad) | 10 |
| 2026-06-01 | Rep-Acquired (iPad) | 6 |

### Q-41_rep_results.md

# Q-41-rep Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-41-rep — First-Time eCat Orderers — By Rep
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 25
- **Run date**: 2026-06-16


| rep | new_ecat_buyers_acquired |
| --- | --- |
| Terri Lucas | 34 |
| David Kirsch | 22 |
| Mark Dimitshteyn | 21 |
| John Nord | 19 |
| Neil Phillips | 17 |
| Brad Bowman | 14 |
| David Hadad | 14 |
| Jacki Huelsenbeck | 9 |
| Julie Grothman | 7 |
| Jason Vanderhorst | 6 |
| Sally Simerson | 5 |
| Gregg Lesser | 4 |
| Grant Ford | 4 |
| Jerilyn DeRaad | 3 |
| Jackson Keziah | 3 |
| Gary Geraci | 2 |
| Paul Comer | 2 |
| Alan Erickson | 2 |
| Frank LaDonna | 2 |
| Kaitlin Britz | 2 |
| Dov Kessler | 1 |
| Krista Helton | 1 |
| Mason OConnor | 1 |
| Pierce Erickson | 1 |
| Joe Cryan | 1 |

### Q-52_results.md

# Q-52 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-52 — Customer-Level eCat Penetration
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### Q-53_results.md

# Q-53 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-53 — Unactivated High-Value ERP Accounts
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### Q-54_results.md

# Q-54 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-54 — Geographic eCat Penetration
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### Q-14b_results.md

# Q-14b Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-14b — Account Velocity Deceleration Detection
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 15
- **Run date**: 2026-06-16


| customer_bill_to_number | customer_bill_to_name | total_intervals | historical_avg_interval | recent_avg_interval | deceleration_ratio | annual_gmv |
| --- | --- | --- | --- | --- | --- | --- |
| 43501 | KATHY KUO DESIGNS LLC | 1,468 | 0.30 | 0.50 | 1.67 | $866,709 |
| 33384 | INTERNATIONAL DESIGN SOURCE UNLTD INC | 295 | 1.60 | 2.40 | 1.50 | $348,439 |
| 42820 | FROOOGAL L L C | 474 | 1 | 1.70 | 1.70 | $293,719 |
| 2019 | JORDANS FURNITURE INC | 48 | 8.90 | 18.80 | 2.11 | $281,534 |
| 27506 | MARATHON FURNISHINGS INC | 141 | 3.40 | 5.10 | 1.50 | $278,120 |
| 23269 | ENCORE RESALES INC | 155 | 3 | 5.10 | 1.70 | $271,836 |
| 2922 | BIRMINGHAM WHOLESALE FURNITURE | 143 | 3.20 | 4.90 | 1.53 | $269,265 |
| 32052 | OKL HOLDINGS INC | 572 | 0.80 | 1.30 | 1.63 | $268,550 |
| 46845 | SUZANNE WINSTON AND ASSOCIATES L L C | 239 | 2 | 3.20 | 1.60 | $227,405 |
| 2726 | COCHRAN FURNITURE CO | 121 | 3.70 | 6.80 | 1.84 | $204,372 |
| 46505 | REGINA ANDREW DESIGN INC | 335 | 1.40 | 2.40 | 1.71 | $200,278 |
| 40066 | CART.COM HOLDINGS 2 LLC | 595 | 0.50 | 6.60 | 13.20 | $199,009 |
| 35652 | LIDDON FURNITURE CO INC | 92 | 5.10 | 7.90 | 1.55 | $184,377 |
| 42586 | HENRY HOME INTERIORS LLC | 90 | 5 | 8.90 | 1.78 | $164,253 |
| 36893 | CREATIVE DISPLAYS AND DESIGNS INC | 78 | 5.90 | 9.20 | 1.56 | $156,269 |

### Q-57_results.md

# Q-57 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-57 — Cross-Sell Whitespace by Category
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### Q-66_results.md

(not present — file does not exist or is empty)

### Q-67_results.md

# Q-67 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-67 — Geographic Revenue Displacement
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| state | prior_gmv | current_gmv | gmv_change_pct | current_customers | prior_customers | customer_change | current_orders |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Unknown | $33.0M | $36.5M | 10.70 | 2,455 | 2,310 | 145 | 15,591 |

### Q-68_results.md

# Q-68 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-68 — Wallet Share Estimation
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| customer_bill_to_name | primary_state | customer_spend | peer_avg_spend | wallet_share_pct | gap_to_peer_avg | order_count | active_months | spend_tier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DCOR | Unknown | 27,607.40 | 137,823.67 | 20 | 110,216.27 | 17 | 9 | 5 |
| OUTSIDE INTERIORS LLC | Unknown | 27,617.50 | 137,823.67 | 20 | 110,206.17 | 14 | 8 | 5 |
| PIERCE & PARKER INC | Unknown | 27,642.50 | 137,823.67 | 20.10 | 110,181.17 | 18 | 9 | 5 |
| DESIGN TRADE RESOURCES LLC | Unknown | 27,681.25 | 137,823.67 | 20.10 | 110,142.42 | 18 | 10 | 5 |
| JDUCE DESIGN LLC | Unknown | 27,721.87 | 137,823.67 | 20.10 | 110,101.80 | 2 | 1 | 5 |
| VANESSA BRENNAN INTERIORS LLC | Unknown | 27,799.75 | 137,823.67 | 20.20 | 110,023.92 | 6 | 3 | 5 |
| REMODELING REIMAGINED LLC | Unknown | 27,805.25 | 137,823.67 | 20.20 | 110,018.42 | 5 | 5 | 5 |
| GAYLE SHELBY INTERIORS | Unknown | 27,814.15 | 137,823.67 | 20.20 | 110,009.52 | 4 | 4 | 5 |
| WEEKENDER HOUSE LLC | Unknown | 27,876.25 | 137,823.67 | 20.20 | 109,947.42 | 25 | 10 | 5 |
| GATLIN INTERIORS | Unknown | 27,920 | 137,823.67 | 20.30 | 109,903.67 | 9 | 7 | 5 |
| LISA MAYO INTERIORS | Unknown | 28,081.75 | 137,823.67 | 20.40 | 109,741.92 | 30 | 10 | 5 |
| FURNITURE DISCOUNTERS | Unknown | 28,085 | 137,823.67 | 20.40 | 109,738.67 | 14 | 9 | 5 |
| EASTERN ACCENTS | Unknown | 28,133.60 | 137,823.67 | 20.40 | 109,690.07 | 4 | 2 | 5 |
| JOY OF LIVING | Unknown | 28,173.75 | 137,823.67 | 20.40 | 109,649.92 | 17 | 9 | 5 |
| PALMETTO FURNITURE & MANUFACTURING | Unknown | 28,307.50 | 137,823.67 | 20.50 | 109,516.17 | 14 | 9 | 5 |
| MULLINAX INVESTMENTS | Unknown | 28,326.25 | 137,823.67 | 20.60 | 109,497.42 | 12 | 7 | 5 |
| TRACY PEARCE INTERIOR DESIGN LLC | Unknown | 28,373.50 | 137,823.67 | 20.60 | 109,450.17 | 11 | 8 | 5 |
| WATTS FURNITURE INC | Unknown | 28,416.50 | 137,823.67 | 20.60 | 109,407.17 | 18 | 10 | 5 |
| COMERCIALIZADORA WATTO | Unknown | 28,445 | 137,823.67 | 20.60 | 109,378.67 | 3 | 2 | 5 |
| SCHMITT FURNITURE | Unknown | 28,469.20 | 137,823.67 | 20.70 | 109,354.47 | 12 | 8 | 5 |
