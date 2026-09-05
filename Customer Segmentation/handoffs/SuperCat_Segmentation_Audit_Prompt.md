# AUDIT PROMPT: SuperCat Customer Segmentation Model

## Your Role

You are an independent analyst auditing a customer segmentation framework for SuperCat Solutions, a B2B SaaS company with $1.95M ARR across 110 active accounts. This segmentation will drive pricing decisions, CS resource allocation, product roadmap prioritization, and expansion strategy. It is the single most consequential strategic artifact the company has produced. Your job is to find every hole, every unfounded leap, every place where the data says one thing and the conclusion says another.

Be ruthless. Be specific. Cite data to contradict claims where you can. This is not a "looks good, minor suggestions" exercise — this is "find everything that's wrong, uncertain, or unfounded before we make million-dollar decisions based on it."

---

## Context: What SuperCat Is

SuperCat Solutions sells to furniture and lighting manufacturers. The core product is **eCat iPad** — an offline-capable rep app that field sales reps carry to showrooms, dealer visits, and trade shows to present products, check pricing/inventory, generate PDFs, and (sometimes) submit orders. Secondary products: **eCat Online (eOL)** — a buyer-facing portal for self-service ordering, and a **Sales Portal / Admin Console**.

**Critical context about commerce flow:**
- Almost NO orders flow straight from the iPad app into the customer's ERP
- The typical flow: rep uses iPad to present/quote → sends order to HQ → HQ audits → keys into ERP
- Real commerce happens via EDI (Wayfair, Amazon, Ferguson), phone/email, their own eCommerce sites, and manual ERP entry
- eCat is a **selling tool upstream of commerce**, not a transaction system for most customers
- Therefore, eCat order volume is a distorted measure of platform value — login frequency and feature usage are more reliable signals

**Pricing tiers:**
- T1 — Catalog Essentials ($749/mo, 10 users)
- T2 — Commerce Professional ($1,295/mo, 15 users)
- T3 — Commerce Enterprise ($2,295/mo, 40 users)
- Additional users: $25/user (1–10 excess), $22 (11–25), $20 (26–50), $18 (51+)

---

## The Segmentation Model Being Audited

The attached report (`SuperCat_Customer_Segmentation_CEO_Brief.md` in Downloads) proposes a four-segment model based on **price point × selling motion**:

1. **Showroom Sellers** (~30 orgs): High price ($250–$2,100/unit), relationship-driven distribution to thousands of showrooms/designers/dealers. eCat = primary selling surface. Core ICP.

2. **Collection Presenters** (~20 orgs): Mid-to-high price ($150–$600/unit), mixed distribution — some revenue through traditional dealer reps, some through marketplace/EDI (Wayfair, Pottery Barn). eCat valuable for dealer side only.

3. **Volume Distributors** (~10 orgs): Lower price ($30–$150/unit), selling to regional chains and institutions. eCat = territory management for non-EDI accounts.

4. **Commodity Feeders** (~8 orgs): Lowest price ($3–$30/unit), selling to mass retail (TJX, Walmart, Amazon, Ross). eCat = internal catalog reference and small-account fringe.

**Key claims:**
- Price point predicts eCat value per account better than any other variable
- Revenue concentration (top 10 buyer % of total) correlates inversely with eCat value
- eOL expansion opportunity follows the price spectrum (highest for Showroom Sellers, minimal for Commodity Feeders)
- Accounts previously seen as "underperforming" (high logins, low eCat orders) are actually Showroom Sellers using the tool correctly — they just order through other channels
- The ~26 "zero order" accounts are not all dormant — many are catalog-only users in a valid use case

---

## Data Sources Available to You

You have access to:

1. **Postgres (`user-supercat-postgres-vpn` MCP)** — Live production database:
   - `sales_data` — ERP invoice records: org, bill_to_code, base_item_code, amount_invoiced, quantity_invoiced, amount_on_order. Available for ~67 orgs.
   - `products` — Full product catalog per org: item_number, net_price, collection_codes, category_codes, trade_name_code, deleted flag
   - `customers` — Buyer records per org: code, name, territory_codes, default_price_code, billing address
   - `login_events` — Every iPad login: org, user, timestamp, device model
   - `organizations` — Org config: shortname, name, feature flags, billing_organization_id
   - `orders` — Orders submitted through eCat: org, customer, items, timestamps
   - `org_users` — User records with roles

2. **BigQuery (`user-bigquery-admin` MCP)** — Analytics warehouse:
   - `insightful_product.org_master_with_segments` — Mixpanel behavioral data per org: total_logins, search_products, select_a_customer, mp_submit_order, order_configured_item, create_pdf_catalog, view_library_entry, scan_item_with_camera, access_sales_portal, segment classification, ARR, feature_depth
   - `insightful_product.segment_classifier` — Segment assignment rules
   - `hubspot.*` — HubSpot CRM data
   - `mixpanel.*` — Raw event data
   - `stripe.*` — Billing data

3. **CSV (in Downloads):** `Copy of Customer & Prospect TAM enriched - Customers.csv` — 110 accounts with usage metrics, feature flags, and external enrichment (Product Type, How They Sell, Who They Sell To, Has Dealer Network, Has eCommerce, Channel Count, Est. Revenue, etc.)

---

## What to Audit

### A. DATA VALIDITY

1. **Sales_data time range:** The report doesn't know if the ERP data is lifetime, last year, or last 3 years. Query the data — look for date fields or timestamp patterns. If it's lifetime, the "total invoiced" numbers are misleading for current revenue. If it's recent, they're gold.

2. **Price calculation methodology:** The report computes avg_unit_price as `SUM(amount_invoiced) / SUM(quantity_invoiced)`. Challenge this — are there orgs where quantity_invoiced is unreliable (bulk shipments counted as 1 unit? Set pricing where qty=1 but amount is for a room full of furniture?). Look for outliers where this calculation breaks.

3. **Sales_data coverage bias:** Only 67 of 110 orgs have sales_data. Are the missing 43 randomly distributed across segments, or are they systematically concentrated in one segment (which would mean that segment's characterization is based on inference, not data)?

4. **Mixpanel behavioral data:** The BigQuery segments (Platform-Embedded, Commerce-Active, Catalog-Focused) are referenced but not validated. Do they actually align with the price-based segments? Or are there contradictions (e.g., Commodity Feeders that are "Platform-Embedded" or Showroom Sellers that are "Catalog-Focused")?

### B. SEGMENTATION LOGIC

5. **Boundary challenges:** The report draws lines at $250, $150, $30. Are these thresholds justified by natural breaks in the data, or arbitrary? Look at the actual distribution of avg_unit_price — is it bimodal? Trimodal? Or a smooth continuum where any threshold is debatable?

6. **Segment assignment ambiguity:** Which orgs fall between segments? Is Braxton Culler ($482, concentrated at 884 buyers) really a "Collection Presenter" or a "Showroom Seller"? Is Savoy House ($59/unit, $93M revenue, 1,214 buyers) really a "Volume Distributor" when they might behave more like a Showroom Seller in practice?

7. **The "selling motion" inference:** The report infers selling motion from buyer names and concentration. But does HIGH LOGIN activity in Postgres/Mixpanel actually correlate with the "Showroom Seller" segment? Or are some Commodity Feeders also logging in heavily (which would break the thesis)?

8. **Missing accounts:** 110 accounts in the CSV. 67 with sales_data. The segments only add up to ~68 orgs (30+20+10+8). What about the other 42? Are they unclassifiable? Do they collapse the framework?

### C. STRATEGIC CLAIMS

9. **"Price point predicts eCat value better than any other variable":** Test this. Run the correlation: does avg_unit_price correlate with login_events/90d, mp_total_logins, or ARR better than alternatives (total_buyers, revenue concentration, total_products)?

10. **"eOL opportunity follows price spectrum":** Check the actual eOL adoption data. Do the 28 orgs with eOL orders cluster in the Showroom Seller segment as predicted? Or is eOL adoption driven by something else entirely (cohort year, org size, CSM assignment)?

11. **"Commodity Feeders get less value":** But some pay high ARR (Home Essentials = $8.8K ARR, Kennedy Intl = $16.6K ARR with 19 billable users). If they're getting "less value," why are they still paying? Is there a retention signal that contradicts the "low value" claim?

12. **Pricing implication validity:** The report implies Showroom Sellers are "underpaying" and Commodity Feeders are "appropriately priced." But ARR is seat-based — a 100-user Showroom Seller pays $20K+ in overage alone. Is the value-vs-price gap actually real, or is the seat model already capturing it?

### D. WHAT'S MISSING

13. **Churn prediction:** Does this segmentation actually predict churn? Look at any historical churn data (orgs that disappeared, billing cancellations) — did churned accounts cluster in specific segments?

14. **Growth trajectory:** The model is static — it describes what accounts ARE. It doesn't address which Commodity Feeders might evolve into Collection Presenters (new product lines at higher prices), or which Showroom Sellers are declining.

15. **Vertical conflation:** "Lighting" and "Furniture" are treated as variants within segments rather than primary axes. But do lighting companies and furniture companies at the same price point actually have the same selling motion? Test this with data.

16. **Account relationships:** Several orgs are clearly related (Visual Comfort has 5+ orgs, Summer Classics has 2, Theodore Alexander has 3). The segmentation treats them as independent. Should portfolio brands be analyzed differently?

---

## Output Format

Structure your audit as:

1. **VERDICT** — In 2–3 sentences, is this segmentation model directionally correct and usable, or fundamentally flawed?

2. **CONFIRMED** — Which claims held up under data scrutiny? (With evidence)

3. **CONTRADICTED** — Which claims the data actively disproves? (With specific counter-evidence)

4. **UNSUPPORTED** — Which claims sound plausible but aren't proven by available data? (Distinguish "unproven" from "wrong")

5. **GAPS** — What critical questions can't be answered with current data?

6. **RECOMMENDED REVISIONS** — If you were rebuilding this from scratch with the same data, what would you change about the model?

---

## Approach

- Query the databases directly. Don't trust summaries — verify numbers.
- Cross-reference sources. If the report says Currey & Company has 11,008 buyers, confirm it.
- Look for contradictions between data sources (e.g., BigQuery segment = "Catalog-Focused" but Postgres login_events shows daily logins).
- Pay special attention to edge cases and boundary accounts — that's where segmentation models break.
- Test the central thesis (price predicts value) quantitatively, not just narratively.

Be direct. If the model is 80% right and 20% wrong, say so and say which 20%.
