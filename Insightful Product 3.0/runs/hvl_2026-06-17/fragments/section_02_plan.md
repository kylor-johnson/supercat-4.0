# Section 02 Build Plan — Account Intelligence

**Client**: Hudson Valley Lighting (hvl) | **Run date**: 2026-06-17
**Section confidence (SECTION_CONFIDENCE_2)**: STRONG → label "STRONG VIEW"
**Mode**: engagement (no portal orders). HAS_PORTAL_ORDERS=False, PORTAL_CUSTOMER_DATA_PRESENT=False, PORTAL_REP_DATA_PRESENT=False.

## Pre-Build Gate Check

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has 1 row: 2,289 total customers, 354 ever-ordered eCat) | YES |
| 2. Data Confidence Header | MANDATORY | MET (SECTION_CONFIDENCE_2=STRONG) | YES |
| 3. Top 10 Mini-Briefs (top_accounts.md) | MANDATORY | MET-but-EMPTY (top_accounts.md has 0 data rows; all per-account queries Q-ORG-VELOCITY/CONTRACTION/DECAY/NBP absent or 0 rows) | YES (empty-state note — no account rows available) |
| 3b. eCat Penetration (Q-52) | CONDITIONAL | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=False; Q-52 absent) | NO |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | NOT MET (Q-17 = 0 rows; no SIG-RISK-02) | NO |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (Q-53 absent; no SIG-OPP-02) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL exclusion set) | NO |
| 6. Geographic Distribution (Q-40/Q-54) | CONDITIONAL | NOT MET (Q-40 = 0 rows; Q-54 absent) | NO |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (Q-ORG-CONTRACTION absent; no SIG-DECAY-04) | NO |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY | MET-but-EMPTY (Q-14 = 0 rows; Q-14b absent) | NO (no data rows — gap noted in confidence header) |
| 8b. Deceleration Alert (Q-14b) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-14b absent) | NO |
| 9. Untapped Category Opportunities (Q-57) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False, PORTAL_CUSTOMER_DATA_PRESENT=False; Q-57 absent) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=False; Q-66 absent) | NO |
| 11. Geographic Revenue Trends (Q-67) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-67 absent) | NO |
| 12. Spending Contraction (Q-68) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-68 absent) | NO |

## Data Reality

- Q-12 is the only populated account-level query with usable figures (2,289 total customers; 354 ever-ordered via eCat; active_12mo/6mo/3mo all = 0).
- top_accounts.md returned **0 rows** → no mini-brief content exists. Render subsection 3 scaffold with an honest empty-state callout rather than fabricating accounts.
- Q-14 reorder = 0 rows → subsection 8 has no data; gap folded into confidence header (per Data Presentation "handle thin data gracefully").
- Q-ORG-STOCKOUT has 20 rows but every revenue/qty/customer-revenue field is null and there are no mini-briefs to attach the Stock-Out Impact component to → not rendered (broken/empty data per Data Presentation Rules).
- All portal-dependent subsections skipped (org has no portal orders, no portal customer data).

## Notes
- Confidence header uses §2-STRONG template, "STRONG VIEW" label. ACCOUNT_COUNT resolved = 2,289; LAST_PORTAL_ORDER_DATE unresolvable (no portal orders) → STRONG template falls back to §2-PARTIAL wording per guide ("If LAST_PORTAL_ORDER_DATE cannot be resolved for FULL or STRONG, fall back to §2-PARTIAL"). Keep STRONG VIEW label, use PARTIAL-body wording reflecting all-channel coverage without portal-order date.
- Section-level what-this-means renders (mandatory).
