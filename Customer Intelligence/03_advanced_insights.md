# Customer Intelligence — Advanced Insights Layer

> **Status**: Initial thinking — these go beyond descriptive data summaries into predictive/prescriptive intelligence
> **Date**: 2026-06-15
> **Principle**: A data summary is worth $X. An intelligence system that tells you what to do in the meeting and quantifies what happens if you don't is worth multiples of $X.

---

## 1. Next Best Product (Purchase Sequence Prediction)

**What it does**: Identifies products this customer is statistically likely to buy next, based on the purchase sequences of all other customers in the org.

**How it works**: From `portal_order_items` across ALL customers, compute common purchase sequences. For each of this customer's top items, find the most common next-purchased items across all other customers within a 60-day window. Filter out items this customer already buys.

**Example output**:
> "82% of customers who purchased the Meridian Sectional also purchased the Meridian Ottoman within 60 days. This customer bought the Sectional 34 days ago and hasn't ordered the Ottoman."

**Why it's valuable**: This is the Amazon "customers who bought X also bought Y" engine applied to B2B furniture wholesale. Nobody in this industry has it.

**Data source**: `portal_order_items` + `portal_orders.order_date`, grouped cross-customer

---

## 2. Wallet Share Estimation

**What it does**: Estimates what percentage of this customer's total furniture/lighting budget goes to your client, and quantifies the addressable whitespace.

**How it works**: Compare this customer's total business (`portal_orders` GMV) against the average/median of customers in the same region and size tier. The gap is estimated wallet share opportunity.

**Example output**:
> "Magnolia spends $284K/year with you. Similar retailers in the Southeast averaging $412K. Estimated wallet share: 69%. Estimated addressable whitespace: $128K."

**Why it's valuable**: No manufacturer currently has a data-backed answer to "how much of their furniture budget am I getting?" They guess.

**Data source**: `portal_orders` (this customer) vs. `portal_orders` (cohort of similar customers by `billing_state` region + spend decile)

---

## 3. Reorder Decay Detection (Per-SKU Early Warning)

**What it does**: Detects when a specific product's reorder frequency at a specific customer is decaying — before the orders stop entirely.

**How it works**: For each product × customer pair with 3+ orders, compute the moving average of inter-order intervals from `portal_orders.order_date` + `portal_order_items`. When the latest interval exceeds 1.5x the historical average, flag it.

**Example output**:
> "SKU 0728-004 (Monroe Chair): Historical reorder interval 28 days. Last 3 intervals: 32, 41, 58 days. Decay detected. This product may be losing floor performance at this account."

**Why it's valuable**: Product-level disengagement is invisible until orders just stop. This catches it 2–3 reorder cycles before the product goes dark.

**Data source**: `portal_order_items` + `portal_orders.order_date`, per customer × item

---

## 4. Buyer-Within-Customer Intelligence

**What it does**: Identifies individual buyers placing orders for this customer, tracks their activity, and detects new decision-makers.

**How it works**: `portal_orders.buyer_name` grouped by customer. Track each buyer's order volume, category focus, and first/last activity dates.

**Example output**:
> "3 buyers place orders for Magnolia:
> - Jennifer Walsh — 68% of volume, all categories, primary relationship
> - David Chen — 24%, Lighting only, started Feb 2026 (NEW BUYER)
> - Magnolia Admin — 8%, reorders only, likely automated
>
> Alert: David Chen is a new decision-maker. New buyers who start in one category expand to 2.3 categories within 6 months on average."

**Why it's valuable**: A new name in the order stream means someone new got purchasing authority. That's either an opportunity (new champion) or a risk (predecessor left, relationship reset).

**Data source**: `portal_orders.buyer_name` grouped by `customer_bill_to_number`

---

## 5. Price Trajectory & Margin Erosion

**What it does**: Tracks whether this customer is trading down — buying cheaper items, using more discounts, shifting to promo pricing.

**How it works**: `portal_invoice_items.unit_price` averaged by quarter. `orders.discount_percent` trended over time. Separate promo from non-promo line items.

**Example output**:
> "Avg unit price declining 4.2% per quarter. Customer is shifting toward lower-price-point items. If this continues, projected annual impact: -$18K revenue at same unit volume."

**Diagnostic**:
- Cheaper items = they're repositioning their store, or a competitor is winning the premium end
- More discounts = your rep is giving away margin to hold the account
- More promo = they're cherry-picking deals, not buying the line

**Data source**: `portal_invoice_items.unit_price`, `orders.discount_percent`, `orders.discount_amount`

---

## 6. Same-Store Comps (Multi-Location Accounts)

**What it does**: For customers with multiple ship-to locations, compares performance across locations.

**How it works**: `portal_orders` or `portal_invoice_items` grouped by `customer_ship_to_number`, trended over time.

**Example output**:
> "Charlotte: $168K (+24% YoY) | Asheville: $78K (+11%) | Greenville: $38K (-18%)
>
> Greenville is declining. 4 of its top items had stockouts in Q1. Charlotte and Asheville didn't. The Greenville decline may be supply-driven, not demand-driven."

**Why it's valuable**: No furniture manufacturer is doing same-store comp analysis on their dealer network. Retail chains do this internally; the manufacturer seeing it across their dealer's locations is a new lens entirely.

**Data source**: `portal_orders.customer_ship_to_number` or `portal_invoice_items` via invoice ship-to, `shipping_locations`

---

## 7. Category Share Evolution (Drift Detection)

**What it does**: Tracks how this customer's category mix is shifting over time — and whether dollars that left a category stayed with you or went to a competitor.

**How it works**: `portal_invoice_items` grouped by category per period. Compare LTM vs. prior year. When a category declines but total business grows, the dollars went somewhere else.

**Example output**:
> "Bedroom: 12% of spend → 3% (-9 pts, -$21.8K). Total business grew +17.7%. The Bedroom dollars didn't go to another of your categories. They went somewhere else."

**Why it's valuable**: "They buy less Bedroom" is descriptive. "They buy less Bedroom FROM YOU while spending MORE overall" is a competitive loss signal invisible without total-business context.

**Data source**: `portal_invoice_items` + `products.category_code` + `portal_orders` (total business)

---

## 8. Market Commitment Conversion by Category

**What it does**: Breaks market commitment conversion by product category to identify which categories the customer commits to at market but doesn't follow through on.

**How it works**: `commitment_reports` (items parsed from text blob) cross-referenced with `portal_order_items` post-market, grouped by `products.category_code`.

**Example output**:
> "Upholstery: 91% conversion | Lighting: 95% | Outdoor: 0% | Bedroom: 0%
>
> They committed to Outdoor and Bedroom at market and ordered nothing. These are the same categories where they're under-indexing. Something blocks the purchase — floor space? Pricing? Confidence in the line?"

**Why it's valuable**: Moves from "here's what the data says" to "here's the question to ask in the meeting."

**Data source**: `commitment_reports` + `portal_order_items` + `products`

---

## 9. Fulfillment Impact on Reorder Behavior

**What it does**: Quantifies the revenue impact of backorders on this specific customer's reorder patterns.

**How it works**: Correlate backorder events (from `portal_order_items.quantity_backordered`) with subsequent reorder intervals for the same item at the same customer.

**Example output**:
> "When this customer experiences a backorder, their subsequent reorder interval for that SKU increases by 2.3x (28 days → 65 days). Two items currently on backorder contribute $34K/year historically. Projected revenue impact from delayed reorders: -$14K annualized."

**Why it's valuable**: Turns an inventory problem into a revenue problem. VP Sales can take this to Operations: "fix this, it's costing us $14K at this one account."

**Data source**: `portal_order_items` (ordered vs. backordered) + `portal_orders.order_date` (subsequent reorder timing)

---

## 10. Account Lifecycle Stage (Cohort-Based Forecasting)

**What it does**: Places this customer on a lifecycle curve based on where every other similar customer has gone.

**How it works**: From `portal_orders`, compute the first-order date to determine account tenure. Group all customers by acquisition cohort (same region, same first-year spend level). Compute average spend trajectory at Year 1, 2, 3, 4+. Compare this customer's actual trajectory vs. cohort average.

**Example output**:
> "Magnolia is in Growth Stage (Month 26). Typical lifecycle:
> - Year 1: $120K avg (Magnolia was $142K — above curve)
> - Year 2: $240K avg (Magnolia is $284K — still above)
> - Year 3: $340K typical peak
>
> If they follow the typical pattern, they should peak around $400K next year. That's $116K of addressable growth."

**Why it's valuable**: Cohort-based forecasting. You're not guessing — you're showing where every other similar account went, and where this one is likely heading.

**Data source**: `portal_orders` (first order date, revenue per period) grouped by customer cohort

---

## 11. Competitive Loss Signal

**What it does**: Detects when a customer's orders with you are declining but their total business hasn't — meaning they're shifting spend to a competitor.

**How it works**: Compare eCat order trend (`orders`) with total business trend (`portal_orders`). If eCat declines but total business is flat/growing, the gap is going elsewhere.

**Example output**:
> "This customer's eCat orders declined -15% but their total business grew +8%. The $22K gap is going to another channel or supplier."

**Why it's valuable**: The only thing worse than a customer buying less is a customer buying less FROM YOU while spending MORE. This signal is invisible without ERP total-business context.

**Data source**: `orders` (eCat trend) vs. `portal_orders` (total business trend)

---

## Prioritization

| Insight | Impact | Complexity | Data Ready? |
|---|---|---|---|
| Next Best Product | Very High | Moderate | Yes |
| Wallet Share | Very High | Simple | Yes |
| Reorder Decay | High | Moderate | Yes |
| Buyer-Within-Customer | High | Simple | Yes |
| Category Drift / Competitive Loss | Very High | Simple | Yes |
| Price Erosion | High | Simple | Yes |
| Same-Store Comps | High | Simple | Yes |
| Market Commitment by Category | High | Moderate | Yes (requires text parsing) |
| Fulfillment Impact | Very High | Complex | Yes |
| Lifecycle Stage | High | Complex | Yes |
