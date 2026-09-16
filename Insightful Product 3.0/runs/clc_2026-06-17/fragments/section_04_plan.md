# Section 04 Build Plan — Commerce Patterns

**Client**: Capital Lighting Fixture Co. (clc, org_id=40)
**Confidence tier (SECTION_CONFIDENCE_4)**: STRONG → template §4-STRONG, label "STRONG VIEW". `{{LAST_PORTAL_ORDER_DATE}}` unresolvable (PORTAL_ORDERS_FRESH=false, days_since=9999) → header text avoids citing a fresh portal date.

## Gate inputs
- HAS_PORTAL_ORDERS = True
- HAS_CART = False
- HAS_COMMITMENT_DATA = False
- HAS_INVENTORY = True
- VM45_RENDER = False (Gate2 fail: eCat $1.3M < 5% of $63.2M)
- PORTAL_CUSTOMER_DATA_PRESENT = True (Q-52 has rows)
- PORTAL_REP_DATA_PRESENT = True
- Q-CHANNEL-MIX contains a DATA NOTE (100% Rep/ERP/Unclassified) → DATA NOTE path: honest paragraph, no table

## Subsection manifest (rendered in narrative-arc order)

| Subsection (exact guide name) | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Order Channel Mix | CONDITIONAL (render FIRST) | MET but file has DATA NOTE → DATA NOTE path: render single honest paragraph (NO table) | YES |
| eCat Footprint | CONDITIONAL | MET (HAS_PORTAL_ORDERS=true). VM45_RENDER=false → eCat standalone footprint + data-sync caveat line; NO capture-rate/adoption-stage/share-to-grow framing | YES |
| eCat Order Trend | MANDATORY (Part A always) | MET (Q-18A present). Part B share cols added since HAS_PORTAL_ORDERS=true | YES |
| Top Buyers & Concentration | MANDATORY (always) | MET (Q-13 present; Q-52 enrichment MANDATORY — PORTAL_CUSTOMER_DATA_PRESENT=true + Q-52 rows) | YES |
| Order Type & Workflow | MANDATORY (always) | MET (Q-21 present; 0 quotes → lead with dominant workflow / Hold premium, not quote premium) | YES |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false; only 1 channel — 100% iPad, eCat Online=0; Q-19 not present) | NO |
| Market Commitment Attribution | CONDITIONAL (mandatory when gate met) | NOT MET (HAS_COMMITMENT_DATA=false; Q-58/Q-58b not present) | NO |
| Quote Economics | CONDITIONAL | NOT MET (Q-20 Quote Orders=0; <10 quotes) | NO |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET (Q-18 has no per-rep eCat AOV; Q-56 eCat all $0) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | NOT MET (Q-41 only 5 sparse months <6; Jan=193 is activation/backfill artifact; no account-level trajectory/names to make it intelligence) | NO |
| Ordering Seasonality | CONDITIONAL | NOT MET (no 12-month eCat monthly series; Q-18A spans 5 sparse months) | NO |
| Channel Share Opportunity (Competitive Displacement) | CONDITIONAL (mandatory when gate met) | NOT MET (Q-55: every row eCat share=0 and share_change_ppts=0 → no displacement rows) | NO |
| Product Mix & Pricing Trends (Price Erosion) | CONDITIONAL (mandatory when gate met) | MET (HAS_PORTAL_ORDERS=true; Q-60 has 20 rows). Part B skipped — Q-39 category data not in bundle | YES |

**Rendered: 6 subsections** → Order Channel Mix, eCat Footprint, eCat Order Trend, Top Buyers & Concentration, Order Type & Workflow, Product Mix & Pricing Trends (Price Erosion).

**Thesis = DIGITAL ENABLEMENT, not eCat share.** NEVER "grow eCat X%→Y% / each point worth $Z / capture rate / adoption stage." Opportunity = digitizing the rep-/phone-/email-entered order flow; eCat AND the client's own web both valid. Don't make eCat obsolete — always name its specific strength (rep-assisted/field/showroom/visual selling).

Plus: data confidence header (top), section-level what-this-means, "With Connected Data" note.

## Notes
- Order Channel Mix DATA NOTE path: NEVER imply non-eCat = manual/offline/non-digital. eCat is ONE channel.
- eCat capture = $1.3M / $63.2M ≈ 2% → "Early" tier (<10%), `.badge.danger`.
- Q-60 Part B (category) requires Q-39 — absent → omit silently.
- Forbidden terms (ERP/portal/platform standalone/Mixpanel/Clicky/segment labels) suppressed.
