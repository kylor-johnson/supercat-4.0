# Section 02 Build Plan — Account Intelligence

Client: Craftmade (clli, org_id=149) · Run date 2026-06-17 · Tier: STRONG (SECTION_CONFIDENCE_2)

## Data reality notes (drive rendering decisions)
- `top_accounts.md` is degenerate (single "20 accounts" row) — mini-briefs are built by
  joining named accounts (Q-14, Q-17) to enrichment files keyed on `customer_code`
  (Q-52 penetration, Q-ORG-DECAY-items, Q-ORG-CONTRACTION, Q-ORG-VELOCITY, Q-ORG-STOCKOUT).
- Q-52 / Q-53 / Q-68 / Q-ORG-CONTRACTION / Q-ORG-VELOCITY / Q-ORG-DECAY-items have **blank
  customer_name** (only `customer_code`). `customer_code` is a banned internal ID — never
  rendered. Tables from these sources either (a) use the name resolved via Q-14/Q-17 join,
  or (b) suppress the unresolvable Customer column and render as an aggregate/anonymized view.
- Q-53 / Q-68 customer names fully blank → cannot name entities → render as aggregate
  insight (callout + summary), not a name-keyed leaderboard, per "handle thin data gracefully."

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET | YES |
| 2. Data Confidence Header | MANDATORY | MET (STRONG) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET (built via named-account join) | YES |
| 3b. eCat Penetration of Total Business (Q-52) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true, 30 rows) | YES |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT, 25 rows) | YES |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=false; Q-66 not present) | NO |
| 9. Untapped Category Opportunities (Q-57) | MANDATORY when gate met | NOT MET (Q-57 row_count=0) | NO |
| 5. Unactivated High-Value Accounts (Q-53) | CONDITIONAL (SIG-OPP-02) | MET (20 rows) but names blank → aggregate render | YES (aggregate) |
| 6. Geographic Distribution (Q-40/Q-54) | CONDITIONAL | MET (TX concentration > 30% of eCat GMV) | YES |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (17 rows) | YES |
| 8b. Velocity Deceleration Alert (Q-14b) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true, 15 rows) but names blank → aggregate | YES (aggregate) |
| 4. Dormant High-Value Accounts (Q-17) | CONDITIONAL (SIG-RISK-02) | MET (named rows ≥ $15K, 90+ days) | YES |
| 7. Velocity Deceleration / Contraction (Q-ORG-CONTRACTION) | CONDITIONAL (SIG-DECAY-04) | MET (25 rows) but names blank → aggregate + hypotheses | YES (aggregate) |
| 12. Spending Contraction (Q-68) | MANDATORY when gate met | MET (20 rows) but names blank → aggregate | YES (aggregate, COLLAPSE) |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL exclusion set produced) | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

## Mini-brief account roster (named, joined)
1. Ferguson Enterprises Inc (9800) — $2.6M total business, 0.6% eCat pen; 7 eCat orders LTM; multiple decaying fan SKUs; stock-out exposure (PH-2BZ).
2. Fort Worth Lighting (44515) — $923K total business, 2.2% pen; dormant on eCat (359d); decaying SKUs Z421-MN-LED / P104FB5.
3. Inline Electric Supply (70056) — $393K total business, 2.1% pen; total business -23.8% YoY but eCat +213% (channel shift toward eCat).
4. GW Keeter Lighting & Home (50891) — $286K total business, 3.4% pen (highest of named book); 3 eCat orders.
5. Metro Lighting (18720) — $306K total business, 3.0% pen; dormant on eCat (154d).
6-10 (collapsed): White Oak Cottage (43128), Coastal Lighting LLC (30800), Lady Home (44169), Hajoca Corp (50900), JD Designs Inc (44067).
