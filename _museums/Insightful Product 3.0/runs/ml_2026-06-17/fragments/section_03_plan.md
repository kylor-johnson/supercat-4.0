# Section 03 Build Plan — Product Intelligence

**Client:** Millennium Lighting (ml) · **Run date:** 2026-06-17
**Confidence tier (SECTION_CONFIDENCE_3):** PARTIAL → template `§3-PARTIAL` (label "PARTIAL VIEW")

**Key gates:** HAS_PORTAL_ORDERS=False · HAS_SALES_DATA=False · HAS_INVENTORY=True · HAS_NEW_ITEMS=True
**Cache data present:** Q-07 only (1 row). All other Q-files (not present).

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Fill Rate & Revenue Impact (Q-59) | MANDATORY (when gate met) | NOT MET (HAS_PORTAL_ORDERS=False; Q-59 not present) | NO |
| 2. Ghost SKU Registry (Q-ORG-GHOST) | CONDITIONAL | NOT MET (Q-ORG-GHOST not present) | NO |
| 3. Top Sellers & Inventory Position (Q-37) | CONDITIONAL | NOT MET (HAS_SALES_DATA=False; Q-37 not present) | NO |
| 4. Stock-Out Impact Board (Q-ORG-STOCKOUT) | CONDITIONAL | NOT MET (Q-ORG-STOCKOUT not present) | NO |
| 5. Velocity Signals (Q-38a) | CONDITIONAL | NOT MET (HAS_PORTAL_ORDERS=False; Q-38a not present) | NO |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61) | MANDATORY (Part B when gate met) | NOT MET (HAS_SALES_DATA=False; HAS_PORTAL_ORDERS=False; Q-42/Q-61 not present) | NO |
| 7. What's Selling — Category & Collection (Q-39) | CONDITIONAL | NOT MET (HAS_SALES_DATA=False; Q-39 files not present) | NO |
| 8. Catalog Completeness (Q-07) | MANDATORY | MET (always; Q-07 has 1 data row, 80.50% complete) | YES |

**Confidence header:** MANDATORY — rendered at top (PARTIAL VIEW).
**Section-level what-this-means:** MANDATORY — rendered after subsections.

**Notes:** With sales and all-channel order data absent, every demand/inventory-driven subsection (Top Sellers, Velocity, Stock-Out, Fill Rate, New Introduction, Category breakdown) is correctly skipped. Catalog Completeness is the only data-backed subsection. Completeness 80.50% (< 90%) → alert callout fires. Per §8 cross-reference rule, operational remediation deferred to Platform Health Check.
