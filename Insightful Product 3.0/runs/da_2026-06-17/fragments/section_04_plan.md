# Section 04 Build Plan — Commerce Patterns

Confidence tier: `SECTION_CONFIDENCE_4 = STRONG`. `{{LAST_PORTAL_ORDER_DATE}}` cannot
be resolved (`HAS_PORTAL_ORDERS = false`) → fall back to `§4-PARTIAL` template,
label `PARTIAL VIEW` per guide variable-resolution rule.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| eCat Order Trend | MANDATORY (Part A) | MET (Q-18-A has 13 months) | YES |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false; ecat_online_orders=0 all months → single channel) | NO |
| Top Buyers & Concentration | MANDATORY | MET (Q-13 has 15 rows); enrichment NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false) | YES (base table only) |
| Quote Economics | CONDITIONAL | NOT MET (Q-20 Quote Orders=0) | NO |
| Order Type & Workflow | MANDATORY | MET (Q-21 has rows); no quotes → lead with dominant workflow | YES |
| Ordering Seasonality | CONDITIONAL | MET (Q-18-A has 13 months of monthly data) | YES |
| AOV Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV; Q-18 absent, Q-18-A has no rep dimension) | NO |
| Competitive Displacement | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| Price Erosion | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET (Q-41 has 12 months); account-level trajectory NOT available → state explicitly | YES |

Render order (narrative arc): eCat Order Trend → Top Buyers & Concentration →
Order Type & Workflow → Ordering Seasonality → New Buyer Acquisition & Growth.

Section-level what-this-means: MANDATORY, present.
Forbidden-terms check: no "total business", "all-channel", "portal", "platform" standalone,
"ERP", "Mixpanel", segment labels, internal IDs.
