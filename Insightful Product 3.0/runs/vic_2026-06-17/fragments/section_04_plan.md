# Section 04 Build Plan — Commerce Patterns

Client: Vaxcel International Corporation (vic) · Run date: 2026-06-17
Confidence tier (SECTION_CONFIDENCE_4): **STRONG** → template `§4-STRONG`, label `STRONG VIEW`

THESIS = DIGITAL ENABLEMENT, not eCat share. vic is greenfield on eCat (~$28.8K LTM, 94 orders vs $9.5M total business). Frame eCat as ONE tool in the mix and the opportunity as digitizing the rep-/back-office-entered order flow over time. NEVER "grow eCat X%→Y% / each point worth $Z / capture rate / adoption stage." Do NOT make eCat obsolete — always name its specific strength. NEVER call non-eCat orders manual/offline/non-digital.

## Gate inputs
- HAS_PORTAL_ORDERS = True
- HAS_CART = True
- PORTAL_CUSTOMER_DATA_PRESENT = True
- PORTAL_REP_DATA_PRESENT = False
- HAS_COMMITMENT_DATA = False
- HAS_INVENTORY = True
- VM45_RENDER = False (Gate2 FAIL: ecat $28,840 < 5% of erp $9.5M) → eCat standalone, NO eCat-vs-total share computation
- Q-CHANNEL-MIX contains a DATA NOTE (100% Unclassified) → SKIP channel table, render honest paragraph (DATA NOTE path)

| Subsection (exact guide name) | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Data Confidence Header | MANDATORY | MET (STRONG tier; last total-business order 6d ago) | YES |
| 0. Order Channel Mix | CONDITIONAL | MET (HAS_PORTAL_ORDERS) but file has DATA NOTE → render honest paragraph, NO table, NO what-this-means | YES (paragraph) |
| 1. eCat Footprint | CONDITIONAL | MET (HAS_PORTAL_ORDERS). VM45_RENDER=false → standalone eCat volume + enablement framing; NO share-to-grow, NO adoption ladder | YES |
| 2. eCat Order Trend (Part A) | MANDATORY (always) | MET (Q-18-A, 13 months) | YES |
| 2B. eCat Share of Total Trend | CONDITIONAL | NOT MET in practice — VM45_RENDER=false + DATA NOTE; share-to-grow framing banned. Render Part A trend only | NO (Part B skipped) |
| 4. Top Buyers & Concentration | MANDATORY (always) | MET (Q-13, 15 rows) | YES |
| 4+. Top Buyers enrichment (Q-52) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true; Q-52, 30 rows). Join on customer name where present; "—" where buyer not in Q-52 | YES |
| 6. Order Type & Workflow | MANDATORY (always) | MET (Q-21, 1 row: Confirmed 100%). No quotes → lead with dominant workflow pattern, NOT quote premium | YES |
| 3. Channel Migration | CONDITIONAL | MET (HAS_CART; Q-18-A ipad vs online split). eCat split only, NO share-of-total overlay | YES |
| 11. Market Commitment Attribution | CONDITIONAL (MANDATORY when gate met) | NOT MET (HAS_COMMITMENT_DATA=false; Q-58/58b absent) | NO |
| 5. Quote Economics | CONDITIONAL | NOT MET (0 quote orders in Q-20/Q-21; need 10+) | NO |
| 8. AOV Spread by Rep | CONDITIONAL | NOT MET (PORTAL_REP_DATA_PRESENT=false; Q-18 has no rep AOV dimension; engagement mode) | NO |
| 12. First-Time Buyer Acquisition | CONDITIONAL | MET (Q-41 spans 2025-04→2026-03, 9 mo). Aggregates only; name growth via Q-ORG-VELOCITY; flag account-level gap | YES |
| 7. Ordering Seasonality | CONDITIONAL | NOT MET (Q-21 is single aggregate row, no 12-month monthly series) | NO |
| 9. Channel Share Opportunity (Competitive Displacement) | CONDITIONAL (MANDATORY when gate met) | NOT MET (Q-55: every row eCat=$0, ecat_share_change_ppts=0; no total-grew/share-shrank row) | NO (skip silently) |
| 10. Product Mix & Pricing Trends (Price Erosion) | CONDITIONAL (MANDATORY when gate met) | MET (HAS_PORTAL_ORDERS; Q-60, 20 rows). Part B SKIP (no Q-39 category granularity) | YES (Part A only) |

## Key data notes
- §0: DATA NOTE present → honest single paragraph; do NOT characterize non-eCat as manual/offline. No what-this-means (paragraph form).
- §1 eCat Footprint: VM45_RENDER=false → show eCat standalone $28,840 LTM, 94 orders; add the prose line about data synchronization. NO capture-rate %, NO adoption stage, NO "$X per point", NO "grow A%→B%". Opportunity = digitizing rep/phone/email-entered flow; eCat strength = rep-assisted/field/visual selling.
- §2: Part A only (eCat orders / eCat GMV / AOV by month from Q-18-A, chronological). No total-business share column (Part B skipped). Note partial-month boundary artifacts (Jun 2025, Jun 2026).
- §4: Q-13 pct_of_ecat_gmv ≈ percentages; top5 ≈ 57% → concentration callout fires. Enrich with Q-52 Total Business + eCat Share; most Q-13 buyers absent from Q-52 → "—" (do NOT fabricate). C00989 CED overlaps ($760 eCat / $25,116 total = 3%).
- §6: only Confirmed (100%). No quote premium possible → lead with dominant-workflow framing (all eCat orders flow straight to confirmed; no quote/HFC governance layer in use yet).
- §3: 1 iPad order LTM vs 93 eCat Online → essentially 100% self-service today. Channel attribution statement required (HAS_CART=true).
- §12: Q-41 aggregates only (~1/month, 9 mo). Name growth accounts from Q-ORG-VELOCITY (Orgill $226K peak qtr, Target Plus accelerating). State account-level first-order dates would strengthen.
- §10: account-level only (Part B omitted — no Q-39). Framing = total business / all-channel, investigative, multi-causal, measured. .callout.insight (NOT .callout.warn).
- Banned: ERP, health score, segment labels, "portal orders", standalone "platform", "capture rate", "digital ordering share"/"adoption stage"/"each point worth $X"/"grow eCat A%→B%".

## Render order (narrative arc: context → strength → intelligence → opportunity → risk)
Header → Confidence → 0 Order Channel Mix (context, paragraph) → 1 eCat Footprint (context) →
2 eCat Order Trend (strength) → 4 Top Buyers + enrichment (intelligence) → 6 Order Type & Workflow (intelligence) →
3 Channel Migration (intelligence) → 12 First-Time Buyer Acquisition (intelligence) → 10 Product Mix & Pricing Trends (risk, last) → section what-this-means.
