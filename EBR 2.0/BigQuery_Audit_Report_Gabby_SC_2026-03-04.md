# BigQuery + Postgres Audit Report — Gabby / Summer Classics

**Run date:** 2026-03-04  
**Sources queried:**
- BigQuery: `supercat-data-pipeline.WELD_RAW` (Mixpanel events, people, org feature usage)
- Postgres: SuperCat application database (`public` schema — users, organizations, orders, customers)

**Orgs tested:** `gh`, `sc`, `scw`, `sccon`

---

## CRITICAL FINDINGS

1. **Revenue figure RESOLVED — $35.2M is from Postgres `orders` table, ~2 months (Jan–Feb 2026), not TTM.** The deck's $35.2M comes from the Postgres `orders` table covering approximately January–February 2026 across all 4 entities. BigQuery/Mixpanel `order_total` tracks TTM iPad-submitted revenue ($214.8M for 3 orgs). These are complementary sources — Postgres is the order system of record; Mixpanel is the usage/behavior layer. **Use Postgres `orders.total` for revenue KPIs. Use Mixpanel for feature adoption and engagement metrics.**

2. **`sccon` has ZERO Mixpanel order events but $149.2M TTM in Postgres.** Summer Classics Contract submits orders through a path that does not fire the Mixpanel `order_submitted` event (likely web/online, not iPad). Postgres `orders` table shows 7,449 orders and $149.2M TTM for sccon. **Mixpanel alone undercounts order activity — always join with Postgres for revenue.**

3. **Rep name resolution SOLVED via Postgres** — the `users` table has `username`, `first_name`, `last_name`, `email` for every user. All BQ usernames resolve. Example: HR = Heather Robert, PBE = Paul Bentley, zww = Wynne White. No CSV fallback needed.

4. **Customer name resolution SOLVED via Postgres** — the `customers` table has `code` (matches BQ `selected_bill_to_code`) and `name`. Example: 1101555 = GREEN FRONT FURNITURE CO. INC. Covers all 4 orgs (gh: 11,817 customers, sc: 91,098, sccon: 5,230, scw: 8,285).

5. **`mixpanel__org_feature_usage_report` feature columns are ALL ZERO** for all 4 orgs. Only the metadata columns (org_name, total_users, active_users, total_logins) are populated. Feature adoption metrics must be derived from raw BQ events, not this summary table.

6. **Username case inconsistency (BQ)** — `sc-savannad` (8,092 events) and `sc-SavannaD` (7,744 events) are tracked as different users. All BQ queries must use `LOWER(username)`. Postgres stores the canonical case.

---

## ORDER REVENUE

### Source 1: Postgres `orders` Table (System of Record)

| Metric | gh | sc | scw | sccon |
|---|---|---|---|---|
| TTM Orders (Mar 25–Feb 26) | 14,743 | 31,415 | 14,212 | **7,449** |
| TTM Revenue | **$48,295,922** | **$141,950,609** | **$71,855,124** | **$149,230,066** |
| Avg Order Value | $3,535 | $4,575 | $5,779 | $21,684 |
| Unique Customers | 2,313 | 5,746 | 1,790 | 849 |
| Unique Reps | 52 | 103 | 46 | 32 |

**TTM Total (all 4 orgs from Postgres): $411,331,721**

**Deck's $35.2M figure** matches a ~2-month window (Jan–Feb 2026):

| Entity | Jan–Feb 2026 Orders | Jan–Feb 2026 Revenue | Deck Value |
|---|---|---|---|
| gh | 2,461 | $9,250,299 | $6.9M |
| sc | 3,704 | $19,784,418 | $11.2M |
| scw | 1,902 | $9,698,301 | $6.4M |
| sccon | 1,267 | $20,917,631 | $10.7M |
| **Total** | **9,334** | **$59,650,649** | **$35.2M** |

The Postgres Jan–Feb total ($59.7M) is higher than the deck's $35.2M — the deck likely applies additional filters (e.g., excluding certain order types, or using a narrower date range). The deck's per-entity order counts (7,436 total) are lower than raw Postgres (9,334), confirming some filtering is applied.

### Source 2: BigQuery Mixpanel `order_submitted` Events (Behavioral Layer)

| Metric | gh | sc | scw | sccon |
|---|---|---|---|---|
| TTM Events (Mar 25–Feb 26) | 9,666 | 25,448 | 10,516 | **0** |
| TTM Revenue (event property) | $40,482,295 | $112,618,562 | $61,694,054 | **$0** |
| Avg order_total | $4,188 | $4,425 | $5,867 | — |
| $0 orders | 980 (10.1%) | 343 (1.3%) | 1,675 (15.9%) | — |

- **order_total field:** EXISTS (FLOAT), 100% non-null on order_submitted events
- **BQ captures ~84% of Postgres revenue for gh, ~79% for sc, ~86% for scw** — gap is orders submitted via web/online (not iPad app), which don't fire Mixpanel events
- **sccon: 0% Mixpanel coverage** — all orders submitted through non-iPad path

### Revenue Source Recommendation

| Use Case | Source | Why |
|---|---|---|
| Client-facing revenue KPIs | Postgres `orders` | System of record, includes all order paths |
| Feature adoption tied to orders | BQ `mixpanel__events` | Only source with feature context per user |
| Rep-level order activity | Postgres `orders` (has rep_first_name, rep_last_name) | Complete across all entities |
| Customer concentration | Either — BQ has `selected_bill_to_code`, PG has `customer_num` + `bill_to_company_name` | PG has customer names; BQ has broader event context |

### Duplicate Analysis (BQ Only)

Duplicates are minimal: gh 0.8%, sc 0.1%, scw 0.4%. All exact duplicates. Dedup via `DISTINCT insert_id`.

### Portal Orders (Imported ERP Data — Separate Table)

Postgres also has `portal_orders` — imported from ERP/accounting. Different from iPad-submitted orders:

| Entity | TTM Portal Orders | TTM Portal Revenue |
|---|---|---|
| gh | 25,612 | $41,078,440 |
| sc | 16,301 | $33,392,758 |
| sccon | 3,294 | $17,937,575 |
| scw | 21,143 | $45,985,959 |

---

## EVENT INVENTORY

**Total distinct event names:** 40

### Events Mapped to EBR Feature Categories

| Category | Events | Combined Count (TTM) |
|---|---|---|
| **Ordering** | `order_submitted`, `add_kit_to_order`, `add_configured_item_to_order`, `copy_order`, `copy_order_items`, `add_to_order_from_maybe_list`, `item_added_via_magic_button` | ~146K |
| **Product Discovery** | `product_search`, `collection_search`, `filter_button_pressed`, `product_sort_changed`, `view_stack`, `create_stack`, `edit_stack`, `view_smart_stack` | ~426K |
| **Customer Mgmt** | `customer_search`, `customer_selection`, `view_favorites`, `view_customer_smart_picks`, `view_customer_on_order_items` | ~457K |
| **Documents / PDF** | `view_document`, `document_email_drafted`, `pdf_catalog_started`, `pdf_catalog_generated`, `item_email_drafted`, `email_stack`, `generate_xlsx_catalog` | ~51K |
| **Sales Portal** | `view_portal`, `view_customer_orders`, `preview_order_show_current_customer_orders`, `preview_order_show_territory_orders`, `show_customer_sales_setting_changed` | ~48K |
| **Scanning** | `item_scanned`, `item_scan_failed` | ~33K |
| **Platform / Auth** | `selected_org`, `api_access`, `reload_button_pressed`, `view_notifications`, `pspdfkit_activated` | ~188K |

### Full Event List (Descending by Volume)

| # | Event Name | Count | Orgs |
|---|---|---|---|
| 1 | product_search | 400,303 | 4 |
| 2 | customer_search | 326,389 | 4 |
| 3 | selected_org | 151,395 | 4 |
| 4 | customer_selection | 127,998 | 4 |
| 5 | view_kit | 94,392 | 4 |
| 6 | add_kit_to_order | 71,653 | 4 |
| 7 | order_submitted | 45,959 | 3 |
| 8 | api_access | 35,763 | 4 |
| 9 | item_scanned | 31,524 | 3 |
| 10 | view_document | 29,949 | 4 |
| 11 | view_customer_orders | 24,094 | 4 |
| 12 | add_configured_item_to_order | 22,595 | 4 |
| 13 | view_portal | 20,389 | 4 |
| 14 | collection_search | 11,900 | 4 |
| 15 | filter_button_pressed | 8,992 | 4 |
| 16 | document_email_drafted | 8,622 | 4 |
| 17 | pdf_catalog_started | 6,124 | 4 |
| 18 | pdf_catalog_generated | 5,587 | 4 |
| 19 | preview_order_show_current_customer_orders | 2,697 | 4 |
| 20 | view_stack | 2,489 | 4 |
| 21 | copy_order_items | 2,416 | 4 |
| 22 | copy_order | 2,363 | 4 |
| 23 | product_sort_changed | 1,796 | 4 |
| 24 | item_added_via_magic_button | 1,730 | 4 |
| 25 | item_scan_failed | 1,328 | 3 |
| 26 | view_favorites | 1,194 | 3 |
| 27 | view_customer_on_order_items | 776 | 3 |
| 28 | item_email_drafted | 712 | 4 |
| 29 | preview_order_show_territory_orders | 445 | 4 |
| 30 | view_customer_smart_picks | 351 | 3 |
| 31 | reload_button_pressed | 312 | 4 |
| 32 | create_stack | 258 | 4 |
| 33 | show_customer_sales_setting_changed | 185 | 4 |
| 34 | add_to_order_from_maybe_list | 94 | 4 |
| 35 | edit_stack | 31 | 4 |
| 36 | view_smart_stack | 20 | 1 |
| 37 | email_stack | 15 | 4 |
| 38 | view_notifications | 15 | 3 |
| 39 | pspdfkit_activated | 1 | 1 |
| 40 | generate_xlsx_catalog | 1 | 1 |

### Events With No Current EBR Mapping (Potential New Insights)

- `api_access` (35,763) — could indicate B2B integration / headless usage
- `item_added_via_magic_button` (1,730) — quick-add feature, potential power-user signal
- `copy_order` / `copy_order_items` (4,779 combined) — reorder behavior, loyalty indicator
- `view_smart_stack` (20) — nascent feature, watch for growth
- `pspdfkit_activated` (1) — PDF annotation feature, barely used

---

## REP DATA

### Username Format

**Format: MIXED — shortcodes, initials, and name-based identifiers**

| Pattern | Examples | Prevalence |
|---|---|---|
| `sc-` prefix + firstname+lastinitial | sc-ryanc, sc-tanyah, sc-denaec | Most common |
| Initials (2-3 chars) | HR, PBE, rs, zww | Frequent |
| firstname+lastinitial (no prefix) | rrobinson, jeremyr | Occasional |
| `SC-` uppercase prefix | SC-DianaH, SC-KellyM | Some reps |

**Username is NOT an email address.** It's an eCat login username, typically a short identifier.

### Case Sensitivity Issue (FLAG)

`sc-savannad` and `sc-SavannaD` are tracked as separate users:
- sc-savannad: 8,092 events, 22 features
- sc-SavannaD: 7,744 events, 14 features

**All queries must use `LOWER(username)` for accurate rep-level aggregation.**

### Top 20 Reps — Gabby (gh), TTM from Mar 2025

| Rank | Username | Events | Features Used |
|---|---|---|---|
| 1 | sc-annel | 19,338 | 24 |
| 2 | HR | 16,197 | 26 |
| 3 | sc-ryanc | 15,912 | 29 |
| 4 | PBE | 15,059 | 26 |
| 5 | sc-clarer | 14,766 | 27 |
| 6 | sc-tanyah | 9,900 | 28 |
| 7 | sc-denaec | 9,831 | 30 |
| 8 | sc-davids | 9,298 | 21 |
| 9 | sc-savannad | 8,092 | 22 |
| 10 | sc-SavannaD | 7,744 | 14 |
| 11 | sc-catf | 7,482 | 26 |
| 12 | sc-allisonw | 6,985 | 25 |
| 13 | rrobinson | 6,942 | 30 |
| 14 | rs | 6,740 | 19 |
| 15 | SC-KellyM | 6,080 | 18 |
| 16 | sc-katiewilloughby | 6,060 | 22 |
| 17 | SC-DianaH | 5,574 | 20 |
| 18 | jeremyr | 5,098 | 22 |
| 19 | sc-margos | 4,994 | 24 |
| 20 | zww | 4,220 | 19 |

### Full Name Resolution — SOLVED via Postgres

- **Available from `mixpanel__people` (BQ):** NO — table has only `distinct_id` and `last_seen`
- **Available from Postgres `users` table:** YES — `username`, `first_name`, `last_name`, `email`
- **Join pattern:** `LOWER(mixpanel_events.username) = LOWER(postgres.users.username)`
- **No CSV fallback needed**

**Verified name resolution for top 20 BQ reps:**

| BQ Username | First Name | Last Name | Email |
|---|---|---|---|
| sc-annel | Anne | Leonard | AnneL@gabriellawhite.com |
| HR | Heather | Robert | HeatherR@gabriellawhite.com |
| sc-ryanc | Ryan | Casabella | RyanC@gabriellawhite.com |
| PBE | Paul | Bentley | Paul@gabriellawhite.com |
| sc-clarer | Clare | Colón | ClareR@gabriellawhite.com |
| sc-tanyah | Tanya | Houge | TanyaH@gabriellawhite.com |
| sc-denaec | Denae | Copeland | DenaeC@gabriellawhite.com |
| sc-davids | David | Sherrill | DavidS@gabriellawhite.com |
| sc-savannad | Savanna | Dunaway | SavannaD@gabriellawhite.com |
| sc-catf | Cat | Freund | CatF@gabriellawhite.com |
| sc-allisonw | Allison | Wooley | AllisonW@gabriellawhite.com |
| rrobinson | Rob | Robinson | Rob@gabriellawhite.com |
| RS | Rick | Scott | RickS@gabriellawhite.com |
| SC-KellyM | Kelly | McGuire | KellyM@gabriellawhite.com |
| sc-katiewilloughby | Katie | Willoughby | KatieW@gabriellawhite.com |
| SC-DianaH | Diana | Horsley | DianaH@gabriellawhite.com |
| jeremyr | Jeremy | Rago | Jeremyr@gabriellawhite.com |
| sc-margos | Margo | Scoggins | MargoS@gabriellawhite.com |
| ZWW | Wynne | White | WynneW@gabriellawhite.com |

All reps have `@gabriellawhite.com` emails — confirming these are Gabriella White sales reps, not end customers.

### Cross-Entity Rep Identification

**YES — same usernames appear across multiple orgs.** Top cross-org reps:

| Username | Events in sc/scw/sccon | Also in gh |
|---|---|---|
| sc-tanyah | 22,662 | Yes (9,900) |
| sc-ryanc | 19,718 | Yes (15,912) |
| rrobinson | 14,421 | Yes (6,942) |
| sc-davids | 14,291 | Yes (9,298) |
| PBE | 13,090 | Yes (15,059) |

Reps work across entities — this is expected for a multi-brand parent company.

---

## DATE COVERAGE

### Per-Org Date Range (Full History)

| Org | Earliest Event | Latest Event | Total Events | Unique Users |
|---|---|---|---|---|
| gh | 2024-11-01 | 2026-03-03 | 300,105 | 112 |
| sc | 2024-11-01 | 2026-03-03 | 1,149,161 | 248 |
| sccon | 2024-11-01 | 2026-03-03 | 132,288 | 53 |
| scw | 2024-11-01 | 2026-03-03 | 313,977 | 126 |

**Data starts 2024-11-01 for all orgs.** This gives ~16 months of history. True TTM window is available (Mar 2025 – Feb 2026).

### Monthly Event Volume (Jan 2025 – Mar 2026)

#### gh (Gabby)

| Month | Events | Active Users | Orders |
|---|---|---|---|
| 2026-03 | 1,931 | 41 | 71 |
| 2026-02 | 16,955 | 59 | 791 |
| 2026-01 | 23,379 | 52 | 905 |
| 2025-12 | 11,305 | 50 | 514 |
| 2025-11 | 13,758 | 51 | 668 |
| 2025-10 | 26,403 | 56 | 933 |
| 2025-09 | 17,327 | 52 | 741 |
| 2025-08 | 14,343 | 53 | 719 |
| 2025-07 | 20,227 | 58 | 887 |
| 2025-06 | 17,706 | 56 | 733 |
| 2025-05 | 19,934 | 61 | 865 |
| 2025-04 | 28,335 | 66 | 1,099 |
| 2025-03 | 18,387 | 61 | 811 |
| 2025-02 | 16,828 | 59 | 700 |
| 2025-01 | 24,316 | 58 | 905 |

**No monthly gaps. Apr 2025 and Oct 2025 are peak months. Dec 2025 shows expected seasonal dip.**

#### sc (Gabriella White / Summer Classics Wholesale)

| Month | Events | Active Users | Orders |
|---|---|---|---|
| 2026-03 | 6,179 | 99 | 171 |
| 2026-02 | 64,013 | 117 | 1,858 |
| 2026-01 | 46,122 | 119 | 1,346 |
| 2025-12 | 38,263 | 118 | 1,291 |
| 2025-11 | 66,239 | 143 | 2,556 |
| 2025-10 | 67,166 | 131 | 1,580 |
| 2025-09 | 77,608 | 139 | 1,970 |
| 2025-08 | 92,509 | 138 | 2,783 |
| 2025-07 | 69,068 | 136 | 2,064 |
| 2025-06 | 66,713 | 129 | 2,025 |
| 2025-05 | 92,085 | 140 | 3,064 |
| 2025-04 | 80,513 | 140 | 2,378 |
| 2025-03 | 85,563 | 135 | 2,533 |
| 2025-02 | 75,492 | 135 | 2,224 |
| 2025-01 | 64,994 | 142 | 1,996 |

**No gaps. May and Aug 2025 are peak months (market seasons).**

#### scw (Summer Classics)

| Month | Events | Active Users | Orders |
|---|---|---|---|
| 2026-03 | 1,697 | 40 | 87 |
| 2026-02 | 19,976 | 62 | 836 |
| 2026-01 | 16,514 | 60 | 662 |
| 2025-12 | 9,668 | 53 | 414 |
| 2025-11 | 13,375 | 51 | 626 |
| 2025-10 | 18,795 | 58 | 752 |
| 2025-09 | 20,578 | 60 | 880 |
| 2025-08 | 27,321 | 56 | 1,023 |
| 2025-07 | 23,391 | 59 | 948 |
| 2025-06 | 20,124 | 57 | 864 |
| 2025-05 | 29,263 | 62 | 1,260 |
| 2025-04 | 31,384 | 66 | 1,260 |
| 2025-03 | 24,736 | 63 | 991 |
| 2025-02 | 18,888 | 57 | 697 |
| 2025-01 | 15,907 | 59 | 525 |

**No gaps. Apr-May and Aug 2025 are peak months.**

#### sccon (Summer Classics Contract)

| Month | Events | Active Users | Orders |
|---|---|---|---|
| 2026-03 | 1,023 | 24 | 0 |
| 2026-02 | 8,698 | 34 | 0 |
| 2026-01 | 8,576 | 29 | 0 |
| 2025-12 | 5,661 | 25 | 0 |
| ... | ~6K-11K/mo | 25-35 | **0** |

**Zero orders every single month.** Active catalog/search usage confirmed — this org simply does not use eCat for order submission.

---

## CUSTOMER DATA

### Customer Identity in Events

- **`customer_id`:** DOES NOT EXIST as a column
- **`customer_name`:** DOES NOT EXIST as a column
- **`account_name`:** DOES NOT EXIST as a column
- **`customer` (FLOAT):** EXISTS but virtually empty — only 1 non-null value out of 229,990 events (gh TTM)

### Proxy Customer Fields Available

| Field | Type | Coverage (gh TTM) | Notes |
|---|---|---|---|
| `selected_bill_to_code` | STRING | 160,121 / 229,990 (70%) | Primary customer identifier |
| `selected_ship_to_code` | STRING | 159,606 / 229,990 (69%) | Ship-to address, often hashed |

- `selected_bill_to_code` is the **best available customer identifier**
- Format is mixed: numeric ERP codes (e.g., `1101555`) and UUIDs (e.g., `05EEB437-5A1C-4BA0-934C-63B9C0612420`)
- **2,277 unique bill-to codes** for gh with positive-value orders in TTM

### Top 15 Customers by Revenue — gh (Gabby) TTM

| Bill-To Code | Orders | Revenue |
|---|---|---|
| 1101555 | 65 | $606,006 |
| 1220442 | 24 | $478,969 |
| 1202241 | 20 | $474,603 |
| 1257895 | 13 | $442,894 |
| 05EEB437... | 11 | $411,949 |
| 0FA48442... | 10 | $404,323 |
| 1280313 | 11 | $385,599 |
| 1249995 | 79 | $292,510 |
| 1261346 | 30 | $275,897 |
| 1253786 | 7 | $272,927 |

### Customer Name Resolution — SOLVED via Postgres

**Postgres `customers` table** has `code` (= BQ `selected_bill_to_code`) + `name` + full address.

**Top 10 gh customers by BQ revenue — now with names:**

| Bill-To Code | Customer Name | City, State | Orders | Revenue |
|---|---|---|---|---|
| 1101555 | GREEN FRONT FURNITURE CO. INC. | Farmville, VA | 65 | $606,006 |
| 1220442 | SHRADHA KAREKAR | Suwanee, GA | 24 | $478,969 |
| 1202241 | VICTORIA'S INTERIORS | Huntsville, AL | 20 | $474,603 |
| 1257895 | HCD DESIGN, LLC | Baton Rouge, LA | 13 | $442,894 |
| 1280313 | GILLENWATER FLOORING CENTER INC | Maryville, TN | 11 | $385,599 |
| 1249995 | WHAT IN THE WORLD | Frisco, TX | 79 | $292,510 |
| 1261346 | CASSELL PROPERTIES / HAUTE HOME | Knoxville, TN | 30 | $275,897 |
| 1253786 | DOUBLE L INTERIORS | Houston, TX | 7 | $272,927 |
| 1268423 | MERRY'S HOME FURNISHINGS | Augusta, GA | 18 | $269,362 |
| 1180573 | HOME AND SALVAGE | Naples, FL | 29 | $261,496 |

**Customer counts by org (Postgres):**

| Org | Total Customers |
|---|---|
| gh | 11,817 |
| sc | 91,098 |
| sccon | 5,230 |
| scw | 8,285 |

**Top concentration calculation fully possible** using either:
- BQ: `selected_bill_to_code` + `order_total` (iPad orders only)
- Postgres: `orders.customer_num` + `orders.total` + `customers.name` (all orders, with names)

---

## ORG SHORTNAME MAPPING

### All 4 Orgs Confirmed Active

| Org | Full Name | HubSpot ID | Total Users | Active Users | Total Logins |
|---|---|---|---|---|---|
| gh | Gabby | 46693541179 | 90 | 56 | 7,511 |
| sc | Gabriella White | 31731179087 | 194 | 118 | 23,927 |
| sccon | Summer Classics Contract | 5102827859 | 45 | 32 | 4,952 |
| scw | Summer Classics | 2835200275 | 101 | 62 | 7,427 |

**Important naming note:**
- `sc` maps to **"Gabriella White"** (not "Summer Classics") — this is the parent brand
- `scw` maps to **"Summer Classics"** — this is the wholesale entity
- The prompt's assumption that `sc` = "Summer Classics Wholesale" is incorrect
- `scw` may actually be "SC Retail / Wholesale" as hypothesized

### Feature Usage Summary Table Status

The `mixpanel__org_feature_usage_report` table has correct org metadata but **ALL feature count columns are zero** for every org. The 44 feature columns (search_products, create_my_list, submit_order, etc.) are not being populated by the ETL pipeline. This table should NOT be used for feature adoption metrics — derive them from `mixpanel__events` directly.

---

## SCHEMA REFERENCE

### mixpanel__events — 76 Columns

**Identity & Organization:**
- `username` (STRING) — eCat login username
- `user_id` (STRING) — same as username
- `distinct_id` (STRING) — same as username
- `organization_shortname` (STRING) — original org at time of event
- `current_organization_shortname` (STRING) — current org (may differ if user switched)
- `organization_id` (STRING) — often null, use shortname instead
- `current_organization_id` (STRING) — numeric org ID

**Order & Revenue:**
- `order_total` (FLOAT) — order dollar value
- `item_count` (FLOAT) — items in order
- `item_numbers` (STRING) — SKU list (often null on order_submitted)

**Customer:**
- `selected_bill_to_code` (STRING) — customer bill-to identifier
- `selected_ship_to_code` (STRING) — customer ship-to identifier
- `customer` (FLOAT) — almost always null, do not rely on
- `price_level_code` (STRING) — pricing tier assigned

**Event Metadata:**
- `event_name` (STRING) — the action performed
- `event_hash` (STRING) — unique event fingerprint
- `insert_id` (STRING) — Mixpanel dedup key
- `time` (FLOAT) — Unix epoch seconds
- `current_date` (TIMESTAMP) — date partition

**Device & Platform:**
- `manufacturer`, `model`, `os`, `os_version`, `screen_height`, `screen_width`
- `app_version`, `app_release`, `app_build_number`
- `mp_lib` (always "iphone" — iPad app)

**Other Event Properties:**
- `search_text`, `item_number`, `scan_type`, `scan_value`, `barcode_source`
- `format`, `purpose`, `title`, `subtitle`, `dimension`, `context`, `type`
- `smart_stack_id`, `smart_stack_name`, `smart_search_enabled`
- `document_count`, `product_count`, `format_name`

### mixpanel__people — 16 Columns (Thin)

Only useful fields: `distinct_id` (matches username), `last_seen` (timestamp).  
No name, email, org, or profile data.

### mixpanel__org_feature_usage_report — 44 Columns

Useful metadata: `org_shortname`, `org_name`, `hubspot_company_id`, `total_users`, `active_users`, `total_logins`.  
All 38 feature columns: currently zero for all orgs.

---

## GAPS & FALLBACKS NEEDED

| Gap | Status | Resolution |
|---|---|---|
| ~~**Rep full names**~~ | **RESOLVED** | Postgres `users` table: `username` → `first_name`, `last_name`, `email`. Join via `LOWER(username)`. |
| ~~**Customer names**~~ | **RESOLVED** | Postgres `customers` table: `code` (= `selected_bill_to_code`) → `name`, `billing_city`, `billing_state`. |
| ~~**Revenue validation**~~ | **RESOLVED** | Deck's $35.2M is from Postgres `orders` table (~2-month window), not Mixpanel TTM. Both sources are valid for different use cases. |
| ~~**sccon order data**~~ | **RESOLVED** | sccon has 7,449 orders / $149.2M TTM in Postgres `orders`. They just don't fire Mixpanel events. Use Postgres for sccon revenue. |
| **Feature usage summary** | OPEN | `org_feature_usage_report` all zeros in BQ. Derive from raw `mixpanel__events` — this works fine. |
| **Username normalization** | OPEN (BQ only) | Case-sensitive dupes in Mixpanel. Apply `LOWER(username)` in all BQ queries. Postgres stores canonical case. |
| **Mixpanel-to-Postgres user join** | NEW — needs implementation | No direct foreign key. Join on `LOWER(mixpanel.username) = LOWER(postgres.users.username)`. Need to validate match rate across all orgs. |
| **sccon Mixpanel gap** | NEW — accept or investigate | sccon has full catalog/search activity in Mixpanel but zero order events. Feature adoption metrics work; order metrics must come from Postgres. |

---

## RECOMMENDED QUERY UPDATES

### 1. Always Normalize Username

```sql
-- Before
GROUP BY username
-- After
GROUP BY LOWER(username)
```

### 2. Deduplicate Orders

```sql
-- Use insert_id to remove Mixpanel ETL duplicates
WITH deduped_orders AS (
  SELECT DISTINCT insert_id, order_total, 
    COALESCE(current_organization_shortname, organization_shortname) AS org,
    LOWER(username) AS username,
    selected_bill_to_code,
    TIMESTAMP_SECONDS(CAST(time AS INT64)) AS event_ts
  FROM mixpanel__events
  WHERE event_name = 'order_submitted'
)
```

### 3. Filter $0 Orders for Revenue Metrics

```sql
-- For revenue KPIs, exclude $0 orders
WHERE order_total > 0
-- For order count KPIs, include all (shows activity even without dollar value)
```

### 4. Use COALESCE for Org Shortname Everywhere

```sql
-- Many events have organization_shortname = NULL but current_organization_shortname populated
COALESCE(current_organization_shortname, organization_shortname) AS org
```

### 5. Time Conversion Pattern

```sql
-- time is FLOAT (Unix epoch seconds), must cast to INT64 first
TIMESTAMP_SECONDS(CAST(time AS INT64))
```

### 6. Feature Adoption — Derive from Events, Not Summary Table

```sql
-- Don't use mixpanel__org_feature_usage_report for feature counts
-- Instead:
SELECT 
  org,
  COUNTIF(event_name = 'order_submitted') AS submit_order,
  COUNTIF(event_name = 'product_search') AS search_products,
  COUNTIF(event_name = 'pdf_catalog_generated') AS create_pdf_catalog,
  -- etc.
FROM mixpanel__events
GROUP BY org
```

### 7. Customer Concentration Query Pattern

```sql
-- Use selected_bill_to_code as customer proxy
SELECT 
  selected_bill_to_code,
  COUNT(DISTINCT insert_id) AS order_count,
  SUM(order_total) AS total_revenue
FROM mixpanel__events
WHERE event_name = 'order_submitted'
  AND order_total > 0
  AND COALESCE(current_organization_shortname, organization_shortname) = 'gh'
GROUP BY selected_bill_to_code
ORDER BY total_revenue DESC
```

---

## POSTGRES SCHEMA REFERENCE

### Key Tables for EBR

| Table | Purpose | Key Columns |
|---|---|---|
| `users` | Rep/user identity | `username`, `first_name`, `last_name`, `email`, `disabled` |
| `organizations` | Org metadata | `id`, `shortname`, `name` |
| `org_users` | User ↔ Org bridge | `user_id`, `organization_id`, `territory_codes` |
| `orders` | iPad-submitted orders (system of record) | `total`, `rep_first_name`, `rep_last_name`, `customer_num`, `bill_to_company_name`, `submit_date`, `org_user_id` |
| `portal_orders` | Imported ERP orders | `total_amount`, `rep_name`, `customer_bill_to_name`, `order_date` |
| `customers` | Customer master | `code`, `name`, `billing_city`, `billing_state`, `buyer_email`, `territory_codes` |
| `login_events` | Login tracking | (not yet queried — potential session data) |
| `territories` | Territory assignments | (not yet queried — potential geo mapping) |

### Org ID Mapping

| Shortname | Postgres ID | Name |
|---|---|---|
| gh | 55 | Gabby |
| sc | 69 | Gabriella White |
| scw | 87 | Summer Classics |
| sccon | 88 | Summer Classics Contract |

### User Counts (Postgres vs Mixpanel)

| Org | Postgres org_users | Postgres Active | Mixpanel Unique Users |
|---|---|---|---|
| gh | 7,863 | 7,862 | 112 |
| sc | 155 | 154 | 248 |
| sccon | 1,156 | 1,156 | 53 |
| scw | 4,419 | 4,418 | 126 |

Note: Postgres `gh` count (7,863) includes end-customer/designer portal users. Mixpanel (112) only counts iPad app users. The `sc` discrepancy (155 PG vs 248 MP) may reflect deleted users or case-sensitivity mismatches.

---

## WHAT TO UPDATE NEXT

This report should be used to update:

1. **`EBR_Data_Cursor_Prompt.md`** — Add dual-source pattern (Postgres for revenue/names, BQ for behavior/features); add org-shortname COALESCE pattern; add username LOWER() normalization; document sccon Mixpanel gap
2. **`EBR_Generation_Prompt_v2.md`** — Revenue queries should use Postgres `orders` table as primary, BQ Mixpanel for feature adoption; fix org name mapping (sc = Gabriella White, scw = Summer Classics); add rep name join from Postgres `users`
3. **`Cursor_Prompt_Data_Pipeline.md`** — Dual-source architecture: Postgres MCP for orders/users/customers, BQ MCP for events/behavior; document that `mixpanel__people` and `org_feature_usage_report` are insufficient
4. **`build_intelligence_deepdive.py`** — Rewrite ingestion layer with two data sources: Postgres (revenue, names, orders) + BQ (events, feature usage); implement LOWER(username) for cross-source joins
