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
