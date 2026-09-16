# Section 04 Build Plan — Commerce Patterns

**Client**: Geo Contemporary (gcl) · Run date: 2026-06-17
**Confidence tier**: SECTION_CONFIDENCE_4 = PARTIAL → template `§4-PARTIAL`, label "PARTIAL VIEW"

**Governing gates**: HAS_PORTAL_ORDERS=False, HAS_CART=False, PORTAL_CUSTOMER_DATA_PRESENT=False, HAS_COMMITMENT_DATA=False, HAS_INVENTORY=False, VM45_RENDER=False. eCat-only section — no total-business / all-channel language anywhere.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Digital Ordering Share | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; VM45_RENDER=False) | NO |
| eCat Order Trend (Part A) | MANDATORY | MET (Q-18_partA has 13 months) | YES |
| eCat Share of Total Trend (Part B) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False) | NO |
| Top Buyers & Concentration | MANDATORY | MET (Q-13 has 15 rows; no Q-52 enrichment) | YES |
| Order Type & Workflow | MANDATORY | MET (Q-21 has 6 rows) | YES |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=False; Q-18A shows iPad only, 1 channel) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=False; Q-58 absent) | NO |
| Quote Economics | CONDITIONAL | MET (Q-21: 34 quotes, 182 confirmed; 10+ threshold) | YES |
| AOV Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV; Q-18 full/Part B absent) | NO |
| First-Time Buyer Acquisition | CONDITIONAL | MET (Q-41 has 16 months); no named-account trajectory data | YES |
| Seasonal Timing | CONDITIONAL | MET (Q-18_partA has 13 months of monthly series) | YES |
| Competitive Displacement | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-55 absent) | NO |
| Price Erosion | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-60 absent) | NO |

**Rendering order (strength → intelligence → opportunity → risk, filtered to met gates):**
1. eCat Order Trend (Part A)
2. Top Buyers & Concentration
3. Order Type & Workflow
4. Quote Economics
5. New Buyer Acquisition & Growth
6. Ordering Seasonality

Plus: section-level what-this-means.
