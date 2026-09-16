# Section 02 Build Plan — Account Intelligence

**Client:** Capital Lighting Fixture Co. (clc, org_id 40) · **Run:** 2026-06-17
**Section confidence (SECTION_CONFIDENCE_2):** STRONG → template `§2-STRONG`, label **STRONG VIEW**

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Header Metrics (Q-12) | MANDATORY (always) | MET (Q-12 has 1 row: 3,239 accounts, 245 active 12mo) | YES |
| Data Confidence Header | MANDATORY (always) | MET (SECTION_CONFIDENCE_2 = STRONG) | YES |
| Top 10 Accounts by Signal Density (mini-briefs) | MANDATORY (always) | MET (top_accounts.md has 10 rows) | YES |
| eCat Penetration of Total Business (3b, Q-52) | MANDATORY when gate met | MET (PORTAL_CUSTOMER_DATA_PRESENT=true; Q-52 has 30 rows) | YES |
| Dormant High-Value Accounts (4, Q-17) | CONDITIONAL (SIG-RISK-02) | MET (Q-17-atrisk has 20 rows, $9.7K–$31.8K) | YES |
| Unactivated High-Value Accounts (5, Q-53) | CONDITIONAL (SIG-OPP-02) | MET (Q-53 has 20 rows, $29.4M total business) | YES |
| Enterprise Channel Accounts (5b) | CONDITIONAL (ENTERPRISE_CHANNEL set non-empty) | NOT MET (SIG-OPP-02 folds all 20 into activation set; no separate enterprise set) | NO |
| Geographic Distribution (6, Q-40) | CONDITIONAL (non-uniform >30%) | NOT MET (no single state >30%; covered by 3b + 11) | NO |
| Velocity Deceleration / Accounts Contracting YoY (7, Q-ORG-CONTRACTION) | CONDITIONAL (SIG-DECAY-04) | MET (25 rows; 14 accounts >20% decline & LTM>$50K) | YES |
| Reorder Velocity & Early Warning (8, Q-14/Q-14b) | MANDATORY (always; 8b mandatory when gate met) | MET via 8b (Q-14 empty; Q-14b has 15 rows, HAS_PORTAL_ORDERS=true) | YES |
| Untapped Category Opportunities (9, Q-57) | MANDATORY when gate met | NOT MET (Q-57 row count = 0, no data) | NO |
| Buyer-Within-Account Intelligence (10, Q-66) | CONDITIONAL (HAS_PORTAL_ORDERS + HAS_BUYER_DATA) | MET (both true; Q-66 has 20 rows) | YES |
| Geographic Revenue Trends (11, Q-67) | MANDATORY when gate met | MET (HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT true; Q-67 has 25 rows) | YES |
| Spending Contraction Detection (12, Q-68) | MANDATORY when gate met `[COLLAPSE]` | MET (both gates true; Q-68 has 20 rows, $1.55M gap-to-peak) | YES |
| Section-Level What-This-Means | MANDATORY | MET | YES |

## Notes
- **Q-14 empty:** subsection 8 renders via the MANDATORY 8b Deceleration Alert (Q-14b). The Q-14 high-frequency table is skipped (no data rows) per thin-data rule.
- **Mini-briefs are contraction-heavy:** 8 of 10 top-density accounts fired DECAY-04; Dulles + Echo also fired MOM-01 (recent-quarter rebound). Lead each with positives where present; section positives carried by 3b, 11, 10, 5.
- **Competitive hypotheses** (>25% decline + LTM>$50K) rendered for Shades of Light (mini-brief 3) and Legend Lighting (subsection 7) per Shared Rules §M.
- **Forms:** match TARGET STRUCTURE — `.metrics`/`.metric`/`.metric-label`/`.metric-value`/`.metric-note`, `.sub-label`, `.prose`, `.callout`. Engagement-score badge omitted (not in gold form). Tables get `<thead>`/`<tbody>`, top-5 `row-highlight` + bold names, remainder in `<details>`.
