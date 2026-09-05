# Summer Classics — Generation Notes

**Generated:** March 3, 2026 | **Brief Version:** 1.0

---

## 1. Data Gaps

| Section/Field | Gap | Impact | What Would Fix It |
|---|---|---|---|
| **Fathom — All Sections** | Zero DIRECT meetings found with SC/Gabriella White external contacts in 180+ days. Searched by: invitee emails (gabriellawhite.com, summerclassics.com), invitee names (Sateesh Donti, Ben Erickson, Jim Hardy, Wynne), meeting titles, external domain names. **Indirect references found:** SC is discussed in internal SuperCat support meetings (Kyla Bosch / Chuck Wiebe standups) — Jan 28 references "Summer Classics Bug," other meetings discuss Gabriella White queue items. All SC-relevant hits have `Meeting Has External Invitees: false`. | Relationship Strength and Relationship Cooling scored with Fathom inputs as N/A, weight redistributed. No direct meeting intelligence available. SC is on the internal radar via support but not through proactive engagement. | Establish Fathom-recorded meetings with SC contacts. Even one quarterly call would populate this entire data layer. |
| **HubSpot Deals** | Zero deals found for any Gabriella White entity. Searched by deal name containing Summer Classics, Gabby, SC Home. | Growth Signals "Open HubSpot Deals" scored as 0. No pipeline visibility. | Create HubSpot deals for expansion opportunities (e.g., Flipbook, customer activation program, seat expansion). |
| **HubSpot Account Owner** | Account owner field not confirmed from HubSpot data. Inferred as Brent Sanders from HubSpot contact data (Brent Sanders listed with SC company association). | Minor — no scoring impact. Used Brent Sanders as account owner. | Verify HubSpot owner assignment for SC company records. |
| **Segment Median AOV** | No portfolio-wide AOV benchmarks available. Estimated SC AOV ($3,123) as ~100–150% of Outdoor/Casual segment median. | AOV scoring approximated at 75 (100–150% of median). Could be off by one band. | Run AOV calculation across all 129 orgs to establish segment medians. |
| **eCat Online Customer Logins** | Self-service adoption scored from Order Origin breakdown (35.8% Website) in the Admin Orders Report. No direct customer login data from PostgreSQL or Mixpanel. | Self-Service Rate computed from order origin rather than distinct customer login counts. This is a proxy, not the canonical measure. | Query authenticated_sessions joined through org_users for customer-type users, or use Mixpanel web-context events. |

---

## 2. Schema Mismatches

| Expected | Actual | Resolution |
|---|---|---|
| `import_events.data_type` | Column does not exist. `import_events` schema: id, created_at, organization_id, data (text). | Used `data` field with LIKE matching for error detection. Counted total imports and those containing "error"/"Error" text. Data type breakdown not available without parsing YAML data field. |
| `data_versions.data_type` | Column is `entity_type`, not `data_type`. | Corrected query to use `entity_type`. Successfully retrieved per-entity last update timestamps. |
| `orders.customer_id` | Column is `customer_num`, not `customer_id`. | Corrected query. Retrieved 714 distinct customer_num values with orders in 90d. |
| `mixpanel__events.mp_event_name` | Column is `event_name`, not `mp_event_name`. | Corrected in first query attempt. All subsequent Mixpanel queries used `event_name`. |
| `mixpanel__events._timestamp` | Timestamp stored as FLOAT `time` column (Unix epoch). Also has `current_date` (TIMESTAMP) and `_weld_synced` (TIMESTAMP). | Used `TIMESTAMP_SECONDS(CAST(time AS INT64))` for all time-based filtering. |
| `mixpanel__events` org filter | `organization_shortname = 'scw'` returned only 1 event (`api_access`). Events tracked under `current_organization_shortname = 'scw'`. | Discovered via testing both filters. All Mixpanel queries use `current_organization_shortname = 'scw'` as the org filter. |
| `hubspot__deal.properties_hs_company_id` | Column doesn't exist. HubSpot deal schema uses different association structure. | Searched by deal name (LIKE '%summer classic%') instead. Returned 0 results — likely no deals exist. |
| `hubspot__contact.properties_hs_company_id` | Column doesn't exist. Contact uses `properties_company` (string name). | Searched by properties_company LIKE and email domain. Successfully returned 20 contacts. |
| `stripe__subscription` | Table exists but has 0 rows. | Fell back to `stripe__invoice` per billing model detection hierarchy. Found Summer Classics invoices by customer_name. |
| `quickbooks__invoice` | Table exists but has 0 rows. | Skipped QuickBooks. Used Stripe invoice as primary billing source, PostgreSQL subscriptions as secondary. |
| `authenticated_sessions` | Per known schema notes: does not have `organization_id`. Must join through `org_users`. | Did not directly query authenticated_sessions. Used Mixpanel `selected_org` event as login proxy per Event Name Mapping. |
| `org_users` count = 4,418 | This includes customer accounts (eCat Online users). Not a reliable billable user count for rep-based analysis. | Used CLM report (54 named users) as the canonical billable/licensed user count. |

---

## 3. Scoring Limitations

| Component | Input | Score | Limitation |
|---|---|---|---|
| **Relationship Strength** | Fathom Meeting Cadence | N/A | No direct Fathom meetings with SC contacts. Weight redistributed to remaining 3 inputs. Days Since Last Interaction corrected from >90d (0) to 28 days (75) after discovering HelpScout tickets under "Gabriella White" org. HelpScout Responsiveness corrected from "all resolved quickly" (75) to "Some unresolved" (25) — 7 pending tickets, oldest 55 days. Net component score: 58 (was 50). |
| **Growth Signals** | Fathom Pain → Unused Feature Matches | N/A | No Fathom data. Scored on 4 of 5 inputs. |
| **Growth Signals** | HubSpot Expansion Deals | 0 | Zero deals found. This is likely a CRM hygiene issue rather than absence of opportunity — the account clearly has expansion potential. |
| **Business Impact** | AOV vs. Segment Median | 75 (est.) | No portfolio-wide benchmark available. Estimated based on furniture/outdoor segment norms. |
| **Business Impact** | Customer Activation Rate | 25 | 8.6% activation on 8,281 total customers. The large customer base (likely includes historical/inactive accounts never cleaned up) may deflate this metric. A "cleaned" denominator (customers with any activity in 12 months) would likely yield a higher activation rate. |
| **Relationship Cooling** | Fathom inputs | N/A | Weight redistributed to HelpScout inputs (3 scored). Ticket Pattern: 0 (normal cadence). **Unresolved Ticket Age: 100** (oldest pending = 55 days, >30d threshold). Billing Tags: 0. Component avg: 33.3. **Important context:** The 100 score on Unresolved Ticket Age is a strict threshold application. The 7 pending tickets are predominantly bugs and feature requests parked in the development pipeline (filed to Jira), not customer-waiting-for-response situations. The framework doesn't distinguish between "customer waiting" and "development backlog" — this is a framework limitation. If the threshold were adjusted for dev-tracked tickets, the component would score ~0-8 instead of 33. |

---

## 4. Query Issues

| Query | Issue | Resolution |
|---|---|---|
| Mixpanel per-user activity | Case-sensitive usernames created apparent duplicates: `sc-ryanc` vs `SC-RYANC`, `SC-DianaH` vs `sc-dianah`, `PBE` vs `pbe`, `HR` vs `hr`, `SC-KellyM` vs `sc-kellym`, `sc-Beaut` vs `sc-beaut`, `sc-SavannaD` vs `sc-savannad`, `SC-ASHLEYWR` vs `sc-ashleywr`, `SC-TracyR`. | **Corrected via programmatic de-dup.** 59 raw usernames → **58 unique users** after `LOWER()` de-dup (verified via BigQuery `GROUP BY LOWER(username)`). Initial manual estimate of 52 was incorrect — I overcounted duplicate merges. 4 users (sc-mallorym, sc-tracyr, sc-paulad, sc-johnd) appear in Mixpanel but not in the CLM — likely added post-CLM export. Active User Ratio = 58/54 = 100%+. Scoring impact: none (already at 100 threshold). |
| Org_users billable count | `org_users` for org 87 returns 4,418 total — includes customer accounts with eCat Online access. Cannot distinguish rep accounts from customer accounts with this query alone. | Used CLM report (54 users) as billable user count. This is the Admin Console's canonical view of iPad app users. A more precise PostgreSQL approach would join org_users → users → user_types, but user_types schema was not verified. |
| Admin Orders Report scope | CSV filename says "Gabby Admin Orders Report" — exported from the `gh` admin console, covering all entities (Gabby, Summer Classics, SC Contract, SC Wholesale). | Cannot isolate SC-only orders from the CSV. Territory performance, order type, and AOV metrics are for the combined parent account. Mixpanel data filtered to `current_organization_shortname = 'scw'` is SC-specific. Noted in brief where metrics are combined vs. entity-specific. |
| CLM scope | CLM exported from `gh` admin — includes all 54 users across entities. SC-prefixed users (43) are Summer Classics reps; remaining 11 are Gabby/shared reps. | SC-prefixed users used for SC-specific rep analysis. Non-SC users (pbe, hr, rrobinson, etc.) also show up in scw Mixpanel data, confirming they sell across both brands. CLM feature counts include activity across all orgs, not just scw. |
| Stripe invoice `amount_paid` | All Stripe invoices show `amount_paid = 0` even for `status = 'paid'`. | Relied on `status` field rather than `amount_paid` for payment verification. May be a data sync timing issue in Weld pipeline. |
| HelpScout org name — **CRITICAL CORRECTION** | **Initial search for `%summer classic%` and `%gabby%` missed the primary org.** Tickets are filed under THREE different org names: (1) **"Gabriella White"** — 81 tickets, the primary org. (2) **null** — 31 tickets (email domain matches only). (3) **"SC Home/Gabby LLC"** — 2 tickets. The initial `LIKE '%gabby%'` matched "Gabby" but NOT "Gabriella." This one-word miss hid 81 tickets and led to a completely incorrect "0 tickets in 90 days" finding. **Corrected:** 14 tickets in 90d, 7 pending. Quarterly cadence: ~11-14/quarter since Q4 2024 (consistent). Primary filers: Jonah Tibbs (PIM Designer, 8 tickets) and Ben Erickson (VP IT, 6 tickets), both @gabriellawhite.com. Future queries MUST include `conv_customer_organization = 'Gabriella White'` as the primary filter. |
| Order volume: CSV vs Mixpanel vs PostgreSQL | CSV: 2,215 orders (all entities, Jan–Mar). Mixpanel scw: 1,839 (90d, iPad only). PostgreSQL org 87: 2,413 (90d, all origins). | Different scope explains differences. Mixpanel = iPad `order_submitted` events only. PostgreSQL = all orders including web. CSV = all entities combined. Used each source for its appropriate context and noted provenance. |

---

## 5. Framework Feedback

| Observation | Details |
|---|---|
| **Multi-entity accounts need explicit guidance** | The framework assumes one org = one brief. For Gabriella White (4 entities sharing an admin console, billing, and some reps), the Admin Console exports span all entities. The brief should clarify which metrics are entity-specific (Mixpanel, PostgreSQL) vs. parent-level (CLM, Orders Report, Stripe billing, **HelpScout**). Consider adding a "Multi-Entity Data Scope" note to the brief template. |
| **HelpScout org names are inconsistent and non-obvious** | **This was the single biggest data quality issue in this brief.** The same account family appears under three different HelpScout org names: "Gabriella White" (81 tickets), null (31 tickets), "SC Home/Gabby LLC" (2 tickets). A search for "Summer Classics" or "Gabby" misses the primary org "Gabriella White." The framework should require a HelpScout org name lookup as a prerequisite step, similar to the Mixpanel event name discovery step. Recommended addition: "Step 2.5: HelpScout Org Name Discovery — query `SELECT DISTINCT conv_customer_organization, COUNT(*) FROM helpscout__help_scout_tickets WHERE LOWER(conv_creator_email) LIKE '%[domain]%' GROUP BY 1` to identify all org names before running ticket analysis." |
| **Unresolved Ticket Age threshold doesn't distinguish ticket types** | The >30-day threshold scores 100 (critical) regardless of whether the ticket is an urgent customer-waiting issue or a feature request parked in the dev pipeline. For Gabriella White, 6 of 7 pending tickets are bugs/feature requests filed to Jira — they stay "pending" in HelpScout by design while being worked through development sprints. The scoring framework should consider adding a "ticket type" filter or a "customer wait time" metric alongside raw ticket age. |
| **Billable user count is ambiguous** | PostgreSQL `org_users` includes customer accounts. The CLM is the reliable source but isn't always available at query time. Framework should specify a PostgreSQL fallback for estimating billable users (e.g., join to user_types or filter by username patterns). |
| **Customer Activation Rate denominator may be inflated** | 8,281 total customers likely includes years of historical accounts. A "time-bounded" denominator (customers active in last 12 months, or customers imported in last 12 months) would produce a more actionable activation rate. The 8.6% figure is technically correct but may not reflect the true addressable customer base. |
| **Activity Ladder scoring from Mixpanel vs CLM** | The framework references Mixpanel for Activity Ladder but the CLM provides per-rep breakdowns with consistent naming. For the brief, I used Mixpanel for org-level event counts and CLM for per-rep analysis. The event name mapping (Appendix B) was essential for reconciling the two sources. |
| **Order revenue from CSV showed Jan→Feb decline** | Jan revenue ($3.96M) to Feb ($2.81M) = -29%, while order *count* increased (1,072 → 1,085). This is an AOV compression pattern. Since the CSV covers all entities, the revenue dip may be Gabby-specific or seasonal mix. The brief flags this but doesn't penalize scw since Mixpanel shows scw orders growing. |
| **Flipbook absence as expansion signal** | High PDF + No Flipbook is triggered, but Flipbook may not be relevant for all selling contexts. For outdoor furniture where reps visit dealer showrooms with iPad, PDF catalogs may genuinely be the preferred format. The expansion signal is valid but the business case needs in-conversation validation. |

---

## 6. CSV Data Usage

### CLM Report (`gh_2026-01-01_2026-03-02 (1).csv`)

| Metric Computed | Fields Used | Notes |
|---|---|---|
| Total licensed users (54) | All rows counted | Combined Gabby + SC users |
| SC-specific rep count (43) | Filtered by username starting with `sc-` | — |
| Activity Ladder per rep | Feature columns mapped to Ladder levels per Appendix B | CLM uses legacy PascalCase names (Search Products, Filter Products, etc.) which map to Appendix B legacy column |
| Feature Breadth per rep | Count of non-zero feature columns per user | Used for power user identification and enablement gap analysis |
| Submit Order counts per rep | "Submit Order" column | CLM counts span all orgs user accesses, not just scw |
| Login counts and frequency | "Logins" column | Used for CLM-based login frequency cross-validation |
| eCat Version Currency | "eCat Version" column | Most SC reps on 20260220 (current) or 20251107. A few on older versions (2025.3.3, 2025.4.1, 2025.4.3). No major version currency concern. |
| iPad Type distribution | "iPad Type" column | Range from iPad7,2 to iPad17,4. No parsing issues. |

### Admin Orders Report (`Gabby Admin Orders Report 2026-01-01 - 2026-03-03 (1).csv`)

| Metric Computed | Fields Used | Notes |
|---|---|---|
| Total orders (2,215) | All rows | Covers all entities under Gabby admin |
| AOV ($3,122.59) | Order Total / row count | All-entity combined. No entity-level filtering available in CSV. |
| Order Type breakdown | Order Type column | 87.3% Confirmed, 12.4% Quote, 0.3% TEST |
| Order Origin mix | Order Origin column | 64.2% iPad (empty = iPad app), 35.8% Website. Used for Digital Self-Service Rate. |
| Territory performance | Territory + Order Total columns | 12 named territories + some individual rep names as territory. South Team dominant at 36.8% of revenue. |
| Customer concentration | Customer Name + Order Total | 1,094 distinct customers. Top customer = 1.8% of revenue. |
| Monthly revenue breakdown | Order Date + Order Total | Jan: $3.96M, Feb: $2.81M, Mar: $146K (partial) |
| No parsing issues | — | CSV parsed cleanly with Python csv.DictReader. Some Order Total values = 0 (sample/swatch orders). Some Customer Number fields empty (unmatched customers). |

---

## 7. Scoring Summary

| Score | Value | Band | Quadrant Contribution |
|---|---|---|---|
| **Expansion Readiness** | 69 | Nurture (60–79) | High Expansion |
| **Retention Risk** | 11 | Low Risk (<30) | Low Risk |
| **Quadrant** | **GROW** | — | Ideal for EBR with expansion agenda |

**Score Change Log:**
- Expansion: 68 → 69 (+1). Days Since Last Interaction improved from 0 to 75 (28 days, not >90). HelpScout Responsiveness dropped from 75 to 25 (7 pending tickets). Net: Relationship Strength 50 → 58.
- Risk: 2 → 11 (+9). Unresolved Ticket Age: 0 → 100 (oldest pending 55 days). Repeated Issues: 0 → 25 (File Import Error appeared twice). Net: Relationship Cooling 0 → 33, Operational Deterioration 6 → 13.
- Quadrant unchanged: GROW.

**Scoring Confidence:** Medium. Engagement and operational data are strong and fresh. The primary uncertainties are: (1) **HelpScout attribution** — tickets are filed under the parent "Gabriella White" org and cannot be cleanly separated per entity. The 14 tickets may be partly attributable to other entities (gh, sccon, sc). (2) **Unresolved Ticket Age scoring** — the 100 score on the oldest pending ticket (55 days) applies the strict threshold, but these are dev-pipeline items, not customer-waiting situations. If contextually adjusted, Risk would drop to ~3. (3) **Fathom absence** — no direct meetings, though SC is discussed in internal SuperCat meetings. (4) **HubSpot deal linkage** — deals searched by name only; company-to-deal association unavailable through the BigQuery schema. (5) **AOV benchmark** — no portfolio-wide comparison available.

---

*Generated: March 3, 2026 | Author: Cursor/MCP automated brief generation*
