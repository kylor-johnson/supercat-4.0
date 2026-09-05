# Generation Notes — Crystorama Account Brief Test Run

**Generated:** February 26, 2026 | **Author:** Automated via Cursor/MCP | **Test Purpose:** Validate Internal Account Brief frameworks, scoring model, and data pipeline against a real account.

---

## 1. Data Gaps

### 1.1 Fathom — Complete Absence

**Impact: HIGH (affects 4 sections + 2 scoring components)**

Zero Fathom meeting records found for Crystorama. Searched `fathom__ai_summaries` across: meeting titles, invitee emails (@crystorama.com), invitee names, external company domains, and AI summary text content. Also searched `fathom__sales_meetings_from_fathom_hubspot` across all MEDDIC fields.

**Sections affected:**
- A3 (Top 3 Signals): No Fathom-sourced signals available
- A5 (Recent Activity): "Last Fathom Call" = blank
- B5 (Relationship & Support History): Entire Fathom subsection is empty
- B8 (Context & Preparation): "Commitments from Prior Engagement" = none
- Expansion Readiness → Relationship Strength component: Fathom meeting cadence is N/A
- Retention Risk → Relationship Cooling component: Fathom signals are N/A

**Possible causes:**
1. Crystorama meetings genuinely aren't recorded in Fathom (no Fathom integration active for their calls)
2. Meetings happen at trade shows, in-person, or via phone without Fathom
3. The company name in Fathom doesn't match "Crystorama" (different subsidiary name, contact email domain mismatch, etc.)

**Recommendation:** Fathom absence should be a documented state in the framework, not just an N/A. The framework should explicitly describe how to handle accounts with zero Fathom data — it's a meaningful signal in itself (either we don't have meetings, or we don't record them, both of which are important).

### 1.2 Admin Console Exports — Not Available via MCP

**Impact: HIGH (affects ~30 metrics)**

The Admin Console CLM (Client Lifecycle Management) report, Admin Sales Summary, and Admin Orders Report are CSV exports generated on-demand from the SuperCat Admin Console. They are **not** available via MCP (neither PostgreSQL nor BigQuery).

**Metrics that could NOT be computed due to missing Admin Console data:**
- AOV (precise, by channel — estimated from Postgres `orders.total` instead)
- Orders per Active User (per rep)
- Revenue per Active User
- Items per Order
- Channel Revenue Share / Channel AOV Comparison
- Order Type Breakdown (Confirmed / Quote / HFC)
- Order Origin Mix (Regular / Market / Event)
- Territory Order Volume / Revenue / AOV / Customer Count
- Rep-to-Customer Mapping (precise)
- Customer Concentration (order-level)
- Customer Activation Rate (precise per-customer order attribution)
- All Territory Performance metrics (Section 2a of the metrics framework)

**Recommendation:** The framework lists "Admin Console" as a primary data source for ~30 metrics but doesn't account for the fact that Admin Console exports aren't programmatically accessible. Either: (a) build an automated export pipeline that pushes Admin Console data to BigQuery/Postgres, or (b) flag these metrics as "requires manual CSV export" in the framework so the prompt knows not to attempt them.

### 1.3 Stripe Subscriptions — Zero Rows

**Impact: MEDIUM**

`stripe__subscription` returned 0 rows for Crystorama (customer_id `cus_SXChBKEeY6rWWE`). Despite monthly invoicing at $2,540/mo, there are no active Stripe subscriptions. Billing appears to be manual invoice-based rather than subscription-based.

**Affected metrics:**
- MRR by Product Line (can't break down $2,540 by product)
- Subscription Completeness (can't validate which products are active via Stripe; used Postgres `subscriptions` table instead)
- MRR Trend (no subscription history; derived from QuickBooks invoice amounts instead)
- Net Revenue Retention (no subscription-level period comparison)

**Recommendation:** The framework should specify a fallback hierarchy: Stripe subscription → Stripe invoice → QuickBooks invoice → Postgres subscriptions. Not all accounts will have Stripe subscriptions even if they have Stripe invoices.

### 1.4 Mixpanel Event Name Mismatch

**Impact: MEDIUM (requires event name mapping layer)**

Crystorama's Mixpanel events use **snake_case** naming (newer SDK): `product_search`, `customer_selection`, `item_email_drafted`, `pdf_catalog_generated`, etc. The framework's Activity Ladder and Appendix B reference **PascalCase/legacy** event names: `Search Products`, `Select Customer`, `Email Item Info`, `Create PDF Catalog`, etc.

A query filtering for legacy event names returns **zero rows** for Crystorama. The event name mapping must be applied before querying.

**Full mapping discovered:**

| Framework Name | Actual Mixpanel Name (Crystorama) |
|---|---|
| Search Products | `product_search` |
| Select Customer | `customer_selection` |
| Search Customer | `customer_search` |
| Filter Products | `filter_button_pressed` |
| Change Catalog Sort | `product_sort_changed` |
| Search Collections | `collection_search` |
| Email Item Info | `item_email_drafted` |
| Create PDF Catalog | `pdf_catalog_generated` |
| View Cust. Favorites | `view_favorites` |
| View Cust. Backorders | *(not found)* |
| View SmartPicks | `view_customer_smart_picks` |
| View Placements | `view_customer_placements` |
| View iPad Orders | `view_customer_orders` |
| View Library Entry | `view_document` |
| Access Sales Portal | `view_portal` |
| Submit Order | *(not present for Crystorama)* |
| My Lists | `view_stack` |
| Edit My List | `edit_stack` |
| Share My List | *(not found)* |
| Create Customer Product List | `create_stack` *(overloaded — same event for personal and customer lists?)* |
| Order From Maybe List | `add_to_order_from_maybe_list` |
| Create Maybe List | *(not found as distinct event — may be captured differently)* |
| PDF searches | *(not found)* |
| Email Single Library Entry | `document_email_drafted` *(overloaded?)* |
| Email Multiple Library Entries | *(not found as distinct event)* |
| item_added_via_magic_button | `item_added_via_magic_button` *(same — TTFV event)* |
| document_email_drafted | `document_email_drafted` *(same)* |
| item_email_drafted | `item_email_drafted` *(same)* |

**Recommendation:** The framework needs a canonical event name mapping table that covers both legacy PascalCase and modern snake_case conventions. The prompt should try both naming conventions, or the event mapping should be pre-applied in BigQuery via a view. This is the single most impactful schema issue — without it, Activity Ladder queries return zero for newer orgs.

### 1.5 Login Events — Not Tracked Under Expected Name

**Impact: LOW-MEDIUM**

No events named `Login` or `login` exist in Crystorama's Mixpanel data. Login activity is likely captured by the `selected_org` event (3,202 events in 90 days), which fires when a user selects their organization post-authentication. Login frequency calculations used `selected_org` as a proxy.

**Recommendation:** Framework should specify that `selected_org` is the login proxy event for orgs using the newer SDK, or the `login_events` Postgres table should be used as the primary source.

### 1.6 HelpScout Customer Wait Time — Data Quality Issue

**Impact: LOW**

The `ticket_customer_waiting_secs` field in `helpscout__help_scout_tickets` contains values that resemble Unix timestamps (~1.77 trillion) rather than actual wait durations in seconds. These cannot be interpreted as wait times.

**Recommendation:** Investigate the HelpScout → BigQuery sync pipeline. The field may be storing a timestamp instead of a duration, or the column name is misleading.

---

## 2. Schema Mismatches

| Expected (Framework) | Actual (Database) | Table | Notes |
|---|---|---|---|
| `organizations.short_name` | `organizations.shortname` | PostgreSQL | No underscore |
| `organizations.status` | `organizations.state` | PostgreSQL | Different name and meaning (state = NY, not account status) |
| `product_images.product_id` | No `product_id` column | PostgreSQL | Images link to org via `organization_id`, not to individual products. Can't compute "Products with Images %" directly. |
| `authenticated_sessions.organization_id` | Column doesn't exist | PostgreSQL | Must join through `org_users` table to filter by org |
| `data_versions.updated_at` | `data_versions.timestamp` | PostgreSQL | Different column name |
| `org_settings` table | Does not exist | PostgreSQL | Only `org_setting_values` exists, and it returned 0 rows for Crystorama |
| `import_events.import_type` as clean field | `import_events.data` as YAML blob | PostgreSQL | Import type is embedded in a YAML text field, not a clean column. Requires string parsing. |
| Mixpanel event names (PascalCase) | snake_case event names | BigQuery | See Section 1.4 above |
| `stripe__subscription` data | 0 rows for Crystorama | BigQuery | Manual billing, no subscription objects |
| `ticket_customer_waiting_secs` = seconds | Contains epoch-like values | BigQuery | See Section 1.6 above |

---

## 3. Scoring Limitations

### 3.1 Components Scored with Incomplete Data

| Component | Score Given | Limitation | Data Needed |
|---|---|---|---|
| **Expansion: Relationship Strength** | 55 (adjusted from 75) | Fathom meeting cadence is N/A. Scored using HelpScout ticket responsiveness and HubSpot stakeholder count only. Applied conservative downward adjustment because absence of proactive outreach data is a real gap, not just missing data. | Fathom recordings of Crystorama meetings |
| **Expansion: Business Impact** | 60 | Non-ordering protocol excludes pushed order data ($536K/12mo) from scoring. Buyer-facing actions alone underrepresent the platform's impact for this account. | Framework guidance on how to score non-ordering clients who push significant order data |
| **Expansion: Growth Signals** | 55 | No Fathom pain themes available. No open HubSpot deals. Territory count = 0 (may be structural, not a signal). Expansion signals are triggered but can't be benchmarked against peer segment without portfolio-wide run. | Fathom data, peer benchmark dataset, territory configuration context |
| **Risk: Relationship Cooling** | 10 | Fathom signals entirely N/A. Scored only on HelpScout patterns. | Fathom data |

### 3.2 Components That Cannot Be Scored At All

| Component Input | Why | What Would Fix It |
|---|---|---|
| Activity Ladder aggregate score (precise) | Event name mismatch means legacy queries return 0. Manual remapping was required. | Canonical event name mapping in the framework or BigQuery view |
| Feature Breadth Score (org-level) | Requires counting distinct features per user, then aggregating. Computed as a rough estimate from top-user feature counts. | Formalized scoring rubric with thresholds (e.g., >20 distinct features = Excellent) |
| Subscription Completeness (precise) | Stripe subscriptions = 0. Used Postgres `subscriptions` table as fallback. | Stripe subscription data, or framework-specified fallback hierarchy |
| Active User Ratio (definitive) | Multiple conflicting numbers: Mixpanel says 86, Postgres authenticated_sessions says 464, HubSpot says 66 active / 88 billable. | Clear definition of "active user" — Mixpanel event activity, Postgres sessions, or HubSpot-synced? |
| Customer Activation Rate (precise) | Requires per-customer order attribution from Admin Orders Report. Postgres `orders` table has aggregate data but customer-level activation requires join logic that wasn't tested. | Admin Console export or Postgres customer-to-order join |
| Peer benchmarking | Requires running the model across all 129 orgs. | Portfolio-wide scoring run |

### 3.3 Scoring Model Design Observations

1. **The non-ordering Business Impact scoring significantly underweights accounts that push order data.** Crystorama pushes $536K/year of order data and their reps use eCat for everything except the final Submit Order click. The current scoring protocol ignores this revenue entirely and scores only on PDF/email actions, producing a Business Impact score of 60 that doesn't reflect the platform's actual business value to this client.

2. **Relationship Strength weight redistribution is ambiguous.** The framework says to redistribute N/A component weight, but Relationship Strength is one component with multiple inputs, some of which are N/A (Fathom) and some of which are available (HelpScout, HubSpot). Should the entire component be marked N/A, or should it be scored on available inputs? I chose the latter with a conservative adjustment, but the framework should specify.

3. **The 0–100 scoring scale has no explicit thresholds for individual inputs.** For example, "Feature Breadth Score" — is 15 distinct features good? 25? The framework says to score 0–100 but doesn't provide reference points. This means every implementation will produce different scores based on the operator's assumptions. The scoring model needs a companion threshold document.

---

## 4. Query Issues

| Query | Issue | Resolution |
|---|---|---|
| `SELECT ... FROM organizations WHERE short_name = 'crystorama'` | Column is `shortname` (no underscore) | Fixed to `shortname` |
| `SELECT ... status FROM organizations` | Column is `state` (geographic, not account status) | Fixed, but there's no account status field in Postgres |
| `INFORMATION_SCHEMA.COLUMNS` in BigQuery with dataset prefix | Syntax error — BigQuery MCP server already scopes to dataset | Removed dataset prefix |
| Mixpanel Activity Ladder query with legacy event names | 0 rows returned — event names are snake_case for this org | Remapped using actual event names from top-events query |
| `authenticated_sessions` filtered by `organization_id` | Column doesn't exist on table | Joined through `org_users` |
| `data_versions` with `updated_at` column | Column is `timestamp` | Fixed |
| `import_events.data` YAML parsing | Can't use JSON operators (`->>`) on YAML text field | Used `LIKE` string matching instead |
| `product_images.product_id` | Column doesn't exist | Counted images per org instead of per product |
| Stripe subscriptions query | 0 rows despite active billing | Crystorama is invoiced manually, no subscription objects in Stripe |
| HelpScout `ticket_customer_waiting_secs` | Values are ~1.77T, not seconds | Flagged as data quality issue, metric not computed |
| Three deleted Stripe invoices at $3,960 | Unexpected — possible billing adjustment | Documented in Financial Status and Risks sections |
| BigQuery `INFORMATION_SCHEMA` queries | All failed with syntax errors through MCP | Used `describe_table` MCP tool instead |

---

## 5. Framework Feedback

### 5.1 What Worked Well

1. **The two-score model produces a meaningful quadrant.** Crystorama landing in GROW (67 expansion / 8 risk) feels right — it's a stable, deeply embedded account with clear expansion whitespace and zero churn signals. The quadrant tells you exactly how to approach them.

2. **The Snapshot (Version A) format is genuinely scannable.** A1–A6 can be consumed in 60 seconds. The Top 3 Signals section is the most valuable element — it forces the prompt to interpret rather than just report.

3. **The Intelligence Brief (Version B) section structure is comprehensive.** B1–B7 covers every angle. The stakeholder map populated well from HubSpot contacts.

4. **The use-case detection logic works.** Zero Mixpanel Submit Order + orders in Postgres = Non-Ordering + Pushed Data. The detection was clean and the framework sections adapted correctly.

5. **The data source quick reference table in the outline was helpful** for knowing where to query each element.

### 5.2 What Broke or Needs Iteration

1. **Event name mapping is the #1 blocker for automation.** The framework assumes legacy PascalCase event names that don't exist for newer orgs. This will produce zero-data Activity Ladder results for any org on the modern SDK unless a mapping layer is added. **Suggestion:** Add an event name alias table to the framework, or create a BigQuery view that normalizes event names.

2. **"Non-ordering" is too binary for accounts like Crystorama.** They push $536K/year in order data — the platform is clearly central to their order-to-cash workflow even though reps don't click Submit Order. The current framework scores them as if they have no order-related value, which is misleading. **Suggestion:** Add a third use-case: "Non-Ordering + Pushed Order Data" with a hybrid scoring approach that weights pushed order metrics at a discount (e.g., 50%) rather than ignoring them entirely.

3. **Active User count has three conflicting definitions.** Mixpanel (86 distinct usernames with events), Postgres authenticated_sessions (464 unique users with sessions), HubSpot (66 active users). The framework references all three sources in different places without specifying which is canonical. **Suggestion:** Define one canonical "Active User" metric and use it consistently. Recommendation: Mixpanel distinct users with ≥1 event in period, excluding SuperCat admin usernames.

4. **Admin Console data dependency creates a ~30-metric gap.** The framework lists Admin Console CLM, Admin Sales Summary, and Admin Orders Report as primary sources for many metrics. These aren't available via MCP. Either they need to be piped into BigQuery/Postgres, or the framework should mark them as "manual input required" and specify which metrics are MCP-computable vs. export-dependent.

5. **Fathom absence handling needs explicit protocol.** The framework says to score N/A components and redistribute weight, but doesn't address the case where an entire data source (Fathom) is missing for an account. Fathom absence affects Relationship Strength, Relationship Cooling, and multiple brief sections simultaneously. A blanket "redistribute weight" approach may over-inflate other components. **Suggestion:** Add a "data source availability check" step before scoring that flags which sources are present and adjusts the scoring model accordingly.

6. **The scoring model needs threshold definitions.** "Score each component 0–100 based on where values fall relative to benchmarks or reasonable thresholds" is too open-ended. Without defined thresholds, two different operators will produce different scores for the same data. **Suggestion:** Create a threshold companion document that defines what 0, 25, 50, 75, and 100 mean for each component input (e.g., "Active User Ratio: 0=<10%, 25=10–30%, 50=30–60%, 75=60–80%, 100=>80%").

7. **The B8 (Context & Preparation) section is the most valuable section for actual meeting prep.** It's where interpretation meets action. But it relies heavily on Fathom data for "Commitments from Prior Engagement" — if Fathom is empty, this section loses its most specific content. Consider adding HelpScout resolution promises and HubSpot deal notes as additional sources for commitments.

8. **The framework doesn't address imported/pushed data explicitly.** Crystorama has 116 "Sales Data / Portal Orders / Invoices" imports in the last 30 days and 178 orders in 12 months. This pushed data is a massive signal about account engagement that the framework largely ignores because it's designed around iPad-submitted orders. **Suggestion:** Add import cadence and pushed data volume as first-class metrics in the Data Health section, and incorporate pushed order trends into Business Impact for non-ordering clients.

9. **Territory Count = 0 is ambiguous.** For some accounts, this means they don't use the territory feature (structural choice). For others, it means territories haven't been configured (missed opportunity). The framework treats it as a pure expansion signal, but it needs context. **Suggestion:** Cross-reference territory count with whether the account has a sales rep structure that would benefit from territories.

10. **The Snapshot's "one page" constraint is achievable but tight.** A4 (Usage Pulse) alone has 9+ rows for non-ordering clients. With pushed order data AND non-ordering metrics, the section exceeds its intended density. **Suggestion:** For the Snapshot, show only the primary use-case metrics (non-ordering OR ordering, not both). Move the pushed-data context to a single summary line.

### 5.3 Suggested Framework Additions

1. **Event Name Mapping Table** — Canonical mapping of legacy ↔ modern event names, maintained as a reference file.
2. **Scoring Threshold Companion** — Explicit 0/25/50/75/100 thresholds for every component input.
3. **Data Source Availability Matrix** — Pre-scoring check: which of the 7 data sources (Postgres, Mixpanel, HelpScout, Fathom, HubSpot, Stripe, QuickBooks) have data for this account? Adjust model accordingly.
4. **Pushed Data Protocol** — Framework section for how to treat imported/pushed order data in scoring and reporting.
5. **Account Owner Detection** — Flag when HubSpot has no owner assigned; this is itself a risk signal.
6. **Billing Model Detection** — Some accounts are Stripe subscription, some are manual invoice. Framework should detect and adapt (currently assumes subscription).

---

## Summary Statistics

| Category | Count |
|---|---|
| **Total queries executed** | ~45 (PostgreSQL + BigQuery) |
| **Queries that failed on first attempt** | 12 (schema mismatches, column name errors) |
| **Queries that returned zero/empty results** | 8 (Fathom: 2, Stripe subscriptions: 1, Mixpanel legacy event names: 4, Login events: 1) |
| **Data sources with full data** | PostgreSQL (organizations, org_users, orders, products, customers, inventories, import_events, subscriptions), BigQuery Mixpanel (68,716 events), BigQuery HelpScout (26 tickets/12mo), BigQuery HubSpot (company, contacts, deals), BigQuery Stripe (invoices), BigQuery QuickBooks (157 invoices) |
| **Data sources with partial data** | Stripe (invoices but no subscriptions), HelpScout (wait time field corrupted) |
| **Data sources with no data** | Fathom (0 matches), Admin Console exports (not available via MCP) |
| **Scoring components fully computed** | 5 of 8 |
| **Scoring components with N/A or limited inputs** | 3 of 8 (Relationship Strength, Relationship Cooling, Business Impact — all partially scored with conservative adjustments) |
| **Expansion signals detected** | 7 active signals |
| **Framework sections that couldn't be populated** | B3 ordering-specific rep metrics, B4 customer-level activation detail, B5 Fathom subsection (entirely empty), per-territory analytics |
