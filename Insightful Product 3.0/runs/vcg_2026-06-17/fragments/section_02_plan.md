# Section 02 Build Plan — Account Intelligence

**Client:** Visual Comfort Signature (vcg) · Run date: 2026-06-17
**Confidence tier (SECTION_CONFIDENCE_2):** STRONG

## Gate inputs
- HAS_PORTAL_ORDERS = **False**
- PORTAL_CUSTOMER_DATA_PRESENT = **False**
- HAS_BUYER_DATA = **False**
- HAS_SALES_DATA = True · HAS_INVENTORY = True

## Pre-Build Gate Check

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has 1 row) | YES |
| 2. Data Confidence Header | MANDATORY | MET (tier=STRONG) | YES |
| 3. Top 10 Mini-Briefs (top_accounts) | MANDATORY | MET (10 accounts) | YES |
| 3b. eCat Penetration (Q-52) | CONDITIONAL | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false; Q-52 absent) | NO |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (Q-17/Q-17-atrisk have 25/20 rows, $39K–$74K) | YES |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (Q-53 absent; no portal data) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL set; HAS_PORTAL_ORDERS=false) | NO |
| 6. Geographic Distribution (Q-40) | CONDITIONAL | NOT MET (top state TX=18.1% < 30%; no single-state cluster) | NO |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (Q-ORG-CONTRACTION absent) | NO |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (Q-14 has 20 rows) | YES |
| 8b. Deceleration Alert (Q-14b) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=false; Q-14b absent) | NO |
| 9. Untapped Category Opportunities (Q-57) | CONDITIONAL | NOT MET (both portal gates false; Q-57 absent) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=false; Q-66 absent) | NO |
| 11. Geographic Revenue Trends (Q-67) | CONDITIONAL | NOT MET (both portal gates false; Q-67 absent) | NO |
| 12. Spending Contraction (Q-68) | CONDITIONAL | NOT MET (both portal gates false; Q-68 absent) | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

## Rendered subsections (final)
1. Header Metrics
2. Data Confidence Header (STRONG)
3. Top 10 Mini-Briefs (5 standalone + 6–10 collapsed)
4. Reorder Velocity & Early Warning
5. Dormant High-Value Accounts
6. Section-level what-this-means

## Notes
- Every mini-brief account fired SIG-DECAY-01 (Q-ORG-DECAY). Reorder Pattern Change
  callout (`.callout.insight`) renders on each, framed as early warning.
- No YoY data available (no Q-ORG-VELOCITY/CONTRACTION) → omit YoY metric-notes;
  use Engagement Score + decay framing instead.
- Spending Trajectory, Companion Products, Wallet Position, Stock-Out, Competitive
  Displacement components skipped per gate (no velocity/NBP/portal data; stockout
  rows have no per-account revenue and only internal showroom customers).
- Engagement scores computed against org 90th pctiles (orders≈20, GMV≈$52.6K).
