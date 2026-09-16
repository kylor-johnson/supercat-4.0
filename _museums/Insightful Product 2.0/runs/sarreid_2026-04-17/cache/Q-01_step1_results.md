# Q-01 Step 1 — Mixpanel Behavioral Data (VM-01)

| Field | Value |
|---|---|
| **Query ID** | Q-01 Step 1 |
| **Value Moment** | VM-01 |
| **Source** | BigQuery `mixpanel.user_feature_usage_report` |
| **Org** | SARREID (sarreid, org_id=1) |
| **Run Date** | 2026-04-17 |
| **Rows Returned** | 93 |

> **Note:** Q-01 Step 1 is from BigQuery user_feature_usage_report (all-time cumulative). The full raw dataset has 93 users. This cache file contains the top 30+ users by total_events. Non-selling users are listed separately for Q-04 cross-reference. Full column set in source: username, days_active, total_events, customer_targeting, product_discovery, config_bundling, presentation, information, submit_order.

---

**Top users (sorted by submit_order descending):**

| username | days_active | total_events | customer_targeting | product_discovery | config_bundling | presentation | information | submit_order |
|----------|------------|-------------|-------------------|------------------|----------------|-------------|------------|-------------|
| jaa | 498 | 8,136 | — | — | — | — | — | 144 |
| cwb | 510 | 7,357 | — | — | — | — | — | 104 |
| dklein | 438 | 6,878 | — | — | — | — | — | 84 |
| cdq6175 | 395 | 7,596 | — | — | — | — | — | 67 |
| moloffo | 176 | 3,745 | — | — | — | — | — | 67 |
| stanterry | 475 | 5,463 | — | — | — | — | — | 61 |
| ryan | 408 | 4,613 | — | — | — | — | — | 60 |
| dannigreen | 378 | 3,242 | — | — | — | — | — | 56 |
| joanharrison | 427 | 6,249 | — | — | — | — | — | 53 |
| kurtmuller | 249 | 2,306 | — | — | — | — | — | 34 |
| ripnance | 132 | 1,858 | — | — | — | — | — | 30 |
| jgraubart | 179 | 1,794 | — | — | — | — | — | 28 |
| dholbrook | 278 | 1,852 | — | — | — | — | — | 26 |
| hhoxworth | 227 | 1,498 | — | — | — | — | — | 21 |
| kkseidl | 325 | 3,698 | — | — | — | — | — | 13 |
| acymrot | 127 | 416 | — | — | — | — | — | 11 |
| rfernandini | 161 | 1,298 | — | — | — | — | — | 10 |
| ngodwin | 261 | 1,548 | — | — | — | — | — | 8 |
| cookieb | 107 | 588 | — | — | — | — | — | 7 |
| ngodwin2 | 111 | 1,002 | — | — | — | — | — | 6 |
| clinker | 207 | 2,385 | — | — | — | — | — | 6 |
| dlinker | 214 | 2,194 | — | — | — | — | — | 5 |
| ryanmoeller | 39 | 346 | — | — | — | — | — | 5 |
| cannon | 14 | 124 | — | — | — | — | — | 3 |
| sknaak | 57 | 240 | — | — | — | — | — | 3 |
| rafebethell | 221 | 1,594 | — | — | — | — | — | 3 |
| jbertelsen | 62 | 631 | — | — | — | — | — | 2 |
| nashgilbert | 21 | 205 | — | — | — | — | — | 2 |

**Non-selling notable users (submit_order ≤ 2, high activity):**

| username | days_active | total_events | submit_order | key_metrics | classified_role |
|----------|------------|-------------|-------------|-------------|----------------|
| msharpe2 | 392 | 10,889 | 0 | search_products=4,529 · create_pdf_catalog=72 · my_list_activity=370 | Catalog/Data Manager |
| slanier | 265 | 5,021 | 0 | search_products=1,081 · create_pdf_catalog=109 | Catalog/Data Manager |
| wh4 | 313 | 4,049 | 0 | search_products=2,639 | Sales Support/Inside Sales (warehouse) |
| wh3 | 335 | 3,664 | 0 | search_products=1,903 | Sales Support/Inside Sales (warehouse) |
| coley | 239 | 3,125 | 0 | search_products=1,490 | Catalog/Data Manager |
| bcates | 295 | 2,746 | 0 | search_products=583 · data_exports=50 | Catalog/Data Manager |

> Remaining ~59 users in the full dataset are low-activity or inactive accounts (see Q-04 for full classification). Category-level breakdowns (customer_targeting, product_discovery, config_bundling, presentation, information) available in BigQuery source — this cache captures the summary-level metrics dictated during Stage 1 data gathering.
