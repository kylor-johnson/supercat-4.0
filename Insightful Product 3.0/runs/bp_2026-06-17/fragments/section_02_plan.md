# Section 02 Build Plan — Account Intelligence

Client: Buster & Punch (bp, org_id 250) · Run date 2026-06-17
Section confidence (SECTION_CONFIDENCE_2): **STRONG** → renders as **Partial View**
(§2-PARTIAL template) per portal fallback: HAS_PORTAL_ORDERS=false, so
{{LAST_PORTAL_ORDER_DATE}} cannot resolve → fall back to §2-PARTIAL.

## Gate inputs
- HAS_PORTAL_ORDERS = False
- PORTAL_CUSTOMER_DATA_PRESENT = False
- HAS_BUYER_DATA = False
- HAS_INVENTORY = True
- SALES_SECTION_MODE = engagement
- top_accounts.md = 0 rows (no signal-density accounts; signals fired are §4/§5/§6 only)

## Subsection manifest

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 present, 1 row) | YES |
| 2. Data Confidence Header | MANDATORY | MET (STRONG tier → Partial View via portal fallback) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET — top_accounts.md empty, so briefs built from available eCat account data (Q-14, Q-17, Q-40); thin-data: render top eCat accounts | YES |
| 3b. eCat Penetration (Q-52) | CONDITIONAL (mand. when gate met) | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false; Q-52 absent) | NO |
| 4. Dormant High-Value Accounts (Q-17) | CONDITIONAL | MET (Q-17 has 2 rows) | YES |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (Q-53 absent) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL set) | NO |
| 6. Geographic Distribution (Q-40) | CONDITIONAL | MET (UT $39,998 = ~59% of eCat GMV > 30% concentration) | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (file absent) | NO |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET (Q-14 has 1 row — thin; render as inline stat per thin-data rule) | YES |
| 8b. Deceleration Alert (Q-14b) | CONDITIONAL (mand. when gate met) | NOT MET (HAS_PORTAL_ORDERS=false; Q-14b absent) | NO |
| 9. Untapped Category Opportunities (Q-57) | CONDITIONAL (mand. when gate met) | NOT MET (gates false; Q-57 absent) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=false; Q-66 absent) | NO |
| 11. Geographic Revenue Trends (Q-67) | CONDITIONAL (mand. when gate met) | NOT MET (gates false; Q-67 absent) | NO |
| 12. Spending Contraction (Q-68) | CONDITIONAL (mand. when gate met) | NOT MET (gates false; Q-68 absent) | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

## Notes
- This is an early-adoption / engagement-mode org: only 20 customers have ever
  ordered through eCat; 8 active in 12mo. No all-channel (portal) data, so every
  portal-gated subsection (3b/8b/9/10/11/12) is correctly skipped.
- Mini-briefs are built from the accounts we can actually see ordering through
  eCat (Q-14 + Q-40 + Q-17). No companion/decay/stockout/displacement signals
  fired (all Q-ORG-* files empty), so those mini-brief components are omitted.
- Engagement Score computed from Recency/Frequency/Monetary/Trajectory per guide;
  Trajectory uses 15 (0–20% bucket) where no YoY data exists (first-year accounts).
