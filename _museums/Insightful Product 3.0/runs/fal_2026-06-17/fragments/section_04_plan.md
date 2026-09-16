# Section 04 Build Plan — Commerce Patterns

**Client**: Sarreid, Ltd. (fal) · Run date 2026-06-17
**Confidence tier**: SECTION_CONFIDENCE_4 = STRONG → template `§4-STRONG`, label "STRONG VIEW"

> REFRAMED guide (re-read §4): thesis = DIGITAL ENABLEMENT, not eCat share. §4 opens with
> Order Channel Mix, then **eCat Footprint** (NOT "eCat Ordering Share"). The opportunity is
> digitizing the rep-/back-office-entered order flow; eCat AND the client's own web are both
> valid digital paths. NEVER "grow eCat X%→Y% / each point worth $Z / capture rate / adoption
> stage." Do not make eCat obsolete.

## Key gate flags
- HAS_PORTAL_ORDERS = True
- VM45_RENDER = True
- HAS_CART = False
- PORTAL_CUSTOMER_DATA_PRESENT = True (Q-52 has 30 rows)
- PORTAL_REP_DATA_PRESENT = True (Q-56 has 19 rows)
- HAS_INVENTORY = True
- HAS_COMMITMENT_DATA = False (Q-58 / Q-58b absent)

## fal channel reality
- Q-CHANNEL-MIX: Your B2B web storefront = $9,981,063 (64.1%, 8,663 orders) — already digital, leave it.
- Rep- or ERP-entered = $5,580,407 (35.9%, 2,212 orders) — the enablement opportunity (NOT "manual/offline").
- eCat footprint (Q-45/Q-18-A): $2.6M LTM, 16.4% of total-business GMV, 604 orders, 100% iPad/rep-assisted.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Order Channel Mix | CONDITIONAL | MET (Q-CHANNEL-MIX has rows, NO DATA NOTE, 2 real channels, HAS_PORTAL_ORDERS=true) | YES |
| eCat Footprint | CONDITIONAL | MET (HAS_PORTAL_ORDERS=true, VM45_RENDER=true) | YES |
| eCat Order Trend | MANDATORY (Part A always; Part B conditional) | MET (Q-18-A monthly; Part B via HAS_PORTAL_ORDERS=true + Q-18-B) | YES (A+B) |
| Top Buyers & Concentration | MANDATORY (enrichment conditional) | MET; Q-52 enrichment MET (PORTAL_CUSTOMER_DATA_PRESENT=true + Q-52 rows) | YES (enriched) |
| Order Type & Workflow | MANDATORY | MET (Q-21: Confirmed 568, HFC 36; no quotes → lead with HFC governance pattern) | YES |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false; Q-18-A shows only iPad — online=0 → single channel) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false; Q-58 absent) | NO |
| Quote Economics | CONDITIONAL | NOT MET (0 quote orders in Q-20) | NO |
| AOV Spread by Rep | CONDITIONAL | NOT MET (Q-18 has no rep-level AOV data; Q-18_results.md absent) | NO |
| First-Time Buyer Acquisition | CONDITIONAL | MET (Q-41 has 15 months; named trajectories from Q-ORG-VELOCITY) | YES |
| Ordering Seasonality | CONDITIONAL | MET (13 months of eCat monthly volume via Q-18-A) | YES |
| Competitive Displacement | CONDITIONAL (MANDATORY when met) | NOT MET (Q-55: every row eCat share=0, change_ppts=0 → no row has total_growth>0 AND share_change<0) → SKIP silently | NO |
| Price Erosion / Product Mix | CONDITIONAL (MANDATORY when met) | MET (HAS_PORTAL_ORDERS=true + Q-60 has 14 rows) | YES (Part A only; Q-39 absent → no category Part B) |

## Rendering order (narrative arc: context → strength → intelligence → opportunity → risk)
1. Order Channel Mix (CONTEXT — full digital picture, FIRST)
2. eCat Footprint (CONTEXT — eCat as a tool, not a share)
3. eCat Order Trend (STRENGTH — more orders digitized)
4. Top Buyers & Concentration (INTELLIGENCE)
5. Order Type & Workflow (INTELLIGENCE)
6. New Buyer Acquisition & Growth (INTELLIGENCE)
7. Ordering Seasonality (INTELLIGENCE)
8. Product Mix & Pricing Trends (RISK — last)

## Why subsection 9 (Competitive Displacement) is skipped, not Part-B'd
The reframed guide gates subsection 9 on Q-55 Part A displacement (total_growth>0 AND
ecat_share_change<0). Every Q-55 row has eCat share = 0% and change = 0 ppts, so NO row
qualifies → skip silently (no false alarm). Rendering Q-56 rep-capture-decline alone as
"Channel Share Opportunity" would resurrect banned "grow eCat share / recapture" framing
with eCat at 0% in those categories — explicitly disallowed by the reframe. Omitted.

## Confidence header
SECTION_CONFIDENCE_4 = STRONG → label "Strong View" (§4-STRONG). LAST_PORTAL_ORDER_DATE
unresolvable (PORTAL_ORDERS_FRESH=false) but tier value used verbatim per shared contract §2
(do not recompute). Header kept to ≤2 sentences.
