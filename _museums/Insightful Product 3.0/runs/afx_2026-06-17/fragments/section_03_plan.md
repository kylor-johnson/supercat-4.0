# Section 03 Build Plan — Product Intelligence

**Client:** AFX, Inc. (afx, org_id=185) · Run date 2026-06-17
**Section confidence (SECTION_CONFIDENCE_3):** PARTIAL → `§3-PARTIAL` / "PARTIAL VIEW"

**Key gate flags:** HAS_PORTAL_ORDERS=False · HAS_SALES_DATA=False · HAS_INVENTORY=True · HAS_NEW_ITEMS=True

**Cache data availability:** Only `Q-07_results.md` has data rows. Q-37, Q-38a, Q-39 (category/collection), Q-42, Q-59, Q-61, Q-ORG-GHOST, Q-ORG-STOCKOUT, Q-ORG-NEWITEM are all "(not present)".

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY (when gate met) | NOT MET (HAS_PORTAL_ORDERS=False; Q-59 not present) | NO |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST not present; SIG-ANOMALY-01 did not fire) | NO |
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | NOT MET (HAS_SALES_DATA=False; Q-37 not present) | NO |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | NOT MET (Q-ORG-STOCKOUT not present; SIG-ANOMALY-02 did not fire) | NO |
| 5. Item Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-38a not present) | NO |
| 6. New Introduction Performance & Adoption (Q-42/Q-61/Q-ORG-NEWITEM) | MANDATORY Part B (when gate met) | NOT MET (Part A HAS_SALES_DATA=False; Part B HAS_PORTAL_ORDERS=False, Q-61 not present) | NO |
| 7. What's Selling — Category & Collection (Q-39) | CONDITIONAL | NOT MET (HAS_SALES_DATA=False; Q-39 files not present) | NO |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (always; Q-07 has 2 data rows) | YES |

**Confidence header:** MANDATORY — rendered at top with PARTIAL VIEW tier.
**Section-level what-this-means:** MANDATORY — rendered.

**Render summary:** 1 subsection (Catalog Completeness). Order/inventory-movement history absent this cycle, so all sales- and order-dependent product views are correctly skipped.
