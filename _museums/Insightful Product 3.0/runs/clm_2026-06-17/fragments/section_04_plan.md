# Section 04 Build Plan — Commerce Patterns

**Client**: Crystorama (clm) · **Run date**: 2026-06-17 · **Confidence tier (SECTION_CONFIDENCE_4)**: STRONG → `§4-STRONG` / "STRONG VIEW"

**Thesis (REFRAMED guide): DIGITAL ENABLEMENT, not eCat share.** eCat is ONE tool in the order mix; the opportunity is digitizing the rep-/phone-/email-entered order flow — NOT growing an eCat capture rate. NEVER use "capture rate", "adoption stage", "Early/Emerging/Dominant", "grow eCat X%→Y%", "each point worth $Z", or imply non-eCat orders are manual/offline. Never make eCat look obsolete.

Key gates: HAS_PORTAL_ORDERS=true · HAS_CART=false · HAS_COMMITMENT_DATA=false · HAS_INVENTORY=true · VM45_RENDER=false · PORTAL_CUSTOMER_DATA_PRESENT=true · PORTAL_REP_DATA_PRESENT=false
Q-CHANNEL-MIX contains a **DATA NOTE** (100% Unclassified — feed lacks order-origin detail) → render honest prose paragraph, NOT a channel table. clm = thin order-origin DATA NOTE path.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Order Channel Mix | CONDITIONAL | MET — Q-CHANNEL-MIX present but DATA NOTE → render honest prose, no table | YES (prose) |
| eCat Footprint | CONDITIONAL | MET — HAS_PORTAL_ORDERS=true. eCat = $551,721 LTM (footprint as a tool, NOT a share-to-grow). VM45_RENDER=false → standalone volume + data-sync prose line | YES |
| eCat Order Trend | MANDATORY (Part A always) | MET — Q-18-A 12 months. Part B MET (HAS_PORTAL_ORDERS=true, Q-18-B total business) | YES |
| Top Buyers & Concentration | MANDATORY | MET — Q-13 15 rows. Q-52 enrichment: no Q-13 buyer matches a Q-52 row (all Q-52 ecat_gmv=$0; different account set) → render base Q-13 table (no empty cols), penetration context in WTM | YES |
| Order Type & Workflow | MANDATORY | MET — Q-21 (Confirmed 139, HFC 25, Quote 1) | YES |
| Channel Migration | CONDITIONAL | NOT MET — HAS_CART=false; eCat Online=0; single channel (iPad only) | NO |
| Market Commitment Attribution | CONDITIONAL | NOT MET — HAS_COMMITMENT_DATA=false; Q-58/Q-58b absent | NO |
| Quote Economics | CONDITIONAL | NOT MET — only 1 quote (<10) | NO |
| AOV Spread by Rep | CONDITIONAL | NOT MET — no rep-level AOV (PORTAL_REP_DATA_PRESENT=false; Q-18-A has no rep dimension) | NO |
| New Buyer Acquisition & Growth | CONDITIONAL | MET — Q-41 13 months; named trajectories from Q-ORG-VELOCITY | YES |
| Ordering Seasonality | CONDITIONAL | MET — Q-18-A spans 12 months of eCat sales (monthly series). Frame Jan-2026 spike as an onboarding event, not a recurring seasonal peak | YES |
| Competitive Displacement (Q-55) | CONDITIONAL (mandatory when criteria met) | NOT MET — no category has total_growth_pct>0 AND ecat_share_change_ppts<0 → skip silently | NO |
| Price Erosion (Q-60) | CONDITIONAL (mandatory when gate met) | MET — HAS_PORTAL_ORDERS=true, Q-60 has 20 rows. Part B (category) NOT MET — Q-39 absent | YES (Part A) |

**Render order (narrative arc):** Order Channel Mix → eCat Footprint → eCat Order Trend → Top Buyers & Concentration → Order Type & Workflow → New Buyer Acquisition & Growth → Ordering Seasonality → Product Mix & Pricing Trends → section-level what-this-means.
