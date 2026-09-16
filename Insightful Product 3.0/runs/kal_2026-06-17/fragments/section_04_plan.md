# Section 04 Build Plan — Commerce Patterns

Client: Kalco Lighting / Allegri Crystal (kal), run 2026-06-17
SECTION_CONFIDENCE_4 = **STRONG** → §4-STRONG template, "STRONG VIEW" label.

THESIS = DIGITAL ENABLEMENT, not eCat share. §4 opens with Order Channel Mix,
then **eCat Footprint** (NOT "eCat Ordering Share"). Opportunity = digitizing the
rep/phone/email-entered order flow; eCat AND the client's own web are both valid.
NEVER "grow eCat X%→Y% / each point worth $Z / capture rate / adoption stage."
kal's feed has 100% Unclassified order origin (Q-CHANNEL-MIX DATA NOTE) →
channel-mix table SKIPPED, honest paragraph rendered instead.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Order Channel Mix | CONDITIONAL | MET-with-DATA-NOTE (Q-CHANNEL-MIX 100% Unclassified) → honest paragraph, NO table | YES (paragraph) |
| eCat Footprint | CONDITIONAL | MET (HAS_PORTAL_ORDERS=true, VM45_RENDER=true) | YES |
| eCat Order Trend | MANDATORY (Part A always) | MET; Part B MET (HAS_PORTAL_ORDERS=true) | YES (A+B) |
| Top Buyers & Concentration | MANDATORY (always) | MET; Q-52 enrichment MANDATORY (PORTAL_CUSTOMER_DATA_PRESENT=true, Q-52 has 30 rows) | YES (enriched) |
| Order Type & Workflow | MANDATORY (always) | MET (Q-21 has 6 types incl. Quote) | YES |
| Channel Migration | CONDITIONAL | MET (HAS_CART=true → iPad vs eCat Online split from Q-18/Q-20) | YES |
| Market Commitment Attribution | CONDITIONAL — MANDATORY when met | NOT MET (HAS_COMMITMENT_DATA=false; Q-58/Q-58b absent) | NO |
| Quote Economics | CONDITIONAL | MET (Q-20: 30 quotes ≥10; confirmed orders exist) | YES |
| AOV Spread by Rep | CONDITIONAL | NOT MET (no rep-level eCat AOV; Q-18 is monthly only, Q-56 eCat-per-rep all $0) | NO |
| First-Time Buyer Acquisition | CONDITIONAL | MET (Q-41 spans Mar-2025→Jun-2026, 6+ months) | YES |
| Seasonal Timing | CONDITIONAL | NOT MET (Q-21 has no monthly time series; order-type breakdown only) | NO |
| Competitive Displacement | CONDITIONAL — MANDATORY when met | NOT MET (Q-55: every row ecat_share_change_ppts=0; no total-grew-share-shrank rows) | NO (skip silently) |
| Price Erosion | CONDITIONAL — MANDATORY when met | MET (HAS_PORTAL_ORDERS=true, Q-60 has 20 rows) | YES |

Render order (strength→intelligence→opportunity→risk):
Order Channel Mix → eCat Footprint → eCat Order Trend → Top Buyers → Order Type & Workflow
→ Channel Migration → Quote Economics → First-Time Buyer → Price Erosion.

Section-level what-this-means: YES. Highlights file: YES.

## Computed figures
- eCat sales LTM $2.6M; total business LTM $11.7M (Q-45). eCat footprint = 22.5% of total business (Q-45 ecat_gmv_capture_pct) — shown as factual footprint, NOT a share-to-grow.
- Channel mix: DATA NOTE present (100% Unclassified). eCat shown standalone; non-eCat = "rep- or back-office-entered", NOT manual/offline.
- eCat Order Trend by quarter (Q-18 partA + partB):
  - Q3'25 (Jul–Sep): eCat 35 ord, $440,054; total business $2,756,072; share 16.0%; AOV $12,573
  - Q4'25 (Oct–Dec): eCat 41 ord, $305,316; total business $2,522,787; share 12.1%; AOV $7,447
  - Q1'26 (Jan–Mar): eCat 82 ord, $956,183; total business $3,400,000; share 28.1%; AOV $11,661
  - Q2'26 (Apr–Jun, partial): eCat 14 ord, $587,527; total business $2,558,413; share 23.0%; AOV $41,966 (skewed by one $566K Apr order)
- Top 5 eCat buyers GMV = 152,319+105,057+95,890+90,995+84,489 = $528,750 ≈ 61% of eCat GMV (SIG-RISK-01).
- Q-52 enrichment: FEI Ferguson eCat $95,890 vs total business $652,848 = 14.7% (headroom case). Some buyers have no Q-52 row (→ "—") or eCat>total (timing artifact → cap display).
- Quote AOV $34,333 (30 quotes) vs Confirmed AOV $5,775 (112) → ~5.9x premium (Q-20/Q-21).
- Channel: iPad 164 orders AOV $15,741; eCat Online 33 orders AOV $1,598 (Q-20). 83% iPad / 17% Online by count.
- First-time buyers: Q-41 spans Mar'25–Jun'26; predominantly Rep-Acquired (iPad); eCat Online acquisition rising in 2026.
- Price erosion: 20 accounts QoQ avg unit price decline; FEI Ferguson largest current-qtr GMV $151,967 (−13.5%).
