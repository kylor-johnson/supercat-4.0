# Section 02 Build Plan — Account Intelligence

**Client:** Dainolite Ltd. (da) · Run date 2026-06-17 · Confidence tier: **STRONG** (SECTION_CONFIDENCE_2)

## Gate snapshot (from gate_flags.md)

| Gate | Value | Effect |
|---|---|---|
| HAS_PORTAL_ORDERS | False | Subsections 8b, 9, 11, 12 OMIT |
| PORTAL_CUSTOMER_DATA_PRESENT | False | Subsections 3b, 9, 11, 12 OMIT |
| HAS_BUYER_DATA | False | Subsection 10 OMIT |
| HAS_SALES_DATA | True | eCat account data available |

## Pre-Build Gate Check (mandatory-when-met table)

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 3b eCat Penetration (Q-52) | MANDATORY-when-met | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false; file absent) | NO |
| 8b Deceleration Alert (Q-14b) | MANDATORY-when-met | NOT MET (HAS_PORTAL_ORDERS=false; file absent) | NO |
| 9 Untapped Category (Q-57) | MANDATORY-when-met | NOT MET (both gates false; file absent) | NO |
| 11 Geographic Revenue Trends (Q-67) | MANDATORY-when-met | NOT MET (both gates false; file absent) | NO |
| 12 Spending Contraction (Q-68) | MANDATORY-when-met | NOT MET (both gates false; file absent) | NO |

## Content blocks — render decision

| # | Subsection | Source | Status | Render |
|---|---|---|---|---|
| 1 | Header Metrics | Q-12 | Always | YES |
| 2 | Data Confidence Header | section_confidence (STRONG) | Always | YES |
| 3 | Top 10 Mini-Briefs | Q-14 (ranked by eCat GMV; top_accounts.md empty) | Always | YES (5 full + 6–10 collapsed) |
| 3b | eCat Penetration | Q-52 | gate false / absent | NO |
| 4 | Dormant High-Value | Q-17 / Q-17-atrisk | SIG-RISK-02 rows exist | YES |
| 5 | Unactivated High-Value | Q-53 | absent | NO |
| 5b | Enterprise Channel Accounts | signal pass | exclusion set empty | NO |
| 6 | Geographic Distribution | Q-40 | QC+ON >30%, concentrated | YES |
| 7 | Velocity Deceleration | Q-ORG-CONTRACTION | 0 rows | NO |
| 8 | Reorder Velocity & Early Warning | Q-14 | Always | YES |
| 8b | Deceleration Alert | Q-14b | absent | NO |
| 9 | Untapped Category | Q-57 | absent | NO |
| 10 | Buyer-Within-Account | Q-66 | gate false / absent | NO |
| 11 | Geographic Revenue Trends | Q-67 | gate false / absent | NO |
| 12 | Spending Contraction | Q-68 | gate false / absent | NO |
| — | Section-level what-this-means | — | Mandatory | YES |

## Notes on data adaptation
- `top_accounts.md` contains zero signal-density rows, and the Q-ORG-* signal queries (DECAY/CONTRACTION/VELOCITY/NBP) all returned 0 rows or are absent. Mini-briefs are therefore built from Q-14 reorder data ranked by eCat GMV (the strongest account-level signal present). No all-channel, city/state, YoY, or category data exists per account, so mini-briefs render the eCat metrics actually available (eCat LTM revenue, eCat orders, reorder velocity, last order) and a Pre-Meeting Priority. Spending Trajectory / Companion / Decay / Stock-Out / Displacement components are skipped silently (their signals did not fire).
- Stock-Out (Q-ORG-STOCKOUT) has data but no per-account revenue (all None) and no item LTM revenue, so it does not support the account-mapped Stock-Out Impact component.
- Engagement Score: org 90th-pctile order count ≈ 144 (top of Q-14); 90th-pctile GMV ≈ $168K. Scored per the guide's 4-dimension rubric.
