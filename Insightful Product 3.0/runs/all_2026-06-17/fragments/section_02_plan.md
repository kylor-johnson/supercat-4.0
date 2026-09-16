# Section 02 Build Plan — Account Intelligence

- **Run date**: 2026-06-17
- **Client**: Accord Lighting (all, org_id=223)
- **SECTION_CONFIDENCE_2**: STRONG → template `§2-STRONG`, label `STRONG VIEW`

## Data availability snapshot

| Gate | Value |
|---|---|
| HAS_PORTAL_ORDERS | False |
| PORTAL_CUSTOMER_DATA_PRESENT | False |
| HAS_BUYER_DATA | False |
| HAS_SALES_SECTION | True (engagement mode) |

eCat-originated data is present (Q-12, Q-14, Q-17, Q-40, Q-41). All portal/all-channel
enrichment queries (Q-52, Q-53, Q-54, Q-57, Q-66, Q-67, Q-68) are absent. All org-level
signal queries (Q-ORG-DECAY/NBP/CONTRACTION/VELOCITY/STOCKOUT) returned 0 rows.
`top_accounts.md` signal-density manifest is empty (no rows).

## Pre-Build Gate Check (from guide's gate table)

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has 1 row) | YES |
| 2. Data Confidence Header | MANDATORY | MET (STRONG tier) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET — built from best available per-account data (Q-17 dormant high-value, top by historical eCat GMV) since signal-density manifest is empty | YES |
| 3b. eCat Penetration (Q-52) | MANDATORY when gate met | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=False; Q-52 absent) | NO |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (Q-17 has 12 rows, SIG-RISK-02 style threshold) | YES |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (Q-53 absent; no portal data) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL set) | NO |
| 6. Geographic Distribution (Q-40) | CONDITIONAL | MET — Florida + Puerto Rico together >30% of eCat GMV; non-uniform | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (0 rows) | NO |
| 8. Reorder Velocity & Early Warning (Q-14) | MANDATORY (always) | MET (Q-14 has 1 row → render gracefully) | YES |
| 8b. Deceleration Alert (Q-14b) | MANDATORY when gate met | NOT MET (HAS_PORTAL_ORDERS=False; Q-14b absent) | NO |
| 9. Untapped Category Opportunities (Q-57) | MANDATORY when gate met | NOT MET (both gates False; Q-57 absent) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=False; Q-66 absent) | NO |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY when gate met | NOT MET (both gates False; Q-67 absent) | NO |
| 12. Spending Contraction (Q-68) | MANDATORY when gate met | NOT MET (both gates False; Q-68 absent) | NO |
| Section-level what-this-means | MANDATORY | — | YES |

## Notes on adaptation under thin / eCat-only data

- No all-channel (portal) data, so mini-briefs cannot show all-channel LTM, wallet share,
  companion products, stock-out, or competitive displacement components. Each brief renders
  the mandatory Account Header (eCat figures) + Reorder Pattern (where Q-14 cadence known) +
  Pre-Meeting Priority.
- Engagement Score computed per guide formula using eCat order count, historical eCat GMV,
  recency (days since last order), and trajectory (single-year, treated neutral → mid band).
- Top accounts chosen by historical eCat GMV (the only per-account ranking signal available).
- Geographic Distribution (6) rendered because Florida ($19,554) + Puerto Rico ($18,582)
  = ~46% of the $77,255 eCat GMV total — clear concentration, not uniform.
