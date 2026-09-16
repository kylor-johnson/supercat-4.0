# Section 04 Build Plan — Commerce Patterns

**Client**: Ratana International Ltd. (ril) · Run date 2026-06-17
Confidence tier: SECTION_CONFIDENCE_4 = **STRONG** → template `§4-STRONG`, label "STRONG VIEW".

| Subsection (exact guide name) | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Order Channel Mix | CONDITIONAL (render FIRST) | MET (HAS_PORTAL_ORDERS=true; Q-CHANNEL-MIX has rows, NO DATA NOTE — real eCat vs NAV split) | YES |
| eCat Footprint | CONDITIONAL | MET (HAS_PORTAL_ORDERS=true). REFRAMED: eCat's footprint as a tool (33.8% of $17.29M total business), NOT a share-to-grow. VM45_RENDER=false → standalone volume + data-sync caveat; no capture-rate/adoption-stage framing | YES |
| eCat Order Trend | MANDATORY (Part A always) | MET (Q-18-A 13 months); Part B MET (HAS_PORTAL_ORDERS=true, Q-16/Q-18-B total business) | YES |
| Top Buyers & Concentration | MANDATORY (always) | MET (Q-13 15 rows); Q-52 enrichment MANDATORY (PORTAL_CUSTOMER_DATA_PRESENT=true + Q-52 rows) | YES (enriched) |
| Order Type & Workflow | MANDATORY (always) | MET (Q-21: Quote/Confirmed/Order) | YES |
| Channel Migration | CONDITIONAL | MET (HAS_CART=true → iPad vs eCat Online from Q-18-A/Q-20) | YES |
| Market Commitment Attribution | CONDITIONAL | NOT MET (HAS_COMMITMENT_DATA=false; Q-58/Q-58b absent) | NO (skip silently) |
| Quote Economics | CONDITIONAL | MET (Q-20/Q-21: 1,058 quotes ≥10; Confirmed 169) | YES |
| AOV Spread by Rep | CONDITIONAL | NOT MET (no clean per-rep AOV; Q-56 capture values corrupt >100%/negative — not renderable) | NO (skip silently) |
| First-Time Buyer Acquisition | CONDITIONAL | MET (Q-41 monthly new buyers spanning 15 months; named trajectories via Q-ORG-VELOCITY) | YES |
| Seasonal Timing | CONDITIONAL | MET (13 months of monthly eCat order GMV from Q-16/Q-18 series). Render with realized-order framing; flag partial-month boundaries (Jun 2025, Jun 2026) | YES |
| Competitive Displacement | CONDITIONAL — MANDATORY when gate met | NOT MET (Q-55: only "Uncategorized" meets total↑/share↓ and its values are corrupt — eCat share >100%; other rows are internal CAT codes with ppts ≥ 0. No clean displacement category → skip silently, no false alarm) | NO (skip silently) |
| Price Erosion | CONDITIONAL — MANDATORY when gate met | MET (HAS_PORTAL_ORDERS=true + Q-60 18 clean rows) | YES |

## Render order (narrative arc)
Channel Mix → eCat Footprint → eCat Order Trend → Top Buyers → Order Type & Workflow → Channel Migration → Quote Economics → New Buyer Acquisition → Ordering Seasonality → Product Mix & Pricing Trends → section-level what-this-means.

## Notes
- VM45_RENDER=false but task directs Q-CHANNEL-MIX as honest denominator (eCat ~34% of total business). Q-45's 102.2% capture / $17.6M eCat GMV is a quote-inflated artifact (quotes = $17.1M) — NOT used as a share figure. Section anchors on eCat = $5.84M, 33.8%.
- eCat positioned as ONE channel — the client's main self-service DIGITAL channel (33.8% of total business). The 66.2% NAV/ERP-entered remainder is NOT characterized as manual/offline/phone.
- Q-13/Q-52 eCat GMV is on the ~$6.39M actual-eCat basis (top-5 = $3.07M = 48%, matches SIG-RISK-01). % of eCat GMV computed against $6.39M base.
- §Seasonal rendered from 13-month eCat order GMV series; partial-month boundaries (Jun 2025, Jun 2026) flagged as truncation, not demand. §8 skipped (no clean per-rep AOV). §9 skipped (Q-55/Q-56 corrupt). §11 skipped (no commitment data).
- Channel attribution statement (HAS_CART=true) included: "All eCat orders originate from one of two sources: iPad (rep-submitted) or eCat Online (buyer self-service)."
- Q-60 Part B (category AOV) omitted: Q-39 not in bundle, no category granularity → account-level Part A only.
- Banned: ERP, platform (standalone), portal orders, CAT internal codes, segment labels, peer benchmarks.
