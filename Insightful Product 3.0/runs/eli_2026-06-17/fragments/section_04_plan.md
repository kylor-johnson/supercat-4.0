# Section 04 Build Plan — Commerce Patterns

Section ID: commerce · Section Number: §4 · Confidence Tier (SECTION_CONFIDENCE_4): **STRONG**

Key gates: HAS_PORTAL_ORDERS=False · HAS_CART=True · HAS_COMMITMENT_DATA=False · PORTAL_CUSTOMER_DATA_PRESENT=False · PORTAL_REP_DATA_PRESENT=False · VM45_RENDER=False · HAS_INVENTORY=True

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false) | NO |
| eCat Order Trend | MANDATORY (Part A always) | MET (Q-18_partA has 13 months); Part B NOT MET (no portal) | YES (Part A only) |
| Top Buyers & Concentration | MANDATORY | MET (Q-13 has 15 rows); enrichment NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false, Q-52 absent) | YES (Q-13-only) |
| Order Type & Workflow | MANDATORY | MET (Q-21 has Confirmed/Quote/HFC) | YES |
| Channel Migration | CONDITIONAL | MET (HAS_CART=true; Q-18_partA has iPad/Online split) | YES (eCat-only, no share overlay) |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false, Q-58 absent) | NO |
| Quote Economics | CONDITIONAL | NOT MET (Q-20 shows only 6 quotes; threshold ≥10) | NO |
| AOV Spread by Rep | CONDITIONAL | NOT MET (Q-18 has no rep-level AOV; no spread computable) | NO |
| First-Time Buyer Acquisition | CONDITIONAL | MET (Q-41 spans 14 months by channel; no named-account trajectory data) | YES (aggregate + data-gap note) |
| Ordering Seasonality | CONDITIONAL | MET (Q-18_partA gives 13 months of monthly eCat sales) | YES |
| Competitive Displacement | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false, Q-55 absent) | NO |
| Price Erosion | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false, Q-60 absent) | NO |

Render order (narrative arc): eCat Order Trend → Top Buyers & Concentration → Order Type & Workflow → Channel Migration → First-Time Buyer Acquisition → Ordering Seasonality.

Section-level what-this-means: YES (mandatory).
Confidence header: STRONG → §4-STRONG. {{LAST_PORTAL_ORDER_DATE}} not resolvable (no portal orders) → fall back to §4-PARTIAL template text per guide. Tier LABEL stays from STRONG row = "Strong View".
Note: Because HAS_PORTAL_ORDERS=false, no "total business" / "all-channel" references anywhere; eCat-only framing throughout.
