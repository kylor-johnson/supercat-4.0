# Section 04 Build Plan — Commerce Patterns

Client: Hubbardton Forge (hfg) · Run date: 2026-06-17
Confidence tier (SECTION_CONFIDENCE_4): **STRONG** → template `§4-STRONG` / label `STRONG VIEW`

Key gates: HAS_PORTAL_ORDERS=true · HAS_CART=false · HAS_COMMITMENT_DATA=false · HAS_INVENTORY=false · PORTAL_CUSTOMER_DATA_PRESENT=true · PORTAL_REP_DATA_PRESENT=true · VM45_RENDER=true
Q-CHANNEL-MIX: 100% "Unclassified" — file contains a DATA NOTE → render the honest one-paragraph path, NO channel table. eCat is one channel; never imply non-eCat = manual/offline.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Order Channel Mix | CONDITIONAL | MET (HAS_PORTAL_ORDERS=true, file exists) — DATA NOTE present → honest paragraph, no table | YES (paragraph) |
| eCat Footprint | CONDITIONAL | MET (HAS_PORTAL_ORDERS=true, VM45_RENDER=true; eCat $16.7M = 39.9% of $42.0M total business per Q-45). Footprint-as-tool, NO capture/adoption framing | YES |
| eCat Order Trend | MANDATORY (Part A always) | MET — Part B too (HAS_PORTAL_ORDERS=true) via Q-18-A + Q-18-B | YES |
| Top Buyers & Concentration | MANDATORY (always) | MET — Q-52 enrichment MANDATORY (PORTAL_CUSTOMER_DATA_PRESENT=true, Q-52 has rows); join Q-13↔Q-52 on customer | YES (enriched) |
| Order Type & Workflow | MANDATORY (always) | MET (Q-21: Quote/Confirmed/HFC; quote premium 2.5x) | YES |
| Channel Migration | CONDITIONAL | NOT MET (HAS_CART=false; eCat Online=0 all 13 months — only 1 active channel) | NO |
| Market Commitment Attribution | CONDITIONAL — MANDATORY when gate met | NOT MET (HAS_COMMITMENT_DATA=false; Q-58 absent) | NO |
| Quote Economics | CONDITIONAL | MET (1,396 quotes + 472 confirmed > 10) | YES |
| AOV Spread by Rep | CONDITIONAL | NOT MET (no rep-level AOV; Q-18 combined absent, Q-18-A has no rep dim, Q-56 has no AOV/order counts) | NO |
| First-Time Buyer Acquisition | CONDITIONAL | MET (Q-41 16 months) — named trajectories from Q-ORG-VELOCITY | YES |
| Ordering Seasonality | CONDITIONAL | MET (12+ months eCat monthly GMV from Q-18-A) | YES |
| Competitive Displacement | CONDITIONAL — MANDATORY when gate met | NOT MET (Q-55: no category with total_growth_pct>0 AND ecat_share_change_ppts<0 — both categories contracted) → skip silently incl. Part B | NO |
| Price Erosion | CONDITIONAL — MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true, Q-60 has 20 rows). Part B (category) omitted — Q-39 absent | YES |

Section-level what-this-means: YES (mandatory).
Confidence header: YES — STRONG VIEW, immediately after header metrics / before first subsection. LAST_PORTAL_ORDER_DATE resolvable (days_since_last_erp_order=1 → 2026-06-16).

Render order (narrative arc strength→intelligence→opportunity→risk):
confidence header → Order Channel Mix → eCat Footprint → eCat Order Trend → Top Buyers & Concentration → Order Type & Workflow → Quote Economics → New Buyer Acquisition & Growth → Ordering Seasonality → Product Mix & Pricing Trends → section what-this-means.

THESIS REMINDER: digital enablement, not eCat share. eCat handles $16.7M (rep-assisted/field/showroom/visual selling, all iPad). Opportunity = digitizing rep-/phone-/email-entered order flow (eCat AND client's own web both valid). NEVER "grow eCat X%→Y% / each point worth $Z / capture rate / adoption stage." Don't make eCat obsolete.
