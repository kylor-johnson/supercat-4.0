# Section 04 Build Plan — Commerce Patterns

**Client**: Bulbrite (bri, org_id=222) · **Run**: 2026-06-17
**Confidence tier (SECTION_CONFIDENCE_4)**: STRONG → template `§4-STRONG` → label "Strong View"

**THESIS = DIGITAL ENABLEMENT, not eCat share.** §4 opens with Order Channel Mix
then **eCat Footprint** (NOT "eCat Ordering Share"). The opportunity is digitizing
the rep-/phone-/email-entered order flow; eCat AND the client's own web are both
valid paths. NEVER "grow eCat X%→Y% / each point worth $Z / capture rate / adoption
stage." Do not make eCat obsolete. bri ERP feed is thin on order-origin
(Q-CHANNEL-MIX = 100% Rep/ERP-entered, DATA NOTE present) → DATA NOTE paragraph path.

## Key gate values
- HAS_PORTAL_ORDERS = True
- HAS_CART = True
- VM45_RENDER = True
- PORTAL_CUSTOMER_DATA_PRESENT = True (Q-52 has 30 rows)
- PORTAL_REP_DATA_PRESENT = False
- HAS_COMMITMENT_DATA = False
- HAS_INVENTORY = True
- Q-CHANNEL-MIX contains a DATA NOTE (100% Rep/ERP-entered) → DATA NOTE path

## Subsection manifest (narrative arc order: Strength → Intelligence → Opportunity → Risk)

| Subsection (exact guide name) | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Order Channel Mix | CONDITIONAL | MET but DATA NOTE present → SKIP table, render honest standalone paragraph | YES (paragraph only) |
| eCat Footprint | CONDITIONAL | MET (HAS_PORTAL_ORDERS=true, VM45_RENDER=true; Q-45 row: $3.5M eCat, 18.6% of total business) | YES |
| eCat Order Trend | MANDATORY | MET (always; Part B total-business cols added since HAS_PORTAL_ORDERS=true) | YES |
| Top Buyers & Concentration | MANDATORY | MET (always; Q-52 enrichment added since PORTAL_CUSTOMER_DATA_PRESENT=true) | YES |
| Order Type & Workflow | MANDATORY | MET (always; Q-21 has rows). Only 5 quotes & quote AOV < confirmed → lead with dominant workflow, NOT a quote-premium pitch | YES |
| Channel Migration | CONDITIONAL | MET (HAS_CART=true; iPad vs eCat Online from Q-18-A/Q-20) | YES |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false; Q-58 absent) | NO |
| Quote Economics | CONDITIONAL | NOT MET (only 5 quotes LTM; threshold 10+) | NO |
| Average Order Value Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV in Q-18; PORTAL_REP_DATA_PRESENT=false) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET (Q-41 has 16 months of monthly new-buyer data, by channel) | YES |
| Ordering Seasonality | CONDITIONAL | NOT MET (guide source = Q-21, which has no monthly series; only 2 order-type rows). Monthly trajectory already shown in eCat Order Trend | NO |
| Channel Share Opportunity (Competitive Displacement) | CONDITIONAL (mandatory when met) | NOT MET (Q-55 all rows ecat_share_change_ppts=0; no row total↑ AND share↓) | NO (skip silently) |
| Product Mix & Pricing Trends (Price Erosion) | CONDITIONAL (mandatory when met) | MET (HAS_PORTAL_ORDERS=true; Q-60 has 20 rows) | YES |

## Render order in fragment
1. Order Channel Mix (honest DATA NOTE paragraph)
2. eCat Footprint
3. eCat Order Trend (A+B)
4. Top Buyers & Concentration (enriched)
5. Order Type & Workflow
6. Channel Migration
7. New Buyer Acquisition & Growth
8. Product Mix & Pricing Trends (Price Erosion — risk, last)
+ Section-level what-this-means + "With Connected Data" note

## Notes
- Confidence header placed immediately after the data-confidence label, before first subsection (tier=STRONG, EXACT value, not recomputed).
- Order Channel Mix: DATA NOTE path → no channel table; one honest paragraph; eCat presented standalone below. Never imply non-eCat = manual/offline/non-digital.
- eCat Footprint: factual footprint, NOT a share-to-grow. No "Adoption Stage" ladder. Opportunity framed as digitizing rep-/back-office-entered flow; eCat AND own web both valid.
- Price Erosion Part B (category-level) omitted silently — Q-39 not present.
- Rep Capture Trend (9B) omitted — PORTAL_REP_DATA_PRESENT=false and Q-56 absent.
- All-channel monthly totals from Q-16/Q-18-B; quarterly figures aggregated from monthly eCat (Q-18-A) and all-channel (Q-16).
- Entity names title-cased; internal `**`/`***` flags and customer codes stripped from display.
