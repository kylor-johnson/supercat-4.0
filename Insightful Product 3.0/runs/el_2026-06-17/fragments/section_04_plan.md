# Section 04 Build Plan — Commerce Patterns

**Client:** Eurofase Inc. (el) · **Run date:** 2026-06-17
**Confidence tier (SECTION_CONFIDENCE_4):** STRONG → `§4-STRONG` template, label "STRONG VIEW"
**Key gates:** HAS_PORTAL_ORDERS=true · HAS_CART=false · HAS_COMMITMENT_DATA=false · HAS_INVENTORY=true · VM45_RENDER=true · PORTAL_CUSTOMER_DATA_PRESENT=true · PORTAL_REP_DATA_PRESENT=true
**LAST_PORTAL_ORDER_DATE:** 2026-06-16 (days_since_last_erp_order=1)

> REFRAMED GUIDE — thesis = DIGITAL ENABLEMENT, not eCat share. §1 is "eCat Footprint" (NOT "eCat Ordering Share"). No capture-rate / grow-X%-to-Y% / each-point-worth-$Z language. Opportunity = streamlining rep-/phone-/email-entered order flow; eCat AND client web both valid digital paths.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Order Channel Mix | CONDITIONAL | MET but DATA NOTE present (86.1% Rep/ERP) -> render single honest paragraph, no table | YES (paragraph) |
| eCat Footprint | CONDITIONAL | MET (HAS_PORTAL_ORDERS=true, VM45_RENDER=true; eCat $1.6M / 39.0% of total business — footprint, not a share-to-grow) | YES |
| eCat Order Trend | MANDATORY (A always) | MET; Part B MET (HAS_PORTAL_ORDERS=true) -> add total business + share cols | YES (A+B) |
| Top Buyers & Concentration | MANDATORY | MET; Q-52 enrichment MANDATORY (PORTAL_CUSTOMER_DATA_PRESENT=true, Q-52 rows present) | YES (enriched) |
| Order Type & Workflow | MANDATORY | MET; no Quote orders -> lead with dominant workflow (HFC) per fallback | YES |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false; only 1 channel iPad; ecat_online=0 all months) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false; Q-58 not present) | NO |
| Quote Economics | CONDITIONAL | NOT MET (0 quote orders in Q-20) | NO |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET (no rep-level eCat AOV data; Q-18_results.md absent, partA has no rep col) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET (Q-41 11 months >=6; named trajectories from Q-ORG-VELOCITY) | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET (guide sources from Q-21; Q-21 has no monthly time series, only 2 order-type rows) | NO |
| Channel Share Opportunity (Competitive Displacement) | CONDITIONAL (MANDATORY when criteria met) | NOT MET (Q-55: no row has total_growth>0 AND ecat_share_change<0; all share_change=0 b/c eCat=$0 every category) | NO |
| Product Mix & Pricing Trends (Price Erosion) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true, Q-60 has 3 rows) | YES (Part A; Part B omitted - Q-39 absent) |

## Render order (narrative arc): strength -> intelligence -> opportunity -> risk
0. Order Channel Mix (context paragraph, FIRST)
1. eCat Footprint
2. eCat Order Trend (A+B)
4. Top Buyers & Concentration (enriched)
6. Order Type & Workflow
12. New Buyer Acquisition & Growth
10. Product Mix & Pricing Trends (risk, last)

## Notes
- Channel mix has DATA NOTE -> NO table; honest paragraph + frame opportunity as streamlining rep-/back-office-entered volume. Never call non-eCat "manual/offline".
- Q-13 pct_of_ecat_gmv column mis-formatted ($5/$4/...) = bad source col; ignore it. Compute % of eCat GMV against the eCat-GMV basis implied by SIG-RISK-01 (top-5 = 48%).
- SIG-RISK-01 (P1, §4): top 5 eCat buyers = 48% of eCat GMV ($255,309). Render Revenue Concentration callout (exceeds 25% threshold). eCat-GMV basis ~ $531,894.
- eCat Footprint: $1.6M eCat, 39.0% of $4.1M total business. VM45_RENDER=true. Frame as tool footprint, opportunity = rep/back-office volume.
- Confidence header MANDATORY at top (STRONG VIEW).
