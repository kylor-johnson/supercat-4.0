# Section 02 Build Plan — Account Intelligence

Run: mli (Maxim Lighting), 2026-06-17
Confidence tier: SECTION_CONFIDENCE_2 = **STRONG** (label "STRONG VIEW"; template text falls back to §2-PARTIAL because no portal-order date exists — HAS_PORTAL_ORDERS=false).

## Key gate reality
- HAS_PORTAL_ORDERS = **false** → all portal/total-business subsections gated off.
- PORTAL_CUSTOMER_DATA_PRESENT = **false** → 3b, 9, 11, 12 gated off.
- HAS_BUYER_DATA = **false** → subsection 10 gated off.
- top_accounts.md = **empty** (0 signal-density rows). Mini-briefs built from the only fired account-level signal: SIG-ANOMALY-02 stock-out exposure (Q-ORG-STOCKOUT top_customers), ranked by per-account at-risk revenue.
- Q-ORG-VELOCITY / CONTRACTION / NBP / DECAY = empty → no trajectory, companion, decay, or displacement components available.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 row present) | YES |
| 2. Data Confidence Header | MANDATORY | MET (STRONG; text falls back to PARTIAL template) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET (built from Q-ORG-STOCKOUT account exposure; top_accounts empty) | YES |
| 3b. eCat Penetration (Q-52) | MANDATORY-when-met | NOT MET (Q-52 absent; PORTAL_CUSTOMER_DATA_PRESENT=false) | NO |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (Q-17/Q-17-atrisk rows exist, $15K+/90d+ silent) | YES |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (Q-53 absent) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL set; HAS_CART=false but no exclusion set produced) | NO |
| 6. Geographic Distribution (Q-40) | CONDITIONAL | MET (TX = 56.8% of GMV > 30% concentration) | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (file empty) | NO |
| 8. Reorder Velocity (Q-14) | MANDATORY | MET (Q-14 has 4 rows) | YES |
| 8b. Deceleration Alert (Q-14b) | MANDATORY-when-met | NOT MET (Q-14b absent; HAS_PORTAL_ORDERS=false) | NO |
| 9. Untapped Category Opportunities (Q-57) | MANDATORY-when-met | NOT MET (Q-57 absent; gates false) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (Q-66 absent; HAS_BUYER_DATA=false) | NO |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY-when-met | NOT MET (Q-67 absent; gates false) | NO |
| 12. Spending Contraction (Q-68) | MANDATORY-when-met | NOT MET (Q-68 absent; gates false) | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

## Rendering order (narrative arc)
Header Metrics → Confidence Header → Mini-Briefs (1–5 open, 6–10 collapsed) → Reorder Velocity & Early Warning (§8) → Geographic Distribution (§6) → Dormant High-Value (§4, risk) → Section what-this-means.
