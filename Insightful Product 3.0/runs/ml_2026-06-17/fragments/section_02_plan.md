# Section 02 Build Plan — Account Intelligence

Client: Millennium Lighting (ml), run 2026-06-17.
Confidence tier (`SECTION_CONFIDENCE_2`): **STRONG** → but `{{LAST_PORTAL_ORDER_DATE}}`
is unresolvable (HAS_PORTAL_ORDERS=false), so per guide §2 fallback rule the
confidence header uses the `§2-PARTIAL` template / `PARTIAL VIEW` label.

## Key gate values

| Gate | Value |
|---|---|
| HAS_PORTAL_ORDERS | False |
| PORTAL_CUSTOMER_DATA_PRESENT | False |
| HAS_BUYER_DATA | False |
| HAS_INVENTORY | True |

## Data availability

| Source | Rows | Note |
|---|---|---|
| Q-12 | 1 | total_erp=0, ever_ecat=3, active_12mo=3, active_6mo=1, active_3mo=0 |
| top_accounts.md | 0 | EMPTY — no account passed signal-density selection |
| Q-14 | 0 | no reorder-frequency rows |
| Q-17 / Q-17-atrisk | 0 | no dormant accounts |
| Q-40 | 0 | no geographic rows |
| Q-41 / Q-41-rep | 2 | acquisition: 3 first-time eCat buyers (Kelly Casagrande 2, Doug Dupwe 1) |
| Q-ORG-DECAY | 0 | no decay rows |
| Q-52/53/54/57/66/67/68 | absent | portal enrichment not present |
| Q-ORG-NBP/CONTRACTION/VELOCITY/STOCKOUT | absent | not present |

## Subsection decisions

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 row present) | YES |
| 2. Data Confidence Header | MANDATORY | MET (tier STRONG → PARTIAL template, no portal date) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | source EMPTY — top_accounts.md has 0 rows; no account data to brief | NO (render honest gap note in place) |
| 3b. eCat Penetration (Q-52) | CONDITIONAL/MANDATORY-when-met | NOT MET (PORTAL_CUSTOMER_DATA_PRESENT=false; file absent) | NO |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | NOT MET (Q-17 = 0 rows) | NO |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (file absent) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL set) | NO |
| 6. Geographic Distribution (Q-40) | CONDITIONAL | NOT MET (Q-40 = 0 rows) | NO |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (file absent) | NO |
| 8. Reorder Velocity (Q-14) | MANDATORY | source EMPTY (Q-14 = 0 rows) | NO (render honest gap note) |
| 8b. Deceleration Alert (Q-14b) | MANDATORY-when-met | NOT MET (HAS_PORTAL_ORDERS=false; file absent) | NO |
| 9. Untapped Category Opps (Q-57) | MANDATORY-when-met | NOT MET (gates false; file absent) | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=false; file absent) | NO |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY-when-met | NOT MET (gates false; file absent) | NO |
| 12. Spending Contraction (Q-68) | MANDATORY-when-met | NOT MET (gates false; file absent) | NO |
| Section-level what-this-means | MANDATORY | MET | YES |

## Build note

This is a thin-data section: only Q-12 (account counts) and Q-41 (new-buyer
acquisition) carry rows. The mandatory mini-brief and reorder-velocity sources
are EMPTY, so per the "Handle thin data gracefully" rule those subsections
render as honest gap statements rather than fabricated tables. No portal/ERP
enrichment is present, so every portal-gated subsection (3b, 8b, 9, 10, 11, 12)
is correctly skipped. The section leads with the genuine positive signal: 3
first-time eCat buyers were acquired in the trailing year, all rep-driven on iPad.
