# Section 04 Build Plan — Commerce Patterns

Client: Currey & Company (cci) · Run date: 2026-06-17
Confidence tier (SECTION_CONFIDENCE_4): **STRONG** → template `§4-STRONG`, label `STRONG VIEW`.
LAST_PORTAL_ORDER_DATE: 2026-06-15 (days_since_last_erp_order=2)

THESIS (reframed guide): **DIGITAL ENABLEMENT, not eCat market share.** Lead with the full
channel mix; frame the rep-/back-office-entered volume ($25.2M, 28.7%) as the enablement
opportunity. eCat ($8.0M), the client's own B2B web ($23.7M), and EDI ($12.6M) are ALL valid
digital paths — volume on their web/EDI is healthy, leave it. Never write "grow eCat from X% to
Y%", "capture rate", "each point worth $Z", or "adoption stage". eCat's role = rep-assisted /
field / showroom / visual selling.

Key gates: HAS_PORTAL_ORDERS=True, HAS_CART=False, VM45_RENDER=True,
PORTAL_CUSTOMER_DATA_PRESENT=True, PORTAL_REP_DATA_PRESENT=True, HAS_COMMITMENT_DATA=False,
HAS_INVENTORY=True.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Order Channel Mix | CONDITIONAL (render FIRST) | MET (HAS_PORTAL_ORDERS=True; Q-CHANNEL-MIX has 6 channel rows, no DATA NOTE) | YES |
| eCat Footprint | CONDITIONAL | MET (HAS_PORTAL_ORDERS=True, VM45_RENDER=True) — footprint as a tool, NOT a share to grow | YES |
| eCat Order Trend | MANDATORY (Part A always) | MET (Q-18-A 13 months); Part B MET (Q-18-B total business) | YES |
| Top Buyers & Concentration | MANDATORY | MET (Q-13 15 rows; Q-52 enrichment MET → add Total Business + eCat Share) | YES |
| Order Type & Workflow | MANDATORY | MET (Q-21 Confirmed/Quote/HFC; Quote AOV $4,818 vs Confirmed $2,065) | YES |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=False; eCat Online=0 every month → single iPad channel, no migration) | NO |
| Market Commitment Attribution | CONDITIONAL (MANDATORY when gate met) | NOT MET (HAS_COMMITMENT_DATA=False; Q-58/Q-58b absent) | NO |
| Quote Economics | CONDITIONAL | MET (Q-20: 108 quotes ≥10, Confirmed orders exist) | YES |
| AOV Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV data; Q-18-A monthly only, Q-56 lacks order counts/AOV) | NO |
| First-Time Buyer Acquisition | CONDITIONAL | MET (Q-41 16 months of new-buyer counts; named trajectories from Q-ORG-VELOCITY) | YES |
| Ordering Seasonality | CONDITIONAL | MET (Q-18-A 13 months of eCat monthly data → derive monthly index) | YES |
| Competitive Displacement | CONDITIONAL (MANDATORY when gate met) | NOT MET (Q-55: every category ecat_share_change_ppts=0; no displacement row) | NO |
| Price Erosion / Product Mix | CONDITIONAL (MANDATORY when gate met) | MET (HAS_PORTAL_ORDERS=True, Q-60 20 rows) | YES |

Render order (narrative arc, only rendered subsections):
0. Order Channel Mix (CONTEXT — full digital picture + enablement opportunity)
1. eCat Footprint (CONTEXT — eCat's volume as a tool in the mix)
2. eCat Order Trend (STRENGTH — more orders digitized)
4. Top Buyers & Concentration (INTELLIGENCE)
6. Order Type & Workflow (INTELLIGENCE)
5. Quote Economics (OPPORTUNITY)
12. New Buyer Acquisition & Growth (INTELLIGENCE)
7. Ordering Seasonality (INTELLIGENCE)
10. Product Mix & Pricing Trends / Price Erosion (RISK — last)

Plus section-level what-this-means + "With Connected Data" note.

## Channel mix numbers (Q-CHANNEL-MIX)
- eCat (SuperCat app/online): 3,470 orders · $8,044,701 · 9.2%
- Your B2B web storefront: 13,215 · $23,740,872 · 27.0% (largest digital channel → row-highlight)
- EDI / drop-ship partners: 19,025 · $12,569,735 · 14.3%
- Trade markets / showrooms: 2,846 · $17,830,335 · 20.3%
- Rep- or ERP-entered: 19,065 · $25,215,110 · 28.7% (THE ENABLEMENT OPPORTUNITY)
- Unclassified: 306 · $506,290 · 0.6%
- Self-service digital (eCat+Web+EDI) = $44.4M (50.5%). Rep/ERP+Unclassified = $25.7M (29.3%).

## Q-55 displacement: SKIP §9
Every category shows current/prior eCat share = 100% (query only sees eCat-originated GMV), so
ecat_share_change_ppts = 0 for all rows. No row has total_growth>0 AND share_change<0 → no
displacement signal → skip silently (no false alarm).
