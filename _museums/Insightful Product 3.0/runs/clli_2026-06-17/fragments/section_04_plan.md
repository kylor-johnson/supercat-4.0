# Section 04 Build Plan — Commerce Patterns (Craftmade / clli, 2026-06-17)

**Tier:** SECTION_CONFIDENCE_4 = STRONG → template §4-STRONG → label "STRONG VIEW"
**Thesis (REFRAMED):** DIGITAL ENABLEMENT, not eCat share. BANNED: "grow eCat X→Y", "each point worth $Z", "capture rate", "adoption/Early stage", "runway to N%". eCat = one tool in the mix; never made obsolete. Opportunity = digitizing rep-/back-office-entered order flow.
**Channel feed:** Q-CHANNEL-MIX carries a DATA NOTE (100% Unclassified) → DATA NOTE path: skip channel table, render one honest paragraph.

| # | Subsection (exact guide name) | MAND/COND | Gate Status | Will Render |
|---|---|---|---|---|
| 0 | Order Channel Mix | COND | MET — HAS_PORTAL_ORDERS=true; Q-CHANNEL-MIX has DATA NOTE → honest paragraph, NO table | YES (paragraph) |
| 1 | eCat Footprint | COND | MET — HAS_PORTAL_ORDERS=true; VM45_RENDER=false → standalone volume + "needs validated data sync" prose line | YES |
| 2 | eCat Order Trend | MAND (Part A always) | MET — Q-18A has 11 monthly rows; framed "more orders digitized", peak Jan 2026 | YES (Part A) |
| 4 | Top Buyers & Concentration | MAND | MET — Q-13 rows; Q-52 enrichment gate met → add Total Business + eCat Share cols (join on code: 9800, 44515 only) | YES (enriched) |
| 6 | Order Type & Workflow | MAND | MET — Q-21 rows. Quote≈Confirmed AOV (no premium) → lead with genuine high-AOV pattern (Liked/HFC), not fabricated quote premium | YES |
| 3 | Channel Migration | COND | NOT MET — HAS_CART=false; only iPad (eCat_online=0); Q-19 absent → single channel | NO (skip) |
| 11 | Market Commitment Attribution | COND | NOT MET — HAS_COMMITMENT_DATA=false; Q-58/Q-58b absent | NO (skip) |
| 5 | Quote Economics | COND | MET — 55 quotes (≥10) + Confirmed orders exist | YES |
| 8 | AOV Spread by Rep | COND | NOT MET — no rep-level rows (Q-18_results absent; only monthly partA/partB) | NO (skip) |
| 12 | First-Time Buyer Acquisition | COND | MET — Q-41 spans 6+ months; no named accounts in feed → render with explicit data-extension caveat | YES |
| 7 | Ordering Seasonality | COND | NOT MET — Q-21 has no monthly time series (order-type breakdown only) | NO (skip) |
| 9 | Channel Share Opportunity (Displacement) | COND/mand-when-met | NOT MET — no Q-55 category has total_growth>0 AND ecat_share_change<0; CAT rows $0 eCat; categories are internal codes | NO (skip — no false alarm) |
| 10 | Product Mix & Pricing Trends (Price Erosion) | COND/mand-when-met | GATE MET but ALL Q-60 names blank + artifact rows (−98%/−72% unit-mix) → render subsection via investigative callouts + WTM; NO anonymous-row table (entity rule + data quality) | YES (callout form) |

**Confidence header:** STRONG VIEW, immediately after `.section` open, before subsection 0.
**Section-level what-this-means:** YES (mandatory, max 3 sentences).
**Highlights file:** YES — `cache/section_04_highlights.md`, ≥1 positive.

## Data handling notes
- Q-13 rows "Craftmade Sample Account" / "Craftmade Warranty Account" = house accounts → exclude from buyer-intelligence framing; do not present as customers.
- Q-52 names blank → join Total Business / eCat Share by customer code (9800=Ferguson $2.6M total/0.6%, 44515=Fort Worth Lighting $923K total/2.2%); other Q-13 buyers absent from Q-52 → "—" (not a placeholder column-of-dashes; columns carry real values for the joinable rows).
- Q-60 names all blank + corrupt unit-mix rows → no per-account table; summarize count + combined real GMV, multi-causal, request customer detail.
- ECAT_GMV = $881,333 LTM (Q-45); total business = $47.7M LTM. eCat footprint ≈ 1.8% of total — state as footprint, NOT a share to grow.

## Forbidden-term watch
- BANNED: capture rate, adoption/Early stage, "grow eCat A%→B%", "each point worth $X", runway-to-N%, ERP, Mixpanel, Clicky, portal orders, platform (standalone), segment labels, internal IDs.
- Non-eCat orders never "manual/offline/non-digital" as certainty → "rep- or back-office-entered."
