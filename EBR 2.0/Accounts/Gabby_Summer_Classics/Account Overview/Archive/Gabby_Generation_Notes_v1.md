# Gabby — Generation Notes

**Generated:** March 3, 2026 | **Prompt Version:** Clean-slate run

---

## Data Gaps

| Section/Field | Gap | Impact | Resolution |
|---|---|---|---|
| **Fathom meetings** | Zero Gabby-specific meetings in 180 days. Three results matched on keyword "Gabby" in AI summaries but were internal SuperCat or prospect meetings. | Relationship Strength and Relationship Cooling scored with Fathom inputs as N/A, weight redistributed. B5 Fathom section populated with absence protocol. | Search expanded to Meeting Title, Invitees Name/Email, and AI Summary text using both "Gabby" and "Summer Classics" patterns. No matches for direct account meetings. |
| **HubSpot deals** | Zero deals found matching any Gabby/Summer Classics/Gabriella naming. | Growth Signals HubSpot input scored as 0. B5 open deals section reports "None found." | Searched `properties_dealname` with LIKE patterns for 'gabby', 'summer classic', 'gabriella'. The account may not have a HubSpot company record, or deals may use a different naming convention. |
| **HubSpot company/contact** | Not queried — deal search returned 0 results suggesting HubSpot records may not exist for this account. | B1 headquarters, industry, and some identity fields sourced from PostgreSQL and Stripe instead. Account Owner shows "Not assigned." | Could attempt broader HubSpot search by email domain (@gabriellawhite.com, @summerclassics.com) in a follow-up run. |
| **QuickBooks invoices** | Query failed — `customer_display_name` column not recognized. Schema mismatch on the QuickBooks table. | Invoice aging scored from Stripe only. No QuickBooks backup for payment terms or AR aging. | Need to run `describe_table` on `quickbooks__invoice` to identify correct column names. |
| **Order revenue trend (3-month)** | Admin Orders Report covers Jan 1 – Mar 3 only (2 full months). No December data in CSV. | Scored Order Volume Trend using Mixpanel `order_submitted` monthly counts (Oct–Feb available). Revenue trend for Financial Distress scored Jan→Feb only. | Mixpanel order counts: Oct 933, Nov 668, Dec 514, Jan 905, Feb 791. Seasonal volatility makes 3-month directional assessment noisy. |
| **User Growth (net new, 90d)** | No historical `org_users` snapshot to compare. Only current state available. | Scored as flat (25). MAU growth (42→49) suggests potential net gain, but cannot confirm from PG data alone. | Would need a prior-period org_users count or created_at analysis of recent user additions to score precisely. |
| **Segment benchmarks** | No portfolio-wide benchmark data available for this run (would require running all 129 accounts). | AOV and Customer Activation scored against framework thresholds, not actual segment medians. Peer benchmarking in B6 uses qualitative framing. | First full portfolio run would establish empirical segment medians for all threshold inputs. |
| **HelpScout ticket tags** | `ticket_tags` is a RECORD (nested) type. Could not flatten in initial query. | Ticket themes derived from subject-line analysis rather than tag-based clustering. Billing/cancellation tag check based on subject content. | Need to use UNNEST() on ticket_tags field to access tag names for proper tag-based analysis. |
| **Customer wait time** | `ticket_customer_waiting_secs` values appear unreasonably large (1.77 trillion seconds ≈ 56,000+ years). Likely a data quality issue in the HelpScout sync. | HelpScout Responsiveness scored qualitatively (mix of resolved and pending) rather than using wait time data. | Investigate whether this field uses a different unit or is being populated incorrectly by the Weld sync. |

---

## Schema Mismatches

| Expected | Actual | Table | Fix Applied |
|---|---|---|---|
| `organization_name` | `organization_shortname` (or `current_organization_shortname`) | `mixpanel__events` | Used `current_organization_shortname = 'gh'` — this is the correct field for event-time org context. `organization_shortname = 'gh'` returned only `api_access` events. |
| `_timestamp` | `time` (FLOAT, Unix epoch) | `mixpanel__events` | Used `TIMESTAMP_SECONDS(CAST(time AS INT64))` for all time filtering. `current_date` field is DATE type, requires `DATE_SUB()` not `TIMESTAMP_SUB()`. |
| `mp_event_name` | `event_name` | `mixpanel__events` | Column is `event_name`, not `mp_event_name`. |
| `u.user_type_id` | `ou.user_type_id` | `users` / `org_users` | `user_type_id` is on `org_users`, not `users`. Join path: `org_users.user_type_id → user_types.id`. |
| `ou.billable` | `u.billable` | `org_users` / `users` | `billable` column is on the `users` table, not `org_users`. |
| `property_dealname` | `properties_dealname` | `hubspot__deal` | HubSpot columns use `properties_` prefix (plural), not `property_`. |
| `data_type` column | Does not exist | `import_events` | `import_events` only has: id, created_at, organization_id, data (YAML text). No `data_type` column — import type must be parsed from YAML `data` field. |
| `customer_display_name` | Unknown | `quickbooks__invoice` | Column not recognized. Schema not verified before query. Need `describe_table` to determine correct column names. |

---

## Scoring Limitations

### Components Scored as N/A

| Component | Input | Reason | Weight Handling |
|---|---|---|---|
| Expansion: Growth Signals | Fathom Pain → Unused Feature Matches | No Fathom data for Gabby | Weight redistributed to remaining 4 inputs |
| Expansion: Relationship Strength | Fathom Meeting Cadence | No Fathom meetings recorded | Weight redistributed to remaining 3 inputs (Days Since, Stakeholder Breadth, HelpScout Responsiveness) |
| Risk: Relationship Cooling | Days Since Last Fathom Meeting | No Fathom data | Weight redistributed to HelpScout inputs |
| Risk: Relationship Cooling | Competitor Mentions | No Fathom data | Weight redistributed to HelpScout inputs |

### What Data Would Fix Them

- **Fathom:** Even 1-2 recorded calls would provide meeting cadence, pain themes, competitor mentions, and action items. Scheduling Fathom-recorded meetings going forward would populate these inputs for future briefs.
- **HubSpot:** Creating a company record for Gabriella White/Gabby in HubSpot and associating contacts would enable stakeholder breadth, deal tracking, and owner assignment scoring.

### Scoring Judgment Calls

1. **Order Revenue Trend (Financial Distress):** Jan→Feb revenue dropped 29% ($3.96M→$2.81M). Scored as 75 (declined 15–30%) per threshold table. However, January likely included High Point Market orders driving an artificial spike. The annualized run rate remains healthy. This single input drove the Financial Distress component to 19 — without it, Financial Distress would score ~0.

2. **Unresolved Ticket Age (Relationship Cooling):** Oldest pending ticket is 55 days old (Jan 7). Scored as 100 (>30 days) per threshold table. However, several of these tickets are enhancement requests or bugs awaiting product roadmap decisions, not true support failures. This single input drove Relationship Cooling to 33. In practice, the cooling risk may be lower than the score suggests if the client understands these are feature requests in queue.

3. **Customer Activation Rate (Business Impact):** 968/11,812 = 8.2%. Scored as 25 (5–15% band). The denominator (11,812) includes the full customer database which likely contains historical/inactive customers. The "real" addressable customer base may be smaller, which would push the activation rate higher. A customer data cleanup could improve this metric meaningfully.

4. **Active User Ratio calculation:** Used Mixpanel active (56) / PG active billable non-customer users (60) = 93%. The CLM shows 114 users with logins, but the CLM spans all 4 parent entities. For the gh-specific ratio, PG org 55 users are the correct denominator. The 93% may be slightly inflated if some Mixpanel users are primarily assigned to sibling entities but had gh-context events.

5. **User Count Change (Engagement Decline):** Scored as 50 (flat) due to absence of historical org_users data. MAU growth from 42→49 suggests possible net user gain, but MAU and PG user count are different measures. Conservative scoring applied.

---

## Query Issues

| Query | Issue | Resolution |
|---|---|---|
| Initial Mixpanel event discovery | `organization_shortname = 'gh'` returned only `api_access` (1,325 events). iPad/app events tracked under `current_organization_shortname`. | Switched to `current_organization_shortname = 'gh'` — returned 33 distinct event types, 48K+ events. This is the correct filter for event-time org context. |
| HelpScout first attempt | Searched `conv_customer_organization LIKE '%gabby%' OR LIKE '%summer classic%'` — 0 results. | Organization name in HelpScout is "Gabriella White" and "SC Home/Gabby LLC". Found via email domain search (`%gabriellawhite%`, `%summerclassics%`), then filtered by discovered org names. |
| BigQuery `current_date` column | `current_date >= TIMESTAMP_SUB(...)` failed — type mismatch (DATE vs TIMESTAMP). | Used `TIMESTAMP_SECONDS(CAST(time AS INT64))` for time filtering instead of `current_date` column. |
| Stripe subscription | 0 rows returned — table is empty. | Fell back to `stripe__invoice` per billing model detection hierarchy. Found Gabby invoices under "SC Home/Gabby LLC" customer name. |
| QuickBooks invoice | `customer_display_name` column not found. | Query abandoned. Financial data sourced entirely from Stripe. Need to describe QuickBooks table schema for future runs. |

---

## CSV Data Usage

### Admin CLM Report (`sc_2026-01-01_2026-03-02.csv`)

| Metric Computed | Source Columns | Notes |
|---|---|---|
| Activity Ladder per-level adoption | All feature columns mapped to L1–L6 clusters | CLM uses legacy PascalCase event names; mapped per Appendix B Event Name Mapping |
| Feature Breadth Score (9.8 avg) | Count of non-zero feature columns per user | 38 feature columns checked per user |
| Power user identification (Top 10) | Sum of all feature + login columns | Composite activity ranking |
| Ordering user analysis (55/114, 48%) | `Submit Order` column | Used for concentration risk, top orderer identification |
| Rep login counts | `Logins` column | Cross-referenced with Mixpanel `selected_org` for login frequency |

**Parsing Notes:**
- CLM file named `sc_2026-01-01_2026-03-02.csv` — the `sc` prefix likely refers to the parent account/admin console grouping, not the `sc` (Summer Classics Wholesale) entity specifically.
- File contains 121 rows (users) spanning all 4 Gabriella White entities. Users with "sc-" prefix are shared reps across entities.
- 7 users have no login date or logins (blank fields) — likely accounts that have never been used or were created but never activated.
- Some users appear in CLM but NOT in PG org 55 user list (e.g., users primarily assigned to scw/sc/sccon). For Gabby-specific scoring, Mixpanel `current_organization_shortname = 'gh'` provides the definitive active user filter.

### Admin Orders Report (`Gabby Admin Orders Report 2026-01-01 - 2026-03-03.csv`)

| Metric Computed | Source Columns | Notes |
|---|---|---|
| AOV ($3,122.59) | `Order Total` / order count | 2,215 orders, $6,916,544 total |
| Order Type breakdown | `Order Type` | Confirmed 87.3%, Quote 12.4%, TEST 0.3% |
| Order Origin breakdown | `Order Origin` | Regular (blank) 64.2%, Website 35.8% |
| Territory performance (Top 10) | `Territory`, `Order Total`, `Customer Number` | South Team leads at 36.8% of revenue |
| Customer concentration | `Customer Name`, `Order Total` | Top customer 1.8% — very low concentration |
| Customer activation rate | Distinct `Customer Number` = 968 / PG total 11,812 | 8.2% activation |
| Monthly revenue breakdown | `Order Date` parsed to month | Jan $3.96M, Feb $2.81M |

**Parsing Notes:**
- Order Date format: YYYY-MM-DD (standard, no parsing issues)
- 7 TEST orders included in totals — negligible impact ($14,527 of $6.92M = 0.2%)
- `Order Origin` blank for 1,422 orders — treated as "Regular" (non-website/non-event origin)
- Currency: all USD

---

## Framework Feedback

1. **Multi-entity accounts need explicit guidance.** The framework assumes a 1:1 org-to-account mapping. For Gabby (4 entities sharing reps, billing, and support), every metric requires a decision: entity-specific or parent-aggregate? The prompt should include a "multi-entity protocol" specifying which metrics scope to the entity vs. parent.

2. **CLM-to-Mixpanel reconciliation is non-trivial.** CLM usernames don't always match Mixpanel usernames (case sensitivity, prefixes). CLM covers all entities while Mixpanel can filter by `current_organization_shortname`. A clear "source of truth" designation per metric would reduce ambiguity.

3. **Customer Activation Rate denominator needs scrutiny.** 11,812 total customers likely includes years of historical data. For ordering clients, a "customers with any activity in last 12 months" denominator might produce a more actionable metric than the full database count.

4. **HelpScout customer_waiting_secs appears broken.** Values in the trillions of seconds suggest a sync or unit issue. This field should be validated across the portfolio before being used for scoring.

5. **Billing model detection for multi-entity accounts.** Stripe has separate customer records for "SC Home/Gabby LLC" and "Summer Classics". The combined MRR requires summing across Stripe customers, which the framework doesn't explicitly address for multi-entity accounts.

6. **Order Volume Trend scoring is noisy for seasonal accounts.** MoM direction over 3 months doesn't account for seasonality (market months, trade shows). For outdoor/casual furniture clients, a year-over-year same-month comparison would be more signal and less noise than MoM trending.

7. **Activity Ladder L4 gap pattern.** The framework doesn't call out this specific pattern (high L5/L6, low L4) as a named signal. It's worth adding as an expansion signal in Section 14: "L4 Bypass — L5 adoption >2x L4 indicates reps bypassing personalization features, suggesting either a training gap or a workflow that doesn't incentivize customer-specific curation."

---

*Generation Notes | Gabby (gh) | Generated March 3, 2026*
