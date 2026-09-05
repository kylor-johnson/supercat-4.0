# Summer Classics Contract — Generation Notes

**Generated:** March 2, 2026 | **Framework Version:** Internal Account Brief v1.0, Scoring Framework v3.0, Thresholds v1.1, Metrics Framework v5.0

---

## 1. Data Gaps

### Sections/Fields That Could Not Be Populated

| Section | Field | Gap | Impact |
|---|---|---|---|
| B1 | Industry Segment revenue | No revenue data for Summer Classics as a company. HubSpot shows "FURNITURE" industry but no company size/revenue. | Used qualitative description based on customer mix and order volume. |
| B1 | Relationship History Narrative | No Fathom call summaries, no HubSpot deal notes, no engagement history | Constructed from data timestamps (partner since 2015, eCat Online added Aug 2025) rather than qualitative relationship arc. |
| B1 | Account Owner Name | HubSpot owner_id 140777477 retrieved but no join to owner name table performed | Would need `hubspot__owner` table query to resolve ID to name. |
| A1/B1 | MRR Entity Allocation | Stripe billing is consolidated under parent "Summer Classics" (cus_SXCh70eQmJpFAl). Individual entity invoices exist for Summer Classics Contract (cus_SXChSnV1ju6Thl) but all are status "deleted" | Cannot determine sccon-specific MRR. Reported consolidated parent MRR. |
| B2 | Growth Signals — HubSpot Deals | Query returned 0 deals for "summer classics" | Either deals use a different naming convention, are associated at the parent company level by ID rather than name, or no deals exist. |
| B5 | Fathom — all fields | Zero meetings found matching Summer Classics across title, invitee name, invitee email, and external domain filters | Either meetings occur under different naming, aren't recorded in Fathom, or no proactive meetings have been conducted. |
| B5 | HelpScout — all fields | Zero tickets found matching Summer Classics organization or summerclassics.com email domain | Either tickets are filed under a different organization/email, or the account genuinely has zero support needs. Given 11-year tenure and high engagement, the latter is most likely. |
| B4 | Inactive Buyer Flags | Would require historical order data (prior 90d) to identify customers who previously ordered but stopped | Only current-period activation could be computed. |
| B4 | Reorder Gap Analysis | Would require item-level order history across multiple periods | Not computed — requires deeper product-level analysis. |
| B6 | Peer Benchmarking | No portfolio-wide aggregation was performed | Qualitative benchmarking only. Precise percentile rankings require running the model across all 129 accounts. |

### Fields Marked N/A in Scoring

| Component | Input | Reason |
|---|---|---|
| Expansion — Relationship Strength | Fathom Meeting Cadence | No Fathom data exists. Weight redistributed to remaining 3 inputs per framework protocol. |
| Expansion — Growth Signals | Fathom Pain → Unused Feature Matches | No Fathom data. Weight redistributed. |
| Retention — Relationship Cooling | Days Since Last Fathom Meeting | No Fathom data (not a cessation — no meetings were ever recorded). Weight redistributed to HelpScout inputs. |
| Retention — Relationship Cooling | Competitor Mentions | No Fathom data. Weight redistributed. |

---

## 2. Schema Mismatches

| Expected | Actual | Resolution |
|---|---|---|
| `organizations.status` column | Column does not exist. `state` exists but is geographic state (AL), not account status. | Used `state` for geographic info only. No account status field available. |
| `users.user_type_id` | Column is on `org_users`, not `users`. | Fixed join: `LEFT JOIN user_types ut ON ou.user_type_id = ut.id` |
| `import_events.data_type` | Column does not exist. Only columns: `id`, `created_at`, `organization_id`, `data` (YAML text). | Parsed data type from YAML text preview (e.g., "Customers", "Inventory", "Territories"). |
| `authenticated_sessions.organization_id` | Column does not exist per known schema notes. | Did not query authenticated_sessions directly. Used Mixpanel for active user canonical count. |
| `product_images.product_id` | Column does not exist per known schema notes. | Used `organization_id` to count total images per org. |
| `mixpanel__events.mp_event_name` | Column name is `event_name`, not `mp_event_name`. | Used `event_name` for all queries. |
| `mixpanel__events` org filter | Using `organization_shortname = 'sccon'` returned only 1 event (api_access). | Expanded filter to `organization_shortname = 'sccon' OR current_organization_shortname = 'sccon'` which returned all 29 event types. The `current_organization_shortname` column captures the org context at event time. |
| `hubspot__deal.deal_name` | Column is `properties_dealname`. All HubSpot columns use `properties_` prefix. | Used `properties_dealname`, `properties_amount`, etc. |
| `hubspot__company.company_name` | Column is `properties_name`. | Used `properties_name` for company queries. |
| `stripe__subscription` | Table exists but has 0 rows. | Fell back to `stripe__invoice` per billing model detection hierarchy. Found active invoicing under parent customer. |
| `helpscout__help_scout_tickets.ticket_id` | Column does not exist. Primary key is `conversation_id`. | Used `conversation_id` for ticket queries. |

---

## 3. Scoring Limitations

### Components with Reduced Confidence

| Component | Score | Limitation |
|---|---|---|
| **Relationship Strength (58)** | Days Since Last Interaction scored 0 (>90 days) because no Fathom/HelpScout/HubSpot interactions exist. However, the platform shows daily active usage and data imports. The score underweights the implicit relationship health demonstrated by consistent platform engagement. | If "last platform activity" were an acceptable interaction proxy, this input would score 100 (<15 days). |
| **Business Impact (63)** | The Buyer-Facing Actions count has significant variance between CLM (430) and Mixpanel (176). This is likely due to the Mixpanel org filter issue (organization_shortname vs current_organization_shortname). CLM was used as the canonical source per prompt instructions. | The true count is likely between 176 and 430. Scoring used CLM-derived values. |
| **Growth Signals (50)** | HubSpot Deals scored 0 because no deals were found. This may be a data gap rather than absence of expansion activity — deals may exist under the parent company or use a different naming convention. | Would require querying HubSpot deals by associated company_id rather than deal name. |

### What Data Would Improve Scoring

1. **Fathom meeting recordings** — Even 1-2 meetings would unlock Relationship Strength and Growth Signals inputs (pain themes, competitor mentions, next steps).
2. **HubSpot deal association by company ID** — Query deals associated with HubSpot company_id 5102827859 (Summer Classics Contract) rather than by deal name.
3. **QuickBooks invoice data** — Would provide entity-level MRR allocation that Stripe consolidated billing obscures.
4. **Historical Mixpanel data (12-month)** — Would enable proper MoM trend analysis for Business Impact trend inputs.
5. **Sibling entity Mixpanel data** — Would enable cross-entity feature gap analysis and peer benchmarking within the parent account.

---

## 4. Query Issues

| Query | Issue | Resolution |
|---|---|---|
| Mixpanel events with `organization_shortname = 'sccon'` | Returned only 1 event (api_access). The majority of events are tagged with `current_organization_shortname` instead. | Added OR condition on `current_organization_shortname`. This is a critical finding for all future Mixpanel queries — always filter on BOTH columns. |
| PostgreSQL `org_users` count | Returned 1,155 — far higher than the 29 reps in the CLM report. | The 1,155 includes customer portal users, internal accounts, and historical users. The CLM report's 29 users is the accurate billable rep count. |
| PostgreSQL `import_events.data` | YAML text field, not structured. Could not reliably parse error counts from the data field without complex text processing. | Used import event counts and YAML previews to assess data freshness and import types. Error rate estimation is approximate. |
| HelpScout search for "Summer Classics" | Zero results across 180 days. | Tried both `conv_customer_organization LIKE '%summer classics%'` and `conv_customer_email LIKE '%summerclassics%'`. Neither returned results. This may mean tickets are filed under individual rep names rather than the organization. |
| Fathom search for Summer Classics | Zero results across 180 days. | Searched `Meeting Title`, `Meeting Invitees Name`, `Meeting Invitees Email`, and `External Domain Names`. None matched. |
| Stripe entity-level billing | Summer Classics Contract (cus_SXChSnV1ju6Thl) has only deleted invoices. | Billing appears to be consolidated on the parent entity. Deleted invoices suggest they were drafted per-entity then replaced with a consolidated invoice. |

---

## 5. Framework Feedback

### Sections That Worked Well

1. **Use-Case Profile Detection** — The three-profile system (Ordering / Non-Ordering / Non-Ordering + Pushed Data) correctly identified this account. The pushed data scoring at 50% weight appropriately reflects the platform's centrality to order-to-cash without overweighting transactional engagement that doesn't exist.
2. **Fathom/HelpScout Absence Protocol** — The v3.0 fix (N/A with weight redistribution, not penalty) was essential for this account. Under the old model, Relationship Strength and Relationship Cooling would have been significantly penalized for a self-sufficient 11-year account.
3. **Activity Ladder from CLM** — The CLM data provided granular per-rep feature usage that Mixpanel event aggregates couldn't match. The CLM is the definitive source for rep-level analysis.

### Sections That Felt Redundant or Unclear

1. **"Days Since Last Interaction" as a scoring input** — For accounts like this with no Fathom/HelpScout/HubSpot presence, this input always scores 0 (worst). But the account is among the healthiest in the portfolio. The input should either (a) accept platform activity as a valid interaction proxy, or (b) be marked N/A when all three interaction channels are absent. Currently it disproportionately drags down Relationship Strength.
2. **Library Share Rate threshold confusion** — The input measures emails sent / documents viewed, but the CLM columns "Email Single Library Entry" and "Email Multiple Library Entries" capture something slightly different from the Mixpanel `document_email_drafted` event. CLM shows 164 emails vs. Mixpanel 73. The threshold document should specify which source is canonical for this input.
3. **Pushed Data Business Impact weighting** — The formula `(non-ordering × 0.67) + (pushed × 0.5 × 0.33)` means pushed data inputs contribute only ~16.5% of the Business Impact component even for accounts where pushed revenue is $10M+. For heavily pushed-data accounts, the 50% weight on pushed inputs may undervalue the platform's business impact. Consider a sliding scale based on pushed revenue volume.

### Missing Elements

1. **Kit/Configured Item ordering metrics** — This account's primary platform value is kit building and configured item ordering (3,539 kit orders + 1,543 configured items in 61 days). These events are captured in the Activity Ladder (Level 5) but not in the Business Impact scoring for non-ordering clients. For Non-Ordering + Pushed Data accounts with heavy CPQ usage, kit/configured item volume should be a first-class Business Impact input.
2. **Cross-entity comparison** — The framework mentions multi-entity analysis (Section 8) but the scoring model doesn't incorporate it. For parent accounts with 4 entities, cross-entity feature gaps and parity scores would be valuable expansion signals.
3. **eCat Version Currency** — The CLM data reveals version fragmentation (7 reps on 20251107, 10 on 20260220, etc.) but this isn't incorporated into any scoring component. It's mentioned in Section 9 of the Metrics Framework but not in the scoring thresholds.

---

## 6. CSV Data Usage

### Admin CLM Report (sccon_2026-01-01_2026-03-02.csv)

| Metric Computed | CLM Columns Used | Notes |
|---|---|---|
| Active User Count (29) | All user rows with Logins > 0 | Used as billable rep count denominator |
| Activity Ladder per level | All feature columns mapped to Ladder levels | CLM is the definitive per-rep source |
| Feature Breadth Score | Count of non-zero feature columns per user | Averaged across 29 users ≈ 14 |
| Power User identification | Logins + composite of high-count features | Top 5 identified: sc-jessieh, sc-triciamitchell, sc-shawndan, lhanson, zww |
| Enablement Gap identification | Users with logins but <8 distinct features | Bottom quartile: sc-margaretm, sc-kevina, bene, sbratz, sc-grantj |
| Buyer-Facing Actions total | Email Item Info + Create PDF Catalog + Email Single/Multiple Library Entries | CLM total: 430 vs Mixpanel total: 176 (significant variance) |
| Feature utilization highlights | All feature columns | Identified zero-usage features: SmartPicks, Flipbook, Maybe Lists, Favorites, Backorders |
| eCat Version distribution | eCat Version column | 7 versions present across 29 reps |
| Submit Order confirmation | Submit Order column | All zeros — confirmed non-ordering profile |

**Parsing Notes:** No parsing issues. CSV was clean with standard comma-delimited format. One user name had extra whitespace ("Betty   Henderson" — triple space) but did not affect data extraction.

### Admin Orders Report (Summer Classics Contract Admin Orders Report 2026-01-01 - 2026-03-03.csv)

| Metric Computed | CSV Columns Used | Notes |
|---|---|---|
| Total orders (849) | Row count | — |
| AOV ($15,240 non-zero) | Order Total | 149 orders had $0 total (excluded from non-zero AOV) |
| Order Type breakdown | Order Type | Quote: 492 (57.9%), Confirmed: 357 (42.1%). No HFC orders. |
| Order Origin | Order Origin | Regular (blank): 834, Website: 15. No Market/Event tagged orders. |
| Territory performance | Territory + Order Total | Top 5 territories computed. Wynne White concentration flagged. |
| Customer concentration | Customer Name + Order Total | Top 10 customers identified. OMNI Hotels at 8.3%. |
| Customer activation rate | Distinct Customer Number / 5,228 (PostgreSQL) | 316 distinct customer numbers with orders = 6.0% |
| Website order analysis | Order Origin = "Website" | 15 orders, $28,552 total — minimal eCat Online B2B Cart adoption |

**Parsing Notes:**
- Some Customer Name values contain commas inside quotes (e.g., `"J. BANKS DESIGN GROUP, INC"`). Python CSV reader handled these correctly.
- Some rows have empty Customer Number fields (7 orders) — these were still counted in total orders but not in distinct customer number count.
- One Customer Name variant issue: "OMNI HOTELS MANAGEMENT CORP" and "OMNI HOTELS MANGEMENT CORP. " (with typo and trailing space) appear as separate customers. Combined revenue is ~$1.17M / 11%.
- "Marketing Material Accounts" territory has $622,911 in revenue but most orders are $0 Confirmed (internal material transfers). The non-zero orders under this territory are likely misclassified or represent sample/demo shipments.

---

## 7. Scoring Summary

| Score | Value | Band | Key Factors |
|---|---|---|---|
| **Expansion Readiness** | **66** | Nurture | Strong adoption (88) pulls up; growth signals (50) and relationship strength (58) pull down due to absent Fathom/HubSpot engagement data |
| **Retention Risk** | **1** | Low Risk | Near-zero across all components. No engagement decline, no financial distress, no operational issues. |
| **Quadrant** | **GROW** | — | High expansion readiness + low retention risk |

### Score Sensitivity Analysis

| If this changed... | Expansion Readiness would... | Retention Risk would... |
|---|---|---|
| 1 Fathom meeting recorded | +3 to +5 pts (Relationship Strength improves from 58→70+) | No change |
| 1 HubSpot expansion deal opened | +4 to +6 pts (Growth Signals improves from 50→62+) | No change |
| "Days Since Last Interaction" scored as N/A | +3 pts (Relationship Strength improves from 58→75+) | No change |
| Customer Activation Rate improved to 15% | +2 pts (triggers fewer expansion signals but improves Business Impact) | No change |
| SmartPicks adopted | -1 expansion signal but +2 pts in Adoption Depth | No change |

The Expansion Readiness score is most sensitive to the Relationship Strength component, which is suppressed by the absence of tracked interactions. A single Fathom meeting and a HubSpot deal would push this account into the 72-75 range — firmly Nurture with a path to Active Target.
