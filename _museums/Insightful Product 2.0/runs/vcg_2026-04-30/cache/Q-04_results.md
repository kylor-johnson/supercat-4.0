# Q-04: Non-Selling User Role Classification — Visual Comfort Signature (vcg, org_id=141)
- **Source**: BigQuery MCP (mixpanel.user_feature_usage_report) + Postgres user group mapping
- **Run date**: 2026-04-30
- **Classification**: Users with submit_order = 0 in Mixpanel behavioral data
- **Row count**: 21 non-selling users identified in top 55 Mixpanel users

## Non-Selling Users by Behavioral Profile

| Username | User Group | Days Active | Total Events | Dominant Behavior | Classification |
|----------|-----------|-------------|-------------|-------------------|---------------|
| tsecson | Sales Reps | 463 | 20,583 | search_products (2,716), search_for_customer (1,835), select_a_customer (968) | Catalog Power User — zero orders despite massive engagement |
| acastaneda | Sales Reps | 281 | 5,540 | search_products (1,720), search_for_customer (645), select_a_customer (302) | Catalog Power User — heavy research, no order submissions |
| bob1 | (not in org_users) | 389 | 3,750 | search_products (1,916), select_a_customer (488) | Catalog Browser — possible external/legacy account |
| tedteuten | Sales Reps | 103 | 2,022 | search_products (704), search_for_customer (81), select_a_customer (77) | Catalog Browser — moderate activity |
| johnnynelis | Sales Reps | 112 | 1,911 | search_products (580), view_library_entry (58), select_a_customer (48) | Content Consumer + Browser |
| randy1 | Sales Reps | 443 | 1,868 | search_products (163), select_a_customer (101), view_library_entry (79) | Diversified — long tenure, broad feature usage |
| lvanderbent | Sales Reps | 245 | 1,809 | search_products (492), search_for_customer (237), select_a_customer (153) | Customer Manager — heavy customer targeting |
| fdenegri | Sales Reps | 123 | 1,232 | search_products (622), select_a_customer (153), search_for_customer (105) | Catalog Browser + Customer Targeting |
| daveake | (not in org_users) | 85 | 1,214 | search_products (297), search_for_customer (165), view_library_entry (85) | Content Consumer — possible external account |
| ypovolotskiy | (not in org_users) | 57 | 1,101 | search_products (137), search_for_customer (112) | Customer Manager — possible external account |
| jmetekingi | (not in org_users) | 199 | 1,083 | search_products (238), select_a_customer (85) | Catalog Browser — possible external account |
| greggf | Sales Reps | 101 | 1,065 | search_products (522), select_a_customer (99), view_library_entry (74) | Catalog Browser + Content Consumer |
| jevans1 | Sales Reps | 118 | 811 | search_products (312), select_a_customer (98), view_library_entry (40) | Catalog Browser |
| arienne | Sales Reps | 167 | 736 | search_products (195), search_for_customer (49), select_a_customer (17) | Catalog Browser — low intensity |
| mgubakin | (not in org_users) | 111 | 629 | search_products (205), view_library_entry (83), select_a_customer (38) | Content Consumer — possible external account |
| katiep | Sales Reps | 39 | 446 | search_for_customer (36), select_a_customer (30), view_library_entry (10) | Customer Manager — low activity |
| foliveira | Sales Reps | 63 | 373 | search_products (113), search_for_customer (54), select_a_customer (38) | Catalog Browser — low activity |
| swt | z-SuperCat | 24 | 354 | search_for_customer (45), select_a_customer (41), view_library_entry (29) | Internal — SuperCat staff |
| brittneyh | Sales Reps | 48 | 339 | search_products (63), view_library_entry (50), create_pdf_catalog (11) | Content Consumer + Presenter |
| jpomeroy | Sales Reps | 11 | 319 | search_products (230), select_a_customer (15) | Catalog Browser — low tenure |
| wendyc | (not in org_users) | 27 | 309 | select_a_customer (22), search_for_customer (17) | Customer Manager — possible external account |

## Classification Summary

| Classification | Count | Avg Events | Avg Days Active |
|---------------|-------|-----------|----------------|
| Catalog Power User | 2 | 13,062 | 372 |
| Catalog Browser | 8 | 1,044 | 133 |
| Customer Manager | 4 | 935 | 97 |
| Content Consumer | 3 | 744 | 87 |
| Diversified | 1 | 1,868 | 443 |
| Internal (SuperCat) | 1 | 354 | 24 |
| Content Consumer + Presenter | 1 | 339 | 48 |
| Content Consumer + Browser | 1 | 1,911 | 112 |

## Notes
- 6 of 21 non-selling users (bob1, daveake, ypovolotskiy, jmetekingi, mgubakin, wendyc) are NOT in the Postgres org_users table — may be former users, external demo accounts, or Mixpanel tracking artifacts.
- tsecson is the highest-activity non-seller (20,583 events, 463 days active) — Sales Reps group. Likely a catalog specialist or internal support role.
- jevans1 (Jason Evans) IS in orders table with 16 orders/$34,784 GMV but shows submit_order = 0 in Mixpanel — possible Mixpanel attribution gap for this user.
