# Account Brief Generation Prompt — v2

Copy everything below the line into a new Cursor chat (Opus 4.6). Replace `[ACCOUNT_NAME]` and `[ORG_SHORTNAME]` with the target account before pasting.

---

IMPORTANT: Do NOT reference, use, or pull from any previous conversations, cached files, memory, or prior work in this workspace. This is a clean-slate run. The ONLY inputs you should use are:

1. The reference documents in the `EBR 2.0` folder (listed below)
2. Live data from BigQuery (WELD_RAW) and PostgreSQL (SuperCat Production) via MCP
3. Admin Console CSV files uploaded to this chat (if provided)
4. The instructions in this prompt

If you encounter anything that looks like prior analysis, scoring, or account briefs from previous sessions — ignore it completely. Query all data fresh. Generate everything from scratch.

---

## Task

Generate both an Account Snapshot (Version A) and an Account Intelligence Brief (Version B) for **[ACCOUNT_NAME]** (org shortname: `[ORG_SHORTNAME]`).

You have access to BigQuery (WELD_RAW dataset) and PostgreSQL (SuperCat Production) via MCP. You also have reference documents in the `EBR 2.0` folder that define the frameworks you'll follow.

---

## Step 0: Prerequisite Check — Admin Console CSVs

Before doing ANYTHING else, check whether the following Admin Console CSV exports have been uploaded to this chat or are present in the workspace:

1. **Admin CLM Report** (`clm_[date_range].csv`) — Per-rep feature usage counts. Columns: User, Name, Last Login Date, eCat Version, iOS Version, iPad Type, Logins, then one column per feature (Search Products, Filter Products, Change Catalog Sort, Search Collections, Create 'My List', Edit 'My List', View 'My List', Share 'My List', Create Customer Product List, View Cust. Product List, Create Maybe List, Email Item Info, Create PDF Catalog, Export Data to CSV/Excel, View Library Entry, Email Single/Multiple Library Entries, PDF searches, Select a Customer, Search for Customer, Show Sales in Catalog, View Cust. Favorites/Backorders, View SmartPicks, Access Sales Portal, View iPad Orders, View/Order Kit, Order Configured Item, Order From Maybe List, Scan Item with Camera, Submit Order, View Placements, View Commitments, View Flipbook, Add to List/Order from Flipbook).
2. **Admin Orders Report** (`[Account]_Admin_Orders_Report_[date_range].csv`) — Order-level detail. Columns: Order Number, Order Date, Customer Number, Customer Name, PO Number, Territory, Order Type, Order Origin, Order Total, Currency.

These CSVs are NOT available via MCP. They must be manually exported from the SuperCat Admin Console and uploaded.

**If either CSV is missing, STOP immediately.** Do not proceed with data collection or brief generation. Instead, respond with exactly this:

> **Missing required data files.** To generate the account brief for [ACCOUNT_NAME], I need the following Admin Console CSV exports uploaded to this chat:
>
> - [ ] Admin CLM Report — exported from Admin Console → Feature Usage / CLM for [ACCOUNT_NAME], date range covering at least the last 90 days
> - [ ] Admin Orders Report — exported from Admin Console → Orders Report for [ACCOUNT_NAME], date range covering at least the last 90 days
>
> Once both files are uploaded, re-run this prompt.

Do not attempt to generate a partial brief without these files. The CLM provides the canonical per-rep Activity Ladder data, and the Orders Report provides AOV, order type/origin breakdown, territory performance, and customer-level order attribution that are critical to scoring accuracy and brief quality.

**How to use the CSVs once present:**
- **CLM Report:** This is the definitive source for per-rep feature usage. Use it for Activity Ladder scoring, Feature Breadth per user, rep leaderboards, and identifying power users vs. inactive reps. The column headers use PascalCase event names — these are the legacy names from the Event Name Mapping table. Cross-reference with Mixpanel data for validation but prefer CLM counts for per-rep breakdowns since Mixpanel usernames may not match 1:1.
- **Orders Report:** Compute AOV (average of Order Total), order volume by period, Order Type breakdown (Confirmed/Quote/HFC), Order Origin breakdown (Regular/Market/Event), territory-level performance (group by Territory), customer concentration (group by Customer Name), and customer activation rate (distinct Customer Numbers with orders / total customers in Postgres).

---

## Step 1: Read Reference Documents

Read these files from the `EBR 2.0` folder before generating anything:

1. **`Internal_Account_Brief_Outlines.md`** — Structural blueprint. Follow sections A1-A6 (Snapshot) and B1-B8 (Intelligence Brief) exactly.
2. **`Account_Scoring_Framework_v3.md`** — Two-score model (Expansion Readiness + Retention Risk). Component weights, inputs, use-case profiles, Fathom/HelpScout absence protocol.
3. **`Scoring_Thresholds_Companion.md`** — Explicit 0/25/50/75/100 thresholds for every scoring input. USE THESE for all scoring decisions — do not invent your own thresholds.
4. **`Metrics_Framework_QBR_EBR_Full_Surface_Area_v5.md`** — Full 180-metric reference including the Event Name Mapping table in Appendix B (critical for Mixpanel queries).
5. **`Metrics_Surface_Area_v5.csv`** — Flat reference of all 180 metrics with data sources.

---

## Step 2: Mixpanel Event Name Discovery

Before running any Mixpanel queries, determine which event naming convention this org uses:

```sql
SELECT DISTINCT mp_event_name
FROM `mixpanel__events`
WHERE [org filter for ACCOUNT_NAME]
  AND _timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
ORDER BY mp_event_name
LIMIT 50
```

Compare the results against the **Event Name Mapping table in Appendix B** of the Metrics Framework. Determine if this org uses legacy PascalCase (`Search Products`, `Select Customer`) or modern snake_case (`product_search`, `customer_selection`). Apply the correct event names for ALL subsequent Mixpanel queries.

If legacy names return zero rows, try modern names before concluding the event doesn't exist. Log any events that don't exist under either convention in the Generation Notes.

---

## Step 3: Use-Case Profile Detection

Determine the account's use-case profile (three options):

1. Query Mixpanel for `Submit Order` / `submit_order` events in the last 90 days
2. Query PostgreSQL `orders` table for this org's orders in the last 90 days

**Classification:**
- **Ordering:** Submit Order events exist in Mixpanel → full transactional scoring
- **Non-Ordering:** Zero Submit Order events AND zero orders in PostgreSQL → buyer-facing action scoring only
- **Non-Ordering + Pushed Data:** Zero Submit Order events in Mixpanel BUT orders exist in PostgreSQL (ERP imports) → hybrid scoring. Business Impact uses all non-ordering inputs PLUS pushed order metrics at 50% weight.

Set the profile flag and apply it to all scoring components and brief sections.

---

## Step 4: Data Collection

### PostgreSQL (SuperCat Production)

**Known schema notes (from prior test runs — verify before querying):**
- Organization lookup: `SELECT * FROM organizations WHERE shortname = '[ORG_SHORTNAME]'` — note: column is `shortname` (no underscore), NOT `short_name`
- There is no `status` column on organizations — use `state` (but this is geographic state, not account status)
- `authenticated_sessions` does NOT have an `organization_id` column — join through `org_users` to filter by org
- `data_versions` uses `timestamp`, not `updated_at`
- `import_events.data` is a YAML text field, not JSON — use `LIKE` string matching, not `->>`operators
- `product_images` does NOT have a `product_id` column — can only count images per org via `organization_id`

**Tables to query:**
- Organization config: `organizations`, `org_users`, `org_setting_values`
- Users: `users`, `user_types`, `authenticated_sessions`
- Products: `products`, `product_images`, `options`
- Customers: `customers`, `customer_favorites`
- Orders: `orders`, `cart_items`, `portal_orders`, `portal_order_items`, `portal_invoices`
- Territories: `territories`
- Subscriptions: `subscriptions`, `subscription_plans`
- Data health: `import_events`, `data_versions`, `inventories`
- Pricing: `price_levels`, `contract_prices`
- Content: `taxonomies`, `smart_stacks`

### BigQuery (WELD_RAW)

**Schema verification:** Use the `describe_table` MCP tool (NOT `INFORMATION_SCHEMA` queries — these fail through the BigQuery MCP server). Verify column names on any table before your first query against it.

**Tables to query:**
- **Mixpanel:** `mixpanel__events` — use the correct event names from Step 2
- **HelpScout:** `helpscout__help_scout_tickets`, `helpscout__conversation_threads` — match on `conv_customer_organization` containing "[ACCOUNT_NAME]" or customer email domain
- **Fathom:** `fathom__ai_summaries`, `fathom__sales_meetings_from_fathom_hubspot` — match on company/account name, invitee emails, invitee names, and AI summary text content
- **HubSpot:** `hubspot__deal`, `hubspot__company`, `hubspot__contact` — match on company name containing "[ACCOUNT_NAME]"
- **Stripe:** `stripe__subscription`, `stripe__invoice`, `stripe__customer` — match on customer name/email. **Note:** not all accounts have Stripe subscriptions. If `stripe__subscription` returns 0 rows, fall back to `stripe__invoice` for billing data. Then QuickBooks. Then PostgreSQL `subscriptions`.
- **QuickBooks:** `quickbooks__invoice` — match on customer name

---

## Step 5: Scoring

Compute both scores using the component structure in `Account_Scoring_Framework_v3.md` and the explicit thresholds in `Scoring_Thresholds_Companion.md`.

**For each component:**
1. Query the specified data sources for each input
2. Look up the input value in the threshold table to determine the 0-100 score
3. Average the input scores to get the component score
4. Apply the component weight

**Critical scoring rules:**
- **Use the thresholds document.** Do not invent your own thresholds or benchmarks.
- **Canonical Active User:** Distinct Mixpanel usernames with ≥1 event in period, excluding SuperCat admin usernames (listed in Metrics Framework Appendix C). This is the ONLY active user definition used in scoring.
- **Fathom absence is NOT a penalty.** If no Fathom data exists, Fathom inputs are N/A — weight redistributes to remaining inputs. Do not score Fathom absence as zero. Surface it as an operational callout in the brief, not a scoring input.
- **HelpScout silence is only a risk signal when it represents a CHANGE from established patterns.** Low tickets from a high-engagement account = self-sufficient. Compare current cadence to the account's own historical norm.
- **Pushed data clients (Non-Ordering + Pushed Data profile):** Include pushed order metrics in Business Impact at 50% weight per the thresholds document formula.
- **Insufficient data:** If an input can't be computed, mark as N/A and redistribute weight. Do not score as zero.

---

## Step 6: Generate Outputs

**Output 1: `[ACCOUNT_NAME]_Snapshot_v1.md`**
Follow sections A1-A6 from `Internal_Account_Brief_Outlines.md`. Keep it to one-screen density. Use actual data values.

**Output 2: `[ACCOUNT_NAME]_Intelligence_Brief_v1.md`**
Follow sections B1-B7 from `Internal_Account_Brief_Outlines.md`. Use actual data values throughout.

For B8 (Context & Preparation): only generate this section if context is provided below. If no context line appears, omit B8 entirely.

**B8 Context:** [LEAVE BLANK OR INSERT CONTEXT, e.g., "EBR preparation — first executive business review with this client."]

**Output 3: `[ACCOUNT_NAME]_Generation_Notes_v1.md`**
Document EVERYTHING:
1. **Data gaps:** Sections/fields that couldn't be populated, and why
2. **Schema mismatches:** Expected vs. actual table/column names
3. **Scoring limitations:** Components marked N/A, what data would fix them
4. **Query issues:** Failed or unexpected query results
5. **Framework feedback:** Sections that felt redundant, unclear, or missing something
6. **CSV data usage:** Which metrics were computed from the CLM Report and Orders Report CSVs, and any parsing issues

---

## Execution Order

1. **Step 0:** Check for Admin Console CSVs — STOP if missing
2. **Step 1:** Read all 5 reference documents
3. **Step 2:** Discover Mixpanel event naming convention
4. **Step 3:** Detect use-case profile (ordering / non-ordering / non-ordering + pushed data)
5. **Step 4:** Pull all PostgreSQL data, then all BigQuery data
6. **Step 5:** Compute both scores using threshold document
7. **Step 6:** Generate Snapshot, Intelligence Brief, and Generation Notes
8. Save all three files as markdown in the workspace
